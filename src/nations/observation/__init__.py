"""Observation : séries et exports.

Les séries sont tenues hors de l'état et n'ont **aucun effet sur la
trajectoire** : activer, désactiver ou modifier l'observation ne change aucun
résultat du moteur.

Modules (ADR 0012, Conséquences) :
- `observateur` : protocole `Observateur`, `ObservateurNul`, événement `FinDePas` ;
- `residus` : `ReleveDesResidus`, relevé des résidus / S des identités du noyau.

`observation` n'importe de `nations` que `etat` et `noyau`, pour les types ; seul
le moteur l'importe, et seulement son protocole (`observateur`).
"""
