"""Scénarios : état initial et archétypes de pays.

L'état initial est **résolu comme équilibre des règles** du moteur, sans
préparation cachée ; il est la référence du test zéro (ratios de stocks
stables sur 60 ans sans choc). Les archétypes de pays sont anonymisés : aucun
nom de pays réel n'est associé à une configuration.

Le résolveur en formes fermées de l'état stationnaire est le module feuille
`stationnaire` (ADR 0015) ; ce paquet n'importe rien, de sorte qu'importer le
résolveur ne charge de `nations` que `nations`, `nations.scenarios` et lui.
"""
