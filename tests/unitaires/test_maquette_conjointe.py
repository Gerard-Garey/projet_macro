"""Tests de la maquette linéarisée de la boucle conjointe (issue #65).

Propriétés de l'outil, écrites avant l'essai par le brief de #65 : il
n'importe ni `src/` ni `archive/` ; il est déterministe ; il s'exécute en
quelques secondes ; son relevé couvre chaque chiffre recensé dans les
paragraphes de la spécification qui citent des boucles conjointes. S'y
ajoutent deux contrôles de la méthode : la carte du socle est une seconde
transcription des règles, qui rend la même clôture qu'`etat_stationnaire.un_pas`
sur l'état résolu et sur des états perturbés ; la jacobienne redonne les
valeurs propres analytiques de la boucle propre du bloc production
(`sec:production-conditions`). Aucun test ne fige une valeur publiée : leur
reproduction est publiée par le script et relève du visa de `macro`.
"""

import ast
import importlib.util
import math
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pytest

RACINE = Path(__file__).resolve().parents[2]
SCRIPT = RACINE / "outils" / "maquette_conjointe.py"
DUREE_MAX = 10.0  # secondes, « quelques secondes » (brief de #65), exécution complète en sous-processus


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
    # Seul module du dépôt chargé par son chemin : le script d'état stationnaire.
    assert '"etat_stationnaire"' in SCRIPT.read_text(encoding="utf-8")


def test_deterministe_et_rapide():
    sorties, durees = [], []
    for _ in range(2):
        debut = time.perf_counter()
        r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, cwd=RACINE, check=False)
        durees.append(time.perf_counter() - debut)
        assert r.returncode == 0, r.stderr
        sorties.append(r.stdout)
    assert sorties[0] == sorties[1]
    assert max(durees) < DUREE_MAX


def test_releve_couvre_chaque_chiffre_recense(maquette):
    lignes = maquette.lire_spec()
    publies = {c.publie.replace("{,}", ",") for c in maquette.releve()}
    recenses = maquette.recenser(lignes)
    assert recenses
    manquants = [x for x in recenses if x[2] not in publies and (x[0], x[2]) not in maquette.EXCLUS]
    assert manquants == []
    # Aucune exclusion périmée : chacune désigne un nombre encore écrit dans son paragraphe.
    cles = {(label, nombre) for label, _, nombre in recenses}
    assert set(maquette.EXCLUS) <= cles


def test_chaque_chiffre_releve_a_sa_ligne(maquette):
    lignes = maquette.lire_spec()
    sans_ligne = [c.ident for c in maquette.releve() if not maquette.lignes_du_motif(lignes, c.motif)]
    assert sans_ligne == []
    idents = [c.ident for c in maquette.releve()]
    assert len(idents) == len(set(idents))


def test_points_fixes_et_racine_nominale(maquette):
    r = maquette.calculer()
    assert max(r["residus"].values()) <= maquette.TOL_POINT_FIXE
    assert max(r["racines_nominales"].values()) <= maquette.TOL_RACINE_NOMINALE
    for x in r["releve"]:
        assert x["verdict"] in ("reproduit", "écart", "sans objet")
        assert (x["remesure"] is None) == (x["verdict"] == "sans objet")
        assert x["remesure"] is None or math.isfinite(x["remesure"])


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


def _liste_de_la_fiche(debut):
    texte = (RACINE / "docs" / "blocs" / "banque_centrale.md").read_text(encoding="utf-8").splitlines()
    i = texte.index("**Grille G** :")
    ligne = next(l for l in texte[i:i + 8] if l.startswith(debut))
    return [SYMBOLES[s.strip().rstrip(";").strip()] for s in ligne.split(":", 1)[1].split(",")]


def test_grille_conforme_a_la_fiche(maquette):
    import dataclasses
    vitesses = _liste_de_la_fiche("- chaque vitesse ×0,5 et ×2")
    gains = _liste_de_la_fiche("- chaque gain ×0,5 et ×2")
    champs = {f.name for f in dataclasses.fields(maquette.BASE)}
    assert list(maquette.VITESSES_GRILLE) == vitesses
    assert set(maquette.GAINS_GRILLE) | set(maquette.ABSENTS_GRILLE) == set(gains)
    assert not set(maquette.GAINS_GRILLE) & set(maquette.ABSENTS_GRILLE)
    # Un paramètre absent de la grille codée l'est du socle ; un paramètre ajouté est publié hors grille.
    assert not set(maquette.ABSENTS_GRILLE) & champs
    assert set(maquette.VITESSES_GRILLE + maquette.GAINS_GRILLE + maquette.HORS_GRILLE) <= champs
    assert not set(maquette.HORS_GRILLE) & set(vitesses + gains)
    branches = dict(maquette.branches_grille())
    attendues = {"calibration": ()}
    for nom in vitesses + list(maquette.GAINS_GRILLE):
        for f in (0.5, 2.0):
            attendues[f"{nom} ×{f:g}"] = ((nom, f),)
    for f in (0.5, 2.0):  # « toutes les vitesses » : les gains n'y entrent pas
        attendues[f"vitesses ×{f:g}"] = tuple((nom, f) for nom in vitesses)
    assert branches == attendues
    assert len(branches) == 1 + 2 * (len(vitesses) + len(gains)) + 2 - 2 * len(maquette.ABSENTS_GRILLE)
    # Les mesures complémentaires (ζ, gains ensemble) n'entrent ni dans la grille ni dans le relevé.
    complements = dict(maquette.branches_complementaires())
    assert not set(complements) & set(branches)
    assert all(nom in maquette.HORS_GRILLE + maquette.GAINS_ENSEMBLE
               for fac in complements.values() for nom, _ in fac)
    releve = {c.ident: c for c in maquette.releve()}
    assert "socle.grille.vitesses÷2" in releve and "socle.grille.toutes÷2" not in releve


def _retirer(brutes, variete, tol):
    """Valeurs propres brutes qui ne s'apparient à aucune valeur propre de la variété (appariement glouton)."""
    restantes = list(brutes)
    for z in variete:
        i = min(range(len(restantes)), key=lambda q: abs(restantes[q] - z))
        assert abs(restantes[i] - z) <= tol, z
        restantes.pop(i)
    return restantes


@pytest.mark.parametrize("pi", [0.0, 0.02])
def test_spectre_restreint_retire_les_racines_des_identites(maquette, pi):
    """Sur la variété des identités, les gradients ne portent plus de valeur propre : la restriction retire
    exactement une racine en 1/Γ̄ par identité et garde toutes les autres, racine nominale comprise."""
    J, J_var, Gs, inv = maquette.jacobiennes_socle(pi, "hausse")
    n_id = len(maquette.IDENTITES_SOCLE)
    assert J_var.shape == (len(J) - n_id, len(J) - n_id)
    # Chaque gradient est vecteur propre à gauche de valeur propre 1/Γ̄ : la variété est invariante.
    assert np.max(np.linalg.norm(Gs @ J - Gs * inv, axis=1) / np.linalg.norm(Gs, axis=1)) <= 1e-6
    tol = maquette.TOL_RACINE_MULTIPLE
    retirees = _retirer(np.linalg.eigvals(J), np.linalg.eigvals(J_var), tol)
    assert len(retirees) == n_id and all(abs(z - inv) <= tol for z in retirees)
    s = maquette.lectures_socle(pi, "hausse")
    assert s.multiplicite_brute - s.multiplicite_variete == n_id
    assert s.noyau_brut == s.multiplicite_brute  # racines en 1/Γ̄ semi-simples
    assert abs(s.suivante - inv) > tol and abs(s.suivante) <= s.rayon_variete
    assert s.rayon_variete <= s.rayon_brut + tol
    assert s.residu_identites <= 1e-12
