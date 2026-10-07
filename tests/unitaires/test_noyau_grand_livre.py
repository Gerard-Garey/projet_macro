"""Grand livre du noyau : interface, identités, refus et diagnostics (issue #95).

Contrat : ADR 0012 (A2 à A8, points 8 et 9 décidés le 07/10/2026) ; critères
du rang 1b de #95 et leur complément du point 8. Chaque test énonce une
propriété (signe, identité, refus, égalité bit à bit), jamais une valeur à
reproduire. Le schéma d'état (#96) et les paramètres typés (#97) n'existent
pas encore : l'état d'ouverture et les tolérances sont des doubles minimaux,
et les flux sont tirés par un générateur à graine explicite.
"""

import ast
import dataclasses
import json
import math
import struct
from dataclasses import dataclass, make_dataclass
from pathlib import Path

import numpy as np
import pytest

from nations.noyau import catalogue as cat
from nations.noyau import grand_livre as gl_module
from nations.noyau import identites as idt
from nations.noyau.diagnostics import ArretNoyau, DefautComptable, RefusDeProposition
from nations.noyau.grand_livre import FluxPropose, ouvrir_pas

RACINE = Path(__file__).resolve().parents[2]
NOYAU = RACINE / "src" / "nations" / "noyau"
EPS = 1e-12

CHAMPS = cat.NOMS_POSTES + tuple(cat.VALEUR_NETTE_FLUX[s] for s in cat.SECTEURS)
EtatDouble = make_dataclass(
    "EtatDouble", [("t", int)] + [(c, float) for c in CHAMPS], frozen=True)


@dataclass(frozen=True)
class CadreDouble:
    """Double des paramètres du cadre (#97) : les deux tolérances, sans dimension."""

    tolerance_identite_pas: float = EPS
    tolerance_identite_cumulee: float = EPS


CADRE = CadreDouble()

# Positions d'ouverture d'essai, en u.m. ; S^CB est le plus petit des cinq S.
OUVERTURE = dict(D_H=600.0, D_F=400.0, L=500.0, B_H=200.0, B_Bk=300.0, B_CB=100.0,
                 Res=50.0, L_CB=20.0, M_G=150.0, K=900.0, IN=100.0)


def etat(t=0, v_flux=None, **positions):
    """État d'ouverture double, V^flux = V^stock sauf indication contraire."""
    p = dict(OUVERTURE)
    p.update(positions)
    v = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(p, s) for s in cat.SECTEURS}
    if v_flux is not None:
        v.update(v_flux)
    return EtatDouble(t=t, **p, **v)


def etat_suivant(cloture):
    return EtatDouble(t=cloture.t, **cloture.variables)


def flux(identifiant, *valeurs, proposant=None):
    """Flux proposé de la ligne, un montant par terme dans l'ordre du catalogue."""
    ligne = cat.LIGNE[identifiant]
    montants = {t.nom: float(v) for t, v in zip(ligne.termes, valeurs, strict=True)}
    return FluxPropose(identifiant, montants, proposant or ligne.proposant)


def plan_nul():
    """Toutes les lignes proposables au socle, à montant nul explicite (hors 21)."""
    return {l.identifiant: flux(l.identifiant, *([0.0] * len(l.termes)))
            for l in cat.LIGNES if l.proposant is not None and l.identifiant != "21"}


def plan_aleatoire(rng, echelle=1.0):
    """Montants tirés à graine explicite ; signes admis par chaque ligne.

    Les impôts (ligne 7) sont tirés positifs, comme les impôts nets d'un pas
    ordinaire, pour que la caisse de l'État tienne sur une longue trajectoire ;
    la ligne 7 négative est exercée par un test dédié.
    """
    plan = {}
    for ligne in cat.LIGNES:
        if ligne.proposant is None or ligne.identifiant == "21":
            continue
        bas = -echelle if ligne.admet_negatif and ligne.identifiant != "7" else 0.0
        valeurs = [float(rng.uniform(bas, echelle)) for _ in ligne.termes]
        plan[ligne.identifiant] = flux(ligne.identifiant, *valeurs)
    return plan


def declarer_si_perte(gl, plan):
    """Déclaration obligatoire du montant couvert, si la ligne 16 du plan est négative."""
    perte = plan["16"].montants["Pi_CB"]
    if perte < 0.0:
        gl.declarer_montant_couvert("16", montant_couvert_de_l_etat(gl, perte),
                                    "finances_publiques")


def remboursement(gl):
    """B7 sous la forme exacte −min(Res^{8b} ; L^CB), sur la position lue au grand livre."""
    return flux("21", -min(gl.position("Res"), gl.position("L_CB")))


def montant_couvert_de_l_etat(gl, perte):
    """c = min(|Π| ; max(0 ; M^{G,8a})), lu au grand livre (ADR 0012, A3.2 et A8)."""
    return min(-perte, max(0.0, gl.position("M_G")))


def derouler(gl, plan, rng_ordre=None, couvert=None, declarer_avant=False, ligne_21=None,
             lignes=None):
    """Déroule les onze clôtures ; rend (clôtures de phase, clôture du pas).

    `rng_ordre` permute l'ordre des appels dans chaque phase ; `couvert`
    déclare le montant couvert de la ligne 16 (avant ou après sa proposition).
    Sans `couvert`, une ligne 16 strictement négative est déclarée comme le
    ferait l'État, la déclaration étant obligatoire. `lignes` remplace les
    lignes de chaque phase (double du catalogue).
    """
    lignes = cat.LIGNES_DE_LA_PHASE if lignes is None else lignes
    clotures = []
    for phase in cat.PHASES:
        appels = []
        for ligne in lignes[phase]:
            if ligne.identifiant in plan:
                appels.append(("proposer", plan[ligne.identifiant]))
        if phase == "8b" and couvert is None and "16" in plan:
            perte = plan["16"].montants["Pi_CB"]
            if perte < 0.0:
                couvert = montant_couvert_de_l_etat(gl, perte)
        if phase == "8b" and couvert is not None:
            declaration = ("declarer", couvert)
            appels.insert(0 if declarer_avant else len(appels), declaration)
        if rng_ordre is not None:
            appels = [appels[i] for i in rng_ordre.permutation(len(appels))]
        for nature, argument in appels:
            if nature == "proposer":
                gl.proposer(argument)
            else:
                gl.declarer_montant_couvert("16", argument, "finances_publiques")
        if phase == "8c":
            gl.proposer(ligne_21(gl) if ligne_21 is not None else remboursement(gl))
        clotures.append(gl.clore_phase(phase))
    return clotures, gl.clore_pas()


def empreinte(objet):
    """Représentation bit à bit : chaque flottant par son motif binaire (−0,0 ≠ 0,0)."""
    if isinstance(objet, float):
        return struct.pack("<d", objet).hex()
    if isinstance(objet, (tuple, list)):
        return [empreinte(x) for x in objet]
    if isinstance(objet, dict) or hasattr(objet, "items"):
        return {k: empreinte(v) for k, v in objet.items()}
    if dataclasses.is_dataclass(objet):
        return {f.name: empreinte(getattr(objet, f.name)) for f in dataclasses.fields(objet)}
    return objet


# --------------------------------------------------------------------------
# Pas complets : identités tenues, propriétés de signe
# --------------------------------------------------------------------------


@pytest.mark.parametrize("graine", [1, 2, 3, 20261007])
def test_trajectoire_aleatoire_identites_tenues(graine):
    """24 pas tirés : aucune identité violée, résidus ≤ ε × S, Res_{t+1} · L^CB_{t+1} = 0."""
    rng = np.random.default_rng(graine)
    e = etat()
    for _ in range(24):
        clotures, fin = derouler(ouvrir_pas(e, CADRE), plan_aleatoire(rng, echelle=5.0))
        assert len(clotures) == 11
        assert [c.phase for c in clotures] == list(cat.PHASES)
        for c in clotures:
            for _, _, rapport in c.rapports:
                assert rapport <= EPS
        # Res_{t+1} ≥ 0 strict, exactement tenu par B7 sous −min.
        assert fin.variables["Res"] >= 0.0
        assert fin.variables["Res"] * fin.variables["L_CB"] == 0.0
        e = etat_suivant(fin)
    assert e.t == 24


def test_onze_clotures_dans_l_ordre():
    """A3.3 : onze clôtures, dont 8a, 8b, 8c ; toute autre clôture est refusée."""
    gl = ouvrir_pas(etat(), CADRE)
    assert gl.phase_courante() == "1"
    with pytest.raises(RefusDeProposition, match="phase 2 demandée, phase 1 attendue"):
        gl.clore_phase("2")
    plan = plan_nul()
    vues = []
    for phase in cat.PHASES:
        vues.append(gl.phase_courante())
        for ligne in cat.LIGNES_DE_LA_PHASE[phase]:
            if ligne.identifiant in plan:
                gl.proposer(plan[ligne.identifiant])
        if phase == "8c":
            gl.proposer(remboursement(gl))
        gl.clore_phase(phase)
    assert vues == list(cat.PHASES)
    gl.clore_pas()
    with pytest.raises(RefusDeProposition, match="pas déjà clos"):
        gl.phase_courante()
    with pytest.raises(RefusDeProposition):
        gl.clore_pas()


# --------------------------------------------------------------------------
# Critère 1 : chaque contrôle sait échouer
# --------------------------------------------------------------------------

FAMILLES = [idt.SOMME_LIGNE, idt.SOMME_COLONNE, idt.CLOTURE_POSTE, idt.VARIATION_MONNAIE,
            idt.VARIATION_MONNAIE_CENTRALE]


@pytest.mark.parametrize("regle", FAMILLES, ids=lambda r: r.nom)
@pytest.mark.parametrize("echelle", [1.0, 3.7e9, 2.5e-4])
def test_identite_par_pas_sait_echouer(regle, echelle):
    """2 ε S est un défaut, 0,5 ε S passe, quelle que soit l'échelle (forme |r| ≤ ε S)."""
    assert idt.verifier_identites(regle, [0.5 * EPS * echelle], [echelle],
                                  [("banque", None, None)], EPS, t=3, phase="6")[1] <= EPS
    assert idt.verifier_identite(-0.5 * EPS * echelle, echelle, EPS, regle, t=3, phase="6") <= EPS
    with pytest.raises(DefautComptable) as erreur:
        idt.verifier_identites(regle, [2 * EPS * echelle], [echelle],
                               [("banque", "7", "T_H")], EPS, t=3, phase="6")
    assert erreur.value.regle == regle.nom
    assert (erreur.value.t, erreur.value.phase) == (3, "6")
    assert erreur.value.secteur == "banque" and erreur.value.ligne == "7"
    assert erreur.value.rapport == pytest.approx(2 * EPS)
    with pytest.raises(DefautComptable):
        idt.verifier_identite(-2 * EPS * echelle, echelle, EPS, regle, t=3, phase="6")


def test_tolerance_par_pas_forme_commune():
    """`eq:noyau-tolerance-pas` : |r| ≤ ε S, NaN refusé, échelle nulle sans division."""
    assert idt.dans_la_tolerance(0.5 * EPS * 10.0, 10.0, EPS)
    assert not idt.dans_la_tolerance(2 * EPS * 10.0, 10.0, EPS)
    assert not idt.dans_la_tolerance(math.nan, 10.0, EPS)
    assert idt.dans_la_tolerance(0.0, 0.0, EPS)
    assert not idt.dans_la_tolerance(1e-300, 0.0, EPS)


@pytest.mark.parametrize("facteur, defaut", [(0.5, False), (2.0, True)])
def test_identite_cumulee_sait_echouer(facteur, defaut):
    """`eq:noyau-tolerance-cumulee` (et les deux valeurs nettes) : V^flux décalée de f ε_V S."""
    e0 = etat()
    s_banque = ouvrir_pas(e0, CADRE).echelle("banque")
    nom = cat.VALEUR_NETTE_FLUX["banque"]
    decale = etat(v_flux={nom: getattr(e0, nom) + facteur * EPS * s_banque})
    gl = ouvrir_pas(decale, CADRE)
    if defaut:
        with pytest.raises(DefautComptable) as erreur:
            derouler(gl, plan_nul())
        assert erreur.value.regle == "eq:noyau-tolerance-cumulee"
        assert erreur.value.secteur == "banque" and erreur.value.phase == "9"
    else:
        derouler(gl, plan_nul())


@pytest.mark.parametrize("facteur, defaut", [(0.5, False), (2.0, True)])
@pytest.mark.parametrize("poste", ["D_H", "Res", "K", "L_CB"])
def test_cloture_poste_sait_echouer_dans_le_grand_livre(poste, facteur, defaut):
    """Écart injecté dans une position (hors ligne) : 2 ε S est relevé, 0,5 ε S passe.

    L'injection passe par l'attribut privé : c'est la simulation d'une
    corruption, que l'interface publique rend impossible (test plus bas).
    """
    gl = ouvrir_pas(etat(), CADRE)
    p = cat.POSTE[poste]
    bilans = [p.detenteur] + ([p.emetteur] if p.emetteur else [])
    echelle = min(gl.echelle(s) for s in bilans)
    gl._positions[poste] += facteur * EPS * echelle
    # Phases 1 et 2 sans ligne : aucune position n'y change par l'interface,
    # et leurs contrôles sont sautés ; la phase 3 est la première qui exécute.
    jusqu_a(gl, "3", plan_nul())
    if defaut:
        with pytest.raises(DefautComptable) as erreur:
            gl.clore_phase("3")
        assert erreur.value.regle == "eq:noyau-cloture-poste"
        assert erreur.value.terme == poste
    else:
        gl.clore_phase("3")


def test_reserves_de_cloture_strictes():
    """Res_{t+1} = 0 passe ; −1 ulp et −0,5 ε S sont des défauts (point 8, (iii-b))."""
    idt.verifier_reserves_cloture(0.0, 100.0, t=0)
    idt.verifier_reserves_cloture(-0.0, 100.0, t=0)
    for x in (-math.ulp(0.0), -math.ulp(1.0), -0.5 * EPS * 100.0):
        with pytest.raises(DefautComptable) as erreur:
            idt.verifier_reserves_cloture(x, 100.0, t=4)
        assert erreur.value.regle == "eq:noyau-reserves-cloture"
        assert erreur.value.phase == "9"


@pytest.mark.parametrize("facteur, defaut", [(-0.5, False), (-2.0, True), (0.0, False)])
def test_caisse_nette_a_epsilon_s_du_payeur(facteur, defaut):
    """Lecture nette : −0,5 ε S_payeur passe, −2 ε S_payeur est un défaut."""
    echelles = {"menages": 1234.5, "entreprises": 10.0, "etat": 7.0}
    mouvements = {"1": {"D_H": -1.0, "D_F": 1.0}, "5": {"D_H": 0.5}}
    for moyen, payeur in cat.MOYENS_LECTURE_NETTE:
        positions = {"D_H": 1.0, "D_F": 1.0, "M_G": 1.0}
        positions[moyen] = facteur * EPS * echelles[payeur]
        if defaut:
            with pytest.raises(DefautComptable) as erreur:
                idt.verifier_caisse(positions, echelles, EPS, t=0, phase="5",
                                    positions_debut=dict.fromkeys(positions, 1.0),
                                    mouvements_par_ligne=mouvements)
            assert erreur.value.regle == "eq:noyau-caisse-nette"
            assert (erreur.value.secteur, erreur.value.moyen) == (payeur, moyen)
            assert erreur.value.lignes_debitrices == (("1",) if moyen == "D_H" else ())
        else:
            idt.verifier_caisse(positions, echelles, EPS, t=0, phase="5",
                                positions_debut=dict.fromkeys(positions, 1.0),
                                mouvements_par_ligne=mouvements)


def test_echelle_nulle_est_un_defaut():
    """A3.1 (ii), point 11 : S_{s,t} > 0 à l'ouverture ; une échelle nulle n'est jamais un repli."""
    e = etat(D_H=0.0, B_H=0.0)
    with pytest.raises(DefautComptable) as erreur:
        ouvrir_pas(e, CADRE)
    assert erreur.value.regle == "eq:noyau-echelle-bilan"
    assert erreur.value.secteur == "menages" and erreur.value.phase == "0"


def test_echelle_somme_des_valeurs_absolues_valeur_nette_comprise():
    """`eq:noyau-echelle-bilan` : S = Σ |postes| + |V|, |Res| et |E| compris."""
    p = dict(OUVERTURE)
    e_bk = p["L"] + p["B_Bk"] + p["Res"] - p["D_H"] - p["D_F"] - p["L_CB"]
    e_cb = p["B_CB"] + p["L_CB"] - p["Res"] - p["M_G"]
    gl = ouvrir_pas(etat(), CADRE)
    assert gl.echelle("banque") == pytest.approx(
        p["L"] + p["B_Bk"] + abs(p["Res"]) + p["D_H"] + p["D_F"] + p["L_CB"] + abs(e_bk),
        rel=1e-15)
    assert gl.echelle("banque_centrale") == pytest.approx(
        p["B_CB"] + p["L_CB"] + abs(p["Res"]) + p["M_G"] + abs(e_cb), rel=1e-15)
    assert e_bk < 0 and e_cb < 0  # les valeurs absolues de E y servent


# --------------------------------------------------------------------------
# Critère 2 : échelles
# --------------------------------------------------------------------------


def test_separation_de_l_echelle_de_la_banque_centrale():
    """Un résidu de 2 ε S^CB dans la colonne de la banque centrale est détecté.

    Sous la lecture (β), la somme des S des secteurs touchés l'aurait masqué.
    """
    gl = ouvrir_pas(etat(), CADRE)
    s = [gl.echelle(x) for x in cat.SECTEURS]
    s_cb = gl.echelle("banque_centrale")
    assert s_cb == min(s) and 2 * EPS * s_cb < 0.5 * EPS * sum(s)
    residus = [0.0, 0.0, 0.0, 2 * EPS * s_cb, 0.0]
    objets = [(x, None, None) for x in cat.SECTEURS]
    with pytest.raises(DefautComptable) as erreur:
        idt.verifier_identites(idt.SOMME_COLONNE, residus, s, objets, EPS, t=0, phase="8a")
    assert erreur.value.secteur == "banque_centrale"
    # Dans le grand livre : Res est tenue par la banque et par la banque
    # centrale ; un écart de 2 ε S^CB, sous ε S^Bk, est relevé au bilan de la BC.
    assert 2 * EPS * s_cb < EPS * gl.echelle("banque")
    gl._positions["Res"] += 2 * EPS * s_cb
    jusqu_a(gl, "3", plan_nul())
    with pytest.raises(DefautComptable) as erreur:
        gl.clore_phase("3")
    assert erreur.value.secteur == "banque_centrale" and erreur.value.terme == "Res"


def test_echelle_figee_a_l_ouverture():
    """S lue en fin de chaque phase est égale à sa valeur de la phase 0 (P33 (a))."""
    rng = np.random.default_rng(5)
    gl = ouvrir_pas(etat(), CADRE)
    s0 = {s: gl.echelle(s) for s in cat.SECTEURS}
    plan = plan_aleatoire(rng, echelle=5.0)
    for phase in cat.PHASES:
        for ligne in cat.LIGNES_DE_LA_PHASE[phase]:
            if ligne.identifiant in plan:
                gl.proposer(plan[ligne.identifiant])
        if phase == "8b":
            declarer_si_perte(gl, plan)
        if phase == "8c":
            gl.proposer(remboursement(gl))
        gl.clore_phase(phase)
        assert {s: gl.echelle(s) for s in cat.SECTEURS} == s0
        if phase not in ("1", "2"):
            assert any(gl.position(p) != gl.ouverture(p) for p in cat.NOMS_POSTES)


def test_lecture_alpha_echelle_de_ligne(monkeypatch):
    """Point 9 (α) : une porte ligne par ligne se contrôle au plus petit S des secteurs touchés.

    On fausse la signature déclarée de la ligne 11c (État → banque centrale,
    S^CB la plus petite) : la porte ΔH ne tient plus et l'écart est relevé.
    """
    faussee = dataclasses.replace(cat.LIGNE["11c"], signature=(0, 1))
    phase6 = tuple(faussee if l.identifiant == "11c" else l for l in cat.LIGNES_DE_LA_PHASE["6"])
    monkeypatch.setitem(gl_module.LIGNES_DE_LA_PHASE, "6", phase6)
    gl = ouvrir_pas(etat(), CADRE)
    plan = plan_nul()
    plan["11c"] = flux("11c", 1.0)
    with pytest.raises(DefautComptable) as erreur:
        derouler(gl, plan)
    assert erreur.value.regle == "eq:noyau-variation-monnaie-centrale"
    assert erreur.value.ligne == "11c" and erreur.value.phase == "6"
    assert erreur.value.echelle == min(gl.echelle("etat"), gl.echelle("banque_centrale"))


# --------------------------------------------------------------------------
# Critère 3 : double calcul indépendant de la valeur nette
# --------------------------------------------------------------------------


def test_lignes_financieres_sans_effet_sur_v_flux():
    """Lignes 18, 19a et 21 seules : V^flux_{t+1} = V^flux_t bit à bit."""
    e = etat()
    plan = plan_nul()
    plan["18"] = flux("18", 37.25)
    plan["19a-ménages"] = flux("19a-ménages", 11.5)
    plan["19a-banque"] = flux("19a-banque", -3.0)
    plan["19a-BC"] = flux("19a-BC", 8.125)
    _, fin = derouler(ouvrir_pas(e, CADRE), plan, ligne_21=lambda gl: flux("21", 13.0))
    for s in cat.SECTEURS:
        nom = cat.VALEUR_NETTE_FLUX[s]
        assert empreinte(fin.variables[nom]) == empreinte(getattr(e, nom))
    assert fin.variables["L"] == e.L + 37.25 and fin.variables["L_CB"] == e.L_CB + 13.0


def test_v_flux_tiree_des_seuls_montants_executes():
    """V^flux_{t+1} = V^flux_t + Σ des montants exécutés des lignes 1 à 16 (colonne de résultat)."""
    rng = np.random.default_rng(11)
    e = etat()
    gl = ouvrir_pas(e, CADRE)
    derouler(gl, plan_aleatoire(rng, echelle=3.0))
    for s in cat.SECTEURS:
        colonne = cat.COLONNE_DE_RESULTAT[s]
        resultat = 0.0
        for ligne in cat.LIGNES:
            if ligne.resultat:
                resultat += gl.montant_execute(ligne.identifiant, colonne)
        attendu = getattr(e, cat.VALEUR_NETTE_FLUX[s]) + resultat
        assert gl.valeur_nette_flux(s) == pytest.approx(attendu, rel=0, abs=EPS * gl.echelle(s))
        assert abs(gl.valeur_nette_stock(s) - gl.valeur_nette_flux(s)) <= EPS * gl.echelle(s)


def test_fermeture_du_systeme_sur_la_cloture_du_pas():
    """Critère 16, relu (annotation du 07/10/2026, point 4) : propriété vérifiée en test.

    Σ_s V^stock_s = K + IN sur l'état de clôture de chaque pas (`ClotureDuPas`),
    à ε × min_s S_s près (lecture (α)) ; le moteur ne la contrôle plus.
    """
    rng = np.random.default_rng(3)
    e = etat()
    for _ in range(48):
        gl = ouvrir_pas(e, CADRE)
        clotures, fin = derouler(gl, plan_aleatoire(rng, echelle=7.0))
        assert all(r[0] != "fermeture du système" for c in clotures for r in c.rapports)
        v = fin.variables
        somme = 0.0
        for s in cat.SECTEURS:
            somme += idt.valeur_nette_stock(v, s)
        assert abs(somme - (v["K"] + v["IN"])) <= EPS * min(gl.echelle(s) for s in cat.SECTEURS)
        e = etat_suivant(fin)


def test_fermeture_du_systeme_table_des_signes():
    """Statique : chaque instrument +1 chez son détenteur, −1 chez son émetteur ; K et IN +1.

    Σ_s V_s = K + IN en découle pour toutes positions : c'est pourquoi le
    contrôle est une tautologie de la tenue par positions.
    """
    somme = dict.fromkeys(cat.NOMS_POSTES, 0.0)
    for s in cat.SECTEURS:
        for poste, signe in cat.POSTES_DU_BILAN[s]:
            p = cat.POSTE[poste]
            assert signe == (1.0 if p.detenteur == s else -1.0)
            assert s == p.detenteur or s == p.emetteur
            somme[poste] += signe
    assert somme == {p: (1.0 if p in ("K", "IN") else 0.0) for p in cat.NOMS_POSTES}
    assert not hasattr(idt, "FERMETURE")


# --------------------------------------------------------------------------
# Critère 4 : reprise exacte
# --------------------------------------------------------------------------


def test_reprise_exacte_bit_a_bit():
    """Reprise à t = 6 (sauvegarde JSON, `repr` des flottants) : relevé identique bit à bit."""
    def trajectoire(n, e, graine):
        rng = np.random.default_rng(graine)
        releves = []
        for _ in range(n):
            plans = plan_aleatoire(rng, echelle=4.0)
            clotures, fin = derouler(ouvrir_pas(e, CADRE), plans)
            releves.append(empreinte(clotures))
            e = etat_suivant(fin)
        return releves, e

    graines = np.random.SeedSequence(20261007).spawn(2)
    sans_interruption = []
    e = etat()
    for g in graines:
        releves, e = trajectoire(6, e, g)
        sans_interruption += releves
    final_continu = empreinte(e)

    graines = np.random.SeedSequence(20261007).spawn(2)
    releves, e = trajectoire(6, etat(), graines[0])
    document = json.dumps({c: getattr(e, c) for c in ("t",) + CHAMPS}, allow_nan=False)
    repris = EtatDouble(**json.loads(document))
    suite, e = trajectoire(6, repris, graines[1])
    assert releves + suite == sans_interruption
    assert empreinte(e) == final_continu


# --------------------------------------------------------------------------
# Critères 5 et 6 : catalogue, phases, unicité, proposant
# --------------------------------------------------------------------------


@pytest.mark.parametrize("identifiant", ["17", "20", "22"])
def test_contreparties_non_proposables(identifiant):
    gl = ouvrir_pas(etat(), CADRE)
    ligne = cat.LIGNE[identifiant]
    montants = {t.nom: 1.0 for t in ligne.termes}
    with pytest.raises(RefusDeProposition, match="contrepartie de règlement"):
        gl.proposer(FluxPropose(identifiant, montants, "banque"))


@pytest.mark.parametrize("identifiant", [l.identifiant for l in cat.LIGNES
                                         if l.proposant is not None])
def test_chaque_ligne_refusee_hors_de_sa_phase(identifiant):
    """Une ligne n'est acceptée que dans sa phase ; les phases 1, 2 et 9 n'en acceptent aucune."""
    ligne = cat.LIGNE[identifiant]
    proposition = flux(identifiant, *([0.0] * len(ligne.termes)))
    plan = plan_nul()
    gl = ouvrir_pas(etat(), CADRE)
    acceptee_dans = []
    for phase in cat.PHASES:
        try:
            gl.proposer(proposition)
            acceptee_dans.append(phase)
        except RefusDeProposition as refus:
            assert refus.ligne == identifiant and refus.phase == phase
            if phase == "9":
                assert "aucun flux en phase 9" in str(refus)
        for l in cat.LIGNES_DE_LA_PHASE[phase]:
            if l.identifiant in plan and l.identifiant != identifiant:
                gl.proposer(plan[l.identifiant])
        if phase == "8c" and identifiant != "21":
            gl.proposer(remboursement(gl))
        gl.clore_phase(phase)
    assert acceptee_dans == [ligne.phase]


def test_proposition_dupliquee_refusee():
    gl = ouvrir_pas(etat(), CADRE)
    gl.clore_phase("1")
    gl.clore_phase("2")
    gl.proposer(flux("18", 1.0))
    with pytest.raises(RefusDeProposition, match="seconde proposition") as refus:
        gl.proposer(flux("18", 1.0))
    assert refus.value.ligne == "18" and refus.value.phase == "3"


def test_proposition_d_un_autre_bloc_refusee():
    gl = ouvrir_pas(etat(), CADRE)
    gl.clore_phase("1")
    gl.clore_phase("2")
    with pytest.raises(RefusDeProposition, match="proposant 'banque'") as refus:
        gl.proposer(flux("18", 1.0, proposant="banque"))
    assert refus.value.secteur == "banque"
    gl.proposer(flux("18", 1.0))  # le proposant déclaré, lui, est admis


@pytest.mark.parametrize("identifiant", ["19b-ménages", "19b-banque"])
def test_lignes_19b_sans_proposant_au_socle(identifiant):
    gl = ouvrir_pas(etat(), CADRE)
    for phase in ("1", "2", "3", "4", "5", "6"):
        plan = plan_nul()
        for l in cat.LIGNES_DE_LA_PHASE[phase]:
            gl.proposer(plan[l.identifiant])
        gl.clore_phase(phase)
    with pytest.raises(RefusDeProposition, match="sans proposant au socle"):
        gl.proposer(FluxPropose(identifiant, {cat.LIGNE[identifiant].termes[0].nom: 1.0},
                                "banque_centrale"))


def test_ligne_oubliee_refusee_a_la_cloture():
    """Une ligne à proposant déclaré oubliée est un refus à la clôture, jamais un zéro."""
    gl = ouvrir_pas(etat(), CADRE)
    for phase in ("1", "2", "3", "4", "5"):
        plan = plan_nul()
        for l in cat.LIGNES_DE_LA_PHASE[phase]:
            gl.proposer(plan[l.identifiant])
        gl.clore_phase(phase)
    plan = plan_nul()
    for l in cat.LIGNES_DE_LA_PHASE["6"]:
        if l.identifiant != "11b":
            gl.proposer(plan[l.identifiant])
    with pytest.raises(RefusDeProposition, match="non proposée") as refus:
        gl.clore_phase("6")
    assert refus.value.ligne == "11b" and refus.value.secteur == "finances_publiques"


@pytest.mark.parametrize("montants, motif", [
    ({}, "terme manquant"),
    ({"T_H": 1.0}, "terme manquant"),
    ({"T_H": 1.0, "T_F": 1.0, "Tr": 1.0}, "terme en trop"),
    ({"T_H": 1, "T_F": 1.0}, "float fini attendu"),
    ({"T_H": np.float64(1.0), "T_F": 1.0}, "float fini attendu"),
    ({"T_H": math.nan, "T_F": 1.0}, "float fini attendu"),
    ({"T_H": math.inf, "T_F": 1.0}, "float fini attendu"),
])
def test_termes_et_montants_refuses(montants, motif):
    gl = ouvrir_pas(etat(), CADRE)
    for phase in ("1", "2", "3", "4", "5"):
        plan = plan_nul()
        for l in cat.LIGNES_DE_LA_PHASE[phase]:
            gl.proposer(plan[l.identifiant])
        gl.clore_phase(phase)
    with pytest.raises(RefusDeProposition, match=motif):
        gl.proposer(FluxPropose("7", montants, "finances_publiques"))


def test_ligne_inconnue_refusee():
    gl = ouvrir_pas(etat(), CADRE)
    with pytest.raises(RefusDeProposition, match="inconnue"):
        gl.proposer(FluxPropose("23", {"X": 1.0}, "banque"))


# --------------------------------------------------------------------------
# Critère 7 : ordre canonique, permutation bit à bit
# --------------------------------------------------------------------------


@pytest.mark.parametrize("graine", [7, 8, 9])
def test_permutation_des_appels_bit_a_bit(graine):
    """Toute permutation des appels d'une phase (8 (b) comprise) laisse la clôture identique.

    Les montants sont d'échelles très différentes, pour que l'ordre des
    additions compte en double précision s'il n'était pas canonique.
    """
    rng = np.random.default_rng(graine)
    plan = plan_aleatoire(rng, echelle=1.0)
    for identifiant in ("1", "2", "7", "10", "6", "9", "14", "15", "11a"):
        ligne = cat.LIGNE[identifiant]
        plan[identifiant] = flux(identifiant, *[float(rng.uniform(0, 1)) * 10.0 ** float(
            rng.integers(-6, 3)) for _ in ligne.termes])
    plan["16"] = flux("16", -0.75)
    reference = None
    for k in range(6):
        ordre = None if k == 0 else np.random.default_rng(graine * 100 + k)
        clotures, fin = derouler(ouvrir_pas(etat(), CADRE), plan, rng_ordre=ordre,
                                 couvert=0.5, declarer_avant=bool(k % 2))
        resultat = empreinte((clotures, fin))
        if reference is None:
            reference = resultat
        assert resultat == reference


def test_l_ordre_d_execution_compte_en_double_precision(monkeypatch):
    """Témoin : sous un autre ordre des lignes, la clôture diffère au bit près.

    C'est l'ordre canonique du catalogue, non l'ordre d'arrivée, qui rend la
    permutation des appels sans effet (test précédent).
    """
    rng = np.random.default_rng(7)
    plan = plan_aleatoire(rng, echelle=1.0)
    for identifiant in ("6", "7", "9", "10", "11a", "14", "15"):
        ligne = cat.LIGNE[identifiant]
        plan[identifiant] = flux(identifiant, *[float(rng.uniform(0, 1)) * 10.0 ** float(
            rng.integers(-6, 3)) for _ in ligne.termes])
    canonique = empreinte(derouler(ouvrir_pas(etat(), CADRE), plan))
    monkeypatch.setitem(gl_module.LIGNES_DE_LA_PHASE, "6",
                        tuple(reversed(cat.LIGNES_DE_LA_PHASE["6"])))
    inverse = derouler(ouvrir_pas(etat(), CADRE), plan)
    assert empreinte(inverse[1]) != canonique[1]


# --------------------------------------------------------------------------
# Critère 8 : règlements routés ligne par ligne
# --------------------------------------------------------------------------


def test_table_de_routage_faussee_detectee_par_les_colonnes(monkeypatch):
    """11b réglée en dépôts des ménages au lieu de réserves : la somme des colonnes la relève."""
    ligne = cat.LIGNE["11b"]
    terme = dataclasses.replace(ligne.termes[0], reglement=(("D_H", 1.0),))
    faussee = dataclasses.replace(ligne, termes=(terme,))
    phase6 = tuple(faussee if l.identifiant == "11b" else l for l in cat.LIGNES_DE_LA_PHASE["6"])
    monkeypatch.setitem(gl_module.LIGNES_DE_LA_PHASE, "6", phase6)
    plan = plan_nul()
    plan["11b"] = flux("11b", 2.5)
    with pytest.raises(DefautComptable) as erreur:
        derouler(ouvrir_pas(etat(), CADRE), plan)
    assert erreur.value.regle == "eq:noyau-somme-colonne"
    assert erreur.value.phase == "6"


def test_contreparties_derivees_des_moyens_de_paiement():
    """17, 20, 22 = variations de D_H + D_F, Res et M^G sur le pas, routées ligne par ligne."""
    rng = np.random.default_rng(21)
    e = etat()
    gl = ouvrir_pas(e, CADRE)
    _, fin = derouler(gl, plan_aleatoire(rng, echelle=6.0))
    v = fin.variables
    s_bk = gl.echelle("banque")
    for identifiant, postes in (("17", ("D_H", "D_F")), ("20", ("Res",)), ("22", ("M_G",))):
        variation = sum(v[p] - getattr(e, p) for p in postes)
        assert abs(gl.montant_execute_ligne(identifiant) - variation) <= EPS * s_bk
    # Cellules de 17 : −ΔD_H (ménages), −ΔD_F (entreprises, capital), leur somme à la banque.
    assert gl.montant_execute("17", "banque") == -(
        gl.montant_execute("17", "menages") + gl.montant_execute("17", "entreprises_capital"))
    assert gl.montant_execute("17", "entreprises_courant") == 0.0
    assert gl.montant_execute("20", "banque") == -gl.montant_execute("20", "banque_centrale")
    assert gl.montant_execute("22", "etat") == -gl.montant_execute("22", "banque_centrale")


# --------------------------------------------------------------------------
# Critère 9 : portes à montant signé, à l'exécution
# --------------------------------------------------------------------------


@pytest.mark.parametrize("identifiant, montant", [
    ("16", -2.5), ("18", -4.0), ("19a-ménages", -1.5), ("19a-banque", -2.0),
    ("19a-BC", -3.0), ("21", -6.0), ("16", 2.5), ("18", 4.0), ("21", 6.0),
])
def test_portes_signees_a_l_execution(identifiant, montant):
    """ΔM = ΔD et ΔH = ΔRes, signés, pour une ligne seule non nulle, négative comprise."""
    e = etat()
    gl = ouvrir_pas(e, CADRE)
    plan = plan_nul()
    if identifiant != "21":
        plan[identifiant] = flux(identifiant, montant)
    derouler(gl, plan, ligne_21=lambda g: flux("21", montant if identifiant == "21" else 0.0))
    sgn_m, sgn_h = cat.LIGNE[identifiant].signature
    executes = gl.montant_execute_ligne(identifiant)
    assert executes == montant
    delta_d = (gl.position("D_H") - e.D_H) + (gl.position("D_F") - e.D_F)
    assert delta_d == sgn_m * montant
    assert gl.position("Res") - e.Res == sgn_h * montant


# --------------------------------------------------------------------------
# Critère 10 : sous-phases et lectures
# --------------------------------------------------------------------------


def test_position_lue_en_8c_est_le_flottant_auquel_21_s_ajoute():
    """B7 en −min : Res_{t+1} = Res^{8b} + ΔL^CB exactement ; 0 si Res^{8b} ≤ L^CB."""
    rng = np.random.default_rng(31)
    for _ in range(200):
        res0 = float(rng.uniform(0.0, 3.0))
        e = etat(Res=res0, L_CB=float(rng.uniform(0.0, 3.0)))
        gl = ouvrir_pas(e, CADRE)
        lu = {}

        def b7(g):
            lu["Res"] = g.position("Res")
            lu["L_CB"] = g.position("L_CB")
            return flux("21", -min(lu["Res"], lu["L_CB"]))

        derouler(gl, plan_aleatoire(rng, echelle=2.0), ligne_21=b7)
        assert gl.position("Res") == lu["Res"] + -min(lu["Res"], lu["L_CB"])
        if lu["Res"] <= lu["L_CB"]:
            assert gl.position("Res") == 0.0
        assert gl.position("Res") * gl.position("L_CB") == 0.0
        assert gl.ouverture("Res") == res0  # ouverture figée, lecture distincte


def test_lecture_avant_cloture_refusee():
    """Montant exécuté lu avant la clôture de sa phase : refus, jamais un zéro."""
    gl = ouvrir_pas(etat(), CADRE)
    with pytest.raises(RefusDeProposition, match="avant la clôture"):
        gl.montant_execute("5", "menages")
    gl.clore_phase("1")
    gl.clore_phase("2")
    gl.proposer(flux("18", 3.0))
    gl.clore_phase("3")
    assert gl.montant_execute("18", "banque") == -3.0
    assert gl.montant_execute("18", "entreprises_capital") == 3.0
    assert gl.montant_execute_ligne("18") == 3.0
    with pytest.raises(RefusDeProposition, match="avant la clôture"):
        gl.montant_execute_ligne("17")
    with pytest.raises(RefusDeProposition, match="avant la clôture"):
        gl.valeur_nette_flux("banque")
    with pytest.raises(RefusDeProposition, match="colonne inconnue"):
        gl.montant_execute("18", "reel")


def test_cellules_exécutees_de_la_ligne_7():
    gl = ouvrir_pas(etat(), CADRE)
    plan = plan_nul()
    plan["7"] = flux("7", 2.0, 3.0)
    derouler(gl, plan)
    assert gl.montant_execute("7", "menages") == -2.0
    assert gl.montant_execute("7", "entreprises_courant") == -3.0
    assert gl.montant_execute("7", "etat") == 5.0
    assert gl.montant_execute("7", "banque") == 0.0
    assert gl.montant_execute_ligne("7") == 5.0
    assert gl.montant_execute_ligne("19b-ménages") == 0.0


# --------------------------------------------------------------------------
# Critères 11 et 12 : lecture nette de la caisse et diagnostic
# --------------------------------------------------------------------------


def jusqu_a(gl, derniere, plan):
    """Propose les lignes du plan jusqu'à la phase `derniere`, close toutes les précédentes.

    Une ligne 16 négative déclarée hors de 8 (b) reste au test (aucune
    déclaration ici quand 8 (b) est la dernière phase).
    """
    for phase in cat.PHASES[:cat.PHASES.index(derniere) + 1]:
        for l in cat.LIGNES_DE_LA_PHASE[phase]:
            if l.identifiant in plan:
                gl.proposer(plan[l.identifiant])
        if phase == "8b" and phase != derniere and "16" in plan:
            declarer_si_perte(gl, plan)
        if phase == "8c":
            gl.proposer(remboursement(gl))
        if phase == derniere:
            return
        gl.clore_phase(phase)


@pytest.mark.parametrize("facteur, defaut", [(0.5, False), (2.0, True)])
def test_caisse_des_menages_dans_le_grand_livre(facteur, defaut):
    """Consommation qui dépasse D_H de f ε S_H : 0,5 passe (la position reste négative), 2 arrête."""
    e = etat(D_H=1.0)
    gl = ouvrir_pas(e, CADRE)
    plan = plan_nul()
    plan["1"] = flux("1", 1.0 + facteur * EPS * gl.echelle("menages"))
    jusqu_a(gl, "5", plan)
    if not defaut:
        gl.clore_phase("5")
        assert gl.position("D_H") < 0.0  # jamais ramenée à zéro
        return
    with pytest.raises(DefautComptable) as erreur:
        gl.clore_phase("5")
    d = erreur.value
    assert (d.phase, d.secteur, d.moyen, d.lignes_debitrices) == ("5", "menages", "D_H", ("1",))
    assert d.position_debut == pytest.approx(1.0 / gl.echelle("menages"), rel=1e-15)
    assert d.position_fin == pytest.approx(-facteur * EPS, rel=1e-3)
    message = str(d)
    for mot in ("phase 5", "menages", "D_H", "ligne 1", "début de phase", "fin de phase"):
        assert mot in message
    # L'arrêt n'assemble aucun état t + 1, et le grand livre refuse tout appel.
    with pytest.raises(RefusDeProposition, match="arrêté"):
        gl.clore_pas()
    with pytest.raises(RefusDeProposition, match="arrêté"):
        gl.phase_courante()


def test_diagnostic_de_caisse_nomme_les_lignes_debitrices_de_la_phase():
    """État en phase 6 : transferts, intérêts sur titres débitent M^G ; les impôts le créditent."""
    e = etat(M_G=1.0)
    gl = ouvrir_pas(e, CADRE)
    plan = plan_nul()
    plan["6"] = flux("6", 0.8)
    plan["11a"] = flux("11a", 0.5)
    plan["11c"] = flux("11c", 0.25)
    plan["7"] = flux("7", 0.1, 0.1)
    jusqu_a(gl, "6", plan)
    with pytest.raises(DefautComptable) as erreur:
        gl.clore_phase("6")
    assert erreur.value.secteur == "etat" and erreur.value.moyen == "M_G"
    assert erreur.value.lignes_debitrices == ("6", "11a", "11c")


def test_banque_et_banque_centrale_exclues_de_la_lecture_nette():
    """Critère 11 : seuls D_H, D_F et M^G sont contrôlés ; Res négatives en cours de pas passent."""
    assert [m for m, _ in cat.MOYENS_LECTURE_NETTE] == ["D_H", "D_F", "M_G"]
    assert {p for _, p in cat.MOYENS_LECTURE_NETTE} == {"menages", "entreprises", "etat"}


# --------------------------------------------------------------------------
# Critère 13 : montant couvert de la ligne 16
# --------------------------------------------------------------------------


def jusqu_a_8b(e):
    gl = ouvrir_pas(e, CADRE)
    jusqu_a(gl, "8b", plan_nul() | {"16": None})
    return gl


def test_montant_couvert_refuse_hors_du_domaine():
    def gl8b():
        gl = ouvrir_pas(etat(), CADRE)
        plan = plan_nul()
        del plan["16"]
        jusqu_a(gl, "8b", plan)
        return gl

    cas = [
        (lambda g: g.declarer_montant_couvert("16", 1.0, "banque_centrale"), "liste fermée"),
        (lambda g: g.declarer_montant_couvert("7", 1.0, "finances_publiques"), "liste fermée"),
        (lambda g: g.declarer_montant_couvert("16", -0.5, "finances_publiques"), "négatif"),
        (lambda g: g.declarer_montant_couvert("16", 1, "finances_publiques"), "float fini"),
        (lambda g: g.declarer_montant_couvert("16", math.nan, "finances_publiques"),
         "float fini"),
    ]
    for appel, motif in cas:
        with pytest.raises(RefusDeProposition, match=motif):
            appel(gl8b())
    # Ligne 16 positive, dans les deux ordres.
    for avant in (True, False):
        g = gl8b()
        appels = [lambda: g.proposer(flux("16", 2.0)),
                  lambda: g.declarer_montant_couvert("16", 1.0, "finances_publiques")]
        if avant:
            appels.reverse()
        appels[0]()
        with pytest.raises(RefusDeProposition, match="non négative"):
            appels[1]()
    # c > |Π|, dans les deux ordres : refusé, jamais écrêté.
    for avant in (True, False):
        g = gl8b()
        appels = [lambda: g.proposer(flux("16", -2.0)),
                  lambda: g.declarer_montant_couvert("16", 2.0 + 1e-9, "finances_publiques")]
        if avant:
            appels.reverse()
        appels[0]()
        with pytest.raises(RefusDeProposition, match="supérieur à la perte"):
            appels[1]()
    # Seconde déclaration.
    g = gl8b()
    g.proposer(flux("16", -2.0))
    g.declarer_montant_couvert("16", 1.0, "finances_publiques")
    with pytest.raises(RefusDeProposition, match="seconde déclaration"):
        g.declarer_montant_couvert("16", 1.0, "finances_publiques")
    # Déclaration sans proposition : refus à la clôture de 8 (b).
    g = ouvrir_pas(etat(), CADRE)
    plan = plan_nul()
    del plan["16"]
    jusqu_a(g, "8b", plan)
    g.declarer_montant_couvert("16", 0.0, "finances_publiques")
    with pytest.raises(RefusDeProposition, match="non proposée"):
        g.clore_phase("8b")
    # Hors de 8 (b).
    g = ouvrir_pas(etat(), CADRE)
    plan = plan_nul()
    jusqu_a(g, "8a", plan)
    with pytest.raises(RefusDeProposition, match="phase 8a"):
        g.declarer_montant_couvert("16", 0.0, "finances_publiques")


def test_refus_d_appel_laisse_le_grand_livre_inchange():
    """Un refus au second appel n'enregistre rien : l'appel correct est ensuite admis."""
    def gl8b():
        gl = ouvrir_pas(etat(), CADRE)
        plan = plan_nul()
        del plan["16"]
        jusqu_a(gl, "8b", plan)
        return gl

    g = gl8b()
    g.proposer(flux("16", -2.0))
    with pytest.raises(RefusDeProposition, match="supérieur à la perte"):
        g.declarer_montant_couvert("16", 3.0, "finances_publiques")
    g.declarer_montant_couvert("16", 1.5, "finances_publiques")
    g.clore_phase("8b")
    assert g.montant_execute_ligne("16") == -1.5

    g = gl8b()
    g.declarer_montant_couvert("16", 1.0, "finances_publiques")
    with pytest.raises(RefusDeProposition, match="non négative"):
        g.proposer(flux("16", 4.0))
    g.proposer(flux("16", -4.0))
    g.clore_phase("8b")
    assert g.montant_execute_ligne("16") == -1.0


def test_montant_couvert_execute_et_part_non_couverte():
    """Exécuté −c ; exécuté − proposé = u au bit ; M^G ≥ 0 exactement ; ΔE^CB = −u.

    10 000 tirages : perte Π et encaisse M^{G,8a} tirées, c = min(|Π| ; M^{G,8a}),
    cas saturé, partiel et nul compris. La forme « exécuté − proposé = u » est
    exacte au bit dans les trois cas, u = 0 compris ; « proposé − exécuté = −u »
    ne vaut qu'au signe de zéro près (ADR 0012, annotation du 07/10/2026, point 2).
    """
    rng = np.random.default_rng(20261008)
    sature = 0
    nuls = 0
    for k in range(10_000):
        m_g = float(rng.uniform(0.0, 2.0)) * 10.0 ** float(rng.integers(-3, 3))
        pi = -float(rng.uniform(0.0, 2.0)) * 10.0 ** float(rng.integers(-3, 3))
        if k == 0:
            pi = -m_g  # couverture exacte
        e = etat(M_G=m_g, B_H=200.0 + m_g)
        gl = ouvrir_pas(e, CADRE)
        plan = plan_nul()
        # Π est le résultat de la banque centrale : intérêts sur réserves versés
        # (ligne 12) sans recette, Π = −i_res Res / n_a < 0.
        plan["12"] = flux("12", -pi)
        del plan["16"]
        jusqu_a(gl, "8b", plan)
        m_g_8a = gl.position("M_G")
        c = min(-pi, max(0.0, m_g_8a))
        if k % 2:
            gl.declarer_montant_couvert("16", c, "finances_publiques")
            gl.proposer(flux("16", pi))
        else:
            gl.proposer(flux("16", pi))
            gl.declarer_montant_couvert("16", c, "finances_publiques")
        gl.clore_phase("8b")
        u = -pi - c
        assert gl.montant_execute_ligne("16") == -c
        assert empreinte(gl.montant_execute_ligne("16") - pi) == empreinte(u)
        nuls += u == 0.0
        assert gl.position("M_G") >= 0.0
        if c == m_g_8a:
            assert gl.position("M_G") == 0.0
            sature += 1
        gl.proposer(remboursement(gl))
        gl.clore_phase("8c")
        gl.clore_phase("9")
        v_cb = gl.valeur_nette_flux("banque_centrale") - getattr(
            e, cat.VALEUR_NETTE_FLUX["banque_centrale"])
        assert abs(v_cb - (-u)) <= EPS * gl.echelle("banque_centrale")
    assert sature > 1000
    assert nuls > 1000


def test_aucune_ligne_nouvelle_pour_la_part():
    """La part non couverte n'ajoute aucune ligne : la phase 8 (b) n'exécute que 16 et ses contreparties."""
    clotures, _ = derouler(ouvrir_pas(etat(), CADRE), plan_nul() | {"16": flux("16", -3.0)},
                           couvert=1.0)
    huit_b = next(c for c in clotures if c.phase == "8b")
    assert [identifiant for identifiant, _ in huit_b.montants] == ["16", "17", "20", "22"]
    assert len(cat.LIGNES) == 28


# --------------------------------------------------------------------------
# Critère 14 : découvert de réserves
# --------------------------------------------------------------------------


@pytest.mark.parametrize("source, derniere, montants", [
    ("phase 6", "6", {"11b": None, "7": None, "15": (5.0,)}),
    ("ligne 19a en phase 7", "7", {"19a-banque": (6.0,)}),
    ("ligne 13 en 8 (a)", "8a", {"13": (6.0,)}),
])
@pytest.mark.parametrize("couvert", [True, False])
def test_decouvert_intra_pas_des_reserves(source, derniere, montants, couvert):
    """Res < 0 admis à la clôture des phases 1 à 8 (b), banque seule ; à la clôture, défaut s'il reste."""
    e = etat(Res=1.0, D_H=600.0)
    plan = plan_nul()
    if source == "phase 6":
        # Les ménages paient l'impôt à l'État : D_H, Res et M^G bougent ensemble.
        plan["7"] = flux("7", 5.0, 0.0)
    else:
        for identifiant, valeurs in montants.items():
            plan[identifiant] = flux(identifiant, *valeurs)
    gl = ouvrir_pas(e, CADRE)
    jusqu_a(gl, derniere, plan)
    gl.clore_phase(derniere)
    assert gl.position("Res") < 0.0
    phases = cat.PHASES[cat.PHASES.index(derniere) + 1:]
    for phase in phases:
        for l in cat.LIGNES_DE_LA_PHASE[phase]:
            if l.identifiant in plan:
                gl.proposer(plan[l.identifiant])
        if phase == "8c":
            gl.proposer(remboursement(gl) if couvert else flux("21", 0.0))
        if phase == "9" and not couvert:
            with pytest.raises(DefautComptable) as erreur:
                gl.clore_phase(phase)
            assert erreur.value.regle == "eq:noyau-reserves-cloture"
            return
        gl.clore_phase(phase)
        if phase in ("8a", "8b"):
            assert gl.position("Res") < 0.0
    assert gl.clore_pas().variables["Res"] == 0.0


# --------------------------------------------------------------------------
# Critère 15 : une seule fonction de contrôle de signe ; aucune tolérance absolue
# --------------------------------------------------------------------------


def modules_du_noyau():
    return sorted(NOYAU.glob("*.py"))


def est_zero(noeud):
    if isinstance(noeud, ast.UnaryOp) and isinstance(noeud.op, (ast.USub, ast.UAdd)):
        noeud = noeud.operand
    return isinstance(noeud, ast.Constant) and type(noeud.value) in (int, float) and \
        noeud.value == 0


def comparaisons_de_signe(source):
    """(ligne, fonction englobante) de chaque comparaison d'ordre à zéro et de chaque min/max à 0."""
    arbre = ast.parse(source)
    trouvees = []

    def visiter(noeud, fonction):
        if isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fonction = noeud.name
        if isinstance(noeud, ast.Compare):
            operandes = [noeud.left] + noeud.comparators
            if any(isinstance(op, (ast.Lt, ast.LtE, ast.Gt, ast.GtE)) for op in noeud.ops) and \
                    any(est_zero(o) for o in operandes):
                trouvees.append((noeud.lineno, fonction))
        if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Name) and \
                noeud.func.id in ("min", "max") and any(est_zero(a) for a in noeud.args):
            trouvees.append((noeud.lineno, fonction))
        for enfant in ast.iter_child_nodes(noeud):
            visiter(enfant, fonction)

    visiter(arbre, None)
    return trouvees


def test_une_seule_fonction_de_controle_de_signe():
    """Point 8 : aucune comparaison de signe dans `src/nations/noyau/` hors de `controle_de_signe`."""
    hors = []
    dedans = 0
    for chemin in modules_du_noyau():
        for ligne, fonction in comparaisons_de_signe(chemin.read_text(encoding="utf-8")):
            if chemin.name == "identites.py" and fonction == "controle_de_signe":
                dedans += 1
            else:
                hors.append(f"{chemin.name}:{ligne} ({fonction})")
    assert hors == []
    assert dedans == 4  # un domaine par branche


def test_le_controle_textuel_detecte_une_comparaison_de_signe():
    assert comparaisons_de_signe("def f(x):\n    return x < 0.0\n") == [(2, "f")]
    assert comparaisons_de_signe("def f(x):\n    return 0 <= x\n") == [(2, "f")]
    assert comparaisons_de_signe("y = max(0.0, x)\n") == [(1, None)]
    assert comparaisons_de_signe("y = x < -0.0\n") == [(1, None)]
    assert comparaisons_de_signe("y = x == 0.0 or x < y\n") == []


def test_domaines_declares_par_regle():
    """Le domaine est une propriété déclarée de la règle : strict pour Res, relatif pour la caisse."""
    assert idt.RESERVES_CLOTURE.domaine is idt.Domaine.POSITIF_OU_NUL
    assert idt.CAISSE.domaine is idt.Domaine.POSITIF_OU_NUL_A_EPSILON_S
    assert idt.controle_de_signe(0.0, idt.RESERVES_CLOTURE, EPS, 10.0)
    assert not idt.controle_de_signe(-math.ulp(0.0), idt.RESERVES_CLOTURE, EPS, 10.0)
    assert idt.controle_de_signe(-0.5 * EPS * 10.0, idt.CAISSE, EPS, 10.0)
    assert not idt.controle_de_signe(-2 * EPS * 10.0, idt.CAISSE, EPS, 10.0)
    assert not idt.controle_de_signe(math.nan, idt.CAISSE, EPS, 10.0)
    with pytest.raises(ValueError):
        idt.controle_de_signe(1.0, idt.SOMME_LIGNE, EPS, 10.0)


def test_aucune_tolerance_absolue_dans_le_noyau():
    """Aucune constante flottante autre que 0 et 1, aucun `max(1, ·)` dans `src/nations/noyau/`."""
    ecarts = []
    for chemin in modules_du_noyau():
        source = chemin.read_text(encoding="utf-8")
        for noeud in ast.walk(ast.parse(source)):
            if isinstance(noeud, ast.Constant) and type(noeud.value) is float and \
                    noeud.value not in (0.0, 1.0):
                ecarts.append(f"{chemin.name}:{noeud.lineno} constante {noeud.value!r}")
            if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Name) and \
                    noeud.func.id in ("max", "min") and any(
                        isinstance(a, ast.Constant) and a.value == 1 for a in noeud.args):
                ecarts.append(f"{chemin.name}:{noeud.lineno} {noeud.func.id}(1, ·)")
            if isinstance(noeud, ast.Attribute) and noeud.attr in ("ulp", "float_info"):
                ecarts.append(f"{chemin.name}:{noeud.lineno} {noeud.attr}")
    assert ecarts == []


# --------------------------------------------------------------------------
# Critère 17 : état chargé ; interface sans affectation
# --------------------------------------------------------------------------


def echelle_a_zero(poste, secteur):
    """S du secteur quand le poste vaut 0 (l'écart à S d'une poussière est négligeable)."""
    return ouvrir_pas(etat(**{poste: 0.0}), CADRE).echelle(secteur)


@pytest.mark.parametrize("poste, secteur, facteur, regle", [
    ("Res", "banque", None, "eq:noyau-reserves-cloture"),
    ("Res", "banque", -0.5, "eq:noyau-reserves-cloture"),
    ("D_H", "menages", -2.0, "eq:noyau-caisse-nette"),
    ("D_F", "entreprises", -2.0, "eq:noyau-caisse-nette"),
    ("M_G", "etat", -2.0, "eq:noyau-caisse-nette"),
])
def test_etat_charge_controle_avant_la_phase_1(poste, secteur, facteur, regle):
    """Critère 17 : mêmes domaines à t = 0 et à la reprise, contrôlés à l'ouverture.

    Res : −1 ulp et −0,5 ε S sont des défauts (strict) ; caisse : −2 ε S_payeur.
    """
    x = -math.ulp(0.0) if facteur is None else facteur * EPS * echelle_a_zero(poste, secteur)
    with pytest.raises(DefautComptable) as erreur:
        ouvrir_pas(etat(t=7, **{poste: x}), CADRE)
    assert erreur.value.regle == regle and erreur.value.phase == "0" and erreur.value.t == 7
    assert erreur.value.secteur == secteur


@pytest.mark.parametrize("poste, secteur", [("D_H", "menages"), ("D_F", "entreprises"),
                                            ("M_G", "etat")])
def test_etat_charge_admis_a_la_frontiere_des_domaines(poste, secteur):
    """Res = 0 passe ; une caisse à −0,5 ε S_payeur passe et reste négative."""
    ouvrir_pas(etat(Res=0.0), CADRE)
    x = -0.5 * EPS * echelle_a_zero(poste, secteur)
    gl = ouvrir_pas(etat(**{poste: x}), CADRE)
    assert gl.position(poste) == x < 0.0


@pytest.mark.parametrize("valeur", [1, np.float64(1.0), math.nan, math.inf])
def test_etat_charge_non_flottant_refuse(valeur):
    p = dict(OUVERTURE)
    p["K"] = valeur
    e = EtatDouble(t=0, **p, **{cat.VALEUR_NETTE_FLUX[s]: 0.0 for s in cat.SECTEURS})
    with pytest.raises(RefusDeProposition, match="float fini"):
        ouvrir_pas(e, CADRE)


@pytest.mark.parametrize("cadre", [CadreDouble(0.0, EPS), CadreDouble(EPS, -EPS),
                                   CadreDouble(1, EPS), CadreDouble(math.nan, EPS),
                                   CadreDouble(math.inf, EPS), CadreDouble(EPS, math.inf)])
def test_tolerances_hors_domaine_refusees(cadre):
    with pytest.raises(RefusDeProposition, match="tolérance"):
        ouvrir_pas(etat(), cadre)


def test_aucun_poste_affecte_hors_d_une_ligne():
    """L'interface n'offre aucune affectation : attributs refusés, lectures en valeurs."""
    gl = ouvrir_pas(etat(), CADRE)
    with pytest.raises(RefusDeProposition, match="affectation"):
        gl._positions = {}
    with pytest.raises(RefusDeProposition, match="affectation"):
        gl.D_H = 0.0
    with pytest.raises(RefusDeProposition):
        del gl._positions
    publiques = {n for n in dir(gl) if not n.startswith("_")}
    assert publiques == {
        "proposer", "declarer_montant_couvert", "clore_phase", "clore_pas", "phase_courante",
        "montant_execute", "montant_execute_ligne", "position", "ouverture", "echelle",
        "valeur_nette_stock", "valeur_nette_flux",
    }
    assert type(gl.position("D_H")) is float
    # Les valeurs rendues sont immuables.
    _, fin = derouler(ouvrir_pas(etat(), CADRE), plan_nul())
    with pytest.raises(TypeError):
        fin.variables["D_H"] = 0.0
    with pytest.raises(dataclasses.FrozenInstanceError):
        fin.t = 3
    proposition = flux("1", 1.0)
    with pytest.raises(TypeError):
        proposition.montants["C"] = 2.0


def test_cloture_du_pas_rend_les_variables_d_etat_du_noyau():
    """Onze positions et cinq V^flux, au pas t + 1 ; l'état d'ouverture reste intact."""
    e = etat(t=4)
    copie = empreinte(e)
    _, fin = derouler(ouvrir_pas(e, CADRE), plan_aleatoire(np.random.default_rng(2)))
    assert fin.t == 5
    assert set(fin.variables) == set(CHAMPS)
    assert all(type(v) is float for v in fin.variables.values())
    assert empreinte(e) == copie


def test_diagnostics_sont_des_arrets_types():
    assert issubclass(RefusDeProposition, ArretNoyau)
    assert issubclass(DefautComptable, ArretNoyau)
    assert not issubclass(RefusDeProposition, DefautComptable)


# --------------------------------------------------------------------------
# Reprise de l'audit (C1 à C7) et décisions du 07/10/2026 (ADR 0012, annotation
# du 07/10/2026, questions de `coder`)
# --------------------------------------------------------------------------


def test_porte_monnaie_ligne_par_ligne_a_l_echelle_alpha(monkeypatch):
    """C1, C2 : porte ΔM de la ligne 1 faussée, relevée en phase 5 à min(S_H, S_F).

    La ligne 1 lie ménages et entreprises, dont aucun n'a le plus petit S
    global (S^CB) : l'échelle (α) de la ligne n'est pas le minimum global.
    """
    faussee = dataclasses.replace(cat.LIGNE["1"], signature=(1, 0))
    phase5 = tuple(faussee if l.identifiant == "1" else l for l in cat.LIGNES_DE_LA_PHASE["5"])
    monkeypatch.setitem(gl_module.LIGNES_DE_LA_PHASE, "5", phase5)
    gl = ouvrir_pas(etat(), CADRE)
    echelle_ligne = min(gl.echelle("menages"), gl.echelle("entreprises"))
    assert echelle_ligne > min(gl.echelle(s) for s in cat.SECTEURS)
    plan = plan_nul()
    plan["1"] = flux("1", 1.0)
    with pytest.raises(DefautComptable) as erreur:
        derouler(gl, plan)
    assert erreur.value.regle == "eq:noyau-variation-monnaie"
    assert (erreur.value.ligne, erreur.value.phase) == ("1", "5")
    assert erreur.value.echelle == echelle_ligne


@pytest.mark.parametrize("facteur, defaut", [(0.5, False), (2.0, True)])
@pytest.mark.parametrize("ligne, terme, phase, regle, secteur", [
    ("18", "Delta_L", "3", "eq:noyau-variation-monnaie", "banque"),
    ("21", "Delta_LCB", "8c", "eq:noyau-variation-monnaie-centrale", "banque_centrale"),
])
def test_portes_du_pas_a_l_echelle_du_bilan(ligne, terme, phase, regle, secteur, facteur, defaut):
    """C1 : ΔM du pas à ε S^Bk, ΔH du pas à ε S^CB, jamais à ε Σ S.

    Un montant exécuté corrompu après la clôture de sa phase (attribut privé :
    simulation, l'interface ne le permet pas) laisse les portes ligne par
    ligne intactes ; seul le contrôle du pas, en phase 9, le voit. Un écart
    de 2 ε S_secteur, sous ε Σ_s S_s, est relevé ; 0,5 ε S_secteur passe.
    """
    gl = ouvrir_pas(etat(), CADRE)
    s = gl.echelle(secteur)
    assert 2 * s < sum(gl.echelle(x) for x in cat.SECTEURS)
    plan = plan_nul()
    plan["18"] = flux("18", 3.0)
    jusqu_a(gl, phase, plan)
    gl.clore_phase(phase)
    gl._executes[ligne][terme] += facteur * EPS * s
    for suivante in cat.PHASES[cat.PHASES.index(phase) + 1:]:
        for l in cat.LIGNES_DE_LA_PHASE[suivante]:
            if l.identifiant in plan:
                gl.proposer(plan[l.identifiant])
        if suivante == "8c":
            gl.proposer(remboursement(gl))
        if suivante == "9" and defaut:
            with pytest.raises(DefautComptable) as erreur:
                gl.clore_phase("9")
            assert erreur.value.regle == regle
            assert (erreur.value.phase, erreur.value.secteur) == ("9", secteur)
            assert erreur.value.echelle == s
            return
        gl.clore_phase(suivante)


@pytest.mark.parametrize("ligne, poste, regle, contrepartie", [
    ("18", "D_H", "eq:noyau-variation-monnaie", "17"),
    ("19a-banque", "Res", "eq:noyau-variation-monnaie-centrale", "20"),
])
def test_portes_des_contreparties_de_reglement(monkeypatch, ligne, poste, regle, contrepartie):
    """C5 : les portes s'évaluent aussi pour 17, 20 et 22.

    Le double du catalogue fait varier un moyen de paiement hors du règlement
    (variation d'instrument fautive) : ni la ligne, ni les colonnes, ni la
    clôture des postes ne le voient ; la porte de la contrepartie le relève
    dans la phase même.
    """
    origine = cat.LIGNE[ligne]
    terme = dataclasses.replace(origine.termes[0],
                                variations=origine.termes[0].variations + ((poste, 1.0),))
    faussee = dataclasses.replace(origine, termes=(terme,))
    phase = origine.phase
    lignes = tuple(faussee if l.identifiant == ligne else l
                   for l in cat.LIGNES_DE_LA_PHASE[phase])
    monkeypatch.setitem(gl_module.LIGNES_DE_LA_PHASE, phase, lignes)
    plan = plan_nul()
    plan[ligne] = flux(ligne, 2.0)
    with pytest.raises(DefautComptable) as erreur:
        derouler(ouvrir_pas(etat(), CADRE), plan)
    assert erreur.value.regle == regle
    assert (erreur.value.ligne, erreur.value.phase) == (contrepartie, phase)


def test_portes_des_contreparties_dans_les_rapports():
    """Les familles des portes comptent les lignes décidées et les trois contreparties."""
    rng = np.random.default_rng(41)
    clotures, _ = derouler(ouvrir_pas(etat(), CADRE), plan_aleatoire(rng, echelle=3.0))
    for c in clotures:
        if c.montants:
            assert [i for i, _ in c.montants][-3:] == ["17", "20", "22"]
            rapports = {r[0]: r[2] for r in c.rapports}
            assert rapports["eq:noyau-variation-monnaie"] <= EPS
            assert rapports["eq:noyau-variation-monnaie-centrale"] <= EPS


@pytest.mark.parametrize("positions, v_flux", [
    (dict(D_H=1e308, D_F=5e307, L=1e308), None),
    (dict(D_H=1.7e308, D_F=1.7e308), {cat.VALEUR_NETTE_FLUX["banque"]: 0.0,
                                      cat.VALEUR_NETTE_FLUX["menages"]: 0.0}),
])
def test_echelle_infinie_est_un_defaut(positions, v_flux):
    """C3 : S finie exigée à l'ouverture, en plus de S > 0 (cas adverse de l'audit en tête)."""
    e = etat(v_flux=v_flux, **positions)
    with pytest.raises(DefautComptable) as erreur:
        ouvrir_pas(e, CADRE)
    assert erreur.value.regle == "eq:noyau-echelle-bilan" and erreur.value.phase == "0"
    assert math.isinf(erreur.value.echelle)


def test_montant_couvert_au_plus_la_perte_exact():
    """C4 : c ≤ |Π| par `controle_de_signe` (|Π| − c ≥ 0, strict), exact au flottant près.

    10^5 couples tirés sur 600 ordres de grandeur, sous-normaux compris, et
    leurs voisins immédiats : le contrôle de signe donne exactement `c <= |Π|`.
    """
    rng = np.random.default_rng(20261012)
    regle = idt.MONTANT_COUVERT_AU_PLUS_LA_PERTE
    assert regle.domaine is idt.Domaine.POSITIF_OU_NUL
    ecarts = 0
    for _ in range(100_000):
        perte = float(rng.uniform(0.5, 1.0)) * 2.0 ** float(rng.integers(-1074, 1000))
        for c in (perte, math.nextafter(perte, math.inf), math.nextafter(perte, 0.0),
                  float(rng.uniform(0.0, 2.0)) * perte):
            ecarts += idt.controle_de_signe(perte - c, regle, EPS, 0.0) != (c <= perte)
    assert ecarts == 0
    # Dans le grand livre : c = |Π| admis, son successeur refusé.
    for c, admis in ((0.75, True), (math.nextafter(0.75, math.inf), False)):
        gl = ouvrir_pas(etat(), CADRE)
        plan = plan_nul()
        del plan["16"]
        jusqu_a(gl, "8b", plan)
        gl.proposer(flux("16", -0.75))
        if admis:
            gl.declarer_montant_couvert("16", c, "finances_publiques")
        else:
            with pytest.raises(RefusDeProposition, match="supérieur à la perte") as refus:
                gl.declarer_montant_couvert("16", c, "finances_publiques")
            assert refus.value.regle == regle.nom


def test_grand_livre_construit_par_ouvrir_pas_seul():
    """C7 : la classe refuse l'appel direct ; t est un entier."""
    with pytest.raises(RefusDeProposition, match="ouvrir_pas"):
        gl_module.GrandLivre()
    with pytest.raises(RefusDeProposition, match="ouvrir_pas"):
        gl_module.GrandLivre(0, EPS, EPS, dict(OUVERTURE), {}, {})


@pytest.mark.parametrize("t", ["sept", 7.0, True, np.int64(7), None])
def test_pas_non_entier_refuse(t):
    """C7 : `type(t) is int` (un booléen ou un entier NumPy est refusé)."""
    e = dataclasses.replace(etat(), t=t)
    with pytest.raises(RefusDeProposition, match="entier attendu"):
        ouvrir_pas(e, CADRE)


@pytest.mark.parametrize("montants", [(-0.5, 0.0), (-0.5, -0.25), (-0.5, 0.25)])
def test_ligne_7_negative_executee(montants):
    """Ligne 7 admise négative, par ligne (T^cou de signe quelconque) : portes (−, −) signées."""
    e = etat()
    gl = ouvrir_pas(e, CADRE)
    plan = plan_nul()
    plan["7"] = flux("7", *montants)
    # Plan nul ailleurs : les positions avant la phase 6 sont celles d'ouverture.
    jusqu_a(gl, "6", plan)
    gl.clore_phase("6")
    montant = montants[0] + montants[1]
    assert gl.montant_execute_ligne("7") == montant
    sgn_m, sgn_h = cat.LIGNE["7"].signature
    assert (sgn_m, sgn_h) == (-1, -1)
    delta_d = (gl.position("D_H") - e.D_H) + (gl.position("D_F") - e.D_F)
    assert abs(delta_d - sgn_m * montant) <= EPS * gl.echelle("banque")
    assert gl.position("Res") - e.Res == sgn_h * montant
    assert gl.montant_execute("7", "menages") == -montants[0]


LIGNES_QUI_REFUSENT_UN_NEGATIF = [
    l.identifiant for l in cat.LIGNES if l.proposant is not None and not l.admet_negatif]


@pytest.mark.parametrize("identifiant", LIGNES_QUI_REFUSENT_UN_NEGATIF)
def test_ligne_qui_refuse_un_negatif(identifiant):
    """Sens admis par ligne : toute ligne hors de la liste fermée refuse −1 ulp, admet −0,0."""
    ligne = cat.LIGNE[identifiant]
    gl = ouvrir_pas(etat(), CADRE)
    plan = plan_nul()
    del plan[identifiant]
    jusqu_a(gl, ligne.phase, plan)
    with pytest.raises(RefusDeProposition, match="ne l'admet pas") as refus:
        gl.proposer(flux(identifiant, *([-math.ulp(0.0)] * len(ligne.termes))))
    assert refus.value.ligne == identifiant
    gl.proposer(flux(identifiant, *([-0.0] * len(ligne.termes))))


def test_montant_couvert_obligatoire_si_perte():
    """Ligne 16 strictement négative sans déclaration : refus à la clôture de 8 (b).

    Cas de `macro` : |Π| = M^{G,8a} + 0,5 ε S_G, que le contrôle de caisse
    laisserait passer en silence. Π = −0,0 et Π = 0 n'y obligent pas ;
    c = 0 reste admis.
    """
    gl = ouvrir_pas(etat(), CADRE)
    plan = plan_nul()
    del plan["16"]
    jusqu_a(gl, "8b", plan)
    perte = -(gl.position("M_G") + 0.5 * EPS * gl.echelle("etat"))
    gl.proposer(flux("16", perte))
    with pytest.raises(RefusDeProposition, match="sans déclaration du montant couvert") as refus:
        gl.clore_phase("8b")
    assert (refus.value.ligne, refus.value.phase, refus.value.regle) == (
        "16", "8b", "ligne 16 négative")
    with pytest.raises(RefusDeProposition, match="arrêté"):
        gl.clore_pas()
    for montant in (-0.0, 0.0):
        gl = ouvrir_pas(etat(), CADRE)
        derouler(gl, plan | {"16": flux("16", montant)}, couvert=None)
        assert gl.montant_execute_ligne("16") == 0.0
    gl = ouvrir_pas(etat(M_G=0.0), CADRE)
    _, fin = derouler(gl, plan | {"16": flux("16", -2.0)}, couvert=0.0)
    assert gl.montant_execute_ligne("16") == 0.0
    # Exécuté − proposé = u = |Π| − c, au bit.
    assert empreinte(gl.montant_execute_ligne("16") - -2.0) == empreinte(2.0 - 0.0)
    assert fin.variables["M_G"] >= 0.0


def perte_au_socle(e, i_cb, n_a=12.0):
    """Lignes 11c et 13 du socle sous un taux directeur négatif ; Π = 11c + 13 − 12, ligne 12 nulle."""
    l11c = i_cb * e.B_CB / n_a
    l13 = i_cb * e.L_CB / n_a
    l12 = 0.0
    return l11c, l13, l12, l11c + l13 - l12


@pytest.mark.parametrize("b_cb", [0.0, 100.0])
def test_montant_couvert_au_socle_lignes_11c_et_13_negatives(b_cb):
    """Cas du socle (`monnaie`) : Res = 0, perte par les lignes 13 (et 11c) négatives.

    Exécuté − proposé = u exactement au bit ; ΔV^CB + u à ε S^CB près (Π est
    une somme de trois termes, la propriété ne tient pas au bit). B_CB = 0
    est la position du socle (11c vaut alors −0,0) ; B_CB > 0 exerce 11c < 0.
    """
    rng = np.random.default_rng(20261007)
    partielles = 0
    for _ in range(500):
        i_cb = -float(rng.uniform(0.001, 0.05))
        m_g = float(rng.uniform(0.0, 3.0)) * 10.0 ** float(rng.integers(-2, 2))
        e = etat(Res=0.0, B_CB=b_cb, L_CB=150.0, M_G=m_g, B_H=200.0 + m_g)
        l11c, l13, l12, perte = perte_au_socle(e, i_cb)
        gl = ouvrir_pas(e, CADRE)
        plan = plan_nul()
        plan["11c"] = flux("11c", l11c)
        plan["13"] = flux("13", l13)
        plan["12"] = flux("12", l12)
        del plan["16"]
        jusqu_a(gl, "8b", plan)
        c = montant_couvert_de_l_etat(gl, perte)
        u = -perte - c
        partielles += u > 0.0
        gl.proposer(flux("16", perte))
        gl.declarer_montant_couvert("16", c, "finances_publiques")
        gl.clore_phase("8b")
        assert empreinte(gl.montant_execute_ligne("16") - perte) == empreinte(u)
        gl.proposer(remboursement(gl))
        gl.clore_phase("8c")
        gl.clore_phase("9")
        nom = cat.VALEUR_NETTE_FLUX["banque_centrale"]
        delta_v = gl.valeur_nette_flux("banque_centrale") - getattr(e, nom)
        assert abs(delta_v + u) <= EPS * gl.echelle("banque_centrale")
    assert partielles > 50


def lignes_19b_proposees(monkeypatch):
    """Double du catalogue dans le test (ADR 0012, annotation du 07/10/2026, point 3).

    Les deux lignes 19b reçoivent `banque_centrale` pour proposant, dans
    l'espace de noms de `grand_livre` seulement ; `catalogue.py` est intact.
    """
    doubles = {i: dataclasses.replace(cat.LIGNE[i], proposant="banque_centrale")
               for i in ("19b-ménages", "19b-banque")}
    # Objets neufs dans l'espace de noms de `grand_livre` : `cat.LIGNE` et
    # `cat.LIGNES_DE_LA_PHASE` ne sont pas mutés.
    phase7 = tuple(doubles.get(l.identifiant, l) for l in cat.LIGNES_DE_LA_PHASE["7"])
    lignes_de_la_phase = {**cat.LIGNES_DE_LA_PHASE, "7": phase7}
    monkeypatch.setattr(gl_module, "LIGNE", {**cat.LIGNE, **doubles})
    monkeypatch.setattr(gl_module, "LIGNES", tuple(doubles.get(l.identifiant, l)
                                                   for l in cat.LIGNES))
    monkeypatch.setattr(gl_module, "LIGNES_DE_LA_PHASE", lignes_de_la_phase)
    assert cat.LIGNE["19b-ménages"].proposant is None
    return lignes_de_la_phase


@pytest.mark.parametrize("menages, banque", [(5.0, 7.0), (-3.0, -4.0)])
def test_lignes_19b_a_l_execution(monkeypatch, menages, banque):
    """19b sous un double du catalogue : deux signes, portes, identité de B_CB, découvert en 8 (c).

    ΔM = ΔD_H = 19b-ménages ; ΔH = ΔRes = les deux lignes ;
    ΔB_CB = ΔB_CB^prim + ΔB_H^sec + ΔB_Bk^sec. Une vente rend les réserves
    négatives en phase 7, couvertes par le refinancement de la phase 8 (c).
    """
    lignes = lignes_19b_proposees(monkeypatch)
    e = etat(Res=1.0)
    gl = ouvrir_pas(e, CADRE)
    plan = plan_nul()
    plan["19a-BC"] = flux("19a-BC", 2.0)
    plan["19b-ménages"] = flux("19b-ménages", menages, proposant="banque_centrale")
    plan["19b-banque"] = flux("19b-banque", banque, proposant="banque_centrale")
    clotures, fin = derouler(gl, plan, lignes=lignes)
    sept = next(c for c in clotures if c.phase == "7")
    assert [i for i, _ in sept.montants] == [
        "19a-ménages", "19a-banque", "19a-BC", "19b-ménages", "19b-banque", "17", "20", "22"]
    assert gl.montant_execute_ligne("19b-ménages") == menages
    assert gl.montant_execute_ligne("19b-banque") == banque
    assert gl.position("D_H") - e.D_H == menages
    assert fin.variables["B_CB"] - e.B_CB == 2.0 + menages + banque
    assert fin.variables["B_H"] - e.B_H == -menages
    assert fin.variables["B_Bk"] - e.B_Bk == -banque
    assert gl.montant_execute_ligne("20") == fin.variables["Res"] - e.Res
    assert fin.variables["Res"] >= 0.0 and fin.variables["Res"] * fin.variables["L_CB"] == 0.0
    if menages < 0.0:
        assert e.Res + menages + banque < 0.0  # découvert de la phase 7
        assert gl.montant_execute_ligne("21") > 0.0  # couvert en 8 (c)


def test_vente_19b_aux_menages_au_dela_des_depots(monkeypatch):
    """Une vente aux ménages au-delà de D_H : défaut de caisse nommant 19b-ménages."""
    lignes = lignes_19b_proposees(monkeypatch)
    gl = ouvrir_pas(etat(D_H=1.0), CADRE)
    plan = plan_nul()
    plan["19b-ménages"] = flux("19b-ménages", -2.0, proposant="banque_centrale")
    plan["19b-banque"] = flux("19b-banque", 0.0, proposant="banque_centrale")
    with pytest.raises(DefautComptable) as erreur:
        derouler(gl, plan, lignes=lignes)
    assert erreur.value.regle == "eq:noyau-caisse-nette"
    assert (erreur.value.phase, erreur.value.moyen) == ("7", "D_H")
    assert erreur.value.lignes_debitrices == ("19b-ménages",)


def test_prédicat_de_cloture_sans_ligne_structurel():
    """C6 : le prédicat est « aucune ligne du catalogue dans la phase », non une liste écrite."""
    for phase in cat.PHASES:
        assert gl_module._sans_ligne(phase) == (len(cat.LIGNES_DE_LA_PHASE[phase]) == 0)
    # Constat au socle (non écrit dans `src/`) : les phases 1, 2 et 9 n'ont pas de ligne.
    assert [p for p in cat.PHASES if gl_module._sans_ligne(p)] == ["1", "2", "9"]


@pytest.mark.parametrize("graine", [12, 13, 14])
def test_cloture_sans_ligne_egale_au_calcul_complet(monkeypatch, graine):
    """C6 : la clôture sautée est égale, au bit, à celle du calcul complet.

    Le calcul complet s'obtient en neutralisant le prédicat ; la phase 9
    garde dans les deux cas sa couche noyau. Le rapport de clôture des postes
    en phase 9, repris de la phase 8 (c), n'est pas nul : le test le compare
    vraiment.
    """
    def pas(plan):
        return derouler(ouvrir_pas(etat(), CADRE), plan)

    rng = np.random.default_rng(graine)
    plans = [plan_aleatoire(rng, echelle=50.0) for _ in range(4)]
    sautes = [pas(p) for p in plans]
    monkeypatch.setattr(gl_module, "_sans_ligne", lambda phase: False)
    complets = [pas(p) for p in plans]
    assert empreinte(sautes) == empreinte(complets)
    rapports_9 = [{r[0]: r[2] for r in clotures[-1].rapports} for clotures, _ in sautes]
    assert any(r["eq:noyau-cloture-poste"] > 0.0 for r in rapports_9)
    for clotures, _ in sautes:
        assert {r[0] for r in clotures[-1].rapports} >= {
            "eq:noyau-tolerance-cumulee", "eq:noyau-variation-monnaie",
            "eq:noyau-variation-monnaie-centrale"}


# --------------------------------------------------------------------------
# Réserves M1 à M4 de l'audit de #95
# --------------------------------------------------------------------------


def v_flux_decalee(e, facteur, cadre=CADRE, secteurs=cat.SECTEURS):
    """V^flux de l'état e, décalée de facteur × S de chaque secteur nommé (S lue à l'ouverture)."""
    gl = ouvrir_pas(e, cadre)
    return {cat.VALEUR_NETTE_FLUX[s]: getattr(e, cat.VALEUR_NETTE_FLUX[s]) + facteur * gl.echelle(s)
            for s in secteurs}


def test_v_flux_suivante_au_bit_quand_v_flux_differe_de_v_stock():
    """M1 : V^flux_{t+1} = V^flux_t + résultat du pas, au bit, sur trois pas.

    V^flux est décalée une fois, à t = 0, de 0,5 ε S dans chaque secteur : le
    décalage est conservé (V^flux ≠ V^stock à chaque clôture), et V^flux_{t+1}
    se déduit de V^flux_t, jamais de V^stock. Le résultat est recomposé par
    les lectures publiques, dans l'ordre du catalogue.
    """
    rng = np.random.default_rng(20261009)
    e = etat(v_flux=v_flux_decalee(etat(), 0.5 * EPS))
    for _ in range(3):
        gl = ouvrir_pas(e, CADRE)
        _, fin = derouler(gl, plan_aleatoire(rng, echelle=3.0))
        for s in cat.SECTEURS:
            nom = cat.VALEUR_NETTE_FLUX[s]
            resultat = 0.0
            for ligne in cat.LIGNES:
                if ligne.resultat:
                    resultat += gl.montant_execute(ligne.identifiant, cat.COLONNE_DE_RESULTAT[s])
            attendu = getattr(e, nom) + resultat
            assert empreinte(fin.variables[nom]) == empreinte(attendu)
            assert empreinte(gl.valeur_nette_flux(s)) == empreinte(attendu)
            ecart = gl.valeur_nette_stock(s) - fin.variables[nom]
            assert 0.25 * EPS * gl.echelle(s) < abs(ecart) <= EPS * gl.echelle(s)
        e = etat_suivant(fin)


@pytest.mark.parametrize("facteur, defaut", [(0.6, True), (0.4, False)])
def test_identite_cumulee_accumule_les_decalages_d_un_pas_a_l_autre(facteur, defaut):
    """M1 : un décalage de f ε S injecté à chaque pas s'accumule dans V^flux.

    Plan nul et L^CB = 0 : aucune position ne bouge, S est la même aux deux
    pas. À t = 0 l'écart vaut f ε S, à t = 1 il vaut 2 f ε S : 0,6 tombe à
    t = 1 (1,2 ε S), 0,4 passe (0,8 ε S). Si V^flux_{t+1} était tirée de
    V^stock, l'écart repartirait de zéro à chaque pas et 0,6 passerait.
    """
    e = etat(L_CB=0.0)
    s_banque = ouvrir_pas(e, CADRE).echelle("banque")
    for t in range(2):
        assert ouvrir_pas(e, CADRE).echelle("banque") == s_banque
        e = dataclasses.replace(e, **v_flux_decalee(e, facteur * EPS, secteurs=("banque",)))
        assert e.t == t
        if t == 1 and defaut:
            with pytest.raises(DefautComptable) as erreur:
                derouler(ouvrir_pas(e, CADRE), plan_nul())
            assert erreur.value.regle == "eq:noyau-tolerance-cumulee"
            assert (erreur.value.t, erreur.value.phase, erreur.value.secteur) == (1, "9", "banque")
            return
        _, fin = derouler(ouvrir_pas(e, CADRE), plan_nul())
        e = etat_suivant(fin)
    assert e.t == 2


@pytest.mark.parametrize("eps, eps_v, defaut", [(1e-12, 1e-6, False), (1e-6, 1e-12, True)])
def test_identite_cumulee_a_eps_v_distincte_de_eps(eps, eps_v, defaut):
    """M2 : l'identité cumulée se contrôle à ε_V, jamais à ε.

    Écart de V^flux de 2 × 10⁻¹² × S^Bk : il passe sous ε_V = 10⁻⁶ même si
    ε = 10⁻¹², et il est un défaut sous ε_V = 10⁻¹² même si ε = 10⁻⁶.
    """
    cadre = CadreDouble(eps, eps_v)
    e = etat(v_flux=v_flux_decalee(etat(), 2e-12, cadre=cadre, secteurs=("banque",)))
    gl = ouvrir_pas(e, cadre)
    if defaut:
        with pytest.raises(DefautComptable) as erreur:
            derouler(gl, plan_nul())
        assert erreur.value.regle == "eq:noyau-tolerance-cumulee"
        assert erreur.value.secteur == "banque" and erreur.value.tolerance == eps_v
        return
    clotures, _ = derouler(gl, plan_nul())
    rapports = {(r[0], r[1]): r[2] for r in clotures[-1].rapports}
    # Le rapport dépasse ε : seul ε_V le laisse passer.
    assert eps < rapports[("eq:noyau-tolerance-cumulee", "banque")] <= eps_v


def test_echelle_alpha_exclut_le_secteur_d_un_terme_nul(monkeypatch):
    """M4 : un terme nul ne fait pas entrer son secteur dans l'échelle (α) de la ligne.

    Double du catalogue : le terme T_F de la ligne 7 est versé par la banque
    centrale (plus petit S) au lieu des entreprises, et proposé nul ; la
    signature de la ligne est faussée pour que la porte ΔM la relève. L'échelle
    du diagnostic est min(S_H, S_G), sans S^CB.
    """
    origine = cat.LIGNE["7"]
    t_h, t_f = origine.termes
    t_f_bc = dataclasses.replace(
        t_f, colonne_moins="banque_centrale",
        reglement=cat.chemin_de_reglement("banque_centrale", "etat"))
    faussee = dataclasses.replace(origine, termes=(t_h, t_f_bc), signature=(0, -1))
    phase6 = tuple(faussee if l.identifiant == "7" else l for l in cat.LIGNES_DE_LA_PHASE["6"])
    monkeypatch.setitem(gl_module.LIGNES_DE_LA_PHASE, "6", phase6)
    gl = ouvrir_pas(etat(), CADRE)
    s_cb = gl.echelle("banque_centrale")
    echelle_ligne = min(gl.echelle("menages"), gl.echelle("etat"))
    assert s_cb == min(gl.echelle(s) for s in cat.SECTEURS) and s_cb < echelle_ligne
    plan = plan_nul()
    plan["7"] = flux("7", 1.0, 0.0)
    with pytest.raises(DefautComptable) as erreur:
        derouler(gl, plan)
    assert erreur.value.regle == "eq:noyau-variation-monnaie"
    assert (erreur.value.ligne, erreur.value.phase) == ("7", "6")
    assert erreur.value.echelle == echelle_ligne
    # Même propriété sur la fonction isolée : cellule nulle de la BC ignorée.
    echelles = {s: gl.echelle(s) for s in cat.SECTEURS}
    cellules = {"menages": -1.0, "etat": 1.0, "banque_centrale": 0.0}
    assert gl_module._echelle_de_ligne(cellules, echelles) == echelle_ligne
    assert gl_module._echelle_de_ligne({"banque_centrale": -0.0, "etat": 0.0}, echelles) == 0.0
