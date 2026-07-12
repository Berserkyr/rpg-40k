from src.progression import ProgressionState, Skill, SkillCategory


def make_skill(**overrides):
    data = {
        "id": "skill-test",
        "name": "Compétence test",
        "description": "Une compétence de test.",
        "category": SkillCategory.TECHNIQUE,
        "xp_cost": 50,
        "level_required": 1,
        "prerequisites": [],
    }
    data.update(overrides)
    return Skill(**data)


def test_add_xp_can_level_up_multiple_times_and_keeps_overflow():
    state = ProgressionState(level=1, current_xp=0)

    messages = state.add_xp(400)

    assert state.level == 3
    assert state.current_xp == 25
    assert state.total_xp_earned == 400
    assert state.attribute_points_available == 2
    assert state.skill_points_available == 2
    assert messages == [
        "NIVEAU 2 ATTEINT! +1 point d'attribut, +1 point de competence.",
        "NIVEAU 3 ATTEINT! +1 point d'attribut, +1 point de competence.",
    ]


def test_unlock_skill_spends_xp_and_prevents_duplicate_unlock():
    state = ProgressionState(level=2, current_xp=100, skills_unlocked=["base"])
    skill = make_skill(id="advanced", xp_cost=75, level_required=2, prerequisites=["base"])

    success, message = state.unlock_skill(skill)

    assert success is True
    assert "debloquee" in message
    assert state.current_xp == 25
    assert state.skills_unlocked == ["base", "advanced"]

    success, reason = state.unlock_skill(skill)
    assert success is False
    assert reason == "Competence deja acquise"


def test_can_unlock_skill_reports_missing_level_xp_and_prerequisite():
    low_level = ProgressionState(level=1, current_xp=500)
    high_level_skill = make_skill(level_required=3)
    assert low_level.can_unlock_skill(high_level_skill) == (
        False,
        "Niveau 3 requis (actuel: 1)",
    )

    low_xp = ProgressionState(level=3, current_xp=10)
    expensive_skill = make_skill(xp_cost=100)
    assert low_xp.can_unlock_skill(expensive_skill) == (False, "XP insuffisant (10/100)")

    missing_prereq = ProgressionState(level=3, current_xp=200)
    prereq_skill = make_skill(prerequisites=["base"])
    assert missing_prereq.can_unlock_skill(prereq_skill) == (
        False,
        "Prerequis manquant: base",
    )


def test_progression_state_round_trip_keeps_unlocked_skills():
    state = ProgressionState(
        level=4,
        current_xp=80,
        total_xp_earned=780,
        skills_unlocked=["combat_base", "endurci"],
        attribute_points_available=2,
    )

    restored = ProgressionState.from_dict(state.to_dict())

    assert restored.level == 4
    assert restored.current_xp == 80
    assert restored.total_xp_earned == 780
    assert restored.skills_unlocked == ["combat_base", "endurci"]
    assert restored.attribute_points_available == 2
