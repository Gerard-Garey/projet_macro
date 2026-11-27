---
status: proposed
date: 2026-11-27
---

# Échelle d'une ligne du noyau à repli structurel, jamais nulle ; familles de refus classées par moment, avec deux traductions arithmétiques en liste fermée ; domaines de représentabilité distincts des domaines économiques

> **Statut « accepté » le 27/11/2026, par décision du mainteneur** (V1 à V4 acceptés selon l'ADR ; V5 : finitude, borne ln(DBL_MAX) maintenue ; P298 jugée non déclenchée, sans Fable ; numéros P attribués à la consignation). Texte d'origine du statut : « proposé », à accepter par le mainteneur. Rédigé par `architect-approfondi` (Opus, effort `high` ; P298 : sans Fable, l'ADR n'ayant pas à modifier l'ADR 0005 ni l'ADR 0014, voir Conséquences) au rang 1 de J3-e2 (`claude/j3-e2-refus-types`, PR #193, tête `bda0368`). Les points 1 à 7, 10.1, 11, 13 (deuxième tiret), 18 et 19 consignent des décisions **arrêtées** par le mainteneur le 27/11/2026 sur les avis de `monnaie` (#153) et de `macro` (#158, #125 point 6, #178) du rang 1 ; leur numéro P est attribué à la consignation. Les autres points en sont la mise en forme, **proposée**. Les points à accepter ou à trancher sont repris sous « Points soumis au mainteneur » (V1 à V6).

## Contexte

Quatre constats, tous établis à la tête `bda0368`, dont le code de `src/` est celui de `ce3662a`, appellent une même décision : quel est le dénominateur d'une identité du noyau quand l'échelle naïve s'annule, et sous quelle forme un état que le moteur ne peut pas traiter s'arrête-t-il ?

**1. Échelle nulle d'une ligne (#153).** Mesures de `monnaie` (scripts `scratchpad/m153/repro.py`, `grille.py`, `instrument.py`, `empreintes_avec_repli.py`, `cumulee.py` de la session du rang 1). Le banc est le socle complet (`derouler`), avec ς_B = 1 aux pas 5 à 7 et θ_Tr composé à tous les pas.
- À π\* = 10 % et θ_Tr = 0,3, le moteur s'arrête : `DefautComptable` au pas 7, phase 6, `eq:noyau-variation-monnaie-centrale`, ligne 20, résidu −1,13e−17, S = 0,0, résidu/S = inf. La grille θ_Tr ∈ [0,1 ; 0,4] × π\* ∈ {0 ; 2 ; 10 %} donne huit arrêts du même type. Leur apparition n'est pas monotone en θ_Tr : c'est la signature d'un arrondi.
- **Mécanisme.** La ligne 20 (Δ Réserves) est une contrepartie de règlement. Son montant de phase, m = Σ des mouvements routés de `Res`, vaut exactement 0,0, car les mouvements se compensent. La variation des positions, cumulée séquentiellement sur la position de début, vaut 1,13e−17 : l'addition flottante n'est pas associative. Toutes les cellules de la ligne étant nulles, `_echelle_de_ligne` (`src/nations/noyau/grand_livre.py:85-92`) rend 0, et |r| ≤ ε × 0 exige r = 0 exactement.
- **L'état économique est légitime.** Des placements ratés vident le compte du Trésor ; au socle, θ_CB = 0 et la banque est en refinancement, si bien que le bilan de la banque centrale se réduit à L^CB = M^G. S^CB tombe de 1,34 au pas 4 à 3,1e−5 au pas 7.
- **Hypothèse démentie.** L'ADR 0012 admet une échelle nulle (A5 : « une échelle nulle ne divisant pas »), et la docstring de `rapport_a_l_echelle` (`src/nations/noyau/diagnostics.py:22-28`), comme la spécification (l. 637 : « nulle si aucun, le résidu devant alors être nul »), affirment que le résidu y est « nul par construction ». C'est vrai pour une ligne proposée, faux pour une contrepartie, dont la porte compare deux calculs flottants d'une même variation. Seules les lignes 17 et 20 y sont exposées ; la 22 a une signature (0, 0).

**2. Familles de refus dispersées** (relevé `grep -rn "^class "` dans `src/nations`, vérifié). Les refus vivent dans quatre familles sans règle commune :
- `ArretNoyau` (`RefusDeProposition`, `DefautComptable`), `noyau/diagnostics.py`, et `ArretMoteur` (`DefautDeDeclaration`, `RefusDuMoteur` et ses dérivées `PlanHorsDomaine`, `EntreeHorsDomaine`, `DepassementNumerique`), `moteur/diagnostics.py` : deux racines distinctes, toutes deux dérivées d'`Exception` ;
- `ValueError` et `TypeError` levées par la construction d'`EtatPays` (D1) ; `SauvegardeRefusee(Exception)` à la reprise (D4) ;
- `NormalisationHorsDomaine(ValueError)` et `EchelleNonRepresentable(ValueError)` (`scenarios/initial.py:105`, `:109`), `EtatStationnaireInexistant(Exception)` (`scenarios/stationnaire.py:294`), hors d'`ArretMoteur` par décision (ADR 0015, pt 8.2, S10), l'harmonisation étant renvoyée à J3-e2 (ADR 0015, pt 8.4). P297 en confie la forme au présent ADR et la mise en œuvre à #194, au J4.

**3. Exceptions arithmétiques brutes (#158).** T2 (`travail.py:73`) calcule exp(−μ̃_{t−1}) et T3 (l. 89-91) divise ω\* par ω_{t−1}. À μ̃ = 746, T3 lève `ZeroDivisionError` ; à μ̃ = −710, T2 lève `OverflowError` (tableau de #158). `_appeler` (`ordonnanceur.py:921-928`) ne traduit que `OverflowError`, en `DepassementNumerique` (P139). Mesures de la représentation, vérifiées ici :

```
uv run python -c "import math,sys; m=math.log(sys.float_info.max); print(repr(m), math.exp(m), math.exp(-m), 1/math.exp(-m), sys.float_info.min)"
709.782712893384 1.7976931348622732e+308 5.562684646268137e-309 1.7976931348622728e+308 2.2250738585072014e-308
```

Au-delà de ln(DBL_MAX), `math.exp` lève `OverflowError` (« math range error », vérifié sur `nextafter`).

**4. Bornes inférieures des paramètres de production (#125, point 6).** Le domaine de la table (σ > 0 ; κ > 0 et 1/κ fini ; ADR 0014, H3.2) admet des valeurs sous-normales, κ = 5,6e−309 et σ = 1e−320 (critère du plan, P294). **#178** : d < 0 n'est atteignable par aucune voie du moteur (avis de `monnaie`, par appel direct de `plan_de_depense` et de `ventes`).

**Concordance** (vérifiée) : `uv run python outils/concordance_spec_moteur.py --strict` donne 91 labels, 91 balises, aucun écart ; 12 labels `eq:noyau-*` dans `nations_et_marches.tex`.

## Décision

### I. Échelle d'une ligne (#153) — arrêtée par le mainteneur le 27/11/2026 (option (a) de `monnaie`)

1. **Définition.** L'échelle d'une ligne ℓ exécutée dans une phase est :
   - **S_ℓ = min { S_s : le secteur s a un montant non nul sur ℓ }** si cet ensemble n'est pas vide : c'est la lecture (α), inchangée (ADR 0012, point 9 ; ADR 0014, A5) ;
   - sinon, **S_ℓ = min { S_s : la ligne ℓ porte une colonne du secteur s au catalogue }** (`tab:matrice-flux` ; les deux sous-colonnes des entreprises comptent pour un secteur). C'est l'**échelle de repli**, structurelle.

   S_s est l'échelle du bilan du secteur à l'ouverture du pas (`eq:noyau-echelle-bilan` ; ADR 0014, A3.1). Repli des contreparties : ligne 17, min(S^H, S^F, S^Bk) ; ligne 20, min(S^Bk, S^CB), soit l'échelle même de `eq:noyau-cloture-poste` pour `Res` ; ligne 22, min(S^G, S^CB) (relevé du catalogue, vérifié).
2. **Propriétés.**
   - S_ℓ n'est **jamais nulle**, puisque S_s > 0 est un domaine contrôlé à l'ouverture (ADR 0012, point 11 ; `grand_livre.py:214-224`).
   - Elle n'est **jamais absolue** : ni constante, ni `max(1, ·)`, ni flux.
   - La forme du contrôle reste |r| ≤ ε × S_ℓ, et ε n'est pas élargi.
   - Ce n'est pas le « repli » qu'exclut l'ADR 0012, point 11 (tolérance absolue ou `max(·)` à la place d'une échelle de secteur nulle) : S_s ≤ 0, infinie ou non définie reste un défaut à l'ouverture (`grand_livre.py:217-224`, commentaire « jamais un repli », qui vise S_s). L'échelle de repli d'une ligne est une échelle de bilan du même pas, choisie par la structure du catalogue.
3. **Portée.** S_ℓ est le dénominateur commun de trois identités : `eq:noyau-somme-ligne` et les deux portes ligne par ligne (`eq:noyau-variation-monnaie`, `eq:noyau-variation-monnaie-centrale`), contreparties comprises. Les autres échelles ne changent pas : `eq:noyau-cloture-poste` (plus petit des deux bilans qui tiennent le poste), sommes de colonnes, caisse nette, contrôles par pas et identité cumulée de la phase 9.
4. **Innocuité.** Sur toute trajectoire qui ne s'arrêtait pas, S_ℓ = 0 impliquait r = 0, et le rapport publié valait 0. Avec le repli, il vaut encore 0, car `verifier_identites` rend `0.0 if residu == 0.0` (`identites.py:251`, vérifié). Aucune sortie ne change. Mesure de `monnaie` : empreintes des bancs identiques à `ce3662a` (globale `b8cbd18d…d7d3`), avec un repli déclenché 293 757 fois ; c'est un critère du rang 2, à remesurer.
5. **Label.** La règle est active, non triviale et partagée par trois identités : elle reçoit le label **`eq:noyau-echelle-ligne`**, balisé une fois dans `nations.noyau.grand_livre._echelle_de_ligne`. La concordance passe à **92 / 92**, et le noyau à **treize** labels `eq:noyau-*` au lieu des douze d'A5 (ADR 0014 annoté).
6. **Lectures de la spécification**, écrites selon le code :
   - **(L1)** « secteurs touchés » (l. 698) se lit « secteurs qui ont un montant non nul » (l. 637, 4407), puis le repli ;
   - **(L2)** le montant d'une contrepartie est la **somme des mouvements de règlement routés** sur la phase ; sa porte le **compare à la variation des positions** des moyens de paiement. Ce n'est pas « la variation de ses postes » (l. 551), lecture qui rendrait la porte tautologique.
7. **Hypothèse corrigée.** « Échelle nulle, résidu nul par construction » ne vaut plus nulle part. La docstring de `rapport_a_l_echelle` et la l. 637 de la spécification sont corrigées. Après le repli, aucune échelle nulle n'atteint le noyau quand les S_s de l'ouverture sont > 0 : la branche `ZeroDivisionError` de `rapport_a_l_echelle` devient inatteignable depuis le noyau. Son sort (garde documentée ou retrait) revient à `coder` et à `audit` au rang 2 ; il est sans effet sur les résultats.

### II. Familles de refus — forme proposée (P297)

8. **Principe : une famille par moment du refus**, et non par couche. C'est la distinction dont l'appelant a besoin (script, simulateur J4, interface J7) : refus avant tout pas, refus d'un état ou d'un scénario, arrêt pendant un pas.

   | Famille | Classes | Moment | Champs portés |
   |---|---|---|---|
   | Arrêt du noyau | `ArretNoyau` : `RefusDeProposition`, `DefautComptable` | pendant un pas : à l'appel, à la clôture | t, phase, règle (label `eq:` ou nom), secteur ou payeur, ligne, terme ; pour une identité, résidu, S, rapport, tolérance (ADR 0014, A6) |
   | Refus du moteur | `RefusDuMoteur` et ses dérivées : `PlanHorsDomaine`, `EntreeHorsDomaine`, `DepassementNumerique`, refus de division (pt 10) | pendant un pas, à l'appel | t, étape, bloc, nom (variable, ligne, poste, entrée) ; `None` si sans objet ; cause chaînée pour une traduction |
   | Refus de déclaration | `DefautDeDeclaration` | avant le premier pas : table, assemblage | nom (paramètre, siège) ; t, étape sans objet |
   | Refus de chargement d'un état | `ValueError` et `TypeError` d'`EtatPays` (D1) ; `SauvegardeRefusee` (D4) | construction (état initial, `replace`) ; reprise | champ et motif dans le message ; pays et champ pour la reprise |
   | Refus du scénario | `RefusDuScenario` : `EtatStationnaireInexistant`, `NormalisationHorsDomaine`, `EchelleNonRepresentable` (pt 14) | résolution de l'état initial, avant le premier pas | champs propres (conditions ; normalisation, grandeur, valeur) ; cause chaînée pour une traduction |

9. **Arrêts du pas : inchangés.** ADR 0014, A6 et B, sans modification. Aucun arrêt n'est rattrapé pour continuer, et l'état d'ouverture reste intact. Une traduction (pt 10) n'est pas un rattrapage : le pas s'arrête.
10. **Traductions des exceptions arithmétiques : une liste fermée, deux sites.**
    1. **Dans le moteur** (décision du mainteneur du 27/11/2026, point 2 ; P299). `_appeler` traduit, à l'appel d'une méthode d'étape, exactement deux exceptions :
       - `OverflowError` en `DepassementNumerique` (P139, inchangé) ;
       - `ZeroDivisionError` en un **refus de division**, dérivé de `RefusDuMoteur`. Il porte t, étape et bloc (radical de la méthode appelée), avec `nom = None` : l'arithmétique ne connaît pas la variable. L'exception d'origine est chaînée. Le nom de classe est un contrat de `coder` au rang 3 (proposé : `DivisionParZero`).

       Aucune autre exception n'est traduite : ni `ValueError` de `math`, ni `TypeError`, ni `KeyError`.
    2. **Dans `scenarios/`** : la résolution traduit déjà les deux mêmes exceptions en `EchelleNonRepresentable` (`initial.py:234-236`), inchangé.
    3. **Motif de la liste.** Ces deux exceptions disent que la double précision ne représente plus le résultat. Leur occurrence dépend des données, et un domaine économique ne peut l'exclure en toute expression qu'en se dupliquant. Une autre exception signale un domaine non déclaré ou un défaut de code : elle se corrige par un domaine ou par une forme, jamais par une traduction.
    4. **Condition d'attribution.** Le filet couvre tout ce que la méthode d'étape appelle, vue et noyau compris. Une `ZeroDivisionError` levée par du code du noyau ou du moteur atteint par la vue serait donc attribuée au bloc. Le code du moteur et du noyau atteignable depuis une vue ne divise par aucune grandeur qui puisse être nulle : échelles > 0 par domaine, registre > 0 (ADR 0014, D1). C'est une *hypothèse* que l'audit du rang 3 vérifie par relevé. Les clôtures (`clore_phase`) sont appelées par l'ordonnanceur, hors du filet.
11. **Lecture du critère de #158** (décision du mainteneur du 27/11/2026, point 2) : « aucune exception brute ne sort du moteur ». Il est tenu par les domaines déclarés (pt 18) et par les deux traductions du point 10. Une exception brute d'un autre type qui sortirait de `executer_pas` serait un défaut, au sens du point 10.3 (V3).
12. **Refus de déclaration : inchangé.** `DefautDeDeclaration`, à la construction d'une table (ADR 0014, H3.1) et à l'assemblage (B3). Les domaines de κ et σ (pt 18) s'y rangent.
13. **Refus de chargement d'un état : la forme de D1 est maintenue expressément.**
    - `EtatPays` refuse un champ hors domaine par `ValueError` et un type faux par `TypeError`, sans pas, ni étape, ni bloc. La reprise enveloppe ce refus dans `SauvegardeRefusee` (D4).
    - Décision du mainteneur du 27/11/2026, point 2 : μ̃ hors domaine est refusé par `ValueError` à la construction, par `SauvegardeRefusee` à la reprise, et à l'écriture en phase 5 par `RefusDuMoteur` (`Vue.ecrire_etat` : t, étape « 5 », bloc `prix`, nom ; ADR 0014, B2).
    - C'est le seul cas où un refus du modèle est une `ValueError` : le critère 2 de #194 le prévoit, et l'ADR le prévoit expressément.
14. **Refus du scénario : une racine propre, `RefusDuScenario(Exception)`** (ce que #194 met en œuvre au J4).
    1. **Place.** `RefusDuScenario` est défini dans `nations.scenarios.stationnaire`. C'est le module feuille que le script charge sans `moteur/` (ADR 0015, pt 8.2 ; ADR 0014, annotation du 26/11/2026, pt 4). `EtatStationnaireInexistant` y reste. `NormalisationHorsDomaine` et `EchelleNonRepresentable` restent dans `scenarios/initial.py` et dérivent de `resolveur.RefusDuScenario`.
    2. **Héritage.** Les trois classes **ne dérivent plus de `ValueError`**, et aucune ne dérive d'`ArretMoteur`. Un `except ValueError` générique ne les capte plus, car il capterait aussi les erreurs de domaine de `math` et les refus d'`EtatPays` construits par la résolution.
    3. **Champs.** La racine porte le message. Chaque classe garde ses champs structurés : `conditions` ; `normalisation`, `grandeur`, `valeur`. `NormalisationHorsDomaine` reçoit le nom du champ de `Normalisation` et la valeur refusée. Pas, étape et bloc sont sans objet : la résolution précède le premier pas. Une traduction chaîne sa cause.
    4. **À faire dans #194** : appliquer les points 14.1 à 14.3 ; adapter les `pytest.raises` et les `except` (relevé de #194) ; mettre à jour la docstring de `moteur/diagnostics.py` (familles) et la surface documentaire (pt 22). Aucun label, résultats identiques au bit.
15. **Aucune racine globale.** L'union des familles (« tout refus du modèle ») est une liste fermée de types écrite par l'appelant de J4 (restitution) : `ArretNoyau`, `ArretMoteur`, `SauvegardeRefusee`, `RefusDuScenario`, plus `ValueError` et `TypeError` à la seule construction d'un `EtatPays`. Ce n'est pas une classe de `src/` (options écartées).

### III. Domaines de représentabilité

16. **Une catégorie distincte.** Le projet sépare désormais trois sortes de domaines, chacune nommée comme telle dans le code et dans la spécification :
    - **domaine de définition** : une équation n'a pas de sens au-dehors (W > 0, UC = W/pr ; ADR 0012, annotation du 13/11/2026, point 1.7) ;
    - **condition d'existence** de l'état stationnaire : U^eq, μ̄ (P71), conditions de l'ADR 0015, point 8 ;
    - **domaine de représentabilité** : borne qui ne vient que de binary64 (plage, normalité), **sans contenu économique**, et qui garde finie, ou normale, une expression nommée par son label.

    Membres actuels : S finie (ADR 0014, A3.1) ; « 1/κ fini » ; flottants normaux de l'état résolu (`EchelleNonRepresentable`, S7). S'y ajoutent μ̃, κ et σ (pt 18).
17. **Règles d'un domaine de représentabilité.**
    1. La borne se **calcule** depuis `sys.float_info` (`max`, `min`), au besoin par `math.log`. Elle ne s'écrit jamais en littéral décimal.
    2. Elle déclare la propriété qu'elle garantit, finitude ou normalité, et l'expression protégée.
    3. Elle s'écrit à l'identique dans le moteur et dans `outils/etat_stationnaire.py` quand les deux contrôlent le même paramètre.
    4. Hors domaine, elle refuse, jamais elle n'écrête.
    5. Ce n'est **pas une tolérance** : elle borne une variable ou un paramètre, jamais un résidu d'identité, et n'entre pas dans le noyau. L'invariant « tolérance relative, jamais absolue » (ADR 0005, pt 14 ; ADR 0012, pt 11) ne la concerne pas.
    6. Ce n'est **pas une borne économique** au sens de « toute borne est déclarée ; préférer un mécanisme à une borne » : elle est déclarée, mais n'est active sur aucune trajectoire du domaine économique. Le critère « empreintes inchangées » le vérifie sur les bancs. L'atteindre signifie que la trajectoire a quitté la plage représentable, non que l'économie rencontre une limite.
18. **Domaines retenus** (décisions du mainteneur du 27/11/2026, points 2 et 3).
    1. **μ̃ : |μ̃| ≤ ln(DBL_MAX)**, calculé par `math.log(sys.float_info.max)` (709,782712893384, mesuré). Motif : e^{±μ̃} finis, dans `eq:prix-prix-du-pas` et `eq:travail-salaire-relatif`. Il entre dans `DOMAINES` de `src/nations/etat/prix.py` et il est contrôlé au chargement, à la reprise et à l'écriture en phase 5 (pt 13). Il étend la liste de l'ADR 0012, annotation du 13/11/2026, point 1.7, où μ̃ était « de signe quelconque, sans domaine ». Dans la spécification, « p > 0 par la forme exponentielle » ne vaut qu'en arithmétique exacte, avec un renvoi au filet du point 10.
    2. **κ ≥ DBL_MIN et σ ≥ DBL_MIN** (`sys.float_info.min`, 2,2250738585072014e−308, mesuré) : flottants normaux, sans contenu économique. Ces bornes remplacent κ > 0 et σ > 0 dans la table `production` (`DefautDeDeclaration`) et, à l'identique, dans `outils/etat_stationnaire.py`. « 1/κ fini » en découle (1/DBL_MIN ≈ 4,49e307, mesuré) et peut rester écrit.

### IV. Domaine de la demande adressée (#178) — arrêté par le mainteneur le 27/11/2026, point 4

19. **Aucun code dans `src/`.** d ≥ 0 est une **propriété dérivée**, déjà tenue en trois endroits :
    - par E1 (max(0 ; M^G)) ;
    - par le noyau (M^G < −ε S^G refusé à l'ouverture et à chaque clôture, `eq:noyau-caisse-nette`) ;
    - par `PlanHorsDomaine` (ADR 0014, B4).

    Aucune famille et aucun domaine nouveaux. Le critère est corrigé : tests par appel direct.

### Points soumis au mainteneur

- **V1** (pt 8, 15) : familles classées par moment, sans racine globale ; l'union est écrite par l'appelant de J4.
- **V2** (pt 14) : racine `RefusDuScenario` dans `scenarios/stationnaire.py` ; abandon de l'héritage `ValueError` pour les trois classes ; champs. C'est la forme que #194 met en œuvre.
- **V3** (pt 10.3, 11) : principe de la liste fermée des traductions (exceptions de représentabilité seules). Lecture : une autre exception brute est un défaut, corrigé par un domaine, jamais traduit.
- **V4** (pt 16, 17) : catégorie « domaine de représentabilité » et ses six règles.
- **V5** (pt 18.1, observation de mesure) : à la borne, e^{−μ̃} = 5,56e−309 est **sous-normal** (< DBL_MIN). Le domaine de μ̃ garantit la finitude, celui de κ et σ la normalité ; les deux critères coexistent, chacun déclaré (pt 17.2). T3 reste défini à la borne (1/e^{−μ̃} = 1,80e308, fini). Si `macro` préfère la normalité, la borne serait −ln(DBL_MIN) ≈ 708,40 ; cela n'a pas été instruit. La décision du 27/11/2026 est consignée telle quelle.
- **V6** (pt 7) : sort de la branche `ZeroDivisionError` de `rapport_a_l_echelle`, laissé à `coder` et `audit` au rang 2.

## Options écartées

- **#153, (b) échelle structurelle toujours** (min des S des secteurs touchés, montants nuls compris). Elle n'est pas plus juste. Elle change S dès qu'un terme est nul (ligne 17 sous ΔD_F = 0), donc des rapports publiés dans `ClotureDePhase` (non mesuré), et rouvre (α) au-delà du cas vide.
- **#153, (c) refus typé** (proposé sous le nom `EchelleNonRepresentable`, déjà pris par `scenarios/`). Il arrête une trajectoire légitime, un Trésor vidé par un placement raté, pour une identité tenue à 1e−15 près du bilan de la banque centrale : c'est un faux positif. Ici, le défaut est dans la règle d'échelle, non dans l'état. Le joueur verrait le moteur s'arrêter sur un défaut comptable, ce qui est illisible.
- **#153, (d) lecture littérale de la l. 551**, où le montant de la contrepartie est la variation de ses postes : la porte devient tautologique et ne contrôle plus rien.
- **#153, (β) Σ S_s** (ADR 0012, point 9) et **toute tolérance absolue, `max(1, ·)` ou ε élargi** : restent écartés (ADR 0005, pt 14 ; ADR 0012, pt 11).
- **Racine globale** commune à toutes les familles, dans un module feuille de `nations`. Elle ferait importer au noyau un module hors de `noyau/`, et au script un second module de `nations` (ADR 0014, annotation du 26/11/2026, pt 4). Elle changerait aussi A6 et B, pour un besoin (« tout refus ») que l'appelant couvre par une liste fermée.
- **Refus du scénario dérivés d'`ArretMoteur`** ou de `DefautDeDeclaration`. Le script ne doit pas charger `moteur/` (ADR 0015, pt 8.2), et les champs pas, étape et bloc y sont sans objet.
- **Garder l'héritage `ValueError`** en ajoutant des champs : un `except ValueError` confondrait le refus avec une erreur de domaine de `math` et avec un refus d'`EtatPays`.
- **Traduire toute exception d'une méthode d'étape** (`except Exception`) : cela masquerait les défauts de code sous un refus « du modèle ».
- **Refus propre dans T2 et T3** au lieu du filet : P299 retient le domaine de μ̃ plus le filet générique, qui couvre aussi les divisions des autres blocs.
- **Bornes de représentabilité en littéral** (709, 1e−300) : arbitraires, et non alignées sur la plateforme. **κ > 0 et σ > 0 seuls** : admettent les sous-normaux, où la précision relative se perd.

## Conséquences

- **ADR 0005 et ADR 0014 : annotés, non modifiés.**
  - L'ADR 0005, point 14, est appliqué tel quel : échelle de bilan à l'ouverture, aucune constante absolue, ε inchangé. Il ne reçoit pas d'annotation.
  - L'ADR 0014 reçoit une annotation datée du 27/11/2026, en vigueur à l'acceptation du présent ADR (A5, A6, B5, H1.2, H3.2, G).
  - Le point I complète la règle (α) pour l'ensemble vide, que l'ADR 0012 traitait par l'hypothèse démentie : ce changement de contrat au-delà d'une précision passe par un nouvel ADR, selon l'ADR 0014, Décision 3. La règle (α) n'est pas renversée.
  - L'ADR 0012 ne reçoit plus d'annotation (ADR 0014, Décision 3) : ses points A5, 9 et 1.7 se lisent par l'annotation de l'ADR 0014.
- **Code, par rang de J3-e2.**
  - Rang 2 (#153) : `grand_livre._echelle_de_ligne`, avec sa balise ; docstring de `rapport_a_l_echelle`.
  - Rang 3 (#158) : `DOMAINES` de `etat/prix.py` ; `_appeler` et le refus de division dans `moteur/diagnostics.py`.
  - Rang 4 (#125, point 6) : `moteur/parametres/production.py` et `outils/etat_stationnaire.py`.
  - J4 (#194) : point 14.
- **Effet sur les résultats : aucun.** Critères : empreintes des bancs identiques à `ce3662a` (globale `b8cbd18d…d7d3`) ; sortie du script `052db4c4…4251` inchangée ; rapports des `ClotureDePhase` inchangés sur les bancs ; aucun verdict ne change.
- **Concordance.** 92 / 92 au commit de #153. La balise `# eq:noyau-echelle-ligne` et le label arrivent ensemble : commit `docs:` minimal, selon l'exception de la règle 9, poussé avec le commit `code:`. Le texte complet est écrit au rang 7.
- **Surface pour `docwriter`** (rang 7, un commit `docs:` par issue) :
  - #153 : `sec:cadre-identites`, l. 551 (L2), 553, 637 (définition, hypothèse corrigée), 698 (L1) ; glossaire, l. 4407 ; équation `eq:noyau-echelle-ligne`, avec son encadré ; décomptes des labels du noyau et de la concordance ; journal.
  - #158 : `eq:prix-prix-du-pas` et `eq:travail-salaire-relatif` (« Limites » : arithmétique exacte, renvoi au filet) ; domaine de μ̃ dans `sec:prix-conditions` et dans la table des variables d'état ; filet de division dans `sec:cadre-phases` (paragraphes des domaines et des refus, l. 798-802).
  - #125, point 6 : `sec:production-conditions` et `sec:calibration` (κ, σ, catégorie « représentabilité »).
  - #194 (J4) : sections qui nomment les trois refus (l. 3812 et `sec:finances_publiques-conditions`, relevé à faire).
- **`CONTEXT.md`** : entrées « échelle de repli (d'une ligne) », « domaine de représentabilité » et « famille de refus », à verser à la consignation.
- **Ce que l'ADR ne règle pas.**
  - **#195** : l'identité cumulée (`eq:noyau-tolerance-cumulee`, ε_V × S_{s,t}) jugée contre une échelle effondrée. Le repli ne s'y applique pas, puisque S^CB > 0, et ne la règle pas. Mesure de `monnaie` : `DefautComptable` au pas 8, rapport 3,6e−12 à θ_Tr = 0,35. Toute solution respecte l'ADR 0005, pt 14, et l'absence d'historique dans l'état (ADR 0002), ou passe par un nouvel ADR. D'ici là, le refus reste un `DefautComptable`.
  - #148 (B_CB sous rachat net) ; (1′) de P215 et #143 (ti = 0).
- **Conditions de réouverture** :
  - une trajectoire légitime arrêtée par une porte malgré le repli ;
  - une exception arithmétique autre que les deux de la liste qui se révèle dépendante des seules données ;
  - un besoin, au J4, d'une racine commune que la liste fermée de l'appelant ne couvre pas.

Issues : #153, #158, #125 (point 6), #178, #194, #195 ; liées : #148, #143, #181.
