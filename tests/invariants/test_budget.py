"""Invariant : budget de calcul d'au plus 1 ms par pays-semaine.

`CLAUDE.md`, invariant 3, et `docs/exigences.md` § 4.4. Le test de budget
s'exécute sur la plateforme de référence (CI Linux, ADR 0003), avec une marge
pour la variabilité de l'exécuteur, **mesurée avant d'être fixée** : elle n'est
pas encore connue. Tant qu'aucun bloc ni ordonnanceur n'existe, le test est
inactif (skip) ; la mesure elle-même est prête et testée.
"""

import time
from collections.abc import Callable

import pytest

pytestmark = pytest.mark.budget

# Budget : secondes de calcul par pays et par semaine simulée.
BUDGET_S_PAR_PAYS_SEMAINE = 1e-3


def secondes_par_pays_semaine(
    executer_pas: Callable[[], None],
    nb_pas: int,
    nb_pays: int,
    semaines_par_pas: float,
) -> float:
    """Temps moyen de calcul par pays-semaine sur `nb_pas` pas.

    `executer_pas` déroule un pas pour `nb_pays` pays ; `semaines_par_pas`
    convertit la durée du pas en semaines (la durée du pas n'est pas encore
    tranchée : `docs/specification/CONVENTIONS.md` § 6).
    """
    if nb_pas <= 0 or nb_pays <= 0 or semaines_par_pas <= 0:
        raise ValueError("nb_pas, nb_pays et semaines_par_pas doivent être positifs")
    debut = time.perf_counter()
    for _ in range(nb_pas):
        executer_pas()
    duree = time.perf_counter() - debut
    return duree / (nb_pas * nb_pays * semaines_par_pas)


def test_mesure_rapporte_au_pays_semaine():
    # Un pas factice de durée connue : 2 pays, pas de 4 semaines.
    def pas_factice():
        time.sleep(0.008)

    mesure = secondes_par_pays_semaine(pas_factice, nb_pas=5, nb_pays=2, semaines_par_pas=4)
    # 8 ms par pas / (2 pays x 4 semaines) = 1 ms, au moins (sleep ne rend
    # jamais avant l'échéance) ; borne haute large pour l'ordonnanceur du système.
    assert 1e-3 <= mesure < 5e-3


def test_mesure_refuse_un_denominateur_nul():
    with pytest.raises(ValueError):
        secondes_par_pays_semaine(lambda: None, nb_pas=0, nb_pays=1, semaines_par_pas=1)


@pytest.mark.skip(
    reason="aucun bloc ni ordonnanceur : le budget se mesure dès qu'un pas s'exécute "
    "(jalon J2), avec la marge mesurée sur la plateforme de référence (ADR 0003)"
)
def test_budget_par_pays_semaine():
    # À compléter quand l'ordonnanceur existe : état initial résolu d'un
    # archétype, puis `secondes_par_pays_semaine(<pas du moteur>, ...)`
    # comparé à BUDGET_S_PAR_PAYS_SEMAINE multiplié par la marge mesurée.
    raise NotImplementedError
