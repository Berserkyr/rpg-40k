"""Tests de non-regression de l'anomalie ANO-2026-002.

`Session.save()` persistait la progression, l'inventaire, les quetes, la carte,
les relations et l'equipe — mais **pas la fiche de personnage**. Celle-ci etait
systematiquement rechargee depuis le modele vierge `character_sheet.yaml`.

Consequence : blessures, stress, ressources et points d'attribut alloues
etaient perdus a chaque redemarrage du serveur, alors que le niveau et
l'inventaire, eux, survivaient. Cette perte **partielle** rendait le symptome
particulierement deroutant pour le joueur.

Ces tests echouent sur le code anterieur au correctif.
"""
from __future__ import annotations

import shutil

import pytest

import backend.api as api
from src.state import CharacterState

UTILISATEUR = "test-persistance-fiche"


@pytest.fixture()
def session_neuve():
    """Fournit une session isolee, nettoyee avant et apres le test."""
    dossier = api._save_dir_for_user(UTILISATEUR)
    shutil.rmtree(dossier, ignore_errors=True)
    api._sessions.pop(UTILISATEUR, None)

    yield lambda: _recharger()

    shutil.rmtree(dossier, ignore_errors=True)
    api._sessions.pop(UTILISATEUR, None)


def _recharger() -> api.Session:
    """Simule un redemarrage du serveur : les sessions en memoire disparaissent."""
    api._sessions.pop(UTILISATEUR, None)
    return api.get_session(UTILISATEUR)


# ---------------------------------------------------------------------------
# Serialisation de la fiche
# ---------------------------------------------------------------------------
def test_la_fiche_sait_se_reconstruire_depuis_un_dictionnaire() -> None:
    """`to_dict` existait sans `from_dict` : la fiche ne pouvait pas etre relue."""
    origine = CharacterState.from_file("character_sheet.yaml")
    origine.resources["rations"] = 7
    origine.tracks["blessures"] = "Grave"

    copie = CharacterState.from_dict(origine.to_dict())

    assert copie.name == origine.name
    assert copie.resources["rations"] == 7
    assert copie.tracks["blessures"] == "Grave"


def test_from_dict_tolere_un_dictionnaire_vide() -> None:
    """Une sauvegarde tronquee ne doit pas faire echouer le chargement."""
    fiche = CharacterState.from_dict({})
    assert fiche.attributes == {}
    assert fiche.resources == {}


# ---------------------------------------------------------------------------
# Persistance effective au fil des sessions
# ---------------------------------------------------------------------------
def test_les_ressources_survivent_a_un_redemarrage(session_neuve) -> None:
    session = api.get_session(UTILISATEUR)
    session.character.apply_updates_from_text("[ETAT: rations=-2, munitions=-1]")
    attendu_rations = session.character.resources["rations"]
    attendu_munitions = session.character.resources["munitions"]
    session.save()

    rechargee = session_neuve()

    assert rechargee.character.resources["rations"] == attendu_rations
    assert rechargee.character.resources["munitions"] == attendu_munitions


def test_les_blessures_survivent_a_un_redemarrage(session_neuve) -> None:
    """Symptome principal rapporte : le personnage revient indemne."""
    session = api.get_session(UTILISATEUR)
    session.character.apply_updates_from_text("[ETAT: blessures=Grave, stress=4]")
    session.save()

    rechargee = session_neuve()

    assert rechargee.character.tracks["blessures"] == "Grave"
    assert rechargee.character.tracks["stress"] == 4


def test_les_points_d_attribut_alloues_survivent(session_neuve) -> None:
    """Les points depenses a la montee de niveau ne doivent pas etre perdus."""
    session = api.get_session(UTILISATEUR)
    attribut = next(iter(session.character.attributes))
    session.character.attributes[attribut] += 3
    attendu = session.character.attributes[attribut]
    session.save()

    rechargee = session_neuve()

    assert rechargee.character.attributes[attribut] == attendu


def test_fiche_et_progression_restent_coherentes(session_neuve) -> None:
    """Coeur de l'anomalie : une perte partielle est plus deroutante qu'une perte totale."""
    session = api.get_session(UTILISATEUR)
    session.character.apply_updates_from_text("[ETAT: rations=-2, blessures=Grave]")
    session.progression.level = 3
    session.progression.current_xp = 250
    session.save()

    rechargee = session_neuve()

    # La progression survivait deja avant le correctif...
    assert rechargee.progression.level == 3
    assert rechargee.progression.current_xp == 250
    # ...la fiche doit desormais survivre de la meme facon.
    assert rechargee.character.tracks["blessures"] == "Grave"
    assert rechargee.character.resources["rations"] == 1


# ---------------------------------------------------------------------------
# Compatibilite ascendante
# ---------------------------------------------------------------------------
def test_une_sauvegarde_anterieure_reste_chargeable(session_neuve) -> None:
    """Les parties creees avant le correctif n'ont pas de character.yaml."""
    session = api.get_session(UTILISATEUR)
    session.save()
    (session.save_dir / "character.yaml").unlink(missing_ok=True)

    rechargee = session_neuve()

    modele = CharacterState.from_file(api.CHARACTER_FILE)
    assert rechargee.character.name == modele.name
    assert rechargee.character.resources == modele.resources


def test_une_fiche_corrompue_ne_bloque_pas_la_partie(session_neuve) -> None:
    """Un fichier illisible doit provoquer un repli, pas une erreur fatale."""
    session = api.get_session(UTILISATEUR)
    session.save()
    (session.save_dir / "character.yaml").write_text("{[ ceci n'est pas du yaml", encoding="utf-8")

    rechargee = session_neuve()

    assert rechargee.character.name == CharacterState.from_file(api.CHARACTER_FILE).name
