---
bloc: Investissement et financement des entreprises
module: src/nations/blocs/investissement.py
expert pilote: macro
experts consultés: monnaie (demande de crédit face à l'offre bancaire : frontière crédit) ; jeu
statut: en instruction (critères validés le 03/10/2026)
décision: —
issue: #42
---

# Fiche comparative — Investissement et financement des entreprises

> Fiche ouverte à partir du gabarit `0000-gabarit.md` (validé à l'usage, M20), sur le modèle de forme des fiches 3 « travail et salaires » et 4 « prix » (critères validés le 03/10/2026, `4aee609`). Jalon 1 de l'issue #42 : § 1 et § 2 seuls ; les rubriques suivantes portent « non instruit » jusqu'au jalon 2. Décidée avec la fiche 5 « ménages » (décision du mainteneur du 03/10/2026 : décisions par paires).

Une fiche comparative instruit **l'origine de l'approche** d'un bloc (`docs/exigences.md` § 2.3) : la spécification v1.5, le moteur v2.0, ou une approche nouvelle. Elle est **instruite par l'expert pilote**, commentée par `jeu` et par l'expert consulté que désigne `README.md`, et **décidée par le mainteneur** (décision M-n, reportée dans `docs/feuille-de-route.md`). Aucune approche n'entre dans le moteur ni dans la spécification sans cette décision. Les agents n'écrivent pas la fiche dans le dépôt : elle figure dans leur compte rendu et la session principale la commite. Un **bloc-cadre** (temps et comptabilité) n'est pas un module de `blocs/` : sa fiche instruit ce que le cadre **définit** (conventions, matrices, règles), non des flux proposés ; les adaptations que cela impose sont signalées rubrique par rubrique.

Règles de rigueur (`CLAUDE.md`, « Rigueur ») : un chiffre se remesure ou cite sa source ; une équation de la v1.5 n'a jamais été garantie exécutée ; un comportement de la v2.0 ne vaut que sous son profil (état D1, **non versé** : aucun fait ne peut y être remesuré) et avec ses défauts connus ; chaque fait de la première tentative porte son **statut** S+O, O, R, L, V ou V+O (`CONTEXT.md`, « Statut d'un fait » ; un fait V sur le prototype v2.0 reste un fait de la première tentative, non un résultat v3) ; chaque référence est une publication retrouvée. Citer `archive/v1.5/…` avec numéro d'équation et section, ou avec le **numéro de ligne du `.tex`** quand section ou équation ne sont pas identifiables sans compiler ; `archive/v2.0/…` avec fichier et ligne. **Principe de simplicité** (adopté par le mainteneur le 30/09/2026, fiche « temps et comptabilité » § 2 ; `CONTEXT.md`) : à exigences comptables égales, l'option la plus simple pour le joueur et pour le moteur est préférée ; toute complexité se justifie par une identité qu'elle rend vérifiable ou par un mécanisme perçu à l'échelle d'une partie ; une simplification ne supprime ni une contrepartie comptable visible d'un levier ni une grandeur restituée au tour ; les identités, les tolérances relatives, le déterminisme, les invariants de l'ADR 0002 et la concordance ne se simplifient pas.

## 1. Question posée

*Rédigé par `macro` (expert pilote), 03/10/2026, sur la spécification à l'état `4aee609` (branche `claude/j1-economie-reelle`, PR #43).*

Le bloc décide l'investissement des entreprises et son financement.

Ce qu'il écrit et propose :
- l'**investissement visé**, plan de dépense en u.m. écrit en phase 2, que le bloc 2 sert au prorata (rationnement proportionnel, M24 (g)) ;
- la **ligne 3** en phase 5, soit le volume livré multiplié par p_t ;
- la **ligne 8** en phase 6, soit δK/n_a sur la valeur comptable d'ouverture ;
- la **demande de crédit** présentée à la banque en phase 3 (ligne 18) ;
- si Q6 le confirme, le partage du résultat courant entre dividendes (ligne 14) et profits non distribués.

Il fixe aussi deux grandeurs que la fiche 2 lui laisse :
- le taux d'amortissement δ (`sec:production-capital`, l. 680) ;
- le rapport stationnaire du capital en volume à la production, d'où le taux d'utilisation stationnaire t̄u (`sec:production-stationnaire`, l. 728 et 739).

Le bloc est la première moitié de la frontière crédit et débloque la fiche 7 (`docs/blocs/README.md` § 3, rang 6). Sous M22, un pas est un tour (n_a = 12, n_m = 1) : toute fenêtre exprimée en pas l'est aussi en tours.

La fiche est décidée **avec la fiche 5** (M27 et M28, numéros sous réserve de l'ordre réel des décisions ; décision du mainteneur du 03/10/2026 : décisions par paires). Son critère 5 (c) répond au bouclage de l'épargne et du financement que porte la fiche 5.

### 1.1 Contrats hérités

| Contrat | Source | Ce qu'il impose à la fiche 6 | Ce qui le rouvrirait |
|---|---|---|---|
| Calendrier, conversions et phases du bloc | M22 ; ADR 0005 ; `tab:phases` (l. 505 à 509) | Pas mensuel, n_a = 12. Conversion **linéaire unique** des taux, flux et vitesses, avec λ ≤ n_a ; δ est un taux annuel et la ligne 8 vaut δK/n_a. Investissement visé en phase 2. Demande de crédit en phase 3 (ligne 18 ; « investissement, banque »). Ligne 3 en phase 5. Ligne 8 en phase 6 (« État, banque, investissement »). Neuf phases triangulaires, aucune résolution simultanée | Décision M-m citant M22 |
| Ordres internes des phases | `sec:cadre-phases` (l. 487) ; ADR 0007 ; `sec:production-phases` (l. 690 à 692) | Seules les phases 1, 4, 5 et 7 ont un ordre interne, fixé par leurs fiches. En phase 5, l'ordre est « prix, puis production, puis ménages, investissement, État » : le bloc 6 propose la ligne 3 après le bloc 2, sans lire les achats des ménages ni ceux de l'État. Les phases 2, 3 et 6 n'ont pas d'ordre interne : le bloc 6 n'y lit rien de ce qu'un autre bloc y écrit, ni y\* en phase 2, ni la réponse de la banque en phase 3, ni T_F ou les intérêts écrits en phase 6. Y déclarer un ordre modifie la liste de la l. 487 et `tab:phases` | Décision citant M22 et ADR (issue sensible, comme pour l'ADR 0007) |
| Frontière des blocs 2 et 6 (Q4) | M24, Q4 (fiche 2 § 3.N-5 et § 8) ; `sec:production-capital` (l. 675) | K^vol est tenu par le bloc 2 (N10, phase 5) ; I^vol est le volume livré après rationnement (N6). Le bloc 6 décide l'investissement visé (phase 2), lit K^vol à l'ouverture et écrit les lignes 3 et 8 en valeur comptable. La fiche **confirme** cette répartition, ou propose une révision par une décision citant M24 | Décision citant M24 |
| Valeur comptable du capital | `sec:cadre`, encadré de portée (l. 521) ; `sec:production-capital` (l. 676 à 680) ; visa du mainteneur du 03/10/2026 (fiche 2 § 3.N-5, amendement de notation) | K est un poste en valeur comptable, sans réévaluation ; il ne varie que par les lignes 3 et 8. ρ̄_K = K/(p K^vol) = (n_a γ + δ)/[n_a(((1 + g)(1 + π̄))^{1/n_a} − 1) + δ], avec γ = (1 + g)^{1/n_a} − 1, π̄ étant le glissement annuel stationnaire. ρ̄_K vaut 0,7786 à g = π̄ = 2 % et δ = 5 %, et 0,4214 à π̄ = 10 % (*révisé par M25 (b)*, 03/10/2026 ; fiche 2 § 3.N-5 ; 0,7791 et 0,4221 sous la conversion linéaire de g). Une évaluation au prix courant demanderait une ligne de réévaluation. Une correction ad hoc de l'amortissement relèverait des instabilités 10 et 11 | Décision citant M22 (ligne de réévaluation) |
| Capacité normale et taux d'utilisation | M24 (e) ; `sec:production-stationnaire` (l. 728, 739) ; condition 4 de `jeu` (fiche 2 § 9.5) ; #37 | y^cap = K^vol/(n_a κ) est un indicateur sans plafond. t̄u = n_a κ y/K^vol est « fixé par le bloc investissement » ; l'état initial résolu prend K^vol_0 = n_a κ y_0/t̄u. La fiche dit ce que tu déclenche ; sinon tu sort de la restitution, au plus tard à la décision de la fiche. Un plafond de capacité réviserait M24 (e) | Décision citant M24 |
| Technique et croissance | M24 (f) ; `sec:production` (l. 592, 616, 741) | Technique de Leontief en travail : le capital ne contraint pas la production. pr suit une tendance exogène ; g = n_a[(1 + g_pr/n_a)(1 + g_N/n_a) − 1]. Un canal d'offre qui rend pr, g ou la production dépendants de l'accumulation révise M24 (e) ou (f) | Décision citant M24 |
| Sous-colonnes des entreprises (#36) | Décision du mainteneur du 02/10/2026 sur #36 (voie (i), PR #35) ; `sec:cadre-flux` (l. 292, 296 ; légende l. 304) ; fiche 2 § 3.N-10 et § 9.8 | **Voie (i)**, en vigueur : chaque colonne somme à zéro, les deux sous-colonnes réunies ; « prise seule, une sous-colonne des entreprises n'est pas nulle en général ». La sous-colonne courante vaut les profits non distribués FU, soit 0,33059 % de V_F par pas à l'état stationnaire (g = π̄ = 2 % ; *révisé par M25 (b)*, 03/10/2026 ; fiche 2 § 3.N-10). **Voie (ii)**, ligne « profits non distribués » : elle modifie `tab:matrice-flux`, contrat partagé (`docs/agents/routage.md` § 4.2). La clause de la l. 292 et la légende sont alors à reprendre, et la sortie de `verifier_matrices.py --strict` change | Décision citant M22 et ADR |
| Lignes et règle de caisse | `tab:matrice-flux` ; `sec:cadre-caisse` (l. 458) ; `sec:production-phases` (l. 696) | Les lignes 3 et 8 reviennent au bloc 6 ; la ligne 18 s'exécute en phase 3 avec le bloc 7. Les lignes 9 (intérêts sur crédits) et 14 (dividendes des entreprises) s'exécutent en phase 6 ; leur propriétaire est à déclarer. T_F (ligne 7) relève de la fiche 9. La ligne 17 (ΔD_F) est une contrepartie de règlement, jamais décidée. Les entreprises paient en dépôts ; « un payeur ne paie pas plus que son moyen de paiement » ; la part non payée est une ligne nommée du bloc payeur ; « le crédit (phase 3) précède les règlements » ; chaque bloc déclare son ordre de priorité des paiements | Décision citant M22 si une ligne s'ajoute |
| Bornes | #38, lecture (ii) ; `CONVENTIONS.md` § 2.4 ; `docs/exigences.md` § 2.7 | Une borne à seuil libre a un paramètre déclaré et un motif contre un mécanisme. Une contrainte de conservation ou de technique n'a pas de paramètre : elle est déclarée dans les `\limites`, avec son activité à l'état stationnaire et un test | Décision citant #38 |
| Fiches 3 et 4 | Fiche 3, critère 8 (c) ; fiche 4, critères 1 (c), 5 (c) et 8 (validés le 03/10/2026) | La masse salariale excédentaire réduit FU. Un amortissement compté dans la base de coût du prix n'est pas la ligne 8. La fiche 4 instruit une variante où le prix réagit à tu et transmet la condition 4 de `jeu` à la fiche 6 | M25 et M26 |
| Taux et anticipations | `docs/blocs/README.md` § 2 et § 3 ; `tab:instruments` (l. 253) | La fiche déclare les variables qu'elle consomme : i_L, fixé par le bloc banque, et une anticipation d'inflation si la règle emploie un taux réel. La fixation de i_L relève de la fiche 7, la loi de formation des anticipations de la fiche 8 | — |
| Fiche 5, décidée avec la fiche 6 | Décision du mainteneur du 03/10/2026 (décisions par paires) | Les dividendes sont un revenu des ménages. L'épargne des ménages et le besoin de financement des entreprises se bouclent dans l'état stationnaire conjoint | M27 et M28, prises ensemble |
| Statut des faits | Décision P1 du 03/10/2026 ; `CONTEXT.md` | Statuts S+O, O, R, L, V ou V+O. Un fait V mesuré sur le prototype v2.0 reste un fait de la première tentative. L'état D1 n'est pas versé | — |

### 1.2 Ce que le bloc doit produire

Les symboles **ne sont pas fixés** : ils le seront à l'instruction, sous le critère 15. Plusieurs sont déjà pris :
- ℓ est l'indice de ligne : le levier ne s'écrit pas ℓ ;
- F est une marque de secteur : les profits ne s'écrivent pas F ;
- κ et δ sont pris ;
- r désigne le taux réel ex post, i − π (`tab:symboles`).

| Grandeur | Définition | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| Investissement visé | Plan de dépense d'équipement du pas, écrit en phase 2, servi au prorata par le bloc 2 | u.m. par pas | — | le pas, phase 2 |
| Investissement I_t (ligne 3) | p_t·I^vol_t, où I^vol_t est le volume livré après rationnement (N6, bloc 2) ; entreprises « courant » +I, « capital » −I | u.m. par pas | — | le pas, phase 5 ; restitution : le tour, et la somme sur 12 tours |
| Investissement non servi | (plan − I)/plan | fraction | plan du pas | le pas, phase 5 ; le tour |
| Taux d'investissement | Somme des I sur somme du PIB nominal (C + G + I + ΔIN) | fraction | PIB nominal sur 12 tours | 12 tours |
| Amortissement (ligne 8) | δK_t/n_a sur la valeur comptable d'ouverture ; « courant » −, « capital » + | u.m. par pas | — | le pas, phase 6 |
| Rapport capital / PIB | Définition à déclarer (Q2). Trois candidates : comptable (K) ou en volume valorisé (p K^vol), rapportés au PIB annuel ; ou en volume, K^vol/(n_a y) | années | test zéro : 12 × PIB nominal du pas (M22, lecture (e)) ; restitution : PIB des 12 derniers tours ; volume : n_a y | ouverture (test zéro) ; clôture (restitution) |
| Rapport ρ̄_K | K/(p K^vol) à l'état stationnaire | fraction | p K^vol | état stationnaire ; publié |
| Taux d'utilisation tu, t̄u | tu = y/y^cap (bloc 2, phase 4) ; t̄u, sa valeur stationnaire, est fixée par le bloc 6 | fraction | y^cap du pas | le pas, phase 4 ; le tour |
| Demande de crédit | Crédit nouveau demandé dans le pas | u.m. par pas | — | le pas, phase 3 |
| Crédit nouveau ΔL (ligne 18) | Crédit accordé et exécuté ; la demande non satisfaite est publiée | u.m. par pas ; fraction | demande du pas | le pas, phase 3 |
| Levier | L rapporté au capital, dénominateur à déclarer (K comptable ou p K^vol) ; les deux diffèrent du facteur ρ̄_K à l'état stationnaire | fraction | K ou p K^vol d'ouverture | ouverture ; le tour |
| Dépôts des entreprises D_F | Poste qui ne varie que par la ligne 17 (contrepartie de règlement) | u.m. ; années de PIB | 12 × PIB nominal du pas | ouverture |
| Dividendes Div_F (ligne 14) | Part du résultat courant distribuée aux ménages ; propriétaire de la ligne à déclarer (Q6) | u.m. par pas | — | le pas, phase 6 ; 12 tours |
| Profits non distribués FU | Somme de la sous-colonne « courant » (fiche 2 § 3.N-10). C'est le résultat courant après distribution : ventes − cm·v − (WB − UC·y) − T_F − δK/n_a − intérêts nets − Div_F | u.m. par pas ; fraction par pas | V_F d'ouverture | le pas, phase 6 ; valeur stationnaire : 0,33059 % de V_F par pas (*révisé par M25 (b)*, 03/10/2026 ; fiche 2 § 3.N-10) |
| Taux de distribution | Somme des Div_F sur somme des résultats courants avant distribution | fraction | résultat courant sur 12 tours | 12 tours |
| Coût du capital, taux réel du crédit, rentabilité | Si l'option en emploie : définition et anticipation consommée | fraction par an | selon l'option | le pas |
| Variables d'état du bloc | Par exemple : rentabilité lissée, investissement retardé, profit lissé, tu ou y du pas précédent | unité propre | — | ouverture |

### 1.3 Ce qu'il lit

- **Ouverture** :
  - ses variables d'état ;
  - K^vol_t (bloc 2) ;
  - les postes K_t, L_t et D_F,t ;
  - v^e_t et IN^vol_t, si la règle anticipe la demande ;
  - y ou tu du pas précédent, s'ils figurent dans l'état (critère 13) ;
  - le registre des prix.
- **Phase 1** :
  - les taux arrêtés (règle de taux, bloc 8) ;
  - l'anticipation d'inflation (bloc 8), si elle est consommée ;
  - P_t et π_t ;
  - W_t (bloc 3), si la règle lit un coût.

  `tab:phases` (l. 504) fait écrire en phase 1 « travail, prix, banque centrale », sans le bloc banque. Le taux du crédit lu par le plan de la phase 2 est donc celui de l'ouverture, sauf retouche de la table (Q8).
- **Phase 2** : rien de ce qu'un autre bloc y écrit, la phase n'ayant pas d'ordre interne.
- **Phase 3** : la réponse de la banque, seulement dans la lecture qui déclare un ordre interne (Q7).
- **Phase 5** : p_t (bloc 4) et le volume livré v_{F,j,t} = I^vol_t (bloc 2), écrits avant lui dans la phase.
- **Phase 6** : rien de ce qu'un autre bloc y écrit, sauf ordre interne déclaré (Q6). Les intérêts et les taux du pas sont connus dès l'ouverture et la phase 1.
- **Leviers du joueur** :
  - aucun levier propre au socle sans décision ;
  - transitent par le bloc : le taux (par i_L et le coût du capital), la dépense publique (par la demande et tu) et l'impôt sur les entreprises (ligne 7, fiche 9) ;
  - l'investissement public, un crédit d'impôt ou l'accumulation planifiée (mode planifié, J7 ; #37) font l'objet de Q12.
- **Décisions qui le contraignent** :
  - M7, M13 ;
  - M22 (ADR 0005) et M24 (ADR 0007) ;
  - décision du 02/10/2026 sur #23 (indices c, j, k) ;
  - décision du 02/10/2026 sur #36 (voie (i)) ;
  - décision du 03/10/2026 sur #38 (lecture (ii)) ;
  - visa du 03/10/2026 sur ρ̄_K.

### 1.4 Frontières

- **Production et stocks (fiche 2, décidée)** :
  - Q4 ;
  - K^vol, I^vol, tu, y^cap, κ et t̄u ;
  - rationnement proportionnel du plan d'investissement.

  Critères 3, 4 et 10.
- **Prix (fiche 4, décidée avec la fiche 3)** :
  - conséquence de tu sur le prix (critère 8 de la fiche 4, condition 4 transmise) ;
  - un amortissement dans la base de coût n'est pas la ligne 8 ;
  - la marge alimente le résultat courant.

  Critères 4 (c) et 10.
- **Travail et salaires (fiche 3)** : la masse salariale excédentaire réduit FU. Critère 2.
- **Ménages (fiche 5, décidée avec la fiche 6)** :
  - Div_F est un revenu des ménages ;
  - l'épargne des ménages et le financement des entreprises se bouclent ;
  - la variable qui ferme l'égalité de l'épargne et de l'investissement est à déclarer.

  Critère 5 (c).
- **Banque commerciale (fiche 7, `monnaie`) : frontière crédit.**
  - Chez `macro` : la demande de crédit et le financement de l'investissement.
  - Chez `monnaie` : l'offre, i_L, les fonds propres et le rationnement.
  - Lignes 18 et 9.

  Critères 3 (b) et 11 ; avis de `monnaie` (§ 6).
- **Banque centrale et anticipations (fiche 8, `monnaie`)** :
  - anticipation consommée, si la règle emploie un taux réel ;
  - boucle taux – investissement – inflation – règle de taux.

  Critères 7 (e) et 11 (d).
- **État et dette (fiche 9)** :
  - T_F (ligne 7) et son assiette, qui comprend la ligne 8 comptable ;
  - le capital public comme canal d'offre éventuel (#37) ;
  - la dépense publique reste un achat (ligne 2), non un capital des entreprises.

  Critère 10.
- **`jeu`** : critères 10 (c) et 12 ; avis au § 7.

### 1.5 Ce que la fiche ne tranche pas, et questions ouvertes

**Hors du périmètre** :
- l'offre de crédit, i_L, les fonds propres de la banque et le refinancement (fiche 7) ;
- la loi de formation des anticipations et la crédibilité (fiche 8) ;
- la fiscalité des entreprises et le capital public (fiche 9) ;
- les actions, le financement par actions, les faillites et l'immobilier (J6) — sans actions, V_F n'est détenue par aucun secteur au socle, ce qui se déclare ;
- les secteurs, les intrants et le prix relatif du capital (J5 à J7 ; J = 1, M24) ;
- l'accumulation planifiée (J7) ;
- les valeurs numériques de l'état stationnaire et la calibration (J3) : la fiche vérifie qu'une forme fermée existe ;
- les bandes du test zéro : proposées ici, confirmées avec O1 avant l'essai (M19).

**Questions ouvertes à instruire** :
- **Q1 — Q4 de la fiche 2.** La fiche confirme la répartition des blocs 2 et 6, ou propose une révision par une décision citant M24.
- **Q2 — Définition de K/Y.** Comptable, en volume valorisé ou en volume : unité, dénominateur, fenêtre, relation à ρ̄_K. La fiche dit laquelle sert à O1, laquelle à la calibration, laquelle est restituée au joueur (critère 4 (a)).
- **Q3 — κ, t̄u et K^vol/(n_a y).** Lequel est un paramètre, lesquels sont des résultats. Un seul ancrage du taux d'utilisation, commun avec la fiche 4 (critère 4 (c)).
- **Q4 — #36, voies (i) et (ii).** Les deux sont instruites (critère 2).
- **Q5 — #37.** Canal d'offre de l'investissement, ou absence de levier d'offre au socle, déclarée (critère 10).
- **Q6 — Règle de financement.**
  - Distribution : partage entre Div_F et FU.
  - Demande de crédit.
  - Ancrage de L et de D_F.
  - Ordre de priorité des paiements des entreprises et ligne nommée de la part non payée.
  - Propriétaire des lignes 9 et 14.
  - Triangularité de la phase 6.
- **Q7 — Phase 3.** Deux lectures sont instruites :
  - (a) la banque publie ses conditions (taux, plafond ou règle d'octroi) à l'ouverture ou en phase 1, et le bloc 6 propose seul la ligne 18 : aucun ordre interne n'est nécessaire ;
  - (b) « investissement, puis banque » : ordre interne nouveau de la phase 3, décision citant M22 et ADR.

  Dans les deux cas, la fiche dit quel plan le bloc 2 sert en phase 5. Le plan de la phase 2 est celui que lit aujourd'hui `tab:production-phases` (l. 714). Un plan financé, réécrit en phase 3, demanderait de compléter la colonne « Lisent » de `tab:phases`, ligne 5 (« phases 2 et 4 »), retouche à qualifier par `architect`.
- **Q8 — Variables consommées.** Date de i_L : à l'ouverture, ou en phase 1, ce qui demande d'ajouter le bloc banque à la phase 1 de `tab:phases`. Anticipation d'inflation, si un taux réel est employé, avec un symbole distinct de r.
- **Q9 — Fermeture.** Quelle variable ferme l'égalité de l'épargne et de l'investissement à l'état stationnaire : tu, la répartition, le taux réel ou la propension des ménages. Question conjointe avec la fiche 5 (critère 5 (c)).
- **Q10 — Variantes à instruire.**
  - **A** (v1.5) :
    - `eq:invest` (l. 562 à 568, § `sec:invest`, l. 559 ; Γ, plafond 2δ et q̄, l. 575 à 581 ; Λ et accumulation avec délai de livraison T_K, l. 584) ;
    - `eq:profit`, `eq:cash` et `eq:div` (l. 545 à 547, § « Compte d'exploitation, trésorerie et dividendes », l. 543) ;
    - ordre « dividendes, puis investissement », l. 555.
  - **B** (v2.0), `investment_mode='legacy_q'`, dans `model.py` :
    - taux réel long, l. 857 ; q, l. 862 ; Λ, l. 864 ;
    - utilisation et seuil, l. 866 et 867 ;
    - accélérateur, l. 870, désactivé par défaut, l. 301 ;
    - q̄ et réponse saturée, l. 872 et 873 ;
    - cash-flow, l. 874 à 877 (`iota_Pi` = 0 par défaut, l. 150) ;
    - plafond, l. 880 ; investissement, l. 881 ; ajustement partiel, l. 890 ;
    - financement, l. 891 à 897 ;
    - remboursement, l. 1030 à 1036 ;
    - rétention et dividende de P1, l. 1037 à 1043.

    Coefficients effectifs du profil D1 (faits § 1.1) : `investment_mode='legacy_q'` ; P1 actif (`payout_mode='leverage_target'`, `ell_star` = 0,3, `lam_ell` = 0,1), contre `payout_mode='psi'` par défaut (l. 116). La branche active se vérifie avant toute citation. La cible de capital à coût minimal (`investment_mode='sales_cost'`, `closure.py` l. 49 à 58 et 73, inactive dans D1) suppose une technique substituable : sous M24, elle réviserait la technique.
  - **Au moins une approche nouvelle**. La forme de Godley et Lavoie (2007, chap. 11, « A Growth Model Prototype », p. 378-444) est à lire ; la v2.0 la cite pour P1 (l. 116, L). S'y ajoute au moins une règle d'ajustement du stock de capital avec terme de tendance.
  - **Une variante sans retard**, où le capital visé est atteint dans le pas, comme référence (`docs/exigences.md` § 2.7).
- **Q11 — δ.** Valeur, unité et source ; un seul δ pour N10 et pour la ligne 8.
- **Q12 — Leviers d'investissement** (investissement public, crédit d'impôt, accumulation planifiée). Instruits comme options, ou renvoyés au catalogue des leviers (J4) et au mode planifié (J7), avec leur interface notée.

## 2. Critères d'évaluation, écrits avant l'instruction

**Statut** : proposés par `macro` le 03/10/2026, validés par le mainteneur le 03/10/2026, avec les amendements ci-dessous (jalon 1 de #42). La liste est fermée : elle ne se déplace pas après observation (`docs/exigences.md` § 2.5). Un amendement adopté avant l'instruction se consigne sous le tableau.

Correspondance avec le gabarit :

| Critère du gabarit | Critère de la fiche |
|---|---|
| 1 | 1 |
| 2 | 5 et 6 |
| 3 | 7 |
| 4 | 14 |
| 5 | 12 |
| 6 | 9 et 13 |

Critères propres au bloc : 2, 3, 4, 8, 10, 11, 15, 16 et 17.

Sont des **exigences** (ils peuvent écarter une option) :
- 1, 2, 3, 4, 5, 6 ;
- 7 (a) à (d), pour la stabilité ;
- 8, 9 ;
- 10 (a) et (b) ;
- 11 (a) à (d) ;
- 12 (b) ;
- 13 (sans historique ni drapeau) ;
- 14 (sans itération) ;
- 15 et 17.

Sont des **mesures** (elles décrivent sans écarter) :
- 7 : la période et la demi-vie de (b) et (c), et (e) ;
- 10 (c) ;
- 12 (a), (c) et (d) ;
- 13 (décompte) ;
- 14 (décompte) ;
- 16.

| N° | Critère | Ce qui est attendu (seuil ou forme du verdict) | Par quoi on le vérifie | Qui | Quand |
|---|---|---|---|---|---|
| 1 | Cohérence stock-flux (gabarit 1 ; `macro`) — **exigence** | (a) Flux proposés par le bloc : ligne 3, I = p_t·I^vol_t, entreprises « courant » +I et « capital » −I, en phase 5 ; ligne 8, δK_t/n_a sur la valeur comptable d'ouverture, « courant » − et « capital » +, en phase 6 ; ligne 18, demande présentée en phase 3, le montant exécuté résultant de l'offre (fiche 7) ; ligne 14, si Q6 la donne au bloc 6. Signatures de `tab:portes-monnaie` inchangées. Toute autre ligne est déclarée avec sa phase et sa signature : c'est un contrat partagé, donc une décision citant M22 (pour la ligne FU, voir le critère 2). (b) Aucun poste n'est ajouté. K ne varie que par les lignes 3 et 8 (l. 521) ; I^vol et K^vol sont des variables, non des postes. L ne varie que par la ligne 18, D_F que par la contrepartie de règlement (ligne 17) : aucun solde résiduel, ni D_F ni L n'est obtenu par différence. V_F est calculée deux fois. (c) La contrainte budgétaire des entreprises (sous-colonnes réunies) est écrite sur un pas, ΔD_F − ΔL = FU − (I − δK/n_a) − ΔIN, avec FU selon la fiche 2 § 3.N-10 et la part qui revient à chaque bloc. (d) **Règle de caisse des entreprises** (`sec:cadre-caisse`, l. 458) : ordre de priorité des paiements en dépôts (WB en phase 4, I en phase 5, intérêts, impôts et dividendes en phase 6), bloc qui le déclare (Q6), ligne nommée qui porte la part non payée ; D_F ≥ 0 à chaque paiement | Matrice des flux de l'option, en tableau. Cas à la main sur un pas, crédit demandé accordé puis refusé de moitié : lignes 3, 8, 14, 17 et 18, D_F, L, et V_F par le stock et par les flux. Si une table change : `uv run python outils/verifier_matrices.py --strict <copie>`, sortie citée | `macro` ; `monnaie` ((a), ligne 18) | fiche ; J3 (identités, ε = 1e−12 × S, M22) |
| 2 | Sous-colonnes des entreprises et profits non distribués (#36 ; Q2 de la fiche 2 ; `macro`) — **exigence** | (a) Les deux voies sont instruites. **Voie (i)** : `tab:matrice-flux` et la clause de `sec:cadre-flux` (l. 292) sont inchangées ; FU reste la somme de la sous-colonne « courant ». **Voie (ii)** : une ligne « profits non distribués », entreprises « courant » −FU et « capital » +FU, de somme nulle, sans effet sur M ni sur H. La fiche déclare son symbole, sa phase, le bloc qui la propose, et dit si le noyau l'exécute comme une ligne (sans mouvement d'instrument) ou si elle reste une ligne de lecture de la table. La clause de la l. 292, la phrase de la l. 296 et la légende (l. 304) sont reprises ; `tab:portes-monnaie` reçoit la ligne, de signature nulle. (b) La voie (ii) est un contrat partagé (`docs/agents/routage.md` § 4.2). La fiche dit ce qu'elle rend vérifiable que la voie (i) ne rend pas (chaque sous-colonne nulle, FU lu dans une ligne), face à son coût (une ligne non monétaire, un ADR), au regard du principe de simplicité. Si elle est recommandée, la décision cite M22 et un ADR rédigé par `architect`. (c) **Sortie de `verifier_matrices.py --strict`**. Avant, à `4aee609` : « tab:matrice-bilans : 9 lignes, 6 colonnes, 44 termes ; tab:matrice-flux : 28 lignes, 6 colonnes, 62 termes ; tab:portes-monnaie : 28 lignes, 3 colonnes, 31 termes ; Aucun écart. » (commande au Retour). Sous la voie (i), la sortie reste identique (`cmp`). Sous la voie (ii), sur une copie de la spécification, le changement attendu se limite à une ligne de plus dans `tab:matrice-flux` et dans `tab:portes-monnaie`, avec les termes de la ligne FU ; tout autre écart arrête le circuit. (d) La valeur stationnaire de FU (0,33210 % de V_F par pas à g = π̄ = 2 %, fiche 2 § 3.N-10) est reprise, et le taux de distribution stationnaire écrit en forme fermée dans les deux voies | Rédaction des deux voies ; `uv run python outils/verifier_matrices.py --strict <copie>`, sortie citée avant et après | `macro` ; `architect` (ADR, si voie (ii)) | fiche ; M28 |
| 3 | Contrats hérités, phases et lectures (tableau du § 1.1 ; ADR 0005 et 0007 ; Q4, Q6, Q7 ; `macro`, `monnaie` pour (b)) — **exigence** | (a) L'investissement visé est écrit en phase 2 ; il ne lit que l'ouverture et la phase 1, rien d'autre de la phase 2 (en particulier ni y\* ni N\* du pas). Un plan qui exigerait y\* du pas demande un ordre interne de la phase 2, donc une décision citant M22 et ADR. (b) **Phase 3** (Q7) : la triangularité de l'échange entre demande et offre est déclarée par l'une des deux lectures instruites, et le plan servi en phase 5 est identifié (plan de la phase 2, ou plan financé de la phase 3, avec la retouche de `tab:phases` qu'il implique). (c) La ligne 3 est proposée en phase 5, après le bloc 2, sur v_{F,j,t}·p_t ; le bloc ne lit ni C ni G du pas. (d) La ligne 8 est assise sur K_t d'ouverture. Si Div_F (ligne 14) revient au bloc, il ne lit en phase 6 ni T_F ni les intérêts écrits dans la phase par les blocs 9 et 7, sauf ordre interne déclaré, donc décision citant M22. Une distribution assise sur des encours d'ouverture, des taux de la phase 1 ou un résultat retardé l'évite. (e) Q4 est confirmée, ou une révision est proposée avec la décision citant M24 qu'elle exige. (f) tu_t est écrit en phase 4 : une règle de la phase 2 ne lit que tu ou y du pas précédent, variable d'état déclarée (critère 13). (g) La matrice des lectures reste triangulaire | Tableau phase → lit / écrit par option, pour les phases 2, 3, 5 et 6, avec les blocs 2, 7 et 9 ; triangularité vérifiée à la main | `macro` ; `monnaie` ((b)) | fiche ; J2 (test de triangularité de l'ordonnanceur) |
| 4 | Rapport capital / PIB, ρ̄_K, κ, t̄u et δ (fiche 2 § 3.N-5 et § 9.8 ; Q2, Q3, Q11 ; `macro`) — **exigence** | (a) **Définition de K/Y déclarée**, avec son unité (années), son dénominateur et sa fenêtre, parmi : (i) comptable, K rapporté au PIB nominal annuel ; (ii) volume valorisé, p K^vol rapporté au même PIB ; (iii) volume, K^vol/(n_a y). Au test zéro, le rapport est stock d'ouverture / (12 × flux du pas) ; à la restitution, stock de clôture / somme des 12 derniers tours (M22, lecture (e)). Les relations sont écrites en forme fermée : (i) = ρ̄_K × (ii) ; (ii)/(iii) = p·y / PIB nominal du pas. **Illustration** : pour K^vol/(n_a y) = 3 ans, K/(n_a p y) vaut 2,3372 ans à π̄ = 2 % et 1,2662 an à π̄ = 10 % (g = 2 %, δ = 5 %, n_a = 12 ; commande au Retour). À capital physique égal, le rapport comptable baisse donc de 46 % quand π̄ passe de 2 % à 10 %. La fiche dit quelle définition sert à O1 (« ratios capital/PIB à ±10 % », `docs/exigences.md` § 1.3), laquelle sert à la calibration et laquelle est restituée au joueur. La comptabilité nationale évaluerait le capital au coût de remplacement courant : à vérifier sur OCDE (2009), *Measuring Capital*, existence vérifiée, non lu. (b) **ρ̄_K** : forme reprise de la l. 678, avec sa dépendance à n_a, déclarée à l'ordre π̄/n_a : 0,7782, 0,7791 et 0,7794 pour n_a = 4, 12 et 52 à π̄ = 2 % ; 0,4193, 0,4221 et 0,4231 à π̄ = 10 % (commande au Retour). Toute grandeur de la règle assise sur K comptable (levier, rentabilité comptable, coût du capital) hérite de la dépendance à π̄ par ρ̄_K : elle est écrite et chiffrée à π̄ = 2 % et 10 %. Une correction de la ligne 8 vers le prix courant relève des instabilités 10 et 11 (critère 7 (a)). (c) **κ et t̄u** : l'identité t̄u = κ / [K^vol/(n_a y)] ne laisse qu'un degré de liberté entre κ, t̄u et K^vol/(n_a y). La fiche dit lequel est un paramètre et lesquels sont des résultats. Si une règle ramène tu vers un niveau normal, ce niveau est t̄u, ancre unique, que la fiche 4 lit sans paramètre propre (critère 8 (a) de la fiche 4). Si K^vol/(n_a y) résulte du coût du capital, t̄u est un résultat publié et κ se calibre sur un taux d'utilisation établi, défini comme celui du socle ou avec l'écart de définition déclaré (source candidate : Federal Reserve, statistique G.17, existence vérifiée, non lue). (d) **δ** : valeur, unité (par an) et source ; un seul δ pour N10 (volume) et pour la ligne 8 (valeur comptable), conformément à `sec:production-capital` (l. 673) | Calcul à la main ; formes fermées ; sources citées | `macro` | fiche ; J3 (calibration) |
| 5 | État stationnaire en forme fermée (gabarit 2 ; `macro`) — **exigence** | (a) **Trajectoire de référence**, celle des critères 3 (a) des fiches 3 et 4 : volumes en croissance de g/n_a par pas, prix en hausse de (1 + π̄)^{1/n_a} − 1 par pas, π̄ étant le glissement annuel stationnaire. N10 y donne exactement I^vol/K^vol = (g + δ)/n_a par pas, soit g + δ = 7 % par an pour g = 2 % et δ = 5 %, quel que soit n_a. Sur cette trajectoire, chaque grandeur du bloc a sa valeur stationnaire en forme fermée, sans simulation : K^vol/(n_a y) ; K/Y dans les trois définitions du critère 4 ; t̄u ; taux d'investissement ; levier ; D_F/(12 × PIB) ; taux de distribution ; FU/V_F ; V_F/(12 × PIB) ; rentabilité et coût du capital, si la règle en emploie. Chaque variable d'état a sa valeur stationnaire, d'où se déduit l'état initial résolu (K^vol_0 = n_a κ y_0/t̄u, `sec:production-stationnaire` l. 739 ; K_0 = ρ̄_K p_0 K^vol_0 ; L_0 ; D_F,0). (b) **Indépendance envers n_a** : K^vol/(n_a y), le taux d'investissement, t̄u et le taux de distribution n'en dépendent pas. Les dépendances par ρ̄_K et ρ̄_IN sont déclarées ; toute autre est écrite et chiffrée pour n_a = 4, 12 et 52, avec la condition qui la supprime. (c) **État stationnaire conjoint avec la fiche 5** (paire M27-M28). La fiche écrit la condition que son état stationnaire impose aux autres blocs : sur la trajectoire de référence, la somme des capacités de financement des secteurs est nulle. Elle dit **quelle variable ferme** l'égalité de l'épargne et de l'investissement : tu (fermeture kaleckienne), la répartition (fiche 4), le taux réel (fiche 8 ; acquis « l'épargne n'y entre pas (bouclage wicksellien) », R, faits § 8) ou la propension des ménages (fiche 5). Une règle qui vise t̄u pendant que tu ferme le modèle surdétermine l'état stationnaire : cela se déclare. Le point est **contesté** ; sources candidates, existence vérifiée, non lues : Skott (2012), *Metroeconomica* 63(1), 109-138 ; Hein, Lavoie et van Treeck (2012), *Metroeconomica* 63(1), 139-169 ; Lavoie (2014), *Post-Keynesian Economics: New Foundations*, Edward Elgar, chapitre « Accumulation and Capacity ». L'état stationnaire conjoint est calculé en forme fermée quand la fiche 5 est « avis rendus », avant M27 et M28. (d) Le bloc ne fixe ni π̄ (fiche 8) ni g (M24 (f)), sauf si un canal d'offre est retenu (critère 10) : g endogène a alors sa forme fermée, et sa dépendance aux leviers est écrite | Calcul à la main dans la fiche. Au J3, script contre moteur : un pas sans choc depuis l'état initial résolu laisse chaque variable d'état du bloc sur sa trajectoire stationnaire à **1e−10 près en relatif** (seuil des fiches 2 à 4, reconduit) | `macro` ; `monnaie` ((c), taux réel) | fiche ; avant M27-M28 ; J3 |
| 6 | Aucune vitesse d'ajustement ne détermine l'état d'arrivée (`docs/exigences.md` § 2.7 ; `macro`) — **exigence** | (a) Aucune vitesse, ni la durée du pas, n'apparaît dans les formes fermées du critère 5. **Cas à examiner explicitement** : (i) un ajustement partiel du capital vers un capital visé qui croît de g/n_a par pas laisse un écart stationnaire fonction de la vitesse, sauf terme de tendance (g + δ) ; c'est la même construction que `sec:production`, l. 617. (ii) La v1.5 écrit q\* = 1 + g/(ι Γ Λ Λ^Bk) (l. 577 à 581), et l'acquis K/Y = part du capital / (q\*(r_L + ρ_E + δ)) (R, faits § 8) fait dépendre K/Y de ι, sensibilité de l'investissement net à q (fraction du capital par an) ; la fiche dit si ι est une vitesse au sens du § 2.7 et en tire la conséquence. (iii) Dans la v2.0, `lam_I` (l. 890 ; 1,0 par défaut, l. 267), `lam_qbar` (l. 268), `lam_r` (l. 299), `lam_ell` (l. 118) et `lam_div` (l. 268) : leur base (semaine ou an) est lue dans le code, convertie en base annuelle et confrontée à λ ≤ n_a. Si une dépendance subsiste, elle est écrite, chiffrée pour la vitesse divisée et multipliée par 2, avec la condition qui la supprime. (b) **Aucun intégrateur sans ancre** : D_F, contrepartie de règlement, et L ont chacun une ancre (cible de levier, cible de trésorerie, ou autre). Sinon, leur niveau stationnaire dépend de l'état initial ou du chemin : c'est un continuum d'équilibres, documenté et soumis au mainteneur. Pour mémoire, « sans les deux derniers termes, le levier tend vers zéro dans les deux moteurs » (P1, R, faits § 8). Une moyenne mobile (q̄ de la v1.5, l. 564) a une valeur stationnaire explicite. (c) La fiche dit quelles grandeurs le bloc ne détermine pas : le rythme d'inflation (fiche 8), et g (M24 (f)) sauf critère 10 | Calcul à la main sur les formes fermées. Au J3, depuis l'état initial résolu : dépense publique +1 % pendant 12 tours, puis deux branches où toutes les vitesses du bloc sont multipliées par 0,5 et par 2 (dans λ ≤ n_a). Écart relatif de chaque ratio du bloc entre les deux branches au plus de **1e−6 après 720 pas** (seuil reconduit) | `macro` | fiche ; J3 |
| 7 | Stabilité (gabarit 3 ; `macro` ; (d) et (e) avec `monnaie`) — **exigence** pour (a), et pour (b) à (d) quant au rayon spectral ; **mesure** pour la période et la demi-vie de (b) et (c), et pour (e) | (a) **Instabilités et faits connus** (faits § 6 à 8), non réintroduits sans fait nouveau. N° 10 (dépréciation au prix lissé, prix ×2,9, R) et n° 11 (dépréciation indexée, R) : en v3, toute réévaluation de K ou de la ligne 8 hors d'une ligne déclarée en relève. N° 1 (construction répondant au niveau d'un rapport de prix, R) : sans objet sous J = 1, à vérifier pour toute règle qui répond au niveau d'un rapport du prix au coût. N° 4 (estimateur de r\* sans ancre, R), si la règle lit un taux naturel. N° 15 (un plafond produit un cycle, R), pour tout plafond d'investissement ou de capacité. N° 16 (tolérances absolues). Faits rapportés hors de la liste, examinés : l'accélérateur crée des cycles de Samuelson-Hicks d'écart-type 3 à 7 points, et un taux long lissé un cycle de 8 à 12 ans (v1.5, l. 576, R) ; la v2.0 désactive l'accélérateur par défaut pour cette raison (`model.py` l. 301, L). L'hypothèse réfutée n° 4 (blocage de l'investissement en v1.7) n'est pas reprise. Acquis discutés : P1 (R) ; formule de K/Y (R) ; accélérateur financier inactif à la calibration de référence (v1.5, l. 582, R). (b) **Boucle propre du bloc** (capital, financement), à demande, prix et taux exogènes, au pas mensuel : valeurs propres de module **strictement inférieur à 1** pour la calibration proposée et pour chaque vitesse ×0,5 et ×2 ; module, demi-vie en tours, période si les racines sont complexes. (c) **Boucle investissement – demande – production** : système N1 à N7 de la fiche 2, avec la règle d'investissement et une demande induite d = A + m·y_{t−1} pour m = 0,5, 0,6, 0,7 et 0,8 (hypothèse ; m effectif fourni par les fiches 5 et 9 au J3), l'investissement entrant dans la demande. Rayon spectral < 1 pour la calibration proposée et pour les vitesses ×0,5 et ×2 ; période et demi-vie publiées. Une règle qui ramène tu vers t̄u est examinée explicitement au regard de l'instabilité harrodienne (critère 5 (c)). (d) **Dynamique de l'endettement des entreprises** : sous la règle de financement, le levier et D_F/(12 × PIB) sont stables pour i_L à sa valeur stationnaire et à +2 points maintenus (exigence à la calibration ; i_L exogène ; avis de `monnaie`). (e) **Boucle taux – investissement – inflation – règle de taux** (v1.5, l. 576 (ii), R) : mesurée quand la fiche 8 est instruite ; la fiche 6 publie l'interface (élasticité de l'investissement au taux, délai en tours) | Faits § 6 à 8, puis `tab:instabilites`. Valeurs propres calculées à la main ou par `uv run python`, commande et sortie citées | `macro` ; `monnaie` ((d), (e)) | fiche ; avant M27-M28 ; J3 ; fiche 8 ((e)) |
| 8 | Test zéro des ratios du bloc (`docs/exigences.md` § 2.6 ; O1 ; `macro`) — **exigence**, mesurée au J3 | Sur 60 ans (720 pas) sans choc depuis l'état initial résolu, pour plusieurs graines : la moyenne par blocs de 5 ans (60 pas) de chaque ratio reste dans sa bande autour de la valeur stationnaire résolue. **Bandes proposées**, à confirmer par le mainteneur avec O1 avant l'essai (M19) : K/Y dans la définition retenue au critère 4 (stock d'ouverture / (12 × PIB nominal du pas)), ±10 % en relatif (point de départ d'O1, `docs/exigences.md` § 1.3) ; taux d'utilisation ±0,02, **bande commune avec la fiche 2** (critère 6) ; taux d'investissement (somme des I sur somme du PIB nominal, 12 tours) ±1 point ; levier (L sur le dénominateur déclaré, à l'ouverture) ±10 % en relatif ; dépôts des entreprises (D_F d'ouverture / (12 × PIB nominal du pas)) ±10 % en relatif. Pour mémoire seulement, sans valeur de référence : D1 rapporte une dérive de K/Y de 3,41 % (bloc contre bloc de 5 à 10 ans), ramenée de 11,2 % par la préparation de 150 ans, et q̄ = 1,111 (R, faits § 2 ; la définition de K/Y n'est pas établie par la synthèse). Toute dérive depuis l'état résolu est un défaut | Au stade de la fiche, seul le préalable (critère 5) se vérifie ; au J3, test zéro du socle | `macro` ; mainteneur (bandes) | J3 |
| 9 | Bornes (gabarit 6 ; #38, lecture (ii) ; `CONVENTIONS.md` § 2.4 ; `macro`) — **exigence** | (a) Chaque borne de chaque option est classée par le critère de tri de `CONVENTIONS.md` § 2.4. **Non-négativité de l'investissement brut**, I^vol ≥ 0 : contrainte de technique si la fiche déclare dans la technique l'irréversibilité du capital installé (sous J = 1, un investissement négatif reconvertirait l'équipement en bien vendu) ; borne à seuil libre sinon. Le classement est motivé, et la forme de la règle rend la borne inactive à l'état stationnaire, marge chiffrée (I^vol/K^vol = (g + δ)/n_a > 0). **Contraintes de conservation** : D_F ≥ 0 (un dépôt négatif serait un crédit non déclaré ; `sec:cadre-caisse` l. 458) et L ≥ 0 (un crédit négatif serait un dépôt), déclarées dans les `\limites`, avec leur activité à l'état stationnaire et un test. **Bornes à seuil libre** : déclarées avec leur paramètre, motivées contre un mécanisme, avec leur activité à l'état stationnaire. Exemples dans la v1.5 : plafond min(·, 2δ) (l. 565, 581) ; Γ écrêté à [0, 1] sur [0,80 ; 0,95] (l. 566, 575) ; Λ écrêté à [0, 1] (l. 584). Exemples dans la v2.0 : plancher −0,5δ et plafond `inv_cap`·δ de l'investissement net (l. 880 et 881 ; `inv_cap` = 2,0, l. 302) ; utilisation écrêtée à [0 ; 1,5] (l. 866) ; croissance anticipée écrêtée à [−0,05 ; 0,10] (l. 870) ; taux de cash-flow (l. 875) ; dividende (l. 1040) ; seuil `ell_bar` + 0,4 (l. 901). (b) Un mécanisme est préféré à un plancher : la positivité de I^vol découle, quand c'est possible, de la forme de la règle. (c) **Instabilité 15** : aucune borne n'est active à l'état stationnaire ni dans les scénarios O2 (dépense publique +1 % et +5 %). Scénarios adverses : dépense publique −5 % pendant 12 tours, dimensionnée pour rendre l'investissement visé nul ou négatif ; refus de la moitié du crédit demandé pendant 12 tours (avec la fiche 7). Une borne qui s'y active cesse de l'être **au plus tard 12 tours après la fin du choc** et ne se réactive pas sans nouveau choc (seuil des fiches 3 et 4, reconduit). (d) Les conditions (λ ≤ n_a ; δ/n_a < 1) sont déclarées comme conditions, jamais comme écrêtages | Décompte des bornes par option, avec leur classement. Cas à la main : le choc adverse sur un tour (investissement visé, ligne 3, D_F). Au J3 ou au J4 : scénarios O2 et scénarios adverses | `macro` ; mainteneur (classement de I^vol ≥ 0, seuil de (c)) | fiche ; J3 ou J4 |
| 10 | Canal d'offre et taux d'utilisation (#37 ; condition 4 de `jeu`, fiche 2 § 9.5 ; fiche 4, critère 8 ; `macro`, `jeu`) — **exigence** pour (a) et (b), **mesure** pour (c) | (a) La fiche instruit au moins une variante où l'investissement agit sur l'offre, et la variante « aucun levier d'offre au socle », déclarée. Variantes candidates : capacité qui contraint (révise M24 (e) ; instabilité 15) ; productivité qui dépend de l'accumulation (révise M24 (f) ; source candidate : Arrow (1962), *Review of Economic Studies* 29(3), 155-173, existence vérifiée, non lu) ; capital public (fiche 9, interface seulement) ; choc de niveau prévu au J5 (renvoi). Pour chacune : le contrat qu'elle rouvre et la décision qu'elle exige ; son effet sur l'état stationnaire (g ou le niveau dépendent-ils de la politique suivie, la forme fermée du critère 5 tient-elle) ; son effet sur la stabilité ; l'indépendance envers n_a ; ce que le joueur percevrait, et en combien de tours. (b) **Taux d'utilisation** : la fiche dit si la règle d'investissement lit tu (forme, signe, valeur stationnaire), avec pour niveau normal le t̄u de l'état résolu, sans second ancrage (critère 4 (c)) ; sinon, l'absence est justifiée. Avec la réponse de la fiche 4 (critère 8), la condition 4 de `jeu` est réglée à M28 : tu a une conséquence déclarée, ou il sort de la restitution. (c) **Réponse à #37** : la fiche dit si la décision clôt l'issue (`Closes #37`) ou la laisse ouverte jusqu'au J7. En cas d'absence de levier d'offre, elle donne l'énoncé à porter au catalogue des leviers (J4) et dans l'encadré de portée de `sec:investissement`. Avis de `jeu` (§ 7) | Formes fermées ; tableau des variantes ; avis de `jeu` | `macro` ; `jeu` | fiche ; M28 |
| 11 | Frontière crédit (`docs/blocs/README.md` § 2 ; `macro` ; avis de `monnaie` au § 6) — **exigence** pour (a) à (d) | (a) **Demande de crédit déclarée** : définition (montant demandé dans le pas, en u.m. par pas), phase 3, ce dont elle dépend (besoin de financement, cible de levier, trésorerie), ce que le bloc 7 reçoit et ce que le bloc 6 lit en retour (taux, crédit accordé, conditions publiées), dans la lecture de la phase 3 retenue (critère 3 (b)). (b) **Rationnement** : la règle de caisse dit quelle dépense cède la première (investissement, dividendes ou trésorerie) et par quelle ligne nommée ; la demande non satisfaite est publiée. (c) **Robustesse** : l'état stationnaire et la stabilité du bloc tiennent sous deux hypothèses d'offre, sans présumer le choix de la fiche 7 : (i) offre accommodante au taux i_L ; (ii) rationnement quantitatif partiel. La place de l'accélérateur financier est déclarée : coût du capital du bloc 6 ou offre du bloc 7 (v1.5 : Λ, l. 571 à 584 ; prime de financement externe croissante avec le levier, l. 582). (d) **Variables consommées** : i_L (fiche 7), avec sa date (ouverture ou phase 1, Q8) ; l'anticipation d'inflation (fiche 8), si la règle emploie un taux réel, avec sa définition, son horizon, son unité, sa phase et sa valeur stationnaire requise (π̄). Le taux réel anticipé reçoit un symbole distinct de r = i − π (`tab:symboles`). (e) `monnaie` rend son avis sur (a) à (d) au § 6 ; un désaccord est décrit en deux positions, et le mainteneur tranche | Tableau de l'interface (demande, réponse, phase, ligne) ; cas à la main du critère 1 ; avis de `monnaie` | `macro` ; `monnaie` | fiche ; fiche 7 (offre) |
| 12 | Lisibilité pour le joueur (gabarit 5 ; `macro`, à soumettre à `jeu`) — **exigence** pour (b), **mesure** pour (a), (c) et (d) | (a) **Indicateurs au tour**, chacun avec sa définition, son unité, son dénominateur et sa fenêtre : investissement (glissement sur 12 tours) ; taux d'investissement (12 tours) ; K/Y dans la définition retenue ; taux d'utilisation, s'il est gardé ; levier ; crédit nouveau et demande de crédit non satisfaite ; dividendes et profits non distribués (12 tours) ; taux réel du crédit ou indicateur de rentabilité, si la règle en emploie un. Cet indicateur est rapporté à sa valeur stationnaire, comme le q/q\* de la v1.5 (l. 581), pour ne pas donner de signal permanent. S'y ajoutent les niveaux normaux (K/Y, t̄u, taux d'investissement), publiés par le script d'état stationnaire, comme pour la condition 2 de `jeu` à la fiche 2. (b) **Délais en tours entiers** : taux → investissement visé (0 ou 1 tour selon la date de i_L, Q8) ; investissement → demande (même tour, ligne 3 en phase 5) ; investissement → capacité (K^vol mis à jour en phase 5, y^cap au tour suivant) ; profits → dividendes ; crédit → dépôts (même tour). La contrepartie est visible le même tour (crédit, dépôts, stocks, ventes par acheteur). Aucun effet plus rapide que le tour sans contrepartie. (c) Tableau levier → indicateur → délai → contrepartie pour le taux, la dépense publique et l'impôt sur les entreprises. Aucun levier propre sans décision (Q12) ; aucun drapeau de mode. (d) **Ampleur** : la réponse de l'investissement à une hausse de 1 point du taux du crédit maintenue 12 tours, et à une dépense publique de +1 % et de +5 % pendant 12 tours, est perceptible à l'échelle d'une partie (60 à 120 tours). **Seuil à proposer par `jeu` au mainteneur.** Un signe contre-intuitif, s'il existe, est déclaré | Tableau du § 9, « Interfaces ». Exemple daté à la main, même choc que les fiches 2 à 4 (dépense publique +1 % aux tours 1 à 12, part de G 20 %, hypothèse) : investissement, K/Y, tu, levier, crédit nouveau et dividendes aux tours 1, 2, 3, 4, 9, 13, 14, 18 et 24. Avis de `jeu` (§ 7) ; au J4, scénario apparié (O2) | `jeu` ; `macro` (exemple daté) | fiche ; J4 |
| 13 | Simplicité, empreinte sur l'état, déterminisme (gabarit 6 et rubrique 9 ; principe de simplicité ; `macro`) — **mesure** (décompte) et **exigence** (sans historique ni drapeau) | Décompte par option : paramètres, bornes, variables d'état, registres, lignes et phases touchées ; chaque élément est justifié par une identité vérifiable ou un mécanisme perçu. Chaque variable d'état a son unité et sa valeur stationnaire (critère 5). Une moyenne mobile (rentabilité, profit, croissance des commandes) ou une grandeur du pas précédent (y, tu) est une variable d'état déclarée, jamais un historique. Une seule règle par mécanisme : les modes de la v2.0 (`investment_mode`, `investment_signal`, `payout_mode`, `capital_finance`, `capital_price_forecast` ; l. 116, 172 et 173, validés l. 350) ne sont pas repris comme drapeaux (ADR 0002). Aucun tirage, ou un tirage par la graine du pays, déclaré | Tableau de décompte ; liste des variables d'état | `macro` | fiche ; J2 (reprise exacte) |
| 14 | Coût de calcul (gabarit 4 ; `macro`) — **exigence** (aucune itération) et **mesure** (décompte) | Aucune itération ni optimisation à chaque pas (ADR 0002). Une cible de capital à coût minimal n'est admise qu'en forme fermée (la v2.0 en a une, `closure.py` l. 49 à 58, inactive dans D1). Un point fixe, par exemple une distribution assise sur un résultat qui en dépend, est résolu en forme fermée ou évité par la date de lecture. Décompte des opérations par pas. **Part indicative proposée : 0,48 ms par pays-pas**, celle des blocs 2 à 4 ((52/12 − 0,5)/8) | Décompte dans la fiche ; au J3, `tests/invariants/test_budget.py` | `macro` ; `audit` | fiche ; J3 |
| 15 | Notation (`CONVENTIONS.md` § 5.2 ; décision du 02/10/2026 sur #23 ; `macro`) — **exigence** | Chaque symbole a un seul sens et n'entre en collision ni avec les indices réservés (c, j, k, h, t ; s, ℓ, u du cadre) ni avec `tab:symboles`. En particulier : le levier ne s'écrit pas ℓ (v1.5 l. 571 ; v2.0 `ell`), ni sa cible ℓ\*, ni λ_ℓ. F est une marque de secteur : les profits ne s'écrivent pas F, et le symbole FU de la fiche 2 est confirmé ou remplacé. s_q (v1.5, l. 576) est renommé. κ, δ, tu, t̄u, y^cap, ρ̄_K, ρ̄_IN, I, I^vol, K, K^vol, L et Div_F gardent leur sens. ρ_E (v1.5) se distingue de ρ̄_K et de ρ̄_IN. r désigne le taux réel ex post i − π : un taux réel anticipé reçoit sa propre marque. q et ι sont absents de `tab:symboles`, à confirmer. L'anticipation suit la convention de l'exposant e, son symbole étant fixé avec la fiche 8 | Liste des symboles confrontée à `tab:symboles` (commande `grep` et sortie citées) | `macro` ; `docwriter` (section) | fiche ; section proposée |
| 16 | Calibrabilité et faits établis (`macro`) — **mesure** | Les paramètres se calibrent sur des ordres de grandeur établis, chacun avec sa source retrouvée et sa date : K/Y au coût de remplacement courant, δ, taux d'investissement, taux d'utilisation, levier des entreprises, taux de distribution, réponse de l'investissement au coût du capital et à la demande. Les faits contestés sont séparés. La sensibilité de l'investissement au cash-flow, prise comme mesure de la contrainte de financement, en est un : Fazzari, Hubbard et Petersen (1988), *Brookings Papers on Economic Activity* 1988(1) ; Kaplan et Zingales (1997), *Quarterly Journal of Economics* 112(1), 169-215. La sensibilité de l'investissement au taux d'utilisation à long terme en est un autre (critère 5 (c)). Sources candidates, **non lues à ce jalon**, existence vérifiée : Chirinko (1993), *Journal of Economic Literature* 31(4), 1875-1911 ; OCDE (2009), *Measuring Capital*, 2e éd. ; Federal Reserve, G.17 ; Godley et Lavoie (2007), chap. 11, « A Growth Model Prototype », p. 378-444. Un résultat de la v1.5 ou de la v2.0 n'est pas un fait établi : ainsi des K/Y de 2,3 et 2,9 et des I/Y de 13 % et 18 % du prototype de la v1.5 (l. 575, R). Une source introuvable est déclarée | Sources citées ; « non trouvée » le cas échéant | `macro` | fiche ; J3 (calibration) |
| 17 | Remesure des faits de la première tentative (décision P1 du 03/10/2026 ; `CONTEXT.md` ; `macro`) — **exigence** de procédure | (a) Chaque fait cité porte son statut (S+O, O, R, L, V, V+O). Les faits établis sur D1 (dérive de K/Y, q̄ ; faits § 2) ne sont pas remesurables, D1 n'étant pas versé ; ils sont cités avec leur statut d'origine. (b) Toute remesure (statut V) passe par un script d'`outils/` qui exécute le prototype **dans un processus séparé, jamais par import** (invariant 4), revu par `audit` (circuit 3, `coder` → `audit`). Ses critères sont écrits dans la fiche **avant l'essai**, sur le modèle de la remesure S1 (fiche 2 § 9.7) : grandeur, définition, unité, fenêtre, seuil. Son verdict est publié même défavorable. Le statut V+O n'est donné que si le vérificateur réexécute le script. (c) Un fait V sur le prototype v2.0 reste un fait de la première tentative, jamais un résultat v3. (d) Les lectures de code (L) citent fichier et ligne, vérifiés à la date de la fiche, **avec la branche active et les coefficients effectifs du profil**. Dans D1 : `investment_mode='legacy_q'` et P1 actif (`payout_mode='leverage_target'`, `ell_star` = 0,3, `lam_ell` = 0,1), contre `payout_mode='psi'` par défaut (`model.py` l. 116). Les valeurs dans D1 de `lam_I`, `lam_r`, `acc`, `iota_Pi` et `sat_q` ne sont pas établies par la synthèse | Liste des faits et statuts ; commande, sortie et commit de chaque script | `macro` ; `coder` ; `audit` | fiche (jalon 2) |

### Amendements adoptés

Décisions du mainteneur du 03/10/2026, prises avant l'instruction, sur les questions de `macro` :

- **Critères** : les dix-sept critères sont validés tels quels, avec leur nature (exigence ou mesure).
- **Seuils reconduits des fiches 2 à 4**, adoptés : 1e−10 en relatif (critère 5) ; écart ≤ 1e−6 après 720 pas entre les branches ×0,5 et ×2 (critère 6) ; 0,48 ms par pays-pas (critère 14) ; désactivation d'une borne au plus tard 12 tours après la fin du choc (critère 9 (c)).
- **Bandes du test zéro** (critère 8), adoptées, à confirmer avec O1 avant l'essai (M19) : K/Y ±10 % en relatif ; taux d'utilisation ±0,02, bande commune avec la fiche 2 ; taux d'investissement ±1 point ; levier ±10 % en relatif ; D_F/PIB ±10 % en relatif.
- **Critère 4 (a)** : le critère « capital/PIB à ±10 % » d'O1 se lit sur la définition de K/Y retenue par la fiche 6.
- **Critère 7 (c)** : la stabilité de la boucle investissement – demande est exigée à la calibration ; sa période est publiée, sans bande exigée.
- **Critère 2 (#36)** : les deux voies sont instruites ; si la voie (ii) est recommandée, l'ADR peut appeler une consultation Fable (`docs/agents/routage.md` § 4.1, point 3).
- **Critère 3 (b), Q7 et Q8** : les deux lectures de la phase 3 sont instruites ; tout ordre interne nouveau en phase 3 ou 6, ou l'ajout du bloc banque à la phase 1, est une issue sensible (décision citant M22 et ADR).
- **Critère 10 (#37)** : une variante qui révise M24 (e) ou (f) entre dans le périmètre de l'instruction ; la décision qui la retiendrait citerait M24.
- **Critère 9 (a)** : le classement de I^vol ≥ 0 (contrainte technique si l'irréversibilité est déclarée, ou borne à seuil libre) est proposé par la fiche et tranché par le mainteneur à M28.
- **Q6** : le bloc 6 est instruit comme propriétaire de la ligne 14 (règle de distribution) ; le propriétaire de la ligne 9 est fixé avec la fiche 7.

*Amendement proposé par `macro` le 03/10/2026, **en attente du visa du mainteneur** (ne vaut pas adoption) :*

- **Amendement de notation (03/10/2026, visa du mainteneur à recueillir)**. Sous la lecture (G) de M25 (b) (ADR 0008, partie I) :
  - **Critère 5 (a)** :
    - « volumes en croissance de g/n_a par pas » se lit « volumes en croissance de γ = (1 + g)^{1/n_a} − 1 par pas » ;
    - « I^vol/K^vol = (g + δ)/n_a par pas, soit g + δ = 7 % par an […] quel que soit n_a » se lit « I^vol/K^vol = (n_aγ + δ)/n_a par pas, soit n_aγ + δ = 6,9852 %, 6,9819 % et 6,9806 % par an pour n_a = 4, 12 et 52 (g = 2 %, δ = 5 %) ». Cette dépendance à n_a est déclarée (ADR 0008, I.6).
  - **Critère 5 (b)** : à « Les dépendances par ρ̄_K et ρ̄_IN sont déclarées » s'ajoute « et celles qui passent par n_aγ (ADR 0008, I.6) ».
  - **Critère 6 (a) (i)** : « un capital visé qui croît de g/n_a par pas […] sauf terme de tendance (g + δ) » se lit « qui croît de γ par pas […] sauf terme de tendance (n_aγ + δ) ».
  - **Critère 9 (a)** : la marge « I^vol/K^vol = (g + δ)/n_a > 0 » se lit « (n_aγ + δ)/n_a > 0 ».
  - **Critère 4 (a)**, illustration :
    - K/(n_a p y) vaut **2,3358 ans** à π̄ = 2 % et **1,2643 an** à π̄ = 10 % (g = 2 %, δ = 5 %, n_a = 12) ;
    - la baisse est de 45,9 % ;
    - sous la conversion linéaire de g : 2,3372 et 1,2662, baisse de 45,8 %.
  - **Critère 4 (b)**, ρ̄_K = (n_aγ + δ)/[n_a(((1 + g)(1 + π̄))^{1/n_a} − 1) + δ] :
    - à π̄ = 2 % : **0,7778, 0,7786 et 0,7789** pour n_a = 4, 12 et 52 ;
    - à π̄ = 10 % : **0,4188, 0,4214 et 0,4225** ;
    - sous la conversion linéaire de g : 0,7782, 0,7791 et 0,7794, puis 0,4193, 0,4221 et 0,4231.
  - **Critère 2 (d)** : « 0,33210 % de V_F par pas » se lit « **0,33059 %** (*révisé par M25 (b)*, fiche 2 § 3.N-10, `9b50d58`) ».
  - **§ 1.1, première ligne** : « conversion linéaire unique des taux, flux et vitesses » est annotée « *révisé par M25 (b)* : taux de croissance et d'inflation convertis géométriquement (ADR 0008, I.1) ».
  - Seuils inchangés. Aucun verdict antérieur, puisque l'instruction n'avait pas commencé.
  - Origine : instruction de la fiche 6 par `macro`.

Ces valeurs reproduisent exactement celles mesurées par la session principale (sortie au Retour).

## 3. Options

*Partie 1 sur 2 (options A et B), instruite par `macro` le 03/10/2026 sur la fiche à l'état `cb8e5d9`. La partie 2 (options nouvelles, variante sans retard, voies (i) et (ii) de #36, état conjoint avec la fiche 5, cas à la main du critère 1, boucle investissement – demande avec N1 à N7) reste à instruire.*

### 3.0 Conventions de l'instruction

**Découpage.** A et B sont instruites en entier. Les options nouvelles, la variante sans retard, les voies (i) et (ii) de #36 et l'état conjoint avec la fiche 5 relèvent de la partie 2.

**Transposition commune de A et B dans le cadre v3** (hypothèses déclarées) :
- J = 1, donc p_K = p. La technique de Leontief en travail (M24 (e), (f)) fait que le profit ne dépend pas de K ;
- conversion selon ADR 0008, I.1 :
  - taux de flux, vitesses et δ : x/n_a ;
  - croissance et inflation : (1 + x)^{1/n_a} ;
- lectures conformes aux phases (critère 3) : y, tu et profit du pas précédent ;
- trajectoire de référence (G) : g = 2 %, δ = 5 %, n_a = 12, π̄ = 2 % (10 % en variante).

**Calibration indicative**, qui est une **hypothèse** et non un fait :

| Paramètre | Valeur | Source |
|---|---|---|
| s_Π, profit brut / valeur de la production (J = 1, sans intrants) | 0,30 | hypothèse |
| c = r_L + ρ_E + δ | 0,09, avec r_L = 2 % (hypothèse) et ρ_E = 2 % | v1.5 l. 575 ; v2.0 l. 288 |
| ι | 0,20 | v1.5 l. 581 et 2376 ; v2.0 l. 120 |
| Bande de Γ | [0,80 ; 0,95] | v1.5 l. 575 ; v2.0 l. 242 |
| s_q | 0,03 | — |
| λ_q | 1 par an | — |
| κ | calé sur t̄u = 0,93 à la calibration de base | v1.5 l. 581 |
| Maquette de financement : K^vol/(n_a y) | 3 | hypothèse |
| ℓ\* ; λ_ℓ | 0,3 ; 0,1 par an | — |
| ψ | 0,9 | — |
| m̄ | 8 semaines de chiffre d'affaires | — |
| i_L | (1 + r_L)(1 + π̄) − 1 | — |

**Maquettes réduites** (résultats du modèle, sans statut de fait) :
- `f6_boucle.py` : boucle propre du capital, à demande exogène ;
- `f6_demande.py` : boucle investissement – demande. y = a + m·y_{t−1} + I^vol, **sans les stocks N1 à N7** de la fiche 2. Valeurs propres prises au point fixe, tanh linéarisé ;
- `f6_finance.py` : financement, investissement et ventes exogènes sur la trajectoire de référence.

**Statut des faits** : S+O, O, R, L, V, V+O (`CONTEXT.md`). Une sortie de maquette est un résultat v3 de maquette, jamais un fait de la première tentative.

**Notation provisoire** (critère 15) : x = K^vol/(n_a y) ; q\*, q̄ ; Γ_u pour le filtre d'utilisation de la v1.5, renommé à cause de la collision avec Γ, facteur de croissance nominale de la fiche 5 ; φ = 1/[(1 + γ)(1 + π̄)^{1/n_a}], facteur de retard d'un pas sur un profit nominal.

### 3.A Option A — v1.5

1. **Source.** `archive/v1.5/Nations_et_Marches_v1_5.tex` :
   - `eq:profit`, `eq:cash` et `eq:div` (l. 545 à 547), avec leur lecture (l. 551 à 554) ;
   - l. 555 : ordre « dividendes, puis investissement » et remboursement R_j d'un quart de l'excédent ;
   - l. 557 : faillite ;
   - `eq:invest` (l. 562 à 568), avec q (l. 564), I (l. 565) et Γ (l. 566) ;
   - l. 575 : ρ_E, bande de Γ, plafond 2δ ; l. 576 : q̄, s_q, λ_q, rejets ; l. 577 à 581 : q\* ; l. 582 : accélérateur financier inactif ; l. 584 : Λ, accumulation et délai T_K ;
   - table : l. 2309 (δ_j = 0,035 ; 0,045 ; 0,04 ; 0,05), l. 2310 (ψ = 0,9 ; m̄ = 8 semaines), l. 2326 (s_q, λ_q), l. 2376 (ι = 0,20 ; **T_K fixé en dur, sans valeur**).

   **Équations jamais garanties exécutées.**

2. **Équations.**
   - q = (E[Π^brut]/(p_K K))/(r^L + ρ_E + δ), avec r^L = i^L − π^e et q̄_{t+1} = q̄_t + λ_q(q_t − q̄_t).
   - I = K(δ + min(ι(q̄ − 1) + ι s_q tanh((q − q̄)/s_q), 2δ)^+ · Λ Λ^Bk Γ), avec Γ = clip((Ŷ/Y^cap − u̲)/(ū − u̲), 0, 1).
   - Λ = clip(1 − η_ℓ(ℓ − ℓ̄), 0, 1).
   - K_{t+1} = (1 − δ)K_t + I_t, livré après T_K mois.
   - Div = min(ψΠ⁺, (M − R)⁺) + ¼(M − R − m̄ pQ)⁺.
   - **Interprétation** : les taux de `eq:invest` et de l'accumulation sont annuels, alors que la v1.5 travaille « par tick » (semaine). La transposition les lit comme annuels, convertis en x/n_a. Écrite par tick, avec δ annuel, l'accumulation serait absurde. Deux lectures sont donc possibles ; je retiens la seconde.
   - La moyenne mobile E[Π^brut] n'a **pas de vitesse** (l. 571 : « moyenne mobile »).

3. **Verdicts par critère.**

| Critère | Verdict | Mesure ou motif |
|---|---|---|
| 1 Cohérence stock-flux | **Écart** | (c) `eq:cash` (l. 546) écrit ΔM = Π − Div − p_K I + ΔL. Or Π est net de δ p_K K (l. 545) et I est brut (l. 565) : l'amortissement est déduit deux fois de la trésorerie. Pour K/Y = 3 et δ = 5 %, cela fait **0,15 PIB par an** de trésorerie détruite sans contrepartie, puisque la forme cohérente est ΔM = Π + δ p_K K − Div − p_K I + ΔL. (a) Ligne 8 au prix courant δ p_K K (l. 545) : contraire au contrat de la valeur comptable (l. 521) ; à transposer en δK/n_a. Lignes 3, 14 et 18 transposables. Cas à la main du crédit refusé de moitié **non fait**. Avec refus, la v1.5 conclut à la faillite (l. 557), hors du socle |
| 2 #36 | Compatible avec la voie (i) (FU = résultat non distribué, aucune ligne) | Taux de distribution stationnaire : ψ = 0,9 en régime β, mesuré 0,9000 ; 0,5693 en régime α (ψ = 0,5, π̄ = 2 %), excédent compris (`f6_finance.py`). La voie (ii) relève de la partie 2 |
| 3 Phases | **Écart transposable** | (a) et (f) : Γ lit Ŷ, la production visée du pas, donc y\* de la phase 2. À remplacer par tu_{t−1}, variable d'état. (d) Div lit Π du pas, qui contient T_F et les intérêts de la phase 6 : lire Π_{t−1}. L'ordre « dividendes, puis investissement » (l. 555) est inverse de l'ordre des phases v3 (ligne 3 en phase 5, ligne 14 en phase 6) : la priorité de caisse de la v1.5 n'est pas transposable telle quelle. (b) Crédit : le bloc demande lorsque la trésorerie devient négative ; lecture (a) possible |
| 4 K/Y, ρ̄_K, κ, t̄u, δ | **Écart** | (a) q se rapporte à p_K K, c'est-à-dire la définition (ii), volume valorisé. Le transposer sur K comptable (définition (i)) donnerait x = s_Π φ/(q\* ρ̄_K c) : à q\* donné, **K^vol/(n_a y) augmenterait de 85 %** de π̄ = 2 % à 10 % (0,7786/0,4214 = 1,848). Le dénominateur de q doit donc rester p K^vol. (c) t̄u est un **résultat**, et il dépend de ι : 0,93, puis 1,00 à ι × 0,5, puis 0,898 à ι × 2 (`f6_boucle.py`). La bande [0,80 ; 0,95] est un second ancrage, contraire au critère 4 (c). (d) δ_j sectoriels (l. 2309) : un seul δ à fixer sous J = 1 |
| 5 État stationnaire | Forme fermée **existante**, **dépendances non admises** | Sur la trajectoire (G) : q\* = 1 + n_aγχ/(ιΓ_u), avec χ = (1 + γ)^{T_K} (correction de livraison, cf. acquis R « corrigée du taux de livraison »). Si Γ_u est intérieur, x résout l'équation du second degré s_Π φ/(x c) = 1 + n_aγχ(ū − u̲)x/(ι(κ − u̲x)). Mesuré : x = 2,9815 (base), 2,9697 (n_a = 4), 2,9859 (n_a = 52), 2,9705 (π̄ = 10 %), 2,9804, 2,9784 et 2,9753 (T_K = 1, 3 et 6 pas). La dépendance à n_a et à π̄ vient du retard d'un pas sur un profit **nominal** (φ). Elle disparaît si la règle lit le taux de profit Π_{t−1}/(p_{t−1}K^vol_{t−1}) |
| 6 Vitesses | **Échec** (exigence) | (ii) ι **est une vitesse au sens du § 2.7**. ι(q − 1) est un « gain × écart » : à g = 0, q\* = 1 quel que soit ι ; à g > 0, l'écart stationnaire n_aγ/(ιΓ_u) dépend de ι. C'est exactement le cas (i). Mesuré : x = 2,7728, 2,9815 et 3,0880 pour ι × 0,5, × 1 et × 2, soit −7,0 % et +3,6 %. Condition qui la supprime : sortir un terme de tendance, I/K = (n_aγ + δ)/n_a + ι(q − 1)Γ_u/n_a, d'où q\* = 1. λ_q n'a aucun effet stationnaire (q̄ est la moyenne d'un ratio stationnaire ; x identique à × 0,5 et × 2). Le quart d'excédent (¼ par semaine, soit 13 par an, **supérieur à n_a = 12**, donc inadmissible tel quel) est inactif en régime β. (b) Deux régimes selon ψ (`f6_finance.py`) : **β** (ψ = 0,9) : D_F = 0 ; **α** (ψ = 0,5) : L = 0. Pas de continuum : ℓ converge vers la même valeur depuis ℓ = 0,3 et depuis ℓ = 0,6. Mais son ancre est la **seule croissance nominale**, ℓ = [n_aγ − (1 − ψ)(s_Π/x − δ)]/[n_a(Γ − 1) − (1 − ψ)i_L] : 0,4159 (π̄ = 2 %), **0,1432** (π̄ = 10 %), 0,4406 (i_L + 2 points). Demi-vie de **233 pas**. Cette ancre n'existe que si n_a(Γ − 1) > (1 − ψ)i_L. C'est cohérent avec P1 (R) : « sans les deux derniers termes, le levier tend vers zéro » (régime α) |
| 9 Bornes | **Échec** | Seuil libre : min(·, 2δ), inactif (marge de 0,077 par an sur le taux net). ^+ sur l'investissement net, plus restrictif que I^vol ≥ 0 car il interdit le désinvestissement net : inactif à l'état stationnaire (taux net 0,0229 par an). Γ_u écrêté à [0, 1] sur [0,80 ; 0,95] : inactif à la base, mais avec une marge de 0,02 seulement, et **saturé à l'état stationnaire pour ι × 0,5** (tu = 1,00). Λ : inactif (ℓ < 0,6). Conservation : D_F ≥ 0, **active à l'état stationnaire en régime β** ; L ≥ 0, active en régime α. (c) n'est donc pas satisfait. Faillite hors du socle |
| 13 Empreinte | Mesure | Paramètres : ι, λ_q, s_q, ρ_E, δ, u̲, ū, η_ℓ, ℓ̄, T_K (sans valeur), ψ, m̄, ¼ (en dur), la vitesse de E[Π] (sans valeur) et Λ^Bk (fiche 7) : 15, dont 2 sans valeur. Bornes : 7. Variables d'état : q̄, E[Π^brut], tu_{t−1}, et le registre des T_K commandes en cours. Aucun drapeau |
| 14 Coût | Conforme (aucune itération) | Une tangente hyperbolique et une vingtaine d'opérations par pas. Coût non mesuré |
| 15 Notation | **Collisions** | ℓ (levier) contre l'indice de ligne ; Γ (filtre) contre Γ de la fiche 5 ; M_j (trésorerie) contre M ; Π contre Π^CB ; s_q, ρ_E (contre ρ̄_K et ρ̄_IN) ; q et ι absents de `tab:symboles`. Décomptes par `grep -c -F` au Retour |
| 17 Faits | Voir le tableau des statuts | — |

4. **Critère 7.**
   - **(a) Instabilités.**
     - N° 10 et 11 : la ligne 8 au prix courant (l. 545) est une réévaluation hors ligne déclarée, ce qui en relève. À transposer en δK/n_a sur la valeur comptable.
     - N° 1 : sans objet sous J = 1.
     - N° 4 : sans objet, la règle ne lit pas r\*.
     - N° 15 : voir le critère 9 et (c) ci-dessous.
     - N° 16 : sans objet.
     - Accélérateur explicite : absent, rejeté par la v1.5 (l. 576 (iii), R).
   - **(b) Boucle propre du capital**, à demande, prix et taux exogènes, pas mensuel :

     | Variante | ρ | Demi-vie | Racine |
     |---|---|---|---|
     | Base | 0,97179 | 24,2 tours | réelle |
     | ι × 0,5 | 0,99003 | 69,2 tours | réelle |
     | ι × 2 | 0,96089 | 17,4 tours | réelle |
     | λ_q × 0,5 ou × 2 | inchangé | — | — |
     | T_K = 1, 3, 6 pas | 0,97107 ; 0,96943 ; 0,96627 | — | réelle |
     | n_a = 4 ; n_a = 52 | 0,91294 ; 0,99356 | 7,6 ; 107,2 pas | — |

     La demi-vie est la même en années pour n_a = 4, 12 et 52 (environ 2 ans). **Conforme.**
   - **(c) Boucle investissement – demande** (maquette sans stocks) : **instable** (racine réelle, de type harrodien) :

     | | m = 0,5 | m = 0,6 | m = 0,7 | m = 0,8 |
     |---|---|---|---|---|
     | ι × 1 | 1,460 | 1,568 | 1,673 | 1,776 |
     | ι × 2 | 1,888 | 1,993 | 2,096 | 2,199 |
     | ι × 0,5 | 0,981 | 0,961 (période 265 tours) | 1,011 | 1,120 |

     Stable seulement à ι × 0,5 avec m ≤ 0,6, parce que Γ_u y est saturé.

     Dérivation à la main, cohérente avec la mesure : le gain de basse fréquence ∂I/∂y, rapporté à y, vaut x[ιΓ_u q\* + ι(q\* − 1)·tu/(ū − u̲)] = 2,98 × (0,193 + 0,142) ≈ **0,99**. Le canal de q donne 0,58 et celui du filtre 0,42. Avec m, on obtient m + 0,99 > 1 pour tout m > 0.

     **Échec probable de l'exigence à la calibration**, à confirmer avec N1 à N7 en partie 2. Dans la v1.5, seules les saturations (tanh, écrêtage de Γ_u, ^+, 2δ) contiennent cette instabilité linéaire : c'est le terrain de l'instabilité 15.
   - **(d) Endettement** : ℓ est stable à i_L et à i_L + 2 points (valeur propre 0,99703, puis 0,99720), mais très lent et dépendant de π̄ (voir le critère 6 (b)).
   - **(e) Interface** : une hausse de 1 point de r^L baisse q d'environ 1/c, soit 11 % ici (« environ 12 % par point », l. 576, R). Délai : 1 tour si i_L est lu à l'ouverture.

5. **Joueur.** L'indicateur q/q\* (l. 581) est lisible. Le filtre d'utilisation et la saturation tanh sont invisibles. La faillite sort du socle.

### 3.B Option B — v2.0 (`investment_mode='legacy_q'`)

1. **Source** (statut L, lignes vérifiées le 03/10/2026). `archive/v2.0/prototype/model.py` :
   - **Calendrier** : `WEEKS = 52` (l. 36). Le bloc s'exécute **chaque semaine** : la section 4 (l. 853 à 905) est au niveau du corps de `_step_normal`, hors du test `month` (l. 607).
   - **Taux réel** : r_now = (1 + i_L)/(1 + π^e) − 1 (l. 854) ; `r_long` lissé par `lam_r` (l. 857) ; i_L = i_CB + mL + ρ1 max(ℓ − ℓ̄, 0) (l. 1972 à 1974).
   - **Signal et q** :
     - signal = `Pi_brut_bar` (l. 859, `price_basis='average'`) ;
     - `Pi_brut_bar`, moyenne mobile à **0,05 par semaine codée en dur** (l. 1025) ;
     - q (l. 862), ℓ (l. 863), Λ (l. 864), Λ^Bk (l. 865 ; l. 1976).
   - **Utilisation et filtre** :
     - utilisation = Yhat/Ycap_full, écrêtée à [0 ; 1,5] (l. 866) ;
     - Yhat est la production planifiée de la semaine (l. 644, avec g0/52 linéaire) ;
     - Ycap_full est une capacité Cobb-Douglas (l. 675) ;
     - filtre (l. 867).
   - **Accélérateur** : g_e écrêté à [−0,05 ; 0,10] (l. 870).
   - **Réponse en q** : q̄ (l. 872) ; réponse saturée (l. 873) ; cash-flow (l. 874 à 877) ; q − 1 (l. 879).
   - **Investissement** : plafond (l. 880) ; Iw avec plancher −0,5δ (l. 881) ; ajustement partiel (l. 890).
   - **Financement** : l. 893 à 905, P1 aux l. 896 et 897, accès au crédit si ℓ < ℓ̄ + 0,4 (l. 901).
   - **Livraison et capital** : livraison rationnée sans délai (l. 964) ; K = (1 − δ/52)K + Igot (l. 1002).
   - **Profits et dividendes** :
     - Π net de **δ/52 · p_K · K_d'ouverture, au prix courant** (l. 1021) ;
     - impôt (l. 1022 à 1024) ;
     - remboursement de l'excès de levier (l. 1032 et 1033) ;
     - `Pi_net_bar` (l. 1037) ;
     - P1 (l. 1038 à 1040) ; ψ (l. 1042) ; dividende (l. 1043).
   - **Paramètres par défaut** :

     | Paramètre | Valeur | Ligne |
     |---|---|---|
     | δ | 0,035 ; 0,045 ; 0,04 ; 0,05 par an | 101 |
     | ℓ\*, `lam_ell` | 0,3 ; 0,1 | 117 et 118 |
     | m̄ | 8 | 119 |
     | ι | 0,2 | 120 |
     | ℓ̄, η_ℓ | 0,6 ; 2 | 121 |
     | `iota_Pi` | 0 | 150 |
     | `lam_I` | 1,0 | 267 |
     | `sat_q`, `lam_qbar`, `lam_div` | 0,03 ; 1/52 ; 0,1 | 268 |
     | ρ_E | 0,02 | 288 |
     | `lam_r` | 1,0 | 299 |
     | `acc` | 0 | 301 |
     | `inv_cap` | 2,0 | 302 |

   - `closure.py` : `capital_target` (l. 49 à 58) est un coût minimal Cobb-Douglas en forme fermée ; `investment_plan` (l. 73 à 115) lui ajoute un terme de tendance. Branche `sales_cost`, **inactive dans D1**.

   **Branche active dans D1** (faits § 1.1, S+O) : `investment_mode='legacy_q'` et P1 (`payout_mode='leverage_target'`, ℓ\* = 0,3, `lam_ell` = 0,1).
   - Sous les valeurs par défaut, `sat_q` = 0,03 > 0 : la branche q̄ saturée (l. 871 à 873) est active.
   - `iota_Pi` = 0 : le cash-flow est inactif.
   - `acc` = 0 : l'accélérateur est nul.
   - `lam_I` = 1 et `lam_r` = 1 : pas de lissage.
   - **Les valeurs de ces paramètres dans D1 ne sont pas établies** (critère 17 (d)) : seules les valeurs par défaut sont citées.

2. **Verdicts par critère.**

| Critère | Verdict | Mesure ou motif |
|---|---|---|
| 1 | **Écart** (évaluation du capital) | Les flux passent par le grand livre (`led.transfer` ; « crédit crée le dépôt », l. 905 : lignes 18 et 17). Mais K est un volume valorisé à p_K courant, sans poste en valeur comptable, et la ligne 8 est au prix courant (l. 1021) : contraire à l. 521 ; à transposer. La v2.0 lit Ycap Cobb-Douglas, contraire à M24 (e) et (f) ; transposé sur une technique de Leontief |
| 2 | Compatible avec la voie (i) | Distribution P1 endogène = 1 − [(1 − ℓ\*)p I + (λ_ℓ/n_a)(L − ℓ\* p K^vol)]/Π̄ + part de l'excédent. Maquette : **0,7362** (π̄ = 2 %) ; **1,0779** (π̄ = 10 %) : à 10 %, FU < 0, les dividendes dépassent le profit |
| 3 | **Écart transposable** | Le filtre lit Yhat de la semaine (y\* de la phase 2) : lire tu_{t−1}. `Pi_net_bar` intègre Π_net de la semaine, après impôt et intérêts (phase 6) : lire le pas précédent. Crédit : `short` est calculé sur le plan et sur `credit_room` connu ; le refus retombe sur D_F, le plan n'est pas révisé. C'est la lecture (a) |
| 4 | **Écart** | Définition (ii) comme A. t̄u est un résultat, dépendant de ι (identique à A). δ sectoriels |
| 5 | Forme fermée **existante**, dépendances | Même équation du second degré que A, avec χ = 1 (pas de délai). Le biais de la moyenne mobile d'un profit nominal croissant remplace φ. Mesuré : x = 2,9464 (base) ; 2,9460 et 2,9465 (n_a = 4 et 52 : quasi indépendant) ; **2,8965 à π̄ = 10 %** (−1,7 %) |
| 6 | **Échec** (exigence) | Voir le tableau des vitesses ci-dessous |
| 9 | **Écart** | Seuil libre : plancher −0,5δ et plafond `inv_cap`·δ (l. 880 et 881 ; inactifs à l'état stationnaire, marge de 0,077 par an) ; utilisation [0 ; 1,5] (inactive) ; filtre (comme A, saturé à ι × 0,5) ; g_e (sans effet, `acc` = 0) ; `cf_rate` (inactif) ; ℓ < ℓ̄ + 0,4 (l. 901, inactif) ; planchers absolus 1e−9 (l. 862 et 863). Conservation : base_div ∈ [0, D_F − remboursement] (l. 1040). **Coudes actifs à l'état stationnaire** : remboursement min(·, L − ℓ\*pK) à π̄ = 2 % (ℓ = 0,2990), et seuil d'excédent m̄ (D_F au seuil). Exposition à l'instabilité 15 |
| 13 | **Échec** (état caché, drapeaux) | `getattr` avec défaut aux l. 857, 870, 872, 875, 890, 1037 et 1039. Drapeaux : `investment_mode`, `investment_signal`, `price_basis`, `payout_mode`, `capital_finance`, et les branches `sat_q > 0` et `iota_Pi > 0`. Moyennes calculées même inactives (l. 1026 à 1029). Environ 19 paramètres et 6 constantes en dur (0,05 ; 0,25 ; 0,5 m̄ ; +0,4 ; −0,5δ ; 1,5). État : `r_long`, `q_bar`, `g_orders`, `Pi_brut_bar`, `Pi_net_bar`, `Iw_prev`, `Qbar` |
| 14 | Conforme | `legacy_q` sans itération (boucle sur les secteurs) ; `sales_cost` en forme fermée. Coût non mesuré |
| 15 | **Collisions** | `ell`, ℓ\*, λ_ℓ (critère 15 explicite) ; q, ι, Λ ; ρ_E |
| 17 | Voir le tableau des statuts | — |

   **Vitesses du critère 6**, base lue dans le code, convertie en base annuelle et confrontée à λ ≤ n_a :

| Vitesse | Base dans le code | Par an | Par pas (n_a = 12) | Effet stationnaire mesuré |
|---|---|---|---|---|
| `lam_I` (l. 267, 890) | 1,0 par semaine (inactif) | — | ≤ 1 | Si actif, x = 2,9453 (0,5) et 2,9433 (0,25) contre 2,9464 : **dépend** (cas (i), plan croissant lissé) |
| `lam_qbar` (l. 268) | 1/52 par semaine | 1 | 1/12 | Aucun : x identique à × 0,5 et × 2 |
| `lam_r` (l. 299) | 1,0 par semaine (inactif) | — | ≤ 1 | Aucun : moyenne d'un ratio stationnaire, en forme fermée |
| `Pi_brut_bar` (l. 1025, **en dur**) | 0,05 par semaine | 2,6 | 0,217 | **x = 2,9205, 2,9464 et 2,9590** à × 0,5, × 1 et × 2 (±0,9 %) |
| `lam_ell` (l. 118 ; /52 aux l. 897 et 1039) | 0,1 par an | 0,1 | 0,1/12 | π̄ = 2 % : masqué (ℓ ramené à ℓ\* par le remboursement). π̄ = 10 % : **ℓ = 0,2170, 0,2362 et 0,2564**, soit ℓ = ℓ\*(n_aγ + δ + λ_ℓ)/(n_a(Γ − 1) + λ_ℓ), forme fermée exacte. Elle n'égale ℓ\* que si n_a(Γ − 1) = n_aγ + δ |
| `lam_div` (l. 268) | 0,1 par semaine | 5,2 | 0,433 | Masqué : D_F est fixé par le seuil m̄ |
| ¼ de l'excédent (l. 1033, 1043) | 0,25 par semaine | **13 > n_a** | inadmissible ; ramené à ≤ 1 | **D_F/(12 PIB) = 0,1538, 0,1608 et 0,1745** pour 1, 0,5 et 0,25 par pas |

   Condition qui supprime la dépendance de `lam_ell` : un terme de tendance nominale dans P1, c'est-à-dire emprunter ℓ\* × (variation de p K^vol), et non ℓ\* × p I. Pour `Pi_brut_bar` : lisser un taux, non un niveau nominal.

3. **Critère 7.**
   - **(a) Instabilités.**
     - N° 10 et 11 : ligne 8 au prix courant (l. 1021), même constat que A.
     - N° 1 : sans objet sous J = 1. La v2.0 (J = 4) a p_K = p_[3], donc un canal de prix relatif.
     - N° 4 : sans objet.
     - Taux long lissé : inactif (`lam_r` = 1), conforme au rejet (ii) de la v1.5.
     - Accélérateur : `acc` = 0 (l. 301, L), mais un accélérateur **implicite** passe par q et par le filtre ; voir (c).
   - **(b) Boucle propre** : ρ = 0,97179 (24,2 tours) ; 0,99003 (ι × 0,5) ; 0,96089 (ι × 2) ; 0,97150 et 0,97191 (moyenne du profit × 0,5 et × 2) ; 0,97105 et 0,96928 (`lam_I` = 0,5 et 0,25). **Conforme.**
   - **(c) Boucle investissement – demande** (sans stocks) : **instable**.

     | | m = 0,5 | m = 0,6 | m = 0,7 | m = 0,8 |
     |---|---|---|---|---|
     | ι × 1 | 1,204 | 1,288 | 1,372 | 1,459 |
     | ι × 2 | 1,412 | 1,497 | 1,584 | 1,672 |
     | ι × 0,5 | 0,978 | 0,980 (période 281 tours) | 1,002 | 1,057 |

     La moyenne mobile du profit amortit sans supprimer : le gain de basse fréquence est le même que dans A. Même verdict que A.
   - **(d)** : ℓ et D_F stables dans la maquette à i_L et à i_L + 2 points (ℓ inchangé, distribution de 0,7362 à 0,6863) ; D_F fixé au seuil m̄.
   - **(e) Interface** : identique à A, avec un délai d'une semaine dans la v2.0.

4. **Joueur.** Des dividendes résiduels de P1 qui peuvent dépasser le profit à inflation élevée (distribution 1,08 à π̄ = 10 %) seraient un signal contre-intuitif à soumettre à `jeu`. Le levier visé ℓ\* est lisible.


### Statut des faits de la première tentative (critère 17)

| Fait | Statut |
|---|---|
| Profil D1 : `legacy_q`, P1, ℓ\* = 0,3, `lam_ell` = 0,1 | S+O (faits § 1.1) |
| Valeurs dans D1 de `lam_I`, `lam_r`, `acc`, `iota_Pi`, `sat_q`, `lam_qbar`, `lam_div`, ι, `inv_cap` | non établies (valeurs par défaut citées, L) |
| Lignes de `model.py` et de `closure.py` citées | L, vérifiées le 03/10/2026 |
| D1 : dérive de K/Y de 3,41 % (11,2 % avant préparation) ; q̄ = 1,111 | R (faits § 2), non remesurables |
| Instabilités 1, 4, 10, 11 et 15 | R (faits § 6) |
| Instabilité 16 | S+O (G2, J2, K2c) |
| Hypothèse réfutée n° 4 (blocage de l'investissement en v1.7) | R, non reprise |
| Acquis P1, formule de K/Y, « l'épargne n'y entre pas » | R (faits § 8) |
| v1.5 : accélérateur de Samuelson-Hicks (3 à 7 points), taux long lissé (cycle de 8 à 12 ans), −5,9 / −2,9 % de PIB (l. 576) ; q\* = 1,11 (l. 581) ; accélérateur financier inactif, ℓ = 0,32 ou 0,08 (l. 582) ; ℓ = 0,34, dividendes 9 % du PIB, crédits 1,0 PIB (l. 555) ; K/Y de 2,3 et 2,9 et I/Y de 13 et 18 % (l. 575) | R, rapportés par la v1.5, invérifiables |
| Sorties des maquettes `f6_*.py` | résultats v3 de maquette, sans statut de fait |

Aucune remesure V n'est proposée. Les échecs au critère 6 sont établis par forme fermée et par maquette, et ils ne dépendent pas de D1.


### 3.X Acquis de A et B pour la suite de l'instruction

1. **Conventions** :
   - I^vol/K^vol = (n_aγ + δ)/n_a ;
   - ρ̄_K et l'illustration du critère 4 (a) recalculés sous (G) (amendement ci-dessus).
2. **Le dénominateur de toute rentabilité doit être p K^vol (définition (ii))**, et non K comptable. Sinon K^vol/(n_a y) augmente de 85 % entre π̄ = 2 % et 10 %.
3. **Une réponse en « gain × écart » sans terme de tendance fait dépendre l'état d'arrivée de la vitesse** :
   - ι(q − 1) : x de −7,0 % à +3,6 % ;
   - P1 avec ℓ\*·p I : ℓ de 0,2170 à 0,2564 à π̄ = 10 %.

   Toute option nouvelle porte un terme de tendance explicite : n_aγ + δ pour le capital, croissance nominale pour la dette.
4. **Lisser un niveau nominal crée un biais qui dépend de la vitesse, de π̄ et de n_a** (x ±0,9 %). On lisse des taux.
5. **Le filtre [0,80 ; 0,95] est un second ancrage de tu, qui sature à l'état stationnaire pour ι × 0,5.** Il est à écarter au profit d'un t̄u unique (critère 4 (c)).
6. **Instabilité harrodienne de la boucle investissement – demande** : ∂I/∂y ≈ 0,99 à la calibration de A et B, d'où ρ > 1 pour tout m ≥ 0,5. Une option nouvelle doit garder un gain de basse fréquence inférieur à 1 − m, ou reposer sur un mécanisme stabilisant déclaré. À remesurer avec N1 à N7 (stocks) en partie 2.
7. **Financement** :
   - sans cible de levier (A), D_F = 0 ou L = 0 au coin, contrainte active à l'état stationnaire ;
   - ℓ est ancré par la seule croissance nominale (demi-vie de 233 pas ; 0,4159 → 0,1432 de π̄ = 2 % à 10 %) ;
   - avec P1 (B), le seuil m̄ ancre D_F, mais des coudes restent actifs à l'état stationnaire, et la vitesse du quart d'excédent (13 par an) est supérieure à n_a.
8. **Voie (i) de #36** : compatible avec A et B ; référence pour la comparaison avec la voie (ii).
9. **État conjoint** : dans A et B, x est fixé par le coût du capital et ι, donc t̄u = κ/x n'est pas libre. La fermeture kaleckienne par tu est exclue, et l'égalité de l'épargne et de l'investissement doit se fermer ailleurs (taux réel, propension ou niveau d'activité), avec la fiche 5. Point **contesté**.
10. **Lecture (a) de la phase 3** : réalisée dans la v2.0 (conditions connues, refus porté par D_F).

## 4. Tableau comparatif

Non instruit.

## 5. Avis de l'expert pilote

Non instruit.

## 6. Avis de l'expert consulté

Non instruit (`monnaie`, frontière crédit, au jalon 2).

## 7. Avis de `jeu`

Non instruit.

## 8. Décision du mainteneur

Non instruit (M28, décidée avec la fiche 5).

## 9. Conséquences de la décision

Non instruit.

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 03/10/2026 | Ouverture (issue #42) ; § 1 et § 2 proposés | `macro` ; session principale |
| 03/10/2026 | Critères validés avec amendements (seuils et bandes, lecture d'O1, période publiée, deux voies de #36, contrats sensibles des phases 3 et 6, variantes révisant M24, I^vol ≥ 0 tranché à M28, ligne 14 ; issue #42) | mainteneur |
| 03/10/2026 | Jalon 2, partie 1 : § 3.0, options A (v1.5) et B (v2.0), statut des faits, acquis pour la suite ; A et B échouent au critère 6 (exigence) et, sur maquette sans stocks, au critère 7 (c) ; amendement de notation sous (G) proposé, en attente du visa | `macro` ; session principale |
