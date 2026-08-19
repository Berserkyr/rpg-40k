"""Cohérence du journal des versions (C4.3.2).

La version était écrite en dur dans `backend/api.py` et avait dérivé : le code
annonçait `1.0.0` alors que le journal en était à `1.2.0`. Une anomalie
remontée par un joueur ne pouvait donc pas être rattachée de façon fiable à une
version précise.

Ces tests empêchent la dérive de se reproduire : le fichier `VERSION`, la
version exposée par l'API et l'entrée la plus récente de `CHANGELOG.md` doivent
rester alignés.
"""
from __future__ import annotations

import re
from pathlib import Path

from fastapi.testclient import TestClient

from backend.api import app
from backend.version import CHANGELOG_FILE, VERSION_FILE, get_version, latest_changelog_version

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


def test_le_fichier_version_existe() -> None:
    assert VERSION_FILE.is_file(), "le fichier VERSION est la source unique de verite"


def test_la_version_respecte_le_versionnage_semantique() -> None:
    version = get_version()
    assert SEMVER.match(version), f"version non conforme au format x.y.z : {version!r}"


def test_l_api_expose_la_version_du_fichier() -> None:
    """Sans cela, /api/health identifie mal la version reellement deployee."""
    client = TestClient(app)
    assert client.get("/api/health").json()["version"] == get_version()


def test_la_version_correspond_au_journal() -> None:
    """Toute version publiee doit figurer en tete du journal des versions."""
    assert latest_changelog_version() == get_version(), (
        "le fichier VERSION et la derniere entree publiee de CHANGELOG.md "
        "doivent designer la meme version"
    )


def test_le_journal_documente_la_version_courante() -> None:
    """L'entree courante doit decrire les evolutions, pas seulement exister."""
    contenu = CHANGELOG_FILE.read_text(encoding="utf-8")
    version = get_version()
    debut = contenu.find(f"## [{version}]")
    assert debut != -1, f"aucune section pour la version {version}"

    suivante = contenu.find("\n## [", debut + 1)
    section = contenu[debut : suivante if suivante != -1 else len(contenu)]

    assert len(section) > 500, "l'entree de version est trop succincte pour etre utile"
    # Une version de maintenance doit au minimum tracer ce qu'elle corrige.
    assert "### Corrigé" in section, "les correctifs deployes doivent etre documentes"


def test_le_journal_reference_l_anomalie_traitee() -> None:
    """Le correctif deploye doit etre relie a sa fiche de consignation."""
    contenu = CHANGELOG_FILE.read_text(encoding="utf-8")
    assert "ANO-2026-001" in contenu


def test_le_mode_debug_est_desactive_par_defaut() -> None:
    """Recommandation R6 : aucune trace d'execution ne doit fuiter en production."""
    assert app.debug is False, (
        "le mode debug doit etre pilote par API_DEBUG et desactive par defaut"
    )
