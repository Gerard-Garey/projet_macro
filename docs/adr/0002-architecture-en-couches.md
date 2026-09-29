---
status: accepted
date: 2026-09-29
---

# Moteur v3 en couches : un noyau comptable qui exécute tous les flux, des blocs sans état caché, un ordonnanceur à phases numérotées, un état sans historique

## Contexte

L'ADR 0001 (§ 1, 3 et 6 du contexte) mesure ce que coûte l'architecture du moteur v2.0 :

- un pas entier tient dans une méthode de 900 lignes qui est aussi un générateur ; toute modification d'un mécanisme oblige à lire l'ensemble, et rien ne s'isole pour un test ;
- les flux monétaires sont exécutés à plusieurs endroits (`Ledger.transfer`, `World._clear.pay`), avec des tolérances absolues (`1e-9*max(1, a)`) qui cassent l'invariance d'unité (arrêt en semaine 824 sous redénomination ×100, rapporté) ;
- l'état caché (`getattr` avec défaut) et les drapeaux de mode (`*_mode`, `eight_points.enable`, `audit_profile.enable`) font que l'équation lue n'est pas l'équation exécutée : huit hypothèses réfutées pour cette seule raison (rapporté) ;
- l'état porte ses historiques (≈ 70 Mo sur 72 Mo, mesuré le 29/09/2026), ce qui rend la sauvegarde lourde et mêle observation et trajectoire ;
- 70 % du temps passe dans une liste de 23 403 cohortes parcourue en Python pur et 18 % dans une résolution itérative de portefeuille à chaque pas (mesuré le 29/09/2026), pour 308,6 ms par semaine contre un budget de 1 ms par pays-semaine (M13) ;
- l'état initial est le produit de 150 ans de simulation, pas un équilibre des règles : le test zéro ne peut pas partir de t = 0.

Le mainteneur a accepté le 29/09/2026 le principe de l'architecture ci-dessous ; `CLAUDE.md`, « Architecture », la rend impérative depuis le commit `a5d873c`. Le présent ADR en donne la justification et les options écartées.

## Décision

Arrêtée par le mainteneur le 29/09/2026 (principe), consignée par `architect` le 29/09/2026.

### Couches (`src/nations/`)

1. **`noyau/`** — comptes : bilans, flux, grand livre. **Seul endroit où un flux monétaire s'exécute.** Après chaque phase, il vérifie les identités comptables avec une tolérance **relative à l'échelle du bilan** (somme des valeurs absolues des postes), jamais une constante absolue. Module le plus profond du moteur : une interface étroite (ouvrir un pas, proposer un flux, clore une phase) et toute la comptabilité derrière.
2. **`blocs/`** — un module par bloc de la spécification (production, travail, prix, ménages, investissement, banque, banque centrale, État…). Un bloc **lit l'état d'ouverture et rend des flux proposés et des variables nouvelles** ; il n'écrit pas dans les comptes. **Aucun état caché** (ni attribut créé à la volée, ni `getattr` avec défaut). **Aucun drapeau de mode** : une variante écartée sort du code et reste consignée dans sa fiche comparative.
3. **`moteur/`** — l'ordonnanceur, qui déroule les **phases numérotées d'un pas, identiques à celles de la spécification** (barrières entre pays au jalon J5), et les **paramètres typés**, chacun avec unité, source et étiquette d'équation, présent dans au moins un test.
4. **`etat/`** — schéma d'état typé et versionné ; sauvegarde et reprise exactes ; **aucun historique dans l'état**.
5. **`observation/`** — séries et exports, hors de l'état, **sans effet sur la trajectoire** (test de suppression : retirer l'observation ne change aucun résultat).
6. **`scenarios/`** — état initial **résolu comme équilibre des règles** (état stationnaire résolu), sans préparation cachée ; archétypes de pays anonymisés.
7. **`leviers/`** — commandes du joueur, typées, disponibles selon le régime de souveraineté A à E.
8. **Interface** (ligne de commande et rapports en J4, web en J7) : saisie, appel du moteur, restitution ; **aucun calcul économique**. Si un résultat peut être calculé indépendamment de l'interface, il va dans le moteur.

### Invariants transverses

9. **Concordance** : chaque `\label{eq:…}` de la spécification a exactement une balise `# eq:…` dans `src/`, et réciproquement ; `outils/concordance_spec_moteur.py --strict` le vérifie, bloquant en CI (ADR 0004).
10. **Déterminisme** : une graine explicite par pays ; un ordre canonique des pays (identifiant, jamais ordre des joueurs) dans toute somme ou agrégation ; une reprise de sauvegarde qui reproduit la trajectoire à l'identique.
11. **Budget de calcul** : au plus 1 ms par pays-semaine (M13), mesuré par un test ; aucune optimisation itérative à chaque pas ; les populations (cohortes, contrats) sont représentées par des agrégats, la forme exacte de chaque agrégat relevant de la fiche du bloc concerné.
12. **`archive/` n'est jamais importée ni modifiée** ; elle sert de source aux fiches comparatives.
13. **État initial** : équilibre des règles en vigueur ; vérification à dix ans sans choc, puis test zéro sur 60 ans depuis t = 0 (`docs/exigences.md` § 2.6). Toute modification d'une règle impose de résoudre à nouveau l'état initial.

## Options écartées

- **Monolithe par pays, avec un générateur qui rend la main aux barrières monde** (forme de la v2.0). Écarté : aucune localité (une évolution typique, ajouter un terme à une équation de prix, oblige à relire 900 lignes et à vérifier chaque `yield`), aucun test par bloc possible, et l'ordre des phases n'est lisible nulle part hors du code.
- **Drapeaux de mode pour garder plusieurs variantes d'un mécanisme dans le code.** Écarté : c'est la source directe des hypothèses réfutées de la première tentative (équation lue inactive). Une variante se compare dans la fiche comparative, le mainteneur tranche (M2), et le code ne porte que l'approche retenue. Comparer deux variantes en cours d'instruction se fait sur deux branches ou par un script dans `outils/`, jamais par un paramètre du moteur.
- **Flux exécutés par les blocs eux-mêmes**, le noyau se bornant à vérifier a posteriori. Écarté : c'est le schéma de la v2.0, où deux fonctions de paiement portaient deux tolérances ; le contrôle après coup ne dit pas quel bloc a rompu l'identité. Un point d'exécution unique rend l'identité comptable structurelle et localise toute violation dans la phase qui l'a produite.
- **Tolérance absolue** (`1e-9`, `1e-12`) sur les identités. Écarté : elle dépend de l'unité monétaire, donc casse l'invariance d'unité (objectif O4) ; la tolérance relative à l'échelle du bilan est la seule qui survive à une redénomination.
- **Historiques dans l'état** (séries, fenêtres glissantes stockées). Écarté : ils gonflent la sauvegarde, entrent dans le calcul (moyennes glissantes) et rendent la reprise inexacte si la fenêtre est tronquée. Une grandeur retardée dont une équation a besoin est une **variable d'état déclarée** (par exemple l'indice des prix d'il y a douze mois), pas un historique ; les séries vont dans `observation/`.
- **État initial préparé par une longue simulation** (150 ans dans la v2.0). Écarté : le test zéro ne part pas de l'état initial, la préparation masque une dérive lente, et l'état obtenu n'est pas recalculable à la main ; il ne peut pas non plus être fourni au joueur comme point de départ documenté.
- **Optimisation itérative à chaque pas** (résolution jointe de portefeuille, 18 % du temps mesuré). Écarté par l'invariant 11 : le budget de 1 ms l'exclut, et une règle en forme fermée donne un état stationnaire calculable. Le choix de la règle (consommation, portefeuille) reste ouvert dans les fiches, sous cette contrainte.
- **Calcul économique dans l'interface** (indicateurs dérivés calculés à l'affichage). Écarté : un indicateur qui n'existe que dans l'interface n'est ni testé ni concordant avec la spécification ; il va dans `observation/`.
- **Ordre des pays selon l'ordre des joueurs** dans les agrégations. Écarté : source de non-invariance à la permutation (objectif O4) ; l'identifiant de pays fixe l'ordre canonique.

## Conséquences

- **Fichiers** : `CLAUDE.md`, « Architecture » (déjà en place, commit `a5d873c`) ; `docs/exigences.md` § 4 ; fiche `coder.md` (conventions : balises `# eq:<label>`, pas d'état caché, tolérances relatives, graine par pays) ; fiche `audit.md` (défauts de la v2.0 à rechercher). L'issue #4 crée le squelette `src/nations/{noyau,blocs,moteur,etat,observation,scenarios,leviers}` et les batteries de vérification.
- **Effet sur les résultats** : aucun à ce jour (aucun résultat v3). Les invariants imposent des tests dès le jalon J2 : conservation exacte, reprise identique, invariance d'unité, budget de temps.
- **Ce qui reste à faire** : la fiche « temps et comptabilité » (jalon J1) fixe le pas et la matrice des flux avant que le noyau ne soit écrit ; le noyau (J2) peut démarrer dès qu'elle est tranchée.
- **Ce que l'ADR ne règle pas** : le contenu économique de chaque bloc (fiches comparatives, M2) ; la forme des barrières entre pays (J5) ; le protocole entre serveur et client web (J7). Toute modification d'un invariant de ce document passe par un nouvel ADR qui le cite.

Issues : #3, #4.
