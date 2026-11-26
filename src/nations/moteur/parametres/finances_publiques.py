"""Paramètres du bloc 9, État et dette : ν_G et les valeurs à levier fermé θ_G, θ_Tr, τ_H, τ_F, φ.

Contrat : ADR 0012, F1 et F2 ; ADR 0013, annotation du 15/11/2026 (rang 1b de J3-d2), point 8
(P165 : table dans `EnsembleDesParametres`, forme de la table `menages`) ; spécification,
`sec:finances_publiques-conditions`, `tab:calibration` et `tab:leviers` ; fiche
`docs/blocs/finances_publiques.md`, § 9.2 ; décision M33 ; issue #132.

**Leviers au J3** (point 8) : θ_G, θ_Tr, τ_H, τ_F et φ sont les leviers budgétaires du joueur ;
au socle et au J3, leur valeur à levier fermé (« suivre la règle ») est un paramètre de cette
table, sur le précédent de π* (BC4). Leur passage en commandes du joueur relève du J4 (G4),
sans drapeau de mode : seule la source de la valeur change.

**Valeurs indicatives** (H3.3) : celles de `Parametres` de `outils/etat_stationnaire.py`, sauf
deux, déclarées :

- **ν_G = 1,15**, valeur retenue (décision du mainteneur du 05/10/2026, #84) : le défaut du
  script, ν_G = 1, est le point de référence de la forme fermée, hors du domaine ν_G > 1 ;
- **θ_G** n'a pas de défaut au script, qui le résout (fermeture, #44) : la valeur de la table est
  θ_G résolu à π* = 2 % par le résolveur `nations.scenarios.stationnaire`, que le script importe
  (θ_G ne dépend pas de ν_G, C59), seule valeur résolue écrite dans `src/` (ADR 0015, S3),
  égalité au bit tenue par des tests (`tests/unitaires/test_parametres_du_bloc_9.py`,
  `tests/unitaires/test_scenarios_initial.py`) ; `nations.scenarios.initial.etat_initial` ne lit
  pas ce θ_G et rend les tables alignées, θ_G résolu à leur π* (S4).

U^eq (E1, E6) et r̄ (E4) ne sont pas dans cette table : U^eq a sa seule maison dans la table du
travail et r̄ dans celle de la banque centrale (H3.3, une maison par paramètre ;
`sec:finances_publiques-depense` : « U^eq, paramètre du bloc travail »), lus par la vue.

Domaines (`sec:finances_publiques-conditions`, « Conditions de domaine »), refusés à toute
construction de la table, jamais écrêtés : 0 ≤ τ_H < 1 ; 0 ≤ τ_F < 1 ; θ_G ≥ 0 ; θ_Tr ≥ 0 ;
φ ∈ {0 ; 1} (deux valeurs d'un levier, jamais un curseur continu) ; ν_G > 1. La section ne
déclare **aucune condition jointe** entre les champs de la table : `__post_init__` n'appelle que
`valider_table`. Les conditions de l'état stationnaire (θ_G > 0 résolu, marge du plafond de E1,
B ≥ 0, D2) portent sur l'état résolu et sont refusées par `scenarios.initial.etat_initial`
(`EtatStationnaireInexistant`) et par le script d'état stationnaire.

Les labels `eq:finances_publiques-…` sont ceux de `tab:finances_publiques-equations` ; ils sont
dans la spécification depuis `a059d10` (P62).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from nations.moteur.parametres import Parametre, domaine, table_des_declarations, valider_table

NU_G = Parametre(
    "nu_G", "ν_G", 1.15, "sans dimension",
    "décision du mainteneur du 05/10/2026 (#84) ; M33 ; tab:calibration",
    ("eq:finances_publiques-encaisse-visee",),
    domaine("ν_G > 1 (sec:finances_publiques-conditions ; ν_G ≤ 1 demande une décision citant "
            "M33)", lambda x: x > 1.0))

THETA_G = Parametre(
    "theta_G", "θ_G", 0.22058388898746367, "fraction",
    "levier fermé (M33) ; θ_G résolu par nations.scenarios.stationnaire, importé par "
    "outils/etat_stationnaire.py, à π* = 2 % (#44)",
    ("eq:finances_publiques-plan-depense",),
    domaine("θ_G ≥ 0 (sec:finances_publiques-conditions)", lambda x: x >= 0.0))

THETA_TR = Parametre(
    "theta_Tr", "θ_Tr", 0.0, "fraction",
    "levier fermé, nul au test zéro (M33) ; sec:finances_publiques-stationnaire",
    ("eq:finances_publiques-transferts",),
    domaine("θ_Tr ≥ 0 (sec:finances_publiques-conditions)", lambda x: x >= 0.0))

TAU_H = Parametre(
    "tau_H", "τ_H", 0.25, "fraction",
    "tab:calibration (indicative) ; M33",
    ("eq:finances_publiques-impot-menages",),
    domaine("0 ≤ τ_H < 1 (sec:finances_publiques-conditions)", lambda x: 0.0 <= x < 1.0))

TAU_F = Parametre(
    "tau_F", "τ_F", 0.0, "fraction",
    "levier fermé à 0 au socle (M33, QM5)",
    ("eq:finances_publiques-impot-entreprises",),
    domaine("0 ≤ τ_F < 1 (sec:finances_publiques-conditions)", lambda x: 0.0 <= x < 1.0))

PHI = Parametre(
    "phi", "φ", 1.0, "sans dimension",
    "levier de couverture des intérêts, valeur de règle « couverture intégrale » (M33)",
    ("eq:finances_publiques-couverture-interets",),
    domaine("φ ∈ {0 ; 1} (sec:finances_publiques-conditions ; deux valeurs, jamais un curseur "
            "continu)", lambda x: x in (0.0, 1.0)))

PARAMETRES_DES_FINANCES_PUBLIQUES = (NU_G, THETA_G, THETA_TR, TAU_H, TAU_F, PHI)


@dataclass(frozen=True, slots=True)
class TableFinancesPubliques:
    """Les paramètres du bloc 9 sous leur nom ; validée à toute construction."""

    DECLARATIONS: ClassVar[tuple[Parametre, ...]] = PARAMETRES_DES_FINANCES_PUBLIQUES

    nu_G: float
    theta_G: float
    theta_Tr: float
    tau_H: float
    tau_F: float
    phi: float

    def __post_init__(self) -> None:
        valider_table(self, self.DECLARATIONS)


FINANCES_PUBLIQUES = table_des_declarations(TableFinancesPubliques,
                                            PARAMETRES_DES_FINANCES_PUBLIQUES)
