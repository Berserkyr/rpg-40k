"""
Systeme de progression - XP, niveaux et arbre de competences
Survivant de Ruche - Warhammer 40K Solo RPG
"""
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class SkillCategory(Enum):
    """Categories de competences."""
    COMBAT = "combat"
    SURVIE = "survie"
    SOCIAL = "social"
    TECHNIQUE = "technique"
    FOI = "foi"
    OMBRE = "ombre"


@dataclass
class Skill:
    """Une competence deblocable."""
    id: str
    name: str
    description: str
    category: SkillCategory
    xp_cost: int
    level_required: int
    prerequisites: list[str] = field(default_factory=list)
    # Bonus accordes
    attribute_bonus: dict[str, int] = field(default_factory=dict)
    special_ability: Optional[str] = None
    passive: bool = False


@dataclass
class ProgressionState:
    """Etat de progression du personnage."""
    level: int = 1
    current_xp: int = 0
    total_xp_earned: int = 0
    skills_unlocked: list[str] = field(default_factory=list)
    attribute_points_available: int = 0
    
    def xp_for_next_level(self) -> int:
        """XP requis pour le prochain niveau."""
        # Progression: 100, 250, 450, 700, 1000, 1350...
        return 100 + (self.level - 1) * 150 + (self.level - 1) ** 2 * 25
    
    def xp_to_next_level(self) -> int:
        """XP restant avant le prochain niveau."""
        return max(0, self.xp_for_next_level() - self.current_xp)
    
    def can_level_up(self) -> bool:
        """Verifie si le personnage peut monter de niveau."""
        return self.current_xp >= self.xp_for_next_level()
    
    def add_xp(self, amount: int) -> list[str]:
        """
        Ajoute de l'XP et gere les montees de niveau.
        Retourne les messages de montee de niveau.
        """
        messages = []
        self.current_xp += amount
        self.total_xp_earned += amount
        
        while self.can_level_up():
            overflow = self.current_xp - self.xp_for_next_level()
            self.level += 1
            self.current_xp = overflow
            self.attribute_points_available += 1
            messages.append(
                f"NIVEAU {self.level} ATTEINT! +1 point d'attribut disponible."
            )
        
        return messages
    
    def has_skill(self, skill_id: str) -> bool:
        """Verifie si une competence est deja debloquee."""
        return skill_id in self.skills_unlocked
    
    def can_unlock_skill(self, skill: Skill) -> tuple[bool, str]:
        """
        Verifie si une competence peut etre debloquee.
        Retourne (possible, raison).
        """
        if self.has_skill(skill.id):
            return False, "Competence deja acquise"
        
        if self.level < skill.level_required:
            return False, f"Niveau {skill.level_required} requis (actuel: {self.level})"
        
        if self.current_xp < skill.xp_cost:
            return False, f"XP insuffisant ({self.current_xp}/{skill.xp_cost})"
        
        for prereq in skill.prerequisites:
            if prereq not in self.skills_unlocked:
                return False, f"Prerequis manquant: {prereq}"
        
        return True, "OK"
    
    def unlock_skill(self, skill: Skill) -> tuple[bool, str]:
        """
        Tente de debloquer une competence.
        Retourne (succes, message).
        """
        can_unlock, reason = self.can_unlock_skill(skill)
        if not can_unlock:
            return False, reason
        
        self.current_xp -= skill.xp_cost
        self.skills_unlocked.append(skill.id)
        return True, f"Competence '{skill.name}' debloquee!"
    
    def to_dict(self) -> dict:
        """Serialise l'etat de progression."""
        return {
            "level": self.level,
            "current_xp": self.current_xp,
            "total_xp_earned": self.total_xp_earned,
            "skills_unlocked": self.skills_unlocked.copy(),
            "attribute_points_available": self.attribute_points_available,
            "xp_to_next_level": self.xp_to_next_level(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProgressionState":
        """Charge l'etat depuis un dict."""
        state = cls(
            level=data.get("level", 1),
            current_xp=data.get("current_xp", 0),
            total_xp_earned=data.get("total_xp_earned", 0),
            attribute_points_available=data.get("attribute_points_available", 0),
        )
        state.skills_unlocked = data.get("skills_unlocked", []).copy()
        return state


# =============================================================================
# ARBRE DE COMPETENCES
# =============================================================================

SKILL_TREE: dict[str, Skill] = {}


def _register_skill(skill: Skill) -> Skill:
    """Enregistre une competence dans l'arbre."""
    SKILL_TREE[skill.id] = skill
    return skill


# --- COMBAT ---
_register_skill(Skill(
    id="combat_base",
    name="Entrainement de base",
    description="Vous savez tenir une arme sans vous blesser. +1 aux jets d'attaque.",
    category=SkillCategory.COMBAT,
    xp_cost=50,
    level_required=1,
    attribute_bonus={"attaque": 1},
    passive=True,
))

_register_skill(Skill(
    id="coup_desespere",
    name="Coup desespere",
    description="Quand vous etes a 1 PV, vos attaques infligent +2 degats.",
    category=SkillCategory.COMBAT,
    xp_cost=100,
    level_required=2,
    prerequisites=["combat_base"],
    special_ability="coup_desespere",
))

_register_skill(Skill(
    id="parade",
    name="Parade",
    description="Une fois par combat, annulez completement une attaque ennemie.",
    category=SkillCategory.COMBAT,
    xp_cost=150,
    level_required=3,
    prerequisites=["combat_base"],
    special_ability="parade",
))

_register_skill(Skill(
    id="fureur_imperiale",
    name="Fureur imperiale",
    description="Sacrifiez 2 Stress pour relancer tous vos des d'attaque.",
    category=SkillCategory.COMBAT,
    xp_cost=200,
    level_required=4,
    prerequisites=["coup_desespere", "parade"],
    special_ability="fureur_imperiale",
))

# --- SURVIE ---
_register_skill(Skill(
    id="endurci",
    name="Endurci",
    description="Les rues de la ruche vous ont forge. +1 PV max.",
    category=SkillCategory.SURVIE,
    xp_cost=50,
    level_required=1,
    attribute_bonus={"pv_max": 1},
    passive=True,
))

_register_skill(Skill(
    id="recuperation",
    name="Recuperation",
    description="Recuperez 1 PV supplementaire lors des repos.",
    category=SkillCategory.SURVIE,
    xp_cost=75,
    level_required=2,
    prerequisites=["endurci"],
    special_ability="recuperation",
))

_register_skill(Skill(
    id="instinct_danger",
    name="Instinct du danger",
    description="+2 aux jets pour eviter les pieges et embuscades.",
    category=SkillCategory.SURVIE,
    xp_cost=100,
    level_required=2,
    attribute_bonus={"evasion_piege": 2},
    passive=True,
))

_register_skill(Skill(
    id="survivant_ne",
    name="Survivant-ne",
    description="Une fois par session, ignorez une blessure mortelle (restez a 1 PV).",
    category=SkillCategory.SURVIE,
    xp_cost=250,
    level_required=5,
    prerequisites=["recuperation", "instinct_danger"],
    special_ability="survivant_ne",
))

# --- SOCIAL ---
_register_skill(Skill(
    id="langue_bien_pendue",
    name="Langue bien pendue",
    description="+1 aux jets de persuasion et negociation.",
    category=SkillCategory.SOCIAL,
    xp_cost=50,
    level_required=1,
    attribute_bonus={"persuasion": 1},
    passive=True,
))

_register_skill(Skill(
    id="contacts",
    name="Reseau de contacts",
    description="Vous connaissez quelqu'un dans chaque secteur. Bonus aux recherches d'info.",
    category=SkillCategory.SOCIAL,
    xp_cost=100,
    level_required=2,
    prerequisites=["langue_bien_pendue"],
    special_ability="contacts",
))

_register_skill(Skill(
    id="intimidation",
    name="Regard de l'Empereur",
    description="Votre regard glace le sang. +2 aux jets d'intimidation.",
    category=SkillCategory.SOCIAL,
    xp_cost=75,
    level_required=2,
    attribute_bonus={"intimidation": 2},
    passive=True,
))

# --- TECHNIQUE ---
_register_skill(Skill(
    id="bricoleur",
    name="Bricoleur",
    description="Reparations improvisees. +1 aux jets techniques.",
    category=SkillCategory.TECHNIQUE,
    xp_cost=50,
    level_required=1,
    attribute_bonus={"technique": 1},
    passive=True,
))

_register_skill(Skill(
    id="sabotage",
    name="Sabotage",
    description="Desactivez ou piégez les systemes mecaniques.",
    category=SkillCategory.TECHNIQUE,
    xp_cost=100,
    level_required=2,
    prerequisites=["bricoleur"],
    special_ability="sabotage",
))

_register_skill(Skill(
    id="tech_heresy",
    name="Heresie technique",
    description="Utilisez les technologies xenophiles ou heretiques. +2 Corruption a l'apprentissage.",
    category=SkillCategory.TECHNIQUE,
    xp_cost=150,
    level_required=3,
    prerequisites=["sabotage"],
    special_ability="tech_heresy",
))

# --- FOI ---
_register_skill(Skill(
    id="priere_empereur",
    name="Priere a l'Empereur",
    description="Murmurez une priere pour -1 Stress.",
    category=SkillCategory.FOI,
    xp_cost=50,
    level_required=1,
    special_ability="priere",
))

_register_skill(Skill(
    id="foi_inébranlable",
    name="Foi inebranlable",
    description="La corruption ne peut vous atteindre facilement. Resistez a +2 aux jets anti-corruption.",
    category=SkillCategory.FOI,
    xp_cost=100,
    level_required=2,
    prerequisites=["priere_empereur"],
    attribute_bonus={"resistance_corruption": 2},
    passive=True,
))

_register_skill(Skill(
    id="martyr",
    name="Esprit du Martyr",
    description="Subissez les degats a la place d'un allie une fois par combat.",
    category=SkillCategory.FOI,
    xp_cost=150,
    level_required=3,
    prerequisites=["foi_inébranlable"],
    special_ability="martyr",
))

# --- OMBRE ---
_register_skill(Skill(
    id="furtivite",
    name="Furtivite",
    description="Vous savez vous fondre dans les tenebres. +1 Discretion.",
    category=SkillCategory.OMBRE,
    xp_cost=50,
    level_required=1,
    attribute_bonus={"discretion": 1},
    passive=True,
))

_register_skill(Skill(
    id="coup_sournois",
    name="Coup sournois",
    description="Attaques depuis les ombres: +3 degats si non detecte.",
    category=SkillCategory.OMBRE,
    xp_cost=100,
    level_required=2,
    prerequisites=["furtivite"],
    special_ability="coup_sournois",
))

_register_skill(Skill(
    id="evasion",
    name="Evasion",
    description="Fuyez automatiquement un combat une fois par session.",
    category=SkillCategory.OMBRE,
    xp_cost=150,
    level_required=3,
    prerequisites=["furtivite"],
    special_ability="evasion_auto",
))

_register_skill(Skill(
    id="fantome",
    name="Fantome de la Ruche",
    description="Traversez les zones dangereuses sans declencer d'alerte.",
    category=SkillCategory.OMBRE,
    xp_cost=200,
    level_required=4,
    prerequisites=["coup_sournois", "evasion"],
    special_ability="fantome",
))


# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def get_skills_by_category(category: SkillCategory) -> list[Skill]:
    """Retourne toutes les competences d'une categorie."""
    return [s for s in SKILL_TREE.values() if s.category == category]


def get_available_skills(progression: ProgressionState) -> list[Skill]:
    """Retourne les competences deblocables par le personnage."""
    available = []
    for skill in SKILL_TREE.values():
        can_unlock, _ = progression.can_unlock_skill(skill)
        if can_unlock:
            available.append(skill)
    return available


def get_unlocked_skills(progression: ProgressionState) -> list[Skill]:
    """Retourne les competences deja acquises."""
    return [SKILL_TREE[sid] for sid in progression.skills_unlocked if sid in SKILL_TREE]


def calculate_total_bonuses(progression: ProgressionState) -> dict[str, int]:
    """Calcule tous les bonus passifs des competences acquises."""
    bonuses: dict[str, int] = {}
    for skill in get_unlocked_skills(progression):
        if skill.passive:
            for attr, bonus in skill.attribute_bonus.items():
                bonuses[attr] = bonuses.get(attr, 0) + bonus
    return bonuses


def get_special_abilities(progression: ProgressionState) -> list[str]:
    """Retourne la liste des capacites speciales disponibles."""
    abilities = []
    for skill in get_unlocked_skills(progression):
        if skill.special_ability:
            abilities.append(skill.special_ability)
    return abilities


def format_skill_tree(progression: ProgressionState) -> str:
    """Formate l'arbre de competences pour affichage."""
    lines = ["=== ARBRE DE COMPETENCES ===", ""]
    
    for category in SkillCategory:
        skills = get_skills_by_category(category)
        if not skills:
            continue
        
        lines.append(f"--- {category.value.upper()} ---")
        
        for skill in sorted(skills, key=lambda s: s.level_required):
            if progression.has_skill(skill.id):
                status = "[X]"
            elif progression.can_unlock_skill(skill)[0]:
                status = "[ ]"
            else:
                status = "[#]"  # Verrouille
            
            prereq_str = ""
            if skill.prerequisites:
                prereq_str = f" (Requis: {', '.join(skill.prerequisites)})"
            
            lines.append(
                f"  {status} {skill.name} (Niv.{skill.level_required}, {skill.xp_cost} XP){prereq_str}"
            )
            lines.append(f"      {skill.description}")
        
        lines.append("")
    
    return "\n".join(lines)


# =============================================================================
# XP REWARDS
# =============================================================================

XP_REWARDS = {
    # Actions
    "survie_scene": 10,
    "objectif_mineur": 25,
    "objectif_majeur": 75,
    "quete_complete": 150,
    
    # Combat
    "victoire_facile": 15,
    "victoire_difficile": 35,
    "victoire_heroique": 60,
    "fuite_reussie": 10,
    
    # Roleplay
    "decision_difficile": 20,
    "sacrifice": 50,
    "revelation_lore": 30,
    
    # Exploration
    "nouvelle_zone": 20,
    "secret_decouvert": 40,
    "pnj_important": 25,
}


def award_xp(progression: ProgressionState, reason: str, custom_amount: int = 0) -> tuple[int, list[str]]:
    """
    Attribue de l'XP et retourne (montant, messages).
    """
    if custom_amount > 0:
        amount = custom_amount
    else:
        amount = XP_REWARDS.get(reason, 10)
    
    messages = progression.add_xp(amount)
    messages.insert(0, f"+{amount} XP ({reason})")
    
    return amount, messages
