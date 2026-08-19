"""Source unique de vérité pour la version du logiciel (C4.3.2).

La version était auparavant écrite en dur dans `backend/api.py`, ce qui l'a
laissée à `1.0.0` alors que le journal des versions annonçait `1.2.0` : la
route `/api/health` identifiait donc incorrectement la version en service, et
une anomalie remontée par un joueur ne pouvait pas être rattachée de façon
fiable à une version précise.

La version est désormais lue depuis le fichier `VERSION` à la racine du dépôt,
seul endroit à modifier lors d'une publication. Un test automatisé vérifie sa
cohérence avec `CHANGELOG.md`.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = REPO_ROOT / "VERSION"
CHANGELOG_FILE = REPO_ROOT / "CHANGELOG.md"

# Repli utilisé uniquement si le fichier VERSION est absent (déploiement
# partiel, exécution depuis une archive). Volontairement identifiable.
_FALLBACK = "0.0.0-inconnue"


def get_version() -> str:
    """Retourne la version courante du logiciel."""
    try:
        version = VERSION_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return _FALLBACK
    return version or _FALLBACK


def latest_changelog_version() -> str | None:
    """Retourne le numéro de la version publiée la plus récente du journal.

    Les sections non publiées (`## [Non publié]`) sont ignorées : seule une
    version réellement numérotée est retenue.
    """
    try:
        contenu = CHANGELOG_FILE.read_text(encoding="utf-8")
    except OSError:
        return None

    for ligne in contenu.splitlines():
        correspondance = re.match(r"^##\s*\[([0-9][^\]]*)\]", ligne.strip())
        if correspondance:
            return correspondance.group(1)
    return None


__version__ = get_version()
