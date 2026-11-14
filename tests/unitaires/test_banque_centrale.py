"""Bloc 8, banque centrale et anticipations : lignes « J3 » de classe (a) de la fiche 8 (#91).

Classe (a) du classement du rang 1a de J3-c (synthèse en commentaire de la PR
#129, § 1 ; fiche 8, § 9.6) : cas à la main (N-8) ; partie (a) de « Perte » (BC6
et BC9 à i_CB < 0) ; « Phases » (inspection de la déclaration) ; « Bornes »
(égalité exacte, taux négatif, marche de cible) ; « Empreinte » ; ligne
ajoutée : **invariant π^e > −1 de BC3** (forme convexe, P92 ; ADR 0013,
annotation du 14/11/2026, points 4 et 9). S'y ajoutent l'égalité des formes de
BC1 à BC6 du bloc et du script d'état stationnaire (P93, n_a ∈ {4 ; 12 ; 52},
P77 : n_a ≠ 12 couvert par le script), la forme « au socle » de BC6 (point de
forme 3 du mainteneur, 14/11/2026) et le refus de `Vue.glissement()` hors de
1 + π_{t−1} > 0, −1 exactement compris (point de forme 1), éprouvé dans
`tests/unitaires/test_moteur_ordonnanceur.py`. Seuils écrits avant l'essai
(fiche 8, § 9.6), non déplacés. Chaque test appelle les fonctions pures de
`nations.blocs.banque_centrale`, sans le moteur.
"""

import ast
import inspect
import math
import time
from dataclasses import replace

import numpy as np
import pytest

from nations.blocs import banque_centrale as bloc
from nations.etat import schema
from nations.moteur.contrat_bloc import OUVERTURE, REGISTRE, Lecture
from nations.moteur.conversions import par_pas
from nations.moteur.parametres import TauxDeFlux
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt

N_A = PARAMETRES_DE_REFERENCE.cadre.pas_par_an
# Seuils écrits avant l'essai (fiche 8, § 9.6).
SEUIL_ETAT_STATIONNAIRE = 1e-10
SEUIL_CAS_A_LA_MAIN = 1e-12  # × S^CB
# Invariant π^e > −1 (P92) : graine déclarée, 10^6 tirages.
GRAINE_INVARIANT = 20261114
NB_TIRAGES = 10**6


def pas(taux):
    """Taux annuel de flux converti au pas par la seule conversion linéaire."""
    return par_pas(TauxDeFlux(taux))


# --------------------------------------------------------------------------
# Formes : BC1 à BC9 par appel direct
# --------------------------------------------------------------------------


def test_bc1_a_bc9_valeurs_a_la_main():
    """BC1 à BC9 sur des valeurs choisies : chaque fonction rend sa forme écrite, à l'arrondi."""
    r_hat, pi_etoile, pi_prec, a_pi = 0.01, 0.02, 0.03, 0.5
    i_regle = bloc.taux_indique_par_la_regle(r_hat, pi_etoile, pi_prec, a_pi)
    assert i_regle == pytest.approx(1.01 * 1.02 + 0.5 * 0.01 - 1.0, rel=1e-15)
    assert bloc.taux_neutre_suivant(r_hat, pi_prec, pi_etoile, 0.25 / 12) == pytest.approx(
        0.01 + 0.25 / 12 * 0.01, rel=1e-15)
    assert bloc.anticipation_suivante(0.02, 0.05, 0.2 / 12) == pytest.approx(
        0.02 + 0.2 / 12 * 0.03, rel=1e-15)
    assert bloc.cible_suivante(0.02) == 0.02
    assert bloc.part_a_l_emission(0.3) == 0.3
    i = pas(0.04)
    assert bloc.resultat(i, 25.0, i, 20.0, i, 5.0) == pytest.approx(0.04 * 40.0 / 12, rel=1e-15)
    assert bloc.interets_sur_reserves(i, 5.0) == pytest.approx(0.04 * 5.0 / 12, rel=1e-15)
    assert bloc.interets_sur_refinancement(i, 20.0) == pytest.approx(0.04 * 20.0 / 12,
                                                                     rel=1e-15)
    assert bloc.versement_du_resultat(-0.25) == -0.25


def test_une_cible_abaissee_baisse_la_prescription_a_l_impact():
    """`sec:banque_centrale-regle`, « Une cible abaissée baisse le taux à l'impact » :
    ∂(1 + i^règle)/∂π* = (1 + r̂*) − a_π, soit 0,51 à r̂* = 1 % ; π_{t−1} tenu."""
    avant = bloc.taux_indique_par_la_regle(0.01, 0.02, 0.02, 0.5)
    apres = bloc.taux_indique_par_la_regle(0.01, 0.01, 0.02, 0.5)
    assert (apres - avant) / -0.01 == pytest.approx(1.01 - 0.5, rel=1e-12)
    assert apres < avant


def test_prescription_negative_sans_plancher_et_perte_versee_sans_troncature():
    """Fiche 8, § 9.6, « Bornes » et partie (a) de « Perte » : aucune borne ; la prescription
    suit la règle même négative ; à i_CB < 0, Π^CB < 0 (BC6, sous E^CB = 0 : i_CB M^G/n_a) et la
    ligne 16 égale Π^CB, négative, sans troncature (BC9)."""
    i_regle = bloc.taux_indique_par_la_regle(-0.04, 0.0, -0.01, 0.5)
    assert i_regle == pytest.approx(0.96 * 1.0 - 0.005 - 1.0, rel=1e-14) and i_regle < 0.0
    i = pas(i_regle)
    M_G, B_CB, Res = 20.0, 0.0, 0.0
    L_CB = B_CB + M_G - Res  # E^CB = 0 : L^CB = M^G au socle
    Pi_CB = bloc.resultat(i, B_CB, i, L_CB, i, Res)
    assert Pi_CB < 0.0
    assert Pi_CB == pytest.approx(i_regle * M_G / N_A, rel=1e-15)
    assert bloc.versement_du_resultat(Pi_CB) == Pi_CB


@pytest.mark.parametrize("B_CB, L_CB, Res, M_G", [
    (0.0, 20.0, 0.0, 20.0), (25.0, 0.0, 5.0, 20.0), (30.0, 3.0, 13.0, 21.0),
    (7.0, 11.0, 0.5, 16.0), (0.0, 20.0, 0.0, 19.0),
])
@pytest.mark.parametrize("i_CB", [0.0302, -0.015, 0.111])
def test_bc6_forme_au_socle_identite_de_bilan(B_CB, L_CB, Res, M_G, i_CB):
    """Point de forme 3 du mainteneur (14/11/2026) : BC6 s'exécute sous sa forme générale ; la
    forme « au socle », Π^CB = i_CB (M^G + E^CB)/n_a, en découle par la définition des fonds
    propres E^CB = B_CB + L^CB − Res − M^G (`sec:cadre-bilans`), E^CB lu par le stock du noyau
    (`valeur_nette_stock`), à 1e−12 × S^CB, E^CB nul ou non."""
    positions = {nom: 0.0 for nom in cat.NOMS_POSTES}
    positions.update(B_CB=B_CB, L_CB=L_CB, Res=Res, M_G=M_G)
    E_CB = idt.valeur_nette_stock(positions, "banque_centrale")
    assert E_CB == pytest.approx(B_CB + L_CB - Res - M_G, abs=1e-15)
    i = pas(i_CB)
    generale = bloc.resultat(i, B_CB, i, L_CB, i, Res)
    au_socle = i * (M_G + E_CB)
    S_CB = idt.echelle_bilan(positions, "banque_centrale")
    assert abs(generale - au_socle) <= SEUIL_CAS_A_LA_MAIN * S_CB


# --------------------------------------------------------------------------
# Cas à la main (N-8 ; critère 1 (c))
# --------------------------------------------------------------------------


def test_cas_a_la_main_n8():
    """Fiche 8, § 3.N-8 et § 9.6, « Cas à la main », par appel direct de BC1 à BC9 : taux
    directeur de 3 à 4 % (BC1 depuis r̂* = 1 %, π* = 2 %, π_{t−1} = 3,96 %), M^G* = 20,
    ouverture L^CB = M^G = 20, B_CB = Res = E^CB = 0 ; achat de 25 de titres à la banque en
    phase 7 (ligne 19b-banque, J6 : donnée de l'appel direct), ligne 21 = −20. Lignes 13 =
    0,04 × 20/12, 12 = 0, Π^CB = ligne 16 ; clôture B_CB = 25, L^CB = 0, Res + M^G = 25 ;
    E^CB par le stock et par les flux ; contrainte budgétaire ΔB_CB + ΔL^CB = ΔRes + ΔM^G +
    Π^CB − ligne 16 ; à 1e−12 × S^CB."""
    i_CB = bloc.taux_indique_par_la_regle(0.01, 0.02, 0.0396, 0.5)
    assert i_CB == pytest.approx(0.04, abs=1e-15)
    ouverture = {"B_CB": 0.0, "L_CB": 20.0, "Res": 0.0, "M_G": 20.0}
    i = pas(i_CB)
    Pi_CB = bloc.resultat(i, ouverture["B_CB"], i, ouverture["L_CB"], i, ouverture["Res"])
    l12 = bloc.interets_sur_reserves(i, ouverture["Res"])
    l13 = bloc.interets_sur_refinancement(i, ouverture["L_CB"])
    l16 = bloc.versement_du_resultat(Pi_CB)
    # Clôture par les flux : achat de 25 payé en réserves (19b-banque, donnée de l'appel
    # direct), refinancement remboursé (ligne 21 = −20), lignes 12 et 13 sur les réserves,
    # ligne 16 sur le compte du Trésor. La fiche (N-8) arrondit la clôture en omettant le
    # règlement des intérêts : Res = 5 et M^G = 20 ; par les flux, Res + M^G = 25.
    achat, l21 = 25.0, -20.0
    cloture = {"B_CB": ouverture["B_CB"] + achat, "L_CB": ouverture["L_CB"] + l21,
               "Res": ouverture["Res"] + achat + l21 + l12 - l13,
               "M_G": ouverture["M_G"] + l16}
    positions = {nom: 0.0 for nom in cat.NOMS_POSTES}
    positions.update(cloture)
    S_CB = idt.echelle_bilan(positions, "banque_centrale")
    attendus = {"ligne 13": (l13, 0.04 * 20.0 / 12), "ligne 12": (l12, 0.0),
                "Π^CB": (Pi_CB, 0.04 * 20.0 / 12), "ligne 16": (l16, Pi_CB),
                "B_CB": (cloture["B_CB"], 25.0), "L^CB": (cloture["L_CB"], 0.0),
                "Res + M^G": (cloture["Res"] + cloture["M_G"], 25.0)}
    for nom, (obtenu, attendu) in attendus.items():
        assert abs(obtenu - attendu) <= SEUIL_CAS_A_LA_MAIN * S_CB, nom
    e_stock = idt.valeur_nette_stock(positions, "banque_centrale")
    e_flux = 0.0 + Pi_CB - l16
    assert abs(e_stock) <= SEUIL_CAS_A_LA_MAIN * S_CB
    assert abs(e_flux) <= SEUIL_CAS_A_LA_MAIN * S_CB
    gauche = (cloture["B_CB"] - ouverture["B_CB"]) + (cloture["L_CB"] - ouverture["L_CB"])
    droite = (cloture["Res"] - ouverture["Res"]) + (cloture["M_G"] - ouverture["M_G"]) \
        + Pi_CB - l16
    assert abs(gauche - droite) <= SEUIL_CAS_A_LA_MAIN * S_CB


# --------------------------------------------------------------------------
# Formes du bloc et du script d'état stationnaire (P93 ; P77)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
@pytest.mark.parametrize("n_a", [4, 12, 52])
def test_formes_du_bloc_egales_au_script(stationnaire, pi, n_a):
    """P93 et P77 : BC1 à BC6 du bloc, évaluées sur l'ouverture stationnaire du script
    (`ouverture`, ν_G = 1,15), égalent au bit les règles du pas 0 du script (`un_pas` : i_CB,
    r̂*_1, π^e_1 sous la forme convexe alignée, Π^CB à 1e−15 relatif, forme générale du bloc
    contre (i B_CB + i L^CB − i Res)/n_a du script), et la fiche 8, § 9.6, « État
    stationnaire » à 1e−10 : r̂*_1 = r̄, π^e_1 = π*, i_CB = i^règle = (1 + r̄)(1 + π*) − 1,
    Π^CB = i_CB (M^G + E^CB)/n_a. Les taux par pas sont convertis par le test au n_a du point
    (le moteur ne s'exécute qu'à n_a = 12)."""
    par = replace(stationnaire.Parametres(), pi_cible=pi, n_a=n_a, nu_G=1.15)
    e = stationnaire.etat_stationnaire(par)
    o = stationnaire.ouverture(e, par)
    s = stationnaire.un_pas(o, par)
    P = o["registre"]
    pi_prec = P[0] / P[n_a] - 1.0
    i_regle = bloc.taux_indique_par_la_regle(o["r_hat"], o["pi_cible"], pi_prec, par.a_pi)
    r_hat_1 = bloc.taux_neutre_suivant(o["r_hat"], pi_prec, o["pi_cible"], par.a_I / n_a)
    pi_e_1 = bloc.anticipation_suivante(o["pi_e"], pi_prec, par.lambda_e / n_a)
    i = i_regle / n_a
    Pi_CB = bloc.resultat(i, o["B_CB"], i, o["L_CB"], i, o["Res"])
    assert i_regle.hex() == s["i_CB"].hex()
    assert r_hat_1.hex() == s["r_hat_1"].hex()
    assert pi_e_1.hex() == s["pi_e_1"].hex()
    assert abs(Pi_CB / s["Pi_CB"] - 1.0) <= 1e-15
    ecarts = {
        "r̂*_1/r̄": abs(r_hat_1 / par.rbar - 1.0),
        "π^e_1/π*": abs(pi_e_1 - pi) if pi == 0.0 else abs(pi_e_1 / pi - 1.0),
        "i_CB": abs(i_regle / ((1 + par.rbar) * (1 + pi) - 1) - 1.0),
        "Π^CB": abs(Pi_CB / (i_regle * (o["M_G"] + o["E_CB"]) / n_a) - 1.0),
    }
    for nom, x in ecarts.items():
        assert x <= SEUIL_ETAT_STATIONNAIRE, (nom, x)


def test_script_execute_bc3_sous_la_forme_convexe(stationnaire):
    """P93 : le script d'état stationnaire exécute BC3 sous la forme convexe (P92), comme le
    bloc : sur l'exemple adverse de `monnaie` (λ_e = n_a, π^e = 680 268,97, π_{t−1} =
    −0,9999999999999962), il rend π_{t−1} (> −1), là où la forme littérale rend −1."""
    par = replace(stationnaire.Parametres(), lambda_e=12.0)
    o = stationnaire.ouverture(stationnaire.etat_stationnaire(par), par)
    pi_prec = -0.9999999999999962
    rapport = 1.0 + pi_prec
    o = dict(o, pi_e=680268.97,
             registre=[rapport] + [1.0] * (par.n_a - 1) + [1.0, 1.0])
    s = stationnaire.un_pas(o, par)
    assert s["pi_prec"] == o["registre"][0] / o["registre"][par.n_a] - 1.0
    assert s["pi_e_1"] == bloc.anticipation_suivante(680268.97, s["pi_prec"], 1.0)
    assert s["pi_e_1"] > -1.0
    litterale = 680268.97 + 1.0 * (s["pi_prec"] - 680268.97)
    assert litterale == -1.0


# --------------------------------------------------------------------------
# Invariant π^e > −1 de BC3 (P92 ; critère 1 de l'amendement du rang 0)
# --------------------------------------------------------------------------


def _bc3_sur_tirages(lambdas, pi_es, pis):
    """BC3 du bloc, appelée directement tirage par tirage, sur les tirages admis : 0 < λ_e ≤
    n_a, 1 + π^e_t > 0 (domaine du schéma) et 1 + π_{t−1} > 0 tel que calculé (précondition,
    tenue par la vue). Rend (nombre de tirages admis, nombre d'échecs de π^e_{t+1} > −1 ou de
    1 + π^e_{t+1} > 0, premier échec)."""
    admis = echecs = 0
    premier = None
    for lam, pi_e, pi in zip(lambdas, pi_es, pis):
        if not (0.0 < lam <= N_A and 1.0 + pi_e > 0.0 and 1.0 + pi > 0.0):
            continue
        admis += 1
        suivant = bloc.anticipation_suivante(pi_e, pi, pas(lam))
        if not (suivant > -1.0 and 1.0 + suivant > 0.0):
            echecs += 1
            premier = premier or (lam, pi_e, pi, suivant)
    return admis, echecs, premier


def test_invariant_pi_e_sur_un_million_de_tirages():
    """P92, critère 1 de l'amendement du rang 0 de #91 : sur 10^6 tirages à graine déclarée
    (20261114), λ_e uniforme sur ]0 ; n_a], 1 + π^e_t = exp(u), u uniforme sur [−40 ; 15],
    rapport des prix P_{t−1}/P_{t−1−n_a} = exp(v), v uniforme sur [−40 ; 40], π_{t−1} calculé
    comme par le registre (rapport − 1) ; tirages admis : π^e_t > −1 et 1 + π_{t−1} > 0 tels que
    calculés. BC3 du bloc rend π^e_{t+1} > −1 (et 1 + π^e_{t+1} > 0) à chaque tirage admis."""
    rng = np.random.default_rng(GRAINE_INVARIANT)
    lambdas = N_A * (1.0 - rng.random(NB_TIRAGES))
    pi_es = np.exp(rng.uniform(-40.0, 15.0, NB_TIRAGES)) - 1.0
    rapports = np.exp(rng.uniform(-40.0, 40.0, NB_TIRAGES))
    debut = time.perf_counter()
    pis = [float(r) / 1.0 - 1.0 for r in rapports.tolist()]
    admis, echecs, premier = _bc3_sur_tirages(lambdas.tolist(), pi_es.tolist(), pis)
    duree = time.perf_counter() - debut
    assert admis >= 0.9 * NB_TIRAGES
    assert echecs == 0, premier
    # Garde de durée de la batterie (mesure du compte rendu de #91 : ≈ 1 s) ; large, la
    # machine de CI pouvant être plus lente.
    assert duree < 30.0, duree


def _bords():
    """Lot adverse sur les bords : λ_e aux bords de ]0 ; n_a] ; π^e au bord de −1 et très
    grand ; π_{t−1} calculé (rapport − 1) depuis des rapports des prix au bord de 2^−53 (le plus
    petit rapport dont le glissement reste > −1 ; en dessous de 2^−54, il vaut −1 et la vue le
    refuse) et très grands ; plus l'exemple de `monnaie` (λ_e = n_a, π^e = 680 268,97,
    π = −0,9999999999999962) et 2 × 10^5 tirages concentrés près de ces bords (graine
    20261114 + 1)."""
    lambdas = [5e-324, 1e-300, 1e-16, 1e-8, 0.2, 1.0, 6.0, math.nextafter(N_A, 0.0),
               float(N_A)]
    pi_es = [math.nextafter(-1.0, 0.0), -1.0 + 2.0**-52, -1.0 + 1e-15, -0.999999, -0.5, 0.0,
             0.02, 1.0, 680268.97, 1e10, 1e300]
    rapports = [2.0**-53, 2.0**-53 * (1.0 + 2.0**-52), 2.0**-52, 3.8e-15, 1e-15, 1e-10, 0.5,
                1.0, 2.0, 1e10, 1e300]
    grille = [(lam, pi_e, r - 1.0) for lam in lambdas for pi_e in pi_es for r in rapports]
    rng = np.random.default_rng(GRAINE_INVARIANT + 1)
    n = 200_000
    lam = np.where(rng.random(n) < 0.5, float(N_A), N_A * (1.0 - rng.random(n)))
    pi_e = np.exp(rng.uniform(-36.0, 30.0, n)) - 1.0
    rapport = np.exp(rng.uniform(-36.9, -30.0, n))
    tires = list(zip(lam.tolist(), pi_e.tolist(), (rapport - 1.0).tolist()))
    return grille + [(float(N_A), 680268.97, -0.9999999999999962)] + tires


def test_invariant_pi_e_lot_adverse_sur_les_bords():
    """P92 : second lot, adverse, sur les bords (`_bords`) : BC3 du bloc rend π^e_{t+1} > −1 à
    chaque tirage admis ; la forme littérale π^e + c(π − π^e), évaluée sur le même lot par le
    test, rend −1 sur une partie de ces tirages (pouvoir discriminant du lot, publié)."""
    lot = _bords()
    lambdas, pi_es, pis = zip(*lot)
    admis, echecs, premier = _bc3_sur_tirages(lambdas, pi_es, pis)
    assert echecs == 0, premier
    litterale = sum(1 for lam, pe, p in lot if 0.0 < lam <= N_A and 1.0 + pe > 0.0
                    and 1.0 + p > 0.0 and not pe + pas(lam) * (p - pe) > -1.0)
    assert admis >= 0.5 * len(lot)
    assert litterale > 0


# --------------------------------------------------------------------------
# Phases, empreinte, déclaration (inspection)
# --------------------------------------------------------------------------


def test_declaration_conforme_a_tab_banque_centrale_phases():
    """`tab:banque_centrale-phases` et ADR 0013, annotation du 14/11/2026, point 5 : sièges en
    phases 1, 8 (a) et 8 (b) seulement (aucune écriture en phases 2 à 7) ; en phase 1, lectures
    de l'ouverture π*, r̂*, π^e, B_CB, L^CB, Res et du glissement, jamais W, p, U, M^G ni une
    variable du pas ; écritures i^règle, i_CB, θ_CB, Π^CB et les états r̂*, π^e, π* ; en 8 (a),
    Res, L^CB et i_CB, lignes 12 et 13 ; en 8 (b), Π^CB, ligne 16 ; aucune ligne 19b, aucun
    montant couvert ; aucune variable `i_res` ni `i_B`."""
    sieges = {s.etape: s for s in bloc.BanqueCentrale.declaration.sieges}
    assert tuple(sieges) == ("1", "8a", "8b")
    assert set(sieges["1"].lit) == {Lecture(OUVERTURE, n) for n in (
        "pi_etoile", "r_hat_etoile", "pi_e", "B_CB", "L_CB", "Res")} | {
        Lecture(REGISTRE, "glissement")}
    assert set(sieges["1"].ecrit) == {"i_regle", "i_CB", "theta_CB", "Pi_CB"}
    assert set(sieges["1"].etat) == {"pi_e", "r_hat_etoile", "pi_etoile"}
    assert set(sieges["8a"].lit) == {Lecture(OUVERTURE, "Res"), Lecture(OUVERTURE, "L_CB"),
                                     Lecture("1", "i_CB")}
    assert set(sieges["8b"].lit) == {Lecture("1", "Pi_CB")}
    assert [s.propose for s in sieges.values()] == [(), ("12", "13"), ("16",)]
    assert all(s.couvre == () for s in sieges.values())
    assert sieges["8a"].ecrit == sieges["8b"].ecrit == ()
    assert sieges["8a"].etat == sieges["8b"].etat == ()
    lus = {lu.nom for s in sieges.values() for lu in s.lit}
    assert not lus & {"W", "p", "U", "W_suivant", "M_G", "i_res", "i_B"}
    ecrits = {n for s in sieges.values() for n in s.ecrit + s.etat}
    assert not ecrits & {"i_res", "i_B"}
    assert not any(ligne.startswith("19b") for s in sieges.values() for ligne in s.propose)


def test_empreinte_deux_variables_nouvelles_et_la_cible():
    """Fiche 8, § 9.6, « Empreinte et coût », partie (a) : deux variables d'état nouvelles (π^e,
    r̂*) et la cible en vigueur π*, au radical `banque_centrale`, scalaires, écrites en phase 1,
    dans l'ordre du schéma π^e, r̂*, π* (ADR 0013, annotation du 14/11/2026, point 3) ; aucun
    registre propre, aucun tirage : le module n'importe que `contrat_bloc` et `conversions` ;
    le bloc n'a pas d'attribut d'instance."""
    variables = [v for v in schema.VARIABLES_DES_BLOCS if v.proprietaire == "banque_centrale"]
    assert [(v.nom, v.phase_ecriture, v.unite) for v in variables] == [
        ("pi_e", "1", "par an, taux de croissance"),
        ("r_hat_etoile", "1", "par an, taux de croissance"),
        ("pi_etoile", "1", "par an, taux de croissance")]
    assert all(v.type is float and v.longueur == 1 for v in variables)
    arbre = ast.parse(inspect.getsource(bloc))
    importes = {n.module for n in ast.walk(arbre) if isinstance(n, ast.ImportFrom)}
    importes |= {a.name for n in ast.walk(arbre) if isinstance(n, ast.Import) for a in n.names}
    assert importes == {"__future__", "nations.moteur.contrat_bloc",
                        "nations.moteur.conversions"}
    instance = bloc.BanqueCentrale()
    assert not hasattr(instance, "__dict__") and bloc.BanqueCentrale.__slots__ == ()


def test_domaine_de_r_hat_finitude_seule():
    """ADR 0013, annotation du 14/11/2026, point 4 : r̂* sans condition de signe (aucun
    plancher), refusé seulement non fini, par la seule fonction de domaine du schéma."""
    for x in (-0.9, -5.0, 0.0, 3.0):
        assert schema.defaut_de_domaine("r_hat_etoile", x) is None
    for x in (math.inf, -math.inf, math.nan):
        assert "non fini" in schema.defaut_de_domaine("r_hat_etoile", x)
