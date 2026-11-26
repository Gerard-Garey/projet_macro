# Feuille de route

Tenue par `architect`, après chaque série de PR fusionnées. Chaque mise à jour est datée et cite le SHA de `main` et de la branche de travail. **Tête condensée** (#119, P76) : périmètre courant, jalons, décisions en vigueur et points ouverts ; le reste est dans `docs/feuille-de-route-historique.md` (parties A à G et leurs compléments, sans rien supprimé ni réécrit), dont la « Lecture des renvois » dit où lire chaque renvoi absent de la tête.

**Dernière mise à jour** : 26/11/2026, rang 1 de J3-e1 (`architect-approfondi`, Fable 1 sur 3) — `main` = `831547c` (commit de fusion de la PR #162, § 7) ; branche de travail `claude/j3-e1-etat-initial` à `eed2d31`, PR brouillon #174 ; plan de J3-e1 **décidé** (§ 1 ; P246 à P257, § 4) ; #175 et #176 créées ; **ADR 0015 proposé**, à accepter (points S1 à S10) ; relevé des issues du 26/11/2026 (§ 3). Mises à jour antérieures et extraits sortis : historique, partie H (fiche de la branche « calibration », relevé du 16/11/2026, points soumis au rang 11), puis parties G à A et `git log -- docs/feuille-de-route.md`.

## 1. Branche de travail en cours

**J3-e1 « état initial résolu et test zéro »** (`claude/j3-e1-etat-initial`, créée depuis `main` à `831547c` le 26/11/2026 ; PR brouillon #174) : ouverture décidée par le mainteneur le 26/11/2026 (ligne 12 du § 2 ; découpage P212). Plan ci-dessous **décidé** par le mainteneur le 26/11/2026 (P246 à P257, § 4). Fiche de la branche « calibration », figée à la fusion de la PR #162 : historique, partie H, § 1.

### Plan de J3-e1 (`claude/j3-e1-etat-initial`) — état initial résolu par `scenarios/` (#175), test zéro et `observation/` (#176), radical `observation` (#115), cohérence de l'état chargé (#122), formes du script (#125, points 3 à 5)

*Proposé par `architect-approfondi` au rang 0, décidé par le mainteneur le 26/11/2026. La forme est fixée par l'**ADR 0015**, proposé au rang 1 et **accepté le 26/11/2026 (P258)**.*

- **Issues** (P246) : avec `Closes`, #175, #176, #115, #122 ; sans `Closes`, #125 points 3 à 5. Le point 6 de #125 (bornes inférieures de κ et σ, question de domaine relevant de `macro`) va en J3-e2, avec #158 (écart à P212 assumé) ; le point 2 reste en J3-f1 (`Closes`).
- **Motif** : le test zéro part de l'état initial résolu (`docs/exigences.md` § 2.6 ; ADR 0002, pt 13). À `831547c`, `src/nations/scenarios/` ne contient que son `__init__.py` ; l'état d'ouverture est construit dans `tests/` (`socle_partiel.etat_initial`, depuis `outils/etat_stationnaire.py` chargé par son chemin), et les grandeurs B y sont calculées (`socle_partiel.grandeurs_b`), hors d'`observation/`. #115 précède le premier label `eq:observation-…`. #122 porte sur l'état que `scenarios/` construira. #125 (points 3 à 5) porte sur des écarts de forme et de domaine entre le script et le moteur.
- **Forme de la résolution** (P247 ; ADR 0015). **R1** : le résolveur en formes fermées (`etat_stationnaire` et `ouverture` du script) passe dans `src/nations/scenarios/` comme fonction pure sur des flottants, sans table ni drapeau. Deux adaptateurs l'appellent : `scenarios` (tables → `EtatPays` et tables alignées, θ_G résolu), et le script, qui l'importe (précédent : `outils/linearisation.py` importe `nations`). Les formes fermées n'ont ainsi qu'une maison, sans dupliquer le script. A1 contrôle alors la transcription (unités, registre, V^flux, correspondance des noms) ; A2 contrôle l'équilibre des règles ; l'algèbre indépendante reste celle des blocs, d'`un_pas`, de `residus_des_regles` et des valeurs publiées (P248). Options écartées (motifs complets : ADR 0015) :
  - R2, seconde implémentation indépendante : deux maisons par règle, et #125 montre déjà la dérive de formes dupliquées ;
  - R3, point fixe numérique sur la carte du moteur : continuum en ϱ̄_L et en stocks de la banque centrale tenus en niveau, jacobienne singulière, état non recalculable à la main (ADR 0002) ;
  - R4, état précalculé versé en fichier : préparation, et archétypes non résolubles à la demande.
- **Ordre** : #115 ; #175 (extraction, puis adaptateur) ; #122 et #125 sur l'état de #175 ; #176 en dernier, sur l'état de `scenarios/`.
- **Experts pilotes** (`docs/blocs/README.md` pour les blocs) :
  - `macro` pour #175, #176, #122 et #125 (état stationnaire, bouclage stock-flux, blocs 2 à 4) ;
  - `monnaie` consulté sur #175 et #176 pour les blocs 7 et 8 (B17 à B19, B25, B26 ; existence du dividende de la banque ; stocks de la banque centrale) ;
  - #115 : aucun pilote (circuit 3) ;
  - `jeu` : non déclenché, aucun mécanisme visible (la restitution du test zéro relève du J4).
- **Hors périmètre** : F2 (attraction), en J3-f1 avec S1 (P249) ; #168 et #170 à #173 (§ 2, ligne 12 bis, P255) ; domaines et refus typés (J3-e2). Une question de fond qui surgit est une condition d'arrêt, jamais un ajout.
- **Contrats partagés** (`docs/agents/routage.md` § 4.2), fixés par l'ADR 0015 avant tout code :
  - interface de `scenarios/` (module feuille `stationnaire`, `initial.etat_initial`, refus `EtatStationnaireInexistant`), lue par `tests/`, par `outils/etat_stationnaire.py`, par `outils/empreintes_des_bancs.py` (via `socle_partiel`), puis par les leviers (J4) et les archétypes (J5) ;
  - test « conversion unique » : liste fermée d'exemptions pour le module feuille (ADR 0015, pt 13 ; modifie ADR 0014, F2) ;
  - imports du script : bibliothèque standard et le seul module feuille (ADR 0015, pt 14) ;
  - radicaux de la concordance (#115 ; 90 labels à `831547c`, 91 avec `eq:observation-ratio-pib-annuel`) ;
  - conditions jointes de l'état dans `nations.etat.schema` (#122 ; P251 ; ADR 0014, annotation du 26/11/2026) ;
  - série du test zéro dans `observation/`, sous le protocole inchangé (ADR 0014, E1).
  
  Restent inchangés : équations, phases, variables d'état, `tab:etat-stationnaire`.

| Rang | Étape | Agent | Circuit |
|---|---|---|---|
| 0 | **Fait (`c93150a`)** : point d'étape, plan proposé, partie H de l'historique ; PR brouillon #174 ; règle P242 dans `CLAUDE.md` (`eed2d31`) | `architect-approfondi`, session | `docs:`, `claude:` |
| 1 | **Fait (présente mise à jour)** : décisions P246 à P257 ; #175 et #176 créées par la session ; ADR 0015 proposé ; annotations des ADR 0014 et 0005 ; termes de `CONTEXT.md`. ADR 0015 accepté par le mainteneur (P258) | mainteneur ; `architect-approfondi` (Fable, P253) | § 4.2 |
| 2 | #115 : `observation` dans `RADICAUX_TRANSVERSES`, tests d'admission et de refus | `coder` → `audit` léger | 3 |
| 3 | #175, après l'acceptation de l'ADR 0015. Commit 1 : extraction du résolveur dans le module feuille, que le script importe, avec les exemptions et les tests d'imports. Commit 2 : `scenarios.etat_initial`, `socle_partiel.etat_initial` et `parametres_du_sentier` réduits à des adaptateurs | `coder` → `audit` léger ; contrôle de `macro` (`monnaie` consulté) | 3 + contrôle |
| 4 | #122 : condition jointe dans le schéma d'état (P251 ; ADR 0015, pt 12), avec les points 2 et 3 du commentaire du 13/11/2026 ; le point 1 (μ̃) est renvoyé à #158 | `macro` (avis), `coder` → `audit` léger | 2 |
| 5 | #125, points 3 à 5 : avis de `macro` (forme distincte déclarée ou forme du moteur), puis `coder` | `macro` ; `coder` → `audit` léger | 2 |
| 6 | #176 : séries B1 à B26 et écarts d'A2 dans `observation/`. Premier label `eq:observation-ratio-pib-annuel`, avec un commit `docs:` minimal poussé avec le code (exception de la règle 9). Tests A1, A2, B, F1 et C1 (P249) sur P et L | `coder` → `audit` léger ; `macro`, `monnaie` | 1, sans changement de trajectoire |
| 7 | Mesures « après » : empreintes, sortie du script, test de suppression, verdicts | session, `coder` → `audit` ; `macro`, `monnaie` | — |
| 8 | Passage unique de `docwriter`, un commit `docs:` par issue : état initial résolu, verdicts du test zéro dans `sec:calibration`, radical, limites de #122, formes de #125 ; validation par `macro` et `monnaie` | `docwriter` ; `macro`, `monnaie` | règle 9 |
| 9 | Revue finale complète, puis `/code-review` | `audit` | règle 10 |
| 10 | Consignation, corps de PR, sortie du brouillon, fusion en commit de fusion | `architect`, session, mainteneur | — |

**Critères d'acceptation, écrits avant l'essai** (communs) :
- **Identique au bit** (P250), à chaque commit `code:` et `tests:` :
  - `uv run python outils/empreintes_des_bancs.py --comparer outils/empreintes_des_bancs_ce3662a.json` sort en code 0 ; mesuré à `831547c` le 26/11/2026 : code 0, empreinte globale `b8cbd18d…` ;
  - la sortie de `uv run python outils/etat_stationnaire.py` est identique à l'octet à celle du script de `831547c`. Remesuré au rang 1 (`eed2d31`, script inchangé) : sortie standard de 205 933 octets, sha256 `fb187be1…`, deux exécutions identiques ; bilan « 449 valeurs comparées, 429 égales sur l'état résolu, 20 égales en arithmétique de la spécification (catégorie S), aucun écart », contre-épreuve 47 sur 47, historique 29. **La valeur `a0970c9f…` du rang 0 (reprise dans #175) n'est pas reproduite, cause non établie** : la référence est régénérée par la session, sur la machine de l'essai, avant le premier commit `code:` (ADR 0015, S8) ;
  - aucune référence d'empreintes nouvelle.
- **Concordance et matrices** : `--strict` sans écart (90 labels, puis 91 au rang 6) ; matrices sans écart.
- **Observation sans effet** (ADR 0014, E1) : sauvegardes identiques à l'octet sous la série du test zéro et sous `ObservateurNul`, aux trois π\*, sur 720 pas.
- **Dépendances** : `src/` n'importe ni `outils/` ni `tests/` (test existant). Batteries vertes ; #80 et #139 restent en échec attendu (un succès inattendu suit la règle des tests).

**Critères propres** :
- **#175** :
  - aux trois π\*, `scenarios.etat_initial` rend un `EtatPays` égal au bit à celui de `socle_partiel.etat_initial` à `831547c` (positions, V^flux, variables, registre), et des tables égales à celles de `parametres_du_sentier` (θ_G résolu) ;
  - une condition d'existence violée (D1, D2, dividende de la banque, Div_F ≥ 0, θ_G > 0, marge du plafond de E1, B, B_Bk, B_CB ≥ 0) donne un refus typé, jamais un état ;
  - aucun littéral nouveau de valeur résolue dans `src/` ; θ_G de la table de référence reste, tenu au bit par son test (ADR 0015, S3).
- **#176** :
  - A1 (transcription, P248) : écart ≤ 1e−9 relatif, pour chaque valeur de `tab:etat-stationnaire`, à t = 0 et π\* ∈ {0 ; 2 ; 10 %} ;
  - A2 (équilibre des règles, P248) : écart ≤ 1e−9 à chaque pas de P, puis de L, pour B1 à B26 et r̂\* ; grandeurs nulles à 1e−12 S près ;
  - B1 à B26 : jugés sur la moyenne de chaque bloc de 60 pas, sur P et L, à π\* = 2 %, verdicts publiés côte à côte. Demi-largeurs et définitions de `tab:criteres-j3` inchangées. **Le centre c est calculé par `scenarios/` à la table T1 (M34)**, jamais recopié ; son égalité à la colonne « valeur résolue », à la précision de publication, est contrôlée par le script ;
  - F1 et C1, définitions de `tab:criteres-j3` (P249) ;
  - une grandeur qui ne s'évalue pas sans un contrat nouveau est une condition d'arrêt : la ligne n'est jamais retirée.
- **#115**, **#122** : critères des issues. Pour #122, l'état initial et la reprise sont couverts ; les points 2 et 3 du commentaire reçoivent un refus typé ou une limite déclarée, sur avis de `macro`.
- **#125 (3 à 5)** :
  - point 5 : le script refuse le même ensemble que la table (κ > 0 et 1/κ fini) ;
  - point 4 : N6 donne un refus explicite à d = 0 ;
  - point 3 : forme (i) déclarée comme forme indépendante, ou forme (ii) du moteur, sur avis de `macro` ;
  - aucune ligne de la sortie du script ne change aux valeurs par défaut.

**Conditions d'arrêt** :
- un bit de différence, dans les empreintes ou dans la sortie du script ;
- A2 ou une bande B non tenus depuis l'état de `scenarios/` ;
- un élément de l'état résolu fixé par une convention de sélection sur un continuum que l'ADR 0015 ne déclare pas (pt 10) ;
- le besoin d'une variable du pas, d'une phase, d'une entrée ou d'un champ de `FinDePas` nouveaux ;
- une question de fond hors des cinq issues, ou un désaccord entre `macro` et `monnaie` ;
- un constat bloquant ou majeur après la reprise unique.

**Effet attendu sur les résultats** : aucun changement de trajectoire. Les premiers verdicts du test zéro (A1, A2, B) sont des résultats finaux, soumis au mainteneur. `tests/references/` reste absent (J3-g2).

**Délégation** : P175 et P211 reconduites (P254). **Budget Fable** : 1 sur 3 utilisée (ADR 0015, rang 1 ; P253) ; aucune autre sans nouvel accord.

## 2. Branches suivantes

Les branches fusionnées sont au § 7 ; lignes 7 à 9 (J3-b, J3-c, J3-d1) : historique, partie E, § 2 ; ligne 10 (J3-d2) : historique, partie F, § 2 ; ligne 10 bis (forme du code) : historique, partie G, § 2 ; ligne 11 (calibration) : historique, partie H, § 2.

**Découpage de J3-e à J3-g (P61, P177), décidé le 16/11/2026 (P212).** Avec les issues nées depuis P61 (#153, #154, #156, #158 à #161, #163), chacune des trois branches indicatives dépassait la règle des trois à cinq issues : chacune a été scindée selon le module touché et l'ordre des dépendances. Les lignes 13 à 18 restent indicatives jusqu'au point d'étape qui précède chacune. #157 : correctif rapide hors branche (P212).

| Ordre | Branche | Issues | Motif du regroupement et état |
|---|---|---|---|
| 12 | **J3-e1 « état initial résolu et test zéro » `claude/j3-e1-etat-initial`, PR #174 — en cours, plan décidé (§ 1)** | #175, #176, #115, #122 ; #125 (points 3 à 5, sans `Closes`) | Critères A1, A2, B, F1, C1 ; résolution par `scenarios/` sans dupliquer le script (P247, ADR 0015) ; bandes B centrées sur l'état calibré (M34). |
| 12 bis | « suites de M34 à la table T1 » — **décidée** (P255), après J3-e1 | #168, #170, #171, #172, #173 | Remesures et outils à la table T1 : `outils/etat_stationnaire.py`, `outils/maquette_conjointe.py`, `tests/unitaires/test_etat_stationnaire.py`, ligne 17 de `tab:instabilites`. Placée après J3-e1, qui réorganise le même script. Pilote `macro`, `monnaie` pour #173. Les chiffres de #171 liés à #88 et #131 sont remesurés dans J3-f2 et J3-e3, sans double travail. |
| 13 | J3-e2 « domaines à l'état chargé et refus typés » | #120, #153, #158 ; #125 point 6 (P246) | Refus typés au lieu d'exceptions brutes ; après J3-e1 (états chargés par `scenarios/`). Le point 1 du commentaire de #122 (μ̃) relève de #158. |
| 14 | J3-e3 « critère I1 » | #114 (avec #131, mesure), #139, #140, #169 (P240) | Lignes « J3 » des fiches sur le socle complet depuis l'état résolu (P122, P149, P150) ; après J3-e1. |
| 15 | J3-f1 « stabilité linéarisée » | S1 (à rédiger), #147, #116, #125 (point 2, `Closes`), #163 (P204) ; F2 (P249) | Linéarisation sur le moteur ; ratio de sacrifice sur le socle linéarisé (C7). **Condition de M34 : #163 traitée avant la démonstration J4.** |
| 16 | J3-f2 « trajectoires après chocs » | S2 (à rédiger), #87, #88, #111, #154 | Après J3-f1 (#116 → #111). |
| 17 | J3-g1 « chemin chaud » | #110, #159, #160, #161, #156 | Forme du code sans changement de résultat (critère « identique au bit ») ; avant G1, qui mesure le coût final. |
| 18 | J3-g2 « budget, références, passage » | G1 (à rédiger), références et `outils/regenerer_references.py` (à rédiger) | Dix exécutions, premières références, passage de J3. |

Ordre des modules de J3-b à J3-d (P41 (a), P111) : historique, partie E, complément du rang 8 de J3-d2.

Issues à rédiger plus tard (`architect`, au point d'étape qui précède chaque branche, approuvées par le mainteneur) : S1 (J3-f1 ; #163 rédigée le 16/11/2026, P204) ; S2 (J3-f2) ; G1, budget du socle complet, et références avec `outils/regenerer_references.py` (J3-g2). N1 et N2 du rang 0 de J3-e1 : créées le 26/11/2026, #175 et #176 (P257).

## 3. Issues hors plan

*Relevé du 26/11/2026* (point d'étape après la fusion de la PR #162, `main` = `831547c`) : **63 issues ouvertes** (`list_issues`, état ouvert, `totalCount` = 63, `architect-approfondi`, rang 1, 26/11/2026 ; 61 au rang 0, plus #175 et #176). #92, #55, #130, #62, #45 et #166 ont été fermées par la PR #162 (fermetures vérifiées par la session le 26/11/2026) ; #163 à #173 ont été créées depuis le relevé du 16/11/2026 (56 + 11 − 6 = 61). Relevé précédent : historique, partie H, § 3. La colonne « Branche prévue » n'est pas reportée sur GitHub.

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #10 | Registre d'exemptions de la concordance | hors plan | aucune exemption prévue |
| #11, #14 | Dependabot ; ruleset de `main` | mainteneur, hors branche | `ready-for-human` depuis le 30/09/2026 |
| #37 | Aucun levier d'offre au socle | J4, au plus tard J7 | M26, M28 |
| #46, #47, #48 | Okun ; prix administrés ; levier de répartition | J4 (#47 puis J7) | inchangé |
| #52, #53, #63, #70, #79 | Restitutions et scénarios O2, O3 | J4 | inchangé |
| #54, #56 | Aller-retour de π\* ; signe net d'une hausse de taux | J4, sans `Closes` | condition (c) du levier de cible sur #54 (P99) ; durée d'une partie : #155 (P180) |
| #57 | Crises de crédit sous la règle F | J6 | inchangé |
| #64 | S-ζ hors cible durable | J5 | inchangé |
| #78, #89 | Coût de la dette ; stratégie dominante | J4 (#78 puis J6) | #89 dépend de #88 |
| #80 | Superneutralité (critère 13 de la fiche 8) | hors branche, échec attendu | republiée à la table T1 (`tab:criteres-j3`, E1) ; voie (c) de M32 maintenue |
| #81, #82 | Restitutions des blocs 8 et 9 | J4 | #81 : plancher du taux directeur, avis de `monnaie` avant le J4 (P181) ; #82 amendée (P178) |
| #87, #88, #111 | D_F ≥ 0 hors stationnaire ; fenêtre longue ; trajectoires C-HS | J3-f2 (P42, P60) | #116 → #111 |
| #108 | Identifiants Cn et Co | J5 | P46 (a) |
| #110 | Processeur de l'exécuteur en CI | J3-g1 (P60) | marge du noyau seul (P57, rang 8 de la calibration : historique, partie G) |
| #114, #131 | Critère I1 ; BC2 en log | J3-e3 (#131 mesuré à #114, P101) | reçoit les lignes (c) des fiches 5 et 6 (P122) et l'exécution de #139 et #140 |
| #115, #122 | Radical `observation` ; IN^vol = 0 ⇒ IN = 0 à l'état chargé | **J3-e1, en cours (§ 1)** | #122 : condition jointe du schéma d'état (P251) ; point 1 du commentaire (μ̃) renvoyé à #158 |
| #116, #147 | Maquette conjointe ; C62 en régime linéaire | J3-f1 (S1) | #147 reçoit l'harmonisation « 63 tours » (P178) |
| #120 | `Cadre` à n_a ≠ 12 | J3-e2 (P82, option (a)) | inchangé |
| #125 | Facteur de croissance par pas, formes et domaines du script | points 3 à 5 : **J3-e1** (sans `Closes`) ; point 6 : J3-e2 (P246) ; point 2 : J3-f1, `Closes` | point 1 réalisé en J3-c (P88) |
| #135 | `tab:phases` et levier de taux au J4 | J4 | recoupe #54, #56 |
| #139, #140 | Critère « Endettement, dépôts » ; bornes (c) de la fiche 6 | J3-e3 (voies P149, P150) | #139 en échec attendu strict (P237) |
| #141, #145 | Restitution du refus de crédit ; coefficient de richesse sur π\* de la table | J4 (P152) | #141 avec #70 ; #145 avec #54 |
| #143 | S6 : ti = 0 au-delà d'une frontière | (1′) en J3-e2, levier au J4, crise au J6 (P215) | instruite au rang 1 de la calibration (P207) ; M28 non rouverte ; caisse : refus voulu (P216) |
| #148 | B_Bk, B_CB ≥ 0 sans contrôle sous rachat net | J4, instruction de `monnaie` avant (P178) | inactif au socle |
| #152 | E5 par colonne des entreprises | J5 (P172) | point 3 de #150 |
| #153 | Noyau : résidu/S infini à échelle nulle | J3-e2 (P178) | refus typé |
| #154 | Plafond de E1 sous placement raté prolongé | J3-f2 (P178) | inchangé |
| #155 | Durée d'une partie | avant le J4 (P180) | décisions du mainteneur |
| #156 | Bloc 7 : lecture nette de D_H et D_F hors de la phase 6 | J3-g1 (P212) | P191 ; suite de #142, critère « identique au bit » |
| #157 | Tests textuels de `src/` : m1 (P202), R1, R2 | correctif rapide (P212), sinon J3-e2 | `tests:` seul, résultats identiques |
| #158 | T3 : domaine de μ̃, exceptions brutes | J3-e2 (P212) | `travail.py:73` et `:90` (relevé du 16/11/2026) |
| #159, #160, #161 | f(π\*_t) deux fois ; contrôles refaits par `etat_de_cloture` ; i_L·L/n_a et δK/n_a recalculés | J3-g1 (P212) | critère « identique au bit » ; #161 recoupe #144 point 2 et respecte C41 |
| #163 | C7 : a_π, a_I, λ_e sur un ratio de sacrifice sourcé (fiche 8, critère 23) | J3-f1 (P204) | **condition de M34 : traitée avant la démonstration J4** |
| #164 | δ et consommation de capital fixe ; dividendes dans la valeur ajoutée | hors branche (P214) | née de l'instruction de #92 |
| #165 | Indicateur d'investissement au tour | J4 (P221) | avis de `jeu` sur ζ = 8 |
| #167 | Bêta des dépôts (limite de B2) | J4 ou J6 (P227) | née de l'instruction de #130 |
| #168 | Instabilité 17 : lecture (a) des ménages à la table de M34, motif de stabilité de M27 | 12 bis (P255) | née de M34 (§ 7.14 de la fiche de calibration) |
| #169 | Critère « Endettement » de #139 en enveloppe | J3-e3, avec #139 (P240) | correction prospective |
| #170 | Cas adverse lv\* = 0,45 à la table T1 | 12 bis (P255) | P240 |
| #171 | Remesure à T1 des chiffres publiés « à la calibration indicative » | 12 bis (P255) | créée le 26/11/2026 (P245) ; `macro` |
| #172 | Robustesse des outils de calibration et de la maquette après M34 | 12 bis (P255) | créée le 26/11/2026 (P245) ; même module que #175 : après J3-e1 |
| #173 | Libellé « Δr̄_α au minimum en ζ (ζ = 68) » à T1 | 12 bis (P255) | créée le 26/11/2026 (P245) ; `monnaie` ; grille fine : point 4 de #172 |
| #175 | `scenarios/` : état initial résolu par le moteur | **J3-e1, en cours (§ 1)** | créée le 26/11/2026 (P257) ; forme : ADR 0015 ; `macro`, `monnaie` consulté |
| #176 | Test zéro : séries dans `observation/`, verdicts A1, A2, B1 à B26, F1, C1 | **J3-e1, en cours (§ 1)** | créée le 26/11/2026 (P257) ; après #175 et #115 |

**Points ouverts sans issue** :
- mutant équivalent B_Bk/Res dans B5, à rouvrir avec le corridor (J6, P116) ;
- réserves mineures de J3-d2 non corrigées : lectures de `TABLEAU_DES_PHASES` non reliées au `.tex` ; contrôle de priorité du critère 12 doublé par le noyau pour les erreurs qui créent un découvert ; coût du socle complet publié sans verdict jusqu'à G1 (J3-g2) ;
- divergences du texte de l'ADR 0013 relevées par l'ADR 0014 (n5.1, n1.5, n6.3, n1.4, n7.5 ; compte rendu du rang 9, PR #151), sans effet sur les règles : non traitées par l'annotation du 26/11/2026, limitée aux contrats de J3-e1 ; elles restent à porter dans une annotation de l'ADR 0014.

Le point « résolution de l'état initial par `scenarios/` sans dupliquer le script » est passé au plan de J3-e1 (§ 1, P247, ADR 0015).

**Dépendances** (26/11/2026, après la PR #162).
- **Ajoutées** (décidées le 26/11/2026) : #115 → #176 ; #175 → #122, #125 (points 3 à 5), #176 ; J3-e1 → ligne 12 bis (#172 et #173 touchent `outils/etat_stationnaire.py`, que #175 réorganise ; P255) ; S1 → F2 (P249) ; #172 point 4 → #173 (grille). **Ajoutée au rang 1** : acceptation de l'ADR 0015 → #175, #122, #176 (rangs 3, 4 et 6) ; #115 (rang 2) n'en dépend pas.
- **Retirées**, levées par la fusion de la PR #162 : #92 → #55 → #130 ; instruction de #143 → section de #55 ; #45 (λ_w, M34) → #163 ; branche de calibration → J3-e.
- **Inchangées** : S1 → #163 ; #163 → démonstration J4 (condition de M34) ; J3-e1 → J3-e2 et J3-e3 ; J3-f1 → J3-f2 ; J3-g1 → J3-g2 ; #143 → domaine du levier de taux (J4) ; avis de `monnaie` sur la caisse des entreprises → #143 ; #145 → #54 ; #141 → J4 (avec #70) ; #131 → #114 ; #116 → #111 ; #89 → #88 ; #148 → leviers du J4 ; #152 → J5.

## 4. Décisions du mainteneur

M1 à M33 sont arrêtées par le mainteneur du 29/09/2026 au 04/10/2026 ; dates, lieux de consignation, forme canonique `Mn` et trois décisions de mise en œuvre sans numéro : historique, partie E, § 4 (sorti le 15/11/2026, texte inchangé).

| N° | Date | Décision | Où elle est consignée |
|---|---|---|---|
| M1 | 29/09/2026 | Nouveau moteur modulaire « v3 », écrit bloc par bloc ; v1.5 et v2.0 servent d'archives de référence. Rouvre la décision du 19/09/2026 « pas de reconstruction du prototype v2.0 » (motifs dans l'ADR 0001). | ADR 0001, pt 1 ; `CLAUDE.md`, « Contexte » |
| M2 | 29/09/2026 | Le mainteneur tranche lui-même, bloc par bloc, l'origine de chaque approche (v1.5, v2.0 ou nouvelle), sur fiche comparative. | ADR 0001, pt 2 ; ADR 0004, pt 7 ; `docs/exigences.md` § 2.3 |
| M3 | 29/09/2026 | Des approches autres que celles de la v1.7 et de la v2.0 sont bienvenues, appuyées sur des références vérifiées. | ADR 0001, pt 3 |
| M4 | 29/09/2026 | Simulateur d'abord ; jeu tour par tour mensuel à terme. | ADR 0001, pt 4 ; `docs/exigences.md` § 1.1 |
| M5 | 29/09/2026 | Interface cible : navigateur web, moteur Python côté serveur ; ligne de commande d'abord. | ADR 0001, pt 5 ; `docs/exigences.md` § 5 |
| M6 | 29/09/2026 | Dossier `archive/` dans le dépôt, strict nécessaire, voué à être supprimé (au plus tard fin J6) ; contenu et exclusions fixés. | ADR 0001, pt 6 ; `CONTEXT.md`, « Archive » |
| M7 | 29/09/2026 | Premier jalon économique : économie fermée, un pays (le socle). | ADR 0001, pt 7 |
| M8 | 29/09/2026 | Spécification en LaTeX (XeLaTeX), forme de la v1.5, chaîne documentaire reprise d'`outil_usp`. | ADR 0001, pt 8 ; ADR 0004 |
| M9 | 29/09/2026 | Trois experts de fond : `macro`, `monnaie`, `jeu`. | ADR 0001, pt 9 ; `CLAUDE.md`, « Sous-agents » |
| M10 | 29/09/2026 | On se passe de la v1.7 : ni prototype ni document. | ADR 0001, pt 10 ; `docs/exigences.md` § 2.2 |
| M11 | 29/09/2026 | Claude seul sur le dépôt, sans autre flux d'assistants. | ADR 0001, pt 11 |
| M12 | 29/09/2026 | Les six objectifs du 17/09/2026, reformulés « simulateur d'abord », fondent `docs/exigences.md`. | ADR 0001, pt 12 ; `docs/exigences.md` § 1.3 |
| M13 | 29/09/2026 | Budget de calcul : au plus 1 ms par pays-semaine. | ADR 0001, pt 13 ; ADR 0002, inv. 11 ; `CLAUDE.md`, « Architecture » |
| M14 | 29/09/2026 | Code en français, identifiants ASCII ; commentaires et docstrings en français avec accents ; symboles courts admis quand la spécification les nomme. | ADR 0001, pt 14 ; `docs/exigences.md` § 4.2 |
| M15 | 29/09/2026 | Cours magistral reporté au jalon J8. | ADR 0001, pt 15 ; `docs/exigences.md` § 3.6 |
| M16 | 29/09/2026 | Plateforme de référence des résultats : la CI Linux de GitHub Actions (`ubuntu-latest`), Python 3.12 géré par uv, versions verrouillées dans `uv.lock`. | ADR 0003, pt 4 ; `CLAUDE.md`, « Changements de résultats » |
| M17 | 29/09/2026 | Les pièces d'`archive/` sont versées intactes. Le source v1.5 et le cours citent des pays réels comme épisodes historiques et en bibliographie seulement, jamais dans la grille des dix configurations ; la règle est « aucun nom de pays réel associé aux configurations » ; le critère de l'issue #5 (« aucune occurrence ») est corrigé en ce sens. | ADR 0001, pt 6 ; `docs/exigences.md` § 2.9 |
| M18 | 29/09/2026 | Le gabarit de fiche comparative (`docs/blocs/0000-gabarit.md`, issue #6) est validé par le mainteneur après la fusion de la PR #7, avant la première fiche du jalon J1. Précisée par M20. | § 2 ci-dessus et § 6 ci-dessous (J1) |
| M19 | 29/09/2026 | Critères de passage des jalons J1 à J8 arrêtés (§ 6) ; le budget de calcul passe de J2 à J3, J2 ne mesurant que le coût du noyau. | § 6 ci-dessous |
| M20 | 30/09/2026 | Précise M18 : le gabarit de fiche comparative est validé **à l'usage**, éprouvé sur la première fiche (« temps et comptabilité ») puis validé par le mainteneur avec ses retouches, à la décision de cette fiche. Aucune validation préalable n'est requise pour l'ouvrir. **Fait le 30/09/2026** : gabarit retouché (retours de #15 et #16) validé par le mainteneur. | § 1 ci-dessus (issues 1 et 3 de la branche) ; ADR 0004, pt 7 (annotation) ; `docs/blocs/README.md` |
| M21 | 30/09/2026 | Organisation du jalon J1 : la première branche de travail porte la **fiche « temps et comptabilité » seule** (gabarit éprouvé, fiche instruite jusqu'à la décision, puis sa section de spécification) ; les issues d'outillage #8 à #14 font l'objet d'une **branche technique à part**, plus tard, intercalée entre deux branches de fiches (workflow `circuit-technique`). | § 1, § 2 et § 3 ci-dessus |
| M22 | 30/09/2026 | Fiche « temps et comptabilité » : **option C**, pas mensuel unique (12 pas par an, un pas = un tour, date de décision à tout pas), combinée au socle commun § 3.N de la fiche corrigé par les constats de `monnaie` : règle de conversion **linéaire unique** (taux, flux, vitesses) ; six instruments financiers et deux actifs réels, matrices des bilans et des flux en tableaux, aucun solde résiduel, valeur nette calculée deux fois ; tolérance ε = 1e−12 × échelle du bilan, par pas et en cumul ; neuf phases triangulaires ; compte du Trésor **à la banque centrale** ; **k = 0** ; résultat de la banque centrale versé **chaque tour sans troncature** ; ratio stationnaire = stock d'ouverture / (12 × flux du pas) ; émission des titres publics **après les règlements** (α), encaisse M^G stationnaire résolue. Écartés : A, B, D, E, conversion composée, Trésor à la banque, troncature du versement, émission avant les règlements (β). Réouverture par une décision M-m citant M22 si un fait établit un besoin infra-mensuel. | `docs/blocs/temps_comptabilite.md` § 8 ; ADR 0005 (accepté) ; `docs/blocs/README.md` ; `CONTEXT.md` |
| M24 | 02/10/2026 | Fiche « production et stocks » : **option C**, socle commun § 3.N de la fiche (forme du modèle DIS de Godley et Lavoie, 2007, chap. 9, lue par reproductions, avec cinq modifications motivées) à **bien unique, J = 1**, équations indexées par j dès le socle. Lectures, toutes en (i) : (a) stocks valorisés au **coût moyen pondéré** (conforme à `sec:cadre` l. 520, sans réévaluation) ; (b) **ordre interne de la phase 4 « travail, puis production »**, l'emploi effectif tenu par le bloc 3 et lu par le bloc 2 — modifie un contrat partagé (`tab:phases`), décision citant M22, **ADR 0007** ; (c) anticipations assises sur la **demande adressée**, servie ou non ; (d) **J = 1** ; (e) capacité normale du capital tenue comme **indicateur sans plafond** ; (f) conversion **linéaire** de la croissance de productivité, g_pr/n_a, croissance effective (2,0184 % pour 2 %) publiée ; (g) rationnement **proportionnel** au socle, la priorité de l'État relevant d'un levier éventuel du mode planifié (J7). Q4 : volume du capital au bloc 2, ajustement de l'emploi au bloc 3, à confirmer par les fiches 3 et 6. Conditions : les cinq réserves de `macro` (seuils écrits avant l'essai, J3 ; remesure S1 dont le verdict ne change pas la décision) et les sept conditions de restitution de `jeu` (fiche § 7), pour le § 9. Écartés : A (v1.5) et B (v2.0), qui échouent au critère 4 (ratio stocks / ventes dépendant des vitesses) et aux critères 1 (b) et 3 (b), B ayant en outre une borne active à l'état stationnaire et un cycle propre de 6 ans ; D (J = 2), qui n'ajoute aucune identité vérifiable et paie un prix relatif à stabiliser sans levier qui l'exploite ; la valorisation au coût courant ; l'ordre « production, puis travail » ; le plafond de capacité ; la priorité de l'État au socle. Issue liée : #37. Recommandations concordantes de `macro` (§ 5) et de `jeu` (§ 7). *Lecture (f) révisée par M25, lecture (b), le 03/10/2026 (conversion géométrique de g_pr ; ADR 0008, partie I).* | `docs/blocs/production.md` § 8 ; ADR 0007 (lecture (b)) ; `docs/blocs/README.md` ; § 5 ci-dessous (piste « deux secteurs ») |
| M23 | 30/09/2026 | Routage du modèle et de l'effort d'`architect`, `macro`, `monnaie` et `jeu` : Opus par défaut (effort `medium` en routine, `high` en jugement, fiches `-approfondi` générées), Fable réservé aux cas de `docs/agents/routage.md` § 4.1 ou à l'accord du mainteneur, plafonds d'escalade, lecture ciblée, retour structuré, journal local des sous-agents, trace des escalades hors branche (section « Escalades, relances et arrêts hors branche ») ; politique du modèle `Modele_vibe_code` adaptée au projet. Branche `claude/routage-modele-effort` (PR #22), ad hoc, sur instruction du mainteneur : pendant qu'elle est ouverte, la PR #22 n'est pas la PR d'une branche de travail ; la branche de travail reste `claude/j1-temps-comptabilite` (PR #20) ; les consultations faites pour #22 sont tracées dans la PR #22 et comptent pour son propre plafond Fable. Numéro M23 retenu parce que M20 à M22 sont pris par la PR #20. **Confirmée par le mainteneur le 02/10/2026** (point d'étape après la PR #20) : la présente ligne, y compris les constats de la relecture d'`architect-approfondi` retenus le 02/10/2026 (`b81265d`, `14f86f5`, `b331ee3`, `a554cf4`) ; l'ouverture de la PR #22 en parallèle de la PR #20 est une exception ponctuelle à la règle « une seule branche de travail à la fois », **sans valeur de précédent** ; termes de routage de `CONTEXT.md` confirmés, complétés le même jour (« Relance ciblée » ; une consultation Fable reste de niveau « jugement »). | ADR 0006, `docs/agents/routage.md`, `CONTEXT.md` |
| M25 | 03/10/2026 | Fiche « travail et salaires » : **option C**, rétention asymétrique avec terme de tendance, **λ_N = 3,5 par an** (demi-vie de 2,01 tours), salaire **SN** (avec niveau), sous la **lecture (i)** du critère 10 (b) : retard d'emploi établi par les sources lues ; forme asymétrique, non établie, déclarée comme approximation dans les `\limites` (réserve 9). Lectures : (a) anticipation lue **à l'ouverture** ; (b) lecture commune **(G)** des taux annuels pour les fiches 3, 4 et 8, conversion **géométrique**, (1 + x)^{1/n_a} par pas, des taux de croissance et d'inflation, les taux d'intérêt, flux et vitesses restant linéaires (M22 (a)) — **révise M24 (f)** et `sec:cadre-calendrier`, décision citant M22 et M24, **ADR 0008**, partie I ; (c) norme ω* = 1/(1 + μ̄), lecture **(w1)**, (w2) renvoyée au J4 ; (d) population active en tendance exogène, **tenue par le bloc 3** ; (e) Q4 de la fiche 2 confirmée (emploi au bloc 3) ; (f) aucun levier propre. **Bande commune** du test zéro sur la part salariale (fiches 3 et 4) : centrée sur la valeur résolue de ΣWB/ΣVA sur 12 tours (0,7989 à π̄ = 2 %). Conditions : neuf réserves de `macro` (§ 5, seuils écrits avant l'essai) ; conditions de restitution de `jeu` (§ 7) ; C1 à C8 transmises à la fiche 8 (§ 6.3) ; règle de salaire sur le dernier prix connu (constat T2). Écartés : A et B (critères 4 et 5 (b), révision de M24) ; D (critère 5 (c)) ; SP (critère 5 (b)) ; R, gardée comme référence sans retard mais contredite par le retard établi. Remesure T1 proposée, non lancée, sans effet sur la décision. Issues créées : #44, #45, #46. Prise par paire avec M26. | `docs/blocs/travail.md` § 8 ; ADR 0008, partie I (accepté le 03/10/2026) ; annotation de l'ADR 0005 ; `docs/blocs/README.md` ; `CONTEXT.md` |
| M26 | 03/10/2026 | Fiche « prix » : **option M**, prix égal au coût unitaire UC majoré d'une marge rappelée vers la marge normale μ̄, avec un terme de stocks ξ. Base UC, **UC écrit par le bloc 2 en phase 2** ; aucune anticipation consommée ; partage ancré par μ̄, avec (w1) à la fiche 3 ; aucun terme en taux d'utilisation : la variante T est transmise à la fiche 6, à décider au plus tard à M28 (#37) ; prix administrés renvoyés au J4 et au J7. **Phase de P_t, lecture (c)** : l'indice est le prix du tour, les règles le lisent au tour suivant — modifie l'ADR 0005, pt 16, décision citant M22, **ADR 0008**, partie II (forme : registre de 13 niveaux, point II.3, retenu à l'acceptation de l'ADR le 03/10/2026) ; **clause de réouverture** vers (b) si l'analyse C10 de la fiche 8 montre que le délai d'un tour est déterminant à la calibration retenue (décision citant M26, M24 et M22). Lecture (G) et bande commune de part salariale : décidées avec M25. Conditions : réserves de `macro` (§ 5, seuils écrits avant l'essai), dont le test d'alternance étendu à la variation mensuelle du prix ; conditions de restitution de `jeu` (§ 7) ; C9 à C13 transmises à la fiche 8 (§ 6.4) ; seuil du critère 10 (d) proposé par `jeu` (0,2 point pour +1 %, 1,0 point pour +5 %), à confirmer avant le J4. Écartés : A et B (critères 4, 7 et 11 ; B viole λ ≤ n_a et a un état caché) ; C (variation mensuelle alternée, explosive dès que les vitesses doublent) ; D (sensible à un défaut des anticipations, marge contracyclique contestée) ; R, gardée comme référence ; coût complet et marge sur cm (critère 3 (d)) ; lectures (a) et (b) de P_t. Remesure P1 proposée, non lancée, sans effet sur la décision. Issues créées : #47, #48. Volet « prix » de #24 tranché. Prise par paire avec M25. | `docs/blocs/prix.md` § 8 ; ADR 0008, partie II (accepté le 03/10/2026) ; annotation de l'ADR 0005 ; `docs/blocs/README.md` ; `CONTEXT.md` |
| M27 | 03/10/2026 | Fiche « ménages » : **option C**, cible de richesse avec terme de tendance, ménage représentatif ; Q10 en **lecture (c)** sur la cible déclarée π\* (jamais π̄), réouverture vers (b) par la seule clause C26 ; **cible de richesse sur le revenu de Haig-Simons** (π_s lu sur π\*) ; plafond du plan en phase 2, B_H ≡ 0 au socle, canal du taux rentier seul, taux d'épargne restitué nominal et corrigé. Correction prospective du critère 4 (ii) (#59). Recommandation concordante de `macro`, `monnaie` et `jeu` | `docs/blocs/menages.md` § 8 |
| M28 | 03/10/2026 | Fiche « investissement et financement » : **option S-ζ** (part d'investissement visée, taux d'utilisation visé fonction du taux réel du crédit ; ζ déclaré, calibré au J3), règle de financement **F** (levier sur K comptable, cible de dépôts, dividende résiduel) ; lecture (a) de Q7, i_L lu à l'ouverture, ϱ_L sur π\*, **voie (i)** de #36, aucun levier d'offre (#37 ouverte jusqu'au J7), Div ≥ 0 en contrainte de domaine ; C36 dans la rédaction de `monnaie` ; seuils (d1) à (d3) du critère 12 (d) ; C37 transmise à la fiche 9 | `docs/blocs/investissement.md` § 8 |
| M29 | 03/10/2026 | Contrat des phases (citant M22, M27 et M28) : en phase 9, après les identités du noyau et avant l'avancée du registre et le passage au pas suivant, les blocs déclarés écrivent leurs variables d'état du pas suivant, sans flux et sans lecture mutuelle, les montants exécutés du pas se lisant au grand livre en lecture seule ; T_{F,t} (bloc 6) et YD_t (H7, bloc 5) retenus en phase 9 ; ménages retirés des écrivains de la phase 7 au socle. Lecture (i) d'`architect`, acceptée après relecture Fable (consultation 1 sur 3) | ADR 0009 ; fiches 5 et 6 § 9.10 ; `CONTEXT.md` |
| M30 | 03/10/2026 | Cible d'inflation en vigueur et facteur Γ^e (citant M27 et M28) : π\*_t variable d'état par pays, lue à l'ouverture par les blocs (délai d'un tour), écrite en phase 1 (reconduite par le moteur jusqu'à la fiche 8, puis écrite par le bloc 8) ; Γ^e = [(1 + g)(1 + π\*_t)]^{1/n_a} grandeur du moteur calculée une fois par pas (`eq:moteur-croissance-nominale-attendue`) ; Γ̂ supprimé. Rédigé par Fable dans la consultation 1 sur 3 ; accepté avec ses points de forme 3, 4 et 6 | ADR 0010 ; fiches 5 et 6 § 9.10 ; #61 ; `CONTEXT.md` |
| M31 | 04/10/2026 | Fiche « banque commerciale » (#71) : **option C**, socle commun § 3.N de la fiche — taux des crédits et des dépôts à écart constant du taux directeur, écrits en phase 8 (c) et lus au tour suivant (i_L, i_D variables d'état du bloc 7) ; ligne 21 décidée sur la position nette de réserves (Res·L^CB = 0 à la clôture, sans paramètre) ; fonds propres ancrés à ϑ·L par un dividende résiduel versé le tour même ; crédit à la demande ; entrées de scénario ς_L et ς_B ; aucun levier bancaire au socle. Lectures (a) à (e), (g), (h) selon l'avis commun de `monnaie`, `macro` et `jeu` ; (f), propriétaire des lignes 19a, renvoyée à M33. Conditions C38 à C44 (`macro`) et neuf conditions de restitution (`jeu`). Fiche `docs/blocs/banque.md`, § 8. |
| M32 | 04/10/2026 | Fiche « banque centrale et anticipations » (#72), par paire avec M33 : **option C** — action intégrale sans fuite sous Fisher sur π\*, a_π = 0,5, k_I = 0,25/an, anticipation adaptative λ_e = 0,2/an en phase 1, sans crédibilité ni plancher, corridor nul, E^CB_0 = 0, fermeture monétaire (#44, lecture (1)) ; π\* paramètre au socle et au J4 (ouverture du levier après #54 et deux critères de `jeu`). **Critère 13 (C15) : défaut connu déclaré** (voie (c)), critère gardé, échec attendu au J3, issue de suivi ; aucune réouverture. Fiche `docs/blocs/banque_centrale.md`, § 8. |
| M33 | 04/10/2026 | Fiche « État et dette » (#73), par paire avec M32, citant M22, M25, M28, M29 et M31 : **option C-HS** (reprise réelle intégrale des intérêts, T9 réel ; impôt sur le revenu de Haig-Simons retardé ; dépense indexée sur la production potentielle ; valeur par défaut des leviers) ; **couverture des intérêts en levier distinct du barème, à deux valeurs** (lecture du critère 19) ; **A8** (lignes 19a au bloc 9, s_CB écrit par le bloc 8 en phase 1 ; ADR d'architecture à rédiger, consultation Fable) ; **i_B ≡ i_CB** ; contrôle de caisse en lecture nette (deux conditions d'`architect`) ; **M^G\* = m × paiements bruts, m > 1** fixé avant l'essai sur la propriété de `jeu` (modification de la l. 502, l. 2064 et de l'ADR 0005 pt 13) ; critère « −2 points » de la fiche 6 lu sur le taux directeur, écarts constants. Fiche `docs/blocs/finances_publiques.md`, § 8. |
| M34 | 17/11/2026 | Calibration du socle (branche « calibration », PR #162 ; P206), sur le dossier du § 7 de `docs/blocs/calibration.md`, avis des experts retenus pour chaque question du § 7.13 et du § 7.16 : **table T1** — μ̄ = 0,60 (#92), ζ = 8 (#55), ϑ = 0,15 (#130 ; ϖ_L = 0,02, ϖ_D = 0,01, r̄ = 0,01 inchangés et sourcés), ν_H = 1,1 et λ_H = 0,4 (#62), λ_w = 0,18 et β = 2 (#45), autres paramètres inchangés ; **visa du tableau prédit** : colonnes E1 (#92, #55), E2 (#130), E3 (#62, #45) du § 7.5, référence « mesuré égal au prédit à 1e−9 » de chaque commit ; **λ_w commité au rang 7**, coût de désinflation publié « non calibré, #163 », **condition : #163 traitée avant la démonstration J4** ; **ligne 17** republiée à la table de M34 (formulation du § 7.13 q. 4) et issue du § 7.14 créée (#168) ; **C62** : formulation du § 7.7 (remplace P222 et P232), retouche « stable, quasi neutre (demi-vie ≈ 125 ans) » à π̄ = 0 soumise à `jeu` ; critère des valeurs prédites nulles et critère des tests C62 à 720 pas (§ 1, précisions prospectives) ; **dette de référence publiée sans cible** (réserve de `monnaie` sur les seuils futurs de la prime) ; 26 chiffres de la maquette versés à la surface de #92 ; ROE publié « brut, nominal, sans charges » ; lien canal rentier ↔ rayon mesuré au rang 8 ; points ouverts du § 7.13 q. 9 sans effet sur la table. | `docs/blocs/calibration.md` § 7 ; PR #162 |

**Décisions sans numéro M et points P1 à P73, D1 à D13, G1, F2, S1, S2** : historique, partie A, § 4. Elles restent en vigueur tant qu'aucune décision ultérieure ne les remplace ; celles que cite la branche en cours sont rappelées au § 1 par leur numéro (J3-e1 : P61, P84, P161, P175, P209, P211, P212 ; branche « calibration » : P43 (a), P57, P98, P115, P148, P151, P177, P184 ; branches antérieures : P41 (a), P51, P52, P53, P56, P62, P72).

**Décisions P74 à P171** : historique, parties B à F, § 4 et compléments (texte inchangé ; plage par partie : « Lecture des renvois »), en vigueur ; anciens paragraphes de renvoi : partie G, complément du rang 1 de la calibration.

### Décisions P200 et suivantes (branche « calibration »), 16/11/2026

P182 à P199 et les points ouverts du rang 9 de la branche « forme du code » : historique, partie G, § 4 (sortis le 16/11/2026, texte inchangé), en vigueur ; P172 à P181 et les questions Q1 à Q8 qui les fondent : historique, partie F, complément du rang 9.

P200 à P203 (ouverture, #157 à #161, m1, ADR 0014) et P213 à P224 (ci-dessous) : historique, partie G, complément du rang 1 de la calibration (texte inchangé), en vigueur.

P204 à P212 (plan, questions Q1 à Q9 du 16/11/2026) et P225 à P241 (rangs 1 à 8) : historique, partie G, complément du rang 11 de la calibration (texte inchangé), en vigueur. **Index** : P204 #45 réduite à λ_w, C7 dans #163 ; P205 fiche transverse `docs/blocs/calibration.md` ; P206 décision unique M34 et visa du tableau prédit (1e−9) ; P207 #143 instruite sans `Closes` ; P208 source « non trouvée » déclarée ; P209 valeurs résolues de `tab:criteres-j3` ; P210 une référence d'empreintes par commit ; P211 délégation P175 reconduite ; P212 découpage de J3-e à J3-g (§ 2) ; P225 et P226 #130 (ϑ = 0,15 ; ϖ_L, ϖ_D, r̄ sourcés) ; P227 #167 ; P228 et P229 délégation pendant l'absence du mainteneur, issues sur accord ; P230 et P232 C62 et λ_w = 0,18 ; P231 fin du rang 1 ; P233 ν_H = 1,1, λ_H = 0,4 ; P234 `BORNES_MARGE_HAUSSE` (écart au critère « Diff » accepté, `3c8156e`) ; P235 amas des racines nulles (`399323c`) ; P236 horizon prospectif des critères de vitesse ; P237 #139 en échec attendu ; P238 `BORNES_MARGE` [1 ; 3] ; P239 variantes λ_w relatives ; P240 #169, #170 ; P241 lectures de C62.

P213 à P224 (rang 1, instruction ; `docs/blocs/calibration.md`, P205) : #92, P213 et P214 (§ 1 ; #164) ; #143, P215 à P217 (§ 2 ; commentaire sur #143) ; #55, P218 à P224 (§ 3, § 3.13 ; #164, #165, #166, PR #162). Texte inchangé : historique, partie G, complément du rang 1 de la calibration.

### Décisions P242 et suivantes (point d'étape après la PR #162, rangs 0 et 1 de J3-e1), 26/11/2026

Points (a) à (d) soumis au mainteneur au rang 11 de la calibration (texte du 17/11/2026 : historique, partie H, § 4), tranchés par le mainteneur le 26/11/2026 selon l'avis proposé.
- **P242** (a) : **exception consignée au découpage par domaine.** Un commit `docs:` qui republie des valeurs peut modifier, dans `outils/`, les littéraux de valeurs publiées que `test_valeurs_en_vigueur_ecrites_hors_barre_dans_leur_source` (`tests/unitaires/test_etat_stationnaire.py`) lie au texte : les séparer ferait échouer la batterie au commit intermédiaire. La règle sera écrite dans `CLAUDE.md` par la session (`claude:`), sur accord du texte proposé (Q11). Hors de l'exception, deux changements avaient été relevés au point (a) : trois boucles de `releve()` restructurées (`4eb70a5`) et un libellé de provenance (`82481d7`) ; leur traitement est soumis au mainteneur (Q11).
- **P243** (b) : trois changements de structure non déclarés au critère « Diff » de la calibration sont **mentionnés à l'historique, sans autre suite** : `ENTREES_D_ORIGINE` et la contre-épreuve (`d7163ca`) ; les libellés `roe` et `marge_nette` (`3c8156e`) ; `frontiere_ou_aucune` (`ce3662a`). Mention portée au § 7, ligne de la PR #162.
- **P244** (c) : les chaînes `source` des tables qui citent « États-Unis » ou « zone euro » sont **compatibles avec M17** : elles donnent la provenance d'une donnée, pas une configuration de pays. Relevé à `831547c` (`src/nations/moteur/parametres/`) : `banque.py:39`, `:41` et `:55`, `investissement.py:78` et `:82`, `menages.py:63`, `prix.py:40`, `travail.py:43` et `:48`. Liste du 17/11/2026 : historique, partie H, § 4.
- **P245** (d) : **trois issues créées par la session le 26/11/2026** : #171 (remesure à T1 des chiffres « à la calibration indicative », `macro`), #172 (robustesse des outils de calibration après M34) et #173 (libellé « Δr̄_α au minimum en ζ (ζ = 68) »). Rattachement proposé : § 2, ligne 12 bis (Q10).

Questions Q1 à Q12 du plan de J3-e1 (compte rendu du rang 0, PR #174), tranchées par le mainteneur le 26/11/2026, toutes selon l'avis du plan.
- **P246** (Q1) : périmètre de J3-e1 : #175, #176, #115 et #122 avec `Closes` ; #125 points 3 à 5 sans `Closes` ; point 6 de #125 en J3-e2 (écart à P212 assumé).
- **P247** (Q2) : **forme R1**. Le résolveur en formes fermées passe dans `src/nations/scenarios/`, fonction pure, importée par `outils/etat_stationnaire.py` ; R2 à R4 écartées (ADR 0015).
- **P248** (Q3) : **A1 contrôle la transcription, A2 l'équilibre des règles**, déclaré avant l'essai ; le critère 5 de la fiche 9 se lit de même (ADR 0015, pt 2 ; ADR 0005, annotation du 26/11/2026).
- **P249** (Q4) : critères de la branche : A1, A2, B, plus F1 et C1 ; F2 en J3-f1, avec S1.
- **P250** (Q5) : non-régression identique au bit contre `ce3662a`, et sortie du script identique à l'octet.
- **P251** (Q6) : contrôle de #122 dans le schéma d'état (ADR 0015, pt 12 ; ADR 0014, annotation du 26/11/2026).
- **P252** (Q7) : formes fermées sans label `eq:`, renvoi à `sec:<bloc>-stationnaire` en commentaire.
- **P253** (Q8) : une consultation Fable pour l'ADR 0015, faite au rang 1 (1 sur 3).
- **P254** (Q9) : délégations P175 et P211 reconduites.
- **P255** (Q10) : ligne 12 bis « suites de M34 » (#168, #170 à #173), après J3-e1.
- **P256** (Q11) : règle de P242 écrite dans `CLAUDE.md` (`eed2d31`) ; `4eb70a5` et `82481d7` en simple mention, sans autre suite.
- **P257** (Q12) : N1 et N2 créées par la session le 26/11/2026 : **#175** et **#176**.
- **P258** (26/11/2026) : **ADR 0015 accepté**, points S1 à S10 selon les avis de l'ADR. S1 : exemption fermée du test « conversion unique » pour le module feuille (modifie l'ADR 0014, F2). S8 : référence de la sortie du script = sha256 `fb187be113c513ea17c74ded4339d206ae6a38faa40b7b3c3c2478c2a983e088` (205 933 octets), remesurée par la session à `f97cc6f`, script inchangé depuis `831547c` ; #175 corrigée le même jour.

**Points ouverts au 26/11/2026** :
- condition de M34 : **#163 traitée avant la démonstration J4** ;
- marge du noyau seul sur l'exécuteur lent (#110, J3-g1) ;
- déjà ouverts : plancher du taux directeur (P181), durée d'une partie (#155), #11, #14.


## 5. Pistes à instruire dans les fiches comparatives (aucune n'est décidée)

Ouvertes par M2 et M3 ; texte complet (motifs, pistes tranchées : pas mensuel unique, retenu par M22 ; deux secteurs, écartée par M24) : historique, partie B, § 5. Pistes encore ouvertes : consommation à cible de richesse (ménages), corridor de taux explicite et loi de crédibilité ou apprentissage à gain constant (banque centrale), prix au coût normal majoré (prix), encours hypothécaires par strate (actifs et crises, J6).


## 6. Jalons

Critères de passage arrêtés par le mainteneur le 29/09/2026 (M19). La colonne « État » est condensée ; son historique est dans l'historique, partie A, § 6. Lignes de J0 à J2, jalons passés : historique, partie G, complément du rang 1 de la calibration.

| Jalon | Contenu | Critère de passage | État |
|---|---|---|---|
| **J0 à J2** (fondations, socle, noyau) | Contenu et critère : voir ci-dessus | — | **Passés** : J0 le 30/09/2026 (PR #7, `facf97f`), J1 le 07/10/2026 (PR #85, `833afd9`), J2 le 15/10/2026 (PR #99, `2e643a2`). |
| **J3 Économie fermée** | Blocs du socle, état stationnaire résolu, test zéro, premières références de non-régression | Critères d'O1 fixés **avant l'essai** et confirmés par le mainteneur (point de départ : critères du 16/09/2026, `docs/exigences.md` § 1.3) ; test zéro réussi sur les deux fenêtres pour plusieurs graines ; budget ≤ 1 ms par pays-semaine mesuré sur le socle complet, sur la plateforme de référence (M16) ; références régénérées après visa. | **En cours depuis le 15/10/2026** : J3-a fusionnée (PR #109, `204ab2d`), J3-b fusionnée (PR #117, `688f299`, 14/11/2026), J3-c fusionnée (PR #129, `731aac3`, 14/11/2026), J3-d1 fusionnée (PR #136, `30078bb`, 15/11/2026), J3-d2 fusionnée (PR #146, `2744be3`, 16/11/2026 ; bloc 9, socle complet) : neuf fiches sur neuf implémentées ; branche « forme du code » fusionnée (PR #151, `890471b`, 16/11/2026) ; branche « calibration » fusionnée (PR #162, `831547c`, 26/11/2026 ; M34, table T1) ; J3-e1 en cours, plan décidé (§ 1 ; P246 à P257) ; découpage de J3-e à J3-g décidé au § 2 (P61, P177, P212) ; découpage J3-a à J3-g au § 2 (P61, P85). Critères de J3 arrêtés avant l'essai le 15/10/2026 : `tab:criteres-j3` (`sec:calibration`), D12 sur #107. |
| **J4 Simulateur utilisable** | Scénarios, leviers, rapports en ligne de commande, catalogue des effets des leviers | O2 : pour chaque levier, scénario apparié du signe attendu avec délai et distribution ; O5 : démonstration au mainteneur sur des scénarios de 5 à 10 ans ; avis de `jeu` ; revue d'`app-review`. | À venir |
| **J5 N pays** | Commerce, change, balance des paiements, régimes A à E, barrières entre pays | O4 : tests d'invariance sur les deux fenêtres (5 et 60 ans) — pays seul contre monde à un pays, unité monétaire (×100), permutation des pays, reprise de sauvegarde — à 1e-12 relatif à l'échelle du bilan, aucun solde de bilan calculé comme résidu ; balance des paiements bouclée exactement à chaque pas (somme mondiale des soldes courants et financiers nulle) ; chaque régime A à E expose ses leviers et eux seuls (un test par régime) ; budget ≤ 1 ms par pays-semaine avec au moins quatre pays. | À venir |
| **J6 Actifs et crises** | Blocs actifs et crises financières ; grille des dix configurations en tests | O3 : pour chaque type de crise retenu, précondition, contrefactuel, signal précurseur, intervention, reprise sans effacement gratuit ; **`archive/` supprimée au plus tard à la fin de J6** (M6). | À venir |
| **J7 Web, puis jeu** | Serveur, client web, tours mensuels, plusieurs joueurs, IA des pays non joueurs, conditions de fin | Mêmes résultats, bit à bit, en ligne de commande et par le web à graine et décisions égales (test) ; aucun calcul économique hors du moteur, vérifié par `app-review` ; O5 : partie complète menée par le mainteneur, au moins deux joueurs et une IA, jusqu'à une condition de fin ; reprise d'une partie sauvegardée identique ; revue de jouabilité de `jeu` avant la démonstration. | À venir |
| **J8 Cours** | Dérivations des volumes 1 et 2 corrigées et alignées sur la spécification v3 ; table de correspondance générée par script | Chaque chiffre du cours produit par un test ou un script, jamais recopié (les corrigés faux relevés le 29/09/2026 corrigés) ; chaque équation porte son statut *dérivée / approchée / choix de conception* et renvoie à son label de la spécification ; table de correspondance cours ↔ spécification générée par script et contrôlée en CI ; relecture de fond de `macro` et `monnaie`. | À venir |

## 7. Branches fusionnées

Détail des issues, commits, décisions et escalades de chaque branche jusqu'à J3-a : historique, partie A, § 7. Lignes de ces branches (`claude/fondations`, PR #7, à `claude/j3-maquette-criteres`, PR #109) : historique, partie B, § 7. Lignes de `claude/correctif-litteral-12` (PR #118), de J3-b (PR #117) et des correctifs CR2 et CR1 (PR #127, #128) : historique, partie D, § 7, et corps des PR. Ligne de J3-c : historique, partie E, complément du rang 8 de J3-d2. Ligne de J3-d1 : historique, partie F, § 7. Ligne de J3-d2 : historique, partie G, § 7. Ligne de la branche « forme du code » (PR #151) : historique, partie H, § 7. Pour J3-c, J3-d1 et J3-d2 : historique, parties C, E et F, § 1, et corps des PR #129, #136 et #146.

| Branche | PR | Jalon | Fusion | Détail |
|---|---|---|---|---|
| `claude/j3-calibration` | #162 | J3 (calibration) | 26/11/2026, 06:33 UTC, commit de fusion `831547c` (parents `890471b`, `e60edb5`), par le mainteneur | Issues fermées par `Closes` : #92, #55, #130, #62, #45 et #166 (ajoutée au périmètre, P223) ; fermetures vérifiées par la session le 26/11/2026. 49 commits hors fusion : 12 `code:`, 11 `tests:`, 26 `docs:` (`git rev-list --no-merges 890471b..e60edb5`). **Erratum** : la ligne d'attente (historique, partie H, § 7) annonçait « 57 commits à `6f419bf` (34 `docs:`) » ; la même commande donne 47 commits à `6f419bf`, dont 24 `docs:`. Fiche, rangs et SHA : historique, partie H, § 1, et corps de la PR #162. Décision M34 (table T1) ; P204 à P241 ; P242 à P245 au point d'étape. Fable : 0 sur 3. L'état stationnaire de référence change, visé (M34). Références d'empreintes `59e1c1b` et `ce3662a` ; les empreintes à `831547c` sont identiques à `ce3662a` (code 0, 26/11/2026). `tests/references/` absent. Écarts au critère « Diff » mentionnés sans suite (P243) : `d7163ca`, `3c8156e`, `ce3662a` ; exception au découpage par domaine : P242. Condition de M34 : **#163 traitée avant la démonstration J4**. Branche suivante : J3-e1 (§ 1). |

## 8. Escalades, relances et arrêts hors branche

Consultations faites hors de toute branche ouverte (`docs/agents/routage.md`, § 7) ; une consultation Fable compte pour la branche suivante (`docs/agents/routage.md`, § 5.2). Lignes antérieures au 13/11/2026 : historique, partie A, § 8 ; ligne du 13/11/2026 : partie B, § 8 ; lignes du 14/11/2026 et du 15/11/2026 (rang 0 de J3-d2) : partie E, § 8.

Aucune ligne depuis le 15/11/2026, rang 0 de J3-d2.
