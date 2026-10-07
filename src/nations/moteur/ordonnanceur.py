"""Ordonnanceur : assemblage contrôlé une fois, puis déroulement d'un pas sans état propre.

Contrat : ADR 0012, B2 à B5, C2 et C3 ; ADR 0009 (état d'ouverture figé,
couches de la phase 9, écriture unique des variables d'état) ; ADR 0011
(phase 7, sous-phase 8 (b)) ; spécification, `sec:cadre-phases`.

- `assembler(phases, blocs, parametres, entrees) → Ordonnanceur` vérifie
  **une fois**, avant le premier pas, les déclarations des blocs contre
  `PHASES` et le catalogue du noyau (B3), et refuse par `DefautDeDeclaration` :
  écrivain sans implémentation ou bloc sans siège ; siège hors des étapes du
  bloc ; bloc à attribut d'instance (`__dict__`, ou `__slots__` non vide
  dans sa hiérarchie de classes : la déclaration est un attribut de classe) ;
  ligne proposée hors de sa phase, sans proposant au socle ou par un
  autre bloc que son proposant ; ligne à proposant sans exactement un bloc
  proposant ; montant couvert hors de la liste fermée des couples ; variable
  du pas écrite deux fois ; variable d'état sans propriétaire qui l'écrive,
  à deux propriétaires, ou hors de sa phase d'écriture ; **triangularité** :
  une lecture d'une variable du pas exige qu'elle soit écrite dans une étape
  antérieure, ou dans la même étape par un groupe antérieur dans l'ordre
  « puis » (jamais le même groupe) ; une lecture du montant exécuté d'une
  ligne exige que l'étape de la ligne soit close avant l'étape lectrice ;
  **colonne « Lisent »**, normative : une variable du pas d'une autre phase
  n'est lisible que si cette phase figure parmi les phases lues de la phase
  lectrice (`Phase.lisent`), la phase 0 (ouverture) étant toujours lisible et
  la phase lectrice elle-même relevant de la seule triangularité. En
  phase 9, un bloc n'écrit que des variables d'état. L'ordre d'appel des
  blocs d'un groupe est l'ordre canonique des radicaux (`_ordre_du_groupe`),
  sans effet par construction : un groupe ne se lit pas, et le noyau exécute
  les propositions d'une étape dans l'ordre du catalogue.
- `executer_pas(etat_ouverture, entrees_du_tour, ordonnanceur, observateur)
  → etat_cloture`, fonction **sans état propre** (B5) : phase 0 (ouverture
  du grand livre, grandeurs calculées à l'ouverture, entrées de scénario) ;
  étapes 1 à 8 (c) (blocs groupe par groupe, clôture du noyau, relevé de la
  clôture) ; phase 9 par couches (clôture du noyau et relevé ; blocs du
  groupe ; couche moteur : avance du registre, assemblage de l'état t + 1,
  contrôle de l'écriture unique des variables d'état, relevé de la fin du
  pas, qui porte les variables du pas et les grandeurs calculées à
  l'ouverture dans l'ordre d'inscription à l'assemblage). L'état d'ouverture est une lecture figée (`EtatPays` gelé) ; un
  arrêt du noyau ou du moteur n'est jamais rattrapé.
- Les **variables du pas** vivent dans un espace (`VariablesDuPas`) créé à
  l'ouverture et perdu à la fin du pas (B4) : ce n'est pas l'état.
- Un bloc reçoit une **vue** (`Vue`) par appel : l'état d'ouverture, les
  paramètres, les variables du pas qu'il a déclaré lire, le grand livre en
  lecture seule, `proposer` et `declarer_montant_couvert` pour ses seules
  lignes déclarées dans l'étape (le proposant et le payeur apposés par la
  vue ; aucune en phase 9, où tout flux est refusé), les lectures du
  registre, et l'écriture de ses seules variables déclarées.

Les observateurs ne reçoivent que des valeurs immuables et sont appelés par le
moteur seul (ADR 0012, E1).
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from types import MappingProxyType

from nations.etat import schema
from nations.moteur import registre
from nations.moteur.contrat_bloc import (
    GRAND_LIVRE,
    LECTURES_DU_REGISTRE,
    OUVERTURE,
    REGISTRE,
    SUFFIXE_SUIVANT,
    DeclarationDeBloc,
    Siege,
    methode_de_l_etape,
)
from nations.moteur.diagnostics import DefautDeDeclaration, RefusDuMoteur
from nations.moteur.ouverture import GRANDEURS_OUVERTURE
from nations.moteur.phases import MOTEUR, NOYAU, Etape, Phase
from nations.noyau.catalogue import (
    COUPLES_MONTANT_COUVERT,
    LIGNE,
    LIGNES,
    LIGNES_DE_LA_PHASE,
    NOMS_POSTES,
)
from nations.noyau.catalogue import PHASES as CLOTURES_DU_NOYAU
from nations.noyau.grand_livre import FluxPropose, GrandLivre, ouvrir_pas
from nations.observation.observateur import FinDePas, Observateur

# Indice des prix du pas, P_t : variable du pas écrite par le bloc prix en
# phase 5 (ADR 0008, II.1 ; au J2, par le générateur de #98), lue par la
# couche moteur de la phase 9 pour avancer le registre (`registre.avancer`).
INDICE_DES_PRIX = "P"
ECRIVAIN_DE_L_INDICE = ("5", "prix")

# Étape des contreparties de règlement (17, 20, 22), sans phase propre au
# catalogue : leur montant du pas se lit après la dernière clôture qui
# exécute des lignes (comme au grand livre).
_ETAPE_DES_CONTREPARTIES = "8c"

# Variables d'état du moteur, que la couche moteur de la phase 9 écrit.
_VARIABLES_DU_MOTEUR = ("t", "registre_prix")

# Types de base d'une variable du pas (ADR 0012, annotation du 07/10/2026,
# point 4 : relevées sous des types qui n'importent rien de `moteur`).
_TYPES_DE_BASE = frozenset({float, int, bool})


def _ordre_du_groupe(groupe: Sequence[str]) -> tuple[str, ...]:
    """Ordre d'appel des blocs d'un groupe : ordre canonique des radicaux (B5.2)."""
    return tuple(sorted(groupe))


def _est_de_type_de_base(valeur: object) -> bool:
    if type(valeur) is tuple:
        return all(type(x) is float for x in valeur)
    return type(valeur) in _TYPES_DE_BASE


def _est_finie(valeur: object) -> bool:
    """Valeur de type de base sans NaN ni infini, éléments d'un n-uplet compris."""
    if type(valeur) is tuple:
        return all(math.isfinite(x) for x in valeur)
    return type(valeur) is not float or math.isfinite(valeur)


# --------------------------------------------------------------------------
# Entrées du tour
# --------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DeclarationDesEntrees:
    """Noms des entrées du tour, déclarés à l'assemblage (B5, G4).

    - `scenario` : entrées de scénario (ς_{L,t}, ς_{B,t} au J3), publiées en
      phase 0 ;
    - `leviers` : leviers du joueur (J4), lus par le moteur en phase 1,
      premier groupe.
    """

    scenario: tuple[str, ...]
    leviers: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EntreesDuTour:
    """Valeurs des entrées du tour, hors de l'état : (nom, valeur) dans l'ordre déclaré."""

    scenario: tuple[tuple[str, float], ...]
    leviers: tuple[tuple[str, float], ...]


def _verifier_entrees(entrees: EntreesDuTour, declaration: DeclarationDesEntrees,
                      t: int) -> None:
    """Les entrées du tour portent exactement les noms déclarés, dans l'ordre, en `float` fini."""
    if type(entrees) is not EntreesDuTour:
        raise RefusDuMoteur("entrées du tour : EntreesDuTour attendu", t=t, etape="0",
                            bloc=MOTEUR)
    for famille, valeurs, noms in (("scénario", entrees.scenario, declaration.scenario),
                                   ("leviers", entrees.leviers, declaration.leviers)):
        if tuple(nom for nom, _ in valeurs) != noms:
            raise RefusDuMoteur(f"entrées de {famille} : noms {noms!r} attendus dans l'ordre "
                                "déclaré", t=t, etape="0", bloc=MOTEUR)
        for nom, valeur in valeurs:
            if type(valeur) is not float:
                raise RefusDuMoteur(f"entrée {valeur!r} : float attendu", t=t, etape="0",
                                    bloc=MOTEUR, nom=nom)
            if not math.isfinite(valeur):
                raise RefusDuMoteur(f"entrée {valeur!r} : valeur non finie refusée", t=t,
                                    etape="0", bloc=MOTEUR, nom=nom)


# --------------------------------------------------------------------------
# Espace des variables du pas (B4)
# --------------------------------------------------------------------------


class VariablesDuPas:
    """Espace des variables du pas, à noms déclarés ; créé à l'ouverture, perdu à la fin.

    Une écriture d'un nom non déclaré, une seconde écriture du même nom, ou
    une valeur qui n'est pas de type de base fini (`float`, `int`, `bool`,
    n-uplet de `float`, sans NaN ni infini) est refusée ; une lecture d'un nom non encore écrit est refusée, jamais une
    valeur par défaut.
    """

    __slots__ = ("_declares", "_t", "_valeurs")

    def __init__(self, declares: frozenset[str], t: int) -> None:
        self._declares = declares
        self._t = t
        self._valeurs: dict[str, object] = {}

    def ecrire(self, nom: str, valeur: object) -> None:
        if nom not in self._declares:
            raise RefusDuMoteur("variable du pas non déclarée", t=self._t, nom=nom)
        if nom in self._valeurs:
            raise RefusDuMoteur("seconde écriture d'une variable du pas", t=self._t, nom=nom)
        if not _est_de_type_de_base(valeur):
            raise RefusDuMoteur(f"valeur {valeur!r} : float, int, bool ou tuple de float "
                                "attendu", t=self._t, nom=nom)
        if not _est_finie(valeur):
            raise RefusDuMoteur(f"valeur {valeur!r} : valeur non finie refusée", t=self._t,
                                nom=nom)
        self._valeurs[nom] = valeur

    def lire(self, nom: str) -> object:
        try:
            return self._valeurs[nom]
        except KeyError:
            raise RefusDuMoteur("variable du pas lue avant son écriture : refusée, jamais "
                                "une valeur par défaut", t=self._t, nom=nom) from None

    def releve(self, noms: tuple[str, ...]) -> tuple[tuple[str, object], ...]:
        """(nom, valeur) des variables écrites parmi `noms`, dans l'ordre de `noms`."""
        valeurs = self._valeurs
        return tuple((nom, valeurs[nom]) for nom in noms if nom in valeurs)


# --------------------------------------------------------------------------
# Vue d'un bloc (B2)
# --------------------------------------------------------------------------


class LectureDuGrandLivre:
    """Le grand livre du pas en lecture seule (ADR 0012, A3.3, « Lectures seules »)."""

    __slots__ = ("_livre",)

    def __init__(self, livre: GrandLivre) -> None:
        self._livre = livre

    def montant_execute(self, ligne: str, colonne: str) -> float:
        return self._livre.montant_execute(ligne, colonne)

    def montant_execute_ligne(self, ligne: str) -> float:
        return self._livre.montant_execute_ligne(ligne)

    def position(self, poste: str) -> float:
        return self._livre.position(poste)

    def ouverture(self, poste: str) -> float:
        return self._livre.ouverture(poste)

    def echelle(self, secteur: str) -> float:
        return self._livre.echelle(secteur)

    def valeur_nette_stock(self, secteur: str) -> float:
        return self._livre.valeur_nette_stock(secteur)

    def valeur_nette_flux(self, secteur: str) -> float:
        return self._livre.valeur_nette_flux(secteur)


@dataclass(frozen=True, slots=True)
class _Droits:
    """Droits d'un bloc dans une étape, arrêtés à l'assemblage."""

    radical: str
    etape: str
    lectures: frozenset[str]
    ecritures: frozenset[str]
    etat: frozenset[str]
    lignes: frozenset[str]
    couvertes: frozenset[str]


class _Pas:
    """Contexte d'un pas, créé par `executer_pas` et perdu avec lui."""

    __slots__ = ("espace", "etat", "etat_suivant", "livre", "parametres", "t", "vue_du_livre")

    def __init__(self, etat: schema.EtatPays, parametres: object, espace: VariablesDuPas,
                 livre: GrandLivre) -> None:
        self.t = etat.t
        self.etat = etat
        self.parametres = parametres
        self.espace = espace
        self.livre = livre
        self.vue_du_livre = LectureDuGrandLivre(livre)
        # Valeurs du pas suivant des variables d'état des blocs (C2).
        self.etat_suivant: dict[str, object] = {}


class Vue:
    """Ce qu'un bloc voit et peut faire dans une étape (B2), et rien d'autre."""

    __slots__ = ("_droits", "_pas")

    def __init__(self, pas: _Pas, droits: _Droits) -> None:
        self._pas = pas
        self._droits = droits

    def _refus(self, message: str, nom: str) -> RefusDuMoteur:
        d = self._droits
        return RefusDuMoteur(message, t=self._pas.t, etape=d.etape, bloc=d.radical, nom=nom)

    @property
    def ouverture(self) -> schema.EtatPays:
        """État d'ouverture du pas, figé."""
        return self._pas.etat

    @property
    def parametres(self) -> object:
        """Paramètres du moteur."""
        return self._pas.parametres

    @property
    def grand_livre(self) -> LectureDuGrandLivre:
        """Grand livre en lecture seule."""
        return self._pas.vue_du_livre

    def lire(self, nom: str) -> object:
        """Variable du pas déclarée en lecture par le bloc dans cette étape."""
        if nom not in self._droits.lectures:
            raise self._refus("lecture d'une variable du pas non déclarée", nom)
        return self._pas.espace.lire(nom)

    def ecrire_pas(self, nom: str, valeur: object) -> None:
        """Écrit une variable du pas déclarée par le bloc dans cette étape."""
        if nom not in self._droits.ecritures:
            raise self._refus("écriture d'une variable du pas non déclarée par le bloc", nom)
        self._pas.espace.ecrire(nom, valeur)

    def ecrire_etat(self, nom: str, valeur: object) -> None:
        """Écrit la valeur du pas suivant d'une variable d'état du bloc, une fois par pas (C2)."""
        if nom not in self._droits.etat:
            raise self._refus("écriture d'une variable d'état hors de son propriétaire ou de "
                              "sa phase d'écriture", nom)
        etat_suivant = self._pas.etat_suivant
        if nom in etat_suivant:
            raise self._refus("seconde écriture d'une variable d'état dans le pas", nom)
        variable = schema.VARIABLE[nom]
        if not variable.admet(valeur):
            raise self._refus(f"valeur {valeur!r} : {variable.description_du_type()} attendu", nom)
        etat_suivant[nom] = valeur
        self._pas.espace.ecrire(nom + SUFFIXE_SUIVANT, valeur)

    def _ligne_non_declaree(self, ligne: str) -> RefusDuMoteur:
        precision = " ; aucun flux en phase 9" if self._droits.etape == "9" else ""
        return self._refus("ligne non déclarée par le bloc dans cette étape" + precision, ligne)

    def proposer(self, ligne: str, montants: dict[str, float]) -> None:
        """Propose au noyau un flux d'une ligne déclarée, le bloc étant apposé comme proposant."""
        if ligne not in self._droits.lignes:
            raise self._ligne_non_declaree(ligne)
        self._pas.livre.proposer(FluxPropose(ligne, montants, self._droits.radical))

    def declarer_montant_couvert(self, ligne: str, montant: float) -> None:
        """Déclare au noyau le montant couvert d'une ligne déclarée, le bloc étant apposé comme
        payeur."""
        if ligne not in self._droits.couvertes:
            raise self._ligne_non_declaree(ligne)
        self._pas.livre.declarer_montant_couvert(ligne, montant, self._droits.radical)

    def dernier_prix(self) -> float:
        """P_{t−1}, lu sur le registre d'ouverture."""
        return registre.dernier_prix(self._pas.etat.registre_prix)

    def glissement(self) -> float:
        """π_{t−1}, lu sur le registre d'ouverture."""
        return registre.glissement(self._pas.etat.registre_prix)

    def variation_sur_le_tour(self) -> float:
        """Variation de l'indice sur le dernier tour clos, lue sur le registre d'ouverture."""
        return registre.variation_sur_le_tour(self._pas.etat.registre_prix)


# --------------------------------------------------------------------------
# Assemblage (B3)
# --------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Ordonnanceur:
    """Résultat immuable de l'assemblage ; ne change pas d'un pas à l'autre.

    - `etapes` : pour les étapes 1 à 8 (c), (identifiant, appels), un appel
      étant (droits, méthode du bloc), dans l'ordre d'exécution ;
    - `appels_de_la_phase_9` : appels des blocs du groupe de la phase 9 ;
    - `declares` : noms de toutes les variables du pas ;
    - `ordre_des_variables` : variables du pas autres que les grandeurs
      calculées à l'ouverture, dans l'ordre d'inscription (entrées de
      scénario, leviers, puis radicaux dans l'ordre canonique, sièges dans
      leur ordre, écritures puis valeurs du pas suivant) : il ne dépend pas de
      l'ordre de la liste de blocs passée à `assembler` ; c'est l'ordre du
      relevé de `FinDePas` ;
    - `variables_des_blocs` : variables d'état des blocs, dans l'ordre du schéma.
    """

    phases: tuple[Phase, ...]
    parametres: object
    entrees: DeclarationDesEntrees
    etapes: tuple[tuple[str, tuple[tuple[_Droits, object], ...]], ...]
    appels_de_la_phase_9: tuple[tuple[_Droits, object], ...]
    declares: frozenset[str]
    ordre_des_variables: tuple[str, ...]
    variables_des_blocs: tuple[str, ...]


def _defaut(message: str, *, etape: str | None = None, bloc: str | None = None,
            nom: str | None = None) -> DefautDeDeclaration:
    return DefautDeDeclaration(message, etape=etape, bloc=bloc, nom=nom)


def _structure(phases: tuple[Phase, ...]
               ) -> tuple[dict[str, int], dict[str, dict[str, int]], dict[str, Phase]]:
    """Rang de chaque étape, rang de groupe de chaque écrivain et phase de chaque étape, après
    contrôle de forme.

    Les étapes 1 à 9 sont les clôtures du noyau, dans son ordre ; `moteur`
    n'écrit qu'en phase 0, au premier groupe de la phase 1 et à la dernière
    couche de la phase 9 ; `noyau` n'écrit qu'à la première couche de la phase 9.
    """
    etapes = [etape for phase in phases for etape in phase.etapes]
    identifiants = tuple(e.identifiant for e in etapes)
    if identifiants != ("0",) + CLOTURES_DU_NOYAU:
        raise _defaut(f"étapes {identifiants!r} : phase 0 puis les clôtures du noyau "
                      f"{CLOTURES_DU_NOYAU!r} attendues")
    for etape in etapes:
        lignes = LIGNES_DE_LA_PHASE[etape.identifiant] if etape.identifiant != "0" else ()
        if etape.lignes != tuple(ligne.identifiant for ligne in lignes):
            raise _defaut(f"lignes {etape.lignes!r} : celles du catalogue attendues",
                          etape=etape.identifiant)
    rang = {e.identifiant: k for k, e in enumerate(etapes)}
    groupes: dict[str, dict[str, int]] = {}
    for etape in etapes:
        places: dict[str, int] = {}
        for g, groupe in enumerate(etape.groupes):
            for ecrivain in groupe:
                if ecrivain in places:
                    raise _defaut("écrivain cité deux fois dans l'étape", etape=etape.identifiant,
                                  bloc=ecrivain)
                places[ecrivain] = g
        for ecrivain in (MOTEUR, NOYAU):
            cle = (etape.identifiant, ecrivain)
            if (ecrivain in places) != (cle in _PLACES_DU_MOTEUR_ET_DU_NOYAU):
                raise _defaut(f"écrivain {ecrivain} hors de sa place", etape=etape.identifiant,
                              bloc=ecrivain)
            if ecrivain in places:
                attendu = _PLACES_DU_MOTEUR_ET_DU_NOYAU[cle] % len(etape.groupes)
                if places[ecrivain] != attendu or len(etape.groupes[attendu]) != 1:
                    raise _defaut(f"écrivain {ecrivain} hors de sa place",
                                  etape=etape.identifiant, bloc=ecrivain)
        groupes[etape.identifiant] = places
    phase_de = {e.identifiant: p for p in phases for e in p.etapes}
    return rang, groupes, phase_de


# Places de `moteur` et `noyau` : (étape, écrivain) → rang de groupe, seul
# dans son groupe (−1 : dernière couche). Phase 0 : ouverture ; phase 1 :
# leviers ; phase 9 : couche noyau, puis couche moteur (ADR 0009, point 2).
_PLACES_DU_MOTEUR_ET_DU_NOYAU = {("0", MOTEUR): 0, ("1", MOTEUR): 0, ("9", NOYAU): 0,
                                 ("9", MOTEUR): -1}


def _controler_lignes(par_radical: dict[str, tuple[DeclarationDeBloc, dict[str, Siege], object]]
                      ) -> None:
    """Lignes proposées dans leur phase, par leur proposant au socle, une fois ; montants
    couverts sur la liste fermée des couples (ligne, payeur), dans la phase de la ligne."""
    proposants: dict[str, list[str]] = {}
    for radical, (_, sieges, _) in par_radical.items():
        for siege in sieges.values():
            for identifiant in siege.propose:
                if identifiant not in LIGNE:
                    raise _defaut("ligne inconnue du catalogue", etape=siege.etape, bloc=radical,
                                  nom=identifiant)
                ligne = LIGNE[identifiant]
                if ligne.proposant != radical:
                    raise _defaut(f"ligne proposée par un autre bloc que son proposant au socle "
                                  f"({ligne.proposant!r})", etape=siege.etape, bloc=radical,
                                  nom=identifiant)
                if ligne.phase != siege.etape:
                    raise _defaut(f"ligne de la phase {ligne.phase} proposée hors de sa phase",
                                  etape=siege.etape, bloc=radical, nom=identifiant)
                proposants.setdefault(identifiant, []).append(radical)
            for identifiant in siege.couvre:
                if (identifiant, radical) not in COUPLES_MONTANT_COUVERT or (
                        LIGNE[identifiant].phase != siege.etape) or siege.couvre.count(
                        identifiant) != 1:
                    raise _defaut("montant couvert hors de la liste fermée des couples (ligne, "
                                  "payeur), de la phase de la ligne, ou déclaré deux fois",
                                  etape=siege.etape, bloc=radical, nom=identifiant)
    for ligne in LIGNES:
        if ligne.proposant is not None and (ligne.identifiant not in proposants or len(
                proposants[ligne.identifiant]) != 1):
            raise _defaut("ligne à proposant au socle sans exactement un bloc proposant",
                          nom=ligne.identifiant)


def _controler_lecture(source: str, nom: str, etape: str, groupe: int, lecteur: str,
                       rang: dict[str, int], ecrivains: dict[str, tuple[str, int, str]],
                       phase_de: dict[str, Phase]) -> None:
    """Une lecture déclarée (B3) : source connue et, pour une variable du pas ou le montant
    exécuté d'une ligne, triangularité ; pour une variable du pas, colonne « Lisent ».

    Une variable du pas est lisible si elle est écrite dans une étape antérieure,
    ou dans la même étape par un groupe antérieur (jamais le même groupe), et si
    sa phase est la phase 0, la phase lectrice ou l'une de ses phases lues ; le
    montant exécuté d'une ligne, si l'étape de la ligne est close avant l'étape
    lectrice ; un champ de l'ouverture, une lecture du registre et une
    position courante, toujours.
    """
    if source == OUVERTURE:
        if nom not in schema.CHAMPS:
            raise _defaut("lecture d'un champ inconnu de l'état", etape=etape, bloc=lecteur,
                          nom=nom)
    elif source == REGISTRE:
        if nom not in LECTURES_DU_REGISTRE:
            raise _defaut("lecture inconnue du registre", etape=etape, bloc=lecteur, nom=nom)
    elif source == GRAND_LIVRE:
        if nom in LIGNE:
            phase = LIGNE[nom].phase
            etape_de_la_ligne = _ETAPE_DES_CONTREPARTIES if phase is None else phase
            if not rang[etape_de_la_ligne] < rang[etape]:
                raise _defaut(f"montant exécuté de la ligne lu avant la clôture de la phase "
                              f"{etape_de_la_ligne}", etape=etape, bloc=lecteur, nom=nom)
        elif nom not in NOMS_POSTES:
            raise _defaut("lecture inconnue du grand livre", etape=etape, bloc=lecteur, nom=nom)
    elif source in rang:
        if nom not in ecrivains:
            raise _defaut("lecture d'une variable du pas que personne n'écrit", etape=etape,
                          bloc=lecteur, nom=nom)
        etape_ecrite, groupe_ecrivain, ecrivain = ecrivains[nom]
        if etape_ecrite != source:
            raise _defaut(f"variable déclarée en phase {source}, écrite en phase "
                          f"{etape_ecrite}", etape=etape, bloc=lecteur, nom=nom)
        anterieure = rang[etape_ecrite] < rang[etape] or (
            etape_ecrite == etape and groupe_ecrivain < groupe)
        if not anterieure:
            raise _defaut(f"triangularité : variable écrite par {ecrivain} en phase "
                          f"{etape_ecrite}, groupe {groupe_ecrivain}, lue en phase {etape}, "
                          f"groupe {groupe}", etape=etape, bloc=lecteur, nom=nom)
        phase_source, phase_lectrice = phase_de[source], phase_de[etape]
        if phase_source.numero not in (0, phase_lectrice.numero) + phase_lectrice.lisent:
            raise _defaut(f"phase {phase_source.numero} hors de la colonne « Lisent » de la "
                          f"phase {phase_lectrice.numero} ({phase_lectrice.lisent!r})",
                          etape=etape, bloc=lecteur, nom=nom)
    else:
        raise _defaut(f"source de lecture inconnue : {source!r}", etape=etape, bloc=lecteur,
                      nom=nom)


def _controler_attributs_d_instance(bloc: object, radical: str) -> None:
    """Aucun attribut d'instance (B2 ; annotation du 07/10/2026, point 8) : ni `__dict__`, ni
    `__slots__` non vide dans la hiérarchie de classes du bloc."""
    if hasattr(bloc, "__dict__"):
        raise _defaut("bloc à attribut d'instance (__dict__) : la déclaration est un attribut "
                      "de classe, le reste arrive par la vue", bloc=radical)
    for classe in type(bloc).__mro__:
        if classe.__dict__.get("__slots__", ()):
            raise _defaut(f"bloc à attribut d'instance (__slots__ non vide de "
                          f"{classe.__name__}) : la déclaration est un attribut de classe, le "
                          "reste arrive par la vue", bloc=radical)


def assembler(phases: tuple[Phase, ...], blocs: Sequence[object], parametres: object,
              entrees: DeclarationDesEntrees) -> Ordonnanceur:
    """Contrôle statique des déclarations, une fois, et ordonnanceur immuable (B3)."""
    rang, places, phase_de = _structure(phases)
    etapes_du_bloc: dict[str, set[str]] = {}
    for identifiant, places_de_l_etape in places.items():
        for ecrivain in places_de_l_etape:
            if ecrivain not in (MOTEUR, NOYAU):
                etapes_du_bloc.setdefault(ecrivain, set()).add(identifiant)

    # Blocs : une déclaration, un radical écrivain d'au moins une étape, un siège
    # par étape où `phases` le déclare, et la méthode de chaque siège.
    par_radical: dict[str, tuple[DeclarationDeBloc, dict[str, Siege], object]] = {}
    for bloc in blocs:
        try:
            declaration = bloc.declaration
        except AttributeError:
            raise _defaut("bloc sans déclaration") from None
        if type(declaration) is not DeclarationDeBloc:
            raise _defaut("déclaration de bloc : DeclarationDeBloc attendue")
        radical = declaration.radical
        _controler_attributs_d_instance(bloc, radical)
        if radical in par_radical:
            raise _defaut("deux blocs sous le même radical", bloc=radical)
        if radical not in etapes_du_bloc:
            raise _defaut("bloc écrivain d'aucune phase", bloc=radical)
        sieges: dict[str, Siege] = {}
        for siege in declaration.sieges:
            if type(siege) is not Siege:
                raise _defaut("siège : Siege attendu", bloc=radical)
            if siege.etape in sieges:
                raise _defaut("deux sièges dans la même étape", etape=siege.etape, bloc=radical)
            if siege.etape not in etapes_du_bloc[radical]:
                raise _defaut("siège dans une étape où tab:phases ne déclare pas le bloc",
                              etape=siege.etape, bloc=radical)
            sieges[siege.etape] = siege
        par_radical[radical] = (declaration, sieges, bloc)
    for radical, etapes in sorted(etapes_du_bloc.items()):
        if radical not in par_radical:
            raise _defaut("écrivain de tab:phases sans implémentation", bloc=radical)
        sieges = par_radical[radical][1]
        for identifiant in sorted(etapes, key=rang.__getitem__):
            if identifiant not in sieges:
                raise _defaut("étape de tab:phases sans siège du bloc", etape=identifiant,
                              bloc=radical)

    _controler_lignes(par_radical)

    # Écrivains des variables du pas : nom → (étape, rang de groupe, écrivain).
    ecrivains: dict[str, tuple[str, int, str]] = {}

    def inscrire(nom: str, etape: str, groupe: int, ecrivain: str) -> None:
        if nom in ecrivains:
            raise _defaut(f"variable du pas déjà écrite par {ecrivains[nom][2]} en phase "
                          f"{ecrivains[nom][0]}", etape=etape, bloc=ecrivain, nom=nom)
        ecrivains[nom] = (etape, groupe, ecrivain)

    for grandeur in GRANDEURS_OUVERTURE:
        inscrire(grandeur.nom, "0", 0, MOTEUR)
    for nom in entrees.scenario:
        inscrire(nom, "0", 0, MOTEUR)
    for nom in entrees.leviers:
        inscrire(nom, "1", 0, MOTEUR)

    # Variables d'état : une par propriétaire déclarant, dans sa phase d'écriture.
    variables_des_blocs = tuple(v.nom for v in schema.VARIABLES
                                if v.proprietaire not in (MOTEUR, NOYAU))
    for v in schema.VARIABLES:
        if v.proprietaire == MOTEUR and v.nom not in _VARIABLES_DU_MOTEUR:
            raise _defaut("variable d'état du moteur que la couche moteur n'écrit pas",
                          bloc=MOTEUR, nom=v.nom)
    ecrivain_d_etat: dict[str, str] = {}
    for radical, (_, sieges, _) in sorted(par_radical.items()):
        for identifiant, siege in sieges.items():
            groupe = places[identifiant][radical]
            if identifiant == "9" and siege.ecrit:
                raise _defaut("en phase 9, un bloc n'écrit que des variables d'état",
                              etape=identifiant, bloc=radical, nom=siege.ecrit[0])
            for nom in siege.ecrit:
                inscrire(nom, identifiant, groupe, radical)
            for nom in siege.etat:
                if nom not in schema.VARIABLE:
                    raise _defaut("variable d'état inconnue du schéma", etape=identifiant,
                                  bloc=radical, nom=nom)
                variable = schema.VARIABLE[nom]
                if variable.proprietaire != radical:
                    raise _defaut(f"variable d'état de {variable.proprietaire!r}, écrite par un "
                                  "autre bloc", etape=identifiant, bloc=radical, nom=nom)
                if variable.phase_ecriture != identifiant:
                    raise _defaut(f"variable d'état de la phase {variable.phase_ecriture}, "
                                  "écrite hors de sa phase", etape=identifiant, bloc=radical,
                                  nom=nom)
                if nom in ecrivain_d_etat:
                    raise _defaut("variable d'état écrite deux fois", etape=identifiant,
                                  bloc=radical, nom=nom)
                ecrivain_d_etat[nom] = radical
                inscrire(nom + SUFFIXE_SUIVANT, identifiant, groupe, radical)
    for nom in variables_des_blocs:
        if nom not in ecrivain_d_etat:
            raise _defaut("variable d'état sans propriétaire qui l'écrive", nom=nom)

    # Triangularité, lecture par lecture ; la couche moteur de la phase 9 lit
    # l'indice des prix du pas.
    droits: dict[tuple[str, str], _Droits] = {}
    for radical, (_, sieges, _) in sorted(par_radical.items()):
        for identifiant, siege in sieges.items():
            groupe = places[identifiant][radical]
            lectures = set()
            for lecture in siege.lit:
                _controler_lecture(lecture.source, lecture.nom, identifiant, groupe,
                                   radical, rang, ecrivains, phase_de)
                if lecture.source in rang:
                    lectures.add(lecture.nom)
            droits[(radical, identifiant)] = _Droits(
                radical, identifiant, frozenset(lectures), frozenset(siege.ecrit),
                frozenset(siege.etat), frozenset(siege.propose), frozenset(siege.couvre))
    _controler_lecture(ECRIVAIN_DE_L_INDICE[0], INDICE_DES_PRIX, "9", places["9"][MOTEUR],
                       MOTEUR, rang, ecrivains, phase_de)
    if ecrivains[INDICE_DES_PRIX][2] != ECRIVAIN_DE_L_INDICE[1]:
        raise _defaut(f"indice des prix écrit par {ecrivains[INDICE_DES_PRIX][2]}, attendu de "
                      f"{ECRIVAIN_DE_L_INDICE[1]}", nom=INDICE_DES_PRIX)

    # Appels, étape par étape, groupe par groupe, dans l'ordre canonique.
    def appels(etape: Etape, identifiant: str) -> tuple[tuple[_Droits, object], ...]:
        rendus = []
        for groupe in etape.groupes:
            for radical in _ordre_du_groupe(groupe):
                if radical in (MOTEUR, NOYAU):
                    continue
                bloc = par_radical[radical][2]
                try:
                    methode = getattr(bloc, methode_de_l_etape(identifiant))
                except AttributeError:
                    raise _defaut(f"méthode {methode_de_l_etape(identifiant)} absente",
                                  etape=identifiant, bloc=radical) from None
                if not callable(methode):
                    raise _defaut("méthode de phase non appelable", etape=identifiant,
                                  bloc=radical)
                rendus.append((droits[(radical, identifiant)], methode))
        return tuple(rendus)

    etapes_executees = []
    appels_9: tuple[tuple[_Droits, object], ...] = ()
    for phase in phases:
        for etape in phase.etapes:
            if etape.identifiant == "0":
                continue
            if etape.identifiant == "9":
                appels_9 = appels(etape, "9")
            else:
                etapes_executees.append((etape.identifiant, appels(etape, etape.identifiant)))
    # Ordre du relevé : ordre d'inscription, grandeurs d'ouverture à part.
    grandeurs = {grandeur.nom for grandeur in GRANDEURS_OUVERTURE}
    ordre_des_variables = tuple(nom for nom in ecrivains if nom not in grandeurs)
    return Ordonnanceur(tuple(phases), parametres, entrees, tuple(etapes_executees), appels_9,
                        frozenset(ecrivains), ordre_des_variables, variables_des_blocs)


# --------------------------------------------------------------------------
# Déroulement d'un pas (B5)
# --------------------------------------------------------------------------


def executer_pas(etat_ouverture: schema.EtatPays, entrees_du_tour: EntreesDuTour,
                 ordonnanceur: Ordonnanceur, observateur: Observateur) -> schema.EtatPays:
    """Déroule le pas t et rend l'état d'ouverture du pas t + 1 (B5).

    Fonction sans état propre : le résultat ne dépend que de l'état
    d'ouverture, des entrées du tour et de l'ordonnanceur. Aucun arrêt n'est
    rattrapé ; l'état d'ouverture, gelé, reste intact.
    """
    o = ordonnanceur
    t = etat_ouverture.t
    # Phase 0 : ouverture du grand livre (lecture figée, échelles, domaines de
    # l'état chargé), grandeurs calculées à l'ouverture, entrées de scénario.
    livre = ouvrir_pas(etat_ouverture, o.parametres)
    espace = VariablesDuPas(o.declares, t)
    pas = _Pas(etat_ouverture, o.parametres, espace, livre)
    grandeurs: dict[str, object] = {}
    lecture_des_grandeurs = MappingProxyType(grandeurs)
    for grandeur in GRANDEURS_OUVERTURE:
        valeur = grandeur.fonction(etat_ouverture, o.parametres, lecture_des_grandeurs)
        espace.ecrire(grandeur.nom, valeur)
        grandeurs[grandeur.nom] = valeur
    _verifier_entrees(entrees_du_tour, o.entrees, t)
    for nom, valeur in entrees_du_tour.scenario:
        espace.ecrire(nom, valeur)
    # Phase 1, premier groupe : le moteur lit les leviers ; rien ne s'exécute
    # entre la phase 0 et lui.
    for nom, valeur in entrees_du_tour.leviers:
        espace.ecrire(nom, valeur)
    # Étapes 1 à 8 (c) : blocs groupe par groupe, puis clôture et relevé.
    for identifiant, appels in o.etapes:
        for droits, methode in appels:
            methode(Vue(pas, droits))
        observateur.relever(livre.clore_phase(identifiant))
    # Phase 9 : couche noyau, puis le groupe des blocs, puis la couche moteur.
    observateur.relever(livre.clore_phase("9"))
    for droits, methode in o.appels_de_la_phase_9:
        methode(Vue(pas, droits))
    registre_suivant = registre.avancer(etat_ouverture.registre_prix,
                                        espace.lire(INDICE_DES_PRIX))
    cloture = livre.clore_pas()
    champs = {"identifiant": etat_ouverture.identifiant, "graine": etat_ouverture.graine,
              "t": cloture.t, "registre_prix": registre_suivant}
    champs.update(cloture.variables)
    etat_suivant = pas.etat_suivant
    for nom in o.variables_des_blocs:
        if nom not in etat_suivant:
            raise RefusDuMoteur("variable d'état non écrite par son propriétaire dans le pas",
                                t=t, etape="9", bloc=MOTEUR, nom=nom)
        champs[nom] = etat_suivant[nom]
    etat_cloture = schema.EtatPays(**champs)
    observateur.relever(FinDePas(
        t, etat_cloture, espace.releve(o.ordre_des_variables),
        tuple((grandeur.nom, grandeurs[grandeur.nom]) for grandeur in GRANDEURS_OUVERTURE)))
    return etat_cloture
