"""Observation hors de l'état : protocole, relevé des résidus, suppression, imports (issue #96).

Contrat : ADR 0012, E1 et E2 ; critères de #96 et leur complément du rang 1b
(aucun contrôle ne lit `observation/`, la reprise couvre le relevé). L'
ordonnanceur (#97) n'existe pas encore : le pas d'essai ci-dessous en tient le
rôle, avec des flux tirés par un générateur à graine explicite (graine du
pays, t), si bien qu'un pas repris d'une sauvegarde tire les mêmes flux.
"""

import ast
import dataclasses
import struct
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from nations.etat.sauvegarde import charger, sauvegarder
from nations.etat.schema import EtatPays
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.grand_livre import ClotureDePhase, FluxPropose, ouvrir_pas
from nations.observation.observateur import FinDePas, Observateur, ObservateurNul
from nations.observation.residus import IDENTITE_CUMULEE, ReleveDesResidus

RACINE = Path(__file__).resolve().parents[2]
NATIONS = RACINE / "src" / "nations"
EPS = 1e-12

OUVERTURE = {"D_H": 600.0, "D_F": 400.0, "L": 500.0, "B_H": 200.0, "B_Bk": 300.0,
             "B_CB": 100.0, "Res": 50.0, "L_CB": 20.0, "M_G": 150.0, "K": 900.0, "IN": 100.0}


@dataclasses.dataclass(frozen=True)
class CadreDouble:
    """Double des paramètres du cadre (#97) : les deux tolérances, sans dimension."""

    tolerance_identite_pas: float = EPS
    tolerance_identite_cumulee: float = EPS


CADRE = CadreDouble()


def etat_initial(identifiant="A", graine=20261007, decalage=0.0):
    """État d'essai ; V^flux = V^stock + décalage × S de chaque secteur."""
    p = dict(OUVERTURE)
    v = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(p, s) for s in cat.SECTEURS}
    registre = tuple(1.02 ** (-u / 12) for u in range(1, 14))
    e = EtatPays(identifiant=identifiant, graine=graine, t=0, registre_prix=registre, **p, **v)
    gl = ouvrir_pas(e, CADRE)
    return dataclasses.replace(e, **{
        cat.VALEUR_NETTE_FLUX[s]: v[cat.VALEUR_NETTE_FLUX[s]] + decalage * gl.echelle(s)
        for s in cat.SECTEURS})


def plan_du_pas(etat):
    """Flux du pas, tirés à la graine (graine du pays, t) : signes admis par chaque ligne."""
    rng = np.random.default_rng([etat.graine, etat.t])
    plan = {}
    for ligne in cat.LIGNES:
        if ligne.proposant is None or ligne.identifiant == "21":
            continue
        bas = -4.0 if ligne.admet_negatif and ligne.identifiant != "7" else 0.0
        plan[ligne.identifiant] = FluxPropose(
            ligne.identifiant, {t.nom: float(rng.uniform(bas, 4.0)) for t in ligne.termes},
            ligne.proposant)
    return plan


def pas_d_essai(etat, observateur):
    """Un pas : onze clôtures relevées, puis l'état t + 1 assemblé et relevé.

    Tient le rôle de l'ordonnanceur (#97) ; le registre n'est pas avancé (#97).
    """
    gl = ouvrir_pas(etat, CADRE)
    plan = plan_du_pas(etat)
    for phase in cat.PHASES:
        for ligne in cat.LIGNES_DE_LA_PHASE[phase]:
            if ligne.identifiant in plan:
                gl.proposer(plan[ligne.identifiant])
        if phase == "8b":
            perte = plan["16"].montants["Pi_CB"]
            if perte < 0.0:
                gl.declarer_montant_couvert("16", min(-perte, max(0.0, gl.position("M_G"))),
                                            "finances_publiques")
        if phase == "8c":
            remboursement = -min(gl.position("Res"), gl.position("L_CB"))
            gl.proposer(FluxPropose("21", {"Delta_LCB": remboursement}, "banque"))
        observateur.relever(gl.clore_phase(phase))
    fin = gl.clore_pas()
    suivant = dataclasses.replace(etat, t=fin.t, **fin.variables)
    observateur.relever(FinDePas(etat.t, suivant))
    return suivant


def trajectoire(etat, n, observateur):
    for _ in range(n):
        etat = pas_d_essai(etat, observateur)
    return etat


def bits(releves):
    return [tuple(struct.pack("<d", x).hex() if type(x) is float else x for x in r)
            for r in releves]


# --------------------------------------------------------------------------
# Protocole
# --------------------------------------------------------------------------


def test_observateurs_satisfont_le_protocole():
    """E1 : une méthode, `relever`, qui ne rend rien ; aucun attribut créé à la volée."""
    observateurs: list[Observateur] = [ObservateurNul(), ReleveDesResidus()]
    for observateur in observateurs:
        assert observateur.relever(FinDePas(0, etat_initial())) is None
        assert not hasattr(observateur, "__dict__")


def test_evenements_immuables():
    """E1 : l'observateur reçoit des valeurs immuables (aucune rétroaction possible)."""
    releve = ReleveDesResidus()
    e = etat_initial()
    pas_d_essai(e, releve)
    fin = FinDePas(0, e)
    with pytest.raises(dataclasses.FrozenInstanceError):
        fin.t = 1
    with pytest.raises(dataclasses.FrozenInstanceError):
        fin.etat.K = 0.0
    cloture = ClotureDePhase(0, "3", (("r", "", 0.0),), ())
    with pytest.raises(dataclasses.FrozenInstanceError):
        cloture.rapports = ()


def test_evenement_inconnu_refuse():
    with pytest.raises(TypeError, match="inconnu"):
        ReleveDesResidus().relever({"t": 0})


# --------------------------------------------------------------------------
# Test de suppression : sauvegardes identiques à l'octet
# --------------------------------------------------------------------------


@pytest.mark.parametrize("graine", [1, 2, 20261007])
def test_suppression_de_l_observation_identique_a_l_octet(graine):
    """E1 : avec ObservateurNul ou avec le relevé, la trajectoire sauvegardée est la même à l'octet."""
    e = etat_initial(graine=graine)
    sans = trajectoire(e, 24, ObservateurNul())
    releve = ReleveDesResidus()
    avec = trajectoire(e, 24, releve)
    assert sauvegarder([avec]) == sauvegarder([sans])
    assert len(releve.pas()) == 24 and releve.releves()


# --------------------------------------------------------------------------
# Relevé des résidus (E2)
# --------------------------------------------------------------------------


def test_releve_par_cloture_et_accumulation_par_pas():
    """Un relevé par règle et par clôture ; un point d'accumulation par pas et par secteur."""
    releve = ReleveDesResidus()
    e = etat_initial(decalage=0.5 * EPS)
    trajectoire(e, 6, releve)
    par_cloture = {}
    for t, phase, regle, objet, rapport in releve.releves():
        par_cloture.setdefault((t, phase), []).append(regle)
        assert type(rapport) is float and 0.0 <= rapport <= EPS
    assert len(par_cloture) == 6 * len(cat.PHASES)
    for s in cat.SECTEURS:
        points = releve.accumulation(s)
        assert [t for t, _ in points] == list(range(6))
        # Le décalage injecté à t = 0 est relevé à chaque pas, sous ε_V.
        assert all(0.25 * EPS < r <= EPS for _, r in points)
    rapport, t, phase, objet = releve.maximum(IDENTITE_CUMULEE)
    assert 0.25 * EPS < rapport <= EPS and phase == "9" and objet in cat.SECTEURS
    assert releve.maximum("règle absente") == (0.0, None, None, None)


def test_maximum_ex_aequo_rend_le_premier_releve():
    """Deux rapports égaux au maximum : `maximum` rend le premier relevé, dans l'ordre des clôtures."""
    releve = ReleveDesResidus()
    releve.relever(ClotureDePhase(0, "3", (("r", "ligne 1", 0.25 * EPS),), ()))
    releve.relever(ClotureDePhase(0, "5", (("r", "ligne 2", 0.5 * EPS),), ()))
    releve.relever(ClotureDePhase(1, "3", (("r", "ligne 3", 0.5 * EPS),), ()))
    releve.relever(ClotureDePhase(1, "5", (("r", "ligne 4", 0.1 * EPS),), ()))
    assert releve.maximum("r") == (0.5 * EPS, 0, "5", "ligne 2")


def test_grandeurs_publiees_avec_definition_unite_denominateur_fenetre():
    """E2 : chaque grandeur porte sa définition, son unité, son dénominateur et sa fenêtre."""
    releve = ReleveDesResidus()
    assert all("aucun pas" in g.fenetre for g in releve.grandeurs())
    trajectoire(etat_initial(), 3, releve)
    for g in releve.grandeurs():
        assert g.nom and g.definition and g.denominateur
        assert g.unite == "sans dimension"
        assert "ouverture du pas" in g.denominateur
        assert g.fenetre == "pas 0 à 2 (3 pas clos relevés)"


def test_reprise_couvre_le_releve():
    """C96-3 : relevé avant la sauvegarde + relevé après la reprise = relevé sans interruption, bit à bit."""
    e = etat_initial(decalage=0.3 * EPS)
    continu = ReleveDesResidus()
    fin_continue = trajectoire(e, 12, continu)

    avant = ReleveDesResidus()
    milieu = trajectoire(e, 6, avant)
    repris, = charger(sauvegarder([milieu]))
    apres = ReleveDesResidus()
    fin_reprise = trajectoire(repris, 6, apres)

    assert bits(avant.releves() + apres.releves()) == bits(continu.releves())
    assert avant.pas() + apres.pas() == continu.pas()
    for s in cat.SECTEURS:
        assert bits(avant.accumulation(s) + apres.accumulation(s)) == bits(continu.accumulation(s))
    assert sauvegarder([fin_reprise]) == sauvegarder([fin_continue])


# --------------------------------------------------------------------------
# Graphe d'imports : observation/ n'est importée que par le moteur
# --------------------------------------------------------------------------


def imports_de_nations(chemin):
    """Modules `nations.…` importés par un fichier (instructions `import` et `from … import`)."""
    importes = []
    for noeud in ast.walk(ast.parse(chemin.read_text(encoding="utf-8"))):
        if isinstance(noeud, ast.Import):
            importes += [a.name for a in noeud.names if a.name.split(".")[0] == "nations"]
        elif isinstance(noeud, ast.ImportFrom) and noeud.module and noeud.level == 0:
            if noeud.module.split(".")[0] == "nations":
                importes += [noeud.module] + [f"{noeud.module}.{a.name}" for a in noeud.names]
        elif isinstance(noeud, ast.ImportFrom) and noeud.level:
            importes.append("." * noeud.level + (noeud.module or ""))
    return importes


def couche(module):
    """Couche d'un nom importé ou d'un fichier : second composant de `nations.<couche>`."""
    parties = module.split(".")
    return parties[1] if len(parties) > 1 else ""


# Couches de `nations` que chaque couche peut importer (ADR 0012, Conséquences),
# sans compter l'importation de soi-même.
IMPORTS_ADMIS = {
    "noyau": set(),
    "etat": {"noyau"},
    "observation": {"etat", "noyau"},
}


def modules_de_nations():
    for chemin in sorted(NATIONS.rglob("*.py")):
        relatif = chemin.relative_to(NATIONS.parent).with_suffix("")
        yield ".".join(relatif.parts), chemin


def test_graphe_d_imports_des_couches():
    """noyau n'importe rien de nations ; etat, noyau seul ; observation, etat et noyau seuls."""
    ecarts = []
    for module, chemin in modules_de_nations():
        source = couche(module)
        for importe in imports_de_nations(chemin):
            if importe.startswith("."):
                ecarts.append(f"{module} : importation relative {importe}")
                continue
            cible = couche(importe)
            if source in IMPORTS_ADMIS and cible not in IMPORTS_ADMIS[source] | {source, ""}:
                ecarts.append(f"{module} importe {importe}")
    assert ecarts == []


def test_observation_importee_par_le_moteur_seul_et_par_son_protocole():
    """E1 : hors d'elle-même, seule la couche moteur importe observation/, et seulement son protocole."""
    ecarts = []
    for module, chemin in modules_de_nations():
        if couche(module) == "observation":
            continue
        for importe in imports_de_nations(chemin):
            if couche(importe) != "observation":
                continue
            if couche(module) != "moteur" or not importe.startswith(
                    "nations.observation.observateur"):
                ecarts.append(f"{module} importe {importe}")
    assert ecarts == []


def test_le_controle_d_imports_sait_echouer(tmp_path):
    fichier = tmp_path / "f.py"
    fichier.write_text("from nations.observation.residus import ReleveDesResidus\n"
                       "import nations.observation\nfrom . import x\n", encoding="utf-8")
    assert imports_de_nations(fichier) == [
        "nations.observation.residus", "nations.observation.residus.ReleveDesResidus",
        "nations.observation", "."]


def test_calcul_charge_sans_observation():
    """Importer le noyau, l'état et la sauvegarde ne charge aucun module d'observation."""
    code = ("import sys, nations.noyau.grand_livre, nations.noyau.identites, "
            "nations.etat.schema, nations.etat.sauvegarde\n"
            "print(sorted(m for m in sys.modules if m.startswith('nations.observation')))")
    sortie = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                            check=True)
    assert sortie.stdout.strip() == "[]"
