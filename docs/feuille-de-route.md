# Feuille de route

Tenue par `architect`, après chaque série de PR fusionnées. Chaque mise à jour est datée et cite le SHA de `main` et de la branche de travail.

**Dernière mise à jour** : 30/09/2026 — `main` = `facf97f` (commit de fusion de la PR #7) ; aucune branche de travail ouverte, la suivante est `claude/j1-temps-comptabilite` (§ 1), à créer une fois ses issues approuvées.

## 1. Branche de travail en cours

- **Branche** : `claude/j1-temps-comptabilite` — PR à ouvrir en brouillon dès la création de la branche, à partir de `main` `facf97f` — jalon **J1 Spécification du socle**, première branche : **fiche « temps et comptabilité » seule** (M21).
- **Objet** : éprouver le gabarit de fiche comparative sur sa première fiche (M20), instruire la fiche « temps et comptabilité » jusqu'à la décision du mainteneur, puis écrire la section « Cadre : temps, entités, comptabilité » de la spécification (proposée : aucun code avant J2) et le script qui vérifie les matrices des bilans et des flux (critère de passage de J1, M19).
- **Périmètre** (fermé, cinq issues ; issues créées le 30/09/2026 sur accord du mainteneur) :
  - [ ] #15 — Fiche « temps et comptabilité » : question posée et critères d'évaluation, écrits avant l'instruction — agent : `macro` (expert pilote), `monnaie` et `jeu` consultés sur les critères de leur domaine ; commit `docs:` par la session principale — circuit : 1 (première étape) — résultats : aucun — **point de décision** : le mainteneur valide les critères en commentaire de l'issue avant l'instruction.
  - [ ] #16 — Fiche « temps et comptabilité » : instruction des options et avis (`macro`, `monnaie`, `jeu`) — agents : `macro` (§ 3 à 5), `monnaie` (§ 6), `jeu` (§ 7) ; commit `docs:` par la session principale — circuit : 1 — résultats : aucun — statut de la fiche à l'issue : « avis rendus ».
  - [ ] #17 — Décision du mainteneur sur la fiche « temps et comptabilité » (M22) et validation du gabarit à l'usage (M20) — agents : mainteneur (décision), `architect` (consignation : § 4 ci-dessous, `docs/blocs/README.md`, `CONTEXT.md`, ADR 0005), session principale (§ 8 de la fiche dans les mots du mainteneur, retouches du gabarit), `docwriter` (`CONVENTIONS.md` § 6, en fin de branche) — circuit : 1 — résultats : aucun — **point de décision** : M22 et retouches du gabarit.
  - [ ] #18 — Spécification : section « Cadre : temps, entités, comptabilité » (proposée) issue de M22 — agent : `docwriter` ; validation de fond par `macro`, `monnaie` sur les bilans de la banque et de la banque centrale — circuit : 1 (fin) — résultats : aucun — PDF recompilé dans le même commit, concordance `--strict` verte.
  - [ ] #19 — Script de vérification des matrices des bilans et des flux (sommes nulles), lu depuis la spécification — agents : `coder`, puis `audit` (workflow `circuit-technique`) — circuit : 3 — résultats : aucun (le moteur v3 n'exécute encore rien).
- **Ordre** : 1 → validation des critères → 2 → décision M22 → 3 → 4 → 5 (la convention d'écriture des tableaux est fixée dans l'issue 5 avant la rédaction de l'issue 4, pour que le script lise ce que `docwriter` écrit ; le script ne s'exécute sur la spécification qu'une fois l'issue 4 commitée).
- **Ordre des commits** : sans objet (aucun résultat ne change).
- **Revue finale complète** (règle 10, avant la sortie du brouillon) : `audit` sur `git diff main...HEAD` (script et tests) et `/code-review` ; `docwriter` a déjà fait son passage unique (issue 4) ; `macro` valide le diff de la spécification et la fiche ; `app-review` non déclenché (aucune interface).
- **Ce que cette branche ne fait pas** : aucune autre fiche (M21) ; aucun code du noyau (J2) ; aucune issue d'outillage (#8 à #14, branche technique à part, § 2).

## 2. Branches suivantes

| Ordre | Branche | Issues | Motif du regroupement |
|---|---|---|---|
| 2 | Technique — outillage de J0 (workflow `circuit-technique`) | #8, #12 et, si un premier cas s'est présenté, #10 (même script `outils/concordance_spec_moteur.py`) ; #9 et #13 (mêmes tests `tests/invariants/test_archive_*.py`) ; #11 et #14 sont des décisions du mainteneur, réglées hors branche ou dans celle-ci sur son instruction | Décision M21 : une branche technique entre deux branches de fiches ; quatre ou cinq issues, un seul domaine de commit (`code:`, `tests:`), résultats strictement identiques. |
| 3 | J1 — fiches du secteur réel | Production et stocks ; travail et salaires ; prix ; ménages ; investissement et financement | Même expert pilote (`macro`), sections contiguës de la spécification ; l'inflation (prix, salaires) consulte `monnaie`. À découper en deux branches si cinq fiches dépassent le périmètre de trois à cinq issues (chaque fiche vaut au moins deux issues : instruction, décision et section). |
| 4 | J1 — fiches du secteur monétaire et de l'État | Banque commerciale ; banque centrale et anticipations ; État et dette | Expert pilote `monnaie` (7, 8) et `macro` (9) ; la dette publique consulte les deux. |
| 5 | J2 — noyau | Comptes, ordonnanceur, état et sauvegarde, observation, tests d'invariants et mesure du coût du noyau (le budget de calcul est un critère de J3, M19) | Peut démarrer dès que M22 est prise, en parallèle des branches 3 et 4 si le mainteneur l'autorise (une seule branche de travail à la fois : à intercaler). |

Les issues de ces branches ne sont pas encore créées : `architect` les rédige au point d'étape qui précède chaque branche, et le mainteneur les approuve.

## 3. Issues hors plan

Au 30/09/2026, sept issues ouvertes, toutes d'outillage, aucune dans le périmètre de la branche J1 n°1 (M21) :

| Issue | Objet | Module touché | Groupe proposé | Remarque |
|---|---|---|---|---|
| #8 | Concordance : faux négatifs sur `\iffalse` et verbatim cité en commentaire | `outils/concordance_spec_moteur.py` | branche technique | `bug` ; à traiter avant que la spécification ne porte des `\if…` d'`etoolbox`. |
| #12 | Concordance, règle 3 : label sur ligne non numérotée ou en excès | `outils/concordance_spec_moteur.py`, `CONVENTIONS.md` § 9 | branche technique | Devient utile dès la première équation numérotée (J2). |
| #10 | Concordance : registre d'exemptions | `outils/concordance_spec_moteur.py` | branche technique, seulement si un premier cas existe | Aucun cas au 30/09/2026. |
| #9 | Invariant archive : chemin construit dans une variable | `tests/invariants/test_archive_non_importee.py` | branche technique | Utile dès qu'un script d'`outils/` lit `archive/` pour une fiche. |
| #13 | Test d'archive : ignorer `__pycache__` | `tests/invariants/test_archive_intacte.py` | branche technique | Gêne toute exécution du prototype v2.0 pour remesurer un fait : à traiter en premier dans la branche technique. |
| #11 | Dependabot : suivre ou non `uv.lock` | `.github/dependabot.yml` | décision du mainteneur | Libellé proposé : `ready-for-human`. |
| #14 | Ruleset de `main` : concorder le JSON et le ruleset appliqué | `.github/ruleset-main.json` ou interface web | décision du mainteneur | Libellé proposé : `ready-for-human`. |

## 4. Décisions du mainteneur

M1 à M19 sont datées du 29/09/2026, M20 et M21 du 30/09/2026, toutes arrêtées par le mainteneur. M1 à M15 sont consignées dans l'ADR 0001 (§ Décision, point de même numéro) ; M16 dans l'ADR 0003 ; M17 précise M6 dans l'ADR 0001 ; M18 à M21 n'ont pas d'ADR (règles de procédure). La forme canonique du numéro est `Mn` (`M16`), citée telle quelle dans les fiches comparatives, la spécification (provenance des équations, `CONVENTIONS.md` § 2.3) et les issues ; « M-n » désigne une décision quelconque dans la prose. Trois décisions de mise en œuvre sont consignées par annotation d'ADR sans numéro (elles ne changent aucune décision numérotée) : garder `outils/compiler_specification.sh` (29/09/2026, ADR 0004, pt 4) ; déclarer le hook `preparer_latex.sh` en `SessionStart` (29/09/2026, ADR 0004, pt 5) ; règle 4 de la concordance, une décision par mention, le pluriel « décisions M3 et M16 » et la forme groupée « (M3, M16) » restant refusés (30/09/2026, ADR 0004, pt 6, et `CONVENTIONS.md` § 9).

| N° | Date | Décision | Où elle est consignée |
|---|---|---|---|
| M1 | 29/09/2026 | Nouveau moteur modulaire « v3 », écrit bloc par bloc ; v1.5 et v2.0 servent d'archives de référence. Rouvre la décision du 19/09/2026 « pas de reconstruction du prototype v2.0 » (motifs dans l'ADR 0001). | ADR 0001, pt 1 ; `CLAUDE.md`, « Contexte » |
| M2 | 29/09/2026 | Le mainteneur tranche lui-même, bloc par bloc, l'origine de chaque approche (v1.5, v2.0 ou nouvelle), sur fiche comparative. | ADR 0001, pt 2 ; ADR 0004, pt 7 ; `docs/exigences.md` § 2.3 |
| M3 | 29/09/2026 | Des approches autres que celles de la v1.7 et de la v2.0 sont bienvenues, appuyées sur des références vérifiées. | ADR 0001, pt 3 |
| M4 | 29/09/2026 | Simulateur d'abord ; jeu tour par tour mensuel à terme. | ADR 0001, pt 4 ; `docs/exigences.md` § 1.1 |
| M5 | 29/09/2026 | Interface cible : navigateur web, moteur Python côté serveur ; ligne de commande d'abord. | ADR 0001, pt 5 ; `docs/exigences.md` § 5 |
| M6 | 29/09/2026 | Dossier `archive/` dans le dépôt, strict nécessaire, voué à être supprimé (au plus tard fin J6) ; contenu et exclusions fixés. | ADR 0001, pt 6 ; `CONTEXT.md`, « Archive » |
| M7 | 29/09/2026 | Premier jalon économique : économie fermée, un pays (le socle). | ADR 0001, pt 7 |
| M8 | 29/09/2026 | Spécification en LaTeX (XeLaTeX), forme de la v1.5, chaîne documentaire reprise d'`outil_usp`. | ADR 0001, pt 8 ; ADR 0004 |
| M9 | 29/09/2026 | Trois experts de fond : `macro`, `monnaie`, `jeu`. | ADR 0001, pt 9 ; `CLAUDE.md`, « Sous-agents » |
| M10 | 29/09/2026 | On se passe de la v1.7 : ni prototype ni document. | ADR 0001, pt 10 ; `docs/exigences.md` § 2.2 |
| M11 | 29/09/2026 | Claude seul sur le dépôt, sans autre flux d'assistants. | ADR 0001, pt 11 |
| M12 | 29/09/2026 | Les six objectifs du 17/09/2026, reformulés « simulateur d'abord », fondent `docs/exigences.md`. | ADR 0001, pt 12 ; `docs/exigences.md` § 1.3 |
| M13 | 29/09/2026 | Budget de calcul : au plus 1 ms par pays-semaine. | ADR 0001, pt 13 ; ADR 0002, inv. 11 ; `CLAUDE.md`, « Architecture » |
| M14 | 29/09/2026 | Code en français, identifiants ASCII ; commentaires et docstrings en français avec accents ; symboles courts admis quand la spécification les nomme. | ADR 0001, pt 14 ; `docs/exigences.md` § 4.2 |
| M15 | 29/09/2026 | Cours magistral reporté au jalon J8. | ADR 0001, pt 15 ; `docs/exigences.md` § 3.6 |
| M16 | 29/09/2026 | Plateforme de référence des résultats : la CI Linux de GitHub Actions (`ubuntu-latest`), Python 3.12 géré par uv, versions verrouillées dans `uv.lock`. | ADR 0003, pt 4 ; `CLAUDE.md`, « Changements de résultats » |
| M17 | 29/09/2026 | Les pièces d'`archive/` sont versées intactes. Le source v1.5 et le cours citent des pays réels comme épisodes historiques et en bibliographie seulement, jamais dans la grille des dix configurations ; la règle est « aucun nom de pays réel associé aux configurations » ; le critère de l'issue #5 (« aucune occurrence ») est corrigé en ce sens. | ADR 0001, pt 6 ; `docs/exigences.md` § 2.9 |
| M18 | 29/09/2026 | Le gabarit de fiche comparative (`docs/blocs/0000-gabarit.md`, issue #6) est validé par le mainteneur après la fusion de la PR #7, avant la première fiche du jalon J1. Précisée par M20. | § 2 ci-dessus et § 6 ci-dessous (J1) |
| M19 | 29/09/2026 | Critères de passage des jalons J1 à J8 arrêtés (§ 6) ; le budget de calcul passe de J2 à J3, J2 ne mesurant que le coût du noyau. | § 6 ci-dessous |
| M20 | 30/09/2026 | Précise M18 : le gabarit de fiche comparative est validé **à l'usage**, éprouvé sur la première fiche (« temps et comptabilité ») puis validé par le mainteneur avec ses retouches, à la décision de cette fiche. Aucune validation préalable n'est requise pour l'ouvrir. | § 1 ci-dessus (issues 1 et 3 de la branche) ; ADR 0004, pt 7 (annotation) ; `docs/blocs/README.md` |
| M21 | 30/09/2026 | Organisation du jalon J1 : la première branche de travail porte la **fiche « temps et comptabilité » seule** (gabarit éprouvé, fiche instruite jusqu'à la décision, puis sa section de spécification) ; les issues d'outillage #8 à #14 font l'objet d'une **branche technique à part**, plus tard, intercalée entre deux branches de fiches (workflow `circuit-technique`). | § 1, § 2 et § 3 ci-dessus |

Le même jour (30/09/2026), le mainteneur a validé sans numéro : l'inventaire `docs/blocs/README.md` (`macro` pilote de « temps et comptabilité » et de « État et dette », module `finances_publiques.py`) ; le maintien des sections `sec:objet`, `sec:ecartees` et `sec:chantiers` du squelette `.tex` telles que remplies au jalon J0 ; `docs/specification/CONVENTIONS.md` tenu par `docwriter`, qui tient déjà `docs/specification/` (et non par `architect`, comme l'indiquait l'en-tête du fichier) ; libellé `ready-for-human` sur #11 et #14.

## 5. Pistes à instruire dans les fiches comparatives (aucune n'est décidée)

Ouvertes par M2 et M3 ; chacune sera présentée dans la fiche du bloc concerné, avec ses références vérifiées, l'avis de l'expert pilote et de `jeu`, puis tranchée par le mainteneur (M-n à venir).

| Piste | Fiche | Motif de l'instruction |
|---|---|---|
| Pas de temps mensuel unique | temps et comptabilité | Quatre fois moins de pas ; supprime l'incohérence calendaire de la v1.5 (4 pas par mois, 52 par an, glissement sur 12 mois) ; le moteur v2.0 prend 13 dates de décision par an. À peser contre la granularité hebdomadaire des marchés. |
| Consommation par règle stock-flux à cible de richesse (forme fermée) plutôt qu'une optimisation à chaque pas | ménages | État stationnaire calculable ; compatible avec l'invariant 11 de l'ADR 0002. |
| Corridor de taux explicite (facilités permanentes) | banque centrale et anticipations | Réserves et refinancement deviennent des flux décidés, pas des soldes résiduels (défaut d'invariance de la v2.0, ADR 0001 § 6). |
| Loi de crédibilité revue ; alternative : apprentissage à gain constant | banque centrale et anticipations | Piège de la loi v2.0 (ADR 0001 § 2). |
| Prix au coût normal majoré | prix | Forme fermée, lisible pour le joueur ; à confronter au terme de demande R3, acquis mesuré de la première tentative. |
| Deux secteurs pour le socle (consommation, équipement) avant les quatre de la v1.5 et de la v2.0 | production et stocks | Budget de complexité (`docs/exigences.md` § 2.7). |
| Encours hypothécaires agrégés par strate plutôt que cohortes individuelles | actifs et crises (J6) | 70 % du temps de la v2.0 dans 23 403 cohortes (mesuré le 29/09/2026). |

## 6. Jalons

Critères de passage arrêtés par le mainteneur le 29/09/2026 (M19).

| Jalon | Contenu | Critère de passage | État |
|---|---|---|---|
| **J0 Fondations** (#2 à #6, PR #7) | Cadre du projet, ADR 0001 à 0004, feuille de route, `archive/`, gabarits et conventions, squelette Python, CI | CI verte (tests, concordance, compilation XeLaTeX) ; plus aucun « À ADAPTER » ; PR #7 fusionnée par commit de fusion. | **Passé le 30/09/2026** : PR #7 fusionnée à 05:29 UTC (commit de fusion `facf97f`), issues #2 à #6 fermées, ruleset « Protection main » appliqué par le mainteneur via l'interface web (écart avec `.github/ruleset-main.json` suivi par #14). |
| **J1 Spécification du socle** | Gabarit de fiche éprouvé sur la première fiche et validé à l'usage (M20), fiche « temps et comptabilité », puis environ huit fiches (production et stocks ; travail et salaires ; prix ; ménages ; investissement et financement ; banque commerciale ; banque centrale et anticipations ; État et dette) → décisions M-n → spécification v3.0 « socle », sections marquées « proposées » jusqu'au code | Les neuf fiches tranchées, chacune avec sa décision M-n reportée ici ; chaque équation porte statut, provenance et M-n (contrôle par la concordance `--strict`) ; matrices des bilans et des flux écrites en tableaux, lignes et colonnes de somme nulle vérifiées par un script d'`outils/` ; état stationnaire calculé sous forme fermée par un script d'`outils/`, sans simulation, avec ses ratios publiés (K/Y, part salariale, taux réel, inflation, dette/PIB ; unité et dénominateur) ; revue de fond de `macro` et `monnaie`, avis de `jeu` sur les leviers prévus, validation du mainteneur. | **En cours** depuis le 30/09/2026 : branche J1 n°1 (§ 1). |
| **J2 Noyau** | Comptes, ordonnanceur, état et sauvegarde, observation ; tests d'invariants | Conservation exacte des identités comptables ; reprise de sauvegarde identique ; invariance d'unité ; coût du noyau seul mesuré et publié (le budget de calcul est un critère de J3, M19). Peut démarrer dès que la fiche « temps et comptabilité » est tranchée. | À venir |
| **J3 Économie fermée** | Blocs du socle, état stationnaire résolu, test zéro, premières références de non-régression | Critères d'O1 fixés **avant l'essai** et confirmés par le mainteneur (point de départ : critères du 16/09/2026, `docs/exigences.md` § 1.3) ; test zéro réussi sur les deux fenêtres pour plusieurs graines ; budget ≤ 1 ms par pays-semaine mesuré sur le socle complet, sur la plateforme de référence (M16) ; références régénérées après visa. | À venir |
| **J4 Simulateur utilisable** | Scénarios, leviers, rapports en ligne de commande, catalogue des effets des leviers | O2 : pour chaque levier, scénario apparié du signe attendu avec délai et distribution ; O5 : démonstration au mainteneur sur des scénarios de 5 à 10 ans ; avis de `jeu` ; revue d'`app-review`. | À venir |
| **J5 N pays** | Commerce, change, balance des paiements, régimes A à E, barrières entre pays | O4 : tests d'invariance sur les deux fenêtres (5 et 60 ans) — pays seul contre monde à un pays, unité monétaire (×100), permutation des pays, reprise de sauvegarde — à 1e-12 relatif à l'échelle du bilan, aucun solde de bilan calculé comme résidu ; balance des paiements bouclée exactement à chaque pas (somme mondiale des soldes courants et financiers nulle) ; chaque régime A à E expose ses leviers et eux seuls (un test par régime) ; budget ≤ 1 ms par pays-semaine avec au moins quatre pays. | À venir |
| **J6 Actifs et crises** | Blocs actifs et crises financières ; grille des dix configurations en tests | O3 : pour chaque type de crise retenu, précondition, contrefactuel, signal précurseur, intervention, reprise sans effacement gratuit ; **`archive/` supprimée au plus tard à la fin de J6** (M6). | À venir |
| **J7 Web, puis jeu** | Serveur, client web, tours mensuels, plusieurs joueurs, IA des pays non joueurs, conditions de fin | Mêmes résultats, bit à bit, en ligne de commande et par le web à graine et décisions égales (test) ; aucun calcul économique hors du moteur, vérifié par `app-review` ; O5 : partie complète menée par le mainteneur, au moins deux joueurs et une IA, jusqu'à une condition de fin ; reprise d'une partie sauvegardée identique ; revue de jouabilité de `jeu` avant la démonstration. | À venir |
| **J8 Cours** | Dérivations des volumes 1 et 2 corrigées et alignées sur la spécification v3 ; table de correspondance générée par script | Chaque chiffre du cours produit par un test ou un script, jamais recopié (les corrigés faux relevés le 29/09/2026 corrigés) ; chaque équation porte son statut *dérivée / approchée / choix de conception* et renvoie à son label de la spécification ; table de correspondance cours ↔ spécification générée par script et contrôlée en CI ; relecture de fond de `macro` et `monnaie`. | À venir |

## 7. Branches fusionnées

| Branche | PR | Jalon | Fusion | Issues et commits |
|---|---|---|---|---|
| `claude/fondations` | #7 | J0 | 30/09/2026, commit de fusion `facf97f` | #2 (`a5d873c`, `75e2cc6`, `377bda3`) ; #3 (`19839bb`, `85bda79`) ; #5 (`fcb54a6`, `84e6ad9`) ; #6 (`85573bc`) ; #4 (`6090310`, `8ba19ff`, `d8eeb17`, `8c8a633`, `da76229`, `bd0cd44`, `eda7278`, `4651b5f`, `878fc6f`, `75c9e72`). Revue finale complète faite avant la sortie du brouillon ; aucun résultat changé (le moteur v3 n'exécute rien). Issues nées de la revue : #8 à #13 (audit, `docwriter`, session principale) ; #14 après la fusion (ruleset). |
