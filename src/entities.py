"""Procedural generation of NPCs and creatures for the 40K RPG."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class Faction(Enum):
    TYRANID = "tyranide"
    GENESTEALER_CULT = "culte_genestealer"
    IMPERIAL_GUARD = "garde_imperiale"
    ARBITES = "arbites"
    CIVILIAN = "civil"
    MECHANICUS = "mechanicus"
    CHAOS = "chaos"
    ECCLESIARCHY = "ecclesiarchie"


class ThreatLevel(Enum):
    MINION = "sbire"        # Facile, en groupe
    STANDARD = "standard"   # Adversaire moyen
    ELITE = "elite"         # Dangereux seul
    BOSS = "boss"           # Menace majeure


@dataclass
class EntityStats:
    combat: int      # Capacite offensive
    defense: int     # Resistance aux degats
    speed: int       # Initiative / mobilite
    special: int     # Capacites speciales (psy, acide, etc.)

    def total_threat(self) -> int:
        return self.combat + self.defense + self.speed + self.special


@dataclass
class Entity:
    name: str
    faction: Faction
    threat_level: ThreatLevel
    stats: EntityStats
    abilities: List[str] = field(default_factory=list)
    weakness: Optional[str] = None
    description: str = ""

    def as_markdown(self) -> str:
        abilities_str = ", ".join(self.abilities) if self.abilities else "Aucune"
        weakness_str = self.weakness or "Inconnue"
        return (
            f"**{self.name}** ({self.faction.value} - {self.threat_level.value})\n"
            f"- Combat: {self.stats.combat} | Defense: {self.stats.defense} | "
            f"Vitesse: {self.stats.speed} | Special: {self.stats.special}\n"
            f"- Capacites: {abilities_str}\n"
            f"- Faiblesse: {weakness_str}\n"
            f"- {self.description}"
        )

    def to_prompt_block(self) -> str:
        """Compact format for MJ context injection."""
        abilities_str = "/".join(self.abilities) if self.abilities else "-"
        return (
            f"[{self.name}|{self.faction.value}|{self.threat_level.value}|"
            f"C{self.stats.combat}/D{self.stats.defense}/V{self.stats.speed}/S{self.stats.special}|"
            f"cap:{abilities_str}|faib:{self.weakness or '-'}]"
        )


# ---------------------------------------------------------------------------
# Templates par faction
# ---------------------------------------------------------------------------

TYRANID_TEMPLATES: Dict[ThreatLevel, List[dict]] = {
    ThreatLevel.MINION: [
        {"name": "Hormagaunt", "stats": (2, 1, 3, 0), "abilities": ["Essaim"], "weakness": "Feu", "desc": "Creature rapide aux griffes acerees."},
        {"name": "Termagant", "stats": (2, 1, 2, 1), "abilities": ["Tir_bioplasma"], "weakness": "Isolation synaptique", "desc": "Bioform arme a distance."},
        {"name": "Ripper", "stats": (1, 0, 2, 0), "abilities": ["Nuee"], "weakness": "Ecrasement", "desc": "Minuscules predateurs en masse."},
    ],
    ThreatLevel.STANDARD: [
        {"name": "Guerrier Tyranide", "stats": (4, 3, 3, 2), "abilities": ["Synapse", "Armes_bio"], "weakness": "Tir concentre", "desc": "Noeud synaptique de la flotte-ruche."},
        {"name": "Genestealer", "stats": (5, 2, 4, 1), "abilities": ["Infiltration", "Griffes_rendantes"], "weakness": "Lumiere intense", "desc": "Chasseur furtif et mortel."},
    ],
    ThreatLevel.ELITE: [
        {"name": "Lictor", "stats": (5, 3, 5, 3), "abilities": ["Camouflage", "Embuscade", "Feromones_terreur"], "weakness": "Detection thermique", "desc": "Assassin invisible de la flotte."},
        {"name": "Ravener", "stats": (5, 3, 5, 2), "abilities": ["Fouisseur", "Attaque_surprise"], "weakness": "Sol metallique", "desc": "Surgit du sol sans prevenir."},
    ],
    ThreatLevel.BOSS: [
        {"name": "Carnifex", "stats": (7, 6, 2, 3), "abilities": ["Charge", "Carapace_blindee", "Ecrasement"], "weakness": "Armes lourdes", "desc": "Tank vivant de la flotte-ruche."},
        {"name": "Tyran des Ruches", "stats": (6, 5, 3, 6), "abilities": ["Synapse_majeure", "Pouvoirs_psyker", "Commandement"], "weakness": "Isolation psionique", "desc": "Intelligence supreme de l'essaim local."},
    ],
}

GENESTEALER_CULT_TEMPLATES: Dict[ThreatLevel, List[dict]] = {
    ThreatLevel.MINION: [
        {"name": "Neophyte", "stats": (2, 1, 2, 0), "abilities": ["Arme_improvisee"], "weakness": "Moral faible", "desc": "Cultiste de bas rang."},
        {"name": "Brood Brother", "stats": (2, 2, 2, 0), "abilities": ["Formation_militaire"], "weakness": "Hierarchie", "desc": "Garde corrompu."},
    ],
    ThreatLevel.STANDARD: [
        {"name": "Acolyte Hybride", "stats": (4, 2, 3, 1), "abilities": ["Griffes", "Fanatisme"], "weakness": "Lumiere sacree", "desc": "Hybride de seconde generation."},
        {"name": "Metamorphe", "stats": (4, 2, 4, 2), "abilities": ["Mutation", "Regeneration"], "weakness": "Feu purificateur", "desc": "Forme instable et mortelle."},
    ],
    ThreatLevel.ELITE: [
        {"name": "Magus", "stats": (2, 2, 2, 5), "abilities": ["Hypnose", "Pouvoirs_psyker", "Domination"], "weakness": "Volonte forte", "desc": "Psyker du culte."},
        {"name": "Primus", "stats": (5, 3, 4, 2), "abilities": ["Tactique", "Embuscade", "Commandement"], "weakness": "Combat singulier", "desc": "Chef militaire du culte."},
    ],
    ThreatLevel.BOSS: [
        {"name": "Patriarche", "stats": (6, 4, 4, 6), "abilities": ["Controle_mental", "Griffes_adamantines", "Aura_terreur"], "weakness": "Armes benedites", "desc": "Genestealer ancestral, pere du culte."},
    ],
}

IMPERIAL_GUARD_TEMPLATES: Dict[ThreatLevel, List[dict]] = {
    ThreatLevel.MINION: [
        {"name": "Troufion", "stats": (2, 1, 2, 0), "abilities": ["Lasgun"], "weakness": "Panique", "desc": "Soldat de base."},
    ],
    ThreatLevel.STANDARD: [
        {"name": "Sergent", "stats": (3, 2, 2, 1), "abilities": ["Commandement", "Pistolet_bolter"], "weakness": "Perte d'officier", "desc": "Sous-officier experimente."},
        {"name": "Stormtrooper", "stats": (4, 3, 3, 1), "abilities": ["Hellgun", "Tactique_elite"], "weakness": "Surnombre", "desc": "Soldat d'elite."},
    ],
    ThreatLevel.ELITE: [
        {"name": "Commissaire", "stats": (4, 3, 3, 3), "abilities": ["Execution", "Moral_inebranlab"], "weakness": "Tir de precision", "desc": "Officier politique redoute."},
        {"name": "Ogryn", "stats": (5, 5, 1, 0), "abilities": ["Force_brute", "Ripper_gun"], "weakness": "Intelligence limitee", "desc": "Abhuman massif et loyal."},
    ],
    ThreatLevel.BOSS: [
        {"name": "Officier Senior", "stats": (4, 3, 3, 4), "abilities": ["Commandement_supreme", "Appui_orbital"], "weakness": "Decapitation", "desc": "Haut grade avec ressources."},
    ],
}

CIVILIAN_TEMPLATES: Dict[ThreatLevel, List[dict]] = {
    ThreatLevel.MINION: [
        {"name": "Refugie", "stats": (1, 0, 2, 0), "abilities": [], "weakness": "Terreur", "desc": "Civil en fuite."},
        {"name": "Ouvrier", "stats": (1, 1, 1, 0), "abilities": ["Outil_improvise"], "weakness": "Panique", "desc": "Travailleur de la ruche."},
    ],
    ThreatLevel.STANDARD: [
        {"name": "Ganger", "stats": (3, 2, 3, 0), "abilities": ["Arme_illegale", "Connaissance_locale"], "weakness": "Autorite", "desc": "Membre de gang."},
        {"name": "Marchand", "stats": (1, 1, 2, 2), "abilities": ["Negociation", "Contacts"], "weakness": "Violence", "desc": "Commercant pragmatique."},
    ],
    ThreatLevel.ELITE: [
        {"name": "Noble mineur", "stats": (2, 2, 2, 3), "abilities": ["Influence", "Gardes_du_corps"], "weakness": "Scandale", "desc": "Aristocrate local."},
        {"name": "Chirurgien clandestin", "stats": (1, 1, 2, 4), "abilities": ["Soins", "Drogues"], "weakness": "Arbites", "desc": "Medecin non officiel."},
    ],
    ThreatLevel.BOSS: [
        {"name": "Seigneur de gang", "stats": (4, 3, 3, 3), "abilities": ["Reseau_criminel", "Combattant_veterant"], "weakness": "Trahison interne", "desc": "Chef du sous-monde local."},
    ],
}

ALL_TEMPLATES: Dict[Faction, Dict[ThreatLevel, List[dict]]] = {
    Faction.TYRANID: TYRANID_TEMPLATES,
    Faction.GENESTEALER_CULT: GENESTEALER_CULT_TEMPLATES,
    Faction.IMPERIAL_GUARD: IMPERIAL_GUARD_TEMPLATES,
    Faction.CIVILIAN: CIVILIAN_TEMPLATES,
}


# ---------------------------------------------------------------------------
# Generation procedurale
# ---------------------------------------------------------------------------

def _apply_variance(base: int, variance: int = 1) -> int:
    """Add random variance to a stat."""
    return max(0, base + random.randint(-variance, variance))


def generate_entity(
    faction: Faction,
    threat_level: ThreatLevel,
    context: Optional[str] = None,
    name_override: Optional[str] = None,
) -> Entity:
    """
    Generate an entity from templates with procedural variance.
    
    Args:
        faction: The faction of the entity.
        threat_level: How dangerous the entity should be.
        context: Optional narrative context to influence description.
        name_override: Optional custom name for the entity.
    
    Returns:
        A fully generated Entity with randomized stats.
    """
    templates = ALL_TEMPLATES.get(faction, CIVILIAN_TEMPLATES)
    level_templates = templates.get(threat_level, templates[ThreatLevel.MINION])
    
    template = random.choice(level_templates)
    base_stats = template["stats"]
    
    # Apply variance based on threat level
    variance = {
        ThreatLevel.MINION: 0,
        ThreatLevel.STANDARD: 1,
        ThreatLevel.ELITE: 1,
        ThreatLevel.BOSS: 2,
    }.get(threat_level, 1)
    
    stats = EntityStats(
        combat=_apply_variance(base_stats[0], variance),
        defense=_apply_variance(base_stats[1], variance),
        speed=_apply_variance(base_stats[2], variance),
        special=_apply_variance(base_stats[3], variance),
    )
    
    name = name_override or template["name"]
    description = template["desc"]
    
    # Enrich description with context if provided
    if context:
        description = f"{description} [Contexte: {context}]"
    
    return Entity(
        name=name,
        faction=faction,
        threat_level=threat_level,
        stats=stats,
        abilities=list(template.get("abilities", [])),
        weakness=template.get("weakness"),
        description=description,
    )


def generate_encounter(
    faction: Faction,
    difficulty: str = "standard",
    context: Optional[str] = None,
) -> List[Entity]:
    """
    Generate a balanced encounter for the given faction and difficulty.
    
    Args:
        faction: The faction to generate enemies from.
        difficulty: "easy", "standard", "hard", or "deadly".
        context: Narrative context for the encounter.
    
    Returns:
        List of entities forming the encounter.
    """
    encounter_configs = {
        "easy": [(ThreatLevel.MINION, 2)],
        "standard": [(ThreatLevel.MINION, 3), (ThreatLevel.STANDARD, 1)],
        "hard": [(ThreatLevel.MINION, 2), (ThreatLevel.STANDARD, 2), (ThreatLevel.ELITE, 1)],
        "deadly": [(ThreatLevel.STANDARD, 2), (ThreatLevel.ELITE, 2), (ThreatLevel.BOSS, 1)],
    }
    
    config = encounter_configs.get(difficulty, encounter_configs["standard"])
    entities = []
    
    for threat_level, count in config:
        for _ in range(count):
            entity = generate_entity(faction, threat_level, context)
            entities.append(entity)
    
    return entities


def generate_npc(
    role: str,
    faction: Faction = Faction.CIVILIAN,
    threat_level: ThreatLevel = ThreatLevel.STANDARD,
    context: Optional[str] = None,
) -> Entity:
    """
    Generate a named NPC with a specific role.
    
    Args:
        role: The role/profession of the NPC.
        faction: Their allegiance.
        threat_level: How capable they are.
        context: Narrative context.
    
    Returns:
        A generated NPC entity.
    """
    # Generate a grimdark name
    prefixes = ["Varn", "Kael", "Mor", "Sev", "Drak", "Thul", "Grim", "Vik", "Zael", "Brak"]
    suffixes = ["us", "ax", "on", "ek", "or", "an", "is", "os", "ar", "en"]
    
    name = random.choice(prefixes) + random.choice(suffixes)
    
    entity = generate_entity(faction, threat_level, context, name_override=name)
    entity.description = f"{role}. {entity.description}"
    
    return entity


# ---------------------------------------------------------------------------
# Utility for prompt injection
# ---------------------------------------------------------------------------

def encounter_to_prompt(entities: List[Entity]) -> str:
    """Format an encounter for injection into the MJ prompt."""
    blocks = [e.to_prompt_block() for e in entities]
    return "Entites presentes: " + " ".join(blocks)


def entity_difficulty_for_player(entity: Entity, player_combat: int = 3) -> str:
    """Estimate how dangerous an entity is for the player."""
    threat = entity.stats.total_threat()
    if threat <= player_combat + 2:
        return "Gerable"
    elif threat <= player_combat + 5:
        return "Dangereux"
    elif threat <= player_combat + 8:
        return "Tres dangereux"
    else:
        return "Mortel"
