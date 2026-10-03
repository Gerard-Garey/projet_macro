---
bloc: Investissement et financement des entreprises
module: src/nations/blocs/investissement.py
expert pilote: macro
experts consultés: monnaie (demande de crédit face à l'offre bancaire : frontière crédit) ; jeu
statut: avis rendus (03/10/2026)
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

Décisions du mainteneur du 03/10/2026, prises **après** le dépôt de l'instruction (§ 3 à 5) :

- **Amendement prospectif du critère 6, essai du J3** (proposé par `macro`, § 5, lecture (f)) : l'écart entre les branches ×0,5 et ×2 se mesure **après 2 160 pas** au lieu de 720, seuil de 1e−6 inchangé. Motif : le seuil de 720 pas est inatteignable par la lenteur de la valeur comptable du capital (racine d'au moins 0,9926), non par une dépendance à la vitesse (S : 3,9e−6 à 720 pas, 3,0e−6 à 1 440, 1,6e−7 à 2 160 ; C : 3,2e−6 à 720). Correction prospective : aucun essai n'avait été fait ; le critère d'origine reste publié ci-dessus.
- **Lecture de la v1.5 (option A)** : les taux d'`eq:invest` et de l'accumulation se lisent **annuels**, convertis en x/n_a ; la dépendance de l'état d'arrivée au délai de livraison T_K (x de 2,9804 à 2,9753 pour T_K = 1 à 6 pas) est une **dépendance déclarée**, comme celle à n_a, et non une vitesse au sens du § 2.7. Aucun verdict ne change (A échoue au critère 6 par ι).

- **Amendement de notation (03/10/2026, proposé par `macro`, visa du mainteneur le 03/10/2026)**. Sous la lecture (G) de M25 (b) (ADR 0008, partie I) :
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

*Partie 1 sur 2 (options A et B), instruite par `macro` le 03/10/2026 sur la fiche à l'état `cb8e5d9`. Partie 2 (options nouvelles S et C, variante sans retard R, variante PI écartée, socle de financement F, voies (i) et (ii), état conjoint, cas à la main, boucles avec N1 à N7), instruite par `macro` le 03/10/2026 sur la fiche à l'état `d80bfe7`. Chiffres de la partie 2 non encore contre-éprouvés de façon indépendante.*

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
   - **Interprétation** : les taux de `eq:invest` et de l'accumulation sont annuels, alors que la v1.5 travaille « par tick » (semaine). La transposition les lit comme annuels, convertis en x/n_a. Écrite par tick, avec δ annuel, l'accumulation serait absurde. Deux lectures sont donc possibles ; je retiens la seconde. *Lecture retenue par le mainteneur le 03/10/2026 (§ 2, amendements).*
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

### 3.N Socle commun des options nouvelles (S, C, R) et règle de financement F

**Conventions.** Ce sont celles du § 3.0, lecture (G).
- Statut : les sorties des maquettes sont des résultats v3 de maquette, sans statut de fait.
- **Hypothèses de calcul** (ce ne sont pas des calibrations) :
  - x = K^vol/(n_a y) = 2 ans en base, 3 ans en variante ;
  - t̄u = 0,8, d'où κ = x·t̄u ;
  - μ̄ = 0,25 ;
  - lv\* = 0,4 ; ν_F = 1/6 an (2 mois de ventes) ;
  - i_L = i_D = 3 % dans la boucle conjointe, r = 1 % dans les formes fermées, soit i = (1 + r)(1 + π̄) − 1 = 3,02 % à π̄ = 2 % et 11,1 % à π̄ = 10 % (taux nominal retenu aussi pour la ligne π̄ = 10 % de la boucle conjointe) ;
  - η_r = 2 par unité de taux ;
  - T_F = 0.

**Notation proposée** (critère 15). Contrôle par `grep -c -F` sur la spécification (commande au Retour). Les motifs `\varrho`, `\mathit{lv}`, `\mathit{ti}`, `\eta`, `\nu` et `\mathit{FU}` sortent à 0.

| Symbole | Sens | Unité |
|---|---|---|
| ti_t | part d'investissement visée, I^vol visé / ŷ_t. Elle se distingue du taux d'investissement restitué, I/PIB sur 12 tours | fraction |
| ŷ_t = (1 + γ) y_{t−1} | production attendue | u.v. par pas |
| ϱ_{L,t} = (1 + i_{L,t})/(1 + π\*) − 1 | taux réel du crédit anticipé, lu sur la cible π\* (lecture (c), comme la fiche 5) ; distinct de r = i − π | par an |
| ϱ̄_L | sa valeur à l'état résolu ; ce n'est pas une ancre des ratios réels | par an |
| η_r | semi-élasticité du plan au taux réel anticipé | sans dimension, par unité de taux |
| λ_ti, λ_K | vitesses (λ du cadre avec indice) | par an |
| lv_t = L_t/K_t, lv\* | levier sur K comptable, et sa cible | fraction |
| ν_F | dépôts visés, en années de ventes | an |
| FU | profits non distribués (fiche 2, symbole confirmé) | u.m. par pas |

h (indice réservé), ℓ et ε (tolérance du cadre) sont évités.

**Règle de financement F** (commune à S, C et R).
- **(F1) Demande de crédit, phase 3.**
  - Formule : ΔL^d_t = lv\*·[(1 − δ/n_a)K_t + p̂_t I^vol,plan_t] − L_t, avec p̂_t = p_{t−1}(1 + π\*)^{1/n_a}.
  - Elle ne lit que l'ouverture et le plan de la phase 2.
  - **Lecture (a) de Q7** :
    - la banque publie à l'ouverture, ou en phase 1, i_L et une condition d'octroi (plafond ou taux de service) ;
    - le bloc 6 propose la ligne 18, soit min(ΔL^d, plafond) ;
    - aucun ordre interne n'est nécessaire ;
    - le plan servi en phase 5 est celui de la phase 2 : `tab:phases` est inchangée.
  - L ≥ 0 tient par la forme : lv\*·K ≥ 0.
  - Le levier sur K comptable est exact à chaque pas où le plan est servi : L_{t+1}/K_{t+1} = lv\*, sans indice de prix ni vitesse.
- **(F2) Cible de dépôts.**
  - Formule : D\*_{t+1} = ν_F·n_a·p_{t−1}(1 + π\*)^{2/n_a}·v^e_{t+1}.
  - v^e_{t+1} est écrite en phase 5 par le bloc 2 et lue en phase 6.
- **(F3) Dividende, phase 6, résiduel de caisse.**
  - Formule : Div_{F,t} = max{0, D_{F,t} + ΔL_t + C_t + G_t − WB_t − i_L L_t/n_a + i_D D_{F,t}/n_a − T̂_{F,t} − D\*_{t+1}}.
  - T̂_{F,t} = Γ̂·T_{F,t−1} est une variable d'état, avec Γ̂ = [(1 + g)(1 + π\*)]^{1/n_a}.
  - Les intérêts sont assis sur les encours d'ouverture et les taux d'ouverture.
  - Le bloc ne lit en phase 6 ni T_F ni les intérêts écrits par les blocs 9 et 7 : critère 3 (d) tenu.
  - L'écart T_F − T̂_F est porté par D_F et résorbé au pas suivant.
- **Priorité des paiements** (critère 1 (d)) : WB (phase 4), puis intérêts et impôts (phase 6), puis Div_F en dernier.
  - L'investissement ne sort pas de dépôts au niveau du secteur, car la ligne 3 est interne aux entreprises sous J = 1.
  - Le crédit refusé cède d'abord sur les dividendes, puis sur D_F. Il ne cède jamais sur l'investissement.
  - La demande non satisfaite (ΔL^d − ΔL) est publiée.
- **Variantes de F écartées, mesurées dans la boucle conjointe** (`conj6_b.py`, `conj6_c.py`) :

  | Variante | Rayon | Statut |
  |---|---|---|
  | Levier sur p K^vol, avec cible de dépôts sur p v du pas | **1,4925** | vérifié |
  | Cible de dépôts sur p v du pas, levier comptable | **1,4991** | vérifié |
  | Levier sur p K^vol, avec cible sur v^e | **1,0530** (période 109 tours) | vérifié |
  | Ajustement partiel de D_F (λ_D = 0,5 à 2) avec levier sur p K^vol | 1,07 à 1,16 | vérifié |
  | Levier comptable avec cible sur v^e (F retenue) | 0,9971 | vérifié |

  *Précision après contre-épreuve indépendante (03/10/2026)* : les rayons de ce tableau sont mesurés sur l'option S à vitesse ×2 (λ_ti = 0,04) ; à la base, F retenue vaut 0,9980 (§ 3.B7). La variante « levier sur p K^vol » s'écrit L^cible = lv\*·p̂_t·K^vol_t d'ouverture ; selon l'écriture (prix p̂ ou p_{t−1}, capital d'ouverture ou capital après investissement), le rayon de S va de 1,0528 à 1,0538, toujours explosif.

  - **Mécanisme du levier sur p K^vol** : une hausse du niveau des prix réévalue le capital, donc relève la cible de crédit. Le crédit nouveau est versé en dividendes, d'où de la demande et des prix. C'est une réévaluation du capital qui alimente des flux, parente des instabilités 10 et 11. **Fait nouveau ; hypothèse sur le mécanisme.**
  - **Conséquence** : la cible de levier se pose sur K comptable. Elle n'est pas posée sur p K^vol, ce qui ne contredit pas l'acquis 2, qui portait sur les rentabilités.
  - Contrepartie : L/(p K^vol) = lv\*·ρ̄_K dépend de π̄. Il vaut 0,3114 à π̄ = 2 % et 0,1686 à π̄ = 10 % (`stat.py`). Cette dépendance est déclarée.

### 3.S Option S — part d'investissement visée (supermultiplicateur), nouvelle

1. **Source.** Forme inspirée du supermultiplicateur sraffien :
   - Freitas et Serrano (2015), *Review of Political Economy* 27(3), 258-281 ;
   - Lavoie (2016), *Metroeconomica* 67(1), 172-201.

   Existence vérifiée par recherche ; **articles non lus**, l'accès au texte étant bloqué par le proxy. L'écriture ci-dessous est la mienne : elle n'est pas attribuée à ces auteurs.
2. **Équations.**
   - Plan, phase 2 : I^vol,plan_t = ti_t·ŷ_t·exp[−η_r(ϱ_{L,t} − ϱ̄_L)]. Le plan nominal vaut p̂_t·I^vol,plan.
   - État, mis à jour en phase 5 après tu_t (phase 4) : ti_{t+1} = ti_t·exp[(λ_ti/n_a)(tu_t − t̄u)].
   - Financement : F.
3. **Verdicts.**

| Critère | Verdict | Mesure ou motif |
|---|---|---|
| 1 | **Conforme** | Lignes 3, 8, 14 et 18 ; aucun poste ajouté. Cas à la main ci-dessous : V_F par le stock et par les flux, écart de −5,2e−13 sur 1 800 u.m. (vérifié, `cas1.py`) |
| 2 | Compatible avec les deux voies | Distribution stationnaire en forme fermée ci-dessous |
| 3 | **Conforme** | Phase 2 : ti_t, y_{t−1}, i_L d'ouverture, π\* (paramètre). Phase 3 : lecture (a). Phase 5 : ti_{t+1} lit tu_t (phase 4). Phase 6 : F3. Matrice des lectures triangulaire, vérifiée à la main |
| 4 | **Conforme** | Ancre unique t̄u, paramètre lu par la fiche 4. x = κ/t̄u. Aucune bande de filtre |
| 5 | **Forme fermée** | Tableau du § 3.E. Aucune vitesse n'y entre (vérifié) |
| 6 (a), (b) | **Conforme, formes fermées** | λ_ti, η_r et ϱ̄ sont absents des ratios. Le facteur de taux est absorbé par ti : hors de ϱ̄, seul ti stationnaire change (vérifié par construction). L et D_F ont une ancre exacte sans vitesse (F1, F2) |
| 6, essai du J3 | **Échec mécanique**, par lenteur et non par continuum | Après G +1 % aux tours 1 à 12, écart entre les branches ×0,5 et ×2 : 3,9e−6 (K/Y et tu) et 7,6e−6 (I/ventes) à 720 pas ; 3,0e−6 à 1 440 pas ; **1,6e−7 à 2 160 pas**. L'écart décroît : c'est la transition, non un continuum (vérifié, `sim2.py`). Voir l'amendement proposé |
| 7 (b) | **Conforme** | Boucle propre : le couple (K^vol, ti) donne une paire de module √[(1 − δ/n_a)/(1 + γ)] = 0,99709 quand les racines sont complexes (hypothèse issue d'un système réduit 2×2 ; mesuré 0,9970 à 0,9972) |
| 7 (c) | **Tenu à la calibration pour m ≤ 0,7 ; échec à ×2 pour m = 0,7 (x = 3) et m = 0,8 (x = 2)** ; boucle conjointe stable | Tableaux du § 3.B7 |
| 7 (d) | **Conforme** | lv = lv\* à chaque pas. D_F/(12 PIB) = 0,16605 à i_L et à i_L + 2 points. La distribution passe de 0,5685 à 0,5133 (`stat.py`) |
| 9 | **Aucune borne à seuil libre** | I^vol ≥ 0 tient par la forme (exponentielle et ŷ ≥ 0) : c'est un mécanisme. Contraintes : L ≥ 0, par la forme ; D_F ≥ 0, inactive (D_F = 2 mois de ventes contre des paiements mensuels) ; Div ≥ 0 (pas d'actions au socle), inactive à la base (Div/ventes = 6,26 %), mais active si x > x_max (2,933 ans à μ̄ = 0,25 et lv\* = 0,4 ; 4,927 à μ̄ = 0,5 ; 2,853 à π̄ = 10 %). Scénarios adverses (G −5 %, crédit refusé de moitié pendant 12 tours) : **non mesurés** (J3) |
| 10 (b) | **tu lu** | Signe + sur ti. Niveau normal t̄u, ancre unique : la condition 4 de `jeu` a une conséquence déclarée, mais lente (§ 3.L) |
| 11 | **Conforme**, lecture (a) | Tableau de l'interface au § 3.F |
| 13 | Décompte | 7 paramètres libres (t̄u, κ, λ_ti, η_r, lv\*, ν_F, δ) ; ϱ̄ est résolu. 3 variables d'état (ti, y_{t−1}, T̂_F). 0 borne à seuil libre, 3 contraintes. Lignes 3, 8, 14, 18 ; aucun drapeau, aucun tirage |
| 14 | Conforme | Deux exponentielles et une vingtaine d'opérations par pas, sans itération. **Coût non mesuré** |
| 15 | Conforme | Symboles du tableau ci-dessus |

### 3.C Option C — ajustement du stock de capital avec terme de tendance (forme harrodienne), nouvelle

- **Équation** : I^vol,plan_t = (γ + δ/n_a)K^vol_t + (λ_K/n_a)(n_a x ŷ_t − K^vol_t). C'est équivalent à I/K^vol = (n_aγ + δ)/n_a + (λ_K/n_a)(t̂u_t/t̄u − 1), avec t̂u = n_a κ ŷ/K^vol.
- C'est la fonction d'accumulation dite harrodienne, g_K = g + γ_u(u − u_n), avec terme de tendance. La forme est la mienne : Skott (2012) n'a pas été lu.
- Financement : F.
- **Forme fermée identique à S.** Aucune vitesse n'y entre sur la trajectoire de référence (vérifié). I^vol ≥ 0 tient par la forme si λ_K < n_aγ + δ = 0,0698 par an (vérifié à la main).
- **Défaut au critère 6 avec un canal du taux.** Un terme −(η_r/n_a)(ϱ − ϱ̄) laisse t̂u/t̄u = 1 + (η_r/λ_K)(ϱ − ϱ̄) à l'état stationnaire. À η_r = 2, λ_K = 0,05 et un point d'écart : tu/t̄u = **1,4**, puis 1,8 et 1,2 aux vitesses ×0,5 et ×2 (calcul à la main). L'état d'arrivée dépend de la vitesse dès que ϱ ≠ ϱ̄ : c'est une fermeture kaleckienne par tu, et t̄u n'est plus une ancre. **Sans canal du taux**, C ne transmet le levier du taux que par la demande.
- **Critère 7 (c)** : § 3.B7.

### 3.R Variante sans retard (référence, `docs/exigences.md` § 2.7)

- Le capital visé est atteint dans le pas : C avec λ_K = n_a.
- **État stationnaire identique à S et C** (x = κ/t̄u ; I^vol/K^vol = (n_aγ + δ)/n_a). Les formes fermées de S et C n'ont donc aucun écart dû au retard (vérifié).
- Boucle investissement – demande : **4,02 à 4,04** pour m = 0,5 à 0,8. C'est l'accélérateur plein ; la variante sert de référence pour l'état stationnaire seulement.

### 3.P Variante PI (S + terme proportionnel de C), écartée

- Forme : I = ti·ŷ + (λ_K/n_a)(n_a x ŷ − K).
- **Plus lente** que S et C dans la boucle conjointe : 0,9985 à λ_K = 0,1 et λ_ti = 0,05. Elle est **instable** dans la boucle réduite dès m = 0,6 : 1,0019 ; 1,0199 à ×2 pour m = 0,5 (`conj6_pi.py`, `n_table.py`).
- Elle est écartée par le principe de simplicité et par le critère 7 (c).

### 3.B7 Boucles investissement – demande (critère 7 (c))

**(1) Boucle réduite avec N1 à N7** (`n_table.py`) : d = A + m·y_{t−1} + I^plan, prix exogènes, λ_v = 3, λ_IN = 1,5, σ = 1,4 mois. Chaque case donne le rayon à la base, puis aux vitesses du bloc 6 ×0,5 et ×2 (pour A et B, ι). La lettre P donne la période en tours.

| x = 3 | m = 0,5 | m = 0,6 | m = 0,7 | m = 0,8 (A < 0) |
|---|---|---|---|---|
| A | **1,1629** / 0,9849 / **1,2653** | **1,1948** / **1,0016** / **1,2915** | **1,2236** / **1,0199** / **1,3163** | **1,2505** / **1,0748** / **1,3401** |
| B | **1,1082** / 0,9816 / **1,1805** | **1,1403** / 0,9925 / **1,2066** | **1,1684** / **1,0101** / **1,2312** | **1,1946** / **1,0516** / **1,2547** |
| S (λ_ti = 0,02) | 0,9976 (P 4 562) / 0,9991 / 0,9981 | 0,9978 / 0,9991 / 0,9986 | 0,9987 / 0,9987 / **1,0003** | **1,0280** / **1,0252** / **1,0324** |
| C (λ_K = 0,05) | 0,9965 / 0,9986 / 0,9881 | 0,9968 / 0,9988 / 0,9939 (P 127) | 0,9975 / 0,9992 / **1,0121** | **1,0009** / **1,0002** / **1,0643** |
| R | **4,0245** | **4,0288** | **4,0331** | **4,0374** |

| x = 2 | m = 0,6 | m = 0,7 | m = 0,8 |
|---|---|---|---|
| S | 0,9975 / 0,9992 / 0,9978 | 0,9977 / 0,9991 / 0,9983 | 0,9986 / 0,9987 / **1,0003** |
| C | 0,9964 / 0,9985 / 0,9893 | 0,9967 / 0,9987 / 0,9928 | 0,9975 / 0,9992 / **1,0108** |

- **A et B avec les stocks** : l'échec de la partie 1 est **confirmé** (vérifié).
- **Condition nécessaire, écrite en forme fermée** : la part de demande autonome, rapportée à y, A = v/y − m/(1 + γ) − (n_aγ + δ)x, avec v/y = 1/(1 + n_aσγ), doit être positive (*Précision après contre-épreuve indépendante (03/10/2026)* : écrite d'abord avec 1 au lieu de v/y, ce qui donnait −0,0081 au lieu de −0,0104 à x = 3, m = 0,8 ; signe et verdict inchangés). C'est la condition du supermultiplicateur.
  - Le gain de basse fréquence ∂I/∂y d'une règle qui ancre x vaut exactement (n_aγ + δ)x : **0,2095 à x = 3** et 0,1396 à x = 2.
  - **À x = 3, m = 0,8 est hors du domaine (A = −0,0104)** : les cas m = 0,8 de la partie 1 avaient eux aussi A < 0. Ce constat est **nouveau ; il ne change pas le verdict de A et B**.
- **Condition de vitesse** : seuils mesurés.
  - S est instable dès λ_ti ≥ 0,05 à m = 0,7, et dès 0,1 à m = 0,6.
  - C est instable dès λ_K ≥ 0,1 à m = 0,7, et à 0,25 pour tout m (`n_scan.py`).

**(2) Boucle conjointe avec les fiches 3, 4 et 5** (`final_conj.py`). Système :
- la fiche 5 du § 3.C-10 : cible de Haig-Simons, lecture (c) ;
- le bloc 6 avec F ;
- x = 2, η_r = 2.

Rayon hors racine nominale, en régimes H et B (identiques au 4e chiffre). Chaque case donne la base, puis ×0,5 et ×2 sur la vitesse du bloc 6.

| Lecture du revenu | Ā (part de G) | S (λ_ti = 0,02) | C (λ_K = 0,05) |
|---|---|---|---|
| F (dividende résiduel) | +0,0040 | 0,9980 / 0,9992 / 0,9971 (P 2 287 à 2 296 selon la maquette) | 0,9961 / 0,9979 / 0,9964 |
| θ_H = 0,8 (salaires seuls) | +0,0660 | 0,9978 / 0,9992 / 0,9972 | 0,9959 / 0,9980 / 0,9926 |
| θ_H = 1 | **−0,1320** (hors du domaine) | 0,9978 / 0,9992 / 0,9972 | 0,9959 / 0,9980 / 0,9926 |
| F, π̄ = 10 % | — | 0,9979 / 0,9992 / 0,9971 | 0,9958 / 0,9979 / 0,9921 |
| F, toutes vitesses des blocs 2 à 6 ×0,5 et ×2 | — | 0,9992 / 0,9971 | 0,9979 / 0,9965 |

- **Stable partout** (vérifié). Demi-vies de 180 à 900 tours.
- La racine dominante de C et de S à ×2 est celle de **la valeur comptable du capital et du crédit** (vecteur propre : K, L et niveau des prix ; `ident.py`). Sans levier (lv\* = 0), elle vaut (1 − δ/n_a)/[(1 + γ)(1 + π̄)^{1/n_a}], soit, mesuré, **0,9926**.
  - C'est la contrepartie de la règle « K sans réévaluation » (l. 521). Elle est commune à toute option.
  - Statut : vérifié pour la mesure, hypothèse pour l'interprétation.
- **θ_H = 1 est hors du domaine** si I/PIB ≈ 14 % et sans impôts : l'épargne des ménages (environ 4 % du revenu) ne finance pas l'investissement sans rétention des entreprises. Cela répond à la **réserve 4 de la fiche 5** : sous F, la part du revenu versée aux ménages, (WB + Div)/PIB = 0,861 à la base, est un **résultat** (vérifié à partir des sorties de `cas1.py`).

### 3.E État stationnaire conjoint (critère 5, Q9, #44)

**Formes fermées** sous S, C ou R, avec F. Commande `stat.py`.

| Grandeur | Forme | x = 2 | x = 3 | π̄ = 10 % | n_a = 4 / 52 |
|---|---|---|---|---|---|
| K^vol/(n_a y) (iii) | κ/t̄u | 2 | 3 | 2 | 2 |
| ti | (n_aγ + δ)x | 0,13964 | 0,20946 | 0,13964 | 0,13970 / 0,13961 |
| Taux d'investissement, I/PIB | p·ti·y/(p v + ΔIN) | 0,13945 | 0,20917 | 0,13849 | 0,13951 / 0,13942 |
| p K^vol/(12 PIB) (ii) | x·p y/PIB_pas | 1,99726 | 2,99589 | 1,98361 | 1,99727 / 1,99726 |
| K/(12 PIB) (i) | ρ̄_K × (ii) | 1,55510 | 2,33264 | 0,83598 | 1,55356 / 1,55569 |
| L/K | lv\* | 0,4 | 0,4 | 0,4 | 0,4 |
| L/(p K^vol) | lv\*·ρ̄_K | 0,31145 | 0,31145 | 0,16858 | — |
| D_F/(12 PIB) | ν_F·p v/PIB_pas | 0,16605 | 0,16605 | 0,16492 | 0,16605 |
| V_F/(12 PIB) | (K + IN + D_F − L)/(12 PIB) | 1,19174 | 1,65826 | 0,75713 | 1,19051 / 1,19221 |
| FU/V_F par pas | Γ − 1 | 0,33059 % | idem | 0,964 % | — |
| Distribution Div/(Div + FU) | (R − FU)/R | 0,56853 | **−0,07314** | 0,39995 | 0,56791 / 0,56876 |

- **Contrôle de la forme fermée** : Div/ventes vaut 0,06262 en forme fermée comme dans la maquette conjointe (0,0626), à i = 3 % ; à i = 3,02 %, taux du tableau, 0,06252 ; l'écart entre la forme du résultat et la forme de caisse est nul.
- **Indépendance envers n_a** (critère 5 (b)) :
  - x et lv n'en dépendent pas ;
  - ti, I/PIB et la distribution en dépendent par n_aγ, à l'ordre 1e−4 en relatif (ADR 0008, I.6) ;
  - K/Y (i) et L/(p K^vol) en dépendent par ρ̄_K ;
  - toutes ces dépendances sont déclarées.
- **État initial résolu** :
  - K^vol_0 = n_a κ y_0/t̄u ;
  - ti_0 = (n_aγ + δ)x ;
  - K_0 = ρ̄_K p_0 K^vol_0 ;
  - L_0 = lv\*·K_0 ;
  - D_{F,0} = ν_F n_a p v ;
  - y_{−1} = y_0/(1 + γ) ;
  - T̂_F,0 = T̄_F/Γ.

**Quelle variable ferme S = I (critère 5 (c), Q9)** :
- **Sous S, C et R, tu ne ferme pas** : il tend vers t̄u, l'ancre unique, et il n'y a pas de surdétermination.
- **L'égalité se ferme par le niveau d'activité rapporté à la demande autonome**, par le supermultiplicateur à stocks et flux cohérents. La forme fermée vaut PIB = G/(1 − c̄·θ̄ − ι̂ − ι_N), avec :
  - c̄ = C/YD, fixé par ν (fiche 5) ;
  - θ̄ = YD/PIB, résultat de F ;
  - ι̂ = I/PIB ;
  - ι_N = ΔIN/PIB.
- **En ratios** :
  - les ménages fixent V_H = ν n_a YD^HS ;
  - les entreprises fixent L − D_F ;
  - l'État porte le solde : B/PIB = [ν n_a YD^HS − (L − D_F)]/(12 PIB), avec B_H ≡ 0 et une banque sans fonds propres.
- **Condition transmise à la fiche 9** : si la règle budgétaire vise B/PIB, le taux d'impôt est son résultat, sans surdétermination. Viser à la fois le taux et B/PIB surdétermine l'état stationnaire.
- **#44 (emploi)** : le niveau d'activité est déterminé par la demande. Sous S (λ_ti > 0), le taux n'a **aucun effet permanent** sur I/PIB : ti absorbe le facteur de taux. Le canal du taux sur la consommation est « à l'envers » (rentier, fiche 5).
  - **Le bloc 6 ne ferme donc pas U = U^eq.** La fermeture relève de la fiche 9 (règle budgétaire) ou d'un canal permanent du taux : fiche 5, lecture (d), ou fermeture kaleckienne, c'est-à-dire C avec canal du taux, qui fait dépendre tu de la vitesse.
  - **Point contesté**, trois fermetures en présence :
    - supermultiplicateur (Freitas et Serrano 2015 ; Lavoie 2016, non lus) ;
    - kaleckienne ;
    - wicksellienne (acquis R).
  - Fiches 8 et 9, mainteneur.

### 3.V Sous-colonnes des entreprises (#36, critère 2)

- **Voie (i)** : `tab:matrice-flux`, la clause de la l. 292 et la légende sont inchangées. FU est la somme de la sous-colonne courante.
  - Sortie de `verifier_matrices.py --strict`, identique avant et sous la voie (i) (`cmp`) : « tab:matrice-bilans : 9 lignes, 6 colonnes, 44 termes ; tab:matrice-flux : 28 lignes, 6 colonnes, 62 termes ; tab:portes-monnaie : 28 lignes, 3 colonnes, 31 termes ; Aucun écart. »
- **Voie (ii)**, sur une copie de la spécification : la ligne « 23 Profits non distribués » s'ajoute en fin de table, sans renumérotation des lignes 3, 8, 14, 17 et 18 citées.
  - Dans `tab:matrice-flux` : `& & $-\mathit{FU}$ & $+\mathit{FU}$ & & &`.
  - Dans `tab:portes-monnaie` : `$+\mathit{FU}$ & 0 & 0`.
  - Elle est proposée par le bloc 6 en phase 6, en dernier, comme ligne de lecture sans mouvement d'instrument.
  - Sortie : « tab:matrice-flux : **29** lignes, 6 colonnes, **64** termes ; tab:portes-monnaie : **29** lignes, 3 colonnes, **32** termes ; Aucun écart ». Le `diff` se limite à ces deux lignes : **changement conforme à l'attendu**.
  - À reprendre : la clause de la l. 292 (« chaque sous-colonne des entreprises somme aussi à zéro »), la l. 296 et la légende (l. 304).
- **Ce que la voie (ii) rend vérifiable** : chaque sous-colonne est nulle, et FU se lit dans une ligne.
  - **Mais `verifier_matrices.py` ne contrôle pas les colonnes de la matrice des flux au-delà du placement des postes** (docstring, l. 12 à 16, sous-colonnes réunies). Le gain demanderait d'étendre le script, ou que le noyau exécute la ligne.
  - Coût : une ligne non monétaire et un ADR.
- **Recommandation : voie (i).** L'information est la même (FU = somme de la sous-colonne courante, contrôlée par l'identité de V_F par le stock et par les flux, critère 1). C'est le principe de simplicité.
- **Distribution stationnaire en forme fermée, identique dans les deux voies** : Div/(Div + FU) = 1 − (Γ − 1)V_F/R, soit 0,56853.

### 3.F Interface crédit (critère 11) et cas à la main (critère 1)

| Sens | Grandeur | Phase | Ligne |
|---|---|---|---|
| Bloc 7 → bloc 6 | i_L et condition d'octroi (plafond ou taux de service), publiés à l'ouverture ou en phase 1 | ouverture ou phase 1 | — |
| Bloc 6 → bloc 7 | ΔL^d (F1) ; la proposition de ligne 18 vaut min(ΔL^d, plafond) | 3 | 18 |
| Publication | demande non satisfaite ΔL^d − ΔL, et sa fraction | 3 | — |
| Bloc 6 | intérêts i_L L_t/n_a, i_D D_{F,t}/n_a (propriétaire de la ligne 9 à fixer avec la fiche 7) ; Div (F3) | 6 | 9, 10, 14 |

**Robustesse (critère 11 (c))** :
- (i) Offre accommodante : c'est le cas de base.
- (ii) Rationnement partiel : sous J = 1, il ne réduit pas l'investissement. Il réduit les dividendes, donc le revenu des ménages. L'état stationnaire n'est pas affecté : le rationnement est un choc transitoire.
- **Accélérateur financier** : il est placé dans l'offre du bloc 7. Un facteur de disponibilité du crédit dans le plan (par exemple, le taux de service publié) est une question pour `monnaie`. Il n'est **pas** dans S au socle.

**Cas à la main** (`cas1.py`, pas stationnaire) : v = 100 u.v., p = 1,25, UC = 1, x = 2, lv\* = 0,4, i = 3 %.
- **Ouverture** : K = 2 341,2472 ; K^vol = 2 405,5493 ; L = 936,4989 ; D_F = 250 ; IN = 139,4480 ; V_F = 1 794,1963.
- **Flux** :
  - lignes 1 et 2 : C + G = 107,5049 ;
  - ligne 3 : I = 17,4951 (I^vol = 13,9961) ;
  - ligne 4 : ΔIN = 0,4610 ;
  - ligne 5 : WB = 100,2312 ;
  - ligne 8 : 9,7552 ;
  - ligne 9 : 2,3412 ;
  - ligne 10 : 0,6250.

| | Crédit accordé | Crédit refusé de moitié |
|---|---|---|
| Ligne 18, demande / accordé / non satisfait | 3,0960 / 3,0960 / 0 | 3,0960 / 1,5480 / 1,5480 |
| Ligne 14, Div | 7,8269 | **6,2789** (cède en premier) |
| Ligne 17, ΔD_F | 0,8265 | 0,8265 (D_F à sa cible, 250,8265) |
| L de clôture ; L/K | 939,5948 ; 0,400000 | 938,0469 ; 0,399341 |
| FU | 5,9314 | 7,4794 |
| V_F par le stock / par les flux | 1 800,1277 / 1 800,1277 (écart −5,2e−13) | 1 801,6757 / 1 801,6757 (écart −5,2e−13) |
| ΔD_F − ΔL = FU − (I − δK/n_a) − ΔIN | −2,2695 = −2,2695 | −0,7215 = −0,7215 |

Statut : vérifié.

### 3.Q Q2, Q3, Q5 (#37), Q11, Q12

- **Q2, définition de K/Y.**
  - O1 et la calibration sur (ii), p K^vol rapporté à 12 × PIB du pas : c'est le coût de remplacement courant, comparable à la comptabilité nationale (OCDE 2009, *Measuring Capital*, **non lu**).
  - Restitution : (ii) au joueur ; (i), comptable, dans le bilan, avec sa dépendance à π̄ (1,5551 à 2 % ; 0,8360 à 10 %).
  - Le rapport (iii) = x est l'ancre technique. La relation (ii)/(iii) = p y/PIB_pas vaut 0,99863 (vérifié).
- **Q3, κ, t̄u et x.**
  - t̄u est un **paramètre**, l'ancre unique lue par la fiche 4.
  - κ est un paramètre de technique.
  - x = κ/t̄u est un **résultat**.
  - À la calibration : x sur K/Y (ii), t̄u sur un taux d'utilisation établi (Federal Reserve G.17, **non lu**), d'où κ = x·t̄u.
- **Q11, δ.**
  - Un seul δ, par an, pour N10 et la ligne 8.
  - 5 % reste une **hypothèse**. La source est à lire au J3 (OCDE 2009, non lu). Aucune source n'est vérifiée à ce jalon.
- **Q5, #37, variantes d'offre.**
  - **(0) Aucun levier d'offre au socle**, déclaré (recommandé) : l'investissement agit sur la demande et sur tu (indicateur), pas sur la production possible (Leontief en travail, M24 (e) et (f)).
  - (1) Capacité qui contraint : révise M24 (e). Instabilité 15 (plafond, cycle) ; écartée sans fait nouveau.
  - (2) Productivité liée à l'accumulation (Arrow 1962, non lu) : révise M24 (f). L'état stationnaire en ratios est inchangé (g_K = g), mais le niveau de pr dépend du chemin (hystérèse, continuum de niveaux à déclarer). Stabilité **non mesurée**. Candidat au J5.
  - (3) Capital public : interface avec la fiche 9 seulement. Un stock public qui relève pr en niveau.
  - (4) Choc de niveau : J5, renvoi.
  - **Réponse à #37** : l'issue **reste ouverte jusqu'au J7**, sans `Closes`. Énoncé pour le catalogue des leviers (J4) et l'encadré de `sec:investissement` : « Au socle, l'investissement n'accroît pas la production possible : il crée de la demande et de la capacité normale, indicateur sans plafond. Un canal d'offre relève d'une décision citant M24. »
- **Q12** : renvoi au catalogue des leviers (J4) et au mode planifié (J7).
  - Interface : un crédit d'impôt ou un levier d'investissement entrerait comme facteur multiplicatif du plan, au même titre que e^{−η_r(·)}.
  - Il est absorbé par ti à très long terme ; son effet est donc durable à l'échelle d'une partie, mais non permanent.

### 3.L Exemple daté (critère 12) et interface du taux (7 (e))

*Remesuré le 03/10/2026 après les avis de `monnaie` (C34) et de `jeu` (§ 7). La version précédente ne déplaçait que le plan d'investissement.*

Commande `l1.py` (maquette `regle6.py` : boucle conjointe de `conj6.py`, option S, F, x = 2, η_r = 2, λ_ti = 0,02 par an, régime H, taux exogène).
- **Contrôle** : avec le seul canal du plan et Δi = 1,02 point (Δϱ_L = 1 point), la maquette reproduit l'ancien tableau à tous les tours publiés. Valeurs reproduites :
  - I : −1,98 % au tour 1, −2,21 % au tour 4, −0,50 % au tour 13 ;
  - Div : +3,24 % au tour 4 ;
  - y : −0,230 % au tour 4 ;
  - p : −0,425 % au tour 13.
- **Conventions** :
  - I^vol = I/p_t est le volume livré, celui qui entre dans K^vol (N10) ;
  - chaque colonne donne l'écart au sentier sans choc, sauf K^vol/(n_a y) et tu, qui sont des niveaux ;
  - le levier L/K vaut exactement 0,40000 à tous les tours.
- **Hypothèses de la maquette** :
  - pas d'impôts ;
  - G exogène en volume, à 0,40 % de la demande ; le choc est imposé en volume ;
  - π^e = π\* (pas de fiche 8) ;
  - banque sans fonds propres et i_L = i_D, d'où Div_Bk ≡ 0 ;
  - les intérêts de la dette publique implicite (B = V + D_F − L) sont financés par le déficit, sauf dans la ligne T9.

**(a) Dépense publique +1 % aux tours 1 à 12** (part de G de 20 %, **hypothèse**, soit +0,2 % de la demande ; taux inchangé)

| Tour | I (u.m.) | I^vol | K^vol/(n_a y) | tu | Crédit nouveau | Div | y | p |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 0 | 2,00000 | 0,80000 | 0 | +1,59 % | 0 | 0 |
| 2 | 0 | −0,010 % | 1,99833 | 0,80067 | 0 | +1,50 % | +0,084 % | +0,010 % |
| 3 | +0,093 % | +0,052 % | 1,99672 | 0,80132 | +0,21 % | +0,93 % | +0,164 % | +0,041 % |
| 4 | +0,206 % | +0,115 % | 1,99543 | 0,80183 | +0,46 % | −0,02 % | +0,229 % | +0,091 % |
| 9 | +0,596 % | +0,197 % | 1,99588 | 0,80165 | +1,33 % | −0,59 % | +0,212 % | +0,399 % |
| 13 | +0,635 % | +0,117 % | 1,99766 | 0,80094 | +1,39 % | −0,22 % | +0,126 % | +0,517 % |
| 14 | +0,647 % | +0,120 % | 1,99939 | 0,80025 | +1,41 % | +0,04 % | +0,040 % | +0,527 % |
| 18 | +0,312 % | −0,086 % | 2,00305 | 0,79878 | +0,64 % | +2,66 % | −0,142 % | +0,398 % |
| 24 | +0,252 % | −0,011 % | 2,00017 | 0,79993 | +0,49 % | +0,20 % | −0,001 % | +0,263 % |

- Au tour 14, l'investissement monte de +0,647 % en u.m., mais de **+0,120 % en volume**. Plus des quatre cinquièmes du mouvement nominal sont donc du prix (p +0,527 %). Le pic en volume est de +0,197 %, au tour 9 (`jeu` : +0,20 %, recoupé).

**(b) Taux du crédit et des dépôts +1 point aux tours 1 à 12, tous canaux (C34)**
- i_L et i_D sont lus à l'ouverture.
- ϱ_L monte de 0,980 point dans le plan.
- Les lignes 9 et 10 (sur L, D_F et les dépôts des ménages) passent au même taux.

| Tour | I (u.m.) | I^vol | Crédit nouveau | Div | YD | C^vol | y | p |
|---|---|---|---|---|---|---|---|---|
| 1 | −1,94 % | −1,94 % | −4,39 % | −6,87 % | +0,498 % | 0 | 0 | 0 |
| 2 | −1,94 % | −1,93 % | −4,37 % | −3,82 % | +0,611 % | +0,340 % | −0,114 % | −0,013 % |
| 4 | −2,05 % | −2,00 % | −4,57 % | −2,83 % | +0,749 % | +0,508 % | −0,008 % | −0,048 % |
| 6 | −1,92 % | −1,91 % | −4,25 % | −4,26 % | +0,778 % | +0,549 % | +0,127 % | −0,016 % |
| 9 | −1,67 % | −1,79 % | −3,64 % | −5,80 % | +0,821 % | +0,451 % | +0,206 % | +0,124 % |
| 12 | −1,55 % | −1,80 % | −3,32 % | −4,97 % | +0,942 % | +0,405 % | +0,161 % | +0,256 % |
| 13 | +0,42 % | +0,13 % | +1,15 % | +2,34 % | +0,488 % | +0,411 % | +0,144 % | +0,289 % |
| 24 | +0,33 % | 0,00 % | +0,88 % | +1,51 % | +0,434 % | +0,067 % | +0,003 % | +0,333 % |
| 36 | +0,38 % | +0,02 % | +0,95 % | +0,58 % | +0,406 % | +0,024 % | +0,016 % | +0,360 % |

**Par canal** (même choc ; y en écart cumulé)

| Canaux | y, tours 1 à 12 | y, tours 1 à 36 | y, tour 4 | p, tour 12 | Div, tours 1 / 4 |
|---|---|---|---|---|---|
| Plan seul (ancien tableau, Δϱ_L = 1 point) | −0,157 % | −0,025 % | −0,230 % | −0,414 % | +0,45 % / +3,24 % |
| Plan et ligne 9 (i_L sur L) | −0,524 % | −0,145 % | −0,553 % | −1,396 % | −9,53 % / −8,73 % |
| Tous canaux, intérêts publics financés par le déficit | **+0,093 %** | +0,057 % | −0,008 % | +0,256 % | −6,87 % / −2,83 % |
| Tous canaux + T9 | −0,154 % | −0,024 % | −0,226 % | −0,406 % | −6,87 % / −4,13 % |

T9 est une hypothèse de fiche 9, déclarée : le surcroît d'intérêts sur B est repris aux ménages par un prélèvement forfaitaire, dans le tour même.

- **Investissement** : −1,94 % au tour 1 pour +0,98 point de ϱ_L. En volume, il reste entre −1,79 % et −2,00 % sur les tours 1 à 12. Le « −2 % par point » tient en volume à 10 % près.
- **Dividendes (correction de la version précédente)**.
  - Le « signe contre-intuitif » (+3,2 % au tour 4) venait de l'isolement du plan. Avec tous les canaux, les dividendes **baissent** : −6,87 % au tour 1, −2,83 % au tour 4, −4,97 % au tour 12. La mention est retirée.
  - Décomposition au tour 1 :
    - intérêts sur L : −9,97 % (`monnaie`) ;
    - intérêts reçus sur D_F : +2,66 % ;
    - trésorerie libérée par l'investissement non fait : +0,45 %.
  - Le mécanisme de trésorerie libérée subsiste : il atténue la baisse, sans l'inverser.
- **Signe net sur la production** : il ne dépend pas du bloc 6.
  - Tous canaux, le canal rentier l'emporte dès le tour 6 (y +0,127 %). Le cumul sur 12 tours est de +0,093 % (`jeu` : +0,090 % pour +1 point de ϱ_L, recoupé).
  - Avec T9, le revenu des ménages ne bouge plus (YD −0,025 % au tour 4, contre +0,749 %). Le signe redevient alors celui du plan (−0,154 %).
  - Le signe du principal levier monétaire dépend donc de la fiche 9, qui décide qui paie le surcroît d'intérêts publics (condition 9 de `jeu`).
- **Délais en tours entiers (C35)** :
  - décision du tour n → i_L et i_D à l'ouverture du tour n + 1 → plan d'investissement et lignes 9 et 10 au tour n + 1 ;
  - investissement → demande : le même tour ;
  - revenus du tour n + 1 → plan des ménages du tour n + 2 (C^vol : 0 au tour 1, +0,340 % au tour 2) ;
  - investissement → capacité : le tour suivant ;
  - crédit → dépôts et dividendes : le même tour.
- **Statut** : les mesures sont vérifiées ; ce sont des résultats de maquette, sans statut de fait. L'interprétation des mécanismes est une hypothèse.

## 4. Tableau comparatif

| Critère | A (v1.5) | B (v2.0) | S (nouvelle) | C (nouvelle) | R (sans retard) |
|---|---|---|---|---|---|
| 1 Stock-flux | Écart (double amortissement) | Écart (évaluation au prix courant) | Conforme (cas à la main) | Conforme | Conforme |
| 2 #36 | voie (i) | voie (i) | (i) ou (ii) ; distribution 0,5685 | idem S | idem S |
| 3 Phases | Écart transposable | Écart transposable | Conforme, lecture (a) | Conforme | Conforme |
| 4 Ancrage | t̄u résultat, dépendant de ι ; filtre | idem | **t̄u ancre unique** | t̄u ancre unique | idem |
| 5 Forme fermée | Existe, dépendances | idem | **Sans vitesse** | Sans vitesse ; dépend de λ_K avec le taux | Sans vitesse |
| 6 Vitesses | **Échec** | **Échec** | Formes fermées conformes ; essai du J3 : 3,9e−6 à 720 pas, par lenteur | Idem sans le taux ; **échec avec le taux** | — |
| 7 (b) | 0,9718 | 0,9718 | 0,9971 | ≈ 1 − λ_K/n_a | — |
| 7 (c), boucle réduite avec stocks | **Instable** (1,11 à 1,34) | **Instable** | Stable pour m ≤ 0,7 sauf ×2 à m = 0,7 (x = 3) | Stable pour m ≤ 0,6 ; ×2 instable à m = 0,7 | **4,02** |
| 7 (c), boucle conjointe | non mesurée | non mesurée | **Stable** (0,9971 à 0,9992) | **Stable** (0,9926 à 0,9980) | — |
| 9 Bornes à seuil libre | 7 (dont une saturée) | environ 9, coudes actifs | **0** | 0 | 0 |
| 11 Crédit | Faillite | Lecture (a) | Lecture (a), rationnement sur Div | idem | idem |
| 13 Paramètres / état | 15 / 4 | environ 19 / 7 | 7 / 3 | 6 / 2 | 5 / 1 |
| 12 Lisibilité | q/q\* | ℓ\* | Investissement ∝ activité ; taux −2 % par point | Accélérateur sur tu | — |

## 5. Avis de l'expert pilote

*`macro`, 03/10/2026.*

**Recommandation : option S** (part d'investissement visée, ajustée sur tu − t̄u), avec la règle de financement F :
- levier visé sur **K comptable** ;
- cible de dépôts sur v^e_{t+1} ;
- dividende résiduel en dernier en phase 6 ;
- **lecture (a)** de Q7 ;
- i_L lu à **l'ouverture** (Q8, `tab:phases` inchangée) ;
- ϱ_L lu sur **π\*** (comme la fiche 5) ;
- **voie (i)** de #36 ;
- **aucun levier d'offre** au socle (#37 ouverte jusqu'au J7).

Calibration indicative (hypothèse) : t̄u = 0,8, x = 2, λ_ti = 0,02 par an, η_r = 2, lv\* = 0,4, ν_F = 2 mois, δ = 5 %.

**Motifs** :
- ancre unique t̄u ;
- formes fermées sans vitesse ;
- le facteur de taux est absorbé par ti, si bien qu'aucun continuum n'apparaît hors de ϱ̄, ce que C ne tient pas ;
- I^vol ≥ 0 par la forme ;
- aucune borne à seuil libre ;
- stable dans la boucle conjointe à la base et à ×0,5 et ×2 ;
- pas d'accélérateur (R vaut 4,02).

**Écartées** :
- A et B : critères 6 et 7 (c), confirmés avec les stocks ;
- C : critère 6 dès qu'un canal du taux existe ;
- PI : 7 (c) ;
- R : référence d'état stationnaire seulement ;
- levier sur p K^vol et cible sur les ventes du pas : explosifs (1,05 ; 1,49).

**Lectures soumises au mainteneur** :
- (a) **Fermeture de S = I** : supermultiplicateur (recommandé ; tu → t̄u), kaleckienne (C avec taux ; tu résultat, dépendant de la vitesse) ou wicksellienne (substitution, révise M24). Point **contesté**, avec `monnaie` et les fiches 8 et 9.
- (b) Q7 : lecture (a), recommandée, ou (b), ordre interne nouveau de la phase 3.
- (c) #36 : voie (i), recommandée, ou (ii), qui exige un ADR.
- (d) Base du levier : K comptable (recommandé) ou p K^vol (explosif sous ajustement complet).
- (e) Div ≥ 0 : contrainte de domaine de la ligne 14 sans actions (proposé), ou borne à seuil libre. À trancher avec I^vol ≥ 0 à M28 ; sous S, I^vol ≥ 0 tient par la forme.
- (f) **Amendement prospectif du critère 6** (voir plus bas).

**Réserves, avec leurs critères écrits avant l'essai (J3)** :
1. Un pas sans choc depuis l'état résolu laisse ti, y_{t−1}, lv, D_F/(n_a p v) et x sur leur sentier à 1e−10 près en relatif.
2. Rayon de la boucle conjointe < 1 en régimes H et B, à la calibration retenue et à ×0,5 et ×2 sur toutes les vitesses, avec la loi de π^e de la fiche 8 et la règle de la fiche 9.
3. Calibration : Div ≥ 0 stationnaire avec une marge déclarée. La condition x < x_max(μ̄, lv\*, π̄) vaut 2,933 à μ̄ = 0,25 : **x = 3 avec μ̄ = 0,25 est hors du domaine** (distribution de −0,073).
4. Scénarios adverses (G −5 %, crédit refusé de moitié pendant 12 tours) : Div ≥ 0 et D_F ≥ 0 cessent d'être actifs au plus tard 12 tours après le choc. **Non mesurés.**
5. A > 0 : m effectif + (n_aγ + δ)x < 1, contrôlé au chargement.
6. Lenteur : demi-vies de 240 à 900 tours sur tu et K/Y. tu s'écarte durablement de t̄u après un choc (fait pour `jeu`).

**Amendement prospectif proposé (critère 6, essai du J3)** :
- **Constat** : le seuil de 1e−6 après 720 pas est inatteignable par lenteur, et non par dépendance à la vitesse. Mesures de S : 3,9e−6 à 720 pas, 3,0e−6 à 1 440, 1,6e−7 à 2 160 ; C : 3,2e−6 à 720 pas. Toute option qui garde K sans réévaluation a une racine d'au moins 0,9926.
- **Proposition** : écart ≤ 1e−6 **après 2 160 pas**, ou écart rapporté à l'écart initial ≤ 1e−3 après 720 pas, ce dernier seuil restant à fixer par le mainteneur.
- Le verdict antérieur reste publié.

**Coût en fidélité** :
- le taux n'a pas d'effet permanent sur I/PIB ;
- le rationnement du crédit ne touche pas l'investissement sous J = 1 ;
- aucun choix de technique.

**Additif de `macro` (03/10/2026), après les avis de `monnaie` (§ 6) et de `jeu` (§ 7).**

**1. S ou S-ζ (§ 6.1, Q4 ; C36).**

*Maquette* (`regle6.py`) : la boucle conjointe du § 3.B7 (2) (fiches 2 à 6, N1 à N7, S, F, x = 2, η_r = 2, λ_ti = 0,02, régime H), à laquelle s'ajoute une règle de taux simple à action intégrale, déclarée.
- **Règle** :
  - inflation lue : π¹²_t = ln(p_t/p_{t−12}), en unités détendues, soit l'écart annuel à π\* ;
  - r\*_{t+1} = r\*_t + (k_I/n_a)·π¹²_t, avec k_I = 0,2 par an : action intégrale sans fuite (C2) ;
  - i_{t+1} = r\*_{t+1} + π\* + a_π·π¹²_t, avec a_π = 0,5 ;
  - i_L = i_D = i, lus à l'ouverture (C27).
- **Canaux du taux** : ϱ_L dans le plan ; lignes 9 et 10 ; Div_Bk ≡ 0.
- **Pas de π^e (fiche 8)** : le salaire se réfère à π\*. Tant que U ≠ U^eq, l'inflation dévie durablement, sans accélérer. C'est la différence avec la maquette de `monnaie`, qui a une courbe de Phillips accélérationniste, mais ni stocks ni dette publique.
- **Deux réglages budgétaires** :
  - sans impôts : G = 0,40 % de la demande ;
  - impôt proportionnel τ = 0,25 sur le revenu des ménages : G = 22,3 % de la demande.

  Chacun est mesuré avec ou sans T9 (reprise forfaitaire de (1 − τ)·Δi·B).
- **Choc** : G +1 % permanent.

*Modules dominants hors racine nominale (`r3.py`, `r7.py`)*

| Réglage | S | S-ζ, ζ = 2 |
|---|---|---|
| τ = 0, T9 | **1,000000** (racine unitaire) | 0,999688 (demi-vie de 2 221 tours) |
| τ = 0, sans T9 | **1,009238** (doublement en 75 tours) | **1,008902** |
| τ = 0,25, T9 | **1,000000** (racine double) | 0,998904 (demi-vie de 632 tours) |
| τ = 0,25, sans T9 | **1,002206** | **1,001229** |

*État d'arrivée après G +1 % permanent, avec T9 (`r5.py`, `r7.py`, `r8.py`)*

| | λ_ti ×0,5 | ×1 | ×2 |
|---|---|---|---|
| τ = 0, S (24 000 tours, sans arrivée) : r = i − π ; π ; tu | 2,932 % ; 2,0048 % ; 0,80190 | 3,440 % ; 2,0062 % ; 0,80121 | 3,831 % ; 2,0072 % ; 0,80070 |
| τ = 0, S-ζ (120 000 tours) : r̄ ; π̄ ; tu | 1,27985 % ; 2,00000 % ; 0,80440 | idem | idem (écart 2,7e−12) |
| τ = 0,25, S (7 200 tours, sans arrivée) | 13,27 % ; 2,092 % ; 0,8359 | 19,68 % ; 2,151 % ; 0,8297 | 27,90 % ; 2,226 % ; 0,8222 |
| τ = 0,25, S-ζ (120 000 tours) | 3,83265 % ; 2,00000 % ; 0,84569 | idem | idem (écart 1,5e−12) |

Sous S-ζ (τ = 0,25, T9), r̄, π̄ et tu sont aussi identiques au 8e chiffre dans les branches ×0,5 et ×2 de k_I, de a_π, de η_r et des vitesses des blocs 2 à 5.

**Constats.**
- (a) **Le constat de `monnaie` est confirmé dans la boucle conjointe, sous T9.** Sous S :
  - la racine est unitaire ;
  - le taux part en rampe ;
  - l'inflation garde un biais, et tu reste hors de t̄u ; tous deux dépendent de λ_ti.

  Vérifié (maquette).
- (b) **Fait nouveau : sans T9, le gain statique est positif.**
  - **Effet** : l'action intégrale explose avec S, avec S-ζ et avec ν(r) (fiche 5, ζ_H = 2 : 1,006095 à τ = 0 ; 1,001426 à τ = 0,25). La racine augmente avec ζ_H (1,0324 à ζ_H = 5, τ = 0). La seule partie proportionnelle (a_π = 1,5, k_I = 0) donne déjà 1,0020 (τ = 0).
  - **Seuils de ζ** :
    - à τ = 0, il faut ζ ≈ 40 pour approcher la stabilité locale (1,001056 à ζ = 40) ;
    - à τ = 0,25, la stabilité est locale dès ζ = 4 (0,999145). Mais il n'y a pas d'arrivée : à ζ = 4 et 6, le système diverge même pour un choc G +0,1 %. À ζ = 10 et 17, les branches ×1 et ×2 convergent (r̄ = 2,2934 % et 1,4651 %), mais la branche ×0,5 diverge.
  - **Conséquence** : sans reprise budgétaire, l'existence de l'état stationnaire dépend d'une vitesse. Aucun ζ testé (2 à 17) ne tient C36.

  Vérifié (`r2.py`, `r6.py`, `r11.py` à `r13.py`).
- (c) **Sous T9, S-ζ tient C36 (i) et (ii), mais seulement à l'horizon asymptotique.**
  - À 7 200 tours, l'écart relatif de r entre les branches λ_ti ×0,5 et ×2 vaut encore 5,4e−4 (τ = 0) et 1,6e−3 (τ = 0,25).
  - À τ = 0, r monte encore de 1,248 % à 1,280 % entre 7 200 et 120 000 tours. C'est une convergence, non une rampe : C36 (iii) ne les distingue pas.
- (d) **L'allocation d'arrivée ne dépend pas de ζ ; seul r̄ en dépend.** À τ = 0,25, avec T9 :
  - tu = 0,84569 et x = 1,8919 pour ζ = 2, 4, 5, 10 et 17 ;
  - r̄ − ϱ̄ vaut +2,833, +1,416, +1,133, +0,567 et +0,333 point, soit ∝ 1/ζ.
  - Sous S-ζ (ζ = 2), G +0,223 point des ventes a pour contrepartie I^vol −0,756 point et C +0,533 point.
  - Sous ν(r) (ζ_H = 2), tu = t̄u exactement, C baisse de 0,223 point, et r̄ monte de 9,26 points (`r14.py`).
  - **Le canal choisi décide donc quelle composante est évincée à long terme** : l'investissement (ζ), la consommation (ν(r)), ou la dépense et l'impôt (règle de la fiche 9). L'élasticité ne fixe que le taux nécessaire. Statut : vérifié pour la mesure ; le mécanisme de la hausse de C est une hypothèse.
- (e) **Ordre de grandeur.**
  - Dans le modèle (τ = 0,25, T9), r̄ monte de 72 points de base par point de B/PIB à ζ = 2, de 36 à ζ = 4, de 14,5 à ζ = 10 et de 8,5 à ζ = 17 (`r9.py`, `r10.py`).
  - **Fait établi** : Laubach, *New Evidence on the Interest Rate Effects of Budget Deficits and Debt*, FEDS 2003-12, version de mai 2007 (résumé, lu). Il estime « about 25 basis points per percentage point increase in the projected deficit/GDP ratio, and 3 to 4 basis points for the debt/GDP ratio », sur des taux à terme longs du Trésor américain.
  - Les concepts diffèrent (taux nominaux à terme d'un côté, taux réel du crédit stationnaire de l'autre). La comparaison est donc une **hypothèse** d'ordre de grandeur. Elle suffit à dire qu'à ζ = 2, le modèle est environ vingt fois plus sensible.
- (f) **Calibration de ζ (hypothèse, sans source lue).**
  - Par l'élasticité σ de K/Y au coût d'usage : ζ ≈ σ/(ϱ̄_L + δ). Pour σ de 0,25 à 1 et ϱ̄_L + δ ≈ 6 %, ζ va de 4 à 17.
  - σ est **contestée**. Chirinko, Fazzari et Meyer (1999), *Journal of Public Economics* 74(1), 53-80 : existence vérifiée, valeur non lue.
  - À ζ = 17, la contrainte Div ≥ 0 devient atteignable : x > x_max = 2,933 dès que Δϱ < −ln(2,933/2)/ζ = −2,25 points. À ζ = 2, il faudrait −19 points (calcul à la main).

**Formes fermées de S-ζ (critère 5)**, avec Δϱ = ϱ_L − ϱ̄_L stationnaire :
- tu = t̄u·e^{ζΔϱ} ;
- x = (κ/t̄u)·e^{−ζΔϱ} ;
- ti = (n_aγ + δ)(κ/t̄u)·e^{(η_r − ζ)Δϱ} ;
- I/PIB, K/Y (i) et (ii), V_F et la distribution : celles du § 3.E, avec ce x ;
- L/K = lv\* ; D_F inchangé.

À Δϱ = 0, elles sont identiques à S. **Vérification** (`z1.py`, taux exogène, Δϱ = +1 point permanent) :
- tu → 0,816161 et x → 1,960397, conformes à la forme, dans les branches λ_ti ×0,5, ×1 et ×2 ;
- écart de 2,3e−11 à 24 000 pas, de 7,3e−4 à 2 160 pas (S : 5,2e−3 à 2 160 pas).

**Critère 6.** ζ n'est pas une vitesse : l'arrivée ne dépend ni de λ_ti, ni de k_I, ni de a_π, ni de η_r, ni des vitesses des blocs 2 à 5 (mesuré ci-dessus). C'est une élasticité de niveau, comme ν. Le protocole du critère 6 (G +1 % aux tours 1 à 12, taux exogène) donne les mêmes résultats que S, puisque Δϱ = 0 : 3,9e−6 à 720 pas et 1,6e−7 à 2 160 pas.

**Critère 7 (c), taux exogène** (`z1.py`, fonction `rayon` de `final_conj.py`) : S-ζ ≡ S par construction. Rayons à la base, à ×0,5 et à ×2 :
- régime H : 0,9980 / 0,9992 / 0,9971 (P 2 296) ;
- régime B : identiques (P 2 297).

**Autres critères.**
- Critère 3 : ti_{t+1} lit tu_t (phase 4) et ϱ_{L,t} (ouverture) : conforme.
- Critère 4 : t̄u devient « le niveau normal à ϱ̄_L ». tu stationnaire vaut t̄u·e^{ζΔϱ} (0,8457 après G +1 %, τ = 0,25, T9). L'ancre est conditionnelle, et cela se déclare.
- Critère 9 : aucune borne nouvelle.
- Critère 13 : 8 paramètres libres.
- **Joueur** : aucun effet dans une partie. Au tour 120, i vaut 3,0112 % sous S et 3,0110 % sous S-ζ (τ = 0, T9).

**Position de `macro`.**
- **Accord sur le constat** de `monnaie`.
- **Accord sur la forme S-ζ** :
  - elle lève un coût de fidélité que j'avais déclaré (sans elle, le taux n'a pas d'effet permanent sur I/PIB) ;
  - ses formes fermées sont sans vitesse ;
  - elle est invisible dans une partie.
- **Désaccord sur sa portée.**
  - (1) Sans reprise budgétaire du surcroît d'intérêts publics, aucun ζ testé ne tient C36. La condition première relève donc de la fiche 9.
  - (2) Avec cette reprise, ζ = 2 rend r̄ environ vingt fois trop sensible à la dette.
  - (3) Le vrai choix est celui de la composante évincée (investissement, consommation ou budget). Il se fait à M27-M28 au vu de la fiche 9.
- **Je propose** :
  - retenir à M28 la forme S-ζ, avec ζ déclaré et à calibrer au J3 (ordre de grandeur de 4 à 17, hypothèse) ;
  - mesurer C36 avec la règle de la fiche 9 ;
  - si une autre fermeture est retenue, faire sortir le terme ζ de la spécification, par une décision citant M28. Un coefficient nul ne reste pas dans le texte.

**Désaccord résiduel, à trancher par le mainteneur (M28, avec M27 et la fiche 9)** :
- *`macro`* : la forme S-ζ est acceptable, mais elle ne garantit pas C36. Sans reprise budgétaire des intérêts publics, aucun ζ testé (2 à 17) n'y suffit ; avec elle, ζ = 2 rend r̄ environ vingt fois trop sensible à la dette. ζ se calibre au J3, et C36 se juge avec la règle de la fiche 9.
- *`monnaie`* (avis du § 6, antérieur à ces mesures) : S-ζ avec ζ = 2 à M28, pour donner à l'action intégrale C2 un état stationnaire ; à défaut, ν(r) ou la fiche 9.

**Condition transmise à la fiche 9** : la règle budgétaire dit qui paie le surcroît d'intérêts sur la dette publique. Sous déficit pur, le gain statique de la demande au taux est positif dans les deux réglages mesurés. Aucun canal du bloc 6 ne le compense alors sans faire dépendre l'arrivée d'une vitesse.

**Précision proposée pour C36** (prospective ; condition de `monnaie`) :
- (ii) s'évalue à un horizon d'au moins dix demi-vies de la racine dominante mesurée, ou avec un seuil de 1e−3 à 7 200 tours ;
- (iii) « aucune rampe » se lit : module dominant < 1 hors racine nominale, au point fixe.

**2. Réserve 6, remplacée** :

6. **Lenteur, après un choc permanent seulement.**
   - Les demi-vies de 240 à 900 tours sur tu et K/Y ne valent que pour les chocs permanents (nuance de `jeu`, § 7, question 2, confirmée par remesure, `t1.py`).
   - **Après un choc temporaire** (G +5 % aux tours 1 à 12) :
     - tu revient près de t̄u en 24 tours : 0,8112 au tour 6, 0,7939 au tour 18, 0,7997 au tour 24, 0,7999 au tour 120 ;
     - les trois branches de λ_ti sont identiques au 4e chiffre jusqu'au tour 24 ;
     - le reste, au plus 3e−4, s'efface à la vitesse lente.
   - **Après un choc permanent**, tu s'écarte durablement (G +5 % maintenu) : 0,8048 au tour 24, 0,8035 au tour 120, 0,8006 au tour 480.
   - Sous S-ζ avec action intégrale, tu se fixe à t̄u·e^{ζΔϱ} après un choc permanent.

**3. Lectures soumises au mainteneur, mises à jour** :
- (a) **Fermeture de S = I.**
  - Côté réel : le supermultiplicateur. `monnaie` et `jeu` sont d'accord.
  - Côté monétaire : C36 se juge avec la fiche 9. Les canaux de niveau candidats sont S-ζ (l'investissement est évincé), ν(r) (la consommation) et une règle budgétaire.
  - La fermeture kaleckienne est écartée : r̄ y dépend de λ_K (`monnaie`), et tu de la vitesse à taux exogène.
  - Point **contesté**.
- (b) à (f) : inchangées.
- (g) **S ou S-ζ** : le désaccord résiduel ci-dessus.
- (h) **Précision prospective de C36**, ci-dessus.
- **Coût en fidélité, mis à jour** :
  - sous S, le taux n'a pas d'effet permanent sur I/PIB ;
  - sous S-ζ, l'effet est de −ζ en log de x par unité de ϱ, à taux exogène.
- **Question 3 pour `jeu`** (dividendes qui montent avec le taux) : elle est sans objet avec tous les canaux (§ 3.L).

### Questions pour `jeu`

1. Est-ce perceptible ? Une hausse d'un point du taux donne −2 % d'investissement au tour 1 et −0,23 % de production au tour 4. Le choc G +1 % donne +0,65 % d'investissement au tour 14. Quel seuil proposer pour le critère 12 (d) ?
2. tu revient vers t̄u avec une demi-vie de 240 à 900 tours. Faut-il le garder comme indicateur avec son niveau normal (condition 4), ou sous une forme qualitative du type « capacités tendues » ?
3. Signe contre-intuitif : les dividendes montent quand le taux monte (+3,2 % au tour 4), et ils absorbent le crédit refusé. Faut-il le restituer, et comment ?
4. K/Y (ii) au joueur, et (i) dans le bilan : est-ce lisible ?

### Questions pour `monnaie` (frontière crédit, critère 11)

1. La lecture (a) convient-elle à la fiche 7 (conditions publiées à l'ouverture ou en phase 1, ligne 18 = min(ΔL^d, plafond)) ? Faut-il un facteur de disponibilité du crédit dans le plan, puisque, sous J = 1, le rationnement ne touche que les dividendes ?
2. i_L à l'ouverture, donc un tour de délai, ou en phase 1, ce qui ajoute le bloc banque à la phase 1 (issue sensible) ?
3. ϱ_L sur π\* : est-ce cohérent avec la clause C26 ?
4. Sous S, le taux n'a aucun effet permanent sur la demande d'investissement, et le canal de la consommation est rentier. Qu'en conclure pour la boucle 7 (e) et pour #44 ? Faut-il préférer la fermeture kaleckienne ?
5. Levier sur K comptable : L/(p K^vol) passe de 0,311 à 0,169 entre π̄ = 2 % et 10 %. Quelle conséquence pour la prime et l'accélérateur financier de l'offre ?

## 6. Avis de l'expert consulté

*Rédigé par `monnaie` (expert consulté sur la frontière crédit) le 03/10/2026. Avis porté sur la fiche à l'état `0586a92` (branche `claude/j1-economie-reelle`, PR #43). Il est cohérent avec mes avis sur les fiches 3, 4 et 5 (conditions C1 à C26). Les conditions nouvelles sont numérotées C27 à C36 (§ 6.3).*

*Sources lues :*
- *fiche 6 : § 1.1, § 1.5, critères 3, 7 (d) (e), 11 et 15, § 3.0, § 3.X, § 3.N, § 3.S, § 3.C, § 3.B7, § 3.E, § 3.F, § 3.L, § 4 et § 5 ;*
- *fiche 5 : § 5 et § 6 (dont § 6.5, C26) ;*
- *fiche 3 : § 6.1 (Q5) et § 6.3 (C1 à C8) ; fiche 4 : § 6.3 (C9 à C13) ;*
- *issue #44 ;*
- *`nations_et_marches.tex` : l. 252 et 253 (taux des instruments), l. 460 (intérêts), l. 504 à 509 (`tab:phases`), l. 521 et 523 ;*
- *`archive/v1.5/Nations_et_Marches_v1_5.tex` : l. 571 et 582 ; `archive/v2.0/prototype/model.py` : l. 896 et 897, l. 1972 à 1974 ;*
- *`archive/faits_mesures_G_K.md` : § 6 et § 8 ;*
- *scripts de `macro` `conj6.py` (l. 8 et 40) et `sim2.py` (l. 17 et 18), lus pour savoir où le choc de taux entre.*

*Calculs : six scripts du scratchpad, dans `monnaie6/` (commandes et sorties au Retour). Une contre-épreuve recoupe le cas à la main de `macro` : K_{t+1} = 2 348,9871, L/K = 0,400000 avec le crédit accordé et 0,399341 avec le crédit refusé de moitié, ΔL^d = 3,0959 (`macro` : 3,0960).*

*Statut des références :*
- *lu : texte primaire ;*
- *par reproduction : modèle GROWTH de Godley et Lavoie (2007, chap. 11) relu dans la reproduction sfcr `gl8-growth.Rmd`, téléchargée le 03/10/2026 ; l'ouvrage n'est pas lu ;*
- *extrait : notice ou résumé ;*
- *existence vérifiée, non lu.*

*Les sorties de maquette sont des résultats de modèle, sans statut de fait.*

### 6.1 Réponses aux cinq questions de `macro`

**Q1 — Lecture (a) de la phase 3 et facteur de disponibilité du crédit. La lecture (a) convient à la fiche 7. Je déconseille un facteur de disponibilité dans le plan au socle.**

1. **La lecture (a) est la forme standard de la monnaie endogène** : la banque affiche son prix, et la quantité suit la demande des emprunteurs solvables.
   - Moore (1988), *Horizontalists and Verticalists*, Cambridge University Press : existence vérifiée, non lu.
   - Godley et Lavoie, modèle GROWTH, par reproduction :
     - « Loans to firms supplied on demand », `Lfs ~ Lfd` (éq. 11.88, `gl8-growth.Rmd` l. 185) ;
     - taux du crédit `Rl ~ Rm + ADDl` (éq. 11.98, l. 203).
   - Statut : vérifié pour la forme de Godley et Lavoie (par reproduction) ; non lu pour Moore.
2. **Au socle, je recommande à la fiche 7 une offre accommodante au taux affiché, sans plafond** : la ligne 18 vaut ΔL^d. Le refus partiel du crédit reste un **scénario adverse déclaré** (critère 9 (c)), non une règle à seuil. C'est l'hypothèse (i) du critère 11 (c), qui devient le cas de base (C27).
3. **Pourquoi pas de facteur de disponibilité.**
   - Sous J = 1, la ligne 3 est interne aux entreprises : l'investissement agrégé ne se paie pas en dépôts.
   - Le crédit finance la masse salariale et les distributions. Un refus de crédit retombe donc sur Div, puis sur D_F (F3), jamais sur l'investissement. Ce n'est pas une omission de F : c'est la conséquence de l'agrégation.
   - Ordres de grandeur, recalculés sur le cas à la main de `macro` :
     - un refus **total** du crédit nouveau laisse Div = 4,7309 > 0 ;
     - pour épuiser Div puis D_F, il faudrait exiger un remboursement de 258,65 u.m. dans le tour, soit 27,6 % de L ou 2,58 mois de masse salariale ;
     - le remboursement volontaire maximal de F1 (plan nul) vaut lv\*·δK/n_a = 3,90 u.m. par tour, soit 1,56 % de D_F.

     Au socle, la contrainte D_F ≥ 0 ne peut donc s'activer que sous un rappel massif des crédits, qui relève de J6. Statut : vérifié (`m6_calc.py` et contrôle en ligne).
   - Un facteur de disponibilité serait un comportement, non une identité. Il coûterait au moins un paramètre, et en pratique un seuil (instabilité 15), sans donnée au socle. Sous une offre accommodante, il serait de plus inactif.
   - Le canal de prix (η_r sur ϱ_L) porte déjà la même information sous forme continue.
4. **Interface notée pour J6.** Le facteur entrerait comme facteur multiplicatif du plan, au même titre que e^{−η_r(·)}, sur la condition publiée à l'ouverture : aucun ordre interne nouveau. Sous S, il serait absorbé par ti à long terme.
5. **Fidélité.** Le canal « resserrement du crédit → investissement » (canal du crédit bancaire) est absent du socle : c'est un coût déclaré.

**Q2 (Q8) — Date de i_L. Je recommande i_L lu à l'ouverture**, comme variable d'état du bloc 7 écrite en fin de tour (phase 8 (c), ou clôture) à partir du i_CB du tour. Délai entre la décision et le plan : 1 tour.

1. **C'est la datation de Godley et Lavoie** (par reproduction) : les intérêts du pas portent le taux fixé au pas précédent sur l'encours d'ouverture, `Rl[-1]*(Lfd[-1] - IN[-1])` (éq. 11.38, l. 99), avec `Rl ~ Rm + ADDl` (l. 203). C'est aussi celle de la l. 460 : intérêts « assis sur [l']encours brut d'ouverture ».
2. **`tab:phases` est inchangée.** L'ajout du bloc banque à la phase 1 demanderait un ordre interne « banque centrale, puis banque », donc une issue sensible (amendement Q8).
3. **Un tour est le plus court délai du modèle**, et il reste bien plus court que les délais mesurés : chez Romer et Romer (2003, NBER w9866, lu pour la fiche 5, PDF p. 6), l'effet maximal sur la production industrielle survient après 22 mois. Un délai nul (phase 1) ferait agir la décision sur la demande au tour même.
4. **Coût, déclaré à la fiche 7 (C29)** : pendant le tour d'une décision, i_CB et i_res s'appliquent dès la phase 8 (a) (l. 460), alors que i_L et i_D ne changent qu'au tour suivant. La marge de la banque est donc comprimée, ou gonflée, pendant un tour.
5. **Délais qui en découlent (C35)** :
   - décision du tour n → plan d'investissement du tour n + 1 ;
   - décision du tour n → intérêts des lignes 9 et 10 au tour n + 1 → plan des ménages du tour n + 2, si i_D est aussi daté à l'ouverture.
6. **Point de forme pour `docwriter`.** La colonne « Lisent » de `tab:phases` omet « ouverture » pour les phases 2 et 3 (l. 505 et 506), mais la donne pour les phases 6 et 7 (l. 509). Sous la lecture (a), la phase 3 lit les conditions publiées à l'ouverture. Il faut dire si « ouverture » est implicite partout, ou l'ajouter. Ce n'est pas une décision de fond.

Statut : vérifié pour les sources et les lignes ; le choix est une recommandation.

**Q3 — ϱ_L lu sur π\* et cohérence avec C26. C'est cohérent, sous trois conditions (C32 et C33).**

1. **Une seule lecture de l'inflation dans l'économie.** Le bloc 6 doit lire la même π^lu que le bloc 5. Toute réouverture par C26 vaut donc pour les deux fiches, par une décision citant M27 et M28. Les conditions (ii) et (iii) de C26 incluent le canal de l'investissement, avec ϱ_L lu sur π^e. Sinon, ménages et entreprises liraient deux inflations différentes.
2. **Propriété utile.** Sous (c), on a exactement ϱ_L − ϱ̄_L = (i_L − ī_L)/(1 + π\*) : toute hausse du taux nominal est une hausse du taux réel perçu. Le canal de l'investissement n'exige donc pas le principe de Taylor, contrairement à une lecture sur π^e adaptative. Statut : vérifié (algèbre).
3. **Effet d'un changement de cible, à déclarer.** À i_L donné, une baisse d'un point de π\* fait passer ϱ_L de 0,9804 % à 1,9802 % et le plan de −1,98 %.
   - C'est de signe opposé à l'effet chez les ménages (+0,55 %, § 6.5 de la fiche 5).
   - Effet net sur la demande à l'impact : +0,085 point de PIB si G pèse 20 % du PIB, +0,193 point si G pèse 0,4 % comme dans la maquette conjointe. L'annonce d'une désinflation est donc légèrement expansionniste au tour même, à i_L donné.
   - Statut : vérifié pour le chiffre (`m6_calc.py`) ; parts de C et de I : hypothèses.
4. **Hors cible durable, ϱ_L surestime le taux réel de π̄ − π\*.** Exemple : π\* = 2 %, inflation stationnaire de 10 %, i_L de Fisher à r = 1 %. Alors i_L = 11,10 %, ϱ_L = 8,92 % contre ϱ̄_L = 1,00 %, et le plan est multiplié par 0,854 jusqu'à ce que ti l'absorbe. Sous C2, l'écart à la cible est transitoire. Dans les régimes B, D et E, sans cible propre, la π\* lue reste à définir (fiche 8 et J5, comme pour la fiche 5). Statut : vérifié (`m6_calc.py`).

**Q4 — Sous S, le taux n'a aucun effet permanent sur I/PIB. Conclusion : il ne faut pas préférer la fermeture kaleckienne, mais S ne suffit pas à la fiche 8.** C'est le point principal de cet avis.

1. **Constat structurel.** Sous S, le gain statique (à fréquence nulle) de l'investissement au taux est nul par construction : ti absorbe le facteur e^{−η_r(ϱ−ϱ̄)}. Avec une règle à action intégrale sans fuite (C2), le gain statique de la demande au taux vaut donc la somme de deux termes :
   - le canal rentier, de signe positif ou nul (fiche 5, § 6.1, Q3) ;
   - la règle budgétaire (fiche 9).

   Un intégrateur sur un système de gain statique nul a une racine unitaire. Sur un gain positif, il est explosif.
2. **Maquette** (`m6_dc.py`). Hypothèses :
   - S et la règle F réduite, sans stocks ;
   - Phillips accélérationniste sur l'écart de production (φ = 0,5) ;
   - π^e adaptative (λ_e = 1 par an) ;
   - règle i = r\* + π^e + 0,5(π_{t−1} − π\*), r\* intégrant π − π\* (k_I = 0,2 par an) ;
   - m = 0,6, x = 2, t̄u = 0,8, λ_ti = 0,02, η_r = 2 ;
   - c_R : terme rentier direct, en fraction de y\* par unité de taux.

   Modules dominants, puis délai de doublement ou demi-vie :

   | c_R | Module dominant | Délai |
   |---|---|---|
   | 0 | **1,000000** (puis 0,994379) | racine unitaire |
   | +0,02 | 1,000103 | doublement en 6 760 tours |
   | +0,05 | 1,000278 | doublement en 2 490 tours |
   | +0,10 | 1,000649 | doublement en 1 068 tours |
   | −0,02 | 0,999907 | demi-vie de 7 474 tours |
   | −0,10 | 0,999611 | demi-vie de 1 780 tours |

   Statut : vérifié (maquette).
3. **Continuum du taux réel, qui dépend des vitesses** (c_R = 0, `m6_dc2.py`).
   - Après un choc de demande autonome de +5 % pendant 12 tours, r\* se fixe au-dessus de r̄ de +3,77, +7,54 et +15,08 points de base pour λ_ti = 0,01, 0,02 et 0,04, et de +15,03, +7,54 et +3,79 points de base pour η_r = 1, 2 et 4. Le résultat est quasi indépendant de λ_e (7,53 à 7,55 points de base).
   - ti suit le même écart (ti/ti_0 = 1,00148 à la base).
   - **Le taux réel d'arrivée dépend de λ_ti/η_r et du chemin parcouru.** C'est le critère 6 appliqué à l'état monétaire, et c'est une structure parente de l'instabilité 4 (estimateur de r\* sans ancre ; R). Statut : vérifié pour la mesure ; parenté avec l'instabilité 4 : hypothèse.
4. **Choc budgétaire permanent : aucun état stationnaire** (`m6_dc3.py` et `m6_dc4.py` ; demande autonome +1 %, permanente ; c_R = 0).
   - **S avec C2** : l'écart de production se referme, mais i monte sans fin (4,05 % au tour 120 ; 13,03 % au tour 7 200). L'inflation garde un biais de +0,078 point à λ_ti = 0,02 (+0,039 et +0,155 point à λ_ti = 0,01 et 0,04), et tu se fixe à 0,8152 ≠ t̄u. La rampe du taux est le seul canal permanent : il faut tu − t̄u = η_r ϱ̇/λ_ti.
   - **S avec une règle à fuite vers r̄** (1 par an) : π part en rampe (2,59 % au tour 120 ; 7,80 % au tour 7 200).
   - **C avec canal du taux** (η_C = 2(n_aγ + δ), même effet d'impact) : π̄ = 2,000 % exactement et tu = 0,8152 pour toute λ_K. **Mais r̄ dépend de λ_K** : 1,347 %, 1,694 % et 2,388 % pour λ_K = 0,025, 0,05 et 0,10. Le module dominant est 0,994411 ; la racine 1 de la maquette est l'état ti, inutilisé dans C (vecteur propre pur sur ti, vérifié).
   - Statut : vérifié (maquette).
5. **Précision sur le verdict de C au § 3.C.** Il est exact à taux exogène. Avec une règle endogène qui ferme U = U^eq, tu est fixé par la fermeture de la demande et ne dépend pas de λ_K ; la dépendance à la vitesse passe sur r̄. **C reste donc écartée**, mais pour ce motif : le taux naturel serait fixé par une vitesse. Statut : vérifié (maquette).
6. **Ce que je propose : S avec un terme de niveau, « S-ζ »** (`m6_dc5.py`).
   - Forme : ti_{t+1} = ti_t·exp[(λ_ti/n_a)(tu_t − t̄u·e^{ζ(ϱ_{L,t} − ϱ̄_L)})]. Le taux d'utilisation visé croît avec le taux réel anticipé : c'est un capital désiré, x\* = κ/tu\*, qui décroît avec le coût réel du crédit.
   - ζ est une **élasticité de niveau, non une vitesse**.
   - M24 (e) et (f) restent intacts : le capital ne contraint toujours pas la production.
   - Mesures :

     | ζ | Module dominant | Demi-vie |
     |---|---|---|
     | 1 | 0,999333 | 1 038 tours |
     | 2 | 0,998665 | 519 tours |
     | 5 | 0,996648 | 206 tours |

   - Choc permanent de +1 % à ζ = 2 : r̄ = 1,9599 %, π̄ = 2,0000 % et tu = 0,81520 **à l'identique pour λ_ti = 0,01, 0,02 et 0,04**.
   - On retrouve ainsi la fermeture wicksellienne du niveau d'activité par le taux (acquis R « bouclage wicksellien », faits § 8) : r̄ est déterminé par G, ν, F et ζ, indépendamment des vitesses. C'est ce que supposaient C2 et C3.
   - Sous un taux exogène égal à ϱ̄_L (essais de la fiche 6), S-ζ se confond avec S : les formes fermées du § 3.E et le critère 6 du bloc sont inchangés.
   - Statut : vérifié (maquette).
7. **Coût de S-ζ.**
   - Un paramètre de plus. Sa source est l'élasticité du capital au coût d'usage, **contestée**. Chirinko, Fazzari et Meyer (1999), *Journal of Public Economics* 74(1), 53-80 : existence vérifiée, valeur non lue. Chirinko (1993) : candidat de `macro`, non lu.
   - Si la variante T de la fiche 4 est retenue, elle doit lire tu\*, et non t̄u, sous peine de surdétermination.
   - À l'état résolu, deux lectures sont possibles (#44) :
     - ϱ̄_L = r̄ est un paramètre et G_0 est résolu ;
     - r̄ est résolu à G/PIB donné, et seul t̄u·e^{−ζϱ̄_L} est identifié.
8. **Alternatives au même rôle**, dans mon ordre de recours de C14 (fiche 5, § 6.1, Q3, point 4) :
   - le coût du capital de la fiche 6 : c'est S-ζ ;
   - une règle budgétaire (fiche 9) ;
   - une cible de richesse ν(r) (fiche 5, M27).

   Sans aucun canal, il ne reste que la fermeture budgétaire de U, que j'ai déconseillée pour le pays joué (fiche 3, § 6.1, Q5) : décision du mainteneur.
9. **Interface pour le critère 7 (e) de la fiche 6.**
   - Élasticité d'impact : −1,98 % du plan par point (η_r = 2), délai d'un tour.
   - Élasticité de long terme : nulle sous S, et −ζ sur tu\* sous S-ζ.
   - La mesure de C10 et de C14 doit déplacer ensemble ϱ_L dans le plan, i_L et i_D dans les lignes 9 et 10, et Div_Bk. Or, dans `conj6.py` (l. 40), le choc `dr` n'entre que dans le plan (C34).

**Q5 — Levier sur K comptable : conséquences pour la prime et l'accélérateur financier de l'offre. Je recommande aucune prime sur le levier de l'emprunteur au socle (C28).**

1. **Une prime sur L/K comptable serait inerte sous F**, puisque lv = lv\* à chaque pas servi. L'écart vaut −1,5e−6 pour une surprise de prix de 0,05 % dans le pas, et −3,0e−5 pour 1 % ; il est corrigé au pas suivant, la cible portant sur un niveau. Le mot « exact » du § 3.N (F1) se lit donc « exact quand p_t = p̂_t et que le plan est servi ». Sous rationnement, lv baisse et la prime baisserait, à contresens d'une crise. La forme continue centrée sur ℓ\* proposée par la v1.5 (l. 582, R) serait donc sans effet. Statut : vérifié (`m6_calc.py`).
2. **Une prime sur L/(p K^vol) aurait deux défauts.**
   - Sa valeur stationnaire dépend de π̄ : 0,311 à 2 % et 0,169 à 10 % (§ 3.N). L'écart i_L − i_CB dépendrait donc de π̄, contre C15 (superneutralité).
   - Elle formerait une boucle de réévaluation : niveau des prix en hausse → levier de marché en baisse → prime en baisse → investissement et demande en hausse → prix en hausse. C'est le parent, par les prix, du mécanisme explosif du levier sur p K^vol que `macro` a mesuré (1,49 ; 1,05), et des instabilités 10 et 11. Statut : hypothèse, non mesurée.
3. **La forme de la v2.0**, i_L = i_CB + mL + ρ1·max(ℓ − ℓ̄, 0) avec ℓ sur p_K·K (`model.py` l. 1972 à 1974), est une borne à seuil libre : instabilité 15. Elle ne se reprend pas.
4. **Recommandation.** Au socle, l'écart i_L − i_CB dépend au plus de l'état propre de la banque : fonds propres rapportés à L, deux stocks nominaux, donc superneutre. C'est la forme de Godley et Lavoie, `ADDl` réglé sur un objectif de fonds propres et de profit (éq. 11.99 à 11.106, l. 203 à 214, par reproduction). L'accélérateur de Bernanke, Gertler et Gilchrist (1999 ; cité par la v1.5, l. 571 ; non lu) attend J6, où la valeur nette des emprunteurs sera définie avec les actions et les prix d'actifs.
5. **Conséquence bancaire du levier comptable, à déclarer (C30)**, recalculée sur le tableau du § 3.E :

   | Grandeur | π̄ = 2 % | π̄ = 10 % |
   |---|---|---|
   | L/(12 PIB) | 0,622 | 0,334 |
   | (L − D_F)/(12 PIB) | 0,456 | 0,169 |

   - À V_H/PIB donné, la dette publique et la part de titres détenue par la banque portent l'écart, soit +0,287 année de PIB à 10 %. Statut : vérifié (arithmétique sur les valeurs de `macro`).
   - Le sens est conforme à un fait établi : la profondeur financière décroît avec l'inflation, selon une relation inverse et non linéaire (Boyd, Levine et Smith, 2001, *Journal of Monetary Economics* 47(2), 221-248 ; résumé extrait). Le mécanisme du modèle, la valeur comptable sans réévaluation, n'est pas celui de l'article.
   - Pour C15 : si le canal rentier n'est pas neutralisé, une dette publique plus forte à 10 % relève le revenu des ménages et casse la superneutralité des allocations réelles. Hypothèse, non mesurée.

### 6.2 Avis général, côté monnaie

**Favorable à S avec F, lecture (a), i_L à l'ouverture, ϱ_L sur π\*, voie (i) et aucun levier d'offre**, sous une réserve de fond : **le canal permanent du taux** (Q4).

- **Règle F.**
  - F1 :
    - L ≥ 0 tient par la forme ;
    - le remboursement volontaire maximal reste faible (1,56 % de D_F par tour) ;
    - lv est exact à 3e−5 près sous une surprise de prix de 1 %.
  - F2 : cible de dépôts sur v^e, stable.
  - F3 : dividende résiduel. **Le canal de trésorerie de la politique monétaire sur les entreprises devient un canal de distribution vers les ménages.** Une hausse d'un point de i_L retire 0,780 u.m. par tour à Div_F, soit −9,97 % ; i_D sur D_F en rend 0,208, soit +2,66 %. L'effet passe à Div_Bk en équilibre général.
  - Le signe contre-intuitif du § 3.L (Div +3,24 % au tour 4) est mesuré **sans** les flux d'intérêts (`conj6.py` l. 40). Avec eux, Div_F baisserait probablement : environ −4 %, en additionnant ces ordres de grandeur. Hypothèse, à mesurer avec C34.
  - Différence avec le modèle GROWTH de Godley et Lavoie (par reproduction) : dividendes sur le profit retardé (11.36), rétention visée ψ_U·INV[−1] (11.35), crédit résiduel (11.39). F inverse les rôles, crédit visé et dividende résiduel. Les deux structures sont stock-flux cohérentes ; F est retenue par `macro` pour sa stabilité mesurée. Je n'y oppose rien.
- **Lecture (a) de Q7** : favorable (Q1).
- **Date de i_L** : à l'ouverture (Q2).
- **ϱ_L sur π\*** : favorable, sous C32 et C33 (Q3).
- **Fermeture S = I et #44.**
  - L'égalité de l'épargne et de l'investissement se ferme par le niveau d'activité (supermultiplicateur), et tu → t̄u. J'en suis d'accord pour le côté réel.
  - **Côté monétaire, S seule laisse la fiche 8 sans gain statique de la demande au taux.** L'action intégrale C2 y a alors soit une racine unitaire (continuum de r̄ et de ti, fonction de λ_ti/η_r), soit une racine lentement explosive (canal rentier positif). Sous un choc budgétaire permanent, elle n'a aucun état stationnaire : le taux part en rampe, et le biais d'inflation dépend de λ_ti.
  - Sur un horizon de partie (≤ 120 tours), ces effets restent faibles. Mais ils interdisent l'état stationnaire exigé par C2 et C3, et ils reproduisent la structure de l'instabilité 4.
  - **Je recommande S-ζ**, ou un canal de même rôle dans la fiche 5 ou la fiche 9, décidé à M27-M28. **Je ne recommande pas la fermeture kaleckienne** : r̄ y dépend de λ_K.
- **Accélérateur financier dans l'offre** : aucun au socle (Q5).
  - La place déclarée au critère 11 (c) est l'offre du bloc 7, par i_L.
  - Il ne s'appuie sur aucune grandeur du levier de l'emprunteur tant que la valeur nette n'est pas définie (J6).
  - S'il revient, il passe par ϱ_L et η_r, sans paramètre nouveau dans le bloc 6.

**Désaccord avec `macro`, à trancher par le mainteneur (M28, avec M27)** :
- *`macro`* : S sans canal permanent du taux ; la fermeture de U (#44) relève de la fiche 9 ou d'un canal hors du bloc 6 ; C est écartée par le critère 6.
- *`monnaie`* : S-ζ (tu visé fonction de niveau de ϱ_L) ou un canal de même rôle en fiche 5 ou 9, décidé à M27-M28. Sans lui, l'action intégrale C2 n'a pas d'état stationnaire sous un choc budgétaire permanent. C reste écartée, parce que r̄ y dépend de λ_K.

Aucun autre désaccord : lecture (a), date de i_L, ϱ_L sur π\*, levier comptable, voie (i), aucun levier d'offre.

### 6.3 Conditions transmises

**Fiche 7 (banque commerciale)** :
- **C27 — Offre au socle.** Prix affiché et quantité à la demande (lecture (a)). i_L et i_D sont des variables d'état du bloc 7, lues à l'ouverture et écrites en fin de tour à partir du i_CB du tour. Pas de plafond au socle. Le refus partiel est un scénario déclaré (critère 9 (c) de la fiche 6), jamais une règle à seuil. La ligne 18 négative (remboursement) est acceptée.
- **C28 — Écart i_L − i_CB.** Aucune prime sur le levier de l'emprunteur au socle :
  - sur L/K comptable, elle serait inerte sous F ;
  - sur L/(p K^vol), elle ne serait pas superneutre et créerait une boucle de réévaluation.

  Un mécanisme d'écart, s'il existe, lit l'état propre de la banque (fonds propres sur L), est superneutre et déclaré. L'accélérateur de Bernanke, Gertler et Gilchrist attend J6.
- **C29 — Marge pendant le tour d'une décision.** i_CB et i_res s'appliquent dès la phase 8 (a) du tour (l. 460) ; i_L et i_D au tour suivant. L'effet sur Π^Bk et Div_Bk est déclaré, et i_L et i_D portent la même date.
- **C30 — Bilans fonction de π̄.** L/(12 PIB) passe de 0,622 à 0,334, et (L − D_F)/(12 PIB) de 0,456 à 0,169 entre π̄ = 2 % et 10 %. La composition de l'actif bancaire (B_Bk) et B/PIB portent l'écart (+0,287 année de PIB). C'est déclaré et testé avec C15 ; c'est aussi un renvoi à la fiche 9.
- **C31 — Robustesse du bloc 6.** Le cas de base de la fiche 6 est C27. Le scénario « refus de la moitié du crédit pendant 12 tours » se mesure avec F3 ; Div ≥ 0 et D_F ≥ 0 doivent y rester inactives (marges du § 6.1, Q1).

**Fiche 8 (banque centrale et anticipations)**, en complément de C1 à C26 :
- **C32 — Une seule lecture de l'inflation.** ϱ_L lit la même π^lu que le bloc 5. Une réouverture par C26 vaut pour les fiches 5 et 6, par une décision citant M27 et M28. Les boucles de C26 (ii) et (iii) incluent le canal de l'investissement.
- **C33 — Changement de cible.** Effets à déclarer :
  - −1,98 % du plan d'investissement par point de baisse de π\* à i_L donné, contre +0,55 % pour le plan des ménages ;
  - effet net à l'impact de +0,085 à +0,193 point de PIB ;
  - hors cible durable, ϱ_L surestime le taux réel de π̄ − π\* (facteur 0,854 à 10 %).
- **C34 — Mesure de C10 et C14.** Les canaux du taux sont déplacés ensemble : ϱ_L dans le plan, i_L et i_D dans les lignes 9 et 10, Div_Bk. L'effet du plan seul ne suffit pas.
- **C35 — Délais.** Décision du tour n → i_L et i_D à l'ouverture du tour n + 1 → plan d'investissement du tour n + 1 → plan des ménages du tour n + 2. C16 est mise à jour en conséquence.
- **C36 — Gain statique et stationnarité de l'action intégrale**, critère écrit avant l'essai :
  - (i) le gain statique (fréquence nulle) de la demande totale au taux réel est strictement négatif, tous canaux réunis (fiches 5, 6 et 9) ;
  - (ii) après un choc budgétaire permanent de +1 %, π̄ = π\* à 1e−6 près et r̄ est identique à 1e−6 près en relatif dans les branches ×0,5 et ×2 de toutes les vitesses ;
  - (iii) aucune rampe du taux sur 7 200 tours.

  Si (i) échoue sous S sans ζ, C2 n'est pas admissible, et la fermeture revient à la décision du mainteneur : S-ζ, ν(r) ou fermeture budgétaire. C36 précise C14 et le fait nouveau qu'exige C2 contre l'instabilité 4.

### 6.4 Points signalés à `jeu` (non tranchés)

- « Resserrement du crédit → investissement » : absent au socle. Un refus de crédit touche les dividendes, donc la consommation au tour suivant.
- Le signe « taux en hausse → dividendes en hausse » vient d'un essai où seul le plan bouge. Avec les flux d'intérêts, les dividendes des entreprises baisseraient probablement, et le revenu passerait par la banque. À remesurer (C34) avant toute restitution.
- Délai d'un tour entre la décision de taux et l'investissement, et de deux tours pour la consommation.
- Changer la cible d'inflation agit au tour même, en sens opposé sur l'investissement et la consommation (C33).
- Sous S sans ζ, le « taux neutre » change avec l'histoire de la partie. Comme référence affichée, il serait illisible.
- Le crédit aux entreprises rapporté au PIB baisse de moitié entre 2 % et 10 % d'inflation stationnaire.

**Commentaire proposé par `monnaie` sur #44** (soumis au mainteneur ; texte dans le compte rendu de la session, PR #43).

### 6.6 Additif de `monnaie` (03/10/2026) : S-ζ après les mesures de `macro`

*Relance ciblée sur le désaccord S / S-ζ. J'ai lu l'additif de `macro` (§ 5), le § 3.L remesuré et les scripts `regle6.py`, `r1.py`, `r3.py`, `r5.py` et `r7.py` à `r10.py`.*

*J'ai écrit quatre scripts dans `monnaie6/` :*
- *`m6_fisc.py` : copie de `regle6.py` où un prélèvement forfaitaire sur les ménages est réglé sur B/PIB ;*
- *`m6_fisc1.py` à `m6_fisc3.py` : les essais.*

*Les sorties de maquette sont des résultats de modèle. Elles n'ont pas le statut de faits.*

**1. Vérification des mesures de `macro` (question 1)**

- **Mesures reproduites** au dernier chiffre affiché. Statut : vérifié.
  - Sans T9, modules dominants :
    - S : 1,009238 à τ = 0 et 1,002206 à τ = 0,25 ;
    - S-ζ (ζ = 2) : 1,008902 et 1,001229 (`r1.py`, `r7.py`).
  - S-ζ avec T9, τ = 0,25 :
    - r̄ = 3,83265 %, π̄ = 2,00000 %, tu = 0,84569 ;
    - valeurs identiques au 8e chiffre dans les branches ×0,5 et ×2 de k_I, a_π, η_r et des vitesses des blocs 2 à 5 ;
    - demi-vie de 632 tours (`r8.py`).
  - S avec T9, τ = 0,25 : racine unitaire. Au tour 7 200, r vaut 13,27 %, 19,68 % ou 27,90 % selon λ_ti (`r8.py`).
  - Sensibilité de r̄ à la dette : 72,5 pb par point de B/PIB à ζ = 2 (`r9.py`), 36,2 à ζ = 4 et 8,5 à ζ = 17 (`r10.py`).
- **Mon constat initial est confirmé.** Avec le canal du plan seul, S a deux racines unitaires (la nominale et celle de l'action intégrale) ; S-ζ n'en a qu'une, la nominale (`r1.py`). Statut : vérifié.
- **(a) Le ratio « pb par point de B/PIB » n'identifie pas un effet de la dette sur le taux.**
  - Sous T9 (τ = 0,25), B/PIB monte de +3,91 points. Cette hausse se décompose ainsi (`m6_fisc2.py`) :
    - ΔV = +0,54 point ;
    - ΔD_F = 0,00 ;
    - −ΔL = +3,37 points.
  - 86 % de la hausse de B est donc le miroir de la baisse du crédit. C'est l'identité B = V + D_F − L, avec une banque sans fonds propres.
  - Cette décomposition est la même pour ζ = 2 et ζ = 10. Le ratio divise donc r̄ − ϱ̄ (∝ 1/ζ) par un résultat d'allocation qui ne dépend pas de ζ.
  - Statut : décomposition vérifiée ; interprétation : hypothèse.
- **Rapporté à la dépense publique** (G +0,223 point de PIB), r̄ monte de :
  - 1 270 pb par point de G/PIB à ζ = 2 ;
  - 635 pb à ζ = 4 ;
  - 254 pb à ζ = 10 ;
  - 149 pb à ζ = 17.

  (Calcul fait sur les sorties de `r8.py` et `r10.py`.)
  - Laubach, FEDS 2003-12, version de mai 2003, résumé lu : « roughly 25 basis points » par point de déficit projeté rapporté au PIB.
  - Les concepts diffèrent : taux longs à terme d'un côté, taux réel stationnaire de l'autre. Le rapprochement n'est qu'un ordre de grandeur (hypothèse).
  - Le chiffre « vingt fois » de `macro` n'est donc pas robuste. La sensibilité de r̄ tient à l'allocation au moins autant qu'à ζ : pour G +0,223 point, I^vol baisse de 0,756 point, parce que C monte de 0,533 point.
  - Mécanisme supposé (hypothèse) : sous F3, la trésorerie libérée par l'investissement non fait est distribuée en dividendes, qui soutiennent C.
- **(b)** Le terme T9 lit i − i0 même quand le canal « D » est coupé (`regle6.py`, ligne de YD). C'est sans effet sur les mesures publiées, faites avec tous les canaux. Statut : vérifié par lecture.
- **(c) Limite de la maquette** : banque sans fonds propres, i_L = i_D et Div_Bk ≡ 0. Le canal de la marge bancaire (C29) est absent. Non mesuré.
- **(d) Le réglage τ = 0 est un cas limite** : G y vaut 0,40 % de la demande et B/PIB 41 %, sans fiscalité. Il ne devrait pas peser dans la calibration (avis).

**2. Faut-il la reprise forfaitaire T9, ou une règle de dette suffit-elle ? (fait nouveau)**

*Montage (`m6_fisc1.py` à `m6_fisc3.py`) : sans T9, un prélèvement forfaitaire T = θ·p·y sur les ménages, avec b = B/(12 p y).*

- **Cible intégrale de B/PIB** (θ suit (k_B/n_a)(b − b0)) : explosive et oscillante pour tous les ζ testés (0 à 10).
  - τ = 0,25 : de 1,001231 à 1,001379 avec k_B = 0,2 ; de 1,000021 à 1,000216 avec k_B = 0,05 et ζ ≥ 2.
  - τ = 0 : de 1,0045 à 1,0080.
  - Statut : vérifié (maquette).
- **Réaction de Bohn** (T/PIB = φ_B(b − b0)), τ = 0,25 :
  - **Stabilité locale** : acquise dès ζ = 4 avec φ_B = 0,005 (0,999050). À ζ = 2, il faut φ_B = 0,1 (0,999351).
  - **Pas d'arrivée sous G +1 % permanent** dans deux cas pourtant stables localement :
    - ζ = 4, φ_B = 0,02 : r +15,3 points au tour 1 200, puis divergence ;
    - ζ = 2, φ_B = 0,1 : r +9,3 points au tour 4 800, puis divergence.

    Les deux convergent sous G +0,1 % (`m6_fisc3.py`).
  - **Arrivée sous G +1 %** dans deux cas : r̄ +0,841 point (ζ = 4, φ_B = 0,1) et +0,629 point (ζ = 10, φ_B = 0,02). Les valeurs sont identiques, à 1e−4 point près, dans les branches ×0,5 et ×2 de λ_ti et de k_I (`m6_fisc2.py`).
  - **À τ = 0** : aucune combinaison testée (φ_B ≤ 0,1, ζ ≤ 10) n'est stable localement (`m6_fisc1.py`).
  - Statut : vérifié (maquette).
- **Lecture (hypothèse, algèbre approchée)** : à l'état stationnaire, une règle de Bohn ne reprend qu'une fraction φ_B/(g − i + φ_B) du surcroît d'intérêts.
  - Le reste est un revenu rentier permanent.
  - Avec i < g (ici i0 = 3 % contre 4,04 %), cette fraction est inférieure à 1 pour tout φ_B fini. T9 est la limite φ_B → ∞.
- **Littérature**
  - Leeper (1991), *JME* 27(1), 129-147 (résumé lu) : l'existence et l'unicité de l'équilibre dépendent ensemble de la réaction de la politique monétaire et de celle de la politique budgétaire à la dette.
  - Bohn (1998), *QJE* 113(3), 949-963 (résumé lu) : le surplus primaire des États-Unis croît avec B/PIB.
  - Point propre au modèle (hypothèse) : la soutenabilité de la dette ne suffit pas, c'est le gain statique de la demande au taux qui décide (C36 (i)).
  - Godley et Lavoie, par reproduction (vignette sfcr `gl2-pc.Rmd`, section « The puzzling impact of interest rates reconsidered », modèle PCEX2) : l'effet expansionniste du taux y est traité en faisant dépendre la propension à consommer du taux, α1 = α10 − ι·r[−1]. C'est la voie ν(r). Ouvrage non lu.

**3. Portée de S-ζ (question 2)**

- **Je retire ζ = 2**, pour deux raisons.
  - **Calibration** : ζ = σ/(ϱ̄_L + δ), pour K/Y ∝ (coût d'usage)^−σ (CES, calcul à la main). Avec ϱ̄_L + δ ≈ 6 % :
    - ζ = 2 suppose σ ≈ 0,12 ;
    - σ = 0,25 donne ζ ≈ 4,2.
  - σ = 0,12 est sous l'estimation basse de Chirinko, Fazzari et Meyer (environ −0,25 sur données de firmes). Statut de cette référence :
    - valeur relevée par moteur de recherche, document de travail Levy n° 175 (1996), publié dans *JPubE* 74(1), 1999 ;
    - texte non lu (accès bloqué par le proxy) ;
    - σ est **contestée**.
  - **Effet sur r̄** : à allocation donnée, r̄ ∝ 1/ζ (`r8.py`). ζ = 2 double l'écart de r̄ par rapport à ζ = 4.
- **Je me range à la proposition de `macro`**, avec deux précisions.
  - S-ζ est retenue à M28, et ζ est calibré au J3 sur σ (coût d'usage), pas sur l'effet de la dette sur le taux (§ 1 (a)).
    - Ordre de grandeur : 4 à 8, pour σ de 0,25 à 0,5 (hypothèse).
    - Au-delà, la borne Div ≥ 0 devient atteignable après une baisse de taux de quelques points (`macro`, (f) : −2,25 points à ζ = 17).
  - C37 est nécessaire mais ne suffit pas : S avec T9 garde une racine unitaire (`r7.py`, `r8.py`). Si ζ sort de la spécification, un autre canal de niveau doit le remplacer : ν(r), ou une fermeture budgétaire de U. T9 seul ne ferme pas le modèle.
- **Pour le joueur, le choix est neutre** : la demi-vie vaut 218 tours à ζ = 4 et 252 tours à ζ = 17 (`r10.py`).

**4. Précision prospective de C36**

- **(ii)** J'accepte l'horizon déclaré, mais je refuse l'alternative « seuil de 1e−3 à 7 200 tours ».
  - C'est un relâchement du seuil de 1e−6. Il ne sert qu'à ζ = 2 (écart de 1,6e−3 à 7 200 tours). À ζ ≥ 4, r̄ est atteint, à l'affichage, dès 7 200 tours (`r10.py`).
  - Dix demi-vies laissent environ 1e−3 du transitoire, ce qui est incompatible avec 1e−6.
  - **Contre-proposition :**
    - (ii-a) r̄ et π̄ sont calculés par résolution du point fixe dans chaque branche, à 1e−6 relatif ;
    - (ii-b) la trajectoire simulée après G +1 % permanent atteint ce point fixe (écart relatif inférieur à 1e−3) en au plus 20 demi-vies de la racine dominante.
- **(iii)** Un module inférieur à 1 au point fixe ne suffit pas : au moins quatre cas mesurés sont stables localement sans arrivée (`macro` : ζ = 4 et 6 sans T9 ; ici : Bohn ζ = 4, φ_B = 0,02 et ζ = 2, φ_B = 0,1).
  - **Proposition de lecture de « aucune rampe »** : module dominant inférieur à 1, hors racine nominale et hors état inerte déclaré, **et** (ii-b) satisfait.
- **L'ancien verdict ne change pas** : S-ζ (ζ = 2) avec T9 passe C36 dans son libellé initial ; S, et tout cas sans reprise budgétaire, échouent.

**5. Condition transmise à la fiche 9 (question 3)** : accord. Je l'écris comme suit.

- **C37 — Qui paie le surcroît d'intérêts publics (fiche 9, avec la fiche 8).**
  - **Exigence** : la règle budgétaire de référence (test zéro, pays non joués) reprend aux agents privés, à fréquence nulle, le surcroît d'intérêts sur B qu'entraîne une hausse durable du taux. Cette reprise doit assurer deux choses :
    - C36 (i) tient, tous canaux réunis ;
    - l'arrivée existe après G +1 % permanent (C36 (ii-b)).
  - **Mesuré** (maquettes, τ = 0,25) :
    - T9 suffit pour tous les ζ testés (2 à 17) ;
    - une réaction de Bohn avec φ_B ≤ 0,1 ne suffit pas toujours : à ζ = 2, il faut φ_B = 0,1 pour la seule stabilité locale, et même avec elle, l'arrivée manque dans deux cas sur quatre (§ 2) ;
    - une cible intégrale de B/PIB échoue.
  - C37 ne remplace pas un canal de niveau (ζ ou ν(r)), puisque S avec T9 garde une racine unitaire.
  - **Financement des intérêts par le déficit** : c'est un régime déclaré, une dominance budgétaire au sens de Leeper (1991), pas une référence. Le gain de la demande au taux y est positif, et la règle C2 y explose.
  - **Pays joué** : la fiche 9 et `jeu` décident si le joueur choisit de reprendre ou non ce surcroît.

**6. Désaccord résiduel (question 4)**

- **Portée de S-ζ** : aucun désaccord. Je me range à `macro` et retire ζ = 2.
- **Précision de C36** :
  - *`macro`* : (ii) se juge à au moins dix demi-vies, ou avec un seuil de 1e−3 à 7 200 tours ; (iii) se lit « module dominant inférieur à 1, hors racine nominale ».
  - *`monnaie`* : (ii) se juge par résolution du point fixe à 1e−6, plus une arrivée simulée à 1e−3 en au plus 20 demi-vies ; (iii) exige un module inférieur à 1 **et** une arrivée simulée, puisque la stabilité locale ne suffit pas (au moins quatre cas mesurés).

**Signalé à `jeu` (non tranché)** : si le joueur finance les intérêts par le déficit, un resserrement durable devient expansionniste à long terme, et la règle C2 diverge si le joueur la délègue. La question est de savoir si c'est lisible comme « dominance budgétaire » ou illisible, comme un paradoxe. À instruire avec la fiche 9.

## 7. Avis de `jeu`

*`jeu`, 03/10/2026 (issue #42, jalon 2), sur la fiche à l'état `0586a92` (branche `claude/j1-economie-reelle`, PR #43). Réponses aux quatre questions de `macro`.*

**Chiffres.** Aucun moteur n'existe encore. J'ai utilisé deux maquettes, exécutées le 03/10/2026 hors dépôt.

- **Équilibre partiel du bloc (PE)**, écrite par `jeu` à partir des seules équations du § 3.S (`pe.py`).
  - Hypothèses : ŷ et prix sur leur sentier, K^vol par N10, ti mis à jour sur tu.
  - Contrôle : dérive nulle sans choc sur 720 tours. I^vol/ŷ vaut 0,1396380 aux tours 1 et 720, soit le ti du § 3.E.
- **Boucle conjointe (EG)** : c'est la maquette `conj6.py` de `macro` (fiches 2 à 6, option S, F, x = 2, η_r = 2, λ_ti = 0,02, régime H). **Elle n'est pas indépendante.**
  - `jeu` y a ajouté trois choses (`m1.py` à `m5.py`) :
    - la transmission d'une hausse de taux aux intérêts versés (i_L·L) et reçus (i_D·D_F, i_D·V), sans toucher à l'état stationnaire ;
    - l'investissement en volume livré, I/p ;
    - la consommation en volume.
  - Contrôle : la maquette reproduit au troisième chiffre les deux tableaux du § 3.L, pour I en u.m., tu et les dividendes.
  - Hypothèses de la maquette EG :
    - pas d'impôts ;
    - G exogène ;
    - π^e exogène, sans règle de taux ;
    - les intérêts de la dette publique sont versés sans règle budgétaire ;
    - transmission complète : i_L et i_D montent d'autant.
  - Les chiffres de signe net (question 1, point 3) dépendent entièrement de ces hypothèses.

**Question ludique de la fiche.** Le bloc n'ouvre aucun levier propre. Trois leviers le traversent : le taux, la dépense publique et l'impôt sur les entreprises. Au socle, il porte aussi la seule trace de ce que le crédit coûte aux entreprises. Trois questions en découlent :
- le taux a-t-il, par l'investissement, un effet identifiable, durable dans une partie, et du bon signe une fois tous les canaux réunis ?
- les indicateurs du bloc bougent-ils quand il se passe quelque chose, et seulement dans ce cas ?
- le financement crée-t-il des gagnants et des perdants lisibles, ou une remise à zéro silencieuse ?

### 7.A, 7.B, 7.P et 7.R (brièvement)

- **A : à revoir.** Les échecs aux critères 6 et 7 (c) sont confirmés avec les stocks (rayons de 1,11 à 1,34). Le résultat est un cycle d'investissement explosif sans cause que le joueur ait donnée. Son indicateur q/q\* était lisible : l'idée d'un indicateur rapporté à sa norme est reprise pour S, sous la forme ϱ_L − ϱ̄_L.
- **B : à revoir.** Elle a les mêmes échecs, environ neuf bornes, et des coudes actifs à l'état stationnaire, c'est-à-dire des planchers invisibles.
- **PI : écartée, d'accord.** Elle est instable dès m = 0,6 dans la boucle réduite.
- **R : hors classement.** C'est une référence d'état stationnaire seulement (accélérateur plein, rayon 4,02).

### 7.S Option S — part d'investissement visée, avec la règle F

- **Récit en une phrase** : « les entreprises investissent une part stable de la production qu'elles attendent ; un point de taux réel du crédit au-dessus de sa norme en retranche 2 %, tant qu'il dure ». Une seule phrase, sans exception cachée.
- **Ce que voit le joueur** (EG, sauf mention contraire).
  - **Taux réel du crédit +1 point aux tours 1 à 12** (canal de l'investissement seul, expérience du § 3.L) :
    - investissement en volume : −1,98 % au tour 1, −2,17 % au tour 6, −2,07 % au tour 12, puis −0,08 % au tour 13 ;
    - production : −0,230 % au tour 4, −0,244 % au tour 6 ; écart cumulé des tours 1 à 12 : −0,157 %.
  - **Même hausse maintenue** :
    - investissement : −2,05 % au tour 24, −1,94 % au tour 120 ;
    - 94 % de l'effet du tour 12 subsiste au tour 120 ; en PE, 95,7 % à λ_ti = 0,02 et encore 79 % à λ_ti = 0,10 ;
    - l'effet « absorbé par ti à très long terme » (§ 3.Q, Q12) est donc invisible dans une partie : **le levier ne s'use pas**.
  - **Dépense publique +1 % aux tours 1 à 12** : l'investissement en volume monte au plus de +0,20 % (tours 6 à 9).
    - Le +0,647 % d'investissement du § 3.L au tour 14 est en u.m. : en volume, il vaut +0,120 %.
    - Plus des quatre cinquièmes du chiffre publié sont donc du prix (p +0,527 %).
  - **Dépense publique +5 % aux tours 1 à 12** :
    - investissement en volume : +1,01 % au tour 6, pour une production à +1,41 % ;
    - il reste au-dessus de +0,5 % pendant 11 tours, à partir du tour 4.
  - **Élasticité de l'investissement à la production : 1 par construction** (I^vol = ti·ŷ).
    - L'investissement est le miroir de la production, avec un tour de retard.
    - En volume, il est moins ample qu'elle dans les chocs mesurés (pic de +1,01 % contre +1,41 %).
    - Qu'il soit en fait plus volatil que le PIB est un fait stylisé à vérifier par `macro` (critère 16). Je ne demande pas d'accélérateur : R vaut 4,02.
- **Leviers.**
  - **Taux** : un canal direct et durable, avec un délai d'un tour. La contrepartie est visible le tour même (crédit nouveau −4,48 % au tour 1, § 3.L).
  - **Dépense publique** : aucun canal propre ; l'investissement suit la production.
  - **Impôt sur les entreprises** : F3 retranche T̂_F du dividende résiduel, et le plan de S ne lit aucun profit.
    - L'impôt tombe donc entièrement sur les dividendes, c'est-à-dire sur le revenu des ménages, jamais sur l'investissement.
    - C'est une lecture des équations F3 et du § 3.S, non mesurée : T_F = 0 dans la maquette.
- **Stratégies.**
  - Aucune remise à zéro gratuite du côté du capital : ti ne saute pas et K ne se réévalue pas.
  - **Sous-investir ne coûte rien à la production** (forme concrète de #37). Avec le taux à +1 point pendant 120 tours :
    - l'investissement est à −1,94 % ;
    - la production n'est qu'à −0,05 % au tour 120 (tu à 0,808) ;
    - une désinflation par le taux n'a donc aucun coût d'offre futur.

    D'accord pour laisser #37 ouverte jusqu'au J7.
  - **Asymétrie fiscale** : l'impôt sur les sociétés ne touche pas l'investissement, alors qu'un crédit d'impôt (Q12) multiplie le plan, de façon durable à l'échelle d'une partie, comme le taux. La combinaison « impôt élevé et crédit d'impôt » est à éprouver au J4 pour écarter une stratégie dominante (condition 10).
- **Risques.**
  - *Signe net du taux* (question 1, point 3) : le seul canal du bon signe est faible.
  - *Indicateurs morts* :
    - le taux d'utilisation (question 2) ;
    - le levier L/K, qui vaut 0,40000 à tous les tours du § 3.L.
  - *Dividendes au tour, très bruités* (§ 7.F).
  - *Le rationnement du crédit ne touche pas l'investissement sous J = 1.*
    - Cas à la main du § 3.F : les dividendes passent de 7,83 à 6,28 (−20 % au tour) et l'investissement est inchangé.
    - Pour le joueur, une crise du crédit se lit comme une baisse des dividendes.
    - Accepté au socle. À revoir avant les types de crise du J6 (O3), avec l'accélérateur financier placé dans l'offre du bloc 7 (`monnaie`).
  - *Pas de surendettement possible des entreprises.*
    - Sous F, L/K = lv\* à chaque pas où le plan est servi : un choc passe par les dividendes et les dépôts, jamais par une dette qui s'accumule.
    - Aucune crise de dette privée ne peut émerger au socle. Limite à déclarer, à rouvrir au J6 (issue 2 proposée).
- **Verdict : lisible**, sous les conditions 1 à 11.

### 7.C Option C — ajustement du capital avec terme de tendance

- **Avec un canal du taux : à revoir.** Une hausse durable d'un point déplace le taux d'utilisation d'arrivée : tu/t̄u vaut 1,4, puis 1,8 et 1,2 selon la vitesse (§ 3.C). Le niveau normal affiché serait faux, et un réglage de vitesse le déplacerait. C'est ce que j'ai refusé pour S à la fiche 5, quand les α étaient libres.
- **Sans canal du taux : à revoir.** Le taux n'atteint alors l'investissement que par la demande.
  - J'ai pris comme approximation S avec η_r = 0 : même absence d'effet direct, mais ce n'est pas C.
  - Avec transmission complète, une hausse d'un point **relève** la production (écart cumulé de +0,246 % sur les tours 1 à 12) et les prix (+0,664 % au tour 12).
  - Le principal levier monétaire aurait le signe inverse.
- **Accélérateur sur tu** : ∂I/∂ŷ = λ_K·x = 0,1, contre I/ŷ = 0,1396. L'élasticité vaut donc environ 0,72 (calcul à la main sur l'équation du § 3.C), moins que S. Aucun gain de lisibilité.

### 7.F Règle de financement F

- **Ordre de priorité des paiements** (salaires, puis intérêts et impôts, puis dividendes en dernier) : **lisible**. Le joueur voit qui absorbe un choc de trésorerie, et c'est l'actionnaire.
- **Variantes écartées** (levier sur p K^vol, cible de dépôts sur les ventes du pas) : d'accord. Explosives (1,05 et 1,49), elles seraient injouables.
- **Le dividende du tour est un résiduel de caisse, et il oscille.** Après une dépense publique de +5 % aux tours 1 à 12 :
  - +7,96 % au tour 1, −6,96 % au tour 7, +5,33 % au tour 12, −1,23 % au tour 13, +13,43 % au tour 18 ;
  - six changements de sens sur les tours 1 à 36, avec un extrême 6 tours après la fin du choc ;
  - la somme sur 12 tours est bien plus calme : +0,17 % au tour 12, −1,21 % au tour 14, +6,59 % au tour 24, +0,04 % au tour 36 ;
  - le revenu disponible des ménages reste lisse (de +0,56 % à +2,82 %, en hausse continue sur les tours 1 à 12).

  Le bruit ne se propage donc pas : c'est une question d'affichage.
- **La dépense publique se voit d'abord dans les dividendes** (+1,59 % au tour 1 pour G +1 %, avant toute hausse de production). Les entreprises encaissent la commande sur leurs stocks et distribuent l'excédent : « la relance profite d'abord aux actionnaires ». Les gagnants sont lisibles, si la restitution les montre (condition 5).
- **Verdict : lisible**, sous les conditions 4 à 6.

### Réponses aux quatre questions de `macro`

1. **Perceptibilité : oui pour le taux sur l'investissement, non pour la dépense publique de +1 %. Le signe net du taux n'est pas acquis.**
   - **Taux.** Le chiffre de −2 % est vérifié (−1,98 % au tour 1).
     - Il apparaît au tour où le taux du crédit publié change, donc au tour n + 1 de la décision si la banque reporte le taux directeur dans le tour (fiche 7).
     - Il est durable (point 7.S).
     - Sur la production, l'effet est faible : −0,230 % au tour 4 (vérifié), soit −0,2 point de glissement à une décimale.
   - **Dépense publique.** Le +0,65 % au tour 14 est en u.m. ; en volume, il vaut +0,12 %.
     - Pour G +1 %, l'investissement n'est pas un signal : il ne dépasse pas +0,20 %.
     - Pour G +5 %, il l'est : +1,01 %, et 11 tours au-dessus de +0,5 %.
   - **Point 3 : signe net d'une hausse d'un point** (transmission complète, tours 1 à 12). La fiche 6 n'en est pas seule maîtresse, mais elle en porte le seul terme du bon signe.

     | η_r | Production, écart cumulé tours 1 à 12 | Tours 1 à 36 | Prix, tour 12 | Prix, tour 36 |
     |---|---|---|---|---|
     | 0 | +0,246 % | +0,081 % | +0,664 % | +0,483 % |
     | 2 (proposé) | **+0,090 %** | +0,056 % | **+0,248 %** | +0,357 % |
     | 4 | −0,063 % | +0,032 % | −0,157 % | +0,234 % |
     | 6 | −0,212 % | +0,009 % | −0,551 % | +0,115 % |
     | 8 | −0,358 % | −0,014 % | −0,934 % | −0,002 % |

     - **Maintenue 120 tours à η_r = 2** : production +0,27 % et prix +4,25 % au tour 120.
     - **Par canal**, à η_r = 2 :
       - investissement seul : −0,157 % ;
       - avec les intérêts versés par les entreprises : −0,527 %, avec des dividendes en baisse de 9,5 % à 11,7 % ;
       - avec en plus les intérêts reçus par les ménages : +0,090 %.

       Le canal rentier de la fiche 5 l'emporte.
     - **Ce n'est pas un verdict sur S.** Le signe dépend de la fiche 7 (transmission à i_D), de la fiche 8 (règle de taux) et de la fiche 9 (qui paie les intérêts de la dette publique).
     - **Mais sous S avec η_r = 2, le canal de l'investissement ne garantit pas à lui seul le signe intuitif du principal levier monétaire.**
     - Je ne demande pas de relever η_r pour corriger le signe. Ce serait un **choix de conception**, dont `macro` et `monnaie` diraient le coût en fidélité.
     - Je demande la mesure avant l'ouverture du levier (condition 9, issue 1). C'est la condition 8 de la fiche 5, chiffrée ici.
   - **Seuil** : voir plus bas.

2. **Taux d'utilisation : ni chiffre avec niveau normal au tableau du tour, ni libellé « capacités tendues ». Hors du tableau du tour.**
   - **Mesures** (EG) :
     - Après un choc temporaire, tu revient en 24 tours (G +5 % : 0,8112 au tour 6, 0,7939 au tour 18, 0,7997 au tour 24).
     - Il ne s'écarte durablement qu'après un choc permanent :
       - G +5 % maintenu : 0,8048 au tour 24, 0,8035 au tour 120, 0,8006 au tour 480 ;
       - taux +1 point maintenu : 0,8077 au tour 120.
     - Les demi-vies de 240 à 900 tours (réserve 6) ne concernent donc que les chocs permanents. C'est une nuance, pas un désaccord.
   - **Conséquence sous S : tu agit sur ti, de façon imperceptible.**
     - Pour un écart de +0,0035 pendant 120 tours, ti monte de 0,07 % (calcul à la main sur l'équation du § 3.S : (λ_ti/n_a)·Δtu·120).
     - Sous M26, tu n'a aucun effet sur les prix.
   - **Variante T** (ψ_tu = 0,5) : avec Δtu ≈ 0,004 durable, la cible de marge monterait de 0,2 % en log, et U\* de 0,1 point (forme de la fiche 4 : +1,25 point pour Δtu = 0,05). Elle est imperceptible elle aussi et ajoute un paramètre : **je ne la recommande pas à M28**.
   - **Pourquoi pas « capacités tendues »** : le libellé promet une conséquence (goulot, inflation) qui n'existe pas au socle. Ce serait un piège de lecture.
   - **Condition 4 de la fiche 2, réglée ainsi** :
     - tu sort du tableau du tour ;
     - il reste publié dans les séries et dans la fiche détaillée de l'investissement, avec la mention : « capacité normale utilisée, sans plafond ni effet sur les prix au socle ; elle infléchit très lentement la part d'investissement (moins de 0,1 % en dix ans pour un écart d'un demi-point) » ;
     - il revient au tableau quand un canal d'offre (#37) lui donne un effet perceptible.
3. **Dividendes qui montent avec le taux : c'est un effet de l'expérience, à ne pas mettre en avant.**
   - **Le +3,2 % vient de l'isolement du canal de l'investissement.**
     - Si les entreprises paient aussi leur crédit plus cher, les dividendes baissent : −9,52 % au tour 1, −11,68 % au tour 2.
     - Avec transmission complète (les dépôts des entreprises rapportent aussi davantage) : −6,86 % au tour 1.
     - Le joueur qui relève le taux voit donc baisser les dividendes : c'est le signe intuitif.
   - **Le mécanisme subsiste et atténue la baisse** : la trésorerie libérée par l'investissement non fait est distribuée. Il se déclare dans la fiche du levier.
   - **Restitution** :
     - (i) dividendes et profits non distribués **sur 12 tours seulement**, avec le taux de distribution, jamais la valeur du tour au tableau de bord (bruit mesuré au § 7.F) ;
     - (ii) **emplois de la trésorerie des entreprises** au tour, en contributions additives (condition 5) ;
     - (iii) crédit refusé : « demande de crédit non satisfaite : x u.m. ; absorbée par les dividendes (y) et les dépôts (z) ; investissement non touché ».
4. **K/Y (ii) au joueur, (i) dans le bilan : lisible, à deux conditions.**
   - **(ii) au joueur, à clarifier sur la fenêtre.**
     - Dans la définition du test zéro : 1,997 an à 2 % et 1,984 à 10 %. C'est une grandeur physique.
     - Dans la définition de restitution (lecture (e) : stock de clôture / somme des 12 derniers PIB), le niveau normal vaut **2,040 ans à 2 % et 2,110 à 10 %**.
       - Le facteur est Γ·12/Σ_{u=0}^{11}Γ^{−u}, soit 1,0216 et 1,0638 (calcul `python3 -c`).
       - C'est un effet de fenêtre qui dépend de l'inflation, comme pour le ratio de richesse de la fiche 5.
       - Le niveau normal se publie dans la définition affichée, à l'inflation mesurée.
     - K/Y bouge lentement : après une dépense publique de +5 % permanente, K^vol/(n_a y) passe de 2,000 à 1,972 au tour 6, puis 1,991 au tour 120. C'est un indicateur structurel, à placer au panneau annuel et non au tableau du tour.
   - **(i) dans le bilan, avec une ligne de rapprochement** : « écart de valorisation, capital au coût historique », égale à −(1 − ρ̄_K) : −22,1 % à 2 %, −57,9 % à 10 %.
     - Sans elle, le joueur voit la valeur nette des entreprises V_F tomber de 1,19 à 0,76 an de PIB entre 2 % et 10 % d'inflation.
     - Il y lirait une perte qui n'existe pas physiquement.
   - **Levier.**
     - L/K comptable est constant (0,40000 à tous les tours ; 0,399341 seulement sous rationnement) : hors du tableau.
     - À sa place, « dette des entreprises en années de PIB », L/(12 × PIB) : 0,622 à 2 % et 0,334 à 10 % (test zéro, 0,4 × K/Y (i) du § 3.E), soit 0,635 et 0,356 dans la définition de restitution.
     - Cette dette bouge avec l'activité et l'inflation. Elle montre que l'inflation allège la dette des emprunteurs : des gagnants et des perdants lisibles (O2).

### Indicateurs du tour (critère 12 (a))

| Indicateur | Verdict | Motif ou point à clarifier |
|---|---|---|
| Investissement, **en volume** (glissement sur 12 tours) | **à clarifier** | En u.m., plus des quatre cinquièmes du mouvement après G +1 % sont du prix (+0,647 % contre +0,120 % au tour 14). Valeur nominale en second, avec la décomposition volume / prix |
| Taux d'investissement, ΣI/ΣPIB sur 12 tours | **lisible** | Niveau normal publié : 13,945 % à 2 %, 13,849 % à 10 % |
| Écart du taux réel du crédit à sa norme, ϱ_L − ϱ̄_L | **à ajouter** | C'est la variable que lit la règle, rapportée à sa norme comme q/q\*. Mention dans la définition : « −2 % d'investissement par point » |
| Crédit nouveau ; demande de crédit non satisfaite | **lisible** | La demande non satisfaite porte la mention « absorbée par les dividendes et les dépôts ; investissement non touché » |
| Dividendes, profits non distribués, taux de distribution | **à clarifier** | Sur 12 tours seulement ; au tour, bruit de −7 % à +13 % après G +5 % |
| Emplois de la trésorerie des entreprises (au tour) | **à ajouter** | Explique les mouvements des dividendes (condition 5) |
| Dette des entreprises en années de PIB | **à ajouter** | Remplace le levier ; niveau normal à l'inflation mesurée |
| Levier L/K | **hors du tableau** | Constant par construction |
| Taux d'utilisation | **hors du tableau du tour** | Conséquence déclarée mais imperceptible (question 2) |
| K/Y (ii) | **à clarifier** ; panneau annuel | Niveau normal dans la définition affichée (2,040 ans à 2 % sous la lecture (e)) |
| Part d'investissement visée ti | **hors du tableau** | Imperceptible dans une partie |

### Préférence motivée

- **Ma préférence va à S avec F**, comme celle de `macro`.
  - **Mes motifs propres** :
    - une règle en une phrase ;
    - un effet du taux sur l'investissement immédiat, chiffrable (−2 % par point) et durable dans une partie (94 % au tour 120) ;
    - aucun cycle explosif sans cause, puisqu'il n'y a pas d'accélérateur ;
    - des niveaux normaux exacts, qu'aucune vitesse ne déplace ;
    - I^vol ≥ 0 et Div ≥ 0 tenus par la forme, donc sans plancher invisible ;
    - une impulsion temporaire qui ne laisse pas de gain permanent : après G +1 %, la production culmine à +0,283 % au tour 6 et revient à +0,040 % au tour 14. La condition 10 de la fiche 5 est tenue dans cette boucle.
  - **Les motifs de `macro`**, que je ne juge pas : critères 3 à 7, 9 et 13.
- **Faiblesses ludiques**, toutes déclarables et aucune rédhibitoire au socle :
  - l'investissement n'est qu'un miroir de la production ;
  - deux indicateurs sont morts (tu, L/K) ;
  - le rationnement du crédit et l'impôt sur les sociétés ne touchent pas l'investissement ;
  - aucune crise de dette privée n'est possible ;
  - le signe net du taux n'est pas établi.
- **Classement** : S > C sans canal du taux > C avec canal du taux > PI > B > A. R est hors classement.
- **Lectures soumises au § 5** :
  - (a) **Fermeture.** Pas d'objection ludique au supermultiplicateur.
    - Une dépense publique durable a un effet de niveau qui se renforce lentement : +0,68 % au tour 24, +0,95 % au tour 480. C'est lisible : « l'investissement suit et amplifie lentement ».
    - Je refuse la fermeture kaleckienne par C avec canal du taux : la norme affichée dépendrait de la vitesse.
    - La fermeture wicksellienne révise M24 et n'est pas de mon ressort. Le point reste contesté.
  - (b) **Lecture (a) de Q7 : accord.** Les conditions de crédit sont publiées à l'ouverture : le joueur et les entreprises ont la même information. Le délai d'un tour respecte la grammaire commune.
  - (c) **Voie (i) : accord.** FU apparaît de toute façon dans le tableau de trésorerie (condition 5).
  - (d) **Levier sur K comptable : accord**, avec sa conséquence : le levier sort du tableau (condition 4).
  - (e) **Div ≥ 0 comme contrainte de domaine : accord.**
    - Elle est inactive dans mes scénarios adverses : G −5 % (dividendes / ventes au plus bas à 5,54 %) et G −25 % (2,59 %).
    - Si elle s'active, le tableau affiche « dividendes suspendus ».
  - (f) **Amendement du critère 6 : aucun enjeu ludique.** Accord sur le principe : la lenteur n'est pas un continuum.
- **Coût en fidélité** : je ne demande aucun écart à la littérature. L'investissement en volume, l'écart du taux à sa norme, la trésorerie, la dette en années de PIB et le retrait de tu et de L/K du tableau sont des choix de restitution. Relever η_r pour le signe net serait un choix de conception : je ne le demande pas.

### Conditions demandées au § 9

1. **Investissement restitué en volume** (glissement sur 12 tours), l'u.m. en second, avec la décomposition volume / prix.
2. **Écart du taux réel du crédit à sa norme**, ϱ_L − ϱ̄_L, en points, avec la mention « −2 % d'investissement par point, au tour où le taux du crédit change ».
3. **Taux d'utilisation hors du tableau du tour.**
   - Il reste publié dans les séries et la fiche détaillée, avec la mention de la question 2.
   - Pas de libellé qualitatif.
   - Variante T non retenue.
   - Retour au tableau avec un canal d'offre (#37).
4. **Levier L/K hors du tableau.**
   - À sa place, la dette des entreprises en années de PIB et la dette nette L − D_F.
   - Leurs niveaux normaux sont publiés dans la définition affichée, à l'inflation mesurée.
5. **Emplois de la trésorerie des entreprises** au tour, en contributions additives : ventes encaissées, salaires, intérêts nets, impôts, investissement non financé par le crédit, variation des dépôts, et dividendes (résiduel). Dividendes et profits non distribués sur 12 tours seulement.
6. **Crédit refusé** : « absorbé par les dividendes (y) et les dépôts (z) ; investissement non touché (J = 1) ».
7. **K/Y (ii)** au panneau annuel, avec son niveau normal dans la définition affichée (2,040 ans à 2 % sous la lecture (e)). Dans le bilan, K comptable avec la ligne « écart de valorisation, capital au coût historique » (−(1 − ρ̄_K)).
8. **Tableau levier → indicateur → délai → contrepartie** (critère 12 (c)), délai mécanique et délai perçu :

   | Levier | Indicateur | Délai | Contrepartie |
   |---|---|---|---|
   | Taux | Investissement | Tour où i_L change | Crédit nouveau, dividendes |
   | Dépense publique | Investissement | n + 2 en volume | Dividendes, dès le tour n |
   | Impôt sur les entreprises | Dividendes | Le tour même ; aucun effet sur l'investissement | Revenu des ménages |

   Pour le taux, les dividendes baissent sauf la part d'investissement non faite, qui est distribuée. Gagnants et perdants sont nommés.
9. **Signe net d'une hausse de taux** sur la production et les prix, à 12, 36 et 120 tours. Il est mesuré avec les fiches 5 à 9 avant l'ouverture du levier de taux au J4, avec des critères écrits avant l'essai (issue 1). C'est la condition 8 de la fiche 5, chiffrée ici.
10. **Catalogue J4 : asymétrie fiscale.** La combinaison « impôt sur les sociétés et crédit d'impôt sur l'investissement » est éprouvée contre une stratégie dominante : un scénario apparié par levier et un scénario combiné.
11. **Limites déclarées pour le J6** (O3) : le rationnement du crédit et le surendettement des entreprises ne touchent pas l'investissement au socle. Ils sont à rouvrir avec la fiche 7 (accélérateur financier dans l'offre) avant de définir les crises de crédit (issue 2).

### Seuil proposé au mainteneur (critère 12 (d))

- **Grandeur** : e_I(t) = I^vol_t / I^vol,réf_t − 1, en %, l'investissement en volume rapporté à la trajectoire de référence, même état et même graine.
- **(d1) Taux** : taux réel du crédit anticipé +1 point aux tours 1 à 12.
  - **Seuil** : **|e_I(t)| ≥ 1,0 % à chacun des tours 1 à 12**, en équilibre partiel du bloc, à la calibration proposée. Aux vitesses ×0,5 et ×2 sur η_r, les valeurs sont publiées.
  - **Mesuré** : −1,980 % (PE, η_r = 2), et −1,97 % à −2,17 % en EG.
  - **Contrainte de calibration** : η_r ≥ ln(1/0,99)/0,01 = 1,005.
  - **Motif** : en deçà, le canal de l'investissement disparaît derrière le canal rentier de la consommation (+0,66 % de C au tour 2 par point de i_D, fiche 5). Le joueur ne relie plus le taux à l'investissement.
  - **Borne haute** : je n'ai trouvé aucun argument ludique pour en fixer une, et je n'en propose pas.
- **(d2) Persistance (garde)** : même choc maintenu 120 tours.
  - **Seuil** : e_I(120)/e_I(12) ≥ 0,5, en PE.
  - **Mesuré** : 0,957 à λ_ti = 0,02 et 0,793 à λ_ti = 0,10. Le seuil ne contraint pas la calibration actuelle.
  - **Motif** : il empêche qu'une calibration du J3 rende le levier « usé » au cours d'une partie.
- **(d3) Dépense publique +5 % aux tours 1 à 12.**
  - **Seuil** : e_I ≥ +0,5 % pendant au moins 6 des tours 1 à 24, en boucle conjointe, au J4 (scénario O2).
  - **Mesuré** dans la maquette : 11 tours, à partir du tour 4, pic de +1,01 % au tour 6.
  - **G +1 %** : valeurs publiées sans être exigées (pic de +0,20 %). L'exiger demanderait un accélérateur, donc une instabilité connue (R vaut 4,02).
- **Transparence.**
  - Je propose ces seuils après avoir mesuré les réponses. Ils ne départagent pas les options : seule S a ses formes fermées sans vitesse avec un canal du taux.
  - Leur rôle est d'encadrer la calibration du J3 (η_r, λ_ti).
  - Vérification au J3 par appel direct de la fonction du bloc en équilibre partiel, sans le programme entier (`CLAUDE.md`, « Règles des tests »).

**Issues proposées par `jeu`** (création soumise au mainteneur ; corps dans le compte rendu de la session, PR #43) : « Signe net d'une hausse de taux sur la production et les prix : essai conjoint des fiches 5 à 9 avant l'ouverture du levier de taux (J4) » ; « J6 — crises de crédit et dette des entreprises : sous la règle F, le rationnement et le surendettement ne touchent pas l'investissement ».

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
| 03/10/2026 | Jalon 2, partie 2 : socle F, options S, C, R et PI, boucles avec N1 à N7 et boucle conjointe, état stationnaire conjoint, voies (i)/(ii) de #36 (sortie de `verifier_matrices.py` avant et sur copie), cas à la main, Q2, Q3, Q5, Q11, Q12, exemple daté ; § 4 et § 5 (recommandation S + F, lecture (a), voie (i), amendement prospectif du critère 6 proposé) | `macro` ; session principale |
| 03/10/2026 | Décisions du mainteneur : visa de l'amendement de notation sous (G) ; amendement prospectif du critère 6 (2 160 pas) ; lecture annuelle des taux de la v1.5 et T_K en dépendance déclarée | mainteneur ; session principale |
| 03/10/2026 | Contre-épreuve indépendante de la partie 2 (formes fermées du § 3.E, cas à la main, boucle réduite avec N1 à N7, boucle conjointe) : concordance au 4e chiffre ; précisions d'écriture (taux nominal des formes fermées, configuration du tableau des variantes de F, condition A avec v/y, Div/ventes, période) | session principale |
| 03/10/2026 | Avis de `jeu` (§ 7) : S + F lisible sous onze conditions ; C, A et B à revoir ; taux d'utilisation hors du tableau du tour, variante T non recommandée ; seuils (d1) à (d3) du critère 12 (d) proposés ; signe net d'une hausse de taux non établi (maquette de `macro` étendue, non indépendante) ; deux issues proposées | `jeu` ; session principale |
| 03/10/2026 | Avis de `monnaie` (§ 6) : favorable à S + F, lecture (a), i_L à l'ouverture, ϱ_L sur π\*, voie (i), aucune prime sur le levier au socle ; conditions C27 à C36 ; **désaccord avec `macro`** : S-ζ (canal permanent du taux par le niveau de tu visé) contre S seule. Statut « avis rendus » | `monnaie` ; session principale |
| 03/10/2026 | Additif de `macro` (§ 5) : S et S-ζ mesurées avec une règle à action intégrale dans la boucle conjointe (constat de `monnaie` confirmé sous reprise budgétaire des intérêts ; fait nouveau sans elle : gain statique positif, aucun ζ testé ne tient C36) ; § 3.L remesuré avec tous les canaux du taux (C34) et l'investissement en volume (signe des dividendes corrigé) ; réserve 6 nuancée | `macro` ; session principale |
| 03/10/2026 | Relance ciblée de `monnaie` (§ 6.6) : mesures de `macro` reproduites ; ζ = 2 retiré, ralliement à S-ζ avec ζ calibré au J3 ; C37 (fiche 9 : reprise du surcroît d'intérêts publics) ; fait nouveau : une règle de Bohn ou une cible intégrale de dette ne remplace pas la reprise ; désaccord résiduel sur la rédaction prospective de C36 seulement | `monnaie` ; session principale |
