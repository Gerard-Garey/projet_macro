"""Tests de la maquette linéarisée de la boucle conjointe (issue #65).

Propriétés de l'outil, écrites avant l'essai par le brief de #65 : il
n'importe ni `src/` ni `archive/` ; il est déterministe ; il s'exécute en
quelques secondes ; son relevé couvre chaque chiffre recensé dans les
paragraphes de la spécification qui citent des boucles conjointes. S'y
ajoutent deux contrôles de la méthode : la carte du socle est une seconde
transcription des règles, qui rend la même clôture qu'`etat_stationnaire.un_pas`
sur l'état résolu et sur des états perturbés ; la jacobienne redonne les
valeurs propres analytiques de la boucle propre du bloc production
(`sec:production-conditions`). Lot de correction de #65 (décisions du
15/10/2026) : contenu des identités de bilan contre `etat_stationnaire`,
liste « Grille G » de la fiche lue ligne à ligne, invariance de la variété
dans les six cas et code de sortie qui en dépend, lecture (c) et cause des
racines déclarées, verdicts des deux grilles, frontières φ* et marge
conjointe, contrôle avant/arrière des coudes, méthode de la seconde écriture
des variantes de F (#66). Republication du 15/10/2026 : un nombre recensé
n'est couvert que par un chiffre qui déclare son paragraphe, et une valeur
barrée n'est ni recensée ni cherchée. Aucun test ne fige une valeur publiée :
leur reproduction est publiée par le script et relève du visa de l'expert
pilote.
"""

import ast
import dataclasses
import importlib.util
import math
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

RACINE = Path(__file__).resolve().parents[2]
SCRIPT = RACINE / "outils" / "maquette_conjointe.py"
DUREE_MAX = 10.0  # secondes, « quelques secondes » (brief de #65), exécution complète en sous-processus
# Le seuil de durée rend son verdict sur la plateforme de référence seulement (ADR 0003, M16), comme les
# seuils de coût du moteur (`tests/invariants/test_budget.py`) ; ailleurs, la mesure est publiée et le test
# se termine par un saut qui la dit (#126). Le déterminisme est vérifié sur toute machine.
PLATEFORME_DE_REFERENCE = os.environ.get("GITHUB_ACTIONS") == "true" and sys.platform == "linux"


@pytest.fixture(scope="module")
def maquette():
    """Module `outils/maquette_conjointe.py`, chargé par son chemin (`outils/` n'est pas un paquet)."""
    spec = importlib.util.spec_from_file_location("maquette_conjointe", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_n_importe_ni_src_ni_archive():
    arbre = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    modules = set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            modules.update(a.name.split(".")[0] for a in noeud.names)
        elif isinstance(noeud, ast.ImportFrom):
            modules.add((noeud.module or "").split(".")[0])
    assert not modules & {"nations", "archive", "src"}
    assert modules <= {"__future__", "argparse", "dataclasses", "functools", "importlib", "json", "math",
                       "pathlib", "re", "sys", "numpy"}
    # Seul module du dépôt chargé par son chemin : le script d'état stationnaire. Aucun autre chargement
    # dynamique (indépendance de la contre-épreuve #66, symétrique de son propre test).
    assert '"etat_stationnaire"' in SCRIPT.read_text(encoding="utf-8")
    appels = [n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", None)
              for n in ast.walk(arbre) if isinstance(n, ast.Call)]
    assert appels.count("spec_from_file_location") == 1 and appels.count("module_from_spec") == 1
    natifs = {n.func.id for n in ast.walk(arbre) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert "import_module" not in appels and not {"__import__", "exec", "eval", "compile"} & natifs


@pytest.fixture(scope="module")
def deux_executions():
    """Deux exécutions complètes du script en sous-processus : (sorties, durées en secondes)."""
    sorties, durees = [], []
    for _ in range(2):
        debut = time.perf_counter()
        r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, cwd=RACINE, check=False)
        durees.append(time.perf_counter() - debut)
        assert r.returncode == 0, r.stderr
        sorties.append(r.stdout)
    return sorties, durees


def test_deterministe(deux_executions):
    sorties, _ = deux_executions
    assert sorties[0] == sorties[1]


def test_rapide(deux_executions):
    _, durees = deux_executions
    duree = max(durees)
    if not PLATEFORME_DE_REFERENCE:
        verdict = "<" if duree < DUREE_MAX else "≥"
        pytest.skip(f"durée {duree:.2f} s {verdict} {DUREE_MAX} s, hors référence : seuil de durée contrôlé "
                    "sur la plateforme de référence seulement (CI GitHub Actions, ADR 0003, M16) ; "
                    "mesure publiée (#126)")
    assert duree < DUREE_MAX


def test_releve_couvre_chaque_chiffre_recense(maquette):
    lignes = maquette.lire_spec()
    releve = maquette.releve()
    # Un nombre recensé n'est couvert que par un chiffre du relevé qui déclare son paragraphe (`ou`) : un
    # nombre égal relevé pour une autre grandeur, dans un autre paragraphe, ne le couvre pas.
    couverts = {(label, c.publie.replace("{,}", ",")) for c in releve for label in c.ou}
    recenses = maquette.recenser(lignes) + maquette.recenser_fiches(maquette.lire_fiches())
    assert recenses
    # Chaque paragraphe et chaque ligne de fiche déclarés sont recensés.
    assert {label for label, _ in maquette.PARAGRAPHES} | {f for f, _ in maquette.LIGNES_FICHES} \
        <= {label for label, _, _ in recenses}
    manquants = [x for x in recenses if (x[0], x[2]) not in couverts and (x[0], x[2]) not in maquette.EXCLUS]
    assert manquants == []
    # Aucune exclusion périmée : chacune désigne un nombre encore écrit, non barré, dans son paragraphe.
    cles = {(label, nombre) for label, _, nombre in recenses}
    assert set(maquette.EXCLUS) <= cles
    # Une exclusion ne double pas un chiffre relevé.
    assert not set(maquette.EXCLUS) & couverts


def _lever_barres(ligne):
    """Ligne dont chaque valeur barrée, `\\barre{…}`, est remplacée par son contenu (deux niveaux d'accolades)."""
    levee = re.sub(r"\\barre\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", r"\1", ligne)
    assert "\\barre{" not in levee, ligne
    return levee


def test_chaque_chiffre_releve_a_sa_ligne(maquette):
    """Chaque chiffre est écrit, hors valeur barrée, dans chacun des paragraphes et fiches qu'il déclare, sauf les six
    chiffres sans objet à la table T1 (`SANS_OBJET_M34`), écrits barrés dans chacun des paragraphes qu'ils déclarent :
    un chiffre sans objet encore écrit en vigueur, ou un chiffre en vigueur barré ou effacé, fait échouer la
    batterie."""
    lignes, fiches = maquette.lire_spec(), maquette.lire_fiches()
    paragraphes = {label for label, _ in maquette.PARAGRAPHES} | {f for f, _ in maquette.LIGNES_FICHES}
    releve = maquette.releve()
    absents = []
    for c in releve:
        assert c.ou and set(c.ou) <= paragraphes, c.ident
        trouves = {label for label, _ in maquette.lignes_du_motif(lignes, c.motif, c.ou)}
        trouves |= {f for f in c.ou if maquette.lignes_du_motif_fiches(fiches, c.motif, (f,))}
        absents += [(c.ident, label) for label in c.ou if label not in trouves]
    attendus = [(c.ident, label) for c in releve if c.ident in SANS_OBJET_M34 for label in c.ou]
    assert len(attendus) == 8 and sorted(absents) == sorted(attendus)
    # Les six chiffres sans objet se lisent dans chacun de leurs paragraphes une fois les valeurs barrées levées,
    # par la règle de `lignes_du_motif` (aucun n'est déclaré dans une fiche).
    for c in releve:
        if c.ident in SANS_OBJET_M34:
            assert not set(c.ou) & {f for f, _ in maquette.LIGNES_FICHES}, c.ident
            expression = re.compile(r"(?<![\d,])" + re.escape(c.motif.replace("{,}", ",")) + r"(?!\d)")
            barres = {label for label, num in maquette.lignes_paragraphes(lignes)
                      if label in c.ou and expression.search(_lever_barres(lignes[num - 1]).replace("{,}", ","))}
            assert barres == set(c.ou), c.ident
    idents = [c.ident for c in releve]
    assert len(idents) == len(set(idents))


def test_valeurs_barrees_ni_recensees_ni_cherchees(maquette):
    """Une valeur barrée (`\\barre{…}`, CONVENTIONS.md, § 4.3) sort du recensement et de la recherche des motifs."""
    s = maquette.sans_barres
    ligne = r"vaut \barre{0,997497} 0,997390, \barre{$-20{,}63$} et \barre{$\{2\}$ 0,5} ; fin"
    propre = s(ligne)
    assert len(propre) == len(ligne)
    assert "0,997390" in propre and "fin" in propre
    assert not any(x in propre for x in ("0,997497", "20{,}63", "0,5", "barre"))
    assert s("sans barre, 0,5") == "sans barre, 0,5"
    # Accolade échappée : ne ferme ni n'ouvre la valeur barrée.
    assert s(r"\barre{$\}$} 0,1 \barre{\{} 0,2") == " " * 12 + " 0,1 " + " " * 10 + " 0,2"
    with pytest.raises(ValueError):
        s(r"ouvert \barre{0,1 et rien")
    # Sur la spécification, seconde écriture (un niveau d'accolades) : un nombre écrit seulement dans une
    # valeur barrée n'est pas recensé dans son paragraphe ; il y en a (anciens rayons du socle et φ*).
    lignes = maquette.lire_spec()
    recenses = maquette.recenser(lignes)
    seulement_barres = set()
    for label, num in maquette.lignes_paragraphes(lignes):
        texte = lignes[num - 1]
        barres = {n for m in re.finditer(r"\\barre\{((?:[^{}]|\{[^{}]*\})*)\}", texte) for n in _nombres(m.group(1))}
        seulement_barres |= {(label, num, n) for n in barres - _nombres(maquette.sans_barres(texte))}
    assert {("sec:finances_publiques-impots", "0,131"), ("sec:banque_centrale-conditions", "0,997497")} \
        <= {(label, n) for label, _, n in seulement_barres}
    assert not seulement_barres & set(recenses)


def _nombres(texte):
    return {x.replace("{,}", ",") for x in re.findall(r"\d+(?:\{,\}|,)\d+", texte)}


def test_points_fixes_et_racine_nominale(maquette):
    r = maquette.calculer()
    assert max(r["residus"].values()) <= maquette.TOL_POINT_FIXE
    assert max(r["racines_nominales"].values()) <= maquette.TOL_RACINE_NOMINALE
    assert maquette.controles_tenus(r) == []
    for x in r["releve"]:
        assert x["verdict"] in ("reproduit", "écart", "sans objet")
        assert (x["remesure"] is None) == (x["verdict"] == "sans objet")
        assert x["remesure"] is None or math.isfinite(x["remesure"])


# Chiffres du relevé en écart, liste exacte (#65) : la valeur de la fiche 5 à n_a = 4 (cause non établie). Les
# 8 rayons φ ≠ 0 de la table φ de la fiche 9, en écart depuis l'amendement de E12 (historique de la spécification,
# ligne 30), sont republiés à la table T1 dans la fiche (reprise du rang 9, constat m1 de `macro`) et reproduits.
# Aucun chiffre en vigueur de la spécification n'y figure : un chiffre en vigueur qui passe en écart,
# ou en « sans objet », fait échouer la batterie ; un écart qui se résorbe aussi, la liste est alors à revoir.
ECARTS_ATTENDUS = frozenset({"instabilite17.a.n_a4.hausse"})
#
# Calibration du socle (M34) : la spécification republiée au rang 9 (`docwriter`, commits 9cb6ab9 à 1f86f0a) écrit
# en vigueur les chiffres de la table T1 (#92, #55, #130, #62, #45), tous reproduits. Six chiffres sont sans objet à
# la table T1 (λ_w = 0,18, #45) et barrés dans chacun de leurs paragraphes : les frontières en ν_H et h de
# l'instabilité 17 (rayon de la lecture (a) sous 1 sur [0,3 ; 1] ; « sans objet », M34), les périodes de la lecture
# (a) (racine réelle à θ_H = 0,8) et les périodes de la branche ×2 (racines réelles). Ils restent au relevé, publiés
# « sans objet » ; `test_chaque_chiffre_releve_a_sa_ligne` les lit barrés.
SANS_OBJET_M34 = frozenset({
    "instabilite17.frontiere_h",
    "instabilite17.frontiere_nu_H",
    "menages_inflation.a.periode.max",
    "menages_inflation.a.periode.min",
    "socle.marge_conjointe.x2.baisse.periode",
    "socle.marge_conjointe.x2.hausse.periode",
})
NON_REPRODUITS_ATTENDUS = ECARTS_ATTENDUS | SANS_OBJET_M34
#
# #45 (λ_w = 1 → 0,18, M34) : les variantes « toutes÷2 », « toutes×2 » et « lambda_w×2 » de la boucle salaires --
# prix prennent λ_w relative à la table, × 0,5 et × 2, comme les autres vitesses (décision du mainteneur du
# 17/11/2026) : elles fixaient λ_w en valeur absolue, 0,5 et 2,0, et « toutes÷2 » accélérait λ_w à 0,18.
VARIANTES_RELATIVES_45 = ("toutes÷2", "toutes×2", "lambda_w×2")


def test_ensemble_des_ecarts_fige(maquette):
    """Liste exacte : 7 chiffres non reproduits sur 148, 1 en écart, antérieur à M34 (`ECARTS_ATTENDUS`), et 6 sans
    objet à la table T1 (`SANS_OBJET_M34`) ; tous les autres, dont ceux republiés à la table T1, sont reproduits."""
    r = maquette.calculer()
    assert len(r["releve"]) == 148
    assert len(ECARTS_ATTENDUS) == 1 and len(SANS_OBJET_M34) == 6 and not ECARTS_ATTENDUS & SANS_OBJET_M34
    assert {x["ident"] for x in r["releve"] if not x["reproduit"]} == NON_REPRODUITS_ATTENDUS
    assert {x["ident"] for x in r["releve"] if x["verdict"] == "écart"} == ECARTS_ATTENDUS
    assert {x["ident"] for x in r["releve"] if x["verdict"] == "sans objet"} == SANS_OBJET_M34


# Mesures mises en cache qui lisent `BASE` à l'appel (lecture du module, 17/11/2026) : à vider quand `BASE` est
# remplacée. Les autres caches du module sont indexés par des paramètres complets (`etat_socle`, `carte_socle`,
# `lectures`) ou ne lisent pas la table (`_paragraphes`) ; `test_caches_lisant_la_table_recenses` tient la liste.
CACHES_LISANT_BASE = ("carte_offre", "carte_investissement", "carte_menages", "grille_socle", "complements_socle",
                      "marge_conjointe", "frontiere_marge", "phi_star", "variantes_F")
CACHES_INDEXES_PAR_LES_PARAMETRES = ("etat_socle", "carte_socle", "lectures", "_paragraphes")


def test_caches_lisant_la_table_recenses(maquette):
    """Chaque fonction mise en cache du module est classée : lit `BASE` à l'appel, ou indexée par ses paramètres."""
    caches = {nom for nom, f in vars(maquette).items() if callable(f) and hasattr(f, "cache_clear")}
    assert caches == set(CACHES_LISANT_BASE) | set(CACHES_INDEXES_PAR_LES_PARAMETRES)


def _base_remplacee(maquette, monkeypatch, **champs):
    """Remplace `BASE` de la maquette et vide, avant et après le test, chaque mesure mise en cache qui lit `BASE` à
    l'appel (`CACHES_LISANT_BASE`). Réserve : les défauts `lambda_w=BASE.lambda_w` de `carte_offre` et
    `nu_H=BASE.nu_H` de `carte_menages` sont figés à l'import ; aucun test sous ces fixtures n'appelle ces cartes sans
    passer `lambda_w` (ou `nu_H`) explicitement."""
    caches = [getattr(maquette, nom) for nom in CACHES_LISANT_BASE]
    for c in caches:
        c.cache_clear()
    monkeypatch.setattr(maquette, "BASE", dataclasses.replace(maquette.BASE, **champs))
    yield maquette
    monkeypatch.undo()
    for c in caches:
        c.cache_clear()


@pytest.fixture
def a_nu_H_un(maquette, monkeypatch):
    """Maquette sur la table d'avant #62 et #45 (ν_H = 1, λ_w = 1 ; état E2, ϑ = 0,15) : les propriétés de la branche
    ×2 sans a_I y sont construites (à ν_H = 1,1 et λ_w = 1, cette branche sort de la région stable du régime de
    hausse ; à λ_w = 0,18, ses racines (c) sont réelles dans les deux régimes)."""
    yield from _base_remplacee(maquette, monkeypatch, nu_H=1.0, lambda_w=1.0)


@pytest.fixture
def a_lambda_w_un(maquette, monkeypatch):
    """Maquette sur la table d'avant #45 (λ_w = 1, ν_H = 1,1 ; état E3) : les propriétés de la frontière de la marge
    conjointe et de la branche ×2 sans a_I construites au rang 6 (#62) y sont gardées."""
    yield from _base_remplacee(maquette, monkeypatch, lambda_w=1.0)


def test_branche_x2_sans_a_I_explosive_en_hausse_avant_lambda_w(a_lambda_w_un):
    """À ν_H = 1,1 et λ_w = 1 (#62, avant #45), la frontière du régime de hausse est sous 2 : la lecture (c) de la
    branche ×2 en hausse, à a_I ×0,001 et ×0,01, est une paire complexe de module > 1 ; l'écart à 1 de la racine
    réelle est sans objet (None), jamais une valeur silencieuse."""
    maquette = a_lambda_w_un
    assert maquette.BASE.nu_H == 1.1 and maquette.BASE.lambda_w == 1.0
    assert maquette.frontiere_marge("hausse") < 2.0
    for f_aI in (1e-3, 1e-2):
        l = maquette.lectures(maquette._ensemble_sans_aI(f_aI), "hausse")
        assert maquette.nature_racine(l.suivante)[0] == "complexe" and l.rayon_c > 1.0
        assert maquette.ecart_racine_reelle(f_aI) is None


def test_variantes_de_vitesse_salaires_prix_relatives_a_la_table(maquette):
    """Les variantes « toutes÷2 », « toutes×2 » et « lambda_w×2 » de la boucle salaires -- prix prennent λ_w relative
    à la table (décision du mainteneur du 17/11/2026, #45). À la table calibrée (λ_w = 0,18 ≠ 1, où relatif et absolu
    se distinguent), chacun des six rayons de `releve()` égale l'extrême sur m = 0,5 à 0,8 calculé avec
    λ_w = `BASE.lambda_w` × k (k = 0,5 ou 2) et diffère de celui calculé avec l'ancienne valeur absolue (0,5 ou 2,0)."""
    base = maquette.BASE
    assert base.lambda_w == 0.18
    autres = {"toutes÷2": {"lambda_v": 1.5, "lambda_IN": 0.75, "lambda_mu": 0.6},
              "toutes×2": {"lambda_v": 6.0, "lambda_IN": 3.0, "lambda_mu": 2.4}, "lambda_w×2": {}}
    k = {"toutes÷2": 0.5, "toutes×2": 2.0, "lambda_w×2": 2.0}
    assert tuple(autres) == VARIANTES_RELATIVES_45
    releve = {c.ident: c for c in maquette.releve()}
    for nom in VARIANTES_RELATIVES_45:
        def rayons(lambda_w, nom=nom):
            return [maquette.spectre(maquette.carte_offre(m, "regle", True, lambda_w=lambda_w, **autres[nom])).rayon
                    for m in maquette.M4]
        relatifs, absolus = rayons(base.lambda_w * k[nom]), rayons(k[nom])
        for quel, extreme in (("min", min), ("max", max)):
            publie = releve[f"salaires_prix.rayon.{nom}.{quel}"].calcul()
            assert publie == extreme(relatifs), (nom, quel)
            assert abs(publie - extreme(absolus)) > 1e-3, (nom, quel)


def test_branche_x2_sans_a_I_racine_reelle_a_la_table_calibree(maquette):
    """À la table calibrée (λ_w = 0,18, #45), la frontière du régime de hausse revient au-delà de 2 (2,7826) : la
    lecture (c) de la branche ×2 sans a_I est une racine réelle positive sous 1 dans les deux régimes, à a_I ×0,001
    et ×0,01, et son écart à 1 est mesurable (8,61e−6 et 8,69e−5, à peu près proportionnel à a_I)."""
    assert maquette.BASE.lambda_w == 0.18 and maquette.BASE.nu_H == 1.1
    assert round(maquette.frontiere_marge("hausse"), 4) == 2.7826
    for f_aI in (1e-3, 1e-2):
        for regime in ("hausse", "baisse"):
            l = maquette.lectures(maquette._ensemble_sans_aI(f_aI), regime)
            assert maquette.nature_racine(l.suivante)[0] == "réelle positive" and l.rayon_c < 1.0
    e3, e2 = maquette.ecart_racine_reelle(1e-3), maquette.ecart_racine_reelle(1e-2)
    assert 0 < e3 < e2 < 1e-3 and 9 < e2 / e3 < 11


def test_ecart_a_1_de_la_racine_reelle_proportionnel_a_a_I(a_nu_H_un):
    """Branche ×2 sans a_I, régime de hausse, à ν_H = 1 et λ_w = 1 (`a_nu_H_un`) : la lecture (c) est une racine
    réelle sous 1 dont l'écart à 1 est à peu près proportionnel à a_I (a_I ÷ 1000 et ÷ 100) ; en régime de baisse,
    la lecture (c) est une paire."""
    maquette = a_nu_H_un
    e3, e2 = maquette.ecart_racine_reelle(1e-3), maquette.ecart_racine_reelle(1e-2)
    assert 0 < e3 < e2 < 1e-3
    assert 9 < e2 / e3 < 11
    assert e3 == 1 - maquette.lectures(maquette._ensemble_sans_aI(), "hausse").rayon_c
    baisse = maquette.lectures(maquette._ensemble_sans_aI(), "baisse").suivante
    assert maquette.nature_racine(baisse)[0] == "complexe"
    assert maquette._mise_a_echelle(None, 6) is None


CLOTURE = {
    "N_m1": "N", "U_m1": "U", "W_m1": "W", "ve": "ve_1", "IN_vol": "IN_vol_1", "IN": "IN_1", "K_vol": "K_vol_1",
    "K": "K_1", "ti": "ti_1", "y_m1": "y", "T_F_m1": "T_F", "L": "L_1", "D_F": "D_F_1", "YD_m1": "YD",
    "D_H": "D_H_1", "i_L": "i_L_1", "i_D": "i_D_1", "E_Bk": "E_Bk_1_flux", "L_CB": "L_CB_1", "Res": "Res_1",
    "B_Bk": "B_Bk_1", "B_CB": "B_CB_1", "M_G": "M_G_1", "E_CB": "E_CB_1_flux", "r_hat": "r_hat_1",
    "pi_e": "pi_e_1", "Y_HS_m1": "Y_HS", "P_1": "P_0",
}


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
@pytest.mark.parametrize("regime", ["hausse", "baisse"])
def test_carte_du_socle_egale_un_pas(maquette, pi, regime):
    """Deux transcriptions des règles : même clôture sur l'état résolu et sur des états perturbés du régime."""
    es = maquette.es
    par = maquette.parametres_socle(pi)
    e, o = maquette.etat_socle(par)
    carte = maquette.carte_socle(par, regime)
    n = par.n_a
    assert set(carte.noms) == set(CLOTURE) | {f"P_{u}" for u in range(1, n + 2)}
    rng = np.random.default_rng(65)
    compares = 0
    for k in range(40):
        x = carte.x0 if k == 0 else carte.x0 * (1 + 1e-3 * rng.standard_normal(len(carte.x0)))
        o2 = dict(o)
        o2["registre"] = list(x[:n + 1])
        o2.update({nom: x[n + 1 + i] for i, nom in enumerate(carte.noms[n + 1:])})
        s = es.un_pas(o2, par)
        if (s["N"] == s["N_star"]) != (regime == "hausse"):
            continue  # un_pas applique T4 avec son coude : état d'un autre régime
        x1 = dict(zip(carte.noms, carte.pas(x)))
        echelle = 1e-9 * e["PIB"]
        ecart = max(abs(x1[k] - s[v]) / max(abs(s[v]), echelle) for k, v in CLOTURE.items())
        assert ecart <= 1e-12, (k, ecart)
        compares += 1
    assert compares >= 5


def test_jacobienne_redonne_la_boucle_propre_de_la_production(maquette):
    """À demande exogène (m = 0), valeurs propres 1 − λ_v/n_a et (1 − λ_IN/n_a)/(1 + g)^{1/n_a} (sec:production-conditions)."""
    carte = maquette.carte_offre(0.0)
    valeurs = sorted(abs(np.linalg.eigvals(maquette.jacobienne(carte))))
    par, n = maquette.BASE, 12
    attendues = sorted([0.0, 1 - par.lambda_v / n, (1 - par.lambda_IN / n) / (1 + par.g_pr) ** (1 / n)])
    assert np.allclose(valeurs, attendues, atol=1e-8)


def test_frontiere_refuse_un_intervalle_non_encadrant(maquette):
    with pytest.raises(ValueError):
        maquette.frontiere(lambda x: 0.5, 0.0, 1.0)


def test_remesure_sans_objet_publiee(maquette, capsys):
    """Une remesure None (racine réelle, rayon ≥ 1) est publiée « sans objet », jamais convertie en nombre."""
    lignes = maquette.lire_spec()
    c = maquette.Chiffre("essai.sans_objet", "275", "275", "période", "socle", "essai", lambda: None)
    x = maquette.evaluer(c, lignes)
    assert x["remesure"] is None and x["ecart"] is None and x["verdict"] == "sans objet" and not x["reproduit"]
    assert maquette._extremes(lambda a: None if a == 2 else 1.0, (1, 2, 3), "min")() is None
    assert maquette._moins(96, None) is None
    r = maquette.calculer()
    r["releve"] = [x]
    maquette.afficher(r)
    sortie = capsys.readouterr().out
    assert "essai.sans_objet" in sortie and "sans objet" in sortie.split("essai.sans_objet")[1].splitlines()[0]
    assert "1 sans objet : essai.sans_objet" in sortie


# Grille G de la fiche du bloc banque centrale (docs/blocs/banque_centrale.md, « Grille G ») : symboles de la
# fiche et paramètres du socle. k_I de la fiche est a_I (BC2).
SYMBOLES = {"λ_v": "lambda_v", "λ_IN": "lambda_IN", "λ_w": "lambda_w", "λ_N": "lambda_N", "λ_μ": "lambda_mu",
            "λ_H": "lambda_H", "λ_ti": "lambda_ti", "λ_e": "lambda_e", "k_I": "a_I", "a_π": "a_pi", "a_U": "a_U",
            "ψ_ξ": "psi_xi", "β": "beta", "η_r": "eta_r"}
# Lignes de la liste « Grille G » dont le texte fixe la composition des branches sans liste de symboles.
LIGNES_FIXES = ("- calibration indicative ;", "- toutes les vitesses ×0,5, puis ×2 ;", "- deux régimes de l'emploi.")


def _grille_de_la_fiche():
    """Liste « Grille G » de la fiche, ligne à ligne, jusqu'à la ligne vide : (vitesses, gains, lignes fixes)."""
    texte = (RACINE / "docs" / "blocs" / "banque_centrale.md").read_text(encoding="utf-8").splitlines()
    i = texte.index("**Grille G** :") + 1
    bloc = []
    while texte[i].strip():
        bloc.append(texte[i])
        i += 1
    listes, fixes = {}, []
    for ligne in bloc:
        for debut in ("- chaque vitesse ×0,5 et ×2", "- chaque gain ×0,5 et ×2"):
            if ligne.startswith(debut):
                listes[debut] = [SYMBOLES[x.strip().rstrip(";").strip()] for x in ligne.split(":", 1)[1].split(",")]
                break
        else:
            fixes.append(ligne)
    return listes["- chaque vitesse ×0,5 et ×2"], listes["- chaque gain ×0,5 et ×2"], fixes


def test_grille_conforme_a_la_fiche(maquette):
    vitesses, gains, fixes = _grille_de_la_fiche()
    # Toute ligne de la liste est lue : une ligne qui change (« toutes les vitesses et les gains », une branche
    # ajoutée) fait échouer le test, au lieu d'une composition codée en dur.
    assert fixes == list(LIGNES_FIXES)
    champs = {f.name for f in dataclasses.fields(maquette.BASE)}
    assert list(maquette.VITESSES_GRILLE) == vitesses
    assert set(maquette.GAINS_GRILLE) | set(maquette.ABSENTS_GRILLE) == set(gains)
    assert not set(maquette.GAINS_GRILLE) & set(maquette.ABSENTS_GRILLE)
    # Un paramètre absent de la grille codée l'est du socle ; un paramètre ajouté n'est pas dans la fiche.
    assert not set(maquette.ABSENTS_GRILLE) & champs
    assert set(maquette.VITESSES_GRILLE + maquette.GAINS_GRILLE + maquette.AJOUTS_GRILLE) <= champs
    assert not set(maquette.AJOUTS_GRILLE) & set(vitesses + gains)
    branches = dict(maquette.branches_grille())
    attendues = {"calibration": ()}
    for nom in vitesses + list(maquette.GAINS_GRILLE):
        for f in (0.5, 2.0):
            attendues[f"{nom} ×{f:g}"] = ((nom, f),)
    for f in (0.5, 2.0):  # « toutes les vitesses ×0,5, puis ×2 » : la liste de la ligne des vitesses
        attendues[f"vitesses ×{f:g}"] = tuple((nom, f) for nom in vitesses)
    assert branches == attendues
    assert len(branches) == 1 + 2 * (len(vitesses) + len(gains)) + 2 - 2 * len(maquette.ABSENTS_GRILLE)
    ajoutees = dict(maquette.branches_ajoutees())
    assert ajoutees == {f"{nom} ×{f:g}": ((nom, f),) for nom in maquette.AJOUTS_GRILLE for f in (0.5, 2.0)}
    # Les mesures complémentaires (gains ensemble) n'entrent ni dans la grille ni dans le relevé.
    complements = dict(maquette.branches_complementaires())
    assert not set(complements) & (set(branches) | set(ajoutees))
    assert all(nom in maquette.GAINS_ENSEMBLE for fac in complements.values() for nom, _ in fac)
    releve = {c.ident: c for c in maquette.releve()}
    assert "socle.grille.vitesses÷2" in releve and "socle.grille.toutes÷2" not in releve


def test_verdicts_des_deux_grilles(maquette):
    """Grille G, puis G augmentée de ζ : décompte des branches, des branches stables et pire branche."""
    grille = maquette.grille_socle()
    n_G = len(maquette.branches_grille())
    assert [nom for nom, _ in grille] == [nom for nom, _ in maquette.branches_grille() + maquette.branches_ajoutees()]
    v = maquette.verdicts_grille()
    for cle, partie in (("G", grille[:n_G]), ("G + zeta", grille)):
        assert v[cle]["branches"] == len(partie)
        assert v[cle]["stables"] == sum(r < 1 for _, r in partie)
        assert (v[cle]["branche_pire"], v[cle]["pire"]) == max(partie, key=lambda x: x[1])
    releve = {c.ident: c.calcul for c in maquette.releve()}
    assert releve["socle.grille.pire"]() == v["G"]["pire"]
    # Grille synthétique : une branche instable de G, une de ζ ; le pire et le décompte suivent.
    synthetique = tuple((nom, 0.9) for nom, _ in grille)
    synthetique = ((grille[0][0], 1.5),) + synthetique[1:-1] + ((grille[-1][0], 1.2),)
    w = maquette.verdicts_grille(synthetique)
    assert (w["G"]["stables"], w["G"]["pire"], w["G"]["branche_pire"]) == (n_G - 1, 1.5, grille[0][0])
    assert (w["G + zeta"]["stables"], w["G + zeta"]["branches"]) == (len(grille) - 2, len(grille))
    # Chaque branche est la lecture (c), pire des deux régimes, de ses paramètres.
    nom, fac = maquette.branches_ajoutees()[0]
    assert dict(grille)[nom] == maquette.rayon_c(maquette.parametres_socle(0.02, facteurs=dict(fac)))


# Amas des racines nulles (décision du mainteneur du 17/11/2026, rang 6 de la calibration, #62) : les racines
# exactement nulles de J et de J_var (8 dans chacune, aux six cas) ne sont connues qu'au bruit des différences
# finies de la jacobienne (h = 1e−6) : |z| ≤ 1,10e−7 à ν_H = 1,1 (E3), où l'appariement glouton atteint 1,10e−7
# > `TOL_RACINE_MULTIPLE`, et ≤ 1,11e−7 à ν_H = 1 (E2, appariement 1,35e−8). Elles sont appariées par
# multiplicité : même nombre de racines de module ≤ `SEUIL_AMAS_NUL` dans J et J_var. Seuil 1e−5 : marge de 90
# sur le plus grand module mesuré de l'amas (1,10e−7), de 96 sous la plus petite racine non nulle (9,57e−4 à
# π̄ = 0, 2,89e−3 à 2 %, 1,05e−2 à 10 %). L'amas compte 8 racines dans J et J_var aux six cas, à E2 comme à E3.
# Toutes les autres racines restent appariées à `TOL_RACINE_MULTIPLE` (1e−7), avec une marge mince à π̄ = 0 : pire
# écart 9,36e−8 (hausse) et 9,78e−8 (baisse), sur la paire 0,190 ± 0,242i et 0,188 ± 0,250i (module ≈ 0,31) ;
# 2,0e−8 à 2 %, 5,5e−9 à 10 %. C'est du bruit des différences finies, sensible au pas : à π̄ = 0, 2,0e−8 à
# `PAS_RELATIF` = 1e−5 et 2,6e−6 à 1e−7 (mesures du 17/11/2026, pas de la maquette inchangé, 1e−6).
SEUIL_AMAS_NUL = 1e-5
RACINES_DE_L_AMAS_NUL = 8


def _retirer(brutes, variete, tol):
    """Valeurs propres brutes qui ne s'apparient à aucune valeur propre de la variété : amas des racines nulles
    apparié par multiplicité (`SEUIL_AMAS_NUL`), autres racines par appariement glouton à `tol`."""
    amas_brut = sum(abs(z) <= SEUIL_AMAS_NUL for z in brutes)
    amas_variete = sum(abs(z) <= SEUIL_AMAS_NUL for z in variete)
    assert amas_brut == amas_variete == RACINES_DE_L_AMAS_NUL, (amas_brut, amas_variete)
    restantes = [z for z in brutes if abs(z) > SEUIL_AMAS_NUL]
    for z in (z for z in variete if abs(z) > SEUIL_AMAS_NUL):
        i = min(range(len(restantes)), key=lambda q: abs(restantes[q] - z))
        assert abs(restantes[i] - z) <= tol, z
        restantes.pop(i)
    return restantes


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
@pytest.mark.parametrize("regime", ["hausse", "baisse"])
def test_spectre_restreint_retire_les_racines_des_identites(maquette, pi, regime):
    """Sur la variété des identités, les gradients ne portent plus de valeur propre : la restriction retire
    exactement une racine en 1/Γ̄ par identité et garde toutes les autres, racine nominale comprise. Les
    racines en 1/Γ̄ qui restent sont celles des stocks tenus en niveau (lecture (c))."""
    J, J_var, Gs, inv = maquette.jacobiennes_socle(pi, regime)
    n_id = len(maquette.IDENTITES_SOCLE)
    assert J_var.shape == (len(J) - n_id, len(J) - n_id)
    # Chaque gradient est vecteur propre à gauche de valeur propre 1/Γ̄ : la variété est invariante.
    assert np.max(np.linalg.norm(Gs @ J - Gs * inv, axis=1) / np.linalg.norm(Gs, axis=1)) <= maquette.TOL_GAUCHE
    assert maquette.TOL_GAUCHE <= 1e-8
    tol = maquette.TOL_RACINE_MULTIPLE
    retirees = _retirer(np.linalg.eigvals(J), np.linalg.eigvals(J_var), tol)
    assert len(retirees) == n_id and all(abs(z - inv) <= tol for z in retirees)
    s = maquette.lectures_socle(pi, regime)
    assert s.residu_gauche <= maquette.TOL_GAUCHE
    assert s.multiplicite_brute - s.multiplicite_variete == n_id
    assert s.noyau_brut == s.multiplicite_brute  # racines en 1/Γ̄ semi-simples
    # Cause déclarée : une racine en 1/Γ̄ de la variété par stock dont la ligne de la jacobienne est e_i/Γ̄.
    carte = maquette.carte_socle(maquette.parametres_socle(pi), regime)
    tenus = [nom for i, nom in enumerate(carte.noms) if np.max(np.abs(J[i] - inv * np.eye(len(J))[i])) <= 1e-8]
    assert tuple(sorted(tenus)) == s.tenus_en_niveau == maquette.TENUS_ATTENDUS
    assert s.multiplicite_variete == len(s.tenus_en_niveau)
    assert abs(s.suivante - inv) > tol and abs(s.suivante) <= s.rayon_variete
    assert s.rayon_c == abs(s.suivante) <= s.rayon_brut + tol
    assert s.residu_identites <= 1e-12


@pytest.mark.parametrize("pi", [0.0, 0.10])
def test_identites_conformes_a_etat_stationnaire(maquette, pi):
    """Contenu de `IDENTITES_SOCLE` : sur des états perturbés (E^CB ≠ 0 compris), le gradient appliqué aux postes
    de clôture d'`etat_stationnaire.un_pas` vaut E_1_stock − E_1_flux tels que `un_pas` les définit."""
    es = maquette.es
    par = maquette.parametres_socle(pi)
    _, o = maquette.etat_socle(par)
    carte = maquette.carte_socle(par, "hausse")
    n = par.n_a
    G = maquette.gradients_identites(carte)
    noms = [nom for nom, _ in maquette.IDENTITES_SOCLE]
    capitaux = {"bilan de la banque centrale": "E_CB", "bilan des banques": "E_Bk"}
    assert sorted(noms) == sorted(capitaux)
    rng = np.random.default_rng(65)
    i_res, i_LCB = carte.noms.index("Res"), carte.noms.index("L_CB")
    regimes_B7 = set()
    for k in range(10):
        x = carte.x0 + 1e-3 * carte.echelle * rng.standard_normal(len(carte.x0))
        # Deux côtés de B7, une perturbation d'un PIB : refinancement au-delà des réserves (Res_1 = 0,
        # L^CB_1 > 0), puis réserves au-delà du refinancement (L^CB_1 = 0, Res_1 > 0).
        if k % 2:
            x[i_res] = 2 * x[i_LCB] + carte.echelle[i_res]
        else:
            x[i_res], x[i_LCB] = 0.0, x[i_LCB] + carte.echelle[i_LCB]
        o2 = dict(o)
        o2["registre"] = list(x[:n + 1])
        o2.update({nom: x[n + 1 + i] for i, nom in enumerate(carte.noms[n + 1:])})
        s = es.un_pas(o2, par)
        regimes_B7.add(s["Res_1"] > 0)
        cloture = np.array([s[CLOTURE[nom]] if nom in CLOTURE else 0.0 for nom in carte.noms])
        for ligne, nom in enumerate(noms):
            k = capitaux[nom]
            attendu = s[f"{k}_1_stock"] - s[f"{k}_1_flux"]
            assert abs(attendu) > 1e-6 * o["L"]  # l'état perturbé viole l'identité : le test discrimine
            assert abs(G[ligne] @ cloture - attendu) <= 1e-12 * o["L"], (nom, G[ligne] @ cloture, attendu)
    assert regimes_B7 == {False, True}  # chaque coefficient est sollicité : Res_1 > 0 et L^CB_1 > 0 sont vus


def test_code_de_sortie_depend_des_controles(maquette, monkeypatch, capsys):
    """`main` rend 2 dès qu'un contrôle de `controles_tenus` échoue : variété (≤ TOL_GAUCHE), coudes, racines."""
    r = maquette.calculer()
    assert maquette.controles_tenus(r) == []
    for cle, valeur in (("residu_gauche", 10 * maquette.TOL_GAUCHE), ("residu_gauche_variantes", 1.0),
                        ("coude", 10 * maquette.TOL_COUDE), ("coude_variantes", 1.0)):
        r2 = dict(r, controles=dict(r["controles"], **{cle: valeur}))
        assert maquette.controles_tenus(r2), cle
        monkeypatch.setattr(maquette, "calculer", lambda r2=r2: r2)
        assert maquette.main([]) == 2, cle
    lect = {pi: dict(reg) for pi, reg in r["lectures_socle"].items()}
    lect["0"] = dict(lect["0"], hausse=dict(lect["0"]["hausse"], tenus_en_niveau=["E_CB"]))
    assert maquette.controles_tenus(dict(r, lectures_socle=lect))
    # Une racine en 1/Γ̄ de plus que les stocks tenus attendus, stocks tenus inchangés.
    lect = {pi: dict(reg) for pi, reg in r["lectures_socle"].items()}
    lect["0"] = dict(lect["0"], hausse=dict(lect["0"]["hausse"], multiplicite_variete=3))
    assert maquette.controles_tenus(dict(r, lectures_socle=lect))
    # Stocks tenus hors des six cas du socle (grille, compléments, φ, marge, variantes de F).
    r2 = dict(r, controles=dict(r["controles"], tenus_hors_attendus=["grille beta ×2 hausse"]))
    assert maquette.controles_tenus(r2)
    monkeypatch.setattr(maquette, "calculer", lambda r2=r2: r2)
    assert maquette.main([]) == 2
    r2 = dict(r, racines_nominales=dict(r["racines_nominales"], variete_cas_controles=1e-3))
    assert maquette.controles_tenus(r2)
    monkeypatch.setattr(maquette, "calculer", lambda: r)
    assert maquette.main([]) == 0
    capsys.readouterr()


def test_stocks_tenus_et_racine_nominale_sur_chaque_carte_publiee(maquette, monkeypatch):
    """Les contrôles des stocks tenus en niveau et de la racine nominale portent sur chaque carte du socle dont
    une lecture (c) est publiée : six cas, grille augmentée, compléments, table φ et φ*, marge, variantes de F."""
    cas = maquette.cas_controles()
    branches = maquette.branches_grille() + maquette.branches_ajoutees() + maquette.branches_complementaires()
    grille = maquette.branches_grille() + maquette.branches_ajoutees()
    # Marge : frontière des deux régimes, frontière du régime de hausse, ×2, ×2 avec a_I ×0,001 et ×0,01 ;
    # grille G augmentée aussi à π̄ = 0 et 10 % (pires branches publiées).
    attendu = (6 + 2 * len(branches) + 2 * 2 * (len(maquette.PHI_TABLE) + 1) + 2 * 5 + 2 * 2 * len(grille)
               + len(maquette.variantes_F()))
    assert len(cas) == attendu
    variantes = {(v["configuration"], v["lambda_ti"], v["taux"], v["B6"], v["financement"], v["regime"])
                 for v in maquette.variantes_F()}
    assert variantes <= {(e.split()[1], par.lambda_ti, t, B6, f, r) for e, par, r, t, f, B6 in cas
                         if e.startswith("variante")}
    n, hors, nominale = maquette.tenus_et_nominales()
    assert (n, hors) == (len(cas), []) and 0 < nominale <= maquette.TOL_RACINE_NOMINALE
    # Le contrôle discrimine : attendu faux, chaque carte est signalée.
    monkeypatch.setattr(maquette, "TENUS_ATTENDUS", ("E_CB",))
    assert len(maquette.tenus_et_nominales()[1]) == len(cas)
    # Une racine en 1/Γ̄ de plus, stocks tenus attendus : chaque carte est signalée aussi.
    monkeypatch.undo()
    lectures = maquette.lectures
    monkeypatch.setattr(maquette, "lectures", lambda *a: dataclasses.replace(lectures(*a), multiplicite_variete=3))
    assert len(maquette.tenus_et_nominales()[1]) == len(cas)


def test_combinaison_levier_pK_et_depots_ventes(maquette):
    """La combinaison (fiche 6, § 3.N, première ligne) porte les deux écritures : état et carte."""
    combinaison, levier = maquette.LEVIER_PK_DEPOTS_VENTES, "levier_pK.p_hat.ouverture"
    assert maquette.ecritures_financement(combinaison) == (levier, True)
    assert maquette.ecritures_financement(levier) == (levier, False)
    assert maquette.ecritures_financement("depots_ventes") == (None, True)
    assert maquette.ecritures_financement("F") == (None, False)
    with pytest.raises(ValueError):
        maquette.ecritures_financement("inconnu")
    for par in (maquette.parametres_socle(0.02), maquette.parametres_fiche(0.02)):
        etat = maquette.parametres_etat(par, combinaison)
        assert etat.lv == maquette.parametres_etat(par, levier).lv != par.lv
        assert etat.nu_F == maquette.parametres_etat(par, "depots_ventes").nu_F != par.nu_F
        J = maquette.jacobienne(maquette.carte_socle(par, "hausse", "exogene", combinaison, "verse"))
        for seule in (levier, "depots_ventes"):
            J_seule = maquette.jacobienne(maquette.carte_socle(par, "hausse", "exogene", seule, "verse"))
            assert np.max(np.abs(J - J_seule)) > 1e-3


def test_controle_avant_arriere_detecte_un_coude(maquette):
    """Une carte à coude au point fixe (|x|) donne un écart d'ordre 1 ; une carte lisse, d'ordre h."""
    lisse = maquette._carte([("x", 1.0, 1.0, False, 1.0)], lambda x: [1.0 + 0.5 * (x[0] - 1) ** 2], False)
    coude = maquette._carte([("x", 1.0, 1.0, False, 1.0)], lambda x: [1.0 + abs(x[0] - 1)], False)
    assert maquette.ecart_avant_arriere(lisse) <= 10 * maquette.PAS_RELATIF
    assert maquette.ecart_avant_arriere(coude) > maquette.TOL_COUDE


def test_couverture_phi(maquette):
    """φ* est la frontière de la lecture (c) entre φ = 0 (pays joué) et φ = 1 (règle de référence) ; elle
    monte avec l'inflation ; le doublement est ln 2/ln du rayon à φ = 0."""
    phis = {}
    for pi in (0.02, 0.10):
        bas, haut = maquette.rayon_phi(pi, 0.0), maquette.rayon_phi(pi, 1.0)
        assert bas > 1 > haut
        f = phis[pi] = maquette.phi_star(pi)
        assert 0 < f < 1
        assert maquette.rayon_phi(pi, f - 1e-6) > 1 > maquette.rayon_phi(pi, f + 1e-6)
        assert maquette.doublement(bas) == pytest.approx(math.log(2) / math.log(bas), rel=1e-15)
        # L'état résolu ne dépend pas de φ : seule la règle E4 change.
        e0 = maquette.etat_socle(maquette.parametres_socle(pi))[0]
        e1 = maquette.etat_socle(maquette.replace(maquette.parametres_socle(pi), phi=0.0))[0]
        assert e0["D_H"] == e1["D_H"] and e0["T_cou"] == e1["T_cou"] == 0.0
    assert phis[0.10] > phis[0.02]
    assert maquette.doublement(0.999) is None


def test_marge_conjointe_au_dela_de_2_a_la_table_calibree(maquette):
    """À la table calibrée (λ_w = 0,18, #45), la lecture (c) de l'ensemble (β, a_π, η_r) reste sous 1 sur [1 ; 2]
    (0,99746 à ×1, 0,99719 à ×2) et passe 1 à 2,7826, égale à la frontière du régime de hausse : recherchée sur
    `BORNES_MARGE` = [1 ; 3] (décision du mainteneur du 17/11/2026), elle est publiée chiffrée, reproduite depuis
    la republication du rang 9. Les racines (c) à ×2 sont réelles positives sous 1, sans période."""
    m = maquette.marge_conjointe()
    assert maquette.BORNES_MARGE == (1.0, 3.0)
    assert maquette.rayon_c(maquette._ensemble(1.0)) < 1 and maquette.rayon_c(maquette._ensemble(2.0)) < 1
    assert round(m["facteur"], 4) == round(maquette.frontiere_marge("hausse"), 4) == 2.7826
    for x in m["x2"].values():
        assert x["nature"] == "réelle positive" and x["periode"] is None and x["rayon"] < 1
    assert max(x["rayon"] for x in m["x2"].values()) == maquette.rayon_c(maquette._ensemble(2.0))
    c = {c.ident: c for c in maquette.releve()}["socle.marge_conjointe.facteur"]
    assert maquette.evaluer(c, maquette.lire_spec())["verdict"] == "reproduit"


def test_frontiere_ou_aucune(maquette):
    """`frontiere_ou_aucune` : la frontière de `frontiere` si le rayon passe 1 sur l'intervalle ; sans objet (None)
    si le rayon, fini, est sous 1 aux deux bornes (stable sur l'intervalle) ; erreur explicite s'il est au-dessus de
    1 aux deux bornes (instable sur tout l'intervalle) ; un rayon non fini ou égal à 1 aux bornes reste refusé
    (intervalle non encadrant), jamais converti en « sans objet »."""
    assert maquette.frontiere_ou_aucune(lambda x: 0.5 + x, 0.0, 1.0) == pytest.approx(0.5, abs=1e-12)
    assert maquette.frontiere_ou_aucune(lambda x: 0.5, 0.0, 1.0) is None
    with pytest.raises(ValueError, match="instable sur tout l'intervalle"):
        maquette.frontiere_ou_aucune(lambda x: 1.5, 0.0, 1.0)
    for rayon in (math.nan, math.inf, 1.0):
        with pytest.raises(ValueError, match="non encadrant"):
            maquette.frontiere_ou_aucune(lambda x, rayon=rayon: rayon, 0.0, 1.0)


def test_marge_conjointe_est_une_frontiere(a_lambda_w_un):
    """À λ_w = 1 (`a_lambda_w_un`, avant #45), la frontière de la marge conjointe est dans `BORNES_MARGE` ; la
    bissection sur [1 ; 3] la rend égale, à 1e−12 près, à celle sur [1 ; 2], intervalle d'avant le 17/11/2026."""
    maquette = a_lambda_w_un
    m = maquette.marge_conjointe()
    f = m["facteur"]
    sur_1_2 = maquette.frontiere(lambda x: maquette.rayon_c(maquette._ensemble(x)), 1.0, 2.0)
    assert abs(f - sur_1_2) <= 1e-12 and round(f, 4) == 1.7013
    base, ens = maquette.parametres_socle(0.02), maquette._ensemble(1.5)
    modifies = {c.name for c in dataclasses.fields(base) if getattr(base, c.name) != getattr(ens, c.name)}
    assert modifies == set(maquette.GAINS_ENSEMBLE) == {"beta", "a_pi", "eta_r"}
    assert all(getattr(ens, nom) == 1.5 * getattr(base, nom) for nom in modifies)
    assert maquette.BORNES_MARGE[0] < f < maquette.BORNES_MARGE[1]
    assert maquette.rayon_c(maquette._ensemble(f - 1e-6)) < 1 < maquette.rayon_c(maquette._ensemble(f + 1e-6))
    assert max(x["rayon"] for x in m["x2"].values()) == maquette.rayon_c(maquette._ensemble(2.0))


def test_frontiere_de_la_marge_en_regime_de_hausse(maquette):
    """La frontière du régime de hausse sépare la lecture (c) de ce régime de part et d'autre de 1, et n'est pas
    en deçà de la frontière du pire des deux régimes ; recherchée sur `BORNES_MARGE_HAUSSE` = [1 ; 3] (décision du
    mainteneur du 17/11/2026, #130 : à ϑ = 0,15 et ν_H = 1 elle dépasse 2 ; à ν_H = 1,1, #62, elle revient
    à 1,9693 ; à λ_w = 0,18, #45, elle vaut 2,7826)."""
    f_h = maquette.frontiere_marge("hausse")
    assert maquette.BORNES_MARGE_HAUSSE == (1.0, 3.0) and maquette.BORNES_MARGE == (1.0, 3.0)
    assert maquette.BORNES_MARGE_HAUSSE[0] < f_h < maquette.BORNES_MARGE_HAUSSE[1]
    assert round(f_h, 4) == 2.7826
    rayon = lambda f: maquette.lectures(maquette._ensemble(f), "hausse").rayon_c  # noqa: E731
    assert rayon(f_h - 1e-6) < 1 < rayon(f_h + 1e-6)
    assert f_h >= maquette.marge_conjointe()["facteur"]


def test_paire_sous_la_racine_reelle_a_a_I_reduit(a_nu_H_un):
    """À ν_H = 1 (`a_nu_H_un` ; la frontière du régime de hausse y est au-delà de 2), à a_I ×0,001, la lecture (c)
    en hausse est une racine réelle, sous laquelle se trouve la paire complexe relevée à côté."""
    maquette = a_nu_H_un
    par = maquette._ensemble_sans_aI()
    assert par == maquette.parametres_socle(0.02, facteurs={"beta": 2.0, "a_pi": 2.0, "eta_r": 2.0, "a_I": 1e-3})
    z = maquette.lectures(par, "hausse").suivante
    assert maquette.nature_racine(z)[0] == "réelle positive"
    J_var = maquette.jacobiennes_carte(maquette.carte_socle(par, "hausse"), par)[1]
    assert maquette.module_paire(np.linalg.eigvals(J_var)) < abs(z)


@pytest.mark.parametrize("rayon", [math.nan, math.inf, 1.0])
def test_frontiere_marge_refuse_un_rayon_non_fini_ou_egal_a_un(maquette, monkeypatch, rayon):
    """Un rayon non fini ou égal à 1 aux bornes est refusé par `frontiere` (intervalle non encadrant), jamais
    converti en frontière."""
    monkeypatch.setattr(maquette, "lectures", lambda *a: SimpleNamespace(rayon_c=rayon))
    maquette.frontiere_marge.cache_clear()
    try:
        with pytest.raises(ValueError, match="non encadrant"):
            maquette.frontiere_marge("hausse")
    finally:
        monkeypatch.undo()
        maquette.frontiere_marge.cache_clear()


def test_module_paire_sans_paire_est_sans_objet(maquette):
    """Un spectre sans paire complexe rend « sans objet » (None), sans lever d'erreur ni perdre le relevé."""
    assert maquette.module_paire(np.array([0.5 + 0j, 0.9 + 0j])) is None
    assert maquette.module_paire(np.array([0.99, 0.9 + 0.1j, 0.9 - 0.1j])) == abs(0.9 + 0.1j)
    c = maquette.Chiffre("essai.paire", "0,9993", "0,9993", "racine", "socle", "essai",
                         lambda: maquette.module_paire(np.array([0.5 + 0j])))
    assert maquette.evaluer(c, maquette.lire_spec())["verdict"] == "sans objet"


def test_point_fixe_controle_sur_chaque_carte_publiee(maquette, monkeypatch):
    """Le résidu du point fixe est contrôlé sur chaque carte de `cas_controles`, dont celles de la grille aux
    trois π̄, de la marge conjointe (frontières, ×2, a_I ×0,001), et entre dans le code de sortie."""
    etiquettes = [e for e, *_ in maquette.cas_controles()]
    assert {"marge ×2, a_I ×0,001", "marge ×2, a_I ×0,01", f"marge ×{maquette.frontiere_marge('hausse'):g}",
            "grille zeta ×0.5, π̄ = 0", "grille eta_r ×2, π̄ = 0.1"} <= set(etiquettes)
    r = maquette.calculer()
    assert r["residus"]["cas_controles"] == maquette.residu_cas_controles() <= maquette.TOL_POINT_FIXE
    # Chaque carte compte : un résidu sur la seule carte a_I ×0,001 remonte au contrôle.
    visee = maquette.carte_socle(maquette._ensemble_sans_aI(), "hausse", "regle", "F", "regle")
    residu = maquette.residu_point_fixe
    monkeypatch.setattr(maquette, "residu_point_fixe", lambda c: 1.0 if c is visee else residu(c))
    assert maquette.residu_cas_controles() == 1.0
    monkeypatch.undo()
    r2 = dict(r, residus=dict(r["residus"], cas_controles=1.0))
    assert maquette.controles_tenus(r2)


def _ligne_de(carte, nom):
    return carte.noms.index(nom)


def test_variantes_de_F_methode(maquette):
    """Seconde écriture des variantes de F : point stationnaire propre, règle effectivement changée, taux tenu
    (lignes nulles), branches de B6 et contrôle des coudes."""
    par = maquette.parametres_socle(0.02)
    J_F = maquette.jacobienne(maquette.carte_socle(par, "hausse"))
    for financement in maquette.FINANCEMENTS:
        etat = maquette.parametres_etat(par, financement)
        carte = maquette.carte_socle(par, "hausse", "regle", financement)
        assert maquette.residu_point_fixe(carte) <= maquette.TOL_POINT_FIXE
        if financement == "F":
            assert etat == par and np.array_equal(maquette.jacobienne(carte), J_F)
            continue
        assert etat != par
        assert np.max(np.abs(maquette.jacobienne(carte) - J_F)) > 1e-3  # la variante change la carte
        # Le point fixe de la variante n'est pas celui de F : l'état de F n'est pas stationnaire sous la variante.
        decalee = dataclasses.replace(carte, x0=maquette.carte_socle(par, "hausse").x0)
        assert maquette.residu_point_fixe(decalee) > 1e3 * maquette.TOL_POINT_FIXE
    for taux, figes in (("exogene", ("i_L", "i_D", "r_hat")), ("exogene_ancre", ("i_L", "i_D", "r_hat", "pi_e"))):
        carte = maquette.carte_socle(par, "hausse", taux)
        J = maquette.jacobienne(carte)
        assert all(np.max(np.abs(J[_ligne_de(carte, nom)])) == 0.0 for nom in figes)
        libres = set(("i_L", "i_D", "r_hat", "pi_e")) - set(figes)
        assert all(np.max(np.abs(J[_ligne_de(carte, nom)])) > 0 for nom in libres)
    # Au socle (ϑ > 0), le plancher de B6 est inactif : la règle écrite et la branche « verse » coïncident.
    assert np.array_equal(maquette.jacobienne(maquette.carte_socle(par, "hausse", B6="verse")), J_F)
    # Dans « fiche », B6 est à son coude : la règle écrite le franchit, chaque branche non.
    fiche = maquette.parametres_fiche(0.02)
    e = maquette.etat_socle(fiche)[0]
    assert e["E_Bk"] == 0.0 and e["Pi_Bk"] == 0.0 and abs(e["i_L"] - 0.03) < 1e-15 and abs(e["i_D"] - 0.03) < 1e-15
    assert maquette.ecart_avant_arriere(maquette.carte_socle(fiche, "hausse", B6="regle")) > maquette.TOL_COUDE
    for B6 in maquette.B6_CONFIGURATION["fiche"]:
        assert maquette.ecart_avant_arriere(maquette.carte_socle(fiche, "hausse", B6=B6)) <= maquette.TOL_COUDE
    with pytest.raises(ValueError):
        maquette.carte_socle(par, "hausse", "regle", "inconnu")


def test_variantes_de_F_publiees(maquette):
    """Chaque combinaison déclarée est publiée une fois, avec un point fixe tenu et une nature cohérente."""
    v = maquette.variantes_F()
    cles = [(x["configuration"], x["lambda_ti"], x["taux"], x["B6"], x["financement"], x["regime"]) for x in v]
    assert len(cles) == len(set(cles))
    attendu = sum(len(maquette.LAMBDA_TI_F) * len(maquette.TAUX_SOCLE) * len(b6) * len(maquette.FINANCEMENTS) * 2
                  for b6 in maquette.B6_CONFIGURATION.values())
    assert len(v) == attendu
    for x in v:
        assert x["residu"] <= maquette.TOL_POINT_FIXE and x["coude"] <= maquette.TOL_COUDE
        z = complex(*x["racine"])
        assert x["rayon"] == abs(z)
        assert (x["nature"], x["periode"]) == maquette.nature_racine(z)
    assert maquette.nature_racine(complex(-1.5, 0.0)) == ("réelle négative", 2.0)
    assert maquette.nature_racine(complex(0.5, 0.0)) == ("réelle positive", None)
