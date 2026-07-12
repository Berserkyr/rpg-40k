"""
Systeme de carte et exploration - Zones, deplacements, evenements
Survivant de Ruche - Warhammer 40K Solo RPG
"""
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import random


class ZoneType(Enum):
    """Types de zones dans la ruche."""
    HABITATION = "habitation"
    INDUSTRIEL = "industriel"
    COMMERCIAL = "commercial"
    ADMINISTRATIF = "administratif"
    RELIGIEUX = "religieux"
    SOUTERRAIN = "souterrain"
    RUINE = "ruine"
    EXTERIEUR = "exterieur"


class ThreatLevel(Enum):
    """Niveau de danger d'une zone."""
    SECURISE = 1       # Patrouilles, refuges
    INCERTAIN = 2      # Quelques dangers
    DANGEREUX = 3      # Ennemis frequents
    HOSTILE = 4        # Zone de guerre active
    MORT = 5           # Infestation totale


class ZoneStatus(Enum):
    """Etat actuel d'une zone."""
    INCONNU = "inconnu"
    EXPLORE = "explore"
    SECURISE = "securise"
    INFESTE = "infeste"
    DETRUIT = "detruit"
    BLOQUE = "bloque"


@dataclass
class PointOfInterest:
    """Un point d'interet dans une zone."""
    id: str
    name: str
    description: str
    discovered: bool = False
    visited: bool = False
    loot_available: bool = True
    quest_related: bool = False
    special_event: Optional[str] = None


@dataclass
class Zone:
    """Une zone explorable de la ruche."""
    id: str
    name: str
    description: str
    zone_type: ZoneType
    threat_level: ThreatLevel
    status: ZoneStatus = ZoneStatus.INCONNU
    
    # Connexions vers d'autres zones
    connections: list[str] = field(default_factory=list)
    
    # Points d'interet
    points_of_interest: list[PointOfInterest] = field(default_factory=list)
    
    # Ressources disponibles
    resources: dict[str, int] = field(default_factory=dict)
    
    # Modificateurs
    visibility_modifier: int = 0  # Bonus/malus aux jets de discretion
    survival_modifier: int = 0    # Bonus/malus aux jets de survie
    
    # Evenements potentiels
    possible_events: list[str] = field(default_factory=list)
    
    # NPCs presents
    npcs: list[str] = field(default_factory=list)
    
    # Historique des visites
    times_visited: int = 0
    last_visited_scene: int = 0
    
    def to_dict(self) -> dict:
        """Serialise la zone."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "zone_type": self.zone_type.value,
            "threat_level": self.threat_level.value,
            "status": self.status.value,
            "connections": self.connections.copy(),
            "points_of_interest": [
                {
                    "id": poi.id,
                    "name": poi.name,
                    "description": poi.description,
                    "discovered": poi.discovered,
                    "visited": poi.visited,
                    "loot_available": poi.loot_available,
                    "quest_related": poi.quest_related,
                    "special_event": poi.special_event,
                }
                for poi in self.points_of_interest
            ],
            "resources": self.resources.copy(),
            "visibility_modifier": self.visibility_modifier,
            "survival_modifier": self.survival_modifier,
            "possible_events": self.possible_events.copy(),
            "npcs": self.npcs.copy(),
            "times_visited": self.times_visited,
            "last_visited_scene": self.last_visited_scene,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Zone":
        """Charge une zone depuis un dict."""
        zone = cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            zone_type=ZoneType(data["zone_type"]),
            threat_level=ThreatLevel(data["threat_level"]),
            status=ZoneStatus(data.get("status", "inconnu")),
        )
        zone.connections = data.get("connections", []).copy()
        zone.points_of_interest = [
            PointOfInterest(
                id=poi["id"],
                name=poi["name"],
                description=poi["description"],
                discovered=poi.get("discovered", False),
                visited=poi.get("visited", False),
                loot_available=poi.get("loot_available", True),
                quest_related=poi.get("quest_related", False),
                special_event=poi.get("special_event"),
            )
            for poi in data.get("points_of_interest", [])
        ]
        zone.resources = data.get("resources", {}).copy()
        zone.visibility_modifier = data.get("visibility_modifier", 0)
        zone.survival_modifier = data.get("survival_modifier", 0)
        zone.possible_events = data.get("possible_events", []).copy()
        zone.npcs = data.get("npcs", []).copy()
        zone.times_visited = data.get("times_visited", 0)
        zone.last_visited_scene = data.get("last_visited_scene", 0)
        return zone


@dataclass
class WorldMap:
    """Carte du monde avec toutes les zones."""
    zones: dict[str, Zone] = field(default_factory=dict)
    current_zone_id: str = ""
    discovered_zones: list[str] = field(default_factory=list)
    travel_history: list[str] = field(default_factory=list)
    
    def add_zone(self, zone: Zone) -> None:
        """Ajoute une zone a la carte."""
        self.zones[zone.id] = zone
    
    def get_zone(self, zone_id: str) -> Optional[Zone]:
        """Recupere une zone par son ID."""
        return self.zones.get(zone_id)
    
    def get_current_zone(self) -> Optional[Zone]:
        """Retourne la zone actuelle."""
        return self.zones.get(self.current_zone_id)
    
    def discover_zone(self, zone_id: str) -> bool:
        """Marque une zone comme decouverte."""
        if zone_id in self.zones and zone_id not in self.discovered_zones:
            self.discovered_zones.append(zone_id)
            return True
        return False
    
    def can_travel_to(self, target_zone_id: str) -> tuple[bool, str]:
        """Verifie si le deplacement est possible."""
        current = self.get_current_zone()
        if not current:
            return False, "Position actuelle inconnue"
        
        target = self.get_zone(target_zone_id)
        if not target:
            return False, "Zone cible inconnue"
        
        if target_zone_id not in current.connections:
            return False, f"Pas de chemin direct vers {target.name}"
        
        if target.status == ZoneStatus.BLOQUE:
            return False, f"{target.name} est bloquee"
        
        return True, "OK"
    
    def travel_to(self, target_zone_id: str, current_scene: int) -> tuple[bool, str, Optional[str]]:
        """
        Effectue le deplacement vers une zone.
        Retourne (succes, message, evenement_aleatoire).
        """
        can_travel, reason = self.can_travel_to(target_zone_id)
        if not can_travel:
            return False, reason, None
        
        target = self.zones[target_zone_id]
        
        # Marquer visite
        target.times_visited += 1
        target.last_visited_scene = current_scene
        
        # Decouvrir si necessaire
        if target_zone_id not in self.discovered_zones:
            self.discovered_zones.append(target_zone_id)
            target.status = ZoneStatus.EXPLORE
        
        self.current_zone_id = target_zone_id
        if not self.travel_history:
            self.travel_history.append(target_zone_id)
        elif self.travel_history[-1] != target_zone_id:
            self.travel_history.append(target_zone_id)
        
        # Evenement aleatoire base sur le danger
        event = self._roll_travel_event(target)
        
        return True, f"Arrive a {target.name}", event
    
    def _roll_travel_event(self, zone: Zone) -> Optional[str]:
        """Determine si un evenement se produit pendant le voyage."""
        # Plus la zone est dangereuse, plus les evenements sont probables
        event_chance = zone.threat_level.value * 15  # 15%, 30%, 45%, 60%, 75%
        
        if random.randint(1, 100) <= event_chance:
            if zone.possible_events:
                return random.choice(zone.possible_events)
            return random.choice(RANDOM_EVENTS.get(zone.threat_level, ["rien"]))
        
        return None
    
    def get_accessible_zones(self) -> list[Zone]:
        """Retourne les zones accessibles depuis la position actuelle."""
        current = self.get_current_zone()
        if not current:
            return []
        
        accessible = []
        for zone_id in current.connections:
            zone = self.zones.get(zone_id)
            if zone and zone.status != ZoneStatus.BLOQUE:
                accessible.append(zone)
        
        return accessible
    
    def to_dict(self) -> dict:
        """Serialise la carte."""
        return {
            "current_zone_id": self.current_zone_id,
            "discovered_zones": self.discovered_zones.copy(),
            "travel_history": self.travel_history.copy(),
            "zones": {zid: zone.to_dict() for zid, zone in self.zones.items()},
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "WorldMap":
        """Charge la carte depuis un dict."""
        world = cls()
        world.current_zone_id = data.get("current_zone_id", "")
        world.discovered_zones = data.get("discovered_zones", []).copy()
        world.travel_history = data.get("travel_history", []).copy()
        for zone_data in data.get("zones", {}).values():
            zone = Zone.from_dict(zone_data)
            world.zones[zone.id] = zone
        if not world.travel_history and world.current_zone_id:
            world.travel_history = [world.current_zone_id]
        return world


# =============================================================================
# EVENEMENTS ALEATOIRES
# =============================================================================

RANDOM_EVENTS: dict[ThreatLevel, list[str]] = {
    ThreatLevel.SECURISE: [
        "patrouille_amie",
        "refugie_perdu",
        "rumeur_utile",
    ],
    ThreatLevel.INCERTAIN: [
        "pillards_distants",
        "sons_suspects",
        "cadavre_frais",
        "cache_provisions",
    ],
    ThreatLevel.DANGEREUX: [
        "embuscade_cultiste",
        "meute_genestealers",
        "effondrement",
        "survivants_pieges",
        "artefact_etrange",
    ],
    ThreatLevel.HOSTILE: [
        "patrouille_tyranide",
        "nid_secondaire",
        "combat_en_cours",
        "corruption_warp",
        "guerrier_isole",
    ],
    ThreatLevel.MORT: [
        "essaim_complet",
        "bioforms_massifs",
        "spores_toxiques",
        "terrain_transforme",
    ],
}


# =============================================================================
# CARTE DE DEPART - RUCHE PRIMUS SECTEUR 7
# =============================================================================

def create_starting_map() -> WorldMap:
    """Cree la carte de depart du jeu."""
    world = WorldMap()
    
    # Zone de depart - Bloc d'habitation
    world.add_zone(Zone(
        id="hab_block_7",
        name="Bloc Habitation 7-Gamma",
        description="Votre bloc d'habitation. Les etages superieurs sont effondres, "
                    "mais les niveaux inferieurs offrent encore un abri precaire.",
        zone_type=ZoneType.HABITATION,
        threat_level=ThreatLevel.INCERTAIN,
        status=ZoneStatus.EXPLORE,
        connections=["corridor_principal", "sous_sol", "bloc_voisin"],
        points_of_interest=[
            PointOfInterest(
                id="appartement_karimus",
                name="Appartement de Karimus",
                description="Votre petit logement. Quelques affaires peuvent encore etre recuperees.",
                discovered=True,
                visited=True,
            ),
            PointOfInterest(
                id="station_vox_locale",
                name="Station Vox Locale",
                description="Une petite antenne de communication. Peut-etre fonctionnelle.",
                discovered=True,
            ),
        ],
        resources={"rations": 2, "eau": 3},
        possible_events=["bruit_etage", "voisin_cache", "fuite_gaz"],
    ))
    
    # Corridor principal
    world.add_zone(Zone(
        id="corridor_principal",
        name="Corridor Principal Niveau 7",
        description="Le long couloir qui traverse le secteur. Des barricades improvisees "
                    "bloquent certains passages. L'eclairage clignote.",
        zone_type=ZoneType.HABITATION,
        threat_level=ThreatLevel.DANGEREUX,
        connections=["hab_block_7", "marche_noir", "clinique", "checkpoint_pdf"],
        points_of_interest=[
            PointOfInterest(
                id="barricade_ouest",
                name="Barricade Ouest",
                description="Une barricade tenue par des survivants armes.",
            ),
        ],
        possible_events=["patrouille_genestealers", "refugies_fuyards", "tir_distant"],
        visibility_modifier=-1,
    ))
    
    # Sous-sol
    world.add_zone(Zone(
        id="sous_sol",
        name="Sous-sols du Bloc 7",
        description="Un labyrinthe de tuyaux, de cables et de tunnels de maintenance. "
                    "Sombre, humide, mais cache des choses utiles... et dangereuses.",
        zone_type=ZoneType.SOUTERRAIN,
        threat_level=ThreatLevel.DANGEREUX,
        connections=["hab_block_7", "tunnels_maintenance", "cave_stockage"],
        visibility_modifier=2,
        survival_modifier=-1,
        possible_events=["creature_ombre", "fuite_toxique", "cache_contrebandier"],
    ))
    
    # Bloc voisin
    world.add_zone(Zone(
        id="bloc_voisin",
        name="Bloc Habitation 7-Delta",
        description="Le bloc adjacent. Partiellement evacue, des rumeurs parlent de "
                    "survivants caches et de pillards.",
        zone_type=ZoneType.HABITATION,
        threat_level=ThreatLevel.DANGEREUX,
        connections=["hab_block_7", "corridor_principal"],
        status=ZoneStatus.INCONNU,
        possible_events=["pillards", "famille_cachee", "piege_cultiste"],
    ))
    
    # Marche noir
    world.add_zone(Zone(
        id="marche_noir",
        name="Marche Noir du Secteur 7",
        description="Un marche clandestin dans une ancienne usine. Les prix sont exorbitants, "
                    "mais on y trouve de tout... pour ceux qui peuvent payer.",
        zone_type=ZoneType.COMMERCIAL,
        threat_level=ThreatLevel.INCERTAIN,
        connections=["corridor_principal", "district_industriel"],
        points_of_interest=[
            PointOfInterest(
                id="stand_armes",
                name="Stand d'armes de Grox",
                description="Un ancien garde qui vend des armes recuperees.",
            ),
            PointOfInterest(
                id="infirmerie_fortune",
                name="Infirmerie de fortune",
                description="Un medic deserteur offre ses services.",
            ),
        ],
        resources={"credits": 50},
        possible_events=["arnaque", "raid_pdf", "nouveau_vendeur"],
    ))
    
    # Clinique
    world.add_zone(Zone(
        id="clinique",
        name="Clinique du Secteur 7",
        description="L'ancienne clinique du secteur. Partiellement pillee, mais quelques "
                    "fournitures medicales restent peut-etre.",
        zone_type=ZoneType.ADMINISTRATIF,
        threat_level=ThreatLevel.INCERTAIN,
        connections=["corridor_principal"],
        points_of_interest=[
            PointOfInterest(
                id="pharmacie",
                name="Pharmacie",
                description="Armoire a medicaments. Verrouillee.",
            ),
            PointOfInterest(
                id="salle_operation",
                name="Salle d'operation",
                description="Du materiel medical de valeur, si encore intact.",
            ),
        ],
        resources={"medikit": 1, "stimm": 2},
    ))
    
    # Checkpoint PDF
    world.add_zone(Zone(
        id="checkpoint_pdf",
        name="Checkpoint PDF Abandonne",
        description="Un ancien point de controle de la Defense Planetaire. Abandonne "
                    "dans la panique, peut-etre reste-t-il du materiel.",
        zone_type=ZoneType.ADMINISTRATIF,
        threat_level=ThreatLevel.DANGEREUX,
        connections=["corridor_principal", "zone_frontline"],
        points_of_interest=[
            PointOfInterest(
                id="armurerie",
                name="Armurerie",
                description="Porte blindee. Contenu inconnu.",
            ),
            PointOfInterest(
                id="poste_vox",
                name="Poste Vox",
                description="Equipement de communication militaire.",
                quest_related=True,
            ),
        ],
        possible_events=["soldat_blesse", "retour_pdf", "piege_genestealer"],
    ))
    
    # Zone de front
    world.add_zone(Zone(
        id="zone_frontline",
        name="Ligne de Front - Niveau 5",
        description="La ou les combats font rage. Des barricades brisees, des corps, "
                    "et le bourdonnement constant des essaims.",
        zone_type=ZoneType.RUINE,
        threat_level=ThreatLevel.HOSTILE,
        status=ZoneStatus.INFESTE,
        connections=["checkpoint_pdf"],
        visibility_modifier=-2,
        survival_modifier=-2,
        possible_events=["assaut_tyranide", "bombardement", "survivants_coinces", "tyran_garde"],
    ))
    
    # District industriel
    world.add_zone(Zone(
        id="district_industriel",
        name="District Industriel Epsilon",
        description="Les usines du secteur. Certaines fonctionnent encore en mode automatique, "
                    "d'autres sont des ruines fumantes.",
        zone_type=ZoneType.INDUSTRIEL,
        threat_level=ThreatLevel.DANGEREUX,
        connections=["marche_noir", "tunnels_maintenance"],
        points_of_interest=[
            PointOfInterest(
                id="usine_munitions",
                name="Usine de munitions",
                description="Production automatisee. Dangereusement instable.",
            ),
            PointOfInterest(
                id="atelier_mecanique",
                name="Atelier mecanique",
                description="Outils et pieces de rechange.",
            ),
        ],
        possible_events=["machine_folle", "ouvriers_pieges", "explosion"],
    ))
    
    # Tunnels de maintenance
    world.add_zone(Zone(
        id="tunnels_maintenance",
        name="Tunnels de Maintenance",
        description="Le reseau souterrain qui relie tout le secteur. Dangereux mais rapide.",
        zone_type=ZoneType.SOUTERRAIN,
        threat_level=ThreatLevel.HOSTILE,
        connections=["sous_sol", "district_industriel", "temple_empereur"],
        visibility_modifier=3,
        survival_modifier=-2,
        possible_events=["rippers", "effondrement", "nid_cache", "passage_secret"],
    ))
    
    # Temple de l'Empereur
    world.add_zone(Zone(
        id="temple_empereur",
        name="Temple de l'Empereur-Dieu",
        description="Le temple du secteur. Un bastion de foi et de resistance. "
                    "Les pretres et quelques fideles s'y sont barricades.",
        zone_type=ZoneType.RELIGIEUX,
        threat_level=ThreatLevel.SECURISE,
        connections=["tunnels_maintenance"],
        points_of_interest=[
            PointOfInterest(
                id="autel_principal",
                name="Autel Principal",
                description="Lieu de priere. Accordez une benediction.",
            ),
            PointOfInterest(
                id="crypte",
                name="Crypte",
                description="Passages secrets et reliques cachees.",
            ),
        ],
        npcs=["pere_mordecai", "soeur_helene"],
        resources={"eau_benite": 1},
        survival_modifier=1,
        possible_events=["sermon", "refugie_malade", "vision_empereur"],
    ))
    
    # Cave de stockage
    world.add_zone(Zone(
        id="cave_stockage",
        name="Cave de Stockage Abandonnee",
        description="Un ancien entrepot souterrain. L'air est lourd et des bruits "
                    "etranges resonnent dans l'obscurite.",
        zone_type=ZoneType.SOUTERRAIN,
        threat_level=ThreatLevel.DANGEREUX,
        connections=["sous_sol"],
        points_of_interest=[
            PointOfInterest(
                id="caisses_scellees",
                name="Caisses scellees",
                description="Conteneurs de transport. Contenu inconnu.",
            ),
        ],
        resources={"rations": 5, "munitions": 10},
        possible_events=["rat_ogryns", "contrebandier", "creature_cachee"],
    ))
    
    # Position de depart
    world.current_zone_id = "hab_block_7"
    world.discovered_zones = ["hab_block_7"]
    world.travel_history = ["hab_block_7"]
    
    return world


def format_zone_info(zone: Zone, include_connections: bool = True) -> str:
    """Formate les informations d'une zone pour affichage."""
    lines = [
        f"=== {zone.name.upper()} ===",
        f"Type: {zone.zone_type.value.capitalize()}",
        f"Danger: {'*' * zone.threat_level.value} ({zone.threat_level.name})",
        f"Statut: {zone.status.value.capitalize()}",
        "",
        zone.description,
        "",
    ]
    
    if zone.points_of_interest:
        lines.append("Points d'interet:")
        for poi in zone.points_of_interest:
            marker = "[X]" if poi.visited else "[?]" if poi.discovered else "[!]"
            lines.append(f"  {marker} {poi.name}")
    
    if include_connections:
        lines.append("")
        lines.append("Passages:")
        for conn_id in zone.connections:
            lines.append(f"  -> {conn_id}")
    
    if zone.visibility_modifier != 0:
        sign = "+" if zone.visibility_modifier > 0 else ""
        lines.append(f"Discretion: {sign}{zone.visibility_modifier}")
    
    if zone.survival_modifier != 0:
        sign = "+" if zone.survival_modifier > 0 else ""
        lines.append(f"Survie: {sign}{zone.survival_modifier}")
    
    return "\n".join(lines)


def format_map_overview(world: WorldMap) -> str:
    """Formate une vue d'ensemble de la carte."""
    lines = ["=== CARTE DU SECTEUR 7 ===", ""]
    
    current = world.get_current_zone()
    if current:
        lines.append(f"Position actuelle: {current.name}")
        lines.append("")
    
    lines.append("Zones decouvertes:")
    for zone_id in world.discovered_zones:
        zone = world.zones.get(zone_id)
        if zone:
            marker = "[*]" if zone_id == world.current_zone_id else "[ ]"
            danger = "*" * zone.threat_level.value
            lines.append(f"  {marker} {zone.name} ({danger})")
    
    lines.append("")
    lines.append("Zones accessibles:")
    for zone in world.get_accessible_zones():
        status = f"({zone.status.value})" if zone.status != ZoneStatus.INCONNU else "(inexplore)"
        lines.append(f"  -> {zone.name} {status}")
    
    return "\n".join(lines)
