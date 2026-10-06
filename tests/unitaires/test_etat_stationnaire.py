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
import re
import subprocess
import sys
from dataclasses import fields, replace
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[2]
SCRIPT = RACINE / "outils" / "etat_stationnaire.py"
TOL = 1e-12

# Écarts historiques aux valeurs publiées avant le visa du 05/10/2026 (#84,
# commit 9c8bdbd), publiés par le script et visés par le mainteneur : la
# spécification (commit 8b9fa94) et les annotations des fiches 8 et 9 les ont
# republiés. Le script garde l'ancien verdict (`table_historique`) ; le test
# vérifie que la liste est exacte et que chaque ancienne valeur est celle
# figée ici en littéral (constat m3 du rang 8 : une ancienne valeur publiée ne
# se modifie pas sans échec). Les explications établies sont des propriétés
# testées (`test_explication_*`) ; les écarts de r̄_α, des allocations (α) et
# des racines parasites relèvent de #80. Les quatre dernières (fiche 9, n_a = 4
# et 52 à 0 et 10 %) sont visées après la revue finale (décision du mainteneur
# du 05/10/2026, point B).
ANCIENNES_PUBLIEES = {
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, n_a = 4"): "0,25237",
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, n_a = 52"): "0,25844",
    ("sec:finances_publiques-stationnaire", "Y^HS/PIB à 2 %"): "0,8672",
    ("sec:finances_publiques-depense", "G/PB à 2 %"): "0,96343",
    ("sec:finances_publiques-depense", "G/PB à 10 %"): "0,78639",
    ("sec:finances_publiques-depense", "marge de E1 à 10 %"): "0,2060",
    ("sec:finances_publiques-emission", "borne de ν_G à 10 %"): "0,8734",
    ("sec:finances_publiques-emission ; tab:calibration", "marge J-ν à ν_G = 1,1, 0 %, %"): "0,37",
    ("sec:banque_centrale-stationnaire", "sensibilité de θ_G, % de la production par point de r̄ (|dθ_G/dr̄|)"):
        "0,026",
    ("sec:banque_centrale-stationnaire", "points de r̄ par point de PIB de dépense (|·|), environ"): "38",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 0 %, %"): "1,536",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 1 %, %"): "1,203",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 3 %, %"): "0,878",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 4 %, %"): "0,813",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 6 %, %"): "0,799",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 10 %, %"): "1,075",
    ("sec:banque_centrale-conditions", "r̄_α(0) − r̄_α(10 %), point"): "0,461",
    ("sec:banque_centrale-conditions", "écart maximal de r̄_α sur le profil, point"): "0,74",
    ("sec:banque_centrale-conditions", "marche de cible de 2 à 3 %, point"): "-0,12",
    ("sec:finances_publiques-impots", "racine parasite à 0 %, %"): "-20,63",
    ("sec:finances_publiques-impots", "racine parasite à 2 %, %"): "-26,65",
    ("sec:finances_publiques-impots", "racine parasite à 10 %, %"): "-40,49",
    ("fiche 9 § 3.C", "(α) : C/PIB à 0 % moins à 2 %, point"): "0,435",
    ("fiche 9 § 3.C", "(α) : C/PIB à 10 % moins à 2 %, point"): "-0,473",
    ("fiche 9 § 3.C", "(α) : max − min de C/PIB, point"): "0,908",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 0 %, n_a = 4"): "0,09466",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 10 %, n_a = 4"): "0,49978",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 0 %, n_a = 52"): "0,10045",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 10 %, n_a = 52"): "0,51438",
}
ECARTS_PUBLIES = set(ANCIENNES_PUBLIEES)


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


VOLUMES_PAR_TETE = ("y", "v", "IN_vol", "K_vol", "I_vol", "y_pot")


@pytest.mark.parametrize(
    "champ, proportionnels, invariants",
    [
        ("p_0", ("p", "UC", "W"), VOLUMES_PAR_TETE + ("N", "N_pa")),
        ("N_pa_0", VOLUMES_PAR_TETE + ("N", "N_pa"), ("p", "UC", "W")),
        # pr_0 : volumes et salaire par tête proportionnels, prix et effectifs invariants (réponse (a) de `macro`).
        ("pr_0", VOLUMES_PAR_TETE + ("W", "pr"), ("p", "UC", "N", "N_pa")),
    ],
)
def test_homogeneite_de_degre_un(stationnaire, base, champ, proportionnels, invariants):
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
    for p in points(stationnaire, base):
        q = replace(p, **{champ: 100 * getattr(p, champ)})
        e, f = stationnaire.etat_stationnaire(p), stationnaire.etat_stationnaire(q)
        for k in nominaux + proportionnels:
            assert relatif(f[k], 100 * e[k]) <= TOL, (champ, k)
        for k in invariants:
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
    """lv* = 0,6, ν_G = 1 : dette brute négative sur une partie de la grille, refusée ; le plafond de E1 seul n'est
    pas un refus au point de référence (décision de `macro`, option (b)), mais il l'est à ν_G > 1."""
    refus = e1_seul = 0
    for p in points(stationnaire, replace(base, lv=0.6)):
        e = stationnaire.etat_stationnaire(p, controler=False)
        if e["B"] < 0 or e["B_Bk"] < 0:
            refus += 1
            with pytest.raises(stationnaire.HorsDomaine, match="B ="):
                stationnaire.etat_stationnaire(p)
        else:
            e1_seul += e["marge_E1_montant"] <= 0
            assert stationnaire.etat_stationnaire(p)["marge_E1_montant"] == e["marge_E1_montant"]
    assert (refus, e1_seul) == (5, 1)
    with pytest.raises(stationnaire.HorsDomaine):
        stationnaire.calculer(replace(base, lv=0.6))
    # Les deux conditions sont violées séparément sur la grille (π̄ = 0, n_a = 12 : les deux à la fois).
    e = stationnaire.etat_stationnaire(replace(base, lv=0.6, pi_cible=0.0), controler=False)
    assert e["marge_E1_montant"] < 0 and e["B"] < 0 and e["B_Bk"] < 0


def test_dividende_nul_admis_a_la_borne(stationnaire, base):
    """Réponse (b) de `macro` : Div_F ≥ 0 est une inégalité large (plancher de F3 atteint, non contraignant).
    Par bissection sur τ_F (π̄ = 2 %, n_a = 12), le dernier flottant où Div_F ≥ 0 donne 0 ≤ Div_F ≤ 10⁻¹⁵ p v
    (propriété indépendante de l'arrondi de la plateforme) : l'état y est admis ; au flottant suivant, Div_F < 0
    est refusé."""
    def etat(tau_F):
        return stationnaire.etat_stationnaire(replace(base, tau_F=tau_F), controler=False)

    bas, haut = base.tau_F, 0.9
    assert etat(bas)["Div_F"] > 0 > etat(haut)["Div_F"]
    while (milieu := (bas + haut) / 2) not in (bas, haut):
        if etat(milieu)["Div_F"] >= 0:
            bas = milieu
        else:
            haut = milieu
    e = etat(bas)
    assert 0 <= e["Div_F"] <= 1e-15 * e["p"] * e["v"] and etat(haut)["Div_F"] < 0
    stationnaire.controler_domaine(replace(base, tau_F=bas))
    stationnaire.etat_stationnaire(replace(base, tau_F=bas))  # admis
    with pytest.raises(stationnaire.HorsDomaine, match="Div_F"):
        stationnaire.etat_stationnaire(replace(base, tau_F=haut))


def test_dividende_exactement_nul_admis_par_le_controle(stationnaire, base):
    """Égalité exacte, sans dépendre de l'arrondi : un état où Div_F est posé à 0,0 est admis par `controler_etat`
    (une inégalité stricte Div_F > 0 le refuserait) ; Div_F = −5·10⁻³²⁴ est refusé."""
    e = stationnaire.etat_stationnaire(base, controler=False)
    stationnaire.controler_etat(e | {"Div_F": 0.0}, base)
    with pytest.raises(stationnaire.HorsDomaine, match="Div_F"):
        stationnaire.controler_etat(e | {"Div_F": -5e-324}, base)


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


# --- Colonne de référence ν_G = 1 hors domaine (décision de `macro`, option (b)) ---------


@pytest.mark.parametrize("pi, n_a, admis", [
    (0.0, 4, False), (0.0, 12, False), (0.0, 52, False), (0.02, 4, True), (0.02, 12, False), (0.02, 52, False),
])
def test_lv_0_6_a_nu_G_1_15_refus_sur_la_dette_brute(stationnaire, base, pi, n_a, admis):
    """`macro` : lv* = 0,6, ν_G = 1,15 : refus sur B < 0 là où la marge de E1 est positive (le refus ne vient pas
    de E1) ; témoin admis à π̄ = 2 %, n_a = 4 (B/(n_a PIB) ≈ +0,042)."""
    p = replace(base, lv=0.6, nu_G=1.15, pi_cible=pi, n_a=n_a)
    e = stationnaire.etat_stationnaire(p, controler=False)
    assert 1 - e["Gam"] * (e["G"] / e["PB"]) / p.nu_G > 0 and e["marge_E1_montant"] > 0
    if admis:
        assert 0.04 < stationnaire.etat_stationnaire(p)["B"] / (n_a * e["PIB"]) < 0.045
    else:
        assert e["B"] < 0
        with pytest.raises(stationnaire.HorsDomaine, match="B = .*dette brute"):
            stationnaire.etat_stationnaire(p)


def test_lv_0_6_calculer_refuse_sur_une_colonne_nu_G_1_15(stationnaire, base):
    """`macro` : la grille complète à lv* = 0,6 est refusée, motif B < 0, sur la colonne retenue ν_G = 1,15
    (calculée avant la colonne de référence)."""
    with pytest.raises(stationnaire.HorsDomaine, match=r"colonne ν_G = 1\.15, .* : B = .*dette brute"):
        stationnaire.calculer(replace(base, lv=0.6), nu_g_retenu=1.15)


def test_plafond_de_E1_refuse_a_nu_G_superieur_a_un(stationnaire, base):
    """Le plafond de E1 reste un refus sur les colonnes ν_G > 1 (lv* = 0,45, π̄ = 0, n_a = 4, ν_G = 1,001)."""
    p = replace(base, lv=0.45, pi_cible=0.0, n_a=4, nu_G=1.001)
    assert stationnaire.etat_stationnaire(p, controler=False)["marge_E1_montant"] <= 0
    with pytest.raises(stationnaire.HorsDomaine, match="plafond de E1"):
        stationnaire.etat_stationnaire(p)


def test_reference_hors_domaine_publiee_comme_constat(stationnaire, base, monkeypatch, capsys):
    """`macro` : lv* = 0,45 : plafond de E1 actif à ν_G = 1 en (0, 4) et (0, 12), toutes les colonnes ν_G > 1
    admissibles ; code 0, constat publié, aucune valeur d'état ni résidu pour ces points de référence."""
    variante = replace(base, lv=0.45)
    hors = {(0.0, 4), (0.0, 12)}
    for p in points(stationnaire, variante):
        e = stationnaire.etat_stationnaire(p)  # aucun refus au point de référence
        assert (e["marge_E1_montant"] <= 0) == ((p.pi_cible, p.n_a) in hors)
    for nu in sorted(set(stationnaire.NU_G_PROPOSES) | {stationnaire.NU_G_RETENU}):
        for p in points(stationnaire, variante, nu):
            assert stationnaire.etat_stationnaire(p)["marge_E1_montant"] > 0
    r = stationnaire.calculer(variante)
    assert set(r["reference_hors_domaine"]) == hors
    assert all(m < 0 for m in r["reference_hors_domaine"].values())
    for pi, na in hors:
        assert (1.0, pi, na) not in r["grille"] and (1.0, pi, na) not in r["controles"]
        assert (1.0, pi, na) not in r["niveaux"]
        assert (1.15, pi, na) in r["grille"] and (1.15, pi, na) in r["niveaux"]
    assert (1.0, 0.0) not in r["republication"] and (1.15, 0.0) in r["republication"]
    assert stationnaire.plus_grand_residu(r) <= TOL
    non_publiees = [l for l in r["publiees"] if l["verdict"] == "non publiée"]
    assert non_publiees and all(math.isnan(l["script"]) for l in non_publiees)
    tampon = io.StringIO()
    stationnaire.afficher(r, tampon)
    texte = tampon.getvalue()
    assert "point de référence hors domaine : plafond de E1 actif (marge = -0.00202929), état non publié" in texte
    assert f"{len(non_publiees)} non publiées (point de référence hors domaine" in texte
    monkeypatch.setattr(stationnaire, "Parametres", lambda: variante)
    assert stationnaire.main([]) == 0
    assert "état non publié" in capsys.readouterr().out


def test_etat_initial_publie_a_nu_G_retenu_puis_a_la_reference(stationnaire, resultat):
    """R1 et R3 de `macro` (rang 6) : l'état initial résolu est publié à ν_G retenu, l'état que lira `scenarios/`,
    puis au point de référence ν_G = 1 ; θ_G n'en dépend pas, M^G_0 (= L^CB_0), B_0 et Π^CB en dépendent."""
    nu = stationnaire.NU_G_RETENU
    entetes = [(pi, na) for pi in stationnaire.POINTS_PI for na in stationnaire.POINTS_NA]
    assert set(resultat["niveaux"]) == {(v, pi, na) for v in (nu, 1.0) for pi, na in entetes}
    for pi, na in entetes:
        retenu, reference = resultat["niveaux"][(nu, pi, na)], resultat["niveaux"][(1.0, pi, na)]
        assert retenu["theta_G"] == reference["theta_G"]
        assert retenu["L_CB"] == retenu["M_G"] and retenu["M_G"] > reference["M_G"]
        assert retenu["B_0"] > reference["B_0"] and retenu["Pi_CB"] > reference["Pi_CB"]
    tampon = io.StringIO()
    stationnaire.afficher(resultat, tampon)
    texte = tampon.getvalue()
    retenu_, reference_ = f"ν_G = {stationnaire._f(nu)} (valeur retenue)", "ν_G = 1 (référence hors domaine"
    ordre = [texte.index(f"## Grille, {retenu_}"), texte.index("## Forme fermée"),
             texte.index(f"## Grille, {reference_}"), texte.index("## État initial résolu"),
             texte.index(f"### {retenu_}"), texte.index(f"### {reference_}")]
    assert ordre == sorted(ordre)


def test_D2_sans_borne_a_taux_directeur_nul(stationnaire, base):
    """r̄ = 0, π̄ = 0 : i_CB = 0, a = 0, D2 sans borne (ν_G maximal infini) ; calcul complet sans exception."""
    r = stationnaire.calculer(replace(base, rbar=0.0))
    assert r["grille"][(1.15, 0.0, 12)]["nu_G_max_D2"] == math.inf
    assert stationnaire.plus_grand_residu(r) <= TOL


def test_rachat_net_publie_comme_constat(stationnaire, base):
    """γ̄ < 0 (g_pr = −0,1 %, π̄ = 0) : Em ≤ 0 sans refus, publié « rachat net » par `afficher`."""
    r = stationnaire.calculer(replace(base, g_pr=-0.001))
    negatifs = {k for k, v in r["grille"].items() if v["Em"] <= 0}
    assert negatifs == {(nu, 0.0, na) for nu in (1.0, 1.15) for na in stationnaire.POINTS_NA}
    tampon = io.StringIO()
    stationnaire.afficher(r, tampon)
    assert tampon.getvalue().count("rachat net (Em ≤ 0)") == len(negatifs)


# --- Domaine des champs : valeurs non finies et normalisations (constat m1 de l'audit) -------


@pytest.mark.parametrize("valeur", [math.nan, math.inf, -math.inf])
def test_champ_non_fini_refuse(stationnaire, base, valeur):
    for champ in fields(base):
        if champ.name == "n_a":
            continue
        with pytest.raises(stationnaire.HorsDomaine):
            stationnaire.controler_domaine(replace(base, **{champ.name: valeur}))


@pytest.mark.parametrize("champs", [
    {"p_0": 1e-300}, {"p_0": 1e300}, {"pr_0": 1e-300}, {"pr_0": 1e300}, {"N_pa_0": 1e-300}, {"N_pa_0": 1e300},
    {"p_0": 1e60, "pr_0": 1e60}, {"p_0": 1e-60, "N_pa_0": 1e-60},
])
def test_normalisations_hors_borne_refusees(stationnaire, base, champs):
    bas, haut = stationnaire.BORNE_ECHELLE
    attendu = re.escape(f"dans [{bas:g} ; {haut:g}] attendu (borne déclarée des normalisations)")
    with pytest.raises(stationnaire.HorsDomaine, match=attendu):
        stationnaire.controler_domaine(replace(base, **champs))


@pytest.mark.parametrize("champs", [
    {"p_0": 1e50, "pr_0": 1e50}, {"p_0": 1e-50, "pr_0": 1e-50}, {"p_0": 1e100}, {"N_pa_0": 1e-100},
    {"p_0": 1e100, "pr_0": 1e-100, "N_pa_0": 1e100}, {"p_0": 1e34, "pr_0": 1e33, "N_pa_0": 1e33},
])
def test_normalisations_a_la_borne_admises(stationnaire, base, champs):
    """Constat m-b de l'audit : une valeur égale à la borne à l'arrondi près (1e50 × 1e50 = 1,0000000000000002e100)
    est admise ; l'état y tient ses contrôles, rapportés à l'échelle du bilan."""
    p = replace(base, nu_G=stationnaire.NU_G_RETENU, **champs)
    stationnaire.controler_domaine(p)
    e = stationnaire.etat_stationnaire(p)
    assert max(stationnaire.max_controles(stationnaire.controles(e, p)).values()) <= TOL


def test_complementarite_res_L_CB_relative_a_l_echelle(stationnaire, base):
    """R4 de `macro` : le contrôle Res · L^CB = 0 est écrit min(|Res|, |L^CB|)/S_CB, relatif à l'échelle du bilan
    de la banque centrale : un écart de 1e−6 S_CB sur les deux encours se lit 1e−6 à toute échelle nominale."""
    for echelle in (1e-100, 1.0, 1e100):
        p = replace(base, nu_G=stationnaire.NU_G_RETENU, p_0=echelle)
        e = stationnaire.etat_stationnaire(p)
        assert stationnaire.controles(e, p)["identites"]["Res · L^CB = 0"] == 0.0
        S_CB = e["B_CB"] + e["L_CB"] + e["M_G"]
        fausse = dict(e, Res=1e-6 * S_CB)
        lu = stationnaire.controles(fausse, p)["identites"]["Res · L^CB = 0"]
        assert abs(lu - 1e-6 * S_CB / (S_CB + 1e-6 * S_CB)) <= 1e-12 * lu, echelle


def test_valeurs_speciales_aucune_exception_hors_refus(stationnaire, base):
    """Rejeu du balayage de l'audit : valeurs spéciales sur chaque champ ; seul `HorsDomaine` peut être levé."""
    autres = []
    for champ in fields(base):
        if champ.name == "n_a":
            continue
        for x in (math.nan, math.inf, -math.inf, 0.0, -0.0, 1e-300, 1e300, -1.0):
            p = replace(base, **{champ.name: x})
            try:
                stationnaire.controler_domaine(p)
                e = stationnaire.etat_stationnaire(p)
                stationnaire.valeurs(e, p)
                stationnaire.max_controles(stationnaire.controles(e, p))
            except stationnaire.HorsDomaine:
                pass
            except Exception as erreur:  # toute autre exception est l'objet du test
                autres.append((champ.name, x, repr(erreur)))
    assert autres == []


# --- Explications établies des écarts publiés (#84), en propriétés --------------


def test_explication_dette_consolidee_sigma_en_pas(stationnaire, base):
    """La maquette tenait σ = 1,4 pas de ventes (σ = 1,4/n_a an) : elle redonne 0,25237 et 0,25844 à 2 %, et les
    quatre valeurs de la fiche 9 à 0 et 10 % (visées après la revue finale)."""
    for pi, na, publie in ((0.02, 4, "0,25237"), (0.02, 52, "0,25844"), (0.0, 4, "0,09466"), (0.10, 4, "0,49978"),
                           (0.0, 52, "0,10045"), (0.10, 52, "0,51438")):
        p = replace(base, pi_cible=pi, n_a=na, sigma=1.4 / na)
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


def test_explications_des_ecarts_A_publiees_avec_leur_statut(stationnaire, resultat):
    """Constat m3 : chaque écart historique de catégorie A porte son explication et son statut (établie après
    l'essai, ou cause non établie) ; les écarts C gardent l'explication écrite avant l'essai."""
    ecarts_A = {(l["section"], l["grandeur"]): l["explication"] for l in resultat["historique"]
                if l["verdict"] == "écart" and l["categorie"] == "A"}
    assert set(ecarts_A) == set(stationnaire.EXPLICATIONS_ECARTS)
    etablies = {k for k, x in ecarts_A.items() if x.startswith("établie après l'essai : ")}
    assert {k[1] for k in etablies} == {"dette consolidée à 2 %, n_a = 4", "dette consolidée à 2 %, n_a = 52",
                                       "Y^HS/PIB à 2 %", "marge J-ν à ν_G = 1,1, 0 %, %",
                                       "dette consolidée à 0 %, n_a = 4", "dette consolidée à 10 %, n_a = 4",
                                       "dette consolidée à 0 %, n_a = 52", "dette consolidée à 10 %, n_a = 52"}
    for k, x in ecarts_A.items():
        if k not in etablies:
            assert x == "cause non établie : maquette perdue (visa du 05/10/2026)", k
    for l in resultat["historique"]:
        if l["verdict"] == "écart" and l["categorie"] == "C":
            assert l["explication"].startswith("écrite avant l'essai : ")
    tampon = io.StringIO()
    stationnaire.afficher(resultat, tampon)
    texte = tampon.getvalue()
    assert texte.count("— explication établie après l'essai : ") == 8
    assert texte.count("— cause non établie : maquette perdue (visa du 05/10/2026)") == 4


def test_racines_parasites_absentes_affichees_aucune(stationnaire, resultat):
    """Libellé : une racine parasite inexistante se lit « aucune », non « sans objet »."""
    lignes = [l for l in resultat["publiees"] if l["grandeur"] in stationnaire.SANS_RACINE]
    assert len(lignes) == 3 and all(math.isnan(l["script"]) and l["libelle"] == "aucune" for l in lignes)
    tampon = io.StringIO()
    stationnaire.afficher(resultat, tampon)
    for ligne in tampon.getvalue().splitlines():
        if "racine parasite à" in ligne and "publié" in ligne:
            assert "script aucune" in ligne and "sans objet" not in ligne


def test_rho_IN_a_50_pourcent_lu_sur_la_configuration(stationnaire, base):
    """Constat m4 : la ligne « ρ̄_IN à 50 % (forme) » lit σ et g de la configuration, non des constantes."""
    def ligne(calc):
        return next(float(f(calc)) for _, d, _, f, _ in stationnaire.VALEURS_PUBLIEES if d == "ρ̄_IN à 50 % (forme)")

    calc = stationnaire.Calculs(base)
    assert ligne(calc) == stationnaire.rho_IN(12, base.sigma, calc.etat()["g"], 0.50)
    assert ligne(stationnaire.Calculs(replace(base, sigma=2 / 12))) != ligne(calc)
    assert ligne(stationnaire.Calculs(replace(base, g_pr=0.03))) != ligne(calc)


def test_seuil_derniere_decimale(stationnaire):
    assert stationnaire.decimales("0,25674") == 5
    assert stationnaire.comparer("0,25674", 0.256744999)[2]
    assert not stationnaire.comparer("0,25674", 0.2567451)[2]
    assert stationnaire.comparer("-0,000947", -0.0009474)[2]
    assert not stationnaire.comparer("1,536", math.nan)[2]


def test_valeurs_publiees_toutes_egales(stationnaire, resultat):
    """Valeurs en vigueur (spécification et fiches 8 et 9 republiées) : toutes égales à la dernière décimale
    publiée ; aucune valeur barrée n'y figure (catégories B-1 et N en contre-épreuve)."""
    lignes = resultat["publiees"]
    assert len(lignes) == 433
    assert {l["categorie"] for l in lignes} == {"A", "S", "B-2", "D"}
    assert sum(1 for l in lignes if l["categorie"] == "S") == 7
    assert all(l["verdict"] == "égal" for l in lignes if l["categorie"] == "S")
    assert [l for l in lignes if l["verdict"] != "égal"] == []
    for l in lignes:
        if l["publie"] == stationnaire.AUCUNE:
            assert math.isnan(l["script"]), l
        else:
            assert abs(l["ecart"]) <= l["seuil"], l


def test_valeurs_republiees_toutes_egales(stationnaire, resultat):
    """C4 de `macro` (rang 7) : les 29 valeurs visées et republiées (spécification, commit 8b9fa94 ; fiches 8 et 9)
    sont égales au script ; l'historique (commit 9c8bdbd) garde les 29 anciennes valeurs, toutes en écart, chacune
    égale à sa valeur figée en littéral (`ANCIENNES_PUBLIEES`)."""
    historique = resultat["historique"]
    assert len(historique) == len(ECARTS_PUBLIES) == 29
    assert {(l["section"], l["grandeur"]) for l in historique if l["verdict"] == "écart"} == ECARTS_PUBLIES
    assert {(l["section"], l["grandeur"]): l["publie"] for l in historique} == ANCIENNES_PUBLIEES
    en_vigueur = {(l["section"], l["grandeur"]): l for l in resultat["publiees"]}
    for k in stationnaire._AVANT_VISA:
        assert en_vigueur[k]["verdict"] == "égal", en_vigueur[k]
        ancienne = stationnaire._AVANT_VISA[k]
        assert en_vigueur[k]["publie"] != (ancienne if isinstance(ancienne, str) else ancienne[2]), k
    tampon = io.StringIO()
    stationnaire.afficher(resultat, tampon)
    texte = tampon.getvalue()
    assert ("Bilan : 433 valeurs comparées, 426 égales sur l'état résolu, 7 égales en arithmétique de la "
            "spécification (catégorie S, sans état résolu), aucun écart.") in texte
    assert "Bilan de l'historique : 29 valeurs, 29 écarts, visés le 05/10/2026" in texte
    assert "valeurs publiées avant le visa du 05/10/2026 (commit 9c8bdbd)" in texte


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
            assert len(a["racines"]) == 1  # aucune racine parasite (C51), mesurée sur tout le balayage
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


def test_alpha_et_fermeture_identiques_a_nu_G_1(stationnaire, base, resultat):
    """R2 de `macro` (rang 6) : la mesure de #80 (lecture (β) comprise) et la fermeture sont calculées à
    ν_G = `NU_G_RETENU`, où le plafond de E1 est un refus ; elles sont identiques bit à bit à ν_G = 1 (C59 :
    θ_G est fixé avant l'entrée de ν_G), là où ce plafond est inactif aux deux valeurs."""
    retenu = replace(base, nu_G=stationnaire.NU_G_RETENU)
    reference = replace(base, nu_G=1.0)
    for p in points(stationnaire, base, 1.0) + points(stationnaire, base, stationnaire.NU_G_RETENU):
        assert stationnaire.etat_stationnaire(p)["marge_E1_montant"] > 0  # plafond inactif aux deux valeurs
    assert stationnaire.superneutralite(reference) == stationnaire.superneutralite(retenu)
    assert stationnaire.sensibilite_fermeture(reference) == stationnaire.sensibilite_fermeture(retenu)
    assert resultat["superneutralite"] == stationnaire.superneutralite(retenu)
    assert resultat["fermeture"] == stationnaire.sensibilite_fermeture(retenu)


@pytest.mark.parametrize("nu_g_retenu, attendu", [(None, 1.15), (1.15, 1.15), (1.1, 1.1)])
def test_alpha_et_fermeture_lisent_la_valeur_retenue(stationnaire, base, resultat, monkeypatch, nu_g_retenu,
                                                      attendu):
    """Constat m2 : `calculer` passe à la mesure de #80 et à la fermeture le ν_G retenu effectif (l'argument, ou
    `NU_G_RETENU` s'il vaut None), et la sortie l'annonce (constat m1). L'identité bit à bit du test précédent ne
    distingue pas une lecture de `NU_G_RETENU` d'une lecture de l'argument : la garde enregistre le ν_G reçu."""
    assert stationnaire.NU_G_RETENU == 1.15
    recus = []

    def superneutralite(par):
        recus.append(("alpha", par.nu_G))
        return resultat["superneutralite"]

    def sensibilite_fermeture(par):
        recus.append(("fermeture", par.nu_G))
        return resultat["fermeture"]

    monkeypatch.setattr(stationnaire, "superneutralite", superneutralite)
    monkeypatch.setattr(stationnaire, "sensibilite_fermeture", sensibilite_fermeture)
    r = stationnaire.calculer(base, nu_g_retenu)
    # Une mesure de #80 ; trois fermetures : 2 % (`Calculs.fermeture`), puis 0 et 10 % (pentes publiées).
    assert sorted(recus) == [("alpha", attendu)] + [("fermeture", attendu)] * 3
    tampon = io.StringIO()
    stationnaire.afficher(r, tampon)
    texte = tampon.getvalue()
    assert f"sensibilité de θ_G à r̄ (π̄ = 2 %, n_a = 12, ν_G = {stationnaire._f(attendu)} ;" in texte
    assert f"- verdict : Δr̄_α = max − min sur {{0 ; 2 ; 10 %}}, n_a = 12, ν_G = {stationnaire._f(attendu)} (" in texte


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


def test_sensibilite_a_zeta_publiee(stationnaire, base, resultat):
    """`macro` : verdict jugé à ζ = 4 ; étendue des allocations L2 publiée à ζ ∈ {4 ; 8} et à ζ = 2 (illustration) ;
    les allocations dépendantes de ζ (mesurées) sont C/Y_o, ti et T^cou/PIB, exclues des tests d'invariance."""
    assert base.zeta == 4.0 and stationnaire.ZETA_PLAGE == (4.0, 8.0) and stationnaire.ZETA_ILLUSTRATION == 2.0
    sn = resultat["superneutralite"]
    assert set(sn["zeta"]) == {2.0, 4.0, 8.0}
    for q in stationnaire.ALLOCATIONS_VERDICT:  # à ζ du paramètre, l'étendue publiée est celle du verdict
        assert sn["zeta"][4.0]["allocations"][q] == sn["allocations"][q]
    assert sn["dependantes_de_zeta"] == ["C/Y_o", "ti", "T^cou/PIB"]
    assert not set(sn["dependantes_de_zeta"]) & set(ALLOCATIONS_ZETA)
    assert not set(sn["dependantes_de_zeta"]) & {"C/PIB", "G/PIB", "I/PIB", "ΔIN/PIB"}
    tampon = io.StringIO()
    stationnaire.afficher(resultat, tampon)
    texte = tampon.getvalue()
    assert "ζ = 2 (illustration, sans verdict)" in texte and "ζ = 8 (plage de la table)" in texte
    assert "allocations dépendantes de ζ" in texte and ": C/Y_o, ti, T^cou/PIB" in texte


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


# --- Domaine : facteur de croissance avant la racine n_a-ième (/code-review du rang 8) ------


@pytest.mark.parametrize("champs", [{"g_N": -1.5}, {"g_pr": -2.0}])
def test_facteur_de_croissance_negatif_refuse_avant_la_racine(stationnaire, base, champs, capsys):
    """(1 + g_pr)(1 + g_N) ≤ 0 : refus de domaine (`HorsDomaine`, code de sortie 1), non `TypeError` sur le
    complexe que donnerait la racine n_a-ième d'une base négative."""
    with pytest.raises(stationnaire.HorsDomaine, match=r"\(1 \+ g_pr\)\(1 \+ g_N\) > 0"):
        stationnaire.controler_domaine(replace(base, **champs))
    with pytest.raises(stationnaire.HorsDomaine, match=r"\(1 \+ g_pr\)\(1 \+ g_N\) > 0"):
        stationnaire.calculer(replace(base, **champs))


# --- Racine parasite : aucune, une, plusieurs (constat m2 du rang 8) -------------------


class _CalculsFactices:
    """`Calculs` réduit à `alpha()`, aux racines données pour chaque π* (appel direct de `_racine_parasite`)."""

    def __init__(self, racines: list[float]) -> None:
        self._racines = racines

    def alpha(self) -> dict[str, object]:
        return {"alpha": {pi: {"racines": self._racines} for pi in (0.0, 0.02, 0.10)}}


def test_racine_parasite_aucune_une_plusieurs(stationnaire):
    """NaN (« aucune ») seulement sans racine hors du domaine C51 ; une racine est rendue en % ; deux ou plus sont
    refusées, faute de pouvoir publier une valeur unique."""
    assert math.isnan(stationnaire._racine_parasite(_CalculsFactices([0.01]), 0.02))
    assert stationnaire._racine_parasite(_CalculsFactices([-0.2, 0.01]), 0.02) == 100 * -0.2
    with pytest.raises(stationnaire.HorsDomaine, match="2 racines parasites"):
        stationnaire._racine_parasite(_CalculsFactices([-0.3, -0.2, 0.01]), 0.02)
    # La borne −5 % est hors du domaine C51 (−5 % ; 100 %] : elle compte comme racine parasite.
    assert stationnaire._racine_parasite(_CalculsFactices([-0.05, 0.01]), 0.02) == 100 * -0.05


# --- Contre-épreuve hors du bilan des valeurs en vigueur (constat M1 du rang 8) ---------


def test_contre_epreuve_hors_du_bilan_et_egale(stationnaire, resultat):
    """Les 47 valeurs barrées reproduites sous leurs entrées d'origine (B-1 : illustration du bloc 7 ; N : ν_G non
    retenu) ont leur section et leur bilan, toutes égales, et aucune n'est comptée en vigueur."""
    lignes = resultat["contre_epreuve"]
    assert len(lignes) == 47
    assert {l["categorie"] for l in lignes} == {"B-1", "N"}
    assert sum(1 for l in lignes if l["categorie"] == "N") == 4
    assert all(l["verdict"] == "égal" for l in lignes)
    en_vigueur = {(l["section"], l["grandeur"], l["publie"]) for l in resultat["publiees"]}
    assert not en_vigueur & {(l["section"], l["grandeur"], l["publie"]) for l in lignes}
    tampon = io.StringIO()
    stationnaire.afficher(resultat, tampon)
    assert "Bilan de la contre-épreuve : 47 valeurs barrées, 47 égales sous leurs entrées d'origine, aucun écart." \
        in tampon.getvalue()


def test_minimum_de_delta_r_alpha_en_zeta(stationnaire, base):
    """« Δr̄_α ne descend pas sous 0,1428 point, minimum vers ζ ≈ 68 » : sur ζ ∈ {4 ; 30 ; 50 ; 67 ; 69 ; 100 ;
    1 000}, Δr̄_α reste au-dessus de sa valeur à ζ = 68, publiée."""
    calc = stationnaire.Calculs(base)
    minimum = stationnaire._delta_r_alpha(calc, 68.0)
    assert stationnaire.comparer("0,1428", minimum)[2]
    for zeta in (4.0, 30.0, 50.0, 67.0, 69.0, 100.0, 1000.0):
        assert stationnaire._delta_r_alpha(calc, zeta) > minimum, zeta


def test_canal_ecarts_nominaux_egale_l_identite(stationnaire, base):
    """`monnaie` (06/10/2026) : la part de ϖ_L dans r̄_α(10 %) − r̄_α(0), mesurée sur l'état résolu (catégorie D),
    égale l'identité ϖ_L[1/1,02 − 1/1,10] − ϖ_L[1/1,02 − 1], en point, à 1e−9 près."""
    identite = 100 * base.varpi_L * ((1 / 1.02 - 1 / 1.10) - (1 / 1.02 - 1))
    mesure = stationnaire._canal_ecarts_nominaux(stationnaire.Calculs(base), 4.0)
    assert abs(mesure - identite) <= 1e-9
    assert stationnaire.comparer("0,182", mesure)[2]


def test_canal_ecarts_nominaux_independant_de_zeta(stationnaire, base):
    """La part de ϖ_L dans r̄_α(10 %) − r̄_α(0) ne dépend pas de ζ (2, 4, 8), à 1e−9 point près."""
    calc = stationnaire.Calculs(base)
    mesures = [stationnaire._canal_ecarts_nominaux(calc, zeta) for zeta in (2.0, 4.0, 8.0)]
    assert max(mesures) - min(mesures) <= 1e-9


def test_canal_ecarts_nominaux_seul_varpi_L_s_isole(stationnaire, base):
    """Limite déclarée : ϖ_L et ϖ_D annulés ensemble sortent du domaine (existence du dividende de la banque) ;
    ϖ_L seul annulé y reste."""
    p = replace(base, nu_G=stationnaire.NU_G_RETENU)
    with pytest.raises(stationnaire.HorsDomaine, match="dividende de la banque"):
        stationnaire.mesure_alpha(replace(p, varpi_L=0.0, varpi_D=0.0), 0.0, 12)
    assert math.isfinite(stationnaire.mesure_alpha(replace(p, varpi_L=0.0), 0.10, 12)["r_alpha"])


@pytest.mark.parametrize("phi, zeta", [(1.0, 4.0), (1.0, 8.0), (0.0, 4.0), (0.0, 8.0)])
def test_hausse_d_un_point_du_signe_de_la_derivee(stationnaire, base, phi, zeta):
    """`monnaie` : l'effet d'un point fini sur θ_G (norme et i^ref tenus) a le signe de la dérivée publiée au même
    (φ, ζ), et la dérivée à droite tend vers la dérivée centrée quand le pas se réduit."""
    calc = stationnaire.Calculs(base)
    derivee = stationnaire._derivee_norme_tenue(calc, phi, zeta)
    point = stationnaire._hausse_d_un_point(calc, phi, zeta)
    assert point * derivee > 0
    r = base.rbar
    petit = (stationnaire._theta_norme_tenue(calc, phi, zeta, r + 1e-5)
             - stationnaire._theta_norme_tenue(calc, phi, zeta, r)) / 1e-5
    assert abs(petit - derivee) < abs(point - derivee) + 1e-12


# --- Valeurs publiées lues dans leur source (constat M1 du rang 8, décision A (iii)) ----

SPECIFICATION = RACINE / "docs" / "specification" / "nations_et_marches.tex"
FICHES = {
    "fiche 8": RACINE / "docs" / "blocs" / "banque_centrale.md",
    "banque_centrale.md": RACINE / "docs" / "blocs" / "banque_centrale.md",
    "fiche 9": RACINE / "docs" / "blocs" / "finances_publiques.md",
}


def _partager_tex(texte: str) -> tuple[str, str]:
    """(texte dans les \\barre{…}, texte hors des \\barre{…}), accolades imbriquées comprises ; hors barre, chaque
    \\barre{…} est remplacé par une espace, pour garder une ligne de tableau sur une ligne."""
    dedans, dehors, i = [], [], 0
    while (j := texte.find("\\barre{", i)) >= 0:
        dehors.append(texte[i:j])
        k, profondeur = j + len("\\barre{"), 1
        while profondeur:
            profondeur += {"{": 1, "}": -1}.get(texte[k], 0)
            k += 1
        dedans.append(texte[j + len("\\barre{"):k - 1])
        i = k
    dehors.append(texte[i:])
    return "\n".join(dedans), " ".join(dehors)


def _partager_md(texte: str) -> tuple[str, str]:
    """(texte dans les ~~…~~, texte hors des ~~…~~), sur une ligne."""
    return "\n".join(re.findall(r"~~(.+?)~~", texte)), re.sub(r"~~(.+?)~~", "\n", texte)


def _section_tex(texte: str, label: str) -> str:
    """Texte de la spécification depuis \\label{label} jusqu'au label de section ou de tableau suivant."""
    debut = texte.index("\\label{" + label + "}")
    suite = re.compile(r"\\label\{(?:sec|tab):").search(texte, debut + 1)
    return texte[debut:suite.start() if suite else len(texte)]


def _sources(section: str) -> list[tuple[str, str, str]]:
    """(nom, texte barré, texte hors barre) de chaque source citée par la section d'une valeur publiée : sections et
    tableaux de la spécification par leur label, fiches par leur fichier."""
    tex = SPECIFICATION.read_text(encoding="utf-8")
    sources = [(label, *_partager_tex(_section_tex(tex, label)))
               for label in re.findall(r"(?:sec|tab):[\w-]+", section)]
    sources += [(nom, *_partager_md(chemin.read_text(encoding="utf-8")))
                for nom, chemin in FICHES.items() if nom in section]
    assert sources, section
    return sources


# Règle de lecture d'une valeur publiée dans sa source (constat mi-1 de l'audit) :
# - frontière : ni chiffre, ni décimale collés (« 2 » ne se lit pas dans « 2,5 », ni « 5 » dans « 2,5 ») ; la virgule
#   s'écrit « , » ou « {,} » (mode mathématique) ;
# - signe : une valeur publiée négative (« -x » ou « −x ») se lit précédée d'un signe moins, « − » ou « - » (hors
#   « -- », tiret d'intervalle, et hors « - » collé à une lettre ASCII ou à « } », trait d'union : « P-0,182 »),
#   séparé du nombre au plus par des espaces, « $ », « ~ » ou « \, » (« $-0{,}058$ », « $-$0,058 »,
#   « $0{,}6505 - 0{,}4560$ ») ; une valeur publiée positive (« x » ou « +x ») se lit sans signe moins
#   devant (« + » admis) ;
# - tableau (`tab:…`) : la valeur se lit dans la ligne que déclare `LIGNES_DE_TABLEAU` (première cellule), égale à la
#   cellule de sa colonne, ou, colonne non déclarée, figurant dans une cellule de la ligne.
_ENTRE_SIGNE_ET_NOMBRE = re.compile(r"(?:\s|\$|~|\\,)+$")
_SIGNE_MOINS = re.compile(r"(?:−|(?<![-A-Za-z}])-)$")


def _figure(publie: str, texte: str) -> bool:
    """La valeur publiée figure dans le texte, signe compris, sans chiffre ni décimale collés (règle ci-dessus)."""
    absolu = publie.lstrip("-−+")
    formes = "|".join(re.escape(f) for f in (absolu, absolu.replace(",", "{,}")))
    motif = r"(?<![0-9])(?<![0-9][,.])(?<![0-9]\{,\})(?:" + formes + r")(?![0-9])(?![,.][0-9])(?!\{,\}[0-9])"
    negative = publie[0] in "-−"
    for m in re.finditer(motif, texte):
        avant = _ENTRE_SIGNE_ET_NOMBRE.sub("", texte[max(0, m.start() - 12):m.start()])
        if (_SIGNE_MOINS.search(avant) is not None) == negative:
            return True
    return False


def _cellules(texte: str, ligne: str) -> list[str]:
    """Cellules de l'unique ligne de tableau dont la première cellule est `ligne`."""
    rangs = [r for r in texte.split("\n") if re.split(r"(?<!\\)&", r)[0].strip() == ligne]
    assert len(rangs) == 1, (ligne, len(rangs))
    return [c.strip() for c in re.split(r"(?<!\\)&", rangs[0].strip().removesuffix("\\\\"))]


def _normaliser(cellule: str) -> str:
    return cellule.replace("$", "").replace("{,}", ",").replace("−", "-").strip().lstrip("+")


def _lue(stationnaire, section: str, grandeur: str, publie: str, nom: str, dehors: str) -> bool:
    """La valeur en vigueur se lit hors barre dans la source `nom` (règle ci-dessus)."""
    if not nom.startswith("tab:"):
        return _figure(publie, dehors)
    ligne, colonne = stationnaire.LIGNES_DE_TABLEAU[(section, grandeur)]
    cellules = _cellules(dehors, ligne)
    if colonne is None:
        return any(_figure(publie, c) for c in cellules[1:])
    return _normaliser(cellules[colonne]) == _normaliser(publie.replace("−", "-"))


def test_lecture_signe_frontiere_et_cellule():
    """La règle de lecture refuse les faux succès du constat mi-1 : signe ignoré, « 2 » lu dans « 2,5 », cellule
    lue ailleurs dans le tableau."""
    assert _figure("-0,058", "$-0{,}058$") and _figure("-0,058", "−0,058") and _figure("-0,058", "$-$0,058")
    assert not _figure("-0,058", "+0,058") and not _figure("-0,058", "0,058")
    assert _figure("0,182", "+0,182") and _figure("+0,157", "+0,157") and _figure("0,182", "soit 0,182 point")
    assert not _figure("0,182", "−0,182") and not _figure("0,182", "$-0{,}182$")
    assert _figure("2", "1--2") and not _figure("-2", "1--2") and _figure("2", "de 1 à 2 %")
    assert _figure("-0,4560", "$0{,}6505 - 0{,}4560$") and _figure("-0,05", "$-\\,0{,}05$")
    assert not _figure("2", "2,5") and not _figure("5", "2,5") and not _figure("5", "2{,}5")
    assert not _figure("0,18", "0,182") and not _figure("2", "12")
    assert _figure("0,182", "P-0,182") and not _figure("-0,058", "P-0,058")
    assert _figure("0,182", "\\mathrm{x}-0,182") and not _figure("-0,058", "\\mathrm{x}-0,058")
    tab = "A & x & 1,00 & 2,000\\\\\nB & y & 2,000 & $-0{,}5$\\\\"
    assert _cellules(tab, "B") == ["B", "y", "2,000", "$-0{,}5$"]
    assert _normaliser(_cellules(tab, "B")[3]) == _normaliser("-0,5")
    assert _normaliser(_cellules(tab, "A")[2]) != _normaliser("2,000")


def test_valeurs_en_vigueur_ecrites_hors_barre_dans_leur_source(stationnaire):
    """Chaque valeur en vigueur figure hors de \\barre{…} (spécification) et de ~~…~~ (fiches) dans chacune des
    sources que cite sa section, signe compris, sans décimale collée, et, dans un tableau, dans la cellule de sa
    ligne et de sa colonne (`LIGNES_DE_TABLEAU`) : une valeur barrée ne peut être comptée en vigueur."""
    manquantes = [(section, grandeur, publie) for section, grandeur, publie, _, _ in stationnaire.VALEURS_PUBLIEES
                  if publie != stationnaire.AUCUNE
                  and not all(_lue(stationnaire, section, grandeur, publie, nom, dehors)
                              for nom, _, dehors in _sources(section))]
    assert manquantes == []


def test_chaque_valeur_de_tableau_a_sa_ligne(stationnaire):
    """Toute valeur en vigueur lue dans un tableau a un rattachement déclaré, et tout rattachement sert."""
    lues = {(section, grandeur) for section, grandeur, _, _, _ in stationnaire.VALEURS_PUBLIEES if "tab:" in section}
    assert lues == set(stationnaire.LIGNES_DE_TABLEAU)


def test_valeurs_de_contre_epreuve_et_d_historique_barrees_dans_leur_source(stationnaire):
    """Chaque valeur de contre-épreuve et d'historique figure barrée dans au moins une des sources que cite sa
    section, signe compris : une valeur qui change de statut dans la source sans que le script suive fait échouer la
    batterie."""
    listes = stationnaire.VALEURS_CONTRE_EPREUVE + stationnaire.VALEURS_AVANT_VISA
    assert len(listes) == 47 + 29
    manquantes = [(section, grandeur, publie) for section, grandeur, publie, _, _ in listes
                  if not any(_figure(publie, dedans) for _, dedans, _ in _sources(section))]
    assert manquantes == []
