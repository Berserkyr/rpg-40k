"""Prompt building helpers."""

from pathlib import Path

from .state import CharacterState


def build_system_prompt(prompt_path: str | Path, state: CharacterState) -> str:
    """Combine the base prompt with character data."""
    template = Path(prompt_path).read_text(encoding="utf-8")
    sheet_block = state.to_prompt_fragment()
    stitched = template + "\n\n" + "Etat initial du survivant :\n" + sheet_block
    return stitched
