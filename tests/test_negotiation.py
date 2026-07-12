"""Tests du systeme de negociation (src/negotiation.py)."""

from src.negotiation import (
    NegotiationApproach,
    attempt_negotiation,
    is_negotiable,
    approach_from_str,
)


def test_tyranide_non_negociable():
    assert is_negotiable("tyranide") is False
    out = attempt_negotiation(
        NegotiationApproach.PERSUASION, modifier=10,
        threat_id="standard", faction_id="tyranide",
    )
    assert out.outcome == "impossible"
    assert out.ends_combat is False


def test_culte_negociable():
    assert is_negotiable("culte_genestealer") is True


def test_grande_reussite_termine_le_combat():
    # Modificateur enorme -> reussite garantie quelle que soit la valeur des des.
    out = attempt_negotiation(
        NegotiationApproach.PERSUASION, modifier=20,
        threat_id="sbire", faction_id="culte_genestealer",
    )
    assert out.outcome == "success"
    assert out.ends_combat is True


def test_persuasion_forte_peut_recruter():
    out = attempt_negotiation(
        NegotiationApproach.PERSUASION, modifier=20,
        threat_id="sbire", faction_id="culte_genestealer",
    )
    assert out.can_recruit is True


def test_echec_rend_ennemi_enrage():
    # Modificateur tres negatif -> echec garanti.
    out = attempt_negotiation(
        NegotiationApproach.INTIMIDATION, modifier=-20,
        threat_id="boss", faction_id="culte_genestealer",
    )
    assert out.outcome == "fail"
    assert out.condition == "enrage"
    assert out.condition_turns > 0


def test_intimidation_plus_facile_sur_sbire():
    # A modificateur egal, un sbire est plus facile a intimider qu'un boss.
    sbire = attempt_negotiation(
        NegotiationApproach.INTIMIDATION, modifier=0,
        threat_id="sbire", faction_id="culte_genestealer",
    )
    boss = attempt_negotiation(
        NegotiationApproach.INTIMIDATION, modifier=0,
        threat_id="boss", faction_id="culte_genestealer",
    )
    assert sbire.difficulty < boss.difficulty


def test_approach_from_str():
    assert approach_from_str("persuasion") == NegotiationApproach.PERSUASION
    assert approach_from_str("intimidation") == NegotiationApproach.INTIMIDATION
    assert approach_from_str("inconnu") is None
