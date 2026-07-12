"""Gestion d'equipe - compagnons persistants pour les combats de groupe.

Le joueur peut recruter des compagnons (via la negociation ou le ralliement)
qui l'accompagnent au combat. L'equipe est persistee dans team.yaml.

Module volontairement independant de FastAPI et de l'UI pour rester testable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Companion:
    """Un membre de l'equipe."""
    id: str
    name: str
    archetype: str
    combat: int
    defense: int
    speed: int
    special: int
    max_health: int
    level_required: int = 1

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "archetype": self.archetype,
            "combat": self.combat,
            "defense": self.defense,
            "speed": self.speed,
            "special": self.special,
            "max_health": self.max_health,
            "level_required": self.level_required,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Companion":
        return cls(
            id=data["id"],
            name=data.get("name", data["id"]),
            archetype=data.get("archetype", "milicien"),
            combat=int(data.get("combat", 4)),
            defense=int(data.get("defense", 3)),
            speed=int(data.get("speed", 3)),
            special=int(data.get("special", 2)),
            max_health=int(data.get("max_health", 8)),
            level_required=int(data.get("level_required", 1)),
        )


# Archetypes recrutables. Chaque template definit les stats de base et le
# niveau requis pour l'enroler (progression du joueur).
COMPANION_TEMPLATES: Dict[str, dict] = {
    "milicien": {
        "name": "Milicien de la Ruche",
        "archetype": "milicien",
        "combat": 4, "defense": 3, "speed": 3, "special": 2,
        "max_health": 8, "level_required": 1,
    },
    "eclaireur": {
        "name": "Eclaireur furtif",
        "archetype": "eclaireur",
        "combat": 5, "defense": 2, "speed": 5, "special": 2,
        "max_health": 7, "level_required": 2,
    },
    "sororitas": {
        "name": "Soeur de Bataille",
        "archetype": "sororitas",
        "combat": 6, "defense": 4, "speed": 3, "special": 5,
        "max_health": 12, "level_required": 4,
    },
    "tech_pretre": {
        "name": "Tech-pretre",
        "archetype": "tech_pretre",
        "combat": 4, "defense": 4, "speed": 2, "special": 6,
        "max_health": 10, "level_required": 3,
    },
}


@dataclass
class Team:
    """Roster d'equipe persistant."""
    members: List[Companion] = field(default_factory=list)
    max_size: int = 3

    def is_full(self) -> bool:
        return len(self.members) >= self.max_size

    def has(self, companion_id: str) -> bool:
        return any(m.id == companion_id for m in self.members)

    def add(self, companion: Companion) -> tuple[bool, str]:
        if self.is_full():
            return False, "L'equipe est complete."
        if self.has(companion.id):
            return False, "Ce compagnon fait deja partie de l'equipe."
        self.members.append(companion)
        return True, f"{companion.name} rejoint l'equipe."

    def remove(self, companion_id: str) -> tuple[bool, str]:
        for i, m in enumerate(self.members):
            if m.id == companion_id:
                removed = self.members.pop(i)
                return True, f"{removed.name} quitte l'equipe."
        return False, "Compagnon introuvable."

    def to_dict(self) -> dict:
        return {
            "members": [m.to_dict() for m in self.members],
            "max_size": self.max_size,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Team":
        team = cls(max_size=int(data.get("max_size", 3)))
        team.members = [Companion.from_dict(m) for m in data.get("members", [])]
        return team


def create_companion(template_id: str, level: int) -> tuple[Companion | None, str]:
    """Cree un compagnon a partir d'un archetype, si le niveau le permet."""
    template = COMPANION_TEMPLATES.get(template_id)
    if not template:
        return None, "Archetype inconnu."
    if level < template["level_required"]:
        return None, f"Niveau {template['level_required']} requis pour ce compagnon."
    companion = Companion(
        id=template_id,
        name=template["name"],
        archetype=template["archetype"],
        combat=template["combat"],
        defense=template["defense"],
        speed=template["speed"],
        special=template["special"],
        max_health=template["max_health"],
        level_required=template["level_required"],
    )
    return companion, f"{companion.name} est pret a combattre."


def available_templates(level: int) -> List[dict]:
    """Liste les archetypes recrutables au niveau donne."""
    result = []
    for tid, tpl in COMPANION_TEMPLATES.items():
        entry = dict(tpl)
        entry["id"] = tid
        entry["unlocked"] = level >= tpl["level_required"]
        result.append(entry)
    return result
