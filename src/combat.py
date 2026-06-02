"""Tactical combat system for the 40K RPG."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Tuple

from .dice import roll_2d6, DiceResult
from .entities import Entity, EntityStats, ThreatLevel


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
        return self.defense + bonus
    
    def effective_attack(self) -> int:
        """Calculate attack including aim bonus."""
        bonus = 0
        if self.is_aiming:
            bonus += 2
            self.is_aiming = False  # Consume aim
        return self.combat + bonus
    
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
                   range_penalty: int = 0) -> Dict:
    """
    Resolve an attack action.
    
    Returns dict with:
        - hit: bool
        - damage: int
        - critical: bool
        - fumble: bool
        - description: str
    """
    attack_roll = roll_2d6()
    attack_value = attacker.effective_attack() + attack_roll.total - range_penalty
    defense_value = defender.effective_defense() + 7  # Base difficulty
    
    result = {
        "hit": False,
        "damage": 0,
        "critical": False,
        "fumble": False,
        "roll": attack_roll,
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
        base_damage = attacker.combat + 2
        result["damage"] = base_damage * 2
        result["description"] = f"CRITIQUE! {attacker.name} inflige {result['damage']} degats a {defender.name}!"
        return result
    
    # Normal resolution
    if attack_value >= defense_value:
        result["hit"] = True
        base_damage = max(1, attacker.combat - defender.defense + random.randint(1, 4))
        result["damage"] = base_damage
        result["description"] = f"{attacker.name} touche {defender.name} pour {base_damage} degats."
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
