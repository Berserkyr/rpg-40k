from pathlib import Path

import json
import yaml

from src.state import CharacterState


def test_state_from_file(tmp_path: Path):
    data = """
name: Test
role: Courrier
origin: Niveau 12
objective: Survivre
attributes:
  sang_froid: 3
resources:
  rations: 2
tracks:
  blessures: Indemne
notes:
  - Garder la foi
"""
    file_path = tmp_path / "sheet.yaml"
    file_path.write_text(data, encoding="utf-8")

    state = CharacterState.from_file(file_path)

    assert state.name == "Test"
    assert state.attributes["sang_froid"] == 3
    assert "rations" in state.resources
    assert state.tracks["blessures"] == "Indemne"
    assert state.notes == ["Garder la foi"]
    assert state.source_path == file_path

    fragment = state.to_prompt_fragment()
    assert "Nom=Test" in fragment
    assert "Attributs" in fragment


def test_state_save_snapshot(tmp_path: Path):
    state = CharacterState(
        name="Test",
        role="Rescapee",
        origin="Bloc 7",
        objective="Survivre",
        attributes={"sang_froid": 3},
        resources={"rations": 1},
        tracks={"blessures": "Indemne"},
        notes=["Tenir bon"],
    )

    yaml_path = state.save_snapshot(tmp_path, 1, fmt="yaml")
    data_yaml = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    assert data_yaml["name"] == "Test"
    assert yaml_path.name == "scene_001.yaml"

    json_path = state.save_snapshot(tmp_path, 2, fmt="json")
    data_json = json.loads(json_path.read_text(encoding="utf-8"))
    assert data_json["notes"] == ["Tenir bon"]
    assert json_path.name == "scene_002.json"
