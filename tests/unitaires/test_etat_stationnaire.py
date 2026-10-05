"""Tests du script d'état stationnaire sous forme fermée (issue #84).

Propriétés écrites avant l'essai (commentaires de #84 du 05/10/2026) : P1 à
P10 de la part de `macro`, propriétés 1 à 12 de la part de `monnaie`. Chaque
test énonce une propriété (égalité bit à bit, identité à 1e−12 près, signe),
pas une valeur à reproduire, sauf la comparaison aux valeurs publiées, dont
le seuil est la dernière décimale publiée (décision du 05/10/2026, point 2).

La superneutralité (critère 13 de la fiche 8) est un défaut connu du socle :
deux tests séparés, en échec attendu strict, avec renvoi à #80.
"""

import ast
import io
import math
import subprocess
import sys
from dataclasses import fields, replace
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[2]
SCRIPT = RACINE / "outils" / "etat_stationnaire.py"
TOL = 1e-12

# Écarts aux valeurs publiées (#84), publiés par le script et visés par le
# mainteneur le 05/10/2026 : ils ne sont ni masqués ni marqués en échec
# attendu. Le test vérifie que la liste est exacte : un écart nouveau, ou un
# écart résorbé, fait échouer la batterie. Les explications établies sont des
# propriétés testées (`test_explication_*`) ; les écarts de r̄_α, des
# allocations (α) et des racines parasites relèvent de #80. La liste se vide
# quand `docwriter` republie les valeurs visées (rang 7 de la branche).
ECARTS_PUBLIES = {
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, n_a = 4"),
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, n_a = 52"),
    ("sec:finances_publiques-stationnaire", "Y^HS/PIB à 2 %"),
    ("sec:finances_publiques-depense", "G/PB à 2 %"),
    ("sec:finances_publiques-depense", "G/PB à 10 %"),
    ("sec:finances_publiques-depense", "marge de E1 à 10 %"),
    ("sec:finances_publiques-emission", "borne de ν_G à 10 %"),
    ("sec:finances_publiques-emission", "marge J-ν à ν_G = 1,1, 0 %, %"),
    ("sec:banque_centrale-stationnaire", "sensibilité de θ_G, % de la production par point de r̄ (|dθ_G/dr̄|)"),
    ("sec:banque_centrale-stationnaire", "points de r̄ par point de PIB de dépense (|·|), environ"),
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 0 %, %"),
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 1 %, %"),
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 3 %, %"),
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 4 %, %"),
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 6 %, %"),
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 10 %, %"),
    ("sec:banque_centrale-conditions", "r̄_α(0) − r̄_α(10 %), point"),
    ("sec:banque_centrale-conditions", "écart maximal de r̄_α sur le profil, point"),
    ("sec:banque_centrale-conditions", "marche de cible de 2 à 3 %, point"),
    ("sec:finances_publiques-impots", "racine parasite à 0 %, %"),
    ("sec:finances_publiques-impots", "racine parasite à 2 %, %"),
    ("sec:finances_publiques-impots", "racine parasite à 10 %, %"),
    ("fiche 9 § 3.C", "(α) : C/PIB à 0 % moins à 2 %, point"),
    ("fiche 9 § 3.C", "(α) : C/PIB à 10 % moins à 2 %, point"),
    ("fiche 9 § 3.C", "(α) : max − min de C/PIB, point"),
}


@pytest.fixture(scope="module")
def base(stationnaire):
    return stationnaire.Parametres()


@pytest.fixture(scope="module")
def resultat(stationnaire, base):
    return stationnaire.calculer(base)


def points(stationnaire, base, nu=1.0):
    """Paramètres des neuf points π̄ × n_a de la grille, à ν_G donné."""
    return [
        replace(base, pi_cible=pi, n_a=na, nu_G=nu) for pi in stationnaire.POINTS_PI for na in stationnaire.POINTS_NA
    ]


def relatif(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


# --- Indépendance et déterminisme (P9 ; propriété 11) -----------------------------


def test_n_importe_que_la_bibliotheque_standard():
    arbre = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    modules = set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            modules.update(a.name.split(".")[0] for a in noeud.names)
        elif isinstance(noeud, ast.ImportFrom):
            modules.add((noeud.module or "").split(".")[0])
    assert modules <= {"__future__", "argparse", "dataclasses", "json", "math", "sys"}
    assert not modules & {"nations", "archive", "src"}


def test_deux_executions_identiques_a_l_octet(tmp_path):
    sorties = []
    for i in range(2):
        chemin_json = tmp_path / f"r{i}.json"
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--json", str(chemin_json)], capture_output=True, check=True
        )
        sorties.append((proc.stdout, chemin_json.read_bytes()))
    assert sorties[0] == sorties[1]
    assert len(sorties[0][0]) > 0


def test_valeur_retenue_par_defaut_troisieme_colonne(stationnaire, resultat):
    """ν_G retenu = 1,15 par défaut (décision du mainteneur du 05/10/2026) : troisième colonne de la grille."""
    assert stationnaire.NU_G_RETENU == 1.15
    assert {k[0] for k in resultat["grille"]} == {1.0, 1.15}
    tampon = io.StringIO()
    stationnaire.afficher(resultat, tampon)
    assert "ν_G = 1.15 (valeur retenue)" in tampon.getvalue()


def test_valeur_retenue_egale_a_un_refusee(stationnaire, base, capsys):
    """--nu-g-retenu 1.0 dupliquerait la colonne du point de référence : refus, code 1."""
    with pytest.raises(stationnaire.HorsDomaine, match="déjà le point de référence"):
        stationnaire.calculer(base, nu_g_retenu=1.0)
    assert stationnaire.main(["--nu-g-retenu", "1.0"]) == 1
    assert "Refus de domaine" in capsys.readouterr().err


def test_code_de_sortie_2_si_un_residu_depasse_le_seuil(stationnaire, monkeypatch, capsys):
    """Code 0 quand tous les résidus sont ≤ 1e−12 ; code 2, distinct du refus, si le seuil est abaissé sous eux."""
    assert stationnaire.main([]) == 0
    capsys.readouterr()
    monkeypatch.setattr(stationnaire, "TOL_IDENTITE", 0.0)
    assert stationnaire.main([]) == 2
    sortie = capsys.readouterr()
    assert "Résidu non tenu" in sortie.err and "Bilan :" in sortie.out


# --- Propriétés du bloc 8 (propriétés 1, 2 de `monnaie` ; P3 de `macro`) ----------


def test_glissement_stationnaire_egal_a_la_cible(stationnaire, base):
    for p in points(stationnaire, base):
        e = stationnaire.etat_stationnaire(p)
        o = stationnaire.ouverture(e, p)
        glissement = e["p"] / o["registre"][p.n_a - 1] - 1
        assert abs(glissement - p.pi_cible) <= 1e-15
        assert e["pi_e"] == p.pi_cible
        s = stationnaire.un_pas(o, p)
        assert abs(s["pi_e_1"] - e["pi_e"]) <= 1e-15  # BC3 au point fixe
        assert abs(s["r_hat_1"] - e["r_hat"]) <= 1e-15  # BC2 au point fixe
        assert s["pi_cible_1"] == p.pi_cible  # BC4


def test_taux_directeur_fisher_sur_la_cible(stationnaire, base):
    for p in points(stationnaire, base):
        e = stationnaire.etat_stationnaire(p)
        attendu = p.rbar + p.pi_cible + p.rbar * p.pi_cible  # expression indépendante
        assert abs(e["i_CB"] - attendu) <= 1e-15
        s = stationnaire.un_pas(stationnaire.ouverture(e, p), p)
        assert abs(s["i_CB"] - e["i_CB"]) <= 1e-15  # BC1 évaluée : i^règle = i_CB


def test_ecarts_et_ancre_superneutres(stationnaire, base):
    for p in points(stationnaire, base):
        e = stationnaire.etat_stationnaire(p)
        assert abs((e["i_L"] - e["i_CB"]) - p.varpi_L) <= 1e-15
        assert abs((e["i_CB"] - e["i_D"]) - p.varpi_D) <= 1e-15
        assert abs(e["E_Bk"] / e["L"] - p.vartheta) <= 1e-15 * p.vartheta


def test_couverture_nulle_et_reserves_nulles_en_lecture_e(stationnaire, base):
    for p in points(stationnaire, base):
        e = stationnaire.etat_stationnaire(p)
        assert e["T_cou"] == 0.0
        assert e["Res"] == 0.0 and e["Res"] * e["L_CB"] == 0.0
        assert e["L_CB"] == e["M_G"]


# --- Vitesses (P1 de `macro` ; propriété 4 de `monnaie`) ------------------------


@pytest.mark.parametrize("facteur", [0.5, 2.0])
def test_aucune_vitesse_n_entre_dans_l_etat_un_a_un(stationnaire, base, facteur):
    references = [stationnaire.etat_stationnaire(p) for p in points(stationnaire, base)]
    for nom in stationnaire.VITESSES + stationnaire.ELASTICITES_DE_NIVEAU:
        varie = replace(base, **{nom: getattr(base, nom) * facteur})
        stationnaire.controler_domaine(varie)  # la variante est dans son domaine
        for p, ref in zip(points(stationnaire, varie), references, strict=True):
            e = stationnaire.etat_stationnaire(p)
            assert e == ref, nom  # bit à bit
            assert stationnaire.valeurs(e, p) == stationnaire.valeurs(ref, replace(p, **{nom: getattr(base, nom)})), nom


@pytest.mark.parametrize("facteur", [0.5, 2.0])
def test_aucune_vitesse_n_entre_dans_les_sorties_toutes_ensemble(stationnaire, base, resultat, facteur):
    varie = replace(base, **{nom: getattr(base, nom) * facteur for nom in stationnaire.VITESSES})
    r = stationnaire.calculer(varie)
    for cle in ("grille", "niveaux", "propositions", "republication", "fermeture", "superneutralite", "cf"):
        assert r[cle] == resultat[cle], cle
    assert [l["script"] for l in r["publiees"]] == [l["script"] for l in resultat["publiees"]]
    # Les résidus des règles, qui lisent les vitesses, restent sous le seuil.
    assert max(max(c.values()) for c in r["controles"].values()) <= TOL


# --- Règles évaluées une fois, identités, matrices (P2, P3 ; propriété 7) -------


def test_regles_identites_matrices_et_routes_doubles(resultat):
    for point, c in resultat["controles"].items():
        for famille, residu in c.items():
            assert residu <= TOL, (point, famille, residu)


def test_matrices_detaillees_a_somme_nulle(stationnaire, base):
    p = replace(base, pi_cible=0.10, n_a=4)
    c = stationnaire.controles(stationnaire.etat_stationnaire(p), p)
    m = c["matrices"]
    assert set(m["flux"]) >= {
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11a",
        "11b",
        "11c",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19a-menages",
        "19a-banque",
        "19a-BC",
        "19b-menages",
        "19b-banque",
        "20",
        "21",
        "22",
    }
    assert max(m["lignes_bilans"].values()) <= TOL
    assert max(m["colonnes_bilans"].values()) <= TOL
    assert max(m["secteurs_flux"].values()) <= TOL
    assert max(m["valeurs_nettes"].values()) <= TOL
    assert max(c["routes_doubles"].values()) <= TOL


def test_une_route_fausse_est_detectee(stationnaire, base):
    """Non-tautologie : une ligne de flux faussée de 1e−9 × PIB fait échouer la colonne de son secteur."""
    p = base
    e = stationnaire.etat_stationnaire(p)
    s = stationnaire.un_pas(stationnaire.ouverture(e, p), p)
    s_faux = dict(s, Div_Bk=s["Div_Bk"] + 1e-9 * e["PIB"])
    m = stationnaire.matrices(e, s_faux, p)
    assert m["secteurs_flux"]["Bk"] > TOL and m["secteurs_flux"]["H"] > TOL


# --- Dépendances déclarées (P4, P5, P6) -----------------------------------------


def test_grandeurs_independantes_de_n_a_a_inflation_nulle(stationnaire, base):
    cles = ("U", "omega", "K_vol_sur_y", "L_sur_K", "richesse_HS", "tu", "rho_K")
    ref = None
    for na in stationnaire.POINTS_NA:
        p = replace(base, pi_cible=0.0, n_a=na)
        v = stationnaire.valeurs(stationnaire.etat_stationnaire(p), p)
        if ref is None:
            ref = v
        for k in cles:
            assert relatif(v[k], ref[k]) <= TOL, (na, k)


def test_ratios_ne_dependent_que_de_g(stationnaire, base):
    variante = replace(base, g_pr=1.02 / 1.005 - 1, g_N=0.005)
    stationnaire.controler_domaine(variante)
    for p, q in zip(points(stationnaire, base), points(stationnaire, variante), strict=True):
        v = stationnaire.valeurs(stationnaire.etat_stationnaire(p), p)
        w = stationnaire.valeurs(stationnaire.etat_stationnaire(q), q)
        differents = {k for k in v if abs(v[k] - w[k]) > TOL * max(abs(v[k]), 1.0)}
        assert differents == {"hausse_salaire_pas", "hausse_salaire_an"}


@pytest.mark.parametrize("champ, nominal", [("p_0", True), ("N_pa_0", False)])
def test_homogeneite_de_degre_un(stationnaire, base, champ, nominal):
    prix = ("p", "UC", "W")
    nominaux = (
        "WB",
        "IN",
        "dIN",
        "K",
        "I",
        "PIB",
        "L",
        "D_F",
        "V_F",
        "Div_F",
        "E_Bk",
        "D_H",
        "Y_HS",
        "T_H",
        "YD",
        "C",
        "G",
        "M_G",
        "B",
        "B_Bk",
        "L_CB",
        "Pi_CB",
        "Pi_Bk",
        "Em",
        "X",
        "PB",
    )
    volumes = ("y", "v", "IN_vol", "K_vol", "I_vol", "N", "N_pa", "y_pot")
    for p in points(stationnaire, base):
        q = replace(p, **{champ: 100 * getattr(p, champ)})
        e, f = stationnaire.etat_stationnaire(p), stationnaire.etat_stationnaire(q)
        for k in nominaux + (prix if nominal else volumes):
            assert relatif(f[k], 100 * e[k]) <= TOL, (champ, k)
        for k in volumes if nominal else prix:
            assert relatif(f[k], e[k]) <= TOL, (champ, k)
        v, w = stationnaire.valeurs(e, p), stationnaire.valeurs(f, q)
        for k in v:
            assert abs(v[k] - w[k]) <= TOL * max(abs(v[k]), 1.0), (champ, k)


# --- Neutralité de ν_G (P7 ; propriété 5 ; C59) ----------------------------------


def test_neutralite_de_nu_G(stationnaire, base):
    for p in points(stationnaire, base, nu=1.1):
        q = replace(p, nu_G=1.2)
        e, f = stationnaire.etat_stationnaire(p), stationnaire.etat_stationnaire(q)
        for k in ("theta_G", "YD", "Y_HS", "Div_F", "Div_Bk", "Pi_Bk", "D_c", "C", "G", "i_CB", "D_H"):
            assert relatif(f[k], e[k]) <= TOL, k
        nette_e = e["interets"] - e["Pi_CB"]
        nette_f = f["interets"] - f["Pi_CB"]
        assert relatif(nette_f, nette_e) <= TOL
        hausse = f["M_G"] - e["M_G"]
        S = f["B"] + f["M_G"]
        for k in ("B", "L_CB", "B_Bk"):
            assert abs((f[k] - e[k]) - hausse) <= TOL * S, k


def test_multiplicateur_du_refinancement(stationnaire, base):
    for p in points(stationnaire, base):
        e1 = stationnaire.etat_stationnaire(p)
        for nu in (1.1, 1.15):
            e = stationnaire.etat_stationnaire(replace(p, nu_G=nu))
            a = e["a"]
            assert relatif(e["L_CB"] / e1["L_CB"], nu * (1 - a) / (1 - nu * a)) <= 1e-9


def test_nu_G_min_tient_la_marge_exacte(stationnaire, base):
    """ν_G,min exact donne une marge J-ν nulle ; ν_G minimal pour 0,03 donne 0,03."""
    for p in points(stationnaire, base):
        v = stationnaire.valeurs(stationnaire.etat_stationnaire(p), p)
        for cle, marge in (("nu_G_min", 0.0), ("nu_G_J", stationnaire.MARGE_J_NU)):
            q = replace(p, nu_G=v[cle])
            w = stationnaire.valeurs(stationnaire.etat_stationnaire(q, controler=False), q)
            assert abs(w["marge_J_nu"] - marge) <= TOL


# --- Fermeture (P8) ------------------------------------------------------------


def test_fermeture_explicite_et_derivee_declaree(stationnaire, base):
    f = stationnaire.sensibilite_fermeture(base)
    assert math.isfinite(f["dtheta_G_dr"])
    assert f["erreur"] <= 1e-6 * abs(f["dtheta_G_dr"])


# --- Contrôles de domaine (propriété 10) ----------------------------------------


@pytest.mark.parametrize(
    "champ, valeur",
    [
        ("lambda_v", 0.0),
        ("lambda_v", 13.0),
        ("lambda_H", 13.0),
        ("lambda_e", 0.0),
        ("beta", 0.0),
        ("psi_xi", -0.1),
        ("nu_H", 3.0),
        ("tau_H", 1.0),
        ("tau_F", -0.1),
        ("theta_Tr", -0.1),
        ("phi", 0.5),
        ("nu_G", 0.99),
        ("nu_G", 1.0 - 1e-12),
        ("rbar", -0.05),
        ("delta", 0.0),
        ("lv", 1.0),
        ("nu_F", 0.0),
        ("tu_bar", 0.0),
        ("zeta", -1.0),
        ("eta_r", -1.0),
        ("vartheta", 0.0),
        ("a_pi", 0.0),
        ("a_pi", 1.5),
        ("a_I", 0.0),
        ("theta_CB", 1.1),
        ("varsigma_L", 0.1),
        ("varsigma_B", 1.5),
        ("pi_cible", -1.0),
        ("U_eq", 1.0),
        ("p_0", 0.0),
    ],
)
def test_refus_explicite_hors_domaine(stationnaire, base, champ, valeur):
    with pytest.raises(stationnaire.HorsDomaine):
        stationnaire.controler_domaine(replace(base, **{champ: valeur}))


def test_nu_G_egal_a_un_admis_et_declare(stationnaire, base):
    assert any("ν_G = 1" in d for d in stationnaire.controler_domaine(base))
    assert stationnaire.controler_domaine(replace(base, nu_G=1.1)) == []


def test_refus_de_la_condition_d_existence_a_ecarts_nuls(stationnaire, base):
    p = replace(base, varpi_L=0.0, varpi_D=0.0)
    with pytest.raises(stationnaire.HorsDomaine, match="existence"):
        stationnaire.etat_stationnaire(p)
    e = stationnaire.etat_stationnaire(p, controler=False)
    assert e["existence_Bk"] < 0


def test_refus_a_lv_0_6(stationnaire, base):
    """lv* = 0,6 : plafond de E1 à marge négative et dette brute négative sur une partie de la grille ; refus."""
    refus = 0
    for p in points(stationnaire, replace(base, lv=0.6)):
        e = stationnaire.etat_stationnaire(p, controler=False)
        hors = e["marge_E1_montant"] <= 0 or e["B"] < 0 or e["B_Bk"] < 0
        if hors:
            refus += 1
            with pytest.raises(stationnaire.HorsDomaine):
                stationnaire.etat_stationnaire(p)
        else:
            stationnaire.etat_stationnaire(p)
    assert refus == 6
    with pytest.raises(stationnaire.HorsDomaine):
        stationnaire.calculer(replace(base, lv=0.6))
    # Les deux conditions sont violées séparément sur la grille (π̄ = 0, n_a = 12 : les deux à la fois).
    e = stationnaire.etat_stationnaire(replace(base, lv=0.6, pi_cible=0.0), controler=False)
    assert e["marge_E1_montant"] < 0 and e["B"] < 0 and e["B_Bk"] < 0


def test_refus_de_theta_G_nul(stationnaire, base):
    """Domaine ouvert A = θ_G > 0 strict : θ_G ≤ 0 est refusé (ici par un transfert qui absorbe la dépense)."""
    p = replace(base, theta_Tr=0.5)
    e = stationnaire.etat_stationnaire(p, controler=False)
    assert e["theta_G"] <= 0
    with pytest.raises(stationnaire.HorsDomaine, match="θ_G"):
        stationnaire.etat_stationnaire(p)


def test_em_negatif_n_est_pas_un_refus(stationnaire, base):
    """Em = γ̄ B a le signe de γ̄ : à γ̄ < 0 (rachat net), l'état se résout sans refus."""
    p = replace(base, lv=0.1, g_pr=0.0, pi_cible=-0.01)
    stationnaire.controler_domaine(p)
    e = stationnaire.etat_stationnaire(p)
    assert e["gam"] < 0 and e["Em"] < 0
    assert relatif(e["Em"], e["gam"] * e["B"]) <= TOL


@pytest.mark.parametrize("champ, valeur", [("lv", 0.0), ("tau_H", 0.0)])
def test_bords_fermes_du_domaine_sans_exception(stationnaire, base, champ, valeur):
    """lv* = 0 et τ_H = 0 (domaine fermé) : calcul complet sans exception ; rapports sans objet publiés tels."""
    variante = replace(base, **{champ: valeur})
    r = stationnaire.calculer(variante)
    assert stationnaire.plus_grand_residu(r) <= TOL
    tampon = io.StringIO()
    stationnaire.afficher(r, tampon)
    assert "sans objet" in tampon.getvalue()
    for v in r["grille"].values():
        if champ == "lv":
            assert math.isnan(v["roe"]) and math.isnan(v["existence_Bk"]) and math.isnan(v["E_sur_L"])
        else:
            assert math.isnan(v["D_H_sur_T_H"])
    if champ == "lv":
        e = stationnaire.etat_stationnaire(variante)
        assert e["L"] == 0.0 and e["E_Bk"] == 0.0 and e["existence_Bk_montant"] > 0


def test_existence_en_montants_egale_la_marge_publiee(stationnaire, base):
    """n_a Π^Bk − n_a γ̄ E^Bk rapporté à L redonne la forme ϑ i_CB + ϖ_L + ϖ_D D/L − ϑ n_a γ̄."""
    for p in points(stationnaire, base):
        e = stationnaire.etat_stationnaire(p)
        forme = (p.vartheta * e["i_CB"] + p.varpi_L + p.varpi_D * (e["D_H"] + e["D_F"]) / e["L"]
                 - p.vartheta * p.n_a * e["gam"])
        assert abs(e["existence_Bk"] - forme) <= TOL * max(abs(forme), p.varpi_L)


def test_refus_des_poles_D1_et_D2(stationnaire, base):
    with pytest.raises(stationnaire.HorsDomaine, match="D2"):
        stationnaire.etat_stationnaire(replace(base, nu_G=1000.0))
    with pytest.raises(stationnaire.HorsDomaine, match="D1"):
        stationnaire.etat_stationnaire(replace(base, rbar=1.5))


def test_q1_publie_comme_constat_a_n_a_4(stationnaire, resultat):
    """D_F en fin de phase 4 : négatif à n_a = 4 (constat), positif à n_a = 12 et 52 (décision du 05/10/2026, pt 4).

    q1 est un constat publié, pas un résidu : il ne change pas le code de sortie.
    """
    for (_nu, pi, na), v in resultat["grille"].items():
        assert (v["caisse_DF4"] < 0) == (na == 4), (pi, na)
        assert (v["nu_F_min"] > resultat["parametres"].nu_F) == (na == 4)
    tampon = io.StringIO()
    stationnaire.afficher(resultat, tampon)
    colonnes_nu = len({k[0] for k in resultat["grille"]})
    assert tampon.getvalue().count("q1 : D_F en fin de phase 4 négatif") == 3 * colonnes_nu


# --- Valeurs publiées (propriété 9 ; critère J1) --------------------------------


# --- Explications établies des écarts publiés (#84), en propriétés --------------


def test_explication_dette_consolidee_sigma_en_pas(stationnaire, base):
    """La maquette tenait σ = 1,4 pas de ventes (σ = 1,4/n_a an) : elle redonne 0,25237 et 0,25844."""
    for na, publie in ((4, "0,25237"), (52, "0,25844")):
        p = replace(base, n_a=na, sigma=1.4 / na)
        v = stationnaire.valeurs(stationnaire.etat_stationnaire(p), p)
        assert stationnaire.comparer(publie, v["dette_consolidee"])[2], (na, v["dette_consolidee"])


def test_explication_Y_HS_par_T_H_arrondi(stationnaire, base):
    """Y^HS/PIB publié à 2 % = T_H/PIB arrondi au centième de point ÷ τ_H : 21,68 %/0,25 = 0,8672."""
    v = stationnaire.valeurs(stationnaire.etat_stationnaire(base), base)
    assert stationnaire.comparer("0,8672", round(v["T_H_sur_PIB"], 2) / 100 / base.tau_H)[2]
    assert not stationnaire.comparer("0,8672", v["Y_HS"])[2]


def test_explication_marge_J_nu_sur_G_PB_a_nu_G_un(stationnaire, base):
    """« 0,37 % » à ν_G = 1,1, π̄ = 0 : marge J-ν calculée sur G/PB à ν_G = 1, non à ν_G = 1,1."""
    p1 = replace(base, pi_cible=0.0)
    v1 = stationnaire.valeurs(stationnaire.etat_stationnaire(p1), p1)
    marge = 1 - stationnaire.HAUSSE_J_NU * v1["Gamma"] * v1["G_sur_PB"] / 1.1
    assert stationnaire.comparer("0,37", 100 * marge)[2]
    p11 = replace(p1, nu_G=1.1)
    v11 = stationnaire.valeurs(stationnaire.etat_stationnaire(p11), p11)
    assert not stationnaire.comparer("0,37", 100 * v11["marge_J_nu"])[2]


def test_seuil_derniere_decimale(stationnaire):
    assert stationnaire.decimales("0,25674") == 5
    assert stationnaire.comparer("0,25674", 0.256744999)[2]
    assert not stationnaire.comparer("0,25674", 0.2567451)[2]
    assert stationnaire.comparer("-0,000947", -0.0009474)[2]
    assert not stationnaire.comparer("1,536", math.nan)[2]


def test_valeurs_publiees_egales_sauf_ecarts_publies(resultat):
    lignes = resultat["publiees"]
    assert {l["categorie"] for l in lignes} == {"A", "S", "B-1", "C", "D"}
    assert all(l["verdict"] == "égal" for l in lignes if l["categorie"] == "S")
    ecarts = {(l["section"], l["grandeur"]) for l in lignes if l["verdict"] != "égal"}
    assert ecarts == ECARTS_PUBLIES
    for l in lignes:
        if (l["section"], l["grandeur"]) not in ECARTS_PUBLIES:
            assert abs(l["ecart"]) <= l["seuil"], l


def test_formes_de_83_republiees_a_un_milliardieme(stationnaire, base):
    """Formes fermées du bloc 7 appelées sur l'état résolu contre l'état résolu lui-même (seuil de #83)."""
    calc = stationnaire.Calculs(base)
    for pi in stationnaire.POINTS_PI:
        e = calc.etat(pi)
        b = calc.banque(pi=pi)
        A = 12 * e["PIB"]
        assert relatif(b["b_Bk"], e["B_Bk"] / A) <= 1e-9
        assert relatif(b["refinancement"], e["L_CB"] / A) <= 1e-9
        assert relatif(b["c"], e["D_c"] / A) <= 1e-9
        assert relatif(b["Pi_Bk"] / 100, e["Pi_Bk"] / e["PIB"]) <= 1e-9


# --- Mesure de #80 (propriété 12 ; P10) -----------------------------------------


def test_racine_unique_dans_le_domaine_et_residu(resultat):
    sn = resultat["superneutralite"]
    for mesures in [sn["alpha"]] + list(sn["alpha_n_a"].values()):
        for a in mesures.values():
            assert sum(1 for r in a["racines"] if -0.05 < r <= 1.0) == 1
            assert a["poles"] == []
            assert abs(a["F"]) <= 1e-12


def test_racines_d_une_F_adverse_detectees_et_refusees(stationnaire):
    """F à deux racines dans le domaine et un pôle à changement de signe : les trois sont trouvés, puis refus."""
    r1, r2, pole = 0.0123456789, 0.0456789123, 0.0301234567

    def F(r):
        return (r - r1) * (r - r2) / (r - pole)

    res = stationnaire.racines_balayage(F)
    trouvees = [x["r"] for x in res["racines"]]
    assert len(trouvees) == 2
    assert abs(trouvees[0] - r1) <= 1e-13 and abs(trouvees[1] - r2) <= 1e-13
    assert len(res["poles"]) == 1 and abs(res["poles"][0] - pole) <= 1e-13
    with pytest.raises(stationnaire.HorsDomaine, match="2 racine"):
        stationnaire.racine_unique(res, "F adverse")
    # Une seule racine mais un pôle : refus aussi.
    res_pole = stationnaire.racines_balayage(lambda r: (r - r1) / (r - pole))
    assert len(res_pole["dans_domaine"]) == 1 and len(res_pole["poles"]) == 1
    with pytest.raises(stationnaire.HorsDomaine):
        stationnaire.racine_unique(res_pole, "F adverse à pôle")
    # Aucune racine : refus.
    with pytest.raises(stationnaire.HorsDomaine, match="0 racine"):
        stationnaire.racine_unique(stationnaire.racines_balayage(lambda r: 1.0 + r * r), "F sans racine")


@pytest.mark.parametrize("n_a", [4, 12, 52])
def test_aller_retour_de_la_lecture_alpha(stationnaire, base, n_a):
    a = stationnaire.mesure_alpha(base, 0.02, n_a)
    assert abs(a["r_alpha"] - 0.01) <= 1e-10


def test_r_alpha_independant_de_nu_G(stationnaire, base):
    for pi in stationnaire.POINTS_PI:
        a = stationnaire.mesure_alpha(base, pi, 12)
        b = stationnaire.mesure_alpha(replace(base, nu_G=1.15), pi, 12)
        assert abs(a["r_alpha"] - b["r_alpha"]) <= 1e-10


@pytest.mark.xfail(
    strict=True,
    reason="#80 : critère 13 de la fiche 8, défaut connu du socle (M32) ; C30, conversion linéaire, écarts nominaux",
)
def test_superneutralite_taux_neutre(resultat):
    assert resultat["superneutralite"]["delta_r_alpha"] <= 0.001


@pytest.mark.xfail(
    strict=True,
    reason="#80 : critère 13 de la fiche 8, défaut connu du socle (M32) ; C30, conversion linéaire, écarts nominaux",
)
def test_superneutralite_allocations(stationnaire, resultat):
    """Liste L2 (critère 13 (a) de la fiche 8) : C/Y_o, ti, tu sous le seuil de 0,1 point."""
    for allocation in stationnaire.ALLOCATIONS_VERDICT:
        assert resultat["superneutralite"]["allocations"][allocation] <= 0.001, allocation


def test_liste_L2_et_invariance_exacte(stationnaire, resultat):
    """Liste L2 déclarée ; V_H/(n_a YD^HS) invariante à 1e−12 relatif (= ν_H) sur le profil de (α)."""
    assert stationnaire.ALLOCATIONS_VERDICT == ("C/Y_o", "ti", "tu")
    assert stationnaire.ALLOCATIONS_INVARIANTES == ("V_H/(n_a YD^HS)",)
    assert {"K^vol/(n_a y)", "C/PIB", "G/PIB", "I/PIB", "ΔIN/PIB", "I^vol/y"} <= set(stationnaire.ALLOCATIONS_MESUREES)
    sn = resultat["superneutralite"]
    assert sn["invariance"]["V_H/(n_a YD^HS)"] <= 1e-12
    for a in sn["alpha"].values():
        assert relatif(a["allocations"]["V_H/(n_a YD^HS)"], resultat["parametres"].nu_H) <= 1e-12
        al = a["allocations"]
        # Décomposition de ΔIN et versions sur p v : identités.
        assert abs(al["ΔIN/PIB volume"] + al["ΔIN/PIB prix"] - al["ΔIN/PIB"]) <= 1e-15
        assert abs(al["C/(p v)"] + al["G/(p v)"] + al["I/(p v)"] - 1) <= 1e-15
    idents = {g.ident for g in stationnaire.GRANDEURS_ALPHA}
    assert set(stationnaire.ALLOCATIONS_VERDICT + stationnaire.ALLOCATIONS_INVARIANTES
               + stationnaire.ALLOCATIONS_MESUREES) | {"r_alpha"} == idents


# --- Propriétés de (α) demandées par `macro` et `monnaie` (écrites avant l'essai) ---


ALLOCATIONS_ZETA = ("C/PIB", "G/PIB", "I/PIB", "tu", "K^vol/(n_a y)")


def test_alpha_allocations_independantes_de_zeta_et_eta_r(stationnaire, base):
    """`macro` : ζ ∈ {2 ; 8}, η_r ∈ {1 ; 4} : allocations identiques à 1e−12 relatif ; ζ Δϱ invariant."""
    for pi in (0.0, 0.10):
        ref = stationnaire.mesure_alpha(base, pi, 12)
        for nom, valeurs_ in (("zeta", (2.0, 8.0)), ("eta_r", (1.0, 4.0))):
            for val in valeurs_:
                a = stationnaire.mesure_alpha(replace(base, **{nom: val}), pi, 12)
                for q in ALLOCATIONS_ZETA:
                    assert relatif(a["allocations"][q], ref["allocations"][q]) <= 1e-12, (pi, nom, val, q)
                if nom == "zeta":
                    assert relatif(val * a["d_rho"], base.zeta * ref["d_rho"]) <= 1e-9, (pi, val)


def test_alpha_r_alpha_varie_avec_zeta(stationnaire, base):
    """`macro` : r̄_α − 1 % varie avec ζ hors de π* = 2 % (le niveau ζ Δϱ est fixé, pas Δϱ)."""
    for pi in (0.0, 0.10):
        r = [stationnaire.mesure_alpha(replace(base, zeta=z), pi, 12)["r_alpha"] for z in (2.0, 8.0)]
        assert abs(r[0] - r[1]) > 1e-6, pi


def test_alpha_eta_r_ne_touche_que_ti(stationnaire, base):
    """`macro` et `monnaie` : η_r sans effet bit à bit sur r̄_α ; parmi les allocations, seul ti change."""
    for pi in (0.0, 0.10):
        ref = stationnaire.mesure_alpha(base, pi, 12)
        for val in (1.0, 4.0):
            a = stationnaire.mesure_alpha(replace(base, eta_r=val), pi, 12)
            assert a["r_alpha"] == ref["r_alpha"]
            changent = {q for q in a["allocations"] if a["allocations"][q] != ref["allocations"][q]}
            assert changent == {"ti"}, changent


def test_alpha_allocations_independantes_de_zeta_seuil_monnaie(stationnaire, base):
    """`monnaie` : allocations (α) de ses essais (C/PIB, G/PIB, I/PIB, ΔIN/PIB) indépendantes de ζ à 1e−10.

    Mesure publiée à côté (non une propriété) : C/Y_o, ti et T^cou/PIB dépendent de ζ, car r̄_α en dépend.
    """
    for pi in (0.0, 0.10):
        a = stationnaire.mesure_alpha(replace(base, zeta=2.0), pi, 12)
        b = stationnaire.mesure_alpha(replace(base, zeta=8.0), pi, 12)
        for q in ("C/PIB", "G/PIB", "I/PIB", "ΔIN/PIB"):
            assert abs(a["allocations"][q] - b["allocations"][q]) <= 1e-10, (pi, q)


def test_alpha_egale_la_forme_fermee(stationnaire, base):
    """`monnaie` : r̄_α = ϱ̄_L − ϖ_L/(1 + π*) − (1/ζ) ln[(θ_G* − a)/b], θ_G(r̄) = a + b e^{−ζ Δϱ(r̄)}, à 1e−12."""
    e0 = stationnaire.etat_stationnaire(replace(base, pi_cible=0.02, rbar=0.01))
    theta_cible, rho_bar = e0["theta_G"], e0["rho_L"]
    for pi in stationnaire.PROFIL_PI:
        point = replace(base, pi_cible=pi)

        def theta(r, point=point):
            return stationnaire.etat_stationnaire(point, r_neutre=r, rho_bar_L=rho_bar, controler=False)["theta_G"]

        def u(r, pi=pi):
            return math.exp(-base.zeta * (r + base.varpi_L / (1 + pi) - rho_bar))

        r1, r2 = 0.0, 0.03
        b = (theta(r1) - theta(r2)) / (u(r1) - u(r2))
        a = theta(r1) - b * u(r1)
        ferme = rho_bar - base.varpi_L / (1 + pi) - math.log((theta_cible - a) / b) / base.zeta
        assert abs(stationnaire.mesure_alpha(base, pi, 12)["r_alpha"] - ferme) <= 1e-12, pi


def test_F_independante_de_r_sous_norme_recalculee(stationnaire, base):
    """`monnaie` : sous la lecture A et la norme ϱ̄_L recalculée, θ_G ne dépend pas de r̄ (à 1e−15) : T^cou
    neutralise le canal rentier ; c'est pourquoi (α) fixe la norme (décision du 05/10/2026, #80)."""
    for pi in stationnaire.POINTS_PI:
        p = replace(base, pi_cible=pi)
        thetas = [stationnaire.etat_stationnaire(p, r_neutre=r, controler=False)["theta_G"]
                  for r in (-0.04, 0.0, 0.01, 0.05, 0.20)]
        assert max(thetas) - min(thetas) <= 1e-15, (pi, max(thetas) - min(thetas))


# --- Déclarations ----------------------------------------------------------------


def test_chaque_parametre_est_declare(stationnaire, base):
    noms = {f.name for f in fields(base)}
    assert noms == set(stationnaire.DECLARATIONS)
    for unite, source, equation in stationnaire.DECLARATIONS.values():
        assert unite and source and equation


def test_chaque_grandeur_publiee_porte_sa_definition(stationnaire, resultat):
    idents = [g.ident for g in stationnaire.GRANDEURS]
    assert len(idents) == len(set(idents))
    for g in stationnaire.GRANDEURS:
        assert g.definition and g.unite and g.denominateur and g.fenetre and g.source
    for v in resultat["grille"].values():
        assert set(idents) <= set(v)
