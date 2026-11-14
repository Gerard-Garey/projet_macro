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
- un module par bloc (`nations.moteur.parametres.<radical>` : `production`,
  `travail`, `prix`, et `investissement` réduit à δ en J3-b ; ADR 0012,
  annotation du 13/11/2026, point 3 ; puis `banque` et `banque_centrale` en
  J3-c, ADR 0013, annotation du 14/11/2026, point 6) : déclarations `Parametre` et une
  **table** immuable dont les champs portent les mêmes noms, validée à toute
  construction (`valider_table`) ; valeurs par archétype dans `scenarios/`
  (F1, J3-e) ;
- `ensemble` : `EnsembleDesParametres`, l'ensemble immuable des tables passé à
  `assembler` et lu par les blocs par la vue (`vue.parametres.<radical>.<nom>`),
  et son instance de référence `PARAMETRES_DE_REFERENCE`.

`parametres` n'importe de `nations` que `etat.unites`, qui n'importe rien.
"""

from __future__ import annotations

import dataclasses
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


def _flottant_fini(x: object) -> bool:
    return type(x) is float and math.isfinite(x)


def domaine(texte: str, condition: Callable[[float], bool]) -> Domaine:
    """Domaine d'un paramètre `float` fini : `texte` en clair, `condition` sur la valeur.

    La condition s'écrit sous sa forme positive ; un `NaN` ou un infini est
    refusé avant elle.
    """
    return Domaine(f"float fini, {texte}", lambda x: _flottant_fini(x) and condition(x))


def vitesse(n_a: int) -> Domaine:
    """Domaine d'une vitesse d'ajustement : 0 < λ ≤ n_a (P65 ; `sec:cadre-calendrier`)."""
    return domaine(f"0 < λ ≤ n_a = {n_a} (vitesse d'ajustement, P65)",
                   lambda x: 0.0 < x <= n_a)


def vitesse_stricte(n_a: int) -> Domaine:
    """Domaine strict de λ_v : 0 < λ_v < n_a (P70)."""
    return domaine(f"0 < λ_v < n_a = {n_a}, strict (avec λ_v = n_a et d = 0, v^e = 0 et P1 "
                   "n'est pas défini au pas suivant ; P70)", lambda x: 0.0 < x < n_a)


TAUX_DE_CROISSANCE_ANNUEL = domaine("1 + x > 0 (taux de croissance)", lambda x: 1.0 + x > 0.0)


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


# --------------------------------------------------------------------------
# Tables de paramètres d'un bloc (ADR 0012, annotation du 13/11/2026, point 3)
# --------------------------------------------------------------------------

_TYPES_DE_TAUX = (TauxDeFlux, TauxDeCroissance)


def valeur_de_table(parametre: Parametre) -> float | TauxDeFlux | TauxDeCroissance:
    """Valeur d'un paramètre telle qu'une table la porte : un taux annuel sous le type de sa
    nature, lu dans son unité (`taux_du_parametre`), tout autre paramètre en `float`."""
    if parametre.unite in (UNITE_TAUX_DE_FLUX, UNITE_TAUX_DE_CROISSANCE):
        return taux_du_parametre(parametre)
    return parametre.valeur


def valider_table(table: object, declarations: tuple[Parametre, ...]) -> None:
    """Contrôle d'une table contre ses déclarations, à toute construction (`__post_init__`,
    `dataclasses.replace` compris) : champs exactement ceux des déclarations, chacun du type que
    porte son unité et dans son domaine ; hors domaine, `DefautDeDeclaration`, jamais un
    écrêtage (ADR 0011, point 2)."""
    noms = tuple(f.name for f in dataclasses.fields(table))
    if noms != tuple(p.nom for p in declarations):
        raise DefautDeDeclaration(f"champs {noms!r} : ceux des déclarations attendus, dans "
                                  "leur ordre")
    for parametre, champ in zip(declarations, dataclasses.fields(table), strict=True):
        valeur = getattr(table, champ.name)
        attendu = type(valeur_de_table(parametre))
        if type(valeur) is not attendu:
            raise DefautDeDeclaration(f"valeur {valeur!r} : {attendu.__name__} attendu (unité "
                                      f"{parametre.unite!r})", nom=parametre.nom)
        brute = valeur.valeur if attendu in _TYPES_DE_TAUX else valeur
        if not parametre.domaine.predicat(brute):
            raise DefautDeDeclaration(
                f"valeur {brute!r} hors du domaine ({parametre.domaine.texte}) : refusée, "
                "jamais écrêtée", nom=parametre.nom)


def table_des_declarations(classe: type, declarations: tuple[Parametre, ...]) -> object:
    """Table de référence : chaque champ à la valeur indicative de sa déclaration."""
    return classe(**{p.nom: valeur_de_table(p) for p in declarations})


def varier(table: object, **valeurs: float) -> object:
    """Constructeur validé des variations de test et des archétypes : la table dont les
    paramètres nommés prennent la valeur donnée (`float`), typée par l'unité de sa déclaration
    (la nature d'un taux n'est jamais choisie au site d'appel, F2) et contrôlée par son
    domaine ; un nom inconnu est refusé. Les déclarations sont celles de la classe de la table
    (attribut de classe `DECLARATIONS`)."""
    par_nom = {p.nom: p for p in type(table).DECLARATIONS}
    champs = {}
    for nom, valeur in valeurs.items():
        if nom not in par_nom:
            raise DefautDeDeclaration("paramètre inconnu de la table", nom=nom)
        champs[nom] = valeur_de_table(dataclasses.replace(par_nom[nom], valeur=valeur))
    return dataclasses.replace(table, **champs)
