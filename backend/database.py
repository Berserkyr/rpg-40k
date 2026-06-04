"""Couche SQLite minimale pour les utilisateurs et les traces de session."""
from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "rpg40k.sqlite3"


def utc_now() -> str:
    """Retourne un horodatage UTC ISO-8601."""
    return datetime.now(timezone.utc).isoformat()


def normalize_user_id(user_id: str | None) -> str:
    """Produit un identifiant utilisateur sûr pour les chemins et la BDD."""
    raw = (user_id or "default").strip().lower()
    normalized = re.sub(r"[^a-z0-9_-]+", "-", raw).strip("-")
    return normalized or "default"


def connect() -> sqlite3.Connection:
    """Ouvre une connexion SQLite avec dictionnaires de colonnes."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    """Crée le schéma SQLite si nécessaire."""
    with connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                display_name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_seen_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS session_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                detail TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )
        connection.commit()


def ensure_user(user_id: str | None, display_name: str | None = None) -> dict[str, Any]:
    """Crée ou met à jour un utilisateur puis le retourne."""
    init_db()
    safe_id = normalize_user_id(user_id)
    now = utc_now()
    name = (display_name or safe_id).strip() or safe_id
    with connect() as connection:
        existing = connection.execute("SELECT * FROM users WHERE id = ?", (safe_id,)).fetchone()
        if existing:
            connection.execute(
                "UPDATE users SET last_seen_at = ?, display_name = COALESCE(NULLIF(?, ''), display_name) WHERE id = ?",
                (now, display_name or "", safe_id),
            )
        else:
            connection.execute(
                "INSERT INTO users (id, display_name, created_at, last_seen_at) VALUES (?, ?, ?, ?)",
                (safe_id, name, now, now),
            )
        connection.commit()
        row = connection.execute("SELECT * FROM users WHERE id = ?", (safe_id,)).fetchone()
    return dict(row)


def list_users() -> list[dict[str, Any]]:
    """Liste les utilisateurs connus."""
    init_db()
    with connect() as connection:
        rows = connection.execute(
            "SELECT id, display_name, created_at, last_seen_at FROM users ORDER BY last_seen_at DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def record_event(user_id: str | None, event_type: str, detail: str | None = None) -> None:
    """Enregistre un événement applicatif simple pour audit/debug."""
    user = ensure_user(user_id)
    with connect() as connection:
        connection.execute(
            "INSERT INTO session_events (user_id, event_type, detail, created_at) VALUES (?, ?, ?, ?)",
            (user["id"], event_type, detail, utc_now()),
        )
        connection.commit()
