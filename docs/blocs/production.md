---
bloc: Production et stocks
module: src/nations/blocs/production.py
expert pilote: macro
experts consultés: jeu (lisibilité de la production, des stocks et du délai entre demande et production ; nombre de secteurs vu du joueur) ; monnaie non consulté (docs/blocs/README.md § 1)
statut: en instruction (critères validés par le mainteneur le 02/10/2026)
décision: —
issue: #34
---

# Fiche comparative — Production et stocks

> Fiche ouverte à partir du gabarit `0000-gabarit.md` (validé à l'usage, M20), sur le modèle de forme de la fiche 1 « temps et comptabilité » (M22). Jalon 1 de l'issue #34 : § 1 et § 2 seuls ; les rubriques suivantes portent « non instruit » jusqu'au jalon 2. Notation de la spécification après #23 (décision du mainteneur du 02/10/2026) : pays c, secteur productif j, intrant k.

Une fiche comparative instruit **l'origine de l'approche** d'un bloc (`docs/exigences.md` § 2.3) : la spécification v1.5, le moteur v2.0, ou une approche nouvelle. Elle est **instruite par l'expert pilote**, commentée par `jeu` et par l'expert consulté que désigne `README.md`, et **décidée par le mainteneur** (décision M24, reportée dans `docs/feuille-de-route.md`). Aucune approche n'entre dans le moteur ni dans la spécification sans cette décision. Les agents n'écrivent pas la fiche dans le dépôt : elle figure dans leur compte rendu et la session principale la commite.

Règles de rigueur (`CLAUDE.md`, « Rigueur ») : un chiffre se remesure ou cite sa source ; une équation de la v1.5 n'a jamais été garantie exécutée ; un comportement de la v2.0 ne vaut que sous son profil (état D1, **non versé** : aucun fait ne peut y être remesuré) et avec ses défauts connus ; chaque fait de la première tentative porte son **statut** S+O, O, R ou L (`CONTEXT.md`, « Statut d'un fait ») ; chaque référence est une publication retrouvée. Citer `archive/v1.5/…` avec numéro d'équation et section, ou avec le **numéro de ligne du `.tex`** ; `archive/v2.0/…` avec fichier et ligne. **Principe de simplicité** (adopté par le mainteneur le 30/09/2026) : à exigences comptables égales, l'option la plus simple pour le joueur et pour le moteur est préférée ; toute complexité se justifie par une identité qu'elle rend vérifiable ou par un mécanisme perçu à l'échelle d'une partie ; une simplification ne supprime ni une contrepartie comptable visible d'un levier ni une grandeur restituée au tour ; les identités, les tolérances relatives, le déterminisme, les invariants de l'ADR 0002 et la concordance ne se simplifient pas.

## 1. Question posée

*Rédigé par `macro` (expert pilote), 02/10/2026, sur la spécification à l'état `be1e2cc` (branche `claude/j1-cadre-production`).*

Le bloc porte le côté offre du socle : technique de production, production visée et réalisée, stocks de produits finis, et nombre de secteurs productifs (`docs/blocs/README.md` § 3, rang 2 ; `nations_et_marches.tex`, `sec:production`). Il débloque les fiches 3 (travail), 4 (prix) et 6 (investissement). Sous M22, un pas est un tour (n_a = 12, n_m = 1) : toute fenêtre exprimée en pas l'est aussi en tours.

### 1.1 Ce que le bloc doit produire

Symboles **non fixés** : ils le seront à l'instruction, sous le critère 13 (le symbole c est l'indice des pays). « u.v._j » désigne l'unité de volume du bien j, dont la normalisation est fixée à l'instruction.

| Grandeur | Définition | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| Production visée du secteur j | Volume que le secteur prévoit de produire dans le pas ; plan de la phase 2 | u.v._j par pas | — | le pas, phase 2 |
| Production du secteur j | Volume produit dans le pas | u.v._j par pas | — | le pas, phase 4 ; restitution : le tour, et la somme des 12 derniers tours |
| Ventes du secteur j | Volume livré dans le pas aux acheteurs (ménages, État, entreprises) ; les lignes 1 à 3 de `tab:matrice-flux` sont les ventes exécutées, en u.m. | u.v._j par pas | — | le pas, phase 5 |
| Demande non servie | Demande en volume adressée au secteur j au-delà du disponible (stock d'ouverture plus production du pas) ; grandeur restituée, pas un flux | u.v._j par pas ; ratio sans dimension | demande du pas | le pas, phase 5 |
| Stock de produits finis (volume) | Variable d'état du bloc (`sec:cadre`, encadré « portée » : le volume d'un actif réel est une variable du bloc qui le lit, non un poste) | u.v._j | — | ouverture du pas |
| Stocks IN (valeur) | Poste du cadre, tenu en valeur comptable, varié par la seule ligne 4 | u.m. | — | ouverture du pas |
| Variation des stocks ΔIN | Ligne 4 de `tab:matrice-flux` : valeur de la variation du volume des stocks, selon une règle de valorisation à déclarer | u.m. par pas | — | le pas, phase 5 |
| Ratio stocks / ventes | Stock d'ouverture en volume / ventes en volume du pas | mois de ventes | ventes du pas | ouverture et pas ; restitution : stock de clôture du tour / moyenne mensuelle des ventes des 12 derniers tours (forme de M22, lecture (e)) |
| Capacité de production (si l'option en a une) | Volume maximal du pas, compte tenu du volume du capital et de la technique | u.v._j par pas | — | le pas |
| Taux d'utilisation (si capacité) | Production / capacité | fraction | capacité du pas | le pas ; restitution : le tour |
| Demande de travail | Travail requis pour la production visée (transmis au bloc 3), puis emploi utilisé pour la production réalisée | personnes (ou heures) par pas | — | phases 2 et 4 |
| Productivité du travail | Production / emploi ; sa tendance de croissance si le bloc la porte | u.v._j par personne et par pas ; croissance en fraction par an | emploi du pas | le pas ; croissance en base annuelle |
| Coefficients d'intrants (si l'option en a) | Volume du bien k requis par unité du bien j | u.v._k / u.v._j | — | constants (paramètres) |
| PIB en volume (si J ≥ 2) | Agrégat des productions en volume ; méthode (prix de base fixes ou indice chaîné) à déclarer | indice ou u.m. de l'année de base | — | le tour ; 12 tours |

### 1.2 Ce qu'il lit

- **État d'ouverture** : ses variables d'état (stocks en volume, ventes anticipées s'il en tient, tendance de productivité) ; le volume du capital, dont la loi d'accumulation est partagée avec la fiche 6 (question Q4).
- **Phase 1** : prix et salaires décidés (blocs 4 et 3), leviers lus par le moteur.
- **Phase 4** : emploi effectif et salaires versés (bloc 3), écrits dans la même phase.
- **Phase 5** : demandes des ménages, de l'État et des entreprises (plans de la phase 2) et prix du pas.
- **Leviers du joueur** : aucun ne porte sur la production dans le socle, puisque le joueur ne produit pas, sauf en mode planifié, au J7 (`docs/exigences.md` § 2.1, point 1). Des leviers transitent par le bloc : dépense publique, impôts, taux par l'investissement.
- **Décisions qui le contraignent** :
  - M7 : économie fermée, donc la production nationale est la seule source de biens ;
  - M13 : budget de calcul ;
  - M22 : pas mensuel, conversion linéaire unique, condition λ ≤ n_a (l. 196), neuf phases, K et IN en valeur comptable sans ligne de réévaluation (l. 520) ;
  - décision du mainteneur du 02/10/2026 sur #23 : indices c, j, k.

### 1.3 Frontières

- **Travail et salaires (fiche 3)** : demande de travail (bloc 2) et emploi effectif (bloc 3). Les deux blocs écrivent en phase 4. Le bloc qui porte l'ajustement de l'emploi reste à proposer (Q4). Critères 8 et 11.
- **Prix (fiche 4)** : le bloc 2 fournit le versant volume du coût unitaire (travail et intrants par unité produite). Prix relatifs si J ≥ 2. Règle de valorisation des stocks, si elle passe par le coût unitaire. Critères 1 (b), 3 et 10.
- **Investissement et financement (fiche 6)** : volume du capital et capacité ; demande d'investissement ; amortissement (ligne 8, en valeur comptable) ; sous-colonnes des entreprises et profits non distribués (Q2). Critères 1, 2 et 3.
- **Ménages (fiche 5) et État et dette (fiche 9)** : demandes en valeur adressées aux biens, et, si J ≥ 2, leur composition par bien. Critères 7 (b) et 10 (e).
- **`jeu`** : critères 10 et 11 ; avis au § 7.
- **`monnaie`** : non consulté (`README.md` § 1). Le critère 3 (d) touche la question #24 (conversion des taux de croissance et des cibles), qui est à la frontière de `macro` et `monnaie` aux fiches 4 et 8.

### 1.4 Ce que la fiche ne tranche pas

- Les équations des fiches 3, 4 et 6 : formation des salaires et des prix, règle d'investissement, règle de dividendes et financement. En particulier, le choix entre rédaction « sous-colonnes réunies » et ligne « profits non distribués » relève de la fiche 6 (Q2).
- Les secteurs hors socle : énergie, alimentation, ressources (J5) ; construction et immobilier (J6) ; planification par entrées-sorties et nationalisation (J7). La fiche dit seulement comment un secteur s'ajoutera sans réécrire ce que M24 fixe (critère 10 (d)).
- Les valeurs numériques de l'état stationnaire et la calibration (J3) : la fiche vérifie qu'un calcul en forme fermée existe, elle ne le fait pas.
- Les bandes du test zéro (critère 6) : proposées ici, confirmées par le mainteneur avec les critères d'O1 avant l'essai du J3 (M19).

### 1.5 Questions ouvertes à instruire, non tranchées ici

- **Q1 — Nombre de secteurs productifs du socle** (piste « deux secteurs », feuille de route § 5). Question ouverte, tranchée par M24 seulement ; elle est mesurée par le critère 10, qui n'écarte aucune valeur de J d'avance. Faits relevés (L, 02/10/2026) :
  - la v2.0 a quatre secteurs : alimentation, énergie, biens de consommation, biens d'équipement (`archive/v2.0/prototype/model.py` l. 68) ;
  - la v1.5 propose sept secteurs et un secteur de ressources pour les pays dotés (`archive/v1.5/Nations_et_Marches_v1_5.tex` l. 391) ;
  - la mention de la feuille de route § 5 (« les quatre de la v1.5 et de la v2.0 ») est donc inexacte pour la v1.5.
- **Q2 — Sous-colonnes « Entr. courant » et « Entr. capital » (constat C1 de `macro`, validation de #25).**
  - *Relevé.* Relevé symbolique de `tab:matrice-flux` (`uv run python`, 02/10/2026, script ad hoc qui réutilise `lire_table` et `lire_termes` d'`outils/verifier_matrices.py`) : « Entr. courant » : +C +G +I +ΔIN −WB −T_F −δK/n_a −i_L L/n_a +i_D D_F/n_a −Div_F ; « Entr. capital » : −I −ΔIN +δK/n_a −ΔD_F +ΔL. Aucun terme ne se compense à l'intérieur d'une sous-colonne. Réunies, les deux sous-colonnes somment à zéro, ΔD_F étant le poste de règlement ; `verifier_matrices.py` les réunit (l. 129-131).
  - *Identité dérivée.* La somme de la sous-colonne courante est le résultat des entreprises après intérêts et impôts, moins les dividendes : les profits non distribués. Les lignes 3, 4 et 8 étant les seules variations de K et de IN (l. 520), cette somme est **exactement ΔV_F**. Contrôle en fractions exactes sur trois tirages (`uv run python`, 02/10/2026) : écart nul.
  - *Conséquence dérivée.* Sur une trajectoire où les ratios au PIB sont constants et où la croissance nominale annuelle γ est positive, V_F croît de γ/n_a par pas. La sous-colonne courante vaut alors (γ/n_a)·V_F par pas, non nulle dès que V_F ≠ 0. La phrase « Chaque colonne somme à zéro » (l. 291) et la légende de `tab:matrice-flux` (l. 303) ne sont donc vraies que sous-colonnes réunies, ce que dit la l. 295.
  - *Deux voies.* (i) Rédaction « sous-colonnes réunies » à la l. 291 et dans la légende, sans changer de table ; elle est vraie quelle que soit la décision ultérieure. (ii) Une ligne « profits non distribués » (courant −, capital +), qui rend chaque sous-colonne nulle ; les dividendes et les profits non distribués deviennent alors l'un un flux décidé, l'autre la clôture de la colonne courante ; c'est un flux du pas, non un poste, donc compatible avec « aucun poste obtenu par différence » ; cette voie modifie `tab:matrice-flux`, contrat partagé : décision citant M22.
  - *Rattachement.* Le choix dépend de la règle de distribution et de financement de l'investissement (autofinancement, demande de crédit) : il relève de la **fiche 6**. La fiche 2 n'en porte que la valorisation de ΔIN (ligne 4), qui entre dans le résultat courant : critère 2.
- **Q3 — Lettres des grandeurs réelles.** Le symbole c est l'indice des pays (l. 165 ; décision du 02/10/2026 sur #23) : aucune grandeur de production ou de consommation réelle ne s'écrit c. De même, k (intrant) et s (secteur institutionnel) sont pris. La consommation nominale reste C (ligne 1). Critère 13.
- **Q4 — Frontières de propriété.** La fiche 2 propose quel bloc tient le volume du capital (2 ou 6) et l'ajustement de l'emploi (2 ou 3) ; les fiches 3 et 6 confirment. Sous `sec:cadre` (l. 520), le volume d'un actif réel est une variable du bloc qui le lit.
- **Q5 — Ordre interne de la phase 2.** `tab:phases` ne déclare d'ordre interne que pour les phases 1, 5 et 7 (l. 486). Une production visée qui lirait un autre plan de la phase 2 exigerait une décision citant M22. Critère 8.
- **Q6 — Conversion d'un taux de croissance.** Un taux de croissance n'est aucune des trois natures de M22, lecture (a) (l. 194 ; #24). La fiche déclare comment elle convertit la croissance de la productivité ; l'harmonisation se fait avec #24. Critère 3 (d).

## 2. Critères d'évaluation, écrits avant l'instruction

**Statut : proposés par `macro` le 02/10/2026, validés tels quels par le mainteneur le même jour, avant toute instruction** (jalon 1 de #34). La liste est fermée : elle ne se déplace pas après observation (`docs/exigences.md` § 2.5). Un amendement adopté avant l'instruction est consigné sous le tableau.

Correspondance avec le gabarit :

| Critère du gabarit | Critère de la fiche |
|---|---|
| 1 | 1 |
| 2 | 3 et 4 |
| 3 | 5 |
| 4 | 9 |
| 5 | 11 |
| 6 | 7 et 12 |

Critères propres au bloc : 2, 6, 8, 10, 13, 14.

Sont des **exigences** (ils peuvent écarter une option) : 1, 3, 4, 5, 6, 7, 8, 9 (sans itération), 11 (b), 12 (sans historique ni drapeau), 13. Sont des **mesures** (elles décrivent sans écarter) : 2, 9 (décompte), 10, 11 (a), (c) et (d), 12 (décompte), 14.

| N° | Critère | Ce qui est attendu (seuil ou forme du verdict) | Par quoi on le vérifie | Qui | Quand |
|---|---|---|---|---|---|
| 1 | Cohérence stock-flux (gabarit 1, adapté ; `macro`) — **exigence** | (a) Tout flux proposé a une ligne nommée de `tab:matrice-flux`. Ventes et variation des stocks : lignes 1 à 4 ; une ligne nouvelle déclare sa phase et sa signature (ΔM, ΔH) au sens de `tab:portes-monnaie`. Il modifie des postes de `tab:matrice-bilans`. Aucune monnaie n'est créée hors d'une ligne. La colonne des entreprises, sous-colonnes réunies, somme à zéro, avec ΔD_F comme poste de règlement. (b) **Volume et valeur.** Chaque variable de volume du bloc (stocks ; capital s'il le lit) a une loi d'évolution déclarée. Sa contrepartie en valeur (IN, K) ne varie que par les lignes 3, 4 et 8 (l. 520). La règle qui donne ΔIN (u.m. par pas) à partir de la variation du volume est écrite : coût unitaire du pas, coût historique ou prix. Le rapport « valeur comptable / (prix courant × volume) » a une valeur stationnaire explicite. Une option qui exige une ligne de réévaluation le déclare : décision citant M22 (`docs/agents/routage.md` § 4.2). (c) Si l'option divise la colonne des entreprises par secteur j, chaque transaction entre secteurs (biens d'équipement, intrants k) a sa ligne, de somme nulle. Le niveau de consolidation est déclaré : bilan financier par j, ou bilan consolidé et comptes de production par j | Matrices de l'option écrites en tableaux dans la fiche. Si l'option modifie une table : `uv run python outils/verifier_matrices.py --strict <copie de la spécification portant les tables modifiées>`, décomptes et écarts cités. Calcul à la main de ΔIN sur un pas où prix et coûts varient | `macro` | fiche ; J3 (identités sur le moteur, ε = 1e−12 × S, M22) |
| 2 | Sous-colonnes des entreprises (`macro`, constat C1 ; § 1.5, Q2) — **mesure** ; la décision relève de la fiche 6 | Pour chaque option, la fiche donne en forme fermée la somme de chaque sous-colonne, sous ses propres définitions des lignes 3, 4 et 8, et sa valeur stationnaire en u.m. par pas et rapportée à V_F. Elle dit si ses flux font, à l'état stationnaire, des profits non distribués non nuls (attendu, si γ > 0 et V_F > 0 : environ (γ/n_a)·V_F par pas). Aucun flux de la fiche 2 ne présuppose l'issue : ni ligne de profits non distribués, ni rédaction « sous-colonnes réunies » | Relevé symbolique des termes de chaque sous-colonne, par la commande du § 1.5 appliquée aux tables de chaque option ; calcul à la main de la valeur stationnaire | `macro` | fiche |
| 3 | État stationnaire en forme fermée, croissance équilibrée (gabarit 2, adapté ; `macro`) — **exigence** | (a) Sur une trajectoire où les volumes croissent au taux annuel g et les prix au taux annuel π̄, chaque ratio du bloc a une valeur stationnaire en forme fermée. Elle se calcule à la main ou par le script d'état stationnaire d'`outils/` (critère de passage de J1, M19), sans simulation. Ratios concernés : stocks / ventes (mois de ventes), production / ventes, taux d'utilisation (si capacité), productivité rapportée à sa tendance, et, si J ≥ 2, prix relatifs et parts des secteurs dans la production en valeur. IN et ΔIN sont donnés explicitement sous π̄ > 0. (b) Chaque variable d'état du bloc a une valeur stationnaire explicite, d'où se déduit l'état initial résolu sans préparation (`docs/exigences.md` § 2.6). (c) Les ratios en base annuelle ne dépendent pas de n_a (fiche 1, critère 2 (c)). (d) La source de g est déclarée : tendance de productivité du bloc, population active des blocs 3 et 5. La conversion par pas d'un taux de croissance (l. 194 ; #24) est déclarée et son effet sur le taux annuel effectif est chiffré | Calcul à la main dans la fiche pour chaque option. Au J3, script contre moteur : un pas sans choc depuis l'état initial résolu laisse chaque variable d'état du bloc sur sa trajectoire stationnaire (croissance g/n_a, inflation π̄/n_a) à **1e−10 près en relatif** | `macro` | fiche ; J3 |
| 4 | Aucune vitesse d'ajustement ne détermine l'état d'arrivée (`docs/exigences.md` § 2.7 ; `macro`) — **exigence** | (a) Ni une vitesse d'ajustement (correction des stocks, lissage des ventes anticipées, ajustement de l'emploi ou de la capacité) ni la durée du pas n'apparaît dans les formes fermées du critère 3. Si l'une y apparaît (par exemple une extrapolation des ventes lissées à une croissance anticipée différente de la croissance réalisée), la fiche : écrit la dépendance ; la chiffre pour la vitesse divisée et multipliée par 2 ; dit la condition qui la supprime. Les règles de production visée des options A et B (v1.5 l. 519 ; v2.0 `model.py` l. 644) sont examinées sous ce critère. (b) Aucun intégrateur sans ancre : un état d'arrivée qui dépend du chemin (continuum d'équilibres) est documenté comme tel et soumis au mainteneur | Calcul à la main sur les formes fermées. Au J3, depuis l'état initial résolu : choc de demande temporaire, dépense publique +1 % pendant 12 tours ; deux branches où toutes les vitesses du bloc sont multipliées par 0,5 et par 2 (dans le domaine λ ≤ n_a). Écart relatif de chaque ratio du bloc entre les deux branches ≤ **1e−6 après 720 pas** | `macro` | fiche ; J3 |
| 5 | Stabilité (gabarit 3 ; `macro`) — **exigence** | (a) Aucune instabilité connue n'est réintroduite sans fait nouveau. Concernées, dans `archive/faits_mesures_G_K.md` § 6 : n° 1 (réponse au niveau d'un prix relatif : construction et p_Z/p_K, cycle de 3,5 ans) ; n° 9 (prix de l'équipement ×4,8 en 60 ans) ; n° 10 et 11 (dépréciation au prix lissé, ou indexée) ; n° 14 (règle de prix sans terme de demande : production d'équipement nulle, R) ; n° 15 (un plafond produit un cycle). Les hypothèses réfutées 1, 2 et 4 du § 7 ne sont pas reprises sans fait nouveau. (b) Boucle propre du bloc (production visée, production, stocks, ventes anticipées), demande exogène constante, au pas mensuel : la récurrence linéarisée autour de l'état stationnaire a toutes ses valeurs propres de module **strictement inférieur à 1**, pour la calibration proposée et pour chaque vitesse multipliée par 0,5 et par 2. La fiche donne le module, la demi-vie en tours et, si les racines sont complexes, la période du cycle des stocks en tours | Liste du § 6, puis `tab:instabilites` ; instabilités concernées pour chaque option. Valeurs propres calculées à la main ou par `uv run python`, commande et sortie citées | `macro` | fiche ; J3 (critère 6) |
| 6 | Test zéro des ratios du bloc (`docs/exigences.md` § 2.6 ; O1 ; `macro`) — **exigence**, mesurée au J3 | Sur 60 ans (720 pas) sans choc depuis l'état initial résolu, pour plusieurs graines, la moyenne par blocs de 5 ans (60 pas) de chaque ratio du bloc reste dans sa bande autour de la valeur stationnaire résolue. **Bandes proposées**, à confirmer par le mainteneur avec O1 avant l'essai (M19) : stocks / ventes (stock d'ouverture / ventes du pas) ±10 % ; taux d'utilisation ±0,02 ; prix relatif de chaque secteur au prix de la consommation (si J ≥ 2) ±10 %. Pour mémoire, la v2.0 depuis D1 présente une dérive rapportée de 12,8 % du prix de l'équipement relatif à la consommation (R, faits § 2). K/Y relève d'O1 et de la fiche 6. Une transition n'est pas un état stationnaire : toute dérive depuis l'état résolu est un défaut | Au stade de la fiche, seul le préalable (critère 3) se vérifie ; au J3, test zéro du socle | `macro` ; mainteneur (bandes) | J3 |
| 7 | Bornes et rationnement des biens (gabarit 6 ; `docs/exigences.md` § 2.7 ; `macro`) — **exigence** | (a) Toute borne (min, max, plancher, plafond, écrêtage) est déclarée avec son paramètre et motivée contre un mécanisme. La fiche dit lesquelles sont actives à l'état stationnaire : une borne active y fixe l'état d'arrivée et doit être justifiée. Une technique à coefficients fixes est déclarée comme telle. (b) Disponibilité : ventes du pas ≤ stock d'ouverture + production du pas ; aucun stock négatif. La demande excédentaire est rationnée selon un ordre de priorité déclaré entre ménages, État et entreprises ; les lignes 1 à 3 sont les ventes exécutées. La demande non servie est restituée, ce n'est pas un flux | Décompte des bornes par option. Cas à la main : demande excédant le disponible de 10 %, avec les flux et les stocks du pas | `macro` | fiche ; J3 (test) |
| 8 | Phases et lectures (fiche 1, critère 12 (a) ; `tab:phases` ; `macro`) — **exigence** | Les calculs se placent dans les phases de `tab:phases` : 2 pour la production visée et la demande de travail ; 4 pour la production, l'emploi et les stocks ; 5 pour les ventes et la variation des stocks. Ils ne lisent que l'ouverture, la phase 1 ou une phase antérieure. La phase 2 n'a pas d'ordre interne déclaré (l. 486). Lire un autre plan de la phase 2 (consommation, dépense publique, investissement visé) exige donc d'en déclarer un, ce qui modifie un contrat partagé et demande une décision citant M22 ; la fiche le dit pour chaque option. Aucune résolution simultanée | Tableau phase → lit / écrit par option ; triangularité vérifiée à la main | `macro` | fiche ; J2 et J3 |
| 9 | Coût de calcul (gabarit 4 ; `macro`) — **exigence** (aucune itération) et **mesure** (décompte) | Aucune itération ni optimisation à chaque pas (ADR 0002). Un système linéaire à coefficients constants (inverse de Leontief) se résout au chargement. Décompte des opérations par pas en fonction de J et du nombre d'intrants. Budget du socle : 52/12 ≈ 4,333 ms par pays-pas (M13, M22). **Part indicative proposée** : (52/12 − 0,5)/8 ≈ 0,48 ms pour le bloc, soit le budget restant après le noyau (0,5 ms, J2) réparti entre les huit blocs de comportement | Décompte dans la fiche ; au J3, `tests/invariants/test_budget.py` sur le socle complet (52/12 semaines par pas) | `macro` ; `audit` | fiche (décompte) ; J3 (mesure) |
| 10 | Nombre de secteurs productifs du socle (feuille de route § 5 ; § 1.5, Q1 ; `macro`) — **mesure** : aucune valeur de J n'écarte une option d'avance | Instruit au moins pour J = 1 (bien unique), J = 2 (consommation, équipement), J = 4 (v2.0) et la liste de la v1.5 (sept secteurs et ressources). (a) Ce que chaque secteur ajoute : identité rendue vérifiable ou mécanisme perçu à l'échelle d'une partie. (b) Ce qu'il coûte : paramètres ; variables d'état ; J − 1 prix relatifs à rendre stationnaires (critères 3 et 6) ; lignes ou sous-colonnes ; instabilités liées à l'équipement (critère 5). (c) Définition du PIB en volume pour J ≥ 2 (prix de base fixes ou indice chaîné), avec unité, base et fenêtre. (d) Extensibilité : comment un secteur s'ajoute aux jalons J5 (biens échangeables, ressources), J6 (construction) et J7 (planification par entrées-sorties, v1.5 l. 1585) sans réécrire M24. (e) Leviers du socle dont la portée change avec J (composition de la dépense publique par bien) | Tableau par option et par valeur de J ; avis de `jeu` sur la lisibilité de chaque secteur | `macro` ; `jeu` | fiche |
| 11 | Lisibilité pour le joueur (gabarit 5 ; `macro`, à soumettre à `jeu` au jalon 2) — **exigence** pour (b), **mesure** pour (a), (c), (d) | (a) Indicateurs restitués au tour : production (volume ; indice si J ≥ 2), taux d'utilisation, stocks en mois de ventes, demande non servie, emploi (avec le bloc 3). Chacun avec définition, unité, dénominateur et fenêtre : le tour, et 12 tours pour un ratio annuel (forme de M22, lecture (e)). (b) Délai, en tours entiers, entre une variation de la demande et la réponse de la production, puis de l'emploi. La contrepartie comptable est visible le même tour : baisse des stocks ou demande non servie. Aucun effet plus rapide que le tour sans contrepartie. (c) Le bloc n'ouvre aucun levier du socle (`docs/exigences.md` § 2.1, point 1). Tableau levier → indicateur → délai en tours → contrepartie pour les leviers qui transitent par lui : dépense publique, impôts, taux par l'investissement. (d) Ampleur de la réponse et période du cycle des stocks en tours (critère 5 (b)), perceptibles sur une partie de 60 à 120 tours | Tableau du § 9, « Interfaces » ; exemple daté à la main (choc de demande au tour n) ; avis de `jeu` (§ 7) ; au J4, scénario apparié (O2) | `jeu` ; `macro` (exemple daté) | fiche ; J4 |
| 12 | Simplicité, empreinte sur l'état, déterminisme (gabarit 6 et rubrique 9 ; `macro`) — **mesure** (décompte) et **exigence** (sans historique ni drapeau) | Décompte par option : paramètres, bornes, variables d'état, lignes et sous-colonnes ajoutées, phases touchées, secteurs ; chaque élément justifié par une identité vérifiable ou un mécanisme perçu. Exigences : chaque variable d'état a son unité et sa valeur stationnaire (critère 3 (b)). Aucune moyenne glissante qui exigerait un historique : un lissage exponentiel est une variable d'état ; un registre de longueur fixe se déclare comme celui des prix (`sec:cadre-calendrier`). Une seule règle par mécanisme, aucun drapeau de mode (ADR 0002). Aucun tirage aléatoire, ou un tirage par la graine du pays, déclaré | Tableau de décompte ; liste des variables d'état avec unité et valeur stationnaire | `macro` | fiche ; J2 (reprise exacte) |
| 13 | Notation (`CONVENTIONS.md` § 5.2 ; décision du mainteneur du 02/10/2026 sur #23 ; § 1.5, Q3) — **exigence** | Chaque symbole proposé a un seul sens. Il n'entre en collision ni avec les indices réservés (pays c, secteur productif j, intrant k, strate h, pas t ; s, ℓ, u du cadre), ni avec un symbole de `tab:symboles`. Aucune grandeur de production ou de consommation réelle ne s'écrit c. Une convention « minuscule = volume » est inapplicable telle quelle pour c, k et s. Les majuscules du cadre (C, G, I, K, IN, WB, T, Tr, D, L, B, M, H, S, V, E, P) gardent leur sens | Liste des symboles proposés confrontée à `tab:symboles` (commande `grep` et sortie citées dans la fiche) | `macro` ; `docwriter` (section) | fiche ; section proposée |
| 14 | Calibrabilité et faits établis (`macro`) — **mesure** | Les paramètres de l'option se calibrent sur des ordres de grandeur établis : ratio stocks / ventes, taux d'utilisation des capacités, part salariale, K/Y. Chacun porte sa source retrouvée et sa date. Un résultat de la v1.5 ou de la v2.0 n'est pas un fait établi. Une source introuvable est déclarée comme telle | Sources citées dans la fiche ; mention « non trouvée » le cas échéant | `macro` | fiche ; J3 (calibration) |

### Décisions du mainteneur sur les critères (02/10/2026, avant l'instruction)

- Les 14 critères sont validés tels quels, avec leur nature (exigence ou mesure).
- Seuils adoptés : critère 3 (pas stationnaire à 1e−10 près en relatif, J3) ; critère 4 (écart ≤ 1e−6 après 720 pas entre les branches à vitesses ×0,5 et ×2, J3) ; critère 9 (part indicative de 0,48 ms par pays-pas pour le bloc). Les bandes du critère 6 restent **proposées** : elles sont confirmées avec O1 avant l'essai du J3 (M19).
- Q1 : J est une mesure ; l'instruction couvre J = 1, J = 2, J = 4 (v2.0) et la liste de la v1.5 (sept secteurs et ressources).
- Q2 (constat C1) : le choix de fond (ligne de profits non distribués ou non) relève de la fiche 6 ; la rédaction « sous-colonnes réunies » de `sec:cadre-flux` est corrigée dès maintenant, par une issue ajoutée au périmètre de la branche n° 3a.
- Q4 : la fiche 2 propose quel bloc tient le volume du capital et l'ajustement de l'emploi ; les fiches 3 et 6 confirment.
- Q5 : une option qui exige un ordre interne de la phase 2 reste instruite, au prix d'une décision citant M22.

### Amendements adoptés

Aucun à ce jour.

## 3. Options

Non instruit (jalon 2 de #34).

## 4. Tableau comparatif

Non instruit.

## 5. Avis de l'expert pilote

Non instruit.

## 6. Avis de l'expert consulté

Sans objet, parce que `docs/blocs/README.md` § 1 ne désigne pour ce bloc aucun expert de fond consulté (`monnaie` non consulté) ; l'avis de `jeu` figure au § 7.

## 7. Avis de `jeu`

Non instruit (jalon 2 de #34).

## 8. Décision du mainteneur

Sans objet avant l'instruction : décision M24 attendue au jalon 3 de #34.

## 9. Conséquences de la décision

Non instruit.

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 02/10/2026 | Ouverture (issue #34) ; § 1 et § 2 proposés | `macro` ; session principale |
| 02/10/2026 | Critères validés tels quels ; seuils des critères 3, 4 et 9 adoptés ; bandes du critère 6 renvoyées au J3 (issue #34) | mainteneur |
| | Instruction déposée (§ 3 à 5) | `macro` |
| | Avis de `jeu` (§ 7) | `jeu` |
| | Constats intégrés ; statut « avis rendus » | `macro` ; session principale |
| | Décision M24 | mainteneur |
