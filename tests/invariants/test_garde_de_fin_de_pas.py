"""Garde de fin de pas des tests d'invariants (R1, #157).

La fabrique `_fin_de_pas_controlee` du `conftest` (contrôle complet de chaque état de fin de pas)
est posée par une fixture `autouse` de portée module : elle doit être en place dans chaque module
de `tests/invariants/`, **avant toute fixture de portée module** de ce module (bancs,
trajectoires), et pendant chaque test hors du budget. Le débordement sur `tests/unitaires/` est
contrôlé de l'autre côté (`test_fabrique_de_fin_de_pas_du_moteur_hors_des_invariants`).
"""

import pytest

from nations.moteur import ordonnanceur
from nations.observation.observateur import FinDePas


@pytest.fixture(scope="module")
def fabrique_a_la_construction_d_un_banc():
    """Fabrique de `FinDePas` en place quand une fixture de portée module est construite."""
    return ordonnanceur.FinDePas


def test_garde_posee_avant_les_fixtures_de_portee_module(fabrique_a_la_construction_d_un_banc):
    assert fabrique_a_la_construction_d_un_banc.__name__ == "_fin_de_pas_controlee"


def test_garde_posee_pendant_un_test():
    assert ordonnanceur.FinDePas.__name__ == "_fin_de_pas_controlee"
    assert ordonnanceur.FinDePas is not FinDePas


@pytest.mark.budget
def test_garde_retiree_pour_un_test_du_budget():
    """Exception déclarée du `conftest` : les tests du budget chronomètrent le moteur seul."""
    assert ordonnanceur.FinDePas is FinDePas
