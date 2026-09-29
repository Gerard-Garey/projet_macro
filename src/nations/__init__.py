"""Nations & Marchés : moteur v3 d'un simulateur macroéconomique multi-pays à
cohérence stock-flux.

Le moteur est organisé en couches (`CLAUDE.md`, « Architecture » ; ADR 0002) :

- `noyau` : comptes, seul lieu d'exécution des flux monétaires ;
- `blocs` : un module par bloc de la spécification ;
- `moteur` : ordonnanceur des phases d'un pas et paramètres typés ;
- `etat` : schéma d'état typé et versionné, sauvegarde et reprise ;
- `observation` : séries et exports, sans effet sur la trajectoire ;
- `scenarios` : état initial résolu comme équilibre des règles, archétypes ;
- `leviers` : commandes du joueur, selon le régime de souveraineté.

La spécification `docs/specification/nations_et_marches.tex` fait foi : chaque
équation qu'elle numérote porte ici une balise `# eq:<label>`, et
réciproquement (`outils/concordance_spec_moteur.py`).
"""
