"""Paramètres du bloc 4, prix : μ̄, λ_μ, ψ_ξ.

Contrat : ADR 0012, F1 et F2, et annotation du 13/11/2026, point 3 (P63, P65,
P71) ; spécification, `sec:prix` et `tab:calibration`. Valeurs indicatives
égales aux valeurs par défaut de `Parametres` de `outils/etat_stationnaire.py`
(P63, égalité tenue par un test). μ̄ a sa seule maison ici ; le bloc 3 la lit
dans cette table, par la vue (ω* = 1/(1 + μ̄), T3 ; point 3.3).

Domaines (point 3.2), refusés à toute construction de la table, jamais écrêtés :
0 < λ_μ ≤ n_a (P65) ; ψ_ξ ≥ 0 (`tab:calibration`) ; μ̄ > 0, **condition de
conception et d'existence de l'état stationnaire** (P71 : une marge nulle ou
négative ne couvre pas l'amortissement), qui contient le domaine de définition
1 + μ̄ > 0 (ln(1 + μ̄) et ω* = 1/(1 + μ̄) définis).

Les labels `eq:prix-…` sont ceux de la fiche 4 (§ 9.1) ; ils sont dans la
spécification depuis le rang 8 de J3-b (P62).
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
    vitesse,
)
from nations.moteur.parametres.cadre import PAS_PAR_AN

_N_A = PAS_PAR_AN.valeur

MU_BAR = Parametre(
    "mu_bar", "μ̄", 0.25, "fraction",
    "tab:calibration (hypothèse) ; P71",
    ("eq:prix-marge", "eq:travail-salaire"),
    domaine("μ̄ > 0 (condition de conception et d'existence de l'état stationnaire : une marge "
            "nulle ou négative ne couvre pas l'amortissement, P71 ; elle contient le domaine de "
            "définition 1 + μ̄ > 0)", lambda x: x > 0.0))

LAMBDA_MU = Parametre(
    "lambda_mu", "λ_μ", 1.2, "par an, taux de flux",
    "tab:calibration (indicative) ; unité P65",
    ("eq:prix-marge",), vitesse(_N_A))

PSI_XI = Parametre(
    "psi_xi", "ψ_ξ", 0.5, "sans dimension",
    "tab:calibration (indicative)",
    ("eq:prix-marge",),
    domaine("ψ_ξ ≥ 0 (tab:calibration)", lambda x: x >= 0.0))

PARAMETRES_DES_PRIX = (MU_BAR, LAMBDA_MU, PSI_XI)


@dataclass(frozen=True, slots=True)
class TablePrix:
    """Les paramètres du bloc 4 sous leur nom ; validée à toute construction."""

    DECLARATIONS: ClassVar[tuple[Parametre, ...]] = PARAMETRES_DES_PRIX

    mu_bar: float
    lambda_mu: TauxDeFlux
    psi_xi: float

    def __post_init__(self) -> None:
        valider_table(self, self.DECLARATIONS)


PRIX = table_des_declarations(TablePrix, PARAMETRES_DES_PRIX)
