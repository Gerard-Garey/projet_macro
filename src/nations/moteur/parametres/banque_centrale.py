"""Paramètres du bloc 8, banque centrale et anticipations : a_π, a_I, λ_e, θ_CB, π*, r̄.

Contrat : ADR 0012, F1 et F2 ; ADR 0013, annotation du 14/11/2026, points 2 et 6
(P96 ; synthèse du rang 1a de J3-c, § 6) ; spécification, `sec:banque_centrale`
et `tab:calibration`. Valeurs indicatives égales aux valeurs par défaut de
`Parametres` de `outils/etat_stationnaire.py` (H3.3, égalité tenue par un test) ;
le script nomme `pi_cible` et `rbar` ce que la table nomme `pi_etoile` et `r_bar`,
correspondance portée par le test, le script n'étant pas renommé. Aucune unité
nouvelle (P96).

π* a sa seule maison ici : sa valeur est la valeur initiale de la variable
d'état `pi_etoile`, cible en vigueur (BC4 ; ADR 0010 ; état résolu), que lisent
les blocs et la phase 0 (Γ^e, `nations.moteur.ouverture`). Un champ de table et
une variable d'état portent le même nom (point 2 : espaces de noms distincts).

Domaines (point 6), refusés à toute construction de la table, jamais écrêtés :
0 < a_π < 1,5 ; a_I > 0 ; 0 < λ_e ≤ n_a (P65) ; 0 ≤ θ_CB ≤ 1 ; 1 + π* > 0
(type ; facteur de Fisher de BC1 et f(π*) de Γ^e) ; r̄ > −5 % (C51 ; contient
1 + r̄ > 0).

Les labels `eq:banque_centrale-…` sont ceux de la fiche 8 (§ 9.1) ; ils entrent
dans la spécification au passage de `docwriter` (rang 7 de J3-c, P62), avec
`eq:moteur-croissance-nominale-attendue`.
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

A_PI = Parametre(
    "a_pi", "a_π", 0.5, "sans dimension",
    "tab:calibration (indicative) ; M32 ; P96",
    ("eq:banque_centrale-regle-taux",),
    domaine("0 < a_π < 1,5 (sec:banque_centrale-conditions)", lambda x: 0.0 < x < 1.5))

A_I = Parametre(
    "a_I", "a_I", 0.25, "par an, taux de flux",
    "tab:calibration (indicative) ; M32 ; unité P96",
    ("eq:banque_centrale-taux-neutre",),
    domaine("a_I > 0 (sec:banque_centrale-conditions)", lambda x: x > 0.0))

LAMBDA_E = Parametre(
    "lambda_e", "λ_e", 0.2, "par an, taux de flux",
    "tab:calibration (indicative) ; M32 ; unité P65",
    ("eq:banque_centrale-anticipation",), vitesse(_N_A))

THETA_CB = Parametre(
    "theta_CB", "θ_CB", 0.0, "fraction",
    "tab:calibration (0 au socle) ; M33 ; P96",
    ("eq:banque_centrale-part-souscription",),
    domaine("0 ≤ θ_CB ≤ 1 (sec:banque_centrale-conditions)", lambda x: 0.0 <= x <= 1.0))

PI_ETOILE = Parametre(
    "pi_etoile", "π*", 0.02, "par an, taux de croissance",
    "tab:calibration ; ADR 0010 (M30) ; P96",
    ("eq:banque_centrale-cible", "eq:banque_centrale-regle-taux",
     "eq:banque_centrale-taux-neutre", "eq:moteur-croissance-nominale-attendue"),
    TAUX_DE_CROISSANCE_ANNUEL)

R_BAR = Parametre(
    "r_bar", "r̄", 0.01, "par an, taux de croissance",
    "tab:calibration (indicative) ; C51 ; unité P96",
    ("eq:banque_centrale-regle-taux", "eq:banque_centrale-taux-neutre"),
    domaine("r̄ > −5 % (C51 ; contient 1 + r̄ > 0)", lambda x: x > -0.05))

PARAMETRES_DE_LA_BANQUE_CENTRALE = (A_PI, A_I, LAMBDA_E, THETA_CB, PI_ETOILE, R_BAR)


@dataclass(frozen=True, slots=True)
class TableBanqueCentrale:
    """Les paramètres du bloc 8 sous leur nom ; validée à toute construction."""

    DECLARATIONS: ClassVar[tuple[Parametre, ...]] = PARAMETRES_DE_LA_BANQUE_CENTRALE

    a_pi: float
    a_I: TauxDeFlux
    lambda_e: TauxDeFlux
    theta_CB: float
    pi_etoile: TauxDeCroissance
    r_bar: TauxDeCroissance

    def __post_init__(self) -> None:
        valider_table(self, self.DECLARATIONS)


BANQUE_CENTRALE = table_des_declarations(TableBanqueCentrale, PARAMETRES_DE_LA_BANQUE_CENTRALE)
