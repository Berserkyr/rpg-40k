"""Tactical combat system for the 40K RPG."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Tuple

from random import randint

from .dice import roll_2d6, DiceResult
from .entities import Entity, EntityStats, ThreatLevel


# ---------------------------------------------------------------------------
# Conditions (bonus / malus temporaires)
# ---------------------------------------------------------------------------

# Chaque condition applique des modificateurs tant qu'il reste des tours.
#   attack   : modificateur au jet d'attaque du porteur
#   defense  : modificateur a la defense du porteur
#   incoming : degats supplementaires subis par le porteur quand il est touche
#   dot      : degats infliges au porteur en debut de tour (poison/saignement)
#   skip     : le porteur perd son tour (etourdi)
CONDITION_DEFS: Dict[str, Dict] = {
    "saignement": {"label": "Saignement", "dot": 2, "icon": "🩸"},
    "etourdi": {"label": "Étourdi", "skip": True, "icon": "💫"},
    "supprime": {"label": "Supprimé", "attack": -3, "icon": "🔻"},
    "marque": {"label": "Marqué", "incoming": 2, "icon": "🎯"},
    "aveugle": {"label": "Aveuglé", "attack": -2, "icon": "🌫"},
    "inspire": {"label": "Inspiré", "attack": 2, "icon": "🔥"},
    "en_garde": {"label": "En garde", "defense": 2, "icon": "🛡"},
    "enrage": {"label": "Enragé", "attack": 2, "defense": -1, "icon": "😤"},
}


def roll_with_advantage(level: int) -> DiceResult:
    """Lance 2d6 avec avantage/desavantage tactique.

    level > 0 : avantage  -> lance des des supplementaires, garde les 2 meilleurs.
    level < 0 : desavantage -> lance des des supplementaires, garde les 2 pires.
    level == 0: jet 2d6 normal.
    L'ampleur est plafonnee a 2 des supplementaires pour rester lisible.
    """
    extra = min(2, abs(level))
    if extra == 0:
        return roll_2d6()
    dice = sorted(randint(1, 6) for _ in range(2 + extra))
    kept = dice[-2:] if level > 0 else dice[:2]
    return DiceResult(total=kept[0] + kept[1], values=(kept[0], kept[1]))


class CombatRange(Enum):
    MELEE = "melee"           # Corps a corps
    SHORT = "courte"          # 0-10m, pistolets
    MEDIUM = "moyenne"        # 10-30m, carabines
    LONG = "longue"           # 30m+, fusils


class CoverType(Enum):
    NONE = "aucune"           # Pas de couverture
    LIGHT = "legere"          # +1 defense (debris, fumee)
    HEAVY = "lourde"          # +2 defense (mur, vehicule)
    TOTAL = "totale"          # +3 defense (bunker, blindage)


class ActionType(Enum):
    ATTACK = "attaquer"
    DEFEND = "defendre"
    MOVE = "deplacer"
    USE_ABILITY = "capacite"
    USE_ITEM = "objet"
    FLEE = "fuir"
    AIM = "viser"
    RELOAD = "recharger"
    OVERWATCH = "surveillance"


@dataclass
class CombatAction:
    action_type: ActionType
    target: Optional[str] = None
    details: str = ""
    
    def describe(self) -> str:
        if self.target:
            return f"{self.action_type.value} -> {self.target}"
        return self.action_type.value


@dataclass
class Combatant:
    """A participant in combat (player or NPC/creature)."""
    
    name: str
    is_player: bool
    
    # Stats
    combat: int
    defense: int
    speed: int
    special: int
    
    # Combat state
    health: int = 10
    max_health: int = 10
    action_points: int = 2
    max_action_points: int = 2
    
    # Position & status
    range_to_player: CombatRange = CombatRange.MEDIUM
    cover: CoverType = CoverType.NONE
    is_aiming: bool = False
    is_defending: bool = False
    is_overwatching: bool = False
    is_fleeing: bool = False
    is_dead: bool = False
    
    # Abilities & conditions
    abilities: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)  # stunned, bleeding, etc.
    # Conditions temporisees: nom -> nombre de tours restants
    status_effects: Dict[str, int] = field(default_factory=dict)
    # Compteur d'utilisation des capacites (pour les "une fois par combat")
    ability_uses: Dict[str, int] = field(default_factory=dict)
    
    @classmethod
    def from_entity(cls, entity: Entity) -> "Combatant":
        """Create a combatant from an Entity."""
        # Health based on threat level
        health_map = {
            ThreatLevel.MINION: 4,
            ThreatLevel.STANDARD: 8,
            ThreatLevel.ELITE: 14,
            ThreatLevel.BOSS: 25,
        }
        hp = health_map.get(entity.threat_level, 8)
        
        return cls(
            name=entity.name,
            is_player=False,
            combat=entity.stats.combat,
            defense=entity.stats.defense,
            speed=entity.stats.speed,
            special=entity.stats.special,
            health=hp,
            max_health=hp,
            abilities=list(entity.abilities),
        )
    
    @classmethod
    def from_player_state(cls, state) -> "Combatant":
        """Create a combatant from CharacterState."""
        # Map player attributes to combat stats
        combat = state.attributes.get("robustesse", 2) + state.attributes.get("discretion", 2)
        defense = state.attributes.get("sang_froid", 3)
        speed = state.attributes.get("ingeniosite", 3)
        special = state.attributes.get("foi", 2)
        
        # Health based on wounds track
        health_map = {
            "Indemne": 10,
            "Erafle": 7,
            "Fracture": 4,
            "Condamne": 1,
        }
        hp = health_map.get(state.tracks.get("blessures", "Indemne"), 10)
        
        return cls(
            name=state.name,
            is_player=True,
            combat=combat,
            defense=defense,
            speed=speed,
            special=special,
            health=hp,
            max_health=10,
        )
    
    def effective_defense(self) -> int:
        """Calculate defense including cover and stance."""
        bonus = 0
        if self.cover == CoverType.LIGHT:
            bonus += 1
        elif self.cover == CoverType.HEAVY:
            bonus += 2
        elif self.cover == CoverType.TOTAL:
            bonus += 3
        if self.is_defending:
            bonus += 2
        return self.defense + bonus + self.condition_defense_mod()

    def effective_attack(self) -> int:
        """Calculate attack including aim bonus."""
        bonus = 0
        if self.is_aiming:
            bonus += 2
            self.is_aiming = False  # Consume aim
        return self.combat + bonus + self.condition_attack_mod()

    # --- Conditions (bonus / malus temporaires) -----------------------------

    def add_condition(self, name: str, turns: int = 2) -> None:
        """Applique (ou prolonge) une condition pour un nombre de tours."""
        if name not in CONDITION_DEFS:
            return
        self.status_effects[name] = max(self.status_effects.get(name, 0), turns)

    def has_condition(self, name: str) -> bool:
        return self.status_effects.get(name, 0) > 0

    def condition_attack_mod(self) -> int:
        return sum(
            CONDITION_DEFS[name].get("attack", 0)
            for name in self.status_effects
            if self.status_effects[name] > 0
        )

    def condition_defense_mod(self) -> int:
        return sum(
            CONDITION_DEFS[name].get("defense", 0)
            for name in self.status_effects
            if self.status_effects[name] > 0
        )

    def incoming_damage_mod(self) -> int:
        return sum(
            CONDITION_DEFS[name].get("incoming", 0)
            for name in self.status_effects
            if self.status_effects[name] > 0
        )

    def is_stunned(self) -> bool:
        return any(
            CONDITION_DEFS[name].get("skip")
            for name in self.status_effects
            if self.status_effects[name] > 0
        )

    def tick_conditions(self) -> List[str]:
        """Applique les degats sur la duree et decremente les conditions.

        Retourne les messages a journaliser (saignements, expirations).
        """
        messages: List[str] = []
        remaining: Dict[str, int] = {}
        for name, turns in self.status_effects.items():
            if turns <= 0:
                continue
            dot = CONDITION_DEFS[name].get("dot", 0)
            if dot:
                self.take_damage(dot)
                label = CONDITION_DEFS[name].get("label", name)
                messages.append(f"{self.name} subit {dot} degats ({label}).")
            if turns - 1 > 0:
                remaining[name] = turns - 1
        self.status_effects = remaining
        return messages

    def active_conditions(self) -> List[dict]:
        """Liste serialisable des conditions actives (pour l'UI)."""
        out = []
        for name, turns in self.status_effects.items():
            if turns <= 0:
                continue
            spec = CONDITION_DEFS.get(name, {})
            out.append({
                "id": name,
                "label": spec.get("label", name),
                "icon": spec.get("icon", "•"),
                "turns": turns,
            })
        return out
    
    def take_damage(self, amount: int) -> Tuple[int, bool]:
        """Apply damage, return (actual_damage, is_dead)."""
        actual = max(0, amount)
        self.health = max(0, self.health - actual)
        self.is_dead = self.health <= 0
        return actual, self.is_dead
    
    def reset_turn(self) -> None:
        """Reset per-turn states."""
        self.action_points = self.max_action_points
        self.is_defending = False
        self.is_overwatching = False
        self.is_fleeing = False


@dataclass
class CombatState:
    """Tracks the state of an ongoing combat encounter."""
    
    player: Combatant
    enemies: List[Combatant]
    allies: List[Combatant] = field(default_factory=list)
    
    turn_number: int = 1
    current_phase: str = "player"  # "player", "enemy", "ally"
    is_active: bool = True
    combat_log: List[str] = field(default_factory=list)
    
    # Environment
    environment: str = "couloir_ruche"
    lighting: str = "faible"
    hazards: List[str] = field(default_factory=list)
    
    def add_log(self, message: str) -> None:
        self.combat_log.append(f"[Tour {self.turn_number}] {message}")
    
    def get_all_combatants(self) -> List[Combatant]:
        return [self.player] + self.enemies + self.allies
    
    def get_living_enemies(self) -> List[Combatant]:
        return [e for e in self.enemies if not e.is_dead]
    
    def is_combat_over(self) -> Tuple[bool, str]:
        """Check if combat is over, return (is_over, reason)."""
        if self.player.is_dead:
            return True, "defaite"
        if self.player.is_fleeing:
            return True, "fuite"
        if not self.get_living_enemies():
            return True, "victoire"
        return False, ""
    
    def next_turn(self) -> None:
        """Advance to next turn."""
        self.turn_number += 1
        for c in self.get_all_combatants():
            c.reset_turn()
        self.current_phase = "player"


# ---------------------------------------------------------------------------
# Combat resolution
# ---------------------------------------------------------------------------

def calculate_initiative(combatants: List[Combatant]) -> List[Combatant]:
    """Sort combatants by initiative (speed + 2d6)."""
    initiatives = []
    for c in combatants:
        if c.is_dead:
            continue
        roll = roll_2d6()
        init_value = c.speed + roll.total
        initiatives.append((c, init_value, roll))
    
    initiatives.sort(key=lambda x: x[1], reverse=True)
    return [c for c, _, _ in initiatives]


def resolve_attack(attacker: Combatant, defender: Combatant,
                   range_penalty: int = 0, advantage: int = 0,
                   bonus_damage: int = 0) -> Dict:
    """
    Resolve an attack action.

    Args:
        attacker, defender: les combattants.
        range_penalty: malus lie a la portee.
        advantage: niveau d'avantage tactique (>0 avantage, <0 desavantage).
        bonus_damage: degats supplementaires (capacites).

    Returns dict with:
        - hit: bool
        - damage: int
        - critical: bool
        - fumble: bool
        - advantage: int
        - description: str
    """
    attack_roll = roll_with_advantage(advantage)
    attack_value = attacker.effective_attack() + attack_roll.total - range_penalty
    defense_value = defender.effective_defense() + 7  # Base difficulty

    result = {
        "hit": False,
        "damage": 0,
        "critical": False,
        "fumble": False,
        "roll": attack_roll,
        "advantage": advantage,
        "attack_total": attack_value,
        "defense_total": defense_value,
        "description": "",
    }

    # Fumble on double 1
    if attack_roll.is_double() and attack_roll.values[0] == 1:
        result["fumble"] = True
        result["description"] = f"{attacker.name} rate catastrophiquement son attaque!"
        return result

    # Critical on double 6
    if attack_roll.is_double() and attack_roll.values[0] == 6:
        result["critical"] = True
        result["hit"] = True
        base_damage = attacker.combat + 2 + bonus_damage
        result["damage"] = base_damage * 2 + defender.incoming_damage_mod()
        result["description"] = f"CRITIQUE! {attacker.name} inflige {result['damage']} degats a {defender.name}!"
        return result

    # Normal resolution
    if attack_value >= defense_value:
        result["hit"] = True
        base_damage = max(1, attacker.combat - defender.defense + random.randint(1, 4))
        base_damage += bonus_damage + defender.incoming_damage_mod()
        result["damage"] = base_damage
        tag = ""
        if advantage > 0:
            tag = " [avantage]"
        elif advantage < 0:
            tag = " [desavantage]"
        result["description"] = f"{attacker.name} touche {defender.name} pour {base_damage} degats.{tag}"
    else:
        result["description"] = f"{attacker.name} rate {defender.name}."

    return result


def resolve_flee(fleeing: Combatant, pursuers: List[Combatant]) -> Dict:
    """
    Resolve a flee attempt.
    
    Returns dict with:
        - success: bool
        - damage_taken: int (from attacks of opportunity)
        - description: str
    """
    flee_roll = roll_2d6()
    flee_value = fleeing.speed + flee_roll.total
    
    # Average pursuer speed as difficulty
    avg_speed = sum(p.speed for p in pursuers if not p.is_dead) / max(1, len(pursuers))
    difficulty = int(avg_speed) + 7
    
    result = {
        "success": flee_value >= difficulty,
        "damage_taken": 0,
        "roll": flee_roll,
        "description": "",
    }
    
    if result["success"]:
        fleeing.is_fleeing = True
        result["description"] = f"{fleeing.name} reussit a fuir le combat!"
    else:
        # Attack of opportunity from one random pursuer
        living = [p for p in pursuers if not p.is_dead]
        if living:
            attacker = random.choice(living)
            opp_attack = resolve_attack(attacker, fleeing)
            if opp_attack["hit"]:
                result["damage_taken"] = opp_attack["damage"]
                fleeing.take_damage(opp_attack["damage"])
        result["description"] = f"{fleeing.name} echoue a fuir et subit une attaque d'opportunite!"
    
    return result


# ---------------------------------------------------------------------------
# Combat abilities & tactical advantage
# ---------------------------------------------------------------------------


@dataclass
class AbilitySpec:
    """Description d'une capacite active utilisable en combat."""
    id: str
    name: str
    ap_cost: int
    target: str  # "enemy", "self" ou "ally"
    description: str
    icon: str = "✦"
    once_per_combat: bool = False


# Registre des capacites actives. Les identifiants correspondent aux
# special_ability de l'arbre de competences (progression.py) et aux traits
# d'armes, afin que debloquer une competence rende sa capacite jouable.
COMBAT_ABILITIES: Dict[str, AbilitySpec] = {
    "frappe_puissante": AbilitySpec(
        "frappe_puissante", "Frappe puissante", 2, "enemy",
        "Attaque avec avantage et +2 degats.", "💥"),
    "coup_sournois": AbilitySpec(
        "coup_sournois", "Coup sournois", 1, "enemy",
        "Attaque rapide infligeant +3 degats.", "🗡"),
    "coup_etourdissant": AbilitySpec(
        "coup_etourdissant", "Coup etourdissant", 2, "enemy",
        "Attaque qui etourdit la cible si elle touche.", "💫"),
    "tir_suppression": AbilitySpec(
        "tir_suppression", "Tir de suppression", 1, "enemy",
        "Applique Supprimé (-3 attaque) a la cible.", "🔻"),
    "marquage": AbilitySpec(
        "marquage", "Marquage", 1, "enemy",
        "Marque la cible: +2 degats subis.", "🎯"),
    "parade": AbilitySpec(
        "parade", "Parade", 1, "self",
        "Position En garde (+2 defense).", "🛡", once_per_combat=True),
    "fureur_imperiale": AbilitySpec(
        "fureur_imperiale", "Fureur imperiale", 2, "self",
        "Entre en rage (+2 attaque, avantage).", "🔥", once_per_combat=True),
    "priere": AbilitySpec(
        "priere", "Priere a l'Empereur", 1, "self",
        "Soigne 2 PV et dissipe la suppression.", "✨"),
    "cri_ralliement": AbilitySpec(
        "cri_ralliement", "Cri de ralliement", 1, "self",
        "Inspire le groupe (+2 attaque).", "📣"),
}

# Capacites toujours disponibles pour tout combattant joueur.
BASIC_ABILITIES = ["parade"]


def get_available_abilities(ability_ids: List[str]) -> List[dict]:
    """Retourne les specs serialisables des capacites connues + basiques."""
    seen = set()
    out = []
    for aid in list(ability_ids) + BASIC_ABILITIES:
        if aid in COMBAT_ABILITIES and aid not in seen:
            seen.add(aid)
            spec = COMBAT_ABILITIES[aid]
            out.append({
                "id": spec.id,
                "name": spec.name,
                "ap_cost": spec.ap_cost,
                "target": spec.target,
                "description": spec.description,
                "icon": spec.icon,
                "once_per_combat": spec.once_per_combat,
            })
    return out


def compute_tactical_advantage(attacker: Combatant, defender: Combatant,
                               combat: "CombatState") -> int:
    """Calcule le niveau d'avantage tactique net d'une attaque (borne +/-2)."""
    level = 0
    if attacker.is_aiming:
        level += 1
    if defender.cover in (CoverType.HEAVY, CoverType.TOTAL):
        level -= 1
    # Prise en tenaille: le joueur epaule par des allies vivants.
    if attacker.is_player and combat.allies and any(not a.is_dead for a in combat.allies):
        level += 1
    if attacker.has_condition("enrage") or attacker.has_condition("inspire"):
        level += 1
    if attacker.has_condition("supprime") or attacker.has_condition("aveugle"):
        level -= 1
    if defender.is_stunned():
        level += 1
    return max(-2, min(2, level))


def use_combat_ability(user: Combatant, ability_id: str,
                       target: Optional[Combatant],
                       combat: "CombatState") -> Dict:
    """Execute une capacite active. Retourne {log, hit, damage, ...}."""
    spec = COMBAT_ABILITIES.get(ability_id)
    result = {"log": [], "success": False, "hit": False, "damage": 0}

    if spec is None:
        result["log"].append("Capacite inconnue.")
        return result
    if user.action_points < spec.ap_cost:
        result["log"].append(f"Pas assez de PA pour {spec.name} ({spec.ap_cost} requis).")
        return result
    if spec.once_per_combat and user.ability_uses.get(ability_id, 0) >= 1:
        result["log"].append(f"{spec.name} deja utilisee ce combat.")
        return result

    user.action_points -= spec.ap_cost
    user.ability_uses[ability_id] = user.ability_uses.get(ability_id, 0) + 1
    result["success"] = True

    if ability_id == "frappe_puissante" and target:
        adv = compute_tactical_advantage(user, target, combat) + 1
        atk = resolve_attack(user, target, advantage=adv, bonus_damage=2)
        result["hit"], result["damage"] = atk["hit"], atk["damage"]
        result["log"].append(f"{spec.icon} {atk['description']}")
    elif ability_id == "coup_sournois" and target:
        adv = compute_tactical_advantage(user, target, combat)
        atk = resolve_attack(user, target, advantage=adv, bonus_damage=3)
        result["hit"], result["damage"] = atk["hit"], atk["damage"]
        result["log"].append(f"{spec.icon} {atk['description']}")
    elif ability_id == "coup_etourdissant" and target:
        adv = compute_tactical_advantage(user, target, combat)
        atk = resolve_attack(user, target, advantage=adv)
        result["hit"], result["damage"] = atk["hit"], atk["damage"]
        result["log"].append(f"{spec.icon} {atk['description']}")
        if atk["hit"]:
            target.add_condition("etourdi", 1)
            result["log"].append(f"{target.name} est etourdi!")
    elif ability_id == "tir_suppression" and target:
        target.add_condition("supprime", 2)
        result["log"].append(f"{spec.icon} {user.name} cloue {target.name} au sol (Supprimé).")
    elif ability_id == "marquage" and target:
        target.add_condition("marque", 3)
        result["log"].append(f"{spec.icon} {user.name} marque {target.name}.")
    elif ability_id == "parade":
        user.add_condition("en_garde", 2)
        result["log"].append(f"{spec.icon} {user.name} adopte une posture de parade.")
    elif ability_id == "fureur_imperiale":
        user.add_condition("enrage", 3)
        result["log"].append(f"{spec.icon} {user.name} entre dans une fureur sacree!")
    elif ability_id == "priere":
        healed = min(2, user.max_health - user.health)
        user.health += healed
        user.status_effects.pop("supprime", None)
        result["log"].append(f"{spec.icon} {user.name} prie: +{healed} PV, suppression dissipee.")
    elif ability_id == "cri_ralliement":
        user.add_condition("inspire", 2)
        for ally in combat.allies:
            if not ally.is_dead:
                ally.add_condition("inspire", 2)
        result["log"].append(f"{spec.icon} {user.name} galvanise le groupe!")
    else:
        user.action_points += spec.ap_cost  # rembourse
        user.ability_uses[ability_id] -= 1
        result["success"] = False
        result["log"].append(f"{spec.name}: cible invalide.")

    return result


def enemy_ai_action(enemy: Combatant, player: Combatant, 
                    combat_state: CombatState) -> CombatAction:
    """Simple AI to determine enemy action."""
    
    # If low health, might flee
    if enemy.health <= enemy.max_health * 0.2 and random.random() < 0.3:
        return CombatAction(ActionType.FLEE)
    
    # If far, move closer or aim
    if enemy.range_to_player in (CombatRange.LONG, CombatRange.MEDIUM):
        if random.random() < 0.4:
            return CombatAction(ActionType.MOVE, details="approche")
        if random.random() < 0.3:
            return CombatAction(ActionType.AIM)
    
    # Use special ability if available
    if enemy.abilities and random.random() < 0.2:
        ability = random.choice(enemy.abilities)
        return CombatAction(ActionType.USE_ABILITY, target=player.name, details=ability)
    
    # Default: attack
    return CombatAction(ActionType.ATTACK, target=player.name)


# ---------------------------------------------------------------------------
# Combat formatting
# ---------------------------------------------------------------------------

def format_combat_status(combat: CombatState) -> str:
    """Format current combat state for display."""
    lines = [
        f"=== COMBAT - Tour {combat.turn_number} ===",
        f"Environnement: {combat.environment} | Eclairage: {combat.lighting}",
        "",
        f"** {combat.player.name} (JOUEUR) **",
        f"   PV: {combat.player.health}/{combat.player.max_health} | PA: {combat.player.action_points}",
        f"   Couverture: {combat.player.cover.value}",
        "",
        "** ENNEMIS **",
    ]
    
    for i, e in enumerate(combat.enemies, 1):
        status = "MORT" if e.is_dead else f"PV:{e.health}/{e.max_health}"
        range_str = e.range_to_player.value
        cover_str = e.cover.value
        lines.append(f"   {i}. {e.name} [{status}] | Portee: {range_str} | Couvert: {cover_str}")
        if e.abilities:
            lines.append(f"      Capacites: {', '.join(e.abilities)}")
    
    if combat.allies:
        lines.append("")
        lines.append("** ALLIES **")
        for a in combat.allies:
            status = "MORT" if a.is_dead else f"PV:{a.health}/{a.max_health}"
            lines.append(f"   - {a.name} [{status}]")
    
    if combat.hazards:
        lines.append("")
        lines.append(f"Dangers: {', '.join(combat.hazards)}")
    
    return "\n".join(lines)


def format_combat_actions() -> str:
    """List available combat actions."""
    return """Actions disponibles (1 PA chacune sauf mention contraire):
  !attack <cible>   - Attaquer un ennemi
  !defend           - Position defensive (+2 def ce tour)
  !move <direction> - Se deplacer (avant/arriere/couvert)
  !aim              - Viser (+2 att prochaine attaque)
  !flee             - Tenter de fuir le combat
  !ability <nom>    - Utiliser une capacite speciale
  !item <nom>       - Utiliser un objet
  !overwatch        - Tir de reaction sur mouvement ennemi
  !combat-status    - Voir l'etat du combat"""
