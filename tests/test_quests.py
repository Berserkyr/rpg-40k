from src.quests import Quest, QuestLog, QuestObjective, QuestReward, QuestStatus, QuestType


def make_quest(**overrides):
    data = {
        "id": "q1",
        "title": "Trouver le signal",
        "description": "Localiser une transmission vox.",
        "quest_type": QuestType.PRINCIPALE,
        "status": QuestStatus.DISPONIBLE,
        "objectives": [
            QuestObjective(id="reach", description="Atteindre le relais"),
            QuestObjective(id="scan", description="Scanner la fréquence", optional=True),
        ],
        "reward": QuestReward(xp=50, credits=10, items=["vox_part"]),
    }
    data.update(overrides)
    return Quest(**data)


def test_quest_progress_ignores_optional_objectives_for_completion():
    quest = make_quest()

    assert quest.progress_percentage() == 0
    assert quest.is_complete() is False

    quest.objectives[0].completed = True

    assert quest.progress_percentage() == 100.0
    assert quest.is_complete() is True


def test_time_limited_quest_expires_when_timer_reaches_limit():
    quest = make_quest(status=QuestStatus.ACTIVE, time_limit=2)

    assert quest.advance_time() is False
    assert quest.scenes_elapsed == 1
    assert quest.status == QuestStatus.ACTIVE

    assert quest.advance_time() is True
    assert quest.status == QuestStatus.EXPIREE


def test_quest_log_accept_complete_and_reward_flow():
    quest = make_quest(status=QuestStatus.DISPONIBLE, completion_text="Signal sécurisé.")
    log = QuestLog(quests={quest.id: quest})

    accepted, accept_message = log.accept_quest("q1")
    assert accepted is True
    assert "acceptee" in accept_message
    assert quest.status == QuestStatus.ACTIVE

    completed_objective, objective_message = log.complete_objective("q1", "reach")
    assert completed_objective is True
    assert "Tous les objectifs" in objective_message

    completed, message, reward = log.complete_quest("q1")
    assert completed is True
    assert message == "Signal sécurisé."
    assert reward is quest.reward
    assert quest.status == QuestStatus.COMPLETEE
    assert log.completed_quest_ids == ["q1"]


def test_quest_log_updates_kill_count_and_marks_objective_complete():
    objective = QuestObjective(
        id="kill_gaunts",
        description="Éliminer les gaunts",
        target_kill_count=3,
        current_kill_count=1,
    )
    quest = make_quest(status=QuestStatus.ACTIVE, objectives=[objective])
    log = QuestLog(quests={quest.id: quest})

    success, message = log.update_kill_count("q1", "kill_gaunts", count=2)

    assert success is True
    assert message == "Progres: 3/3"
    assert objective.completed is True
    assert "Objectif complete" in quest.journal_entries[-1]


def test_quest_log_round_trip_preserves_status_and_history():
    quest = make_quest(status=QuestStatus.ECHOUEE)
    quest.add_journal_entry("Trop tard.")
    log = QuestLog(quests={quest.id: quest}, failed_quest_ids=[quest.id])

    restored = QuestLog.from_dict(log.to_dict())

    restored_quest = restored.get_quest("q1")
    assert restored.failed_quest_ids == ["q1"]
    assert restored_quest is not None
    assert restored_quest.status == QuestStatus.ECHOUEE
    assert restored_quest.journal_entries == ["Trop tard."]
    assert restored_quest.reward.xp == 50
