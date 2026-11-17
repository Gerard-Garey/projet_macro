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

Les labels `eq:banque-…` sont ceux de la fiche 7 (§ 9.1) ; ils sont entrés dans
la spécification au passage de `docwriter` (commit `7d90789`, rang 5 de J3-c,
P62).
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
    "BCE, statistiques de taux d'intérêt des IFM (MIR), indicateur composite du coût de "
    "l'emprunt des sociétés non financières, affaires nouvelles "
    "(ECB/MIR/M.U2.B.A2I.AM.R.A.2240.EUR.N), moins le taux du jour le jour (EONIA jusqu'en "
    "2019-09, puis €STR), zone euro, moyenne mensuelle 2003-2024 : 2,09 points (encours : 2,30) ; "
    "DBnomics, consulté le 16/11/2026 ; arrondi au point ; tab:calibration ; décision M34 ; M31 ; "
    "P96",
    ("eq:banque-taux-credit",),
    domaine(_SANS_SIGNE, lambda x: True))

VARPI_D = Parametre(
    "varpi_D", "ϖ_D", 0.01, "par an, taux de flux",
    "BCE, MIR et BSI : taux des dépôts des ménages et des sociétés non financières (à vue, à "
    "terme, à préavis), pondéré par les encours de la BSI, moins le taux du jour le jour (EONIA "
    "puis €STR) ; taux des MIR : dépôts à vue des ménages et des SNF (L21…2250.EUR.N, "
    "L21…2240.EUR.N), dépôts à terme, encours (L22.A…2250.EUR.O, L22.A…2240.EUR.O), dépôts à "
    "préavis de 3 mois au plus des ménages (L23.D…2250.EUR.N, employé aussi pour les SNF) ; poids "
    "de la BSI : ECB/BSI/M.U2.N.A.{L21,L22,L23}.A.1.U2.{2250,2240}.Z01.E ; zone euro : 0,85 point (2003-01 à 2008-08) et 1,93 point (2022-07 à 2024-12), "
    "fenêtres de taux positifs ; moyenne 2003-2024 de −0,05 point, dominée par les taux négatifs, "
    "écartée ; fenêtre contestée ; écart dépendant du régime (limite de B2, #167) ; DBnomics, "
    "consulté le 16/11/2026 ; tab:calibration ; décision M34 ; M31 ; P96",
    ("eq:banque-taux-depots",),
    domaine(_SANS_SIGNE, lambda x: True))

VARTHETA = Parametre(
    "vartheta", "ϑ", 0.15, "fraction",
    "BCE, statistiques de supervision bancaire (MSU), ratio CET1 des établissements importants "
    "(ECB/SUP/Q.B01.W0._Z.I4008._T.SII._Z._Z._Z.PCT.C), moyenne 2015T3-2024T4 : 14,75 % des "
    "actifs pondérés des risques ; DBnomics, consulté le 16/11/2026 ; définition déclarée : ϑ "
    "rapporte les fonds propres aux crédits, distinct d'un ratio sur actifs pondérés, auquel il est "
    "égal sous les pondérations de Bâle 1988 (Comité de Bâle, juillet 1988, § 44 et annexe 2, lus "
    "le 16/11/2026) ; dénominateur de Bâle III plus petit, écart non mesuré, contesté ; arrondi ; "
    "tab:calibration ; décision M34 ; M31 ; P96",
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
