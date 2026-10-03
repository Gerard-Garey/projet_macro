---
bloc: Prix
module: src/nations/blocs/prix.py
expert pilote: macro
experts consultés: monnaie (indexation des prix sur les anticipations, indice et glissement lus par la règle de taux : frontière inflation) ; jeu
statut: en instruction (critères validés le 03/10/2026)
décision: —
issue: #40
---

# Fiche comparative — Prix

> Fiche ouverte à partir du gabarit `0000-gabarit.md` (validé à l'usage, M20), sur le modèle de forme de la fiche 3 « travail et salaires ». Jalon 1 de l'issue #40 : § 1 et § 2 seuls ; les rubriques suivantes portent « non instruit » jusqu'au jalon 2. Décidée avec la fiche 3 « travail et salaires » (décision du mainteneur du 03/10/2026 : décisions par paires).

Une fiche comparative instruit **l'origine de l'approche** d'un bloc (`docs/exigences.md` § 2.3) : la spécification v1.5, le moteur v2.0, ou une approche nouvelle. Elle est **instruite par l'expert pilote**, commentée par `jeu` et par l'expert consulté que désigne `README.md`, et **décidée par le mainteneur** (décision M-n, reportée dans `docs/feuille-de-route.md`). Aucune approche n'entre dans le moteur ni dans la spécification sans cette décision. Les agents n'écrivent pas la fiche dans le dépôt : elle figure dans leur compte rendu et la session principale la commite. Un **bloc-cadre** (temps et comptabilité) n'est pas un module de `blocs/` : sa fiche instruit ce que le cadre **définit** (conventions, matrices, règles), non des flux proposés ; les adaptations que cela impose sont signalées rubrique par rubrique.

Règles de rigueur (`CLAUDE.md`, « Rigueur ») : un chiffre se remesure ou cite sa source ; une équation de la v1.5 n'a jamais été garantie exécutée ; un comportement de la v2.0 ne vaut que sous son profil (état D1, **non versé** : aucun fait ne peut y être remesuré) et avec ses défauts connus ; chaque fait de la première tentative porte son **statut** S+O, O, R, L, V ou V+O (`CONTEXT.md`, « Statut d'un fait » ; un fait V sur le prototype v2.0 reste un fait de la première tentative, non un résultat v3) ; chaque référence est une publication retrouvée. Citer `archive/v1.5/…` avec numéro d'équation et section, ou avec le **numéro de ligne du `.tex`** quand section ou équation ne sont pas identifiables sans compiler ; `archive/v2.0/…` avec fichier et ligne. **Principe de simplicité** (adopté par le mainteneur le 30/09/2026, fiche « temps et comptabilité » § 2 ; `CONTEXT.md`) : à exigences comptables égales, l'option la plus simple pour le joueur et pour le moteur est préférée ; toute complexité se justifie par une identité qu'elle rend vérifiable ou par un mécanisme perçu à l'échelle d'une partie ; une simplification ne supprime ni une contrepartie comptable visible d'un levier ni une grandeur restituée au tour ; les identités, les tolérances relatives, le déterminisme, les invariants de l'ADR 0002 et la concordance ne se simplifient pas.

## 1. Question posée

*Rédigé par `macro` (expert pilote), 03/10/2026, sur la spécification à l'état `17f5137` (branche `claude/j1-economie-reelle`, PR #43).*

Le bloc forme le prix du bien du socle (J = 1, M24). Il forme aussi l'indice des prix et son glissement annuel, que lisent la règle de salaire (fiche 3) et la règle de taux (fiche 8).

Il ne propose **aucune ligne de flux** :
- les acheteurs (blocs 5, 6 et 9) appliquent le prix aux volumes servis (lignes 1 à 3) ;
- le bloc 2 valorise la ligne 4 au coût moyen pondéré.

Avec le coût unitaire UC = W/pr écrit par le bloc 2 (fiche 2 § 3.N-4), le prix détermine la marge, donc le partage de la valeur ajoutée. Le bloc est le premier point de la frontière inflation avec la fiche 8 (`docs/blocs/README.md` § 3, rang 4) et il débloque les fiches 5 et 6.

Sous M22, un pas est un tour (n_a = 12, n_m = 1) : toute fenêtre exprimée en pas l'est aussi en tours. La fiche est décidée **avec la fiche 3** (M25 et M26, décision du mainteneur du 03/10/2026 : décisions par paires). Ses critères 3 (d) et 5 (e) répondent aux critères 3 (d) et 5 (d) de la fiche 3.

### 1.1 Contrats hérités

| Contrat | Source | Ce qu'il impose à la fiche 4 | Ce qui le rouvrirait |
|---|---|---|---|
| Calendrier, conversions, indice des prix | M22 ; ADR 0005, pts 4, 5, 15 et 16 ; `sec:cadre-calendrier` (l. 195 à 203) | Pas mensuel, n_a = 12. Conversion **linéaire unique** des taux, flux et vitesses, avec λ ≤ n_a. **L'indice des prix et son glissement sont révisés en phase 1** (`tab:phases`, l. 504). Le registre de 12 valeurs P_{t−1}, …, P_{t−12} est mis à jour en phase 9 (l. 512) ; sa valeur stationnaire est P_{t−u} = P_t (1 + π̄)^{−u/n_a}. Le glissement π_t = P_t/P_{t−n_a} − 1 est « mesuré, jamais converti » (l. 195). Neuf phases triangulaires | Décision M-m citant M22. Pour la phase de P_t : **issue sensible**, décision citant M22 et ADR (#24 ; ADR 0005, pt 16) |
| Prix du pas et ordre de la phase 5 | M24 ; fiche 2 § 9.4 ; `tab:phases` l. 508 | p_t est écrit en phase 5 par le **premier** bloc de la phase (« prix, puis production, puis ménages, investissement, État »). Il ne lit ni v_t ni rien de ce que la phase 5 écrit après lui. Il lit l'ouverture et les phases 1 à 4 | Décision citant M24, et M22 si `tab:phases` change |
| Coût unitaire | M24 (a) ; fiche 2 § 3.N-4 (N8) | UC = W/pr est défini par le bloc 2 et lu par le bloc 4. La fiche **fixe la phase, 2 ou 4, où le bloc 2 écrit UC**. Une autre base de coût du prix (coût normal, amortissement, coût retardé) est une variable du bloc 4, distincte de UC. Redéfinir UC (par exemple UC = WB/y) réviserait M24 | Décision citant M24 |
| Marge constante à l'état stationnaire | `sec:production-stationnaire` (l. 722, « marge constante, hypothèse du bloc prix ») ; fiche 2 § 3.N-4 | Les formes fermées de M24 (ρ̄_IN, ΔIN, IN/(p·IN^vol) = ρ̄_IN/(1 + μ)) supposent que p et UC croissent au même rythme, (1 + π̄)^{1/n_a} − 1 par pas | Décision citant M24 si la règle retenue ne le donne pas |
| Bien unique, indexation par j | M24 (d) ; fiche 2 § 9.8 | Aucun prix relatif au socle ; règle écrite indexée par j. Au J5 viennent le terme d'intrants Σ_k a_kj p_k (N8) et la triangularité des lectures entre prix d'un même pas : signalés, non résolus ici | Décision citant M24 |
| Terme de demande | Fiche 2 § 9.8 (constat transmis) ; `archive/faits_mesures_G_K.md` § 6, n° 14, et § 8, R3 | Sous J = 1, la règle de prix garde un terme de demande | Fait nouveau soumis au mainteneur (critère 5 (b)) |
| Amortissement dans le coût | Fiche 2 § 9.8 ; faits § 6, n° 10 et 11 | Sous J = 1 (p_K = p), un amortissement inclus dans le coût au prix courant est un **point fixe scalaire**. La ligne 8 vaut δK/n_a sur la valeur comptable (`nations_et_marches.tex` l. 676 ; ρ̄_K = 0,7791 à g = π̄ = 2 % et δ = 5 %) | — |
| Taux d'utilisation | M24 (e) ; condition 4 de `jeu` (fiche 2 § 9.5) ; #37 | tu = y/y^cap est un indicateur sans plafond, écrit en phase 4 par le bloc 2. La fiche 4 ou la fiche 6 dit ce qu'il déclenche ; sinon il sort de la restitution, au plus tard à la décision de la fiche 6 | Décision du mainteneur |
| Taux annuels et cibles | #24 ; M24 (f) | Lecture (i) : une cible est convertie en x/n_a. Lecture (ii) : une cible annuelle se compare au glissement mesuré. La croissance effective de la productivité est publiée (2,0184 % pour 2 %) | Décision du mainteneur (volet « prix » ici, volet « banque centrale » à la branche n° 4) |
| Bornes | #38, lecture (ii) ; `CONVENTIONS.md` § 2.4 ; `docs/exigences.md` § 2.7 | Une borne à seuil libre a un paramètre déclaré et un motif contre un mécanisme. Une contrainte de conservation ou de technique n'a pas de paramètre : elle est déclarée dans les `\limites`, avec son activité à l'état stationnaire et un test | Décision citant #38 |
| Anticipations | `docs/blocs/README.md` § 2 et § 3 | La fiche déclare la variable d'anticipation consommée, ou qu'elle n'en consomme aucune. La loi de formation relève de la fiche 8 | — |
| Fiche 3, décidée avec la fiche 4 | Fiche 3 § 2, critères validés le 03/10/2026 | W_t est écrit en phase 1 ; même trajectoire de référence (3 (a)) ; part salariale conjointe (3 (d)) ; boucle salaires – prix (5 (d)) ; lecture de l'anticipation en phase 1 (Q3) | M25 et M26, prises ensemble |
| Statut des faits | Décision P1 du 03/10/2026 ; `CONTEXT.md` | Statuts S+O, O, R, L, V ou V+O. Un fait V mesuré sur le prototype v2.0 reste un fait de la première tentative. L'état D1 n'est pas versé | — |

### 1.2 Ce que le bloc doit produire

Les symboles **ne sont pas fixés** : ils le seront à l'instruction, sous le critère 13. μ désigne déjà la marge dans la fiche 2 (§ 3.N-4) ; κ est pris (capital), P, p et π aussi.

| Grandeur | Définition | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| Prix du bien p_{j,t} | Prix de vente du pas, le même pour tous les acheteurs | u.m. par u.v. | — | le pas, phase 5 ; restitution : le tour |
| Indice des prix P_t | Indice lu par les blocs 3 et 8. Sous J = 1, c'est un prix du bien, p_t ou p_{t−1} (date à fixer, Q1). Restitution en base 100 au tour 1 | indice | prix du tour 1 (restitution) | phase 1 selon le contrat actuel, sinon la phase retenue (Q1) |
| Glissement annuel π_t | P_t/P_{t−n_a} − 1 | fraction par an | P_{t−n_a} | 12 pas (registre) ; restitution : le tour |
| Variation du prix sur le tour | p_t/p_{t−1} − 1 | fraction par tour | p_{t−1} | 1 tour |
| Marge | p/UC − 1. Si la base de coût du prix diffère de UC, on publie aussi la marge sur cette base | fraction | UC du pas, ou base de coût du pas | le pas ; restitution : le tour, et la moyenne sur 12 tours |
| Part salariale implicite | W/(p·pr) = UC/p. Sous J = 1, sans rétention ni intrants, elle vaut 1/(1 + marge) | fraction | p·pr du pas | le pas |
| Part salariale restituée | Somme des WB sur somme de la valeur ajoutée en u.m., la valeur ajoutée valant p·v + ΔIN (définition de la fiche 3 § 1.2) | fraction | valeur ajoutée sur 12 tours | 12 tours |
| Décomposition de l'inflation | Croissance en log du prix = croissance en log de UC + croissance en log de (1 + marge) | fraction par an | — | 12 tours |
| Base de coût du prix, si l'option en a une distincte de UC | Par exemple coût normal, ou coût complet avec amortissement | u.m. par u.v. | — | le pas, dans la phase déclarée |
| Variables d'état du bloc, si l'option en a | Par exemple marge d'ouverture, prix d'ouverture si la règle a un retard, coût normal | unité propre | — | ouverture du pas |

### 1.3 Ce qu'il lit

- **Ouverture** :
  - ses variables d'état ;
  - le registre P_{t−1}, …, P_{t−n_a}, s'il coïncide avec le prix retardé dont la règle a besoin ;
  - l'état du bloc 2 : IN^vol_t, v^e_t, K^vol_t, pr_t ;
  - la valeur comptable K, si la base de coût comprend un amortissement.
- **Phase 1** :
  - W_t (bloc 3) ;
  - la variable d'anticipation (bloc 8), si elle est consommée.

  `tab:phases` sépare aujourd'hui « travail, prix, banque centrale » par des virgules : aucune lecture mutuelle n'est déclarée. Tout ordre interne de la phase 1 se déclare avec les fiches 3 (Q3) et 8.
- **Phase 2** :
  - y* et N* (bloc 2) ;
  - les plans de demande en u.m. (blocs 5, 6 et 9) ;
  - UC, s'il est écrit en phase 2.
- **Phase 4** :
  - y, y^cap, tu et la production visée non réalisée (bloc 2) ;
  - N et WB (bloc 3) ;
  - UC, s'il est écrit en phase 4.
- **Phase 5** : rien ; le bloc est le premier de la phase.
- **Leviers du joueur** :
  - aucun levier propre au socle sans décision ;
  - transitent par le bloc la dépense publique, les impôts et le taux, par la demande ;
  - les prix administrés (v1.5, ϱ^p, `sec:systemes` l. 1614 ; mode planifié, J7) font l'objet de Q10.
- **Décisions qui le contraignent** : M7, M13, M22 (ADR 0005), M24 (ADR 0007), décision du 02/10/2026 sur #23 (indices c, j, k) et décision du 03/10/2026 sur #38.

### 1.4 Frontières

- **Production et stocks (fiche 2, décidée)** :
  - le bloc reçoit UC et rend p_t ;
  - la ligne 4 reste au bloc 2 ;
  - la marge est constante à l'état stationnaire.

  Critères 2, 3 (e), 5 (f) et 8.
- **Travail et salaires (fiche 3, décidée avec la fiche 4)** :
  - W_t est lu en phase 1, directement ou par UC ;
  - la part salariale stationnaire résulte conjointement des deux règles ;
  - la boucle salaires – prix se mesure sur les deux règles ;
  - π_t est lu par l'indexation éventuelle des salaires (critère 9 de la fiche 3).

  Critères 3 (d), 5 (e) et 9.
- **Banque centrale et anticipations (fiche 8, `monnaie`) : frontière inflation.**
  - Chez `macro` : la formation du prix, l'indexation des prix et la définition de l'indice.
  - Chez `monnaie` : l'anticipation, la crédibilité et la cible (volet « banque centrale » de #24).
  - π_t est lu par la règle de taux : la phase de P_t fixe le délai de cette lecture.

  Critères 2 (c) et (d), 3 (b), 9 ; avis de `monnaie` (§ 6).
- **Ménages (fiche 5)** :
  - les plans de demande sont en u.m. et le prix fixe le volume servi ;
  - la marge alimente les profits distribués.
- **Investissement (fiche 6)** :
  - la marge alimente les profits non distribués (#36) ;
  - tu et le canal d'offre relèvent de #37 ;
  - ρ̄_K ; amortissement en ligne 8.
- **État et dette (fiche 9)** : la dépense publique est en u.m. ; une fiscalité indirecte éventuelle ne relève pas du bloc 4.
- **`jeu`** : critères 8 (c) et 10 ; avis au § 7.

### 1.5 Ce que la fiche ne tranche pas, et questions ouvertes

**Hors du périmètre** :
- la loi de formation des anticipations, la crédibilité et la cible d'inflation (fiche 8) ;
- les prix relatifs, les intrants et les prix d'actifs (J5 à J6) ;
- le change ;
- les prix administrés et l'inflation réprimée (J7) ;
- la fiscalité indirecte (fiche 9) ;
- les valeurs numériques de l'état stationnaire et la calibration (J3) : la fiche vérifie qu'une forme fermée existe ;
- les bandes du test zéro : proposées ici, confirmées avec O1 avant l'essai (M19).

**Questions ouvertes à instruire** :
- **Q1 — Phase de P_t et relation au prix (#24).** Trois lectures sont instruites, chacune avec son empreinte sur l'état et le délai en tours entre un mouvement du prix et sa lecture par les blocs 3 et 8 :
  - (a) P_t arrêté en phase 1 sur le dernier prix connu, P_t ≡ p_{t−1}. Le registre garde 12 valeurs ; c'est conforme au contrat actuel ; l'indice a un tour de retard sur le prix.
  - (b) p_t fixé en phase 1, P_t ≡ p_t. Le contrat de M24 (p_t écrit en phase 5) et `tab:phases` sont révisés ; UC doit être disponible en phase 1, et aucune variable des phases 2 à 4 n'est lue.
  - (c) P_t arrêté en phase 5 ou 9, P_t ≡ p_t, et lu par la phase 1 du pas suivant. Il faut un registre de 13 valeurs ou un glissement porté comme variable d'état : décision citant M22 et ADR (ADR 0005, pt 16).
- **Q2 — Phase d'écriture de UC (2 ou 4)** par le bloc 2, avec son motif : quels blocs lisent UC avant la phase 5.
- **Q3 — Base de coût du prix.** Plusieurs bases sont possibles :
  - UC seul, la marge couvrant l'amortissement et la rémunération du capital ;
  - un coût normal ;
  - un coût complet avec amortissement, à la valeur comptable ou au prix courant ;
  - un coût retardé.

  Dans chaque cas, la fiche déclare son lien à UC et à la ligne 8.
- **Q4 — Terme de demande.** Plusieurs variables sont possibles :
  - le stock d'ouverture rapporté à sa cible ;
  - la production visée non réalisée ;
  - la demande non servie du tour précédent ;
  - tu.

  Pour chacune : phase, signe, forme, valeur stationnaire. À défaut, un fait nouveau (critère 5 (b)).
- **Q5 — Taux d'utilisation (#37)** : conséquence sur le prix, ou absence de conséquence justifiée et transmise à la fiche 6.
- **Q6 — Anticipation et indexation.** Variable consommée, ou aucune. Une indexation des prix s'ajoutant à celle des salaires risque un double comptage (v2.0, `model.py` l. 1120, commentaire).
- **Q7 — Lecture de #24 pour les taux annuels de la règle** (anticipation, croissance de la productivité dans un coût normal, cible éventuelle). La lecture retenue est la même qu'à la fiche 3 (Q4) et à la fiche 8.
- **Q8 — Variantes à instruire** :
  - **A** (v1.5) : `eq:price` (l. 754 à 760 : tâtonnement, indexation ϖπ^e, rappel μ_c vers c^u(1 + m_j), bornes) ; `eq:cpi` (l. 679).
  - **B** (v2.0) : branche `wsps2` de `model.py` :
    - indicateur z, l. 1072 ;
    - coût unitaire avec amortissement au prix de remplacement, l. 1076, lissé si `valuation_smoothing` > 0 (défaut 0, l. 208 ; valeur dans D1 non établie par la synthèse des faits) ;
    - `flex`, l. 1090 ;
    - marge et cible, l. 1100 et 1101 ;
    - `normal_average`, l. 1117 à 1119 ;
    - rappel `mu_fast` et R3, l. 1120 à 1122 ;
    - bornes, l. 1128.

    Coefficients effectifs du profil D1 (faits § 1.1) : `mu_fast` = 0,15 contre 0,25 par défaut (l. 135) ; R3 actif, avec `kappa_p` = 0,1 et `kappa_bar` = 0,05, contre inactif par défaut (l. 134). La branche active se vérifie avant toute citation.
  - **Au moins une approche nouvelle**, dont la piste « prix au coût normal majoré » (feuille de route § 5), confrontée à R3.
  - **Une variante sans retard** (prix égal à la base de coût majorée dans le pas), comme référence (`docs/exigences.md` § 2.7).
- **Q9 — Ancrage du partage** : qui ancre la part salariale (marge du bloc 4, salaire réel du bloc 3, ou les deux). Question conjointe avec la Q6 de la fiche 3.
- **Q10 — Prix administrés** : instruits comme option, ou renvoyés au catalogue des leviers (J4) et au mode planifié (J7), avec leur interface notée.

## 2. Critères d'évaluation, écrits avant l'instruction

**Statut** : proposés par `macro` le 03/10/2026, **validés par le mainteneur le 03/10/2026** (jalon 1 de #40), avec les amendements ci-dessous. La liste est fermée : elle ne se déplace pas après observation (`docs/exigences.md` § 2.5). Un amendement adopté avant l'instruction se consigne sous le tableau.

Correspondance avec le gabarit :

| Critère du gabarit | Critère de la fiche |
|---|---|
| 1 | 1 |
| 2 | 3 et 4 |
| 3 | 5 |
| 4 | 12 |
| 5 | 10 |
| 6 | 7 et 11 |

Critères propres au bloc : 2, 6, 8, 9, 13, 14 et 15.

Sont des **exigences** (ils peuvent écarter une option) : 1, 2, 3, 4, 5 (a) à (d), 5 (e) pour la partie réelle sous anticipation exogène, 5 (f) pour la calibration proposée, 6, 7, 8 (a) et (b), 9 (a) et (c), 10 (b), 11 (sans historique ni drapeau), 12 (sans itération), 13 et 15.

Sont des **mesures** (elles décrivent sans écarter) : 5 (e) sous anticipation adaptative, 5 (f) aux vitesses ×0,5 et ×2, 8 (c), 9 (b), 10 (a), (c) et (d), 11 (décompte), 12 (décompte) et 14.

| N° | Critère | Ce qui est attendu (seuil ou forme du verdict) | Par quoi on le vérifie | Qui | Quand |
|---|---|---|---|---|---|
| 1 | Cohérence stock-flux (gabarit 1 ; `macro`) — **exigence** | (a) Le bloc ne propose **aucune ligne de flux**. Il écrit p_t ; les blocs 5, 6 et 9 l'appliquent aux volumes servis (lignes 1 à 3) et le bloc 2 l'emploie par cm pour la ligne 4. Aucune ligne et aucun poste ne sont ajoutés ; `tab:portes-monnaie` est inchangée. Une option qui exige une ligne (subvention, prélèvement sur la marge) la déclare avec sa phase et sa signature : c'est un contrat partagé, donc une décision citant M22. (b) Le prix ne crée ni ne détruit de valeur nette : il répartit la valeur entre acheteurs et entreprises (sous-colonne « courant »). (c) Un amortissement inclus dans la base de coût n'est pas la ligne 8 (δK/n_a, bloc 6) : la fiche dit sa valorisation et ne double aucun flux | Cas à la main sur un même pas, avec deux valeurs de p distantes de 1 % et des plans en u.m. donnés. On écrit les volumes servis, les lignes 1 à 4, le résultat courant des entreprises, et les valeurs nettes calculées par le stock et par les flux. Si une table change : `uv run python outils/verifier_matrices.py --strict <copie>`, sortie citée | `macro` | fiche ; J3 (identités, ε = 1e−12 × S, M22) |
| 2 | Contrats hérités, phases et lectures (tableau du § 1.1 ; ADR 0005 et 0007 ; #24 ; `macro`, `monnaie` pour (c) et (d)) — **exigence** | (a) p_t est écrit en phase 5, avant le bloc 2. Il ne lit que l'ouverture et les phases 1 à 4, ni v_t ni rien de ce que la phase 5 écrit ensuite. Un indicateur de demande en volume, d = plan/p, suppose p_t : il est écarté ou écrit en forme fermée, sans itération. (b) La phase d'écriture de UC (2 ou 4) est fixée et motivée. UC = W/pr reste celui de M24 ; une base de coût différente est une variable du bloc 4, déclarée. (c) **Phase de P_t** (Q1) : déclarée, avec la relation entre P_t et p, le nombre de variables du registre (12, ou 13, ou 12 plus une), sa valeur stationnaire explicite, et le délai en tours entiers entre un mouvement de p et sa lecture par les blocs 3 et 8. Une phase autre que la phase 1, ou p_t déplacé en phase 1, est une **issue sensible** : décision citant M22, M24 et ADR (ADR 0005, pt 16). (d) Si le bloc écrit en phase 1, l'ordre interne de la phase 1 est déclaré **avec les fiches 3 et 8**, pour report dans `tab:phases`. Il est triangulaire : un bloc prix qui lit W_t pendant que le bloc travail lit π_t dans la même phase forme un cycle, à écarter. (e) Sous la règle, p/UC est constant à l'état stationnaire (hypothèse de `sec:production-stationnaire`, l. 722) ; sinon la révision des formes fermées de M24 est déclarée. (f) La règle s'écrit indexée par j. La place d'un terme d'intrants (N8) est indiquée sans être résolue, et la triangularité entre prix d'un même pas est signalée pour le J5. (g) La matrice des lectures reste triangulaire | Tableau phase → lit / écrit par option, phase 1 comprise avec les blocs 3 et 8 ; triangularité vérifiée à la main | `macro` ; `monnaie` ((c), (d)) | fiche ; J2 (test de triangularité de l'ordonnanceur) |
| 3 | État stationnaire en forme fermée (gabarit 2 ; `macro`) — **exigence** | (a) **Trajectoire de référence**, celle du critère 3 (a) de la fiche 3 : volumes en croissance g, prix en hausse de (1 + π̄)^{1/n_a} − 1 par pas, π̄ étant le glissement annuel stationnaire. Sur cette trajectoire, chaque grandeur du bloc a sa valeur stationnaire en forme fermée, sans simulation : marge, p/UC, W/(p·pr), WB/VA sur 12 tours, variation du prix par pas, glissement, indicateur du terme de demande, base de coût. Chaque variable d'état a sa valeur stationnaire, d'où se déduit l'état initial résolu ; le registre vaut P_{t−u} = P_t (1 + π̄)^{−u/n_a}. **Cas à examiner** : WB/VA ≠ W/(p·pr), parce que ΔIN entre dans la valeur ajoutée. Illustration sous M24, p = (1 + μ)UC, μ = 0,25 (hypothèse), σ = 1,4 mois, g = 2 % : WB/VA = 0,798907 à π̄ = 2 % et 0,793448 à 10 %, soit −0,109 et −0,655 point par rapport à 1/(1 + μ) (commande au Retour). La fiche l'écrit pour chaque option. (b) **Glissement stationnaire (#24)**, calculé à la main. Sous (ii), π_t = π̄ et la hausse par pas vaut (1 + π̄)^{1/n_a} − 1, soit 0,16516 % pour 2 % à n_a = 12. Sous (i), une cible π* convertie en π*/n_a donne un glissement de (1 + π*/n_a)^{n_a} − 1 : 2,0151 %, 2,0184 % et 2,0197 % à n_a = 4, 12 et 52 pour 2 % ; 10,3813 %, 10,4713 % et 10,5065 % pour 10 %. La fiche déclare la lecture retenue pour chaque taux annuel de sa règle (Q7), la même que celle des fiches 3 et 8. (c) **Indépendance envers n_a** : la marge, la part salariale et le glissement n'en dépendent pas. Toute dépendance est écrite et chiffrée pour n_a = 4, 12 et 52, avec la condition qui la supprime. Elle peut venir d'une conversion, ou d'un coût retardé d'un pas : p_t/UC_t = (1 + μ)/(1 + π̄)^{1/n_a}. La dépendance de WB/VA par ρ̄_IN (inférieure à 0,0003 point dans l'illustration de (a)) est déclarée. (d) **Compatibilité avec la fiche 3**, réponse au critère 3 (d) de la fiche 3 : la fiche écrit la part salariale qu'implique sa règle, et la condition qu'elle impose à la règle de salaire ; elle dit lequel des blocs 3 et 4 ancre le partage (Q9) ; si les deux portent une cible (salaire réel visé et marge visée), le cas des prétentions incompatibles, où π̄ dépend de l'écart, est examiné et déclaré. Le rythme d'inflation serait alors fixé par les blocs 3 et 4, contre le critère 4 (c) de la fiche 3 ; le point est soumis au mainteneur. Source candidate : Rowthorn (1977), *Cambridge Journal of Economics* 1(3), 215-239, existence vérifiée, non lue. L'état stationnaire conjoint des blocs 3 et 4 est calculé en forme fermée quand les deux fiches sont « avis rendus », avant M25 et M26. (e) Le bloc ne fixe ni π̄ (fiche 8) ni t̄u (fiches 2 et 6) : il les lit | Calcul à la main dans la fiche. Au J3, script contre moteur : un pas sans choc depuis l'état initial résolu laisse chaque variable d'état du bloc sur sa trajectoire stationnaire à **1e−10 près en relatif** (seuil des fiches 2 et 3, reconduit) | `macro` ; `monnaie` ((b)) | fiche ; avant M25-M26 ; J3 |
| 4 | Aucune vitesse d'ajustement ne détermine l'état d'arrivée (`docs/exigences.md` § 2.7 ; `macro`) — **exigence** | (a) Aucune vitesse, ni la durée du pas, n'apparaît dans les formes fermées du critère 3. **Cas à examiner explicitement** : un ajustement partiel du prix vers une cible de coût majoré qui croît de (1 + π̄)^{1/n_a} − 1 par pas laisse un écart stationnaire fonction de λ_p/n_a et de π̄, sauf terme de tendance. C'est la même construction que `sec:production` (l. 617). Cas concernés : v1.5, rappel μ_c de `eq:price` ; v2.0, `mu_fast` (l. 1120 ; 0,15 par semaine dans D1) et la dynamique de la marge (l. 1100 : `kappa_mu_z`, `kappa_mu_s`, `lam_mu_n`), dont la valeur stationnaire n'égale `mu_n` que si z et l'écart de stocks s'annulent. Les vitesses hebdomadaires sont converties en base annuelle et confrontées à λ ≤ n_a. Si une dépendance subsiste, elle est écrite, chiffrée pour la vitesse divisée et multipliée par 2, avec la condition qui la supprime. (b) Le terme de demande est nul à l'état stationnaire, ou sa valeur y est explicite et indépendante des vitesses. Son indicateur prend la valeur stationnaire des formes fermées de M24. (c) **Aucun intégrateur sans ancre** : une marge qui intègre z ou l'écart de stocks sans rappel crée un continuum d'équilibres. La fiche le documente et le soumet. (d) La fiche dit quelle grandeur nominale le bloc ne détermine pas : le rythme d'inflation, ancré par la fiche 8, et le niveau des prix. La question est restée ouverte au terme de K (faits § 7) | Calcul à la main sur les formes fermées. Au J3, depuis l'état initial résolu : dépense publique +1 % pendant 12 tours, puis deux branches où toutes les vitesses du bloc sont multipliées par 0,5 et par 2 (dans λ ≤ n_a). L'écart relatif de chaque ratio du bloc entre les deux branches est au plus de **1e−6 après 720 pas** (seuil reconduit) | `macro` | fiche ; J3 |
| 5 | Stabilité (gabarit 3 ; `macro` ; (e) avec `monnaie`) — **exigence** pour (a) à (d), pour (e) dans sa partie réelle sous anticipation exogène et pour (f) à la calibration proposée ; **mesure** pour (e) sous anticipation adaptative et pour (f) aux vitesses ×0,5 et ×2 | (a) **Instabilités et hypothèses connues** (faits § 6 à 8), non réintroduites sans fait nouveau : n° 14, règle sans terme de demande (G1, branche « R3 désactivé », S+O : inflation moyenne 4,839 % contre 4,048 %, PIB final −13,803 %, chômage final 16,438 % ; dérive du prix de l'équipement en G1b, S+O ; production d'équipement nulle en semaine 736, R) ; n° 10, dépréciation au prix lissé, ×2,9 (R) ; n° 11, dépréciation indexée (R) ; n° 9, 12 et 13, liées aux prix (R) ; n° 15, un plafond produit un cycle (R) ; n° 16, tolérances absolues. Les hypothèses réfutées n° 1 et 2 (prix relatifs) sont dites sans objet sous J = 1 ; la n° 9 (R3 n'est pas un canal d'inflation) est rappelée, avec G-P (O : le prix suit le coût unitaire à 0,04 point par an près). Les acquis R3 et « les tâtonnements de prix… stabilisateurs cachés de la v1 » (R) sont discutés. (b) **Terme de demande sous J = 1** : la règle garde un terme de demande (constat de la fiche 2 § 9.8), avec sa variable, sa phase, son signe et sa valeur stationnaire (Q4) ; sinon la fiche établit, comme fait nouveau soumis au mainteneur, que le mécanisme de l'instabilité 14 n'existe pas sous M24. Ce mécanisme a été mesuré sur un modèle à quatre secteurs, avec une spirale du prix de l'équipement ; sa transposition à J = 1 n'est pas établie, et la fiche le dit. (c) **Amortissement dans le coût** : si la base de coût comprend un amortissement au prix courant, p = (1 + μ)[UC + δ p K^vol/(n_a y)] est un point fixe scalaire. Il est résolu en forme fermée, jamais par itération ; sa condition d'existence, (1 + μ) δ K^vol/(n_a y) < 1, est déclarée comme condition (pas comme écrêtage) et chiffrée à t̄u et au plus bas tu du scénario O2 ; ce qui se passe si elle est violée en trajectoire est dit ; la valorisation est déclarée (valeur comptable : pas de point fixe, dépendance à π̄ par ρ̄_K ; ou prix courant) ; un amortissement au prix lissé ou indexé (instabilités 10 et 11) n'est pas repris sans fait nouveau. (d) **Boucle propre du bloc** (prix, marge), coûts et demande exogènes, au pas mensuel : valeurs propres de module **strictement inférieur à 1** pour la calibration proposée et pour chaque vitesse ×0,5 et ×2, avec module, demi-vie en tours et période si les racines sont complexes. (e) **Boucle salaires – prix**, réponse au critère 5 (d) de la fiche 3 : récurrence linéarisée des règles des fiches 3 et 4 réunies, mesurée sur les ratios réels (W/(p·pr), marge, taux de chômage) et sur le rythme d'inflation. Sous π^e = π̄ exogène, rayon spectral de la partie réelle < 1 (exigence) ; une racine unitaire du niveau des prix est attendue et déclarée, le niveau n'étant pas ancré. Sous une anticipation adaptative **hypothétique**, π^e_{t+1} = π^e_t + (λ_e/n_a)(π_t − π^e_t) avec λ_e ∈ {0,5 ; 1 ; 2} par an (ce n'est pas un choix de la fiche 8) : mesure publiée, avis de `monnaie`. Mesurée quand les deux fiches sont « avis rendus », avant M25 et M26. (f) **Boucle prix – stocks – demande**, si le terme de demande lit les stocks ou la production : système N1 à N7 de la fiche 2, avec la règle de prix, des plans de demande en u.m. et une demande induite d = A + m·y_{t−1}, pour m = 0,5, 0,6, 0,7 et 0,8 (hypothèse ; m effectif fourni par les fiches 5 et 9 au J3). Rayon spectral < 1 à la calibration proposée ; aux vitesses ×0,5 et ×2, module, demi-vie et période sont publiés | Faits § 6 à 8, puis `tab:instabilites`. Valeurs propres calculées à la main ou par `uv run python`, commande et sortie citées | `macro` ; `monnaie` ((e)) | fiche ; avant M25-M26 ; J3 |
| 6 | Test zéro des ratios du bloc (`docs/exigences.md` § 2.6 ; O1 ; `macro`) — **exigence**, mesurée au J3 | Sur 60 ans (720 pas) sans choc depuis l'état initial résolu, pour plusieurs graines : la moyenne par blocs de 5 ans (60 pas) de chaque ratio reste dans sa bande autour de la valeur stationnaire résolue. **Bandes proposées**, à confirmer par le mainteneur avec O1 avant l'essai (M19) : marge (p/UC − 1, fraction de UC, moyenne sur 12 tours) ±0,5 point ; part salariale (somme des WB sur somme de la valeur ajoutée, 12 tours) ±1 point, **bande commune avec la fiche 3**, une seule définition ; glissement annuel de l'indice (12 tours) ±0,2 point autour de π̄. Pour mémoire seulement, sans valeur de référence : D1 rapporte une inflation de 4,07 % contre un critère prospectif de 2 ± 1 point, et une dérive de la part salariale de 0,147 point (R, faits § 2). Toute dérive depuis l'état résolu est un défaut | Au stade de la fiche, seul le préalable (critère 3) se vérifie ; au J3, test zéro du socle | `macro` ; mainteneur (bandes) | J3 |
| 7 | Bornes (gabarit 6 ; #38, lecture (ii) ; `CONVENTIONS.md` § 2.4 ; `macro`) — **exigence** | (a) Chaque borne de chaque option est classée par le critère de tri de `CONVENTIONS.md` § 2.4. Les **bornes à seuil libre** sont déclarées avec leur paramètre, motivées contre un mécanisme, avec leur activité à l'état stationnaire (exemples : v2.0, `clip(1 + adj, 0,7, max_weekly_price = 1,19)` (l. 1128, l. 303), écart à la cible écrêté à ±0,5 (l. 1120), marge écrêtée à [0, 2] (l. 1100), R3 écrêté à ±`kappa_bar`·`flex` (l. 1122) ; v1.5, `eq:price`, bornes [0,7 ; 1,19], ±½ et ±κ̄f). Les **contraintes de conservation ou de technique** sont déclarées dans les `\limites`, sans paramètre, avec un test. (b) La positivité de p et de (1 + marge) découle du mécanisme (forme de la règle) plutôt que d'un plancher. Un plancher est une borne à seuil libre : un prix négatif ne contredit aucune identité. (c) **Instabilité 15** : aucune borne active à l'état stationnaire ni dans les scénarios O2 (dépense publique +1 % et +5 %). Si une borne s'active dans le scénario adverse, elle cesse de l'être **au plus tard 12 tours après la fin du choc** et ne se réactive pas sans nouveau choc (seuil de la fiche 3, critère 7 (c), reconduit). (d) La condition d'existence d'un point fixe (5 (c)) est une condition déclarée, comme λ ≤ n_a (`sec:cadre-calendrier`, l. 197), jamais une borne silencieuse | Décompte des bornes par option, avec classement. Cas à la main : le choc O2 à +5 % sur un tour, prix et marge. Au J3 ou au J4 : scénarios O2 | `macro` ; mainteneur (seuil de (c)) | fiche ; J3 ou J4 |
| 8 | Taux d'utilisation (#37 ; condition 4 de `jeu`, fiche 2 § 9.5 ; `macro`, `jeu`) — **exigence** pour (a) et (b), **mesure** pour (c) | (a) La fiche dit si le prix réagit à tu (fraction, dénominateur y^cap du pas, lu en phase 4) : forme, signe, valeur stationnaire. Une règle qui compare tu à un niveau normal prend pour ce niveau t̄u de l'état stationnaire résolu, et non un paramètre libre qui créerait un second ancrage. La fiche dit quel bloc fait tendre tu vers t̄u (fiche 6). (b) Sinon, l'absence de conséquence est justifiée (par exemple, un prix au coût normal insensible à l'utilisation ; source candidate : Coutts, Godley et Nordhaus (1978), *Industrial Pricing in the United Kingdom*, Cambridge University Press, existence vérifiée, non lu), et la condition 4 est transmise à la fiche 6, décision au plus tard à la sienne. (c) La fiche décrit ce que chaque voie donnerait au joueur, pour avis de `jeu` : un coût perceptible du sous-investissement sous forme d'inflation en capacité tendue, ou un indicateur à retirer de la restitution. Le canal d'offre reste à la fiche 6 | Forme fermée ; avis de `jeu` (§ 7) | `macro` ; `jeu` | fiche ; décision de la fiche 6 au plus tard |
| 9 | Frontière inflation (`docs/blocs/README.md` § 2 ; `macro` ; avis de `monnaie` au § 6) — **exigence** pour (a) et (c), **mesure** pour (b) | (a) **Variable d'anticipation consommée** déclarée : définition (glissement annuel anticipé de quel indice, sur quel horizon), unité (fraction par an), fenêtre, phase et ordre de lecture, valeur stationnaire requise (égale à π̄). Ou bien « aucune », avec son motif. Si la règle module sa vitesse par l'anticipation, c'est une consommation (v2.0, `flex` = 1 + 5·max(π^e, 0), l. 1090 et l. 303). La loi de formation et la crédibilité sont laissées à la fiche 8. (b) **Indexation des prix** : forme, coefficient, et risque de double comptage avec des coûts qui contiennent déjà les salaires indexés (v2.0, l. 1120, commentaire). Le terme ϖπ^e de la v1.5 (`eq:price`) est examiné sans être tenu pour un fait, avec sa conséquence stationnaire (critère 4 (a)). (c) **Indice produit** : définition de P_t sous J = 1, et place des pondérations à J ≥ 2 laissée ouverte (v1.5, `eq:cpi`, Laspeyres, l. 679). π_t est mesuré, jamais converti (l. 195). Phase et délai de lecture par les blocs 3 et 8 (critère 2 (c)). Lecture de #24 retenue, la même qu'aux fiches 3 et 8. (d) `monnaie` rend son avis sur (a) à (c) et sur le volet « prix » de #24 au § 6. Un désaccord est décrit en deux positions, et le mainteneur tranche | Formes fermées ; tableau de la variable consommée ; avis de `monnaie` | `macro` ; `monnaie` | fiche ; fiche 8 (loi de formation) |
| 10 | Lisibilité pour le joueur (gabarit 5 ; `macro`, à soumettre à `jeu`) — **exigence** pour (b), **mesure** pour (a), (c) et (d) | (a) **Indicateurs au tour**, chacun avec définition, unité, dénominateur et fenêtre : indice des prix (base 100 au tour 1) ; glissement annuel (12 tours) ; variation du prix sur le tour ; marge (p/UC − 1) ; part salariale (12 tours) ; décomposition de l'inflation entre coût unitaire et marge (12 tours) ; indicateur lu par le terme de demande. S'y ajoutent les niveaux normaux (marge, part salariale, π̄), publiés par le script d'état stationnaire, comme pour la condition 2 de `jeu` à la fiche 2. (b) **Délais en tours entiers** : salaire → prix (0 si p_t lit UC_t du même tour) ; demande → prix ; prix → indice lu par la règle de taux et par les salaires (0 ou 1 tour selon Q1). La contrepartie est visible le même tour (marge, stocks, ventes). Aucun effet plus rapide que le tour sans contrepartie. (c) Tableau levier → indicateur → délai → contrepartie pour la dépense publique, les impôts et le taux. Aucun levier propre sans décision (Q10) ; aucun drapeau de mode. (d) **Ampleur** : l'écart de glissement annuel produit par une dépense publique de +1 % et de +5 % pendant 12 tours est perceptible à l'échelle d'une partie (60 à 120 tours). **Seuil à proposer par `jeu` au mainteneur** (écart minimal en points). Signes non contre-intuitifs : un prix qui monte en récession par l'amortissement par unité est déclaré | Tableau du § 9, « Interfaces ». Exemple daté à la main, même choc que les fiches 2 et 3 (dépense publique +1 % aux tours 1 à 12, part de G 20 %, hypothèse) : prix, variation, glissement lu par la règle de taux, marge, part salariale et indicateur de demande aux tours 1, 2, 3, 4, 9, 13, 14, 18 et 24. Avis de `jeu` (§ 7) ; au J4, scénario apparié (O2) | `jeu` ; `macro` (exemple daté) | fiche ; J4 |
| 11 | Simplicité, empreinte sur l'état, déterminisme (gabarit 6 et rubrique 9 ; principe de simplicité ; `macro`) — **mesure** (décompte) et **exigence** (sans historique ni drapeau) | Décompte par option : paramètres, bornes, variables d'état, registres, lignes et phases touchées. Chaque élément est justifié par une identité vérifiable ou un mécanisme perçu. Chaque variable d'état a son unité et sa valeur stationnaire (critère 3). Un prix retardé est lu dans le registre s'il coïncide avec P_{t−1} ; sinon c'est une variable d'état déclarée, jamais un historique. Une seule règle par mécanisme : les sept modes de prix ou de coût de la v2.0 (`price_mode`, `pricing_cost_mode`, `price_basis`, `markup_live`, `markup_inv`, `equipment_price_mode`, `price_demand_feedback`) ne sont pas repris comme drapeaux (ADR 0002). Aucun tirage, ou un tirage par la graine du pays, déclaré | Tableau de décompte ; liste des variables d'état | `macro` | fiche ; J2 (reprise exacte) |
| 12 | Coût de calcul (gabarit 4 ; `macro`) — **exigence** (aucune itération) et **mesure** (décompte) | Aucune itération ni optimisation à chaque pas (ADR 0002) ; un point fixe est résolu en forme fermée. Décompte des opérations par pas. **Part indicative proposée : 0,48 ms par pays-pas**, celle adoptée pour les blocs 2 et 3 ((52/12 − 0,5)/8) | Décompte dans la fiche ; au J3, `tests/invariants/test_budget.py` | `macro` ; `audit` | fiche ; J3 |
| 13 | Notation (`CONVENTIONS.md` § 5.2 ; décision du 02/10/2026 sur #23 ; `macro`) — **exigence** | Chaque symbole a un seul sens et n'entre en collision ni avec les indices réservés (c, j, k, h, t ; s, ℓ, u du cadre) ni avec `tab:symboles`. En particulier : κ est pris (capital), donc les `kappa_p` et `kappa_bar` de R3 sont renommés ; m désigne la propension de la demande à la production (fiche 2 § 9.5) et la marge normale m_j de la v1.5 : à départager ; ϖ, employé dans plusieurs sens par la v1.5, est proscrit sans indice distinctif ; μ est employé pour la marge par la fiche 2 (§ 3.N-4) et absent de `tab:symboles` : à confirmer ; P, p, π, UC, cm et tu gardent leur sens. L'anticipation suit la convention de l'exposant e, son symbole étant fixé avec la fiche 8 | Liste des symboles confrontée à `tab:symboles` (commande `grep` et sortie citées) | `macro` ; `docwriter` (section) | fiche ; section proposée |
| 14 | Calibrabilité et faits établis (`macro`) — **mesure** | Les paramètres se calibrent sur des ordres de grandeur établis, chacun avec sa source retrouvée et sa date : marge ou part salariale, fréquence et vitesse d'ajustement des prix, réponse des prix à la demande. Les faits contestés sont séparés : la cyclicité de la marge en est un. Sources candidates, **non lues à ce jalon**, existence vérifiée : Nakamura et Steinsson (2008), *Quarterly Journal of Economics* 123(4), 1415-1464 ; Nekarda et Ramey (2020), *Journal of Money, Credit and Banking* 52(S2), 319-353 ; Coutts, Godley et Nordhaus (1978). Godley et Lavoie (2007), chap. 8 et 9 (prix au coût normal) est à retrouver. Un résultat de la v1.5 ou de la v2.0 n'est pas un fait établi ; une source introuvable est déclarée | Sources citées ; « non trouvée » le cas échéant | `macro` | fiche ; J3 (calibration) |
| 15 | Remesure des faits de la première tentative (décision P1 du 03/10/2026 ; `CONTEXT.md` ; `macro`) — **exigence** de procédure | (a) Chaque fait cité porte son statut (S+O, O, R, L, V, V+O). Les faits établis sur D1 (G1 et G1b, G-P, G-W) ne sont pas remesurables, D1 n'étant pas versé ; ils sont cités avec leur statut d'origine. (b) Toute remesure (statut V) passe par un script d'`outils/` qui exécute le prototype **dans un processus séparé, jamais par import** (invariant 4), revu par `audit` (circuit 3, `coder` → `audit`). Ses critères sont écrits dans la fiche **avant l'essai**, sur le modèle de la remesure S1 (fiche 2 § 9.7) : grandeur, définition, unité, fenêtre, seuil. Son verdict est publié même défavorable. Le statut V+O n'est donné que si le vérificateur réexécute le script. (c) Un fait V sur le prototype v2.0 reste un fait de la première tentative, jamais un résultat v3. (d) Les lectures de code (L) citent fichier et ligne, vérifiés à la date de la fiche, **avec la branche active et les coefficients effectifs du profil** (par exemple `mu_fast` = 0,15 dans D1 contre 0,25 par défaut ; `valuation_smoothing` dans D1 non établi) | Liste des faits et statuts ; commande, sortie et commit de chaque script | `macro` ; `coder` ; `audit` | fiche (jalon 2) |

### Amendements adoptés

Décisions du mainteneur du 03/10/2026, prises avant l'instruction, sur les questions de `macro` :

- **Critères** : les quinze critères sont validés tels quels, avec leur nature (exigence ou mesure).
- **Seuils reconduits des fiches 2 et 3**, adoptés : 1e−10 en relatif (critère 3) ; écart ≤ 1e−6 après 720 pas (critère 4) ; 0,48 ms par pays-pas (critère 12) ; désactivation d'une borne au plus tard 12 tours après la fin du choc (critère 7 (c)).
- **Bandes du test zéro** (critère 6), adoptées, à confirmer avec O1 avant l'essai (M19) : marge ±0,5 point ; glissement annuel ±0,2 point autour de π̄ ; part salariale ±1 point, bande commune avec la fiche 3, sur une seule définition.
- **Critère 5 (e)** : la stabilité de la boucle salaires – prix est une **exigence** pour la partie réelle sous anticipation exogène ; elle lie la paire des fiches 3 et 4 (le critère 5 (d) de la fiche 3 reste une mesure de son côté).
- **Part salariale de la condition de compatibilité** (critère 3 (d), ici et à la fiche 3) : la condition s'écrit sur W/(p·pr) ; l'écart avec WB/VA sur 12 tours est publié.
- **Q1 (#24)** : les trois lectures (a), (b) et (c) de la phase de P_t sont instruites ; une révision de contrat ne se décide qu'à M26 (décision citant M22, M24 et ADR).
- **Critère 5 (b)** : le terme de demande est gardé par défaut ; une démonstration en forme fermée que le mécanisme de l'instabilité 14 n'existe pas sous M24 peut être soumise au mainteneur comme fait nouveau.
- **Critère 8 (#37)** : au moins une variante où le prix réagit au taux d'utilisation est instruite ; la conclusion « aucune conséquence » reste possible.
- **Q7 (#24)** : une seule lecture des taux annuels pour les fiches 3, 4 et 8 ; le choix se fait à M25-M26, puis à la fiche 8.
- **Q10** : les prix administrés sont renvoyés au catalogue des leviers (J4) et au mode planifié (J7) ; la fiche en note l'interface.

## 3. Options

Non instruit (jalon 2 de l'issue #40, après validation des critères).

## 4. Tableau comparatif

Non instruit.

## 5. Avis de l'expert pilote

Non instruit.

## 6. Avis de l'expert consulté

Non instruit (`monnaie`, frontière inflation et volet « prix » de #24, au jalon 2).

## 7. Avis de `jeu`

Non instruit.

## 8. Décision du mainteneur

Non instruit (M26, décidée avec la fiche 3).

## 9. Conséquences de la décision

Non instruit.

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 03/10/2026 | Ouverture (issue #40) ; § 1 et § 2 proposés | `macro` ; session principale |
| 03/10/2026 | Critères validés avec amendements (seuils et bandes, critère 5 (e) en exigence, part salariale sur W/(p·pr), trois lectures de P_t, terme de demande, variante en tu, lecture unique de #24, Q10 ; issue #40) | mainteneur |
