# Inventaire des blocs du socle

Tenu par `architect`. Ce fichier désigne, pour chaque bloc de la spécification, l'**expert pilote** (qui instruit la fiche comparative, spécifie en amont et valide en aval), les **experts consultés** sur les sujets frontière, le **module** de `src/nations/blocs/` visé et l'**ordre d'instruction**. Il fait foi pour « l'expert » de `CLAUDE.md` et du workflow `circuit-technique`. Le gabarit des fiches est `0000-gabarit.md` ; il est validé **à l'usage** (M20, 30/09/2026) : éprouvé sur la première fiche, « temps et comptabilité », puis validé par le mainteneur avec ses retouches, à la décision de cette fiche. Les désignations d'experts pilotes et de modules du § 1 ont été validées par le mainteneur le 30/09/2026.

Le **socle** est l'économie fermée à un pays (jalons J1 à J3, décision du mainteneur du 29/09/2026 : premier jalon en économie fermée). Les blocs hors socle (commerce et change, actifs et crises, systèmes économiques et soutien politique) seront inventoriés ici aux jalons J5 à J7 ; ils ne sont pas instruits avant.

## 1. Les neuf blocs du socle

| N° | Bloc | Fiche | Module visé | Expert pilote | Experts consultés | Statut |
|---|---|---|---|---|---|---|
| 1 | Temps et comptabilité | `temps_comptabilite.md` | transverse : `src/nations/noyau/` (comptes, grand livre, identités) et `src/nations/moteur/` (calendrier, phases) ; radicaux de labels `noyau` et `moteur` | `macro` | `monnaie` (bilans de la banque et de la banque centrale) ; `jeu` (rapport pas / tour) | **décidée (M22)**, 30/09/2026 : option C (pas mensuel unique) et socle commun § 3.N, lectures (a) à (f) ; ADR 0005 ; **spécifiée**, 02/10/2026 : section `sec:cadre` rédigée en section proposée et validée par `macro` et `monnaie` (#18, PR #20 fusionnée le 02/10/2026, `3518e18`) ; labels `noyau` et `moteur` posés au J2. **Complété par M24, lecture (b)** (02/10/2026, ADR 0007) : la phase 4 reçoit un ordre interne déclaré, « travail, puis production » ; `sec:cadre` (l. 486 et `tab:phases`, ligne 4) à retoucher par `docwriter` avec la section de la fiche 2, sans changement de table |
| 2 | Production et stocks | `production.md` | `src/nations/blocs/production.py` | `macro` | `jeu` | **décidée (M24)**, 02/10/2026 : option C, socle commun § 3.N à bien unique (J = 1), lectures (a) à (g) toutes en (i) ; lecture (b), ordre interne de la phase 4 « travail, puis production » (contrat partagé) : **ADR 0007** (accepté le 02/10/2026) ; Q4 : volume du capital au bloc 2, ajustement de l'emploi au bloc 3, à confirmer par les fiches 3 et 6 ; issue liée #37 ; conséquences rédigées (fiche § 9 : douze labels `eq:production-*` à poser au J3, cinq paramètres, interfaces, tests attendus, remesure S1). « Spécifiée » une fois la section `sec:production` rédigée par `docwriter` et validée par `macro` (#34, jalon 4, branche n° 3a) |
| 3 | Travail et salaires | `travail.md` | `src/nations/blocs/travail.py` | `macro` | `monnaie` (indexation des salaires sur les anticipations : frontière inflation) ; `jeu` | à instruire (branche n° 3b). Hérite de M24 : tient l'emploi effectif N et la ligne 5, écrits en phase 4 **avant** le bloc 2 (ADR 0007) ; lit la demande de travail N* = y*/pr (phase 2) ; porte la contrainte d'offre de travail et l'ajustement éventuel de l'emploi (préférence de `jeu` pour un retard modéré, fiche 2 § 7, question 7 ; boucle emploi – stocks à mesurer, fiche 2 § 5) ; confirme Q4 |
| 4 | Prix | `prix.md` | `src/nations/blocs/prix.py` | `macro` | `monnaie` (indexation des prix sur les anticipations : frontière inflation) ; `jeu` | à instruire (branche n° 3b). Hérite de M24 : lit le coût unitaire UC = W/pr du bloc 2 (fiche 2 § 3.N-4) ; écrit le prix du pas en phase 5 avant le bloc 2 ; dit ce que déclenche le taux d'utilisation (#37) |
| 5 | Ménages | `menages.md` | `src/nations/blocs/menages.py` | `macro` | `monnaie` (dépôts et détention de titres publics : frontière dette publique) ; `jeu` | à instruire (branche n° 3b) |
| 6 | Investissement et financement des entreprises | `investissement.md` | `src/nations/blocs/investissement.py` | `macro` | `monnaie` (demande de crédit face à l'offre bancaire : frontière crédit) ; `jeu` | à instruire (branche n° 3b). Hérite de M24 : confirme le volume du capital au bloc 2 (Q4) ; reçoit le rapport ρ_K = K/(p K^vol) = 0,7775 à g = π̄ = 2 % et δ = 5 % et la définition de K/Y à déclarer (fiche 2 § 3.N-5) ; tranche la voie (ii) de #36 (ligne « profits non distribués », contrat partagé `tab:matrice-flux`) ; canal d'offre de l'investissement (#37) |
| 7 | Banque commerciale | `banque.md` | `src/nations/blocs/banque.py` | `monnaie` | `macro` (demande de crédit des entreprises : frontière crédit) ; `jeu` | à instruire |
| 8 | Banque centrale et anticipations | `banque_centrale.md` | `src/nations/blocs/banque_centrale.py` | `monnaie` | `macro` (prix et salaires : frontière inflation) ; `jeu` | à instruire |
| 9 | État et dette | `finances_publiques.md` | `src/nations/blocs/finances_publiques.py` | `macro` | `monnaie` (placement de la dette et prime : frontière dette publique) ; `jeu` | à instruire |

Conventions de nommage : modules en français, identifiants ASCII (`docs/exigences.md` § 4.2). Le bloc « État et dette » vise `finances_publiques.py` et non `etat.py`, pour ne pas entrer en collision avec le paquet `src/nations/etat/` (schéma d'état). Le radical du module est celui des labels d'équation `eq:<module>-<nom>` (`docs/specification/CONVENTIONS.md` § 2.1). Le bloc 1 n'est pas un module de `blocs/` : c'est le cadre que le noyau et l'ordonnanceur mettent en œuvre ; sa fiche tranche des questions qui conditionnent toutes les autres.

## 2. Sujets frontière

Trois sujets traversent plusieurs blocs et consultent les deux experts de fond (`CLAUDE.md`, « Experts de fond »). En cas de désaccord, les deux positions sont décrites dans la fiche et le mainteneur tranche.

| Sujet | Chez `macro` | Chez `monnaie` | Blocs concernés |
|---|---|---|---|
| Inflation | Formation des prix et des salaires | Anticipations et crédibilité | 3, 4, 8 |
| Crédit aux entreprises | Demande de crédit, financement de l'investissement | Offre bancaire, fonds propres, refinancement | 6, 7 |
| Dette publique | Solde, dynamique de la dette, règle budgétaire | Placement (banque, ménages, banque centrale), prime souveraine | 5, 7, 8, 9 |

`jeu` donne son avis sur chaque fiche (lisibilité, délai, coût, équilibre entre stratégies) ; il ne tranche pas le fond.

## 3. Ordre d'instruction proposé

L'ordre suit les dépendances : une fiche ne s'instruit pas avant que celles dont elle lit les variables soient au moins « avis rendus ». Il est proposé au mainteneur, qui peut le modifier.

| Rang | Bloc | Pourquoi à ce rang | Débloque |
|---|---|---|---|
| 1 | Temps et comptabilité | Fixe la durée du pas, la convention calendaire (question ouverte, `CONVENTIONS.md` § 6), la matrice des bilans et des flux, les tolérances relatives, l'ordre des phases. Toutes les autres fiches expriment leurs vitesses et leurs flux dans ce cadre | Toutes les fiches ; le jalon J2 (noyau) peut démarrer dès sa décision |
| 2 | Production et stocks | Côté offre : fonction de production, nombre de secteurs du socle (piste « deux secteurs » à instruire), stocks et production visée | 3, 4, 6 |
| 3 | Travail et salaires | Demande de travail issue de 2 ; salaire nominal et courbe de Phillips ; définit le coût du travail que 4 lit | 4, 5 |
| 4 | Prix | Coût unitaire (2, 3), marge, indexation ; c'est le premier point de la frontière inflation avec 8 | 5, 6 |
| 5 | Ménages | Revenu disponible (3, 4, plus tard 9), consommation (piste « cible de richesse » à instruire), épargne, dépôts et titres | 6, 7, 9 |
| 6 | Investissement et financement | Investissement (2, 4), autofinancement et demande de crédit ; première moitié de la frontière crédit | 7 |
| 7 | Banque commerciale | Offre de crédit (6), dépôts (5), fonds propres, réserves et refinancement (piste « corridor explicite » à instruire) ; seconde moitié de la frontière crédit | 8, 9 |
| 8 | Banque centrale et anticipations | Règle de taux, bilan, anticipations et crédibilité (piste « apprentissage à gain constant » à instruire) ; lit 4 et 3 (inflation réalisée), 7 (refinancement) | 9 |
| 9 | État et dette | Recettes assises sur 3 à 7, dépenses, solde, dette et son placement (5, 7, 8) ; clôt le bouclage stock-flux du socle | Spécification v3.0 « socle » ; résolution de l'état stationnaire (J3) |

Deux fiches peuvent s'instruire en parallèle quand leurs dépendances sont satisfaites et que leurs experts pilotes diffèrent : par exemple 6 (`macro`) et 7 (`monnaie`), sous réserve de l'échange sur la frontière crédit. Les anticipations (8) sont lues par 3 et 4 : les fiches 3 et 4 déclarent la variable d'anticipation qu'elles consomment et laissent à 8 sa loi de formation.

Les pistes nouvelles citées (« deux secteurs », « cible de richesse », « corridor explicite », « apprentissage à gain constant », « prix au coût normal majoré », « pas mensuel unique ») viennent de la passation du 29/09/2026 (§ 8) : ce sont des **options à instruire**, non des choix ; chacune doit s'appuyer sur une référence retrouvée dans sa fiche. La piste « pas mensuel unique » a été instruite et **retenue** (M22, 30/09/2026) : toutes les fiches suivantes expriment leurs vitesses en base annuelle, converties par la règle linéaire unique du cadre, et leurs délais en tours entiers (un pas = un tour). La piste « deux secteurs » a été instruite (fiche 2, option D, contre J = 1, J = 4 et la liste de la v1.5 : sept secteurs et des ressources) et **écartée** (M24, 02/10/2026) : le socle est à bien unique, J = 1, les équations étant indexées par j dès le socle pour qu'un secteur s'ajoute aux jalons J5 à J7 sans réécrire M24.

## 4. Cycle de vie d'une fiche

`à instruire` → `en instruction` (expert pilote saisi, issue ouverte) → `avis rendus` (expert pilote, expert consulté, `jeu`) → `décidée (M-n)` (décision du mainteneur reportée dans `docs/feuille-de-route.md`) → `spécifiée` (section **proposée** de la spécification rédigée par `docwriter` et validée par l'expert pilote ; sans label `eq:`, une équation non exécutée n'en portant pas, `CONVENTIONS.md` § 2.2) → `implémentée` (module codé, labels `eq:` créés et balises posées, concordance verte).

Définition de « spécifiée » et d'« implémentée » arrêtée par le mainteneur le 02/10/2026 (point d'étape après la PR #20) : la précédente exigeait des labels créés dès « spécifiée », ce qu'aucune fiche ne pouvait atteindre avant le code.

Une fiche décidée ne se réécrit pas : une révision passe par une nouvelle décision M-m, datée, qui cite la précédente. Le statut de ce tableau est mis à jour par `architect` à chaque changement.

Rythme d'instruction arrêté par M21 (30/09/2026) : la fiche 1 s'instruit **seule**, dans une branche de travail dédiée, jusqu'à sa décision et sa section de spécification ; les fiches suivantes s'instruisent par branches de trois à cinq issues, une branche technique d'outillage pouvant s'intercaler entre deux branches de fiches. Chaque fiche donne lieu à **une issue, en quatre jalons** cochés dans l'issue, chacun un commit `docs:` dont le SHA y est noté : critères écrits avant l'instruction (§ 1 et § 2 de la fiche), **validés par le mainteneur avant tout commit d'instruction** ; instruction et avis (§ 3 à 7) ; décision du mainteneur (§ 8) ; section proposée de la spécification (§ 9). Granularité arrêtée par le mainteneur le 02/10/2026 (point d'étape après la PR #29), en remplacement d'« au moins trois issues par fiche », qui portait une branche de deux fiches au-delà de cinq issues ; la fiche 1 en avait compté quatre (#15 à #18). La première fiche sert aussi d'épreuve du gabarit (M20) : les retours des agents sur le gabarit sont consignés dans leur compte rendu et soumis au mainteneur avec la décision.

## 5. Hors socle (inventaire à venir)

| Bloc | Jalon | Expert pilote pressenti |
|---|---|---|
| Commerce, change, balance des paiements, régimes de souveraineté A à E | J5 | `monnaie` (change, régimes) ; `macro` (commerce) |
| Actifs, bulles, ruées, défaut, hyperinflation, économie effondrée | J6 | `monnaie` |
| Systèmes économiques (planification, nationalisation), soutien politique, conditions de fin | J7 | `macro` (systèmes) ; `jeu` (soutien, fin) |

Ces désignations sont pressenties, non arrêtées ; elles seront fixées quand le socle sera décidé.

## 6. Historique de l'inventaire

| Date | Événement |
|---|---|
| 29/09/2026 | Création (issue #6, branche `claude/fondations`) : neuf blocs, experts pilotes, ordre d'instruction proposé. |
| 30/09/2026 | Mainteneur : experts pilotes et modules validés (`macro` pour « temps et comptabilité » et « État et dette », module `finances_publiques.py`) ; gabarit validé à l'usage (M20) ; fiche 1 instruite seule dans la branche J1 n°1 (M21). |
| 30/09/2026 | Fiche 1 « temps et comptabilité » décidée (M22) : option C et socle commun ; ADR 0005 accepté ; gabarit retouché validé par le mainteneur (M20, issue #17). |
| 02/10/2026 | PR #20 fusionnée (`3518e18`) : section `sec:cadre` proposée, sans label `eq:`. Mainteneur : « spécifiée » redéfinie (section proposée rédigée par `docwriter` et validée par l'expert pilote ; les labels font passer à « implémentée », § 4) ; fiche 1 « temps et comptabilité » passée à « spécifiée ». |
| 02/10/2026 | Mainteneur, point d'étape après la PR #29 : une issue par fiche, en quatre jalons (§ 4) ; fiches 2 à 6 réparties entre les branches n° 3a (fiche 2, issue #34) et n° 3b (fiches 3 à 6), `docs/feuille-de-route.md` § 2 ; ordre d'instruction inchangé. |
| 02/10/2026 | Fiche 2 « production et stocks » décidée (M24, branche n° 3a, PR #35) : option C, socle commun § 3.N à bien unique (J = 1) ; piste « deux secteurs » écartée ; ordre interne de la phase 4 « travail, puis production » (ADR 0007, accepté le 02/10/2026) ; Q4 (capital au bloc 2, emploi au bloc 3) à confirmer par les fiches 3 et 6 ; issue #37 créée (aucun levier d'offre au socle 3.N). Statut « spécifiée » attendu au jalon 4 de #34. |
