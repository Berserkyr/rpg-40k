from src.inventory import (
    Armor,
    Consumable,
    Inventory,
    Item,
    ItemType,
    Rarity,
    Weapon,
    WeaponRange,
)


def test_inventory_refuses_overweight_item():
    inventory = Inventory(max_weight=1.0)
    heavy_item = Item(
        id="scrap-heavy",
        name="Bloc de ferraille",
        item_type=ItemType.MISC,
        description="Trop lourd pour Karimus.",
        weight=2.0,
    )

    assert inventory.add_item(heavy_item) is False
    assert inventory.items == []
    assert inventory.current_weight() == 0


def test_stackable_consumables_merge_until_max_stack():
    inventory = Inventory(max_weight=20.0)
    first_stack = Consumable(
        id="stimm",
        name="Stimm",
        item_type=ItemType.CONSUMABLE,
        description="Injection médicale.",
        weight=0.1,
        quantity=7,
    )
    second_stack = Consumable(
        id="stimm",
        name="Stimm",
        item_type=ItemType.CONSUMABLE,
        description="Injection médicale.",
        weight=0.1,
        quantity=5,
    )

    assert inventory.add_item(first_stack) is True
    assert inventory.add_item(second_stack) is True

    assert len(inventory.items) == 2
    assert inventory.items[0].quantity == 10
    assert inventory.items[1].quantity == 2


def test_equipping_weapon_removes_it_from_inventory_and_returns_previous():
    inventory = Inventory(max_weight=20.0)
    knife = Weapon(
        id="knife",
        name="Couteau",
        item_type=ItemType.WEAPON_MELEE,
        description="Lame de secours.",
        weight=0.3,
        damage=2,
        accuracy=1,
        range_type=WeaponRange.MELEE,
    )
    pistol = Weapon(
        id="laspistol",
        name="Laspistol",
        item_type=ItemType.WEAPON_RANGED,
        description="Pistolet laser.",
        weight=0.8,
        damage=3,
        accuracy=1,
        range_type=WeaponRange.SHORT,
        ammo_capacity=15,
        current_ammo=15,
    )

    inventory.add_item(knife)
    inventory.add_item(pistol)

    assert inventory.equip_weapon(knife, slot="main") is None
    previous = inventory.equip_weapon(pistol, slot="main")

    assert previous == knife
    assert inventory.weapon_main == pistol
    assert inventory.get_item("laspistol") is None
    assert inventory.get_item("knife") == knife


def test_armor_damage_degrades_defense_and_never_goes_negative():
    armor = Armor(
        id="flak",
        name="Gilet Flak",
        item_type=ItemType.ARMOR,
        description="Protection standard.",
        defense_bonus=4,
        max_defense_bonus=4,
        durability=100,
        max_durability=100,
        rarity=Rarity.COMMON,
    )

    defense_after_hit = armor.take_damage(50)
    assert armor.durability == 75
    assert defense_after_hit == 3

    defense_after_massive_hit = armor.take_damage(500)
    assert armor.durability == 0
    assert defense_after_massive_hit == 0
    assert armor.take_damage(10) == 0


def test_inventory_round_trip_serialization_preserves_equipment():
    inventory = Inventory(max_weight=25.0, credits=42)
    armor = Armor(
        id="helmet",
        name="Casque d'ouvrier",
        item_type=ItemType.ARMOR,
        description="Casque renforcé.",
        defense_bonus=1,
        coverage="tete",
    )
    inventory.add_item(armor)
    inventory.equip_armor(armor)

    restored = Inventory.from_dict(inventory.to_dict())

    assert restored.credits == 42
    assert restored.max_weight == 25.0
    assert restored.armor_head is not None
    assert restored.armor_head.id == "helmet"
    assert restored.total_defense_bonus() == 1
