"""Tests de non-regression de l'anomalie ANO-2026-001.

Un marqueur `[ETAT: ...]` produit par le MJ avec une valeur non numerique sur
une ressource provoquait une `ValueError` non interceptee. Levee au sein du
generateur SSE **apres** l'envoi de la narration mais **avant** `session.save()`,
elle interrompait le flux sans evenement `done` et faisait perdre la
progression de la scene.

Ces tests echouent sur le code anterieur au correctif.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

import backend.api as api
from src.state import CharacterState

FICHE = Path("character_sheet.yaml")


@pytest.fixture()
def personnage() -> CharacterState:
    return CharacterState.from_file(FICHE)


# ---------------------------------------------------------------------------
# Cause racine : robustesse du parseur
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "valeur",
    ["aucune", "quelques-unes", "+", "-", "", "beaucoup", "3 rations", "N/A"],
)
def test_valeur_de_ressource_non_numerique_ne_leve_pas(personnage, valeur) -> None:
    """Aucune valeur textuelle ne doit produire d'exception."""
    resultat = personnage.apply_updates_from_text(f"Scene. [ETAT: rations={valeur}]")
    assert isinstance(resultat, list)


def test_le_marqueur_invalide_est_consigne(personnage) -> None:
    """Un marqueur rejete doit rester tracable pour la supervision."""
    personnage.apply_updates_from_text("Scene. [ETAT: rations=aucune]")
    assert personnage.rejected_updates == ["rations=aucune"]


def test_la_ressource_reste_inchangee_si_la_valeur_est_invalide(personnage) -> None:
    """Rejeter un marqueur ne doit jamais corrompre l'etat existant."""
    avant = personnage.resources["rations"]
    personnage.apply_updates_from_text("Scene. [ETAT: rations=aucune]")
    assert personnage.resources["rations"] == avant


def test_les_marqueurs_valides_sont_appliques_malgre_un_voisin_invalide(personnage) -> None:
    """Un marqueur mal forme ne doit pas annuler les marqueurs corrects."""
    avant = personnage.resources["rations"]  # 3 au depart : pas d'ecretage
    changements = personnage.apply_updates_from_text(
        "Combat. [ETAT: munitions=plus rien, rations=-1]"
    )
    assert personnage.resources["rations"] == avant - 1
    assert any("rations" in c for c in changements)
    assert personnage.rejected_updates == ["munitions=plus rien"]


def test_les_ressources_restent_ecretees_a_zero(personnage) -> None:
    """Regle de jeu existante : une ressource ne descend jamais sous zero.

    Verifiee ici pour garantir que le correctif ne l'a pas alteree.
    """
    personnage.apply_updates_from_text("Fusillade. [ETAT: munitions=-99]")
    assert personnage.resources["munitions"] == 0


def test_la_liste_des_rejets_est_reinitialisee_a_chaque_parsing(personnage) -> None:
    """Les rejets ne doivent pas s'accumuler d'une scene a l'autre."""
    personnage.apply_updates_from_text("Scene 1. [ETAT: rations=aucune]")
    assert len(personnage.rejected_updates) == 1
    personnage.apply_updates_from_text("Scene 2. [ETAT: rations=-1]")
    assert personnage.rejected_updates == []


def test_comportement_nominal_preserve(personnage) -> None:
    """Le correctif ne doit rien changer au fonctionnement normal."""
    avant = personnage.resources["rations"]
    changements = personnage.apply_updates_from_text("Repas. [ETAT: rations=-1, stress=2]")
    assert personnage.resources["rations"] == avant - 1
    assert personnage.tracks["stress"] == 2
    assert changements
    assert personnage.rejected_updates == []


def test_valeur_absolue_toujours_appliquee(personnage) -> None:
    personnage.apply_updates_from_text("Ravitaillement. [ETAT: rations=7]")
    assert personnage.resources["rations"] == 7


# ---------------------------------------------------------------------------
# Impact constate : integrite du flux SSE et de la sauvegarde
# ---------------------------------------------------------------------------
@pytest.fixture()
def client_authentifie() -> TestClient:
    client = TestClient(api.app)
    identifiants = {"username": "joueur-regression", "password": "motdepasse1"}
    client.post("/api/auth/register", json={**identifiants, "display_name": "Regression"})
    token = client.post("/api/auth/login", json=identifiants).json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


def _compter(corps: str, evenement: str) -> int:
    return len([l for l in corps.splitlines() if f'"{evenement}"' in l])


def test_la_scene_se_termine_malgre_un_marqueur_invalide(client_authentifie) -> None:
    """Le flux doit rester complet : c'est le symptome rapporte par le joueur."""
    narration = (
        "Karimus partage ses dernieres provisions avec les survivants.\n"
        "[ETAT: rations=aucune, stress=+1]"
    )
    with patch.object(api, "_offline_gm_text", return_value=narration):
        reponse = client_authentifie.post("/api/chat", json={"message": "Je partage"})

    assert reponse.status_code == 200
    assert _compter(reponse.text, "token") > 0, "la narration doit parvenir au joueur"
    assert _compter(reponse.text, "done") == 1, (
        "l'evenement de cloture doit etre emis, sans quoi le client reste en attente"
    )


def test_la_sauvegarde_est_effectuee_malgre_un_marqueur_invalide(client_authentifie) -> None:
    """La progression de la scene ne doit pas etre perdue."""
    narration = "Le bloc s'effondre.\n[ETAT: munitions=plus rien]"
    with patch.object(api, "_offline_gm_text", return_value=narration):
        with patch.object(api.Session, "save", autospec=True) as sauvegarde:
            client_authentifie.post("/api/chat", json={"message": "Je fuis"})

    assert sauvegarde.called, "session.save() doit etre atteint malgre le marqueur invalide"


def test_la_sonde_de_supervision_compte_les_marqueurs_rejetes(client_authentifie) -> None:
    """Le phenomene doit devenir mesurable (lien avec C4.1.2)."""
    avant = client_authentifie.get("/api/metrics").text
    depart = 0.0
    for ligne in avant.splitlines():
        if ligne.startswith("rpg40k_state_markers_rejected_total "):
            depart = float(ligne.rsplit(" ", 1)[1])

    with patch.object(api, "_offline_gm_text", return_value="Scene. [ETAT: rations=aucune]"):
        client_authentifie.post("/api/chat", json={"message": "test sonde"})

    apres = client_authentifie.get("/api/metrics").text
    arrivee = 0.0
    for ligne in apres.splitlines():
        if ligne.startswith("rpg40k_state_markers_rejected_total "):
            arrivee = float(ligne.rsplit(" ", 1)[1])

    assert arrivee == depart + 1
