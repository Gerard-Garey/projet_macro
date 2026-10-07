"""Calendrier : tour, pas, date affichée et prédicat de date de décision.

Contrat : ADR 0012, F3 et C3 ; ADR 0005, points 1 à 3 ; spécification,
`sec:cadre-calendrier`, « Pas mensuel unique » et « Date de décision ». Le
pas t = 0, 1, 2, … est l'unité du moteur ; le tour n = 1, 2, … celle du jeu.
Un pas est un tour (n_m = 1) : t = n − 1. Le joueur lit une date
(année, mois), jamais un numéro de pas :

    mois = (t mod n_a) + 1,   année = ⌊t / n_a⌋ + 1.

Tout se déduit de t seul, sans compteur : aucune de ces grandeurs n'est une
variable d'état (la date et le prédicat sont des grandeurs calculées à
l'ouverture, `nations.moteur.ouverture`). Le quotient entier de t par n_a
est un calcul de date, non une conversion de taux.
"""

from __future__ import annotations

from nations.moteur.parametres.cadre import PAS_PAR_AN, PAS_PAR_TOUR


def pas_du_tour(n: int) -> int:
    """Pas t du tour n (n ≥ 1) : t = n − 1."""
    if type(n) is not int or n < 1:
        raise ValueError(f"tour {n!r} : entier ≥ 1 attendu")
    return n - 1


def tour_du_pas(t: int) -> int:
    """Tour n du pas t (t ≥ 0) : n = t + 1."""
    if type(t) is not int or t < 0:
        raise ValueError(f"pas {t!r} : entier ≥ 0 attendu")
    return t + 1


def date(t: int) -> tuple[int, int]:
    """Date affichée du pas t : (année, mois), année et mois comptés à partir de 1."""
    if type(t) is not int or t < 0:
        raise ValueError(f"pas {t!r} : entier ≥ 0 attendu")
    annee, rang = divmod(t, PAS_PAR_AN.valeur)
    return annee + 1, rang + 1


def est_date_de_decision(t: int) -> bool:
    """Prédicat de date de décision, tiré de t seul : premier pas d'un tour.

    Vrai à tout pas sous n_m = 1 (`sec:cadre-calendrier`).
    """
    if type(t) is not int or t < 0:
        raise ValueError(f"pas {t!r} : entier ≥ 0 attendu")
    return t % PAS_PAR_TOUR.valeur == 0
