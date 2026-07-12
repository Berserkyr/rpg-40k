"""Tests du systeme de gestion d'equipe (src/team.py)."""

from src.team import (
    Team,
    Companion,
    create_companion,
    available_templates,
    COMPANION_TEMPLATES,
)


def test_create_companion_respecte_niveau():
    companion, msg = create_companion("sororitas", level=1)
    assert companion is None
    assert "Niveau" in msg

    companion, _ = create_companion("sororitas", level=4)
    assert companion is not None
    assert companion.archetype == "sororitas"


def test_create_companion_archetype_inconnu():
    companion, msg = create_companion("inexistant", level=10)
    assert companion is None
    assert "inconnu" in msg.lower()


def test_team_add_and_limit():
    team = Team(max_size=2)
    c1, _ = create_companion("milicien", level=5)
    c2, _ = create_companion("eclaireur", level=5)
    c3, _ = create_companion("tech_pretre", level=5)
    assert team.add(c1)[0] is True
    assert team.add(c2)[0] is True
    ok, msg = team.add(c3)
    assert ok is False
    assert "complete" in msg.lower()


def test_team_no_duplicate():
    team = Team()
    c1, _ = create_companion("milicien", level=5)
    team.add(c1)
    ok, _ = team.add(c1)
    assert ok is False


def test_team_remove():
    team = Team()
    c1, _ = create_companion("milicien", level=5)
    team.add(c1)
    ok, _ = team.remove("milicien")
    assert ok is True
    assert len(team.members) == 0
    ok, _ = team.remove("milicien")
    assert ok is False


def test_team_roundtrip_serialization():
    team = Team(max_size=3)
    c1, _ = create_companion("milicien", level=5)
    team.add(c1)
    restored = Team.from_dict(team.to_dict())
    assert restored.max_size == 3
    assert len(restored.members) == 1
    assert restored.members[0].id == "milicien"


def test_available_templates_unlock_flag():
    templates = available_templates(level=1)
    by_id = {t["id"]: t for t in templates}
    assert by_id["milicien"]["unlocked"] is True
    assert by_id["sororitas"]["unlocked"] is False
    assert len(templates) == len(COMPANION_TEMPLATES)
