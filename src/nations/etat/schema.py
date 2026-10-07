"""Schéma d'état d'un pays : variables déclarées, `EtatPays` engendré, version.

Contrat : ADR 0012, C1, D1 et D2 ; critères du rang 1b de #96 (V^flux dans
l'état, S hors de l'état). Une **variable d'état** est déclarée une fois, par
une valeur immuable `VariableEtat` (propriétaire, phase d'écriture, unité,
type, valeur stationnaire, invariance d'unité) ; `EtatPays`, dataclasse gelée à
champs tous obligatoires, est **engendrée depuis ces déclarations** : aucun
champ n'existe sans déclaration, aucun attribut ne se crée à la volée, aucun
champ n'a de valeur par défaut.

Champs de `EtatPays`, dans l'ordre :

- deux **champs d'identité**, qui ne sont pas des variables d'état (aucune
  phase ne les écrit) : `identifiant` (chaîne non vide, clé de l'ordre
  canonique des pays, comparée par point de code Unicode) et `graine` (entier
  ≥ 0, graine explicite du pays ; aucun générateur n'est tiré au J2) ;
- les variables du **moteur** : `t` (entier) et `registre_prix`, les 13
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
from dataclasses import dataclass
from enum import Enum

from nations.noyau.catalogue import NOMS_POSTES, PHASES, SECTEURS, VALEUR_NETTE_FLUX

VERSION_SCHEMA = 1

# Vocabulaire fermé des unités, **unique** pour les variables d'état et les
# paramètres (ADR 0012, F2, et annotation du 07/10/2026, point 2) : celui de
# F2, complété de « pas » (unité de t), « u.v. », « u.v. par pas » et « u.m.
# par u.v. » (unité de P_t). Une unité hors liste est un refus de déclaration ;
# les paramètres du moteur (#97) importent ce tuple.
UNITES = (
    "pas par an",
    "pas par tour",
    "sans dimension",
    "u.m.",
    "u.m. par pas",
    "par an, taux de flux",
    "par an, taux de croissance",
    "années",
    "personnes",
    "fraction",
    "pas",
    "u.v.",
    "u.v. par pas",
    "u.m. par u.v.",
)

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


def defaut_d_identite(nom: str, valeur: str | int) -> str | None:
    """Motif de refus d'un champ d'identité de bon type hors de son domaine, sinon `None`.

    Domaine (ADR 0012, annotation du 07/10/2026, point 1) : identifiant non
    vide, graine ≥ 0. Partagé par la construction et la reprise.
    """
    if nom == "identifiant" and valeur == "":
        return "identifiant vide"
    if nom == "graine" and valeur < 0:
        return f"graine négative {valeur!r} : entier ≥ 0 attendu"
    return None


def _verifier_types(etat: object) -> None:
    """Refuse un `EtatPays` dont un champ n'a pas exactement son type déclaré, ou hors domaine."""
    for nom, type_ in CHAMPS_D_IDENTITE:
        valeur = getattr(etat, nom)
        if type(valeur) is not type_:
            raise TypeError(f"EtatPays.{nom} : {type_.__name__} attendu, {valeur!r} reçu")
        motif = defaut_d_identite(nom, valeur)
        if motif is not None:
            raise ValueError(f"EtatPays.{nom} : {motif}")
    for variable in VARIABLES:
        valeur = getattr(etat, variable.nom)
        if not variable.admet(valeur):
            raise TypeError(f"EtatPays.{variable.nom} : {variable.description_du_type()} "
                            f"attendu, {valeur!r} reçu")


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
(`TypeError`), un champ d'identité hors de son domaine aussi (`ValueError`).
L'état d'un monde est une séquence d'`EtatPays` triée par identifiant, par
point de code Unicode.
"""

CHAMPS = tuple(f.name for f in dataclasses.fields(EtatPays))
