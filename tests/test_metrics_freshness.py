"""Tests de non-regression de l'anomalie ANO-2026-004.

Les jauges `rpg40k_ready` et `rpg40k_dependency_up` n'etaient alimentees que
par la route `/api/health/ready`. Or Prometheus interroge `/api/metrics`, et
jamais la sonde d'aptitude. Consequence : au demarrage, `rpg40k_ready` valait 0
(valeur par defaut d'une jauge) et les series `dependency_up` n'existaient pas
encore. L'alerte critique `ServiceNonPret` se serait donc declenchee a chaque
redemarrage sur un service parfaitement sain --- exactement le genre de faux
positif qui fait cesser de croire aux alertes.

Ces tests echouent sur le code anterieur au correctif.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

import backend.api as api
from backend import monitoring


def _valeur(payload: str, metrique: str, **labels: str) -> float | None:
    """Retourne la valeur d'une serie, ou None si elle est absente."""
    if labels:
        rendu = ",".join(f'{k}="{labels[k]}"' for k in sorted(labels))
        cible = f"{metrique}{{{rendu}}}"
    else:
        cible = metrique
    for ligne in payload.splitlines():
        if ligne.startswith("#"):
            continue
        nom, _, valeur = ligne.rpartition(" ")
        if nom.strip() == cible:
            return float(valeur)
    return None


@pytest.fixture()
def client_neuf() -> TestClient:
    """Client dont les jauges de dependance sont remises a leur etat initial.

    Reproduit la situation d'un processus qui vient de demarrer et que
    Prometheus interroge avant tout appel a la sonde d'aptitude.
    """
    monitoring.READINESS.set(0)
    return TestClient(api.app)


def test_le_scrape_alimente_la_jauge_d_aptitude(client_neuf: TestClient) -> None:
    """Sans appel prealable a /api/health/ready, /api/metrics doit dire « pret »."""
    payload = client_neuf.get("/api/metrics").text
    assert _valeur(payload, "rpg40k_ready") == 1.0, (
        "rpg40k_ready doit etre rafraichie au moment du scrape, sinon l'alerte "
        "ServiceNonPret se declenche sur un service sain"
    )


def test_le_scrape_expose_chaque_dependance(client_neuf: TestClient) -> None:
    """Les series dependency_up doivent exister des le premier scrape."""
    payload = client_neuf.get("/api/metrics").text
    for dependance in ("database", "character_sheet", "prompt_file", "save_dir"):
        valeur = _valeur(payload, "rpg40k_dependency_up", dependency=dependance)
        assert valeur is not None, (
            f"la serie dependency_up[{dependance}] est absente : la regle "
            "DependanceIndisponible n'aurait aucune donnee a evaluer"
        )
        assert valeur == 1.0


def test_le_scrape_reste_coherent_avec_la_sonde_d_aptitude(client_neuf: TestClient) -> None:
    """Les deux routes doivent rapporter le meme etat."""
    etat_route = client_neuf.get("/api/health/ready").json()["status"]
    valeur_scrape = _valeur(client_neuf.get("/api/metrics").text, "rpg40k_ready")
    assert (etat_route == "ready") == (valeur_scrape == 1.0)
