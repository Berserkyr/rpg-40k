"""Character state management."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

import json
import yaml


@dataclass
class CharacterState:
    name: str
    role: str
    origin: str
    objective: str
    attributes: Dict[str, int]
    resources: Dict[str, int]
    tracks: Dict[str, str | int]
    notes: List[str] = field(default_factory=list)
    source_path: Path | None = None

    @classmethod
    def from_file(cls, path: str | Path) -> "CharacterState":
        file_path = Path(path)
        data = yaml.safe_load(file_path.read_text(encoding="utf-8"))
        return cls(
            name=data["name"],
            role=data["role"],
            origin=data.get("origin", ""),
            objective=data.get("objective", ""),
            attributes=data.get("attributes", {}),
            resources=data.get("resources", {}),
            tracks=data.get("tracks", {}),
            notes=data.get("notes", []),
            source_path=file_path,
        )

    def as_markdown(self) -> str:
        """Return a markdown description of the current sheet."""
        attrs = "\n".join(f"- {k.replace('_', ' ').title()}: {v}" for k, v in self.attributes.items())
        res = "\n".join(f"- {k.replace('_', ' ').title()}: {v}" for k, v in self.resources.items())
        tracks = "\n".join(f"- {k.title()}: {v}" for k, v in self.tracks.items())
        notes = "\n".join(f"- {line}" for line in self.notes) or "- Aucune note"
        return (
            f"### Profil\n"
            f"- Nom : {self.name}\n"
            f"- Role : {self.role}\n"
            f"- Origine : {self.origin}\n"
            f"- Objectif : {self.objective}\n\n"
            f"### Attributs\n{attrs}\n\n"
            f"### Ressources\n{res}\n\n"
            f"### Jauges\n{tracks}\n\n"
            f"### Notes\n{notes}\n"
        )

    def to_prompt_fragment(self) -> str:
        """Return a compact text block for injecting into the system prompt."""
        attributes = ", ".join(f"{k}:{v}" for k, v in self.attributes.items())
        resources = ", ".join(f"{k}:{v}" for k, v in self.resources.items())
        tracks = ", ".join(f"{k}:{v}" for k, v in self.tracks.items())
        notes = " | ".join(self.notes)
        return (
            f"Nom={self.name}; Role={self.role}; Origine={self.origin}; Objectif={self.objective}. "
            f"Attributs[{attributes}]. Ressources[{resources}]. Jauges[{tracks}]. Notes[{notes}]."
        )

    # Persistence helpers -------------------------------------------------

    def to_dict(self) -> Dict[str, object]:
        """Return raw data structure for serialization."""
        return {
            "name": self.name,
            "role": self.role,
            "origin": self.origin,
            "objective": self.objective,
            "attributes": self.attributes,
            "resources": self.resources,
            "tracks": self.tracks,
            "notes": self.notes,
        }

    def save(self, path: str | Path, fmt: str | None = None) -> Path:
        """Serialize the state to disk in yaml or json format."""

        target = Path(path)
        fmt = (fmt or target.suffix.lstrip(".") or "yaml").lower()
        data = self.to_dict()
        target.parent.mkdir(parents=True, exist_ok=True)

        if fmt == "json":
            target.write_text(json.dumps(data, ensure_ascii=True, indent=2), encoding="utf-8")
        elif fmt == "yaml":
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        else:
            raise ValueError(f"Format non supporte: {fmt}")

        return target

    def save_snapshot(self, directory: str | Path, scene_index: int, fmt: str = "yaml") -> Path:
        """Save a numbered snapshot (scene) into the specified directory."""

        suffix = ".json" if fmt == "json" else ".yaml"
        directory_path = Path(directory)
        directory_path.mkdir(parents=True, exist_ok=True)
        filename = directory_path / f"scene_{scene_index:03d}{suffix}"
        return self.save(filename, fmt=fmt)

    # Dynamic state updates -----------------------------------------------

    def update_track(self, track_name: str, value: str | int) -> None:
        """Update a track (blessures, stress, corruption)."""
        self.tracks[track_name] = value

    def update_resource(self, resource_name: str, delta: int) -> None:
        """Adjust a resource by delta (positive or negative)."""
        current = self.resources.get(resource_name, 0)
        self.resources[resource_name] = max(0, current + delta)

    def set_resource(self, resource_name: str, value: int) -> None:
        """Set a resource to an absolute value."""
        self.resources[resource_name] = max(0, value)

    def apply_updates_from_text(self, text: str) -> List[str]:
        """
        Parse MJ response for state update markers and apply them.
        
        Expected format in MJ text:
        [ETAT: blessures=Erafle, stress=2, rations=-1, munitions=-1]
        
        Returns list of changes applied.
        """
        import re
        
        changes = []
        pattern = r'\[ETAT:\s*([^\]]+)\]'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if not match:
            return changes
        
        updates_str = match.group(1)
        for part in updates_str.split(','):
            part = part.strip()
            if '=' not in part:
                continue
            
            key, value = part.split('=', 1)
            key = key.strip().lower()
            value = value.strip()
            
            # Handle tracks (blessures, stress, corruption)
            if key in ('blessures', 'stress', 'corruption'):
                if key == 'blessures':
                    self.tracks['blessures'] = value
                    changes.append(f"Blessures -> {value}")
                else:
                    try:
                        self.tracks[key] = int(value)
                        changes.append(f"{key.title()} -> {value}")
                    except ValueError:
                        self.tracks[key] = value
                        changes.append(f"{key.title()} -> {value}")
            
            # Handle resources with delta or absolute
            elif key in ('rations', 'acces_vox', 'contacts', 'munitions'):
                if value.startswith(('+', '-')):
                    delta = int(value)
                    self.update_resource(key, delta)
                    changes.append(f"{key} {value}")
                else:
                    self.set_resource(key, int(value))
                    changes.append(f"{key} = {value}")
        
        return changes
