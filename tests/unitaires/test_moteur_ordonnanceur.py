"""Moteur : déclaration des phases, assemblage, triangularité, déroulement d'un pas (issue #97).

Contrat : ADR 0012, B1 à B5, C1 à C3, E1 ; ADR 0009 (tests (1) à (4)) ;
ADR 0011 (sous-phase 8 (b)) ; critères de #97 et leurs compléments du rang 1b
(C97-1, C97-2, C97-4). Aucun bloc réel n'existe : des **blocs d'essai**
minimaux, définis ici, siègent sous les huit radicaux, proposent toutes les
lignes à proposant du catalogue avec des montants tirés d'avance à graine
explicite, et écrivent quelques variables du pas pour exercer les lectures.
Le générateur complet est celui de #98.
"""

import dataclasses
import itertools
import re
import struct
from pathlib import Path

import numpy as np
import pytest

from nations.etat import schema
from nations.etat.sauvegarde import sauvegarder
from nations.etat.schema import EtatPays, Invariance, VariableEtat
from nations.moteur import ordonnanceur as ordo
from nations.moteur.contrat_bloc import (
    GRAND_LIVRE,
    OUVERTURE,
    REGISTRE,
    DeclarationDeBloc,
    Lecture,
    Siege,
    methode_de_l_etape,
)
from nations.moteur.conversions import facteur_par_pas
from nations.moteur.diagnostics import DefautDeDeclaration, RefusDuMoteur
from nations.moteur.ordonnanceur import (
    INDICE_DES_PRIX,
    DeclarationDesEntrees,
    EntreesDuTour,
    assembler,
    executer_pas,
)
from nations.moteur.parametres import TauxDeCroissance
from nations.moteur.parametres.cadre import CADRE, PAS_PAR_AN
from nations.moteur.phases import (
    ETAPES,
    LIBELLES,
    MOTEUR,
    NOYAU,
    PHASES,
    RADICAUX_DES_BLOCS,
)
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas, ObservateurNul

SPECIFICATION = (Path(__file__).resolve().parents[2] / "docs" / "specification"
                 / "nations_et_marches.tex")
N_A = PAS_PAR_AN.valeur
GRAINE = 20261007

POSITIONS = {"D_H": 600.0, "D_F": 400.0, "L": 500.0, "B_H": 200.0, "B_Bk": 300.0,
             "B_CB": 100.0, "Res": 50.0, "L_CB": 20.0, "M_G": 150.0, "K": 900.0, "IN": 100.0}

SANS_ENTREES = DeclarationDesEntrees((), ())
ENTREES_VIDES = EntreesDuTour((), ())


def bits(x):
    return struct.pack("<d", x).hex()


def registre_stationnaire(pi_barre):
    """P_{t−u} = P_{t−1} (1 + π̄)^{−(u−1)/n_a}, u = 1 … 13, P_{t−1} = 1."""
    return tuple((1.0 + pi_barre) ** (-(u - 1) / N_A) for u in range(1, N_A + 2))


def etat_initial(pi_barre=0.02, positions=POSITIONS):
    v = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(positions, s) for s in cat.SECTEURS}
    return EtatPays(identifiant="A", graine=GRAINE, t=0,
                    registre_prix=registre_stationnaire(pi_barre), **positions, **v)


# --------------------------------------------------------------------------
# Blocs d'essai
# --------------------------------------------------------------------------


def siege(etape, ecrit=(), lit=(), propose=(), couvre=(), etat=()):
    return Siege(etape, tuple(ecrit), tuple(lit), tuple(propose), tuple(couvre), tuple(etat))


def _methode(action):
    """Méthode de phase d'un bloc d'essai : appelle `action(vue)`."""
    def methode(self, vue):
        action(vue)
    return methode


def fabriquer(radical, sieges, actions, bases=(), slots=()):
    """Bloc d'essai : une classe sans attribut d'instance (`__slots__` vide, sauf essai), la
    déclaration en attribut de classe, une méthode par étape, aucun état.

    `slots=None` : classe sans `__slots__` (instance à `__dict__`)."""
    espace = {"declaration": DeclarationDeBloc(radical, tuple(sieges))}
    if slots is not None:
        espace["__slots__"] = slots
    for etape, action in actions.items():
        espace[methode_de_l_etape(etape)] = _methode(action)
    return type(f"Bloc_{radical}", tuple(bases), espace)()


def etapes_du(radical):
    return [e.identifiant for e in ETAPES if any(radical in g for g in e.groupes)]


def lignes_de(radical, etape):
    return tuple(ligne.identifiant for ligne in cat.LIGNES_DE_LA_PHASE[etape]
                 if ligne.proposant == radical)


def tirer_plans(nb_pas, amplitude=0.4, graine=GRAINE):
    """Montants des lignes proposées, par pas, tirés d'avance à graine explicite."""
    rng = np.random.default_rng(graine)
    plans = {}
    for t in range(nb_pas):
        plan = {}
        for ligne in cat.LIGNES:
            if ligne.proposant is None or ligne.identifiant == "21":
                continue
            bas = -amplitude if ligne.admet_negatif and ligne.identifiant != "7" else 0.0
            plan[ligne.identifiant] = {te.nom: float(rng.uniform(bas, amplitude))
                                       for te in ligne.termes}
        plans[t] = plan
    return plans


def plans_nuls(nb_pas):
    return {t: {ligne.identifiant: {te.nom: 0.0 for te in ligne.termes} for ligne in cat.LIGNES
                if ligne.proposant is not None and ligne.identifiant != "21"}
            for t in range(nb_pas)}


# Variables du pas des blocs d'essai : (radical, étape) → (écritures, lectures).
ECRITURES_ET_LECTURES = {
    ("banque_centrale", "1"): (("i_CB",), ()),
    ("travail", "1"): (("W",), ()),
    ("travail", "4"): (("N",), (Lecture("1", "W"),)),
    ("production", "4"): (("y",), (Lecture("4", "N"),)),
    ("production", "5"): ((), (Lecture("4", "y"), Lecture("5", INDICE_DES_PRIX))),
    ("prix", "5"): ((INDICE_DES_PRIX,), (Lecture(REGISTRE, "dernier_prix"),)),
    ("finances_publiques", "7"): ((), (Lecture("1", "i_CB"), Lecture(GRAND_LIVRE, "6"))),
    ("finances_publiques", "8b"): ((), (Lecture(GRAND_LIVRE, "M_G"),)),
    ("banque", "8c"): ((), (Lecture(GRAND_LIVRE, "Res"), Lecture(GRAND_LIVRE, "L_CB"),
                            Lecture(GRAND_LIVRE, "16"))),
    ("menages", "2"): ((), (Lecture("0", "mois"), Lecture(OUVERTURE, "t"))),
    ("menages", "9"): ((), (Lecture(GRAND_LIVRE, "17"), Lecture(GRAND_LIVRE, "5"))),
    ("investissement", "9"): ((), (Lecture(GRAND_LIVRE, "22"),)),
}


def action_d_essai(radical, etape, plans, pi_barre):
    """Ce que fait le bloc d'essai dans l'étape : ses lignes, ses écritures, ses lectures."""
    lignes = lignes_de(radical, etape) if etape in cat.LIGNES_DE_LA_PHASE else ()
    ecritures, lectures = ECRITURES_ET_LECTURES.get((radical, etape), ((), ()))
    facteur = facteur_par_pas(TauxDeCroissance(pi_barre))

    def agir(vue):
        plan = plans[vue.ouverture.t]
        for lecture in lectures:
            if lecture.source not in (OUVERTURE, REGISTRE, GRAND_LIVRE):
                vue.lire(lecture.nom)
        for nom in ecritures:
            if nom == INDICE_DES_PRIX:
                vue.ecrire_pas(nom, vue.dernier_prix() * facteur)
            else:
                vue.ecrire_pas(nom, 1.0 + vue.ouverture.t)
        for identifiant in lignes:
            if identifiant == "21":
                # B7 sous la forme exacte −min(Res^{8b} ; L^CB) (ADR 0012, A5).
                livre = vue.grand_livre
                vue.proposer("21", {"Delta_LCB": -min(livre.position("Res"),
                                                      livre.position("L_CB"))})
            else:
                vue.proposer(identifiant, plan[identifiant])
        if (radical, etape) == ("finances_publiques", "8b"):
            perte = plan["16"]["Pi_CB"]
            if perte < 0.0:
                couvert = min(-perte, max(0.0, vue.grand_livre.position("M_G")))
                vue.declarer_montant_couvert("16", couvert)

    return agir


def declarations_d_essai(remplacer=None):
    """Sièges des huit blocs d'essai : (radical → {étape: Siege}), modifiables par `remplacer`."""
    sieges = {}
    for radical in sorted({e for etape in ETAPES for g in etape.groupes for e in g}
                          - {MOTEUR, NOYAU}):
        sieges[radical] = {}
        for etape in etapes_du(radical):
            ecritures, lectures = ECRITURES_ET_LECTURES.get((radical, etape), ((), ()))
            sieges[radical][etape] = siege(
                etape, ecrit=ecritures, lit=lectures,
                propose=lignes_de(radical, etape) if etape in cat.LIGNES_DE_LA_PHASE else (),
                couvre=("16",) if (radical, etape) == ("finances_publiques", "8b") else ())
    if remplacer is not None:
        remplacer(sieges)
    return sieges


def blocs_d_essai(plans, pi_barre=0.02, remplacer=None, actions=None):
    """Les huit blocs d'essai ; `actions` remplace l'action de certains (radical, étape)."""
    blocs = []
    for radical, sieges in declarations_d_essai(remplacer).items():
        faits = {}
        for etape in sieges:
            if actions is not None and (radical, etape) in actions:
                faits[etape] = actions[(radical, etape)]
            else:
                faits[etape] = action_d_essai(radical, etape, plans, pi_barre)
        blocs.append(fabriquer(radical, sieges.values(), faits))
    return blocs


def ordonnanceur_d_essai(plans, pi_barre=0.02, remplacer=None, actions=None,
                         entrees=SANS_ENTREES):
    return assembler(PHASES, blocs_d_essai(plans, pi_barre, remplacer, actions), CADRE, entrees)


class Enregistreur:
    """Observateur d'essai : garde les événements reçus, dans l'ordre."""

    __slots__ = ("evenements",)

    def __init__(self):
        self.evenements = []

    def relever(self, evenement):
        self.evenements.append(evenement)


def bits_de_base(valeur):
    """Empreinte d'une valeur de type de base : bits d'un float, type et valeur sinon."""
    if type(valeur) is float:
        return bits(valeur)
    if type(valeur) is tuple:
        return tuple(bits(x) for x in valeur)
    return (type(valeur).__name__, valeur)


def empreinte(evenements):
    """Empreinte bit à bit d'une suite d'événements : clôtures, états t + 1, variables du pas
    et grandeurs calculées à l'ouverture."""
    rendu = []
    for e in evenements:
        if type(e) is ClotureDePhase:
            rendu.append((e.t, e.phase, tuple((r, o, bits(x)) for r, o, x in e.rapports),
                          tuple((ligne, tuple((n, bits(x)) for n, x in m))
                                for ligne, m in e.montants)))
        else:
            rendu.append((e.t, sauvegarder([e.etat]),
                          tuple((n, bits_de_base(v)) for n, v in e.variables_du_pas),
                          tuple((n, bits_de_base(v)) for n, v in e.grandeurs_ouverture)))
    return rendu


def trajectoire(ordonnanceur, etat, nb_pas, observateur, entrees=ENTREES_VIDES):
    for _ in range(nb_pas):
        etat = executer_pas(etat, entrees, ordonnanceur, observateur)
    return etat


# --------------------------------------------------------------------------
# B1 : PHASES = tab:phases, lue dans la spécification
# --------------------------------------------------------------------------


def _sans_parentheses(texte):
    return re.sub(r"\s*\([^)]*\)", "", texte)


def lire_ecrivains(texte, numero):
    """Colonne « Écrivent » : {étape: groupes}, « puis » séparant les groupes."""
    radical = {libelle: r for r, libelle in LIBELLES.items()}
    if numero == 8:
        sous_phases = {}
        for libelle, lettres in re.findall(r"\s*([^,(]+?)\s*\(([^)]*)\)", texte):
            for lettre in lettres.split(","):
                sous_phases.setdefault("8" + lettre.strip(), []).append(radical[libelle])
        return {e: (tuple(v),) for e, v in sorted(sous_phases.items())}
    groupes = tuple(tuple(radical[b.strip()] for b in _sans_parentheses(g).split(","))
                    for g in re.split(r",?\s*puis\s+", texte))
    return {str(numero): groupes}


def _identifiants(jeton):
    """Lignes du catalogue désignées par un jeton (« 7 », « 19a » : 19a-ménages, …)."""
    if jeton in cat.LIGNE:
        return [jeton]
    return [i for i in cat.IDENTIFIANTS if i.startswith(jeton + "-")]


def lire_lignes(texte, numero):
    """Colonne « Lignes » : {étape: lignes}, « puis » séparant les sous-phases de la phase 8."""
    if texte.strip() == "aucune":
        return {str(numero): ()}
    morceaux = re.split(r",?\s*puis\s+", texte)
    etapes = [str(numero)] if numero != 8 else ["8a", "8b", "8c"]
    rendu = {}
    for etape, morceau in zip(etapes, morceaux, strict=True):
        lignes = []
        for jeton in re.split(r"[,;]", re.sub(r"au jalon J\d", "", morceau)):
            jeton = jeton.strip()
            if " à " in jeton:
                debut, fin = (j.strip() for j in jeton.split(" à "))
                if debut.isdigit():
                    jetons = [str(k) for k in range(int(debut), int(fin) + 1)]
                else:
                    jetons = [debut[:-1] + chr(c) for c in range(ord(debut[-1]), ord(fin[-1]) + 1)]
            else:
                jetons = [jeton]
            for j in jetons:
                lignes += _identifiants(j)
        rendu[etape] = tuple(sorted(lignes, key=cat.IDENTIFIANTS.index))
    return rendu


def lire_phases_lues(texte, numero):
    """Colonne « Lisent » : numéros de phases (« tout » : toutes les phases antérieures)."""
    texte = _sans_parentheses(re.sub(r"\$[^$]*\$", "", texte))
    if texte.strip().startswith("tout"):
        return tuple(range(1, numero))
    numeros = []
    for m in re.finditer(r"(\d+)\s*à\s*(\d+)|(\d+)", texte.split(";")[0]):
        if m.group(3):
            numeros.append(int(m.group(3)))
        else:
            numeros += range(int(m.group(1)), int(m.group(2)) + 1)
    return tuple(numeros)


@pytest.fixture(scope="module")
def table_des_phases(matrices):
    texte = SPECIFICATION.read_text(encoding="utf-8")
    table, ecarts = matrices.lire_table(texte, "tab:phases", "spec")
    assert ecarts == [] and table is not None
    return table


def phases_lues(table):
    """PHASES reconstruite depuis tab:phases : {numéro: (nom, {étape: groupes}, {étape:
    lignes}, phases lues)}."""
    cles = [c.cle for c in table.colonnes]
    assert cles == ["contenu", "ecrivent", "lisent", "lignes"]
    lues = {}
    for ligne in table.lignes:
        numero = int(ligne.identifiant)
        cellules = {c: cel.texte for c, cel in zip(cles, ligne.cellules, strict=True)}
        nom = ligne.etiquette.split(" ", 1)[1]
        lues[numero] = (nom, lire_ecrivains(cellules["ecrivent"], numero),
                        lire_lignes(cellules["lignes"], numero),
                        lire_phases_lues(cellules["lisent"], numero))
    return lues


def phases_declarees(phases):
    return {p.numero: (p.nom, {e.identifiant: e.groupes for e in p.etapes},
                       {e.identifiant: e.lignes for e in p.etapes}, p.lisent) for p in phases}


# Seul point de `PHASES` en avance sur `tab:phases` : la phase 6 lit la phase 2
# (décision du mainteneur du 07/10/2026 ; spécification, ligne 6 des plans de
# la phase 2 et `sec:finances_publiques-impots`). La comparaison stricte le
# retire des deux côtés, et de lui seul ; le test en échec attendu ci-dessous
# compare tout, ce point compris. Au rang 6 (`docwriter`), quand `tab:phases`
# le portera, ce test réussira : retirer sa marque, cette constante et
# `_sans_le_point_en_attente`.
POINT_EN_ATTENTE_DE_TAB_PHASES = (6, 2)


def _sans_le_point_en_attente(phases):
    numero, lue = POINT_EN_ATTENTE_DE_TAB_PHASES
    nom, ecrivains, lignes, lisent = phases[numero]
    return {**phases, numero: (nom, ecrivains, lignes, tuple(p for p in lisent if p != lue))}


def test_declaration_egale_a_tab_phases(table_des_phases):
    """B1 : écrivains, groupes, ordre « puis », sous-phases, couches, lignes et phases lues,
    hors du seul point en attente de `tab:phases`."""
    numero, lue = POINT_EN_ATTENTE_DE_TAB_PHASES
    assert lue in PHASES[numero].lisent
    assert (_sans_le_point_en_attente(phases_declarees(PHASES))
            == _sans_le_point_en_attente(phases_lues(table_des_phases)))


@pytest.mark.xfail(strict=True, reason="tab:phases à corriger au rang 6 (docwriter), décision "
                   "du 07/10/2026")
def test_declaration_egale_a_tab_phases_point_en_attente_compris(table_des_phases):
    """B1, comparaison entière : la phase 6 lit la phase 2 dans `tab:phases` aussi."""
    assert phases_declarees(PHASES) == phases_lues(table_des_phases)


@pytest.mark.parametrize("mutation", [
    "groupe permute", "bloc deplace", "puis devient virgule", "sous-phase", "lisent", "nom",
])
def test_la_comparaison_a_tab_phases_sait_echouer(table_des_phases, mutation):
    """Chaque altération de la déclaration est vue par la comparaison."""
    phases = list(PHASES)
    if mutation == "groupe permute":
        p = phases[4]
        phases[4] = dataclasses.replace(p, etapes=(dataclasses.replace(
            p.etapes[0], groupes=p.etapes[0].groupes[::-1]),))
    elif mutation == "bloc deplace":
        p = phases[6]
        phases[6] = dataclasses.replace(p, etapes=(dataclasses.replace(
            p.etapes[0], groupes=(("finances_publiques", "banque"),)),))
    elif mutation == "puis devient virgule":
        p = phases[1]
        phases[1] = dataclasses.replace(p, etapes=(dataclasses.replace(
            p.etapes[0], groupes=(("moteur", "travail", "banque_centrale"),)),))
    elif mutation == "sous-phase":
        p = phases[8]
        phases[8] = dataclasses.replace(p, etapes=(p.etapes[0], dataclasses.replace(
            p.etapes[1], groupes=(("banque_centrale",), ("finances_publiques",))), p.etapes[2]))
    elif mutation == "lisent":
        phases[7] = dataclasses.replace(phases[7], lisent=(1, 4, 5))
    else:
        phases[3] = dataclasses.replace(phases[3], nom="Crédits")
    assert (_sans_le_point_en_attente(phases_declarees(tuple(phases)))
            != _sans_le_point_en_attente(phases_lues(table_des_phases)))


def test_lecteur_des_lignes():
    assert lire_lignes("6 à 10, 11a à 11c, 14, 15", 6) == {"6": (
        "6", "7", "8", "9", "10", "11a", "11b", "11c", "14", "15")}
    assert lire_lignes("12, 13, puis 16, puis 21", 8) == {
        "8a": ("12", "13"), "8b": ("16",), "8c": ("21",)}
    assert lire_lignes("19a ; 19b au jalon J6", 7)["7"] == (
        "19a-ménages", "19a-banque", "19a-BC", "19b-ménages", "19b-banque")


def test_ecrivains_et_libelles():
    """Les écrivains de PHASES sont les huit radicaux des blocs, plus moteur et noyau ;
    la correspondance radical ↔ libellé est une bijection."""
    ecrivains = {b for e in ETAPES for g in e.groupes for b in g}
    assert ecrivains == set(RADICAUX_DES_BLOCS) | {MOTEUR, NOYAU} == set(LIBELLES)
    assert len(set(LIBELLES.values())) == len(LIBELLES)


def test_phases_structure():
    """Phase 7 à écrivain unique ; phase 9 par couches ; groupe de la phase 9 sans moteur."""
    assert PHASES[7].etapes[0].groupes == (("finances_publiques",),)
    assert PHASES[9].etapes[0].groupes[0] == (NOYAU,)
    assert PHASES[9].etapes[0].groupes[-1] == (MOTEUR,)
    assert [e.identifiant for e in ETAPES] == ["0"] + list(cat.PHASES)


# --------------------------------------------------------------------------
# B3 : assemblage et refus
# --------------------------------------------------------------------------


def test_assemblage_du_monde_d_essai():
    o = ordonnanceur_d_essai(plans_nuls(1))
    assert [e for e, _ in o.etapes] == list(cat.PHASES[:-1])
    # Ordre d'appel : groupe par groupe, ordre canonique des radicaux.
    assert [d.radical for d, _ in dict(o.etapes)["5"]] == [
        "prix", "production", "finances_publiques", "investissement", "menages"]
    assert [d.radical for d, _ in o.appels_de_la_phase_9] == ["investissement", "menages"]
    with pytest.raises(dataclasses.FrozenInstanceError):
        o.etapes = ()


def _retirer(radical, etape, champ, valeur):
    def remplacer(sieges):
        sieges[radical][etape] = dataclasses.replace(sieges[radical][etape], **{champ: valeur})
    return remplacer


def _ajouter_siege(radical, etape, **champs):
    def remplacer(sieges):
        sieges[radical][etape] = siege(etape, **champs)
    return remplacer


REFUS_D_ASSEMBLAGE = {
    "écrivain sans implémentation": (lambda s: s.pop("prix"), "sans implémentation"),
    "bloc écrivain d'aucune phase": (lambda s: s.update({"inconnu": {}}), "aucune phase"),
    "siège hors des étapes du bloc": (_ajouter_siege("prix", "6"), "ne déclare pas le bloc"),
    "étape sans siège": (lambda s: s["production"].pop("5"), "sans siège"),
    "ligne hors de sa phase": (_retirer("menages", "2", "propose", ("1",)), "hors de sa phase"),
    "ligne d'un autre bloc": (_retirer("banque", "6", "propose", ("6", "9", "10", "15")),
                              "autre bloc"),
    "ligne sans proposant": (_retirer("investissement", "3", "propose", ()), "exactement un"),
    "ligne proposée deux fois": (_retirer("investissement", "3", "propose", ("18", "18")),
                                 "exactement un"),
    "ligne 19b proposée": (_retirer("finances_publiques", "7", "propose", (
        "19a-ménages", "19a-banque", "19a-BC", "19b-ménages")), "autre bloc"),
    "contrepartie proposée": (_retirer("banque", "8c", "propose", ("21", "20")), "autre bloc"),
    "ligne inconnue": (_retirer("banque", "8c", "propose", ("21", "99")), "inconnue"),
    "flux déclaré en phase 9": (_retirer("menages", "9", "propose", ("1",)), "hors de sa phase"),
    "montant couvert par un autre bloc": (_retirer("banque_centrale", "8b", "couvre", ("16",)),
                                          "liste fermée"),
    "montant couvert hors de sa phase": (_retirer("finances_publiques", "7", "couvre", ("16",)),
                                         "liste fermée"),
    "montant couvert déclaré deux fois": (
        _retirer("finances_publiques", "8b", "couvre", ("16", "16")), "déclaré deux fois"),
    "variable du pas écrite en phase 9": (_retirer("menages", "9", "ecrit", ("x",)),
                                          "variables d'état"),
    "variable du pas écrite deux fois": (_retirer("banque_centrale", "1", "ecrit", ("i_CB", "W")),
                                         "déjà écrite"),
    "variable du pas homonyme d'une grandeur": (_retirer("travail", "1", "ecrit", ("annee",)),
                                                "déjà écrite"),
    "variable d'état d'un autre propriétaire": (_retirer("menages", "9", "etat", ("t",)),
                                                "autre bloc"),
    "variable d'état inconnue": (_retirer("menages", "9", "etat", ("zzz",)), "inconnue"),
    "triangularité : phase ultérieure": (_retirer("travail", "4", "lit", (Lecture("5", "P"),)),
                                         "triangularité"),
    "triangularité : même groupe": (_retirer("travail", "1", "lit", (Lecture("1", "i_CB"),)),
                                    "triangularité"),
    "triangularité : groupe ultérieur": (_retirer("travail", "4", "lit", (Lecture("4", "y"),)),
                                         "triangularité"),
    "triangularité : couche moteur de la phase 9": (
        _retirer("travail", "1", "lit", (Lecture("9", "P"),)), "déclarée en phase 9"),
    "source déclarée fausse": (_retirer("production", "5", "lit", (Lecture("5", "N"),)),
                               "écrite en phase 4"),
    "variable que personne n'écrit": (_retirer("production", "5", "lit", (Lecture("2", "q"),)),
                                      "personne"),
    "ligne lue avant sa clôture": (_retirer("banque", "6", "lit", (Lecture(GRAND_LIVRE, "16"),)),
                                   "avant la clôture"),
    "ligne de l'étape lue dans l'étape": (
        _retirer("investissement", "3", "lit", (Lecture(GRAND_LIVRE, "18"),)), "avant la clôture"),
    "contrepartie lue avant la phase 9": (
        _retirer("banque", "8c", "lit", (Lecture(GRAND_LIVRE, "20"),)), "avant la clôture"),
    "lecture inconnue du grand livre": (
        _retirer("banque", "8c", "lit", (Lecture(GRAND_LIVRE, "Z"),)), "inconnue"),
    "champ inconnu de l'ouverture": (_retirer("banque", "8c", "lit", (Lecture(OUVERTURE, "Z"),)),
                                     "champ inconnu"),
    "lecture inconnue du registre": (_retirer("prix", "5", "lit", (Lecture(REGISTRE, "P"),)),
                                     "inconnue du registre"),
    "source inconnue": (_retirer("prix", "5", "lit", (Lecture("6b", "P"),)), "source"),
    "phase hors de la colonne Lisent": (
        _retirer("investissement", "3", "lit", (Lecture("1", "i_CB"),)),
        "phase 1 hors de la colonne « Lisent » de la phase 3"),
    "indice des prix écrit par un autre bloc": (
        lambda s: (s.__setitem__("prix", {"5": siege("5")}),
                   s["production"].__setitem__("5", siege("5", ecrit=("P",), propose=("4",)))),
        "indice des prix écrit par production"),
}


@pytest.mark.parametrize("cas", sorted(REFUS_D_ASSEMBLAGE))
def test_assemblage_refuse(cas):
    """B3 : chaque déclaration fautive est refusée avant le premier pas, avec un diagnostic."""
    remplacer, motif = REFUS_D_ASSEMBLAGE[cas]
    blocs = []
    for radical, sieges in declarations_d_essai(remplacer).items():
        blocs.append(fabriquer(radical, sieges.values(),
                               {e: (lambda vue: None) for e in sieges}))
    with pytest.raises(DefautDeDeclaration, match=motif):
        assembler(PHASES, blocs, CADRE, SANS_ENTREES)


@pytest.mark.parametrize("lecture, etape, lecteur", [
    (Lecture("4", "N"), "4", "production"),           # même phase, groupe antérieur
    (Lecture(GRAND_LIVRE, "16"), "8c", "banque"),     # sous-phase antérieure
    (Lecture(GRAND_LIVRE, "12"), "8b", "finances_publiques"),
    (Lecture(GRAND_LIVRE, "20"), "9", "menages"),     # contrepartie lue en phase 9
    (Lecture("0", "date_de_decision"), "1", "travail"),
    (Lecture(OUVERTURE, "registre_prix"), "1", "travail"),
    (Lecture(GRAND_LIVRE, "D_H"), "2", "menages"),    # position courante
    (Lecture("0", "date_de_decision"), "3", "investissement"),  # phase 0 hors de « Lisent »
    (Lecture("1", "i_CB"), "7", "finances_publiques"),  # phase 1 dans « Lisent » de la 7
])
def test_lectures_admises(lecture, etape, lecteur):
    """B3 : lectures triangulaires admises."""
    def remplacer(sieges):
        s = sieges[lecteur][etape]
        sieges[lecteur][etape] = dataclasses.replace(s, lit=s.lit + (lecture,))
    assembler(PHASES, blocs_d_essai(plans_nuls(1), remplacer=remplacer), CADRE, SANS_ENTREES)


def _plan_de_la_phase_2(sieges):
    s = sieges["menages"]["2"]
    sieges["menages"]["2"] = dataclasses.replace(s, ecrit=s.ecrit + ("T_H_plan",))
    s = sieges["finances_publiques"]["6"]
    sieges["finances_publiques"]["6"] = dataclasses.replace(
        s, lit=s.lit + (Lecture("2", "T_H_plan"),))


def test_colonne_lisent_normative():
    """Décision du 07/10/2026 : la phase 6 lit la phase 2 (impôt des ménages planifié en
    phase 2, proposé en phase 6) ; sans la phase 2 dans sa colonne « Lisent », la même
    déclaration est refusée."""
    blocs = blocs_d_essai(plans_nuls(1), remplacer=_plan_de_la_phase_2)
    assert 2 in PHASES[6].lisent
    assembler(PHASES, blocs, CADRE, SANS_ENTREES)
    phases = list(PHASES)
    phases[6] = dataclasses.replace(phases[6], lisent=(1, 3, 4, 5))
    with pytest.raises(DefautDeDeclaration, match="phase 2 hors de la colonne « Lisent » de la "
                       "phase 6") as refus:
        assembler(tuple(phases), blocs, CADRE, SANS_ENTREES)
    assert (refus.value.etape, refus.value.bloc, refus.value.nom) == (
        "6", "finances_publiques", "T_H_plan")


def test_bloc_sans_declaration_ni_methode():
    blocs = blocs_d_essai(plans_nuls(1))
    with pytest.raises(DefautDeDeclaration, match="sans déclaration"):
        assembler(PHASES, blocs + [object()], CADRE, SANS_ENTREES)
    sans_methode = fabriquer("prix", [siege("5", ecrit=("P",))], {})
    autres = [b for b in blocs if b.declaration.radical != "prix"]
    with pytest.raises(DefautDeDeclaration, match="phase_5 absente"):
        assembler(PHASES, autres + [sans_methode], CADRE, SANS_ENTREES)
    with pytest.raises(DefautDeDeclaration, match="même radical"):
        assembler(PHASES, blocs + blocs[:1], CADRE, SANS_ENTREES)


@pytest.mark.parametrize("mutation, motif", [
    ("moteur dans un groupe de blocs", "moteur hors de sa place"),
    ("noyau absent de la phase 9", "noyau hors de sa place"),
    ("étape absente", "clôtures du noyau"),
    ("lignes fausses", "catalogue"),
])
def test_assemblage_refuse_une_declaration_des_phases_fautive(mutation, motif):
    phases = list(PHASES)
    if mutation == "moteur dans un groupe de blocs":
        e = phases[1].etapes[0]
        phases[1] = dataclasses.replace(phases[1], etapes=(dataclasses.replace(
            e, groupes=(("moteur", "travail"), ("banque_centrale",))),))
    elif mutation == "noyau absent de la phase 9":
        e = phases[9].etapes[0]
        phases[9] = dataclasses.replace(phases[9], etapes=(dataclasses.replace(
            e, groupes=e.groupes[1:]),))
    elif mutation == "étape absente":
        phases[8] = dataclasses.replace(phases[8], etapes=phases[8].etapes[:2])
    else:
        phases[3] = dataclasses.replace(phases[3], etapes=(dataclasses.replace(
            phases[3].etapes[0], lignes=("18", "21")),))
    with pytest.raises(DefautDeDeclaration, match=motif):
        assembler(tuple(phases), blocs_d_essai(plans_nuls(1)), CADRE, SANS_ENTREES)


class _BaseAEmplacement:
    __slots__ = ("memoire",)


class _BaseSansSlots:
    pass


@pytest.mark.parametrize("cas, bases, slots, motif", [
    ("sans __slots__", (), None, "__dict__"),
    ("__slots__ non vide", (), ("memoire",), "__slots__ non vide de Bloc_prix"),
    ("__slots__ en chaîne", (), "memoire", "__slots__ non vide de Bloc_prix"),
    ("emplacement hérité", (_BaseAEmplacement,), (), "__slots__ non vide de _BaseAEmplacement"),
    ("__dict__ hérité", (_BaseSansSlots,), (), "__dict__"),
])
def test_bloc_a_attribut_d_instance_refuse(cas, bases, slots, motif):
    """Annotation du 07/10/2026, point 8 : un bloc n'a aucun attribut d'instance, même vide."""
    blocs = [b for b in blocs_d_essai(plans_nuls(1)) if b.declaration.radical != "prix"]
    sieges = declarations_d_essai()["prix"]
    fautif = fabriquer("prix", sieges.values(), {e: (lambda vue: None) for e in sieges},
                       bases=bases, slots=slots)
    with pytest.raises(DefautDeDeclaration, match=motif) as refus:
        assembler(PHASES, blocs + [fautif], CADRE, SANS_ENTREES)
    assert refus.value.bloc == "prix"


def test_blocs_d_essai_sans_attribut_d_instance():
    """Les blocs d'essai s'y conforment : déclaration en attribut de classe."""
    for bloc in blocs_d_essai(plans_nuls(1)):
        assert not hasattr(bloc, "__dict__")
        assert "declaration" in type(bloc).__dict__


# --------------------------------------------------------------------------
# B5 : déroulement d'un pas
# --------------------------------------------------------------------------


def test_pas_complet_et_releves_dans_l_ordre():
    """Onze clôtures relevées dans l'ordre, puis la fin du pas ; t avance de 1."""
    plans = tirer_plans(6)
    o = ordonnanceur_d_essai(plans)
    releve = Enregistreur()
    etat = etat_initial()
    for t in range(6):
        etat = executer_pas(etat, ENTREES_VIDES, o, releve)
        assert etat.t == t + 1
    attendu = [(t, p) for t in range(6) for p in list(cat.PHASES) + ["fin"]]
    assert [(e.t, e.phase if type(e) is ClotureDePhase else "fin")
            for e in releve.evenements] == attendu
    assert all(type(e) is FinDePas for e in releve.evenements[11::12])


def test_couches_de_la_phase_9_dans_l_ordre():
    """ADR 0009, point 2 : clôture du noyau (relevée), puis les blocs du groupe, puis la
    couche moteur (fin du pas relevée), consignés dans un même journal."""
    journal = []

    class Journal:
        __slots__ = ()

        def relever(self, evenement):
            journal.append(("clôture", evenement.phase) if type(evenement) is ClotureDePhase
                           else ("fin",))

    plans = plans_nuls(2)

    def consigner(radical):
        base = action_d_essai(radical, "9", plans, 0.02)

        def agir(vue):
            journal.append(("bloc", radical))
            base(vue)
        return agir

    o = ordonnanceur_d_essai(plans, actions={(r, "9"): consigner(r)
                                             for r in ("menages", "investissement")})
    trajectoire(o, etat_initial(), 2, Journal())
    pas = [("clôture", p) for p in cat.PHASES] + [("fin",)]
    pas[-1:-1] = [("bloc", "investissement"), ("bloc", "menages")]
    assert journal == pas + pas
    assert pas[-5:] == [("clôture", "8c"), ("clôture", "9"), ("bloc", "investissement"),
                        ("bloc", "menages"), ("fin",)]


def test_identifiant_et_graine_recopies():
    """L'état t + 1 garde l'identifiant et la graine du pays (valeurs autres que celles de
    l'état d'essai par défaut)."""
    o = ordonnanceur_d_essai(plans_nuls(3))
    etat = dataclasses.replace(etat_initial(), identifiant="B", graine=12345)
    for t in range(3):
        etat = executer_pas(etat, ENTREES_VIDES, o, ObservateurNul())
        assert (etat.identifiant, etat.graine, etat.t) == ("B", 12345, t + 1)


ENTREES_D_ESSAI = DeclarationDesEntrees(("sigma_L",), ("levier",))


def _valeurs_des_entrees(t):
    return EntreesDuTour((("sigma_L", 0.5 + t),), (("levier", 0.03),))


def test_fin_de_pas_porte_variables_et_grandeurs():
    """E1 (annotation du 07/10/2026, point 2) : variables du pas écrites et grandeurs
    calculées à l'ouverture, (nom, valeur) de types de base, dans l'ordre d'inscription."""
    plans = plans_nuls(14)
    o = ordonnanceur_d_essai(plans, entrees=ENTREES_D_ESSAI)
    releve = Enregistreur()
    etat = etat_initial()
    for t in range(14):
        etat = executer_pas(etat, _valeurs_des_entrees(t), o, releve)
    fins = [e for e in releve.evenements if type(e) is FinDePas]
    assert [f.t for f in fins] == list(range(14))
    facteur = facteur_par_pas(TauxDeCroissance(0.02))
    assert fins[13].etat.registre_prix[0] == fins[12].etat.registre_prix[0] * facteur
    for f in (fins[0], fins[13]):
        t = f.t
        # P_t : premier niveau du registre avancé de l'état t + 1.
        p_t = f.etat.registre_prix[0]
        assert f.variables_du_pas == (
            ("sigma_L", 0.5 + t), ("levier", 0.03), ("i_CB", 1.0 + t), (INDICE_DES_PRIX, p_t),
            ("y", 1.0 + t), ("W", 1.0 + t), ("N", 1.0 + t))
    assert fins[0].grandeurs_ouverture == (("annee", 1), ("mois", 1), ("date_de_decision", True))
    assert fins[13].grandeurs_ouverture == (("annee", 2), ("mois", 2),
                                            ("date_de_decision", True))
    for f in fins:
        for nom, valeur in f.variables_du_pas + f.grandeurs_ouverture:
            assert type(nom) is str and type(valeur) in (float, int, bool, tuple)
    with pytest.raises(dataclasses.FrozenInstanceError):
        fins[0].variables_du_pas = ()


def test_fin_de_pas_independante_de_l_ordre_de_la_liste_de_blocs():
    """L'ordre déclaré ne dépend pas de l'ordre de la liste passée à `assembler` : trois
    ordres de la liste, mêmes `FinDePas` (égales et bit à bit)."""
    plans = tirer_plans(3)
    blocs = blocs_d_essai(plans)
    melange = list(blocs)
    np.random.default_rng(GRAINE).shuffle(melange)
    ordres = (blocs, blocs[::-1], melange)
    assert len({tuple(b.declaration.radical for b in liste) for liste in ordres}) == 3
    fins = []
    for liste in ordres:
        o = assembler(PHASES, liste, CADRE, ENTREES_D_ESSAI)
        releve = Enregistreur()
        etat = etat_initial()
        for t in range(3):
            etat = executer_pas(etat, _valeurs_des_entrees(t), o, releve)
        fins.append([e for e in releve.evenements if type(e) is FinDePas])
    assert fins[0] == fins[1] == fins[2]
    assert empreinte(fins[0]) == empreinte(fins[1]) == empreinte(fins[2])
    assert len(fins[0][0].variables_du_pas) == 7


def test_ligne_16_negative_et_montant_couvert_exerces():
    """Le monde d'essai couvre la ligne 16 négative avec déclaration du montant couvert."""
    plans = tirer_plans(6)
    assert any(plans[t]["16"]["Pi_CB"] < 0.0 for t in range(6))
    assert any(plans[t]["16"]["Pi_CB"] > 0.0 for t in range(6))


def test_observation_sans_effet_et_ouverture_figee():
    """E1 : ObservateurNul ou enregistreur, mêmes sauvegardes ; ADR 0009, test (4)."""
    plans = tirer_plans(12)
    o = ordonnanceur_d_essai(plans)
    debut = etat_initial()
    avant = sauvegarder([debut])
    nul = trajectoire(o, debut, 12, ObservateurNul())
    observe = trajectoire(o, debut, 12, Enregistreur())
    assert sauvegarder([nul]) == sauvegarder([observe])
    assert sauvegarder([debut]) == avant


def test_executer_pas_sans_etat_propre():
    """B5 : deux exécutions du même pas, ou d'un pas après d'autres, sont identiques bit à bit."""
    plans = tirer_plans(4)
    o = ordonnanceur_d_essai(plans)
    e0 = etat_initial()
    r1, r2, r3 = Enregistreur(), Enregistreur(), Enregistreur()
    executer_pas(e0, ENTREES_VIDES, o, r1)
    trajectoire(o, e0, 3, Enregistreur())
    executer_pas(e0, ENTREES_VIDES, o, r2)
    executer_pas(e0, ENTREES_VIDES, ordonnanceur_d_essai(plans), r3)
    assert empreinte(r1.evenements) == empreinte(r2.evenements) == empreinte(r3.evenements)


def test_flux_propose_en_phase_9_refuse():
    """ADR 0009, point 2 : un bloc du groupe de la phase 9 qui propose un flux est arrêté."""
    def proposer_en_9(vue):
        vue.proposer("1", {"C": 1.0})
    o = ordonnanceur_d_essai(plans_nuls(1), actions={("menages", "9"): proposer_en_9})
    with pytest.raises(RefusDuMoteur, match="aucun flux en phase 9") as refus:
        executer_pas(etat_initial(), ENTREES_VIDES, o, ObservateurNul())
    assert (refus.value.etape, refus.value.bloc, refus.value.nom) == ("9", "menages", "1")


def test_declaration_de_montant_couvert_en_phase_9_refusee():
    def couvrir_en_9(vue):
        vue.declarer_montant_couvert("16", 0.0)
    o = ordonnanceur_d_essai(plans_nuls(1), actions={("menages", "9"): couvrir_en_9})
    with pytest.raises(RefusDuMoteur, match="aucun flux en phase 9"):
        executer_pas(etat_initial(), ENTREES_VIDES, o, ObservateurNul())


def test_ligne_non_declaree_refusee_par_la_vue():
    """B2 : la vue n'ouvre au bloc que les lignes de son siège ; le noyau reste le dernier
    rempart (une ligne d'une autre phase y serait refusée)."""
    def proposer_hors_siege(vue):
        vue.proposer("2", {"G": 1.0})
    o = ordonnanceur_d_essai(plans_nuls(1), actions={("finances_publiques", "2"):
                                                     proposer_hors_siege})
    with pytest.raises(RefusDuMoteur, match="ligne non déclarée") as refus:
        executer_pas(etat_initial(), ENTREES_VIDES, o, ObservateurNul())
    assert refus.value.etape == "2" and "phase 9" not in str(refus.value)


def _remplacer_action(radical, etape, faire):
    base = action_d_essai(radical, etape, plans_nuls(1), 0.02)

    def agir(vue):
        faire(vue, base)
    return {(radical, etape): agir}


@pytest.mark.parametrize("cas, faire, motif", [
    ("seconde écriture", lambda vue, base: (base(vue), vue.ecrire_pas("y", 2.0)),
     "seconde écriture"),
    ("écriture non déclarée", lambda vue, base: (base(vue), vue.ecrire_pas("N", 2.0)),
     "non déclarée par le bloc"),
    ("lecture non déclarée", lambda vue, base: (base(vue), vue.lire("i_CB")), "non déclarée"),
    ("variable d'état d'un autre propriétaire", lambda vue, base: (
        base(vue), vue.ecrire_etat("t", 1)), "hors de son propriétaire"),
    ("valeur NumPy", lambda vue, base: vue.ecrire_pas("y", np.float64(1.0)), "float, int"),
    ("valeur non finie", lambda vue, base: vue.ecrire_pas("y", float("nan")), "non finie"),
])
def test_refus_a_l_execution(cas, faire, motif):
    """B4 : l'espace du pas et la vue refusent ce qui n'est pas déclaré, jamais un défaut."""
    o = ordonnanceur_d_essai(plans_nuls(1), actions=_remplacer_action("production", "4", faire))
    with pytest.raises(RefusDuMoteur, match=motif) as refus:
        executer_pas(etat_initial(), ENTREES_VIDES, o, ObservateurNul())
    assert refus.value.t == 0


@pytest.mark.parametrize("valeur", [float("nan"), float("inf"), -float("inf"),
                                    (1.0, float("nan")), (float("-inf"),)])
def test_espace_du_pas_refuse_une_valeur_non_finie(valeur):
    """Constat 6 de l'audit de #97 : NaN et infinis refusés, éléments d'un n-uplet compris."""
    espace = ordo.VariablesDuPas(frozenset({"x"}), 3)
    with pytest.raises(RefusDuMoteur, match="non finie") as refus:
        espace.ecrire("x", valeur)
    assert (refus.value.t, refus.value.nom) == (3, "x")
    espace.ecrire("x", (1.0, 2.0))
    assert espace.lire("x") == (1.0, 2.0)


@pytest.mark.parametrize("famille", ["scenario", "leviers"])
@pytest.mark.parametrize("valeur", [float("nan"), float("inf"), -float("inf")])
def test_entrees_du_tour_non_finies_refusees(famille, valeur):
    """Constat 6 : une entrée du tour non finie est refusée, à l'appel direct comme au pas."""
    entrees = (EntreesDuTour(((("sigma_L", valeur),)), (("levier", 0.03),))
               if famille == "scenario" else EntreesDuTour((("sigma_L", 0.5),),
                                                         (("levier", valeur),)))
    with pytest.raises(RefusDuMoteur, match="non finie"):
        ordo._verifier_entrees(entrees, ENTREES_D_ESSAI, 0)
    ordo._verifier_entrees(_valeurs_des_entrees(0), ENTREES_D_ESSAI, 0)
    o = ordonnanceur_d_essai(plans_nuls(1), entrees=ENTREES_D_ESSAI)
    with pytest.raises(RefusDuMoteur, match="non finie") as refus:
        executer_pas(etat_initial(), entrees, o, ObservateurNul())
    assert refus.value.nom == ("sigma_L" if famille == "scenario" else "levier")


def test_lecture_d_une_variable_non_ecrite_refusee():
    """B4 : une lecture d'un nom déclaré mais non encore écrit est refusée."""
    o = ordonnanceur_d_essai(plans_nuls(1), actions={("travail", "4"): lambda vue: None})
    with pytest.raises(RefusDuMoteur, match="avant son écriture"):
        executer_pas(etat_initial(), ENTREES_VIDES, o, ObservateurNul())


def test_indice_des_prix_non_ecrit_refuse():
    o = ordonnanceur_d_essai(plans_nuls(1), actions={
        ("prix", "5"): lambda vue: None,
        ("production", "5"): lambda vue: vue.proposer("4", {"Delta_IN": 0.0})})
    with pytest.raises(RefusDuMoteur, match="avant son écriture") as refus:
        executer_pas(etat_initial(), ENTREES_VIDES, o, ObservateurNul())
    assert refus.value.nom == INDICE_DES_PRIX


# --------------------------------------------------------------------------
# Entrées du tour (B5, G4)
# --------------------------------------------------------------------------


def _avec_entrees(sieges):
    s = sieges["banque"]["6"]
    sieges["banque"]["6"] = dataclasses.replace(s, lit=s.lit + (Lecture("0", "sigma_L"),))
    s = sieges["banque_centrale"]["1"]
    sieges["banque_centrale"]["1"] = dataclasses.replace(s, lit=s.lit + (Lecture("1", "levier"),))


def test_entrees_du_tour_lues_par_les_blocs():
    """Entrée de scénario en phase 0, levier en phase 1, lus par les blocs qui les déclarent."""
    lus = []

    def lire_sigma(vue):
        lus.append(("sigma_L", vue.lire("sigma_L")))
        action_d_essai("banque", "6", plans_nuls(1), 0.02)(vue)

    def lire_levier(vue):
        lus.append(("levier", vue.lire("levier")))
        action_d_essai("banque_centrale", "1", plans_nuls(1), 0.02)(vue)

    o = ordonnanceur_d_essai(plans_nuls(1), remplacer=_avec_entrees,
                             actions={("banque", "6"): lire_sigma,
                                      ("banque_centrale", "1"): lire_levier},
                             entrees=DeclarationDesEntrees(("sigma_L",), ("levier",)))
    executer_pas(etat_initial(), EntreesDuTour((("sigma_L", 0.5),), (("levier", 0.03),)), o,
                 ObservateurNul())
    assert lus == [("levier", 0.03), ("sigma_L", 0.5)]
    for entrees in (ENTREES_VIDES, EntreesDuTour((("sigma_L", 0.5),), (("autre", 0.03),)),
                    EntreesDuTour((("sigma_L", 1),), (("levier", 0.03),)), {}):
        with pytest.raises(RefusDuMoteur, match="entrée"):
            executer_pas(etat_initial(), entrees, o, ObservateurNul())


def test_levier_lu_par_un_bloc_du_premier_groupe_refuse():
    """Le levier est écrit par le moteur au premier groupe de la phase 1 : lisible après lui."""
    def remplacer(sieges):
        s = sieges["menages"]["2"]
        sieges["menages"]["2"] = dataclasses.replace(s, lit=s.lit + (Lecture("0", "levier"),))
    with pytest.raises(DefautDeDeclaration, match="déclarée en phase 0"):
        ordonnanceur_d_essai(plans_nuls(1), remplacer=remplacer,
                             entrees=DeclarationDesEntrees((), ("levier",)))


# --------------------------------------------------------------------------
# C1, C2 : variables d'état d'un bloc (schéma d'essai)
# --------------------------------------------------------------------------


@pytest.fixture
def schema_avec_variables_de_bloc(monkeypatch):
    """Schéma d'essai : deux variables de bloc, l'une écrite en phase 1, l'autre en phase 9.

    Aucun bloc n'a de variable d'état au J2 (ADR 0012, C1 ; G1 ouverte) : le
    test étend le schéma le temps du test, sans toucher `etat/`.
    """
    base = etat_initial()
    ajout = (
        VariableEtat("pi_cible", "banque_centrale", "1", "par an, taux de croissance", float, 1,
                     "cible déclarée", Invariance.SANS_DIMENSION),
        VariableEtat("revenu", "menages", "9", "u.m.", float, 1, "essai", Invariance.NOMINAL),
    )
    variables = schema.VARIABLES + ajout
    etat_pays = dataclasses.make_dataclass(
        "EtatPays", [(f.name, f.type) for f in dataclasses.fields(schema.EtatPays)]
        + [(v.nom, float) for v in ajout], frozen=True, slots=True)
    monkeypatch.setattr(schema, "VARIABLES", variables)
    monkeypatch.setattr(schema, "VARIABLE", {v.nom: v for v in variables})
    monkeypatch.setattr(schema, "EtatPays", etat_pays)
    monkeypatch.setattr(schema, "CHAMPS", tuple(f.name for f in dataclasses.fields(etat_pays)))
    return etat_pays(**{f.name: getattr(base, f.name) for f in dataclasses.fields(EtatPays)},
                     pi_cible=0.02, revenu=0.0)


def _sieges_d_etat(sieges):
    s = sieges["banque_centrale"]["1"]
    sieges["banque_centrale"]["1"] = dataclasses.replace(s, etat=("pi_cible",))
    s = sieges["menages"]["9"]
    sieges["menages"]["9"] = dataclasses.replace(s, etat=("revenu",))
    s = sieges["finances_publiques"]["7"]
    sieges["finances_publiques"]["7"] = dataclasses.replace(
        s, lit=s.lit + (Lecture("1", "pi_cible_suivant"),))


def _actions_d_etat(lus, doubler=False, oublier=False):
    def cible(vue):
        action_d_essai("banque_centrale", "1", plans_nuls(1), 0.02)(vue)
        vue.ecrire_etat("pi_cible", vue.ouverture.pi_cible)
        if doubler:
            vue.ecrire_etat("pi_cible", 0.0)

    def revenu(vue):
        if not oublier:
            vue.ecrire_etat("revenu", vue.grand_livre.montant_execute_ligne("5"))

    def tresor(vue):
        lus.append(vue.lire("pi_cible_suivant"))
        action_d_essai("finances_publiques", "7", plans_nuls(1), 0.02)(vue)

    return {("banque_centrale", "1"): cible, ("menages", "9"): revenu,
            ("finances_publiques", "7"): tresor}


def test_variable_d_etat_ecrite_une_fois_et_assemblee(schema_avec_variables_de_bloc):
    """C2 : écrite par son propriétaire, lue sous son nom daté, assemblée dans l'état t + 1 et
    relevée dans la fin du pas sous `<nom>_suivant`, à sa place d'inscription."""
    lus = []
    plans = tirer_plans(1)
    o = ordonnanceur_d_essai(plans, remplacer=_sieges_d_etat, actions=_actions_d_etat(lus))
    assert o.variables_des_blocs == ("pi_cible", "revenu")
    releve = Enregistreur()
    suivant = executer_pas(schema_avec_variables_de_bloc, ENTREES_VIDES, o, releve)
    assert lus == [0.02]
    assert suivant.pi_cible == 0.02
    assert suivant.revenu == plans[0]["5"]["WB"]
    fin = releve.evenements[-1]
    assert [n for n, _ in fin.variables_du_pas] == [
        "i_CB", "pi_cible_suivant", "revenu_suivant", "P", "y", "W", "N"]
    assert dict(fin.variables_du_pas)["revenu_suivant"] == plans[0]["5"]["WB"]


@pytest.mark.parametrize("valeur", [1, True, (0.02,)])
def test_variable_d_etat_de_mauvais_type_refusee(schema_avec_variables_de_bloc, valeur):
    """C2 : la vue refuse une valeur du pas suivant qui n'a pas le type déclaré au schéma,
    même de type de base pour l'espace du pas (`int`, `bool`, n-uplet de `float`)."""
    def cible(vue):
        action_d_essai("banque_centrale", "1", plans_nuls(1), 0.02)(vue)
        vue.ecrire_etat("pi_cible", valeur)
    actions = {**_actions_d_etat([]), ("banque_centrale", "1"): cible}
    o = ordonnanceur_d_essai(plans_nuls(1), remplacer=_sieges_d_etat, actions=actions)
    with pytest.raises(RefusDuMoteur, match="float attendu") as refus:
        executer_pas(schema_avec_variables_de_bloc, ENTREES_VIDES, o, ObservateurNul())
    assert (refus.value.etape, refus.value.bloc, refus.value.nom) == (
        "1", "banque_centrale", "pi_cible")


@pytest.mark.parametrize("doubler, oublier, motif", [
    (True, False, "seconde écriture d'une variable d'état"),
    (False, True, "non écrite par son propriétaire"),
])
def test_variable_d_etat_ecriture_unique(schema_avec_variables_de_bloc, doubler, oublier, motif):
    """ADR 0009, test (1) : seconde écriture refusée ; variable non écrite, arrêt en phase 9."""
    o = ordonnanceur_d_essai(plans_nuls(1), remplacer=_sieges_d_etat,
                             actions=_actions_d_etat([], doubler, oublier))
    with pytest.raises(RefusDuMoteur, match=motif):
        executer_pas(schema_avec_variables_de_bloc, ENTREES_VIDES, o,
                     ObservateurNul())


@pytest.mark.parametrize("cas, remplacer, motif", [
    ("sans propriétaire qui l'écrive", lambda s: None, "sans propriétaire"),
    ("hors de sa phase", lambda s: (_sieges_d_etat(s), s["menages"].__setitem__(
        "9", siege("9")), s["menages"].__setitem__("5", dataclasses.replace(
            s["menages"]["5"], etat=("revenu",)))), "hors de sa phase"),
    ("deux propriétaires", lambda s: (_sieges_d_etat(s), s["menages"].__setitem__(
        "5", dataclasses.replace(s["menages"]["5"], etat=("revenu",)))), "hors de sa phase"),
    ("lue dans le même groupe en phase 9", lambda s: (_sieges_d_etat(s), s[
        "investissement"].__setitem__("9", siege("9", lit=(Lecture("9", "revenu_suivant"),)))),
     "triangularité"),
    ("écrite deux fois par son propriétaire", lambda s: (_sieges_d_etat(s), s[
        "menages"].__setitem__("9", siege("9", etat=("revenu", "revenu")))), "deux fois"),
])
def test_variable_d_etat_declarations_refusees(schema_avec_variables_de_bloc, cas, remplacer,
                                               motif):
    """C1, B3 : propriétaire unique, dans sa phase d'écriture ; phase 9 sans lecture mutuelle."""
    with pytest.raises(DefautDeDeclaration, match=motif):
        ordonnanceur_d_essai(plans_nuls(1), remplacer=remplacer)


# --------------------------------------------------------------------------
# Registre sur une trajectoire (C97-1, C97-2)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi_barre", [0.0, 0.02, 0.10])
def test_registre_stationnaire_a_chaque_ouverture(pi_barre):
    """C97-1 : P_{t−u}/P_{t−1} = (1 + π̄)^{−(u−1)/n_a}, u = 1 … 13, et glissement = π̄, à 1e−12.

    Le bloc prix d'essai écrit P_t = P_{t−1} (1 + π̄)^{1/n_a} en phase 5, depuis
    un registre initial stationnaire ; contrôle à chaque ouverture, 720 pas.
    """
    o = ordonnanceur_d_essai(plans_nuls(720), pi_barre=pi_barre)
    attendus = [(1.0 + pi_barre) ** (-(u - 1) / N_A) for u in range(1, N_A + 2)]
    etat = etat_initial(pi_barre)
    pire = 0.0
    for _ in range(720):
        etat = executer_pas(etat, ENTREES_VIDES, o, ObservateurNul())
        r = etat.registre_prix
        for u in range(1, N_A + 2):
            pire = max(pire, abs(r[u - 1] / r[0] / attendus[u - 1] - 1.0))
        glissement = r[0] / r[N_A] - 1.0
        pire = max(pire, abs((1.0 + glissement) / (1.0 + pi_barre) - 1.0))
    assert etat.t == 720
    assert pire <= 1e-12


def test_avance_du_registre_bit_a_bit():
    """C97-2 : registre d'ouverture de t + 1 = (P_t, P_{t−1}, …, P_{t−12}), une copie bit à bit."""
    facteur = facteur_par_pas(TauxDeCroissance(0.02))
    o = ordonnanceur_d_essai(plans_nuls(30))
    etat = etat_initial()
    for _ in range(30):
        suivant = executer_pas(etat, ENTREES_VIDES, o, ObservateurNul())
        p_t = etat.registre_prix[0] * facteur
        assert [bits(x) for x in suivant.registre_prix] == (
            [bits(p_t)] + [bits(x) for x in etat.registre_prix[:12]])
        etat = suivant


# --------------------------------------------------------------------------
# Permutation des blocs d'un groupe (C97-4 ; ADR 0011, l. 74)
# --------------------------------------------------------------------------


GROUPES_A_VIRGULE = [(e.identifiant, g) for e in ETAPES for g in e.groupes
                     if len(g) > 1 and not {MOTEUR, NOYAU} & set(g)]


def test_cellules_a_virgule():
    """Toutes les cellules à virgule de tab:phases : phases 1, 2, 5, 6, 8 (b) et 9."""
    assert [e for e, _ in GROUPES_A_VIRGULE] == ["1", "2", "5", "6", "8b", "9"]


@pytest.mark.parametrize("etape, groupe", GROUPES_A_VIRGULE, ids=[e for e, _ in GROUPES_A_VIRGULE])
def test_permutation_d_un_groupe_bit_a_bit(monkeypatch, etape, groupe):
    """C97-4 : toute permutation de l'appel des blocs d'un groupe laisse les clôtures et l'état
    t + 1 identiques bit à bit, sur 4 pas dont des lignes 16 négatives et positives."""
    plans = tirer_plans(4, amplitude=3.0)
    assert {plans[t]["16"]["Pi_CB"] < 0.0 for t in range(4)} == {True, False}
    reference = Enregistreur()
    trajectoire(ordonnanceur_d_essai(plans), etat_initial(), 4, reference)
    canonique = ordo._ordre_du_groupe
    for permutation in itertools.permutations(groupe):
        def ordre(g, permutation=permutation):
            return permutation if set(g) == set(groupe) else canonique(g)
        monkeypatch.setattr(ordo, "_ordre_du_groupe", ordre)
        o = ordonnanceur_d_essai(plans)
        appels = dict(o.etapes)[etape] if etape != "9" else o.appels_de_la_phase_9
        assert tuple(d.radical for d, _ in appels if d.radical in groupe) == permutation
        releve = Enregistreur()
        trajectoire(o, etat_initial(), 4, releve)
        assert empreinte(releve.evenements) == empreinte(reference.evenements)
