"""
Systeme de reputation et relations - Factions, PNJ, consequences
Survivant de Ruche - Warhammer 40K Solo RPG
"""
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class FactionType(Enum):
    """Types de factions."""
    IMPERIAL = "imperial"
    CIVIL = "civil"
    CRIMINEL = "criminel"
    RELIGIEUX = "religieux"
    MILITAIRE = "militaire"
    HOSTILE = "hostile"


class ReputationLevel(Enum):
    """Niveaux de reputation."""
    ENNEMI = -3      # Attaque a vue
    HOSTILE = -2     # Mefiant, peut attaquer
    MEFIANT = -1     # Echanges limites
    NEUTRE = 0       # Indifferent
    AMICAL = 1       # Cooperatif
    ALLIE = 2        # Aide active
    DEVOUE = 3       # Loyaute totale
    
    @classmethod
    def from_value(cls, value: int) -> "ReputationLevel":
        """Convertit une valeur en niveau."""
        if value <= -50:
            return cls.ENNEMI
        elif value <= -25:
            return cls.HOSTILE
        elif value <= -10:
            return cls.MEFIANT
        elif value <= 10:
            return cls.NEUTRE
        elif value <= 25:
            return cls.AMICAL
        elif value <= 50:
            return cls.ALLIE
        else:
            return cls.DEVOUE


class NPCDisposition(Enum):
    """Disposition d'un PNJ."""
    HOSTILE = "hostile"
    MEFIANT = "mefiant"
    NEUTRE = "neutre"
    AMICAL = "amical"
    LOYAL = "loyal"
    MORT = "mort"


@dataclass
class Faction:
    """Une faction avec laquelle le joueur peut interagir."""
    id: str
    name: str
    description: str
    faction_type: FactionType
    
    # Reputation du joueur (de -100 a +100)
    reputation: int = 0
    
    # Relations avec autres factions
    allies: list[str] = field(default_factory=list)
    enemies: list[str] = field(default_factory=list)
    
    # Bonus/malus accordes
    trade_modifier: int = 0      # % sur les prix
    info_access: bool = False    # Acces aux infos
    safe_passage: bool = False   # Passage sur
    
    # PNJs membres
    members: list[str] = field(default_factory=list)
    
    def get_level(self) -> ReputationLevel:
        """Retourne le niveau de reputation."""
        return ReputationLevel.from_value(self.reputation)
    
    def modify_reputation(self, amount: int) -> tuple[int, Optional[str]]:
        """
        Modifie la reputation et retourne (nouvelle_valeur, message_si_changement_niveau).
        """
        old_level = self.get_level()
        self.reputation = max(-100, min(100, self.reputation + amount))
        new_level = self.get_level()
        
        message = None
        if old_level != new_level:
            if amount > 0:
                message = f"Reputation amelioree avec {self.name}: {new_level.name}"
            else:
                message = f"Reputation degradee avec {self.name}: {new_level.name}"
            
            # Mettre a jour les bonus
            self._update_bonuses()
        
        return self.reputation, message
    
    def _update_bonuses(self) -> None:
        """Met a jour les bonus bases sur la reputation."""
        level = self.get_level()
        
        if level.value >= 1:  # Amical+
            self.info_access = True
            self.trade_modifier = level.value * 5  # Reduction des prix
        elif level.value <= -1:  # Mefiant-
            self.info_access = False
            self.trade_modifier = level.value * 10  # Augmentation des prix
        else:
            self.info_access = False
            self.trade_modifier = 0
        
        self.safe_passage = level.value >= 2  # Allie+
    
    def to_dict(self) -> dict:
        """Serialise la faction."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "faction_type": self.faction_type.value,
            "reputation": self.reputation,
            "allies": self.allies.copy(),
            "enemies": self.enemies.copy(),
            "trade_modifier": self.trade_modifier,
            "info_access": self.info_access,
            "safe_passage": self.safe_passage,
            "members": self.members.copy(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Faction":
        """Charge une faction depuis un dict."""
        faction = cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            faction_type=FactionType(data["faction_type"]),
            reputation=data.get("reputation", 0),
        )
        faction.allies = data.get("allies", []).copy()
        faction.enemies = data.get("enemies", []).copy()
        faction.trade_modifier = data.get("trade_modifier", 0)
        faction.info_access = data.get("info_access", False)
        faction.safe_passage = data.get("safe_passage", False)
        faction.members = data.get("members", []).copy()
        return faction


@dataclass
class NPC:
    """Un personnage non-joueur."""
    id: str
    name: str
    description: str
    faction_id: Optional[str] = None
    
    # Disposition envers le joueur
    disposition: NPCDisposition = NPCDisposition.NEUTRE
    relationship_score: int = 0  # -100 a +100
    
    # Caracteristiques
    role: str = ""  # Marchand, garde, refugie, etc.
    zone_id: Optional[str] = None
    
    # Etat
    alive: bool = True
    met: bool = False
    trust_level: int = 0  # Niveau de confiance
    
    # Memoire des interactions
    interactions: list[str] = field(default_factory=list)
    favors_owed: int = 0  # Faveurs que le PNJ nous doit
    favors_given: int = 0  # Faveurs qu'on lui doit
    
    # Quetes liees
    quest_giver: list[str] = field(default_factory=list)
    
    # Dialogue et personnalite
    personality_traits: list[str] = field(default_factory=list)
    known_info: list[str] = field(default_factory=list)
    
    def modify_relationship(self, amount: int) -> tuple[int, Optional[str]]:
        """Modifie la relation avec ce PNJ."""
        old_disposition = self.disposition
        self.relationship_score = max(-100, min(100, self.relationship_score + amount))
        
        # Mise a jour de la disposition
        if self.relationship_score <= -50:
            self.disposition = NPCDisposition.HOSTILE
        elif self.relationship_score <= -20:
            self.disposition = NPCDisposition.MEFIANT
        elif self.relationship_score <= 20:
            self.disposition = NPCDisposition.NEUTRE
        elif self.relationship_score <= 50:
            self.disposition = NPCDisposition.AMICAL
        else:
            self.disposition = NPCDisposition.LOYAL
        
        message = None
        if old_disposition != self.disposition:
            message = f"{self.name} est maintenant {self.disposition.value} envers vous."
        
        return self.relationship_score, message
    
    def add_interaction(self, description: str) -> None:
        """Enregistre une interaction."""
        self.interactions.append(description)
        if not self.met:
            self.met = True
    
    def add_favor_owed(self) -> None:
        """Le PNJ nous doit une faveur."""
        self.favors_owed += 1
        self.trust_level += 1
    
    def use_favor(self) -> bool:
        """Utilise une faveur que le PNJ nous doit."""
        if self.favors_owed > 0:
            self.favors_owed -= 1
            return True
        return False
    
    def to_dict(self) -> dict:
        """Serialise le PNJ."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "faction_id": self.faction_id,
            "disposition": self.disposition.value,
            "relationship_score": self.relationship_score,
            "role": self.role,
            "zone_id": self.zone_id,
            "alive": self.alive,
            "met": self.met,
            "trust_level": self.trust_level,
            "interactions": self.interactions.copy(),
            "favors_owed": self.favors_owed,
            "favors_given": self.favors_given,
            "quest_giver": self.quest_giver.copy(),
            "personality_traits": self.personality_traits.copy(),
            "known_info": self.known_info.copy(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "NPC":
        """Charge un PNJ depuis un dict."""
        npc = cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            faction_id=data.get("faction_id"),
            disposition=NPCDisposition(data.get("disposition", "neutre")),
            relationship_score=data.get("relationship_score", 0),
            role=data.get("role", ""),
            zone_id=data.get("zone_id"),
            alive=data.get("alive", True),
            met=data.get("met", False),
            trust_level=data.get("trust_level", 0),
            favors_owed=data.get("favors_owed", 0),
            favors_given=data.get("favors_given", 0),
        )
        npc.interactions = data.get("interactions", []).copy()
        npc.quest_giver = data.get("quest_giver", []).copy()
        npc.personality_traits = data.get("personality_traits", []).copy()
        npc.known_info = data.get("known_info", []).copy()
        return npc


@dataclass
class RelationshipManager:
    """Gestionnaire des relations du joueur."""
    factions: dict[str, Faction] = field(default_factory=dict)
    npcs: dict[str, NPC] = field(default_factory=dict)
    
    def add_faction(self, faction: Faction) -> None:
        """Ajoute une faction."""
        self.factions[faction.id] = faction
    
    def add_npc(self, npc: NPC) -> None:
        """Ajoute un PNJ."""
        self.npcs[npc.id] = npc
    
    def get_faction(self, faction_id: str) -> Optional[Faction]:
        """Recupere une faction."""
        return self.factions.get(faction_id)
    
    def get_npc(self, npc_id: str) -> Optional[NPC]:
        """Recupere un PNJ."""
        return self.npcs.get(npc_id)
    
    def modify_faction_reputation(self, faction_id: str, amount: int) -> list[str]:
        """
        Modifie la reputation avec une faction.
        Propage les effets aux factions alliees/ennemies.
        """
        messages = []
        faction = self.factions.get(faction_id)
        if not faction:
            return messages
        
        _, msg = faction.modify_reputation(amount)
        if msg:
            messages.append(msg)
        
        # Propagation aux allies (50% de l'effet)
        for ally_id in faction.allies:
            ally = self.factions.get(ally_id)
            if ally:
                _, ally_msg = ally.modify_reputation(amount // 2)
                if ally_msg:
                    messages.append(ally_msg)
        
        # Propagation aux ennemis (effet inverse, 50%)
        for enemy_id in faction.enemies:
            enemy = self.factions.get(enemy_id)
            if enemy:
                _, enemy_msg = enemy.modify_reputation(-amount // 2)
                if enemy_msg:
                    messages.append(enemy_msg)
        
        return messages
    
    def modify_npc_relationship(self, npc_id: str, amount: int) -> list[str]:
        """Modifie la relation avec un PNJ."""
        messages = []
        npc = self.npcs.get(npc_id)
        if not npc:
            return messages
        
        _, msg = npc.modify_relationship(amount)
        if msg:
            messages.append(msg)
        
        # Petit effet sur la faction
        if npc.faction_id:
            faction = self.factions.get(npc.faction_id)
            if faction:
                _, faction_msg = faction.modify_reputation(amount // 4)
                if faction_msg:
                    messages.append(faction_msg)
        
        return messages
    
    def kill_npc(self, npc_id: str) -> list[str]:
        """Tue un PNJ et gere les consequences."""
        messages = []
        npc = self.npcs.get(npc_id)
        if not npc or not npc.alive:
            return messages
        
        npc.alive = False
        npc.disposition = NPCDisposition.MORT
        messages.append(f"{npc.name} est mort.")
        
        # Consequences sur la faction
        if npc.faction_id:
            faction_msgs = self.modify_faction_reputation(npc.faction_id, -25)
            messages.extend(faction_msgs)
        
        return messages
    
    def get_npcs_in_zone(self, zone_id: str) -> list[NPC]:
        """Retourne les PNJs vivants dans une zone."""
        return [
            npc for npc in self.npcs.values()
            if npc.zone_id == zone_id and npc.alive
        ]
    
    def get_met_npcs(self) -> list[NPC]:
        """Retourne les PNJs deja rencontres."""
        return [npc for npc in self.npcs.values() if npc.met and npc.alive]
    
    def to_dict(self) -> dict:
        """Serialise le gestionnaire."""
        return {
            "factions": {fid: f.to_dict() for fid, f in self.factions.items()},
            "npcs": {nid: n.to_dict() for nid, n in self.npcs.items()},
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "RelationshipManager":
        """Charge depuis un dict."""
        manager = cls()
        for faction_data in data.get("factions", {}).values():
            faction = Faction.from_dict(faction_data)
            manager.factions[faction.id] = faction
        for npc_data in data.get("npcs", {}).values():
            npc = NPC.from_dict(npc_data)
            manager.npcs[npc.id] = npc
        return manager


# =============================================================================
# FACTIONS ET PNJ DE DEPART
# =============================================================================

def create_starting_relationships() -> RelationshipManager:
    """Cree les factions et PNJs de depart."""
    manager = RelationshipManager()
    
    # --- FACTIONS ---
    
    manager.add_faction(Faction(
        id="civils",
        name="Survivants Civils",
        description="Les habitants ordinaires de la ruche, luttant pour leur survie.",
        faction_type=FactionType.CIVIL,
        reputation=10,  # Karimus est l'un d'eux
        allies=["ecclesiarchie", "pdf"],
        enemies=["culte"],
    ))
    
    manager.add_faction(Faction(
        id="pdf",
        name="Forces de Defense Planetaire",
        description="Les restes desorganises de l'armee locale. Debordees mais resistantes.",
        faction_type=FactionType.MILITAIRE,
        reputation=0,
        allies=["civils", "ecclesiarchie"],
        enemies=["culte", "criminels"],
    ))
    
    manager.add_faction(Faction(
        id="ecclesiarchie",
        name="Ecclesiarchie Locale",
        description="Les pretres et fideles du Culte Imperial. Un phare de foi dans les tenebres.",
        faction_type=FactionType.RELIGIEUX,
        reputation=0,
        allies=["civils", "pdf"],
        enemies=["culte"],
    ))
    
    manager.add_faction(Faction(
        id="marchands",
        name="Reseau des Marchands",
        description="Commercants et contrebandiers. Ils profitent du chaos pour faire fortune.",
        faction_type=FactionType.CRIMINEL,
        reputation=0,
        allies=[],
        enemies=[],
    ))
    
    manager.add_faction(Faction(
        id="culte",
        name="Culte Genestealer",
        description="Les adorateurs des Grands Devoreurs. Traites et monstres.",
        faction_type=FactionType.HOSTILE,
        reputation=-50,
        allies=[],
        enemies=["civils", "pdf", "ecclesiarchie"],
    ))
    
    manager.add_faction(Faction(
        id="criminels",
        name="Gangs de la Ruche",
        description="Pillards et gangers profitant de l'anarchie.",
        faction_type=FactionType.CRIMINEL,
        reputation=-10,
        allies=["marchands"],
        enemies=["pdf"],
    ))
    
    # --- PNJs ---
    
    manager.add_npc(NPC(
        id="pere_mordecai",
        name="Pere Mordecai",
        description="Un vieux pretre au regard dur mais au coeur compatissant. "
                    "Il dirige le temple et organise la resistance spirituelle.",
        faction_id="ecclesiarchie",
        role="Pretre",
        zone_id="temple_empereur",
        disposition=NPCDisposition.AMICAL,
        relationship_score=15,
        personality_traits=["pieux", "pragmatique", "protecteur"],
        known_info=["passages_secrets", "histoire_temple", "resistance"],
        quest_giver=["secret_temple"],
    ))
    
    manager.add_npc(NPC(
        id="soeur_helene",
        name="Soeur Helene",
        description="Une jeune soeur de l'ordre hospitalier. Elle soigne les blesses "
                    "et les malades avec un devouement sans faille.",
        faction_id="ecclesiarchie",
        role="Hospitaliere",
        zone_id="temple_empereur",
        disposition=NPCDisposition.NEUTRE,
        personality_traits=["bienveillante", "courageuse", "naive"],
        known_info=["medecine", "rumeurs_blesses"],
    ))
    
    manager.add_npc(NPC(
        id="grox",
        name="Grox",
        description="Un ancien garde reconverti en marchand d'armes. Bourru mais fiable... "
                    "tant qu'on paie.",
        faction_id="marchands",
        role="Marchand d'armes",
        zone_id="marche_noir",
        disposition=NPCDisposition.MEFIANT,
        relationship_score=-5,
        personality_traits=["cupide", "pragmatique", "veteran"],
        known_info=["armes", "rumeurs_marche", "mouvements_pdf"],
        quest_giver=["commerce_noir"],
    ))
    
    manager.add_npc(NPC(
        id="doc_felix",
        name="Doc Felix",
        description="Un medic deserteur de la PDF. Il soigne sans poser de questions, "
                    "mais ses tarifs sont eleves.",
        faction_id="marchands",
        role="Medecin clandestin",
        zone_id="marche_noir",
        disposition=NPCDisposition.NEUTRE,
        personality_traits=["cynique", "competent", "secret"],
        known_info=["medecine", "pdf_deserteurs"],
    ))
    
    manager.add_npc(NPC(
        id="caporal_vex",
        name="Caporal Vex",
        description="Un soldat PDF blesse, abandonne lors d'une retraite chaotique. "
                    "Il cherche a rejoindre ses camarades.",
        faction_id="pdf",
        role="Soldat blesse",
        zone_id="checkpoint_pdf",
        disposition=NPCDisposition.MEFIANT,
        personality_traits=["meurtri", "loyal", "mefiant"],
        known_info=["positions_pdf", "mouvements_tyranides", "codes_militaires"],
    ))
    
    manager.add_npc(NPC(
        id="mira",
        name="Mira",
        description="Une enfant d'une dizaine d'annees, seule survivante de sa famille. "
                    "Elle se cache dans les conduits de ventilation.",
        faction_id="civils",
        role="Refugiee",
        zone_id="bloc_voisin",
        disposition=NPCDisposition.MEFIANT,
        relationship_score=-10,
        personality_traits=["effrayee", "debrouilarde", "silencieuse"],
        known_info=["passages_secrets", "cachettes"],
    ))
    
    manager.add_npc(NPC(
        id="kontrar",
        name="Kontrar le Balafre",
        description="Chef d'un petit gang de pillards. Brutal mais pas stupide.",
        faction_id="criminels",
        role="Chef de gang",
        zone_id="corridor_principal",
        disposition=NPCDisposition.HOSTILE,
        relationship_score=-30,
        personality_traits=["violent", "ambitieux", "territorial"],
        known_info=["territoire_gang", "caches_pillards"],
    ))
    
    return manager


def format_faction_info(faction: Faction) -> str:
    """Formate les informations d'une faction."""
    level = faction.get_level()
    bar = "=" * (5 + level.value) + "-" * (5 - level.value)
    
    lines = [
        f"=== {faction.name.upper()} ===",
        f"Type: {faction.faction_type.value.capitalize()}",
        f"Reputation: [{bar}] {level.name} ({faction.reputation})",
        "",
        faction.description,
        "",
    ]
    
    if faction.trade_modifier != 0:
        sign = "+" if faction.trade_modifier > 0 else ""
        lines.append(f"Prix: {sign}{faction.trade_modifier}%")
    
    if faction.info_access:
        lines.append("Acces aux informations: Oui")
    
    if faction.safe_passage:
        lines.append("Passage securise: Oui")
    
    return "\n".join(lines)


def format_npc_info(npc: NPC) -> str:
    """Formate les informations d'un PNJ."""
    status = "MORT" if not npc.alive else npc.disposition.value.upper()
    
    lines = [
        f"=== {npc.name.upper()} ===",
        f"Role: {npc.role}",
        f"Statut: {status}",
        f"Relation: {npc.relationship_score}",
        "",
        npc.description,
    ]
    
    if npc.favors_owed > 0:
        lines.append(f"\nVous doit {npc.favors_owed} faveur(s)")
    
    if npc.trust_level > 0:
        lines.append(f"Confiance: {npc.trust_level}")
    
    if npc.interactions:
        lines.append("\nDernieres interactions:")
        for inter in npc.interactions[-3:]:
            lines.append(f"  - {inter}")
    
    return "\n".join(lines)


def format_relationships_overview(manager: RelationshipManager) -> str:
    """Formate une vue d'ensemble des relations."""
    lines = ["=== RELATIONS ===", ""]
    
    lines.append("FACTIONS:")
    for faction in manager.factions.values():
        level = faction.get_level()
        indicator = {
            ReputationLevel.ENNEMI: "XXX",
            ReputationLevel.HOSTILE: "XX-",
            ReputationLevel.MEFIANT: "X--",
            ReputationLevel.NEUTRE: "---",
            ReputationLevel.AMICAL: "-++",
            ReputationLevel.ALLIE: "++>",
            ReputationLevel.DEVOUE: "<3>",
        }.get(level, "???")
        lines.append(f"  [{indicator}] {faction.name} ({level.name})")
    
    lines.append("")
    lines.append("PNJ RENCONTRES:")
    met_npcs = manager.get_met_npcs()
    if met_npcs:
        for npc in met_npcs:
            disp = npc.disposition.value[:3].upper()
            lines.append(f"  [{disp}] {npc.name} - {npc.role}")
    else:
        lines.append("  (Aucun)")
    
    return "\n".join(lines)
