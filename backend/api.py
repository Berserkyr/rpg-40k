"""
Backend FastAPI - Survivant de Ruche
Expose les systemes de jeu via REST + SSE pour la reponse en streaming du MJ.
"""
from __future__ import annotations

import asyncio
import json
import os
import random
from pathlib import Path
from typing import AsyncIterator, Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from backend.database import (
    DATABASE_PATH, create_account, ensure_user, get_account, init_db,
    list_users, normalize_user_id, record_event, touch_last_seen,
)
from backend.auth import (
    CurrentUser, ROLE_ADMIN, ROLE_PLAYER, create_access_token,
    get_current_user, hash_password, require_admin, verify_password,
)

load_dotenv()

# ---------------------------------------------------------------------------
# Imports des systemes
# ---------------------------------------------------------------------------
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.state import CharacterState
from src.prompt_builder import build_system_prompt
from src.dice import format_roll, roll_2d6
from src.entities import (
    Faction, ThreatLevel, generate_entity, generate_encounter,
    entity_body_type, HOSTILE_FACTIONS,
)
from src.combat import (
    Combatant, CombatState, resolve_attack, resolve_flee,
    CoverType, CombatRange, use_combat_ability, compute_tactical_advantage,
    get_available_abilities, enemy_ai_action, ActionType,
)
from src.negotiation import (
    NegotiationApproach, attempt_negotiation, approach_from_str, is_negotiable,
)
from src.team import (
    Team, Companion, create_companion, available_templates,
)
from src.inventory import (
    Inventory, generate_loot, WEAPON_TEMPLATES, ARMOR_TEMPLATES,
    create_weapon, create_armor,
)
from src.progression import (
    ProgressionState, SKILL_TREE, award_xp,
    format_skill_tree, get_available_skills, get_unlocked_skills,
    calculate_total_bonuses, get_special_abilities, serialize_skill_tree,
)
from src.world import WorldMap, create_starting_map, format_zone_info, format_map_overview
from src.quests import QuestLog, create_starting_quests, format_quest_log, format_quest_info
from src.relationships import (
    RelationshipManager, create_starting_relationships,
    format_relationships_overview,
)
from src.persistence import GameWorld, create_new_game_world, format_world_status, generate_gm_context

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(title="Survivant de Ruche API", version="1.0.0", debug=True)
init_db()


def _cors_origins() -> list[str]:
    """Origines CORS autorisées.

    En production, définir `CORS_ALLOWED_ORIGINS` (liste séparée par des virgules)
    pour restreindre l'accès. Par défaut, ouvre tout en développement uniquement.
    Sécurité : couvre OWASP A05 (Security Misconfiguration).
    """
    raw = os.getenv("CORS_ALLOWED_ORIGINS", "").strip()
    if not raw:
        return ["*"]
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Sessions utilisateurs en memoire, avec sauvegardes isolees par utilisateur
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.parent
SAVE_DIR = BASE_DIR / "saves"
CHARACTER_FILE = BASE_DIR / "character_sheet.yaml"
PROMPT_FILE = BASE_DIR / "prompt_survivant.md"
CAMPAIGN = "campagne1"


class Session:
    """Etat de session charge en memoire."""

    def __init__(self, user_id: str = "default") -> None:
        self.user_id = normalize_user_id(user_id)
        save_dir = _save_dir_for_user(self.user_id)
        save_dir.mkdir(parents=True, exist_ok=True)

        self.character = CharacterState.from_file(CHARACTER_FILE)
        self.world = GameWorld.load(save_dir) or create_new_game_world(CAMPAIGN)
        self._load_subsystems(save_dir)
        self.combat: Optional[CombatState] = None
        self.messages: list[dict] = [
            {"role": "system", "content": self._build_prompt()}
        ]
        self.save_dir = save_dir

    def _load_subsystems(self, save_dir: Path) -> None:
        import yaml

        def _load(fname: str, cls, fallback):
            p = save_dir / fname
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                    if hasattr(cls, "from_dict"):
                        return cls.from_dict(data)
            return fallback()

        self.progression = _load("progression.yaml", ProgressionState, ProgressionState)
        self.inventory = _load(
            "inventory.yaml", Inventory,
            lambda: _init_inventory(),
        )
        self.world_map = _load("world_map.yaml", WorldMap, create_starting_map)
        self.quest_log = _load("quests.yaml", QuestLog, create_starting_quests)
        self.relationships = _load("relationships.yaml", RelationshipManager, create_starting_relationships)
        self.team = _load("team.yaml", Team, Team)

    def _build_prompt(self) -> str:
        base = build_system_prompt(PROMPT_FILE, self.character)
        return f"{base}\n\n{generate_gm_context(self.world)}"

    def save(self) -> None:
        import yaml
        self.world.save(self.save_dir)
        for fname, obj in [
            ("progression.yaml", self.progression),
            ("inventory.yaml", self.inventory),
            ("world_map.yaml", self.world_map),
            ("quests.yaml", self.quest_log),
            ("relationships.yaml", self.relationships),
            ("team.yaml", self.team),
        ]:
            with open(self.save_dir / fname, "w", encoding="utf-8") as f:
                yaml.safe_dump(obj.to_dict(), f, allow_unicode=True)

    def _progression_payload(self) -> dict:
        """Serialise la progression enrichie (arbre + competences disponibles)."""
        payload = self.progression.to_dict()
        payload["skill_tree"] = serialize_skill_tree(self.progression)
        payload["available_skills"] = [
            s.id for s in SKILL_TREE.values()
            if self.progression.can_unlock_with_point(s)[0]
        ]
        payload["unlocked_skills"] = list(self.progression.skills_unlocked)
        return payload

    def full_state(self) -> dict:
        """Sérialise tout l'etat visible par l'UI."""
        zone = self.world_map.get_current_zone()
        build = _character_build(self)
        return {
            "user": {"id": self.user_id},
            "character": self.character.to_dict(),
            "character_build": build,
            "progression": self._progression_payload(),
            "inventory": self.inventory.to_dict(),
            "world": self.world.to_dict(),
            "world_map": self.world_map.to_dict(),
            "current_zone": zone.to_dict() if zone else None,
            "accessible_zones": [z.to_dict() for z in self.world_map.get_accessible_zones()],
            "active_quests": [
                q.to_dict() for q in self.quest_log.get_active_quests()
            ],
            "available_quests": [
                q.to_dict() for q in self.quest_log.get_available_quests()
            ],
            "relationships": {
                "factions": {
                    fid: {"name": f.name, "reputation": f.reputation, "level": f.get_level().name}
                    for fid, f in self.relationships.factions.items()
                },
                "npcs": [
                    {"id": n.id, "name": n.name, "role": n.role, "disposition": n.disposition.value}
                    for n in self.relationships.get_met_npcs()
                ],
            },
            "combat": _combat_state(self.combat),
            "team": {
                "members": [m.to_dict() for m in self.team.members],
                "max_size": self.team.max_size,
                "available": available_templates(self.progression.level),
            },
        }


def _init_inventory() -> Inventory:
    inv = Inventory()
    knife = create_weapon("knife")
    helmet = create_armor("worker_helmet")
    if knife:
        inv.add_item(knife)
    if helmet:
        inv.add_item(helmet)
    return inv


def _combat_state(combat: Optional[CombatState]) -> Optional[dict]:
    if not combat:
        return None
    living = combat.get_living_enemies()
    spokesperson_faction = (
        getattr(living[0], "faction_id", "tyranide") if living else "tyranide"
    )
    return {
        "active": combat.is_active,
        "turn": combat.turn_number,
        "player": {
            "name": combat.player.name,
            "health": combat.player.health,
            "max_health": combat.player.max_health,
            "action_points": combat.player.action_points,
            "max_action_points": combat.player.max_action_points,
            "cover": combat.player.cover.value,
            "is_aiming": combat.player.is_aiming,
            "is_defending": combat.player.is_defending,
            "conditions": combat.player.active_conditions(),
        },
        "abilities": get_available_abilities(combat.player.abilities),
        "enemies": [
            {
                "name": e.name,
                "health": e.health,
                "max_health": e.max_health,
                "is_dead": e.is_dead,
                "cover": e.cover.value,
                "conditions": e.active_conditions(),
                "faction": getattr(e, "faction_id", "tyranide"),
                "threat": getattr(e, "threat_id", "standard"),
                "archetype": getattr(e, "archetype", "beast"),
            }
            for e in combat.enemies
        ],
        "allies": [
            {
                "name": a.name,
                "health": a.health,
                "max_health": a.max_health,
                "is_dead": a.is_dead,
                "conditions": a.active_conditions(),
            }
            for a in combat.allies
        ],
        "negotiable": is_negotiable(spokesperson_faction),
    }


def _character_build(session: Session) -> dict:
    """Calcule les attributs effectifs dynamiques du personnage.

    Sources de bonus:
    - niveau du personnage
    - équipement porté (armes/armures)
    - compétences (skills), talents passifs et dons spéciaux
    """
    base_attributes = session.character.attributes.copy()
    progression = session.progression
    inventory = session.inventory

    level = progression.level
    unlocked = get_unlocked_skills(progression)
    passive_bonuses = calculate_total_bonuses(progression)
    special_abilities = get_special_abilities(progression)

    equipment_bonus = {
        "attaque": 0,
        "defense": inventory.total_defense_bonus(),
        "precision": 0,
        "pv_max": 0,
    }
    equipment_traits: list[str] = []

    if inventory.weapon_main:
        equipment_bonus["attaque"] += max(1, inventory.weapon_main.damage // 2)
        equipment_bonus["precision"] += inventory.weapon_main.accuracy
        equipment_traits.extend(inventory.weapon_main.special_abilities)
    if inventory.weapon_secondary:
        equipment_bonus["attaque"] += max(0, inventory.weapon_secondary.damage // 3)
        equipment_bonus["precision"] += max(0, inventory.weapon_secondary.accuracy)
        equipment_traits.extend(inventory.weapon_secondary.special_abilities)
    if inventory.armor_body and inventory.armor_body.special_properties:
        equipment_traits.extend(inventory.armor_body.special_properties)
    if inventory.armor_head and inventory.armor_head.special_properties:
        equipment_traits.extend(inventory.armor_head.special_properties)

    level_bonus = {
        "attaque": max(0, (level - 1) // 2),
        "defense": max(0, (level - 1) // 3),
        "pv_max": max(0, (level - 1) * 2),
    }

    talents = [s.name for s in unlocked if s.passive]
    gifts = []
    if level >= 3:
        gifts.append("Instinct de vétéran")
    if level >= 5:
        gifts.append("Volonté inébranlable")
    if level >= 7:
        gifts.append("Présence héroïque")
    if any((i and i.rarity.value == "relique") for i in [inventory.weapon_main, inventory.weapon_secondary, inventory.armor_body, inventory.armor_head]):
        gifts.append("Porteur de relique")

    effective_attributes = base_attributes.copy()
    for key, value in passive_bonuses.items():
        effective_attributes[key] = effective_attributes.get(key, 0) + value

    combat_skill = (
        effective_attributes.get("robustesse", 2)
        + effective_attributes.get("discretion", 2)
        + passive_bonuses.get("attaque", 0)
        + equipment_bonus["attaque"]
        + level_bonus["attaque"]
    )
    defense_skill = (
        effective_attributes.get("sang_froid", 3)
        + equipment_bonus["defense"]
        + level_bonus["defense"]
    )
    speed_skill = effective_attributes.get("ingeniosite", 3) + passive_bonuses.get("technique", 0)
    special_skill = effective_attributes.get("foi", 2) + passive_bonuses.get("resistance_corruption", 0)
    max_health = (
        10
        + max(0, effective_attributes.get("robustesse", 2) - 2) * 2
        + passive_bonuses.get("pv_max", 0)
        + level_bonus["pv_max"]
    )

    return {
        "level": level,
        "base_attributes": base_attributes,
        "effective_attributes": effective_attributes,
        "derived_stats": {
            "combat": combat_skill,
            "defense": defense_skill,
            "speed": speed_skill,
            "special": special_skill,
            "max_health": max_health,
            "precision": equipment_bonus["precision"],
        },
        "bonuses": {
            "skills": passive_bonuses,
            "equipment": equipment_bonus,
            "level": level_bonus,
        },
        "skills": [{"id": s.id, "name": s.name, "category": s.category.value} for s in unlocked],
        "talents": talents,
        "special_gifts": gifts,
        "special_abilities": sorted(set(special_abilities + equipment_traits)),
    }


# Sessions en memoire
_session: Optional[Session] = None
_sessions: dict[str, Session] = {}


def _save_dir_for_user(user_id: str) -> Path:
    """Retourne le dossier de sauvegarde d'un utilisateur."""
    safe_user = normalize_user_id(user_id)
    if safe_user == "default":
        return SAVE_DIR / CAMPAIGN
    return SAVE_DIR / "users" / safe_user / CAMPAIGN


def current_user_id(user: CurrentUser = Depends(get_current_user)) -> str:
    """Résout l'utilisateur courant à partir du jeton JWT (Authorization: Bearer)."""
    return normalize_user_id(user.username)


def get_session(user_id: str = "default") -> Session:
    global _session
    safe_user = normalize_user_id(user_id)
    ensure_user(safe_user)
    if safe_user == "default":
        if _session is None:
            _session = Session(safe_user)
        return _session
    if safe_user not in _sessions:
        _sessions[safe_user] = Session(safe_user)
    return _sessions[safe_user]


# ---------------------------------------------------------------------------
# OpenAI client
# ---------------------------------------------------------------------------
def get_openai_client() -> AsyncOpenAI:
    key = os.getenv("OPENAI_API_KEY", "")
    if not key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY manquant")
    return AsyncOpenAI(api_key=key)


def _offline_gm_text(
    session: Session,
    user_message: str,
    opening: bool = False,
    missing_key_notice: bool = True,
) -> str:
    """Fallback local: permet de jouer même sans OPENAI_API_KEY."""
    zone = session.world_map.get_current_zone()
    zone_name = zone.name if zone else "zone inconnue"
    accessible = session.world_map.get_accessible_zones()
    exits = ", ".join(z.name for z in accessible[:3]) or "aucune sortie claire"

    if opening:
        prefix = "[MODE MJ LOCAL — aucune clé OPENAI_API_KEY détectée]\n\n" if missing_key_notice else ""
        return (
            prefix
            + f"Karimus reprend conscience dans {zone_name}. Les alarmes de la ruche hurlent, "
            "les conduites vox crachent des prières fragmentées et la poussière de ferro-béton "
            "tombe du plafond comme une cendre grise. Au loin, quelque chose gratte contre les cloisons.\n\n"
            f"Issues repérées : {exits}.\n"
            "Objectif immédiat : sécuriser la famille, trouver des provisions, puis choisir une route sûre."
        )

    lower = user_message.lower()
    if any(word in lower for word in ("fouille", "chercher", "loot", "provision")):
        return (
            f"Karimus fouille {zone_name} avec méthode. Un jet de dé peut aider à savoir si le bruit attire "
            "quelque chose. Utilisez le bouton [FOUILLER] pour générer du butin concret."
        )
    if any(word in lower for word in ("attaque", "combat", "ennemi", "tir")):
        return (
            "Les ombres répondent par un cliquetis chitineux. Utilisez [RENCONTRE] pour générer une menace, "
            "puis les boutons de combat pour résoudre l'affrontement."
        )
    if any(word in lower for word in ("aller", "partir", "déplacer", "deplacer", "route")):
        return (
            f"Les passages accessibles depuis {zone_name} sont : {exits}. Cliquez une destination dans le panneau "
            "d'actions pour voyager et déclencher un éventuel incident."
        )

    return (
        f"Dans {zone_name}, votre action — « {user_message} » — produit un bref silence inquiet. "
        "La ruche semble retenir son souffle. Choisissez une action : lancer les dés, fouiller, voyager ou provoquer une rencontre."
    )


async def _yield_text_as_sse(text: str) -> AsyncIterator[str]:
    """Diffuse du texte en petits fragments façon streaming."""
    for i in range(0, len(text), 14):
        await asyncio.sleep(0.015)
        yield json.dumps({"type": "token", "content": text[i:i + 14]})


async def _gm_stream(session: Session, user_message: str, opening: bool = False) -> AsyncIterator[str]:
    """Stream OpenAI si disponible, sinon fallback local jouable."""
    key = os.getenv("OPENAI_API_KEY", "")
    full_text = ""

    if not key:
        full_text = _offline_gm_text(session, user_message, opening=opening)
        async for event in _yield_text_as_sse(full_text):
            yield event
    else:
        try:
            client = AsyncOpenAI(api_key=key)
            stream = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=session.messages,
                stream=True,
            )
            async for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    full_text += delta
                    yield json.dumps({"type": "token", "content": delta})
        except Exception as exc:
            full_text = (
                f"[MODE MJ LOCAL — OpenAI indisponible: {exc}]\n\n"
                + _offline_gm_text(session, user_message, opening=opening, missing_key_notice=False)
            )
            async for event in _yield_text_as_sse(full_text):
                yield event

    session.messages.append({"role": "assistant", "content": full_text})
    session.world.advance_scene()
    changes = session.character.apply_updates_from_text(full_text)
    expired = session.quest_log.advance_all_timers()
    session.save()
    yield json.dumps({
        "type": "done",
        "changes": changes,
        "expired_quests": expired,
        "state": session.full_state(),
    })


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str


class CommandRequest(BaseModel):
    command: str
    args: list[str] = []


class TravelRequest(BaseModel):
    zone_id: str


class SpawnRequest(BaseModel):
    faction: str = "tyranide"
    level: str = "standard"
    count: Optional[int] = None  # nombre total d'ennemis (None = auto varie)


class EquipRequest(BaseModel):
    item_id: str
    slot: str = "main"  # main|secondary|body|head


class UnequipRequest(BaseModel):
    slot: str  # weapon_main|weapon_secondary|armor_body|armor_head


class AttributeAllocationRequest(BaseModel):
    attribute: str
    points: int = 1


class ConsumableRequest(BaseModel):
    item_id: str


class CombatActionRequest(BaseModel):
    command: str                     # attack|aim|cover|defend|flee|ability
    target: int = 0                  # index de l'ennemi cible
    ability_id: Optional[str] = None  # capacite a utiliser (command == "ability")


class NegotiateRequest(BaseModel):
    approach: str = "persuasion"     # persuasion|intimidation|marchandage
    target: int = 0                  # index de l'ennemi vise (porte-parole)


class RecruitRequest(BaseModel):
    template_id: str                 # archetype du compagnon (ex: "milicien")


def _improve_wound_track(current: str) -> str:
    order = ["Condamne", "Fracture", "Erafle", "Indemne"]
    try:
        idx = order.index(current)
    except ValueError:
        return "Indemne"
    return order[min(len(order) - 1, idx + 1)]

def _apply_consumable_effect(session: Session, item) -> str:
    """Applique l'effet d'un consommable sur l'état du personnage."""
    effect = getattr(item, "effect_type", "")
    value = int(getattr(item, "effect_value", 0) or 0)

    if effect == "heal":
        before = str(session.character.tracks.get("blessures", "Indemne"))
        session.character.tracks["blessures"] = _improve_wound_track(before)
        if session.character.tracks["blessures"] == before:
            # Si deja indemne, on convertit en reduction de stress
            stress = int(session.character.tracks.get("stress", 0) or 0)
            reduced = min(stress, max(1, value // 2))
            session.character.tracks["stress"] = max(0, stress - reduced)
            return f"{item.name}: -{reduced} stress."
        return f"{item.name}: blessures {before} -> {session.character.tracks['blessures']}."

    if effect == "cure":
        corruption = int(session.character.tracks.get("corruption", 0) or 0)
        reduced = min(corruption, max(1, value))
        session.character.tracks["corruption"] = max(0, corruption - reduced)
        return f"{item.name}: -{reduced} corruption."

    if effect == "buff":
        stress = int(session.character.tracks.get("stress", 0) or 0)
        reduced = min(stress, max(1, value))
        session.character.tracks["stress"] = max(0, stress - reduced)
        return f"{item.name}: regain de focus, -{reduced} stress."

    return f"{item.name} utilise sans effet notable."



class UserRequest(BaseModel):
    user_id: str
    display_name: str | None = None


class RegisterRequest(BaseModel):
    username: str
    password: str
    display_name: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health_check():
    """Retourne l'etat de sante minimal de l'API."""
    return {
        "status": "ok",
        "service": "survivant-de-ruche-api",
        "version": app.version,
        "database": str(DATABASE_PATH),
    }


@app.post("/api/auth/register", status_code=201)
def register(req: RegisterRequest):
    """Crée un compte joueur avec mot de passe haché et retourne un JWT."""
    username = normalize_user_id(req.username)
    if not username or username == "default":
        raise HTTPException(status_code=400, detail="Identifiant invalide.")
    digest = hash_password(req.password)
    try:
        account = create_account(username, digest, req.display_name, role=ROLE_PLAYER)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    record_event(username, "register")
    token = create_access_token(account["id"], account["role"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": account["id"], "display_name": account["display_name"], "role": account["role"]},
    }


@app.post("/api/auth/login")
def login(req: LoginRequest):
    """Authentifie un utilisateur et retourne un JWT."""
    username = normalize_user_id(req.username)
    account = get_account(username)
    if not account or not account.get("password_hash") or not verify_password(req.password, account["password_hash"]):
        raise HTTPException(status_code=401, detail="Identifiants incorrects.")
    touch_last_seen(username)
    record_event(username, "login")
    token = create_access_token(account["id"], account["role"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": account["id"], "display_name": account["display_name"], "role": account["role"]},
    }


@app.get("/api/auth/me")
def me(user: CurrentUser = Depends(get_current_user)):
    """Retourne l'identité de l'utilisateur authentifié."""
    account = get_account(user.username)
    if not account:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable.")
    return {"id": account["id"], "display_name": account["display_name"], "role": account["role"]}


@app.get("/api/users")
def users(_admin: CurrentUser = Depends(require_admin)):
    """Liste les utilisateurs connus (réservé aux administrateurs)."""
    return {"users": list_users()}


@app.get("/api/state")
def get_state(user_id: str = Depends(current_user_id)):
    """Retourne l'etat complet de la session."""
    return get_session(user_id).full_state()


@app.post("/api/start")
async def start_game(user_id: str = Depends(current_user_id)):
    """Demarre une nouvelle scene d'ouverture (SSE streaming)."""
    session = get_session(user_id)

    opening_prompt = "Lance la scene d'ouverture. Karimus se reveille dans le chaos de l'invasion tyranide."

    if session.world.global_state.total_scenes == 0:
        session.messages.append({
            "role": "user",
            "content": opening_prompt,
        })

    return EventSourceResponse(_gm_stream(session, opening_prompt, opening=True))


@app.post("/api/chat")
async def chat(req: ChatRequest, user_id: str = Depends(current_user_id)):
    """Envoie un message au MJ et streame la reponse."""
    session = get_session(user_id)
    session.messages.append({"role": "user", "content": req.message})
    return EventSourceResponse(_gm_stream(session, req.message))


@app.post("/api/roll")
def roll_dice(_user: str = Depends(current_user_id)):
    """Lance 2d6 et retourne le resultat."""
    result = roll_2d6()
    return {"formatted": format_roll(result), "total": result.total, "values": result.values}


@app.post("/api/spawn")
def spawn_entity(req: SpawnRequest, _user: str = Depends(current_user_id)):
    """Genere une entite procedural."""
    faction_map = {
        "tyranide": Faction.TYRANID,
        "culte": Faction.GENESTEALER_CULT,
        "garde": Faction.IMPERIAL_GUARD,
        "civil": Faction.CIVILIAN,
        "chaos": Faction.CHAOS,
    }
    level_map = {
        "sbire": ThreatLevel.MINION,
        "standard": ThreatLevel.STANDARD,
        "elite": ThreatLevel.ELITE,
        "boss": ThreatLevel.BOSS,
    }
    faction = faction_map.get(req.faction.lower(), Faction.TYRANID)
    level = level_map.get(req.level.lower(), ThreatLevel.STANDARD)
    entity = generate_entity(faction, level)
    return {
        "name": entity.name,
        "faction": entity.faction.value,
        "threat_level": entity.threat_level.value,
        "stats": {
            "combat": entity.stats.combat,
            "defense": entity.stats.defense,
            "speed": entity.stats.speed,
            "special": entity.stats.special,
        },
        "abilities": list(entity.abilities),
        "description": entity.description,
    }


@app.post("/api/combat/start")
def start_combat(req: SpawnRequest, user_id: str = Depends(current_user_id)):
    """Demarre un combat, potentiellement contre un groupe varie d'ennemis."""
    session = get_session(user_id)
    faction_map = {
        "tyranide": Faction.TYRANID,
        "culte": Faction.GENESTEALER_CULT,
        "culte_genestealer": Faction.GENESTEALER_CULT,
        "chaos": Faction.CHAOS,
        "mechanicus": Faction.MECHANICUS,
        "arbites": Faction.ARBITES,
        "ecclesiarchie": Faction.ECCLESIARCHY,
        "garde_imperiale": Faction.IMPERIAL_GUARD,
    }
    level_map = {"sbire": ThreatLevel.MINION, "standard": ThreatLevel.STANDARD,
                 "elite": ThreatLevel.ELITE, "boss": ThreatLevel.BOSS}
    key = req.faction.lower()
    if key in ("random", "aleatoire", "mixte"):
        faction = random.choice(HOSTILE_FACTIONS)
    else:
        faction = faction_map.get(key, Faction.TYRANID)
    level = level_map.get(req.level.lower(), ThreatLevel.STANDARD)

    enemies = _spawn_enemy_group(faction, level, req.count)

    player = Combatant.from_player_state(session.character)
    build = _character_build(session)
    derived = build.get("derived_stats", {})
    player.combat = int(derived.get("combat", player.combat))
    player.defense = int(derived.get("defense", player.defense))
    player.speed = int(derived.get("speed", player.speed))
    player.special = int(derived.get("special", player.special))
    player.max_health = int(derived.get("max_health", player.max_health))
    player.health = min(player.health, player.max_health)
    # Capacites actives issues des competences et traits d'equipement.
    player.abilities = list(build.get("special_abilities", []))
    player.action_points = player.max_action_points
    allies = _build_team_allies(session)
    session.combat = CombatState(player=player, enemies=enemies, allies=allies)
    session.save()
    ally_note = f" (+{len(allies)} allie(s))" if allies else ""
    lead = enemies[0].name
    group_note = f" et {len(enemies) - 1} autre(s)" if len(enemies) > 1 else ""
    return {
        "message": f"Combat contre {lead}{group_note}!{ally_note}",
        "combat": _combat_state(session.combat),
        "state": session.full_state(),
    }


def _make_enemy(faction: Faction, level: ThreatLevel) -> Combatant:
    """Genere un Combatant ennemi enrichi (faction, menace, silhouette)."""
    entity = generate_entity(faction, level)
    enemy = Combatant.from_entity(entity)
    enemy.faction_id = faction.value
    enemy.threat_id = level.value
    enemy.archetype = entity_body_type(entity)
    return enemy


def _spawn_enemy_group(faction: Faction, level: ThreatLevel, count: Optional[int]) -> list:
    """Construit un groupe d'ennemis varie selon le niveau de menace.

    Un chef du niveau demande est toujours present; des sbires l'accompagnent
    pour des combats de groupe plus dynamiques. `count` force le nombre total.
    """
    leader = _make_enemy(faction, level)
    group = [leader]

    if count is not None:
        extra = max(0, int(count) - 1)
        for _ in range(min(extra, 5)):
            group.append(_make_enemy(faction, ThreatLevel.MINION))
        return group

    if level == ThreatLevel.MINION:
        for _ in range(random.randint(1, 2)):
            group.append(_make_enemy(faction, ThreatLevel.MINION))
    elif level == ThreatLevel.STANDARD:
        for _ in range(random.randint(0, 2)):
            group.append(_make_enemy(faction, ThreatLevel.MINION))
    elif level in (ThreatLevel.ELITE, ThreatLevel.BOSS) and random.random() < 0.5:
        group.append(_make_enemy(faction, ThreatLevel.MINION))
    return group


def _build_team_allies(session: Session) -> list:
    """Construit les combattants allies a partir de l'equipe recrutee.

    La competence 'meneur' accorde +2 PV max a chaque compagnon.
    """
    build = _character_build(session)
    leader_bonus = 2 if "cri_ralliement" in build.get("special_abilities", []) else 0
    # 'meneur' est passif: detecte via les competences acquises.
    if session.progression.has_skill("meneur"):
        leader_bonus += 2
    allies = []
    for member in session.team.members:
        hp = member.max_health + leader_bonus
        allies.append(Combatant(
            name=member.name,
            is_player=False,
            combat=member.combat,
            defense=member.defense,
            speed=member.speed,
            special=member.special,
            health=hp,
            max_health=hp,
        ))
    return allies


_NO_AP_DETAIL = "Plus de points d'action"


def _spend_ap(player, cost: int = 1) -> None:
    """Depense des points d'action ou leve une erreur 400."""
    if player.action_points < cost:
        raise HTTPException(status_code=400, detail=_NO_AP_DETAIL)
    player.action_points -= cost


def _run_enemy_turn(combat, log: list) -> None:
    """Fait jouer chaque ennemi vivant (conditions, IA, attaque)."""
    for enemy in combat.get_living_enemies():
        # Conditions (saignement, etc.) puis controle (etourdi).
        log.extend(enemy.tick_conditions())
        if enemy.is_dead:
            log.append(f"{enemy.name} succombe a ses blessures!")
            continue
        if enemy.is_stunned():
            log.append(f"{enemy.name} est etourdi et perd son tour.")
            continue
        target = combat.player
        # Cible un allie proche parfois (combat de groupe).
        living_allies = [a for a in combat.allies if not a.is_dead]
        if living_allies and random.random() < 0.4:
            target = random.choice(living_allies)
        adv = compute_tactical_advantage(enemy, target, combat)
        result = resolve_attack(enemy, target, advantage=adv)
        log.append(result["description"])
        if result["hit"]:
            target.take_damage(result["damage"])


def _run_ally_turn(combat, log: list) -> None:
    """Fait agir chaque allie/compagnon vivant (combat de groupe)."""
    for ally in combat.allies:
        if ally.is_dead:
            continue
        log.extend(ally.tick_conditions())
        if ally.is_dead or ally.is_stunned():
            continue
        living_enemies = combat.get_living_enemies()
        if not living_enemies:
            break
        target = random.choice(living_enemies)
        adv = compute_tactical_advantage(ally, target, combat)
        result = resolve_attack(ally, target, advantage=adv)
        log.append(f"[Allie] {result['description']}")
        if result["hit"]:
            target.take_damage(result["damage"])


@app.post("/api/combat/action")
def combat_action(req: CombatActionRequest, user_id: str = Depends(current_user_id)):
    """Execute une action de combat tactique.

    Commandes: attack | aim | cover | defend | flee | ability.
    Le joueur agit tant qu'il a des points d'action; les commandes qui
    terminent le tour (defend/flee, ou epuisement des PA) declenchent le
    tour ennemi.
    """
    session = get_session(user_id)
    if not session.combat or not session.combat.is_active:
        raise HTTPException(status_code=400, detail="Pas de combat actif")

    combat = session.combat
    player = combat.player
    enemies = combat.get_living_enemies()
    log: list[str] = []

    if not enemies:
        combat.is_active = False
        session.save()
        return {"log": ["Plus d'ennemis!"], "combat": _combat_state(combat), "state": session.full_state(), "ended": True, "victory": True}

    # Selection de la cible par index (borne).
    idx = max(0, min(req.target, len(enemies) - 1))
    target = enemies[idx]
    command = req.command
    ends_turn = False

    if command == "attack":
        _spend_ap(player)
        adv = compute_tactical_advantage(player, target, combat)
        result = resolve_attack(player, target, advantage=adv)
        log.append(result["description"])
        if result["hit"]:
            target.take_damage(result["damage"])
            if target.is_dead:
                log.append(f"{target.name} est elimine!")
    elif command == "aim":
        _spend_ap(player)
        player.is_aiming = True
        log.append(f"{player.name} vise soigneusement (avantage a la prochaine attaque).")
    elif command == "cover":
        _spend_ap(player)
        player.cover = CoverType.HEAVY if player.cover != CoverType.HEAVY else CoverType.LIGHT
        log.append(f"{player.name} se met a couvert ({player.cover.value}).")
    elif command == "ability":
        result = use_combat_ability(player, req.ability_id or "", target, combat)
        log.extend(result["log"])
        if not result["success"]:
            # Action refusee: ne consomme pas le tour.
            session.save()
            return {"log": log, "combat": _combat_state(combat), "state": session.full_state(), "ended": False, "victory": False}
        if target.is_dead:
            log.append(f"{target.name} est elimine!")
    elif command == "defend":
        player.is_defending = True
        player.add_condition("en_garde", 1)
        log.append(f"{player.name} se met en position defensive.")
        ends_turn = True
    elif command == "flee":
        flee_result = resolve_flee(player, enemies)
        log.append(flee_result["description"])
        if flee_result["success"]:
            combat.is_active = False
            _, xp_msgs = award_xp(session.progression, "fuite_reussie")
            log.extend(xp_msgs)
            session.save()
            return {"log": log, "combat": _combat_state(combat), "state": session.full_state(), "ended": True, "victory": False, "fled": True}
        ends_turn = True
    else:
        raise HTTPException(status_code=400, detail=f"Action inconnue: {command}")

    # Verifie une victoire immediate.
    is_over, reason = combat.is_combat_over()
    if not is_over and (ends_turn or player.action_points <= 0):
        # Fin du tour joueur -> conditions du joueur puis allies puis ennemis.
        log.extend(player.tick_conditions())
        _run_ally_turn(combat, log)
        _run_enemy_turn(combat, log)
        combat.next_turn()
        is_over, reason = combat.is_combat_over()

    victory = reason == "victoire"
    if is_over:
        combat.is_active = False
        if victory:
            threat = getattr(combat.enemies[0], "threat_id", "standard")
            reward = {"sbire": "victoire_facile", "standard": "victoire_difficile",
                      "elite": "victoire_heroique", "boss": "victoire_heroique"}.get(threat, "victoire_difficile")
            _, xp_msgs = award_xp(session.progression, reward)
            log.extend(xp_msgs)

    session.save()
    return {
        "log": log,
        "combat": _combat_state(combat),
        "state": session.full_state(),
        "ended": is_over,
        "victory": victory,
        "player_ap": player.action_points,
    }


def _negotiation_modifier(build: dict, approach: NegotiationApproach) -> int:
    """Calcule le bonus de negociation selon l'approche et le personnage.

    Chaque registre s'appuie sur un attribut du personnage (enrichi par les
    competences sociales via effective_attributes) :
      - persuasion   : solidarite + competence 'negociation'
      - intimidation : sang_froid + competence 'intimidation'
      - marchandage  : ingeniosite + competence 'commandement'
    """
    attrs = build.get("effective_attributes", {})
    if approach == NegotiationApproach.INTIMIDATION:
        base = attrs.get("sang_froid", 3) + attrs.get("intimidation", 0)
    elif approach == NegotiationApproach.MARCHANDAGE:
        base = attrs.get("ingeniosite", 3) + attrs.get("commandement", 0)
    else:  # PERSUASION
        base = attrs.get("solidarite", 3) + attrs.get("negociation", 0)
    # On centre le modificateur pour que 2d6 (moy. 7) reste pertinent.
    return base - 3


@app.post("/api/combat/negotiate")
def combat_negotiate(req: NegotiateRequest, user_id: str = Depends(current_user_id)):
    """Tente de negocier avec l'ennemi pour eviter ou inflechir le combat."""
    session = get_session(user_id)
    combat = session.combat
    if not combat or not combat.is_active:
        raise HTTPException(status_code=400, detail="Aucun combat actif")

    approach = approach_from_str(req.approach) or NegotiationApproach.PERSUASION
    living = combat.get_living_enemies()
    if not living:
        raise HTTPException(status_code=400, detail="Aucun ennemi a qui parler")
    idx = max(0, min(req.target, len(living) - 1))
    spokesperson = living[idx]
    faction_id = getattr(spokesperson, "faction_id", "tyranide")
    threat_id = getattr(spokesperson, "threat_id", "standard")

    build = _character_build(session)
    modifier = _negotiation_modifier(build, approach)
    result = attempt_negotiation(approach, modifier, threat_id, faction_id)

    log: list[str] = [f"[Negociation - {approach.value}] {result.message}"]

    if result.outcome == "impossible":
        return {
            "log": log, "combat": _combat_state(combat), "state": session.full_state(),
            "outcome": result.outcome, "ended": False,
        }

    if result.outcome == "success":
        if result.can_recruit:
            # Rallie le porte-parole comme allie (lien avec la gestion d'equipe).
            combat.enemies.remove(spokesperson)
            spokesperson.name = f"{spokesperson.name} (rallie)"
            spokesperson.is_fleeing = False
            combat.allies.append(spokesperson)
            log.append(f"{spokesperson.name} rejoint votre groupe!")
        # Les autres ennemis se retirent.
        for enemy in combat.get_living_enemies():
            enemy.is_fleeing = True
        combat.is_active = False
        _, xp_msgs = award_xp(session.progression, "fuite_reussie")
        log.extend(xp_msgs)
        session.save()
        return {
            "log": log, "combat": _combat_state(combat), "state": session.full_state(),
            "outcome": result.outcome, "ended": True, "victory": True, "negotiated": True,
        }

    # waver / fail : la tentative consomme le tour, l'ennemi riposte.
    if result.condition:
        for enemy in combat.get_living_enemies():
            enemy.add_condition(result.condition, result.condition_turns)
    log.extend(session.combat.player.tick_conditions())
    _run_ally_turn(combat, log)
    _run_enemy_turn(combat, log)
    combat.next_turn()
    is_over, reason = combat.is_combat_over()
    if is_over:
        combat.is_active = False
    session.save()
    return {
        "log": log, "combat": _combat_state(combat), "state": session.full_state(),
        "outcome": result.outcome, "ended": is_over, "victory": reason == "victoire",
    }


@app.get("/api/team")
def get_team(user_id: str = Depends(current_user_id)):
    """Retourne l'equipe et les compagnons recrutables."""
    session = get_session(user_id)
    return {
        "members": [m.to_dict() for m in session.team.members],
        "max_size": session.team.max_size,
        "available": available_templates(session.progression.level),
    }


@app.post("/api/team/recruit")
def recruit_companion(req: RecruitRequest, user_id: str = Depends(current_user_id)):
    """Recrute un compagnon d'un archetype donne."""
    session = get_session(user_id)
    companion, msg = create_companion(req.template_id, session.progression.level)
    if not companion:
        raise HTTPException(status_code=400, detail=msg)
    ok, add_msg = session.team.add(companion)
    if not ok:
        raise HTTPException(status_code=400, detail=add_msg)
    session.save()
    return {"message": add_msg, "state": session.full_state()}


@app.post("/api/team/dismiss")
def dismiss_companion(req: RecruitRequest, user_id: str = Depends(current_user_id)):
    """Retire un compagnon de l'equipe."""
    session = get_session(user_id)
    ok, msg = session.team.remove(req.template_id)
    if not ok:
        raise HTTPException(status_code=404, detail=msg)
    session.save()
    return {"message": msg, "state": session.full_state()}


@app.post("/api/travel")
def travel(req: TravelRequest, user_id: str = Depends(current_user_id)):
    """Deplacement vers une zone."""
    session = get_session(user_id)
    success, msg, event = session.world_map.travel_to(
        req.zone_id, session.world.global_state.current_scene
    )
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    session.save()
    return {
        "message": msg,
        "event": event,
        "zone": session.world_map.get_current_zone().to_dict(),
        "accessible": [z.to_dict() for z in session.world_map.get_accessible_zones()],
        "state": session.full_state(),
    }


@app.post("/api/loot")
def loot(req: CommandRequest, user_id: str = Depends(current_user_id)):
    """Genere du butin et l'ajoute a l'inventaire."""
    session = get_session(user_id)
    level = req.args[0] if req.args else "standard"
    if level.isdigit():
        level = {"1": "sbire", "2": "standard", "3": "standard", "4": "elite", "5": "boss"}.get(level, "standard")
    items = generate_loot(level)
    for item in items:
        session.inventory.add_item(item)
    session.save()
    return {
        "items": [{"name": i.name, "rarity": i.rarity.value, "type": i.item_type.value} for i in items],
        "inventory": session.inventory.to_dict(),
        "state": session.full_state(),
    }


@app.post("/api/inventory/use")
def use_consumable(req: ConsumableRequest, user_id: str = Depends(current_user_id)):
    """Utilise un consommable de l'inventaire."""
    session = get_session(user_id)
    item = session.inventory.get_item(req.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Consommable introuvable")
    if item.item_type.value != "consommable":
        raise HTTPException(status_code=400, detail="Cet objet n'est pas un consommable")

    removed = session.inventory.remove_item(req.item_id, 1)
    if not removed:
        raise HTTPException(status_code=400, detail="Impossible d'utiliser cet objet")

    message = _apply_consumable_effect(session, item)
    session.save()
    return {"message": message, "state": session.full_state()}


@app.post("/api/inventory/equip")
def equip_item(req: EquipRequest, user_id: str = Depends(current_user_id)):
    """Equipe un objet depuis l'inventaire vers un slot précis."""
    session = get_session(user_id)
    item = session.inventory.get_item(req.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Objet introuvable dans l'inventaire")

    slot = (req.slot or "main").lower()
    if item.item_type.value in ("arme_melee", "arme_distance"):
        if slot not in ("main", "secondary"):
            raise HTTPException(status_code=400, detail="Slot d'arme invalide")
        old = session.inventory.equip_weapon(item, slot=slot)
        message = f"{item.name} equipe en {slot}."
        if old:
            message += f" {old.name} range dans le sac."
    elif item.item_type.value == "armure":
        old = session.inventory.equip_armor(item)
        message = f"{item.name} equipe."
        if old:
            message += f" {old.name} range dans le sac."
    else:
        raise HTTPException(status_code=400, detail="Cet objet ne peut pas etre equipe")

    session.save()
    return {"message": message, "state": session.full_state()}


@app.post("/api/inventory/unequip")
def unequip_item(req: UnequipRequest, user_id: str = Depends(current_user_id)):
    """Retire un objet équipe et le remet dans l'inventaire."""
    session = get_session(user_id)
    slot = req.slot

    allowed_slots = {"weapon_main", "weapon_secondary", "armor_body", "armor_head"}
    if slot not in allowed_slots:
        raise HTTPException(status_code=400, detail="Slot invalide")

    item = getattr(session.inventory, slot)
    if not item:
        raise HTTPException(status_code=400, detail="Aucun objet equipe sur ce slot")

    if not session.inventory.can_add(item):
        raise HTTPException(status_code=400, detail="Inventaire trop charge pour desequiper")

    setattr(session.inventory, slot, None)
    session.inventory.add_item(item)
    session.save()
    return {"message": f"{item.name} retire et range dans le sac.", "state": session.full_state()}


@app.post("/api/attributes/allocate")
def allocate_attribute(req: AttributeAllocationRequest, user_id: str = Depends(current_user_id)):
    """Alloue des points d'attribut gagnés au niveau."""
    session = get_session(user_id)
    points = max(1, int(req.points or 1))
    if session.progression.attribute_points_available < points:
        raise HTTPException(status_code=400, detail="Pas assez de points d'attribut disponibles")

    attr = (req.attribute or "").strip().lower()
    if attr not in session.character.attributes:
        raise HTTPException(status_code=400, detail="Attribut inconnu")

    session.character.attributes[attr] = int(session.character.attributes.get(attr, 0)) + points
    session.progression.attribute_points_available -= points
    session.save()
    return {
        "message": f"{attr} augmente de +{points}.",
        "remaining": session.progression.attribute_points_available,
        "state": session.full_state(),
    }


@app.get("/api/character/build")
def character_build(user_id: str = Depends(current_user_id)):
    """Retourne le build dynamique: skills/talents/dons/stats effectives."""
    session = get_session(user_id)
    return _character_build(session)


@app.post("/api/learn")
def learn_skill(req: CommandRequest, user_id: str = Depends(current_user_id)):
    """Apprend une competence."""
    session = get_session(user_id)
    if not req.args:
        avail = get_available_skills(session.progression)
        return {"available": [{"id": s.id, "name": s.name, "cost": s.xp_cost} for s in avail]}
    skill_id = req.args[0]
    if skill_id not in SKILL_TREE:
        raise HTTPException(status_code=404, detail="Competence inconnue")
    success, msg = session.progression.unlock_with_skill_point(SKILL_TREE[skill_id])
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    session.save()
    return {"message": msg, "progression": session._progression_payload(), "state": session.full_state()}


@app.post("/api/save")
def save(user_id: str = Depends(current_user_id)):
    """Sauvegarde manuelle."""
    get_session(user_id).save()
    return {"message": "Sauvegarde effectuee"}


@app.post("/api/reset")
def reset(user_id: str = Depends(current_user_id)):
    """Reinitialise la session (nouvelle partie)."""
    global _session
    safe_user = normalize_user_id(user_id)
    if safe_user == "default":
        _session = None
    else:
        _sessions.pop(safe_user, None)
    return {"message": "Session reinitia lisee"}
