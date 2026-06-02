from src.dice import roll_2d6


def test_roll_2d6_range():
    result = roll_2d6()
    assert 2 <= result.total <= 12
    assert all(1 <= value <= 6 for value in result.values)
