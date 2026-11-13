"""Déclaration d'une variable d'état : `VariableEtat` et son invariance d'unité.

Contrat : ADR 0012, C1. Module feuille de `etat/` (ADR 0012, annotation du
13/11/2026, point 1.5) : les modules de déclarations par radical
(`nations.etat.production`, `.travail`, `.prix`, `.banque_centrale`) et
`nations.etat.schema`, qui les assemble, l'importent sans cycle. La forme de
`VariableEtat` et d'`Invariance` est celle du schéma v1, inchangée ;
`nations.etat.schema` les réexporte.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from nations.etat.unites import UNITES
from nations.noyau.catalogue import PHASES

# Types admis d'une variable d'état (C1) : entier, flottant, ou tuple de
# flottants de longueur fixe déclarée.
TYPES = (int, float, tuple)


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


def scalaire(nom: str, proprietaire: str, phase: str, unite: str, valeur_stationnaire: str,
             invariance: Invariance) -> VariableEtat:
    """Variable d'état scalaire de type `float` (les dix variables des blocs du schéma v2)."""
    return VariableEtat(nom, proprietaire, phase, unite, float, 1, valeur_stationnaire,
                        invariance)
