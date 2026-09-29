# Glossaire

Vocabulaire à employer tel quel dans le code, la documentation, les issues et les comptes rendus d'agents. Un terme nouveau ou précisé est ajouté par `architect`. Les termes économiques propres à un bloc (symboles, paramètres) sont définis dans le glossaire de la notation de la spécification ; ce fichier fixe les termes qui structurent le projet.

## Domaine : le projet

- **Nations & Marchés** : le projet — simulateur macroéconomique multi-pays à cohérence stock-flux, puis jeu multijoueur tour par tour mensuel.
- **Simulateur** : moteur, scénarios, leviers et restitution, sans couche de jeu (jalons J1 à J4). *Ne pas dire* : prototype, pour la v3.
- **Jeu** : couche ajoutée au simulateur au jalon J7 : partie, joueurs, tours, IA des pays non joueurs, conditions de fin.
- **Joueur** : personne qui incarne l'**État** d'un pays ; elle fixe le cadre (politique monétaire, finances publiques, institutions) et ne produit pas elle-même, sauf en mode planifié.
- **Pays** : économie nationale simulée, avec ses ménages, entreprises, banque commerciale, banque centrale et État. Identifié par un **identifiant de pays**, qui fixe l'ordre canonique des agrégations. *Ne pas dire* : nation, joueur (pour le pays).
- **Mainteneur** : responsable du projet ; il arbitre les choix de conception, de jeu et de périmètre, décide l'approche de chaque bloc et vise les changements de résultats finals.

## Domaine : versions et sources

- **Moteur v3** : le moteur en cours d'écriture dans `src/nations/`. *Ne pas dire* : v2, nouveau prototype.
- **Spécification** : le document LaTeX `docs/specification/nations_et_marches.tex`, qui fait foi pour le moteur v3. *Ne pas dire* : document chapeau (terme de la première tentative, réservé aux versions archivées).
- **Première tentative** : travaux antérieurs au 29/09/2026 — spécification v1.5 et moteur v2.0, conservés dans `archive/`.
- **Spécification v1.5** : document de conception de la première tentative (104 p., 65 équations numérotées) ; source historique à instruire, pas une référence.
- **Moteur v2.0** : moteur Python de la première tentative (profil W10 + P1 + R3, état D1), archivé sans ses suites de tests ; source historique à instruire. *Ne pas dire* : prototype (sans préciser v2.0).
- **v1.7** : version intermédiaire de la première tentative (spécification et prototype) ; **non utilisée** dans ce projet.
- **Archive** : dossier `archive/`, temporaire, en lecture seule, jamais importé par le moteur ; supprimé au plus tard à la fin du jalon J6.
- **Fait mesuré** : chiffre établi par exécution et reproduit ; il porte sa définition, sa fenêtre et la commande ou le rapport qui l'établit. *Ne pas dire* : résultat, sans préciser s'il est mesuré, rapporté ou calculé.

## Domaine : le modèle

- **Bloc** : partie de la spécification et du moteur qui porte un mécanisme économique cohérent (production, travail, prix, ménages, investissement, banque, banque centrale, État…) ; un module de `src/nations/blocs/`, une section de la spécification, une fiche comparative.
- **Socle** : ensemble des blocs de l'économie fermée à un pays (jalons J1 à J3).
- **Pas** : unité de temps du moteur (semaine ou mois, choix de la fiche « temps et comptabilité »). *Ne pas dire* : tick, tour (le tour est l'unité du jeu).
- **Date de décision** : pas où les décisions mensuelles (politique économique, salaires, anticipations) sont révisées.
- **Tour** : dans le jeu, intervalle entre deux décisions des joueurs (un mois).
- **Phase** : étape numérotée d'un pas, dans l'ordre fixé par la spécification et exécuté par l'ordonnanceur.
- **Noyau comptable** : couche du moteur qui tient les bilans et le grand livre, exécute tous les flux monétaires et vérifie les identités stock-flux.
- **Cohérence stock-flux** : tout flux quitte un bilan pour entrer dans un autre ; les matrices des bilans et des flux se bouclent. *Ne pas dire* : SFC, sans l'avoir défini.
- **Identité comptable** : égalité qui doit tenir par construction (bilan, conservation de la monnaie) ; sa violation est un défaut, jamais un ajustement.
- **Échelle du bilan** : somme des valeurs absolues des postes du bilan concerné ; dénominateur de toute tolérance sur un montant.
- **État d'ouverture / état de clôture** : valeurs d'une variable au début et à la fin d'un pas ; toute grandeur publiée précise laquelle.
- **Paramètre** : constante du moteur, déclarée avec valeur, unité, source et étiquette d'équation. *Ne pas dire* : coefficient magique, réglage.
- **Levier** : commande du joueur (taux directeur, taux d'imposition, dépense, émission de dette, avances…), typée et disponible selon le régime de souveraineté. *Ne pas dire* : bouton, option.
- **Régime de souveraineté** : classe A à E qui fixe les leviers disponibles d'un pays (A émetteur souverain, B membre d'une union, C petit pays à monnaie propre, D économie partiellement dollarisée, E ancrage unilatéral rigide).
- **Configuration** : archétype anonymisé de pays servant à la validation (dix dans la v1.5) ; jamais associé à un pays réel.
- **État stationnaire résolu** : état initial calculé comme équilibre des règles en vigueur, sans préparation cachée. *Ne pas dire* : état préparé (réservé à l'état D1 de la v2.0, obtenu par 150 ans de simulation).
- **Test zéro** : 60 ans de simulation sans choc depuis l'état stationnaire résolu ; les ratios de stocks doivent rester dans leurs bandes.
- **Fenêtre de partie / fenêtre longue** : horizon d'une partie depuis l'état initial / horizon de 60 ans ; les verdicts se publient sur les deux.
- **Scénario** : simulation définie par un état initial, des paramètres, une graine et une suite de leviers ; reproductible.
- **Contrôle apparié** : simulation de référence partant du même état et de la même graine qu'une branche, pour mesurer l'effet d'une intervention.
- **Pays-semaine** : une semaine simulée d'un pays ; unité du budget de calcul (au plus 1 ms).

## Domaine : l'instruction des blocs

- **Fiche comparative** : document `docs/blocs/<bloc>.md` qui présente les options d'un bloc (v1.5, v2.0, nouvelles), leurs équations, comportement mesuré, coût et défauts, l'avis de l'expert pilote et de `jeu`, puis la décision du mainteneur.
- **Expert pilote** : expert de fond (`macro` ou `monnaie`) désigné pour un bloc par `docs/blocs/README.md` ; il instruit la fiche, spécifie en amont et valide en aval. Dans `CLAUDE.md` et le workflow, « expert » le désigne.
- **Provenance** : origine d'une équation retenue — v1.5, v2.0 ou nouvelle — avec la décision M-n qui l'a retenue.
- **Statut d'équation** : *dérivée*, *approchée* ou *choix de conception* (`docs/exigences.md` § 2.4).
- **Décision M-n** : décision du mainteneur, numérotée dans `docs/feuille-de-route.md`.

## Organisation du travail

- **Branche de travail** : l'unique branche `claude/…` en cours, au périmètre fermé d'issues, portée par une PR brouillon vers `main`.
- **Correctif rapide** : modification hors périmètre qui laisse les résultats strictement identiques, touche un seul domaine de commit et pas la documentation de fond ; branche temporaire partie de `main`, PR directe.
- **Tableau avant / après** : pour un commit qui change un résultat, une ligne par grandeur modifiée (avant, après, écart, explication).
- **Visa** : approbation d'un tableau avant / après — par le mainteneur pour un résultat final ou un verdict, par l'expert pilote sinon. Sans visa, rien n'est commité.
- **Surface d'impact documentaire** : liste, dans le commit proposé par `coder`, des endroits de la spécification que la modification oblige à rouvrir ; point de départ de `docwriter`.
- **Constat** : défaut du code relevé par un vérificateur, avec gravité (bloquant / majeur / mineur), `fichier:ligne` et mesure exécutée. Conduit à une reprise ou à un arrêt.
- **Question pour l'expert** : doute sur le fond, qui n'est pas un défaut du code ; ne relance pas `coder`.
- **Audit léger** : lecture du diff et des fonctions touchées avec leurs appelants et appelés.
- **Revue finale complète** : lecture de tout `git diff main...HEAD`, batteries complètes et scénarios adverses, avant la sortie du brouillon.
- **Mesure** : commande exécutée et sa sortie, qui fonde une affirmation sur le comportement du code.
