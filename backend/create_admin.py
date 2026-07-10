"""Crée ou promeut un compte administrateur.

Usage :
    python -m backend.create_admin <username> <password>

Ce script sert à disposer d'un compte avec le rôle "admin" pour tester
les routes protégées par rôle (ex. GET /api/users).
"""
from __future__ import annotations

import sys

from backend.auth import ROLE_ADMIN, hash_password
from backend.database import create_account, get_account, init_db, normalize_user_id


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python -m backend.create_admin <username> <password>")
        return 1

    username = normalize_user_id(sys.argv[1])
    password = sys.argv[2]
    init_db()

    existing = get_account(username)
    digest = hash_password(password)

    if existing and existing.get("password_hash"):
        # Compte déjà existant : on force le rôle admin en réécrivant le hash.
        import sqlite3
        from backend.database import DATABASE_PATH

        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.execute(
                "UPDATE users SET password_hash = ?, role = ? WHERE id = ?",
                (digest, ROLE_ADMIN, username),
            )
            conn.commit()
        print(f"Compte '{username}' promu administrateur.")
    else:
        create_account(username, digest, username, role=ROLE_ADMIN)
        print(f"Compte administrateur '{username}' créé.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
