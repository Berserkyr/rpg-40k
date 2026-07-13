"""Tests du bestiaire etendu et des archetypes visuels (src/entities.py)."""

from src.entities import (
    Faction,
    ThreatLevel,
    ALL_TEMPLATES,
    HOSTILE_FACTIONS,
    BODY_TYPES,
    generate_entity,
    entity_body_type,
)


def test_toutes_les_factions_hostiles_ont_des_templates():
    for faction in HOSTILE_FACTIONS:
        assert faction in ALL_TEMPLATES
        # Chaque faction couvre les 4 niveaux de menace.
        for level in ThreatLevel:
            assert ALL_TEMPLATES[faction].get(level), f"{faction} sans template {level}"


def test_generation_toutes_factions_tous_niveaux():
    for faction in ALL_TEMPLATES:
        for level in ThreatLevel:
            entity = generate_entity(faction, level)
            assert entity.name
            assert entity.faction == faction


def test_body_type_valide_pour_toutes_entites():
    for faction in ALL_TEMPLATES:
        for level in ThreatLevel:
            entity = generate_entity(faction, level)
            assert entity_body_type(entity) in BODY_TYPES


def test_body_type_tyranide_est_bestial_ou_specialise():
    ripper = generate_entity(Faction.TYRANID, ThreatLevel.MINION, name_override="Ripper")
    assert entity_body_type(ripper) == "swarm"
    carnifex = generate_entity(Faction.TYRANID, ThreatLevel.BOSS, name_override="Carnifex")
    assert entity_body_type(carnifex) == "brute"


def test_body_type_mechanicus_est_machine():
    magos = generate_entity(Faction.MECHANICUS, ThreatLevel.BOSS)
    assert entity_body_type(magos) == "machine"


def test_body_type_garde_imperiale_humanoide():
    guard = generate_entity(Faction.IMPERIAL_GUARD, ThreatLevel.STANDARD)
    assert entity_body_type(guard) == "humanoid"


def test_hostile_factions_non_vide():
    assert len(HOSTILE_FACTIONS) >= 5
    assert Faction.TYRANID in HOSTILE_FACTIONS
    assert Faction.CHAOS in HOSTILE_FACTIONS
