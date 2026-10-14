"""Fixtures partagées des tests d'invariants, et publication des mesures du jalon J2 (#98).

Les mesures publiées (accumulation de l'identité cumulée, coût du noyau seul,
couverture du générateur par graine) sont des nombres nouveaux du jalon J2
(feuille de route § 1) : chaque test qui en produit une l'inscrit par la
fixture `publier`, et le résumé de fin de session les écrit, avec leur
définition, sous le titre « Mesures publiées (#98) », y compris en mode `-q`
et en CI.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[2]
_MESURES = pytest.StashKey[list]()


def _charger(nom, chemin):
    """Module chargé par son chemin (`outils/` et `tests/` ne sont pas des paquets)."""
    if nom in sys.modules:
        return sys.modules[nom]
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def generateur():
    """Module `tests/invariants/generateur_j2.py`, le générateur de flux de #98."""
    return _charger("generateur_j2", Path(__file__).with_name("generateur_j2.py"))


@pytest.fixture(scope="session")
def matrices():
    """Module `outils/verifier_matrices.py`, lecteur des tables de la spécification."""
    return _charger("verifier_matrices", RACINE / "outils" / "verifier_matrices.py")


def pytest_configure(config):
    config.stash[_MESURES] = []


@pytest.fixture
def publier(request):
    """Inscrit une mesure publiée : (titre, lignes de texte), écrite au résumé de session."""
    def inscrire(titre, lignes):
        request.config.stash[_MESURES].append((titre, tuple(lignes)))
    return inscrire


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    mesures = config.stash.get(_MESURES, [])
    if not mesures:
        return
    terminalreporter.section("Mesures publiées (#98)")
    for titre, lignes in mesures:
        terminalreporter.write_line(titre)
        for ligne in lignes:
            terminalreporter.write_line(f"  {ligne}")
