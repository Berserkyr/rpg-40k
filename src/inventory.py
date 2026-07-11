"""Inventory and equipment system for the 40K RPG."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict


class ItemType(Enum):
    WEAPON_MELEE = "arme_melee"
    WEAPON_RANGED = "arme_distance"
    ARMOR = "armure"
    CONSUMABLE = "consommable"
    TOOL = "outil"
    KEY_ITEM = "objet_cle"
    AMMO = "munitions"
    MISC = "divers"


class WeaponRange(Enum):
    MELEE = "melee"
    SHORT = "courte"
    MEDIUM = "moyenne"
    LONG = "longue"


class Rarity(Enum):
    COMMON = "commun"
    UNCOMMON = "peu_commun"
    RARE = "rare"
    EXOTIC = "exotique"
    RELIC = "relique"


@dataclass
class Item:
    """Base item class."""
    
    id: str
    name: str
    item_type: ItemType
    description: str
    weight: float = 1.0
    value: int = 0
    rarity: Rarity = Rarity.COMMON
    stackable: bool = False
    quantity: int = 1
    max_stack: int = 1
    
    def as_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.item_type.value,
            "description": self.description,
            "weight": self.weight,
            "value": self.value,
            "rarity": self.rarity.value,
            "quantity": self.quantity,
        }


@dataclass
class Weapon(Item):
    """A weapon with combat stats."""
    
    damage: int = 2
    accuracy: int = 0
    range_type: WeaponRange = WeaponRange.MELEE
    ammo_type: Optional[str] = None
    ammo_capacity: int = 0
    current_ammo: int = 0
    special_abilities: List[str] = field(default_factory=list)
    two_handed: bool = False
    
    def __post_init__(self):
        if self.range_type == WeaponRange.MELEE:
            self.item_type = ItemType.WEAPON_MELEE
        else:
            self.item_type = ItemType.WEAPON_RANGED
    
    def needs_reload(self) -> bool:
        return self.ammo_capacity > 0 and self.current_ammo == 0
    
    def reload(self, ammo_available: int) -> int:
        """Reload weapon, return ammo consumed."""
        needed = self.ammo_capacity - self.current_ammo
        consumed = min(needed, ammo_available)
        self.current_ammo += consumed
        return consumed

    def as_dict(self) -> Dict:
        data = super().as_dict()
        data.update({
            "damage": self.damage,
            "accuracy": self.accuracy,
            "range_type": self.range_type.value,
            "ammo_type": self.ammo_type,
            "ammo_capacity": self.ammo_capacity,
            "current_ammo": self.current_ammo,
            "special_abilities": self.special_abilities.copy(),
            "two_handed": self.two_handed,
        })
        return data


@dataclass
class Armor(Item):
    """Armor providing defense."""
    
    defense_bonus: int = 1
    max_defense_bonus: int = 1
    durability: int = 100
    max_durability: int = 100
    coverage: str = "torse"  # torse, tete, jambes, complet
    special_properties: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.item_type = ItemType.ARMOR
    
    def take_damage(self, amount: int) -> int:
        """Reduce durability, return actual defense provided."""
        if self.durability <= 0:
            return 0
        self.durability = max(0, self.durability - amount // 2)
        effectiveness = self.durability / self.max_durability
        return int(self.defense_bonus * effectiveness)

    def as_dict(self) -> Dict:
        data = super().as_dict()
        data.update({
            "defense_bonus": self.defense_bonus,
            "max_defense_bonus": self.max_defense_bonus,
            "durability": self.durability,
            "max_durability": self.max_durability,
            "coverage": self.coverage,
            "special_properties": self.special_properties.copy(),
        })
        return data


@dataclass
class Consumable(Item):
    """Consumable items with effects."""
    
    effect_type: str = "heal"  # heal, buff, cure, damage
    effect_value: int = 0
    effect_duration: int = 0  # 0 = instant
    effect_description: str = ""
    
    def __post_init__(self):
        self.item_type = ItemType.CONSUMABLE
        self.stackable = True
        self.max_stack = 10

    def as_dict(self) -> Dict:
        data = super().as_dict()
        data.update({
            "effect_type": self.effect_type,
            "effect_value": self.effect_value,
            "effect_duration": self.effect_duration,
            "effect_description": self.effect_description,
        })
        return data


@dataclass
class Inventory:
    """Player inventory management."""
    
    items: List[Item] = field(default_factory=list)
    max_weight: float = 20.0
    credits: int = 0
    
    # Equipment slots
    weapon_main: Optional[Weapon] = None
    weapon_secondary: Optional[Weapon] = None
    armor_body: Optional[Armor] = None
    armor_head: Optional[Armor] = None
    
    def current_weight(self) -> float:
        return sum(item.weight * item.quantity for item in self.items)
    
    def can_add(self, item: Item) -> bool:
        return self.current_weight() + (item.weight * item.quantity) <= self.max_weight
    
    def add_item(self, item: Item) -> bool:
        """Add item to inventory. Returns False if overweight."""
        if not self.can_add(item):
            return False
        
        # Stack if possible
        if item.stackable:
            for existing in self.items:
                if existing.id == item.id and existing.quantity < existing.max_stack:
                    space = existing.max_stack - existing.quantity
                    transfer = min(space, item.quantity)
                    existing.quantity += transfer
                    item.quantity -= transfer
                    if item.quantity <= 0:
                        return True
        
        if item.quantity > 0:
            self.items.append(item)
        return True
    
    def remove_item(self, item_id: str, quantity: int = 1) -> Optional[Item]:
        """Remove item from inventory."""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                if item.stackable and item.quantity > quantity:
                    item.quantity -= quantity
                    removed = Item(
                        id=item.id,
                        name=item.name,
                        item_type=item.item_type,
                        description=item.description,
                        quantity=quantity,
                    )
                    return removed
                else:
                    return self.items.pop(i)
        return None
    
    def get_item(self, item_id: str) -> Optional[Item]:
        """Find item by ID."""
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def equip_weapon(self, weapon: Weapon, slot: str = "main") -> Optional[Weapon]:
        """Equip weapon, return previously equipped."""
        if slot == "main":
            old = self.weapon_main
            self.weapon_main = weapon
        else:
            old = self.weapon_secondary
            self.weapon_secondary = weapon
        
        # Remove from inventory
        self.remove_item(weapon.id)
        
        # Add old to inventory if exists
        if old:
            self.add_item(old)
        
        return old
    
    def equip_armor(self, armor: Armor) -> Optional[Armor]:
        """Equip armor, return previously equipped."""
        if armor.coverage in ("torse", "complet"):
            old = self.armor_body
            self.armor_body = armor
        else:
            old = self.armor_head
            self.armor_head = armor
        
        self.remove_item(armor.id)
        if old:
            self.add_item(old)
        
        return old
    
    def total_defense_bonus(self) -> int:
        """Calculate total defense from equipped armor."""
        bonus = 0
        if self.armor_body:
            bonus += self.armor_body.defense_bonus
        if self.armor_head:
            bonus += self.armor_head.defense_bonus
        return bonus
    
    def as_markdown(self) -> str:
        """Format inventory for display."""
        lines = [
            f"### Inventaire ({self.current_weight():.1f}/{self.max_weight:.1f} kg)",
            f"Credits: {self.credits}",
            "",
            "**Equipe:**",
        ]
        
        if self.weapon_main:
            lines.append(f"  Arme principale: {self.weapon_main.name} (Deg:{self.weapon_main.damage})")
        if self.weapon_secondary:
            lines.append(f"  Arme secondaire: {self.weapon_secondary.name}")
        if self.armor_body:
            lines.append(f"  Armure: {self.armor_body.name} (Def:+{self.armor_body.defense_bonus})")
        if self.armor_head:
            lines.append(f"  Casque: {self.armor_head.name}")
        
        lines.append("")
        lines.append("**Objets:**")
        
        if not self.items:
            lines.append("  (vide)")
        else:
            for item in self.items:
                qty = f" x{item.quantity}" if item.quantity > 1 else ""
                lines.append(f"  - {item.name}{qty} ({item.item_type.value})")
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict:
        """Serialize inventory."""
        return {
            "items": [i.as_dict() for i in self.items],
            "max_weight": self.max_weight,
            "credits": self.credits,
            "weapon_main": self.weapon_main.as_dict() if self.weapon_main else None,
            "weapon_secondary": self.weapon_secondary.as_dict() if self.weapon_secondary else None,
            "armor_body": self.armor_body.as_dict() if self.armor_body else None,
            "armor_head": self.armor_head.as_dict() if self.armor_head else None,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Inventory":
        """Deserialize inventory data saved by to_dict()."""
        inv = cls(
            max_weight=data.get("max_weight", 20.0),
            credits=data.get("credits", 50),
        )
        inv.items = [item_from_dict(item) for item in data.get("items", [])]
        inv.items = [item for item in inv.items if item is not None]
        inv.weapon_main = item_from_dict(data.get("weapon_main"))
        inv.weapon_secondary = item_from_dict(data.get("weapon_secondary"))
        inv.armor_body = item_from_dict(data.get("armor_body"))
        inv.armor_head = item_from_dict(data.get("armor_head"))
        return inv


# ---------------------------------------------------------------------------
# Item templates / loot tables
# ---------------------------------------------------------------------------

WEAPON_TEMPLATES = {
    "laspistol": {
        "name": "Laspistol",
        "damage": 3,
        "accuracy": 1,
        "range_type": WeaponRange.SHORT,
        "ammo_type": "cellule_energie",
        "ammo_capacity": 15,
        "weight": 0.8,
        "value": 25,
        "rarity": Rarity.COMMON,
        "description": "Pistolet laser standard de l'Imperium.",
    },
    "autopistol": {
        "name": "Autopistol",
        "damage": 4,
        "accuracy": 0,
        "range_type": WeaponRange.SHORT,
        "ammo_type": "balle_auto",
        "ammo_capacity": 12,
        "weight": 1.0,
        "value": 15,
        "rarity": Rarity.COMMON,
        "description": "Pistolet a projectiles bruyant mais efficace.",
    },
    "lasgun": {
        "name": "Lasgun",
        "damage": 4,
        "accuracy": 1,
        "range_type": WeaponRange.MEDIUM,
        "ammo_type": "cellule_energie",
        "ammo_capacity": 30,
        "weight": 2.5,
        "value": 50,
        "rarity": Rarity.COMMON,
        "two_handed": True,
        "description": "Fusil laser standard de la Garde Imperiale.",
    },
    "stub_revolver": {
        "name": "Revolver Stub",
        "damage": 5,
        "accuracy": 0,
        "range_type": WeaponRange.SHORT,
        "ammo_type": "balle_stub",
        "ammo_capacity": 6,
        "weight": 1.2,
        "value": 20,
        "rarity": Rarity.COMMON,
        "description": "Revolver rustique mais fiable.",
    },
    "knife": {
        "name": "Couteau",
        "damage": 2,
        "accuracy": 1,
        "range_type": WeaponRange.MELEE,
        "weight": 0.3,
        "value": 5,
        "rarity": Rarity.COMMON,
        "description": "Lame basique pour le corps a corps.",
    },
    "club": {
        "name": "Gourdin",
        "damage": 3,
        "accuracy": 0,
        "range_type": WeaponRange.MELEE,
        "weight": 1.5,
        "value": 2,
        "rarity": Rarity.COMMON,
        "description": "Barre de metal ou baton renforce.",
    },
    "chainsword": {
        "name": "Epee-tronconneuse",
        "damage": 6,
        "accuracy": 0,
        "range_type": WeaponRange.MELEE,
        "weight": 3.0,
        "value": 150,
        "rarity": Rarity.UNCOMMON,
        "special_abilities": ["Dechiquetage"],
        "description": "Lame dentee motorisee, symbole de l'Imperium.",
    },
    "shotgun": {
        "name": "Fusil a pompe",
        "damage": 6,
        "accuracy": -1,
        "range_type": WeaponRange.SHORT,
        "ammo_type": "cartouche",
        "ammo_capacity": 8,
        "weight": 3.5,
        "value": 40,
        "rarity": Rarity.COMMON,
        "two_handed": True,
        "special_abilities": ["Dispersion"],
        "description": "Devastateur a courte portee.",
    },
}

ARMOR_TEMPLATES = {
    "flak_vest": {
        "name": "Gilet Flak",
        "defense_bonus": 1,
        "durability": 80,
        "weight": 4.0,
        "value": 30,
        "rarity": Rarity.COMMON,
        "coverage": "torse",
        "description": "Protection standard contre les eclats.",
    },
    "flak_armor": {
        "name": "Armure Flak Complete",
        "defense_bonus": 2,
        "durability": 100,
        "weight": 8.0,
        "value": 75,
        "rarity": Rarity.COMMON,
        "coverage": "complet",
        "description": "Protection complete de la Garde.",
    },
    "carapace": {
        "name": "Armure Carapace",
        "defense_bonus": 3,
        "durability": 150,
        "weight": 12.0,
        "value": 200,
        "rarity": Rarity.UNCOMMON,
        "coverage": "complet",
        "special_properties": ["Lourd"],
        "description": "Protection superieure des Stormtroopers.",
    },
    "mesh_cloak": {
        "name": "Cape en Mailles",
        "defense_bonus": 1,
        "durability": 50,
        "weight": 1.5,
        "value": 100,
        "rarity": Rarity.UNCOMMON,
        "coverage": "torse",
        "special_properties": ["Discret"],
        "description": "Protection legere et discrete.",
    },
    "worker_helmet": {
        "name": "Casque d'Ouvrier",
        "defense_bonus": 1,
        "durability": 40,
        "weight": 1.0,
        "value": 10,
        "rarity": Rarity.COMMON,
        "coverage": "tete",
        "description": "Casque de travail basique.",
    },
}

CONSUMABLE_TEMPLATES = {
    "stimm": {
        "name": "Stimm",
        "effect_type": "heal",
        "effect_value": 4,
        "weight": 0.1,
        "value": 15,
        "rarity": Rarity.COMMON,
        "description": "Injection medicale d'urgence.",
    },
    "medikit": {
        "name": "Medikit",
        "effect_type": "heal",
        "effect_value": 8,
        "weight": 0.5,
        "value": 50,
        "rarity": Rarity.UNCOMMON,
        "description": "Kit medical complet.",
    },
    "ration_imperiale": {
        "name": "Ration Imperiale",
        "effect_type": "buff",
        "effect_value": 1,
        "effect_duration": 3,
        "weight": 0.3,
        "value": 5,
        "rarity": Rarity.COMMON,
        "description": "Nourriture de survie standardisee.",
    },
    "frenzon": {
        "name": "Frenzon",
        "effect_type": "buff",
        "effect_value": 3,
        "effect_duration": 2,
        "weight": 0.1,
        "value": 40,
        "rarity": Rarity.UNCOMMON,
        "special_properties": ["Combat_bonus", "Stress_apres"],
        "description": "Drogue de combat. +3 attaque, +1 stress apres.",
    },
    "obscura": {
        "name": "Obscura",
        "effect_type": "cure",
        "effect_value": 2,
        "weight": 0.05,
        "value": 25,
        "rarity": Rarity.UNCOMMON,
        "special_properties": ["Stress_reduction", "Addictif"],
        "description": "Drogue recreative. Reduit stress mais addictive.",
    },
}


def create_weapon(template_id: str) -> Optional[Weapon]:
    """Create a weapon from template."""
    template = WEAPON_TEMPLATES.get(template_id)
    if not template:
        return None
    
    return Weapon(
        id=template_id,
        name=template["name"],
        item_type=ItemType.WEAPON_RANGED if template.get("range_type", WeaponRange.MELEE) != WeaponRange.MELEE else ItemType.WEAPON_MELEE,
        description=template["description"],
        weight=template.get("weight", 1.0),
        value=template.get("value", 0),
        rarity=template.get("rarity", Rarity.COMMON),
        damage=template["damage"],
        accuracy=template.get("accuracy", 0),
        range_type=template.get("range_type", WeaponRange.MELEE),
        ammo_type=template.get("ammo_type"),
        ammo_capacity=template.get("ammo_capacity", 0),
        current_ammo=template.get("ammo_capacity", 0),
        special_abilities=template.get("special_abilities", []),
        two_handed=template.get("two_handed", False),
    )


def create_armor(template_id: str) -> Optional[Armor]:
    """Create armor from template."""
    template = ARMOR_TEMPLATES.get(template_id)
    if not template:
        return None
    
    return Armor(
        id=template_id,
        name=template["name"],
        item_type=ItemType.ARMOR,
        description=template["description"],
        weight=template.get("weight", 1.0),
        value=template.get("value", 0),
        rarity=template.get("rarity", Rarity.COMMON),
        defense_bonus=template["defense_bonus"],
        max_defense_bonus=template["defense_bonus"],
        durability=template.get("durability", 100),
        max_durability=template.get("durability", 100),
        coverage=template.get("coverage", "torse"),
        special_properties=template.get("special_properties", []),
    )


def create_consumable(template_id: str, quantity: int = 1) -> Optional[Consumable]:
    """Create consumable from template."""
    template = CONSUMABLE_TEMPLATES.get(template_id)
    if not template:
        return None
    
    return Consumable(
        id=template_id,
        name=template["name"],
        item_type=ItemType.CONSUMABLE,
        description=template["description"],
        weight=template.get("weight", 0.1),
        value=template.get("value", 0),
        rarity=template.get("rarity", Rarity.COMMON),
        quantity=quantity,
        max_stack=10,
        stackable=True,
        effect_type=template["effect_type"],
        effect_value=template["effect_value"],
        effect_duration=template.get("effect_duration", 0),
        effect_description=template.get("effect_description", ""),
    )


def item_from_dict(data: Optional[Dict]) -> Optional[Item]:
    """Rebuild an Item/Weapon/Armor/Consumable from serialized data."""
    if not data:
        return None

    item_id = data.get("id", "unknown")
    item_type = data.get("type", ItemType.MISC.value)
    quantity = data.get("quantity", 1)

    if item_id in WEAPON_TEMPLATES or item_type in (ItemType.WEAPON_MELEE.value, ItemType.WEAPON_RANGED.value):
        weapon = create_weapon(item_id)
        if weapon:
            weapon.quantity = quantity
            weapon.current_ammo = data.get("current_ammo", weapon.current_ammo)
            return weapon

    if item_id in ARMOR_TEMPLATES or item_type == ItemType.ARMOR.value:
        armor = create_armor(item_id)
        if armor:
            armor.quantity = quantity
            armor.durability = data.get("durability", armor.durability)
            return armor
        return Armor(
            id=item_id,
            name=data.get("name", item_id),
            item_type=ItemType.ARMOR,
            description=data.get("description", "Protection recuperee dans la ruche."),
            weight=data.get("weight", 1.0),
            value=data.get("value", 0),
            rarity=Rarity(data.get("rarity", Rarity.COMMON.value)),
            quantity=quantity,
            defense_bonus=data.get("defense_bonus", 1),
            max_defense_bonus=data.get("max_defense_bonus", data.get("defense_bonus", 1)),
            durability=data.get("durability", 100),
            max_durability=data.get("max_durability", 100),
            coverage=data.get("coverage", "torse"),
            special_properties=data.get("special_properties", []).copy(),
        )

    if item_id in CONSUMABLE_TEMPLATES or item_type == ItemType.CONSUMABLE.value:
        consumable = create_consumable(item_id, quantity)
        if consumable:
            return consumable

    try:
        parsed_type = ItemType(item_type)
    except ValueError:
        parsed_type = ItemType.MISC

    try:
        parsed_rarity = Rarity(data.get("rarity", Rarity.COMMON.value))
    except ValueError:
        parsed_rarity = Rarity.COMMON

    return Item(
        id=item_id,
        name=data.get("name", item_id),
        item_type=parsed_type,
        description=data.get("description", "Objet recupere dans la ruche."),
        weight=data.get("weight", 1.0),
        value=data.get("value", 0),
        rarity=parsed_rarity,
        stackable=data.get("stackable", False),
        quantity=quantity,
        max_stack=data.get("max_stack", 1),
    )


def generate_loot(threat_level: str, context: str = "") -> List[Item]:
    """Generate random loot based on threat level."""
    loot = []
    
    # Loot chances by threat
    loot_tables = {
        "sbire": {"weapon": 0.1, "armor": 0.05, "consumable": 0.3, "credits": (5, 15)},
        "standard": {"weapon": 0.25, "armor": 0.15, "consumable": 0.4, "credits": (10, 40)},
        "elite": {"weapon": 0.5, "armor": 0.3, "consumable": 0.6, "credits": (30, 100)},
        "boss": {"weapon": 0.9, "armor": 0.6, "consumable": 0.8, "credits": (100, 300)},
    }
    
    table = loot_tables.get(threat_level, loot_tables["standard"])
    
    # Weapons
    if random.random() < table["weapon"]:
        weapon_id = random.choice(list(WEAPON_TEMPLATES.keys()))
        weapon = create_weapon(weapon_id)
        if weapon:
            loot.append(weapon)
    
    # Armor
    if random.random() < table["armor"]:
        armor_id = random.choice(list(ARMOR_TEMPLATES.keys()))
        armor = create_armor(armor_id)
        if armor:
            loot.append(armor)
    
    # Consumables
    if random.random() < table["consumable"]:
        consumable_id = random.choice(list(CONSUMABLE_TEMPLATES.keys()))
        consumable = create_consumable(consumable_id, random.randint(1, 3))
        if consumable:
            loot.append(consumable)
    
    return loot
