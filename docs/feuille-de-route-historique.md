# Feuille de route : historique

Tenu par `architect`. Ce fichier reçoit, **sans rien supprimer ni réécrire**, ce que la condensation de `docs/feuille-de-route.md` sort de la tête (issue #119, décision P76 du mainteneur du 14/11/2026). Il n'est pas lu par défaut : on y vient par un renvoi de la tête. Les numéros M-n, P-n et D-n y restent stables ; la décision qui fait foi pour un numéro M-n est la ligne du tableau de la tête (`docs/feuille-de-route.md` § 4, lue par `outils/concordance_spec_moteur.py`).

Chaque condensation ajoute une partie, la plus récente en tête. Une partie est figée.

**Lecture des renvois.** Un renvoi daté d'avant le 14/11/2026 vers « la feuille de route, § n » (par exemple « § 4, P10 » dans une fiche, un ADR ou la spécification) se lit dans la partie A, au § de même numéro. Un renvoi à P74 à P86, ou à une branche fusionnée jusqu'à J3-a, absent de la tête, se lit dans la partie B (ajoutée le 14/11/2026). Un renvoi à la fiche de J3-c, au relevé d'issues du 14/11/2026 après la PR #117 ou à P87 à P99, absent de la tête, se lit dans la partie C (ajoutée le 14/11/2026, après la fusion de la PR #129). Un renvoi au plan de J3-d1 (rangs 0 à 8), à P100 à P118, aux mises à jour de la tête du 13/11 au 14/11/2026 ou aux lignes du § 7 de la PR #118 à la PR #128, absent de la tête, se lit dans la partie D (ajoutée le 15/11/2026, rang 8 de J3-d1). Un renvoi à la fiche de J3-d1 (état et critères à la fusion de la PR #136), au relevé d'issues du 14/11/2026 après la PR #129, à P119 à P146 ou aux mises à jour de la tête du 14/11/2026 après la PR #129 et du 15/11/2026 (rangs 4 et 5 de J3-d1), absent de la tête, se lit dans la partie E (ajoutée le 15/11/2026, point d'étape après la fusion de la PR #136). Un renvoi à P147 à P155, à la ligne du § 7 de la PR #129 ou aux mises à jour de la tête des rangs 0 et 1a de J3-d2, absent de la tête, se lit dans la partie E, complément du rang 8 de J3-d2. Un renvoi à la fiche de J3-d2 (plan, mesures du rang 5, critères et conditions d'arrêt, à la fusion de la PR #146), par exemple « `docs/feuille-de-route.md` § 1, critères de #132 » dans `tests/`, au relevé d'issues du 15/11/2026 après la PR #136, aux points ouverts du rang 8 de J3-d2 ou à la ligne du § 7 de la PR #136, absent de la tête, se lit dans la partie F (ajoutée le 16/11/2026, point d'étape après la fusion de la PR #146). Un renvoi à P172 à P181, aux questions Q1 à Q8 du 16/11/2026 ou aux points ouverts du rang 0 de la branche « forme du code », absent de la tête, se lit dans la partie F, complément du rang 9 de cette branche. Un renvoi à la fiche de la branche « forme du code » (plan, critères, conditions d'arrêt et résultats des rangs 6 à 9, à la fusion de la PR #151), au relevé d'issues du 16/11/2026 après la PR #146 (avec les réserves de la revue finale et les dépendances), à P182 à P199, aux points ouverts du rang 9 de cette branche ou à la ligne du § 7 de la PR #146, absent de la tête, se lit dans la partie G (ajoutée le 16/11/2026, point d'étape après la fusion de la PR #151). Un renvoi à P200 à P203, à P213 à P224, à la présentation des parties A à G tenue en tête de `docs/feuille-de-route.md` jusqu'au 16/11/2026, à l'erratum du commit `afa9e89`, aux paragraphes de renvoi vers les parties B à F ou aux lignes J0 à J2 des jalons, absent de la tête, se lit dans la partie G, complément du rang 1 de la branche « calibration ». Un renvoi à P204 à P212, à P225 à P241, aux mesures du rang 8 de la branche « calibration » (coût P57, canal rentier ↔ rayon, consignes pour `docwriter`), à la mise à jour de la tête du 17/11/2026 (rang 8) ou aux questions Q1 à Q9 du 16/11/2026, absent de la tête, se lit dans la partie G, complément du rang 11 de la branche « calibration ». Un renvoi à la fiche de la branche « calibration » (plan, critères, précisions prospectives de M34, mesures du rang 8, conditions d'arrêt et rangs 0 à 11, à la fusion de la PR #162), au relevé d'issues du 16/11/2026 après la PR #151 (avec les issues proposées 1 à 3 du rang 11, les points ouverts et les dépendances), aux points (a) à (d) soumis au mainteneur au rang 11 de la calibration (texte du 17/11/2026), à la mise à jour de la tête du 17/11/2026 (rang 11), à la ligne 11 du § 2 ou aux lignes du § 7 de la PR #151 et de la PR #162 avant sa fusion, absent de la tête, se lit dans la partie H (ajoutée le 26/11/2026, point d'étape après la fusion de la PR #162). Un renvoi au plan de J3-e1 tel que décidé (motif, forme R1 et options écartées, contrats partagés, critères d'acceptation, conditions d'arrêt, état des rangs avant le rang 10), à P242 à P245, à l'en-tête du relevé d'issues du 26/11/2026 et à ses dépendances, à la mise à jour de la tête du rang 1 de J3-e1 ou à la ligne du § 7 de la PR #162 après sa fusion, absent de la tête, se lit dans la partie H, complément du rang 10 de J3-e1. Un renvoi à la fiche de J3-e1 telle qu'à sa fusion (rangs 0 à 10, résultats contre les critères, escalades, vigilance), au texte de P242 à P266 et aux points ouverts du 26/11/2026 (rang 10 de J3-e1), au relevé d'issues du 26/11/2026 au rang 10 de J3-e1 et à ses dépendances, à la ligne 12 du § 2 avant la fusion, à la mise à jour de la tête du rang 10 de J3-e1 ou à la ligne du § 7 de la PR #174 avant sa fusion, absent de la tête, se lit dans la partie I (ajoutée le 26/11/2026, point d'étape après la fusion de la PR #174). Un renvoi au texte de P267 à P276 ou aux critères détaillés de #171, #173, #170 et #168 (rang 1 de la branche 12 bis), absent de la tête, se lit dans la partie I, complément du rang 10 de la branche 12 bis. Un renvoi à la fiche de la branche 12 bis telle qu'à sa fusion (plan, critères, conditions d'arrêt, état des rangs, escalades), à la ligne 12 bis du § 2 avant la fusion, à l'en-tête du relevé d'issues du rang 10 de la branche 12 bis, aux lignes des issues fermées par les PR #183 et #184 et aux dépendances d'alors, aux points ouverts du rang 10 ou à la mise à jour de la tête du rang 10 de la branche 12 bis, absent de la tête, se lit dans la partie I, complément du point d'étape après la fusion de la PR #184. Un renvoi au texte de P277 à P293, aux décisions de la session de la branche 12 bis, à l'état de la tête au point d'étape après la fusion de la PR #184 (en-tête, § 1, ligne 13 du § 2 avant la décision du plan, en-tête du relevé et lignes alors modifiées, dépendances, points ouverts), absent de la tête, se lit dans la partie I, complément du rang 1 de J3-e2. Un renvoi à la fiche de J3-e2 telle qu'à sa fusion (périmètre, rangs 0 à 9, résultats, critères, conditions d'arrêt, visa, escalades, vigilance), à la ligne 13 du § 2 avant la fusion, à la ligne 13 ter avant la décision de son plan (P312), à l'en-tête du relevé d'issues du rang 9 de J3-e2, aux lignes des issues fermées par la PR #193, aux issues proposées N2 à N6 avant leur création, aux dépendances du rang 9, au texte de P303 à P311, aux questions Q-a à Q-d, aux points ouverts du rang 9 de J3-e2, à la mise à jour de la tête du rang 9 de J3-e2 ou aux lignes du § 7 des PR #183 et #184, absent de la tête, se lit dans la partie J (ajoutée le 27/11/2026, point d'étape après la fusion de la PR #193). Un renvoi au tableau des rangs ou aux critères d'acceptation de la ligne 13 ter au rang 0 (avant P313, P314 et P318 à P321), au texte réservé de P313 et P314, aux points ouverts du rang 0 de la ligne 13 ter, aux index de P204 à P241, P242 à P266, P294 à P302 et P303 à P311, au paragraphe de P213 à P224, aux faits du rang 0, aux dépendances du rang 0, aux paragraphes d'introduction du § 2 et du § 7, à la mise à jour de la tête du rang 0 de la ligne 13 ter ou à la ligne du § 7 de la PR #196, absent de la tête, se lit dans la partie J, complément du rang 1 de la ligne 13 ter. Un renvoi aux critères d'acceptation de la ligne 13 ter précisés au rang 1 (commun, #185, #186, #188, #191 et #198, dont le critère P314 de #186), à la ligne des escalades du rang 1, aux dépendances du rang 1, aux faits du rang 1, aux points ouverts du rang 1 de la ligne 13 ter ou à la mise à jour de la tête du rang 1, absent de la tête, se lit dans la partie J, complément du rang 10 de la ligne 13 ter.

## Partie J : extraits de la tête sortis le 27/11/2026 (point d'étape après la fusion de la PR #193, rang 0 de la ligne 13 ter), figés

Texte copié sans modification depuis la tête à `7fc1cdf` (`main`, commit de fusion de la PR #193), pour tenir la tête sous son plafond de 60 ko (P76) ; décision P317 du mainteneur du 27/11/2026 : titres décalés d'un niveau, lignes de tableau extraites avec leur en-tête. Les numéros P-n restent stables ; ces décisions restent en vigueur tant qu'aucune décision ultérieure ne les remplace. Les renvois « § 1 », « § 2 », « § 3 », « § 4 », « § 7 » et « ci-dessous » de ces lignes se lisent dans la présente partie. N2 à N6 ont été créées le 27/11/2026 sous #198 à #202 ; #153, #158, #178 et #181 ont été fermées par la PR #193 (tête, § 3 et § 7).

### En-tête (extrait : mise à jour de la tête du 27/11/2026, rang 9 de J3-e2)

**Dernière mise à jour** : 27/11/2026, rang 9 de J3-e2 (`architect`) — `main` = `c9d4f28` (PR #196, § 7) ; branche `claude/j3-e2-refus-types` à `baf0128` (avant la présente consignation), PR brouillon #193, rangs 0 à 9 faits, prête à sortir du brouillon (§ 1, § 2) ; P303 à P311 et Q-a à Q-d (§ 4) ; #195 et #197 « à trier », N2 à N6 proposées, relevé recompté (§ 3) ; extraits sortis : historique, partie I, complément du rang 9 de J3-e2. Mises à jour antérieures : historique, partie I et ses compléments, puis parties H à A et `git log -- docs/feuille-de-route.md`.

### 1. Branche de travail en cours (extrait : fiche de J3-e2, à la fusion de la PR #193)

**Branche 13, J3-e2 « domaines à l'état chargé et refus typés »** — `claude/j3-e2-refus-types`, créée le 27/11/2026 par la session depuis `caa6cce` (point d'étape, sur `main` = `d08332c`) ; **PR brouillon #193**. Plan proposé par `architect` le 27/11/2026, décidé le même jour par le mainteneur selon cet avis (P294 à P302, § 4). Fiche de la branche 12 bis à sa fusion : historique, partie I, complément du point d'étape après la PR #184. **Rangs 0 à 9 faits ; prête à sortir du brouillon** (27/11/2026) : restent le corps de la PR, la sortie du brouillon (session) et la fusion (mainteneur). Tableau des rangs au rang 1 : historique, partie I, complément du rang 9 de J3-e2.

**Périmètre (P294)** : avec `Closes` : #153 (noyau, échelle nulle d'une ligne), #158 (bloc 3, domaine de μ̃, exceptions brutes), #178 (bloc 2, N6, d < 0), #181 (B_CB ≥ 0, section citée) ; sans `Closes` : #125, point 6 (domaines de κ et σ ; le point 2 reste en J3-f1 avec `Closes`). Hors périmètre : #120 et #180, au J4 (P295, P296) ; familles de refus hors d'`ArretMoteur`, forme fixée par l'ADR du rang 1 et mise en œuvre par #194 (N1) au J4, qui n'est pas une sixième issue de la branche (P297) ; #157, correctif rapide hors branche (P302).

| Rang | Issue | Travail | Pilote ; circuit | Commits | État |
|---|---|---|---|---|---|
| 0 | — | Point d'étape, plan | — | `caa6cce` | **fait** |
| 1 | — | P294 à P302 ; PR #193 ; #194 ; lectures de `macro` et `monnaie` ; ADR 0016 accepté (P309), ADR 0014 annoté | `architect-approfondi` | `bda0368`, `76a6e1d` | **fait** |
| 2 | #153 | Échelle de repli d'une ligne, label `eq:noyau-echelle-ligne` (P304) | `monnaie` ; circuit 2 | `f97327a`, `bb95098` (`docs:` minimal) | **fait**, validé par `monnaie` |
| 3 | #158 | Domaine de μ̃, `DivisionParZero` (P305) ; reprise unique (m2, P310) | `macro` ; circuit 2 | `d69a70e`, `1127ec9` | **fait**, validé par `macro` |
| 4 | #125 pt 6, #178 | κ, σ ≥ DBL_MIN (P306) ; d ≥ 0 propriété dérivée, tests seuls (P307) | `macro` ; circuit 2 | `74e1213`, `55e915b` | **fait**, validé par `macro` |
| 5 | #181 | B_CB ≥ 0 écrite, dix conditions comparées ; un seul lieu d'écriture (P311) | `monnaie` ; circuits 4 et 3 | `7b8504d`, `8725d02` (`docs:` minimaux), `e10f942`, `38759cc`, `313310a`, `baf0128` | **fait** |
| 6 | — | Mesures « après » | session | aucun | **fait** (PR #193) |
| 7 | toutes | `docwriter`, un `docs:` par issue (règle 9) | circuit 4 | `02b7896` (#153), `403e2e3` (#158), `b9f66cd` (#125), `3d90918` (#178), `37f0e8a` (#181) | **fait** ; validés par `monnaie` (#153), `macro` (#158, #125, #178), les deux (#181), selon les messages |
| 8 | toutes | Revue finale complète (`audit`, règle 10) et `/code-review` | — | — | **fait** ; constats hors périmètre : N3 à N6 (§ 3), Q-d (§ 4) |
| 9 | — | Consignation : P303 à P311, ADR 0016 annoté, `CONTEXT.md`, #195 et #197 | `architect` | présent commit | **fait** |

**Commits** : 20 hors fusion à `baf0128` (4 `code:`, 5 `tests:`, 11 `docs:` ; `git log --no-merges main..HEAD`), plus la fusion de `main` (`859097e`, après la PR #196) et la présente consignation. **Résultats** : aucune trajectoire des bancs ni aucun verdict ne change (PR #193) ; concordance stricte 92 / 92 à `baf0128` (+1 de chaque côté, `eq:noyau-echelle-ligne`) ; cas hors bancs : tableau de la PR #193.

**Ordre** : l'ADR d'abord (contrat des refus et dénominateur du noyau, que les rangs 2 à 5 respectent) ; puis #153, seul contrat partagé ; puis #158 ; puis #125 pt 6 et #178 (même module de paramètres, même bloc 2) ; #181, petit et indépendant, ferme la branche. Aucun commit n'est censé changer un résultat ni une valeur publiée.

**Critères d'acceptation, écrits avant l'essai** (plan du 27/11/2026, décidé par P294) :
- **trajectoire** : à chaque commit `code:`, empreintes des bancs identiques à `ce3662a` (P250 ; aucun commit dans `src/` depuis, `git diff --stat 4462939 d08332c -- src` vide) ; sortie du script identique à l'octet à `052db4c4…4251`, celle de la maquette à `be66c5a4…4e03` tant que le `.tex` n'a pas bougé (#189) ; tout écart demande un tableau avant / après ; [27/11/2026, rang 9 : la maquette vaut `2020d57b…8f7b` à `baf0128` (57 109 octets, code 0, remesurée par `architect`) ; seuls les numéros de ligne du `.tex` cités ont changé (#189) : diff contre la sortie à `d08332c` sans écart une fois la colonne des lignes retirée ; script et bancs : PR #193.]
- **#153** : le cas (socle complet, π\* = 2 %, θ_Tr = 0,3, ς_B = 1 aux pas 5 à 7), ainsi que π\* = 10 % avec θ_Tr ∈ {0,2 ; 0,3}, passe sans arrêt ou s'arrête par un refus typé et motivé ; dénominateur déclaré dans l'ADR et dans la spécification ; aucune constante absolue ;
- **#158** : aux cinq valeurs du tableau de l'issue, refus typé (pas, étape, bloc, variable) ou résultat fini ; aucune `ZeroDivisionError` ni `OverflowError` ne sort de T2 ou de T3 ; toute borne est déclarée ;
- **#125 pt 6** : κ = 5,6e−309 et σ = 1e−320 refusés au chargement par la table, par un refus typé qui cite le domaine ; script et table appliquent le même domaine ;
- **#178** : d < 0 exclu par un domaine déclaré de M_G, ou refusé par un refus typé en N6 ; test par appel direct de `ventes` ;
- **#181** : la section citée écrit B_CB ≥ 0 ; le test qui lie chaque section citée au paragraphe « État initial du moteur » couvre B_Bk, B_CB et B_H ;
- **verdicts** : aucun verdict publié ne change ; batteries vertes ; concordance stricte 91 / 91, ou +1 de chaque côté par label de domaine nouveau, déclaré au rang 1.

**Conditions d'arrêt** : une trajectoire du sentier change ; #153 exige une constante absolue, ou contredit l'ADR 0005 sans ADR nouveau ; un domaine n'a qu'une borne arbitraire et les experts divergent ; un verdict publié change ; une seconde reprise `coder` → `audit` sur une même issue.

**Visa** : aucun résultat final ne doit changer. Validations de l'expert pilote : `macro` pour #158, #125 et #178 ; `monnaie` pour #153, #181 et M_G. Délégations P175 et P211 reconduites (P301).

**Escalades, relances et arrêts** (notés dans la PR #193) : Fable 0 sur 3 (P298 jugée non déclenchée, P309) ; aucune hausse d'effort ; deux relances ciblées de `macro`, chacune après la limite de 40 tours (validation de #158 ; validation du diff de la spécification) ; une reprise unique `coder` → `audit` (#158, m2). **Règle 9** (constat de `/code-review`) : trois commits `docs:` touchent la spécification pour #181 (`7b8504d`, `8725d02`, `37f0e8a`) et deux pour #153 (`bb95098`, `02b7896`) ; `7b8504d`, `8725d02` et `bb95098` sont des `docs:` minimaux annoncés dans leur message comme exceptions de la règle 9 (écart de CI) ; `02b7896` et `37f0e8a` appartiennent au passage unique.

**Vigilance** : #163 avant la démonstration J4 (condition de M34) ; sorties du script et de la maquette tenues par aucune batterie (#179) : sha256 sur stdout seul remesuré à chaque commit `code:` ou `tests:`, et pour la maquette à chaque commit qui déplace des lignes du `.tex` (#189) ; valeurs à `d08332c` : § 7.

### 2. Branches suivantes (extrait : lignes 13 et 13 ter avant la décision du plan de la ligne 13 ter, paragraphe des issues à rédiger)

| Ordre | Branche | Issues | Motif du regroupement et état |
|---|---|---|---|
| 13 | J3-e2 « domaines à l'état chargé et refus typés » `claude/j3-e2-refus-types` — **prête à sortir du brouillon** le 27/11/2026, rangs 0 à 9 faits (PR brouillon #193, § 1) | #153, #158, #178, #181 ; #125 point 6, sans `Closes` (P294) | Refus typés au lieu d'exceptions brutes ; après J3-e1 (états chargés par `scenarios/`). Le point 1 du commentaire de #122 (μ̃) relève de #158. Familles de refus hors d'`ArretMoteur` : forme par l'ADR du rang 1, mise en œuvre par #194 au J4 (P297). Sortent de la ligne : #120 et #180, au J4 (P295, P296). |
| 13 ter | « suites de la PR #184 » — créée le 27/11/2026 (P300), après J3-e2 et avant J3-e3 | #185, #186, #188, #191, #192 | `outils/etat_stationnaire.py` et ses tests : contre-épreuve et contrôles appliqués aux variantes de lv\* (#185, puis #186, critère de `macro` avant l'essai) ; NaN masqué et refus de domaine non capté (#188 avec #191 ; phrase des refus du `.tex` à rétablir après correction) ; constats mineurs (#192). Nom de branche, ordre et circuits au point d'étape qui la précède. |

Issues à rédiger plus tard (`architect`, au point d'étape qui précède chaque branche, approuvées par le mainteneur) : S1 (J3-f1 ; #163 rédigée le 16/11/2026, P204) ; S2 (J3-f2) ; G1, budget du socle complet, et références avec `outils/regenerer_references.py` (J3-g2). N1 et N2 du rang 0 de J3-e1 : créées le 26/11/2026, #175 et #176 (P257). N1 du rang 1 de J3-e2 : créée le 27/11/2026, #194 (P297). N2 à N6 du rang 9 de J3-e2 : proposées, non créées (§ 3).

### 3. Issues hors plan (extrait : en-tête du relevé du rang 9 de J3-e2, lignes des issues fermées par la PR #193 ou modifiées au rang 0 de la ligne 13 ter, issues proposées N2 à N6, dépendances du rang 9)

*Relevé du 27/11/2026, rang 9 de J3-e2* : **69 issues ouvertes** (`list_issues`, état ouvert, `totalCount` = 69, `architect`, 27/11/2026 ; 68 au rang 1, plus #195 et #197 créées, moins #157 fermée par la PR #196). En-têtes des relevés antérieurs, lignes alors modifiées et dépendances d'alors : historique, partie I, complément du rang 9 de J3-e2 et compléments antérieurs. La colonne « Branche prévue » n'est pas reportée sur GitHub.

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #125 | Facteur de croissance par pas, formes et domaines du script | points 3 à 5 : faits en J3-e1 ; point 6 : **fait en J3-e2** (`74e1213`, `b9f66cd` ; P306), sans `Closes` ; point 2 : J3-f1, `Closes` | point 1 réalisé en J3-c (P88) ; à la fermeture, noter que l'arrêt au premier pas n'était plus observable depuis `d69a70e` |
| #148 | B_Bk, B_CB ≥ 0 sans contrôle sous rachat net | J4, instruction de `monnaie` avant (P178) | inactif au socle ; recoupe #181 (J3-e2) |
| #153 | Noyau : résidu/S infini à échelle nulle | **J3-e2, rang 2, fait** (P304) | `monnaie` ; échelle de repli (ADR 0016, I) ; suite : N4 |
| #158 | T3 : domaine de μ̃, exceptions brutes | **J3-e2, rang 3, fait** (P305, P310) | domaine \|μ̃\| ≤ ln(DBL_MAX) et `DivisionParZero` ; suites : #197, N3, N5, Q-a |
| #178 | N6 : domaine de la demande adressée, d < 0 accepté par le moteur | **J3-e2, rang 4, fait** (P307) | aucun code ; tests par appel direct |
| #181 | B_CB : section citée par `CONDITIONS_D_EXISTENCE` | **J3-e2, rang 5, fait** (P311) | un seul lieu d'écriture, `sec:finances_publiques-conditions` ; recoupe #148 ; suite : N2 |
| #185 | `calculer` : contre-épreuve et contrôles de valeurs publiées appliqués aux variantes de lv\* | ligne 13 ter (P300) | `outils/etat_stationnaire.py` ; avant #186 |
| #186 | Fenêtre lv\* ≈ [0,5106 ; 0,5234] à π̄ = 0 | ligne 13 ter (P300), après #185 | `macro`, critère avant l'essai ; hors verdict de #170 (P278) |
| #188 | `superneutralite.ecart` : NaN masqué par max − min | ligne 13 ter (P300) | même défaut que M1 de #173 ; avec #191 |
| #191 | `minimum_delta_r_alpha_en_zeta` : refus de domaine non capté | ligne 13 ter (P300) | phrase des refus du `.tex` à rétablir après correction ; avec #188 |
| #192 | Constats mineurs de la revue finale de la PR #184 | ligne 13 ter (P300) | `outils/etat_stationnaire.py`, `outils/maquette_conjointe.py`, deux tests |
| #195 | Noyau : identité cumulée de la valeur nette jugée contre une échelle effondrée | à trier (P308) | `monnaie` ; hors de l'ADR 0016 ; recoupe N4 |
| #197 | Moteur : `registre.avancer` hors de `_appeler`, `ValueError` brute si P_t ≤ 0 | à trier (P310) | audit du rang 3 de J3-e2 ; défaut au sens de l'ADR 0016, pt 11 ; recoupe N3, Q-a, #194 |

**Issues proposées au rang 9 de J3-e2, non créées** (création sur accord du mainteneur ; rattachement à trier au point d'étape) :
- **N2** (`monnaie`, R4) : le besoin d'émission stationnaire de E9 manque au relevé des « valeurs publiées en vigueur » d'`outils/etat_stationnaire.py`, d'où la survie des valeurs de la calibration indicative jusqu'à #181 ; la sortie du script changerait (lignes nouvelles du relevé), aucun état ne change ;
- **N3** (`/code-review`, préexistant) : à μ̃ = −ln(DBL_MAX) et μ̄ au-delà d'environ 1e15 (admis par μ̄ > 0), `math.log(ω*/ω)` de T3 (`travail.py` ~l. 90 ; domaine de `etat/prix.py` ~l. 44) reçoit 0,0 et lève une `ValueError` brute, contraire à la lecture de P305 ; pistes : borner μ̄, ou T3 en logarithmes ;
- **N4** (`/code-review`, préexistant) : `_echelle_de_ligne` (`grand_livre.py` ~l. 104) juge « non nul » sur la cellule nette ; deux termes qui se compensent sur un même secteur l'excluent de l'échelle (α) ; à rapprocher de #195 ;
- **N5** (`/code-review` nit, audit m2 ; diagnostics du bloc prix) : μ̃ étant écrit avant ξ, un ξ non fini est refusé sous le nom « mu_tilde_suivant » par le contrôle de finitude, non par le domaine, ce qui masque la cause (écrire ξ, puis μ̃, puis p respecte m2) ; la docstring « Bornes » de `blocs/prix.py` (~l. 35-44) ne dit ni le débordement de p en +∞ ni un p sous-normal non nul (R2 de `macro`, déjà dans la spécification) ;
- **N6** (`/code-review` nit) : aucun test ne garde l'hypothèse de l'ADR 0016, point 10.4 (aucune division non gardée dans les chemins de vue et de noyau) ; `0.0 ** -a` serait aussi traduit en « division par zéro ».

**Dépendances** (27/11/2026, rang 9 de J3-e2 ; état du rang 1 : historique, partie I, complément du rang 9 de J3-e2).
- **Levées** (rangs 1 à 8) : ADR du rang 1 → #153, #158, #125 pt 6, #178, #181 ; lectures de `macro` et `monnaie` → rangs 2 à 5 ; avis de `monnaie` sur le domaine de M_G → #178.
- **Ajoutées le 27/11/2026 (rang 9)** : #195 ↔ N4 ; #197 ↔ N3 ↔ Q-a (exceptions brutes, lecture de P305) ; Q-a → #194 (avis de `macro` : J4) ; N2 → `outils/etat_stationnaire.py` (ligne 13 ter, même module).
- **Maintenues (P294 à P300)** : ADR 0016, II → #194 ; #180 → F2 (P296) ; #185 → #186 ; ligne 13 → ligne 13 ter → ligne 14 (J3-e3) ; décision du mainteneur → #190 → J3-f1.
- **Inchangées** : liste du rang 1 (historique, partie I, complément du rang 9 de J3-e2), sauf « #143 → domaine du levier de taux (J4) », qui se lit « (1′) de P215 → levier de taux du J4 » (P303), et « avis de `monnaie` sur le domaine de M_G → #178 », levée.

### 4. Décisions du mainteneur (extrait : texte de P303 à P311, questions Q-a à Q-d et points ouverts du rang 9 de J3-e2)

Décisions du mainteneur du 27/11/2026 pendant les rangs 1 à 8 (corps de la PR #193, « Non numérotées »), numérotées au rang 9 :
- **P303** (#143) : le point (1′) de P215 (refus typé du domaine de validité de S-ζ en ζΔϱ) passe au J4, avec le levier de taux ;
- **P304** (#153 ; ADR 0016, I, points 1 à 7) : échelle de repli structurelle d'une ligne sans montant, jamais nulle ni absolue ; label `eq:noyau-echelle-ligne` ; lectures L1 et L2 de la spécification, écrites selon le code ;
- **P305** (#158 ; ADR 0016, points 10.1, 11, 13 et 18.1) : domaine \|μ̃\| ≤ ln(DBL_MAX) et filet `ZeroDivisionError` en `DivisionParZero` ; formes de refus acceptées : `ValueError` sans pas, filet sans nom ; lecture du critère : « aucune exception brute ne sort du moteur » ;
- **P306** (#125, point 6 ; ADR 0016, point 18.2) : κ ≥ DBL_MIN et σ ≥ DBL_MIN, dans la table et à l'identique dans le script ;
- **P307** (#178 ; ADR 0016, point 19) : aucun code, d ≥ 0 propriété dérivée ; critère corrigé (tests par appel direct) ;
- **P308** : #195 créée, hors périmètre ;
- **P309** : ADR 0016 accepté, V1 à V4 selon l'ADR ; V5 : finitude, borne ln(DBL_MAX) maintenue ; P298 jugée non déclenchée, donc sans Fable ;
- **P310** (audit de #158) : m1, #197 créée, hors périmètre ; m2, μ̃ écrit avant p ;
- **P311** (#181) : B_Bk ≥ 0 et B_CB ≥ 0 n'ont qu'un lieu d'écriture, `sec:finances_publiques-conditions` (position A de `monnaie`, sans objection de `macro`) ; les sections banque et banque centrale y renvoient ; le code et le script citent cette section ; mis en œuvre par `38759cc`, `8725d02`, `313310a`, `37f0e8a` et `baf0128`.

**Questions au mainteneur, non bloquantes** (rang 9 de J3-e2) :
- **Q-a** (`macro`, #158) : refus nommé d'un prix sous-dépassé (aujourd'hui `DivisionParZero`, sans nom ; un domaine « p > 0 » sortirait de P299) ; avis de `macro` : J4, avec #194 ;
- **Q-b** (`macro`, #125) : test de propriété « κ = DBL_MIN admis par la table, puis refusé à la résolution » ?
- **Q-c** (`macro`, #125) : nommer « domaine de représentabilité » au paragraphe des tables de paramètres de la spécification ?
- **Q-d** (`audit`, m3) : trois commits `code:` de la branche contiennent des fichiers `tests/` (`f97327a`, `d69a70e`, `74e1213`), comme 16 des 110 derniers commits `code:` de `main` (relevé d'`audit`) ; usage admis, ou règle à appliquer (`CLAUDE.md`, « Git et GitHub ») ?

**Points ouverts au 27/11/2026** (rang 9 de J3-e2 ; version du rang 1 : historique, partie I, complément du rang 9 de J3-e2) :
- condition de M34 : **#163 traitée avant la démonstration J4** ;
- identité au bit des sorties du script et de la maquette : aucune batterie (#179, J3-g2) ; remesure manuelle sur stdout seul ; maquette dépendante des numéros de ligne du `.tex` (#189, J3-g2) ;
- marge du noyau seul sur l'exécuteur lent (#110, J3-g1) ; familles de refus : #194 (J4) ; exceptions brutes restantes : #197, N3 (ADR 0016, annotation du 27/11/2026) ; catégorie « placement raté » de C1 (J6) ;
- déjà ouverts : plancher du taux directeur (P181), durée d'une partie (#155), #11, #14 ;
- J3-f1 indicative à plus de cinq éléments : à redécouper au point d'étape qui la précède ;
- en attente du mainteneur : #190 ; Q-a à Q-d ; création de N2 à N6 ; suppression de la branche distante `ccr-e5be5328-tvkv0d`.

### 7. Branches fusionnées (extrait : lignes des PR #183 et #184)

| Branche | PR | Jalon | Fusion | Détail |
|---|---|---|---|---|
| `claude/correctif-182-renvois-j3e` | #183 | J3 (correctif rapide #182, `docs:` seul) | **27/11/2026, 08:13 UTC, commit de fusion `9518fcd`** | `ba07717` ; #182 fermée ; `main` fusionnée dans `claude/j3-suites-m34` (`dcc883c`), branche temporaire supprimée ; aucun résultat ne change. |
| `claude/j3-suites-m34` | #184 | J3 (suites de M34 à la table T1) | **27/11/2026, 12:39 UTC, commit de fusion `d08332c`** | #172, #173, #170, #168, #171 fermées (`completed`, vérifié par la session ; absentes des 67 issues ouvertes, § 3). 22 commits hors fusion propres à la branche (`git log --no-merges 9518fcd..d08332c` : 6 `code:`, 7 `tests:`, 9 `docs:`), consignation `d6f54de` et `2df6a29` (P293) compris ; 23 depuis la base `4462939`, avec `ba07717` (#182, PR #183). P267 à P293. Fable : 0 sur 3. Aucun commit dans `src/`, aucune trajectoire ni aucun verdict publié changé. Sorties remesurées par `architect` à `d08332c` (stdout seul, code 0) : script 206 094 octets, `052db4c4…4251` ; maquette 57 109 octets, `be66c5a4…4e03`. Branche suivante : ligne 13 (§ 2). |

### Complément sorti le 27/11/2026 au rang 1 de la ligne 13 ter (`claude/j3-suites-pr184`, tête `9410e81`, PR #203)

Texte copié sans modification depuis la tête à `9410e81`, pour tenir la tête sous son plafond de 60 ko (P76) : titres décalés de deux niveaux, lignes de tableau extraites avec leur en-tête. Les renvois « § 1 », « § 3 », « § 4 » et « § 7 » de ces lignes se lisent dans la tête à `9410e81` (`git show 9410e81:docs/feuille-de-route.md`). P313 et P314, réservées dans ces lignes, ont été tranchées le 27/11/2026 au rang 1 de la ligne 13 ter, avec P318 à P321 (tête, § 1 et § 4) ; les index de P204 à P241, P242 à P266, P294 à P302 et P303 à P311 restent en vigueur, comme les décisions qu'ils résument.

#### En-tête (extrait : mise à jour de la tête du 27/11/2026, rang 0 de la ligne 13 ter)

**Dernière mise à jour** : 27/11/2026, rang 0 de la ligne 13 ter (`architect`) — `main` = `7fc1cdf` (PR #193, § 7) ; branche `claude/j3-suites-pr184` créée depuis `7fc1cdf`, PR brouillon #203 (§ 1) ; P312, P315 à P317 décidées, P313 et P314 réservées au rang 1 (§ 4) ; N2 à N6 créées sous #198 à #202 et rattachées, relevé recompté (§ 3) ; extraits sortis : historique, partie J. Mises à jour antérieures : historique, partie J, puis partie I et ses compléments, parties H à A et `git log -- docs/feuille-de-route.md`.

#### 1. Branche de travail en cours (extrait : tableau des rangs et critères d'acceptation de la ligne 13 ter au rang 0)

| Rang | Issue | Travail | Pilote ; circuit | Résultat attendu | État |
|---|---|---|---|---|---|
| 0 | — | Consignation (feuille de route, historique, partie J ; P312, P315 à P317) ; PR brouillon | `architect` ; session | — | **en cours** (présent commit) |
| 1 | #185, #186, #198 | `macro` : option de #185 (P313) et critère de #186 écrit avant l'essai (P314) ; `monnaie` : portée de #188 et #191, avis sur #198 ; le mainteneur tranche P313 et P314 | `macro`, `monnaie` | aucun | à faire |
| 2 | #188 | `superneutralite.ecart` : NaN ou refus dès qu'un r̄_α du triplet n'est pas fini ; test par `mesure_alpha` | `monnaie` ; circuit 3 | sortie identique | à faire |
| 3 | #191 | `minimum_delta_r_alpha_en_zeta` : `HorsDomaine` converti en `MinimumNonEncadre` motivé ; voisins bornés à `bornes`, ou refus de `tol >= b − a` et de `a <= 0` ; tests `_RAlphaSynthetique` | `monnaie` ; circuit 3 | sortie identique | à faire |
| 4 | #185 | Contre-épreuve et relevé des valeurs publiées hors de `calculer`, appliqués à la seule table de référence (option a), ou signalés sans refus (option b), selon P313 | `macro` ; circuit 2 (lecture au rang 1), puis 3 | sortie et maquette identiques | à faire |
| 5 | #198 | Besoin d'émission de E9 au relevé (π̄ = 0, 2 et 10 %, % du PIB du pas) ; anciennes valeurs barrées à la contre-épreuve | `macro` (bloc 9), `monnaie` consultée ; circuit 2 | **sortie changée** : lignes ajoutées seulement ; tableau avant / après ; visa P315 | à faire |
| 6 | #186 | Essai selon le critère du rang 1 ; verdict « cas adverse » ou « artefact de la marge de E1 » | `macro` ; circuit 1 | constat nouveau, aucun verdict existant changé | à faire |
| 7 | — | Mesures « après » | session | — | à faire |
| 8 | toutes | `docwriter`, un `docs:` par issue (règle 9) : phrase générale des refus de « Sensibilité à ζ » rétablie (#191) ; constat de #186 dans `sec:finances_publiques-conditions` ; #185 et #198 seulement si le texte les décrit | circuit 4 | — | à faire |
| 9 | toutes | Revue finale complète (`audit`, règle 10) et `/code-review` | — | — | à faire |
| 10 | — | Consignation | `architect` | — | à faire |


**Critères d'acceptation, écrits avant l'essai** (plan du 27/11/2026, décidé par P312 ; ceux de #185 et #186 seront complétés au rang 1 par P313 et P314, avant tout essai) :
- **commun** : aucun fichier de `src/` touché (`git diff --stat main...HEAD -- src` vide) ; bancs : `outils/empreintes_des_bancs.py --comparer outils/empreintes_des_bancs_ce3662a.json`, code 0, globale `b8cbd18d…d7d3` ; sortie du script identique à l'octet à `052db4c4…4251` (206 094 octets) à chaque commit `code:` ou `tests:`, sauf au commit de #198 ; maquette `2020d57b…8f7b` (57 109 octets), ou diff nul une fois la colonne des lignes du `.tex` retirée (#189) ; concordance stricte 92 / 92 ; batteries vertes ;
- **#188** : un NaN hors de la tête du triplet donne NaN ou un refus, dans `alpha()["delta_r_alpha"]` comme dans `zeta[…]["delta_r_alpha"]` ; test par `mesure_alpha` ;
- **#191** : `bornes=(1e-9, 200)` et un `tol` inférieur à l'espacement flottant publient « refusée » avec un motif, le script sortant en code 0 ; aucune évaluation hors de `bornes` ni en ζ ≤ 0 ;
- **#185** : pour lv\* ∈ [0,4654 ; 0,5236], `calculer(replace(base, lv=x))` n'est plus refusé par la contre-épreuve (option a) ou le signale sans refus (option b) ; contre-épreuve inchangée à la table de référence (309 valeurs) ; verdict de #170 sur [0,30 ; 0,47] inchangé ;
- **#198** : trois lignes nouvelles au relevé, avec définition, unité (% du PIB du pas), dénominateur et cas, chacune « égal » aux valeurs publiées par #181 (0,4473 ; 1,4902 ; 7,1818 % ; spécification, rubrique « Limites » de E9) ; liées au texte par `test_valeurs_en_vigueur_ecrites_hors_barre_dans_leur_source` ; le diff de la sortie ne contient que des lignes ajoutées et les décomptes des bilans ; une ancienne valeur (0,2376 ; 1,1048 ; 6,2050 %) en « écart » sous `ENTREES_D_ORIGINE` arrête la branche et fait l'objet d'un rapport ;
- **#186** : critère de `macro` (intervalle [0,47 ; 0,5236] à π̄ = 0, pas, précision, conditions d'admission complètes, colonnes n_a = 4 et 12) consigné avant tout essai ; verdict publié avec sa définition, son unité et sa fenêtre ; aucun verdict publié ne change.

#### 2. Branches suivantes (extrait : paragraphe d'introduction des renvois)

Les branches fusionnées sont au § 7 ; lignes 7 à 9 (J3-b, J3-c, J3-d1) : historique, partie E, § 2 ; ligne 10 (J3-d2) : historique, partie F, § 2 ; ligne 10 bis (forme du code) : historique, partie G, § 2 ; ligne 11 (calibration) : historique, partie H, § 2 ; ligne 12 (J3-e1) avant sa fusion : historique, partie I, § 2 ; ligne 12 bis avant sa fusion : historique, partie I, complément du point d'étape après la PR #184. Lignes 12 et 12 bis à leur fusion, ligne de la PR #174 au § 7 : historique, partie I, complément du rang 9 de J3-e2. Lignes 13 et 13 ter avant la décision du plan de la ligne 13 ter : historique, partie J, § 2.

#### 3. Issues hors plan (extrait : dépendances du rang 0 de la ligne 13 ter)

**Dépendances** (27/11/2026, rang 0 de la ligne 13 ter ; état du rang 9 de J3-e2 : historique, partie J, § 3).
- **Levées** : ligne 13 → ligne 13 ter (PR #193 fusionnée, § 7) ; N2 → `outils/etat_stationnaire.py`, devenue #198, dans le périmètre (P312).
- **Ajoutées le 27/11/2026 (rang 0)** : P313 → #185 ; P314 → #186 ; #188 et #191 → #185 → #198 et #186 (ordre du § 1) ; instruction de #195 et #200 par `monnaie` → J3-f2 (P316) ; #192 → J3-g2, avec #189 (P316).
- **Retirées** : #192 de la ligne 13 ter (P312).
- **Maintenues** : #195 ↔ #200 (ex-N4) ; #197 ↔ #199 (ex-N3) ↔ Q-a, regroupées avec #201, #202 et #194 sur la ligne J4 « refus typés hors du sentier » (P316) ; ADR 0016, II → #194 ; #180 → F2 (P296) ; ligne 13 ter → ligne 14 (J3-e3) ; décision du mainteneur → #190 → J3-f1.

#### 4. Décisions du mainteneur (extrait : P313 et P314 réservées, points ouverts au rang 0 de la ligne 13 ter, index de P204 à P241, P242 à P266, P294 à P302 et P303 à P311, paragraphe de P213 à P224, faits du rang 0)

- **P313** (réservée, non tranchée) : option de #185, (a) contre-épreuve et relevé des valeurs publiées appliqués à la seule table de référence, ou (b) signalés sans refus pour les variantes ; à décider au rang 1, sur lecture de `macro` ;
- **P314** (réservée, non tranchée) : critère de #186, écrit avant l'essai (intervalle, pas, précision, conditions d'admission, colonnes n_a) ; à décider au rang 1, sur lecture de `macro` ;

**Points ouverts au 27/11/2026** (rang 0 de la ligne 13 ter ; version du rang 9 de J3-e2 : historique, partie J, § 4) :
- condition de M34 : **#163 traitée avant la démonstration J4** ;
- P313 et P314 : au rang 1 de la ligne 13 ter, sur lecture de `macro` ;
- identité au bit des sorties du script et de la maquette : aucune batterie (#179, J3-g2) ; remesure manuelle sur stdout seul ; maquette dépendante des numéros de ligne du `.tex` (#189, J3-g2) ;
- marge du noyau seul sur l'exécuteur lent (#110, J3-g1) ; refus typés hors du sentier : ligne J4 (P316) ; catégorie « placement raté » de C1 (J6) ;
- déjà ouverts : plancher du taux directeur (P181), durée d'une partie (#155), #11, #14 ;
- J3-f1 indicative à plus de cinq éléments, J3-g2 à six depuis P316 : à redécouper au point d'étape qui précède chacune ;
- en attente du mainteneur : #190 ; Q-b à Q-d ; suppression de la branche distante `ccr-e5be5328-tvkv0d`.

P204 à P212 (plan, questions Q1 à Q9 du 16/11/2026) et P225 à P241 (rangs 1 à 8) : historique, partie G, complément du rang 11 de la calibration (texte inchangé), en vigueur. **Index** : P204 #45 réduite à λ_w, C7 dans #163 ; P205 fiche transverse `docs/blocs/calibration.md` ; P206 décision unique M34 et visa du tableau prédit (1e−9) ; P207 #143 instruite sans `Closes` ; P208 source « non trouvée » déclarée ; P209 valeurs résolues de `tab:criteres-j3` ; P210 une référence d'empreintes par commit ; P211 délégation P175 reconduite ; P212 découpage de J3-e à J3-g (§ 2) ; P225 et P226 #130 (ϑ = 0,15 ; ϖ_L, ϖ_D, r̄ sourcés) ; P227 #167 ; P228 et P229 délégation pendant l'absence du mainteneur, issues sur accord ; P230 et P232 C62 et λ_w = 0,18 ; P231 fin du rang 1 ; P233 ν_H = 1,1, λ_H = 0,4 ; P234 `BORNES_MARGE_HAUSSE` (écart au critère « Diff » accepté, `3c8156e`) ; P235 amas des racines nulles (`399323c`) ; P236 horizon prospectif des critères de vitesse ; P237 #139 en échec attendu ; P238 `BORNES_MARGE` [1 ; 3] ; P239 variantes λ_w relatives ; P240 #169, #170 ; P241 lectures de C62.

P242 à P266 et points ouverts du rang 10 de J3-e1 : historique, partie I, § 4 (texte inchangé ; P242 à P245 aussi en partie H, complément du rang 10 de J3-e1), en vigueur. **Index** : P242 valeurs publiées liées au texte (règle de `CLAUDE.md`, P256) ; P243 trois changements de structure mentionnés sans suite ; P244 sources « États-Unis », « zone euro » compatibles avec M17 ; P245 #171 à #173 créées ; P246 périmètre de J3-e1 ; P247 forme R1 (ADR 0015) ; P248 A1 contrôle la transcription, A2 l'équilibre des règles ; P249 critères A1, A2, B, F1, C1, F2 en J3-f1 ; P250 identique au bit contre `ce3662a` ; P251 #122 dans le schéma d'état ; P252 formes fermées sans label ; P253 Fable pour l'ADR 0015 ; P254 délégations P175 et P211 reconduites ; P255 ligne 12 bis ; P256 règle de P242 dans `CLAUDE.md` ; P257 #175, #176 ; P258 ADR 0015 accepté, sortie du script de référence sha256 `fb187be1…e088` ; P259 forme (i) de P2/T2, #177 à #179 ; P260 exemptions fermées du test « conversion unique » (`observation`) ; P261 verdicts du test zéro visés ; P262 C1 à π\* = 2 %, précision écrite après l'essai ; P263 sections de `CONDITIONS_D_EXISTENCE` ; P264 seuil de 𝒟₂ non publié ; P265 exception au contrat F3 ; P266 #180 à #182.

P294 à P302 (plan de J3-e2, Q1 à Q9, `bda0368`) et points ouverts du rang 1 : historique, partie I, complément du rang 9 de J3-e2 (texte inchangé), en vigueur. **Index** : P294 périmètre A ; P295 #120 au J4 ; P296 #180 au J4, avant F2 ; P297 forme des familles de refus par l'ADR du rang 1, #194 ; P298 ADR par `architect-approfondi`, Fable seulement s'il modifie l'ADR 0005 ou 0014 ; P299 #158, domaine et filet ; P300 ligne 13 ter, #187, #189, #190 ; P301 délégations reconduites ; P302 #157 en correctif rapide (PR #196, fusionnée).

P303 à P311 (rangs 1 à 8 de J3-e2, numérotées au rang 9), questions Q-a à Q-d et points ouverts du rang 9 : historique, partie J, § 4 (texte inchangé), en vigueur. **Index** : P303 (1′) de P215 au J4, avec le levier de taux ; P304 échelle de repli d'une ligne, `eq:noyau-echelle-ligne` ; P305 domaine de μ̃ borné par ln(DBL_MAX), filet `DivisionParZero` ; P306 κ et σ ≥ DBL_MIN ; P307 d ≥ 0 propriété dérivée, aucun code ; P308 #195 ; P309 ADR 0016 accepté, sans Fable ; P310 #197, m2 ; P311 lieu unique d'écriture de B_Bk ≥ 0 et B_CB ≥ 0.

P213 à P224 (rang 1, instruction ; `docs/blocs/calibration.md`, P205) : #92, P213 et P214 (§ 1 ; #164) ; #143, P215 à P217 (§ 2 ; commentaire sur #143) ; #55, P218 à P224 (§ 3, § 3.13 ; #164, #165, #166, PR #162). Texte inchangé : historique, partie G, complément du rang 1 de la calibration.

Faits du rang 0 (27/11/2026), sans décision : N2 à N6 créées sous #198 à #202 (`needs-triage`) ; commentaires postés par la session sur #125 (point 6 traité ; symptôme non observable depuis `d69a70e`) et sur #148 (voie (ii) remesurée par appel direct de E10 et E11) ; branche assignée de la session supprimée en local, jamais poussée.

#### 7. Branches fusionnées (extrait : paragraphe d'introduction des renvois, ligne de la PR #196)

Détail des issues, commits, décisions et escalades de chaque branche jusqu'à J3-a : historique, partie A, § 7. Lignes de ces branches (`claude/fondations`, PR #7, à `claude/j3-maquette-criteres`, PR #109) : historique, partie B, § 7. Lignes de `claude/correctif-litteral-12` (PR #118), de J3-b (PR #117) et des correctifs CR2 et CR1 (PR #127, #128) : historique, partie D, § 7, et corps des PR. Ligne de J3-c : historique, partie E, complément du rang 8 de J3-d2. Ligne de J3-d1 : historique, partie F, § 7. Ligne de J3-d2 : historique, partie G, § 7. Ligne de la branche « forme du code » (PR #151) : historique, partie H, § 7. Pour J3-c, J3-d1 et J3-d2 : historique, parties C, E et F, § 1, et corps des PR #129, #136 et #146. Ligne de la branche « calibration » (PR #162) après sa fusion : historique, partie H, complément du rang 10 de J3-e1. Ligne de J3-e1 avant sa fusion : historique, partie I, § 7. Lignes des PR #183 et #184 : historique, partie J, § 7.

| Branche | PR | Jalon | Fusion | Détail |
|---|---|---|---|---|
| `correctif/157-tests-textuels` | #196 | J3 (correctif rapide #157, `tests:` seul, P302) | **27/11/2026, 15:55 UTC, commit de fusion `c9d4f28`** | `007c15d` ; #157 fermée ; `main` fusionnée dans `claude/j3-e2-refus-types` (`859097e`) ; CI verte après une relance (`test_cout_du_noyau_seul`, #110) ; aucun résultat ne change. |

### Complément sorti le 28/11/2026 au rang 10 de la ligne 13 ter (`claude/j3-suites-pr184`, tête `1e315c6`, PR #203)

Texte copié sans modification depuis la tête à `1e315c6`, pour tenir la tête sous son plafond de 60 ko (P76) : titres décalés de deux niveaux. Les renvois « § 1 », « § 3 », « § 4 » et « § 7 » de ces lignes se lisent dans la tête à `1e315c6` (`git show 1e315c6:docs/feuille-de-route.md`). Ces critères ont été écrits avant l'essai et ne sont pas déplacés ; leur résultat, issue par issue, est dans la tête (§ 1) ; le renvoi « § 1 de la feuille de route, paragraphe #186 » de `tests/unitaires/test_etat_stationnaire.py` (critère P314) se lit ici.

#### En-tête (extrait : mise à jour de la tête du 27/11/2026, rang 1 de la ligne 13 ter)

**Dernière mise à jour** : 27/11/2026, rang 1 de la ligne 13 ter (`architect`) — `main` = `7fc1cdf` (PR #193, § 7) ; branche `claude/j3-suites-pr184` à `9410e81` (avant la présente consignation), PR brouillon #203, rangs 0 et 1 faits (§ 1) ; P313 et P314 tranchées, P318 à P321 (critères de #185, #188, #191, #198) (§ 4) ; #204 créée hors périmètre (§ 3) ; extraits sortis : historique, partie J, complément du rang 1 de la ligne 13 ter. Mises à jour antérieures : même lieu, puis partie J, partie I et ses compléments, parties H à A et `git log -- docs/feuille-de-route.md`.

#### 1. Branche de travail en cours (extrait : critères d'acceptation de la ligne 13 ter, précisés au rang 1, et ligne des escalades)

**Critères d'acceptation, écrits avant l'essai** (plan du 27/11/2026, P312 ; ceux de #185, #186, #188, #191 et #198 précisés au rang 1, avant tout essai, par P313, P314 et P318 à P321 ; version du rang 0 : historique, partie J, complément du rang 1 de la ligne 13 ter) :
- **commun** : aucun fichier de `src/` touché (`git diff --stat main...HEAD -- src` vide) ; bancs : `outils/empreintes_des_bancs.py --comparer outils/empreintes_des_bancs_ce3662a.json`, code 0, globale `b8cbd18d…d7d3` ; sortie du script identique à l'octet à `052db4c4…4251` (206 094 octets) à chaque commit `code:` ou `tests:`, sauf au commit de #198 ; maquette `2020d57b…8f7b` (57 109 octets), ou diff nul une fois la colonne des lignes du `.tex` retirée (#189) ; concordance stricte 92 / 92 ; batteries vertes ;
- **#188** (P319) : assistant `_etendue` (NaN si une valeur n'est pas finie, sinon max − min, identique bit à bit sur des valeurs finies) dans `ecart`, `ecart_profil`, `beta_theta_G`, `alloc_beta` ; verdicts du rendu : `all(isfinite)` avant les `max(...) <= seuil`, « sans objet (valeur non finie) » sur un NaN ; NaN propagé, pas de refus (précédent `94246ac`). (a) NaN hors de la tête du triplet (π\* = 2 % ou 10 %) → NaN dans `alpha()["delta_r_alpha"]`, `zeta[z]["delta_r_alpha"]` pour les trois ζ et `delta_r_alpha_n_a[4|52]` ; (b) NaN dans le profil → NaN dans `ecart_profil` ; (c) la ligne « Δr̄_α, verdict (ζ = 8) » sort en « écart », script NaN ; (d) aucun verdict rendu « tenu » ni « non tenu (défaut connu, #80) » sur un NaN ; (e) sortie identique à l'octet ;
- **#191** (P320) : `HorsDomaine` d'argument pour `a <= 0` et pour `tol >= b − a` ; `HorsDomaine` des évaluations converti en `MinimumNonEncadre` motivé ; précision de la machine (`m in (a, b)`), dépassement d'itérations et voisins hors `bornes` → `MinimumNonEncadre` (pas d'écrêtage) ; `table_publiees` publie « refusée », avec motif, pour `bornes=(1e-9, 200)` et pour `tol=1e-15`, script à défaut en code 0 et sortie identique ; toute ζ passée à `calc.r_alpha` est dans `bornes` et > 0 (calc traceur, sur T1 et sur le cas synthétique r̄_α(0) = (5e−4 − ζ)/100, `bornes=(1e-4, 200)`, `tol=1e-3`, qui évalue aujourd'hui en ζ = −0,00066) ;
- **#185** (P313, P318) : relevé (450 lignes), historique (29) et contre-épreuve (47) calculés hors de `calculer` par une fonction de publication sans argument `base` (refus par construction, aucun drapeau de mode), sur `Parametres()` seule ; `main` l'appelle ; `afficher` imprime au même endroit et accepte un résultat sans relevé (test l. 676) ; sortie identique à l'octet à la table de référence ; contre-épreuve du script inchangée (47 barrées, 47 égales) ; 310 anciennes valeurs de M34 égales sous `ENTREES_D_ORIGINE` (`test_contre_epreuve_des_valeurs_republiees_sous_les_entrees_d_origine`) ; après #198 : 47 et 313. Effets attendus (`macro`) : partie (iii) du test #170 (`tests/unitaires/test_etat_stationnaire.py` l. 1039-1041, refus de `calculer` en lv\* ≈ 0,465469) réécrite ; frontière de refus de `calculer` en [0,523594 ; 0,523672] (points T1, déjà publiée) ; ligne de #173 plus produite pour une variante, constat [0,346172 ; 0,458437] gardé par l'appel direct (l. 1055) ; verdict de #170 sur [0,30 ; 0,47] inchangé ;
- **#198** (P321) : trois lignes de catégorie A dans `VALEURS_PUBLIEES`, section `sec:finances_publiques-emission`, fonction `c.v(pi=…, nu=_NU)["Em"]` (sans `nu=_NU`, ν_G = 1 donne « écart », mesuré), avec définition, unité (% du PIB du pas), dénominateur et cas, chacune « égal » aux valeurs publiées par #181 (0,4473 ; 1,4902 ; 7,1818 % ; rubrique « Limites » de E9) et liée au texte par `test_valeurs_en_vigueur_ecrites_hors_barre_dans_leur_source` ; anciennes valeurs (0,2376 ; 1,1048 ; 6,2050 %) dans `ANCIENNES_M34_92` (convention cumulée #55, #92, #130, #62 ; à π\* = 0, μ̄ n'en sort que de 6,1e−5 pour un seuil de 5e−5 ; provenance en commentaire : republiées par #181, anciennes = sortie du script à `1aaba84`), pas dans `VALEURS_CONTRE_EPREUVE` ; décomptes 450 → 453 (433 égales), 310 → 313 (#92 : 176) ; le diff de la sortie ne contient que des lignes ajoutées et les décomptes ; une ancienne valeur en « écart » sous `ENTREES_D_ORIGINE` arrête la branche et fait l'objet d'un rapport ;
- **#186** (P314, critère de `macro`, consigné avant l'essai) : table T1 = `Parametres()` à la tête après #185 ; π̄ = 0 seulement ; lv\* (fraction du capital comptable) sur [0,47 ; 0,5236], pas 0,001 bornes incluses (55 points), bissection à 1e−6 sur chaque changement ; colonnes n_a = 4 et 12 (`_admis_170` paramétré) ; indicateurs par appel direct d'`etat_stationnaire` : R1 = E1 refusé à ν_G = 1 ; S1 = à ν_G = 1, E1 seule condition violée (`controler=True` aboutit) ; A(ν) = admission complète à ν ∈ {1,001 ; 1,15} (et 1,0001 pour N2). Prédicat C = R1 ∧ S1 ∧ A(1,001) ∧ A(1,15) ; contrôle C170 (prédicat de P277 restreint à π̄ = 0) : si C ≠ C170 en un point, arrêt et rapport sans verdict. Publier pour chaque composante de W = {lv\* : C} : bornes à 1e−6, indicateur qui ferme chaque bout, min et max de `marge_E1` = 1 − Γ̄(G/PB)/ν_G à ν_G = 1 (unité et dénominateur de sa `Grandeur` ; fenêtre : point stationnaire). Verdict par colonne : « aucun cas » si W est vide ; « artefact de la marge de E1 » si chaque composante vérifie N1 (borne basse = frontière de E1 à ν_G = 1, borne haute = frontière à 1,001, à 2e−6) et N2 (avec la sonde 1,0001, largeur divisée par un facteur dans [9 ; 11]) ; « cas adverse » sinon (bornes et conditions publiées) ; composante qui touche 0,47 ou 0,5236 : « non encadrée », rapport sans verdict. Garde du classifieur : C, N1 et N2 appliqués au cas d'origine (lv\* = 0,45, ϑ = 0,10, ν_H = 1, n_a = 12), classe publiée. Aucun verdict publié ne change (#170 porte sur [0,30 ; 0,47], n_a = 12). **Déclaration** : avant la consignation, `macro` a évalué la marge de E1 en neuf points (six de T1, lv\* de 0,505 à 0,5236 ; trois du cas d'origine, de 0,44 à 0,46 ; n_a = 4 et 12, π̄ = 0) pour concevoir le critère ; il a constaté que marge(1,001) ≈ marge(1) + 0,00100, que la conjonction sélectionne la couche −0,1 % < marge(1) ≤ 0, que le cas d'origine (marge −0,00038) y tombe et que T1 est translatée d'environ +0,065 en lv\* ; « cas adverse » et « artefact » ne sont donc pas exclusifs. Aucun essai du prédicat C n'a été fait.

**Escalades, relances et arrêts** : à noter dans la PR brouillon #203 ; aucun au rang 0.

#### 3. Issues hors plan (extrait : dépendances du rang 1 de la ligne 13 ter)

**Dépendances** (27/11/2026, rang 1 de la ligne 13 ter ; état du rang 0 : historique, partie J, complément du rang 1 de la ligne 13 ter).
- **Levées** : P313 → #185 et P314 → #186 (tranchées, § 4).
- **Ajoutées** : #204 ↔ #191 (même fonction `r_alpha`, recoupement à trier).
- **Maintenues** : #188 et #191 → #185 → #198 et #186 (ordre du § 1) ; instruction de #195 et #200 par `monnaie` → J3-f2 ; #192 → J3-g2, avec #189 (P316) ; #195 ↔ #200 ; #197 ↔ #199 ↔ Q-a, avec #201, #202 et #194 sur la ligne J4 « refus typés hors du sentier » (P316) ; ADR 0016, II → #194 ; #180 → F2 (P296) ; ligne 13 ter → ligne 14 (J3-e3) ; décision du mainteneur → #190 → J3-f1.

#### 4. Décisions du mainteneur (extrait : faits du rang 1 et points ouverts au rang 1 de la ligne 13 ter)

Faits du rang 1 (27/11/2026), sans décision : lectures de `macro` et `monnaie` ; #204 créée par la session (hors périmètre, `needs-triage`, § 3).

**Points ouverts au 27/11/2026** (rang 1 de la ligne 13 ter ; version du rang 0 : historique, partie J, complément du rang 1 de la ligne 13 ter) :
- condition de M34 : **#163 traitée avant la démonstration J4** ;
- #204 : à trier au prochain point d'étape ; critère de #186 : « cas adverse » et « artefact de la marge de E1 » non exclusifs (déclaration de P314) ;
- identité au bit des sorties du script et de la maquette : aucune batterie (#179, J3-g2) ; remesure manuelle sur stdout seul ; maquette dépendante des numéros de ligne du `.tex` (#189, J3-g2) ;
- marge du noyau seul sur l'exécuteur lent (#110, J3-g1) ; refus typés hors du sentier : ligne J4 (P316) ; catégorie « placement raté » de C1 (J6) ;
- déjà ouverts : plancher du taux directeur (P181), durée d'une partie (#155), #11, #14 ;
- J3-f1 indicative à plus de cinq éléments, J3-g2 à six depuis P316 : à redécouper au point d'étape qui précède chacune ;
- en attente du mainteneur : #190 ; Q-b à Q-d ; suppression de la branche distante `ccr-e5be5328-tvkv0d`.

## Partie I : extraits de la tête sortis le 26/11/2026 (point d'étape après la fusion de la PR #174, rang 0 de la branche 12 bis), figés

Texte copié sans modification depuis la tête à `4462939` (fusion de la PR #174).

### En-tête (extrait : mise à jour de la tête du 26/11/2026, rang 10 de J3-e1)

**Dernière mise à jour** : 26/11/2026, rang 10 de J3-e1 (`architect`) — `main` = `831547c` ; branche de travail `claude/j3-e1-etat-initial` à `285e6aa` (avant le commit de la présente consignation), PR brouillon #174 ; rangs 0 à 10 faits, sortie du brouillon et fusion en attente (§ 1, § 7) ; décisions P262 à P266 (§ 4) ; #177 à #179 rattachées (§ 2, § 3) ; prochaine branche : ligne 12 bis (§ 2, P255). Mises à jour antérieures et extraits sortis : historique, partie H et son complément du rang 10 de J3-e1, puis parties G à A et `git log -- docs/feuille-de-route.md`.

### 1. Branche de travail en cours (extrait : fiche de J3-e1, à la fusion de la PR #174)

**J3-e1 « état initial résolu et test zéro »** (`claude/j3-e1-etat-initial`, créée depuis `main` à `831547c` le 26/11/2026 ; PR brouillon #174) : plan décidé par le mainteneur le 26/11/2026 (P246 à P257), forme fixée par l'ADR 0015 (accepté, P258). **Rangs 0 à 10 faits** ; restent le corps de la PR, la sortie du brouillon (session) et la fusion en commit de fusion (mainteneur). Fiche décidée (motif, forme R1 et options écartées, contrats partagés, critères d'acceptation et conditions d'arrêt écrits avant l'essai) : historique, partie H, complément du rang 10 de J3-e1 ; fiche de la branche « calibration » : partie H, § 1.

- **Issues** (P246) : avec `Closes`, #175, #176, #115, #122 ; sans `Closes`, #125 points 3 à 5 (point 6 en J3-e2, point 2 en J3-f1).
- **Commits** : 34 hors fusion à `285e6aa` (10 `code:`, 8 `tests:`, 15 `docs:`, 1 `claude:` ; `git log --no-merges --format=%s 831547c..285e6aa`), plus le commit `docs:` de la présente consignation.

| Rang | Étape | Commits |
|---|---|---|
| 0 | Point d'étape après la PR #162, plan proposé, partie H de l'historique | `c93150a` |
| 1 | Règle P242 dans `CLAUDE.md` ; P246 à P258 ; ADR 0015 (Fable, 1 sur 3) accepté ; annotations des ADR 0014 et 0005 ; #175 et #176 créées | `eed2d31`, `f97cc6f`, `3f8e5e7` |
| 2 | #115 : radical `observation` admis par la concordance | `02e8657`, `28c2c64` |
| 3 | #175 : résolveur dans `nations.scenarios.stationnaire`, importé par le script ; adaptateur `nations.scenarios.initial.etat_initial` | `17e4a47`, `5c19961`, `2deeeae`, `0aaced6`, `29007ac` |
| 4 | #122 : condition jointe `stock_vide_sans_valeur` du schéma d'état | `f14bea7`, `6526e08` |
| 5 | #125, points 3 à 5 ; forme (i) de P2/T2 (P259) | `1a380be`, `e123557` |
| 6 | #176 : série du test zéro dans `observation/`, verdicts ; label `eq:observation-ratio-pib-annuel` ; P259 à P261 | `f16dc0f`, `fde046b`, `a92e74d`, `9cf44f6`, `de8b7ca` |
| 7 | Mesures « après » (session) | aucun |
| 8 | `docwriter`, un commit par issue : `0e972c9` (#115), `8141886` (#122), `1904caf` (#175), `b0e1d87` (#176) ; retouches de validation de `macro` et `monnaie` ; sections des conditions d'existence alignées (P263) | `aa20c2e`, `483256d`, `6ec9597`, `dfdea34`, `7be1b4d` |
| 9 | Revue finale complète d'`audit` (règle 10) et `/code-review` ; corrections revues sur leur diff | `35e3be1`, `2c31301`, `f4bf3a9`, `5d24684`, `285e6aa` |
| 10 | Consignation (`architect`) : § 1 à § 4, § 6, § 7 ; P262 à P266 ; ADR 0014 annoté (F2, F3) ; `CONTEXT.md` | présent commit |

**Résultats contre les critères écrits avant l'essai** (aucune condition d'arrêt rencontrée ; aucun changement de trajectoire ; `tests/references/` absent, J3-g2) :
- **identique au bit** (P250), remesuré par `architect` à `285e6aa` le 26/11/2026 : empreintes des bancs identiques à `ce3662a` (code 0) ; sortie de `outils/etat_stationnaire.py` de 205 933 octets, sha256 `fb187be1…e088`, celui de P258 ;
- concordance stricte (91 labels, 91 balises) et matrices : aucun écart ; batteries à `285e6aa` : unitaires 2162 passed, 2 skipped, 2 xfailed ; invariants 809 passed, 3 skipped, 1 xfailed (remesurés à `285e6aa`) (#80 et #139 en échec attendu) ;
- **test zéro** (#176 ; verdicts visés, P261, P262 ; non remesurés au rang 10) : A1 tenu sur 18 lignes sur 19 aux trois π\* (ligne ν_G = 1 non évaluable par construction) ; A2, B1 à B26 (sur P et L), F1 et observation sans effet tenus ; C1 tenu, jugé à π\* = 2 % (précision écrite après l'essai, P262).

**Escalades, relances et arrêts** (détail : PR #174) : `architect-approfondi` aux rangs 0 et 1, Fable au rang 1 (ADR 0015) : **1 sur 3**, aucune autre hausse d'effort ni consultation Fable ; reprises uniques `coder` → `audit` aux rangs 3, 4 et 6, puis pour l'alignement des sections (#175) et pour les corrections de la revue finale (#176), sans seconde reprise. **Dérogation à la règle 9**, déclarée : retouches de validation de la spécification en commits `docs:` supplémentaires (`aa20c2e` #122, `483256d` #175, `6ec9597` et `285e6aa` #176, `35e3be1` README #175), consécutives aux avis de `macro` et `monnaie` et à la revue finale, et un commit `code:` (`dfdea34`) après le passage de `docwriter`, sans changement de la spécification.

**Vigilance** (suites au § 2 et au § 4) : #163 avant la démonstration J4 (condition de M34) ; identité au bit de la sortie du script tenue par aucune batterie (#179) : sha256 remesuré à chaque commit `code:` ou `tests:` jusqu'à J3-g2 ; familles de refus pour J3-e2 ; exception au contrat F3 du registre (P265).

### 2. Branches suivantes (extrait : ligne 12, J3-e1, avant la fusion)

| Ordre | Branche | Issues | Motif du regroupement et état |
|---|---|---|---|
| 12 | **J3-e1 « état initial résolu et test zéro » `claude/j3-e1-etat-initial`, PR #174 — rangs 0 à 10 faits, fusion en attente (§ 1, § 7)** | #175, #176, #115, #122 ; #125 (points 3 à 5, sans `Closes`) | Critères A1, A2, B, F1, C1 tenus, verdicts visés (P261, P262) ; résolution par `scenarios/` sans dupliquer le script (P247, ADR 0015) ; bandes B centrées sur l'état calibré (M34). |

### 3. Issues hors plan (extrait : relevé du 26/11/2026 au rang 10 de J3-e1, lignes des issues fermées par la PR #174, dépendances)

*Relevé du 26/11/2026, mis à jour au rang 10 de J3-e1* : **69 issues ouvertes** (`list_issues`, état ouvert, `totalCount` = 69, `architect`, 26/11/2026 ; 63 au rang 1, plus #177, #178 et #179, P259 ; plus #180, #181 et #182, P266). En-tête du relevé au rang 1 et dépendances d'alors : historique, partie H, complément du rang 10 de J3-e1. La colonne « Branche prévue » n'est pas reportée sur GitHub.

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #115, #122 | Radical `observation` ; IN^vol = 0 ⇒ IN = 0 à l'état chargé | **J3-e1, fermées par la PR #174** | #122 : condition jointe du schéma d'état (P251) ; point 1 du commentaire (μ̃) renvoyé à #158 |
| #175 | `scenarios/` : état initial résolu par le moteur | **J3-e1, fermée par la PR #174** | créée le 26/11/2026 (P257) ; forme : ADR 0015 ; `macro`, `monnaie` consulté |
| #176 | Test zéro : séries dans `observation/`, verdicts A1, A2, B1 à B26, F1, C1 | **J3-e1, fermée par la PR #174** | créée le 26/11/2026 (P257) ; après #175 et #115 |

**Dépendances** (26/11/2026, rang 10 de J3-e1).
- **Ajoutées** : question du mainteneur de #177 → #177 ; avis de `monnaie` sur le domaine de M_G → #178 ; #179 → références de J3-g2 ; #181 ↔ #148 (même condition B_CB ≥ 0, recoupement) ; fusion de la PR #174 → #182 (correctif rapide).
- **Levées par la fusion de la PR #174** : #115 → #176 ; #175 → #122, #125 (points 3 à 5), #176 ; acceptation de l'ADR 0015 → rangs 3, 4 et 6 ; J3-e1 → ligne 12 bis, J3-e2 et J3-e3.
- **Inchangées** : S1 → #163 ; #163 → démonstration J4 (condition de M34) ; S1 → F2 (P249) ; #172 point 4 → #173 (grille) ; J3-f1 → J3-f2 ; J3-g1 → J3-g2 ; #143 → domaine du levier de taux (J4) ; avis de `monnaie` sur la caisse des entreprises → #143 ; #145 → #54 ; #141 → J4 (avec #70) ; #131 → #114 ; #116 → #111 ; #89 → #88 ; #148 → leviers du J4 ; #152 → J5.

### 4. Décisions du mainteneur (extrait : P242 à P266 et points ouverts au 26/11/2026, rang 10 de J3-e1)

P242 à P245 (points (a) à (d) du rang 11 de la calibration, tranchés le 26/11/2026) : historique, partie H, complément du rang 10 de J3-e1 (texte inchangé), en vigueur. **Index** : P242 valeurs publiées liées au texte, exception au découpage par domaine (règle de `CLAUDE.md`, P256) ; P243 trois changements de structure mentionnés sans suite ; P244 sources « États-Unis », « zone euro » compatibles avec M17 ; P245 #171 à #173 créées.

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
- **P259** (26/11/2026) : #125, point 3 : le script d'état stationnaire garde la **forme (i)** de P2/T2, forme indépendante du contrôle (avis de `macro` ; `1a380be`). Issues créées sur accord : #177 (emplacement des balises), #178 (N6, d < 0), #179 (CI de la sortie du script), à rattacher.
- **P260** (26/11/2026) : exemption fermée et nommée du test « conversion unique » pour `nations.observation.serie_test_zero.ratio_au_pib_annuel`, étendue le même jour à `richesse_sur_revenu_annuel` (B10, hors du label, avis de `macro`) (#176 ; modifie l'ADR 0014, F2, à annoter au rang 10).
- **P261** (26/11/2026) : test zéro (#176) — A1 publié « tenu sur 18 lignes sur 19, la ligne ν_G = 1 (référence hors domaine) non évaluable par construction » (précision prospective du texte d'A1 au passage de `docwriter`) ; C1 jugé à π* = 2 % seulement, 0 et 10 % publiés comme mesures ; activations du plancher de F3 et du max(0, ·) des dépôts publiées sans verdict (avis de `monnaie`) ; « placement raté » noté pour C1 au J6 ; **verdicts A1, A2, B1 à B26, F1, C1 visés**, sous réserve qu'aucun défaut de mesure ne soit trouvé (audit léger : aucun).

Décisions du mainteneur du 26/11/2026 aux rangs 8 et 9 (avis de `macro` et `monnaie` à la validation de la spécification et à la revue finale), consignées au rang 10 :
- **P262** : C1 (#176) — le jugement à π\* = 2 % (P261) est une **précision écrite après l'essai** (`CONTEXT.md`) : `tab:criteres-j3` ne fixait pas la cible ; le verdict est identique sous la lecture aux trois cibles ; déclarée comme telle dans la cellule de C1 et dans la ligne des verdicts (avis de `monnaie`, R1 ; `6ec9597`).
- **P263** : sections citées par `CONDITIONS_D_EXISTENCE` et par le message `HorsDomaine` du script **alignées sur la spécification** : D1 → `sec:menages-conditions` ; D2 et marge du plafond de E1 → `sec:finances_publiques-conditions`, la grandeur publiée `marge_E1` gardant sa section de définition ; B_H inchangé (avis de `macro` et `monnaie` ; `dfdea34`, `7be1b4d`, ce dernier liant chaque section au paragraphe « État initial du moteur » de `sec:calibration`). B_CB, dont la section citée n'écrit pas B_CB ≥ 0, est hors périmètre (#181, P266).
- **P264** : le seuil de 𝒟₂ proposé par `monnaie` (R4, optionnelle) **n'est pas publié** ; 𝒟₂ reste publié à ν_G = 1,15 (`483256d`).

Décisions du mainteneur du 26/11/2026 sur les points soumis au rang 10 :
- **P265** (contrat F3 ; ADR 0014, F3 ; ADR 0012, F3) : **exception déclarée**. `SerieDuTestZero` lit directement `registre_prix[0]` et `registre_prix[n_a − 1]` (glissement de B7) : `observation/` n'importe pas `moteur/` (graphe d'imports de l'ADR 0012), et `FinDePas` ne publie pas ce glissement. Lecture seule de deux positions, dans ce seul module, sans effet sur la trajectoire (E1) ; le calcul de B7 reste une seconde écriture, non balisée, de `eq:moteur-glissement` ; une seconde lectrice du registre dans `observation/` rouvre la forme. Option écartée : glissement publié par le moteur, ou fonctions d'indexation dans une couche importable (forme en J3-g1). Annotation de l'ADR 0014 du 26/11/2026 (F3).
- **P266** : trois issues créées par la session le 26/11/2026 : **#180** (série du test zéro : B19 à S^CB = 0 et bande B17 vide à L ≡ 0 ; `monnaie` ; J3-e2 ou J4), **#181** (B_CB : section citée par `CONDITIONS_D_EXISTENCE` ; `monnaie` ; J3-e2), **#182** (renvois « branche J3-e » de la spécification ; valeurs par archétype renvoyées au **jalon J5** ; correctif rapide `docs:` après la fusion de la PR #174, `macro` pour la ligne 3529).

**Points ouverts au 26/11/2026** :
- condition de M34 : **#163 traitée avant la démonstration J4** ;
- marge du noyau seul sur l'exécuteur lent (#110, J3-g1) ;
- déjà ouverts : plancher du taux directeur (P181), durée d'une partie (#155), #11, #14.
- identité au bit de la sortie du script : aucune batterie (#179, J3-g2) ; remesure manuelle à chaque commit `code:` ou `tests:` ;
- familles de refus hors d'`ArretMoteur` (J3-e2) ; catégorie « placement raté » de C1 (J6).

### 7. Branches fusionnées (extrait : ligne de `claude/j3-e1-etat-initial` avant la fusion)

| Branche | PR | Jalon | Fusion | Détail |
|---|---|---|---|---|
| `claude/j3-e1-etat-initial` | #174 (brouillon) | J3 (état initial résolu, test zéro) | **en attente** : sortie du brouillon par la session, fusion par le mainteneur en commit de fusion | `Closes` prévus, un par ligne : #175, #176, #115, #122 ; #125 sans `Closes` (points 3 à 5 faits) ; fermetures à vérifier après la fusion. 34 commits hors fusion à `285e6aa` (10 `code:`, 8 `tests:`, 15 `docs:`, 1 `claude:`), plus la consignation. P246 à P266 ; ADR 0015 accepté (P258) ; ADR 0014 annoté aux rangs 1 et 10 (F2, F3). Fable : 1 sur 3. Aucun changement de trajectoire ; verdicts du test zéro visés (P261). Empreintes identiques à `ce3662a` ; sortie du script `fb187be1…e088`. `tests/references/` absent. Branche suivante : ligne 12 bis (§ 2). |

### Complément sorti le 27/11/2026 au rang 10 de la branche 12 bis (`claude/j3-suites-m34`, tête `da4e455`, PR #184)

Sortis de `docs/feuille-de-route.md` pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé (titre des décisions décalé de deux niveaux). Les numéros P-n restent stables ; P267 à P276 restent en vigueur. Les renvois « § n », « ci-dessous » et « ci-dessus » de ces lignes se lisent dans la tête à `da4e455`. Erratum, sans retouche du texte : la « ligne `outils/etat_stationnaire.py:2478` » de P273 désigne la ligne de sortie « Δr̄_α au minimum en ζ (ζ = 68) » à `4462939`, relibellée « Δr̄_α à ζ = 68, point » par `ad6e577` (l. 2575 à `da4e455`) ; un numéro de ligne d'outil n'est pas un repère stable.

#### 1. Branche de travail en cours (extrait : critères d'acceptation de #171, #173, #170 et #168, précisés au rang 1 par les lectures des experts, 26/11/2026)

- **#171** : chaque chiffre est remesuré à T1 par une commande citée (script ou test, avec sortie), avec définition, unité, dénominateur et fenêtre, ou publié « non calibré, #163 », ou renvoyé (P267) avec renvoi dans le texte ; aucun chiffre recopié. Inventaire de `macro` (rang 1) : (1) 79 tours de cliquet (`.tex` l. 4136) : P274 ; (2) gain statique −0,2208 % (l. 3485) : P275 ; (3) π\* < 2 760 % à λ_H = 0,8 (l. 2019) : extension de `test_coefficient_de_richesse_refuse_au_chargement_de_l_ensemble`, sinon « aucune frontière sous X % » sur un intervalle déclaré ; (4) pas 182 sous φ = 0 (l. 3525) : `test_temps_de_doublement_sous_phi_nul`, correspondance indice / pas à fixer, sans verdict ; (5) dépôts de 12,03 à 12,25 mois (l. 2067) : banc X4 + X3 de `test_stationnarite_j3d1.py`, sans verdict ; (6) P_36 de la table φ de la fiche 9 : P275 ; (7) 2,08 de la maquette de la fiche 8 (l. 2935) : « non calibré, #163 », barré, renvoi à 13,89 ; (8) « 1,0000 » (l. 3045) : 0,999991 republié, « non calibré, #163 » ;
- **#173** (lecture de `monnaie`, forme P273) : seules trois lignes de sortie du script changent (l. 1081, libellé ; une ligne nouvelle ; bilan 449 → 450 comparées, 429 → 430 égales) ; test de position sans littéral 63 (pas 1 autour de ζ\*, grille de pas 10, ζ = 1 000 ; même contrôle sous les entrées d'origine, argmin 68) ; décomptes de la contre-épreuve (12, 173, 101, 24) et 310 inchangés ; retouche minimale de `sec:banque_centrale-conditions` au rang 8 ; aucune fiche annotée. #172 point 4 pose seul le test au pas 1 autour des littéraux, que #173 remplace par ζ\* ;
- **#170** (critère de `macro`) : lv\* ∈ [0,30 ; 0,47] balayé au pas 0,005, puis bissection à 1e−4 sur chaque changement de « E1 refusé à ν_G = 1 », à T1, n_a = 12, π̄ ∈ {0 ; 2 ; 10 %} ; cas trouvé si, aux trois π̄, E1 est refusé à ν_G = 1, admis à 1,001 et 1,15, et B ≥ 0 ; sinon, publier les deux frontières mesurées (E1 à ν_G = 1, B < 0) et l'absence ; contre-épreuve aux entrées d'origine ;
- **#168** (lecture de `macro`) : à T1, lecture (a) 0,983113, 0,983478, 1,001931, 0,996549 (θ_H = 0,8 / 1, hausse / baisse ; 1,004371 en a_entretien), lecture (c) de 0,9790 à 0,9898 ; restes : (i) phrase de `sec:ecartees` barrée et remplacée (`docwriter` relocalise) ; (ii) relevé `instabilite17.a.n_a4.hausse` reclassé en valeur d'origine ou contre-épreuve (`code:`, texte inchangé, l. 115 de `tab:changements-v3x` déjà à 0,95) ; (iii) « sans objet » justifiés dans la sortie ; (iv) motif de M27 (P276) ; (v) annotation datée de la fiche « ménages » ;

#### 4. Décisions du mainteneur (extrait : P267 à P276, rangs 0 et 1 de la branche 12 bis)

##### Décisions P267 à P276 (branche 12 bis, rangs 0 et 1), 26/11/2026

Plan de la branche 12 bis (questions Q1 à Q6 du rang 0, `824bd44`), tranché par le mainteneur le 26/11/2026, chaque fois selon l'avis d'`architect` :
- **P267** (Q1, périmètre) : les cinq issues avec `Closes` ; #171 réduite à huit chiffres ; « +141 pb et 0,42 % » renvoyés à #88 (remesurés à T1 par un scénario de J3-f2), « r̂\* » à #131 (remesuré par la mesure de #131 en J3-e3) ; commentaires sur les trois issues ([#171](https://github.com/Gerard-Garey/projet_macro/issues/171#issuecomment-7195761645), [#88](https://github.com/Gerard-Garey/projet_macro/issues/88#issuecomment-7195763404), [#131](https://github.com/Gerard-Garey/projet_macro/issues/131#issuecomment-7195764978)) ; le texte qui les cite reçoit un renvoi au rang 8 ;
- **P268** (Q2, #168) : M27 maintenue sans réouverture ; motif précisé de façon prospective (texte : P276), l'ancien motif restant publié barré ; annotation datée de la fiche « ménages », § 8 ; C26 non touchée ;
- **P269** (Q3) : les fiches décidées (#168, #171) sont annotées (date, renvoi à la remesure), sans réécriture de leurs valeurs d'instruction ;
- **P270** (Q4) : délégations P175 et P211 reconduites ;
- **P271** (Q5, #172 point 6) : écart de la contre-épreuve du script dû à l'ajout de ζ et λ_w à `ENTREES_D_ORIGINE` accepté (pas un résultat du modèle), avec tableau avant / après et visa de `macro` ;
- **P272** (Q6) : workflow `circuit-technique` lancé pour #172 (principe 1).

Lectures du rang 1 (critères au § 1), tranchées le 26/11/2026 :
- **P273** (#173, lecture de `monnaie`) : le minimum de Δr̄_α en ζ est un **point anguleux** (r̄_α(0) y rejoint r̄_α(2 %) = r̄ ; artefact de la statistique max − min, pas un optimum économique) ; bissection sur [2 ; 200] à 1e−3 : ζ\* = 63,0695, Δ = 0,159764 à T1 ; 68,4964 et 0,142803 aux entrées d'origine. La ligne `outils/etat_stationnaire.py:2478` devient « Δr̄_α à ζ = 68, point » (0,1614 inchangée, clé de `ANCIENNES_M34_130` renommée) ; ligne nouvelle « Δr̄_α au minimum en ζ sur [2 ; 200], point », publiée 0,1598 (0,1428 aux entrées d'origine), évaluée par bissection, refus explicite si le signe ne change pas aux bornes ;
- **P274** (#171, chiffre 1) : 79 tours de cliquet remesurés par un bloc 9 dérivé dans `tests/` (encaisse visée à ν = 1, comme `bloc_9_compose`), banc π̄ = 0, G −5 % aux tours 1 à 12, pas où le plafond de E1 est actif, sur 120 pas ;
- **P275** (#171, chiffres 2 et 6) : gain statique −0,2208 % barré, renvoi à dθ_G/dr̄ publié à T1 (−0,266955 ; −0,194 aux entrées d'origine), dit non identique ; P_36 remesurés par un test sur le socle complet (choc de taux par composition), sauf si `monnaie` y voit un scénario de J3-f2 : renvoi à #111 ;
- **P276** (#168, Q2) : motif de M27 adopté tel que rédigé par `macro` : « Motif précisé le JJ/MM/2026 (#168, P268 ; décision maintenue, sans réouverture) : ~~la lecture (a) est explosive en boucle conjointe~~ ; à la calibration indicative (μ̄ = 0,25, λ_w = 1), la lecture (a) était explosive dans les quatre configurations ; à la table T1 (M34), elle est faiblement explosive dans la seule configuration du socle, θ_H = 1 en régime de hausse de l'emploi (rayon 1,0019 ; 1,0044 en lecture a_entretien), et stable ailleurs (0,9831 à 0,9965) ; sa stabilité dépend des vitesses (λ_w) et de la marge normale μ̄, alors que la lecture retenue (c) est stable aux deux tables. Le motif de M27 tient : (a) ne garantit pas la stabilité dans la configuration du socle. C26, qui porte sur la lecture (b), n'est pas touchée. Maquette conjointe, `outils/maquette_conjointe.py`, sortie sha256 `28cf3d86…5ffe`. »

### Complément sorti le 27/11/2026 au point d'étape après la fusion de la PR #184 (`main` = `d08332c`)

Sortis de `docs/feuille-de-route.md` à la fusion de la PR #184, pour tenir la tête sous son plafond de 60 ko (P76) : texte copié sans modification depuis la tête à `d08332c` (seuls les titres des extraits sont ajoutés). Les numéros P-n restent stables ; P277 à P293 restent en vigueur (texte : tête, § 4). Les renvois « § n », « ci-dessous » et « ci-dessus » de ces lignes se lisent dans la tête à `d08332c`.

#### En-tête (extrait : mise à jour de la tête du 27/11/2026, rang 10 de la branche 12 bis)

**Dernière mise à jour** : 27/11/2026, rang 10 de la branche 12 bis (`architect`) — `main` = `9518fcd` (fusion de la PR #183, § 7) ; branche de travail `claude/j3-suites-m34` à `da4e455`, PR brouillon #184 ; rangs 0 à 9 faits (§ 1) ; P277 à P292 consignées (§ 4) ; #185 à #192 rattachées (§ 3) ; P267 à P276 et critères détaillés du rang 1 sortis dans l'historique, partie I, complément du rang 10 de la branche 12 bis. Mises à jour antérieures et extraits sortis : historique, partie I, puis parties H à A et `git log -- docs/feuille-de-route.md`.

#### 1. Branche de travail en cours (extrait : fiche de la branche 12 bis, à la fusion de la PR #184)

**Branche 12 bis « suites de M34 à la table T1 »** (`claude/j3-suites-m34`, créée par la session depuis `main` à `4462939` le 26/11/2026 ; ligne décidée par P255 ; PR brouillon #184). **Plan décidé** le 26/11/2026 (P267 à P272, toutes selon l'avis d'`architect`) ; **rangs 0 à 9 faits, rang 10 en cours** (27/11/2026). Fiche de J3-e1 à sa fusion : historique, partie I, § 1.

**Motif.** M34 a fixé la table T1 ; restent cinq suites : des chiffres publiés encore mesurés à la calibration indicative (#171, #168), un cas adverse du script sans équivalent à T1 (#170), le libellé d'une ligne publiée (#173) et la robustesse des outils qui produisent ces chiffres (#172). Modules touchés : `outils/etat_stationnaire.py`, `outils/maquette_conjointe.py`, `tests/unitaires/test_etat_stationnaire.py`, la spécification et des fiches décidées ; ni `src/`, ni une équation exécutée.

**État de départ**, mesuré par `architect` à `4462939` le 26/11/2026 (sorties dans un `mktemp -d` hors du dépôt) :
- `uv run python outils/etat_stationnaire.py` : 205 933 octets, sha256 `fb187be1…e088`, la référence de P258 ;
- `uv run python outils/maquette_conjointe.py` : 55 736 octets, sha256 `28cf3d86…5ffe` ; « 148 chiffres relevés ; 141 reproduits à la dernière décimale publiée ; 1 écarts : instabilite17.a.n_a4.hausse ; 6 sans objet ». L'écart : 1,0415 publié dans `sec:changements-v3x` (valeur de la fiche « ménages », calibration indicative), 0,947928 mesuré à T1. Les six « sans objet » : périodes 17 à 19 de la lecture (a), frontières 0,586 et 0,604, deux périodes de `socle.marge_conjointe.x2` ;
- #168 : ligne 17 de `tab:instabilites` et `sec:menages-inflation` **déjà à T1** (PR #162) ; restent `sec:ecartees` (l. 4077) et l'écart n_a = 4 (suite : critères ci-dessous) ;
- #173 : spécification au minimum vers ζ ≈ 63 (0,1598, grille de pas 10) ; ligne de sortie du script « Δr̄_α au minimum en ζ (ζ = 68) », 0,1614, relibellée « Δr̄_α à ζ = 68, point » (P273, `ad6e577`) ;
- batteries : non relancées au rang 0 (aucun commit `code:` ni `tests:` depuis le rang 9 de J3-e1, où elles ont été remesurées).

| Rang | Issue | Reste à faire | Pilote ; circuit type | Commits attendus | Valeur publiée |
|---|---|---|---|---|---|
| 0 | — | Point d'étape, plan proposé, partie I de l'historique (`architect`) | — | présent commit (`docs:`) | aucune |
| 1 | — | **Fait** : P267 à P272 ; PR #184 ; commentaires de P267 ; lectures écrites avant l'essai (rendues, P273 à P276) : `macro` (inventaire de #171, critère de #170, texte du motif de M27 selon P268), `monnaie` (forme de la ligne de #173 ; fiche 9, lignes P_36 et chiffres de #171 qui la touchent) | — | aucun, ou `docs:` de consignation | aucune |
| 2 | #172 | Les huit points de l'issue ; les points 4 (grille de ζ) et 5 (échantillonnage intérieur de `frontiere_ou_aucune`) protègent #173 et #168, les points 2 et 3 (cartes lues à l'appel, variantes relatives) #171 | `coder` → `audit` (circuit 3 ; workflow `circuit-technique` lancé, P272) | `code:` et `tests:` (#172) | aucune : sorties du script et de la maquette identiques à l'octet, sauf point 6 (P271) |
| 3 | #173 | Libellé juste, sans ζ figé faux ; ligne du script qui contrôle la valeur publiée du minimum ; test de position sur grille fine | `monnaie` ; `coder` → `audit` → contrôle de `monnaie` | `code:` et `tests:` (#173) ; `docs:` seulement si le texte change | une ligne de la sortie du script (tableau avant / après, visa de `monnaie`) |
| 4 | #170 | Bissection d'un lv\* où, à T1, le plafond de E1 n'agit qu'à ν_G = 1, ou absence établie sur un intervalle et une précision déclarés avant l'essai | `macro` ; circuit 2 (lecture de `macro` → `coder` → `audit` → `macro`) | `tests:` (#170) ; `docs:` au rang 8 si l'absence est publiée | un constat, aucun résultat du modèle |
| 5 | #168 | Motif de M27 (P268) ; phrase de `sec:ecartees` ; écart n_a = 4 ; relevés « sans objet » de la maquette ; annotation de la fiche « ménages » (P269) | `macro` ; circuit 4, plus `coder` → `audit` si le relevé de la maquette change | `code:` (#168) éventuel ; `docs:` (#168) au rang 8 | valeurs de la maquette (tableau avant / après, visa de `macro`) ; motif d'une décision M (P268) |
| 6 | #171 | Les huit chiffres de l'issue (P267) : remesure à T1 par un script ou un test, puis republication, barre avec renvoi, ou « non calibré, #163 » | `macro`, `monnaie` pour la fiche 9 ; circuit 2 | `code:` et `tests:` (#171), par famille de mesure ; `docs:` (#171) au rang 8 | valeurs publiées (tableau avant / après, visa de l'expert pilote) |
| 7 | — | Mesures « après » : sorties du script et de la maquette, batteries (session) | — | aucun | — |
| 8 | #168, #170, #171, #173 | `docwriter`, un commit `docs:` par issue (règle 9) ; diff validé une fois par `macro` et `monnaie` ; fiches décidées annotées par l'expert pilote (P269) | circuit 4 | `docs:` | celles des rangs 3 à 6 |
| 9 | toutes | Revue finale complète (`audit`, règle 10) et `/code-review` ; corrections revues sur leur diff | — | selon constats | — |
| 10 | — | Consignation (`architect`) | — | `docs:` | — |

**État des rangs** (27/11/2026, `da4e455`) : 0 `824bd44` ; 1 `a5dbf9a` ; 2 `27154d5`, `fbffcd4`, `65b0c17`, `e6605c1` ; 3 `ad6e577`, `ae388a7`, puis P281 `94246ac` ; 4 `6c810dd`, puis N1 et P282 `d32c745` ; 5 `f19fc9c` ; fusion de `main` `dcc883c` ; 6 `40ab44d`, `b538f82`, `64a9a35` ; 7 sans commit ; 8 `b856de5`, `70e5378`, `71010e3`, `da4e455` ; 9 : revue finale, #191 et #192 (P291, P292), `docs:` minimal de #173 ; **10 en cours**. Sorties (stdout) : script `052db4c4…4251` depuis `ad6e577` ; maquette `be66c5a4…4e03` à `da4e455`, variable avec les numéros de ligne du `.tex` (#189).

**Ordre.** #172 d'abord : ses points 4 et 5 sont les outils dont dépendent les verdicts de #173 (minimum en ζ) et de #168 (« frontières disparues ») ; #173 et #170, petits et indépendants, ensuite ; #168 avant #171, qui est le plus large et profite des cartes corrigées. Un commit par issue qui change une valeur publiée ; règle P242 pour les littéraux d'`outils/` liés au texte.

**Critères d'acceptation**, écrits avant l'essai (rang 0, précisés au rang 1 par les lectures des experts, 26/11/2026) :
- **trajectoire** : aucun commit dans `src/` ; si l'un en touche, empreintes des bancs identiques à `ce3662a` (P250) ;
- **sortie du script** identique à l'octet à `fb187be1…e088` à chaque commit `code:` ou `tests:`, sauf aux commits de #173 et du point 6 de #172 (P271) ; chaque écart : tableau avant / après ligne à ligne, chaque ligne expliquée par la modification ;
- **maquette** : sortie identique à l'octet à `28cf3d86…5ffe` jusqu'au rang 5 ; à la fin, aucun « ÉCART », chaque « sans objet » justifié dans la sortie ;
- **#171, #173, #170, #168** : critères précisés au rang 1 par les lectures de `macro` et `monnaie` (inventaire des huit chiffres de #171 ; forme P273 et décomptes de #173 ; balayage et bissection de #170, corrigé par P277 ; lectures (a) et (c) et restes (i) à (v) de #168) : historique, partie I, complément du rang 10 de la branche 12 bis ;
- **verdicts** : aucun verdict publié ne change (`tab:criteres-j3`, critères des fiches, test zéro, C62) ;
- batteries vertes ; concordance stricte inchangée (91 labels, 91 balises ; aucun label nouveau attendu).

**Conditions d'arrêt** (retour au mainteneur) : un verdict publié change ; un écart de sortie inexpliqué ; le point 5 de #172 trouve une frontière intérieure sur [0,3 ; 2] ; la lecture retenue (c) cesse d'être stable à T1, ou la lecture (a) devient explosive dans une autre configuration que θ_H = 1, régime de hausse ; un chiffre de #171 ne se remesure qu'avec un scénario de J3-f (il est renvoyé, pas forcé) ; une équation exécutée serait à changer ; une seconde reprise `coder` → `audit` sur une même issue.

**Visa.** Aucun résultat final (état stationnaire de référence, verdict du test zéro ou d'un scénario) ne doit changer ; les valeurs republiées sont visées par l'expert pilote (`macro` ; `monnaie` pour #173 et la fiche 9) ; le motif de M27 est celui de P276.

**Questions Q1 à Q6** (rang 0, `824bd44`) : tranchées par P267 à P272 (§ 4).

Aucun retrait ni ajout au périmètre ; #182, correctif rapide hors branche : PR #183 fusionnée (`9518fcd`), `main` fusionnée dans la branche (`dcc883c`). Issues nées dans la branche, hors périmètre : #185 à #192 (§ 3).

**Escalades, relances et arrêts** (27/11/2026) : Fable 0 sur 3, aucune hausse d'effort ; relances ciblées de `macro` au rang 1 et au rang 8 (limite de 40 tours) ; arrêt le 27/11/2026, sur instruction du mainteneur, de trois agents avant toute écriture (`coder` du rang 6, `coder` de P281 et P282, `monnaie` sur P_36), relancés ensuite ; reprises uniques `coder` → `audit` sur #172, #173 (deux cycles, une reprise chacun : `ad6e577`, puis P281 avec M1, `94246ac` ; aucune après la revue finale, P291), #170 et #168 ; aucune sur #171. **Vigilance** : #163 avant la démonstration J4 (condition de M34) ; sha256 des sorties remesuré à chaque commit `code:` ou `tests:` (#179 ; maquette : #189).

#### 2. Branches suivantes (extrait : ligne 12 bis, avant la fusion)

| Ordre | Branche | Issues | Motif du regroupement et état |
|---|---|---|---|
| 12 bis | **« suites de M34 à la table T1 » `claude/j3-suites-m34` — en cours** (§ 1), ouverte le 26/11/2026, PR #184 ; plan décidé (P267 à P272) ; rangs 0 à 9 faits, rang 10 en cours (27/11/2026) | #168, #170, #171, #172, #173 | Remesures et outils à la table T1 : `outils/etat_stationnaire.py`, `outils/maquette_conjointe.py`, `tests/unitaires/test_etat_stationnaire.py`, ligne 17 de `tab:instabilites`. Pilote `macro`, `monnaie` pour #173 ; ordre #172, #173, #170, #168, #171 (§ 1). Chiffres de #171 liés à #88 et #131 : remesurés dans J3-f2 et J3-e3 (P267, commentaires sur #171, #88, #131). Sortie du script tenue par aucune batterie (#179) : sha256 remesuré à chaque commit `code:` ou `tests:`. |

#### 3. Issues hors plan (extrait : en-tête du relevé au rang 10 de la branche 12 bis, lignes des issues fermées par les PR #183 et #184, dépendances)

*Relevé du 26/11/2026, point d'étape après la fusion de la PR #174* : **65 issues ouvertes** (`list_issues`, état ouvert, `totalCount` = 65, `architect`, 26/11/2026 ; 69 au rang 10 de J3-e1, moins #115, #122, #175 et #176, fermées par la PR #174). *Mis à jour le 27/11/2026, rang 10 de la branche 12 bis* : **72** (`totalCount` = 72 ; plus #185 à #192, moins #182, fermée par la PR #183). Relevé du rang 10 de J3-e1, ses lignes des issues fermées et ses dépendances : historique, partie I, § 3. La colonne « Branche prévue » n'est pas reportée sur GitHub.

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #168 | Instabilité 17 : lecture (a) des ménages à la table de M34, motif de stabilité de M27 | **12 bis, fait** (`f19fc9c`, `71010e3`) | P268, P276 ; suite : #190 |
| #170 | Cas adverse lv\* = 0,45 à la table T1 | **12 bis, fait** (`6c810dd`, `d32c745`, `70e5378`) | P277, P278, P282 ; suites : #185, #186 |
| #171 | Remesure à T1 des chiffres publiés « à la calibration indicative » | **12 bis, fait** (`40ab44d`, `b538f82`, `64a9a35`, `da4e455`) | P267, P274, P275, P283, P285, P287, P288 ; suite : #187 |
| #172 | Robustesse des outils de calibration et de la maquette après M34 | **12 bis, fait** (rang 2) | P271, P272 |
| #173 | Libellé « Δr̄_α au minimum en ζ (ζ = 68) » à T1 | **12 bis, fait** (`ad6e577`, `ae388a7`, `94246ac`, `b856de5`) | P273, P281, P291 ; suites : #188, #191 |
| #182 | Renvois « branche J3-e » de la spécification | **fermée** par la PR #183 (`9518fcd`, 27/11/2026) | `main` fusionnée dans la branche (`dcc883c`) |

**Dépendances** (26/11/2026, point d'étape après la PR #174 ; état du rang 10 de J3-e1 : historique, partie I, § 3).
- **Ajoutées le 27/11/2026** : #185 ↔ #186 ; #188 ↔ #191 (même module, même défaut) ; #189 ↔ #179 ; #190 → motifs de M27 (décision du mainteneur).
- **Levées par le rang 10 de la branche 12 bis** : #172 point 4 → #173 ; fusion de la PR #183 → fusion de `main` dans `claude/j3-suites-m34`.
- **Ajoutées le 26/11/2026** : #172 point 5 → #168 (frontières « disparues ») ; #172 points 2 et 3 → #171 ; P268 → #168 ; inventaire de `macro` → #171 ; P267 : « +141 pb et 0,42 % » de #171 → #88 (J3-f2), « r̂\* » → #131 (J3-e3).
- **Levées par la fusion de la PR #174** : J3-e1 → ligne 12 bis, J3-e2 et J3-e3 ; fusion de la PR #174 → #182.
- **Inchangées** : question du mainteneur de #177 → #177 ; avis de `monnaie` sur le domaine de M_G → #178 ; #179 → références de J3-g2 ; #181 ↔ #148 ; S1 → #163 ; #163 → démonstration J4 (condition de M34) ; S1 → F2 (P249) ; J3-f1 → J3-f2 ; J3-g1 → J3-g2 ; #143 → domaine du levier de taux (J4) ; avis de `monnaie` sur la caisse des entreprises → #143 ; #145 → #54 ; #141 → J4 (avec #70) ; #131 → #114 ; #116 → #111 ; #89 → #88 ; #148 → leviers du J4 ; #152 → J5.

#### 4. Décisions du mainteneur (extrait : points ouverts au 27/11/2026, rang 10 de la branche 12 bis)

**Points ouverts au 27/11/2026** (rang 10 de la branche 12 bis) :
- condition de M34 : **#163 traitée avant la démonstration J4** ;
- identité au bit de la sortie du script : aucune batterie (#179, J3-g2) ; remesure manuelle à chaque commit `code:` ou `tests:` ;
- marge du noyau seul sur l'exécuteur lent (#110, J3-g1) ; familles de refus hors d'`ArretMoteur` (J3-e2) ; catégorie « placement raté » de C1 (J6) ;
- déjà ouverts : plancher du taux directeur (P181), durée d'une partie (#155), #11, #14 ;
- maquette : empreinte dépendante des numéros de ligne du `.tex` (#189) ;
- aucune question pendante sur la branche 12 bis ; #190 attend une décision du mainteneur.

### Complément sorti le 27/11/2026 au rang 1 de J3-e2 (`claude/j3-e2-refus-types`, PR #193)

Sortis de `docs/feuille-de-route.md` à la consignation des décisions du mainteneur du 27/11/2026 sur le plan de J3-e2 (P294 à P302), pour tenir la tête sous son plafond de 60 ko (P76) : texte copié sans modification depuis la tête à `caa6cce` (seuls les titres des extraits sont ajoutés). Les numéros P-n restent stables ; P277 à P293 restent en vigueur. Les renvois « § n », « ci-dessous » et « ci-dessus » de ces lignes se lisent dans la tête à `caa6cce`.

#### En-tête (extrait : mise à jour de la tête du 27/11/2026, point d'étape après la fusion de la PR #184)

**Dernière mise à jour** : 27/11/2026, point d'étape après la fusion de la PR #184 (`architect`) — `main` = `d08332c` (§ 7) ; aucune branche de travail ouverte (§ 1) ; ligne 12 bis fusionnée (§ 2) ; P293 consignée (§ 4) ; relevé des issues recompté (§ 3) ; plan de la ligne 13 (J3-e2) et tri de #185 à #192 proposés, non décidés ; fiche de la branche 12 bis, ligne 12 bis d'avant la fusion, lignes des issues fermées, dépendances et points ouverts du rang 10 sortis dans l'historique, partie I, complément du point d'étape après la PR #184. Mises à jour antérieures et extraits sortis : historique, partie I et ses compléments, puis parties H à A et `git log -- docs/feuille-de-route.md`.

#### 1. Branche de travail en cours (extrait : état au point d'étape après la fusion de la PR #184)

**Aucune branche de travail ouverte** (27/11/2026, `main` = `d08332c`). La branche 12 bis « suites de M34 à la table T1 » est fusionnée (PR #184, § 7). Sa fiche à la fusion (motif, plan, critères, conditions d'arrêt, état des rangs, escalades) : historique, partie I, complément du point d'étape après la PR #184 ; fiche de J3-e1 : historique, partie I, § 1.

**Branche suivante** : ligne 13, J3-e2 (§ 2). Plan et tri de #185 à #192 proposés par `architect` le 27/11/2026, soumis au mainteneur, **non décidés** ; la fiche s'écrit ici après décision, la PR brouillon s'ouvrant avec la branche.

#### 2. Branches suivantes (extrait : ligne 13, J3-e2, avant la décision du plan)

| Ordre | Branche | Issues | Motif du regroupement et état |
|---|---|---|---|
| 13 | J3-e2 « domaines à l'état chargé et refus typés » — **prochaine branche** ; plan proposé le 27/11/2026, non décidé | #120, #153, #158, #178, #181 ; #125 point 6 (P246) ; #180 ici ou au J4 | Refus typés au lieu d'exceptions brutes ; après J3-e1 (états chargés par `scenarios/`). Le point 1 du commentaire de #122 (μ̃) relève de #158. #178 (domaine de la demande adressée) : `macro`, avec `monnaie` pour le domaine de M_G (E9, E13). Familles de refus à ranger (revue finale de J3-e1) : `EchelleNonRepresentable`, `NormalisationHorsDomaine`, `EtatStationnaireInexistant`, hors d'`ArretMoteur`. |

#### 3. Issues hors plan (extrait : en-tête du relevé du 27/11/2026, lignes modifiées par la décision du plan de J3-e2, dépendances)

*Relevé du 27/11/2026, point d'étape après la fusion de la PR #184* : **67 issues ouvertes** (`list_issues`, état ouvert, `totalCount` = 67, `architect`, 27/11/2026 ; 72 au rang 10 de la branche 12 bis, moins #168, #170, #171, #172 et #173, fermées par la PR #184). En-têtes des relevés antérieurs, lignes des issues fermées (#168, #170 à #173, #182) et dépendances d'alors : historique, partie I, § 3 et complément du point d'étape après la PR #184. #185 à #192 : tri proposé au mainteneur le 27/11/2026, non décidé. La colonne « Branche prévue » n'est pas reportée sur GitHub.

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #120 | `Cadre` à n_a ≠ 12 | J3-e2 (P82, option (a)) | inchangé |
| #125 | Facteur de croissance par pas, formes et domaines du script | points 3 à 5 : **faits en J3-e1** (sans `Closes`) ; point 6 : J3-e2 (P246) ; point 2 : J3-f1, `Closes` | point 1 réalisé en J3-c (P88) |
| #153 | Noyau : résidu/S infini à échelle nulle | J3-e2 (P178) | refus typé |
| #157 | Tests textuels de `src/` : m1 (P202), R1, R2 | correctif rapide (P212), sinon J3-e2 | `tests:` seul, résultats identiques |
| #158 | T3 : domaine de μ̃, exceptions brutes | J3-e2 (P212) | `travail.py:73` et `:90` (relevé du 16/11/2026) |
| #178 | N6 : domaine de la demande adressée, d < 0 accepté par le moteur | J3-e2 (rang 10) | `macro`, `monnaie` pour M_G ; inatteignable depuis l'état résolu |
| #180 | Série du test zéro : B19 à S^CB = 0, bande B17 vide à L ≡ 0 | J3-e2 ou J4 (P266) | `monnaie` ; « sans objet » déclaré avant l'essai |
| #181 | B_CB : section citée par `CONDITIONS_D_EXISTENCE` | J3-e2 (P266) | `monnaie` ; recoupe #148 |
| #185 | `calculer` : contre-épreuve et contrôles de valeurs publiées appliqués aux variantes de lv\* | à trier (P279) | `outils/etat_stationnaire.py` ; recoupe #186 |
| #186 | Fenêtre lv\* ≈ [0,5106 ; 0,5234] à π̄ = 0 | à trier (P280) | `macro`, critère avant l'essai ; hors verdict de #170 (P278) |
| #187 | Ligne (d) de `sec:menages-conditions` : « 1,0015 » non reproduit à T1 | à trier (P284) | `macro` ; origine du chiffre à retrouver |
| #188 | `superneutralite.ecart` : NaN masqué par max − min | à trier (P286) | même défaut que M1 de #173 ; avec #191 |
| #189 | Maquette : sortie dépendante des numéros de ligne du `.tex` | à trier (P289), au plus tard J3-g2 | recoupe #179 |
| #190 | Motifs d'écartement des ménages non réexaminés à T1 | à trier (P290) | décision du mainteneur, sans rouvrir M27 ; critère avant l'essai |
| #191 | `minimum_delta_r_alpha_en_zeta` : refus de domaine non capté | à trier (P291) | phrase des refus du `.tex` à rétablir après correction |
| #192 | Constats mineurs de la revue finale de la PR #184 | à trier (P292) | `outils/etat_stationnaire.py`, `outils/maquette_conjointe.py`, deux tests |

**Dépendances** (27/11/2026, point d'étape après la PR #184 ; état du rang 10 de la branche 12 bis : historique, partie I, complément du point d'étape après la PR #184).
- **Levées par la fusion de la PR #184** : #172 points 2, 3 et 5 → #171 et #168 ; P268 → #168 ; inventaire de `macro` → #171 ; ligne 12 bis → ligne 13 (J3-e2).
- **Ajoutées le 27/11/2026 (rang 10 de la branche 12 bis)** : #185 ↔ #186 ; #188 ↔ #191 (même module, même défaut) ; #189 ↔ #179 ; #190 → motifs de M27 (décision du mainteneur).
- **Inchangées** : P267 : « +141 pb et 0,42 % » de #171 → #88 (J3-f2), « r̂\* » → #131 (J3-e3) ; question du mainteneur de #177 → #177 ; avis de `monnaie` sur le domaine de M_G → #178 ; #179 → références de J3-g2 ; #181 ↔ #148 ; S1 → #163 ; #163 → démonstration J4 (condition de M34) ; S1 → F2 (P249) ; J3-f1 → J3-f2 ; J3-g1 → J3-g2 ; #143 → domaine du levier de taux (J4) ; avis de `monnaie` sur la caisse des entreprises → #143 ; #145 → #54 ; #141 → J4 (avec #70) ; #131 → #114 ; #116 → #111 ; #89 → #88 ; #148 → leviers du J4 ; #152 → J5.

#### 4. Décisions du mainteneur (extrait : P277 à P293, décisions de la session et points ouverts au point d'étape après la fusion de la PR #184)

Décisions du mainteneur des rangs 4 à 9 (P277 à P283 : passation de la PR #184, § 2 ; P284 à P292 : 27/11/2026 ; P293 : 27/11/2026, après le rang 10) :
- **P277** (#170) : critère corrigé prospectivement en « à au moins un π̄ », l'ancien (« aux trois π̄ ») publié et calculé ;
- **P278** (#170) : aucune recherche au-delà de lv\* = 0,47 dans la branche ; constat seulement ;
- **P279** : #185 créée ;
- **P280** : P278 maintenue malgré la fenêtre ≈ [0,5106 ; 0,5234] à π̄ = 0 ; #186 créée ;
- **P281** (#173, R1) : `minimum_delta_r_alpha_en_zeta` compare aussi Δ(ζ\*) à Δ(2) et Δ(200), `MinimumNonEncadre` « minimum aux bornes » si l'une est ≤ Δ(ζ\*) ;
- **P282** (#170, N2) : seules les quatre bornes de `LV_173_ENCADRANTS` en assertion ; frontières à 1e−4 citées comme mesure ponctuelle de `6c810dd` ;
- **P283** (#171, n°3) : intervalle déclaré [0 ; 1 000 %] par an, bissection sur le seul refus du coefficient de richesse ; publié « aucune frontière sous 1 000 % » ;
- **P284** : #187 créée (« 1,0015 » de la ligne (d), hors des huit chiffres de P267) ;
- **P285** (#171, n°6, avis de `monnaie` dans la délégation de P275) : P_36 remesuré aux seules colonnes φ ∈ {0 ; 1} ; colonnes 0,1, 0,25 et 0,5, hors domaine (M33), renvoyées à #111 ; l. 639 et 730 de la fiche 9 non touchées ; [commentaire sur #56](https://github.com/Gerard-Garey/projet_macro/issues/56#issuecomment-7214911794) (P3 du critère 15 à mesurer avant J4) ;
- **P286** : #188 créée ;
- **P287** (#171, n°2) : exception à P242, retrait de l'entrée `EXCLUS` (`sec:finances_publiques-conditions`, « 0,2208 ») dans le `docs:` de #171 ;
- **P288** : P275 étendue, « −0,22 % » de `sec:banque_centrale-conditions` barré, verdict C36 daté à la calibration indicative ; même exception pour (`sec:banque_centrale-conditions`, « 0,22 ») ;
- **P289** : #189 créée ; le message de `94246ac` attribue à tort l'écart `384f2731` → `1008f9da` de la maquette à la plateforme : cause, la fusion de `main` (`dcc883c`), qui décale les lignes du `.tex` ;
- **P290** : #190 créée ;
- **P291** (revue finale) : #191 créée ; phrase des refus de la spécification restreinte par un `docs:` minimal (exception à la règle 9) ; pas de seconde reprise sur #173 ;
- **P292** : #192 créée (constats mineurs groupés) ;
- **P293** (#173, validation de `6def60c` par `monnaie` : « à corriger ») : la phrase de `6def60c` (refus du minimum de Δr̄_α en ζ) est corrigée par un second `docs:` isolé, `2df6a29`, sous la même exception à la règle 9 que `6def60c` (P291). Elle couvre les deux écarts de périmètre relevés par `monnaie` : un NaN de r̄_α(0) − r̄_α(2 %) à un milieu de bissection donne aussi « refusée » ; un `HorsDomaine` interrompt la table où qu'il survienne. Diff validé par `monnaie` ; aucun code changé (correction du code : #191).

Décisions de la session : une ligne « refusée » du script est un constat en code 0 ; aucune issue pour l'écart d'état initial signalé sur #182 (`0aaced6`, égalité au bit) ; sur M1 de l'audit de #173, les lignes « Δr̄_α à ζ = 2, 8, 68 » sortent en écart (NaN), pas « refusée » (`94246ac`).

**Points ouverts au 27/11/2026** (point d'étape après la PR #184 ; version du rang 10 : historique, partie I, complément du point d'étape après la PR #184) :
- condition de M34 : **#163 traitée avant la démonstration J4** ;
- identité au bit des sorties du script et de la maquette : aucune batterie (#179, J3-g2) ; remesure manuelle sur stdout seul ; empreinte de la maquette dépendante des numéros de ligne du `.tex` (#189) ;
- marge du noyau seul sur l'exécuteur lent (#110, J3-g1) ; familles de refus hors d'`ArretMoteur` (J3-e2) ; catégorie « placement raté » de C1 (J6) ;
- déjà ouverts : plancher du taux directeur (P181), durée d'une partie (#155), #11, #14 ;
- en attente du mainteneur : plan de J3-e2 et tri de #185 à #192 (proposés le 27/11/2026) ; #190 (motifs de M27, sans réouverture).

### Complément sorti le 27/11/2026 au rang 9 de J3-e2 (`claude/j3-e2-refus-types`, tête `baf0128`, PR #193)

Sortis de `docs/feuille-de-route.md` à la consignation du rang 9 de J3-e2 (P303 à P311), pour tenir la tête sous son plafond de 60 ko (P76) : texte copié sans modification depuis la tête à `baf0128` (seuls les titres des extraits sont ajoutés). Les numéros P-n restent stables ; P294 à P302 restent en vigueur. Les renvois « § n », « ci-dessous » et « ci-dessus » de ces lignes se lisent dans la tête à `baf0128`.

#### En-tête (extrait : mise à jour de la tête du 27/11/2026, rang 1 de J3-e2)

**Dernière mise à jour** : 27/11/2026, rang 1 de J3-e2 (`architect`) — `main` = `d08332c` (§ 7) ; branche de travail `claude/j3-e2-refus-types` créée depuis `caa6cce`, PR brouillon #193 (§ 1) ; décisions du mainteneur du 27/11/2026 sur le plan de J3-e2 consignées, P294 à P302 (§ 4) ; ligne 13 en cours, ligne 13 ter créée, #120 et #180 au J4 (§ 2) ; #194 (N1) créée et rattachée, relevé recompté (§ 3) ; texte de P277 à P293 et état de la tête au point d'étape après la PR #184 sortis dans l'historique, partie I, complément du rang 1 de J3-e2. Mises à jour antérieures et extraits sortis : historique, partie I et ses compléments, puis parties H à A et `git log -- docs/feuille-de-route.md`.

#### 1. Branche de travail en cours (extrait : tableau des rangs de J3-e2 au rang 1)

| Rang | Issue | Travail | Pilote ; circuit | Commits | État |
|---|---|---|---|---|---|
| 0 | — | Point d'étape, plan | — | `docs:` (session) | **fait** (`caa6cce`) |
| 1 | — | Décisions Q1 à Q9 (P294 à P302) ; PR brouillon #193 ; ADR « échelle nulle d'une ligne du noyau et familles de refus » par `architect-approfondi` (P298 ; contrat partagé, ADR 0005 et 0014) ; lectures écrites avant l'essai : `macro` (domaine de μ̃ en T2 et T3 ; bornes de κ et σ ; domaine de d), `monnaie` (dénominateur de #153, porte de la monnaie centrale ; domaine de M_G, E9 et E13 ; section de B_CB ≥ 0) ; N1 | — | `docs:` (ADR, consignation) | **en cours** : PR #193 ouverte, décisions consignées, N1 créée (#194) ; ADR et lectures à venir |
| 2 | #153 | Dénominateur déclaré pour une ligne à échelle nulle, ou refus typé motivé ; aucune constante absolue | `monnaie` ; circuit 2, `coder` → `audit` → `monnaie` | `code:`, `tests:` | à venir |
| 3 | #158 | Domaine de μ̃ tiré de la spécification si `macro` en trouve un, et traduction générique de `ZeroDivisionError` par l'ordonnanceur en filet, sur le modèle de `DepassementNumerique` (P299) | `macro` ; circuit 2 | `code:`, `tests:` | à venir |
| 4 | #125 pt 6, puis #178 | Bornes inférieures de κ et σ ; domaine de d en N6 ou domaine de M_G à l'ouverture | `macro`, `monnaie` pour M_G ; circuit 2 | `code:`, `tests:` (#125, puis #178) | à venir |
| 5 | #181 | B_CB ≥ 0 écrite dans la section citée (`docwriter`) ou citation corrigée (`coder`) ; test `7be1b4d` étendu au groupe B_Bk, B_CB, B_H | `monnaie` ; circuit 4 ou 3 | `code:` / `tests:`, ou `docs:` au rang 7 | à venir |
| 6 | — | Mesures « après » (session) : empreintes, sorties, batteries | — | aucun | à venir |
| 7 | toutes | `docwriter`, un `docs:` par issue (règle 9) ; diff validé une fois par `macro` et `monnaie` | circuit 4 | `docs:` | à venir |
| 8 | toutes | Revue finale complète (`audit`, règle 10) et `/code-review` | — | selon constats | à venir |
| 9 | — | Consignation (`architect`) | — | `docs:` | à venir |

#### 3. Issues hors plan (extrait : en-tête du relevé du rang 1 de J3-e2, lignes modifiées au rang 9, dépendances du rang 1)

*Relevé du 27/11/2026, rang 1 de J3-e2* : **68 issues ouvertes** (`list_issues`, état ouvert, `totalCount` = 68, `architect`, 27/11/2026 ; 67 au point d'étape après la PR #184, plus #194 créée le même jour). En-têtes des relevés antérieurs, lignes alors modifiées et dépendances d'alors : historique, partie I, complément du rang 1 de J3-e2 et compléments antérieurs. La colonne « Branche prévue » n'est pas reportée sur GitHub.

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #125 | Facteur de croissance par pas, formes et domaines du script | points 3 à 5 : **faits en J3-e1** (sans `Closes`) ; point 6 : **J3-e2, rang 4**, sans `Closes` (P246, P294) ; point 2 : J3-f1, `Closes` | point 1 réalisé en J3-c (P88) |
| #143 | S6 : ti = 0 au-delà d'une frontière | (1′) en J3-e2 selon P215, absente du périmètre décidé (P294) : rattachement à trancher (§ 4) ; levier au J4, crise au J6 (P215) | instruite au rang 1 de la calibration (P207) ; M28 non rouverte ; caisse : refus voulu (P216) |
| #153 | Noyau : résidu/S infini à échelle nulle | **J3-e2, rang 2** (P294) | `monnaie` ; dénominateur déclaré ou refus typé, selon l'ADR du rang 1 |
| #157 | Tests textuels de `src/` : m1 (P202), R1, R2 | correctif rapide hors branche, PR directe vers `main` (P302), en cours | `tests:` seul, résultats identiques |
| #158 | T3 : domaine de μ̃, exceptions brutes | **J3-e2, rang 3** (P294) | `travail.py:73` et `:90` (relevé du 16/11/2026) ; domaine tiré de la spécification et filet `ZeroDivisionError` (P299) |
| #178 | N6 : domaine de la demande adressée, d < 0 accepté par le moteur | **J3-e2, rang 4** (P294) | `macro`, `monnaie` pour M_G ; inatteignable depuis l'état résolu |
| #181 | B_CB : section citée par `CONDITIONS_D_EXISTENCE` | **J3-e2, rang 5** (P294) | `monnaie` ; recoupe #148 |
| #194 | Familles de refus hors d'`ArretMoteur` (N1) | J4 (P297), après J3-e2 | forme fixée par l'ADR du rang 1 de J3-e2 (à venir) ; résultats identiques |

**Dépendances** (27/11/2026, rang 1 de J3-e2 ; état au point d'étape après la PR #184 : historique, partie I, complément du rang 1 de J3-e2).
- **Ajoutées le 27/11/2026 (P294 à P300)** : ADR du rang 1 de J3-e2 → #153, #158, #125 pt 6, #178, #181 et #194 ; lectures de `macro` et `monnaie` du rang 1 → rangs 2 à 5 ; #180 → F2 (P296) ; #185 → #186 ; ligne 13 → ligne 13 ter → ligne 14 (J3-e3) ; décision du mainteneur → #190 → J3-f1.
- **Retirée** : #185 ↔ #186, remplacée par #185 → #186 (P300).
- **Inchangées** : #188 ↔ #191 ; #189 ↔ #179 ; #190 → motifs de M27 (décision du mainteneur) ; P267 : « +141 pb et 0,42 % » de #171 → #88 (J3-f2), « r̂\* » → #131 (J3-e3) ; question du mainteneur de #177 → #177 ; avis de `monnaie` sur le domaine de M_G → #178 ; #179 → références de J3-g2 ; #181 ↔ #148 ; S1 → #163 ; #163 → démonstration J4 (condition de M34) ; S1 → F2 (P249) ; J3-f1 → J3-f2 ; J3-g1 → J3-g2 ; #143 → domaine du levier de taux (J4) ; avis de `monnaie` sur la caisse des entreprises → #143 ; #145 → #54 ; #141 → J4 (avec #70) ; #131 → #114 ; #116 → #111 ; #89 → #88 ; #148 → leviers du J4 ; #152 → J5.

#### 4. Décisions du mainteneur (extrait : P294 à P302 et points ouverts au rang 1 de J3-e2)


Décisions du mainteneur du 27/11/2026 sur le plan de J3-e2 proposé par `architect` au point d'étape après la PR #184 (`caa6cce`), toutes selon cet avis :
- **P294** (Q1) : périmètre A : #153, #158, #178, #181 avec `Closes` ; #125 point 6 sans `Closes` ;
- **P295** (Q2) : #120 au J4 ; option (a) de P82 maintenue, seulement déplacée ;
- **P296** (Q3) : #180 au J4, au plus tard avant F2 (J3-f1) ; dépendance #180 → F2 ;
- **P297** (Q4) : forme des familles de refus hors d'`ArretMoteur` (`EchelleNonRepresentable`, `NormalisationHorsDomaine`, `EtatStationnaireInexistant`) fixée par l'ADR du rang 1 ; mise en œuvre par une issue N1 rattachée au J4, création approuvée : **#194**, créée le 27/11/2026 par `architect` ;
- **P298** (Q5) : ADR du rang 1 rédigé par `architect-approfondi` ; Fable seulement s'il doit modifier l'ADR 0005 ou l'ADR 0014 ;
- **P299** (Q6) : #158 : domaine de μ̃ tiré de la spécification si `macro` en trouve un, plus une traduction générique de `ZeroDivisionError` par l'ordonnanceur en filet, sur le modèle de `DepassementNumerique` ;
- **P300** (Q7) : tri de #185 à #192 : ligne 13 ter « suites de la PR #184 » (§ 2), après J3-e2 et avant J3-e3, avec #185, #186, #188, #191 et #192, dépendance #185 → #186 au lieu de #185 ↔ #186 ; #187 en J3-e3 ; #189 en J3-g2 avec #179 ; #190 : décision du mainteneur d'abord, puis J3-f1 ;
- **P301** (Q8) : délégations P175 et P211 reconduites pour J3-e2 ;
- **P302** (Q9) : #157 traitée en correctif rapide hors branche (PR directe vers `main`), en cours le 27/11/2026.

**Points ouverts au 27/11/2026** (rang 1 de J3-e2 ; version du point d'étape après la PR #184 : historique, partie I, complément du rang 1 de J3-e2) :
- condition de M34 : **#163 traitée avant la démonstration J4** ;
- identité au bit des sorties du script et de la maquette : aucune batterie (#179, J3-g2) ; remesure manuelle sur stdout seul ; empreinte de la maquette dépendante des numéros de ligne du `.tex` (#189, J3-g2) ;
- marge du noyau seul sur l'exécuteur lent (#110, J3-g1) ; familles de refus hors d'`ArretMoteur` : forme à l'ADR du rang 1 de J3-e2, mise en œuvre par #194 (J4) ; catégorie « placement raté » de C1 (J6) ;
- déjà ouverts : plancher du taux directeur (P181), durée d'une partie (#155), #11, #14 ;
- **(1′) de P215** (refus typé du domaine de validité de S-ζ en ζΔϱ, frontière de S6 à ζΔϱ = 13,231, prévu « en J3-e2 ») : omis du plan d'`architect` du 27/11/2026, donc absent du périmètre décidé (P294) ; rattachement à trancher par le mainteneur (J3-e2 avec son accord noté dans la PR #193, ou J4 avec le levier de taux) ;
- J3-f1 indicative à plus de cinq éléments (S1, #147, #116, #125 pt 2, #163, F2, #190) : à redécouper au point d'étape qui la précède ;
- en attente du mainteneur : #190 (motifs de M27, sans réouverture).

#### 2. Branches suivantes (extrait : lignes 12 et 12 bis, fusionnées)

| Ordre | Branche | Issues | Motif du regroupement et état |
|---|---|---|---|
| 12 | J3-e1 « état initial résolu et test zéro » `claude/j3-e1-etat-initial` — **fusionnée** le 26/11/2026 (PR #174, `4462939`, § 7) | #175, #176, #115, #122 ; #125 (points 3 à 5, sans `Closes`) | Fiche à la fusion : historique, partie I, § 1. |
| 12 bis | « suites de M34 à la table T1 » `claude/j3-suites-m34` — **fusionnée** le 27/11/2026 (PR #184, `d08332c`, § 7) | #168, #170, #171, #172, #173 | Fiche à la fusion : historique, partie I, complément du point d'étape après la PR #184. Chiffres de #171 renvoyés à #88 (J3-f2) et #131 (J3-e3), P267. Suites hors périmètre : #185 à #192 (§ 3). |

#### 4. Décisions du mainteneur (extrait : index de P267 à P293)

P267 à P276 (plan, Q1 à Q6 du rang 0, `824bd44` ; lectures du rang 1) : historique, partie I, complément du rang 10 de la branche 12 bis (texte inchangé), en vigueur. **Index** : P267 périmètre, #171 réduite à huit chiffres, renvois à #88 et #131 ; P268 M27 maintenue, motif précisé ; P269 fiches décidées annotées ; P270 délégations P175 et P211 reconduites ; P271 écart de la contre-épreuve accepté ; P272 workflow pour #172 ; P273 minimum de Δr̄_α en ζ au point anguleux ; P274 cliquet par un bloc 9 dérivé ; P275 gain statique barré, P_36 remesuré ou renvoyé à #111 ; P276 texte du motif de M27.

P277 à P293 (rangs 4 à 10 de la branche 12 bis et point d'étape après la PR #184) et décisions de la session de cette branche : historique, partie I, complément du rang 1 de J3-e2 (texte inchangé), en vigueur. **Index** : P277 critère de #170 corrigé prospectivement (« à au moins un π̄ ») ; P278 aucune recherche au-delà de lv\* = 0,47 ; P279 #185 ; P280 P278 maintenue, #186 ; P281 `MinimumNonEncadre` « minimum aux bornes » ; P282 bornes de `LV_173_ENCADRANTS` ; P283 intervalle [0 ; 1 000 %] par an ; P284 #187 ; P285 P_36 aux colonnes φ ∈ {0 ; 1}, renvoi à #111 ; P286 #188 ; P287 et P288 exceptions à P242 ; P289 #189, cause de l'écart de la maquette ; P290 #190 ; P291 #191, exception à la règle 9 ; P292 #192 ; P293 second `docs:` isolé `2df6a29`.

#### 7. Branches fusionnées (extrait : ligne de `claude/j3-e1-etat-initial`)

| Branche | PR | Jalon | Fusion | Détail |
|---|---|---|---|---|
| `claude/j3-e1-etat-initial` | #174 | J3 (état initial résolu, test zéro) | **26/11/2026, 14:40 UTC, commit de fusion `4462939`** | #175, #176, #115, #122 fermées (absentes des 65 issues ouvertes, relevé du § 3) ; #125 ouverte (points 3 à 5 faits, sans `Closes`). 35 commits hors fusion (`git log --no-merges 831547c..4462939`), consignation `b95a2cf` comprise. P246 à P266 ; ADR 0015 accepté (P258) ; ADR 0014 annoté (F2, F3). Fable : 1 sur 3. Aucun changement de trajectoire ; sortie du script `fb187be1…e088`, remesurée à `4462939`. Branche suivante : ligne 12 bis (§ 1). |

## Partie H : extraits de la tête sortis le 26/11/2026 (point d'étape après la fusion de la PR #162, rang 0 de J3-e1), figés

Sortis de `docs/feuille-de-route.md` à `831547c` (`main`, commit de fusion de la PR #162), pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé, titres décalés d'un niveau. Les numéros P-n restent stables ; ces décisions restent en vigueur tant qu'aucune décision ultérieure ne les remplace. Les renvois « § 1 », « § 3 », « § 4 », « § 7 », « ci-dessous » et « ci-dessus » de ces lignes se lisent dans la présente partie. Les points (a) à (d) du § 4 ci-dessous ont été tranchés par le mainteneur le 26/11/2026 : décisions P242 à P245 (tête, § 4).

### En-tête (extrait : mise à jour de la tête du 17/11/2026, rang 11 de la branche « calibration »)

**Dernière mise à jour** : 17/11/2026, rang 11 de la branche « calibration » (`architect`) — `main` = `890471b` ; branche de travail `claude/j3-calibration` à `6f419bf`, PR brouillon #162 ; rangs 0 à 10 faits, rang 11 en cours, fusion en attente du mainteneur (§ 7) ; points soumis au mainteneur (§ 4) ; décisions P204 à P241 en index (§ 4). Mises à jour antérieures et extraits sortis : historique, partie G et ses compléments (rangs 1 et 11 de la calibration), puis `git log -- docs/feuille-de-route.md`.

### 1. Branche de travail en cours (extrait : fiche de la branche « calibration », à la fusion de la PR #162)

**Calibration** (`claude/j3-calibration`, créée depuis `main` à `890471b` le 16/11/2026 ; PR brouillon #162) : branche décidée par P43 (a), confirmée par P115, placée après la branche « forme du code » par P151 ; ouverture décidée par le mainteneur le 16/11/2026 avec le point d'étape P177 en rang 0 (P200). Plan ci-dessous **décidé** par le mainteneur le 16/11/2026 (P204 à P212, § 4). Fiche de la branche « forme du code », figée à la fusion de la PR #151 : historique, partie G, § 1.

#### Plan décidé de la branche « calibration » (`claude/j3-calibration`) — μ̄ (#92), distribution et ζ (#55), écarts bancaires, ϑ et r̄ (#130), ν_H et λ_H (#62), λ_w (#45)

*Proposé par `architect-approfondi` le 16/11/2026 (point d'étape après la PR #151) ; décidé par le mainteneur le 16/11/2026, option recommandée retenue pour Q1 à Q9 (P204 à P212).*

- **Issues avec `Closes`** (P204) : #92, #55, #130, #62, #45. #45 réduite à λ_w : la calibration conjointe de a_π, k_I et λ_e sur un ratio de sacrifice sourcé (C7 ; critère 23 de la fiche 8, `docs/blocs/banque_centrale.md` § 9.6) demande une réponse à une désinflation, mesurable sur le socle linéarisé : issue nouvelle #163, pour J3-f1 (P204).
- **Motif du regroupement** : μ̄ fixe le seuil x_max de la distribution (#55) et pèse sur la condition d'existence du dividende de la banque (#130, `sec:banque-stationnaire`) ; ϖ_L et ϖ_D déplacent les seuils de #55 (2,660 et 2,697 ans, commentaire de `macro` du 04/10/2026 sur #55) ; ζ (#55) déplace la frontière Δϱ ≈ 13,23/ζ de #143 et le verdict C51 (P161). Une décision unique sur la table calibrée évite cinq états stationnaires de référence successifs.
- **Ordre** : les valeurs de niveau d'abord, qui changent l'état stationnaire de référence (#92, #55, #130, ν_H de #62), puis les vitesses, qui ne doivent pas le changer (λ_H de #62, λ_w de #45).
- **Experts pilotes** (`docs/blocs/README.md`) : `macro` pour #92 (bloc 4), #55 (bloc 6), #62 (bloc 5) et #45 (bloc 3) ; `monnaie` pour #130 (blocs 7 et 8). Consultés : `monnaie` sur #55 (frontière crédit) et #45 (frontière inflation) ; `macro` sur #130 (dividende, distribution) ; `jeu` sur #62 (seuil du critère 12 (d) de la fiche 5), #45 (vitesse salariale perçue) et la lisibilité des niveaux retenus.
- **Hors périmètre** : #143 (instruction au rang 1, sans `Closes` ; P148, P207) ; #48 (J4) ; a_π, k_I, λ_e (#163, P204) ; #80 et #139 restent en échec attendu (un succès inattendu suit la règle des tests). Une question de fond qui surgit hors des cinq issues est une condition d'arrêt.
- **Contrats partagés** : aucun attendu (ni équation, ni phase, ni variable d'état). Changent : `tab:calibration`, `tab:etat-stationnaire` et la colonne « valeur résolue » de `tab:criteres-j3` (P209).

| Rang | Étape | Agent | Circuit |
|---|---|---|---|
| 0 | **Fait (`afa9e89`)** : point d'étape P177 et plan ; partie G de l'historique ; PR brouillon #162 ; décisions P204 à P212 consignées | `architect-approfondi`, session | `docs:` |
| 1 | Instruction dans la fiche transverse `docs/blocs/calibration.md` (P205), une section par issue, dans l'ordre #92, #143 (P207), #55 (avec ζ et la frontière de #143), #130, #62, #45 : définition empirique, sources lues et citées ou « non trouvée », valeur proposée et variantes, tableau avant / après **prédit** par `outils/etat_stationnaire.py` (π̄ = 0, 2 et 10 %), conditions d'existence ; avis de `jeu` | `macro`, `monnaie` ; `jeu` | 1 |
| 2 | **Fait (17/11/2026)** : décision M34 du mainteneur sur la table calibrée entière (T1) et visa du tableau prédit (P206 ; colonnes E1 à E3 du § 7.5 de `docs/blocs/calibration.md`) | mainteneur | visa |
| 3 à 7 | **Fait** (`d7163ca` à `a5beb24`, P234 à P238) — Un commit `code:` (et `tests:`) par issue, même ordre : valeurs et sources des tables et des défauts du script, valeurs publiées des tests ; tableau avant / après mesuré ; référence d'empreintes nouvelle écrite par la session après visa (P210) | `coder` → `audit` léger ; session | 1 |
| 8 | **Fait (17/11/2026)** — Mesures « après » : bancs sans arrêt à chaque commit (référence finale `ce3662a`, `"arrets": []`), D et BF lient E1 et E6 ; stationnarité du socle complet (6 tests verts) ; P57 ; contrôle des pilotes : `macro` (#92, #55, #62, #45) et `monnaie` (#130) **conformes**, mesuré égal au prédit E3 à 2,763e−10, ζ_c = 3,6605 (T1) ; variantes « ×2 » relatives (P239) | session, `coder` → `audit` ; `macro`, `monnaie` | — |
| 9 | **Fait (17/11/2026)** — Passage unique de `docwriter`, un commit `docs:` par issue : `9cb6ab9` (#92), `4eb70a5` (#55), `406bcc5` (#166), `7d318e2` (#130), `81d4bc5` (#62), `dd5d20f` (#45), `1f86f0a` (fiches 8 et 9) ; `tests:` `228c373` (listes d'attente retirées, contre-épreuve des 309 anciennes valeurs) ; validation de `macro` et `monnaie` « conforme avec réserves » → reprise `82481d7` (docs) et `57046ec` (tests), revérifiée « conforme avec réserves mineures » → `8aed142` (docs), `273913f` (code : sources de ϖ_L, ϑ, r̄), `6f419bf` (tests). Script : 449 comparées, 429 égales, 20 S, aucun écart ; maquette : 148 relevés, 141 reproduits, 1 écart préexistant (`instabilite17.a.n_a4.hausse`), 6 sans objet | `docwriter` ; `macro`, `monnaie` | règle 9 |
| 10 | **Fait (17/11/2026)** — Revue finale complète d'`audit` à `57046ec` : conforme avec réserves, aucun bloquant ni majeur ; empreintes identiques à `ce3662a` ; unitaires 2022 passed, 2 skipped, 2 xfailed ; invariants 780 passed, 3 skipped, 1 xfailed ; concordance et matrices sans écart. `/code-review` (medium) sur `origin/main...HEAD` : rien de bloquant. Audit léger du dernier lot (`git diff 57046ec 6f419bf`) : **conforme, aucun constat** (empreintes identiques à `ce3662a`, bilan 429 / 20 / aucun écart, concordance et matrices sans écart, unitaires 2022 passed) | `audit` | règle 10 |
| 11 | **En cours** — Consignation (`architect`), corps de PR, sortie du brouillon (session), fusion en commit de fusion (mainteneur) | `architect`, session, mainteneur | — |

**Escalades, relances et arrêts des rangs 9 à 11** (détail : PR #162) : `macro` relancé une fois (limite de tours) à la validation du rang 9, `monnaie` une fois à la revérification ; `docwriter` : une relance ciblée (fiches 8 et 9), puis reprise après vérification et dernier lot ; Fable 0 sur 3 ; aucune condition d'arrêt rencontrée.

**Critères d'acceptation, écrits avant l'essai** (communs aux cinq issues) :
- **Sources** : chaque paramètre calibré porte dans sa table (`source`), puis dans `tab:calibration`, une source lue : auteur, titre, année, page ou tableau, série, zone et fenêtre d'observation, date de consultation, définition empirique et dénominateur de la grandeur lue. À défaut : « non trouvée » et le motif du choix de conception (critère 17 de la fiche 7, critère 23 de la fiche 8 ; P208). Un résultat de la v1.5 ou de la v2.0 n'est pas une source.
- **Diff** : chaque commit `code:` ne change que des valeurs et des sources de paramètres déclarés (`src/nations/moteur/parametres/` ; défauts d'`outils/etat_stationnaire.py`, tenus égaux par `test_valeurs_indicatives_egales_a_celles_du_script`), `git diff --stat` cité ; concordance stricte inchangée, **90 labels** ; matrices sans écart.
- **Domaine et existence**, au point fixe du script, à π̄ ∈ {0 ; 2 ; 10 %} : valeur dans le domaine de sa table (refus, jamais écrêtage) ; Div_F > 0 ; condition d'existence du dividende stationnaire de la banque (`sec:banque-stationnaire`, l. 2688 à `890471b`) ; ν_H·λ_H < 1 ; coefficient de richesse > 0.
- **Tableau avant / après** : une ligne par grandeur de `tab:etat-stationnaire` et par valeur résolue B1 à B26 de `tab:criteres-j3`, à π̄ = 0, 2 et 10 %, chacune expliquée par l'issue du commit ; écart relatif entre la valeur mesurée au commit et la valeur prédite et visée au rang 2 ≤ 1e−9.
- **Bancs** : `uv run python outils/empreintes_des_bancs.py --comparer <référence du commit précédent>` en code 1, écart attendu et déclaré, **aucun banc arrêté** (aucune exception consignée) aux trois π\*, 720 pas ; les bancs D et BF lient encore le plafond de E1 et celui de E6 (P184).
- **Stationnarité** : `test_stationnarite_du_socle_complet` et `test_etat_stationnaire_egal_au_script_sur_le_moteur` (`tests/invariants/test_socle_complet.py`) verts aux trois π\* ; batteries vertes ; #80 et #139 en échec attendu, ou marque retirée selon la règle des tests.

**Précisions prospectives de critère** (M34, 17/11/2026, écrites avant le premier commit des rangs 3 à 7 ; précisions, non des déplacements) :
- **Valeur prédite nulle** (§ 7.13 q. 6 de la fiche) : pour les seules valeurs prédites exactement nulles (inflation et hausse par pas à π̄ = 0, B8, B25, B26), « écart relatif ≤ 1e−9 » se lit « écart ≤ 1e−12 en valeur absolue, dans l'unité de la grandeur ».
- **Tests C62 à 720 pas** (§ 7.16 (a) de la fiche ; avant le commit de #55, qui porte #166, et avant celui de λ_w) : la valeur « arrêt au pas 543 » n'est plus attendue. Les deux tests de C62 restent publiés **sans verdict** ; ils publient la racine dominante identifiée sur la série Δi_CB du moteur (module, argument, temps de doublement si le module dépasse 1), par la méthode de #166, avec la valeur de la maquette en regard ; un arrêt de la trajectoire choquée est publié avec son pas, sans valeur attendue. Aucun critère jugé ne porte sur ces valeurs.

**Critères propres** :
- **#92** : part salariale du modèle ΣWB/ΣVA (fraction ; dénominateur : valeur ajoutée, égale au PIB nominal en économie fermée sans consommation intermédiaire ; 12 tours ; π̄ = 2 %) à 1 point au plus de la valeur de la source, sous la définition retenue (rémunération des salariés, corrigée ou non du revenu mixte ; valeur ajoutée brute ou nette ; secteur ; année). Publiés avant / après : distribution (#55), dividendes sur ventes, dette consolidée (C42), θ_G.
- **#55** : taux de distribution stationnaire (définition de la fiche 6, § 9.6) dans [0,2 ; 0,9] à π̄ ∈ {0 ; 2 ; 10 %}, et sous Δϱ = −2 points permanent lu sur le taux directeur, écarts constants (M33), au ζ retenu ; capital p K^vol/(12 PIB) (B12 ; années de PIB ; ouverture) rapporté à une source de capital productif au coût de remplacement, définition déclarée ; ζ sur une source, ou déclaré. Publiés : verdict C51 « à ζ calibré » (P161) ; frontière de #143 au ζ retenu.
- **#130** : ϖ_L et ϖ_D sur des écarts observés (série, zone, fenêtre) ; ϑ sur une source, définition déclarée (fonds propres sur crédits, distincte d'un ratio sur actifs pondérés) ; r̄ déclaré contesté (critère 23), avec la fourchette des sources lues. Publiés, sans cible : marge nette d'intérêt et rendement des fonds propres, à π̄ = 0, 2 et 10 %.
- **#62** : ν_H·λ_H < 1 et 0,080 ≤ λ_H ≤ 0,634 (seuil de `jeu` du critère 12 (d) à ν_H = 1, remesuré au ν_H retenu) ; tableau du § 9.7 de la fiche 5 ; λ_H seul ne change aucune valeur de `tab:etat-stationnaire` (écart relatif ≤ 1e−12).
- **#45** : λ_w et la pente λ_w·β dans la fourchette des sources lues (celles de l'issue, à relire contre leur texte) ; aucune valeur de `tab:etat-stationnaire` ne change (écart relatif ≤ 1e−12 : une vitesse ne détermine pas l'état d'arrivée) ; demi-vie de la règle SN publiée avant / après, en tours ; critère 5 (d) de la fiche 3 (boucle salaires-prix) remesuré.

**Non-régression** : le critère « identique au bit » ne vaut pas pour une calibration. Il est remplacé par une chaîne : (i) diff limité aux valeurs et aux sources ; (ii) tableau mesuré égal au tableau prédit et visé ; (iii) bancs complets, sans arrêt ; (iv) référence d'empreintes nouvelle, `outils/empreintes_des_bancs_<sha>.json`, écrite par la session après visa (jamais par un agent ni un workflow), contre laquelle le commit suivant se compare. Un commit qui ne touche pas aux valeurs (outil, test) garde le critère « identique au bit » contre la dernière référence. La référence `59e1c1b` reste la mesure « avant » de la branche.

**Mesures du rang 8 (17/11/2026)** : coût P57 (socle complet 0,1201 ms par pays-semaine, run 44073211655), canal rentier ↔ rayon, consignes pour `docwriter` : historique, partie G, complément du rang 11 de la calibration.

**Conditions d'arrêt** : source illisible ou introuvable (aucune valeur inventée ; P208) ; valeur hors domaine ou condition d'existence violée ; calibration qui exige une équation nouvelle ou modifiée (réouverture de fiche par une décision M-n) ; ligne du tableau inexpliquée, ou écart au prédit > 1e−9 relatif ; vitesse qui change l'état stationnaire (continuum d'équilibres, à déclarer) ; banc arrêté, ou banc D ou BF qui ne lie plus son plafond ; frontière de #143 atteinte par un banc ; désaccord entre `macro` et `monnaie` ; part d'un bloc > 0,48 ms ou noyau seul > 0,5 ms sur la plateforme de référence ; constat bloquant ou majeur après la reprise unique.

**Effet attendu sur les résultats** : #92, #55, #130 et ν_H (#62) changent l'**état stationnaire de référence**, résultat final soumis au mainteneur, et toutes les trajectoires ; λ_H et λ_w changent les trajectoires hors du point fixe et les verdicts des bancs choqués (visa de l'expert pilote, du mainteneur si un verdict de scénario change). Aucun changement d'équation, de phase ni de variable d'état. `tests/references/` n'existe pas encore (J3-g2).

**Délégation** : P175 reconduite (P211) : choix de forme à la session ; valeurs, résultats finaux et critères au mainteneur. **Budget Fable** : aucune consultation prévue ; une au plus, sur désaccord entre `macro` et `monnaie` (`docs/agents/routage.md` § 4.1) ; 0 sur 3.

### 2. Branches suivantes (extrait : ligne 11, branche « calibration », avant la fusion)

| Ordre | Branche | Issues | Motif du regroupement et état |
|---|---|---|---|
| 11 | **calibration `claude/j3-calibration` (rangs 0 à 10 faits ; fusion en attente du mainteneur, § 7 ; PR #162)** | #92, #55, #130, #62, #45 | Paramètres et sources ; état stationnaire de référence visé (M34), avant tout test zéro (P209). |

### 3. Issues hors plan (extrait : relevé du 16/11/2026 après la PR #151, avec les issues proposées au rang 11, les points ouverts et les dépendances)

*Relevé du 16/11/2026* (point d'étape après la fusion de la PR #151, `main` = `890471b`) : **51 issues ouvertes** (`list_issues`, état ouvert, `totalCount` = 51, `architect-approfondi`, 16/11/2026) ; #137, #142, #144, #150 et #149 fermées (fermetures vérifiées par la session le 16/11/2026) ; #152 à #156 créées pendant la branche « forme du code » ; #157 à #161 créées par la session le 16/11/2026 (P201), soit 56 issues ouvertes. Branches J3-e1 à J3-g2 : découpage décidé (§ 2, P212). #163 à créer par la session (P204). Relevé précédent (16/11/2026 après la PR #146) : historique, partie G, § 3 ; relevés antérieurs : parties F, E, C et A, § 3. La colonne « Branche prévue » n'est pas reportée sur GitHub. Erratum sur le commit `afa9e89` : historique, partie G, complément du rang 1 de la calibration.

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #10 | Registre d'exemptions de la concordance | hors plan | aucune exemption prévue |
| #11, #14 | Dependabot ; ruleset de `main` | mainteneur, hors branche | `ready-for-human` depuis le 30/09/2026 |
| #37 | Aucun levier d'offre au socle | J4, au plus tard J7 | M26, M28 |
| #45, #55, #62, #92, #130 | Calibrations (λ_w ; fiche 6 et ζ ; ν_H et λ_H ; μ̄ ; ϖ_L, ϖ_D, ϑ, r̄) | **calibration, en cours (§ 1)** | #45 réduite à λ_w (P204) ; ζ déplace la frontière de #143 ; C51 « à ζ calibré » (P161) |
| #46, #47, #48 | Okun ; prix administrés ; levier de répartition | J4 (#47 puis J7) | inchangé |
| #52, #53, #63, #70, #79 | Restitutions et scénarios O2, O3 | J4 | inchangé |
| #54, #56 | Aller-retour de π\* ; signe net d'une hausse de taux | J4, sans `Closes` | condition (c) du levier de cible sur #54 (P99) ; durée d'une partie : #155 (P180) |
| #57 | Crises de crédit sous la règle F | J6 | inchangé |
| #64 | S-ζ hors cible durable | J5 | inchangé |
| #78, #89 | Coût de la dette ; stratégie dominante | J4 (#78 puis J6) | #89 dépend de #88 |
| #80 | Superneutralité (critère 13 de la fiche 8) | hors branche, échec attendu | mesure à republier au r̄ et au ζ calibrés (#130, #55) ; voie (c) de M32 maintenue |
| #81, #82 | Restitutions des blocs 8 et 9 | J4 | #81 : plancher du taux directeur, avis de `monnaie` avant le J4 (P181) ; #82 amendée (P178) |
| #87, #88, #111 | D_F ≥ 0 hors stationnaire ; fenêtre longue ; trajectoires C-HS | J3-f2 (P42, P60) | #116 → #111 |
| #108 | Identifiants Cn et Co | J5 | P46 (a) |
| #110 | Processeur de l'exécuteur en CI | J3-g1 (P60) | attribution de la marge du noyau seul (0,4995 ms au run 43942786775, seuil 0,5) |
| #114, #131 | Critère I1 ; BC2 en log | J3-e3 (#131 mesuré à #114, P101) | reçoit les lignes (c) des fiches 5 et 6 (P122) et l'exécution de #139 et #140 |
| #115, #122 | Radical `observation` ; IN^vol = 0 ⇒ IN = 0 à l'état chargé | J3-e1 (P84) | inchangé |
| #116, #147 | Maquette conjointe ; C62 en régime linéaire | J3-f1 (S1) | #147 reçoit l'harmonisation « 63 tours » (P178) |
| #120 | `Cadre` à n_a ≠ 12 | J3-e2 (P82, option (a)) | inchangé |
| #125 | Facteur de croissance par pas | points 3 à 6 : J3-e1 ; point 2 : J3-f1, `Closes` | point 1 réalisé en J3-c (P88) |
| #135 | `tab:phases` et levier de taux au J4 | J4 | recoupe #54, #56 |
| #139, #140 | Critère « Endettement, dépôts » ; bornes (c) de la fiche 6 | J3-e3 (voies P149, P150) | #139 en échec attendu strict : la calibration peut changer le facteur de convergence |
| #141, #145 | Restitution du refus de crédit ; coefficient de richesse sur π\* de la table | J4 (P152) | #141 avec #70 ; #145 avec #54 |
| #143 | S6 : ti = 0 au-delà d'une frontière | instruite au rang 1 de la calibration, sans `Closes` (P207) ; (1′) en J3-e2, levier au J4, crise au J6 (P215) | M28 non rouverte ; caisse : refus voulu (P216) |
| #148 | B_Bk, B_CB ≥ 0 sans contrôle sous rachat net | J4, instruction de `monnaie` avant (P178) | inactif au socle |
| #152 | E5 par colonne des entreprises | J5 (P172) | point 3 de #150 |
| #153 | Noyau : résidu/S infini à échelle nulle | J3-e2 (P178) | refus typé |
| #154 | Plafond de E1 sous placement raté prolongé | J3-f2 (P178) | inchangé |
| #155 | Durée d'une partie | avant le J4 (P180) | décisions du mainteneur |
| #156 | Bloc 7 : lecture nette de D_H et D_F hors de la phase 6 | J3-g1 (P212) | P191 ; suite de #142, critère « identique au bit » |
| #157 | Tests textuels de `src/` : m1 (P202), R1, R2 | correctif rapide (P212), sinon J3-e2 | `tests:` seul, résultats identiques |
| #158 | T3 : domaine de μ̃, exceptions brutes | J3-e2 (P212) | `travail.py:73` et `:90` |
| #159, #160, #161 | f(π\*_t) deux fois ; contrôles refaits par `etat_de_cloture` ; i_L·L/n_a et δK/n_a recalculés | J3-g1 (P212) | critère « identique au bit » ; #161 recoupe #144 point 2 et respecte C41 |
| #163 | C7 : a_π, a_I, λ_e sur un ratio de sacrifice sourcé (fiche 8, critère 23) | J3-f1 (P204) | créée le 16/11/2026 ; après M34 (λ_w de #45) et S1 |
| #164 | δ et consommation de capital fixe ; dividendes dans la valeur ajoutée | hors branche (P214) | née de l'instruction de #92 |
| #165 | Indicateur d'investissement au tour | J4 (P221) | avis de `jeu` sur ζ = 8 |
| #166 | Estimateur de C62 (racine complexe) | calibration, rang 3 (P223) | ajout au périmètre |
| #167 | Bêta des dépôts (limite de B2) | J4 ou J6 (P227) | née de l'instruction de #130 |
| #168 | Instabilité 17 : lecture (a) des ménages à la table de M34, motif de stabilité de M27 | à rattacher au point d'étape | née de M34 (§ 7.14 de la fiche de calibration) |
| #169, #170 | Critère « Endettement » de #139 en enveloppe ; cas lv\* = 0,45 à la table | J3-e3 (avec #139) ; à rattacher | P240 |
| *proposée 1* | `macro` : remesure à la table T1 (M34) des chiffres encore publiés à la calibration indicative (+141 pb et 0,42 % de #88 ; 79 tours de cliquet ; gain statique −0,2208 % ; π\* < 2 760 % à λ_H = 0,8 ; pas 182 sous φ = 0 ; dépôts 12,03 à 12,25 mois ; r̂\* de #131 ; lignes P_36 de la table φ de la fiche 9 ; 2,08 de la maquette de la fiche 8 ; « 1,0000 » arrondi de `socle.marge_conjointe.x2.a_I÷1000`) | à rattacher | **proposée, en attente d'accord** (rang 11) |
| *proposée 2* | `audit` + `/code-review` : outils de calibration, robustesse des tests et des cartes de la maquette après M34 (`racine_dominante` sur cible de norme nulle ; défauts `lambda_w`, `nu_H` figés à l'import ; variantes λ_v, λ_IN, λ_μ littérales ; grille du test du minimum en ζ ; `frontiere_ou_aucune` sans échantillonnage intérieur ; `ENTREES_D_ORIGINE` sans ζ ni λ_w ; `BORNES_MARGE_HAUSSE` doublon de `BORNES_MARGE` ; `ZETA_PLAGE` (4, 8) décrite comme plage de la table) | à rattacher | **proposée, en attente d'accord** (rang 11) |
| *proposée 3* | `coder` / `monnaie` : libellé « Δr̄_α au minimum en ζ (ζ = 68) » trompeur à T1 (minimum à 63, 0,1598, non contrôlé par une ligne du script) | à rattacher | **proposée, en attente d'accord** (rang 11) |

**Points ouverts sans issue** : mutant équivalent B_Bk/Res dans B5, à rouvrir avec le corridor (J6, P116) ; résolution de l'état initial par `scenarios/` sans dupliquer le script (J3-e1 ; A1 compare les deux) ; réserves mineures de J3-d2 non corrigées (lectures de `TABLEAU_DES_PHASES` non reliées au `.tex`, contrôle de priorité du critère 12 doublé par le noyau pour les erreurs qui créent un découvert, coût du socle complet publié sans verdict jusqu'à G1, J3-g2) ; divergences du texte de l'ADR 0013 relevées par l'ADR 0014 (n5.1, n1.5, n6.3, n1.4, n7.5 ; compte rendu du rang 9, PR #151), sans effet sur les règles : première annotation possible de l'ADR 0014. Levé : branche distante `ccr-063dc6fc-vo9lzk` (absente de `git ls-remote origin` le 16/11/2026, `architect-approfondi`).

**Dépendances** (16/11/2026, après la PR #151). **Ajoutées** (décidées, P204, P207, P212) : #92 → #55 → #130 (seuils de distribution et du dividende de la banque) ; instruction de #143 → section de #55 au rang 1 ; #45 (λ_w, M34) → #163 (J3-f1) ; S1 → #163 ; J3-e1 → J3-e2 et J3-e3 (états chargés, socle complet depuis l'état résolu) ; J3-f1 → J3-f2 ; J3-g1 → J3-g2 (G1 mesuré après le chemin chaud). **Retirées** (levées par la fusion de la PR #151) : annotation de l'ADR 0013 → #144, #150 ; #142 et #150 → #144 points 2 et 3 ; branche « forme du code » → reconsolidation de l'ADR 0013 (ADR 0014) ; branche « forme du code » → calibration (P151). **Inchangées** : branche de calibration → J3-e ; #143 → domaine du levier de taux (J4) et #55 ; avis de `monnaie` sur la caisse des entreprises → #143 ; #145 → #54 ; #141 → J4 (avec #70) ; #131 → #114 ; #116 → #111 ; #89 → #88 ; #148 → leviers du J4 ; #152 → J5.

### 4. Décisions du mainteneur (extrait : points soumis au mainteneur au rang 11 de la calibration et points ouverts après M34, 17/11/2026)

**Points soumis au mainteneur au rang 11 de la calibration** (17/11/2026 ; aucun n'est tranché) :
- (a) **Découpage par domaine** : 7 commits `docs:` du rang 9 touchent aussi `outils/` (`9cb6ab9`, `4eb70a5`, `7d318e2`, `81d4bc5`, `dd5d20f`, `1f86f0a`, `82481d7` ; `git show --stat`) : littéraux de valeurs publiées liés à leur texte par `test_valeurs_en_vigueur_ecrites_hors_barre_dans_leur_source` ; `4eb70a5` restructure aussi trois boucles de `releve()`, `82481d7` change un libellé de provenance. Exception à consigner, éventuellement règle à écrire dans `CLAUDE.md`.
- (b) **Critère « Diff »** : changements de structure dans des commits `code:` de valeurs, non consignés comme écarts acceptés (seul P234 l'est) : `ENTREES_D_ORIGINE` et contre-épreuve (`d7163ca`), libellés `roe` et `marge_nette` (`3c8156e`), `frontiere_ou_aucune` (`ce3662a`).
- (c) **Noms de pays dans les sources** : des chaînes `source` du moteur citent « États-Unis » ou « zone euro » comme provenance de données (`src/nations/moteur/parametres/` : `menages.py:63`, `travail.py:43` et `:48`, `investissement.py:78` et `:82`, `banque_centrale.py:82` (r̄), `banque.py:55`) ; compatibilité avec « aucun nom de pays réel associé aux configurations » (M17).
- (d) **Trois issues proposées**, non créées (§ 3).

**Points ouverts au 17/11/2026, après M34** (décision du mainteneur) : marge du noyau seul sur l'exécuteur lent (#110, J3-g1) ; déjà ouverts : plancher du taux directeur (P181), durée d'une partie (#155), #11, #14.

### 7. Branches fusionnées (extrait : ligne de `claude/j3-calibration` avant la fusion, ligne de `claude/j3-forme-du-code`)

| Branche | PR | Jalon | Fusion | Détail |
|---|---|---|---|---|
| `claude/j3-calibration` | #162 (brouillon) | J3 (calibration) | **en attente** : sortie du brouillon par la session, fusion par le mainteneur en commit de fusion | `Closes` prévus : #92, #55, #130, #62, #45 et #166 (ajoutée au périmètre, P223) ; fermetures à vérifier après la fusion. 57 commits à `6f419bf` (12 `code:`, 11 `tests:`, 34 `docs:` ; `git rev-list --no-merges origin/main..6f419bf`). Décision M34 (table T1) ; P204 à P241. Fable : 0 sur 3. Changement de l'état stationnaire de référence visé (M34) ; références d'empreintes `59e1c1b` et `ce3662a` ; `tests/references/` absent. Condition de M34 : **#163 traitée avant la démonstration J4**. Prochaine branche : J3-e1 (§ 2, ligne 12), non ouverte. |
| `claude/j3-forme-du-code` | #151 | J3 (forme du code) | 16/11/2026, 20:27 UTC, commit de fusion `890471b` (parents `2744be3`, `165f027`), par le mainteneur | Issues fermées par `Closes` : #137, #142, #144, #150, #149 (fermetures vérifiées par la session le 16/11/2026). 47 commits hors fusion (12 `code:`, 17 `tests:`, 18 `docs:` ; `git rev-list --no-merges 2744be3..165f027`). CI de `165f027` (run 43947734302, passation de la session sur la PR #151) : quatre jobs en succès. Rangs et SHA : historique, partie G, § 1, et corps de la PR #151. Décisions : P172 à P199. Fable : 1 sur 3 (ADR 0014). Trajectoires identiques au bit (code 3 avec `--exclure-variables`, P197) ; aucun résultat final ; `tests/references/` intact. Concordance : 90 labels. Issues nées de la branche : #152 à #156 ; #157 à #161 (P201, créées le 16/11/2026). |


### Complément sorti le 26/11/2026 au rang 10 de J3-e1 (`claude/j3-e1-etat-initial`, tête `285e6aa`, PR #174)

Sortis de `docs/feuille-de-route.md` pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé (titre du plan décalé de deux niveaux). Les numéros P-n restent stables ; P242 à P245 restent en vigueur. Les renvois « § n », « ci-dessous » et « ci-dessus » de ces lignes se lisent dans la tête à `285e6aa`.

#### En-tête (extrait : mise à jour de la tête du 26/11/2026, rang 1 de J3-e1)

**Dernière mise à jour** : 26/11/2026, rang 1 de J3-e1 (`architect-approfondi`, Fable 1 sur 3) — `main` = `831547c` (commit de fusion de la PR #162, § 7) ; branche de travail `claude/j3-e1-etat-initial` à `eed2d31`, PR brouillon #174 ; plan de J3-e1 **décidé** (§ 1 ; P246 à P257, § 4) ; #175 et #176 créées ; **ADR 0015 proposé**, à accepter (points S1 à S10) ; relevé des issues du 26/11/2026 (§ 3). Mises à jour antérieures et extraits sortis : historique, partie H (fiche de la branche « calibration », relevé du 16/11/2026, points soumis au rang 11), puis parties G à A et `git log -- docs/feuille-de-route.md`.

#### 1. Branche de travail en cours (extrait : fiche de J3-e1 telle que décidée, avec l'état des rangs à `285e6aa` avant la consignation du rang 10)

**J3-e1 « état initial résolu et test zéro »** (`claude/j3-e1-etat-initial`, créée depuis `main` à `831547c` le 26/11/2026 ; PR brouillon #174) : ouverture décidée par le mainteneur le 26/11/2026 (ligne 12 du § 2 ; découpage P212). Plan ci-dessous **décidé** par le mainteneur le 26/11/2026 (P246 à P257, § 4). Fiche de la branche « calibration », figée à la fusion de la PR #162 : historique, partie H, § 1.

##### Plan de J3-e1 (`claude/j3-e1-etat-initial`) — état initial résolu par `scenarios/` (#175), test zéro et `observation/` (#176), radical `observation` (#115), cohérence de l'état chargé (#122), formes du script (#125, points 3 à 5)

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

#### 3. Issues hors plan (extrait : en-tête du relevé du 26/11/2026, renvoi du point « résolution par `scenarios/` » et dépendances, avant le rang 10)

*Relevé du 26/11/2026* (point d'étape après la fusion de la PR #162, `main` = `831547c`) : **63 issues ouvertes** (`list_issues`, état ouvert, `totalCount` = 63, `architect-approfondi`, rang 1, 26/11/2026 ; 61 au rang 0, plus #175 et #176). #92, #55, #130, #62, #45 et #166 ont été fermées par la PR #162 (fermetures vérifiées par la session le 26/11/2026) ; #163 à #173 ont été créées depuis le relevé du 16/11/2026 (56 + 11 − 6 = 61). Relevé précédent : historique, partie H, § 3. La colonne « Branche prévue » n'est pas reportée sur GitHub.

Le point « résolution de l'état initial par `scenarios/` sans dupliquer le script » est passé au plan de J3-e1 (§ 1, P247, ADR 0015).

**Dépendances** (26/11/2026, après la PR #162).
- **Ajoutées** (décidées le 26/11/2026) : #115 → #176 ; #175 → #122, #125 (points 3 à 5), #176 ; J3-e1 → ligne 12 bis (#172 et #173 touchent `outils/etat_stationnaire.py`, que #175 réorganise ; P255) ; S1 → F2 (P249) ; #172 point 4 → #173 (grille). **Ajoutée au rang 1** : acceptation de l'ADR 0015 → #175, #122, #176 (rangs 3, 4 et 6) ; #115 (rang 2) n'en dépend pas.
- **Retirées**, levées par la fusion de la PR #162 : #92 → #55 → #130 ; instruction de #143 → section de #55 ; #45 (λ_w, M34) → #163 ; branche de calibration → J3-e.
- **Inchangées** : S1 → #163 ; #163 → démonstration J4 (condition de M34) ; J3-e1 → J3-e2 et J3-e3 ; J3-f1 → J3-f2 ; J3-g1 → J3-g2 ; #143 → domaine du levier de taux (J4) ; avis de `monnaie` sur la caisse des entreprises → #143 ; #145 → #54 ; #141 → J4 (avec #70) ; #131 → #114 ; #116 → #111 ; #89 → #88 ; #148 → leviers du J4 ; #152 → J5.

#### 4. Décisions du mainteneur (extrait : P242 à P245)

Points (a) à (d) soumis au mainteneur au rang 11 de la calibration (texte du 17/11/2026 : historique, partie H, § 4), tranchés par le mainteneur le 26/11/2026 selon l'avis proposé.
- **P242** (a) : **exception consignée au découpage par domaine.** Un commit `docs:` qui republie des valeurs peut modifier, dans `outils/`, les littéraux de valeurs publiées que `test_valeurs_en_vigueur_ecrites_hors_barre_dans_leur_source` (`tests/unitaires/test_etat_stationnaire.py`) lie au texte : les séparer ferait échouer la batterie au commit intermédiaire. La règle sera écrite dans `CLAUDE.md` par la session (`claude:`), sur accord du texte proposé (Q11). Hors de l'exception, deux changements avaient été relevés au point (a) : trois boucles de `releve()` restructurées (`4eb70a5`) et un libellé de provenance (`82481d7`) ; leur traitement est soumis au mainteneur (Q11).
- **P243** (b) : trois changements de structure non déclarés au critère « Diff » de la calibration sont **mentionnés à l'historique, sans autre suite** : `ENTREES_D_ORIGINE` et la contre-épreuve (`d7163ca`) ; les libellés `roe` et `marge_nette` (`3c8156e`) ; `frontiere_ou_aucune` (`ce3662a`). Mention portée au § 7, ligne de la PR #162.
- **P244** (c) : les chaînes `source` des tables qui citent « États-Unis » ou « zone euro » sont **compatibles avec M17** : elles donnent la provenance d'une donnée, pas une configuration de pays. Relevé à `831547c` (`src/nations/moteur/parametres/`) : `banque.py:39`, `:41` et `:55`, `investissement.py:78` et `:82`, `menages.py:63`, `prix.py:40`, `travail.py:43` et `:48`. Liste du 17/11/2026 : historique, partie H, § 4.
- **P245** (d) : **trois issues créées par la session le 26/11/2026** : #171 (remesure à T1 des chiffres « à la calibration indicative », `macro`), #172 (robustesse des outils de calibration après M34) et #173 (libellé « Δr̄_α au minimum en ζ (ζ = 68) »). Rattachement proposé : § 2, ligne 12 bis (Q10).

#### 7. Branches fusionnées (extrait : ligne de `claude/j3-calibration`)

| Branche | PR | Jalon | Fusion | Détail |
|---|---|---|---|---|
| `claude/j3-calibration` | #162 | J3 (calibration) | 26/11/2026, 06:33 UTC, commit de fusion `831547c` (parents `890471b`, `e60edb5`), par le mainteneur | Issues fermées par `Closes` : #92, #55, #130, #62, #45 et #166 (ajoutée au périmètre, P223) ; fermetures vérifiées par la session le 26/11/2026. 49 commits hors fusion : 12 `code:`, 11 `tests:`, 26 `docs:` (`git rev-list --no-merges 890471b..e60edb5`). **Erratum** : la ligne d'attente (historique, partie H, § 7) annonçait « 57 commits à `6f419bf` (34 `docs:`) » ; la même commande donne 47 commits à `6f419bf`, dont 24 `docs:`. Fiche, rangs et SHA : historique, partie H, § 1, et corps de la PR #162. Décision M34 (table T1) ; P204 à P241 ; P242 à P245 au point d'étape. Fable : 0 sur 3. L'état stationnaire de référence change, visé (M34). Références d'empreintes `59e1c1b` et `ce3662a` ; les empreintes à `831547c` sont identiques à `ce3662a` (code 0, 26/11/2026). `tests/references/` absent. Écarts au critère « Diff » mentionnés sans suite (P243) : `d7163ca`, `3c8156e`, `ce3662a` ; exception au découpage par domaine : P242. Condition de M34 : **#163 traitée avant la démonstration J4**. Branche suivante : J3-e1 (§ 1). |

## Partie G : extraits de la tête sortis le 16/11/2026 (point d'étape après la fusion de la PR #151, rang 0 de la branche « calibration »), figés

Sortis de `docs/feuille-de-route.md` à `890471b` (`main`, commit de fusion de la PR #151), pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé, titres décalés d'un niveau. Les numéros P-n restent stables ; ces décisions restent en vigueur tant qu'aucune décision ultérieure ne les remplace. Les renvois « § 1 », « § 3 », « ci-dessous » et « ci-dessus » de ces lignes se lisent dans la présente partie.

### En-tête (extrait : mise à jour de la tête du 16/11/2026, rang 9 de la branche « forme du code »)

**Dernière mise à jour** : 16/11/2026, rang 9 de la branche « forme du code » (`architect`) — `main` = `2744be3` ; branche de travail `claude/j3-forme-du-code` à `2355516`, PR brouillon #151 ; rangs 0 à 9 faits (ADR 0014 : `4e02204`) ; décisions P182 à P199 (§ 4 ; P172 à P181 : historique, partie F) ; fusion en attente du mainteneur. Mises à jour antérieures : historique, parties F, E, puis `git log -- docs/feuille-de-route.md`.

### 1. Branche de travail en cours (extrait : fiche de la branche « forme du code », à la fusion de la PR #151)

**Forme du code** (`claude/j3-forme-du-code`, créée depuis `main` à `2744be3` le 16/11/2026 ; PR brouillon #151) : branche décidée par P151 (précise P115), ouverture confirmée par le mainteneur le 16/11/2026 avec le point d'étape en rang 0 ; plan ci-dessous **décidé** par le mainteneur le 16/11/2026 (P172 à P179 : historique, partie F, complément du rang 9). Fiche de J3-d2, figée à la fusion de la PR #146 : historique, partie F, § 1.

#### Plan de la branche « forme du code » (`claude/j3-forme-du-code`) — refus génériques (#137), localité de la lecture nette (#142), travail redondant du chemin chaud (#144), forme du code du bloc 9 (#150)

*Proposé par `architect` le 16/11/2026 (point d'étape après la PR #146) ; décidé par le mainteneur le même jour (P172 à P179 : historique, partie F, complément du rang 9).*

- **Issues avec `Closes`** (Q1) : #137, #142, #144 (P151) et #150 (points 1 et 2, docstrings), qui recoupe #142 (localité du bloc 9) et #144 (E7 calculé deux fois sur le chemin chaud) ; le point 3 de #150 (E5 par colonne) demande une lecture de fond (colonne de chaque ligne, précédent de la ligne 18 lue dans `entreprises_capital`) : détaché dans une issue nouvelle pour le J5 (Q1 (a)).
- **Hors périmètre** : #147 (J3-f), #148 (J4), issue du noyau (J3-e, P178) ; #149 entre au périmètre (P174), au passage de `docwriter` ; aucune question de fond attendue : une question de fond qui surgit est une condition d'arrêt, jamais un ajout.
- **Contrats partagés touchés** (`docs/agents/routage.md` § 4.2), d'où le rang 1b avant tout code : #144 point 1 (domaines : `schema.defaut_de_domaine` « appelée à toute construction » et `Vue.ecrire_etat`, ADR 0013, D et annotation du rang 1b de J3-d1) ; #144 point 2 (conversions invariantes publiées une fois : grandeur d'ouverture, C3, ou champ dérivé d'une table de paramètres, F) ; #144 point 3 (`g` « reste publiée », ADR 0013, annotation du 14/11/2026, point 7 ; `sec:cadre-calendrier`, « huit » grandeurs d'ouverture) ; #150 point 1 si E7 devient une variable du pas (`tab:phases`, lien exact de P170) ; #150 point 2 (position du grand livre « toujours admise », `src/nations/moteur/contrat_bloc.py:28`). #137 et #142 n'en touchent aucun.
- **Experts** : aucun pilote requis (aucune équation ni coefficient ne change) ; `macro` contrôle au rang 6 la conformité des fonctions balisées touchées par #142 et #150 à leurs labels. **Délégation** : Q4. **Budget Fable** : une consultation au plus, pour la reconsolidation de l'ADR 0013 (Q5, § 4.1.3) ; 1 sur 3 utilisée au rang 9 (ADR 0014).

| Rang | Étape | Agent | Circuit |
|---|---|---|---|
| 0 | **Fait** (`eff1c3f`, `084e2d1`) — Point d'étape et plan (présente mise à jour) ; partie F de l'historique ; PR brouillon | `architect`, session | `docs:` |
| 1a | **Fait** (`6a2a544` à `0d35718` ; P57 « avant » : PR #151) — Mesures « avant » : banc d'empreintes du socle complet en script d'`outils/` (Q2) ; empreintes à `2744be3`, arbre identique à `59e1c1b` (`git diff 59e1c1b 2744be3` vide) ; parts P57 et noyau seul lus dans le journal du job « Tests » du run 43758540925 (`59e1c1b`) | `coder` → `audit` (script) ; session (journal) | 3 |
| 1b | **Fait** (`f177cac`) — Annotation de l'ADR 0013 : forme des contrats touchés (#144 points 1 à 3, #150 points 1 et 2) ; décomptes attendus (grandeurs d'ouverture, variables du pas) | `architect` | § 4.2 |
| 2 | **Fait** (`4d44393` à `05541fc`) — #137, puis #144 point 1 (`ordonnanceur.py`, même module, deux commits) | `coder` → `audit` | 3 |
| 3 | **Fait** (`160ba06` à `0e200fc`) — #142 (`menages.py`, `investissement.py`) | `coder` → `audit` | 3 |
| 4 | **Fait** (`ecf9513` à `3c8508c`) — #150 points 1 et 2, docstrings (`finances_publiques.py`, `contrat_bloc.py`, `Vue`) | `coder` → `audit` | 3 |
| 5 | **Fait** (`a379ad7` à `789d854`) — #144 points 2 et 3 (production, travail, investissement, finances publiques, `ouverture.py`) : en dernier, sur les fichiers déjà touchés par #142 et #150 | `coder` → `audit` | 3 |
| 6 | **Fait** (`74e215d`, `60e82da` ; P197) — Mesures « après » : empreintes (critère « Branche »), parts P57 et noyau seul (ci-dessous) ; contrôle de `macro` : neuf labels conformes (H3, H4, H5, F3, E6, E7, E5, F1, S7), aucun écart d'équation | session, `coder` → `audit` ; `macro` | — |
| 7 | **Fait** (`03b6503` #137, `7c557b4` #144, `fede56c` #142, `ba4ef6a` #150, `8e241c8` marque retirée après le `docs:` de #150, `2f9d378` #149 ; P198, P199) — Passage unique de `docwriter`, un commit `docs:` par issue ; validé par `macro` et `monnaie` (fiche 8, C59, frontière E7, lectures de position) | `docwriter` ; `macro`, `monnaie` | règle 9 |
| 8 | **Fait** (`8f5d337`, `2cd1c97`, `a09c95d`, `7f7fb13`, `2355516`) — Revue finale complète du `git diff main...HEAD` : `audit` conforme avec réserves, aucun bloquant ni majeur (unitaires 2003 passed, invariants 778 passed, concordance 90/90, matrices sans écart, références intactes) ; `/code-review` ; corrections revues sur leur diff, conformes avec réserves (R1, R2 ; § 3) | `audit`, `/code-review` | règle 10 |
| 9 | **Fait** (consignation : `8bec385` ; ADR 0014 : `4e02204`, statut `accepted` sur le précédent de P76 (b), à confirmer par le mainteneur) — Consignation ; reconsolidation de l'ADR 0013 par l'ADR 0014 (P176), Fable 1 sur 3 | `architect`, `architect-approfondi` | § 4.1.3 |

Le workflow `circuit-technique` met en œuvre les rangs 2 à 5 ; il n'est lancé que **sur commande explicite du mainteneur** (principe 1), au plus une reprise `coder` → `audit` par rang (principe 4), aucun commit par le workflow (principe 2).

**Critères d'acceptation, écrits avant l'essai** :
- **Branche** : trajectoires **identiques au bit** après chaque commit `code:` : `uv run python outils/empreintes_des_bancs.py --comparer outils/empreintes_des_bancs_59e1c1b.json` en code 0 (huit bancs, dont D et BF choqués, trois π\*, 720 pas ; encodage v2, globale `e3c31c79…695bef`, mesurée sur `git archive 59e1c1b` ; P182 à P184) ; code 3 admis pour les seules grandeurs d'ouverture, écart déclaré (P186) ; au rang 4, critère jugé sur `etats` et `montants` (P187) ; depuis `ecf9513` (`iB_BH`, `iB_BBk`, `iB_BCB` ajoutées, P187), la commande se lit avec `--exclure-variables iB_BH iB_BBk iB_BCB` (P197 ; sans l'option, code 1 dû à ces seules variables : lecture de P187, non un déplacement du critère) ; batteries vertes ; concordance inchangée, **90 labels** ; matrices sans écart ; #80 en échec attendu ; `tests/references/` intact.
- **Coût (P57)** : parts de chaque bloc, total du socle complet et noyau seul (C98-1), avant et après, sur la plateforme de référence, publiés par point de #144 et pour #150 point 1 ; aucun seuil de gain (publication, pas verdict) ; part de chaque bloc ≤ 0,48 ms par pas ; noyau seul ≤ 0,5 ms par pas (0,4877 à `a059d10`, marge de 3 %).
- **#137** : les quatre refus génériques de `VariablesDuPas.ecrire` (nom non déclaré, seconde écriture, type refusé, valeur non finie hors de `DOMAINES_DU_PAS`) nomment le pas, l'étape et le bloc écrivain, comme `PlanHorsDomaine` ; un test par refus ; seuls les messages changent.
- **#142** : aucun max(0 ; ·) dans les méthodes `phase_*` de `menages.py` et `investissement.py` ; lecture nette dans les fonctions balisées H3, H4, H5 et F3 (ou une fonction qu'elles appellent) ; le contrôle statique de localité du bloc 9 étendu aux blocs 5 et 6 ; appel direct à D < 0 égal au bit à l'ancien.
- **#144** : point 1 : un seul contrôle de domaine par variable d'état de bloc et par pas (test de décompte), refus au lieu fixé au rang 1b, jamais d'écrêtage ; point 2 : chaque conversion invariante calculée une fois, au lieu fixé au rang 1b, aucune exemption nouvelle du test « conversion unique », aucune reconstruction dans un bloc ; point 3 : `g` retirée si le rang 1b le fixe (aucun lecteur dans `src/`, test de suppression), sinon motif consigné.
- **#150** : point 1 : E7 calculé une fois par pas (test de décompte, modèle du besoin d'émission) ; point 2 : une lecture de position non déclarée dans l'étape est refusée (test sur un bloc fabriqué), les deux lectures existantes admises (`banque.py`, Res en 8c ; `finances_publiques.py`, M_G en 8b) ; docstrings : aucune mention du rang 6 de J3-d2 au futur dans `src/` (`grep` cité).

**Conditions d'arrêt** : une empreinte qui diffère (régression, jamais une référence à régénérer) ; un point qui demande une lecture de fond ou change une équation ; contrat partagé à modifier au-delà de l'annotation du rang 1b ; drapeau de mode ; exemption nouvelle du test « conversion unique » ; part d'un bloc au-dessus de 0,48 ms ou noyau seul au-dessus de 0,5 ms sur la plateforme de référence (arrêt et passation ; l'attribution à la branche se mesure, #110) ; constat bloquant ou majeur après la reprise unique.

**Effet attendu sur les résultats** : aucun sur les trajectoires ; messages de diagnostic (#137), coût (#144, #150 point 1), contrôle des lectures de position (#150 point 2) ; spécification touchée seulement là où elle cite un objet modifié.

**Résultats des rangs 6 à 9** (session et agents ; remesures d'`architect` à `2355516`, 16/11/2026) :
- **Branche** : `--comparer outils/empreintes_des_bancs_59e1c1b.json --exclure-variables iB_BH iB_BBk iB_BCB` → code 3, globale `e3c31c79…695bef`, 24 lignes `grandeurs` seules (P186, P187, P189) ; sans l'option, code 1 (seules les empreintes `variables` diffèrent). Remesuré par `audit` en revue finale après chaque commit `code:` (codes 0, 0 avec l'option, 3) et par `architect` à la tête. Unitaires à la tête : 2005 passed, 2 skipped, 2 xfailed ; invariants 778 passed, 3 skipped, 1 xfailed (#80) ; concordance stricte sans écart.
- **Coût (P57, après)** : plateforme de référence (ubuntu26 20261111.196.1, Python 3.12.14) ; `src/` identique de `789d854` à `2355516` (`git diff --stat` vide). Noyau seul / socle complet, ms par pas (ms par pays-semaine) : run 43924239462 (`4cba1d1`) 0,2436 / 0,2884 (0,0665) ; 43932725400 (`60e82da`) 0,4970 / 0,5721 (0,1320) ; 43936838926 (`2f9d378`) 0,3179 / 0,3645 (0,0841) ; 43938838794 (`8f5d337`) 0,2509 / 0,2909 (0,0671) ; 43942786775 (`2355516`) 0,4995 / 0,5731 (0,1323). Min / médiane / max : noyau 0,2436 / 0,3179 / 0,4995 ; socle 0,2884 / 0,3645 / 0,5731. Plus forte part : finances publiques, 0,0271 à 0,0525. Avant (run 43758540925) : noyau 0,2540, socle 0,2986 (0,0689), finances publiques 0,0280 ; noyau 0,4877 au run 43744967905. Aucune condition d'arrêt atteinte ; noyau seul à 0,0005 ms du seuil au run 43942786775 (C = min de cinq répétitions, toutes > 0,5) ; distribution bimodale à moteur identique (part du bloc d'essai et durée des invariants doublées aussi) : dispersion d'exécuteur (#110). Publication sans verdict (P57). Chiffres des runs relevés par la session dans les journaux, non remesurés par `architect`.
- **Escalades, relances et arrêts** : `macro` arrêté à sa limite de tours au rang 7, une relance ciblée ; redémarrage du conteneur pendant `docwriter` (travail repris depuis sa transcription, patches vérifiés par recomposition) ; reprise unique `coder` → `audit` aux rangs 6 (majeur d'`audit` : exclusions symétriques, M1) et 8 ; Fable 1 sur 3 (rang 9, ADR 0014).
- **Ligne préparée pour le § 7** (à verser après la fusion, SHA et date à compléter) : `claude/j3-forme-du-code` | #151 | J3 (forme du code) | *date*, commit de fusion *SHA* (parents `2744be3`, *tête*), par le mainteneur | Issues fermées par `Closes` : #137, #142, #144, #150, #149 (fermetures à vérifier). Commits hors fusion : `git rev-list --no-merges 2744be3..<tête>`. Rangs et SHA : § 1 et corps de la PR #151. Décisions : P172 à P199. Fable : 1 sur 3 (ADR 0014). Trajectoires identiques au bit (code 3 avec `--exclure-variables`, P197) ; aucun résultat final ; `tests/references/` intact. Concordance : 90 labels. Issues nées de la branche : #152 à #156, et celles du § 3 si créées.

### 2. Branches suivantes (extrait : ligne 10 bis, branche « forme du code », fusionnée)

| Ordre | Branche | Issues | Motif du regroupement et état |
|---|---|---|---|
| 10 bis | **forme du code `claude/j3-forme-du-code` (décidée, P151 ; rangs 0 à 9 faits, fusion en attente, § 1)** | #137, #142, #144, #150 (P172), #149 (P174) | Circuit 3, conduit à la main (P190) ; trajectoires identiques au bit (P197), P57 avant / après publiée ; ADR 0014 (P176). Avant la calibration. |

### 3. Issues hors plan (extrait : relevé du 16/11/2026 après la PR #146, avec ses points ouverts, réserves et dépendances)

*Relevé du 16/11/2026* (point d'étape après la fusion de la PR #146, `main` = `2744be3`) : **51 issues ouvertes** (`list_issues`, état ouvert, `totalCount` = 51, `architect`, 16/11/2026) ; #133, #132, #106, #101 et #134 fermées (état vérifié par la session le 16/11/2026) ; #147 à #150 créées le 15/11/2026 (P171). Les rattachements de #147 à #150 sont décidés (P172, P174, P178). Relevé précédent (15/11/2026 après la PR #136, mis à jour au rang 8 de J3-d2) : historique, partie F, § 3 ; relevés antérieurs : parties E, C et A, § 3. La colonne « Branche prévue » n'est pas reportée sur GitHub.

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #10 | Registre d'exemptions de la concordance | hors plan | aucune exemption prévue |
| #11, #14 | Dependabot ; ruleset de `main` | mainteneur, hors branche | `ready-for-human` depuis le 30/09/2026 (Q8) |
| #37 | Aucun levier d'offre au socle | J4, au plus tard J7 | M26, M28 |
| #45, #55, #62, #92, #130 | Calibrations (λ_w ; fiche 6 ; ν_H et λ_H ; μ̄ ; ϖ_L, ϖ_D, ϑ, r̄) | calibration (P43 (a), P115) | #55 recoupe #92 ; ζ calibré par #55 déplace la frontière de #143 ; C51 « à ζ calibré » (P161) |
| #46, #47, #48 | Okun ; prix administrés ; levier de répartition | J4 (#47 puis J7) | inchangé |
| #52, #53, #63, #70, #79 | Restitutions et scénarios O2, O3 | J4 | inchangé |
| #81 | Restitution du bloc banque centrale | J4 | constat de `monnaie` versé (P171) : taux directeur négatif aux tours 11 à 19 à π\* = 0 ; à signaler à `jeu` (Q7) |
| #82 | Restitution du bloc État et dette | J4 | amendement proposé : indicateurs du pas de F8 et ratios sur 12 tours (Q7) |
| #54, #56 | Aller-retour de π\* ; signe net d'une hausse de taux | J4, sans `Closes` | condition (c) du levier de cible sur #54 (P99) ; durée d'une partie : #155 (P180) |
| #57 | Crises de crédit sous la règle F | J6 | inchangé |
| #64 | S-ζ hors cible durable | J5 | inchangé |
| #78, #89 | Coût de la dette ; stratégie dominante | J4 (#78 puis J6) | #89 dépend de #88 |
| #80 | Superneutralité (critère 13 de la fiche 8) | hors branche, échec attendu | voie (c) de M32 maintenue (P89) ; échec attendu tenu à la fin de J3-d2 |
| #87, #88, #111, #116 | D_F ≥ 0 hors stationnaire ; fenêtre longue ; trajectoires C-HS ; maquette | J3-f (P42, P60) | #116 → #111 |
| #108 | Identifiants Cn et Co | J5 | P46 (a) |
| #110 | Processeur de l'exécuteur en CI | J3-g (P60) | attribution d'un dépassement du noyau seul (§ 1, conditions d'arrêt) |
| #114 | Critère I1 : lignes « J3 » au socle complet | J3-e | reçoit la mesure de #131, les lignes (c) des fiches 5 et 6 (P122) et l'exécution de #139 et #140 (P149, P150) |
| #115 | Radical `observation` | J3-e | renvois vérifiés par #134 |
| #120 | `Cadre` à n_a ≠ 12 | J3-e (P82) | option (a) |
| #122 | IN^vol = 0 ⇒ IN = 0 à l'état chargé | J3-e (P84) | inchangé |
| #125 | Facteur de croissance par pas | point 2 : J3-f ; points 3 à 6 : J3-e (P84) | point 1 réalisé en J3-c (P88) ; recoupe #144 point 3 (`g`) |
| #131 | BC2 en log, terme de Jensen de r̂\* | J3-e, mesure à #114 (P101) | P117 |
| #135 | `tab:phases` et levier de taux au J4 | J4 | recoupe #54, #56 |
| #137, #142, #144 | Refus génériques sans étape ; localité de la lecture nette ; travail redondant du chemin chaud | **forme du code**, rangs 0 à 9 faits, fusion en attente (§ 1) | trajectoires identiques au bit (P197) ; P57 publiée sans verdict |
| #139 | Critère « Endettement, dépôts » de la fiche 6 | voie (ii) décidée (P149) ; exécution en J3-e | échec attendu strict ; socle complet disponible depuis J3-d2 |
| #140 | Bornes (c) de la fiche 6 | voie (i) décidée (P150) ; exécution en J3-e | test du refus de la moitié du crédit (C31) |
| #141 | Restitution du refus de crédit | J4 (P152) | avec #70 |
| #143 | S6 : ti = 0 au-delà d'une frontière | hors branche ; instruction par `monnaie` et `macro` avant la calibration (P148) | M28 non rouverte ; question à `monnaie` sur la caisse des entreprises sans réponse |
| #145 | Condition du coefficient de richesse sur π\* de la table | J4, avec le levier de cible (#54) (P152) | acceptable en J3 (`macro`) |
| #147 | C62 en régime linéaire (critère d'homogénéité) | J3-f, S1 (Q7) | P167 ; reçoit l'harmonisation « 63 tours (maquette 63,2) » (Q7) |
| #148 | B_Bk, B_CB ≥ 0 sans contrôle sous rachat net | J4, instruction de `monnaie` avant (Q7) | inactif au socle (Em > 0) ; atteignable par les leviers du J4 |
| #149 | « Proposée » périmée au glossaire et à `tab:leviers-cadre` | forme du code, `2f9d378` (P174), fusion en attente | documentation seule |
| #150 | Forme du code du bloc 9 (E7 doublé, lecture de position, E5 par total de ligne, docstrings) | **forme du code**, fusion en attente | point 3 (E5 par colonne) détaché dans #152, J5 (P172) |

**Points ouverts sans issue** : mutant équivalent B_Bk/Res dans B5, à rouvrir avec le corridor (J6, P116) ; résolution de l'état initial par `scenarios/` sans dupliquer le script (J3-e, § 2) ; reconsolidation de l'ADR 0013 (P176 : ADR 0014, rang 9) ; découpage de J3-e à J3-g (P61, P177) ; réserves mineures de J3-d2 non corrigées : lectures de `TABLEAU_DES_PHASES` non reliées au `.tex` (seules les écritures le sont), contrôle de priorité du critère 12 doublé par le noyau pour les erreurs qui créent un découvert, coût du socle complet publié sans verdict jusqu'à G1 (J3-g). Levés au rang 9 : fiche 8, l. ~1497 et ~1524 (`2f9d378`, P174) ; issues de `coder` et de `macro` créées (#153, #154, P178).

**Réserves de la revue finale de la branche « forme du code » (rang 8), issues proposées, non créées** (rattachement proposé, à décider) : (1) tests textuels de `src/` : m1, R2 et R1 (garde de session des invariants) → correctif rapide (`tests:` seul, résultats identiques) ou J3-e, après la décision du mainteneur sur m1 ; (2) domaine de μ̃ dans T3 (`travail.py:73` et `:90`) → J3-e (domaines et état initial résolu) ; (3) f(π\*_t) calculé deux fois par pas (`ouverture.py:123`) → J3-g (budget, G1) ; (4) contrôles d'identité refaits par `etat_de_cloture` (`schema.py:405`) → J3-g ; (5) i_L·L/n_a et δK/n_a recalculés en phase 6 dans trois blocs → J3-g, recoupe #144 point 2 (conversion unique). Texte des issues : compte rendu d'`architect` du rang 9 (PR #151).

**Dépendances** (16/11/2026, après la PR #146). **Ajoutées** (proposées) : annotation de l'ADR 0013 (rang 1b) → #144 et #150 ; #142 et #150 → #144 points 2 et 3 (mêmes fichiers) ; branche « forme du code » → reconsolidation de l'ADR 0013 (Q5) ; #148 → leviers du J4 qui rendent un rachat net atteignable ; E5 par colonne (point 3 de #150) → J5 (lignes à plusieurs termes). **Rattachements proposés** (Q7) : #147 à J3-f (S1), avec l'harmonisation « 63 tours ». **Retirées** (levées par la fusion de la PR #146) : #133 → #132 ; #132 → #106 ; engagements de J3-d1 → #132 ; #132 (localité du bloc 9) → #142 ; J3-d2 → forme du code ; socle complet → #139. **Inchangées** : #143 → domaine du levier de taux (J4) et #55 ; avis de `monnaie` sur la caisse des entreprises → #143 ; #145 → #54 ; #141 → J4 (avec #70) ; #131 → #114 ; branche de calibration → J3-e ; #116 → #111 ; #89 → #88.

### 4. Décisions du mainteneur (extrait : P182 à P199, points ouverts du rang 9 de la branche « forme du code »)

#### Décisions P172 et suivantes (branche « forme du code »), 16/11/2026

P172 à P181 (rang 0) et les questions Q1 à Q8 qui les fondent : historique, partie F, complément du rang 9 de la branche « forme du code » (sortis le 16/11/2026, texte inchangé), en vigueur. Q-1b-1 et Q-1b-2 : ADR 0013, annotation du 16/11/2026. P197 à P199 : choix de la session sous la délégation P175, consignés au rang 9.

| N° | Date | Décision | Question |
|---|---|---|---|
| P182 | 16/11/2026 | Empreinte `d9931c92…f654` de J3-d2 non reproductible (méthode d'`audit` jamais versée ; code identique à `59e1c1b`) : nouvelle référence, mesurée par le script de P173 à encodage documenté sur `git archive 59e1c1b` et à la tête ; le lien avec l'ancienne empreinte est abandonné. | rang 1a |
| P183 | 16/11/2026 | Banc d'empreintes : socle complet et cinq bancs nommés (P87 ; J3-d1 X4 seule, X4 + X3, sans X4, essai pur), aux trois π\*, soit 18 empreintes (la passation de #146 en annonçait 18 pour 15 nommées). | rang 1a |
| P184 | 16/11/2026 | Banc d'empreintes complété de deux bancs choqués choisis par `macro` : D (dépense au-delà de la marge, plafond de E1, Π^CB < 0) et BF (placement raté puis transferts sur le sentier θ_CB = 0,5, plafond de E6, terme 11c), après le constat majeur d'`audit` (plafond de E6 jamais liant sans choc). | rang 1a |
| P185 | 16/11/2026 | Rang 1a commité « conforme avec réserves » après la reprise unique ; mineurs restants d'`audit` (m-a héritage accepté trop largement, m-b docstring de BF, m-c code de sortie) corrigés au rang 2 avec #144 point 1. | rang 1a |
| P186 | 16/11/2026 | m-c : un écart des seules grandeurs d'ouverture (retrait de `g`, #144 point 3) sort en code 3, « trajectoires identiques, grandeurs d'ouverture différentes » ; critère tenu, écart déclaré dans le commit. | rang 1a |
| P187 | 16/11/2026 | Rang 4 (#150 point 1) : si E7 devient une variable du pas, le critère est jugé sur `etats` et `montants` égaux au bit et sur les variables préexistantes ; la variable ajoutée est déclarée ; référence non régénérée. | rang 1a |
| P188 | 16/11/2026 | Q-1b-1 : réouverture de a100.4 pour les seules lectures de position : `LectureDuGrandLivre.position` refuse à l'exécution un poste non déclaré (`RefusDuMoteur`, pas, étape, bloc, poste) ; liste fermée (banque 8c `Res` ; finances publiques 8b `M_G`) tenue par un test (#150 point 2). | rang 1b |
| P189 | 16/11/2026 | Q-1b-2 : le code 3 du banc d'empreintes (P186) couvre l'ajout comme le retrait de grandeurs d'ouverture (`facteur_g_pr`, `facteur_g_N`, `delta_pas` ; `g`), écart déclaré dans le commit. | rang 1b |
| P190 | 16/11/2026 | Rangs 2 à 5 conduits à la main par la session (`coder` → `audit` léger, une reprise au plus, commit après verdict), sans le workflow `circuit-technique`. | rang 1b |
| P191 | 16/11/2026 | Bloc 7 (`banque.py`, `phase_6`) : lecture nette de D_H et D_F encore en phase, même écart que #142 ; issue à part, #156, hors de la branche. | rang 3 |
| P192 | 16/11/2026 | Double contrôle de domaine à la reprise (`sauvegarde.py`), hors chemin chaud : laissé, sans issue. | rang 3 |
| P193 | 16/11/2026 | `eval`, `exec`, `compile` et `__import__` interdits dans `src/` par un test, au rang 4 (réserve mineure de l'audit du rang 3). | rang 3 |
| P194 | 16/11/2026 | P188 limitée aux lectures de position : `valeur_nette_stock` et `valeur_nette_flux` restent non filtrées, comme documenté ; `docwriter` le dit au rang 7. | rang 4 |
| P195 | 16/11/2026 | Docstrings périmées de `parametres/banque.py` et `parametres/banque_centrale.py` (« au passage de `docwriter` », au futur, labels déjà posés) corrigées dans la branche, commit `code:` à part rattaché à #150 (docstrings). | rang 4 |
| P196 | 16/11/2026 | Test d'exécution de texte (P193) : trous relevés par l'audit du rang 4 comblés au rang 5 (`__globals__`, `f_globals`, `f_builtins`, `f_locals`, `sys` sous alias, `from sys import modules`) ; runpy, pickle, code et breakpoint hors de P193. | rang 4 |
| P197 | 16/11/2026 | Session, sous P175 : option `--exclure-variables` du banc d'empreintes (`74e215d`, `60e82da` ; exclusions symétriques après le majeur M1 d'`audit`, reprise unique) au lieu d'une régénération de la référence ; critère « Branche » lu avec `--exclure-variables iB_BH iB_BBk iB_BCB` (§ 1) ; référence `59e1c1b` inchangée. | rang 6 |
| P198 | 16/11/2026 | Session, sous P175 : constat C5 de `macro` écarté (`docs/specification/CONVENTIONS.md` § 4.4 : un décompte ne s'écrit pas en toutes lettres dans la prose). | rang 7 |
| P199 | 16/11/2026 | Session, sous P175 : transcription de la spécification l. ~3026 et ~3468 (C59 des blocs 8 et 9, corrections prospectives P156, P160) incluse dans le commit de #149 (`2f9d378`), pour éviter une divergence fiche 8 ↔ spécification. | rang 7 |

**Points ouverts au 16/11/2026, rang 9 de la branche « forme du code »** (décision du mainteneur) :
- **m1** : élargir P196 aux formes relevées en revue finale (§ 3, issue proposée 1) ou les inscrire hors de P193 ;
- **marge du noyau seul** sur l'exécuteur lent : 0,4995 ms par pas au run 43942786775 (seuil 0,5, à moteur identique) ; attribution par #110 (J3-g) ;
- suppression de la branche distante `ccr-063dc6fc-vo9lzk` (refusée à la session par le contrôle de permissions) ;
- sortie du brouillon de la PR #151 et fusion par commit de fusion, puis vérification de la fermeture de #137, #142, #144, #150, #149 ; ligne du § 7 préparée au § 1 ;
- création des issues proposées du § 3 (réserves de la revue finale) ;
- déjà ouverts : plancher du taux directeur (P181, `monnaie` avant le J4), durée d'une partie (#155), #11, #14 ; instruction de #143 (P148).

### 7. Branches fusionnées (extrait : ligne de J3-d2)

| Branche | PR | Jalon | Fusion | Détail |
|---|---|---|---|---|
| `claude/j3-finances-publiques` | #146 | J3 (J3-d2) | 16/11/2026, 11:59 UTC, commit de fusion `2744be3` (parents `30078bb`, `59e1c1b`), par le mainteneur | Issues fermées par `Closes` : #133, #132, #106, #101, #134 (fermetures vérifiées par la session le 16/11/2026). 23 commits hors fusion (4 `code:`, 4 `tests:`, 15 `docs:` ; `git rev-list --no-merges 30078bb..59e1c1b`). CI de `59e1c1b` (run 43758540925) : quatre jobs en succès. Rangs et SHA : historique, partie F, § 1, et corps de la PR #146. Décisions : P147 à P171. Fable : 0 sur 3. Premiers résultats du moteur pour le bloc 9 et première exécution du socle complet (blocs 2 à 9 réels), aucun résultat final ; `tests/references/` intact. Concordance : 90 labels. Issues nées de la branche : #147 à #150. |

### Complément sorti le 16/11/2026 au rang 1 de la branche « calibration » (`claude/j3-calibration`, tête `ca0ba93`, PR #162)

Sortis de `docs/feuille-de-route.md` pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé (aucun titre déplacé). Les numéros P-n restent stables ; P200 à P203 et P213 à P224 restent en vigueur. Les renvois « § n », « ci-dessous » et « ci-dessus » de ces lignes se lisent dans la tête (`docs/feuille-de-route.md`) au même §, sauf ceux de l'en-tête et des jalons, qui renvoient eux-mêmes à l'historique.

#### En-tête (extrait : présentation des parties A à G et mise à jour de la tête du 16/11/2026, décisions P204 à P224)

Tenue par `architect`, après chaque série de PR fusionnées. Chaque mise à jour est datée et cite le SHA de `main` et de la branche de travail. **Tête condensée** (#119, P76) : périmètre courant, jalons, décisions en vigueur et points ouverts ; l'historique (fiches des branches fusionnées, relevés d'issues antérieurs, décisions sans numéro M, points P1 à P73 et D1 à D13, détail des branches fusionnées jusqu'à J3-a) est dans `docs/feuille-de-route-historique.md`, sans rien supprimé ni réécrit ; partie B (14/11/2026, rang 9 de J3-c) : P74 à P86, pistes du § 5, branches fusionnées jusqu'à J3-a. Partie C (14/11/2026, après la fusion de la PR #129) : fiche de J3-c, relevé d'issues du 14/11/2026 après la PR #117, P87 à P99, points ouverts du rang 9. Partie D (15/11/2026, rang 8 de J3-d1) : mises à jour de la tête du 13/11 au 14/11/2026 (rang 9 de J3-c), plan de J3-d1 (rangs 0 à 8), P100 à P118, points ouverts au 14/11/2026 après la PR #129, lignes du § 7 de la PR #118 à la PR #128. Partie E (15/11/2026, point d'étape après la fusion de la PR #136) : mises à jour de la tête du 14/11/2026 après la PR #129 et du 15/11/2026 (rangs 4 et 5 de J3-d1), fiche de J3-d1, relevé d'issues du 14/11/2026 après la PR #129, P119 à P146, points ouverts du rang 8 de J3-d1. Un renvoi daté d'avant le 14/11/2026 vers « la feuille de route, § n » se lit dans l'historique, partie A, au même §. Partie E complétée au rang 1a de J3-d2 (`142b556`) : en-têtes, classement proposé du § 9.6, Q1 à Q10, introduction des M-n, lignes des § 2 et § 8 ; puis au rang 8 de J3-d2 (`f1c8f2f`) : en-têtes, lignes des § 1 à 3, P147 à P155, ligne de J3-c au § 7. Partie F (16/11/2026, point d'étape après la fusion de la PR #146) : mise à jour de la tête du rang 8 de J3-d2, fiche de J3-d2, relevé d'issues du 15/11/2026 après la PR #136, points ouverts du rang 8 de J3-d2, ligne de J3-d1 au § 7 ; complément du 16/11/2026 au rang 1b de la branche « forme du code » : P156 à P171 ; complément du rang 9 : P172 à P181, Q1 à Q8 et points ouverts du rang 0. Partie G (16/11/2026, point d'étape après la fusion de la PR #151) : mise à jour de la tête du rang 9 de la branche « forme du code », fiche de cette branche, relevé d'issues du 16/11/2026 après la PR #146 (réserves de la revue finale, dépendances), P182 à P199, points ouverts du rang 9, ligne de J3-d2 au § 7.

**Dernière mise à jour** : 16/11/2026, décisions du mainteneur sur le plan de la branche « calibration » (`architect`) — `main` = `890471b` ; branche de travail `claude/j3-calibration` à `afa9e89`, PR brouillon #162 ; plan **décidé** (§ 1), rang 1 en cours (sections #92, #143 et #55 de `docs/blocs/calibration.md`), découpage de J3-e à J3-g décidé (§ 2), décisions P200 à P224 (§ 4 ; P182 à P199 : historique, partie G). Mises à jour antérieures : historique, parties G, F, E, puis `git log -- docs/feuille-de-route.md`.

#### 3. Issues hors plan (extrait : erratum du 16/11/2026)

**Erratum** (16/11/2026, `architect`) : le message du commit `afa9e89` donne « 55 840 octets environ » pour la feuille de route ; mesure après ce commit, `git show afa9e89:docs/feuille-de-route.md | wc -c` : **55 821 octets**. Le message reste tel quel (historique non réécrit).

#### 4. Décisions du mainteneur (extrait : renvois aux parties B à F ; P200 à P203 ; P213 à P224, rang 1 de la branche « calibration »)

**Décisions du mainteneur du 14/11/2026 sur le point d'étape après la PR #117 (P74 à P86)** : historique, partie B, § 4 (sorties de la tête le 14/11/2026, texte inchangé), en vigueur ; la branche cite P74 (périmètre), P75, P76 (plafonds de 60 et 40 ko), P80, P81, P85 et P86.

**Décisions du mainteneur du 14/11/2026 sur le rang 1a de J3-c, l'avis de `jeu` sur #80 et l'ADR 0013 (P87 à P99)** : historique, partie C, § 4 (sorties de la tête le 14/11/2026 après la fusion de la PR #129, texte inchangé), en vigueur ; forme : ADR 0013, annotation du 14/11/2026.

**Décisions du mainteneur du 14/11/2026 après P99 (P100 à P110) et au point d'étape après la PR #129 (P111 à P118)** : historique, partie D, § 4 (sorties de la tête le 15/11/2026, rang 8 de J3-d1, texte inchangé), en vigueur ; la branche cite P111 à P118.

**Décisions du mainteneur du 14/11/2026 au rang 1a de J3-d1 (P119 à P141) et du 15/11/2026 (P142 à P146)** : historique, partie E, § 4 (sorties de la tête le 15/11/2026, point d'étape après la fusion de la PR #136, texte inchangé), en vigueur ; le plan de J3-d2 cite P121, P122, P124, P125, P127, P129, P133 à P138, P140, P141 et P145.

**Décisions du mainteneur du 15/11/2026, rangs 1a à 7 de J3-d2 (P156 à P171), et erratum de P165** : historique, partie F, complément du 16/11/2026 (sorties de la tête au rang 1b de la branche « forme du code », texte inchangé), en vigueur.

| N° | Date | Décision | Question |
|---|---|---|---|
| P200 | 16/11/2026 | Ouverture de la branche « calibration » (ligne 11 du § 2) sous le nom `claude/j3-calibration`, créée depuis `main` à `890471b`, avec en rang 0 le point d'étape qui suit la fusion de la PR #151 (P177). | point d'étape |
| P201 | 16/11/2026 | Création des cinq issues proposées au rang 9 de la branche « forme du code » (réserves de la revue finale ; historique, partie G, § 3) : #157 à #161 (§ 3). | rang 9 |
| P202 | 16/11/2026 | m1 : P196 élargie. Le test d'exécution de texte (`tests/unitaires/test_etat.py`) détecte aussi `from sys import *`, un alias de `sys` lié par affectation, `os.__dict__['__builtins__']`, `sys.__dict__` et `os.sys.modules` ; porté par #157, avec R1 et R2 (rattachement : Q9). | m1 |
| P203 | 16/11/2026 | Statut `accepted` de l'ADR 0014 confirmé (posé au rang 9 sur le précédent de P76 (b)) ; ADR inchangé. | rang 9 |

| N° | Date | Décision | Question |
|---|---|---|---|
| P213 | 16/11/2026 | #92 : définition de la part salariale de la BCE (*Economic Bulletin* 4/2023, zone euro, 1998–2023, 62,4 %, valeur ajoutée brute au prix de base), écart au coût des facteurs déclaré contesté ; **μ̄ = 0,60** retenu comme valeur proposée de la table soumise à M34 (part 0,624645 à π̄ = 2 %) ; relecture prospective d'AMECO ALCD2 (`ec.europa.eu`, `db.nomics.world` ouverts à l'environnement le même jour). | `docs/blocs/calibration.md` § 1 |
| P214 | 16/11/2026 | Dividendes à 22,3 % du PIB à μ̄ = 0,60 (δ = 5 % sans source) : limite déclarée, sans arrêt de la branche ; issue #164 (δ, consommation de capital fixe), hors branche. | `docs/blocs/calibration.md` § 1 |
| P215 | 16/11/2026 | #143 : voie (1) + (1′) + (5), sans rouvrir M28 : borne du levier au J4 (P148) ; domaine de validité de S-ζ en ζΔϱ (frontière de S6 à ζΔϱ = 13,231, indépendante de μ̄, π̄ et #130), refus typé en J3-e2 ; mécanisme de crise au J6 (#57). | `docs/blocs/calibration.md` § 2 |
| P216 | 16/11/2026 | Refus de la caisse des entreprises (intérêts au-delà de D_F) voulu au socle, sans découvert automatique ; refus typé en J3-e2 ; défaut des entreprises au J6 (#57). | `docs/blocs/calibration.md` § 2 |
| P217 | 16/11/2026 | Arrêts sous écart durable du taux (sonde de `monnaie`) consignés en commentaire sur #143, sans issue nouvelle ; `fred.stlouisfed.org` à ouvrir au J4 seulement. | #143 |
| P218 | 16/11/2026 | #55 : ζ = 8 proposé pour M34 (σ ≈ 0,64, contesté) ; κ et l'état stationnaire inchangés par ζ. | calibration.md § 3 |
| P219 | 16/11/2026 | C62 sous φ = 0 remesuré avant M34 (maquette–moteur, ζ_c, couverture, racines), puis reformulé : « explosif à 10 % ; quasi neutre à 2 %, signe dépendant de ζ ». | calibration.md § 3.13 |
| P220 | 16/11/2026 | κ inchangé, écart de B12 à Eurostat déclaré ; κ et δ calés ensemble dans #164. | #164 |
| P221 | 16/11/2026 | Indicateur d'investissement au tour : #165, J4. | #165 |
| P222 | 16/11/2026 | C62 : formulation du § 3.13.7 de la fiche de calibration adoptée pour M34, sous relecture de `monnaie`. | calibration.md § 3.13 |
| P223 | 16/11/2026 | #166 (estimateur de C62) ajoutée au périmètre, traitée avec le commit de #55 au rang 3 ; méthode déléguée (P211). | PR #162 |
| P224 | 16/11/2026 | ζ_c remesuré au rang 8 sur la table calibrée, puis dans #163 et #164. | calibration.md § 3.13.8 |

#### 6. Jalons (extrait : lignes de J0, J1 et J2, jalons passés)

| Jalon | Contenu | Critère de passage | État |
|---|---|---|---|
| **J0 Fondations** (#2 à #6, PR #7) | Cadre du projet, ADR 0001 à 0004, feuille de route, `archive/`, gabarits et conventions, squelette Python, CI | CI verte (tests, concordance, compilation XeLaTeX) ; plus aucun « À ADAPTER » ; PR #7 fusionnée par commit de fusion. | **Passé le 30/09/2026** : PR #7, commit de fusion `facf97f` (historique, partie A, § 6). |
| **J1 Spécification du socle** | Gabarit de fiche éprouvé sur la première fiche et validé à l'usage (M20), fiche « temps et comptabilité », puis environ huit fiches (production et stocks ; travail et salaires ; prix ; ménages ; investissement et financement ; banque commerciale ; banque centrale et anticipations ; État et dette) → décisions M-n → spécification v3.0 « socle », sections marquées « proposées » jusqu'au code | Les neuf fiches tranchées, chacune avec sa décision M-n reportée ici ; chaque équation porte statut, provenance et M-n (contrôle par la concordance `--strict`) ; matrices des bilans et des flux écrites en tableaux, lignes et colonnes de somme nulle vérifiées par un script d'`outils/` ; état stationnaire calculé sous forme fermée par un script d'`outils/`, sans simulation, avec ses ratios publiés (K/Y, part salariale, taux réel, inflation, dette/PIB ; unité et dénominateur) ; revue de fond de `macro` et `monnaie`, avis de `jeu` sur les leviers prévus, validation du mainteneur. | **Passé le 07/10/2026** : PR #85, commit de fusion `833afd9` ; réserves déclarées #80 (superneutralité, échec attendu) et #93 (fermée par la PR #99). Historique de l'état : partie A, § 6. |
| **J2 Noyau** | Comptes, ordonnanceur, état et sauvegarde, observation ; tests d'invariants | Conservation exacte des identités comptables (ε = 1e−12 × échelle du bilan, par pas et en cumul sur 720 pas, M22) ; reprise de sauvegarde identique, y compris à la frontière de tour ; invariance d'unité (×100) ; coût du noyau seul mesuré et publié, seuil écrit avant l'essai : ≤ 0,5 ms par pas mensuel (fiche 1, § 5, réserve 3 ; le budget de calcul sur le socle complet est un critère de J3, M19). Fiche « temps et comptabilité » tranchée le 30/09/2026 (M22, ADR 0005) : le jalon peut démarrer. | **Passé le 15/10/2026** : PR #99, commit de fusion `2e643a2` ; identités ≤ 4,313e−16 × S, ×100, reprise au bit, C = 0,4267 ms (seuil 0,5 ms) ; concordance 18/18 (partie A, § 6). |

### Complément sorti le 17/11/2026 au rang 11 de la branche « calibration » (`claude/j3-calibration`, tête `6f419bf`, PR #162)

Sortis de `docs/feuille-de-route.md` pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé (titres décalés d'un niveau). Les numéros P-n restent stables ; P204 à P212 et P225 à P241 restent en vigueur. Les renvois « § n », « ci-dessous » et « ci-dessus » de ces lignes se lisent dans la tête à `6f419bf`.

#### En-tête (extrait : mise à jour de la tête du 17/11/2026, rang 8 de la branche « calibration »)

**Dernière mise à jour** : 17/11/2026, rang 8 de la branche « calibration » (M34, § 4) — `main` = `890471b` ; branche de travail `claude/j3-calibration` à `a5beb24`, PR brouillon #162 ; plan **décidé** (§ 1), rangs 0 à 8 faits, rang 9 ouvert, découpage de J3-e à J3-g décidé (§ 2), décisions P204 à P212 et P225 à P241 (§ 4 ; P213 à P224 : index). Mises à jour antérieures et extraits sortis : historique, partie G et ses compléments, puis `git log -- docs/feuille-de-route.md`.

#### 1. Branche de travail en cours (extrait : mesures du rang 8 de la branche « calibration »)

**Mesures du rang 8 (17/11/2026)** :
- **Coût (P57, après)** : plateforme de référence (ubuntu26 20261111.196.1, Python 3.12.14), run 44073211655 (`a5beb24`) : noyau seul 0,4458 ms par pas ; socle complet 0,5204 ms par pas (0,1201 ms par pays-semaine) ; plus forte part : finances publiques, 0,0472 ms. Seuils tenus (part ≤ 0,48 ; noyau ≤ 0,5). Publication sans verdict.
- **Canal rentier ↔ rayon** (M34, § 7.16 (c), `macro`) : co-variation vérifiée sur T0, T1 et trois π̄ ; l'instabilité sous φ = 0 exige la règle de taux et le canal rentier ; à canal effectif égal, T1 est un peu plus stable que T0. Coupe « intérêts sur titres dans Div_Bk » non mesurée.
- **Pour `docwriter`** : contre-épreuve B-1/B-2 « sous les entrées d'origine, B-1 et B-2 ne diffèrent que par v_H et m » ; bord τ_H = 0 « bord fermé de l'état ; mesure (α) de #80 refusée à T1 » ; D3 nommé « coût en chômage d'un choc d'anticipations », jamais « ratio de sacrifice » ; réserves de source de `monnaie` (séries du taux au jour le jour pour ϖ_L ; ϖ_D « choix déclaré dans la plage » ; dénominateur de ϑ).

#### 4. Décisions du mainteneur (extrait : P204 à P212, plan de la branche « calibration » ; P225 à P241, rangs 1 à 8)

| N° | Date | Décision | Question |
|---|---|---|---|
| P204 | 16/11/2026 | #45 réduite à λ_w, avec `Closes` (PR #162). La calibration C7 de la fiche 8 (a_π, a_I — k_I de la fiche — et λ_e sur un ratio de sacrifice sourcé ; critère 23) va dans une issue nouvelle, #163, rattachée à J3-f1 : texte rédigé par `architect`, création par la session. | Q1 (a) |
| P205 | 16/11/2026 | Trace de l'instruction : fiche transverse `docs/blocs/calibration.md`, une section par issue, sur le modèle du gabarit, écrite au rang 1 par les experts pilotes ; inscrite à l'inventaire (`docs/blocs/README.md` § 1). | Q2 (a) |
| P206 | 16/11/2026 | Une décision, **M34** (numéro réservé, prise au rang 2), sur la table calibrée entière, avec visa du tableau avant / après prédit. Ce visa couvre chaque commit des rangs 3 à 7 dont le tableau mesuré égale le prédit à 1e−9 relatif près ; tout autre écart arrête. | Q3 (a) |
| P207 | 16/11/2026 | #143 (P148) instruite par `monnaie` et `macro` au rang 1, avant la section de #55, sans `Closes` ; voie à trancher au plus tard au J4. | Q4 (a) |
| P208 | 16/11/2026 | Source « non trouvée » : valeur gardée, déclarée « choix de conception, source non trouvée » avec son motif ; issue fermée sur ce constat visé (notamment r̄, contesté, et richesse liquide de #62). | Q5 (a) |
| P209 | 16/11/2026 | `tab:criteres-j3` : la colonne « valeur résolue » suit l'état calibré ; demi-largeurs et définitions inchangées ; anciennes valeurs barrées. Prospectif : aucun test zéro n'a été exécuté. | Q6 (a) |
| P210 | 16/11/2026 | Une référence d'empreintes par commit de calibration (`outils/empreintes_des_bancs_<sha>.json`), écrite par la session après visa ; en fin de branche ne restent que `59e1c1b` et la dernière. | Q7 (a) |
| P211 | 16/11/2026 | Délégation P175 reconduite pour les choix de forme ; valeurs, résultats finaux et critères réservés au mainteneur. | Q8 (a) |
| P212 | 16/11/2026 | Découpage de J3-e à J3-g en sept branches (lignes 12 à 18 du § 2, indicatives jusqu'au point d'étape qui précède chacune) ; #157 en correctif rapide (`tests:` seul, résultats identiques, aucune documentation de fond ; sinon J3-e2) ; #158 en J3-e2 ; #159 à #161 et #156 en J3-g1. | Q9 |

| N° | Date | Décision | Où elle est consignée |
|---|---|---|---|
| P225 | 16/11/2026 | #130 : ϑ = 0,15 proposé pour M34 (CET1 du MSU, 14,75 % ; dénominateur contesté) ; dette consolidée de référence +12 %. | calibration.md § 4 |
| P226 | 16/11/2026 | #130 : ϖ_L = 0,02, ϖ_D = 0,01, r̄ = 0,01 (contesté) inchangés et sourcés ; zone euro de référence. | calibration.md § 4 |
| P227 | 16/11/2026 | Bêta des dépôts (limite de B2) : #167, hors branche. | #167 |
| P228 | 16/11/2026 | Délégation pour #62 et #45, le mainteneur étant injoignable jusqu'à la session suivante : la valeur recommandée par l'expert pilote est retenue comme proposée pour M34 si elle repose sur une source lue, tient les critères du plan, ne rencontre aucune condition d'arrêt et ne reçoit aucune objection de `jeu` ni de `monnaie` ; sinon, question ouverte. M34 reste réservée. | calibration.md § 5, § 6 |
| P229 | 16/11/2026 | Issues nouvelles proposées par les experts pendant cette absence : rédigées dans le handoff, créées seulement sur accord. | PR #162 |
| P230 | 16/11/2026 | Un changement de signe du module de C62 à 2 % dû à #62 ou #45 est publié et couvert par la formulation de P222, sans arrêt. | calibration.md § 3.13 |
| P231 | 16/11/2026 | Rang 1 terminé : dossier M34 (table entière, tableau prédit consolidé) préparé dans la fiche, sans code, puis handoff. Toute question bloquante : arrêt, travail enregistré, handoff. | calibration.md |
| P232 | 16/11/2026 | Session, sous P228 (aucune objection de `jeu` ni de `monnaie`) : #45, λ_w = 0,18 proposé pour M34, β = 2 ; formulation de C62 à la table proposée remplaçant celle de P222 (P230). Réservés à M34 : ordre entre λ_w et #163 (condition proposée : #163 avant la démonstration J4). Issue sur l'instabilité 17 rédigée, non créée (P229). | calibration.md § 6.13 |
| P233 | 16/11/2026 | Session, sous P228 (aucune objection de `jeu` ni de `monnaie`) : #62, ν_H = 1,1 et λ_H = 0,4 proposés pour M34 ; dette de référence publiée sans cible ; correction du test du continuum avec le commit de #62. Rang 1 instruit. | calibration.md § 5.12 |
| P234 | 17/11/2026 | Rang 5 (#130) : la frontière du régime de hausse de la maquette conjointe est cherchée sur [1 ; 3] (`BORNES_MARGE_HAUSSE`) au lieu d'être publiée « sans objet » ; écart au critère « Diff » accepté. | constat A1 de l'audit ; commit `3c8156e` |
| P235 | 17/11/2026 | Rang 6 (#62) : dans `test_spectre_restreint_retire_les_racines_des_identites`, l'amas des racines nulles est apparié par multiplicité (`SEUIL_AMAS_NUL` = 1e−5), la tolérance 1e−7 gardée pour les autres racines. | commit `399323c` |
| P236 | 17/11/2026 | Rang 7 (#45) : correction **prospective** de l'horizon des critères « une vitesse ne détermine pas l'état d'arrivée » (fiche 3, crit. 4 : 720 → 2 880 pas ; fiche 6, crit. 6 : 2 160 → 6 480 pas ; seuil 1e−6 inchangé) ; ancien verdict publié : échec à l'ancien horizon (2,98e−6 sur ω ; 4,1e−6 sur K/Y), transitoire de la branche lente λ_w × 0,5, sans continuum d'équilibres. | rang 7 |
| P237 | 17/11/2026 | Rang 7 (#45) : #139 remise en échec attendu (`xfail(strict)`), son passage du rang 6 tenant à la phase d'une oscillation. | #139 |
| P238 | 17/11/2026 | Rang 7 (#45) : `BORNES_MARGE` de la marge conjointe élargie à [1 ; 3] (frontière 2,7826 à λ_w = 0,18) ; les frontières en ν_H et h de l'instabilité 17 restent « sans objet » (M34). | rang 7 |
| P239 | 17/11/2026 | Rang 8 : les variantes de vitesse « toutes÷2 », « toutes×2 », « lambda_w×2 » de la boucle salaires-prix (maquette) prennent λ_w relative à la table (× 0,5 et × 2) ; six rayons changent, aucun résultat final (#45). | rang 8 |
| P240 | 17/11/2026 | Rang 8 : critère « Endettement » de #139 laissé en échec attendu dans la branche ; correction prospective (enveloppe sur [6 480 ; 6 720[) proposée dans l'issue séparée #169. Issue #170 (cas lv* = 0,45 à la table) ; commentaires sur #143 et #163 publiés. | #169, #170 |
| P241 | 17/11/2026 | Rang 8 : lectures confirmées — (1) sous le choc de 1 %, aucune racine du moteur publiée, renvoi à la mesure en régime linéaire (lecture B de la précision de M34) ; (2) l'arrêt de C62 linéaire au pas 1 881 à 10 % (refus de S6 par cumul) n'est pas la condition d'arrêt « frontière de #143 atteinte par un banc ». | rang 8 |

Questions Q1 à Q9 du 16/11/2026, avec leurs options et la recommandation d'`architect-approfondi` : `git show afa9e89:docs/feuille-de-route.md`, § 4. Le mainteneur a retenu l'option recommandée pour chacune (P204 à P212).

## Partie F : extraits de la tête sortis le 16/11/2026 (point d'étape après la fusion de la PR #146, rang 0 de la branche « forme du code »), figés

Sortis de `docs/feuille-de-route.md` à `2744be3` (`main`, commit de fusion de la PR #146), pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé, titres décalés d'un niveau. Les numéros P-n restent stables ; ces décisions restent en vigueur tant qu'aucune décision ultérieure ne les remplace.

### En-tête (extrait : mise à jour de la tête du 15/11/2026, rang 8 de J3-d2)

**Dernière mise à jour** : 15/11/2026, rang 8 de J3-d2 (`architect`) — branche `claude/j3-finances-publiques`, tête `f1c8f2f` (PR #146) ; rangs 0 à 7 faits (§ 1) ; décisions P166 à P171 (§ 4) ; fiche 9 « implémentée », neuf fiches sur neuf (`docs/blocs/README.md`) ; ADR 0013 annoté (rang 8). Mises à jour antérieures : historique, partie E (compléments), puis partie D, puis `git log -- docs/feuille-de-route.md`.

### 1. Branche de travail en cours (extrait : fiche de J3-d2, à la fusion de la PR #146)

**J3-d2** (`claude/j3-finances-publiques`, créée depuis `main` à `30078bb` ; PR brouillon #146) : plan ci-dessous, **décidé** par le mainteneur le 15/11/2026 (P147, P155, § 4). Fiche de J3-d1, figée à la fusion de la PR #136 : historique, partie E, § 1.

#### Plan de J3-d2 « finances publiques » (`claude/j3-finances-publiques`) — collision des identifiants (#133), module du bloc 9 (#132), variation sur le tour (#106), test de source (#101), encadré des vitesses (#134)

*Proposé par `architect-approfondi` le 15/11/2026 (point d'étape après la PR #136) ; décidé par le mainteneur le même jour (P147 à P155, § 4).*

- **Issues avec `Closes`** (P113, inchangé) : #133, #132, #106, #101, #134. Rattachés à #132 sans issue propre : les six engagements reportés par J3-d1 (commentaire du 15/11/2026 sur #132) ; les lignes (c) des fiches 5 et 6 qui portent sur une règle du bloc 9 (P122) ; les lignes renvoyées depuis les fiches 7 et 8 (P90 : placement raté ; couverture et C60 de la ligne « Perte » ; lecture de Π^CB en 8b pour la ligne 16 et en phase 7 pour l'émission) ; le double appel de `besoin_d_emission` (bloc d'essai 9).
- **Hors périmètre**, motifs au § 3 et en Q2 à Q6 : #143 (bloc 6 ; son option (3) rouvre M28) ; #139 et #140 (critères de la fiche 6, décisions réservées, P140, P141) ; #137, #142, #144 (forme du code, sans effet sur les trajectoires).
- **Ordre** : #133 → #132 (P114) ; #106 après #132 (« aucun consommateur » ne se constate qu'une fois les blocs du socle tous écrits, P51) ; #101 indépendante (`outils/`), au rang 2 ; #134 au passage de `docwriter`.
- **Experts** : `macro` pilote (fiche 9) ; `monnaie` consulté sur E9 à E11, M^G, ς_B, Π^CB et le placement raté (frontière dette publique, `docs/blocs/README.md`) ; `jeu` au rang 1a sur la propriété de caisse (critère 11) et φ\* (C62), indicateurs visibles.
- **Délégation** : Q7. **Budget Fable** : 0 sur 3, aucune consultation prévue ; une reconsolidation de l'ADR 0013 (Q8) relèverait du § 4.1 de `docs/agents/routage.md`.

| Rang | Étape | Agent | Circuit |
|---|---|---|---|
| 0 | Point d'étape et plan (présente mise à jour) ; PR brouillon ; amendements de #132 (critères ci-dessous), #133, #106, #101, #134 | `architect-approfondi`, session | `docs:` |
| 1a | **Fait le 15/11/2026** (P156 à P164) — lectures avant le code : classement (a)/(b)/(c) des lignes « J3 » du § 9.6 de la fiche 9 (proposition ci-dessous) ; lignes (c) des fiches 5 et 6 reçues (P122), nommées une à une ; lignes des fiches 7 et 8 (P90) ; horizon H du critère 7 déclaré ; nullités calculées du bloc 9 ; décompte des labels | `macro-approfondi` (pilote) ; `monnaie` (E9 à E11, M^G, ς_B, Π^CB) ; `jeu` (critère 11, C62) | 4 |
| 1b | **Fait le 15/11/2026** (P165) — annotation de l'ADR 0013 : table du bloc 9 ; Y^HS en variable d'état (version du schéma) ; ς_B dans `DOMAINES_DES_ENTREES` (P138) ; liste fermée des lectures brutes (E4, E6, E9, avec E^Bk) ; un seul appel du besoin d'émission par pas ; bloc d'essai 9 gardé sous X1 à X4 (P114, #133) | `architect-approfondi` | § 4.2 |
| 2 | **Fait** (`8352db8`, `a7d45f5`) — #133 : exigences du bloc d'essai renommées X1 à X3 dans `tests/` (spécification au rang 6) ; #101 : liste étendue du test de source | `coder` → `audit` ; `macro`, `monnaie` (#101) | 3 |
| 3 | **Fait** (`4759e64`, `fc7a3e2`, labels `a059d10`) — #132 : `finances_publiques.py`, E1 à E13 ; engagements 1 à 6 ; bloc d'essai 9 retiré du banc du socle complet, gardé pour le banc de P87 | `coder` → `audit` ; `macro`, `monnaie` | 1 |
| 4 | **Fait** (`380a325` ; retrait, P51 ; 90 labels) — #106 : `variation_sur_le_tour` retirée de `LECTURES_DU_REGISTRE` faute de consommateur déclaré, ou label et balise avec son consommateur ; `pas_du_tour` et `tour_du_pas` examinées | `coder` → `audit` | 3 |
| 5 | **Fait** (ci-dessous) — mesures : stationnarité du socle complet, verdicts des lignes (a) et (b), nullités, parts P57 sur la plateforme de référence | session ; `macro` | — |
| 6 | **Fait** (`22c8bd2` #133, `b09b008` #132, `b5ea86b` #106, `a0dff49` #101, `a5d5274` #134 ; `7d34b9b`, `664c66d`) — passage unique de `docwriter`, un commit `docs:` par issue (#133 avant #132, puis #106 s'il pose un label, #134) ; labels et balises poussés ensemble (P62) | `docwriter` ; `macro` valide, `monnaie` pour E9 à E11 | règle 9 |
| 7 | **Fait** (conforme avec réserves ; `6b959f7`, `df4e3b9`, `f1c8f2f`, audit léger conforme) — revue finale complète, `/code-review` | `audit`, `macro-approfondi` | règle 10 |
| 8 | **Consignation faite** par le présent commit (fiche 9 « implémentée » : neuf fiches sur neuf) ; **restent** la validation et la fusion par le mainteneur | `architect`, mainteneur | — |

**Mesures du rang 5** (`macro`, 15/11/2026) : critères (a) conformes ; lignes (b) C51, C52, C62 publiées ; parts P57 sur la plateforme de référence (run CI 43744967905, `a059d10`), en ms par pas : noyau seul 0,4877 (seuil 0,5), socle complet 0,5633 (0,1300 ms par pays-semaine, publié sans verdict jusqu'à G1, J3-g), bloc 9 0,0503 ; toutes les parts sous l'alerte de 0,276. **Réserves mineures non corrigées** (rang 7) : lectures de `TABLEAU_DES_PHASES` non reliées au `.tex` (seules les écritures le sont) ; contrôle de priorité du critère 12 doublé par le noyau pour les erreurs qui créent un découvert ; E5 lit les totaux de ligne là où F3 lit la colonne (#150, J5).

**Classement des lignes « J3 » du § 9.6 de la fiche 9, arrêté au rang 1a** *(correction du 15/11/2026, avant tout essai, P155, P160 à P162 ; classement proposé au rang 0 : historique, partie E)* ; aucune ligne essayée ; valeurs de référence = celles du script, jamais les chiffres de maquette (« Domar 3,9802 / 3,9671 / 3,9620 % », précédent P77) :
- (a) : état stationnaire (critère 4) ; cas à la main (critère 1, appel direct, θ_CB = 0,5) ; parts non payées (12) ; caisse (11) ; lecture nette (engagement 4) ; neutralité de ν_G et θ_CB (C59), qui juge aussi « Neutralité de s_CB » de la fiche 8 (P160) ; couverture (E4, C45, choc par r̂\*) ; bornes (16, avec les contraintes de rachat) ; phases et empreinte (2, 19) ; coût (20) ;
- (b) : racine (C51) publiée à ζ = 4 indicatif, verdict « à ζ calibré » → calibration (P161) ; θ_H (C52, critère 14, rayon de la boucle de `sec:menages` avec impôts) ; pays joué (C62) ;
- (c) : test zéro (15) → J3-e ; vitesses et arrivée (7) → #114, J3-f ; stabilité (8) → J3-f (S1) ; « −2 points » (#55), calibration (22) → calibration ; critère 13 de la fiche 8 (#80) : échec attendu inchangé, verdict moteur à #114 ; **ligne ajoutée** (P161) : dette/PIB du J1 (critère 5, « égal au moteur à t = 0 à 1e−9 ») → J3-e, tautologique tant que `scenarios/` ne résout pas l'état initial ;
- reçues des fiches 5 et 6 (P122 lue selon P162) : aucune ligne (c) ne porte sur une règle du bloc 9 (toutes restent à #114) ; J3-d2 réaffirme avec le bloc 9 réel les lignes (b) appuyées sur le bloc d'essai 9 — fiche 6 « État stationnaire » (T_{F,t−1}, T^e_F nuls au bit, sur le τ_F de E5 réel) ; fiche 5 « Revenu par le grand livre » (YD = lignes 5, 6, 7, 10, 11a, 14, 15 à 1e−12·S ; B_H, 11a, 19a-ménages nulles au bit) ; « Délais » des fiches 5 et 6 (signe et date par appel direct, E3, E5, E6 → H6, F3) ; marge de `sec:finances_publiques-caisse` publiée sur le socle complet ;
- reçues des fiches 7 et 8 (P90) : « Placement raté » (M^G_clôture = M^G\* − ς_B·(Em − ΔB^prim_CB) à 1e−12·S^G ; Res, L^CB selon B7 sans solde résiduel) ; « Perte » et C60 (P157) ; « Lecture de Π^CB » (X1 : ligne 16 en 8b et E9 en phase 7 lisent le Π^CB de la phase 1, ligne 16 à 1e−12) ; « Neutralité de s_CB » (P160) ; vitesses, test zéro, C43, (d2), (d3) de la fiche 7 restent à #114.

**Critères d'acceptation, écrits avant l'essai** (à préciser au rang 1a, jamais après une mesure ; précisés le 15/11/2026, P156 à P164) :
- **#133** : aucune exigence du bloc d'essai 9 ne porte plus un identifiant E1 à E13, dans `tests/` comme dans la spécification (contrôle par `grep`, commande citée) ; identifiants X1 à X4 (X4 : couverture de P124) ; une mention de la tête dit que les E1 à E3 de P95 se lisent X1 à X3 (la partie C de l'historique est figée) ; trajectoires identiques au bit.
- **#132** :
  - lignes classées (a) à leurs seuils de fiche, lignes (b) publiées ; état stationnaire égal au script à 1e−10 relatif aux trois π\*, sur la grille de n_a du script (n_a = 4 hors domaine, #87) ;
  - engagement 1 : E4 à φ = 1 sur le banc du socle complet, sans couverture d'essai (X4) ;
  - engagement 2 : E1 lit max(0 ; M^G) ; E6, E9 et l'assiette de E4 lisent M^G brut ; liste fermée des lectures brutes (avec E^Bk) contrôlée par un test ;
  - engagement 3 : E5 et E12 en lecture nette (D̃_F, D̃_H) ;
  - engagement 4 : épreuve à −1 ulp et à −0,5 ε S sur E1 (G^plan = +0 sans `PlanHorsDomaine`), E4, E5, E6, E9 (hors placement raté) et E12 ;
  - engagement 5 : ς_B dans `DOMAINES_DES_ENTREES`, refus typé hors de [0 ; 1] en phase 0, sans écrêtage ; colonne « Lisent » de `tab:phases` inchangée pour la phase 0 ;
  - engagement 6 : F3 lit la colonne des entreprises (`montant_execute(ligne, "entreprises_courant")`) ; trajectoires identiques au bit tant que chaque ligne n'a qu'un terme des entreprises ;
  - lignes (c) des fiches 5 et 6 reçues (P122) et lignes des fiches 7 et 8 (P90) à leurs seuils de fiche ;
  - un seul appel du besoin d'émission par pas (test de décompte) ;
  - localité : max(0 ; ·) appliqué dans les fonctions balisées du bloc 9, aucun dans ses méthodes de phase (la règle que #142 rétablit pour les blocs 5 et 6) ;
  - **treize labels** E1 à E13 (fiche 9, § 9.1), une balise chacun ; E13 garde un label malgré ses deux parts.
  - **précisions du rang 1a** *(correction du 15/11/2026, avant tout essai ; P156 à P159, P161, P164)* :
    - état stationnaire (F2) : n_a = 12 sur le moteur aux trois π\*, 1e−10 relatif ; n_a ∈ {4 ; 52} par appel direct des fonctions du bloc 9 sur l'ouverture du script (#87) ; grandeurs Y^HS_t/Y^HS_{t−1} = Γ̄, M^G\* = ν_G·PB, dette consolidée/(n_a PIB), Em ; nullités en absolu ; les tests passent ν_G = 1,15 explicitement (défaut `nu_G = 1.0` du script hors domaine) ;
    - nullités (F3, P121), au bit : T_F, T_{F,t−1}, T^e_F, Tr, ligne 6, B_H, 11a, 19a, ΔB^prim_CB, B_CB, 11c, E^CB, perte non couverte ; Res par test de signe (L^CB/S^CB ≥ 1e−6) ; T^cou à 1e−12·S^G, non exacte (i_CB de BC1 sous r̂\* intégrateur, P101, #131) ; plafond de E1 inactif ;
    - engagement 4 (F5) : M^G et S^G pour E1, E4, E6, E9 ; D_F et S^F pour E5 ; D_H et S^H pour E12 ; E5 et E12 égaux au bit à leur valeur à D = 0 ; E6 Tr ≥ 0 ; E9 absorbe la poussière ; E4 : A inchangée à k·ε·S ;
    - caisse, critère 11 (P158) : « demandé » = plan non plafonné P(1 + π\*)θ_G ŷ, « exécuté » = ligne 2 ; chocs injectés par composition dans `tests/`, jamais dans `src/` (F1) ; hausse d'un tour au suivant par appel direct de E1 à n_a ∈ {4 ; 12 ; 52}, retour après 12 tours à −5 % jugé à n_a = 12, publié à 52 ; au-delà de la marge (+25 % à π̄ ∈ {0 ; 2 %}, +60 % à 10 %) : G^plan = max(0 ; M^G_t) exactement au tour du choc, rationnement attribué à E1, noyau sans arrêt, plafond levé sous 12 tours, sans réactivation ; marge publiée par π̄ sous la forme h_max = ν_G/(Γ̄ s_G) − 1 (s_G = G/PB), la forme approchée (ν_G/Γ̄ − 1)/s_G étant fausse ;
    - parts non payées, critère 12 (F9, P157) : θ_Tr > 0 déclaré avant l'essai en appel direct, état résolu inchangé ; cas (iii) : arrêt typé du noyau ; cas (ii), par appel direct ou Π^CB imposé : ΔE^CB_t = −(perte non couverte)_t à 1e−12·S^CB ;
    - couverture (F6) : E4(i + 0,01) − E4(i) = φ·par_pas(0,01)·A à 1e−12 relatif ; φ = 0 ⇒ T^cou = 0 exactement ; choc sur r̂\* : au tour n seul Div_Bk varie de Δ·(B_Bk + Res − L^CB)/n_a, T^cou reprend Δ·A/n_a, ΔYD = 0 avec B_H = 0 ; ligne 11c égale au premier terme de Π^CB au bit (F7) ;
    - C59 (P156, P160) : ν_G de 1,1 à 1,2, référence 1,15 ; θ_CB 0 → 0,05 → 0,5 ; marche de ν_G en cours de trajectoire ; seuils 1e−12·S par pas et 1e−10 relatif sur 720 pas (production, prix, taux, revenus non financiers, dette consolidée) ; M^G, B_Bk et (L^CB ou Res) écartés de Δν_G·PB_{t−1} à 1e−12·S ; à la clôture de 8c, Res = max(0 ; B_CB − M^G − E^CB) et L^CB = max(0 ; M^G + E^CB − B_CB) à ε·S^CB (remplace « Res > 0 au-delà de s_CB ≈ m·M^G/B ») ; l'ancien seuil « 1e−12 relatif » reste publié ;
    - bornes, critère 16 : B_CB + θ_CB·Em ≥ 0 et B_Bk + ΔB^prim_Bk ≥ 0 sous rachat, par appel direct ; « plafond actif » := G^plan_t < plan non plafonné ; ς_B uniforme sous Em < 0, déclaré en `\limites` (P159) ;
    - C62 (F11) : comparaison à 0,174 / 0,650 (E12 amendé ; 0,131 / 0,487 historiques) ; temps de doublement sous φ = 0 sur le moteur (choc G +1 % aux tours 1 à 12, contrôle apparié, ρ̂ sur les tours 240 à 720, ln 2 / ln ρ̂), sans verdict ;
    - indicateurs du pas (F8) : G^plan, G exécuté, plan non plafonné, plafond de E1 actif, T^cou, M^G, M^G\*, parts de E13, émission par souscripteur (19a) ; ratios sur 12 tours → J4 (#82) ;
    - horizon du critère 7, ligne (c) (F10) : H_b = max(720 ; 12·⌈20·ln 2/(−ln ρ_b)/12⌉) pas à n_a = 12, ρ_b de `outils/maquette_conjointe.py` figé avant l'essai (rayons publiés à `sec:finances_publiques-conditions`), redéclaré prospectivement si S1 donne un autre ρ ; « H = 5 500 » de la fiche 8 périmé ;
- **#106** : retrait si aucun bloc ne déclare la lecture à la fin du rang 3 (P51), sinon label `eq:moteur-variation-tour`, balise et test ; règle mécanique, aucun choix après mesure ; trajectoires identiques au bit.
- **#101** : « aucun écart » sur la liste étendue de l'issue, chaque valeur avec sa catégorie (A ou S) et sa source ; la mutation par inversion de signe détecte chaque valeur ajoutée.
- **#134** : encadré λ ≤ n_a de `sec:cadre-calendrier` sorti de « proposée » (règle exécutée, ADR 0013, H3.2) ; mentions « `scenarios/` au jalon J3 » ramenées à J3-e ; renvois à #115 vérifiés un à un, corrigés s'ils sont faux ; compilation XeLaTeX verte ; concordance inchangée par ce commit.
- **Branche** : stationnarité du **socle complet** (blocs 2 à 9 réels, aucun bloc d'essai) à 1e−9 relatif sur 720 pas aux trois π\*, liste de P94 étendue aux grandeurs du bloc 9 *(précisée le 15/11/2026, avant tout essai, F4 et P161 : G^plan, G, T_H, T^cou, T_F, Tr, lignes 11b et 11c, M^G, M^G\*, Em, ΔB^prim_Bk, ΔB^prim_CB, B, B_Bk/B, dette consolidée/(n_a PIB), Y^HS, rapportés à Γ̄^t, n_a = 12 ; la ligne du J1 « dette/PIB égal au moteur à t = 0 » va à J3-e)*, nullités calculées (P121 ; T^cou, parts non payées, B_H) ; verdicts du banc de P87 (bloc d'essai 9) et du banc de J3-d1 (X4) identiques au bit ; concordance attendue à **90 labels** (77 + 13), **91** si #106 pose `eq:moteur-variation-tour` ; part de chaque bloc ≤ 0,48 ms (alerte 0,276 ms) sur la plateforme de référence, total du socle complet publié ; #80 en échec attendu (un succès inattendu fait échouer la batterie).

**Conditions d'arrêt** : contrat partagé à modifier au-delà de l'annotation du rang 1b ; drapeau de mode dans `src/` ; stationnarité du socle complet hors seuil sans erreur de code, y compris à π\* = 10 % seul ; rationnement de caisse de l'État ou part non payée sur le sentier sans choc ; arrêt du noyau sur le sentier ; racine parasite à φ = 1 ; état d'arrivée dépendant d'une vitesse d'ajustement (`docs/exigences.md` § 2.7 ; *précisé le 15/11/2026, avant tout essai, P163 :* le continuum connu de r̂\*, P101, #131, en est exclu, seul un continuum nouveau la déclenche) ; boucle propre de module ≥ 1 ; instabilité connue réapparue ; part d'un bloc au-dessus de 0,48 ms ; chiffre publié non reproduit.

**Effet attendu sur les résultats** : premiers résultats du moteur pour le bloc 9 et première exécution du socle complet ; aucun résultat final (état initial résolu par `scenarios/` et test zéro en J3-e), aucune référence ; #133, #106, #101, #134 et l'engagement 6 sans effet sur les trajectoires.

### 2. Branches suivantes (extrait : ligne 10, J3-d2, branche fusionnée)

| Ordre | Branche | Issues | Motif du regroupement et état |
|---|---|---|---|
| 10 | **J3-d2 `claude/j3-finances-publiques` (décidée, P147, P155 ; PR #146)** | #133, #132, #106, #101, #134 ; rattachés : six engagements de J3-d1 (sur #132), lignes (c) des fiches 5 et 6 (P122) et des fiches 7 et 8 (P90), double appel de `besoin_d_emission` | Bloc 9 ; première exécution du socle complet. Rangs 0 à 8 faits (tête `f1c8f2f`) ; en attente de validation et de fusion. |

### 3. Issues hors plan (extrait : relevé du 15/11/2026 après la PR #136, mis à jour au rang 8 de J3-d2, avec ses points ouverts et ses dépendances)

*Relevé du 15/11/2026* (point d'étape après la fusion de la PR #136, `main` = `30078bb`) : **52 issues ouvertes** (`list_issues`, état ouvert, `totalCount` = 52) ; #124, #60, #67, #123, #103 et #138 fermées (état vérifié par la session le 15/11/2026) ; #137 et #139 à #145 créées les 14 et 15/11/2026. Les rattachements de #137 et #139 à #145, et le plan de J3-d2, sont **proposés, à décider** (Q1 à Q6, § 4). Relevé précédent (14/11/2026 après la PR #129, mis à jour au rang 8 de J3-d1) : historique, partie E, § 3 ; relevés antérieurs : parties C et A, § 3. La colonne « Branche prévue » n'est pas reportée sur GitHub.

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #10 | Registre d'exemptions de la concordance | hors plan | aucune exemption prévue |
| #11, #14 | Dependabot ; ruleset de `main` | mainteneur, hors branche | `ready-for-human` depuis le 30/09/2026 (Q10) |
| #37 | Aucun levier d'offre au socle | J4, au plus tard J7 | M26, M28 |
| #45, #55, #62, #92, #130 | Calibrations (λ_w ; fiche 6 ; ν_H et λ_H ; μ̄ ; ϖ_L, ϖ_D, ϑ, r̄) | calibration (P43 (a), P115) | #55 recoupe #92 ; ζ calibré par #55 déplace la frontière de #143 |
| #46, #47, #48 | Okun ; prix administrés ; levier de répartition | J4 (#47 puis J7) | inchangé |
| #52, #53, #63, #70, #79, #81, #82 | Restitutions et scénarios O2, O3 | J4 | inchangé |
| #54, #56 | Aller-retour de π\* ; signe net d'une hausse de taux | J4, sans `Closes` | condition (c) du levier de cible sur #54 (P99) |
| #57 | Crises de crédit sous la règle F | J6 | inchangé |
| #64 | S-ζ hors cible durable | J5 | inchangé |
| #78, #89 | Coût de la dette ; stratégie dominante | J4 (#78 puis J6) | #89 dépend de #88 |
| #80 | Superneutralité (critère 13 de la fiche 8) | hors branche, échec attendu | voie (c) de M32 maintenue (P89) ; rejugée par la batterie en J3-d2 (succès inattendu = échec) |
| #87, #88, #111, #116 | D_F ≥ 0 hors stationnaire ; fenêtre longue ; trajectoires C-HS ; maquette | J3-f (P42, P60) | #116 → #111 |
| #101, #106, #132, #133, #134 | Périmètre de J3-d2 (P147) | **J3-d2, faites** (rangs 2 à 6, § 1) | `Closes` de la PR #146, fermeture à vérifier après la fusion |
| #108 | Identifiants Cn et Co | J5 | P46 (a) |
| #110 | Processeur de l'exécuteur en CI | J3-g (P60) | inchangé |
| #114 | Critère I1 : lignes « J3 » au socle complet | J3-e | reçoit la mesure de #131, les lignes (c) des fiches 5 et 6 (P122) et l'exécution de #139 et #140 (P149, P150) |
| #115 | Radical `observation` | J3-e | renvois de la spécification vérifiés par #134 |
| #120 | `Cadre` à n_a ≠ 12 | J3-e (P82) | option (a) |
| #122 | IN^vol = 0 ⇒ IN = 0 à l'état chargé | J3-e (P84) | inchangé |
| #125 | Facteur de croissance par pas | point 2 : J3-f ; points 3 à 6 : J3-e (P84) | point 1 réalisé en J3-c (P88) |
| #131 | BC2 en log, terme de Jensen de r̂\* | J3-e, mesure à #114 (P101) | P117 |
| #135 | `tab:phases` et levier de taux au J4 | J4 | recoupe #54, #56 |
| #137, #142, #144 | Refus génériques sans étape ; localité de la lecture nette ; travail redondant du chemin chaud | branche technique « forme du code » après J3-d2 (P151) | trajectoires identiques au bit ; mesure P57 avant / après ; le bloc 9 suit d'emblée la règle de #142 (critère de #132) |
| #139 | Critère « Endettement, dépôts » de la fiche 6 | voie (ii) décidée (P149) ; exécution en J3-e | échec attendu strict ; banc à blocs d'essai de banque et de banque centrale |
| #140 | Bornes (c) de la fiche 6 | voie (i) décidée (P150) ; exécution en J3-e | test du refus de la moitié du crédit (C31) dans les deux options |
| #141 | Restitution du refus de crédit | J4 (Q6) | avec #70 ; mesure de `macro` en commentaire |
| #143 | S6 : ti = 0 au-delà d'une frontière | hors J3-d2 ; décision du mainteneur avant le J4 (Q2) | bloc 6 ; option (3) rouvre M28 ; question à `monnaie` sur la caisse des entreprises sans réponse |
| #145 | Condition du coefficient de richesse sur π\* de la table | J4, avec le levier de cible (#54) (Q6) | déclaré par la spécification ; acceptable en J3 (`macro`) |
| #147, #148, #149, #150 | C62 en régime linéaire ; B_Bk, B_CB ≥ 0 sans contrôle ; « proposée » périmée au glossaire ; forme du code du bloc 9 (E7 doublé, lecture de position, E5 par total de ligne, docstrings) | à rattacher au point d'étape après J3-d2 | nées de J3-d2 (P171) ; #150 recoupe #142 et la branche « forme du code » (P151) ; E5 par colonne au J5 |

**Points ouverts sans issue** : mutant équivalent B_Bk/Res dans B5, à rouvrir avec le corridor (J6, P116) ; résolution de l'état initial par `scenarios/` sans dupliquer le script (J3-e, § 2) ; reconsolidation de l'ADR 0013 (P154). Le double appel de `besoin_d_emission` est levé par le bloc 9 réel (rang 3).

**Dépendances** (15/11/2026, après la PR #136). **Ajoutées** (décidées, P147 à P152) : #132 → #106 ; #132 (localité de la lecture nette du bloc 9) → #142 ; J3-d2 → forme du code (#137, #142, #144 : mesure P57 sur le socle complet) ; #143 → domaine du levier de taux (J4) et #55 (ζ calibré) ; avis de `monnaie` sur la caisse des entreprises → #143 ; socle complet (J3-d2) → #139 (banc sans blocs d'essai) ; #145 → #54 ; #141 → J4 (avec #70). **Retirées** : J3-d1 → #101 ; #103 → #132 (#103 fermée, critère de M^G corrigé, P125) ; #124 → blocs acheteurs réels et #60 → #67 (issues fermées). **Inchangées** : #133 → #132 ; achèvement des blocs du socle → #106 ; engagements de J3-d1 → #132 ; #131 → #114 ; branche de calibration → J3-e ; #116 → #111 ; #89 → #88.

### 4. Décisions du mainteneur (extrait : points ouverts du rang 8 de J3-d2)

**Points ouverts au 15/11/2026, rang 8 de J3-d2** : validation et fusion de la PR #146 ; issue proposée par `coder`, non créée (§ 1 de la PR) : « Noyau : rapport résidu/S infini sur une ligne à échelle nulle (ligne 20, porte de la monnaie centrale) » (socle complet, π\* = 2 %, θ_Tr = 0,3 et ς_B = 1 aux pas 5 à 7 : `DefautComptable` au pas 8, phase 6, `eq:noyau-variation-monnaie-centrale`, résidu 5,8e−18 sur S = 0) ; fiche 8 (l. ~1497 et ~1524) : « Neutralité de s_CB » encore classée (c) et grille « borne m·M^G/B » non remplacée par P156 — à reprendre par `docwriter` ; au point d'étape après J3-d2 : reconsolidation de l'ADR 0013 (P154), rattachement de #147 à #150, découpage de J3-e à J3-g (P61) ; instruction de #143 (P148) ; issue proposée par `jeu`, non créée (ou amendement de #82) : grandeurs du bloc 9 calculées hors interface au J4 ; durée d'une partie non fixée (#56).

### 7. Branches fusionnées (extrait : ligne de J3-d1)

| Branche | PR | Jalon | Fusion | Détail |
|---|---|---|---|---|
| `claude/j3-menages-investissement` | #136 | J3 (J3-d1) | 15/11/2026, 10:47 UTC, commit de fusion `30078bb` (parents `731aac3`, `1e7f736`), par le mainteneur | Issues fermées par `Closes` : #124, #60, #67, #123, #103 ; #138 fermée par `ea2e0da` (fermetures vérifiées par la session le 15/11/2026). 36 commits hors fusion (5 `code:`, 4 `tests:`, 27 `docs:` ; `git rev-list --no-merges 731aac3..1e7f736`). Rangs et SHA : historique, partie E, § 1, et corps de la PR #136. Décisions : P111 à P146. Fable : 0 sur 3. Premiers résultats du moteur pour les blocs 5 et 6, aucun résultat final ; `tests/references/` intact. Concordance : 77 labels. Issues nées de la branche : #137 à #145. |

### Complément sorti le 16/11/2026 au rang 1b de la branche « forme du code » (`claude/j3-forme-du-code`, tête `0d35718`, PR #151)

Sortis de `docs/feuille-de-route.md` pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé, titres décalés d'un niveau.

#### Décisions P156 à P171 (rangs 1a à 7 de J3-d2), 15/11/2026

P147 à P155 (point d'étape après la PR #136, Q1 à Q10), en vigueur : historique, partie E, complément du rang 8 de J3-d2 (texte inchangé) ; Q1 à Q10 : partie E, § 4. P156 à P163 : arbitrages R1 à R8 du rang 1a, selon l'avis des experts ; détail dans les critères de la fiche de J3-d2. Depuis le 16/11/2026, un renvoi « § 1 » de P156 à P171 se lit dans l'historique, partie F, § 1. P166 à P171 : décisions du mainteneur sur les rangs 5 à 7.

| N° | Date | Décision | Question |
|---|---|---|---|
| P156 | 15/11/2026 | C59 en deux niveaux de seuil (1e−12·S par pas ; 1e−10 relatif sur 720 pas pour production, prix, taux, revenus, dette consolidée) ; ν_G de 1,1 à 1,2, référence 1,15 ; Res et L^CB sous forme exacte en stocks ; correction prospective avant tout essai, ancien seuil publié. | R1 |
| P157 | 15/11/2026 | C60 et ligne « Perte » de la fiche 8 : ΔE^CB_t = −(perte non couverte)_t à 1e−12·S^CB ; « ligne nommée » lue sous QM2 (a) ; cas (ii) par appel direct. | R2 |
| P158 | 15/11/2026 | Critère 11 complété des trois points de `jeu` : n_a ∈ {12 ; 52} ; cas au-delà de la marge (+25 % ; +60 % à π̄ = 10 %) ; marge publiée sous la forme exacte de `macro`. | R3 |
| P159 | 15/11/2026 | ς_B sous Em < 0 : forme uniforme, déclarée en `\limites`. | R4 |
| P160 | 15/11/2026 | « Neutralité de s_CB » de la fiche 8 jugée dans J3-d2 avec C59 (précise P90). | R5 |
| P161 | 15/11/2026 | Ligne du J1 « dette/PIB égal au moteur à t = 0 » → J3-e, remplacée dans J3-d2 par dette consolidée/(n_a PIB) dans la liste de P94 ; C51 publiée à ζ = 4 indicatif, verdict « à ζ calibré » → branche de calibration. | R6 |
| P162 | 15/11/2026 | P122 se lit « réaffirmation avec le bloc 9 réel des lignes (b) appuyées sur le bloc d'essai 9 » (liste au § 1). | R7 |
| P163 | 15/11/2026 | Continuum connu de r̂\* (P101, #131) exclu de la condition d'arrêt « état d'arrivée dépendant d'une vitesse ». | R8 |
| P164 | 15/11/2026 | Décisions de forme F1 à F11 du rang 1a (critères précisés du § 1), prises par la session sous la délégation P153 (P118, P133). | F1 à F11 |
| P165 | 15/11/2026 | Table `finances_publiques` dans `EnsembleDesParametres` (F1, H3.5 étendus, forme de `menages`) : ν_G, U^eq, valeurs à levier fermé de θ_G, θ_Tr, τ_H, τ_F, φ (paramètres au J3, comme π\* sous BC4 ; commandes au J4, G4, sans drapeau de mode) ; conditions jointes dans `__post_init__`. Forme, session sous P153, **confirmée le 15/11/2026** ; ADR 0013, rang 1b de J3-d2, point 8. | rang 1b |
| P166 | 15/11/2026 | « Délais » des fiches 5 et 6 (P162) : publiés comme **méthode substituée**, passage apparié du moteur au lieu de l'appel direct prévu. | rang 5 |
| P167 | 15/11/2026 | C62 : critère d'homogénéité reporté à #147 ; publication sans marque de régime linéaire. | rang 5 |
| P168 | 15/11/2026 | Temps de doublement sans reprise à 2 % : « 382 tours » remplacé par « 381 tours (maquette 381,6) », 382 barré (`7d34b9b`). | rang 6 |
| P169 | 15/11/2026 | Critère 12 : les sous-points non jugés sont rendus jugés par des tests (`6b959f7`), non reclassés. | rang 7 |
| P170 | 15/11/2026 | Tableau des phases du bloc 9 complété par `docwriter` dans la branche, exception de la règle 9 (`df4e3b9`), lien au `.tex` tenu par un test exact (`f1c8f2f`). | rang 7 |
| P171 | 15/11/2026 | Issues créées : #147 (C62, régime linéaire), #148 (B_Bk, B_CB ≥ 0 sans contrôle), #149 (glossaire « proposée » périmé), #150 (forme du code du bloc 9) ; commentaire de `monnaie` versé sur #81 (taux directeur négatif, tours 11 à 19 à π\* = 0). | rang 7 |

*Erratum de transcription de P165 (15/11/2026, rang 8 ; décision inchangée)* : (1) U^eq **n'est pas** dans la table `finances_publiques` ; sa seule maison reste la table du travail (H3.3 ; spécification l. 3212, « paramètre du bloc travail ») ; (2) la section ne déclare aucune condition jointe entre champs de la table, `__post_init__` n'appelle que `valider_table`. Le code est conforme à la spécification (`src/nations/moteur/parametres/finances_publiques.py:23-32`) ; ADR 0013, annotation du rang 8 de J3-d2.

### Complément sorti le 16/11/2026 au rang 9 de la branche « forme du code » (`claude/j3-forme-du-code`, tête `2355516`, PR #151)

Sortis de `docs/feuille-de-route.md` pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé, titres décalés d'un niveau. Les renvois « ci-dessous », « ci-dessus » et « § 4 » de ces lignes se lisent dans le présent complément ; P172 à P181 restent en vigueur.

#### Décisions P172 à P181 (rang 0 de la branche « forme du code »), 16/11/2026

| N° | Date | Décision | Question |
|---|---|---|---|
| P172 | 16/11/2026 | Q1 (a) : périmètre de la branche « forme du code » = #137, #142, #144, #150 avec `Closes` ; le point 3 de #150 (E5 par colonne) est détaché dans #152, pour le J5. | rang 0 |
| P173 | 16/11/2026 | Q2 (a) : banc d'empreintes SHA-256 (socle complet, bancs de P87 et de J3-d1) versé au rang 1a comme script d'`outils/`, rattaché à #144. | rang 0 |
| P174 | 16/11/2026 | Q3 (a) : #149 cinquième issue du périmètre, au passage unique de `docwriter` ; reprise de la fiche 8 (« Neutralité de s_CB », grille « borne m·M^G/B ») versée sur #149, validée par `monnaie`. | rang 0 |
| P175 | 16/11/2026 | Q4 : délégation P118, P133, P134, P136 et P137 reconduite pour la branche, comme P153 ; résultats finaux et critères de fiche réservés au mainteneur. | rang 0 |
| P176 | 16/11/2026 | Q5 (a) : reconsolidation de l'ADR 0013 au rang 9, ADR 0014 de consolidation sans décision nouvelle, ≤ 40 ko, par `architect-approfondi` avec Fable (§ 4.1.3, consultation 1 sur 3 de la branche) ; l. 149 et 432 de l'ADR 0012 reprises. | rang 0 |
| P177 | 16/11/2026 | Q6 : découpage de J3-e à J3-g au point d'étape qui suit la fusion de la branche, par `architect-approfondi`. | rang 0 |
| P178 | 16/11/2026 | Q7 (a) à (f), toutes retenues : #147 à J3-f, harmonisation « 63 tours » versée sur #147 ; #148 au J4, instruite d'abord par `monnaie` ; issue du noyau (`coder`) créée, #153, J3-e ; issue du plafond de E1 (`macro`) créée, #154, J3-f ; #82 amendée (indicateurs F8) ; constat de #81 signalé à `jeu`. | rang 0 |
| P179 | 16/11/2026 | Q8 : `jeu` consulté dès maintenant sur la durée d'une partie (#56) ; #11 et #14 inchangées. | rang 0 |
| P180 | 16/11/2026 | Avis de `jeu` sur la durée d'une partie (P179) versé dans une issue propre, #155 (120 tours par défaut, format court de 60, évaluation de sortie à leviers figés ; à trancher avant le J4), #56 portant sur le signe d'une hausse de taux ; 381 et 63 tours sont le doublement de l'écart de la boucle taux-inflation sous φ = 0, pas de la dette. | rang 0 |
| P181 | 16/11/2026 | Avis ludique de `jeu` versé sur #81 (π\* = 2 % par défaut, domaine du levier de taux aligné sur la règle) ; coût en fidélité d'un plancher du taux directeur au socle demandé à `monnaie` avant le J4. | rang 0 |

#### Questions au mainteneur du 16/11/2026 (point d'étape après la PR #146, rang 0 de la branche « forme du code »)

Proposées par `architect` ; **décidées par le mainteneur le 16/11/2026 : P172 à P179** (ci-dessus). Recommandation en premier.

- **Q1, périmètre avec `Closes`** : (a) #137, #142, #144, #150, le point 3 de #150 (E5 par colonne) détaché dans une issue nouvelle pour le J5 ; (b) idem, #150 sans `Closes`, laissée ouverte pour son point 3 ; (c) #150 entière, E5 par colonne dans la branche, avec une lecture de `macro` (colonne de chaque ligne 1 à 5), qui fait sortir la branche du circuit 3 ; (d) base de P151 seule, #150 renvoyée à J3-e.
- **Q2, banc d'empreintes** : (a) versé au rang 1a comme script d'`outils/` (empreintes SHA-256 du socle complet et des bancs de P87 et de J3-d1), rattaché à #144, puisque tout contrôle mécanique est un script (principe 7 des workflows) et que le critère de la branche en dépend ; (b) laissé hors dépôt, empreintes citées par la session.
- **Q3, documentation périmée** : (a) #149 en cinquième issue, au passage unique de `docwriter`, avec la reprise de la fiche 8 (l. ~1497 et ~1524 : « Neutralité de s_CB » encore classée (c) malgré P160, grille « borne m·M^G/B » non remplacée par P156) versée sur #149 par commentaire, validée par `monnaie` (pilote de la fiche 8) ; (b) #149 et la fiche 8 en J3-e ; (c) une issue propre pour la fiche 8.
- **Q4, délégation** : reconduire pour la branche P118 (délégation technique), P133, P134, P136 et P137, comme P153 ; résultats finaux et critères de fiche réservés au mainteneur (aucun attendu).
- **Q5, reconsolidation de l'ADR 0013 (P154 ; 93 ko pour un plafond de 40 ko, P76)** : (a) au rang 9 de la branche, une fois les contrats de #144 et #150 stabilisés et avant que J3-e n'y ajoute `scenarios/` et l'observation : ADR 0014 de consolidation, sans décision nouvelle, ≤ 40 ko, rédigé par `architect-approfondi` avec `model: "fable"` (§ 4.1.3, consultation 1 sur 3), les l. 149 et 432 de l'ADR 0012 lues par lui (l'ADR 0012 reste intact, P76) ; (b) idem en Opus `high`, sans Fable ; (c) au point d'étape suivant, avec le découpage (Q6) ; (d) après J3-e.
- **Q6, découpage de J3-e à J3-g (P61)** : au point d'étape qui suit la fusion de la branche « forme du code », par `architect-approfondi`, avant le plan de la branche de calibration ; le seuil « macro » (§ 4.3, deux branches suivantes redécoupées) y sera probablement atteint : Fable proposé alors.
- **Q7, rattachements et issues proposées** : (a) #147 à J3-f (S1) ; l'harmonisation « 63 tours (maquette 63,2) » (un commit `code:` sur le relevé de `outils/maquette_conjointe.py`, puis `docs:`, modèle de 381,6) versée sur #147 par commentaire ; (b) #148 au J4, question de l'issue instruite par `monnaie` avant le J4 ; (c) issue de `coder` (noyau, rapport résidu/S infini sur une ligne à échelle nulle) créée (`bug`), rattachée à J3-e, instruite par `architect` et `monnaie` : elle touche l'invariant « tolérance relative à l'échelle du bilan, jamais une constante absolue » ; (d) issue facultative de `macro` (plafond de E1 sous placement raté total prolongé) créée, rattachée à J3-f, critère écrit avant l'essai ; (e) issue proposée par `jeu` versée comme amendement de #82 (indicateurs du pas de F8) plutôt qu'en issue nouvelle ; (f) constat de #81 signalé à `jeu` par une consultation de routine hors branche (ligne au § 8), ou au point d'étape qui précède le J4.
- **Q8, hors branche** : #11 et #14 (`ready-for-human`) ; durée d'une partie (#56), à fixer avant le J4, sur avis de `jeu` (perceptibilité de φ de 0 à 2 %).

**Points ouverts au 16/11/2026, rang 0 de la branche « forme du code »** : Q1 à Q8 ; instruction de #143 (P148) ; points ouverts du rang 8 de J3-d2 : historique, partie F, § 4, repris au § 3 et ci-dessus.

## Partie E : extraits de la tête sortis le 15/11/2026 (point d'étape après la fusion de la PR #136, rang 0 de J3-d2), figés

Sortis de `docs/feuille-de-route.md` à `30078bb` (`main`, commit de fusion de la PR #136), pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé, titres décalés d'un niveau. Les numéros P-n restent stables ; ces décisions restent en vigueur tant qu'aucune décision ultérieure ne les remplace.

### En-tête (extrait : mises à jour de la tête du 14/11/2026, après la PR #129, au 15/11/2026, rangs 4 et 5 de J3-d1)

**Mise à jour précédente** : 15/11/2026, fin des rangs 4 et 5 de J3-d1 (session, `060933a`) — branche `claude/j3-menages-investissement` ; état au § 1, décisions P130 à P141 au § 4.

**Mise à jour antérieure** : 14/11/2026, point d'étape après la fusion de la PR #129 (`architect-approfondi`) — `main` = `731aac3` (commit de fusion, parents `6a22d39` et `6632dce`) ; aucune branche de travail ouverte ; J3-c consignée (§ 7) ; découpage de J3-d proposé (§ 1, § 2), décisions P111 à P118 (§ 4) ; fiche de J3-c, relevé du 14/11/2026 après la PR #117, P87 à P99 sortis vers l'historique, partie C (P76). Mises à jour plus anciennes : historique, partie D, en-tête, puis historique de Git (`git log -- docs/feuille-de-route.md`).

### 1. Branche de travail en cours (extrait : fiche de J3-d1, à la fusion de la PR #136)

**J3-d1** (`claude/j3-menages-investissement`, PR #136, ouverte depuis `main` à `731aac3`) : plan, état et critères ci-dessous. Fiche de J3-c, figée à la fusion de la PR #129 : historique, partie C, § 1.

#### Plan proposé pour J3-d1 « ménages et investissement » (`claude/j3-menages-investissement`) — domaine des plans (#124), ménages (#60), investissement (#67), labels de d et tu (#123), signes sous lecture nette (#103)

Plan (rangs 0 à 8 ; proposé par `architect-approfondi` le 14/11/2026, décidé par le mainteneur le même jour, P111 à P118) : historique, partie D, § 1, texte inchangé. Issues avec `Closes` : #124, #60, #67, #123, #103 (P112) ; ordre #124 → #60 → #67, #123 avec #67 ; délégation technique reconduite (P118).

**État au 15/11/2026, rang 8 (consignation)** — tête `414a8a4` ; rangs 0 à 7 faits ; restent la sortie du brouillon et la fusion par le mainteneur :
- **rangs 0 à 5** : `49fba27` à `ea2e0da` (P111 à P141 ; passation de la PR #136 du 15/11/2026) ; critère « Branche » **tenu** sur le banc X4 seule aux trois π\* (pire relatif 1,8e−12, pire nulle 1,8e−14) ; sans X4, 3,7e−8 à 10 % (canal rentier confirmé) ;
- **rang 6** (`docwriter`, un commit `docs:` par issue) : `e953afc` (#124), `b5e98f8` (#60), `fae37b3` (#67), `362ef4b` (#123), `1af1b88` (#103) ; validation de `macro` et de `monnaie` (M^G) conforme avec réserves ; reprises `d3635ed`, `ed4c9c2`, `4c5ce65`, `4b8ce65`, `f9e04d7`, `5e5662b` ; `coder` : `046fcde` (lecture nette nommée D̃_H, Ṽ_H ; résultats identiques au bit), `bfbddae` (refus de crédit publié sur 40 pas) ;
- **rang 7** (revue finale complète, règle 10) : `audit` **non conforme** sur M1 (bornes (b) du bloc 6 affirmées pour tout le domaine, alors que S6 rend ti = 0 au-delà d'une frontière), `macro-approfondi` conforme avec réserves, `/code-review` (effort medium) ; reprise `4792a79`, `6e7db86` (M1 en voie 2, P145 ; remarques r1 et r2 d'`audit` du rang 5), `fc48f6e`, `f232b70`, `414a8a4` (réserves de `macro` sur ce diff) ;
- **verdicts** : concordance **77** labels (P142) ; parts P57 sur la plateforme de référence (run 43700445516 sur `bfbddae`) : ménages 0,0081 ms, investissement 0,0186 ms par pays-pas, seuil 0,48 ms, tenu — remplacent « ≤ 0,029 ms hors plateforme » ; « Vitesses » de la fiche 5 non tenu en relatif, tenu sous P130 ; « Endettement, dépôts » de la fiche 6 non tenu (#139) ; bornes (b) de la fiche 6 tenues sur le lot |Δϱ| ≤ 0,1 par an, frontière de S6 publiée (P145) ; bornes (c) en constat sans verdict (#140) ;
- **escalades, relances et arrêts** (aussi dans la PR) : `macro` (contrôle du diff correctif) et `macro-approfondi` (revue finale) arrêtés à leur limite de tours, chacun relancé une fois pour rendre son rapport ; aucune consultation Fable (budget de J3-d1 : 0 sur 3) ;
- **restent ouvertes après la fusion** : #139 et #140 (décisions réservées au mainteneur), #11 et #14 (hors branche) ; #138 fermée par `ea2e0da` ; #141 à #145 créées (P146).

**Critères d'acceptation, écrits avant l'essai** (précisés au rang 1a, jamais après une mesure) :
- **#124** : la voie retenue refuse (exception typée, jamais écrêtage) un plan C_plan, I_plan ou G_plan négatif et d < 0, sur le cas de l'issue (C_plan = −1,0) et sur un lot adverse ; trajectoires de la référence identiques au bit (tableau avant / après sans ligne).
- **#60** : lignes (a) et (b) de la fiche 5, § 9.6, à leurs seuils ; état stationnaire égal au script à 1e−10 relatif à n_a = 12, π\* ∈ {0 ; 2 ; 10 %} (P56, P77), n_a ∈ {4 ; 52} couvert par le script ; YD égal aux lignes exécutées à 1e−12 × S ; plan insensible au registre de l'indice (écart nul, #58) ; B_H ≡ 0 exactement ; boucle propre de module < 1 ; refus au chargement hors du domaine ; ~~sept labels~~ *(correction du 14/11/2026, avant tout essai, P119 : H1 a déjà son label depuis #61)* six labels (H2 à H7).
- **#67** : lignes (a) et (b) de la fiche 6, § 9.6 ; état stationnaire égal au script (mêmes seuil et grille) ; Div ≥ 0 en contrainte de domaine (M28) ; λ_ti dans le domaine de stabilité mesuré de la fiche ; domaine strict de K (P80) ; table du bloc 6 complète ; lignes (c) des fiches 7 et 8 à un bloc près à leurs seuils de fiche ; ~~onze labels~~ *(correction du 15/11/2026, avant l'essai du décompte, P142 : F1 porte aussi `eq:investissement-credit-servi`)* douze labels.
- **#123** : labels de d et de tu, une balise chacun (P83) ; ω\* et g inchangées.
- **#103** : critères et contraintes de signe de D_H, D_F et M^G réécrits sous la lecture nette et le contrat de poussière ; correction prospective, ancien critère publié avec sa date.
- **Branche** : stationnarité partielle à 1e−9 sur 720 pas aux trois π\*, blocs 2 à 8 réels, bloc d'essai 9, liste de P94 étendue aux grandeurs des blocs 5 et 6, ~~grandeurs nulles par liste déclarée (P100)~~ *(correction du 14/11/2026, avant tout essai, P121, P124)* : nullités calculées (P121) ; bloc d'essai 9 avec la couverture X4 (P124), étiquette « couverture X4 active » ; T^cou ajouté aux grandeurs nulles ; concordance attendue à ~~77 labels (57 + 7 + 11 + 2, à confirmer au rang 1a)~~ *(correction du 14/11/2026, avant tout essai, P119)* ~~76 labels (57 + 6 + 11 + 2)~~ *(correction du 15/11/2026, avant l'essai du décompte, P142)* 77 labels (57 + 6 + 12 + 2) ; part de chaque bloc ≤ 0,48 ms (alerte 0,276 ms) ; verdicts de P87 sur le banc de J3-c inchangés.

**Conditions d'arrêt** : contrat partagé à modifier au-delà de l'annotation du rang 1b ; drapeau de mode dans `src/` ; stationnarité partielle hors seuil sans erreur de code ; arrêt du noyau sur le sentier (caisse nette, Res < 0) ; état d'arrivée dépendant d'une vitesse d'ajustement (`docs/exigences.md` § 2.7) ; boucle propre de module ≥ 1 ; instabilité connue réapparue ; part d'un bloc au-dessus de 0,48 ms ; chiffre publié non reproduit.

**Effet attendu sur les résultats** : premiers résultats du moteur pour les blocs 5 et 6 ; aucun résultat final, aucune référence ; #124 sans effet sur la trajectoire de référence.

### 3. Issues hors plan (extrait : relevé du 14/11/2026 après la PR #129, mis à jour le 15/11/2026 au rang 8 de J3-d1)

*Relevé du 14/11/2026* (point d'étape après la fusion de la PR #129, `main` = `731aac3`) : **49 issues ouvertes** (`list_issues`, état ouvert) ; #119, #121, #61, #91 et #90 fermées par la PR #129 ; #130 à #135 créées le 14/11/2026. Rattachements décidés : P111 à P117 (§ 4). Relevés antérieurs : historique, partie C, § 3 (14/11/2026, après la PR #117), et partie A, § 3. La colonne « Branche prévue » n'est pas reportée sur GitHub. *Mise à jour du 15/11/2026 (rang 8 de J3-d1)* : #137 à #145 créées ; #124, #60, #67, #123, #103 et #138 fermées à la fusion de la PR #136 ; rattachement de #137 et #141 à #145 au point d'étape après J3-d1.

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #10 | Registre d'exemptions de la concordance | hors plan | aucune exemption prévue |
| #11, #14 | Dependabot ; ruleset de `main` | mainteneur, hors branche | `ready-for-human` depuis le 30/09/2026 (Q9) |
| #37 | Aucun levier d'offre au socle | J4, au plus tard J7 | M26, M28 |
| #45, #55, #62, #92, #130 | Calibrations (λ_w ; fiche 6 ; ν_H et λ_H ; μ̄ ; ϖ_L, ϖ_D, ϑ, r̄) | calibration (P43 (a), P115) | #55 recoupe #92 |
| #46, #47, #48 | Okun ; prix administrés ; levier de répartition | J4 (#47 puis J7) | inchangé |
| #52, #53, #63, #70, #79, #81, #82 | Restitutions et scénarios O2, O3 | J4 | inchangé |
| #54, #56 | Aller-retour de π\* ; signe net d'une hausse de taux | J4, sans `Closes` | condition (c) du levier de cible sur #54 (P99) |
| #57 | Crises de crédit sous la règle F | J6 | inchangé |
| #60 | `menages.py` | **J3-d1, rang 3** | H1 tenue par le moteur (M30, #61 ; P119) ; six labels |
| #64 | S-ζ hors cible durable | J5 | inchangé |
| #67 | `investissement.py` | **J3-d1, rang 4** | avec #123, P80 et les lignes (c) à un bloc près (P90) |
| #78, #89 | Coût de la dette ; stratégie dominante | J4 (#78 puis J6) | #89 dépend de #88 |
| #80 | Superneutralité (critère 13 de la fiche 8) | hors branche, échec attendu | voie (c) de M32 maintenue (P89) ; condition (c) du levier de cible sur #54 (P99) |
| #87, #88, #111, #116 | D_F ≥ 0 hors stationnaire ; fenêtre longue ; trajectoires C-HS ; maquette | J3-f (P42, P60) | #116 → #111 |
| #101 | Test de source de `sec:investissement-taux` | J3-d2 (P113) | après J3-d1, qui peut republier des valeurs de la section |
| #103 | Signes sous lecture nette (D_H, D_F, M^G) | **J3-d1, rangs 1a et 6** | entière, M^G compris (`monnaie`) |
| #106 | Consommateur de `variation_sur_le_tour` | J3-d2 (P51) | retrait sauf consommateur déclaré, constaté une fois les blocs du socle tous écrits |
| #108 | Identifiants Cn et Co | J5 | P46 (a) |
| #110 | Processeur de l'exécuteur en CI | J3-g (P60) | inchangé |
| #114 | Critère I1 : lignes « J3 » au socle complet | J3-e | reçoit la mesure de #131 et les lignes (c) des fiches 5 et 6 (15/11/2026) |
| #115 | Radical `observation` | J3-e | inchangé |
| #120 | `Cadre` à n_a ≠ 12 | J3-e (P82) | option (a) |
| #122 | IN^vol = 0 ⇒ IN = 0 à l'état chargé | J3-e (P84) | inchangé |
| #123 | Définitions exécutées non numérotées | **J3-d1, rang 4** (P83) | labels de d et tu |
| #124 | Domaine de d ≥ 0 | **J3-d1, rang 2** (P84) | voie (a) ou (b) choisie par `macro` au rang 1a |
| #125 | Facteur de croissance par pas | point 2 : J3-f ; points 3 à 6 : J3-e (P84) | point 1 réalisé en J3-c (P88) |
| #131 | BC2 en log, terme de Jensen de r̂\* | J3-e, mesure à #114 (P101) | fait nouveau de la passation de la PR #129 versé en commentaire (P117) |
| #132 | Module du bloc 9 `finances_publiques.py` | J3-d2 (P113) | reçoit le double appel de `besoin_d_emission` |
| #133 | Collision E1–E3 / E1–E13 | J3-d2, avant #132 (P113, P114) | bloc d'essai 9 gardé (P114) |
| #134 | Encadré des vitesses, mentions de `scenarios/` | J3-d2 (P113) | |
| #135 | `tab:phases` et levier de taux au J4 | J4 | recoupe #54, #56 |
| #137, #142, #144 | Refus génériques sans étape ; localité de la lecture nette (max(0 ; ·) hors des fonctions balisées) ; travail redondant du chemin chaud | point d'étape après J3-d1 | forme du code |
| #139, #140 | Critère « Endettement, dépôts » ; bornes (c) de la fiche 6 | mainteneur (P140, P141) | échec attendu strict ; constat sans verdict |
| #141 | Restitution du refus de crédit | J4 | avec #70 ; mesure de `macro` en commentaire |
| #143 | S6 : ti = 0 au-delà d'une frontière ; domaine du taux réel ou forme bornée de S2/S6 | point d'étape après J3-d1 | P145 ; question à `monnaie` (caisse des entreprises) |
| #145 | Condition du coefficient de richesse sur π\* de la table | point d'étape après J3-d1 | recoupe le levier de cible (#54) |

**Points ouverts sans issue** (revue finale de J3-c, passation de la PR #129) : mutant équivalent B_Bk/Res dans B5, à rouvrir avec le corridor (J6, P116) ; nullités de Res (H) et de ξ déclarées non calculées dans `GRANDEURS_NULLES` → J3-d1, rang 5 (faites, P121, `ea2e0da`) ; deux appels de `besoin_d_emission` par pas (bloc d'essai 9) → #132.

**Dépendances ajoutées** (14/11/2026, après la PR #129) : #103 (critère de M^G) → #132 ; J3-d1 → #101 ; #133 → #132 ; achèvement des blocs du socle → #106 ; branche de calibration → J3-e (état initial résolu et test zéro sur paramètres calibrés). **Retirées** : « module du bloc 9, issue à créer » (créée : #132) ; lignes renvoyées au module du bloc 9 → #132. **Inchangées** : #124 → blocs acheteurs réels ; #60 → #67 ; #131 → #114 ; celles de l'historique, partie C, § 3. **Ajoutées le 15/11/2026** : engagements de J3-d1 → #132 ; avis de `monnaie` sur la caisse des entreprises → #143 ; #141 → J4 (avec #70).

### 4. Décisions du mainteneur (extrait)

#### Décisions du mainteneur du 14/11/2026 au rang 1a de J3-d1 (P119 et suivants) et du 15/11/2026 (P142 et suivants)

P132 à P137 règlent la session des rangs 4 et 5 (mainteneur absent) ; P138, P139 et P141, prises par délégation, sont confirmées par P144. P142 à P146 : session du 15/11/2026 (rangs 6 à 8), mainteneur présent.

| N° | Décision |
|---|---|
| P119 | (Rang 1a de J3-d1, Q1 et Q7 de `macro`) Propriétaire de H1 déjà fixé : le moteur (M30, #61, `eq:moteur-croissance-nominale-attendue`) ; actes de forme : mention datée au § 9.1 de la fiche 5, critère de #60 à six labels, critère « Branche » à 76 labels (57 + 6 + 11 + 2) ; #67 ne dépend plus de H1. |
| P120 | (Q2) #124 par la **voie (a)** : domaine ≥ 0 (valeurs finies) sur chaque plan (C^plan, I^plan, G^plan), refus à l'écriture par exception typée, sans écrêtage ; condition : H5 lit max(0 ; D_H), E1 lit max(0 ; M^G) (#103) ; domaine des variables du pas annoté au rang 1b. Écartée : voie (b), qui laisse passer des signes mêlés. |
| P121 | (Q4) Grandeurs nulles **calculées** : Res (H) par test de signe (L^CB/S^CB ≥ 1e−6), ξ par égalité au bit de IN^vol_0 et IN\*_0, T_F et sa ligne 7 sur τ_F du bloc d'essai 9 ; remplacent la déclaration de `GRANDEURS_NULLES` (réserve de la revue finale de J3-c). |
| P122 | (Q5) Lignes (c) des fiches 5 et 6 **partagées** : J3-d2 (#132) pour celles qui portent sur une règle du bloc 9, #114 pour les propriétés du système fermé (test zéro, superneutralité, C36, rayon de la boucle). Précise P90. |
| P123 | (Q6) Lignes « Vitesses » des fiches 5 et 6 sur un banc à **prix endogènes** ; écart à 6 480 pas publié sans verdict. |
| P124 | (Q3 de `macro`, avis concordant de `monnaie`) Banc de stationnarité partielle de J3-d1 : **couverture des intérêts X4** ajoutée au bloc d'essai 9 (φ = 1 ; T_H = T_H du sentier + φ(i_CB − i_ref)(B − M^G − E^CB)/n_a), en **option de composition** dans `tests/` sur le précédent d'`emission_e3()`, jamais dans le banc de P87 (verdicts de P87 identiques au bit). Motif : sans elle, la maquette donne un rayon de 1,0012 ; 1,0053 ; 1,0160 à π\* = 0 ; 2 ; 10 % (canal rentier) ; avec, 0,9992 ; 0,9992 ; 0,9996. Réserves écrites avant l'essai : i_ref = (1 + r̄)(1 + π\*_t) − 1, π\* lu à l'ouverture, conversion linéaire /n_a ; assiette lue brute ; T^cou dans `GRANDEURS_NULLES` à 1e−12 S^G, calculé ; aucun critère d'arrivée sur 720 pas à 10 % pour les lignes à choc long (demi-vie de 1 799 pas : signe et délai seulement) ; nom X4, pas E4 (#133) ; option refusée sur un bloc 9 réel. Écartées : (ii) π\* = 10 % « non concluant » ; (iii) taux exogène. |
| P125 | (#103, `monnaie`) M^G sous la lecture nette : E1 lit max(0 ; M^G) (A8.2, déjà prescrit) ; **E6 (ii)** : M^G brut sous le max(0 ; ·) extérieur, exception déclarée ; **E9 et E4 : M^G brut**, exception d'identité sur le modèle d'E^Bk ; textes des l. ~3342, ~3356 et ~3194 de la spécification réécrits en correction prospective au passage de `docwriter` de J3-d1 (commit `docs:` de #103), ancien texte publié avec sa date ; code dans #132. |
| P126 | Écart à l'ADR 0012, A8.1 (E1 et H5 « exactes par construction », alors que p·(G^plan/p) ≠ G^plan dans environ 5,7 % des tirages, mesure de `monnaie` confirmée par la session : 0,0572 au-dessus, 0,0568 au-dessous sur 10^5 tirages) : **annotation de l'ADR 0013** au rang 1b, poussière d'un ulp admise sous la lecture nette (#103), comme pour D_H et D_F. Écartée : forme exacte de la ligne 2 et de H5. |
| P127 | (Rang 1b de J3-d1, Q1 d'`architect-approfondi`) Variables d'état qui retiennent une grandeur du pas : suffixe `_m1` partout (`YD_m1`, `y_m1`, `T_F_m1`), H1.1 complété. ADR 0013, annotation de J3-d1. |
| P128 | (Q2) ϱ̄_L : variable d'état d'`investissement`, recopiée de l'ouverture à chaque pas (phase 2), contrat C2 inchangé. Écartée : catégorie « constante résolue » d'`EtatPays`. |
| P129 | (Q3) Domaine des plans (P120) : liste fermée `DOMAINES_DU_PAS` du moteur, contrôlée à l'écriture pour tout écrivain, exception `PlanHorsDomaine`. Écartée : domaine porté par chaque écrivain. |
| P130 | (Rang 3 de J3-d1, Q1 de `macro`) Critère « Vitesses » de la fiche 5 : **verdict « non tenu » publié** (taux d'épargne nominal sur 12 tours, écart relatif après 720 pas entre λ_H × 0,5 et × 2 : 7,9e−6 ; 2,0e−6 ; 4,0e−8 à π\* = 0 ; 2 ; 10 %, seuil 1e−6) ; **correction prospective** du 14/11/2026, postérieure à l'observation et déclarée comme telle : taux d'épargne mesuré en **écart absolu ≤ 1e−6** (fraction du revenu), autres ratios inchangés en relatif, plus la propriété « écart divisé par au moins 100 entre 720 et 1 440 pas ». Motif : écart relatif pris sur un solde (amplification (C/YD)/s ≈ 49 à π\* = 0) ; aucun continuum (≤ 2,5e−12 à 2 160 pas). Écartées : (i) maintien en échec attendu ; (iii) horizon de 1 440 pas. |
| P131 | (Rang 3 de J3-d1, réserve r1 d'`audit`) Critère corrigé de P130 **jugé à π\* = 2 % seul**, comme le critère d'origine ; π\* = 0 et 10 % publiés sans verdict (P123), aucune extension après observation. Issue #138 (« `choc_pi_e` ignoré sans message quand le bloc 8 est réel ») créée sur accord. |
| P132 | (14/11/2026, mainteneur absent jusqu'à la session suivante) Périmètre de la session : **rangs 4 et 5 de J3-d1**, puis passation ; rangs 6 à 8 à la session suivante. |
| P133 | Délégation : une option (i)/(ii) recommandée par un agent et approuvée sans désaccord par l'expert pilote (`macro`, ou `monnaie` pour le crédit) est appliquée et consignée « P-n, par délégation, à confirmer », sauf désaccord entre agents, changement de résultat final ou contradiction avec un ADR ou une décision M-n : alors arrêt et passation. |
| P134 | Critère écrit avant l'essai non tenu sans erreur de code : critère d'un bloc (fiches 5 et 6) → verdict « non tenu » publié, échec attendu strict renvoyant à une issue créée, poursuite ; condition d'arrêt de la branche (stationnarité hors seuil, y compris à π\* = 10 % seul ; instabilité ; arrêt du noyau ; part d'un bloc > 0,48 ms) → arrêt et passation. |
| P135 | Issues proposées par les agents créées par la session (`needs-triage`), listées dans la passation. |
| P136 | Seconde reprise `coder` → `audit` accordée si les constats restants sont mineurs ou de forme, notée dans la PR ; constat bloquant ou majeur persistant → arrêt et passation. |
| P137 | Une consultation Fable au plus dans les cas du § 4.1 de `docs/agents/routage.md`, sans nouvel accord, notée dans la PR. |
| P138 | **Par délégation (P133), confirmée le 15/11/2026 (P144)** (rang 4 de J3-d1, constat M1 d'`audit`, recommandation de `monnaie`, pilote du crédit, sans désaccord) : domaine [0 ; 1] des entrées de scénario ς_L (et ς_B au bloc 9) contrôlé **par le moteur à leur publication en phase 0**, par refus typé sans écrêtage (table fermée des domaines des entrées, sur le modèle de `DOMAINES_DU_PAS`, P129) ; conforme à la spécification (l. ~2546, ~2634, dont le lieu du contrôle est à corriger au rang 6). Contrat partagé étendu : annotation de l'ADR 0013 à faire au rang 8 (faite : annotation du 15/11/2026). |
| P139 | **Par délégation (P133), confirmée le 15/11/2026 (P144)** (rang 4, Q3 de `coder`, recommandation de `macro`) : bornes (b) du bloc 6 lues « pour toute entrée dans le domaine déclaré » ; dépassement des exponentielles de S2, S3 et S6 refusé par un refus typé du moteur ; η_r, ζ ≤ 20 déclarés comme bornes de domaine de la table `investissement`. |
| P140 | (Rang 4, P134) Critère « Endettement, dépôts » de la fiche 6 non tenu (1,1e−5 à 2 160 pas, seuil 1e−6 ; convergence oscillante de module ≈ 0,997, 4,4e−16 à 12 000 pas) : échec attendu strict renvoyant à l'issue #139 ; correction prospective proposée par `macro` (max sur [4 320 ; 4 680] pas ≤ 1e−6, module ≤ 0,998) **réservée au mainteneur**. Boucle conjointe (b-x) en régime B : mesure publiée sans verdict (#114). λ_ti × 2 au-dessus du seuil à m = 0,8 : déjà publié par la fiche, reporté à #114. |
| P141 | **Par délégation (P133), confirmée le 15/11/2026 (P144)** (rang 5 de J3-d1, recommandations de `macro`, sans désaccord) : (a) le verdict du critère « Branche » se rend sur le banc **X4 seule** (lecture littérale de P124), X4 + E3 publié en contrôle ; les scénarios des fiches 5 et 6 (O2, G × 0,95) tournent sur X4 + E3 (précédent de P95), l'arrêt de X4 seule en O2 ~~(M^G < 0 au pas 3, émission d'essai figée)~~ *(précision du 15/11/2026, remesure de `coder`)* (sous G^plan × 1,05 seulement : M^G < 0 en phase 5, pas 3 à π\* = 0 et 2 %, pas 9 à 10 % ; aucun arrêt sous × 1,01 ; émission d'essai figée) publié comme fait du banc ; (b) B8, B25, B26, E^CB et le résidu de B19 restent des nullités déclarées (elles ne dépendent que de règles ; une déclaration à tort fait échouer le test, sens prudent), motif écrit au commentaire de `GRANDEURS_NULLES` ; (c) D_H publié aussi en mois de consommation, sans verdict. Intention de dimensionnement des bornes (c) de la fiche 6 et refus de la moitié du crédit : **réservés au mainteneur** (P140), issue #140. |
| P142 | (15/11/2026, validation du rang 6, constat M2) F1 porte un **second label** `eq:investissement-credit-servi` (crédit servi sous ς_L, ligne 18), balise dans `credit_servi` (`ed4c9c2`) ; concordance 76 → **77**. Correction du critère de décompte **avant son essai** (le décompte se juge à la concordance, après le rang 6) : critère de #67, « onze labels » → douze ; critère « Branche », 76 → 77 (§ 1) ; ADR 0013, annotation de J3-d1, point 8 (annotation du 15/11/2026) ; fiche 6, § 9.1 (mention datée). |
| P143 | (Même validation, constat m6) ζ s'écrit « 4 (hypothèse, indicative) » dans `tab:calibration`, avec la contrainte J3 et ses équivalents (`ed4c9c2`, `5e5662b`) ; calibration : #55 (branche de calibration, P115). |
| P144 | **P138, P139 et P141 confirmées** ; la mention « à confirmer » est levée (§ 4) ; P138 annotée dans l'ADR 0013 (contrat partagé étendu, annotation du 15/11/2026). |
| P145 | (Revue finale, constat M1 d'`audit`) Bornes (b) du bloc 6, **voie 2** : établies sur le lot \|Δϱ\| ≤ 0,1 par an (restriction déclarée ; `6e7db86`, `fc48f6e`) ; frontière de S6 publiée sans verdict par un test versionné (ti_{t+1} = 0 dès Δϱ = 3,307756 par an à ζ = 4, 0,661551 à ζ = 20 ; refus du domaine ti > 0 au-delà) ; P139 « pour toute entrée dans le domaine déclaré » se lit restreinte à ce lot jusqu'à #143. Borne de domaine du taux réel ou forme bornée de S2/S6 : **#143**, avec la question à `monnaie` sur l'arrêt antérieur du noyau à ζ = 4 (intérêts de la ligne 9 > D_F). Écartée : voie 1, borne de domaine posée dans la branche. |
| P146 | Issues créées sur accord : #141 (restitution du refus de crédit, J4), #142 (localité de la lecture nette), #143 (frontière de S6), #144 (travail redondant du chemin chaud), #145 (coefficient de richesse sur π\* de la table) ; commentaires versés sur #114 (lignes (c) des fiches 5 et 6), #131, #132 (engagements de J3-d1), #139 (banc de l'endettement), #141 (mesure de `macro`), #143 (frontière, question à `monnaie`). |

**Points ouverts au 15/11/2026, rang 8 de J3-d1** : #139 et #140 (réservées au mainteneur) ; #11 et #14 (hors branche) ; rattachement de #137 et #141 à #145 au point d'étape après J3-d1 ; résolution de l'état initial par `scenarios/` sans dupliquer le script (J3-e, § 2). Branches distantes `claude/cr-*` et `ccr-*` : supprimées (`git ls-remote --heads origin` au 15/11/2026 : `main` et la branche de travail seules).

### Complément sorti le 15/11/2026 au rang 1a de J3-d2 (branche `claude/j3-finances-publiques`, tête `142b556`, PR #146)

Sortis de `docs/feuille-de-route.md` à `142b556` pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé, titres décalés d'un niveau. Les décisions P147 à P155 restent dans la tête (§ 4), seules les questions Q1 à Q10 qui les fondent sont ici.

### En-tête (extrait : mises à jour de la tête du 15/11/2026, rang 8 de J3-d1 et rang 0 de J3-d2)

**Dernière mise à jour** : 15/11/2026, point d'étape après la fusion de la PR #136, rang 0 de J3-d2 (`architect-approfondi`) — `main` = `30078bb` (commit de fusion, parents `731aac3` et `1e7f736`) ; branche de travail `claude/j3-finances-publiques`, créée depuis `30078bb`, sans PR à cette date ; J3-d1 consignée (§ 2, § 6, § 7) ; plan de J3-d2 proposé (§ 1) ; questions Q1 à Q10 tranchées le même jour par le mainteneur (P147 à P155, § 4) ; PR brouillon #146 ; fiche de J3-d1, relevé du 14/11/2026 après la PR #129, P119 à P146 sortis vers l'historique, partie E (P76).

**Mise à jour précédente** : 15/11/2026, rang 8 de J3-d1 (consignation avant la sortie du brouillon, `architect`) — `main` = `731aac3` ; branche `claude/j3-menages-investissement`, tête `414a8a4` (PR #136) ; état au § 1 ; décisions P142 à P146 au § 4 ; P100 à P118 sortis vers l'historique, partie D (#119, P76). Mises à jour plus anciennes : historique, partie E, en-tête, puis partie D, en-tête, puis historique de Git (`git log -- docs/feuille-de-route.md`).

### 1. Branche de travail en cours (extrait : classement proposé au rang 0 de J3-d2, arrêté au rang 1a par P155 et P160 à P162)

**Classement proposé des lignes « J3 » du § 9.6 de la fiche 9** (proposition d'`architect`, à confirmer ou corriger par `macro` au rang 1a ; aucune ligne n'a été essayée) :
- (a) exigées dans la branche : état stationnaire (critère 4), cas à la main (critère 1), parts non payées (critère 12), caisse (critère 11), lecture nette, neutralité de m et de s_CB (C59), couverture (E4, C45), bornes (critère 16), phases et empreinte (critères 2 et 19), coût (critère 20) ;
- (b) publiées sans verdict : racine (C51), θ_H (C52), pays joué (C62) ;
- (c) renvoyées : test zéro (critère 15) → J3-e ; vitesses et arrivée (critère 7) et stabilité sur le moteur (critère 8) → #114 et J3-f (S1, S2) ; « −2 points » (#55) et calibration (critère 22) → branche de calibration ; critère 13 de la fiche 8 → #80, échec attendu inchangé.

### 2. Branches suivantes (extrait : lignes 7 à 9, branches fusionnées)

| Ordre | Branche | Issues | Motif du regroupement et état |
|---|---|---|---|
| 7 | J3-b `claude/j3-economie-reelle` | #112, #113, #50, #51, #104 | **Fusionnée le 14/11/2026** (PR #117, `688f299`) : § 7. |
| 8 | J3-c `claude/j3-monnaie` | #119, #121, #61, #91, #90 avec `Closes` ; #80 sans `Closes` | **Fusionnée le 14/11/2026** (PR #129, `731aac3`) : § 7. |
| 9 | J3-d1 `claude/j3-menages-investissement` | #124, #60, #67, #123, #103 ; rattachés : domaine de K et table du bloc 6 (P80), lignes (c) des fiches 7 et 8 à un bloc près (P90) | **Fusionnée le 15/11/2026** (PR #136, `30078bb`) : § 7. |

### 4. Décisions du mainteneur (extrait : introduction des M-n ; questions Q1 à Q10 du 15/11/2026)

M1 à M19 sont datées du 29/09/2026, M20 à M23 du 30/09/2026, M24 du 02/10/2026, M25 à M30 du 03/10/2026, toutes arrêtées par le mainteneur. M1 à M15 sont consignées dans l'ADR 0001 (§ Décision, point de même numéro) ; M16 dans l'ADR 0003 ; M17 précise M6 dans l'ADR 0001 ; M18 à M21 n'ont pas d'ADR (règles de procédure) ; M22 est consignée dans l'ADR 0005 (accepté le 30/09/2026) et dans la fiche `docs/blocs/temps_comptabilite.md` § 8 ; M23 est consignée dans l'ADR 0006 ; M24 est consignée dans la fiche `docs/blocs/production.md` § 8 et, pour sa lecture (b) qui modifie un contrat partagé, dans l'ADR 0007 (accepté le 02/10/2026, qui complète l'ADR 0005 sans le réécrire). M25 et M26 sont consignées dans les fiches `docs/blocs/travail.md` § 8 et `docs/blocs/prix.md` § 8 et, pour les deux contrats partagés qu'elles modifient (conversion des taux de croissance et d'inflation ; phase de l'indice des prix), dans l'ADR 0008 (proposé puis accepté le 03/10/2026, avec son point II.3 ; il révise en partie l'ADR 0005, annotation datée de celui-ci). M27 et M28 sont consignées dans les fiches `docs/blocs/menages.md` § 8 et `docs/blocs/investissement.md` § 8 ; M29 dans l'ADR 0009 ; M30 dans l'ADR 0010. La forme canonique du numéro est `Mn` (`M16`), citée telle quelle dans les fiches comparatives, la spécification (provenance des équations, `CONVENTIONS.md` § 2.3) et les issues ; « M-n » désigne une décision quelconque dans la prose. Trois décisions de mise en œuvre sont consignées par annotation d'ADR sans numéro (elles ne changent aucune décision numérotée) : garder `outils/compiler_specification.sh` (29/09/2026, ADR 0004, pt 4) ; déclarer le hook `preparer_latex.sh` en `SessionStart` (29/09/2026, ADR 0004, pt 5) ; règle 4 de la concordance, une décision par mention, le pluriel « décisions M3 et M16 » et la forme groupée « (M3, M16) » restant refusés (30/09/2026, ADR 0004, pt 6, et `CONVENTIONS.md` § 9).

#### Questions au mainteneur du 15/11/2026 (point d'étape après la PR #136) et décisions P147 à P155

Posées par `architect-approfondi` au rang 0 de J3-d2 (`6e8b9e2`) ; tranchées par le mainteneur le 15/11/2026, toutes selon l'avis d'`architect` (tableau des décisions sous celui des questions).

| N° | Question | Options | Avis d'`architect` |
|---|---|---|---|
| Q1 | Périmètre de J3-d2 avec `Closes` | (a) #133, #132, #106, #101, #134 (P113) ; (b) #142 à la place de #101, #101 renvoyée à la calibration ; (c) ajout de #143, #139 ou #140 (six issues ou plus, hors de la règle des trois à cinq) | (a) : aucun fait nouveau ne rouvre P113 ; la localité de la lecture nette est imposée au bloc 9 par un critère de #132, si bien que #142 n'a plus qu'à l'étendre aux blocs 5 et 6 (Q5). |
| Q2 | #143 (frontière de S6) : entrée dans J3-d2 et voie | (0) statu quo jusqu'au J4 : restriction \|Δϱ\| ≤ 0,1 par an déclarée (P145), arrêt diagnostiqué au-delà ; (1) borne de domaine du taux réel du crédit, liée au domaine du levier de taux (J4) ; (3) forme bornée de S2 ou de S6, qui **rouvre M28** (décision M-n nouvelle citant M28, fiche 6 rouverte, circuit 1) | **Hors J3-d2** : bloc 6, et non bloc 9 ; aucune trajectoire prévue en J3 n'approche la frontière (Δϱ ≈ 13,23/ζ par an, soit 3,31 à ζ = 4 et 0,66 à ζ = 20, contre 0,02 pour le critère « −2 points ») ; la question à `monnaie` sur la caisse des entreprises n'a pas de réponse. Sur le fond, sans trancher : (1) au J4, parce qu'à ζ = 4 le noyau refuse déjà le pas dès i_{L,0} ≈ 3,25 par an, avant la frontière de S6 (≈ 3,42) : une forme bornée de S6 seule n'y élargirait pas le domaine (*hypothèse* tirée des mesures de #143, non remesurée) ; (3) à instruire si ζ calibré (#55) rapproche la frontière d'une plage plausible. Instruction : avis de `monnaie` et de `macro`, hors branche, avant la branche de calibration. |
| Q3 | #139 (critère « Endettement, dépôts » de la fiche 6, P140) | (i) correction de `macro` : maximum de l'écart sur [4 320 ; 4 680] pas ≤ 1e−6 et module ≤ 0,998 par pas entre 1 440 et 4 320 pas ; (ii) horizon en demi-vies de la racine dominante, H = 20 demi-vies (règle du critère 7 de la fiche 9 et de C36 (ii-b)), sur la valeur propre publiée 0,99720 : demi-vie 247,2 pas, H ≈ 4 944 pas ; (iii) échec attendu maintenu, critère rejugé sur le socle complet (banc sans blocs d'essai de banque et de banque centrale, remarque de `macro` du 15/11/2026) | (ii), jugé sur le socle complet comme en (iii) : une règle déjà écrite ailleurs plutôt qu'une fenêtre choisie après observation ; la correction reste postérieure à l'observation et se déclare comme telle (précédent P130), l'ancien verdict publié ; exécution en J3-e avec #114. |
| Q4 | #140 (bornes (c) de la fiche 6, P141) | (i) retirer « dimensionné pour… » ou le reporter sur le refus de crédit ; (ii) scénario adverse dimensionné par un calcul à la main fait avant l'essai ; dans les deux cas, test du refus de la moitié du crédit (C31) | (i), report sur le refus de crédit : #124 refuse G^plan < 0 et l'extrapolation de #140 (non mesurée) suggère qu'aucun choc sur G seul n'annule I^plan ; (ii) coûte un calcul qui ne se vérifie qu'à l'essai. Exécution en J3-e avec #114. |
| Q5 | #137, #142, #144 (forme du code) | (a) branche technique `claude/j3-forme-du-code`, circuit 3 (workflow `circuit-technique`), après J3-d2 et avant la calibration ; (b) #137 en correctif rapide dès maintenant, #142 et #144 en (a) ; (c) les trois en J3-g (budget) | (a) : trois issues sans effet sur les trajectoires, mêmes modules (ordonnanceur ; blocs 2, 5 et 6), mesure P57 avant / après sur le socle complet, une fois le bloc 9 écrit ; #137 n'est pas un correctif rapide au sens strict si un test des messages l'accompagne (deux domaines). Insère une branche entre J3-d2 et la calibration (P115) : accord requis. |
| Q6 | #141 et #145 | #141 → J4 avec #70 ; #145 → J4 avec le levier de cible (#54) | Confirmer : ni l'une ni l'autre ne touche une trajectoire de J3. |
| Q7 | Délégation pour J3-d2 | (a) reconduire P118 (délégation technique) et P133, P134, P136, P137 ; (b) P118 seule | (a) : appliquées sans incident en J3-d1 (P144 confirme P138, P139, P141) ; les critères de fiche et les résultats finaux restent au mainteneur. |
| Q8 | ADR 0013 : 78 697 octets (`wc -c`), dont état consolidé 38 865 octets (Contexte à Conséquences, sous le plafond de 40 ko de P97) et annotations ≈ 39,8 ko | (a) annotation du rang 1b de J3-d2 dans l'ADR 0013, reconsolidation par un ADR nouveau au point d'étape après J3-d2 ; (b) reconsolidation avant le rang 1b ; (c) en J3-g | (a) : les tables des neuf blocs ne sont complètes qu'après J3-d2 ; reconsolider avant obligerait à le refaire. L'ADR nouveau serait un ADR d'architecture (cas Fable du § 4.1 de `docs/agents/routage.md`), à décider alors. |
| Q9 | Plan de J3-d2 (§ 1) : rangs, critères, conditions d'arrêt, classement proposé du § 9.6 | approuver ; amender | Approuver ; le classement est confirmé ou corrigé par `macro` au rang 1a, avant tout essai. |
| Q10 | Rappel : #11, #14 (mainteneur, hors branche) | — | Sans décision. |

**Points ouverts au 15/11/2026, après la fusion de la PR #136** : rang 1a de J3-d2 ; instruction de #143 (P148) ; #11 et #14 (Q10) ; résolution de l'état initial par `scenarios/` sans dupliquer le script (J3-e, § 2) ; découpage de J3-e à J3-g au point d'étape après J3-d2 (P61).

### 8. Escalades, relances et arrêts hors branche (extrait : lignes du 14/11/2026 ; ligne du 15/11/2026, rang 0 de J3-d2, sortie au rang 1b)

| Date | Fiche / modèle / critère déclenché / statut obtenu / suite |
|---|---|
| 14/11/2026 | Point d'étape après la PR #117 (plan de J3-c) / `architect` / Opus / seuil § 4.3 atteint par P76 (b) (remplacement de l'ADR 0012 comme document de lecture) / `revue requise`, P74 à P86 décidés le 14/11/2026 / Fable proposé et décliné par le mainteneur ; budget Fable de J3-c : 0 sur 3. |
| 14/11/2026 | Point d'étape après la PR #129 (découpage de J3-d, plan de J3-d1) / `architect-approfondi` / Opus `high` (mission de jugement, P85) / aucun seuil § 4.3 atteint (annotation de l'ADR 0013 renvoyée au rang 1b de J3-d1) / `revue requise`, Q1 à Q9 (§ 4) / aucune consultation Fable ; budget prévu pour J3-d1 : 0 sur 3. |
| 15/11/2026 | Point d'étape après la PR #136 (plan de J3-d2, rang 0) / `architect-approfondi` / Opus `high` (mission de jugement, P85) / aucun seuil § 4.3 atteint (annotation de l'ADR 0013 renvoyée au rang 1b de J3-d2, reconsolidation en Q8) / `revue requise`, Q1 à Q10 (§ 4) / aucune consultation Fable ; budget prévu pour J3-d2 : 0 sur 3 ; décisions P147 à P155 ; reportée dans la PR #146.

### Complément sorti le 15/11/2026 au rang 8 de J3-d2 (branche `claude/j3-finances-publiques`, tête `f1c8f2f`, PR #146)

Sortis de `docs/feuille-de-route.md` à `f1c8f2f` pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé, titres décalés d'un niveau. P147 à P155 restent en vigueur ; P156 à P165 restent dans la tête (§ 4).

### En-tête (extrait : mises à jour de la tête du 15/11/2026, rangs 0 et 1a de J3-d2)

**Dernière mise à jour** : 15/11/2026, rang 1a de J3-d2 (`architect`) — branche `claude/j3-finances-publiques`, tête `142b556` (PR #146) ; lectures de `macro-approfondi`, `monnaie` et `jeu` consignées au § 1 (classement du § 9.6 arrêté, critères précisés avant tout essai) ; décisions P156 à P164 (§ 4) ; questions Q1 à Q10, classement proposé et mise à jour du rang 8 de J3-d1 sortis vers l'historique, partie E (P76).

**Mise à jour précédente** : 15/11/2026, point d'étape après la fusion de la PR #136, rang 0 de J3-d2 (`architect-approfondi`) — `main` = `30078bb` ; P147 à P155 (§ 4). Texte complet et mises à jour plus anciennes : historique, partie E, en-tête, puis partie D, en-tête, puis historique de Git (`git log -- docs/feuille-de-route.md`).

### 1. Branche de travail en cours (extrait : surface d'impact documentaire notée au rang 1a de J3-d2)

**Surface d'impact documentaire notée au rang 1a** (pour `docwriter` au rang 6, sans décision) : fiche 9, § 9.1, 9.4, 9.6 en retard sur la spécification (E12 en phase 7 ; E13 à deux parts ; m → ν_G ; neutralité 1,1 → 1,2 ; condition des intérêts impayables de `sec:finances_publiques`) ; `\limites` de ς_B sous Em < 0 (P159).

### 2. Branches suivantes (extrait : ordre des modules de J3-b à J3-d)

Ordre des modules : J3-b (blocs 2 à 4) → J3-c (blocs 7, 8 et #61) → J3-d (blocs 5, 6 et 9) (P41 (a)), découpée en J3-d1 (blocs 5 et 6) puis J3-d2 (bloc 9) (P111) ; π\*_t est écrite par le bloc 8 (P34 (a)) et lue par les blocs 5 et 6. Le découpage de la queue de J3 (J3-e à J3-g) se fixe au point d'étape de J3-d (P61), soit après J3-d2 ; J3-e compte déjà plus de cinq sujets.

### 3. Issues hors plan (extrait : lignes du relevé du 15/11/2026 regroupées au rang 8 de J3-d2, et points ouverts sans issue)

| #101 | Test de source de `sec:investissement-taux` | **J3-d2, rang 2** (P113) | J3-d1 fusionnée : la dépendance est levée |
| #106 | Consommateur de `variation_sur_le_tour` | **J3-d2, rang 4** (P51) | retrait sauf consommateur déclaré, constaté après #132 |
| #132 | Module du bloc 9 `finances_publiques.py` | **J3-d2, rangs 1a, 3 et 6** (P113) | six engagements de J3-d1, lignes (c) (P90, P122), double appel de `besoin_d_emission` |
| #133 | Collision E1–E3 / E1–E13 | **J3-d2, rangs 2 et 6**, avant #132 (P114) | X1 à X3, X4 déjà nommée (P124) |
| #134 | Encadré des vitesses, mentions de `scenarios/` | **J3-d2, rang 6** (P113) | `docwriter` seul |

**Points ouverts sans issue** : mutant équivalent B_Bk/Res dans B5, à rouvrir avec le corridor (J6, P116) ; deux appels de `besoin_d_emission` par pas (bloc d'essai 9) → #132 ; résolution de l'état initial par `scenarios/` sans dupliquer le script (J3-e, § 2) ; taille de l'ADR 0013 (Q8).

### 4. Décisions du mainteneur (extrait : P147 à P155, points ouverts du rang 1b de J3-d2)

| N° | Date | Décision | Question |
|---|---|---|---|
| P147 | 15/11/2026 | Périmètre de J3-d2 avec `Closes` : #133, #132, #106, #101, #134 (P113 maintenue). | Q1 (a) |
| P148 | 15/11/2026 | #143 hors de J3-d2 ; voie retenue : borne de domaine du taux réel du crédit, liée au domaine du levier de taux (J4) ; instruction par `monnaie` et `macro` hors branche, avant la branche de calibration ; M28 n'est pas rouverte. | Q2 (1) |
| P149 | 15/11/2026 | #139 : critère « Endettement, dépôts » de la fiche 6 corrigé par un horizon de 20 demi-vies de la racine dominante (valeur propre publiée 0,99720, H ≈ 4 944 pas), jugé sur le socle complet ; correction postérieure à l'observation, déclarée comme telle (précédent P130), ancien verdict publié ; exécution en J3-e avec #114. | Q3 (ii) |
| P150 | 15/11/2026 | #140 : intention « dimensionné pour… » des bornes (c) de la fiche 6 reportée sur le refus de crédit ; test du refus de la moitié du crédit (C31) ; exécution en J3-e avec #114. | Q4 (i) |
| P151 | 15/11/2026 | #137, #142, #144 : branche technique `claude/j3-forme-du-code` (circuit 3), après J3-d2 et avant la branche de calibration, qu'elle précède (précise P115). | Q5 (a) |
| P152 | 15/11/2026 | #141 au J4 avec #70 ; #145 au J4 avec le levier de cible (#54). | Q6 |
| P153 | 15/11/2026 | Délégation pour J3-d2 : P118 (délégation technique), P133, P134, P136 et P137 reconduites ; critères de fiche et résultats finaux réservés au mainteneur. | Q7 (a) |
| P154 | 15/11/2026 | ADR 0013 annoté au rang 1b de J3-d2, puis reconsolidé par un ADR nouveau au point d'étape après J3-d2 (consultation Fable du § 4.1 à décider alors). | Q8 (a) |
| P155 | 15/11/2026 | Plan de J3-d2 (§ 1) approuvé ; le classement des lignes « J3 » du § 9.6 de la fiche 9 est confirmé ou corrigé par `macro` au rang 1a, avant tout essai. | Q9 |

**Points ouverts au 15/11/2026, rang 1b de J3-d2** : instruction de #143 (P148) ; #11 et #14 ; résolution de l'état initial par `scenarios/` sans dupliquer le script (J3-e, § 2) ; découpage de J3-e à J3-g au point d'étape après J3-d2 (P61) ; issue proposée par `jeu`, non créée (ou amendement de #82) : grandeurs du bloc 9 calculées hors interface au J4 ; durée d'une partie non fixée (#56).

### 7. Branches fusionnées (extrait : ligne de J3-c)

| Branche | PR | Jalon | Fusion | Détail |
|---|---|---|---|---|
| `claude/j3-monnaie` | #129 | J3 (J3-c) | 14/11/2026, 17:44 UTC, commit de fusion `731aac3` (parents `6a22d39`, `6632dce`), par le mainteneur | Issues fermées par `Closes` : #119, #121, #61, #91, #90 (absentes du relevé du 14/11/2026 après la PR #129) ; #80 sans `Closes`, ouverte (échec attendu). 24 commits hors fusion (5 `code:`, 3 `tests:`, 16 `docs:` ; `git rev-list --no-merges 6a22d39..6632dce`). Rangs et SHA : historique, partie C, § 1, et corps de la PR #129. Décisions : P74 à P110. Fable : 0 sur 3. Premiers résultats du moteur pour les blocs 7 et 8, aucun résultat final ; `tests/references/` intact. Concordance : 57 labels. Issues nées de la branche : #130 à #135. |

## Partie D : extraits de la tête sortis le 15/11/2026 (rang 8 de J3-d1), figés

Sortis de `docs/feuille-de-route.md` à `414a8a4` (branche `claude/j3-menages-investissement`, PR #136, rang 8 de J3-d1), pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé, titres décalés d'un niveau. Les numéros P-n restent stables ; ces décisions restent en vigueur tant qu'aucune décision ultérieure ne les remplace.

### En-tête (extrait : mises à jour de la tête du 13/11/2026 au 14/11/2026, rang 9 de J3-c)

**Mise à jour précédente du même jour** : 14/11/2026, rang 9 de J3-c (consignation de fin de branche) — `main` = `6a22d39` ; branche `claude/j3-monnaie`, tête `aebbd1d` ; rangs 2 à 8 faits ; décisions P100 à P110 (§ 4) ; ADR 0013, annotation de consignation du 14/11/2026 ; P74 à P86 et branches fusionnées jusqu'à J3-a sorties vers l'historique, partie B (P76).

**Mise à jour du même jour** : 14/11/2026, rangs 1a et 1b de J3-c — `main` = `6a22d39` (fusion de la PR #128) ; **branche de travail** `claude/j3-monnaie`, tête `3aca87b` (`main` fusionnée) ; décisions du mainteneur P87 à P99 du 14/11/2026 sur le rang 1a, l'avis de `jeu` sur #80 et l'ADR 0013 (§ 4) ; annotation de forme de J3-c dans l'ADR 0013.

**Autre mise à jour du même jour** : 14/11/2026, rang 0 de J3-c (`d246c28`) : point d'étape et plan, P74 à P86, condensation de la tête (#119, P76).

**Mise à jour précédente** : 13/11/2026, consignation du rang 10 de J3-b (tête de branche `ce7c619`), version figée dans l'historique, partie A. Versions plus anciennes : historique de Git (`git log -- docs/feuille-de-route.md`).

### 1. Branche de travail en cours (extrait : plan de J3-d1, rangs 0 à 8)

#### Plan proposé pour J3-d1 « ménages et investissement » (`claude/j3-menages-investissement`) — domaine des plans (#124), ménages (#60), investissement (#67), labels de d et tu (#123), signes sous lecture nette (#103)

*Proposé par `architect-approfondi` le 14/11/2026 (point d'étape après la PR #129) ; **décidé** par le mainteneur le même jour (P111 à P118, § 4).*

- **Découpage de J3-d** (P85, P111) : J3-d1 (blocs 5 et 6), puis J3-d2 (bloc 9, § 2). Motifs : le propriétaire de H1 se fixe avec la fiche 6 (#60) et #67 dépend de #60 ; le bloc 9 lit les assiettes des blocs 3 à 7 et clôt le bouclage, il vient donc sur les blocs 5 et 6 réels ; #124 précède tout plan écrit par un bloc acheteur réel (P84) ; #103 entière en J3-d1, si bien que la correction prospective du critère de M^G du bloc 9 (l. ~2961) est écrite avant l'essai de J3-d2.
- **Issues avec `Closes`** : #124, #60, #67, #123, #103 (P112). Rattachés sans issue propre : domaine strict de K et table du bloc 6 (P80) et lignes (c) des fiches 7 et 8 qui n'attendaient que le bloc 6 (P90), avec #67 ; nullités de Res (H) et de ξ déclarées non calculées dans `GRANDEURS_NULLES` (réserve de la revue finale de J3-c), au rang 5.
- **Délégation technique** : reconduite (P118). **Budget Fable** : 0 sur 3, aucune consultation prévue.

| Rang | Étape | Agent | Circuit |
|---|---|---|---|
| 0 | Consignation des décisions, PR brouillon ; amendements de #60 (H1), #67 (P80, P83, P90), #103 (M^G compris), #132 (lignes reçues, P90) | `architect`, session | `docs:` |
| 1a | Lectures avant le code : classement (a)/(b)/(c) des lignes « J3 » des § 9.6 des fiches 5 et 6, (c) → J3-d2 ou #114 ; P77 étendue aux fiches 5 et 6 ; propriétaire de H1 ; voie (a) ou (b) de #124 ; lecture de #103 (D_H et D_F : `macro` ; M^G : `monnaie`) ; critère de stationnarité partielle étendue ; décompte des labels | `macro-approfondi` (pilote) ; `monnaie` (crédit, dépôts, M^G) ; `jeu` si un indicateur visible change | 4 |
| 1b | Annotation de l'ADR 0013 : tables des blocs 5 et 6, domaine strict de K (P80), variables d'état des blocs 5 et 6 (version du schéma), domaine des plans si #124 suit la voie (a) | `architect-approfondi` | § 4.2 |
| 2 | #124 : domaine des plans et de d | `coder` → `audit` ; `macro` | 2 |
| 3 | #60 : `menages.py`, H1 à H7 | `coder` → `audit` ; `macro`, `monnaie` consulté | 1 |
| 4 | #67 : `investissement.py`, S1 à S7 et F1 à F4 ; #123 (labels de d et tu, P83) ; P80 ; lignes (c) à un bloc près (P90) | `coder` → `audit` ; `macro`, `monnaie` (crédit) | 1 |
| 5 | Mesures : stationnarité partielle étendue, verdicts des lignes (c), `GRANDEURS_NULLES`, parts P57 des blocs 5 et 6 sur la plateforme de référence | session ; `macro` | — |
| 6 | Passage unique de `docwriter`, un commit `docs:` par issue (#60, #67, #123, #103) ; labels et balises poussés ensemble (P62) | `docwriter` ; `macro` valide, `monnaie` pour M^G | règle 9 |
| 7 | Revue finale complète, `/code-review` | `audit`, `macro-approfondi` | règle 10 |
| 8 | Consignation (fiches 5 et 6 « implémentées »), validation, fusion | `architect`, mainteneur | — |

Ordre : #124 → #60 → #67 ; #123 avec #67 (S6 lit tu).

### 4. Décisions du mainteneur (extrait)

#### Décisions du mainteneur du 14/11/2026 après P99 (rangs 1b à 8 de J3-c ; P100 à P110)

Prises sur les points de forme de l'annotation du rang 1b, les comptes rendus des rangs 2 à 6 et la revue finale (commentaires de la PR #129), sans numéro M ; consignées au rang 9. Les libellés de la PR « D1 à D3 » et « C4 » se lisent P100 à P103 (sans lien avec les D1 à D13 de l'historique). Forme : ADR 0013, annotation de consignation du 14/11/2026.

| N° | Décision |
|---|---|
| P100 | (D1) Grandeurs nulles de P94 par **liste déclarée** (`GRANDEURS_NULLES`, 12 grandeurs, chacune avec sa raison), calculée en exact sur les paramètres, seuil absolu 1e−12 ; les autres au seuil relatif 1e−9 ; échec relatif publié à côté (i_D à π\* = 0, où r̄ = ϖ_D : 76,8 relatif, 6,7e−16 absolu). Aucun verdict ne change. Option écartée : seuil choisi après observation. `8209838`, `47c0205`. |
| P101 | (D2) **Continuum de r̂\*** propre au banc publié sans verdict (`docs/exigences.md` § 2.7) : r̂\* − r̄ au pas 2 159, à π\* = 2 %, choc +1 point : 1,5435 / 1,4550 / 1,3090 e−4 point à λ_e = 0,1 / 0,2 / 0,4 ; terme de Jensen de BC2 ; le niveau des prix revient au contrôle. Issue #131 créée (BC2 en log, mesure à #114). |
| P102 | (D3) Le « ratio de sacrifice » de P87 se nomme **coût en chômage d'un choc d'anticipations** de ±1 point (années-point de chômage par point de π^e_0, écart au contrôle apparié, banc sans canal du taux), publié à côté de 1/(λ_e λ_w β (1 + π\*)) (à λ_e = 0,2 : moyenne 2,5000 à π\* = 0, 2,4510 à 2 %, égale à la valeur analytique à la 4e décimale) ; seuil à #114 ; critère P87 inchangé. |
| P103 | (C4) Entrées de scénario ς_L et ς_B **au futur** dans la spécification, publiées avec les blocs qui les lisent (blocs 6 et 9, J3-d) ; levier de taux au futur dans `tab:phases` (lecture par le bloc 8 au J4). `9692b6f`, `f03a815`, `aebbd1d`. |
| P104 | (d2) de la fiche 7 (critère 13 (d)) traité dans la branche, par appel direct du bloc 7, publié sans verdict (aucun seuil) : +1,2606 point sur 12 tours, +1,0000 au tour 12, égal au script ; « +1,33 point en maquette » de la fiche : valeur d'illustration. Parts de ΔYD : #114. `83b7c23`. |
| P105 | Réserve R1 du socle partiel (`monnaie`, rang 4) : **refus confirmé**, plutôt qu'écrasement, et **étendu à tout paramètre des tables des blocs 7 et 8** (ϖ_L, ϖ_D, ϑ, a_π, a_I, λ_e, θ_CB, π\*, r̄) : une table de l'appelant hors du sentier est refusée (`TableHorsDuSentier`), faute d'appariement au script. Code de test. `83b7c23`. |
| P106 | Point de forme 1 : `Vue.glissement()` **refuse** un glissement tel que non (1 + π_{t−1} > 0), −1 exactement compris, et (visa de `monnaie`, rang 4) un glissement non fini ; jamais d'écrêtage ; règle déclarée dans `\limites` de BC3. `a3702ba`. |
| P107 | Point de forme 2 : **E^Bk calculé par le bloc 7 sur ses six positions d'ouverture**, brutes (L + B_Bk + Res − D_H − D_F − L^CB) ; H5.3 reste fermé ; test contre `valeur_nette_stock`. `bba1125`. |
| P108 | Point de forme 3 : **BC6 sous sa forme générale**, provisoire puis **confirmée par `monnaie`** au rang 4 ; forme « au socle » vérifiée par test. `a3702ba`. |
| P109 | Point de forme 4 : la « mention datée de E2 » désigne les mentions datées de P80 (relevé E2 d'`architect`, point d'étape du 14/11/2026). `b6cef67`. |
| P110 | Arbitrages techniques du rang 2 (session, délégation P86) : natifs dans la liste blanche, liste figée de 149 noms (Python 3.12), six admis (`float`, `int`, `str`, `tuple`, `min`, `max` ; `abs` et `bool` non admis) ; `REGISTRE` et `GRAND_LIVRE` admis ; importation d'un autre bloc refusée ; `math` admis importé entier seulement. `87897bc`. |

#### Décisions du mainteneur du 14/11/2026 au point d'étape après la PR #129 (P111 à P118) et au rang 1a de J3-d1 (P119 et suivants)

Questions Q1 à Q9 posées par `architect-approfondi` le 14/11/2026 ; Q1 à Q8 tranchées par le mainteneur le même jour, chacune selon la recommandation d'`architect` ; Q9 est un rappel, sans décision.

| N° | Décision |
|---|---|
| P111 | (Q1) Découpage de J3-d (P85) : **(a)** J3-d1 (blocs 5 et 6), puis J3-d2 (bloc 9). Écartés : (b) une branche par bloc ; (c) une branche au-delà de cinq issues. |
| P112 | (Q2) Périmètre de J3-d1 avec `Closes` : #124, #60, #67, #123, #103 ; #103 entière, critère de M^G compris (corrigé avant l'essai de J3-d2). |
| P113 | (Q3) Périmètre indicatif de J3-d2 : #132, #133, #106, #101, #134 ; #134 en J3-d2 (et non en J3-e) ; critères écrits au point d'étape après J3-d1. |
| P114 | (Q4) Bloc d'essai 9 **gardé** après #132 comme banc de P87, exigences renommées (#133). |
| P115 | (Q5) Branche de calibration (P43 (a)) **confirmée**, après J3-d2 et avant J3-e : #45, #55, #62, #92, #130. |
| P116 | (Q6) Mutant équivalent B_Bk/Res dans B5 : point ouvert (§ 3), rouvert avec le corridor (J6) ; issue au point d'étape qui précède le corridor. |
| P117 | (Q7) Fait nouveau de la passation de la PR #129 versé sur #131 en commentaire, sans conclusion. |
| P118 | (Q8) Délégation technique (P86) reconduite pour J3-d1. |

Les décisions P119 et suivantes, prises sous le même titre, sont restées dans la tête.

**Points ouverts au 14/11/2026, après la fusion de la PR #129** : #11 et #14 (Q9, mainteneur, hors branche) ; branches distantes `claude/cr-*` et `ccr-*` à supprimer par le mainteneur ; mentions « à numéroter » de la spécification remplacées par P100 à P102 au rang 9 de J3-c (`6632dce`) ; résolution de l'état initial par `scenarios/` sans dupliquer le script (J3-e, § 2).

### 7. Branches fusionnées (extrait : de `claude/correctif-litteral-12` à `claude/cr-statut-fiches`)

| Branche | PR | Jalon | Fusion | Détail |
|---|---|---|---|---|
| `claude/correctif-litteral-12` | #118 | hors jalon (correctif rapide avant J3-b, P50) | 13/11/2026, commit de fusion `02c1e1f` (parents `204ab2d`, `12e3dd3`) | #102 fermée (`12e3dd3`, `tests:` : aucun littéral 12 dans `src/` hors de la déclaration de n_a) ; `main` fusionnée dans J3-b (`d646fa8`). Aucun résultat changé. |
| `claude/j3-economie-reelle` | #117 | J3 (J3-b) | 14/11/2026, 07:47 UTC, commit de fusion `688f299` (parents `02c1e1f`, `4a2b67a`), par le mainteneur | Issues fermées par `Closes` : #112, #113, #50, #51, #104 (absentes du relevé du 14/11/2026). 44 commits hors fusion (12 `code:`, 12 `tests:`, 19 `docs:`, 1 `claude:` ; `git rev-list --no-merges 02c1e1f..4a2b67a`). Rangs et SHA : historique, partie A, § 1, et corps de la PR #117. Décisions : P49 à P73. Fable : 1 sur 3. Premiers résultats du moteur pour les blocs 2 à 4, aucun résultat final ; `tests/references/` intact. État à `4a2b67a` (passation de la PR #117) : unitaires 1423 passed, 1 skipped, 2 xfailed ; invariants 384 passed, 3 skipped ; concordance 40 / 40 ; matrices sans écart. Issues nées de la branche : #119 à #125. |
| `claude/cr-duree-maquette` | #127 | hors jalon (correctif rapide CR2, P75) | 14/11/2026, commit de fusion `5cc28d0` (parents `688f299`, `275a65e`) | #126 fermée (`275a65e`, `tests:`) ; `main` fusionnée dans J3-c (`70aaec6`). Aucun résultat changé. |
| `claude/cr-statut-fiches` | #128 | hors jalon (correctif rapide CR1, P75) | 14/11/2026, commit de fusion `6a22d39` (parents `5cc28d0`, `3bca91b`) | `fa395e6` (`docs:`), statut d'en-tête des fiches 1, 5, 6, 8 et 9 ; `main` fusionnée dans J3-c (`3aca87b`). Aucun résultat changé. |

## Partie C : extraits de la tête sortis le 14/11/2026 (point d'étape après la fusion de la PR #129), figés

Sortis de `docs/feuille-de-route.md` à `731aac3` (`main`, commit de fusion de la PR #129), pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé, titres décalés d'un niveau. Les numéros P-n restent stables ; ces décisions restent en vigueur tant qu'aucune décision ultérieure ne les remplace.

### 1. Branche de travail en cours (extrait : fiche de J3-c, à la fusion de la PR #129)

#### Branche J3-c « monnaie » (`claude/j3-monnaie`) — liste blanche (#121), cible et Γ^e (#61), banque centrale (#91), banque (#90), condensation (#119)

- **Branche** : ouverte depuis `main` à `688f299`. Issues avec `Closes` : #119, #121, #61, #91, #90 ; **#80 sans `Closes`** (instruction de C61 et avis de `jeu` ; le défaut subsiste et l'échec attendu y renvoie). #103 sort de J3-c pour J3-d (P74). Plan d'`architect` du 14/11/2026, décidé par le mainteneur (P74 à P86).
- **Correctifs rapides** (P75), **fusionnés le 14/11/2026** : CR2, test de durée de la maquette conjointe scindé en `test_deterministe` et `test_rapide` (issue #126, fermée ; PR #127, commit de fusion `5cc28d0`) ; CR1, statut d'en-tête des fiches 1, 5, 6, 8 et 9 aligné sur `docs/blocs/README.md` (PR #128, commit de fusion `6a22d39`). `main` fusionnée dans la branche : `70aaec6` (PR #127), `3aca87b` (PR #128).
- **Délégation technique** reconduite (P86) ; #11 et #14 attendent toujours le mainteneur.
- **Budget Fable** : 0 sur 3. P76 (b) atteint le seuil § 4.3 (remplacement de l'ADR 0012 comme document de lecture) ; Fable proposé et **décliné** par le mainteneur (consolidation sans décision nouvelle, contrôlée par relevé).

| Rang | Étape | Agent | Circuit | État |
|---|---|---|---|---|
| 0 | Consignation, PR brouillon ; amendements sur #91, #90, #61, #67, #103, #114 ; #119, volet feuille de route (tête ≤ 60 ko, historique) ; inventaire des blocs | `architect`, session | `docs:` | fait (`d246c28`) |
| 1a | Lectures avant le code : classement (a)/(b)/(c) des lignes « J3 » des § 9.6 des fiches 7 et 8, (c) → #114 ; P77 ; critères de stationnarité partielle et de la boucle T3 ↔ BC3 (P78) ; invariant π^e > −1 ; #125 point 1 (P79) ; corrections de la fiche 6 pour #61 ; C61 de #80 et avis de `jeu` | `monnaie-approfondi` (pilote) ; `macro` ; `jeu` (#80) ; mainteneur | 4 | **fait** : avis en commentaire de la PR #129 ; décisions P87 à P99 ; corrections prospectives des fiches 6, 7 et 8 (`bf76979`) ; condition (c) d'ouverture du levier de cible versée sur #54 (P99) |
| 1b | ADR 0013 de consolidation de l'ADR 0012 (#119, P76 (b)), document de lecture des trois contrats partagés (`docs/adr/0013-consolidation-de-l-adr-0012.md`), puis son annotation : nomenclature du schéma v3 (i_L, i_D ; r̂\*, π\* ; i_CB variable du pas ; forme de i_res ≡ i_CB, question 2 de la fiche 8), domaines, tables des blocs 7 et 8, `VERSION_SCHEMA` = 3 ; mentions datées de P80 | `architect-approfondi` (Opus `high`, § 4.2) | § 4.2 | **fait** : consolidation (`1531271`) ; annotation du 14/11/2026 de l'ADR 0013 (P96, P97) ; amendements sur #91, #90, #114, #67, #61 |
| 2 | #121 : liste blanche des importations d'un bloc (P81) | `coder` → `audit` | 3 | **fait** (`87897bc`) ; une reprise ; arbitrages P110 |
| 3 | #61 : schéma v3, tables, π\* (variable d'état du bloc 8 et paramètre), Γ^e en grandeur d'ouverture ; `facteur_g` en produit et Γ^e = `facteur_g`·f(π\*) (#125 point 1, P88) | `coder` → `audit` ; `monnaie` (et `macro` si #125) | 1 | **fait** (`0f4954c`, `c50be3f`, `4d0430f`) ; une seconde reprise ciblée accordée par le mainteneur |
| 4 | #91 : `banque_centrale.py`, BC1 à BC9, BC3 en forme convexe (P92) ; script aligné (P93) ; blocs d'essai E1, E2 (P95) | `coder` → `audit` ; `monnaie`, `macro` consulté | 1 | **fait** (`a3702ba`, `99eea4a`) ; une reprise ; BC6 générale confirmée (P108) |
| 5 | #90 : `banque.py`, B1 à B7 (B7 en −min) ; script aligné (P93) | `coder` → `audit` ; `monnaie`, `macro` consulté (crédit) | 1 | **fait** (`bba1125`, `7d90789`) ; une reprise ; maquette alignée sur B7 en −min (visas de `macro` et `monnaie`) |
| 6 | Mesures : stationnarité partielle étendue (P94), boucle T3 ↔ BC3 (P87), bloc d'essai E3 (P95), parts P57 des blocs 7 et 8 sur la plateforme de référence | session ; `monnaie` | — | **fait** (`8209838`) ; une reprise ; P100 à P102 |
| 7 | Passage unique de `docwriter` ; labels et balises poussés ensemble (P62) | `docwriter` ; `monnaie` valide | règle 9 | **fait** (`6d7dfa4`, `4b3a256`, `520dfce`, `2c4de6e`, `47c0205`) ; une relance de `monnaie` (limite de tours) |
| 8 | Revue finale complète, `/code-review` | `audit`, `monnaie-approfondi` | règle 10 | **fait** : corrections `83b7c23`, `f03a815`, `9692b6f`, `aebbd1d` ; P103 à P105 |
| 9 | Consignation (fiches 7 et 8 « implémentées »), validation, fusion | `architect`, mainteneur | — | consignation faite (présent commit) ; validation et fusion : mainteneur |

Ordre : #61 → #91 → #90 (BC1 lit π\* ; B1 et B2 lisent i_CB du bloc 8 ; la boucle T3 ↔ BC3 exige le bloc 8 réel).

**Critères d'acceptation, écrits avant l'essai** (boucle T3 ↔ BC3 : P87, écrit au rang 1a, avant toute mesure) :
- **#119** : relevé avant / après qui retrouve tous les P-n, M-n et D-n (commande citée dans la PR) ; tête de la feuille de route ≤ 60 ko ; document de lecture de l'ADR (ADR 0013) ≤ 40 ko ; concordance verte.
- **#121** : les six contournements connus (corps et commentaires de #121) refusés ; modules des blocs 2 à 4 admis sans modification.
- **#61** : π\*_{t+1} = π\*_t exactement à levier fermé ; Γ^e = [(1 + g)(1 + π\*)]^{1/n_a} par appel direct à 1e−15 relatif, calculé une fois en phase 0, après g ; forme exécutée `facteur_g`·f(π\*), `facteur_g` = f(g_pr)·f(g_N) (P88), trajectoires de la référence identiques au bit, tableau avant / après ; aucun bloc ne recalcule Γ^e (contrôle statique) ; reprise exacte en v3, sauvegarde v2 refusée.
- **#91** : lignes (a) et (b) du rang 1a aux seuils de la fiche 8, dont état stationnaire égal au script à 1e−10 (n_a = 12, π\* ∈ {0 ; 2 ; 10 %}, P77), L^CB_0 = M^G_0, Π^CB égal à 11c + 13 − 12 exécutées à 1e−12 × S^CB, **π^e > −1 tenu par BC3** sur tirages (0 < λ_e ≤ n_a, π^e_0 > −1, P > 0), i_CB égal à la prescription même négative ; BC3 en forme convexe, test de l'invariant sur 10^6 tirages à graine déclarée plus un lot adverse, glissement non tel que 1 + π_{t−1} > 0 refusé explicitement (P92 ; ADR 0013, annotation du 14/11/2026, point 4).
- **#90** : lignes (a) et (b), dont B7 en −min avec Res_{t+1} ≥ 0, L^CB ≥ 0 et Res·L^CB = 0 exactement, B5 égal aux lignes exécutées à 1e−12 × S^Bk, D_H et D_F lues en max(0 ; ·), état stationnaire égal au script (P77).
- **Branche** : stationnarité partielle à 1e−9 sur 720 pas aux trois π\*, blocs 2, 3, 4, 7 et 8 réels, étiquette « plans nominaux exogènes », liste étendue de P94 ; boucle T3 ↔ BC3 selon P87 ; concordance attendue à 57 labels (40 + 7 + 9 + 1, confirmé au rang 1b : ADR 0013, annotation du 14/11/2026, point 10) ; part de chaque bloc ≤ 0,48 ms (alerte publiée à 0,276 ms).

**Conditions d'arrêt** : contrat partagé à modifier au-delà de l'annotation du rang 1b ; drapeau de mode dans `src/` ; stationnarité partielle hors seuil sans erreur de code ; arrêt du noyau sur le sentier (Res < 0, caisse nette) ; boucle T3 ↔ BC3 hors de son critère ou instabilité connue réapparue ; part d'un bloc au-dessus de 0,48 ms ; chiffre publié non reproduit ; relevé de #119 incomplet.

**Verdicts** (critères écrits avant l'essai, non déplacés ; `8209838`) : **P87 tenu** sur tous ses critères (30 essais, aucun arrêt du noyau ; V1 ≤ 1e−15 ; V3 et V4 nuls exactement ; V5 au plus 1,57e−4 point pour ±0,1 ; V6 au plus 1,57e−5 pour 0,1 ; (c) au plus 4,9e−11 pour 1e−6 ; coût en chômage publié sans verdict, P102) ; **P94 tenu** aux trois π\*, grandeurs nulles lues selon P100 ; **P57 tenu** sur la CI de référence (exécution 43599918026, `7d90789`) : banque 0,0124 ms, banque centrale 0,0110 ms par pays-pas, pour 0,48 ms. Concordance : 57 labels.

**Effet sur les résultats** : premiers résultats du moteur pour les blocs 7 et 8 ; aucun résultat final, aucune référence ; #125 point 1 adopté (P88) : trajectoires de la référence identiques au bit sur 720 pas aux trois π\*, ~~écart au plus 5,6e−14 hors référence (mesure de `macro`, rang 1a)~~ *(correction prospective du 14/11/2026, réserve R1 de `macro`, tableau de `0f4954c`, 720 pas, g_N = 0,001, π\* = 0 ; 2 ; 10 %)* : variables d'état des blocs 2 à 4, écart relatif à leur propre valeur au plus 4,88e−14 ; 5,55e−14 ; 4,88e−14 ; positions, |Δ| rapporté à S du détenteur au plus 6,96e−14 ; 4,61e−14 ; 1,80e−14 ; V^flux, |Δ|/S au plus 6,98e−14 ; 4,59e−14 ; 1,84e−14 ; montants exécutés, |Δ|/max_s S au plus 1,3e−16 ; ξ (valeur résolue nulle) au plus 9,2e−15 en absolu ; script aligné sur B7 en −min et BC3 en forme convexe (P93), écart à l'arrondi, tableau avant / après ; critère 13 (#80) toujours en échec attendu.

**Escalades, relances et arrêts** : aucun aux rangs 0, 1a et 1b (Opus `high` aux rangs 1a et 1b, § 4.2, sans Fable) ; une reprise `coder` au rang 2 et au rang 3 (plus une seconde reprise ciblée accordée par le mainteneur au rang 3), une au rang 4, une au rang 5, une au rang 6 ; une relance de `monnaie` au rang 7 (limite de tours) ; aucune consultation Fable (budget : 0 sur 3). Le détail ligne à ligne est dans la PR.

### 3. Issues hors plan (extrait : relevé du 14/11/2026 après la PR #117)

*Relevé du 14/11/2026* (point d'étape après la fusion de la PR #117, `main` = `688f299`) : **49 issues ouvertes** (48 relevées par `list_issues`, plus #126 créée le même jour) ; #112, #113, #50, #51 et #104 fermées par la PR #117, #102 par la PR #118. Rattachements décidés par le mainteneur le 14/11/2026 (P74, P80 à P85). Relevés antérieurs : historique, partie A, § 3. La colonne « Branche prévue » n'est pas reportée sur GitHub.

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #10 | Registre d'exemptions de la concordance | hors plan | aucune exemption prévue |
| #11, #14 | Dependabot ; ruleset de `main` | mainteneur, hors branche | `ready-for-human` depuis le 30/09/2026 |
| #37 | Aucun levier d'offre au socle | J4, au plus tard J7 | M26, M28 |
| #45, #55, #62, #92 | Calibrations de λ_w, de la fiche 6, de ν_H et λ_H, de μ̄ | calibration (P43 (a)) | #55 recoupe #92 |
| #130 | Calibration de ϖ_L, ϖ_D, ϑ et r̄ (fiches 7 et 8, critères 17 et 23) | calibration (P98) | créée le 14/11/2026 |
| #46, #47, #48 | Okun ; prix administrés ; levier de répartition | J4 (#47 puis J7) | inchangé |
| #52, #53, #63, #70, #79, #81, #82 | Restitutions et scénarios O2, O3 | J4 | inchangé |
| #54, #56 | Aller-retour de π\* ; signe net d'une hausse de taux | J4, sans `Closes` | #54 garde la mesure de Fisher de #61 et la condition (c) d'ouverture du levier de cible (P99) |
| #57 | Crises de crédit sous la règle F | J6 | inchangé |
| #60, #67 | `menages.py`, `investissement.py` | J3-d | après #61 et #91 ; #67 reçoit domaine de K, table du bloc 6 (P80), labels d et tu (P83), lignes (c) des fiches 7 et 8 à un bloc près (P90) |
| #61 | π\* et Γ^e | **J3-c, rang 3, `Closes`** | `facteur_g` en produit (P88) |
| #64 | S-ζ hors cible durable | J5 | inchangé |
| #78, #89 | Coût de la dette ; stratégie dominante | J4 (#78 puis J6) | #89 dépend de #88 |
| #80 | Superneutralité (critère 13 de la fiche 8) | J3-c, sans `Closes` ; instruction faite | voie (c) de M32 maintenue, aucune source traitée seule, échec attendu conservé (P89) ; condition (c) du levier de cible sur #54 (P99) |
| #87, #88, #111, #116 | D_F ≥ 0 hors stationnaire ; fenêtre longue ; trajectoires C-HS ; maquette | J3-f (P42, P60) | #116 → #111 |
| #90 | `banque.py` | **J3-c, rang 5, `Closes`** | après #121 ; part du bloc 7 de #103 (critère 4) ; lignes (c) → J3-d ou #114 (P90) |
| #91 | `banque_centrale.py` | **J3-c, rang 4, `Closes`** | après #121 et #61 ; lignes (c) → J3-d ou #114 (P90) |
| #101 | Test de source de `sec:investissement-taux` | J3-d | `monnaie` |
| #103 | Signes sous lecture nette (D_H, D_F, M^G) | J3-d (P74) | contraintes des blocs 5, 6 et 9 |
| #106 | Consommateur de `variation_sur_le_tour` | J3-d (P51) | fermeture par retrait, sauf consommateur déclaré |
| #108 | Identifiants Cn et Co | J5 | P46 (a) |
| #110 | Processeur de l'exécuteur en CI | J3-g (P60) | C = 0,2922 contre 0,4291 ms selon l'exécuteur |
| #114 | Critère I1 : lignes « J3 » au socle complet | J3-e | reçoit les lignes (c) des fiches 7 et 8 qui exigent le socle complet (P90) |
| #115 | Radical `observation` | J3-e | → premier label `eq:observation-…` |
| #119 | Condensation de la feuille de route et de l'ADR 0012 | **J3-c, rangs 0 et 1b, `Closes`** | P76 (b) |
| #120 | `Cadre` à n_a ≠ 12 | J3-e (P82) | option (a), refus à l'assemblage |
| #121 | Contrôle statique : liste blanche | **J3-c, rang 2, `Closes`** | P81 (b) |
| #122 | IN^vol = 0 ⇒ IN = 0 à l'état chargé | J3-e (P84) | `scenarios/` et reprise |
| #123 | Définitions exécutées non numérotées | J3-d (P83) | option (a) : labels de d et tu, avec #67 |
| #124 | Domaine de d ≥ 0 | J3-d (P84) | avant les blocs acheteurs réels |
| #125 | Facteur de croissance par pas, formes divergentes | point 1 : adopté (P88), réalisé avec #61 au rang 3 de J3-c ; point 2 : J3-f ; points 3 à 6 : J3-e (P84) | sans `Closes` en J3-c |
| #131 | BC2 en log : terme de Jensen de r̂\* | #114 (mesure), J3-e | créée le 14/11/2026 (P101) |
| #126 | Test de durée de la maquette conjointe | correctif rapide CR2 (PR #127) | créée le 14/11/2026 |

**Dépendances ajoutées** (14/11/2026) : #125 point 1 → #61 ; #121 → #90, #91 ; instruction de #80 → #67 ; rang 1a de J3-c → tout essai de J3-c ; #119 → rang 1b ; lignes (c) de #90 et #91 → #114 (*précisé le 14/11/2026, P90* : celles qui exigent le socle complet ; les lignes à un bloc près vont à J3-d) ; domaine de K et table du bloc 6 → #67. **Ajoutées le 14/11/2026, rang 1a** (P90, P98) : lignes (c) des fiches 7 et 8 à un bloc près → #67 (bloc 6) et module du bloc 9 (J3-d) ; #130 → branche de calibration. **Retirées** : #103 de J3-c (« #103 avec #90 ») ; « position K en J3-c » (P80) ; pour ces lignes à un bloc près, « lignes (c) → #114 » (P90) ; « instruction de #80 → #67 », instruction faite (P89). **Ajoutées le 14/11/2026, rang 9** : #131 → #114 (mesure du terme de Jensen, P101) ; lignes renvoyées au module du bloc 9 (placement raté, C60, lecture de Π^CB en 8b pour E1) → issue du bloc 9, à créer (J3-d). **Inchangées** : celles des 15/10 et 13/11/2026 (historique, partie A, § 3).

### 4. Décisions du mainteneur (extrait)

#### Décisions du mainteneur du 14/11/2026 (rang 1a de J3-c, avis de `jeu` sur #80, ADR 0013 ; P87 à P99)

Prises sur la synthèse du rang 1a (`monnaie-approfondi`, pilote, et `macro-approfondi` ; commentaire de la PR #129 du 14/11/2026) et sur l'avis de `jeu` sur #80, sans numéro M. Consignées au rang 1b de J3-c ; la forme est dans l'ADR 0013, annotation du 14/11/2026.

| N° | Décision |
|---|---|
| P87 | **Critère de la boucle T3 ↔ BC3 (P78), écrit avant l'essai** : fusion des critères de `monnaie` et de `macro`. Banc : socle partiel d'essai, blocs 2, 3, 4, 7 et 8 réels, plans nominaux exogènes ; n_a = 12, ν_G = 1,15, π\* ∈ {0 ; 2 ; 10 %} ; choc de ±1 point sur π^e_0 injecté à l'ouverture, avec un contrôle apparié sans choc ; dans la série de `monnaie`, en plus, un choc G^plan × 1,01 aux tours 1 à 12. **Communs** : délai et signe de π^e_1 à 1e−15 ; r̂\*_T − r̂\*_0 = (a_I/n_a) · Σ(π_{t−1} − π\*) à 1e−12 ; π^e > −1 et aucun arrêt du noyau. **Sur 720 pas** (`monnaie`) : V1, BC3 du moteur égal à une implémentation de référence à 1e−15 ; V2, délai de deux tours ; V3, i_CB − i^règle = 0 exactement ; V4, Res · L^CB = 0 exactement à chaque clôture ; V5, moyennes des pas 660 à 719 dans les bandes de `tab:criteres-j3`, B3 à ±0,5 point, B7, B8, B9 et B25 à ±0,1 point ; V6, max_{600 ≤ t < 720} \|x\| ≤ 0,1 × max \|x\| pour x1 = π^e − π\* (point de % par an, ouverture), x2 = P_t/P_{t−12} − 1 − π\* (point de % par an, glissement sur 12 tours), x3 = U − U^eq (point de %, dénominateur N^pa) et x4 = ln(p/p̄) (sans dimension), chacun mesuré par écart au contrôle apparié. **De `macro`** : (a) signes de W_0, p_0 et U dans les 24 premiers pas ; (c) arrivée indépendante de la vitesse (`docs/exigences.md` § 2.7) : pour λ_e ∈ {0,1 ; 0,2 ; 0,4}, sur les pas 2 148 à 2 159 d'une fenêtre de 2 160 pas, écart au même contrôle apparié |π^e − π^e_contrôle| ≤ 1e−6 par an en valeur absolue, |U − U_contrôle| ≤ 1e−6 en fraction de N^pa, et |x/x_contrôle − 1| ≤ 1e−6 pour P, W et v^e ; (e) verdict « non concluant (banc) » si un bloc d'essai fait arrêter le noyau. **Publiés sans verdict** : demi-vie, ratio de sacrifice (seuil à #114), asymétrie des deux chocs, r̂\* − r̄. Aucun verdict de la boucle conjointe de la fiche 8 (#114). Options écartées : critère de `macro` seul (ratio de sacrifice jugé dès J3-c) ; critère de `monnaie` seul (sans arrivée indépendante de la vitesse). |
| P88 | #125 point 1 (P79), recommandation de `macro` : `facteur_g` = f(g_pr) · f(g_N) et Γ^e = `facteur_g` · f(π\*), f = `facteur_par_pas` ∘ `TauxDeCroissance` ; réalisé dans les commits de #61, tableau avant / après et visa de `macro`. |
| P89 | Corrections prospectives de la fiche 6 liées à #61 (§ 9.2 compris) ; #80 : voie (c) de M32 maintenue, aucune source (C30, conversion linéaire, écarts nominaux) traitée seule, échec attendu conservé (parts de Shapley de `macro`). Réalisé : `bf76979`. |
| P90 | Classement (a)/(b)/(c) des lignes « J3 » des § 9.6 des fiches 7 et 8 retenu (`monnaie`) ; les lignes (c) qui n'attendent qu'un bloc réel de plus vont à J3-d (#67 pour le bloc 6, module du bloc 9), les autres à #114. Réalisé : `bf76979`. |
| P91 | Mentions datées de P77 dans les fiches 7 et 8 (`bf76979`) et, au rang 7, dans la spécification (`docwriter`) ; chiffres périmés signalés sans changer la lecture des lignes. |
| P92 | BC3 exécutée en **forme convexe** (1 − c) π^e_t + c π_{t−1}, c = λ_e/n_a, avec la précondition 1 + π_{t−1} > 0 (refus explicite, jamais écrêtage) ; test de l'invariant π^e > −1 sur 10^6 tirages à graine déclarée plus un lot adverse (#91). |
| P93 | `outils/etat_stationnaire.py` aligné sur B7 en −min (#90) et BC3 en forme convexe (#91), précédent de P72, tableau avant / après. |
| P94 | Stationnarité partielle étendue : B1 à B7, B12, B13, B24, plus B8, B9, B16, B17, B18 (i), B19, B20, B25, B26, D et les états i_L, i_D, r̂\*, π^e, π\*, à 1e−9 relatif ou, pour une grandeur nulle, à 1e−12. |
| P95 | Bloc d'essai 9 : E1 (couverture de la ligne 16 sur Π^CB lu en phase 1) et E2 (lignes 11a à 11c selon E7) au rang 4, E3 (émission selon E9 à E11) au rang 6 ; le bloc d'essai 7 garde B7 en −min. |
| P96 | Unités existantes, aucune unité nouvelle : a_I « par an, taux de flux », r̄ et r̂\* « par an, taux de croissance » ; C51 (r̄ > −5 %) dans la table du bloc 8 ; noms `a_I`, `theta_CB` ; nomenclature du schéma v3 et tables des blocs 7 et 8 : ADR 0013, annotation du 14/11/2026. |
| P97 | ADR 0013 : préséance confirmée (l'ADR 0012 annoté fait foi, l'ADR 0013 se corrige par annotation) ; renvois à P80 confirmés ; plafond de 40 ko pour l'état consolidé seulement, reconsolidation par un nouvel ADR quand les annotations deviennent lourdes. |
| P98 | Issue #130 créée (proposition I1 de `monnaie`) : calibration de ϖ_L, ϖ_D, ϑ et r̄ sur des sources lues ; branche de calibration (P43 (a)). |
| P99 | #80, avis de `jeu` : défaut sans objet pour le joueur au socle et au J4 ; risque réel d'une stratégie « π\* ≈ 4 à 6 % » à l'ouverture du levier de cible (r̄_α en U). **Condition (c) d'ouverture du levier de cible** : l'écart de r̄_α entre l'ancienne et la nouvelle cible reste sous 0,1 point pour toute marche offerte ; à défaut, la marche est bornée, ou les trois sources sont rouvertes ensemble (C61). Versée sur #54 (commentaire du 14/11/2026). |

**Points ouverts au 14/11/2026** : issues proposées au rang 9 (bloc 9, collision E1–E3, encadré des vitesses, `tab:phases` au J4), en attente d'accord ; mentions « à numéroter » de la spécification (l. 2971, 2988, 3741, 3960) à remplacer par P100 à P102 au premier passage de `docwriter` ; #11 et #14 (mainteneur, hors branche) ; découpage de J3-d (P85) ; confirmation de la branche de calibration au point d'étape de J3-d (P43 (a)) ; résolution de l'état initial par `scenarios/` sans dupliquer le script (J3-e, § 2).

## Partie B : extraits de la tête sortis le 14/11/2026 (rang 9 de J3-c), figés

Sortis de `docs/feuille-de-route.md` à `aebbd1d` (tête de la branche `claude/j3-monnaie`, PR #129), pour tenir la tête sous son plafond de 60 ko (P76) : texte inchangé, titres décalés d'un niveau. Les numéros P-n restent stables ; ces décisions restent en vigueur tant qu'aucune décision ultérieure ne les remplace.

### 4. Décisions du mainteneur (extrait)

#### Décisions du mainteneur du 14/11/2026 (point d'étape après la PR #117, P74 à P86)

Points soumis par `architect` (Opus) au point d'étape après la fusion de la PR #117 (`main` = `688f299`), **toutes recommandations retenues par le mainteneur le 14/11/2026**, sans numéro M. Consignés au rang 0 de J3-c.

| N° | Décision |
|---|---|
| P74 | Périmètre de J3-c, option (a) : #119, #121, #61, #91, #90 avec `Closes` ; #80 sans `Closes` (instruction de C61, avis de `jeu`) ; #103 en J3-d, sa part du bloc 7 tenue par le critère 4 de #90. Options écartées : (b) liste indicative (#90, #91, #61, #80, #103) et #119 en branche dédiée ; (c) #121 en J3-d et #103 gardée. |
| P75 | Correctifs rapides avant l'ouverture : CR1, statut d'en-tête des fiches 1, 5, 6, 8 et 9 (PR #128) ; CR2, test de durée de la maquette conjointe (issue #126 créée, PR #127). |
| P76 | #119, option (b) : feuille de route en tête (≤ 60 ko, tableau M-n gardé, lu par `outils/concordance_spec_moteur.py`) et historique (`docs/feuille-de-route-historique.md`) ; ADR 0013 de consolidation, sans décision nouvelle, document de lecture (≤ 40 ko) ; l'ADR 0012 reste intact, les annotations futures vont à l'ADR 0013. **Sans Fable** (seuil § 4.3 atteint, consultation déclinée). Options écartées : (a) section « État en vigueur » dans l'ADR 0012 (le fichier grossit) ; (c) document hors ADR (deux maisons à synchroniser). |
| P77 | P56 étendue aux fiches 7 et 8 : lignes « état stationnaire » lues sur le moteur à n_a = 12 seulement, n_a ∈ {4 ; 52} couvert par le script ; comparaison au script, jamais aux chiffres recopiés d'une fiche (la fiche 7, § 9.6, porte encore Div/Π = 0,892616 à n_a = 12, barré et republié 0,890253 dans `sec:banque-stationnaire`). Correction prospective, ancien texte publié. |
| P78 | Boucle T3 ↔ BC3 mesurée sur le socle partiel (blocs 2, 3, 4, 7, 8 réels, plans nominaux exogènes), critère écrit au rang 1a par `monnaie` et `macro` ; elle remplace l'étiquette « π^e exogène (bloc d'essai) » sans valoir verdict de la boucle conjointe de la fiche 8 (stabilité, vitesses : #114). |
| P79 | #125 point 1 (forme de `facteur_g`) tranché au rang 1a par `macro`, avant Γ^e ; s'il est adopté, réalisé dans les commits de #61 avec tableau avant / après. Option écartée : report à J3-e (Γ^e modifié après coup). |
| P80 | Les mentions « J3-c » de l'ADR 0012, annotation du 13/11/2026, points 1.8 (domaine strict de la position K) et 3.4 (table du bloc 6 complétée), se lisent J3-d, avec #67 : mention datée au rang 1b. |
| P81 | #121, option (b) : liste blanche des importations d'un module de bloc ; rang 2 de J3-c. Option écartée : (a) liste noire. |
| P82 | #120, option (a) : refus à l'assemblage d'un `Cadre` dont n_a diffère de celui des tables ; J3-e. Options écartées : (b) domaines construits depuis le cadre ; (c) limite déclarée. |
| P83 | #123, option (a), avis de `macro` : labels de d et tu, ω\* couverte par `eq:travail-salaire`, g par l'ADR 0012 ; réalisée en J3-d avec #67 (S6 lit tu). Option écartée : (b) catégorie « définition exécutée non numérotée ». |
| P84 | Rattachements : #122 → J3-e ; #124 → J3-d ; #125 point 2 → J3-f, points 3 à 6 → J3-e (borne inférieure de κ et σ : `macro`). |
| P85 | Charge de J3-d au-dessus de cinq issues (§ 2) : découpage à instruire au point d'étape de J3-c. |
| P86 | Délégation technique reconduite pour J3-c. Rappel : #11 et #14. |

### 5. Pistes à instruire dans les fiches comparatives (texte complet sorti de la tête)

Ouvertes par M2 et M3 ; chacune sera présentée dans la fiche du bloc concerné, avec ses références vérifiées, l'avis de l'expert pilote et de `jeu`, puis tranchée par le mainteneur (M-n à venir). Une piste tranchée reste dans le tableau, barrée, avec sa décision.

| Piste | Fiche | Motif de l'instruction |
|---|---|---|
| ~~Pas de temps mensuel unique~~ — **retenue (M22, 30/09/2026)** | temps et comptabilité | Quatre fois moins de pas ; supprime l'incohérence calendaire de la v1.5 (4 pas par mois, 52 par an, glissement sur 12 mois) ; le moteur v2.0 prend 13 dates de décision par an. Pesée contre la granularité hebdomadaire des marchés dans la fiche (§ 3 à 7) : aucun fait mesuré de G à K ne l'exploitait ; réouverture par une décision M-m citant M22 si une fiche (J3, J6) établit un besoin infra-mensuel. |
| Consommation par règle stock-flux à cible de richesse (forme fermée) plutôt qu'une optimisation à chaque pas | ménages | État stationnaire calculable ; compatible avec l'invariant 11 de l'ADR 0002. |
| Corridor de taux explicite (facilités permanentes) | banque centrale et anticipations | Réserves et refinancement deviennent des flux décidés, pas des soldes résiduels (défaut d'invariance de la v2.0, ADR 0001 § 6). |
| Loi de crédibilité revue ; alternative : apprentissage à gain constant | banque centrale et anticipations | Piège de la loi v2.0 (ADR 0001 § 2). |
| Prix au coût normal majoré | prix | Forme fermée, lisible pour le joueur ; à confronter au terme de demande R3, acquis mesuré de la première tentative. |
| ~~Deux secteurs pour le socle (consommation, équipement)~~ — **écartée (M24, 02/10/2026) : J = 1 retenu**, équations indexées par j dès le socle | production et stocks | Budget de complexité (`docs/exigences.md` § 2.7). Instruite comme option D de la fiche (§ 3.D, § 3.J), contre J = 1 (option C), J = 4 et la liste de la v1.5 : à exigences comptables égales, elle n'ajoute aucune identité vérifiable et paie un prix relatif à stabiliser (instabilités 9 à 11 et 14 ; dérive de 12,8 % de p_K/p_C en v2.0, R) sans levier du socle qui l'exploite ; l'investissement se voit sous J = 1 par les ventes par acheteur. Les secteurs arrivent avec leur mécanisme propre aux jalons J5 à J7 (fiche § 3.J (d)). Libellé initial corrigé le 02/10/2026 (fiche § 1.5, Q1) : la mention « avant les quatre de la v1.5 et de la v2.0 » était inexacte pour la v1.5, qui propose **sept secteurs et un secteur de ressources** (`archive/v1.5/Nations_et_Marches_v1_5.tex` l. 391) ; seule la v2.0 en a quatre (`archive/v2.0/prototype/model.py` l. 68). |
| Encours hypothécaires agrégés par strate plutôt que cohortes individuelles | actifs et crises (J6) | 70 % du temps de la v2.0 dans 23 403 cohortes (mesuré le 29/09/2026). |

### 7. Branches fusionnées (extrait : de `claude/fondations` à `claude/j3-maquette-criteres`)

| Branche | PR | Jalon | Fusion | Détail |
|---|---|---|---|---|
| `claude/fondations` | #7 | J0 | 30/09/2026, commit de fusion `facf97f` | historique, partie A, § 7 |
| `claude/routage-modele-effort` | #22 | hors jalon (ad hoc ; M23, ADR 0006) | 02/10/2026, commit de fusion `7a17e01` | historique, partie A, § 7 |
| `claude/j1-temps-comptabilite` | #20 | J1 (branche n° 1 : fiche « temps et comptabilité », M21) | 02/10/2026, commit de fusion `3518e18` | historique, partie A, § 7 |
| `claude/correctif-journal-agents` | #31 | hors jalon (correctif rapide, `CLAUDE.md`, « Git et GitHub ») | 02/10/2026, commit de fusion `3276b7c` | historique, partie A, § 7 |
| `claude/technique-archive-concordance` | #29 | J1, branche technique n° 1 (M21 : outillage de J0) | 02/10/2026, commit de fusion `bf6ad56` (parents `3276b7c`, `8b9af3f`) | historique, partie A, § 7 |
| `claude/j1-cadre-production` | #35 | J1 (branche n° 3a : reprises du cadre et fiche « production et stocks », D2) | 03/10/2026, commit de fusion `3021eaa` (parents `bf6ad56`, `0a59fe0`) | historique, partie A, § 7 |
| `claude/j1-economie-reelle` | #43 | J1 (branche n° 3b : fiches 3 « travail et salaires », 4 « prix », 5 « ménages », 6 « investissement et financement », D2) | 04/10/2026, 10 h 12 UTC, commit de fusion `050ffbf` (parents `3021eaa`, `6157e3f`) | historique, partie A, § 7 |
| `claude/technique-matrices-ci` | #68 | J1, branche n° 3 bis (technique n° 2 : `verifier_matrices`, concordance, invariant d'archive et CI) | 04/10/2026, 12 h 20 UTC, commit de fusion `9097617` (parents `050ffbf`, `906edb5`), par le mainteneur | historique, partie A, § 7 |
| `claude/j1-monnaie-etat` | #77 | J1 (branche n° 4 : fiches 7 « banque commerciale », 8 « banque centrale et anticipations », 9 « État et dette » ; P13, P14) | 05/10/2026, 16 h 08 UTC, commit de fusion `54edad8` (parents `9097617`, `0cfdc44`), par le mainteneur | historique, partie A, § 7 |
| `claude/j1-cloture` | #85 | J1 (branche n° 4 bis : clôture, script d'état stationnaire sous forme fermée, technique n° 3 ; P19 à P27) | 07/10/2026, 10 h 36 UTC, commit de fusion `833afd9` (parents `47e0eb2`, `a8f3061`), par le mainteneur | historique, partie A, § 7 |
| `claude/j1-passage` | #94 | J1 (consignation du passage ; branche dédiée, non branche de travail, P28 (a)) | 07/10/2026, 11 h 15 UTC (date du commit de fusion), commit de fusion `faa3f85` (parents `833afd9`, `6dc9174`) | historique, partie A, § 7 |
| `claude/j2-noyau` | #99 | J2 | 15/10/2026, 05:01 UTC, commit de fusion `2e643a2` (parents `faa3f85`, `0e63473`), par le mainteneur | historique, partie A, § 7 |
| `claude/j3-maquette-criteres` | #109 | J3 (J3-a) | 13/11/2026, 17:34 UTC, commit de fusion `204ab2d` (parents `2e643a2`, `5fe2667`), par le mainteneur | historique, partie A, § 7 |

### 8. Escalades, relances et arrêts hors branche (extrait)

| Date | Fiche / modèle / critère déclenché / statut obtenu / suite |
|---|---|
| 13/11/2026 | Point d'étape après la PR #109 (plan de J3-b, réexamen du découpage de J3) / `architect-approfondi` / Fable, accord du mainteneur du 13/11/2026 (seuil § 4.3, critère 2, report du 15/10/2026) / P49 à P64 décidés le 13/11/2026 (P54, P56, P57, P63 sous réserve de l'avis de `macro`) / compte pour J3-b : 1 sur 3. |

## Partie A : version complète du 13/11/2026, figée le 14/11/2026

Copie intégrale de `docs/feuille-de-route.md` à `688f299` (fusion de la PR #117), titres décalés d'un niveau, texte inchangé. Elle contient la fiche de J3-b, les relevés d'issues des 15/10 et 13/11/2026, les décisions sans numéro M, les points P1 à P73 et D1 à D13, l'historique des jalons et le détail des branches fusionnées jusqu'à J3-a.

## Feuille de route

Tenue par `architect`, après chaque série de PR fusionnées. Chaque mise à jour est datée et cite le SHA de `main` et de la branche de travail.

**Dernière mise à jour** : 13/11/2026, consignation du rang 10 de J3-b — tête de la branche `ce7c619` ; par `architect` (Opus, effort `medium`) : § 1 (rangs 4 à 10, avis d'expert, issues #120 à #125), § 2 (J3-b à fusionner), § 3 (rattachement de #120 à #125).

**Mise à jour précédente** : 13/11/2026, point d'étape après la fusion de la PR #109 — `main` = `204ab2d` ; **branche de travail** `claude/j3-economie-reelle` (PR brouillon) ; par `architect-approfondi` (Fable, consultation accordée par le mainteneur le 13/11/2026, 1 sur 3 pour J3-b), consigné par `architect` : § 1 (fiche de J3-b), § 2, § 3, § 4 (P49 à P64), § 7 (J3-a), § 8.

**Mise à jour antérieure** : 15/10/2026, consignation des rangs 7 et 8 de J3-a, avant la sortie du brouillon — `main` = `2e643a2` ; par `architect` (Opus, effort `medium`, consignation) ; version à `5fe2667`, tête fusionnée de la PR #109 (cette version annonçait la tête `13146ff`, antérieure à son propre commit). Dernière version non condensée : `8511ba3`.

Mises à jour plus anciennes : historique de Git (`git log -- docs/feuille-de-route.md`).

### 1. Branche de travail en cours

#### Branche J3-b « économie réelle » (`claude/j3-economie-reelle`) — échafaudage (#112), production (#113), travail (#50), prix (#51), vocabulaire des unités (#104)

- **Branche** : ouverte depuis `main` à `204ab2d` (fusion de la PR #109). Issues : #112, #113, #50, #51, #104, toutes avec `Closes` (P49). Plan d'`architect-approfondi` du 13/11/2026, décidé par le mainteneur (P49 à P64, § 4). La fiche de J3-a est au § 7 et dans le corps de la PR #109.
- **Avant la branche** : #102 en correctif rapide (P50).
- **Délégation technique** reconduite (P64) ; #11 et #14 attendent toujours le mainteneur.
- **Budget Fable** : 1 sur 3, consommé par le point d'étape du 13/11/2026 (seuil § 4.3, report du 15/10/2026). Aucune autre consultation Fable prévue ; les deux restantes sont réservées à un désaccord entre experts et à un ADR d'architecture.

| Rang | Étape | Agent | Circuit | État |
|---|---|---|---|---|
| 0 | Consignation, PR brouillon, issues créées, `CONTEXT.md` | `architect`, session | `docs:` | fait : `ddb7a5a` (PR #117) |
| 1a | Critères et lectures avant le code : classement des lignes « J3 » des § 9.6 des fiches 2 à 4, T2 (b), part d'un bloc dans le coût, unités, option μ̃, g_N, stationnarité partielle | `macro-approfondi` ; `monnaie` ; validation du mainteneur | 4 | fait : avis favorables, P65 à P67 décidées (§ 4) ; P56 versée aux fiches 3 et 4 |
| 1b | Annotation de l'ADR 0012 : nomenclature des blocs 2 à 4, tables de paramètres, contrôle statique des lectures | `architect-approfondi` (Opus) | § 4.2 | fait : `22e31b8` ; P68 à P73 |
| 2 | #104 : vocabulaire fermé étendu | `coder` → `audit` | 3 | fait : `d5206d5`, `7f927ac` ; audit léger conforme |
| 3 | #112 : schéma v2, tables, socle partiel d'essai, linéarisation, part d'un bloc | `coder` → `audit` ; `macro` | 3 | fait : `a8eae65`, `b10c9a7`, `d79fbcd` ; audit léger conforme avec réserves (3 mineurs) ; avis de `macro` (2 corrections) ; reprise unique `0f95742`, `e230344` (audit : conforme, A1 majeur antérieur) ; lot A1 `76a1c44` (audit : conforme) |
| 3b | Allègement de `CLAUDE.md` (rang ajouté le 13/11/2026, accord du mainteneur) ; principes des workflows dans `.claude/workflows/README.md` | session | `claude:` | fait : `2b836dc` (22 741 → 21 393 octets, aucune règle changée) ; condensation de la feuille de route et de l'ADR 0012 : issue #119, hors périmètre |
| 4 | #113 : `production.py` ; Q2 de l'audit de #112 (finitude) | `coder` → `audit` ; `macro` | 1 | fait : `83a3afa`, `f4cdca6` ; finitude `6312fe0`, `b7d2037` ; audit léger conforme avec réserves (M1 versé sur #120, M2 corrigé au rang 6) ; visa de `macro` sous conditions C1, C2 (tenues) |
| 5 | #50 : `travail.py` | `coder` → `audit` ; `monnaie` consulté | 1 | fait : `1d52a61`, `8685d31` |
| 6 | #51 : `prix.py`, `eq:prix-indice` ; M2 | `coder` → `audit` | 1 | fait : `d0804aa`, `2e0974b` ; M2 `060cba4` |
| 7 | Mesures sur la plateforme de référence | session ; `macro` | — | fait : verdict sur la CI de `060cba4` (exécution 43522565602) : coût du noyau seul C = 0,2922 ms (seuil 0,5) ; parts (P57) production 0,0114, travail 0,0070, prix 0,0027 ms par pas (alerte 0,276, critère 0,48) ; projection cumulée 1,6933 ms contre 2,708 ms. Sur `main` `02c1e1f`, C = 0,4291 ms : la dispersion entre exécuteurs domine (commentaire sur #110) |
| 8 | Passage unique de `docwriter` ; balises et labels poussés ensemble, par issue | `docwriter` ; `macro`, `monnaie` | règle 9 | fait : `edf45de` (#104), `bef5257` (#112), `fca3992` (#113), `a307161` (#50), `49a1c83` (#51) ; docstrings `2027b3e` |
| 9 | Revue finale complète, `/code-review` | `audit` ; `macro` | règle 10 | fait : `audit` conforme avec réserves ; `/code-review` ; validation de `macro` (`dc1d861`) ; reprise unique `98124d2` à `ce7c619` (κ > 0 et 1/κ fini ; script, 1 + g > 0 par taux ; domaine à l'écriture par `Vue.ecrire_etat` ; reprise et ×100 avec blocs réels ; `docs:` `661922b`, `ce7c619`) |
| 10 | Consignation (fiches 2 à 4 « implémentées »), validation, fusion | `architect`, mainteneur | — | consignation faite (ce commit) ; validation et fusion : mainteneur |

**Avis d'expert tenant lieu de décision de lecture (sans numéro P ; avis de `macro`, 13/11/2026)** :
- ΔIN = 0 quand le disponible est nul : la clause de la spécification est conservée (forme B, N8) ;
- règle d'essai N = N\* pour les lignes « Délai » et « Vitesses » de la fiche 2, étiquetée « masse salariale du sentier » ;
- T2 (b) : verdict sur les blocs 2 à 4 réels (`tests/invariants/test_prix.py`) ; la mesure sur les blocs 2 et 3 (prix exogène) est publiée sans verdict ;
- P54, lecture (A) : l'option (i) de référence est évaluée sur l'ouverture de chaque pas de la trajectoire du moteur ;
- ξ jugée en écart absolu dans la ligne « Vitesses » de la fiche 4 (P66 par analogie) : visa de l'expert pilote, **à porter à la connaissance du mainteneur** ;
- `outils/maquette_conjointe.py` n'est pas aligné sur la forme B de N8 : la contre-épreuve reste indépendante.

**Issues créées pendant la branche** (autorisation du mainteneur du 13/11/2026) : #120 (`Cadre` à n_a ≠ 12, Q3), #121 (contournements du contrôle statique, A2), #122 (IN^vol = 0 ⇒ IN = 0 à l'état chargé), #123 (définitions exécutées non numérotées : d, tu, ω\*, g), #124 (domaine des plans nominaux, d < 0), #125 (facteur de croissance par pas sur g arrondi, formes divergentes).

**Escalades, relances et arrêts** : aucune consultation Fable dans la session de fin de branche ; budget Fable de J3-b : 1 sur 3 (point d'étape du 13/11/2026). Une reprise unique `coder` → `audit` après la revue finale (`98124d2` à `ce7c619`). Aucun arrêt. Le détail ligne à ligne est dans la PR #117.

**Stationnarité partielle (P67), mesurée le 13/11/2026 au rang 10** (`uv run pytest -q -s` sur les six fichiers de tests des blocs, 110 passed) : max |x_t/x̄ − 1| sur 720 pas, B1 à B7, B12, B13, B24, aux trois π\*, ≤ 1,8e−12 (B3, blocs 2 et 3 réels, π\* = 10 %) et ≤ 8,9e−14 avec les blocs 2 à 4 réels ; seuil 1e−9. Étiquettes : plans nominaux exogènes ; π^e exogène (bloc d'essai).

**Ce que la branche prouve** : variables des blocs 2 à 4 sur leur sentier à 1e−10 après un pas ; stationnarité partielle à 1e−9 sur 720 pas pour B1 à B7 et B24, aux trois π\* ; boucles propres ; identités, reprise et × 100 sous le schéma v2 ; concordance 40 / 40 ; part de chaque bloc dans le coût. Aucun verdict de J3, aucune référence.

**Conditions d'arrêt** : contrat partagé à modifier ; drapeau de mode dans `src/` ; stationnarité partielle hors seuil sans erreur de code ; arrêt du noyau sur le sentier ; part d'un bloc au-dessus de 0,276 ms (alerte) ou de 0,48 ms (critère) ; chiffre publié non reproduit.

**Effet sur les résultats** : premiers résultats du moteur pour les blocs 2 à 4 ; aucun résultat final. Budget de J3 inchangé : m = 0,60, max_k C_k ≤ 2,708 ms sur le socle complet (#105, #107).

### 2. Branches suivantes

| Ordre | Branche | Issues | Motif du regroupement et état |
|---|---|---|---|
| 4 | J1 — fiches du secteur monétaire et de l'État (`claude/j1-monnaie-etat`) | #71 (F7), #72 (F8), #73 (F9), #26, #69 | **Fusionnée le 05/10/2026** (PR #77, `54edad8`) : § 7. |
| 4 bis | J1, clôture (`claude/j1-cloture`), technique n° 3 comprise (P20 (a)) | #84, #44, #83, #74, #75 avec `Closes` ; #80 sans `Closes` | **Fusionnée le 07/10/2026** (PR #85, `833afd9`) : § 7. |
| — | Consignation du passage de J1 (`claude/j1-passage`), branche dédiée, non branche de travail | aucune | **Fusionnée le 07/10/2026** (PR #94, `faa3f85`) : § 7. Exception ponctuelle sans valeur de précédent (P28 (a)). |
| 5 | J2 — noyau (`claude/j2-noyau`) | #95, #96, #97, #98, #93, avec `Closes` | **Fusionnée le 15/10/2026** (PR #99, `2e643a2`) : § 7. |
| 6 | J3-a `claude/j3-maquette-criteres` | #107, #105, #65, #66, #100 | **Fusionnée le 13/11/2026** (PR #109, `204ab2d`) : § 7. |
| 7 | **J3-b `claude/j3-economie-reelle` (à fusionner)** | #112, #113, #50, #51, #104, avec `Closes` | **À fusionner** (§ 1, rangs 0 à 10 faits ; validation et fusion par le mainteneur) : blocs 2 à 4, schéma v2, socle partiel d'essai. |
| 8 | J3-c `claude/j3-monnaie` (indicative) | #90, #91, #61, #80, #103 | Blocs 7 et 8, π\* et Γ^e, signes sous lecture nette. |
| 9 | J3-d `claude/j3-menages-investissement-etat` (indicative) | #60, #67, bloc 9 (à rédiger), #101, #106 | Blocs 5, 6 et 9 ; socle complet. #106 fermée par retrait, sauf consommateur déclaré (P51). |
| 10 | calibration (P43 (a), indicative) | #45, #55, #62, #92 | Sources lues, visa ; confirmation au point d'étape de J3-d. |
| 11 | J3-e `claude/j3-socle` « socle et test zéro » (indicative, P61) | `scenarios/` (à rédiger), observation et #115, test zéro (à rédiger), #114 | État initial résolu ; critères A1, A2, B, C1, F, I1. |
| 12 | J3-f « stabilité et trajectoires » (indicative, P61) | S1 et S2 (à rédiger), #87, #88, #111, #116 | Linéarisation sur le moteur, trajectoires après chocs. |
| 13 | J3-g « budget, références, passage » (indicative, P61) | #110, G1 (à rédiger), références (à rédiger) | Dix exécutions, premières références, passage de J3. |

Ordre des modules : J3-b (blocs 2 à 4) → J3-c (blocs 7, 8 et #61) → J3-d (blocs 5, 6 et 9) (P41 (a)) ; π\*_t est écrite par le bloc 8 (P34 (a)) et lue par les blocs 5 et 6. Ce n'est pas l'ordre d'instruction de `docs/blocs/README.md` § 3 (les fiches sont toutes instruites). J3-c à J3-g sont indicatives (P39 (a), P61) ; le découpage de la queue de J3 (J3-e à J3-g) se fixe au point d'étape de J3-d (P61).

Issues à rédiger plus tard (`architect`, au point d'étape qui précède chaque branche, approuvées par le mainteneur) : module du bloc 9 `finances_publiques.py` (J3-d) ; `scenarios/` avec état initial résolu et test zéro (J3-e) ; S1 et S2 (J3-f) ; G1, budget du socle complet (J3-g) ; références et `outils/regenerer_references.py` (J3-g). Le module du bloc 2 `production.py` est l'issue #113 (13/11/2026).

Point ouvert pour J3-e, non tranché : la façon dont `scenarios/` résout l'état initial sans dupliquer le script (A1 compare les deux).

### 3. Issues hors plan

*Relevé du 15/10/2026* : point d'étape d'`architect-approfondi` après la fusion de la PR #99 (`main` = `2e643a2`), rattachements décidés par le mainteneur le 15/10/2026 (P39 à P46). Depuis le relevé du 07/10/2026 (41 issues ouvertes), #95, #96, #97, #98 et #93 ont été fermées par la PR #99, #100 à #106 ont été créées pendant J2 (point 8 du 14/10/2026) et #107 et #108 le 15/10/2026 : **45 issues ouvertes** (43 relevées par `list_issues` au point d'étape, plus #107 et #108). Les relevés antérieurs restent dans l'historique de Git (dernière version complète : `8511ba3`). La colonne « Branche prévue » n'est pas reportée sur GitHub. **Couverture** :

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #10 | Concordance : registre d'exemptions (ADR 0004) | hors plan | aucune exemption prévue |
| #11 | Dependabot : suivre ou non `uv.lock` | décision du mainteneur, hors branche | `ready-for-human` depuis le 30/09/2026 (rappel P47) |
| #14 | Ruleset de `main` : concorder le JSON et le ruleset appliqué | décision du mainteneur, hors branche | `ready-for-human` depuis le 30/09/2026 (rappel P47) |
| #37 | Aucun levier d'offre au socle | J4, au plus tard J7 | inchangé (M26, M28) |
| #45 | Calibration de λ_w | calibration (P43 (a)) | avec le gain d'apprentissage de la fiche 8 (C7) ; consulter `jeu` et `monnaie` |
| #46 | Coefficient d'Okun (−0,95 au socle) | J4 ; décision avant J7 | inchangé |
| #47 | Prix administrés : le gel domine sans coût de la marge comprimée | J4, puis J7 | inchangé |
| #48 | Levier de répartition (w2) | J4 | inchangé |
| #50 | `src/nations/blocs/travail.py` | **J3-b, rang 5, `Closes`** | bloc 3 ; après G1 (P40) ; circuit 1 en aval, validation de `macro` ; après #113 (13/11/2026) ; `monnaie` consulté |
| #51 | `src/nations/blocs/prix.py` | **J3-b, rang 6, `Closes`**, avec #50 | bloc 4 ; **porte `eq:prix-indice`** (P34 (a)) ; après #113 (13/11/2026) |
| #52 | Restitution des blocs 3 et 4, scénarios O2 | J4 | inchangé |
| #53 | Surchauffe publique (O3) | J4, avec #52 | inchangé |
| #54 | Aller-retour de la cible π\* | J4, sans `Closes` (mesure sur #65) | inchangé |
| #55 | Calibration de la fiche 6 | calibration (P43 (a)) | recoupe #92 |
| #56 | Signe net d'une hausse de taux | J4, sans `Closes` (mesure sur #65) | inchangé |
| #57 | Crises de crédit sous la règle F | J6 | inchangé |
| #60 | `src/nations/blocs/menages.py` | J3-d | après #61 et #91 (π\*_t lue par le bloc 5, P41 (a)) |
| #61 | Cible π\* et facteur Γ^e : forme et propriétaire | J3-c, avec #91 | π\*_t écrite par le bloc 8 (P34 (a)) ; G1 tranchée (P40), plus de condition « avant #61 » |
| #62 | Calibration de ν_H et λ_H | calibration (P43 (a)) | — |
| #63 | Restitution des ménages | J4, avec #52 | inchangé |
| #64 | S-ζ hors cible durable | J5 | inchangé |
| #65 | Maquette conjointe des blocs 2 à 9 | fermée par la PR #109 (13/11/2026) | P23 (a) ; amendement porté sur l'issue le 15/10/2026 (écart E3 corrigé) ; n'importe ni `src/` ni `archive/` |
| #66 | Contre-épreuve des boucles de la fiche 6 | fermée par la PR #109 (13/11/2026) | après #65, écrite sans lire la maquette |
| #67 | `src/nations/blocs/investissement.py` | J3-d | après #61 et #91 |
| #70 | Restitution de l'investissement | J4 | inchangé |
| #78 | Coût perceptible de la dette publique | J4, puis J6 | inchangé |
| #79 | Restitution de la banque commerciale | J4 | inchangé |
| #80 | Superneutralité (critère 13 de la fiche 8) | J3-c | défaut connu, `xfail(strict=True)` ; instruction de C30 ou de la conversion (C61), avis de `jeu` |
| #81 | Restitution de la banque centrale | J4 | inchangé |
| #82 | Restitution de l'État et dette | J4, avec #81 | inchangé |
| #87 | D_F ≥ 0 hors de l'état stationnaire et selon n_a (q1) | J3-f (P60) | P42 : trajectoires dynamiques, socle complet requis ; estimation préliminaire facultative sur la maquette |
| #88 | Fenêtre longue de la fermeture monétaire | J3-f (P60), avec #111, puis J4 | P42, comme #87 ; unification des conventions à ν_G = 1 |
| #89 | Stratégie dominante sur les combinaisons de leviers | J4 | dépend de #88 |
| #90 | `src/nations/blocs/banque.py` | J3-c | critère : égalité au script à 1e−10 ; avec #103 |
| #91 | `src/nations/blocs/banque_centrale.py` | J3-c, avec #61 | marche de cible ; superneutralité en `xfail` (#80) |
| #92 | Calibration de μ̄ | calibration (P43 (a)) | recoupe #55 et #48 |
| #100 | Contrat de lecture du grand livre (constat C1 de l'`audit` du lot final de #97) | fermée par la PR #109 (13/11/2026) | contrôle de contrat à poser avant que le premier bloc lise le grand livre |
| #101 | Test de source : autres valeurs publiées de `sec:investissement-taux` | J3-d | outil seul, `monnaie` |
| #102 | Test « conversion unique » : littéral 12, appels et constantes de module | correctif rapide avant J3-b (P50) | critère : aucun littéral 12 dans `src/` hors de `cadre.py` ; dépendance #102 → premier code de bloc |
| #103 | Signes sous lecture nette : M^G, D_H, D_F | J3-c | M^G par `monnaie`, D_H et D_F par `macro`, avec #90 ; critère du bloc 9 relu en J3-d |
| #104 | Vocabulaire des unités | **J3-b, rang 2, `Closes`** | avant les paramètres des modules ; avant #112 |
| #105 | Dispersion du coût mesuré en CI | fermée par la PR #109 (13/11/2026) | avant de fixer la marge du budget de J3 ; N = 10 |
| #106 | Consommateur de `variation_sur_le_tour` | J3-d (P51) | hors de J3-b : aucun bloc de J3-b ne la lit ; fermeture par retrait en J3-d, sauf consommateur déclaré |
| #107 | Critères de J3 écrits avant l'essai | fermée par la PR #109 (13/11/2026) | créée le 15/10/2026 |
| #108 | Identifiants : catégories Unicode Cn et Co | J5 | P46 (a), créée le 15/10/2026 |
| #110 | Processeur de l'exécuteur en CI | J3-g (P60) | créée le 15/10/2026 pendant J3-a (#105) ; #110 → G1 |
| #111 | Remesurer les trajectoires C-HS publiées avant l'amendement de E12 | J3-f (P60), avec #88 | créée le 15/10/2026 pendant J3-a (#65) ; trajectoires non remesurées par la maquette ; après #116 |
| #112 | Schéma d'état v2, tables de paramètres des blocs 2 à 4, socle partiel d'essai | **J3-b, rang 3, `Closes`** | créée le 13/11/2026 (A) ; après #104 ; P52, P53, P57, P58 |
| #113 | `src/nations/blocs/production.py` | **J3-b, rang 4, `Closes`** | créée le 13/11/2026 (B) ; après #112 ; balises `eq:production-*` |
| #114 | Critère I1 : lignes « J3 » des § 9.6 des fiches 2 à 9 qui exigent le socle complet | J3-e | créée le 13/11/2026 (C, suivi de I1) ; après #113, #50, #51 |
| #115 | Concordance : radical `observation` admis avant le premier label `eq:observation-…` | J3-e | créée le 13/11/2026 (D) ; #115 → premier label `eq:observation-…` |
| #116 | Maquette conjointe : annotations des fiches dans le relevé, résidu du point fixe des cartes partielles | J3-f | créée le 13/11/2026 (E) ; #116 → #111 |

*Complément du 15/10/2026 (consignation de J3-a)* : #110 et #111 créées pendant J3-a (47 issues ouvertes, hors issue proposée par `coder` sur #100, non créée).

**Dépendances ajoutées** (15/10/2026) : #107 → tout essai de J3 ; #105 → marge du budget de J3 et acceptation de #100 ; G1 → bloc 2, #50, #51, #60, #67, #90, #91, bloc 9 ; #91 et #61 → #60, #67 ; #100 → J3-b ; socle complet (fin de J3-d) → #87, #88. **Retirées** : #65 → #87, #88 (P42) ; « G1 avant #61 » (P40, écart E4). **Inchangées** : #65 → #66, #54, #56 ; #88 → #89 ; P34 → #51.

*Complément du 13/11/2026* : #107, #105, #65, #66 et #100 fermées par la PR #109. Rattachements : #102 → correctif rapide avant J3-b ; #104 → J3-b ; #106 → J3-d ; #110 → J3-g ; #111 → J3-f, avec #88 ; #87 et #88 → J3-f. Issues créées le 13/11/2026 : #112 (A) et #113 (B) pour J3-b, #114 (C, suivi de I1) et #115 (D, radical `observation`) pour J3-e, #116 (E, relevé et point fixe de la maquette) pour J3-f.

*Complément du 13/11/2026 (consignation du rang 10 de J3-b)* : issues créées pendant J3-b, sur autorisation du mainteneur du 13/11/2026, rattachements proposés (à confirmer au point d'étape qui suit la fusion de la PR #117) :

| Issue | Objet | Branche prévue | Remarque |
|---|---|---|---|
| #120 | `EnsembleDesParametres` accepte un `Cadre` à n_a ≠ 12 sans recouper les domaines des tables (Q3 ; M1 de l'audit du rang 4 : N2 lit n_a par la vue) | point d'étape après J3-b | forme du contrôle à fixer |
| #121 | Contrôle statique des lectures : contournements restants, liste noire ou liste blanche | point d'étape après J3-b | choix de méthode (A2) |
| #122 | Cohérence IN^vol = 0 ⇒ IN = 0 à l'état chargé | J3-e | état initial de `scenarios/` et reprise |
| #123 | Définitions exécutées non numérotées (d, tu, ω\*, g) : numéroter ou déclarer leur catégorie | **décision du mainteneur** | règle de concordance (`CONVENTIONS.md`) |
| #124 | Domaine des plans nominaux et de la demande adressée (d < 0, N6) | J3-d | avant les blocs acheteurs réels |
| #125 | Facteur de croissance par pas sur g arrondi ; formes divergentes entre script, linéarisation et moteur | J3-e et J3-f | test zéro (J3-e), linéarisation sur le moteur (J3-f) |

**Dépendances ajoutées** (13/11/2026, rang 10) : #124 → blocs 5, 6 et 9 réels (J3-d) ; #122 → état initial résolu de `scenarios/` (J3-e) ; #125 → test zéro (J3-e) et S1, S2 (J3-f) ; #120 → toute exécution à n_a ≠ 12. **Retirées** : aucune.

**Dépendances ajoutées** (13/11/2026) : rang 1a de J3-b → tout essai de J3-b ; #104 → #112 → #113 → #50, #51 ; #102 → premier code de bloc ; #114 ← #113, #50, #51 ; #115 → premier label `eq:observation-…` ; #110 → G1 ; #116 → #111. **Retirées** : #102 et #106 de J3-b. **Inchangées** : celles du 15/10/2026.

### 4. Décisions du mainteneur

M1 à M19 sont datées du 29/09/2026, M20 à M23 du 30/09/2026, M24 du 02/10/2026, M25 à M30 du 03/10/2026, toutes arrêtées par le mainteneur. M1 à M15 sont consignées dans l'ADR 0001 (§ Décision, point de même numéro) ; M16 dans l'ADR 0003 ; M17 précise M6 dans l'ADR 0001 ; M18 à M21 n'ont pas d'ADR (règles de procédure) ; M22 est consignée dans l'ADR 0005 (accepté le 30/09/2026) et dans la fiche `docs/blocs/temps_comptabilite.md` § 8 ; M23 est consignée dans l'ADR 0006 ; M24 est consignée dans la fiche `docs/blocs/production.md` § 8 et, pour sa lecture (b) qui modifie un contrat partagé, dans l'ADR 0007 (accepté le 02/10/2026, qui complète l'ADR 0005 sans le réécrire). M25 et M26 sont consignées dans les fiches `docs/blocs/travail.md` § 8 et `docs/blocs/prix.md` § 8 et, pour les deux contrats partagés qu'elles modifient (conversion des taux de croissance et d'inflation ; phase de l'indice des prix), dans l'ADR 0008 (proposé puis accepté le 03/10/2026, avec son point II.3 ; il révise en partie l'ADR 0005, annotation datée de celui-ci). M27 et M28 sont consignées dans les fiches `docs/blocs/menages.md` § 8 et `docs/blocs/investissement.md` § 8 ; M29 dans l'ADR 0009 ; M30 dans l'ADR 0010. La forme canonique du numéro est `Mn` (`M16`), citée telle quelle dans les fiches comparatives, la spécification (provenance des équations, `CONVENTIONS.md` § 2.3) et les issues ; « M-n » désigne une décision quelconque dans la prose. Trois décisions de mise en œuvre sont consignées par annotation d'ADR sans numéro (elles ne changent aucune décision numérotée) : garder `outils/compiler_specification.sh` (29/09/2026, ADR 0004, pt 4) ; déclarer le hook `preparer_latex.sh` en `SessionStart` (29/09/2026, ADR 0004, pt 5) ; règle 4 de la concordance, une décision par mention, le pluriel « décisions M3 et M16 » et la forme groupée « (M3, M16) » restant refusés (30/09/2026, ADR 0004, pt 6, et `CONVENTIONS.md` § 9).

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

Le même jour (30/09/2026), le mainteneur a validé sans numéro : l'inventaire `docs/blocs/README.md` (`macro` pilote de « temps et comptabilité » et de « État et dette », module `finances_publiques.py`) ; le maintien des sections `sec:objet`, `sec:ecartees` et `sec:chantiers` du squelette `.tex` telles que remplies au jalon J0 ; `docs/specification/CONVENTIONS.md` tenu par `docwriter`, qui tient déjà `docs/specification/` (et non par `architect`, comme l'indiquait l'en-tête du fichier) ; libellé `ready-for-human` sur #11 et #14.

Le 02/10/2026, sur le point d'étape qui suit la fusion de la PR #20 (`1308807`), le mainteneur a décidé sans numéro : plan de la branche technique n° 1 validé tel quel (§ 1), #8 et #9 en `ready-for-agent` ; technique n° 2 placée entre les branches n° 3 et n° 4 (§ 2) ; #25 traitée par **suppression du double emploi** (la colonne de `tab:matrice-flux` tient lieu de contrainte budgétaire, prose retirée par `docwriter`), et non par un contrôle par script ; #23 tranchée avant l'ouverture de la branche n° 3 et mise en œuvre en tête de celle-ci ; contrats partagés issus de M22, dont `preparer_tex`, ajoutés à `docs/agents/routage.md` § 4.2 ; définition du statut « spécifiée » d'une fiche (`docs/blocs/README.md` § 4) : section proposée rédigée par `docwriter` et validée par l'expert pilote, les labels faisant passer à « implémentée » ; fiche 1 « temps et comptabilité » passée à « spécifiée » le même jour.

Le 02/10/2026, sur le point d'étape qui suit la fusion de la PR #29 (`bf6ad56`), le mainteneur a décidé sans numéro : **notation de #23** — taux nominaux en i (inchangé), indice des pays renommé **c**, le secteur productif gardant j (et k pour un intrant), exposants ^p et ^s des marchés primaire et secondaire remplacés par ^{prim} et ^{sec}, tables du cadre et `outils/verifier_matrices.py` mis à jour ensemble ; la décision initiale du même jour (« pays j ») a été corrigée parce que j est réservé au secteur productif ; le critère de #23 exclut de son champ les marques de secteur (H, F, Bk, CB, G), qui ne sont pas des grandeurs, déclaration faite avant la mise en œuvre ; **découpage de la branche n° 3** en n° 3a et n° 3b, **une issue par fiche en quatre jalons** (`docs/blocs/README.md` § 4 amendé) ; **redéfinition du statut « spécifiée » non numérotée**, la décision de la fiche 2 prenant M24 ; **création de #32 et #33 (proposées dans la PR #29) et de #34 (fiche 2)** et passage de #25 et #23 en `ready-for-agent`, par la session principale ; **délégation technique reconduite pour la branche n° 3** (questions purement techniques, une relance par issue d'un workflow arrêté sur un constat majeur, conduite jusqu'à la sortie du brouillon), le fond et le choix d'approche restant au mainteneur.

Décisions prises **en cours de branche**, le 02/10/2026 (PR #35) : #23, détenteur des titres écrit avec l'indice s (avis de `monnaie`) et « délai k » renommé « délai du premier flux d'intérêt » dans `CONTEXT.md` ; #34, jalon 1, critères validés tels quels ; **#36 ajoutée au périmètre** ; création de #36 et de **#37** (proposée par `jeu`, § 3) ; **M24** (§ 4), avec l'ADR 0007 pour sa lecture (b).

Décisions prises **en cours de branche**, le 03/10/2026 (PR #35), sur la validation de fond de `sec:production` (#34, jalon 4) par `macro-approfondi` : **visa de l'amendement de notation du critère 3 et du § 9.6 de la fiche 2** — π̄ s'y lit comme un **glissement annuel stationnaire** (conforme à `sec:cadre-calendrier` et à `CONTEXT.md`, « Registre de l'indice des prix »), au lieu de la lecture linéaire π̄/n_a de la fiche ; valeurs remesurées par `macro` (script et simulation) : ρ̄_IN = 0,996057 (π̄ = 2 %, n_a = 12), ΔIN = 0,33210 % de IN par pas, ρ̄_K = 0,7791 à π̄ = 2 % et 0,4221 à 10 % (δ = 5 %), au lieu de 0,996021, 0,33361 %, 0,7775 et 0,4114 ; aucun résultat du moteur en jeu (le moteur v3 n'exécute rien), d'où ni tableau avant / après ni référence ; **correction des constats m1 et m2 de la remesure S1 dans la branche** ; **création d'une issue sur les bornes sans paramètre** (#38). Les valeurs corrigées sont reportées dans `docs/blocs/README.md` (ligne de la fiche 6) et dans la ligne de la branche n° 3b (§ 2 de la version d'alors, § 1 depuis le 03/10/2026) ; la notation barrée des valeurs stationnaires (`CONVENTIONS.md` § 5.2) est appliquée à `CONTEXT.md` (« Coût moyen pondéré »).

Le 03/10/2026, après la fusion de la PR #35 (`3021eaa`), le mainteneur a décidé sans numéro : **lancement de la branche n° 3b** avec les quatre fiches 3 à 6, sans recoupage (D2 le permettait) ; délégation technique reconduite pour toute la branche n° 3.

Décisions prises **en cours de branche**, le 03/10/2026 (PR #43), sans numéro M :
- **ADR 0008 accepté**, avec son point II.3 (registre de 13 niveaux, empreinte calendaire de 14 variables) ; l'annotation de l'ADR 0005 le constate et corrige, au point 17, l'incohérence préexistante relevée par `macro` (« 0,9 % » dans le texte de l'ADR, 1,0109 dans la spécification, 1,0108 sous (G)).
- **Visa des chiffres d'état stationnaire de la fiche 2 recalculés sous (G)** (ADR 0008, partie I ; recalcul de `macro`), aucun résultat du moteur en jeu (le moteur v3 n'exécute rien), d'où aucune référence :

  | Grandeur (définition, unité) | Avant (lecture linéaire de g_pr, M24 (f)) | Après (G) | Explication |
  |---|---|---|---|
  | Croissance effective publiée pour g_pr = 2 % (glissement annuel) | 2,0184 % | 2 % | conversion géométrique : un niveau qui croît au taux x croît exactement de x en n_a pas (ADR 0008, pt I.1 et I.5) |
  | ρ̄_K = K/(p K^vol), δ = 5 %, à π̄ = 2 % (et à π̄ = 10 %), g = 2 % | 0,7791 (0,4221) | 0,7786 (0,4214) | croissance réelle par pas (1 + g)^{1/n_a} − 1 au lieu de g/n_a dans la forme fermée (ADR 0008, pt I.5) |
  | ΔIN et FU, en % de IN par pas (g = π̄ = 2 %) | 0,33210 % | 0,33059 % | croissance nominale par pas (1,02 × 1,02)^{1/12} − 1, au lieu de (1 + 0,02/12) × 1,02^{1/12} − 1 |
  | Stocks restitués, en mois de ventes (g = π̄ = 2 %) | 1,4152 | 1,4151 | même révision de la croissance réelle par pas (ADR 0008, pt I.5) |
  | Facteur entre ratio restitué et ratio du test zéro, g = 2 %, n_a = 12 (ADR 0005, pt 17) | 1,0109 | 1,0108 | (1 + g)^{1/n_a} au lieu de 1 + g/n_a |
  | Valeur propre de la dynamique des stocks (g = π̄ = 2 %) | 0,8735 | 0,8736 | même révision de la croissance réelle par pas (ADR 0008, pt I.5) |
  | y/v, production sur ventes à l'état stationnaire | indépendant de n_a | dépend de n_a | ratio mixte, taux de flux linéaire et croissance géométrique : dépendance déclarée (ADR 0008, pt I.6) |

  Chiffres recalculés par `macro` (fiche 2, § 3.N et § 9) ; ΔIN et le facteur sont remesurés par `architect` le 03/10/2026 (0,0033059 ; 1,010768), les autres sont repris du recalcul de `macro`. Forme de la révision de la fiche 2 : § 3.N et § 9 corrigés avec la mention « révisé par M25 (b) » ; § 4 à 7 (avis historiques) laissés tels quels.
- **Seuil du critère 11 (d) de la fiche 3 adopté** : demi-vie de l'emploi de 2 à 4 tours ; λ_N = 3,5 par an (M25) donne 2,01 tours.
- **#44 rattachée à la branche n° 4 sans `Closes`** ; elle se ferme au J3 avec le script d'état stationnaire (§ 2 et § 3).
- **Création de #49 à #52** (§ 3).
- **Fiche 6** (après le dépôt de l'instruction) : visa de l'amendement de notation des critères sous (G) ; amendement prospectif du critère 6 (écart ≤ 1e−6 mesuré après 2 160 pas, et non 720) ; lecture annuelle des taux de la v1.5, T_K en dépendance déclarée (`docs/blocs/investissement.md` § 2, amendements).
- **Création de #53 à #59** (proposées par `jeu` et `macro`, fiches 5 et 6, et propositions de la passation) et de commentaires sur #44 (`macro` : fermeture sous S et extension du script d'état stationnaire ; `monnaie` : S-ζ et C36 ; `jeu` : persistance d'une impulsion) (§ 3).
- **Désaccord `macro` / `monnaie` sur la fiche 6 (S ou S-ζ)** : s'il persiste après la remesure de `macro`, une consultation Fable précède M28 (`docs/agents/routage.md` § 4.1, point 2 ; accord du mainteneur du 03/10/2026).
- **Après M27 et M28** (§ 9 des fiches 5 et 6) : π\* en vigueur lue à l'ouverture (délai 1) par les blocs 5 et 6, Γ^e grandeur du moteur, π\* paramètre au J3 initialisant une variable d'état « cible en vigueur » ; lectures de la fiche 5 retenues (renommages ν_H, λ_H, π^{∗,pas} ; plafond sur D_H ; plancher du plan ; seuil 12 (d) de 0,50 à 0,85) ; **#58 rattachée à la branche sans `Closes`** ; **M29 acceptée sur le fond** (lecture (i) d'`architect` : variables d'état retardées écrites en phase 9 ; ADR 0009 déposé après relecture Fable, consultation 1 sur 3) ; création de #60 à #64 et de commentaires sur #55 et #57 (fiches 5 et 6, § 9.10).
- **Validation de la spécification par `macro` (04/10/2026)**, quatre rapports (un par commit `docs:` de `docwriter`), tous « validés avec réserves », aucune équation fautive : (a) **critère de période de la boucle combinée (36 à 96 tours, fiche 3 critère 5 (c)) mesuré à prix figé** (lecture (a), avis de `macro`) ; la période sous la règle M (100,4 tours à m = 0,7, 115,5 à m = 0,8) est publiée dans `sec:prix-conditions` sans verdict ; (b) annotations datées et prospectives des fiches 2 à 6 (`2af377e`) ; (c) annotation des ADR 0005 et 0008 par `architect` (facteur du ratio restitué en volume ou en u.m. ; `eq:moteur-glissement` ; `b6ad4da`) ; (d) création de #65, #66 et #67 (§ 3). Après le contrôle des reprises par `macro` (04/10/2026) : (e) **critère J3 « Délais » de la fiche 6 corrigé de façon prospective** (critère mal posé, aucun essai fait) : le plan d'investissement en u.m. est testé à n + 2, le volume livré pouvant varier dès n + 1 par le prix ; (f) commentaire sur #60 (départager 1,0415 et 1,09 à n_a = 4) ; (e bis) seconde correction prospective du même critère, le même jour, avant tout essai : aucun rationnement des biens (N6) au tour n + 1 (`6994cbb`). **Revue finale complète** (règle 10, `macro-approfondi` et `/code-review`, 04/10/2026) : (g) **critère J3 « Délais » des ménages corrigé de façon prospective** (dividende de la règle F au tour n, budget au tour n + 1 ; critère mal posé depuis M28, aucun essai fait) ; (h) **écart de valorisation du capital restitué au bilan défini à l'ouverture** (lecture (a)) ; (i) **visa** du niveau normal du capital au prix courant recalculé : 2,037 ans au lieu de 2,040 à π̄ = 2 %, 2,093 au lieu de 2,110 à 10 % (facteur de fenêtre réel pour un volume valorisé au prix du tour).

#### Points P1 à P27 (condensés le 07/10/2026, P29 (a))

Points soumis par `architect` ou `architect-approfondi` aux points d'étape des 03, 04 et 05/10/2026, **tous décidés par le mainteneur selon l'avis présenté**, sans numéro M (organisation, périmètre, triage, rattachement, lecture d'un critère). Une ligne par point ; les avis, variantes et motifs complets sont dans la version de la présente feuille de route à `faa3f85` et dans le commit de consignation cité. Les SHA de la dernière colonne sont vérifiés (`git log` ou `gh api …/commits/<sha>`, 07/10/2026).

| N° | Date | Décision | Consignée |
|---|---|---|---|
| P1 | 03/10/2026 | Statut de fait « V » adopté avec trois amendements (V : remesuré en v3 par un script d'`outils/` revu par `audit` ; V+O si le vérificateur réexécute ; un fait V sur le prototype v2.0 reste un fait de la première tentative) ; écrit dans `CONTEXT.md` | `d62e67a` |
| P2 | 03/10/2026 | M^G\* « encaisse stationnaire » marquée ∗ : rattachée à #26 (fiche 9) | `d62e67a` |
| P3 | 03/10/2026 | #38 cinquième issue de la n° 3b, `Closes` ; #24 et #37 sans `Closes`, hors décompte. Le même jour : décisions par paires des fiches couplées (3 et 4, puis 5 et 6) | `d62e67a` |
| P4 | 04/10/2026 | #59 fermée (« completed », `b8978f2`) | `74c6e35` |
| P5 | 04/10/2026 | #58 fermée (« completed », `b9b8260`) | `74c6e35` |
| P6 | 04/10/2026 | (a) #33 dans la n° 3 bis : cinq issues | `74c6e35` |
| P7 | 04/10/2026 | #32 et #33 en `ready-for-agent` ; règle d'arrêt du cas `\or` en commentaire de #32 | `74c6e35` |
| P8 | 04/10/2026 | Délégation technique reconduite pour la n° 3 bis | `74c6e35` |
| P9 | 04/10/2026 | Contrôle d'identité des listes de batteries ajouté à l'acceptation de #28 | `74c6e35` |
| P10 | 04/10/2026 | Issue #69 créée (ligne 0 de `tab:phases` et Γ^e ; glossaire), rangée à la n° 4 ; visa de forme d'`architect` | `74c6e35` |
| P11 | 04/10/2026 | Issue #70 créée (restitution du bloc investissement, J4) | `74c6e35` |
| P12 | 04/10/2026 | Rappel #11 et #14, sans décision | `74c6e35` |
| P13 | 04/10/2026 | (a) Périmètre de la n° 4 : #71, #72, #73, #26, #69 avec `Closes` ; #24 et #49 critères de #72, sans `Closes` | `10391a1` |
| P14 | 04/10/2026 | Fiche 7 décidée seule (M31), puis 8 et 9 par paire (M32, M33) ; critères des trois fiches validés ensemble | `10391a1` |
| P15 | 04/10/2026 | #74 et #75 créées (technique n° 3) ; point 4 non créé (limites déclarées) ; #76 traitée par le premier commit de la n° 4 (`14c8050`) | `10391a1` |
| P16 | 04/10/2026 | (a) M19 inchangée ; branche n° 4 bis « J1, clôture » (script d'état stationnaire), où #44 se ferme | `10391a1` |
| P17 | 04/10/2026 | Délégation technique reconduite pour la n° 4 | `10391a1` |
| P18 | 04/10/2026 | Rappels (budget Fable, #11, #14), sans décision | `10391a1` |
| P19 | 05/10/2026 | (a) Périmètre de la n° 4 bis : #84, #44, #83, #74, #75 avec `Closes` ; #80 sans `Closes` | `764c7f0` |
| P20 | 05/10/2026 | (a) Technique n° 3 (#74, #75) dans la n° 4 bis, rang 1, circuit 3 | `764c7f0` |
| P21 | 05/10/2026 | (a) « Sans simulation » exclut l'itération dans le temps, non la résolution d'une équation d'état stationnaire (méthode déterministe, tolérance déclarée, racine unique dans le domaine, résidu publié) ; M19 inchangée | `764c7f0` |
| P22 | 05/10/2026 | (a) ν_G fixé dans la n° 4 bis, au rang 4, visa de `macro` (QM6) ; `Closes #83` | `764c7f0` |
| P23 | 05/10/2026 | (a) #65 amendée (blocs 2 à 9, maquette conjointe unique), en tête de J3, avant #66 | `764c7f0` |
| P24 | 05/10/2026 | (a) q1 de `macro` mesurée à l'état stationnaire par le script ; question hors de l'état stationnaire en issue J3 (#87) | `764c7f0` |
| P25 | 05/10/2026 | Délégation technique reconduite pour la n° 4 bis | `764c7f0` |
| P26 | 05/10/2026 | Rappels (−0,43 % caduc, intervalle de a_π, #11 et #14, budget Fable), sans décision | `764c7f0` |
| P27 | 05/10/2026 | (a) Commit `claude:` de budget de tours en correctif rapide (`d7bc95f`, PR #86, fusion `47e0eb2`) ; ni effort ni `maxTurns` changés | `764c7f0` |

Le 04/10/2026, après la fusion de la PR #43 (`050ffbf`), le mainteneur a décidé sans numéro : **lancement de la branche n° 3 bis** (« Lance la branche suivante »), dans l'ordre 3b → 3 bis → 4 fixé le 02/10/2026 (§ 2).

Le 04/10/2026, après la fusion de la PR #68 (`9097617`), le mainteneur a demandé de **passer à la branche suivante** (n° 4, ordre fixé le 02/10/2026, § 2) ; la vérification programmée de la PR #68 a été supprimée (session principale). Plan proposé au § 1, soumis ci-dessous.

#### Validation des critères des fiches 7, 8 et 9 (rang 1 de la n° 4, 04/10/2026)

Critères proposés par `monnaie-approfondi` (fiches 7 et 8, `3b06f8f`, `6777662`) et `macro-approfondi` (fiche 9, `53b4124`), puis relecture croisée (avis de l'expert consulté, une relance ciblée par expert, avis de `jeu`, qualifications des contrats partagés par `architect-approfondi`), intégrée par `c23b302`, `5759b27`, `5066400`. **Décisions du mainteneur du 04/10/2026, toutes selon l'avis des experts** (aucune ne demande de numéro M ; consignées au § 2 « Amendements adoptés » de chaque fiche) :
- critères des trois fiches **validés** tels qu'amendés (18, 24 et 23 critères), seuils reconduits et seuils de `jeu` adoptés ; les options marquées « à trancher » (propriétaire des lignes 19a, règle de i_B, M^G\* et lecture du contrôle de caisse, forme de E^CB, porteur de C2 si la fermeture budgétaire était retenue) se décident à M31-M33, avec leur qualification d'`architect` ;
- #56 : branche (A) de référence = règle de taux en vigueur plus un écart d'un point à la prescription ; taux exogène publié en mesure ;
- #49 / C15 : seuil de matérialité de 0,1 point (un cran d'affichage) ; l. 214 lue comme précision rédactionnelle (annotation datée de l'ADR 0005, point 5, à faire au rang 8) ;
- intention du 17/09/2026 (« cible et taux ») reconfirmée : la persistance du critère 10 (b) (ii) de la fiche 8 est une exigence ;
- issue **#78** créée (coût perceptible de la dette au socle, J4 et J6).

Si A8, la lecture nette tenue par le noyau ou la variante (β) de i_B sont retenus à M33, `architect` recommande un seul ADR d'architecture, rédigé avec une consultation Fable (0 sur 3 à ce jour).

#### Décisions sur les questions des § 9 des fiches 8 et 9 (rang 9 de la n° 4, 04/10/2026)

Questions posées par `monnaie-approfondi` (fiche 8, § 9, `15cc933`), `macro-approfondi` (fiche 9, § 9.3, QM1 à QM8, `3aea20c`) et `architect-approfondi` (ADR 0011, `50cc78b`, Fable, consultation 1 sur 3). Décisions du mainteneur, sans numéro M (précisions de M32 et M33), toutes selon la recommandation présentée :
- **ADR 0011 accepté**, avec ses points de forme 3 et 4, en **lecture (i)** de la ligne 19b : aucun proposant de 19b au socle (achats de la banque centrale au J6), l'État seul écrivain de la phase 7 ; annotations des ADR 0005 (pts 5, 10, 13), 0009 et 0010 à appliquer par `architect` ;
- **borne de m corrigée** : m ≥ 1,0959 à π̄ = 0 (1,10 × Γ̄ × s_G ; le 1,0965 de la fiche 9 § 8, commit `29dea85`, était une erreur de recopie ; remesure de la session : 1,0959441) ;
- **notation** : k_I → a_I ; s_CB, m (encaisse visée) et P (paiements bruts) renommés pour lever des collisions ; r̂\* gardé, exception déclarée au glossaire ; symboles nouveaux fixés par `architect` (rang 9 bis), appliqués par `docwriter` ;
- **bande du test zéro sur r = i − π** (fiche 8, critère 17) centrée sur r̄(1 + π\*), correction prospective écrite avant l'essai ;
- **QM2** : lecture (a), parts non payées enregistrées sans ligne nouvelle de `tab:matrice-flux` ; **QM5** : N-3, N-5, N-6 et τ_F levier à 0 retenus avec M33 ; **QM6** : m visé par l'expert pilote (`macro`) ;
- **QM3, QM4, QM8**, forme de π\* et de i_res : qualifiés par `architect-approfondi` (Opus) avant `docwriter` ;
- numéros de ligne de la spécification cités dans les § 1 à § 8 des fiches : laissés tels quels, datés du commit lu (le § 9 de la fiche 8 en donne la correspondance à `9cc1ead`).

Suite, le même jour, sur le compte rendu d'`architect-approfondi` (Opus ; ADR 0011 accepté et annotations, `a8c4209`) :
- symboles fixés par `architect` sur délégation : **θ_CB** (ex-s_CB), **ν_G** (ex-m, encaisse visée M^G\*_t = ν_G × PB_t), **PB_t** (ex-P, paiements bruts) ; le mainteneur ajoute le renommage de s_G et s_Tr en **θ_G** et **θ_Tr** ;
- **points P1 à P6 de l'ADR 0011 confirmés** : perte non couverte de la banque centrale en 8 (b), État écrivain sans ordre interne (P1) ; transferts et impôt planifiés en phase 2 (P2) ; assiette Y^HS écrite en phase 7, non dans le groupe de la phase 9, date π\*^pas_t (P3, lecture de M29 qui s'écarte de celle de `macro`) ; impôt non recouvré en vérification seule du noyau, violation = défaut, limite déclarée, part non payée au bloc payeur (P4, corrige E13 de la fiche 9) ; ordre de la phase 1 « moteur (leviers), puis travail, banque centrale » (P5) ; i_res ≡ i_CB identité de notation (P6) ;
- **source du paramètre π\*** : table du bloc 8, valeur par archétype dans `scenarios/` (décision citant M30 et M32 ; annotation de l'ADR 0010).

Suite, le même jour, sur les validations de `sec:banque_centrale` (`monnaie`, `macro`, `jeu`) et de `sec:finances_publiques` (`macro`, `monnaie`) :
- **critère J1 de la fiche 9 (C10 de `macro`)** : la dette brute est publiée à ν_G = 1 et en forme fermée en ν_G, puis à la valeur retenue dès qu'elle est fixée ; seuil : égalité à la dernière décimale publiée (correction prospective, avant l'essai) ;
- **libellé « dominance budgétaire »** (valeur φ = 0) gardé, l'analogie avec Leeper (1991) étant déclarée non établie (la règle de taux n'entre dans aucune de ses classes ; constat C2 de `monnaie`) ;
- **issue #83 créée** (republier les chiffres de `sec:banque-stationnaire` et les niveaux du bloc État et dette à la richesse résolue et à la valeur retenue de ν_G ; script de la n° 4 bis) ;
- choix de la session, sans décision : la ligne « Couverture des intérêts » ajoutée par `docwriter` à `tab:leviers-cadre` est retirée (C9 de `macro` ; ADR 0011 : table inchangée ; φ figure dans `tab:leviers`) ;
- intervalle ]1 + r̄ ; 1,5[ de a_π laissé ouvert et déclaré (majeur 2 de `monnaie` sur `sec:banque_centrale`) : toute calibration dans cet intervalle demande un avis de `jeu`.

Revue finale (rang 12) : `monnaie-approfondi`, `macro-approfondi` et `jeu` sur le diff de la spécification à `e4ba6c0`. Décisions du mainteneur du 04/10/2026 :
- **assiette de l'impôt des ménages nette de la couverture des intérêts** (E12 − T^cou ; décision citant M33) : la double reprise sous φ = 1, relevée indépendamment par `macro` et `monnaie`, est levée ; état stationnaire et chiffres du J1 inchangés ;
- commentaires de `jeu` publiés sur #79 et #82 (mention sous φ = 0, précurseurs, aide, scénario de bascule de φ ; condition 8 de la fiche 7).

#### Décisions du mainteneur sur la branche n° 4 bis (rangs 2 à 7, 05/10/2026)

Prises le 05/10/2026, **toutes selon l'avis des experts** (`macro`, `monnaie`, et `jeu` pour la propriété J-ν) ; aucun numéro M (critères avant l'essai, visa d'un tableau avant / après, lecture d'un critère, corrections prospectives, triage). Sources : commentaires du 05/10/2026 sur #84 (critères et décisions, ids 5998959718 à 5998960241 ; amendement, 6000577937), #80 (remesure, 6000009761 ; profil en ζ, 6000577734) et #82 (5998963313, 6000578203) ; corps de #87 à #92 ; corps de la PR #85. Consignées par `architect` à la tête `6631f7d`.

- **Critères du script (#84, rang 2), validés avant l'essai** :
  - croissance : g_pr = 2 % et g_N = 0 (lecture I1 de `macro`) ;
  - seuil « dernière décimale publiée » lu en **arrondi au plus proche** : |écart| ≤ 0,5 unité de la dernière décimale, dans l'unité publiée ;
  - seuils de `sec:investissement-conditions` (bloc 6) laissés au J3 (#55), hors du critère de J1 ;
  - points de grille hors domaine **publiés et déclarés** : n_a = 4 (D_F de fin de phase 4 négatif, q1, P24 ; publié comme constat avec ν_F,min) et ν_G = 1 (point de référence de la forme fermée, jamais valeur de table) ;
  - #80 jugée en **lecture (α)** : max − min de r̄_α sur π\* ∈ {0 ; 2 ; 10 %}, à n_a = 12 et ν_G = 1, seuil de 0,1 point, test en `xfail(strict=True)` ;
  - forme Haig-Simons du taux réel (M8) écrite **sur i_CB** (i_CB − n_a·π^pas), déclarée ; texte du critère 13 (b) de la fiche 8 corrigé au rang 7 ;
  - propriété J-ν (fixation de ν_G) dans la **formulation de `jeu`** : marge m_ν = 1 − 1,10·Γ̄·(G/PB)/ν_G ≥ 0,03 au pire point de la grille π̄ × n_a.
- **#80 et visa du rang 4** :
  - i^ref de E4 en **lecture A** (garde le paramètre r̄) ; **norme ϱ̄_L de S2 tenue** à sa valeur de l'état résolu à π\* = 2 %, r̄ = 1 %, au même n_a (`sec:investissement-taux`) : sous la norme recalculée, la mesure n'est pas définie (couverture des intérêts et canal rentier, démontré par `monnaie`) ;
  - allocations jugées selon la **liste L2**, écrite au critère 13 (a) de la fiche 8 : sous le seuil de 0,1 point, C/Y_o, ti, tu ; invariance exacte, V_H/(n_a·YD^HS) ; publiés en mesure seulement, C, G, I et ΔIN rapportés au PIB ;
  - **ν_G = 1,15** (proposition de `macro`, QM6 ; ν_G minimal pour la marge J-ν ≥ 0,03 au pire point, n_a = 4 : 1,1313, script) ;
  - **visa du tableau avant / après : 25 écarts** (dette consolidée à n_a = 4 et 52, Y^HS/PIB, G/PB et ses conséquences — marge de E1, borne de ν_G, marge J-ν —, sensibilité de la fermeture monétaire, profil de r̄_α et lignes liées de #80, racines parasites, écarts de C/PIB ; décompte de l'historique du script : 25 valeurs), et, sous le même visa, niveaux de #83 republiés à la richesse résolue et à ν_G = 1,15. Après republication, le script rend « 289 valeurs comparées, 282 égales sur l'état résolu, 7 égales en arithmétique de la spécification […], aucun écart » (mesure d'`architect` à `6631f7d`). Verdict de #80 : **non tenu** (Δr̄_α = 0,632 point ; tu, 2,178 points) ; l'ancien verdict reste publié, anciennes valeurs barrées avec leur provenance (maquette de la fiche 9 perdue).
- **Fermeture monétaire réexpliquée** : la sensibilité publiée (0,026 % par point, environ 38 points de r̄ par point de PIB) avait le mauvais signe et un autre objet ; elle se lit désormais comme une **différence entre archétypes** (dθ_G/dr̄), distincte de la réponse d'un pays dont la règle déplace r̂ (#88). Les chiffres dynamiques **+96 pb et 0,28 %** (`sec:finances_publiques-conditions`, `-impots`) gardent la mention « non remesuré » jusqu'au J3 ; ~~motif : la forme fermée donne l'arrivée, non le tour publié~~ (motif contredit par la spécification, qui présente ces chiffres comme une arrivée ; revue finale de `macro`, rang 8) : la forme fermée en contredit la valeur d'arrivée (+141 pb à ζ = 4, +70 pb à ζ = 8 ; 0,42 % du PIB), cause non établie, mention ajoutée dans la spécification (décision du mainteneur du 05/10/2026, après le rang 8) ; remesure dynamique au J3 (#88, point 1).
- **Corrections prospectives des critères du J3** (aucun essai fait ; textes d'origine publiés) :
  - critère de la marche de cible de 2 à 3 % **indexé sur ζ calibré** (0,8185 % à ζ = 4 ; 0,9188 % à ζ = 8 ; ± 0,01 point ; #91) ;
  - dans L2, **I^vol/y à la place de ti et C/PIB à la place de C/Y_o** (l'étendue de ti s'annule à ζ = η_r : artefact de calibration) ; le verdict présent reste « non tenu » ;
  - critère 13 (a) de la fiche 8 précisé (liste L2) ;
  - **§ 7.1 de la part `monnaie` des critères amendé** (ϱ_L recalculé, norme ϱ̄_L tenue ; exemples et verdict attendu remesurés, § 7.2 à 7.4) ;
  - **critère J3 de la racine (C51) réécrit** (`6631f7d`) : racine unique sous φ = 1 ; sous φ = 0, racines publiées et arrivée du moteur comparée à la racine du domaine à 0,01 point.
- **Issues créées le 05/10/2026** (rédigées par les agents, création approuvée) : **#87** (q1 : D_F ≥ 0 hors de l'état stationnaire et selon n_a ; J3 ; P24 (a)) ; **#88** (fenêtre longue : arrivée et gain de long terme de la fermeture monétaire après un choc budgétaire permanent, selon φ et ζ) ; **#89** (recherche de stratégie dominante sur les combinaisons de leviers ; J4) ; **#90** et **#91** (modules `banque.py` et `banque_centrale.py` ; J3) ; **#92** (calibration de μ̄ sur une source lue ; J3). Toutes `needs-triage`.
- **Commentaires versés** : #84 (critères et décisions ; amendement de `monnaie`) ; #80 (remesure, profil en ζ et corrections prospectives) ; #82 (affichage de la « hausse maximale servie ce tour » et infobulle de la dette brute, amendant la condition 2 du § 9.5 de la fiche 9 ; τ_F « fermé au socle »).
- **Décisions du mainteneur après la revue finale (rang 8), 05/10/2026**, selon l'avis des experts et de l'audit :
  - +96 pb et 0,28 % : gardés « non remesurés », annotés « non reproduits par la forme fermée » (point ci-dessus) ;
  - **critère J3 de la racine (C51), correction prospective de `monnaie`** : sous φ = 0, racines publiées avec le signe de dθ_G/dr̂\* en chacune ; trajectoire du moteur classée sans présomption (arrivée à une racine à 0,01 point près, ou divergence : tour où i_CB s'écarte d'un point de sa valeur de départ) ; aucune arrivée exigée ; inchangé sous φ = 1 (le texte de `6631f7d` reste publié) ;
  - **visa de quatre valeurs supplémentaires** de la fiche 9 (dette consolidée à n_a = 4 et 52, π̄ = 0 et 10 % : 0,09466 / 0,49978 / 0,10045 / 0,51438 → 0,09880 / 0,51172 / 0,09886 / 0,50952 ; σ en pas dans la maquette) : republiées en `c9d6d6e` ;
  - **contrôle automatique des valeurs en vigueur** (audit, constat majeur M1, accord de `monnaie`) : lignes d'illustration B-1 gardées en contre-épreuve des formes, hors bilan ; valeurs en vigueur (niveaux bancaires, `tab:etat-stationnaire`, niveaux restitués) ajoutées à la comparaison ; test exigeant chaque valeur en vigueur hors `\barre` dans sa source ; bilan republié, l'ancien gardé avec la mention « incluait 45 valeurs barrées ». Changement de décompte, non de résultat.
- **Décisions de session du 06/10/2026 (fin du rang 8)**, prises par la session selon l'avis des experts (questions de forme et de classement, aucun résultat final changé ; aucun numéro M) ; consignées par `architect` à la tête `ea2c438` :
  - **forme de la fiche 9 selon `macro`** : anciennes valeurs du critère 13 barrées et republiées dans le tableau du § 3.C, § 6.2 gardé en trace d'instruction (`a225e45`, échec attendu retiré en `5eaed92`) ;
  - **classement de +0,182 selon `monnaie`** : valeur mesurée sur l'état résolu, passée de la catégorie S à la catégorie D (`28a37d9`, `86b543f`) ; effets d'une hausse d'un point de r̄ comparés (+0,157, +0,308, −0,058, +0,074) et `tab:calibration` retenue en seconde source des trois valeurs ν_G, selon `monnaie` et `macro` ;
  - **retouche m9 de `macro` retirée par `macro`**, la barre gardée (`181d2fa`) ;
  - constat mi-C de l'audit **reporté** (mineur, sans effet sur la spécification actuelle), proposé à l'issue de rattachement des valeurs de fiche (point (b) du rang 9, § 1).
- **Décisions du mainteneur du 06/10/2026 (points (a) à (d) du rang 9)**, toutes selon l'avis des experts (forme, classement, organisation ; aucun résultat final changé ; aucun numéro M) ; consignées par `architect` à la tête `767e5a1` :
  - **(a) cellule « Racines » de la colonne C-HS du § 3.C de la fiche 9 barrée** et republiée, selon `macro` : une racine à chaque cible (1,632 / 1,000 / 1,146 %, sortie du script d'état stationnaire) ; anciennes racines de la maquette perdue barrées (`767e5a1`) ;
  - **(b) issue #93 créée** (« Test de source : rattacher les valeurs de fiche à leur paragraphe ou à leur ligne de tableau » ; `enhancement`, `needs-triage`), qui couvre aussi mi-C et les valeurs non comparées de `sec:investissement-taux`, selon `monnaie` ; rattachée au § 3, sans branche fixée ;
  - **(c) unification des conventions des valeurs à ν_G = 1** (crochets aux blocs 7 et 8, barre « maquette » au bloc 9), selon `macro` : **consignée pour le J3**, commentaire déposé sur #88 (https://github.com/Gerard-Garey/projet_macro/issues/88#issuecomment-6022788365) ;
  - **(d) précision r2 de `macro` confirmée** (« la racine du domaine n'est pas toujours unique », `76616c2`), qui touche le motif d'une décision du 05/10/2026 déjà appliquée (critère J3 de la racine, C51).
- **Décisions du mainteneur du 07/10/2026 (fin du rang 9)**, aucun résultat changé ; aucun numéro M (validation d'un critère de passage arrêté par M19 et choix d'organisation) ; consignées par `architect` sur `main` = `833afd9` :
  - **passage du jalon J1 validé le 07/10/2026**, après la fusion de la PR #85 (`833afd9`), **en connaissance des réserves déclarées** : (1) superneutralité non tenue (critère 13 de la fiche 8, lecture (α) ; verdict du visa du 05/10/2026, ci-dessus), défaut connu publié selon M32 et codé en échec attendu (`xfail(strict=True)`), suivi par **#80**, ouverte jusqu'au J3 ; (2) limites du test de source reportées à **#93** (constat mi-C de l'audit, inversions de signe non détectées, sept valeurs non comparées de `sec:investissement-taux`) ;
  - **consignation sur une branche dédiée** `claude/j1-passage`, partie de `833afd9`, par PR directe vers `main` (choix du mainteneur) ; elle n'est pas une branche de travail et ne porte que la présente consignation (`docs/feuille-de-route.md`, `docs/blocs/README.md`), sans résultat changé ; le point d'étape qui fixera la branche suivante (J2, noyau) est fait ensuite, séparément.

#### Décisions des 07/10 et 14/10/2026 (branche J2, condensées le 15/10/2026, P48)

Points soumis au mainteneur pendant la branche J2 (`claude/j2-noyau`, PR #99), **tous décidés par lui**, sans numéro M (organisation, périmètre, précisions de forme de l'ADR 0012 accepté ; aucun résultat publié changé). Une ligne par point ; les avis, options écartées et motifs complets sont dans la PR #99, dans les annotations datées de l'ADR 0012 et dans la version de la présente feuille de route à `8511ba3` (dernière version non condensée). Identifiants : P28 à P37 (point d'étape du 07/10/2026) ; « 1a-1b », « #95-n », « #96-n », « N-n », « C-n », « #97-n », « R-n » (décisions du 07/10/2026 par rang et par constat) ; « 14/10-n » (décisions du 14/10/2026).

| N° | Date | Décision | Consignée |
|---|---|---|---|
| P28 (a) | 07/10/2026 | Consignation du passage de J1 sur la branche dédiée `claude/j1-passage` (PR #94, `faa3f85`) : exception ponctuelle sans précédent ; à partir de J2, passage validé avant la fusion et consigné dans la branche | `c43883a`, `f021b13` ; écart E1 au passage de J2 (P38) |
| P29 (a) | 07/10/2026 | Feuille de route condensée à l'ouverture de J2 (fiche de J2 au § 1, P1 à P27 en une ligne par point, tableau M inchangé) ; motif : 170 199 octets à `6dc9174` | `c43883a`, `f021b13` |
| P30 (a) | 07/10/2026 | Périmètre de J2 : #95, #96, #97, #98 et #93 (rang 1c, circuit 3), avec `Closes` | `c43883a`, `f021b13` |
| P31 (a) | 07/10/2026 | ADR d'architecture du noyau, de l'ordonnanceur et du schéma d'état au rang 1a, avec Fable (1 sur 3), accepté avant tout code | ADR 0012 (`294ba78`, accepté `44b5c50`) |
| P32 (a) | 07/10/2026 | Ordre de la concordance : code sans balise pendant la branche ; au rang 6, balises (`code:`) et labels (`docs:`) poussés ensemble, par issue | `c43883a`, `f021b13` |
| P33 (a) | 07/10/2026 | Échelle S évaluée à l'ouverture du pas (confirmée au rang 1b) | ADR 0012 |
| P34 (a) | 07/10/2026 | #61 au J3 avec #91 ; radical `prix` pour P4 (`eq:prix-indice`, avec #51) ; 17 labels en J2 (18 après #95-4) | annotation de l'ADR 0008 du 07/10/2026 |
| P35 (a) | 07/10/2026 | Triage : #93 et #95 à #98 en `ready-for-agent` ; #11 et #14 `ready-for-human`, hors branche | session, 07/10/2026 |
| P36 | 07/10/2026 | Revue de fond du rang 7 bornée à `sec:cadre` exécutée contre le code ; `jeu` et `app-review` non déclenchés ; bilan du journal à coller dans la PR | `c43883a` ; écart E2 (bilan non collé) |
| P37 (a) | 07/10/2026 | Délégation technique reconduite pour J2 ; `archive/` : rien à décider (suppression fin J6, M6) | `c43883a`, `f021b13` |
| 1a-1 | 07/10/2026 | ADR 0012 accepté ; points 1 à 7, 10 et 11 selon la recommandation | `294ba78`, `44b5c50` |
| 1a-2 | 07/10/2026 | Point 9 : (α), plus petit S des secteurs touchés | ADR 0012 |
| 1a-3 | 07/10/2026 | Point 8 : (iii-b), hybride par structure, sur l'instruction de Fable (2 sur 3) : Res ≥ 0 strict, lecture nette de la caisse à x ≥ −ε × S_payeur, montant couvert c de la ligne 16 (amendement de A3.2), contrat de poussière | ADR 0012 |
| 1a-4 | 07/10/2026 | Tolérance de la lecture nette : précision de M22, lecture (B), sans nouveau numéro | annotation de l'ADR 0005, point 10 |
| 1b | 07/10/2026 | P33 (a) confirmée avec trois précisions ; V^flux variable d'état du noyau ; critères complémentaires sur #95 à #98 | fiche 1 § 9.9 (`8a2dfd3`) |
| #95-1 | 07/10/2026 | A2 : liste des lignes admettant un montant négatif (ligne 7 ouverte par ligne) | annotation de l'ADR 0012 (questions de `coder` sur #95), `a3883c1` |
| #95-2 | 07/10/2026 | A3.2 : déclaration du montant couvert obligatoire si Π < 0 ; c = 0 admis | idem |
| #95-3 | 07/10/2026 | G5 : ligne 19b exercée par un double du catalogue dans les tests | idem |
| #95-4 | 07/10/2026 | A5 : label `eq:noyau-caisse-nette` (18 labels en J2) ; ΔM et ΔH, un label chacun | idem ; ADR 0008 (renvoi) |
| #95-5 | 07/10/2026 | A3.1 : S finie et > 0 ; `t` entier ; `GrandLivre` construit seulement par `ouvrir_pas` | idem |
| #95-6 | 07/10/2026 | A3.3 : clôture sans ligne saute ses contrôles, résultat égal, testé ; phase 9 jamais sautée | idem |
| #95-7 | 07/10/2026 | A5 : portes des contreparties 17, 20 et 22 évaluées | idem |
| #95-8 | 07/10/2026 | E3 : « 26 `proposer` » = 25 propositions plus une déclaration de montant couvert | idem |
| #96-1 | 07/10/2026 | D1 : `identifiant` et `graine` champs d'identité de `EtatPays` ; graine ≥ 0, identifiant non vide ; ordre canonique par point de code | annotation de l'ADR 0012 (questions de `coder` sur #96), `07f0ecf` |
| #96-2 | 07/10/2026 | C1/F2 : vocabulaire fermé unique des unités, complété ; invariance `indice` sous ×100 | idem |
| #96-3 | 07/10/2026 | E2 : nom `ReleveDesResidus` (ASCII) | idem |
| #96-4 | 07/10/2026 | E1 : `FinDePas` relève les montants exécutés des `ClotureDePhase` | idem |
| #96-5 | 07/10/2026 | G1 : lieu d'assemblage du schéma laissé ouvert (tranché le 15/10/2026, P40) | idem |
| N-1, N-2 | 07/10/2026 | Graine dans [0 ; 2^64[, `t` entier ≥ 0 ; identifiant UTF-8 sans contrôle ni espace de bord ; module `nations.etat.unites` ; `VERSION_SCHEMA` reste à 1 | compléments à l'annotation, `7abc82c` ; code `1f8917a`, `0564220` |
| C-1, C-2 | 07/10/2026 | `t` dans [0 ; 2^63[ (`T_EXCLU`) ; identifiant en NFC, sans `Cf`, `Zl`, `Zp` ; diagnostic de type faux corrigé | seconds compléments à l'annotation, `7d52fbf` |
| #97-1 | 07/10/2026 | Projet d'annotation approuvé (points 1 à 9) : `assembler(phases, blocs, parametres, entrees)`, indice `"P"`, test « conversion unique », aucun attribut d'instance de bloc | annotation de l'ADR 0012 (questions de `coder` sur #97), `CONTEXT.md` ; `e8d4dc2` |
| #97-2 | 07/10/2026 | Colonne « Lisent » de `tab:phases` normative et contrôlée ; phase 2 ajoutée à la phase 6 | idem (point 10) |
| #97-3 | 07/10/2026 | Coût : aucun allègement du moteur ; mesure de référence en CI avec #98 | idem |
| #97-4 | 07/10/2026 | `audit` non conforme : reprise unique de `coder` | `657591c`, `b2800c7` |
| R-1 | 07/10/2026 | La phase 7 lit aussi la phase 2 (T^cou) | compléments du point 10, `224b1a5` |
| R-2 | 07/10/2026 | « Lisent » borne aussi les montants exécutés lus au grand livre ; contreparties en 8c | idem |
| R-3 | 07/10/2026 | Lecture interne à la phase lectrice confirmée (documentation seule) | idem |
| R-4 (M-1) | 07/10/2026 | Motif de l'échec attendu porte le numéro d'issue ; lot final R1, R2, M-1 | `201b4ba`, `e939170` |
| R-5 | 07/10/2026 | Coût après reprise : 0,63 à 0,68 ms par pas avec blocs d'essai (poste de session) | idem |
| 14/10-1 | 14/10/2026 | #93 lancé par `circuit-technique 93` sur commande du mainteneur | § 1 de J2 (`8511ba3`) |
| 14/10-2 | 14/10/2026 | Constat C1 (vue `LectureDuGrandLivre`) hors périmètre : issue #100 | idem |
| 14/10-3 | 14/10/2026 | Seuil du coût du noyau seul affirmé sur la plateforme de référence seulement ; saut explicite ailleurs | annotation de l'ADR 0012 du 14/10/2026, `da7603e` |
| 14/10-4 | 14/10/2026 | M^G ≥ 0 exact à la clôture de 8 (b) si M^{G,8a} ≥ 0, sinon poussière admise (précision, non déplacement de critère) | idem |
| 14/10-5 | 14/10/2026 | Libellés de 0,110 (β) et 0,921 corrigés en « fiche 9 § 6.3 » | `34c227d`, `b516337` |
| 14/10-6 | 14/10/2026 | Borne basse de B_CB/S portée de −0,2 à 0, révision prospective | `899adfe` |
| 14/10-7 | 14/10/2026 | Sortie du brouillon de la PR #99 si revue finale conforme et CI verte | § 1 de J2 (`8511ba3`) |
| 14/10-8 | 14/10/2026 | Création directe des issues hors périmètre autorisée : #100 à #106 | idem |
| 14/10-9 | 14/10/2026 | Fable 3 sur 3 autorisé en cas de désaccord entre experts ; non utilisé | idem |

#### Décisions du mainteneur du 15/10/2026 (point d'étape après la PR #99, P38 à P48)

Points soumis par `architect-approfondi` (Opus, effort `high`, lecture seule) au point d'étape après la fusion de la PR #99 (`main` = `2e643a2`) ; **décidés par le mainteneur le 15/10/2026, toutes les recommandations retenues** ; sans numéro M. Consignés au rang 0 de J3-a par `architect` (feuille de route) et dans les annotations des ADR 0012 et 0008 et `docs/blocs/README.md` (rédigées en parallèle).

| N° | Décision |
|---|---|
| P38 (a) | Passage de J2 consigné au rang 0 de J3-a (§ 6) ; écart E1 à P28 (a) noté : passage validé à la fusion, non consigné avant. |
| P39 (a) | J3-a = #107 (critères de J3, créée le 15/10/2026), #105, #65, #66, #100, toutes avec `Closes`. J3-b à J3-e indicatives (§ 2). |
| P40 (a) | G1 tranchée : les `VariableEtat` sont déclarées dans `etat/`, un module par radical, référencées par la `DeclarationDeBloc`, bijection contrôlée à l'assemblage (forme déjà lue par `assembler`, annotation de l'ADR 0012 sur #97, point 9). Schéma statique, versionné à un seul endroit ; reprise indépendante des blocs. Coût : une variable se touche à deux endroits, protégés par un test. Annotation de l'ADR 0012, pas de nouvel ADR. Échéance corrigée (E4) : avant le premier module de bloc (le bloc 2 a déjà des variables d'état v^e, IN^vol, pr, K^vol ; spécification l. 1093), et non plus « avant #61 ». |
| P41 (a) | Ordre des modules : J3-b (blocs 2 à 4) → J3-c (blocs 7, 8 et #61) → J3-d (blocs 5, 6 et 9) ; π\*_t écrite par le bloc 8 (P34 (a)), lue par les blocs 5 et 6. Ce n'est pas l'ordre d'instruction de `docs/blocs/README.md` § 3 (les fiches sont toutes instruites). |
| P42 | #87 et #88 en J3-e (trajectoires dynamiques, socle complet requis) ; estimation préliminaire facultative sur la maquette. Dépendance #65 → #87, #88 retirée. |
| P43 (a) | Une branche de calibration (#45, #55, #62, #92) dans J3, avant J3-e ; confirmation au point d'étape de J3-d. |
| P44 (b) | Radical `observation` : `eq:observation-ratio-pib-annuel` (fiche 1 § 9.8, n° 7). Annotation de l'ADR 0008 ; `docwriter` ajoutera le radical à `CONVENTIONS.md` § 2.1 à son passage (rang 6). |
| P45 | Fiche 1 « implémentée » dans `docs/blocs/README.md`, en déclarant trois labels renvoyés au J3 (`eq:prix-indice`, `eq:moteur-croissance-nominale-attendue`, ratio au PIB annuel). L'historique du 07/10 dit « 17 labels » : ligne datée du 15/10 qui donne 18. |
| P46 (a) | Identifiants Cn et Co refusés : issue #108, rattachée à J5. |
| P47 (a) | Délégation technique reconduite pour J3-a, comme P37 (a). Rappel : #11 et #14 attendent toujours le mainteneur. |
| P48 (a) | Feuille de route condensée au rang 0 : la fiche de J2 sort du § 1 ; les décisions des 07 et 14/10 sont condensées à une ligne par point, comme P29 (a). Motif : deux arrêts à 40 tours sur J2 (taille des documents lus : feuille de route 149 667 octets, ADR 0012 114 509 octets). |
| Fable | Seuil « macro » (`docs/agents/routage.md` § 4.3, critère 2) atteint par le découpage de J3 ; consultation Fable proposée au mainteneur, qui la reporte au plan de J3-b (elle comptera pour J3-b). Budget Fable de J3-a : 0 sur 3. |

**Écarts relevés au point d'étape du 15/10/2026** : E1 (P28 (a) : passage de J2 validé à la fusion, non consigné avant ; consigné par P38) ; E2 (P36 : aucun bilan du journal collé dans la PR #99 ; `bilan_journal.sh` rend « Journal vide ou absent » en session cloud, calibration partielle) ; E3 (#65 : amendement P23 (a) jamais porté sur l'issue ; **corrigé le 15/10/2026**, commentaire https://github.com/Gerard-Garey/projet_macro/issues/65#issuecomment-6185209845) ; E4 (échéance de G1, corrigée par P40).

**Points ouverts au 15/10/2026** : #11 et #14 (mainteneur, hors branche) ; consultation Fable au plan de J3-b (report du 15/10/2026) ; confirmation de la branche de calibration au point d'étape de J3-d (P43 (a)). Sortis de la liste : borne de B_CB (exécutée, `899adfe`) ; domaine des niveaux du registre des prix (`3b364bd`, `0e63473`) ; littéral 12 (porté par #102) ; G1 (tranchée, P40) ; identifiants Cn et Co (P46 (a), #108).

#### Décisions du mainteneur du 15/10/2026 sur les rangs 1 à 4 de J3-a

Décisions de fond prises par le mainteneur le 15/10/2026 pendant la branche J3-a, sur les avis de `macro-approfondi` et `monnaie-approfondi` et les audits de #65, #66, #100 et #105 ; consignées sur #107 et dans le corps de la PR #109 ; sans numéro M. Consignées par `architect` (Opus, effort `medium`, consignation).

| N° | Décision |
|---|---|
| D1–D13 | Critères de J3 arrêtés **avant tout essai** : tableau commun A1–I1 de `macro` et `monnaie` (commentaire 6185745866 sur #107, 06:12 UTC) et décisions D1 à D13 (commentaire 6185995449, 06:30 UTC). D3 : niveaux d'O1 = contrôles de calibration à t = 0, adossés à une source lue ; verdict « O1 non tenu à r̄ = 1 % » (r = 1,02 %) publié et conservé. D12 : tableau `tab:criteres-j3` dans `sec:calibration` (« proposée »), rédigé au rang 6 (`f80c34a`) ; annotation datée de `docs/exigences.md` § 1.3 (la liste du 16/09/2026 reste publiée) ; renvoi au § 6. |
| G1 | Budget du socle complet : N = 10 exécutions, marge m = 0,60, max_k C_k ≤ 2,708 ms (commentaire 6186123808 sur #107, 06:39 UTC), sur proposition de `macro` (option A) et mesure de #105 (C = 0,2698 à 0,4308 ms, deux modes). |
| F2, S1 | Décidés après mesure sur les maquettes (#65, #66), **avant tout essai sur le moteur** ; lecture des bandes « ± x = demi-largeur » (commentaire 6187825407 sur #107, 08:26 UTC). |
| Socle | Stabilité du socle des blocs 2 à 9 : **publier les remesures** (visa du mainteneur). Cause établie par `monnaie`, confirmée par `macro` : chiffres mesurés avant l'ajout de −T^cou à E12 (amendement du 04/10/2026) ; sans −T^cou, la maquette reproduit les chiffres publiés à la 6e décimale. Lecture (c) du rayon à π̄ = 0 (variété des identités, hors des deux racines des stocks de la banque centrale tenus en niveau, déclarées). Anciennes valeurs barrées, tableau avant / après au commit `docs:` de #65 (`1e24ba3`). |
| Grille | Grille de 29 branches (a_U sans objet sous M32, BC1 sans terme d'activité), plus ζ ∈ {2 ; 4 ; 8} en prospectif (31 branches) ; verdicts publiés sur 29 et 31 ; **marge conjointe publiée** (β, a_π, η_r ensemble ; frontière ×1,71 en régime de baisse de l'emploi, à π̄ = 2 % (1,9921 en hausse)), qui limite la phrase « rayon < 1 sur toute la grille » à la stabilité un paramètre à la fois et toutes vitesses ensemble. |
| `tab:instabilites` | Variantes écartées de F (#66) : **seconde écriture indépendante d'abord**, dans la maquette de #65 sans lire la contre-épreuve ; ligne versée seulement si concordance au 4e chiffre avec #66. Concordance établie (`50daa4c`) ; **ligne 18 versée** et `sec:ecartees` chiffrée et nuancée (`f2d6291`). |
| Issues | Création de #110 (processeur de l'exécuteur en CI) et #111 (trajectoires C-HS publiées avant l'amendement de E12, à remesurer) ; rattachement au point d'étape suivant (§ 3). L'issue proposée par `coder` sur #100 (positions, ouverture, échelles, valeurs nettes hors du filtre de lecture) n'est pas créée : à soumettre au mainteneur (annotation du 15/10/2026 de l'ADR 0012, #100). |

#### Décisions du mainteneur du 13/11/2026 (point d'étape après la PR #109, P49 à P64)

Points soumis par `architect-approfondi` (Fable, consultation accordée par le mainteneur le 13/11/2026, 1 sur 3 pour J3-b) au point d'étape après la fusion de la PR #109 (`main` = `204ab2d`) ; **décidés par le mainteneur le 13/11/2026** : P49 à P53, P55, P58 à P62 et P64 acceptées ; P54, P56, P57 et P63 acceptées **sous réserve de l'avis de `macro`** au rang 1a de J3-b (retour au mainteneur seulement si l'avis est contraire) ; sans numéro M. Consignés au rang 0 de J3-b par `architect` (feuille de route, `CONTEXT.md`). Issues créées le 13/11/2026 : A = #112, B = #113, C = #114, D = #115, E = #116.

| N° | Recommandation | Décision |
|---|---|---|
| P49 | Périmètre de J3-b : #112, #113, #50, #51, #104, avec `Closes` | acceptée |
| P50 | #102 en correctif rapide avant l'ouverture ; critère « aucun littéral 12 dans `src/` hors de `cadre.py` » | acceptée |
| P51 | #106 hors de J3-b ; fermeture par retrait en J3-d, sauf consommateur déclaré | acceptée |
| P52 | Socle partiel d'essai dans `tests/` seulement, sentier tiré du script ; stationnarité partielle comme critère d'acceptation de J3-b, J3-c et J3-d ; termes « socle partiel d'essai » et « bloc d'essai sur le sentier » dans `CONTEXT.md` | acceptée |
| P53 | Schéma v2 en une fois (variables des blocs 2 à 4, plus π^e), une version par branche ; nomenclature fixée par annotation de l'ADR 0012 avant le code, sans nouvel ADR | acceptée |
| P54 | μ̃ portée en variable d'état du bloc 4 (option (ii) des fiches 3 et 4), pour que N9 ne soit pas inversée dans les blocs 3 et 4 | acceptée sous réserve de l'avis de `macro` |
| P55 | Rang 1a avant tout code ; issue de suivi #114 ; amendements versés sur #50, #51, #104, #106, #102 | acceptée |
| P56 | T2 (b) lu sur le moteur à n_a = 12 seulement, π̄ ∈ {0 ; 2 ; 10 %} ; n_a ∈ {4 ; 52} couvert par le script (T2 (a)). Correction prospective, ancien texte publié | acceptée sous réserve de l'avis de `macro` |
| P57 | Part d'un bloc dans le coût définie avant l'essai ; seuil d'alerte non bloquant de 0,276 ms = (52/12/1,60 − 0,5)/8 ; le critère de 0,48 ms reste publié | acceptée sous réserve de l'avis de `macro` |
| P58 | Lectures d'ouverture, de positions et du registre : contrôle statique, pas de filtre à l'exécution ; annotation datée de l'ADR 0012 | acceptée |
| P59 | Issues de la passation de #109 : #115 créée (J3-e) ; #116 créée, regroupant relevé des fiches et point fixe (J3-f) ; cache de `lectures` abandonné comme issue ; filtre à l'exécution proposé par `coder` (#100) abandonné, remplacé par le contrôle statique (#112, point 6) | acceptée |
| P60 | Rattachements : #110 → J3-g ; #111 → J3-f avec #88 ; #87 → J3-f | acceptée |
| P61 | Queue de J3 en trois branches indicatives (J3-e, J3-f, J3-g), à fixer au point d'étape de J3-d | acceptée |
| P62 | P32 (a) reconduite : code sans balise pendant la branche ; balises et labels poussés ensemble au rang 8 | acceptée |
| P63 | Table du moteur à g_N = 0, valeur de l'état de référence ; ligne g_N de `tab:calibration` mise en accord au rang 8 ; test d'égalité entre table du moteur et script | acceptée sous réserve de l'avis de `macro` |
| P64 | Délégation technique reconduite pour J3-b. Rappel : #11 et #14 | acceptée |

**Contexte : constats du point d'étape du 13/11/2026** : (1) `assembler` refuse un écrivain de `tab:phases` sans implémentation (`ordonnanceur.py:643-644`) → socle partiel d'essai (P52) ; (2) n_a est une constante du moteur (`conversions.py`, `registre.py`, `schema.py`) → T2 (b) inexécutable à n_a ≠ 12 (P56) ; (3) la part de 0,48 ms par bloc donnerait 8 × 0,4815 + 0,4308 = 4,283 ms > 2,708 ms → seuil d'alerte (P57) ; (4) aucun bloc ne lit `variation_sur_le_tour` → #106 hors de J3-b (P51). **Écarts relevés** : `tab:calibration` g_N = 0,005 contre g_N = 0 dans `outils/etat_stationnaire.py:114` (P63) ; unités de `tab:calibration` hors de `UNITES` (#104) ; la feuille de route (en-tête et § 1, version du 15/10/2026) annonçait la tête `13146ff` alors que la tête fusionnée est `5fe2667` (corrigé dans l'en-tête le 13/11/2026).

Seuil § 4.3 : le redécoupage de la queue de J3 (P61) relève du critère 2 ; instruit par la consultation Fable accordée. Aucun nouvel ADR d'architecture ; tension T2 (b) / ADR 0005 et ADR 0012 F1 levée par P56 ; question ouverte de l'annotation du 15/10 de l'ADR 0012 (point 4) fermée par P58 (annotation au rang 1b).

**Rang 1a de J3-b (13/11/2026)** : avis de `macro-approfondi` **favorable** à P54 (sous conditions : invariant |μ̃_t − ln(p_t/UC_t)| ≤ 1e−12 ; `\limites` sur ω = exp(−μ̃), valable sous J = 1 et sans intrants), P56 (correction prospective versée aux § 9.6 des fiches 3 et 4), P57 (part d'un bloc = durée cumulée des méthodes d'étape du bloc, socle partiel d'essai, π\* = 2 %, 720 pas, min sur 5 répétitions ; projection cumulée publiée sans seuil) et P63 (g_N = 0,005 gardée comme valeur d'essai de la ligne « Cohérence des conversions » de la fiche 3) : les quatre décisions tiennent sans retour au mainteneur. Avis de `monnaie` sur π^e lue par le bloc 3 : cinq points confirmés ; réserves : π^e > −1 est un invariant de BC3 sous 0 < λ_e ≤ n_a, π^e_0 > −1 (à contrôler au chargement d'un état, #112) et P > 0 ; hors du sentier, le bloc d'essai à π^e = π\* coupe la boucle T3 ↔ BC3 et toute mesure dynamique de J3-b est étiquetée « π^e exogène (bloc d'essai) ». Synthèse complète : commentaire de la PR #117 du 13/11/2026.

| N° | Décision du mainteneur (13/11/2026, lectures ouvertes par le rang 1a) |
|---|---|
| P65 | Unité des vitesses d'ajustement (λ_v, λ_IN, λ_w, λ_N, λ_μ) et de δ : « par an, taux de flux » (`sec:cadre-calendrier`, M22) ; « vitesse » passe dans la description de `tab:calibration` ; domaine 0 < λ ≤ n_a déclaré par paramètre (F1). Option écartée : unité « par an, vitesse » (contrat partagé). Deux unités ajoutées à `UNITES` (#104) : « u.m. par personne et par pas », « u.v. par personne et par pas ». |
| P66 | Stationnarité partielle et A2 : une grandeur de valeur résolue nulle (B7 à π\* = 0, ξ ; plus tard B8, B25, B26) se juge en valeur absolue, \|x_t\| ≤ 1e−12 (lecture « grandeurs nulles à 1e−12 près » de A2, S = 1 pour une grandeur sans dimension). |
| P67 | Stationnarité partielle de J3-b : B1 à B7, **B12, B13** et B24, à 1e−9 relatif sur 720 pas, aux trois π\*, depuis l'état résolu, sans choc ; B4 à B7 et B24 dès le pas 11 (D13). *Rédaction corrigée le 13/11/2026 (avis de `macro`, rang 3) : « B4 à B7, B13 et B24 dès le pas 11 » ; B13 est une grandeur de 12 tours, que D13 couvre (spécification l. 3463) ; le test la juge ainsi depuis `d79fbcd`.* |

| N° | Décision du mainteneur (13/11/2026, questions ouvertes par le rang 1b, annotation du 13/11/2026 de l'ADR 0012) |
|---|---|
| P68 | Maison de δ : table du bloc 6, `nations.moteur.parametres.investissement`, créée en J3-b avec δ seul (maison de la décision M28, Q11) ; ADR 0005, point 18, intact. Options écartées : (a) table du cadre (contrat de l'ADR 0005 modifié), (c) table de la production. |
| P69 | `executer_pas` passe `parametres.cadre` à `ouvrir_pas` (lettre de A3.1, signature d'`assembler` inchangée) ; les appels d'`assembler` des tests passent l'ensemble des tables de référence. Réalisé dans #112. |
| P70 | Domaine de λ_v : 0 < λ_v < n_a, strict (avec λ_v = n_a et d_t = 0, v^e = 0 et P1 n'est pas défini au pas suivant ; avis de `macro`). Correction prospective de « 0 < λ_v ≤ n_a » de `sec:production-visee`, au passage de `docwriter`. Les autres vitesses restent 0 < λ ≤ n_a. |
| P71 | U^eq > 0 et μ̄ > 0 requalifiés en conditions de conception et d'existence de l'état stationnaire (non en domaines de définition) ; `outils/etat_stationnaire.py` aligné pour les refuser dès le chargement de ses paramètres (commit `code:` dans #112, résultats identiques à la calibration). |
| P72 | Domaine de la position `IN` (ADR 0012, annotation du 13/11/2026, point 1.8), option (c) de `macro` : N8 réécrite ΔIN = cm·IN^vol_{t+1} − IN_t (forme B, algébriquement équivalente ; IN ≥ 0 exact au bit, zéro exact à l'épuisement ; aucun résultat publié changé, ≤ 7e−16) ; domaine **strict** IN ≥ 0 contrôlé dans `ouvrir_pas` du noyau, à côté de Res (A3.1 (ii) étendu), sans tolérance. Lecture retenue : lire la position d'ouverture dans le montant de la ligne 4 n'est pas un solde résiduel au sens de l'ADR 0005, point 8 (A8, règle 1). Réalisation dans #113 (bloc 2, et contrôle du noyau) ; `outils/etat_stationnaire.py` aligné sur la forme B ; spécification (N8, l. 912-919 ; domaines de l'ouverture) au passage de `docwriter`. Options écartées : (a) forme A et contrôle tolérant IN + ε·S^F ≥ 0 (recommandation d'`architect`) ; (b) aucun contrôle, max(0 ; IN) (déconseillée : borne au lieu d'un mécanisme). Position K : même domaine strict en J3-c, sans réécriture (S7 tient K ≥ 0 au bit). |
| P73 | Critère « Valorisation » de la fiche 2, § 9.6 : 1e−12 rapporté à la valeur du stock disponible IN_t + UC_t·y_t (précision écrite avant l'essai, versée à la fiche). |

**Points ouverts au 13/11/2026** : #11 et #14 (mainteneur, hors branche) ; confirmation de la branche de calibration au point d'étape de J3-d (P43 (a)) ; résolution de l'état initial par `scenarios/` sans dupliquer le script (J3-e, § 2). Sortie de la liste : consultation Fable au plan de J3-b (faite le 13/11/2026, § 8).

### 5. Pistes à instruire dans les fiches comparatives (aucune n'est décidée)

Ouvertes par M2 et M3 ; chacune sera présentée dans la fiche du bloc concerné, avec ses références vérifiées, l'avis de l'expert pilote et de `jeu`, puis tranchée par le mainteneur (M-n à venir). Une piste tranchée reste dans le tableau, barrée, avec sa décision.

| Piste | Fiche | Motif de l'instruction |
|---|---|---|
| ~~Pas de temps mensuel unique~~ — **retenue (M22, 30/09/2026)** | temps et comptabilité | Quatre fois moins de pas ; supprime l'incohérence calendaire de la v1.5 (4 pas par mois, 52 par an, glissement sur 12 mois) ; le moteur v2.0 prend 13 dates de décision par an. Pesée contre la granularité hebdomadaire des marchés dans la fiche (§ 3 à 7) : aucun fait mesuré de G à K ne l'exploitait ; réouverture par une décision M-m citant M22 si une fiche (J3, J6) établit un besoin infra-mensuel. |
| Consommation par règle stock-flux à cible de richesse (forme fermée) plutôt qu'une optimisation à chaque pas | ménages | État stationnaire calculable ; compatible avec l'invariant 11 de l'ADR 0002. |
| Corridor de taux explicite (facilités permanentes) | banque centrale et anticipations | Réserves et refinancement deviennent des flux décidés, pas des soldes résiduels (défaut d'invariance de la v2.0, ADR 0001 § 6). |
| Loi de crédibilité revue ; alternative : apprentissage à gain constant | banque centrale et anticipations | Piège de la loi v2.0 (ADR 0001 § 2). |
| Prix au coût normal majoré | prix | Forme fermée, lisible pour le joueur ; à confronter au terme de demande R3, acquis mesuré de la première tentative. |
| ~~Deux secteurs pour le socle (consommation, équipement)~~ — **écartée (M24, 02/10/2026) : J = 1 retenu**, équations indexées par j dès le socle | production et stocks | Budget de complexité (`docs/exigences.md` § 2.7). Instruite comme option D de la fiche (§ 3.D, § 3.J), contre J = 1 (option C), J = 4 et la liste de la v1.5 : à exigences comptables égales, elle n'ajoute aucune identité vérifiable et paie un prix relatif à stabiliser (instabilités 9 à 11 et 14 ; dérive de 12,8 % de p_K/p_C en v2.0, R) sans levier du socle qui l'exploite ; l'investissement se voit sous J = 1 par les ventes par acheteur. Les secteurs arrivent avec leur mécanisme propre aux jalons J5 à J7 (fiche § 3.J (d)). Libellé initial corrigé le 02/10/2026 (fiche § 1.5, Q1) : la mention « avant les quatre de la v1.5 et de la v2.0 » était inexacte pour la v1.5, qui propose **sept secteurs et un secteur de ressources** (`archive/v1.5/Nations_et_Marches_v1_5.tex` l. 391) ; seule la v2.0 en a quatre (`archive/v2.0/prototype/model.py` l. 68). |
| Encours hypothécaires agrégés par strate plutôt que cohortes individuelles | actifs et crises (J6) | 70 % du temps de la v2.0 dans 23 403 cohortes (mesuré le 29/09/2026). |

### 6. Jalons

Critères de passage arrêtés par le mainteneur le 29/09/2026 (M19).

| Jalon | Contenu | Critère de passage | État |
|---|---|---|---|
| **J0 Fondations** (#2 à #6, PR #7) | Cadre du projet, ADR 0001 à 0004, feuille de route, `archive/`, gabarits et conventions, squelette Python, CI | CI verte (tests, concordance, compilation XeLaTeX) ; plus aucun « À ADAPTER » ; PR #7 fusionnée par commit de fusion. | **Passé le 30/09/2026** : PR #7 fusionnée à 05:29 UTC (commit de fusion `facf97f`), issues #2 à #6 fermées, ruleset « Protection main » appliqué par le mainteneur via l'interface web (écart avec `.github/ruleset-main.json` suivi par #14). |
| **J1 Spécification du socle** | Gabarit de fiche éprouvé sur la première fiche et validé à l'usage (M20), fiche « temps et comptabilité », puis environ huit fiches (production et stocks ; travail et salaires ; prix ; ménages ; investissement et financement ; banque commerciale ; banque centrale et anticipations ; État et dette) → décisions M-n → spécification v3.0 « socle », sections marquées « proposées » jusqu'au code | Les neuf fiches tranchées, chacune avec sa décision M-n reportée ici ; chaque équation porte statut, provenance et M-n (contrôle par la concordance `--strict`) ; matrices des bilans et des flux écrites en tableaux, lignes et colonnes de somme nulle vérifiées par un script d'`outils/` ; état stationnaire calculé sous forme fermée par un script d'`outils/`, sans simulation, avec ses ratios publiés (K/Y, part salariale, taux réel, inflation, dette/PIB ; unité et dénominateur) ; revue de fond de `macro` et `monnaie`, avis de `jeu` sur les leviers prévus, validation du mainteneur. | **Passé le 07/10/2026** : PR #85 (branche n° 4 bis « J1, clôture ») fusionnée par le mainteneur à 10 h 36 UTC (commit de fusion `833afd9`), issues #84, #44, #83, #74 et #75 fermées ; passage validé par le mainteneur le même jour, en connaissance des réserves déclarées : superneutralité non tenue, défaut connu publié selon M32 et codé en échec attendu (#80, ouverte jusqu'au J3) ; limites du test de source reportées à #93 (§ 4). Neuf fiches tranchées et « spécifiées », aucune « implémentée » (`docs/blocs/README.md` § 1). *Historique de l'état* : en cours depuis le 30/09/2026 : **deux fiches tranchées sur neuf**, toutes deux « spécifiées » (fiche 1 « temps et comptabilité », M22, 30/09/2026 ; fiche 2 « production et stocks », M24, 02/10/2026, section `sec:production` proposée et validée le 03/10/2026). Branches fusionnées (§ 7) : J1 n°1 (PR #20, `3518e18`, section `sec:cadre` et script de vérification des matrices) ; technique n° 1 (PR #29, `bf6ad56`) ; n° 3a (PR #35, `3021eaa`, 03/10/2026 : reprises du cadre #25, #23, #36 ; fiche 2, ADR 0007). Branche n° 3b ouverte le 03/10/2026 (fiches 3 à 6, § 1) ; puis n° 3 bis (technique) et n° 4 (fiches 7 à 9). *03/10/2026, en cours de branche n° 3b* : **quatre fiches tranchées sur neuf**, dont deux décidées sans être encore spécifiées (fiche 3, M25 ; fiche 4, M26 ; ADR 0008 accepté le 03/10/2026). *04/10/2026, après la fusion de la PR #43 (`050ffbf`)* : **six fiches tranchées sur neuf** (M22, M24 à M28), **toutes « spécifiées »** (`sec:cadre`, `sec:production`, `sec:travail`, `sec:prix`, `sec:menages`, `sec:investissement` : sections proposées sans label `eq:`, validées par `macro` ; `docs/blocs/README.md` § 1) ; contrats partagés consignés par les ADR 0008 à 0010 (M25 (b), M26, M29, M30). Restent, pour le critère de passage : les fiches 7 à 9 (branche n° 4, après la n° 3 bis en cours, § 1) ; l'état stationnaire sous forme fermée par un script d'`outils/` (non commencé ; #44 s'y ferme) ; la revue de fond de `macro` et `monnaie`, l'avis de `jeu` sur les leviers prévus et la validation du mainteneur. Matrices vérifiées par script : `verifier_matrices.py --strict` sans écart à `050ffbf` (§ 1), bloquant en CI après #28. *04/10/2026, après la fusion de la PR #68 (`9097617`)* : état inchangé, **six fiches tranchées sur neuf, toutes « spécifiées »**. `verifier_matrices.py --strict` est une étape bloquante de la CI (« Matrices strictes ») et la quatrième batterie (#28) ; sa sortie à `9097617` est sans écart (9 / 28 / 28 lignes, 44 / 62 / 31 termes ; mesure d'`architect`, § 1). Restent : les fiches 7 à 9 (branche n° 4, en cours depuis le 04/10/2026, #71 à #73, § 1) ; le script d'état stationnaire sous forme fermée, écrit à la branche n° 4 bis « J1, clôture » (P16 (a), décidée le 04/10/2026 : M19 inchangée ; #44 s'y ferme) ; la revue de fond, l'avis de `jeu` sur les leviers prévus et la validation du mainteneur. *05/10/2026, après la fusion de la PR #77 (`54edad8`)* : **neuf fiches tranchées sur neuf** (M22, M24 à M28, M31 à M33), **toutes « spécifiées »** (`sec:banque`, `sec:banque_centrale` et `sec:finances_publiques` ajoutées, validées par `monnaie` et `macro`) ; contrats partagés consignés par l'ADR 0011 ; batteries vertes et matrices sans écart à `54edad8` (§ 1). Restent : le script d'état stationnaire sous forme fermée, la revue de fond de `macro` et `monnaie`, l'avis de `jeu` sur les leviers prévus et la validation du mainteneur. Ils forment la **branche n° 4 bis « J1, clôture »**, ouverte le 05/10/2026 (PR brouillon #85, § 1 ; P19 à P27 décidés, § 4). *05/10/2026, en cours de branche n° 4 bis (`6631f7d`, rangs 0 à 7 faits)* : **critères de passage tenus sous réserve de la revue finale complète (rang 8) et de la validation du mainteneur (rang 9)** — script d'état stationnaire `outils/etat_stationnaire.py` sans simulation (P21 (a)), ratios de référence publiés dans `tab:etat-stationnaire` avec unité, dénominateur et fenêtre, 289 valeurs comparées sans écart après le visa des 25 écarts ; superneutralité non tenue, défaut connu codé en échec attendu (#80) ; revue de fond de `macro` et `monnaie` : J1 validé avec réserves, levées (`0cd5ae0`, `303e419`, `1d90c22`) ; avis de `jeu` : aucun motif ludique de bloquer J1 ; batteries vertes et matrices sans écart à `6631f7d` (§ 1). Le passage n'est consigné qu'au rang 9. *06/10/2026, rang 8 fait (`ea2c438`)* : revue finale complète faite (règle 10 : `audit`, `macro-approfondi`, `monnaie-approfondi`, `/code-review`), corrections revues et validées avec réserves par `macro` et `monnaie` ; script : 433 valeurs comparées, 426 égales sur l'état résolu, 7 égales en arithmétique (catégorie S), aucun écart ; contre-épreuve 47 / 47 ; historique 29 valeurs, 29 écarts visés ; batteries vertes et matrices sans écart à `ea2c438` (§ 1). **Critères de passage tenus, hors la validation du mainteneur** (rang 9 ; quatre points en attente, § 1). *06/10/2026 (`767e5a1`)* : points (a) à (d) tranchés ; reste la validation du passage. |
| **J2 Noyau** | Comptes, ordonnanceur, état et sauvegarde, observation ; tests d'invariants | Conservation exacte des identités comptables (ε = 1e−12 × échelle du bilan, par pas et en cumul sur 720 pas, M22) ; reprise de sauvegarde identique, y compris à la frontière de tour ; invariance d'unité (×100) ; coût du noyau seul mesuré et publié, seuil écrit avant l'essai : ≤ 0,5 ms par pas mensuel (fiche 1, § 5, réserve 3 ; le budget de calcul sur le socle complet est un critère de J3, M19). Fiche « temps et comptabilité » tranchée le 30/09/2026 (M22, ADR 0005) : le jalon peut démarrer. | **Passé le 15/10/2026** : PR #99 (branche J2 « noyau ») fusionnée par le mainteneur à 05:01 UTC (commit de fusion `2e643a2`, parents `faa3f85`, `0e63473`) ; issues #95, #96, #97, #98 et #93 fermées ; passage validé par le mainteneur à la fusion, consigné après celle-ci au rang 0 de J3-a (écart à P28 (a), P38). Critères tenus (verdict de `macro`, rang 7) : identités ≤ 4,313e−16 × S ; A = 3,714e−15 (marge 269) ; ×100 ; reprise au bit ; C = 0,4267 ms par pas en CI (seuil 0,5 ms ; dispersion de 0,2230 à 0,4267 ms suivie par #105). Concordance 18/18. *Historique* : en cours du 07/10 au 15/10/2026 (branche `claude/j2-noyau`, PR #99). |
| **J3 Économie fermée** | Blocs du socle, état stationnaire résolu, test zéro, premières références de non-régression | Critères d'O1 fixés **avant l'essai** et confirmés par le mainteneur (point de départ : critères du 16/09/2026, `docs/exigences.md` § 1.3) ; test zéro réussi sur les deux fenêtres pour plusieurs graines ; budget ≤ 1 ms par pays-semaine mesuré sur le socle complet, sur la plateforme de référence (M16) ; références régénérées après visa. | **En cours depuis le 15/10/2026** (J3-a fusionnée le 13/11/2026, PR #109, § 7 ; J3-b `claude/j3-economie-reelle` en cours, § 1 ; découpage J3-a à J3-g, § 2, P61). Critères de J3 arrêtés avant l'essai le 15/10/2026 : tableau `tab:criteres-j3` de la spécification (`sec:calibration`), décision D12 sur #107 (§ 4). |
| **J4 Simulateur utilisable** | Scénarios, leviers, rapports en ligne de commande, catalogue des effets des leviers | O2 : pour chaque levier, scénario apparié du signe attendu avec délai et distribution ; O5 : démonstration au mainteneur sur des scénarios de 5 à 10 ans ; avis de `jeu` ; revue d'`app-review`. | À venir |
| **J5 N pays** | Commerce, change, balance des paiements, régimes A à E, barrières entre pays | O4 : tests d'invariance sur les deux fenêtres (5 et 60 ans) — pays seul contre monde à un pays, unité monétaire (×100), permutation des pays, reprise de sauvegarde — à 1e-12 relatif à l'échelle du bilan, aucun solde de bilan calculé comme résidu ; balance des paiements bouclée exactement à chaque pas (somme mondiale des soldes courants et financiers nulle) ; chaque régime A à E expose ses leviers et eux seuls (un test par régime) ; budget ≤ 1 ms par pays-semaine avec au moins quatre pays. | À venir |
| **J6 Actifs et crises** | Blocs actifs et crises financières ; grille des dix configurations en tests | O3 : pour chaque type de crise retenu, précondition, contrefactuel, signal précurseur, intervention, reprise sans effacement gratuit ; **`archive/` supprimée au plus tard à la fin de J6** (M6). | À venir |
| **J7 Web, puis jeu** | Serveur, client web, tours mensuels, plusieurs joueurs, IA des pays non joueurs, conditions de fin | Mêmes résultats, bit à bit, en ligne de commande et par le web à graine et décisions égales (test) ; aucun calcul économique hors du moteur, vérifié par `app-review` ; O5 : partie complète menée par le mainteneur, au moins deux joueurs et une IA, jusqu'à une condition de fin ; reprise d'une partie sauvegardée identique ; revue de jouabilité de `jeu` avant la démonstration. | À venir |
| **J8 Cours** | Dérivations des volumes 1 et 2 corrigées et alignées sur la spécification v3 ; table de correspondance générée par script | Chaque chiffre du cours produit par un test ou un script, jamais recopié (les corrigés faux relevés le 29/09/2026 corrigés) ; chaque équation porte son statut *dérivée / approchée / choix de conception* et renvoie à son label de la spécification ; table de correspondance cours ↔ spécification générée par script et contrôlée en CI ; relecture de fond de `macro` et `monnaie`. | À venir |

### 7. Branches fusionnées

| Branche | PR | Jalon | Fusion | Issues et commits |
|---|---|---|---|---|
| `claude/fondations` | #7 | J0 | 30/09/2026, commit de fusion `facf97f` | #2 (`a5d873c`, `75e2cc6`, `377bda3`) ; #3 (`19839bb`, `85bda79`) ; #5 (`fcb54a6`, `84e6ad9`) ; #6 (`85573bc`) ; #4 (`6090310`, `8ba19ff`, `d8eeb17`, `8c8a633`, `da76229`, `bd0cd44`, `eda7278`, `4651b5f`, `878fc6f`, `75c9e72`). Revue finale complète faite avant la sortie du brouillon ; aucun résultat changé (le moteur v3 n'exécute rien). Issues nées de la revue : #8 à #13 (audit, `docwriter`, session principale) ; #14 après la fusion (ruleset). |
| `claude/routage-modele-effort` | #22 | hors jalon (ad hoc ; M23, ADR 0006) | 02/10/2026, commit de fusion `7a17e01` | Aucune issue : branche ad hoc portant M23, fusionnée dans `claude/j1-temps-comptabilite` par `86ae3cb`. Dix commits, dont `e0df3bb` (routage du modèle et de l'effort, fiches `-approfondi`), `4408522` (politique de routage et ADR, créé sous le numéro 0005 puis renuméroté 0006 par `b81265d`), `3cded24` (contrôle CI des fiches `-approfondi`), `1ad0a98` (section « Escalades, relances et arrêts » du modèle de PR), `b81265d` et `14f86f5` (relecture d'`architect-approfondi`), `a554cf4` (relecture du diff de correction). Aucun résultat changé. |
| `claude/j1-temps-comptabilite` | #20 | J1 (branche n° 1 : fiche « temps et comptabilité », M21) | 02/10/2026, commit de fusion `3518e18` | Point d'étape après J0 et fiche de branche (`02726db`) ; #15 (`1ed2050`, `5a31b4a`, `300b23b`, `4b96a02`) ; #16 (`758273a`, `22a0dd6`, `4773077`, `7ae563a` ; corrections du 02/10/2026 : `19b6f0a`, `bbe4e64`) ; #17 (`f080090`, `85590a5`, `37c6b7a`, `b3d6e46`, `8fa2614` ; annotations de l'ADR 0005 : `ac83f51`, `01b82ea`) ; #18 (`5ab629c` ; corrections de la validation de fond : `1803a57`, `7db3062`, et `c0cfa34`, historique de la fiche, que le corps de la PR #20 range sous #16 mais dont le message cite #18) ; #19 (`42b7e2e`, `567c65c`, `a59118a`, `4e4fdd1`) ; fusion de `main` après la PR #22 (`86ae3cb`) ; feuille de route (`c5ade21`, `2a23fef`). Décisions M20, M21, M22 ; ADR 0005 accepté. Exception au circuit : seconde reprise `coder` → `audit` sur #19, accordée par le mainteneur. Validation de fond de `macro` et `monnaie` (règle 9) et revue finale complète (règle 10) faites ; aucun résultat changé (le moteur v3 n'exécute rien). Issues nées de la branche : #21, #23 à #28. |
| `claude/correctif-journal-agents` | #31 | hors jalon (correctif rapide, `CLAUDE.md`, « Git et GitHub ») | 02/10/2026, commit de fusion `3276b7c` | #30 (`d638021`, `claude:` : `.claude/hooks/journal_agents.sh` et `.claude/outils/bilan_journal.sh` : le hook n'écrit plus de ligne pour un sous-agent interne, sans type ni transcript, et le bilan ignore les lignes vides déjà écrites, relevées au point d'étape du 02/10/2026). Partie de `3518e18`, PR directe vers `main` pendant la branche technique n° 1 ; `main` fusionnée ensuite dans `claude/technique-archive-concordance` par `1a9f1ad`. Aucun résultat changé. |
| `claude/technique-archive-concordance` | #29 | J1, branche technique n° 1 (M21 : outillage de J0) | 02/10/2026, commit de fusion `bf6ad56` (parents `3276b7c`, `8b9af3f`) | Point d'étape après la PR #20 et décisions du mainteneur (`1308807`, `a305bcb`, `cf0be8b`) ; fusion de `main` après la PR #31 (`1a9f1ad`) ; #13 (`d508097`) ; #9 (`29d0703`) ; #8 (`9722960`, `22e6739` commun avec #12, `2f78df3` ; `docs:` `cc85700`, `c90c560`, `8b9af3f`) ; #12 (`ba666e1`, `22e6739` ; `docs:` `731b619`) ; feuille de route (`b4582f8`, `8b9af3f`, commun avec #8). SHA vérifiés par `git log` contre le corps de la PR #29 : quatorze commits hors fusion entre `3276b7c` et `8b9af3f`, tous rattachés. Décisions du mainteneur pendant la réalisation : risque accepté sur #13 (fichier forcé dans Git sous `__pycache__`) ; limites du contrôle statique de #9 acceptées, déclarées dans les docstrings, sans suivi ; délégation technique pour terminer la branche. Questions techniques tranchées par la session sous délégation : `\iffalse` non refermé classé en règle 0, `preparer_tex_et_anomalies` ajoutée (contrat partagé enrichi, `preparer_tex` gardant sa signature) ; décompte de la règle 3 par ligne numérotée de niveau supérieur. Revue finale complète (`audit`, `/code-review`) : conforme avec quatre réserves mineures, corrigées et revues ; sorties de la concordance et de `verifier_matrices.py` sur la spécification identiques octet pour octet à l'état d'avant la branche. Escalades : deux workflows arrêtés sur un constat majeur, suivis d'un second passage (#9, consigne du mainteneur ; #12, relance unique sous délégation) ; aucune consultation Fable. Bilan du journal des sous-agents (commentaire de la PR #29, 02/10/2026, `docs/agents/routage.md` § 7) : `architect-approfondi` 1 (2 reprises), `audit` 21, `coder` 7, `docwriter` 1, `general-purpose` 1 (`/code-review`), tous servis par `claude-opus-5-5`, aucun remplacement de modèle. Aucun résultat changé. Issues proposées, non créées à la fusion : deux, créées le 02/10/2026 sous les numéros #32 et #33 (§ 4). |
| `claude/j1-cadre-production` | #35 | J1 (branche n° 3a : reprises du cadre et fiche « production et stocks », D2) | 03/10/2026, commit de fusion `3021eaa` (parents `bf6ad56`, `0a59fe0`) | Point d'étape après la PR #29 et plan de la branche (`1552cbb`) ; #25 (`0771496`) ; #23 (`8c810e1` `code:`, `9f9d0d4` `tests:`, `3d66354`, `be1e2cc`) ; #36, ajoutée au périmètre le 02/10/2026 (`3127e80`) ; #34 : jalon 1 `7a4e99c`, jalon 2 `8e9fe38`, `566cd94`, remesure S1 (`757d2af`, `beb7496`, `dfe896f`, critères `227607e`, verdicts `6a15fb5`), jalon 3 `a23e014` (M24), ADR 0007 `c76fc76`, pilotage `d89dc43`, `ecda63e`, jalon 4 `626461d`, réserves de `macro` levées `7fb8d62`, `a6d1a00`, `21b95eb`, constats m1 et m2 de la revue finale `975bde7`, `d5aa24a`, `48f60ec`, statut « spécifiée » et feuille de route `0a59fe0`. SHA vérifiés par `git log --oneline bf6ad56..0a59fe0` : vingt-sept commits, tous rattachés. Décisions : M24 (§ 4), ADR 0007 accepté, visa de l'amendement de notation de la fiche 2 (π̄ en glissement annuel). Revue finale complète (`audit` conforme avec réserves mineures m1 et m2, levées ; `/code-review` sans constat). Escalades : une consultation Fable sur trois (`architect-approfondi`, § 4.1, point 3 : ADR 0007) ; reprises de `docwriter` (#25, #23, jalon 4, plus une relance ciblée) et de `coder` (S1, après un constat majeur) ; arrêt de la session du 02/10/2026 sur instruction du mainteneur. Écarts notés dans la PR : constat m3 (`dfe896f`, préfixé `code:`, touche `tests/`), `975bde7` sans la reprise annoncée de la docstring (faite en `48f60ec`). Aucun résultat changé (le moteur v3 n'exécute rien ; sorties de `verifier_matrices.py --strict` identiques à celles de `bf6ad56`). Issues nées de la branche : #36, #37, #38. |
| `claude/j1-economie-reelle` | #43 | J1 (branche n° 3b : fiches 3 « travail et salaires », 4 « prix », 5 « ménages », 6 « investissement et financement », D2) | 04/10/2026, 10 h 12 UTC, commit de fusion `050ffbf` (parents `3021eaa`, `6157e3f`) | Issues fermées : #38, #39, #40, #41, #42 (vérifié par la session) ; rattachées sans `Closes`, toujours ouvertes : #24 (volet « banque centrale », n° 4), #37 (J4, J7), #44 (n° 4, J3), #58 (fermeture proposée, P5). Point d'étape et plan (`d62e67a`, `bf3829e`) ; #38 (`3a4b04d`, `bb8d194`) ; #39 : jalon 1 `a1b838e`, `17f5137`, `4aee609`, jalon 2 `e7873e6` à `981046b` et `7bc8eb3`, jalon 3 (M25) `de91847`, `eec62da`, `9b50d58`, `53bc45d`, jalon 4 `9bcd6b9`, reprises `c72a95f`, `19a22e4`, `5415b5a`, `f092bcd` ; #40 : jalon 1 `60a35fd`, `4aee609`, jalon 2 `ff3f97d`, `25be833`, `7bc8eb3`, jalon 3 (M26) `de91847`, `eec62da`, ADR 0008 `ffe4520`, `ac236a7`, jalon 4 `17c064e`, reprise `25002ad` ; #41 : jalon 1 `1afe85c`, `b5a008b`, jalon 2 `d88a47e` à `d9d388b`, jalon 3 (M27) `b8978f2`, `8150824`, `efb6bcd`, ADR 0009 (M29) `c5562fa`, ADR 0010 (M30) `43fe109`, jalon 4 `b9b8260`, reprises `131118c`, `8eec3a0`, `5d2c831` ; #42 : jalon 1 `1afe85c`, `b5a008b`, jalon 2 `d80bfe7` à `f5dcfe6`, jalon 3 (M28) `b8978f2`, `a3ced74`, `efb6bcd`, jalon 4 `e976bb1`, reprises `b1d3c9f`, `6337c89`, `6994cbb`, `d341b9f`, `6157e3f` ; annotations des fiches, des ADR, de `CONTEXT.md` et feuille de route (`2af377e`, `b6ad4da`, `f525839`, `9dcfbaf`, `f0ab28c`, `f7d56c1`, `dafbfb9`, `a13e441`, `b67913b`, `f118a58`, `320c394`, `04b1184`). `git log --no-merges 3021eaa..6157e3f` : 78 commits, tous `docs:` (rattachement d'après le corps de la PR #43). Décisions : M25 à M30 (§ 4) ; ADR 0008, 0009 et 0010 acceptés ; visas des chiffres de la fiche 2 sous (G) (03/10/2026) et du niveau normal du capital au prix courant (04/10/2026) ; critères J3 « Délais » des fiches 5 et 6 corrigés de façon prospective (aucun essai fait). Validation de la spécification par `macro` (quatre rapports, avec reprises) ; revue finale complète (`macro-approfondi`, `/code-review` ; `audit` non déclenché, ni code ni test). Escalades : une consultation Fable sur trois (ADR 0009 relu et amendé, ADR 0010 rédigé) ; relances ciblées (instruction de la fiche 5 ; `monnaie` sur S-ζ, désaccord levé sans Fable) ; deux arrêts sur instruction du mainteneur (passations du 03/10/2026). Aucun résultat du moteur changé (ni `src/` ni `tests/` touchés) ; `verifier_matrices.py --strict` inchangé (9 / 28 / 28 lignes, 44 / 62 / 31 termes). Suivis non bloquants : P10 et P11 (§ 4). Issues nées de la branche : #44 à #67. |
| `claude/technique-matrices-ci` | #68 | J1, branche n° 3 bis (technique n° 2 : `verifier_matrices`, concordance, invariant d'archive et CI) | 04/10/2026, 12 h 20 UTC, commit de fusion `9097617` (parents `050ffbf`, `906edb5`), par le mainteneur | Issues fermées par `Closes` : #21, #27, #32, #33, #28 (absentes du relevé des 30 issues ouvertes, § 3). Point d'étape et plan (`c855226`), décisions P4 à P12 (`74c6e35`) ; #21 (`46c2532` `code:`, `351c89e` `tests:`, `docs:` `799a85d`) ; #27 (`dadcc26`, `b118601`, `docs:` `0c9dfe4`) ; #32 (`99256f6`, `656e244`, `docs:` `38d6f4d`, `b56fc59` ; branche `\else` sans `\fi` : `4a1cd6f`, `da76aad`, `docs:` `88f6506`) ; #33 (`fd2df56`, aucune surface documentaire) ; #28 (`d1dfcb5` `repo:`, `8975e14` et `378b9fd` `tests:` dont le test d'identité des listes de batteries de P9, `1636466` `claude:`, `docs:` `61f401c`, ADR 0003 annotée `3442155`) ; docstrings `9493870` (#21, #32) ; feuille de route `3442155`, `4461e87`, `906edb5`. `git log --no-merges 050ffbf..906edb5` : 25 commits, tous rattachés. Questions techniques tranchées par la session sous délégation (P8) : `[…]` optionnel des filets booktabs ; erreur de fichier sur stderr, code 1 ; refus du signe après un produit limité à `\cdot` et `\times` ; reconnaissance par nom d'attribut dans l'invariant d'archive ; limites déclarées plutôt qu'élargissement pour #32. Workflows `circuit-technique` : #21, #27, #33 « terminé avec questions » ; #32 arrêté sur un constat majeur, corrigé par la reprise ; #28 arrêté (refus de `coder` d'écrire dans `CLAUDE.md` et `.claude/`), modifications faites par la session. Revue finale complète (règle 10) : `audit` conforme avec réserves (C1 et C2 corrigés ; C3, skill `compiler-doc`, en issue proposée) ; `/code-review` : un défaut mineur, corrigé et audité (coût quadratique mesuré). Escalades : aucune consultation Fable, aucune relance ciblée. Bilan du journal dans le commentaire de passation de la PR (04/10/2026) : tous les agents servis par `claude-opus-5-5`. Aucun résultat changé : sorties `--strict` des deux scripts sur la spécification identiques octet pour octet à `050ffbf` (corps de la PR) ; `src/`, `archive/`, `tests/references/` et `nations_et_marches.tex` intacts (`git diff --stat 050ffbf 9097617` vide sur ces chemins, mesure d'`architect`). Issues proposées, non créées : six, rattachées en P15 (§ 4). |
| `claude/j1-monnaie-etat` | #77 | J1 (branche n° 4 : fiches 7 « banque commerciale », 8 « banque centrale et anticipations », 9 « État et dette » ; P13, P14) | 05/10/2026, 16 h 08 UTC, commit de fusion `54edad8` (parents `9097617`, `0cfdc44`), par le mainteneur | Issues fermées par `Closes` : #71, #72, #73, #26, #69 (absentes du relevé des 34 issues ouvertes, § 3). Rattachées sans `Closes` : #24 et #49, fermées par la session pendant la branche (critères de #72) ; #76, fermée par la session le 05/10/2026 (commentaire citant `14c8050` et `54edad8`) ; #44 (n° 4 bis), #54, #56, #57, #61, #64 (instruites, toujours ouvertes). Commits, rattachement d'après les messages et le corps de la PR #77 : #76 `14c8050` (`claude:`) ; point d'étape et plan `10391a1` ; critères des trois fiches, validation et #78 `5f2f2d6`, `c98fa35` ; **#71** : jalon 1 `3b06f8f`, `c23b302`, `942f9f0`, jalon 2 `0e3fb17`, `a246acb`, jalon 3 (M31) `9dca301`, `481c279`, #79 `320bfbb`, jalon 4 `12e1c4d`, corrections `9d746b8`, `2b24827`, `e141586`, annotations `8d52fe5` (avec #55), spécifiée `4c95991` ; **#72** : jalon 1 `6777662`, `5759b27`, `d5e9f7d`, jalon 2 `f07d02f`, `5a14a79`, `33e056e`, `3edff4e`, jalon 3 (M32) `29dea85`, `15cc933`, jalon 4 `e0155c4`, errata `23fbf7a`, `a78205e`, `8c17309`, corrections `81bd85f` ; **#73** : jalon 1 `53b4124`, `5066400`, `168346c`, jalon 2 `18d2868`, `4ce56b2`, `2d1a070`, `5de8f2a`, `0f36843`, jalon 3 (M33) `29dea85`, `3aea20c`, jalon 4 `4e158fb` (avec la lecture (f) de `sec:banque`), erratum `32eb3cc`, corrections `e4ba6c0`, routage § 4.2 `776083c` ; **#72 et #73 ensemble** : issues #80 à #82 `9cc1ead`, ADR 0011 proposé (Fable) `50cc78b`, décisions sur les § 9 `d66e21c`, ADR 0011 accepté et annotations des ADR 0005, 0009, 0010 `a8c4209`, symboles et P1 à P6 `b4d78e9`, `14fe795`, précisions datées des fiches 7 et 9 `a8fc35f`, validations et #83 `dc26cae`, assiette nette `70b5771`, revue finale `ca10fc8`, `2d017b4`, fiches 8 et 9 spécifiées `59f7aa4` ; **#69** `2aaf060`, ADR 0010 annoté `ecd2689` ; **#26** `b9aaf19` ; feuille de route de fin de branche `0cfdc44`. `git log --no-merges 9097617..0cfdc44` : 61 commits, tous rattachés, tous `docs:` sauf `14c8050`. Décisions : M31 (fiche 7, option C), M32 (fiche 8, option C ; critère 13 en défaut connu, #80), M33 (fiche 9, option C-HS) ; précisions du 04/10/2026, sans numéro M (§ 4) : critères des trois fiches validés, ADR 0011 accepté (lecture (i) de 19b, P1 à P6), borne de ν_G 1,0959, notation (a_I, θ_CB, ν_G, PB_t, θ_G, θ_Tr), bande du test zéro sur r̄(1 + π\*), QM2 (a), QM5, QM6, source de π\*, critère J1 de la dette brute, libellé « dominance budgétaire », assiette nette de la couverture des intérêts. Validations des sections par `monnaie` et `macro` ; revue finale complète (règle 10 : `monnaie-approfondi`, `macro-approfondi`, `jeu`, corrections contrôlées sur leur diff ; `/code-review` sans constat ; `audit` non déclenché, ni code ni test). Escalades : une consultation Fable sur trois (`architect-approfondi`, ADR 0011, § 4.1, point 3) ; relances ciblées (jalon 1, les deux experts ; `macro`, C57 et C58 ; relance de forme de `macro`) ; deux arrêts à la limite de tours (`monnaie-approfondi`, `monnaie`), comptes rendus livrés sur relance ; un redémarrage du conteneur pendant un passage de `docwriter`. Bilan du journal des sous-agents : non collé dans la PR (P27). Aucun résultat du moteur changé : `git diff --stat 9097617 54edad8 -- src tests outils archive` vide (mesure d'`architect`) ; `verifier_matrices.py --strict` inchangé (9 / 28 / 28 lignes, 44 / 62 / 31 termes). Suites non tranchées, rangées au § 4 (P22 à P26) : maquettes perdues et critère 11 de la fiche 8, q1 de `macro`, chiffre de −0,43 % caduc, intervalle de a_π. Issues nées de la branche : #78 à #83. |
| `claude/j1-cloture` | #85 | J1 (branche n° 4 bis : clôture, script d'état stationnaire sous forme fermée, technique n° 3 ; P19 à P27) | 07/10/2026, 10 h 36 UTC, commit de fusion `833afd9` (parents `47e0eb2`, `a8f3061`), par le mainteneur | Issues fermées par `Closes` : #84, #44, #83, #74, #75 (état CLOSED vérifié par `gh api`, 07/10/2026). Rattachée sans `Closes`, toujours ouverte : #80 (J3). Commits, rattachement d'après les messages et le corps de la PR #85 : point d'étape et plan `253af3e`, décisions P19 à P27 `764c7f0` ; fusion de `main` après la PR #86 (P27, correctif rapide `d7bc95f`, fusion `47e0eb2`) `3d6e6a8` ; **#74** `cede975` (`code:`), `2950f51` (`tests:`), `21b8443` (`code:`), `docs:` `05b9755` ; **#75** `d1370c0` (`tests:`) ; **#84** `code:` `6edfabc`, `bfccdff`, `0cd5ae0`, `303e419`, `b7339e7`, `28a37d9`, `tests:` `bd6232a` (avec #80), `759ff79`, `9c8bdbd`, `742f9fb`, `ef6d477`, `5eaed92`, `86b543f`, `docs:` `8b9fa94`, `a1a7bf0`, `7cbaede` (avec #80), `1d90c22`, `c9d6d6e` (avec #80), `a225e45`, `181d2fa`, `ea2c438`, `767e5a1` ; **#44** `54473a6`, `5c2f940` ; **#83** `e2b2227` ; **#88** (sans `Closes`, J3) `6631f7d`, `bfb01f8`, `76616c2`, et `a09f958` (avec #84, `docs:` préparatoire) ; feuille de route `281b9ac`, `1d2003c`, `796541f`, `a8f3061`. `git log --no-merges 47e0eb2..a8f3061` : 40 commits (8 `code:`, 9 `tests:`, 23 `docs:`), tous rattachés et vérifiés un à un (`git cat-file -e`, ancêtres de `a8f3061` et non de `54edad8`). Décisions (§ 4) : P19 à P27 (05/10/2026) ; critères du script validés avant l'essai ; visa du tableau avant / après (25 écarts, puis quatre valeurs de la fiche 9 ; historique de 29) ; ν_G = 1,15 ; décisions après la revue finale (05/10/2026) ; décisions de session et points (a) à (d) du rang 9 (06/10/2026) ; passage de J1 validé (07/10/2026). Revue de fond du jalon (`macro-approfondi`, `monnaie-approfondi`) : J1 validé avec réserves, levées ; avis de `jeu-approfondi` : aucun motif ludique de bloquer J1 ; revue finale complète (règle 10 : `audit`, `macro-approfondi`, `monnaie-approfondi`, `/code-review`), corrections revues sur leur diff ; mi-C reporté à #93. Escalades (corps de la PR) : aucune consultation Fable (0 sur 3) ; une reprise `coder` → `audit` au rang 3 (constat majeur) et une au rang 8 (mi-A) ; relances ciblées de `macro` (rangs 3-4, 7) et de `macro-approfondi` (rang 8, limite de tours). Résultats : moteur inchangé (`git diff --stat 54edad8 833afd9 -- src archive tests/references` vide, mesure d'`architect`) ; chiffres publiés de la spécification remesurés par le script, écarts visés par le mainteneur ; sorties `--strict` des deux scripts identiques octet pour octet avant et après #74 et #75 (corps de la PR). État à `833afd9` (mesure d'`architect`, 07/10/2026, sur `claude/j1-passage`, code identique) : unitaires 357 passed, 1 skipped, 2 xfailed ; invariants 89 passed, 1 skipped ; concordance et matrices `--strict` « Aucun écart. » (9 / 28 / 28 lignes, 44 / 62 / 31 termes) ; `outils/etat_stationnaire.py`, code 0 : « 433 valeurs comparées, 426 égales sur l'état résolu, 7 égales en arithmétique de la spécification (catégorie S, sans état résolu), aucun écart », contre-épreuve 47 / 47, historique 29 valeurs, 29 écarts visés. Issues nées de la branche : #87 à #93. |
| `claude/j1-passage` | #94 | J1 (consignation du passage ; branche dédiée, non branche de travail, P28 (a)) | 07/10/2026, 11 h 15 UTC (date du commit de fusion), commit de fusion `faa3f85` (parents `833afd9`, `6dc9174`) | Aucune issue fermée. Un commit, `6dc9174` (`docs:` : `docs/feuille-de-route.md` +19/−12 et `docs/blocs/README.md` +1, `git show --stat`) : PR #85 consignée au § 7, passage de J1 validé par le mainteneur le 07/10/2026 consigné aux § 4 et § 6. Exception ponctuelle sans valeur de précédent (P28 (a)) : à partir de J2, le passage d'un jalon est validé avant la fusion et consigné dans la branche de travail. Aucun résultat changé ; aucune consultation Fable. |
| `claude/j2-noyau` | #99 | J2 | 15/10/2026, 05:01 UTC, commit de fusion `2e643a2` (parents `faa3f85`, `0e63473`), par le mainteneur | Issues fermées par `Closes` : #95, #96, #97, #98, #93. 54 commits (API). Ouverture `c43883a`, `f021b13` ; ADR 0012 `294ba78`, accepté `44b5c50` ; fiche 1 § 9.9 `8a2dfd3`. **#95** `1a3f852`, `a914561`, `f36fcbb`, balises `84130b4`, `docs:` `7f7e5ec`. **#96** `1bfe179`, `0f3d2f6`, `1f8917a`, `0564220`, `b9c3fe8`, `39a2c23`, `629de02`, `cbe4562`, `docs:` `2a82245`. **#97** `657591c`, `b2800c7`, `201b4ba`, `e939170`, balises `6a9e836`, `docs:` `5fa98d5`, xfail levé `f3a0136`, `fb5546d`. **#98** `91b1f2e`, `284675b`, `7419cab`, `899adfe`, `docs:` `0a29b63`. **#93** `9750df4`, `8e1f118`, `34c227d`, `b516337`, `156564b`, `466d0f9`. Rang 7 `55dda6d`, `0025c91`, `24d8a8e`. Rang 8 `3b364bd`, `3c6b280`, `3e8b383`, `0e63473`. Annotations de l'ADR 0012 et feuille de route : `6fd90fa`, `a3883c1`, `07f0ecf`, `7abc82c`, `7d52fbf`, `e8d4dc2`, `224b1a5`, `da7603e`, `8511ba3`. Escalades : Fable 2 sur 3 (ADR 0012 ; point 8) ; deux arrêts à 40 tours (`architect`, `monnaie`), chacun suivi d'une relance ciblée ; `circuit-technique 93` arrêté par un faux positif. Bilan du journal non collé (écart à P36). Premier code exécuté ; aucun résultat publié changé. Deux nombres nouveaux publiés : C et A. Issues nées de la branche : #100 à #106. |
| `claude/j3-maquette-criteres` | #109 | J3 (J3-a) | 13/11/2026, 17:34 UTC, commit de fusion `204ab2d` (parents `2e643a2`, `5fe2667`), par le mainteneur | Issues fermées par `Closes` : #107, #105, #65, #66, #100. 37 commits hors fusion (11 `code:`, 10 `tests:`, 16 `docs:`). Détail des rangs : corps de la PR #109 et version de la feuille de route à `5fe2667`. Décisions : P38 à P48, D1 à D13, G1, F2, S1, S2 (§ 4). Fable : 0 sur 3. Moteur : `src/` modifié pour #100 seulement (`ordonnanceur.py`, `diagnostics.py`), résultats inchangés. État à `204ab2d` : unitaires 1178 passed, 1 skipped, 2 xfailed ; invariants 198 passed, 2 skipped ; concordance 18 / 18 ; matrices sans écart. Issues nées de la branche : #110, #111. |

### 8. Escalades, relances et arrêts hors branche

Consultations faites hors de toute branche ouverte (`docs/agents/routage.md`, § 7) ; une consultation Fable compte pour la branche suivante (`docs/agents/routage.md`, § 5.2).

| Date | Fiche / modèle / critère déclenché / statut obtenu / suite |
|---|---|
| 15/10/2026 | Point d'étape après la PR #99 (passage de J2, plan de J3) / `architect-approfondi` / Opus, effort `high` / passage de jalon / `complet`, décisions P38 à P48 du mainteneur (§ 4). Écarts notés : E1 (passage de J2 validé à la fusion, non consigné avant, P28 (a)) ; E2 (aucun bilan du journal collé dans la PR #99, P36 ; `bilan_journal.sh` : « Journal vide ou absent » en session cloud, calibration partielle). |
| 15/10/2026 | Même point d'étape / seuil « macro » atteint par le découpage de J3 (`docs/agents/routage.md` § 4.3, critère 2) / consultation Fable proposée / **reportée par le mainteneur au plan de J3-b**, où elle comptera (budget Fable de J3-a : 0 sur 3). Les deux arrêts à 40 tours de J2 tiennent à la taille des documents lus, non à l'effort : réponse par P48 et par des briefs à périmètre de lecture fermé, sans relever `maxTurns` ; aucun commit `claude:`. |
| 13/11/2026 | Point d'étape après la PR #109 (plan de J3-b, réexamen du découpage de J3) / `architect-approfondi` / Fable, accord du mainteneur du 13/11/2026 (seuil § 4.3, critère 2, report du 15/10/2026) / P49 à P64 décidés le 13/11/2026 (P54, P56, P57, P63 sous réserve de l'avis de `macro`) / compte pour J3-b : 1 sur 3. |
