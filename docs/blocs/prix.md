---
bloc: Prix
module: src/nations/blocs/prix.py
expert pilote: macro
experts consultés: monnaie (indexation des prix sur les anticipations, indice et glissement lus par la règle de taux : frontière inflation) ; jeu
statut: décidée (M26, 03/10/2026)
décision: M26 (03/10/2026)
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

*Rédigé par `macro` (expert pilote), 03/10/2026, sur la fiche à l'état `981046b` (critères validés le 03/10/2026, avec leurs amendements) et la fiche 3 au même état (statut « avis rendus »). Branche `claude/j1-economie-reelle`, PR #43.*

### 3.0 Conventions de l'instruction

**Découpage par question** (gabarit, § 3). Les options nouvelles partagent un socle commun (§ 3.N : phase de P_t, phase de UC, base de coût, terme de demande, anticipation, lecture des taux, phases, état stationnaire conjoint, boucles, bornes). Elles ne diffèrent que par la règle de marge. Les options A et B sont instruites en entier.

**Notation provisoire** (critère 13), fixée à la décision :
- μ̄ : marge normale ;
- μ_t = p_t/UC_t − 1 : marge effective ;
- μ̃_t = ln(1 + μ_t) : marge en logarithme ;
- ξ_t = (IN^vol*_t − IN^vol_t)/IN^vol*_t : écart relatif du stock d'ouverture à sa cible, avec IN^vol*_t = n_a σ v^e_t ;
- ψ_ξ, ψ_tu : sensibilités de la marge visée au stock et au taux d'utilisation ;
- λ_μ, λ_p : vitesses annuelles de la marge et du prix ;
- π^e : anticipation, symbole fixé avec la fiche 8.

Contrôle par `grep -c -F` sur `nations_et_marches.tex` : 0 occurrence pour `\xi`, `\psi`, `\theta`, `\lambda_p`, `\lambda_e`, `\pi^e` et `\omega` ; `\mu` compte 5 occurrences, toutes dans des `\multicolumn`. Il n'y a donc aucune collision. `\Pi` est pris (7 occurrences, Π^CB) et n'est pas employé ici. φ est laissé à la fiche 3 (pente de Phillips, règle SP).

**Hypothèses de calcul** (ce ne sont pas des calibrations) :
- μ̄ = 0,25 ; g = 2 % ; π̄ = 2 % et 10 % ; σ = 1,4 mois ;
- fiche 2 : λ_v = 3 et λ_IN = 1,5 par an ;
- fiche 3, règle SN : λ_w = 1, β = 2, U^eq = 5 %, lecture (w1) ;
- ψ_ξ = ψ_tu = 0,5 ; λ_μ = λ_p = 1,2 par an ; t̄u = 0,8 ;
- propension m de 0,5 à 0,8 ;
- plans de demande en u.m. fixés en phase 2 au prix p_{t−1}(1 + π^e)^{1/n_a}.

**Lecture des taux annuels** : la fiche est instruite sous (G), et ce qui change sous (L) est indiqué à chaque fois (§ 3.N-6).

**Calculs** (03/10/2026). Commande : `uv run --no-project [--with numpy] python <script>` dans le scratchpad, sortie citée au Retour.

| N° | Script | Objet |
|---|---|---|
| P1 | `p4_s1_partVA.py` | W/(p·pr) contre WB/VA sur 12 tours : forme fermée, et simulation de la comptabilité M24 depuis un état décalé |
| P2 | `p4_s2_stat.py` | états stationnaires de A et de B transposées, de D, du coût complet et de la marge sur cm ; contre-épreuve par récurrence simulée |
| P3 | `p4_s3_modele.py`, `p4_s3_valid.py` | maquette détendue (N1 à N7, emploi R, règle SN, règle de prix, plans en u.m.) et validation contre la fiche 2 |
| P4 | `p4_s4_reduit.py` | système réel réduit, écrit séparément (contre-épreuve) |
| P5 à P8 | `p4_s5_tables.py`, `p4_s6_frontiere.py`, `p4_s7_M.py`, `p4_s8_tables2.py` | boucles 5 (e) et 5 (f) ; frontière de stabilité de C ; option M |
| P9, P10 | `p4_s9_adapt.py`, `p4_s10_adapt_reduit.py` | anticipation adaptative hypothétique : modèle complet, puis formulation en taux de croissance |
| P11 | `p4_s11_exemple.py` | exemple daté |
| P12 | `p4_s12_impulsion.py`, `p4_s12b.py` | impulsions non linéaires ; boucles propres de A et de B |
| P13 | `p4_s13_cout.py` | coût |
| P14 | `p4_s14_ampleur.py` | ampleurs pour `jeu` |
| P15 | `p4_s15_cas_main.py` | cas à la main du critère 1 |

**Validations et contre-épreuves** :
- P3, prix et salaires figés, reproduit exactement la fiche 2 :
  - rayon 0,9459 et période 73,0 tours à g = 0 et m = 0,6 ;
  - 0,9452 et 72,9 tours à g = 2 % ;
  - 0,9681 et 146,9 tours aux vitesses × 0,5 ; 0,9209 et 37,6 tours à × 2 ;
  - l'exemple daté de la fiche 2 : +0,084 / +0,142 / +0,183 / +0,246 / +0,239 / +0,153 / −0,003 / −0,030 %.
- P4, système réduit, contre P8, système complet : rayons identiques à 5,1e−9 près.
- P10 contre P9 (fermeture ancrée) : identiques au 4e chiffre.
- Impulsions non linéaires (P12) : facteur d'amortissement de l'enveloppe 0,9619 contre 0,9618 pour la valeur propre (M, coûts exogènes), 0,9069 contre 0,9068, 0,9287 contre 0,9286. En régime linéaire (ε = 1e−9), les cas explosifs donnent 1,2729 et 1,1295, égaux aux valeurs propres.
- P1 reproduit les −0,109 et −0,655 point de la fiche 3 (C13).

**Corrections apportées en cours de calcul** (déclarées, sans effet sur les verdicts publiés) :
1. P1 et P2 avaient deux erreurs d'affichage : ρ_IN simulé rapporté à un mauvais UC, et τ affiché pour la variante × 2.
2. Dans P3, pour m > 0, le choc multipliait la demande autonome A au lieu de s'ajouter à la demande. C'est corrigé avant P14. L'exemple daté (m = 0) et les jacobiens (calculés sans choc) ne sont pas touchés.
3. Sous la fermeture neutre, la racine unitaire double (niveau et rythme) est mal conditionnée en niveaux. P9 est remplacé par P10, en taux de croissance, où la racine du rythme est simple.

**Intégrité des sources** : `sha256sum` de `model.py` (e1505b7e…) et de `Nations_et_Marches_v1_5.tex` (097d023f…) identiques à `tests/invariants/archive_sha256.txt`. Les lignes citées ont été vérifiées le 03/10/2026.

**Littérature cherchée** : la lecture directe est refusée par le proxy, donc rien n'a été lu en source primaire.

| Source | Ce qui est établi | Statut |
|---|---|---|
| Godley et Lavoie (2007) | ch. 8 « Time, Inventories, Profits and Pricing » (p. 250-283) ; ch. 9 « A Model with Private Bank Money, Inventories and Inflation » | titres vérifiés par extrait ; la forme NHUC = (1 − σ)UC + (1 + r)σUC_{−1} est citée de mémoire, non vérifiée |
| Coutts, Godley et Nordhaus (1978), CUP, DAE monograph 26 | existence | définition du « coût normal » citée de mémoire |
| Nakamura et Steinsson (2008), *QJE* 123(4), 1415-1464 | fréquence médiane des changements de prix hors soldes de 9 à 12 % par mois ; la fréquence des hausses covarie avec l'inflation | extrait de recherche |
| Nekarda et Ramey (2020), *JMCB* 52(S2), 319-353 | la marge monte après un choc de demande positif ; sa cyclicité inconditionnelle dépend de la mesure | extrait |
| Blinder, Canetti, Lebow et Rudd (1998), Russell Sage | prix typiquement révisés environ une fois par an ; 71 % des firmes jugent qu'une hausse après une hausse de coût est tolérée par les clients, 64 % qu'une hausse après une hausse de demande ne l'est pas | extrait |
| Rowthorn (1977), *CJE* 1(3), 215-239 | existence ; vue « conflictuelle » de l'inflation | extrait |

**La littérature ne permet pas de conclure** sur la vitesse de la marge ni sur la sensibilité de la marge à la demande. La cyclicité de la marge est un **fait contesté**.

### 3.A Option A — v1.5

1. **Source** : `archive/v1.5/Nations_et_Marches_v1_5.tex`.
   - `eq:price` (l. 754 à 760) et `eq:cpi` (l. 679) ;
   - table de calibration : l. 2258 (κ_j = 0,10, κ̄ = 0,05 par semaine), l. 2259 (ϖ = 0,5 par tick sur π^e/52), l. 2314 (μ_c = 0,05 par semaine, m_j) ;
   - ρ_E = 2 % (l. 575) ;
   - λ_S : **sans valeur** (l. 2376, « fixé en dur ») ;
   - terme monétaire `eq:monterm` (l. 1419), hors socle.

   **Équations jamais garanties exécutées.**

2. **Équations**, transposées au pas mensuel sous M24 :
   - p_t = p_{t−1}·clip(1 + τ + [1 + z]^+ ϖ π^e/n_a + (μ_c/n_a)·clip(UC_t(1 + m)/p_{t−1} − 1, ±½), bornes [0,7 ; 1,19] par semaine) ;
   - τ = clip((κ/n_a) f z, ±(κ̄/n_a) f), avec f = 1 + 5[π^e]^+ ;
   - m = (r* + ρ_E) p K^vol/(UC·y).

   En base annuelle linéaire : μ_c = 2,6, κ = 5,2, κ̄ = 2,6 par an ; ϖ = 0,5 est un degré annuel d'indexation.

   **Choix de transposition déclarés** :
   - z est celui du pas précédent (variable d'état), puisque d_t = plan/p_t supposerait p_t (critère 2 (a)) ;
   - UC est celui du pas ;
   - S = y + λ_S IN^vol.

   Statut : choix de conception (tâtonnement), approchée (indexation).

3. **État stationnaire** (P2) :
   - sous M24 en croissance, z̄ = (1 − S/v)/(1 + S/v) ≠ 0 ;
   - avec λ_S = 0 : z̄ = −0,001165, τ̄ = −0,667 % par an et écart de rappel x = +0,00634 (π̄ = 2 %) ;
   - p/[UC(1 + m)] = 0,987854, 0,995336 et 0,999120 aux vitesses × 0,5, × 1 et × 2 (π̄ = 2 %) ; 0,952811, 0,987154 et 1,005271 à π̄ = 10 %. L'écart relatif entre × 0,5 et × 2 vaut 1,14e−2 : **la vitesse détermine l'état d'arrivée (échec du critère 4)** ;
   - avec λ_S = 0,5 (valeur de la v2.0 hors `wsps2`, l. 947) : z̄ = −0,2599. Il faudrait x = 0,577 (2 %) ou 0,802 (10 %), au-delà du rappel écrêté à ½ : **aucun état stationnaire**, et le prix simulé tend vers 0 relativement au coût ;
   - la marge normale m est un point fixe sous J = 1, m = a/(1 − a) avec a = (r* + ρ_E)k : 0,1364 pour r* = 2 % et k = 3 ans. La marge dépend de r*, une variable du bloc 8.

4. **Comportement** : non mesuré. Les affirmations de la l. 767 (« ce que le prototype a montré ») sont rapportées par la v1.5 et invérifiables.

5. **Coût** : quelques opérations, sans itération (non mesuré).

6. **Défauts** :
   - critère 4 (ci-dessus) ;
   - la valeur stationnaire dépend de λ_S, qui n'a pas de valeur ;
   - cinq bornes à seuil libre (critère 7) : [0,7 ; 1,19], ±κ̄f, ±½, [1 + z]^+ et [π^e]^+ ;
   - double consommation de π^e (indexation et f) ;
   - aucune instabilité connue réintroduite telle quelle, mais le tâtonnement de prix est l'un des « stabilisateurs cachés de la v1 » (acquis R).

7. **Identités** : aucune ligne de flux ; les lignes 1 à 4 sont inchangées.

8. **Ce que percevrait le joueur** : un prix qui dérive autour du coût selon des vitesses illisibles ; un indicateur z qui n'est pas nul en régime normal.

9. **Empreinte** : p_{t−1} et z_{t−1}, soit 2 variables d'état ; environ 9 paramètres (κ, κ̄, ϖ, μ_c, le coefficient 5 de f, les deux bornes, λ_S, ρ_E).

### 3.B Option B — v2.0

1. **Source** : `archive/v2.0/prototype/model.py`, branche `wsps2`. Statut L, branche active vérifiée :
   - `wsps2 = True` (l. 129) ; `price_mode = 'markup'` (l. 145, et dans D1) ; `pricing_cost_mode = 'legacy'` (l. 74, et dans D1), donc l. 1111 à 1119 **inactives** ; `price_basis = 'average'` (l. 128), donc l. 1077 inactive ;
   - z (l. 1072), avec un seuil de 1e−3·Q̄ ;
   - cu = (wages + intrants + δ/52·p_K^repl·K)/Y (l. 1076), `_pK_repl` par `getattr` (l. 1075 : **état caché**) ;
   - `flex` = 1 + 5·max(π^e, 0) (l. 1090) ;
   - marge (l. 1100) et cible (l. 1101) ; rappel `mu_fast` (l. 1120) ; R3 (l. 1121 et 1122) ; bornes (l. 1128) ;
   - `normal_average` : `workplan.py` l. 28 à 43 (coûts engagés, amortissement compris, répartis sur max(Y, 0,8·capacité)).
   - Coefficients effectifs du profil D1 (faits § 1.1) : `mu_fast` = 0,15 et R3 actif (κ_p = 0,10, κ̄ = 0,05). Valeurs non établies dans D1 : `markup_inv` et `markup_live` (défaut inactif), `valuation_smoothing` (défaut 0), `equipment_supply_response` (sans objet sous J = 1).

2. **Équations**, transposées mensuellement (taux hebdomadaires × 52/12) :
   - μ_t = clip(μ_{t−1}[1 + flex(κ_μz z + κ_μs·écart de stocks)/n_a] + (λ_μn/n_a)(μ_n − μ_{t−1}), 0, 2), avec κ_μz = 2,6, κ_μs = 0,52 et λ_μn = 0,26 par an ;
   - p_t = p_{t−1}·clip(1 + (μ_fast/n_a)·clip((1 + μ_t)cu_t/p_{t−1} − 1, ±½) + clip((κ_p/n_a)·flex·z, ±κ̄·flex/n_a)) ;
   - cu_t = UC_t + (δ/n_a)·p_{t−1}·K^vol/y (amortissement au prix courant, p_K = p).

3. **État stationnaire** (P2 ; μ_n = 0,25, δ = 5 %, K^vol/(n_a y) = 3 ans) :
   - sous M24, z̄ = (1 − y/v)/(1 + y/v) = −0,001165 et l'écart de stocks est nul ;
   - μ̄/μ_n = λ_μn/(λ_μn − flex·κ_μz·z̄) = 0,987344 (π̄ = 2 %) et 0,982821 (10 %). Ce rapport dépend du **rapport de deux vitesses** et de π̄ par `flex` ;
   - p/UC = 1,525068, 1,529815 et 1,532199 à × 0,5, × 1 et × 2 (π̄ = 2 %, écart relatif 4,68e−3) ; 1,496865, 1,519082 et 1,530439 à 10 % ;
   - **échec du critère 4** ;
   - λ ≤ n_a : `mu_fast` vaut 7,8 par an dans D1, mais 13 par an à sa valeur par défaut (0,25 par semaine, au-delà de n_a = 12) et 15,6 par an à × 2. **La condition de M22 est violée.**
   - Condition d'existence (critère 5 (c)) : (1 + μ)δk = 0,187 < 1 à t̄u.
   - Gain stationnaire de R3 avec rappel : d ln p/dz = κ_p·flex/μ_fast = 0,733 (D1, π^e = 2 %).

4. **Comportement** (faits de la première tentative) :
   - G1, branche « R3 désactivé » (S+O) : inflation moyenne 4,839 % contre 4,048 % ; PIB final −13,803 % ; chômage final 16,438 %. G1b (S+O) : prix de l'équipement +65,86 % ;
   - G-P (O) : la croissance du prix égale celle du coût unitaire à 0,04 point par an près ;
   - D1 sur 60 ans (R) : inflation 4,07 %, dérive de la part salariale 0,147 point ;
   - instabilité 9 (R) : `normal_average` seul, prix de l'équipement × 4,8 en 60 ans. Le commentaire de la l. 83 le confirme (L : « piste fermée ») ;
   - aucun de ces faits n'est remesurable (D1 non versé). La remesure P1 est proposée plus bas.

5. **Coût** : sans itération ; non mesuré.

6. **Défauts** :
   - critère 4 ;
   - λ > n_a au défaut ;
   - environ 7 bornes à seuil libre : clip(1 + adj, 0,7, 1,19) (l. 1128, 303), ±0,5 (l. 1120), marge dans [0, 2] (l. 1100), R3 dans ±min(κ̄·flex, 0,5) (l. 1122), écart de stocks dans ±1, max(π^e, 0), seuil 1e−3·Q̄ (l. 1072) ;
   - état caché (l. 1075) ;
   - neuf drapeaux : `wsps2`, `price_mode`, `pricing_cost_mode`, `price_basis`, `markup_live`, `markup_inv`, `equipment_price_mode`, `equipment_supply_response`, `price_demand_feedback` ;
   - amortissement au prix courant dans le coût : point fixe scalaire (instabilités 10 et 11 si lissé ou indexé).

7. **Identités** : aucune ligne ; l'amortissement du coût n'est pas la ligne 8.

8. **Ce que percevrait le joueur** : une marge qui dérive avec z, illisible ; des prix qui montent en récession par l'amortissement par unité.

9. **Empreinte** : p_{t−1}, μ_{t−1} et z_{t−1} (plus `_pK_repl` caché) ; environ 10 paramètres.

### 3.N Socle commun des options nouvelles (R, C, M, T, D)

#### 3.N-1 Phase de P_t (Q1, #24 ; critère 2 (c))

| | (a) P_t ≡ p_{t−1}, arrêté en phase 1 | (b) p_t fixé en phase 1, P_t ≡ p_t | (c) P_t ≡ p_t et π_t arrêtés en phase 5, lus en phase 1 du pas suivant |
|---|---|---|---|
| Ce que lisent les règles en phase 1 du tour n | π = p_{n−1}/p_{n−13} − 1 | π_n = p_n/p_{n−12} − 1 | π_{n−1} = p_{n−1}/p_{n−13} − 1 |
| Empreinte | registre de 12 valeurs (p_{t−2} à p_{t−13}), plus p_{t−1} en état du bloc 4 : **13** | registre de 12 valeurs (p_{t−1} à p_{t−12}) : **12** | registre de 12 valeurs (p_{t−1} à p_{t−12}), plus π_t en état : **13** |
| Valeur stationnaire | P_{t−u} = P_t(1 + π̄)^{−u/n_a} ; p_{t−1} = P_t | idem | idem ; π_t = π̄ |
| Délai prix → règle de taux | 1 tour | 0 tour | 1 tour |
| Délai prix → salaire (terme de niveau de SN) | 1 | 1 | 1 |
| Délai prix → anticipation → salaire (loi adaptative, lecture Q3 (a)) | 2 | 1 | 2 |
| Indice restitué au tour n | prix du tour n − 1 | prix du tour n | prix du tour n |
| Contrats révisés | aucun texte | M24 (p_t en phase 5), `tab:phases`, phase de UC (phase 1), `sec:production-phases` : décision citant M22, M24 et ADR | ADR 0005, pt 16 (une variable de plus), `sec:cadre-calendrier`, `tab:phases` (indice en phase 5) : décision citant M22 et ADR |
| Règles admises | toutes | aucune lecture des phases 2 à 4 (T exclue, sauf avec tu_{t−1} en état) | toutes |

- **Constat 1** : (a) et (c) donnent **des trajectoires identiques**, puisque les règles lisent la même chose. Elles ne diffèrent que par l'étiquette de l'indice et par sa restitution. (a) n'économise aucune variable : le prix p_{t−1} doit être tenu en état.
- **Constat 2, transmis à la fiche 3** : sous (a), T2 doit lire P_t (= p_{t−1}) et non P_{t−1} (= p_{t−2}). Sinon ω̄ = ω*(1 + π̄)^{1/n_a} et U* se déplace de −ln(1 + π̄)/(n_a β) : −0,0825 point (π̄ = 2 %, n_a = 12), −0,397 point (10 %), −0,2475 et −1,191 point à n_a = 4. Ce déplacement dépend de n_a. Sous (b) et (c), T2 lit bien la dernière entrée du registre, p_{t−1}.
- **Ordre interne de la phase 1** (critère 2 (d)) :
  - (c) : le bloc 4 n'écrit pas en phase 1 ; travail et banque centrale dans un ordre libre ;
  - (a) : prix (indice), puis banque centrale ; travail libre s'il lit p_{t−1} dans l'état ;
  - (b) : travail, puis prix, puis banque centrale.

  Les trois ordres sont triangulaires.

#### 3.N-2 Phase de UC (Q2)

- **Phase 2** sous (a) et (c). UC_t = W_t/pr_t ne dépend que de la phase 1 et de l'ouverture. La phase 2 est la première phase où agit le bloc 2 ; la phase 4 n'apporte aucune information de plus. Au socle, aucun bloc ne lit UC avant la phase 5 ; la phase 2 le rend disponible pour les plans de la phase 3 si une fiche ultérieure en a besoin.
- Sous (b), UC est requis en phase 1 : le bloc 2 y écrirait (révision de `tab:production-phases`).

#### 3.N-3 Base de coût (Q3)

- **Retenue pour R, C, M, T et D : UC = W/pr de M24.** Sous M24, pr est la productivité tendancielle : **UC est déjà un coût normal** au sens « coût à productivité normale » (Coutts, Godley et Nordhaus, définition citée de mémoire). La marge couvre l'amortissement et la rémunération du capital. Aucun lien à la ligne 8 et aucun double compte.
- **Coût complet au prix courant** : p/UC = (1 + μ)/(1 − (1 + μ)δk), soit 1,538462 (part salariale 0,650). C'est un point fixe en forme fermée ; il existe tant que tu > (1 + μ)δκ = 0,15. En transition, le prix est contracyclique (il monte quand tu baisse). Non retenu.
- **Coût complet à la valeur comptable** : p/UC = (1 + μ)/(1 − (1 + μ)δρ̄_K k), soit 1,538462 à π̄ = 0, 1,463826 à 2 % et 1,357424 à 10 % (part 0,650, 0,683 et 0,737). **La part salariale dépend de π̄**, contre le critère 3 (d). Écarté.
- **Marge sur cm** : p/UC = 1,247128 (2 %) et 1,236339 (10 %). Sous SN (w1), U* se déplace de −0,115 et −0,550 point, avec une dépendance à n_a (−0,1148 / −0,1150 / −0,1151 à n_a = 4 / 12 / 52). Écarté (critère 3 (c) et (d)). La forme NHUC de Godley et Lavoie (coût historique avec financement des stocks), citée de mémoire, ferait en outre dépendre la part salariale du taux d'intérêt. Notée, non instruite.
- **Coût retardé** (UC_{t−1}) : exact seulement avec un coefficient 1 sur π^e. Aucun gain sur UC_t. Non retenu.

#### 3.N-4 Terme de demande (Q4 ; critères 4 (b) et 5 (b))

- **Retenu : ξ_t**, le stock d'ouverture rapporté à sa cible.
  - Lu à l'ouverture (IN^vol_t, v^e_t) ; disponible dès la phase 1.
  - Signe + : un stock bas relève la marge.
  - Forme logarithmique sur la marge.
  - **Valeur stationnaire nulle exactement**, quelles que soient les vitesses (N3 et N7 donnent IN^vol = n_a σ v^e).
  - Condition déclarée : v^e_t > 0, vraie si d > 0 ou si λ_v < n_a.
- **z de la v1.5 et de la v2.0** : non nul en croissance (−0,001165), donc fait dépendre l'état des vitesses (3.A-3, 3.B-3).
- **Production visée non réalisée** et **demande non servie** : nulles hors contrainte d'emploi ou rationnement ; trop rares pour servir de signal de demande général. Non retenues.
- **tu** : option T.

#### 3.N-5 Anticipation consommée (Q6 ; critère 9)

- R, C, M et T : **aucune**. C'est le coefficient 0 sur une base courante (règle de `monnaie`, fiche 3, § 6.1, Q4). Aucune indexation des prix : pas de double compte avec les salaires indexés (v2.0, l. 1120, commentaire).
- D consomme π^e avec le coefficient 1 − λ_p/n_a : 0 sur base courante (λ_p = n_a), vers 1 sur base retardée (λ_p → 0). C'est la règle de `monnaie` généralisée, à confirmer par `monnaie`.
- Indice produit (9 (c)) : P_t ≡ p_t sous (b) et (c), p_{t−1} sous (a) ; restitution en base 100 au tour 1. Pondérations laissées ouvertes à J ≥ 2 (Laspeyres, v1.5, l. 679). π_t est mesuré, jamais converti.

#### 3.N-6 Lecture des taux annuels (Q7, #24)

- R, C, M et T **ne contiennent aucun taux annuel** : leur état stationnaire est identique sous (L) et sous (G). Le glissement stationnaire vaut π̄ exactement (mesuré).
- Seule D dépend de la lecture. Sous (G), p/[(1 + μ̄)UC] = 1 exactement. Sous (L) avec un π^e en glissement : 1,000136 (π̄ = 2 %, n_a = 12, λ_p = 1,2), 1,003212 (10 %), et 1,000286 / 1,000060 à λ_p × 0,5 / × 2 (écart relatif 2,26e−4, **échec du critère 4**). Sous (L) avec un π^e en taux linéaire annualisé, D est exacte.
- La lecture commune se décide donc sur les fiches 3 et 8 et sur M24 (f). La fiche 4, sous M, ne la contraint pas. Je maintiens la préférence (G) pour la cohérence de la restitution (fiche 3, § 3.N-4).

#### 3.N-7 Phases et lectures (critère 2), sous (c)

| Phase | Le bloc 4 lit | Le bloc 4 écrit |
|---|---|---|
| 1 | rien | rien |
| 2 | — | — (UC écrit par le bloc 2) |
| 5, premier bloc | ouverture : p_{t−1} (registre), W_{t−1}, pr_{t−1}, IN^vol_t, v^e_t ; phase 1 : W_t ; phase 2 : UC_t ; phase 4 : tu_t (T seulement) | p_t ; puis P_t ≡ p_t et π_t = p_t/P_{t−12} − 1 |

Aucune lecture de v_t ni de d_t. Matrice triangulaire. Indexation par j (critère 2 (f)) : p_{j,t} = UC_{j,t}·exp(μ̃_{j,t}). Au J5, le terme d'intrants Σ a_kj p_k du même pas ferait un système linéaire de prix (résolution en forme fermée, ou prix d'intrants retardés pour garder la triangularité). Signalé, non résolu.

#### 3.N-8 État stationnaire, conjoint avec la fiche 3 (critère 3)

Sous SN (w1) et M, C, T, D (sous (G)) ou R :
- p/UC = 1 + μ̄ exactement ; μ_t = μ̄ ; ξ̄ = 0 ;
- W/(p·pr) = ω̄ = 1/(1 + μ̄) = ω*, donc U* = U^eq ;
- variation du prix (1 + π̄)^{1/n_a} − 1 par pas (0,16516 % à 2 %) ; glissement π̄ ;
- aucune vitesse, ni n_a, ni la lecture (L) ou (G) n'y entre (sauf D sous (L)).

**WB/VA sur 12 tours** (P1, μ̄ = 0,25, g = 2 %, σ = 1,4 mois) :

| | π̄ = 2 % | π̄ = 10 % |
|---|---|---|
| (G), n_a = 12 | 0,798903 (−0,1097 point) | 0,793445 (−0,6555 point) |
| (L), n_a = 12 | 0,798907 (−0,1093 point) | 0,793448 (−0,6552 point) |

- Sous (L) à 2 % : 0,798909 / 0,798907 / 0,798906 à n_a = 4 / 12 / 52, soit moins de 0,0003 point d'écart.
- Simulation et forme fermée concordent à 4,4e−16.

**Qui ancre le partage (Q9)** : le bloc 4, par μ̄. Sous (w1), le bloc 3 lit μ̄ par ω* : un seul paramètre, et des prétentions compatibles par construction. Sous (w2), les deux blocs portent une cible, et U* = U^eq + ln(ω*(1 + μ̄))/β. Sous C1 et C2 (`monnaie`), **π̄ ne dépend pas de l'écart** : le conflit est absorbé par le chômage d'équilibre. π̄ en dépendrait seulement si la demande maintenait U ≠ U*. À π^e fixé, l'écart vaudrait π − π^e ≈ λ_w ln(ω*(1 + μ̄)) ; il dépendrait alors de λ_w (critère 4), et le point est soumis au mainteneur. Rowthorn (1977) : existence vérifiée, non lu.

**Ce que le bloc ne fixe pas** (critère 4 (d)) : le niveau des prix (racine unitaire, 3.N-9) et le rythme (fiche 8).

#### 3.N-9 Boucles (critère 5 (d) à (f))

- **5 (d), boucle propre** (coûts et ξ exogènes) :

  | Option | Valeur propre | Demi-vie |
  |---|---|---|
  | M | 1 − λ_μ/n_a = 0,9 | 6,58 tours |
  | M, × 0,5 | 0,95 | 13,5 tours |
  | M, × 2 | 0,8 | 3,11 tours |
  | D | identique à M avec λ_p | |
  | R, C, T instantanée | sans objet : aucune variable d'état | |
  | A | 0,7823 (× 0,5 : 0,8903 ; × 2 : 0,5663) | |
  | B | 0,4702 et 0,9781 (demi-vie de la marge 31,3 tours) ; × 0,5 : 0,7343 et 0,9890 ; × 2 : −0,0579 et 0,9561 | |

- **5 (f), boucle prix – stocks – demande** (coûts exogènes, plans en u.m.) : rayon (période en tours) pour m = 0,5 / 0,6 / 0,7 / 0,8.

  | Option | Calibration | Vitesses de la fiche 2 × 0,5 | Vitesses de la fiche 2 × 2 | ψ × 2 |
  |---|---|---|---|---|
  | R (prix figé) | 0,9279 / 0,9452 / 0,9612 / 0,9762 (69 à 96) | — | — | — |
  | C | 0,9490 / 0,9605 / 0,9717 / 0,9824 (76 à 111) | 0,9700 à 0,9886 | **1,1808 à 1,3028, racine réelle négative (alternance d'un tour sur l'autre)** | **1,2545 à 1,3090, alternance** |
  | M | 0,9420 / 0,9535 / 0,9658 / 0,9783 (94 à 115) | 0,9700 à 0,9878 (169 à 218) | 0,8791 à 0,9647 (43 à 60) | 0,9534 à 0,9813 |
  | T | 0,9233 / 0,9405 / 0,9566 / 0,9716 (76 à 101) | 0,9589 à 0,9837 | 0,9033 à 0,9571 | 0,9202 à 0,9674 |
  | D | identique à M (coûts exogènes) | | | |

  - M aux vitesses du bloc × 0,5 : 0,9400 à 0,9733 ; × 2 : 0,9477 à 0,9808.
  - Frontière de C (P6) : ψ_ξ ≤ 0,257 pour tenir toutes les combinaisons (vitesses de la fiche 2 × 2, m = 0,8) ; ψ_ξ ≤ 0,684 à la calibration.
  - Frontière de M : ψ_ξ ≥ 10 à la calibration, 4,875 aux vitesses × 2.
  - La variante T instantanée, sans mémoire, est explosive aux vitesses de la fiche 2 × 2 avec m = 0,8 (−1,0345).
  - M ≡ C quand λ_μ = n_a (vérifié).

- **5 (e), boucle salaires – prix, exigence** (SN + prix, π^e = π̄ exogène, partie réelle). Rayon pour m = 0,5 / 0,6 / 0,7 / 0,8.

  | Option | Calibration | Tout × 0,5 | Tout × 2 | Autres variantes |
  |---|---|---|---|---|
  | R | 0,8975 / 0,9172 / 0,9353 / 0,9520 | 0,9507 à 0,9779 | 0,7631 à 0,8857 | |
  | C | 0,9157 / 0,9286 / 0,9410 / 0,9529 | | **1,0264 à 1,1219 pour m ≥ 0,6** | vitesses de la fiche 2 × 2 : **1,0833 à 1,2161** ; ψ × 2 : **1,1859 à 1,2439**, toujours en alternance |
  | **M** | **0,8969 / 0,9068 / 0,9225 / 0,9385** | 0,9479 à 0,9714 | 0,8070 à 0,8583 | λ_w × 2 : 0,9322 à 0,9351 ; ψ × 2 : 0,9163 à 0,9346 |
  | T | 0,8990 / 0,9106 / 0,9290 / 0,9459 | 0,9498 à 0,9763 | 0,7922 à 0,8636 | |
  | D | 0,9118 / 0,9290 / 0,9452 / 0,9605 | 0,9555 à 0,9794 | 0,8263 à 0,9224 | |

  **Racine unitaire attendue et déclarée** : le niveau nominal. On a |λ − 1| ≤ 7,5e−10, et le vecteur propre est nominal (composantes réelles ≤ 2,6e−8, p/w = 1,25). Avec M, la boucle salaires – prix est plus amortie que sans terme de demande (0,9068 contre 0,9172 pour R à m = 0,6).

- **5 (e), mesure** (anticipation adaptative hypothétique, λ_e ∈ {0,5 ; 1 ; 2}, glissement sur 12 tours ; P10, m = 0,6) :
  - **Fermeture neutre** (plans indexés sur π^e) : la partie réelle **ne dépend pas de λ_e**. Rayons à λ_w = 1 : R 0,9172, C 0,9286, M 0,9068, T 0,9106, D 0,9290 ; à λ_w = 2 : 0,8851 / 0,8927 / 0,9329 / 0,9034 / 0,9100. Il y a **une racine unitaire du rythme d'inflation** : dichotomie, aucun rythme n'est ancré par les blocs 3 et 4. Résultats identiques sous (b) et sous (c).
  - **Fermeture ancrée hypothétique** (plans indexés sur π̄, substitut de la fiche 8) : stable partout. Pour M, λ_w = 1 : 0,9909 / 0,9856 / 0,9803 (demi-vies 75,8 / 47,8 / 34,8 tours) ; λ_w = 2 : 0,9860 à 0,9731. Pour D : 0,9939 à 0,9821. Les racines sont réelles positives, sans oscillation.
  - La stabilité du rythme relève donc de la règle de la fiche 8 (C2). Le rapport « λ_w = 2 instable » de la v2.0 n'est pas reproduit dans cette maquette ; ce n'est pas une remesure de la v2.0.

#### 3.N-10 Bornes (critère 7)

- M, C, T, D et R : **aucune borne**.
- Positivité de p et de 1 + μ par la forme exponentielle.
- ξ ≤ 1 découle de IN ≥ 0 (conservation).
- Conditions déclarées, sans écrêtage : λ_μ, λ_p ≤ n_a ; v^e > 0.
- 7 (c) : rien à désactiver dans le bloc 4.

#### 3.N-11 Cohérence stock-flux (critère 1 ; P15)

Cas : UC = 1, y = 100, IN^vol = IN = 140, plans de 100 (ménages), 20 (État) et 5 (investissement) en u.m.

| p | Volumes C / G / I | Lignes 1 à 3 | Ligne 4 | Résultat courant | ΔV_F (flux = stock) | Somme des ΔV |
|---|---|---|---|---|---|---|
| 1,25 | 80 / 16 / 4 | 100 / 20 / 5 | 0 | 25,0000 | 25,0000 | 5,0000 = I + ligne 4 |
| 1,2625 | 79,2079 / 15,8416 / 3,9604 | 100 / 20 / 5 | +0,9901 | 25,9901 | 25,9901 | 5,9901 = I + ligne 4 |

Le prix ne crée aucune valeur nette financière : la somme des soldes financiers est nulle dans les deux cas. Il répartit les volumes ; l'invendu reste en stock au coût. Aucune ligne ajoutée.

#### 3.N-12 Faits et calibration (critère 14)

- μ̄ : à caler au J3 sur la part salariale. La fiche 3 cite 0,52 (Penn World Table, extrait).
- ψ_ξ et λ_μ : **aucune source ne les fixe**.
  - Signe de ψ : marge procyclique après un choc de demande (Nekarda et Ramey, extrait), mais **fait contesté**.
  - Faible sensibilité à la demande (Blinder et al., extrait ; Coutts, Godley et Nordhaus, non lu).
  - λ_μ = 1,2 par an : ordre de grandeur de 10 % de révision mensuelle (Nakamura et Steinsson, extrait). Ce n'est pas un fait établi pour une marge.

#### 3.N-13 Coût, empreinte, notation (critères 11 à 13)

- Coût de M (P13) : 0,402 µs par pas, soit 0,084 % de 0,48 ms. Machine de la session (x86_64, 4 cœurs, Python 3.11.15), **qui n'est pas la plateforme de l'ADR 0003**. Aucune itération.
- Empreinte : aucune variable d'état propre à M (μ̃_{t−1} se lit sur p_{t−1}, W_{t−1} et pr_{t−1}). Sous (c), l'empreinte calendaire gagne π_t.

### 3.R Option R — référence sans retard

1. p_{j,t} = (1 + μ̄_j)UC_{j,t}. Choix de conception.
2. État stationnaire exact.
3. 5 (e) : 0,8975 à 0,9520.
4. **Échec du critère 5 (b)** : pas de terme de demande. Démonstration partielle : le mécanisme de l'instabilité 14 mesuré en v2.0 (prix de l'équipement dans son propre coût) n'a pas d'objet, puisque UC ne contient pas p. Mais la transposition de G1b à J = 1 n'est pas établie. **Je ne la soumets pas comme fait nouveau.**
5. Délais : salaire → prix 0 tour, demande → prix seulement par les salaires (2 tours).
6. Joueur : salaire réel figé, aucun effet de répartition (fiche 3, § 7, question 8).
7. Empreinte : 1 paramètre, 0 état, 0 borne.
8. Coût négligeable.
9. Rôle de référence (`docs/exigences.md` § 2.7).

### 3.C Option C — prix au coût normal majoré, marge instantanée sensible aux stocks (nouvelle)

1. **Source** : tarification au coût normal (Coutts, Godley et Nordhaus, 1978, non lu) et marge sensible aux stocks, attribuée à Godley et Lavoie, ch. 8, par le commentaire de la v2.0 (l. 1086, L ; non vérifié dans la source).
2. **Équation** : p_{j,t} = (1 + μ̄_j)·exp(ψ_ξ ξ_{j,t})·UC_{j,t}. Approchée.
3. **État stationnaire** exact (3.N-8).
4. **Comportement** : stable à la calibration. **Explosive en alternance d'un tour sur l'autre** aux vitesses de la fiche 2 × 2 ou à ψ × 2 (3.N-9). Simulation non linéaire : écart de prix de 65 % au tour 60 depuis 1e−6.
5. **Coût** : négligeable.
6. **Défauts** : toile d'araignée prix – plan nominal. ψ ≤ 0,26 pour être robuste, ce qui ne laisse presque plus d'effet de demande. Confrontée à R3 : terme de niveau sur ξ, nul à l'état stationnaire, au lieu d'un terme de taux sur z, non nul en croissance.
7. **Identités** : aucune ligne.
8. **Joueur** : marge qui saute dès le tour suivant le choc (+0,121 point au tour 2) ; risque de prix alternés.
9. **Empreinte** : 2 paramètres, 0 état, 0 borne.

### 3.M Option M — coût normal majoré, marge à ajustement partiel vers une cible sensible aux stocks (nouvelle)

1. **Source** : construction du projet. Elle combine le coût normal (3.N-3), une marge visée sensible aux stocks (comme en C) et un ajustement partiel ancré. Lecture appuyée par l'extrait de Blinder et al. : coûts répercutés, hausses liées à la demande mal tolérées. **Aucune source lue ne donne cette forme exacte.**
2. **Équations** :
   - ln p_{j,t} = ln UC_{j,t} + μ̃_{j,t} ;
   - μ̃_{j,t} = (1 − λ_μ/n_a)·ln(p_{j,t−1}/UC_{j,t−1}) + (λ_μ/n_a)·[ln(1 + μ̄_j) + ψ_ξ ξ_{j,t}].

   Variables : p et UC en u.m. par u.v. ; ξ sans dimension ; λ_μ par an, avec λ_μ ≤ n_a ; ψ_ξ sans dimension. Statut : approchée (ajustement partiel), choix de conception (cible).
3. **État stationnaire** : μ̃ = ln(1 + μ̄) exactement, sans terme de tendance puisque la marge est un rapport. Il est indépendant de λ_μ, de n_a, de π̄ et de la lecture des taux.
4. **Comportement** :
   - 5 (d) : 0,9 ;
   - 5 (e) : 0,8969 à 0,9385, robuste à toutes les variantes ;
   - 5 (f) : 0,9420 à 0,9783 ;
   - marge procyclique ;
   - exemple au § 3.L.
5. **Coût** : 0,402 µs par pas.
6. **Défauts** :
   - période de la boucle prix – stocks plus longue qu'à prix figé (94 contre 73 tours à m = 0,6) ;
   - vitesse de la marge non sourcée ;
   - pas de vitesse modulée par l'inflation (`flex`), qui serait neutre à l'état stationnaire (elle multiplierait un écart nul) : piste possible pour l'hyperinflation au J6.
7. **Identités** : aucune ligne.
8. **Joueur** : coût salarial répercuté le tour même ; marge qui monte progressivement en tension (+0,12 point au pic pour G +1 %, +0,60 point pour +5 %, m = 0) ; part salariale qui baisse en expansion puis se redresse : des gagnants et des perdants.
9. **Empreinte** : 3 paramètres (μ̄, ψ_ξ, λ_μ), 0 état propre, 0 borne.

### 3.T Option T — variante en taux d'utilisation (nouvelle ; critère 8)

1. Cible ln(1 + μ̄) + ψ_tu(tu_{j,t} − t̄u_j), même forme que M. tu est lu en phase 4.
2. **État stationnaire** exact **si tu → t̄u**, ce qui relève de la fiche 6. Sinon, la marge est déplacée de façon permanente et, sous SN (w1), U* = U^eq + ψ_tu Δtu/β. Par exemple, Δtu = +0,05 donne +1,25 point : **second ancrage**.
3. 5 (e) : 0,8990 à 0,9459 ; 5 (f) : 0,9233 à 0,9716.
4. Incompatible avec (b) sans tu_{t−1} en état.
5. t̄u doit être un paramètre de la fiche 6 lu à source unique, comme U^eq (C6 de `monnaie`).
6. Joueur : un coût du sous-investissement sous forme d'inflation en capacité tendue (8 (c)).
7. Empreinte : 3 paramètres, 0 état.
8. Coût : négligeable.
9. Décision au plus tard à la fiche 6 (#37).

### 3.D Option D — prix à ajustement partiel indexé sur l'anticipation (type Calvo, nouvelle)

1. ln p_t = (1 − λ_p/n_a)[ln p_{t−1} + (1/n_a)ln(1 + π^e_t)] + (λ_p/n_a)[ln((1 + μ̄)UC_t) + ψ_ξ ξ_t]. Approchée. Fréquence de Nakamura et Steinsson, extrait.
2. **État stationnaire** exact sous (G), ou sous (L) avec un π^e en taux linéaire. Sous (L) avec un π^e en glissement, échec du critère 4 (3.N-6).
3. 5 (e) : 0,9118 à 0,9605 ; 5 (f) : identique à M.
4. Consomme π^e (coefficient 1 − λ_p/n_a).
5. Marge **contracyclique** en expansion (−0,13 point pour G +1 %) : c'est la transmission NK que l'extrait de Nekarda et Ramey conteste.
6. Délai salaire → prix fractionné : 10 % le tour même.
7. Empreinte : 3 paramètres, 0 état (p_{t−1} vient du registre).
8. Coût : négligeable.
9. Joueur : inflation plus lente et plus lisse (pic +0,25 point pour G +1 %).

### 3.L Restitution et exemple daté (critère 10)

**Exemple** (P11) : dépense publique +1 % aux tours 1 à 12, part de G de 20 % (hypothèse), m = 0, g = 0, π^e exogène, lecture (c). Écarts au sentier pour M :

| Tour | Production % | U (pt) | W % | p % | Variation du prix sur le tour (pt) | Glissement lu par la BC (c) (pt) | Idem sous (b) (pt) | Marge (pt) | W/(p·pr) (pt) | ξ % |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0,000 | 0,000 | 0,000 | 0,000 | 0,000 | 0,000 | 0,000 | 0,000 | 0,000 | 0,000 |
| 2 | +0,084 | −0,080 | 0,000 | +0,010 | +0,010 | 0,000 | +0,010 | +0,012 | −0,008 | +0,193 |
| 3 | +0,138 | −0,131 | +0,014 | +0,038 | +0,028 | +0,010 | +0,039 | +0,030 | −0,019 | +0,304 |
| 4 | +0,168 | −0,160 | +0,038 | +0,077 | +0,039 | +0,039 | +0,078 | +0,049 | −0,031 | +0,349 |
| 9 | +0,193 | −0,184 | +0,211 | +0,300 | +0,043 | +0,262 | +0,306 | +0,111 | −0,071 | +0,282 |
| 13 | +0,189 | −0,179 | +0,364 | +0,461 | +0,038 | +0,431 | +0,471 | +0,121 | −0,077 | +0,197 |
| 14 | +0,104 | −0,099 | +0,402 | +0,489 | +0,028 | +0,471 | +0,489 | +0,108 | −0,069 | −0,013 |
| 18 | −0,007 | +0,006 | +0,450 | +0,472 | −0,012 | +0,370 | +0,312 | +0,028 | −0,018 | −0,225 |
| 24 | −0,011 | +0,010 | +0,438 | +0,407 | −0,009 | +0,034 | −0,016 | −0,037 | +0,024 | −0,147 |

**Comparaison**, prix % et marge (pt) aux tours 2 / 9 / 13 / 18 / 24 :

| Option | Prix % | Marge (pt) |
|---|---|---|
| R | 0 / +0,194 / +0,325 / +0,384 / +0,362 | 0 |
| C | +0,096 / +0,393 / +0,528 / +0,401 / +0,356 | +0,121 / +0,187 / +0,142 / −0,112 / −0,108 |
| T | +0,003 / +0,243 / +0,397 / +0,454 / +0,425 | +0,004 / +0,052 / +0,068 / +0,044 / +0,018 |
| D | +0,010 / +0,156 / +0,242 / +0,251 / +0,227 | +0,012 / −0,047 / −0,091 / −0,120 / −0,077 |

**Contrôles à la main** :
- M au tour 2 : 0,1 × 0,5 × 0,193 % = +0,0097 % ;
- C au tour 2 : 0,5 × 0,193 % = +0,0965 % ;
- R au tour 3 : (1/12) × 2 × 0,080 point = +0,0133 %.

Le niveau des prix reste durablement plus haut (+0,41 % au tour 24) : c'est la racine unitaire nominale.

**Ampleurs** (P14 ; pic de l'écart du glissement lu sous (c), G +1 % / +5 % aux tours 1 à 12) :

| Option | m = 0 | m = 0,6 |
|---|---|---|
| M | +0,49 / +2,46 point (tour 15) | +0,86 / +4,34 point (tour 17) |
| R | +0,37 / +1,85 | +0,69 / +3,51 |
| C | +0,54 / +2,71 | +0,89 / +4,50 |
| T | +0,44 / +2,20 | +0,80 / +4,07 |
| D | +0,25 / +1,24 | +0,47 / +2,36 |

Pour M avec m = 0,6 : marge au plus +0,23 / +1,13 point ; part salariale au plus bas −0,15 / −0,71 point.

**Délais en tours entiers** (M, lecture (c)) :
- salaire → prix : 0 tour ;
- demande → prix : 1 tour (ξ d'ouverture) ;
- prix → règle de taux : 1 tour, 0 sous (b) ;
- prix → salaire : 1 tour ;
- contrepartie au tour du choc : les stocks (fiche 2), puis la marge.

**Leviers** : la dépense publique agit sur les stocks au tour n et sur le prix au tour n + 1. Les impôts et le taux agissent par les fiches 5, 6, 8 et 9, avec 1 tour de plus que leur effet sur la demande.

**Indicateurs au tour** :
- indice (base 100) ; glissement sur 12 tours ; variation sur le tour ;
- marge (au tour et en moyenne sur 12 tours) ;
- part salariale W/(p·pr) et WB/VA sur 12 tours, avec leur écart stationnaire publié ;
- décomposition de l'inflation (coût unitaire, marge) ;
- écart de stocks ξ ;
- niveaux normaux : μ̄, ω̄, π̄.

**Q10, prix administrés** (renvoyés au J4 et au J7). Interface notée : un levier remplacerait p_t en phase 5 ; la marge devient résiduelle ; le rationnement passe par N6. Sous M, à la levée du levier, la marge rejoint μ̄ à la vitesse λ_μ, sans saut : une inflation corrective lisible.

### Statut des faits de la première tentative (critère 15)

| Fait | Statut |
|---|---|
| G1 et G1b (R3 désactivé) | S+O |
| G-P | O |
| D1 sur 60 ans (4,07 %, 0,147 point) | R |
| Instabilités 9 à 13 et 15 | R |
| Instabilité 14 | S+O (G1b) et R |
| Instabilité 16 | S+O |
| Acquis R3 et « stabilisateurs cachés » | R |
| Réfutée 9 | S+O |
| Lignes de la v2.0 et de `workplan.py` citées | L, vérifiées le 03/10/2026 |
| Commentaires l. 83 et l. 1086 | L (commentaire), contenu non mesuré |
| Résultats de la v1.5 (l. 767) | rapportés, invérifiables |
| Instabilités 12 (« N6, correction de marge par le gain ») et 13 (« R1, élasticité à référence mobile ») | contenu non documenté dans la synthèse ; M ne corrige pas la marge par un gain, et la référence de ξ est la cible de M24, ancrée. **À confirmer si leur contenu est retrouvé** |

Aucun fait D1 n'a été remesuré.

## 4. Tableau comparatif

| Critère | A (v1.5) | B (v2.0) | R | C | M | T | D |
|---|---|---|---|---|---|---|---|
| 1 Flux | aucune ligne (3.A-7) | idem (3.B-7) | 3.N-11 | idem | idem | idem | idem |
| 2 Phases | z retardé, état (3.A-2) | idem ; λ > n_a au défaut (3.B-3) | 3.N-7 | 3.N-7 | 3.N-7 | phase 4 ; exclue sous (b) (3.T-4) | 3.N-7 |
| 2 (c) P_t | — | — | 3.N-1 | 3.N-1 | 3.N-1 | 3.N-1 | 3.N-1 |
| 3 Forme fermée | dépend de λ_S ; aucun état stationnaire si λ_S = 0,5 (3.A-3) | dépend des vitesses (3.B-3) | exacte | exacte | exacte | exacte si tu → t̄u | exacte sous (G) |
| 3 (d) avec la fiche 3 | — | — | U* = U^eq (3.N-8) | idem | idem | second ancrage possible | idem |
| 4 Vitesses | **échec** (1,14e−2) | **échec** (4,68e−3) | oui | oui | oui | oui sous condition | (G) oui ; (L) **échec** (2,26e−4) |
| 5 (a) | tâtonnement | instabilités 9 à 11 | 14 (3.R-4) | rien | rien | rien | rien |
| 5 (b) Demande | z | z, R3 | **échec** | ξ | ξ | tu | ξ |
| 5 (d) | 0,7823 | 0,9781 | sans objet | sans objet | 0,9 | 0,9 | 0,9 |
| 5 (e) exigence | non calculé | non calculé | 0,8975 à 0,9520 | 0,9157 à 0,9529 ; **> 1 aux variantes** | **0,8969 à 0,9385** | 0,8990 à 0,9459 | 0,9118 à 0,9605 |
| 5 (e) adaptative | — | — | dichotomie ; ancrée < 1 | idem | idem | idem | idem |
| 5 (f) | — | — | 0,9279 à 0,9762 | **alternance à × 2** | 0,9420 à 0,9783 | 0,9233 à 0,9716 | = M |
| 6 Préalable | non | non | oui | oui | oui | sous condition | oui sous (G) |
| 7 Bornes | 5 | environ 7 | 0 | 0 | 0 | 0 | 0 |
| 8 tu | — | — | non | non | non, renvoi à la fiche 6 | oui | non |
| 9 Anticipation consommée | π^e (×2) | π^e (`flex`) | aucune | aucune | aucune | aucune | π^e |
| 10 Délais | — | — | 0 / 2 | 0 / 1 | 0 / 1 | 0 / 1 | partiel / 1 (3.L) |
| 11 Empreinte | 2 états, environ 9 paramètres | 3 états (1 caché), environ 10 paramètres, 9 drapeaux | 0 état, 1 paramètre | 0 état, 2 paramètres | 0 état, 3 paramètres | 0 état, 3 paramètres | 0 état, 3 paramètres |
| 12 Coût | non mesuré | non mesuré | négligeable | négligeable | 0,402 µs | négligeable | négligeable |
| 13 Notation | collisions ϖ, m | κ | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 |
| 14 Calibration | — | — | 3.N-12 | 3.N-12 | 3.N-12 | 3.N-12 | 3.N-12 |
| 15 Faits | statuts | statuts | — | — | — | — | — |

Dans la ligne 10, le premier chiffre est le délai salaire → prix et le second le délai demande → prix, en tours.

## 5. Avis de l'expert pilote

*`macro`, 03/10/2026.*

**Recommandation : option M**, avec les choix suivants :
- base UC (Q3) ;
- UC écrit en phase 2 (Q2) ;
- terme de demande ξ (Q4) ;
- aucune anticipation consommée (Q6) ;
- règle neutre entre (L) et (G) (Q7 ; préférence (G) maintenue pour les fiches 3 et 8) ;
- partage ancré par μ̄ avec (w1) (Q9) ;
- aucun terme en tu à M26 : T est transmise à la fiche 6, à décider au plus tard à M28 (Q5, #37) ;
- prix administrés renvoyés au J4 et au J7 (Q10).

**Phase de P_t (Q1)** : lecture (c), avec une variable d'état de plus (π_t). Décision citant M22 et l'ADR 0005, pt 16 : issue sensible. Repli : (a), mêmes trajectoires, aucun texte changé, mais un indice décalé d'un tour sur son prix. (b) seulement si `monnaie` tient à un délai nul, au prix d'une révision de M24.

**Motifs** :
- état stationnaire exact et indépendant des vitesses, de n_a et de la lecture des taux (critères 3 et 4) ;
- seule option nouvelle avec terme de demande qui reste stable sur toute la grille (5 (b), (e) et (f)) ;
- aucune borne ;
- aucune anticipation consommée ;
- coût salarial répercuté le tour même ;
- marge qui répond à la tension, comme le demande `jeu` (fiche 3, § 7, question 8).

**Écartées** :
- A et B : critères 4, 7 et 11 ; B viole aussi λ ≤ n_a à ses valeurs par défaut et a un état caché ;
- R : critère 5 (b), gardée comme référence ;
- coût complet et marge sur cm : critère 3 (d).
- C n'échoue à aucune exigence à la calibration. Je la déconseille pour sa fragilité : alternance explosive dès que les vitesses de la fiche 2 ou ψ doublent.
- D est une alternative acceptable sous (G). Elle consomme π^e et sa marge est contracyclique, un fait contesté.

**Réserves**, avec leurs critères écrits avant l'essai (J3) :
1. Un pas sans choc depuis l'état initial résolu laisse μ̃ à ln(1 + μ̄) à 1e−10 près.
2. Critère 4 : écart ≤ 1e−6 après 720 pas entre λ_μ × 0,5 et × 2.
3. 5 (e) et 5 (f) remesurés avec le m effectif des fiches 5 et 9, rayon < 1. Test de propriété : après une impulsion de demande de 1 % sur un tour, l'écart du prix ne change pas de signe plus de deux fois en 12 tours (pas d'alternance).
4. Calibration de ψ_ξ et de λ_μ sur des sources lues.
5. Constat T2 sous (a), transmis à la fiche 3.
6. Valeur centrale de la bande de part salariale : W/(p·pr) ou WB/VA (−0,110 point à 2 %, −0,656 point à 10 %), à trancher par le mainteneur.

**Lectures possibles, soumises au mainteneur** :
- (a) Q1 : (c), (a) ou (b) ;
- (b) M ou C (marge à mémoire ou instantanée) ;
- (c) M ou D (cyclicité de la marge, contestée) ;
- (d) terme en tu maintenant (T) ou à la fiche 6 ;
- (e) (w1) au socle, (w2) au J4.

**Coût en fidélité** : la forme exacte de M n'a pas de source lue. La marge procyclique est contestée. Aucune fréquence de prix dépendante de l'inflation (`flex`). Godley et Lavoie, NHUC (financement des stocks) n'est pas repris.

## 6. Avis de l'expert consulté

*Rédigé par `monnaie` (expert consulté : frontière inflation et volet « prix » de #24) le 03/10/2026, sur la fiche à l'état `ff3f97d` (branche `claude/j1-economie-reelle`, PR #43). Cet avis reste cohérent avec mon avis sur la fiche 3 (`travail.md` § 6, conditions C1 à C8). Il y apporte une précision, au § 6.3.*

*Sources lues dans le dépôt :*
- *fiche 4, § 1 à 5 ;*
- *fiche 3, § 3.N-2 à 3.N-6, § 5 et § 6 ;*
- *issue #24 ;*
- *`sec:cadre-calendrier` et `tab:phases` (l. 190 à 215 et 495 à 512) ;*
- *ADR 0005, pt 16 ;*
- *`archive/faits_mesures_G_K.md`, § 6 à 8.*

*J'ai relancé le script P10 de `macro` et ajouté trois scripts de contrôle (commandes au Retour). Pour chaque référence, j'indique ce qui a été lu (texte primaire), ce qui a été extrait (résumé ou notice) et ce qui est cité de mémoire.*

### 6.1 Réponses aux six questions de `macro`

**Q1 — Phase de P_t.** Je préfère **(c)**. Le repli acceptable est (a), à condition de corriger T2 (Q6). Je ne demande pas (b).

1. **Le calendrier de Barro et Gordon ne tranche pas la Q1.**
   - Ce qu'il fixe : les anticipations sont données avant la décision de la période. Résumé du document de travail NBER w0807 (1981), publié au *JPE* 91(4), 589-610 (1983), extrait : « At each point in time, the policymaker optimizes subject to given inflationary expectations ».
   - Ce calendrier contraint la date de π^e, déjà réglée par la lecture (a) de la Q3 de la fiche 3. Il ne dit pas quelle inflation la règle lit.
   - Sous M, p_n ne dépend que de l'état d'ouverture : W_n (Q3 (a)), UC_n, ξ_n et la marge retardée. Dans les trois lectures, l'inflation lue par la règle au tour n est donc prédéterminée par rapport aux leviers du tour n. Il n'y a de simultanéité dans aucun cas.
2. **Même information pour la règle et pour le joueur.**
   - Sous (c), la règle du tour n lit π_{n−1}, l'inflation que le joueur voit quand il décide. La prescription de la règle se recalcule depuis l'écran ; elle peut être restituée comme indicateur (« taux indiqué par la règle »).
   - Sous (b), la règle lit π_n, que le joueur ne voit pas avant de décider. Pour rétablir la symétrie, il faudrait afficher le prix du tour n avant la décision, ce qui revient à fixer ce prix à la fin du tour n − 1. On change alors l'étiquette des tours et l'on révise M24 sans rien gagner.
   - En multijoueur, un pays non joué sous règle automatique disposerait sous (b) d'une information que le joueur humain n'a pas (point signalé à `jeu`).
3. **Pratique et littérature.**
   - Taylor (1993), *Carnegie-Rochester Conference Series on Public Policy* 39, 195-214, **lu**, p. 202 : « p is the rate of inflation over the previous four quarters ». Et plus bas : « Using the inflation rate over the previous four quarters on the right-hand side of equation (1) indicates that the interest-rate policy rule is written in "real" terms with the lagged inflation rate serving as a proxy for expected inflation ».
   - Orphanides (2001), *AER* 91(4), 964-985, résumé **extrait** : « reliance on the information actually available to policy makers in real time is essential for the analysis of monetary policy rules ».
   - McCallum (1999), *Handbook of Macroeconomics*, vol. 1, ch. 23, 1483-1530. Le résumé de NBER w6016 (**extrait**) cite l'« operationality of rule specifications ». L'idée qu'une règle ne lit que des variables observables à la date de la décision est **citée de mémoire**.
   - (c) est la lecture opérationnelle.
4. **Le délai d'un tour n'est pas neutre pour la stabilité de la règle. La cause principale est pourtant la fenêtre de 12 mois du glissement.**
   - Sous fermeture neutre, (b) et (c) sont identiques. P10 relancé, option M, λ_w = 1 : rayon 0,9068 et une racine unité, pour λ_e = 0,5, 1 et 2, sous les deux lectures. Sous fermeture ancrée : 0,9909 en (c) contre 0,9907 en (b) (λ_e = 0,5).
   - J'ai ajouté à la même maquette une **règle hypothétique** et un canal taux réel → demande autonome (script `m4_regle2.py`, **illustration, pas le fait nouveau de C2**) :
     - règle : r_t − r̄ = r^s_t + a_π(π_lu − π̄), avec r^s_t = r^s_{t−1} + (k/n_a)(π_lu − π̄) ;
     - demande autonome : A·exp(−s(r_t − r̄)) en phase 2 du même tour ;
     - plans indexés sur π^e ; λ_e = λ_w = 1 ; m = 0,6 ; autres hypothèses de `macro` au § 3.0 ;
     - aucun plancher, aucun terme d'activité, aucune crédibilité.

   Rayon spectral (période) :

   | s | a_π | k (par an) | glissement, lecture (c) | glissement, lecture (b) | variation mensuelle annualisée, lue au tour précédent |
   |---|---|---|---|---|---|
   | 1 | 0,5 | 0 | 0,9771 (monotone) | 0,9766 | 0,9787 |
   | 1 | 1,5 | 0 | **1,0056 (21 tours)** | 0,9883 (20 tours) | 0,9659 |
   | 1 | 0,5 | 0,5 | 0,9675 (195 tours) | 0,9671 (198 tours) | 0,9707 (212 tours) |
   | 1 | 1,5 | 0,5 | **1,0127 (21 tours)** | 0,9951 (20 tours) | 0,9734 (422 tours) |
   | 1 | 0,5 | 2 | **1,0231 (30 tours)** | **1,0111 (29 tours)** | 0,9450 (275 tours) |
   | 3 | 1,5 | 0,5 | **1,0967 (17 tours)** | **1,0613 (16 tours)** | **1,3897 (6 tours)** |

   - Pour s = 1, a_π = 1,5, k = 0,5, à λ_e = 0,5 / 1 / 2 : (c) donne 1,0174 / 1,0127 / 1,0074 ; (b) donne 0,9992 / 0,9951 / 0,9907.
   - Ce que j'en lis :
     - le tour de retard déplace la frontière de stabilité ;
     - le retard dominant est la fenêtre du glissement, de 5,5 tours en moyenne : la variation mensuelle stabilise des cas où le glissement explose, sous (b) comme sous (c) ;
     - c'est donc une question de la fiche 8 (mesure lue, coefficients), qui ne justifie pas de déplacer le prix en phase 1.
   - **Clause de réouverture proposée pour M26** : on rouvre la Q1 vers (b) si l'analyse C2 de la fiche 8 montre que le délai d'un tour est déterminant à la calibration retenue. Sous M, ce passage ne serait qu'un réordonnancement, puisque p_n ne lit que l'ouverture. Il demanderait une décision citant M26, M24 et M22.
5. **(a) contre (c).** Les trajectoires sont identiques. Je préfère (c) pour deux raisons :
   - la restitution : l'indice du tour n est le prix du tour n ;
   - (a) tend le piège de T2 (Q6).

   Sur l'empreinte, ma préférence est faible : un registre de n_a + 1 = 13 niveaux plutôt que π_t en variable d'état. Une seule source nominale subsiste, d'où se recalculent le glissement et la variation sur le tour. Le choix revient à `architect`, avec la décision citant M22 et l'ADR 0005, pt 16.

**Q2 — Anticipation consommée.**
- **Oui pour M** : M ne consomme rien (coefficient 0 sur base courante).
- **Oui pour D** : son coefficient est ma règle appliquée part par part. La part retardée (1 − θ, avec θ = λ_p/n_a) reçoit le coefficient 1 sur π^e ; la part courante (θ) reçoit 0.
  - Écart stationnaire calculé : ln p − ln((1 + μ̄)UC) = (1 − θ)[ln(1 + π^e) − ln(1 + π̄)]/(n_a θ). Il est nul sous (G) si C1 tient.
  - **Aucun double compte avec SN.** Le gain d'impact d'une hausse de ln(1 + π^e) sur ln p, rapporté à Δ/n_a, vaut 1,000000 sous D comme sous M. Un choc permanent de π^e avec salaires indexés laisse la marge de D inchangée sur 240 pas (écart 0).
  - L'option A additionne au contraire ϖπ^e et un rappel sur coût courant.
- **Réserve contre D : sa marge stationnaire dépend de C1.**
  - Exemple de la fiche 3 : π^e = 2,2 % pour π̄ = 3 %. On obtient p/[(1 + μ̄)UC] − 1 = −1,227 %, −0,583 % et −0,260 % pour λ_p = 0,6, 1,2 et 2,4. Un échec de C1 à la fiche 8 ferait donc échouer D au critère 4.
  - Sous M, le même échec ne touche pas la marge, seulement U* par SN. **M résiste mieux à un défaut de la fiche 8.**
- **Conséquence pour la suite.** Sous M, π^e n'atteint les prix que par les salaires SN, avec un gain de 1 dans le même tour (W_t en phase 1, UC_t en phase 2, p_t en phase 5).
  - Un levier « indexation légale » au J4 avec un coefficient inférieur à 1 affaiblirait d'autant le canal des anticipations vers les prix.
  - La fiche 8 ne doit ajouter aucun canal direct π^e → p (double compte).

**Q3 — Boucle 5 (e).** Sur la dichotomie, je suis d'accord.
- La partie réelle ne dépend pas de λ_e, et le rythme a une racine unité (P10 relancé). C'est la propriété voulue : une politique accélérationniste à la Friedman-Phelps, conforme à l'intention du mainteneur. Il ne faut pas la « corriger » dans les blocs 3 et 4 (indexation inférieure à 1, ancre sur π̄ dans le prix) : ce serait un second ancrage.

En revanche, je **ne dirais pas « entièrement C2 »**.
- C2 garantit la **valeur** stationnaire π̄ = π*. La **stabilité** du rythme dépend de toute la boucle :
  - la règle : a_π, gain intégral, mesure lue, délai, plancher ;
  - le canal taux → demande des fiches 5, 6 et 9, signe compris (acquis R : « la politique monétaire peut agir à l'envers ») ;
  - la loi d'anticipation : λ_e et crédibilité ;
  - les paramètres des blocs 3 et 4 : λ_w·β, ψ_ξ, λ_μ.
- **Les rayons publiés ne suffisent pas.** Ce sont des entrées nécessaires, mais l'instabilité 4 est l'« estimateur de r* sans ancre ni bande » (faits § 6, R). Le fait nouveau doit porter sur la boucle qui contient cet estimateur, et les rayons publiés ne contiennent ni l'estimateur ni le canal du taux.
- L'illustration de Q1 le montre :
  - k = 2 par an déstabilise (1,0231, période 30 tours) ;
  - k = 0,5 par an est stable (0,9675) mais avec une période d'environ 195 tours, au-delà d'une partie de 60 à 120 tours (point pour `jeu`).
- Le fait nouveau se produit donc à la fiche 8, une fois connue l'élasticité des plans au taux (fiches 5 et 6) : grille × 0,5 et × 2, délai de la lecture retenue, période de la racine dominante comparée à la durée d'une partie.

**Q4 — Lecture des taux.** Oui. M ne contient aucun taux annuel. Le choix repose sur la fiche 3 (g_pr et π^e dans SN), la fiche 8 (cible, π^e) et M24 (f). Je maintiens **(G)**, condition C4 de la fiche 3. La fiche 4 ajoute deux arguments mineurs :
1. **Restitution de la variation sur le tour.** À π̄ = 2 %, l'annualisation géométrique (1 + v)^12 − 1 donne 2,0000 %, l'annualisation linéaire 12v donne 1,9819 %. Sous (L), le joueur verrait deux inflations annuelles. Si la variation est restituée annualisée, elle doit l'être géométriquement.
2. **Exactitude de D.** D n'est exacte que sous (G), ou sous (L) avec un π^e en taux linéaire.

**Q5 — Canal de transmission par la marge.** Acceptable, aux conditions suivantes.
- **Effet transitoire.** Le canal est ancré sur μ̄ : il ne touche ni π̄ ni U*. L'effet durable de la politique monétaire sur l'inflation reste porté par le seul bloc 8.
- **Effet stabilisant.** La boucle 5 (e) est plus amortie : 0,9068 contre 0,9172 pour R.
- **Délais.** Taux du tour n → plans du tour n (si les fiches 5 et 6 lisent i_n en phase 2) → stocks du tour n → ξ_{n+1} → marge → π_{n+1} → lecture par la règle au tour n + 2 sous (c). Il faut au moins 2 tours pour qu'une décision apparaisse dans l'entrée de la règle par ce canal.
- **Statut empirique : contesté.**
  - Nekarda et Ramey, document de travail NBER w19099 (2013), résumé **extrait** : « markups are procyclical conditional on a technology shock. However, we find that they are either procyclical or acyclical conditional on demand shocks. Thus, the textbook NK explanation for the effects of government spending or monetary policy is not supported by the behavior of the markup ». La version *JMCB* (2020) n'a pas été relue par moi.
  - En sens contraire, Barth et Ramey, NBER w7675 (2000), publié dans *NBER Macroeconomics Annual* 16 (2001), résumé **extrait** : après une contraction monétaire, « many industries exhibit periods of falling output and rising price-wage ratios », lu comme un canal de coût.
  - Aucune des deux sources n'établit la forme de M.
- **Absence à déclarer dans la portée.** Le socle n'a pas de canal de coût (UC = W/pr ne contient aucun intérêt). Une hausse de taux ne relève donc jamais les prix par les coûts : le modèle ne reproduit pas l'« énigme des prix » (*price puzzle*).
  - La forme NHUC de Godley et Lavoie (citée de mémoire par `macro`) introduirait ce canal, mais ferait dépendre la part salariale du taux (critère 3 (d)).
  - Un intérêt sur le fonds de roulement introduit par les fiches 6 ou 7 n'entrerait pas dans la base du prix sans révision de M26.
- **Signe hérité.** Le canal par la marge prend le signe de l'effet net du taux sur la demande. Si la fiche 5 a un canal rentier dominant, une hausse de taux relève la demande, baisse les stocks et monte la marge : la marge amplifie un effet pervers. À vérifier aux fiches 5 et 8.
- **Second tour.** La compression des marges réduit les profits non distribués, donc l'investissement et la demande de crédit (fiches 6 et 7). À mesurer à la fiche 7.

**Q6 — Constat T2 sous (a).** C'est un défaut à éliminer, quelle que soit la Q1.
- Valeurs recalculées, β = 2 : U* se déplace de −ln(1 + π̄)/(n_a β), soit −0,0825 point (2 %) et −0,3971 point (10 %) à n_a = 12, et −0,2475 et −1,1914 point à n_a = 4.
- Lecture monétaire : la courbe de long terme n'est plus verticale. Passer de 2 % à 10 % d'inflation achèterait −0,31 point de U* de façon permanente. C'est un arbitrage exploitable par un joueur ou une IA, et il dépend de n_a. Il contredit la propriété de taux naturel sur laquelle repose le cadre de Barro et Gordon (résumé w0807, extrait : « the equilibrium unemployment rate ends up independent of "policy" »), ainsi que la logique de C1 et C2.
- **Remède** : écrire T2 sur le dernier prix connu, p_{t−1}, quelle que soit l'étiquette retenue pour la Q1. C'est la dernière entrée du registre sous (b) et (c), et P_t sous (a).
- **Critère proposé avant l'essai (J3)**, test de propriété du script d'état stationnaire : U* égal à U^eq à 1e−10 près en relatif, pour π̄ ∈ {0 ; 2 % ; 10 %} et n_a ∈ {4 ; 12 ; 52}. Le même contrôle s'étend à la fiche 8 : le taux réel stationnaire de la règle doit être indépendant de π̄ (dates de i et de π appariées).
- Ce constat plaide pour (c).

### 6.2 Avis général sur M, côté monnaie

**Favorable à M**, avec la lecture (c) et les choix du § 5 : base UC, UC en phase 2, terme ξ, aucune anticipation consommée, règle neutre entre (L) et (G).
- **Verticalité de long terme.** p/UC = 1 + μ̄ ne dépend ni de π̄, ni de n_a, ni des vitesses. Le bloc 4 n'apporte aucun second ancrage nominal ; le rythme n'est ancré que par le bloc 8. C'est conforme à l'intention du mainteneur, que C8 demande de reconfirmer.
- **Robustesse à un défaut de C1**, contrairement à D (Q2).
- **Une seule entrée des anticipations**, par les salaires. La chaîne « anticipations → salaires → prix » est lisible et ne comporte aucun double compte.
- **Haute inflation (J6).** M répercute UC en entier à chaque tour, sans `flex`. Gagnon (2009), *QJE* 124(3), 1221-1263, résumé **extrait** : au-delà de 10 à 15 % d'inflation annuelle, « few price decreases are observed and both the frequency and average magnitude are important determinants of inflation ».
  - Une fréquence fixe (λ_p de D) sous-estimerait la répercussion en haute inflation.
  - M ne pose pas ce problème, parce que sa rigidité porte sur la marge, qui est un rapport, et non sur le niveau du prix. C'est un avantage de M sur D pour les régimes de type Cagan.
- **C contre M.** Une règle de taux qui lirait une inflation alternée d'un tour sur l'autre amplifierait l'alternance. C'est un motif monétaire de plus pour écarter C.
- **Aucun désaccord de fond avec `macro`** n'est à décrire en deux positions. J'apporte trois précisions : la stabilité ne relève pas de C2 seule (Q3) ; une clause de réouverture de la Q1 (Q1, point 4) ; le niveau des prix sous C2 (§ 6.3).

### 6.3 Précision à mon avis sur la fiche 3

À la fiche 3 (§ 6.2), j'ai écrit : « le niveau des prix n'est pas ancré, sauf si la fiche 8 retient un terme de niveau des prix ». C'est incomplet.

**L'identité.** Sous C2 en forme intégrale sur le glissement, en logarithmes et sous (G), on a Σ_t(ℓ_t − ℓ*) = Σ_{12 derniers} x − Σ_{12 premiers} x. Ici ℓ_t = ln(P_t/P_{t−12}) et x est l'écart en logarithme du niveau des prix à son sentier tendanciel. Vérification numérique : 7,251e−05 des deux côtés.

**Si r̄ est inchangé après un choc**, r* revient à r̄. La somme des écarts de glissement est alors nulle, et **le niveau des prix revient sur son sentier d'avant le choc**. Les deux formes de C2 sont donc équivalentes aussi sur ce point.

**Si r̄ se déplace durablement de Δr̄**, par exemple après une expansion budgétaire permanente, le niveau reste déplacé de Δr̄/k (n_a = 12) et π revient à π*. Le niveau n'étant pas un rapport, le critère 4 n'est pas en cause.

**Conséquence pour le joueur** (`jeu`) : après un dépassement, la règle automatique produit une période d'inflation sous la cible (dépendance à l'histoire).

L'énoncé de la fiche 4 (« le bloc ne fixe pas le niveau ») reste exact : c'est le bloc 8 qui le fixerait.

### 6.4 Points transmis à la fiche 8, en complément de C1 à C8

- **C9 — Information de la règle.** La règle a la même information que le joueur : au tour n, π_{n−1} (glissement restitué), U_{n−1} et π^e d'ouverture. Sa prescription est restituée.
- **C10 — Contenu du fait nouveau de C2.** Il inclut :
  - le délai de lecture de la Q1 retenue (1 tour sous (c)) ;
  - la mesure lue (le glissement est le retard dominant) ;
  - le canal taux → demande des fiches 5, 6 et 9, avec son signe ;
  - la loi d'anticipation ;
  - ψ_ξ et λ_μ de M ;
  - le plancher ;
  - la grille × 0,5 et × 2 ;
  - la période de la racine dominante, comparée à une partie.

  L'illustration du § 6.1 (Q1, point 4) contient des cas explosifs. La clause de réouverture de la Q1 y est attachée.
- **C11 — Retour du niveau des prix sous C2** (§ 6.3) : à déclarer et à soumettre à `jeu`.
- **C12 — Phase de formation de π^e.** La condition de Barro et Gordon s'écrit : la π^e consommée au tour n ne lit aucun levier du tour n. Sous (c), le délai prix → anticipation → salaire dépend de la formation :
  - 2 tours si π^e est formée en phase 1 du tour n à partir de π_{n−1} et lue au tour n + 1 ;
  - 1 tour si elle est formée en tête de phase 1, avant la lecture des leviers, et lue ensuite par le bloc 3 (bloc 8 en deux temps : anticipations, puis règle) ;
  - 1 tour aussi si elle est formée après la phase 5 du tour n − 1, ce qui révise `tab:phases`.

  Ce choix revient à la fiche 8 ; il ne conditionne pas M26.
- **C13 — Ni canal direct π^e → p, ni canal de coût au socle.** Aucun canal direct, ni dans le bloc 8 ni dans le bloc 4 sous M. Un canal de coût du taux au socle demanderait de réviser M26.

### 6.5 Points signalés à `jeu` (non tranchés)

- Symétrie d'information entre la règle automatique et le joueur ; restitution du « taux indiqué par la règle ».
- Cycles très longs (environ 200 tours) sous une règle intégrale lente ; retour du niveau des prix.
- Variation sur le tour annualisée géométriquement, si elle est restituée annualisée.
- Lisibilité de « resserrement → marges comprimées » ; le modèle ne reproduit pas l'« énigme des prix ».

## 7. Avis de `jeu`

*`jeu`, 03/10/2026 (issue #40, jalon 2), sur la fiche à l'état `ff3f97d` (branche `claude/j1-economie-reelle`, PR #43). Réponses aux huit questions de `macro`.*

**Chiffres.** Aucun moteur n'existe encore. J'ai prolongé ma maquette de la fiche 3 ; elle n'importe aucun script `p4_*`.
- **Ce qu'elle contient** : le socle N1 à N7 en niveaux, l'emploi R, le salaire SN (λ_w = 1, β = 2, terme de niveau sur W_{t−1}/p_{t−1}), les règles R, C, M, T et D, et un prix administré optionnel. Les plans de demande sont en u.m. au prix p_{t−1}, et le volume servi vaut plan/p_t.
- **Hypothèses** : g = 0, π̄ = 0 (grandeurs rapportées au sentier), pr = 1, et les valeurs du § 3.0.
- **Exécution** le 03/10/2026, hors dépôt, par `uv run --no-project python jeu_prix1.py` à `jeu_prix9.py`.

- **Contrôle de la maquette.** Elle reproduit l'exemple daté de M (§ 3.L) à la troisième décimale, sur les neuf tours, pour la production, U, W, p, la variation du prix sur le tour, la marge, W/(p·pr) et ξ. Elle reproduit de même :
  - la comparaison R, C, T, D (prix et marge) ;
  - le pic de marge de M : +0,12 et +0,60 point à m = 0 ; +0,23 et +1,13 point à m = 0,6 ;
  - le creux de part salariale : −0,15 et −0,71 point ;
  - la marge de D : −0,126 point au tour 16.
- **Convention à déclarer au § 3.L, sans erreur.** Les colonnes de glissement et le tableau des ampleurs sont mesurés à π̄ = 2 %. L'écart de glissement y vaut donc (1 + π̄) fois l'écart du niveau des prix sur 12 tours. Ma maquette, à π̄ = 0, donne exactement les valeurs publiées divisées par 1,02. Exemples : 0,257 contre 0,262 au tour 9 ; pic de M de 0,48 / 2,41 et 0,84 / 4,26 point contre 0,49 / 2,46 et 0,86 / 4,34. C'est sans effet sur les verdicts.
- **Constat complémentaire 1 : C alterne déjà à la calibration.**
  - Après une impulsion de demande d'un seul tour (G +1 %), la variation mensuelle du prix sous C change de signe 7 fois (m = 0) et 11 fois (m = 0,6) entre les tours 2 et 13 : +0,096, −0,061, +0,050, −0,030, +0,026 point.
  - Sous M, D, T et R, elle change de signe au plus une fois.
  - L'écart de **niveau** du prix ne change de signe sous aucune règle. Le test de la réserve 3 du § 5, écrit sur l'écart du prix, ne détecterait donc pas cette alternance.
  - Pour un choc de G +5 % aux tours 1 à 12 (m = 0,6), le rythme mensuel annualisé sous C passe de 5,9 % à 2,1 %, puis 5,2 % et 3,3 %, sans aucune décision du joueur.
- **Constat complémentaire 2 : le prix administré, tel que noté en Q10, domine dans la maquette.**
  - Scénario : M, relance de G +5 % aux tours 1 à 18, m = 0,6, prix gelé sur son sentier aux tours 1 à 18, puis levé.
  - Avec gel : niveau des prix au tour 120 de −0,08 % contre +5,19 % sans gel ; production cumulée sur les tours 1 à 120 de +45,1 contre +32,1 %·tour ; pic du glissement lu de 2,74 contre 4,98 points.
  - Même sens sous R (3,58 contre 5,21 % ; 36,1 contre 32,1) et sous D (1,19 contre 3,35 % ; 42,0 contre 36,6).
  - Le seul coût visible est une marge comprimée de 4,3 points, sans conséquence tant que les fiches 5, 6, 8 et 9 ne sont pas branchées.
- **Constat complémentaire 3 : correction de mon avis sur la fiche 3 (question 7).** Voir plus bas, « Correction de mon avis sur la fiche 3 ».

**Question ludique de la fiche.** Le bloc n'ouvre aucun levier. Il fixe ce que le joueur paie pour ses relances (l'inflation) et qui y gagne (le partage entre salaires et profits). La question est donc la suivante : le coût d'une relance arrive-t-il avec un délai, une ampleur et une explication que le joueur peut relier à sa décision, avec des gagnants et des perdants (O2), et sans prix qui « vibrent » ?

### 7.A et 7.B Options A et B (brièvement)

Verdict : **à revoir**. Leur état stationnaire dépend des vitesses (critère 4). Le joueur verrait donc la marge dériver avant toute décision, et l'indicateur z serait non nul en régime normal, donc illisible. B y ajoute des bornes à seuil libre, un état caché et des prix qui montent en récession. Je n'ajoute rien au § 5.

### 7.R Option R — référence sans retard

- **Ce que voit le joueur.** L'inflation ne vient que des salaires : le glissement lu culmine au tour 16 (+0,36 point pour G +1 %, m = 0, maquette). La marge et la part salariale ne bougent jamais.
- **Risque.** C'est le défaut que j'ai relevé à la fiche 3 (question 8) : une relance n'a aucun effet de répartition. La demande n'atteint le prix que par les salaires, avec 2 tours de délai.
- **Verdict : lisible, mais pauvre.** R reste la bonne référence (`docs/exigences.md` § 2.7).

### 7.C Option C — marge instantanée

- **Ce que voit le joueur.** La marge saute dès le tour 2 (+0,12 point). La réponse du glissement est la plus rapide (≥ 0,1 point au tour 4 pour G +1 %).
- **Risques.**
  - *Comportement contre-intuitif non explicable.* La variation mensuelle alterne d'un tour sur l'autre, même à la calibration (constat 1). Aux vitesses de la fiche 2 × 2, l'alternance devient explosive : ±1,7 à 2,4 points par mois aux tours 24 à 27 et prix +12,3 % au tour 60, à partir d'une impulsion de G +1 % sur un tour. À ψ × 2 : ±12 à 19 points par mois et prix +143 %.
  - La robustesse exige ψ ≤ 0,26, et C perd alors l'effet de demande qui la justifiait.
- **Verdict : à revoir** (question 7).

### 7.M Option M — marge à ajustement partiel vers une cible sensible aux stocks

- **Ce que voit le joueur**, pour une relance au tour n :
  - les stocks baissent au tour n (fiche 2), puis la marge monte dès le tour n + 1 ;
  - les salaires suivent quelques tours plus tard, et le prix les répercute le tour même ;
  - la marge se replie ensuite, sous son niveau normal, pendant que le coût unitaire porte encore l'inflation.
- **La décomposition de l'inflation** sur 12 tours (G +5 %, m = 0,6, contributions en points) raconte cette histoire :

  | Tour | Coût unitaire | Marge | Glissement |
  |---|---|---|---|
  | 6 | +0,56 | +0,40 | 0,97 |
  | 13 | +2,81 | +0,90 | 3,77 |
  | 18 | +3,67 | +0,18 | 3,92 |
  | 24 | +2,36 | −0,87 | 1,50 |
  | 30 | +0,44 | −0,93 | −0,49 |

  « D'abord les profits, puis les salaires » : il y a des gagnants et des perdants qui se succèdent dans le temps (O2), et une matière directe pour le soutien politique (J7).
- **Délai de perception** (premier tour où l'écart du glissement lu atteint 0,1 ou 0,2 point) : tours 6 et 8 pour G +1 % ; tours 4 et 5 pour G +5 %. Le glissement culmine aux tours 15 à 17, **après la fin de la relance** : le coût arrive après le bénéfice, ce qui est la bonne structure de tentation.
- **Signal précurseur.** Le rythme mensuel annualisé culmine au tour 13 (+5,16 points pour G +5 %, m = 0,6) et devient négatif au tour 21, quand le glissement sur 12 tours vaut encore +2,88 points. Il annonce le retournement de 4 à 8 tours, à condition d'être affiché (conditions de restitution, point 2).
- **Risques.**
  - *Réponse imperceptible pour les petits chocs* : pour G +1 %, la marge passe de 25,0 à 25,1 % à une décimale. Elle est nette pour G +5 % (25,0 → 25,6 %).
  - Aucune alternance : au plus un changement de signe de la variation mensuelle après une impulsion, même aux vitesses × 2.
- **Verdict : lisible**, sous les conditions de restitution 1 à 9.

### 7.T Option T — variante en taux d'utilisation

- **Ce que voit le joueur.** Même dynamique que M, un peu plus faible : pic de +0,43 point pour G +1 %, et marge au plus +0,07 point.
- **Intérêt.** C'est la seule voie, dans cette fiche, vers un coût du sous-investissement perçu dans les prix (condition 7 de la fiche 2, #37).
- **Risque.** Si tu ne revient pas vers t̄u, la marge et U* se déplacent de façon permanente (+1,25 point de U* pour Δtu = +0,05). Ce serait un coût lisible, mais qui dépend d'une règle d'investissement qui n'existe pas encore (fiche 6).
- **Verdict : à clarifier** à la fiche 6 (question 5).

### 7.D Option D — prix lents indexés sur l'anticipation

- **Ce que voit le joueur.** Une inflation plus lente et plus lisse : pic de +0,24 point pour G +1 % (m = 0), seuil de 0,2 point atteint seulement au tour 13. La marge baisse en expansion (−0,13 point) : la relance profite d'abord aux salariés. Les gagnants et les perdants sont inversés par rapport à M, ce qui est lisible aussi.
- **Risques.**
  - Le prix réagit à π^e. Si la fiche 8 permettait qu'une annonce déplace π^e le tour même, ce serait le levier instantané par la communication que j'ai écarté à la fiche 3 (question 5). La lecture (a) de l'anticipation (un tour) le neutralise.
  - Sous (L), l'état stationnaire dépend des vitesses.
- **Verdict : lisible sous (G)** et sous la lecture (a) de l'anticipation. C'est une alternative acceptable.

### Réponses aux huit questions de `macro`

1. **Règle de marge : M.**
   - M est la seule règle qui donne à la fois un coût salarial répercuté le tour même (la marge ne bouge pas sous un pur choc de salaire) et une marge qui répond progressivement à la tension, sans alternance.
   - Elle remplit le souhait que j'avais formulé à la fiche 3 (question 8) : le salaire réel devient parlant (−0,15 / −0,71 point de part salariale au plus bas, m = 0,6).
   - C saute et vibre (question 7). D lisse mais inverse la cyclicité, et la cyclicité de la marge est un fait contesté que je ne juge pas. R fige le partage.
2. **Délais : ils conviennent.**
   - Salaire → prix en 0 tour : la contrepartie (marge inchangée) est visible le tour même, et le salaire n'est pas un levier du joueur.
   - Demande → prix en 1 tour, par ξ à l'ouverture : c'est la grammaire uniforme de la fiche 3, une décision du tour n agit sur le secteur privé au tour n + 1 au plus tôt.
   - Prix → règle de taux en 1 tour sous (c) : voir la question 3.
   - Je distingue le **délai mécanique** (1 tour) du **délai perçu** (4 à 8 tours avant 0,1 à 0,2 point de glissement) ; le second doit figurer dans la documentation des leviers au J4.
3. **Indice décalé : (c) préférée, (a) acceptable sous conditions, (b) déconseillée.**
   - (a) et (c) donnent la même trajectoire (constat 1 de 3.N-1). La différence est **uniquement ce que voit le joueur**.
   - Sous (a), l'« indice du tour n » est le prix du tour n − 1. La marge, la part salariale, la décomposition et la dépense exécutée p·G^vol (fiche 2) sont pourtant calculées sur p_n. Le joueur aurait alors deux séries de prix décalées d'un tour pour un bien unique, et une décomposition dont la somme ne serait pas la variation de l'indice affiché.
   - Sous (c), tout ce qui est affiché porte le prix du tour, et le décalage n'apparaît que dans la lecture par les règles, où il est déclaré.
   - Argument décisif contre (b) : la règle de taux lirait π_n au tour n, une information que le joueur n'avait pas quand il a décidé pour ce tour. Une règle automatique serait alors mieux informée qu'un joueur qui fixe le taux lui-même, par construction et non par mérite économique : c'est une stratégie dominante de délégation. Sous (c), la règle et le joueur voient la même chose.
   - Si (a) est retenue : la série principale affichée est p_n, et l'indice porte la mention « indice publié, prix du tour précédent, lu par la banque centrale et les salaires ».
4. **Indicateurs : garder la marge, une seule part salariale, la décomposition et ξ ; ne pas afficher W/(p·pr) séparément.**
   - Sous J = 1, W/(p·pr) = UC/p = 1/(1 + marge) par définition. C'est la même information que la marge, comme le sureffectif et la productivité apparente à la fiche 3 (question 2).
   - Je garde la part salariale ΣWB/ΣVA sur 12 tours, avec son niveau normal dans **la même définition** (0,7989 à π̄ = 2 %, et non 0,8), comme le demande ma condition 2 de la fiche 3. L'écart entre W/(p·pr) et WB/VA reste publié dans la documentation, pas au tableau de bord.
   - ξ et les stocks en mois de ventes (fiche 2) disent presque la même chose, avec des signes opposés : au tour 12, −2,42 % pour les stocks, +2,56 % pour ξ ; le signe est cohérent à tous les tours sauf aux deux tours de bascule (16 et 62). Je garde ξ, puisque c'est la variable que lit la règle, sous le nom « tension sur les stocks » (positive quand les stocks sont sous leur niveau visé), affichée à côté de la marge. Sa définition dit son lien aux stocks en mois.
5. **Taux d'utilisation : décider à la fiche 6.**
   - T n'est pas prête : son ancrage dépend de la fiche 6, et le coût du sous-investissement peut aussi venir de la capacité elle-même (#37).
   - D'ici M28, tu ne figure pas dans le panneau des prix.
   - Au socle, tu et ξ bougent ensemble dans un choc de demande, si bien que tu n'induit pas le joueur en erreur. Il le ferait dans un choc d'offre.
   - Si M28 ne lui donne aucune conséquence, tu sort de la restitution (condition 4 de la fiche 2, inchangée).
6. **Seuil du critère 10 (d)** : **0,2 point pour G +1 %, 1,0 point pour G +5 %**. Le détail est plus bas.
7. **Alternance de C : rédhibitoire.**
   - Explosive, elle casse la partie en moins de 60 tours.
   - Amortie, elle reste inexplicable : aucun récit économique ne justifie qu'un bien unique monte, baisse et remonte d'un mois sur l'autre. Elle trompe aussi le joueur (ou une règle) qui lit le rythme mensuel.
   - Elle existe à la calibration (constat 1).
   - Je propose d'étendre la réserve 3 du § 5 : « après une impulsion de demande de 1 % sur un tour, **la variation mensuelle du prix** ne change pas de signe plus de deux fois en 12 tours », en plus de l'écart du prix. M tient (0 ou 1), C échoue (7 et 11).
8. **Levée d'un prix administré : lisible sous M, à condition de restituer la marge comprimée et que le gel ne soit pas gratuit.**
   - Mesure : M, gel aux tours 1 à 18 pendant une relance de G +5 %, levée au tour 19.
     - Inflation corrective de +0,75, +0,66, +0,48, +0,35 et +0,24 point par mois aux tours 19 à 23, sans saut.
     - L'écart de marge **au cas sans gel** se résorbe avec une demi-vie de 7 tours, contre 6,58 tours en théorie : l'affirmation du § 3.L tient, mesurée contre ce contrefactuel.
   - Contre μ̄, ce que le joueur voit en réalité, la marge reste à −2,13 points 12 tours après la levée quand la relance s'arrête au même moment : la fin de la relance accumule des stocks (ξ < 0). La décomposition doit l'expliquer.
   - Sous R, la levée fait un saut de 3,83 points en un mois. Sous C, +5,58 points puis une alternance (−2,42, +1,77, −1,27…).
   - La marge comprimée pendant le gel (−4,3 points) est un **bon signal précurseur** de l'inflation corrective (inflation réprimée de la v1.5).
   - Mais le gel domine dans la maquette (constat 2) : moins d'inflation, un niveau des prix durablement plus bas et plus de production, sans coût visible. Le levier ne doit pas s'ouvrir avant que la marge comprimée ait un coût, par les profits distribués (fiche 5), l'investissement (fiche 6) ou le rationnement. C'est une condition pour Q10 (J4, J7), non un défaut de M.

### Indicateurs du tour (critère 10 (a))

| Indicateur | Verdict | Motif ou point à clarifier |
|---|---|---|
| Prix du tour, indice base 100 | **lisible** sous (c) ; **à clarifier** sous (a) | Sous (a), p_n reste la série principale, et l'indice décalé porte la mention « publié, prix du tour précédent » (question 3) |
| Glissement annuel (12 tours) | **lisible** | Niveau normal dans la définition exacte : π̄ sous (G), le taux effectif publié sous (L) |
| Variation du prix sur le tour | **à clarifier** | L'afficher aussi en rythme annualisé, (1 + x)^12 − 1, comme grandeur de restitution qu'aucune règle ne lit. C'est le signal précurseur du retournement (7.M) ; brute, 0,04 point par mois ne se compare pas à 2 % par an |
| Marge (au tour ; moyenne sur 12 tours) | **lisible** | Niveau normal μ̄ affiché |
| Part salariale W/(p·pr) | **à revoir comme ligne distincte** | Égale à 1/(1 + marge) sous J = 1 : même information que la marge |
| Part salariale ΣWB/ΣVA (12 tours) | **à clarifier** | Niveau normal dans la même définition (0,7989 à π̄ = 2 %), comme à la fiche 3 |
| Décomposition de l'inflation (12 tours) | **à clarifier** | Contributions exactement additives au glissement affiché : parts des logarithmes appliquées au glissement, l'écart croissant avec l'inflation. C'est l'indicateur qui dit qui gagne |
| ξ, « tension sur les stocks » | **à clarifier** | Positive quand les stocks sont sous le niveau visé ; sa définition dit son lien aux stocks en mois (fiche 2), de signe opposé et d'ampleur voisine |
| Taux d'utilisation | **hors du panneau des prix** | Décision à M28 (question 5) |

### Seuil proposé au mainteneur (critère 10 (d))

- **Grandeur** : pic, sur les tours 1 à 36, de l'écart du glissement annuel de l'indice (P_t/P_{t−12} − 1, fenêtre de 12 tours) **lu par la règle de taux**, par rapport au sentier sans choc. Unité : point de pourcentage ; π̄ du scénario déclaré, l'écart étant multiplié par 1 + π̄.
- **Scénario** : dépense publique +1 % et +5 % du flux mensuel aux tours 1 à 12, part de G de 20 % (hypothèse), π^e = π̄ exogène, depuis l'état initial résolu.
- **Seuil** : **au moins 0,2 point pour +1 %**, **au moins 1,0 point pour +5 %**.
- **Calibration visée** : la calibration proposée. Au stade de la fiche, avec m = 0, le cas prudent ; au J3 et au J4, avec le m effectif des fiches 5 et 9. Aux vitesses × 0,5 et × 2, les valeurs sont publiées sans être exigées.
- **Motifs** :
  - le glissement est affiché à une décimale : 0,2 point en fait deux crans, une hausse que le joueur voit (2,0 → 2,2 %) ;
  - 0,2 point est aussi la bande du test zéro pour le glissement (critère 6), si bien qu'une relance de 1 % se distingue de la dérive tolérée de la référence ;
  - la réponse est quasi linéaire : 1,0 point est le même seuil rapporté au choc de +5 %, et il fait passer le chiffre des unités (2 → 3 %).
- **Transparence.** Je propose ce seuil après avoir lu les ampleurs du § 3.L. Il est fondé sur l'affichage et sur le test zéro, non sur le classement des options. Il ne départage d'ailleurs pas les options nouvelles à m = 0 :

  | Option | +1 % | +5 % |
  |---|---|---|
  | M | 0,49 | 2,46 |
  | R | 0,37 | 1,85 |
  | C | 0,54 | 2,71 |
  | T | 0,44 | 2,20 |
  | D | 0,25 | 1,24 |

  Son rôle est de protéger contre une calibration du J3 qui rendrait la relance muette.
- **Robustesse sous M** (+1 %, m = 0, maquette à π̄ = 0) : 0,30 à λ_w × 0,5, 0,42 à ψ × 0,5, 0,77 à λ_w × 2. L'ampleur dépend d'abord de λ_w, donc de la fiche 3 : le critère porte sur la paire des fiches 3 et 4.
- **À surveiller au J4, sans seuil haut proposé.** Avec m = 0,6 et λ_w × 2, une relance de +5 % porte le glissement à +6,5 points. La réaction de la banque centrale (fiche 8) n'est pas encore modélisée.

### Préférence motivée

- **Ma préférence va à M**, comme celle de `macro`.
  - **Mes motifs propres** :
    - une histoire de l'inflation en deux temps (profits, puis salaires), restituée par la décomposition ;
    - une contrepartie visible le tour même (stocks, puis marge) ;
    - un signal précurseur (rythme mensuel) ;
    - aucune alternance.
  - **Les motifs de `macro`**, que je ne juge pas : critères 3, 4 et 5, et aucune borne.
- **Classement** : M > D > R > C > B > A. T est hors classement, comme variante de M à décider à la fiche 6. Je place R au-dessus de C : l'alternance de C est rédhibitoire, alors que R n'est que pauvre.
- **Accords et réserves sur les lectures soumises au § 5** :
  - (a) Q1 : (c) préférée, (a) acceptable sous la mention de la question 3, (b) déconseillée (asymétrie d'information entre la règle et le joueur) ;
  - (b) M plutôt que C : accord ;
  - (c) M ou D : M, D restant acceptable sous (G) et sous la lecture (a) de l'anticipation. Le signe de la cyclicité est un fait contesté qui relève de `macro` ;
  - (d) T à la fiche 6 : accord ;
  - (e) (w1) au socle : accord ; (w2) au J4 : **à réexaminer** (correction ci-dessous) ;
  - lecture des taux annuels : (G), comme à la fiche 3 (question 10).
- **Coût en fidélité** : je ne demande aucun écart à la littérature. Le rythme mensuel annualisé et l'extension du test d'alternance sont des choix de restitution et d'essai.

### Correction de mon avis sur la fiche 3 (question 7)

- À la fiche 3, j'ai écrit qu'un levier sur la norme ω* (lecture (w2)) offrait « une part salariale plus haute contre un chômage d'équilibre plus haut ». **C'est faux sous toute règle de prix où le bloc 4 ancre μ̄** (R, C, M, T).
- Mesure : ω* passe de 0,80 à 0,81 dès le tour 1, avec m = 0,6 et sans banque centrale.
  - Sous M et sous R, W/(p·pr) vaut 0,8000 au tour 240 : le salaire est répercuté le tour même.
  - Le conflit devient une inflation supplémentaire permanente de 0,894 point par an. Prévision par λ_w(ln(ω*/ω̄) − β(U − U^eq)) : 0,890 point.
  - U finit à 5,176 % ; si la banque centrale tenait la demande, il irait vers U* = 5,621 % (3.N-8).
  - Sous D, la part salariale gagne 0,35 point, mais seulement parce que la marge traîne derrière une inflation supérieure à π^e.
- **Conséquence pour le J4.** Sous M, le levier ω* n'a pas de gagnant durable : il est dominé. Un levier de répartition devrait agir sur μ̄ (politique de la concurrence, marges réglementées). Une baisse de μ̄ abaisserait alors U* sous (w2) : il lui faut un coût perceptible (profits, puis investissement à la fiche 6), sinon elle devient dominante. C'est une question de fond pour `macro` et le mainteneur au J4.

### Conditions demandées au § 9 (restitution et essais)

1. **Lecture (c)** : l'indice restitué est le prix du tour. Sous (a), p_n reste la série principale, et l'indice porte la mention « publié, prix du tour précédent, lu par la banque centrale et les salaires ».
2. **Variation du prix sur le tour**, brute et en rythme annualisé ((1 + x)^12 − 1), comme grandeur de restitution qu'aucune règle ne lit.
3. **Une seule part salariale au tableau de bord**, ΣWB/ΣVA sur 12 tours, avec son niveau normal dans la même définition. W/(p·pr) n'apparaît pas comme ligne distincte de la marge.
4. **Marge** (au tour et en moyenne sur 12 tours), avec μ̄ ; **décomposition de l'inflation** en contributions additives au glissement affiché.
5. **ξ** restitué sous le nom « tension sur les stocks », à côté de la marge ; sa définition dit son lien aux stocks en mois.
6. **Niveaux normaux** publiés par le script d'état stationnaire, dans la définition exacte de chaque indicateur : μ̄, part salariale sur 12 tours, π̄ ou le taux effectif.
7. **Test d'alternance** (réserve 3 du § 5, étendue) : après une impulsion de demande de 1 % sur un tour, ni l'écart du prix ni sa variation mensuelle ne changent de signe plus de deux fois en 12 tours.
8. **Scénario O2 au J4** avec le seuil du critère 10 (d) ci-dessus. On publie aussi le délai perçu (premier tour à 0,1 et à 0,2 point) et la décomposition.
9. **Prix administré (Q10, J4 et J7)** : avant d'ouvrir le levier, un scénario apparié gel contre sans gel, écrit avant l'essai, montre un coût perceptible du gel (profits, investissement, rationnement). Sinon le levier n'est pas ouvert. La marge comprimée est restituée pendant le gel comme signal de l'inflation corrective.
10. **Taux d'utilisation** : hors du panneau des prix jusqu'à M28 ; condition 4 de la fiche 2 inchangée.

## 8. Décision du mainteneur

- **Numéro** : M26 (reporté dans `docs/feuille-de-route.md`, § 4), prise le même jour que M25 (fiche 3), décisions par paires.
- **Date** : 03/10/2026.
- **Option retenue** : **M**, prix égal au coût unitaire UC majoré d'une marge rappelée vers la marge normale μ̄ avec un terme de stocks ξ. Choix du § 5 :
  - base de coût UC (Q3) ; UC écrit par le bloc 2 **en phase 2** (Q2) ;
  - terme de demande ξ (Q4) ; aucune anticipation consommée (Q6) ;
  - partage ancré par μ̄, avec (w1) à la fiche 3 (Q9) ;
  - aucun terme en taux d'utilisation à M26 : la variante T est transmise à la fiche 6, à décider au plus tard à M28 (Q5, #37) ;
  - prix administrés renvoyés au J4 et au J7 (Q10), sous la condition de `jeu` (§ 7, condition 9).
- **Phase de P_t (Q1, #24)** : lecture **(c)**, l'indice est le prix du tour et les règles le lisent au tour suivant. Décision citant M22 et l'ADR 0005, pt 16, consignée par ADR ; la forme (registre de 13 niveaux ou glissement porté en variable d'état) est fixée dans l'ADR. **Clause de réouverture** (avis de `monnaie`, § 6.1, Q1, point 4) : la Q1 est rouverte vers (b) si l'analyse de stabilité de la fiche 8 (condition C10) montre que le délai d'un tour est déterminant à la calibration retenue ; décision citant M26, M24 et M22.
- **Lecture commune des taux annuels** : (G), décidée avec M25 ; la règle M y est neutre.
- **Bande commune du test zéro sur la part salariale** : centrée sur la valeur résolue de ΣWB/ΣVA sur 12 tours (décision commune avec M25).
- **Motifs** : recommandation concordante de `macro` (§ 5), `monnaie` (§ 6) et `jeu` (§ 7). Motifs dans ses propres mots : à compléter par le mainteneur s'il le souhaite.
- **Conditions et réserves** : les réserves du § 5 avec leurs seuils écrits avant l'essai, dont le test d'alternance **étendu à la variation mensuelle du prix** (`jeu`, § 7, condition 7) ; les conditions de restitution de `jeu` (§ 7) ; les conditions C9 à C13 transmises à la fiche 8 (§ 6.4) ; seuil du critère 10 (d) proposé par `jeu` (0,2 point pour +1 %, 1,0 point pour +5 %), à confirmer avant le J4.
- **Ce qui est écarté et pourquoi** : A et B (critères 4, 7 et 11 ; B viole λ ≤ n_a et a un état caché) ; C, stable à la calibration mais à variation mensuelle alternée et explosive dès que les vitesses doublent ; D, alternative acceptable mais sensible à un défaut des anticipations (C1) et à marge contracyclique (fait contesté) ; R, gardée comme référence ; coût complet et marge sur cm (critère 3 (d)) ; lectures (a) et (b) de P_t.
- **Remesure P1** : proposée (§ 5), non lancée ; elle ne change pas la décision.
- **Issues liées**, créées sur accord du mainteneur : prix administrés et coût de la marge comprimée ; levier de répartition au J4.

## 9. Conséquences de la décision

*Rédigé par `macro` (expert pilote), 03/10/2026, d'après M26 (§ 8), M25 (fiche 3, § 8) et la lecture commune (G). La règle M ne contient aucun taux annuel : (G) y est neutre (§ 3.N-6), et les chiffres du § 3, instruits sous (G), restent valables.*

### 9.1 Labels d'équation

**Au jalon J1, aucun label** (#40, jalon 4) : encadrés `proposee` citant M26. **Labels à créer au J3**, avec `src/nations/blocs/prix.py` (radical `prix`).

| Label | Ce que l'équation détermine | Équation | Statut | Provenance | Couche |
|---|---|---|---|---|---|
| `eq:prix-tension-stocks` | tension sur les stocks ξ_t, phase 5 | ξ_t = 1 − IN^vol_t/IN^vol*_t, où IN^vol*_t est lu dans N2 (phase 2, bloc 2) **sans être recalculé** (localité) | définition | M26, Q4 ; § 3.N-4 | `blocs/` |
| `eq:prix-marge` | marge en logarithme μ̃_t, phase 5 | μ̃_t = (1 − λ_μ/n_a) ln(p_{t−1}/UC_{t−1}) + (λ_μ/n_a)[ln(1 + μ̄) + ψ_ξ ξ_t] | approchée (ajustement partiel) ; choix de conception (cible) | M26, option M ; construction du projet, sans source lue pour cette forme exacte | `blocs/` |
| `eq:prix-prix-du-pas` | prix du pas p_t, phase 5, premier bloc | ln p_t = ln UC_t + μ̃_t | dérivée | M26, Q3 (base UC) | `blocs/` |
| `eq:prix-indice` | indice des prix P_t | P_t ≡ p_t (J = 1), arrêté en phase 5 et lu en phase 1 du pas suivant | choix de conception | M26, lecture (c) de la Q1 ; ADR | `blocs/` ou `moteur/` |
| `eq:prix-glissement` | glissement annuel π_t | π_t = P_t/P_{t−n_a} − 1, mesuré, jamais converti | dérivée | M22 ; M26, lecture (c) | `blocs/` ou `moteur/` |

- **Radical et propriétaire de `eq:prix-indice` et `eq:prix-glissement`** : à fixer par l'ADR de la lecture (c).
  - Sous un registre de 13 niveaux tenu par le moteur, le radical serait `moteur` et π serait calculé par une fonction unique, lue par les blocs 3 et 8.
  - Sous un glissement porté en variable d'état, le bloc 4 l'écrirait en phase 5 avec le radical `prix`.
  - L'équation `equation*` π_t = P_t/P_{t−n_a} − 1 de `sec:cadre-calendrier` (l. 201) devient alors un renvoi.
- **Option d'implémentation** (avec la fiche 3, § 9.1) : porter μ̃_t en variable d'état du bloc 4. La marge d'ouverture μ̃_{t−1} est alors lue par le bloc 4 et par le bloc 3 (ω_{t−1} = exp(−μ̃_{t−1})), sans recalculer pr_{t−1}. Une variable d'état de plus, trajectoires identiques. Choix de `coder`, visa de `macro`.
- La marge restituée, la part salariale, la décomposition et la variation annualisée relèvent de la couche `observation/` : sans label.

### 9.2 Paramètres

| Symbole | Nom proposé | Valeur | Unité | Source | Équation |
|---|---|---|---|---|---|
| μ̄ | `marge_normale` | 0,25 (hypothèse de l'instruction ; calée au J3 sur la part salariale, avec O1) | fraction de UC | M26 ; choix de conception | `eq:prix-marge` ; lue par le bloc 3 (w1) |
| λ_μ | `vitesse_marge` | 1,2 (indicative ; non sourcée, réserve 4) | par an, λ_μ ≤ n_a | M26 ; ordre de grandeur de la fréquence de révision des prix (Nakamura et Steinsson, extrait, non établi pour une marge) | `eq:prix-marge` |
| ψ_ξ | `sensibilite_marge_stocks` | 0,5 (indicative ; non sourcée, réserve 4) | sans dimension | M26 ; signe procyclique après un choc de demande (Nekarda et Ramey, extrait ; fait contesté) | `eq:prix-marge` |

**Conditions déclarées, jamais écrêtées** :
- λ_μ ≤ n_a ;
- IN^vol*_t > 0, vraie si v^e > 0 (d > 0 ou λ_v < n_a) ;
- ψ_ξ ≥ 0.

Domaine de stabilité : le § 3.N-9 ne trouve d'instabilité de M qu'à ψ_ξ ≥ 10 à la calibration et à ψ_ξ ≥ 4,875 aux vitesses de la fiche 2 × 2. Il se revérifie au J3 (réserve 3).

**Ce qui n'est pas un paramètre** : π^e (aucune anticipation consommée, C13) ; t̄u (variante T, M28) ; la marge stationnaire (égale à μ̄).

### 9.3 Ce qui reste paramétrable après la décision

**Sans rouvrir M26** : μ̄, λ_μ et ψ_ξ, sur des sources lues (réserve 4).

**Par une décision M-m citant M26** :
- **variante T** : terme ψ_tu(tu − t̄u) dans la cible, t̄u lu à source unique dans la fiche 6, au plus tard à M28 (#37) ;
- **clause de réouverture** de la Q1 vers (b) si l'analyse C10 de la fiche 8 montre que le délai d'un tour est déterminant à la calibration retenue : décision citant M26, M24 et M22. Sous M, ce serait un réordonnancement seul, p_n ne lisant que l'ouverture ;
- prix administrés (J4, J7), sous la condition 9 de `jeu` ;
- une vitesse modulée par l'inflation (J6) ;
- un canal de coût (intérêt dans la base, NHUC) ou un canal direct π^e → p (C13) ;
- un levier de répartition agissant sur μ̄ (J4 ; correction de `jeu`).

### 9.4 Interfaces

| Phase | Le bloc 4 lit | Le bloc 4 écrit |
|---|---|---|
| 1 | rien | rien (lecture (c)) |
| 2 | — | — (UC_t = W_t/pr_t écrit par le bloc 2 en phase 2, M26, Q2) |
| 5, premier bloc | ouverture : p_{t−1} (registre), W_{t−1} (bloc 3), pr_t (bloc 2 ; pr_{t−1} = pr_t(1 + g_pr)^{−1/n_a}), IN^vol_t ; phase 2 : UC_t, IN^vol*_t | p_t ; puis l'indice et le glissement, selon la forme fixée par l'ADR |

- Aucune lecture de v_t, de d_t, ni des plans. La matrice est triangulaire.
- Aucune ligne de flux proposée : les acheteurs appliquent p_t aux volumes servis (lignes 1 à 3), et le bloc 2 valorise la ligne 4.
- **Délais** (lecture (c)) :
  - salaire → prix : 0 tour ;
  - demande → prix : 1 tour (ξ d'ouverture) ;
  - prix → règle de taux et prix → salaire : 1 tour ;
  - taux → règle par la marge : au moins 2 tours (`monnaie`, Q5).
- **Leviers qui transitent par le bloc** :
  - dépense publique : stocks au tour n, marge et prix au tour n + 1, glissement lu au tour n + 2 ;
  - impôts : un tour de plus ;
  - taux : par les plans des fiches 5 et 6 ;
  - anticipations : par les salaires (W_t), répercutées le tour même.

**Grandeurs restituées au tour** (couche `observation/`) :

| Grandeur | Définition | Unité | Dénominateur | Fenêtre | Niveau normal |
|---|---|---|---|---|---|
| Indice des prix | 100·p_t/p_1 (prix du tour) | indice | prix du tour 1 | le tour | — |
| Glissement annuel | P_t/P_{t−12} − 1 | par an | P_{t−12} | 12 tours | π̄ |
| Variation du prix sur le tour | p_t/p_{t−1} − 1, et (1 + x)^{12} − 1 ; aucune règle ne la lit | par tour ; par an | p_{t−1} | 1 tour | (1 + π̄)^{1/12} − 1 ; π̄ |
| Marge | p/UC − 1 | fraction | UC du tour | le tour ; moyenne sur 12 tours | μ̄ |
| Part salariale | ΣWB/ΣVA, commune avec la fiche 3 | fraction | VA sur 12 tours | 12 tours | 0,798903 (μ̄ = 0,25, π̄ = 2 %, n_a = 12) |
| Décomposition de l'inflation | contributions π_t·Δ₁₂ln UC/Δ₁₂ln p et π_t·Δ₁₂ln(1 + μ)/Δ₁₂ln p, exactement additives au glissement ; « sans objet » si \|Δ₁₂ln p\| ≤ 1e−12 | par an | glissement | 12 tours | — |
| Tension sur les stocks | ξ, positive quand les stocks sont sous leur niveau visé ; la définition dit son lien aux stocks en mois (fiche 2) | fraction | IN^vol* | le tour | 0 |

W/(p·pr) n'est pas une ligne du tableau de bord (= 1/(1 + marge) sous J = 1). Le taux d'utilisation reste hors du panneau des prix jusqu'à M28.

### 9.5 Conditions de `jeu` (§ 7, reprises telles quelles) et mise en œuvre

1. **Lecture (c)** : l'indice restitué est le prix du tour.
   *Mise en œuvre* : retenue par M26 ; aucune mention d'indice décalé.
2. **Variation du prix sur le tour**, brute et annualisée ((1 + x)^12 − 1), qu'aucune règle ne lit.
   *Mise en œuvre* : tableau du § 9.4 ; annualisation géométrique (`monnaie`, Q4).
3. **Une seule part salariale**, ΣWB/ΣVA sur 12 tours, avec son niveau normal dans la même définition ; W/(p·pr) n'apparaît pas comme ligne distincte.
   *Mise en œuvre* : § 9.4 ; centre de la bande commune (M26).
4. **Marge** (au tour et sur 12 tours) avec μ̄ ; **décomposition** en contributions additives.
   *Mise en œuvre* : § 9.4. La décomposition est définie « sans objet » à glissement nul : la définition manquait.
5. **ξ** restitué comme « tension sur les stocks », à côté de la marge.
   *Mise en œuvre* : § 9.4.
6. **Niveaux normaux** publiés par le script d'état stationnaire : μ̄, part salariale sur 12 tours, π̄ ou le taux effectif.
   *Mise en œuvre* : sous (G), π̄ lui-même ; § 9.6.
7. **Test d'alternance étendu** à la variation mensuelle.
   *Mise en œuvre* : § 9.6 (seuil et pré-validation).
8. **Scénario O2 au J4** avec le seuil du critère 10 (d), avec le délai perçu (premier tour à 0,1 et à 0,2 point) et la décomposition.
   *Mise en œuvre* : § 9.6.
9. **Prix administré (J4, J7)** : scénario apparié gel contre sans gel, écrit avant l'essai, avec un coût perceptible du gel ; sinon, le levier n'est pas ouvert. Marge comprimée restituée pendant le gel.
   *Mise en œuvre* : issue liée de M26 ; § 9.6 (J4).
10. **Taux d'utilisation** hors du panneau des prix jusqu'à M28.
    *Mise en œuvre* : condition transmise à la fiche 6.

**Seuil du critère 10 (d)** (proposé par `jeu`, à confirmer avant le J4, M26) : au moins 0,2 point pour +1 % et au moins 1,0 point pour +5 %.

### 9.6 Tests attendus

| Jalon | Test | Propriété | Seuil |
|---|---|---|---|
| J3 | État stationnaire (réserve 1) | Un pas sans choc depuis l'état résolu : μ̃ = ln(1 + μ̄) ; p croît de (1 + π̄)^{1/n_a} ; ξ = 0 | 1e−10 relatif (ξ : 1e−10 absolu) |
| J3 | T2 | Test commun avec la fiche 3 (§ 9.6) : règle M, π̄ ∈ {0 ; 2 % ; 10 %}, n_a ∈ {4 ; 12 ; 52} | idem |
| J3 | Vitesses (réserve 2) | λ_μ × 0,5 et × 2, G +1 % pendant 12 tours : écart de la marge, de ΣWB/ΣVA et de ξ | ≤ 1e−6 après 720 pas |
| J3 | Boucle propre (5 (d)) | 1 − λ_μ/n_a = 0,9 (× 0,5 : 0,95 ; × 2 : 0,8) | module < 1 |
| J3 | Boucle salaires – prix (5 (e), exigence ; réserve 3) | π^e = π̄ exogène, m effectif : une racine unitaire, de vecteur propre nominal ; toutes les autres de module < 1 | \|λ − 1\| ≤ 1e−8 pour la racine nominale ; rayon de la partie réelle < 1 à la calibration ; publié aux variantes |
| J3 | Boucle prix – stocks – demande (5 (f)) | m effectif | rayon < 1 à la calibration ; publié aux vitesses × 0,5 et × 2 |
| J3 | **Alternance étendue** (réserve 3 ; condition 7) | Depuis l'état résolu, G +1 % (part de 20 %, demande +0,2 %) au seul tour 1. Sur les tours 2 à 13 : (a) écart de ln p au sentier sans choc ; (b) écart de la variation mensuelle Δln p. Changements de signe comptés en ignorant \|x\| ≤ 1e−12. Pré-validation (`g6_alternance.py`) : sous M, (a) 0 et (b) au plus 1, sur m ∈ {0 ; 0,6 ; 0,8}, aux vitesses de la fiche 2 × 2 et à ψ × 2. Sous C, (b) 7 à 11 dès la calibration, alors que (a) vaut 0 : le test sur le niveau seul ne détectait pas l'alternance | ≤ 2 changements pour (a) et pour (b), à la calibration et au m effectif (exigence) ; publié aux variantes |
| J3 | Positivité | Appel direct avec ξ = 1 (stock nul) et ξ = −9 (stock à 10 fois la cible) : p > 0 et fini, par la forme exponentielle | exact |
| J3 | Phases | Le bloc 4 ne lit ni v_t, ni d_t, ni un plan ; il est le premier de la phase 5 ; ξ lit IN^vol* de N2 | aucune lecture hors ordre |
| J3 | Identité (critère 1) | Cas P15 : deux prix distants de 1 % ; somme des soldes financiers nulle ; valeur nette des entreprises égale par les flux et par les stocks | 1e−12 × S |
| J3 | Empreinte | Aucune variable d'état propre (une seule si μ̃ est porté, § 9.1) ; registre selon l'ADR | décompte exact |
| J3 | Coût | `test_budget.py` | ≤ 0,48 ms par pays-pas |
| J4 | O2 et seuil 10 (d) | Pic, sur les tours 1 à 36, de l'écart du glissement lu par la règle (× (1 + π̄)) : m = 0 au stade de la fiche, m effectif au J3 et au J4 ; délai perçu à 0,1 et 0,2 point et décomposition publiés | ≥ 0,2 pt (+1 %) ; ≥ 1,0 pt (+5 %) ; publié à × 0,5 et × 2 |
| J4 | Restitution | Niveaux normaux égaux à ceux du script : μ̄ ; ΣWB/ΣVA résolue ; π̄ | 1e−9 relatif |
| J4 et J7 | Prix administré | Scénario apparié gel contre sans gel, critères écrits avant l'essai | levier ouvert seulement si le coût est perceptible |
| — | Remesure P1 | Proposée, non lancée ; sans effet sur M26 | — |

### 9.7 Contrats partagés touchés, surface de spécification

**Contrats partagés** :
1. **Phase de P_t, lecture (c)** (décision citant M22 et l'ADR 0005, pt 16 ; ADR par `architect`, avec la forme et la clause de réouverture) :
   - `sec:cadre-calendrier` l. 182 : « l'indice des prix et son glissement… révisés en phase 1 » devient « arrêtés en phase 5 et lus en phase 1 du pas suivant » ;
   - l. 199 à 203 : l'empreinte calendaire passe de 13 à 14 variables (t et 13 niveaux, ou t, 12 niveaux et π) ;
   - `tab:phases` :
     - ligne 1 : retirer « indice des prix et glissement annuel (registre) » du contenu, et « prix » des blocs qui écrivent ; ordre libre entre travail et banque centrale ;
     - ligne 5 : ajouter « indice et glissement » si le bloc 4 les écrit ;
     - ligne 9 : mise à jour du registre ;
   - `CONTEXT.md` l. 32 (« Date de décision ») et l. 59 (« Registre de l'indice des prix ») : `architect` ;
   - ADR 0005, pt 16 : annotation.
2. **Phase de UC = 2** (choix laissé à la fiche 4 par M24, sans décision citant M22) : `tab:production-equations` l. 569 (N8 : « 2 ou 4 (fiche prix) » → « 2 ») ; `sec:production-phases` l. 694 ; `tab:production-phases` l. 712 et 713 (UC en phase 2 seulement) ; fiche 2, § 9.1 (ligne N8) et § 9.4.
3. **Lecture (G)** : fiche 3, § 9.8, point 1 ; neutre pour M.
4. Matrices inchangées.

**Surface de spécification** (#40, jalon 4, `docwriter` ; encadrés `proposee` citant M26) :
- **`sec:prix`** :
  - encadré de décision ;
  - tableau des équations ;
  - base UC (coût à productivité normale) ;
  - ξ ;
  - M (variables, sens, hypothèses, `\limites`) ;
  - aucune anticipation consommée, ni canal direct π^e → p, ni canal de coût (C13) ;
  - indice et glissement (c) ;
  - phases (§ 9.4) ;
  - état stationnaire : p/UC = 1 + μ̄, ξ̄ = 0, variation de 0,16516 % par pas à 2 %, WB/VA = 0,798903 (2 %) et 0,793445 (10 %) contre 1/(1 + μ̄) = 0,8, avec sa dépendance à n_a ;
  - boucles (valeurs du § 3.N-9) ;
  - aucune borne, conditions déclarées ;
  - grandeurs restituées ;
  - encadré `joueur` ;
  - encadré `portee` : J = 1 ; aucun terme en tu avant M28 ; aucune vitesse modulée par l'inflation ; aucune « énigme des prix » ; marge procyclique contestée ; forme M sans source lue ; prix administrés au J4 et au J7.
- **`tab:calibration`** : μ̄, λ_μ, ψ_ξ.
- **`tab:symboles`** : μ̄, μ_t, μ̃_t, ξ_t, ψ_ξ, λ_μ ; définition de P_t.
- **`sec:ecartees`**, « Prix (décision M26) » : A ; B ; R (référence, critère 5 (b)) ; C (alternance) ; D (dépend de C1, marge contracyclique) ; T (renvoyée à M28) ; coût complet au prix courant et à la valeur comptable ; marge sur cm ; coût retardé ; NHUC (noté) ; lectures (a) et (b) de P_t.
- **Texte de `tab:instabilites`** :
  - la 14 est traitée par ξ : terme de demande gardé, et non « écartée par construction » ;
  - les 10 et 11 sont sans objet pour le bloc 4 (aucun amortissement dans la base), mais restent des risques de la fiche 6.
- **`sec:changements-v3x`** : une ligne « prix (M26) ».

### 9.8 Constats transmis

- **Fiche 3** : T2 sur le dernier prix connu (déjà repris) ; μ̄ lu à source unique (w1) ; l'option « μ̃ en variable d'état » est commune.
- **Fiche 5** :
  - déclarer la base nominale des plans : l'instruction supposait p_{t−1}(1 + π^e)^{1/n_a}, forme (G) ; les boucles 5 (e) et 5 (f) sont à remesurer avec le m effectif ;
  - signe du canal taux → demande : un canal rentier dominant ferait amplifier un effet pervers par la marge ;
  - la marge alimente les profits distribués, qui sont un coût possible du gel (condition 9).
- **Fiche 6** :
  - T au plus tard à M28 (#37) ; t̄u comme paramètre à source unique ;
  - la marge comprimée réduit les profits non distribués, puis l'investissement ;
  - ρ̄_K = 0,7786 sous (G) (partie C) ;
  - un intérêt sur le fonds de roulement n'entre pas dans la base du prix sans réviser M26.
- **Fiche 8** :
  - C9 à C13, en plus de C1 à C8 ;
  - délai de lecture de 1 tour sous (c) ; π_{n−1} lu dans le registre ; ordre de la phase 1 libre ;
  - clause de réouverture attachée à C10 ;
  - « taux indiqué par la règle » restitué (C9) ;
  - retour du niveau des prix (C11) ;
  - point r = i − π sous (G) (fiche 3, § 9.8).
- **Fiche 9** :
  - une fiscalité indirecte éventuelle pose la question de la base du prix : décision citant M26 ;
  - dépense en u.m. ;
  - le rationnement est un coût possible du gel.
- **`architect`** : ADR de la lecture (c) (forme, empreinte, clause de réouverture) ; `CONTEXT.md` : « marge normale », « tension sur les stocks », « indice des prix (lecture (c)) ».

### 9.9 Issues proposées

Issues liées de M26, à créer sur accord du mainteneur : prix administrés et coût de la marge comprimée ; levier de répartition au J4. Autres propositions : partie E du compte rendu de `macro` du 03/10/2026.

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 03/10/2026 | Ouverture (issue #40) ; § 1 et § 2 proposés | `macro` ; session principale |
| 03/10/2026 | Critères validés avec amendements (seuils et bandes, critère 5 (e) en exigence, part salariale sur W/(p·pr), trois lectures de P_t, terme de demande, variante en tu, lecture unique de #24, Q10 ; issue #40) | mainteneur |
| 03/10/2026 | Instruction déposée (§ 3 à 5) : options A, B, socle 3.N, options nouvelles ; recommandation M (marge à rappel vers μ̄ avec terme de stocks), P_t en lecture (c) ; mesures conjointes avec la fiche 3 (critères 3 (d) et 5 (e)) ; remesure proposée | `macro` |
| 03/10/2026 | Avis de `jeu` (§ 7) : préférence M > D > R > C > B > A, C jugée rédhibitoire (alternance dès la calibration) ; lecture (c) de P_t préférée ; seuil du critère 10 (d) proposé (0,2 point pour +1 %, 1,0 point pour +5 %) ; conditions sur le prix administré et le levier de répartition au J4 ; correction de son avis sur la fiche 3 (question 7) | `jeu` |
| 03/10/2026 | Avis de `monnaie` (§ 6) : favorable à M avec la lecture (c) de P_t ; clause de réouverture de la Q1 proposée ; T2 sous (a) à éliminer ; précision à son avis sur la fiche 3 (retour du niveau des prix sous C2) ; conditions C9 à C13 transmises à la fiche 8 | `monnaie` |
| 03/10/2026 | Statut « avis rendus » | session principale |
| 03/10/2026 | Décision M26 : option M, UC en phase 2, terme ξ, lecture (c) de P_t avec clause de réouverture, (G) commune, T transmise à la fiche 6 | mainteneur |
| 03/10/2026 | Conséquences de M26 (§ 9) rédigées par `macro` : labels, paramètres, interfaces, conditions de `jeu`, tests attendus, contrats partagés et surface de spécification, constats transmis | `macro` ; session principale |
