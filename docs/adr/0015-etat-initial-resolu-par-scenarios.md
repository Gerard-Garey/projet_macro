---
status: accepted
date: 2026-11-26
---

# `scenarios/` résout l'état initial : un résolveur en formes fermées, module feuille de `src/`, appelé par deux adaptateurs (tables du moteur, script), sans drapeau de mode ; A1 contrôle la transcription, A2 l'équilibre des règles

> **Statut « accepté » le 26/11/2026, par décision du mainteneur** (P258 : S1 à S10 acceptés selon les avis de l'ADR, S8 avec la référence remesurée par la session, sha256 `fb187be1…`). Texte d'origine du statut : « proposé », à accepter par le mainteneur. Rédigé par `architect-approfondi` (Fable, consultation 1 sur 3 de la branche, autorisée par P253 ; `docs/agents/routage.md` § 4.1.3) au rang 1 de J3-e1 (`claude/j3-e1-etat-initial`, PR #174, tête `eed2d31`). Les points 1 à 5 de la Décision consignent des décisions **arrêtées** par le mainteneur le 26/11/2026 (P247 à P252) ; leur rédaction détaillée (au point 2 : côté du moteur mesuré par A1, limite d'A2 le long d'un continuum) est celle d'`architect` et s'accepte avec l'ADR. Les points 6 à 14 en sont la mise en forme, **proposée** ; les points que le mainteneur doit accepter ou trancher sont repris sous « Points soumis ».

## Contexte

L'ADR 0002 (pt 6 et 13) et `docs/exigences.md` § 2.6 demandent un état initial **résolu comme équilibre des règles**, d'où part le test zéro. Mesures à la tête `eed2d31` (code identique à `main` = `831547c` : `git diff --stat 831547c HEAD` ne touche que `CLAUDE.md` et la feuille de route) :

- `src/nations/scenarios/` ne contient que son `__init__.py` (une docstring). L'état d'ouverture de tous les bancs est construit dans `tests/invariants/socle_partiel.py` (`sentier`, l. 182 ; `parametres_du_sentier`, l. 621 ; `etat_initial`, l. 663), à partir de `outils/etat_stationnaire.py` chargé par son chemin (`script()`, l. 142). Le moteur ne résout rien : le critère A1 de `tab:criteres-j3` et le critère 5 de la fiche 9 sont sans objet (P161).
- Les formes fermées sont dans le script : `facteurs`, `rho_IN`, `rho_K`, `etat_stationnaire` (l. 459), `controler_etat` (l. 591), `ouverture` (l. 627). Elles lisent **28 des 42 champs** de sa classe `Parametres` ; les 14 autres sont les douze vitesses et gains de `VITESSES` (l. 291), et ς_L, ς_B (relevé sur l'arbre syntaxique des six fonctions, 26/11/2026). L'état `e` a 89 clés, l'ouverture 35, le registre 13 niveaux à n_a = 12.
- Le script appelle ces formes **hors du domaine des tables du moteur** : n_a ∈ {4 ; 12 ; 52} (`POINTS_NA`), alors que `conversions.par_pas` et `facteur_par_pas` lisent la constante `PAS_PAR_AN` (12 ; `conversions.py`, #120) ; ν_G = 1, point de référence que la table refuse (ν_G > 1, `parametres/finances_publiques.py:45`) ; `r_neutre` et `rho_bar_L` donnés (mesure (α) de #80, l. 1472, 1562, 2368) ; contrôle des conditions coupé (`controler=False`, l. 1472 et 2368 ; `controler=(cfg == "R")`, l. 1740 ; quinze sites dans `tests/unitaires/`).
- Le script se déclare indépendant de `src/` (docstring, « Indépendance » ; ADR 0005, pt 20), ce que tient `test_n_importe_que_la_bibliotheque_standard` (`tests/unitaires/test_etat_stationnaire.py:109`).
- Le test « conversion unique » (`tests/invariants/test_conversion_unique.py:286`) parcourt tout `src/` et n'admet une division par n_a ou une puissance en 1/n_a que dans deux listes fermées (les deux conversions, le calendrier ; ADR 0014, F2). Les formes fermées en contiennent à chaque étape. Les réécrire avec les conversions du moteur change des bits : δK/n_a contre `par_pas(δ)`·K diffère d'un ulp aux trois π\* ; Γ̄ = ((1 + g)(1 + π̄))^{1/n_a} contre f(g_pr) f(g_N) f(π\*) diffère d'un ulp à π\* = 10 % (mesure du 26/11/2026).
- La table `finances_publiques` porte déjà un littéral de valeur résolue : θ_G = 0,22058388898746367 (`parametres/finances_publiques.py:53`), égal au bit au θ_G du script à π\* = 2 % (`tests/unitaires/test_parametres_du_bloc_9.py:94`). θ_G résolu diffère aux trois π\* (`0x1.c1b0c4498a8c1p-3`, `0x1.c3c17c69ce222p-3`, `0x1.c2f14056c04f1p-3`).
- Le contrôle du graphe d'imports ne contraint que `noyau`, `etat` et `observation` (`tests/unitaires/test_observation.py`, `IMPORTS_ADMIS`).
- Références de non-régression mesurées le 26/11/2026 : `uv run python outils/empreintes_des_bancs.py --comparer outils/empreintes_des_bancs_ce3662a.json`, code 0, empreinte globale `b8cbd18d…` ; sortie standard de `uv run python outils/etat_stationnaire.py`, 205 933 octets, sha256 `fb187be113c513ea17c74ded4339d206ae6a38faa40b7b3c3c2478c2a983e088`, deux exécutions identiques. **La valeur `a0970c9f…` consignée au rang 0 et dans #175 n'est pas reproduite** ; cause non établie (point soumis S8).
- Coût : une résolution suivie de l'ouverture prend 10,9 µs (script, n_a = 12, meilleure de cinq séries de 2 000 appels, poste de la session ; mesure indicative, hors plateforme de référence).

## Décision

### Arrêté par le mainteneur le 26/11/2026

1. **Forme R1** (P247). Le résolveur en formes fermées passe dans `src/nations/scenarios/`, comme fonction pure ; `outils/etat_stationnaire.py` l'importe au lieu de le contenir. Les formes fermées n'ont qu'une maison.
2. **Portée d'A1 et d'A2** (P248), déclarée avant tout essai (aucun des deux critères n'a été exécuté, #176).
   - **A1 contrôle la transcription.** Pour chaque valeur de `tab:etat-stationnaire`, à t = 0 et π\* ∈ {0 ; 2 ; 10 %}, la valeur du script (sur ses `Parametres`) est comparée à la même grandeur **mesurée côté moteur**, à 1e−9 relatif : sur l'`EtatPays` et les tables rendus par `scenarios/` pour un stock d'ouverture ; sur le pas 0 exécuté par le moteur pour un flux. Pour les stocks d'ouverture, les deux côtés partagent désormais les formes fermées : A1 n'y contrôle plus l'algèbre, mais la chaîne tables → entrées → état résolu → `EtatPays` (correspondance des noms, type et unité des taux, registre, V^flux, normalisation, θ_G reporté dans la table).
   - **A2 contrôle l'équilibre des règles.** C'est la stationnarité exacte du moteur depuis l'état de `scenarios/` (chaque pas de P puis de L, B1 à B26 et r̂\*, 1e−9 ; grandeurs nulles à 1e−12 S) qui établit que l'état est un équilibre : l'algèbre indépendante des formes fermées est celle des blocs. **Limite déclarée** : le long d'un continuum d'équilibres, tout point est stationnaire et A2 ne distingue rien ; ce qui tient alors est la convention de sélection déclarée (point 10), sa transcription (A1) et les valeurs publiées (script contre spécification, à la dernière décimale).
   - Restent indépendants du résolveur et hors de `src/` : `un_pas`, `residus_des_regles`, `matrices` et la table des valeurs publiées du script.
   - Le critère 5 de la fiche 9 (dette consolidée du J1 « égale au moteur à t = 0 ») se lit de même. L'ADR 0005, pt 20, est annoté en ce sens.
3. **Non-régression** (P250) : à chaque commit `code:` ou `tests:`, empreintes des bancs identiques à `ce3662a` (code 0) et sortie du script identique à l'octet.
4. **Contrôle de #122 dans le schéma d'état** (P251) ; forme au point 12.
5. **Labels** (P252) : les formes fermées ne portent aucun label `eq:` ; forme au point 11.

### Forme proposée

6. **Résolveur : module feuille `nations.scenarios.stationnaire`.**
   1. Il n'importe que la bibliothèque standard (`math`, `dataclasses`), aucun module de `nations`. `nations/scenarios/__init__.py` reste sans importation, comme `nations/__init__.py` : importer le résolveur ne charge de `nations` que ces trois modules (test en sous-processus sur `sys.modules`).
   2. Fonctions **pures** sur des flottants : ni table, ni `EtatPays`, ni variable de module modifiée, ni cache, ni graine.
   3. **Aucun argument optionnel, aucun booléen, aucune valeur `None` qui choisisse une branche, aucune branche sur une valeur particulière d'un paramètre.** Les trois souplesses du script deviennent des arguments explicites ou une composition côté appelant :
      - r̂\* et ϱ̄_L sont des **arguments obligatoires** de la résolution. La norme de l'état initial, ϱ̄_L = ϱ_L, s'obtient par la fonction des taux (étape 1 de l'ordre triangulaire), que la résolution rappelle : mêmes opérandes, mêmes opérations, donc Δϱ = 0,0 exactement (mesuré sur le script aux trois π\*) ;
      - `controler=False` devient **deux fonctions** : le calcul des formes, qui ne juge aucune condition d'existence, et le relevé des conditions violées (point 8). `etat_initial` appelle toujours les deux ; le script compose selon son besoin ;
      - le cas ν_G = 1 (marge du plafond de E1 publiée en constat) **reste dans `outils/`**, qui écarte cette condition du relevé à son point de référence.
   4. Résultats en **valeurs immuables à champs fixes déclarés** (état stationnaire, ouverture), chaque champ avec son unité ; pas de dictionnaire à clés libres dans `src/`.
   5. Les noms de fonctions et de types sont laissés à `coder` dans ces contraintes ; un nom fixé ici peut changer s'il est signalé (ADR 0014, Décision 5).
7. **Type d'entrée, défini dans `src/` : `EntreesStationnaires`.**
   1. Dataclasse gelée, **champs obligatoires sans valeur par défaut**, sous les noms des tables du moteur (`pas_par_an`, `pi_etoile`, `r_bar`, `lv_etoile`…) : n_a ; les 24 paramètres de table que lisent les formes fermées (g_pr, σ, κ ; g_N, U^eq ; μ̄ ; ν_H ; δ, t̄u, lv\*, ν_F, ζ, η_r ; ϖ_L, ϖ_D, ϑ ; π\*, r̄, θ_CB ; τ_H, τ_F, θ_Tr, φ, ν_G) ; les trois normalisations p_0, pr_0, N^pa_0. Tous en `float`, sauf n_a.
   2. **Aucune vitesse, aucun gain, aucune entrée de scénario** n'y figure : « une vitesse d'ajustement ne détermine pas l'état d'arrivée » devient une propriété du type. ζ et η_r y figurent (élasticités de niveau, sans effet sous Δϱ = 0).
   3. Sans défaut, le type ne porte **aucune valeur de référence** : celles du moteur restent dans les tables, celles du script dans `Parametres`.
   4. Son domaine est plus large que celui des tables (n_a ≠ 12, ν_G = 1) : il ne contrôle que ce que les formes exigent pour être définies. Les domaines de définition restent ceux des tables (moteur) et de `controler_domaine` (script).
8. **Refus typés.**
   1. Le résolveur rend la **liste ordonnée des conditions d'existence violées**, valeurs immuables (identifiant, valeur, section de la spécification), dans l'ordre du script : D1 > 0, D2 > 0, dividende de la banque ≥ 0, Div_F ≥ 0, θ_G > 0, marge du plafond de E1 > 0, B ≥ 0, B_Bk ≥ 0, B_CB ≥ 0, B_H = 0. Liste fermée, tenue par un test.
   2. `etat_initial` lève **`EtatStationnaireInexistant`** dès que la liste n'est pas vide : jamais un état, jamais un écrêtage. L'exception, à champs structurés, est définie dans le module feuille ; elle ne dérive pas d'`ArretMoteur`, que le script ne doit pas charger.
   3. Un pôle exact (D1 = 0, D2 = 0) rend les formes non définies : le calcul le refuse sous le même type, quel que soit l'appelant, au lieu d'une `ZeroDivisionError`.
   4. Une table hors domaine reste refusée à sa construction (`DefautDeDeclaration`), un `EtatPays` hors domaine à la sienne (ADR 0014, D1). L'harmonisation des familles de refus relève de J3-e2.
9. **Adaptateur du moteur : `nations.scenarios.initial.etat_initial`** (« `scenarios.etat_initial` » dans la feuille de route et les issues).
   1. Signature : `etat_initial(parametres, normalisation, *, identifiant, graine)`, tous obligatoires. `parametres` est un `EnsembleDesParametres` ; `normalisation`, une valeur immuable `Normalisation(p_0, pr_0, N_pa_0)` de `scenarios/`, de domaine « fini > 0 ». La référence (1 ; 1 ; 1) y est une constante nommée.
   2. **π\* se lit sur la table** (`banque_centrale.pi_etoile` ; ADR 0014, H1.4 et H3.3) : aucun argument π\* distinct. Un autre π\* passe par `varier`.
   3. **θ_G de l'ensemble reçu n'est pas lu** : il est l'inconnue de la fermeture (#44, lecture (e) de M32). Déclaré dans la docstring, tenu par un test (θ_G d'entrée varié, résultat identique au bit).
   4. Rend une valeur immuable à deux champs : l'`EtatPays` d'ouverture du pas 0 (t = 0, registre de 13 niveaux, onze positions, V^flux = V^stock par `identites.valeur_nette_stock`, variables des blocs) et l'`EnsembleDesParametres` **aligné**, dont la table `finances_publiques` porte θ_G résolu (par `varier`), les autres tables étant celles reçues.
   5. La correspondance variable d'état → champ de l'ouverture est une table fermée, en bijection avec `schema.VARIABLES_DES_BLOCS` (test).
   6. n_a ≠ 12 n'est pas servi par l'adaptateur (registre de 13 niveaux, `Cadre` ; #120).
   7. **Imports** : `nations.etat`, `nations.moteur.parametres`, `nations.noyau` (catalogue, identités) et le module feuille ; ni `blocs`, ni l'ordonnanceur, ni `observation`. Aucun module de `noyau`, `etat`, `moteur`, `blocs`, `observation` n'importe `scenarios/`. `IMPORTS_ADMIS` est étendu en ce sens.
   8. Les transformations d'essai restent dans `tests/` : `echelle` (× 100) et `choc_pi_e0` de `socle_partiel.etat_initial` s'appliquent à l'état rendu, V^flux étant recalculé sur les positions mises à l'échelle (forme actuelle, l. 668 à 670). `socle_partiel.sentier` garde le script pour `un_pas`.
10. **Conventions de sélection déclarées** (continuum d'équilibres ; toute autre est une condition d'arrêt de la branche) :
    - r̂\*_0 = r̄ et π^e_0 = π\*_0 = π\* (`sec:banque_centrale-stationnaire`) ;
    - ϱ̄_L = ϱ_{L,0} (M32, lecture (e) ; `sec:investissement-stationnaire`) ;
    - θ_G résolu, r̄, τ_H et ν_G donnés (`sec:finances_publiques-stationnaire`, première lecture de #44) ;
    - E^CB_0 = 0 (M32) ; B_H = 0 (M27, C42) ; ς_L = ς_B = 0 ;
    - normalisations p_0, pr_0, N^pa_0 : l'état est homogène de degré un en ces échelles.

    Elles s'appliquent **dans l'adaptateur**, en clair, jamais dans une valeur par défaut du résolveur.
11. **Labels et concordance** (P252).
    1. Les huit sections `sec:<bloc>-stationnaire` ne numérotent aucune équation (0 `\label{eq:` dans chacune ; 90 labels en tout). Le résolveur ne porte donc aucune balise `# eq:` ; chaque étape renvoie à sa section par un commentaire `# sec:<bloc>-stationnaire`, que le script de concordance ne lit pas (`MOTIF_BALISE`, `^#+\s*eq:`).
    2. Les formes fermées sont la solution des règles, non des règles d'un pas : leur lien à la spécification est tenu par les valeurs publiées et par A2.
    3. Si la spécification numérote un jour une forme stationnaire, le radical de son label est une question à rouvrir.
12. **Conditions jointes de l'état** (#122, P251 ; ADR 0014, D1, annoté).
    1. `nations.etat.schema` reçoit une **liste fermée de conditions jointes** (nom, champs lus, prédicat, texte) et une seule fonction qui les évalue. Première entrée : IN^vol = 0 ⇒ IN = 0.
    2. Elle est appelée par le contrôle de construction d'`EtatPays`, après les domaines par champ : état initial, `dataclasses.replace` et reprise sont couverts ; refus avec diagnostic (`ValueError`, donc `SauvegardeRefusee` à la reprise), sans réparation. Rien ne la module.
    3. **Elle n'est pas appelée par `etat_de_cloture`** : le chemin chaud ne change pas (#144). À la clôture, la condition doit tenir par la forme de N8 (ADR 0014, A8.1), ce qu'un test établit sur le socle complet ; sinon, condition d'arrêt.
    4. `VERSION_SCHEMA` reste à 5 : ni champ, ni type, ni unité, ni sens d'un champ ne change ; l'ajout est noté au journal de la version 5.
    5. Les points 2 et 3 du commentaire de #122 reçoivent, sur avis de `macro`, une entrée de cette liste ou une limite déclarée ; le point 3 touche le noyau (P72), que cet ADR ne modifie pas.
13. **Conversions : troisième liste fermée d'exemptions** (modifie ADR 0014, F2).
    1. Le test « conversion unique » admet les divisions par n_a et les puissances en 1/n_a des **seules fonctions du module feuille**, nommées une à une ((module, fonction) → nature), chaque exemption devant servir. L'adaptateur `initial` reste sous la règle commune, comme le reste de `src/`.
    2. Motifs : les formes stationnaires sont écrites à n_a quelconque et évaluées sur trois n_a, ce que les conversions du moteur ne servent pas ; l'identité au bit exige l'ordre des opérations du script (Contexte) ; une conversion fausse dans le résolveur rompt A2, sous les conversions du moteur.
    3. Le contrôle du littéral 12 s'applique sans exemption.
14. **Partage des entrées entre le script et `src/`.**
    1. `src/` n'importe jamais `outils/` (test existant). Le script importe de `nations` **le seul module feuille** ; `test_n_importe_que_la_bibliotheque_standard` devient : bibliothèque standard, plus ce module, jamais `archive`.
    2. Le script garde `Parametres` (42 champs, défauts, `DECLARATIONS`), `controler_domaine`, `HorsDomaine` et ses messages, et les **signatures actuelles** de `etat_stationnaire`, `ouverture`, `controler_etat`, `facteurs`, `rho_IN`, `rho_K`, réduites à des adaptateurs : `Parametres` → `EntreesStationnaires` par une table de correspondance des noms, appel du module feuille, résultat remis en dictionnaire dans l'ordre actuel des clés. Ses appelants ne changent pas.
    3. `outils/maquette_conjointe.py` et `outils/contre_epreuve_financement.py` chargent toujours le script par son chemin ; ils chargent le module feuille par lui, ce que leurs docstrings déclarent.

## Options écartées

- **R2, seconde implémentation indépendante dans `src/`** : deux maisons par forme ; #125 montre déjà la dérive de formes dupliquées entre le script et le moteur.
- **R3, point fixe numérique sur la carte du moteur** : continuum en ϱ̄_L et en stocks de la banque centrale tenus en niveau, donc jacobienne singulière et solution dépendant du point de départ ; état non recalculable à la main (ADR 0002) ; itération, que l'invariant de budget écarte par pas et que rien ne justifie ici (motif du plan du rang 0, non remesuré).
- **R4, état précalculé versé en fichier** : c'est une préparation ; les archétypes ne seraient pas résolubles à la demande, et toute modification d'une règle demanderait de régénérer le fichier (ADR 0002, pt 13).
- **Déplacer `Parametres` du script dans `src/`** : ses défauts dupliqueraient les valeurs des tables (deux maisons par paramètre, contre H3.3), et il porte des champs que l'état n'utilise pas.
- **Donner au résolveur un `EnsembleDesParametres`** : le script devrait construire des tables, donc charger le moteur, et ne pourrait évaluer ni n_a ∈ {4 ; 52} ni ν_G = 1, que les tables refusent.
- **Reprendre la signature du script dans `src/`** (`controler: bool`, `r_neutre=None`, `rho_bar_L=None`, cas ν_G = 1) : un booléen et deux `None` qui choisissent une branche sont des drapeaux de mode (ADR 0002 ; ADR 0014, H6.1).
- **Réécrire les formes avec `par_pas` et `facteur_par_pas`** : change des bits (Contexte) et interdit n_a ≠ 12. **Paramétrer les conversions par n_a** : modifie le contrat F2 et anticipe #120 (J3-e2). **Nommer le champ autrement pour échapper au détecteur** : contournement d'un invariant.
- **Calculer θ_G à l'importation de la table** : `moteur/` importerait `scenarios/`, et une table de référence dépendrait d'un calcul.
- **Labels `eq:scenarios-…` pour les formes fermées** (Q7) : un radical nouveau et des dizaines de labels pour des expressions que la spécification ne numérote pas.
- **Contrôle de #122 ailleurs** : dans `ouvrir_pas`, le noyau devrait lire une variable du bloc 2, à chaque pas ; dans `scenarios/` seul, la reprise n'est pas couverte ; dans `charger` seul, ni l'état initial ni `replace`.

## Conséquences

- **Fichiers** (#175, #122, #176) : `src/nations/scenarios/stationnaire.py` et `initial.py` ; `src/nations/etat/schema.py` ; `outils/etat_stationnaire.py` ; `tests/invariants/socle_partiel.py` (`etat_initial` et `parametres_du_sentier` réduits à des adaptateurs) ; `tests/invariants/test_conversion_unique.py`, `tests/unitaires/test_observation.py`, `tests/unitaires/test_etat_stationnaire.py` ; docstrings de `scenarios/`, de la table `finances_publiques` et des trois scripts. Spécification : les passages « l'état initial sera chargé par `src/nations/scenarios/` » des huit sections, `sec:calibration` (A1, A2), au passage de `docwriter`.
- **Effet sur les résultats : aucun.** Trajectoires, sortie du script et empreintes identiques au bit (point 3). Les verdicts A1, A2 et B du test zéro, premiers du nom, sont des résultats finaux soumis au mainteneur.
- **Reproductibilité.** L'extraction est un déplacement, pas une réécriture : mêmes opérandes, même ordre, mêmes parenthèses, mêmes appels (`**`, `math.exp`, `math.log`), aucune simplification algébrique. Les valeurs des tables égalent déjà les défauts du script (tests de H3.3). La résolution ne tire aucun aléa : la graine traverse `etat_initial` comme champ d'identité. La référence de la sortie du script est régénérée par la session, sur la machine de l'essai, avant le premier commit `code:` (S8).
- **Budget de calcul.** La résolution a lieu une fois par scénario, hors d'`executer_pas`, en formes fermées dans un ordre triangulaire : ni boucle sur un résidu, ni point fixe, ni bissection. Le coût par pas ne change pas ; la condition jointe est hors du chemin chaud (point 12.3). La seule résolution numérique du projet, la bissection de la mesure (α), **reste dans `outils/`**.
- **Le littéral θ_G de la table de référence reste**, seule valeur résolue écrite dans `src/`, tenue au bit par son test, qui compare désormais au résolveur ; le critère de #175 « aucun littéral de valeur résolue dans `src/` » se lit « aucun littéral nouveau » (S3).
- **Ce que l'ADR ne règle pas** : archétypes de pays et leurs normalisations (J5) ; fermeture à θ_G donné, quand il devient un levier (J4) ; perturbation de l'état initial pour F2 (J3-f1) ; `Cadre` à n_a ≠ 12 (#120) ; familles de refus (J3-e2) ; contenu de la série du test zéro dans `observation/` (#176, sous le protocole inchangé d'ADR 0014, E1) ; bornes d'échelle des normalisations (S7).

### Points soumis au mainteneur

- **S1** (pt 13) : exemption fermée du test « conversion unique » pour le module feuille. Modifie ADR 0014, F2.
- **S2** (pt 14.1) : le script cesse d'être indépendant de `src/` par ses imports ; conséquence de P247, à confirmer avec la réécriture du test et de la docstring.
- **S3** : le littéral θ_G reste, exception déclarée ; lecture du critère de #175.
- **S4** (pt 9.2, 9.3) : π\* lu sur la table ; θ_G d'entrée non lu.
- **S5** (pt 12.4) : pas d'incrément de `VERSION_SCHEMA`.
- **S6** (pt 12.3) : condition jointe non recontrôlée à la clôture, tenue par la forme de N8 et par un test.
- **S7** (pt 9.1) : `Normalisation` de domaine « fini > 0 », sans la borne d'échelle du script (`BORNE_ECHELLE`) ; avis de `macro` au rang 3.
- **S8** : référence de la sortie du script. sha256 remesuré `fb187be1…` contre `a0970c9f…` au rang 0 ; à remesurer par la session et à corriger dans #175.
- **S9** (pt 2) : annotation de l'ADR 0005, pt 20.
- **S10** (pt 8.2, 8.3) : refus défini dans le module feuille, hors de la famille `ArretMoteur` ; pôle exact refusé sous ce type.

Issues : #175, #176, #122, #115, #125 ; liées : #44, #80, #120, #144, #158.
