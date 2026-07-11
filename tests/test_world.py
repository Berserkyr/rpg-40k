from src.world import PointOfInterest, ThreatLevel, WorldMap, Zone, ZoneStatus, ZoneType


def make_zone(zone_id, name, *, connections=None, status=ZoneStatus.INCONNU):
    return Zone(
        id=zone_id,
        name=name,
        description=f"Description {name}",
        zone_type=ZoneType.HABITATION,
        threat_level=ThreatLevel.INCERTAIN,
        status=status,
        connections=connections or [],
    )


def test_discover_zone_only_adds_known_zone_once():
    world = WorldMap()
    world.add_zone(make_zone("hab", "Bloc d'habitation"))

    assert world.discover_zone("hab") is True
    assert world.discover_zone("hab") is False
    assert world.discover_zone("unknown") is False
    assert world.discovered_zones == ["hab"]


def test_travel_rejects_unknown_unconnected_and_blocked_targets():
    world = WorldMap(current_zone_id="start")
    world.add_zone(make_zone("start", "Départ", connections=["blocked"]))
    world.add_zone(make_zone("blocked", "Secteur bloqué", status=ZoneStatus.BLOQUE))
    world.add_zone(make_zone("far", "Zone lointaine"))

    assert world.can_travel_to("missing") == (False, "Zone cible inconnue")
    assert world.can_travel_to("far") == (False, "Pas de chemin direct vers Zone lointaine")
    assert world.can_travel_to("blocked") == (False, "Secteur bloqué est bloquee")


def test_successful_travel_updates_current_zone_visit_count_and_discovery(monkeypatch):
    world = WorldMap(current_zone_id="start")
    world.add_zone(make_zone("start", "Départ", connections=["target"]))
    target = make_zone("target", "Sanctuaire", connections=["start"])
    world.add_zone(target)

    monkeypatch.setattr("src.world.random.randint", lambda _a, _b: 100)

    success, message, event = world.travel_to("target", current_scene=7)

    assert success is True
    assert message == "Arrive a Sanctuaire"
    assert event is None
    assert world.current_zone_id == "target"
    assert world.discovered_zones == ["target"]
    assert target.status == ZoneStatus.EXPLORE
    assert target.times_visited == 1
    assert target.last_visited_scene == 7


def test_world_round_trip_serialization_preserves_points_of_interest():
    zone = make_zone("market", "Marché noir", connections=["start"], status=ZoneStatus.EXPLORE)
    zone.points_of_interest.append(
        PointOfInterest(
            id="stall",
            name="Étal secret",
            description="Un marchand cache du matériel.",
            discovered=True,
            visited=True,
            loot_available=False,
            quest_related=True,
            special_event="deal",
        )
    )
    world = WorldMap(zones={"market": zone}, current_zone_id="market", discovered_zones=["market"])

    restored = WorldMap.from_dict(world.to_dict())

    restored_zone = restored.get_zone("market")
    assert restored.current_zone_id == "market"
    assert restored.discovered_zones == ["market"]
    assert restored_zone is not None
    assert restored_zone.points_of_interest[0].id == "stall"
    assert restored_zone.points_of_interest[0].visited is True
    assert restored_zone.points_of_interest[0].special_event == "deal"
