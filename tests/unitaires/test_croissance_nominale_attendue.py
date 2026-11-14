"""Cible en vigueur π* et facteur de croissance nominale attendue Γ^e (issue #61, rang 3 de J3-c).

Contrat : ADR 0010, point 4 (M30) ; ADR 0013, annotation du 14/11/2026, points 3,
4 et 7 (P88, P96). Critères de #61, écrits avant l'essai (feuille de route § 1) :
Γ^e = [(1 + g)(1 + π*)]^{1/n_a} par appel direct à 1e−15 relatif, calculé une
seule fois en phase 0, après g ; forme exécutée `facteur_g` · f(π*), π*_t lue à
l'ouverture. Chaque test appelle directement les grandeurs d'ouverture ; l'appel unique
par pas, en phase 0, est éprouvé avec l'ordonnanceur d'essai
(`test_moteur_ordonnanceur.py`, `test_gamma_e_calcule_une_seule_fois_par_pas_en_phase_0`).
"""

import dataclasses
import itertools

import pytest

from nations.moteur.conversions import facteur_par_pas
from nations.moteur.ouverture import GRANDEURS_OUVERTURE
from nations.moteur.parametres import TauxDeCroissance, varier
from nations.moteur.parametres.cadre import PAS_PAR_AN
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE

N_A = PAS_PAR_AN.valeur
SEUIL_DIRECT = 1e-15  # critère de #61, relatif


def grandeurs(pi_etoile, g_pr=0.02, g_n=0.0):
    """Grandeurs d'ouverture calculées dans l'ordre de `GRANDEURS_OUVERTURE`, état d'ouverture
    réduit à t et π*_t, tables de référence variées en g_pr et g_N."""
    p = PARAMETRES_DE_REFERENCE
    ensemble = dataclasses.replace(p, production=varier(p.production, g_pr=g_pr),
                                   travail=varier(p.travail, g_N=g_n))

    class Ouverture:
        t = 0

    Ouverture.pi_etoile = pi_etoile
    valeurs = {}
    for g in GRANDEURS_OUVERTURE:
        valeurs[g.nom] = g.fonction(Ouverture(), ensemble, valeurs)
    return valeurs


GRILLE = list(itertools.product((0.0, 0.02, 0.03, -0.01), (0.0, 0.001, 0.005),
                                (0.0, 0.02, 0.10, -0.02, 0.5)))


@pytest.mark.parametrize("g_pr, g_n, pi", GRILLE)
def test_gamma_e_egal_a_la_forme_directe(g_pr, g_n, pi):
    """Γ^e = [(1 + g)(1 + π*)]^{1/n_a} à 1e−15 relatif (critère de #61), g = (1 + g_pr)(1 + g_N)
    − 1 ; forme exécutée `facteur_g` · f(π*) au bit ; γ^e = Γ^e − 1 et π^{∗,pas} = f(π*) − 1 au
    bit."""
    v = grandeurs(pi, g_pr, g_n)
    direct = ((1.0 + v["g"]) * (1.0 + pi)) ** (1.0 / N_A)
    assert abs(v["Gamma_e"] / direct - 1.0) <= SEUIL_DIRECT
    f_cible = facteur_par_pas(TauxDeCroissance(pi))
    assert v["Gamma_e"].hex() == (v["facteur_g"] * f_cible).hex()
    assert v["gamma_e"] == v["Gamma_e"] - 1.0
    assert v["pi_etoile_pas"] == f_cible - 1.0


def test_gamma_e_apres_g_et_facteur_g_dans_l_ordre_de_l_annotation():
    """Point 7 : `g`, `facteur_g`, puis `pi_etoile_pas`, `Gamma_e`, `gamma_e`, chacun une seule
    fois dans `GRANDEURS_OUVERTURE` (grandeurs de la phase 0, C3)."""
    noms = [g.nom for g in GRANDEURS_OUVERTURE]
    assert noms[3:] == ["g", "facteur_g", "pi_etoile_pas", "Gamma_e", "gamma_e"]
    assert len(noms) == len(set(noms))


def test_gamma_e_lit_la_cible_en_vigueur_non_le_parametre():
    """ADR 0010 (M30) : Γ^e lit π*_t de l'état d'ouverture (`pi_etoile`), non le paramètre de
    la table du bloc 8 (qui n'en est que la valeur initiale) ; la table n'est pas lue."""
    p = PARAMETRES_DE_REFERENCE
    assert p.banque_centrale.pi_etoile.valeur == 0.02
    v = grandeurs(0.10)
    assert v["Gamma_e"] == v["facteur_g"] * facteur_par_pas(TauxDeCroissance(0.10))
    assert v["Gamma_e"] != v["facteur_g"] * facteur_par_pas(p.banque_centrale.pi_etoile)

