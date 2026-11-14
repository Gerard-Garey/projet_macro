"""Bloc 5, ménages : lignes « J3 » de classe (a) de la fiche 5 (#60).

Classe (a) du classement du rang 1a de J3-d1 (avis de `macro`, § 1 ; fiche 5, § 9.6) :
état stationnaire de H2 à H5 par appel direct sur l'ouverture du script, à π* ∈ {0 ; 2 ;
10 %} et n_a ∈ {4 ; 12 ; 52} (P77 : n_a ≠ 12 par les fonctions pures et le script) ; identité
du cas à 90 % et cas des impôts doublés (noyau et bloc 5, autres montants posés à la main) ;
lecture de l'inflation (#58) ; effet d'un changement de cible ; phases ; bornes (a) et (b) ;
conditions de domaine ; empreinte. Les mesures publiées de classe (a) (boucle propre,
continuum hors C2, part d'un transfert) sont dans `tests/invariants/test_menages.py`. S'y
ajoutent la lecture nette de D_H (ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1),
point 4) à −1 ulp et à −0,5 ε S, et la table `menages` (point 2). Seuils écrits avant l'essai
(fiche 5, § 9.6 ; critère de #60, `docs/feuille-de-route.md` § 1), non déplacés.
"""

import ast
import dataclasses
import inspect
import math

import pytest

from nations.blocs import menages as bloc
from nations.etat import schema
from nations.moteur.contrat_bloc import GRAND_LIVRE, OUVERTURE, Lecture
from nations.moteur.conversions import facteur_par_pas, par_pas
from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres import TauxDeCroissance, TauxDeFlux, varier
from nations.moteur.parametres import menages as table_menages
from nations.moteur.parametres.ensemble import (
    PARAMETRES_DE_REFERENCE,
    coefficient_de_richesse,
)
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.grand_livre import FluxPropose, ouvrir_pas

N_A = PARAMETRES_DE_REFERENCE.cadre.pas_par_an
TABLE = PARAMETRES_DE_REFERENCE.menages
EPSILON = PARAMETRES_DE_REFERENCE.cadre.tolerance_identite_pas
# Seuils écrits avant l'essai (fiche 5, § 9.6).
SEUIL_ETAT_STATIONNAIRE = 1e-10  # relatif
SEUIL_IDENTITE = 1e-12  # × S
SEUIL_IMPOTS_DOUBLES = 1e-12  # relatif
POINTS_PI = (0.0, 0.02, 0.10)
POINTS_N_A = (4, 12, 52)


def gamma_e_et_cible(pi, n_a, g_pr=0.02, g_N=0.0):
    """Γ^e, γ^e et π^{∗,pas} sur la cible π*, à n_a pas par an ; à n_a = 12, par les conversions
    du moteur (forme de Γ^e, `nations.moteur.ouverture`), ailleurs par la forme du script."""
    if n_a == N_A:
        f = facteur_par_pas(TauxDeCroissance(pi))
        gamma = (facteur_par_pas(TauxDeCroissance(g_pr))
                 * facteur_par_pas(TauxDeCroissance(g_N)) * f)
        return gamma, gamma - 1.0, f - 1.0
    gamma = ((1 + g_pr) * (1 + g_N) * (1 + pi)) ** (1 / n_a)
    return gamma, gamma - 1.0, (1 + pi) ** (1 / n_a) - 1.0


def plan(D_H, B_H, YD_m1, pi, n_a=N_A, nu_H=TABLE.nu_H, lambda_H=TABLE.lambda_H.valeur):
    """H2 à H5 par les fonctions du bloc ; D_H lu en max(0 ; ·) comme la phase 2."""
    Gamma_e, gamma_e, pis = gamma_e_et_cible(pi, n_a)
    V_H = max(0.0, D_H) + B_H
    YD_e = bloc.revenu_attendu(Gamma_e, YD_m1)
    V_etoile = bloc.richesse_visee(nu_H, n_a, YD_e, pis, V_H)
    C_regle = bloc.plan_de_la_regle(YD_e, gamma_e, V_H, lambda_H / n_a, V_etoile)
    return {"YD_e": YD_e, "V_etoile_H": V_etoile, "C_regle": C_regle,
            "C_plan": bloc.budget_de_consommation(max(0.0, D_H), C_regle), "V_H": V_H,
            "pis": pis, "Gamma_e": Gamma_e, "gamma_e": gamma_e}


def ecart(x, reference):
    return abs(x) if reference == 0.0 else abs(x / reference - 1.0)


# --------------------------------------------------------------------------
# Table des paramètres et conditions de domaine (§ 9.2 ; annotation, point 2)
# --------------------------------------------------------------------------


def test_table_egale_aux_defauts_du_script(stationnaire):
    """H3.3 : valeurs indicatives de la table égales aux défauts de `Parametres` du script ;
    unités, sources et étiquettes de l'annotation du 14/11/2026 (rang 1b de J3-d1), point 2."""
    defauts = stationnaire.Parametres()
    assert TABLE.nu_H == defauts.nu_H and TABLE.lambda_H == TauxDeFlux(defauts.lambda_H)
    nu, lam = table_menages.NU_H, table_menages.LAMBDA_H
    assert (nu.unite, nu.etiquettes) == ("années", ("eq:menages-richesse-visee",))
    assert (lam.unite, lam.etiquettes) == ("par an, taux de flux",
                                          ("eq:menages-plan-consommation",))
    assert "M27" in nu.source and "#62" in nu.source and "M27" in lam.source


@pytest.mark.parametrize("variation, motif", [
    ({"nu_H": 2.5}, "0 < ν_H λ_H < 1"),          # ν_H λ_H = 1 exactement
    ({"nu_H": 3.0}, "0 < ν_H λ_H < 1"),          # ν_H λ_H > 1
    ({"lambda_H": 12.5}, "λ ≤ n_a"),             # λ_H > n_a
    ({"lambda_H": 0.0}, "0 < λ"),
    ({"nu_H": 0.0}, "ν_H > 0"),
    ({"nu_H": -1.0}, "ν_H > 0"),
    ({"nu_H": math.nan}, "ν_H > 0"),
    ({"lambda_H": math.inf}, "float fini"),
])
def test_domaine_de_la_table_refuse(variation, motif):
    """§ 9.2 et `sec:menages-conditions` : ν_H λ_H = 1 (ou > 1), λ_H > n_a, λ_H ≤ 0, ν_H ≤ 0 ou
    non fini : refus explicite à la construction de la table, sans écrêtage."""
    with pytest.raises(DefautDeDeclaration, match=motif):
        varier(TABLE, **variation)


def test_bornes_de_la_table_admises():
    """λ_H = n_a admise avec ν_H λ_H < 1 (ν_H = 1/24 an) ; ν_H λ_H juste sous 1 admise."""
    varier(TABLE, lambda_H=float(N_A), nu_H=1.0 / 24.0)
    varier(TABLE, nu_H=math.nextafter(2.5, 0.0))


def test_coefficient_de_richesse_refuse_au_chargement_de_l_ensemble():
    """`sec:menages-conditions` : coefficient de richesse λ_H/n_a + ν_H λ_H π^{∗,pas} − γ^e ≤ 0
    refusé à la construction de l'ensemble ; 0,368 par an à la calibration (n_a fois le
    coefficient) ; frontière en π* entre 85,11 % (admis) et 85,12 % (refusé) à λ_H = 0,4, ν_H = 1
    an (`sec:menages-conditions` : π* < 85,12 % par an, frontière mesurée à 85,1175 %), et entre
    24,94 % et 24,95 % à λ_H = 0,2 (frontière mesurée à 24,9425 %)."""
    assert round(N_A * coefficient_de_richesse(PARAMETRES_DE_REFERENCE), 3) == 0.368
    p = PARAMETRES_DE_REFERENCE

    def avec(pi=None, lambda_H=None, g_pr=None):
        champs = {}
        if pi is not None:
            champs["banque_centrale"] = varier(p.banque_centrale, pi_etoile=pi)
        if lambda_H is not None:
            champs["menages"] = varier(p.menages, lambda_H=lambda_H)
        if g_pr is not None:
            champs["production"] = varier(p.production, g_pr=g_pr)
        return dataclasses.replace(p, **champs)
    assert coefficient_de_richesse(avec(pi=0.8511)) > 0.0
    with pytest.raises(DefautDeDeclaration, match="coefficient de richesse"):
        avec(pi=0.8512)
    # λ_H = 0,2 : frontière à 24,94 % ; une croissance réelle forte rend le coefficient négatif.
    assert coefficient_de_richesse(avec(pi=0.2494, lambda_H=0.2)) > 0.0
    with pytest.raises(DefautDeDeclaration, match="coefficient de richesse"):
        avec(pi=0.2495, lambda_H=0.2)
    with pytest.raises(DefautDeDeclaration, match="coefficient de richesse"):
        avec(g_pr=0.5)


# --------------------------------------------------------------------------
# État stationnaire, appel direct (réserve 1 ; P77)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("n_a", POINTS_N_A)
@pytest.mark.parametrize("pi", POINTS_PI)
def test_etat_stationnaire_par_appel_direct(stationnaire, pi, n_a):
    """Fiche 5, § 9.6, « État stationnaire » (classe (a) pour H2 à H5) : sur l'ouverture du
    script (π̄ = π*, ν_G = 1,15), YD^e = YD, V* = V_H, C^règle = C^plan = C et
    V_H/(n_a YD^HS) = ν_H, à 1e−10 relatif ; valeurs de contrôle de V/(n_a YD) lues sur le
    script, égales à celles de la fiche à la sixième décimale."""
    par = dataclasses.replace(stationnaire.Parametres(), pi_cible=pi, n_a=n_a, nu_G=1.15)
    stationnaire.controler_domaine(par)
    e = stationnaire.etat_stationnaire(par)
    o = stationnaire.ouverture(e, par)
    r = plan(o["D_H"], o["B_H"], o["YD_m1"], pi, n_a, par.nu_H, par.lambda_H)
    assert ecart(r["YD_e"], e["YD"]) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart(r["V_etoile_H"], e["V_H"]) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart(r["C_regle"], e["C"]) <= SEUIL_ETAT_STATIONNAIRE
    assert r["C_plan"] == r["C_regle"]  # bornes inactives : plafond et plancher sans effet
    hs = r["V_H"] / (n_a * (r["YD_e"] - r["pis"] * r["V_H"]))
    assert ecart(hs, par.nu_H) <= SEUIL_ETAT_STATIONNAIRE
    controle = {(0.02, 4): 0.980535, (0.02, 12): 0.980566, (0.02, 52): 0.980578,
                (0.10, 4): 0.912030, (0.10, 12): 0.912667, (0.10, 52): 0.912911,
                (0.0, 4): 1.0, (0.0, 12): 1.0, (0.0, 52): 1.0}[(pi, n_a)]
    assert round(r["V_H"] / (n_a * r["YD_e"]), 6) == controle


# --------------------------------------------------------------------------
# Cas à la main sur le grand livre : 90 % servi, impôts doublés (§ 3.N-6, § 3.N-7)
# --------------------------------------------------------------------------

OUVERTURE_DU_CAS = {"D_H": 1200.0, "D_F": 400.0, "L": 500.0, "B_H": 0.0, "B_Bk": 300.0,
                    "B_CB": 100.0, "Res": 50.0, "L_CB": 20.0, "M_G": 150.0, "K": 900.0,
                    "IN": 100.0}


@dataclasses.dataclass(frozen=True)
class _Cadre:
    tolerance_identite_pas: float = EPSILON
    tolerance_identite_cumulee: float = PARAMETRES_DE_REFERENCE.cadre.tolerance_identite_cumulee


def _etat_du_cas():
    v = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(OUVERTURE_DU_CAS, s)
         for s in cat.SECTEURS}
    variables = {"v_e": 1.0, "IN_vol": 1.4, "pr": 1.0, "K_vol": 24.0, "W": 0.8, "U": 0.05,
                 "N": 0.95, "N_pa": 1.0, "mu_tilde": 0.2, "YD_m1": 80.0, "i_L": 0.05,
                 "i_D": 0.03, "pi_e": 0.02, "r_hat_etoile": 0.01, "pi_etoile": 0.02}
    return schema.EtatPays(identifiant="A", graine=1, t=0,
                           registre_prix=tuple(1.02 ** (-u / 12) for u in range(1, 14)),
                           **OUVERTURE_DU_CAS, **v, **variables)


def _derouler_le_cas(montants):
    """Un pas du grand livre où seules les lignes de `montants` (ligne → terme → u.m.) sont non
    nulles ; rend (grand livre clos en phase 9, D_H après chaque phase)."""
    gl = ouvrir_pas(_etat_du_cas(), _Cadre())
    d_h = {}
    for phase in cat.PHASES:
        for ligne in cat.LIGNES_DE_LA_PHASE[phase]:
            if ligne.proposant is not None:
                termes = {t.nom: montants.get(ligne.identifiant, {}).get(t.nom, 0.0)
                          for t in ligne.termes}
                gl.proposer(FluxPropose(ligne.identifiant, termes, ligne.proposant))
        gl.clore_phase(phase)
        d_h[phase] = gl.position("D_H")
    return gl, d_h


def _revenu_par_h7(gl):
    return bloc.revenu_disponible(tuple(gl.montant_execute(ligne, "menages")
                                        for ligne in bloc.LIGNES_DU_REVENU))


def test_identite_du_cas_a_90_pour_cent():
    """Fiche 5, § 9.6, « Identité, cas à 90 % » (§ 3.N-7) : D_H = 1 200, budget de 96 servi à
    90 % (H6, p × v), WB = 80, intérêts de 0,03 × 1 200/12 = 3 : C = 86,4, YD = 83 par H7 sur
    la colonne des ménages, D_H de clôture = 1 196,6 par le stock et par les flux ; le budget
    non dépensé, 9,6, reste en D_H ; à 1e−12 × S^H."""
    p, budget = 1.2, 96.0
    C = bloc.consommation(p, 0.9 * budget / p)
    interets = par_pas(TauxDeFlux(0.03)) * 1200.0
    gl, d_h = _derouler_le_cas({"5": {"WB": 80.0}, "1": {"C": C}, "10": {"iD_DH": interets}})
    s = gl.echelle("menages")
    yd = _revenu_par_h7(gl)
    assert abs(C - 86.4) <= SEUIL_IDENTITE * s
    assert abs(yd - 83.0) <= SEUIL_IDENTITE * s
    assert abs(d_h["9"] - 1196.6) <= SEUIL_IDENTITE * s
    assert abs(d_h["9"] - (1200.0 + yd - C)) <= SEUIL_IDENTITE * s
    assert abs((budget - C) - 9.6) <= SEUIL_IDENTITE * s


def test_impots_doubles_sur_le_grand_livre_et_budget_du_tour_suivant():
    """Fiche 5, § 9.6, « Bornes » (c) (§ 3.N-6) : impôts des ménages doublés pendant un tour (16
    → 32), D_H = 1 200, WB = 80, budget de 96, intérêts de 3 : D_H vaut 1 280, 1 184 puis 1 155
    après les phases 4, 5 et 6 (à 1e−12 × S^H) ; le budget du tour suivant baisse de
    ΔT_H (α_Y Γ^e + λ_H/n_a − γ^e + ν_H λ_H π^{∗,pas}) = 10,12 pour ΔT_H = 16, à 1e−12 relatif
    (appel direct de H2 à H5, YD_{t−1} et D_H d'ouverture abaissés de ΔT_H)."""
    interets = par_pas(TauxDeFlux(0.03)) * 1200.0
    gl, d_h = _derouler_le_cas({"5": {"WB": 80.0}, "1": {"C": 96.0},
                                "10": {"iD_DH": interets}, "7": {"T_H": 32.0}})
    s = gl.echelle("menages")
    for phase, attendu in (("4", 1280.0), ("5", 1184.0), ("6", 1155.0)):
        assert abs(d_h[phase] - attendu) <= SEUIL_IDENTITE * s, phase
    yd = _revenu_par_h7(gl)
    sans_choc = plan(1171.0, 0.0, yd + 16.0, 0.02)
    avec_choc = plan(1155.0, 0.0, yd, 0.02)
    gamma_e, pis = sans_choc["gamma_e"], sans_choc["pis"]
    nu, lam = TABLE.nu_H, TABLE.lambda_H.valeur
    attendu = 16.0 * ((1 - nu * lam) * sans_choc["Gamma_e"] + lam / N_A - gamma_e
                      + nu * lam * pis)
    baisse = sans_choc["C_plan"] - avec_choc["C_plan"]
    assert ecart(baisse, attendu) <= SEUIL_IMPOTS_DOUBLES
    assert round(baisse, 2) == 10.12


# --------------------------------------------------------------------------
# Lecture de l'inflation, changement de cible, bornes (a) et (b), lecture nette
# --------------------------------------------------------------------------


class _VueDEssai:
    """Vue d'essai de la phase 2 : ouverture, paramètres, grandeurs du moteur ; écritures
    relevées. Aucun accès au registre (attribut absent : une lecture lèverait)."""

    def __init__(self, etat, grandeurs, parametres=PARAMETRES_DE_REFERENCE):
        self.ouverture = etat
        self.parametres = parametres
        self._grandeurs = grandeurs
        self.pas = {}

    def lire(self, nom):
        return self._grandeurs[nom]

    def ecrire_pas(self, nom, valeur):
        assert nom not in self.pas
        self.pas[nom] = valeur


def _grandeurs(pi):
    gamma, gamma_e, pis = gamma_e_et_cible(pi, N_A)
    return {"Gamma_e": gamma, "gamma_e": gamma_e, "pi_etoile_pas": pis}


def test_plan_insensible_au_registre_de_l_indice():
    """Fiche 5, § 9.6, « Lecture de l'inflation » (#58 ; C16 révisée) : appel direct de la
    phase 2, deux ouvertures qui ne diffèrent que par le registre de l'indice (stationnaire à
    2 %, puis à 10 % et décalé) : les quatre écritures identiques au bit (écart nul)."""
    etat = _etat_du_cas()
    autre = dataclasses.replace(etat, registre_prix=tuple(3.0 * 1.10 ** (-u / 12)
                                                          for u in range(1, 14)))
    assert autre.registre_prix != etat.registre_prix
    vues = [_VueDEssai(e, _grandeurs(0.02)) for e in (etat, autre)]
    for vue in vues:
        bloc.Menages().phase_2(vue)
    assert set(vues[0].pas) == {"YD_e", "V_etoile_H", "C_regle", "C_plan"}
    assert {k: v.hex() for k, v in vues[0].pas.items()} == {
        k: v.hex() for k, v in vues[1].pas.items()}


def test_changement_de_cible_releve_le_budget(stationnaire):
    """Fiche 5, § 9.6, « Effet d'un changement de cible » (réserve 9) : appel direct, états
    d'ouverture fixés à l'état résolu à 2 %, π* passant de 2 % à 1 % : le plan monte, d'une
    ampleur dans [0,3 % ; 0,8 %] (mesure de la fiche : +0,5543 %)."""
    par = dataclasses.replace(stationnaire.Parametres(), pi_cible=0.02, nu_G=1.15)
    o = stationnaire.ouverture(stationnaire.etat_stationnaire(par), par)
    a_2 = plan(o["D_H"], o["B_H"], o["YD_m1"], 0.02)["C_plan"]
    a_1 = plan(o["D_H"], o["B_H"], o["YD_m1"], 0.01)["C_plan"]
    hausse = a_1 / a_2 - 1.0
    assert 0.003 <= hausse <= 0.008
    assert round(100 * hausse, 4) == 0.5543


def test_bornes_plafond_et_plancher_par_appel_direct(stationnaire):
    """Fiche 5, § 9.6, « Bornes » (a) et (b), exacts : (a) plafond inactif à l'état résolu,
    marge de 12,24 mois de consommation à 2 % ; D_H = 0,5 C^règle donne C^plan = D_H ;
    (b) YD_{t−1} = −YD̄ donne C^plan = 0."""
    par = dataclasses.replace(stationnaire.Parametres(), pi_cible=0.02, nu_G=1.15)
    o = stationnaire.ouverture(stationnaire.etat_stationnaire(par), par)
    r = plan(o["D_H"], o["B_H"], o["YD_m1"], 0.02)
    assert r["C_plan"] == r["C_regle"] < o["D_H"]
    assert round(o["D_H"] / r["C_plan"], 2) == 12.24  # mois de consommation (n_a = 12)
    demi = 0.5 * r["C_regle"]
    assert bloc.budget_de_consommation(demi, r["C_regle"]) == demi
    plancher = plan(o["D_H"], o["B_H"], -o["YD_m1"], 0.02)
    assert plancher["C_regle"] < 0.0 and plancher["C_plan"] == 0.0


# Échelle déclarée du bilan des ménages pour le cas « −0,5 ε × S » (S^H du cas à la main).
_S_H = 1200.0


@pytest.mark.parametrize("D_H", [-math.ulp(0.0), -math.ulp(1.0), -0.5 * EPSILON * _S_H, 0.0,
                                 -0.0], ids=repr)
def test_lecture_nette_de_d_h_dans_h3_h4_h5(D_H):
    """ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1), point 4 ; A8.2 : un dépôt
    d'ouverture négatif (poussière admise par la lecture nette, testée à −1 ulp et à
    −0,5 ε × S) est lu en max(0 ; ·) par la phase 2 : V_H = B_H dans H3 et H4, plafond nul dans
    H5, C^plan = +0,0 exactement (dans le domaine du plan, P120), sans `PlanHorsDomaine`.
    Comparé au bit à la forme recalculée par le test."""
    etat = dataclasses.replace(_etat_du_cas(), D_H=D_H)
    vue = _VueDEssai(etat, _grandeurs(0.02))
    bloc.Menages().phase_2(vue)
    attendu = plan(0.0, 0.0, 80.0, 0.02)
    assert attendu["V_H"] == 0.0
    for nom in ("YD_e", "V_etoile_H", "C_regle"):
        assert vue.pas[nom] == attendu[nom], nom
    assert vue.pas["C_plan"] == 0.0 and math.copysign(1.0, vue.pas["C_plan"]) == 1.0


# --------------------------------------------------------------------------
# Phases, empreinte, déclaration (inspection)
# --------------------------------------------------------------------------


def test_declaration_conforme_a_tab_menages_phases():
    """`tab:menages-phases` et fiche 5, § 9.6, « Phases » : sièges en phases 2, 5 et 9
    seulement ; en phase 2, l'ouverture (D_H, B_H, YD_{t−1}) et les grandeurs du moteur
    (Γ^e, γ^e, π^{∗,pas}) seulement, ni WB, N*, y*, G^plan, I^plan, ni le registre ; en phase 5,
    p et C^vol (écrits par les blocs prix et production, groupes antérieurs), ligne 1 ; en
    phase 9, les montants exécutés des lignes 5, 6, 7, 10, 11a, 14 et 15 (phases ≤ 6), état
    YD_{t−1} ; aucune ligne hors de la ligne 1, aucune couverture."""
    sieges = {s.etape: s for s in bloc.Menages.declaration.sieges}
    assert set(sieges) == {"2", "5", "9"}
    deux = sieges["2"]
    assert set(deux.lit) == {Lecture(OUVERTURE, "D_H"), Lecture(OUVERTURE, "B_H"),
                             Lecture(OUVERTURE, "YD_m1"), Lecture("0", "Gamma_e"),
                             Lecture("0", "gamma_e"), Lecture("0", "pi_etoile_pas")}
    assert deux.ecrit == ("YD_e", "V_etoile_H", "C_regle", "C_plan")
    assert (deux.propose, deux.couvre, deux.etat) == ((), (), ())
    cinq = sieges["5"]
    assert set(cinq.lit) == {Lecture("5", "p"), Lecture("5", "C_vol")}
    assert (cinq.ecrit, cinq.propose, cinq.couvre, cinq.etat) == ((), ("1",), (), ())
    neuf = sieges["9"]
    assert set(neuf.lit) == {Lecture(GRAND_LIVRE, ligne) for ligne in bloc.LIGNES_DU_REVENU}
    assert bloc.LIGNES_DU_REVENU == ("5", "6", "7", "10", "11a", "14", "15")
    assert all(cat.LIGNE[ligne].phase in ("4", "6") for ligne in bloc.LIGNES_DU_REVENU)
    assert (neuf.ecrit, neuf.propose, neuf.couvre, neuf.etat) == ((), (), (), ("YD_m1",))
    # Chaque ligne de H7 touche la colonne des ménages ; aucune autre ligne courante du
    # socle ne la touche, hors de la ligne 1 (dépense), des titres (19a, 19b, nuls au socle,
    # M27 (c)) et de la contrepartie 17 (variation des dépôts).
    touchent = {ligne.identifiant for ligne in cat.LIGNES
                if any("menages" in (t.colonne_plus, t.colonne_moins) for t in ligne.termes)}
    assert touchent - set(bloc.LIGNES_DU_REVENU) == {"1", "17", "19a-ménages", "19b-ménages"}


def test_empreinte_une_variable_d_etat_aucun_tirage():
    """Fiche 5, § 9.6, « Empreinte » : une variable d'état, YD_{t−1}, du radical `menages` ;
    aucun registre lu (déclaration) ; aucun tirage (ni `numpy`, ni `random`, ni graine dans le
    module)."""
    assert [v.nom for v in schema.VARIABLES_DES_BLOCS if v.proprietaire == "menages"] == ["YD_m1"]
    lues = {lu.source for s in bloc.Menages.declaration.sieges for lu in s.lit}
    assert "registre" not in lues
    arbre = ast.parse(inspect.getsource(bloc))
    importes = {a.name for n in ast.walk(arbre) if isinstance(n, ast.Import) for a in n.names} | {
        n.module for n in ast.walk(arbre) if isinstance(n, ast.ImportFrom)}
    assert not importes & {"random", "numpy", "numpy.random"}
    assert "graine" not in inspect.getsource(bloc)


def test_aucun_attribut_d_instance():
    """Bloc sans état caché : `__slots__` vide, aucun `__dict__`."""
    b = bloc.Menages()
    assert not hasattr(b, "__dict__") and bloc.Menages.__slots__ == ()
    assert isinstance(bloc.Menages.declaration.sieges, tuple)
