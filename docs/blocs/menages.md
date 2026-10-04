---
bloc: Ménages
module: src/nations/blocs/menages.py
expert pilote: macro
experts consultés: monnaie (dépôts et détention de titres publics : frontière dette publique) ; jeu
statut: décidée (M27, 03/10/2026)
décision: M27 (03/10/2026)
issue: #41
---

# Fiche comparative — Ménages

> Fiche ouverte à partir du gabarit `0000-gabarit.md` (validé à l'usage, M20), sur le modèle de forme des fiches 3 « travail et salaires » et 4 « prix » (critères validés le 03/10/2026, `4aee609`). Jalon 1 de l'issue #41 : § 1 et § 2 seuls ; les rubriques suivantes portent « non instruit » jusqu'au jalon 2. Décidée avec la fiche 6 « investissement et financement » (décision du mainteneur du 03/10/2026 : décisions par paires).

Une fiche comparative instruit **l'origine de l'approche** d'un bloc (`docs/exigences.md` § 2.3) : la spécification v1.5, le moteur v2.0, ou une approche nouvelle. Elle est **instruite par l'expert pilote**, commentée par `jeu` et par l'expert consulté que désigne `README.md`, et **décidée par le mainteneur** (décision M-n, reportée dans `docs/feuille-de-route.md`). Aucune approche n'entre dans le moteur ni dans la spécification sans cette décision. Les agents n'écrivent pas la fiche dans le dépôt : elle figure dans leur compte rendu et la session principale la commite. Un **bloc-cadre** (temps et comptabilité) n'est pas un module de `blocs/` : sa fiche instruit ce que le cadre **définit** (conventions, matrices, règles), non des flux proposés ; les adaptations que cela impose sont signalées rubrique par rubrique.

Règles de rigueur (`CLAUDE.md`, « Rigueur ») : un chiffre se remesure ou cite sa source ; une équation de la v1.5 n'a jamais été garantie exécutée ; un comportement de la v2.0 ne vaut que sous son profil (état D1, **non versé** : aucun fait ne peut y être remesuré) et avec ses défauts connus ; chaque fait de la première tentative porte son **statut** S+O, O, R, L, V ou V+O (`CONTEXT.md`, « Statut d'un fait » ; un fait V sur le prototype v2.0 reste un fait de la première tentative, non un résultat v3) ; chaque référence est une publication retrouvée. Citer `archive/v1.5/…` avec numéro d'équation et section, ou avec le **numéro de ligne du `.tex`** quand section ou équation ne sont pas identifiables sans compiler ; `archive/v2.0/…` avec fichier et ligne. **Principe de simplicité** (adopté par le mainteneur le 30/09/2026, fiche « temps et comptabilité » § 2 ; `CONTEXT.md`) : à exigences comptables égales, l'option la plus simple pour le joueur et pour le moteur est préférée ; toute complexité se justifie par une identité qu'elle rend vérifiable ou par un mécanisme perçu à l'échelle d'une partie ; une simplification ne supprime ni une contrepartie comptable visible d'un levier ni une grandeur restituée au tour ; les identités, les tolérances relatives, le déterminisme, les invariants de l'ADR 0002 et la concordance ne se simplifient pas.

## 1. Question posée

*Rédigé par `macro` (expert pilote), 03/10/2026, sur la spécification à l'état `4aee609` (branche `claude/j1-economie-reelle`, PR #43).*

Le bloc porte le secteur des ménages du socle :
- le revenu disponible ;
- le plan de dépense de consommation, en u.m., écrit en phase 2 (« budget de consommation », `tab:phases`) ;
- la consommation exécutée sur le volume servi (ligne 1, phase 5) ;
- l'épargne ;
- la richesse nette V_H = D_H + B_H et sa composition entre dépôts et titres publics (souscription en phase 7, ligne 19a-ménages).

C'est par lui que se ferme la demande de consommation. La fiche 2 en a laissé la propension à la production en hypothèse (m de 0,5 à 0,8, § 3.N-8) ; la fiche 5 en fournit la part des ménages pour le J3 (réserve 3 de la fiche 2). Le bloc lit des revenus que d'autres blocs fixent : salaires (fiche 3), dividendes (fiches 6 et 7), intérêts (fiches 7 et 9), impôts et transferts (fiche 9). Il ne fixe aucune de leurs règles. Il débloque les fiches 6, 7 et 9 (`docs/blocs/README.md` § 3, rang 5). Son instruction attend que les fiches 3 et 4 soient « avis rendus » (#41, dépendances).

Sous M22, un pas est un tour (n_a = 12, n_m = 1) : toute fenêtre exprimée en pas l'est aussi en tours. La fiche est décidée **avec la fiche 6** (M27 et M28, numéros sous réserve de l'ordre réel des décisions ; décision du mainteneur du 03/10/2026 : décisions par paires). Elle ne lui est donc pas antérieure pour ce qui touche au partage entre épargne des ménages et financement des entreprises (dividendes, dépôts).

### 1.1 Contrats hérités

| Contrat | Source | Ce qu'il impose à la fiche 5 | Ce qui le rouvrirait |
|---|---|---|---|
| Calendrier et conversions | M22 ; ADR 0005 ; `tab:phases` (l. 505, 508, 510) | Pas mensuel, n_a = 12, un pas = un tour. Deux conversions selon la nature du taux (ADR 0008, point I.2) : **linéaire** (x/n_a) pour les taux de flux (i_D, i_B, intérêts) et les vitesses, avec λ ≤ n_a ; **géométrique** ((1 + x)^{1/n_a}) pour les taux de croissance et d'inflation (g, π̄, π^e, et la tendance de la cible de richesse). Plan de consommation écrit en phase 2 ; ligne 1 en phase 5 ; souscriptions de titres en phase 7. Neuf phases triangulaires, aucune résolution simultanée. Ratio de stock du test zéro : stock d'ouverture / (12 × flux du pas) ; en restitution : stock de clôture / somme des 12 derniers tours (lecture (e)) | Décision M-m citant M22 |
| Plans de demande en u.m. et rationnement | M24 (g) ; fiche 2 § 9.4 et § 9.8 ; `sec:production-ventes` (l. 636 à 639) | Le bloc 5 rend en phase 2 un plan de dépense en u.m. La demande en volume d_{H,j,t} = plan / p_{j,t} est formée par le bloc 2 en phase 5. Le rationnement est proportionnel, sans paramètre ni priorité. Le budget non dépensé reste en dépôts, et « ce qu'en font les acheteurs au pas suivant relève de leurs blocs » (l. 639) : la fiche 5 le dit. À plan donné, la demande en volume a une élasticité de −1 au prix du pas | Décision citant M24 |
| Ordre interne de la phase 5 et ligne 1 | M24 ; fiche 2 § 9.4 ; `sec:production-phases` (l. 692) | « Prix, puis production, puis ménages, investissement, État ». Le bloc 5 propose la ligne 1 sur le volume servi : C = p_{j,t}·C^vol_t, avec C^vol_t = v_{H,j,t}. Il ne lit pas les autres acheteurs | Décision citant M24, et M22 si `tab:phases` change |
| Phase 2 sans ordre interne | `sec:cadre-phases` (l. 487) ; `sec:production-phases` (l. 690) | Le plan des ménages ne lit aucun autre plan de la phase 2 : ni y*, ni N*, ni les plans de l'investissement et de l'État. Une telle lecture demanderait un ordre interne de la phase 2, absent de la liste des phases à ordre interne (1, 4, 5, 7, 8) | Décision citant M22 |
| Colonne des ménages, lignes et portes de la monnaie | M22 ; `tab:matrice-bilans`, `tab:matrice-flux`, `tab:portes-monnaie` | Colonne des ménages : lignes 1, 5, 6, 7, 10, 11a, 14, 15, 17, 19a-ménages et 19b-ménages. Le bloc 5 propose la ligne 1 et sa souscription (19a-ménages, si l'option en a une). Les autres lignes sont proposées par les blocs 3, 6, 7, 9 et la banque centrale ; la ligne 17 est une contrepartie de règlement appliquée par le noyau. V_H = D_H + B_H est la seule grandeur résiduelle, calculée deux fois. Aucune ligne ni aucun poste ajoutés | Décision citant M22 |
| Règles de caisse | M22 ; `sec:cadre-caisse` (l. 458) | Les ménages paient en dépôts. Un payeur ne paie pas plus que son moyen de paiement ; la part non payée est une ligne nommée du bloc payeur, jamais un découvert implicite. L'ordre de priorité des paiements est déclaré par le bloc | Décision citant M22 |
| Instruments du socle | M22 ; `sec:cadre-bilans` (l. 221 à 227) | Ni crédit aux ménages, ni actions, ni immobilier (J6), ni billets, ni reste du monde (J5). Les ménages détiennent D_H et B_H et n'ont aucun passif. D_H ≥ 0 et B_H ≥ 0 découlent de la définition des encours | Décision citant M22 |
| Bornes | #38, lecture (ii) ; `CONVENTIONS.md` § 2.4 | Une borne est classée par le critère de tri. Une borne à seuil libre a un paramètre déclaré et un motif contre un mécanisme. Une contrainte de conservation n'a pas de paramètre : elle est déclarée dans les `\limites`, avec son activité à l'état stationnaire et un test | Décision citant #38 |
| Dates d'effet des leviers | M22 ; `tab:leviers-cadre` (l. 903 et 905) ; fiche 2 § 9.4 | Impôts et transferts modifient les lignes 7 et 6 en phase 6 du tour même (délai 0). L'effet sur la consommation n'est pas mesuré par le cadre : le bloc 5 le déclare en tours entiers. La fiche 2 a supposé « impôts sur les ménages → ventes au tour n + 1 (budget de la phase 2, fiche 5) » ; la fiche 5 confirme ou propose une révision | Décision du mainteneur (une révision de la fiche 2 § 9.4 passe par son visa) |
| Propension effective m | Fiche 2 § 3.N-8 (l. 579 à 588), § 5 (réserve 3), § 9.8 | La fiche 2 définit m comme la propension de la demande à la production du pas précédent, d_t = A + m·y_{t−1}, en hypothèse entre 0,5 et 0,8. Si m dépasse 0,8, la calibration des vitesses de la fiche 2 est revue avant l'essai (J3). La fiche 5 fournit la part des ménages | — |
| Sur-commande | Fiche 2 § 7 (risque, l. 913), § 9.5 (condition 6 de `jeu`), § 9.6 (test O2, J4) | Scénario adverse de sur-commande publique sous pénurie : éviction des ménages visible ; dépense demandée et dépense exécutée restituées | Décision du mainteneur |
| Fiches 3 et 4 (M25, M26) | Fiches 3 et 4, § 2 et amendements du 03/10/2026 | W_t est écrit en phase 1 ; N et WB (ligne 5) en phase 4 ; p_t en phase 5 ; P_t et π_t selon M26 (Q1 de la fiche 4). Une seule lecture des taux annuels (#24) vaut pour les fiches 3, 4 et 8 ; elle est choisie à M25-M26, et la fiche 5 la reprend pour ses propres taux annuels. La population active est instruite comme tendance exogène ; son propriétaire est fixé à M25 | M25 et M26 |
| Fiche 6, décidée avec la fiche 5 | Décision par paires du 03/10/2026 ; #42 | Les dividendes des entreprises (ligne 14) sont fixés par le bloc 6 ; la voie (i) ou (ii) de #36 y est tranchée. L'épargne des ménages et le financement des entreprises se décident ensemble | M27 et M28, prises ensemble |
| Frontière dette publique | `docs/blocs/README.md` § 2 | Chez `macro` : l'épargne, la richesse des ménages et sa valeur stationnaire. Chez `monnaie` : le placement des titres (ménages, banque, banque centrale) et la prime. La détention de dépôts et de titres par les ménages relève des deux experts | — |
| Statut des faits | Décision P1 du 03/10/2026 ; `CONTEXT.md` | Statuts S+O, O, R, L, V ou V+O. Un fait V mesuré sur le prototype v2.0 reste un fait de la première tentative. L'état D1 n'est pas versé | — |

### 1.2 Ce que le bloc doit produire

Les symboles **ne sont pas fixés** : ils le seront à l'instruction, sous le critère 15. S est pris (échelle du bilan) et s aussi (indice de secteur) : l'épargne ne peut s'écrire ainsi. c et h sont des indices réservés. m désigne la propension de la demande à la production (fiche 2). σ et ρ̄ sont pris. Y^d est le symbole de la v1.5, absent de `tab:symboles`.

| Grandeur | Définition | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| Plan de consommation (dépense demandée) | Budget de dépense de consommation du pas, fixé en phase 2 | u.m. par pas | — | le pas, phase 2 ; restitution : le tour |
| Consommation exécutée C_t | p_{j,t}·v_{H,j,t}, ligne 1 (ménages −, entreprises « courant » +) | u.m. par pas | — | le pas, phase 5 ; restitution : le tour et la somme sur 12 tours |
| Taux d'exécution de la dépense des ménages | C / plan, soit 1 moins la demande non servie des ménages (fiche 2 § 9.4) | fraction | plan du pas | le tour |
| Consommation en volume C^vol_t | v_{H,j,t} | u.v. par pas | — | le tour ; glissement sur 12 tours |
| Revenu disponible | WB + Tr + i_D D_H/n_a + i_B B_H/n_a + Div_F + Div_Bk − T_H (lignes 5, 6, 10, 11a, 14, 15, 7), connu à la fin de la phase 6. Une définition corrigée de l'inflation est en question (Q3) | u.m. par pas | — | le pas ; restitution : le tour et la somme sur 12 tours |
| Épargne des ménages | Revenu disponible − C ; égale à ΔV_H, sans réévaluation au socle | u.m. par pas | — | le pas |
| Taux d'épargne | 1 − (somme des C) / (somme des revenus disponibles) | fraction | revenu disponible sur 12 tours | 12 tours |
| Richesse nette V_H | D_H + B_H | u.m. | — | ouverture du pas |
| Richesse rapportée au revenu disponible annuel | Test zéro : V_H,t / (12 × revenu disponible du pas). Restitution : V_H de clôture / somme des 12 derniers revenus (M22, lecture (e)) | années | revenu disponible annuel | ouverture ; restitution : 12 tours |
| Souscription de titres par les ménages | ΔB_H^prim, ligne 19a-ménages | u.m. par pas | — | le pas, phase 7 |
| Part des titres publics dans la richesse | B_H / V_H | fraction | V_H | ouverture ; restitution : la moyenne sur 12 tours |
| Propension effective de la demande des ménages à la production | ∂d_{H,j,t}/∂y_{j,t−1} autour de la trajectoire stationnaire (critère 6), à l'impact et à long terme | sans dimension (u.v. par u.v.) | y_{j,t−1} | un pas (impact) ; état stationnaire (long terme) |
| Population active, si M25 l'attribue au bloc 5 | Personnes disponibles pour l'emploi, tendance exogène de croissance g_N | personnes | — | ouverture du pas |
| Variables d'état du bloc, si l'option en a | Par exemple revenu du pas précédent, revenu anticipé ou richesse cible | unité propre | — | ouverture du pas |

### 1.3 Ce qu'il lit

- **Ouverture** :
  - D_H et B_H ;
  - ses variables d'état ;
  - le registre de l'indice des prix, s'il en a besoin.
- **Phase 1** : W_t (bloc 3) ; P_t et π_t (bloc 4, selon M26) ; les taux arrêtés en phase 1 ; les leviers lus par le moteur (taux d'imposition, transferts) ; la variable d'anticipation, si elle est consommée (critère 2 (e)).
- **Phase 2** : aucun autre plan (contrat « phase 2 sans ordre interne »).
- **Phase 4** : la ligne 5 (WB) est reçue ; le plan de la phase 2 ne peut pas la lire.
- **Phase 5** : p_{j,t} et v_{H,j,t}, écrits avant lui par les blocs 4 et 2, pour proposer la ligne 1.
- **Phase 6** : les lignes 6, 7, 10, 11a, 14 et 15 sont reçues. Elles sont proposées par l'État, la banque et l'investissement ; le bloc 5 n'écrit rien dans cette phase.
- **Phase 7** : D_H après la phase 6 ; i_B ; le besoin de l'État et la règle de placement, si la souscription en dépend, dans l'ordre interne à déclarer (critère 2 (c)).
- **Leviers du joueur** :
  - aucun levier propre au socle sans décision ;
  - transitent par le bloc : impôts sur les ménages, transferts, dépense publique (par le revenu) et taux (par les revenus d'intérêt et la richesse) ;
  - les leviers ciblés sur les ménages (transferts ciblés, fiscalité de la consommation) relèvent de la Q11.
- **Décisions qui le contraignent** : M7, M13, M22 (ADR 0005), M24 (ADR 0007), décision du 02/10/2026 sur #23 (indices c, j, k ; h réservé aux strates de ménages), décision du 03/10/2026 sur #38, M25 et M26 une fois prises, décisions par paires (M27, M28).

### 1.4 Frontières

- **Production et stocks (fiche 2, décidée)** :
  - le plan en u.m. devient d_H, et le volume servi v_H revient au bloc 5 ;
  - la demande non servie des ménages est restituée ;
  - m alimente la réserve 3 ;
  - scénario adverse de sur-commande.

  Critères 2, 5 (c), 6 et 11.
- **Travail et salaires (fiche 3)** : la ligne 5 est le premier revenu des ménages ; le propriétaire de la population active est fixé à M25 ; les allocations de chômage éventuelles relèvent de la fiche 9. Critères 3 (c) et 6 (b).
- **Prix (fiche 4)** :
  - p_t fixe le volume servi à plan donné ;
  - P_t et π_t sont lus en phase 1 si la règle déflate son plan ou porte un terme de tendance nominal ;
  - la marge alimente les dividendes.

  Critères 2 et 3 (d).
- **Investissement et financement (fiche 6, décidée avec la fiche 5)** : dividendes des entreprises (ligne 14) ; voie (i) ou (ii) de #36 ; dépôts des entreprises. L'état stationnaire conjoint se calcule avant M27-M28 (critère 3 (e)).
- **Banque commerciale (fiche 7, `monnaie`)** : i_D et dividendes de la banque (ligne 15) ; les dépôts des ménages sont un passif de la banque.
- **Banque centrale et anticipations (fiche 8, `monnaie`)** :
  - taux ;
  - achats de la banque centrale aux ménages (ligne 19b-ménages) ;
  - anticipation d'inflation, si elle est consommée (critère 2 (e)) ;
  - le taux naturel que la v1.5 ancrait sur l'équation d'Euler des ménages (`r* = ρ + σg`, l. 659) relève de la fiche 8.
- **État et dette (fiche 9, branche n° 4)** : règles de T_H et de Tr, émission du besoin (phase 7), i_B, placement. Le bloc 5 lit ces grandeurs sans en fixer la règle (critère 10). **Frontière dette publique** : critère 9 et avis de `monnaie` (§ 6).
- **`jeu`** : critères 11 et 12 ; avis au § 7.

### 1.5 Ce que la fiche ne tranche pas, et questions ouvertes

**Hors du périmètre** :
- crédit aux ménages, immobilier, actions et effet richesse sur les actifs cotés (J6) ;
- billets, devises et dollarisation (J5) ;
- démographie endogène, migration, taux d'activité endogène (M7 ; v1.5 `sec:demog`, l. 706 à 709) ;
- répartition entre biens (Stone-Geary, v1.5 `eq:les`, l. 666), sans objet sous J = 1, et niveau de vie et inégalités (v1.5 `eq:sol`, l. 678 ; J7) ;
- règles des impôts, des transferts et de l'émission (fiche 9), taux des dépôts (fiche 7), loi des anticipations (fiche 8), clôture du placement de la dette (fiches 7 à 9, `monnaie`) ;
- valeurs numériques de l'état stationnaire et calibration (J3) : la fiche vérifie qu'une forme fermée existe ;
- bandes du test zéro : proposées ici, confirmées avec O1 avant l'essai (M19).

**Questions ouvertes à instruire** :
- **Q1 — Règle de consommation.** Doivent être instruites :
  - l'option A (v1.5) :
    - `eq:yd` (l. 631) ;
    - `eq:cB`, `eq:cH`, `eq:cM` (l. 645 à 648), soit deux régimes, avec une règle keynésienne et une cible d'Euler à ajustement partiel ;
    - Y^perm, moyenne mobile exponentielle (l. 656) ;
  - l'option B (v2.0) : la branche active du profil D1 est à établir avant toute citation. `portfolio_mode='joint_equity'` (faits § 1.1) impose `household_mode='euler'` et `wiu_epsilon` > 0 (`model.py` l. 828 et 829), dont la valeur dans D1 n'est pas établie par la synthèse des faits ; d'où `joint_portfolio.decision_and_settlement` (l. 831 à 833). Les autres branches sont `plan_wealth` (l. 807), `plan_buffer_stock` (l. 818), `plan_household` (l. 821) et la règle de revenu `E_income = c·Yd + cV·V/WEEKS` (l. 793) ;
  - la piste « consommation par règle stock-flux à cible de richesse » (feuille de route § 5), en forme fermée ;
  - la fonction de consommation du modèle SIM (Godley et Lavoie, 2007, chap. 3, C = α1·YD + α2·V_{−1}), si elle diffère de la piste ;
  - au moins une autre approche tirée de la littérature, si l'instruction en trouve une pertinente.
- **Q2 — Revenu lu par le plan de la phase 2.** Trois lectures possibles :
  - le revenu du pas précédent, porté comme variable d'état ;
  - un revenu anticipé ou lissé (v2.0 `Yperm`, l. 789, `hh_income_speed`) ;
  - les composantes connues en phase 1 (W_t, taux, leviers fiscaux).

  Pour chacune : son empreinte, son délai en tours (impôts → consommation, critère 2 (d)) et sa dépendance envers n_a (critère 3 (b)).
- **Q3 — Revenu disponible et inflation.** Revenu nominal, ou revenu corrigé de la perte d'inflation sur la richesse nominale (revenu « Haig-Simons » de Godley et Lavoie, 2007 ; chapitre à retrouver). Conséquence sur le taux d'épargne et le ratio de richesse stationnaires à π̄ = 2 % et 10 % (critère 3 (d)).
- **Q4 — Portefeuille.** Trois variantes : demande de titres à la Tobin (Godley et Lavoie, 2007, chap. 4, modèle PC ; v1.5 `eq:portfolio`, l. 696) ; part fixe ; ou B_H ≡ 0 au socle, les titres étant détenus par la banque et la banque centrale seules. Dans ce dernier cas, les lignes 11a, 19a-ménages et 19b-ménages restent à montant nul, et les retirer demanderait une décision citant M22. Avis de `monnaie`.
- **Q5 — Ordre interne de la phase 7 et placement** : la demande de titres des ménages face au besoin émis par l'État ; qui souscrit le reliquat ; rationnement éventuel de la demande des ménages. L'ordre est déclaré avec les fiches 7 à 9 et `monnaie`, sans être tranché par la fiche 5.
- **Q6 — Nombre de strates au socle** (indice h). Soit un ménage représentatif dont les équations sont indexées par h dès le socle, comme J = 1 sous M24 (d), soit deux types, contraints et non contraints (Galí, López-Salido et Vallés, 2007 ; v1.5 : trois strates ; v2.0 : trois groupes). Des strates en sous-colonnes de `tab:matrice-flux` toucheraient un contrat partagé (décision citant M22).
- **Q7 — Priorité des paiements des ménages et insuffisance de dépôts** : ligne 1 en phase 5, ligne 7 en phase 6, souscription en phase 7 ; ligne nommée et bloc qui la porte si un paiement excède les dépôts (critère 8 (a)).
- **Q8 — Canal du taux sur la consommation** : revenus d'intérêt (lignes 10 et 11a ; acquis « la politique monétaire peut agir à l'envers », R), richesse, ou substitution intertemporelle (hypothèse réfutée n° 3, à ne pas reprendre sans fait nouveau). Signe et délai déclarés ; avis de `monnaie`.
- **Q9 — Population active** : si M25 l'attribue au bloc 5, la fiche la reprend comme tendance exogène, sans comportement.
- **Q10 — Anticipation consommée** : si la règle porte un terme de tendance nominal, choisir la variable qui en porte l'inflation (π̄, π^e de la fiche 8, glissement mesuré), avec la même lecture de #24 que les fiches 3, 4 et 8.
- **Q11 — Leviers ciblés sur les ménages** (transferts ciblés, fiscalité de la consommation) : instruits comme options, ou renvoyés au catalogue des leviers (J4) avec leur interface notée.

## 2. Critères d'évaluation, écrits avant l'instruction

**Statut** : proposés par `macro` le 03/10/2026, **validés par le mainteneur le 03/10/2026, avec les amendements ci-dessous** (jalon 1 de #41). La liste est fermée : elle ne se déplace pas après observation (`docs/exigences.md` § 2.5). Un amendement adopté avant l'instruction se consigne sous le tableau.

Correspondance avec le gabarit :

| Critère du gabarit | Critère de la fiche |
|---|---|
| 1 | 1 |
| 2 | 3 et 4 |
| 3 | 5 |
| 4 | 14 |
| 5 | 12 |
| 6 | 8 et 13 |

Critères propres au bloc : 2, 6, 7, 9, 10, 11, 15, 16 et 17.

Sont des **exigences** (ils peuvent écarter une option) : 1, 2, 3 (a), (b), (c) et (e), 4, 5 (a) et (b), 5 (c) à la calibration proposée, 6 (a) et (b), 7, 8, 9 (a) et (b), 10, 11 (a) et (b), 11 (c) pour le seuil de non-réapparition, 12 (b), 13 (sans historique, état caché ni drapeau), 14 (sans itération), 15 et 17.

Sont des **mesures** (elles décrivent sans écarter) : 3 (d), 5 (c) aux vitesses ×0,5 et ×2, 5 (d), 6 (c), 9 (c), 11 (c) pour l'ampleur, 11 (d), 12 (a), (c) et (d), 13 (décompte), 14 (décompte) et 16.

| N° | Critère | Ce qui est attendu (seuil ou forme du verdict) | Par quoi on le vérifie | Qui | Quand |
|---|---|---|---|---|---|
| 1 | Cohérence stock-flux (gabarit 1 ; `macro`) — **exigence** | (a) Le bloc propose la **ligne 1**, C = p_{j,t}·v_{H,j,t}, en phase 5 (ménages −C, entreprises « courant » +C). Il propose aussi la souscription des ménages en phase 7, ligne 19a-ménages (ménages −ΔB_H^prim, État +), si l'option en a une. Les autres lignes de la colonne viennent d'autres blocs : 5 du bloc 3 ; 6, 7 et 11a du bloc 9 ; 10 et 15 du bloc 7 ; 14 du bloc 6 ; 19b-ménages du bloc 8. La ligne 17 est la contrepartie de règlement. Les signatures de `tab:portes-monnaie` sont inchangées (ligne 1 : 0, 0 ; ligne 19a-ménages : −, −). Aucune ligne et aucun poste ne sont ajoutés. Une option qui en exige (crédit aux ménages, cotisations, fiscalité de la consommation) les déclare avec leur phase et leur signature : c'est un contrat partagé, donc une décision citant M22. (b) **Valeur nette** : V_H = D_H + B_H est calculée par le stock et par les flux, avec ΔV_H = revenu disponible − C, sans réévaluation. Aucun poste des ménages n'est obtenu par différence. D_H n'est fixé par aucune équation de comportement concurrente de la ligne 17 : une règle de portefeuille fixe B_H, et D_H suit. (c) Le budget non dépensé sous rationnement reste en D_H ; aucun flux ne le fait disparaître | Matrice des flux de l'option, écrite en tableau. Cas à la main sur un pas où la demande des ménages est servie à 90 % : plan, C, ΔD_H, et V_H calculée par le stock et par les flux. Si une table change : `uv run python outils/verifier_matrices.py --strict <copie>`, sortie citée | `macro` | fiche ; J3 (identités, ε = 1e−12 × S, M22) |
| 2 | Contrats hérités, phases et lectures (tableau du § 1.1 ; ADR 0005 et 0007 ; `macro`, `monnaie` pour (c)) — **exigence** | (a) **Plan en phase 2** : il ne lit que l'ouverture (D_H, B_H, variables d'état du bloc, registre) et la phase 1 (W_t, P_t, π_t, taux, leviers, anticipation éventuelle). Il ne lit aucun plan de la phase 2, ni aucun revenu du pas courant, puisque les lignes 5 à 15 s'exécutent en phases 4 et 6. Une lecture de N* ou de la dépense publique du pas exige un ordre interne de la phase 2 : décision citant M22. (b) **Ligne 1 en phase 5**, après le bloc 2, sur v_{H,j,t}. Le bloc ne lit ni la ligne 2 ni la ligne 3. (c) **Souscription en phase 7** : elle ne lit que l'ouverture et les phases 1 à 6, dont D_H après la phase 6. L'ordre interne de la phase 7 (État, ménages, banque, banque centrale) est déclaré avec les fiches 7 à 9, pour report dans `tab:phases`, sans cycle (Q5). (d) **Délai impôts → consommation et transferts → consommation**, déclaré en tours entiers. Il confirme la fiche 2 § 9.4 (un tour pour les ventes) ou en propose la révision, soumise au mainteneur. (e) **Variable d'anticipation consommée**, s'il y en a une (inflation dans un terme de tendance nominal, revenu anticipé) : définition, unité, fenêtre, phase et valeur stationnaire. Une anticipation d'inflation relève de la fiche 8 ; elle suit la même lecture de #24 que les fiches 3, 4 et 8 (Q10), et `monnaie` est alors consulté. Un revenu anticipé formé par le bloc 5 est une variable d'état déclarée. (f) La matrice des lectures reste triangulaire | Tableau phase → lit / écrit par option ; triangularité vérifiée à la main | `macro` ; `monnaie` ((c), (e)) | fiche ; J2 (test de triangularité de l'ordonnanceur) |
| 3 | État stationnaire en forme fermée (gabarit 2 ; `macro`) — **exigence** pour (a), (b), (c) et (e) ; **mesure** pour (d) | (a) **Trajectoire de référence**, celle des fiches 3 et 4 : volumes en hausse de g par an (g/n_a par pas), prix en hausse de (1 + π̄)^{1/n_a} − 1 par pas, croissance nominale par pas γ = (1 + g/n_a)(1 + π̄)^{1/n_a} − 1. Sur cette trajectoire, chaque grandeur a sa valeur stationnaire en forme fermée, sans simulation : V_H/(12 × revenu disponible du pas), C/revenu disponible, taux d'épargne, B_H/V_H, taux d'exécution (égal à 1, la demande étant servie). Chaque variable d'état a sa valeur stationnaire, d'où se déduit l'état initial résolu sans préparation. Identité à écrire : taux d'épargne stationnaire = n_a γ × V_H/(n_a × revenu du pas). C'est l'acquis « la propension à consommer ne fixe pas la dépense ; taux d'épargne stationnaire = g × richesse/revenu » (R, faits § 8), lu ici en croissance nominale. La fiche dit lequel de ses paramètres fixe le ratio de richesse et lequel la propension. (b) **Indépendance envers n_a** : le ratio de richesse annuel, le taux d'épargne et B_H/V_H ne dépendent pas de n_a. Toute dépendance est écrite et chiffrée pour n_a = 4, 12 et 52, avec la condition qui la supprime. Elle peut venir d'un revenu retardé d'un pas (facteur 1/(1 + γ) : 0,990111, 0,996690 et 0,999235 à n_a = 4, 12 et 52, pour g = π̄ = 2 % ; commande au Retour) ou de la conversion d'une propension annuelle à la richesse. (c) **Population active et g_N** : la fiche reprend M25 (Q9). (d) **Dépendance à π̄** : le ratio de richesse, le taux d'épargne et C/revenu disponible sont écrits et chiffrés à π̄ = 2 % et 10 %, revenu nominal ou corrigé de l'inflation (Q3). Illustration : sous une cible nominale V_H/revenu annuel = 1, le taux d'épargne stationnaire vaut 3,985 % à π̄ = 2 % et 11,585 % à π̄ = 10 % (g = 2 %, n_a = 12 ; commande au Retour). (e) **Bouclage** : la fiche écrit la condition de compatibilité entre son ratio de richesse stationnaire et les stocks émis par les autres secteurs (dépôts, fiche 7 ; titres, fiche 9 ; V_H = D_H + B_H). Elle dit quelle grandeur s'ajuste à l'état stationnaire : niveau d'activité, dette publique ou taux. C'est la « fermeture du niveau d'activité » de l'acquis R (faits § 8). Calcul conjoint en forme fermée avec la fiche 6 quand les deux fiches sont « avis rendus », avant M27 et M28 ; puis avec la fiche 9 (branche n° 4) | Calcul à la main dans la fiche. Au J3, script contre moteur : un pas sans choc depuis l'état initial résolu laisse chaque variable d'état du bloc sur sa trajectoire stationnaire à **1e−10 près en relatif** (seuil des fiches 2 à 4, reconduit) | `macro` | fiche ; avant M27-M28 ; J3 |
| 4 | Aucune vitesse d'ajustement ne détermine l'état d'arrivée (`docs/exigences.md` § 2.7 ; `macro`) — **exigence** | (a) Aucune vitesse, ni la durée du pas, n'apparaît dans les formes fermées du critère 3. **Cas à examiner explicitement**, en hypothèse α1 = 0,6, α2 = 0,4 par an, g = 2 %, n_a = 12 (commande au Retour) : (i) Forme du modèle SIM, C = α1·revenu + (α2/n_a)·V : le ratio stationnaire vaut V/revenu annuel = (1 − α1)/(n_a γ + α2), soit 0,9094 an contre une « cible » (1 − α1)/α2 = 1 à π̄ = 2 %, et 0,7754 à π̄ = 10 %. Avec α2 ×0,5, il vaut 1,6677 (cible 2) ; avec α2 ×2, 0,4763 (cible 0,5). α2 règle à la fois le niveau et la vitesse : la fiche dit s'il est une vitesse ou un paramètre de niveau et, dans le second cas, comment la vitesse se règle séparément. (ii) Cible de richesse **sans terme de tendance**, C = revenu + (λ_V/n_a)(V* − V) avec V* = ν·n_a·revenu : V/revenu annuel = νλ_V/(n_a γ + λ_V), soit 0,9262, 0,9617 et 0,9805 pour λ_V = 0,5, 1 et 2 par an (ν = 1 an, π̄ = 2 %). **Avec un terme de tendance** γV* (même construction que `sec:production` l. 617), V = V* exactement. Ce terme demande une lecture de π̄ (critère 2 (e), Q10). (iii) Ajustement partiel vers une cible de revenu permanent (v1.5 `eq:cH`, l. 647 ; Y^perm, l. 656) et lissage du revenu (v2.0 `Yperm`, l. 789, `hh_income_speed`) : un revenu lissé qui suit un revenu croissant reste en dessous, d'un écart qui dépend de la vitesse, sauf terme de tendance. Les vitesses hebdomadaires sont converties en base annuelle et confrontées à λ ≤ n_a. Si une dépendance subsiste, elle est écrite, chiffrée pour la vitesse divisée et multipliée par 2, avec la condition qui la supprime. (b) **Aucun intégrateur sans ancre** : une règle sur la croissance de la consommation sans terme de niveau (cible d'Euler seule), ou sur ΔV sans cible, crée un continuum d'équilibres. La fiche le documente et le soumet au mainteneur. (c) La fiche dit ce que le bloc ne détermine pas seul (le niveau d'activité, critère 3 (e)) | Calcul à la main sur les formes fermées. Au J3, depuis l'état initial résolu : dépense publique +1 % pendant 12 tours, puis deux branches où toutes les vitesses du bloc sont multipliées par 0,5 et par 2 (dans λ ≤ n_a). L'écart relatif de chaque ratio du bloc entre les deux branches est au plus de **1e−6 après 720 pas** (seuil reconduit) | `macro` | fiche ; J3 |
| 5 | Stabilité (gabarit 3 ; `macro` ; (d) avec `monnaie`) — **exigence** pour (a), (b) et (c) à la calibration proposée ; **mesure** pour (c) aux vitesses ×0,5 et ×2 et pour (d) | (a) **Instabilités et hypothèses connues** (faits § 6 à 8), non réintroduites sans fait nouveau. Instabilités : n° 6 (effet richesse normé par défaut, R ; son sens exact est à établir à l'instruction, la source, contexte § 5, n'étant pas versée) ; n° 8 (buffer-stock calibré sur un risque iid sans persistance, R) ; n° 15 (un plafond produit un cycle, par exemple un plafond de dépense en fraction de l'encaisse, `cash_consumption_fraction` = 0,9 de la v2.0, l. 200 et 796) ; n° 16 (tolérances absolues). L'hypothèse réfutée n° 3 (élasticité de la consommation au taux comme mécanisme manquant : chômage de 9,02 % à 8,88 % pour η de 0 à 2) n'est pas reprise sans fait nouveau. Les acquis sont discutés : « la propension à consommer ne fixe pas la dépense », « la politique monétaire peut agir à l'envers (canal rentier) », « la préparation de l'état est décisive » (R, faits § 8). (b) **Boucle propre du bloc** (richesse et revenu anticipé), revenus et prix exogènes, au pas mensuel, linéarisée sur les ratios : valeurs propres de module **strictement inférieur à 1** pour la calibration proposée et pour chaque vitesse ×0,5 et ×2, avec module, demi-vie en tours et période si les racines sont complexes. (c) **Boucle production – stocks – demande** : système N1 à N7 de la fiche 2, où la règle des ménages remplace d = A + m·y_{t−1} (revenu → plan → demande, la richesse étant un état), dépense publique et investissement exogènes (hypothèse). L'emploi est sans retard ou avec le retard retenu à M25. Rayon spectral < 1 à la calibration proposée (exigence). Aux vitesses ×0,5 et ×2 (λ_v, λ_IN et vitesses du bloc 5), le module, la demi-vie et la période sont publiés (mesure). La période d'une paire complexe est confrontée à la bande de 36 à 96 tours de la fiche 3 (condition 5 de `jeu`), sans être exigée ici. (d) **Canal du taux** (Q8) : signe et délai en tours de l'effet d'une hausse de i_D et de i_B sur la consommation, par les revenus d'intérêt (lignes 10 et 11a), par la richesse et, le cas échéant, par la substitution ; avis de `monnaie` | Faits § 6 à 8, puis `tab:instabilites`. Valeurs propres calculées à la main ou par `uv run python`, commande et sortie citées | `macro` ; `monnaie` ((d)) | fiche ; J3 |
| 6 | Propension effective m (fiche 2 § 3.N-8, § 5, réserve 3, § 9.8 ; `macro`) — **exigence** pour (a) et (b), **mesure** pour (c) | (a) **Définition déclarée** : m_H = ∂d_{H,j,t}/∂y_{j,t−1}, linéarisée autour de la trajectoire stationnaire, avec d_{H,j,t} = plan / p_{j,t} et les prix sur leur trajectoire stationnaire. Unité : u.v. par u.v., sans dimension. Dénominateur : y_{j,t−1}, production du pas précédent, en u.v. par pas. Fenêtre : un pas (propension d'impact). Est aussi donnée la propension de long terme, après convergence de la richesse sous une hausse permanente de y. (b) m_H s'écrit comme le produit d'une propension des ménages et de la part θ de la valeur de la production marginale qui atteint leur revenu disponible dans le pas. θ dépend de la fiche 3 (emploi, rétention), de la fiche 6 (dividendes) et de la fiche 9 (impôts, transferts, allocations) : ces contributions restent symboliques, avec une valeur sous hypothèses déclarées. Le total m = m_H + m_F + m_G est consolidé au J3, après la fiche 9 (branche n° 4), pour la réserve 3. Le scalaire m résume la boucle ; le test du J3 porte sur la linéarisation complète. (c) Valeur de m_H à la calibration proposée. Si m_H dépasse seul 0,8, la fiche le dit : c'est le seuil de la réserve 3, qui impose de revoir la calibration des vitesses avant l'essai | Formule dans la fiche ; valeur sous hypothèses, commande citée | `macro` | fiche ; J3 (réserve 3) |
| 7 | Test zéro des ratios du bloc (`docs/exigences.md` § 2.6 ; O1 ; `macro`) — **exigence**, mesurée au J3 | Sur 60 ans (720 pas) sans choc depuis l'état initial résolu, pour plusieurs graines : la moyenne par blocs de 5 ans (60 pas) de chaque ratio reste dans sa bande autour de la valeur stationnaire résolue. **Bandes proposées**, à confirmer par le mainteneur avec O1 avant l'essai (M19) : richesse des ménages rapportée au revenu disponible annuel (V_H d'ouverture / (12 × revenu disponible du pas), M22 lecture (e)), ±2 % en relatif ; taux d'épargne (12 tours), ±0,5 point ; part des titres publics dans la richesse (B_H/V_H, moyenne sur 12 tours), ±1 point, si l'option détient des titres (bande commune avec la fiche 9, avis de `monnaie`). Aucune demande non servie des ménages sur les 720 pas. Pour mémoire seulement, sans valeur de référence : G1 rapporte 0 semaine de contrainte budgétaire d'un groupe de ménages sur 260 semaines, et 145 semaines dans la branche « R3 désactivé » (S+O, faits § 2). Toute dérive depuis l'état résolu est un défaut | Au stade de la fiche, seul le préalable (critère 3) se vérifie ; au J3, test zéro du socle | `macro` ; mainteneur (bandes) | J3 |
| 8 | Bornes et non-négativité des encaisses (gabarit 6 ; #38, lecture (ii) ; `CONVENTIONS.md` § 2.4 ; `sec:cadre-caisse` ; `macro`) — **exigence** | (a) **D_H ≥ 0** après chaque paiement des ménages (ligne 1 en phase 5, ligne 7 en phase 6, ligne 19a-ménages en phase 7) et **B_H ≥ 0** sont des **contraintes de conservation** : les assouplir créerait un crédit aux ménages ou une vente à découvert, instruments absents du socle (`sec:cadre-bilans`, l. 225). Elles sont sans paramètre, déclarées dans les `\limites`, avec leur activité à l'état stationnaire (inactives ; marge chiffrée en mois de consommation) et un test. La fiche dit quel mécanisme de la règle les en éloigne, dans quel ordre les paiements des ménages sont honorés (Q7) et ce qui se passe si un paiement excède les dépôts (ligne nommée et bloc qui la porte), sans découvert implicite. Le plan de la phase 2 ne connaît pas WB_t : la fiche montre que le paiement de la phase 5 (au plus D_H d'ouverture + WB_t) est respecté par construction, ou déclare la ligne de rationnement. (b) **Autres bornes**, classées par le critère de tri, chacune déclarée avec son paramètre éventuel, motivée contre un mécanisme et son activité à l'état stationnaire dite. Exemples : v2.0, dépense écrêtée à [0 ; 0,9 × encaisse] (l. 796 et 200, à seuil libre) et `np.maximum(dépôts, 0)` (l. 795) ; v1.5, parts de portefeuille bornées à [0 ; 1] (`eq:portfolio`, l. 696, « on les borne » : la non-négativité est de conservation, mais un écrêtage tenant lieu de mécanisme est à motiver), `cov_t` écrêté à [0 ; 1] (l. 645), subsistance de Stone-Geary (l. 666). (c) **Instabilité 15** : aucune borne active à l'état stationnaire ni dans les scénarios O2 (dépense publique +1 % et +5 %). Une borne activée dans le scénario adverse cesse de l'être **au plus tard 12 tours après la fin du choc** et ne se réactive pas sans nouveau choc (seuil des fiches 3 et 4, reconduit) | Décompte des bornes par option, avec classement. Cas à la main : impôts sur les ménages doublés pendant un tour, dépôts après chaque phase. Au J3 ou au J4 : scénarios O2 et scénario du critère 11 | `macro` ; mainteneur (seuil de (c)) | fiche ; J3 ou J4 |
| 9 | Frontière dette publique : détention de dépôts et de titres publics (`docs/blocs/README.md` § 2 ; `macro` ; avis de `monnaie` au § 6) — **exigence** pour (a) et (b), **mesure** (avis) pour (c) | (a) **Détention déclarée.** Si les ménages détiennent B_H au socle, la fiche donne la règle (forme, variables lues : i_B, i_D, richesse ; phase 7), la part stationnaire B_H/V_H et la lecture de #24 retenue pour chaque taux annuel. Sinon (B_H ≡ 0, Q4), elle dit la conséquence sur les lignes 11a, 19a-ménages et 19b-ménages (montant nul, ou retrait par une décision citant M22) et sur le placement, assuré alors par la banque et la banque centrale seules. (b) La demande de titres des ménages est **une demande**. La fiche ne fixe ni l'émission (État, phase 7, besoin réalisé) ni la clôture du placement : souscripteur du reliquat, rationnement d'une demande des ménages supérieure à l'émission, prime (fiches 7 à 9). Elle dit ce qu'elle reçoit (quantité servie, taux), dans quel ordre de la phase 7, et si les ménages subissent ou décident les achats de la banque centrale (ligne 19b-ménages). (c) `monnaie` rend son avis sur (a), (b) et le critère 5 (d). Un désaccord est décrit en deux positions, et le mainteneur tranche | Règle et forme fermée de B_H/V_H ; tableau de la phase 7 ; avis de `monnaie` | `macro` ; `monnaie` | fiche ; fiche 9 (placement) |
| 10 | Ce que le bloc lit du bloc État et des autres blocs de revenus (fiche 9 ; #41 ; `macro`) — **exigence** | (a) **Liste des grandeurs lues de la fiche 9**, chacune avec sa phase et sa date de lecture (ouverture, phase 1 ou phase 6) : T_H (ligne 7), Tr (ligne 6), i_B (ligne 11a), leviers fiscaux et transferts lus en phase 1. Leurs règles ne sont pas fixées. La dépendance du bloc s'écrit sous une forme symbolique (revenu après impôts, quelle que soit la règle d'impôt), pour que la fiche 9 choisisse sa règle sans réécrire la fiche 5. (b) Même déclaration pour WB (fiche 3), Div_F (fiche 6), i_D et Div_Bk (fiche 7). (c) Les hypothèses provisoires des calculs à la main (impôt proportionnel, transferts nuls…) sont déclarées comme telles et remplacées à la fiche 9. (d) La règle n'anticipe pas les impôts futurs (comportement ricardien) sauf option déclarée, avec sa conséquence sur l'effet de la dette | Tableau des grandeurs lues (bloc, ligne, phase, date) | `macro` | fiche ; fiche 9 |
| 11 | Dépense demandée et exécutée ; scénario adverse de sur-commande (fiche 2 § 7, § 9.5 condition 6, § 9.6 ; `macro`, `jeu`) — **exigence** pour (a), (b) et le seuil de (c) ; **mesure** pour l'ampleur en (c) et pour (d) | (a) **Restitution au tour** : dépense demandée (plan, u.m.), dépense exécutée (C, u.m.), taux d'exécution, demande non servie des ménages (tableau de la fiche 2 § 9.4) ; condition 1 de `jeu`. (b) Sous rationnement, la règle dit en forme fermée ce qu'elle fait au pas suivant du budget non dépensé : terme de richesse, report, ou rien. Aucun mécanisme ne fait croître le plan sans limite du seul fait de la demande non servie : le plan suivant est fonction des stocks et des revenus, non de la demande non servie cumulée. (c) **Scénario adverse** (J4) : dépense publique demandée supérieure au disponible du pas pendant 12 tours (dimension proposée : plan public doublé, hypothèse, à fixer avec `jeu`). Sont mesurés (mesure) : la part servie aux ménages, l'épargne forcée (dépôts en mois de consommation), le rattrapage après la fin du choc et le retour du ratio de richesse dans sa bande. **Seuil proposé** (exigence) : la demande non servie des ménages est nulle au plus tard 12 tours après la fin de la sur-commande et ne réapparaît pas sans nouveau choc (seuil des fiches 3 et 4, reconduit). (d) La gratuité de la sur-commande pour l'État (part non exécutée restée sur le compte du Trésor, fiche 2 § 7) est signalée à `jeu` et à la fiche 9, sans être tranchée ici | Cas à la main sur un tour de sur-commande : volumes servis, ligne 1, ΔD_H, plan du tour suivant. Au J4 : scénario O2 adverse | `macro` ; `jeu` ; mainteneur (seuil, dimension) | fiche ; J4 |
| 12 | Lisibilité pour le joueur (gabarit 5 ; `macro`, à soumettre à `jeu`) — **exigence** pour (b), **mesure** pour (a), (c) et (d) | (a) **Indicateurs au tour**, chacun avec sa définition, son unité, son dénominateur et sa fenêtre : consommation en volume (glissement sur 12 tours) ; dépense demandée et dépense exécutée ; revenu disponible réel (revenu / P_t, glissement sur 12 tours) ; taux d'épargne (12 tours) ; richesse des ménages en années de revenu disponible ; composition dépôts / titres ; demande non servie des ménages. S'y ajoutent les niveaux normaux (ratio de richesse, taux d'épargne) publiés par le script d'état stationnaire, comme pour la condition 2 de `jeu` à la fiche 2. (b) **Délais en tours entiers** : impôts → consommation ; transferts → consommation ; dépense publique → revenu → consommation ; taux → revenus d'intérêt → consommation. La contrepartie est visible le même tour (dépôts des ménages, lignes 6 et 7). Aucun effet plus rapide que le tour sans contrepartie. (c) Tableau levier → indicateur → délai → contrepartie pour les impôts, les transferts, la dépense publique et le taux. Aucun levier propre sans décision (Q11) ; aucun drapeau de mode. (d) **Ampleur** : la part d'un transfert de +1 % du revenu disponible pendant 12 tours qui est dépensée en 12 tours est perceptible à l'échelle d'une partie (60 à 120 tours) ; **seuil à proposer par `jeu` au mainteneur**. Signes non contre-intuitifs : une hausse de taux qui accroît la consommation (canal rentier) est déclarée | Tableau du § 9, « Interfaces ». Exemples datés à la main : (i) même choc que les fiches 2 à 4, dépense publique +1 % aux tours 1 à 12, part de G 20 % (hypothèse) ; (ii) transferts +1 % du revenu disponible aux tours 1 à 12 (hypothèse). Pour chacun : plan, C, revenu disponible, taux d'épargne et ratio de richesse aux tours 1, 2, 3, 4, 9, 13, 14, 18 et 24. Avis de `jeu` (§ 7) ; au J4, scénario apparié (O2) | `jeu` ; `macro` (exemples datés) | fiche ; J4 |
| 13 | Simplicité, empreinte sur l'état, déterminisme (gabarit 6 et rubrique 9 ; principe de simplicité ; `macro`) — **mesure** (décompte) et **exigence** (sans historique, état caché ni drapeau) | Décompte par option : paramètres, bornes, variables d'état, registres, lignes, phases touchées et nombre de strates (Q6). Chaque élément est justifié par une identité vérifiable ou un mécanisme perçu. Chaque variable d'état (revenu retardé, revenu anticipé, richesse cible) a son unité et sa valeur stationnaire (critère 3) ; aucun historique. Aucun état caché : les `getattr` avec valeur par défaut de la v2.0 (`Yperm_real`, l. 789 ; `_other_perm_real`, l. 792) sont exclus (ADR 0002). Une seule règle par mécanisme : les modes de la v2.0 (`household_mode` : euler, income, buffer_stock, l. 389 ; `portfolio_mode` ; `wiu_epsilon` ; mélange `euler_share`, l. 163) ne sont pas repris comme drapeaux. Aucun tirage, ou un tirage par la graine du pays, déclaré | Tableau de décompte ; liste des variables d'état | `macro` | fiche ; J2 (reprise exacte) |
| 14 | Coût de calcul (gabarit 4 ; invariant 3 ; `macro`) — **exigence** (aucune itération) et **mesure** (décompte) | Aucune itération ni optimisation à chaque pas (ADR 0002, invariant 3). Une règle d'optimisation (Euler sur un horizon, richesse dans l'utilité) n'est admise qu'en forme fermée. À examiner sur la branche active de D1 : `joint_portfolio.py` résout par `brentq` (l. 84 et 117) et `wealth_utility.optimum` itère jusqu'à 100 fois (l. 16 et 37). Décompte des opérations par pas. **Part indicative proposée : 0,48 ms par pays-pas**, celle adoptée pour les blocs 2 à 4 ((52/12 − 0,5)/8) | Décompte dans la fiche ; au J3, `tests/invariants/test_budget.py` | `macro` ; `audit` | fiche ; J3 |
| 15 | Notation (`CONVENTIONS.md` § 5.2 ; décision du 02/10/2026 sur #23 ; `macro`) — **exigence** | Chaque symbole a un seul sens. Aucune collision avec les indices réservés (c, j, k, h, t ; s, ℓ, u du cadre) ni avec `tab:symboles`. En particulier : S (échelle du bilan), σ (stock cible), ρ̄ (rapports stationnaires), κ et L sont pris ; m est réservé à la propension de la demande à la production (fiche 2 ; à départager avec la marge normale, fiche 4 critère 13), et les propensions des ménages prennent un autre symbole ; β, employé par la v1.5 pour l'escompte et pour Stone-Geary, est proscrit sans indice distinctif. V_H, D_H, B_H, C, Tr, T_H, Div_F et Div_Bk gardent leur sens ; h, s'il est employé, désigne une strate. L'anticipation suit la convention de l'exposant e, son symbole étant fixé avec la fiche 8 | Liste des symboles confrontée à `tab:symboles` (commande `grep` et sortie citées) | `macro` ; `docwriter` (section) | fiche ; section proposée |
| 16 | Calibrabilité et faits établis (`macro`) — **mesure** | Les paramètres se calibrent sur des ordres de grandeur établis, chacun avec sa source retrouvée et sa date : taux d'épargne des ménages, richesse rapportée au revenu, propension à consommer un revenu transitoire, part des ménages contraints, composition du patrimoine financier. Les faits contestés sont séparés. Sources candidates, **non lues à ce jalon**, existence vérifiée : Jappelli et Pistaferri (2010), *Annual Review of Economics* 2, 479-506 ; Galí, López-Salido et Vallés (2007), *Journal of the European Economic Association* 5(1), 227-270 ; Carroll (1997), *Quarterly Journal of Economics* 112(1), 1-55 (buffer-stock ; instabilité 8). Les chap. 3 (modèle SIM) et 4 (modèle PC) de Godley et Lavoie (2007), dont l'existence et le contenu sont établis par des reproductions, sont à retrouver dans l'ouvrage. Les sources statistiques (comptes nationaux) sont à retrouver. Un résultat de la v1.5 ou de la v2.0 n'est pas un fait établi ; une source introuvable est déclarée | Sources citées ; « non trouvée » le cas échéant | `macro` | fiche ; J3 (calibration) |
| 17 | Remesure des faits de la première tentative (décision P1 du 03/10/2026 ; `CONTEXT.md` ; `macro`) — **exigence** de procédure | (a) Chaque fait cité porte son statut (S+O, O, R, L, V, V+O). Les faits établis sur D1 ne sont pas remesurables, D1 n'étant pas versé ; ils sont cités avec leur statut d'origine. (b) Toute remesure (statut V) passe par un script d'`outils/` qui exécute le prototype **dans un processus séparé, jamais par import** (invariant 4), revu par `audit` (circuit 3, `coder` → `audit`). Ses critères sont écrits dans la fiche **avant l'essai**, sur le modèle de la remesure S1 (fiche 2 § 9.7) : grandeur, définition, unité, fenêtre, seuil. Son verdict est publié même défavorable. Le statut V+O n'est donné que si le vérificateur réexécute le script. (c) Un fait V sur le prototype v2.0 reste un fait de la première tentative, jamais un résultat v3. (d) Les lectures de code (L) citent fichier et ligne, vérifiés à la date de la fiche, **avec la branche active et les coefficients effectifs du profil** : `portfolio_mode='joint_equity'` dans D1 (faits § 1.1), qui exige `wiu_epsilon` > 0 (`model.py` l. 828) ; la valeur de `wiu_epsilon` dans D1 n'est pas établie par la synthèse des faits | Liste des faits et statuts ; commande, sortie et commit de chaque script | `macro` ; `coder` ; `audit` | fiche (jalon 2) |

### Amendements adoptés

Décisions du mainteneur du 03/10/2026, prises avant l'instruction, sur les questions de `macro` :

- **Critères** : les dix-sept critères sont validés tels quels, avec leur nature (exigence ou mesure).
- **Seuils reconduits des fiches 2 à 4**, adoptés : 1e−10 en relatif (critère 3) ; écart ≤ 1e−6 après 720 pas (critère 4) ; 0,48 ms par pays-pas (critère 14) ; 12 tours pour la désactivation d'une borne (critère 8 (c)) et pour la fin de la demande non servie après une sur-commande (critère 11 (c)).
- **Bandes du test zéro** (critère 7), adoptées, à confirmer avec O1 avant l'essai (M19) : ratio de richesse ±2 % en relatif ; taux d'épargne ±0,5 point ; B_H/V_H ±1 point, bande commune avec la fiche 9.
- **Critère 3 (e), bouclage** : l'état stationnaire conjoint est calculé avec la fiche 6 avant M27-M28, puis avec la fiche 9 à la branche n° 4 ; M27 peut être prise sans la fermeture de la fiche 9, au risque assumé d'une révision M-m.
- **Critère 5 (c)** : rayon spectral < 1 exigé à la calibration proposée ; période et demi-vie publiées aux vitesses ×0,5 et ×2 ; aucune bande de période exigée (règle de l'amendement de la fiche 3).
- **Critère 6** : m_H fourni comme propension d'impact et de long terme ; m total consolidé au J3, après la fiche 9.
- **Critère 11 (c)** : la dimension du scénario adverse de sur-commande est fixée avec `jeu`.
- **Critère 3 (d)** : la dépendance à π̄ reste une mesure.
- **Q4** : l'option B_H ≡ 0 au socle est admise à l'instruction, sans retrait des lignes (un retrait demanderait une décision citant M22).
- **Q6** : un ménage représentatif est instruit comme référence, avec une variante à deux types.
- **Q10 et critère 2 (e)** : `monnaie` est consulté sur la frontière inflation (anticipation consommée par un terme de tendance nominal), en plus de la frontière dette publique.
- **Q11** : les leviers ciblés sur les ménages sont renvoyés au catalogue des leviers (J4) ; la fiche en note l'interface.

Décision du mainteneur du 03/10/2026, prise avec M27 (issue #59) :

- **Correction prospective du critère 4 (ii)** : l'illustration de la cible sans tendance se lit **C = revenu − (λ_V/n_a)(V\* − V)**, et non « + » (coquille de signe relevée par `macro` au § 3 ; les chiffres publiés correspondaient déjà à la forme corrigée). Verdicts inchangés ; l'écriture d'origine reste au tableau du § 2.

## 3. Options

*Rédigé par `macro` (expert pilote), 03/10/2026, sur la fiche à l'état `de91847` et l'ADR 0008 (proposé, `ffe4520`). Branche `claude/j1-economie-reelle`, PR #43.*

### 3.0 Conventions de l'instruction

**Découpage par question** (gabarit, § 3). Les options nouvelles (S, C, R, D) partagent un socle commun (§ 3.N) : revenu disponible, revenu lu (Q2), inflation (Q3, Q10), portefeuille (Q4), phases (Q5, Q7), bornes, strates (Q6). Elles ne diffèrent que par la règle de consommation. A et B sont instruites en entier.

**Notation provisoire** (critère 15), fixée à la décision :
- C^plan_t : plan de consommation, en u.m. par pas, écrit en phase 2 (exposant `plan`, comme G^plan de la fiche 2).
- YD_t : revenu disponible du pas.
- YD^e_t : revenu disponible anticipé du pas.
- ν : cible de richesse, en années de revenu disponible.
- λ_V : vitesse annuelle de rappel de la richesse.
- α_1, α_2 : propensions de la forme de Godley et Lavoie (option S).
- θ_H : part de la valeur de la production marginale qui atteint le revenu disponible dans le pas (critère 6).
- Γ = [(1 + g)(1 + π̄)]^{1/n_a} : facteur de croissance nominale par pas ; γ = Γ − 1.

Contrôle par `grep -c -F` sur `nations_et_marches.tex` :
- `\nu`, `\theta`, `YD`, `Y^D`, `\lambda_V`, `\mathrm{plan}`, `V^*` : 0 occurrence chacun ;
- `\alpha` : 1 occurrence, dans `sec:ecartees` (l. 1026), au sens de la part du capital de la v1.5, donc une collision de lecture à juger par `docwriter` ;
- `\rho` : pris (ρ̄_IN, ρ̄_K), d'où « r » est évité pour un taux propre au bloc ;
- `\chi` : 1 occurrence, locale (l. 617).

**Classement des taux du bloc (ADR 0008, point I.2)** :

| Taux | Nature | Conversion |
|---|---|---|
| i_D, i_B (lignes 10, 11a) | flux sur encours | linéaire, i/n_a |
| λ_V | vitesse | linéaire, λ_V/n_a, avec λ_V ≤ n_a |
| g, π̄, π^e, et l'inflation lue dans le terme de tendance | croissance ou inflation | géométrique : Γ = [(1 + g)(1 + π)]^{1/n_a} |
| ν | cible de niveau, en années | V* = ν·n_a·YD^e |

ν n'est pas un taux. Son facteur n_a est un changement d'unité, non une conversion.

**Hypothèses de calcul** (ce ne sont pas des calibrations) :
- g = 2 %, π̄ = 2 % et 10 %, n_a = 12 (et 4, 52) ;
- ν = 1 an, λ_V = 0,4 par an ;
- i_D = 0 ou 3 % ;
- θ_H = 0,8 (salaires seuls : ω̄ = 1/(1 + μ̄), μ̄ = 0,25 ; profits retenus) ou 1,0 (profits distribués dans le pas) ;
- impôts et transferts nuls (hypothèse provisoire, critère 10 (c)) ;
- fiche 2 : λ_v = 3, λ_IN = 1,5 par an, σ = 1,4 mois ;
- emploi R plafonné à N^pa avec U^eq = 5 % ; prix figés à (1 + μ̄)·UC sur leur sentier.

**Calculs** (03/10/2026). Commande : `uv run --no-project [--with numpy] python <script>` dans le scratchpad. Sorties citées au Retour.

| N° | Script | Objet |
|---|---|---|
| F1 | `f5_calculs.py` | formes fermées sous (G) : SIM (revenu courant et retardé), cible sans tendance, transposition v2.0 ; n_a = 4, 12, 52 ; π̄ = 2 % et 10 % |
| F2 | `f5_F2.py` | contre-épreuve par simulation de la règle C |
| F3 | `f5_calculs.py` | taux d'épargne nominal et corrigé (Haig-Simons) |
| F4 | `f5_calculs.py` | m_H d'impact et de long terme |
| F5 | `f5_calculs.py` | boucle propre (critère 5 (b)) |
| B1 | `f5_boucle.py` | boucle fiche 2 + ménages (critère 5 (c)), avec validation ; exemples datés ; sur-commande |
| B2 | `f5_sc.py` | sur-commande sur 720 pas |

**Validations et contre-épreuves** :
- B1, avec la règle fixe d = A + m·y_{t−1} et g = 0, reproduit exactement la fiche 2 : 0,9459 et 73,0 tours (m = 0,6) ; 0,9770 et 95,9 tours (m = 0,8).
- F1 recalcule les illustrations du critère 4, avec un écart dû à la lecture (G), dans laquelle elles n'avaient pas été écrites :
  - (i) SIM : 0,9098 contre 0,9094 publié (π̄ = 2 %) ; 0,7757 contre 0,7754 (10 %) ; α_2 ×0,5 : 1,6690 contre 1,6677 ; ×2 : 0,4764 contre 0,4763 ;
  - (ii) cible sans tendance : 0,9265 / 0,9618 / 0,9806 contre 0,9262 / 0,9617 / 0,9805.
- **Constat sur la rédaction du critère 4 (ii).** La formule s'y lit « C = revenu + (λ_V/n_a)(V* − V) ». Prise à la lettre, elle donne V > V* et un signe absurde : on consommerait plus sous la cible. Les chiffres publiés correspondent à **C = revenu − (λ_V/n_a)(V* − V)**. Je ne modifie pas le critère ; je signale une coquille de signe, à corriger de façon prospective si le mainteneur le juge utile.
- Une première version de la contre-épreuve F2 portait une erreur de détendance : le facteur Γ était compté deux fois dans YD^e. Elle donnait 0,96 à 0,9998 au lieu de 1. Elle est corrigée dans `f5_F2.py` ; aucun chiffre publié n'en provient.

**Intégrité des sources** : `sha256sum` de `model.py` (e1505b7e…) et du `.tex` de la v1.5 (097d023f…), identiques à `tests/invariants/archive_sha256.txt`. Lignes vérifiées le 03/10/2026.

**Littérature** :

| Source | Ce qui est établi | Statut |
|---|---|---|
| Godley et Lavoie (2007), SIM (chap. 3) et PC (chap. 4) | SIM : C = α_1·YD + α_2·H_{−1}, avec α_1 = 0,6, α_2 = 0,4, θ = 0,2 ; SIMEX : YD^e = YD_{−1} ; PC (éq. 4.5) : C = α_1·YD + α_2·V_{−1} ; demande de titres (éq. 4.7) : B_h = V(λ_0 + λ_1·r − λ_2·YD/V), avec λ_0 = 0,635, λ_1 = 5, λ_2 = 0,01, r̄ = 2,5 % | **lu par reproduction** : PKSFC (A. Godin), fichiers `SIM.txt`, `SIMEX.txt` et `PC.txt` (le tutoriel les dit tirés de l'appendice 3.1, p. 91 de l'ouvrage). **Ouvrage non lu** |
| *Idem*, PCEX2 | α_1 = α_10 − ι·r (α_10 = 0,7, ι = 4) : la propension baisse avec le taux | reproduction sfcr (J. Macalós), `gl2-pc.Rmd` l. 339 à 344. Ouvrage non lu |
| *Idem*, DISINF (chap. 9) et INSOUT (chap. 10) | revenu « Haig-Simons » : ydhs = c + Δmh ; ydr = YDr/p − π·V_{−1}/p ; consommation réelle sur le revenu réel corrigé de la perte d'inflation sur la richesse ; INSOUT α_1 = 0,95, α_2 = 0,05 | reproduction sfcr, `gl6-dis.Rmd` l. 73 à 77, `gl7-insout.Rmd` l. 264 à 279. Ouvrage non lu. **Q3 : le chapitre est retrouvé par reproduction, la page n'est pas vérifiée** |
| *Idem*, GROWTH (chap. 11) | C_k = α_1(YD^e_kr + NL_k) + α_2·V_k(−1) (éq. 11.53, α_1 = 0,75, α_2 = 0,064) ; YD_kr = YDr/P − ΔP·V_k(−1)/P (11.55) | reproduction sfcr, `gl8-growth.Rmd` l. 116 à 127, 226 et 227 |
| Jappelli et Pistaferri (2010), NBER WP 15739 | Blundell, Pistaferri et Preston (2008) : propension à consommer un choc transitoire d'environ 5 % (plus forte chez les pauvres), un choc permanent d'environ 0,65 (WP p. 42). Hall et Mishkin : 29 % (p. 42). Italie : environ 1 et 0,3 (note 20). Johnson, Parker et Souleles (2006) : 20 à 40 % du remboursement de 2001 dépensés en biens non durables en trois mois (p. 29). Conclusion : forte hétérogénéité, rôle des contraintes de liquidité (p. 47-48) | **lu** |
| Parker, Souleles, Johnson et McClelland, NBER WP 16684 (version de 2013) | 12 à 30 % des paiements de 2008 en biens non durables sur trois mois ; 50 à 90 % de dépense totale | **lu** (résumé, p. 1 du PDF) |
| Kaplan, Violante et Weidner, NBER WP 20073 (2014) | 25 à 40 % des ménages américains « hand-to-mouth », estimation préférée un tiers (p. 3) ; 31 % en moyenne sur 1989-2010, dont deux tiers « riches » (p. 22) ; environ 20 % du revenu (p. 23) | **lu** |
| Carroll, Otsuka et Slacalek, NBER WP 12746 (2006) | propension à consommer la richesse immobilière : environ 2 cents au trimestre suivant, 9 cents à long terme (p. 2) ; « sagesse conventionnelle » de 3 à 5 cents (p. 1) ; 4 à 10 cents sur plusieurs années (p. 13) ; l'effet de la richesse boursière est plus faible | **lu** |
| Galí, López-Salido et Vallés, NBER WP 11578 | existence vérifiée (PDF téléchargé) | **contenu non lu** |
| Fagereng, Holm et Natvik (gains de loterie) | — | **non retrouvé** dans la session |
| Taux d'épargne, richesse rapportée au revenu (Fed Z.1, BCE) | page B.101h de la Fed accessible ; BCE non accessible | **non lu**, aucun chiffre retenu |

**Ce que la littérature permet de conclure** :
- la propension à consommer un revenu transitoire est hétérogène : environ 0,05 dans les modèles d'assurance, mais 0,2 à 0,4 sur un trimestre pour des transferts ponctuels (biens non durables) et 0,5 à 0,9 en dépense totale ;
- un tiers environ des ménages sont contraints ;
- l'effet richesse, pour une richesse peu liquide, est de 2 à 10 cents par an.

Elle **ne permet pas** de caler λ_V sur la richesse **liquide** (dépôts), qui est celle du socle : la source pertinente (gains de loterie) n'a pas été lue.

### 3.A Option A — v1.5

1. **Source.** `archive/v1.5/Nations_et_Marches_v1_5.tex` :
   - `eq:yd` (l. 631) ;
   - `eq:cB`, `eq:cH`, `eq:cM` (l. 645 à 648) et leur lecture (l. 651 à 656) ;
   - `eq:portfolio` (l. 696) ;
   - table de calibration : l. 2253 (σ = 1), l. 2254 (β = 1/(1 + ρ)), l. 2255 (c_B, c_M, c_H = 0,95 ; 0,80 ; 0,50), l. 2256 (c^V = 0,03), l. 2292 (ψ_h et cov̄), l. 2311 (révision : c = 0,95 ; 0,90 ; 0,80 et c^V = 0 ; 0,04 ; 0,08), l. 2321 (ρ = 0,01).

   **Équations jamais garanties exécutées.**

2. **Équations.**
   - Strate basse : E_B = c_B·Y^d_B + c^V_B·V_B, avec c_h = c^0_h(1 − ψ_h(1 − cov)) et cov écrêté à [0, 1].
   - Strate haute : une cible d'Euler sur la croissance, E_{H,t+1}/E_{H,t} = (β(1 + i^D)/(1 + π^e))^{1/σ}, et un « ajustement partiel vers κ_E(Y^perm_H + r·V_H) ».
   - Strate moyenne : mélange λ_M, sans valeur dans la table.
   - Y^perm : moyenne mobile exponentielle, sans vitesse donnée.
   - Portefeuille : parts de Tobin bornées à [0, 1].
   - **κ_E et λ_M n'ont pas de valeur** (`grep` : l. 647, 648 et 651 seulement ; κ_E désigne par ailleurs la vitesse du cours des actions, l. 1362 et 1367 : collision). La v2.0 porte `kappaE = 0.9` (`model.py` l. 161), qui n'est employé nulle part (L).

3. **État stationnaire.** Il est **non calculable** sans choisir une transposition, pour deux raisons :
   - la combinaison de la cible d'Euler et de l'ancrage de niveau n'est pas écrite (critère 2 du gabarit) ;
   - la vitesse de Y^perm n'est pas donnée.

   Ce qui se démontre :
   - la cible d'Euler seule est un intégrateur sans ancre (critère 4 (b)) : la consommation croît au taux d'Euler, qui n'égale g que si r = ρ + σg. Sinon E/YD dérive ; à r = ρ + σg, tout niveau est stationnaire (continuum) ;
   - un ancrage sur Y^perm lissé sans terme de tendance reste en dessous d'un revenu croissant, d'un écart fonction de la vitesse (critère 4 (iii)) ;
   - strate basse révisée (c^V = 0) : V/(n_a·YD) = (1 − c_B/Γ)/(n_aγ). Le ratio n'est défini que si γ > 0 et diverge sous croissance nominale nulle.

4. **Comportement.** Non mesuré. Les chiffres de la v1.5 (l. 2065, S1 : « propensions ×0,8 : u 20 %, taux zéro » ; l. 2073) sont rapportés et invérifiables.

5. **Coût.** Sans itération dans la forme écrite. Non mesuré.

6. **Défauts.**
   - Critère 4 (Euler sans ancre ; Y^perm sans tendance).
   - Trois strates : sous-colonnes de `tab:matrice-flux`, contrat M22.
   - Bornes à seuil libre : clip de cov, parts dans [0, 1] « on les borne » (l. 700), subsistance de Stone-Geary.
   - Canal de substitution au taux : l'hypothèse réfutée n° 3 n'est pas reprise sans fait nouveau.
   - β est employé deux fois (escompte et Stone-Geary) : critère 15.

7. **Identités.** Ligne 1 ; colonne des ménages en trois strates. Crédit aux ménages (`eq:yd`, i^L_h·L_h) : absent du socle.

8. **Joueur.** Multiplicateur « strate basse » lisible ; canal du taux à la Ramsey (IS).

9. **Empreinte.** Y^perm et E_{H,t−1} par strate, soit 6 variables d'état au moins ; une quinzaine de paramètres, dont 2 sans valeur.

### 3.B Option B — v2.0

1. **Source** (statut L, lignes vérifiées le 03/10/2026). `archive/v2.0/prototype/model.py` :
   - l. 159 : `c` = (0,95 ; 0,90 ; 0,80), `cV` = (0 ; 0,04 ; 0,08) ;
   - l. 162 et 163 : `household_mode='euler'`, `euler_share` = (0 ; 0,5 ; 1) ;
   - l. 165 : `wiu_epsilon` = 0 ;
   - l. 185 : `portfolio_mode='legacy'` ;
   - l. 197 : `hh_income_speed` = 0,02 par semaine ;
   - l. 200 : `cash_consumption_fraction` = 0,9 ;
   - l. 214 : `sB` = 0,30 ;
   - l. 789 et 792 : `getattr` (état caché) ;
   - l. 793 : E_income = c·Yd + cV·V/52 ;
   - l. 795 et 796 : clip à [0 ; 0,9 × encaisse] ;
   - l. 803 à 838 : branches ; l. 838 : E = min((1 − mix)·E_income + mix·E_opt, encaisse) ;
   - l. 1222 : achats de titres = min(sB·(Yd − E), 0,5 × dépôts) ;
   - `joint_portfolio.py` l. 84 et 117 (`brentq`) ; `wealth_utility.py` l. 16 et 37 (Newton, jusqu'à 100 itérations) ; `households.py` l. 74 à 107.

   **Branche active dans D1.** `portfolio_mode='joint_equity'` (faits § 1.1, S+O) impose, par les contrôles des l. 345 et 368 et le test des l. 828 et 829, `sigma` = 1, `household_mode='euler'`, `assets` = True et `wiu_epsilon` > 0. Les l. 803 à 805 sautent alors l'optimiseur liquide, et `decision_and_settlement` (l. 833) résout, chaque semaine :
   - un problème d'utilité de la richesse à horizon de 520 semaines par ménage (`joint_solver.solve`) ;
   - un équilibre du prix des actions (`brentq`).

   **Coefficients effectifs de D1 non établis** : `c`, `cV`, `euler_share`, `wiu_epsilon`, `wiu_targets`, `joint_years`. `config/reference.json` est absent. Le seul profil lisible est celui des valeurs par défaut (`portfolio_mode='legacy'`), qui n'est pas D1.

2. **Équations.**
   - Partie active transposable : la règle de revenu, C = c·YD + cV·V par an. La v2.0 lit le revenu de la semaine même ; transposée sur M24, elle lit YD_{t−1}.
   - Plafond : C ≤ 0,9 × encaisse.
   - Titres : achats en flux, sB·(Yd − E), sans cible de stock ; rachats proportionnels (`treasury.py` l. 59 à 82).

3. **État stationnaire** de la règle de revenu transposée (F1, n_a = 12) : V/(n_a·YD) = (1 − c/Γ)/(n_aγ + cV).

   | Groupe | π̄ = 2 % | π̄ = 10 % | π̄ = 2 %, n_a = 4 / 52 |
   |---|---|---|---|
   | B | 1,3393 | 0,5107 | 1,4914 / 1,2802 |
   | M | 1,2924 | 0,6976 | 1,3642 / 1,2646 |
   | H | 1,6933 | 1,0612 | 1,7352 / 1,6770 |

   - Le groupe B (cV = 0) n'a d'ancre que la croissance nominale : pas d'état stationnaire à γ = 0 (critère 4 (b)).
   - cV est à la fois niveau et vitesse (critère 4 (i)).
   - La part B_H/V_H dépend de l'histoire budgétaire (titres achetés en flux, rachats) : aucune forme fermée.

4. **Comportement.**
   - G1 : 0 semaine de contrainte budgétaire d'un groupe de ménages sur 260 ; 145 semaines dans la branche « R3 désactivé » (S+O).
   - Acquis R : « la propension ne fixe pas la dépense » ; « la politique monétaire peut agir à l'envers ».
   - Aucune élasticité causale de la demande au taux n'est identifiée par G (S+O, G-T).

5. **Coût.** La branche active itère (`brentq` ; Newton jusqu'à 100 fois, sur 520 périodes et 3 ménages) : **échec du critère 14**, qui est une exigence. Coût non mesuré.

6. **Défauts.**
   - Branche active itérative, qui exige des actions (J6) : non transposable au socle.
   - Plafond 0,9 × encaisse, à seuil libre : instabilité 15.
   - `np.maximum(dépôts, 0)` (l. 795).
   - État caché (l. 789 et 792).
   - Drapeaux : `household_mode`, `portfolio_mode`, `euler_share`, `wiu_*`.
   - Instabilités 6 (effet richesse normé par défaut, R, sens à établir) et 8 (buffer-stock, branche `plan_buffer_stock`, l. 818) : non réintroduites si seule la règle de revenu est transposée.

7. **Identités.** Lignes 1, 11a et 19a-ménages. Les actions et l'immobilier sont hors socle.

8. **Joueur.** Propensions par groupe lisibles ; le plafond d'encaisse est invisible.

9. **Empreinte.** Y^perm_real et `_other_perm_real` (cachées), plus les états de l'optimiseur.

### 3.N Socle commun des options nouvelles (S, C, R, D)

**3.N-1 Revenu disponible** (critère 10). Il est connu à la fin de la phase 6 :

YD_t = WB_t (bloc 3, phase 4) + Tr_t (bloc 9, phase 6) + i_D·D_{H,t}/n_a (bloc 7) + i_B·B_{H,t}/n_a (bloc 9) + Div_{F,t} (bloc 6) + Div_{Bk,t} (bloc 7) − T_{H,t} (bloc 9).

La forme est symbolique, quelles que soient les règles d'impôt et de dividende. Les hypothèses provisoires (impôts et transferts nuls, θ_H) sont remplacées aux fiches 6 et 9. Aucune anticipation ricardienne des impôts (critère 10 (d)).

**3.N-2 Revenu lu par le plan (Q2).** Retenu pour S, C et D : **(i) le revenu du pas précédent, porté en variable d'état**, YD^e_t = Γ^e·YD_{t−1}, avec Γ^e = [(1 + g)(1 + π^lu)]^{1/n_a} (ADR 0008, I.1).
- Le terme de tendance supprime la dépendance du ratio stationnaire à n_a qu'aurait un revenu retardé sans tendance (critère 3 (b)).
- Le délai impôts → consommation et transferts → consommation est d'**un tour** : cela **confirme la fiche 2, § 9.4**.
- (ii), un revenu lissé (v2.0, `Yperm`), est écarté : vitesse de lissage dans l'état d'arrivée sans terme de tendance, ou état de plus avec.
- (iii), les composantes connues en phase 1, ne donne pas WB_t (phase 4). C'est l'option R.

**3.N-3 Inflation lue dans la tendance (Q10) et revenu corrigé (Q3).**

Le terme γ·V qu'épargnent les ménages se décompose en deux parts :
- la perte d'inflation sur la richesse nominale, soit la correction de Haig-Simons de Godley et Lavoie (ydr = YDr/p − π·V_{−1}/p, reproduction sfcr) ;
- la part de croissance réelle.

Trois lectures de π^lu :

| Lecture | Valeur stationnaire | Condition d'exactitude |
|---|---|---|
| **(a)** glissement mesuré π_{t−1}, lu dans le registre (ADR 0008, II.2) | π̄ | toujours exacte, quelle que soit la fiche 8 |
| **(b)** π^e de la fiche 8 | π̄ | exacte seulement si C1 tient ; sinon le ratio vaut (γ^e + λ_V/n_a)/(γ + λ_V/n_a) fois la cible, fonction de λ_V : critère 4 |
| **(c)** π̄ (cible) | π̄ | exacte seulement si π̄ = π* (C2) |

Je recommande **(a)**, sous l'avis de `monnaie`.

*Additif du 03/10/2026 (§ 5 mis à jour, § 6.5)* : recommandation révisée en **(c)**, lue sur la **cible déclarée π\*** (paramètre ou levier de la fiche 8), jamais sur π̄ (inflation stationnaire, un résultat) ; dans le tableau, la ligne (c) se lit « π\* (cible) », exacte si π̄ = π\* (C2). (a) est explosive en boucle conjointe (§ 3.C-10). (b) relève de la clause C26 (fiche 8).

Q3, avec ν = 1 et n_a = 12 (F3) :

| | π̄ = 2 % | π̄ = 10 % |
|---|---|---|
| Taux d'épargne nominal = n_aγν | 3,967 % | 11,567 % |
| C/YD | 0,96033 | 0,88433 |
| Revenu de Haig-Simons / revenu nominal | 0,98018 | 0,90431 |
| Taux d'épargne corrigé (Haig-Simons) | 2,025 % | 2,209 % |

Le taux nominal triple avec l'inflation ; le taux corrigé ne bouge presque pas. **Je propose de restituer les deux** ; avis de `jeu`.

**3.N-4 Portefeuille (Q4).** Recommandé au socle : **B_H ≡ 0**.
- Lignes 11a, 19a-ménages et 19b-ménages à montant nul, sans retrait (un retrait demanderait une décision citant M22).
- D_H = V_H, aucune règle de portefeuille, aucune ligne ajoutée.
- Le placement est assuré par la banque et la banque centrale (fiches 7 à 9).
- La dette publique reste une richesse des ménages, mais indirecte : la banque la porte, financée par les dépôts.

Variantes instruites :
- **demande de Tobin** (PC, éq. 4.7) : part stationnaire λ_0 + λ_1·(i_B − i_D) − λ_2/(n_aν), en forme fermée. Elle exige une clôture du placement en phase 7 : une baisse de la demande impose un acheteur (rachat 19a négatif, ou 19b) ;
- **part fixe**.

Les deux sont renvoyées à la fiche 9 ou à J6, avec l'avis de `monnaie`.

**3.N-5 Phases et lectures** (critère 2) :

| Phase | Le bloc 5 lit | Le bloc 5 écrit |
|---|---|---|
| 1 | — | — |
| 2 | ouverture : D_H, B_H, YD_{t−1}, registre (π_{t−1}) ; paramètres g, ν, λ_V | C^plan_t |

*Additif du 03/10/2026 (§ 5 mis à jour, § 6.5)* : sous la lecture (c), le bloc 5 lit en phase 2 la cible π\* et non plus le registre (π_{t−1}).

| 5, après les blocs 4 et 2 | p_t, v_{H,t} | ligne 1, C_t = p_t·v_{H,t} |
| 6 | lignes 5 à 15 reçues | YD_t (variable d'état pour t + 1) |
| 7 | sans objet sous B_H ≡ 0 | — |

- La matrice des lectures est triangulaire ; aucune lecture de N*, y*, G^plan ni I^plan.
- Q5 (ordre interne de la phase 7) est sans objet sous B_H ≡ 0.

**3.N-6 Paiements et bornes (Q7, critère 8).**
- D_H ≥ 0 et B_H ≥ 0 sont des contraintes de conservation, sans paramètre, inactives à l'état stationnaire, avec une marge d'environ 12ν mois de consommation.
- Le plan ne connaît pas WB_t. Le paiement de la phase 5 doit vérifier C ≤ D_{H,t} + WB_t. Deux lectures, soumises au mainteneur (critère de tri de #38) :
  - **(a)** plafond du plan à D_{H,t} d'ouverture, en phase 2 : payable par construction, mais c'est une conservation resserrée, donc **à seuil libre** au sens du tri ;
  - **(b)** plafond en phase 5 à D_H après la phase 4 : c'est la vraie contrainte de conservation, mais il faut que le bloc 2 lise D_H avant de servir, ou un pré-plafond du bloc 5 en tête de phase 5, ce qui modifie l'ordre de M24.
- Je préfère (a), déclarée et testée, inactive à l'état stationnaire.
- Priorité des paiements : ligne 1 (phase 5), puis ligne 7 (phase 6, après les recettes de la phase 6).
- **Cas à la main** (impôts doublés pendant un tour ; D_H = 1 200, WB = 80, plan 96, T_H = 16 → 32, intérêts 3) :
  - D_H vaut 1 280 après la phase 4, 1 184 après la phase 5, 1 155 après la phase 6, soit environ 12 mois de marge ;
  - le plan du tour suivant baisse de (1 − νλ_V)·16 = 9,6 sous C.
- **Aucune autre borne** dans S, C et D.

**3.N-7 Cohérence stock-flux (critère 1).**
- Cas à la main : demande des ménages servie à 90 %. D_H = 1 200, plan 96, WB = 80, i_D = 3 %, Div = T = Tr = 0.
- C = 86,4 ; YD = 80 + 3 = 83.
- Par le stock : D_H = 1 200 + 80 − 86,4 + 3 = 1 196,6. Par les flux : V + YD − C = 1 200 + 83 − 86,4 = 1 196,6.
- Le budget non dépensé, 9,6, reste en D_H.
- Aucune ligne ajoutée ; les signatures de `tab:portes-monnaie` sont inchangées.

**3.N-8 Strates (Q6).** Un ménage représentatif au socle, indexé par h comme J = 1 sous M24 (d). La variante à deux types est instruite en D.

**3.N-9 Canal du taux (Q8, critère 5 (d)).**
- Sous S, C et D, le seul canal est **rentier**. Une hausse de i_D au tour n augmente la ligne 10 dès la phase 6 du tour n, puis le plan au tour n + 1.
- Ordre de grandeur, ν = 1 : +1 point de i_D donne +1 % de YD au tour n, et **+0,656 % du plan au tour n + 1**. La propension α_Y = 1 − νλ_V = 0,6, appliquée à un revenu qui vaut 1/0,960 fois le plan (C/YD = 1 − n_aγν), en donne 0,625 point. Le terme de richesse (λ_V/n_a − γ)·ΔV, c'est-à-dire la hausse de revenu restée en dépôts, ajoute 0,031 point.
- Le signe est **positif** (acquis R « à l'envers ») ; il est déclaré.
- Le canal de substitution n'est pas repris : hypothèse réfutée n° 3, sans fait nouveau. La variante PCEX2 (α_1 = α_10 − ι·r) est notée pour `monnaie` et la fiche 8 (élasticité C10).

**3.N-10 Population active (Q9).** Tenue par le bloc 3 (M25 (d)) : sans objet ici.

**3.N-11 Leviers ciblés (Q11).** Renvoyés au J4. Interface : un transfert ciblé entre dans Tr_t ; sous D, il porte une part de revenu distincte (§ 3.D).

### 3.S Option S — forme SIM / PC de Godley et Lavoie

1. **Source.** Reproduction PKSFC : SIM, SIMEX, PC (éq. 4.5). C^plan_t = α_1·YD_{t−1} + (α_2/n_a)·V_{H,t}. Statut : approchée.
2. **État stationnaire** (F1) : V/(n_a·YD) = (1 − α_1/Γ)/(n_aγ + α_2).
   - α_1 = 0,6, α_2 = 0,4 : 0,9143 (π̄ = 2 %) ; 0,7868 (10 %) ; 0,9229 et 0,9109 à n_a = 4 et 52.
   - Avec le revenu courant : 0,9098 ; à α_2 ×0,5 : 1,6690 ; à ×2 : 0,4764.
3. **Critère 4 : échec.** α_2 est à la fois le niveau et la vitesse. Le ratio dépend aussi de n_a, par 1/Γ.
4. **Lecture** : S coïncide avec C si α_1 est **dérivée** de ν et de λ_V (§ 3.C). Écrite avec α_1 et α_2 libres, elle échoue au critère 4 (i).
5. **Empreinte** : 2 paramètres ; 1 variable d'état (YD_{t−1}).

### 3.C Option C — cible de richesse avec terme de tendance (piste de la feuille de route, § 5)

1. **Équations.**
   - C^plan_t = YD^e_t − γ^e_t·V_{H,t} − (λ_V/n_a)(V*_t − V_{H,t}) ;
   - V*_t = ν·n_a·YD^e_t ;
   - YD^e_t = Γ^e_t·YD_{t−1} ;
   - γ^e_t = [(1 + g)(1 + π_{t−1})]^{1/n_a} − 1.

   *Additif du 03/10/2026 (§ 5 mis à jour, § 6.5)* : sous la recommandation finale, γ^e = [(1 + g)(1 + π\*)]^{1/n_a} − 1 et la cible de richesse s'écrit sur le revenu de Haig-Simons, V\*_t = ν·n_a·(YD^e_t − π_s·V_{H,t}), π_s = (1 + π\*)^{1/n_a} − 1 (§ 3.C-10, point 8). Forme réduite : C = α_Y·YD^e + (λ_V/n_a − γ^e + νλ_V·π_s)·V ; α_Y = 1 − νλ_V et la condition νλ_V < 1 sont inchangées.

   Lecture : les ménages dépensent le revenu attendu, moins l'épargne d'entretien (pour que la richesse suive la croissance nominale : correction de Haig-Simons plus croissance réelle), moins une fraction λ_V/n_a de l'écart à la richesse visée.

   Forme équivalente : C = α_Y·YD^e + (λ_V/n_a − γ)·V, avec α_Y = 1 − νλ_V. C'est la forme S avec α_1 dérivée.

   Variante écartée, la tendance sur V* : α_Y = 1 − ν(n_aγ + λ_V). Elle dépend de π̄ et devient négative en haute inflation.

   Statut : approchée (cible de stock de Godley et Lavoie) ; terme de tendance : choix de conception, sur le modèle de la fiche 2, l. 617. Provenance : α_3 = (1 − α_1)/α_2, la richesse cible implicite de SIM (reproduction).

2. **État stationnaire.**
   - V_H/(n_a·YD) = ν **exactement**, quels que soient λ_V, n_a et π̄. F2 : 1,000000000000 pour λ_V = 0,2 / 0,4 / 0,8, n_a = 4 / 12 / 52, π̄ = 2 % et 10 %.
   - Taux d'épargne : n_aγν (identité du critère 3 (a)) ; C/YD = 1 − n_aγν.
   - Dépendance à n_a : seulement par n_aγ (0,039802 / 0,039671 / 0,039620 à n_a = 4 / 12 / 52), donc dans le taux d'épargne, non dans ν. C'est le point I.6 de l'ADR 0008.
   - **ν fixe le ratio de richesse ; λ_V fixe la propension d'impact** α_Y = 1 − νλ_V.
   - **Condition de domaine** (déclarée) : νλ_V < 1, d'où α_Y > 0. À ν = 1, λ_V ≤ 0,8 garde α_Y ≥ 0,2.

3. **Boucle propre** (F5, revenu hors intérêts exogène) : valeur propre réelle.

   | | i_D = 0 | i_D = 3 % | i_D = 10 % |
   |---|---|---|---|
   | λ_V = 0,4 | 0,96678 (20,5 tours) | 0,96772 (21,1 tours) | 0,96994 (22,7 tours) |
   | λ_V ×0,5 | 0,98339 (41,4 tours) | 0,98385 (42,6 tours) | — |
   | λ_V ×2 | 0,93355 (10,1 tours) | 0,93551 (10,4 tours) | — |

   Toutes sont inférieures à 1.

4. **Boucle avec la fiche 2** (B1 ; prix figés, emploi R ; demi-vie en tours) :

   | | i_D = 0 | i_D = 3 % |
   |---|---|---|
   | θ_H = 0,8 | 0,9838, racine réelle, 42,6 | 0,9859, racine réelle, 49,0 |
   | θ_H = 0,8, plage sur la grille ×0,5 / ×2 | 0,9761 à 0,9889 | 0,9768 à 0,9903 |
   | θ_H = 1,0, toute la grille | 0,9964 à 0,9965 (environ 197) | 0,9993 (environ 1 000) |

   - La grille croise les vitesses de la fiche 2 ×0,5 et ×2 avec λ_V ×0,5 et ×2. À π̄ = 10 % (θ_H = 0,8, i_D = 3 %) : 0,9820.
   - Rayon < 1 partout (exigence tenue).
   - La racine dominante est **réelle**. Seule une période de 559 à 750 tours apparaît (vitesses de la fiche 2 ×0,5, λ_V ×2) ; aucune paire n'entre dans la bande de 36 à 96 tours, et aucune n'est exigée.
   - **Sous θ_H = 1, la racine est quasi unitaire** : sans impôts ni autre fuite, le niveau d'activité est presque indéterminé. C'est le constat de bouclage (#44), qui se ferme avec les fiches 6, 8 et 9.

5. **Propension m_H** (F4, critère 6) :

   | | Impact | Long terme |
   |---|---|---|
   | θ_H = 0,8, i_D = 0 | 0,4808 | 0,7683 |
   | θ_H = 0,8, i_D = 3 % | 0,4808 | 0,7920 |
   | θ_H = 1,0, i_D = 0 | 0,6010 | 0,9603 |
   | θ_H = 1,0, i_D = 3 % | 0,6010 | 0,9900 |

   - Formules : impact = α_Y·θ_H·(1 + g)^{1/n_a} ; long terme = θ_H(1 − n_aγν)/(1 − i_Dν).
   - **Si θ_H = 1, m_H de long terme dépasse 0,8 à lui seul (seuil de la réserve 3 de la fiche 2).** θ_H dépend de la fiche 6 (dividendes) et de la fiche 9 (impôts).

6. **Défauts.**
   - Canal du taux rentier seulement (§ 3.N-9).
   - λ_V n'a pas de source lue sur la richesse liquide. L'effet richesse lu (2 à 10 cents, richesse peu liquide) est bien inférieur à λ_V − n_aγ = 0,36 par an : **fidélité à déclarer**.
   - Aucune instabilité connue réintroduite : pas de plafond (instabilité 15), pas de buffer-stock (8), effet richesse non normé par défaut (6 : le paramètre est déclaré).

7. **Coût.** Une dizaine d'opérations flottantes plus une puissance, sans itération. Non mesuré.

8. **Joueur.** Taux d'épargne, ratio de richesse et niveau normal ν lisibles ; épargne forcée visible sous rationnement. Voir les exemples du § 3.L.

9. **Empreinte.** 2 paramètres (ν, λ_V) ; 1 variable d'état (YD_{t−1}, u.m., valeur stationnaire YD_t/Γ) ; lecture du registre de l'ADR 0008, sans état ajouté. *Additif du 03/10/2026 (§ 5 mis à jour, § 6.5)* : sous la lecture (c), le bloc ne lit plus le registre ; il lit π\*.

#### 3.C-10 Boucle conjointe (critère 5 (c) complet ; réserve 3 du § 5)

*Additif de `macro`, 03/10/2026. Maquette hors dépôt, indépendante des scripts B1 et B2.*

**Système**
- Fiche 2 : N1 à N7, lecture (G).
- Bloc 3 :
  - salaire SN : λ_w = 1, β = 2, U^eq = 5 %, lecture (w1) ;
  - emploi C : λ_N = 3,5 (M25).
- Bloc 4 : règle M, avec λ_μ = 1,2 et ψ_ξ = 0,5 (M26). P_t est en lecture (c), registre de 13 niveaux (ADR 0008, II.3).
- Bloc 5 : règle C, avec ν = 1 et λ_V = 0,4.
- Autres valeurs : g = π̄ = 2 %, n_a = 12, σ = 1,4 mois, μ̄ = 0,25.

**Hypothèses de calcul** (ce ne sont pas des calibrations) :
- **Anticipation** : π^e = π̄, exogène, substitut de la fiche 8. SN la lit à l'ouverture.
- **Dépense autonome** (État et investissement) : planifiée en u.m. au prix p_{t−1}(1 + π^e)^{1/n_a}, comme à la fiche 4 (§ 3.0).
  - Son volume Ā est résolu pour que la demande stationnaire vaille 1.
  - N^pa est résolu pour que U = U^eq. C'est la variable de fermeture de #44.
- **θ_H = 0,8** se lit YD = WB_t + i_D·V/n_a : salaires seuls, sureffectif compris (WB = W·N avec N ≥ N*).
- **θ_H = 1** se lit YD = p_t v_t + UC_t(y_t − v_t) + i_D·V/n_a : salaires plus résultat courant (fiche 4, § 3.N-11), distribué dans le pas.
  - À prix figés, cette lecture redonne exactement les rayons de B1 : 0,9965 et 0,9993.
- Impôts et transferts nuls. Le plafond du § 3.N-6 (a) n'est pas modélisé.
- **Inflation lue dans la tendance (Q10)**, deux lectures :
  - (a) π_{t−1} = P_{t−1}/P_{t−13} − 1, lue dans le registre ;
  - (c) π̄.
  - Sous π^e = π̄ exogène, (b) coïncide avec (c).

**Régimes d'emploi.** La règle T4-C a un coude à l'état stationnaire :
- régime H (hausse) : N = N*, comme sous R ;
- régime B (baisse) : N = rétention.

Le jacobien est calculé dans chaque régime. La règle réelle alterne entre les deux ; sa convergence est vérifiée par simulation non linéaire.

**Scripts.** Commande : `uv run --no-project --with numpy python <script>`, dans le sous-dossier `f5c` du scratchpad.

| N° | Script | Objet |
|---|---|---|
| J1 | `j_modele.py`, `j1_valid.py` | maquette détendue et jacobien ; validations |
| J2 | `j2_calib.py` | calibration |
| J3 | `j3_grille.py` | vitesses une à une, toutes ensemble, grille factorielle 3^6 |
| J4 | `j4_mecanisme.py` | mécanisme et frontières de (a) |
| J5 | `j5_transfert.py` | part du transfert ; exemples datés |
| J6 | `j6_surcommande.py`, `j7_attrib.py`, `j8_compl.py` | sur-commande ; attribution |
| K | `k_niveaux.py`, `k2_compare.py`, `k3_diag.py`, `k5.py` | contre-épreuve en niveaux |

**Validations (J1).** Réduite, la maquette reproduit :
- **fiche 2** : 0,9452 et 72,9 tours (g = 2 %, m = 0,6) ; 0,9459 et 73,0 tours (g = 0) ;
- **fiche 4**, § 3.N-9 (e), M + SN, emploi R : 0,8969 / 0,9068 / 0,9225 / 0,9385 ;
- **fiche 5**, B1 : 0,9838 et 0,9859 (θ_H = 0,8, i_D = 0 et 3 %) ; 0,9965 et 0,9993 (θ_H = 1) ;
- **pas sans choc** : écart au sentier de 1,1e−16 au plus.

**Contre-épreuve indépendante (K).** Une seconde maquette est écrite en niveaux, sans détendance et sans importer la première. pr y croît à g_pr, N^pa à g_N = 0,5 %, et les prix sont en u.m.
- **Sentier sans choc** : tenu à 1,8e−11 pour la production et 2,9e−11 pour le prix, sur 600 tours.
- **Racine dominante, 16 cas du tableau 1.** Elle est estimée sur la simulation : ajustement AR(2) si la racine est complexe, rapport sur 40 tours si elle est réelle.
  - Elle égale celle du jacobien au 4e chiffre, période comprise.
  - Exception : θ_H = 1, (c), régime B. La racine réelle dominante (0,9537) y est à peine excitée par une impulsion de transfert ; la trajectoire décroît plus vite qu'elle.
- **Trajectoires** : la simulation en niveaux, la simulation détendue non linéaire et la propagation linéaire J^t coïncident à 4 chiffres jusqu'au tour 200.

**Corrections en cours de calcul** (déclarées ; aucun chiffre publié n'en provient) :
1. **Régime B forcé.** La première version gardait y = min(y*, N), ce qui crée un second coude à l'état stationnaire. Or N ≥ N* sous T4-C donne y = y*. Le rayon du régime B en était faussé : 0,9663 au lieu de 0,9613 sous (c).
2. **Estimateur.** L'AR(2) ne sépare pas deux racines réelles voisines (0,9637 et 0,9366) : il donnait 0,9856. Il est remplacé, pour les racines réelles, par le rapport sur 40 tours.

**Racine unitaire.** Le niveau nominal porte une racine unitaire, attendue et déclarée (fiche 4, § 3.N-9).
- |λ − 1| ≤ 1,7e−9.
- Les composantes réelles du vecteur propre valent au plus 8,3e−9 de sa norme.
- Elle est exclue du rayon.

**1. Calibration (J2).** Chaque case donne le rayon hors racine nominale, puis la demi-vie en tours (racine réelle) ou la période en tours (paire complexe).

| | (c) régime H | (c) régime B | (a) régime H | (a) régime B |
|---|---|---|---|---|
| θ_H = 0,8 ; i_D = 0 | 0,9642 ; 19,0 | 0,9619 ; 17,8 | **1,0253** ; période 17,4 | **1,0007** ; période 19,4 |
| θ_H = 0,8 ; i_D = 3 % | 0,9637 ; 18,8 | 0,9613 ; 17,6 | **1,0275** ; période 17,3 | **1,0029** ; période 19,3 |
| θ_H = 1 ; i_D = 0 | 0,9566 ; 15,6 | 0,9539 ; 14,7 | **1,0537** ; période 17,2 | **1,0556** ; période 19,2 |
| θ_H = 1 ; i_D = 3 % | 0,9565 ; 15,6 | 0,9537 ; 14,6 | **1,0561** ; période 17,1 | **1,0580** ; période 19,1 |

- **À π̄ = 10 %** (θ_H = 0,8, i_D = 3 %) : (c) 0,9636 / 0,9609 ; (a) 1,0271 / 1,0027.
- **Règle T4-C réelle** (alternance des régimes ; impulsion de 1e−8) :
  - sous (a), l'enveloppe croît de **1,0171 par tour** à θ_H = 0,8 (doublement en 41 tours) et de 1,0385 à θ_H = 1 ;
  - sous (c), elle converge.

**2. Vitesses ×0,5 et ×2 (J3)**, θ_H = 0,8, i_D = 3 %. Toutes les vitesses ensemble :

| | (c) H | (c) B | (a) H | (a) B |
|---|---|---|---|---|
| ×0,5 | 0,9880, réelle, demi-vie 57,5 | 0,9875, réelle, demi-vie 55,0 | 0,9950, période 23,7, demi-vie 137,5 | 0,9917, réelle, demi-vie 83,4 |
| ×2 | 0,9189, réelle, demi-vie 8,2 | 0,9169, réelle, demi-vie 8,0 | **1,0550**, période 8,0 | **1,0187**, période 8,4 |

Une vitesse à la fois :
- **Sous (c)** : de 0,9404 (λ_IN ×2, B) à 0,9796 (λ_IN ×0,5, H). La racine dominante est réelle, sauf des paires de 337 à 2 844 tours (λ_v ×2, λ_IN ×2, λ_V ×0,5).
- **Sous (a)** :
  - toutes les variations du régime H sont explosives, de 1,0004 (λ_w ×0,5) à 1,0564 (λ_w ×2) ;
  - en régime B, seules λ_v ×2, λ_N ×0,5, λ_w ×0,5, λ_μ ×2 et λ_V ×2 sont stables.

Grille factorielle 3^6 (729 combinaisons par cas) : plage du rayon, puis nombre de combinaisons instables.

| Cas | (c) H | (c) B | (a) H | (a) B |
|---|---|---|---|---|
| θ_H = 0,8 ; i_D = 0 | 0,9035 à 0,9902 ; 0 | 0,8814 à 0,9902 ; 0 | 0,9678 à 1,0764 ; 492 | 0,9633 à 1,0746 ; 317 |
| θ_H = 0,8 ; i_D = 3 % | 0,9017 à 0,9903 ; 0 | 0,8805 à 0,9903 ; 0 | 0,9693 à 1,0791 ; 513 | 0,9647 à 1,0776 ; 325 |
| θ_H = 1 ; i_D = 0 | 0,8974 à 0,9840 ; 0 | 0,8685 à 1,0034 ; 3 | 0,9665 à 1,1165 ; 639 | 0,9594 à 1,1558 ; 613 |
| θ_H = 1 ; i_D = 3 % | 0,8976 à 0,9840 ; 0 | 0,8684 à 1,0111 ; 10 | 0,9683 à 1,1197 ; 645 | 0,9611 à 1,1600 ; 617 |

- **Sous (c), θ_H = 0,8** : paires complexes dominantes de 81 à 11 458 tours. Quelques-unes tombent dans la bande de 36 à 96 tours (régime B), qui n'est pas exigée.
- **Sous (c), θ_H = 1, régime B** :
  - les 3 et 10 combinaisons instables (au plus 1,0111, période 28,4) ont toutes λ_N ×0,5, λ_w ×2 et λ_μ ×0,5 ;
  - le régime B n'est jamais permanent. Dans le pire cas, la règle réelle converge : impulsions ±1e−4, |y| passe de 1,4e−4 à 2,7e−14 en 1 200 tours.
- **Sous (a)** : périodes de 8,0 à 27,9 tours.

**3. Mécanisme de l'instabilité sous (a) (J4)**

Sous (a), le terme d'entretien γ^e·V lit l'inflation mesurée :
- ∂C^plan/∂π_{t−1} = −Γ^e(n_aν − α_Y)·YD_{t−1}/[n_a(1 + π_{t−1})] ;
- soit environ −0,93·YD à l'état stationnaire : **un point de glissement retire environ 0,93 % du revenu mensuel au plan**.

La boucle est la suivante : glissement en hausse, plan en baisse, puis stocks, production, emploi, chômage en hausse, salaire SN et ξ en baisse, prix en baisse, et le glissement baisse de 1 à 13 tours plus tard. C'est une rétroaction négative, retardée par la fenêtre du glissement et de fort gain : elle donne une oscillation croissante de 17 à 19 tours.

Mesures :
- **Canal porteur : salaire → coût → prix.**
  - Salaires figés : stable (0,9921 / 0,9926).
  - ψ_ξ = 0 : encore explosive (1,0210 / 1,0126).
  - Prix et salaires figés : 0,9859. π est alors constant, et (a) coïncide avec (c).
- **Frontières**, régime H :
  - ν < 0,586 (λ_V = 0,4) ;
  - correction partielle π^lu = h·π_{t−1} + (1 − h)π̄ : h < 0,604. En régime B, h < 0,949.
- **Autres mesures de l'inflation** : la variation sur un tour annualisée donne 1,0387 (période 6,7), la variation sur 3 tours 1,0781 (période 9,0). Aucune ne stabilise.
- **n_a = 4** : (a) 1,0415 / 1,0349 ; (c) 0,8853 / 0,8836. Ce n'est donc pas un artefact du pas mensuel.
  *Annotation du 04/10/2026 (validation de la spécification par `macro`, remesure ; décision inchangée) : le passage de `docwriter` (03/10/2026) a remesuré la lecture (a) à n_a = 4 à 1,09 (régime H), contre 1,0415 ici ; explosive dans les deux cas, le verdict est inchangé. Les deux maquettes ne sont pas départagées (maquette conjointe non reconstruite par `macro`) ; un cas n_a = 4 de la lecture (a) est à mesurer sur le moteur au J3 (#60). Le corps de la spécification ne cite aucun des deux chiffres ; son historique des versions les cite tous deux.*
- **Statut.** Aucune instabilité de `tab:instabilites` ne correspond : c'est un mécanisme nouveau, mesuré en maquette. Godley et Lavoie corrigent le revenu de la perte d'inflation sur la richesse (DISINF, reproduction sfcr, § 3.0). La stabilité de cette correction dans leurs modèles n'est pas vérifiée ici.

**4. Part d'un transfert dépensée (critère 12 (d) ; J5)**

Transfert de +1 % du YD stationnaire aux tours 1 à 12.
- Part = Σ(C_t − C̄)/ΣTr_t, en u.m. détendues.
- En volume : Σ(C_t/p_t − C̄/p̄)/ΣTr_t, transferts au prix de référence.

| Maquette | 12 tours | 24 tours | 120 tours |
|---|---|---|---|
| Bloc 5 seul (revenus hors intérêts exogènes) | 0,627 | 0,780 | 0,981 |
| B1 (figés, emploi R ; θ_H = 0,8 ; i_D = 3 %) | 1,002 | 1,969 | 4,081 |
| Conjointe (c), θ_H = 0,8 : u.m. / volume | 1,046 / **0,578** | 2,295 / 0,464 | 10,591 / 0,484 |
| Conjointe (c), θ_H = 1 : u.m. / volume | 1,378 / 0,695 | 3,066 / 0,311 | 10,573 / 0,116 |
| Conjointe (a), θ_H = 0,8 : u.m. / volume (non stationnaire) | 0,684 / 0,294 | 1,240 / 0,304 | — |

- **Part propre au ménage** : 0,627 en 12 tours, la même dans toutes les maquettes sous (c), puisque la règle C ne lit aucun prix.
- **En u.m., la boucle dépasse 1.** Deux causes :
  - les revenus induits ;
  - une hausse durable du niveau des prix (+1,21 % au tour 24, +1,07 % au tour 120), qui relève de la racine nominale.
- **En volume**, la hausse des prix rogne le transfert et la richesse : 0,578 en 12 tours.
- **Mesure à retenir pour le seuil de `jeu`** : je propose la part en volume dans la boucle pour la restitution, et la part propre au ménage pour la documentation. Le choix revient à `jeu`, puis au mainteneur.

**Exemples datés en boucle conjointe.** Cas θ_H = 0,8, i_D = 3 %, lecture (c), emploi C. Les colonnes donnent l'écart au sentier du plan, du YD et du prix ; le taux d'épargne 1 − C/YD ; le ratio V d'ouverture/(12·YD du tour), qui vaut ν à l'état stationnaire ; la richesse V/V̄.

| Tour | (i) G +1 %, tours 1 à 12 : plan / YD / taux d'épargne / ratio / V/V̄ / prix | (ii) transferts +1 % du YD, tours 1 à 12 : plan / YD / taux d'épargne / ratio / V/V̄ / prix |
|---|---|---|
| 1 | 0 / 0 / 0,03967 / 1,00000 / 1,00000 / 0 | 0 / +1,000 % / 0,04918 / 0,99010 / 1,00000 / 0 |
| 2 | 0 / +0,081 % / 0,04045 / 0,99919 / 1,00000 / +0,010 % | +0,656 % / +1,002 % / 0,04297 / 0,99090 / 1,00083 / 0 |
| 3 | +0,053 % / +0,148 % / 0,04058 / 0,99859 / 1,00007 / +0,038 % | +0,669 % / +1,215 % / 0,04485 / 0,98912 / 1,00114 / +0,025 % |
| 4 | +0,098 % / +0,214 % / 0,04078 / 0,99801 / 1,00015 / +0,078 % | +0,819 % / +1,393 % / 0,04511 / 0,98785 / 1,00161 / +0,099 % |
| 9 | +0,290 % / +0,460 % / 0,04129 / 0,99618 / 1,00076 / +0,344 % | +1,439 % / +2,160 % / 0,04644 / 0,98321 / 1,00444 / +0,792 % |
| 13 | +0,403 % / +0,589 % / 0,04145 / 0,99552 / 1,00138 / +0,511 % | +1,825 % / +1,593 % / 0,03748 / 0,99126 / 1,00705 / +1,325 % |
| 14 | +0,426 % / +0,589 % / 0,04123 / 0,99568 / 1,00154 / +0,532 % | +1,254 % / +1,679 % / 0,04368 / 0,99027 / 1,00690 / +1,433 % |
| 18 | +0,400 % / +0,488 % / 0,04051 / 0,99715 / 1,00202 / +0,506 % | +1,322 % / +1,565 % / 0,04197 / 0,99261 / 1,00815 / +1,538 % |
| 24 | +0,307 % / +0,339 % / 0,03997 / 0,99894 / 1,00233 / +0,348 % | +1,111 % / +1,185 % / 0,04038 / 0,99721 / 1,00902 / +1,208 % |

**Délais**
- Consommation : inchangés. Dépense publique au tour n, consommation au tour n + 2 ; transferts au tour n, consommation au tour n + 1.
  *Annotation du 04/10/2026 (revue finale de `macro`, mesure ; décision inchangée) : depuis M28 (règle F), une dépense publique du tour n relève le dividende du tour n (ligne 14, environ +0,498 par u.m. de G, les dépôts visés absorbant le reste), compté par H7 dans le revenu du tour n : le budget des ménages bouge **dès le tour n + 1** (+0,315 par u.m. de G), puis au tour n + 2 par l'emploi. Le critère J3 « Délais » est corrigé de façon prospective dans la spécification (décision du mainteneur du 04/10/2026, aucun essai fait).*
- Prix, ajout de la boucle :
  - dépense publique au tour n, prix au tour n + 1 (par ξ) ;
  - transferts au tour n, prix au tour n + 2.

**5. Sur-commande (critères 8 (c) et 11 (c) ; J6)**

Plan public doublé (0,2 de la demande) aux tours 1 à 12 ; borne N ≤ N^pa.

| | B1/B2 (figés, emploi R) | Conjointe (c), θ_H = 0,8 | Conjointe (c), θ_H = 1 | Conjointe (a), θ_H = 0,8 |
|---|---|---|---|---|
| Taux de service, tours 9 à 12 | 0,869 / 0,856 / 0,853 / 0,850 | 1 | 1 | 1 |
| Demande non servie des ménages | tours 9 à 12 | aucune | aucune | aucune |
| Dernier tour à N = N^pa (seuil : tour 24) | 134 | **14** | **15** | 720, fin de la simulation |
| Richesse à l'ouverture du tour 13 | +6,33 % | +5,06 % | +13,20 % | +15,66 % |
| Prix maximal | 0 | +55,6 % (tour 16) | +87,4 % (tour 18) | oscillation (+48,2 % au tour 106) |
| Production minimale | — | −16,65 % (tour 21) | −22,14 % (tour 25) | −24,7 % au tour 240 |
| Chômage maximal | — | +13,99 points (tour 24) | +18,93 points (tour 27) | — |
| Ratio V d'ouverture/(12·YD du tour) hors de ±2 % | tours 2 à 10 | 87 tours (2 à 89), dont 11 pendant le choc | 48 tours (1 à 52) | 651 tours après le tour 12 |

**Attribution (J7)**
- Avec la règle fixe de la fiche 4 (plans indexés) : prix +235 % au tour 56, aucune récession, N = N^pa jusqu'au tour 32.
- La richesse nominale de la règle C ramène donc les prix, par un effet d'encaisses réelles, mais elle produit la récession.
- Avec ψ_ξ = 0 : prix +33,3 %, production au plus bas à −2,9 %, N = N^pa jusqu'au tour 30. **Le seuil de 12 tours est alors dépassé** : le verdict 8 (c) dépend de ψ_ξ, qui n'a pas de source (fiche 4, réserve 4).

**Chocs plus petits** (c) :

| Choc sur la demande | Prix maximal | Production minimale | Tours à N^pa |
|---|---|---|---|
| +0,2 % (G +1 %) | +0,54 % | −0,12 % | 0 |
| +1 % | +2,73 % | −0,59 % | 0 |
| +5 % | +13,99 % | −2,86 % | 5 |

**6. Ce qui change par rapport aux prix figés (§ 3.C-4 et § 3.L)**
1. **Sous (c), la boucle est plus amortie** : 0,9637 contre 0,9859 (θ_H = 0,8, i_D = 3 %), soit une demi-vie de 18,8 tours contre 49,0. Les prix déprécient la richesse nominale non indexée, et le ménage la reconstitue.
2. **La racine quasi unitaire de θ_H = 1 disparaît** : 0,9565 contre 0,9993.
   - SN fixe U* = U^eq, et l'indétermination passe au niveau nominal (racine déclarée).
   - La réserve 5 est levée pour la dynamique réelle dans la maquette.
   - Elle reste ouverte pour la fermeture du niveau stationnaire (Ā, #44).
3. **Sous (a), la boucle devient explosive.** À prix figés, π est constant et (a) coïncide avec (c) : le défaut était invisible au § 3.C-4.
4. **Le régime de baisse de l'emploi C compte peu** sous (c) : 0,9613 contre 0,9637.
5. **Part du transfert en 12 tours** : 1,002 (B1) contre 1,046 en u.m. et 0,578 en volume.
6. **Sur-commande** :
   - la borne cesse au tour 14 au lieu du tour 134 ;
   - le prix rationne à la place du stock ;
   - en contrepartie, une embardée prix-récession.
7. **Délais** : inchangés pour la consommation ; les prix réagissent aux tours n + 1 et n + 2.

**7. Verdict sur le critère 5 (c) complet**
- **Exigence** (rayon < 1 à la calibration) :
  - **tenue sous (c)**, donc sous (b) avec π^e = π̄ : 0,9637 et 0,9613 ; la règle réelle converge ;
  - **échec sous (a)** : 1,0275 et 1,0029 ; la règle réelle diverge, à 1,0171 par tour.
- **Mesure** (×0,5 et ×2) : publiée ci-dessus.
- **Conséquence.** Je retire la recommandation (a) de la Q10 et je recommande (c), sous l'avis de `monnaie`.
- **Coût de (c)** : elle n'est exacte que si π̄ = π* (C2).
  - Hors cible, le ratio dévie et dépend de λ_V : le critère 4 échoue hors cible.
  - Exemple, π stationnaire de 3 % pour une cible de 2 % : −2,27 % à λ_V = 0,4 ; −4,36 % à ×0,5 ; −1,19 % à ×2.
  - Forme exacte : V/(n_a·YD) = [1 − (Γ^e/Γ)(1 − νλ_V)]/[n_a(γ − γ^e) + λ_V], contrôlée par simulation (V/(n_a·YD) = ν·Γ à la clôture).
  - La formule du tableau du § 3.N-3, (γ^e + λ_V/n_a)/(γ + λ_V/n_a), est approchée : elle omet Γ^e/Γ dans YD^e. Elle donne −2,18 % au lieu de −2,27 % dans le même cas.
- **Variante non recommandée sans `monnaie`** : π^lu = h·π_{t−1} + (1 − h)π̄.
  - Stable pour h < 0,604 ; exacte sur la trajectoire de référence.
  - Écart hors cible environ multiplié par (1 − h) : −1,15 % à h = 0,5.
  - Un paramètre de plus, sans source.
- **(b) avec une loi adaptative de π^e** : non mesurée. La fiche 8 vérifiera 5 (c) avec sa loi.

**8. Cible de richesse sur le revenu de Haig-Simons** (question de `monnaie`, § 6, Q2, point 3)

*Additif de `macro`, 03/10/2026, versé par la session principale après contre-épreuve indépendante (maquette écrite à partir des textes, sans les scripts de `macro` : elle reproduit d'abord la boucle propre du § 3.C, point 3, et les 16 cases du tableau 1 sous cible nominale ; tous les chiffres ci-dessous concordent au 4e chiffre, ceux de l'état stationnaire et de la boucle propre au 6e). Les simulations non linéaires de la règle T4-C réelle (enveloppes 0,9799 et 1,0218 par tour) et les sensibilités −0,93·YD et +0,39·YD ne sont pas contre-éprouvées.*

- **Écriture** : V*_t = ν·n_a·(YD^e_t − π_s·V_{H,t}), V_{H,t} d'ouverture.
- **État stationnaire** : V/(n_a·YD) = ν/(1 + ν·n_a·π_s), soit 0,98057 à π̄ = 2 % et 0,91267 à π̄ = 10 %. V/(n_a·YD^HS) = ν exactement, YD^HS = YD − π_s·V.
- **Superneutralité** (r = 1 %, i_D = r + π̄ ; Y_o = YD − i_D·V/n_a, revenu hors intérêts) : V/(n_a·Y_o) vaut 1,010286 à π̄ = 2 % et 1,014518 à π̄ = 10 %, contre 1,030928 et 1,123596 sous la cible nominale. Le résidu tient à #49.
- **Boucle propre** : 0,96612 / 0,96706 (i_D = 0 et 3 %, π̄ = 2 %) ; 0,96727 (i_D = 11 %, π̄ = 10 %).
- **Boucle conjointe**, i_D = 3 %, régimes H / B :

  | γ^e | π_s | θ_H = 0,8 | θ_H = 1 |
  |---|---|---|---|
  | (c) | π̄ | 0,9640 / 0,9617 | 0,9564 / 0,9537 |
  | (c) | π_{t−1} | 0,9823 / 0,9748 (périodes 48,6 / 56,0 tours) | **1,0223 / 1,0218** (56,5 / 59,5 tours) |
  | (a) | π_{t−1} | 0,9967 / 0,9742 | **1,0231 / 1,0271** |

- **Mécanisme** : le terme de cible lu sur l'inflation mesurée agit en sens inverse du terme d'entretien (environ +0,39·YD contre −0,93·YD par unité de π annuel, mesure de `macro`). Il crée une rétroaction positive lente, de 49 à 60 tours, explosive à elle seule à θ_H = 1.
- **Recommandation de `macro`** : cible de Haig-Simons, avec π_s = (1 + π̄)^{1/n_a} − 1, lu comme γ^e. Restituer le ratio sur YD^HS (niveau normal ν), avec le ratio nominal à côté.
- **Position de `monnaie`** (§ 6.1, Q2, point 3) : π_s = (1 + π_{t−1})^{1/n_a} − 1, superneutralité exacte quelle que soit l'inflation stationnaire. Reconsultée sur le cas θ_H = 1 (additif au § 6).

### 3.R Option R — référence « sans retard »

Deux sens sont instruits :
- **(R1) Sans retard d'ajustement** (λ_V = n_a) : α_Y = 1 − 12ν < 0. Inadmissible : une hausse de revenu ferait baisser la consommation. Ce cas montre que la condition de domaine νλ_V < 1 est contraignante.
- **(R2) Sans retard de revenu** : le plan lit WB_t, ce qui le déplace en phase 5, avant le bloc 2. Cela modifie `tab:phases` et l'ordre de la phase 5 de M24 (décision citant M22 et M24). Le multiplicateur devient contemporain. **Non mesuré.** Il n'est retenu que comme référence.

### 3.D Variante à deux types (Q6)

- Une part χ du revenu va aux contraints (C¹ = YD^{1,e}) ; la richesse est tenue par l'autre type, selon la règle C avec ν₂.
- **Au niveau agrégé, l'équation est identique à C avec ν = (1 − χ)ν₂**, et α_Y = 1 − νλ_V ne dépend pas de χ (démonstration algébrique : la somme des deux règles redonne C).
- Sans levier ciblé, χ n'est pas identifiable au socle. Il ne devient distinct qu'avec un transfert ciblé (Q11, J4), dont la propension vaut 1 pour les contraints.
- Ordre de grandeur sourcé : environ un tiers des ménages, environ 20 % du revenu (KVW, p. 3 et 23).
- Des comptes séparés (sous-colonnes) toucheraient M22.

### 3.L Restitution et exemples datés (critère 12)

Maquette B1 : prix figés, emploi R, θ_H = 0,8, i_D = 3 %, ν = 1, λ_V = 0,4. Écarts au sentier.
- **Ratio** = V d'ouverture/(12·YD du tour) : c'est la définition du § 3.C, qui vaut ν exactement à l'état stationnaire.
- **V/V̄** : richesse rapportée à son sentier.
- Taux d'épargne stationnaire : 0,03967.

| Tour | (i) G +1 %, tours 1 à 12 : plan / YD / taux d'épargne / ratio / V/V̄ | (ii) transferts +1 % de YD, tours 1 à 12 : plan / YD / taux d'épargne / ratio / V/V̄ |
|---|---|---|
| 1 | 0 / 0 / 0,03967 / 1,00000 / 1,00000 | 0 / +1,000 % / 0,04918 / 0,99010 / 1,00000 |
| 2 | 0 / +0,081 % / 0,04045 / 0,99919 / 1,00000 | +0,656 % / +1,002 % / 0,04297 / 0,99090 / 1,00083 |
| 3 | +0,053 % / +0,138 % / 0,04048 / 0,99869 / 1,00007 | +0,669 % / +1,215 % / 0,04485 / 0,98912 / 1,00114 |
| 4 | +0,091 % / +0,194 % / 0,04066 / 0,99820 / 1,00014 | +0,819 % / +1,368 % / 0,04487 / 0,98809 / 1,00161 |
| 9 | +0,257 % / +0,405 % / 0,04109 / 0,99664 / 1,00068 | +1,360 % / +2,034 % / 0,04602 / 0,98425 / 1,00427 |
| 13 | +0,350 % / +0,509 % / 0,04119 / 0,99614 / 1,00121 | +1,705 % / +1,410 % / 0,03687 / 0,99270 / 1,00669 |
| 14 | +0,369 % / +0,447 % / 0,04042 / 0,99690 / 1,00135 | +1,124 % / +1,483 % / 0,04307 / 0,99177 / 1,00648 |
| 18 | +0,264 % / +0,292 % / 0,03994 / 0,99867 / 1,00158 | +0,992 % / +1,068 % / 0,04040 / 0,99654 / 1,00718 |
| 24 | +0,159 % / +0,137 % / 0,03947 / 1,00024 / 1,00161 | +0,715 % / +0,651 % / 0,03907 / 1,00074 / 1,00726 |

Le ratio baisse au tour du transfert : le revenu du tour monte avant la richesse. Restitué sur 12 tours (V de clôture/somme des 12 derniers YD), il a un niveau normal de 12ν(Γ − 1)/(1 − Γ^{−12}) = 1,0216 an, et vaut 1,0151 au tour 9 et 1,0183 au tour 24 sous (ii). Le choix de la mesure restituée revient à `jeu`.

- C égale le plan : la demande des ménages est entièrement servie.
- Délais : G au tour n, consommation au tour n + 2 ; transferts au tour n, consommation au tour n + 1.
  *Annotation du 04/10/2026 (revue finale de `macro`, mesure ; décision inchangée) : depuis M28 (règle F), une dépense publique du tour n relève le dividende du tour n (ligne 14, environ +0,498 par u.m. de G, les dépôts visés absorbant le reste), compté par H7 dans le revenu du tour n : le budget des ménages bouge **dès le tour n + 1** (+0,315 par u.m. de G), puis au tour n + 2 par l'emploi. Le critère J3 « Délais » est corrigé de façon prospective dans la spécification (décision du mainteneur du 04/10/2026, aucun essai fait).*
- La part d'un transfert dépensée en 12 tours (critère 12 (d)) n'est **pas calculée** : à extraire de la même maquette.

**Sur-commande** (critère 11 ; maquettes B1 et B2 ; G doublé, part de 20 %, tours 1 à 12 ; plafond N^pa) :
- taux de service de 1 jusqu'au tour 8, puis 0,869 / 0,856 / 0,853 / 0,850 aux tours 9 à 12 ;
- **demande non servie des ménages nulle dès le tour 13** : seuil de 12 tours tenu ;
- épargne forcée : richesse +6,33 % au tour 13, soit 0,79 mois de consommation ;
- Ratio de richesse V d'ouverture/(12·YD du tour) : **0,9514 au tour 2, hors de la bande de ±2 % aux tours 2 à 10**. Le revenu du tour bondit avec la production au plafond, et la richesse suit avec un tour de retard. Il vaut 1,0099 au tour 13, puis reste dans la bande. Dans la lecture « V de clôture/somme des 12 derniers YD », rapportée à son niveau normal de 1,0216 an, l'écart reste dans ±2 % à tous les tours (0,9832 au tour 8, 1,0153 au tour 12).
- **en revanche, la production reste au plafond N^pa (+5,26 %) au moins jusqu'au tour 120.** Elle est revenue à +0,77 % au tour 240 et à +0,03 % au tour 480. Sans rappel des prix ni de la politique, la borne d'emploi reste active plus de 100 tours après le choc : le critère 8 (c) n'est pas évaluable dans cette maquette. C'est le même constat que la maquette C8 de la fiche 3.

### Statut des faits de la première tentative (critère 17)

| Fait | Statut |
|---|---|
| G1 : 0 et 145 semaines de contrainte des ménages | S+O |
| Acquis « propension ≠ dépense », « à l'envers », « préparation décisive » | R |
| Hypothèse réfutée 3 | R |
| Instabilités 6, 8 et 15 | R |
| Lignes de la v2.0 et branche active | L, vérifiées le 03/10/2026 ; coefficients de D1 non établis |
| Chiffres de la v1.5 (l. 2065, 2073) | rapportés, invérifiables |

**Remesure proposée, non lancée : V5-1** (`outils/remesurer_v2_menages.py`, `coder` puis `audit`, processus séparé, profil par défaut, non D1). Critères écrits avant l'essai :
- *Branches* : `household_mode='income'` ; `cV` ×0,5 et ×2 ; graine 0 ; 60 ans.
- *Grandeur* : par groupe h, V_h/(52·Yd_h hebdomadaire moyen de l'année), moyenne des années 31 à 60.
- *(i)* Groupe B : écart relatif de la grandeur à (1 − c/Γ_s)/(n_s·γ_s) au plus de 10 %, Γ_s étant la croissance nominale hebdomadaire mesurée.
- *(ii)* Groupes M et H : écart relatif entre ×0,5 et ×2 supérieur à 1e−6 (dépendance à la vitesse).
- *(iii)* Nombre de semaines où le plafond de 0,9 × encaisse est actif, publié.
- Verdicts publiés quel que soit le résultat. **Ils ne changent pas la recommandation.**

## 4. Tableau comparatif

| Critère | A (v1.5) | B (v2.0) | S (SIM/PC) | C (cible avec tendance) | R | D (deux types) |
|---|---|---|---|---|---|---|
| 1 Matrices | strates : sous-colonnes, M22 (3.A-7) | 11a, 19a ; actions hors socle (3.B-7) | ligne 1 (3.N-7) | ligne 1 ; cas à 90 % bouclé (3.N-7) | idem C | idem C (comptes séparés = M22) |
| 2 Phases | non écrites | revenu de la semaine même | triangulaire (3.N-5) | triangulaire ; délai impôts → C : 1 tour (3.N-2) | R2 révise M24 et M22 | idem C |
| 3 Forme fermée | non calculable (3.A-3) | groupes : formule ; B_H/V_H non (3.B-3) | oui, dépend de α_2 (3.S-2) | **ν exact** (F2) | R1 hors domaine | idem C, ν = (1 − χ)ν₂ |
| 3 (b) n_a | — | 1,49 / 1,34 / 1,28 (B) | 0,9229 / 0,9143 / 0,9109 | ν exact ; taux d'épargne par n_aγ (ADR 0008, I.6) | — | idem C |
| 3 (d) π̄ | — | 1,34 → 0,51 (B) | 0,914 → 0,787 | ν inchangé ; épargne 3,97 % → 11,57 % (HS : 2,03 % → 2,21 %) | — | idem C |
| 3 (e) Bouclage | — | — | ratio de V/YD | ν·n_a·YD = (L − D_F) + (B − M^G) − E_Bk − E_CB ; fermeture à #44 | — | idem C |
| 4 Vitesses | **échec** (Euler sans ancre) | **échec** (cV niveau et vitesse) | **échec** | **tenu** (F2) | — | tenu |
| 5 (a) | substitution réfutée (3) | 8, 15, état caché | rien de réintroduit | rien de réintroduit | — | idem C |
| 5 (b) | non calculé | non calculé | non calculé | 0,9668 (λ_V ×0,5 / ×2 : 0,9834 / 0,9336) | — | idem C |
| 5 (c) | — | — | non calculé | 0,9761 à 0,9903 (θ_H = 0,8) ; 0,9993 (θ_H = 1) ; bande sans objet (racine réelle) | non mesuré | idem C |
| 5 (d) | Euler (IS) | rentier, aucune élasticité identifiée | rentier + | **rentier +** (3.N-9) | — | idem C |
| 6 m_H | — | — | α_1·θ_H | 0,48 / 0,77 à 0,79 (θ_H = 0,8) ; 0,60 / 0,96 à 0,99 (θ_H = 1) | — | idem C |
| 7 Test zéro | — | — | — | préalable tenu ; mesure au J3 | — | — |
| 8 Bornes | clip de cov, parts [0, 1], subsistance | 0,9 × encaisse, max(0) | conservation + lecture (a) ou (b) (3.N-6) | idem S | — | idem |
| 9 Titres | Tobin borné | flux sB, sans stock | B_H ≡ 0 recommandé (3.N-4) | idem | — | idem |
| 10 Lectures | `eq:yd` (crédit hors socle) | — | symbolique (3.N-1) | idem | — | idem |
| 11 Sur-commande | — | — | — | non servie nulle dès le tour 13 ; production au plafond plus de 100 tours (sans prix ni politique) | — | — |
| 12 Lisibilité | strates lisibles | groupes | — | exemples du § 3.L ; restitution HS proposée | — | ciblage au J4 |
| 13 Empreinte | environ 6 états, environ 15 paramètres (2 sans valeur) | états cachés, drapeaux | 1 état, 2 paramètres | 1 état, 2 paramètres | — | 1 état, 3 paramètres |
| 14 Coût | non mesuré | **itératif : échec** | négligeable (décompte) | négligeable, non mesuré | — | idem |
| 15 Notation | β double, collision κ_E | — | α : 1 occurrence (`sec:ecartees`) | ν, λ_V, θ_H libres | — | χ libre |
| 16 Faits | — | — | — | MPC : JP 2010, PSJM 2013 ; effet richesse : COS 2006 ; λ_V sur richesse liquide **non sourcé** | — | KVW 2014 |
| 17 Statuts | rapportés | L ; D1 non établi ; V5-1 proposée | — | — | — | — |

## 5. Avis de l'expert pilote

*`macro`, 03/10/2026 ; mis à jour le 03/10/2026 après l'additif de `monnaie` (§ 6.5).*

**Recommandation : option C** (cible de richesse avec terme de tendance), ménage représentatif, avec les choix suivants :
- revenu lu : YD_{t−1} avec tendance (Q2 (i)) ;
- **inflation lue (Q10) : lecture (c), cible déclarée π\*** (paramètre ou levier de la fiche 8), jamais π̄ (résultat) ; γ^e = [(1 + g)(1 + π\*)]^{1/n_a} − 1 ;
- **cible de richesse sur le revenu de Haig-Simons** : V\* = ν·n_a·(YD^e − π_s·V_H), avec π_s = (1 + π\*)^{1/n_a} − 1, une seule lecture de l'inflation pour γ^e et π_s ;
- le bloc 5 ne lit plus le registre de l'ADR 0008 (§ 3.N-5 et § 3.C, point 9, à reprendre) ;
- taux d'épargne restitué nominal et corrigé (Q3), sous deux libellés distincts (§ 6.5) ;
- **B_H ≡ 0** au socle (Q4) ;
- plafond du plan à D_{H,t} d'ouverture, lecture (a) du § 3.N-6 ;
- la variante D notée pour le J4 (Q6, Q11).

Calibration indicative : ν = 1 an, λ_V = 0,4 par an (α_Y = 0,6).

**Motifs** :
- seule option qui tient le critère 4 sous C2 (ν exact sur YD^HS) ;
- forme fermée ;
- aucune borne à seuil libre hors 3.N-6 (a) ;
- deux paramètres et une variable d'état ;
- boucle conjointe stable à la calibration (0,9640 / 0,9617), là où (a) est explosive (1,0275 / 1,0029) ;
- superneutralité sous C2 : V/(n_a·Y_o) = 1,010286 à 2 % et 1,014518 à 10 % (résidu : #49) ;
- D est équivalente au niveau agrégé sans levier ciblé (principe de simplicité).

**Écartées** :
- A : critère 4 et strates qui touchent M22 ;
- B : critère 14 pour la branche active, critère 4 pour la règle de revenu, plafond ;
- S, écrite avec α libres : critère 4 ;
- R1 : hors domaine ;
- Q10 (a), glissement mesuré : explosive en boucle conjointe (§ 3.C-10) ;
- π_s sur π_{t−1} : explosive à θ_H = 1 (1,0223 / 1,0218) ;
- variante h : h < 0,604 est une frontière de stabilité, pas une calibration sourcée.

R2 reste la référence non mesurée.

**Réserves**, avec leurs critères écrits avant l'essai (J3) :
1. Un pas sans choc depuis l'état résolu laisse V_H/(n_a·YD^HS) = ν et YD_{t−1} sur leur sentier à 1e−10 près en relatif.
2. Critère 4 : écart au plus de 1e−6 après 720 pas entre λ_V ×0,5 et ×2, **sous C2**. Hors C2, λ_V fixe l'état d'arrivée (continuum déclaré) : à 3 % stationnaire pour π\* = 2 %, V/(n_a·YD) s'écarte de −3,35 % / −1,29 % / −0,22 % pour λ_V = 0,2 / 0,4 / 0,8 ; à 10 %, de −19,76 % / −8,58 % / −1,56 %. C2 (intégrale, sans fuite) est donc aussi une condition de la fiche 5.
3. **Boucle conjointe SN, C, M et ménages (critère 5 (c) complet)**, mesurée au § 3.C-10 :
   - lecture (c), cible de Haig-Simons, π_s sur π\* : 0,9640 / 0,9617 (θ_H = 0,8) ; 0,9564 / 0,9537 (θ_H = 1) ;
   - lecture (c), cible nominale : 0,9637 / 0,9613 ; grille 3^6 de 0,8805 à 0,9903 à θ_H = 0,8 ;
   - au J3 : rayon < 1 à la calibration retenue, régimes H et B, recalculé avec la loi de π^e de la fiche 8 ;
   - condition transmise : la loi de π^e ne réintroduit pas la boucle du § 3.C-10, point 3 (C26).
4. **m_H de long terme supérieur à 0,8 si θ_H = 1** : réserve 3 de la fiche 2, à trancher avec les fiches 6 et 9.
5. **Racine quasi unitaire sans fuite** (θ_H = 1, prix figés : 0,9993) : elle disparaît en boucle conjointe pour la dynamique réelle ; la fermeture du niveau stationnaire reste à faire (fiches 6, 8 et 9, #44), conjointement avec la fiche 6 avant M27-M28.
6. Condition de domaine νλ_V < 1, déclarée et contrôlée au chargement.
7. Calibration de λ_V et de ν sur des sources lues : **à instruire**.
8. Sur-commande en boucle conjointe (c), mesurée sous la cible nominale : borne active jusqu'au tour 14 (seuil tenu) ; prix +55,6 %, chômage +14 points au tour 24, ratio hors bande pendant 87 tours ; avec ψ_ξ = 0, borne jusqu'au tour 30 (seuil non tenu). Non remesuré sous la cible de Haig-Simons.
9. **Effet d'un changement de cible, à déclarer** : une baisse d'un point de π\*, états d'ouverture fixés, relève le plan de +0,55 % au tour même (+0,98 % sous la cible nominale). C'est la contrepartie de la correction de Haig-Simons ; sous (c), il ne passe pas par la crédibilité. L'effet net sur plusieurs tours (baisse de i_D, C20) n'est pas mesuré. Signalé à `jeu` et à la fiche 8.
10. Régimes B, D et E : la π\* lue par les ménages reste à définir (fiche 8, J5).

**Lectures soumises au mainteneur** :
- (a) Q10 : **(c), π\*** (`macro` et `monnaie` d'accord) ; (b) avec la loi de π^e de la fiche 8, seulement par la clause **C26** (C1 tient, boucle complète de rayon < 1 sur la grille, contrôle de séparation), décision citant M27 ; (a) et la variante h retirées ;
- (b) § 3.N-6 : plafond en phase 2 (seuil libre déclaré) ou en phase 5 (révision de M24) ;
- (c) Q4 : B_H ≡ 0 ou demande de Tobin ;
- (d) canal du taux : rentier seul, ou variante PCEX2 α_1(r). Cette dernière demande un fait nouveau contre l'hypothèse réfutée 3 ;
- (e) restitution du taux d'épargne : nominal, corrigé, ou les deux (recommandé : les deux, libellés distincts) ;
- (f) cible de richesse : Haig-Simons avec π_s sur π\* (`macro` et `monnaie` d'accord) ou nominale ; les deux positions antérieures sur π_s sont caduques.

**Coût en fidélité** :
- aucun canal de substitution : le taux agit sur la consommation à l'envers ;
- effet richesse plus fort que celui que mesure la littérature lue (richesse peu liquide) ;
- aucune hétérogénéité au socle ;
- hors cible, la richesse visée ne fuit pas devant l'inflation (pas de dynamique de Cagan ; C18, J6) ;
- la forme C n'est pas écrite telle quelle par Godley et Lavoie : c'est leur α_3 cible, rendue exacte sous croissance et corrigée de Haig-Simons.

## 6. Avis de l'expert consulté

*Rédigé par `monnaie` (expert consulté sur deux frontières : la dette publique, puis l'inflation par décision du mainteneur du 03/10/2026) le 03/10/2026. Avis porté sur la fiche à l'état `d88a47e` (branche `claude/j1-economie-reelle`, PR #43). Il reste cohérent avec mes avis sur les fiches 3 et 4 (`travail.md` § 6, conditions C1 à C8 ; `prix.md` § 6, conditions C9 à C13). Les conditions nouvelles sont numérotées à leur suite (C14 à C25, § 6.3).*

*Sources lues dans le dépôt :*
- *fiche 5, § 1 à 5 ;*
- *fiches 3 et 4, § 6 ;*
- *ADR 0008 (accepté), parties I et II ;*
- *issues #44 et #49 ;*
- *`nations_et_marches.tex` : l. 232 (bilans), l. 254 (titres), l. 294 et 338 à 342 (lignes 19a et 19b), l. 354 à 356 et 407 à 411 (portes de la monnaie), l. 460 (intérêts), l. 477 à 479 (émission, placement raté), l. 510 (`tab:phases`, phase 7), l. 521 et 523 (aucune réévaluation, aucune dette à taux fixe), l. 902 à 905 (dates d'effet des leviers) ;*
- *`archive/faits_mesures_G_K.md`, § 3, 6, 7 et 8.*

*Calculs : cinq scripts du scratchpad (commandes et sorties au Retour). Deux contrôles valident ma maquette contre celle de `macro` : ma boucle propre redonne ses valeurs propres F5 (0,96678 et 0,96772), et mes taux d'épargne corrigés redonnent F3 (2,025 % et 2,209 %).*

*Pour chaque référence, j'indique son statut :*
- *lu : texte primaire ;*
- *extrait : résumé ou notice ;*
- *par reproduction : modèle de Godley et Lavoie relu dans les reproductions sfcr (`gl2-pc.Rmd`, `gl6-dis.Rmd`, `gl7-insout.Rmd`), l'ouvrage n'étant pas lu ;*
- *de mémoire.*

### 6.1 Réponses aux cinq questions de `macro`

**Q1 — Dette publique. Je suis favorable à B_H ≡ 0 au socle**, avec les lignes 11a, 19a-ménages et 19b-ménages maintenues à montant nul (amendement Q4). J'ai cinq motifs et trois conditions.

1. **Les titres du socle sont, en pratique, des bons courts renouvelés à chaque pas.**
   - Ils portent le taux de la dernière date de décision (l. 254 et 460).
   - Aucune dette n'est à taux fixe (l. 523) et aucun actif n'est réévalué (l. 521).
   - Pour un ménage, B_H et D_H ne diffèrent donc que par l'écart i_B − i_D et par la liquidité.
   - Une demande de Tobin n'ajouterait qu'une sensibilité de la composition à cet écart (λ_1 de PC). Elle n'aurait aucun effet de prix ni de durée.
2. **La composition ne change pas la taille agrégée du canal rentier.** Il suffit de consolider la banque et la banque centrale (l. 232).
   - Les créances nettes porteuses d'intérêt du secteur privé sur le secteur public valent NPD = B_H + B_Bk + Res − L^CB = B − M^G − E^CB.
   - Hypothèses : la banque et les entreprises distribuent tout leur résultat dans le pas, et la transmission est complète (i_D = i_B = i_res = i_CB).
   - Sous ces hypothèses, le revenu de capital des ménages vaut i·NPD/n_a, **qu'ils détiennent ou non les titres**. Sous B_H ≡ 0, il leur parvient par i_D·D_H et Div_Bk.
   - C'est le résultat de consolidation d'Auclert (2017), document de travail NBER w23451, **lu**, p. 18 et § 3.4, p. 21 : « the net nominal positions and the unhedged interest rate exposure of the combined household and government sectors are zero […] provided firms are correctly consolidated as part of the household sector ».
   - Contre-épreuve sur le modèle PC, reproduit d'après `gl2-pc.Rmd` l. 67 à 96 (script `m5_pc.py`, **résultat de modèle**). Quand r passe de 2,5 % à 3,5 %, Y\* passe de 106,49 à 110,09. Si tous les titres sont tenus par la banque centrale, dont le résultat revient à l'État, Y\* reste à 100,00.
   - Ce qui porte le canal rentier, ce sont donc les titres détenus **hors de la banque centrale**, non les titres détenus **par les ménages**.
   - B_H ≡ 0 ne supprime aucun canal agrégé. Il en reporte le calendrier sur les règles de la banque (fiche 7 : transmission à i_D, versement de Div_Bk).
3. **Une demande de Tobin exige une clôture de la phase 7** qu'aucune fiche n'a encore instruite :
   - le souscripteur du reliquat ;
   - le signe de ce reliquat ;
   - le rationnement d'une demande supérieure à l'émission ;
   - trois paramètres, λ_0, λ_1 et λ_2.

   Sous une cible ν fixe, le terme λ_2·YD/V est une constante qui ne fait que déplacer λ_0. Le principe de simplicité joue donc contre Tobin au socle.
4. **Le seul effet de jeu qu'apporterait Tobin ne serait pas durable au socle.** Il s'agit de la création de monnaie au sens large par des achats de la banque centrale aux ménages : la ligne 19b-ménages fait varier M, la ligne 19b-banque ne le fait pas (`tab:portes-monnaie`, l. 410 et 411).
   - Hypothèses : demande de Tobin en stock, bons courts, banque souscriptrice du reliquat.
   - Sous ces hypothèses, un achat 19b-ménages ne change ni V ni les taux. Les ménages resouscrivent donc le même encours à la phase 7 suivante, et la souscription de la banque baisse d'autant.
   - L'achat équivaut ainsi, au plus tard un tour après, à un achat à la banque : échange de réserves contre titres, M inchangé.
   - Démonstration algébrique sous ces hypothèses, **non mesurée**.
5. **Sous B_H ≡ 0, M = D_H + D_F suit la richesse nominale.** La demande de monnaie n'a aucune élasticité au taux ; c'est la monnaie endogène pure.
   - Un excès de monnaie qui provient d'une création nette de richesse (déficit) est dépensé à la vitesse λ_V − n_aγ. Un échange d'actifs (achat de titres à la banque) est sans effet.
   - Pour la reconfirmation demandée par C8, j'en tire ceci : une création monétaire durable se traduit par de l'inflation durable **quand elle accroît la richesse nette des ménages au-delà de ν** et que la demande excède la capacité. Ce n'est pas le cas quand elle se réduit à un échange d'actifs.
   - À soumettre au mainteneur.

Les trois conditions de B_H ≡ 0 sont transmises à la fiche 7 (§ 6.3, C19 à C21) :
- la banque devient la seule détentrice privée de la dette ;
- sa souscription (19a-banque) est le **reliquat déclaré de l'équation d'émission** (l. 477) après la souscription décidée de la banque centrale (19a-BC), et jamais un solde du bilan bancaire. C'est le défaut v2.0 des réserves et du refinancement calculés par différence ;
- sa règle de taux des dépôts n'est disciplinée par aucun actif concurrent.

**Second cas, si Tobin était retenu (J6 ou décision contraire) : qui achète quand la demande baisse ?**
- **Ce doit être une souscription primaire négative des ménages (19a-ménages < 0), c'est-à-dire un non-renouvellement à l'échéance**, conforme à la nature de bons courts des titres du socle.
- Sa contrepartie est la hausse de la souscription de la banque (19a-banque) dans la même équation d'émission, dont la somme reste égale au besoin.
- Effets : M monte et H monte par la ligne 19a-ménages négative, H baisse par la ligne 19a-banque. Au net, H est inchangée et M monte : la banque a acheté les titres des ménages contre des dépôts nouveaux.
- **Jamais par la ligne 19b**, pour deux raisons :
  - `tab:phases` (l. 510) la réserve aux « achats décidés de la banque centrale » ;
  - la clôture de PC, `Bcb ~ Bs - Bh` (`gl2-pc.Rmd` l. 80, par reproduction), fait de la banque centrale l'acheteur résiduel dans un modèle **sans banque**. Transposée au socle, elle ferait varier M, H et le bilan de la banque centrale sans décision, ce qui serait une monétisation implicite, illisible et indiscernable d'un assouplissement quantitatif décidé.
- Si la banque atteint une limite de détention déclarée, l'État ne renouvelle pas tout ; c'est le « placement raté » du cadre (M^G < M^G\*, l. 479). Le risque de renouvellement relève de J6.

**Q2 (Q10) — Inflation dans le terme de tendance. Je retiens la lecture (a), le glissement mesuré π_{t−1} lu dans le registre**, converti géométriquement ((1 + π_{t−1})^{1/n_a}, ADR 0008, I.1). Le canal « inflation → épargne d'entretien » est acceptable. J'y ajoute un constat de non-superneutralité de la cible, avec une proposition.

1. **Motifs de (a)** :
   - **Exacte quelle que soit la fiche 8**, donc robuste à un échec de C1. J'avais déjà préféré M à D à la fiche 4 pour cette raison.
   - **Une seule entrée des anticipations, par les salaires** (fiche 4, § 6.2, et C13).
     - Sous (b), π^e entrerait une seconde fois, par la demande.
     - Une annonce crédible de désinflation baisserait alors π^e, donc l'épargne d'entretien, et **relèverait la consommation le tour même**, à contre-courant de la désinflation.
     - Ordre de grandeur, ν = 1 : +0,55 % à +0,97 % du plan par point de baisse de π^e (chiffres de la ligne suivante, transposés).
   - **Même information que le joueur** (C9 ; ADR 0008, II.2) : les ménages lisent le glissement restitué.
   - (c) est à écarter. π̄ n'est pas une variable d'état, mais un résultat stationnaire. Lire π\* ferait d'un changement de cible un choc de demande direct.
2. **Le canal est acceptable**, comme effet d'encaisses réelles en forme stock-flux.
   - Godley et Lavoie écrivent la consommation sur le revenu réel corrigé de la perte d'inflation : `gl6-dis.Rmd` l. 73 à 76 et `gl7-insout.Rmd` l. 270 à 279, par reproduction.
   - Son signe est stabilisant : une inflation plus forte réduit le plan.
   - Mesure (`m5_calc2.py`) : +1 point de π_{t−1}, états d'ouverture fixés, donne −0,97 % du plan sous la cible nominale de `macro` et −0,55 % sous la cible corrigée proposée au point 3.
   - Aucune source empirique n'est lue sur l'effet de l'inflation sur l'épargne mesurée.
3. **Constat : la cible V\* = ν·n_a·YD^e, écrite sur le revenu nominal, n'est pas superneutre dès que i_D suit l'inflation.**
   - Le revenu nominal contient la compensation d'inflation des intérêts. Les ménages visent donc une richesse réelle croissante avec π̄.
   - Mesure (`m5_calc.py` ; forme fermée et simulation égales à 1e−6) : Fisher i_D = r + π, r = 1 %, g = 2 %, ν = 1, λ_V = 0,4, n_a = 12. La richesse en années de revenu hors intérêts, V/(n_a·Y_o), vaut :

     | Cible | π̄ = 2 % | π̄ = 3 % | π̄ = 10 % |
     |---|---|---|---|
     | Nominale (`macro`) | 1,030928 | 1,041667 | **1,123596 (+9,0 %)** |
     | Haig-Simons (proposée) | 1,010286 | 1,010514 | 1,014518 (+0,42 %) |
     | Haig-Simons, Fisher géométrique par pas | 1,010071 | — | 1,010136 (+0,006 %) |

     C/Y_o vaut 0,990030 → 0,993633 sous la cible nominale, et 0,990230 → 0,994251 sous la cible corrigée (Fisher linéaire).
   - Conséquence monétaire.
     - La demande stationnaire d'actifs des ménages dépend de la cible d'inflation. La fermeture du niveau d'activité (#44) et le r̄ résolu (C3) en dépendent donc aussi.
     - Changer de cible achèterait un effet réel permanent : c'est un arbitrage exploitable, de même nature que le constat T2 de la fiche 4.
     - Le contrôle que j'ai demandé à la fiche 4 (§ 6.1, Q6 : « le taux réel stationnaire de la règle doit être indépendant de π̄ ») échouerait.
     - Ce n'est pas un échec d'exigence de la fiche 5 (critère 3 (d), mesure par amendement). C'est une condition de la fiche 8.
   - **Proposition : écrire la cible sur le revenu de Haig-Simons**, avec la même lecture de l'inflation :
     - V\*_t = ν·n_a·(YD^e_t − π^lu_s·V_{H,t}), avec π^lu_s = (1 + π_{t−1})^{1/n_a} − 1 ;
     - le reste de la règle C est inchangé.
   - Coût et propriétés (`m5_calc4.py`, `m5_calc2.py`) :
     - aucun paramètre, aucune variable d'état ; α_Y = 1 − νλ_V et la condition de domaine sont inchangés ;
     - V_H = ν·n_a·YD^HS **exactement**, indépendamment de λ_V (λ_V = 0,2 / 0,4 / 0,8 donnent des ratios identiques à 1e−11). Le critère 4 tient ;
     - le ratio restitué V_H/(n_a·YD) devient ν/(1 + ν·n_a·π_s) : 0,98057 à π̄ = 2 %, 0,91267 à π̄ = 10 %, n_a = 12. Sa dépendance à n_a est déclarée (ADR 0008, I.6) : 0,980535 / 0,980566 / 0,980578 à n_a = 4 / 12 / 52 ;
     - boucle propre : 0,96612 / 0,96706 / 0,96727 (i = 0, 3 %, 11 %), contre 0,96678 / 0,96772 / 0,97045 sous la cible nominale. Elle est plus amortie et moins sensible à π̄. Je n'ai pas recalculé la boucle B1 avec la fiche 2 ;
     - avec des dépôts non rémunérés, la richesse réelle diminue avec l'impôt d'inflation net (semi-élasticité de l'ordre de −ν). C'est le sens de Cagan (1956), cité de mémoire, mais d'une ampleur sans rapport avec une hyperinflation (C18).
   - Le résidu (+0,42 %) est l'écart de #49 entre r = i − π, linéaire moins géométrique, et le rendement réel exact. Il se ferme par la définition de la relation de Fisher retenue à la fiche 8. Une forme exacte existe, avec un revenu corrigé déflaté par (1 + π_s) : C/Y_o = 0,99003630 pour π̄ = 0, 2 et 10 %. Je ne la demande pas au socle.
   - **Deux positions, si `macro` maintient la cible nominale** :
     - *`macro`* (§ 3.N-3 et § 5) : cible sur le revenu nominal, correction de Haig-Simons implicite dans le seul terme de tendance. ν est exact sur le ratio restitué. C'est plus simple à lire, et sans conséquence tant que i_D ne suit pas l'inflation.
     - *`monnaie`* : cible sur le revenu de Haig-Simons. Elle est superneutre à #49 près, conforme à Godley et Lavoie (consommation sur le revenu réel corrigé), de même empreinte. Le ratio restitué vaut ν/(1 + ν·n_a·π_s), et la bande du test zéro se centre sur la valeur résolue (critère 7).

**Q3 — Signe du canal du taux. Je transmets à C10 une structure, non un nombre unique. Je ne demande pas d'instruire PCEX2 maintenant.**

1. **Le +0,6 % de `macro` est un effet partiel.** Ma mesure donne +0,62 % du plan au tour n + 1 par point de i_D, avec ν = 1 et i_D = 3 %, sous la cible nominale (+0,61 % sous la cible corrigée).
   - Cette mesure omet la baisse simultanée de Div_Bk et de Div_F qui finance la hausse des intérêts versés.
   - En équilibre général, avec distribution complète dans le pas (point 2 de la Q1), l'effet passe :
     - à l'impact, à environ α_Y·b par point ;
     - à long terme et à dette donnée, à d ln C/di = b/(1 + i·b).
   - Ici, b = NPD/(n_a·Y_o), soit la dette publique nette détenue hors banque centrale, en années de revenu hors intérêts. On a b = ν − (L − D_F − E^Bk)/(n_a·Y_o), d'où b < ν si les entreprises sont emprunteuses nettes.
   - Illustration (`m5_calc3.py`, b hypothétique) :

     | b | Impact | Long terme |
     |---|---|---|
     | 0,25 | +0,15 % | +0,25 % |
     | 0,5 | +0,30 % | +0,49 % |
     | 1 | +0,60 % | +0,97 % |

   - À l'échelle du ménage, le signe est **positif sur le taux nominal** et **négatif sur l'inflation lue** (Q2) : le bloc 5 répond positivement au taux réel, sans substitution.
2. **À long terme, le canal rentier est un canal budgétaire.** Son signe dépend de la règle de la fiche 9.
   - Sous une règle qui stabilise la dette par l'impôt sur les ménages, la charge d'intérêts reçue est reprise en impôt, et l'effet de long terme est voisin de 0.
   - Auclert (2017), **lu**, p. 17 : « the consequences […] between households and the government depend crucially on the fiscal rule ».
   - Sa vitesse découle de l'absence de dette à taux fixe (l. 523). Une part à taux fixe l'étalerait (C24).
3. **Ce que la littérature établit, et ce qui reste contesté.**
   - *Établi (résultats empiriques, sources lues ou extraites)* : un resserrement monétaire réduit l'activité. Romer et Romer (2003), document de travail NBER w9866, **lu**, PDF p. 6 : « A 100-basis-point shock to the funds rate is associated with a reduction in industrial production of 4.8% after 22 months ». Publication dans l'AER (2004), citée de mémoire.
   - *Contesté* : l'élasticité de substitution intertemporelle.
     - Hall (1988), *JPE* 96(2), 339-357, résumé **extrait** : « no strong evidence that the elasticity of intertemporal substitution is positive ».
     - Havranek (2015), *JEEA* 13(6), 1180-1204, résumé **extrait** : moyenne corrigée nulle sur données macroéconomiques, « around 0.3–0.4 » sur données individuelles pour les détenteurs d'actifs.
     - Auclert (2017) conclut que la redistribution **amplifie** l'effet de la politique monétaire, parce que les perdants d'une baisse de taux ont une propension plus faible (résumé, **lu**). Le socle n'a ni ménage emprunteur ni dette longue : il n'a donc pas ce mécanisme.
   - *Résultat de modèle, non un fait* : l'acquis « la politique monétaire peut agir à l'envers » (R).
4. **PCEX2 et l'hypothèse réfutée 3.**
   - L'hypothèse réfutée porte sur le **niveau** du chômage v2.0 : 9,02 % → 8,88 % pour η de 0 à 2 (faits § 7, R). Elle ne dit rien du **signe** de ∂demande/∂r, qui conditionne la stabilité de C2.
   - Le fait nouveau qui justifierait d'y revenir est donc la mesure de C10 elle-même. J'en propose le critère, à écrire dans la fiche 8 avant l'essai (C14) : la boucle conjointe de C2 a un rayon spectral ≥ 1 à la calibration, ou ∂(demande totale)/∂r ≥ 0. La demande totale comprend :
     - le canal rentier et l'épargne d'entretien des ménages ;
     - l'investissement de la fiche 6 ;
     - la règle budgétaire de la fiche 9.
   - Si le critère est déclenché, je recommande d'instruire dans cet ordre :
     - le coût du capital de la fiche 6, qui est déjà prévu ;
     - la réaction budgétaire à la charge d'intérêts et une part de dette à taux fixe (fiche 9) ;
     - le calendrier de transmission et de distribution de la banque (fiche 7) ;
     - en dernier, une substitution chez les ménages.
   - Si une substitution est retenue, sa transposition propre à l'option C est une **cible de richesse fonction du taux réel**, ν(i_D − π_{t−1}), plutôt que α_1(r).
     - PCEX2 revient d'ailleurs à cela : la cible implicite (1 − α_1)/α_2 croît de ι/α_2 = 10 ans par unité de r (calcul à la main).
     - Le critère 4 tient, puisque ν reste un niveau.
     - La valeur ι = 4 de PCEX2 (`gl2-pc.Rmd` l. 339 à 344, par reproduction) donnerait environ −4 % du revenu par point à l'impact (Δα_1 = −0,04 ; calcul à la main). Elle n'a aucune source de calibration et ne se reprend pas.

**Q4 — Taux de flux. Le classement est confirmé.**
- i_D et i_B s'appliquent à un encours d'ouverture pour produire un flux du pas (l. 328 et 460) : ce sont des taux de flux, convertis linéairement (ADR 0008, I.2). λ_V est une vitesse, linéaire. ν est un niveau. g, π_{t−1} et π_s, y compris dans la correction de Haig-Simons, sont géométriques.
- Deux précisions :
  - **#49 est la seule source de non-superneutralité qui subsiste sous la cible corrigée** : +0,42 % de V/(n_a·Y_o) entre 2 % et 10 % sous Fisher linéaire, +0,006 % sous Fisher géométrique. La tolérance du test de superneutralité se fixe avec #49 (C15) ;
  - restituer un « rendement annuel effectif » des dépôts, (1 + i/12)^12 − 1, soit 3,04 % pour i = 3 %, exigerait l'annualisation géométrique de l'ADR 0008 (I.4) et afficherait deux taux. Je recommande de restituer le taux contractuel i_D et le rendement réel i_D − π, cohérent avec le r = i − π du cadre.

**Q5 — Taux d'épargne corrigé. La restitution convient**, sous quatre précisions.
1. **Définition ex post**, sur une fenêtre de 12 tours :
   - perte d'inflation du tour = V_{H,t}·(P_t/P_{t−1} − 1), calculée depuis le registre et P_t, connue dès la phase 5 ;
   - taux corrigé = 1 − ΣC / Σ(YD − perte).
2. **« Impôt d'inflation » désigne la perte nette (π − i_D)·D_H**, non la perte brute π·D_H, que les intérêts compensent en partie ou en totalité. Je propose trois indicateurs : taux d'épargne nominal, taux d'épargne corrigé, rendement réel des dépôts i_D − π (glissement). Sous B_H ≡ 0, la perte d'inflation sur la richesse est entièrement une perte sur les dépôts.
3. **Valeurs** (`m5_calc3.py`, Fisher, ν = 1, n_a = 12) :

   | Cible | Taux | π̄ = 2 % | π̄ = 10 % |
   |---|---|---|---|
   | Nominale | nominal | 3,967 % | 11,567 % |
   | Nominale | corrigé | 2,025 % | 2,209 % |
   | Haig-Simons | nominal | 3,890 % | 10,557 % |
   | Haig-Simons | corrigé | 1,985 % | 1,998 % |

   Sous la cible corrigée, le taux corrigé ne dépend presque plus de l'inflation et se lit comme l'épargne réelle, environ g·ν.
4. Qui profite de l'impôt d'inflation net : les émetteurs de passifs nominaux, l'État et les entreprises emprunteuses, par l'intermédiaire de la banque. Point signalé à la fiche 9 et à `jeu`.

### 6.2 Avis général, côté monnaie

**Favorable à l'option C**, avec :
- B_H ≡ 0 (Q1) ;
- la lecture (a) du terme de tendance (Q2) ;
- le classement des taux de l'ADR 0008 (Q4) ;
- la double restitution du taux d'épargne (Q5).

Deux précisions conditionnent mon accord :
- **la cible sur le revenu de Haig-Simons** (Q2, point 3) : superneutralité de la règle, au résidu de #49 près ;
- **la structure d'équilibre général du canal rentier** (Q3), transmise à C10 à la place du seul effet partiel.

**Désaccord éventuel avec `macro`** : la seule question est l'assiette de la cible, nominale ou corrigée, décrite en deux positions au point 3 de la Q2. Je n'ai pas consulté `macro` sur ce constat. Il n'y a aucun désaccord sur B_H ≡ 0, sur la lecture (a), sur le classement des taux, ni sur le refus de reprendre PCEX2 sans fait nouveau.

**Risque monétaire principal, à garder visible jusqu'à la fiche 8.** Le bloc 5 répond **positivement** au taux réel. Le contrôle de l'inflation par C2 exige donc que la somme des autres canaux le compense (C14). Sinon, une règle intégrale qui relève le taux quand l'inflation monte entretient l'écart au lieu de le refermer. Ce serait un processus cumulatif à l'envers, contraire à l'intention du mainteneur.

### 6.3 Conditions transmises

**Fiche 8 (banque centrale et anticipations)**, en complément de C1 à C13 :
- **C14 — Condition de signe**, à écrire avant l'essai et à mesurer avec C10 : ∂(demande totale)/∂r < 0 à la calibration et rayon de la boucle C2 < 1. Son déclenchement constitue le fait nouveau qui rouvre la question de la substitution (Q3, point 4, ordre de recours).
- **C15 — Superneutralité.** Le r̄ résolu et les allocations réelles (C/Y_o, V/Y_o) sont indépendants de π̄ pour π̄ ∈ {0 ; 2 % ; 10 %}. La tolérance se fixe avec #49. C'est l'extension du contrôle T2 de la fiche 4.
- **C16 — Élasticités des ménages transmises.** Elles figurent dans la Q2 (inflation lue) et dans la Q3 (taux : effet partiel et effet d'équilibre général). Leurs délais :
  - taux du tour n → ligne 10 en phase 6 du tour n → plan du tour n + 1 ;
  - glissement du tour n − 1 → plan du tour n.
- **C17 — Assouplissement quantitatif au socle.** Sous B_H ≡ 0, les achats se font à la banque seule (19b-banque) : échange de réserves contre titres, M inchangé (l. 410 et 411). Ce point est à déclarer à `jeu`. Sous une demande de Tobin en stock, un achat 19b-ménages s'annulerait en un tour (Q1, point 4).
- **C18 — Haute inflation (J6).** Avec ν fixe, il n'y a pas de fuite hors des dépôts : la cible corrigée ne donne qu'une semi-élasticité de l'ordre de −ν. Une dynamique de type Cagan demande un actif de fuite (billets, devises, biens) ou une cible fonction de i_D − π^e, à J6.

**Fiche 7 (banque commerciale)** :
- **C19 — Placement.** Sous B_H ≡ 0, 19a-banque = besoin − 19a-BC, reliquat déclaré de l'équation d'émission. Res s'obtient par les flux et L^CB par la règle de la phase 8 (c). Aucun poste n'est obtenu par différence du bilan bancaire (défaut v2.0).
- **C20 — Taux des dépôts.** Les ménages n'ont aucun actif concurrent. La règle de transmission (écart, délai en tours) est donc déclarée, et la marge est réglée par un mécanisme, non par une borne. Elle fixe le rendement réel des dépôts et l'impôt d'inflation net.
- **C21 — Distribution (ligne 15).** Le délai de versement de Div_Bk fixe la compensation, en équilibre général, du canal rentier (Q3, point 1). Il est déclaré.
- **C22 — Limite de détention de titres**, si elle existe : elle est déclarée, et son activation est le placement raté (l. 479). Le risque de renouvellement relève de J6.

**Fiche 9 (État et dette)** :
- **C23 — Règle budgétaire face à la charge d'intérêts.** Elle est déclarée : elle fixe le signe de long terme du canal rentier (Auclert, 2017, p. 17).
- **C24 — Durée de la dette.** Toute part à taux fixe, qui étalerait le canal rentier, est une décision citant M22 (l. 523).
- **C25 — Ordre de la phase 7 sous B_H ≡ 0** : besoin de l'État, puis souscription et achats décidés de la banque centrale, puis reliquat de la banque. La Q5 est sans objet. Variante de Tobin (J6) : non-renouvellement par la ligne 19a-ménages négative, la banque en reliquat, jamais la ligne 19b en acheteur passif.

### 6.4 Points signalés à `jeu` (non tranchés)

- « Hausse de taux → consommation des ménages en hausse au tour suivant » (canal rentier) : un signe contre-intuitif, à déclarer. L'effet net dépend de l'investissement et de la règle budgétaire (C14, C23).
- « L'inflation ronge l'épargne, les ménages la reconstituent » : effet lisible et stabilisant.
- Trois indicateurs : taux d'épargne nominal, taux d'épargne corrigé, rendement réel des dépôts. Le mot « impôt d'inflation » est réservé à la perte nette.
- Assouplissement quantitatif sans effet sur la masse monétaire au socle (C17).
- Sous la cible nominale, relever la cible d'inflation aurait un effet réel permanent, exploitable. Sous la cible corrigée, l'effet est négligeable.

### 6.5 Additif de `monnaie` (03/10/2026) : Q10 et π_s

*Réponse au § 3.C-10 et à la réponse de `macro` sur la cible de Haig-Simons (point 8). Sources lues : fiche 5, § 3.C, § 3.C-10, § 5 et § 6 ; réponse de `macro` ; ADR 0008, partie I ; fiche 3, § 6.3 (C1 à C3). Calculs : `m6_ratios.py` et `m6_cible.py` (bloc 5 seul, forme fermée et simulation). La boucle conjointe n'a pas été refaite par `monnaie` ; ses rayons ont été confirmés au 4e chiffre par la contre-épreuve indépendante du § 3.C-10, point 8, ce qui lève la condition posée au retrait de (a).*

**Q10 — Inflation lue dans le terme de tendance**
- **Je retire la lecture (a).**
  - Fait nouveau : l'explosivité de (a) en boucle conjointe (1,0275 en régime H, 1,0029 en régime B, enveloppe de 1,0171 par tour ; § 3.C-10), confirmée par la contre-épreuve indépendante.
  - Mon motif pour (a), son exactitude quelle que soit la fiche 8, reste vrai mais ne pèse pas contre un échec de l'exigence 5 (c). Une instabilité mesurée ne se réintroduit pas.
- **Le défaut tient au gain, non à la fenêtre du glissement** : la variation sur un tour et sur 3 tours restent explosives ; frontières ν < 0,586 et h < 0,604 (mesures de `macro`). Statut : hypothèse d'interprétation, cohérente avec ces mesures.
- **Je recommande (c)**, avec quatre précisions :
  1. **La règle lit la cible déclarée π\*, jamais π̄.** π\* est un paramètre ou un levier de la fiche 8 ; π̄ est l'inflation stationnaire, un résultat. La notation « (c) = π̄ » du § 3.C-10 est à écrire π\* dans la spécification. Jusqu'à la fiche 8, π^e = π\* est exogène : (b) et (c) coïncident. Statut : vérifié contre C1 et C2 (fiche 3, § 6.3).
  2. **Sous C2, (c) ne coûte rien à l'état stationnaire** : V/(n_a·Y_o) = 1,010286 à 2 % et 1,014518 à 10 %, comme sous (a) ; le résidu tient à #49. Statut : vérifié (`m6_ratios.py`).
  3. **Un changement de cible devient un choc de demande direct, le tour même** : une baisse d'un point de π\*, états d'ouverture fixés, relève le plan de +0,55 % sous la cible de Haig-Simons (+0,98 % sous la cible nominale). Une désinflation annoncée relève donc la consommation au tour même, à contre-courant. Statut : vérifié (`m6_cible.py`). Signalé à `jeu` et à la fiche 8.
  4. **Les régimes B, D et E n'ont pas de cible propre** : la π\* lue par les ménages y reste à définir (cible de l'union ou inflation de l'ancre). Renvoi à la fiche 8 et au J5. Statut : non instruit.
- **Variante h** (π^lu = h·π_{t−1} + (1 − h)·π\*) : **non recommandée**. h < 0,604 est une frontière de stabilité, non une calibration : ce paramètre sans source masquerait une instabilité. Sa marge n'est mesurée qu'à la calibration.
- **(b) avec la loi de π^e de la fiche 8** : candidate à une réouverture, pas au socle. Avantages : exacte hors C2 si C1 tient ; un changement de cible n'entre que par la crédibilité. Risque : une loi qui suit le glissement avec un fort poids d'impact réintroduit la boucle du § 3.C-10, point 3. Une loi à gain faible devrait atténuer l'oscillation de 17 à 19 tours, au prix d'un retard (hypothèse, non vérifiée).
- **C26 (fiche 8) — clause de réouverture de la Q10 vers (b)**, écrite avant l'essai. Trois conditions :
  - (i) C1 tient ;
  - (ii) la boucle conjointe complète (SN, C, M, ménages avec π^lu = π_s = π^e, règle de taux, loi de π^e) a un rayon < 1, régimes H et B, θ_H = 0,8 et 1, à la calibration et sur la grille ×0,5 / ×2, gain de la loi de π^e compris ;
  - (iii) contrôle de séparation : la même boucle avec π^lu = π\*, pour attribuer une instabilité aux ménages ou aux salaires.
  Si une condition échoue, (c) reste. Une réouverture est une décision citant M27.
- **C16 mise à jour** : sous (c), l'élasticité du plan au glissement est nulle à l'impact ; l'effet d'encaisses réelles passe par le revenu nominal, qui croît plus vite que V (0,9637 contre 0,9859 à prix figés, § 3.C-10, point 6.1). L'élasticité transmise devient celle du plan à π\*.

**Q2, point 3 — π_s dans la cible de Haig-Simons**
- **Je ne maintiens pas π_{t−1}**, pour deux motifs :
  - (i) π_s mesuré est explosif à θ_H = 1 (1,0223 / 1,0218, même avec γ^e sur π\*), et θ_H = 1 est dans le domaine des fiches 6 et 9 ;
  - (ii) la règle C doit avoir une seule lecture de l'inflation : γ^e et π_s lisent la même π^lu. La lecture mixte est aussi la pire hors cible (tableau ci-dessous).
- **Mécanisme** : π_s mesuré fait de la richesse réelle visée une fonction décroissante de l'inflation mesurée, comme la demande d'encaisses de Cagan (1956, cité de mémoire), d'où une rétroaction positive lente. Statut : hypothèse ; condition de stabilité de Cagan non vérifiée.
- **Ralliement** à V\* = ν·n_a·(YD^e − π_s·V_H), avec π_s = (1 + π\*)^{1/n_a} − 1, et au point 8 du § 3.C-10.
- **Ce que l'on perd hors C2** (cible 2 %, i_D = 1 % + π stationnaire, ν = 1, n_a = 12 ; la relation de Fisher hors C2 est une hypothèse de `monnaie`). Statut : vérifié, forme fermée et simulation concordantes à 5 chiffres.

  | π stationnaire | V/(n_a·Y_o), lecture exacte (π_{t−1} partout) | (c) partout, λ_V = 0,4 | (c), λ_V de 0,2 à 0,8 | mixte, γ^e sur π\* et π_s mesuré |
  |---|---|---|---|---|
  | 2 % | 1,01029 | 1,01029 | 1,01029 | 1,01029 |
  | 3 % | 1,01051 | 0,99698 (−1,34 %) | 0,97531 à 1,00822 | 0,98737 (−2,29 %) |
  | 10 % | 1,01452 | 0,91867 (−9,45 %) | 0,79647 à 0,99694 | 0,85933 (−15,30 %) |

  Sur V/(n_a·YD), (c) donne −1,29 % à 3 % (0,95875 contre 0,97126) et −8,58 % à 10 % (0,83435 contre 0,91267).
- **Hors C2, λ_V fixe l'état d'arrivée** : le critère 4 échoue, c'est un continuum d'équilibres, à déclarer. Sous C2, la perte stationnaire est nulle. C2, intégrale et sans fuite, devient donc aussi une condition de la fiche 5 : un point d'écart stationnaire entre π et π\* coûte environ 1,3 % du ratio.
- **C18 renforcée (J6)** : sous (c), la richesse visée ne fuit pas devant l'inflation. Une haute inflation durable hors cible y fait varier la richesse réelle selon λ_V, sans dynamique de Cagan ; elle demandera (b) ou un actif de fuite au J6.
- **Restitution, point signalé à `jeu`** : deux corrections distinctes, qui divergent hors cible, demandent des libellés distincts : le niveau normal ν, sur YD^HS au taux de la cible (comportement), et le taux d'épargne corrigé de la Q5, sur la perte mesurée (constat).

**Pour M27**
- **Aucun désaccord ne subsiste avec `macro`** : cible de Haig-Simons ; γ^e et π_s lus sur la cible ; variante h refusée sans mesure. Les deux positions décrites au § 6.1 (Q2, point 3), dans la réponse de `macro` et au § 6.2 (« lecture (a) ») sont caduques.
- **Trois ajouts de `monnaie`**, à confirmer par `macro` : lecture de π\*, non de π̄ ; clause C26 ; déclaration de l'effet d'un changement de cible.

## 7. Avis de `jeu`

*`jeu`, 03/10/2026 (issue #41, jalon 2), sur la fiche à l'état `d88a47e` (branche `claude/j1-economie-reelle`, PR #43). Réponses aux six questions de `macro`.*

**Chiffres.** Aucun moteur n'existe encore. J'ai écrit une maquette indépendante, qui n'importe aucun script `f5_*` ni `p4_*`.
- **Forme.** Contrairement à B1, elle est écrite **en niveaux**, sans détendance. On peut donc la confronter à B1, détendue, sans reprendre ses conventions.
- **Contenu.** Le socle N1 à N7, avec la tendance géométrique. L'emploi R, plafonné à la population active (U^eq = 5 %). Des prix exogènes sur leur sentier. La règle C avec le plafond du § 3.N-6 (a). Le revenu YD = θ_H·p·y + (i_D/12)·D_H + Tr. Une variante en **équilibre partiel du bloc** (PE) tient sur son sentier la production qui alimente le revenu.
- **Hypothèses** : celles du § 3.0 (g = π̄ = 2 %, ν = 1, λ_V = 0,4, i_D = 3 %, θ_H = 0,8, part de G de 20 %).
- **Exécution** le 03/10/2026, hors dépôt : `uv run --no-project python jeu_men1.py` à `jeu_men12.py`.

- **Contrôle de la maquette.**
  - Sans choc, la dérive relative est au plus de 4·10⁻¹⁴ sur 720 tours.
  - Elle reproduit à la troisième décimale, sur les neuf tours et pour les deux exemples du § 3.L, les colonnes « plan », « YD » et « taux d'épargne ».
  - Elle reproduit les valeurs propres de la boucle propre de F5 : 0,96678 et 0,96772, soit 20,5 et 21,1 tours ; 0,98339 et 0,98385 ; 0,93355 et 0,93551.
  - Elle reproduit la sur-commande. Le service vaut 1 jusqu'au tour 8, puis il est rationné aux tours 9 à 12 (minimum 0,850). La demande non servie des ménages est nulle dès le tour 13. La richesse est à +6,33 %, soit 0,79 mois de consommation. La production reste au plafond jusqu'au tour 134 et revient à +0,77 % au tour 240.
  - Elle reproduit le tableau Q3 dans la convention de Godley et Lavoie, où la perte d'inflation vaut π_mensuel·V_{−1}. Dans la convention (1 − 1/Π)·V, le taux corrigé vaudrait 2,029 % et 2,291 %. L'écart tient à la convention ; je retiens celle de `macro`.
- **Constat 1 : la colonne « ratio » du § 3.L n'est pas le ratio annoncé.** Le § 3.L la définit comme V/(12·YD), mais elle vaut **V/V̄**, la richesse rapportée à son sentier stationnaire. B1 divise par le YD stationnaire (`o['V']/(12*b.YD)`). Avec les définitions de la fiche, le ratio **baisse** après un transfert, parce que le revenu monte avant la richesse :

  | Tour | Colonne publiée (= V/V̄) | V d'ouverture / (12 × YD du tour), lecture du test zéro | V de clôture / somme des 12 derniers YD, lecture de restitution (e) |
  |---|---|---|---|
  | 1 | 1,00000 | 0,99010 | 1,0216 |
  | 9 | 1,00427 | 0,98425 | 1,0151 |
  | 13 | 1,00669 | 0,99270 | 1,0108 |
  | 24 | 1,00726 | 1,00074 | 1,0184 |

  Le niveau normal dans la lecture (e) vaut **1,0216 an, et non 1** : 12ν(Γ − 1)/(1 − Γ^{−12}), vérifié par la formule et par la maquette.
- **Constat 2 : le ratio sort de la bande pendant la sur-commande.** La fiche écrit « ratio de richesse au plus à +0,99 % de ν, donc dans la bande de ±2 % ». Dans la lecture du test zéro, le ratio tombe à **0,9514 au tour 2** et reste hors de ±2 % des tours 2 à 10. Il culmine à 1,0166 au tour 159. Le chiffre +0,99 % est la valeur du seul tour 13. Le critère 11 (c) étant une mesure, aucun verdict ne change.
- **Constat 3 : hausse de taux.** Une hausse de i_D d'un point donne un plan **+0,66 %** au tour n + 1, et non +0,6 % comme l'écrit le § 3.N-9. Le terme de richesse ajoute 0,06 point.

**Question ludique de la fiche.** Le bloc n'ouvre aucun levier. C'est pourtant par lui que trois leviers atteignent la demande : les transferts, les impôts et, à l'envers, le taux. Il porte aussi la mémoire des crises : l'épargne forcée, puis son déblocage. Les questions sont donc les suivantes :
- un transfert agit-il dans l'année, avec une contrepartie visible ?
- la richesse donne-t-elle une inertie que le joueur peut anticiper ?
- un signe contre-intuitif (taux → consommation) reste-t-il explicable ?

### 7.A, 7.B, 7.S et 7.R (brièvement)

- **A : à revoir.** La cible d'Euler sans ancre fait dériver la consommation avant toute décision du joueur. Les trois strates touchent M22. A est la seule option qui donne au taux le signe intuitif, mais par un mécanisme réfuté (hypothèse n° 3). Je ne demande pas qu'il soit repris sans fait nouveau.
- **B : à revoir.** Elle repose sur un plafond invisible (0,9 × encaisse, instabilité 15), un état caché et une branche itérative.
- **S : à revoir avec α libres.** Le niveau normal de richesse dépendrait de la vitesse α_2 : un réglage de vitesse déplacerait ce que le joueur prend pour la norme. Avec α_1 dérivée de ν et de λ_V, S est identique à C.
- **R1 : inadmissible.** Avec α_Y < 0, une hausse de revenu ferait baisser la consommation. C'est un comportement contre-intuitif sans récit possible.
- **R2 : hors classement**, référence non mesurée. Son multiplicateur contemporain casserait la règle des délais (« décision au tour n, effet sur le secteur privé au tour n + 1 au plus tôt »).

### 7.C Option C — cible de richesse avec terme de tendance

- **Ce que voit le joueur.**
  - **Transfert** de +1 % du revenu disponible aux tours 1 à 12 :
    - au tour 1, la contrepartie est visible : les dépôts montent et le taux d'épargne passe de 3,97 à 4,92 % ;
    - la consommation monte dès le tour 2 (+0,66 %) ;
    - à la fin des transferts, en PE, elle retombe en un tour (+0,77 % au tour 13, +0,12 % au tour 14), puis s'éteint lentement (+0,09 % au tour 24).
  - **Dépense publique** : effet sur la consommation au tour n + 2. Le premier tour où l'écart de C atteint 0,1 % est le tour 5 pour G +1 %.
    *Annotation du 04/10/2026 (revue finale de `macro`, mesure ; décision inchangée) : depuis M28 (règle F), une dépense publique du tour n relève le dividende du tour n (ligne 14, environ +0,498 par u.m. de G, les dépôts visés absorbant le reste), compté par H7 dans le revenu du tour n : le budget des ménages bouge **dès le tour n + 1** (+0,315 par u.m. de G), puis au tour n + 2 par l'emploi. Le critère J3 « Délais » est corrigé de façon prospective dans la spécification (décision du mainteneur du 04/10/2026, aucun essai fait).*
  - **Délais mécaniques** : transferts et impôts → consommation, 1 tour ; dépense publique → consommation, 2 tours ; taux → consommation, 1 tour. Ils sont **lisibles** et cohérents avec mes avis sur les fiches 3 (question 5) et 4 (question 2).
- **Leviers.** Aucun levier propre. **Transferts et dépense publique ne sont pas redondants** (production supplémentaire en u.m. par u.m. publique, θ_H = 0,8) :

  | Horizon | G | Transferts du même montant |
  |---|---|---|
  | 12 tours | 1,49 | 0,85 |
  | 24 tours | 3,03 | 2,18 |
  | 60 tours | 3,72 | 3,35 |
  | 120 tours | 4,67 | 4,57 |

  G est plus rapide. Les transferts rattrapent G sur une partie et laissent de la richesse aux ménages. C'est un vrai arbitrage, qui prendra son sens avec la dette (fiche 9) et le soutien politique (J7).
- **Stratégies.** La règle n'ouvre aucune « remise à zéro gratuite ». En revanche, la persistance de l'activité dépend de la fermeture (risque ci-dessous).
- **Risques.**
  - *Persistance quasi permanente sans fuite* (réserve 5 de `macro`, #44). Après les transferts de +1 % du revenu disponible aux tours 1 à 12, l'écart de production vaut :

    | θ_H | Tour 13 | Tour 36 | Tour 60 | Tour 240 |
    |---|---|---|---|---|
    | 0,8 | +1,43 % | +0,28 % | +0,21 % | +0,02 % |
    | 1 | +2,15 % | +1,17 % | +1,01 % | +0,94 % |

    Sous θ_H = 1, une relance d'un an laisserait un gain d'activité quasi permanent, sans signal ni coût à ce stade. Ce serait une stratégie dominante (relance ponctuelle) et, symétriquement, un piège (austérité ponctuelle). Ce n'est pas un défaut de la fiche 5 seule ; je demande un critère de jouabilité à la fermeture (condition 10).
  - *Signe contre-intuitif du taux* (question 4).
  - *Ratio de richesse trompeur à court terme* (constats 1 et 2) : il faut le doubler d'un signal (question 1).
- **Verdict : lisible**, sous les conditions 1 à 10.

### 7.D Variante à deux types

Elle est identique à C au niveau agrégé. Sa valeur ludique n'apparaît qu'avec le transfert ciblé (question 6). **Lisible au J4**, sans objet au socle.

### Réponses aux six questions de `macro`

1. **ν et le taux d'épargne : lisibles, à condition de les restituer sous forme additive et de doubler le ratio d'un signal.**
   - **ν** se lit bien : « les ménages détiennent un an de revenu en dépôts ».
     - Son niveau normal doit être publié **dans la définition affichée** : 1,0216 an dans la lecture (e), et non 1. C'est le même principe que les stocks à 1,4152 mois (fiche 2) et la part salariale à 0,7989 (fiches 3 et 4).
     - Le ratio est un indicateur **lent**, mauvais signal à court terme. Il baisse après un transfert (1,0216 → 1,0108 au tour 13) et tombe à 0,951 au tour 2 de la sur-commande, alors que les dépôts montent.
     - Je demande donc un indicateur de plus, **l'écart à la richesse visée**, (V − V*)/C en mois de consommation, V* étant la cible que lit la règle. C'est le même choix que ξ à la fiche 4 : afficher la variable que lit la règle.
     - Ce signal précurseur dit le sens de la consommation à venir. Pendant les transferts, −0,12 à −0,21 mois (EG) : « les ménages reconstituent leur épargne ». Après une sur-commande de 24 tours, +1,87 mois au tour 25 : « réserve d'épargne à dépenser, rattrapage à venir ».
   - **Taux d'épargne : les deux, mais sous forme additive**, plutôt que deux taux à dénominateurs différents. Restituer le taux nominal, comptable et lié à ΔV, décomposé en points de revenu nominal :

     | | π̄ = 2 % | π̄ = 10 % |
     |---|---|---|
     | Taux nominal | 3,97 % | 11,57 % |
     | dont maintien de la richesse face à l'inflation | 1,98 | 9,57 |
     | dont épargne réelle | 1,98 | 2,00 |

     Sans décomposition, un joueur verrait en haute inflation des ménages qui « épargnent trois fois plus » et y lirait une crise de confiance qui n'existe pas. Décomposé, le chiffre rend visible la **taxe d'inflation payée par les déposants** : un perdant identifiable (O2) et une matière pour le soutien politique (J7).
     - Le taux corrigé de Haig-Simons (2,025 % et 2,209 %) figure dans la définition, sans ligne propre.
     - Le niveau normal est publié **à l'inflation mesurée**, 12γ^e·ν, pour qu'une hausse mécanique ne se lise pas comme un écart.
2. **Demi-vie de 21 tours : perceptible et bien placée, mais là où il faut.**
   - Sur une partie de 60 à 120 tours, un écart de richesse est divisé par 7 à 50 : le retour se voit dans la partie, sans être instantané.
   - Pour λ_V × 0,5, la demi-vie est de 41 tours : le retour n'est vu qu'en partie longue. Pour λ_V × 2, elle est de 10 tours.
   - Après un transfert ordinaire, la queue est minuscule (+0,09 % de C au tour 24, moins d'un cran à une décimale). L'inertie de la richesse ne se perçoit qu'après les **chocs de richesse importants** : épargne forcée, crise. C'est là qu'elle a un sens ludique (le rattrapage d'après-guerre).
   - Ce que le joueur voit de la persistance d'activité dépend de la boucle conjointe (42,6 à 49 tours à θ_H = 0,8 ; environ 200 à 1 000 à θ_H = 1), d'où la condition 10.
3. **Seuil du critère 12 (d) : entre 0,50 et 0,85**, en équilibre partiel du bloc ; détail plus bas.
4. **Taux qui relève la consommation : à déclarer, à décomposer, et à mesurer en net avant d'ouvrir le levier.**
   - L'ampleur n'est pas marginale. Avec ν = 1, un point de i_D vaut un transfert permanent de 1 % du revenu disponible, soit environ quatre fois G +1 % en demande. En PE, la consommation monte de +0,66 % au tour 2 et de +1,03 % au tour 120.
   - Une hausse de 0,25 point fait monter C de 0,1 % dès le tour 2. Avec des intérêts versés de l'extérieur et sans compensation par les dividendes, C est à +0,85 % au tour 60 (EG).
   - Le joueur qui relève le taux contre l'inflation verrait sa consommation monter. Sans explication, c'est contre-intuitif ; avec elle, c'est lisible : « vous enrichissez les épargnants ».
   - Restitution :
     - le revenu disponible décomposé par source (salaires, intérêts, dividendes, transferts, impôts), en contributions additives, avec la ligne « intérêts reçus » qui saute au tour même ;
     - dans la fiche du levier (J4) : signe +, délai de 1 tour, gagnants (déposants), perdants (emprunteurs : entreprises, État) et contrepartie (charges d'intérêts).
   - **Condition** : le signe **net** d'une hausse de taux sur la demande totale à 12 et 36 tours est mesuré et publié avec les fiches 6 à 9 avant que le levier de taux ne s'ouvre au J4. Les intérêts reçus sont en partie compensés par des dividendes plus faibles et par la charge de l'État.
   - Le canal de substitution (variante PCEX2) relève de `macro` et `monnaie`. Je ne demande pas d'écart à la littérature.
5. **Dimension de la sur-commande : le doublement pendant 12 tours ne suffit pas comme scénario adverse.**
   - Les stocks absorbent les 8 premiers tours. Le rationnement ne dure que 4 tours, ce qui ne remplit pas le libellé du critère 11 (c) (« dépense demandée supérieure au disponible du pas pendant 12 tours »).
   - Surtout, la demande non servie des ménages cesse **le tour même** où le choc cesse, si bien que le seuil de 12 tours n'est pas éprouvé.

     | Scénario (prix figés, sans politique) | Rationnement | Service minimal | Dernière demande non servie des ménages | Demande non servie cumulée | Plan maximal | Plafond d'emploi actif jusqu'au tour |
     |---|---|---|---|---|---|---|
     | G ×2, 6 tours | aucun | 1 | — | 0 | +4,99 % | 61 |
     | G ×1,5, 12 tours | aucun | 1 | — | 0 | +4,99 % | 62 |
     | **G ×2, 12 tours** | tours 9 à 12 | 0,850 | tour 12 | 0,60 mois de C | +5,67 % | 134 |
     | G ×2, 20 tours | tours 9 à 62 | 0,830 | tour 62 | 2,5 mois | +9,48 % | 206 |
     | **G ×2, 24 tours** | tours 9 à 89 | 0,820 | tour 89 | 4,0 mois | +11,29 % | 234 |
     | G ×3, 12 tours | tours 4 à 69 | 0,714 | tour 69 | 3,3 mois | +10,62 % | 214 |
     | G ×2, 12 tours, θ_H = 1 | tours 8 à 47 | 0,842 | tour 47 | 0,7 mois | +5,86 % | ≥ 480 |
     | G ×2, 24 tours, θ_H = 1 | tours 8 à ≥ 480 | 0,803 | jamais résorbée | — | +11,90 % | ≥ 480 |

   - **Proposition** : deux dimensions, écrites avant l'essai.
     - (a) **G ×2 pendant 12 tours**, pour la continuité avec la condition 6 de la fiche 2.
     - (b) **G ×2 pendant 24 tours**, qui donne 16 tours de rationnement pendant le choc. Deux ans d'économie de guerre sont une stratégie plausible dans une partie, plus que le triplement. La durée éprouve l'accumulation de l'épargne forcée et le critère 11 (b) : le plan reste borné (+11,3 % au plus).
   - Dans la maquette à prix figés, (b) **échoue** au seuil de 12 tours (demande non servie jusqu'au tour 89). Le seuil n'est tenable qu'avec les prix (M, fiche 4) et la politique (fiche 8) ; c'est ce que le test du J4 doit établir. Accord avec la réserve 8 de `macro`.
   - **Gratuité de la sur-commande** (11 (d)). Sous rationnement proportionnel, gonfler la commande capte des biens sans payer la part non servie. Dans l'épisode (b), passer de ×2 à ×4 aux tours 13 à 24 augmente le volume servi à l'État de +49 % (4,12 → 6,15) et réduit celui des ménages de −23 % (8,60 → 6,64), avec un service tombé à 0,61. C'est une **priorité de fait, gratuite**. Le levier G du J4 ne doit pas la permettre sans coût ni affichage (condition 9).
6. **Deux types : renvoi au J4 avec les transferts ciblés, d'accord.**
   - Au socle, sans levier ciblé, D est indiscernable de C : l'afficher serait de la complexité sans mécanisme perçu.
   - Au J4 :
     - (i) D entre avec le levier ;
     - (ii) un test vérifie qu'en l'absence de transfert ciblé la trajectoire est identique à C, à 1e−12 près ;
     - (iii) le catalogue déclare que le transfert ciblé a une propension d'impact de 1, contre α_Y pour le transfert universel.
   - Pour la stabilisation, le ciblé domine alors l'universel. C'est acceptable comme leçon, à condition que l'universel garde un autre rôle (richesse, soutien politique au J7) ; sinon un des deux leviers est redondant. Question à poser au J4.
   - χ se calibre sur une source lue (KVW, environ 20 % du revenu, `macro`).

### Indicateurs du tour (critère 12 (a))

| Indicateur | Verdict | Motif ou point à clarifier |
|---|---|---|
| Consommation en volume (glissement sur 12 tours) | **lisible** | Niveau normal g dans la définition exacte |
| Dépense demandée, exécutée, taux d'exécution | **lisible** | Condition 1 de la fiche 2 |
| Demande non servie des ménages | **lisible** | Signal de crise, non précurseur (`CONTEXT.md`) ; avec elle, la **demande non servie cumulée de l'épisode** (épargne forcée), en mois de consommation |
| Revenu disponible réel (glissement sur 12 tours) | **à clarifier** | Décomposé par source en contributions additives : c'est ce qui rend lisibles les transferts et le canal du taux (question 4) |
| Taux d'épargne (12 tours) | **à clarifier** | Nominal, décomposé en maintien face à l'inflation et épargne réelle ; niveau normal à l'inflation mesurée (question 1) |
| Richesse en années de revenu | **à clarifier** | Niveau normal dans la définition affichée (1,0216 an sous la lecture (e)) ; indicateur lent, non utilisable comme signal |
| Écart à la richesse visée, (V − V*)/C en mois | **à ajouter** | Signal précurseur du sens de la consommation ; c'est la variable que lit la règle |
| Composition dépôts / titres | **hors du tableau de bord** sous B_H ≡ 0 | Ligne figée à 0 ; elle revient avec une demande de titres (fiche 9 ou J6) |

### Préférence motivée

- **Ma préférence va à C**, comme celle de `macro`.
  - **Mes motifs propres** :
    - des délais d'un tour, uniformes ;
    - une contrepartie visible le tour même (dépôts, taux d'épargne) ;
    - un arbitrage réel entre transferts et dépense publique (vitesse contre persistance) ;
    - une inertie de la richesse qui donne un rattrapage lisible après les crises ;
    - un niveau normal ν exact, qu'aucun réglage de vitesse ne déplace.
  - **Les motifs de `macro`**, que je ne juge pas : critères 3, 4, 5 et 14.
- **Classement** : C = D au socle (D au J4, avec le ciblage) > S (α dérivées, sinon à revoir) > B > A. R1 est exclue ; R2 est hors classement.
- **Lectures soumises au § 5** :
  - (a) π^lu = glissement mesuré : **accord**. Une annonce ne déplace pas l'épargne le tour même, conformément à la fiche 3 (question 5).
  - (b) Plafond en phase 2 : **accord**, sans enjeu ludique tant qu'il est inactif (marge d'environ 12 mois). S'il devient actif : mention « ménages à court de dépôts ».
  - (c) B_H ≡ 0 : **accord au socle**. Qui détient la dette deviendra une question de jeu (crises O3, J4 à J7).
  - (d) Canal rentier seul : **accepté au socle**, sous les conditions de la question 4.
  - (e) Taux d'épargne : **les deux, sous forme additive** (question 1). C'est une nuance de forme, non un désaccord.
- **Cohérence avec mes avis antérieurs.**
  - Fiche 3, question 7, et fiche 4, question 8 : j'y demandais que la consommation des ménages porte le coût d'une baisse de ω* ou d'un gel des prix. La règle C le permet par Div_F, avec α_Y = 0,6 au tour n + 1. L'ampleur dépend de la distribution (fiche 6).
  - La lecture (G) reste préférée (fiche 3, question 10).
- **Coût en fidélité** : je ne demande aucun écart à la littérature. La décomposition du taux d'épargne, l'écart à la richesse visée et le revenu par source sont des choix de restitution. La borne haute du seuil (12 (d)) est un argument de jeu, signalé comme tel.

### Conditions demandées au § 9 (restitution et essais)

1. **Revenu disponible décomposé par source** (salaires, intérêts, dividendes, transferts, impôts), au tour et sur 12 tours, en contributions additives à sa variation.
2. **Taux d'épargne nominal** sur 12 tours, décomposé en points de revenu nominal (maintien de la richesse face à l'inflation, épargne réelle), avec son niveau normal à l'inflation mesurée, 12γ^e·ν. Le taux de Haig-Simons figure dans la définition.
3. **Richesse en années de revenu**, avec son niveau normal dans la définition affichée (1,0216 an à g = π̄ = 2 %, ν = 1, lecture (e)), publié par le script d'état stationnaire.
4. **Écart à la richesse visée**, (V − V*)/C en mois de consommation, nommé « réserve d'épargne » s'il est positif et « épargne à reconstituer » s'il est négatif.
5. **Demande non servie cumulée de l'épisode** (épargne forcée), en mois de consommation, à côté de la demande non servie du tour.
6. **Composition dépôts / titres hors du tableau de bord** tant que B_H ≡ 0.
7. **Tableau levier → indicateur → délai → contrepartie** (critère 12 (c)), avec le délai mécanique et le délai perçu (premier tour où l'écart de C atteint 0,1 % : 2 pour les transferts et les impôts, 5 pour G +1 %, 2 pour i_D +0,25 point). Le signe + du taux y est déclaré, avec gagnants et perdants.
8. **Signe net du taux** sur la demande totale à 12 et 36 tours, mesuré avec les fiches 6 à 9 et publié avant l'ouverture du levier de taux (J4).
9. **Sur-commande au J4**, avec prix et politique endogènes, en deux dimensions écrites avant l'essai : G ×2 pendant 12 tours et G ×2 pendant 24 tours. Sont publiés la part servie aux ménages, la demande non servie cumulée, le rattrapage, l'activité de la borne d'emploi (critère 8 (c)) et le volume servi à l'État. La gratuité de la commande non servie est soit supprimée, soit rendue visible et coûteuse (fiche 9, J4).
10. **Persistance d'une impulsion de demande** (J3, à la fermeture de #44). Après une dépense publique ou des transferts aux tours 1 à 12, l'écart de production revient sous la moitié de son pic en au plus 60 tours, soit la fenêtre de partie la plus courte. Le critère est à écrire avant l'essai.
    - θ_H = 0,8 : le seuil est tenu dans la maquette.
    - θ_H = 1 : il ne l'est pas (+1,01 % au tour 60 pour un pic de +2,15 %).

### Seuil proposé au mainteneur (critère 12 (d))

- **Grandeur** : part = Σ_{t=1..12}(C_t − C̄_t) / Σ_{t=1..12} Tr_t, pour un transfert de 1 % du revenu disponible stationnaire aux tours 1 à 12.
  - Elle est mesurée **en équilibre partiel du bloc** : revenus hors transfert et prix sur leur sentier, comme la boucle propre du critère 5 (b).
  - Sans dimension (u.m. par u.m.) ; fenêtre : tours 1 à 12.
  - Avec le délai d'un tour, elle ne peut dépasser 11/12 ≈ 0,917.
- **Seuil** : **de 0,50 à 0,85, bornes comprises**, à la calibration proposée. Aux vitesses × 0,5 et × 2, les valeurs sont publiées sans être exigées.
- **Mesures** (maquette indépendante, `jeu_men3.py` et `jeu_men4.py`) :

  | Calibration | PE, tours 1 à 12 | PE, tours 1 à 24 | Impulsion : part dépensée dans les 12 tours suivant le versement | EG, tours 1 à 12 |
  |---|---|---|---|---|
  | ν = 1, λ_V = 0,4, i_D = 3 % | **0,628** | 0,786 | 0,744 | 1,007 |
  | i_D = 0 | 0,624 | 0,776 | 0,737 | 1,000 |
  | λ_V × 0,5 | 0,761 | 0,860 | 0,847 | 1,401 |
  | λ_V × 2 | 0,421 | 0,755 | 0,650 | 0,530 |
  | ν = 0,5 | 0,786 | 0,905 | 0,886 | 1,470 |
  | ν = 2 | 0,310 | 0,543 | 0,457 | 0,372 |
  | π̄ = 10 % | 0,614 | 0,759 | 0,723 | 0,983 |

  - **Frontières sous C** : à ν = 1, la part vaut 0,516 à λ_V = 0,6, 0,466 à 0,7 et 0,836 à 0,1. Le seuil demande donc environ 0,08 ≤ λ_V ≤ 0,62 à ν = 1, et λ_V ≤ 0,26 environ à ν = 2.
  - **EG** : la part dépasse 1 sous l'effet du multiplicateur. Elle dépend des fiches 6 et 9 et n'est que publiée au J4.
- **Motifs.**
  - **Borne basse, 0,50.** « Plus de la moitié d'un transfert est dépensée dans l'année » : en deçà, le transfert agit surtout après l'année de la décision, et le joueur ne le relie plus à son effet. Le levier se réduit alors à un placement en dépôts, dominé par G pour la stabilisation (G : 1,49 contre 0,85 par u.m. à 12 tours, même à 0,63). L'ordre de grandeur n'est pas contredit par la littérature lue par `macro` (50 à 90 % de dépense totale en trois mois, PSJM 2013), dont le jugement relève de `macro`.
  - **Borne haute, 0,85.** Au-delà, le transfert devient une dépense publique décalée d'un tour : deux leviers pour une même chose. Le rattrapage disparaît, faute de richesse accumulée. À ν = 1, il y faut λ_V ≤ 0,08, soit une demi-vie de la richesse d'environ 100 tours, plus longue qu'une partie : un choc de richesse ne se résorberait plus pendant la partie. *Argument de jeu, signalé comme tel.*
- **Transparence.** Je propose ce seuil après avoir mesuré les parts. Il ne départage pas les options : seule C a une forme fermée tenue. Il contraint la calibration du J3 (νλ_V), et son rôle est d'empêcher une calibration qui rendrait le transfert muet dans l'année ou identique à G.
- **Vérification au J3** : appel direct de la fonction du bloc en équilibre partiel, sans le programme entier (`CLAUDE.md`, « Règles des tests »).

### Additif de `jeu` (03/10/2026) : boucle conjointe, ratio de richesse, part du transfert

*Sur le § 3.C-10, les réserves 3 et 8 du § 5 et la cible de Haig-Simons (§ 3.C-10, point 8). Maquette indépendante de la règle C en équilibre partiel du bloc (`pe_hs.py`, `norm.py`, `horscible.py`, `decomp.py` ; γ^e et π_s lus sur la cible ; ν = 1, λ_V = 0,4, i_D = 3 %, g = π̄ = 2 %). Contrôles : dérive sans choc ≤ 4,4e−16 ; reproduit 0,98057, 0,91267, −2,27 % hors cible et la part de 0,628. Pas de maquette de la boucle conjointe : les chiffres de la question 1 sont ceux de `macro`, non remesurés par `jeu`.*

**0. Révision du § 7**
- **Q10 : accord à (a) retiré, ralliement à (c).** Sous (a), une oscillation de 17 à 19 tours croît de 1,71 % par tour, sans cause donnée par le joueur ni sortie possible : la partie serait injouable. Le reste de l'accord tient (une annonce ne déplace pas l'épargne le tour même).
- Conditions 2, 3 et 4 du § 7 révisées (Q2 ci-dessous) ; acceptation par le mainteneur au § 9.

**Q1. Embardée de la sur-commande en boucle conjointe — à clarifier** (mécanisme lisible ; ampleur et attribution non établies)
- **Récit en une phrase** : la capacité saturée fait passer la demande publique dans les prix ; la flambée ampute la richesse réelle ; les ménages freinent pour la reconstituer, d'où la récession. La cause se voit le tour suivant (prix au tour n + 1 par ξ).
- **Risque d'attribution** : après la fin du choc, le prix culmine 4 tours plus tard (tour 16), la production 9 (tour 21), le chômage 12 (tour 24). Le joueur imputera la récession à l'arrêt de G. Or, avec plans indexés (J7), il n'y a pas de récession : elle vient de l'effet d'encaisses réelles. La restitution doit montrer cette cause (décomposition, Q2).
- **Falaise non linéaire** (effet par point de choc, prix / production) : +1 % : 2,7 / 0,59 ; +5 % : 2,8 / 0,57 ; +10 % : 5,6 / 1,67. La rupture coïncide avec la saturation de N^pa ; elle n'est lisible que si la saturation est affichée comme signal précurseur (« plein emploi : main-d'œuvre épuisée », #52).
- **Proportionnalité** : une décision d'un an produit −16,65 % de production et +13,99 points de chômage, sans réponse de politique (π^e exogène, aucune banque centrale). Si cette ampleur subsistait au J4 avec politique endogène, doubler G serait un piège plutôt qu'un choix. Crédibilité économique : `macro` et `monnaie` ; verdict ludique reporté au J4, avec la fiche 8.
- **Signal précurseur** : le terme de reconstitution. Ordre de grandeur (hypothèse non mesurée) : un frein de 15 à 18 points de revenu, compatible avec le creux. Non vérifié : qu'il apparaisse avant le tour 21.
- **ψ_ξ, critère 8 (c) à rebours du jeu** : ψ_ξ = 0 échoue au seuil (borne jusqu'au tour 30) mais donne l'épisode le plus doux (+33,3 %, −2,9 %) ; ψ_ξ = 0,5 tient le seuil et donne la dépression. Le seuil ne se lit pas seul : publier l'ampleur à côté. Pas de modification du critère demandée.
- **Critère 11 (c)** non éprouvé en boucle conjointe : aucune demande non servie, les prix rationnent.
- **87 tours hors ±2 %** : ±2 % est la bande du test zéro, pas un seuil d'alerte ; ne pas afficher le ratio en anomalie ; afficher la demi-vie (18,8 tours dans la boucle).
- **Dimension maintenue** : G ×2 pendant 12 et 24 tours, critères écrits avant l'essai, au J4. Ajouts : G ×1,5 pendant 12 tours ; ψ_ξ ∈ {0 ; 0,5} tant que ψ_ξ n'a pas de source ; sortie progressive (G ramené en 12 tours) sous la forme O3.
- **Mesures publiées par scénario** : pic des prix et son tour ; creux de production et son tour ; pic de chômage ; durée de la borne d'emploi ; demande non servie ; terme de reconstitution maximal et son tour ; perte cumulée des tours 13 à 60 rapportée au gain des tours 1 à 12. Aucune exigence nouvelle.

**Q2. Ratio de richesse restitué — lisible, à deux conditions** (définition au tour ; mention « à la cible »)
- **D'abord le ratio de Haig-Simons**, V d'ouverture / (12 × YD^HS du tour). Niveau normal **1 an (ν) exactement**, à π̄ = 2 % comme à 10 % (mesuré : 1,00000). C'est la variable que lit la règle.
- **Lecture (e) de la condition 3 retirée** (1,0216 an) : sous la cible de Haig-Simons, elle donnerait 1,0216 à 2 % et 1,0638 à 10 %, une norme qui dépend de la cible.
- **Libellé** : « Richesse des ménages, en années de revenu » ; définition : « dépôts d'ouverture ÷ [12 × (revenu disponible du tour − érosion des dépôts au rythme de la cible d'inflation)] ; niveau normal 1 an ; exact quand l'inflation est à la cible ». La mention « à la cible » est obligatoire : pendant une embardée, YD^HS ne retranche que la cible, et « corrigé de l'inflation » serait faux.
- **Revenu par source (condition 1)** : ligne « érosion des dépôts (inflation cible) » = −π_s·V.
- **Ratio nominal en second**, « en années de revenu nominal » ; niveaux normaux 0,981 an à 2 %, 0,913 an à 10 %.
- **Hors cible, écart permanent** (cible 2 %, mesuré) : inflation 3 % : −2,27 % (−0,27 mois de consommation) ; 5 % : −6,44 % (−0,78 mois) ; 10 % : −15,16 % (−1,90 mois). Lisible comme un niveau (« surpris par l'inflation, les ménages restent sous leur épargne visée »), s'il est déclaré dans la définition ; il ne disparaît que si π^e s'adapte (fiche 8).
- **Condition 4 révisée** : (V − V\*)/C est remplacé par la **décomposition additive exacte du taux d'épargne du tour** (résidu mesuré 2e−16) : entretien γ^e·V/YD ; reconstitution (λ_V/n_a)(V\* − V)/YD ; revenu imprévu (YD − YD^e)/YD ; épargne forcée (C^plan − C)/YD. Exemple, transferts aux tours 1 à 12 : tour 1, revenu imprévu +0,99 point ; tour 2, reconstitution +0,36 ; tour 13, revenu imprévu −1,00 ; tour 14, reconstitution −0,12. La phrase du § 7 « dit le sens de la consommation à venir » est corrigée : le terme mesure le frein actuel.
- **Condition 2 révisée** : sous (c), le niveau normal du taux d'épargne se lit à la cible. À 2 % / 10 % : taux nominal 3,890 % / 10,557 %, dont maintien face à l'inflation 1,943 / 8,733 et épargne réelle 1,947 / 1,823 ; taux de Haig-Simons 1,985 % / 1,998 %.

**Q3. Part d'un transfert dépensée — lisible ; le seuil tient**
- **Critère 12 (d) et documentation : part propre au ménage**, en équilibre partiel (passer à la part dans la boucle déplacerait le critère après observation) : 0,627 (`macro`) ; 0,628 (cible nominale), 0,629 (Haig-Simons, 2 %), 0,621 (Haig-Simons, 10 %) dans la maquette de `jeu`. **Le seuil de 0,50 à 0,85 tient.**
- **Restitution (fiche du levier, J4) : les deux, sous deux noms** : « part dépensée par les ménages en 12 tours : 0,63 » ; « effet sur la consommation en volume, toutes rétroactions : 0,58 en 12 tours, 0,46 en 24 tours ». **Jamais la part en u.m.** (1,046) sous le nom « part dépensée ».
- **L'inflation rogne le transfert** : part en volume 0,578 / 0,464 / 0,484 (12, 24, 120 tours) ; à θ_H = 1 : 0,695 / 0,311 / 0,116, presque sans effet réel à 120 tours (point à joindre à #44).

**Décisions non résolues relevées par `jeu`** : lecture de π_s (exactitude de l'étiquette ; `jeu` suit la lecture stable) ; calibration de ψ_ξ (fiche 4, réserve 4) ; acceptation des conditions 2 à 4 révisées au § 9.

**Issue proposée** (création soumise au mainteneur) : « J4 — scénario de surchauffe publique en boucle conjointe (sur-commande, forme O3) », corps dans le compte rendu de la session (PR #43).

### Second additif de `jeu` (03/10/2026) : changement de cible et deux taux d'épargne

*Sources lues : § 6.5 (additif de `monnaie`), § 6.1 Q5 (définition du taux corrigé) et additif de `jeu` du § 7. Aucun scénario exécuté. Les chiffres +0,5543 % et +0,9776 % sont ceux de `monnaie` et `macro` ; `jeu` ne les a pas remesurés.*

**1. Un changement de π\* déplace la demande au tour même. Verdict : à clarifier pour la fiche 5, à revoir pour la fiche 8 si π\* devient un levier sans coût.**
- **Ce que voit le joueur.** Il annonce une désinflation, et la consommation monte de 0,55 % le tour même. C'est l'inverse de ce qu'il attend : une baisse de cible se lit comme un resserrement. Sans explication, le joueur ne peut pas comprendre ce comportement.
- **L'ampleur n'est pas le problème.** Elle reste modeste : environ la moitié de l'effet d'un transfert de 1 % du revenu disponible sur 12 tours. Le risque est que l'effet soit **gratuit et répétable**. Rien ne paie l'impulsion d'impact. Tant que l'effet net sur plusieurs tours n'est pas mesuré, rien n'exclut un aller-retour rentable : baisser π\* pour relancer, puis la remonter quand le frein de Fisher arrive (−1 % du revenu disponible par point au tour suivant). Ce serait une remise à zéro gratuite, contraire au principe « plusieurs approches viables ».
- **La fiche 5 déclare l'effet** (troisième ajout de `monnaie`). Le décrire de façon à le relier aux cases déjà affichées :
  - le niveau du ratio de richesse ne bouge pas : sa norme reste 1 an ;
  - l'impact passe par le terme d'entretien de la décomposition du taux d'épargne (γ^e·V/YD), qui baisse ;
  - la ligne « érosion des dépôts (inflation cible) » du revenu par source baisse elle aussi.
  
  Le joueur voit ainsi la cause (« les ménages prévoient de moins compenser l'érosion ») dans des cases qui existent déjà.
- **Essai demandé pour la fiche 8**, critères à écrire avant l'essai et à juger par `monnaie` :
  - (i) **marche** : π\* −1 point, avec la règle de taux endogène. Trajectoires de C, Y, π et i_D aux tours 1, 3, 12, 24 et 60. Publier l'effet cumulé sur C et Y aux tours 12 et 24, et le tour où il change de signe.
  - (ii) **aller-retour** : π\* −1 point au tour t, puis +1 point à t + k, pour k = 1, 3 et 12. La propriété attendue, à faire valider par `monnaie` : le gain cumulé de production ou de consommation sur 24 tours n'est pas significativement positif par rapport à la trajectoire sans changement. Sinon, il y a une stratégie dominante.
  - (iii) **même essai sous cible nominale** (+0,98 %), pour publier ce que coûte le choix de Haig-Simons.
- **Si l'aller-retour est rentable : options de conception pour la fiche 8.** Ce sont des choix de conception, à chiffrer en fidélité par `monnaie`, sans préférence de `jeu` à ce stade :
  - délai d'entrée en vigueur entre l'annonce et π\* effectif ;
  - fréquence de révision limitée, par exemple annuelle ;
  - coût de crédibilité à chaque révision, qui renverrait à la lecture (b) et à la clause C26.
- **J4, fiche du levier π\*.** Le signe et l'ampleur à l'impact, puis l'effet net à 12 tours, sont affichés **avant** la validation de l'annonce. Une annonce de désinflation ne doit jamais être présentée comme restrictive à l'impact.
- **Régimes B, D et E.** Tant que la π\* lue par les ménages n'est pas définie, la fiche du levier n'existe pas dans ces régimes. Le levier n'y est pas proposé.

**2. Les deux taux d'épargne. Verdict : lisible avec deux noms distincts. Le mot « taux d'épargne » n'est jamais affiché seul.**
- **« Taux d'épargne visé (à la cible) »** : il dit ce que les ménages cherchent à faire (comportement).
  - Définition affichée : « 1 − consommation du tour ÷ (revenu disponible du tour − érosion des dépôts au rythme de la cible d'inflation) ; fenêtre : le tour ; niveau normal environ 2 % (croissance × 1 an de richesse) ; exact quand l'inflation est à la cible ».
  - Il partage son dénominateur YD^HS avec le ratio « Richesse des ménages, en années de revenu ».
  - Valeurs de référence : 1,985 % à 2 %, 1,998 % à 10 % (§ 6.1, Q5).
  - Le détail de la décomposition additive (entretien, reconstitution, revenu imprévu, épargne forcée) s'ouvre sous ce taux.
- **« Taux d'épargne constaté, net de l'inflation »** : il dit ce qu'elle a effectivement fait (constat).
  - Définition affichée : « 1 − consommation sur 12 tours ÷ (revenu disponible sur 12 tours − perte réelle des dépôts due à la hausse des prix mesurée) ; fenêtre : 12 tours glissants » (§ 6.1, Q5, point 1).
- **Raccord des deux, pour rendre l'écart explicable.** Ajouter au revenu par source une ligne « érosion imprévue des dépôts (inflation au-dessus de la cible) », égale à −(π mesurée − π_s)·V, sous la ligne « érosion des dépôts (inflation cible) ». À fenêtre égale, l'écart entre les deux taux se lit dans cette ligne. Message du tour, hors cible : « l'inflation dépasse la cible : les ménages épargnent moins qu'ils ne le croient ».
- **Fenêtres différentes** (le tour contre 12 tours) : à déclarer dans les deux définitions. Variante plus simple, à arbitrer par `app-review` au J4 : afficher les deux taux sur 12 tours dans le tableau principal, et le taux visé du tour dans la décomposition seulement.
- **Ordre d'affichage** : le taux visé, puis le taux constaté, puis le taux nominal (« taux d'épargne nominal, sans correction de l'inflation »), puis le rendement réel des dépôts i_D − π. Cet ordre est cohérent avec le ratio de richesse, Haig-Simons d'abord.

**Issue proposée** (création soumise au mainteneur) : « Fiche 8 — essai d'aller-retour de la cible π\* (pas de stimulant gratuit à l'impact) », corps dans le compte rendu de la session (PR #43).

## 8. Décision du mainteneur

- **Numéro** : M27 (reporté dans `docs/feuille-de-route.md`, § 4), prise le même jour que M28 (fiche 6), décisions par paires.
- **Date** : 03/10/2026.
- **Option retenue** : **C**, cible de richesse avec terme de tendance, ménage représentatif, avec la recommandation finale du § 5 telle quelle :
  - (a) Q10 : **lecture (c)**, l'inflation du terme de tendance et de la cible lue sur la **cible déclarée π\*** (paramètre ou levier de la fiche 8), jamais sur π̄ ; γ^e = [(1 + g)(1 + π\*)]^{1/n_a} − 1 ; la lecture (a) et la variante h sont écartées ; une réouverture vers (b) ne passe que par la clause **C26** (fiche 8), par une décision citant M27 ;
  - (f) **cible de richesse sur le revenu de Haig-Simons** : V\* = ν·n_a·(YD^e − π_s·V_H), π_s = (1 + π\*)^{1/n_a} − 1, une seule lecture de l'inflation pour γ^e et π_s ;
  - (b) à (e) : les lectures recommandées au § 5 (plafond du plan en phase 2, seuil libre déclaré ; **B_H ≡ 0** au socle ; canal du taux rentier seul ; taux d'épargne restitué nominal et corrigé, sous deux libellés distincts) ;
  - revenu lu YD_{t−1} avec tendance (Q2 (i)) ; variante D notée pour le J4.
- **Motifs** : le mainteneur a retenu la recommandation concordante de `macro`, de `monnaie` (§ 6.5) et de `jeu` (§ 7). Motifs dans ses propres mots : à compléter par le mainteneur s'il le souhaite.
- **Conditions et réserves** : les dix réserves du § 5, avec leurs critères écrits avant l'essai ; les conditions de `monnaie` (C14 à C26, dont C26) ; les conditions de restitution de `jeu` (§ 7 et ses deux additifs : ratio « Richesse des ménages, en années de revenu » sur YD^HS d'abord, décomposition additive du taux d'épargne, part propre au ménage pour le critère 12 (d), deux taux d'épargne nommés) ; C2 devient aussi une condition de la fiche 5 (hors cible, λ_V fixe l'état d'arrivée : continuum déclaré).
- **Ce qui est écarté et pourquoi** : A et B (critère 4, strates, plafond) ; S à α libres (critère 4) ; R1 (hors domaine) ; Q10 (a), explosive en boucle conjointe (§ 3.C-10) ; π_s sur π_{t−1}, explosive à θ_H = 1 ; variante h (frontière de stabilité, non calibration sourcée) ; cible nominale (superneutralité moindre).
- **Issues liées**, créées sur accord du mainteneur : #53 (surchauffe publique, J4), #54 (aller-retour de π\*, fiche 8), #58 (instabilité de la lecture (a)), #59 (coquille du critère 4 (ii), corrigée au § 2).

## 9. Conséquences de la décision

*Rédigé par `macro` (expert pilote) le 03/10/2026, d'après :*
- *M27 (§ 8) et M28 (fiche 6, § 8) ;*
- *l'ADR 0008 : lecture (G), registre de 13 niveaux ;*
- *les conditions C14 à C26 de `monnaie` (§ 6.3, § 6.5) ;*
- *les conditions de `jeu` (§ 7 et ses deux additifs).*

*« Hk » désigne la ligne k du tableau du § 9.1. Conversions (ADR 0008, I.1) : linéaire pour les taux d'intérêt et les vitesses ; géométrique pour la croissance et l'inflation (g, π\*). Chiffres remesurés le 03/10/2026 (§ 9.7), commandes au compte rendu de `macro`.*

### 9.1 Labels d'équation

**Au jalon J1, aucun label** (#41, jalon 4). `sec:menages` est rédigée en `equation*`, dans des encadrés `proposee` qui citent M27. **Les labels sont créés au J3** avec `src/nations/blocs/menages.py` (radical `menages`) : `coder` pose une balise par label, puis `docwriter` retire l'encadré et pose le label dans le même passage.

**Notation proposée pour la spécification** (critère 15, exigence). Les symboles provisoires du § 3.0 sont repris, sauf trois :

| Fiche (§ 3 à 8) | Spécification (proposé) | Motif |
|---|---|---|
| π_s | π^{∗,pas} = (1 + π\*)^{1/n_a} − 1 | s est un indice réservé du cadre (secteur institutionnel, `tab:symboles`, l. 1150). La notation x^pas existe déjà (l. 1143) : elle est à redéfinir « selon la nature du taux » (ADR 0008) |
| λ_V | λ_H | λ_V et λ_v (ventes anticipées de la fiche 2, 12 occurrences dans le `.tex`) ne se distinguent que par la casse |
| ν | ν_H | symétrie avec ν_F (dépôts visés des entreprises, fiche 6) |

Sont conservés :
- C^plan (budget de consommation) et C^règle (plan de la règle avant bornes) ;
- YD, YD^e, V^∗_H ;
- Γ^e et γ^e, symboles à partager avec la fiche 6, où Γ̂ désigne la même grandeur (§ 9.8, contrat 3).

Contrôle `grep -c -F` sur le `.tex` : `\nu_H`, `\lambda_H`, `\phi`, `\zeta`, `\eta`, `\gamma`, `\Gamma` et `\pi^\ast` donnent 0 occurrence ; `\kappa` en donne 8. Le symbole κ est pris (κ_j) : le coefficient de richesse de la forme réduite reste donc écrit en clair, sans symbole. Le choix final revient à `docwriter`.

| Id. | Label (J3) | Ce que l'équation détermine | Équation | Phase | Statut | Provenance | Couche |
|---|---|---|---|---|---|---|---|
| H1 | `eq:menages-croissance-attendue` (ou `eq:moteur-croissance-nominale-attendue`, § 9.8, contrat 3) | facteur de croissance nominale attendue et inflation cible par pas | Γ^e_t = (1 + g)^{1/n_a}·(1 + π\*_t)^{1/n_a} ; γ^e_t = Γ^e_t − 1 ; π^{∗,pas}_t = (1 + π\*_t)^{1/n_a} − 1. Chaque facteur est rendu par `eq:moteur-conversion-croissance` (ADR 0008, I.3) et n'est jamais recalculé | 2 (π\*_t lu en phase 1 ; date en suspens, § 9.8) | choix de conception | M27 (a) et (f) ; § 3.N-3 (additif) ; § 6.5 ; ADR 0008, I.1 | `blocs/`, ou `moteur/` si la grandeur est partagée avec la fiche 6 |
| H2 | `eq:menages-revenu-attendu` | revenu disponible attendu du pas | YD^e_t = Γ^e_t·YD_{t−1} | 2 | approchée (forme SIMEX, YD^e = YD_{−1}) ; terme de tendance : choix de conception | Q2 (i), § 3.N-2 ; SIMEX (reproduction PKSFC, § 3.0) ; M27 | `blocs/` |
| H3 | `eq:menages-richesse-visee` | richesse visée, sur le revenu de Haig-Simons attendu | V^∗_{H,t} = ν_H·n_a·(YD^e_t − π^{∗,pas}_t·V_{H,t}) | 2 | choix de conception | cible implicite α_3 = (1 − α_1)/α_2 de SIM (reproduction PKSFC) ; revenu de Haig-Simons (DISINF, INSOUT, reproduction sfcr, ouvrage non lu) ; § 3.C-10, point 8 ; § 6.1, Q2, point 3 ; M27 (f) | `blocs/` |
| H4 | `eq:menages-plan-consommation` | plan de la règle, avant bornes | C^règle_t = YD^e_t − γ^e_t·V_{H,t} − (λ_H/n_a)(V^∗_{H,t} − V_{H,t}) | 2 | approchée (ajustement partiel vers une cible de stock) ; terme d'entretien γ^e·V : choix de conception | § 3.C, point 1 ; même construction que `sec:production-visee` (l. 617) ; M27 | `blocs/` |
| H5 | `eq:menages-budget-consommation` | budget de consommation (« budget de consommation » de `tab:phases`, ligne 2) | C^plan_t = min{D_{H,t}, max{0, C^règle_t}} | 2 | choix de conception | § 3.N-6, lecture (a) ; M27, lecture (b) ; #38, lecture (ii) | `blocs/` |
| H6 | `eq:menages-consommation` | consommation exécutée, ligne 1 (ménages −C_t, entreprises « courant » +C_t) | C_t = p_t·v_{H,t} | 5, après les blocs 4 et 2 | dérivée (ligne 1 du cadre) | M22 ; M24 (g) ; critère 1 (a) | `blocs/` |
| H7 | `eq:menages-revenu-disponible` | revenu disponible du pas, porté en variable d'état pour t + 1 | YD_t = Σ_{ℓ ∈ {5, 6, 7, 10, 11a, 14, 15}} f_{ℓ,H,t} = WB_t + Tr_t − T_{H,t} + i_D·D_{H,t}/n_a + i_B·B_{H,t}/n_a + Div_{F,t} + Div_{Bk,t}. Ce sont les montants exécutés, lus au grand livre, jamais recalculés | 7 (§ 9.4 ; lecture soumise, § 9.8, contrat 1) | dérivée (colonne des ménages de `tab:matrice-flux`) | M22 ; § 3.N-1 ; critère 10 | `blocs/` |

Les sept labels respectent l'expression régulière de `CONVENTIONS.md` § 2.1 (contrôle exécuté, § 9.7).

**Forme réduite** (`equation*`, sans label) : C^règle = α_Y·YD^e + (λ_H/n_a − γ^e + ν_Hλ_H·π^{∗,pas})·V_H, avec α_Y = 1 − ν_Hλ_H. ν_H fixe le ratio de richesse ; λ_H fixe la propension d'impact.

**Sans label** :
- V_H = D_H + B_H : le noyau la calcule deux fois, par le stock et par les flux (phase 9) ; ΔV_H = YD − C est une identité contrôlée par le noyau ;
- ligne 19a-ménages : aucune équation, car B_H ≡ 0 ;
- YD^HS, les trois taux d'épargne, la décomposition, les ratios et la demande non servie cumulée : couche `observation/` (§ 9.4).

**Ajout de rédaction à viser par le mainteneur** : le plancher max{0, ·} de H5 n'était pas écrit au § 3. Sans lui, un YD_{t−1} négatif (impôts supérieurs aux revenus) donnerait un plan négatif, donc une demande d_{H,t} < 0 que le rationnement proportionnel de N6 ne traite pas. C'est une contrainte de conservation sans paramètre (#38, lecture (ii)). Elle est inactive à l'état stationnaire, et la condition de domaine du § 9.2 (coefficient de richesse positif) l'y maintient tant que YD^e ≥ 0.

**Choix d'implémentation, au choix de `coder` sous visa de `macro`** (trajectoires identiques dans tous les cas) :
- (i) le propriétaire de H1, à fixer avec la fiche 6 ;
- (ii) C^règle_t est rendu comme variable nouvelle du pas, et non comme état : la décomposition du § 9.4 le lit sans le recalculer ;
- (iii) H7 lit le grand livre ; les intérêts n'y sont jamais recalculés (localité).

### 9.2 Paramètres

À porter dans `tab:calibration` au J1, sans `\code{}` avant le code. Les noms sont des propositions.

| Symbole | Nom proposé | Valeur | Unité (ADR 0008, I.3) | Source | Équation |
|---|---|---|---|---|---|
| ν_H (ν de la fiche) | `richesse_visee_menages` | 1 (indicative ; réserve 7 : calibration à instruire au J3) | an, en années de revenu disponible de Haig-Simons. C'est un niveau, ni taux de flux ni taux de croissance : le facteur n_a est un changement d'unité. Le type est le même que σ_j (fiche 2) et ν_F (fiche 6) | choix de conception, M27 ; aucun ordre de grandeur lu sur la richesse **liquide** des ménages (§ 3.0 : Fed Z.1 non lue, BCE inaccessible) | H3 |
| λ_H (λ_V de la fiche) | `vitesse_richesse_menages` | 0,4 (indicative ; réserve 7) | par an, taux de flux (vitesse, conversion linéaire λ_H/n_a), λ_H ≤ n_a | choix de conception, M27. Fidélité déclarée : l'effet richesse lu (Carroll, Otsuka et Slacalek, 2006 : 2 à 10 cents par an) porte sur une richesse peu liquide (§ 3.C, point 6) | H4 |
| plafond du budget | — (aucune valeur numérique) | base D_{H,t}, dépôts d'ouverture | u.m. | choix de conception, M27, lecture (b) ; motif : payable par construction sans réordonner la phase 5 (M24) | H5 |

**Point d'interprétation** (`CONVENTIONS.md` § 2.4) : une borne à seuil libre « est un paramètre déclaré ». Le seuil est ici la **base** D_{H,t}, et non un nombre. Deux lectures :
- (i) une entrée de `tab:calibration` sans valeur numérique, « base D_{H,t} », avec le motif ;
- (ii) un paramètre fictif φ = 1, fraction des dépôts d'ouverture mobilisable, sans source.

Je recommande (i). Le mainteneur tranche.

**Grandeurs lues, qui ne sont pas des paramètres du bloc** :
- g, dérivée : (1 + g_pr)(1 + g_N) − 1 (ADR 0008, I.5 ; blocs 2 et 3) ;
- π\*, cible d'inflation, paramètre ou levier du bloc 8, de type « par an, taux de croissance », à source unique (§ 9.8, contrat 2) ;
- n_a (cadre).

**Conditions déclarées, contrôlées au chargement, jamais par écrêtage** :
- 0 < ν_Hλ_H < 1, d'où α_Y > 0 (R1 est hors domaine) ;
- 0 < λ_H ≤ n_a ;
- π\* > −1 ;
- **coefficient de richesse positif** : λ_H/n_a + ν_Hλ_H·π^{∗,pas} > γ^e. Avec YD^e ≥ 0, il garantit C^règle ≥ 0. À ν_H = 1, il tient pour π\* < 85,12 % si λ_H = 0,4, pour π\* < 24,94 % si λ_H = 0,2, et pour π\* < 2 760 % si λ_H = 0,8. Il borne le domaine admissible du levier π\* (fiche 8, J4).

**Seuil de calibration de `jeu`** (critère 12 (d) : part propre au ménage en 12 tours dans [0,50 ; 0,85]). Remesuré sous la règle décidée, il demande 0,080 ≤ λ_H ≤ 0,634 à ν_H = 1. La calibration (0,628) est à 0,22 point de part sous la borne haute de λ_H.

**Ce qui n'est pas un paramètre** :
- α_Y, V^∗_H, Γ^e, γ^e et π^{∗,pas}, qui sont dérivés ;
- YD_{−1} et D_{H,0}, valeurs de l'état initial résolu (§ 9.7) ;
- θ_H, grandeur de diagnostic de l'instruction, qui résulte des fiches 6 et 9 ;
- χ (variante D, J4).

### 9.3 Ce qui reste paramétrable après la décision

**Sans rouvrir M27** (calibration au J3, visa de l'expert pilote) :
- ν_H et λ_H, dans leurs conditions et dans le seuil de `jeu` (réserve 7, issue proposée au § 9.9) ;
- la valeur de π\* (fiche 8).

**Par une décision M-m citant M27** :
- Q10 vers (b), par la clause **C26** (fiche 8) : C1 tient ; boucle complète de rayon < 1 sur la grille ; contrôle de séparation ;
- la **variante D** à deux types, avec le levier de transfert ciblé (J4, Q11) ; χ est calibré sur une source lue (Kaplan, Violante et Weidner : environ 20 % du revenu) ;
- une demande de titres de Tobin ou une part fixe (fiche 9 ou J6, avec `monnaie`). Retirer ou ajouter des lignes demande en outre une décision citant M22 ;
- un canal de substitution, seulement sur le fait nouveau défini par C14. La forme propre à C est ν_H(i_D − π) (`monnaie`, § 6.1, Q3, point 4), non PCEX2 ;
- le plafond en phase 5 (lecture (b) du § 3.N-6), qui exige aussi une décision citant M24 ;
- une cible fonction du taux réel, ou un actif de fuite (J6, C18) ;
- un comportement ricardien (critère 10 (d)) ;
- R2, le revenu du pas courant lu par le plan (décisions citant M22 et M24) ;
- le crédit aux ménages (J6, M22).

**Aucun drapeau de mode** (ADR 0002).

### 9.4 Interfaces

**Phases, lectures et écritures du bloc 5** :

| Phase | Le bloc 5 lit | Le bloc 5 écrit, ou propose au noyau |
|---|---|---|
| 1 | — (π\*_t est lu par le moteur parmi les leviers et paramètres) | — |
| 2 | ouverture : D_{H,t}, B_{H,t} (≡ 0), YD_{t−1} ; phase 1 : π\*_t ; g, ν_H, λ_H | Γ^e_t, γ^e_t, π^{∗,pas}_t (H1, si le propriétaire est `menages`) ; YD^e_t, V^∗_{H,t}, C^règle_t, C^plan_t (H2 à H5) |
| 5, après les blocs 4 et 2 | p_t, v_{H,t} | ligne 1, C_t (H6) |
| 6 | — (les lignes 5, 6, 7, 10, 11a, 14 et 15 sont exécutées par les blocs 3, 9, 7 et 6) | rien |
| 7 | grand livre : f_{ℓ,H,t} des phases 4 et 6 | YD_t, variable d'état du pas suivant (H7) ; aucune souscription (B_H ≡ 0) |
| 9 | — | — (le noyau calcule V_H par le stock et par les flux) |

- **Aucune lecture** de WB_t, N\*, y\*, G^plan, I^plan, p_t en phase 2, ni du registre de l'indice. La matrice des lectures est triangulaire.
- **Phase 7** : aucun ordre interne requis. Rien ne lit YD_t dans la phase, et H7 ne lit que les phases 4 et 6, conformément à la colonne « Lisent » de `tab:phases` (ligne 7 : « ouverture, phases 1, 5 et 6 »). L'ordre de C25 (État, puis banque centrale, puis banque) est inchangé. Q5 est sans objet.
- **Variables d'état** : une seule, YD_{t−1} (u.m. par pas ; valeur stationnaire YD_t/Γ̄). Aucun registre, aucun tirage.
- **Plan sans base de prix** (constat de la fiche 4, § 9.8) : le plan est en u.m. et ne lit aucun prix. À plan donné, la demande en volume a une élasticité de −1 au prix du pas (contrat de M24).
- **Priorité des paiements** (Q7) : ligne 1 en phase 5, puis ligne 7 en phase 6. Après la phase 5, D_H ≥ WB_t ≥ 0, puisque C^plan ≤ D_{H,t}. Une insuffisance ne peut venir que de la ligne 7 (constat transmis à la fiche 9, § 9.8).

**Interfaces avec les autres blocs** :

| Bloc | Grandeur | Sens | Phase | Contrat ou condition |
|---|---|---|---|---|
| 2 production | C^plan_t → d_{H,t} = C^plan_t/p_t ; v_{H,t} en retour | écrit, puis lit | 2 ; 5 | M24 (g) ; demande non servie C^plan − C restituée ; m_H d'impact 0,4808, de long terme 0,7922 (θ_H = 0,8, i_D = 3 %) ou 0,9902 (θ_H = 1) → réserve 3 de la fiche 2 |
| 3 travail | WB_t (ligne 5) ; g_N, par g | lit (H7 ; H1) | 4 → 7 ; paramètre | population active au bloc 3 (M25 (d)) ; Q9 sans objet |
| 4 prix | p_t, par la ligne 1 seulement ; P_t et P_{t−1} pour la restitution | lit | 5 ; restitution | **aucune lecture du registre** (M27, lecture (c)) ; aucune base de prix dans le plan |
| 6 investissement | Div_{F,t} (ligne 14, dividende résiduel, F3) ; Γ^e, partagé avec Γ̂ | lit (H7) ; grandeur commune | 6 → 7 ; 2 | θ_H effectif fixé par F ; état stationnaire conjoint (fiche 6, § 3.E) : V_H = ν_H n_a YD^HS ; L − D_F par F ; l'État porte le solde ; C36, C37 |
| 7 banque | i_D, ligne 10 ; Div_{Bk,t}, ligne 15 | lit (H7) | 6 → 7 | C19 (19a-banque, reliquat déclaré) ; C20 (règle de i_D) ; C21 (date de Div_Bk) ; C22 ; les dépôts des ménages sont un passif de la banque |
| 8 banque centrale | π\* (source unique) ; ligne 19b-ménages nulle | lit (H1) | 1 → 2 | C14 (signe) ; C15 (superneutralité, avec #49) ; C16 révisée (élasticité du plan à π\* : +0,5543 % par point de baisse) ; C17 (assouplissement quantitatif à la banque seule) ; C18 (J6) ; C26 ; régimes B, D et E : π\* lue par les ménages à définir (fiche 8, J5) ; date de π\* (§ 9.8, contrat 2) |
| 9 État et dette | T_H (ligne 7), Tr (ligne 6) ; i_B (ligne 11a, nulle) ; 19a-ménages (nulle) | lit (H7) | 6 → 7 | forme symbolique : la fiche 9 choisit ses règles sans réécrire la fiche 5 ; aucune anticipation ricardienne ; C23 à C25 ; fermeture B/PIB (fiche 6, § 3.E) ; insuffisance de dépôts pour la ligne 7 (§ 9.8) |

**Leviers qui transitent par le bloc** (aucun levier propre, Q11). Les délais perçus sont ceux de la maquette de `jeu`, sous la cible nominale ; ils sont à remesurer au J4 (§ 9.6).

| Levier | Indicateur | Délai mécanique (tours entiers) | Délai perçu (premier tour où l'écart de C atteint 0,1 %) | Contrepartie visible le même tour |
|---|---|---|---|---|
| Transferts | C ; revenu par source ; décomposition du taux d'épargne (revenu imprévu) | ligne 6 au tour n, plan au tour n + 1 | tour 2 | dépôts des ménages ; ligne « transferts » |
| Impôts sur les ménages | idem, de signe opposé | n + 1 | tour 2 | dépôts ; ligne « impôts » |
| Dépense publique | C | revenu au tour n + 1 (emploi), plan au tour n + 2 (*Annotation du 04/10/2026 (revue finale de `macro`, mesure ; décision inchangée) : dividende au tour n, plan au tour n + 1 depuis M28)* | tour 5 (G +1 %) | stocks, dépense exécutée (fiche 2) |
| Taux (i_D) | C ; ligne « intérêts reçus » | ligne 10 au tour n, plan au tour n + 1 ; **signe +** (canal rentier) | tour 2 (+0,25 point) | intérêts reçus au tour n |
| Cible π\* | plan ; terme d'entretien de la décomposition ; ligne « érosion des dépôts (inflation cible) » | **0 ou 1 tour selon la date de π\*** (§ 9.8, contrat 2) ; une baisse d'un point relève le plan de +0,5543 % | — | érosion cible en baisse |

La fiche 2, § 9.4, est confirmée : impôts sur les ménages → ventes au tour n + 1.

**Grandeurs restituées au tour** (couche `observation/`). Les niveaux normaux sont publiés par le script d'état stationnaire, à g = π\* = π̄ = 2 % et n_a = 12 (valeurs à 10 % entre parenthèses).

| Grandeur | Définition | Unité | Dénominateur | Fenêtre | Niveau normal |
|---|---|---|---|---|---|
| Consommation en volume | v_H ; glissement v_{H,t}/v_{H,t−12} − 1 | u.v. ; par an | v_{H,t−12} | le tour ; 12 tours | g = 2,00 % |
| Dépense demandée, exécutée, taux d'exécution | C^plan ; C ; C/C^plan | u.m. ; fraction | C^plan | le tour | 1 |
| Demande non servie des ménages | C^plan − C, en u.m. et en fraction de C^plan | u.m. ; fraction | C^plan | le tour | 0 |
| Demande non servie cumulée de l'épisode (épargne forcée) | Σ_épisode(C^plan − C)/C^plan_t. L'épisode est la suite maximale de tours où C^plan − C > 1e−12·C^plan | mois de dépense demandée | C^plan du tour | l'épisode | 0 |
| Revenu disponible, réel et par source | YD ; (YD_t/P_t)/(YD_{t−12}/P_{t−12}) − 1. Lignes : salaires (5), transferts (6), impôts (7), intérêts sur dépôts (10), intérêts sur titres (11a, nulle), dividendes des entreprises (14), dividendes de la banque (15). Deux corrections **sans ligne de la matrice** : « érosion des dépôts (inflation cible) » = −π^{∗,pas}·V_{H,t} ; « érosion imprévue des dépôts (inflation au-dessus de la cible) » = −(P_t/P_{t−1} − 1 − π^{∗,pas})·V_{H,t}. Contributions additives sur 12 tours : (X_{k,t} − X_{k,t−12})/YD_{t−12} | u.m. ; par an | YD_{t−12} | le tour ; 12 tours | g = 2,00 % (réel) |
| **Taux d'épargne visé (à la cible)** | 1 − C_t/(YD_t − π^{∗,pas}·V_{H,t}) | fraction | YD^HS du tour | le tour | 1,9852 % (1,9977 %) |
| **Taux d'épargne constaté, net de l'inflation** | 1 − Σ12 C/Σ12 [YD − (P_t/P_{t−1} − 1)·V_{H,t}] (`monnaie`, § 6.1, Q5) | fraction | revenu net de la perte mesurée, sur 12 tours | 12 tours | 1,9852 % (1,9977 %), égal au précédent sous C2 |
| Taux d'épargne nominal, sans correction de l'inflation | 1 − Σ12 C/Σ12 YD ; dont maintien face à l'inflation π^{∗,pas}V/YD et épargne réelle (γ^e − π^{∗,pas})V/YD | fraction | YD sur 12 tours | 12 tours | 3,8900 % = 1,9434 + 1,9466 (10,5565 % = 8,7333 + 1,8232) |
| Rendement réel des dépôts | i_D − π, π étant le glissement annuel (r = i − π du cadre ; #49) | par an | — | le tour | i_D − π̄ |
| **Richesse des ménages, en années de revenu** | V_{H,t}/[12·(YD_t − π^{∗,pas}·V_{H,t})] ; mention « à la cible » obligatoire | an | 12 × YD^HS du tour | le tour | **ν_H = 1 an exactement** sous C2. Hors cible, écart permanent déclaré (§ 9.7) |
| Richesse en années de revenu nominal | V_{H,t}/(12·YD_t) | an | 12 × YD du tour | le tour | 0,980566 (0,912667) |
| Composition dépôts / titres | B_H/V_H | fraction | V_H | — | **hors du tableau de bord** tant que B_H ≡ 0 |

**Décomposition additive exacte du taux d'épargne du tour** (condition 4 révisée de `jeu`). Avec Δ^plaf = C^règle − C^plan (terme nul hors activation d'une borne) :
- 1 − C/YD^HS ≡ [(γ^e − π^{∗,pas})V + (λ_H/n_a)(V^∗ − V) + (YD − YD^e) + Δ^plaf + (C^plan − C)]/YD^HS ;
- 1 − C/YD ≡ [π^{∗,pas}V + (γ^e − π^{∗,pas})V + (λ_H/n_a)(V^∗ − V) + (YD − YD^e) + Δ^plaf + (C^plan − C)]/YD.

Les termes se lisent dans l'ordre : maintien face à l'inflation (cible) ; entretien réel ; reconstitution ; revenu imprévu ; borne ; épargne forcée.

Le second additif de `jeu` accroche la décomposition au taux visé, dont le dénominateur est YD^HS. Les quatre termes de son premier additif portaient sur YD. Les deux identités ci-dessus sont exactes, mais le choix de présentation revient à `jeu` et à `app-review` (J4). La fenêtre « le tour » du taux visé et la fenêtre de 12 tours du taux constaté sont déclarées dans les définitions (variante plus simple : `jeu`, second additif, point 2).

### 9.5 Conditions de `jeu` (§ 7 et additifs, retenues par M27) et mise en œuvre

1. **Revenu disponible décomposé par source**, au tour et sur 12 tours, en contributions additives.
   *Mise en œuvre* : § 9.4, avec les deux lignes d'érosion des additifs. Ce sont des corrections de restitution, non des flux.
2. **Taux d'épargne**, révisé deux fois : taux visé (à la cible), taux constaté net de l'inflation, taux nominal (décomposé en maintien et épargne réelle), puis rendement réel des dépôts, dans cet ordre. Le mot « taux d'épargne » n'est jamais affiché seul.
   *Mise en œuvre* : § 9.4 ; niveaux normaux à la cible, publiés par le script.
3. **Richesse en années de revenu sur YD^HS d'abord**, niveau normal 1 an, mention « à la cible » ; le ratio nominal en second. La lecture (e) est retirée pour ce ratio.
   *Mise en œuvre* : § 9.4. **Point d'interprétation** (§ 9.8, contrat 6).
4. **Décomposition additive exacte du taux d'épargne du tour**, à la place de (V − V^∗)/C.
   *Mise en œuvre* : identités du § 9.4, complétées du terme de borne Δ^plaf, sans lequel l'identité n'est pas exacte quand le plafond ou le plancher joue.
5. **Demande non servie cumulée de l'épisode**, en mois de consommation.
   *Mise en œuvre* : § 9.4, avec la définition de l'épisode, qui manquait.
6. **Composition dépôts / titres hors du tableau de bord** sous B_H ≡ 0.
   *Mise en œuvre* : § 9.4.
7. **Tableau levier → indicateur → délai → contrepartie**, avec le délai perçu ; signe + du taux, gagnants et perdants.
   *Mise en œuvre* : § 9.4 ; ligne π\* ajoutée, son délai étant en suspens.
8. **Signe net du taux** sur la demande totale à 12 et à 36 tours, publié avant l'ouverture du levier de taux.
   *Mise en œuvre* : #56 (J4).
9. **Sur-commande au J4** :
   - G ×2 pendant 12 tours et pendant 24 tours ; G ×1,5 pendant 12 tours ;
   - ψ_ξ ∈ {0 ; 0,5} ;
   - sortie progressive en forme O3 ;
   - mesures publiées par scénario (§ 7, additif, Q1).

   La gratuité de la commande non servie est supprimée, ou rendue visible et coûteuse.
   *Mise en œuvre* : #53 ; § 9.6 ; fiche 9.
10. **Persistance d'une impulsion de demande** : l'écart de production revient sous la moitié de son pic en au plus 60 tours.
    *Mise en œuvre* : § 9.6 (J3, à la fermeture de #44).

Points supplémentaires des additifs :
- l'**effet d'un changement de π\*** est déclaré par les cases existantes : terme d'entretien et ligne d'érosion cible ;
- la part dépensée est restituée **sous deux noms**, jamais en u.m. sous le nom « part dépensée » :
  - « part dépensée par les ménages en 12 tours » (part propre, 0,63) ;
  - « effet sur la consommation en volume, toutes rétroactions » ;
- l'essai d'aller-retour de π\* relève de #54 (fiche 8) ;
- la variante D est testée identique à C sans transfert ciblé (J4).

**Seuil du critère 12 (d)** : M27 retient la grandeur, la part propre au ménage. L'**adoption explicite** du seuil [0,50 ; 0,85] proposé par `jeu` reste à confirmer par le mainteneur avant le J3 (§ 9.6).

### 9.6 Tests attendus

Chaque test énonce une propriété avec un seuil écrit avant l'essai (réserves 1 à 10 du § 5). « Appel direct » : la fonction du bloc est appelée seule, sans le programme entier.

| Jalon | Test | Propriété | Seuil |
|---|---|---|---|
| J3 | État stationnaire (réserve 1 ; critère 3) | Un pas sans choc depuis l'état résolu laisse YD_{t−1} sur son sentier (facteur Γ̄), V_{H}/(n_a·YD^HS) = ν_H, V^∗_H = V_H et C^plan = C^règle. Cas π\* = π̄ ∈ {0 ; 2 % ; 10 %}, n_a ∈ {4 ; 12 ; 52}. Valeurs de contrôle de V/(n_a·YD) = ν_H/(1 + ν_H n_a π^{∗,pas}) : 0,980535 / 0,980566 / 0,980578 (2 %) ; 0,912030 / 0,912667 / 0,912911 (10 %) ; ν_H exactement à 0 % | 1e−10 relatif |
| J3 | Revenu disponible par le grand livre (critère 1) | YD_t égale la somme des montants exécutés des lignes 5, 6, 7, 10, 11a, 14 et 15 de la colonne des ménages ; V_{H,t+1} − V_{H,t} = YD_t − C_t | 1e−12 × S |
| J3 | Identité, cas à 90 % (critère 1 ; § 3.N-7) | D_H = 1 196,6 par le stock et par les flux ; le budget non dépensé, 9,6, reste en D_H | 1e−12 × S |
| J3 | Lecture de l'inflation (séparation ; #58 ; C16 révisée) | Appel direct, deux ouvertures qui ne diffèrent que par le registre de l'indice : C^plan identique. Le bloc ne lit que π\* | écart nul (exact) |
| J3 | Vitesses (critère 4 ; réserve 2), sous C2 | Blocs 2 à 5, π^e = π\* exogène ; G +1 % pendant 12 tours ; branches λ_H ×0,5 et ×2 : écart de V/(n_a·YD^HS), V/(n_a·YD), du taux d'épargne nominal et de C/YD | ≤ 1e−6 relatif après 720 pas |
| J3 | Continuum hors C2 (réserve 2 ; déclaré) | Bloc 5 seul, revenus hors intérêts croissant au facteur [(1 + g)(1 + π)]^{1/n_a}, avec π = 3 % et 10 % et π\* = 2 %. Après convergence, V/(n_a·YD) = [1 − (1 − ν_Hλ_H)Γ^e/Γ]/[n_a(Γ − Γ^e) + λ_H(1 + n_aν_Hπ^{∗,pas})]. Écarts à la lecture exacte publiés pour λ_H = 0,2 / 0,4 / 0,8 : −3,35 / −1,29 / −0,22 % (3 %) et −19,76 / −8,58 / −1,56 % (10 %) | 1e−8 relatif sur la forme fermée ; écarts publiés |
| J3 | Boucle propre (critère 5 (b)) | Revenus hors intérêts exogènes. Valeur propre dominante : 0,96612 (i_D = 0), 0,96706 (i_D = 3 %), 0,96727 (i_D = 11 %, π̄ = 10 %) ; λ_H ×0,5 : 0,98352 ; ×2 : 0,93419 (i_D = 3 %) | module < 1 aux trois calibrations ; demi-vies publiées |
| J3 | Boucle conjointe (critère 5 (c) ; réserve 3) | SN, C, M, ménages, avec F de la fiche 6 et π^e = π\* exogène ; régimes H et B. Repères de maquette (§ 3.C-10, point 8) : 0,9640 / 0,9617 (θ_H = 0,8), 0,9564 / 0,9537 (θ_H = 1), sous un θ_H effectif fixé par F. Recalculé avec la loi de π^e de la fiche 8 dès qu'elle existe | rayon < 1 à la calibration, hors racine nominale (\|λ − 1\| ≤ 1e−8) ; publié aux vitesses ×0,5 et ×2 |
| J3 | Effet d'un changement de cible (réserve 9) | Appel direct, états d'ouverture fixés, π\* passant de 2 % à 1 % : le plan monte. Mesure : +0,5543 % (+0,9776 % sous la cible nominale écartée) | signe + ; ampleur dans [0,3 % ; 0,8 %] par point, à ν_H = 1 et λ_H = 0,4 |
| J3 | Délais (critères 2 (d) et 12 (b)) | Transferts ou impôts au tour n : C^plan inchangé au tour n, modifié au tour n + 1, du signe du levier. i_D au tour n : ligne 10 au tour n, plan au tour n + 1, signe +. G au tour n : consommation au tour n + 2 (*Annotation du 04/10/2026 (revue finale de `macro`, mesure ; décision inchangée) : corrigé de façon prospective : dividende au tour n, budget au tour n + 1 ; revenu salarial au tour n + 1, budget au tour n + 2)* (boucle). π\* : selon la date retenue (§ 9.8) | signe et date exacts |
| J3 | Phases (critère 2) | En phase 2, le bloc ne lit que l'ouverture et π\* ; aucune lecture de WB_t, N\*, y\*, G^plan, I^plan ni du registre. H6 vient après le bloc 2 ; H7 ne lit que les phases ≤ 6 | aucune lecture hors ordre |
| J3 | Bornes (critère 8 ; #38) | (a) Plafond inactif à l'état résolu, marge de 12,24 mois de consommation ; appel direct avec D_{H,t} = 0,5·C^règle_t : C^plan = D_{H,t}. (b) Plancher : appel direct avec YD_{t−1} = −YD̄ : C^plan = 0. (c) Cas des impôts doublés (§ 3.N-6) : D_H vaut 1 280, 1 184 puis 1 155 après les phases 4, 5 et 6 ; le plan du tour suivant baisse de ΔT_H·(α_YΓ^e + λ_H/n_a − γ^e + ν_Hλ_Hπ^{∗,pas}) = 10,12 pour ΔT_H = 16. (d) D_H ≥ 0 à la fin de chaque phase, en O2 | (a), (b), (d) exacts ; (c) 1e−12 relatif |
| J3 | Conditions de domaine (§ 9.2) | Chargement avec ν_Hλ_H = 1, ou λ_H > n_a, ou un coefficient de richesse ≤ 0 : refus explicite, sans écrêtage | refus |
| J3 | Part d'un transfert (critère 12 (d)) | Appel direct, équilibre partiel du bloc, transfert de 1 % du YD stationnaire aux tours 1 à 12. Mesure : 0,628 (2 %), 0,618 (10 %) ; λ_H ×0,5 : 0,760 ; ×2 : 0,423 | dans [0,50 ; 0,85] à la calibration (sous réserve de l'adoption du seuil, § 9.5) ; publiée aux variantes |
| J3 | Superneutralité (C15, avec la fiche 8) | V/(n_a·Y_o) et C/Y_o pour π̄ = π\* ∈ {0 ; 2 % ; 10 %}, avec la relation de Fisher de la fiche 8 | seuil fixé avec #49, **avant l'essai** (résidu mesuré : +0,42 % sous r = i − π linéaire, +0,006 % sous Fisher géométrique, § 6.1) |
| J3 | Test zéro (critère 7 ; bandes à confirmer avec O1, M19) | 720 pas, plusieurs graines, moyennes par blocs de 60 pas : V_H d'ouverture/(12·YD du pas) dans ±2 % relatif autour de la valeur résolue (0,980566 à 2 %) ; taux d'épargne nominal sur 12 tours dans ±0,5 point de 3,8900 % ; aucune demande non servie ; B_H/V_H sans objet. V/(n_a·YD^HS) publié | bandes du critère 7 |
| J3 | Persistance (condition 10 de `jeu` ; #44) | G ou transferts aux tours 1 à 12, boucle conjointe fermée | écart de production sous la moitié du pic en ≤ 60 tours |
| J3 ou J4 | Instabilité 15 (critère 8 (c)) | O2, G +1 % et +5 % : plafond et plancher inactifs. Scénario adverse : borne désactivée au plus tard 12 tours après la fin du choc, sans réactivation | 12 tours |
| J3 | Empreinte | Une variable d'état, YD_{t−1} ; aucun registre lu ; aucun tirage | décompte exact |
| J3 | Coût | Part du bloc dans `tests/invariants/test_budget.py` | ≤ 0,48 ms par pays-pas |
| J4 | Restitution | Niveaux normaux égaux à ceux du script : 1 an ; 0,980566 ; 1,9852 % ; 3,8900 % ; g. Résidu de la décomposition du § 9.4 | 1e−9 relatif ; résidu ≤ 1e−12 relatif |
| J4 | Sur-commande (critères 8 (c) et 11 (c) ; condition 9 ; #53) | Scénarios du § 9.5, prix et politique endogènes | demande non servie des ménages nulle, et borne d'emploi inactive, au plus tard 12 tours après la fin du choc ; mesures publiées |
| J4 | Signe net du taux (condition 8 ; #56) | Critère écrit dans #56 avant l'essai | idem |
| J4 | Variante D (`jeu`, Q6) | Sans transfert ciblé, trajectoire identique à C | 1e−12 relatif |
| fiche 8 | Aller-retour de π\* (#54) ; clause C26 | Critères écrits dans la fiche 8 avant l'essai | idem |
| — | Remesure V5-1 | Proposée, non lancée ; sans effet sur M27 | — |

**Où sont tenues les réserves du § 5** :
- 1 : état stationnaire ;
- 2 : vitesses et continuum hors C2 ;
- 3 : boucle conjointe et C26 ;
- 4 : m_H, constat transmis à la fiche 2 ;
- 5 : persistance et #44 ;
- 6 : conditions de domaine ;
- 7 : calibration (issue proposée) ;
- 8 : #53 ;
- 9 : effet d'un changement de cible et #54 ;
- 10 : fiche 8, J5.

### 9.7 Chiffres remesurés sous la décision

Commandes, exécutées le 03/10/2026 dans le scratchpad :
- `uv run --no-project --with numpy python f5s9.py` : formes fermées et simulation, n_a = 4, 12 et 52, π̄ = 2 % et 10 %, hors C2 ;
- `f5s9_part.py` : part du transfert et frontières de λ_H ;
- trois scripts courts (`uv run --no-project [--with numpy] python -`) : valeurs propres de la boucle propre, effet de π\*, m_H, cas des impôts doublés, seuil du coefficient de richesse, expression régulière des labels.

Validation : les scripts redonnent les chiffres publiés aux § 3.C, § 3.C-10 point 8, § 5 (réserve 2 : −3,35 / −1,29 / −0,22 % ; −19,76 / −8,58 / −1,56 %) et § 6.1 Q5 (3,890 / 10,557 / 1,985 / 1,998 %), ainsi que la mesure de `jeu` (§ 7, Q2 révisée : 1,943 / 8,733 et 1,947 / 1,823). Ils redonnent aussi les valeurs de la cible nominale publiées au § 3.C (m_H 0,7683 / 0,7920 / 0,9603 / 0,9900).

**Avant / après** : une ligne par grandeur de la fiche que la décision (cible de Haig-Simons, M27 (f)) change. Les chiffres « avant » sont ceux du § 3, cible nominale.

| Grandeur | Avant (§ 3, cible nominale) | Après (M27) | Écart | Explication |
|---|---|---|---|---|
| V/(n_a·YD) stationnaire, 2 % / 10 % | 1 / 1 | 0,980566 / 0,912667 | −1,94 % / −8,73 % | la cible porte sur YD^HS : V = ν_H n_a YD^HS |
| V/(n_a·YD^HS) | — | 1 exactement | — | idem ; niveau normal restitué |
| Dépendance de V/(n_a·YD) à n_a (2 %) | ν, exact | 0,980535 / 0,980566 / 0,980578 | ≤ 4,3e−5 | π^{∗,pas} géométrique ; déclarée (ADR 0008, I.6) |
| Taux d'épargne nominal, 2 % / 10 % | 3,967 % / 11,567 % | 3,8900 % / 10,5565 % | −0,08 / −1,01 pt | idem |
| Taux d'épargne de Haig-Simons, 2 % / 10 % | 2,025 % / 2,209 % | 1,9852 % / 1,9977 % | −0,04 / −0,21 pt | idem ; quasi indépendant de l'inflation |
| Taux de Haig-Simons selon n_a (2 %) | — | 1,9950 / 1,9852 / 1,9814 % (n_a = 4 / 12 / 52) | — | ADR 0008, I.6 ; déclaré |
| C/YD, 2 % / 10 % | 0,96033 / 0,88433 | 0,96110 / 0,89444 | +0,0008 / +0,0101 | idem |
| Boucle propre, i_D = 0 / 3 % | 0,96678 / 0,96772 | 0,96612 / 0,96706 | −0,0007 | idem (déjà au § 3.C-10, point 8) |
| Boucle propre, λ ×0,5 / ×2 (i_D = 3 %) | 0,98385 / 0,93551 | 0,98352 / 0,93419 | −0,0003 / −0,0013 | idem |
| m_H de long terme, θ_H = 0,8 (i_D = 0 / 3 %) | 0,7683 / 0,7920 | 0,7689 / 0,7922 | +0,0006 / +0,0002 | idem ; impact inchangé (0,4808) |
| m_H de long terme, θ_H = 1 (i_D = 0 / 3 %) | 0,9603 / 0,9900 | 0,9611 / 0,9902 | +0,0008 / +0,0002 | idem ; impact inchangé (0,6010) |
| Part propre d'un transfert, 12 tours, 2 % / 10 % | 0,627 (`macro`) / 0,614 (`jeu`) | 0,628 / 0,618 | +0,001 / +0,004 | idem ; `jeu` mesure 0,629 et 0,621 dans sa maquette (écart de 0,003 au plus, convention de taille du transfert) |
| Frontières de λ_H pour le seuil 12 (d), ν_H = 1 | 0,08 à 0,62 | 0,080 à 0,634 | +0,014 en borne haute | idem |
| Marge du plafond | « environ 12ν mois » | 12,24 mois de consommation | — | précision : 12·(V/YD)/(C/YD) |
| Cas des impôts doublés : baisse du plan au tour suivant | 9,6 (§ 3.N-6) | 10,12 | +0,52 | **correction de rédaction**, et non effet de la décision : le § 3.N-6 omettait Γ^e et le terme de richesse (ΔV = −ΔT_H). Sous la cible nominale, la valeur exacte est 10,11 |

**Inchangés** :
- l'effet d'un changement de cible, +0,5543 % (+0,9776 % sous la cible nominale), remesuré ;
- α_Y = 0,6 et la condition ν_Hλ_H < 1 ;
- les délais ;
- la boucle conjointe du § 3.C-10, point 8, non remesurée ici (contre-épreuve indépendante au 4e chiffre) ;
- la sur-commande, **non remesurée sous la cible de Haig-Simons** (réserve 8 ; #53).

**Lignes de la fiche à mettre à jour** (révision citant M27, mention datée, session principale) :
- § 1.2, ligne « Richesse rapportée au revenu disponible annuel », restitution : renvoi au § 9.4 (ratio sur YD^HS au tour, retenu par M27) ;
- § 3.N-6 : « baisse de (1 − νλ_V)·16 = 9,6 » devient « baisse de 16·(α_YΓ^e + coefficient de richesse) = 10,12 ».

Les § 3 à 7 restent sinon la trace de l'instruction.

**Valeurs de l'état initial résolu** (sous C2, π̄ = π\*) :
- YD_{−1} = YD_0/Γ̄, avec Γ̄ = [(1 + g)(1 + π\*)]^{1/n_a} = Γ^e ;
- V_{H,0} = D_{H,0} = ν_H n_a YD_0/(1 + ν_H n_a π^{∗,pas}), soit 11,7668·YD_0 à 2 % ;
- B_{H,0} = 0 ;
- YD_0 vient de la résolution conjointe avec les fiches 6, 7 et 9 (#44).

### 9.8 Contrats partagés touchés, surface de spécification, constats transmis

**Contrats partagés** (`docs/agents/routage.md` § 4.2) :
1. **`tab:phases`, ligne 7** : H7 calcule YD_t en phase 7. Deux lectures :
   - (i) en phase 6, après les autres blocs : cela demande un ordre interne de la phase 6, absent de la liste de la l. 487, donc une décision citant M22 ;
   - (ii) **en phase 7, recommandée** : aucun ordre nouveau ; les lectures sont conformes à la colonne « Lisent ». Seule la colonne « Contenu » gagne « revenu disponible des ménages (variable d'état) ».

   Le § 3.N-5 écrivait « phase 6 → YD_t » ; le § 1.3 écrivait que le bloc 5 « n'écrit rien » en phase 6. À qualifier par `architect`, au visa du mainteneur. La ligne 2 (« budget de consommation ») et la ligne 5 sont inchangées.
2. **π\* à source unique, et sa date** (frontière `monnaie`, fiche 8). Les blocs 5 (M27) et 6 (M28, ϱ_L) lisent π\*. Avant la fiche 8, π\* doit exister au J3 comme paramètre à source unique. **Date, deux lectures** :
   - (a) π\* du tour, lue en phase 1 : c'est la lecture implicite des § 3.N-5 et 6.5 ; délai 0 ;
   - (b) π\* en vigueur à l'ouverture : délai 1.

   (a) déroge à la grammaire des délais des fiches 3 et 4 (« une décision du tour n agit sur le secteur privé au tour n + 1 au plus tôt »). Elle contredit aussi la phrase de l'additif de `jeu` : « une annonce ne déplace pas l'épargne le tour même ». Sous (b), l'impulsion de +0,55 % et le frein de Fisher (baisse de i_D → ligne 10 au tour n → plan au tour n + 1) entrent au même tour, ce qui devrait réduire le gain d'impact visé par #54 (hypothèse, **non mesurée**). Aucun effet stationnaire.

   Je recommande (b), sous l'avis de `monnaie`. C'est une décision du mainteneur citant M27 et M28.
3. **Γ^e partagé avec la fiche 6** : son Γ̂ = [(1 + g)(1 + π\*)]^{1/n_a} est la même grandeur. Un symbole, un calcul (localité). Je propose le radical `moteur` (`eq:moteur-croissance-nominale-attendue`), à fixer avec la fiche 6, § 9, et `architect`.
4. **Matrices inchangées** : les lignes 11a, 19a-ménages et 19b-ménages restent à montant nul, sans retrait. `verifier_matrices.py --strict` garde ses décomptes.
5. **`tab:leviers-cadre`** : inchangée. Les délais vers la consommation sont déclarés dans l'encadré `joueur` de `sec:menages`, et la fiche 2, § 9.4, est confirmée.
6. **Ratio de richesse et M22, lecture (e)** : M27 retient le ratio au tour, stock d'ouverture sur 12 × YD^HS du tour, au lieu de la lecture (e) que les § 1.1 et 1.2 appliquaient. La lecture (e) (ADR 0005, pt 17) vise un « ratio au PIB annuel » ; à mon sens, elle ne s'impose donc pas à ce ratio, et aucune décision citant M22 n'est requise. Le facteur 1,0108 ne s'applique pas à ce ratio. À confirmer par le mainteneur.

**Surface de spécification** (#41, jalon 4, `docwriter` ; encadrés `proposee` citant M27, sans label ; plan de `CONVENTIONS.md` § 1.2) :
- **`sec:menages`** : rédiger la section, qui remplace le paragraphe d'attente des l. 850 à 853. Contenu :
  - rôle ;
  - encadré de décision : M27, option C, lecture (c) sur π\*, cible de Haig-Simons, B_H ≡ 0, plafond en phase 2, canal rentier seul, deux taux d'épargne nommés ;
  - tableau des équations H1 à H7, avec les labels prévus au J3 ;
  - revenu disponible : lignes lues, phase 7, forme symbolique, hypothèses provisoires remplacées à la fiche 9 ;
  - revenu attendu et facteurs, par `eq:moteur-conversion-croissance` ;
  - richesse visée ;
  - plan et forme réduite ; conditions de domaine ;
  - `\limites` : plafond (seuil libre, base D_{H,t}, inactif, marge de 12,24 mois) ; plancher (conservation, inactif) ; D_H ≥ 0 et B_H ≥ 0 (conservation) ; priorité des paiements ;
  - consommation (ligne 1) ;
  - portefeuille : B_H ≡ 0, placement par la banque (C19, C25), assouplissement quantitatif à la banque seule (C17) ;
  - inflation lue : π\*, jamais π̄ ni le registre ; (a) écartée comme explosive (#58) ; C26 ;
  - état stationnaire : V_H = ν_H n_a YD^HS ; ratios et taux du § 9.7, avec leur dépendance à n_a ; superneutralité au résidu de #49 près ; état initial résolu ;
  - continuum hors C2 : forme fermée et chiffres ; C2 devient une condition de la fiche 5 ;
  - boucles et m_H ;
  - canal du taux : rentier, signe + ; structure d'équilibre général b/(1 + i·b) de `monnaie` ;
  - effet d'un changement de cible ;
  - grandeurs restituées et niveaux normaux ;
  - encadré `joueur` : délais et contreparties ;
  - encadré `portee` : ménage représentatif (D au J4) ; ni titres, ni crédit, ni actions, ni immobilier ; aucune substitution intertemporelle (hypothèse réfutée 3) ; aucun comportement ricardien ; effet richesse plus fort que la littérature lue ; λ_H non sourcé ; aucune fuite devant l'inflation (C18, J6) ; forme C non écrite telle quelle par Godley et Lavoie.
- **`tab:calibration`** : ν_H, λ_H, plafond (selon la lecture retenue au § 9.2).
- **`tab:symboles`** : C^plan, C^règle, YD, YD^e, YD^HS (restitution), V^∗_H, ν_H, λ_H, Γ^e, γ^e, π^{∗,pas}, α_Y, π\* (bloc 8, si la fiche 8 ne l'a pas encore posé). Définition de x^pas à réviser selon la nature du taux (ADR 0008).
- **`tab:phases`** : ligne 7, selon le contrat 1.
- **`sec:ecartees`**, « Ménages (décision M27) » :
  - A ; B ; S à α libres ; R1 ; R2 (référence) ;
  - Q10 (a), explosive ; π_s sur π_{t−1}, explosive à θ_H = 1 ; variante h ;
  - cible nominale (superneutralité) ;
  - revenu lissé (Q2 (ii)) ;
  - Tobin et part fixe, renvoyées ;
  - plafond en phase 5 ;
  - PCEX2.
- **`tab:instabilites` (#58)** : deux faits nouveaux, de statut « maquette v3, contre-épreuve indépendante » (fiche 5, § 3.C-10). Ce ne sont pas des faits de la première tentative : le titre et la phrase d'introduction de la table sont à adapter, et la numérotation est à coordonner avec la fiche 6 (variantes explosives de F).
  - **17** : correction d'inflation complète des ménages sur le glissement mesuré. La boucle conjointe salaires – prix – ménages est explosive : 1,0275 / 1,0029 (θ_H = 0,8), oscillation de 17 à 19 tours ; frontières ν < 0,586, h < 0,604.
  - **18** : π^{∗,pas} mesuré dans la cible de Haig-Simons. Explosif à θ_H = 1 : 1,0223 / 1,0218, période de 49 à 60 tours.
  - Paragraphe après la table : le bloc ménages ne réintroduit pas la 8 (aucune épargne de précaution) ni la 15 (aucune borne active à l'état stationnaire ; test 8 (c)). Il déclare ses deux paramètres d'effet richesse, mais le sens exact de la 6 n'est pas établi (source non versée).
- **`sec:changements-v3x`** : une ligne « ménages (M27) ».
- **`CONVENTIONS.md`**, le cas échéant :
  - § 5.2 : notation x^pas par nature, si π^{∗,pas} est retenu, en même temps que les retouches de l'ADR 0008 ;
  - § 2.4 : borne à seuil libre dont le seuil est une base, si la lecture (i) du § 9.2 est retenue.

**Constats transmis** :
- **Fiche 2** :
  - m_H d'impact de 0,48 à 0,60, sous 0,8 ;
  - m_H de long terme de 0,79 à 0,99, au-dessus de 0,8 si θ_H tend vers 1. La réserve 3 se consolide au J3 avec le θ_H effectif de F.
- **Fiche 6** :
  - Γ̂ = Γ^e (un symbole, un calcul) ;
  - la date de π\* vaut aussi pour ϱ_L (contrat 2) ;
  - F fixe le θ_H effectif ;
  - fermeture B/PIB avec V_H = ν_H n_a YD^HS.
- **Fiche 7** : C19 à C22 ; la règle de i_D n'est disciplinée par aucun actif concurrent ; la date de Div_Bk fixe la compensation du canal rentier.
- **Fiche 8** :
  - C14 à C18 et C26 ;
  - π\* à source unique, avec sa date et son domaine (coefficient de richesse positif : π\* < 85 % à la calibration) ;
  - C2 est aussi une condition de la fiche 5 (un point d'écart stationnaire coûte environ 1,3 % du ratio) ;
  - #54 ; régimes B, D et E.
- **Fiche 9** :
  - C23 à C25 ;
  - **insuffisance de dépôts pour la ligne 7** : un impôt ne peut excéder D_H après la phase 5 plus les recettes de la phase 6 que sous une règle de la fiche 9. Le traitement compatible avec le socle est un rationnement déclaré (impôt non recouvré), sans créance fiscale, instrument absent. La date du contrôle de caisse dans une phase sans ordre interne est à préciser avec `docwriter` (`sec:cadre-caisse`) ;
  - gratuité de la sur-commande (#53).
- **`jeu` et `app-review`** : dénominateurs de la décomposition (§ 9.4) ; terme de borne Δ^plaf ; définition de l'épisode ; délai de π\*.
- **`architect`** :
  - contrats 1, 3 et 6 ;
  - `CONTEXT.md` : « richesse visée », « revenu de Haig-Simons », « taux d'épargne visé », « taux d'épargne constaté », « épargne forcée (demande non servie cumulée) », « budget de consommation » ;
  - statut de l'inventaire ;
  - rattachement éventuel de #58 au périmètre de la branche, sur accord du mainteneur.

### 9.9 Issues proposées

Création sur accord du mainteneur ; corps au compte rendu de `macro` du 03/10/2026 :
1. « J3 — src/nations/blocs/menages.py et ses tests (fiche 5, § 9.6), balises eq:menages-* » ;
2. « Cible d'inflation π\* et facteur Γ^e : source unique, date de lecture et propriétaire (blocs 5 et 6, avant la fiche 8) » ;
3. « Fiche 5 : calibration de ν_H et de λ_H sur des sources lues, dans le seuil du critère 12 (d) » ;
4. « J4 — restitution du bloc ménages : revenu par source, trois taux d'épargne, richesse en années de revenu, décomposition, épargne forcée » (ou extension de #52).

### 9.10 Décisions du mainteneur sur les conséquences (03/10/2026)

*Prises après le dépôt des § 9 des fiches 5 et 6, sur les lectures soumises par `macro`, l'avis de `monnaie` et celui d'`architect`. Elles s'imposent au passage de `docwriter` ; le texte des § 9.1 à 9.9 reste celui de `macro`, à lire avec les corrections ci-dessous.*

- **Date de lecture de π\*** (décision citant M27 et M28 ; recommandation concordante de `macro` et `monnaie`) : les blocs 5 et 6 lisent la cible **en vigueur à l'ouverture** (délai d'un tour, même date que i_L, C27). Le facteur **Γ^e = [(1 + g)(1 + π\*)]^{1/n_a}** est une grandeur du moteur, calculée une seule fois (`eq:moteur-croissance-nominale-attendue` proposé) ; le symbole Γ̂ de la fiche 6 disparaît. Au J3, π\* est un paramètre typé à source unique de `moteur/` qui initialise une variable d'état « cible en vigueur » ; à la fiche 8, cette variable est écrite par le levier du bloc 8. Issue #61.
- **Phase des variables d'état retardées assises sur des flux de la phase 6** (M29, contrat partagé `tab:phases`) : lecture (i) d'`architect`, acceptée sur le fond ; l'ADR 0009 est déposé après relecture Fable. Le bloc 6 retient T_{F,t} et le bloc 5 calcule YD_t (H7) **en phase 9**, après les identités du noyau et avant le passage au pas suivant, sans flux ; les ménages sortent des écrivains de la phase 7 au socle (B_H ≡ 0).
- **Lectures de la fiche 5 retenues** : renommages ν → ν_H, λ_V → λ_H, π_s → π^{∗,pas} (critère 15) ; plafond du budget sur les dépôts d'ouverture D_{H,t}, sans paramètre ; plancher max{0, ·} du plan (inactif à l'état stationnaire, à déclarer selon `CONVENTIONS.md` § 2.4) ; seuil du critère 12 (d) de 0,50 à 0,85 sur la part propre d'un transfert dépensée en 12 tours ; **#58 rattachée à la branche** (sans `Closes`) : l'instabilité de la lecture (a) est versée à `tab:instabilites`.
- **Issues créées** : #60 (J3, `menages.py`), #61 (π\* et Γ^e), #62 (calibration de ν_H et λ_H), #63 (restitution du bloc ménages au J4).

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 03/10/2026 | Ouverture (issue #41) ; § 1 et § 2 proposés | `macro` ; session principale |
| 03/10/2026 | Critères validés avec amendements (seuils et bandes, bouclage avec la fiche 9 en risque assumé, B_H ≡ 0 admise, ménage représentatif et variante à deux types, `monnaie` consulté aussi sur l'inflation, Q11 au J4 ; issue #41) | mainteneur |
| 03/10/2026 | Instruction déposée (§ 3 à 5), partielle (boucle conjointe avec SN, C et M et état conjoint avec la fiche 6 non mesurés ; une relance ciblée après la limite de tours) : options A, B, S, C, R, D ; recommandation C (cible de richesse avec terme de tendance, B_H ≡ 0) ; § 1.1 aligné sur l'ADR 0008 | `macro` ; session principale |
| 03/10/2026 | Avis de `jeu` (§ 7) : préférence C ; seuil du critère 12 (d) proposé (part d'un transfert dépensée en 12 tours entre 0,50 et 0,85, en équilibre partiel ; 0,628 à la calibration) ; double dimension de la sur-commande (G ×2 pendant 12 et 24 tours) ; conditions de restitution ; trois constats chiffrés transmis à `macro` | `jeu` |
| 03/10/2026 | Avis de `monnaie` (§ 6) : favorable à C avec B_H ≡ 0, lecture (a), classement des taux confirmé, double restitution du taux d'épargne ; constat de non-superneutralité de la cible nominale et proposition d'une cible sur le revenu de Haig-Simons (deux positions si `macro` maintient la sienne) ; structure d'équilibre général du canal rentier ; conditions C14 à C25 pour les fiches 7, 8 et 9 | `monnaie` |
| 03/10/2026 | Additif de `macro` (§ 3.C-10) : boucle conjointe SN, C, M et ménages mesurée, contre-épreuve en niveaux ; critère 5 (c) tenu sous (c) (0,9637 / 0,9613), explosif sous (a) (1,0275 / 1,0029), d'où la recommandation de la Q10 révisée vers (c) ; instabilité nouvelle mesurée ; § 3.L, sur-commande et § 3.N-9 corrigés après les constats de `jeu` ; réserves 3 et 8 remplacées | `macro` ; session principale |
| 03/10/2026 | Réponse de `macro` sur la cible de Haig-Simons (§ 3.C-10, point 8 ; § 5 : second additif, réserve 3, lecture (f)), versée après contre-épreuve indépendante concordante au 4e chiffre | `macro` ; session principale |
| 03/10/2026 | Additif de `monnaie` (§ 6.5) : retrait de (a), ralliement à (c) en lisant π\* pour γ^e et π_s, cible de Haig-Simons, variante h refusée, clause C26, C16 et C18 mises à jour ; aucun désaccord résiduel avec `macro` | `monnaie` ; session principale |
| 03/10/2026 | Additif de `jeu` (§ 7) : ralliement à (c) ; embardée de sur-commande « à clarifier » (attribution, falaise, ψ_ξ), dimension maintenue et trois variantes ; ratio de Haig-Simons affiché d'abord (niveau normal 1 an), lecture (e) retirée ; conditions 2 et 4 révisées ; part propre au ménage pour le critère 12 (d), seuil tenu | `jeu` ; session principale |
| 03/10/2026 | Avis de `macro` sur l'additif de `monnaie` : accord sur π\*, C26, effet d'un changement de cible (+0,5543 % / +0,9776 %, remesurés) et continuum hors C2 ; § 5 réécrit (version antérieure : `3b31b6e`), recommandation (c) sur π\* et cible de Haig-Simons ; additifs datés aux § 3.N-3, 3.N-5 et 3.C (points 1 et 9) | `macro` ; session principale |
| 03/10/2026 | Second additif de `jeu` (§ 7) : effet d'un changement de π\* « à clarifier » (déclaré par les cases existantes ; essai d'aller-retour demandé à la fiche 8) ; deux taux d'épargne lisibles sous deux libellés. Statut « avis rendus » : avis de `macro`, `monnaie` et `jeu` rendus, aucun désaccord résiduel | `jeu` ; session principale |
| 03/10/2026 | Décision M27 : option C, lecture (c) sur π\*, cible de Haig-Simons, lectures (b) à (e) du § 5 ; correction prospective du critère 4 (ii) (#59) | mainteneur |
| 03/10/2026 | Conséquences de M27 (§ 9) rédigées par `macro` : labels (au J3), notation, paramètres, interfaces, conditions de `jeu`, tests, chiffres remesurés, contrats partagés et surface de `sec:menages`, quatre issues proposées ; lectures soumises au mainteneur | `macro` ; session principale |
| 03/10/2026 | Décisions du mainteneur sur les conséquences (§ 9.10) : date de π\* (délai 1), Γ^e au moteur, M29 (YD en phase 9), lectures de la fiche 5 retenues, #58 rattachée, issues #60 à #63 | mainteneur ; session principale |
