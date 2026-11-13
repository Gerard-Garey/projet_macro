"""Vocabulaire fermé des unités, unique pour les variables d'état et les paramètres.

Contrat : ADR 0012, F2, et annotation du 07/10/2026, point 2. Une unité hors
de `UNITES` est un refus de déclaration, pour une variable d'état
(`nations.etat.schema`) comme pour un paramètre du moteur (#97).

Ce module n'importe rien de `nations`, pas même `noyau` : la couche `moteur`
peut l'importer sans charger le schéma d'état ni le noyau.
"""

# Le vocabulaire de F2, complété de « pas » (unité de t), « u.v. », « u.v. par
# pas » et « u.m. par u.v. » (unité de P_t) ; puis, au J3 (#104 ; P65 ; ADR 0012,
# annotation du 13/11/2026), de deux unités par personne employée et par pas
# (dénominateur : personnes employées × un pas ; fenêtre : le pas) :
# « u.m. par personne et par pas » (salaire W, nominale) et « u.v. par personne
# et par pas » (productivité pr, volume). L'invariance sous la redénomination
# est portée par la déclaration de la variable, non par l'unité.
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
    "u.m. par personne et par pas",
    "u.v. par personne et par pas",
)
