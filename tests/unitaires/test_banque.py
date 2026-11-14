"""Bloc 7, banque commerciale : lignes « J3 » de classe (a) de la fiche 7 (#90).

Classe (a) du classement du rang 1a de J3-c (synthèse en commentaire de la PR
#129, § 1 ; fiche 7, § 9.6) : cas à la main dans ses quatre variantes ; C29 ;
boucle propre ; neutralité des achats de titres ; (d1) ; parties (a) de
« Réserves et refinancement » (B7 dans ses trois cas sur tirages, achat
19b-banque), « Bornes » (scénarios de taux en équilibre partiel), « Monnaie
endogène » (inspection), « Phases » et « Empreinte » (inspection). S'y ajoutent
l'égalité des formes de B1 à B7 du bloc et du script d'état stationnaire (P93,
n_a ∈ {4 ; 12 ; 52}, P77 : n_a ≠ 12 couvert par le script), E^Bk calculé sur les
six positions comparé à `valeur_nette_stock` (ADR 0013, annotation du 14/11/2026,
point 5) et le contrat de poussière (D_H et D_F lus en max(0 ; ·), critère 4 du
07/10/2026), éprouvé sur la méthode de phase par une vue d'essai. Seuils écrits
avant l'essai (fiche 7, § 9.6 ; `sec:banque-conditions`), non déplacés. Les
tests de formes appellent les fonctions pures de `nations.blocs.banque`, sans le
moteur.
"""

import ast
import inspect
import math
import time
import types
from dataclasses import replace

import numpy as np
import pytest

from nations.blocs import banque as bloc
from nations.etat import schema
from nations.moteur.contrat_bloc import GRAND_LIVRE, OUVERTURE, Lecture
from nations.moteur.conversions import par_pas
from nations.moteur.parametres import TauxDeFlux
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt

N_A = PARAMETRES_DE_REFERENCE.cadre.pas_par_an
TABLE = PARAMETRES_DE_REFERENCE.banque
EPSILON = PARAMETRES_DE_REFERENCE.cadre.tolerance_identite_pas
# Seuils écrits avant l'essai (fiche 7, § 9.6 ; `sec:banque-conditions`).
SEUIL_ETAT_STATIONNAIRE = 1e-10
SEUIL_CAS_A_LA_MAIN = 1e-12  # × S^Bk
SEUIL_C29 = 1e-12  # relatif
SEUIL_BOUCLE_PROPRE = 1e-12  # relatif
SEUIL_NEUTRALITE = 1e-12  # relatif
SEUIL_I_D = 1e-15
# B7 sur tirages (critère 1 du 07/10/2026) : graine déclarée, 10^6 tirages.
GRAINE_B7 = 20261115
NB_TIRAGES = 10**6


def pas(taux):
    """Taux annuel de flux converti au pas par la seule conversion linéaire."""
    return par_pas(TauxDeFlux(taux))


def positions(**postes):
    """Les onze positions du noyau, nulles sauf celles données."""
    p = {nom: 0.0 for nom in cat.NOMS_POSTES}
    p.update(postes)
    return p


# --------------------------------------------------------------------------
# Formes : B1 à B7 par appel direct
# --------------------------------------------------------------------------


def test_b1_a_b7_valeurs_a_la_main():
    """B1 à B7 sur des valeurs choisies : chaque fonction rend sa forme écrite, à l'arrondi."""
    assert bloc.taux_des_credits_suivant(0.04, 0.02) == pytest.approx(0.06, rel=1e-15)
    assert bloc.taux_des_depots_suivant(0.04, 0.01) == pytest.approx(0.03, rel=1e-15)
    assert bloc.interets_sur_credits(pas(0.05), 600.0) == pytest.approx(2.5, rel=1e-15)
    assert bloc.interets_sur_depots(pas(0.02), 700.0, 110.0) == pytest.approx(
        (0.02 * 700.0 / 12, 0.02 * 110.0 / 12), rel=1e-15)
    i, iL, iD = pas(0.04), pas(0.05), pas(0.02)
    assert bloc.resultat(iL, 600.0, i, 290.0, i, 0.0, iD, 700.0, 110.0, i, 20.0) == \
        pytest.approx((0.05 * 600 + 0.04 * 290 - 0.02 * 810 - 0.04 * 20) / 12, rel=1e-14)
    assert bloc.dividendes(60.0, 2.05, 0.1, 600.0, 10.0) == pytest.approx(1.05, rel=1e-13)
    assert bloc.dividendes(50.0, 2.05, 0.1, 600.0, 10.0) == 0.0
    assert bloc.refinancement(-0.5, 20.0) == 0.5
    assert bloc.refinancement(5.0, 20.0) == -5.0
    assert bloc.refinancement(24.5, 20.0) == -20.0
    assert bloc.fonds_propres(600.0, 290.0, 0.0, 700.0, 110.0, 20.0) == 60.0


@pytest.mark.parametrize("graine", range(5))
def test_fonds_propres_sur_six_positions_egaux_a_la_valeur_nette_du_noyau(graine):
    """ADR 0013, annotation du 14/11/2026, point 5 : E^Bk calculé par le bloc sur les six positions
    (L + B_Bk + Res − D_H − D_F − L^CB) égale `valeur_nette_stock` de la banque, à ε × S^Bk (et
    au bit : même ordre de sommation que `catalogue.POSTES_DU_BILAN`), positions tirées (graine
    déclarée), signes quelconques, D_H et D_F négatifs compris."""
    rng = np.random.default_rng(20261115 + graine)
    for _ in range(1000):
        x = (rng.standard_normal(6) * np.exp(rng.uniform(-10, 10, 6))).tolist()
        p = positions(L=x[0], B_Bk=x[1], Res=x[2], D_H=x[3], D_F=x[4], L_CB=x[5])
        e_bloc = bloc.fonds_propres(p["L"], p["B_Bk"], p["Res"], p["D_H"], p["D_F"], p["L_CB"])
        e_noyau = idt.valeur_nette_stock(p, "banque")
        assert abs(e_bloc - e_noyau) <= EPSILON * idt.echelle_bilan(p, "banque")
        assert e_bloc == e_noyau


# --------------------------------------------------------------------------
# Cas à la main (§ banque-refinancement ; fiche 7, § 3.K) et ses trois variantes
# --------------------------------------------------------------------------

# Ouverture du cas : L = 600, B_Bk = 290, Res = 0, L^CB = 20, D_H = 700, D_F = 110, d'où E^Bk =
# 60 ; M^G = 20, B_CB = 0 ; i_CB relevé de 3 à 4 % au tour, i_L = 5 % et i_D = 2 % d'ouverture ;
# ϑ = 0,1 ; crédit demandé 10, dépense publique 30, impôts 28.
CAS = {"L": 600.0, "B_Bk": 290.0, "Res": 0.0, "L_CB": 20.0, "D_H": 700.0, "D_F": 110.0,
       "M_G": 20.0}


def cas_a_la_main(credit=10.0, M_G_cible=20.0, achat=0.0):
    """Le cas déroulé par appel direct de B3 à B7 ; la souscription (E11 du bloc 9) et l'achat
    19b-banque (J6) sont des données de l'appel. Rend les lignes et les positions de clôture,
    par les flux."""
    o = CAS
    i, iL, iD = pas(0.04), pas(0.05), pas(0.02)
    G, T = 30.0, 28.0
    E = bloc.fonds_propres(o["L"], o["B_Bk"], o["Res"], o["D_H"], o["D_F"], o["L_CB"])
    l9 = bloc.interets_sur_credits(iL, o["L"])
    l10_H, l10_F = bloc.interets_sur_depots(iD, o["D_H"], o["D_F"])
    Pi = bloc.resultat(iL, o["L"], i, o["B_Bk"], i, o["Res"], iD, o["D_H"], o["D_F"], i, o["L_CB"])
    Div = bloc.dividendes(E, Pi, 0.1, o["L"], credit)
    l11b, l12, l13 = i * o["B_Bk"], i * o["Res"], i * o["L_CB"]
    Pi_CB = i * o["L_CB"]  # BC6 au socle (B_CB = Res = 0)
    souscription = G + l11b - T - Pi_CB + M_G_cible - o["M_G"]  # E9 à E11 (θ_CB = 0)
    Res_8b = o["Res"] + G - T + l11b + l12 - l13 - souscription + achat
    l21 = bloc.refinancement(Res_8b, o["L_CB"])
    cloture = {"L": o["L"] + credit, "B_Bk": o["B_Bk"] + souscription - achat,
               "Res": Res_8b + l21, "L_CB": o["L_CB"] + l21,
               "D": o["D_H"] + o["D_F"] + credit + G - T - l9 + l10_H + l10_F + Div}
    return {"E": E, "l9": l9, "l10": l10_H + l10_F, "Pi": Pi, "Div": Div, "l21": l21,
            "souscription": souscription, "Res_8b": Res_8b, "cloture": cloture}


@pytest.mark.parametrize("variante, credit, M_G_cible, achat, attendus", [
    ("base", 10.0, 20.0, 0.0,
     {"souscription": 2.9, "l21": 0.0, "L_CB": 20.0, "Res": 0.0, "Div": 1.05, "E_1": 61.0}),
    ("position négative", 10.0, 20.5, 0.0,
     {"souscription": 3.4, "l21": 0.5, "L_CB": 20.5, "Res": 0.0, "Div": 1.05, "E_1": 61.0}),
    ("position positive", 10.0, 20.5, 25.0,
     {"souscription": 3.4, "l21": -20.0, "L_CB": 0.0, "Res": 4.5, "Div": 1.05, "E_1": 61.0}),
    ("refus de la moitié", 5.0, 20.0, 0.0,
     {"souscription": 2.9, "l21": 0.0, "L_CB": 20.0, "Res": 0.0, "Div": 1.55, "E_1": 60.5}),
])
def test_cas_a_la_main_quatre_variantes(variante, credit, M_G_cible, achat, attendus):
    """Fiche 7, § 9.6, « Cas à la main », et `sec:banque-refinancement` : lignes 9 = 2,5, 10 = 1,35,
    Π^Bk = 2,05 ; ligne 15 et ligne 21 de chaque variante ; L^CB et Res de clôture (Res = 4,5 =
    B_CB − M^G* après l'achat de 25) ; E^Bk de clôture par le stock et par les flux, égale à ϑ
    fois les crédits de clôture ; contrainte budgétaire ΔL + ΔB_Bk + ΔRes − (ΔD + ΔL^CB) − (Π −
    Div) = 0 ; Res L^CB = 0 exactement ; à 1e−12 × S^Bk. La variante « refus de la moitié »
    sert un crédit de 5 (clause du bloc 6, donnée de l'appel)."""
    c = cas_a_la_main(credit, M_G_cible, achat)
    k = c["cloture"]
    p = positions(L=k["L"], B_Bk=k["B_Bk"], Res=k["Res"], L_CB=k["L_CB"], D_H=k["D"])
    S = idt.echelle_bilan(p, "banque")
    e_stock = idt.valeur_nette_stock(p, "banque")
    e_flux = c["E"] + c["Pi"] - c["Div"]
    obtenus = {"ligne 9": (c["l9"], 2.5), "ligne 10": (c["l10"], 1.35), "Π^Bk": (c["Pi"], 2.05),
               "E^Bk_0": (c["E"], 60.0), "souscription": (c["souscription"],
                                                          attendus["souscription"]),
               "ligne 15": (c["Div"], attendus["Div"]), "ligne 21": (c["l21"], attendus["l21"]),
               "L^CB": (k["L_CB"], attendus["L_CB"]), "Res": (k["Res"], attendus["Res"]),
               "E^Bk stock": (e_stock, attendus["E_1"]), "E^Bk flux": (e_flux, attendus["E_1"]),
               "E^Bk = ϑ L_1": (e_stock, 0.1 * k["L"])}
    for nom, (obtenu, attendu) in obtenus.items():
        assert abs(obtenu - attendu) <= SEUIL_CAS_A_LA_MAIN * S, (variante, nom, obtenu)
    o = CAS
    budget = ((k["L"] - o["L"]) + (k["B_Bk"] - o["B_Bk"]) + (k["Res"] - o["Res"])
              - ((k["D"] - o["D_H"] - o["D_F"]) + (k["L_CB"] - o["L_CB"])) - (c["Pi"] - c["Div"]))
    assert abs(budget) <= SEUIL_CAS_A_LA_MAIN * S, variante
    assert k["Res"] >= 0.0 and k["L_CB"] >= 0.0 and k["Res"] * k["L_CB"] == 0.0


# --------------------------------------------------------------------------
# C29, boucle propre, neutralité des achats de titres, (d1), bornes
# --------------------------------------------------------------------------


def _ouverture_du_script(stationnaire, pi=0.02, n_a=12):
    par = replace(stationnaire.Parametres(), pi_cible=pi, n_a=n_a, nu_G=1.15)
    e = stationnaire.etat_stationnaire(par)
    return par, e, stationnaire.ouverture(e, par), e["Gam"]


def _pi_bk(o, i_CB, i_L, i_D, n_a=N_A):
    """B5 sur les encours `o` aux taux annuels donnés, i_B ≡ i_res ≡ i_CB."""
    i, iL, iD = i_CB / n_a, i_L / n_a, i_D / n_a
    return bloc.resultat(iL, o["L"], i, o["B_Bk"], i, o["Res"], iD, o["D_H"], o["D_F"], i,
                         o["L_CB"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
@pytest.mark.parametrize("delta", [0.01, -0.01])
def test_c29_saut_d_un_tour_du_resultat(stationnaire, pi, delta):
    """C29 (fiche 7, § 9.6), par appel direct, en équilibre partiel (encours d'ouverture du script
    tenus), i_B = i_res = i_CB du tour : au tour n d'une décision de Δ, i_L et i_D inchangés,
    ΔΠ^Bk = Δ (B_Bk + Res − L^CB)/n_a = Δ (B − M^G − E^CB)/n_a (bilan de la banque centrale,
    B_H = 0) ; au tour n + 1, i_L et i_D relevés par B1 et B2, ΔΠ^Bk = Δ E^Bk/n_a ; à 1e−12
    relatif."""
    par, e, o, _ = _ouverture_du_script(stationnaire, pi)
    i0 = e["i_CB"]
    base = _pi_bk(o, i0, o["i_L"], o["i_D"])
    tour_n = _pi_bk(o, i0 + delta, o["i_L"], o["i_D"])
    i_L1 = bloc.taux_des_credits_suivant(i0 + delta, par.varpi_L)
    i_D1 = bloc.taux_des_depots_suivant(i0 + delta, par.varpi_D)
    tour_n1 = _pi_bk(o, i0 + delta, i_L1, i_D1)
    B = o["B_H"] + o["B_Bk"] + o["B_CB"]
    attendu_n = delta * (B - o["M_G"] - o["E_CB"]) / N_A
    assert abs((tour_n - base) / attendu_n - 1.0) <= SEUIL_C29
    assert abs((tour_n - base) / (delta * (o["B_Bk"] + o["Res"] - o["L_CB"]) / N_A) - 1.0) \
        <= SEUIL_C29
    E = bloc.fonds_propres(o["L"], o["B_Bk"], o["Res"], o["D_H"], o["D_F"], o["L_CB"])
    assert abs((tour_n1 - base) / (delta * E / N_A) - 1.0) <= SEUIL_C29


def _trajectoire_partielle(o, gam, i_CB, varpi_L, varpi_D, vartheta, E_0, nb):
    """Équilibre partiel : encours de la banque sur leur sentier (× Γ̄ par pas), crédit exécuté
    L_t (Γ̄ − 1), taux directeur exogène `i_CB(t)` ; i_L et i_D suivent B1 et B2 (écrits au pas
    t, lus au pas t + 1), E^Bk suit E_{t+1} = E_t + Π_t − Div_t. Rend, par pas, (i_CB, i_L, i_D,
    Π, Div, E_t, L_t, L_{t+1})."""
    i_L, i_D, E = o["i_L"], o["i_D"], E_0
    rendus = []
    for t in range(nb):
        f = gam ** t
        enc = {k: o[k] * f for k in ("L", "B_Bk", "Res", "L_CB", "D_H", "D_F")}
        dL = enc["L"] * (gam - 1.0)
        i = i_CB(t)
        Pi = _pi_bk(enc, i, i_L, i_D)
        Div = bloc.dividendes(E, Pi, vartheta, enc["L"], dL)
        rendus.append((i, i_L, i_D, Pi, Div, E, enc["L"], enc["L"] + dL))
        E = E + Pi - Div
        i_L = bloc.taux_des_credits_suivant(i, varpi_L)
        i_D = bloc.taux_des_depots_suivant(i, varpi_D)
    return rendus


def test_boucle_propre_ancre_des_fonds_propres(stationnaire):
    """Fiche 7, § 9.6, « Boucle propre » (critère 10 (b)) : taux et demande exogènes, E^Bk_0 =
    0,9 ϑ L_0 : le plancher du dividende est actif tant que les fonds propres sont sous l'ancre,
    puis, dès le premier pas où Div_Bk > 0, E^Bk_{t+1} = ϑ L_{t+1} à 1e−12 relatif, à chaque pas
    suivant (module 0 : aucune vitesse)."""
    par, e, o, gam = _ouverture_du_script(stationnaire)
    rendus = _trajectoire_partielle(o, gam, lambda t: e["i_CB"], par.varpi_L, par.varpi_D,
                                    par.vartheta, 0.9 * par.vartheta * o["L"], 24)
    premier = next(t for t, r in enumerate(rendus) if r[4] > 0.0)
    assert premier >= 1  # le plancher est actif au premier pas
    for i, i_L, i_D, Pi, Div, E, L, L_1 in rendus[premier:]:
        assert Div > 0.0
        assert abs((E + Pi - Div) / (par.vartheta * L_1) - 1.0) <= SEUIL_BOUCLE_PROPRE


@pytest.mark.parametrize("scenario", ["taux nul", "taux + 5 points"])
def test_bornes_scenarios_de_taux_en_equilibre_partiel(stationnaire, scenario):
    """Fiche 7, § 9.6, « Bornes », partie (a) : sous un taux directeur à 0 pendant 12 tours, puis
    relevé de 5 points pendant 12 tours (depuis l'état résolu à 2 %, puis retour), en équilibre
    partiel : i_D = i_CB − ϖ_D exactement (à 1e−15), même négatif (aucun plancher), et i_L = i_CB
    + ϖ_L, au tour suivant ; le plancher Div_Bk ≥ 0 inactif sur toute la fenêtre de 48 pas
    (critère de la fiche : inactif, ou désactivé au plus tard 12 tours après la fin du choc ;
    la mesure le tient inactif, réserve R3 de `monnaie`) ; ancre E^Bk = ϑ L dès que le
    dividende est positif."""
    par, e, o, gam = _ouverture_du_script(stationnaire)
    i0 = e["i_CB"]
    choc = 0.0 if scenario == "taux nul" else i0 + 0.05

    def i_CB(t):
        return choc if 1 <= t <= 12 else i0

    rendus = _trajectoire_partielle(o, gam, i_CB, par.varpi_L, par.varpi_D, par.vartheta,
                                    o["E_Bk"], 48)
    for t in range(1, len(rendus)):
        i_prec = rendus[t - 1][0]
        assert abs(rendus[t][2] - (i_prec - par.varpi_D)) <= SEUIL_I_D
        assert abs(rendus[t][1] - (i_prec + par.varpi_L)) <= SEUIL_I_D
    if scenario == "taux nul":
        assert min(r[2] for r in rendus) < 0.0  # i_D négatif, sans plancher
    # Réserve R3 de `monnaie` : le plancher de B6 reste inactif sur toute la fenêtre de 48 pas
    # (Div_Bk > 0 à chaque pas) ; Div/Π au plus bas est publié par
    # `tests/invariants/test_banque.py::test_bornes_plancher_inactif_publie`.
    assert all(r[4] > 0.0 for r in rendus)


def test_d1_taux_releves_d_un_point_au_tour_suivant(stationnaire):
    """(d1) de `jeu` (fiche 7, § 7 et § 9.6) : taux directeur relevé d'un point aux tours 1 à 12,
    en équilibre partiel : i_L et i_D relevés d'un point au tour n + 1 (au moins 0,5 point), par
    B1 et B2, exactement à 1e−15 ; inchangés au tour n."""
    par, e, o, gam = _ouverture_du_script(stationnaire)
    i0 = e["i_CB"]
    rendus = _trajectoire_partielle(o, gam, lambda t: i0 + 0.01 if 1 <= t <= 12 else i0,
                                    par.varpi_L, par.varpi_D, par.vartheta, o["E_Bk"], 3)
    assert rendus[1][1] == rendus[0][1] and rendus[1][2] == rendus[0][2]
    for k in (1, 2):
        hausse = rendus[2][k] - rendus[1][k]
        assert abs(hausse - 0.01) <= SEUIL_I_D and hausse >= 0.005


@pytest.mark.parametrize("facteur", [0.5, 1.0, 2.0, 0.0])
def test_neutralite_des_achats_de_titres(facteur):
    """Fiche 7, § 9.6, « Neutralité des achats de titres » (avis de `jeu`) et partie (a) de
    « Réserves et refinancement » (achat 19b-banque) : sur le cas à la main, un achat x = facteur
    × L^CB de titres à la banque (appel direct de B7) baisse B_Bk de x et L^CB de min(x ; L^CB) ;
    les réserves ne montent qu'au-delà de L^CB = M^G* + E^CB − B_CB ; le résultat du tour suivant
    (B5 sur les encours de clôture, i_B = i_res = i_CB), la masse monétaire et les taux (B1, B2)
    sont inchangés, à 1e−12 relatif."""
    base = cas_a_la_main()
    x = facteur * CAS["L_CB"]
    apres = cas_a_la_main(achat=x)
    kb, ka = base["cloture"], apres["cloture"]
    assert abs(ka["B_Bk"] - (kb["B_Bk"] - x)) <= SEUIL_NEUTRALITE * kb["B_Bk"]
    assert abs((kb["L_CB"] - ka["L_CB"]) - min(x, kb["L_CB"])) <= SEUIL_NEUTRALITE * kb["L_CB"]
    assert abs(ka["Res"] - max(0.0, x - kb["L_CB"])) <= SEUIL_NEUTRALITE * kb["L_CB"]
    assert ka["D"] == kb["D"]
    i = 0.04

    def suivant(k):
        enc = {"L": k["L"], "B_Bk": k["B_Bk"], "Res": k["Res"], "L_CB": k["L_CB"],
               "D_H": k["D"], "D_F": 0.0}
        return _pi_bk(enc, i, 0.06, 0.03)

    assert abs(suivant(ka) / suivant(kb) - 1.0) <= SEUIL_NEUTRALITE
    # Taux inchangés : B1 et B2 ne prennent que le taux directeur et l'écart, aucune position.
    for f in (bloc.taux_des_credits_suivant, bloc.taux_des_depots_suivant):
        assert len(inspect.signature(f).parameters) == 2


# --------------------------------------------------------------------------
# B7 dans ses trois cas, sur tirages (critère 1 du 07/10/2026)
# --------------------------------------------------------------------------


def test_b7_trois_cas_sur_tirages_res_et_l_cb_exacts():
    """Critères 1 à 3 du 07/10/2026 et ADR 0013, annotation du 14/11/2026, point 9 : sur 10^6
    tirages à graine déclarée (20261115), Res^{8b} de signe quelconque, L^CB ≥ 0 (nul compris),
    B7 sous la forme −min donne, la ligne 21 ajoutée aux deux positions comme le fait le noyau,
    Res_{t+1} ≥ 0, L^CB_{t+1} ≥ 0 et Res_{t+1} L^CB_{t+1} = 0 exactement, dans les trois cas
    (découvert couvert, remboursement partiel, remboursement total), chacun représenté ; la
    forme littérale max(L^CB − Res^{8b} ; 0) − L^CB, évaluée par le test sur les mêmes tirages,
    échoue sur une partie d'entre eux (pouvoir discriminant, publié)."""
    rng = np.random.default_rng(GRAINE_B7)
    L = np.exp(rng.uniform(-30.0, 30.0, NB_TIRAGES))
    L[rng.random(NB_TIRAGES) < 0.05] = 0.0
    echelle = np.where(L > 0.0, L, np.exp(rng.uniform(-30.0, 30.0, NB_TIRAGES)))
    R = echelle * rng.uniform(-2.0, 2.0, NB_TIRAGES)
    proches = rng.random(NB_TIRAGES) < 0.1
    R[proches] = L[proches] * (1.0 + rng.uniform(-1e-15, 1e-15, int(proches.sum())))
    cas = {"découvert couvert": 0, "remboursement partiel": 0, "remboursement total": 0}
    litterale = 0
    debut = time.perf_counter()
    for r, lcb in zip(R.tolist(), L.tolist()):
        d = bloc.refinancement(r, lcb)
        res_1, lcb_1 = r + d, lcb + d
        assert res_1 >= 0.0 and lcb_1 >= 0.0 and res_1 * lcb_1 == 0.0, (r, lcb)
        cas["découvert couvert" if r < 0.0 else "remboursement partiel" if r < lcb
            else "remboursement total"] += 1
        dl = max(lcb - r, 0.0) - lcb
        if not (r + dl >= 0.0 and lcb + dl >= 0.0 and (r + dl) * (lcb + dl) == 0.0):
            litterale += 1
    duree = time.perf_counter() - debut
    assert all(n >= 0.1 * NB_TIRAGES for n in cas.values()), cas
    assert litterale > 0
    assert duree < 30.0, duree


# --------------------------------------------------------------------------
# Formes du bloc et du script d'état stationnaire (P93 ; P77)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
@pytest.mark.parametrize("n_a", [4, 12, 52])
def test_formes_du_bloc_egales_au_script(stationnaire, pi, n_a):
    """P93 et P77 : B1 à B7 du bloc, évaluées sur l'ouverture stationnaire du script (`ouverture`,
    ν_G = 1,15) et sur ses grandeurs du pas 0 (i_CB, ΔL, Res^{8b}), égalent les règles du pas 0
    du script (`un_pas`) : i_{L,1}, i_{D,1} et la ligne 21 au bit (B7 en −min dans les deux),
    lignes 9 et 10, Π^Bk et Div_Bk à 1e−13 × S^Bk (taux convertis au pas avant le produit dans
    le bloc, après dans le script) ; E^Bk sur les six positions égal à E^Bk du script à ε × S^Bk ;
    et la fiche 7, § 9.6, « État stationnaire », à 1e−10 : i_L − i_CB = ϖ_L, i_CB − i_D = ϖ_D,
    E^Bk/L = ϑ, Res_1 L^CB_1 = 0 exactement. Les taux par pas sont convertis par le test au n_a
    du point (le moteur ne s'exécute qu'à n_a = 12)."""
    par = replace(stationnaire.Parametres(), pi_cible=pi, n_a=n_a, nu_G=1.15)
    e = stationnaire.etat_stationnaire(par)
    o = stationnaire.ouverture(e, par)
    s = stationnaire.un_pas(o, par)
    i_CB = s["i_CB"]
    i, iL, iD = i_CB / n_a, o["i_L"] / n_a, o["i_D"] / n_a
    D_H, D_F = max(0.0, o["D_H"]), max(0.0, o["D_F"])
    E = bloc.fonds_propres(o["L"], o["B_Bk"], o["Res"], o["D_H"], o["D_F"], o["L_CB"])
    l9 = bloc.interets_sur_credits(iL, o["L"])
    l10_H, l10_F = bloc.interets_sur_depots(iD, D_H, D_F)
    Pi = bloc.resultat(iL, o["L"], i, o["B_Bk"], i, o["Res"], iD, D_H, D_F, i, o["L_CB"])
    Div = bloc.dividendes(E, Pi, par.vartheta, o["L"], s["dL"])
    l21 = bloc.refinancement(s["Res_8b"], o["L_CB"])
    assert bloc.taux_des_credits_suivant(i_CB, par.varpi_L).hex() == s["i_L_1"].hex()
    assert bloc.taux_des_depots_suivant(i_CB, par.varpi_D).hex() == s["i_D_1"].hex()
    assert l21.hex() == s["dL_CB"].hex()
    p = positions(**{k: o[k] for k in ("L", "B_Bk", "Res", "L_CB", "D_H", "D_F")})
    S = idt.echelle_bilan(p, "banque")
    for nom, x, y in (("l9", l9, s["l9"]), ("l10_H", l10_H, s["l10_H"]),
                      ("l10_F", l10_F, s["l10_F"]), ("Π^Bk", Pi, s["Pi_Bk"]),
                      ("Div_Bk", Div, s["Div_Bk"])):
        assert abs(x - y) <= 1e-13 * S, (nom, x, y)
    assert abs(E - o["E_Bk"]) <= EPSILON * S
    res_1, lcb_1 = s["Res_8b"] + l21, o["L_CB"] + l21
    assert res_1 >= 0.0 and lcb_1 >= 0.0 and res_1 * lcb_1 == 0.0
    assert s["Res_1"] == res_1 == 0.0
    ecarts = {
        "i_L − i_CB = ϖ_L": abs((s["i_L_1"] - i_CB) / par.varpi_L - 1.0),
        "i_CB − i_D = ϖ_D": abs((i_CB - s["i_D_1"]) / par.varpi_D - 1.0),
        "E^Bk_1/L_1 = ϑ": abs((E + Pi - Div) / (o["L"] + s["dL"]) / par.vartheta - 1.0),
    }
    for nom, x in ecarts.items():
        assert x <= SEUIL_ETAT_STATIONNAIRE, (nom, x)


def test_script_execute_b7_sous_la_forme_moins_min(stationnaire):
    """P93 : le script d'état stationnaire exécute B7 sous la forme −min, comme le bloc : sur la
    grille π̄ × n_a × ν_G ∈ {1 ; 1,15} (18 points), Res_1 = 0 exactement et la ligne 21 égale
    `refinancement(Res^{8b}, L^CB)` au bit ; avant l'alignement, Res_1 valait de −2,1e−17 à
    +1,9e−17 (16 points sur 18 non nuls, mesure du compte rendu de #90)."""
    for nu in (1.0, 1.15):
        for pi in (0.0, 0.02, 0.10):
            for n_a in (4, 12, 52):
                par = replace(stationnaire.Parametres(), pi_cible=pi, n_a=n_a, nu_G=nu)
                o = stationnaire.ouverture(stationnaire.etat_stationnaire(par), par)
                s = stationnaire.un_pas(o, par)
                assert s["dL_CB"] == bloc.refinancement(s["Res_8b"], o["L_CB"])
                assert s["Res_1"] == 0.0 and s["L_CB_1"] >= 0.0


# --------------------------------------------------------------------------
# Contrat de poussière : la méthode de phase 6 lit D_H et D_F en max(0 ; ·)
# --------------------------------------------------------------------------


class _VueDEssai:
    """Vue d'essai de la phase 6 : l'ouverture, la table du bloc 7, i_CB du tour et la ligne 18
    exécutée ; relève les propositions et les écritures. Elle n'est pas la vue du moteur (aucun
    contrôle de droits) : elle isole le câblage de la méthode."""

    def __init__(self, ouverture, i_CB, delta_L):
        self.ouverture = types.SimpleNamespace(**ouverture)
        self.parametres = PARAMETRES_DE_REFERENCE
        self._i_CB, self._delta_L = i_CB, delta_L
        self.grand_livre = types.SimpleNamespace(
            montant_execute_ligne=lambda ligne: {"18": self._delta_L}[ligne])
        self.propose, self.pas = {}, {}

    def lire(self, nom):
        return {"i_CB": self._i_CB}[nom]

    def ecrire_pas(self, nom, valeur):
        self.pas[nom] = valeur

    def proposer(self, ligne, montants):
        self.propose[ligne] = dict(montants)


# Échelle du bilan du détenteur d'un dépôt, déclarée pour les cas « −0,5 ε × S » de la vue d'essai
# (ordre de grandeur des bilans du cas à la main), u.m.
S_DU_DETENTEUR = 1000.0
# Plus petit flottant négatif, « −1 ulp » de zéro (ADR 0013, A8.2).
MOINS_UN_ULP = -math.ulp(0.0)


@pytest.mark.parametrize("D_H, D_F", [
    (-1e-13, 110.0), (700.0, -1e-14), (-2e-15, -3e-15), (700.0, 110.0),
    # Cas discriminants (réserve R1 de `monnaie`, reprise du rang 5) : l'autre dépôt nul, si bien
    # que D_H + D_F n'absorbe pas le dépôt négatif ; max(0 ; ·) ne dépend pas de sa taille.
    (0.0, -0.25), (-0.25, 0.0),
    # Cas prescrits par l'ADR 0013, A8.2 : −1 ulp et −0,5 ε × S du détenteur.
    (0.0, MOINS_UN_ULP), (MOINS_UN_ULP, 0.0),
    (0.0, -0.5 * EPSILON * S_DU_DETENTEUR), (-0.5 * EPSILON * S_DU_DETENTEUR, 0.0),
])
def test_contrat_de_poussiere_d_h_et_d_f_lus_en_max_zero(D_H, D_F):
    """Critère 4 du 07/10/2026 (part du bloc 7 de #103) et ADR 0013, A8.2 : un dépôt d'ouverture
    négatif (poussière admise par la lecture nette du noyau, D + ε S ≥ 0, testée à −1 ulp et à
    −0,5 ε × S ; et −0,25, la règle ne dépendant pas de la taille) est lu en max(0 ; ·) par la
    phase 6 : terme de la ligne 10 nul, Π^Bk sans ce terme ; E^Bk, identité de bilan, porte la
    position telle quelle. Chaque valeur est comparée au bit à la forme recalculée par le test,
    sur la méthode `phase_6` du bloc appelée avec une vue d'essai."""
    ouverture = {"L": 600.0, "B_Bk": 290.0, "Res": 3.0, "L_CB": 20.0, "D_H": D_H, "D_F": D_F,
                 "i_L": 0.05, "i_D": 0.02}
    vue = _VueDEssai(ouverture, 0.04, 10.0)
    bloc.Banque().phase_6(vue)
    iL, iD, i = 0.05 / N_A, 0.02 / N_A, 0.04 / N_A
    dh, df = max(0.0, D_H), max(0.0, D_F)
    assert vue.propose["10"] == {"iD_DH": iD * dh, "iD_DF": iD * df}
    assert vue.propose["9"] == {"iL_L": iL * 600.0}
    pi_bk = iL * 600.0 + i * 290.0 + i * 3.0 - iD * (dh + df) - i * 20.0
    assert vue.pas["Pi_Bk"] == pi_bk
    e_bk = -D_H - D_F + 600.0 + 290.0 + 3.0 - 20.0
    assert vue.propose["15"] == {"Div_Bk": max(0.0, e_bk + pi_bk - TABLE.vartheta * 610.0)}


# --------------------------------------------------------------------------
# Phases, empreinte, monnaie endogène, déclaration (inspection)
# --------------------------------------------------------------------------


def test_declaration_conforme_a_tab_banque_phases():
    """`tab:banque-phases` et ADR 0013, annotation du 14/11/2026, point 5 : sièges en phases 6 et
    8 (c) seulement (aucune écriture en phases 3 et 7) ; en phase 6, lectures de l'ouverture L,
    B_Bk, Res, L^CB, D_H, D_F, i_L, i_D, de i_CB (phase 1) et de la ligne 18 exécutée (phase 3),
    rien d'autre ; écriture Π^Bk ; lignes 9, 10, 15 ; en 8 (c), position Res au grand livre, L^CB
    d'ouverture, i_CB ; ligne 21 ; états i_L, i_D ; aucune ligne 18 ni 19a, aucun montant
    couvert ; aucune variable `i_res` ni `i_B` ; aucune lecture de valeur nette."""
    sieges = {s.etape: s for s in bloc.Banque.declaration.sieges}
    assert tuple(sieges) == ("6", "8c")
    assert set(sieges["6"].lit) == {Lecture(OUVERTURE, n) for n in (
        "L", "B_Bk", "Res", "L_CB", "D_H", "D_F", "i_L", "i_D")} | {
        Lecture("1", "i_CB"), Lecture(GRAND_LIVRE, "18")}
    assert sieges["6"].ecrit == ("Pi_Bk",) and sieges["6"].etat == ()
    assert set(sieges["8c"].lit) == {Lecture(GRAND_LIVRE, "Res"), Lecture(OUVERTURE, "L_CB"),
                                     Lecture("1", "i_CB")}
    assert sieges["8c"].ecrit == () and sieges["8c"].etat == ("i_L", "i_D")
    assert [s.propose for s in sieges.values()] == [("9", "10", "15"), ("21",)]
    assert all(s.couvre == () for s in sieges.values())
    ecrits = {n for s in sieges.values() for n in s.ecrit + s.etat}
    assert not ecrits & {"i_res", "i_B"}


def test_monnaie_endogene_le_bloc_ne_propose_pas_le_credit():
    """Fiche 7, § 9.6, « Monnaie endogène », partie (a) : la banque ne siège pas en phase 3 et ne
    propose pas la ligne 18 (proposant : le bloc investissement, au catalogue du noyau) ; aucune
    de ses lectures n'entre dans la phase 3 : le crédit servi ne dépend ni des réserves ni du
    refinancement d'ouverture. La ligne 18 est une porte de la masse monétaire (dépôts des
    entreprises, contrepartie 17). La partie ς_L et ΔM = ΔL exécuté relèvent du bloc 6 (J3-d)."""
    assert cat.LIGNE["18"].proposant == "investissement" and cat.LIGNE["18"].phase == "3"
    assert all(s.etape != "3" for s in bloc.Banque.declaration.sieges)
    assert all("18" not in s.propose for s in bloc.Banque.declaration.sieges)


def test_empreinte_deux_variables_d_etat():
    """Fiche 7, § 9.6, « Empreinte », partie (a) : deux variables d'état (i_L, i_D) au radical
    `banque`, scalaires, écrites en phase 8 (c), par an, taux de flux, dans l'ordre du schéma
    avant celles du bloc 8 (ADR 0013, annotation du 14/11/2026, point 3) ; aucun registre, aucun
    tirage : le module n'importe que `contrat_bloc` et `conversions` ; le bloc n'a pas
    d'attribut d'instance."""
    variables = [v for v in schema.VARIABLES_DES_BLOCS if v.proprietaire == "banque"]
    assert [(v.nom, v.phase_ecriture, v.unite) for v in variables] == [
        ("i_L", "8c", "par an, taux de flux"), ("i_D", "8c", "par an, taux de flux")]
    assert all(v.type is float and v.longueur == 1 for v in variables)
    noms = [v.nom for v in schema.VARIABLES_DES_BLOCS]
    assert noms.index("i_D") + 1 == noms.index("pi_e")
    arbre = ast.parse(inspect.getsource(bloc))
    importes = {n.module for n in ast.walk(arbre) if isinstance(n, ast.ImportFrom)}
    importes |= {a.name for n in ast.walk(arbre) if isinstance(n, ast.Import) for a in n.names}
    assert importes == {"__future__", "nations.moteur.contrat_bloc",
                        "nations.moteur.conversions"}
    instance = bloc.Banque()
    assert not hasattr(instance, "__dict__") and bloc.Banque.__slots__ == ()


def test_domaine_de_i_l_et_i_d_finitude_seule():
    """ADR 0013, annotation du 14/11/2026, point 4 : i_L et i_D sans condition de signe (i_D
    négatif sans plancher : M31, lecture (d)), refusés seulement non finis, par la seule
    fonction de domaine du schéma."""
    for nom in ("i_L", "i_D"):
        for x in (-0.9, -0.01, 0.0, 3.0):
            assert schema.defaut_de_domaine(nom, x) is None
        for x in (math.inf, -math.inf, math.nan):
            assert "non fini" in schema.defaut_de_domaine(nom, x)
