import pytest
from src.entities import (
    Faction, ThreatLevel, EntityStats, Entity,
    generate_entity, generate_encounter, generate_npc,
    encounter_to_prompt, entity_difficulty_for_player,
)


def test_entity_stats_total():
    stats = EntityStats(combat=3, defense=2, speed=4, special=1)
    assert stats.total_threat() == 10


def test_generate_entity_tyranid():
    entity = generate_entity(Faction.TYRANID, ThreatLevel.MINION)
    assert entity.faction == Faction.TYRANID
    assert entity.threat_level == ThreatLevel.MINION
    assert entity.name in ("Hormagaunt", "Termagant", "Ripper")


def test_generate_entity_boss():
    entity = generate_entity(Faction.TYRANID, ThreatLevel.BOSS)
    assert entity.threat_level == ThreatLevel.BOSS
    assert entity.stats.total_threat() >= 10


def test_generate_encounter_standard():
    encounter = generate_encounter(Faction.TYRANID, difficulty="standard")
    assert len(encounter) >= 2
    threat_levels = [e.threat_level for e in encounter]
    assert ThreatLevel.MINION in threat_levels or ThreatLevel.STANDARD in threat_levels


def test_generate_npc():
    npc = generate_npc("Medecin clandestin", Faction.CIVILIAN, ThreatLevel.STANDARD)
    assert "Medecin clandestin" in npc.description
    assert npc.faction == Faction.CIVILIAN


def test_encounter_to_prompt():
    entities = [generate_entity(Faction.TYRANID, ThreatLevel.MINION)]
    prompt = encounter_to_prompt(entities)
    assert "Entites presentes:" in prompt
    assert "tyranide" in prompt


def test_entity_difficulty():
    weak = Entity(
        name="Test", faction=Faction.CIVILIAN, threat_level=ThreatLevel.MINION,
        stats=EntityStats(1, 1, 1, 0)
    )
    assert entity_difficulty_for_player(weak, player_combat=3) == "Gerable"
    
    strong = Entity(
        name="Boss", faction=Faction.TYRANID, threat_level=ThreatLevel.BOSS,
        stats=EntityStats(7, 6, 3, 5)
    )
    assert entity_difficulty_for_player(strong, player_combat=3) == "Mortel"
