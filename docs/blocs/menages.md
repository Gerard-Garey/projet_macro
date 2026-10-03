---
bloc: Ménages
module: src/nations/blocs/menages.py
expert pilote: macro
experts consultés: monnaie (dépôts et détention de titres publics : frontière dette publique) ; jeu
statut: en instruction (critères validés le 03/10/2026)
décision: —
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
- Ordre de grandeur, ν = 1 : +1 point de i_D donne +1 % de YD par mois, et +0,6 % du plan au tour n + 1 (α_Y = 1 − νλ_V = 0,6).
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

9. **Empreinte.** 2 paramètres (ν, λ_V) ; 1 variable d'état (YD_{t−1}, u.m., valeur stationnaire YD_t/Γ) ; lecture du registre de l'ADR 0008, sans état ajouté.

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

Maquette B1 : prix figés, emploi R, θ_H = 0,8, i_D = 3 %, ν = 1, λ_V = 0,4. Écarts au sentier ; ratio = V/(12·YD) ; taux d'épargne stationnaire 0,03967.

| Tour | (i) G +1 %, tours 1 à 12 : plan / YD / taux d'épargne / ratio | (ii) transferts +1 % de YD, tours 1 à 12 : plan / YD / taux d'épargne / ratio |
|---|---|---|
| 1 | 0 / 0 / 0,03967 / 1,00000 | 0 / +1,000 % / 0,04918 / 1,00000 |
| 2 | 0 / +0,081 % / 0,04045 / 1,00000 | +0,656 % / +1,002 % / 0,04297 / 1,00083 |
| 3 | +0,053 % / +0,138 % / 0,04048 / 1,00007 | +0,669 % / +1,215 % / 0,04485 / 1,00114 |
| 4 | +0,091 % / +0,194 % / 0,04066 / 1,00014 | +0,819 % / +1,368 % / 0,04487 / 1,00161 |
| 9 | +0,257 % / +0,405 % / 0,04109 / 1,00068 | +1,360 % / +2,034 % / 0,04602 / 1,00427 |
| 13 | +0,350 % / +0,509 % / 0,04119 / 1,00121 | +1,705 % / +1,410 % / 0,03687 / 1,00669 |
| 14 | +0,369 % / +0,447 % / 0,04042 / 1,00135 | +1,124 % / +1,483 % / 0,04307 / 1,00648 |
| 18 | +0,264 % / +0,292 % / 0,03994 / 1,00158 | +0,992 % / +1,068 % / 0,04040 / 1,00718 |
| 24 | +0,159 % / +0,137 % / 0,03947 / 1,00161 | +0,715 % / +0,651 % / 0,03907 / 1,00726 |

- C égale le plan : la demande des ménages est entièrement servie.
- Délais : G au tour n, consommation au tour n + 2 ; transferts au tour n, consommation au tour n + 1.
- La part d'un transfert dépensée en 12 tours (critère 12 (d)) n'est **pas calculée** : à extraire de la même maquette.

**Sur-commande** (critère 11 ; maquettes B1 et B2 ; G doublé, part de 20 %, tours 1 à 12 ; plafond N^pa) :
- taux de service de 1 jusqu'au tour 8, puis 0,869 / 0,856 / 0,853 / 0,850 aux tours 9 à 12 ;
- **demande non servie des ménages nulle dès le tour 13** : seuil de 12 tours tenu ;
- épargne forcée : richesse +6,33 % au tour 13, soit 0,79 mois de consommation ;
- ratio de richesse au plus à +0,99 % de ν, donc dans la bande de ±2 % ;
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

*`macro`, 03/10/2026.*

**Recommandation : option C** (cible de richesse avec terme de tendance), ménage représentatif, avec les choix suivants :
- revenu lu : YD_{t−1} avec tendance (Q2 (i)) ;
- inflation de la tendance : glissement mesuré π_{t−1} (Q10 (a)) ;
- revenu corrigé de Haig-Simons implicite, taux d'épargne restitué nominal et corrigé (Q3) ;
- **B_H ≡ 0** au socle (Q4) ;
- plafond du plan à D_{H,t} d'ouverture, lecture (a) du § 3.N-6 ;
- la variante D notée pour le J4 (Q6, Q11).

Calibration indicative : ν = 1 an, λ_V = 0,4 par an (α_Y = 0,6).

**Motifs** :
- seule option qui tient le critère 4 (ν exact, F2) ;
- forme fermée ;
- aucune borne à seuil libre hors 3.N-6 (a) ;
- deux paramètres et une variable d'état ;
- rayon < 1 sur toute la grille (B1) ;
- D est équivalente au niveau agrégé sans levier ciblé (principe de simplicité).

**Écartées** :
- A : critère 4 et strates qui touchent M22 ;
- B : critère 14 pour la branche active, critère 4 pour la règle de revenu, plafond ;
- S, écrite avec α libres : critère 4 ;
- R1 : hors domaine.

R2 reste la référence non mesurée.

**Réserves**, avec leurs critères écrits avant l'essai (J3) :
1. Un pas sans choc depuis l'état résolu laisse V_H/(n_a·YD) = ν et YD_{t−1} sur leur sentier à 1e−10 près en relatif.
2. Critère 4 : écart au plus de 1e−6 après 720 pas entre λ_V ×0,5 et ×2.
3. **Boucle conjointe SN, C, M et ménages (critère 5 (c) complet) : non mesurée.** Rayon < 1 exigé à la calibration ; publication aux vitesses ×0,5 et ×2.
4. **m_H de long terme supérieur à 0,8 si θ_H = 1** : réserve 3 de la fiche 2, à trancher avec la fiche 6 (distribution des dividendes) et la fiche 9 (impôts).
5. **Racine quasi unitaire sans fuite** (θ_H = 1 : 0,9993) : le niveau d'activité n'est fermé que par les fiches 6, 8 et 9 (#44). Le calcul conjoint avec la fiche 6 est à faire avant M27-M28 ; il n'est pas fait ici.
6. Condition de domaine νλ_V < 1, déclarée et contrôlée au chargement.
7. Calibration de λ_V et de ν sur des sources lues (richesse liquide, gains de loterie, comptes financiers) : **à instruire**.
8. Sur-commande : seuil du critère 11 (c) tenu dans la maquette, mais la borne N ≤ N^pa reste active plus de 100 tours sans rappel des prix ni de la politique. Mesure au J3 ou au J4 avec les fiches 4 et 8.

**Lectures soumises au mainteneur** :
- (a) Q10 : π^lu = glissement mesuré, π^e ou π̄ ;
- (b) § 3.N-6 : plafond en phase 2 (seuil libre déclaré) ou en phase 5 (révision de M24) ;
- (c) Q4 : B_H ≡ 0 ou demande de Tobin ;
- (d) canal du taux : rentier seul, ou variante PCEX2 α_1(r). Cette dernière demande un fait nouveau contre l'hypothèse réfutée 3 ;
- (e) restitution du taux d'épargne : nominal, corrigé, ou les deux.

**Coût en fidélité** :
- aucun canal de substitution : le taux agit sur la consommation à l'envers ;
- effet richesse plus fort que celui que mesure la littérature lue (richesse peu liquide) ;
- aucune hétérogénéité au socle ;
- la forme C n'est pas écrite telle quelle par Godley et Lavoie : c'est leur α_3 cible, rendue exacte sous croissance.

## 6. Avis de l'expert consulté

Non instruit (`monnaie`, frontière dette publique : détention de dépôts et de titres publics, au jalon 2).

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

## 8. Décision du mainteneur

Non instruit (M27, décidée avec la fiche 6).

## 9. Conséquences de la décision

Non instruit.

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 03/10/2026 | Ouverture (issue #41) ; § 1 et § 2 proposés | `macro` ; session principale |
| 03/10/2026 | Critères validés avec amendements (seuils et bandes, bouclage avec la fiche 9 en risque assumé, B_H ≡ 0 admise, ménage représentatif et variante à deux types, `monnaie` consulté aussi sur l'inflation, Q11 au J4 ; issue #41) | mainteneur |
| 03/10/2026 | Instruction déposée (§ 3 à 5), partielle (boucle conjointe avec SN, C et M et état conjoint avec la fiche 6 non mesurés ; une relance ciblée après la limite de tours) : options A, B, S, C, R, D ; recommandation C (cible de richesse avec terme de tendance, B_H ≡ 0) ; § 1.1 aligné sur l'ADR 0008 | `macro` ; session principale |
| 03/10/2026 | Avis de `jeu` (§ 7) : préférence C ; seuil du critère 12 (d) proposé (part d'un transfert dépensée en 12 tours entre 0,50 et 0,85, en équilibre partiel ; 0,628 à la calibration) ; double dimension de la sur-commande (G ×2 pendant 12 et 24 tours) ; conditions de restitution ; trois constats chiffrés transmis à `macro` | `jeu` |
