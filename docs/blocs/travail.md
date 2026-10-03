---
bloc: Travail et salaires
module: src/nations/blocs/travail.py
expert pilote: macro
experts consultés: monnaie (indexation des salaires sur les anticipations : frontière inflation) ; jeu
statut: en instruction (critères validés le 03/10/2026)
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

## 3. Options

Non instruit (jalon 2 de l'issue #39, après validation des critères).

## 4. Tableau comparatif

Non instruit.

## 5. Avis de l'expert pilote

Non instruit.

## 6. Avis de l'expert consulté

Non instruit (`monnaie`, frontière inflation, au jalon 2).

## 7. Avis de `jeu`

Non instruit.

## 8. Décision du mainteneur

Non instruit (M25, décidée avec la fiche 4).

## 9. Conséquences de la décision

Non instruit.

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 03/10/2026 | Ouverture (issue #39) ; § 1 et § 2 proposés | `macro` ; session principale |
| 03/10/2026 | Critères validés avec amendements (seuils, bande du critère 5 (c), lecture (ii) de #38 au critère 7, Q2, Q3, Q7 ; issue #39) | mainteneur |
