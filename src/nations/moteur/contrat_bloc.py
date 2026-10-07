"""Contrat de bloc : déclaration statique et méthodes de phase.

Contrat : ADR 0012, B2 et C1. Module feuille, sans dépendance vers
l'ordonnanceur : les blocs (J3) l'importent pour se déclarer.

Un **bloc** est un objet qui expose :

- un attribut `declaration`, une `DeclarationDeBloc` immuable : son radical
  et un **siège** (`Siege`) par étape où il écrit ;
- une **méthode par étape déclarée**, nommée `methode_de_l_etape(etape)`
  (`phase_2`, `phase_8b`, `phase_9`), appelée par l'ordonnanceur avec une
  **vue** (`nations.moteur.ordonnanceur.Vue`), et qui ne rend rien.

Un siège déclare, pour une étape : les **variables du pas** que le bloc
écrit ; ses **lectures**, chacune (source, nom) ; les **lignes qu'il
propose** ; les lignes dont il est **payeur déclarant** du montant couvert
(ADR 0012, A3.2) ; les **variables d'état** dont il écrit la valeur du pas
suivant (C1, C2). Sources d'une lecture :

- `"ouverture"` : un champ de l'état d'ouverture (toujours admise) ;
- `"registre"` : une fonction de lecture du registre (`dernier_prix`,
  `glissement`, `variation_sur_le_tour` ; toujours admise) ;
- `"grand_livre"` : le montant exécuté d'une ligne (identifiant du
  catalogue), admis si l'étape de la ligne est close avant l'étape lectrice,
  ou la position courante d'un poste (toujours admise) ;
- l'identifiant d'une étape (`"0"` à `"9"`, `"8a"`…) : une variable du pas
  écrite dans cette étape (grandeur d'ouverture et entrée de scénario en
  `"0"`, levier en `"1"`, variable d'un bloc ; valeur du pas suivant d'une
  variable d'état sous le nom `<nom>_suivant`).

Un bloc n'a **aucun attribut d'instance** : `declaration` est un attribut
de classe ; les paramètres, l'état et les variables du pas arrivent par la
vue, et ce qu'il doit retenir d'un pas à l'autre est une variable d'état
déclarée. `assembler` refuse un bloc dont l'instance a un `__dict__` ou un
`__slots__` non vide dans sa hiérarchie de classes (annotation du 07/10/2026,
point 8).
"""

from __future__ import annotations

from dataclasses import dataclass

# Sources d'une lecture autres qu'une étape (B3).
OUVERTURE = "ouverture"
REGISTRE = "registre"
GRAND_LIVRE = "grand_livre"

# Lectures du registre offertes par la vue (ADR 0012, F3).
LECTURES_DU_REGISTRE = ("dernier_prix", "glissement", "variation_sur_le_tour")

# Suffixe de la valeur du pas suivant d'une variable d'état, déposée dans
# l'espace du pas à son écriture (C2).
SUFFIXE_SUIVANT = "_suivant"


def methode_de_l_etape(etape: str) -> str:
    """Nom de la méthode de bloc appelée dans une étape : `phase_<étape>`."""
    return f"phase_{etape}"


@dataclass(frozen=True, slots=True)
class Lecture:
    """Une lecture déclarée : (source, nom)."""

    source: str
    nom: str


@dataclass(frozen=True, slots=True)
class Siege:
    """Ce qu'un bloc fait dans une étape (B2) ; tous les champs sont obligatoires."""

    etape: str
    ecrit: tuple[str, ...]
    lit: tuple[Lecture, ...]
    propose: tuple[str, ...]
    couvre: tuple[str, ...]
    etat: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DeclarationDeBloc:
    """Déclaration statique d'un bloc (B2) : radical et sièges, dans l'ordre des étapes."""

    radical: str
    sieges: tuple[Siege, ...]
