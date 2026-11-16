"""Bloc 9, État et dette : critères (a) par appel direct des fonctions du bloc (#132, rang 3
de J3-d2).

Critères écrits avant l'essai (`docs/feuille-de-route.md` § 1, critères de #132 et précisions
du rang 1a, P156 à P164 ; `sec:finances_publiques-conditions`), non déplacés :

- **état stationnaire** (F2) : E1 à E13 par appel direct sur l'ouverture du script d'état
  stationnaire, n_a ∈ {4 ; 12 ; 52} (n_a = 4 hors domaine, #87, point de robustesse de la forme
  fermée), π* ∈ {0 ; 2 ; 10 %}, ν_G = 1,15 passé explicitement (défaut du script ν_G = 1, hors
  domaine) : à 1e−10 relatif ; Y^HS_t/Y^HS_{t−1} = Γ̄, M^G* = ν_G PB, Em = γ̄ B ; nullités en
  absolu (T^cou, T_F, Tr, parts de E13) ;
- **lecture nette** (engagement 4, F5) : épreuve à −1 ulp et à −0,5 ε S de E1 (G^plan = +0),
  E4 (assiette inchangée à k ε S), E5 et E12 (égales au bit à leur valeur à D = 0), E6 (Tr ≥ 0)
  et E9 (absorbe la poussière) ;
- **liste fermée des lectures brutes** (engagement 2 ; ADR 0013, annotation du 15/11/2026,
  point 4) et **localité** des max(0 ; ·) (critère de #132) : contrôle sur l'arbre syntaxique
  (lectures par `vue.ouverture.<moyen>`, `vue.grand_livre.position` ou `.ouverture`, et toute
  constante "M_G", "D_H" ou "D_F" des méthodes de la classe, de phase ou auxiliaires ; aucun
  alias de `vue.ouverture` ni de `vue.grand_livre` ; paramètre d'une lecture nette employé
  seulement dans max(0.0, ·)) ; étendu aux blocs 5 (H3, H4, H5) et 6 (F3) par le critère de
  #142 (branche « forme du code », rang 3) ;
- **couverture** (F6) : E4(i + 0,01) − E4(i) = φ par_pas(0,01) A à 1e−12 relatif ; φ = 0 ⇒
  T^cou = 0 exactement ;
- **bornes** (critère 16) : B_CB + θ_CB Em ≥ 0 et B_Bk + ΔB^prim_Bk ≥ 0 sous rachat (Em < 0),
  ς_B sous la même forme (P159) ;
- **phases et empreinte** (critères 2 et 19) : déclaration conforme à
  `tab:finances_publiques-phases`, une variable d'état, aucun tirage, aucun attribut d'instance.

Les critères sur le moteur (stationnarité du socle complet, nullités, caisse, parts non payées,
C59, reprise, décompte de l'émission) sont dans `tests/invariants/test_socle_complet.py`.
"""

import ast
import dataclasses
import inspect
import math
from pathlib import Path

import pytest

from nations.blocs import finances_publiques as bloc
from nations.blocs import investissement as bloc_6
from nations.blocs import menages as bloc_5
from nations.etat import schema
from nations.moteur.contrat_bloc import GRAND_LIVRE, OUVERTURE, REGISTRE, Lecture
from nations.moteur.conversions import TauxDeFlux, par_pas
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.noyau import catalogue as cat

N_A = PARAMETRES_DE_REFERENCE.cadre.pas_par_an
EPSILON = PARAMETRES_DE_REFERENCE.cadre.tolerance_identite_pas
NU_G = 1.15
# Seuils écrits avant l'essai (critères de #132, § 1 de la feuille de route).
SEUIL_ETAT_STATIONNAIRE = 1e-10  # relatif
SEUIL_COUVERTURE = 1e-12  # relatif
POINTS_PI = (0.0, 0.02, 0.10)
POINTS_N_A = (4, 12, 52)
SPECIFICATION = (Path(__file__).resolve().parents[2] / "docs" / "specification"
                 / "nations_et_marches.tex")


def ecart(x, reference):
    return abs(x / reference - 1.0)


def _resolu(stationnaire, pi, n_a):
    par = dataclasses.replace(stationnaire.Parametres(), pi_cible=pi, n_a=n_a, nu_G=NU_G)
    stationnaire.controler_domaine(par)
    e = stationnaire.etat_stationnaire(par)
    return par, e, stationnaire.ouverture(e, par)


def regles_du_pas_0(par, e, o):
    """E1 à E13 par les fonctions du bloc sur l'ouverture `o` du script, les montants exécutés
    du pas 0 étant ceux de l'état résolu `e` (lignes servies, plafonds inactifs) ; taux convertis
    au pas par n_a (`par.n_a`), Γ^e = Γ̄ et π^{∗,pas} du script (π̄ = π*)."""
    n = par.n_a
    pis, Gam = e["pis"], e["Gam"]
    y_pot = bloc.production_potentielle(o["pr"], par.U_eq, o["N_pa"])
    G_vise = bloc.depense_visee(o["registre"][0], pis, o["theta_G"], y_pot)
    G_plan = bloc.plan_de_depense(o["M_G"], G_vise)
    i_ref = bloc.taux_de_reference(par.rbar, o["pi_cible"])
    T_cou = bloc.couverture_des_interets(par.phi, (e["i_CB"] - i_ref) / n, o["B_H"], o["B_Bk"],
                                         o["B_CB"], o["L_CB"], o["Res"], o["M_G"])
    T_H = bloc.impot_des_menages(par.tau_H, Gam, o["Y_HS_m1"], T_cou)
    l11 = bloc.interets_sur_titres(e["i_CB"] / n, o["B_H"], o["B_Bk"], o["B_CB"])
    interets = l11[0] + l11[1] + l11[2]
    Tr_lev = bloc.transferts_vises(o["registre"][0], pis, par.theta_Tr, y_pot)
    Tr = bloc.transferts(Tr_lev, o["M_G"], T_H, interets, G_plan)
    G = e["G"]
    T_F = bloc.impot_des_entreprises(par.tau_F, e["C"], G, e["I"], e["dIN"], e["WB"],
                                     par.delta / n * o["K"], o["i_L"] / n * o["L"], o["i_D"] / n,
                                     o["D_F"])
    M_G_etoile = bloc.encaisse_visee(par.nu_G, G, Tr, interets)
    Em = bloc.besoin_d_emission(G, Tr, interets, T_H + T_F, e["Pi_CB"], M_G_etoile, o["M_G"])
    dB_CB, dB_H = bloc.souscriptions_banque_centrale_et_menages(par.theta_CB, Em)
    dB_Bk = bloc.souscription_banque(par.varsigma_B, Em, dB_CB)
    Y_HS = bloc.assiette_de_l_impot(e["WB"], o["i_D"] / n * o["D_H"], e["Div_F"], e["Div_Bk"],
                                    pis, o["D_H"], T_cou)
    _, tr_nv = bloc.part_non_payee(Tr_lev, Tr)
    return {"G_vise": G_vise, "G_plan": G_plan, "T_cou": T_cou, "T_H": T_H, "l11": l11,
            "interets": interets, "Tr": Tr, "T_F": T_F, "M_G_etoile": M_G_etoile, "Em": Em,
            "dB_CB": dB_CB, "dB_H": dB_H, "dB_Bk": dB_Bk, "Y_HS": Y_HS, "tr_nv": tr_nv,
            "y_pot": y_pot}


# --------------------------------------------------------------------------
# État stationnaire par appel direct (F2)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("n_a", POINTS_N_A)
@pytest.mark.parametrize("pi", POINTS_PI)
def test_etat_stationnaire_par_appel_direct(stationnaire, pi, n_a):
    """Critère 4 de la fiche 9 (classe (a)), F2 : sur l'ouverture du script (π̄ = π*, ν_G = 1,15
    explicite), un pas sans choc laisse l'assiette sur son sentier (Y^HS_t/Y^HS_{t−1} = Γ̄), la
    couverture nulle, M^G* = ν_G PB = Γ̄ M^G, Em = γ̄ B, G^plan = G (plafond de E1 inactif), T_H
    du script, intérêts i_CB B/n_a, à 1e−10 relatif ; nullités en absolu."""
    par, e, o = _resolu(stationnaire, pi, n_a)
    r = regles_du_pas_0(par, e, o)
    n = n_a
    assert r["G_plan"] == r["G_vise"]  # plafond de E1 inactif
    assert ecart(r["G_plan"], e["G"]) <= SEUIL_ETAT_STATIONNAIRE
    assert r["T_cou"] == 0.0  # i_CB = i^ref exactement : même forme de Fisher
    assert ecart(r["T_H"], e["T_H"]) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart(r["interets"], e["i_CB"] * e["B"] / n) <= SEUIL_ETAT_STATIONNAIRE
    assert r["l11"][0] == 0.0 and r["l11"][2] == 0.0  # B_H = B_CB = 0 (θ_CB = 0)
    assert (r["Tr"], r["T_F"], r["tr_nv"], r["dB_CB"], r["dB_H"]) == (0.0, 0.0, 0.0, 0.0, 0.0)
    assert ecart(r["M_G_etoile"], par.nu_G * e["PB"]) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart(r["M_G_etoile"], e["Gam"] * e["M_G"]) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart(r["Em"], e["gam"] * e["B"]) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart(r["dB_Bk"], e["gam"] * e["B_Bk"]) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart(r["Y_HS"], e["Y_HS"]) <= SEUIL_ETAT_STATIONNAIRE
    assert ecart(r["Y_HS"] / o["Y_HS_m1"], e["Gam"]) <= SEUIL_ETAT_STATIONNAIRE
    # Dette consolidée d'ouverture rapportée à n_a fois le PIB : celle du script.
    dette = (o["B_Bk"] + o["B_CB"] + o["B_H"] - o["M_G"] - o["E_CB"]) / (n * e["PIB"])
    assert ecart(dette, (e["B"] - e["M_G"]) / (n * e["PIB"])) <= SEUIL_ETAT_STATIONNAIRE


def test_impot_des_entreprises_sous_tau_F_positif(stationnaire):
    """E5 sous τ_F = 0,1 (appel direct, levier ouvert pour l'épreuve seulement) : T_F = τ_F Π^av
    du script, à 1e−10 relatif, Π^av = C + G + I + ΔIN − WB − δK/n_a − i_L L/n_a + i_D D_F/n_a."""
    par, e, o = _resolu(stationnaire, 0.02, N_A)
    T_F = bloc.impot_des_entreprises(0.1, e["C"], e["G"], e["I"], e["dIN"], e["WB"],
                                     par.delta / N_A * o["K"], o["i_L"] / N_A * o["L"],
                                     o["i_D"] / N_A, o["D_F"])
    assert ecart(T_F, 0.1 * e["Pi_av"]) <= SEUIL_ETAT_STATIONNAIRE


# --------------------------------------------------------------------------
# Lecture nette (engagement 4, F5)
# --------------------------------------------------------------------------

_S_G = 1000.0  # échelle déclarée du bilan de l'État pour le cas « −0,5 ε S »
POUSSIERES = (-math.ulp(0.0), -math.ulp(1.0), -0.5 * EPSILON * _S_G)


@pytest.mark.parametrize("poussiere", POUSSIERES, ids=repr)
def test_lecture_nette_de_e1(poussiere):
    """E1 lit max(0 ; M^G) : sous une poussière, G^plan = +0 exactement (dans le domaine du plan,
    sans `PlanHorsDomaine`)."""
    G_plan = bloc.plan_de_depense(poussiere, 100.0)
    assert G_plan == 0.0 and math.copysign(1.0, G_plan) == 1.0
    assert bloc.plan_de_depense(-0.0, 100.0) == 0.0
    assert math.copysign(1.0, bloc.plan_de_depense(-0.0, 100.0)) == 1.0


@pytest.mark.parametrize("poussiere", POUSSIERES, ids=repr)
def test_lecture_nette_de_e5_et_e12(poussiere):
    """E5 lit D̃_F et E12 lit D̃_H : sous une poussière, égales au bit à leur valeur à D = 0."""
    args5 = (0.1, 107.5, 20.0, 15.0, 0.5, 100.2, 3.0, 1.25, 0.002)
    assert (bloc.impot_des_entreprises(*args5, poussiere)
            == bloc.impot_des_entreprises(*args5, 0.0))
    args12 = (80.0, 0.0, 12.0, 3.0, 0.00165)
    assert (bloc.assiette_de_l_impot(*args12, poussiere, 0.0)
            == bloc.assiette_de_l_impot(*args12, 0.0, 0.0))


@pytest.mark.parametrize("poussiere", POUSSIERES, ids=repr)
def test_lectures_brutes_de_e4_e6_e9(poussiere):
    """E6 (M^G brut) rend Tr ≥ 0 ; E9 (M^G brut) absorbe la poussière à l'émission du pas (Em plus
    grand de |poussière|, à l'arrondi près de Em) ; E4 (assiette brute) garde l'identité de bilan :
    assiette inchangée à quelques ε S (M^G s'annule algébriquement)."""
    tr = bloc.transferts(5.0, poussiere, 0.0, 0.0, 0.0)
    assert tr >= 0.0
    base = bloc.besoin_d_emission(100.0, 0.0, 1.0, 90.0, 0.2, 115.0, 0.0)
    absorbe = bloc.besoin_d_emission(100.0, 0.0, 1.0, 90.0, 0.2, 115.0, poussiere)
    assert absorbe >= base and abs(absorbe - base + poussiere) <= 4 * math.ulp(base)
    positions = dict(B_H=0.0, B_Bk=900.0, B_CB=50.0, L_CB=40.0, Res=0.0)
    a = bloc.couverture_des_interets(1.0, 1.0, M_G=poussiere, **positions)
    b = bloc.couverture_des_interets(1.0, 1.0, M_G=0.0, **positions)
    assert abs(a - b) <= 4 * EPSILON * _S_G


# --------------------------------------------------------------------------
# Liste fermée des lectures brutes (engagement 2) et localité des max(0 ; ·)
# --------------------------------------------------------------------------

# (fonction balisée, paramètre) : moyens de paiement lus en max(0 ; ·) dans la fonction.
LECTURES_NETTES = {("plan_de_depense", "M_G"), ("impot_des_entreprises", "D_F"),
                   ("assiette_de_l_impot", "D_H"), ("part_non_payee", "disponible")}
# Lectures brutes admises (ADR 0013, annotation du 15/11/2026, point 4), et elles seules.
LECTURES_BRUTES = {("couverture_des_interets", "M_G"), ("transferts", "M_G"),
                   ("besoin_d_emission", "M_G")}
MOYENS_DE_PAIEMENT = {"M_G", "D_H", "D_F"}
# Blocs soumis au contrôle de localité : (module, lectures nettes, lectures brutes, préfixe des
# balises). Blocs 5 et 6 : critère de #142 (lecture nette de D_H dans H3, H4, H5 ; de D_F dans
# F3), aucune lecture brute d'un moyen de paiement.
BLOCS_DE_LA_LOCALITE = {
    "finances_publiques": (bloc, LECTURES_NETTES, LECTURES_BRUTES, "# eq:finances_publiques-"),
    "menages": (bloc_5, {("richesse_visee", "D_H"), ("plan_de_la_regle", "D_H"),
                         ("budget_de_consommation", "D_H")}, set(), "# eq:menages-"),
    "investissement": (bloc_6, {("dividendes", "D_F")}, set(), "# eq:investissement-"),
}


# Accesseurs du grand livre qui lisent une position par son nom (`vue.grand_livre.position`,
# `vue.grand_livre.ouverture`).
LECTURES_DU_GRAND_LIVRE = {"position", "ouverture"}


def _lecture_d_un_moyen(noeud):
    """Vrai si `noeud` lit D_H, D_F ou M^G : `vue.ouverture.<moyen>`,
    `vue.grand_livre.position("<moyen>")` ou `vue.grand_livre.ouverture("<moyen>")`."""
    if (isinstance(noeud, ast.Attribute) and noeud.attr in MOYENS_DE_PAIEMENT
            and isinstance(noeud.value, ast.Attribute) and noeud.value.attr == "ouverture"):
        return True
    return (isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Attribute)
            and noeud.func.attr in LECTURES_DU_GRAND_LIVRE and noeud.args
            and isinstance(noeud.args[0], ast.Constant)
            and noeud.args[0].value in MOYENS_DE_PAIEMENT)


def _constantes_hors_lecture(methode):
    """Constantes "M_G", "D_H" ou "D_F" d'une méthode de phase qui ne sont pas le nom lu par un
    accesseur reconnu (`_lecture_d_un_moyen`) : toute autre voie de lecture (accesseur nouveau,
    `getattr`, clé) est un défaut tant que le test ne la reconnaît pas."""
    nommees = {id(n.args[0]) for n in ast.walk(methode)
               if isinstance(n, ast.Call) and _lecture_d_un_moyen(n)}
    return [n.value for n in ast.walk(methode) if isinstance(n, ast.Constant)
            and n.value in MOYENS_DE_PAIEMENT and id(n) not in nommees]


def _hors_d_un_max_nul(fonction, parametre):
    """Occurrences de `parametre` dans `fonction` hors d'un appel max(0.0, <parametre>)."""
    dans_un_max = {id(n.args[1]) for n in ast.walk(fonction)
                   if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                   and n.func.id == "max" and len(n.args) == 2 and not n.keywords
                   and isinstance(n.args[0], ast.Constant) and n.args[0].value == 0.0
                   and type(n.args[0].value) is float
                   and isinstance(n.args[1], ast.Name) and n.args[1].id == parametre}
    return [ast.unparse(n) for n in ast.walk(fonction)
            if isinstance(n, ast.Name) and n.id == parametre and id(n) not in dans_un_max]


def _parametres(fonction):
    return [a.arg for a in fonction.args.args]


# Accès de la vue d'où partent les lectures d'un moyen de paiement (`vue.ouverture`,
# `vue.grand_livre`) : ils ne s'emploient que suivis d'un attribut ou d'une méthode, jamais liés à
# un nom (alias), passés en argument ni rendus, ce qui soustrairait la lecture au contrôle.
ACCES_DE_LA_VUE = {"ouverture", "grand_livre"}


def _acces_detaches(noeud):
    """Accès `<nom>.ouverture` ou `<nom>.grand_livre` de `noeud` qui ne sont pas le préfixe d'un
    attribut (`vue.ouverture.M_G`, `vue.grand_livre.position`) : alias, argument, valeur rendue."""
    prefixes = {id(n.value) for n in ast.walk(noeud) if isinstance(n, ast.Attribute)}
    return [ast.unparse(n) for n in ast.walk(noeud)
            if isinstance(n, ast.Attribute) and n.attr in ACCES_DE_LA_VUE
            and isinstance(n.value, ast.Name) and id(n) not in prefixes]


def _corps_de_la_classe(classe):
    """Instructions du corps de la classe du bloc hors de sa déclaration : toute méthode (de phase
    ou auxiliaire) ; la docstring, `__slots__` et `declaration` sont les seules autres
    instructions admises (une instruction de classe nouvelle échappe sinon au contrôle)."""
    corps = []
    for n in classe.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            corps.append(n)
        elif isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant):
            continue
        else:
            assert (isinstance(n, ast.Assign) and len(n.targets) == 1
                    and isinstance(n.targets[0], ast.Name)
                    and n.targets[0].id in {"__slots__", "declaration"}), ast.unparse(n)
    return corps


@pytest.mark.parametrize("radical", sorted(BLOCS_DE_LA_LOCALITE))
def test_lectures_brutes_liste_fermee_et_localite(radical):
    """Engagement 2 et localité (critères de #132 ; blocs 5 et 6 : critère de #142, aucun
    max(0 ; ·) dans les méthodes de phase, lecture nette dans H3, H4, H5 et F3, aucune lecture
    brute d'un moyen de paiement) : dans toutes les méthodes de la classe du bloc
    (de phase ou auxiliaires), toute lecture de D_H, D_F ou M^G (`vue.ouverture.<moyen>`,
    `vue.grand_livre.position` ou `.ouverture` du moyen) est passée telle quelle à une fonction du
    module, jamais transformée ni écrêtée sur place, et aucune constante "M_G", "D_H" ou "D_F"
    n'y figure hors de ces accesseurs ; chaque (fonction, paramètre) qui la reçoit est dans la
    liste des lectures nettes, dont la fonction n'emploie le paramètre qu'à l'intérieur de
    max(0.0, <paramètre>), ou dans la liste fermée des lectures brutes ; aucune méthode n'appelle
    `max`. Réserve M1 de la revue finale de J3-d2 : `vue.ouverture` et `vue.grand_livre` ne sont
    jamais liés à un nom ni passés tels quels (`_acces_detaches`), dans tout le module ; hors de
    la classe, aucune lecture d'un moyen de paiement ; le corps de la classe ne contient que ses
    méthodes, sa docstring, `__slots__` et `declaration` (`_corps_de_la_classe`)."""
    module, lectures_nettes, lectures_brutes, balise = BLOCS_DE_LA_LOCALITE[radical]
    arbre = ast.parse(inspect.getsource(module))
    fonctions = {n.name: n for n in arbre.body if isinstance(n, ast.FunctionDef)}
    classe = next(n for n in arbre.body if isinstance(n, ast.ClassDef))
    methodes = _corps_de_la_classe(classe)
    assert not _acces_detaches(arbre), _acces_detaches(arbre)
    hors_de_la_classe = [n for n in arbre.body if n is not classe]
    assert not [n for h in hors_de_la_classe for n in ast.walk(h) if _lecture_d_un_moyen(n)]
    relevees = set()
    for methode in methodes:
        appels_max = [n for n in ast.walk(methode) if isinstance(n, ast.Call)
                      and isinstance(n.func, ast.Name) and n.func.id == "max"]
        assert not appels_max, f"max dans {methode.name} (localité)"
        assert not _constantes_hors_lecture(methode), (
            f"nom d'un moyen de paiement hors d'un accesseur reconnu dans {methode.name}")
        lectures = [n for n in ast.walk(methode) if _lecture_d_un_moyen(n)]
        for appel in (n for n in ast.walk(methode) if isinstance(n, ast.Call)
                      and isinstance(n.func, ast.Name) and n.func.id in fonctions):
            noms = _parametres(fonctions[appel.func.id])
            for i, argument in enumerate(appel.args):
                if _lecture_d_un_moyen(argument):
                    relevees.add((appel.func.id, noms[i]))
                    lectures.remove(argument)
            for mot in appel.keywords:
                if _lecture_d_un_moyen(mot.value):
                    relevees.add((appel.func.id, mot.arg))
                    lectures.remove(mot.value)
        assert not lectures, f"lecture d'un moyen de paiement hors d'un appel dans {methode.name}"
    assert relevees == lectures_nettes | lectures_brutes
    for nom, parametre in lectures_nettes:
        assert balise in inspect.getsource(getattr(module, nom))
        assert f"max(0.0, {parametre})" in ast.unparse(fonctions[nom]), (nom, parametre)
        hors = _hors_d_un_max_nul(fonctions[nom], parametre)
        assert not hors, (nom, parametre, hors)
    for nom, parametre in lectures_brutes:
        source = inspect.getsource(getattr(module, nom))
        assert "Lecture brute de M^G" in source and "point 4" in source, nom


# --------------------------------------------------------------------------
# Couverture (F6), bornes (critère 16), parts non payées (E13)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", POINTS_PI)
def test_couverture_d_un_point_de_taux(stationnaire, pi):
    """F6 : un point de taux directeur de plus relève la couverture de A/n_a × 0,01,
    A = B − M^G − E^CB d'ouverture, à 1e−12 relatif ; sous φ = 0, couverture nulle exactement."""
    par, e, o = _resolu(stationnaire, pi, N_A)
    positions = {q: o[q] for q in ("B_H", "B_Bk", "B_CB", "L_CB", "Res", "M_G")}
    i_ref = bloc.taux_de_reference(par.rbar, pi)
    i_CB = e["i_CB"]

    def couverture(phi, i):
        return bloc.couverture_des_interets(phi, par_pas(TauxDeFlux(i - i_ref)), **positions)
    A = o["B_H"] + o["B_Bk"] + o["B_CB"] - o["M_G"] - o["E_CB"]
    hausse = couverture(1.0, i_CB + 0.01) - couverture(1.0, i_CB)
    assert ecart(hausse, par_pas(TauxDeFlux(0.01)) * A) <= SEUIL_COUVERTURE
    for i in (i_CB, i_CB + 0.01, i_CB - 0.03):
        assert couverture(0.0, i) == 0.0


@pytest.mark.parametrize("theta_CB", (0.0, 0.05, 0.5, 1.0))
@pytest.mark.parametrize("varsigma_B", (0.0, 0.5, 1.0))
def test_bornes_sous_rachat(theta_CB, varsigma_B):
    """Critère 16 (P159) : sous un rachat Em ∈ [−B ; 0[, sur une composition de la dette
    B_CB = θ_CB B et B_Bk = (1 − θ_CB) B (forme du sentier), E10 et E11 tiennent B_CB + θ_CB Em
    ≥ 0 et B_Bk + ΔB^prim_Bk ≥ 0 ; ς_B s'applique sous la même forme qu'à l'émission."""
    B = 1000.0
    for k in range(101):
        Em = -B * k / 100.0
        dB_CB, dB_H = bloc.souscriptions_banque_centrale_et_menages(theta_CB, Em)
        dB_Bk = bloc.souscription_banque(varsigma_B, Em, dB_CB)
        assert dB_H == 0.0
        assert theta_CB * B + dB_CB >= -1e-12 * B
        assert (1.0 - theta_CB) * B + dB_Bk >= -1e-12 * B
        assert dB_Bk == (1.0 - varsigma_B) * (Em - theta_CB * Em)


def test_part_non_payee_contrainte_de_conservation():
    """E13 : payé = min(dû ; max(0 ; disponible)) dans [0 ; dû], non payé = dû − payé ≥ 0 ;
    disponible négatif (poussière) : rien de payé ; transferts : (Tr^lev, Tr) rend Tr payé et
    Tr^lev − Tr non versé."""
    for du, disponible in ((10.0, 25.0), (10.0, 4.0), (10.0, 0.0), (10.0, -math.ulp(0.0)),
                           (0.0, 3.0)):
        paye, non_paye = bloc.part_non_payee(du, disponible)
        assert 0.0 <= paye <= du and non_paye == du - paye >= 0.0
    assert bloc.part_non_payee(10.0, 4.0) == (4.0, 6.0)
    assert bloc.part_non_payee(5.0, 3.5) == (3.5, 1.5)


# --------------------------------------------------------------------------
# Phases, déclaration, empreinte
# --------------------------------------------------------------------------


def _ouvertures(*noms):
    return {Lecture(OUVERTURE, nom) for nom in noms}


def _lignes_executees(*lignes):
    return {Lecture(GRAND_LIVRE, ligne) for ligne in lignes}


# Transcription de `tab:finances_publiques-phases`, siège par siège : (lectures, écritures de
# variables du pas), telles que le tableau les donne une fois complété par le commit `docs:` de
# #132 qui suit (écritures `G_vise` en phase 2 et `T_F` en phase 6, que le tableau omet). Sources :
# OUVERTURE, REGISTRE, GRAND_LIVRE (montants exécutés, ou M^{G,8a} en 8 (b)), ou la phase de
# l'écriture lue (« 0 » : grandeurs du moteur et entrées de scénario). Paramètres des tables :
# non déclarés comme lectures. Phase 6, « ses calculs de la phase 2 » : T_H, Tr^lev et Tr.
TABLEAU_DES_PHASES = {
    "2": (_ouvertures("M_G", "B_H", "B_Bk", "B_CB", "L_CB", "Res", "pr", "N_pa", "Y_HS_m1",
                      "pi_etoile")
          | {Lecture(REGISTRE, "dernier_prix"), Lecture("1", "i_CB"), Lecture("0", "Gamma_e"),
             Lecture("0", "pi_etoile_pas")},
          {"G_vise", "G_plan", "T_cou", "T_H", "Tr_lev", "Tr"}),
    "5": ({Lecture("5", "p"), Lecture("5", "G_vol")}, set()),
    "6": (_ouvertures("B_H", "B_Bk", "B_CB", "K", "L", "D_F", "i_L", "i_D")
          | {Lecture("1", "i_CB"), Lecture("2", "T_H"), Lecture("2", "Tr_lev"),
             Lecture("2", "Tr")}
          | _lignes_executees("1", "2", "3", "4", "5"),
          {"T_F", "Tr_non_verses"}),
    "7": (_ouvertures("M_G", "D_H")
          | {Lecture("0", "varsigma_B"), Lecture("0", "pi_etoile_pas"), Lecture("1", "theta_CB"),
             Lecture("1", "Pi_CB"), Lecture("2", "T_cou")}
          | _lignes_executees("2", "5", "6", "7", "10", "11a", "11b", "11c", "14", "15"),
          {"M_G_etoile", "Em"}),
    "8b": ({Lecture("1", "Pi_CB"), Lecture(GRAND_LIVRE, "M_G")}, {"perte_non_couverte"}),
}
# Écriture de chaque variable du pas dans la colonne « Le bloc écrit » du tableau (fragment
# LaTeX ou libellé) ; `G_vise` et `T_F` : écritures à ajouter par `docwriter`.
ECRITURES_DU_TABLEAU = {
    "2": {"G_vise": "plan non plafonné", "G_plan": r"$G^{\mathrm{plan}}_t$",
          "T_cou": r"$T^{\mathrm{cou}}_t$", "T_H": r"$T_{H,t}$",
          "Tr_lev": r"$\mathit{Tr}^{\mathrm{lev}}_t$", "Tr": r"$\mathit{Tr}_t$"},
    "5": {},
    "6": {"T_F": r"$T_{F,t}$", "Tr_non_verses": "transferts non versés"},
    "7": {"M_G_etoile": r"$M^{G*}_t$", "Em": r"$\mathit{Em}_t$"},
    "8b": {"perte_non_couverte": "perte non couverte"},
}


def _colonne_ecrite_du_tableau():
    """Phase → cellule « Le bloc écrit, ou propose au noyau » de `tab:finances_publiques-phases`,
    lue dans la spécification (lignes après la fin de l'en-tête, jusqu'au filet du bas)."""
    texte = SPECIFICATION.read_text(encoding="utf-8")
    debut = texte.index(r"\label{tab:finances_publiques-phases}")
    corps = texte[texte.index(r"\endhead", debut) + len(r"\endhead"):
                  texte.index(r"\bottomrule", debut)]
    cellules = {}
    for ligne in corps.split("\\\\\n"):
        if not ligne.strip():
            continue
        phase, *_, ecrit = ligne.strip().split(" & ")
        cellules[phase.replace(r"\,", "").replace("(", "").replace(")", "")] = ecrit
    return cellules


def test_declaration_conforme_a_tab_finances_publiques_phases():
    """`tab:finances_publiques-phases` et ADR 0013, annotation du 15/11/2026, point 1 : sièges en
    phases 2, 5, 6, 7 et 8 (b) seulement ; lectures et écritures de variables du pas de chaque
    siège **égales** (ensembles) à la transcription du tableau, `TABLEAU_DES_PHASES` ; aucune
    écriture en phase 1 ; en phase 6, aucune lecture d'une écriture de la phase (source « 6 ») ;
    lectures du grand livre de la phase 7 sur des lignes des phases 4 à 6 ; lignes 2 (5), 6, 7,
    11a à 11c (6), trois lignes 19a (7), montant couvert de la ligne 16 (8 b) ; Y^HS écrite en
    phase 7."""
    sieges = {s.etape: s for s in bloc.FinancesPubliques.declaration.sieges}
    assert set(sieges) == set(TABLEAU_DES_PHASES) == {"2", "5", "6", "7", "8b"}
    for etape, (lit, ecrit) in TABLEAU_DES_PHASES.items():
        assert set(sieges[etape].lit) == lit, (etape, set(sieges[etape].lit) ^ lit)
        assert len(sieges[etape].lit) == len(lit), etape
        assert set(sieges[etape].ecrit) == ecrit, (etape, set(sieges[etape].ecrit) ^ ecrit)
        assert len(sieges[etape].ecrit) == len(ecrit), etape
    assert sieges["5"].propose == ("2",)
    assert sieges["6"].propose == ("6", "7", "11a", "11b", "11c")
    assert set(sieges["7"].propose) == {"19a-ménages", "19a-banque", "19a-BC"}
    assert sieges["8b"].couvre == ("16",) and sieges["8b"].propose == ()
    assert all(s.couvre == () for e, s in sieges.items() if e != "8b")
    assert sieges["2"].propose == () and sieges["8b"].propose == ()
    assert sieges["7"].etat == ("Y_HS_m1",)
    assert all(s.etat == () for e, s in sieges.items() if e != "7")
    assert not any(lu.source == "6" for lu in sieges["6"].lit)
    assert all(cat.LIGNE[lu.nom].phase in ("4", "5", "6")
               for lu in sieges["7"].lit if lu.source == GRAND_LIVRE)


def test_tab_finances_publiques_phases_porte_chaque_ecriture():
    """Lien entre la transcription et la spécification : chaque écriture de variable du pas de
    `TABLEAU_DES_PHASES` figure, sous son écriture `ECRITURES_DU_TABLEAU`, dans la cellule « Le
    bloc écrit » de sa phase dans `tab:finances_publiques-phases`."""
    cellules = _colonne_ecrite_du_tableau()
    assert {e: set(m) for e, m in ECRITURES_DU_TABLEAU.items()} == {
        e: ecrit for e, (_, ecrit) in TABLEAU_DES_PHASES.items()}
    absentes = {(etape, nom) for etape, ecritures in ECRITURES_DU_TABLEAU.items()
                for nom, fragment in ecritures.items() if fragment not in cellules[etape]}
    assert not absentes, sorted(absentes)


def test_empreinte_une_variable_d_etat_aucun_tirage():
    """Critère 19 : une variable d'état, Y^HS_{t−1}, du radical `finances_publiques`, écrite en
    phase 7 ; aucun tirage (ni `numpy`, ni `random`, ni graine dans le module)."""
    propres = [v for v in schema.VARIABLES_DES_BLOCS if v.proprietaire == "finances_publiques"]
    assert [(v.nom, v.phase_ecriture) for v in propres] == [("Y_HS_m1", "7")]
    source = inspect.getsource(bloc)
    arbre = ast.parse(source)
    importes = {a.name for n in ast.walk(arbre) if isinstance(n, ast.Import) for a in n.names} | {
        n.module for n in ast.walk(arbre) if isinstance(n, ast.ImportFrom)}
    assert not importes & {"random", "numpy", "numpy.random"}
    assert "graine" not in source


def test_treize_balises_une_par_equation():
    """Critère de #132 : treize balises `# eq:finances_publiques-…`, une par équation E1 à E13
    (`tab:finances_publiques-equations`), chacune une seule fois, dans une fonction du module."""
    source = inspect.getsource(bloc)
    balises = [ligne.strip()[2:] for ligne in source.splitlines()
               if ligne.strip().startswith("# eq:")]
    assert balises == [
        "eq:finances_publiques-plan-depense", "eq:finances_publiques-depense",
        "eq:finances_publiques-impot-menages", "eq:finances_publiques-couverture-interets",
        "eq:finances_publiques-impot-entreprises", "eq:finances_publiques-transferts",
        "eq:finances_publiques-interets-titres", "eq:finances_publiques-encaisse-visee",
        "eq:finances_publiques-besoin-emission",
        "eq:finances_publiques-souscription-banque-centrale",
        "eq:finances_publiques-souscription-banque", "eq:finances_publiques-assiette-impot",
        "eq:finances_publiques-parts-non-payees"]


def test_aucun_attribut_d_instance():
    """Bloc sans état caché : `__slots__` vide, aucun `__dict__`."""
    b = bloc.FinancesPubliques()
    assert not hasattr(b, "__dict__") and bloc.FinancesPubliques.__slots__ == ()
