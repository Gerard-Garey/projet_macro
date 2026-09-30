"""Ordonnanceur et paramètres.

L'ordonnanceur déroule les phases numérotées d'un pas, identiques à celles de
la spécification (barrières entre pays au jalon J5). Les paramètres sont typés,
chacun avec son unité, sa source et l'étiquette de l'équation qui l'emploie.

Aucune optimisation itérative à chaque pas ; budget de calcul : au plus 1 ms
par pays-semaine. Radical des labels d'équation du calendrier et de
l'ordonnancement : `moteur` (`eq:moteur-<nom>`).
"""
