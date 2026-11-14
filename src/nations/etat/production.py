"""Variables d'état du bloc 2, production (radical `production`), schéma v2.

Contrat : ADR 0012, G1 (a), et annotation du 13/11/2026, points 1.2 et 1.7
(P53). Quatre variables, écrites en phase 5 par le bloc production (C2 :
valeur du pas suivant sous `<nom>_suivant`), toutes `float`, d'invariance
« volume » (inchangées sous une redénomination ×100). Valeurs stationnaires :
`sec:production-stationnaire` (`outils/etat_stationnaire.py`, `ouverture`).

Domaines au chargement (point 1.7, visa de `macro`), refusés par
`schema.defaut_de_domaine` sous la forme « <valeur> hors du domaine
<condition> », qui refuse aussi `NaN`, sans écrêtage :

- v^e > 0 : IN^vol* = n_a σ v^e est le dénominateur de ξ (P1) ;
- IN^vol ≥ 0 : invariant de conservation (N6, N7), jamais borné pendant un pas ;
- pr > 0 : dénominateur de UC = W/pr (N8) ;
- K^vol > 0 : dénominateur de tu (N11).
"""

from __future__ import annotations

from nations.etat.variables import Invariance, scalaire

RADICAL = "production"

VARIABLES = (
    scalaire("v_e", RADICAL, "5", "u.v. par pas",
             "v^e_t (sec:production-stationnaire ; outils/etat_stationnaire.py, ouverture)",
             Invariance.VOLUME),
    scalaire("IN_vol", RADICAL, "5", "u.v.",
             "IN^vol_t (sec:production-stationnaire ; outils/etat_stationnaire.py, ouverture)",
             Invariance.VOLUME),
    scalaire("pr", RADICAL, "5", "u.v. par personne et par pas",
             "pr_t, productivité par personne employée (sec:production-stationnaire ; "
             "outils/etat_stationnaire.py, ouverture)",
             Invariance.VOLUME),
    scalaire("K_vol", RADICAL, "5", "u.v.",
             "K^vol_t (sec:production-stationnaire, sec:investissement-stationnaire ; "
             "outils/etat_stationnaire.py, ouverture)",
             Invariance.VOLUME),
)

# Domaines au chargement : nom → (condition en clair, prédicat de la condition).
DOMAINES = {
    "v_e": ("v^e > 0 (IN^vol* = n_a σ v^e, dénominateur de ξ, P1)", lambda x: x > 0.0),
    "IN_vol": ("IN^vol ≥ 0 (invariant de conservation, N6 et N7)", lambda x: x >= 0.0),
    "pr": ("pr > 0 (UC = W/pr, N8)", lambda x: x > 0.0),
    "K_vol": ("K^vol > 0 (dénominateur de tu, N11)", lambda x: x > 0.0),
}
