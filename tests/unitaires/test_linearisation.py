"""Linéarisation numérique de la carte d'un pas (issue #112, point 4).

Critère écrit avant l'essai : la linéarisation retrouve une valeur propre
connue en forme fermée sur un cas d'essai, à 1e−8. Ici, sur des cartes
linéaires d'essai (valeurs propres connues, complexes comprises) et sur les
facteurs de tendance par unité ; le cas d'essai sur le moteur (N1 dans le
socle partiel d'essai, 1 − λ_v/n_a) est dans
`tests/invariants/test_socle_partiel.py`.
"""

import cmath
import dataclasses

import numpy as np
import pytest

from nations.etat import schema
from nations.moteur.conversions import facteur_par_pas
from nations.moteur.parametres import TauxDeCroissance, varier
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE

SEUIL = 1e-8


def carte_lineaire(linearisation, matrice, x0, facteurs):
    """Carte affine x ↦ f ⊙ (x0 + M (x − x0)), ramenée au sentier par f : point fixe x0,
    jacobienne M."""
    matrice, x0, facteurs = (np.asarray(a, dtype=float) for a in (matrice, x0, facteurs))
    return linearisation.Carte(
        ("a", "b", "c")[:len(x0)], x0, np.where(np.abs(x0) > 0, np.abs(x0), 1.0),
        lambda x: (facteurs * (x0 + matrice @ (x - x0))) / facteurs)


@pytest.mark.parametrize("rayon, angle", [(0.9, 0.3), (0.997, 2 * np.pi / 3617), (1.02, 1.0)])
def test_paire_complexe_retrouvee(linearisation, rayon, angle):
    """Une rotation-homothétie de valeurs propres ρ e^{±iθ} : retrouvées à 1e−8, sur des
    variables d'échelles très différentes (mise à l'échelle S⁻¹ J S)."""
    m = rayon * np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    s = np.diag([1e3, 1e-2])
    carte = carte_lineaire(linearisation, s @ m @ np.linalg.inv(s), [5e3, 0.02], [1.003, 1.0])
    valeurs = linearisation.valeurs_propres(carte)
    attendues = sorted([cmath.rect(rayon, angle), cmath.rect(rayon, -angle)],
                       key=lambda z: (-abs(z), z.real, z.imag))
    assert np.max(np.abs(valeurs - np.array(attendues))) <= SEUIL
    assert linearisation.residu_point_fixe(carte) <= 1e-15


def test_valeurs_reelles_et_variable_nulle(linearisation):
    """Matrice triangulaire : valeurs propres = diagonale (0,75 ; 0,5 ; 0), une variable nulle au
    point fixe (échelle au plancher déclaré)."""
    m = [[0.75, 0.2, 0.0], [0.0, 0.5, 3.0], [0.0, 0.0, 0.0]]
    carte = carte_lineaire(linearisation, m, [2.0, 0.3, 0.0], [1.0, 1.0, 1.0])
    assert carte.echelle[2] == linearisation.PLANCHER_D_ECHELLE
    valeurs = linearisation.valeurs_propres(carte)
    assert np.max(np.abs(valeurs - np.array([0.75, 0.5, 0.0]))) <= SEUIL


def test_facteurs_de_tendance_par_unite(linearisation):
    """La tendance d'un pas est lue dans l'unité, par la conversion géométrique du moteur, sur
    g_pr et g_N des tables de l'ensemble passé ; une unité sans tendance déclarée est refusée."""
    p = PARAMETRES_DE_REFERENCE
    varie = dataclasses.replace(p, production=varier(p.production, g_pr=0.03),
                                travail=varier(p.travail, g_N=0.005))
    pi = 0.1

    def f(x):
        return facteur_par_pas(TauxDeCroissance(x))

    attendus = {
        "u.m.": f(1.03 * 1.005 * 1.1 - 1), "u.v.": f(1.03 * 1.005 - 1),
        "u.v. par pas": f(1.03 * 1.005 - 1), "u.v. par personne et par pas": f(0.03),
        "personnes": f(0.005), "u.m. par personne et par pas": f(1.03 * 1.1 - 1),
        "u.m. par u.v.": f(0.1), "fraction": 1.0, "sans dimension": 1.0,
        "par an, taux de croissance": 1.0, "par an, taux de flux": 1.0,
    }
    for unite, attendu in attendus.items():
        assert linearisation.facteur_de_tendance(unite, varie, pi) == pytest.approx(
            attendu, rel=1e-15, abs=0.0), unite
    # Chaque variable d'état scalaire hors V^flux a une tendance déclarée.
    for v in schema.VARIABLES:
        if v.type is float:
            assert v.unite in linearisation.FACTEURS_PAR_UNITE, v.nom
    with pytest.raises(ValueError, match="tendance non déclarée"):
        linearisation.facteur_de_tendance("années", p, pi)


@pytest.mark.parametrize("nom", ["registre_prix", "t", "V_flux_menages", "inconnu"])
def test_carte_du_moteur_refuse_une_variable_hors_de_la_carte(linearisation, nom):
    """Le registre, t et les V^flux (recalculées) ne sont pas des variables de la carte."""
    with pytest.raises(ValueError, match="variable d'état scalaire"):
        linearisation.carte_du_moteur(object(), object(), [nom], 0.02)
