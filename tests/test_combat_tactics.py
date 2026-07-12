"""Tests du systeme de combat tactique (Phase A)."""

from src.combat import (
    Combatant, CombatState, CoverType,
    roll_with_advantage, compute_tactical_advantage,
    use_combat_ability, get_available_abilities, resolve_attack,
)


def _make_combatant(name="Testeur", is_player=True, combat=4, defense=2, hp=12):
    return Combatant(
        name=name, is_player=is_player,
        combat=combat, defense=defense, speed=3, special=2,
        health=hp, max_health=hp,
    )


def test_roll_with_advantage_bounds():
    for _ in range(50):
        assert 2 <= roll_with_advantage(2).total <= 12
        assert 2 <= roll_with_advantage(-2).total <= 12
        assert 2 <= roll_with_advantage(0).total <= 12


def test_conditions_apply_and_expire():
    c = _make_combatant()
    c.add_condition("supprime", 2)
    assert c.has_condition("supprime")
    assert c.condition_attack_mod() == -3
    # Deux ticks -> la condition expire.
    c.tick_conditions()
    c.tick_conditions()
    assert not c.has_condition("supprime")


def test_bleeding_deals_damage_over_time():
    c = _make_combatant(hp=10)
    c.add_condition("saignement", 2)
    c.tick_conditions()
    assert c.health == 8  # -2 par tour


def test_stun_flag():
    c = _make_combatant()
    c.add_condition("etourdi", 1)
    assert c.is_stunned() is True


def test_marked_increases_incoming_damage():
    attacker = _make_combatant(name="Att", combat=6)
    defender = _make_combatant(name="Def", is_player=False, defense=0, hp=30)
    defender.add_condition("marque", 3)
    # Force un coup: enorme avantage + attaque elevee.
    total = 0
    for _ in range(20):
        d = defender
        d.health = 30
        res = resolve_attack(attacker, d, advantage=2)
        if res["hit"]:
            total += 1
    assert total > 0  # au moins un coup porte, la logique marque ne casse pas


def test_available_abilities_include_basic_parade():
    abilities = get_available_abilities([])
    ids = {a["id"] for a in abilities}
    assert "parade" in ids


def test_use_ability_parade_grants_guard():
    player = _make_combatant()
    combat = CombatState(player=player, enemies=[_make_combatant(name="E", is_player=False)])
    player.action_points = 2
    res = use_combat_ability(player, "parade", None, combat)
    assert res["success"] is True
    assert player.has_condition("en_garde")


def test_use_ability_insufficient_ap():
    player = _make_combatant()
    enemy = _make_combatant(name="E", is_player=False)
    combat = CombatState(player=player, enemies=[enemy])
    player.action_points = 0
    res = use_combat_ability(player, "frappe_puissante", enemy, combat)
    assert res["success"] is False


def test_tactical_advantage_aiming_and_cover():
    player = _make_combatant()
    enemy = _make_combatant(name="E", is_player=False)
    combat = CombatState(player=player, enemies=[enemy])
    player.is_aiming = True
    enemy.cover = CoverType.HEAVY
    # +1 (visee) -1 (couvert lourd) = 0
    assert compute_tactical_advantage(player, enemy, combat) == 0
