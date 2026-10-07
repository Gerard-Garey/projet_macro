"""Vocabulaire fermé des unités, unique pour les variables d'état et les paramètres.

Contrat : ADR 0012, F2, et annotation du 07/10/2026, point 2. Une unité hors
de `UNITES` est un refus de déclaration, pour une variable d'état
(`nations.etat.schema`) comme pour un paramètre du moteur (#97).

Ce module n'importe rien de `nations`, pas même `noyau` : la couche `moteur`
peut l'importer sans charger le schéma d'état ni le noyau.
"""

# Le vocabulaire de F2, complété de « pas » (unité de t), « u.v. », « u.v. par
# pas » et « u.m. par u.v. » (unité de P_t).
UNITES = (
    "pas par an",
    "pas par tour",
    "sans dimension",
    "u.m.",
    "u.m. par pas",
    "par an, taux de flux",
    "par an, taux de croissance",
    "années",
    "personnes",
    "fraction",
    "pas",
    "u.v.",
    "u.v. par pas",
    "u.m. par u.v.",
)
