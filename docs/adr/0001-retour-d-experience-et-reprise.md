---
status: accepted
date: 2026-09-29
---

# Reprendre le projet sur un moteur v3 modulaire, écrit bloc par bloc, en archivant la première tentative

## Contexte

*Nations & Marchés* a connu une première tentative, close le 21/09/2026 : une spécification v1.5 (104 p., 65 équations numérotées) et un moteur Python v2.0 (profil W10 + P1 + R3, état de référence D1), travaillés lors des sessions G à K (14 au 21/09/2026). Le 29/09/2026, le mainteneur a jugé cette tentative « plutôt ratée » et a demandé un retour d'expérience avant de repartir. Les constats ci-dessous distinguent ce qui a été **mesuré** le 29/09/2026 (sur le poste Windows du mainteneur, Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, un seul fil BLAS), ce qui a été **lu** dans le code, et ce qui est **rapporté** par les comptes rendus des sessions G à K.

### 1. Un moteur de recherche, pas un moteur de jeu

- **Lu** : `model.py` fait 1 986 lignes ; la méthode `Economy._step_normal`, qui déroule un pas, en fait 900 (l. 601 à 1501) et est un générateur qui rend la main aux barrières monde de `worldn.py`. L'état caché passe par `getattr(self, 'x', défaut)`. Deux profils greffés (`eight_points.enable`, `audit_profile.enable`) modifient le comportement.
- **Mesuré** : l'état D1 contient 323 paramètres et 228 clés d'état ; il pèse 72 Mo, dont environ 70 Mo d'historiques (`flow_history` 24 Mo, `mortgage_vintages` 11 Mo, `monetary_history` 10,6 Mo…) ; 23 403 cohortes hypothécaires y sont tenues en liste de dictionnaires parcourue en Python pur.
- **Lu** : des dizaines de modes (`*_mode`, drapeaux) ; le profil D1 diffère des valeurs par défaut sur de nombreux paramètres (`a_pi` 1,5 contre 0,5 ; `portfolio_mode='joint_equity'` ; `wiu_epsilon=0,03` ; `tax_rule` ; `rstar_anchor='deposit_wedge'`…). **Rapporté** : huit hypothèses ont été réfutées du 14 au 17/09/2026 parce qu'une équation lue dans le code était inactive dans le profil exécuté.

### 2. Une référence économique en échec

- **Mesuré** au chargement de D1 : t = 20 280 semaines (soit 390 ans, dont 150 ans de préparation invisible pour construire l'état), `cred = 0`, `pi_e = 0,0399`, `i_cb = 0,0918`.
- **Rapporté** (sessions G à K, reproduit par le vérificateur pour le contrôle G1 sur 260 semaines) : inflation moyenne d'environ 4,05 % pour une cible de 2 % (moyenne des glissements annuels hebdomadaires) ; **rapporté, non reproduit** (D1 sur 60 ans) : crédibilité nulle sur 3 120 semaines sur 3 120, taux réel directeur 5,1 %.
- **Lu** (`model.py` l. 1305, vérifié en session K) : la loi de crédibilité est piégée : le bonus `nu1` ne joue que si |π − π*| < `eps_bar` = 1 point ; au-delà, seule la pénalité agit, et une crédibilité offerte se vide d'environ un point par an (mesure K1 rapportée : 0,963 à 5 ans, 0,769 à 30 ans).

### 3. Une vitesse incompatible avec un jeu

- **Mesuré** : 308,6 ms par semaine simulée sur 52 semaines depuis D1, soit environ 16 minutes pour 60 ans d'un seul pays. Le profil sur 26 semaines met environ 70 % du temps dans `mortgage_vintages` et environ 18 % dans `joint_solver._solve` (résolution itérative de portefeuille à chaque pas).
- **Rapporté** : un compte rendu antérieur annonçait 0,06 s par semaine (autre machine, état antérieur) ; la v1.7 aurait fait 200 ans en « une dizaine de secondes ». Aucun de ces deux chiffres n'a été remesuré.

### 4. Une documentation qui ne décrit pas le code exécuté

La v1.5 décrit une intention ; le document du moteur v2.0 exécuté, dont la rédaction avait été rendue prioritaire le 19/09/2026, n'a jamais été écrit ; le cours (volumes 1 et 2) décrit une version antérieure à la v1.4. La v1.5 elle-même porte des incohérences internes : convention calendaire (4 pas par mois, 52 par an), numéros d'équation en dur, totaux de tests discordants, paramètres retirés encore employés, symboles à plusieurs sens, matrice des flux absente sous forme de tableau.

### 5. Un processus plus coûteux que le travail

Cinq intervenants (un assistant exécutant, un assistant superviseur sans exécution, un vérificateur, un planificateur, le mainteneur arbitre), échanges par fichiers, PDF et manifestes de sommes de contrôle. Le correctif K2c, qui touchait deux blocs de `worldn.py`, est resté ouvert après trois tours. **Les sessions G à K n'ont modifié aucune équation économique** : seulement des exports diagnostiques.

### 6. Pas de couche de jeu, et des défauts d'invariance

Ni leviers du joueur, ni boucle de tour, ni interface, ni état initial jouable. **Rapporté** (H2, J2, K2b) : les soldes résiduels `Res` et `L_cb` dérivent par arrondi (test de permutation : premier franchissement de 1e−12 de l'échelle du bilan en semaine 910) ; la tolérance `1e-9*max(1, a)` de `World._clear.pay` et de `Ledger.transfer` n'est pas homogène (arrêt en semaine 824 sous redénomination ×100, sur un paiement demandé de −1,86e−9 alors que le dépôt vaut 5,7e6).

### 7. Pièces manquantes

Ne sont plus disponibles : le prototype et le document v1.7 ; les suites de tests du moteur v2.0 (`tests.py` à `tests5.py`, `test_zero.py`, `w10_checks.py`, `audit3.py`, `run_suites.py`) ; `config/reference.json`, sans lequel `simulate.py` et `World.homogeneous()` ne s'exécutent pas ; le plan du cours et le relevé d'erreurs de la v1.5. Le moteur v2.0 n'est donc pas exécutable tel quel hors de son état D1.

### 8. Ce qui est acquis

- Les principes de conception (`docs/exigences.md` § 2.1) : un joueur = un État, secteur privé autonome, plusieurs approches viables, émergence plutôt que script, cohérence stock-flux stricte.
- Le grand livre et ses contrôles comptables.
- Trois acquis mesurés par la première tentative (rapportés, reproduits pour G1) : **P1**, la cible de levier des firmes, qui stabilise les stocks ; **R3**, le terme de demande dans le prix (sans lui, le chômage passe à 16,44 %, le PIB final perd 13,80 % et le prix de l'équipement monte de 65,86 % sur 260 semaines) ; **WS-PS**, qui donne le bon partage de la valeur ajoutée ; et le résultat stock-flux « la propension à consommer ne fixe pas la dépense ».
- Les listes d'instabilités connues et d'hypothèses réfutées ; la forme de la v1.5 (encadrés « Lecture », régimes A à E, grille des dix configurations) ; l'étiquetage épistémique (mesuré, lu, calculé, hypothèse).

### Pourquoi la décision du 19/09/2026 est rouverte

Le 19/09/2026, la première tentative avait arrêté : « pas de reconstruction du prototype v2.0 ; priorité au document v2.0 du moteur exécuté ». Cette décision reposait sur trois prémisses : le moteur v2.0 était la base à conserver, il suffisait de le documenter, et le processus à cinq intervenants continuait. Les trois sont tombées le 29/09/2026 :

1. **Faits nouveaux mesurés.** La vitesse (308,6 ms par semaine) est trois cents fois au-dessus du budget qu'un jeu tour par tour exige (M13 : 1 ms par pays-semaine) ; l'état de référence n'est pas un équilibre des règles mais le produit de 150 ans de simulation ; la référence échoue sur ses propres critères (inflation, crédibilité, taux réel). Documenter ce moteur reviendrait à documenter un échec.
2. **Base non exécutable.** Sans ses suites de tests ni `config/reference.json`, le moteur v2.0 ne se relance pas hors de D1. La « non-reconstruction » n'a plus d'objet : il n'y a pas de base opérationnelle à préserver.
3. **Objectif et organisation changés.** L'objectif n'est plus de finir un prototype de recherche mais de livrer un simulateur, puis un jeu (M4) ; l'organisation passe à un seul exécutant (M11) avec des experts de fond. La décision du 19/09/2026 arbitrait un coût de coordination qui n'existe plus.

Le présent ADR ne contredit pas le fond de la décision du 19/09 : personne ne « reconstruit le prototype v2.0 ». Il l'annule en changeant de projet : un moteur neuf, dit v3, dont chaque bloc est instruit contre la v1.5 et la v2.0 comme sources historiques.

## Décision

Arrêtée par le mainteneur le 29/09/2026 (décisions M1 à M15 de `docs/feuille-de-route.md`, § 4 ; M17, prise le même jour, précise M6) :

1. **M1 — Nouveau moteur modulaire « v3 »**, écrit bloc par bloc dans `src/nations/` ; la spécification v1.5 et le moteur v2.0 servent d'archives de référence, jamais de code importé.
2. **M2 — Le mainteneur tranche lui-même**, bloc par bloc, l'origine de chaque approche (v1.5, v2.0 ou nouvelle), sur fiche comparative (`docs/blocs/<bloc>.md`, ADR 0004). Aucun agent ne décide à sa place.
3. **M3 — Des approches autres** que celles de la v1.7 et de la v2.0 sont bienvenues, appuyées sur des références vérifiées.
4. **M4 — Simulateur d'abord** (jalons J1 à J4) ; jeu tour par tour mensuel à terme (J7).
5. **M5 — Interface cible : navigateur web**, moteur Python côté serveur ; restitution en ligne de commande d'abord (J4).
6. **M6 — Dossier `archive/`** dans le dépôt, avec le strict nécessaire aux premiers essais de la v3, voué à être supprimé (au plus tard à la fin du jalon J6). Contenu : source `.tex` de la v1.5, code v2.0 sans l'état D1, synthèse des faits mesurés des sessions G à K, PDF des volumes 1 et 2 du cours. Exclus : toute correspondance entre configurations et pays réels, tout lien vers un stockage privé, les notes de supervision, les archives compressées. **M17 (29/09/2026)** : les pièces sont versées **intactes**. Le source v1.5 et le cours citent des pays réels comme épisodes historiques et en bibliographie seulement, jamais dans la grille des dix configurations ; la règle du dépôt public est « aucun nom de pays réel associé aux configurations » (`docs/exigences.md` § 2.9), et le critère de l'issue #5 (« aucune occurrence ») est corrigé en ce sens.
7. **M7 — Premier jalon économique : économie fermée, un pays** (le socle).
8. **M8 — Spécification en LaTeX, forme de la v1.5**, selon l'ADR 0004.
9. **M9 — Trois experts de fond** : `macro`, `monnaie`, `jeu`.
10. **M10 — On se passe de la v1.7** : ni prototype ni document (pièces indisponibles, § 7 du contexte).
11. **M11 — Claude seul sur le dépôt**, sans autre flux d'assistants.
12. **M12 — Les six objectifs du 17/09/2026, reformulés « simulateur d'abord »**, fondent `docs/exigences.md` § 1.3.
13. **M13 — Budget de calcul : au plus 1 ms par pays-semaine.**
14. **M14 — Code en français, identifiants ASCII** ; commentaires et docstrings en français avec accents ; symboles courts admis quand la spécification les nomme (`pi_e`, `i_cb`).
15. **M15 — Cours magistral reporté au jalon J8.**

## Options écartées

- **Poursuivre le moteur v2.0 : le documenter, puis le refactoriser** (décision du 19/09/2026). Écartée pour les trois raisons données ci-dessus : faits nouveaux, base non exécutable, objectif changé. Le coût d'un refactoring de `_step_normal` (900 lignes, générateur, 323 paramètres, état caché) aurait dépassé celui d'une écriture bloc par bloc, sans garantir la vitesse.
- **Reprendre la v1.7** (prototype réputé plus rapide, document d'environ 108 p.). Écartée (M10) : les pièces sont introuvables, et le chiffre de vitesse est rapporté, non remesuré.
- **Réécrire le moteur v2.0 « à l'identique » sous une forme propre.** Écartée : cela transporterait la loi de crédibilité piégée, l'état préparé par 150 ans de simulation et la référence à 4 % d'inflation. Chaque bloc doit être réinstruit, la v2.0 n'étant qu'une option parmi d'autres (M2, M3).
- **Conserver le processus à cinq intervenants**, en le resserrant. Écartée (M11) : les sessions G à K ont produit des exports diagnostiques et aucune équation ; le vérificateur doit exécuter, et tous les artefacts vont dans git (fin des manifestes et des échanges par fichiers).
- **Commencer par le jeu ou l'interface web.** Écartée (M4, M5) : sans économie de référence fiable (objectif O1), il n'y a rien à jouer ; l'interface ne calcule rien et peut attendre.
- **Commencer en économie ouverte à N pays.** Écartée (M7) : les défauts d'invariance multi-pays (§ 6 du contexte) se corrigent dans le noyau comptable, testable dès un pays ; les barrières entre pays arrivent au jalon J5.
- **Écrire le cours en parallèle de la spécification.** Écartée (M15) : les volumes existants décrivent une version antérieure à la v1.4 et comportent des corrigés faux ; le cours dérivera d'une spécification v3 stabilisée.

## Conséquences

- **Fichiers** : `CLAUDE.md` (contexte, architecture, rigueur, sous-agents), `docs/exigences.md`, `CONTEXT.md`, huit fiches d'agents `.claude/agents/` et le modèle de PR ont été adaptés par l'issue #2 (commits `a5d873c`, `75e2cc6`, `377bda3`). Le présent ADR, l'ADR 0002 (architecture), l'ADR 0003 (outillage) et l'ADR 0004 (documentation) consignent le reste de la reprise ; `docs/feuille-de-route.md` porte les jalons et les décisions M-n.
- **`archive/`** est constitué par l'issue #5, en lecture seule, jamais importé (invariant 4 de `CLAUDE.md`, « Architecture »), pièces versées intactes (M17). Sa synthèse des faits mesurés recopie les définitions et fenêtres depuis les rapports d'origine, pas depuis un résumé.
- **Effet sur les résultats** : aucun. Il n'existe pas encore de résultat du moteur v3 ; les résultats de la v2.0 deviennent des faits mesurés historiques, cités avec leur source.
- **Ce que l'ADR ne règle pas** : l'origine de chaque bloc (fiches comparatives, jalon J1, décisions M-n à venir) ; le pas de temps (fiche « temps et comptabilité ») ; la loi de crédibilité, la règle de consommation, la forme du corridor de taux, le nombre de secteurs, l'agrégation des encours hypothécaires — toutes pistes « à instruire », listées dans `docs/feuille-de-route.md` § 5, aucune n'étant décidée.
- **Instabilités connues et hypothèses réfutées** de la première tentative : reprises dans la synthèse d'`archive/`, puis dans la spécification ; elles ne se réintroduisent pas sans fait nouveau (`docs/exigences.md` § 2.8).

Issues : #2, #3, #5.
