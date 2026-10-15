"""Tests de la contre-épreuve indépendante de la fiche 6 (#66).

Ils vérifient l'indépendance du script (aucun import de `src/` ni
d'`archive/`, aucun chargement dynamique hors de l'état stationnaire), son
déterminisme, sa durée, ses contrôles internes (transcription du pas sur le
sentier stationnaire, homogénéité nominale, convergence de Newton,
dérivabilité de la jacobienne) et le signe des pentes du pas que le contrôle
de sentier ne voit pas. Aucun ne fige un rayon : les valeurs remesurées
attendent la validation de `macro` (#66).
"""

import ast
import importlib.util
import json
import math
import sys
import time
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

RACINE = Path(__file__).resolve().parents[2]
SCRIPT = RACINE / "outils" / "contre_epreuve_financement.py"
MODULES_ADMIS = {"__future__", "argparse", "cmath", "importlib", "json", "math", "sys", "time", "dataclasses",
                 "pathlib", "numpy"}
# Appels de chargement dynamique : admis dans `_charger_etat_stationnaire` seulement.
CHARGEURS = {"import_module", "spec_from_file_location", "module_from_spec", "__import__", "exec_module"}
# Sources qu'aucune chaîne du script (docstrings exceptées) ne doit nommer : maquettes de la fiche 6, de #65.
SOURCES_INTERDITES = ("maquette_conjointe", "conj6", "archive", "nations")


@pytest.fixture(scope="module")
def ce():
    """Module `outils/contre_epreuve_financement.py`, chargé par son chemin."""
    spec = importlib.util.spec_from_file_location("contre_epreuve_financement", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_n_importe_ni_src_ni_archive():
    arbre = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    importes = set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            importes |= {a.name.split(".")[0] for a in noeud.names}
        elif isinstance(noeud, ast.ImportFrom):
            importes.add((noeud.module or "").split(".")[0])
    assert importes <= MODULES_ADMIS, importes - MODULES_ADMIS
    # Le seul fichier chargé par son chemin est le script d'état stationnaire.
    docstrings = {id(n.body[0].value) for n in ast.walk(arbre)
                  if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef)) and n.body
                  and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
    chaines = {n.value for n in ast.walk(arbre) if isinstance(n, ast.Constant) and isinstance(n.value, str)
               and id(n) not in docstrings}
    chemins = {c for c in chaines if c.endswith(".py")}
    assert chemins == {"etat_stationnaire.py"}
    assert "src" not in chaines
    assert not [c for c in chaines if any(s in c for s in SOURCES_INTERDITES)]


def _appels_de_chargement(noeud) -> list[str]:
    noms = []
    for n in ast.walk(noeud):
        if isinstance(n, ast.Call):
            nom = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", None)
            if nom in CHARGEURS:
                noms.append(nom)
    return sorted(noms)


def test_aucun_chargement_dynamique_hors_etat_stationnaire():
    """`import_module`, `spec_from_file_location`… ne servent qu'à charger `outils/etat_stationnaire.py`."""
    arbre = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    chargeur = [n for n in arbre.body if isinstance(n, ast.FunctionDef) and n.name == "_charger_etat_stationnaire"]
    assert len(chargeur) == 1
    dans_chargeur = _appels_de_chargement(chargeur[0])
    assert dans_chargeur == ["exec_module", "module_from_spec", "spec_from_file_location"]
    assert _appels_de_chargement(arbre) == dans_chargeur


@pytest.mark.parametrize("configuration", ["socle", "fiche"])
@pytest.mark.parametrize("regime", ["hausse", "baisse"])
@pytest.mark.parametrize("taux", ["exogene", "regle"])
def test_le_pas_garde_l_etat_resolu_sur_son_sentier(ce, configuration, regime, taux):
    par = ce.Parametres() if configuration == "socle" else ce.config_fiche(ce.Parametres())
    o = ce.ouverture_resolue(par)
    assert ce.residu_sentier(o, par, ce.Config(regime=regime, taux=taux)) <= ce.TOL_SENTIER


@pytest.mark.parametrize("credit", ["comptable", "pK_phat_ouv"])
@pytest.mark.parametrize("depots", ["ve", "ventes_du_pas"])
def test_homogeneite_nominale_et_racine_retiree(ce, credit, depots):
    par = ce.Parametres()
    res = ce.rayon_conjoint(par, ce.Config(credit=credit, depots=depots))
    sp = res["spectre"]
    assert res["residu_stationnaire"] <= ce.TOL_NEWTON
    assert sp.homogeneite <= ce.TOL_HOMOGENEITE
    assert abs(sp.racine_retiree - 1) <= ce.TOL_RACINE_NOMINALE
    assert sp.racine_restante is None
    assert res["planchers_actifs"] == 0


def test_une_racine_restee_pres_de_1_apres_deflation_echoue(ce, monkeypatch):
    """Racine 1 double : la déflation n'en retire qu'une, l'autre reste et le contrôle de la racine retirée
    échoue, dans `spectre` comme dans `calculer`."""
    sp = ce.spectre(np.diag([1.0, 1.0, 0.5]), np.array([1.0, 0.0, 0.0]), 0)
    assert abs(sp.racine_retiree - 1) <= ce.TOL_RACINE_NOMINALE
    assert sp.racine_restante is not None and abs(sp.racine_restante - 1) <= ce.TOL_RACINE_NOMINALE
    assert ce.spectre(np.diag([1.0, 0.9, 0.5]), np.array([1.0, 0.0, 0.0]), 0).racine_restante is None
    spectre = ce.spectre
    monkeypatch.setattr(ce, "spectre", lambda *a: replace(spectre(*a), racine_restante=complex(1.0)))
    r = ce.calculer()
    assert not ce.controles_passent(r)
    assert all(not math.isfinite(v) for k, v in r["controles"].items() if k.startswith("racine retirée"))


def test_seuil_lambda_ti_refuse_un_rayon_deja_explosif_au_premier_point(ce, monkeypatch):
    """Rayon ≥ 1 dès λ_ti = 0,002 : le plus petit seuil n'est pas encadré, la fonction refuse au lieu de rendre
    un franchissement ultérieur ou « jamais » ; un franchissement encadré reste trouvé."""
    def boucle(rayons):
        return lambda par, m: ce.Spectre(rayons(par.lambda_ti), 0j, 0.0, complex(math.nan), None, None, None)
    monkeypatch.setattr(ce, "rayon_boucle_reduite", boucle(lambda l: 1.5 if l < 0.003 else (1.2 if l > 0.5 else 0.5)))
    with pytest.raises(ValueError):
        ce.seuil_lambda_ti(ce.Parametres(), 0.8)
    monkeypatch.setattr(ce, "rayon_boucle_reduite", boucle(lambda l: 1.5))
    with pytest.raises(ValueError):
        ce.seuil_lambda_ti(ce.Parametres(), 0.8)
    monkeypatch.setattr(ce, "rayon_boucle_reduite", boucle(lambda l: 0.9 + l / 2))
    assert ce.seuil_lambda_ti(ce.Parametres(), 0.8) == pytest.approx(0.2, abs=1e-9)
    monkeypatch.setattr(ce, "rayon_boucle_reduite", boucle(lambda l: 0.5))
    assert ce.seuil_lambda_ti(ce.Parametres(), 0.8) is None


def test_seuil_non_encadre_fait_echouer_les_controles(ce, monkeypatch, capsys, tmp_path):
    """Un seuil de λ_ti refusé (non encadré par la grille) ne lève pas d'exception hors du script : il est publié
    sans mesure, et le contrôle en échec donne le code de sortie 2, documenté, y compris après passage par JSON ;
    les seuils encadrés ne créent aucun contrôle (sortie inchangée)."""
    assert not any(k.startswith("seuil") for k in ce.calculer()["controles"])
    seuil = ce.seuil_lambda_ti

    def refus_a_m_07(par, m):
        if m == 0.7:
            raise ValueError("seuil non encadré (essai)")
        return seuil(par, m)

    monkeypatch.setattr(ce, "seuil_lambda_ti", refus_a_m_07)
    chemin = tmp_path / "ce.json"
    assert ce.main(["--json", str(chemin)]) == 2
    sortie = capsys.readouterr().out
    assert "Contrôles : ÉCHEC" in sortie
    assert sum(l.startswith("| boucle réduite, seuil de λ_ti (par an), m = 0.7") and "| — |" in l
               for l in sortie.splitlines()) == 2
    r = json.loads(chemin.read_text(encoding="utf-8"))
    assert [k for k in r["controles"] if k.startswith("seuil")] == ["seuil de λ_ti encadré, m = 0.7, 2 ans",
                                                                     "seuil de λ_ti encadré, m = 0.7, 3 ans"]
    assert not ce.controles_passent(r)


def test_f_retenue_est_deja_stationnaire(ce):
    """L'état initial résolu est un point fixe : Newton n'itère pas sous F retenue."""
    st = ce.stationnaire_variante(ce.Parametres(), ce.Config())
    assert st.iterations == 0
    assert st.residu <= ce.TOL_NEWTON


def test_levier_vise_tenu_par_la_variante(ce):
    """Variante « levier sur p K^vol » : à l'état stationnaire, L = lv* p̂ K^vol d'ouverture (définition)."""
    par = ce.Parametres()
    st = ce.stationnaire_variante(par, ce.Config(credit="pK_phat_ouv"))
    o = st.ouverture
    f = ce.facteurs_sentier(par)
    phat = o["P0"] * (1 + par.pi_cible) ** (1 / par.n_a)
    # L de clôture (= L d'ouverture × Γ̄) égale la cible posée sur l'ouverture.
    assert o["L"] * f["L"] == pytest.approx(par.lv * phat * o["K_vol"], rel=1e-12)


def test_deterministe_et_court(ce, tmp_path):
    t0 = time.perf_counter()
    r = ce.calculer()
    duree = time.perf_counter() - t0
    a = json.dumps(ce._jsonable(r), ensure_ascii=False)
    b = json.dumps(ce._jsonable(ce.calculer()), ensure_ascii=False)
    assert a == b
    assert duree < 30.0
    echecs = {k: v for k, v in r["controles"].items() if not ce.controles_passent({"controles": {k: v}})}
    assert not echecs, echecs
    assert ce.controles_passent(json.loads(a))


@pytest.mark.parametrize("valeur", [None, math.inf, math.nan])
def test_un_controle_absent_ou_non_fini_echoue(ce, valeur):
    """Un résidu infini (Newton qui diverge), devenu `None` par JSON, est un échec, pas une erreur."""
    assert not ce.controles_passent({"controles": {"Newton socle x1 comptable ve hausse exogene": valeur}})


# --- Contrôle de dérivabilité de la jacobienne ------------------------------------


def test_le_controle_de_derivabilite_voit_un_coude(ce):
    _, coude = ce.jacobienne(lambda x: np.array([x[0], abs(x[0])]), 2)
    assert coude == pytest.approx(2.0)
    assert coude > ce.TOL_COUDE


def test_le_coude_d_une_colonne_a_ligne_nulle_est_exempte(ce):
    """La colonne 0 a un coude, mais sa ligne de J est nulle : sans effet sur le spectre, elle est exemptée."""
    J, coude = ce.jacobienne(lambda x: np.array([0.0, abs(x[0]) + x[1]]), 2)
    assert np.all(J[0] == 0.0)
    assert coude <= ce.TOL_COUDE


@pytest.mark.parametrize("configuration", ["socle", "fiche"])
@pytest.mark.parametrize("regime", ["hausse", "baisse"])
@pytest.mark.parametrize("credit", ["comptable", "pK_phat_ouv"])
def test_jacobienne_derivable_dans_chaque_regime(ce, configuration, regime, credit):
    """Chaque régime de T4 prend sa branche de N5 : différences avant et arrière concordent."""
    par = ce.Parametres() if configuration == "socle" else ce.config_fiche(ce.Parametres())
    assert ce.rayon_conjoint(par, ce.Config(credit=credit, regime=regime))["coude"] <= ce.TOL_COUDE


# --- Pentes du pas (le contrôle de sentier ne voit que les niveaux) ----------------


def _pas_perturbe(ce, cle, facteur, par=None, regime="hausse"):
    par = ce.Parametres() if par is None else par
    o = ce.ouverture_resolue(par)
    cfg = ce.Config(regime=regime)
    base = ce.pas(o, par, cfg)
    o2 = dict(o)
    o2[cle] = o[cle] * facteur if o[cle] != 0.0 else facteur - 1.0
    return base, ce.pas(o2, par, cfg)


@pytest.mark.parametrize("regime", ["hausse", "baisse"])
def test_pente_chomage_salaire(ce, regime):
    """T3 : −β (U_{t−1} − U^eq), β > 0 ; un chômage d'ouverture plus haut baisse le salaire nominal."""
    assert ce.Parametres().beta > 0
    base, haut = _pas_perturbe(ce, "U_m1", 1.1, regime=regime)
    assert haut["W_m1"] < base["W_m1"]


@pytest.mark.parametrize("regime", ["hausse", "baisse"])
def test_pente_stocks_prix(ce, regime):
    """P1, P2 : ξ = 1 − IN^vol / IN^vol*, terme + ψ_ξ ξ, ψ_ξ > 0 ; des stocks plus hauts baissent le prix."""
    assert ce.Parametres().psi_xi > 0
    base, haut = _pas_perturbe(ce, "IN_vol", 1.01, regime=regime)
    assert haut["P0"] < base["P0"]


@pytest.mark.parametrize("regime", ["hausse", "baisse"])
def test_pente_taux_du_credit_investissement(ce, regime):
    """S1, S3 : exp[−η_r (ϱ_L − ϱ̄_L)], η_r > 0 ; un taux du crédit plus haut baisse I^{vol,plan}, donc
    le capital en volume de clôture (N10, toute la demande servie à l'état stationnaire)."""
    assert ce.Parametres().eta_r > 0
    base, haut = _pas_perturbe(ce, "i_L", 1.1, regime=regime)
    assert haut["K_vol"] < base["K_vol"]


@pytest.mark.parametrize("regime", ["hausse", "baisse"])
def test_pente_patrimoine_vise_consommation(ce, regime):
    """H3, H4 : − λ_H/n_a (V* − V), λ_H > 0 ; un patrimoine visé plus haut (ν_H) baisse la consommation, donc
    la demande et les ventes anticipées de clôture (N1)."""
    par = ce.Parametres()
    assert par.lambda_H > 0
    o = ce.ouverture_resolue(par)
    cfg = ce.Config(regime=regime)
    base = ce.pas(o, par, cfg)
    haut = ce.pas(o, replace(par, nu_H=1.1 * par.nu_H), cfg)
    assert haut["ve"] < base["ve"]
