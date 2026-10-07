"""Schéma d'état d'un pays : variables déclarées, `EtatPays` engendré, version.

Contrat : ADR 0012, C1, D1 et D2 ; critères du rang 1b de #96 (V^flux dans
l'état, S hors de l'état). Une **variable d'état** est déclarée une fois, par
une valeur immuable `VariableEtat` (propriétaire, phase d'écriture, unité,
type, valeur stationnaire, invariance d'unité) ; `EtatPays`, dataclasse gelée à
champs tous obligatoires, est **engendrée depuis ces déclarations** : aucun
champ n'existe sans déclaration, aucun attribut ne se crée à la volée, aucun
champ n'a de valeur par défaut.

Le vocabulaire des unités est celui de `nations.etat.unites`.

Champs de `EtatPays`, dans l'ordre :

- deux **champs d'identité**, qui ne sont pas des variables d'état (aucune
  phase ne les écrit) : `identifiant` (chaîne non vide, encodable en UTF-8,
  en forme normale NFC, sans caractère de contrôle, de format ni séparateur
  de ligne ou de paragraphe, sans espace de bord ; clé de l'ordre canonique
  des pays, comparée par point de code Unicode) et `graine` (entier de
  [0 ; 2^64[, graine explicite du pays ; aucun générateur n'est tiré au J2) ;
- les variables du **moteur** : `t` (entier de [0 ; 2^63[) et `registre_prix`, les 13
  niveaux P_{t−1}, …, P_{t−13} de l'indice des prix à l'ouverture du pas t,
  en u.m. par u.v. (spécification, P4), `registre_prix[u − 1]` = P_{t−u}
  (ADR 0008, II.3) ; ensemble, l'**empreinte
  calendaire**, 14 variables (ADR 0008, II.4) ;
- les variables du **noyau** : les onze positions de `catalogue.POSTES` et les
  cinq V^flux de `catalogue.VALEUR_NETTE_FLUX`, en u.m.

L'échelle S des bilans n'est pas dans l'état : c'est une grandeur dérivée,
recalculée à l'ouverture de chaque pas, reprise comprise (C96-2). Aucun
historique, aucune série, aucun compteur hors de t : les séries relèvent de
`nations.observation`. Les variables des blocs s'ajoutent au J3, chacune par
sa déclaration (ADR 0012, G1), avec une nouvelle version du schéma.

Journal des versions (D2 : la version est incrémentée à tout changement de la
liste des champs, d'un type, d'une unité ou d'une sémantique) :

- **1** (07/10/2026, #96, ADR 0012, C1, D1, D2) : identifiant, graine, t,
  registre de 13 niveaux, onze positions, cinq V^flux.
"""

from __future__ import annotations

import dataclasses
import unicodedata
from dataclasses import dataclass
from enum import Enum

from nations.etat.unites import UNITES
from nations.noyau.catalogue import NOMS_POSTES, PHASES, SECTEURS, VALEUR_NETTE_FLUX

VERSION_SCHEMA = 1

# Types admis d'une variable d'état (C1) : entier, flottant, ou tuple de
# flottants de longueur fixe déclarée.
TYPES = (int, float, tuple)

# Longueur du registre de l'indice des prix : n_a + 1 niveaux (ADR 0008, II.3).
NIVEAUX_DU_REGISTRE = 13


class Invariance(Enum):
    """Invariance d'unité d'une variable (C1) : ce que fait une redénomination ×100.

    - `NOMINAL` : multipliée par 100 ;
    - `SANS_DIMENSION`, `VOLUME` : inchangée ;
    - `INDICE` : multipliée par 100, et comparée par le critère relatif du
      glissement (ADR 0008 ; ADR 0012, annotation du 07/10/2026, point 2).
    """

    NOMINAL = "nominal"
    SANS_DIMENSION = "sans_dimension"
    VOLUME = "volume"
    INDICE = "indice"


@dataclass(frozen=True, slots=True)
class VariableEtat:
    """Déclaration d'une variable d'état (ADR 0012, C1).

    - `nom` : nom du champ de `EtatPays` et clé de la sauvegarde ;
    - `proprietaire` : `noyau`, `moteur` ou le radical d'un bloc ; seul à
      écrire la valeur du pas suivant, une fois par pas ;
    - `phase_ecriture` : clôture où elle est écrite (`catalogue.PHASES`) ;
    - `unite` : dans `UNITES` ;
    - `type` : `int`, `float` ou `tuple` (de `float`) ;
    - `longueur` : nombre de scalaires, 1 pour un scalaire, la longueur
      déclarée pour un tuple ;
    - `valeur_stationnaire` : formule ou renvoi ; l'état résolu (J3) la fournit ;
    - `invariance` : comportement sous une redénomination ×100.
    """

    nom: str
    proprietaire: str
    phase_ecriture: str
    unite: str
    type: type
    longueur: int
    valeur_stationnaire: str
    invariance: Invariance

    def __post_init__(self) -> None:
        if not self.nom.isidentifier() or not self.nom.isascii():
            raise ValueError(f"nom de variable d'état invalide : {self.nom!r}")
        if not self.proprietaire:
            raise ValueError(f"variable d'état sans propriétaire : {self.nom}")
        if self.phase_ecriture not in PHASES:
            raise ValueError(f"{self.nom} : phase d'écriture {self.phase_ecriture!r} inconnue")
        if self.unite not in UNITES:
            raise ValueError(f"{self.nom} : unité {self.unite!r} hors du vocabulaire")
        if self.type not in TYPES:
            raise ValueError(f"{self.nom} : type {self.type!r} non admis")
        if type(self.longueur) is not int or self.longueur < 1 or (
                self.type is not tuple and self.longueur != 1):
            raise ValueError(f"{self.nom} : longueur {self.longueur!r} invalide")
        if type(self.invariance) is not Invariance:
            raise ValueError(f"{self.nom} : invariance {self.invariance!r} invalide")

    def description_du_type(self) -> str:
        """Type déclaré, en clair (diagnostics)."""
        if self.type is tuple:
            return f"tuple de {self.longueur} float"
        return self.type.__name__

    def admet(self, valeur: object) -> bool:
        """Vrai si la valeur a exactement le type déclaré (ni booléen, ni scalaire NumPy)."""
        if self.type is tuple:
            return type(valeur) is tuple and len(valeur) == self.longueur and all(
                type(x) is float for x in valeur)
        return type(valeur) is self.type


# Variables du moteur : l'empreinte calendaire (ADR 0008, II.4 ; ADR 0012, C1).
VARIABLES_MOTEUR = (
    VariableEtat("t", "moteur", "9", "pas", int, 1,
                 "0 à l'état initial résolu, puis t + 1 à chaque pas", Invariance.SANS_DIMENSION),
    VariableEtat("registre_prix", "moteur", "9", "u.m. par u.v.", tuple, NIVEAUX_DU_REGISTRE,
                 "P_{t−u} = P_t (1 + π̄)^{−u/n_a}, u = 1, …, 13 (ADR 0008, II.3)",
                 Invariance.INDICE),
)

# Variables du noyau : onze positions et cinq V^flux, nominales, écrites en
# phase 9 (ADR 0012, A5 et C1 ; C96-1).
VARIABLES_NOYAU = tuple(
    VariableEtat(nom, "noyau", "9", "u.m.", float, 1,
                 "position de l'état initial résolu (J3, scenarios/)", Invariance.NOMINAL)
    for nom in NOMS_POSTES
) + tuple(
    VariableEtat(VALEUR_NETTE_FLUX[s], "noyau", "9", "u.m.", float, 1,
                 f"V par le stock du secteur {s} à l'état initial résolu", Invariance.NOMINAL)
    for s in SECTEURS
)

# Le schéma : toutes les déclarations, dans l'ordre des champs de `EtatPays`.
VARIABLES = VARIABLES_MOTEUR + VARIABLES_NOYAU
VARIABLE = {v.nom: v for v in VARIABLES}

# Champs d'identité du pays, avant les variables d'état (D1).
CHAMPS_D_IDENTITE = (("identifiant", str), ("graine", int))

if len(VARIABLE) != len(VARIABLES) or set(VARIABLE) & {n for n, _ in CHAMPS_D_IDENTITE}:
    raise ValueError("schéma d'état : nom de variable en double")

_ANNOTATIONS = {int: int, float: float, tuple: tuple[float, ...]}
_NOMS_D_IDENTITE = frozenset(n for n, _ in CHAMPS_D_IDENTITE)

# Bornes déclarées des champs entiers (décision du mainteneur du 07/10/2026,
# constat N-2 de l'audit de #96 ; ADR 0012, annotation du 07/10/2026, point 1) :
# graine dans [GRAINE_MINIMALE ; GRAINE_EXCLUE[, t dans [T_MINIMAL ; T_EXCLU[.
# La borne haute de la graine tient aussi le document de sauvegarde loin de la
# limite de conversion des entiers de Python (4 300 chiffres) : une graine de
# 2^64 − 1 s'écrit en 20 chiffres.
GRAINE_MINIMALE = 0
GRAINE_EXCLUE = 2**64
T_MINIMAL = 0
# Borne haute de t, exclue (décision du mainteneur du 07/10/2026, constat C-1
# de l'audit de 1f8917a sur #96) : t dans [0 ; 2^63[, 2^63 − 1 admis.
T_EXCLU = 2**63

# Catégories Unicode refusées à toute position d'un identifiant (décision du
# mainteneur du 07/10/2026 sur #96) : contrôle (`Cc`), format (`Cf`, dont
# U+200B et U+202E), séparateurs de ligne (`Zl`) et de paragraphe (`Zp`).
_CATEGORIES_REFUSEES = {"Cc": "de contrôle", "Cf": "de format",
                        "Zl": "séparateur de ligne", "Zp": "séparateur de paragraphe"}

# Au-delà de ce nombre de bits, un entier est décrit par sa taille dans un
# diagnostic, jamais écrit : son `repr` échouerait au-delà de 4 300 chiffres.
_BITS_ECRITS = 128


def _entier_en_clair(valeur: int) -> str:
    """Entier écrit tel quel s'il est court, sinon décrit par son nombre de bits."""
    if valeur.bit_length() <= _BITS_ECRITS:
        return repr(valeur)
    return f"{'-' if valeur < 0 else ''}entier de {valeur.bit_length()} bits"


def _valeur_en_clair(valeur: object) -> str:
    """Valeur reçue, écrite pour un diagnostic : entiers par `_entier_en_clair`, tuples et
    listes élément par élément, le reste par son `repr`."""
    if isinstance(valeur, int):
        return _entier_en_clair(valeur)
    if type(valeur) in (tuple, list):
        elements = ", ".join(_valeur_en_clair(x) for x in valeur)
        if type(valeur) is list:
            return f"[{elements}]"
        return f"({elements},)" if len(valeur) == 1 else f"({elements})"
    return repr(valeur)


def defaut_d_identite(nom: str, valeur: str | int) -> str | None:
    """Motif de refus d'un champ d'identité de bon type hors de son domaine, sinon `None`.

    Domaine (ADR 0012, annotation du 07/10/2026, point 1 ; décision du
    mainteneur du 07/10/2026, constats N-1 et N-2, puis complément du même
    jour) : identifiant non vide, encodable en UTF-8 (aucun substitut isolé),
    sans caractère de catégorie Unicode `Cc`, `Cf`, `Zl` ou `Zp` à aucune
    position, sans espace de bord (`str.isspace`), en forme normale NFC
    (`unicodedata.normalize("NFC", x) == x`) ; graine dans [0 ; 2^64[.
    Partagé par la construction et la reprise.
    """
    if nom == "identifiant":
        if valeur == "":
            return "identifiant vide"
        try:
            valeur.encode("utf-8")
        except UnicodeEncodeError:
            return f"identifiant {valeur!r} non encodable en UTF-8 (substitut isolé)"
        for c in valeur:
            categorie = unicodedata.category(c)
            if categorie in _CATEGORIES_REFUSEES:
                return (f"identifiant {valeur!r} avec un caractère "
                        f"{_CATEGORIES_REFUSEES[categorie]} (U+{ord(c):04X}, {categorie})")
        if valeur != valeur.strip():
            return f"identifiant {valeur!r} avec un espace de bord"
        if unicodedata.normalize("NFC", valeur) != valeur:
            return f"identifiant {valeur!r} hors de la forme normale NFC"
    if nom == "graine":
        if valeur < GRAINE_MINIMALE:
            return (f"graine négative {_entier_en_clair(valeur)} : entier de "
                    "[0 ; 2^64[ attendu")
        if valeur >= GRAINE_EXCLUE:
            return (f"graine {_entier_en_clair(valeur)} ≥ 2^64 : entier de "
                    "[0 ; 2^64[ attendu")
    return None


def defaut_de_t(valeur: int) -> str | None:
    """Motif de refus d'un `t` entier hors de son domaine [0 ; 2^63[, sinon `None`."""
    if valeur < T_MINIMAL:
        return f"t négatif {_entier_en_clair(valeur)} : entier de [0 ; 2^63[ attendu"
    if valeur >= T_EXCLU:
        return f"t {_entier_en_clair(valeur)} ≥ 2^63 : entier de [0 ; 2^63[ attendu"
    return None


def defaut_de_domaine(nom: str, valeur: object) -> str | None:
    """Motif de refus d'un champ de bon type hors de son domaine, sinon `None`.

    Seule fonction de domaine de `EtatPays`, appelée par la construction et par
    la reprise : champs d'identité (`defaut_d_identite`) et `t` (`defaut_de_t`) ;
    les autres champs n'ont pas de domaine au-delà de leur type.
    """
    if nom in _NOMS_D_IDENTITE:
        return defaut_d_identite(nom, valeur)
    if nom == "t":
        return defaut_de_t(valeur)
    return None


def _verifier_types(etat: object) -> None:
    """Refuse un `EtatPays` dont un champ n'a pas exactement son type déclaré, ou hors domaine."""
    for nom, type_ in CHAMPS_D_IDENTITE:
        valeur = getattr(etat, nom)
        if type(valeur) is not type_:
            raise TypeError(f"EtatPays.{nom} : {type_.__name__} attendu, "
                            f"{_valeur_en_clair(valeur)} reçu")
        motif = defaut_de_domaine(nom, valeur)
        if motif is not None:
            raise ValueError(f"EtatPays.{nom} : {motif}")
    for variable in VARIABLES:
        valeur = getattr(etat, variable.nom)
        if not variable.admet(valeur):
            raise TypeError(f"EtatPays.{variable.nom} : {variable.description_du_type()} "
                            f"attendu, {_valeur_en_clair(valeur)} reçu")
        motif = defaut_de_domaine(variable.nom, valeur)
        if motif is not None:
            raise ValueError(f"EtatPays.{variable.nom} : {motif}")


EtatPays = dataclasses.make_dataclass(
    "EtatPays",
    [(nom, type_) for nom, type_ in CHAMPS_D_IDENTITE]
    + [(v.nom, _ANNOTATIONS[v.type]) for v in VARIABLES],
    frozen=True,
    slots=True,
    namespace={"__post_init__": _verifier_types},
    module=__name__,
)
EtatPays.__doc__ = """État d'un pays à l'ouverture d'un pas (ADR 0012, D1), gelé.

Champs engendrés depuis `CHAMPS_D_IDENTITE` et `VARIABLES`, tous obligatoires,
sans valeur par défaut ; un champ de type faux est refusé à la construction
(`TypeError`), un champ hors de son domaine aussi (`ValueError`, par
`defaut_de_domaine` : identifiant, graine, t).
L'état d'un monde est une séquence d'`EtatPays` triée par identifiant, par
point de code Unicode.
"""

CHAMPS = tuple(f.name for f in dataclasses.fields(EtatPays))
