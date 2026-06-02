"""
Systeme de quetes - Missions, objectifs et recompenses
Survivant de Ruche - Warhammer 40K Solo RPG
"""
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class QuestType(Enum):
    """Types de quetes."""
    PRINCIPALE = "principale"     # Histoire principale
    SECONDAIRE = "secondaire"     # Quetes optionnelles
    URGENTE = "urgente"           # Limite de temps
    CACHEE = "cachee"             # Decouverte par exploration
    REPETABLE = "repetable"       # Peut etre refaite


class QuestStatus(Enum):
    """Statut d'une quete."""
    DISPONIBLE = "disponible"     # Peut etre acceptee
    ACTIVE = "active"             # En cours
    COMPLETEE = "completee"       # Terminee avec succes
    ECHOUEE = "echouee"           # Ratee
    EXPIREE = "expiree"           # Temps ecoule
    CACHEE = "cachee"             # Non encore decouverte


@dataclass
class QuestObjective:
    """Un objectif de quete."""
    id: str
    description: str
    completed: bool = False
    optional: bool = False
    hidden: bool = False  # Revele quand atteint
    
    # Conditions de completion
    target_zone: Optional[str] = None
    target_npc: Optional[str] = None
    target_item: Optional[str] = None
    target_kill_count: int = 0
    current_kill_count: int = 0
    
    def is_complete(self) -> bool:
        """Verifie si l'objectif est complete."""
        if self.completed:
            return True
        if self.target_kill_count > 0:
            return self.current_kill_count >= self.target_kill_count
        return False
    
    def progress_text(self) -> str:
        """Retourne le texte de progression."""
        if self.target_kill_count > 0:
            return f"{self.current_kill_count}/{self.target_kill_count}"
        if self.completed:
            return "[X]"
        return "[ ]"


@dataclass 
class QuestReward:
    """Recompenses de quete."""
    xp: int = 0
    credits: int = 0
    items: list[str] = field(default_factory=list)
    reputation_changes: dict[str, int] = field(default_factory=dict)
    unlock_zones: list[str] = field(default_factory=list)
    unlock_quests: list[str] = field(default_factory=list)
    special: Optional[str] = None


@dataclass
class Quest:
    """Une quete complete."""
    id: str
    title: str
    description: str
    quest_type: QuestType
    status: QuestStatus = QuestStatus.DISPONIBLE
    
    # Objectifs
    objectives: list[QuestObjective] = field(default_factory=list)
    
    # Recompenses
    reward: QuestReward = field(default_factory=QuestReward)
    failure_penalty: Optional[QuestReward] = None  # Consequences d'echec
    
    # Conditions
    level_required: int = 1
    prerequisite_quests: list[str] = field(default_factory=list)
    zone_required: Optional[str] = None
    
    # Limite de temps (en scenes)
    time_limit: int = 0  # 0 = pas de limite
    scenes_elapsed: int = 0
    
    # Narratif
    giver_npc: Optional[str] = None
    completion_text: str = ""
    failure_text: str = ""
    
    # Journal
    journal_entries: list[str] = field(default_factory=list)
    
    def is_complete(self) -> bool:
        """Verifie si tous les objectifs obligatoires sont completes."""
        for obj in self.objectives:
            if not obj.optional and not obj.is_complete():
                return False
        return True
    
    def is_expired(self) -> bool:
        """Verifie si la quete a expire."""
        if self.time_limit > 0:
            return self.scenes_elapsed >= self.time_limit
        return False
    
    def progress_percentage(self) -> float:
        """Retourne le pourcentage de completion."""
        required = [o for o in self.objectives if not o.optional]
        if not required:
            return 100.0
        completed = sum(1 for o in required if o.is_complete())
        return (completed / len(required)) * 100
    
    def add_journal_entry(self, entry: str) -> None:
        """Ajoute une entree au journal."""
        self.journal_entries.append(entry)
    
    def advance_time(self) -> bool:
        """Avance le temps et retourne True si expiree."""
        if self.time_limit > 0:
            self.scenes_elapsed += 1
            if self.is_expired():
                self.status = QuestStatus.EXPIREE
                return True
        return False
    
    def to_dict(self) -> dict:
        """Serialise la quete."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "quest_type": self.quest_type.value,
            "status": self.status.value,
            "objectives": [
                {
                    "id": obj.id,
                    "description": obj.description,
                    "completed": obj.completed,
                    "optional": obj.optional,
                    "hidden": obj.hidden,
                    "target_zone": obj.target_zone,
                    "target_npc": obj.target_npc,
                    "target_item": obj.target_item,
                    "target_kill_count": obj.target_kill_count,
                    "current_kill_count": obj.current_kill_count,
                }
                for obj in self.objectives
            ],
            "reward": {
                "xp": self.reward.xp,
                "credits": self.reward.credits,
                "items": self.reward.items.copy(),
                "reputation_changes": self.reward.reputation_changes.copy(),
                "unlock_zones": self.reward.unlock_zones.copy(),
                "unlock_quests": self.reward.unlock_quests.copy(),
                "special": self.reward.special,
            },
            "level_required": self.level_required,
            "prerequisite_quests": self.prerequisite_quests.copy(),
            "zone_required": self.zone_required,
            "time_limit": self.time_limit,
            "scenes_elapsed": self.scenes_elapsed,
            "giver_npc": self.giver_npc,
            "completion_text": self.completion_text,
            "failure_text": self.failure_text,
            "journal_entries": self.journal_entries.copy(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Quest":
        """Charge une quete depuis un dict."""
        reward_data = data.get("reward", {})
        reward = QuestReward(
            xp=reward_data.get("xp", 0),
            credits=reward_data.get("credits", 0),
            items=reward_data.get("items", []).copy(),
            reputation_changes=reward_data.get("reputation_changes", {}).copy(),
            unlock_zones=reward_data.get("unlock_zones", []).copy(),
            unlock_quests=reward_data.get("unlock_quests", []).copy(),
            special=reward_data.get("special"),
        )
        
        quest = cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            quest_type=QuestType(data["quest_type"]),
            status=QuestStatus(data.get("status", "disponible")),
            reward=reward,
            level_required=data.get("level_required", 1),
            zone_required=data.get("zone_required"),
            time_limit=data.get("time_limit", 0),
            scenes_elapsed=data.get("scenes_elapsed", 0),
            giver_npc=data.get("giver_npc"),
            completion_text=data.get("completion_text", ""),
            failure_text=data.get("failure_text", ""),
        )
        
        quest.prerequisite_quests = data.get("prerequisite_quests", []).copy()
        quest.journal_entries = data.get("journal_entries", []).copy()
        
        for obj_data in data.get("objectives", []):
            quest.objectives.append(QuestObjective(
                id=obj_data["id"],
                description=obj_data["description"],
                completed=obj_data.get("completed", False),
                optional=obj_data.get("optional", False),
                hidden=obj_data.get("hidden", False),
                target_zone=obj_data.get("target_zone"),
                target_npc=obj_data.get("target_npc"),
                target_item=obj_data.get("target_item"),
                target_kill_count=obj_data.get("target_kill_count", 0),
                current_kill_count=obj_data.get("current_kill_count", 0),
            ))
        
        return quest


@dataclass
class QuestLog:
    """Journal de quetes du personnage."""
    quests: dict[str, Quest] = field(default_factory=dict)
    completed_quest_ids: list[str] = field(default_factory=list)
    failed_quest_ids: list[str] = field(default_factory=list)
    
    def add_quest(self, quest: Quest) -> None:
        """Ajoute une quete au journal."""
        self.quests[quest.id] = quest
    
    def get_quest(self, quest_id: str) -> Optional[Quest]:
        """Recupere une quete par ID."""
        return self.quests.get(quest_id)
    
    def accept_quest(self, quest_id: str) -> tuple[bool, str]:
        """Accepte une quete."""
        quest = self.quests.get(quest_id)
        if not quest:
            return False, "Quete inconnue"
        
        if quest.status != QuestStatus.DISPONIBLE:
            return False, f"Quete non disponible (statut: {quest.status.value})"
        
        quest.status = QuestStatus.ACTIVE
        quest.add_journal_entry("Quete acceptee.")
        return True, f"Quete '{quest.title}' acceptee!"
    
    def complete_objective(self, quest_id: str, objective_id: str) -> tuple[bool, str]:
        """Marque un objectif comme complete."""
        quest = self.quests.get(quest_id)
        if not quest:
            return False, "Quete inconnue"
        
        for obj in quest.objectives:
            if obj.id == objective_id:
                obj.completed = True
                quest.add_journal_entry(f"Objectif complete: {obj.description}")
                
                if quest.is_complete():
                    return True, f"Tous les objectifs de '{quest.title}' sont completes!"
                return True, f"Objectif complete: {obj.description}"
        
        return False, "Objectif inconnu"
    
    def update_kill_count(self, quest_id: str, objective_id: str, count: int = 1) -> tuple[bool, str]:
        """Met a jour le compteur de kills."""
        quest = self.quests.get(quest_id)
        if not quest:
            return False, "Quete inconnue"
        
        for obj in quest.objectives:
            if obj.id == objective_id:
                obj.current_kill_count += count
                if obj.is_complete():
                    obj.completed = True
                    quest.add_journal_entry(f"Objectif complete: {obj.description}")
                return True, f"Progres: {obj.current_kill_count}/{obj.target_kill_count}"
        
        return False, "Objectif inconnu"
    
    def complete_quest(self, quest_id: str) -> tuple[bool, str, Optional[QuestReward]]:
        """Complete une quete et retourne les recompenses."""
        quest = self.quests.get(quest_id)
        if not quest:
            return False, "Quete inconnue", None
        
        if not quest.is_complete():
            return False, "Objectifs non completes", None
        
        quest.status = QuestStatus.COMPLETEE
        quest.add_journal_entry("QUETE TERMINEE!")
        self.completed_quest_ids.append(quest_id)
        
        return True, quest.completion_text or f"Quete '{quest.title}' terminee!", quest.reward
    
    def fail_quest(self, quest_id: str, reason: str = "") -> tuple[bool, str]:
        """Fait echouer une quete."""
        quest = self.quests.get(quest_id)
        if not quest:
            return False, "Quete inconnue"
        
        quest.status = QuestStatus.ECHOUEE
        quest.add_journal_entry(f"QUETE ECHOUEE: {reason}" if reason else "QUETE ECHOUEE")
        self.failed_quest_ids.append(quest_id)
        
        return True, quest.failure_text or f"Quete '{quest.title}' echouee..."
    
    def get_active_quests(self) -> list[Quest]:
        """Retourne les quetes actives."""
        return [q for q in self.quests.values() if q.status == QuestStatus.ACTIVE]
    
    def get_available_quests(self) -> list[Quest]:
        """Retourne les quetes disponibles."""
        return [q for q in self.quests.values() if q.status == QuestStatus.DISPONIBLE]
    
    def advance_all_timers(self) -> list[str]:
        """Avance les timers de toutes les quetes actives."""
        expired = []
        for quest in self.get_active_quests():
            if quest.advance_time():
                expired.append(f"QUETE EXPIREE: {quest.title}")
                self.failed_quest_ids.append(quest.id)
        return expired
    
    def to_dict(self) -> dict:
        """Serialise le journal."""
        return {
            "quests": {qid: q.to_dict() for qid, q in self.quests.items()},
            "completed_quest_ids": self.completed_quest_ids.copy(),
            "failed_quest_ids": self.failed_quest_ids.copy(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "QuestLog":
        """Charge le journal depuis un dict."""
        log = cls()
        log.completed_quest_ids = data.get("completed_quest_ids", []).copy()
        log.failed_quest_ids = data.get("failed_quest_ids", []).copy()
        for quest_data in data.get("quests", {}).values():
            quest = Quest.from_dict(quest_data)
            log.quests[quest.id] = quest
        return log


# =============================================================================
# QUETES DE DEPART
# =============================================================================

def create_starting_quests() -> QuestLog:
    """Cree les quetes de depart du jeu."""
    log = QuestLog()
    
    # Quete principale 1 - Survie immediate
    log.add_quest(Quest(
        id="survie_jour_1",
        title="Premier Jour",
        description="L'invasion a commence. Vous devez trouver des provisions et un abri sur "
                    "avant la tombee de la nuit.",
        quest_type=QuestType.PRINCIPALE,
        status=QuestStatus.ACTIVE,
        objectives=[
            QuestObjective(
                id="trouver_eau",
                description="Trouver de l'eau potable",
                target_item="eau",
            ),
            QuestObjective(
                id="trouver_nourriture",
                description="Trouver des rations",
                target_item="rations",
            ),
            QuestObjective(
                id="securiser_abri",
                description="Securiser un abri pour la nuit",
                target_zone="hab_block_7",
            ),
        ],
        reward=QuestReward(
            xp=50,
            unlock_quests=["signal_vox"],
        ),
        time_limit=5,  # 5 scenes
        completion_text="Vous avez survecu au premier jour. Mais ce n'est que le debut...",
    ))
    
    # Quete principale 2 - Signal Vox
    log.add_quest(Quest(
        id="signal_vox",
        title="Le Signal",
        description="En tant que technicien vox, vous avez capte un signal faible. "
                    "Il semble provenir du checkpoint PDF abandonne.",
        quest_type=QuestType.PRINCIPALE,
        status=QuestStatus.DISPONIBLE,
        objectives=[
            QuestObjective(
                id="atteindre_checkpoint",
                description="Atteindre le checkpoint PDF",
                target_zone="checkpoint_pdf",
            ),
            QuestObjective(
                id="reparer_vox",
                description="Reparer l'equipement vox militaire",
            ),
            QuestObjective(
                id="decoder_signal",
                description="Decoder le message",
            ),
        ],
        reward=QuestReward(
            xp=100,
            items=["vox_militaire"],
            unlock_quests=["contact_resistance"],
        ),
        prerequisite_quests=["survie_jour_1"],
        completion_text="Le message est clair: une resistance s'organise au Temple de l'Empereur.",
    ))
    
    # Quete secondaire - Marche noir
    log.add_quest(Quest(
        id="commerce_noir",
        title="Le Marche des Ombres",
        description="Des rumeurs parlent d'un marche noir ou l'on peut trouver de tout. "
                    "Cela pourrait etre utile...",
        quest_type=QuestType.SECONDAIRE,
        status=QuestStatus.DISPONIBLE,
        objectives=[
            QuestObjective(
                id="trouver_marche",
                description="Trouver le marche noir",
                target_zone="marche_noir",
            ),
            QuestObjective(
                id="rencontrer_grox",
                description="Rencontrer Grox le marchand d'armes",
                target_npc="grox",
                optional=True,
            ),
        ],
        reward=QuestReward(
            xp=40,
            credits=25,
            reputation_changes={"marchands": 10},
        ),
        zone_required="corridor_principal",
    ))
    
    # Quete secondaire - Voisins
    log.add_quest(Quest(
        id="voisins_disparus",
        title="Les Disparus du Delta",
        description="Vous avez entendu des cris provenant du bloc voisin. "
                    "Des survivants sont peut-etre pieges.",
        quest_type=QuestType.SECONDAIRE,
        status=QuestStatus.DISPONIBLE,
        objectives=[
            QuestObjective(
                id="explorer_delta",
                description="Explorer le Bloc 7-Delta",
                target_zone="bloc_voisin",
            ),
            QuestObjective(
                id="trouver_survivants",
                description="Chercher des survivants",
            ),
            QuestObjective(
                id="choix_final",
                description="Decider du sort des survivants",
            ),
        ],
        reward=QuestReward(
            xp=60,
            reputation_changes={"civils": 15},
            special="allie_potentiel",
        ),
        time_limit=8,
        failure_text="Les cris se sont tus. Il est trop tard...",
    ))
    
    # Quete urgente - Creature dans les tenebres
    log.add_quest(Quest(
        id="creature_sous_sol",
        title="Bruits dans l'Obscurite",
        description="Quelque chose rode dans les sous-sols. Les survivants ont peur "
                    "de descendre chercher des provisions.",
        quest_type=QuestType.URGENTE,
        status=QuestStatus.DISPONIBLE,
        objectives=[
            QuestObjective(
                id="descendre_sous_sol",
                description="Descendre dans les sous-sols",
                target_zone="sous_sol",
            ),
            QuestObjective(
                id="identifier_menace",
                description="Identifier la menace",
            ),
            QuestObjective(
                id="eliminer_neutraliser",
                description="Eliminer ou neutraliser la creature",
            ),
        ],
        reward=QuestReward(
            xp=80,
            items=["trophee_creature"],
            unlock_zones=["cave_stockage"],
        ),
        time_limit=3,
        failure_penalty=QuestReward(
            reputation_changes={"civils": -10},
        ),
    ))
    
    # Quete cachee - Temple secret
    log.add_quest(Quest(
        id="secret_temple",
        title="La Crypte Oubliee",
        description="Les tunnels de maintenance menent a un passage secret vers le temple...",
        quest_type=QuestType.CACHEE,
        status=QuestStatus.CACHEE,
        objectives=[
            QuestObjective(
                id="decouvrir_passage",
                description="Decouvrir le passage secret",
                target_zone="tunnels_maintenance",
                hidden=True,
            ),
            QuestObjective(
                id="atteindre_crypte",
                description="Atteindre la crypte du temple",
            ),
            QuestObjective(
                id="secret_crypte",
                description="Decouvrir le secret de la crypte",
            ),
        ],
        reward=QuestReward(
            xp=120,
            items=["relique_empereur"],
            special="benediction_empereur",
        ),
        zone_required="tunnels_maintenance",
    ))
    
    return log


def format_quest_info(quest: Quest) -> str:
    """Formate les informations d'une quete."""
    lines = [
        f"=== {quest.title.upper()} ===",
        f"Type: {quest.quest_type.value.capitalize()}",
        f"Statut: {quest.status.value.capitalize()}",
    ]
    
    if quest.time_limit > 0:
        remaining = quest.time_limit - quest.scenes_elapsed
        lines.append(f"Temps restant: {remaining} scenes")
    
    lines.append("")
    lines.append(quest.description)
    lines.append("")
    lines.append("Objectifs:")
    
    for obj in quest.objectives:
        if obj.hidden and not obj.completed:
            continue
        status = obj.progress_text()
        optional = " (optionnel)" if obj.optional else ""
        lines.append(f"  {status} {obj.description}{optional}")
    
    if quest.reward.xp > 0:
        lines.append("")
        lines.append(f"Recompense: {quest.reward.xp} XP")
        if quest.reward.credits > 0:
            lines.append(f"           {quest.reward.credits} credits")
        if quest.reward.items:
            lines.append(f"           Objets: {', '.join(quest.reward.items)}")
    
    if quest.journal_entries:
        lines.append("")
        lines.append("Journal:")
        for entry in quest.journal_entries[-3:]:  # 3 dernieres entrees
            lines.append(f"  - {entry}")
    
    return "\n".join(lines)


def format_quest_log(log: QuestLog) -> str:
    """Formate le journal de quetes complet."""
    lines = ["=== JOURNAL DE QUETES ===", ""]
    
    active = log.get_active_quests()
    if active:
        lines.append("QUETES ACTIVES:")
        for quest in active:
            progress = f"{quest.progress_percentage():.0f}%"
            time_info = ""
            if quest.time_limit > 0:
                remaining = quest.time_limit - quest.scenes_elapsed
                time_info = f" [!{remaining} scenes]"
            lines.append(f"  [{progress}] {quest.title}{time_info}")
        lines.append("")
    
    available = log.get_available_quests()
    if available:
        lines.append("QUETES DISPONIBLES:")
        for quest in available:
            lines.append(f"  [ ] {quest.title}")
        lines.append("")
    
    if log.completed_quest_ids:
        lines.append(f"QUETES TERMINEES: {len(log.completed_quest_ids)}")
    
    if log.failed_quest_ids:
        lines.append(f"QUETES ECHOUEES: {len(log.failed_quest_ids)}")
    
    return "\n".join(lines)
