"""Paramètres du bloc 6, investissement : δ seul en J3-b, complétée en J3-c.

Contrat : ADR 0012, F1 et F2, et annotation du 13/11/2026, point 3.4
(décision du mainteneur du 13/11/2026, P68, option (b)) : la maison de δ est
la table du bloc 6, maison de la décision qui l'a fixé (M28, fiche 6, Q11 : un
seul δ pour le volume et la valeur comptable) ; le bloc 2 la lit par la vue
(N10). L'objet `Cadre` que lit le noyau et l'ADR 0005, point 18, sont
inchangés. Valeur indicative égale à la valeur par défaut de `Parametres` de
`outils/etat_stationnaire.py` (P63, égalité tenue par un test).

Domaine : 0 < δ < n_a (`sec:investissement-conditions` ; script, δ/n_a dans
]0 ; 1[), refusé à toute construction de la table, jamais écrêté.
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
from nations.moteur.parametres.cadre import PAS_PAR_AN

_N_A = PAS_PAR_AN.valeur

DELTA = Parametre(
    "delta", "δ", 0.05, "par an, taux de flux",
    "tab:calibration (hypothèse) ; M28, Q11 ; maison P68 ; unité P65",
    ("eq:production-capital-volume", "eq:investissement-amortissement"),
    domaine(f"0 < δ < n_a = {_N_A} (sec:investissement-conditions)",
            lambda x: 0.0 < x < _N_A))

PARAMETRES_DE_L_INVESTISSEMENT = (DELTA,)


@dataclass(frozen=True, slots=True)
class TableInvestissement:
    """Les paramètres du bloc 6 sous leur nom (δ seul en J3-b) ; validée à toute construction."""

    DECLARATIONS: ClassVar[tuple[Parametre, ...]] = PARAMETRES_DE_L_INVESTISSEMENT

    delta: TauxDeFlux

    def __post_init__(self) -> None:
        valider_table(self, self.DECLARATIONS)


INVESTISSEMENT = table_des_declarations(TableInvestissement, PARAMETRES_DE_L_INVESTISSEMENT)
