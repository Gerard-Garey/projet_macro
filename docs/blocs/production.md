---
bloc: Production et stocks
module: src/nations/blocs/production.py
expert pilote: macro
experts consultés: jeu (lisibilité de la production, des stocks et du délai entre demande et production ; nombre de secteurs vu du joueur) ; monnaie non consulté (docs/blocs/README.md § 1)
statut: spécifiée (03/10/2026)
décision: M24 (02/10/2026)
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

- **Amendement de notation (03/10/2026, visa du mainteneur)** : dans le critère 3 et au § 9.6, « prix au taux annuel π̄ » et « inflation π̄/n_a » se lisent « prix en hausse de (1 + π̄)^{1/n_a} − 1 par pas », π̄ étant le glissement annuel stationnaire de `sec:cadre-calendrier`. Seuils inchangés ; aucun verdict antérieur. Origine : validation de fond de `sec:production` par `macro`.

## 3. Options

*Instruit par `macro` (expert pilote), 02/10/2026 (issue #34), sur la fiche à la tête `7a4e99c` (branche `claude/j1-cadre-production`). Les critères du § 2 et les décisions du mainteneur sur Q1, Q2, Q4 et Q5 sont lus tels que validés ; aucun n'est déplacé. Pour Q2, la fiche ne présuppose ni la ligne « profits non distribués » ni la rédaction « sous-colonnes réunies » ; la rédaction de `sec:cadre-flux` est corrigée par #36 et le fond relève de la fiche 6.*

**Découpage par question.**
- Les options A (v1.5) et B (v2.0) sont instruites en entier, en neuf rubriques chacune.
- Les options nouvelles partagent un socle commun « v3 proposé » (§ 3.N) : technique, production visée, ventes et rationnement, stocks et leur valorisation, volume du capital, phases, notation. Ce socle est écrit pour J secteurs (indice j).
- C et D ne diffèrent que par le nombre de secteurs : C est le bien unique (J = 1), D la piste « deux secteurs » (consommation et équipement, J = 2).
- J = 4 (v2.0) est instruit dans B, et la liste de la v1.5 (sept secteurs et des ressources) dans A. Toutes les valeurs de J sont comparées au § 3.J (critère 10).

**Notation employée au § 3.** Les options A et B gardent leurs symboles d'origine (Ŷ, Q̄, S^inv, Sinv…). Le socle 3.N emploie la notation proposée au critère 13 (§ 3.N-7) :
- volumes : X^vol pour le volume d'une grandeur nominale du cadre (IN^vol, K^vol, C^vol, G^vol, I^vol) ;
- y : production ; y* : production visée ; v : ventes ; v^e : ventes anticipées ; d : demande adressée ;
- pr : productivité du travail ; tu : taux d'utilisation ; N* : demande de travail ;
- UC : coût unitaire des entrées en stock ; cm : coût moyen des stocks.

**Mesures.** Toutes ont été exécutées le 02/10/2026 par `uv run --project /home/user/projet_macro python <script>`. Les scripts sont des scripts de travail, hors dépôt, rangés dans le scratchpad de la session (`…/scratchpad/p2/`). Chaque résultat est aussi donné en forme fermée dans le texte, donc recalculable à la main.

| N° | Script | Ce qu'il calcule | Résultats principaux |
|---|---|---|---|
| M1 | `ss_ab.py` | Ratio stocks / ventes stationnaire sous la règle de production visée de A et de B, en forme fermée et par simulation de 20 000 pas ; vitesses ×1, ×0,5, ×2 | 3.A-3, 3.B-3 |
| M2 | `vp.py` | Valeurs propres de la boucle production – stocks – emploi de A et de B (pas hebdomadaire natif, puis transposition mensuelle) | 3.A-8, 3.B-8 ; aussi la boucle de Metzler du socle |
| M3 | `vp_c.py` | Valeurs propres du socle 3.N, demande exogène | 3.N-8 |
| M4 | `met.py`, `frontiere.py` et une commande en ligne | Socle avec demande induite (complément hors critère) : simulation d'impulsion, frontière de stabilité, variante avec ajustement partiel de l'emploi | 3.N-8 |
| M5 | `exemple.py` | Exemple daté : dépense publique +1 % pendant 12 tours | 3.N-8, critère 11 |
| M6 | `valo.py` | Valorisation des stocks sur un pas où prix et coûts varient ; rapports stationnaires ρ̄_IN et ρ̄_K ; vérification par simulation | 3.N-4 |
| M7 | commande en ligne | Dépendance de ρ̄_IN et ρ̄_K à n_a | 3.N-4 |
| M8 | `cout.py` | Maquette du socle 3.N en Python pur, coût d'un pas pour J = 1, 2, 4, 8 | 3.N-11 |
| M9 | commande en ligne | Cas à la main : demande supérieure de 10 % au disponible | 3.N-3 |
| M10 | commande en ligne | Règle de Godley et Lavoie « littérale » sous croissance ; contre-épreuve du socle | 3.N-2 |
| M11 | `grep` | Collisions des symboles proposés dans la spécification | 3.N-7 |

**Lignes d'archive relues (statut L, 02/10/2026).**
- `archive/v1.5/Nations_et_Marches_v1_5.tex` : l. 388–432, 488–489, 494–601, 739–775, 1585–1616, 2008–2081, 2239–2376.
- `archive/v2.0/prototype/model.py` : l. 35–38, 64–141, 241, 250, 268, 436–493, 601–700, 866, 915–1022, 1075–1079, 1418, 1707–1709, 1718–1719, 1956.

**Faits de la première tentative cités.**
- G1 et G1b (S+O).
- D1 sur 60 ans (R).
- Instabilités n° 1, 9 à 11, 14 et 15 (R, avec S+O pour la 14) et hypothèses réfutées n° 1, 2 et 4 (`archive/faits_mesures_G_K.md` § 6 et 7).
- Acquis du § 8 (R).

**Littérature.** Le proxy a refusé l'accès, le 02/10/2026, à `models.sfc-models.net`, `joaomacalos.github.io`, `iasplus.com`, `cpdbox.com`, `fred.stlouisfed.org`, `federalreserve.gov`, `www2.census.gov`, `rug.nl` et `unstats.un.org`.

| Source | Ce qui a été lu | Ce qu'elle soutient |
|---|---|---|
| Godley et Lavoie, *Monetary Economics*, 2007, chap. 9, « A Model with Private Bank Money, Inventories and Inflation » | Titre retrouvé (Springer, lien de chapitre). **Texte du livre non lu.** Équations du modèle DIS lues dans deux reproductions secondaires concordantes : la vignette `vignettes/articles/gl6-dis.Rmd` du paquet R `sfcr` (J. Macalós, dépôt GitHub `joaomacalos/sfcr`, lue par `raw.githubusercontent.com`) et `DIS.py` du dépôt GitHub `RWGreber3/Monetary-Economics` | y = s^e + in^e − in_{−1} ; in^T = σ^T s^e (`DIS.py` assoit la cible sur s) ; in^e = in_{−1} + γ(in^T − in_{−1}) ; s^e = β s_{−1} + (1−β) s^e_{−1} ; N = y/pr ; UC = WB/y ; IN = in·UC ; EF = S − WB + ΔIN − r_{l,−1} IN_{−1} ; paramètres de `sfcr` : β = 0,75, γ = 0,25, σ^T = 0,15. **À vérifier sur le livre** |
| L. A. Metzler, « The Nature and Stability of Inventory Cycles », *Review of Economics and Statistics* 23 (1941), 113–129, DOI 10.2307/1927555 | Référence retrouvée, texte non lu | Origine usuelle du cycle des stocks (attribution par la littérature secondaire) |
| A. S. Blinder et L. J. Maccini, « Taking Stock: A Critical Assessment of Recent Research on Inventories », *Journal of Economic Perspectives* 5(1) (1991), 73–96 | Référence retrouvée ; résumé secondaire seul | Dans les données agrégées, la production est plus variable que les ventes (accélérateur des stocks). Texte non lu |
| IAS 2 « Stocks », § 25 | Résumés secondaires (résultats de recherche) ; texte de la norme non lu | Premier entré, premier sorti, ou coût moyen pondéré ; dernier entré, premier sorti exclu depuis la révision de 2003 |
| SCN 2008, chap. 15 | Extrait de recherche ; texte non lu | Indices de volume chaînés annuellement, de type Laspeyres |
| Faits de calibration | Extraits de recherche ; sources primaires non lues | Voir § 3.N-12 |

Conclusion sur la littérature :
- La littérature retrouvée soutient la forme « production = ventes anticipées + correction des stocks ; emploi = production / productivité ; stocks valorisés au coût » (Godley et Lavoie, par reproductions) et l'existence d'un cycle des stocks (Metzler, titre).
- Elle ne permet pas de conclure sur des valeurs canoniques des vitesses.
- Elle ne tranche pas entre une valorisation au coût unitaire courant (Godley et Lavoie) et une valorisation au coût moyen pondéré (norme comptable).

### 3.A Option A — v1.5

1. **Source exacte.** `archive/v1.5/Nations_et_Marches_v1_5.tex` :
   - entités et secteurs, l. 388–391 ; bilan des entreprises (stocks S^inv_j en volume), l. 412 ; ordre d'un tick, l. 422–432 ; règles de caisse et bornes, l. 488–489 ;
   - § « Secteur productif » : `eq:prod`, l. 500–504 ; commande d'intrants, l. 513 ; production visée, l. 517–527 ; `eq:labour`, l. 528–541 ; `eq:profit` et trésorerie, l. 545–549 ; accumulation, l. 584 ; `eq:tfp`, l. 590–594 ;
   - § « Marchés » : agrégation, l. 741–745 ; rationnement et loi des stocks, l. 771 ;
   - planification, l. 1585–1598 ;
   - prototype, l. 2011, 2013–2033, 2074, 2080 ;
   - calibration, l. 2261, 2323, 2327, 2376.
2. **Équations** (pas hebdomadaire ; statut proposé entre crochets).
   - **Capacité et production** (l. 501–502) [choix de conception] : Y^cap_j = A_j K_j^{α_j} (H L_j)^{1−α_j} et Y_j = Y^cap_j · min(1, min_k X^obt_kj/(a_kj Y^cap_j)). La part du capital α_j vaut 0,30 à 0,40 (l. 2251). La capacité est calculée sur l'**emploi courant**.
   - **Commande d'intrants** (l. 513) [approchée] : X^dem_kj = a_kj Ŷ_j + λ_S (s* a_kj Ŷ_j − S^inv_kj). Les secteurs tiennent des stocks d'intrants.
   - **Production visée** (l. 519–520) [approchée] : Ŷ_{j,t} = Q̄_{j,t}(1 + g^e) + λ_inv (s*_j Q̄_{j,t} − S^inv_{j,t}), avec Q̄_{j,t} = (1 − μ) Q̄_{j,t−1} + μ Q_{j,t−1}. Le stock cible s* vaut 4 semaines (l. 2323). μ, λ_inv, λ_S et g^e sont « fixés en dur » (l. 2376) : **leurs valeurs ne figurent pas dans le texte**.
   - **Demande de travail** (l. 530–532) [approchée] : L*_j = min{(Ŷ_j/(A_j K_j^α H^{1−α}))^{1/(1−α)}, (1−α) p_j Ŷ_j/(W_j(1+τ_S))}, puis L_{j,t+1} = L_{j,t} + λ_L (L* − L). λ_L vaut 0,25 par semaine (l. 2261), et λ_L/2 pour l'équipement (l. 2327).
   - **Marché** (l. 744, 771) [choix de conception] : S_j = Y_j + λ_S S^inv_j + IM_j et Q_j = min(D_j, S_j). La demande excédentaire est rationnée proportionnellement, au taux S/D, avec une priorité possible à l'État ou aux intrants en mode planifié. Si S > D, la loi des stocks est S^inv_{t+1} = S^inv_t + (S_j − Q_j).
   - **Profit** (l. 545) : Π_j = p_j Q_j − W(1+τ_S) L − Σ_k p_k X^obt_kj − δ p_K K − i L − τ_Π (·)^+. Il ne contient **aucune variation de stocks**, et l'amortissement est compté au prix courant p_K.
   - **Accumulation et productivité** : K_{t+1} = (1 − δ) K + I, livré avec T_K mois de retard (l. 584). La croissance de la productivité g_0 s'augmente de la R&D, du capital public, du rattrapage, d'une pénalité de planification et d'un choc AR(1) (l. 592).
   - **Secteurs** : sept plus les ressources (l. 391). Le prototype n'en a que **quatre** (l. 2011, R).
3. **État stationnaire impliqué.** Calcul à la main, en croissance équilibrée au taux γ par pas, avec Y = Ŷ. Le volume Q̄ retarde sur Q d'un facteur κ = μ/(μ + γ), d'où :
   - S/Q = [κ(1 + g^e + λ_inv s*) − 1]/(γ + λ_inv) ;
   - avec g^e = γ : S/Q = [λ_inv s* μ − γ(1 − μ)]/[(μ + γ)(γ + λ_inv)], qui ne vaut s* que si γ = 0.

   Chiffres (M1), avec les valeurs μ = 0,10 et λ = 0,03 par semaine lues dans le code v2.0 (l. 111–113, branche hors `wsps2`) faute de valeurs v1.5 (**hypothèse**), et g^e = γ = 1,9 % par an (état stationnaire du prototype, l. 2019, R) :

   | Pas | Nominal | μ ×0,5 | μ ×2 | λ ×0,5 | λ ×2 |
   |---|---|---|---|---|---|
   | Hebdomadaire | 3,8296 semaines (−4,26 % de s*) | −7,59 % | −2,58 % | −8,06 % | −2,32 % |
   | Mensuel (conversion linéaire) | 0,8930 mois (−3,26 %) | −6,60 % | −1,58 % | −6,09 % | −1,82 % |

   - **Taux d'utilisation.** Il est dégénéré : la capacité étant calculée sur l'emploi courant, Ŷ/Y^cap tend vers 1 à l'état stationnaire quand L_tech est la borne qui lie. Le taux de 0,93 rapporté (l. 581, R) n'est pas reproductible depuis le texte : non calculable.
   - **Productivité.** Y/L = A^{1/(1−α)} (K/Y)^{α/(1−α)} H : forme fermée conditionnelle à K/Y (fiche 6).
   - **État initial.** Le texte prévoit un « transitoire initial de trois à cinq ans » et des parties démarrant « sur un état sauvegardé après dix ans de simulation » (l. 2080, R) : **pas d'état initial résolu**.
4. **Comportement mesuré.** Non mesuré : aucune équation de la v1.5 n'a été garantie exécutée. Faits rapportés (R) :
   - le prototype a quatre biens (l. 2011) ;
   - « les entreprises servent les commandes et ajustent leurs capacités ; le tâtonnement ne voit presque jamais d'excès de demande » (l. 2074) ;
   - le transitoire initial dure de trois à cinq ans (l. 2080).
5. **Coût de calcul.** J = 8 (sept secteurs et les ressources) au pas hebdomadaire.
   - Par tick : une inversion de la fonction de production par secteur (puissance) ; un minimum sur les intrants (64 coefficients) ; les stocks d'intrants.
   - Aucune itération ; l'inverse de Leontief ne sert qu'à la planification (l. 1589).
   - Ordre de grandeur : une centaine d'opérations par tick. Non mesuré ; non discriminant (voir 3.N-11).
6. **Défauts connus et instabilités documentées.**
   - **(i) Loi des stocks non conservatrice telle qu'écrite.** Avec S = Y + λ_S S^inv + IM (l. 744) et S^inv_{t+1} = S^inv_t + (S − Q) (l. 771), on obtient S^inv_{t+1} − S^inv_t − (Y + IM − Q) = λ_S S^inv_t > 0 : le texte **crée λ_S S^inv_t par tick** quand S > D. Le cas D > S n'est pas écrit. La lecture cohérente (retrait de la part offerte) ne figure pas dans le texte ; la v2.0 l'écrit correctement (`model.py` l. 1000) (L, calcul).
   - **(ii) Valorisation des stocks non définie.** Le profit ne contient pas de ΔIN (l. 545) et le bilan porte S^inv en volume (l. 412). Le critère 1 (b) ne peut être satisfait.
   - **(iii) Une vitesse détermine l'état d'arrivée** (rubrique 3).
   - **(iv) λ_L = 0,25 par semaine, soit 13 par an, dépasse n_a = 12.** La valeur n'est pas transposable au pas mensuel sous la condition λ ≤ n_a (`sec:cadre` l. 196) : en transposition, une valeur propre vaut −0,0956 (alternance) (M2).
   - **(v) Bornes** :
     - min(L_tech, L_prof) (l. 530) ;
     - contrainte de caisse sur la masse salariale, v(π^e)(M_j + ½ p_j Q_j) (l. 488) ;
     - vitesse saturée à π^e = 1 (l. 488–489) ;
     - « commandes suivies ≤ 1,1 × offre » (l. 2323) ;
     - Leontief des intrants (technique).
   - **(vi) Instabilités concernées** : n° 1 (construction et rapport p_Z/p_K, secteur prévu à la l. 391) ; n° 9 à 11 et 14 (prix relatif et amortissement de l'équipement au prix p_K, l. 545) ; n° 15 (plafonds de (v)). Les hypothèses réfutées n° 1, 2 et 4 portent sur la même zone.
   - **(vii) Aléa** : choc AR(1) de productivité (l. 601) et aléa climatique (l. 838).
7. **Identités de bilan touchées.**
   - Bilan des entreprises par secteur j : trésorerie M_j, capital p_K K_j au prix courant, stocks S^inv_j, dette L_j (l. 412).
   - Pas de matrice des flux (fiche 1, 3.A-2).
   - L'amortissement et le capital au prix courant (l. 545) supposent une réévaluation implicite, contraire à `sec:cadre` l. 520 sans ligne de réévaluation.
   - Les intrants sont échangés entre secteurs (−Σ p_k X^obt) ; ces échanges disparaissent en colonne consolidée.
   - **Critère 2 (sous-colonnes)** : l'équation de trésorerie (l. 546), M_{t+1} = M + Π − Div − p_K I + ΔL + Sub, donne une sous-colonne « courant » égale à Π − Div + Sub. Comme Π exclut ΔIN, ce n'est pas la sous-colonne du cadre, et sa valeur stationnaire n'est pas calculable (ΔIN non défini).
   - Aucune ligne ne fait varier M ou H dans ce bloc.
8. **Ce que le joueur en percevrait.**
   - Un tick hebdomadaire, contraire à M22.
   - La production suit la demande par l'emploi. Les valeurs propres sont réelles (M2, hebdomadaire : 0,9665, 0,9 et 0,776), donc sans cycle propre ; demi-vie de 4,7 mois (2,4 mois et 9,3 mois pour les vitesses ×2 et ×0,5).
   - Une pénurie se traduit par un rationnement proportionnel.
   - Le taux d'utilisation est dégénéré (proche de 1), donc inutilisable comme signal.
   - Huit secteurs : l'énergie, l'alimentation et la construction relèvent des jalons J5 et J6.
9. **Empreinte sur l'état.**
   - Par secteur : Q̄_j, S^inv_j, L_j, K_j et A_j, plus J² stocks d'intrants S^inv_kj ; s'y ajoutent H, la terre T et le stock de ressource. Pour J = 8 : 5 × 8 + 64 + 3 = 107 variables.
   - Un registre de livraisons de T_K mois (l. 584).
   - La moyenne mobile Q̄ est une variable d'état (lissage exponentiel), pas un historique.

### 3.B Option B — v2.0

1. **Source exacte.** `archive/v2.0/prototype/model.py` :
   - secteurs, l. 68 ; `nsec`, α, δ, l. 99–101 ; matrice a des coefficients techniques, l. 103–106 ; g0, l. 109 ;
   - `mu_ema`, `s_star`, `lam_inv`, `lam_L`, l. 111–114 ; `wsps2`, l. 129 ; `phi_S`, `lam_inv_2`, `lam_L_2`, l. 139–141 ; `order_cap`, l. 241 ; `lam_L_sec`, l. 268 ;
   - état initial, l. 446–449, 491, 493 ;
   - capacité, l. 637 et 673 ; production visée et plancher, l. 644–645 ; intrants, l. 647–650 ; travail, l. 652–669 ; production, l. 676–680 ; utilisation, l. 866 ;
   - offre, stocks et ventes, l. 923–924, 946–951, 1000 ; capital, l. 1002 ;
   - valorisation et profit, l. 1019–1022 ; amortissement lissé, l. 1075 ; moyenne des commandes, l. 1418 ; valeur comptable, l. 1707–1709 ; `solve_init`, l. 1956.

   Faits : § 1.1, § 2 (G1, S+O ; D1, R), § 6 et 7 d'`archive/faits_mesures_G_K.md`.
2. **Équations** (pas hebdomadaire ; statut proposé : approchée ou choix de conception).
   - **Capacité et production.** Y^cap = A_eff K^α (H L)^{1−α}, sur l'emploi courant (l. 673). Y = Y^cap · thr, avec thr = clip(min_k X_kj/(a_kj Y^cap), 0, 1) (l. 679–680).
   - **Production visée.** Ŷ = Q̄ (1 + g0/52) + λ_inv2 (s* Q̄ − Sinv) (l. 644), avec le plancher Ŷ ≥ 0,05 Y^cap (l. 645).
     - g0 = 0,015 est la croissance de la productivité globale des facteurs (l. 109) ; s* = 4 semaines (l. 112) ; λ_inv2 = 0,02 par semaine (l. 140, actif puisque `wsps2 = True`, l. 129).
   - **Travail.**
     - L_tech = (Ŷ/(A K^α H^{1−α}))^{1/(1−α)} (l. 652) ; L_prof est le produit marginal en valeur ajoutée (l. 653–659) ; L* = min(L_tech, L_prof, L_cash) (l. 660, 665).
     - L'emploi est plafonné à 0,98 de la population active privée (l. 668).
     - Ajustement : L_{t+1} = L + λ_L2 · λ_L_sec · (L* − L) (l. 669), avec λ_L2 = 0,04 par semaine (l. 141) et λ_L_sec = 1, ou 0,5 pour l'équipement (l. 268).
   - **Offre et ventes.** excess = max(Sinv − s* Q̄, 0) (l. 923, 946), puis S = Y + φ_S · excess avec φ_S = 0,10 par semaine (l. 139, 924, 947). Ensuite Q = min(D, S) (l. 948) ; les exportations sont servies en premier (l. 949), puis la demande intérieure au prorata (l. 951).
   - **Stocks** : Sinv_{t+1} = Sinv + Y − Q (l. 1000), loi conservatrice.
   - **Moyenne des commandes** : Q̄_{t+1} = (1 − μ) Q̄ + μ min(D, 1,1 S) (l. 1418), avec μ = 0,10 par semaine (l. 111) et le plafond `order_cap` de 1,1 (l. 241).
   - **Valorisation.** inventory_change = ΔSinv · p, au prix de vente courant (l. 1019), entre dans `Pi_brut` (l. 1020). L'amortissement δ/52 · pK · K est compté au prix courant (l. 1021) ; le prix de remplacement est lissé dans le coût (l. 1075). La valeur comptable des entreprises (`equity_book`, l. 1707–1709) vaut K·pK + Sinv·p + Xinv·p − dettes + dépôts, avec un plancher.
   - **Capital** : K_{t+1} = (1 − δ/52) K + Igot (l. 1002).
   - **Utilisation** : clip(Ŷ/Y^cap_full, 0, 1,5) (l. 866).
3. **État stationnaire impliqué.** La forme fermée de 3.A-3 s'applique, avec g^e = g0/52.

   Chiffres (M1), avec la croissance réalisée mesurée en G1 (PIB réel +11,53 % en 260 semaines, S+O), soit 2,206 % par an :

   | Cas | Nominal | μ ×0,5 | μ ×2 | λ ×0,5 | λ ×2 |
   |---|---|---|---|---|---|
   | Hebdomadaire, g^e = g0/52 | 3,7107 semaines (−7,23 %) | −12,71 % | −4,47 % | −13,77 % | −3,86 % |
   | Hebdomadaire, g^e = γ | −7,07 % | — | — | — | — |
   | Mensuel (vitesses × 52/12, s* = 12/13 mois) | 0,8664 mois (−6,14 %) | 0,8152 (−11,68 %) | 0,8922 (−3,35 %) | 0,8158 (−11,62 %) | 0,8925 (−3,31 %) |

   L'écart à s* a trois sources :
   - le retard de la moyenne, κ = μ/(μ + γ) ;
   - l'absence de terme pour la croissance du stock cible ;
   - g^e = g0, alors que la v2.0 suppose elle-même une croissance stationnaire g0/(1 − α moyen) ≈ 2,24 % par an (l. 449) (L, calcul).

   Conséquences :
   - S/Q < s*, donc la **borne max(·, 0) de la l. 923 est active à l'état stationnaire**. Aucun stock n'est offert (S = Y), et la marge Y − Q = γ S vaut environ 0,16 % des ventes du pas : un surcroît de demande supérieur à 0,16 % est rationné alors que des stocks existent (calcul analytique ; remesuré le 02/10/2026 sur le prototype, profil par défaut, non D1, script S1 : la borne est active toutes les semaines dans la consommation, et dans l'équipement hors de l'épisode des années 37 à 39 ; voir 3.B-4 et l'interprétation qui suit les verdicts).
   - L'état initial pose Sinv = s* Ycol et Q̄ = Ycol (l. 491, 493). Ce n'est pas l'état stationnaire de la règle (κ < 1, S/Q < s*) : il y a une transition dès t = 0, et D1 a été obtenu après 150 ans de préparation (R). Le critère 3 (b) n'est pas satisfait.
   - Le taux d'utilisation a une forme fermée conditionnelle à L_prof, donc aux prix (fiche 4).
4. **Comportement mesuré.**
   - G1 (S+O) : PIB réel +11,53 % en 260 semaines.
   - G1b (S+O) : sans le terme R3, prix de l'équipement +65,86 % et chômage de 16,438 % ; c'est l'instabilité 14.
   - D1 sur 60 ans (R) : dérive du prix de l'équipement relatif à la consommation de 12,8 %, épisode de 13,6 %.
   - Instabilité 9 (R ; commentaire lu à la l. 83, L) : prix de l'équipement ×4,8 en 60 ans sous `normal_average`.
   - Instabilité 14 (R) : production d'équipement nulle en semaine 736.
   - Ratio de stocks, activation de la borne de la l. 923 (branche exécutée l. 946) et sensibilité aux vitesses : non mesurés en G–K ; **remesurés le 02/10/2026** (profil par défaut, non D1 ; script S1, § 9.7). Verdicts et interprétation ci-dessous.
   - **Remesure S1, 02/10/2026** (statut : remesuré le 02/10/2026, profil par défaut, non D1). Critères écrits avant l'essai au § 9.7, commités en `227607e`.
     - **Exécution.** Commande : `uv run python outils/remesurer_v2_production.py --sortie <fichier>`. Script au commit `dfe896f`, audit conforme. Valeurs par défaut : 60 ans, graine 0, cinq branches. Durée 32 s, code de sortie 0. Modèle `2.5-claude-w10-20260914` ; pilote sous Python 3.12.3, numpy 2.5.3, scipy 1.18.1.
     - **Contrôles.** Les cinq branches sont remesurées, sans aucune semaine exclue dans la fenêtre. `find archive -name __pycache__` est vide : `archive/` n'a pas été modifiée.
     - **Critère (i) : non satisfait.** Branche nominale, années 31 à 60, moyenne des moyennes annuelles :
       - consommation : Sinv/(s*·Q̄) = 0,91644, part des semaines avec excess > 0 = 0,0 ;
       - équipement : Sinv/(s*·Q̄) = 0,92703, part des semaines avec excess > 0 = **0,08013**, au-dessus du seuil de 0,05.
       - La condition sur le ratio (< 0,99) tient dans les deux secteurs. La condition sur la part des semaines n'échoue que dans l'équipement.
     - **Critère (ii) : satisfait.** Ratio Sinv/Q en semaines, valeurs ×0,5 puis ×2, écart relatif :

       | Vitesse | Consommation | Équipement |
       |---|---|---|
       | `mu_ema` | 4,10410 et 3,68462 ; écart 0,10221 | 8,07675 et 3,85009 ; écart 0,52331 |
       | `lam_inv_2` | 3,41802 et 3,74767 ; écart 0,09645 | 3,64464 et 3,93041 ; écart 0,07841 |

     - **Portée.** Ces verdicts ne changent pas M24 (réserve 5 du § 5).

   **Interprétation de la remesure S1.**

   *`macro`, 02/10/2026. Les valeurs sont lues dans le JSON de sortie : moyennes annuelles et moyennes de fenêtre de toutes les grandeurs du script. Ce que le prototype produit est séparé de ce que je prédisais.*

   **Ce que le prototype produit** (profil par défaut, années 31 à 60).

   - **Consommation, branche nominale :**
     - Sinv/(s*·Q̄) vaut 0,9164, et l'excédent de stock n'est jamais positif : la borne max(·, 0) est active **toutes les semaines**.
     - Sinv/Q vaut 3,651 semaines.
     - D > S dans 3,72 % des semaines, avec un rationnement moyen (D − Q)/D de 0,02 %. Comme aucun stock n'est jamais offert, chacune de ces semaines est une semaine de demande rationnée alors que le stock vaut environ 3,65 semaines de ventes.
     - Y/Ŷ vaut 0,9993.
   - **Équipement, branche nominale :**
     - L'excédent de stock est nul 27 années sur 30. Il est positif dans un seul épisode : part de 0,48 en année 37, 1,0 en année 38, 0,92 en année 39, avec Sinv/(s*·Q̄) de 1,079, 1,184 et 1,050.
     - Hors épisode, Sinv/(s*·Q̄) décroît de 0,995 (année 40) à 0,894–0,896 (années 45 à 60).
     - D > S dans 29,5 % des semaines ; rationnement moyen de 0,09 %.
     - Le dépassement du seuil de 5 % (0,080) tient donc **entièrement à cet épisode**.
   - **Branche μ ×0,5 :** les deux secteurs changent de régime.
     - Consommation : excédent positif 35,8 % des semaines, D > S 64,6 %.
     - Équipement : Sinv/(s*·Q̄) = 1,925 en moyenne de fenêtre ; Sinv/Q = 8,08 semaines ; rationnement moyen de 15,8 %. Les moyennes quinquennales oscillent entre 0,88 et 3,0 sur les 60 ans, si bien que la moyenne de fenêtre n'y décrit pas un état stationnaire.
   - **Branches λ ×0,5 et ×2, μ ×2 :** pas de changement de régime dans la consommation (excédent jamais positif).

   **Ma prédiction analytique** (3.B-3 ; bloc seul, demande exogène, g^e = g0/52, croissance de 2,206 % par an prise de G1 ; ce n'est pas un fait), confrontée à la remesure :

   | Point prédit | Prédiction | Ce que le prototype produit | Lecture |
   |---|---|---|---|
   | Borne active à l'état stationnaire (S/Q < s*) | oui | consommation : toutes les semaines ; équipement : 27 années sur 30 | **confirmée qualitativement** |
   | Pénurie alors que des stocks existent | oui (marge d'environ 0,16 %) | D > S dans 3,7 % (consommation) et 29,5 % (équipement) des semaines, aucun stock offert | **confirmée qualitativement** ; l'ampleur au-delà du seuil de 0,16 % n'est pas mesurée par le script |
   | Niveau Sinv/(s*·Q̄) | ≈ 0,93 | 0,916 (consommation) ; 0,927 (équipement, épisode compris) ; 0,895 (équipement, années 45 à 60) | même ordre de grandeur, un peu plus bas ; **écart non expliqué** |
   | Niveau Sinv/Q | 3,7107 semaines | 3,651 (consommation) | −1,6 % ; non expliqué |
   | Sens de l'effet de λ (×0,5 baisse le ratio, ×2 le monte) | −13,8 % et +3,6 % | consommation : −6,4 % et +2,7 % par rapport à la branche nominale | **sens confirmé**, ampleur plus faible |
   | Sens de l'effet de μ ×2 | +3,0 % | consommation : +0,9 % | sens confirmé |
   | Sens de l'effet de μ ×0,5 | −12,7 % | consommation : **+12,4 %** (4,104 contre 3,651) | **contredit** : le prototype change de régime, la prédiction du bloc seul ne s'y applique pas |

   Causes candidates des écarts, **non vérifiées** :
   - la croissance réalisée sous le profil par défaut n'est pas mesurée par le script, et peut différer des 2,206 % de G1, qui portait sur D1 ;
   - Y/Ŷ est inférieur à 1 (0,9993 et 0,9985) ;
   - la demande n'est pas exogène dans le prototype ;
   - les commandes suivies sont plafonnées à 1,1 × S (l. 1418) ;
   - la marge réagit aux stocks (l. 1086–1099).

   Le script ne permet pas de les départager. **Aucune mesure supplémentaire n'est demandée**, puisque le verdict ne touche pas M24.

   **Conséquence pour la fiche.** Les verdicts sont publiés tels quels.
   - Le critère (i) est non satisfait par la part des semaines dans l'équipement, sans requalification après coup. Le fait que le dépassement tienne à un seul épisode est une **observation**, pas une correction du critère.
   - Le critère (ii) établit, sur le prototype lui-même, que **les vitesses déplacent l'état d'arrivée** (8 % à 52 %). C'est le défaut pour lequel B est écartée au critère 4.
   - La branche μ ×0,5 montre en outre une sensibilité de régime (oscillation de grande amplitude, rationnement de 15,8 % dans l'équipement) que l'analyse linéaire ne prévoyait pas. Je la consigne comme observation sur l'option écartée ; elle n'appelle aucune suite.
   - M24 est inchangée (réserve 5).

5. **Coût de calcul.**
   - Quatre secteurs, matrices 4 × 4, quelques centaines d'opérations vectorielles par semaine dans cette partie.
   - L'inverse de Leontief (l. 447) et le point fixe `solve_init` (l. 1956) ne s'exécutent qu'au chargement.
   - Moteur entier : 308,6 ms par semaine simulée (fiche 1, 3.B-4 ; ADR 0001 § 3 ; 29/09/2026). Part du bloc non isolée : non mesuré.
6. **Défauts connus et instabilités documentées.**
   - (i) Une vitesse détermine l'état d'arrivée (rubrique 3).
   - (ii) Une borne est active à l'état stationnaire et gèle le stock tampon (rubrique 3).
   - (iii) Le profit inclut la marge sur les invendus (ΔSinv · p), et la valeur comptable (l. 1709) réévalue le capital et les stocks au prix courant sans ligne : contraire à `sec:cadre` l. 520.
   - (iv) g^e ≠ croissance propre (rubrique 3).
   - (v) Neuf bornes :
     - Ŷ ≥ 0,05 Y^cap (l. 645) ;
     - intrants : max(0, ·) et plafond de trésorerie (l. 647, 650) ;
     - min(L_tech, L_prof) (l. 660) ;
     - L_cash (l. 664–665) ;
     - plafond de 0,98 de la population active (l. 668) ;
     - thr ∈ [0, 1] (l. 679) ;
     - excess ≥ 0 (l. 923) ;
     - `order_cap` de 1,1 (l. 1418) ;
     - substitution d'emploi des entreprises zombies (l. 661).
   - (vi) État initial non résolu.
   - (vii) Instabilités concernées : n° 9 (R), 10 et 11 (amortissement au prix lissé, l. 1075 : « p_K entre dans son propre coût »), 14 (S+O et R) et 15 (R). Hypothèses réfutées n° 1, 2 et 4.
   - (viii) Cycle propre amorti d'environ 6 ans (rubrique 8).
7. **Identités de bilan touchées.**
   - Grand livre de dépôts par entreprise F_j ; intrants payés de F_j à F_k (l. 993) ; exportations via le compte FX.
   - Pas de matrice (fiche 1, 3.B).
   - Critère 2 : la sous-colonne courante vaut le profit net moins les dividendes. Mais V_F par le stock (l. 1709) moins V_F par les flux égale la réévaluation cumulée Σ(Sinv Δp + K ΔpK), non nulle sous inflation. La reprendre exigerait une ligne de réévaluation, donc une décision citant M22 (critère 1 (b)).
8. **Ce que le joueur en percevrait.** La production suit la demande par l'emploi (λ_L = 2,08 par an) et les stocks (1,04 par an). La boucle a une paire de valeurs propres complexes : c'est un **cycle amorti des stocks et de l'emploi propre au bloc** (M2).

   | Pas | Vitesses | Période | Demi-vie | Module |
   |---|---|---|---|---|
   | Mensuel (transposition) | ×1 | 72,7 mois | 7,3 mois | 0,9092 |
   | Mensuel | ×0,5 | 145,1 mois | 15,3 mois | — |
   | Mensuel | ×2 | 36,9 mois | 3,3 mois | — |
   | Hebdomadaire natif | ×1 | 72,5 mois | 7,8 mois | — |
   | Hebdomadaire natif, équipement (λ_L × 0,5) | — | 83,4 mois | 15,8 mois | — |

   Le joueur verrait aussi des pénuries dès qu'un surcroît de demande dépasse 0,16 % (comportement contre-intuitif). Les quatre secteurs incluent l'alimentation et l'énergie, qui relèvent du jalon J5.
9. **Empreinte sur l'état.**
   - Q̄ (4), Sinv (4), Xinv (16), L (4), K (4), A (4), zombie (4), Pi_brut_bar (4), H, stock de ressource, aléa climatique : environ 45 variables.
   - Historiques dans l'état (fiche 1, 3.B-6).

### 3.N Socle commun aux options nouvelles (C et D)

Le socle reprend la forme du modèle DIS de Godley et Lavoie (2007, chap. 9 ; équations lues par reproductions, voir la littérature), avec cinq modifications, chacune motivée par un critère :
- (a) des ventes anticipées corrigées de la tendance et un terme de croissance du stock cible (critère 4 ; la règle littérale échoue sous croissance, 3.N-2) ;
- (b) des anticipations assises sur la demande adressée, non sur les ventes (idée de la v2.0, l. 1418 et son commentaire) ;
- (c) une valorisation des stocks au coût moyen pondéré (critère 1 (b) et `sec:cadre` l. 520) ;
- (d) une capacité normale du capital, servant d'indicateur et non de plafond (critère 7, instabilité 15) ;
- (e) l'écriture par secteur j, avec J déclaré (critère 10 (d)).

#### 3.N-1 Technique (critères 3, 7, 13)

- **Leontief en travail.** La production requiert N = y/pr travailleurs.
  - Statut : choix de conception pour la technique à coefficients fixes ; N4 et N5 en sont dérivées (critère 7 (a)).
  - Provenance : Godley et Lavoie, modèle DIS (N = y/pr).
- **Productivité (N9).**
  - Règle : pr_{j,t+1} = pr_{j,t} (1 + g_pr)^{1/n_a}, tendance exogène au socle, variable d'état (un choc de niveau, jalon J5, n'exigera pas de réécriture).
  - Statut : choix de conception.
  - Conversion : 3.N-11 et lecture (G) (*révisé par M25 (b)*, 03/10/2026 ; ADR 0008, pt I.5 ; lecture (f) de M24 remplacée).
- **Capacité normale (N11).**
  - Règle : y^cap_{j,t} = K^vol_{j,t}/(n_a κ_j) et tu_{j,t} = y_{j,t}/y^cap_{j,t}, où κ_j est le rapport du capital à la production annuelle à capacité normale (années).
  - Rôle : indicateur pour la fiche 6 et pour le joueur, **sans plafond**. tu peut dépasser 1 (heures supplémentaires) ; la contrainte physique porte sur l'emploi, qui ne peut dépasser la population active (borne du bloc 3, inactive à l'état stationnaire).
  - Statut : choix de conception.
- **Abandon de la Cobb-Douglas de A et B**, pour quatre raisons :
  - pas d'inversion non linéaire de la production ;
  - plus de borne L_prof ;
  - état stationnaire en forme fermée ;
  - à capital donné, une Cobb-Douglas ferait varier l'emploi de 1/(1 − α) ≈ 1,5 fois la production, alors que le fait de comparaison (loi d'Okun, rétention de main-d'œuvre) **n'est pas sourcé ici**.

  En contrepartie, le partage de la valeur ajoutée n'est plus ancré par un produit marginal : il relève de la marge (fiche 4). C'est ce que dit l'acquis R du § 8 (« les tâtonnements de prix et l'emploi au profit nul étaient les stabilisateurs cachés de la v1 »).

#### 3.N-2 Ventes anticipées et production visée (critères 3, 4, 8)

Paramètres :
- λ_v et λ_IN : vitesses annuelles, au plus égales à n_a ;
- σ_j : stock cible en années de ventes, restitué en mois comme 12σ_j ;
- g : croissance annuelle stationnaire de la production. g n'est pas un paramètre libre : il est dérivé, g = (1 + g_pr)(1 + g_N) − 1, où g_N est la croissance de la population active (bloc 3, M25 (d)) ; g = g_pr si la population active est constante.

Équations :
- **(N1)** v^e_{j,t+1} = (1 + g)^{1/n_a} · [(1 − λ_v/n_a) v^e_{j,t} + (λ_v/n_a) d_{j,t}], formée en phase 5 du pas t et tenue à la clôture. Statut : approchée (anticipation adaptative autour de la tendance).
- **(N2)** IN^vol*_{j,t} = n_a σ_j v^e_{j,t}, en phase 2.
- **(N3)** y*_{j,t} = max{0, v^e_{j,t} + [(1 + g)^{1/n_a} − 1] IN^vol*_{j,t} + (λ_IN/n_a)(IN^vol*_{j,t} − IN^vol_{j,t})}, en phase 2. La production couvre les ventes anticipées, la croissance tendancielle du stock cible et une correction de l'écart. Statut : approchée.
- **(N4)** N*_{j,t} = y*_{j,t}/pr_{j,t}, en phase 2, transmise au bloc 3. Statut : dérivée.

**Exactitude de l'état stationnaire.** Sur une trajectoire où d croît de γ = (1 + g)^{1/n_a} − 1 par pas (*révisé par M25 (b)*, 03/10/2026 ; ADR 0008, pt I.1) :
- (N1) donne v^e = v exactement, quel que soit λ_v (point fixe de κ(1 + γ) = (1 − b)κ + b(1 + γ), d'où κ = 1) ;
- (N3) et IN^vol_{t+1} = IN^vol_t + y − v donnent (IN^vol − IN^vol*)(γ + λ_IN/n_a) = 0, donc IN^vol = n_a σ v exactement.

Contre-épreuve (M10) : IN^vol/v vaut 1,400000000000 pour les vitesses ×1, ×0,5 et ×2. La règle de Godley et Lavoie littérale (cible σ s^e, anticipation sans tendance, pas de terme de croissance de la cible) donne au contraire, sous la même croissance, 1,3201, 1,1406 et 1,3729 mois, soit −5,70 %, −18,53 % et −1,94 % (M10). Elle a été écrite pour une économie stationnaire.

#### 3.N-3 Ventes, rationnement, stocks en volume (critères 1, 7 (b))

- **(N5)** y_{j,t} = min{y*_{j,t}, pr_{j,t} N_{j,t}}, en phase 4 ; N_{j,t} est l'emploi effectif du bloc 3 (Q4). Statut : dérivée (Leontief).
- **(N6)** v_{j,t} = min{d_{j,t}, IN^vol_{j,t} + y_{j,t}}, en phase 5, avec d_{j,t} = Σ_b (plan de b en u.m.)/p_{j,t} pour b ∈ {ménages, État, entreprises}.
  - Rationnement **proportionnel** : chaque acheteur obtient la fraction v/d de sa demande (choix de conception, sans paramètre).
  - Les lignes 1 à 3 sont les ventes exécutées en u.m. : C = p C^vol, G = p G^vol, I = p I^vol.
  - La demande non servie, d − v, et son ratio (d − v)/d sont restitués ; ce ne sont pas des flux (le budget non dépensé reste en dépôts ou sur le compte du Trésor).
- **(N7)** IN^vol_{j,t+1} = IN^vol_{j,t} + y_{j,t} − v_{j,t}. Statut : dérivée. Aucun stock négatif n'est possible.

**Cas à la main (M9).** Demande supérieure de 10 % au disponible.
- Ouverture : IN^vol = 14 u.v. et IN = 13,944 u.m. ; dans le pas : y = 10 et UC = 1 ; prix p = 1,25.
- Disponible : 24 ; demande : 26,4, dont ménages 18,48, État 3,96, entreprises 3,96.
- Ventes : 24, soit un taux de service de 0,909091.
- Quantités obtenues : ménages 16,80, État 3,60, entreprises 3,60. Lignes 1 à 3 : 21,00, 4,50 et 4,50 u.m.
- Demande non servie : 2,4 u.v., soit 9,09 % de la demande.
- Ligne 4 : coût moyen 0,997667 et ΔIN = −13,944, d'où IN = 0 et IN^vol = 0 à la clôture.
- Au pas suivant, (N3) relance la production pour reconstituer le stock.

#### 3.N-4 Valorisation des stocks, ligne 4 (critères 1 (b), 2, 3)

- **(N8)** Coût unitaire des entrées : UC_{j,t} = W_t/pr_{j,t}. À J ≥ 2 avec intrants, s'ajoute Σ_k a_kj p_k.
- Coût moyen pondéré : cm_{j,t} = (IN_{j,t} + UC_{j,t} y_{j,t})/(IN^vol_{j,t} + y_{j,t}).
- **Ligne 4** : ΔIN_{j,t} = UC_{j,t} y_{j,t} − cm_{j,t} v_{j,t}, en u.m. par pas et en phase 5. Si IN^vol + y = 0, alors v = 0 et ΔIN = 0.
- La masse salariale excédentaire en cas de rétention de main-d'œuvre, WB − UC·y, n'est pas portée en stock : c'est une charge du pas.
- IN ne varie que par la ligne 4, et IN = cm × IN^vol après chaque pas ; IN n'est jamais négatif.

Quatre règles de valorisation sont comparées sur un pas où coûts et prix varient (M6). Ouverture : IN^vol = 140 et IN = 138,6 ; UC passe de 0,99 à 1,02 ; y = 100 ; v = 105 ; p = 1,30.

| Règle | ΔIN | IN de clôture | Marge (ventes − WB + ΔIN) | Verdict |
|---|---|---|---|---|
| **Coût moyen pondéré** (proposée) | −3,2625 | 135,3375 = cm · 135 | 31,2375 = v(p − cm) | conforme à la l. 520 : gain réalisé à la vente seulement |
| Coût unitaire courant, IN = UC · IN^vol (Godley et Lavoie) | −0,9, dont volume −5,1 et réévaluation +4,2 | 137,7 | 33,6 | gain de détention latent inscrit dans la ligne 4 ; demande une décision citant M22 (lecture (a)) |
| Coût du pas sans réévaluation, UC · ΔIN^vol | −5,1 | 133,5 | — | **IN peut devenir négatif** : stock vendu à UC = 1,5 après une valeur historique de 140 × 0,99, IN = −71,4 ; écartée |
| Prix de vente (v2.0, l. 1019) | −6,5 | 132,1 par les flux, contre 175,5 au bilan (l. 1709) | — | réévaluation non tracée ; écartée |

**Rapports stationnaires** (M6, M7), sous la croissance g et l'inflation π̄ des coûts :
- **ρ̄_IN** = IN/(UC · IN^vol) = 1/[1 + ((1 + π̄)^{1/n_a} − 1)(1 + n_a σ/(1 + n_a σγ))], γ = (1 + g)^{1/n_a} − 1, π̄ étant le glissement annuel stationnaire (`sec:cadre-calendrier`). Pour g = 2 % et σ = 1,4 mois : 0,996057 à π̄ = 2 %, 0,981246 à 10 %, 0,923901 à 50 % (simulations identiques). Par ailleurs IN/(p · IN^vol) = ρ̄_IN/(1 + μ), où μ est la marge (fiche 4).
- **ΔIN** = [((1 + g)(1 + π̄))^{1/n_a} − 1] · IN, soit 0,33059 % de IN par pas à g = π̄ = 2 % (*révisé par M25 (b)*, 03/10/2026 ; 0,33210 % sous la conversion linéaire de g).
- **Dépendance déclarée à n_a** (critère 3 (c)) : ρ̄_IN vaut 0,992779, 0,996057, 0,997321 et 0,997700 pour n_a = 4, 12, 52 et n_a → ∞. C'est un écart d'ordre (1 + π̄)^{1/n_a} − 1, qui disparaît sous la règle de Godley et Lavoie (ρ = 1). Les ratios du critère 3 (a) ne dépendent pas de n_a, sauf y/v, à l'ordre g²/n_a (1,0023160 / 1,0023122 / 1,0023107 pour n_a = 4, 12 et 52 ; *révisé par M25 (b)*, ADR 0008, pt I.6).

#### 3.N-5 Volume du capital et emploi : proposition sur Q4

- **Volume du capital : au bloc 2.**
  - Règle (N10, phase 5, dérivée) : K^vol_{j,t+1} = (1 − δ/n_a) K^vol_{j,t} + I^vol_{j,t}, où I^vol est le volume livré après rationnement et δ le δ du cadre.
  - Motifs : le bloc 2 exécute les livraisons et lit le capital pour la capacité. Le bloc 6 décide l'investissement visé (phase 2), lit K^vol à l'ouverture et écrit les lignes 3 et 8 en valeur comptable.
  - **Constat transmis à la fiche 6** : K est tenu en valeur comptable et la ligne 8 vaut δK/n_a sur cette valeur, d'où K/(p K^vol) = (n_a γ + δ)/[n_a(((1 + g)(1 + π̄))^{1/n_a} − 1) + δ], avec γ = (1 + g)^{1/n_a} − 1. Ce rapport, noté ρ̄_K, vaut 0,7786 pour g = π̄ = 2 % et δ = 5 %, 1,0000 pour π̄ = 0 et 0,4214 pour π̄ = 10 % (*révisé par M25 (b)*, 03/10/2026 ; 0,7791 et 0,4221 sous la conversion linéaire de g, M6, simulations identiques). L'amortissement comptable sous-estime alors l'amortissement au prix courant d'environ 22 % à π̄ = 2 %. Le K/Y d'O1 doit déclarer s'il est comptable ou en volume valorisé. Ce sont les instabilités 10 et 11 qui guettent une correction ad hoc.
- **Ajustement de l'emploi : au bloc 3.** Le bloc 2 transmet N* (phase 2) et lit N (phase 4). Le bloc 3 porte la rétention de main-d'œuvre éventuelle, la contrainte d'offre de travail et la masse salariale (ligne 5).
  - Si la fiche 3 retient un ajustement partiel de vitesse λ_N, la boucle redevient du second ordre en hausse (3.N-8).
  - Conséquence sur le contrat des phases : 3.N-6, lecture (b).

#### 3.N-6 Phases et lectures (critère 8)

| Phase | Le bloc 2 lit | Le bloc 2 écrit |
|---|---|---|
| 2 | ouverture : v^e_t, IN^vol_t, pr_t | IN^vol*_t, y*_t, N*_t |
| 4 | phase 2 ; ouverture (K^vol_t) ; N_t du bloc 3 dans la même phase | y_t, y^cap_t, tu_t |
| 5 | plans de demande (phase 2) ; prix du pas (bloc 4, avant le bloc 2 dans la phase 5) ; y_t et WB_t (phase 4) | v_t et ventes par acheteur (lignes 1 à 3) ; ΔIN (ligne 4) ; IN^vol_{t+1}, K^vol_{t+1}, v^e_{t+1}, pr_{t+1} |

- **Phase 2.** Le bloc ne lit aucun autre plan de la phase 2 : aucun ordre interne n'est requis (Q5 sans objet pour C et D).
- **Phase 5.** Son ordre interne est fixé par les fiches (l. 486) : « prix, puis production (ventes et stocks) » ne demande pas de décision citant M22.
- **Phase 4, fait nouveau.** La l. 486 ne déclare d'ordre interne que pour les phases 1, 5 et 7, alors que le bloc 2 doit lire l'emploi du bloc 3 dans la phase 4. Quelle que soit la répartition retenue pour Q4, un ordre interne de la phase 4 est nécessaire :
  - « travail, puis production » si l'emploi est au bloc 3 ;
  - « production, puis travail » si l'emploi est au bloc 2, puisque le bloc 3 verse alors les salaires sur cet emploi.

  C'est une modification des phases de l'ordonnanceur, donc une décision citant M22 (`docs/agents/routage.md` § 4.2) : lecture (b).

La matrice des lectures est triangulaire dans les deux cas, sans résolution simultanée.

#### 3.N-7 Notation (critère 13)

Contrôle (M11) : boucle `grep -c` sur `docs/specification/nations_et_marches.tex` pour les motifs `$y`, `$v`, `$d`, `\sigma`, `\kappa`, `\mathit{pr}`, `\mathit{tu}`, `$N`, `\mathit{cm}`, `\tilde`, `\mathit{in}`, `\theta`, `\upsilon`, `$q`, `\beta`, `\mathit{UC}`, `$Y`. Sortie : 0 pour chacun. La lecture complète de `tab:symboles` (l. 798–846) le confirme.

| Symbole proposé | Sens | Unité | Remarque |
|---|---|---|---|
| y_{j,t}, y*_{j,t} | production, production visée (exposant * pour une cible, convention du glossaire) | u.v._j par pas | lettre libre |
| v_{j,t}, v^e_{j,t} | ventes, ventes anticipées | u.v._j par pas | s est pris (secteur institutionnel) ; v peut évoquer V (valeur nette) ; q, autre choix possible, est réservé si la fiche 6 retient le q de Tobin |
| d_{j,t} | demande adressée | u.v._j par pas | D_H et D_F gardent leur sens (dépôts) |
| X^vol (IN^vol, K^vol, C^vol, G^vol, I^vol) | volume d'une grandeur nominale du cadre | u.v. ou u.v. par pas | exposant `\mathrm{vol}` dans le style de `prim` et `sec` (#23) ; la convention « minuscule = volume » est inapplicable pour c, g, i, k et s ; autre choix : un tilde |
| σ_j | stock cible | années de ventes | restitué en mois : 12σ |
| κ_j | capital / production annuelle à capacité normale | années | |
| pr_{j,t}, g_pr | productivité du travail ; sa croissance | u.v. par personne et par pas ; par an | g reste la croissance stationnaire (`tab:symboles`) |
| N*_{j,t} | demande de travail | personnes | N est à confirmer par la fiche 3 ; n est le numéro de tour et ne peut noter une croissance de population |
| tu_{j,t} | taux d'utilisation | fraction | u est réservé (retard du registre) |
| λ_v, λ_IN | vitesses (λ du cadre, avec indice) | par an | |
| UC_{j,t}, cm_{j,t} | coût unitaire des entrées, coût moyen des stocks | u.m. par u.v. | UC est partagé avec la fiche 4 ; la barre est réservée à « stationnaire » |
| j = 1, 2 (pour D) | consommation, équipement | — | c et k sont réservés |

#### 3.N-8 Stabilité (critère 5)

**(a) Instabilités connues.**
- Sous C, les n° 1 et 9, ainsi que la forme « équipement » des n° 10, 11 et 14, n'ont pas d'objet : il n'y a ni prix relatif du capital, ni construction. *Précision du 02/10/2026 (§ 9.6, correction de l'instruction sans changement de verdict)* : la règle de prix sans terme de demande (14) et l'amortissement dans le coût (10 et 11) restent des risques des fiches 4 et 6 ; ils ne sont pas « écartés par construction ».
- La n° 15 ne concerne pas le bloc, qui n'a pas de plafond ; le plafond d'emploi du bloc 3 est inactif à l'état stationnaire.
- Sous D, les n° 9, 10, 11 et 14 sont concernées, ainsi que les hypothèses réfutées n° 1 et 2 (définition et dénominateur du prix de l'équipement).

**(b) Boucle propre, demande exogène constante, pas mensuel (M3).** La matrice est triangulaire ; ses valeurs propres sont 1 − λ_v/n_a et (1 − λ_IN/n_a)/(1 + g)^{1/n_a}, réelles et positives (*révisé par M25 (b)*, 03/10/2026). **Aucun cycle propre.**

| Calibration | Valeurs propres | Demi-vie |
|---|---|---|
| Indicative : λ_v = 3 et λ_IN = 1,5 par an ; σ = 1,4 mois ; g = 2 % | 0,75 et 0,8736 | 5,1 mois |
| Vitesses ×0,5 | 0,875 et 0,9360 | 10,5 mois |
| Vitesses ×2 | 0,5 et 0,7488 | 2,4 mois |

**Compléments hors critère 5 (b), M4.**
- **Ajustement partiel de l'emploi** (si la fiche 3 le retient, λ_N = 2,08 par an, valeur de la v2.0). La paire devient complexe, de module √(1 − λ_N/n_a) = 0,9092 : période de 51,7 mois et demi-vie de 7,3 mois. Pour les vitesses ×0,5 : 104,5 mois et 15,3 mois ; pour ×2 : 25,2 mois et 3,3 mois. Le module de la paire ne dépend que de la vitesse de l'emploi.
- **Demande induite**, d_t = A + m y_{t−1}, où m est une propension de la demande à la production du pas précédent ; c'est une **hypothèse**, fixée par les fiches 5 et 9. On obtient un cycle des stocks à la Metzler.

  | Calibration | m | Rayon spectral | Demi-vie | Période |
  |---|---|---|---|---|
  | λ_v = 3, λ_IN = 1,5 | 0,6 | 0,9459 | 12,5 mois | 73,0 mois |
  | λ_v = 3, λ_IN = 1,5 | 0,8 | 0,9770 | 29,8 mois | 95,9 mois |
  | Vitesses ×0,5 | 0,6 | 0,9681 | — | 146,9 mois |
  | Vitesses ×2 (λ_v = 6, λ_IN = 3) | 0,6 | 0,9209 | — | 37,6 mois |

  **Risque.** À λ_v = 12 et λ_IN = 6 par an (anticipation naïve), la boucle est **explosive** pour m = 0,6 : valeur propre −1,2366, alternance de période 2 vérifiée par simulation d'impulsion. Frontière (λ_IN = λ_v/2) : λ_v maximal stable de 10,7, 9,9, 9,2, 8,6 et 8,1 par an pour m = 0,5 à 0,9 (σ = 1,4 mois) ; 7,9 pour m = 0,8 et 3,7 pour m = 0,9 (σ = 2 mois). La calibration indicative garde ses vitesses doublées dans le domaine stable pour m ≤ 0,8.

**Exemple daté (critère 11, M5).** Bloc seul, demande exogène. La part de G dans la demande est fixée à 20 % (**hypothèse**) ; G augmente de 1 % aux tours 1 à 12, soit une demande en hausse de 0,2 %.
- Tour 1 : production inchangée (+0,000 %) ; le stock baisse dans le tour, de 1,4000 à 1,3980 mois de ventes stationnaires (contrepartie visible le jour même).
- Tours suivants : production +0,084 % au tour 2, +0,142 % au tour 3, +0,183 % au tour 4, +0,246 % au tour 9 (dépassement pour reconstituer le stock), +0,239 % au tour 13.
- Après la fin du choc : production +0,153 % au tour 14, −0,003 % au tour 18, −0,030 % au tour 24.
- Aucune demande non servie.
- Avec m = 0,6 : production +0,450 % au tour 9 et +0,578 % au tour 13, puis +0,121 % au tour 24.

#### 3.N-9 Bornes (critère 7 (a))

| Borne | Type | Active à l'état stationnaire ? |
|---|---|---|
| y* ≥ 0 | plancher physique ; ne joue qu'après un effondrement de la demande (stock supérieur à la cible de plus de n_a/λ_IN = 8 mois de ventes) | non |
| v ≤ IN^vol + y | disponibilité, critère 7 (b) | non |
| y ≤ pr · N | technique à coefficients fixes, déclarée | les deux termes sont égaux, sans rationnement |

Les autres bornes du socle relèvent d'autres blocs : l'emploi au plus égal à la population active (bloc 3) et les bornes de prix éventuelles (bloc 4). Comparaison : A en compte 5 (3.A-6) et B 9 (3.B-6), dont une active à l'état stationnaire.

#### 3.N-10 Sous-colonnes des entreprises (critère 2, mesure)

- **Sous-colonne courante** : C + G + I + ΔIN − WB − T_F − δK/n_a − i_L L/n_a + i_D D_F/n_a − Div_F.
  - Avec la ligne 4 de 3.N-4 : (ventes − cm·v) − (WB − UC·y) − T_F − δK/n_a − intérêts nets − Div_F, soit les profits non distribués FU.
- **Sous-colonne capital** : −FU.
- **Valeur stationnaire** : FU = ΔV_F = [((1 + g)(1 + π̄))^{1/n_a} − 1] V_F, soit 0,33059 % de V_F par pas à g = π̄ = 2 %, non nul dès que V_F > 0 (*révisé par M25 (b)*, 03/10/2026). C'est exactement la croissance nominale de V_F par pas.
- Aucun flux du socle ne présuppose l'issue de Q2 (fiche 6).

#### 3.N-11 État stationnaire résolu et coût (critères 3, 9)

**Formes fermées** sous la croissance g et l'inflation π̄ :
- v^e = v ;
- stock d'ouverture / ventes du pas = n_a σ, soit 1,4 pour σ = 1,4/12 an ;
- y/v = 1 + n_a σγ, γ = (1 + g)^{1/n_a} − 1, soit 1,0023122 (*révisé par M25 (b)*, 03/10/2026 ; 1 + gσ = 1,002333 sous la conversion linéaire de g) ;
- productivité / tendance = 1 ;
- t̄u = κ/(K^vol/(n_a y)), conditionnel au K/Y de la fiche 6 (t̄u = 0,8 si K^vol/(n_a y) = 3 ans et κ = 2,4 ans) ;
- ρ̄_IN, ΔIN et ρ̄_K : 3.N-4 et 3.N-5.

Ni λ_v ni λ_IN n'entrent dans ces formes. Trois ratios dépendent de n_a, dépendance déclarée : ρ̄_IN et ρ̄_K, à l'ordre (1 + π̄)^{1/n_a} − 1 ; y/v, à l'ordre g²/n_a, ratio mixte d'un taux de flux et d'une croissance géométrique (*révisé par M25 (b)*, 03/10/2026 ; ADR 0008, pt I.6).

**État initial résolu, sans préparation** : à partir de v_0, résolu par le socle, on pose y_0 = v_0(1 + n_a σγ), v^e_0 = v_0, IN^vol_0 = n_a σ v_0, IN_0 = ρ̄_IN UC_0 IN^vol_0, pr_0 par normalisation, K^vol_0 = n_a κ y_0/t̄u (avec t̄u de la fiche 6).

**Croissance (critère 3 (d)).**
*Paragraphe *révisé par M25 (b)*, 03/10/2026 (ADR 0008, pt I.1 et I.5) ; il remplaçait la conversion linéaire de M24 (f).*
- Source de g : g_pr (bloc 2) et g_N (bloc 3, M25 (d)) ; g = (1 + g_pr)(1 + g_N) − 1.
- Conversion géométrique : (1 + g_pr)^{1/n_a} par pas. La croissance annuelle effective est exactement g_pr ; aucune croissance effective distincte n'est publiée.
- Les ratios du bloc n'en dépendent que par la dépendance à n_a déclarée ci-dessus.

**Coût (critère 9).**
- Environ 35 opérations flottantes par secteur et par pas, sans itération ni inverse.
- Mesure de la maquette (M8, machine de la session cloud, x86_64, 4 cœurs, **pas la plateforme de référence de l'ADR 0003**) : 0,81 µs par pas pour J = 1, 1,25 µs pour J = 2, 2,30 µs pour J = 4, 4,11 µs pour J = 8. Pour J = 1, c'est 0,17 % de la part indicative de 0,48 ms.

#### 3.N-12 Calibration et faits établis (critère 14)

Valeurs indicatives, à fixer au J3 :
- λ_v = 3 par an ; λ_IN = 1,5 par an (3.N-8) ;
- σ = 1,4/12 an ;
- κ, à fixer avec la fiche 6 ;
- g_pr, avec O1.

Faits (statut « établi » seulement si la source primaire est lue ; ici, **sources primaires non lues**) :

| Grandeur | Valeur lue | Source | Réserve |
|---|---|---|---|
| Stocks / ventes, États-Unis, ensemble des entreprises | 1,36 à 1,39 mois en 2025 | US Census, *Manufacturing and Trade Inventories and Sales* (extraits de recherche du 02/10/2026) | couvre industrie, gros et détail, et tous les stades des stocks, pas les seuls produits finis |
| Taux d'utilisation des capacités, industrie | moyenne de 79,4 % sur 1972–2025 | Réserve fédérale, publication G.17 d'août 2026 (extrait de recherche) | industrie, mines et services collectifs seulement |
| Part salariale | moyenne de 0,52 | Penn World Table (Feenstra, Inklaar et Timmer), extrait de recherche | relève des fiches 3 et 4 |
| K/Y | non trouvée (proxy) | — | relève d'O1 et de la fiche 6 |

Les « repères observés » du tableau de la v1.5 (l. 2019–2033) sont sans source : ce ne sont pas des faits établis.

### 3.C Option C — socle 3.N, J = 1 (bien unique)

1. **Source.** Socle 3.N. Modèle DIS de Godley et Lavoie (2007, chap. 9), lu par reproductions. Principe de simplicité.
2. **Équations.** N1 à N11 avec J = 1. Un seul prix p, donc p_K = p, et I^vol = I/p. Le PIB en volume est y.
3. **État stationnaire.** 3.N-11, exact ; aucun prix relatif.
4. **Comportement mesuré.** Non mesuré sur un moteur. Maquettes du bloc seul : M3, M5, M6.
5. **Coût.** 0,81 µs par pas (maquette).
6. **Défauts.** Aucune instabilité connue concernée. Trois risques déclarés :
   - la boucle fermée devient explosive si les vitesses sont rapides (3.N-8) ;
   - la valeur comptable du capital est fragile sous inflation (constat pour la fiche 6) ;
   - l'ordre interne de la phase 4 doit être déclaré (lecture (b)).
7. **Identités touchées.** Lignes 1 à 4 (phase 5) ; la ligne 5 (salaires) relève du bloc 3 et la ligne 8 du bloc 6. Aucune ligne nouvelle, aucune table modifiée : `verifier_matrices.py` n'est pas à rejouer. Aucun solde résiduel ; aucune position intra-pas. Les lignes 1, 3 et 4 n'ont aucun effet sur M ni sur H ; la ligne 2 est une porte (fiche 9).
8. **Ce que le joueur en percevrait.**
   - Une variation de la demande se voit le tour même dans les stocks ou la demande non servie.
   - La production et l'emploi répondent au tour suivant : 1 tour, ou davantage si le bloc 3 retient un retard.
   - Il n'y a pas de cycle propre ; un cycle amorti de 3 à 8 ans apparaît si la demande est induite.
   - Indicateurs : un seul indice de production, le taux d'utilisation, les stocks en mois et la demande non servie.
9. **Empreinte.** Quatre variables d'état : v^e (u.v. par pas, valeur stationnaire v_0) ; IN^vol (u.v., n_a σ v_0) ; pr (normalisation) ; K^vol (n_a κ y_0/t̄u). S'y ajoutent les postes IN et K du cadre. Aucun historique, aucun drapeau de mode, aucun tirage aléatoire.

### 3.D Option D — socle 3.N, J = 2 (consommation et équipement)

1. **Source.** Socle 3.N avec J = 2 ; piste « deux secteurs » (feuille de route § 5). Aucune référence de modèle stock-flux à deux secteurs n'a été retrouvée et lue : **la littérature retrouvée ne permet pas de conclure**.
2. **Équations.** N1 à N11 par secteur.
   - Demande : d_1 = C^vol + G^vol et d_2 = I^vol. Sans capital public au socle, G n'achète que le bien 1.
   - Prix relatif p_2/p_1 fixé par la fiche 4.
   - Colonne des entreprises consolidée, avec des comptes de production par j : aucune ligne nouvelle (critère 1 (c)). Les ventes d'équipement entre secteurs restent dans la ligne 3.
   - IN_j sont des sous-positions du poste IN, dont la forme est à confirmer par la fiche 6 et le noyau.
   - PIB en volume : Σ_j p_{j,0} y_j aux prix de l'état initial résolu, ou indice chaîné annuel (SCN 2008, extrait non lu). Les deux coïncident à l'état stationnaire.
3. **État stationnaire.** Par secteur, comme dans 3.N-11. Sous une marge constante et des coûts salariaux seuls, p_2/p_1 = (1 + μ_2) pr_1/((1 + μ_1) pr_2), stationnaire si et seulement si g_pr,1 = g_pr,2. Si le prix inclut l'amortissement au prix de l'équipement, p_2 entre dans son propre coût : c'est la boucle de la v2.0 (l. 1075).
4. **Comportement mesuré.** Non mesuré. Pour mémoire, la dérive de p_K/p_C en v2.0 depuis D1 est de 12,8 % (R), au-delà de la bande de ±10 % proposée au critère 6.
5. **Coût.** 1,25 µs par pas (maquette).
6. **Défauts.** Instabilités n° 9, 10, 11 et 14 et hypothèses réfutées n° 1 et 2 concernées (3.N-8). Le prix relatif doit être rendu stationnaire. La composition de la demande doit être fixée par les fiches 5 et 9.
7. **Identités touchées.** Les mêmes que C ; les lignes 1 à 4 sont réparties par bien.
8. **Ce que le joueur en percevrait.** Le seul mécanisme nouveau perçu : une variation de l'investissement frappe d'abord l'emploi et le prix du secteur d'équipement. Aucun levier nouveau au socle (critère 10 (e)).
9. **Empreinte.** Huit variables d'état (quatre par secteur) et deux sous-positions IN_j. Environ huit paramètres.

### 3.J Nombre de secteurs (critère 10, mesure)

| | J = 1 (C) | J = 2 (D) | J = 4 (B) | v1.5 : 7 + ressources (A) |
|---|---|---|---|---|
| (a) Ce qu'il ajoute | Le socle seul : toutes les identités du bloc sont vérifiables (y = v + ΔIN^vol ; PIB en volume = y) | Un marché de l'équipement : le prix relatif et l'emploi par secteur rendent visible l'accélérateur ; aucune identité nouvelle | Énergie et alimentation : chocs d'offre et intrants (mécanismes du jalon J5) | Intermédiaires, construction (J6), services, terre et ressources (J5 à J7) |
| (b) Ce qu'il coûte | 5 paramètres, 4 variables d'état, 0 prix relatif, 0 ligne | Environ 8 paramètres, 8 variables, 1 prix relatif, instabilités 9 à 11 et 14 | Environ 40 paramètres, 45 variables, 3 prix relatifs, matrice a (l. 103–106), instabilités 9 à 11 et 14 (S+O pour G1b) | Environ 107 variables, 7 prix relatifs, 64 coefficients, instabilités 1, 9 à 11, 14 et 15 |
| (c) PIB en volume | y | Prix de base fixes de l'état résolu, ou indice chaîné ; identiques à l'état stationnaire | Idem, en valeur ajoutée | Idem |
| (d) Extensibilité | Équations indexées par j dès le socle : un secteur s'ajoute par une composante, et les intrants par un terme de UC et une ligne interne à la colonne consolidée, sans réécrire M24. J7 : x = (I − A)^{-1} d se calcule au chargement | Idem | Retour au socle : retrait de deux secteurs | Réécriture |
| (e) Leviers du socle | G porte sur le bien unique | Composition de G entre biens inerte sans capital public | Idem, plus l'énergie (J5) | Idem |

## 4. Tableau comparatif

Renvois : 3.A-k et 3.B-k désignent la rubrique k ; 3.N-k la sous-section du socle ; 3.C, 3.D et 3.J les sous-sections correspondantes.

| Critère | A. v1.5 | B. v2.0 | C. socle, J = 1 | D. socle, J = 2 |
|---|---|---|---|---|
| 1 (a) Lignes, monnaie | Pas de matrice (3.A-7) ; loi des stocks non conservatrice telle qu'écrite (3.A-6 (i)) | Loi des stocks conservatrice ; pas de matrice (3.B-7) | Oui : lignes 1 à 4, aucune ligne nouvelle (3.C-7) | Oui (3.D-2) |
| 1 (b) Volume et valeur | Non : ΔIN non défini (3.A-6 (ii)) | Non : réévaluation implicite au prix courant (3.B-6 (iii)) | Oui : coût moyen pondéré, ρ̄_IN explicite (3.N-4) | Oui (3.N-4) |
| 1 (c) Secteurs | Bilan par j, sans matrice | Grand livre par j | Sans objet | Colonne consolidée et comptes de production par j (3.D-2) |
| 2 Sous-colonnes (mesure) | Non calculable (3.A-7) | Écart égal à la réévaluation (3.B-7) | FU = 0,33210 % de V_F par pas (3.N-10) | Idem |
| 3 (a) Formes fermées | Ratio des stocks calculable, mais dépend des vitesses ; utilisation dégénérée (3.A-3) | Idem ; utilisation conditionnelle aux prix (3.B-3) | Oui (3.N-11) | Oui, plus le prix relatif (3.D-3) |
| 3 (b) État initial résolu | Non : transitoire de 3 à 5 ans (R) (3.A-3) | Non : état initial hors état stationnaire de sa propre règle, D1 préparé (3.B-3) | Oui (3.N-11) | Oui |
| 3 (c) Indépendance de n_a | λ_L non transposable (3.A-6 (iv)) | Non vérifiée | Oui ; ρ̄_IN et ρ̄_K dépendent de n_a à l'ordre (1 + π̄)^{1/n_a} − 1, déclaré (3.N-4) | Idem |
| 3 (d) Source et conversion de g | g^e non déclaré | g^e = g0 ≠ croissance propre (3.B-3) | g dérivé, conversion linéaire chiffrée (3.N-11) | Idem |
| 4 (a) Vitesses et état d'arrivée | **Non** : environ 5 % d'écart entre les branches ×0,5 et ×2 (3.A-3) | **Non** : environ 9 % d'écart (3.B-3) | Oui : 1,400000000000 dans toutes les branches (3.N-2) | Oui |
| 4 (b) Intégrateur sans ancre | Non relevé | Non relevé | Aucun | Aucun |
| 5 (a) Instabilités connues | 1, 9 à 11, 14, 15 (3.A-6) | 9, 10, 11, 14 (S+O), 15 (3.B-6) | Aucune (3.N-8) | 9 à 11, 14 (3.D-6) |
| 5 (b) Valeurs propres | Réelles, demi-vie de 4,7 mois au pas hebdomadaire ; −0,0956 en transposition (3.A-8) | Complexes : 6,1 ans de période, 7,3 mois de demi-vie ; ×2 : 3,1 ans ; ×0,5 : 12,1 ans (3.B-8) | Réelles : 0,75 et 0,8735 ; module < 1 pour les vitesses ×0,5 et ×2 (3.N-8) | Idem, par secteur |
| 6 Test zéro (J3) | Non mesuré | Dérive de 12,8 % du prix relatif depuis D1 (R), hors de la bande de ±10 % | Préalable satisfait (3.N-11) | Préalable satisfait ; prix relatif à tenir (fiche 4) |
| 7 (a) Bornes | 5 (3.A-6 (v)) | 9, dont une active à l'état stationnaire (3.B-6 (v)) | 3 physiques ou techniques, aucune active (3.N-9) | Idem |
| 7 (b) Disponibilité et rationnement | Proportionnel ; loi des stocks fautive | Exportations d'abord, puis prorata ; stock gelé sous la cible | Proportionnel, cas à la main (3.N-3) | Idem |
| 8 Phases | Bloc compatible ; emploi interne au bloc (3.A-2) | Compatible (3.B-2) | Phase 2 sans ordre interne ; **ordre interne de la phase 4 requis**, décision citant M22 (3.N-6) | Idem |
| 9 Coût | Non mesuré, non discriminant | 308,6 ms par semaine pour le moteur entier ; bloc non isolé | 0,81 µs par pas (maquette) | 1,25 µs |
| 10 Secteurs (mesure) | 3.J | 3.J | 3.J | 3.J |
| 11 (a) Indicateurs | Utilisation dégénérée | Utilisation bornée par clip | Production, tu, stocks en mois, demande non servie (3.C-8) | Idem, par secteur |
| 11 (b) Délais | Tick hebdomadaire | Cycle propre ; pénuries dès 0,16 % | 1 tour pour la production ; stocks visibles le tour même (3.N-8) | Idem |
| 11 (c) Leviers | Aucun levier propre | Idem | Tableau du § 5 | Idem |
| 11 (d) Cycle | Aucun | 6 ans | Aucun, ou 3 à 8 ans si la demande est induite (3.N-8) | Idem |
| 12 Simplicité (décompte) | Environ 107 variables, 5 bornes, aléa (3.A-9) | Environ 45 variables, historiques, 9 bornes (3.B-9) | 5 paramètres, 4 variables, 0 ligne, 3 phases (3.C-9) | 8 paramètres, 8 variables (3.D-9) |
| 13 Notation | Symboles en collision (S, i, H…) | Sans objet | Proposée, sans collision (3.N-7) | Idem ; j = 1, 2 |
| 14 Calibrabilité | Repères sans source | D1 non versé | Trois ordres de grandeur, sources primaires non lues (3.N-12) | Idem |

## 5. Avis de l'expert pilote

*`macro`, 02/10/2026.*

**Recommandation : option C**, c'est-à-dire le socle commun 3.N avec un bien unique (J = 1) et des équations indexées par j dès le socle. Elle se combine avec :
- la valorisation des stocks au coût moyen pondéré ;
- le volume du capital tenu par le bloc 2 ;
- l'ajustement de l'emploi tenu par le bloc 3 (proposition sur Q4).

Classement : C > D > B > A.

Critère par critère :
- **1 et 4 (exigences)** : A et B sont écartés. La règle de production visée qu'ils partagent fait dépendre le ratio stocks / ventes des vitesses (environ 5 % et 9 % d'écart entre les branches) ; A n'a pas de valorisation des stocks et B réévalue sans ligne. Le socle corrige le défaut par deux termes (tendance et croissance de la cible) dont l'effet est exact (M10).
- **3** : seul le socle a un état initial résolu en forme fermée. Sa seule dépendance à n_a (ρ̄_IN, ordre (1 + π̄)^{1/n_a} − 1) est déclarée.
- **5** : sans demande induite, le socle n'a pas de cycle propre ; B a un cycle propre de 6 ans et un stock gelé à l'état stationnaire.
- **7** : le socle n'a aucune borne active, contre 9 bornes pour B.
- **10** (règle d'arbitrage, principe de simplicité) : à exigences comptables égales, C et D se valent sur les identités. D n'ajoute aucune identité vérifiable et un seul mécanisme perçu, l'accélérateur visible dans l'équipement. Il paie ce mécanisme d'un prix relatif à stabiliser, précisément la zone des instabilités 9 à 11 et 14 et de la dérive de 12,8 % de D1, sans aucun levier du socle qui l'exploite. Les secteurs arrivent aux jalons J5 et J6 avec leurs mécanismes propres.
- **12** : C a le plus petit décompte (4 variables, 5 paramètres, 0 ligne).

**Réserves et conditions, seuils écrits avant l'essai.**
1. **J3, état stationnaire** : un pas sans choc depuis l'état résolu laisse v^e, IN^vol, IN, pr et K^vol sur leur trajectoire stationnaire à 1e−10 près en relatif (critère 3). Le script d'état stationnaire d'`outils/` (M19) porte les formes fermées de 3.N-11.
2. **J3, vitesses** : choc G +1 % pendant 12 tours, branches λ ×0,5 et ×2. Écart relatif du ratio stocks / ventes et de y/v d'au plus 1e−6 après 720 pas (critère 4).
3. **J3, boucle fermée** : rayon spectral de la linéarisation du socle complet inférieur à 1 pour la calibration et pour les vitesses ×0,5 et ×2. Si m (propension effective de la demande à la production) dépasse 0,8 ou si σ dépasse 2 mois, la calibration des vitesses est revue avant l'essai (3.N-8).
4. **J3, coût** : part du bloc mesurée dans `tests/invariants/test_budget.py`, d'au plus 0,48 ms par pays-pas.
5. **Remesure S1** sur le prototype v2.0 (confirmation de 3.B-3). Le verdict est publié quel qu'il soit et ne change pas la recommandation.

**Lectures possibles, à trancher par le mainteneur.**
- **(a) Valorisation des stocks.**
  - (i) Coût moyen pondéré : conforme à la l. 520 de `sec:cadre`, gain réalisé à la vente, ρ̄_IN = 0,996057, faible dépendance à n_a.
  - (ii) Coût unitaire courant de Godley et Lavoie : ρ = 1 exactement et forme de la littérature, mais gain de détention latent inscrit dans la ligne 4 (+4,2 sur 138,6 dans l'exemple de 3.N-4). C'est une réévaluation dans une ligne de transaction : décision citant M22.
  - Avis : (i).
- **(b) Ordre interne de la phase 4.**
  - (i) « travail, puis production » (emploi au bloc 3) ;
  - (ii) « production, puis travail » (emploi au bloc 2, salaires au bloc 3).
  - Les deux modifient la l. 486 et demandent une décision citant M22, sur un contrat partagé. Avis : (i), pour que tout ce qui touche au marché du travail relève d'un seul bloc.
- **(c) Base des anticipations.** (i) La demande adressée, servie ou non (v2.0) ; (ii) les ventes (v1.5, Godley et Lavoie). Avis : (i), parce qu'une pénurie ne s'auto-entretient pas et que l'état stationnaire est identique.
- **(d) Nombre de secteurs.** Avis : J = 1. J = 2 est la seule autre valeur défendable.
- **(e) Capacité.** (i) Indicateur sans plafond ; (ii) plafond min(y*, y^cap). Avis : (i), à cause de l'instabilité 15 et d'une borne qui serait active en reprise.
- **(f) Conversion de g_pr.**
  - (i) Linéaire, g_pr/n_a : croissance effective de 2,0184 % pour 2 %, publiée.
  - (ii) Calibrée sur une croissance effective (1,9819 % pour 2 %) : seconde règle de conversion, à harmoniser avec #24 (frontière avec `monnaie`).
  - Avis : (i).
- **(g) Priorité du rationnement.** (i) Proportionnelle ; (ii) l'État d'abord. Avis : (i), sans paramètre. À soumettre à `jeu`.

**Tableau levier → indicateur → délai → contrepartie (critère 11 (c), option C)** :

| Levier | Indicateur du bloc | Délai (tours entiers) | Contrepartie visible le même tour |
|---|---|---|---|
| Dépense publique | Ventes, stocks en mois, demande non servie ; puis production et emploi | 0 pour les ventes et les stocks ; 1 pour la production | Baisse des stocks (ligne 4 négative) ou demande non servie (conforme à `tab:leviers-cadre`) |
| Impôts sur les ménages | Ventes au tour n+1 (budget de phase 2 lu à l'ouverture, fiche 5), puis production | 1 pour les ventes ; 2 pour la production | Hausse des stocks au tour n+1 |
| Taux, par l'investissement | Ventes d'équipement, puis production | Fixé par les fiches 6 et 7 : au mieux 0, puis 1 | Stocks |

**Ce que l'option retenue coûte en fidélité.**
- Pas de substitution entre capital et travail, pas de produit marginal : le partage de la valeur ajoutée est confié à la marge (fiche 4). La formule de K/Y de la v2.0 (acquis du § 8, R) ne se transpose pas et sera refaite par la fiche 6.
- Pas de stocks d'intrants ni de secteurs, jusqu'aux jalons J5 à J7.
- Pas de rétention de main-d'œuvre dans le bloc, qui relève de la fiche 3.
- Au regard de Godley et Lavoie, deux termes sont ajoutés (tendance et croissance de la cible) et la valorisation est celle de la norme IAS 2 plutôt que le coût courant.

**Constats transmis aux autres fiches.**
- **Fiche 3** : ordre de la phase 4 ; contrainte d'offre de travail ; un retard d'emploi éventuel rend la boucle du second ordre (module √(1 − λ_N/n_a)).
- **Fiche 4** : UC est partagé ; sous J = 1, la boucle de l'amortissement dans le prix devient un point fixe scalaire.
- **Fiche 6** : ρ̄_K = 0,7791 ; définition de K/Y ; Q2.

## 6. Avis de l'expert consulté

Sans objet, parce que `docs/blocs/README.md` § 1 ne désigne pour ce bloc aucun expert de fond consulté (`monnaie` non consulté) ; l'avis de `jeu` figure au § 7.

## 7. Avis de `jeu`

*`jeu`, 02/10/2026 (issue #34), sur la fiche à la tête `8e9fe38` (branche `claude/j1-cadre-production`).*

**Chiffres.** Aucun moteur n'existe encore (`src/nations/blocs/` ne contient que `__init__.py`). J'ai écrit une maquette indépendante du socle 3.N avec J = 1 (équations N1 à N7, population active constante, prix fixes), qui n'importe pas les scripts de `macro`. Je l'ai exécutée le 02/10/2026 par `uv run python <scratchpad>/jeu_c.py`, puis `jeu_c2.py` et deux commandes en ligne ; les scripts sont hors dépôt.
- **Exemple daté M5 (G +1 % aux tours 1 à 12, soit 0,2 % de la demande ; m = 0).** Production : +0,000 % au tour 1, +0,084 % au tour 2, +0,142 % au tour 3, +0,182 % au tour 4, +0,245 % au tour 9, +0,239 % au tour 13, +0,152 % au tour 14, −0,003 % au tour 18, −0,030 % au tour 24. Avec m = 0,6 : +0,449 % au tour 9, +0,577 % au tour 13, +0,121 % au tour 24. Mes chiffres concordent avec M5 à 0,001 point près, ce qui relève de l'arrondi.
- **Même choc multiplié par 10 (G +10 %, soit 2 % de la demande).** Production : +0,836 % au tour 2, +2,450 % au tour 9, −0,301 % au tour 24. Stocks de clôture : 1,380 mois au tour 1, 1,361 au tour 4, 1,445 au tour 18.
- **Contrepartie du tour 1.** Les stocks passent de 1,4000 à 1,3980 mois de ventes. La variation des stocks rapportée aux ventes du tour passe de +0,233 % à +0,033 %.
- **Ratio restitué stationnaire** (forme de M22, lecture (e) : stock de clôture / moyenne mensuelle des ventes des 12 derniers tours) : 1,4152 mois, et non 1,4.
- **Cycle avec demande induite** (choc G +1 % aux tours 1 à 12) :
  - m = 0,6 : pic à +0,577 % au tour 13, creux à −0,105 % au tour 40 (0,18 fois le pic) ;
  - m = 0,8 : pic à +0,797 % au tour 13, creux à −0,248 % au tour 60 (0,31 fois le pic).
- **Plafond d'emploi.** Hypothèses : chômage initial de 5 %, emploi ajusté sans retard, prix fixes ; demande permanente en hausse de 10 %.
  - L'emploi atteint son plafond au tour 3.
  - La production visée non réalisée, (y* − y)/y*, vaut 1,72 % au tour 3, 11,13 % au tour 12 et 16,31 % au tour 24.
  - Le stock en mois de ventes effectives vaut 1,182 au tour 1, 0,706 au tour 12 et 0,208 au tour 24.
  - La **première demande non servie apparaît au tour 30** (3,82 %, puis 4,08 %).
  - Avec une demande en hausse de 6 % seulement, aucune demande non servie n'apparaît en 121 tours.
- **Taux d'utilisation.** Avec t̄u = 0,8 et un emploi au plafond depuis 5 % de chômage, tu = 0,842. Après 48 tours sans investissement (δ = 5 %), K^vol vaut 0,818 fois sa valeur initiale et tu = 0,978.
- **Valorisation.** Écart à l'état stationnaire entre le résultat sous le coût courant (lecture (a)(ii)) et sous le coût moyen pondéré (a)(i), avec une marge μ = 0,25 (**hypothèse**) : 0,007 % de la marge brute à π̄ = 2 %, 0,110 % à 10 %, 2,207 % à 50 %.

**Question ludique de la fiche.** Le bloc n'ouvre aucun levier. Il fixe trois choses :
- **ce que le joueur voit de l'offre** quand il agit sur la demande : délai, ampleur, contrepartie ;
- **les signaux de tension** : stocks, pénurie, utilisation ;
- **le nombre de marchés** affichés.

La question est donc : chaque grandeur affichée a-t-elle un sens, une cause que le joueur peut relier à ses décisions et une conséquence ?

### 7.A Option A — v1.5 (brièvement)

- **Ce que voit le joueur** :
  - un tick hebdomadaire, contraire à M22 ;
  - huit secteurs, dont aucun n'est l'objet d'un levier au socle ;
  - un taux d'utilisation dégénéré (proche de 1), donc muet ;
  - une transition initiale de 3 à 5 ans (l. 2080, R).
- **Leviers** : aucun propre. La contrepartie de ΔIN n'est pas montrable, ΔIN n'étant pas défini (3.A-6 (ii)).
- **Stratégies** : sans objet.
- **Risques** :
  - *piège sans signal* : la transition initiale fait dériver la partie avant toute décision, et le joueur hérite d'une trajectoire qu'il n'a pas causée ;
  - *création de stock* par la loi des stocks telle qu'écrite (3.A-6 (i)) : des biens qui apparaissent sans production, ce qui est inexplicable.
- **Verdict** : **à revoir**.

### 7.B Option B — v2.0 (brièvement)

- **Ce que voit le joueur** :
  - un cycle propre de 6 ans (3.B-8), relancé par la transition initiale (état initial non résolu, 3.B-3) : une oscillation sans aucune décision du joueur ;
  - des pénuries dès qu'un surcroît de demande dépasse 0,16 %, alors que des stocks existent (borne active, 3.B-3).
- **Leviers** : aucun propre.
- **Stratégies** : sans objet.
- **Risques** :
  - *comportement contre-intuitif* non explicable (« les entrepôts sont pleins et les rayons vides ») ;
  - un prix relatif de l'équipement qui dérive de 12,8 % sur 60 ans (R), sans cause lisible ni levier qui le corrige ;
  - un taux d'utilisation écrêté par `clip` : le signal se tait précisément quand il serait utile.
- **Verdict** : **à revoir**.

### 7.C Option C — socle 3.N, J = 1

- **Ce que voit le joueur** :
  - Une hausse de la dépense publique au tour n se lit le tour même dans les ventes et dans la variation des stocks, puis à partir du tour n + 1 dans la production et l'emploi.
  - La production dépasse les ventes pendant la reconstitution des stocks (pic au tour 9 pour un choc qui dure 12 tours).
  - Un léger « trou d'air » suit la fin de la relance : −0,030 % au tour 24 pour G +1 %, −0,301 % pour G +10 %.
  - Chaque étape s'explique par une identité affichable : production = ventes + variation des stocks.
- **Ampleur** : la réponse est linéaire. G +1 % (0,2 point de demande) donne un effet à la limite du perceptible ; un levier de l'ordre d'un point de PIB (G +5 %) donne +0,4 % de production au tour 2 et +1,2 % au tour 9 avec m = 0, ce qui est nettement perceptible.
- **Leviers** : le bloc n'en ouvre aucun (conforme à `docs/exigences.md` § 2.1, point 1). Le tableau levier → indicateur → délai → contrepartie du § 5 est lisible.
- **Stratégies** : aucune stratégie dominante n'est créée par le bloc. Deux points de vigilance relèvent d'autres fiches :
  - **(i) Le chômage comme bouton de la dépense.** Sous la technique de Leontief, avec une productivité exogène et un emploi sans retard, le taux d'emploi est exactement l'écart de production. G devient alors un réglage du chômage presque instantané, au tour suivant. Son coût doit apparaître ailleurs : salaires et prix quand le chômage est bas (fiches 3 et 4), dette (fiche 9). Sinon, la gestion de la demande domine toutes les autres approches.
  - **(ii) Aucun levier n'agit sur l'offre au socle 3.N** (constat de `jeu`, non relevé au § 5). La capacité est un indicateur sans plafond, la production ne dépend que de pr·N, et pr suit une tendance exogène. L'investissement n'a donc qu'un effet de demande, et la croissance tendancielle est la même quelle que soit la politique suivie. Pour le simulateur (J1 à J4), c'est acceptable comme simplification déclarée. Pour le jeu (J7), cela restreint le principe « plusieurs approches viables » à la gestion du cycle. Le point vaut pour C comme pour D : il tient au socle 3.N-1, pas au nombre de secteurs. Issue proposée ci-dessous.
- **Risques** :
  - *Réponse imperceptible* : pour les petits leviers seulement, et seulement si la restitution n'affiche que des niveaux. Le stock en mois de ventes bouge de 1,400 à 1,398 au tour 1 pour G +1 %, ce qui est invisible à deux décimales. La variation des stocks rapportée aux ventes bouge de +0,23 % à +0,03 %, ce qui est visible.
  - *Effet instantané sans coût* : aucun dans le bloc ; voir le point (i) ci-dessus pour les autres fiches.
  - *Piège sans signal* : aucun, à condition que la restitution suive le § 9 (point 3). La demande non servie est un signal **tardif** : 29 tours après le premier signal dans mon cas d'école.
  - *Comportement contre-intuitif* : la boucle devient explosive à λ_v = 12 (alternance d'un mois sur l'autre, 3.N-8). Ce serait illisible ; la réserve 3 du § 5 le prévient et je la soutiens.
- **Verdict** : **lisible**, sous les clarifications sur les indicateurs données plus bas.

### 7.D Option D — socle 3.N, J = 2

- **Ce que voit le joueur** : tout ce que voit C, plus l'emploi et le prix du secteur d'équipement. Un choc sur l'investissement, par exemple le taux par la fiche 6, frappe d'abord ce secteur.
- **Leviers** : aucun nouveau (3.J (e)). La composition de G est inerte faute de capital public.
- **Stratégies** : aucune nouvelle.
- **Risques** :
  - *Comportement contre-intuitif* : un prix relatif p_2/p_1 qui dérive (instabilités 9 à 11 et 14 ; 12,8 % sur D1, R) est le pire signal pour un joueur. Il bouge sans que le joueur l'ait causé, il ne peut pas le corriger et l'interface ne peut pas l'expliquer.
  - L'apport perçu, un investissement qui se voit à part, s'obtient sous C sans prix relatif : il suffit de restituer les ventes par acheteur (C^vol, G^vol, I^vol), déjà exécutées en lignes 1 à 3.
- **Verdict** : **à revoir pour le socle**. Ce n'est pas une objection à deux secteurs en soi : un secteur se justifie quand il apporte un levier (capital public, politique industrielle) ou un choc propre (J5, J6).

### Réponses aux huit questions de `macro`

1. **J = 1 contre J = 2.**
   - Sur 60 à 120 tours, le secteur d'équipement distinct ne se perçoit que comme une répartition de l'emploi et un prix relatif.
   - L'information utile, la chute de l'investissement après une hausse de taux, est déjà lisible sous C par les ventes par acheteur.
   - Le coût perçu de D est un prix relatif qui peut dériver sans cause lisible.
   - Pour un jeu inspiré de Victoria 3, le joueur s'attend à des marchés. Mais un marché sans levier ni choc propre est un décor, et ici un décor instable. Les secteurs doivent arriver avec leur raison d'être ludique : énergie et alimentation (chocs d'offre, échanges) au J5, construction au J6.
   - **J = 1**.
2. **Indicateurs du tour** : tableau ci-dessous. Un taux d'utilisation au-delà de 100 % est compris (« au-delà de la capacité normale, heures supplémentaires ») s'il est libellé ainsi et affiché à côté de son niveau normal (80 %). Il est pratiquement **inatteignable en jeu normal** : 0,842 au plafond d'emploi ; 0,978 seulement après 4 ans sans aucun investissement. Le vrai risque n'est pas le dépassement de 100 % : c'est un indicateur **sans conséquence**. Si rien ne dépend de tu, ni l'investissement (fiche 6) ni les prix (fiche 4), le joueur apprendra à l'ignorer.
3. **Délai et ampleur.**
   - Le délai d'un tour est net : la restitution distingue « ventes et stocks au tour n » de « production au tour n + 1 ».
   - L'ampleur de G +1 % (+0,08 %, puis +0,25 %) est sous le seuil de perception dans un jeu sans contrefactuel, puisque la croissance tendancielle est de 0,165 % par tour. À G +5 % ou +10 %, c'est perceptible.
   - Il ne faut **pas de nouvel indicateur économique**. Il faut :
     - (a) restituer au tour la ligne d'identité : demande adressée, ventes, production, variation des stocks (en % des ventes) ;
     - (b) dans le simulateur (J4), l'écart au scénario de contrôle apparié (O2) ;
     - (c) sous C, le taux d'emploi, qui sert d'écart de production sans calcul supplémentaire.
   - Une seule grandeur restituée est à ajouter, sans variable d'état : la **production visée non réalisée** (y* − y)/y*. Voir la question 5.
4. **Cycle des stocks amorti.**
   - Avec m = 0,6 ou 0,8, le joueur voit en une partie une bosse, puis un creux de 0,18 à 0,31 fois le pic, 27 à 47 tours plus tard. C'est perçu comme une « relance suivie d'un trou d'air », moins comme un cycle.
   - **C'est souhaitable** : une décision a un écho différé, émergent, explicable par les stocks au-dessus de la normale. Le joueur qui relance à nouveau dans le creux apprend la procyclicité à ses dépens, ce qui est de bon jeu.
   - Deux conditions :
     - la période reste dans la bande de 3 à 8 ans et amortie ; un cycle plus court qu'un an serait du bruit, un cycle explosif un piège ;
     - le signal précurseur du creux (stocks au-dessus de leur niveau normal) est affiché. Pour G +1 % il est minuscule (+0,008 mois), donc seuls les leviers d'un point de PIB et plus produisent un écho visible.
   - Le cycle propre ne doit jamais apparaître **sans impulsion**. C'est le cas sous C, puisque l'état initial est résolu.
5. **Rationnement et signal de pénurie.**
   - **Proportionnel, préféré pour le socle.** La dépense publique est elle aussi rationnée, et le joueur reçoit la sanction directe de la pénurie sur son propre levier : « votre dépense n'a été exécutée qu'à 91 % ». Restitution demandée : dépense publique demandée / exécutée, en u.m.
   - **« L'État d'abord »** rend le joueur immunisé contre la pénurie qu'il cause. L'éviction des ménages devient totale et ne se voit que si la demande non servie des ménages est affichée. C'est un trait réaliste d'une économie planifiée ou de guerre (v1.5 l. 771) : elle doit être un **levier** du mode planifié (J7), avec sa contrepartie visible (demande des ménages non servie, dépôts non dépensés), non une règle du socle. La compatibilité d'une priorité réglable par levier avec la règle « aucun drapeau de mode » (ADR 0002) est à confirmer par `architect`.
   - **Risque à tester au J4** (scénario adverse) : sous rationnement proportionnel, sur-commander est gratuit si la part non exécutée de G reste au Trésor sans coût. L'État capte alors une plus grande part des biens. Ce n'est pas bloquant, car l'éviction des ménages est visible, mais c'est à documenter.
   - **La demande non servie est un mauvais signal précurseur** : nulle en jeu normal, elle n'apparaît qu'une fois les stocks épuisés (tour 30 dans le cas d'école, 27 tours après la saturation de l'emploi). C'est un indicateur de crise, pas d'alerte. Les signaux précurseurs sont :
     - les stocks en mois de ventes sous leur niveau normal ;
     - la **production visée non réalisée** (y* − y)/y*, positive dès que l'emploi plafonne (1,72 % au tour 3, 11,13 % au tour 12). Elle se calcule à partir de deux grandeurs que le bloc tient déjà ; elle est restituée, ce n'est ni un flux ni une variable d'état.
6. **Valorisation des stocks.**
   - Le joueur ne s'en soucie pas en régime normal : l'écart vaut 0,11 % de la marge brute à 10 % d'inflation, 2,2 % à 50 % (μ = 0,25, hypothèse).
   - Sous une hyperinflation, les « profits d'inflation » imposés sont un phénomène réel, mais de niche. Ils ne justifient pas une réévaluation dans une ligne de transaction, qui demanderait une décision citant M22.
   - Pas de préférence ludique : (i) convient.
7. **Chômage en retard sur la production, ou au même tour.**
   - **Préférence pour un retard modéré par ajustement partiel** (fiche 3), pour deux raisons :
     - (a) La rétention de main-d'œuvre crée un **signal précurseur** : la productivité apparente y/N baisse sous sa tendance et les profits se compriment avant les licenciements (O3).
     - (b) Elle crée le dilemme classique « la production repart, le chômage tarde ». C'est une tension politique lisible (le chômage est l'indicateur le plus visible pour un État). Elle retire au joueur le réglage du chômage au tour près (point (i) du 7.C).
   - Conditions :
     - demi-vie de l'ordre de 2 à 6 tours ;
     - restitution de la productivité apparente rapportée à sa tendance ;
     - mesure par `macro` de la boucle combinée (cycle de l'emploi, 52 mois à la vitesse de la v2.0, plus cycle de Metzler), pour que deux cycles superposés restent lisibles.
   - La justification empirique (loi d'Okun, rétention) n'est pas sourcée dans la fiche (3.N-1) : elle relève de `macro`. Mon avis est une préférence de conception.
8. **Mode planifié (J7).**
   - **Jouable à bien unique, en forme réduite**, avec trois leviers : un objectif de production ou d'emploi par directive, le partage entre consommation, investissement et dépense publique, et un prix administré (fiche 4) qui produit du rationnement.
   - Le surplomb monétaire de la v1.5 (Ω) **émerge** déjà du socle : le budget non dépensé reste en dépôts (3.N-3). C'est un bon point d'émergence.
   - Forces : plein emploi par directive, aucun cycle des stocks. Faiblesses : rationnement, surplomb, pénalité de productivité.
   - Ce que J = 1 ne permet pas :
     - la tension du plan au sens de Leontief et les priorités entre secteurs, qui exigent J ≥ 2 et des intrants ;
     - la pénalité de complexité à la Hayek, croissante avec le nombre de biens (v1.5, `sec:plan`) ;
     - surtout, la **croissance extensive par accumulation forcée**, qui exige un capital productif, absent du socle 3.N (point (ii) du 7.C).
   - Le tableau entrées-sorties n'est donc pas requis pour que le mode planifié soit jouable. Un capital productif l'est pour que ce mode ait sa stratégie signature. L'indexation par j du socle (3.J (d)) laisse la question ouverte jusqu'à la fiche du J7, sans réécrire M24.

### Indicateurs du tour (critère 11 (a))

| Indicateur | Verdict | Motif ou point à clarifier |
|---|---|---|
| Indice de production (volume, base 100 = état initial résolu ; tour et 12 tours) | **lisible** | Afficher le glissement annuel (12 tours) et la croissance tendancielle de référence, avec le taux effectif de 2,0184 % et non le paramètre (lecture (f)) |
| Taux d'utilisation | **à clarifier** | Libellé « utilisation de la capacité normale des équipements », niveau normal affiché, dépassement de 100 % permis et expliqué. Surtout, dire ce qu'il déclenche (investissement, fiche 6 ; prix, fiche 4) ; sans conséquence, il est à retirer de la restitution |
| Stocks en mois de ventes | **à clarifier** | Niveau normal affiché dans **la même définition** que l'indicateur (1,4152 mois selon la lecture (e) de M22, et non 1,4), sinon le joueur voit un écart permanent à l'état stationnaire. Indicateur lent : le compléter par la variation des stocks en % des ventes du tour, qui reflète le choc le tour même |
| Demande non servie (%) | **à clarifier** | Signal de crise, non précurseur ; à ventiler par acheteur, avec la dépense publique demandée / exécutée en u.m. Précurseur à restituer : production visée non réalisée, (y* − y)/y* |
| Emploi | **lisible** | Sous C sans retard, c'est l'écart de production ; avec un retard (fiche 3), ajouter la productivité apparente rapportée à sa tendance |

### Préférence motivée

**Option C**, comme `macro`, mais pour une autre raison. `macro` la retient pour ses exigences (état stationnaire exact, aucune instabilité connue) et pour sa simplicité. Je la retiens parce que **chaque grandeur qu'elle affiche a une cause que le joueur peut relier à une décision**. Sous D, le prix relatif de l'équipement peut bouger sans cause lisible ni levier. Sous A et B, l'état initial non résolu fait bouger la partie avant le premier tour.

**Classement** : C > D > B > A, identique à celui de `macro`. D n'est pas illisible ; il paie un mécanisme sans usage ludique au socle.

**Accords et réserves sur les lectures du § 5** :
- (a) (i), sans préférence ludique ;
- (b) (i), sans enjeu ludique ;
- (c) (i), préférée : sous (ii), une pénurie persiste sans que les entreprises la voient, et le joueur ne peut se l'expliquer ;
- (d) J = 1 ;
- (e) (i), sous la condition du tableau ci-dessus ;
- (f) (i), en restituant le taux effectif ;
- (g) (i) au socle, et la priorité de l'État comme levier du mode planifié au J7.

**Conditions demandées au § 9** (aucune n'est une réserve sur C) :
1. **Restitution au tour** de la ligne d'identité : demande adressée, ventes par acheteur, production, variation des stocks en % des ventes, demande non servie par acheteur. Pour l'État : dépense demandée / exécutée.
2. **Niveaux normaux** affichés dans la définition exacte de l'indicateur (stocks : 1,4152 mois en restitution ; utilisation : t̄u).
3. **Production visée non réalisée**, (y* − y)/y*, ajoutée aux grandeurs restituées du § 1.1, comme signal précurseur de pénurie.
4. **Taux d'utilisation** : la fiche 6 (ou la fiche 4) dit ce qu'il déclenche ; sinon, il sort de la restitution.
5. **Fiche 3** : retard d'emploi par ajustement partiel préféré par `jeu`, avec la mesure de la boucle combinée emploi – stocks par `macro`.
6. **Test O2 au J4** : la dépense publique à +1 % et à +5 % du flux mensuel, plus un scénario adverse de sur-commande publique sous pénurie.
7. **Avant J7** : le point « aucun levier n'agit sur l'offre » est traité (issue ci-dessous).

## 8. Décision du mainteneur

- **Numéro** : M24 (reporté dans `docs/feuille-de-route.md`, § 4).
- **Date** : 02/10/2026.
- **Option retenue** : **C**, socle commun du § 3.N avec un bien unique (J = 1), équations indexées par j dès le socle. Lectures du § 5 :
  - (a) valorisation des stocks au **coût moyen pondéré** (conforme à la l. 520 de `sec:cadre`, sans réévaluation dans une ligne de transaction) ;
  - (b) ordre interne de la phase 4 : **travail, puis production** ; l'emploi est tenu par le bloc 3 et lu par le bloc 2. Cette lecture modifie un contrat partagé (`tab:phases`, l. 486) : décision citant M22, consignée par ADR ;
  - (c) anticipations fondées sur la **demande adressée**, servie ou non ;
  - (d) **J = 1** ;
  - (e) capacité tenue comme un **indicateur sans plafond** ;
  - (f) conversion **linéaire** de la croissance de productivité, g_pr/n_a, la croissance effective (2,0184 % pour 2 %) étant publiée. *Révisée par M25 (b) le 03/10/2026 (ADR 0008, pt I.5) : conversion géométrique, (1 + g_pr)^{1/n_a} par pas ; la croissance effective de 2,0184 % n'existe plus. Chiffres d'état stationnaire recalculés sous (G) et visés par le mainteneur le même jour (`docs/feuille-de-route.md` § 4) ; § 3.N et § 9 corrigés, § 4 à 7 laissés tels quels.* ;
  - (g) rationnement **proportionnel** au socle ; la priorité de l'État relève d'un levier éventuel du mode planifié (J7).
  - Q4 : volume du capital au bloc 2, ajustement de l'emploi au bloc 3, à confirmer par les fiches 3 et 6.
- **Motifs** : le mainteneur a retenu les recommandations concordantes de `macro` (§ 5) et de `jeu` (§ 7), sur toutes les lectures. Motifs dans ses propres mots : à compléter par le mainteneur s'il le souhaite.
- **Conditions et réserves** : les cinq réserves du § 5, avec leurs seuils écrits avant l'essai (état stationnaire, vitesses, boucle fermée et coût au J3 ; remesure S1, dont le verdict ne change pas la décision) ; les sept conditions de restitution de `jeu` (§ 7) pour le § 9.
- **Ce qui est écarté et pourquoi** : A (v1.5) et B (v2.0), qui échouent au critère 4 (ratio stocks / ventes stationnaire dépendant des vitesses) et aux critères 1 (b) et 3 (b) ; B a en outre une borne active à l'état stationnaire et un cycle propre de 6 ans ; D (J = 2), qui n'ajoute aucune identité vérifiable et paie un prix relatif à stabiliser sans levier qui l'exploite ; la valorisation au coût courant ; l'ordre « production, puis travail » ; le plafond de capacité ; la priorité de l'État au socle.
- **Issue liée** : « aucun levier n'agit sur l'offre au socle 3.N » (proposée par `jeu`, créée sur accord du mainteneur), à instruire aux fiches 4 et 6, au plus tard avant J7.

## 9. Conséquences de la décision

*Rédigé par `macro` (expert pilote), 02/10/2026, d'après M24 (§ 8). « Nk » désigne l'équation k du § 3.N ; « lecture (x) », la lecture du § 5 retenue en (i) par M24.*

*Annotation du 04/10/2026 (validation de la spécification par `macro`, remesure ; décision inchangée) : le γ de cette fiche désigne la croissance réelle par pas, (1 + g)^{1/n_a} − 1. Il est distinct de γ^e_t = Γ^e_t − 1, croissance nominale attendue (ADR 0010, M30), seul γ de la spécification, qui écrit la croissance réelle par pas en clair. Les tests repris au J3 suivent la notation de la spécification.*

### 9.1 Labels d'équation

**Au jalon J1, aucun label** (#34, jalon 4). La section `sec:production` est écrite sans `\label{eq:…}`. Chaque mécanisme figure dans un encadré `proposee` citant M24, avec ses équations en `equation*` (`CONVENTIONS.md` § 4.1 ; règle 1 de la concordance).

**Labels à créer au jalon où le module est écrit** (J3, `src/nations/blocs/production.py`). Radical : `production`. `coder` pose une balise par label ; `docwriter` retire l'encadré et pose le label dans le même passage.

| Label | Ce que l'équation détermine | Équation | Statut | Provenance | Couche |
|---|---|---|---|---|---|
| `eq:production-ventes-anticipees` | v^e_{j,t+1} = (1 + g)^{1/n_a}[(1 − λ_v/n_a) v^e_{j,t} + (λ_v/n_a) d_{j,t}], phase 5 | N1 | approchée | M24, lecture (c) ; M25 (b) ; modèle DIS de Godley et Lavoie modifié (tendance) ; v2.0 (anticipation sur la demande, l. 1418) | `blocs/` |
| `eq:production-stock-cible` | IN^vol*_{j,t} = n_a σ_j v^e_{j,t}, phase 2 | N2 | choix de conception | M24 ; Godley et Lavoie (DIS) | `blocs/` |
| `eq:production-visee` | y*_{j,t} = max{0, v^e + [(1 + g)^{1/n_a} − 1] IN^vol* + (λ_IN/n_a)(IN^vol* − IN^vol)}, phase 2 ; plancher physique déclaré | N3 | approchée | M24 ; M25 (b) ; Godley et Lavoie (DIS) avec un terme de croissance de la cible | `blocs/` |
| `eq:production-demande-travail` | N*_{j,t} = y*_{j,t}/pr_{j,t}, phase 2, transmise au bloc 3 | N4 | dérivée (Leontief) | M24 ; Godley et Lavoie (DIS) | `blocs/` |
| `eq:production-realisee` | y_{j,t} = min{y*_{j,t}, pr_{j,t} N_{j,t}}, phase 4, après le bloc 3 | N5 | dérivée (Leontief) | M24, lecture (b) | `blocs/` |
| `eq:production-ventes` | v_{j,t} = min{d_{j,t}, IN^vol_{j,t} + y_{j,t}} ; rationnement proportionnel au taux v/d, phase 5 | N6 | dérivée (disponibilité) ; choix de conception (proportionnalité) | M24, lecture (g) ; v1.5 l. 771 | `blocs/` |
| `eq:production-stock-volume` | IN^vol_{j,t+1} = IN^vol_{j,t} + y_{j,t} − v_{j,t} | N7 | dérivée | M24 | `blocs/` |
| `eq:production-cout-unitaire` | UC_{j,t} = W_t/pr_{j,t} (plus Σ_k a_kj p_k quand il y aura des intrants, J5), phase 2 | N8 | choix de conception | M24 ; M26 (UC écrit par le bloc 2 en phase 2) | `blocs/` (lu par le bloc 4) |
| `eq:production-variation-stocks` | ligne 4 : ΔIN = UC·y − cm·v, avec cm = (IN + UC·y)/(IN^vol + y) ; ΔIN = 0 si IN^vol + y = 0 | N8 | choix de conception (coût moyen pondéré ; IAS 2 § 25, résumés secondaires) | M24, lecture (a) | `blocs/` |
| `eq:production-productivite` | pr_{j,t+1} = pr_{j,t}(1 + g_pr)^{1/n_a} | N9 (3.N-1) | choix de conception | M24, lecture (f), révisée par M25 (b) (ADR 0008, pt I.5) | `blocs/` |
| `eq:production-capital-volume` | K^vol_{j,t+1} = (1 − δ/n_a) K^vol_{j,t} + I^vol_{j,t}, livraisons après rationnement, phase 5 | N10 | dérivée | M24, Q4 | `blocs/` |
| `eq:production-capacite` | y^cap_{j,t} = K^vol_{j,t}/(n_a κ_j) ; tu_{j,t} = y_{j,t}/y^cap_{j,t}, sans plafond | N11 (3.N-1) | choix de conception | M24, lecture (e) | `blocs/` |

Les douze labels respectent l'expression régulière de `CONVENTIONS.md` § 2.1.

**Grandeurs restituées** (demande non servie, production visée non réalisée, stocks en mois, variation des stocks en pourcentage des ventes, niveaux normaux) : ce sont des définitions de la couche `observation/`. Elles ne portent un label que lorsque le radical de cette couche sera fixé (fiche 1 § 9.8, n° 7, toujours ouvert dans `CONVENTIONS.md` § 2.1). D'ici là, ce sont des définitions non numérotées de `sec:production`.

**Correspondance à corriger dans la fiche** : N9 et N11 sont citées au § 3.C (« N1 à N11 ») mais pas numérotées au § 3.N-1. N9 désigne la productivité, N11 la capacité et le taux d'utilisation.

### 9.2 Paramètres

Cinq paramètres, à porter dans `tab:calibration` au jalon J1, sans `\code{}` avant le code. Les noms dans le code sont des propositions, que `coder` peut changer.

| Symbole | Nom proposé | Valeur | Unité | Source | Équation |
|---|---|---|---|---|---|
| λ_v | `vitesse_ventes_anticipees` | 3 (indicative, fixée au J3) | par an | M24 ; 3.N-8 (domaine de boucle fermée) | `eq:production-ventes-anticipees` |
| λ_IN | `vitesse_correction_stocks` | 1,5 (indicative, J3) | par an | M24 ; 3.N-8 | `eq:production-visee` |
| σ | `stock_cible` | 1,4/12 ≈ 0,1167 (indicative) | années de ventes, restituées en mois (12σ) | ordre de grandeur Census MTIS 2025, 1,36 à 1,39 mois (extraits ; source primaire non lue) | `eq:production-stock-cible` |
| g_pr | `croissance_productivite` | à fixer avec O1 (J3) | par an, taux de croissance, conversion géométrique (ADR 0008, pt I.1 et I.3) | M24, lecture (f), révisée par M25 (b) | `eq:production-productivite` |
| κ | `capital_par_production_normale` | à fixer avec la fiche 6 (t̄u ≈ 0,8 visé ; G.17, 79,4 % sur 1972–2025, extrait non lu) | années | M24, lecture (e) | `eq:production-capacite` |

**Conditions déclarées, contrôlées au chargement, jamais par écrêtage** : λ_v ≤ n_a et λ_IN ≤ n_a. Le domaine de stabilité en boucle fermée (réserve 3 du § 5) se vérifie au J3 par le test 9.6.

**Ce qui n'est pas un paramètre** :
- **J** : c'est la dimension du schéma d'état, fixée à 1 par M24 ;
- **δ** : paramètre du cadre (ligne 8), dont la valeur relève de la fiche 6 ;
- **g** : dérivé, g = (1 + g_pr)(1 + g_N) − 1, où g_N vient du bloc 3 (M25 (d)) ;
- **ρ̄_IN, ρ̄_K et t̄u** : grandeurs de l'état stationnaire ;
- les niveaux normaux restitués (9.5), publiés par le script d'état stationnaire (M19). La croissance effective de 2,0184 % n'existe plus sous (G) (*révisé par M25 (b)*, 03/10/2026).

### 9.3 Ce qui reste paramétrable après la décision

**Sans rouvrir M24** (calibration au J3, visa de l'expert pilote ; ou décision de la fiche concernée) :
- les valeurs de λ_v, λ_IN, σ, κ et g_pr, dans leurs conditions déclarées ;
- la règle d'emploi du bloc 3 (ajustement partiel, contrainte d'offre de travail) : N5 vaut pour toutes ;
- les règles de prix (fiche 4), d'investissement et de distribution (fiche 6), et les plans de demande (fiches 5 et 9) ;
- l'ajout, au jalon J5, d'un terme d'intrants dans UC (N8).

**Par une décision M-m citant M24** :
- J > 1 (jalons J5 à J7, par l'indexation j sans réécrire N1 à N11) ;
- la valorisation des stocks (le coût courant demanderait aussi M22) ;
- la base des anticipations ;
- un plafond de capacité ;
- une priorité de rationnement (au J7, comme levier du mode planifié ; sa compatibilité avec la règle « aucun drapeau de mode » de l'ADR 0002 est à faire confirmer par `architect`, selon le point de `jeu`) ;
- l'ordre de la phase 4 (aussi M22).

**Aucun drapeau de mode** (ADR 0002) : une seule règle par équation.

### 9.4 Interfaces

**Phases, lectures et écritures du bloc 2** :

| Phase | Lit | Écrit, ou propose au noyau |
|---|---|---|
| 2 | ouverture : v^e, IN^vol, pr | y*, IN^vol*, N* (vers le bloc 3) ; aucun autre plan de la phase 2 n'est lu |
| 4 | phase 2 ; N_t, écrit **avant lui** par le bloc 3 dans la même phase (ordre « travail, puis production », M24 (b)) | y, y^cap, tu ; production visée non réalisée (restituée) |
| 5 | plans de demande des ménages, de l'État et des entreprises, en u.m. (phase 2) ; prix p_t du bloc 4, écrit **avant lui** ; W_t (phase 1) ; y (phase 4) | v, taux de service v/d, volumes servis par acheteur, d − v par acheteur ; **ligne 4** (ΔIN) ; IN^vol_{t+1}, K^vol_{t+1}, v^e_{t+1}, pr_{t+1} |

**Ordre interne de la phase 5**, déclaré par les fiches (l. 486, sans décision citant M22) : prix (bloc 4), puis production (bloc 2 : ventes, rationnement, ligne 4), puis les acheteurs (blocs 5, 6 et 9), qui proposent les lignes 1, 3 et 2 sur les volumes servis multipliés par p_t. Leur ordre entre eux est indifférent, puisqu'ils ne se lisent pas les uns les autres.

**Lignes de flux** :
- le bloc 2 propose la **ligne 4** ;
- les lignes 1, 2 et 3 restent proposées par les blocs 5, 9 et 6 (fiche 1 § 9.4), sur les volumes servis ;
- la ligne 5 relève du bloc 3, la ligne 8 du bloc 6 (en valeur comptable).

Aucune ligne nouvelle ; `tab:matrice-flux` et `tab:portes-monnaie` sont inchangées.

**Ce que les blocs voisins fournissent** :
- bloc 3 : W_t en phase 1, N_t en phase 4 ;
- bloc 4 : p_t en phase 5, sans lire v_t ;
- blocs 5, 6 et 9 : les plans de demande en u.m. en phase 2 ;
- bloc 6 : I^vol livré, par la ligne 3.

**Leviers qui transitent par le bloc** (aucun levier propre, `docs/exigences.md` § 2.1, point 1) :

| Levier | Indicateur du bloc | Délai (tours entiers) | Contrepartie visible le même tour |
|---|---|---|---|
| Dépense publique | ventes, variation des stocks en % des ventes, dépense demandée / exécutée ; puis production et emploi | 0 pour les ventes et les stocks ; 1 pour la production | ligne 4 négative (stocks en baisse) ou demande non servie ; conforme à `tab:leviers-cadre` |
| Impôts sur les ménages | ventes au tour n + 1 (budget de la phase 2, fiche 5) | 1 pour les ventes ; 2 pour la production | hausse des stocks au tour n + 1 |
| Taux, par l'investissement | ventes aux entreprises, puis production | fixé par les fiches 6 et 7 | stocks |

**Grandeurs restituées au tour** : elles complètent le § 1.1 selon les conditions 1 et 3 de `jeu`. Ce sont des grandeurs de la couche d'observation, ni flux ni variables d'état.

| Grandeur | Définition | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| Ligne d'identité | demande adressée d ; ventes par acheteur (C^vol, G^vol, I^vol) ; production y ; variation des stocks ΔIN^vol = y − v | u.v. par tour | — | le tour |
| Variation des stocks en % des ventes | (y − v)/v | fraction | ventes du tour | le tour |
| Demande non servie, par acheteur | (d_b − v_b)/d_b | fraction | demande de l'acheteur | le tour |
| Dépense publique demandée / exécutée | G^plan et p·G^vol | u.m. par tour | — | le tour |
| Production visée non réalisée | (y* − y)/y* ; « sans objet » si y* = 0 | fraction | production visée du tour | le tour |
| Stocks en mois de ventes | stock de clôture / moyenne mensuelle des ventes des 12 derniers tours (M22, lecture (e)) | mois | ventes moyennes sur 12 tours | le tour (12 tours au dénominateur) |
| Taux d'utilisation | « utilisation de la capacité normale des équipements », tu | fraction | y^cap du tour | le tour, sous la condition 4 de 9.5 |
| Indice de production | y/y_0 × 100, et glissement annuel sur 12 tours | indice ; par an | production du tour 1 | le tour ; 12 tours |

### 9.5 Conditions de `jeu` (§ 7, reprises telles quelles) et mise en œuvre

1. **Restitution au tour de la ligne d'identité** : demande adressée, ventes par acheteur, production, variation des stocks en % des ventes, demande non servie par acheteur ; pour l'État, dépense demandée / exécutée.
   *Mise en œuvre* : tableau 9.4 ; couche `observation/` (J4) ; définitions dans `sec:production`.
2. **Niveaux normaux** affichés dans la définition exacte de l'indicateur.
   *Mise en œuvre* :
   - Stocks restitués : niveau normal = n_a σ × n_a(1 + γ)/Σ_{u=0}^{n_a−1}(1 + γ)^{−u}, γ = (1 + g)^{1/n_a} − 1, en mois. Cela fait **1,4151 mois** pour σ = 1,4/12 et g = 2 % (facteur 1,0108 de M22, lecture (e) ; *révisé par M25 (b)*, recalculé le 03/10/2026, 1,0107678 × 1,4 = 1,4150749 ; 1,4152 et 1,0109 sous la conversion linéaire de g), contre 1,4 dans la définition du test zéro.
   - Utilisation : t̄u.
   - Production : glissement stationnaire égal à g (2 % pour g_pr = 2 % et g_N = 0 ; *révisé par M25 (b)*, 2,0184 % auparavant).
   - Les trois valeurs sont publiées par le script d'état stationnaire (J3) et affichées au J4.
3. **Production visée non réalisée**, (y* − y)/y*, ajoutée aux grandeurs restituées comme signal précurseur de pénurie.
   *Mise en œuvre* : tableau 9.4 ; calculée en phase 4, sans variable d'état.
4. **Taux d'utilisation** : la fiche 6 (ou la fiche 4) dit ce qu'il déclenche ; sinon, il sort de la restitution.
   *Mise en œuvre* : condition transmise aux fiches 4 et 6 (9.8) et à #37 ; décision au plus tard à la décision de la fiche 6.
5. **Fiche 3** : retard d'emploi par ajustement partiel, préféré par `jeu`, avec la mesure de la boucle combinée emploi – stocks par `macro`.
   *Mise en œuvre* : à la fiche 3, `macro` calcule les valeurs propres du système N1 à N7 avec ajustement partiel de l'emploi et demande induite (m de 0,5 à 0,8), pour la calibration et pour les vitesses ×0,5 et ×2. Critère écrit avant l'essai : amorti, période dans la bande de 3 à 8 ans, demi-vie de l'emploi traduite en λ_N. *Suite (03/10/2026)* : M25 retient λ_N = 3,5 par an, soit une demi-vie de 2,01 tours ; le seuil du critère 11 (d) de la fiche 3, demi-vie de l'emploi de 2 à 4 tours, a été adopté par le mainteneur.
6. **Test O2 au J4** : dépense publique à +1 % et à +5 % du flux mensuel, plus un scénario adverse de sur-commande publique sous pénurie.
   *Mise en œuvre* : 9.6.
7. **Avant J7** : le point « aucun levier n'agit sur l'offre » est traité.
   *Mise en œuvre* : issue #37 (fiches 4 et 6).

### 9.6 Tests attendus

Chaque test énonce une propriété, avec un seuil écrit avant l'essai (§ 5, réserves 1 à 5).

| Jalon | Test | Propriété | Seuil |
|---|---|---|---|
| J3 | État stationnaire | Un pas sans choc depuis l'état résolu laisse v^e, IN^vol, IN, pr et K^vol sur leur trajectoire (volumes en hausse de (1 + g)^{1/n_a} − 1 par pas, prix de (1 + π̄)^{1/n_a} − 1 par pas ; *révisé par M25 (b)*) ; IN/(UC·IN^vol) = ρ̄_IN | 1e−10 relatif |
| J3 | Vitesses (critère 4) | Choc G +1 % pendant 12 tours ; branches λ_v, λ_IN × 0,5 et × 2 : écart des ratios stocks / ventes et y/v | ≤ 1e−6 après 720 pas |
| J3 | Boucle propre | Valeurs propres du bloc, demande exogène : réelles, dans ]0, 1[ (0,75 et 0,8736 à la calibration) | module < 1 pour la calibration et les vitesses × 0,5 et × 2 |
| J3 | Boucle fermée | Rayon spectral de la linéarisation du socle complet | < 1 pour la calibration et les vitesses × 0,5 et × 2 ; si m > 0,8 ou σ > 2 mois, recalibration avant l'essai |
| J3 | Délai | Choc de demande au tour n : production inchangée au tour n, stocks en baisse au tour n, production du signe du choc au tour n + 1 | signe et date exacts |
| J3 | Identité de volume | y = v + (IN^vol_{t+1} − IN^vol_t) | exacte (1e−12 relatif) |
| J3 | Disponibilité | v ≤ IN^vol + y ; IN^vol ≥ 0 ; IN ≥ 0 ; demande supérieure de 10 % au disponible : même taux de service pour chaque acheteur, IN = 0 et IN^vol = 0 à la clôture, d − v restitué sans flux | exact ; IN = 0 à 1e−12 × échelle S près |
| J3 | Plancher (borne y* ≥ 0, N3) | Appel direct de N3, sous la calibration, avec un stock d'ouverture IN^vol = IN^vol* + f·E, où E = (n_a/λ_IN)(v^e + γ·IN^vol*), γ = (1 + g)^{1/n_a} − 1, est l'excédent de stock au-delà duquel le plancher joue. Pour f = 0,99 : y* > 0 (plancher inactif). Pour f = 1,01 : y* = 0, N* = 0 et y = 0, jamais négatifs ; au pas suivant, IN^vol baisse des ventes. À l'état résolu, plancher inactif : y* > 0 | signe exact de part et d'autre du seuil ; y* = 0 et N* = 0 exactement |
| J3 | Technique (borne y ≤ pr·N, N5) | Appel direct de N5. (a) Emploi effectif égal à la demande de travail (N = N*, cas de l'état résolu) : y = y* = pr·N, borne atteinte sans rationnement. (b) N = 0,9·N* (contrainte d'offre de travail) : y = pr·N < y*. (c) N = 1,1·N* (rétention de main-d'œuvre) : y = y* < pr·N. Dans tous les cas, y ≤ pr·N | (a) égalité à 1e−12 relatif ; (b) et (c) signe exact des écarts ; y ≤ pr·N exact |
| J3 | Valorisation | IN ne varie que par la ligne 4 ; IN = cm·IN^vol après chaque pas | 1e−12 relatif |
| J3 | Phases | Le bloc 2 lit N_t après le bloc 3 en phase 4, et p_t après le bloc 4 en phase 5 ; aucune lecture d'un autre plan de la phase 2 | aucune lecture hors ordre |
| J3 | Empreinte | Quatre variables d'état par secteur (J = 1 : 4), aucun historique, aucun tirage aléatoire | décompte exact |
| J3 | Coût | Part du bloc dans `tests/invariants/test_budget.py` | ≤ 0,48 ms par pays-pas |
| J4 | O2 (condition 6 de `jeu`) | G +1 % et +5 % du flux mensuel : effet de signe attendu au tour n sur les ventes et les stocks, au tour n + 1 sur la production ; scénario adverse de sur-commande publique sous pénurie (éviction des ménages visible) | signe et date exacts |
| J4 | Restitution | Niveaux normaux égaux aux valeurs publiées du script d'état stationnaire (1,4151 mois ; t̄u ; croissance g, *révisé par M25 (b)*) | 1e−9 relatif |
| maintenant | Remesure S1 (9.7) | Critères (i) et (ii) | verdicts publiés au § 3.B-4, sans effet sur M24 |

*Ajout du 03/10/2026, avant l'essai (issue #38, lecture (ii), décision du mainteneur ; avis de `macro`)* : lignes « Plancher » et « Technique ». Elles donnent leur test aux deux bornes sans paramètre qui n'en avaient pas. La disponibilité est déjà couverte par la ligne « Disponibilité ». Aucun seuil existant n'est modifié ; aucun verdict n'existe.

**Précision sur le § 3.N-8 (a)** : sous J = 1, les instabilités 1 et 9, ainsi que les parties « équipement » des 10, 11 et 14, n'ont pas d'objet, puisqu'il n'y a ni construction ni prix relatif du capital. En revanche, la règle de prix sans terme de demande (14) et l'amortissement dans le coût (10 et 11) restent des risques des fiches 4 et 6. `tab:instabilites` ne doit donc pas les dire « écartées par construction ».

### 9.7 Remesure S1 : spécification et critères écrits avant l'essai

*Écrits par `macro` le 02/10/2026 et commités avant toute exécution du script.*

- **Script** : `outils/remesurer_v2_production.py` (circuit 3, `coder` puis `audit`).
- **Exécution** :
  - Le prototype tourne dans un processus séparé, sur une copie temporaire vérifiée contre `tests/invariants/archive_sha256.txt`, sans import ni écriture dans `archive/` (invariant 4).
  - Profil : valeurs par défaut de `Params`, sans D1 (non versé) ; `config/reference.json` est absent.
  - Branches : nominale, `mu_ema` × 0,5 et × 2, `lam_inv_2` × 0,5 et × 2. Graine 0 ; 60 ans de 52 semaines.
- **Grandeurs**, par branche, par année et par secteur, comme moyennes sur les semaines valides :
  - Sinv/Q, en semaines, Q = min(D, S) (l. 948) ;
  - Sinv/(s*·Q̄), en fin de semaine ;
  - part des semaines où excess > 0 strictement, Sinv et Q̄ pris à l'ouverture de la semaine. La borne est celle de la l. 923 (monde), identique à la l. 946, branche exécutée en économie fermée ;
  - part des semaines où D > S ;
  - (D − Q)/D ;
  - Y/Ŷ.
- **Fenêtre** : années numérotées 31 à 60, soit t ∈ [30, 60[ ans. La grandeur de fenêtre est la moyenne des moyennes annuelles.
- **Semaines exclues** : une semaine d'effondrement est exclue ; leur nombre dans la fenêtre est publié avec chaque verdict. Une année sans semaine valide rend le verdict « non évaluable ».
- **Critère (i)** : branche nominale ; dans **chacun** des secteurs consommation (2) et équipement (3), Sinv/(s*·Q̄) < 0,99 et part des semaines avec excess > 0 inférieure à 5 %. La prédiction informative, issue du bloc seul (3.B-3), est d'environ 0,93 ; elle n'entre pas dans le seuil.
- **Critère (ii)** : pour chaque vitesse, écart relatif |r(× 2) − r(× 0,5)|/|r(× 0,5)| > 1e−6, avec r = Sinv/Q sur la même fenêtre, dans **chacun** des deux secteurs. Le verdict global exige les deux vitesses.
- **Statut du fait** : « remesuré le <date>, profil par défaut, non D1 ». Verdicts publiés quel que soit le résultat, au § 3.B-4, par une ligne datée. Une branche non exécutable est déclarée « non remesurable ».
- *Précision prospective du 03/10/2026 (constat m1 de l'audit, revue finale ; décision du mainteneur sur avis de `macro`)* : la formule du critère (ii) n'est pas définie pour r(× 0,5) = 0 ; l'écart vaut 0 si r(× 2) = 0 aussi, sinon le critère est « non évaluable » pour ce secteur. Sans effet sur les verdicts publiés (r de 3,418 à 8,077), qui restent publiés tels quels.

### 9.8 Contrats partagés touchés, surface de spécification, constats transmis

**Contrats partagés** (`docs/agents/routage.md` § 4.2) :

1. **Ordre interne de la phase 4** (M24 (b), décision citant M22 ; issue sensible) :
   - `sec:cadre-phases` l. 486 : « ordre des blocs des phases 1, 5 et 7 » devient « ordre des blocs des phases 1, 4, 5 et 7 », avec « phase 4 : travail, puis production (décision M24) » ;
   - `tab:phases`, ligne 4 : « Lisent » devient « phases 2 et 3 ; dans la phase, le bloc production lit l'emploi écrit par le bloc travail » ;
   - consignation par `architect` : annotation datée de l'ADR 0005 (pt 15) citant M24, ou ADR nouveau si `architect` le juge nécessaire.
2. **Convention de notation** : l'exposant `\mathrm{vol}` (volume d'une grandeur nominale du cadre) est ajouté à la convention du glossaire (`sec:glossaire`, « Une variable anticipée porte l'exposant e… ») et à `CONVENTIONS.md` § 5.2. Il s'applique à toutes les fiches suivantes.
3. **Rien d'autre** : `tab:matrice-bilans`, `tab:matrice-flux` et `tab:portes-monnaie` sont inchangées. La ligne 4 garde son symbole ΔIN ; sa règle de valorisation est déclarée dans `sec:production`, conforme à la l. 520. `verifier_matrices.py --strict` doit garder ses décomptes.

**Surface de spécification** (jalon 4 de #34, `docwriter`, encadrés `proposee` citant M24, sans label) :
- **`sec:production`** :
  - technique (Leontief en travail, productivité tendancielle, capacité normale sans plafond) ;
  - N1 à N11, avec statut et provenance ;
  - valorisation au coût moyen pondéré ;
  - rationnement proportionnel ;
  - phases et ordre interne des phases 4 et 5 ;
  - état stationnaire en forme fermée : v^e = v, IN^vol = n_a σ v, y/v = 1 + n_a σγ, ρ̄_IN, ΔIN, t̄u, avec la dépendance de ρ̄_IN, ρ̄_K et y/v à n_a déclarée (*révisé par M25 (b)*) ;
  - conditions déclarées (λ ≤ n_a, domaine de boucle fermée) ;
  - grandeurs restituées du tableau 9.4 ;
  - un encadré `portee` : J = 1 ; pas d'intrants ; pas de levier d'offre (#37) ; capacité sans plafond ; emploi au bloc 3 ; volume du capital au bloc 2.
- **`sec:cadre-phases` et `tab:phases`** : point 1 ci-dessus.
- **`sec:calibration` et `tab:calibration`** : les cinq paramètres de 9.2.
- **`tab:symboles` et convention du glossaire** : symboles de 3.N-7 et exposant `vol`.
- **`sec:ecartees`**, sous-section « Production et stocks (décision M24) » :
  - A (loi des stocks non conservatrice telle qu'écrite ; ΔIN non défini) ;
  - B (borne active à l'état stationnaire ; cycle propre de 6 ans ; réévaluation implicite) ;
  - le défaut commun à A et B : ratio stocks / ventes dépendant des vitesses ;
  - D (prix relatif sans levier) ;
  - valorisation au coût courant ; plafond de capacité ; priorité de l'État au socle ; ordre « production, puis travail » ; anticipations sur les ventes ; conversion calibrée sur une croissance effective (sans objet sous la conversion géométrique, *révisé par M25 (b)*).
- **Texte qui accompagne `tab:instabilites`** : formulation de la précision de 9.6.
- **`sec:changements-v3x`** : une ligne « production et stocks (M24) ».
- **Inchangés** :
  - `sec:leviers` : `tab:leviers-cadre` porte déjà « production au tour suivant » ;
  - `sec:cadre-flux` : la clause de #36 reste (voir la fiche 6 ci-dessous).

**Constats transmis** :
- **Fiche 3** :
  - confirmer Q4 : emploi au bloc 3, N* reçu en phase 2, N écrit en phase 4 avant le bloc 2 ;
  - la contrainte d'offre de travail est une borne déclarée, inactive à l'état stationnaire ;
  - la masse salariale excédentaire en cas de rétention (WB − UC·y) est une charge du pas, non portée en stock ;
  - restituer la productivité apparente y/N rapportée à sa tendance si un retard d'emploi est retenu ;
  - condition 5 de `jeu` : mesure de la boucle combinée par `macro` ;
  - la justification empirique d'un retard d'emploi (loi d'Okun, rétention) reste à sourcer.
- **Fiche 4** :
  - UC (`eq:production-cout-unitaire`) est défini par le bloc 2 et lu par le bloc 4 ;
  - p_t est écrit en phase 5 avant le bloc 2 et ne lit pas v_t ;
  - sous J = 1, il n'y a pas de prix relatif, mais la règle de prix doit garder un terme de demande (instabilité 14 ; acquis R3, R) ;
  - un amortissement inclus dans le coût est un point fixe scalaire, et les instabilités 10 et 11 restent à surveiller ;
  - condition 4 (taux d'utilisation) ; #37 ; #24 (conversion des taux de croissance, tranchée par M25 (b) et l'ADR 0008 : la croissance effective n'est plus publiée) ;
  - fixer la phase (2 ou 4) où le bloc 2 écrit UC, avant la phase 5 où le bloc prix le lit ; au J5, terme d'intrants et triangularité de la matrice des lectures.
- **Fiche 6** :
  - confirmer Q4 : K^vol au bloc 2, I^vol livré après rationnement, lignes 3 et 8 au bloc 6 ;
  - **constat** : la valeur comptable du capital vaut ρ̄_K = 0,7786 fois sa valeur au prix courant à g = π̄ = 2 % et δ = 5 % (0,4214 à π̄ = 10 % ; *révisé par M25 (b)*, 0,7791 et 0,4221 auparavant). Le K/Y d'O1 doit dire s'il est comptable ou en volume valorisé ;
  - calibrer κ avec t̄u ; condition 4 ; #37 (levier d'offre) ;
  - **Q2 et M1 de #36** : si la fiche 6 retient une ligne de profits non distribués (voie (ii) de Q2), la clause de `sec:cadre-flux`, « prise seule, une sous-colonne des entreprises n'est pas nulle en général », devient fausse et est à reprendre, ainsi que la légende de `tab:matrice-flux`. C'est un contrat partagé : décision citant M22. Sous la voie (i), elle reste exacte. La valeur stationnaire des profits non distribués du socle est donnée au § 3.N-10 (0,33059 % de V_F par pas, *révisé par M25 (b)*).
- **Fiches 5 et 9** :
  - les plans de demande sont en u.m. en phase 2 ; sous rationnement proportionnel, le budget non dépensé reste en dépôts ou sur le compte du Trésor ;
  - restituer la dépense demandée / exécutée ;
  - fournir pour le J3 la propension effective m de la demande à la production, qui entre dans la réserve 3 ;
  - scénario adverse de sur-commande (condition 6).
- **`architect`** :
  - consignation de la phase 4 (point 1 des contrats) ;
  - entrées de `CONTEXT.md` : « production visée », « demande non servie », « coût moyen pondéré », « capacité normale », « volume (exposant vol) » ;
  - statut de l'inventaire ;
  - question de `jeu` sur une priorité de rationnement réglable par levier et l'ADR 0002.

### 9.9 Issues proposées (titres, non créées ; #34, #36 et #37 exclues)

1. ADR ou annotation de l'ADR 0005 : ordre interne de la phase 4 « travail, puis production » (M24 (b), citant M22) — `architect`. Issue sensible ; à traiter avant ou avec le jalon 4 de #34, qui modifie `tab:phases`.
2. `CONVENTIONS.md` § 5.2 et glossaire : exposant `\mathrm{vol}` pour les volumes — `docwriter`, validation `macro`. Peut entrer dans le jalon 4 de #34.
3. J3 — `src/nations/blocs/production.py` et ses tests (9.6), douze balises `eq:production-*` — `coder`, puis `audit`.
4. J3 — script d'état stationnaire (M19) : formes fermées du bloc 2 et niveaux normaux restitués (9.5, condition 2).
5. J4 — restitution du bloc 2 (tableau 9.4) et test O2 (condition 6) — `coder`, `app-review`, `jeu`.
6. Fiche : numérotation N9 et N11 au § 3.N-1 et précision du § 3.N-8 (a) sur les instabilités 10, 11 et 14 — commit `docs:` de la session principale. C'est une correction de l'instruction, sans changement de verdict.

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 02/10/2026 | Ouverture (issue #34) ; § 1 et § 2 proposés | `macro` ; session principale |
| 02/10/2026 | Critères validés tels quels ; seuils des critères 3, 4 et 9 adoptés ; bandes du critère 6 renvoyées au J3 (issue #34) | mainteneur |
| 02/10/2026 | Instruction déposée (§ 3 à 5) : options A et B, socle commun 3.N, options C (J = 1) et D (J = 2) ; recommandation C ; lectures (a) à (g) ; remesure S1 demandée | `macro` |
| 02/10/2026 | Avis de `jeu` (§ 7) : préférence C (classement C > D > B > A), sept conditions de restitution au § 9, une issue proposée (aucun levier d'offre au socle 3.N) | `jeu` |
| 02/10/2026 | Statut « avis rendus » (aucun constat de vérificateur à intégrer) | session principale |
| 02/10/2026 | Décision M24 : option C, lectures (a) à (g) en (i), ordre « travail, puis production » en phase 4 | mainteneur |
| 02/10/2026 | Conséquences de la décision (§ 9) ; lecture opérationnelle de S1 confirmée et critères de S1 versés au § 9.7 avant l'essai ; numérotation N9 et N11 au § 3.N-1 et précision du § 3.N-8 sur les instabilités 10, 11 et 14 | `macro` ; session principale |
| 02/10/2026 | Remesure S1 exécutée (script `dfe896f`, critères au § 9.7, `227607e`) : (i) non satisfait (part des semaines dans l'équipement 0,080 > 0,05, épisode des années 37 à 39) ; (ii) satisfait (écarts de 0,078 à 0,523) ; mentions « à remesurer » du § 3.B levées ; interprétation de `macro` ; M24 inchangée | session principale ; `macro` |
| 03/10/2026 | Validation de fond de `sec:production` (`macro`) : lecture de π̄ comme glissement annuel confirmée ; ρ̄_IN, ΔIN, FU et ρ̄_K recalculés (0,996057 ; 0,33210 % ; 0,7791) ; notation barrée (ρ̄_IN, ρ̄_K, t̄u) ; statut de la technique ; lectures de la phase 2 (§ 9.4) ; phase de UC transmise à la fiche 4 (§ 9.8) ; amendement de notation du critère 3 et du § 9.6 ; précision prospective du § 9.7 (constat m1) | `macro` ; mainteneur ; session principale |
| 03/10/2026 | Issue #38, lecture (ii) : tests des bornes y* ≥ 0 et y ≤ pr·N ajoutés au § 9.6 avant l'essai ; disponibilité déjà couverte | `macro` ; mainteneur ; session principale |
| 03/10/2026 | Révision par M25 (b) (lecture (G), ADR 0008, pt I.5) : M24 (f) révisée, ligne datée au § 8 ; § 3.N et § 9 corrigés (N1, N3, N9, g, ρ̄_K 0,7786 / 0,4214, ΔIN et FU 0,33059 %, y/v 1,0023122 et sa dépendance à n_a, valeurs propres 0,8736 et 0,9360, stocks restitués 1,4151 mois, facteur 1,0108) ; chiffres visés par le mainteneur (`docs/feuille-de-route.md` § 4), remesurés par la session principale ; § 4 à 7 inchangés | `macro` ; mainteneur ; session principale |
