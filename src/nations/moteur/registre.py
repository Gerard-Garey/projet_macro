"""Registre de l'indice des prix : avance en phase 9 et lectures, seules à l'indexer.

Contrat : ADR 0012, F3 ; ADR 0008, partie II (II.2 à II.4, annotation du
04/10/2026) ; spécification, `sec:cadre-calendrier`, « Empreinte calendaire
de l'état ». Le registre est la variable d'état `registre_prix` du moteur :
à l'ouverture du pas t, les n_a + 1 = 13 derniers niveaux de l'indice,
`registre[u − 1]` = P_{t−u}, u = 1, …, n_a + 1. C'est une variable retardée
de longueur fixe, jamais un historique.

Les fonctions de ce module sont les **seules qui indexent le registre** :
aucun bloc ne l'indexe ; il lit ses trois fonctions de lecture par sa vue.

- `avancer(registre, P_t)` : couche moteur de la phase 9 ; P_t entre,
  P_{t−n_a−1} sort, une copie sans calcul ;
- `dernier_prix` : P_{t−1}, dernier prix connu, lu par les règles en phase 1 ;
- `glissement` : glissement annuel du tour précédent, π_{t−1} = P_{t−1} /
  P_{t−1−n_a} − 1 ; le glissement du tour t se lit sur le registre avancé
  (`glissement(avancer(registre, P_t))`), dès la phase 5 ;
- `variation_sur_le_tour` : variation de l'indice sur le dernier tour clos,
  P_{t−1} / P_{t−1−n_m} − 1.
"""

from __future__ import annotations

import math

from nations.moteur.parametres.cadre import PAS_PAR_AN, PAS_PAR_TOUR

# n_a + 1 niveaux (ADR 0008, II.3).
NIVEAUX = PAS_PAR_AN.valeur + 1


def _verifier(registre: tuple[float, ...]) -> None:
    """Un registre est un tuple de n_a + 1 `float` ; refus sinon."""
    if type(registre) is not tuple or len(registre) != NIVEAUX:
        raise ValueError(f"registre de {NIVEAUX} niveaux attendu, {registre!r} reçu")


def avancer(registre: tuple[float, ...], prix: float) -> tuple[float, ...]:
    """Registre d'ouverture du pas t + 1 : (P_t, P_{t−1}, …, P_{t−n_a})."""
    _verifier(registre)
    if type(prix) is not float or not math.isfinite(prix) or not prix > 0.0:
        raise ValueError(f"indice des prix {prix!r} : float fini > 0 attendu")
    return (prix,) + registre[:-1]


def dernier_prix(registre: tuple[float, ...]) -> float:
    """Dernier prix connu à l'ouverture du pas t : P_{t−1}."""
    _verifier(registre)
    return registre[0]


def glissement(registre: tuple[float, ...]) -> float:
    """Glissement annuel du tour précédent : π_{t−1} = P_{t−1} / P_{t−1−n_a} − 1."""
    _verifier(registre)
    return registre[0] / registre[PAS_PAR_AN.valeur] - 1.0


def variation_sur_le_tour(registre: tuple[float, ...]) -> float:
    """Variation de l'indice sur le dernier tour clos : P_{t−1} / P_{t−1−n_m} − 1."""
    _verifier(registre)
    return registre[0] / registre[PAS_PAR_TOUR.valeur] - 1.0
