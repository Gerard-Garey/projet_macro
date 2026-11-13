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
import re
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
    # Seul module du dépôt chargé par son chemin : le script d'état stationnaire. Aucun autre chargement
    # dynamique (indépendance de la contre-épreuve #66, symétrique de son propre test).
    assert '"etat_stationnaire"' in SCRIPT.read_text(encoding="utf-8")
    appels = [n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", None)
              for n in ast.walk(arbre) if isinstance(n, ast.Call)]
    assert appels.count("spec_from_file_location") == 1 and appels.count("module_from_spec") == 1
    natifs = {n.func.id for n in ast.walk(arbre) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert "import_module" not in appels and not {"__import__", "exec", "eval", "compile"} & natifs


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


def test_chaque_chiffre_releve_a_sa_ligne(maquette):
    """Chaque chiffre est écrit, hors valeur barrée, dans chacun des paragraphes et fiches qu'il déclare."""
    lignes, fiches = maquette.lire_spec(), maquette.lire_fiches()
    paragraphes = {label for label, _ in maquette.PARAGRAPHES} | {f for f, _ in maquette.LIGNES_FICHES}
    absents = []
    for c in maquette.releve():
        assert c.ou and set(c.ou) <= paragraphes, c.ident
        trouves = {label for label, _ in maquette.lignes_du_motif(lignes, c.motif, c.ou)}
        trouves |= {f for f in c.ou if maquette.lignes_du_motif_fiches(fiches, c.motif, (f,))}
        absents += [(c.ident, label) for label in c.ou if label not in trouves]
    assert absents == []
    idents = [c.ident for c in maquette.releve()]
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


# Chiffres du relevé en écart, liste exacte (#65) : la valeur de la fiche 5 à n_a = 4 (cause non établie) et les
# 8 rayons de la table φ de la fiche 9, mesurés avant l'amendement de E12 (historique de la spécification,
# ligne 30). Aucun chiffre en vigueur de la spécification n'y figure : un chiffre en vigueur qui passe en écart,
# ou en « sans objet », fait échouer la batterie ; un écart qui se résorbe aussi, la liste est alors à revoir.
ECARTS_ATTENDUS = frozenset({"instabilite17.a.n_a4.hausse"} | {
    f"finances.rayon.phi{phi:g}.pi{pi:g}" for phi in (0.1, 0.25, 0.5, 1) for pi in (0.02, 0.1)})


def test_ensemble_des_ecarts_fige(maquette):
    r = maquette.calculer()
    assert {x["ident"] for x in r["releve"] if not x["reproduit"]} == ECARTS_ATTENDUS
    assert {x["ident"] for x in r["releve"] if x["verdict"] == "écart"} == ECARTS_ATTENDUS


def test_ecart_a_1_de_la_racine_reelle_proportionnel_a_a_I(maquette):
    """Branche ×2 sans a_I, régime de hausse : la lecture (c) est une racine réelle sous 1 dont l'écart à 1 est
    à peu près proportionnel à a_I (a_I ÷ 1000 et ÷ 100) ; en régime de baisse, la lecture (c) est une paire."""
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


def _retirer(brutes, variete, tol):
    """Valeurs propres brutes qui ne s'apparient à aucune valeur propre de la variété (appariement glouton)."""
    restantes = list(brutes)
    for z in variete:
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


def test_marge_conjointe_est_une_frontiere(maquette):
    m = maquette.marge_conjointe()
    f = m["facteur"]
    base, ens = maquette.parametres_socle(0.02), maquette._ensemble(1.5)
    modifies = {c.name for c in dataclasses.fields(base) if getattr(base, c.name) != getattr(ens, c.name)}
    assert modifies == set(maquette.GAINS_ENSEMBLE) == {"beta", "a_pi", "eta_r"}
    assert all(getattr(ens, nom) == 1.5 * getattr(base, nom) for nom in modifies)
    assert maquette.BORNES_MARGE[0] < f < maquette.BORNES_MARGE[1]
    assert maquette.rayon_c(maquette._ensemble(f - 1e-6)) < 1 < maquette.rayon_c(maquette._ensemble(f + 1e-6))
    assert max(x["rayon"] for x in m["x2"].values()) == maquette.rayon_c(maquette._ensemble(2.0))


def test_frontiere_de_la_marge_en_regime_de_hausse(maquette):
    """La frontière du régime de hausse sépare la lecture (c) de ce régime de part et d'autre de 1, et n'est pas
    en deçà de la frontière du pire des deux régimes ; à a_I ×0,001, la lecture (c) en hausse est une racine
    réelle, sous laquelle se trouve la paire complexe relevée à côté."""
    f_h = maquette.frontiere_marge("hausse")
    assert maquette.BORNES_MARGE[0] < f_h < maquette.BORNES_MARGE[1]
    rayon = lambda f: maquette.lectures(maquette._ensemble(f), "hausse").rayon_c  # noqa: E731
    assert rayon(f_h - 1e-6) < 1 < rayon(f_h + 1e-6)
    assert f_h >= maquette.marge_conjointe()["facteur"]
    par = maquette._ensemble_sans_aI()
    assert par == maquette.parametres_socle(0.02, facteurs={"beta": 2.0, "a_pi": 2.0, "eta_r": 2.0, "a_I": 1e-3})
    z = maquette.lectures(par, "hausse").suivante
    assert maquette.nature_racine(z)[0] == "réelle positive"
    J_var = maquette.jacobiennes_carte(maquette.carte_socle(par, "hausse"), par)[1]
    assert maquette.module_paire(np.linalg.eigvals(J_var)) < abs(z)


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
