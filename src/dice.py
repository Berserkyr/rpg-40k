"""Utility helpers for dice rolls."""

from dataclasses import dataclass
from random import randint
from typing import Tuple


@dataclass(frozen=True)
class DiceResult:
    total: int
    values: Tuple[int, int]

    def is_double(self) -> bool:
        """Return True when both dice rolled the same value."""
        return self.values[0] == self.values[1]


def roll_2d6() -> DiceResult:
    """Roll two six-sided dice and return both individual values and the sum."""
    first = randint(1, 6)
    second = randint(1, 6)
    return DiceResult(total=first + second, values=(first, second))


def format_roll(result: DiceResult) -> str:
    """Return a short human readable representation of a DiceResult."""
    flag = " (double)" if result.is_double() else ""
    return f"2d6 -> {result.values[0]} + {result.values[1]} = {result.total}{flag}"
