"""Paramètres du bloc 5, ménages : ν_H, λ_H.

Contrat : ADR 0012, F1 et F2 ; ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1),
point 2 ; spécification, `sec:menages-plan`, `sec:menages-conditions` et `tab:calibration` ;
fiche `docs/blocs/menages.md`, § 9.2 ; décision M27 ; issue #60. Valeurs indicatives égales
aux valeurs par défaut de `Parametres` de `outils/etat_stationnaire.py` (H3.3, égalité tenue
par un test). Aucune unité nouvelle. Calibration sur sources : #62.

Domaines, refusés à toute construction de la table, jamais écrêtés :

- ν_H > 0, en années (un niveau, ni taux de flux ni taux de croissance : n_a y est un
  changement d'unité dans H3, non une conversion) ;
- 0 < λ_H ≤ n_a (vitesse d'ajustement, P65), par an, taux de flux, convertie linéairement ;
- **condition jointe** 0 < ν_H λ_H < 1 (`sec:menages-conditions`), d'où α_Y = 1 − ν_H λ_H > 0,
  contrôlée dans `__post_init__` de la table, toute construction comprise
  (`dataclasses.replace`, `varier`).

Le **coefficient de richesse** λ_H/n_a + ν_H λ_H π^{∗,pas} > γ^e lit aussi les tables de la
production, du travail et de la banque centrale : il est contrôlé par
`EnsembleDesParametres` (`nations.moteur.parametres.ensemble`). Le plafond de H5 n'a pas de
champ (décision du mainteneur du 03/10/2026, lecture (i)).

Les labels `eq:menages-…` sont ceux de la fiche 5 (§ 9.1) ; ils ont été posés dans la
spécification avec leurs balises au passage de `docwriter` (rang 6 de J3-d1, P62).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from nations.moteur.diagnostics import DefautDeDeclaration
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

NU_H = Parametre(
    "nu_H", "ν_H", 1.1, "années",
    "Eurostat, comptes annuels des secteurs (SEC 2010 ; nasa_10_f_bs, nasa_10_nf_tr), ménages et "
    "ISBLSM (S14_S15), numéraire et dépôts (F.2, actif, non consolidé) sur revenu disponible brut "
    "(B.6g, prix courants), EA21, moyenne 2001-2023 : 1,076 an ; consulté le 16/11/2026 ; "
    "définition déclarée : V_H (dépôts seuls, sans passif) sur le revenu disponible annuel, "
    "rapport comparé à B10, d'où ν_H = R/(1 − R n_a π^{∗,pas}) à π* = 2 % : 1,0995, arrondi à "
    "1,1 ; contrôle stock-flux : acquisition nette de F.2 sur B.6g, 4,32 % (2002-2023), contre "
    "4,27 % d'épargne nominale dans le modèle ; écart déclaré : B.6g contient l'excédent des "
    "logements et le revenu mixte ; tab:calibration ; décision M34 ; M27",
    ("eq:menages-richesse-visee",),
    domaine("ν_H > 0 (sec:menages-conditions)", lambda x: x > 0.0))

LAMBDA_H = Parametre(
    "lambda_H", "λ_H", 0.4, "par an, taux de flux",
    "choix de conception dans la fourchette lue : dépense totale, durables compris, de 50 à 90 % "
    "d'un versement sur le trimestre de réception (J. A. Parker, N. S. Souleles, D. S. Johnson et "
    "R. McClelland, « Consumer Spending and the Economic Stimulus Payments of 2008 », NBER "
    "Working Paper 16684, janvier 2011, résumé lu le 16/11/2026 ; États-Unis, 2008 ; période du "
    "chiffre à confirmer sur l'article) ; dépense cumulée d'une aubaine sur 3 tours de 0,605 à "
    "ν_H = 1,1 ; correspondance : hypothèse, contestée (versements annoncés, données américaines, "
    "ménage représentatif) ; tab:calibration ; décision M34 ; M27 ; unité P65",
    ("eq:menages-plan-consommation",), vitesse(_N_A))

PARAMETRES_DES_MENAGES = (NU_H, LAMBDA_H)


@dataclass(frozen=True, slots=True)
class TableMenages:
    """Les paramètres du bloc 5 sous leur nom ; validée à toute construction, condition jointe
    0 < ν_H λ_H < 1 comprise."""

    DECLARATIONS: ClassVar[tuple[Parametre, ...]] = PARAMETRES_DES_MENAGES

    nu_H: float
    lambda_H: TauxDeFlux

    def __post_init__(self) -> None:
        valider_table(self, self.DECLARATIONS)
        produit = self.nu_H * self.lambda_H.valeur
        if not 0.0 < produit < 1.0:
            raise DefautDeDeclaration(
                f"ν_H λ_H = {produit!r} hors du domaine 0 < ν_H λ_H < 1 (sec:menages-conditions ; "
                "α_Y = 1 − ν_H λ_H > 0) : refusé, jamais écrêté", nom="lambda_H")


MENAGES = table_des_declarations(TableMenages, PARAMETRES_DES_MENAGES)
