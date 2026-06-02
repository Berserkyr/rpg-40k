"""
Backend FastAPI - Survivant de Ruche
Expose les systemes de jeu via REST + SSE pour la reponse en streaming du MJ.
"""
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import AsyncIterator, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

load_dotenv()

# ---------------------------------------------------------------------------
# Imports des systemes
# ---------------------------------------------------------------------------
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.state import CharacterState
from src.prompt_builder import build_system_prompt
from src.dice import format_roll, roll_2d6
from src.entities import Faction, ThreatLevel, generate_entity, generate_encounter
from src.combat import Combatant, CombatState, resolve_attack, resolve_flee
from src.inventory import (
    Inventory, generate_loot, WEAPON_TEMPLATES, ARMOR_TEMPLATES,
    create_weapon, create_armor,
)
from src.progression import (
    ProgressionState, SKILL_TREE, award_xp,
    format_skill_tree, get_available_skills, get_unlocked_skills,
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Session unique (pour l'instant une seule partie a la fois)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.parent
SAVE_DIR = BASE_DIR / "saves"
CHARACTER_FILE = BASE_DIR / "character_sheet.yaml"
PROMPT_FILE = BASE_DIR / "prompt_survivant.md"
CAMPAIGN = "campagne1"


class Session:
    """Etat de session charge en memoire."""

    def __init__(self) -> None:
        save_dir = SAVE_DIR / CAMPAIGN
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
        ]:
            with open(self.save_dir / fname, "w", encoding="utf-8") as f:
                yaml.safe_dump(obj.to_dict(), f, allow_unicode=True)

    def full_state(self) -> dict:
        """Sérialise tout l'etat visible par l'UI."""
        zone = self.world_map.get_current_zone()
        return {
            "character": self.character.to_dict(),
            "progression": self.progression.to_dict(),
            "inventory": self.inventory.to_dict(),
            "world": self.world.to_dict(),
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
    return {
        "active": combat.is_active,
        "turn": combat.turn_number,
        "player": {
            "name": combat.player.name,
            "health": combat.player.health,
            "max_health": combat.player.max_health,
        },
        "enemies": [
            {
                "name": e.name,
                "health": e.health,
                "max_health": e.max_health,
                "is_dead": e.is_dead,
            }
            for e in combat.enemies
        ],
    }


# Session singleton
_session: Optional[Session] = None


def get_session() -> Session:
    global _session
    if _session is None:
        _session = Session()
    return _session


# ---------------------------------------------------------------------------
# OpenAI client
# ---------------------------------------------------------------------------
def get_openai_client() -> AsyncOpenAI:
    key = os.getenv("OPENAI_API_KEY", "")
    if not key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY manquant")
    return AsyncOpenAI(api_key=key)


def _offline_gm_text(session: Session, user_message: str, opening: bool = False) -> str:
    """Fallback local: permet de jouer même sans OPENAI_API_KEY."""
    zone = session.world_map.get_current_zone()
    zone_name = zone.name if zone else "zone inconnue"
    accessible = session.world_map.get_accessible_zones()
    exits = ", ".join(z.name for z in accessible[:3]) or "aucune sortie claire"

    if opening:
        return (
            "[MODE MJ LOCAL — aucune clé OPENAI_API_KEY détectée]\n\n"
            f"Karimus reprend conscience dans {zone_name}. Les alarmes de la ruche hurlent, "
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
                + _offline_gm_text(session, user_message, opening=opening)
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


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/state")
def get_state():
    """Retourne l'etat complet de la session."""
    return get_session().full_state()


@app.post("/api/start")
async def start_game():
    """Demarre une nouvelle scene d'ouverture (SSE streaming)."""
    session = get_session()

    opening_prompt = "Lance la scene d'ouverture. Karimus se reveille dans le chaos de l'invasion tyranide."

    if session.world.global_state.total_scenes == 0:
        session.messages.append({
            "role": "user",
            "content": opening_prompt,
        })

    return EventSourceResponse(_gm_stream(session, opening_prompt, opening=True))


@app.post("/api/chat")
async def chat(req: ChatRequest):
    """Envoie un message au MJ et streame la reponse."""
    session = get_session()
    session.messages.append({"role": "user", "content": req.message})
    return EventSourceResponse(_gm_stream(session, req.message))


@app.post("/api/roll")
def roll_dice():
    """Lance 2d6 et retourne le resultat."""
    result = roll_2d6()
    return {"formatted": format_roll(result), "total": result.total, "values": result.values}


@app.post("/api/spawn")
def spawn_entity(req: SpawnRequest):
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
def start_combat(req: SpawnRequest):
    """Demarre un combat."""
    session = get_session()
    faction_map = {"tyranide": Faction.TYRANID, "culte": Faction.GENESTEALER_CULT}
    level_map = {"sbire": ThreatLevel.MINION, "standard": ThreatLevel.STANDARD,
                 "elite": ThreatLevel.ELITE, "boss": ThreatLevel.BOSS}
    faction = faction_map.get(req.faction.lower(), Faction.TYRANID)
    level = level_map.get(req.level.lower(), ThreatLevel.STANDARD)
    entity = generate_entity(faction, level)
    enemy = Combatant.from_entity(entity)
    player = Combatant.from_player_state(session.character)
    session.combat = CombatState(player=player, enemies=[enemy])
    session.save()
    return {"message": f"Combat contre {enemy.name}!", "combat": _combat_state(session.combat), "state": session.full_state()}


@app.post("/api/combat/action")
def combat_action(req: CommandRequest):
    """Execute une action de combat (attack/defend/flee)."""
    import random
    session = get_session()
    if not session.combat or not session.combat.is_active:
        raise HTTPException(status_code=400, detail="Pas de combat actif")

    action = req.command
    combat = session.combat
    player = combat.player
    enemies = combat.get_living_enemies()
    log = []

    if not enemies:
        combat.is_active = False
        session.save()
        return {"log": ["Plus d'ennemis!"], "combat": _combat_state(combat), "state": session.full_state(), "ended": True, "victory": True}

    target = enemies[0]

    if action == "attack":
        result = resolve_attack(player, target)
        log.append(result["description"])
        if result["hit"]:
            target.health -= result["damage"]
            if target.health <= 0:
                target.is_dead = True
                log.append(f"{target.name} est elimine!")
    elif action == "defend":
        player.is_defending = True
        log.append(f"{player.name} se met en position defensive.")
    elif action == "flee":
        flee_result = resolve_flee(player, enemies)
        log.append(flee_result["description"])
        if flee_result["success"]:
            combat.is_active = False
            session.save()
            return {"log": log, "combat": _combat_state(combat), "state": session.full_state(), "ended": True, "victory": False, "fled": True}

    # Tour ennemi
    for enemy in combat.get_living_enemies():
        enemy_action = random.choice(["attack", "attack", "defend"])
        if enemy_action == "attack":
            result = resolve_attack(enemy, player)
            log.append(result["description"])
            if result["hit"]:
                player.health -= result["damage"]
                if player.health <= 0:
                    player.is_dead = True

    # Reset defense
    player.is_defending = False
    for e in enemies:
        e.is_defending = False

    combat.next_turn()
    is_over, reason = combat.is_combat_over()
    victory = reason == "victoire"
    if is_over:
        combat.is_active = False
        if victory:
            _, xp_msgs = award_xp(session.progression, "victoire_difficile")
            log.extend(xp_msgs)
    session.save()

    return {"log": log, "combat": _combat_state(combat), "state": session.full_state(), "ended": is_over, "victory": victory}


@app.post("/api/travel")
def travel(req: TravelRequest):
    """Deplacement vers une zone."""
    session = get_session()
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
def loot(req: CommandRequest):
    """Genere du butin et l'ajoute a l'inventaire."""
    session = get_session()
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


@app.post("/api/learn")
def learn_skill(req: CommandRequest):
    """Apprend une competence."""
    session = get_session()
    if not req.args:
        avail = get_available_skills(session.progression)
        return {"available": [{"id": s.id, "name": s.name, "cost": s.xp_cost} for s in avail]}
    skill_id = req.args[0]
    if skill_id not in SKILL_TREE:
        raise HTTPException(status_code=404, detail="Competence inconnue")
    success, msg = session.progression.unlock_skill(SKILL_TREE[skill_id])
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    session.save()
    return {"message": msg, "progression": session.progression.to_dict(), "state": session.full_state()}


@app.post("/api/save")
def save():
    """Sauvegarde manuelle."""
    get_session().save()
    return {"message": "Sauvegarde effectuee"}


@app.post("/api/reset")
def reset():
    """Reinitialise la session (nouvelle partie)."""
    global _session
    _session = None
    return {"message": "Session reinitia lisee"}
