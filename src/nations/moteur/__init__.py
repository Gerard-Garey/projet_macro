"""Ordonnanceur et paramètres.

L'ordonnanceur déroule les phases numérotées d'un pas, identiques à celles de
la spécification (barrières entre pays au jalon J5). Les paramètres sont typés,
chacun avec son unité, sa source et l'étiquette de l'équation qui l'emploie.

Modules (ADR 0012, Conséquences) :
- `phases` : `PHASES`, transcription unique de `tab:phases` (étapes, groupes
  et ordre « puis », sous-phases de la phase 8, couches de la phase 9) ;
- `contrat_bloc` : `DeclarationDeBloc`, `Siege`, `Lecture`, module feuille
  importé par les blocs ;
- `ordonnanceur` : `assembler` (contrôle statique, triangularité),
  `executer_pas`, espace des variables du pas, vue d'un bloc, entrées du tour ;
- `ouverture` : `GRANDEURS_OUVERTURE`, grandeurs calculées en phase 0 ;
- `calendrier` : tour, pas, date affichée, prédicat de date de décision ;
- `conversions` : `par_pas` et `facteur_par_pas`, les deux seules conversions ;
- `registre` : avance et lectures du registre de l'indice des prix, seules
  fonctions qui l'indexent ;
- `parametres` : `Parametre`, `TauxDeFlux`, `TauxDeCroissance` ;
  `parametres.cadre` : n_a, n_m, ε, ε_V et `CADRE` ;
- `diagnostics` : `DefautDeDeclaration`, `RefusDuMoteur`.

`moteur` importe de `nations` le noyau, l'état et, de l'observation, son seul
protocole (`observation.observateur`).

Aucune optimisation itérative à chaque pas ; budget de calcul : au plus 1 ms
par pays-semaine. Radical des labels d'équation du calendrier et de
l'ordonnancement : `moteur` (`eq:moteur-<nom>`).
"""
