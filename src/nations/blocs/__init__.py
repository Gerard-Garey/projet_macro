"""Blocs de comportement : un module par bloc de la spécification.

Modules visés par l'inventaire `docs/blocs/README.md` : `production`,
`travail`, `prix`, `menages`, `investissement`, `banque`, `banque_centrale`,
`finances_publiques`. Le nom du module est le radical des labels de ses
équations (`eq:<module>-<nom>`).

Règles d'un bloc :

- il lit l'état d'ouverture et rend des flux proposés et des variables
  nouvelles ; il n'exécute aucun flux monétaire (rôle du noyau) ;
- **aucun état caché** : ni attribut créé à la volée, ni `getattr` avec valeur
  par défaut ;
- **aucun drapeau de mode** : une variante écartée sort du code, et sa fiche
  comparative la consigne.
"""
