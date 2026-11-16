"""Bloc 6, investissement et financement des entreprises : lignes « J3 » de classe (a) de la fiche 6
(#67), table du bloc 6, domaine strict de K (P80) et lectures nettes de D_F (#103).

Classe (a) du classement du rang 1a de J3-d1 (avis de `macro`, § 1 ; fiche 6, § 9.6) : état
stationnaire de S1 à S7 et F1 à F4 par appel direct sur l'ouverture du script, π* ∈ {0 ; 2 ;
10 %} et n_a ∈ {4 ; 12 ; 52} (P77) ; F4 sous T_{F,t−1} ≠ 0 (avis, § 2) ; cas à la main (§ 3.F)
sur le grand livre ; répartition d'un choc de résultat ; bornes (b) ; phases et empreinte
(inspection). (d1), (d2), la frontière de la double précision des bornes (b) et l'ajout du 14/11
(b) sont publiés par `tests/invariants/test_investissement.py`. S'y ajoutent la
lecture nette de D_F dans F3 à −1 ulp et à −0,5 ε S (ADR 0013, annotation du 14/11/2026 (rang
1b de J3-d1), point 4), le domaine strict de K par la monotonie de l'arrondi (point 3) et les
domaines de l'état (point 1). Lignes de classe (b) : `tests/invariants/test_investissement.py`.
Seuils écrits avant l'essai (fiche 6, § 9.6 ; critère de #67, `docs/feuille-de-route.md` § 1),
non déplacés.
"""

import ast
import dataclasses
import inspect
import math

import numpy as np
import pytest

from nations.blocs import investissement as bloc
from nations.etat import schema
from nations.moteur.contrat_bloc import GRAND_LIVRE, OUVERTURE, REGISTRE, Lecture
from nations.moteur.conversions import facteur_par_pas, par_pas
from nations.moteur.parametres import TauxDeCroissance, TauxDeFlux, varier
from nations.moteur.parametres import investissement as table_investissement
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.grand_livre import FluxPropose, ouvrir_pas

N_A = PARAMETRES_DE_REFERENCE.cadre.pas_par_an
TABLE = PARAMETRES_DE_REFERENCE.investissement
EPSILON = PARAMETRES_DE_REFERENCE.cadre.tolerance_identite_pas
# Seuils écrits avant l'essai (fiche 6, § 9.6).
SEUIL_ETAT_STATIONNAIRE = 1e-10  # relatif
SEUIL_CAS = 1e-12  # × S
SEUIL_CHOC_DE_RESULTAT = 1e-12  # relatif
SEUIL_LEVIER = 1e-12  # relatif
POINTS_PI = (0.0, 0.02, 0.10)
POINTS_N_A = (4, 12, 52)
GRAINE = 20261114


def ecart(x, reference):
    return abs(x) if reference == 0.0 else abs(x / reference - 1.0)


def facteurs(pi, n_a, g_pr=0.02, g_N=0.0):
    """(1 + g)^{1/n_a}, π^{∗,pas} et Γ^e : à n_a = 12 par les conversions du moteur (forme de
    `facteur_g` et de Γ^e, `nations.moteur.ouverture`), ailleurs par la forme du script."""
    if n_a == N_A:
        f_g = facteur_par_pas(TauxDeCroissance(g_pr)) * facteur_par_pas(TauxDeCroissance(g_N))
        f_pi = facteur_par_pas(TauxDeCroissance(pi))
        return f_g, f_pi - 1.0, f_g * f_pi
    g = (1 + g_pr) * (1 + g_N) - 1
    return (1 + g) ** (1 / n_a), (1 + pi) ** (1 / n_a) - 1, ((1 + g) * (1 + pi)) ** (1 / n_a)


# --------------------------------------------------------------------------
# État stationnaire par appel direct (classe (a) pour S1 à S7 et F1 à F4 ; P77)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("n_a", POINTS_N_A)
@pytest.mark.parametrize("pi", POINTS_PI)
def test_etat_stationnaire_des_regles_par_appel_direct(stationnaire, pi, n_a):
    """Fiche 6, § 9.6, « État stationnaire » (réserve 1), partie des règles : S1 à S7 et F1 à F4
    évaluées par les fonctions du bloc sur l'ouverture du script (`ouverture`), lectures du pas
    (y, tu, p, I^vol, v^e_{t+1}, C, G, WB, ΔL) prises au pas 0 du script (`un_pas`), égales au
    script à 1e−10 relatif ; ti_{t+1} = ti, tu* = tu = t̄u, ϱ_L = ϱ̄_L, L_{t+1}/K_{t+1} = lv*,
    D_{F,t+1} = D*_{F,t+1}. Le pas complet est jugé sur le moteur (classe (b))."""
    par = dataclasses.replace(stationnaire.Parametres(), pi_cible=pi, n_a=n_a, nu_G=1.15)
    e = stationnaire.etat_stationnaire(par)
    o = stationnaire.ouverture(e, par)
    s = stationnaire.un_pas(o, par)
    f_g, pis, gamma_e = facteurs(pi, n_a)
    delta_pas = par.delta / n_a
    varrho_L = bloc.taux_reel_du_credit(o["i_L"], o["pi_cible"])
    tu_etoile = bloc.utilisation_visee(par.tu_bar, par.zeta, varrho_L, o["rho_bar_L"])
    I_vol_plan = bloc.plan_en_volume(o["ti"], f_g, o["y_m1"], par.eta_r, varrho_L,
                                     o["rho_bar_L"])
    I_plan = bloc.plan_nominal(o["registre"][0], pis, I_vol_plan)
    Delta_L_d = bloc.demande_de_credit(par.lv, delta_pas, o["K"], I_plan, o["L"])
    Delta_L = bloc.credit_servi(0.0, Delta_L_d)
    I = bloc.investissement_execute(s["p"], s["I"] / s["p"])
    ti_1 = bloc.part_visee_suivante(o["ti"], par.lambda_ti / n_a, s["tu"], tu_etoile)
    amort = bloc.amortissement(delta_pas, o["K"])
    D_etoile = bloc.depots_vises(par.nu_F, n_a, o["registre"][0], pis, s["ve_1"])
    T_e = bloc.impot_anticipe(gamma_e, o["T_F_m1"])
    Div = bloc.dividendes(o["D_F"], Delta_L, s["C"], s["G"], s["WB"], o["i_L"] / n_a * o["L"],
                          o["i_D"] / n_a, T_e, D_etoile)
    for nom, x, ref in (("S1", varrho_L, s["rho_L"]), ("S2", tu_etoile, s["tu_star"]),
                        ("S3", I_vol_plan, s["I_vol_plan"]), ("S4", I_plan, s["I_plan"]),
                        ("S5", I, s["I"]), ("S6", ti_1, s["ti_1"]), ("S7", amort, s["amort"]),
                        ("F1 ΔL^d", Delta_L_d, s["dL_d"]), ("F1 ΔL", Delta_L, s["dL"]),
                        ("F2", D_etoile, s["D_F_star"]), ("F4", T_e, s["T_F_e"]),
                        ("F3", Div, s["Div_F"])):
        assert ecart(x, ref) <= SEUIL_ETAT_STATIONNAIRE, nom
    # Sur le sentier : ti, tu*, ϱ_L sur leur valeur résolue ; levier et dépôts sur leur ancre.
    assert ecart(ti_1, o["ti"]) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart(tu_etoile, par.tu_bar) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart(s["tu"], tu_etoile) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart(varrho_L, o["rho_bar_L"]) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart((o["L"] + Delta_L) / (o["K"] + I - amort), par.lv) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart(s["D_F_1"], D_etoile) <= SEUIL_ETAT_STATIONNAIRE
    # T_{F,t−1} nulle au socle (τ_F = 0, M33) : F4 se juge par appel direct ci-dessous.
    assert o["T_F_m1"] == 0.0 and T_e == 0.0


def test_un_pas_publie_le_plan_en_volume_et_la_demande_de_credit(stationnaire):
    """Avis de `macro`, rang 1a de J3-d1, § 2, point 2 (précédent de P93) : `un_pas` publie
    I^{vol,plan} (S3) et ΔL^d (F1) ; I^plan = P_{t−1}(1 + π^{∗,pas}) I^{vol,plan} et, ς_L = 0,
    ΔL = ΔL^d, au bit."""
    par = dataclasses.replace(stationnaire.Parametres(), nu_G=1.15)
    e = stationnaire.etat_stationnaire(par)
    o = stationnaire.ouverture(e, par)
    s = stationnaire.un_pas(o, par)
    pis = (1 + par.pi_cible) ** (1 / par.n_a) - 1
    assert s["I_plan"] == o["registre"][0] * (1 + pis) * s["I_vol_plan"]
    assert s["dL"] == s["dL_d"]


@pytest.mark.parametrize("T_F_m1", [1.0, 123.456, -7.5, 5e-324])
@pytest.mark.parametrize("pi", POINTS_PI)
def test_impot_anticipe_sur_un_impot_non_nul(pi, T_F_m1):
    """F4 sous T_{F,t−1} ≠ 0 (avis de `macro`, rang 1a, § 2, point 3 : nul à l'état stationnaire
    au socle) : T^e_{F,t} = Γ^e_t T_{F,t−1}, au bit, Γ^e lu tel quel (aucun recalcul)."""
    _, _, gamma_e = facteurs(pi, N_A)
    assert bloc.impot_anticipe(gamma_e, T_F_m1) == gamma_e * T_F_m1


# --------------------------------------------------------------------------
# Cas à la main (§ 3.F ; `sec:investissement-financement`) sur le grand livre
# --------------------------------------------------------------------------

# Ouverture du cas : postes des entreprises du cas à la main, les autres posés pour équilibrer
# les bilans sans effet sur le cas.
OUVERTURE_DU_CAS = {"D_H": 1500.0, "D_F": 250.0, "L": 936.4989, "B_H": 0.0, "B_Bk": 400.0,
                    "B_CB": 100.0, "Res": 50.0, "L_CB": 20.0, "M_G": 150.0, "K": 2341.2472,
                    "IN": 139.4480}
# Flux du pas du cas (u.m.) : C + G, I, ΔIN, WB, lignes 9 et 10 (part des entreprises) ; taux
# des dépôts par pas du cas, i_D/n_a, que F3 reçoit (#142) : iD_DF = i_D_pas × D_F, 0,625 exact.
I_D_PAS_DU_CAS = 0.0025
FLUX_DU_CAS = {"C": 107.5049, "I": 17.4951, "Delta_IN": 0.4610, "WB": 100.2312,
               "iL_L": 2.3412, "iD_DF": I_D_PAS_DU_CAS * OUVERTURE_DU_CAS["D_F"]}
D_ETOILE_DU_CAS = 250.8265


@dataclasses.dataclass(frozen=True)
class _Cadre:
    tolerance_identite_pas: float = EPSILON
    tolerance_identite_cumulee: float = PARAMETRES_DE_REFERENCE.cadre.tolerance_identite_cumulee


def _etat(ouverture, **variables):
    v = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(ouverture, s) for s in cat.SECTEURS}
    base = {"v_e": 1.0, "IN_vol": 1.4, "pr": 1.0, "K_vol": 24.0, "W": 0.8, "U": 0.05,
            "N": 0.95, "N_pa": 1.0, "mu_tilde": 0.2, "YD_m1": 80.0, "ti": 0.14, "y_m1": 1.0,
            "T_F_m1": 0.0, "varrho_bar_L": 0.0296, "i_L": 0.03, "i_D": 0.03, "pi_e": 0.02,
            "r_hat_etoile": 0.01, "pi_etoile": 0.02, "Y_HS_m1": 80.0}
    base.update(variables)
    return schema.EtatPays(identifiant="A", graine=1, t=0,
                           registre_prix=tuple(1.02 ** (-u / 12) for u in range(1, 14)),
                           **ouverture, **v, **base)


def _derouler(etat, montants):
    """Un pas du grand livre où seules les lignes de `montants` (ligne → terme → u.m.) sont non
    nulles ; rend le grand livre clos en phase 9."""
    gl = ouvrir_pas(etat, _Cadre())
    for phase in cat.PHASES:
        for ligne in cat.LIGNES_DE_LA_PHASE[phase]:
            if ligne.proposant is not None:
                termes = {t.nom: montants.get(ligne.identifiant, {}).get(t.nom, 0.0)
                          for t in ligne.termes}
                gl.proposer(FluxPropose(ligne.identifiant, termes, ligne.proposant))
        gl.clore_phase(phase)
    return gl


def _cas_a_la_main(varsigma_L):
    """F1, S7, F3 par les fonctions du bloc sur le cas ; puis le pas sur le grand livre."""
    o, f = OUVERTURE_DU_CAS, FLUX_DU_CAS
    delta_pas = par_pas(TABLE.delta)
    Delta_L_d = bloc.demande_de_credit(TABLE.lv_etoile, delta_pas, o["K"], f["I"], o["L"])
    Delta_L = bloc.credit_servi(varsigma_L, Delta_L_d)
    amort = bloc.amortissement(delta_pas, o["K"])
    Div = bloc.dividendes(o["D_F"], Delta_L, f["C"], 0.0, f["WB"], f["iL_L"], I_D_PAS_DU_CAS,
                          0.0, D_ETOILE_DU_CAS)
    gl = _derouler(_etat(o), {"1": {"C": f["C"]}, "3": {"I": f["I"]},
                              "4": {"Delta_IN": f["Delta_IN"]}, "5": {"WB": f["WB"]},
                              "8": {"deltaK": amort}, "9": {"iL_L": f["iL_L"]},
                              "10": {"iD_DF": f["iD_DF"]}, "14": {"Div_F": Div},
                              "18": {"Delta_L": Delta_L}})
    return Delta_L_d, Delta_L, amort, Div, gl


def test_cas_a_la_main_lignes_valeur_nette_et_contrainte_budgetaire():
    """Fiche 6, § 9.6, « Cas à la main » (critère 1 ; § 3.F) : un pas, crédit accordé puis
    refusé de moitié ; lignes 3, 8, 14, 17 et 18 exécutées égales aux montants du bloc ; V_F par
    le stock et par les flux ; ΔD_F − ΔL = FU − (I − δK/n_a) − ΔIN ; à 1e−12 × S^F. Un refus
    de x u.m. baisse Div_F de x sans changer I ni ΔD_F. Chiffres publiés (ΔL^d = 3,096,
    Div_F = 7,8269, FU = 5,9314, V_F = 1 800,1277 ; sous refus : 6,2789 et 7,4794) remesurés à
    3e−4 près, leurs entrées étant publiées à 1e−4."""
    resultats = {}
    for varsigma in (0.0, 0.5):
        Delta_L_d, Delta_L, amort, Div, gl = _cas_a_la_main(varsigma)
        s = gl.echelle("entreprises")
        o, f = OUVERTURE_DU_CAS, FLUX_DU_CAS
        for ligne, montant in (("3", f["I"]), ("8", amort), ("14", Div), ("18", Delta_L)):
            assert abs(gl.montant_execute_ligne(ligne) - montant) <= SEUIL_CAS * s, ligne
        Delta_D_F = gl.position("D_F") - o["D_F"]
        # Ligne 17 : −ΔD_F dans la sous-colonne capital des entreprises (dépôts réglés).
        assert abs(gl.montant_execute("17", "entreprises_capital") + Delta_D_F) <= SEUIL_CAS * s
        FU = (f["C"] + f["I"] + f["Delta_IN"] - f["WB"] - amort - f["iL_L"] + f["iD_DF"] - Div)
        V_stock = gl.valeur_nette_stock("entreprises")
        V_ouverture = idt.valeur_nette_stock(o, "entreprises")
        assert abs(V_stock - (V_ouverture + FU)) <= SEUIL_CAS * s
        Delta_L_exec = gl.position("L") - o["L"]
        assert abs((Delta_D_F - Delta_L_exec)
                   - (FU - (f["I"] - amort) - f["Delta_IN"])) <= SEUIL_CAS * s
        levier = gl.position("L") / gl.position("K")
        resultats[varsigma] = (Delta_L_d, Div, FU, V_stock, levier, Delta_D_F, gl)
    (dld, div0, fu0, v0, lev0, dd0, _), (_, div5, fu5, _, lev5, dd5, _) = (
        resultats[0.0], resultats[0.5])
    # Refus de x = ΔL^d/2 : Div_F baisse de x, ΔD_F inchangée, I inchangé (flux posé).
    x = dld / 2
    s = resultats[0.0][6].echelle("entreprises")
    assert abs((div0 - div5) - x) <= SEUIL_CAS * s
    assert abs(dd5 - dd0) <= SEUIL_CAS * s
    for valeur, publie in ((dld, 3.096), (div0, 7.8269), (fu0, 5.9314), (v0, 1800.1277),
                           (lev0, 0.400000), (div5, 6.2789), (fu5, 7.4794), (lev5, 0.399341)):
        assert abs(valeur - publie) <= 3e-4, (valeur, publie)


@pytest.mark.parametrize("surprise", [0.0, 0.01, -0.05])
def test_levier_exact_quand_le_plan_nominal_est_servi(surprise):
    """Fiche 6, § 9.6, « Endettement » (7 (d)), partie (a) : L_{t+1}/K_{t+1} = lv* à 1e−12
    relatif quand le plan nominal est servi (I_t = I^plan_t, d_F = I^plan/p, quel que soit le
    prix du pas : surprise de 0, +1 % et −5 %)."""
    o = OUVERTURE_DU_CAS
    delta_pas = par_pas(TABLE.delta)
    I_plan = 17.4951
    p = 1.25 * (1.0 + surprise)
    I = bloc.investissement_execute(p, I_plan / p)
    Delta_L = bloc.credit_servi(0.0, bloc.demande_de_credit(TABLE.lv_etoile, delta_pas, o["K"],
                                                            I_plan, o["L"]))
    K_1 = o["K"] + I - bloc.amortissement(delta_pas, o["K"])
    assert ecart((o["L"] + Delta_L) / K_1, TABLE.lv_etoile) <= SEUIL_LEVIER


@pytest.mark.parametrize("x", [0.1, 1.0, 5.0])
def test_repartition_d_un_choc_de_resultat(x):
    """Fiche 6, § 9.6, « Répartition d'un choc de résultat » : appel direct de F3 ; une charge
    supplémentaire de x u.m. dans le pas (masse salariale accrue) baisse Div_F de x ; FU (la
    charge et le dividende se compensent), ΔL^d et I inchangés ; à 1e−12 relatif."""
    o, f = OUVERTURE_DU_CAS, FLUX_DU_CAS
    delta_pas = par_pas(TABLE.delta)
    Delta_L_d = bloc.demande_de_credit(TABLE.lv_etoile, delta_pas, o["K"], f["I"], o["L"])
    amort = bloc.amortissement(delta_pas, o["K"])

    def div_et_fu(WB):
        div = bloc.dividendes(o["D_F"], Delta_L_d, f["C"], 0.0, WB, f["iL_L"], I_D_PAS_DU_CAS,
                              0.0, D_ETOILE_DU_CAS)
        return div, f["C"] + f["I"] + f["Delta_IN"] - WB - amort - f["iL_L"] + f["iD_DF"] - div
    div0, fu0 = div_et_fu(f["WB"])
    div1, fu1 = div_et_fu(f["WB"] + x)
    assert ecart(div0 - div1, x) <= SEUIL_CHOC_DE_RESULTAT
    assert ecart(fu1, fu0) <= SEUIL_CHOC_DE_RESULTAT
    # ΔL^d et I ne lisent pas la charge (F1 et S5 n'en dépendent pas : inspection des arguments).
    assert "WB" not in inspect.signature(bloc.demande_de_credit).parameters
    assert "WB" not in inspect.signature(bloc.investissement_execute).parameters


# --------------------------------------------------------------------------
# Bornes (b), dividende ≥ 0 en contrainte de domaine, lecture nette de D_F
# --------------------------------------------------------------------------


def test_plan_et_part_visee_positifs_sur_un_lot():
    """Fiche 6, § 9.6, « Bornes » (b), tenues sur le lot |Δϱ| ≤ 0,1 par an (restriction déclarée ;
    décision du mainteneur du 15/11/2026, constat M1 d'`audit` ; borne ou mécanisme renvoyés à
    #143) : par appel direct, I^{vol,plan} > 0, tu* > 0 et ti_{t+1} > 0 sur un lot de 10^5 tirages
    (graine déclarée) dans les domaines de l'état (ti > 0, y_{t−1} > 0) et de la table (0 ≤ η_r,
    ζ ≤ 20 ; λ_ti/n_a ≤ 1), écart de taux Δϱ = ϱ_L − ϱ̄_L ∈ [−0,1 ; 0,1] par an, tu ∈ [0 ; 5] :
    exact. Le verdict ne vaut pas pour tout le domaine déclaré : S6 rend ti_{t+1} = 0,0 au-delà
    d'une frontière en Δϱ (≈ 3,31 par an à ζ = 4, ≈ 0,66 à ζ = 20), publiée avec la frontière
    de la double précision, et le pas est alors refusé par le moteur
    (`tests/invariants/test_investissement.py`)."""
    rng = np.random.default_rng(GRAINE)
    n = 100_000
    ti = rng.uniform(1e-6, 1.0, n)
    y = rng.uniform(1e-6, 1e6, n)
    eta = rng.uniform(0.0, 20.0, n)
    zeta = rng.uniform(0.0, 20.0, n)
    ecart_taux = rng.uniform(-0.1, 0.1, n)
    tu = rng.uniform(0.0, 5.0, n)
    lam = rng.uniform(1e-6, 1.0, n)
    for k in range(n):
        tu_etoile = bloc.utilisation_visee(0.8, float(zeta[k]), float(ecart_taux[k]), 0.0)
        assert tu_etoile > 0.0
        assert bloc.plan_en_volume(float(ti[k]), 1.0016515813019202, float(y[k]),
                                   float(eta[k]), float(ecart_taux[k]), 0.0) > 0.0
        assert bloc.part_visee_suivante(float(ti[k]), float(lam[k]), float(tu[k]),
                                        tu_etoile) > 0.0
    assert bloc.plan_en_volume(0.14, 1.0, 0.0, 2.0, 0.0, 0.0) == 0.0  # y_m1 = 0 admis : ≥ 0


@pytest.mark.parametrize("brut", [8.0, 1.0, 0.0, -0.0, -1.0, -1e9])
def test_dividende_plancher_de_domaine(brut):
    """F3, plancher : Div_F = max{0 ; ·} ≥ 0 exactement, contrainte de domaine de la ligne 14
    (M28 (e)), sans paramètre ; Div_F = brut si brut ≥ 0."""
    div = bloc.dividendes(brut, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    assert div >= 0.0 and div == max(0.0, brut)


# Ancienne composition (`05541fc`, avant #142) : la phase 6 lisait D_F en max(0 ; ·), calculait
# les intérêts des dépôts sur D̃_F et passait les deux à F3 ; corps recopié tel quel.
def _anciens_dividendes(D_F, Delta_L, C, G, WB, interets_L, interets_D_F, T_e_F, D_etoile_F):
    return max(0.0, D_F + Delta_L + C + G - WB - interets_L + interets_D_F - T_e_F - D_etoile_F)


def _ancienne_composition_de_f3(D_F, i_D_pas, Delta_L, C, G, WB, interets_L, T_e_F, D_etoile_F):
    D_F_net = max(0.0, D_F)
    interets_D_F = i_D_pas * D_F_net
    return _anciens_dividendes(D_F_net, Delta_L, C, G, WB, interets_L, interets_D_F, T_e_F,
                               D_etoile_F)


def test_localite_lecture_nette_egale_au_bit_a_l_ancienne_composition():
    """Critère de #142, écrit avant l'essai : F3 appelée directement avec D_F brut (D_F < 0 :
    poussière et au-delà ; ±0) et i_D/n_a rend, au bit (`float.hex`, signe du zéro compris),
    Div_F de l'ancienne composition « phase → max(0 ; ·), intérêts sur D̃_F → fonction »
    (`05541fc`) ; cas du dividende positif et du plancher ; lot de 2 000 tirages (graine
    déclarée). Pour que l'épreuve morde, D*_F est nul un cas sur deux : au moins 400 cas à
    D_F < 0 ont un dividende positif, hors du plancher."""
    rng = np.random.default_rng(20261116)
    etat0 = _etat(dict(OUVERTURE_DU_CAS, D_F=0.0))
    S_F = idt.echelle_bilan({q: getattr(etat0, q) for q in cat.NOMS_POSTES}, "entreprises")
    negatifs = (-0.0, 0.0, -math.ulp(0.0), -math.ulp(1.0), -0.5 * EPSILON * S_F, -1.0, -1e9)
    f = FLUX_DU_CAS
    cas = [(d, f["WB"]) for d in negatifs] + [(d, 0.0) for d in negatifs]
    cas += [(float(d), float(w)) for d, w in zip(rng.uniform(-1e4, 1e4, 2000),
                                                  rng.uniform(0.0, 100.0, 2000))]
    hors_du_plancher = 0
    for k, (D_F, WB) in enumerate(cas):
        entrees = {"Delta_L": 3.0 * (k % 4 - 1), "C": f["C"], "G": 0.5 * (k % 3), "WB": WB,
                   "interets_L": f["iL_L"], "T_e_F": 0.1 * (k % 5),
                   "D_etoile_F": D_ETOILE_DU_CAS if k % 2 else 0.0}
        i_D_pas = I_D_PAS_DU_CAS * (1 + k % 5)
        ancien = _ancienne_composition_de_f3(D_F, i_D_pas, **entrees)
        nouveau = bloc.dividendes(D_F=D_F, i_D_pas=i_D_pas, **entrees)
        assert nouveau.hex() == ancien.hex(), (D_F, WB)
        hors_du_plancher += D_F < 0.0 and ancien > 0.0
    assert hors_du_plancher >= 400, hors_du_plancher


class _VueDEssai:
    """Vue d'essai d'une phase du bloc 6 : ouverture, paramètres, grandeurs et variables du pas
    lues ; montants exécutés du grand livre ; écritures relevées. Registre : P_{t−1} seul."""

    def __init__(self, etat, lues, montants=None, parametres=PARAMETRES_DE_REFERENCE):
        self.ouverture = etat
        self.parametres = parametres
        self._lues = lues
        self.pas, self.etat, self.lignes = {}, {}, {}
        self.grand_livre = self
        self._montants = montants or {}

    def lire(self, nom):
        return self._lues[nom]

    def dernier_prix(self):
        return self.ouverture.registre_prix[0]

    def montant_execute_ligne(self, ligne):
        return self._montants[ligne]

    def montant_execute(self, ligne, colonne):
        return self._montants[(ligne, colonne)]

    def ecrire_pas(self, nom, valeur):
        assert nom not in self.pas
        self.pas[nom] = valeur

    def ecrire_etat(self, nom, valeur):
        assert nom not in self.etat
        self.etat[nom] = valeur

    def proposer(self, ligne, montants):
        assert ligne not in self.lignes
        self.lignes[ligne] = dict(montants)


def _phase_6(D_F):
    etat = _etat(dict(OUVERTURE_DU_CAS, D_F=D_F))
    lues = {"Gamma_e": 1.0033, "pi_etoile_pas": 0.00165, "v_e_suivant": 100.0,
            "delta_pas": par_pas(TABLE.delta)}
    # Engagement 6 de #132 : F3 lit les cellules signées de la colonne des entreprises
    # (capital pour la ligne 18, courante pour 1, 2 et 5 ; WB débité, −100,2).
    montants = {("18", "entreprises_capital"): 3.0, ("1", "entreprises_courant"): 107.5,
                ("2", "entreprises_courant"): 0.0, ("5", "entreprises_courant"): -100.2}
    vue = _VueDEssai(etat, lues, montants)
    bloc.Investissement().phase_6(vue)
    return vue, etat


@pytest.mark.parametrize("D_F", [-math.ulp(0.0), -math.ulp(1.0), "−0,5 ε S", 0.0, -0.0])
def test_lecture_nette_de_d_f_dans_f3(D_F):
    """ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1), point 4 ; A8.2 ; #103 : un dépôt
    d'ouverture négatif (poussière admise par la lecture nette, testée à −1 ulp et à
    −0,5 ε × S^F) est lu en max(0 ; ·) par F3, dans le terme de dépôts et dans les intérêts :
    ligne 14 égale au bit à F3 recalculée avec D_F = 0."""
    if D_F == "−0,5 ε S":
        etat0 = _etat(dict(OUVERTURE_DU_CAS, D_F=0.0))
        positions = {q: getattr(etat0, q) for q in cat.NOMS_POSTES}
        D_F = -0.5 * EPSILON * idt.echelle_bilan(positions, "entreprises")
    vue, etat = _phase_6(D_F)
    T = TABLE
    D_etoile = bloc.depots_vises(T.nu_F, N_A, etat.registre_prix[0], 0.00165, 100.0)
    attendu = bloc.dividendes(0.0, 3.0, 107.5, 0.0, 100.2,
                              par_pas(TauxDeFlux(etat.i_L)) * etat.L, 0.0,
                              bloc.impot_anticipe(1.0033, etat.T_F_m1), D_etoile)
    assert vue.lignes["14"]["Div_F"] == attendu
    assert vue.pas["D_etoile_F"] == D_etoile


# --------------------------------------------------------------------------
# Domaine strict de K par la monotonie de l'arrondi (point 3 ; P80)
# --------------------------------------------------------------------------


def test_capital_comptable_positif_par_monotonie_de_l_arrondi_sur_un_lot():
    """ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1), point 3 (hypothèse à éprouver,
    précédent de P72) : K_{t+1} = fl(fl(K_t + I_t) − fl(c K_t)) ≥ 0 pour K_t ≥ 0, I_t ≥ 0 et
    c = `par_pas(δ)` < 1, δ dans son domaine ]0 ; n_a[ ; 10^6 tirages (graine déclarée, K et I
    sur 600 ordres de grandeur, δ jusqu'à la borne exclue) et un lot adverse (sous-normaux,
    I = 0, δ juste sous n_a, K maximal) : aucun K_{t+1} < 0. Calculé par les mêmes opérations
    que le noyau (ligne 3 en phase 5, ligne 8 en phase 6, sur K d'ouverture)."""
    rng = np.random.default_rng(GRAINE)
    n = 1_000_000
    K = 10.0 ** rng.uniform(-300, 300, n)
    I = np.where(rng.uniform(size=n) < 0.3, 0.0, 10.0 ** rng.uniform(-300, 300, n))
    deltas = rng.uniform(0.0, N_A, n)
    deltas[deltas == 0.0] = 5e-324
    c = deltas / N_A
    K_1 = (K + I) - c * K
    assert (K_1 >= 0.0).all()
    # Les conversions du moteur rendent la même valeur que δ/n_a vectorisé.
    assert all(par_pas(TauxDeFlux(float(d))) == float(d) / N_A for d in deltas[:1000])
    adverses = [(5e-324, 0.0, math.nextafter(N_A, 0.0)), (5e-324, 5e-324, 6.0),
                (1.7976931348623157e308, 0.0, math.nextafter(N_A, 0.0)), (1.0, 0.0, 11.9999),
                (0.0, 0.0, 0.05), (2.2250738585072014e-308, 0.0, math.nextafter(N_A, 0.0)),
                (1e-310, 1e-320, math.nextafter(N_A, 0.0))]
    minimum = math.inf
    for k, i, d in adverses:
        k_1 = (k + i) - bloc.amortissement(par_pas(TauxDeFlux(d)), k)
        minimum = min(minimum, k_1)
        assert k_1 >= 0.0, (k, i, d)
    # Pas enchaînés sans investissement, δ juste sous n_a : K décroît jusqu'à 0, jamais sous 0.
    for k in (1.0, 1e300, 5e-324):
        c_max = par_pas(TauxDeFlux(math.nextafter(N_A, 0.0)))
        for _ in range(400):
            k = (k + 0.0) - bloc.amortissement(c_max, k)
            assert k >= 0.0
    assert minimum >= 0.0 and float(K_1.min()) >= 0.0


def test_capital_comptable_sur_le_grand_livre_pas_enchaines():
    """Point 3 (P80), sur le noyau : lignes 3 et 8 seules, proposées par les fonctions du bloc
    (S5, S7), 60 pas enchaînés depuis K = 1, I = 0 et δ juste sous n_a : le noyau ouvre chaque
    pas sans refus (`STOCKS_OUVERTURE`, K ≥ 0) et K ne passe jamais sous 0."""
    tables = varier(TABLE, delta=math.nextafter(N_A, 0.0))
    c = par_pas(tables.delta)
    ouverture = dict(OUVERTURE_DU_CAS, K=1.0)
    for _ in range(60):
        etat = _etat(ouverture)
        gl = _derouler(etat, {"3": {"I": 0.0},
                              "8": {"deltaK": bloc.amortissement(c, ouverture["K"])}})
        ouverture = {q: gl.position(q) for q in cat.NOMS_POSTES}
        assert ouverture["K"] >= 0.0
    assert ouverture["K"] == 0.0


# --------------------------------------------------------------------------
# Phases, empreinte, domaines de l'état (inspection)
# --------------------------------------------------------------------------


def test_declaration_conforme_a_tab_investissement_phases():
    """`tab:investissement-phases` et fiche 6, § 9.6, « Phases » (critère 3) : sièges en phases
    2, 3, 5, 6 et 9 ; phase 2 : ouverture, registre et grandeurs du moteur seulement (aucun plan
    de la phase) ; phase 3 : ouverture, δ/n_a (grandeur `delta_pas`, #144, point 2), ς_L et le
    plan de la phase 2 ; phase 5 : p, I^vol (phase 5), tu, y (phase 4), tu* (phase 2) ; phase 6 :
    δ/n_a (`delta_pas`), ni la ligne 7 (impôt), ni les lignes 9 et 10 (intérêts) du pas ; phase
    9 : la ligne 7 seule, au grand livre. Lignes 18, 3, 8, 14 ; états ϱ̄_L (2), ti et y_{t−1}
    (5), T_{F,t−1} (9)."""
    sieges = {s.etape: s for s in bloc.Investissement.declaration.sieges}
    assert set(sieges) == {"2", "3", "5", "6", "9"}
    deux = sieges["2"]
    assert {(lu.source, lu.nom) for lu in deux.lit} == {
        (OUVERTURE, "ti"), (OUVERTURE, "y_m1"), (OUVERTURE, "varrho_bar_L"), (OUVERTURE, "i_L"),
        (OUVERTURE, "pi_etoile"), (REGISTRE, "dernier_prix"), ("0", "facteur_g"),
        ("0", "pi_etoile_pas")}
    assert deux.ecrit == ("varrho_L", "tu_etoile", "I_vol_plan", "I_plan")
    assert (deux.propose, deux.etat) == ((), ("varrho_bar_L",))
    trois = sieges["3"]
    assert set(trois.lit) == {Lecture(OUVERTURE, "K"), Lecture(OUVERTURE, "L"),
                              Lecture("0", "delta_pas"), Lecture("0", "varsigma_L"),
                              Lecture("2", "I_plan")}
    assert (trois.ecrit, trois.propose, trois.etat) == (("Delta_L_d",), ("18",), ())
    cinq = sieges["5"]
    assert set(cinq.lit) == {Lecture(OUVERTURE, "ti"), Lecture("5", "p"), Lecture("5", "I_vol"),
                             Lecture("4", "tu"), Lecture("4", "y"), Lecture("2", "tu_etoile")}
    assert (cinq.propose, cinq.etat) == (("3",), ("ti", "y_m1"))
    six = sieges["6"]
    lues_au_grand_livre = {lu.nom for lu in six.lit if lu.source == GRAND_LIVRE}
    assert lues_au_grand_livre == {"18", "5", "1", "2"}
    assert not lues_au_grand_livre & {"7", "9", "10"}
    assert {lu.nom for lu in six.lit if lu.source == "0"} == {"Gamma_e", "pi_etoile_pas",
                                                             "delta_pas"}
    assert (six.propose, six.etat) == (("8", "14"), ())
    neuf = sieges["9"]
    assert neuf.lit == (Lecture(GRAND_LIVRE, "7"),) and neuf.etat == ("T_F_m1",)
    for s in sieges.values():
        assert s.couvre == ()


def test_empreinte_trois_variables_et_une_constante_sans_tirage():
    """Fiche 6, § 9.6, « Empreinte » (critère 13) : ti, y_{t−1}, T_{F,t−1} et la constante ϱ̄_L,
    propriétaire `investissement` ; aucun registre propre ; aucun tirage (le module n'importe ni
    `random` ni `numpy`) ; aucun attribut d'instance."""
    assert [v.nom for v in schema.VARIABLES_DES_BLOCS if v.proprietaire == "investissement"] == [
        "ti", "y_m1", "T_F_m1", "varrho_bar_L"]
    arbre = ast.parse(inspect.getsource(bloc))
    importes = {a.name for n in ast.walk(arbre) if isinstance(n, ast.Import) for a in n.names}
    importes |= {n.module for n in ast.walk(arbre) if isinstance(n, ast.ImportFrom)}
    assert not {"random", "numpy", "secrets"} & importes
    assert bloc.Investissement.__slots__ == ()


@pytest.mark.parametrize("nom, valeur", [("ti", 0.0), ("ti", -1e-300), ("ti", math.nan),
                                         ("y_m1", -5e-324), ("y_m1", -1.0), ("y_m1", math.inf)])
def test_domaines_de_l_etat_refuses(nom, valeur):
    """Point 1 (visa de `macro` au rang 4) : ti > 0 et y_{t−1} ≥ 0 refusés hors domaine par
    `defaut_de_domaine` (forme non (condition), NaN compris), sans écrêtage ; T_{F,t−1} et ϱ̄_L :
    finitude seule."""
    assert schema.defaut_de_domaine(nom, valeur) is not None
    with pytest.raises(Exception, match=nom):
        _etat(OUVERTURE_DU_CAS, **{nom: valeur})


@pytest.mark.parametrize("nom, valeur", [("ti", 5e-324), ("y_m1", 0.0), ("y_m1", -0.0),
                                         ("T_F_m1", -1e9), ("varrho_bar_L", -0.5)])
def test_domaines_de_l_etat_admis(nom, valeur):
    """Point 1 : ti > 0 au plus petit sous-normal, y_{t−1} = ±0 admis ; T_{F,t−1} et ϱ̄_L sans
    condition de signe."""
    assert schema.defaut_de_domaine(nom, valeur) is None


def test_table_du_bloc_6_complete_et_egale_au_script(stationnaire):
    """ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1), point 2 (P80) : table complète, δ
    avec l'étiquette de F1 ; valeurs égales au bit aux défauts du script (`lv` pour
    `lv_etoile`) ; η_r et ζ sans dimension."""
    noms = [p.nom for p in table_investissement.PARAMETRES_DE_L_INVESTISSEMENT]
    assert noms == ["delta", "tu_bar", "lambda_ti", "eta_r", "zeta", "lv_etoile", "nu_F"]
    assert "eq:investissement-demande-credit" in table_investissement.DELTA.etiquettes
    defaut = stationnaire.Parametres()
    for p in table_investissement.PARAMETRES_DE_L_INVESTISSEMENT:
        script = getattr(defaut, {"lv_etoile": "lv"}.get(p.nom, p.nom))
        assert script.hex() == p.valeur.hex(), p.nom
    assert table_investissement.ETA_R.unite == table_investissement.ZETA.unite == "sans dimension"
    # λ_ti × 0,5 et × 2 admises (variations des critères « Vitesses » et « Boucles »).
    for facteur in (0.5, 2.0):
        varie = varier(TABLE, lambda_ti=TABLE.lambda_ti.valeur * facteur)
        assert varie.lambda_ti == TauxDeFlux(TABLE.lambda_ti.valeur * facteur)


def test_distribution_positive_sous_un_ecart_de_taux_de_moins_deux_points(stationnaire):
    """Fiche 6, § 9.6, « Bornes » (d) (classe (a), forme fermée) : à ζ calibré (ζ = 4, table),
    Δϱ = −2 points permanent, la baisse portant sur le taux directeur, écarts du bloc banque
    constants (lecture retenue par M33 ; `sec:investissement-financement`) : état stationnaire du
    script à r = r̄ − 0,02 et ϱ̄_L de l'état résolu (Δϱ = Δr) ; distribution Div_F/(Div_F + FU) > 0,
    à π* ∈ {0 ; 2 ; 10 %}."""
    for pi in POINTS_PI:
        par = dataclasses.replace(stationnaire.Parametres(), pi_cible=pi, nu_G=1.15)
        assert par.zeta == TABLE.zeta
        norme = stationnaire.etat_stationnaire(par)["rho_L"]
        e = stationnaire.etat_stationnaire(par, r_neutre=par.rbar - 0.02, rho_bar_L=norme,
                                           controler=False)
        assert abs(e["d_rho"] + 0.02) <= 1e-12
        assert e["Div_F"] / (e["Div_F"] + e["FU"]) > 0.0, pi
