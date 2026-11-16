"""Bloc 5, ménages, dans le socle partiel d'essai : lignes de classe (b) de la fiche 5 (#60), et
mesures publiées de classe (a).

Classe (b) du classement du rang 1a de J3-d1 (avis de `macro`, § 1 ; fiche 5, § 9.6) : état
stationnaire du pas complet (P77 : moteur à n_a = 12 aux trois π*, valeurs de référence du
script `outils/etat_stationnaire.py`, jamais recopiées) ; revenu disponible par le grand livre ;
délais ; impôts doublés sur le socle (« Bornes » (c)) ; vitesses (b-x : blocs 2 à 5 réels,
π^e = π* exogène, prix endogènes, P123), sous la correction prospective de P130 (taux d'épargne
en écart absolu, propriété ÷ 100 entre 720 et 1 440 pas ; ancien verdict relatif publié). S'y ajoutent B_H ≡ 0 exactement, le plan insensible
au registre de l'indice sur le moteur (#58) et le plan dans son domaine par la forme de H5
(P120 ; la lecture nette de D_H à −1 ulp et à −0,5 ε S est éprouvée par appel direct,
`tests/unitaires/test_menages.py` : à l'ouverture, S^H = |D_H| quand D_H est le seul actif des
ménages, et le noyau refuse tout D_H < 0). Mesures de classe (a) publiées ici :
boucle propre, continuum hors C2, part d'un transfert (appel direct des fonctions du bloc, sans
le moteur). Reprise exacte : `test_socle_partiel.py` (blocs réels, dont le bloc 5) ; coût :
`test_budget.py` (P57). Seuils écrits avant l'essai (fiche 5, § 9.6 ; critère de #60,
`docs/feuille-de-route.md` § 1), non déplacés.

**Hors de ce module** (avis de `macro`, § 1) : boucle conjointe (b-x, « avec F de la fiche 6 ») et
canal des dividendes des délais (F3) : bloc 6 réel, rang 4 (#67) ; « Bornes » (d), D_H en O2 :
banc à couverture X4, rang 5 ; lignes (c) : J3-d2 (#132) et #114 (P122).

**Étiquettes** : blocs 2, 3, 4, 5, 7 et 8 réels, blocs 6 et 9 d'essai, plans de
l'investissement et de l'État exogènes ; aucune mesure ici ne vaut verdict de la stationnarité
partielle de la branche (rang 5) ni de la boucle conjointe (#114).
"""

import dataclasses
import math

import numpy as np
import pytest

from nations.blocs import menages as bloc
from nations.blocs.menages import Menages
from nations.blocs.prix import Prix
from nations.blocs.production import Production
from nations.blocs.travail import Travail
from nations.moteur import ordonnanceur as ordo
from nations.moteur.diagnostics import PlanHorsDomaine
from nations.moteur.parametres import varier
from nations.moteur.parametres.cadre import PAS_PAR_AN
from nations.moteur.conversions import par_pas
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE, coefficient_de_richesse
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas

N_A = PAS_PAR_AN.valeur
NB_PAS = 720
EPSILON = PARAMETRES_DE_REFERENCE.cadre.tolerance_identite_pas
TABLE = PARAMETRES_DE_REFERENCE.menages
ETIQUETTES = ("blocs 2, 3, 4, 5, 7 et 8 réels ; bloc 6 d'essai ; plans de l'investissement et de "
              "l'État exogènes")
# Seuils écrits avant l'essai (fiche 5, § 9.6).
SEUIL_UN_PAS = 1e-10  # relatif
SEUIL_H7 = 1e-12  # × S^H
SEUIL_IMPOTS_DOUBLES = 1e-12  # relatif
SEUIL_VITESSES = 1e-6  # relatif, après 720 pas
SEUIL_CONTINUUM = 1e-8  # relatif, sur la forme fermée
BORNES_DE_LA_PART = (0.50, 0.85)  # part d'un transfert dépensée en 12 tours (§ 9.5, critère 12 (d))


class Releve:
    """Observateur d'essai : par pas, montants exécutés par ligne (total) et par cellule de la
    colonne des ménages, variables du pas, grandeurs d'ouverture, état t + 1."""

    def __init__(self):
        self.pas = []
        self._montants = {}

    def relever(self, e):
        if type(e) is ClotureDePhase:
            for ligne, termes in e.montants:
                self._montants[ligne] = sum(x for _, x in termes)
                self._montants[f"{ligne}:termes"] = dict(termes)
        elif type(e) is FinDePas:
            self.pas.append({**self._montants, "t": e.t, "variables": dict(e.variables_du_pas),
                             "grandeurs": dict(e.grandeurs_ouverture), "etat": e.etat})
            self._montants = {}


def ecart(x, reference):
    """|x/x̄ − 1| ; pour une valeur de référence nulle, |x|."""
    return abs(x) if reference == 0.0 else abs(x / reference - 1.0)


def cellule_des_menages(pas, ligne):
    """Montant exécuté de la ligne dans la colonne des ménages, recalculé par le test depuis ses
    termes et le catalogue (signe de la colonne), non par le grand livre."""
    termes = pas.get(f"{ligne}:termes", {})
    total = 0.0
    for terme in cat.LIGNE[ligne].termes:
        if terme.colonne_plus == "menages":
            total += termes.get(terme.nom, 0.0)
        elif terme.colonne_moins == "menages":
            total -= termes.get(terme.nom, 0.0)
    return total


def reels_du_bloc_5(socle):
    """Banc des lignes de la fiche 5 jugées au rang 3 (#60) : blocs réels de `blocs_reels()` sauf
    le bloc 6 (rang 4, #67), gardé d'essai pour que ces verdicts restent sur leur banc
    (`ETIQUETTES`) ; le bloc 6 réel n'entre que dans les lignes qui l'attendaient (canal des
    dividendes F3 des délais)."""
    return tuple(b for b in socle.blocs_reels() if b.declaration.radical != "investissement")


def derouler(socle, sentier, nb_pas, initial=None, reels=None, parametres=None, refus=None,
             **options):
    releve = Releve()
    initial = socle.etat_initial(sentier) if initial is None else initial
    o = socle.ordonnanceur(sentier, PARAMETRES_DE_REFERENCE if parametres is None else parametres,
                           reels=reels_du_bloc_5(socle) if reels is None else reels, **options)
    socle.derouler(initial, nb_pas, o, releve, refus)
    return initial, releve


@pytest.fixture(scope="module")
def trajectoires(socle):
    """Socle partiel, blocs réels de `reels_du_bloc_5` (2, 3, 4, 5, 7 et 8), 720 pas, π* ∈ {0 ;
    2 ; 10 %}."""
    rendus = {}
    for pi in socle.POINTS_PI:
        sentier = socle.sentier(pi)
        assert [b.declaration.radical for b in reels_du_bloc_5(socle)] == [
            "production", "travail", "prix", "menages", "banque", "banque_centrale"]
        initial, releve = derouler(socle, sentier, NB_PAS)
        rendus[pi] = (sentier, initial, releve)
    return rendus


# --------------------------------------------------------------------------
# État stationnaire du pas complet (réserve 1 ; P77)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_un_pas_depuis_l_etat_resolu_egal_au_script(trajectoires, pi, publier):
    """Fiche 5, § 9.6, « État stationnaire » (classe (b) pour le pas complet) : un pas sans choc
    depuis l'état initial résolu laisse YD_{t−1} sur son sentier (YD_0 du script), V_H/(n_a
    YD^HS) = ν_H (YD^HS = YD_0 − π^{∗,pas} V_H), V* = V_H et C^plan = C^règle, et YD^e,
    C^plan égaux au script, à 1e−10 relatif, n_a = 12."""
    sentier, initial, releve = trajectoires[pi]
    p = releve.pas[0]
    v, s = p["variables"], sentier.s
    V_H = initial.D_H + initial.B_H
    YD = p["etat"].YD_m1
    pis = p["grandeurs"]["pi_etoile_pas"]
    ecarts = {
        "YD_0 (état du pas 1)": ecart(YD, s["YD"]),
        "YD^e": ecart(v["YD_e"], s["YD_e"]),
        "V*/V_H": ecart(v["V_etoile_H"], V_H),
        "C^plan": ecart(v["C_plan"], s["C_plan"]),
        "V_H/(n_a YD^HS) − ν_H": ecart(V_H / (N_A * (YD - pis * V_H)), TABLE.nu_H),
    }
    assert v["C_plan"] == v["C_regle"]
    assert all(e <= SEUIL_UN_PAS for e in ecarts.values()), ecarts
    publier(f"Bloc 5, un pas depuis l'état résolu, π* = {pi:.0%} ({ETIQUETTES})", [
        " ; ".join(f"{k} : {e:.1e}" for k, e in ecarts.items()) + " (seuil 1e−10)"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_coefficient_de_richesse_egal_aux_grandeurs_du_moteur(socle, trajectoires, pi):
    """Constat m2 de l'audit du rang 3 : `coefficient_de_richesse`, contrôlé au chargement de
    l'ensemble sur le paramètre π*, égale au bit λ_H/n_a + ν_H λ_H π^{∗,pas} − γ^e calculé sur
    les grandeurs `pi_etoile_pas` et `gamma_e` du pas 0 du moteur (π* d'ouverture = π̄), aux
    trois π*, tables des blocs 7 et 8 alignées sur le sentier (R1)."""
    sentier, _, releve = trajectoires[pi]
    parametres = socle.parametres_du_sentier(sentier)
    g = releve.pas[0]["grandeurs"]
    lam = parametres.menages.lambda_H
    attendu = (par_pas(lam) + parametres.menages.nu_H * lam.valeur * g["pi_etoile_pas"]
               - g["gamma_e"])
    assert coefficient_de_richesse(parametres).hex() == attendu.hex()


# --------------------------------------------------------------------------
# Revenu disponible par le grand livre ; B_H ≡ 0 (critère 1 ; M27 (c))
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_revenu_disponible_par_le_grand_livre_et_b_h_nul(trajectoires, pi, publier):
    """Fiche 5, § 9.6, « Revenu disponible par le grand livre » : à chaque pas des 720,
    YD_t (état YD_{t−1} du pas suivant) égale la somme des montants exécutés des lignes 5, 6, 7,
    10, 11a, 14 et 15 dans la colonne des ménages (recalculée par le test depuis les termes), et
    V_{H,t+1} − V_{H,t} = YD_t − C_t, à 1e−12 × S^H ; B_H ≡ 0 exactement (M27, lecture (c)) :
    B_H nul au bit à chaque ouverture, lignes 11a, 19a-ménages et 19b-ménages nulles au bit."""
    _, initial, releve = trajectoires[pi]
    pire_h7 = pire_v = 0.0
    ouverture = initial
    for p in releve.pas:
        e = p["etat"]
        s_h = idt.echelle_bilan({q: getattr(ouverture, q) for q in cat.NOMS_POSTES}, "menages")
        somme = sum(cellule_des_menages(p, ligne) for ligne in bloc.LIGNES_DU_REVENU)
        pire_h7 = max(pire_h7, abs(e.YD_m1 - somme) / s_h)
        variation = (e.D_H + e.B_H) - (ouverture.D_H + ouverture.B_H)
        pire_v = max(pire_v, abs(variation - (e.YD_m1 - p["1"])) / s_h)
        assert e.B_H == 0.0 and ouverture.B_H == 0.0
        for ligne in ("11a", "19a-ménages"):
            assert p[ligne] == 0.0, ligne
        assert p.get("19b-ménages", 0.0) == 0.0
        ouverture = e
    assert pire_h7 <= SEUIL_H7 and pire_v <= SEUIL_H7
    publier(f"Bloc 5, revenu par le grand livre, π* = {pi:.0%}, 720 pas ({ETIQUETTES})", [
        f"max_t |YD_t − Σ lignes|/S^H = {pire_h7:.1e} ; max_t |ΔV_H − (YD − C)|/S^H = "
        f"{pire_v:.1e} (seuil 1e−12) ; B_H, 11a, 19a-ménages : 0 au bit"])


# --------------------------------------------------------------------------
# Lecture de l'inflation sur le moteur (#58) ; plan dans son domaine par la forme (P120)
# --------------------------------------------------------------------------


def test_plan_insensible_au_registre_sur_le_moteur(socle):
    """Fiche 5, § 9.6, « Lecture de l'inflation » (#58), sur le moteur : deux ouvertures qui ne
    diffèrent que par le registre de l'indice (stationnaire à 2 %, puis multiplié par 1,1) :
    YD^e, V*, C^règle et C^plan du pas 0 identiques au bit, alors que le glissement lu en
    phase 1 par le bloc 8 diffère (le registre est bien lu ailleurs)."""
    sentier = socle.sentier(0.02)
    initial = socle.etat_initial(sentier)
    autre = dataclasses.replace(initial, registre_prix=tuple(
        1.1 * x if u else x for u, x in enumerate(initial.registre_prix)))
    _, a = derouler(socle, sentier, 1, initial)
    _, b = derouler(socle, sentier, 1, autre)
    for nom in ("YD_e", "V_etoile_H", "C_regle", "C_plan"):
        assert a.pas[0]["variables"][nom].hex() == b.pas[0]["variables"][nom].hex(), nom
    assert a.pas[0]["variables"]["i_CB"] != b.pas[0]["variables"]["i_CB"]


def test_plan_hors_domaine_impossible_par_la_forme(socle):
    """P120 : C^plan ≥ 0 par la forme de H5 (plancher, D_H en max(0 ; ·)) ; YD_{t−1} très
    négatif (−10 YD̄) : le pas s'exécute, C^plan = +0,0 (aucun `PlanHorsDomaine`)."""
    sentier = socle.sentier(0.02)
    initial = dataclasses.replace(socle.etat_initial(sentier),
                                  YD_m1=-10.0 * socle.etat_initial(sentier).YD_m1)
    o = socle.ordonnanceur(sentier, reels=reels_du_bloc_5(socle))
    releve = Releve()
    try:
        ordo.executer_pas(initial, socle.ENTREES_SANS_SCENARIO, o, releve)
    except PlanHorsDomaine as refus:  # pragma: no cover - échec du critère
        pytest.fail(f"plan refusé : {refus}")
    assert releve.pas[0]["variables"]["C_plan"] == 0.0


# --------------------------------------------------------------------------
# Délais (critères 2 (d) et 12 (b)) ; impôts doublés sur le socle (« Bornes » (c))
# --------------------------------------------------------------------------

TOUR_DU_CHOC = 5
NB_PAS_DES_DELAIS = 9


def _regle_de_ligne(socle, ligne, terme, variation):
    """Règle d'essai de la ligne `ligne` du bloc d'essai 9 : montants du sentier
    (`socle.LIGNES_DU_SENTIER`), le terme `terme` augmenté de `variation` au seul tour du
    choc."""
    def regle(vue, sentier):
        t = vue.ouverture.t
        montants = {nom: sentier.valeur(cle, socle.NOMINAL, t)
                    for nom, cle in socle.LIGNES_DU_SENTIER[ligne].items()}
        if t == TOUR_DU_CHOC:
            montants[terme] += variation
        return montants
    return regle


def _plans(releve):
    return [p["variables"]["C_plan"] for p in releve.pas]


def _delai(base, choc):
    """Premier tour où C^plan diffère au bit de la base, et le signe de l'écart."""
    for t, (a, b) in enumerate(zip(_plans(base), _plans(choc), strict=True)):
        if a != b:
            return t, math.copysign(1.0, b - a)
    return None, 0.0


def test_delais_des_revenus_et_de_la_cible(socle, publier):
    """Fiche 5, § 9.6, « Délais » (`sec:menages-phases`), signe et date exacts, choc au tour
    n = 5 : transfert (ligne 6, + 1 % de YD̄) ou impôt (ligne 7, + 1 % de YD̄) au tour n : C^plan
    inchangé au bit jusqu'au tour n, modifié au tour n + 1, du signe du levier (+ ; −) ;
    i_D + 1 point au tour n : ligne 10 plus haute au tour n, C^plan modifié au
    tour n + 1, signe +, à revenus des autres secteurs inchangés (`sec:menages-restitution`,
    « Canal du taux, rentier seul ») : bloc d'essai 7, ligne 10 relevée de 0,01 D̄_H/n_a au tour
    n, dividende de la banque sur le sentier ; avec le bloc 7 réel (dividende résiduel B6), la
    même hausse au seul taux des dépôts baisse YD_n de 0,01 D_F/n_a (mesure publiée, sans
    verdict) ; cible π* − 1 point décidée au tour n (bloc d'essai 8, BC4) : C^plan au
    tour n + 1, signe + ; dépense publique + 1 % au tour n (bloc d'essai 9, plan exogène) :
    C^plan au tour n + 2 (revenu salarial au tour n + 1 par l'emploi), signe +. Le canal des
    dividendes (F3, dividende au tour n, budget au tour n + 1) attend le bloc 6 réel (#67)."""
    sentier = socle.sentier(0.02)
    n = TOUR_DU_CHOC
    _, base = derouler(socle, sentier, NB_PAS_DES_DELAIS)
    un_pour_cent = 0.01 * sentier.s["YD"]
    mesures = {}
    _, tr = derouler(socle, sentier, NB_PAS_DES_DELAIS, lignes={
        "6": _regle_de_ligne(socle, "6", "Tr", un_pour_cent)})
    mesures["transfert"] = (_delai(base, tr), (n + 1, 1.0))
    _, th = derouler(socle, sentier, NB_PAS_DES_DELAIS, lignes={
        "7": _regle_de_ligne(socle, "7", "T_H", un_pour_cent)})
    mesures["impôt"] = (_delai(base, th), (n + 1, -1.0))
    sans_7 = tuple(b for b in reels_du_bloc_5(socle) if b.declaration.radical != "banque")
    _, base_7 = derouler(socle, sentier, NB_PAS_DES_DELAIS, reels=sans_7)
    hausse = 0.01 / N_A * socle.position_d_ouverture(sentier, "D_H", n)
    _, i_d = derouler(socle, sentier, NB_PAS_DES_DELAIS, reels=sans_7, lignes={
        "10": _regle_de_ligne(socle, "10", "iD_DH", hausse)})
    mesures["taux des dépôts (revenus des autres secteurs inchangés)"] = (
        _delai(base_7, i_d), (n + 1, 1.0))
    assert i_d.pas[n]["10"] > base_7.pas[n]["10"]
    # Bloc 7 réel : i_D + 1 point à l'ouverture du tour 0 (mesure publiée, sans verdict).
    initial = socle.etat_initial(sentier)
    _, reel = derouler(socle, sentier, 2, dataclasses.replace(initial, i_D=initial.i_D + 0.01))
    yd_reel = reel.pas[0]["etat"].YD_m1 - base.pas[0]["etat"].YD_m1
    canal_reel = (f"bloc 7 réel, i_D + 1 point au tour 0 : ΔYD_0 = {yd_reel:.3e}, contre "
                  f"−0,01 D_F/n_a = {-0.01 / N_A * initial.D_F:.3e} (dividende résiduel B6) ; "
                  f"premier tour modifié {_delai(base, reel)}")
    sans_8 = tuple(b for b in reels_du_bloc_5(socle)
                   if b.declaration.radical != "banque_centrale")

    def cible(vue, s, t):
        return vue.ouverture.pi_etoile - (0.01 if t == n else 0.0)
    _, base_8 = derouler(socle, sentier, NB_PAS_DES_DELAIS, reels=sans_8)
    _, pi = derouler(socle, sentier, NB_PAS_DES_DELAIS, reels=sans_8,
                     regles={"pi_etoile": cible})
    mesures["cible"] = (_delai(base_8, pi), (n + 1, 1.0))

    def g_plan(t):
        return 1.01 if t == n else 1.0
    _, g = derouler(socle, sentier, NB_PAS_DES_DELAIS, chocs_des_plans={"G_plan": g_plan})
    mesures["dépense publique"] = (_delai(base, g), (n + 2, 1.0))
    publier(f"Bloc 5, délais du budget, choc au tour {n} ({ETIQUETTES})", [
        f"{nom} : premier tour modifié {mesure[0]}, signe {mesure[1]:+.0f} "
        f"(attendu : tour {attendu[0]}, signe {attendu[1]:+.0f})"
        for nom, (mesure, attendu) in mesures.items()] + [canal_reel + " (publié, sans verdict)"])
    for nom, (mesure, attendu) in mesures.items():
        assert mesure == attendu, nom


def test_impots_doubles_sur_le_socle(socle, publier):
    """Fiche 5, § 9.6, « Bornes » (c), classe (b) : impôt des ménages doublé au seul tour n = 5
    (règle de ligne 7 du bloc d'essai 9) : D_H d'ouverture du tour n + 1 abaissé de ΔT_H, à
    1e−12 × S^H, et C^plan du tour n + 1 abaissé de ΔT_H (α_Y Γ^e + λ_H/n_a − γ^e +
    ν_H λ_H π^{∗,pas}), à 1e−12 relatif ; plafond et plancher inactifs."""
    sentier = socle.sentier(0.02)
    n = TOUR_DU_CHOC
    _, base = derouler(socle, sentier, n + 2)
    delta_T = sentier.valeur("T_H", socle.NOMINAL, n)
    _, choc = derouler(socle, sentier, n + 2, lignes={
        "7": _regle_de_ligne(socle, "7", "T_H", delta_T)})
    e_base, e_choc = base.pas[n]["etat"], choc.pas[n]["etat"]
    s_h = idt.echelle_bilan({q: getattr(e_base, q) for q in cat.NOMS_POSTES}, "menages")
    assert abs((e_base.D_H - e_choc.D_H) - delta_T) <= SEUIL_H7 * s_h
    g = base.pas[n + 1]["grandeurs"]
    nu, lam = TABLE.nu_H, TABLE.lambda_H.valeur
    attendu = delta_T * ((1 - nu * lam) * g["Gamma_e"] + lam / N_A - g["gamma_e"]
                         + nu * lam * g["pi_etoile_pas"])
    vb, vc = base.pas[n + 1]["variables"], choc.pas[n + 1]["variables"]
    baisse = vb["C_plan"] - vc["C_plan"]
    assert vc["C_plan"] == vc["C_regle"] and vb["C_plan"] == vb["C_regle"]
    assert ecart(baisse, attendu) <= SEUIL_IMPOTS_DOUBLES
    publier(f"Bloc 5, impôts doublés au tour {n} ({ETIQUETTES})", [
        f"ΔT_H = {delta_T:.6g} ; baisse de C^plan au tour {n + 1} = {baisse:.6g}, forme fermée "
        f"{attendu:.6g}, écart relatif {ecart(baisse, attendu):.1e} (seuil 1e−12)"])


# --------------------------------------------------------------------------
# Vitesses, sous C2 (critère 4 ; réserve 2 ; P123 ; P130)
# --------------------------------------------------------------------------

HORIZONS_DES_VITESSES = (720, 1440, 2160, 6480)
EPARGNE = "épargne nominale (12 tours)"
# P130 : propriété de convergence, écart divisé par au moins 100 entre 720 et 1 440 pas.
FACTEUR_DE_CONVERGENCE = 100.0


def _hausse_de_g_pendant_12_tours(t):
    return 1.01 if 1 <= t <= 12 else 1.0


def _ratios_au_pas(releve, initial, t):
    """V/(n_a YD^HS), V/(n_a YD), taux d'épargne nominal sur 12 tours 1 − ΣC/ΣYD, et C/YD du
    pas t ; V_H d'ouverture du pas t, YD_t, C_t ligne 1 exécutée."""
    ouverture = initial if t == 0 else releve.pas[t - 1]["etat"]
    p = releve.pas[t]
    V, YD = ouverture.D_H + ouverture.B_H, p["etat"].YD_m1
    pis = p["grandeurs"]["pi_etoile_pas"]
    fenetre = releve.pas[t - N_A + 1:t + 1]
    return {"V/(n_a YD^HS)": V / (N_A * (YD - pis * V)), "V/(n_a YD)": V / (N_A * YD),
            EPARGNE: 1.0 - sum(q["1"] for q in fenetre) / sum(q["etat"].YD_m1 for q in fenetre),
            "C/YD": p["1"] / YD}


@pytest.fixture(scope="module")
def vitesses(socle):
    """Branches λ_H × 0,5 et × 2 : blocs 2 à 5 réels, 6 à 9 d'essai (π^e = π* exogène, bloc
    d'essai 8), G + 1 % aux tours 1 à 12, π* ∈ {0 ; 2 ; 10 %}, 6 480 pas ; aux horizons de
    `HORIZONS_DES_VITESSES`, écart relatif entre branches de chaque ratio (clé « relatif ») et
    écart absolu du taux d'épargne nominal, en fraction du revenu (clé « absolu », P130)."""
    reels = (Production(), Travail(), Prix(), Menages())
    rendus = {}
    for pi in socle.POINTS_PI:
        branches = []
        for facteur in (0.5, 2.0):
            lam = facteur * TABLE.lambda_H.valeur
            sentier = socle.sentier(pi, lambda_H=lam)
            parametres = dataclasses.replace(PARAMETRES_DE_REFERENCE,
                                             menages=varier(TABLE, lambda_H=lam))
            initial, releve = derouler(socle, sentier, HORIZONS_DES_VITESSES[-1], reels=reels,
                                       parametres=parametres,
                                       chocs_des_plans={"G_plan": _hausse_de_g_pendant_12_tours})
            branches.append({h: _ratios_au_pas(releve, initial, h - 1)
                             for h in HORIZONS_DES_VITESSES})
        rendus[pi] = {h: {"relatif": {k: ecart(branches[0][h][k], branches[1][h][k])
                                      for k in branches[0][h]},
                          "absolu": abs(branches[0][h][EPARGNE] - branches[1][h][EPARGNE])}
                      for h in HORIZONS_DES_VITESSES}
    return rendus


def test_vitesses_publication_du_verdict_relatif(vitesses, publier):
    """Fiche 5, § 9.6, « Vitesses » (b-x), critère d'origine : écart relatif entre les branches
    λ_H × 0,5 et × 2 au plus 1e−6 après 720 pas, pour les quatre grandeurs. **Verdict publié, sans
    assertion (P130)** : « non tenu » pour le taux d'épargne nominal (écart relatif pris sur un
    solde) ; verdict à π* = 2 % seul, comme le critère d'origine ; π* = 0 et 10 %, et 1 440,
    2 160 et 6 480 pas, publiés sans verdict (P123, P131). L'ancien critère reste
    publié avec son verdict ; la correction prospective de P130 est jugée par les tests
    suivants."""
    lignes = []
    for pi, par_h in vitesses.items():
        for h, m in par_h.items():
            rel = m["relatif"]
            verdict = ""
            if h == 720 and pi == 0.02:
                tenu = max(rel.values()) <= SEUIL_VITESSES
                verdict = (" (critère d'origine, relatif ≤ 1e−6 : "
                           + ("tenu" if tenu else "non tenu") + ")")
            lignes.append(f"π* = {pi:.0%}, {h} pas : "
                          + " ; ".join(f"{k} {e:.1e} rel." for k, e in rel.items())
                          + f" ; {EPARGNE} {m['absolu']:.1e} abs." + verdict)
    publier("Bloc 5, vitesses (λ_H × 0,5 contre × 2), G + 1 % aux tours 1 à 12 (blocs 2 à 5 "
            "réels, bloc 6 d'essai, π^e = π* exogène, prix endogènes ; P123, P130)", lignes)


@pytest.mark.parametrize("pi", [0.02])
def test_vitesses_sous_c2_correction_p130(vitesses, pi):
    """Fiche 5, § 9.6, « Vitesses », sous la **correction prospective de P130** (14/11/2026,
    postérieure à l'observation et déclarée comme telle ; ancien verdict publié par
    `test_vitesses_publication_du_verdict_relatif`) : après 720 pas, écart relatif entre les
    branches λ_H × 0,5 et × 2 au plus 1e−6 pour V/(n_a YD^HS), V/(n_a YD) et C/YD ; écart
    **absolu** du taux d'épargne nominal sur 12 tours au plus 1e−6 (fraction du revenu), à
    π* = 2 % seul, comme le critère d'origine (P131 : aucune extension après observation ;
    π* = 0 et 10 % publiés sans verdict)."""
    m = vitesses[pi][720]
    for grandeur in ("V/(n_a YD^HS)", "V/(n_a YD)", "C/YD"):
        assert m["relatif"][grandeur] <= SEUIL_VITESSES, grandeur
    assert m["absolu"] <= SEUIL_VITESSES


@pytest.mark.parametrize("pi", [0.02])
def test_vitesses_convergence_p130(vitesses, pi):
    """P130 (correction prospective, postérieure à l'observation), à π* = 2 % seul (P131) :
    l'écart entre les branches
    est divisé par au moins 100 entre 720 et 1 440 pas, pour chacune des quatre grandeurs
    relatives et pour l'écart absolu du taux d'épargne : convergence, non un continuum
    (`sec:menages-stationnaire` : sous C2, aucune vitesse n'entre dans l'état d'arrivée).
    Remplace le contrôle « ≤ 1e−10 à 2 160 pas » de la première remise, fixé après
    observation (constat m3 d'`audit`)."""
    a, b = vitesses[pi][720], vitesses[pi][1440]
    paires = [(a["relatif"][k], b["relatif"][k], k) for k in a["relatif"]]
    paires.append((a["absolu"], b["absolu"], f"{EPARGNE}, absolu"))
    for e720, e1440, nom in paires:
        assert e1440 * FACTEUR_DE_CONVERGENCE <= e720, (nom, e720, e1440)


# --------------------------------------------------------------------------
# Mesures de classe (a) publiées : boucle propre, continuum hors C2, part d'un transfert
# --------------------------------------------------------------------------


def _facteurs(pi, g=0.02, pi_cible=None):
    """Γ (réalisé, π), Γ^e, γ^e et π^{∗,pas} (cible π*, par défaut π) ; n_a = 12."""
    pi_cible = pi if pi_cible is None else pi_cible
    realise = ((1 + g) * (1 + pi)) ** (1 / N_A)
    attendu = ((1 + g) * (1 + pi_cible)) ** (1 / N_A)
    return realise, attendu, attendu - 1.0, (1 + pi_cible) ** (1 / N_A) - 1.0


def _pas_du_bloc_seul(V, YD_m1, Y_o, i_D, Gamma_e, gamma_e, pis, nu, lam):
    """Un pas du bloc seul, demande servie : H2 à H5 (fonctions du bloc), revenu
    YD = Y_o + i_D V/n_a (revenus hors intérêts exogènes), V_{t+1} = V + YD − C. V est passé
    en D_H, B_H = 0 (socle, M27) ; H3 à H5 le lisent en max(0 ; V), égal à V pour V ≥ 0 (#142)."""
    YD_e = bloc.revenu_attendu(Gamma_e, YD_m1)
    V_etoile = bloc.richesse_visee(nu, N_A, YD_e, pis, V, 0.0)
    C = bloc.budget_de_consommation(V, bloc.plan_de_la_regle(YD_e, gamma_e, V, 0.0, lam / N_A,
                                                             V_etoile))
    YD = Y_o + i_D / N_A * V
    return V + YD - C, YD, C


def _boucle_propre(i_D, pi, lam):
    """Valeurs propres de la récurrence (V, YD_{t−1}) du bloc seul, ramenée au sentier (÷ Γ),
    au point fixe en forme fermée (V/(n_a YD) = ν_H/(1 + ν_H n_a π^{∗,pas}), Y_o = 1) ;
    jacobienne par différences centrées (carte linéaire : exacte à l'arrondi près)."""
    G, G_e, g_e, pis = _facteurs(pi)
    nu = TABLE.nu_H
    r = nu / (1 + nu * N_A * pis)
    YD = 1.0 / (1 - i_D * r)
    x0 = np.array([r * N_A * YD, YD / G])

    def carte(x):
        V1, YD1, _ = _pas_du_bloc_seul(x[0], x[1], 1.0, i_D, G_e, g_e, pis, nu, lam)
        return np.array([V1 / G, YD1 / G])
    J = np.zeros((2, 2))
    for k in range(2):
        h = np.zeros(2)
        h[k] = 1e-6 * abs(x0[k])
        J[:, k] = (carte(x0 + h) - carte(x0 - h)) / (2 * h[k])
    return max(abs(np.linalg.eigvals(J)))


def test_boucle_propre_module_inferieur_a_un(publier):
    """Fiche 5, § 9.6, « Boucle propre » (critère 5 (b)) : revenus hors intérêts exogènes,
    module de la valeur propre dominante < 1 aux trois calibrations (i_D = 0 et 3 % à π* = 2 %,
    11 % à 10 %) ; λ_H × 0,5 et × 2 (i_D = 3 %) publiés ; demi-vies publiées. Repères de la
    fiche : 0,96612, 0,96706, 0,96727 ; 0,98352 et 0,93419 (cinq décimales)."""
    cas = {"i_D = 0, π* = 2 %": (0.0, 0.02, 0.4, 0.96612),
           "i_D = 3 %, π* = 2 %": (0.03, 0.02, 0.4, 0.96706),
           "i_D = 11 %, π* = 10 %": (0.11, 0.10, 0.4, 0.96727),
           "λ_H × 0,5, i_D = 3 %": (0.03, 0.02, 0.2, 0.98352),
           "λ_H × 2, i_D = 3 %": (0.03, 0.02, 0.8, 0.93419)}
    lignes = []
    for nom, (i_D, pi, lam, repere) in cas.items():
        module = _boucle_propre(i_D, pi, lam)
        assert module < 1.0, nom
        assert round(module, 5) == repere, nom
        lignes.append(f"{nom} : |λ| = {module:.6f}, demi-vie {math.log(0.5) / math.log(module):.1f} "
                      "tours")
    publier("Bloc 5, boucle propre (revenus hors intérêts exogènes ; appel direct)", lignes)


def _ratio_converge(pi_bar, pi_cible, lam, i_D, nb=3000):
    """Bloc seul, revenus hors intérêts croissant au facteur [(1 + g)(1 + π̄)]^{1/n_a}, cible
    π* ; V/(n_a YD) après `nb` pas (ramené au sentier, Y_o = 1). Pire cas de convergence :
    |λ| = 0,98352 (λ_H = 0,2) ; 3 000 pas donnent 0,98352^3000 ≈ 2e−22."""
    G, G_e, g_e, pis = _facteurs(pi_bar, pi_cible=pi_cible)
    nu = TABLE.nu_H
    V, YD_m1 = N_A * nu, 1.0 / G
    for _ in range(nb):
        V1, YD, _ = _pas_du_bloc_seul(V, YD_m1, 1.0, i_D, G_e, g_e, pis, nu, lam)
        V, YD_m1 = V1 / G, YD / G
    return V / (N_A * YD_m1 * G), G, G_e, pis


def test_continuum_hors_c2_sur_la_forme_fermee(publier):
    """Fiche 5, § 9.6, « Continuum hors C2 » (réserve 2 ; déclaré) : bloc 5 seul, revenus hors
    intérêts croissant au facteur [(1 + g)(1 + π̄)]^{1/n_a}, π̄ = 3 % et 10 %, π* = 2 % ; après
    convergence, V/(n_a YD) égal à [1 − α_Y Γ^e/Γ]/[n_a(Γ − Γ^e) + λ_H(1 + n_a ν_H π^{∗,pas})] à
    1e−8 relatif ; écarts à la lecture exacte 1/(1 + n_a[(1 + π̄)^{1/n_a} − 1]) publiés pour
    λ_H = 0,2 / 0,4 / 0,8 (fiche : −3,35 / −1,29 / −0,22 % à 3 % ; −19,76 / −8,58 / −1,56 % à
    10 %, deux décimales)."""
    reperes = {(0.03, 0.2): -3.35, (0.03, 0.4): -1.29, (0.03, 0.8): -0.22,
               (0.10, 0.2): -19.76, (0.10, 0.4): -8.58, (0.10, 0.8): -1.56}
    nu = TABLE.nu_H
    lignes = []
    for (pi_bar, lam), repere in reperes.items():
        ratio, G, G_e, pis = _ratio_converge(pi_bar, 0.02, lam, i_D=0.0)
        forme = (1 - (1 - nu * lam) * G_e / G) / (N_A * (G - G_e) + lam * (1 + N_A * nu * pis))
        assert ecart(ratio, forme) <= SEUIL_CONTINUUM, (pi_bar, lam)
        exacte = 1.0 / (1 + N_A * ((1 + pi_bar) ** (1 / N_A) - 1))
        ecart_publie = 100 * (forme / exacte - 1)
        assert round(ecart_publie, 2) == repere, (pi_bar, lam)
        lignes.append(f"π̄ = {pi_bar:.0%}, λ_H = {lam} : V/(n_a YD) = {ratio:.6f}, forme fermée "
                      f"{forme:.6f} (écart {ecart(ratio, forme):.1e}), écart à la lecture exacte "
                      f"{ecart_publie:+.2f} %")
    publier("Bloc 5, continuum hors C2 (π* = 2 % ; appel direct, revenus hors intérêts "
            "exogènes, i_D = 0)", lignes)


def _part_d_un_transfert(pi, i_D, lam):
    """Part propre au ménage : Σ_{tours 1 à 12} ΔC / Σ transferts, transfert de 1 % du YD
    stationnaire aux tours 1 à 12, bloc seul (revenus hors intérêts exogènes), depuis le point
    fixe en forme fermée."""
    G, G_e, g_e, pis = _facteurs(pi)
    nu = TABLE.nu_H
    r = nu / (1 + nu * N_A * pis)
    YD_bar = 1.0 / (1 - i_D * r)

    def consommations(avec_transfert):
        V, YD_m1, rendus = r * N_A * YD_bar, YD_bar / G, []
        for t in range(13):
            tr = 0.01 * YD_bar if avec_transfert and 1 <= t <= 12 else 0.0
            V1, YD, C = _pas_du_bloc_seul(V, YD_m1, 1.0 + tr, i_D, G_e, g_e, pis, nu, lam)
            rendus.append(C)
            V, YD_m1 = V1 / G, YD / G
        return rendus
    base, choc = consommations(False), consommations(True)
    return sum(choc[t] - base[t] for t in range(1, 13)) / (12 * 0.01 * YD_bar)


def test_part_d_un_transfert_depensee_en_12_tours(publier):
    """Fiche 5, § 9.6, « Part d'un transfert » (critère 12 (d)) : appel direct, équilibre
    partiel du bloc, transfert de 1 % du YD stationnaire aux tours 1 à 12 (i_D = 3 %) : part
    dans [0,50 ; 0,85] à la calibration (π* = 2 %) ; publiée à 10 % et aux variantes λ_H × 0,5 et
    × 2 (fiche : 0,628 ; 0,618 ; 0,760 ; 0,423)."""
    cas = {"π* = 2 % (calibration)": (0.02, 0.4, 0.628), "π* = 10 %": (0.10, 0.4, 0.618),
           "λ_H × 0,5": (0.02, 0.2, 0.760), "λ_H × 2": (0.02, 0.8, 0.423)}
    parts = {nom: _part_d_un_transfert(pi, 0.03, lam) for nom, (pi, lam, _) in cas.items()}
    publier("Bloc 5, part d'un transfert dépensée en 12 tours (appel direct, i_D = 3 %)", [
        f"{nom} : {part:.4f}" for nom, part in parts.items()])
    bas, haut = BORNES_DE_LA_PART
    assert bas <= parts["π* = 2 % (calibration)"] <= haut
    for nom, (_, _, repere) in cas.items():
        assert round(parts[nom], 3) == repere, nom
