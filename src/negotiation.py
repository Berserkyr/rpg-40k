"""Systeme de negociation - dialogue avec les ennemis avant/pendant le combat.

Permet d'eviter ou d'inflechir un combat par la parole plutot que par les armes.
Trois approches, chacune adossee a un attribut du personnage et a des competences
sociales (voir src/progression.py: negociateur, intimidation, langue_bien_pendue).

Module volontairement pur (aucune dependance FastAPI) pour rester testable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from .dice import roll_2d6, DiceResult


class NegotiationApproach(Enum):
    """Les trois registres de dialogue possibles."""
    PERSUASION = "persuasion"      # convaincre par la raison / l'empathie
    INTIMIDATION = "intimidation"  # forcer le repli par la peur
    MARCHANDAGE = "marchandage"    # proposer un echange (ressources, information)


# Toutes les factions ne peuvent pas negocier. L'esprit-ruche tyranide est un
# organisme collectif sans conscience individuelle: aucun dialogue possible.
# Les cultistes genestealer restent humains (corrompus) et peuvent hesiter.
FACTION_NEGOTIABLE: Dict[str, bool] = {
    "tyranide": False,
    "culte_genestealer": True,
    "culte": True,
}


# Difficulte de base selon le niveau de menace de l'adversaire.
THREAT_DIFFICULTY: Dict[str, int] = {
    "sbire": 6,
    "minion": 6,
    "standard": 8,
    "elite": 10,
    "boss": 12,
}


# Ajustement de difficulte selon l'approche et le niveau de menace.
# L'intimidation fonctionne bien sur les sbires mais se retourne contre un boss.
APPROACH_MODIFIER: Dict[NegotiationApproach, Dict[str, int]] = {
    NegotiationApproach.INTIMIDATION: {"sbire": -2, "minion": -2, "boss": +2},
    NegotiationApproach.PERSUASION: {},
    NegotiationApproach.MARCHANDAGE: {"elite": -1, "boss": -1},
}


@dataclass
class NegotiationOutcome:
    """Resultat d'une tentative de negociation."""
    outcome: str                       # impossible|success|waver|fail
    message: str
    approach: str = ""
    total: int = 0
    difficulty: int = 0
    margin: int = 0
    roll: Optional[DiceResult] = None
    # Effet a appliquer par l'appelant (api.py):
    #   ends_combat  : les ennemis se retirent, combat gagne sans effusion
    #   condition    : condition a appliquer aux ennemis ("aveugle", "enrage"...)
    #   condition_turns : duree de la condition
    ends_combat: bool = False
    condition: Optional[str] = None
    condition_turns: int = 0
    can_recruit: bool = False


def is_negotiable(faction_id: str) -> bool:
    """Indique si une faction accepte le dialogue."""
    return FACTION_NEGOTIABLE.get(faction_id, False)


def _difficulty_for(approach: NegotiationApproach, threat_id: str) -> int:
    base = THREAT_DIFFICULTY.get(threat_id, 8)
    adjust = APPROACH_MODIFIER.get(approach, {}).get(threat_id, 0)
    return base + adjust


def attempt_negotiation(
    approach: NegotiationApproach,
    modifier: int,
    threat_id: str,
    faction_id: str,
) -> NegotiationOutcome:
    """Resout une tentative de negociation.

    Args:
        approach: registre de dialogue choisi.
        modifier: bonus total du personnage (attribut social + competences).
        threat_id: niveau de menace de l'ennemi ("sbire", "standard"...).
        faction_id: faction de l'ennemi (determine la negociabilite).

    Returns:
        NegotiationOutcome decrivant l'issue et l'effet a appliquer.
    """
    if not is_negotiable(faction_id):
        return NegotiationOutcome(
            outcome="impossible",
            approach=approach.value,
            message="L'esprit-ruche ne connait ni peur ni raison. Le dialogue est impossible.",
        )

    difficulty = _difficulty_for(approach, threat_id)
    roll = roll_2d6()
    total = roll.total + modifier
    margin = total - difficulty

    if margin >= 3:
        # Grande reussite: l'ennemi renonce au combat.
        recruit = approach == NegotiationApproach.PERSUASION and margin >= 5
        msg = (
            "Vos mots portent. L'adversaire baisse son arme et se retire."
            if not recruit
            else "Convaincu par votre plaidoyer, l'adversaire accepte meme de vous preter main-forte."
        )
        return NegotiationOutcome(
            outcome="success",
            approach=approach.value,
            total=total, difficulty=difficulty, margin=margin, roll=roll,
            message=msg,
            ends_combat=True,
            can_recruit=recruit,
        )

    if margin >= 0:
        # Reussite partielle: l'ennemi hesite (malus temporaire).
        condition = "aveugle" if approach != NegotiationApproach.INTIMIDATION else "supprime"
        return NegotiationOutcome(
            outcome="waver",
            approach=approach.value,
            total=total, difficulty=difficulty, margin=margin, roll=roll,
            message="L'adversaire hesite, desarconne. Il combat avec moins d'assurance.",
            condition=condition,
            condition_turns=2,
        )

    # Echec: la tentative attise l'hostilite.
    return NegotiationOutcome(
        outcome="fail",
        approach=approach.value,
        total=total, difficulty=difficulty, margin=margin, roll=roll,
        message="Votre approche echoue et provoque la fureur de l'adversaire.",
        condition="enrage",
        condition_turns=2,
    )


def approach_from_str(value: str) -> Optional[NegotiationApproach]:
    """Convertit une chaine en NegotiationApproach (ou None si invalide)."""
    try:
        return NegotiationApproach(value)
    except ValueError:
        return None
