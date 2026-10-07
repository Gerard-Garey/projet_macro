"""Paramètres typés : une valeur immuable par paramètre, avec unité, source et étiquette.

Contrat : ADR 0012, F1 et F2 ; ADR 0005, point 18 ; ADR 0008, I.3. Un
**paramètre** (`Parametre`) porte son nom, son symbole, sa valeur, son unité
(vocabulaire fermé `nations.etat.unites.UNITES`), sa source (décision M-n,
issue), les labels `eq:` des équations qui l'emploient et son **domaine**,
vérifié à la construction : une valeur hors domaine est un refus
(`DefautDeDeclaration`), jamais un écrêtage (ADR 0011, point 2).

**L'unité porte la nature, le type porte la conversion** (F2). Un taux annuel
est déclaré « par an, taux de flux » ou « par an, taux de croissance » ;
`taux_du_parametre` en rend la valeur sous l'un de deux types distincts,
`TauxDeFlux` ou `TauxDeCroissance`, construits depuis l'unité, et chacune des
deux conversions de `nations.moteur.conversions` n'accepte que le sien :
aucune fonction ne prend la nature en argument.

Modules :
- `cadre` : les quatre paramètres du cadre (n_a, n_m, ε, ε_V) et `CADRE`,
  valeur immuable qui les porte sous leur nom (lue par le noyau) ;
- au J3, un module par bloc (`nations.moteur.parametres.<radical>`), valeurs
  par archétype dans `scenarios/` (F1).

`parametres` n'importe de `nations` que `etat.unites`, qui n'importe rien.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass

from nations.etat.unites import UNITES
from nations.moteur.diagnostics import DefautDeDeclaration

# Unités des deux natures de taux annuel (F2).
UNITE_TAUX_DE_FLUX = "par an, taux de flux"
UNITE_TAUX_DE_CROISSANCE = "par an, taux de croissance"

# Préfixe d'un label d'équation (`CONVENTIONS.md` § 2.1).
_PREFIXE_DE_LABEL = "eq:"


@dataclass(frozen=True, slots=True)
class Domaine:
    """Domaine d'un paramètre : texte affiché dans le diagnostic, prédicat vérifié."""

    texte: str
    predicat: Callable[[object], bool]


def _entier_au_moins_un(x: object) -> bool:
    return type(x) is int and x >= 1


def _flottant_fini_positif(x: object) -> bool:
    return type(x) is float and math.isfinite(x) and x > 0.0


ENTIER_STRICTEMENT_POSITIF = Domaine("entier ≥ 1", _entier_au_moins_un)
FLOTTANT_STRICTEMENT_POSITIF = Domaine("float fini > 0", _flottant_fini_positif)


@dataclass(frozen=True, slots=True)
class TauxDeFlux:
    """Taux annuel de flux (intérêt, flux annuel, vitesse d'ajustement), par an.

    Converti au pas par la seule conversion linéaire (`conversions.par_pas`).
    """

    valeur: float

    def __post_init__(self) -> None:
        if type(self.valeur) is not float or not math.isfinite(self.valeur):
            raise DefautDeDeclaration(f"taux de flux {self.valeur!r} : float fini attendu")


@dataclass(frozen=True, slots=True)
class TauxDeCroissance:
    """Taux annuel de croissance ou d'inflation d'un niveau, par an.

    Converti au pas par la seule conversion géométrique
    (`conversions.facteur_par_pas`) ; domaine : 1 + x > 0.
    """

    valeur: float

    def __post_init__(self) -> None:
        if type(self.valeur) is not float or not math.isfinite(self.valeur) or not (
                1.0 + self.valeur > 0.0):
            raise DefautDeDeclaration(
                f"taux de croissance {self.valeur!r} : float fini avec 1 + x > 0 attendu")


@dataclass(frozen=True, slots=True)
class Parametre:
    """Un paramètre typé (ADR 0012, F1), immuable.

    - `nom` : identifiant ASCII (`pas_par_an`) ;
    - `symbole` : symbole de la spécification (`n_a`) ;
    - `valeur` : `int` ou `float`, dans le domaine ;
    - `unite` : dans `UNITES` ;
    - `source` : décision M-n, issue ;
    - `etiquettes` : labels `eq:` des équations qui l'emploient, au moins un ;
    - `domaine` : prédicat vérifié à la construction.
    """

    nom: str
    symbole: str
    valeur: int | float
    unite: str
    source: str
    etiquettes: tuple[str, ...]
    domaine: Domaine

    def __post_init__(self) -> None:
        if not self.nom.isidentifier() or not self.nom.isascii():
            raise DefautDeDeclaration("nom de paramètre invalide", nom=self.nom)
        if self.unite not in UNITES:
            raise DefautDeDeclaration(f"unité {self.unite!r} hors du vocabulaire", nom=self.nom)
        if not self.source:
            raise DefautDeDeclaration("paramètre sans source", nom=self.nom)
        if type(self.etiquettes) is not tuple or not self.etiquettes or not all(
                type(e) is str and e.startswith(_PREFIXE_DE_LABEL) for e in self.etiquettes):
            raise DefautDeDeclaration(
                f"étiquettes {self.etiquettes!r} : au moins un label eq: attendu", nom=self.nom)
        if not self.domaine.predicat(self.valeur):
            raise DefautDeDeclaration(
                f"valeur {self.valeur!r} hors du domaine ({self.domaine.texte}) : refusée, "
                "jamais écrêtée", nom=self.nom)


def taux_du_parametre(parametre: Parametre) -> TauxDeFlux | TauxDeCroissance:
    """Valeur d'un taux annuel sous le type de sa nature, lue dans son unité (F2).

    Un paramètre dont l'unité n'est pas un taux annuel est refusé.
    """
    if parametre.unite == UNITE_TAUX_DE_FLUX:
        return TauxDeFlux(parametre.valeur)
    if parametre.unite == UNITE_TAUX_DE_CROISSANCE:
        return TauxDeCroissance(parametre.valeur)
    raise DefautDeDeclaration(f"unité {parametre.unite!r} : pas un taux annuel",
                              nom=parametre.nom)
