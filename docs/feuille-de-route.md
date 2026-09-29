# Feuille de route

Tenue par `architect`, après chaque série de PR fusionnées. Chaque mise à jour est datée et cite le SHA de `main` et de la branche de travail.

**Dernière mise à jour** : 29/09/2026 — `main` = `fdb3fd4`, `claude/fondations` = `fcb54a6`.

## 1. Branche de travail en cours

- **Branche** : `claude/fondations` — PR #7 (brouillon), partie de `main` `fdb3fd4`, tête `fcb54a6` au 29/09/2026 — jalon **J0 Fondations**.
- **Périmètre** (fermé, cinq issues) :
  - [x] #2 — Adapter le cadre du projet : `CLAUDE.md`, exigences, glossaire, fiches d'agents — agent : session principale — circuit : 4 — résultats : aucun — fait (`a5d873c`, `75e2cc6`, `377bda3`).
  - [ ] #3 — ADR de fondation (0001 à 0004) et feuille de route — agent : `architect` — circuit : 4 — résultats : aucun — en cours.
  - [x] #5 — Constituer `archive/` : sélection temporaire de pièces de la première tentative — agent : session principale — circuit : 4 (commit `archive:`) — résultats : aucun — fait (`fcb54a6`). Critères : contenu limité à M6 (source `.tex` v1.5, code v2.0 sans l'état D1, synthèse des faits mesurés G à K avec définitions et fenêtres, PDF des volumes 1 et 2 du cours), pièces versées intactes (M17) ; aucun nom de pays réel associé aux configurations (les mentions d'épisodes historiques et de bibliographie du source v1.5 et du cours sont admises, M17) ; aucune correspondance configurations ↔ pays réels, aucun lien vers un stockage privé, aucune archive compressée ; `archive/` jamais importée.
  - [ ] #6 — Conventions de la spécification v3, gabarit de fiche comparative et inventaire des blocs du socle — agents : `architect` (`docs/blocs/README.md`, ordre d'instruction, experts pilotes), `docwriter` (`CONVENTIONS.md`, squelette `.tex`, gabarit de fiche) — circuit : 4 — résultats : aucun. Critères : ADR 0004, points 1, 3 et 7 ; le squelette compile en XeLaTeX ; environ neuf blocs du socle inventoriés, chacun avec son expert pilote.
  - [ ] #4 — Squelette Python du moteur v3 et chaîne de vérification (tests, concordance, compilation LaTeX), réécriture du `README.md` — agents : `coder`, puis `audit` — circuit : 3 (workflow `circuit-technique`, une fois les batteries créées) — résultats : aucun. Critères : ADR 0002 (arborescence des couches), ADR 0003 (uv, `pyproject.toml`, `uv.lock`, CI), ADR 0004 (skill `compiler-doc`, hook LaTeX, concordance `--strict`) ; les trois batteries passent ; plus aucun « À ADAPTER » dans le dépôt.
- **Ordre conseillé** pour le reste : #3 → #6 → #4. Aucun commit ne change un résultat (le moteur v3 n'existe pas encore).
- **Ordre des commits** : sans objet pour cette branche.
- **Revue finale complète** (règle 10, avant la sortie du brouillon) : `audit` sur `git diff main...HEAD` (squelette, scripts, CI, hook) et `/code-review` ; `docwriter` si la spécification a été touchée au-delà du squelette ; `app-review` non déclenché (aucune interface). L'expert pilote n'est pas déclenché (aucune équation).
- **Critère de passage J0** : CI verte (tests, concordance, compilation) ; plus aucun « À ADAPTER » ; ADR 0001 à 0004 et cette feuille de route en place ; chaque issue #2 à #6 fermée par la fusion (un `Closes #N` par ligne dans la PR #7).

## 2. Branches suivantes

Les issues de ces branches ne sont pas encore créées : elles seront rédigées par `architect` et créées sur accord du mainteneur, au point d'étape qui suit la fusion de la PR #7. **Préalable à la première fiche (M18)** : le mainteneur valide le gabarit `docs/blocs/0000-gabarit.md` après la fusion de la PR #7 ; aucune fiche n'est instruite avant.

| Branche | Issues (à créer) | Motif du regroupement |
|---|---|---|
| J1 — fiche « temps et comptabilité » | Fiche comparative (pas de temps, calendrier, matrice des bilans et des flux, ordre des phases) → décision du mainteneur → section de la spécification | Elle conditionne le noyau (J2) et toutes les autres fiches ; elle est instruite seule et en premier. Expert pilote : `macro` (bouclage stock-flux), `monnaie` consulté. |
| J1 — fiches du secteur réel | Production et stocks ; travail et salaires ; prix ; ménages ; investissement et financement | Même expert pilote (`macro`), sections contiguës de la spécification ; l'inflation (prix, salaires) consulte `monnaie`. |
| J1 — fiches du secteur monétaire et de l'État | Banque commerciale ; banque centrale et anticipations ; État et dette | Expert pilote `monnaie` ; la dette publique consulte `macro`. |
| J2 — noyau | Comptes, ordonnanceur, état et sauvegarde, observation, tests d'invariants et mesure du coût du noyau (le budget de calcul est un critère de J3, M19) | Peut démarrer dès que la fiche « temps et comptabilité » est tranchée, en parallèle des autres fiches. |

## 3. Issues hors plan

Aucune au 29/09/2026 : les cinq issues ouvertes (#2 à #6) sont dans le périmètre de la branche de fondations.

## 4. Décisions du mainteneur

Toutes datées du 29/09/2026 et arrêtées par le mainteneur. M1 à M15 sont consignées dans l'ADR 0001 (§ Décision, point de même numéro) ; M16 dans l'ADR 0003 ; M17 précise M6 dans l'ADR 0001 ; M18 et M19 n'ont pas d'ADR (règles de procédure). Le numéro M-n est cité tel quel dans les fiches comparatives, la spécification (provenance des équations) et les issues.

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
| M18 | 29/09/2026 | Le gabarit de fiche comparative (`docs/blocs/0000-gabarit.md`, issue #6) est validé par le mainteneur après la fusion de la PR #7, avant la première fiche du jalon J1. | § 2 ci-dessus et § 6 ci-dessous (J1) |
| M19 | 29/09/2026 | Critères de passage des jalons J1 à J8 arrêtés (§ 6) ; le budget de calcul passe de J2 à J3, J2 ne mesurant que le coût du noyau. | § 6 ci-dessous |

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

| Jalon | Contenu | Critère de passage |
|---|---|---|
| **J0 Fondations** (#2 à #6, PR #7) | Cadre du projet, ADR 0001 à 0004, feuille de route, `archive/`, gabarits et conventions, squelette Python, CI | CI verte (tests, concordance, compilation XeLaTeX) ; plus aucun « À ADAPTER » ; PR #7 fusionnée par commit de fusion. |
| **J1 Spécification du socle** | Gabarit de fiche validé par le mainteneur (M18), puis fiche « temps et comptabilité », puis environ huit fiches (production et stocks ; travail et salaires ; prix ; ménages ; investissement et financement ; banque commerciale ; banque centrale et anticipations ; État et dette) → décisions M-n → spécification v3.0 « socle », sections marquées « proposées » jusqu'au code | Les neuf fiches tranchées, chacune avec sa décision M-n reportée ici ; chaque équation porte statut, provenance et M-n (contrôle par la concordance `--strict`) ; matrices des bilans et des flux écrites en tableaux, lignes et colonnes de somme nulle vérifiées par un script d'`outils/` ; état stationnaire calculé sous forme fermée par un script d'`outils/`, sans simulation, avec ses ratios publiés (K/Y, part salariale, taux réel, inflation, dette/PIB ; unité et dénominateur) ; revue de fond de `macro` et `monnaie`, avis de `jeu` sur les leviers prévus, validation du mainteneur. |
| **J2 Noyau** | Comptes, ordonnanceur, état et sauvegarde, observation ; tests d'invariants | Conservation exacte des identités comptables ; reprise de sauvegarde identique ; invariance d'unité ; coût du noyau seul mesuré et publié (le budget de calcul est un critère de J3, M19). Peut démarrer dès que la fiche « temps et comptabilité » est tranchée. |
| **J3 Économie fermée** | Blocs du socle, état stationnaire résolu, test zéro, premières références de non-régression | Critères d'O1 fixés **avant l'essai** et confirmés par le mainteneur (point de départ : critères du 16/09/2026, `docs/exigences.md` § 1.3) ; test zéro réussi sur les deux fenêtres pour plusieurs graines ; budget ≤ 1 ms par pays-semaine mesuré sur le socle complet, sur la plateforme de référence (M16) ; références régénérées après visa. |
| **J4 Simulateur utilisable** | Scénarios, leviers, rapports en ligne de commande, catalogue des effets des leviers | O2 : pour chaque levier, scénario apparié du signe attendu avec délai et distribution ; O5 : démonstration au mainteneur sur des scénarios de 5 à 10 ans ; avis de `jeu` ; revue d'`app-review`. |
| **J5 N pays** | Commerce, change, balance des paiements, régimes A à E, barrières entre pays | O4 : tests d'invariance sur les deux fenêtres (5 et 60 ans) — pays seul contre monde à un pays, unité monétaire (×100), permutation des pays, reprise de sauvegarde — à 1e-12 relatif à l'échelle du bilan, aucun solde de bilan calculé comme résidu ; balance des paiements bouclée exactement à chaque pas (somme mondiale des soldes courants et financiers nulle) ; chaque régime A à E expose ses leviers et eux seuls (un test par régime) ; budget ≤ 1 ms par pays-semaine avec au moins quatre pays. |
| **J6 Actifs et crises** | Blocs actifs et crises financières ; grille des dix configurations en tests | O3 : pour chaque type de crise retenu, précondition, contrefactuel, signal précurseur, intervention, reprise sans effacement gratuit ; **`archive/` supprimée au plus tard à la fin de J6** (M6). |
| **J7 Web, puis jeu** | Serveur, client web, tours mensuels, plusieurs joueurs, IA des pays non joueurs, conditions de fin | Mêmes résultats, bit à bit, en ligne de commande et par le web à graine et décisions égales (test) ; aucun calcul économique hors du moteur, vérifié par `app-review` ; O5 : partie complète menée par le mainteneur, au moins deux joueurs et une IA, jusqu'à une condition de fin ; reprise d'une partie sauvegardée identique ; revue de jouabilité de `jeu` avant la démonstration. |
| **J8 Cours** | Dérivations des volumes 1 et 2 corrigées et alignées sur la spécification v3 ; table de correspondance générée par script | Chaque chiffre du cours produit par un test ou un script, jamais recopié (les corrigés faux relevés le 29/09/2026 corrigés) ; chaque équation porte son statut *dérivée / approchée / choix de conception* et renvoie à son label de la spécification ; table de correspondance cours ↔ spécification générée par script et contrôlée en CI ; relecture de fond de `macro` et `monnaie`. |
