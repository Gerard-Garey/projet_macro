"""Tests du résolveur de l'état stationnaire, module feuille `nations.scenarios.stationnaire` (#175).

Contrat : ADR 0015 (accepté le 26/11/2026, P258), points 6 à 8, 11, 13 et 14 ;
plan de J3-e1, rang 3, commit 1 (extraction à ordre d'opérations conservé).
L'identité au bit avec le script d'origine est établie hors de cette batterie
par la sortie standard du script (sha256 de référence, ADR 0015, S8) et par les
empreintes des bancs (P250) ; ici, les propriétés de forme du module : feuille,
pur, sans argument optionnel ni drapeau, entrées sans défaut ni vitesse, liste
fermée des conditions d'existence, refus typé au pôle exact.
"""

import ast
import dataclasses
import re
import subprocess
import sys
from dataclasses import fields, replace
from pathlib import Path

import pytest

from nations.scenarios import stationnaire as resolveur

RACINE = Path(__file__).resolve().parents[2]
MODULE = RACINE / "src" / "nations" / "scenarios" / "stationnaire.py"
SPECIFICATION = RACINE / "docs" / "specification" / "nations_et_marches.tex"
POINTS_PI = (0.0, 0.02, 0.10)

# Liste fermée des conditions d'existence, dans l'ordre du script (ADR 0015, point 8.1).
CONDITIONS_ATTENDUES = ("D1", "D2", "existence_dividende_banque", "Div_F", "theta_G", "marge_plafond_E1",
                        "B", "B_Bk", "B_CB", "B_H")


def entrees(stationnaire, **variations):
    """Entrées du résolveur aux paramètres de référence du script, ν_G = 1,15 (valeur retenue)."""
    par = replace(stationnaire.Parametres(), nu_G=stationnaire.NU_G_RETENU, **variations)
    return stationnaire.entrees_stationnaires(par)


def etat_initial(e):
    """État résolu sous les conventions de l'état initial : r̂* = r̄, ϱ̄_L = ϱ_L (ADR 0015, point 10)."""
    return resolveur.etat_stationnaire(e, e.r_bar, resolveur.taux(e, e.r_bar).rho_L)


def imports(chemin):
    """Modules importés par un fichier : (noms complets, niveau relatif maximal)."""
    noms, niveau = set(), 0
    for noeud in ast.walk(ast.parse(chemin.read_text(encoding="utf-8"))):
        if isinstance(noeud, ast.Import):
            noms.update(a.name for a in noeud.names)
        elif isinstance(noeud, ast.ImportFrom):
            niveau = max(niveau, noeud.level)
            noms.add(noeud.module or "")
            noms.update(f"{noeud.module}.{a.name}" for a in noeud.names if noeud.module)
    return noms, niveau


# --- Module feuille (point 6.1) ----------------------------------------------------


def test_le_module_feuille_n_importe_que_la_bibliotheque_standard():
    noms, niveau = imports(MODULE)
    assert niveau == 0
    assert {n.split(".")[0] for n in noms} <= {"__future__", "math", "dataclasses", "typing"}


def test_importer_le_resolveur_ne_charge_de_nations_que_trois_modules():
    code = ("import sys\nimport nations.scenarios.stationnaire\n"
            "print(sorted(m for m in sys.modules if m == 'nations' or m.startswith('nations.')))\n")
    sortie = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout
    assert sortie.strip() == "['nations', 'nations.scenarios', 'nations.scenarios.stationnaire']"


def test_aucune_couche_du_moteur_n_importe_scenarios():
    """noyau, etat, moteur, blocs et observation n'importent pas `scenarios/` (ADR 0015, point 9.7)."""
    ecarts = []
    for couche in ("noyau", "etat", "moteur", "blocs", "observation"):
        for chemin in sorted((RACINE / "src" / "nations" / couche).rglob("*.py")):
            noms, _ = imports(chemin)
            ecarts += [f"{chemin.name} importe {n}" for n in noms if n.startswith("nations.scenarios")]
    assert ecarts == []


# --- Fonctions pures, sans argument optionnel ni drapeau (point 6.3) ------------------


def test_aucun_argument_optionnel_ni_booleen_ni_none():
    arbre = ast.parse(MODULE.read_text(encoding="utf-8"))
    ecarts = []
    for noeud in ast.walk(arbre):
        if isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            a = noeud.args
            if a.defaults or any(d is not None for d in a.kw_defaults) or a.vararg or a.kwarg:
                ecarts.append(f"{getattr(noeud, 'name', 'lambda')} : argument optionnel")
            for arg in a.posonlyargs + a.args + a.kwonlyargs:
                texte = ast.unparse(arg.annotation) if arg.annotation is not None else ""
                if "bool" in texte or "None" in texte:
                    ecarts.append(f"{noeud.name}({arg.arg}: {texte})")
    assert ecarts == []


def test_deux_resolutions_identiques_et_valeurs_immuables(stationnaire):
    e = entrees(stationnaire)
    etat = etat_initial(e)
    assert etat == etat_initial(e)
    o = resolveur.ouverture(etat, e)
    assert o == resolveur.ouverture(etat, e)
    with pytest.raises(dataclasses.FrozenInstanceError):
        e.pi_etoile = 0.0
    for valeur, champ in ((etat, "theta_G"), (o, "M_G"), (resolveur.taux(e, e.r_bar), "i_CB")):
        with pytest.raises(AttributeError):
            setattr(valeur, champ, 0.0)
    assert isinstance(o.registre, tuple)


# --- Entrées (point 7) ----------------------------------------------------------------


def test_entrees_sans_defaut_sous_les_noms_des_tables():
    for champ in fields(resolveur.EntreesStationnaires):
        assert champ.default is dataclasses.MISSING and champ.default_factory is dataclasses.MISSING, champ.name
    assert len(fields(resolveur.EntreesStationnaires)) == 28


def test_entrees_sans_vitesse_ni_entree_de_scenario(stationnaire):
    """28 des 42 champs de `Parametres` sont lus ; les 14 autres sont les douze vitesses et gains et ς_L, ς_B."""
    correspondance = stationnaire.CORRESPONDANCE_DES_ENTREES
    assert list(correspondance) == [c.name for c in fields(resolveur.EntreesStationnaires)]
    lus = set(correspondance.values())
    assert len(lus) == len(correspondance)
    non_lus = {c.name for c in fields(stationnaire.Parametres)} - lus
    assert non_lus == set(stationnaire.VITESSES) | {"varsigma_L", "varsigma_B"}
    assert len(non_lus) == 14


@pytest.mark.parametrize("n_a", [0, -12, 12.0, True])
def test_entrees_refusent_un_n_a_qui_n_est_pas_un_entier_positif(stationnaire, n_a):
    with pytest.raises(ValueError, match="pas_par_an"):
        replace(entrees(stationnaire), pas_par_an=n_a)


# --- Norme de l'état initial et résultats (points 6.3 et 6.4) ----------------------------


@pytest.mark.parametrize("pi", POINTS_PI)
def test_la_norme_de_l_etat_initial_donne_un_ecart_de_taux_nul_exactement(stationnaire, pi):
    """ϱ̄_L = ϱ_L par `taux`, rappelée par la résolution sur les mêmes opérandes : Δϱ = 0,0 au bit."""
    e = entrees(stationnaire, pi_cible=pi)
    etat = etat_initial(e)
    assert etat.d_rho == 0.0
    assert etat.tu == e.tu_bar
    assert etat.rho_bar_L == etat.rho_L == resolveur.taux(e, e.r_bar).rho_L


@pytest.mark.parametrize("n_a", [4, 12, 52])
def test_registre_de_n_a_plus_un_niveaux(stationnaire, n_a):
    e = entrees(stationnaire, n_a=n_a)
    o = resolveur.ouverture(etat_initial(e), e)
    assert len(o.registre) == n_a + 1
    assert len(resolveur.EtatStationnaire._fields) == 89
    assert len(resolveur.Ouverture._fields) == 35
    for type_ in (resolveur.Facteurs, resolveur.Taux, resolveur.EtatStationnaire, resolveur.Ouverture):
        assert type_._field_defaults == {}, type_.__name__


# --- Conditions d'existence et refus typé (point 8) ---------------------------------------


def test_liste_fermee_des_conditions_et_sections_de_la_specification():
    assert tuple(c[0] for c in resolveur.CONDITIONS_D_EXISTENCE) == CONDITIONS_ATTENDUES
    labels = set(re.findall(r"\\label\{(sec:[^}]+)\}", SPECIFICATION.read_text(encoding="utf-8")))
    assert {c[2] for c in resolveur.CONDITIONS_D_EXISTENCE} <= labels


@pytest.mark.parametrize("pi", POINTS_PI)
def test_aucune_condition_violee_a_l_etat_de_reference(stationnaire, pi):
    assert resolveur.relever_conditions(etat_initial(entrees(stationnaire, pi_cible=pi))) == ()


def test_releve_dans_l_ordre_de_la_liste_sans_ecart(stationnaire):
    etat = etat_initial(entrees(stationnaire))
    toutes = etat._replace(D1=-1.0, D2=0.0, existence_Bk_montant=-1.0, Div_F=-5e-324, theta_G=0.0,
                     marge_E1_montant=0.0, B=-1.0, B_Bk=-1.0, B_CB=-1.0, B_H=1.0)
    releve = resolveur.relever_conditions(toutes)
    assert tuple(c.identifiant for c in releve) == CONDITIONS_ATTENDUES
    assert releve[3].valeur == -5e-324
    assert all(c.section == dict((i, s) for i, _, s in resolveur.CONDITIONS_D_EXISTENCE)[c.identifiant]
               for c in releve)
    deux = resolveur.relever_conditions(etat._replace(B=-1.0, Div_F=-1.0))
    assert tuple(c.identifiant for c in deux) == ("Div_F", "B")
    # Bornes larges et strictes : Div_F = 0 et existence = 0 admis ; θ_G = 0 et marge = 0 refusés.
    bornes = resolveur.relever_conditions(etat._replace(Div_F=0.0, existence_Bk_montant=0.0))
    assert bornes == ()


def entrees_au_pole(nu_H, nu_G):
    """Entrées où D1 = 1 − ν_H/2 et D2 = 1 − ν_G/2 au bit (n_a = 1, π* = g = 0, i_CB = r̄ = 0,5, τ_H = 0)."""
    return resolveur.EntreesStationnaires(
        pas_par_an=1, g_pr=0.0, sigma=1.0, kappa=1.0, g_N=0.0, U_eq=0.05, mu_bar=0.6, nu_H=nu_H, delta=0.05,
        tu_bar=0.8, lv_etoile=0.4, nu_F=0.1, zeta=0.0, eta_r=0.0, varpi_L=0.0, varpi_D=0.0, vartheta=0.1,
        pi_etoile=0.0, r_bar=0.5, theta_CB=0.0, tau_H=0.0, tau_F=0.0, theta_Tr=0.0, phi=1.0, nu_G=nu_G,
        p_0=1.0, pr_0=1.0, N_pa_0=1.0)


@pytest.mark.parametrize("nu_H, nu_G, attendu", [
    (2.0, 1.5, ("D1",)),
    (1.0, 2.0, ("D2",)),
    (3.0, 2.0, ("D1", "D2")),
])
def test_un_pole_exact_est_refuse_sous_le_type_du_resolveur(nu_H, nu_G, attendu):
    """D1 = 0 ou D2 = 0 : `EtatStationnaireInexistant`, jamais `ZeroDivisionError` (point 8.3) ; au pôle de D2,
    une violation antérieure de D1 est relevée avant lui."""
    e = entrees_au_pole(nu_H, nu_G)
    with pytest.raises(resolveur.EtatStationnaireInexistant) as refus:
        etat_initial(e)
    assert tuple(c.identifiant for c in refus.value.conditions) == attendu
    assert refus.value.conditions[-1].valeur == 0.0
    assert not isinstance(refus.value, ZeroDivisionError)


def test_hors_du_pole_les_memes_entrees_se_resolvent():
    """Témoin : à ν_H = 1 et ν_G = 1,5, D1 = 0,5 et D2 = 0,25 ; l'état est rendu (aucune condition jugée par le calcul)."""
    etat = etat_initial(entrees_au_pole(1.0, 1.5))
    assert etat.D1 == 0.5 and etat.D2 == 0.25


def test_le_script_refuse_le_pole_en_hors_domaine_meme_sans_controle(stationnaire):
    """L'adaptateur du script garde son refus (`HorsDomaine`, message de D2), contrôle activé ou non."""
    par = replace(stationnaire.Parametres(), n_a=1, g_pr=0.0, pi_cible=0.0, rbar=0.5, varpi_L=0.0, varpi_D=0.0,
                  tau_H=0.0, nu_H=1.0, nu_G=2.0)
    for controler in (True, False):
        with pytest.raises(stationnaire.HorsDomaine, match=r"^D2 = 0\.0 : "):
            stationnaire.etat_stationnaire(par, controler=controler)


def test_le_script_a_un_message_par_condition_de_la_liste(stationnaire):
    """Chaque condition de la liste fermée a son message `HorsDomaine` dans le script, et seulement elles."""
    assert tuple(stationnaire.MESSAGES_DES_CONDITIONS) == CONDITIONS_ATTENDUES
