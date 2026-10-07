"""Déclaration statique des phases d'un pas : transcription unique de `tab:phases`.

Contrat : ADR 0012, B1 ; ADR 0007 (ordre de la phase 4), ADR 0009 (couches de
la phase 9), ADR 0011 (phase 7 à écrivain unique, sous-phase 8 (b) sans
ordre, ordre de la phase 1) ; spécification, `sec:cadre-phases` et
`tab:phases`, qui font foi. Un test relit `tab:phases` par le lecteur
d'`outils/verifier_matrices.py` et compare à `PHASES` écrivains, groupes,
ordre, sous-phases, couches, lignes et phases lues.

`PHASES` : dix phases (0 à 9). Chacune a une ou plusieurs **étapes** (une
seule hors de la phase 8 ; trois sous-phases ordonnées, `"8a"`, `"8b"`,
`"8c"`, en phase 8). Une étape porte ses **écrivains** sous forme d'une
séquence de **groupes** : un groupe est un ensemble de blocs sans lecture
mutuelle (virgule de `tab:phases`), la séquence est l'ordre « puis ». En
phase 9, les groupes sont des couches : `noyau`, puis les blocs, puis
`moteur`. Les écrivains sont nommés par le radical de leur module, plus
`moteur` et `noyau` (`LIBELLES`).

Les **lignes** d'une étape ne sont pas recopiées : elles sont lues dans le
catalogue du noyau (`catalogue.LIGNES_DE_LA_PHASE`), seule source (ADR 0012,
A1) ; le test les compare à la colonne « Lignes » de la table.

Les **phases lues** (`lisent`, colonne « Lisent ») sont normatives :
`assembler` refuse une lecture d'une variable du pas écrite dans une phase
qui n'y figure pas (hors phase 0 et phase lectrice elle-même), décision du
mainteneur du 07/10/2026.
"""

from __future__ import annotations

from dataclasses import dataclass

from nations.noyau.catalogue import LIGNES_DE_LA_PHASE

# Radicaux des blocs de la spécification (`CONVENTIONS.md` § 2.1).
RADICAUX_DES_BLOCS = (
    "production", "travail", "prix", "menages", "investissement",
    "banque", "banque_centrale", "finances_publiques",
)
# Écrivains qui ne sont pas des blocs.
MOTEUR = "moteur"
NOYAU = "noyau"

# Correspondance unique radical ↔ libellé de la colonne « Écrivent » de
# `tab:phases`.
LIBELLES = {
    "production": "production",
    "travail": "travail",
    "prix": "prix",
    "menages": "ménages",
    "investissement": "investissement",
    "banque": "banque",
    "banque_centrale": "banque centrale",
    "finances_publiques": "État",
    MOTEUR: "moteur",
    NOYAU: "noyau",
}


@dataclass(frozen=True, slots=True)
class Etape:
    """Une phase, ou une sous-phase de la phase 8 : identifiant, groupes, lignes.

    - `identifiant` : `"0"` à `"9"`, `"8a"`, `"8b"`, `"8c"` ;
    - `groupes` : écrivains, groupe par groupe dans l'ordre « puis », chaque
      groupe dans l'ordre de la table ;
    - `lignes` : identifiants du catalogue exécutés à la clôture de l'étape.
    """

    identifiant: str
    groupes: tuple[tuple[str, ...], ...]
    lignes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Phase:
    """Une phase de `tab:phases` : numéro, nom, étapes, phases lues (numéros)."""

    numero: int
    nom: str
    etapes: tuple[Etape, ...]
    lisent: tuple[int, ...]


def _etape(identifiant: str, *groupes: tuple[str, ...]) -> Etape:
    """Étape dont les lignes sont celles du catalogue (aucune en phase 0)."""
    lignes = LIGNES_DE_LA_PHASE[identifiant] if identifiant != "0" else ()
    return Etape(identifiant, groupes, tuple(ligne.identifiant for ligne in lignes))


PHASES = (
    Phase(0, "Ouverture", (_etape("0", (MOTEUR,)),), ()),
    Phase(1, "Décision", (_etape("1", (MOTEUR,), ("travail", "banque_centrale")),), ()),
    Phase(2, "Plans",
          (_etape("2", ("production", "menages", "investissement", "finances_publiques")),),
          (1,)),
    Phase(3, "Crédit", (_etape("3", ("investissement",)),), (2,)),
    Phase(4, "Production et travail", (_etape("4", ("travail",), ("production",)),),
          (1, 2, 3)),
    Phase(5, "Marché des biens",
          (_etape("5", ("prix",), ("production",),
                  ("menages", "investissement", "finances_publiques")),),
          (2, 4)),
    # Phase 2 lue : l'impôt des ménages et les transferts, planifiés en phase 2,
    # sont proposés en phase 6 (`sec:finances_publiques-impots` ; décision du
    # 07/10/2026 ; `tab:phases` à corriger au rang 6).
    Phase(6, "Revenus et impôts",
          (_etape("6", ("finances_publiques", "banque", "investissement")),), (1, 2, 3, 4, 5)),
    # Écrivain unique, aucun ordre interne (ADR 0011).
    Phase(7, "Titres publics", (_etape("7", ("finances_publiques",)),), (1, 4, 5, 6)),
    # Trois sous-phases ordonnées ; en 8 (b), banque centrale et État ne se
    # lisent pas (ADR 0011, P1).
    Phase(8, "Monnaie centrale",
          (_etape("8a", ("banque_centrale",)),
           _etape("8b", ("banque_centrale", "finances_publiques")),
           _etape("8c", ("banque",))),
          (1, 2, 3, 4, 5, 6, 7)),
    # Couches : noyau, puis le groupe des blocs, puis moteur (ADR 0009).
    Phase(9, "Clôture", (_etape("9", (NOYAU,), ("menages", "investissement"), (MOTEUR,)),),
          (1, 2, 3, 4, 5, 6, 7, 8)),
)

# Étapes dans l'ordre d'exécution : une écriture d'une étape antérieure est
# lisible (triangularité, B3).
ETAPES = tuple(etape for phase in PHASES for etape in phase.etapes)
