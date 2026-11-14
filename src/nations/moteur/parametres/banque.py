"""Paramètres du bloc 7, banque : ϖ_L, ϖ_D, ϑ.

Contrat : ADR 0012, F1 et F2 ; ADR 0013, annotation du 14/11/2026, point 6
(P96 ; synthèse du rang 1a de J3-c, § 6) ; spécification, `sec:banque` et
`tab:calibration`. Valeurs indicatives égales aux valeurs par défaut de
`Parametres` de `outils/etat_stationnaire.py` (H3.3, égalité tenue par un test).
Aucune unité nouvelle (P96). Posée au rang 3 de J3-c avec la table du bloc 8,
avant le bloc qui la lit (#90, rang 5) ; calibration sur sources : #130.

Domaines (point 6), refusés à toute construction de la table, jamais écrêtés :
ϖ_L et ϖ_D finis, **sans condition de signe** (la condition d'existence du
dividende stationnaire les contraint, script) ; ϑ > 0.

Les labels `eq:banque-…` sont ceux de la fiche 7 (§ 9.1) ; ils entrent dans la
spécification au passage de `docwriter` (rang 7 de J3-c, P62).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from nations.moteur.parametres import (
    Parametre,
    TauxDeFlux,
    domaine,
    table_des_declarations,
    valider_table,
)

_SANS_SIGNE = ("sans condition de signe (la condition d'existence du dividende stationnaire "
               "le contraint, outils/etat_stationnaire.py)")

VARPI_L = Parametre(
    "varpi_L", "ϖ_L", 0.02, "par an, taux de flux",
    "tab:calibration (indicative) ; M31 ; P96",
    ("eq:banque-taux-credit",),
    domaine(_SANS_SIGNE, lambda x: True))

VARPI_D = Parametre(
    "varpi_D", "ϖ_D", 0.01, "par an, taux de flux",
    "tab:calibration (indicative) ; M31 ; P96",
    ("eq:banque-taux-depots",),
    domaine(_SANS_SIGNE, lambda x: True))

VARTHETA = Parametre(
    "vartheta", "ϑ", 0.10, "fraction",
    "tab:calibration (hypothèse) ; M31 ; P96",
    ("eq:banque-dividendes",),
    domaine("ϑ > 0 (sec:banque-conditions)", lambda x: x > 0.0))

PARAMETRES_DE_LA_BANQUE = (VARPI_L, VARPI_D, VARTHETA)


@dataclass(frozen=True, slots=True)
class TableBanque:
    """Les paramètres du bloc 7 sous leur nom ; validée à toute construction."""

    DECLARATIONS: ClassVar[tuple[Parametre, ...]] = PARAMETRES_DE_LA_BANQUE

    varpi_L: TauxDeFlux
    varpi_D: TauxDeFlux
    vartheta: float

    def __post_init__(self) -> None:
        valider_table(self, self.DECLARATIONS)


BANQUE = table_des_declarations(TableBanque, PARAMETRES_DE_LA_BANQUE)
