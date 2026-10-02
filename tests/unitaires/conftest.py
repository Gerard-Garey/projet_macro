"""Fixtures partagées des tests unitaires."""

import importlib.util
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def concordance():
    """Module `outils/concordance_spec_moteur.py`, chargé par son chemin.

    `outils/` n'est pas un paquet : le script se charge comme un fichier.
    """
    chemin = RACINE / "outils" / "concordance_spec_moteur.py"
    spec = importlib.util.spec_from_file_location("concordance_spec_moteur", chemin)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def matrices():
    """Module `outils/verifier_matrices.py`, chargé par son chemin."""
    chemin = RACINE / "outils" / "verifier_matrices.py"
    spec = importlib.util.spec_from_file_location("verifier_matrices", chemin)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
