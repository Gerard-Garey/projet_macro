"""Tests de l'adaptateur du moteur `nations.scenarios.initial.etat_initial` (#175, commit 2).

Contrat : ADR 0015 (accepté le 26/11/2026, P258), points 9 et 10, décisions S3,
S4 et S7 ; plan de J3-e1, rang 3. Condition de `macro` sur S7, écrite avant
l'essai : une échelle extrême qui rend une grandeur non finie est refusée par un
refus typé et nommé, jamais propagée (ni `inf` ni `NaN` dans l'`EtatPays`).
L'identité au bit avec l'état que construisait `socle_partiel` à `5c19961` est
établie hors de cette batterie (instantané avant / après) et par les empreintes
des bancs (P250) ; ici, l'égalité au bit avec l'ouverture du script et les
propriétés de l'adaptateur.
"""

import ast
import dataclasses
import inspect
import math
import sys
from dataclasses import fields, replace
from pathlib import Path

import pytest

from nations.etat import schema
from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres import varier
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE as REFERENCE
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.scenarios import initial
from nations.scenarios import stationnaire as resolveur

RACINE = Path(__file__).resolve().parents[2]
MODULE = RACINE / "src" / "nations" / "scenarios" / "initial.py"
POINTS_PI = (0.0, 0.02, 0.10)
GRAINE = 20261113


def tables(**variations):
    """Tables de référence, variées par `variations` : {radical: {champ: valeur}}."""
    return replace(REFERENCE, **{radical: varier(getattr(REFERENCE, radical), **valeurs)
                                 for radical, valeurs in variations.items()})


def tables_a(pi):
    return tables(banque_centrale={"pi_etoile": pi})


def resoudre(parametres, normalisation=initial.NORMALISATION_DE_REFERENCE):
    return initial.etat_initial(parametres, normalisation, identifiant="A", graine=GRAINE)


def flottants(etat):
    """Tous les flottants d'un `EtatPays` (variables et niveaux du registre)."""
    valeurs = [getattr(etat, v.nom) for v in schema.VARIABLES if v.type is float]
    return valeurs + list(etat.registre_prix)


# --- Table fermée et correspondance des noms (point 9.5) -------------------------------


def test_correspondance_des_variables_en_bijection_avec_le_schema():
    assert set(initial.OUVERTURE_DES_VARIABLES) == {v.nom for v in schema.VARIABLES_DES_BLOCS}
    champs = initial.OUVERTURE_DES_VARIABLES.values()
    assert len(set(champs)) == len(initial.OUVERTURE_DES_VARIABLES)
    assert set(champs) <= set(resolveur.Ouverture._fields)
    assert set(cat.NOMS_POSTES) <= set(resolveur.Ouverture._fields)


def test_entrees_lues_sur_les_tables_sous_leurs_noms():
    """Chaque entrée du résolveur, hors normalisations, est un champ de table de même nom ; θ_G n'en
    est pas une (S4)."""
    noms = [c.name for c in fields(resolveur.EntreesStationnaires)]
    assert list(initial.ENTREES_DES_TABLES) + ["p_0", "pr_0", "N_pa_0"] == noms
    for entree, (radical, champ) in initial.ENTREES_DES_TABLES.items():
        assert entree == champ
        assert champ in {f.name for f in fields(getattr(REFERENCE, radical))}, entree
    assert ("finances_publiques", "theta_G") not in initial.ENTREES_DES_TABLES.values()


def _autre_valeur(champ, valeur):
    """Valeur voisine dans le domaine : φ ∈ {0 ; 1} basculé, sinon un écart relatif de 1e−6."""
    if champ == "phi":
        return 1.0 - valeur
    return valeur * (1 + 1e-6) if valeur != 0.0 else 1e-6


def test_entrees_des_tables_lit_exactement_la_correspondance_declaree():
    """`entrees_des_tables` (accès nommés) lit chaque entrée sur le champ que déclare
    `ENTREES_DES_TABLES`, et sur lui seul : un champ varié ne change que son entrée."""
    n = initial.NORMALISATION_DE_REFERENCE
    temoin = initial.entrees_des_tables(REFERENCE, n)
    assert temoin.pas_par_an == REFERENCE.cadre.pas_par_an
    for entree, (radical, champ) in initial.ENTREES_DES_TABLES.items():
        if radical == "cadre":
            continue
        brute = getattr(getattr(REFERENCE, radical), champ)
        valeur = _autre_valeur(champ, getattr(brute, "valeur", brute))
        lues = initial.entrees_des_tables(tables(**{radical: {champ: valeur}}), n)
        ecarts = {c.name for c in fields(lues) if getattr(lues, c.name) != getattr(temoin, c.name)}
        assert ecarts == {entree} and getattr(lues, entree) == valeur, entree
    autre = initial.Normalisation(2.0, 3.0, 5.0)
    lues = initial.entrees_des_tables(REFERENCE, autre)
    assert (lues.p_0, lues.pr_0, lues.N_pa_0) == (2.0, 3.0, 5.0)
    assert replace(lues, p_0=1.0, pr_0=1.0, N_pa_0=1.0) == temoin


def test_signature_sans_argument_optionnel():
    signature = inspect.signature(initial.etat_initial)
    assert list(signature.parameters) == ["parametres", "normalisation", "identifiant", "graine"]
    for nom, parametre in signature.parameters.items():
        assert parametre.default is inspect.Parameter.empty, nom
    assert signature.parameters["identifiant"].kind is inspect.Parameter.KEYWORD_ONLY
    assert signature.parameters["graine"].kind is inspect.Parameter.KEYWORD_ONLY


# --- Égalité au bit avec l'ouverture du script --------------------------------------------


@pytest.mark.parametrize("pi", POINTS_PI)
def test_etat_egal_au_bit_a_l_ouverture_du_script(stationnaire, pi):
    """Aux trois π*, positions, variables, registre et θ_G égaux au bit à l'ouverture du script à
    ses paramètres (ν_G = 1,15) ; V^flux = V^stock (`identites.valeur_nette_stock`)."""
    par = replace(stationnaire.Parametres(), pi_cible=pi, nu_G=stationnaire.NU_G_RETENU)
    o = stationnaire.ouverture(stationnaire.etat_stationnaire(par), par)
    rendu = resoudre(tables_a(pi))
    etat = rendu.etat
    for nom in cat.NOMS_POSTES:
        assert getattr(etat, nom).hex() == float(o[nom]).hex(), nom
    for variable, champ in initial.OUVERTURE_DES_VARIABLES.items():
        assert getattr(etat, variable).hex() == float(o[champ]).hex(), variable
    assert [x.hex() for x in etat.registre_prix] == [float(x).hex() for x in o["registre"]]
    assert len(etat.registre_prix) == schema.NIVEAUX_DU_REGISTRE
    positions = {nom: getattr(etat, nom) for nom in cat.NOMS_POSTES}
    for secteur in cat.SECTEURS:
        assert getattr(etat, cat.VALEUR_NETTE_FLUX[secteur]) == idt.valeur_nette_stock(positions,
                                                                                       secteur)
    assert (etat.identifiant, etat.graine, etat.t) == ("A", GRAINE, 0)
    assert rendu.parametres.finances_publiques.theta_G.hex() == float(o["theta_G"]).hex()


def test_litteral_theta_G_de_la_table_egal_au_bit_au_resolu():
    """S3 : le littéral θ_G de la table de référence (π* = 2 %) vaut au bit le θ_G résolu."""
    assert REFERENCE.banque_centrale.pi_etoile.valeur == 0.02
    rendu = resoudre(REFERENCE)
    assert rendu.parametres.finances_publiques.theta_G.hex() == \
        REFERENCE.finances_publiques.theta_G.hex()
    assert rendu.parametres == REFERENCE


# --- Tables alignées et conventions de sélection (points 9.2 à 9.4, 10) ------------------


@pytest.mark.parametrize("pi", POINTS_PI)
def test_seul_theta_G_est_aligne(pi):
    recues = tables_a(pi)
    alignees = resoudre(recues).parametres
    for champ in fields(recues):
        if champ.name != "finances_publiques":
            assert getattr(alignees, champ.name) is getattr(recues, champ.name), champ.name
    assert alignees.finances_publiques == replace(
        recues.finances_publiques, theta_G=alignees.finances_publiques.theta_G)


@pytest.mark.parametrize("theta_G", [0.05, 0.3, 0.9])
def test_theta_G_recu_n_est_pas_lu(theta_G):
    """S4 : θ_G de l'ensemble reçu varié, état et tables alignées identiques au bit."""
    temoin = resoudre(tables_a(0.10))
    varie = resoudre(tables(banque_centrale={"pi_etoile": 0.10},
                            finances_publiques={"theta_G": theta_G}))
    assert varie.etat == temoin.etat
    assert [x.hex() for x in flottants(varie.etat)] == [x.hex() for x in flottants(temoin.etat)]
    assert varie.parametres == temoin.parametres


@pytest.mark.parametrize("pi", POINTS_PI)
def test_pi_etoile_lu_sur_la_table_et_conventions_de_l_etat_initial(pi):
    """π^e_0 = π*_0 = π* de la table ; r̂*_0 = r̄ ; ϱ̄_L = ϱ_{L,0} (point 10)."""
    recues = tables_a(pi)
    etat = resoudre(recues).etat
    assert etat.pi_e == etat.pi_etoile == recues.banque_centrale.pi_etoile.valeur == pi
    assert etat.r_hat_etoile == recues.banque_centrale.r_bar.valeur
    assert etat.varrho_bar_L == (1 + etat.i_L) / (1 + pi) - 1


def test_identite_traversee_sans_effet_sur_les_valeurs():
    a = resoudre(REFERENCE).etat
    b = initial.etat_initial(REFERENCE, initial.NORMALISATION_DE_REFERENCE, identifiant="B",
                             graine=7).etat
    assert (b.identifiant, b.graine) == ("B", 7)
    assert replace(b, identifiant="A", graine=GRAINE) == a


# --- Refus typés (point 8.2) -------------------------------------------------------------


@pytest.mark.parametrize("variations, attendu", [
    ({"finances_publiques": {"theta_Tr": 0.5}}, ("theta_G",)),
    ({"finances_publiques": {"tau_H": 0.9}}, ("B", "B_Bk")),
    ({"banque": {"varpi_L": 0.0, "varpi_D": 0.0}}, ("existence_dividende_banque",)),
])
def test_condition_d_existence_violee_refusee(variations, attendu):
    with pytest.raises(resolveur.EtatStationnaireInexistant) as refus:
        resoudre(tables(**variations))
    assert tuple(c.identifiant for c in refus.value.conditions) == attendu


def test_l_etat_sans_credit_est_rendu():
    """lv* = 0 est dans le domaine : la marge d'existence rapportée à L est sans objet (NaN dans le
    résolveur), l'état est rendu fini."""
    etat = resoudre(tables(investissement={"lv_etoile": 0.0})).etat
    assert etat.L == 0.0
    assert all(math.isfinite(x) for x in flottants(etat))


# --- Normalisation et échelles extrêmes (S7) ----------------------------------------------


@pytest.mark.parametrize("valeur", [0.0, -1.0, math.inf, math.nan, 1, True, "1"])
def test_normalisation_hors_domaine_refusee(valeur):
    for position in range(3):
        arguments = [1.0, 1.0, 1.0]
        arguments[position] = valeur
        with pytest.raises(initial.NormalisationHorsDomaine):
            initial.Normalisation(*arguments)


def test_normalisation_de_reference():
    assert initial.NORMALISATION_DE_REFERENCE == initial.Normalisation(1.0, 1.0, 1.0)
    with pytest.raises(dataclasses.FrozenInstanceError):
        initial.NORMALISATION_DE_REFERENCE.p_0 = 2.0


@pytest.mark.parametrize("normalisation", [
    (1e300, 1.0, 1.0), (1e-300, 1.0, 1.0), (1.0, 1e300, 1.0), (1.0, 1e-300, 1.0),
    (1.0, 1.0, 1e300), (1.0, 1.0, 1e-300),
])
def test_echelle_extreme_representable_rendue_finie_et_homogene(normalisation):
    """Aux bornes p_0 = 1e300 et 1e−300 (et de même pour pr_0, N^pa_0), l'état est fini et
    homogène de degré un : K/(p_0 pr_0 N^pa_0) égal à celui de référence à 1e−12 près."""
    rendu = resoudre(REFERENCE, initial.Normalisation(*normalisation))
    assert all(math.isfinite(x) for x in flottants(rendu.etat))
    reference = resoudre(REFERENCE).etat
    produit = normalisation[0] * normalisation[1] * normalisation[2]
    assert rendu.etat.K / produit == pytest.approx(reference.K, rel=1e-12, abs=0.0)
    assert rendu.parametres.finances_publiques.theta_G == pytest.approx(
        REFERENCE.finances_publiques.theta_G, rel=1e-12, abs=0.0)


@pytest.mark.parametrize("normalisation, grandeur", [
    ((1e307, 1.0, 1.0), "V_F"),  # dépassement : grandeur infinie
    ((1.7e308, 1.0, 1.0), "K"),
    ((1.0, 1.0, 1.7e308), "IN_vol"),
    ((1e200, 1e200, 1.0), "W"),
    ((1e-200, 1e-200, 1.0), "ZeroDivisionError"),  # sous-dépassement : division par zéro
])
def test_echelle_qui_rend_une_grandeur_non_finie_refusee_sous_un_type_nomme(normalisation,
                                                                            grandeur):
    """Condition de `macro` sur S7 : refus `EchelleNonRepresentable`, nommant la grandeur, jamais un
    état portant `inf` ou `NaN`, ni une condition d'existence relevée en `inf` ou `NaN`."""
    n = initial.Normalisation(*normalisation)
    with pytest.raises(initial.EchelleNonRepresentable) as refus:
        resoudre(REFERENCE, n)
    assert refus.value.normalisation == n
    assert refus.value.grandeur == grandeur
    assert not isinstance(refus.value, resolveur.EtatStationnaireInexistant)


@pytest.mark.parametrize("position, grandeur", [(0, "p"), (1, "pr"), (2, "N_pa")])
@pytest.mark.parametrize("valeur", [1e-310, 1e-320, 5e-324])
def test_echelle_qui_rend_une_grandeur_denormale_refusee_sous_un_type_nomme(position, grandeur,
                                                                            valeur):
    """Précision de `macro` sur S7 (écrite avant l'essai) : toute grandeur de l'état est 0,0 ou un
    flottant normal ; une normalisation dénormale (p_0, pr_0 ou N^pa_0) est refusée par
    `EchelleNonRepresentable` avant le relevé des conditions d'existence (5e−324 ne sort plus en
    `EtatStationnaireInexistant`)."""
    arguments = [1.0, 1.0, 1.0]
    arguments[position] = valeur
    n = initial.Normalisation(*arguments)
    with pytest.raises(initial.EchelleNonRepresentable) as refus:
        resoudre(REFERENCE, n)
    assert (refus.value.grandeur, refus.value.valeur) == (grandeur, valeur)
    assert not isinstance(refus.value, resolveur.EtatStationnaireInexistant)


def test_grandeur_denormale_venue_d_un_parametre_de_table_refusee():
    """La cause peut être un paramètre de table (audit, C1) : t̄u = 5e−324 rend tu dénormal."""
    with pytest.raises(initial.EchelleNonRepresentable, match="aux tables reçues") as refus:
        resoudre(tables(investissement={"tu_bar": 5e-324}))
    assert (refus.value.grandeur, refus.value.valeur) == ("tu", 5e-324)


@pytest.mark.parametrize("position", range(3))
@pytest.mark.parametrize("valeur", [1e300, 1e-300])
def test_aux_bornes_toute_grandeur_est_nulle_ou_normale(position, valeur):
    """À 1e±300 sur chaque normalisation, chaque flottant de l'`EtatPays` et θ_G est 0,0 ou normal."""
    arguments = [1.0, 1.0, 1.0]
    arguments[position] = valeur
    rendu = resoudre(REFERENCE, initial.Normalisation(*arguments))
    for x in flottants(rendu.etat) + [rendu.parametres.finances_publiques.theta_G]:
        assert x == 0.0 or (math.isfinite(x) and abs(x) >= sys.float_info.min), x


# --- Imports (point 9.7) ----------------------------------------------------------------------


def test_imports_de_l_adaptateur():
    """`nations.etat`, `nations.moteur.parametres`, `nations.noyau` et le module feuille seuls."""
    importes = set()
    for noeud in ast.walk(ast.parse(MODULE.read_text(encoding="utf-8"))):
        if isinstance(noeud, ast.ImportFrom):
            assert noeud.level == 0
            importes.add(noeud.module)
        elif isinstance(noeud, ast.Import):
            importes.update(a.name for a in noeud.names)
    de_nations = {m for m in importes if m.split(".")[0] == "nations"}
    admis = ("nations.etat", "nations.moteur.parametres", "nations.noyau",
             "nations.scenarios")
    hors = {m for m in de_nations if not any(m == a or m.startswith(a + ".") for a in admis)}
    assert de_nations and hors == set()
    assert importes - de_nations <= {"__future__", "math", "sys", "types", "dataclasses"}


def test_domaine_des_tables_refuse_a_la_construction():
    """Une table hors domaine reste refusée à sa construction (point 8.4), avant l'adaptateur."""
    with pytest.raises(DefautDeDeclaration):
        varier(REFERENCE.finances_publiques, nu_G=1.0)
