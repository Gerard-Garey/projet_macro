"""Paramètres du bloc 3, travail : λ_w, β, U^eq, λ_N, g_N.

Contrat : ADR 0012, F1 et F2, et annotation du 13/11/2026, point 3 (P63, P65,
P71) ; spécification, `sec:travail` et `tab:calibration`. Valeurs indicatives
égales aux valeurs par défaut de `Parametres` de `outils/etat_stationnaire.py`,
**g_N = 0**, valeur de l'état de référence (P63, égalité tenue par un test).
g_pr et μ̄, lus par le bloc 3 (T3), ont leur seule maison dans les tables de
la production et des prix (point 3.3).

Domaines (point 3.2), refusés à toute construction de la table, jamais écrêtés :
0 < λ_w ≤ n_a et 0 < λ_N ≤ n_a (P65) ; 1 + g_N > 0 (type) ; β > 0
(`tab:calibration`) ; 0 < U^eq < 1, **condition de conception et d'existence de
l'état stationnaire**, non domaine de définition (P71 : la borne N ≤ N^pa est
inactive à l'état stationnaire avec une marge de U^eq).

Les labels `eq:travail-…` sont ceux de la fiche 3 (§ 9.1) ; ils sont dans la
spécification depuis le rang 8 de J3-b (P62).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from nations.moteur.parametres import (
    TAUX_DE_CROISSANCE_ANNUEL,
    Parametre,
    TauxDeCroissance,
    TauxDeFlux,
    domaine,
    table_des_declarations,
    valider_table,
    vitesse,
)
from nations.moteur.parametres.cadre import PAS_PAR_AN

_N_A = PAS_PAR_AN.valeur

LAMBDA_W = Parametre(
    "lambda_w", "λ_w", 1.0, "par an, taux de flux",
    "tab:calibration (indicative) ; unité P65",
    ("eq:travail-salaire",), vitesse(_N_A))

BETA = Parametre(
    "beta", "β", 2.0, "sans dimension",
    "tab:calibration (indicative)",
    ("eq:travail-salaire",),
    domaine("β > 0 (tab:calibration)", lambda x: x > 0.0))

U_EQ = Parametre(
    "U_eq", "U^eq", 0.05, "fraction",
    "tab:calibration (hypothèse) ; P71",
    ("eq:travail-salaire",),
    domaine("0 < U^eq < 1 (condition de conception et d'existence de l'état stationnaire, non "
            "domaine de définition : la borne N ≤ N^pa y est inactive avec une marge de U^eq ; "
            "P71)", lambda x: 0.0 < x < 1.0))

LAMBDA_N = Parametre(
    "lambda_N", "λ_N", 3.5, "par an, taux de flux",
    "tab:calibration ; unité P65",
    ("eq:travail-emploi",), vitesse(_N_A))

G_N = Parametre(
    "g_N", "g_N", 0.0, "par an, taux de croissance",
    "décision du mainteneur du 05/10/2026 (#84, point 1, lecture I1) ; P63 (valeur de l'état "
    "de référence)",
    ("eq:travail-population-active", "eq:travail-emploi"),
    TAUX_DE_CROISSANCE_ANNUEL)

PARAMETRES_DU_TRAVAIL = (LAMBDA_W, BETA, U_EQ, LAMBDA_N, G_N)


@dataclass(frozen=True, slots=True)
class TableTravail:
    """Les paramètres du bloc 3 sous leur nom ; validée à toute construction."""

    DECLARATIONS: ClassVar[tuple[Parametre, ...]] = PARAMETRES_DU_TRAVAIL

    lambda_w: TauxDeFlux
    beta: float
    U_eq: float
    lambda_N: TauxDeFlux
    g_N: TauxDeCroissance

    def __post_init__(self) -> None:
        valider_table(self, self.DECLARATIONS)


TRAVAIL = table_des_declarations(TableTravail, PARAMETRES_DU_TRAVAIL)
