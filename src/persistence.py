"""
Systeme de monde persistant - Etat global, memoire, coherence
Survivant de Ruche - Warhammer 40K Solo RPG
"""
from dataclasses import dataclass, field
from typing import Optional, Any
from datetime import datetime
from pathlib import Path
import json
import yaml


@dataclass
class WorldEvent:
    """Un evenement qui a eu lieu dans le monde."""
    id: str
    scene: int
    timestamp: str
    category: str  # combat, exploration, dialogue, choix, monde
    description: str
    consequences: list[str] = field(default_factory=list)
    related_npcs: list[str] = field(default_factory=list)
    related_zones: list[str] = field(default_factory=list)
    importance: int = 1  # 1-5, pour filtrer lors du resume


@dataclass
class GlobalState:
    """Etat global du monde."""
    # Progression de l'invasion
    invasion_level: int = 1  # 1-10, augmente avec le temps
    tyranid_presence: dict[str, int] = field(default_factory=dict)  # zone_id -> niveau
    
    # Temps ecoule
    current_day: int = 1
    current_scene: int = 1
    total_scenes: int = 0
    
    # Ressources globales
    survivor_count: int = 100  # Nombre de survivants dans le secteur
    food_scarcity: int = 1     # 1-5, affecte les prix
    
    # Drapeaux de progression
    flags: dict[str, Any] = field(default_factory=dict)
    
    # Morts significatives
    dead_npcs: list[str] = field(default_factory=list)
    
    # Zones detruites ou transformees
    destroyed_zones: list[str] = field(default_factory=list)
    secured_zones: list[str] = field(default_factory=list)


@dataclass
class MemoryEntry:
    """Une entree dans la memoire longue."""
    scene: int
    summary: str
    tags: list[str] = field(default_factory=list)
    importance: int = 1


@dataclass 
class WorldMemory:
    """Memoire longue du monde pour le contexte IA."""
    
    # Evenements importants
    events: list[WorldEvent] = field(default_factory=list)
    
    # Resumes par chapitre/arc
    chapter_summaries: list[str] = field(default_factory=list)
    
    # Memoire compacte pour le prompt
    compact_memory: list[MemoryEntry] = field(default_factory=list)
    
    # Decisions majeures du joueur
    major_decisions: list[str] = field(default_factory=list)
    
    # Promesses et menaces
    pending_threads: list[str] = field(default_factory=list)  # Fils narratifs en suspens
    
    def add_event(self, event: WorldEvent) -> None:
        """Ajoute un evenement a l'historique."""
        self.events.append(event)
        
        # Ajouter a la memoire compacte si important
        if event.importance >= 3:
            self.compact_memory.append(MemoryEntry(
                scene=event.scene,
                summary=event.description,
                tags=[event.category] + event.related_npcs,
                importance=event.importance,
            ))
    
    def add_decision(self, decision: str) -> None:
        """Enregistre une decision majeure."""
        self.major_decisions.append(decision)
    
    def get_recent_events(self, count: int = 10) -> list[WorldEvent]:
        """Retourne les evenements recents."""
        return self.events[-count:]
    
    def get_important_events(self, min_importance: int = 3) -> list[WorldEvent]:
        """Retourne les evenements importants."""
        return [e for e in self.events if e.importance >= min_importance]
    
    def generate_context_summary(self, max_entries: int = 20) -> str:
        """Genere un resume pour le contexte IA."""
        lines = ["=== MEMOIRE DU MONDE ===", ""]
        
        # Decisions majeures
        if self.major_decisions:
            lines.append("DECISIONS MAJEURES:")
            for decision in self.major_decisions[-5:]:
                lines.append(f"  - {decision}")
            lines.append("")
        
        # Evenements recents importants
        important = self.get_important_events()[-max_entries:]
        if important:
            lines.append("EVENEMENTS MARQUANTS:")
            for event in important:
                lines.append(f"  [Scene {event.scene}] {event.description}")
            lines.append("")
        
        # Fils narratifs
        if self.pending_threads:
            lines.append("FILS NARRATIFS EN COURS:")
            for thread in self.pending_threads:
                lines.append(f"  - {thread}")
        
        return "\n".join(lines)


@dataclass
class GameWorld:
    """Le monde de jeu complet avec persistance."""
    
    # Etat global
    global_state: GlobalState = field(default_factory=GlobalState)
    
    # Memoire
    memory: WorldMemory = field(default_factory=WorldMemory)
    
    # Sous-systemes (references, charges separement)
    world_map: Any = None
    quest_log: Any = None
    relationships: Any = None
    progression: Any = None
    inventory: Any = None
    character: Any = None
    
    # Metadonnees
    campaign_name: str = "campagne1"
    created_at: str = ""
    last_played: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def advance_scene(self) -> list[str]:
        """Avance a la scene suivante et retourne les evenements."""
        messages = []
        self.global_state.current_scene += 1
        self.global_state.total_scenes += 1
        
        # Verifier changement de jour (toutes les 10 scenes)
        if self.global_state.current_scene % 10 == 0:
            self.global_state.current_day += 1
            messages.append(f"=== JOUR {self.global_state.current_day} ===")
            
            # Progression de l'invasion
            self._advance_invasion()
            messages.append(f"Niveau d'invasion: {self.global_state.invasion_level}/10")
        
        # Mise a jour des ressources
        if self.global_state.current_scene % 5 == 0:
            self._update_scarcity()
        
        return messages
    
    def _advance_invasion(self) -> None:
        """Fait progresser l'invasion tyranide."""
        # L'invasion progresse lentement
        if self.global_state.current_day % 3 == 0:
            self.global_state.invasion_level = min(10, self.global_state.invasion_level + 1)
            self.global_state.survivor_count = max(0, self.global_state.survivor_count - 10)
    
    def _update_scarcity(self) -> None:
        """Met a jour la rarete des ressources."""
        # La rarete augmente avec le temps et l'invasion
        base_scarcity = 1 + (self.global_state.current_day // 5)
        invasion_modifier = self.global_state.invasion_level // 3
        self.global_state.food_scarcity = min(5, base_scarcity + invasion_modifier)
    
    def record_event(
        self,
        category: str,
        description: str,
        importance: int = 1,
        consequences: list[str] = None,
        npcs: list[str] = None,
        zones: list[str] = None,
    ) -> None:
        """Enregistre un evenement dans le monde."""
        event = WorldEvent(
            id=f"evt_{self.global_state.total_scenes}_{len(self.memory.events)}",
            scene=self.global_state.current_scene,
            timestamp=datetime.now().isoformat(),
            category=category,
            description=description,
            consequences=consequences or [],
            related_npcs=npcs or [],
            related_zones=zones or [],
            importance=importance,
        )
        self.memory.add_event(event)
    
    def set_flag(self, flag_name: str, value: Any = True) -> None:
        """Definit un drapeau de progression."""
        self.global_state.flags[flag_name] = value
    
    def get_flag(self, flag_name: str, default: Any = None) -> Any:
        """Recupere un drapeau."""
        return self.global_state.flags.get(flag_name, default)
    
    def check_flag(self, flag_name: str) -> bool:
        """Verifie si un drapeau est vrai."""
        return bool(self.global_state.flags.get(flag_name, False))
    
    def to_dict(self) -> dict:
        """Serialise le monde."""
        return {
            "campaign_name": self.campaign_name,
            "created_at": self.created_at,
            "last_played": datetime.now().isoformat(),
            "global_state": {
                "invasion_level": self.global_state.invasion_level,
                "tyranid_presence": self.global_state.tyranid_presence.copy(),
                "current_day": self.global_state.current_day,
                "current_scene": self.global_state.current_scene,
                "total_scenes": self.global_state.total_scenes,
                "survivor_count": self.global_state.survivor_count,
                "food_scarcity": self.global_state.food_scarcity,
                "flags": self.global_state.flags.copy(),
                "dead_npcs": self.global_state.dead_npcs.copy(),
                "destroyed_zones": self.global_state.destroyed_zones.copy(),
                "secured_zones": self.global_state.secured_zones.copy(),
            },
            "memory": {
                "events": [
                    {
                        "id": e.id,
                        "scene": e.scene,
                        "timestamp": e.timestamp,
                        "category": e.category,
                        "description": e.description,
                        "consequences": e.consequences,
                        "related_npcs": e.related_npcs,
                        "related_zones": e.related_zones,
                        "importance": e.importance,
                    }
                    for e in self.memory.events
                ],
                "chapter_summaries": self.memory.chapter_summaries.copy(),
                "compact_memory": [
                    {
                        "scene": m.scene,
                        "summary": m.summary,
                        "tags": m.tags,
                        "importance": m.importance,
                    }
                    for m in self.memory.compact_memory
                ],
                "major_decisions": self.memory.major_decisions.copy(),
                "pending_threads": self.memory.pending_threads.copy(),
            },
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "GameWorld":
        """Charge le monde depuis un dict."""
        world = cls(
            campaign_name=data.get("campaign_name", "campagne1"),
            created_at=data.get("created_at", ""),
            last_played=data.get("last_played", ""),
        )
        
        # Global state
        gs_data = data.get("global_state", {})
        world.global_state = GlobalState(
            invasion_level=gs_data.get("invasion_level", 1),
            tyranid_presence=gs_data.get("tyranid_presence", {}).copy(),
            current_day=gs_data.get("current_day", 1),
            current_scene=gs_data.get("current_scene", 1),
            total_scenes=gs_data.get("total_scenes", 0),
            survivor_count=gs_data.get("survivor_count", 100),
            food_scarcity=gs_data.get("food_scarcity", 1),
            flags=gs_data.get("flags", {}).copy(),
            dead_npcs=gs_data.get("dead_npcs", []).copy(),
            destroyed_zones=gs_data.get("destroyed_zones", []).copy(),
            secured_zones=gs_data.get("secured_zones", []).copy(),
        )
        
        # Memory
        mem_data = data.get("memory", {})
        world.memory = WorldMemory(
            chapter_summaries=mem_data.get("chapter_summaries", []).copy(),
            major_decisions=mem_data.get("major_decisions", []).copy(),
            pending_threads=mem_data.get("pending_threads", []).copy(),
        )
        
        for e_data in mem_data.get("events", []):
            world.memory.events.append(WorldEvent(
                id=e_data["id"],
                scene=e_data["scene"],
                timestamp=e_data["timestamp"],
                category=e_data["category"],
                description=e_data["description"],
                consequences=e_data.get("consequences", []),
                related_npcs=e_data.get("related_npcs", []),
                related_zones=e_data.get("related_zones", []),
                importance=e_data.get("importance", 1),
            ))
        
        for m_data in mem_data.get("compact_memory", []):
            world.memory.compact_memory.append(MemoryEntry(
                scene=m_data["scene"],
                summary=m_data["summary"],
                tags=m_data.get("tags", []),
                importance=m_data.get("importance", 1),
            ))
        
        return world
    
    def save(self, directory: Path) -> None:
        """Sauvegarde le monde dans un repertoire."""
        directory.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder l'etat principal
        world_file = directory / "world_state.yaml"
        with open(world_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(self.to_dict(), f, allow_unicode=True, default_flow_style=False)
    
    @classmethod
    def load(cls, directory: Path) -> Optional["GameWorld"]:
        """Charge le monde depuis un repertoire."""
        world_file = directory / "world_state.yaml"
        if not world_file.exists():
            return None
        
        with open(world_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        return cls.from_dict(data)


def create_new_game_world(campaign_name: str = "campagne1") -> GameWorld:
    """Cree un nouveau monde de jeu."""
    world = GameWorld(campaign_name=campaign_name)
    
    # Etat initial
    world.global_state.invasion_level = 1
    world.global_state.survivor_count = 150
    
    # Memoire initiale
    world.memory.pending_threads = [
        "L'invasion tyranide vient de commencer - la ruche est en chaos",
        "Le signal vox capte par Karimus semble important",
        "Des rumeurs parlent d'une resistance organisee au Temple",
    ]
    
    world.record_event(
        category="monde",
        description="L'invasion de la Flotte-Ruche commence. Karimus se reveille dans le chaos.",
        importance=5,
    )
    
    return world


def format_world_status(world: GameWorld) -> str:
    """Formate le statut du monde pour affichage."""
    gs = world.global_state
    
    invasion_bar = "=" * gs.invasion_level + "-" * (10 - gs.invasion_level)
    
    lines = [
        "=== ETAT DU MONDE ===",
        "",
        f"Jour: {gs.current_day}",
        f"Scene: {gs.current_scene}",
        "",
        f"Niveau d'invasion: [{invasion_bar}] {gs.invasion_level}/10",
        f"Survivants estimes: ~{gs.survivor_count}",
        f"Rarete des ressources: {'*' * gs.food_scarcity}",
        "",
    ]
    
    if gs.dead_npcs:
        lines.append(f"PNJs morts: {len(gs.dead_npcs)}")
    
    if gs.destroyed_zones:
        lines.append(f"Zones detruites: {len(gs.destroyed_zones)}")
    
    if gs.secured_zones:
        lines.append(f"Zones securisees: {len(gs.secured_zones)}")
    
    return "\n".join(lines)


def generate_gm_context(world: GameWorld) -> str:
    """Genere le contexte complet pour le MJ IA."""
    lines = [
        "=== CONTEXTE MONDE ===",
        "",
        f"Jour {world.global_state.current_day}, Scene {world.global_state.current_scene}",
        f"Invasion: Niveau {world.global_state.invasion_level}/10",
        f"Survivants: ~{world.global_state.survivor_count}",
        "",
    ]
    
    # Drapeaux actifs
    if world.global_state.flags:
        lines.append("Drapeaux actifs:")
        for flag, value in world.global_state.flags.items():
            if value:
                lines.append(f"  - {flag}")
        lines.append("")
    
    # Memoire
    lines.append(world.memory.generate_context_summary())
    
    return "\n".join(lines)
