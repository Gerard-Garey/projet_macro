---
bloc: Travail et salaires
module: src/nations/blocs/travail.py
expert pilote: macro
experts consultés: monnaie (indexation des salaires sur les anticipations : frontière inflation) ; jeu
statut: avis rendus (03/10/2026)
décision: —
issue: #39
---

# Fiche comparative — Travail et salaires

> Fiche ouverte à partir du gabarit `0000-gabarit.md` (validé à l'usage, M20), sur le modèle de forme de la fiche 2 « production et stocks » (M24). Jalon 1 de l'issue #39 : § 1 et § 2 seuls ; les rubriques suivantes portent « non instruit » jusqu'au jalon 2. Décidée avec la fiche 4 « prix » (décision du mainteneur du 03/10/2026 : décisions par paires).

Une fiche comparative instruit **l'origine de l'approche** d'un bloc (`docs/exigences.md` § 2.3) : la spécification v1.5, le moteur v2.0, ou une approche nouvelle. Elle est **instruite par l'expert pilote**, commentée par `jeu` et par l'expert consulté que désigne `README.md`, et **décidée par le mainteneur** (décision M-n, reportée dans `docs/feuille-de-route.md`). Aucune approche n'entre dans le moteur ni dans la spécification sans cette décision. Les agents n'écrivent pas la fiche dans le dépôt : elle figure dans leur compte rendu et la session principale la commite. Un **bloc-cadre** (temps et comptabilité) n'est pas un module de `blocs/` : sa fiche instruit ce que le cadre **définit** (conventions, matrices, règles), non des flux proposés ; les adaptations que cela impose sont signalées rubrique par rubrique.

Règles de rigueur (`CLAUDE.md`, « Rigueur ») : un chiffre se remesure ou cite sa source ; une équation de la v1.5 n'a jamais été garantie exécutée ; un comportement de la v2.0 ne vaut que sous son profil (état D1, **non versé** : aucun fait ne peut y être remesuré) et avec ses défauts connus ; chaque fait de la première tentative porte son **statut** S+O, O, R, L, V ou V+O (`CONTEXT.md`, « Statut d'un fait » ; un fait V sur le prototype v2.0 reste un fait de la première tentative, non un résultat v3) ; chaque référence est une publication retrouvée. Citer `archive/v1.5/…` avec numéro d'équation et section, ou avec le **numéro de ligne du `.tex`** quand section ou équation ne sont pas identifiables sans compiler ; `archive/v2.0/…` avec fichier et ligne. **Principe de simplicité** (adopté par le mainteneur le 30/09/2026, fiche « temps et comptabilité » § 2 ; `CONTEXT.md`) : à exigences comptables égales, l'option la plus simple pour le joueur et pour le moteur est préférée ; toute complexité se justifie par une identité qu'elle rend vérifiable ou par un mécanisme perçu à l'échelle d'une partie ; une simplification ne supprime ni une contrepartie comptable visible d'un levier ni une grandeur restituée au tour ; les identités, les tolérances relatives, le déterminisme, les invariants de l'ADR 0002 et la concordance ne se simplifient pas.

## 1. Question posée

*Rédigé par `macro` (expert pilote), 03/10/2026, sur la spécification à l'état `bf3829e` (branche `claude/j1-economie-reelle`, PR #43).*

Le bloc porte le marché du travail du socle : emploi effectif, contrainte d'offre de travail, ajustement éventuel de l'emploi, salaire nominal et masse salariale versée (ligne 5 de `tab:matrice-flux`). Il définit le coût du travail que lit le bloc prix, puisque le coût unitaire UC = W/pr est écrit par le bloc 2 sur le salaire W du bloc 3 (fiche 2 § 3.N-4). Il débloque les fiches 4 et 5 (`docs/blocs/README.md` § 3, rang 3). Sous M22, un pas est un tour (n_a = 12, n_m = 1) : toute fenêtre exprimée en pas l'est aussi en tours. La fiche est décidée **avec la fiche 4** (M25 et M26, décision du mainteneur du 03/10/2026 : décisions par paires). Elle ne lui est donc pas antérieure pour ce qui touche au processus d'inflation.

### 1.1 Contrats hérités

| Contrat | Source | Ce qu'il impose à la fiche 3 | Ce qui le rouvrirait |
|---|---|---|---|
| Calendrier et conversions | M22 ; ADR 0005 | Pas mensuel, n_a = 12, un pas = un tour. Conversion **linéaire unique** des taux, flux et vitesses, avec la condition λ ≤ n_a. Salaires révisés en phase 1, qui est une date de décision à tout pas. Ligne 5 exécutée en phase 4. Neuf phases triangulaires, aucune résolution simultanée | Décision M-m citant M22 |
| Ordre interne de la phase 4 | M24 (b) ; ADR 0007 | « **Travail, puis production** ». Le bloc 3 écrit l'emploi effectif N_{j,t} en phase 4 **avant** le bloc 2, à partir de la demande de travail N* = y*/pr écrite en phase 2 par le bloc 2. Il exécute la ligne 5 sur cet emploi. Il ne lit en phase 4 aucune variable écrite après lui, en particulier ni y_t ni la capacité. Une telle lecture serait une résolution simultanée, à écarter (ADR 0007, « Conditions de réouverture ») | Décision M-m citant M24 et M22 |
| Frontière des blocs 2 et 3 (Q4) | M24, Q4 (fiche 2 § 8) | Plan et production au bloc 2 ; emploi et salaires au bloc 3. La fiche **confirme** que l'ajustement de l'emploi relève du bloc 3, ou propose une révision par une décision citant M24 | Décision citant M24 |
| Demande de travail et technique | M24 ; `sec:production` (l. 592, 617) | N* = y*/pr est défini par le bloc 2. La technique est de Leontief en travail, y = min{y*, pr·N}. Il n'y a pas de produit marginal : le partage de la valeur ajoutée n'est pas ancré par la technique (l. 592). Une option dont la demande de travail diffère de N*, par exemple fondée sur le produit marginal (v1.5 `eq:labour`, l. 532 ; v2.0 `model.py` l. 653), réviserait M24 | Décision citant M24 |
| Valorisation des stocks | M24 (a) | Les entrées en stock sont valorisées à UC = W/pr, non à WB/y. Une masse salariale supérieure à UC·y ne se stocke pas | Décision citant M24 |
| Croissance | M24 (f) ; `sec:production` l. 616 | g = n_a[(1 + g_pr/n_a)(1 + g_N/n_a) − 1]. g_N, croissance annuelle de la population active, relève des « blocs travail et ménages » (`tab:symboles`). Son propriétaire est à déclarer | Décision citant M24 si la forme de g change |
| Borne d'offre de travail | #38 (avant le jalon 2) ; `sec:production` l. 592 et 753 | Emploi au plus égal à la population active : borne du bloc travail, **inactive à l'état stationnaire**. Sa déclaration suit la lecture (i) ou (ii) retenue pour #38 | Décision du mainteneur sur #38 |
| Boucle production – stocks – emploi | M24, conditions de `jeu` (fiche 2 § 9.5, condition 5) | Si l'emploi s'ajuste avec retard, `macro` mesure la boucle combinée : elle doit être amortie, avoir une période de 3 à 8 ans, et la demi-vie de l'emploi doit être traduite en λ_N | Décision du mainteneur |
| Anticipations | `docs/blocs/README.md` § 3 ; § 2 (frontière inflation) | La fiche déclare la variable d'anticipation qu'elle consomme. Sa loi de formation relève de la fiche 8 | — |
| Statut des faits | Décision P1 du 03/10/2026 ; `CONTEXT.md` | Statuts S+O, O, R, L, V ou V+O. Un fait V mesuré sur le prototype v2.0 reste un fait de la première tentative. L'état D1 n'est pas versé | — |

### 1.2 Ce que le bloc doit produire

Les symboles **ne sont pas fixés** : ils le seront à l'instruction, sous le critère 14. u est pris (retard dans le registre) et L aussi (crédits) : ni le taux de chômage ni la population active ne peuvent s'écrire ainsi.

| Grandeur | Définition | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| Salaire nominal W_t | Salaire par personne employée, fixé en phase 1 | u.m. par personne et par pas | — | le pas, phase 1 ; restitution : le tour, et le glissement sur 12 tours |
| Emploi effectif N_{j,t} | Personnes employées dans le pas | personnes | — | le pas, phase 4, avant le bloc 2 |
| Masse salariale WB_t | W_t·N_t, ligne 5 (ménages +, entreprises « courant » −) | u.m. par pas | — | le pas, phase 4 |
| Masse salariale excédentaire | WB − UC·y = W·(N − y/pr), positive en cas de rétention ; charge du pas, non stockée | u.m. par pas ; fraction | WB du pas | le pas ; restitution : le tour |
| Population active | Personnes disponibles pour l'emploi ; propriétaire à déclarer (bloc 3 ou 5) | personnes | — | ouverture du pas ; croissance g_N par an |
| Taux de chômage | (population active − N) / population active | fraction | population active du pas | le pas ; restitution : le tour, et la moyenne sur 12 tours |
| Productivité apparente rapportée à sa tendance | (y/N)/pr ; au plus 1 sous la technique de M24 ; vaut 1 sans rétention | fraction | pr du pas | le tour ; 12 tours |
| Salaire réel rapporté à la productivité | W/(p·pr), soit la part salariale sous J = 1 sans intrants | fraction | p·pr du pas | le pas ; restitution sur 12 tours, somme des WB sur somme de la valeur ajoutée en u.m. |
| Variables d'état du bloc (si l'option en a) | Par exemple emploi d'ouverture, salaire cible, chômage de référence | unité propre | — | ouverture du pas |

### 1.3 Ce qu'il lit

- **Ouverture** :
  - ses variables d'état ;
  - la population active ;
  - le taux de chômage du pas précédent : la phase 1 ne lit que l'ouverture et le registre ;
  - le registre des prix (`sec:cadre-calendrier`).
- **Phase 1** : la variable d'anticipation d'inflation, à l'ouverture ou après le bloc 8 dans la phase 1. La phase 1 est une phase à ordre « fixé par leurs fiches » (l. 487). Dans `tab:phases`, « travail » et « banque centrale » y sont séparés par une virgule : un ordre « banque centrale, puis travail » est à déclarer par les fiches 3 et 8, sans décision citant M22.
- **Phase 2** : la demande de travail N*_{j,t} (bloc 2).
- **Leviers du joueur** :
  - aucun levier propre au socle sans décision ;
  - transitent par le bloc la dépense publique, les impôts et le taux (par la demande) ;
  - un levier institutionnel éventuel (salaire minimum, comme W^min de la v1.5 l. 621 ; indexation légale) est une question du § 1.5.
- **Décisions qui le contraignent** :
  - M7 (économie fermée : pas de migration) ;
  - M13 (budget) ;
  - M22 ;
  - M24 et l'ADR 0007 ;
  - décision du 02/10/2026 sur #23 (indices c, j, k).

### 1.4 Frontières

- **Production et stocks (fiche 2, décidée)** : N* reçu, N rendu. La production visée non réalisée (N < N*) et la productivité apparente (N > N*) sont les deux faces visibles de l'écart. Critères 2, 5 (c), 8 et 11.
- **Prix (fiche 4, décidée avec la fiche 3)** :
  - UC = W/pr est lu par le bloc prix en phase 5 ;
  - la part salariale stationnaire résulte conjointement de la règle de salaire et de la marge ;
  - la boucle salaires – prix se mesure sur les deux règles.
  
  Critères 3 (d) et 5 (d).
- **Banque centrale et anticipations (fiche 8, `monnaie`)** : **frontière inflation**. Chez `macro` : la formation du salaire, l'indexation et sa forme. Chez `monnaie` : l'anticipation et la crédibilité. Le bloc 8 lit en outre le taux de chômage à l'ouverture pour une règle de taux qui aurait un terme d'activité. Critère 9 et avis de `monnaie` (§ 6).
- **Ménages (fiche 5)** : la ligne 5 est un revenu des ménages. Le propriétaire de la population active et de g_N reste à fixer (§ 1.5, Q2).
- **État et dette (fiche 9)** :
  - allocations de chômage éventuelles, en ligne 6 ;
  - cotisations sociales et impôt sur les salaires, en ligne 7 (la v1.5 a un τ_S, l. 536) ;
  - emploi public **absent du socle** : la ligne 2 est un achat de biens aux entreprises.
  
  Le bloc 3 ne propose aucune de ces lignes.
- **Investissement (fiche 6)** : la masse salariale excédentaire réduit les profits non distribués (sous-colonne « courant », Q2 de la fiche 2 ; #36).
- **`jeu`** : critères 5 (c), 10 et 11 ; avis au § 7.

### 1.5 Ce que la fiche ne tranche pas, et questions ouvertes

**Hors du périmètre** :
- la loi de formation des anticipations et la crédibilité (fiche 8) ;
- les allocations, cotisations et impôts sur les salaires (fiche 9) ;
- l'hétérogénéité des travailleurs et les salaires sectoriels (J ≥ 2, hors socle) ;
- la migration et l'économie duale (v1.5 l. 852 : J5 et au-delà) ;
- les heures de travail : N est en personnes (`tab:symboles`) ;
- les valeurs numériques de l'état stationnaire et la calibration (J3) : la fiche vérifie qu'une forme fermée existe ;
- les bandes du test zéro : proposées ici, confirmées avec O1 avant l'essai (M19).

**Questions ouvertes à instruire** :
- **Q1 — Q4 de la fiche 2** : la fiche confirme que l'ajustement de l'emploi relève du bloc 3, ou propose sa révision par une décision citant M24.
- **Q2 — Propriétaire de la population active et de g_N** (bloc 3 ou 5 ; `tab:symboles` : « travail et ménages »). Au socle, la population active est une tendance exogène ou résulte d'un taux d'activité.
- **Q3 — Lecture de l'anticipation en phase 1** : à l'ouverture, formée au pas précédent, ou après le bloc 8 dans la même phase. La seconde lecture engage la fiche 8 sur l'ordre interne de la phase 1.
- **Q4 — Conversion des taux annuels dans la règle de salaire** (anticipation, croissance de la productivité ; #24) : linéaire, conforme à M22 et M24 (f), ou autre, avec son effet chiffré (critères 3 (b) et 9 (c)).
- **Q5 — Variante de référence** : l'instruction couvre au moins une variante **sans retard d'emploi**, N = min{N*, population active}, à côté de toute variante à retard (critère 10 (b)). Elle couvre aussi les options A (v1.5 : `eq:labour` l. 532, `eq:wage` l. 612, `eq:un` l. 724) et B (v2.0 : `model.py` l. 653, 669, 1338 à 1358). Elle couvre enfin au moins une approche nouvelle tirée de la littérature, si l'instruction en trouve une pertinente.
- **Q6 — Ancrage de l'état stationnaire** : quelle grandeur la règle de salaire ancre (taux de chômage, part salariale), et laquelle elle laisse à d'autres blocs (rythme d'inflation : fiche 8).
- **Q7 — Levier institutionnel** (salaire minimum, indexation légale) : instruit comme option, avec sa contrepartie, ou renvoyé au catalogue des leviers (J4).

## 2. Critères d'évaluation, écrits avant l'instruction

**Statut** : proposés par `macro` le 03/10/2026, **validés par le mainteneur le 03/10/2026**, avec les amendements ci-dessous (jalon 1 de #39). La liste est fermée : elle ne se déplace pas après observation (`docs/exigences.md` § 2.5). Un amendement adopté avant l'instruction se consigne sous le tableau.

Correspondance avec le gabarit :

| Critère du gabarit | Critère de la fiche |
|---|---|
| 1 | 1 et 8 |
| 2 | 3 et 4 |
| 3 | 5 |
| 4 | 13 |
| 5 | 11 |
| 6 | 7 et 12 |

Critères propres au bloc : 2, 6, 9, 10, 14, 15, 16.

Sont des **exigences** (ils peuvent écarter une option) : 1, 2, 3, 4, 5 (a), (b), (c) pour l'amortissement et la bande de la calibration proposée, 6, 7, 8, 9 (a) et (c), 10 (b), 11 (b), 12 (sans historique ni drapeau), 13 (sans itération), 14, 16.

Sont des **mesures** (elles décrivent sans écarter) : 5 (c) aux vitesses ×0,5 et ×2, 5 (d), 9 (b), 10 (a) et (c), 11 (a), (c) et (d), 12 (décompte), 13 (décompte), 15.

| N° | Critère | Ce qui est attendu (seuil ou forme du verdict) | Par quoi on le vérifie | Qui | Quand |
|---|---|---|---|---|---|
| 1 | Cohérence stock-flux (gabarit 1 ; `macro`) — **exigence** | (a) Le seul flux proposé par le bloc est la **ligne 5**, WB = W·N : ménages +WB, entreprises (sous-colonne « courant ») −WB, en phase 4. Signature de `tab:portes-monnaie` inchangée. Aucune ligne nouvelle. Une option qui en exige une la déclare, avec sa phase et sa signature : c'est un contrat partagé, donc une décision citant M22. (b) Aucun poste de `tab:matrice-bilans` n'est ajouté par le bloc ; une variable d'état en personnes n'est pas un poste. (c) Les cotisations, allocations et impôts sur les salaires ne sont pas proposés par le bloc 3 (fiches 5 et 9) : une option qui les porte (v1.5 τ_S, l. 536) dit à quelle ligne existante ils iraient | Matrice des flux de l'option, écrite en tableau. Si une table change : `uv run python outils/verifier_matrices.py --strict <copie>`, sorties citées | `macro` | fiche ; J3 (identités, ε = 1e−12 × S, M22) |
| 2 | Contrats hérités, phases et lectures (tableau du § 1.1 ; ADR 0007 ; Q4) — **exigence** | (a) N_{j,t} est écrit en phase 4 avant le bloc 2. Il ne lit que l'ouverture, les phases 1 à 3 et, en phase 4, rien d'autre que ce qui précède le bloc 3. Aucune lecture de y_t, de y^cap ni de tu du pas. (b) W_t est écrit en phase 1. Il ne lit que l'ouverture, le registre et, si la fiche le déclare, l'anticipation écrite avant lui dans la phase 1 (Q3). L'ordre « banque centrale, puis travail », s'il est retenu, est déclaré pour report dans `tab:phases`. (c) N* = y*/pr et UC = W/pr restent ceux de M24. Une option qui exige une autre demande de travail ou UC = WB/y le déclare comme révision de M24. (d) Q4 est confirmée, ou une révision est proposée avec la décision citant M24 qu'elle exige. (e) La matrice des lectures reste triangulaire | Tableau phase → lit / écrit par option ; triangularité vérifiée à la main | `macro` | fiche ; J2 (test de triangularité de l'ordonnanceur) |
| 3 | État stationnaire en forme fermée (gabarit 2 ; `macro`) — **exigence** | (a) Trajectoire de référence : volumes en croissance annuelle g, prix en hausse de (1 + π̄)^{1/n_a} − 1 par pas (π̄ : glissement annuel stationnaire, amendement de la fiche 2), population active en croissance g_N. Sur cette trajectoire, chaque grandeur du bloc a une valeur stationnaire en forme fermée, calculée à la main ou par le script d'état stationnaire d'`outils/`, sans simulation : taux de chômage, N/N*, (y/N)/pr, W/(p·pr), croissance du salaire nominal par pas et en glissement annuel, masse salariale excédentaire. Chaque variable d'état a sa valeur stationnaire explicite, d'où se déduit l'état initial résolu sans préparation (`docs/exigences.md` § 2.6). (b) **Indépendance envers n_a** : le taux de chômage, la part salariale et la croissance annuelle du salaire réel ne dépendent pas de n_a. Toute dépendance (conversion de l'anticipation, de g_pr ou de g_N ; Q4, #24) est écrite et chiffrée pour n_a = 4, 12 et 52, avec la condition qui la supprime. (c) La source de g_N et son propriétaire sont déclarés (Q2). (d) **Cohérence avec la fiche 4** : la fiche écrit la condition que son état stationnaire impose à la marge (part salariale compatible). L'état stationnaire conjoint des blocs 3 et 4 est calculé en forme fermée quand la fiche 4 est « avis rendus », avant M25 et M26 | Calcul à la main dans la fiche. Au J3, script contre moteur : un pas sans choc depuis l'état initial résolu laisse chaque variable d'état du bloc sur sa trajectoire stationnaire à **1e−10 près en relatif** (seuil de la fiche 2, reconduit) | `macro` | fiche ; avant M25-M26 ; J3 |
| 4 | Aucune vitesse d'ajustement ne détermine l'état d'arrivée (`docs/exigences.md` § 2.7 ; `macro`) — **exigence** | (a) Aucune vitesse, ni la durée du pas, n'apparaît dans les formes fermées du critère 3. Sont visées : l'ajustement de l'emploi λ_N, le rappel du salaire vers une cible, le lissage de la productivité ou de l'indexation. Cas à examiner explicitement : un ajustement partiel de l'emploi vers un N* qui croît de g_N/n_a par pas laisse N < N* à l'état stationnaire, d'un écart qui dépend de λ_N, sauf terme de tendance (même construction que `sec:production` l. 617). Si une dépendance subsiste, la fiche l'écrit, la chiffre pour la vitesse divisée et multipliée par 2, et dit la condition qui la supprime. Les vitesses hebdomadaires des options A et B (v1.5 λ_L = 0,25 par semaine, l. 2261 ; v2.0 `lam_L_2`, `model.py` l. 669) sont converties en base annuelle et confrontées à λ ≤ n_a. (b) **Aucun intégrateur sans ancre** : une hystérèse du chômage de référence (v1.5 `eq:un` l. 724 ; v2.0 u_n hystérétique, 5,125 % contre 5 % en H0, S+O, `archive/faits_mesures_G_K.md` § 3) ou une règle de croissance salariale sans terme de niveau crée un continuum d'équilibres. La fiche le documente comme tel et le soumet au mainteneur. (c) La fiche dit quelle grandeur nominale le bloc ne détermine pas : le rythme d'inflation, ancré par la fiche 8 ; question ouverte au terme de K, faits § 7 | Calcul à la main sur les formes fermées. Au J3, depuis l'état initial résolu : dépense publique +1 % pendant 12 tours ; deux branches où toutes les vitesses du bloc sont multipliées par 0,5 et par 2 (dans λ ≤ n_a). Écart relatif de chaque ratio du bloc entre les deux branches ≤ **1e−6 après 720 pas** (seuil de la fiche 2, reconduit) | `macro` | fiche ; J3 |
| 5 | Stabilité (gabarit 3 ; `macro` ; (c) : condition 5 de `jeu`) — **exigence** pour (a), (b) et (c) ; **mesure** pour (c) aux vitesses ×0,5 et ×2 et pour (d) | (a) **Instabilités et hypothèses connues** (faits § 6 à 8), non réintroduites sans fait nouveau : n° 7 (ancrage salarial fort sur la productivité marginale ; sans objet sous la technique de M24, à vérifier pour A et B) ; n° 15 (un plafond produit un cycle : borne d'offre de travail, critère 7) ; n° 16 (tolérances absolues) ; défaut G-W (O) : l'indexation sur max(π^e, π) fait cliquet à la baisse. Les hypothèses réfutées n° 7, 9 et 10 ne sont pas reprises sans fait nouveau. Les acquis (§ 8 : WS-PS, R ; « l'emploi au profit nul était un stabilisateur caché de la v1 », R) sont discutés. (b) **Boucle propre du bloc** (emploi, salaire), demande et prix exogènes, au pas mensuel : valeurs propres de la récurrence linéarisée de module **strictement inférieur à 1**, pour la calibration proposée et pour chaque vitesse ×0,5 et ×2 ; module, demi-vie en tours, période si les racines sont complexes. (c) **Boucle combinée production – stocks – emploi** (condition 5 de `jeu`, fiche 2 § 9.5), si l'emploi s'ajuste avec retard. Système N1 à N7 de la fiche 2, avec la règle d'emploi et la demande induite d = A + m·y_{t−1}, pour m = 0,5, 0,6, 0,7 et 0,8 (hypothèse ; m effectif fourni par les fiches 5 et 9 au J3). Rayon spectral < 1 pour la calibration et pour toutes les vitesses (λ_v, λ_IN, λ_N) ×0,5 et ×2. Pour la calibration proposée : période dans la **bande de 36 à 96 tours** (3 à 8 ans) et demi-vie de l'écart d'emploi, ln 2 / (−ln(1 − λ_N/n_a)) tours, avec la valeur de λ_N qu'elle implique. Aux vitesses ×0,5 et ×2, la période et la demi-vie sont publiées sans être exigées (question au mainteneur). (d) **Boucle salaires – prix** : rayon spectral sur les règles des fiches 3 et 4 réunies, mesuré quand la fiche 4 est « avis rendus », avant M25 et M26 | Liste des faits § 6 à 8, puis `tab:instabilites`. Valeurs propres calculées à la main ou par `uv run python`, commande et sortie citées | `macro` | fiche ; avant M25-M26 ; J3 |
| 6 | Test zéro des ratios du bloc (`docs/exigences.md` § 2.6 ; O1 ; `macro`) — **exigence**, mesurée au J3 | Sur 60 ans (720 pas) sans choc depuis l'état initial résolu, pour plusieurs graines : la moyenne par blocs de 5 ans (60 pas) de chaque ratio reste dans sa bande autour de la valeur stationnaire résolue. **Bandes proposées**, à confirmer par le mainteneur avec O1 avant l'essai (M19) : taux de chômage (fraction de la population active) ±0,5 point ; part salariale (somme des WB sur somme de la valeur ajoutée en u.m., 12 tours) ±1 point ; croissance annuelle du salaire réel sur 12 tours ±0,1 point autour de la croissance effective de pr. Pour mémoire seulement, sans valeur de référence : D1 rapporte un chômage de 5,18 %, 12 blocs sur 12 dans 4 à 8 %, et une dérive de la part salariale de 0,147 point (R, faits § 2). Toute dérive depuis l'état résolu est un défaut | Au stade de la fiche, seul le préalable (critère 3) se vérifie ; au J3, test zéro du socle | `macro` ; mainteneur (bandes) | J3 |
| 7 | Bornes, dont la contrainte d'offre de travail (gabarit 6 ; `docs/exigences.md` § 2.7 ; #38 ; `macro`) — **exigence** | (a) **Emploi au plus égal à la population active.** Dans les deux lectures de #38, la borne est déclarée dans la section, avec sa forme et la grandeur qu'elle lit (population active : propriétaire, unité, valeur stationnaire). Elle figure dans au moins un test. Sous la lecture (i), son paramètre est nommé (par exemple un taux d'emploi maximal, ou l'énoncé que la population active en tient lieu). Sous la lecture (ii), elle est déclarée physique, sans seuil libre. Dans les deux lectures, elle est **inactive à l'état stationnaire**, avec la marge chiffrée (taux de chômage stationnaire > 0, en points). La fiche dit le mécanisme qui l'en éloigne en trajectoire normale (« préférer un mécanisme à une borne »). Quand elle est active, l'excédent N* − N apparaît comme production visée non réalisée (fiche 2) ; la fiche dit qui est rationné si J ≥ 2 (hors socle). (b) Autres bornes de chaque option (N ≥ 0 ; planchers et plafonds de salaire, comme les clips 0,9 et 2,0 et la baisse de 20 % de la v2.0, `model.py` l. 1356 ; idx_u, l. 1338 ; plafond payable de la v1.5, l. 619) : chacune est déclarée avec son paramètre et motivée contre un mécanisme, et son activité à l'état stationnaire est dite. (c) **Instabilité 15** : activer la borne ne produit pas de cycle. Seuil proposé : la borne cesse d'être active au plus tard 12 tours après la fin du choc et ne se réactive pas sans nouveau choc | Décompte des bornes par option. Cas à la main : N* supérieur de 2 % à la population active pendant un tour, flux et grandeurs restituées. Au J3 ou au J4 : scénario de dépense publique dimensionnée pour activer la borne pendant 12 tours | `macro` ; mainteneur (seuil de (c)) | fiche ; J3 ou J4 |
| 8 | Masse salariale en cas de rétention (fiche 2 § 9.8 ; `macro`) — **exigence** (comptable), **mesure** (ampleur) | (a) Quand N > y/pr (rétention, y = y* < pr·N), la masse salariale excédentaire W·(N − y/pr) = WB − UC·y est une **charge du pas** de la sous-colonne « courant ». Elle n'entre ni dans IN (M24 (a)) ni dans aucun poste ; la ligne 5 reste WB = W·N. (b) Sa valeur stationnaire est donnée : nulle si N = N* à l'état stationnaire, sinon explicite et rattachée au critère 4 (a). (c) Effet sur les profits non distribués (fiche 6, #36) écrit sur un pas. (d) Cas symétrique N < N* : y = pr·N < y*, aucun salaire n'est versé pour l'emploi non pourvu, la production visée non réalisée est restituée | Calcul à la main sur un pas où N = 1,02·N* : WB, UC·y, ΔIN, résultat courant | `macro` | fiche ; J3 (identités) |
| 9 | Frontière inflation (`docs/blocs/README.md` § 2 ; `macro` ; avis de `monnaie` au § 6) — **exigence** pour (a) et (c), **mesure** pour (b) | (a) **Variable d'anticipation consommée** déclarée : définition (glissement annuel anticipé de quel indice, sur quel horizon), unité (fraction par an), fenêtre, phase et ordre de lecture (Q3), valeur stationnaire requise (égale à π̄). La loi de formation et la crédibilité sont laissées à la fiche 8, et la fiche le dit. (b) **Indexation** : forme (anticipation, inflation passée, max ou combinaison), coefficient et pente de long terme de la relation salaires – chômage, verticale ou non. Si elle n'est pas verticale, la dépendance du chômage stationnaire à π̄ est écrite et chiffrée pour π̄ = 2 % et 10 %. Le cas de la v1.5 est examiné sans être tenu pour un fait : γ_A < 1 donnerait une inflation stationnaire π* − (1 − γ_A)g (l. 619 ; équation jamais garantie exécutée). (c) **Conversion** de l'anticipation annuelle en croissance du salaire par pas (Q4, #24), déclarée, avec son effet chiffré sur le chômage stationnaire. (d) `monnaie` rend son avis sur (a) à (c) au § 6. Un désaccord est décrit en deux positions et le mainteneur tranche | Formes fermées ; tableau de la variable consommée ; avis de `monnaie` | `macro` ; `monnaie` | fiche ; fiche 8 (loi de formation) |
| 10 | Retard d'emploi : justification empirique (fiche 2 § 9.8 ; préférence de `jeu`, fiche 2 § 7 ; `macro`) — **mesure** pour (a) et (c), **exigence** pour (b) | (a) Pour toute option à retard d'emploi (ajustement partiel, rétention), la fiche cite des faits **établis**, avec source retrouvée et date : relation de court terme entre production et chômage ou emploi (loi d'Okun) ; productivité apparente procyclique et rétention de main-d'œuvre. Elle sépare ce que le modèle produit, ce qui est établi et ce qui est contesté (par exemple, l'évolution de la cyclicité de la productivité). Sources candidates, **non lues à ce jalon** : Okun (1962) ; Oi (1962), cité par la v2.0 l. 669 ; Ball, Leigh et Loungani (2017), *Journal of Money, Credit and Banking* 49(7), 1413-1441, existence vérifiée ; Biddle (2014), *Journal of Economic Perspectives* 28(2), 197-212, existence vérifiée. (b) **Tension avec `docs/exigences.md` § 2.7** (« préférer une correction sans retard ») : un retard n'est retenu que s'il est soutenu par (a) et par un mécanisme perçu à l'échelle d'une partie (critère 11). Sinon, la variante sans retard (Q5) prévaut. (c) La calibration de λ_N, traduite en demi-vie en tours, est confrontée aux ordres de grandeur sourcés ; une source introuvable est déclarée | Sources citées ; mention « non trouvée » le cas échéant ; avis de `jeu` | `macro` ; `jeu` | fiche |
| 11 | Lisibilité pour le joueur (gabarit 5 ; `macro`, à soumettre à `jeu`) — **exigence** pour (b), **mesure** pour (a), (c) et (d) | (a) **Indicateurs au tour**, chacun avec définition, unité, dénominateur et fenêtre : taux de chômage ; emploi ; salaire nominal (glissement sur 12 tours) ; salaire réel ; part salariale (12 tours) ; **productivité apparente y/N rapportée à sa tendance pr**, si un retard est retenu ; masse salariale excédentaire, si rétention. S'y ajoutent les niveaux normaux (taux de chômage et part salariale stationnaires, publiés par le script d'état stationnaire), comme pour la condition 2 de `jeu` à la fiche 2. (b) **Délais en tours entiers** : demande → emploi ; chômage → salaire (au moins 1 tour, la phase 1 lisant l'ouverture) ; salaire → prix (fiche 4). La contrepartie est visible le même tour (production visée non réalisée, stocks, productivité apparente). Aucun effet plus rapide que le tour sans contrepartie. (c) Tableau levier → indicateur → délai → contrepartie pour les leviers qui transitent par le bloc. Aucun levier propre sans décision (Q7) ; aucun drapeau de mode. (d) Ampleur et période (critère 5 (c)) perceptibles sur 60 à 120 tours. La « préférence pour un retard modéré » de `jeu` est traduite en fourchette de demi-vie de l'emploi en tours, **seuil à proposer par `jeu` au mainteneur** | Tableau du § 9, « Interfaces ». Exemple daté à la main, même choc que la fiche 2 (dépense publique +1 % aux tours 1 à 12, part de G 20 %, hypothèse) : emploi, chômage, salaire et productivité apparente aux tours 1, 2, 3, 4, 9, 13, 14, 18 et 24. Avis de `jeu` (§ 7) ; au J4, scénario apparié (O2) | `jeu` ; `macro` (exemple daté) | fiche ; J4 |
| 12 | Simplicité, empreinte sur l'état, déterminisme (gabarit 6 et rubrique 9 ; principe de simplicité ; `macro`) — **mesure** (décompte) et **exigence** (sans historique ni drapeau) | Décompte par option : paramètres, bornes, variables d'état, registres, lignes, phases touchées ; chaque élément est justifié par une identité vérifiable ou un mécanisme perçu. Chaque variable d'état a son unité et sa valeur stationnaire (critère 3). Un retard ou un glissement sur 12 tours dont la règle a besoin est une variable d'état ou un registre de longueur fixe déclaré, comme celui des prix (`sec:cadre-calendrier`), jamais un historique. Une seule règle par mécanisme, aucun drapeau de mode (ADR 0002). Aucun tirage, ou un tirage par la graine du pays, déclaré | Tableau de décompte ; liste des variables d'état | `macro` | fiche ; J2 (reprise exacte) |
| 13 | Coût de calcul (gabarit 4 ; `macro`) — **exigence** (aucune itération) et **mesure** (décompte) | Aucune itération ni optimisation à chaque pas (ADR 0002). Décompte des opérations par pas. **Part indicative proposée : 0,48 ms par pays-pas**, celle que le mainteneur a adoptée pour le bloc 2 ((52/12 − 0,5)/8) | Décompte dans la fiche ; au J3, `tests/invariants/test_budget.py` | `macro` ; `audit` | fiche ; J3 |
| 14 | Notation (`CONVENTIONS.md` § 5.2 ; décision du 02/10/2026 sur #23 ; `macro`) — **exigence** | Chaque symbole a un seul sens et n'entre pas en collision avec les indices réservés (c, j, k, h, t ; s, ℓ, u du cadre) ni avec `tab:symboles`. En particulier, le taux de chômage ne s'écrit pas u, la population active ne s'écrit pas L, et N, N*, W, WB, UC, pr gardent leur sens. L'anticipation suit la convention de l'exposant e, son symbole étant fixé avec la fiche 8 | Liste des symboles confrontée à `tab:symboles` (commande `grep` et sortie citées) | `macro` ; `docwriter` (section) | fiche ; section proposée |
| 15 | Calibrabilité et faits établis (`macro`) — **mesure** | Les paramètres se calibrent sur des ordres de grandeur établis : taux de chômage, part salariale, pente de la relation salaires – chômage, coefficient d'Okun, vitesse d'ajustement de l'emploi. Chacun porte sa source retrouvée et sa date. Un résultat de la v1.5 ou de la v2.0 n'est pas un fait établi ; une source introuvable est déclarée | Sources citées ; « non trouvée » le cas échéant | `macro` | fiche ; J3 (calibration) |
| 16 | Remesure des faits de la première tentative (décision P1 du 03/10/2026 ; `CONTEXT.md` ; `macro`) — **exigence** de procédure | (a) Chaque fait cité porte son statut (S+O, O, R, L, V, V+O). Les faits établis sur D1 (G-W, H0, I1c ; faits § 3 et 4) ne sont pas remesurables (D1 non versé) et sont cités avec leur statut d'origine. (b) Toute remesure (statut V) passe par un script d'`outils/` qui exécute le prototype **dans un processus séparé, jamais par import** (invariant 4), revu par `audit` (circuit 3, `coder` → `audit`). Ses critères sont écrits dans la fiche **avant l'essai**, sur le modèle de la remesure S1 (fiche 2 § 9.7) : grandeur, définition, unité, fenêtre, seuil. Son verdict est publié même défavorable. V+O seulement si le vérificateur réexécute le script. (c) Un fait V sur le prototype v2.0 reste un fait de la première tentative, jamais un résultat v3. (d) Les lectures de code (L) citent fichier et ligne, vérifiés à la date de la fiche | Liste des faits et statuts ; commande, sortie et commit de chaque script | `macro` ; `coder` ; `audit` | fiche (jalon 2) |

### Amendements adoptés

Décisions du mainteneur du 03/10/2026, prises avant l'instruction, sur les questions de `macro` :

- **Critères** : les seize critères sont validés tels quels, avec leur nature (exigence ou mesure).
- **Seuils reconduits de la fiche 2**, adoptés : critère 3, 1e−10 en relatif au J3 ; critère 4, écart ≤ 1e−6 après 720 pas entre les branches ×0,5 et ×2 ; critère 13, 0,48 ms par pays-pas.
- **Seuils proposés**, adoptés : bandes du test zéro du critère 6 (chômage ±0,5 point, part salariale ±1 point, croissance annuelle du salaire réel ±0,1 point), à confirmer avec O1 avant l'essai (M19) ; critère 7 (c), la borne d'offre de travail cesse d'être active au plus tard 12 tours après la fin du choc.
- **Critère 5 (c)** : la bande de 36 à 96 tours n'est exigée que pour la calibration proposée ; aux vitesses ×0,5 et ×2, la stabilité est exigée, la période et la demi-vie sont publiées.
- **Critère 7 et #38** : lecture (ii) retenue (décision du 03/10/2026, `CONVENTIONS.md` § 2.4) ; l'emploi au plus égal à la population active est une contrainte de conservation, sans paramètre, déclarée dans les `\limites` avec son activité à l'état stationnaire et un test.
- **Critère 9 (b)** : la pente de long terme de la relation salaires – chômage reste une mesure.
- **Critère 10 (b)** : règle de `macro` adoptée ; un retard d'emploi n'est retenu que s'il est soutenu par un fait établi et sourcé et par un mécanisme perçu ; la variante sans retard est toujours instruite comme référence.
- **Q2** : la fiche instruit la population active comme tendance exogène du socle ; son propriétaire (bloc 3 ou 5) est fixé à M25.
- **Q3** : les deux lectures de l'anticipation en phase 1 sont instruites ; si la lecture « après le bloc 8 » est retenue, l'ordre « banque centrale, puis travail » est reporté dans l'inventaire comme engagement de la fiche 8.
- **Q7** : le levier institutionnel (salaire minimum, indexation légale) est renvoyé au catalogue des leviers (J4) ; la fiche en note l'interface.
- **Amendement du 03/10/2026, pris avec la validation des critères de la fiche 4** : la condition de compatibilité de la part salariale (critère 3 (d)) s'écrit sur W/(p·pr), l'écart avec WB/VA sur 12 tours étant publié ; la bande du test zéro sur la part salariale (critère 6) est commune aux fiches 3 et 4, sur une seule définition ; une seule lecture des taux annuels (#24) vaut pour les fiches 3, 4 et 8 (Q4), choisie à M25-M26.

## 3. Options

*Rédigé par `macro` (expert pilote), 03/10/2026, sur la fiche à l'état `17f5137` (critères validés le 03/10/2026) et la spécification au même commit (branche `claude/j1-economie-reelle`, PR #43).*

### 3.0 Conventions de l'instruction

**Notation provisoire** (critère 14). Elle est fixée à la décision.
- U_t : taux de chômage, en fraction de la population active.
- U^eq : chômage d'équilibre (paramètre).
- N^pa_t : population active, en personnes.
- ω_t = W_t/(P_t·pr_t) : part salariale unitaire, c'est-à-dire le salaire réel rapporté à la productivité du § 1.2.
- ω* : norme de part salariale (cible). ω̄ : sa valeur stationnaire.
- λ_w, λ_N : vitesses annuelles.
- β : semi-élasticité du salaire cible au chômage, par unité de taux.
- φ : pente de Phillips, par an.
- μ̄ : marge normale (symbole de la fiche 4).
- π^e_t : anticipation (symbole fixé avec la fiche 8).

Contrôle C12 : `grep -c -F` sur `docs/specification/nations_et_marches.tex` pour `$U`, `U_`, `U^`, `\omega`, `\beta`, `\mathrm{pa}`, `\mathrm{eq}`, `\lambda_w`, `\lambda_N`, `\pi^e`, `\mathit{PA}`. Sortie : 0 pour chacun. `\mu` compte 5 occurrences, toutes dans `\multicolumn` : aucun symbole μ n'est employé. Réserve : U voisine de \mathit{UC}. Autre choix possible : \mathit{ch}, à juger par `docwriter`.

**Hypothèses de calcul**, qui ne sont pas des calibrations :
- g_pr = 2 % par an ; g_N = 0,5 % par an (et 1 %) ; U* = 5 % ;
- fiche 2 : λ_v = 3 et λ_IN = 1,5 par an, σ = 1,4 mois ;
- λ_w = 1 par an et β = 2 (valeurs de la v2.0, `model.py` l. 138 et 136) ;
- λ_N = 2,4 par an (proposée en 3.C) ;
- m = 0,5 à 0,8.

**Calculs** (commande : `uv run --no-project [--with numpy] python <script>`) :

| N° | Script | Objet |
|---|---|---|
| C1 | `t1_conversion.py` | conversion linéaire, forme additive (A, B) |
| C2 | `t2_ajustement.py` | ajustement partiel sans terme de tendance sous M24 (formule et simulation concordantes à 1e−6) |
| C3 | `t3_boucle.py`, `t3b.py` | validation de la construction contre la fiche 2 |
| C4 | `t4_c5c.py` | boucle combinée, critère 5 (c) |
| C5 | `t5_e1.py` | seuil de bande de D ; impulsions non linéaires |
| C6 | `t6_exemple.py` | exemple daté |
| C7 | `t7_propre.py` | boucle propre (5 (b)) ; grandeurs stationnaires de A |
| C8 | `t8_borne.py` | borne d'offre de travail (7 (c)) |
| C9 | `t9_cout.py` | coût |
| C10 | `t10_formes.py` | formes fermées ; critère 8 ; coefficient d'Okun |
| C11 | `t11_q4.py` | conversion de l'anticipation (forme multiplicative, R, C, D) |
| C12 | `grep` | notation |
| C13 | `t12_partVA.py` | écart entre W/(p·pr) et WB/VA sur 12 tours |

**Validation C3.** Avec g = 0, la construction reproduit exactement la fiche 2, § 3.N-8 :
- 0,9459 et 73,0 mois (m = 0,6) ; 0,9770 et 95,9 (m = 0,8) ;
- 0,9681 et 146,9 (×0,5) ; 0,9209 et 37,6 (×2) ;
- paire 0,9092 et 51,7 (ajustement partiel, λ_N = 2,08).

Avec g = 2 %, on trouve 0,9452 et 72,9 ; 0,9762 et 95,8. **Observation transmise à la fiche 2** : les chiffres de boucle fermée de son § 3.N-8 correspondent à g = 0. L'écart est d'au plus 0,0008 sur le rayon spectral et de 0,7 mois sur la période ; aucun verdict ne change.

**Intégrité des sources.** `sha256sum` de `archive/v2.0/prototype/model.py` (e1505b7e…) et de `archive/v1.5/Nations_et_Marches_v1_5.tex` (097d023f…) : identiques à `tests/invariants/archive_sha256.txt`. Lignes vérifiées le 03/10/2026.

### 3.A Option A — v1.5

1. **Source.** `archive/v1.5/Nations_et_Marches_v1_5.tex` : `eq:labour` (l. 528 à 533), `eq:wage` (l. 605 à 612), offre de travail (l. 708 à 711), `eq:un` (l. 722 à 724) et table de calibration (l. 2260, 2261, 2293, 2313, 2327, 2347, 2369). **Équations jamais garanties exécutées.**

2. **Équations.**
   - Demande de travail : L* = min{(Ŷ/(A K^α H^{1−α}))^{1/(1−α)}, (1−α)pŶ/(W(1+τ_S))}.
   - Ajustement partiel sans terme de tendance : L_{t+1} = L_t + λ_L(L* − L_t), avec λ_L = 0,25 par semaine (l. 2261) et λ_L/2 pour l'équipement (l. 2327).
   - Salaire, révisé chaque mois : W_{t+1}/W_t = 1 + ω_u ϖ_w π^ref + φ_u(u^n − u) + φ_x min(x^L, 1) + φ_v v_j + γ_A ĝ^prod, avec W ≥ W^min. Termes :
     - π^ref = cπ^e + (1−c)max(π^e, π) ;
     - ω_u = clip(1 − 2[u − u^n]^+, 0, 1) ;
     - x^L = [ΣL*/((1−u^n)L^S) − 1]^+ ;
     - deux règles de bord (l. 619) : un plafond payable, et une baisse de 20 % par mois si l'emploi rentable tombe sous la moitié de l'emploi technique.
   - Chômage naturel endogène : u^n_{t+1} = max(u^n + η_u(u − u^n) + η'_u(u^n_0 − u^n), 3 %), avec η_u = 0,03 et η'_u = 0,01 par mois, et u^n_0 = 5 % (l. 2293).
   - Valeurs : φ_u = 0,3 (l. 2260) ; γ_A = 1 et φ_x = 0,3 (l. 2313). **φ_v n'a aucune valeur dans la table** (`grep phi_v` : l. 607 et 615 seulement).

3. **Révision de M24, déclarée.** La demande de travail au produit marginal et la technique Cobb-Douglas contredisent N* = y*/pr et la technique de Leontief (§ 1.1). La transposition sur M24 retire le second terme du min.
   - Unités du salaire : le texte ne dit pas si π^ref, taux annuel, est divisé par 12 dans une révision mensuelle. L'équation est dimensionnellement ambiguë.
   - Le τ_S (l. 536) relèverait de la ligne 7 (fiche 9), non du bloc 3 (critère 1 (c)).

4. **Comportement.** Non mesuré. Les résultats cités par la v1.5 (l. 619 : « ce que le prototype a montré » ; l. 731 ; l. 2397) sont rapportés par la v1.5 et invérifiables.

5. **État stationnaire et vitesses** (C2, C7 ; transposition sur M24, g_N = 0,5 %) :
   - **Condition λ ≤ n_a (M22) violée.** λ_L = 0,25 par semaine fait 13 par an, au-dessus de n_a = 12. Valeur propre de l'emploi : 1 − 13/12 = −0,0833 (alternance d'un mois sur l'autre). À ×2, −1,1667 : **explosive**.
   - N/N* stationnaire : 1,000032 à λ = 13 ; 0,9996477 à ×0,5, d'où un stock d'ouverture à 0,998013 de la cible ; 1,0002243 à ×2. **La vitesse détermine l'état d'arrivée** (critère 4).
   - Le terme φ_v v est non nul à l'état stationnaire. Avec u^n ancré (η' > 0), le chômage stationnaire vaut u^n = 0,75u + 0,25u^n_0 et U* − u^n_0 = 4(φ_v/φ_u)v. Avec φ_v = 0,1 (hypothèse, valeur de la v2.0 l. 1360), on trouve −0,0043 point (λ = 13), +0,0470 point (×0,5) et −0,0299 point (×2).
   - L'hystérèse est ancrée, donc ce n'est pas un continuum strict : valeur propre 0,96 par mois, demi-vie de 17 tours (concorde avec la l. 2397).
   - **Le salaire n'a pas de terme de niveau** : valeur propre 1 à prix exogènes, **échec du critère 5 (b)**.
   - Cas γ_A < 1 (l. 619) examiné. La formule π* − (1 − γ_A)g ne vaut que si π^e est ancrée à π*. Si π^e = π̄, c'est U qui se déplace, de (1 − γ_A)g/φ_u.

6. **Bornes** (critère 7) : neuf.
   - L* ≤ L_prof ; W ≥ W^min ; plafond payable ;
   - baisse de 20 % sous le seuil de 1/2 ;
   - clip de ω_u ; min(x^L, 1) ; partie positive de x^L ;
   - plancher u^n ≥ 3 % ; max(π^e, π).

7. **Défauts.**
   - Cliquet de l'indexation sur max(π^e, π) : défaut G-W (O).
   - Notation : u et L entrent en collision (critère 14).
   - Aucune valeur pour φ_v.

### 3.B Option B — v2.0

1. **Source.** `archive/v2.0/prototype/model.py`, profil `wsps2` (statut L) :
   - l. 652 à 670 : L_tech, L_prof (l. 657), min (l. 660), L_cash (l. 664), plafond 0,98·(N^act − LG) (l. 668), ajustement (l. 669), u (l. 670) ;
   - salaires, à chaque date de décision (13 par an, l. 36 à 38) : l. 1326 à 1363.

2. **Équations.**
   - Emploi : L ← L + lam_L_2·lam_L_sec·(L* − L), avec lam_L_2 = 0,04 par semaine (l. 141), soit **2,08 par an**, et lam_L_sec = (1, 1, 1, 0,5) (l. 268).
   - Salaire : W_new = W·clip(1 + [idx_u·ϖ_w·π_ref + λ_w·clip(ln(W*/W), ±0,5) + γ_A·g_A]/13, 0,9 ; 2,0), ou 0,8·W si `unprof` (l. 1337, 1356).
   - Cible : W* = (1−α)·p_va·Q̄/L/(1+τ_S)·exp(−β_u(u − u_ref)), avec u_ref = u_n0 = 5 % puisque h_ins = 0 (l. 137, 1349, 1352).
   - Bornes du salaire : W ≤ max(W_payable, 0,5W) (l. 1362) ; idx_u = clip(1 − 2[u − u_n]^+, 0, 1) (l. 1338).
   - Productivité : g_A lissée à 0,9/0,1 avec clip ±0,1 (l. 1326 à 1329).
   - Hystérèse : u_n (l. 1363), avec eta_u = 0,03/13 et eta_u2 = 0,01/13 **par décision** (l. 154), soit **0,03 et 0,01 par an**, contre 0,03 et 0,01 **par mois** dans la v1.5 (l. 2293). **Écart d'un facteur 12 entre les deux sources (L)** : demi-vie de 17,3 ans contre 17 mois.

3. **Révision de M24, déclarée.**
   - L_prof et W* reposent sur la productivité marginale d'une Cobb-Douglas.
   - Le bloc lit le prix et la trésorerie des entreprises. Transposé, il lirait le prix d'ouverture.

4. **Comportement** (faits de la première tentative) :
   - G-W (O) : forme active ; croissance salariale mesurée 6,19 % contre 6,22 % prédits ; cliquet.
   - H0 (S+O) : aucune borne salariale ni branche `unprof` sur 28 observations ; u_n compris entre 5,125137 et 5,125414 %.
   - I1c (O) : −0,495 point par an, dont −0,319 par le terme de niveau.
   - D1 sur 60 ans (R) : chômage 5,18 % ; dérive de la part salariale 0,147 point.
   - Contrôle de `macro` (calcul sur faits S+O, fenêtres différentes) : avec u_n ancré, u = (5,125 − 1,25)/0,75 = 5,167 %, cohérent avec le chômage final G1 de 5,185 % (S+O). D'où idx_u ≈ 0,9992 à l'état d'arrivée : **indexation incomplète, relation non verticale**.

5. **État stationnaire sous M24** (C2). Avec λ_N = 2,08 :
   - N/N* = 0,998018 et IN/IN* = 0,988803 (stock −1,12 %) à g_N = 0,5 % ;
   - 0,996045 et −2,23 % à g_N = 1 % ;
   - à ×0,5 : −2,47 % ; à ×2 : −0,44 %.

   **La vitesse détermine l'état d'arrivée** (critère 4), et l'égalité exacte IN^vol = n_aσv vérifiée par M24 est perdue.

6. **Boucle propre** (C7) : 0,8267 (emploi), 0,9167 (salaire, λ_w = 1), 0,99667 (u_n, demi-vie 207,6 tours), 0,9722 (u_rec), 0,9. Toutes sont inférieures à 1.
   - Le commentaire de la l. 138 dit « 2,0 est instable » pour λ_w. C'est un fait rapporté dans le code, non mesuré : remesure T1 demandée.

7. **Bornes** : treize environ.
   - L_prof, L_cash, plafond 0,98 (**à seuil libre** selon `CONVENTIONS.md` § 2.4) ;
   - u ≥ 0 ; clip de g_A ; clip ±0,5 ; clip de croissance 0,9 et 2,0 ;
   - `unprof` (0,8 et 1/2) ; W_payable et 0,5W ; clip de idx_u ;
   - max(π_e, π) ; plancher u_n ≥ 3 % ; `zombie`.

8. **Défauts.**
   - Instabilité 7 : W* ancré sur (1 − α) fois le produit moyen, c'est-à-dire la productivité marginale.
   - Cliquet G-W.
   - **État caché** : `getattr` et `hasattr` avec valeurs par défaut, l. 1327 à 1329 et 1348 (ADR 0002).
   - **Drapeaux de mode** : `wsps2`, `ws_anchor`, `L_prof_va`, `wage_indexation_mode`.

### 3.N Socle commun des options nouvelles (R, C, D)

#### 3.N-1 Population active (Q2)

- **(T1)** N^pa_{t+1} = N^pa_t·(1 + g_N/n_a), écrite en phase 4 du pas t. Tendance exogène (amendement Q2). Choix de conception.
- Cohérence avec M24 (f) : N* = y*/pr croît exactement de (1 + g/n_a)/(1 + g_pr/n_a) = 1 + g_N/n_a par pas. Le taux de chômage est donc constant sur la trajectoire de référence.
- Propriétaire proposé : **le bloc 3**, seul lecteur au socle. À fixer à M25.

#### 3.N-2 Règle de salaire : deux formes instruites (Q6)

- **(T2)** ω_{t−1} = W_{t−1}/(P_{t−1}·pr_{t−1}), avec pr_{t−1} = pr_t/(1 + g_pr/n_a). C'est une définition. P_{t−1} est la dernière entrée du registre ; le libellé exact de l'indice relève de la fiche 4 (#24).
- **(T3-SN) Salaire avec niveau (WS-PS ancrée, correction d'erreur)**, en phase 1 :
  ln W_t = ln W_{t−1} + ln(1 + g_pr/n_a) + (1/n_a)·ln(1 + π^e_t) + (λ_w/n_a)·[ln(ω*/ω_{t−1}) − β(U_{t−1} − U^eq)], avec λ_w ≤ n_a.
  - Sous la lecture (w1), ω* = 1/(1 + μ̄) : le terme de niveau vaut alors ln[(1 + μ_{t−1})/(1 + μ̄)], l'écart de la marge effective du pas précédent à la marge normale.
  - Statut : approchée. Provenance :
    - forme WS-PS (acquis R, faits § 8) ;
    - semi-élasticité calée sur l'élasticité de −0,1 de la courbe des salaires (Blanchflower et Oswald, NBER WP 11338, 2005, p. 1 et p. 4 ; −0,07 après correction du biais de publication), d'où β = 0,1/U* = 2 à U* = 5 % (1,4 avec −0,07). L'équation en correction d'erreur est discutée par Blanchard et Katz (NBER WP 6924, 1999, p. 5) : terme de niveau absent des équations agrégées américaines, voisin de 0,25 par an en Europe.
    - équation en correction d'erreur discutée par Blanchard et Katz (1999, *AER* 89(2), 69-74 ; notice retrouvée, contenu non lu).
- **(T3-SP) Phillips sans niveau** : ln W_t = ln W_{t−1} + ln(1 + g_pr/n_a) + (1/n_a)·ln(1 + π^e_t) − (φ/n_a)(U_{t−1} − U^eq). Elle est instruite pour comparaison.
- **Verdict sur SP.** À prix exogènes, la valeur propre du salaire vaut **1** : **échec du critère 5 (b)**. Le salaire réel n'a pas d'ancre propre, ce qui est un continuum au sens du critère 4 (b), documenté. Sous une marge instantanée, SN se réduit à SP avec φ = λ_w·β et U^eq = U* : SN n'apporte que la correction de l'écart de marge (fiche 4, terme de demande, instabilité 14), et c'est elle qui ancre le salaire réel du bloc. **SP est écartée.**
- **Paramétrage de la norme**, en deux lectures :
  - **(w1)** ω* = 1/(1 + μ̄), lu dans la fiche 4. U* = U^eq exactement. Trois paramètres : λ_w, β, U^eq. Une variation de μ̄ ne déplace pas U*. La variable de la règle est W/(p·pr), celle de la condition 3 (d).
  - **(w2)** ω* est un paramètre du bloc 3. U* = U^eq + ln(ω*(1 + μ̄))/β : une marge plus forte relève le chômage d'équilibre. Mais seul ln ω* + βU^eq est identifié, et l'un des deux devient une constante de calibration.
  - (w2) est l'interface naturelle d'un levier institutionnel (Q7, J4).
- **Indexation** : coefficient 1 sur π^e. Ni max(π^e, π), puisque le cliquet G-W est écarté, ni indexation sur l'inflation passée, pour éviter un double compte avec la loi adaptative de la fiche 8 et la Q6 de la fiche 4. La productivité entre par sa tendance g_pr, non par la productivité apparente (v1.5 ĝ^prod, v2.0 g_A), qui importerait le cycle de rétention.

#### 3.N-3 Anticipation consommée (critère 9 (a) ; Q3)

- **Variable** : π^e_t, glissement annuel anticipé de l'indice des prix P (J = 1 : p) sur les 12 tours à venir. Fraction par an. Valeur stationnaire requise : π̄. La loi de formation et la crédibilité relèvent de la fiche 8.
- **Lecture (a), à l'ouverture** : π^e formée au pas t − 1. Aucun ordre interne de la phase 1 n'est requis. Délai anticipation → salaire : 1 tour.
- **Lecture (b), après le bloc 8 dans la phase 1** : ordre « banque centrale, puis travail », engagement de la fiche 8 (amendement Q3). Délai : 0 tour. La lecture reste triangulaire si le bloc 8 ne lit pas W_t (il lit U_{t−1} à l'ouverture).
- Les états stationnaires sont identiques. Seule la dynamique diffère, d'un tour.

#### 3.N-4 Lecture commune des taux annuels (Q4, #24 ; critères 3 (b), 4 et 9 (c))

La lecture est **commune** aux fiches 3, 4 et 8 (décision du 03/10/2026). La forme mixte instruite plus haut, productivité linéaire et anticipation géométrique, est **exclue** par cette décision. Pour la cohérence de T1 avec N*, j'inclus g_N dans la lecture commune : N^pa doit croître exactement comme N* = y*/pr. Deux lectures sont instruites.

**Lecture (L), linéaire pour tous les taux** (x/n_a par pas, conforme à M22 et à M24 (f)) :
- Productivité ln(1 + g_pr/n_a) et population (1 + g_N/n_a) : exactes par construction.
- Anticipation ln(1 + π^e/n_a) : exacte seulement si π^e est un **taux annualisé linéaire**, c'est-à-dire n_a fois la hausse par pas anticipée.
  - Sa valeur stationnaire vaut alors n_a[(1 + π̄)^{1/n_a} − 1] : 1,9852 / 1,9819 / 1,9806 % pour π̄ = 2 % et n_a = 4 / 12 / 52 ; 9,6455 / 9,5690 / 9,5398 % pour π̄ = 10 %.
  - Ce n'est pas π̄. Le critère 9 (a) (« égale à π̄ ») ne serait tenu qu'à cette transposition près : **correction prospective du critère, à décider par le mainteneur**.
- Si au contraire la fiche 8 forme π^e sur le glissement mesuré (valeur stationnaire π̄), SN échoue au critère 4. Le tableau C11 reste valable : écart relatif de 2,71e−3 entre ×0,5 et ×2 à π̄ = 2 % et n_a = 12 ; U − U* de +0,009 point (2 %) et +0,214 point (10 %) à λ_w = 1.
- Cible : une cible de 2 % convertie linéairement donne un glissement effectif de 2,0151 / 2,0184 / 2,0197 % (n_a = 4 / 12 / 52) ; 10,3813 / 10,4713 / 10,5065 % pour 10 % (`sec:cadre-calendrier` le signale déjà).
- Croissance du salaire réel : 2,0151 / 2,0184 / 2,0197 %. Dépendance à n_a déclarée (critère 3 (b)).

**Lecture (G), géométrique pour tous les taux** ((1 + x)^{1/n_a} par pas, ou ln(1 + x)/n_a) :
- SN est exacte avec π^e défini comme glissement, de valeur stationnaire π̄ : le critère 9 (a) est tenu tel qu'il est écrit.
- U* et ω̄ ne dépendent ni de n_a ni de λ_w.
- La croissance du salaire réel vaut exactement g_pr pour tout n_a : le critère 3 (b) est entièrement satisfait. La cible donne exactement son glissement.
- Coût :
  - **révision de M24 (f)** (N9 : pr_{t+1} = pr_t(1 + g_pr)^{1/n_a} ; g = (1 + g_pr)(1 + g_N) − 1 ; `sec:production` l. 616 et 741 ; publication de 2,0184 % retirée) ;
  - une conversion des taux de croissance et d'inflation ajoutée à `sec:cadre-calendrier` (`CONVENTIONS.md` § 5.2) : **contrat partagé, décision citant M22 et M24**.
- Les taux d'intérêt, flux et vitesses restent linéaires (M22, lecture (a)), puisqu'un taux de croissance ou d'inflation n'est aucune des trois natures de M22.

**Ce que chaque lecture exige de la fiche 3** :
- (L) : l'anticipation consommée par SN doit être un taux linéaire annualisé (engagement de la fiche 8) et le critère 9 (a) doit être transposé.
- (G) : rien de plus. M24 (f) doit être révisée.
- Sous l'une ou l'autre lecture, SN reste exacte et indépendante des vitesses. **Seule la forme mixte, désormais exclue, et (L) avec une anticipation en glissement font échouer le critère 4.**

**Avis de `macro` sur la lecture commune.** Je préfère (G).
- C'est la seule qui tienne les critères 3 (b) et 9 (a) tels qu'ils sont écrits.
- Elle fait coïncider la cible, l'anticipation et le glissement restitué au joueur : « 2 % » veut dire 2 %.
- Le prix est la révision de M24 (f) : une ligne de N9, la forme de g, et le retrait d'un chiffre publié.

(L) est viable à deux conditions : la fiche 8 forme une anticipation en taux linéaire, et le critère 9 (a) est transposé. Le joueur verrait alors un glissement de 2,0184 % pour une cible de 2 %. Le choix revient au mainteneur, à M25-M26.

#### 3.N-5 Phases et lectures (critère 2)

| Phase | Le bloc 3 lit | Le bloc 3 écrit |
|---|---|---|
| 1 | ouverture : W_{t−1}, U_{t−1}, N^pa_t, pr_t, N_{t−1} (C et D) ; registre (P_{t−1}) ; π^e (lecture a : ouverture ; lecture b : après le bloc 8) | W_t |
| 4, avant le bloc 2 | N*_t (phase 2) ; W_t ; N^pa_t ; N_{t−1} (C et D) | N_t, U_t, WB_t = W_t·N_t (**ligne 5**), N^pa_{t+1} |

- Aucune lecture de y_t, de y^cap ni de tu. La matrice des lectures est triangulaire.
- **Q4 de la fiche 2 confirmée** : l'emploi est au bloc 3.
- La masse salariale excédentaire W(N − y/pr) est une grandeur d'observation, calculée après le bloc 2.

#### 3.N-6 État stationnaire en forme fermée (critères 3 et 4) ; état initial résolu

Sous SN, conversion géométrique, (w1), R ou C, sur la trajectoire de référence :
- U* = U^eq, soit 5 % ;
- N/N* = 1 ; (y/N)/pr = 1 ;
- ω̄ = 1/(1 + μ̄) (condition 3 (d) ci-dessous) ;
- masse salariale excédentaire nulle.

Croissance du salaire (C10) :

| | n_a = 4 | n_a = 12 | n_a = 52 |
|---|---|---|---|
| Salaire nominal par pas, π̄ = 2 % | 0,99877 % | 0,33210 % | 0,07657 % |
| Glissement annuel nominal, π̄ = 2 % | 4,0554 % | 4,0588 % | 4,0601 % |
| Glissement annuel nominal, π̄ = 10 % | 12,2166 % | 12,2203 % | 12,2217 % |
| Salaire réel annuel | 2,0151 % | 2,0184 % | 2,0197 % |

- **Dépendance déclarée à n_a** : la croissance du salaire réel hérite de la conversion linéaire de g_pr (M24 (f), #24). Elle disparaîtrait sous une conversion géométrique de g_pr, ce qui réviserait M24 (f). U* et ω̄ ne dépendent ni de n_a ni d'aucune vitesse.
- **Variables d'état** : W, U, N^pa (R) ; plus N_{t−1} (C et D).
- **État initial résolu** :
  - W_0 tel que ω = ω̄ ;
  - U_0 = U^eq ;
  - N^pa_0 = N_0/(1 − U^eq), avec N_0 = y_0/pr_0 ;
  - N_{−1} = N_0/(1 + g_N/n_a) pour C.
- **Condition 3 (d)** (décision du 03/10/2026), écrite sur **W/(p·pr)**. La valeur stationnaire de W/(p·pr) que donne la règle de prix doit égaler la norme ω* de SN : avec (w1), ω* = 1/(1 + μ̄), et la fiche 4 doit donner exactement p/UC = 1 + μ̄ à l'état stationnaire.
  - Si la fiche 4 marquait sur une autre base, par exemple le coût moyen pondéré, la condition se lirait sur la même variable W/(p·pr). U* se déplacerait de ln(ω*·p/UC)/β, qui dépend de n_a.
  - **Écart publié** entre W/(p·pr) et WB/VA sur 12 tours : −0,109 point à π̄ = 2 % et −0,655 point à 10 % (μ = 0,25, remesure C13). Il vient de la variation des stocks valorisée au coût dans la valeur ajoutée. Il croît avec π̄ et ne dépend d'aucune vitesse.
  - La bande du test zéro de ±1 point est commune aux fiches 3 et 4 et porte sur une seule définition. À π̄ = 10 %, l'écart consomme les deux tiers de la bande si celle-ci est centrée sur W/(p·pr) plutôt que sur la valeur résolue de WB/VA. **Laquelle des deux est la valeur centrale de la bande reste à préciser par le mainteneur.**
- **Constat de bouclage.** U* est vertical, fixé par le bloc 3. L'état stationnaire exige que la demande soit cohérente avec y = pr(1 − U^eq)N^pa. Si elle ne l'est pas, π dérive jusqu'à ce que la politique de la fiche 8 ajuste la demande. L'état initial résolu doit donc résoudre une variable de fermeture : le taux réel neutre (fiche 8) ou la position budgétaire (fiche 9). C'est la « fermeture du niveau d'activité » de l'acquis R (faits § 8) et la question ouverte au terme de K (faits § 7).

#### 3.N-7 Stabilité propre (critère 5 (a) et (b))

- **5 (a)** :
  - instabilité 7 : sans objet, faute de produit marginal ;
  - instabilité 15 : voir 3.N-8 ;
  - instabilité 16 : le bloc n'a aucune tolérance ;
  - cliquet G-W : écarté.
  - Les hypothèses réfutées 7, 9 et 10 ne sont pas reprises. La 10 est cohérente avec le terme de niveau de SN (I1c : le niveau porte −0,319 des −0,495 point).
- **5 (b)**, demande et prix exogènes, pas mensuel (C7) :

  | Règle | Valeur propre | Demi-vie |
  |---|---|---|
  | SN, λ_w = 1 | 0,91667 | 7,97 tours |
  | SN, ×0,5 | 0,95833 | 16,29 tours |
  | SN, ×2 | 0,83333 | 3,80 tours |
  | Emploi C et D, λ_N = 2,4 | 0,8 | 3,11 tours |
  | Emploi C et D, ×0,5 | 0,9 | 6,58 tours |
  | Emploi C et D, ×2 | 0,6 | 1,36 tours |
  | SP | 1 | échec |

  La matrice est triangulaire : U ne dépend pas de W à prix exogènes.

#### 3.N-8 Bornes (critère 7, lecture (ii) de #38)

- **Borne unique** : N_t ≤ N^pa_t, contrainte de conservation sans paramètre. Elle est déclarée dans les `\limites`.
  - Inactive à l'état stationnaire, avec une marge de U^eq = 5 points.
  - Mécanisme qui l'en éloigne : à U → 0, la cible salariale monte de βU^eq = 10 %, d'où environ 10 points de hausse salariale par an au-dessus de π^e (λ_w = 1). La transmission passe ensuite par les prix (fiche 4) et la politique monétaire (fiche 8). Le bloc seul n'a pas d'autre rappel.
  - Quand elle est active, N* − N apparaît comme production visée non réalisée (fiche 2).
- **Autres contraintes.** N ≥ 0 découle du plancher y* ≥ 0 du bloc 2. W > 0 découle de la forme logarithmique, sans clip. Sous C, le max est la règle elle-même, sans seuil.
- **Cas à la main** : N* = 1,02·N^pa pendant un tour. Alors N = N^pa, y = pr·N^pa, production visée non réalisée 1,96 %, WB = W·N^pa et U = 0.
- **7 (c), maquette C8** : bloc 2 avec règle d'emploi, sans rétroaction des prix ni de la politique. Durée d'activité de la borne après la fin d'un choc de demande aux tours 1 à 12 :
  - m = 0 : +6 % → 2 tours ; +10 % → 7 tours ; +13 % → 12 tours ;
  - m = 0,6 : +3 % → 5 tours ; +6 % → 17 tours ; +13 % → 56 tours ;
  - aucune réactivation après interruption ; R et C identiques.

  Le seuil de 12 tours dépend donc du rappel prix – politique (fiches 4 et 8). La mesure est à faire au J3 ou au J4, comme prévu.

#### 3.N-9 Masse salariale et rétention (critère 8 ; C10)

- **Pas avec N = 1,02·N*** (W = pr = 1, N* = 100, p = 1,25, v = y = 100, cm = UC) :
  - WB = 102 ; UC·y = 100 ;
  - masse salariale excédentaire = 2, soit 1,961 % de WB ;
  - ΔIN = 0 : l'excédent n'est pas stocké ;
  - résultat courant de 23 contre 25. Les profits non distribués baissent de 2 à dividendes égaux (fiche 6, #36).
- **Pas avec N = 0,98·N*** : y = 98, production visée non réalisée 2 %, WB = 98. Aucun salaire n'est versé pour les emplois non pourvus.

#### 3.N-10 Empreinte et coût (critères 12 et 13)

- Ligne 5 seule ; phases 1 et 4 ; aucun registre propre ; aucun tirage ; aucun drapeau.
- Paramètres : R, 4 (λ_w, β, U^eq, g_N) ; 5 sous (w2) ; C et D, plus λ_N.
- Calcul : environ 25 opérations flottantes plus 2 log et 1 exp, sans itération.
- Maquette R + C (C9) : 1,034 µs par pas, soit 0,215 % de 0,48 ms. Machine de la session cloud (x86_64, 4 cœurs, Python 3.11.15), **qui n'est pas la plateforme de référence de l'ADR 0003**.

#### 3.N-11 Faits et calibration (critères 10 et 15)

Statut : les sources primaires ont été lues le 03/10/2026, en texte intégral (version NBER ou version publiée en accès libre), sauf mention « non lu ». Les pages citées sont celles des versions lues. Un fait établi porte sa source, son échantillon et sa date. Un résultat du modèle n'en porte pas.

| N° | Grandeur | Valeur lue (unité, fréquence, échantillon) | Source exacte | Statut |
|---|---|---|---|---|
| F1 | Coefficient d'Okun, États-Unis | **−0,411** (é.-t. 0,024), R² ajusté 0,817. Unité : points de chômage par % d'écart de production. Annuel, 1948-2011, filtre HP λ = 100. Aucune rupture au test sup-Wald ; −0,35 (1948-1979) contre −0,41 (1980-2011), p = 0,20 | Ball, Leigh et Loungani, NBER WP 18668, § III.A p. 7, tableau 1 p. 24 | établi |
| F2 | Symétrie du coefficient d'Okun | −0,37 (écarts positifs) et −0,39 (écarts négatifs), p = 0,61. Annuel | *idem*, p. 7 | établi, au pas annuel seulement |
| F3 | Retards trimestriels d'Okun | En niveaux, HP 1 600, 1948T2-2011T4 : β0 = −0,245, β1 = −0,133, β2 = −0,116, somme −0,494. Les auteurs parlent de « modest delays in the full adjustment of unemployment to output ». Calcul : part contemporaine 49,6 %, cumul de 76,5 % au trimestre suivant, retard moyen de 0,74 trimestre. Forme : retards distribués **symétriques** | *idem*, p. 6, p. 10, tableau 2 p. 25 | établi |
| F4 | Décomposition de la loi d'Okun | Élasticité de l'emploi à la production γ = **0,543** (0,040). Élasticité du chômage à l'emploi δ = **−0,728** (0,027). β = −0,405. Annuel, 1948-2011, SUR, HP 100. β = γδ n'est pas rejeté (p = 0,38) | *idem*, p. 12, tableau 4 p. 27 | établi |
| F5 | Dispersion entre pays | −0,15 (Japon), −0,45 (États-Unis), −0,85 (Espagne). Moyenne de 20 pays : −0,40. Annuel, 1980-2011 | *idem*, p. 3, p. 15 | établi |
| F6 | Okun original | Okun estimait environ −0,3 en trimestriel, sans retard (1947T2-1960T4), d'où sa règle de 3 % de production par point de chômage. L'écart avec −0,4 ou −0,5 vient de l'absence de retards | *idem*, p. 11-12. Okun (1962) **non lu** : citation de seconde main | établi par BLL |
| F7 | Vitesse d'ajustement de l'emploi, industrie manufacturière | Coefficient de Koyck ρ_T, trimestriel : régression de ln E sur l'indice de production industrielle, 1973-1990. Les crochets donnent les retards médian et moyen, en trimestres. **États-Unis : 0,383** (0,039) [0 ; 0,6], soit 62 % de l'ajustement dans le trimestre. **Allemagne : 0,837** [3 ; 5,1]. **France : 0,935** [10 ; 14,4]. **Belgique : 0,823** [3 ; 4,6]. Dans les quatre pays, les heures s'ajustent bien plus vite que l'emploi. Forme : ajustement partiel **symétrique** | Abraham et Houseman, NBER WP 4390 : § III p. 11-13, § IV p. 14-15, tableau 3A | établi, daté (1973-1990, industrie manufacturière). Biais possible vers un ajustement rapide aux États-Unis : l'indice de production y est construit en partie sur les heures (p. 16) |
| F8 | Ajustement au niveau de l'usine | AR(1) mensuel de l'emploi : 0,474 (7 usines regroupées), 0,361 (agrégées). L'ajustement se fait par sauts : l'emploi ne bouge pas pour de petits chocs et rejoint d'un coup son nouveau niveau pour les grands | Hamermesh, NBER WP 2572, p. 14-16 et tableau 1 | établi pour l'échantillon (une entreprise, 1983-1987), non généralisable |
| F9 | **Asymétrie aux points de retournement**, États-Unis, après-guerre | Emploi mesuré par log(1 − taux de chômage). Ses **pics suivent ceux de la production de 2,25 trimestres** (203 jours). Ses **creux coïncident** avec ceux de la production (0,13 trimestre, 12 jours). Selon les méthodes, le retard au pic va de 1 à 3 trimestres et les creux sont à moins d'un trimestre. Les contractions de l'emploi sont plus brèves et plus violentes : croissance moyenne de +0,18 % en expansion contre −0,39 % en contraction, par trimestre. Les auteurs résument : « employment is a lagging indicator of output cycles only when coming down but not when going up » | McKay et Reis, NBER WP 12400 : résumé, p. 6-8 (résultats 2 et 3), p. 16 | établi (robuste à des centaines de combinaisons de méthodes, selon les auteurs) |
| F10 | Procyclicité de la productivité | Corrélation avec la production ; filtre passe-bande ; secteur privé non agricole, 1948-2015. Productivité horaire : 0,63 (1948-1984) → 0,07 (1985-2015). **Productivité par personne : 0,78 → 0,50**. Corrélation de la productivité horaire avec les heures : 0,23 → −0,43 | Galí et van Rens, *EJ* 131 : tableau 1 p. 306, p. 307-309 | La **baisse** est établie (« highly significant, robust », p. 308). Le **signe actuel est contesté** (« controversial », p. 307). Hors des États-Unis, aucun retournement comparable (p. 309, annexe en ligne B.2 non lue) |
| F11 | Main-d'œuvre quasi fixe | « labor is a quasi-fixed factor » : les entreprises absorbent d'abord les variations de production par les heures et l'effort | Oi (1962) **non lu**. Cité par BLL p. 5 et par Galí et van Rens p. 303 | mécanisme établi, de seconde main |
| F12 | Rétention, histoire du concept | — | Biddle (2014) : **non lu** | non trouvé |
| F13 | Coûts d'ajustement asymétriques | — | Hamermesh et Pfann (1996) : **non lu** | non trouvé |
| F14 | Courbe des salaires (niveau) | Élasticité du salaire réel au taux de chômage local : environ **−0,1** (16 pays dans le livre de 1994, plus de 40 pays ensuite). Méta-analyse : −0,1 sans correction, **−0,07** après correction du biais de publication. Bande du livre : « −0,05 to −0,20 ». États-Unis, panel d'États 1980-2001, annuel : −0,08 ; −0,16 avec instruments ; environ −0,1 pour les spécifications complètes ; −0,07 et −0,12 selon la période | Blanchflower et Oswald, NBER WP 11338 : résumé, p. 1, p. 4 et note 5, p. 11-12, p. 14 | établi |
| F15 | Persistance du salaire régional | Coefficient du salaire retardé, annuel : 0,955 sans effets fixes d'État ; 0,699 avec ; 0,60 (instrumenté, spécification préférée) ; 0,81 et 0,71 | *idem*, p. 11-12, p. 15 | établi pour le panel, dépend de la spécification |
| F16 | Correction d'erreur dans l'équation de salaire agrégée | **États-Unis : coefficient proche de 0**, souvent de mauvais signe, non significatif. **Europe : (1 − μλ) ≈ 0,25** en moyenne. Annuel | Blanchard et Katz, NBER WP 6924, § II p. 5 | établi sur données agrégées. Contesté par F14-F15 sur données micro (Blanchard et Katz p. 6-7 ; Blanchflower et Oswald p. 12) |
| F17 | Pente de Phillips des salaires, États-Unis | Coefficient du chômage dans la hausse trimestrielle des gains horaires, 1964T1-2009T3 : **−0,079** (0,015) (col. 3, indexation sur l'inflation en glissement sur 4 trimestres, de coefficient 0,565). Effet de niveau δ = −(ψ0 + ψ1) : 0,073 (col. 6) à 0,099 (col. 8, échantillon arrêté en 2007T4) | Galí, NBER WP 15758 : p. 17 (éq. 19-20), § 4.2 p. 23-25, tableau 1 | établi pour l'échantillon. Forme réduite d'un modèle NK, indexation inférieure à 1. Hypothèse : unités cohérentes (points de hausse trimestrielle par point de chômage) |
| F18 | Part salariale | 0,52 | Penn World Table (fiche 2, extrait) | non relu ici |

**Conversions.**
- Convention du § 3.C : le facteur par tour vaut 1 − λ_N/12 ; un coefficient trimestriel ρ_T devient ρ_T^{1/3} par mois.
- Commande : `uv run --no-project python conv.py`.

| Source | Coefficient lu | Persistance par tour | Demi-vie (tours) | λ_N équivalent (par an) |
|---|---|---|---|---|
| F7, États-Unis | ρ_T = 0,383 | 0,7262 | **2,17** | 3,29 |
| F7, Allemagne | 0,837 | 0,9424 | 11,69 | 0,69 |
| F7, France | 0,935 | 0,9778 | 30,94 | 0,27 |
| F7, Belgique | 0,823 | 0,9371 | 10,67 | 0,75 |
| F3, ajustement partiel mensuel qui reproduit la part du trimestre 0 (49,6 %) | — | 0,6946 | **1,90** | 3,66 |
| F8, usines regroupées (agrégées) | ρ_M = 0,474 (0,361) | — | 0,93 (0,68) | 6,31 (7,67) |
| Seuils de `jeu` et calibration | λ_N = 3,51 ; 2,48 ; 2,40 ; 1,91 | — | 2,00 ; 2,99 ; 3,11 ; 4,00 | — |

- Contrôle de l'ajustement mensuel calé sur F3 : il donne un cumul de 0,831 au trimestre suivant, contre 0,765 dans BLL. Une forme géométrique n'épouse donc qu'approximativement les retards distribués de BLL.
- Salaires :
  - F15 : correction annuelle 1 − ρ de 0,19 à 0,40, soit λ_w linéaire de 0,21 à 0,50 par an ;
  - F16, Europe : correction de 0,25, soit λ_w = 0,284 ;
  - SN avec λ_w = 1 : correction annuelle 1 − (11/12)^12 = **0,648** ;
  - F17 : 4 × δ = **0,29 à 0,40** point de hausse salariale annuelle par point de chômage. La pente d'impact de SN vaut λ_w·β = **2,0**.

**Ce que le modèle produit, confronté aux faits.** Ce sont des résultats du modèle, non sourcés.
- **Okun**, R et C : dU/d ln y = −(1 − U*) = −0,95, contre −0,41 (F1).
  - Décomposition (F4) : γ = 1 contre 0,54, δ = −0,95 contre −0,73.
  - C ne modifie γ que pendant quelques tours (N = N* hors transitoire). La limite déclarée subsiste. Elle tient à la fois à l'absence de marge d'heures ou d'effort (γ) et à la population active exogène (δ).
- **Retard moyen** : nul sous R ; demi-vie de 3,11 tours sous C avec λ_N = 2,4, en baisse seulement. Faits : 1,9 à 2,2 tours aux États-Unis (F3, F7) ; 10,7 à 30,9 tours en Allemagne, en Belgique et en France (F7).
- **Points de retournement**, mesurés par `uv run --no-project python points.py` (N* sinusoïdal, amplitude 2 %, g = 0) :

  | Règle | Retard au pic | Retard au creux |
  |---|---|---|
  | R | 0 | 0 |
  | C, demi-vie 2 tours | 0 | 2 tours |
  | C, demi-vie 3 tours | 0 | 3 tours (période 36) ; 4 tours (périodes 60 et 96) |
  | C, demi-vie 4 tours | 0 | 4 à 5 tours |
  | Faits (F9) | 3 à 9 tours | moins de 3 tours (0,4 tour en moyenne) |

  - Sous C, quand N*_t < N_{t−1}, N_t < N_{t−1} : l'emploi baisse dès le premier tour de recul. C ne peut donc **jamais** retarder un pic. Elle retarde en revanche les creux, ce qui est l'**asymétrie inverse** de F9.
  - Reproduire le retard au pic exige N < N* en fin d'expansion, donc une marge d'heures. La technique de M24 ne la permet pas sans pénurie : c'est le défaut de D.
- **Productivité par personne** : acyclique sous R. Sous C, elle baisse en récession et ne dépasse jamais sa tendance. Fait : procyclique, à 0,50 après 1985 (F10).
- **Salaires** :
  - β = 0,1/U* = **2,0** est conforme à F14 (1,4 avec l'élasticité corrigée de −0,07).
  - λ_w = 1 donne une correction annuelle de 0,648. Les faits donnent 0,19 à 0,40 (F15), 0,25 (F16, Europe) et environ 0 (F16, États-Unis agrégés).
  - La pente d'impact λ_w·β = 2 points par an vaut **5 à 7 fois** les 0,29 à 0,40 de F17.
  - L'excès vient de λ_w, non de β. Avec λ_w = 0,284 : pente de 0,57 et demi-vie de SN de 28,9 tours, contre 7,97 tours aujourd'hui.

#### 3.N-12 Verdict sur le critère 10 (b), option C (additif du 03/10/2026, sources lues)

**Le retard d'emploi est soutenu par des faits établis quant à son existence et à son ordre de grandeur. Sa forme asymétrique ne l'est pas.**

- **Établi** :
  - l'emploi suit la production avec retard (F3, F7) ;
  - les entreprises absorbent d'abord par les heures et l'effort (F7, F11) ;
  - la productivité par personne est procyclique (F10).

  C représente la moitié « baisse » de ces faits.
- **Non établi** : « embauche immédiate, débauche lente ».
  - Les ajustements mesurés sont symétriques (F3, F7). F2 ne trouve aucune asymétrie au pas annuel.
  - La seule asymétrie établie (F9) va dans l'autre sens aux points de retournement : retard aux pics, coïncidence aux creux.
  - Le récit de C « la reprise est là, mais le chômage monte encore » (§ 7.C) est donc un **produit de la règle**, non un fait. Aux États-Unis, les creux du chômage et de la production coïncident en moyenne (0,13 trimestre). BLL (§ IV) attribuent les « reprises sans emplois » à une croissance lente, non à un retard d'emploi.
- **Demi-vie impliquée** : de **1,9 à 2,2 tours** aux États-Unis.
  - Elle se place à la borne basse du seuil de 2 à 4 tours de `jeu`. Le calage sur F3 (1,90) est même juste en dessous.
  - λ_N = 2,4 (3,11 tours) est plus lent que les faits américains, mais reste dans la fourchette de `jeu`.
  - Avec 3 tours ou plus, le retard au creux atteint 3 à 4 tours. Il sort alors de la fourchette de F9 (« à moins d'un trimestre »).
  - Les valeurs européennes (10,7 à 30,9 tours) sont très au-delà de la borne haute de 4 tours, que `jeu` a fixée pour limiter le gain de la demande pulsée.

**Deux lectures du critère 10 (b).** C'est la formulation du critère qui est en cause, non un manque de documentation. Le mainteneur tranche.
- **(i)** Le critère exige qu'un retard d'emploi soit établi et que son ordre de grandeur soit sourcé. **C le satisfait**, à condition de déclarer la forme asymétrique comme une approximation imposée par la technique de M24, avec son écart à F9, et de caler λ_N sur environ 2 tours.
- **(ii)** Le critère exige que la règle elle-même soit soutenue, asymétrie comprise. **C ne le satisfait pas**, et R prévaut.

Mon avis : la lecture (i) est la plus fidèle au texte adopté (« un retard d'emploi n'est retenu que s'il est soutenu par un fait établi et sourcé »). Sur les faits, C, avec une demi-vie de 2 tours, est mieux placée que R :
- en faveur de C : le retard moyen (F3, F7) et la productivité par personne (F10). R est contredite sur ces deux points ;
- en faveur de R : les creux (F9), mais C n'en est qu'à 2 tours, ce qui reste à moins d'un trimestre ;
- échec commun : le retard au pic (F9) et le coefficient d'Okun (F1).

La branche « mécanisme perçu » est remplie selon `jeu` pour les chocs d'un point de demande ou plus, y compris à 2 tours (§ 7 : chômage de +0,48 point au tour 4 contre +0,97 sous R ; pic de +2,38 contre +2,75).

### 3.R Option R — référence sans retard : N = min{N*, N^pa}, salaire SN

1. **Équations** : T1, T2, T3-SN, et T4-R : N_t = min{N*_t, N^pa_t}. Puis U_t = 1 − N_t/N^pa_t et WB_t = W_t·N_t.
2. **Boucle combinée** (C4) : c'est celle de la fiche 2. Valeurs à g = 2 %, calibration :

   | m | Rayon spectral | Période |
   |---|---|---|
   | 0,5 | 0,9279 | 68,9 tours |
   | 0,6 | 0,9452 | 72,9 tours |
   | 0,7 | 0,9612 | 80,7 tours |
   | 0,8 | 0,9762 | 95,8 tours (95,9 à g = 0) |

   - Toutes les périodes sont dans la bande de 36 à 96 tours. **Marge de 0,1 à 0,2 tour à m = 0,8.**
   - Vitesses ×0,5 : 141,8 à 184,5 tours (publiées). ×2 : 34,3 à 52,2 tours.
   - Rayon spectral < 1 partout.
3. **Délais** : demande → production et emploi, 1 tour (fiche 2) ; chômage → salaire, 1 tour ; contrepartie au tour du choc : stocks.
4. **Défauts.** Productivité apparente toujours égale à la tendance : la restitution de la rétention est sans objet. Coefficient d'Okun de −0,95, contemporain.

### 3.C Option C — rétention asymétrique avec terme de tendance (nouvelle), salaire SN

1. **Règle (T4-C)** : N_t = min{N^pa_t, max{N*_t, (1 + g_N/n_a)(1 − λ_N/n_a)N_{t−1} + (λ_N/n_a)N*_t}}.
   - L'entreprise embauche sans délai ce que son plan exige. Elle ne réduit un effectif excédentaire qu'à la vitesse λ_N.
   - Statut : approchée. Provenance : retard de l'emploi sur la production (BLL, tableau 2 ; Abraham et Houseman, tableau 3A) et main-d'œuvre quasi fixe (Oi, 1962, cité par BLL p. 5). **La forme asymétrique est un choix imposé par la technique de M24**, sans marge d'heures. Elle n'est pas établie, et elle est inverse de McKay et Reis (2006) aux points de retournement : aucun retard au pic, retard de 2 tours au creux à demi-vie de 2 tours. À déclarer dans les `\limites`.
2. **État stationnaire** : N = N* exactement, quel que soit λ_N, puisque N_{t−1} = N*_t/(1 + g_N/n_a) sur la trajectoire de référence.
3. **Production** : y = min{y*, pr·N} = y* dans les deux régimes, puisque N ≥ N*. **La production est identique à celle de R** (C5 : impulsions de ±1 %, mêmes écarts que R à 1e−16 près). Le retard n'affecte que N, U, WB et les profits. La boucle combinée est celle de R, plus la valeur propre découplée 1 − λ_N/n_a = 0,8 en régime de baisse. Bande respectée, comme R.
4. **Demi-vie de l'écart d'emploi** : ln 2/(−ln(1 − λ_N/n_a)) = **3,11 tours** à λ_N = 2,4 ; 6,58 tours à ×0,5 ; 1,36 tour à ×2.
   - Correspondance demi-vie → λ_N : 2 tours → 3,51 ; 3 tours → 2,48 ; 6 tours → 1,31 par an.
   - Faits : demi-vie de 1,9 tour (BLL, tableau 2, calage mensuel) à 2,2 tours (Abraham et Houseman, États-Unis, 1973-1990) ; 10,7 à 30,9 tours en Belgique, en Allemagne et en France. Calibration proposée : **λ_N = 3,5 par an**, soit une demi-vie de **2,01 tours**. Aux vitesses ×0,5 et ×2 : 4,40 et 0,79 tour (publiées).
5. **Productivité apparente** : elle est inférieure ou égale à 1. Elle baisse dans les récessions, et elle ne peut dépasser la tendance dans les reprises (Leontief). La procyclicité n'est donc représentée qu'à moitié, alors qu'elle est contestée.

### 3.D Option D — ajustement partiel symétrique avec terme de tendance (nouvelle), salaire SN

1. **Règle (T4-D)** : N_t = min{N^pa_t, (1 + g_N/n_a)(1 − λ_N/n_a)N_{t−1} + (λ_N/n_a)N*_t}. État stationnaire exact (N = N*).
2. **En hausse**, N < N* : la production est contrainte, y = pr·N < y*. C'est une boucle du second ordre (C4, g = 2 %, λ_N = 2,4) :

   | m | Rayon spectral | Période |
   |---|---|---|
   | 0,5 | 0,9627 | 75,9 tours |
   | 0,6 | 0,9717 | 85,1 tours |
   | 0,7 | 0,9800 | **98,6 tours** |
   | 0,8 | 0,9878 | **121,2 tours** |

   **Hors de la bande pour m ≥ 0,7.** La bande à m = 0,8 n'est atteinte qu'à **λ_N ≥ 11,69 par an** (11,91 à g = 0), c'est-à-dire sans retard. Elle l'est à m = 0,7 dès λ_N ≥ 2,70 (C5).
3. **Verdict** : échec du critère 5 (c) à la calibration proposée, dont les vitesses de la fiche 2 sont indicatives. D produit en outre une pénurie en reprise malgré 5 % de chômage, ce qui est l'opposé de la productivité procyclique. Les impulsions non linéaires convergent (C5).

### 3.L Restitution et exemple daté (critère 11)

**Exemple** (C6, script corrigé `t6_exemple_corrige.py`) : même choc que la fiche 2. Dépense publique +1 % aux tours 1 à 12, part de G 20 % (hypothèse), demande +0,2 %, demande exogène, g = 0, U* = 5 %, λ_w = 1, β = 2, λ_N = 2,4. La production reproduit exactement la fiche 2 (M5). Écarts au sentier :

| Tour | Production % | Emploi R % | Emploi C % | U (R), points | U (C), points | (y/N)/pr − 1 (C) % | W (R), H-p1 % | W (R), H-p2 % | W (C), H-p1 % |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0,000 | 0,000 | 0,000 | 0,000 | 0,000 | 0,000 | 0,000 | 0,000 | 0,000 |
| 2 | +0,084 | +0,084 | +0,084 | −0,080 | −0,080 | 0,000 | 0,000 | 0,000 | 0,000 |
| 3 | +0,142 | +0,142 | +0,142 | −0,135 | −0,135 | 0,000 | +0,013 | +0,013 | +0,013 |
| 4 | +0,183 | +0,183 | +0,183 | −0,174 | −0,174 | 0,000 | +0,035 | +0,036 | +0,035 |
| 9 | +0,246 | +0,246 | +0,246 | −0,233 | −0,233 | 0,000 | +0,172 | +0,210 | +0,172 |
| 13 | +0,239 | +0,239 | +0,244 | −0,228 | −0,232 | −0,004 | +0,258 | +0,365 | +0,258 |
| 14 | +0,153 | +0,153 | +0,226 | −0,145 | −0,214 | −0,073 | +0,274 | +0,403 | +0,275 |
| 18 | −0,003 | −0,003 | +0,110 | +0,003 | −0,105 | −0,113 | +0,234 | +0,452 | +0,295 |
| 24 | −0,030 | −0,030 | +0,008 | +0,029 | −0,008 | −0,038 | +0,121 | +0,431 | +0,216 |

- **H-p1** : prix sur leur sentier, donc le salaire réel varie et l'écart se referme, avec une demi-vie de 7,97 tours (§ 3.N-7). **H-p2** : marge instantanée, donc W/P est constant et le niveau nominal se déplace durablement. C'est une racine unité nominale, qui relève de la fiche 8.
- **Choc de −1 %, option C** : emploi −0,017 % au tour 2 contre −0,084 % de production ; productivité apparente −0,067 % ; U +0,016 point contre +0,080 sous R. Au tour 9 : −0,182 %, U +0,173 point. Le salaire de C (H-p1) est à −0,090 % au tour 9 et −0,175 % au tour 13, contre −0,172 % et −0,258 % sous R.

**Délais en tours entiers** (R ; C identique en hausse) :
- dépense publique → stocks au tour n, production et emploi au tour n + 1, salaire au tour n + 2 ;
- impôts des ménages → ventes au tour n + 1, emploi au tour n + 2, salaire au tour n + 3 ;
- anticipation → salaire au tour n + 1 sous la lecture (a), au tour n sous la lecture (b) ;
- salaire → prix : fiche 4.

**Indicateurs au tour** :
- U (au tour, et moyenne sur 12 tours) et N ;
- W (glissement sur 12 tours) ; W/P ;
- part salariale, mesure restituée ΣWB/ΣVA sur 12 tours, publiée avec la variable des règles W/(p·pr) et leur écart stationnaire ;
- sous C seulement : (y/N)/pr et masse salariale excédentaire en fraction de WB ;
- niveaux normaux : U^eq, ω̄, glissement salarial stationnaire (4,0588 % à π̄ = 2 %).

Aucun levier propre (Q7 renvoyé au J4). Interface notée : un levier institutionnel entrerait par ω* ou U^eq (lecture (w2)) plutôt que par une borne W ≥ W^min.

### Statut des faits de la première tentative (critère 16)

| Fait | Statut |
|---|---|
| G-W : forme active, cliquet | O |
| H0 : u_n à 5,125 %, aucune borne salariale | S+O |
| I1c : transmission salariale | O |
| G1 : chômage final 5,185 % | S+O |
| D1 sur 60 ans : chômage 5,18 %, dérive de la part salariale 0,147 point | R |
| Instabilités 7 et 15 | R |
| Instabilité 16 | S+O |
| Réfutée 7 | R, complétée O |
| Réfutée 10 | O |
| Acquis WS-PS et « emploi au profit nul » | R |
| « λ_w = 2 instable » (`model.py` l. 138) | L (commentaire), contenu non mesuré |
| Lignes de la v2.0 citées | L, vérifiées le 03/10/2026 |
| Résultats chiffrés de la v1.5 (l. 619, 731, 2397) | rapportés par la v1.5, invérifiables |

Aucun fait D1 n'a été remesuré.

## 4. Tableau comparatif

| Critère | A (v1.5) | B (v2.0) | R (sans retard) | C (rétention asymétrique) | D (ajustement symétrique) |
|---|---|---|---|---|---|
| 1 Matrices | ligne 5 ; τ_S vers la ligne 7 (fiche 9) | ligne 5 ; τ_S ; emploi public | ligne 5 seule | idem R | idem R |
| 2 Phases et M24 | **révise M24** (produit marginal) | **révise M24** ; lit prix et trésorerie | conforme ; Q4 confirmée | conforme | conforme |
| 3 Forme fermée | partielle ; unités du salaire ambiguës | non (N/N* et stock dépendent de λ) | oui : U* = U^eq, N = N*, ω̄ = 1/(1+μ̄) | oui | oui |
| 3 (b) n_a | — | — | lecture commune (L) : salaire réel 2,0151 / 2,0184 / 2,0197 % ; (G) : exactement g_pr | idem | idem |
| 4 Vitesses | **non** : λ_L = 13 > n_a ; terme φ_v v | **non** : stock −1,12 % (g_N = 0,5 %) | oui sous (G), ou sous (L) avec une anticipation en taux linéaire ; échec sous (L) avec une anticipation en glissement (2,7e−3) | idem R | idem R |
| 5 (a) | cliquet G-W | instabilité 7, cliquet | rien de réintroduit | idem | idem |
| 5 (b) | −0,083 ; ×2 : −1,167 ; salaire = 1 : **échec** | < 1 (u_n 0,99667) | 0,9167 | 0,9167 et 0,8 | idem C |
| 5 (c) bande | sans objet (λ > n_a) | pas d'état exact | 68,9 à 95,8 tours, dans la bande | idem R ; demi-vie 3,1 tours | **98,6 et 121,2 tours : échec** |
| 6 Préalable | non | non | oui | oui | oui |
| 7 Bornes | 9 | environ 13 (dont 0,98 à seuil libre) | 1 (conservation) | 1 | 1 |
| 8 Rétention | N/N* = 1,000032 à l'état stationnaire | N < N* à l'état stationnaire | nulle | transitoire, nulle à l'état stationnaire | transitoire, plus pénurie en reprise |
| 9 Inflation | π^ref avec max ; ω_u | idx_u·max ; incomplète (≈ 0,9992) | coefficient 1, vertical | idem | idem |
| 10 Retard | sans tendance | sans tendance | retard nul, contredit par F3 et F7 ; creux conformes à F9 | retard établi (demi-vie de 1,9 à 2,2 tours) ; forme asymétrique non établie, inverse de F9 aux pics et aux creux | forme symétrique comme F7, mais pénurie (échec du critère 5 (c)) |
| 11 Lisibilité | — | — | U, W, W/P, part salariale | plus productivité apparente et excédent | plus pénurie en reprise |
| 12 Empreinte | environ 13 paramètres ; 4 variables d'état | environ 15 paramètres ; 6 variables d'état (3 cachées) ; 4 drapeaux | 4 paramètres ; 3 variables d'état | 5 ; 4 | 5 ; 4 |
| 13 Coût | puissances, sans itération (non mesuré) | idem (non mesuré) | 1,03 µs par pas (maquette) | idem | idem |
| 14 Notation | collisions u, L | idem | libre (C12) | libre | libre |

## 5. Avis de l'expert pilote

*`macro`, 03/10/2026.*

**Recommandation : option R** (N = min{N*, N^pa}, salaire SN), avec les lectures suivantes.
- (a) Q3 : anticipation lue à l'ouverture, sous réserve de l'avis de `monnaie`.
- (b) **Lecture commune des taux annuels (Q4, #24 ; fiches 3, 4 et 8)** : (G), géométrique, avec révision de M24 (f) et décision citant M22 et M24. À défaut, (L) avec une anticipation en taux linéaire annualisé (engagement de la fiche 8) et une transposition prospective du critère 9 (a). Choix du mainteneur à M25-M26.
- (c) Norme ω* = 1/(1 + μ̄), lecture (w1). La lecture (w2) est renvoyée au J4 avec le levier institutionnel.
- (d) Population active en tendance exogène, propriétaire le bloc 3.
- (e) Q4 de la fiche 2 confirmée.
- (f) Aucun levier propre.

**Motifs.**
- Aucune vitesse ni la durée du pas n'entre dans l'état d'arrivée.
- Une seule borne, de conservation.
- Une ancre réelle (le niveau) et une pente de long terme verticale.
- Le minimum de paramètres.
- (Motif remplacé par l'additif du 03/10/2026 : voir ci-dessous, « La recommandation dépend de la lecture du critère 10 (b) ».)

*Additif du 03/10/2026 (sources primaires lues, § 3.N-11 et § 3.N-12) :*

**La recommandation dépend de la lecture du critère 10 (b), que tranche le mainteneur.**
- **Lecture (i)** : je recommande **C**, salaire SN, avec **λ_N = 3,5 par an** (demi-vie de 2,01 tours), et les lectures (a) à (f) inchangées. Le retard est établi. C ne change pas la production, de sorte que la bande du critère 5 (c) et l'état stationnaire restent ceux de R. Le retard est perçu (`jeu`, § 7), et la demi-vie de 2 tours minimise le gain de la demande pulsée mesuré par `jeu`.
- **Lecture (ii)** : **R** reste imposée.

**Écartées.**
- D : échec du critère 5 (c), exigence.
- A et B : révision de M24, critères 4 et 5 (b) (A), bornes, état caché et drapeaux (B).
- SP : critère 5 (b).

**Réserves, avec seuils écrits avant l'essai.**
1. Bouclage du niveau d'activité : constat transmis aux fiches 8 et 9 et au script d'état stationnaire.
2. Critère 5 (d), boucle salaires – prix : à mesurer avec la fiche 4. Le rapport « λ_w = 2 instable » de la v2.0 reste à instruire (remesure T1).
3. Condition 3 (d) sur W/(p·pr) ; écart publié de −0,109 et −0,655 point avec WB/VA ; valeur centrale de la bande commune à préciser.
4. Coefficient d'Okun de −0,95 : limite déclarée.
5. Bande à m = 0,8 tenue à 0,1 ou 0,2 tour près : toute recalibration de la fiche 2 au J3 la revérifie.
6. Critère 7 (c) mesuré au J3 ou au J4. La maquette dépasse 12 tours sans rétroaction des prix.
7. **λ_w = 1 est hors des ordres de grandeur sourcés** (correction annuelle de 0,648 contre 0,19 à 0,40 ; pente d'impact de 2 contre 0,29 à 0,40). β = 2 est conforme. Recalibration de λ_w au J3, avec le critère 5 (d) et la remesure T1. Sujet frontière avec `monnaie` (indexation inférieure à 1 dans F17).
8. **Archétypes** : la vitesse d'ajustement de l'emploi varie d'un facteur 14 entre pays (F7), et le coefficient d'Okun d'un facteur 5 (F5). Calibrer un archétype « continental » sortirait du seuil de 2 à 4 tours de `jeu` et amplifierait la demande pulsée. Question pour J5, à soumettre à `jeu` et au mainteneur.
9. **Sous C**, la restitution et la spécification ne présentent pas comme un fait « le chômage monte encore pendant la reprise ». L'écart à F9 est déclaré dans les `\limites`.

## 6. Avis de l'expert consulté

*Rédigé par `monnaie` (expert consulté, frontière inflation), le 03/10/2026, sur la fiche à l'état `e7873e6` (branche `claude/j1-economie-reelle`, PR #43). La question 3 est traitée dans sa version remplacée du 03/10/2026 : une seule lecture des taux annuels pour les fiches 3, 4 et 8, la forme mixte du § 3.N-4 étant exclue. Sources lues : fiche 4 § 1 et § 2 ; issue #24 ; `sec:cadre-calendrier` (l. 174 à 215) ; `CONVENTIONS.md` § 5.2 et § 6 ; `archive/faits_mesures_G_K.md` § 3, 4, 6 à 8 ; `archive/v2.0/prototype/model.py` l. 224 à 229, 289 à 300, 1289 à 1310, 1364 à 1375 ; `archive/v2.0/prototype/policies.py` l. 54 à 71. Lectures du code : statut L, vérifiées le 03/10/2026.*

### 6.1 Réponses aux questions de `macro`

**Q1 — Variable consommée.** La définition du § 3.N-3 me convient : π^e_t est le glissement annuel anticipé de P sur les 12 tours à venir, en fraction par an, avec la valeur stationnaire requise π̄ (sous la lecture (G), voir Q3). Mais l'égalité π^e = π̄ à l'état stationnaire **n'est pas automatique sous une règle de crédibilité**. C'est une condition que la fiche 8 doit remplir.
- Contre-exemple, la loi de la v2.0 (`model.py` l. 1300, L) : π^e += [λ(π − π^e) + cred·(π* − π^e) + ups·(g_M − g_Y − π^e)]/13. Dès que cred > 0 et π̄ ≠ π*, sa valeur stationnaire est une moyenne pondérée de π̄ et de π*, donc différente de π̄.
- Conséquence sous SN, lecture (w1), marge à sa norme : λ_w·β·(U − U^eq) = ln(1 + π^e) − ln(1 + π̄). Une erreur d'anticipation permanente déplace le chômage stationnaire, et ce déplacement dépend de λ_w, ce qui fait **échouer le critère 4**. Exemple calculé (commande au Retour), avec la loi de la v2.0, π̄ = 3 %, π* = 2 %, λ = 0,2, cred = 0,8, d'où π^e = 2,200 % : U − U^eq = −0,780, −0,390 et −0,195 point pour λ_w = 0,5, 1 et 2.
- **Condition transmise à la fiche 8 (C1)** : aucune erreur d'anticipation à l'état stationnaire, π^e = π̄ dans tout état stationnaire. Deux voies la remplissent :
  - une loi d'apprentissage pure, comme l'apprentissage à gain constant d'Evans et Honkapohja (2001), cité de mémoire : dans un état stationnaire déterministe, l'estimateur de la moyenne converge vers π̄ ;
  - un terme d'ancrage vers π* combiné à une règle de taux qui garantit π̄ = π* dans tout état stationnaire (Q5) : l'ancrage agit alors en transition et s'annule à l'arrivée.

  La crédibilité reste donc possible comme mécanisme de jeu, à condition de ne pas créer d'erreur stationnaire.

**Q2 — Lecture de π^e (Q3 de la fiche).** Je recommande la **lecture (a), à l'ouverture**, comme `macro`. Trois motifs :
1. **Calendrier de Barro et Gordon (1983)** : les anticipations sont fixées avant la décision de politique de la période. C'est ce calendrier qui donne un sens à l'opposition entre surprise et annonce, et au biais d'inflation (lecture de mémoire ; existence de l'article vérifiée, contenu non relu). Sous (a), une décision du joueur au tour n ne peut pas être déjà intégrée dans les salaires du tour n.
2. **Découplage de la phase 1.** Sous (a), la position du bloc 8 dans la phase 1 ne contraint pas le bloc 3. La Q1 de la fiche 4 reste ouverte. Si elle retient P_t ≡ p_t avec p_t en phase 1 (lecture (b) de la fiche 4), le bloc 8 doit venir après le bloc prix pour lire π_t. L'ordre « travail, prix, banque centrale » reste alors triangulaire, ce que la lecture (b) de la Q3 aurait interdit.
3. **Aucun mécanisme d'annonce n'exige une transmission aux salaires dans le tour même.** Le délai d'un tour (un mois) est court devant la durée d'un contrat salarial. Une annonce faite au tour n peut afficher dès ce tour l'anticipation π^e_{n+1} qu'elle produit, la contrepartie visible étant l'anticipation elle-même. Les salaires réagissent au tour n + 1.

Le bloc 8 ne lit W_t en aucun cas : d'accord. Sous (a), la question ne se pose même pas.

À noter pour la fiche 8 : sous (a), π^e est une variable d'état d'ouverture du bloc 8. La phase où elle est formée (phase 1 après les leviers du tour n − 1, ou phase 9 après le prix du tour n − 1) relève de la fiche 8. Le délai prix → anticipation → salaire dépend aussi de la Q1 de la fiche 4 : jusqu'à 2 tours sous P_t ≡ p_{t−1}.

**Q3 (remplacée) — Lecture commune des taux annuels.** Je préfère **(G)**, comme `macro`. Le motif monétaire est décisif à mes yeux. Sous (G), les trois grandeurs d'inflation que le joueur lit et que la règle compare (glissement mesuré π_t, anticipation π^e, cible π*) sont **sur la même échelle, sans aucune conversion dans le bloc 8**. La cible se compare directement au glissement : c'est la lecture (ii) de #24, et aucune conversion de la cible n'est nécessaire, sauf pour une règle qui lirait une inflation par pas. C'est aussi la pratique des banques centrales :
- Réserve fédérale : « 2 percent, as measured by the annual change in the price index for personal consumption expenditures » (déclaration de 2012, réaffirmée ; formulation vérifiée par extrait de recherche, document non lu) ;
- BCE : cible symétrique de 2 % à moyen terme sur l'IPCH (stratégie du 08/07/2021, extrait de recherche) ; la formulation en glissement annuel est citée de mémoire.

Sous (L), réponse à la question posée : oui, la loi de la fiche 8 peut produire un taux linéaire annualisé, mais par l'une de deux voies, toutes deux coûteuses.
- **Apprendre sur n_a[(1 + π_t)^{1/n_a} − 1].** Il faut alors une conversion géométrique du glissement, qui est « mesuré, jamais converti » (`sec:cadre-calendrier`). (L) ne supprime donc pas la formule géométrique : il la déplace dans le bloc 8.
- **Apprendre sur la variation mensuelle annualisée n_a(P_t/P_{t−1} − 1).** Cette mesure est bruitée dès J ≥ 2 ou en présence de chocs.

Dans les deux cas, le joueur voit deux inflations. Et toute loi de crédibilité qui compare le glissement à une cible linéaire pénalise un écart permanent : 2,0184 % contre 2 % ; 10,4713 % contre 10 % pour une cible de 10 % (n_a = 12), soit 0,47 point, que la règle K1a de la v2.0 aurait sanctionné indéfiniment. Valeurs de π^e sous (L), commande au Retour : 1,9852 %, 1,9819 % et 1,9806 % pour π̄ = 2 % à n_a = 4, 12 et 52.

**Coût de (G), à déclarer.** Les taux d'intérêt, les flux et les vitesses restent linéaires (M22 (a) inchangée). Un ratio stationnaire qui combine un taux linéaire et une croissance géométrique dépend alors légèrement de n_a. Exemple : K/I = 1/(n_a[(1 + g)^{1/n_a} − 1] + δ) vaut 14,3160, 14,3228 et 14,3253 à n_a = 4, 12 et 52 (g = 2 %, δ = 5 %), contre 14,2857 sous (L). Conséquences :
- la phrase de `sec:cadre-calendrier` « un ratio stationnaire […] ne dépend pas de n_a pourvu que les taux de croissance soient […] linéaire[s] » devient fausse ;
- « C'est la seule conversion du moteur » aussi ;
- `CONVENTIONS.md` § 5.2 et § 6 sont touchés ;
- les formes de la fiche 2 (ρ̄_IN, ρ̄_K = 0,7791) sont à recalculer par `macro`.

Il faut donc une décision citant M22 et M24 (f), comme le dit `macro`, avec une annotation de l'ADR 0005 par `architect`. Comme n_a est fixé à 12 par M22, cette dépendance est déclarée et non une dérive.

**Suggestion de mise en œuvre** (non tranchée) : porter les taux de croissance et d'inflation en logarithme, ℓ = ln(1 + x). La conversion géométrique devient alors linéaire, ℓ/n_a par pas, et la condition de domaine π^e > −1 est satisfaite par construction. La règle SN est déjà écrite ainsi.

**Q4 — Indexation.** D'accord avec une indexation complète sur π^e, sans max(π^e, π) (le cliquet G-W, O, est écarté) et sans inflation passée.
- Si la fiche 8 retient une loi adaptative, l'inflation passée entre déjà par π^e. Une indexation directe sur π_{t−1} compterait deux fois la persistance.
- Le coefficient 1 donne la verticalité de long terme. Avec C1, il garantit que la politique monétaire agit sur π̄ et non sur U*, conformément à l'intention du mainteneur, « une création monétaire durable se traduit par une inflation durable ».
- **Double compte avec la Q6 de la fiche 4**, à préciser. Si le prix est une marge sur UC_t du même tour, le coût contient déjà le salaire indexé. Une indexation supplémentaire du prix sur π^e ajouterait π^e une seconde fois à la hausse du prix au tour du choc : gain de 2 sur π^e à l'impact, et marge stationnaire fonction de λ_p et de π̄ (échec du critère 4 (a) de la fiche 4). Règle proposée à la fiche 4 : le coefficient de π^e dans le prix est celui qui rend p/UC indépendant de π̄. Il vaut 0 sur une base de coût courante et 1 sur une base retardée d'un pas (UC_{t−1}), où il **remplace** le facteur (1 + π̄)^{1/n_a} du critère 3 (c) au lieu de s'ajouter.
- Même vigilance pour une vitesse modulée par π^e (v2.0, `flex`, l. 1090) : elle ne doit pas apparaître dans les formes stationnaires.
- Pour le J4 (levier « indexation légale ») : une indexation mêlant π^e et l'inflation passée reste verticale si la somme des coefficients vaut 1 et si C1 tient.

**Q5 — Bouclage.** La piste de `macro` est la bonne, et l'algèbre est exacte sous la forme du cadre r = i − π. Avec la règle i = r* + π^e + a_π(π − π*) + terme d'activité, à l'état stationnaire π^e = π̄ et U = U^eq. Le taux réel requis par la fermeture de la demande, r̄ (fiches 5, 6 et 9), impose alors :

  **π̄ − π* = (r̄ − r*)/a_π**, exactement (non une approximation).

La forme de Taylor (1993), i = π + r* + 0,5(π − π*) + 0,5·écart de production, donne le même biais avec a_π = 0,5, donc doublé (dérivation de l'auteur ; la forme de la règle est citée de mémoire, l'existence de l'article est vérifiée). Un a_π fort réduit le biais sans l'annuler.

**Lecture des faits de la première tentative.** Elle est compatible avec cette piste, sans l'établir.
- G-T (S+O) : r* estimé 2,417 ; anticipation 4,007 ; contribution d'inflation 2,953 = 1,5 × 1,969 point d'écart ; activité −0,153. Le taux réel exigé vaut donc 9,225 − 4,007 = 5,218 %, soit le « taux réel directeur à 5 % » de la v2.0.
- J1a (S+O) : biais de 1,965 et 1,989 point pour des cibles de 3 % et 2 %. Le biais ne dépend pas de la cible, comme le prédit la formule.
- K1 et K1a (S+O, L) : une crédibilité fixée à 1 ne referme pas l'écart. C'est cohérent avec un biais stationnaire indépendant de l'ancrage des anticipations.
- Mécanisme lu (L), `policies.py` l. 62 : en mode `anchored`, l'estimateur de r* rappelle vers l'ancre (`rstar_reversion` = 1 par an, l. 293) et intègre l'écart d'inflation (`lam_rstar` = 0,02 par décision, l. 289), dans une bande de ±1 point (l. 292). C'est un **intégrateur à fuite**. À l'état stationnaire, r* − ancre = k·écart, avec k = 0,02/(1 − e^{−1/13}) = 0,270, et π̄ − π* = (r̄ − ancre)/(a_π + k).
  - Prévu, aux valeurs par défaut : r* − ancre = 0,53 point ; écart = 1,91 point. Observé : 0,42 point et 1,97 point. L'ordre de grandeur est compatible ; l'écart n'est pas expliqué (valeurs de D1 non vérifiables, D1 non versé, transition).
  - Ce biais dépend du rapport de deux vitesses : la v2.0 violait aussi `docs/exigences.md` § 2.7.

  Ce n'est pas un fait établi : aucun essai n'a fait varier l'ancre. Statut : calcul sur L et S+O.

**Mécanisme recommandé pour la fiche 8 (C2)** : une action intégrale sans fuite sur l'écart d'inflation. Deux formes sont équivalentes en algèbre : un r* estimé qui intègre π − π*, ou un terme de niveau des prix dans la règle. Elle donne π̄ = π* dans tout état stationnaire, quel que soit r̄, donc quelles que soient les décisions budgétaires du joueur, et quelle que soit sa vitesse.
- **Réserve forte** : l'instabilité 4 (« estimateur de r* sans ancre ni bande », R, faits § 6) interdit de reprendre cet intégrateur sans fait nouveau. Le fait nouveau exigible est l'analyse de stabilité en forme fermée de la boucle conjointe : intégrateur du bloc 8, SN, règle de prix, demande. Il faut un rayon spectral < 1 à la calibration et aux vitesses ×0,5 et ×2, avec un plancher de taux déclaré.
- **Fermeture budgétaire** : je la déconseille pour le pays joué. Elle retirerait au joueur son levier budgétaire, et elle ferait dépendre π̄ d'une règle cachée. Elle ne se discute que pour un pays non joué, ou si la fiche 9 a de toute façon une règle budgétaire.
- **r* fixe** : exact à la référence si r* = r̄ résolu. Mais tout choix budgétaire permanent du joueur déplace π̄ de (Δr̄)/a_π : c'est la reproduction du régime à 4 %.

**État initial résolu** :
- le script impose π̄ = π* et U = U^eq, et résout r̄ par la fermeture des fiches 5, 6 et 9 ;
- les états du bloc 8 prennent r*_0 = r̄, π^e_0 = π̄, i_0 = r̄ + π̄ (unités de la règle), et la crédibilité sa valeur stationnaire explicite à écart nul ;
- le registre se déduit de π̄.

Condition d'existence à déclarer : r̄ + π* ≥ plancher du taux. Sinon, aucun état stationnaire à π̄ = π* n'existe, et la résolution échoue de façon visible, sans préparation cachée.

**Précision de forme au § 3.N-6** : « π dérive jusqu'à ce que la politique de la fiche 8 ajuste la demande » vaut sous une règle intégrale ou sous un taux fixé. Sous une règle de Taylor sans action intégrale, π ne dérive pas : il se fixe à l'écart permanent ci-dessus. Il dérive (processus cumulatif de Wicksell) si le taux est maintenu sous r̄ + π* avec des anticipations adaptatives, ou si a_π ≤ 0. C'est par ce canal que la politique monétaire a un effet durable sur l'inflation dans un socle à monnaie endogène.

**Q6 — Terme d'activité.** Confirmé : s'il existe, il lit U_{t−1} à l'ouverture contre U^eq, le paramètre du bloc 3, lu à cette source unique et non dupliqué dans le bloc 8. Il ne lit jamais un chômage hystérétique (hypothèse réfutée 7 ; la v2.0 l'écartait déjà, l. 1368). Deux précisions :
- Écrire le terme directement en U, a_U(U^eq − U_{t−1}), plutôt qu'en écart de production converti par un coefficient d'Okun. La v2.0 prenait `okun` = 2 (l. 224), alors que la technique de M24 donne dU/d ln y = −0,95 (§ 3.N-11), soit un facteur 1/0,95 ≈ 1,05. Une constante d'Okun importée serait incohérente avec le modèle.
- Sous C2, un U^ref du bloc 8 différent de U^eq serait absorbé par r* sans effet sur π̄, mais il laisserait un terme d'activité non nul à l'état stationnaire, illisible pour le joueur. D'où la source unique.

**Q7 — Pente de court terme.** λ_w·β = 2 points de hausse salariale par point d'écart de chômage et par an.
- Approximation (marge instantanée, anticipation adaptative de gain λ_e, temps continu) : le ratio de sacrifice vaut environ **1/(λ_e·λ_w·β)** point-année de chômage par point de désinflation. Cela donne 2,50 à λ_e = 0,2 (`lam0` de la v2.0, l. 228), 1,00 à 0,5, 0,50 à 1 et 0,25 à 2 (commande au Retour). Le coût de désinflation est donc fixé **conjointement** par la pente et par la loi de la fiche 8 ; une crédibilité qui fait sauter π^e vers la cible le réduit encore. Calibrer λ_w·β seul n'a pas de sens.
- **Aucune source de calibration lue.** Candidats :
  - Ball (1994), « What Determines the Sacrifice Ratio? », dans Mankiw (dir.), *Monetary Policy*, University of Chicago Press, 155-182. Existence vérifiée. Résultat lu dans un extrait de recherche, chiffres non lus : le ratio est plus faible quand la désinflation est rapide et les salaires flexibles.
  - Galí (2011), « The Return of the Wage Phillips Curve », *JEEA*. Cité de mémoire, existence non vérifiée dans la session.
- Je propose une calibration conjointe (λ_w·β, λ_e) au J3, sur une cible de ratio de sacrifice sourcée. Le rapport « λ_w = 2 instable » de la v2.0 (l. 138, L) relève de la mesure 5 (e) de la fiche 4, sur la grille λ_e ∈ {0,5 ; 1 ; 2}.

### 6.2 Avis général sur R + SN, côté monnaie

**Favorable**, sous les conditions C1 à C8 transmises à la fiche 8.
- La règle SN avec un coefficient 1 sur π^e donne une courbe de long terme verticale, et laisse au bloc 8 seul l'ancre nominale. La racine unité nominale signalée au § 3.L (H-p2) est attendue : le niveau des prix n'est pas ancré, sauf si la fiche 8 retient un terme de niveau des prix.
- Les lectures (a) pour la Q3 et (G) pour la Q4 sont concordantes avec `macro`. **Aucun désaccord de fond** n'est à soumettre en deux positions. Seule précision : la forme de la phrase du § 3.N-6 (Q5).
- Sur le choix entre R et C, je suis neutre : il relève de `macro` et de `jeu`. C modifie WB et les profits non distribués, donc la demande de crédit (fiches 6 et 7), de façon transitoire seulement.
- Pour `jeu` : sous SN et C2, une cible relevée relève π̄ point pour point sans gain d'emploi durable ; une désinflation coûte de l'ordre de 0,25 à 2,5 points-années de chômage par point, selon la crédibilité. Ce sont deux coûts perceptibles à l'échelle d'une partie.

### 6.3 Conditions transmises à la fiche 8 (banque centrale et anticipations)

- **C1** — Aucune erreur d'anticipation à l'état stationnaire : π^e = π̄ dans tout état stationnaire. Un terme d'ancrage vers π* ne s'admet que si C2 garantit π̄ = π*.
- **C2** — Action intégrale sans fuite sur l'écart d'inflation (r* estimé ou terme de niveau des prix), donnant π̄ = π* indépendamment de r̄ et des vitesses. Exige un fait nouveau contre l'instabilité 4 : stabilité en forme fermée de la boucle conjointe, aux vitesses ×0,5 et ×2. L'ancre avec bande et rappel de la v2.0 forme un intégrateur à fuite (`policies.py` l. 62) : écart stationnaire (r̄ − ancre)/(a_π + k), fonction des vitesses. À ne pas reprendre.
- **C3** — État initial résolu : r*_0 = r̄ (fermeture des fiches 5, 6 et 9), π^e_0 = π̄ = π*, i_0 = r̄ + π̄, crédibilité à sa valeur stationnaire explicite à écart nul. Condition d'existence déclarée : r̄ + π* ≥ plancher du taux.
- **C4** — Lecture commune (G) des taux annuels : cible comparée au glissement (lecture (ii) de #24), π^e en glissement anticipé. Stocker ln(1 + π^e) est suggéré (domaine π^e > −1 par construction).
- **C5** — π^e est une variable d'état d'ouverture du bloc 8, lue par les blocs 3 (et 4) sous la lecture (a). Le bloc 8 ne lit jamais W_t. Sa position en phase 1 reste libre, et s'ordonne avec la Q1 de la fiche 4.
- **C6** — Terme d'activité éventuel : a_U(U^eq − U_{t−1}), U^eq lu dans le bloc 3, aucun coefficient d'Okun importé, aucune hystérèse.
- **C7** — Calibration conjointe du gain d'apprentissage λ_e et de la pente λ_w·β sur un ratio de sacrifice sourcé (J3). Le ratio de sacrifice est restitué au joueur ou dans le scénario O2 (avis de `jeu`).
- **C8** — La crédibilité a une valeur stationnaire explicite, indépendante des vitesses. Une loi à seuil comme K1a (bonus seulement si l'écart est inférieur à 1 point, `model.py` l. 1305) n'est pas reprise sans fait nouveau. Il faut aussi reconfirmer l'intention du mainteneur du 17/09/2026 : effet de long terme de la politique monétaire sur l'inflation, par la cible et le taux, la monnaie étant endogène.

## 7. Avis de `jeu`

*`jeu`, 03/10/2026 (issue #39, jalon 2), sur la fiche à l'état `e7873e6` (branche `claude/j1-economie-reelle`, PR #43). Réponses aux questions 1 à 10 de `macro`, dont la question 10 ajoutée en cours d'instruction.*

**Chiffres.** Aucun moteur n'existe encore (`src/nations/blocs/` ne contient que `__init__.py`). J'ai écrit une maquette indépendante, qui n'importe pas les scripts de `macro`. Elle comprend :
- le socle N1 à N7 de la fiche 2 ;
- la règle d'emploi R ou C ;
- le salaire SN, sous H-p1 ou H-p2.

Hypothèses : g = 0, pr = 1, anticipation constante, et les valeurs du § 3.0 (λ_v = 3, λ_IN = 1,5, σ = 1,4 mois, U* = 5 %, λ_w = 1, β = 2, part de G 20 %).

Exécution le 03/10/2026, scripts hors dépôt : `uv run --no-project python jeu_travail.py`, `variantes.py`, `jeu2.py` et `jeu3.py`.

- **Contrôle de la maquette.** Elle reproduit le § 3.L au millième près pour la production, l'emploi R et C, le chômage R et C, la productivité apparente C et la colonne H-p2.
- **Écart sur la colonne « W (R), H-p1 »** (constat transmis à `macro`, sans effet sur mon verdict). Les valeurs publiées sont +0,142, +0,188, +0,195, +0,127 et +0,027 % aux tours 9, 13, 14, 18 et 24. Ce sont exactement celles de **λ_w = 2 et β = 1**. Avec λ_w = 1 et β = 2, les valeurs du § 3.0 et du § 3.N-7 (valeur propre 0,91667), on obtient +0,172, +0,258, +0,274, +0,234 et +0,121 %. Les tours 3 et 4, et la colonne H-p2, ne dépendent que du produit λ_w·β = 2, ce qui explique qu'ils concordent. La question 9 (« +0,19 % au tour 13 ») vient de cette colonne.
- **Ampleurs sous R, H-p1.**

  | Choc | m | Chômage au plus bas | Glissement salarial sur 12 tours, au tour 13 | Pic du salaire |
  |---|---|---|---|---|
  | G +1 % | 0 | −0,23 point (tour 10) | +0,26 point | tour 15 |
  | G +1 % | 0,6 | −0,55 point (tour 13) | +0,45 point | tour 19 |
  | G +5 % | 0 | −1,17 point | +1,29 point | tour 15 |
  | G +5 % | 0,6 | −2,75 point (chômage à 2,25 %) | +2,25 points | tour 19 |
  | G +10 % | 0,6 | **chômage à 0 au tour 12** ; production visée non réalisée 0,52 % | +4,45 points | tour 19 |

- **Récession, G −5 % aux tours 1 à 12, m = 0,6.** Creux de production de −2,89 % au tour 13 dans tous les cas.

  | Règle | Pic du chômage | Chômage au tour 4 | Sureffectif maximal |
  |---|---|---|---|
  | R | +2,75 points au tour 13 | +0,97 point | 0 |
  | C, demi-vie 2 tours | +2,38 points au tour 14 | +0,48 point | 0,60 % |
  | C, demi-vie 3 tours | +2,19 points au tour 15 | +0,36 point | 0,84 % |
  | C, demi-vie 4 tours | +2,02 points au tour 16 | +0,29 point | 1,05 % |
  | C, demi-vie 6 tours | +1,74 point au tour 17 | +0,21 point | 1,36 % |

  Le sureffectif est nul au tour 24 dans tous les cas.
- **Scénario adverse : demande pulsée.** G suit un créneau de ±a, de moyenne nulle, en demi-périodes de h tours ; m = 0,6 ; moyennes des tours 13 à 252.

  | Règle | a = 5 %, h = 3 | a = 5 %, h = 6 | a = 5 %, h = 12 | a = 10 %, h = 6 |
  |---|---|---|---|---|
  | R | +0,002 | +0,005 | +0,013 | +0,009 |
  | C, demi-vie 2 tours | −0,23 | −0,29 | −0,35 | −0,58 |
  | C, demi-vie 3 tours | −0,29 | −0,39 | −0,52 | −0,79 |
  | C, demi-vie 4 tours | — | −0,48 | −0,65 | — |
  | C, demi-vie 6 tours | −0,39 | −0,59 | −0,86 | −1,17 |

  Écarts du chômage moyen, en points. La production moyenne est identique sous R et sous C (−0,002 à −0,014 %). Sous C, la contrepartie est un sureffectif moyen de 0,24 à 1,23 % de l'emploi, payé par les profits, et un salaire plus élevé de 0,5 à 2,4 % sous H-p1.
- **Question 10.** Sous (L), la cible affichée π et le glissement effectif s'écartent ainsi :

  | Cible affichée | Glissement effectif | Anticipation stationnaire |
  |---|---|---|
  | 2 % | 2,0184 % | 1,9819 % |
  | 10 % | 10,4713 % | 9,5690 % |
  | 50 % | 63,2094 % | 41,2393 % |

  Formules : (1 + π/12)^12 − 1 pour le glissement, et 12[(1 + π)^{1/12} − 1] pour l'anticipation.

**Question ludique de la fiche.** Le bloc n'ouvre aucun levier. Il fixe ce que le joueur voit de **son indicateur le plus politique**, le chômage, et du **coût différé** de ses relances, le salaire. La question est donc : le chômage a-t-il un délai, une contrepartie et un signal avant-coureur que le joueur peut relier à ses décisions, sans devenir un bouton réglable au tour près ?

### 7.A et 7.B Options A et B (brièvement)

Verdict : **à revoir**. Elles révisent M24 et ne résolvent pas leur état stationnaire (critères 3 et 4), si bien que le chômage dérive avant toute décision du joueur. B ajoute des bornes à seuil libre et un état caché, qui rendent une hausse de salaire inexplicable (clip 0,9 et 2,0, baisse de 20 %). Je n'ajoute rien au § 5.

### 7.R Option R — sans retard

- **Ce que voit le joueur.**
  - Une relance au tour n se lit dans les stocks au tour n, dans la production et le chômage au tour n + 1, dans le salaire au tour n + 2.
  - Le chômage reproduit la production au tour près, avec un coefficient de −0,95.
  - Le salaire culmine 2 à 6 tours après le creux du chômage (tour 15 ou 19 pour un chômage au plus bas au tour 10 ou 13). Le coût arrive après le bénéfice : c'est la bonne structure de tentation (relance aujourd'hui, inflation salariale demain).
- **Leviers.** Aucun propre. Le tableau levier → délai du § 3.L est net.
- **Stratégies.** Le point (i) du 7.C de la fiche 2 subsiste entièrement : **le chômage est l'écart de production, réglable au tour suivant par la dépense**, dans les deux sens. Son coût n'est que salarial, puis relève des prix (fiche 4) et de la dette (fiche 9).
- **Risques.**
  - Aucun signal avant-coureur côté emploi d'une récession : le chômage monte le tour même où la production baisse. Le seul signal reste celui des stocks (fiche 2).
  - Le chômage atteint 0 avec un levier ordinaire (question 6).
- **Verdict : lisible.** R ne fait rien de faux. Elle ne donne au joueur ni signal d'alerte côté emploi, ni inertie du chômage.

### 7.C Option C — rétention asymétrique

- **Ce que voit le joueur.**
  - **En hausse**, tout est identique à R : l'embauche est immédiate.
  - **En baisse**, le chômage ne monte pas au tour du choc. Le sureffectif apparaît d'abord (0,84 % de l'emploi au tour 8 pour G −5 %, demi-vie de 3 tours), les licenciements suivent, et le chômage culmine au tour 15, **deux tours après le creux de production**. Le joueur vit le dilemme classique « la reprise est là, mais le chômage monte encore ».
  - **Après une relance**, le chômage tarde à remonter : −0,105 point au tour 18 contre +0,003 sous R. Le sureffectif est alors la gueule de bois de la relance, visible dans les profits.
  - **Ce que C ne produit pas** : la « reprise sans emplois » de mon avis à la fiche 2 (7, question 7 (b)). Seule D la produirait, et D échoue au critère 5 (c).
- **Leviers.** Aucun propre. La production est identique à celle de R, donc le cycle des stocks déjà commenté à la fiche 2 ne change pas : c'est un bon point de lisibilité.
- **Stratégies.** Le réglage du chômage au tour près disparaît **à la baisse** : une austérité ne fait pas monter le chômage tout de suite. Il reste **à la hausse**. D'où le risque ci-dessous.
- **Risques.**
  - **Demande pulsée** (mesure ci-dessus). Alterner relance et rigueur abaisse durablement le chômage moyen, de −0,23 à −0,86 point selon la demi-vie et le rythme, à production moyenne inchangée. Ce n'est pas gratuit : le sureffectif est payé par les profits, ce qui réduit l'investissement si la fiche 6 le lit, et le salaire monte, puis les prix (fiche 4) et la réaction de la banque centrale (fiche 8). La maquette ne mesure pas ces coûts, faute de prix endogènes. **À tester au J4** (condition 4). L'ampleur croît avec la demi-vie, d'où ma borne haute.
  - *Réponse imperceptible* pour les petits chocs. À G +1 %, l'écart entre R et C sur le chômage est d'au plus 0,07 point (tour 14 : −0,145 contre −0,214). Le retard ne se voit que pour des chocs d'un point de demande ou plus.
  - *Comportement contre-intuitif* : aucun. La productivité apparente ne dépasse jamais sa tendance. C'est une demi-procyclicité, mais elle ne choque pas le joueur, qui ne voit qu'un « sureffectif » nul ou positif.
- **Verdict : lisible**, sous les conditions 1 à 4.

### 7.D Option D — ajustement partiel symétrique

- **Ce que voit le joueur.** Une pénurie en reprise alors que 5 % de la population active est au chômage : « des chômeurs, et des entreprises qui ne peuvent pas produire faute de bras ». C'est inexplicable dans un modèle sans appariement.
- **Verdict : à revoir.** Ce n'est pas ce que je demandais à la fiche 2 : je voulais un signal avant-coureur et de l'inertie, non une pénurie de main-d'œuvre fictive. Ma condition 5 de la fiche 2 (« ajustement partiel ») est remplie dans son intention par C.

### Réponses aux dix questions de `macro`

1. **R ou C.**
   - **Ma préférence ludique est C.** Elle apporte le signal avant-coureur (sureffectif avant licenciements) et l'inertie du chômage en sortie de crise, sans toucher au cycle de production.
   - Le critère 10 (b) est une exigence à deux branches. La branche « mécanisme perçu », qui relève de moi, est **satisfaite** pour les chocs d'un point de demande ou plus (pic du chômage décalé de 2 tours et réduit de 20 % à demi-vie de 3 tours ; sureffectif de 0,8 %). Elle ne l'est **pas** pour les chocs de 0,2 point.
   - La branche « fait établi » n'est pas remplie : 3.N-11 ne s'appuie que sur des extraits. **Je ne conteste donc pas que R prévale tant que les sources ne sont pas lues.**
   - **Fourchette proposée** : demi-vie de **2 à 4 tours**, soit λ_N de 1,91 à 3,51 par an, avec une valeur centrale de **3 tours** (λ_N = 2,48). La valeur de `macro`, λ_N = 2,4 (3,11 tours), est dans la fourchette. Le seuil est développé plus bas.
2. **Productivité apparente et masse salariale excédentaire sous C.**
   - Ce sont **la même information** : W(N − y/pr)/(W·N) = 1 − (y/N)/pr. Vérifié au tour 18 : sureffectif de 0,113 %, productivité apparente de −0,113 %. 3.N-9 donne aussi 1,961 % = 1 − 1/1,02.
   - Afficher les deux, c'est afficher deux fois la même chose sous deux noms. Je demande **un seul indicateur**, le **sureffectif** : « emplois conservés sans production correspondante », en personnes et en % de l'emploi. La productivité apparente sert de définition. Le montant en u.m. ne figure que dans le compte des entreprises, comme charge réduisant le résultat courant.
   - Sous cette forme, l'indicateur est **lisible** : « les entreprises paient 0,8 % de leurs salariés à ne rien produire ».
   - Je révise ma condition de la fiche 2 (« productivité apparente rapportée à sa tendance ») en ce sens.
   - Sous R, l'indicateur disparaît. Le signal avant-coureur reste alors celui des stocks au-dessus de leur niveau normal (fiche 2).
3. **Coefficient d'Okun de −0,95.**
   - **Acceptable au socle et au J3 comme limite déclarée, à traiter avant le J7.**
   - Conséquence ludique mesurée : avec m = 0,6, une relance de G +10 %, soit 2 points de demande pendant 12 tours, **amène le chômage à 0 au tour 12**. Une relance de cet ordre n'a rien d'extrême dans une partie. Le chômage devient un indicateur trop sensible, et c'est probablement l'indicateur le plus pondéré par le joueur, puis par le score et le soutien politique (J7).
   - Le choix du mécanisme relève de `macro` : participation endogène (« travailleurs découragés », lisible et dans l'esprit de Victoria 3 au prix d'un indicateur de plus, le taux d'activité) ou marge des heures. Ma préférence ludique va à un mécanisme plutôt qu'à un plancher (question 6).
   - Je propose de décider au J4, sur la fréquence d'un chômage inférieur à 1 % dans les scénarios du catalogue (issue proposée).
4. **Pente de 2 points par point de chômage et par an.**
   - **Perceptible** : à G +5 % et m = 0,6, le glissement salarial passe de 4,06 % à environ 6,3 % au tour 13.
   - **Pas trop forte pour le jeu**, puisqu'elle fait apparaître le coût de la relance dans l'année. Le pic du salaire 6 tours après le creux du chômage donne au joueur le temps de céder à la tentation, ce qui est voulu.
   - Je ne peux pas dire si elle est trop forte en fidélité (pente non trouvée en 3.N-11), ni dans la boucle salaires – prix (critère 5 (d), avec la fiche 4).
   - Réserve : l'Okun doublé double aussi la réponse salariale par point de production (environ 1,9 point par an et par point d'écart de production). La question 3 commande donc aussi celle-ci.
5. **Délai anticipation → salaire : 1 tour (lecture (a)).**
   - La grammaire des délais reste uniforme : une décision du tour n agit sur le secteur privé au tour n + 1 au plus tôt.
   - Sous (b), toute annonce de la banque centrale qui déplace π^e le tour même (fiche 8) agirait sur les salaires sans délai, sans contrepartie visible au tour. Ce serait un levier instantané par la communication. Accord avec `macro`.
6. **Chômage à 0 en surchauffe.**
   - Un « 0,0 % » affiché est **contre-intuitif** : personne ne cherche d'emploi, pas même entre deux postes.
   - Affichage demandé quand la borne N ≤ N^pa est active : le chômage avec la mention « **plein emploi : main-d'œuvre épuisée** », et, à côté, la production visée non réalisée (condition 3 de la fiche 2), qui en est la contrepartie.
   - Signal avant-coureur : le chômage sous la moitié de U^eq, signalé comme « tension sur le marché du travail ».
   - Je **ne demande pas de plancher frictionnel** : ce serait une borne à paramètre, contraire à la lecture (ii) de #38 décidée le 03/10/2026.
   - **Question pour `macro`** (choix de fond, non tranché ici) : une courbe des salaires convexe, dont la semi-élasticité croît quand U tend vers 0, éloignerait le chômage de 0 par un mécanisme.
7. **Levier institutionnel au J4 : préférence pour une entrée par la norme ω* (lecture (w2)).**
   - Avec un seul type de travailleur, un W^min borné ne mord jamais, ou fixe d'un coup tout le salaire. C'est un interrupteur sans gradation, et une borne qui rappelle l'instabilité 15.
   - Par ω*, le levier « pouvoir de négociation, droit du travail » agit progressivement (demi-vie de 8 tours de SN). Il a un arbitrage lisible : une part salariale plus haute contre un chômage d'équilibre plus haut (U* = U^eq + ln(ω*(1 + μ̄))/β), avec des gagnants (salariés en place) et des perdants (profits, chômeurs).
   - **Condition** : abaisser ω* doit avoir un coût perceptible, par la consommation des ménages (fiche 5) ou par le soutien politique (J7). Sinon, réduire le chômage d'équilibre par la loi est une stratégie dominante.
   - Le salaire minimum proprement dit attend une hétérogénéité des travailleurs (J ≥ 2, hors socle).
8. **Salaire réel sous marge instantanée (H-p2) : à clarifier.**
   - Le joueur voit un salaire nominal en hausse durable (+0,43 % au tour 24) et un pouvoir d'achat inchangé : « les hausses de salaire sont mangées par les prix ». C'est lisible et pédagogique, **à condition** d'afficher côte à côte W, W/P et la part salariale.
   - Le défaut est ailleurs : la relance n'a aucun effet de répartition entre salaires et profits, et ses seuls gagnants sont les nouveaux embauchés. O2 demande des gagnants et des perdants. Une marge qui répond à la tension rendrait le salaire réel parlant. C'est l'affaire de la fiche 4 (instabilité 14), que je commenterai à son avis.
9. **Ampleurs de l'exemple daté.**
   - −0,23 point de chômage est **à la limite du perceptible** : 5,0 → 4,8 % à une décimale.
   - Le salaire, remesuré sous la calibration déclarée, monte de +0,26 % au tour 13, et non de +0,19 % (constat ci-dessus). Le glissement passe de 4,06 à 4,32 % : **perceptible** à une décimale.
   - Avec m = 0,6 : −0,55 point et +0,45 point, nettement perceptibles.
   - Je maintiens le test O2 à +1 % et à +5 % (condition 6 de la fiche 2).
10. **Lecture des taux annuels : (G) préférée.**
    - À 2 %, l'écart de (L) est invisible à une décimale (2,0184 %, 1,9819 %). Il n'en reste pas moins un défaut ludique, pour trois raisons :
      - (a) le **levier** est une cible fixée par le joueur (fiche 8), et sous (L) elle n'est jamais atteinte, ce qui contredit « ce que je fixe est ce que je vois » ;
      - (b) l'écart entre la cible et l'anticipation stationnaire (2 % contre 1,98 %) se lirait comme un **défaut de crédibilité** qui n'en est pas un, alors que c'est précisément le signal que la fiche 8 doit rendre lisible ;
      - (c) l'écart croît avec l'inflation (10 % → 10,47 % et 9,57 % ; 50 % → 63,2 % et 41,2 %), c'est-à-dire **dans les crises** (O3), là où le joueur lit les chiffres de plus près.
    - (G) est en outre une condition de SN au critère 4 (3.N-4).
    - Si (L) était retenue, la restitution devrait afficher le taux effectif à côté du paramètre, comme pour la croissance tendancielle à la fiche 2 (2,0184 %).

### Indicateurs du tour (critère 11 (a))

| Indicateur | Verdict | Motif ou point à clarifier |
|---|---|---|
| Taux de chômage (au tour ; moyenne sur 12 tours) | **lisible** | Afficher U^eq comme niveau normal. Mention « plein emploi : main-d'œuvre épuisée » quand la borne est active (question 6) |
| Emploi (personnes) | **lisible** | — |
| Salaire nominal (glissement sur 12 tours) | **lisible** | Niveau normal dans la définition exacte : 4,0588 % à π̄ = 2 % (g_pr linéaire, M24 (f)), et non 4 % |
| Salaire réel W/P | **à clarifier** | Indice de base 100, avec son glissement normal (2,0184 %) ; toujours affiché à côté du nominal (question 8) |
| Part salariale (ΣWB/ΣVA sur 12 tours) | **à clarifier** | Niveau normal dans **la même définition** que l'indicateur : l'écart entre ω̄ et WB/VA sur 12 tours, publié selon l'amendement, ne doit pas apparaître comme une dérive (même principe que les stocks à 1,4152 mois, fiche 2) |
| Productivité apparente et masse salariale excédentaire (C) | **à revoir comme deux lignes** | Grandeur unique ; restituer le **sureffectif** en personnes et en % de l'emploi, et le montant en u.m. dans le compte des entreprises seulement (question 2) |

### Préférence motivée

- **Ma préférence va à C**, `macro` recommandant R et préférant C si un retard est retenu. Nous ne divergeons pas sur la procédure : sans fait établi, le critère 10 (b) impose R, et je ne le conteste pas. Je retiens C parce que le chômage y acquiert un **délai, un signal avant-coureur et une inertie de sortie de crise** que le joueur peut relier à ses décisions, sans changer la production.
- **Suggestion au mainteneur** : faire lire les sources primaires avant M25 plutôt qu'adopter R pour passer à C plus tard. Le passage serait peu coûteux (production identique), mais il changerait le chômage restitué, donc demanderait un visa.
- **Classement** : C > R > D > B > A. R est lisible mais n'offre ni signal avant-coureur ni inertie. D crée une pénurie inexplicable.
- **Accords et réserves sur les lectures du § 5** :
  - (a) lecture à l'ouverture : accord (question 5) ;
  - (b) conversion géométrique : accord, et (G) pour la lecture unique (question 10) ;
  - (c) (w1) au socle, (w2) au J4 comme interface du levier : accord, sous la condition de coût de la question 7 ;
  - (d) et (e) : sans enjeu ludique ;
  - (f) aucun levier propre : accord.

### Conditions demandées au § 9 (restitution et essais)

1. **Sureffectif** (sous C), indicateur unique en personnes et en % de l'emploi, qui remplace la productivité apparente et la masse salariale excédentaire comme lignes distinctes. Le montant en u.m. figure dans le compte des entreprises, comme charge du pas.
2. **Niveaux normaux** dans la définition exacte de chaque indicateur, publiés par le script d'état stationnaire : U^eq ; glissement salarial nominal (4,0588 % à π̄ = 2 %) ; glissement du salaire réel (2,0184 %) ; part salariale dans la définition sur 12 tours.
3. **Chômage nul** : mention « plein emploi : main-d'œuvre épuisée » et production visée non réalisée à côté. Signal de tension sous U^eq/2. Aucun plancher frictionnel.
4. **Scénario adverse O2 au J4, à écrire avant l'essai.** Dépense publique en créneau de ±5 %, de moyenne nulle, en demi-périodes de 6 et de 12 tours, contre une dépense constante, avec prix et politique monétaire endogènes. On publie l'écart du chômage moyen, le sureffectif, les profits, le glissement salarial et l'inflation. Le critère de verdict (coût jugé suffisant ou non) est à fixer par le mainteneur avant l'essai.
5. **W, W/P et la part salariale toujours affichés ensemble.**
6. **Fourchette de demi-vie** de la condition 5 de la fiche 2, ramenée à 2 à 4 tours (seuil ci-dessous) si C est retenue.

### Seuil proposé au mainteneur (critère 11 (d)), si C est retenue

- **Grandeur** : demi-vie de l'écart d'emploi en régime de baisse, ln 2 / (−ln(1 − λ_N/12)), en tours.
- **Seuil** : de 2 à 4 tours, bornes comprises, soit λ_N de 1,91 à 3,51 par an. Valeur centrale proposée : 3 tours (λ_N = 2,48). La valeur 2,4 de `macro` (3,11 tours) est dans la fourchette.
- **Calibration visée** : la calibration proposée. Aux vitesses ×0,5 et ×2, les valeurs sont publiées sans être exigées, comme pour la bande du critère 5 (c).
- **Motifs** :
  - **Borne basse.** À 2 tours, le retard reste perceptible pour un choc d'un point de demande : chômage au tour 4 de +0,48 point contre +0,97 sous R, pic décalé d'un tour, sureffectif maximal de 0,60 %. Je n'ai pas mesuré en deçà : la borne reprend ma condition de la fiche 2.
  - **Borne haute.** Au-delà de 4 tours, la demande pulsée rapporte plus de 0,6 point de chômage moyen pour un créneau de ±5 % (−0,65 à 4 tours, −0,86 à 6 tours, pour h = 12). Et le pic de chômage d'une récession est amorti de plus d'un quart (−27 % à 4 tours, −37 % à 6 tours) : la crise se lit alors dans les profits plutôt que dans le chômage.
  - **Indication non établie.** L'extrait d'Okun (« un à deux trimestres », 3.N-11) suggère une demi-vie d'environ 3 tours. Ce n'est pas un fait établi.

## 8. Décision du mainteneur

Non instruit (M25, décidée avec la fiche 4).

## 9. Conséquences de la décision

Non instruit.

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 03/10/2026 | Ouverture (issue #39) ; § 1 et § 2 proposés | `macro` ; session principale |
| 03/10/2026 | Critères validés avec amendements (seuils, bande du critère 5 (c), lecture (ii) de #38 au critère 7, Q2, Q3, Q7 ; issue #39) | mainteneur |
| 03/10/2026 | Amendement pris avec les critères de la fiche 4 (part salariale sur W/(p·pr), bande commune, lecture unique de #24), avant la fin de l'instruction | mainteneur |
| 03/10/2026 | Instruction déposée (§ 3 à 5) : options A, B, socle 3.N, R, C, D ; recommandation R (salaire SN, lectures (a) à (f)), C en alternative conditionnelle ; A, B, D et SP écartées ; remesure T1 proposée | `macro` |
| 03/10/2026 | Additif de `macro` après la décision du mainteneur sur la part salariale et la lecture unique des taux annuels : § 3.N-4 remplacé (lectures communes (L) et (G), préférence (G) avec révision de M24 (f)), condition 3 (d) sur W/(p·pr) avec écart publié (C13), § 4 et § 5 mis à jour | `macro` ; session principale |
| 03/10/2026 | Avis de `jeu` (§ 7) : préférence C > R > D > B > A, R imposée par le critère 10 (b) tant que les sources ne sont pas lues ; seuil de demi-vie de 2 à 4 tours proposé ; lecture (G) préférée ; écart relevé dans la colonne « W (R), H-p1 » du § 3.L | `jeu` |
| 03/10/2026 | Correction de l'exemple daté du § 3.L (constat de `jeu`) : la règle de salaire du script soustrayait deux fois l'écart de salaire, ce qui revenait à λ_w = 2 et β = 1 au lieu de λ_w = 1 et β = 2 ; colonnes « W, H-p1 » de R et de C remesurées ; colonne H-p2, valeur propre et verdicts inchangés | `macro` ; `jeu` |
| 03/10/2026 | Avis de `monnaie` (§ 6) : favorable à R + SN, lectures (a) et (G), indexation complète, aucun désaccord de fond ; huit conditions transmises à la fiche 8 (C1 à C8) | `monnaie` |
| 03/10/2026 | Statut « avis rendus » | session principale |
| 03/10/2026 | `jeu` corrige sa réponse à la question 7 du § 7 (levier sur la norme ω*, lecture (w2)) : sous une règle de prix qui ancre μ̄, ω* ne déplace pas la part salariale et le conflit devient une inflation permanente ; correction consignée au § 7 de la fiche 4 (`docs/blocs/prix.md`) | `jeu` ; session principale |
| 03/10/2026 | Additif de `macro` : sources primaires lues (BLL 2013, Abraham et Houseman 1993, Hamermesh 1988, McKay et Reis 2006, Galí et van Rens 2021, Blanchflower et Oswald 2005, Blanchard et Katz 1999, Galí 2010) ; § 3.N-11 remplacé, § 3.N-12 ajouté ; retard établi, forme asymétrique non établie ; deux lectures du critère 10 (b) soumises au mainteneur ; λ_N = 3,5 proposé sous la lecture (i) ; réserve sur λ_w | `macro` |
