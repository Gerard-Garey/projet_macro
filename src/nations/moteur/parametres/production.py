"""Paramètres du bloc 2, production : λ_v, λ_IN, σ, g_pr, κ.

Contrat : ADR 0012, F1 et F2, et annotation du 13/11/2026, point 3 (P63, P65,
P70) ; spécification, `sec:production` et `tab:calibration`. Valeurs
indicatives égales aux valeurs par défaut de `Parametres` de
`outils/etat_stationnaire.py` (P63, égalité tenue par un test) ; valeurs par
archétype dans `scenarios/` (J3-e). g_pr a sa seule maison ici ; le bloc 3 la
lit dans cette table, par la vue (point 3.3).

Domaines (point 3.2), refusés à toute construction de la table, jamais écrêtés :
0 < λ_v < n_a, strict (P70) ; 0 < λ_IN ≤ n_a (P65) ; 1 + g_pr > 0 (type) ;
σ > 0 et κ > 0, domaines de définition (dénominateurs de N2 et N11).

Les labels `eq:production-…` sont ceux de la fiche 2 (§ 9.1) ; ils sont dans
la spécification depuis le rang 8 de J3-b (P62).
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
    vitesse_stricte,
)
from nations.moteur.parametres.cadre import PAS_PAR_AN

_N_A = PAS_PAR_AN.valeur

LAMBDA_V = Parametre(
    "lambda_v", "λ_v", 3.0, "par an, taux de flux",
    "tab:calibration (indicative) ; unité P65 ; domaine strict P70",
    ("eq:production-ventes-anticipees",), vitesse_stricte(_N_A))

LAMBDA_IN = Parametre(
    "lambda_IN", "λ_IN", 1.5, "par an, taux de flux",
    "tab:calibration (indicative) ; unité P65",
    ("eq:production-visee",), vitesse(_N_A))

SIGMA = Parametre(
    # 1,4 pas de ventes à n_a = 12 : le littéral est la valeur de 1,4/12 en double précision,
    # égale au bit à la valeur par défaut du script (P63) ; aucun littéral de n_a hors de
    # `cadre` (#102).
    "sigma", "σ", 0.11666666666666665, "années",
    "tab:calibration (indicative) : 1,4 pas de ventes à n_a = 12 ; unité P65",
    ("eq:production-stock-cible",),
    domaine("σ > 0 (domaine de définition : IN^vol* = n_a σ v^e > 0, dénominateur de ξ)",
            lambda x: x > 0.0))

G_PR = Parametre(
    "g_pr", "g_pr", 0.02, "par an, taux de croissance",
    "décision du mainteneur du 05/10/2026 (#84, point 1, lecture I1)",
    ("eq:production-productivite", "eq:production-ventes-anticipees", "eq:production-visee",
     "eq:travail-salaire"),
    TAUX_DE_CROISSANCE_ANNUEL)

KAPPA = Parametre(
    "kappa", "κ", 1.6, "années",
    "tab:calibration (indicative) ; unité P65",
    ("eq:production-capacite",),
    domaine("κ > 0 (domaine de définition : y^cap = K^vol/(n_a κ), N11)", lambda x: x > 0.0))

PARAMETRES_DE_LA_PRODUCTION = (LAMBDA_V, LAMBDA_IN, SIGMA, G_PR, KAPPA)


@dataclass(frozen=True, slots=True)
class TableProduction:
    """Les paramètres du bloc 2 sous leur nom ; validée à toute construction."""

    DECLARATIONS: ClassVar[tuple[Parametre, ...]] = PARAMETRES_DE_LA_PRODUCTION

    lambda_v: TauxDeFlux
    lambda_IN: TauxDeFlux
    sigma: float
    g_pr: TauxDeCroissance
    kappa: float

    def __post_init__(self) -> None:
        valider_table(self, self.DECLARATIONS)


PRODUCTION = table_des_declarations(TableProduction, PARAMETRES_DE_LA_PRODUCTION)
