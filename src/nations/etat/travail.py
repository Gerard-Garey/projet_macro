"""Variables d'état du bloc 3, travail (radical `travail`), schéma v2.

Contrat : ADR 0012, G1 (a), et annotation du 13/11/2026, points 1.2 et 1.7
(P53). Quatre variables, toutes `float` : le salaire W (écrit en phase 1, seule
variable nominale des dix), le taux de chômage U, l'emploi N et la population
active N^pa (écrits en phase 4). À l'ouverture du pas t, `W`, `U` et `N`
valent W_{t−1}, U_{t−1} et N_{t−1}, `N_pa` vaut N^pa_t. Valeurs
stationnaires : `sec:travail-stationnaire`.

Domaines au chargement (point 1.7, visa de `macro`), refusés par
`schema.defaut_de_domaine` sous la forme « non (condition) », qui refuse aussi
`NaN`, sans écrêtage :

- W > 0 : UC = W/pr (N8) ;
- 0 ≤ U ≤ 1 : U = 0 et U = 1 sont atteignables par la dynamique (T4, T5) ;
- N ≥ 0 : invariant de conservation ;
- N^pa > 0 : dénominateur de U = 1 − N/N^pa (T5).
"""

from __future__ import annotations

from nations.etat.variables import Invariance, scalaire

RADICAL = "travail"

VARIABLES = (
    scalaire("W", RADICAL, "1", "u.m. par personne et par pas",
             "W_{t−1}, salaire par personne employée (sec:travail-stationnaire)",
             Invariance.NOMINAL),
    scalaire("U", RADICAL, "4", "fraction", "U_{t−1} = U^eq (sec:travail-stationnaire)",
             Invariance.SANS_DIMENSION),
    scalaire("N", RADICAL, "4", "personnes", "N_{t−1} (sec:travail-stationnaire)",
             Invariance.VOLUME),
    scalaire("N_pa", RADICAL, "4", "personnes", "N^pa_t (sec:travail-stationnaire)",
             Invariance.VOLUME),
)

# Domaines au chargement : nom → (condition en clair, prédicat de la condition).
DOMAINES = {
    "W": ("W > 0 (UC = W/pr, N8)", lambda x: x > 0.0),
    "U": ("0 ≤ U ≤ 1 (T4, T5)", lambda x: 0.0 <= x <= 1.0),
    "N": ("N ≥ 0 (invariant de conservation)", lambda x: x >= 0.0),
    "N_pa": ("N^pa > 0 (U = 1 − N/N^pa, T5)", lambda x: x > 0.0),
}
