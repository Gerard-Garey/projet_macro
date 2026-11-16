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


@pytest.fixture(autouse=True)
def etat_de_fin_de_pas_controle_en_entier(request, monkeypatch):
    """Contrôle complet de chaque état de fin de pas, sur toutes les trajectoires des tests
    d'invariants (#144, point 1 ; M1 de l'audit du rang 2 de la branche « forme du code »).

    Le moteur ne recontrôle pas, à la clôture, le domaine des variables d'état des blocs
    (`schema.etat_de_cloture`) : il est contrôlé à l'écriture par `Vue.ecrire_etat`, seul site
    qui remplit `_Pas.etat_suivant` (tests textuels de `tests/unitaires/test_etat.py`). Pour
    qu'une valeur entrée par une voie que ces tests textuels ne voient pas (`getattr` dynamique,
    alias) soit refusée quand même, la `FinDePas` que construit `executer_pas` passe ici par une
    fabrique qui reconstruit l'état par le constructeur (`EtatPays(**champs)`, contrôle complet)
    avant de rendre la `FinDePas` réelle (le type relevé par les observateurs est inchangé).
    Sans coût pour le moteur : tests seulement ; les tests du budget (`budget`), qui
    chronomètrent le moteur, en sont exclus.
    """
    if request.node.get_closest_marker("budget") is not None:
        return
    from nations.etat import schema
    from nations.moteur import ordonnanceur
    from nations.observation.observateur import FinDePas

    def fin_de_pas_controlee(t, etat, *args, **kwargs):
        schema.EtatPays(**{nom: getattr(etat, nom) for nom in schema.CHAMPS})
        return FinDePas(t, etat, *args, **kwargs)
    monkeypatch.setattr(ordonnanceur, "FinDePas", fin_de_pas_controlee)


@pytest.fixture(scope="session")
def generateur():
    """Module `tests/invariants/generateur_j2.py`, le générateur de flux de #98."""
    return _charger("generateur_j2", Path(__file__).with_name("generateur_j2.py"))


@pytest.fixture(scope="session")
def socle():
    """Module `tests/invariants/socle_partiel.py`, le socle partiel d'essai de #112 (P52)."""
    return _charger("socle_partiel", Path(__file__).with_name("socle_partiel.py"))


@pytest.fixture(scope="session")
def linearisation():
    """Module `outils/linearisation.py`, linéarisation de la carte d'un pas (#112, point 4)."""
    return _charger("linearisation", RACINE / "outils" / "linearisation.py")


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
