# Cahier des charges

Ce document fixe ce que le projet doit faire ; `CLAUDE.md` renvoie ici pour le fond. Chaque exigence est numérotée pour être citée dans les issues, les ADR et les revues (par exemple `docs/exigences.md` § 2.3). Il reprend les six objectifs de la première tentative (17/09/2026), reformulés « simulateur d'abord » par décision du mainteneur du 29/09/2026.

## 1. Objet, destinataires et objectifs

### 1.1 Objet

*Nations & Marchés* simule des économies nationales reliées entre elles, à cohérence stock-flux, au pas hebdomadaire ou mensuel (choix de la fiche « temps et comptabilité », jalon J1).

Chaque pays est piloté par un **État**, qui fixe le cadre sans produire lui-même, sauf en mode planifié :
- politique monétaire ;
- finances publiques ;
- cadre institutionnel.

Le secteur privé est **autonome** : ménages, entreprises, banques.

Le projet livre, dans l'ordre :
1. un **simulateur** : moteur, scénarios, leviers, restitution ;
2. puis un **jeu multijoueur tour par tour mensuel**, avec interface web.

### 1.2 Destinataires et ce qui prime

- **Destinataires** : le mainteneur, concepteur du jeu ; plus tard, les joueurs ; les lecteurs de la spécification et du cours.
- **Ce qui prime** :
  1. la concordance entre spécification et moteur ;
  2. la reproductibilité ;
  3. la lisibilité des mécanismes pour le joueur.
- Le modèle n'est pas un outil de prévision. Un écart aux valeurs observées est acceptable tant qu'il ne produit pas une trajectoire qualitativement différente.

### 1.3 Objectifs

Chaque objectif a **son test d'acceptation écrit avant l'essai**. Un objectif sans test est une intention, pas un objectif. Les critères s'évaluent sur deux fenêtres, publiées côte à côte : la **fenêtre de partie** depuis l'état initial, et la **fenêtre longue** (60 ans).

| N° | Objectif | Test d'acceptation (principe ; seuils fixés avant l'essai) | Jalon |
|---|---|---|---|
| O1 | **Économie de référence fiable** : croissance sans dérive persistante inexpliquée des prix, de l'emploi, des ratios de stocks ou des dettes, depuis l'état initial et plusieurs graines | Test zéro (§ 2.6) réussi sur les deux fenêtres, pour plusieurs graines | J3 |
| O2 | **Décisions utiles et compréhensibles** : chaque levier a un effet identifiable, un coût, un délai, des gagnants et des perdants, et des contreparties comptables | Pour chaque levier du catalogue, un scénario apparié (même état, même graine) montre un effet du signe attendu, son délai et sa distribution ; avis de `jeu` | J4 |
| O3 | **Crises explicables et sorties crédibles** : signes précurseurs lisibles, sorties progressives et financées, sans remise à zéro gratuite des dettes, des stocks, des anticipations ou de la confiance | Pour chaque type de crise retenu : précondition admissible, contrefactuel publié, signal précurseur, intervention, reprise sans effacement gratuit | J6 |
| O4 | **Multi-pays équitable et solide** : aucun résultat matériel ne dépend de l'ordre des joueurs, de l'unité monétaire, d'une permutation de pays ou d'une reprise de sauvegarde | Tests d'invariance (pays seul contre monde à un pays, changement d'unité, permutation, reprise) sur les deux fenêtres, avec tolérance relative à l'échelle du bilan | J5 (reprise dès J2) |
| O5 | **Simulation jouable, puis partie jouable** : état initial compatible avec les règles actives, sans préparation cachée ; indicateurs lisibles ; réponses perceptibles à l'échelle d'une partie | Simulateur : scénarios de 5 à 10 ans lisibles, démonstration au mainteneur (J4). Jeu : partie complète menée par le mainteneur (J7) | J4, J7 |
| O6 | **Spécification à jour** : les équations, règles actives, conventions de mesure et limites connues correspondent au moteur livré | Script de concordance en CI, bloquant ; revue de l'expert pilote en fin de branche | Continu dès J0 |

Critères de la première tentative (16/09/2026), point de départ proposé pour O1, à confirmer par le mainteneur au jalon J3 :
- ratios capital/PIB et monnaie/PIB à ±10 % ;
- part salariale à ±2 points ;
- chômage entre 4 et 8 % ;
- inflation à 2 ± 1 point ;
- taux réel directeur entre 1,5 et 3 % ;
- aucune entrée en crise ni dépression.

Toutes ces valeurs s'entendent **par blocs de cinq ans**.

## 2. Exigences de fond

### 2.1 Principes de conception (non négociables)

1. **Un joueur = un État.** Il fixe le cadre ; il ne construit pas les usines, sauf en mode planifié.
2. **Secteur privé autonome**, avec des règles de comportement dérivées de l'optimisation mais locales dans le temps : l'agent décide à partir de ce qu'il observe.
3. **Plusieurs approches viables.** Économie libérale et économie planifiée doivent être jouables, avec des forces et des faiblesses différentes, sans hiérarchie imposée.
4. **Émergence plutôt que script.** Inflation, chômage, cycles et crises résultent des interactions et des décisions, pas de tirages imposés.
5. **Cohérence stock-flux stricte.** Tout flux quitte un bilan pour entrer dans un autre ; aucune monnaie n'est créée ni détruite hors des mécanismes explicites. C'est un test permanent du moteur.

### 2.2 Sources et autorité

- La **spécification v3** (`docs/specification/`) fait foi pour le moteur.
- Les **décisions consignées** (ADR, fiches comparatives, décisions M-n) s'imposent jusqu'à leur révision explicite.
- La **spécification v1.5** et le **moteur v2.0** (`archive/`, temporaire) sont des sources historiques à instruire, pas des références. La v1.7 n'est pas utilisée (décision du 29/09/2026).
- Toute référence bibliographique est une publication retrouvée, qui soutient l'affirmation citée.

### 2.3 Choix d'approche par bloc

- L'approche de chaque bloc est retenue par le mainteneur, sur **fiche comparative**. La fiche présente les options v1.5, v2.0 et au moins une approche nouvelle quand il en existe une pertinente.
- La fiche est instruite par l'expert pilote et commentée par `jeu`.
- Aucune approche n'entre dans le moteur sans cette décision.

### 2.4 Statuts épistémiques

- Chaque équation porte un statut :
  - **dérivée** : obtenue d'un problème d'optimisation ou d'une identité ;
  - **approchée** : règle locale qui approche une solution optimale ;
  - **choix de conception** : sans fondement théorique, retenue pour le jeu.
- Chaque affirmation factuelle distingue :
  - ce que le **modèle produit**, qui se recalcule ;
  - ce qui est **établi**, avec source et date ;
  - ce qui est **contesté**.
- Un résultat du modèle n'est jamais présenté comme un fait empirique.

### 2.5 Grandeurs et critères

- Une grandeur porte sa **définition, son unité, son dénominateur et sa fenêtre**, dans les tableaux comme dans les critères.
- Un critère s'écrit **avant l'essai** et ne se déplace pas après observation. Une correction de critère mal posé est **prospective**, et l'ancien verdict reste publié.
- Une différence entre deux branches appariées mesure l'effet total d'une intervention sur la fenêtre exécutée, pas la cause unique d'un niveau de long terme.

### 2.6 État initial et test zéro

- L'état initial d'une simulation est **résolu comme équilibre des règles en vigueur**, sans préparation cachée.
- Vérification : dix ans sans choc, aucune dérive au-delà des tolérances déclarées.
- **Test zéro** : sur 60 ans sans choc depuis l'état initial, les ratios de stocks restent dans leurs bandes (O1).
- Toute modification d'une règle impose de résoudre à nouveau l'état initial.

### 2.7 Budget de complexité

- **Raffiner plutôt qu'ajouter** : chercher d'abord si un mécanisme manquant peut sortir d'une équation existante.
- Chaque équation, borne ou seuil a un paramètre déclaré et figure dans au moins un test.
- **Préférer un mécanisme à une borne**, et une correction sans retard à une correction avec retard. Toute borne est déclarée.
- Une vitesse d'ajustement ne doit pas déterminer l'état d'arrivée ; si elle le fait, le continuum d'équilibres est documenté.

### 2.8 Pistes écartées et instabilités connues

- Les pistes écartées par la première tentative sont maintenues, sauf argument nouveau : guerre, promoteurs immobiliers, intermédiation non bancaire détaillée, chaînes de valeur multi-frontières, sous-secteurs publics, statistiques truquées, compétitivité hors-prix endogène, épargne de précaution politique.
- Les instabilités connues ne se réintroduisent pas sans fait nouveau et test. Leur liste est dans la synthèse des faits mesurés d'`archive/`, puis dans la spécification.

### 2.9 Confidentialité

Le dépôt est public : aucun nom de pays réel n'est associé à une configuration ou à un archétype. Les dix configurations de validation restent des archétypes anonymisés.

## 3. Exigences documentaires

### 3.1 Spécification

- Un **fichier LaTeX unique**, `docs/specification/nations_et_marches.tex`, compilé en XeLaTeX sans erreur ni renvoi indéfini, dans la forme de la v1.5. Ses conventions sont dans `docs/specification/CONVENTIONS.md`.
- Le **PDF est versionné**, recompilé et commité avec chaque modification du `.tex`.
- Le document décrit le **moteur exécuté**, jamais une intention non codée. Une section « proposée » peut précéder le code ; elle est marquée comme telle.

### 3.2 Équations

Chaque équation numérotée comporte :
- un **label nommé** `eq:<bloc>-<nom>` ;
- un encadré **« Lecture »** en quatre rubriques : variables, sens, hypothèses, limites ;
- son **statut** (§ 2.4) ;
- sa **provenance** : v1.5, v2.0 ou nouvelle, avec la décision M-n qui l'a retenue ;
- ses **paramètres**, avec valeur, unité et source.

Aucun renvoi n'est écrit sous forme de numéro en dur.

### 3.3 Concordance

La concordance entre spécification et moteur est vérifiée par un script (`outils/concordance_spec_moteur.py --strict`), bloquant en CI : chaque label a exactement une balise dans le code, et réciproquement ; chaque nom de code cité existe.

### 3.4 Évolutions et chantiers

- Chaque version commence par une table **« Ce qui change en vX.Y »** : modification, section touchée, et ce que le moteur ou l'audit a révélé.
- Chaque version se termine par l'**état des chantiers** ouverts, honnêtement formulé : ce qui a été essayé, et pourquoi cela a échoué.

### 3.5 Fiches comparatives

Une fiche par bloc dans `docs/blocs/` (gabarit `docs/blocs/0000-gabarit.md`) : options, équations, comportement mesuré, coût, défauts connus, avis de l'expert pilote et de `jeu`, décision du mainteneur.

### 3.6 Cours magistral

Reporté au jalon J8. Il dérivera chaque bloc de la spécification v3 stabilisée. Les dérivations des volumes 1 et 2 de la première tentative, conservées dans `archive/`, seront reprises et corrigées.

## 4. Exigences d'architecture

### 4.1 Découpage

Moteur en couches (`CLAUDE.md`, « Architecture » ; ADR 0002) :
- noyau comptable ;
- blocs ;
- ordonnanceur et paramètres ;
- état ;
- observation ;
- scénarios ;
- leviers ;
- interface, sans calcul économique.

### 4.2 Outillage

- Python 3.12, géré par uv (`pyproject.toml`, `uv.lock`) ; NumPy ; pytest.
- Code en français, identifiants ASCII.

### 4.3 Reproductibilité

- Graine explicite par pays.
- Ordre canonique des pays dans toute agrégation.
- Sauvegarde et reprise exactes.
- Références de non-régression régénérées sur une plateforme de référence unique (ADR 0003).

### 4.4 Performance

- **Au plus 1 ms par pays-semaine**, mesuré par un test : 60 ans d'un pays en quelques secondes.
- Aucune optimisation itérative à chaque pas.
- Les historiques ne sont pas stockés dans l'état.

### 4.5 Invariances multi-pays (jalon J5)

- Tolérances relatives à l'échelle du bilan, jamais constantes absolues.
- Aucun solde de bilan calculé comme résidu sans justification.

## 5. Interface

### 5.1 Restitution du simulateur (jalon J4)

- Ligne de commande et rapports.
- Chaque indicateur affiché porte sa définition, son unité, son dénominateur et sa fenêtre, et provient du module d'observation.
- Un rapport de scénario indique la version du moteur (commit), les paramètres et la graine.

### 5.2 Interface web et jeu (jalon J7)

- Moteur Python côté serveur, client web.
- Tours mensuels.
- Plusieurs joueurs.
- Détail à préciser avant J7.

### 5.3 Règles communes

- Aucun calcul économique dans l'interface.
- Saisie contrôlée avec message explicite ; aucune donnée modifiée silencieusement.
- Erreurs restituées lisiblement.
