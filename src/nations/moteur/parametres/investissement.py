"""Paramètres du bloc 6, investissement et financement des entreprises : δ, t̄u, λ_ti, η_r, ζ,
lv*, ν_F.

Contrat : ADR 0012, F1 et F2, et annotation du 13/11/2026, point 3.4 (décision du mainteneur du
13/11/2026, P68, option (b)) : la maison de δ est la table du bloc 6, maison de la décision qui
l'a fixé (M28, fiche 6, Q11 : un seul δ pour le volume et la valeur comptable) ; le bloc 2 la lit
par la vue (N10). L'objet `Cadre` que lit le noyau et l'ADR 0005, point 18, sont inchangés.
Table complétée au rang 4 de J3-d1 (ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1),
point 2 ; P80 ; #67) : δ reçoit l'étiquette de F1 ; t̄u, λ_ti, η_r, ζ, lv*, ν_F. Valeurs
indicatives égales aux valeurs par défaut de `Parametres` de `outils/etat_stationnaire.py`
(H3.3, égalité tenue par un test ; le script nomme `lv` ce que la table nomme `lv_etoile`).
Aucune unité nouvelle : η_r et ζ sont « sans dimension », sur le précédent de β et de a_π, la
source gardant « par unité de taux réel annuel, sans conversion » (élasticités de niveau, non
des vitesses). Calibration sur sources : #55, #62.

Domaines (`sec:investissement-conditions`), refusés à toute construction de la table, jamais
écrêtés : 0 < δ < n_a ; t̄u > 0 ; 0 < λ_ti ≤ n_a (vitesse, P65) ; 0 ≤ η_r ≤ 20 ; 0 ≤ ζ ≤ 20
(bornes hautes déclarées par P139 : domaine dans lequel les bornes (b) du bloc sont lues) ;
0 ≤ lv* < 1 ; ν_F > 0.

**Hors de la table** (point 2) : A > 0, taux de distribution dans [0,2 ; 0,9] (#55),
η_r ≥ 1,005 (seuil (d1)), λ_ti × 2 dans le domaine de stabilité : contraintes de calibration,
contrôlées par le script et les tests, non des refus (fiche 6, § 9.2). ϱ̄_L, π*, g et Γ^e ne
sont pas des paramètres : ϱ̄_L est une variable d'état du bloc (P128), π*_t est lue à
l'ouverture, Γ^e et π^{∗,pas} sont des grandeurs du moteur.

Les labels `eq:investissement-…` sont ceux de la fiche 6 (§ 9.1) ; ils ont été posés dans la
spécification avec leurs balises au passage de `docwriter` (rang 6 de J3-d1, P62).
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

DELTA = Parametre(
    "delta", "δ", 0.05, "par an, taux de flux",
    "tab:calibration (hypothèse) ; M28, Q11 ; maison P68 ; unité P65",
    ("eq:production-capital-volume", "eq:investissement-amortissement",
     "eq:investissement-demande-credit"),
    domaine(f"0 < δ < n_a = {_N_A} (sec:investissement-conditions)",
            lambda x: 0.0 < x < _N_A))

TU_BAR = Parametre(
    "tu_bar", "t̄u", 0.8, "fraction",
    "M28 ; tab:calibration (indicative) ; ancre unique du bloc (Q3)",
    ("eq:investissement-utilisation-visee", "eq:investissement-part-visee"),
    domaine("t̄u > 0 (sec:investissement-conditions)", lambda x: x > 0.0))

LAMBDA_TI = Parametre(
    "lambda_ti", "λ_ti", 0.02, "par an, taux de flux",
    "M28 ; hypothèse ; unité P65",
    ("eq:investissement-part-visee",), vitesse(_N_A))

ETA_R = Parametre(
    "eta_r", "η_r", 2.0, "sans dimension",
    "M28 ; hypothèse ; par unité de taux réel annuel, sans conversion",
    ("eq:investissement-plan",),
    domaine("0 ≤ η_r ≤ 20 (sec:investissement-conditions ; borne haute P139)",
            lambda x: 0.0 <= x <= 20.0))

ZETA = Parametre(
    "zeta", "ζ", 4.0, "sans dimension",
    "M28 ; à calibrer (4 à 8), valeur du script ; par unité de taux réel annuel, sans "
    "conversion (élasticité de niveau, non une vitesse)",
    ("eq:investissement-utilisation-visee",),
    domaine("0 ≤ ζ ≤ 20 (sec:investissement-conditions ; borne haute P139)",
            lambda x: 0.0 <= x <= 20.0))

LV_ETOILE = Parametre(
    "lv_etoile", "lv*", 0.4, "fraction",
    "M28 ; hypothèse ; nommé `lv` par le script",
    ("eq:investissement-demande-credit",),
    domaine("0 ≤ lv* < 1 (sec:investissement-conditions)", lambda x: 0.0 <= x < 1.0))

NU_F = Parametre(
    "nu_F", "ν_F", 1.0 / 6.0, "années",
    "M28 ; hypothèse (deux mois de ventes)",
    ("eq:investissement-depots-vises",),
    domaine("ν_F > 0 (sec:investissement-conditions)", lambda x: x > 0.0))

PARAMETRES_DE_L_INVESTISSEMENT = (DELTA, TU_BAR, LAMBDA_TI, ETA_R, ZETA, LV_ETOILE, NU_F)


@dataclass(frozen=True, slots=True)
class TableInvestissement:
    """Les paramètres du bloc 6 sous leur nom ; validée à toute construction."""

    DECLARATIONS: ClassVar[tuple[Parametre, ...]] = PARAMETRES_DE_L_INVESTISSEMENT

    delta: TauxDeFlux
    tu_bar: float
    lambda_ti: TauxDeFlux
    eta_r: float
    zeta: float
    lv_etoile: float
    nu_F: float

    def __post_init__(self) -> None:
        valider_table(self, self.DECLARATIONS)


INVESTISSEMENT = table_des_declarations(TableInvestissement, PARAMETRES_DE_L_INVESTISSEMENT)
