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
| Valeur comptable du capital | `sec:cadre`, encadré de portée (l. 521) ; `sec:production-capital` (l. 676 à 680) ; visa du mainteneur du 03/10/2026 (fiche 2 § 3.N-5, amendement de notation) | K est un poste en valeur comptable, sans réévaluation ; il ne varie que par les lignes 3 et 8. ρ̄_K = K/(p K^vol) = (g + δ)/[n_a((1 + π̄)^{1/n_a}(1 + g/n_a) − 1) + δ], π̄ étant le glissement annuel stationnaire. ρ̄_K vaut 0,7791 à g = π̄ = 2 % et δ = 5 %, et 0,4221 à π̄ = 10 %. Une évaluation au prix courant demanderait une ligne de réévaluation. Une correction ad hoc de l'amortissement relèverait des instabilités 10 et 11 | Décision citant M22 (ligne de réévaluation) |
| Capacité normale et taux d'utilisation | M24 (e) ; `sec:production-stationnaire` (l. 728, 739) ; condition 4 de `jeu` (fiche 2 § 9.5) ; #37 | y^cap = K^vol/(n_a κ) est un indicateur sans plafond. t̄u = n_a κ y/K^vol est « fixé par le bloc investissement » ; l'état initial résolu prend K^vol_0 = n_a κ y_0/t̄u. La fiche dit ce que tu déclenche ; sinon tu sort de la restitution, au plus tard à la décision de la fiche. Un plafond de capacité réviserait M24 (e) | Décision citant M24 |
| Technique et croissance | M24 (f) ; `sec:production` (l. 592, 616, 741) | Technique de Leontief en travail : le capital ne contraint pas la production. pr suit une tendance exogène ; g = n_a[(1 + g_pr/n_a)(1 + g_N/n_a) − 1]. Un canal d'offre qui rend pr, g ou la production dépendants de l'accumulation révise M24 (e) ou (f) | Décision citant M24 |
| Sous-colonnes des entreprises (#36) | Décision du mainteneur du 02/10/2026 sur #36 (voie (i), PR #35) ; `sec:cadre-flux` (l. 292, 296 ; légende l. 304) ; fiche 2 § 3.N-10 et § 9.8 | **Voie (i)**, en vigueur : chaque colonne somme à zéro, les deux sous-colonnes réunies ; « prise seule, une sous-colonne des entreprises n'est pas nulle en général ». La sous-colonne courante vaut les profits non distribués FU, soit 0,33210 % de V_F par pas à l'état stationnaire (g = π̄ = 2 %). **Voie (ii)**, ligne « profits non distribués » : elle modifie `tab:matrice-flux`, contrat partagé (`docs/agents/routage.md` § 4.2). La clause de la l. 292 et la légende sont alors à reprendre, et la sortie de `verifier_matrices.py --strict` change | Décision citant M22 et ADR |
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
| Profits non distribués FU | Somme de la sous-colonne « courant » (fiche 2 § 3.N-10). C'est le résultat courant après distribution : ventes − cm·v − (WB − UC·y) − T_F − δK/n_a − intérêts nets − Div_F | u.m. par pas ; fraction par pas | V_F d'ouverture | le pas, phase 6 ; valeur stationnaire : 0,33210 % de V_F par pas |
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

## 3. Options

Non instruit (jalon 2 de l'issue #42, après validation des critères et quand les fiches 4 et 5 sont « avis rendus »).

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
