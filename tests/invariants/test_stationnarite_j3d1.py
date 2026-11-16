"""Stationnarité partielle de la branche J3-d1 sur le banc à couverture X4 (rang 5 ; P124, P121).

**Bancs** (critère « Branche » de la feuille de route, § 1 ; P124) : socle
partiel d'essai, blocs 2 à 8 réels (`blocs_reels()`), bloc d'essai 9 avec la
**couverture X4** (`socle.couverture_x4()`) ; n_a = 12, ν_G = 1,15, π* ∈ {0 ;
2 % ; 10 %}. Deux variantes (`BANCS`), P141 (a) : **X4 seule** (X1, X2 et X4,
émission aux montants du sentier ; lecture littérale de P124, banc de la mesure
de référence de `macro`, rang 4), **banc du verdict** du critère « Branche » ;
**X4 + X3** (X1 à X3 et X4, `composer` ; avis de `macro`, rang 1a de J3-d1,
§ 6), publié en **contrôle** du même critère, et banc des scénarios (lignes
(b-E4)). Contre-épreuve publiée sans verdict : le même relevé sans X4.
**Étiquette** de toute mesure : celle de son banc (`BANCS`), qui contient
« couverture X4 active ». Aucune mesure ici ne vaut verdict de la boucle
conjointe (#114).

**Critères, écrits avant l'essai, non déplacés** :
- **Branche** : 720 pas sans choc depuis l'état résolu, aux trois π* ; max sur
  les pas de |x_t/x̄_t − 1| ≤ 1e−9 pour la liste de P94 (`grandeurs_b`,
  `grandeurs_p94`, états i_L, i_D, r̂*, π^e, π*) étendue aux grandeurs des blocs 5
  et 6 (avis de `macro`, rang 1a de J3-d1, § 6 : `grandeurs_des_blocs_5_et_6`) ;
  une grandeur nulle par le calcul (`socle.est_nulle`, D1 et P121) : |x_t| ≤
  1e−12, rapportée à l'échelle indiquée (S^CB pour B19, S^F pour T_F, S^G pour
  T^cou) ; ϱ̄_L tenue au bit (P128). Hors seuil sans erreur de code : condition
  d'arrêt de la branche (P134), verdict « non tenu » sans échec attendu.
- **X4** (ADR 0013, annotation de J3-d1, point 7) : ligne 7 = T_H du sentier +
  T^cou ; composition avec X3 indépendante de l'ordre ; refus sur un bloc 9
  réel ; jamais dans le banc de P87.
- **Fiche 5, « Bornes » (d)**, sous la correction prospective de #103 : en O2
  (G^plan × 1,01 et × 1,05 aux tours 1 à 12), D_H + ε S^H ≥ 0 à la fin de chaque
  phase (aucun arrêt du noyau), plafond et plancher de H5 inactifs ; min_t D_H/S^H
  publié (P141 (c), m5 : minimum sur les phases qui débitent D_H, 5 à 7, et D_H
  en mois de consommation, sans verdict). Bornes du bloc 6 inactives en O2
  (fiches 5 et 6, critères 8 (c) et 9 (c) : aucune borne active dans O2).
- **Fiche 6, « Bornes » (c)**, ligne (b-E4), G^plan × 0,95 aux tours 1 à 12 :
  signe et délai seulement (P124 : aucun critère d'arrivée sur 720 pas à 10 %) ;
  I^plan s'écarte du contrôle à la baisse, et une borne activée cesse de l'être
  au plus tard 12 tours après la fin du choc. Intention de dimensionnement
  (« investissement visé nul ou négatif ») réservée au mainteneur, issue #140.

**Seuil du test, fixé par `coder` au rang 5 avant tout essai** (hors des critères
ci-dessus) : `SEUIL_X4`, 1e−12 × max_t |T^cou|, pour l'égalité de T^cou à une
mise en œuvre de référence du test (forme de la maquette de `macro`, assiette
B_H + B_Bk + Res − L^CB), sur un choc qui l'éloigne de zéro.

Les scénarios tournent sur le banc X4 + X3 : sur X4 seule, l'émission aux
montants du sentier laisse l'écart des paiements au compte du Trésor, et le
noyau arrête en phase 5 sous G^plan × 1,05 (M^G < 0 ; pas 3 à π* = 0 et 2 %,
pas 9 à 10 % ; aucun arrêt sous × 1,01 ; mesuré au rang 5), artefact du bloc
d'essai 9 que X3 referme (précédent de P95) ; fait du banc publié sans verdict
(`test_arret_de_x4_seule_en_o2_fait_du_banc`, P141 (a)).
"""

import dataclasses
import importlib.util
import math
import sys
from pathlib import Path

import pytest

from nations.moteur.parametres.cadre import CADRE, PAS_PAR_AN
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.diagnostics import DefautComptable
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas

N_A = PAS_PAR_AN.valeur
NB_PAS = 720
EPS = CADRE.tolerance_identite_pas
X4_X3, X4_SEULE = "X4 + X3", "X4 seule"
BANCS = {X4_X3: "blocs 2 à 8 réels ; bloc d'essai 9 avec X1 à X3 ; couverture X4 active",
         X4_SEULE: ("blocs 2 à 8 réels ; bloc d'essai 9 avec X1, X2, émission aux montants du "
                    "sentier ; couverture X4 active")}
ETIQUETTE = BANCS[X4_X3]
BANC_DU_VERDICT = X4_SEULE  # P141 (a)
# Seuils écrits avant l'essai (critère « Branche » ; P94, P121, P124).
SEUIL_RELATIF = 1e-9
SEUIL_NUL = 1e-12
# Seuil du test (non un critère) : fixé par `coder` au rang 5, avant tout essai.
SEUIL_X4 = 1e-12
FENETRE_DE_DERIVE = 360
# Scénarios (fiche 5, critère 8 (c), O2 ; fiche 6, critère 9 (c)) : tours 1 à 12, pas 0 à 11.
TOURS_DU_CHOC = 12
DELAI_DE_DESACTIVATION = 12
O2 = {"G^plan × 1,01 aux tours 1 à 12": 1.01, "G^plan × 1,05 aux tours 1 à 12": 1.05}
ADVERSE = ("G^plan × 0,95 aux tours 1 à 12", 0.95)
LIGNES_RELEVEES = ("1", "2", "3", "4", "5", "7", "8", "14", "15", "18")
PHASES_QUI_DEBITENT_D_H = ("5", "6", "7")


class Releve:
    """Observateur d'essai : par pas, montants exécutés des lignes `LIGNES_RELEVEES` (total, et
    termes de la ligne 7), variables du pas, grandeurs d'ouverture et état t + 1."""

    def __init__(self):
        self.pas = []
        self._montants = {}

    def relever(self, e):
        if type(e) is ClotureDePhase:
            for ligne, termes in e.montants:
                if ligne in LIGNES_RELEVEES:
                    self._montants[ligne] = sum(x for _, x in termes)
                if ligne == "7":
                    self._montants["7:termes"] = dict(termes)
        elif type(e) is FinDePas:
            self.pas.append({**self._montants, "t": e.t, "variables": dict(e.variables_du_pas),
                             "grandeurs": dict(e.grandeurs_ouverture), "etat": e.etat})
            self._montants = {}


def _choc_de_g(facteur):
    def choc(t):
        return facteur if t < TOURS_DU_CHOC else 1.0
    return choc


def options_du_banc(socle, banc):
    """Options de `blocs` du banc nommé (`BANCS`)."""
    if banc == X4_X3:
        return socle.composer(socle.couverture_x4(), socle.emission_x3())
    return socle.couverture_x4()


def derouler(socle, sentier, nb_pas, options, facteur_g=None):
    options = dict(options)
    if facteur_g is not None:
        options["chocs_des_plans"] = {"G_plan": _choc_de_g(facteur_g)}
    initial = socle.etat_initial(sentier)
    releve = Releve()
    o = socle.ordonnanceur(sentier, reels=socle.blocs_reels(), **options)
    socle.derouler(initial, nb_pas, o, releve)
    return initial, releve


@pytest.fixture(scope="module")
def banc(socle):
    """(banc, π*) → (sentier, état initial, relevé) : 720 pas sans choc."""
    rendus = {}
    for nom in BANCS:
        for pi in socle.POINTS_PI:
            sentier = socle.sentier(pi)
            rendus[nom, pi] = (sentier, *derouler(socle, sentier, NB_PAS,
                                                  options_du_banc(socle, nom)))
    return rendus


def _positions(etat):
    return {q: getattr(etat, q) for q in cat.NOMS_POSTES}


# --------------------------------------------------------------------------
# Grandeurs des blocs 5 et 6 (avis de `macro`, rang 1a de J3-d1, § 6)
# --------------------------------------------------------------------------

# Grandeurs relatives : nom → (définition, unité ; référence sur le sentier).
DEFINITIONS = {
    "YD (état)": "YD_t retenu pour t + 1, u.m. par pas ; sentier nominal",
    "C^plan": "budget de la phase 2, u.m. ; sentier nominal",
    "V*_H": "richesse visée (H3), u.m. ; sentier nominal",
    "R_H": "V_{H,t}/(n_a (YD_t − π^{∗,pas}_t V_{H,t})), années ; valeur du script (ν_H)",
    "I^plan": "plan d'investissement (S4), u.m. ; sentier nominal",
    "ti (état)": "part visée ti_{t+1}, sans dimension ; sentier",
    "ϱ̄_L (état)": "norme ϱ̄_L, par an ; valeur d'ouverture du script, tenue au bit",
    "ϱ_L": "taux réel du crédit anticipé (S1), par an ; ϱ_L du script",
    "tu*": "taux d'utilisation visé (S2), fraction ; tu du script",
    "y_{t−1} (état)": "production retenue y_t, u.v. par pas ; sentier volume",
    "L/K": "L_{t+1}/K_{t+1}, fraction, clôture ; L/K du script (lv*)",
    "D_F/(n_a P_{t−1}(1 + π^{∗,pas})² v^e_{t+1})": "D_{F,t+1} rapporté (F2), années ; ν_F",
    "K^vol/(n_a y)": "K^vol_t/(n_a y_t), années ; K^vol/(n_a y) du script (κ/t̄u)",
    "tu": "y_t/y^cap_t (N11), fraction, phase 4 ; tu du script",
    "ligne 8": "amortissement exécuté, u.m. par pas ; sentier nominal",
    "ligne 14": "dividende des entreprises exécuté, u.m. par pas ; sentier nominal",
    "ligne 18": "crédit servi exécuté, u.m. par pas ; sentier nominal",
    "T_F_m1": "T_{F,t} retenu, rapporté à S^F (nulle)",
    "ligne 7 T_F": "terme T_F de la ligne 7 exécutée, rapporté à S^F (nulle)",
    "T^cou": "T^cou_t de X4, variable du pas, rapportée à S^G (nulle)",
}


def grandeurs_des_blocs_5_et_6(socle, pas, initial, sentier, avec_x4=True):
    """Grandeurs des blocs 5 et 6 ajoutées à la liste de P94 : nom → [(t, x_t, x̄_t)] ; les
    nulles (T_F_m1, ligne 7 T_F, T^cou) déjà rapportées à leur échelle, x̄ = 0. Valeurs de
    référence lues sur le script et le sentier, jamais recopiées (P77). Sans X4 (`avec_x4`
    faux, contre-épreuve), T^cou n'existe pas et n'est pas relevée."""
    e, par = sentier.e, sentier.par
    n = N_A
    resolues = {"R_H": socle.script().valeurs(e, par)["richesse_HS"], "ϱ_L": e["rho_L"], "tu": e["tu"],
                "L/K": e["L"] / e["K"], "K^vol/(n_a y)": e["K_vol"] / (n * e["y"])}
    ouvertures = [initial] + [p["etat"] for p in pas[:-1]]
    g = {cle: [] for cle in DEFINITIONS if avec_x4 or cle != "T^cou"}
    for t, p in enumerate(pas):
        v, o, f, gr = p["variables"], ouvertures[t], p["etat"], p["grandeurs"]

        def nominal(cle, t=t):
            return sentier.valeur(cle, socle.NOMINAL, t)

        def ouverture(nom, t=t):
            return socle.valeur_d_ouverture(sentier, nom, t + 1)

        v_h = o.D_H + o.B_H
        pis = gr["pi_etoile_pas"]
        g["YD (état)"].append((t, f.YD_m1, ouverture("YD_m1")))
        g["C^plan"].append((t, v["C_plan"], nominal("C_plan")))
        g["V*_H"].append((t, v["V_etoile_H"], nominal("V_star")))
        g["R_H"].append((t, v_h / (n * (f.YD_m1 - pis * v_h)), resolues["R_H"]))
        g["I^plan"].append((t, v["I_plan"], nominal("I_plan")))
        g["ti (état)"].append((t, f.ti, ouverture("ti")))
        g["ϱ̄_L (état)"].append((t, f.varrho_bar_L, float(sentier.o["rho_bar_L"])))
        g["ϱ_L"].append((t, v["varrho_L"], resolues["ϱ_L"]))
        g["tu*"].append((t, v["tu_etoile"], resolues["tu"]))
        g["y_{t−1} (état)"].append((t, f.y_m1, ouverture("y_m1")))
        g["L/K"].append((t, f.L / f.K, resolues["L/K"]))
        g["D_F/(n_a P_{t−1}(1 + π^{∗,pas})² v^e_{t+1})"].append(
            (t, f.D_F / (n * o.registre_prix[0] * (1.0 + pis) ** 2 * f.v_e), par.nu_F))
        g["K^vol/(n_a y)"].append((t, o.K_vol / (n * v["y"]), resolues["K^vol/(n_a y)"]))
        g["tu"].append((t, v["tu"], resolues["tu"]))
        g["ligne 8"].append((t, p["8"], nominal("amort")))
        g["ligne 14"].append((t, p["14"], nominal("Div_F")))
        g["ligne 18"].append((t, p["18"], nominal("dL")))
        s_f = idt.echelle_bilan(_positions(f), "entreprises")
        s_g = idt.echelle_bilan(_positions(f), "etat")
        g["T_F_m1"].append((t, f.T_F_m1 / s_f, 0.0))
        g["ligne 7 T_F"].append((t, p["7:termes"]["T_F"] / s_f, 0.0))
        if avec_x4:
            g["T^cou"].append((t, v["T_cou"] / s_g, 0.0))
    return g


ETATS_P94 = ("i_L", "i_D", "r_hat_etoile", "pi_e", "pi_etoile")


def releves_et_references(socle, sentier, initial, releve, avec_x4=True):
    """Toutes les grandeurs du critère « Branche » : nom → [(t, x_t, x̄_t)]."""
    resolues = {**socle.valeurs_resolues(sentier), **socle.valeurs_resolues_p94(sentier)}
    series = {}
    for cle, serie in {**socle.grandeurs_b(releve.pas, initial, sentier),
                       **socle.grandeurs_p94(releve.pas, initial, sentier)}.items():
        series[cle] = [(t, x, resolues[cle]) for t, x in serie]
    for nom in ETATS_P94:
        series[nom] = [(t, getattr(p["etat"], nom), socle.valeur_d_ouverture(sentier, nom, t + 1))
                       for t, p in enumerate(releve.pas)]
    series.update(grandeurs_des_blocs_5_et_6(socle, releve.pas, initial, sentier, avec_x4))
    return series


def derive_par_fenetre(socle, sentier, releve):
    """Max sur chaque fenêtre de 360 pas de |position/position du sentier − 1| (positions non
    nulles au sentier), et rayon apparent (rapport des fenêtres)^(1/360)."""
    fenetres = {}
    for t, p in enumerate(releve.pas):
        w = t // FENETRE_DE_DERIVE
        for poste in cat.NOMS_POSTES:
            ref = socle.position_d_ouverture(sentier, poste, t + 1)
            if ref != 0.0:
                x = abs(getattr(p["etat"], poste) / ref - 1.0)
                if x > fenetres.get(w, (0.0, ""))[0]:
                    fenetres[w] = (x, poste)
    valeurs = [fenetres[w][0] for w in sorted(fenetres)]
    rayon = ((valeurs[-1] / valeurs[0]) ** (1.0 / FENETRE_DE_DERIVE)
             if len(valeurs) > 1 and valeurs[0] > 0.0 else math.nan)
    return fenetres, rayon


# --------------------------------------------------------------------------
# Critère « Branche » : stationnarité partielle sur 720 pas
# --------------------------------------------------------------------------


def juger(socle, sentier, initial, releve, avec_x4=True):
    """Relevé du critère « Branche » : (séries, nulles, pires écarts, grandeurs hors seuil)."""
    assert len(releve.pas) == NB_PAS
    tables = socle.parametres_du_sentier(sentier)
    series = releves_et_references(socle, sentier, initial, releve, avec_x4)
    nulles = {cle for cle in series if socle.est_nulle(cle, tables, sentier)}
    # Toute grandeur de la liste des nulles est relevée, et toute grandeur de référence nulle
    # en flottant y est classée (aucune grandeur nulle jugée en relatif par défaut de liste).
    assert ((set(socle.GRANDEURS_NULLES) | set(socle.GRANDEURS_NULLES_DE_J3D1))
            - (set() if avec_x4 else {"T^cou"})) <= set(series)
    assert {c for c, s in series.items() if all(r == 0.0 for _, _, r in s)} <= nulles
    pires = {}
    for cle, serie in series.items():
        assert serie and serie[-1][0] == NB_PAS - 1, cle
        if cle in nulles:
            pires[cle] = max(abs(x) for _, x, _ in serie)
        else:
            pires[cle] = max(abs(x / r - 1.0) for _, x, r in serie)
    hors = {c: x for c, x in pires.items() if x > (SEUIL_NUL if c in nulles else SEUIL_RELATIF)}
    return series, nulles, pires, hors


@pytest.mark.parametrize("nom_du_banc", list(BANCS))
@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_stationnarite_partielle_de_la_branche(banc, socle, nom_du_banc, pi, publier):
    """Critère « Branche » (P94 étendue, P121, P124) : max_t |x_t/x̄_t − 1| ≤ 1e−9 ; une grandeur
    nulle par le calcul (`socle.est_nulle`), |x_t| ≤ 1e−12 à son échelle ; ϱ̄_L égale au bit à
    sa valeur résolue ; publié grandeur par grandeur, avec la dérive des positions par fenêtre
    de 360 pas. Verdict sur le banc X4 seule (P141 (a)) ; X4 + X3 publié en contrôle, sans
    verdict."""
    sentier, initial, releve = banc[nom_du_banc, pi]
    series, nulles, pires, hors = juger(socle, sentier, initial, releve)
    assert all(x == r for _, x, r in series["ϱ̄_L (état)"])
    fenetres, rayon = derive_par_fenetre(socle, sentier, releve)
    if nom_du_banc == BANC_DU_VERDICT:
        verdict = "non tenu (P134 : condition d'arrêt)" if hors else "tenu"
        role = "banc du verdict (P141 (a))"
    else:
        verdict = ("hors seuil" if hors else "dans les seuils") + " (contrôle, sans verdict)"
        role = "contrôle (P141 (a))"
    croissance = ([f"rapport des deux fenêtres, ramené au pas : {rayon:.6f} (rayon apparent, "
                   "sans verdict)"] if hors else [])
    publier(f"Stationnarité partielle de la branche J3-d1, banc {nom_du_banc}, {role}, π* = "
            f"{100 * pi:g} %, 720 pas ({BANCS[nom_du_banc]})", [
        f"verdict : {verdict} ; seuils 1e−9 relatif, 1e−12 pour une grandeur nulle à son échelle",
        *(f"{c} : {pires[c]:.1e} " + ("(nulle, |x|)" if c in nulles else "(relatif)")
          + (f" — {DEFINITIONS[c]}" if c in DEFINITIONS else "") for c in series),
        "nulles par le calcul (D1, P121, P124) : " + " ; ".join(sorted(nulles)),
        "dérive des positions par fenêtre de 360 pas : " + " | ".join(
            f"pas {FENETRE_DE_DERIVE * w}–{FENETRE_DE_DERIVE * (w + 1) - 1} : {x:.1e} ({q})"
            for w, (x, q) in sorted(fenetres.items())),
        *croissance,
    ])
    if nom_du_banc == BANC_DU_VERDICT:
        assert not hors, hors


def test_contre_epreuve_sans_x4(socle, publier):
    """Contre-épreuve d'`audit` (rang 5), publiée sans verdict : le relevé du critère « Branche »
    sur le banc sans X4 (X1, X2, émission aux montants du sentier). Les π* où il sort des seuils
    sont ceux où X4 discrimine sur 720 pas ; mesuré au rang 5 : π* = 10 % seul (dérive des
    positions sans X4 de 8,6e−12 à 2 %, 3,7e−8 à 10 %)."""
    lignes, discrimine = [], []
    for pi in socle.POINTS_PI:
        sentier = socle.sentier(pi)
        initial, releve = derouler(socle, sentier, NB_PAS, {})
        series, nulles, pires, hors = juger(socle, sentier, initial, releve, avec_x4=False)
        pire = max(pires, key=lambda c: pires[c] / (SEUIL_NUL if c in nulles else SEUIL_RELATIF))
        if hors:
            discrimine.append(pi)
        lignes.append(f"π* = {100 * pi:g} % : " + (
            f"hors seuil sur {len(hors)} grandeurs" if hors else "dans les seuils")
            + f" ; pire {pire} {pires[pire]:.1e}")
    lignes.append("sur 720 pas, X4 ne discrimine qu'à π* = " + (
        " ; ".join(f"{100 * pi:g} %" for pi in discrimine) if discrimine else "aucun π*")
        + " (sans X4, échec à ces π* seulement)")
    publier("Contre-épreuve sans X4 du critère « Branche », 720 pas (blocs 2 à 8 réels ; bloc "
            "d'essai 9 avec X1, X2, émission aux montants du sentier ; X4 inactive ; sans "
            "verdict)", lignes)


def test_nullites_calculees(socle, publier):
    """P121, P124 : Res (H), ξ, T_F (état et ligne 7) et T^cou nulles par leur calcul aux trois π*
    (refinancement net, égalité au bit, τ_F, exact) ; chaque calcul répond non quand sa
    condition tombe (L^CB nul, IN^vol_0 décalé d'un ulp, τ_F ≠ 0, r̄ de la table ≠ r̄ du
    sentier) : le classement n'est pas une déclaration."""
    lignes = []
    for pi in socle.POINTS_PI:
        sentier = socle.sentier(pi)
        tables = socle.parametres_du_sentier(sentier)
        cles = ("B19 Res (H)", "xi", "T_F_m1", "ligne 7 T_F", "T^cou")
        assert all(socle.est_nulle(c, tables, sentier) for c in cles), pi
        e = sentier.e
        lignes.append(f"π* = {100 * pi:g} % : L^CB/S^CB = "
                      f"{e['L_CB'] / socle.script().echelle_CB(e):.4f} ; IN^vol_0 = IN*_0 au bit ; "
                      f"τ_F = {sentier.par.tau_F!r} ; i_CB − i_ref = 0 en exact")
    sentier = socle.sentier(0.02)
    tables = socle.parametres_du_sentier(sentier)
    sans_refinancement = dataclasses.replace(sentier, e={**sentier.e, "L_CB": 0.0})
    assert not socle.est_nulle("B19 Res (H)", tables, sans_refinancement)
    decale = dataclasses.replace(sentier, o={**sentier.o, "IN_vol": math.nextafter(
        float(sentier.o["IN_vol"]), math.inf)})
    assert not socle.est_nulle("xi", tables, decale)
    impose = dataclasses.replace(sentier, par=dataclasses.replace(sentier.par, tau_F=0.1))
    assert not socle.est_nulle("T_F_m1", tables, impose)
    assert not socle.est_nulle("ligne 7 T_F", tables, impose)
    autre_r = dataclasses.replace(sentier, par=dataclasses.replace(sentier.par, rbar=0.02))
    assert not socle.est_nulle("T^cou", tables, autre_r)
    assert not socle.est_nulle("YD (état)", tables, sentier)
    publier("Nullités calculées (P121, P124)", lignes)


# --------------------------------------------------------------------------
# Couverture X4 : forme, composition, refus
# --------------------------------------------------------------------------


def _assiette_de_reference(o):
    """Assiette de X4 sous la forme de la consigne : B_H + B_Bk + Res − L^CB (= B − M^G − E^CB
    par l'identité de la banque centrale)."""
    return o.B_H + o.B_Bk + o.Res - o.L_CB


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_x4_egale_la_forme_de_reference_sous_un_choc(socle, pi, publier):
    """X4, sous G^plan × 0,95 aux tours 1 à 12 (T^cou loin de zéro) : à chaque pas, la ligne 7
    exécutée vaut T_H du sentier + T^cou au bit, T_F du sentier au bit ; T^cou égale la forme de
    référence φ (i_CB − i_ref) (B_H + B_Bk + Res − L^CB)/n_a (maquette de `macro`) à 1e−12 près
    de max_t |T^cou|."""
    sentier = socle.sentier(pi)
    initial, releve = derouler(socle, sentier, 120, options_du_banc(socle, X4_X3), ADVERSE[1])
    ouvertures = [initial] + [p["etat"] for p in releve.pas[:-1]]
    r_bar = sentier.par.rbar
    tcou = [p["variables"]["T_cou"] for p in releve.pas]
    echelle = max(abs(x) for x in tcou)
    assert echelle > 0.0
    pire = 0.0
    for t, (o, p) in enumerate(zip(ouvertures, releve.pas)):
        i_ref = (1.0 + r_bar) * (1.0 + o.pi_etoile) - 1.0
        attendu = 1.0 * (p["variables"]["i_CB"] - i_ref) * _assiette_de_reference(o) / N_A
        pire = max(pire, abs(tcou[t] - attendu))
        termes = p["7:termes"]
        assert termes["T_H"] == sentier.valeur("T_H", socle.NOMINAL, t) + tcou[t], t
        assert termes["T_F"] == sentier.valeur("T_F", socle.NOMINAL, t), t
    assert pire <= SEUIL_X4 * echelle
    publier(f"Couverture X4, forme de référence, G^plan × 0,95, π* = {100 * pi:g} %, 120 pas "
            f"({ETIQUETTE})", [f"max |T^cou| = {echelle:.3e} u.m. ; max |T^cou − référence| = "
                               f"{pire:.1e} u.m. (seuil 1e−12 × max |T^cou|)"])


def test_composition_de_x4_et_x3_independante_de_l_ordre(socle):
    """Composition (ADR 0013, annotation de J3-d1, point 7) : `composer(X4, X3)` et
    `composer(X3, X4)` rendent la même déclaration et les mêmes règles ; X4 touche le siège 6
    (ligne 7), X3 le siège 7 (lignes 19a) ; deux options sur le même siège ou la même ligne sont
    refusées."""
    x4, x3 = socle.couverture_x4(), socle.emission_x3()
    a, b = socle.composer(x4, x3), socle.composer(x3, x4)
    assert a["declarations"] == b["declarations"]
    assert a["lignes"] == b["lignes"]
    assert set(a["lignes"]) == {"7", "19a-BC", "19a-ménages", "19a-banque"}
    propre = socle.declaration_d_essai("finances_publiques")
    for base, compose in zip(propre.sieges, a["declarations"]["finances_publiques"].sieges):
        attendu = {"6": x4, "7": x3}.get(base.etape)
        if attendu is None:
            assert compose == base
        else:
            assert compose == next(s for s in attendu["declarations"]["finances_publiques"].sieges
                                   if s.etape == base.etape)
    with pytest.raises(socle.OptionsIncompatibles):
        socle.composer(x4, x4)
    # Même siège, sans ligne commune (constat m3 de l'audit du rang 5).
    d = {"declarations": socle.couverture_x4()["declarations"]}
    with pytest.raises(socle.OptionsIncompatibles, match="même siège|siège 6"):
        socle.composer(d, d)
    with pytest.raises(socle.OptionsIncompatibles):
        socle.composer(x4, {"lignes": {"7": lambda vue, s: {}}})
    sentier = socle.sentier(0.02)
    assert len(socle.blocs(sentier, reels=socle.blocs_reels(), **a)) == len(socle.RADICAUX)


def test_x4_refusee_sur_un_bloc_9_reel(socle):
    """Refus typé à l'assemblage (P124) : sous un bloc 9 « réel » (ici le bloc d'essai passé
    dans `reels`, faute de bloc 9 réel en J3-d1), les options de X4 sont refusées
    (`OptionSansBlocDEssai`), jamais ignorées."""
    sentier = socle.sentier(0.02)
    bloc_9 = socle.classe_d_essai("finances_publiques", sentier)()
    with pytest.raises(socle.OptionSansBlocDEssai, match="remplacé par un bloc réel"):
        socle.blocs(sentier, reels=(bloc_9,), **socle.couverture_x4())
    with pytest.raises(socle.OptionSansBlocDEssai, match="remplacé par un bloc réel"):
        socle.blocs(sentier, reels=(bloc_9,), lignes=socle.couverture_x4()["lignes"])


def _module_de_p87():
    """Module `tests/invariants/test_boucle_t3_bc3.py`, chargé par son chemin."""
    nom = "test_boucle_t3_bc3_garde_x4"
    if nom not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            nom, Path(__file__).with_name("test_boucle_t3_bc3.py"))
        module = importlib.util.module_from_spec(spec)
        sys.modules[nom] = module
        spec.loader.exec_module(module)
    return sys.modules[nom]


def _options_du_banc_de_p87(socle, monkeypatch):
    """Options que l'ordonnanceur du banc de P87 (`test_boucle_t3_bc3.ordonnanceur`) passe à
    `socle.ordonnanceur`, relevées par une enveloppe, avec et sans choc de G^plan."""
    p87 = _module_de_p87()
    relevees = []
    assembler = socle.ordonnanceur

    def releve(sentier, parametres, **options):
        relevees.append(options)
        return assembler(sentier, parametres, **options)

    monkeypatch.setattr(socle, "ordonnanceur", releve)
    sentier = socle.sentier(0.02)
    for choc_g in (False, True):
        p87.ordonnanceur(socle, sentier, p87.LAMBDA_DE_LA_TABLE, choc_g)
    monkeypatch.setattr(socle, "ordonnanceur", assembler)
    return relevees


def _porte_x4(socle, options):
    """Vrai si des options de `blocs` portent X4 : `T_cou` écrite par un siège de
    `finances_publiques`, ou règle de ligne 7 de X4."""
    declaration = options.get("declarations", {}).get("finances_publiques")
    ecrit = declaration is not None and any("T_cou" in s.ecrit for s in declaration.sieges)
    regle = options.get("lignes", {}).get("7")
    return ecrit or regle is socle._impots_avec_couverture


def test_x4_hors_du_banc_de_p87(socle, monkeypatch):
    """P124 (constat m2 de l'audit du rang 5) : les options que l'ordonnanceur du banc de P87
    (`test_boucle_t3_bc3.ordonnanceur`, contrôle et choc de G^plan) passe au socle ne portent
    ni `T_cou` dans la déclaration de `finances_publiques`, ni la règle de ligne 7 de X4. La
    garde est éprouvée : si X4 est injectée dans le banc (X3 composée avec X4), elle la voit."""
    relevees = _options_du_banc_de_p87(socle, monkeypatch)
    assert len(relevees) == 2
    assert not any(_porte_x4(socle, options) for options in relevees)
    emission = socle.emission_x3
    monkeypatch.setattr(socle, "emission_x3",
                        lambda: socle.composer(emission(), socle.couverture_x4()))
    injectees = _options_du_banc_de_p87(socle, monkeypatch)
    assert all(_porte_x4(socle, options) for options in injectees)


def test_choc_pi_e_refuse_sous_le_bloc_8_reel(socle):
    """#138 : un `choc_pi_e` autre que le choc nul est refusé (`OptionSansBlocDEssai`) quand le
    bloc 8 réel remplace le bloc d'essai ; il reste admis sous le bloc d'essai 8, et le choc nul
    sous le bloc réel."""
    sentier = socle.sentier(0.02)
    reels = socle.blocs_reels()
    assert "banque_centrale" in {b.declaration.radical for b in reels}
    with pytest.raises(socle.OptionSansBlocDEssai, match="#138"):
        socle.blocs(sentier, reels=reels, choc_pi_e=lambda t: 0.01)
    sans_8 = tuple(b for b in reels if b.declaration.radical != "banque_centrale")
    assert len(socle.blocs(sentier, reels=sans_8, choc_pi_e=lambda t: 0.01)) == 8
    assert len(socle.blocs(sentier, reels=reels)) == 8


# --------------------------------------------------------------------------
# Fiche 5, « Bornes » (d), sous #103 ; fiche 6, « Bornes » (c), ligne (b-E4)
# --------------------------------------------------------------------------


class CaisseParPhase:
    """Relève D_H/S^H, D_F/S^F et M^G/S^G à chaque fin des phases 1 à 9 (la phase 0 contrôle
    l'ouverture), sur les arguments du contrôle de caisse du noyau
    (`identites.verifier_caisse`), qu'il appelle ensuite : la trajectoire est inchangée. S_p est
    l'échelle d'ouverture du pas (celle du noyau) ; D_H étant le seul actif des ménages, D_H/S^H
    vaut 1/2 à l'ouverture."""

    def __init__(self, original):
        self.original = original
        self.minimums = {"D_H": math.inf, "D_F": math.inf, "M_G": math.inf}
        # P141 (c), m5 (b) : min de D_H/D_H d'ouverture du pas sur les phases qui débitent D_H
        # (5 : ligne 1 ; 6 : ligne 7 ; 7 : ligne 19a-ménages).
        self.min_d_h_debit = math.inf
        self.d_h_ouverture = math.nan
        self.nb = 0

    def __call__(self, positions, echelles, epsilon, **cles):
        if cles["phase"] == "0":
            self.d_h_ouverture = positions["D_H"]
            return self.original(positions, echelles, epsilon, **cles)
        self.nb += 1
        for moyen, secteur in (("D_H", "menages"), ("D_F", "entreprises"), ("M_G", "etat")):
            self.minimums[moyen] = min(self.minimums[moyen], positions[moyen] / echelles[secteur])
        if cles["phase"] in PHASES_QUI_DEBITENT_D_H:
            self.min_d_h_debit = min(self.min_d_h_debit, positions["D_H"] / self.d_h_ouverture)
        return self.original(positions, echelles, epsilon, **cles)


def bornes_actives(releve):
    """Pas où une borne des blocs 5 et 6 est active : plafond ou plancher de H5, plancher de F3
    (Div_F = 0), I^{vol,plan} ≤ 0 ; ΔL^d < 0 (remboursement, F1) relevé à part."""
    pas = releve.pas
    return {
        "plafond ou plancher de H5": [p["t"] for p in pas
                                      if p["variables"]["C_plan"] != p["variables"]["C_regle"]
                                      or p["variables"]["C_regle"] <= 0.0],
        "plancher de F3 (Div_F = 0)": [p["t"] for p in pas if p["14"] == 0.0],
        "I^{vol,plan} ≤ 0": [p["t"] for p in pas if p["variables"]["I_vol_plan"] <= 0.0],
        "ΔL^d < 0": [p["t"] for p in pas if p["variables"]["Delta_L_d"] < 0.0],
    }


def mois_de_consommation(initial, releve):
    """D_{H,t} d'ouverture rapporté à la consommation exécutée du pas (ligne 1), en mois (un pas
    = un mois, n_a = 12) : min et max sur les pas."""
    ouvertures = [initial] + [p["etat"] for p in releve.pas[:-1]]
    mois = [o.D_H / p["1"] for o, p in zip(ouvertures, releve.pas)]
    return min(mois), max(mois)


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_bornes_d_de_la_fiche_5_en_o2(socle, pi, monkeypatch, publier):
    """Fiche 5, « Bornes » (d), correction prospective de #103 : en O2 (G^plan × 1,01 et × 1,05
    aux tours 1 à 12), 720 pas, D_H + ε S^H ≥ 0 à la fin de chaque phase (aucun arrêt du noyau,
    min D_H/S^H ≥ −ε), plafond et plancher de H5 inactifs (C^plan = C^règle, 0 < C^règle) ;
    bornes du bloc 6 inactives (Div_F > 0, I^{vol,plan} > 0 ; constat m4 de l'audit du rang 5).
    Publiés sans verdict (P141 (c)) : min sur les phases 5 à 7 de D_H/D_H d'ouverture du pas,
    D_H en mois de consommation, et les pas de remboursement (ΔL^d < 0), mécanisme de F1 et non
    borne, comme à la fiche 6 (c) (constat r1 de la revue finale d'`audit`, rang 7)."""
    sentier = socle.sentier(pi)
    lignes = []
    for nom, facteur in O2.items():
        caisse = CaisseParPhase(idt.verifier_caisse)
        monkeypatch.setattr(idt, "verifier_caisse", caisse)
        initial, releve = derouler(socle, sentier, NB_PAS, options_du_banc(socle, X4_X3),
                                   facteur)
        monkeypatch.setattr(idt, "verifier_caisse", caisse.original)
        assert len(releve.pas) == NB_PAS
        assert caisse.minimums["D_H"] >= -EPS
        actives = bornes_actives(releve)
        remboursements = actives.pop("ΔL^d < 0")
        for borne, pas in actives.items():
            assert not pas, (borne, pas[:5])
        mois_min, mois_max = mois_de_consommation(initial, releve)
        lignes.append(f"{nom} : aucun arrêt ; min sur les phases 5 à 7 de D_H/D_H d'ouverture = "
                      f"{caisse.min_d_h_debit:.6f} (min D_H/S^H en fin des phases 1 à 9 = "
                      f"{caisse.minimums['D_H']:.6f}) ; D_H d'ouverture en mois de consommation : "
                      f"{mois_min:.3f} à {mois_max:.3f} (sans verdict) ; aucune borne des blocs 5 "
                      "et 6 active (" + ", ".join(actives) + ") ; ΔL^d < 0 (remboursement, "
                      "mécanisme de F1, sans assertion) : " + (
                          f"pas {remboursements[0]} à {remboursements[-1]} "
                          f"({len(remboursements)} pas)" if remboursements else "jamais"))
    publier(f"Fiche 5, Bornes (d) sous #103, O2, π* = {100 * pi:g} %, 720 pas ({ETIQUETTE})",
            lignes)


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_bornes_c_de_la_fiche_6_signe_et_delai(socle, pi, monkeypatch, publier):
    """Fiche 6, « Bornes » (c), ligne (b-E4), G^plan × 0,95 aux tours 1 à 12, 720 pas, contre le
    contrôle sans choc du même banc : signe (I^plan sous le contrôle au premier pas où il s'en
    écarte) et délai (une borne activée — plancher de F3, Div_F = 0 ; plafond ou plancher de H5 ;
    remboursement du crédit, ΔL^d < 0, publié comme mécanisme et non comme borne — cesse de
    l'être au plus tard au tour 12 + 12) ; aucun arrêt du noyau. Sans critère d'arrivée (P124) :
    l'écart final est publié."""
    sentier = socle.sentier(pi)
    _, controle = derouler(socle, sentier, NB_PAS, options_du_banc(socle, X4_X3))
    caisse = CaisseParPhase(idt.verifier_caisse)
    monkeypatch.setattr(idt, "verifier_caisse", caisse)
    _, choc = derouler(socle, sentier, NB_PAS, options_du_banc(socle, X4_X3), ADVERSE[1])
    monkeypatch.setattr(idt, "verifier_caisse", caisse.original)
    assert len(choc.pas) == NB_PAS
    i_c = [p["variables"]["I_plan"] for p in controle.pas]
    i_s = [p["variables"]["I_plan"] for p in choc.pas]
    premier = next(t for t, (a, b) in enumerate(zip(i_s, i_c)) if a != b)
    assert i_s[premier] < i_c[premier]
    bornes = bornes_actives(choc)
    remboursements = bornes.pop("ΔL^d < 0")
    fin_autorisee = TOURS_DU_CHOC - 1 + DELAI_DE_DESACTIVATION
    for nom, pas in bornes.items():
        assert all(t <= fin_autorisee for t in pas), (nom, pas[-5:])
    ecart_final = i_s[-1] / i_c[-1] - 1.0
    min_ecart = min(a / b - 1.0 for a, b in zip(i_s, i_c))
    aucune = not any(bornes.values())
    publier(f"Fiche 6, Bornes (c), {ADVERSE[0]}, π* = {100 * pi:g} %, 720 pas ({ETIQUETTE} ; "
            "signe et délai seulement, P124)", [
        f"I^plan s'écarte du contrôle au pas {premier}, à la baisse "
        f"({i_s[premier] / i_c[premier] - 1.0:+.3e}) ; min_t (I^plan/I^plan_c − 1) = "
        f"{min_ecart:+.3e}",
        *(f"{nom} : " + (f"active aux pas {pas[0]} à {pas[-1]} ({len(pas)} pas)" if pas
                         else "jamais active") for nom, pas in bornes.items()),
        *(["aucune borne activée : délai non éprouvé"] if aucune else []),
        "constat (sans verdict, réservé au mainteneur, #140) : " + (
            "aucune borne activée" if aucune else "bornes désactivées au plus tard au tour "
            f"{fin_autorisee}") + " sur le scénario écrit (G −5 %) ; intention de "
        f"dimensionnement non atteinte, I^plan {100 * min_ecart:+.1f} % au plus",
        "ΔL^d < 0 (remboursement, mécanisme de F1) : " + (
            f"pas {remboursements[0]} à {remboursements[-1]} ({len(remboursements)} pas)"
            if remboursements else "jamais"),
        f"min sur les phases 5 à 7 de D_H/D_H d'ouverture {caisse.min_d_h_debit:.6f} ; min en "
        f"fin des phases 1 à 9 : D_H/S^H {caisse.minimums['D_H']:.6f} ; D_F/S^F "
        f"{caisse.minimums['D_F']:.6f} ; M^G/S^G {caisse.minimums['M_G']:.6f}",
        f"écart final I^plan/I^plan_c − 1 au pas 719 = {ecart_final:+.3e} (sans critère "
        "d'arrivée, P124)",
    ])


def test_arret_de_x4_seule_en_o2_fait_du_banc(socle, publier):
    """P141 (a), publié sans verdict : sur le banc X4 seule (émission d'essai figée aux montants
    du sentier), O2 arrête le noyau sur M^G < 0 en phase 5 (mesuré au rang 5 : sous G^plan ×
    1,05, pas 3 à π* = 0 et 2 %, pas 9 à 10 % ; aucun arrêt sous × 1,01). Fait du banc, non du bloc 5 : X3 referme l'écart des paiements (précédent de
    P95), d'où le banc X4 + X3 des scénarios. Aucune assertion de verdict ; le test vérifie
    seulement que la mesure a été faite."""
    lignes = []
    for pi in socle.POINTS_PI:
        sentier = socle.sentier(pi)
        for nom, facteur in O2.items():
            releve = Releve()
            o = socle.ordonnanceur(sentier, reels=socle.blocs_reels(),
                                   chocs_des_plans={"G_plan": _choc_de_g(facteur)},
                                   **options_du_banc(socle, X4_SEULE))
            try:
                socle.derouler(socle.etat_initial(sentier), NB_PAS, o, releve)
                issue = f"aucun arrêt sur {NB_PAS} pas"
            except DefautComptable as defaut:
                issue = f"arrêt au pas {len(releve.pas)} : {defaut}"
            lignes.append(f"π* = {100 * pi:g} %, {nom} : {issue}")
    publier(f"Arrêt du banc X4 seule en O2, fait du banc sans verdict, P141 (a) "
            f"({BANCS[X4_SEULE]})", lignes)
