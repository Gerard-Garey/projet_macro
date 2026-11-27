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
    # Libellé corrigé le 14/10/2026 (« fiche 9 § 3.C » → « fiche 9 § 6.3 »), décision du mainteneur ; valeur et
    # verdict inchangés.
    ("fiche 9 § 6.3", "(α) : max − min de C/PIB, point"): "0,908",
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


def aux_entrees_des_cas_adverses(stationnaire, base):
    """Cas adverses du domaine (lv* = 0,6 et 0,45) construits à ϑ = 0,10 et ν_H = 1, avant M34 (#130, #62) : refus
    et constats décidés par `macro` sous ces valeurs. À ϑ = 0,15 puis ν_H = 1,1, la dette consolidée plus haute
    (C42 : +ΔE^Bk, puis +ΔD_H) relève B et la marge de E1, et ces cas sortent de leur région ; ϑ et ν_H sont donc
    rétablis seuls (μ̄ = 0,60 et ζ = 8 gardés)."""
    return replace(base, vartheta=stationnaire.ENTREES_D_ORIGINE["vartheta"],
                   nu_H=stationnaire.ENTREES_D_ORIGINE["nu_H"])


def points(stationnaire, base, nu=1.0):
    """Paramètres des neuf points π̄ × n_a de la grille, à ν_G donné."""
    return [
        replace(base, pi_cible=pi, n_a=na, nu_G=nu) for pi in stationnaire.POINTS_PI for na in stationnaire.POINTS_NA
    ]


def relatif(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


# --- Indépendance et déterminisme (P9 ; propriété 11) -----------------------------


def test_n_importe_que_la_bibliotheque_standard_et_le_module_feuille():
    """Bibliothèque standard, plus le seul module feuille `nations.scenarios.stationnaire` ; jamais
    `archive` (ADR 0015, point 14.1 ; décision S2)."""
    arbre = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    modules, de_nations = set(), set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            modules.update(a.name.split(".")[0] for a in noeud.names)
            de_nations.update(a.name for a in noeud.names if a.name.split(".")[0] == "nations")
        elif isinstance(noeud, ast.ImportFrom):
            assert noeud.level == 0
            modules.add((noeud.module or "").split(".")[0])
            if (noeud.module or "").split(".")[0] == "nations":
                de_nations.update(f"{noeud.module}.{a.name}" for a in noeud.names)
    assert modules <= {"__future__", "argparse", "dataclasses", "json", "math", "sys", "nations"}
    assert de_nations == {"nations.scenarios.stationnaire"}
    assert not modules & {"archive", "src"}


def test_le_script_ne_charge_de_nations_que_le_module_feuille():
    """À l'exécution, importer le script ne charge de `nations` que le paquet, `scenarios` et le module
    feuille (les `__init__` de `nations` et de `scenarios` n'importent rien)."""
    code = ("import importlib.util, sys\n"
            f"spec = importlib.util.spec_from_file_location('etat_stationnaire', {str(SCRIPT)!r})\n"
            "module = importlib.util.module_from_spec(spec)\n"
            "sys.modules['etat_stationnaire'] = module\n"
            "spec.loader.exec_module(module)\n"
            "print(sorted(m for m in sys.modules if m == 'nations' or m.startswith('nations.')))\n")
    sortie = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout
    assert sortie.strip() == "['nations', 'nations.scenarios', 'nations.scenarios.stationnaire']"


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


def test_marge_en_logarithme_publiee_a_l_ouverture(stationnaire, base):
    """P54 (#112) : `ouverture` publie μ̃_{−1} = ln(1 + μ̄), égale à ln(P_{−1}/UC_{−1}) que lit P2
    dans `un_pas` (à 1e−15 près), et P2 rend μ̃_0 = μ̃_{−1} au point fixe (ξ = 0)."""
    for p in points(stationnaire, base):
        e = stationnaire.etat_stationnaire(p)
        o = stationnaire.ouverture(e, p)
        assert o["mu_tilde_m1"] == math.log(1 + p.mu_bar)
        pr_m1 = o["pr"] * (1 + p.g_pr) ** (-1 / p.n_a)
        assert abs(o["mu_tilde_m1"] - math.log(o["registre"][0] / (o["W_m1"] / pr_m1))) <= 1e-15
        assert abs(stationnaire.un_pas(o, p)["mu_tilde"] - o["mu_tilde_m1"]) <= 1e-15


def test_marge_de_p2_et_t2_sous_la_forme_i_declaree(stationnaire, base):
    """#125, point 3 : `un_pas` évalue P2 et T2 sous la forme (i), ln(P_{t−1}/UC_{t−1}) tirée du
    registre et de W_{t−1}, forme indépendante déclarée (le moteur lit μ̃_{t−1}, P54, option (ii)) :
    une ouverture où μ̃_{−1} ≠ ln(P_{−1}/UC_{−1}) donne le même pas, au bit."""
    for p in points(stationnaire, base):
        o = stationnaire.ouverture(stationnaire.etat_stationnaire(p), p)
        s = stationnaire.un_pas(o, p)
        assert stationnaire.un_pas({**o, "mu_tilde_m1": o["mu_tilde_m1"] + 0.1}, p) == s


def test_n6_refuse_une_demande_adressee_nulle(stationnaire, base):
    """#125, point 4 : à l'état résolu, à d = 0 (C^plan = I^plan = G^plan = 0 : D_H = 0, ti = 0, M_G = 0), N6 du
    script donne un refus explicite au lieu d'une division par zéro ; le moteur, lui, rend des
    volumes servis nuls (`nations.blocs.production.ventes`)."""
    for p in points(stationnaire, base):
        o = stationnaire.ouverture(stationnaire.etat_stationnaire(p), p)
        with pytest.raises(stationnaire.HorsDomaine, match="N6 : demande adressée d = 0"):
            stationnaire.un_pas({**o, "D_H": 0.0, "ti": 0.0, "M_G": 0.0}, p)


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
        ("U_eq", 0.0),
        ("U_eq", -0.01),
        ("mu_bar", 0.0),
        ("mu_bar", -0.1),
        ("mu_bar", -1.0),
        ("p_0", 0.0),
    ],
)
def test_refus_explicite_hors_domaine(stationnaire, base, champ, valeur):
    with pytest.raises(stationnaire.HorsDomaine):
        stationnaire.controler_domaine(replace(base, **{champ: valeur}))


@pytest.mark.parametrize("champ, valeur, motif", [
    ("U_eq", 0.0, "0 < U\\^eq < 1 .*existence"), ("mu_bar", 0.0, "μ̄ > 0 .*existence")])
def test_conditions_d_existence_p71_nommees(stationnaire, base, champ, valeur, motif):
    """P71 : U^eq ≤ 0 et μ̄ ≤ 0 refusés dès le chargement des paramètres, le motif les nommant
    comme conditions de conception et d'existence de l'état stationnaire ; la calibration
    (U^eq = 0,05, μ̄ = 0,60) n'est pas refusée."""
    with pytest.raises(stationnaire.HorsDomaine, match=motif):
        stationnaire.controler_domaine(replace(base, **{champ: valeur}))
    stationnaire.controler_domaine(replace(base, nu_G=1.15))


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
    pas un refus au point de référence (décision de `macro`, option (b)), mais il l'est à ν_G > 1. Cas construit à
    ϑ = 0,10 et ν_H = 1 (`aux_entrees_des_cas_adverses`)."""
    base = aux_entrees_des_cas_adverses(stationnaire, base)
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
    """lv* = 0 et τ_H = 0 (domaine fermé) : calcul complet sans exception ; rapports sans objet publiés tels. Le bord
    τ_H = 0 est construit à ν_H = 1 (avant M34, #62) : à ν_H = 1,1, la lecture (α) de #80 n'a plus de racine sur
    [−60 % ; 100 %] à π* = 10 %, n_a = 52 (θ_G* ≈ 0,0056 ; `test_bord_tau_H_nul_refuse_par_la_lecture_alpha`)."""
    if champ == "tau_H":
        base = replace(base, nu_H=stationnaire.ENTREES_D_ORIGINE["nu_H"])
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


def test_bord_tau_H_nul_refuse_par_la_lecture_alpha(stationnaire, base):
    """τ_H = 0 à la table calibrée (ν_H = 1,1, #62) : l'état stationnaire se résout aux neuf points de la grille, mais
    la lecture (α) de #80 (C51) n'a aucune racine sur [−60 % ; 100 %] à π* = 10 %, n_a = 52 (F(r̄) < 0 sur tout le
    balayage) : `calculer` refuse par `HorsDomaine`, motif nommé, sans valeur silencieuse. À ν_H = 1, la racine
    existe (r̄_α ≈ 27,4 %)."""
    variante = replace(base, tau_H=0.0)
    assert variante.nu_H == 1.1
    for p in points(stationnaire, variante, stationnaire.NU_G_RETENU):
        stationnaire.etat_stationnaire(p)
    with pytest.raises(stationnaire.HorsDomaine, match=r"lecture \(α\), π\* = 0\.1, n_a = 52 : 0 racine"):
        stationnaire.calculer(variante)
    origine = replace(variante, nu_H=stationnaire.ENTREES_D_ORIGINE["nu_H"], nu_G=stationnaire.NU_G_RETENU)
    assert round(stationnaire.mesure_alpha(origine, 0.10, 52)["r_alpha"], 3) == 0.274


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


def test_q1_publie_comme_constat_sous_mu_bar_d_origine_seulement(stationnaire, base, resultat):
    """D_F en fin de phase 4 : sous μ̄ = 0,25 (entrées d'origine), négatif à n_a = 4 (constat publié), positif à
    n_a = 12 et 52 (décision du 05/10/2026, pt 4) ; sous μ̄ = 0,60 (M34, #92), positif aux trois n_a, ν_F,min < ν_F,
    et aucun constat q1 n'est publié.

    q1 est un constat publié, pas un résidu : il ne change pas le code de sortie.
    """
    assert base.mu_bar == 0.60
    for (_nu, pi, na), v in resultat["grille"].items():
        assert v["caisse_DF4"] > 0, (pi, na)
        assert v["nu_F_min"] < resultat["parametres"].nu_F, (pi, na)
    tampon = io.StringIO()
    stationnaire.afficher(resultat, tampon)
    assert "q1 : D_F en fin de phase 4 négatif" not in tampon.getvalue()
    origine = stationnaire.calculer(replace(base, **stationnaire.ENTREES_D_ORIGINE))
    for (nu, pi, na), v in origine["grille"].items():
        assert (v["caisse_DF4"] < 0) == (na == 4), (nu, pi, na)
        assert (v["nu_F_min"] > origine["parametres"].nu_F) == (na == 4), (nu, pi, na)
    tampon = io.StringIO()
    stationnaire.afficher(origine, tampon)
    colonnes_nu = len({k[0] for k in origine["grille"]})
    assert tampon.getvalue().count("q1 : D_F en fin de phase 4 négatif") == 3 * colonnes_nu


# --- Valeurs publiées (propriété 9 ; critère J1) --------------------------------


# --- Colonne de référence ν_G = 1 hors domaine (décision de `macro`, option (b)) ---------


@pytest.mark.parametrize("pi, n_a, admis", [
    (0.0, 4, False), (0.0, 12, False), (0.0, 52, False), (0.02, 4, True), (0.02, 12, False), (0.02, 52, False),
])
def test_lv_0_6_a_nu_G_1_15_refus_sur_la_dette_brute(stationnaire, base, pi, n_a, admis):
    """`macro` : lv* = 0,6, ν_G = 1,15 : refus sur B < 0 là où la marge de E1 est positive (le refus ne vient pas
    de E1) ; témoin admis à π̄ = 2 %, n_a = 4 (B/(n_a PIB) ≈ +0,042). Cas construit à ϑ = 0,10 et ν_H = 1
    (`aux_entrees_des_cas_adverses`)."""
    p = replace(aux_entrees_des_cas_adverses(stationnaire, base), lv=0.6, nu_G=1.15, pi_cible=pi, n_a=n_a)
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
    """Le plafond de E1 reste un refus sur les colonnes ν_G > 1 (lv* = 0,45, π̄ = 0, n_a = 4, ν_G = 1,001) ; cas
    construit à ϑ = 0,10 et ν_H = 1 (`aux_entrees_des_cas_adverses`)."""
    p = replace(aux_entrees_des_cas_adverses(stationnaire, base), lv=0.45, pi_cible=0.0, n_a=4, nu_G=1.001)
    assert stationnaire.etat_stationnaire(p, controler=False)["marge_E1_montant"] <= 0
    with pytest.raises(stationnaire.HorsDomaine, match="plafond de E1"):
        stationnaire.etat_stationnaire(p)


def test_plafond_de_E1_refuse_a_nu_G_superieur_a_un_a_la_table_calibree(stationnaire, base):
    """Équivalent prospectif à la table calibrée (E3, ν_H = 1,1 ; audit léger de #62, 17/11/2026) : lv* = 0,52,
    π̄ = 0, n_a = 4, ν_G = 1,001 : marge de E1 négative (−2,85e−4 en montant), B et B_Bk positifs
    (B/(n_a PIB) ≈ 0,056), refus motivé par le seul plafond de E1. Marges mesurées : la marge de E1 change de
    signe entre lv* = 0,500 (+3,6e−5) et 0,505 (−4,4e−5), B entre 0,55 (+0,0055) et 0,56 (−0,011)."""
    assert base.nu_H == 1.1
    p = replace(base, lv=0.52, pi_cible=0.0, n_a=4, nu_G=1.001)
    e = stationnaire.etat_stationnaire(p, controler=False)
    assert e["marge_E1_montant"] < 0 and e["B"] > 0 and e["B_Bk"] > 0
    assert 0.05 < e["B"] / (p.n_a * e["PIB"]) < 0.06
    with pytest.raises(stationnaire.HorsDomaine, match="plafond de E1"):
        stationnaire.etat_stationnaire(p)


def test_reference_hors_domaine_publiee_comme_constat(stationnaire, base, monkeypatch, capsys):
    """`macro` : lv* = 0,45 : plafond de E1 actif à ν_G = 1 en (0, 4) et (0, 12), toutes les colonnes ν_G > 1
    admissibles ; constat publié, aucune valeur d'état ni résidu pour ces points de référence ; le constat seul ne
    change pas le code de sortie. Cas construit à ϑ = 0,10 et ν_H = 1 (`aux_entrees_des_cas_adverses`). Sous ce cas,
    r̄_α(10 %) croît avec ζ et le croisement de r̄_α(0) et r̄ (ζ ≈ 77,57) n'est pas un minimum de Δr̄_α : la ligne du
    minimum (#173) est refusée, seule, constat publié comme « état non publié » : code 0."""
    variante = replace(aux_entrees_des_cas_adverses(stationnaire, base), lv=0.45)
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
    refusees = [l for l in r["publiees"] if l["verdict"] == "refusée"]
    assert [l["grandeur"] for l in refusees] == ["Δr̄_α au minimum en ζ sur [2 ; 200], point"]
    assert "croisement trouvé mais non minimal" in refusees[0]["libelle"]
    monkeypatch.setattr(stationnaire, "Parametres", lambda: variante)
    assert stationnaire.main([]) == 0
    sortie = capsys.readouterr()
    assert "état non publié" in sortie.out
    assert "1 refusée (minimum de Δr̄_α en ζ non localisé, motif à la ligne)." in sortie.out


# Équivalent du cas adverse lv* = 0,6 à la table calibrée, ajouté de façon prospective après l'audit léger de #130
# (17/11/2026) : lv* = 0,65 en reproduit le motif à ϑ = 0,15, ν_H = 1 (état E2, mesuré avant l'écriture). À ν_H = 1,1
# (#62, état E3), la dette consolidée plus haute (C42 : +ΔD_H) relève B : lv* = 0,65 sort de la région (trois refus,
# aucun plafond de E1 seul), et lv* = 0,70 en reproduit le motif (mesuré sur lv* ∈ {0,65 ; 0,70 ; 0,72 ; 0,74 ; 0,75}
# avant l'écriture ; 0,72 et au-delà : six refus). Le cas lv* = 0,45 n'a pas d'équivalent mesuré à E2 sur
# [0,450 ; 0,500] (pas de 0,005) : à lv* = 0,475, le plafond de E1 n'agit qu'en (0, 4) et (0, 12) à ν_G = 1, mais
# `calculer` refuse une valeur publiée (B < 0) dès lv* = 0,47 ; à E3 (table T1), sa recherche selon le critère de
# `macro` est `test_cas_lv_0_45_a_la_table_t1_critere_de_macro` (#170).


@pytest.mark.parametrize("nu_H, lv, temoin", [(1.0, 0.65, 0.0224), (1.1, 0.70, 0.0228)],
                         ids=["E2, lv 0,65", "E3, lv 0,70"])
def test_refus_a_lv_equivalent_a_la_table_calibree(stationnaire, base, nu_H, lv, temoin):
    """lv* = 0,65 à ϑ = 0,15, ν_H = 1 (E2), et lv* = 0,70 à la table calibrée (E3, ν_H = 1,1), ν_G = 1 : cinq points
    refusés sur B < 0 et un plafond de E1 seul en (2 %, 4), comme lv* = 0,6 à ϑ = 0,10 ; à ν_G = 1,15, refus sur
    B < 0 là où la marge de E1 est positive, témoin admis en (2 %, 4) (B/(n_a PIB) ≈ +0,022 et +0,023) ; la grille
    complète est refusée."""
    assert base.nu_H == 1.1
    variante = replace(base, lv=lv, nu_H=nu_H)
    refus, e1_seul = [], []
    for p in points(stationnaire, variante):
        e = stationnaire.etat_stationnaire(p, controler=False)
        if e["B"] < 0 or e["B_Bk"] < 0:
            refus.append((p.pi_cible, p.n_a))
            with pytest.raises(stationnaire.HorsDomaine, match="B ="):
                stationnaire.etat_stationnaire(p)
        elif e["marge_E1_montant"] <= 0:
            e1_seul.append((p.pi_cible, p.n_a))
    assert refus == [(0.0, 4), (0.0, 12), (0.0, 52), (0.02, 12), (0.02, 52)]
    assert e1_seul == [(0.02, 4)]
    for pi, n_a in ((0.0, 4), (0.0, 12), (0.0, 52), (0.02, 4), (0.02, 12), (0.02, 52)):
        p = replace(variante, nu_G=1.15, pi_cible=pi, n_a=n_a)
        e = stationnaire.etat_stationnaire(p, controler=False)
        assert e["marge_E1_montant"] > 0
        if (pi, n_a) == (0.02, 4):
            assert round(stationnaire.etat_stationnaire(p)["B"] / (n_a * e["PIB"]), 4) == temoin
        else:
            assert e["B"] < 0
            with pytest.raises(stationnaire.HorsDomaine, match="B = .*dette brute"):
                stationnaire.etat_stationnaire(p)
    with pytest.raises(stationnaire.HorsDomaine):
        stationnaire.calculer(variante)


# Recherche de l'équivalent du cas lv* = 0,45 à la table T1 (#170), critère écrit par `macro` avant l'essai (feuille de
# route, § 1, rang 4) : lv* ∈ [0,30 ; 0,47] balayé au pas 0,005, puis bissection à 1e−4 sur chaque changement de
# l'indicateur « E1 refusé à ν_G = 1 » ; T1, n_a = 12, π̄ ∈ {0 ; 2 ; 10 %}. Formulation d'origine : cas trouvé si,
# « aux trois π̄ », E1 est refusé à ν_G = 1, admis à ν_G = 1,001 et 1,15, et B ≥ 0. Elle était mal posée : le cas
# d'origine lui-même (lv* = 0,45, entrées d'origine) n'est refusé qu'à π̄ = 0. Correction prospective du mainteneur
# (P277, 26/11/2026) : « à au moins un π̄ » ; le verdict publié sous l'ancienne formulation, aucun cas sur
# [0,30 ; 0,47], est inchangé, et la nouvelle lecture le reproduit (mesuré par ce test). « Admis » à ν_G > 1 se lit
# comme l'admission complète (`etat_stationnaire(..., controler=True)` sans `HorsDomaine`). Sinon, les deux
# frontières mesurées (E1 à ν_G = 1, B < 0) et l'absence sont publiées. La frontière de E1, hors de l'intervalle, est
# cherchée au-delà au même pas, jusqu'à `LV_170_EXTENSION` (borne déclarée de cette seule mesure, sans effet sur le
# verdict) ; aucune recherche de cas au-delà de 0,47 (P278) : la frontière de E1 à ν_G = 1,001 (π̄ = 0) n'y est
# imprimée qu'en constat. La contre-épreuve reste aux entrées d'origine (`test_reference_hors_domaine_publiee_comme_
# constat`) ; son application aux variantes de lv* par `calculer` est #185 (P279).
LV_170_INTERVALLE = (0.30, 0.47)
LV_170_PAS = 0.005
LV_170_TOL = 1e-4
LV_170_NU = (1.0, 1.001, 1.15)
LV_170_EXTENSION = 0.70
# Constat de #185 : la ligne de #173 (« Δr̄_α au minimum en ζ sur [2 ; 200] ») refusée hors d'un intervalle de lv*.
# Balayage grossier mesuré avant l'écriture (`minimum_delta_r_alpha_en_zeta`, T1) : refus « croisement non minimal »
# en lv* ∈ {0,30 ; 0,31 ; … ; 0,34 ; 0,345} et {0,46 ; 0,47}, admission en {0,35 ; 0,36 ; … ; 0,45 ; 0,455}. Les
# deux couples encadrants ci-dessous partent de ce balayage ; une évaluation coûte environ 1,5 s, d'où deux seules
# bissections à 1e−4.
LV_173_ENCADRANTS = ((0.345, 0.35), (0.455, 0.46))


def _bissection_lv(predicat, a, b, tol=LV_170_TOL):
    """[a ; b] de largeur ≤ `tol` encadrant le changement de `predicat` (valeurs différentes aux deux bornes)."""
    pa = predicat(a)
    assert pa != predicat(b)
    while b - a > tol:
        m = (a + b) / 2
        if predicat(m) == pa:
            a = m
        else:
            b = m
    return a, b


def _balayage_lv(debut, fin, pas=LV_170_PAS):
    """Points du balayage de `debut` à `fin` inclus (arrondis au pas : aucun cumul d'erreur)."""
    return [round(debut + k * pas, 6) for k in range(round((fin - debut) / pas) + 1)]


def test_cas_lv_0_45_a_la_table_t1_critere_de_macro(stationnaire, base):
    """#170 : verdict du critère de `macro` (ci-dessus, lecture corrigée P277) à la table T1, et frontières mesurées.

    Propriétés : (i) sur [0,30 ; 0,47], l'indicateur « E1 refusé à ν_G = 1 » ne change à aucun π̄ (aucune bissection
    à faire) et ne vaut jamais vrai : aucun cas « à au moins un π̄ » (P277), donc aucun sous l'ancienne lecture
    « aux trois π̄ » ; (ii) la frontière de E1 à ν_G = 1 (π̄ = 0) est au-delà de 0,47, et elle recule quand π̄ monte
    (celle de π̄ = 0 est sous celle de 2 %, aucune à 10 % jusqu'à `LV_170_EXTENSION`) : sens de variation mesuré,
    qui contrôle l'indicateur aux trois π̄ ; (iii) la frontière B < 0 de `calculer` est dans l'intervalle, encadrée à
    1e−4 : `calculer` admet la borne gauche et refuse la borne droite (« dette brute ») ; le point refusé est dans la
    contre-épreuve (`ENTREES_D_ORIGINE` sur le lv* de la variante, n_a = 12, ν_G = 1), les points T1 de la grille
    gardant B ≥ 0 (#185). L'indicateur est validé sur le cas d'origine (lv* = 0,45, ϑ = 0,10, ν_H = 1 : E1 refusé à
    ν_G = 1 en π̄ = 0, n_a = 12). Constats imprimés sans verdict : frontière de E1 à ν_G = 1,001 (π̄ = 0, P278) et
    intervalle de lv* hors duquel la ligne de #173 est refusée (#185). Verdict et frontières imprimés (`pytest -s`)."""
    assert base.nu_H == 1.1 and base.vartheta == 0.15  # table T1

    def etat(b, lv, pi, nu, n_a=12):
        return stationnaire.etat_stationnaire(replace(b, lv=lv, pi_cible=pi, n_a=n_a, nu_G=nu), controler=False)

    def e1_refuse(b, lv, pi, nu=1.0):
        return not etat(b, lv, pi, nu)["marge_E1_montant"] > 0  # test de `Calculs.etat`

    def admis(lv, pi, nu):
        """Admission complète à ν_G > 1 : toutes les conditions de `etat_stationnaire`, plafond de E1 compris."""
        try:
            stationnaire.etat_stationnaire(replace(base, lv=lv, pi_cible=pi, n_a=12, nu_G=nu), controler=True)
        except stationnaire.HorsDomaine:
            return False
        return True

    def cas_en(lv, pi):
        return (e1_refuse(base, lv, pi) and etat(base, lv, pi, 1.0)["B"] >= 0
                and all(admis(lv, pi, nu) for nu in LV_170_NU[1:]))

    def cas(lv):  # « à au moins un π̄ » (P277)
        return any(cas_en(lv, pi) for pi in stationnaire.POINTS_PI)

    def cas_ancienne_lecture(lv):  # « aux trois π̄ » (formulation d'origine, verdict publié)
        return all(cas_en(lv, pi) for pi in stationnaire.POINTS_PI)

    # L'indicateur reconnaît le cas d'origine (garde contre une recherche vide).
    assert e1_refuse(aux_entrees_des_cas_adverses(stationnaire, base), 0.45, 0.0)

    # (i) Balayage et bissections du critère.
    grille = _balayage_lv(*LV_170_INTERVALLE)
    assert grille[0] == LV_170_INTERVALLE[0] and grille[-1] == LV_170_INTERVALLE[1] and len(grille) == 35
    indicateur = {pi: [e1_refuse(base, lv, pi) for lv in grille] for pi in stationnaire.POINTS_PI}
    changements = {pi: [_bissection_lv(lambda x, pi=pi: e1_refuse(base, x, pi), a, b)
                        for a, b, ia, ib in zip(grille, grille[1:], ind, ind[1:]) if ia != ib]
                   for pi, ind in indicateur.items()}
    candidats = grille + [x for encadrements in changements.values() for ab in encadrements for x in ab]
    trouves = sorted(lv for lv in candidats if cas(lv))
    trouves_ancienne = sorted(lv for lv in candidats if cas_ancienne_lecture(lv))
    marge_min = min((etat(base, lv, pi, 1.0)["marge_E1_montant"], lv, pi)
                    for lv in grille for pi in stationnaire.POINTS_PI)
    print(f"\n#170, T1, n_a = 12, lv* ∈ [{LV_170_INTERVALLE[0]} ; {LV_170_INTERVALLE[1]}], pas {LV_170_PAS} : "
          f"changements de « E1 refusé à ν_G = 1 » : {changements} ; marge minimale de E1 à ν_G = 1 : "
          f"{marge_min[0]:.6g} (lv* = {marge_min[1]}, π̄ = {marge_min[2]}) ; verdict « à au moins un π̄ » (P277) : "
          f"{'cas trouvé ' + str(trouves) if trouves else 'aucun cas'} ; ancienne lecture « aux trois π̄ » : "
          f"{'cas trouvé ' + str(trouves_ancienne) if trouves_ancienne else 'aucun cas'}")
    assert all(not any(ind) for ind in indicateur.values())
    assert all(not c for c in changements.values()) and not trouves and not trouves_ancienne

    # (ii) Frontières de E1 au-delà de l'intervalle (même pas, même précision) : à ν_G = 1 aux trois π̄, et, en constat
    # sans verdict (P278), à ν_G = 1,001 en π̄ = 0.
    extension = _balayage_lv(LV_170_INTERVALLE[1], LV_170_EXTENSION)

    def frontiere(pi, nu):
        ind = [e1_refuse(base, lv, pi, nu) for lv in extension]
        premier = next((k for k in range(1, len(ind)) if ind[k] != ind[0]), None)
        return (None if premier is None else
                _bissection_lv(lambda x: e1_refuse(base, x, pi, nu), extension[premier - 1], extension[premier]))

    def encadrement(f):
        return "aucune" if f is None else f"[{f[0]:.6f} ; {f[1]:.6f}]"

    frontieres_e1 = {pi: frontiere(pi, 1.0) for pi in stationnaire.POINTS_PI}
    frontiere_e1_1001 = frontiere(0.0, LV_170_NU[1])
    print(f"#170, frontière de E1 à ν_G = 1 (n_a = 12) sur [{LV_170_INTERVALLE[1]} ; {LV_170_EXTENSION}] : "
          + " ; ".join(f"π̄ = {pi} : {encadrement(f)}" for pi, f in frontieres_e1.items()))
    print(f"#170, constat sans verdict (P278) : frontière de E1 à ν_G = {LV_170_NU[1]} (π̄ = 0, n_a = 12) sur "
          f"[{LV_170_INTERVALLE[1]} ; {LV_170_EXTENSION}] : {encadrement(frontiere_e1_1001)}")
    assert frontieres_e1[0.0] is not None and frontieres_e1[0.0][0] > LV_170_INTERVALLE[1]
    assert frontieres_e1[0.02] is not None and frontieres_e1[0.0][1] < frontieres_e1[0.02][0]
    assert frontieres_e1[0.10] is None

    # (iii) Frontière B < 0 de `calculer` : B minimal sur les points que `calculer` résout (grille T1 aux colonnes
    # ν_G, contre-épreuve aux entrées d'origine, n_a = 12, ν_G = 1), encadrée à 1e−4, puis confirmée par `calculer`.
    origine = replace(base, **stationnaire.ENTREES_D_ORIGINE)
    colonnes = (1.0, *stationnaire.NU_G_PROPOSES)

    def b_t1(lv):
        return min(etat(base, lv, pi, nu, na)["B"] for pi in stationnaire.POINTS_PI
                   for na in stationnaire.POINTS_NA for nu in colonnes)

    def b_origine(lv):
        return min(etat(origine, lv, pi, 1.0)["B"] for pi in stationnaire.POINTS_PI)

    signe_b = [min(b_t1(lv), b_origine(lv)) < 0 for lv in grille]
    assert not signe_b[0] and signe_b[-1]
    k = signe_b.index(True)
    a, b = _bissection_lv(lambda x: min(b_t1(x), b_origine(x)) < 0, grille[k - 1], grille[k])
    assert b_t1(b) >= 0 and b_origine(b) < 0  # refus de la contre-épreuve, points T1 admis
    stationnaire.calculer(replace(base, lv=a))  # admis
    with pytest.raises(stationnaire.HorsDomaine, match="dette brute"):
        stationnaire.calculer(replace(base, lv=b))
    signe_t1 = [b_t1(lv) < 0 for lv in extension]
    assert not signe_t1[0] and signe_t1[-1]
    j = signe_t1.index(True)
    a1, b1 = _bissection_lv(lambda x: b_t1(x) < 0, extension[j - 1], extension[j])
    print(f"#170, frontière B < 0 de `calculer` (contre-épreuve, ENTREES_D_ORIGINE, n_a = 12, ν_G = 1 ; points T1 : "
          f"B ≥ 0 ; #185) : [{a:.6f} ; {b:.6f}]")
    print(f"#170, frontière B < 0 des seuls points T1 (grille, colonnes {colonnes}) : [{a1:.6f} ; {b1:.6f}] ; "
          "absence publiée")
    assert LV_170_INTERVALLE[0] < a < b <= LV_170_INTERVALLE[1] < a1

    # Constat sans verdict (#185) : intervalle de lv* hors duquel la ligne de #173 est refusée.
    def ligne_173_refusee(lv):
        try:
            stationnaire.minimum_delta_r_alpha_en_zeta(stationnaire.Calculs(replace(base, lv=lv)))
        except stationnaire.MinimumNonEncadre:
            return True
        return False

    gauche, droite = (_bissection_lv(ligne_173_refusee, *ab) for ab in LV_173_ENCADRANTS)
    print(f"#170, constat sans verdict (#185) : ligne de #173 « Δr̄_α au minimum en ζ sur [2 ; 200] » refusée hors "
          f"de lv* ∈ [{gauche[1]:.6f} ; {droite[0]:.6f}] (frontières encadrées à 1e−4 : [{gauche[0]:.6f} ; "
          f"{gauche[1]:.6f}] et [{droite[0]:.6f} ; {droite[1]:.6f}])")


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
    quatre valeurs de la fiche 9 à 0 et 10 % (visées après la revue finale), sous les entrées d'origine (μ̄ = 0,25)."""
    base = replace(base, **stationnaire.ENTREES_D_ORIGINE)
    for pi, na, publie in ((0.02, 4, "0,25237"), (0.02, 52, "0,25844"), (0.0, 4, "0,09466"), (0.10, 4, "0,49978"),
                           (0.0, 52, "0,10045"), (0.10, 52, "0,51438")):
        p = replace(base, pi_cible=pi, n_a=na, sigma=1.4 / na)
        v = stationnaire.valeurs(stationnaire.etat_stationnaire(p), p)
        assert stationnaire.comparer(publie, v["dette_consolidee"])[2], (na, v["dette_consolidee"])


def test_explication_Y_HS_par_T_H_arrondi(stationnaire, base):
    """Y^HS/PIB publié à 2 % = T_H/PIB arrondi au centième de point ÷ τ_H : 21,68 %/0,25 = 0,8672, sous les entrées
    d'origine (μ̄ = 0,25)."""
    base = replace(base, **stationnaire.ENTREES_D_ORIGINE)
    v = stationnaire.valeurs(stationnaire.etat_stationnaire(base), base)
    assert stationnaire.comparer("0,8672", round(v["T_H_sur_PIB"], 2) / 100 / base.tau_H)[2]
    assert not stationnaire.comparer("0,8672", v["Y_HS"])[2]


def test_explication_marge_J_nu_sur_G_PB_a_nu_G_un(stationnaire, base):
    """« 0,37 % » à ν_G = 1,1, π̄ = 0 : marge J-ν calculée sur G/PB à ν_G = 1, non à ν_G = 1,1, sous les entrées
    d'origine (μ̄ = 0,25, ϑ = 0,10)."""
    p1 = replace(base, pi_cible=0.0, **stationnaire.ENTREES_D_ORIGINE)
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


# Calibration du socle (M34) : valeurs republiées au rang 9 (`docwriter`, commits 9cb6ab9 à 1f86f0a), liste exacte
# des clés (section, grandeur), chacune avec son ancienne valeur, figée en littéral et barrée dans sa source. Ces 310
# valeurs étaient publiées à l'état E0 (μ̄ = 0,25, ϑ = 0,10, ν_H = 1), et à ζ = 4 (`ENTREES_D_ORIGINE`) ; la table T1
# les a déplacées au-delà de leur dernière décimale publiée. Toute autre valeur en vigueur est inchangée. Une
# ancienne valeur ne se modifie pas sans échec (`test_contre_epreuve_des_valeurs_republiees_sous_les_entrees_d_origine`,
# `test_anciennes_valeurs_de_M34_barrees_dans_leur_source`).
#
# #55 (ζ = 4 → 8) : les 12 valeurs de la mesure (α) de #80 (lecture (α), Δϱ ≠ 0 entre deux cibles) ; l'état
# stationnaire de référence ne lit pas ζ (Δϱ = 0).
ANCIENNES_M34_55 = {
    ("sec:banque_centrale-conditions", "(α) : écart de C/Y_o, point"): "0,633",
    ("sec:banque_centrale-conditions", "(α) : écart de ti, point"): "0,186",
    ("sec:banque_centrale-conditions", "marche de cible de 2 à 3 %, point"): "-0,18",
    ("sec:banque_centrale-conditions", "r̄_α(0) − r̄_α(10 %), point"): "0,486",
    ("sec:banque_centrale-conditions", "écart maximal de r̄_α sur le profil, point"): "0,976",
    ("sec:banque_centrale-conditions", "Δr̄_α, verdict (ζ = 8), point"): "0,632",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 0 %, %"): "1,632",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 1 %, %"): "1,264",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 10 %, %"): "1,146",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 3 %, %"): "0,818",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 4 %, %"): "0,706",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 6 %, %"): "0,656",
}
# #92 (μ̄ = 0,25 → 0,60) : 173 valeurs, dont T_H, YD^HS et Y^HS sur le PIB à π̄ = 0, qui retombaient sur la décimale
# publiée sous ϑ = 0,15 (#130) et en sortent sous ν_H = 1,1 (#62).
ANCIENNES_M34_92 = {
    ("fiche 9 § 3.C", "(α) : C/PIB à 0 % moins à 2 %, point"): "0,487",
    ("fiche 9 § 3.C", "(α) : C/PIB à 10 % moins à 2 %, point"): "-0,434",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 0 %, n_a = 4"): "0,09880",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 0 %, n_a = 52"): "0,09886",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 10 %, n_a = 4"): "0,51172",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 10 %, n_a = 52"): "0,50952",
    ("fiche 9 § 6.3", "(α) : max − min de C/PIB, point"): "0,921",
    ("sec:banque-conditions", "déficit de Domar dû à E^Bk à 10 %, % du PIB"): "0,387",
    ("sec:banque-restitution", "masse monétaire restitué(e) à 10 %"): "0,86279",
    ("sec:banque-restitution", "masse monétaire restitué(e) à 2 %"): "0,83423",
    ("sec:banque-restitution", "refinancement restitué(e) à 10 %"): "0,02800",
    ("sec:banque-restitution", "refinancement restitué(e) à 2 %"): "0,02222",
    ("sec:banque-restitution", "titres de la banque restitué(e) à 10 %"): "0,57066",
    ("sec:banque-restitution", "titres de la banque restitué(e) à 2 %"): "0,28451",
    ("sec:banque-stationnaire", "crédits à 0 %"): "0,80037",
    ("sec:banque-stationnaire", "crédits à 10 %"): "0,33439",
    ("sec:banque-stationnaire", "crédits à 2 %"): "0,62204",
    ("sec:banque-stationnaire", "crédits à 2 %, n_a = 12"): "0,622039",
    ("sec:banque-stationnaire", "crédits à 2 %, n_a = 4"): "0,621423",
    ("sec:banque-stationnaire", "crédits à 2 %, n_a = 52"): "0,622275",
    ("sec:banque-stationnaire", "dette consolidée c à 0 %"): "0,09884",
    ("sec:banque-stationnaire", "dette consolidée c à 10 %"): "0,51013",
    ("sec:banque-stationnaire", "dette consolidée c à 2 %"): "0,25674",
    ("sec:banque-stationnaire", "dette consolidée de 2 à 10 %"): "0,25339",
    ("sec:banque-stationnaire", "dont fonds propres (ϑ Δl), 2 à 10 %"): "-0,0288",
    ("sec:banque-stationnaire", "dont richesse des ménages, 2 à 10 %"): "-0,0044",
    ("sec:banque-stationnaire", "dépôts des entreprises à 0 %"): "0,16636",
    ("sec:banque-stationnaire", "e_Bk à 0 %"): "0,08004",
    ("sec:banque-stationnaire", "e_Bk à 10 %"): "0,03344",
    ("sec:banque-stationnaire", "e_Bk à 2 %"): "0,06220",
    ("sec:banque-stationnaire", "masse monétaire M à 0 %"): "0,81917",
    ("sec:banque-stationnaire", "masse monétaire M à 10 %"): "0,81108",
    ("sec:banque-stationnaire", "masse monétaire M à 2 %"): "0,81658",
    ("sec:banque-stationnaire", "refinancement à 0 %, ν_G = 1"): "0,018282",
    ("sec:banque-stationnaire", "refinancement à 0 %, ν_G = 1,15"): "0,021027",
    ("sec:banque-stationnaire", "refinancement à 10 %, ν_G = 1"): "0,022857",
    ("sec:banque-stationnaire", "refinancement à 10 %, ν_G = 1,15"): "0,026322",
    ("sec:banque-stationnaire", "refinancement à 2 %, ν_G = 1"): "0,018904",
    ("sec:banque-stationnaire", "refinancement à 2 %, ν_G = 1,15"): "0,021748",
    ("sec:banque-stationnaire", "richesse des ménages à 2 %"): "0,6505",
    ("sec:banque-stationnaire", "résultat Π^Bk/PIB à 0 %"): "0,02500",
    ("sec:banque-stationnaire", "résultat Π^Bk/PIB à 10 %"): "0,01851",
    ("sec:banque-stationnaire", "résultat Π^Bk/PIB à 2 %"): "0,02249",
    ("sec:banque-stationnaire", "titres de 2 à 10 %, ν_G = 1"): "0,25734",
    ("sec:banque-stationnaire", "titres de 2 à 10 %, ν_G = 1,15"): "0,25797",
    ("sec:banque-stationnaire", "titres de la banque à 0 %, ν_G = 1"): "0,11712",
    ("sec:banque-stationnaire", "titres de la banque à 0 %, ν_G = 1,15"): "0,11987",
    ("sec:banque-stationnaire", "titres de la banque à 10 %, ν_G = 1"): "0,53299",
    ("sec:banque-stationnaire", "titres de la banque à 10 %, ν_G = 1,15"): "0,53645",
    ("sec:banque-stationnaire", "titres de la banque à 2 %, ν_G = 1"): "0,27564",
    ("sec:banque-stationnaire", "titres de la banque à 2 %, ν_G = 1,15"): "0,27849",
    ("sec:banque_centrale-restitution", "refinancement restitué à 0 %"): "0,02125",
    ("sec:banque_centrale-restitution", "refinancement restitué à 10 %"): "0,02800",
    ("sec:banque_centrale-restitution", "refinancement restitué à 2 %"): "0,02222",
    ("sec:banque_centrale-restitution", "résultat de la banque centrale à 10 %, ν_G = 1, % du PIB"): "0,2537",
    ("sec:banque_centrale-restitution", "résultat de la banque centrale à 10 %, ν_G = 1,15, % du PIB"): "0,2922",
    ("sec:finances_publiques-impots", "dette consolidée, 10 % moins 2 %"): "0,253",
    ("sec:finances_publiques-restitution", "charge brute à 10 %, ν_G = 1,15, % du PIB"): "5,9546",
    ("sec:finances_publiques-restitution", "charge brute à 2 %, ν_G = 1,15, % du PIB"): "0,8410",
    ("sec:finances_publiques-restitution", "dette brute affichée à 10 %, ν_G = 1,15, % du PIB"): "57,1",
    ("sec:finances_publiques-stationnaire", "G/PIB à 0 %, %"): "21,86",
    ("sec:finances_publiques-stationnaire", "G/PIB à 10 %, %"): "21,78",
    ("sec:finances_publiques-stationnaire", "G/PIB à 2 %, %"): "21,93",
    ("sec:finances_publiques-stationnaire", "T_H/PIB à 0 %, %"): "21,76",
    ("sec:finances_publiques-stationnaire", "T_H/PIB à 10 %, %"): "21,54",
    ("sec:finances_publiques-stationnaire", "T_H/PIB à 2 %, %"): "21,68",
    ("sec:finances_publiques-stationnaire", "YD^HS/PIB à 0 %"): "0,6528",
    ("sec:finances_publiques-stationnaire", "YD^HS/PIB à 10 %"): "0,6462",
    ("sec:finances_publiques-stationnaire", "YD^HS/PIB à 2 %"): "0,6505",
    ("sec:finances_publiques-stationnaire", "Y^HS/PIB à 0 %"): "0,8704",
    ("sec:finances_publiques-stationnaire", "Y^HS/PIB à 10 %"): "0,8616",
    ("sec:finances_publiques-stationnaire", "Y^HS/PIB à 2 %"): "0,8674",
    ("sec:finances_publiques-stationnaire", "dette brute à 0 %"): "0,11712",
    ("sec:finances_publiques-stationnaire", "dette brute à 0 %, ν_G = 1,15"): "0,11987",
    ("sec:finances_publiques-stationnaire", "dette brute à 10 %"): "0,53299",
    ("sec:finances_publiques-stationnaire", "dette brute à 10 %, ν_G = 1,15"): "0,53645",
    ("sec:finances_publiques-stationnaire", "dette brute à 2 %"): "0,27564",
    ("sec:finances_publiques-stationnaire", "dette brute à 2 %, ν_G = 1,15"): "0,27849",
    ("sec:finances_publiques-stationnaire", "dette consolidée à 0 %"): "0,09884",
    ("sec:finances_publiques-stationnaire", "dette consolidée à 10 %"): "0,51013",
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %"): "0,25674",
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, n_a = 4"): "0,25726",
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, n_a = 52"): "0,25654",
    ("sec:finances_publiques-stationnaire", "décomposition à 2 % : fonds propres de la banque"): "0,0622",
    ("sec:finances_publiques-stationnaire", "décomposition à 2 % : richesse des ménages"): "0,6505",
    ("sec:finances_publiques-stationnaire", "décomposition à 2 % : somme"): "0,2567",
    ("sec:finances_publiques-stationnaire", "décomposition à 2 % : −crédits nets"): "-0,4560",
    ("sec:finances_publiques-stationnaire", "déficit de Domar à 0 %, % du PIB"): "0,1959",
    ("sec:finances_publiques-stationnaire", "déficit de Domar à 10 %, % du PIB"): "5,9005",
    ("sec:finances_publiques-stationnaire", "déficit de Domar à 2 %, % du PIB"): "1,0185",
    ("sec:finances_publiques-stationnaire", "encaisse à 0 %"): "0,018282",
    ("sec:finances_publiques-stationnaire", "encaisse à 0 %, ν_G = 1,15"): "0,021027",
    ("sec:finances_publiques-stationnaire", "encaisse à 10 %"): "0,022857",
    ("sec:finances_publiques-stationnaire", "encaisse à 10 %, ν_G = 1,15"): "0,026322",
    ("sec:finances_publiques-stationnaire", "encaisse à 2 %"): "0,018904",
    ("sec:finances_publiques-stationnaire", "encaisse à 2 %, ν_G = 1,15"): "0,021748",
    ("sec:finances_publiques-stationnaire", "intérêts bruts à 0 %, % du PIB"): "0,1171",
    ("sec:finances_publiques-stationnaire", "intérêts bruts à 10 %, % du PIB"): "5,9162",
    ("sec:finances_publiques-stationnaire", "intérêts bruts à 10 %, ν_G = 1,15, % du PIB"): "5,9546",
    ("sec:finances_publiques-stationnaire", "intérêts bruts à 2 %, % du PIB"): "0,8324",
    ("sec:finances_publiques-stationnaire", "intérêts bruts à 2 %, ν_G = 1,15, % du PIB"): "0,8410",
    ("sec:finances_publiques-stationnaire", "intérêts nets à 0 %, % du PIB"): "0,0988",
    ("sec:finances_publiques-stationnaire", "intérêts nets à 10 %, % du PIB"): "5,6625",
    ("sec:finances_publiques-stationnaire", "intérêts nets à 2 %, % du PIB"): "0,7754",
    ("sec:finances_publiques-stationnaire", "solde primaire à 10 %, % du PIB"): "-0,2381",
    ("sec:finances_publiques-stationnaire", "solde primaire à 2 %, % du PIB"): "-0,2432",
    ("sec:finances_publiques-transferts", "impôt des ménages à 2 %, % du PIB"): "21,68",
    ("sec:investissement-stationnaire", "I/PIB à 10 % (C-F), %"): "13,849",
    ("sec:investissement-stationnaire", "I/PIB à 2 % (C-F), %"): "13,945",
    ("sec:investissement-stationnaire", "I/PIB, n_a = 4 (C-F), %"): "13,951",
    ("sec:investissement-stationnaire", "I/PIB, n_a = 52 (C-F), %"): "13,942",
    ("sec:investissement-stationnaire", "capital au prix courant à 10 % (C-F)"): "1,98361",
    ("sec:investissement-stationnaire", "capital au prix courant à 2 % (C-F)"): "1,99726",
    ("sec:investissement-stationnaire", "capital comptable à 10 % (C-F)"): "0,83598",
    ("sec:investissement-stationnaire", "capital comptable à 2 % (C-F)"): "1,55510",
    ("sec:investissement-stationnaire", "capital comptable, n_a = 4 (C-F)"): "1,55356",
    ("sec:investissement-stationnaire", "capital comptable, n_a = 52 (C-F)"): "1,55569",
    ("sec:investissement-stationnaire", "crédits nets à 10 % (C-F)"): "0,16947",
    ("sec:investissement-stationnaire", "crédits nets à 2 % (C-F)"): "0,45598",
    ("sec:investissement-stationnaire", "crédits à 10 % (C-F)"): "0,33439",
    ("sec:investissement-stationnaire", "crédits à 2 % (C-F)"): "0,62204",
    ("sec:investissement-stationnaire", "distribution à 10 % (C-F)"): "0,39995",
    ("sec:investissement-stationnaire", "distribution à 10 % (R)"): "0,36359",
    ("sec:investissement-stationnaire", "distribution à 2 % (C-F)"): "0,56853",
    ("sec:investissement-stationnaire", "distribution à 2 % (R)"): "0,50480",
    ("sec:investissement-stationnaire", "distribution, n_a = 4 (C-F)"): "0,56791",
    ("sec:investissement-stationnaire", "distribution, n_a = 52 (C-F)"): "0,56876",
    ("sec:investissement-stationnaire", "dividendes/ventes à 10 % (C-F), %"): "5,90",
    ("sec:investissement-stationnaire", "dividendes/ventes à 10 % (R), %"): "5,06",
    ("sec:investissement-stationnaire", "dividendes/ventes à 2 % (C-F), %"): "6,25",
    ("sec:investissement-stationnaire", "dividendes/ventes à 2 % (R), %"): "4,84",
    ("sec:investissement-stationnaire", "dépôts à 10 % (C-F)"): "0,16492",
    ("sec:investissement-stationnaire", "dépôts à 2 % (C-F)"): "0,16605",
    ("sec:investissement-stationnaire", "valeur nette des entreprises à 10 % (C-F)"): "0,75713",
    ("sec:investissement-stationnaire", "valeur nette des entreprises à 2 % (C-F)"): "1,19174",
    ("sec:prix-stationnaire", "part salariale à 10 %, n_a = 12"): "0,793445",
    ("sec:prix-stationnaire", "part salariale à 10 %, n_a = 4"): "0,793499",
    ("sec:prix-stationnaire", "part salariale à 10 %, n_a = 52"): "0,793424",
    ("sec:travail-stationnaire", "part salariale à 2 %, n_a = 12"): "0,798903",
    ("sec:travail-stationnaire", "part salariale à 2 %, n_a = 4"): "0,798906",
    ("sec:travail-stationnaire", "part salariale à 2 %, n_a = 52"): "0,798902",
    ("sec:travail-stationnaire", "écart à ω̄ à 10 %, point"): "0,656",
    ("sec:travail-stationnaire", "écart à ω̄ à 2 %, point"): "0,110",
    ("tab:etat-stationnaire", "capital sur production (b), au prix courant à 0 %"): "2,0009",
    ("tab:etat-stationnaire", "capital sur production (b), au prix courant à 10 %"): "1,9836",
    ("tab:etat-stationnaire", "capital sur production (b), au prix courant à 2 %"): "1,9973",
    ("tab:etat-stationnaire", "capital sur production (c), comptable à 0 %"): "2,0009",
    ("tab:etat-stationnaire", "capital sur production (c), comptable à 10 %"): "0,8360",
    ("tab:etat-stationnaire", "capital sur production (c), comptable à 2 %"): "1,5551",
    ("tab:etat-stationnaire", "dette brute affichée, % du PIB à 10 %"): "57,1",
    ("tab:etat-stationnaire", "dette brute à 0 %"): "0,11987",
    ("tab:etat-stationnaire", "dette brute à 10 %"): "0,53645",
    ("tab:etat-stationnaire", "dette brute à 2 %"): "0,27849",
    ("tab:etat-stationnaire", "dette brute, ν_G = 1 à 0 %"): "0,11712",
    ("tab:etat-stationnaire", "dette brute, ν_G = 1 à 10 %"): "0,53299",
    ("tab:etat-stationnaire", "dette brute, ν_G = 1 à 2 %"): "0,27564",
    ("tab:etat-stationnaire", "dette consolidée à 0 %"): "0,09884",
    ("tab:etat-stationnaire", "dette consolidée à 10 %"): "0,51013",
    ("tab:etat-stationnaire", "dette consolidée à 2 %"): "0,25674",
    ("tab:etat-stationnaire", "déficit public (Domar), % du PIB à 0 %"): "0,1959",
    ("tab:etat-stationnaire", "déficit public (Domar), % du PIB à 10 %"): "5,9005",
    ("tab:etat-stationnaire", "déficit public (Domar), % du PIB à 2 %"): "1,0185",
    ("tab:etat-stationnaire", "masse monétaire à 0 %"): "0,81917",
    ("tab:etat-stationnaire", "masse monétaire à 10 %"): "0,81108",
    ("tab:etat-stationnaire", "masse monétaire à 2 %"): "0,81658",
    ("tab:etat-stationnaire", "part salariale à 0 %"): "0,80037",
    ("tab:etat-stationnaire", "part salariale à 10 %"): "0,79344",
    ("tab:etat-stationnaire", "part salariale à 2 %"): "0,79890",
    ("tab:etat-stationnaire", "solde primaire, % du PIB à 10 %"): "-0,2381",
    ("tab:etat-stationnaire", "solde primaire, % du PIB à 2 %"): "-0,2432",
    ("tab:etat-stationnaire", "taux d'investissement, % à 0 %"): "13,970",
    ("tab:etat-stationnaire", "taux d'investissement, % à 10 %"): "13,849",
    ("tab:etat-stationnaire", "taux d'investissement, % à 2 %"): "13,945",
}
# #130 (ϑ = 0,10 → 0,15) : 101 valeurs de l'effet (ϑ) (E^Bk = ϑL, dette consolidée par C42, θ_G résolu, résultat et
# rendement de la banque ; Δr̄_α par θ_G, dont son minimum en ζ, ligne de #173 contrôlée contre son ancienne valeur
# barrée) ; ϖ_L, ϖ_D et r̄ sont inchangés. Deux autres (θ_G(r̄ + 1 point) − θ_G(r̄),
# φ = 1, à ζ = 4 et 8 : « +0,308 » et « +0,157 ») s'écartaient sous ϑ = 0,15 et retombent sur leur décimale publiée
# sous ν_H = 1,1 : en vigueur inchangées, elles ne figurent pas ici.
ANCIENNES_M34_130 = {
    ("fiche 8 § 9.6", "r̄_α(3 %) à ζ = 8, %"): "0,9188",
    ("fiche 9 § 6.3", "(β) : écart de θ_G entre 0, 2 et 10 %, point"): "0,110",
    ("sec:banque-conditions", "(d2), 2 %, point"): "1,26",
    ("sec:banque-conditions", "couplage −ϑ lv*"): "-0,04",
    ("sec:banque-conditions", "déficit de Domar dû à E^Bk à 0 %, % du PIB"): "0,159",
    ("sec:banque-conditions", "déficit de Domar dû à E^Bk à 2 %, % du PIB"): "0,247",
    ("sec:banque-resultat", "saut C29 au tour n, 2 %, %"): "11,42",
    ("sec:banque-resultat", "saut C29 ensuite, 2 %, %"): "2,77",
    ("sec:banque-stationnaire", "canal rentier, % de YD par point à 0 %"): "0,151",
    ("sec:banque-stationnaire", "canal rentier, % de YD par point à 10 %"): "0,721",
    ("sec:banque-stationnaire", "canal rentier, % de YD par point à 2 %"): "0,387",
    ("sec:banque-stationnaire", "condition d'existence à écarts nuls, 2 %"): "-0,000947",
    ("sec:banque-stationnaire", "encaisse de 2 à 10 %, ν_G = 1"): "0,0040",
    ("sec:banque-stationnaire", "encaisse de 2 à 10 %, ν_G = 1,15"): "0,0046",
    ("sec:banque-stationnaire", "marge d'existence, par an à 0 %"): "0,0293",
    ("sec:banque-stationnaire", "marge d'existence, par an à 10 %"): "0,0438",
    ("sec:banque-stationnaire", "marge d'existence, par an à 2 %"): "0,0322",
    ("sec:banque-stationnaire", "marge nette d'intérêt (Π^Bk/actif), % à 0 %, ν_G = 1"): "2,725",
    ("sec:banque-stationnaire", "marge nette d'intérêt (Π^Bk/actif), % à 0 %, ν_G = 1,15"): "2,717",
    ("sec:banque-stationnaire", "marge nette d'intérêt (Π^Bk/actif), % à 10 %, ν_G = 1"): "2,134",
    ("sec:banque-stationnaire", "marge nette d'intérêt (Π^Bk/actif), % à 10 %, ν_G = 1,15"): "2,126",
    ("sec:banque-stationnaire", "marge nette d'intérêt (Π^Bk/actif), % à 2 %, ν_G = 1"): "2,505",
    ("sec:banque-stationnaire", "marge nette d'intérêt (Π^Bk/actif), % à 2 %, ν_G = 1,15"): "2,497",
    ("sec:banque-stationnaire", "part des dividendes des entreprises, 2 %, %"): "-177,6",
    ("sec:banque-stationnaire", "part des intérêts des dépôts, 2 %, %"): "253,4",
    ("sec:banque-stationnaire", "part des titres dans l'actif à 0 %, ν_G = 1"): "0,1277",
    ("sec:banque-stationnaire", "part des titres dans l'actif à 0 %, ν_G = 1,15"): "0,1303",
    ("sec:banque-stationnaire", "part des titres dans l'actif à 10 %, ν_G = 1"): "0,6145",
    ("sec:banque-stationnaire", "part des titres dans l'actif à 10 %, ν_G = 1,15"): "0,6160",
    ("sec:banque-stationnaire", "part des titres dans l'actif à 2 %, ν_G = 1"): "0,3071",
    ("sec:banque-stationnaire", "part des titres dans l'actif à 2 %, ν_G = 1,15"): "0,3093",
    ("sec:banque-stationnaire", "part distribuée à 0 %"): "0,93655",
    ("sec:banque-stationnaire", "part distribuée à 10 %"): "0,79105",
    ("sec:banque-stationnaire", "part distribuée à 2 %"): "0,89025",
    ("sec:banque-stationnaire", "part distribuée à 2 %, n_a = 12"): "0,890253",
    ("sec:banque-stationnaire", "part distribuée à 2 %, n_a = 4"): "0,889928",
    ("sec:banque-stationnaire", "part distribuée à 2 %, n_a = 52"): "0,890378",
    ("sec:banque-stationnaire", "part du dividende de la banque, 2 %, %"): "24,2",
    ("sec:banque-stationnaire", "rendement des fonds propres (brut, nominal, sans charges), % à 0 %"): "31,23",
    ("sec:banque-stationnaire", "rendement des fonds propres (brut, nominal, sans charges), % à 10 %"): "55,36",
    ("sec:banque-stationnaire", "rendement des fonds propres (brut, nominal, sans charges), % à 2 %"): "36,15",
    ("sec:banque-stationnaire", "rendement des fonds propres (brut, nominal, sans charges), variante basse, 0 %, %"): "7,19",
    ("sec:banque-stationnaire", "rendement des fonds propres (brut, nominal, sans charges), variante basse, 10 %, %"): "20,29",
    ("sec:banque-stationnaire", "rendement des fonds propres (brut, nominal, sans charges), variante basse, 2 %, %"): "9,83",
    ("sec:banque_centrale-conditions", "(α) : écart de tu, point"): "2,178",
    ("sec:banque_centrale-conditions", "marche de cible de 2 à 3 % à ζ = 2, point"): "-0,38",
    ("sec:banque_centrale-conditions", "marche de cible de 2 à 3 % à ζ = 8, point"): "-0,08",
    # Les deux clés Δr̄_α suivantes dépendent à la fois de #130 (ϑ) et de #62 (ν_H) : 0,1428 n'est retrouvé qu'avec
    # les deux ensemble (mesuré à la reprise de #173 : à ζ = 68, 0,152557 sous ϑ = 0,10 seul, 0,151300 sous ν_H = 1
    # seul, 0,142804 sous les deux ; au point anguleux, 0,152196, 0,149586 et 0,142803). Rangées avec #130 (accord de
    # `monnaie`).
    ("sec:banque_centrale-conditions", "Δr̄_α à ζ = 68, point"): "0,1428",
    ("sec:banque_centrale-conditions", "Δr̄_α au minimum en ζ sur [2 ; 200], point"): "0,1428",
    ("sec:banque_centrale-conditions", "Δr̄_α à ζ = 2, point"): "1,304",
    ("sec:banque_centrale-conditions", "Δr̄_α à ζ = 8, point"): "0,297",
    ("sec:banque_centrale-conditions ; fiche 8 § 9.6", "r̄_α(3 %) à ζ = 4, %"): "0,8185",
    ("sec:banque_centrale-restitution", "résultat de la banque centrale à 0 %, ν_G = 1,15, % du PIB"): "0,0210",
    ("sec:banque_centrale-restitution", "résultat de la banque centrale à 2 %, ν_G = 1, % du PIB"): "0,0571",
    ("sec:banque_centrale-restitution", "résultat de la banque centrale à 2 %, ν_G = 1,15, % du PIB"): "0,0657",
    ("sec:banque_centrale-stationnaire", "L^CB_0 à 2 %, ν_G = 1,15, u.m."): "0,248264",
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̂, norme et i^ref tenus, φ = 0, ζ = 4, point par point"): "-0,034",
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̂, norme et i^ref tenus, φ = 0, ζ = 8, point par point"): "0,127",
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̂, norme et i^ref tenus, φ = 1, ζ = 8, point par point"): "0,321",
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̄ à 0 %, point par point"): "-0,073",
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̄ à 10 %, point par point"): "-0,421",
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̄, % de la production par point de r̄"): "-0,194",
    ("sec:banque_centrale-stationnaire", "points de r̄ par point de PIB de dépense"): "-5,15",
    ("sec:banque_centrale-stationnaire", "θ_G(r̄ + 1 point) − θ_G(r̄), norme et i^ref tenus, φ = 0, ζ = 4, point"): "-0,058",
    ("sec:banque_centrale-stationnaire", "θ_G(r̄ + 1 point) − θ_G(r̄), norme et i^ref tenus, φ = 0, ζ = 8, point"): "+0,074",
    ("sec:finances_publiques-depense", "G/PB à 0 %"): "0,99467",
    ("sec:finances_publiques-depense", "G/PB à 10 %"): "0,78637",
    ("sec:finances_publiques-depense", "G/PB à 2 %"): "0,96342",
    ("sec:finances_publiques-depense", "hausse admissible à 0 %, ν_G = 1, %"): "0,37",
    ("sec:finances_publiques-depense", "marge de E1 à 0 %"): "0,0037",
    ("sec:finances_publiques-depense", "marge de E1 à 10 %"): "0,2061",
    ("sec:finances_publiques-depense", "marge de E1 à 2 %"): "0,0334",
    ("sec:finances_publiques-emission", "borne de ν_G à 0 %"): "1,0959",
    ("sec:finances_publiques-emission", "borne de ν_G à 10 %"): "0,8733",
    ("sec:finances_publiques-emission", "borne de ν_G à 2 %"): "1,0633",
    ("sec:finances_publiques-emission", "hausse admissible à 0 %, ν_G = 1,15, %"): "15,44",
    ("sec:finances_publiques-emission", "hausse admissible à 10 %, ν_G = 1,15, %"): "45,05",
    ("sec:finances_publiques-emission", "hausse admissible à 2 %, ν_G = 1,15, %"): "19,02",
    ("sec:finances_publiques-emission", "marge J-ν au pire point à ν_G = 1,1, %"): "0,23",
    ("sec:finances_publiques-emission", "retour après −5 % (approché), 0 %"): "1,0485",
    ("sec:finances_publiques-emission", "ν_G,min au pire point (n_a = 4, 0 %)"): "1,0975",
    ("sec:finances_publiques-emission", "ν_G,min exact à 0 %"): "1,0959",
    ("sec:finances_publiques-emission", "ν_G,min exact à 10 %"): "0,8744",
    ("sec:finances_publiques-emission", "ν_G,min exact à 2 %"): "1,0631",
    ("sec:finances_publiques-emission ; tab:calibration", "marge J-ν au pire point à ν_G = 1,15"): "0,0458",
    ("sec:finances_publiques-emission ; tab:calibration", "marge J-ν à ν_G = 1,1, 0 %, %"): "0,38",
    ("sec:finances_publiques-emission ; tab:calibration", "ν_G minimal pour la marge J-ν (n_a = 4, 0 %)"): "1,1313",
    ("sec:finances_publiques-restitution", "dette brute affichée à 2 %, ν_G = 1,15, % du PIB"): "28,5",
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, arrondie"): "0,257",
    ("sec:finances_publiques-stationnaire", "intérêts bruts à 0 %, ν_G = 1,15, % du PIB"): "0,1199",
    ("sec:finances_publiques-stationnaire", "solde primaire à 0 %, % du PIB"): "-0,0971",
    ("sec:finances_publiques-stationnaire", "θ_G à 0 %"): "0,218474",
    ("sec:finances_publiques-stationnaire", "θ_G à 10 %"): "0,219568",
    ("sec:finances_publiques-stationnaire", "θ_G à 2 %"): "0,219573",
    ("sec:finances_publiques-transferts", "charge brute à 2 %, ν_G = 1,15, % du PIB"): "0,84",
    ("tab:etat-stationnaire", "dette brute affichée, % du PIB à 0 %"): "12,1",
    ("tab:etat-stationnaire", "dette brute affichée, % du PIB à 2 %"): "28,5",
    ("tab:etat-stationnaire", "part de la dépense publique θ_G à 0 %"): "0,218474",
    ("tab:etat-stationnaire", "part de la dépense publique θ_G à 10 %"): "0,219568",
    ("tab:etat-stationnaire", "part de la dépense publique θ_G à 2 %"): "0,219573",
    ("tab:etat-stationnaire", "solde primaire, % du PIB à 0 %"): "-0,0971",
}
# #62 (ν_H = 1 → 1,1, λ_H inchangé) : 24 valeurs de l'effet (ν) (D_H monte de 10,09 % à 2 % ; C42 : ΔD_c = ΔD_H ;
# θ_G résolu monte) ou des ménages (V_H/(n_a YD) = ν_H/(1 + ν_H n_a π^{∗,pas}), épargne et C/YD).
ANCIENNES_M34_62 = {
    ("sec:banque-stationnaire", "impôt d'inflation net à 10 %, %"): "-0,485",
    ("sec:banque-stationnaire", "impôt d'inflation net à 2 %, %"): "-0,037",
    ("sec:banque_centrale-restitution", "résultat de la banque centrale à 0 %, ν_G = 1, % du PIB"): "0,0183",
    ("sec:finances_publiques-caisse", "dépôts des ménages / impôt du mois, environ"): "36",
    ("sec:menages-stationnaire", "C/YD à 10 %"): "0,8944",
    ("sec:menages-stationnaire", "C/YD à 2 %"): "0,96110",
    ("sec:menages-stationnaire", "V_H/(n_a YD) à 10 %"): "0,912667",
    ("sec:menages-stationnaire", "V_H/(n_a YD) à 10 %, n_a = 4"): "0,912030",
    ("sec:menages-stationnaire", "V_H/(n_a YD) à 10 %, n_a = 52"): "0,912911",
    ("sec:menages-stationnaire", "V_H/(n_a YD) à 2 %"): "0,980566",
    ("sec:menages-stationnaire", "V_H/(n_a YD) à 2 %, n_a = 4"): "0,980535",
    ("sec:menages-stationnaire", "V_H/(n_a YD) à 2 %, n_a = 52"): "0,980578",
    ("sec:menages-stationnaire", "V_H_0/YD_0 à 2 %"): "11,7668",
    ("sec:menages-stationnaire", "dont maintien à 10 %, point"): "8,7333",
    ("sec:menages-stationnaire", "dont maintien à 2 %, point"): "1,9434",
    ("sec:menages-stationnaire", "dont épargne réelle à 10 %, point"): "1,8232",
    ("sec:menages-stationnaire", "dont épargne réelle à 2 %, point"): "1,9466",
    ("sec:menages-stationnaire", "marge du plafond à 2 %, mois"): "12,24",
    ("sec:menages-stationnaire", "taux d'épargne à 10 %, %"): "10,5565",
    ("sec:menages-stationnaire", "taux d'épargne à 2 %, %"): "3,8900",
    ("sec:menages-stationnaire", "épargne visée à 10 %, %"): "1,9977",
    ("sec:menages-stationnaire", "épargne visée à 2 %, %"): "1,9852",
    ("sec:menages-stationnaire", "épargne visée à 2 %, n_a = 4, %"): "1,9950",
    ("sec:menages-stationnaire", "épargne visée à 2 %, n_a = 52, %"): "1,9814",
}
ANCIENNES_M34 = ANCIENNES_M34_55 | ANCIENNES_M34_92 | ANCIENNES_M34_130 | ANCIENNES_M34_62


def test_valeurs_publiees_toutes_egales(stationnaire, resultat):
    """Valeurs en vigueur (spécification et fiches 8 et 9, republiées à la table T1 de M34 au rang 9) : toutes égales
    à la dernière décimale publiée, sans exception ; aucune valeur barrée n'y figure (catégories B-1 et N en
    contre-épreuve)."""
    lignes = resultat["publiees"]
    assert len(lignes) == 450
    assert {l["categorie"] for l in lignes} == {"A", "S", "B-2", "D"}
    assert sum(1 for l in lignes if l["categorie"] == "S") == 20
    assert [l for l in lignes if l["verdict"] != "égal"] == []
    for l in lignes:
        if l["publie"] == stationnaire.AUCUNE:
            assert math.isnan(l["script"]), l
        else:
            assert abs(l["ecart"]) <= l["seuil"], l


def test_contre_epreuve_des_valeurs_republiees_sous_les_entrees_d_origine(stationnaire, base):
    """R3 de l'audit de #130, après la republication du rang 9 : les 310 anciennes valeurs (`ANCIENNES_M34`), mises à
    la place des valeurs en vigueur, sont égales à la dernière décimale publiée sous `ENTREES_D_ORIGINE` complètes
    (état E0, ζ = 4, valeur des publications de la mesure (α) de #80, et λ_w = 1 ; ni ζ ni λ_w n'entrent dans l'état
    stationnaire) : chaque republication s'explique par un paramètre déclaré de M34. À ζ = 8 (T1), seules les 12 de
    #55 restent en écart ; λ_w seul ne déplace aucune des 450 valeurs. Sous `ENTREES_D_ORIGINE`, les valeurs en
    vigueur sont en écart exactement sur les 310 clés : une valeur republiée ne retombe pas sur sa décimale à l'état
    E0, une valeur non republiée ne dépend pas de M34."""
    en_vigueur = {(section, grandeur): publie for section, grandeur, publie, _, _ in stationnaire.VALEURS_PUBLIEES}
    assert (len(ANCIENNES_M34_55), len(ANCIENNES_M34_92), len(ANCIENNES_M34_130), len(ANCIENNES_M34_62)) \
        == (12, 173, 101, 24)
    assert len(ANCIENNES_M34) == 310 and set(ANCIENNES_M34) <= set(en_vigueur)
    assert [k for k, ancienne in ANCIENNES_M34.items() if ancienne == en_vigueur[k]] == []
    anciennes = tuple((section, grandeur, ANCIENNES_M34.get((section, grandeur), publie), fonction, categorie)
                      for section, grandeur, publie, fonction, categorie in stationnaire.VALEURS_PUBLIEES)

    def ecarts(liste, **entrees):
        calc = stationnaire.Calculs(replace(base, **entrees), stationnaire.NU_G_RETENU)
        lignes = stationnaire.table_publiees(calc, liste)
        assert len(lignes) == 450
        return {(l["section"], l["grandeur"]) for l in lignes if l["verdict"] != "égal"}
    origine = stationnaire.ENTREES_D_ORIGINE
    assert (origine["zeta"], origine["lambda_w"]) == (4.0, 1.0) and (base.zeta, base.lambda_w) == (8.0, 0.18)
    assert ecarts(anciennes, **origine) == set()
    assert ecarts(anciennes, **{**origine, "zeta": base.zeta}) == set(ANCIENNES_M34_55)
    assert ecarts(anciennes, **{**origine, "lambda_w": base.lambda_w}) == set()
    assert ecarts(stationnaire.VALEURS_PUBLIEES, **origine) == set(ANCIENNES_M34)


def test_valeurs_republiees_toutes_egales(stationnaire, resultat):
    """C4 de `macro` (rang 7) : les 29 valeurs visées et republiées (spécification, commit 8b9fa94 ; fiches 8 et 9)
    sont égales au script ; aucune n'est republiée à son ancienne valeur ; l'historique (commit 9c8bdbd) garde les 29
    anciennes valeurs, toutes en écart, chacune égale à sa valeur figée en littéral (`ANCIENNES_PUBLIEES`)."""
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
    assert ("Bilan : 450 valeurs comparées, 430 égales sur l'état résolu, 20 égales en arithmétique de la "
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
    """`macro` : verdict jugé au ζ de la table (8, M34 ; #55) ; étendue des allocations L2 publiée à ζ ∈ {4 ; 8} et
    à ζ = 2 (illustration) ;
    les allocations dépendantes de ζ (mesurées) sont C/Y_o, ti et T^cou/PIB, exclues des tests d'invariance."""
    assert base.zeta == 8.0 and stationnaire.ZETA_PLAGE == (4.0, 8.0) and stationnaire.ZETA_ILLUSTRATION == 2.0
    sn = resultat["superneutralite"]
    assert set(sn["zeta"]) == {2.0, 4.0, 8.0}
    for q in stationnaire.ALLOCATIONS_VERDICT:  # à ζ du paramètre, l'étendue publiée est celle du verdict
        assert sn["zeta"][8.0]["allocations"][q] == sn["allocations"][q]
    assert sn["dependantes_de_zeta"] == ["C/Y_o", "ti", "T^cou/PIB"]
    assert not set(sn["dependantes_de_zeta"]) & set(ALLOCATIONS_ZETA)
    assert not set(sn["dependantes_de_zeta"]) & {"C/PIB", "G/PIB", "I/PIB", "ΔIN/PIB"}
    tampon = io.StringIO()
    stationnaire.afficher(resultat, tampon)
    texte = tampon.getvalue()
    assert "ζ = 2 (illustration, sans verdict)" in texte and "ζ = 8 (table T1)" in texte
    assert "ζ = 4 (calibration indicative)" in texte
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


@pytest.mark.parametrize("champs", [{"g_N": -1.5}, {"g_pr": -2.0}, {"g_pr": -1.5, "g_N": -1.5}])
def test_facteur_de_croissance_negatif_refuse_avant_la_racine(stationnaire, base, champs, capsys):
    """1 + g_pr ≤ 0 ou 1 + g_N ≤ 0 : refus de domaine (`HorsDomaine`, code de sortie 1), non `TypeError` sur
    le complexe que donnerait la racine n_a-ième d'une base négative ; g_pr = g_N = −1,5, de produit
    (1 + g_pr)(1 + g_N) > 0, compris."""
    with pytest.raises(stationnaire.HorsDomaine, match=r"1 \+ g_(pr|N) > 0"):
        stationnaire.controler_domaine(replace(base, **champs))
    with pytest.raises(stationnaire.HorsDomaine, match=r"1 \+ g_(pr|N) > 0"):
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


# Grille du minimum de Δr̄_α en ζ (#172, point 4 ; #173) : ζ entiers autour de ζ*, puis pas de 5 jusqu'à 200.
DEMI_LARGEUR_ZETA_ENTIERE = 5
PAS_GRILLE_ZETA = 5


def test_minimum_de_delta_r_alpha_en_zeta(stationnaire, base):
    """« Δr̄_α […] atteint sur la grille de ζ mesurée, de 2 à 200, un minimum de 0,160 point (0,1598) vers
    ζ ≈ 63 (0,1614 à ζ = 68, où était le minimum, 0,1428 barré, à la calibration indicative) » : le minimum, point
    anguleux où r̄_α(0) rejoint r̄_α(2 %) (P273), est localisé par `minimum_delta_r_alpha_en_zeta` (bissection sur
    [2 ; 200]) ; sa valeur est égale à 0,1598 à la table T1 et, en contre-épreuve sous `ENTREES_D_ORIGINE`, à
    0,1428 (valeur barrée). Test de position, sans littéral de ζ (#173) : l'argmin sur les ζ entiers mesurés est
    ⌊ζ*⌋ ou ⌈ζ*⌉ ; Δr̄_α(ζ*) est strictement sous Δr̄_α en chaque ζ entier de ⌊ζ*⌋ − `DEMI_LARGEUR_ZETA_ENTIERE` à
    ⌈ζ*⌉ + `DEMI_LARGEUR_ZETA_ENTIERE`, aux multiples de `PAS_GRILLE_ZETA` de 5 à 200, à 2, 200 et 1 000 ; sur ces
    points et ζ*, Δr̄_α décroît strictement jusqu'à ζ*, puis croît strictement (unimodalité, #172, point 4)."""
    for calc, publie in ((stationnaire.Calculs(base), "0,1598"),
                         (stationnaire.Calculs(replace(base, **stationnaire.ENTREES_D_ORIGINE)), "0,1428")):
        zeta_min, delta_min = stationnaire.minimum_delta_r_alpha_en_zeta(calc)
        assert 2.0 < zeta_min < 200.0
        assert stationnaire.comparer(publie, delta_min)[2], (zeta_min, delta_min)
        bas, haut = math.floor(zeta_min), math.ceil(zeta_min)
        entiers = sorted({*range(bas - DEMI_LARGEUR_ZETA_ENTIERE, haut + DEMI_LARGEUR_ZETA_ENTIERE + 1),
                          *range(PAS_GRILLE_ZETA, 201, PAS_GRILLE_ZETA), 2, 200, 1000})
        valeurs = {zeta: stationnaire._delta_r_alpha(calc, float(zeta)) for zeta in entiers}
        assert min(entiers, key=valeurs.__getitem__) in (bas, haut), zeta_min
        assert delta_min <= valeurs[bas] and delta_min <= valeurs[haut], zeta_min
        assert all(delta_min < v for v in valeurs.values()), zeta_min
        grille = sorted({*entiers, zeta_min})
        suite = [delta_min if zeta == zeta_min else valeurs[zeta] for zeta in grille]
        rang = grille.index(zeta_min)
        assert all(a > b for a, b in zip(suite[:rang], suite[1:rang + 1])), zeta_min
        assert all(a < b for a, b in zip(suite[rang:], suite[rang + 1:])), zeta_min


def test_minimum_de_delta_r_alpha_en_zeta_refuse_sans_croisement(stationnaire, base):
    """#173 : si r̄_α(0) − r̄_α(2 %) ne change pas de signe aux bornes, le minimum n'est pas localisé, refus explicite
    (`MinimumNonEncadre`, sous-classe de `HorsDomaine`, motif à l'appui), jamais une valeur NaN ni une borne rendue
    comme minimum."""
    calc = stationnaire.Calculs(base)
    zeta_min, _ = stationnaire.minimum_delta_r_alpha_en_zeta(calc)
    for bornes in ((2.0, math.floor(zeta_min)), (math.ceil(zeta_min), 200.0)):
        with pytest.raises(stationnaire.MinimumNonEncadre, match="aucun changement de signe") as refus:
            stationnaire.minimum_delta_r_alpha_en_zeta(calc, bornes)
        assert isinstance(refus.value, stationnaire.HorsDomaine) and "point anguleux non encadré" in refus.value.motif


class _RAlphaSynthetique:
    """`calc` synthétique de `minimum_delta_r_alpha_en_zeta` : r̄_α(2 %) = 0, r̄_α(0) = (50 − ζ)/100 (croisement à
    ζ = 50, jamais un milieu dyadique de [2 ; 200]) ; r̄_α(10 %) donné par `haut`."""

    def __init__(self, haut) -> None:
        self.haut = haut

    def r_alpha(self, pi: float, zeta: float) -> float:
        return {0.0: (50.0 - zeta) / 100, 0.02: 0.0, 0.10: self.haut(zeta)}[pi]


@pytest.mark.parametrize("bornes, tol", [
    ((200.0, 2.0), 1e-3), ((50.0, 50.0), 1e-3), ((math.nan, 200.0), 1e-3), ((2.0, math.inf), 1e-3),
    ((2.0, 200.0), math.nan), ((2.0, 200.0), 0.0), ((2.0, 200.0), -1e-3), ((2.0, 200.0), math.inf)])
def test_minimum_de_delta_r_alpha_refuse_bornes_et_tolerance_invalides(stationnaire, bornes, tol):
    """C1 de l'audit de #173 : bornes non finies ou non croissantes, tolérance non finie ou ≤ 0 : refus par
    `HorsDomaine` (pas `MinimumNonEncadre`, que la table publierait « refusée »), motif à l'appui, sans bissection."""
    calc = _RAlphaSynthetique(lambda zeta: 1.0)
    with pytest.raises(stationnaire.HorsDomaine, match="finies et croissantes") as refus:
        stationnaire.minimum_delta_r_alpha_en_zeta(calc, bornes, tol)
    assert not isinstance(refus.value, stationnaire.MinimumNonEncadre)


def test_minimum_de_delta_r_alpha_refuse_un_croisement_non_minimal(stationnaire):
    """C2 de l'audit de #173 : un croisement encadré où Δr̄_α culmine (r̄_α(10 %) en pic à ζ = 50, pente 1 000 contre
    1 pour r̄_α(0)) est refusé, motif « croisement trouvé mais non minimal ». Le même croisement sous un point
    anguleux de Δr̄_α en creux à ζ = 50 est rendu, à la tolérance près : creux symétrique (pentes ∓1 000, que la seule
    comparaison aux extrémités de l'intervalle final refuserait : ζ* = 50,00033 tombe au-delà du point anguleux, plus
    loin que l'extrémité 49,99995) et creux à descente raide (pentes −1 000 et +1,01, la forme mesurée à T1)."""
    with pytest.raises(stationnaire.MinimumNonEncadre, match="croisement trouvé mais non minimal"):
        stationnaire.minimum_delta_r_alpha_en_zeta(_RAlphaSynthetique(lambda zeta: 10.0 - 1000 * abs(zeta - 50.0)))
    for haut in (lambda zeta: 10.0 + 1000 * abs(zeta - 50.0),
                 lambda zeta: 10.0 + 1000 * max(50.0 - zeta, 0.0) + max(zeta - 50.0, 0.0)):
        zeta_min, delta_min = stationnaire.minimum_delta_r_alpha_en_zeta(_RAlphaSynthetique(haut))
        assert abs(zeta_min - 50.0) <= stationnaire.TOL_ZETA_MINIMUM / 2
        assert 100 * 10.0 <= delta_min <= 100 * (10.0 + 1000 * stationnaire.TOL_ZETA_MINIMUM)


@pytest.mark.parametrize("haut", [
    lambda zeta: 0.0 if zeta < 10.0 else 10.0 + 1000 * abs(zeta - 50.0),
    lambda zeta: 0.0 if zeta > 150.0 else 10.0 + 1000 * abs(zeta - 50.0)], ids=["borne_basse", "borne_haute"])
def test_minimum_de_delta_r_alpha_refuse_un_minimum_aux_bornes(stationnaire, haut):
    """P281 (constat R1 de l'audit de #173) : le creux symétrique de C2 (pentes ∓1 000, accepté par
    `test_minimum_de_delta_r_alpha_refuse_un_croisement_non_minimal`) reste un minimum local à ζ = 50, mais
    r̄_α(10 %) tombe à 0 près d'une borne : Δr̄_α y vaut 48 (ζ = 2) ou 150 points (ζ = 200), sous les 1 000 points du
    croisement. Le minimum global est à la borne : refus `MinimumNonEncadre`, motif « minimum aux bornes », et non une
    valeur publiée comme minimum « sur [2 ; 200] »."""
    with pytest.raises(stationnaire.MinimumNonEncadre, match="minimum aux bornes") as refus:
        stationnaire.minimum_delta_r_alpha_en_zeta(_RAlphaSynthetique(haut))
    assert "n'est pas au croisement" in refus.value.motif


def _creux_symetrique(zeta):
    """r̄_α(10 %) du creux symétrique de C2 (pentes ∓1 000 autour de ζ = 50), accepté comme minimum."""
    return 10.0 + 1000 * abs(zeta - 50.0)


class _RAlphaEgalAUneBorne(_RAlphaSynthetique):
    """Creux symétrique dont le triplet r̄_α à `borne` reprend celui de ζ* : Δr̄_α(borne) = Δr̄_α(ζ*) au bit. Avec
    `permuter` (borne basse), r̄_α(0) et r̄_α(2 %) y sont échangés : Δr̄_α inchangé, signe de r̄_α(0) − r̄_α(2 %)
    opposé à celui de ζ* > 50. La bissection ne lit que ce signe et suit donc le même chemin vers le même ζ*."""

    def __init__(self, borne, zeta_etoile, permuter) -> None:
        super().__init__(_creux_symetrique)
        self.borne, self.zeta_etoile, self.permuter = borne, zeta_etoile, permuter

    def r_alpha(self, pi: float, zeta: float) -> float:
        if zeta != self.borne:
            return super().r_alpha(pi, zeta)
        if self.permuter:
            pi = {0.0: 0.02, 0.02: 0.0, 0.10: 0.10}[pi]
        return super().r_alpha(pi, self.zeta_etoile)


@pytest.mark.parametrize("cote", [0, 1], ids=["borne_basse", "borne_haute"])
def test_minimum_de_delta_r_alpha_refuse_l_egalite_a_une_borne(stationnaire, cote):
    """m2 de l'audit de #173 (P281) : Δr̄_α à une borne égal au bit à Δr̄_α(ζ*) est refusé (« ≤ », pas « < ») :
    le minimum sur [2 ; 200] n'est pas unique au croisement."""
    zeta_etoile, _ = stationnaire.minimum_delta_r_alpha_en_zeta(_RAlphaSynthetique(_creux_symetrique))
    assert zeta_etoile > 50.0  # r̄_α(0) − r̄_α(2 %) < 0 en ζ*, la permutation à la borne basse le rend > 0
    borne = stationnaire.ZETA_MINIMUM_BORNES[cote]
    calc = _RAlphaEgalAUneBorne(borne, zeta_etoile, permuter=cote == 0)
    assert stationnaire._delta_r_alpha(calc, borne) == stationnaire._delta_r_alpha(calc, zeta_etoile)
    with pytest.raises(stationnaire.MinimumNonEncadre, match="minimum aux bornes"):
        stationnaire.minimum_delta_r_alpha_en_zeta(calc)


@pytest.mark.parametrize("ou", [
    lambda zeta: zeta == 2.0, lambda zeta: zeta == 200.0, lambda zeta: abs(zeta - 50.0) < 0.01, lambda zeta: True],
    ids=["borne_basse", "borne_haute", "zeta_etoile", "partout"])
def test_minimum_de_delta_r_alpha_refuse_r_alpha_10_non_fini(stationnaire, ou):
    """M1 et m1 de l'audit de #173 : r̄_α(10 %), qui n'entre pas dans la bissection, NaN à une borne, autour de ζ*
    ou partout. `max` et `min` ignoreraient ce NaN (il n'est pas en tête du triplet) : refus `MinimumNonEncadre`,
    motif « r̄_α non fini », et non un minimum rendu ni le motif « minimum aux bornes »."""
    calc = _RAlphaSynthetique(lambda zeta: math.nan if ou(zeta) else _creux_symetrique(zeta))
    with pytest.raises(stationnaire.MinimumNonEncadre, match="r̄_α non fini à ζ = ") as refus:
        stationnaire.minimum_delta_r_alpha_en_zeta(calc)
    assert "minimum aux bornes" not in refus.value.motif and "non minimal" not in refus.value.motif


def test_minimum_de_delta_r_alpha_refuse_r_alpha_10_non_fini_en_zeta_etoile_exact(stationnaire):
    """n2 de la ré-audit de #173 : r̄_α(10 %) NaN au seul ζ* (mesuré d'abord ; la bissection ne lit pas r̄_α(10 %),
    donc suit le même chemin) : le refus vient du contrôle de finitude en ζ*, motif « r̄_α non fini », et non de la
    comparaison aux bornes qui lirait la valeur NaN."""
    zeta_etoile, _ = stationnaire.minimum_delta_r_alpha_en_zeta(_RAlphaSynthetique(_creux_symetrique))
    calc = _RAlphaSynthetique(lambda zeta: math.nan if zeta == zeta_etoile else _creux_symetrique(zeta))
    with pytest.raises(stationnaire.MinimumNonEncadre, match="r̄_α non fini à ζ = ") as refus:
        stationnaire.minimum_delta_r_alpha_en_zeta(calc)
    assert "minimum aux bornes" not in refus.value.motif and "non minimal" not in refus.value.motif


def test_delta_r_alpha_non_fini_publie_nan(stationnaire):
    """M1 de l'audit de #173 : `_delta_r_alpha` rend NaN dès qu'un r̄_α n'est pas fini, quelle que soit sa place dans
    le triplet ; les lignes « Δr̄_α à ζ = 2, 8, 68 » sortent alors en écart (« script sans objet ; écart +nan »), jamais un Δr̄_α
    calculé sur les deux seules valeurs finies."""
    assert max([0.0, math.nan, 1.0]) - min([0.0, math.nan, 1.0]) == 1.0  # le masquage corrigé
    assert math.isnan(stationnaire._delta_r_alpha(_RAlphaSynthetique(lambda zeta: math.nan), 8.0))
    assert math.isnan(stationnaire._delta_r_alpha(_RAlphaSynthetique(lambda zeta: math.inf), 8.0))
    assert stationnaire._delta_r_alpha(_RAlphaSynthetique(lambda zeta: 1.0), 8.0) == 100 * (1.0 - 0.0)
    ligne = [l for l in stationnaire.table_publiees(_RAlphaSynthetique(lambda zeta: math.nan),
                                                     tuple(v for v in stationnaire.VALEURS_PUBLIEES
                                                           if v[1] == "Δr̄_α à ζ = 8, point"))]
    assert len(ligne) == 1 and ligne[0]["verdict"] == "écart" and math.isnan(ligne[0]["script"])


def test_ligne_refusee_constat_publie_code_0(stationnaire, monkeypatch, capsys):
    """C3 de l'audit de #173 : une ligne « refusée » est un constat publié, comme « état non publié », et non un refus
    de domaine des paramètres : `main` sort en code 0, la table imprimée en entier, bilan accordé au singulier."""
    def refus(calc, *args):
        raise stationnaire.MinimumNonEncadre("refus simulé")
    monkeypatch.setattr(stationnaire, "minimum_delta_r_alpha_en_zeta", refus)
    assert stationnaire.main([]) == 0
    sortie = capsys.readouterr()
    assert "Bilan : 450 valeurs comparées, 429 égales" in sortie.out
    assert "aucun écart, 1 refusée (minimum de Δr̄_α en ζ non localisé, motif à la ligne)." in sortie.out
    assert "script refus (refus simulé) ; refusée" in sortie.out
    assert "Refus de domaine" not in sortie.err


def test_minimum_non_encadre_publie_refuse_dans_la_table(stationnaire, base):
    """#173 : sous une variante où le croisement sort de [2 ; 200] (lv* = 0, bord fermé du domaine), la ligne du
    minimum est publiée « refusée », motif à l'appui, sans interrompre la table ni rendre une valeur comme mesure."""
    cle = ("sec:banque_centrale-conditions", "Δr̄_α au minimum en ζ sur [2 ; 200], point")
    liste = tuple(l for l in stationnaire.VALEURS_PUBLIEES if (l[0], l[1]) == cle)
    assert len(liste) == 1
    [ligne] = stationnaire.table_publiees(stationnaire.Calculs(replace(base, lv=0.0)), liste)
    assert ligne["verdict"] == "refusée" and math.isnan(ligne["script"])
    assert ligne["libelle"].startswith("refus (") and "aucun changement de signe" in ligne["libelle"]


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
    \\barre{…} est remplacé par « ¦ », pour garder une ligne de tableau sur une ligne et couper la lecture d'un signe
    placé devant le passage barré (« ¦ » est hors de `_ENTRE_SIGNE_ET_NOMBRE` ; constat m2, #93)."""
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
    return "\n".join(dedans), " ¦ ".join(dehors)


def _partager_md(texte: str) -> tuple[str, str]:
    """(texte dans les ~~…~~, texte hors des ~~…~~), sur une ligne ; hors barre, chaque ~~…~~ est remplacé par
    « ¦ », pour garder un paragraphe ou une ligne de tableau sur une ligne, et couper la lecture d'un signe placé
    devant le passage barré (« ¦ » est hors de `_ENTRE_SIGNE_ET_NOMBRE` ; constat m2, #93)."""
    return "\n".join(re.findall(r"~~(.+?)~~", texte)), re.sub(r"~~(.+?)~~", " ¦ ", texte)


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


# Règle de lecture d'une valeur publiée dans sa source (constat mi-1 de l'audit ; #93) :
# - frontière : ni chiffre, ni décimale collés (« 2 » ne se lit pas dans « 2,5 », ni « 5 » dans « 2,5 ») ; la virgule
#   s'écrit « , » ou « {,} » (mode mathématique) ;
# - signe : une valeur publiée négative (« -x » ou « −x ») se lit précédée d'un signe moins, séparé du nombre au plus
#   par des espaces, « $ », « ~ » ou « \, » (« $-0{,}058$ », « $-$0,058 », « $0{,}6505 - 0{,}4560$ ») ; une valeur
#   publiée positive (« x » ou « +x ») se lit sans signe moins devant (« + » admis). Signe moins : « − », ou « - »
#   hors « -- » (tiret d'intervalle) ; un « - » collé à une lettre ASCII n'est un signe qu'en mode mathématique
#   (nombre impair de « $ » non échappés avant lui sur sa ligne : « $x-0{,}058$ », « $P_{t-1}$ »), et reste hors de
#   ce mode un trait d'union (« P-0,182 ») ; collé à « } », c'est un signe (« \,}-0{,}058 », « {}-0,058 », constat
#   mi-C). Limites déclarées : les environnements d'équation sans « $ » ne sont pas lus en mode mathématique ; le
#   mode est compté sur la ligne seule, si bien qu'un « $…$ » ouvert sur une ligne et fermé sur la suivante, ou un
#   « $$ », fausserait la parité (constat m3) : précondition figée par `test_sources_sans_mode_mathematique_a_cheval` ;
#   un signe placé devant un passage barré ne s'attache pas au nombre qui le suit (constat m2) ;
# - ligne (`PARAGRAPHES_DE_SOURCE`, #93) : une valeur rattachée se lit dans chacun de ses passages, et non dans le
#   reste de la source ; le passage est le fragment déclaré s'il contient la valeur au signe près (« soit 1 pour
#   $\bar\pi = 0$ », dont la ligne écrit aussi « $\bar\rho_K - 1$ »), sinon l'unique ligne de la source qui le
#   contient ; le signe d'un nombre du fragment se lit dans sa ligne (« 0,110 point » dans « : −0,110 point » est
#   négatif, constat m1) ; toute valeur lue dans une fiche est rattachée ;
# - tableau (`tab:…`) : la valeur se lit dans la ligne que déclare `LIGNES_DE_TABLEAU` (première cellule), égale à la
#   cellule de sa colonne, ou, colonne non déclarée, figurant dans une cellule de la ligne.
_ENTRE_SIGNE_ET_NOMBRE = re.compile(r"(?:\s|\$|~|\\,)+$")
_DOLLAR = re.compile(r"(?<!\\)\$")


def _signe_moins(ligne: str) -> bool:
    """Le texte `ligne`, début de ligne jusqu'au nombre, finit par un signe moins (règle ci-dessus)."""
    fenetre = ligne[-12:]
    avant = _ENTRE_SIGNE_ET_NOMBRE.sub("", fenetre)
    if avant.endswith("−"):
        return True
    if not avant.endswith("-") or avant.endswith("--"):
        return False
    if re.search(r"[A-Za-z]-$", avant) is None:
        return True
    position = len(ligne) - len(fenetre) + len(avant) - 1
    return len(_DOLLAR.findall(ligne, 0, position)) % 2 == 1


def _signes(publie: str, texte: str, debut: int = 0, fin: int | None = None) -> list[bool]:
    """Pour chaque occurrence de la valeur absolue de `publie` dans le texte, sans chiffre ni décimale collés, comprise
    dans texte[debut:fin] : vrai si elle est précédée d'un signe moins, lu dans le texte entier (règle ci-dessus)."""
    fin = len(texte) if fin is None else fin
    absolu = publie.lstrip("-−+")
    formes = "|".join(re.escape(f) for f in (absolu, absolu.replace(",", "{,}")))
    motif = r"(?<![0-9])(?<![0-9][,.])(?<![0-9]\{,\})(?:" + formes + r")(?![0-9])(?![,.][0-9])(?!\{,\}[0-9])"
    return [_signe_moins(texte[texte.rfind("\n", 0, m.start()) + 1:m.start()]) for m in re.finditer(motif, texte)
            if debut <= m.start() and m.end() <= fin]


def _figure(publie: str, texte: str) -> bool:
    """La valeur publiée figure dans le texte, signe compris, sans chiffre ni décimale collés (règle ci-dessus)."""
    return (publie[0] in "-−") in _signes(publie, texte)


def _passage(texte: str, fragment: str, publie: str) -> tuple[str, int, int]:
    """Passage où se lit une valeur rattachée, (ligne, début, fin) : le fragment dans l'unique ligne du texte qui le
    contient, s'il contient la valeur au signe près, sinon la ligne entière ; le signe se lit dans la ligne, jamais
    dans le fragment seul (constat m1 ; règle ci-dessus)."""
    lignes = [l for l in texte.split("\n") if fragment in l]
    assert len(lignes) == 1, (fragment, len(lignes))
    ligne = lignes[0]
    debut = ligne.index(fragment)
    fin = debut + len(fragment)
    return (ligne, debut, fin) if _signes(publie, ligne, debut, fin) else (ligne, 0, len(ligne))


def _cellules(texte: str, ligne: str) -> list[str]:
    """Cellules de l'unique ligne de tableau dont la première cellule est `ligne`."""
    rangs = [r for r in texte.split("\n") if re.split(r"(?<!\\)&", r)[0].strip() == ligne]
    assert len(rangs) == 1, (ligne, len(rangs))
    return [c.strip() for c in re.split(r"(?<!\\)&", rangs[0].strip().removesuffix("\\\\"))]


def _normaliser(cellule: str) -> str:
    return cellule.replace("¦", "").replace("$", "").replace("{,}", ",").replace("−", "-").strip().lstrip("+")


def _lue(stationnaire, section: str, grandeur: str, publie: str, nom: str, dehors: str) -> bool:
    """La valeur en vigueur se lit hors barre dans la source `nom` (règle ci-dessus)."""
    if (fragments := stationnaire.PARAGRAPHES_DE_SOURCE.get((section, grandeur, nom))) is not None:
        return all((publie[0] in "-−") in _signes(publie, *_passage(dehors, f, publie)) for f in fragments)
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
    assert _figure("2", "a-2 et $b + c$") and not _figure("-2", "$a$ et b-2") and not _figure("-2", "$1--2$")
    tab = "A & x & 1,00 & 2,000\\\\\nB & y & 2,000 & $-0{,}5$\\\\"
    assert _cellules(tab, "B") == ["B", "y", "2,000", "$-0{,}5$"]
    assert _normaliser(_cellules(tab, "B")[3]) == _normaliser("-0,5")
    assert _normaliser(_cellules(tab, "A")[2]) != _normaliser("2,000")
    barre = _partager_tex("L & \\barre{0,1} 0,2 & x\\\\")[1]
    assert _normaliser(_cellules(barre, "L")[1]) == _normaliser("0,2")


@pytest.mark.parametrize("texte", ["$a\\,}-0{,}058$", "${}-0,058$", "{}-0,058", "\\mathrm{x}-0,058",
                                   "$x-0{,}058$", "$\\bar r-0{,}058$", "$x - 1$ puis $y-0{,}058$"])
def test_signe_moins_colle_a_une_accolade_ou_en_mode_mathematique(texte):
    """Constat mi-C (#93) : un « - » collé à « } », ou collé à une lettre en mode mathématique, est un signe moins ;
    la valeur négative s'y lit, la valeur positive ne s'y lit pas."""
    assert _figure("-0,058", texte) and not _figure("0,058", texte)


def test_mode_mathematique_compte_sur_la_ligne():
    """Le mode mathématique se lit sur la ligne du nombre : un « $ » d'une ligne précédente ne s'y reporte pas, un
    « \\$ » échappé n'ouvre pas le mode."""
    assert _figure("-1", "$P_{t-1}$") and not _figure("1", "$P_{t-1}$")
    assert _figure("1", "$a$\nt-1") and _figure("1", "\\$ t-1") and not _figure("-1", "$a\nt-1")


def test_valeur_rattachee_lue_dans_sa_seule_ligne(stationnaire, monkeypatch):
    """#93, point 1 : une valeur rattachée se lit dans sa ligne, ou dans son fragment s'il la contient au signe près,
    seulement ; une valeur écrite ailleurs, signe inversé compris, ne la fait pas compter ; un fragment ambigu
    (plusieurs lignes) est refusé."""
    dehors = "ligne A : +0,110 point\nligne B : −0,110 %\nligne C : 2,5"
    cle = ("fiche 9 § 6.3", "g", "fiche 9")
    monkeypatch.setattr(stationnaire, "PARAGRAPHES_DE_SOURCE", {cle: ("ligne A",)})
    assert _lue(stationnaire, "fiche 9 § 6.3", "g", "0,110", "fiche 9", dehors)
    assert not _lue(stationnaire, "fiche 9 § 6.3", "g", "-0,110", "fiche 9", dehors)
    assert _figure("-0,110", dehors)
    monkeypatch.setattr(stationnaire, "PARAGRAPHES_DE_SOURCE", {cle: ("ligne A", "ligne C")})
    assert not _lue(stationnaire, "fiche 9 § 6.3", "g", "0,110", "fiche 9", dehors)
    monkeypatch.setattr(stationnaire, "PARAGRAPHES_DE_SOURCE", {cle: ("ligne B : −0,1",)})
    assert _figure("0,1", "ligne A : soit 0,1 et $x - 0{,}1$")
    dehors_1 = "ligne A : soit 0,1 et $x - 0{,}1$\nligne B : −0,1"
    assert _lue(stationnaire, "fiche 9 § 6.3", "g", "-0,1", "fiche 9", dehors_1)
    monkeypatch.setattr(stationnaire, "PARAGRAPHES_DE_SOURCE", {cle: ("soit 0,1 et",)})
    assert _lue(stationnaire, "fiche 9 § 6.3", "g", "0,1", "fiche 9", dehors_1)
    assert not _lue(stationnaire, "fiche 9 § 6.3", "g", "-0,1", "fiche 9", dehors_1)
    monkeypatch.setattr(stationnaire, "PARAGRAPHES_DE_SOURCE", {cle: ("ligne",)})
    with pytest.raises(AssertionError):
        _lue(stationnaire, "fiche 9 § 6.3", "g", "0,110", "fiche 9", dehors)


def test_signe_du_fragment_lu_dans_sa_ligne(stationnaire, monkeypatch):
    """Constat m1 (#93) : un fragment qui commence au nombre ne coupe pas le signe qui le précède dans sa ligne."""
    cle = ("fiche 9 § 6.3", "g", "fiche 9")
    monkeypatch.setattr(stationnaire, "PARAGRAPHES_DE_SOURCE", {cle: ("0,110 point",)})
    dehors = "ligne A : −0,110 point"
    assert not _lue(stationnaire, "fiche 9 § 6.3", "g", "0,110", "fiche 9", dehors)
    assert _lue(stationnaire, "fiche 9 § 6.3", "g", "-0,110", "fiche 9", dehors)


def test_signe_devant_un_passage_barre_coupe():
    """Constat m2 (#93) : un signe placé devant un passage barré ne s'attache pas au nombre qui suit la barre."""
    dedans, dehors = _partager_md("écart −~~0,2~~ 0,110 point")
    assert dedans == "0,2" and "\n" not in dehors
    assert _figure("0,110", dehors) and not _figure("-0,110", dehors)
    assert _figure("-0,110", _partager_md("écart ~~−0,2~~ −0,110 point")[1])


@pytest.mark.parametrize("texte", ["écart −\\barre{0,2} 0,110 point", "$-\\barre{0{,}2}\\,0{,}110$"])
def test_signe_devant_un_barre_tex_coupe(texte):
    """Constat m2 (#93), côté spécification : un signe placé devant un \\barre{…} ne s'attache pas au nombre qui le
    suit."""
    dedans, dehors = _partager_tex(texte)
    assert dedans in ("0,2", "0{,}2") and "\n" not in dehors
    assert _figure("0,110", dehors) and not _figure("-0,110", dehors)


def test_sources_sans_mode_mathematique_a_cheval():
    """Constat m3 (#93) : le mode mathématique se compte sur la ligne seule (règle ci-dessus) ; précondition : aucune
    ligne de la spécification ni des fiches n'a un nombre impair de « $ » non échappés, ni de « $$ »."""
    for chemin in (SPECIFICATION, *dict.fromkeys(FICHES.values())):
        lignes = chemin.read_text(encoding="utf-8").split("\n")
        impaires = [n for n, l in enumerate(lignes, 1) if len(_DOLLAR.findall(l)) % 2]
        doubles = [n for n, l in enumerate(lignes, 1) if "$$" in l]
        assert (impaires, doubles) == ([], []), chemin.name


def _inverser(publie: str) -> str:
    return publie[1:] if publie[0] in "-−" else "-" + publie.lstrip("+")


def test_toute_inversion_de_signe_detectee(stationnaire):
    """Critère d'acceptation de #93 : l'inversion du signe de chaque valeur en vigueur fait échouer la lecture dans sa
    source (dont « 0,110 », (β) de la fiche 9, et « 1 », ρ̄_K à 0 %, que la lecture de la source entière manquait)."""
    non_detectees = [(section, grandeur, publie) for section, grandeur, publie, _, _ in stationnaire.VALEURS_PUBLIEES
                     if publie != stationnaire.AUCUNE
                     and all(_lue(stationnaire, section, grandeur, _inverser(publie), nom, dehors)
                             for nom, _, dehors in _sources(section))]
    assert non_detectees == []


def test_chaque_valeur_de_fiche_a_sa_ligne(stationnaire):
    """Toute valeur en vigueur lue dans une fiche est rattachée à ses lignes (`PARAGRAPHES_DE_SOURCE`), et tout
    rattachement sert à une valeur et à une source qu'elle cite."""
    citees = {(section, grandeur, nom) for section, grandeur, publie, _, _ in stationnaire.VALEURS_PUBLIEES
              if publie != stationnaire.AUCUNE for nom, _, _ in _sources(section)}
    assert {cle for cle in citees if cle[2] in FICHES} <= set(stationnaire.PARAGRAPHES_DE_SOURCE)
    assert set(stationnaire.PARAGRAPHES_DE_SOURCE) <= citees


def test_delta_rho_hors_cible_independant_de_varpi_L(stationnaire, base):
    """`sec:investissement-taux` (limites) publie « même Δϱ » avec et sans l'écart ϖ_L : Δϱ = (π̄ − π*)(1 + r̄)/(1 + π*)
    ne dépend pas de ϖ_L."""
    avec = stationnaire._fisher_hors_cible(base, 0.10, base.varpi_L)["d_rho"]
    sans = stationnaire._fisher_hors_cible(base, 0.10, 0.0)["d_rho"]
    attendu = 100 * (0.10 - base.pi_cible) * (1 + base.rbar) / (1 + base.pi_cible)
    assert abs(avec - sans) <= TOL * abs(attendu) and abs(avec - attendu) <= TOL * abs(attendu)


def test_valeurs_en_vigueur_ecrites_hors_barre_dans_leur_source(stationnaire):
    """Chaque valeur en vigueur figure hors de \\barre{…} (spécification) et de ~~…~~ (fiches) dans chacune des
    sources que cite sa section, signe compris, sans décimale collée, dans les lignes auxquelles elle est rattachée
    (`PARAGRAPHES_DE_SOURCE`), et, dans un tableau, dans la cellule de sa ligne et de sa colonne
    (`LIGNES_DE_TABLEAU`) : une valeur barrée ne peut être comptée en vigueur."""
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


def test_anciennes_valeurs_de_M34_barrees_dans_leur_source(stationnaire):
    """Chaque ancienne valeur republiée au rang 9 (`ANCIENNES_M34`) figure barrée dans au moins une des sources que
    cite sa section, signe compris : la republication garde la trace de la valeur qu'elle remplace."""
    manquantes = [(section, grandeur, ancienne) for (section, grandeur), ancienne in ANCIENNES_M34.items()
                  if not any(_figure(ancienne, dedans) for _, dedans, _ in _sources(section))]
    assert manquantes == []
