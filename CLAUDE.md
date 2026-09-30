# CLAUDE.md

Ce fichier guide Claude Code (claude.ai/code) dans ce dépôt.

## Contexte

*Nations & Marchés* est un simulateur macroéconomique multi-pays à cohérence stock-flux, destiné à devenir un jeu multijoueur tour par tour mensuel. Chaque joueur y incarne un État (politique monétaire, finances publiques, cadre institutionnel) face à un secteur privé autonome qui réagit aux prix et aux décisions publiques.

Le projet reprend sur un **moteur neuf, dit « v3 »**, une première tentative : la spécification v1.5 et le moteur v2.0, dont l'échec est analysé dans l'ADR 0001. Les livrables, dans l'ordre des jalons de `docs/feuille-de-route.md` :
- la spécification LaTeX (`docs/specification/`) ;
- le moteur Python (`src/nations/`) ;
- un simulateur utilisable (J4) ;
- le jeu web (J7) ;
- un cours magistral (J8).

**Ce qui prime** :
- la **concordance exacte entre spécification et moteur** : toute équation active est documentée, toute équation documentée est exécutée ;
- la **reproductibilité** ;
- la **lisibilité des mécanismes pour le joueur**.

Le modèle n'est pas un outil de prévision : il doit produire des trajectoires qualitativement justes et explicables.

**Sources** : la spécification v3 fait foi pour le moteur. La spécification v1.5 et le moteur v2.0, rangés dans `archive/` (dossier temporaire, voué à disparaître), sont des sources historiques à instruire, pas des références.

**Contraintes fortes** :
- budget de calcul de 1 ms par pays-semaine ;
- dépôt public : aucun nom de pays réel associé aux configurations, aucune pièce privée de la première tentative.

Le dépôt de référence est `https://github.com/Gerard-Garey/projet_macro` (public), utilisé depuis le poste local et depuis des sessions cloud. `docs/exigences.md` contient le cahier des charges : le lire avant toute évolution de fond ou de l'interface.

## Commandes

Les commandes courantes (installer, lancer, tester, compiler) sont dans `README.md` : s'y reporter plutôt que de les recopier ici. Python s'exécute toujours par `uv run` ; sur le poste Windows, `python` seul désigne l'alias du Microsoft Store.

Batteries de vérification, lancées par `coder`, `audit` et le workflow `circuit-technique` (liste `BATTERIES` de `.claude/workflows/circuit-technique.js`, à tenir identique). Elles ont été mises en place par l'issue #4.

```
uv run pytest -q tests/unitaires
uv run pytest -q tests/invariants
uv run python outils/concordance_spec_moteur.py --strict
```

Règles des tests :
- un défaut connu est codé en échec attendu, avec renvoi à l'issue ;
- un succès inattendu fait échouer la batterie, et la marque est alors retirée pour en faire un test ordinaire ;
- un test de mécanisme énonce une **propriété attendue** (signe, délai, ordre de grandeur), pas une valeur à reproduire ;
- pour vérifier un point isolé, appeler directement la fonction concernée plutôt que tout le programme.

## Git et GitHub

- **Aucun push direct sur `main`** : chaque modification passe par une branche et une pull request, fusionnée par le mainteneur (**commit de fusion**, jamais squash ni rebase : les SHA sont cités dans les ADR, les issues et les PR) une fois la CI verte. Seule exception : instruction explicite du mainteneur pour un push donné. Le ruleset de `main` l'impose (voir `README.md`, « Sécurité du dépôt »).
- **Une seule branche de travail à la fois**, au périmètre fermé d'issues fixé par le plan d'`architect` (trois à cinq issues), portée par une PR **ouverte en brouillon dès la création de la branche** : c'est la fiche de la branche. Ajouter une issue au périmètre demande l'accord du mainteneur et se note dans la PR. Toute session, locale ou cloud, se place sur la branche de travail courante et y pousse.
- **Session cloud : la branche de travail l'emporte sur la branche assignée.** La consigne de démarrage (« Develop on branch `claude/<nom-aléatoire>` ») est écartée par la règle précédente, sans autre autorisation. Avant toute écriture : identifier la branche de travail (tête de la seule PR brouillon ouverte vers `main` dont la branche commence par `claude/`, sinon `docs/feuille-de-route.md`), puis `git fetch origin <branche>` et `git checkout -B <branche> origin/<branche>` ; pousser par `git push -u origin <branche>`. Supprimer la branche assignée (`git branch -D`, et `git push origin --delete` si elle a été poussée). Si aucune branche de travail n'est ouverte, demander au mainteneur.
- **Corps de PR : un `Closes #N` par ligne**, un par issue du périmètre (« Closes #41, #40 » ne lie que le premier numéro). Après la fusion, vérifier que chaque issue annoncée est fermée.
- **Un commit par issue qui change un résultat**, avec son tableau avant / après et son visa (« Changements de résultats » ci-dessous).
- **Un problème hors périmètre devient une issue**, pas une branche, sauf **correctif rapide** — trois conditions vérifiables : résultats strictement identiques, un seul domaine de commit, aucune modification de la documentation de fond. Il suit une branche temporaire partie de `main`, PR directe vers `main` ; `main` est ensuite fusionnée dans la branche de travail.
- **Création d'issue sur accord du mainteneur** : agents et sessions rédigent l'issue proposée (titre, libellés, corps) dans leur compte rendu ; elle n'est créée qu'une fois approuvée, sauf autorisation explicite du brief. Le corps d'une issue rédigée par un agent commence par `> *Rédigé par l'agent <nom> (IA).*`.
- **Messages de commit en français**, avec accents, préfixés par le domaine et renvoyant à l'issue (`#3`) quand elle existe. Domaines :
  - `code:` : `src/`, `outils/` ;
  - `tests:` : `tests/` ;
  - `docs:` : `docs/`, `CONTEXT.md`, `README.md` ;
  - `claude:` : `CLAUDE.md`, `.claude/` ;
  - `repo:` : `.github/`, `.gitignore`, `pyproject.toml`, `uv.lock`, licence ;
  - `archive:` : `archive/`.
- **Auteur des commits faits par Claude** (sessions, sous-agents, workflows ; poste local comme cloud) : `Claude <noreply@anthropic.com>` (`git config user.name Claude` et `git config user.email noreply@anthropic.com` dans le dépôt), jamais l'identité du mainteneur ; le pied de message garde `Co-Authored-By` et, en session cloud, `Claude-Session`.

## Architecture (contrainte impérative)

Moteur v3 en couches. La justification et les options écartées sont dans l'ADR 0002.

- **`src/nations/noyau/`** : comptes (bilans, flux, grand livre). C'est le **seul endroit où un flux monétaire s'exécute**. Après chaque phase, il vérifie les identités stock-flux avec une tolérance **relative à l'échelle du bilan**, jamais une constante absolue.
- **`src/nations/blocs/`** : un module par bloc de la spécification (production, travail, prix, ménages, investissement, banque, banque centrale, État…).
  - Un bloc lit l'état d'ouverture et rend des flux proposés et des variables nouvelles.
  - **Aucun état caché** : ni attribut créé à la volée, ni `getattr` avec valeur par défaut.
  - **Aucun drapeau de mode** : une variante écartée sort du code, et sa fiche comparative la consigne.
- **`src/nations/moteur/`** : l'ordonnanceur, qui déroule les phases numérotées d'un pas, identiques à celles de la spécification (barrières entre pays au jalon J5), et les paramètres typés, chacun avec unité, source et étiquette d'équation.
- **`src/nations/etat/`** : schéma d'état typé et versionné ; sauvegarde et reprise exactes ; **aucun historique dans l'état**.
- **`src/nations/observation/`** : séries et exports, hors de l'état, sans effet sur la trajectoire.
- **`src/nations/scenarios/`** : état initial **résolu comme équilibre des règles** (aucune préparation cachée) ; archétypes de pays.
- **`src/nations/leviers/`** : commandes du joueur, typées, disponibles selon le régime de souveraineté.
- **Interface** (restitution en J4, web en J7) : saisie, appel du moteur, restitution ; **aucun calcul économique**.

Invariants transverses :
1. **Concordance** : chaque `\label{eq:…}` de la spécification a exactement une balise `# eq:…` dans `src/`, et réciproquement. Le script `outils/concordance_spec_moteur.py` le vérifie en CI.
2. **Déterminisme** :
   - une graine explicite par pays ;
   - un ordre canonique des pays (identifiant, jamais ordre des joueurs) dans toute somme ou agrégation ;
   - une reprise de sauvegarde qui reproduit la trajectoire à l'identique.
3. **Budget de calcul** : au plus 1 ms par pays-semaine, mesuré par un test. Aucune optimisation itérative à chaque pas.
4. **`archive/` n'est jamais importée ni modifiée** : elle sert de source aux fiches comparatives.

Si un résultat peut être calculé indépendamment de l'interface, il va dans le moteur.

## Changements de résultats et reproductibilité

- À entrées, paramètres et graine identiques, le programme produit des résultats identiques ; toute source d'aléa a une graine explicite.
- Toute modification qui change un résultat est **identifiée, quantifiée et expliquée** : un **tableau avant / après** (grandeur, avant, après, écart, explication), une ligne par grandeur modifiée, chaque ligne expliquée par la modification ; une ligne inexpliquée est une régression à corriger, pas une référence à régénérer.
- **Visa** : tout changement d'un résultat final (état stationnaire de référence, verdict du test zéro ou d'un scénario) est soumis au mainteneur. Les autres changements sont validés par l'expert pilote du bloc (`macro` ou `monnaie`). Sans visa, rien n'est commité.
- Les références de non-régression (`tests/references/`) ne sont régénérées qu'après visa, par la session principale (jamais par un agent ni un workflow), avec `uv run python outils/regenerer_references.py` (créé avec les premières références). La plateforme de référence est fixée par l'ADR 0003.

## Rigueur

- **Une affirmation sur le comportement du code s'adosse à une mesure exécutée** (commande et sortie), citée dans le compte rendu. Une explication plausible non vérifiée est la façon la plus sûre d'introduire une erreur qui survit aux relectures.
- **Un chiffre ne se recopie pas, il se remesure** ; un chiffre qui vient d'une source (texte, publication) se vérifie contre cette source, citée.
- Ne fabriquer aucune référence, aucun numéro de page ni résultat ; si la source ne permet pas de conclure, l'écrire.
- Faire évoluer les livrables existants plutôt que les réécrire ; ne jamais remplacer silencieusement une méthode ni réintroduire une formule déjà corrigée.
- Exigences de fond propres au domaine, héritées de la première tentative (détail dans `docs/exigences.md` § 2) :
  - **une grandeur porte sa définition, son unité, son dénominateur et sa fenêtre**, dans les tableaux comme dans les critères ;
  - **un critère s'écrit avant l'essai** et ne se déplace pas après observation ; une correction de critère mal posé est prospective, et l'ancien verdict reste publié ;
  - **test zéro** : une référence n'est utilisable que si ses ratios de stocks sont stables sur 60 ans sans choc, **depuis l'état initial résolu** ; une transition longue n'est pas un état stationnaire ;
  - **avant d'invoquer une équation, vérifier qu'elle est active** dans la configuration exécutée, avec ses coefficients effectifs ;
  - **un résultat du modèle n'est pas un fait empirique** : distinguer ce que le modèle produit, ce qui est établi (avec source et date) et ce qui est contesté ;
  - **toute borne est déclarée** ; préférer un mécanisme à une borne ;
  - **une vitesse d'ajustement ne doit pas déterminer l'état d'arrivée** ; si elle le fait, le modèle a un continuum d'équilibres, et il faut le dire ;
  - **ne pas réintroduire une instabilité connue** sans fait nouveau (liste dans la synthèse des faits mesurés d'`archive/`, puis dans la spécification).

Le vocabulaire du projet est défini dans `CONTEXT.md` : l'employer tel quel dans le code, la documentation et les issues.

## Sous-agents

Huit sous-agents de projet (`.claude/agents/`), orchestrés par la session principale. Règle de séparation : **ceux qui écrivent ne vérifient pas, ceux qui vérifient n'écrivent pas**.

| Famille | Agent | Écrit | Question |
|---|---|---|---|
| Pilotage | `architect` | `docs/adr/`, `CONTEXT.md`, `docs/feuille-de-route.md`, `docs/blocs/README.md` | Dans quel ordre, avec quels agents, sous quelle forme ? |
| Fond | `macro` | rien (avis, fiches comparatives, issues proposées) | Est-ce juste : économie réelle, bouclage stock-flux, état stationnaire, finances publiques ? |
| Fond | `monnaie` | rien (avis, fiches comparatives, issues proposées) | Est-ce juste : banque centrale, anticipations et crédibilité, banques et crédit, dette publique et prime, change, actifs et crises financières ? |
| Fond | `jeu` | rien (avis, issues proposées) | Le mécanisme est-il lisible, perceptible à l'échelle d'une partie, équilibré entre stratégies ? |
| Réalisation | `coder` | code, tests (pas la spécification) ; surface d'impact documentaire dans le commit proposé | Comment l'implémenter ? |
| Réalisation | `docwriter` | spécification (`docs/specification/`) | Spécification juste, rigoureuse, concordante avec le moteur ? |
| Vérification | `audit` | rien (rapport) | Code correct et reproductible ? |
| Vérification | `app-review` | rien (rapport) | Restitution et interface conformes à `docs/exigences.md` ? |

**Experts de fond.**
- Dans ce document et dans le workflow `circuit-technique`, « expert » désigne l'**expert pilote** du sujet : `macro` ou `monnaie`, selon le bloc. L'inventaire des blocs `docs/blocs/README.md` et l'issue le désignent.
- `jeu` donne son avis sur chaque fiche comparative et sur toute question de jouabilité ; il ne tranche pas le fond économique.
- Un sujet à la frontière consulte `macro` et `monnaie` : l'inflation (prix et salaires chez l'un, anticipations chez l'autre), le crédit, la dette publique. En cas de désaccord entre experts, le mainteneur tranche.

**Routage du modèle et de l'effort** (`docs/agents/routage.md`, ADR 0005) — `architect`, `macro`, `monnaie` et `jeu` existent en deux fiches au même corps : la fiche de base (Opus, effort `medium`, routine) et la fiche `-approfondi` (Opus, effort `high`, jugement), générée par `bash .claude/outils/fiches_jumelles.sh` et contrôlée par la CI ; ne jamais modifier une fiche `-approfondi` à la main. La session principale choisit la fiche selon la matrice de `docs/agents/routage.md` (§ 3) et ne passe `model: "fable"` à l'appel que dans les cas du § 4.1 (échec documenté d'Opus `high`, désaccord entre agents, rédaction d'un ADR d'architecture) ou sur accord du mainteneur ; au plus une relance ciblée, une hausse d'effort et une consultation Fable par question, trois consultations Fable par branche sans nouvel accord ; un modèle indisponible arrête le circuit (aucun remplacement silencieux). Les agents signalent les critères rencontrés dans leur bloc « Retour », ils ne décident pas de leur escalade ; la session note chaque escalade d'une ligne dans la PR.

**Choix d'approche.** Pour chaque bloc, l'origine de l'approche retenue (v1.5, v2.0 ou nouvelle) est **décidée par le mainteneur** sur **fiche comparative** (`docs/blocs/<bloc>.md`, gabarit `docs/blocs/0000-gabarit.md`), jamais par un agent. La fiche est instruite par l'expert pilote et commentée par `jeu`. La décision est numérotée (M-n) dans `docs/feuille-de-route.md`.

**Déclencheurs** — un agent n'entre dans le circuit que si la modification touche son domaine :
- plusieurs issues ou forme du code → `architect` en amont ;
- question de fond (méthode, équation, règle de comportement, calibration) → l'expert pilote : spécification en amont, validation en aval ;
- mécanisme visible par le joueur (levier, indicateur, délai, coût) → `jeu` ;
- code → `audit` ;
- restitution ou interface → `app-review` ;
- spécification → `docwriter`, en dernier, une seule fois par branche (règle 9).

**Circuits types** (chacun se termine par un ou plusieurs commits de la session principale sur la branche de travail) :

1. **Évolution de fond** : fiche comparative (expert pilote, avis de `jeu`) → décision du mainteneur → `coder` → `audit` (+ `app-review` si la restitution change) → `docwriter` (en fin de branche) → l'expert pilote valide.
2. **Correction de fond** (écart à la spécification) : l'expert pilote établit la lecture de la spécification → le mainteneur tranche si un résultat final change → `coder` → `audit` → l'expert pilote contrôle la conformité → `docwriter`.
3. **Correction technique** : `coder` → `audit` (workflow `circuit-technique`).
4. **Documentation seule** : `docwriter` (+ l'expert pilote si le fond change).

Un constat bloquant ou majeur d'un vérificateur renvoie à l'étape de réalisation. Quand la spécification ou une source admet deux lectures, l'expert pilote les décrit et donne son avis, le mainteneur tranche.

**Workflows** (`.claude/workflows/`). Un workflow met en œuvre un circuit type et en fixe les appels d'agents, les sorties structurées et les conditions d'arrêt. Huit principes :

1. lancement **sur commande explicite du mainteneur** uniquement ;
2. **aucune écriture dans l'historique ni l'état partagé** par le workflow ou ses agents : ni `git commit`, ni `git push`, ni régénération de référence, ni création d'issue — interdiction portée par les consignes et les fiches, les permissions de `.claude/settings.json` ne l'imposant pas : la session principale vérifie `git status` et `git log` après chaque workflow ;
3. **arrêt avec les rapports à tout point de décision** (question de fond, visa du mainteneur, contradiction entre vérificateurs) ;
4. **au plus une reprise** `coder` → `audit` ;
5. **vérificateurs ciblés sur le diff** (audit léger) ;
6. **constats structurés** : gravité (bloquant / majeur / mineur), `fichier:ligne`, mesure exécutée ; un constat sans emplacement ni mesure n'est pas recevable ;
7. **tout contrôle mécanique est un script**, jamais un agent : un agent lit la sortie d'un script, il ne refait pas le décompte ; un contrôle récurrent sans script en appelle un (issue) ;
8. **effort réduit** pour les étapes mécaniques ; aucun `model` fixé dans un workflow (hérité de la session).

Un **constat** (défaut du code) conduit à la reprise ou à l'arrêt ; une **question pour l'expert** (doute de `coder`, question de l'audit) ne relance pas `coder`. Trois statuts de fin : `termine`, `termine avec questions` (les seules remontées sont des questions : la session principale les porte à l'expert pilote avant tout commit), `arrete` ; une batterie en échec à la dernière vérification finit toujours par `arrete`.

**Règle 9 — un seul passage de `docwriter` par branche** : `docwriter` intervient une fois, en fin de branche, sur l'état final du code, avec **un commit `docs:` par issue** ; `coder` ne modifie pas la spécification et liste dans chaque commit proposé la **surface d'impact documentaire** (sections, tableaux, décomptes, fonctions citées), dont `docwriter` part ; l'expert pilote valide le diff de la spécification une fois, en fin de branche. Exceptions : commit `docs:` préparatoire qui protège la suite, branche où le document porte la décision et précède le code (spécification d'un bloc au jalon J1), écart de concordance qui ferait échouer la CI (commit `docs:` minimal, aussitôt).

**Règle 10 — audit léger en cours, revue finale complète avant la sortie du brouillon** : pendant l'implémentation, `audit` (et `app-review`) se limitent au diff et aux fonctions touchées avec leurs appelants et appelés ; avant la sortie du brouillon, revue finale complète du `git diff main...HEAD` entier (fonctions touchées avec appelants et appelés, batteries complètes, scénarios adverses, cohérence code ↔ tests ↔ documentation) par les vérificateurs que désignent les déclencheurs, plus `/code-review` ; toute correction postérieure est revue à son tour, sur son diff. La relecture intégrale hors diff est réservée aux jalons de livraison.

**Revues périodiques**, hors de tout changement :
- `architect` : point d'étape et feuille de route, après chaque série de PR fusionnées ;
- `macro` et `monnaie` : revue de fond avant chaque jalon ;
- `jeu` : revue de jouabilité avant chaque démonstration ;
- `app-review` et `docwriter` : relecture intégrale avant démonstration ou livraison.

## Décisions et vocabulaire

- **ADR** (`docs/adr/NNNN-titre-court.md`, gabarit `docs/adr/0000-gabarit.md`) : toute décision d'architecture ou d'organisation, et toute piste rejetée pour une raison qu'un futur relecteur devrait connaître. Rédigés par `architect` ; une décision du mainteneur y est datée. Une proposition qui contredit un ADR le signale explicitement et dit pourquoi le rouvrir.
- **Fiches comparatives** (`docs/blocs/`) : une par bloc de la spécification ; options, mesures, avis, puis décision du mainteneur. Elles restent la trace de l'origine de chaque équation.
- **`CONTEXT.md`** : glossaire du domaine et de l'organisation.
- **`docs/feuille-de-route.md`** : périmètre de la branche de travail en cours et des suivantes, jalons, décisions du mainteneur numérotées (M1, M2…).

## Agent skills

### Issue tracker

Issues et specs dans les GitHub Issues du dépôt : outils `mcp__github__*` en session cloud, CLI `gh` sur le poste local. Voir `docs/agents/issue-tracker.md`.

### Triage labels

Les cinq libellés canoniques (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). Voir `docs/agents/triage-labels.md`.

### Domain docs

Mono-contexte : un `CONTEXT.md` et `docs/adr/` à la racine. Voir `docs/agents/domain.md`.
