"""Observation : séries et exports.

Les séries sont tenues hors de l'état et n'ont **aucun effet sur la
trajectoire** : activer, désactiver ou modifier l'observation ne change aucun
résultat du moteur.

Modules (ADR 0012, Conséquences) :
- `observateur` : protocole `Observateur`, `ObservateurNul`, événement `FinDePas` ;
- `residus` : `ReleveDesResidus`, relevé des résidus / S des identités du noyau ;
- `cout` : `ReleveDuCout`, relevé du coût de calcul par pas ;
- `serie_test_zero` : `SerieDuTestZero`, grandeurs B1 à B26 de `tab:criteres-j3` et r̂*,
  moyennes par bloc de 60 pas et écarts d'A2 ; ratio au PIB annuel (#176).

`observation` n'importe de `nations` que `etat` et `noyau`, pour les types ; seul
le moteur l'importe, et seulement son protocole (`observateur`).
"""
