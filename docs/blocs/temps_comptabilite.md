---
bloc: Temps et comptabilité
module: transverse : src/nations/noyau/ (comptes, grand livre, identités) et src/nations/moteur/ (calendrier, phases) ; radicaux de labels `noyau` et `moteur`
expert pilote: macro
experts consultés: monnaie (bilans de la banque et de la banque centrale : réserves, refinancement, avances) ; jeu (rapport pas / tour)
statut: décidée (M22)
décision: M22 (30/09/2026)
issue: #15
---

# Fiche comparative — Temps et comptabilité

> Fiche ouverte à partir du gabarit `0000-gabarit.md`, **validé à l'usage** sur cette première fiche (M20) : les retours sur le gabarit sont rassemblés pour l'issue #17. Toute rubrique sans contenu porte la mention « non instruit » ou « non mesuré », jamais un vide.

Une fiche comparative instruit **l'origine de l'approche** d'un bloc (`docs/exigences.md` § 2.3) : la spécification v1.5, le moteur v2.0, ou une approche nouvelle. Elle est **instruite par l'expert pilote**, commentée par `jeu` et par l'expert consulté, et **décidée par le mainteneur** (décision M-n, reportée dans `docs/feuille-de-route.md`). Aucune approche n'entre dans le moteur ni dans la spécification sans cette décision. Les agents n'écrivent pas la fiche dans le dépôt : elle figure dans leur compte rendu et la session principale la commite.

Règles de rigueur (`CLAUDE.md`, « Rigueur ») : un chiffre se remesure ou cite sa source ; une équation de la v1.5 n'a jamais été garantie exécutée ; un comportement de la v2.0 ne vaut que sous son profil (état D1) et avec ses défauts connus ; chaque référence est une publication retrouvée. Citer `archive/v1.5/…` avec numéro d'équation et section (ou numéro de ligne du `.tex` quand la section n'est pas identifiable sans compiler), `archive/v2.0/…` avec fichier et ligne.

## 1. Question posée

*Rédigé par `macro` (expert pilote), 30/09/2026.*

Le bloc 1 n'est pas un module de `src/nations/blocs/` : c'est le **cadre** que le noyau comptable et l'ordonnanceur mettent en œuvre (`docs/blocs/README.md` § 1). La fiche instruit donc ce que le cadre **définit**, et non des flux qu'un bloc proposerait au noyau. Toutes les autres fiches expriment leurs vitesses, leurs fenêtres et leurs flux dans ce cadre ; le jalon J2 (noyau) ne démarre qu'une fois la fiche tranchée (ADR 0002, § Conséquences).

### 1.1 Ce que le cadre doit produire

Les grandeurs ci-dessous sont celles que la section « Cadre : temps, entités, comptabilité » (`sec:cadre`, `CONVENTIONS.md` § 1.1) devra fixer. Les symboles sont **provisoires** (la spécification fixe la notation, `CONVENTIONS.md` § 5.2–5.3) ; chaque grandeur porte définition, unité, dénominateur et fenêtre (`docs/exigences.md` § 2.5).

| Grandeur | Définition | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| **Durée du pas** (Δ, provisoire) | Durée de temps simulé entre deux clôtures successives de l'état ; unité de temps du moteur (« pas », `CONTEXT.md`) | semaines simulées par pas (ou fraction d'année par pas, les deux étant données) | — | constante sur toute la simulation |
| **Nombre de pas par an** (n_a, provisoire) | Nombre de pas dont la somme des durées fait une année simulée | pas par an (entier) | par an | constante |
| **Nombre de pas par tour** (n_m, provisoire) | Nombre de pas entre deux dates de décision consécutives ; le tour du jeu est mensuel (décision du mainteneur du 29/09/2026, M4) | pas par tour (entier, constant ou suite périodique déclarée dont la somme sur l'année vaut n_a) | par tour | constante ou périodique sur l'année |
| **Date de décision** | Prédicat sur l'indice de pas t : vrai aux pas où les décisions mensuelles (leviers du joueur, salaires, anticipations, indice des prix) sont révisées (`CONTEXT.md`) ; déductible de t seul, sans compteur caché | booléen | — | évalué à chaque pas |
| **Conversion des taux** | Application unique qui transforme un taux exprimé en base annuelle (fraction par an) en taux par pas ; équation labellisée `eq:moteur-conversion-taux`, jamais recalculée localement (`CONVENTIONS.md` § 5.2 et § 6) | fraction par pas, à partir d'une fraction par an | — | constante |
| **Conversion des vitesses et des fenêtres** | Règle qui transforme un paramètre de vitesse « par an » et une fenêtre « d'un an » ou « d'un mois » en leur équivalent par pas et en nombre entier de pas | par pas ; pas | — | constante |
| **Matrice des bilans** | Tableau postes × secteurs (ménages, entreprises, banque commerciale, banque centrale, État) donnant, pour chaque poste, sa valeur à l'ouverture du pas, signée actif (+) / passif (−) ; chaque poste financier somme à zéro entre les secteurs (la créance de l'un est la dette de l'autre) ; chaque colonne somme à zéro une fois la richesse nette du secteur portée au passif (forme des matrices de Godley et Lavoie, *Monetary Economics*, 2007, chap. 2) | unité monétaire (stock) | — | ouverture du pas t (état d'ouverture, `CONTEXT.md`) |
| **Matrice des flux de transactions** | Tableau flux × secteurs donnant, pour chaque flux exécuté dans le pas (paiement courant ou variation d'un poste financier), le montant signé reçu (+) / versé (−) par chaque secteur ; chaque ligne somme à zéro (tout flux quitte un bilan et entre dans un autre), chaque colonne somme à zéro (contrainte budgétaire du secteur, variations de stocks financiers comprises) (Godley et Lavoie, 2007, chap. 2) | unité monétaire par pas | par pas | le pas t (flux daté du pas où il s'exécute, `CONVENTIONS.md` § 5.2) |
| **Échelle du bilan** | Somme des valeurs absolues des postes du bilan concerné (`CONTEXT.md`) ; dénominateur de toute tolérance sur un montant | unité monétaire | — | ouverture du pas, ou clôture de la phase selon l'identité vérifiée (à fixer par la fiche) |
| **Identités comptables et tolérances** | Liste des égalités qui tiennent par construction (bilan de chaque secteur ; conservation de la monnaie : tout flux débité est crédité ; clôture = ouverture + flux du pas, poste par poste) et, pour chacune, la tolérance ε sous laquelle son résidu est tenu pour nul | résidu rapporté à l'échelle du bilan : sans dimension | échelle du bilan | fin de chaque phase (ADR 0002, couche 1) |
| **Règles de caisse** | Pour chaque flux de la matrice : le payeur, le receveur, le moyen de paiement (dépôt, réserves, avance…), la phase où il s'exécute, et ce qui se passe si le payeur ne peut pas payer (rationnement déclaré, jamais un solde qui absorbe) | — | — | le pas ; phase précisée |
| **Ordre des phases d'un pas** | Liste numérotée des phases, identique dans la spécification et dans l'ordonnanceur (ADR 0002, couche 3), avec pour chaque phase les blocs qui y lisent et ceux qui y écrivent | — | — | le pas |
| **Empreinte calendaire de l'état** | Liste des variables d'état que le calendrier impose (indice de pas, variables retardées déclarées telles que « indice des prix il y a un an ») ; aucun historique dans l'état (ADR 0002, couche 4) | nombre de variables ; unité de chacune | — | état de clôture |

### 1.2 Ce qu'il lit

- **Rien du moteur** : le cadre précède tous les blocs.
- Le **tour du jeu**, mensuel (décision du mainteneur du 29/09/2026 ; M4 ; `docs/exigences.md` § 5.2) : il contraint le rapport entre pas et tour, non la durée du pas (`CONVENTIONS.md` § 6).
- Le **budget de calcul** : au plus 1 ms par pays-semaine (M13 ; `CLAUDE.md`, « Architecture », invariant 3), soit, par arithmétique, 52 ms par pays et par an simulé, et 52/n_a ms par pays-pas.
- Les **invariants de l'ADR 0002** que le cadre met en œuvre : point d'exécution unique des flux (noyau), tolérances relatives à l'échelle du bilan, phases numérotées, aucun historique dans l'état, aucune optimisation itérative à chaque pas, état initial résolu.
- La **convention de datation** déjà fixée : x_t valeur d'ouverture, x_{t+1} valeur de clôture, flux daté du pas où il s'exécute (`CONVENTIONS.md` § 5.2).

### 1.3 Frontières

- **Tous les blocs du socle** (2 à 9) : chacun déclare ses vitesses en base annuelle et les convertit par la règle du cadre ; chacun place ses flux dans une phase et dans une ligne de la matrice des flux.
- **`monnaie`** : postes et flux des bilans de la banque commerciale et de la banque centrale (réserves, refinancement, avances au Trésor, fonds propres) ; critères 9 (b), 10 (b) et (c), 11 (b) à (d), 12 (b) et (c), 14 et 7 (b) du § 2 ; avis au § 6.
- **`jeu`** : rapport pas / tour, dates de décision, lisibilité des délais en tours ; critères 4 (c), 5 (b), 7 (c), 8, 12 (d) et 13 (b) du § 2 ; avis au § 7.
- **`etat/`** (schéma d'état, J2) : le cadre fixe combien de variables retardées le calendrier impose et lesquelles ; la forme du schéma relève de J2.

### 1.4 Ce que la fiche ne tranche pas

- Le **contenu économique des blocs** : équations, paramètres, nombre de secteurs productifs (fiche « production et stocks » : la matrice du cadre est écrite par secteur institutionnel, la sous-division de la colonne « entreprises » par secteur productif est renvoyée à cette fiche), règle de consommation, corridor de taux, loi de crédibilité (pistes de `docs/feuille-de-route.md` § 5).
- Les **barrières entre pays** et l'**ordre canonique des pays** dans les agrégations (J5 ; `CLAUDE.md`, invariant 2) : le cadre du socle est écrit pour un pays ; la fiche dit seulement ce qu'elle laisse ouvert pour que le secteur « reste du monde » s'ajoute en colonne sans réécrire les matrices.
- Le **régime de souveraineté** A à E et les leviers qu'il ouvre (J5).
- Les **postes d'actifs** hors socle (immobilier, actions, prêts sur marge) et les crises (J6) : la matrice du socle ne les contient pas ; la fiche dit comment une ligne s'ajoutera.
- Les **valeurs numériques** de l'état stationnaire (J3) : la fiche vérifie que le cadre permet le calcul, elle ne le fait pas.

## 2. Critères d'évaluation, écrits avant l'instruction

Liste **fermée**, fixée avant toute mesure ; elle ne se déplace pas après observation (`docs/exigences.md` § 2.5). **Statut : validée par le mainteneur le 30/09/2026 (point de décision de l'issue #15), avec les amendements de la sous-section « Amendements adoptés », qui prévalent sur le texte du tableau là où ils le modifient.**

Liste courte, établie par `macro` sur décisions du mainteneur du 30/09/2026 :
1. le rapport pas / tour (critère 8) est une **mesure**, qui n'écarte aucune option d'avance ;
2. la valeur nette, seule grandeur résiduelle, est calculée deux fois (critère 10 (c)) ;
3. les critères qui en précisaient un autre y sont regroupés sous une lettre, sans perte de contenu vérifiable.

La version longue (34 critères) est au commit `1ed2050` ; la table de correspondance suit le tableau. Provenance de chaque exigence entre parenthèses : `macro` ; `monnaie` B-n ; `jeu` J-x. Les numéros de ligne cités par `monnaie` et `jeu` restent sous leur responsabilité ; ceux de `macro` ont été vérifiés le 30/09/2026.

Aucun de ces critères ne préjuge : pas hebdomadaire ou mensuel ; corridor ou taux unique ; base de réserves rémunérée totale ou partielle ; conversion composée ou linéaire ; compte du Trésor à la banque ou à la banque centrale ; existence des billets ; existence des avances dans le socle. Chacun demande que la fiche **déclare** le choix et rende son effet vérifiable (`monnaie`). Chaque critère vaut quel que soit le nombre de pas par tour (`jeu`).

**Principe de simplicité** (proposé par `macro`, adopté par le mainteneur le 30/09/2026 ; règle d'arbitrage entre options, mesurée par le critère 6) :
- À exigences comptables égales (matrices à sommes nulles, aucun poste calculé comme résidu, tolérances relatives à l'échelle du bilan, reprise exacte), l'option la plus simple est préférée. Elle l'est pour le joueur (moins de dates, de délais et de grandeurs à lire) comme pour le moteur (moins de postes, de lignes de flux, de phases, de paramètres et de variables d'état).
- Toute complexité supplémentaire se justifie par l'une de deux raisons seulement : une identité comptable qu'elle rend vérifiable, ou un mécanisme que le joueur perçoit à l'échelle d'une partie (critère 5).
- Réciproquement, une simplification ne supprime ni une contrepartie comptable visible d'un levier du socle ni une grandeur restituée au tour (critère 7 (c)) ; la granularité de la restitution peut se simplifier au-dessus du tour, jamais en dessous (`jeu`, adopté le 30/09/2026).
- Une complexité « pour plus tard » (J5, J6) ne se code pas dans le socle : le cadre dit seulement comment la ligne ou la colonne s'ajoutera sans réécrire les matrices (§ 1.4).
- **Ne se simplifie pas**, parce que c'est ce qui rend le modèle juste et reproductible :
  - les identités (critères 1, 10, 11 (a)) ;
  - les tolérances relatives (9) ;
  - le déterminisme et la reprise exacte (13) ;
  - les invariants de l'ADR 0002 : point d'exécution unique des flux, phases numérotées sans lecture d'une phase ultérieure (12 (a)), aucun historique dans l'état, aucune itération à chaque pas, état initial résolu (2) ;
  - la concordance spécification ↔ moteur.
- **Peut se simplifier**, et le cadre le **déclare** plutôt qu'il ne l'impose : la liste des instruments du socle (billets, avances, sous-postes), le nombre de taux administrés, la périodicité des intérêts, la localisation du compte du Trésor, le nombre de phases, la régularité des tours, la granularité de la restitution, le nombre de variables retardées.

| N° | Critère | Ce qui est attendu | Comment on le vérifie |
|---|---|---|---|
| 1 | Cohérence stock-flux (gabarit, adapté) | Le cadre est tel que **tout** flux de tout bloc du socle a une ligne de la matrice des flux et modifie des postes de la matrice des bilans ; aucune monnaie créée ni détruite hors d'une ligne de la matrice ; les identités touchées se bouclent sans solde résiduel (`macro`) | Matrices de l'option écrites en tableaux ; contrôle des sommes par le script de l'issue #19 ; relecture par `macro` (secteurs réels et État) et `monnaie` (banque, banque centrale) |
| 2 | État stationnaire : forme fermée, indépendante des vitesses et de la durée du pas (gabarit, adapté) | (a) Le cadre n'introduit aucune grandeur qui ne s'écrive à l'état stationnaire en forme fermée ; aucune de ses conventions (datation, conversion, fenêtres) ne fait dépendre l'état d'arrivée d'une vitesse d'ajustement (`macro`). (b) Le cadre permet de calculer l'état stationnaire par un script d'`outils/`, sans simulation (critère de passage de J1, M19) : toute variable retardée déclarée a une valeur stationnaire explicite (par exemple, indice des prix il y a un an = indice courant / (1 + π̄)), le facteur de conversion et les fenêtres ont une expression stationnaire, et aucune phase ne demande une valeur qui n'existe qu'après simulation (`macro`, issue #15 n° 8). (c) Les ratios stationnaires écrits en base annuelle (stock sur PIB annuel, taux réel annuel, inflation annuelle) ne dépendent pas de n_a : la durée du pas change la transition, jamais l'état d'arrivée (`CLAUDE.md`, « Rigueur » ; `CONVENTIONS.md` § 6 : paramètres exprimés par an) (`macro`) | Calcul à la main donné dans la fiche pour chaque option ; écriture stationnaire des grandeurs du cadre, confirmée par le script de J1 (M19) ; calcul à la main sur la règle de conversion des taux et des vitesses ; si une option viole (c), la fiche le dit et documente le continuum (`docs/exigences.md` § 2.7) |
| 3 | Stabilité (gabarit) | Aucune instabilité connue réintroduite sans fait nouveau ; pour ce bloc, en particulier l'instabilité 16 (« tolérances absolues sur des soldes résiduels ou des montants en unité locale », `archive/faits_mesures_G_K.md` § 6) et le défaut « un plafond produit un cycle » (instabilité 15) s'il devait s'appliquer à une borne du cadre (`macro`) ; les instabilités 2 (avances sans intérêt) et 3 (coupon au taux du moment) sont traitées au critère 14 | Liste des instabilités d'`archive/faits_mesures_G_K.md` § 6, reprise dans `sec:chantiers` de la spécification (`tab:instabilites`) ; pour chaque option, la fiche dit lesquelles sont concernées |
| 4 | Coût de calcul et lecture du budget selon le pas (gabarit, adapté) | (a) Coût du **noyau seul** par pas (nombre de flux exécutés, de postes mis à jour, d'identités vérifiées par phase) compatible avec le budget par pas de (b) ; aucune résolution itérative dans le cadre ; le coût du noyau seul est un critère de J2 (M19), pas de cette fiche : ici, un décompte suffit (`macro`). (b) Le budget est fixé par pays-semaine (M13) ; la fiche donne, pour chaque option, le budget équivalent par pas : 1 ms × 52 / n_a par pays-pas (arithmétique), et 52 ms par pays-an quelle que soit l'option ; si le pas est mensuel, le budget par pas est écrit explicitement et c'est lui que le test de J3 mesure (`macro`, issue #15 n° 3). (c) Coût maximal d'un tour = N × (semaines par tour) × 1 ms, hors barrières (J5) et hors IA (J7) ; indépendant du nombre de pas par tour ; la fiche fixe la valeur de `semaines_par_pas` que lira `tests/invariants/test_budget.py`. Seuil ludique écrit avant l'essai : un tour d'un monde à 10 pays sous **1 s** de moteur sur la plateforme de référence, et 60 ans d'un pays en « quelques secondes » (`docs/exigences.md` § 4.4) (`jeu` J-e) | Décompte d'opérations par pas, exprimé dans l'unité de (b) ; arithmétique donnée dans la fiche par option, pour N = 1, 4 et 10 ; le test de budget (J3, M19) est écrit contre la valeur de (b) ; à J2/J3, `tests/invariants/test_budget.py::secondes_par_pays_semaine` avec la valeur de `semaines_par_pas` fixée par la fiche |
| 5 | Lisibilité pour le joueur et perceptibilité à l'échelle d'une partie (gabarit) | (a) Le joueur identifie la date de décision, sait quels flux se produisent entre deux tours et peut lire tout délai d'un bloc en nombre entier de tours (`macro`). (b) Fenêtre de partie : 5 à 10 ans = **60 à 120 tours** (O5). Le joueur peut **dater un effet au tour près** et distinguer un délai d'un tour d'un délai de 6 à 18 mois (ordres de grandeur **rapportés** par la v1.5, l. 1800–1803, jamais vérifiés, non repris comme cibles). Aucun effet plus rapide que le tour sans contrepartie visible dans le même tour ; aucun délai de transmission du socle plus court que ce que la restitution au tour peut distinguer de l'instantané (`jeu` J-c) | Avis de `jeu` (§ 7), adossé aux tableaux des critères 8 et 12 ; par option, durée d'une partie type en pas et en tours, et plus court délai représentable (un pas) en fraction de tour ; au § 9, chaque levier déclare son délai attendu **en tours** avec la contrepartie comptable visible le même tour. Vérification à J4 : scénario apparié par levier, effet du signe attendu daté au tour près (test O2) |
| 6 | Simplicité : nombre de paramètres, de bornes, de postes, de lignes de flux, de phases et de variables d'état (gabarit, élargi par le principe de simplicité) | Le cadre n'introduit que des paramètres déclarés (durée du pas, nombre de pas par an et par tour, tolérances ε) et **aucune borne** ; toute borne qu'une option exigerait est déclarée et motivée contre un mécanisme (`macro`). Chaque poste de bilan, ligne de flux, phase et variable d'état du cadre est justifié par une identité qu'il rend vérifiable ou par un mécanisme perçu par le joueur (critère 5) (`macro`, principe de simplicité) | Décompte par option, en tableau : paramètres, bornes, postes, lignes de flux, phases, variables d'état ; pour chaque élément, sa justification |
| 7 | Cohérence calendaire, conversions et fenêtres (issue #15, n° 1) — **amendé, voir « Amendements adoptés »** | (a) n_a est un entier ; un tour vaut un nombre entier de pas (constant, ou suite périodique déclarée dont la somme sur l'année vaut n_a) ; une **seule** conversion des taux (`eq:moteur-conversion-taux`) et une seule règle de conversion des vitesses et des fenêtres, précisée en (b) ; toute fenêtre « d'un an » vaut exactement n_a pas et toute fenêtre « d'un mois » exactement n_m pas ; aucune division locale par un nombre de périodes (la loi de crédibilité v2.0 divise par 13 en ligne, `archive/faits_mesures_G_K.md` § 4, K1a) (`macro`). (b) Le cadre distingue et déclare une fois, dans `eq:moteur-conversion-taux` (`CONVENTIONS.md` § 5.2) ou à côté : un **taux d'intérêt** annuel converti de façon composée (1+i)^(1/n) − 1 (v1.5 l. 402 ; v2.0 `wk()` l. 40–41) ou linéaire i/n ; un **flux annuel** réparti linéairement X/n (v2.0 l. 1021, 1203, 1212) ; une **vitesse d'ajustement** annuelle λ, convertie en λ/n ou en 1 − (1 − λ)^(1/n) (v2.0 l. 1305). L'effet du choix sur la capitalisation annuelle est chiffré. Calcul de `monnaie` du 30/09/2026 (`uv run python`) pour i = 4 % par an : composé, capitalisé 4,0000 % par an avec 52 ou 12 pas ; linéaire, 4,0795 % (52 pas) ou 4,0742 % (12 pas). Avec la conversion linéaire, le taux annuel effectif dépend du pas ; avec la composée, non (`monnaie` B12). (c) Toute grandeur restituée est définie **sur la fenêtre du tour** : stock à la clôture du tour ; flux cumulé sur le tour, et sur 12 tours pour tout ratio « au PIB annuel » ; taux en base annuelle ; glissement annuel d'un indice = tour n contre tour n − 12, **exactement**. Aucune grandeur restituée n'est un « par pas » nu ; la définition d'un flux mensuel ne dépend pas du nombre de pas par tour. Les indicateurs d'alerte se calculent sans historique dans l'état (`jeu` J-d) | Arithmétique donnée dans la fiche pour chaque option ; rappel de l'incohérence v1.5 : mois de 4 ticks (`archive/v1.5/Nations_et_Marches_v1_5.tex` l. 400) et conversion par 1/52 (l. 402), soit 48 ≠ 52 ; v2.0 : `WEEKS = 52`, `DECISION_WEEKS = 4`, `PERIODS_PER_YEAR = 13` (`archive/v2.0/prototype/model.py` l. 36–38), soit 13 « mois » par an. Arithmétique donnée pour les trois natures de conversion ; aucun coefficient « par semaine » ou « par mois » ailleurs que dans cette équation (`CONVENTIONS.md` § 6) ; contrôle prospectif pour J2 : un test qui capitalise un encours constant sur un an et compare au taux annuel déclaré. Le tableau des grandeurs du § 1 porte une colonne « fenêtre » exprimée en tours ; liste des variables d'état datées nécessaires (indice des prix à t − 12 tours, etc.) avec leur décompte (voir critère 13) ; contrôle à J2 que `observation/` produit ces séries sans effet sur la trajectoire (ADR 0002) |
| 8 | Rapport pas / tour : mesure de la régularité des tours (issue #15, n° 2 ; `jeu` J-a, reformulé en mesure sur décision du mainteneur du 30/09/2026) — **amendé, voir « Amendements adoptés »** | Pour chaque option, la fiche **déclare et évalue**, sans qu'aucune valeur n'écarte l'option d'avance : le nombre de pas par tour (constant ou suite périodique) ; le nombre de tours par an et, s'il diffère de 12, l'écart au tour mensuel (M4) ; l'existence d'un pas résiduel, de mois de longueur variable ou d'une 13e période ; si l'année du joueur (en tours) et l'année de la conversion des taux (critère 7) coïncident. Reste exigé quelle que soit l'option : exactement **une date de décision par tour**, au premier pas du tour ; le joueur lit une date (année, mois), jamais un numéro de pas. L'irrégularité éventuelle est évaluée par `jeu` : perceptible ou non par le joueur, et à quel coût de lisibilité | Tableau de 24 tours dans la fiche, par option : pour chaque tour, indices du premier et du dernier pas, pas portant la date de décision, mois et année affichés ; identité « pas par an = somme des pas des tours d'une année » posée en toutes lettres (elle se réduit à pas_par_an = 12 × pas_par_tour quand les tours sont égaux) ; contrôle de ce qu'affiche le tour 13 par rapport au tour 1 (même mois avec l'année + 1, ou l'écart déclaré). L'arithmétique commune avec le critère 7 n'est vérifiée qu'une fois ; avis de `jeu` sur la perceptibilité |
| 9 | Tolérances relatives à l'échelle du bilan, invariantes par redénomination (issue #15, n° 4) | (a) Toute tolérance s'écrit ε × échelle du bilan, ε sans dimension et déclaré ; l'échelle est la somme des valeurs absolues des postes (`CONTEXT.md`) ; aucun seuil de la forme « absolu sous 1, relatif au-dessus » ni rapporté à un flux (v2.0 : `1e-9*max(1., …)`, `model.py` l. 55 et `worldn.py` l. 166 ; `1e-8*max(|Y|, 1)`, `model.py` l. 1463–1469) ; ε est justifié par l'arithmétique en double précision (nombre d'opérandes) et non choisi à l'œil ; sous redénomination ×100 de tous les nominaux, chaque ratio résidu / échelle est inchangé (`macro`). (b) Pour la banque centrale, la tolérance est rapportée à **l'échelle de son propre bilan**, jamais aux fonds propres ni à une constante. Défauts à exclure : `numerical_audit.py` l. 17, `max(1., abs(e.E_cb))` ; `model.py` l. 1463, `max(abs(f["Y"]), 1.)` (identité de stock rapportée à un flux). L'échelle `B_close` des faits § 1.3 omettait Res, B^CB, A^G, E^CB : l'échelle v3 inclut tous les postes du bilan contrôlé (`monnaie` B4) | Examen à la main, dans la fiche, de la tolérance proposée sous ×100 ; faits G2, J2, K2c (`archive/faits_mesures_G_K.md` § 5) ; test d'invariance d'unité en J2 (critère de passage). Formule écrite dans la fiche pour les deux bilans (banque, banque centrale) ; examinée sous ×100 **et** sous E^CB = 0 puis E^CB < 0 (la v1.5, l. 1006, admet des fonds propres négatifs) |
| 10 | Aucun solde de bilan calculé comme résidu ; la valeur nette, seule grandeur résiduelle, calculée deux fois (issue #15, n° 5) | (a) Chaque poste de chaque bilan à la clôture vaut son ouverture plus la somme des flux **décidés** qui le touchent dans le pas ; aucun poste n'est obtenu par différence des autres postes ; en particulier réserves et refinancement (v2.0 : `Res` dérivé du bilan bancaire puis reporté sur `L_cb` s'il est négatif, `archive/v2.0/prototype/model.py` l. 1278–1283, 1574–1575, 1631–1632 ; ADR 0001 § 6) ; la richesse nette est la seule grandeur définie comme solde, et aucun flux ne s'en déduit (`macro`). (b) ΔRes et ΔL^CB d'un pas sont chacun la **somme de lignes nommées** de la matrice des flux. Un besoin de réserves se règle par un **flux de refinancement décidé dans une phase nommée**, à un taux nommé ; aucune règle « si Res < 0 alors L^CB += −Res ». Défaut à exclure : `model.py` l. 1280–1283 (et copies l. 556–557, 1574–1575, 1631–1632 : quatre points d'écriture d'une même identité, source des dérives d'arrondi des faits G2, H2, J2/K2b, `archive/faits_mesures_G_K.md` § 5) (`monnaie` B2). (c) Les fonds propres E^Bk, E^CB (et la valeur nette de chaque secteur) bouclent par définition la colonne du bilan (Godley et Lavoie, 2007, *Monetary Economics*, chap. 2). Ce n'est pas un solde résiduel au sens de (a) à condition que la valeur nette soit calculée **deux fois** : par le stock (actifs − passifs) et par les flux (ouverture + résultat − distribution), l'écart entre les deux étant l'identité vérifiée, jamais un poste ajusté. Défaut à exclure : `model.py` l. 562 et l. 1633, où E^CB est posé égal à actifs − passifs, ce qui rend circulaire `central_bank_check` (`numerical_audit.py` l. 10–20) (`monnaie` B3 ; accepté par le mainteneur le 30/09/2026) | Pour chaque poste de la matrice des bilans, la fiche donne la liste des flux qui le modifient et leur phase ; un poste sans flux, ou déterminé par « le reste », fait échouer le critère ; relecture de `monnaie` pour les postes de la banque et de la banque centrale. Dans la matrice des flux, les lignes dont la somme donne ΔRes et ΔL^CB sont listées ; dans le tableau phase → blocs (critère 12), la phase où le refinancement est décidé suit tous les règlements du pas ; contre-épreuve à la main : un pas où les règlements font baisser Res sous zéro produit une ligne de flux « refinancement » explicite, pas une correction de solde. La fiche donne, pour la banque et la banque centrale, les deux expressions de la valeur nette et désigne l'identité de contrôle ; aucune des deux n'est écrite comme affectation d'un poste |
| 11 | Matrices en tableaux : postes nommés, un émetteur par instrument, sommes nulles, portes de création monétaire, compte du Trésor (issue #15, n° 6) — **amendé, voir « Amendements adoptés »** | (a) Matrice des bilans et matrice des flux écrites en tableaux dans la fiche puis dans `sec:cadre` ; toutes les lignes de la matrice des flux et tous les postes financiers de la matrice des bilans somment à zéro ; toutes les colonnes somment à zéro (richesse nette incluse) ; unités et fenêtres déclarées en tête de tableau (stocks à l'ouverture en unité monétaire ; flux en unité monétaire par pas) ; une ligne par flux du socle, un poste par ligne de bilan (`macro`). (b) La matrice des bilans comporte une colonne « banque » et une colonne « banque centrale », et une ligne par instrument : dépôts D, crédits L, titres publics détenus B^Bk et B^CB, réserves Res (monnaie centrale), refinancement L^CB, avances au Trésor A^G, compte du Trésor M^G, fonds propres E^Bk et E^CB, billets C s'ils existent (la v1.5 les a, l. 414 et 420 ; la v2.0 n'a que des dépôts). Chaque instrument a **exactement un émetteur** (signe −) et un ou plusieurs détenteurs (signe +). Chaque poste porte définition, unité, fenêtre. Incohérence de la v1.5 à exclure : la table des bilans (l. 414) omet A^G et E^CB que l'identité de la banque centrale (l. 995) contient (`monnaie` B1). (c) Le cadre liste **exhaustivement** les lignes de la matrice des flux qui font varier la masse monétaire (D, plus C) et celles qui font varier la monnaie centrale (Res, plus C) ; toute autre ligne est un transfert entre détenteurs. La v1.5 (l. 485) nomme quatre portes pour M ; la fiche v3 donne sa propre liste. Préalable comptable à l'intention de conception du 17/09/2026 (une création monétaire durable se traduit par une inflation durable) : elle n'est testable que si la création est visible (`monnaie` B5). (d) Le cadre dit **où est tenu le compte du Trésor** : à la banque commerciale (v2.0 : dépôt du grand livre bancaire) ou à la banque centrale (v1.5 l. 415, ambigu). Ce choix décide si un impôt ou une dépense publique déplace des réserves, donc si un besoin de refinancement peut naître des paiements de l'État (`monnaie` B6) | Script d'`outils/` de l'issue #19, lu depuis la spécification ; en attendant, vérification à la main dans la fiche. Pour chaque ligne de la matrice des bilans, un seul signe − ; chaque poste de l'identité de bilan écrite dans le texte figure dans la matrice, et réciproquement (script de #19 si sa convention le permet ; sinon relecture de `monnaie`). Pour chaque ligne de la matrice des flux, colonnes « effet sur M » et « effet sur H » (0, +, −) ; ΔM et ΔH recalculés depuis la matrice égalent la variation des postes du bilan (script de #19 s'il lit ces colonnes). Matrice des bilans : la ligne « compte du Trésor » a pour émetteur soit la banque, soit la banque centrale ; liste des flux qui touchent Res (croisement avec les critères 10 (b) et 11 (c)) |
| 12 | Ordre des phases : flux unique, lectures antérieures, monnaie centrale, dates d'effet des décisions (issue #15, n° 7) — **amendé, voir « Amendements adoptés »** | (a) Chaque flux s'exécute dans une phase unique et une seule ; chaque bloc ne lit que l'état d'ouverture ou des variables produites dans une phase antérieure du même pas ; aucune lecture d'une variable écrite dans une phase ultérieure (sinon résolution simultanée, donc itération, exclue par l'ADR 0002, invariant 11) ; les identités sont vérifiées à la fin de chaque phase (`macro`). (b) Tous les règlements du pas (salaires, achats, impôts, dividendes, achats de titres) précèdent la phase où la banque constate sa position de réserves et où la banque centrale exécute ses opérations ; les intérêts sur Res et L^CB sont assis sur l'encours d'**ouverture** (ou de clôture, à dire), dans une phase nommée. La v1.5 (l. 422–432) place « Finance » (phase 5) avant « État » (phase 7, intérêts et dette) : le cadre v3 dit dans quelle phase les intérêts publics se règlent et si leur règlement peut créer un besoin de réserves après la phase de refinancement (`monnaie` B13). (c) Le taux qui s'applique aux flux d'intérêt d'un pas t est celui décidé à la **dernière date de décision antérieure** à t (ou égale, à dire), avec le **délai en pas** entre décision et premier flux d'intérêt qui la porte. Les grandeurs lues par la règle de taux (inflation observée, glissement annuel de l'indice) sont datées de la date de décision, sur une fenêtre en **nombre entier de pas**, par des **variables d'état retardées déclarées**, sans historique (ADR 0002). Défaut à exclure : `model.py` l. 1292–1294, `P_hist[-1-13]` (`monnaie` B8). (d) Un levier saisi à la date de décision du tour n s'applique dans le tour n à partir d'une **phase identifiée**, jamais sur un pas déjà exécuté ; un levier à délai porte un délai en **tours entiers**, déclaré dans le catalogue, tenu par une **variable d'état datée**, pas par un historique (ADR 0002). Toutes les décisions d'un tour (joueurs, plus tard IA) sont lues dans la **même phase, avant tout flux du tour** ; l'ordre de saisie n'a aucun effet (`jeu` J-b) | Tableau phase → blocs qui écrivent / blocs qui lisent, donné dans la fiche ; la matrice de dépendance qu'il induit est triangulaire (vérification à la main ; test en J2). Dans ce tableau : aucune ligne de flux qui touche Res n'est exécutée après la phase de refinancement du même pas, ou, si c'en est une, la fiche dit comment la position de fin de pas est financée ; la phase de décision précède le calcul des intérêts du pas où le nouveau taux entre ; exemple daté à la main (décision au pas t, premier intérêt au taux nouveau au pas t+k, k déclaré, soumis à `jeu` au titre du critère 5) ; liste des variables retardées que le glissement annuel exige (reportée au critère 13) ; une ligne « lecture des leviers » avant toute phase de flux ; pour trois leviers types du socle (taux directeur, taux d'imposition, dépense publique), phase de lecture, premier flux modifié et **délai minimal en tours** (décompte à J1, mesure par scénario apparié à J4, test O2) |
| 13 | Empreinte calendaire de l'état et reprise exacte, y compris à la frontière de tour (ajout `macro`) | (a) Le calendrier n'impose que des variables d'état déclarées (indice de pas ; variables retardées nommées, dont celles exigées par les critères 7 (c) et 12 (c)), aucun historique ni compteur caché ; la date de décision se déduit de l'indice de pas seul ; l'état de clôture d'un pas suffit à reprendre la simulation à l'identique (`CLAUDE.md`, invariant 2 ; ADR 0002, couche 4) (`macro`). (b) L'état de clôture d'un tour est **complet** : aucune variable « en attente » d'un pas partiel, aucune fenêtre glissante intra-tour ; une sauvegarde prise à la frontière de tour, rechargée, reproduit la trajectoire **bit à bit**, y compris si des décisions différentes sont saisies après la reprise (contrefactuel apparié, base du test O2). Le jeu n'a jamais besoin d'une sauvegarde en milieu de tour (`jeu` J-f) | Décompte, par option, des variables d'état que le calendrier impose, avec leur unité ; à J1, la fiche déclare que la frontière de tour coïncide avec une frontière de pas et liste les variables d'état datées ; à J2, test de reprise (invariant 2), test de reprise à la frontière de tour (O4) et cas « reprise puis décisions différentes » qui ne diverge qu'à partir de la phase de lecture des leviers |
| 14 | Instruments porteurs d'intérêt : intérêts courus, corridor, avances au Trésor, résultat de la banque centrale (`monnaie`) — **amendé, voir « Amendements adoptés »** | (a) Pour chaque instrument porteur d'intérêt, le cadre donne la **base** (encours d'ouverture), la **périodicité** (versé à chaque pas, ou couru et versé à une date fixée) et **où va un intérêt couru non versé** : poste « intérêts courus » identifié, ou capitalisation par une **ligne de flux nommée**. Aucun intérêt n'entre silencieusement dans un poste de principal. Défauts à exclure : `model.py` l. 1178–1182 (intérêt impayé de l'État ajouté aux encours, E^CB crédité payé ou non) ; l. 1016 (intérêt d'entreprise impayé ajouté à `Loans`). Instabilité n° 3 des faits § 6 (coupon au taux du moment) : tout coupon porte sa date de fixation (`monnaie` B9). (b) Le cadre permet, sans les imposer, jusqu'à **trois taux administrés distincts** (rémunération des réserves, refinancement, taux directeur), chacun taux annuel converti une seule fois (critère 7). La matrice des flux comporte **deux lignes séparées** « intérêts sur réserves » et « intérêts sur refinancement », chacune avec sa base, son taux et sa fenêtre. Le cadre ne fixe aucun de ces taux ni leur écart (`monnaie` B7). (c) Si le cadre prévoit la ligne A^G (ouverture par régime : J5 ; règle : fiche 9 avec avis de `monnaie`), elle est un **instrument complet** : poste à l'actif de la banque centrale et au passif de l'État, flux de tirage, de remboursement, d'intérêt (a), effet sur M et H déclaré (critère 11 (c)). Instabilité n° 2 des faits § 6 (avances sans intérêt) ; la v2.0 garde une part gratuite `AG_free` (l. 564, 1177) : aucun sous-poste sans intérêt sans le déclarer comme borne ou exception (`monnaie` B10). (d) La matrice des flux comporte les lignes du compte de résultat de la banque centrale et une ligne « versement du résultat à l'État », **calculée sur le résultat d'une fenêtre déclarée**, jamais sur le stock E^CB ; fenêtre et date de versement données. Défaut historique : v1.5 l. 1012, distribution hebdomadaire d'une fraction du stock, « +50 % de dépôts la première année » (chiffre **rapporté**, non remesuré) ; v2.0 l. 1207–1209. La règle elle-même relève de la fiche 8 (`monnaie` B11) | Tableau instrument × (base, taux annuel, périodicité, poste d'accueil de l'intérêt couru, ligne de flux de capitalisation) ; à la main : sur un encours constant X et un taux annuel i, les intérêts d'une année valent iX à la capitalisation intra-annuelle déclarée près, quel que soit le pas. Les deux lignes d'intérêts (réserves, refinancement) existent dans la matrice des flux avec base, taux, fenêtre ; aucune équation de taux dans la fiche (renvoi à `banque_centrale.md` et `banque.md`) ; le cadre n'interdit pas une base rémunérée partielle. Ligne A^G présente dans les deux matrices avec ses quatre flux ; colonne « effet sur M/H » remplie ; aucune fraction gratuite implicite. Lignes du compte de résultat présentes ; fenêtre et date du versement écrites ; le versement est une fonction de lignes de flux de la même fenêtre, pas d'un poste de bilan |

Adaptations signalées par `macro` :
- critères 1, 2 et 4 reformulés pour un bloc qui *définit* le noyau au lieu de lui rendre des flux ;
- au critère 9 (a), « ε justifié par l'arithmétique en double précision » (fait G2 : résidus en fractions dyadiques du pas flottant d'un bilan d'environ 6,6e11) ;
- au critère 12 (a), la triangularité comme test mécanique de l'ordre partiel ;
- critère 13 (a), parce que le calendrier impose les variables retardées que l'ADR 0002 oblige à déclarer ;
- critère 2 (c), parce que la durée du pas est la vitesse d'ajustement la plus générale du modèle (distinct de 2 (b) : un état peut être calculable en forme fermée et dépendre de n_a).

### Amendements adoptés (principe de simplicité, 30/09/2026)

Proposés par `macro`, examinés par `monnaie` et `jeu`, adoptés par le mainteneur le 30/09/2026. Ils prévalent sur le texte du tableau là où ils le modifient ; les défauts à exclure et leurs sources restent en place. Aucune identité ni aucun invariant n'est touché.

| Critère | Texte adopté | Origine |
|---|---|---|
| 7 (b) | **Déclarer** : le cadre déclare, pour chacune des trois natures (taux d'intérêt, flux annuel, vitesse d'ajustement), la règle de conversion retenue, dans `eq:moteur-conversion-taux` ou à côté ; deux natures peuvent partager une règle si la grandeur annuelle correspondante (taux annuel effectif ; total annuel du flux ; fraction annuelle de l'écart résorbée) est invariante par n_a. La fiche chiffre l'effet du choix pour un taux (4,0000 / 4,0795 / 4,0742 %) et pour une vitesse (λ = 0,5 par λ/n : 0,3949 de l'écart résorbé en un an sur 52 pas, 0,3999 sur 12 pas) | `macro`, reformulé par `monnaie` : une règle unique est exacte pour les taux, pas pour les vitesses. Calcul de `monnaie`, recalculé par la session principale le 30/09/2026 (`python3`, 1 − (1 − λ/n)^n) : λ = 0,1 → 0,0952 / 0,0955 ; 0,5 → 0,3949 / 0,3999 ; 1 → 0,6357 / 0,6480 ; 2 → 0,8699 / 0,8878 (52 / 12 pas) |
| 8 | Colonne « comment on le vérifie » : tableau de 24 tours exigé pour toute option où le nombre de pas par tour n'est pas constant, où le nombre de tours par an diffère de 12, ou qui comporte un pas résiduel. Pour une option à tours égaux et 12 tours par an suffisent : l'identité pas_par_an = 12 × pas_par_tour posée en toutes lettres ; la formule donnant, pour le tour n, l'indice du premier pas (qui porte la date de décision), l'indice du dernier pas, le mois et l'année affichés ; le contrôle du tour 13 contre le tour 1 (même mois, année + 1). L'arithmétique commune avec le critère 7 n'est vérifiée qu'une fois ; avis de `jeu` sur la perceptibilité de toute irrégularité déclarée | `macro`, reformulé par `jeu` |
| 11 (b) | **Déclarer** : le cadre déclare la liste des instruments du socle ; tout instrument présent a un émetteur unique, définition, unité, fenêtre ; les instruments absents du socle (billets, avances) ne sont pas interdits et la fiche dit comment leur ligne s'ajoute ; pour chaque instrument absent, la fiche écrit l'identité qui s'en trouve simplifiée (sans billets : M = D et H = Res ; sans avances : la seule porte de monnaie centrale vers l'État est l'achat de titres par la banque centrale). L'incohérence v1.5 (l. 414 contre l. 995) reste un défaut à exclure | `macro`, complété par `monnaie` |
| 12 (b) | Tous les intérêts sont assis sur l'**encours d'ouverture** du pas (l'alternative « ou de clôture » est retirée : un intérêt sur l'encours de clôture dépend des flux du pas, dont lui-même, soit une résolution simultanée exclue par 12 (a)) | `monnaie` |
| 12 (c) | **Déclarer**. Le cas k = 0 (premier flux d'intérêt au taux nouveau dans le tour même de la décision, au premier pas du tour, sur l'encours d'ouverture de ce pas, à partir de la phase identifiée au 12 (d), jamais sur un pas déjà exécuté) est admis sans justification ; tout k > 0 s'exprime en tours entiers et se justifie par un mécanisme perçu (critère 5). k ne mesure que le délai décision → premier flux d'intérêt, non la transmission aux autres blocs | `macro`, reformulé par `jeu` et `monnaie` |
| 14 (a) | **Déclarer** : le cadre déclare la périodicité de versement de chaque intérêt ; le versement à chaque pas (ou tour) sur l'encours d'ouverture, sans poste d'intérêts courus, est admis ; un intérêt couru non versé a son poste ou sa ligne de capitalisation nommé. Un intérêt dû et non payé est soit rationné selon la règle de caisse, soit capitalisé par une ligne de flux nommée, jamais ajouté au principal (défauts l. 1016, 1178–1182). Une dette publique à taux variable réglée chaque pas au taux de la dernière date de décision satisfait « date de fixation » (instabilité 3) en le déclarant | `macro`, complété par `monnaie` |
| 14 (b) | Le cadre ne fixe ni le nombre de taux administrés ni leur écart (la fiche 8 décide du corridor). La matrice des flux comporte une ligne d'intérêts par instrument porteur d'intérêt présent dans la matrice des bilans, assise sur l'encours brut d'ouverture de ce seul instrument ; aucune ligne assise sur une position nette de deux instruments (défaut v2.0 : l. 1189 et 1278–1283) | `macro`, reformulé par `monnaie` |
| 14 (c) | Forme conditionnelle gardée ; le socle peut ne pas prévoir la ligne A^G. Sans A^G, le compte du Trésor ne devient jamais négatif : l'incapacité de payer suit la règle de caisse déclarée (rationnement), jamais un découvert implicite (instabilité 2 par la porte de derrière) | `macro`, complété par `monnaie` |
| 14 (d) | Le résultat de la banque centrale sur la fenêtre déclarée est la somme algébrique de ses lignes d'intérêts **exécutées** sur cette fenêtre (non des montants dus : défaut v2.0 l. 1182, 1207) ; la ligne de versement à l'État en est une fonction déclarée ; toute troncature (versement nul en cas de perte) est déclarée comme borne (critère 6), la perte restant dans E^CB, vérifiée par le double calcul de 10 (c). Un versement sur une fenêtre plus longue que le pas exige une variable d'état « résultat cumulé », comptée au 13 (a). Interdit maintenu : jamais sur le stock E^CB | `macro`, complété par `monnaie` |

Critères gardés tels quels : 1, 2, 3, 4, 5, 6 (élargi), 7 (a), 7 (c), 9, 10, 11 (a), (c), (d), 12 (a), (d), 13.

### Correspondance avec la version longue (`1ed2050`)

| Ancien | Nouveau | Ancien | Nouveau | Ancien | Nouveau |
|---|---|---|---|---|---|
| 1 | 1 | 13 | 12 (a) | 25 (B9) | 14 (a) |
| 2 | 2 (a) | 14 | 2 (b) | 26 (B10) | 14 (c) |
| 3 | 3 | 15 | 13 (a) | 27 (B11) | 14 (d) |
| 4 | 4 (a) | 16 | 2 (c) | 28 (B12) | 7 (b) |
| 5 | 5 (a) | 17 (B1) | 11 (b) | 29 (B13) | 12 (b) |
| 6 | 6 | 18 (B2) | 10 (b) | 30 (J-b) | 12 (d) |
| 7 | 7 (a) | 19 (B3) | 10 (c) | 31 (J-c) | 5 (b) |
| 8 (J-a) | 8, reformulé en mesure | 20 (B4) | 9 (b) | 32 (J-d) | 7 (c) |
| 9 | 4 (b) | 21 (B5) | 11 (c) | 33 (J-e) | 4 (c) |
| 10 | 9 (a) | 22 (B6) | 11 (d) | 34 (J-f) | 13 (b) |
| 11 | 10 (a) | 23 (B7) | 14 (b) | | |
| 12 | 11 (a) | 24 (B8) | 12 (c), variables retardées au 13 (a) | | |

Chaque ancien critère est conservé en entier, sources et lignes comprises ; seule exigence modifiée : le critère 8, passé d'exigence à mesure (décision du mainteneur du 30/09/2026).

## 3. Options

*Instruit par `macro` (expert pilote), 30/09/2026 (issue #16). Critères du § 2 lus tels que validés ; aucun n'est déplacé.*

**Découpage par question.** Le bloc est un cadre, pas un module : trois des cinq questions qu'il tranche (matrices et instruments ; tolérances et soldes ; ordre des phases et empreinte de l'état) ne dépendent pas de la durée du pas. Les options A (v1.5) et B (v2.0) répondent aux cinq questions à leur manière et sont instruites en huit rubriques chacune. Les options C, D, E ne diffèrent que sur la **question 1 (calendrier)** et sur ce qui en découle (budget par pas, variables d'état, perception) ; leurs réponses aux questions 2 à 5 forment un **socle commun « v3 proposé »** (§ 3.N), instruit une fois, avec lequel chacune se combine.

**Mesures.** Toutes exécutées par `uv run python -` le 30/09/2026, sorties citées dans le texte :
- conversions des taux, des flux et des vitesses pour n = 1, 12, 13, 52 ;
- intérêts versés dans l'année sur encours constant ;
- ratio stationnaire K/I selon la règle de conversion ;
- budget par pas et par tour pour N = 1, 4, 10 ;
- tableaux de 24 tours des options D et E, et prédicat de date de décision de E ;
- borne d'accumulation d'arrondi sur 720, 3 120 et 20 280 pas ;
- contre-épreuve numérique des sommes nulles des deux matrices, de l'égalité ΔRes vue des deux côtés, et du double calcul de E^Bk et E^CB.

Lignes d'archive relues (statut L) ; faits G2, H2, J2/K2b, K2c cités avec leur statut d'`archive/faits_mesures_G_K.md`. Contrôle de la session principale : les conversions des taux (3,9285 / 3,9280 / 3,9236 %) et le ratio K/(n·I) (14,2857 en linéaire pour tout n ; 14,1208 / 14,0840 / 14,0825 / 14,0698 en composé pour n = 4 / 12 / 13 / 52) ont été recalculés à l'identique (`python3`, 30/09/2026).

**Littérature.** Le proxy a refusé l'accès le 30/09/2026 à `bankofengland.co.uk`, `levyinstitute.org`, `ideas.repec.org`, `papers.ssrn.com`, `cepremap.fr` et `marcopassarella.it` : seuls des titres et des résumés ont été lus.
- Godley et Lavoie, *Monetary Economics*, 2007 : forme des matrices (chap. 2) ; **aucun passage sur la longueur de la période n'a pu être vérifié**.
- Nikiforos et Zezza, 2017, « Stock-Flow Consistent Macroeconomic Models: A Survey », *Journal of Economic Surveys* 31, 1204–1239 : résumé seul, muet sur la période.
- Burgess, Burrows, Godin, Kinsella et Millard, 2016, « A dynamic model of financial balances for the United Kingdom », Bank of England Staff Working Paper 614 : fréquence non vérifiée.
- Zezza et Zezza, 2020, « A Stock-Flow Consistent Quarterly Model of the Italian Economy », Levy Economics Institute Working Paper 958 : son titre établit l'existence d'un modèle stock-flux empirique **trimestriel**.

Aucun modèle stock-flux à pas mensuel ou hebdomadaire n'a été retrouvé. **La littérature retrouvée ne permet pas de conclure** à une durée de pas canonique : le pas le plus court retrouvé est le trimestre, et aucune des options C, D, E n'est plus fidèle que les autres à la littérature.

### 3.A Option A — v1.5

1. **Source exacte.** `archive/v1.5/Nations_et_Marches_v1_5.tex` :
   - § « Temps » l. 396–402 ; § « Bilans et cohérence stock-flux » l. 404–420 ; § « Ordre de résolution d'un tick » l. 422–432 ;
   - § « Règles de caisse et bornes numériques » l. 483–489 (`sec:sfc`) ;
   - bilan de la banque centrale l. 995 ; éq. `eq:ecb` l. 998–1005, contrainte E^CB/H ≥ κ (négatif admis) l. 1006 ;
   - « Précisions de la v1.2 » l. 1012 (chiffres rapportés) ; délais rapportés l. 1800–1803.
2. **Équations.** Toutes « choix de conception », sauf les identités, « dérivées » :
   - tick = une semaine (l. 399) ; mois = 4 ticks (l. 400) ; conversion unique i^(w) = (1+i)^{1/52} − 1 (l. 402) ;
   - M = C + D, H = C + Res (l. 420) ; bilan BC G + e R^FX + B^CB + L^CB + A^G = C + Res + E^CB (l. 995) ;
   - « quatre portes » de la monnaie (l. 485) ; règles de caisse sans découvert, contrainte hebdomadaire v(π^e)(M_j + ½ p_j Q_j) avec v = exp(a·min(π^e, 1)) (l. 487–488) ;
   - bornes (l. 489) : prix ×[0,7 ; 1,19] par semaine, salaires ×[0,9 ; 2] par mois, π^e ≤ 12, taux directeur ≤ 1, prime ≤ 0,3.

   La matrice des flux est affirmée « fermée » (l. 405) mais **n'existe pas sous forme de tableau**.
3. **État stationnaire impliqué.** Sans objet pour un cadre, sauf sur un point : la fenêtre « un an » y vaut soit 52 ticks (conversion) soit 12 mois × 4 = 48 ticks, et **48 ≠ 52** (l. 400 contre 402). Aucun ratio annuel n'est calculable sans lever cette ambiguïté : critère 2 (b) non satisfait.
4. **Comportement mesuré.** Non mesuré : aucune équation de la v1.5 n'a été garantie exécutée. Les chiffres de la l. 1012 (« +50 % de dépôts la première année », effondrement en 45 ans, monétisation cachée de 2,5 % du PIB par an) sont **rapportés** (R), non remesurés.
5. **Coût de calcul.** 52 pas par an, 8 étapes par pas, budget de 1 ms par pas ; coût non mesuré. La v1.7 « une dizaine de secondes pour 200 ans » est un chiffre rapporté (ADR 0001 § 3).
6. **Défauts connus.**
   - (i) 48 ≠ 52.
   - (ii) Matrice des flux absente.
   - (iii) Table des bilans (l. 414) sans A^G ni E^CB.
   - (iv) « Finance » (étape 5) placée avant « État » (étape 7).
   - (v) Décisions des joueurs en « Fin de mois » (étape 8) : un levier s'applique au tick suivant.
   - (vi) Bornes numériques absolues (l. 488–489), qui concernent l'instabilité 15.
   - (vii) Seigneuriage distribué sur le stock (l. 1012, rapporté).
   - (viii) Aucune tolérance définie.

   Instabilités 2 et 3 concernées.
7. **Identités de bilan touchées.** Au moins 20 postes. Le compte du Trésor « dépôt au Trésor M^G » (l. 415) ne dit pas chez qui il est tenu. Aucune règle ne dit quel poste est calculé comme résidu : non spécifié, donc non vérifiable.
8. **Ce que le joueur en percevrait.** Un tour de 4 ticks, mais 12 ou 13 tours par an selon la lecture ; effet d'un levier au tick suivant la décision. Délais « 6 à 12 mois » et « 12 à 18 mois » rapportés (l. 1801–1802), jamais vérifiés.

### 3.B Option B — v2.0

1. **Source exacte.**
   - `archive/v2.0/prototype/model.py` :
     - calendrier : `WEEKS`, `DECISION_WEEKS`, `PERIODS_PER_YEAR` (l. 36–38) ; `wk(r)` (l. 40–41) ;
     - grand livre : `Ledger.transfer` (l. 49–61, tolérance l. 55) ;
     - état initial : `Res` résiduel puis `L_cb` (l. 556–557) ; `E_cb` posé (l. 562) ; `AG_free` (l. 564) ;
     - date de décision : `month` (l. 607–608) ;
     - intérêts impayés ajoutés au principal (l. 1016) ; flux annuels `/ WEEKS` (l. 1021, 1203, 1212) ; `lam_ell / WEEKS` (l. 1039) ;
     - intérêts publics (l. 1172–1182) ; rémunération sur position nette (l. 1189) ; versement `seig` (l. 1207–1209) ;
     - `Res` résiduel et report sur `L_cb` (l. 1278–1283, copies l. 556–557, 1574–1575, 1631–1632) ; `E_cb` posé (l. 1633) ;
     - `P_hist[-1-13]` (l. 1292–1294) ; divisions par 13 (l. 1300, 1305) ; tolérances (l. 1460–1470).
   - `worldn.py` l. 164–166 ; `numerical_audit.py` l. 10–20.
   - Faits G2, H2, J2/K2b, K2c (§ 5) et D1 (§ 2, R).
2. **Équations.**
   - Calendrier : 52 pas, date de décision t mod 4 = 0, **13 périodes par an**.
   - Conversions : taux composée `wk` ; flux linéaires X/52 ; vitesses λ/52 ou λ/13 selon le bloc.
   - Identité de bilan bancaire écrite comme **affectation** (`Res = …`, l. 1280), puis « si Res < 0 : L_cb += −Res » (l. 1282–1283) ; `E_cb` posé (l. 562).
   - Tolérances `1e-9·max(1, montant)` (l. 55), `1e-8·max(|Y|, 1) + k·eps·Σ|opérandes|` (l. 1463–1469), `/max(1, |E_cb|)` (`numerical_audit.py` l. 16–20).
   - Versement de la BC assis sur un profit qui inclut les intérêts **dus** (l. 1182, 1207).
3. **État stationnaire impliqué.** Sans objet pour le cadre. L'année des décisions (13 × 4 = 52) et celle de la conversion (52) coïncident : c'est la seule option historique au calendrier cohérent. Mais l'état D1 n'est pas résolu (150 ans de préparation, ADR 0001 § 2).
4. **Comportement mesuré.**
   - **G2 (S+O)** : `Res` diverge de 2,44e−4 en semaine 5 (pays seul contre monde) ; `L_cb` de 8,58e−5 (×100) et 1,22e−4 (permutation) en semaine 1.
   - **H2 (S+O)** : sur 260 semaines, `L_cb`/B_close ≤ 1,449e−13 et `Res`/B_close ≤ 8,23e−15.
   - **J2/K2b (S ; O jusqu'à 920)** : `Res` franchit 1e−12 de l'échelle en semaine 910 (ratio maximal 3,30e−12) ; `L_cb` en semaine 1 154.
   - **K2c (S+O)** : arrêt en semaine 824 sous ×100 sur un paiement de −1,86e−9.
   - **Vitesse** : 308,6 ms par semaine simulée (29/09/2026, moteur entier ; ADR 0001 § 3).
5. **Coût de calcul.** 52 pas par an ; `_step_normal` de 900 lignes ; part du grand livre non isolée : non mesuré.
6. **Défauts connus.**
   - Instabilité 16 réintroduite (S+O, G2, K2c) ; instabilité 2 par `AG_free`.
   - Historiques dans l'état (≈ 70 Mo sur 72).
   - Quatre points d'écriture d'une même identité.
   - Intérêts impayés ajoutés au principal ; `E_cb` posé, qui rend le contrôle circulaire.
   - Intérêt sur position nette ; versement assis sur des intérêts dus.
   - Division par 13 en ligne ; 13 « mois » par an.
7. **Identités de bilan touchées.** Compte du Trésor **à la banque** (`led.dep["G"]`) ; pas de billets ; `Res` dérivé ; `E_cb` posé ; A^G avec une fraction gratuite. Le grand livre unique des dépôts est l'acquis à garder (ADR 0001 § 8).
8. **Ce que le joueur en percevrait.** Aucun tour ni levier n'existe. En projetant un tour sur la date de décision : 13 tours par an ; barème fiscal avec k = 0, taux directeur avec k = 1 pas. Deux dates d'effet différentes, non déclarées.

### 3.C, 3.D, 3.E — Question 1 : le calendrier

Rubriques 1 à 5 et 8 par option ; les rubriques 6 et 7 sont communes (§ 3.N). Symboles provisoires : n_a pas par an, n_m pas par tour.

| Rubrique | **C — pas mensuel unique** | **D — hebdomadaire, 13 dates de 4 semaines** | **E — hebdomadaire, mois de 4 ou 5 semaines** |
|---|---|---|---|
| 1. Source | Piste de `docs/feuille-de-route.md` § 5 ; `CONVENTIONS.md` § 6 ; littérature : trimestriel au plus fin | Forme v2.0 assumée (`model.py` l. 36–38, 607) | `CONVENTIONS.md` § 6 ; motif « 4-4-5 » proposé par `macro` ; aucune référence retrouvée |
| 2. Équations (choix de conception) | n_a = 12 ; n_m = 1 ; date de décision : tout pas ; tour n = pas n − 1 ; mois = (n−1) mod 12 + 1, année = (n−1) div 12 + 1 ; pas_par_an = 12 × 1 ; tour 13 = mois 1 de l'année 2 | n_a = 52 ; n_m = 4 ; date de décision t mod 4 = 0 ; 13 tours par an ; 13 × 4 = 52 ; « période » (t mod 52) div 4 + 1 ∈ {1..13} ; le tour 14 est la période 1 de l'année 2 | n_a = 52 ; motif (4, 4, 5) × 4 ; date de décision t mod 52 ∈ {0, 4, 8, 13, 17, 21, 26, 30, 34, 39, 43, 47} (vérifié : 24 dates sur 104 pas) ; 12 tours par an ; tour 13 : pas 52, janvier de l'année 2 |
| Tableau des tours (crit. 8 amendé) | Tours égaux, 12 par an : la formule suffit | Tableau exécuté : tours 1–13 → pas 0–51, périodes 1–13 de l'année 1 ; tours 14–26 → pas 52–103 ; tour 27 → pas 104–107, période 1 de l'année 3 | Tableau exécuté (tour ; pas ; longueur ; mois) : 1 ; 0–3 ; 4 ; janv · 2 ; 4–7 ; 4 ; févr · 3 ; 8–12 ; 5 ; mars · 4 ; 13–16 ; 4 ; avr · 5 ; 17–20 ; 4 ; mai · 6 ; 21–25 ; 5 ; juin · 7 ; 26–29 ; 4 ; juil · 8 ; 30–33 ; 4 ; août · 9 ; 34–38 ; 5 ; sept · 10 ; 39–42 ; 4 ; oct · 11 ; 43–46 ; 4 ; nov · 12 ; 47–51 ; 5 ; déc · 13 ; 52–55 ; 4 ; janv année 2 · … · 24 ; 99–103 ; 5 ; déc année 2 |
| Année du joueur = année de la conversion ? | Oui | En durée oui, en mois non : 13 tours par an, sans mois calendaire | Oui |
| 3. État stationnaire | Registre de 12 valeurs de l'indice, P_{−k} = P/(1+π̄)^{k/12} ; « un an » = 12 pas, « un mois » = 1 pas | Registre de 13 valeurs ; « un mois » = 4 pas | Registre de 12 valeurs ; « un mois » = 4 ou 5 pas : un flux « mensuel » stationnaire n'est pas constant d'un tour à l'autre |
| 4. Comportement mesuré | Non mesuré | Non mesuré en v3 ; aucun défaut calendaire relevé en G–K | Non mesuré |
| 5. Coût (crit. 4) | 4,333 ms par pays-pas (52/12) ; tour : 4,33 / 17,3 / 43,3 ms pour N = 1 / 4 / 10 ; 60 ans d'un pays : 3,12 s ; `semaines_par_pas = 52/12` ; 720 pas sur la fenêtre longue | 1 ms par pays-pas ; tour : 4 / 16 / 40 ms ; 3,12 s ; `semaines_par_pas = 1` ; 3 120 pas | 1 ms ; tour : 5 / 20 / 50 ms au plus ; 3,12 s ; `semaines_par_pas = 1` ; 3 120 pas |
| 8. Joueur (crit. 5) | Partie de 60 à 120 tours ; plus court délai : 1 tour ; tout se date au tour ; une seule date (année, mois) | 65 à 130 tours ; plus court délai : ¼ de tour ; le joueur lit « période 5 de l'année 2 », pas un mois | 60 à 120 tours ; plus court délai : ¼ ou ⅕ de tour ; tous les flux cumulés sur le tour oscillent de **+25 % / −20 %** entre un tour de 4 et un tour de 5 semaines : dents de scie sur chaque indicateur mensuel, que 7 (c) interdit de normaliser |

Toutes trois satisfont 7 (a) : n_a entier, tour en nombre entier de pas, une seule année.

### 3.N Socle commun aux options nouvelles — questions 2 à 5

Indépendant de la durée du pas, il s'applique à C, D ou E. Statut : identités **dérivées** ; règles de conversion, liste des instruments et phases : **choix de conception**.

#### Q2 — Conversions (critères 7 (b) et 14)

Une seule équation `eq:moteur-conversion-taux` déclare la règle pour les trois natures.

| Nature | Règle linéaire x/n_a | Règle composée (1+x)^{1/n_a} − 1 |
|---|---|---|
| Taux i = 4 % : **intérêts versés dans l'année**, encours constant, intérêt payé à chaque pas sur l'encours d'ouverture (forme du 14 (a)) | **4,0000 %** pour n = 12, 13, 52 | 3,9285 % (12), 3,9280 % (13), 3,9236 % (52) : dépend de n |
| Taux i = 4 % : rendement annuel d'un agent qui **replace** chaque intérêt | 4,0742 % (12), 4,0747 % (13), 4,0795 % (52) : dépend de n | **4,0000 %** pour tout n |
| Flux annuel X | total annuel = X exactement pour tout n | sans objet |
| Vitesse λ : fraction de l'écart résorbée en un an | λ = 0,5 : 0,3999 (12), 0,3949 (52) ; λ = 0,1 : 0,0955 / 0,0952 ; λ = 1 : 0,6480 / 0,6357 ; λ = 2 : 0,8878 / 0,8699 : dépend de n | 0,5000 pour tout n (λ < 1 seulement) |
| **Ratio stationnaire** K_t/(n·I_t), g = 2 %, δ = 5 % (crit. 2 (c)) | **14,2857 = 1/(g+δ) pour tout n** | 14,2857 (1), 14,1208 (4), 14,0840 (12), 14,0825 (13), 14,0698 (52) : dépend de n |

**Lecture de `macro`.**
- Le chiffre de `monnaie` (critère 7 (b) : 4,0000 % contre 4,0795 %) vaut **pour un intérêt capitalisé**. Or le socle verse les intérêts à chaque pas sur l'encours d'ouverture et interdit toute capitalisation silencieuse (12 (b), 14 (a)).
- Pour un intérêt **versé**, c'est la règle linéaire qui rend l'année invariante (iX exactement). C'est elle aussi qui rend les ratios stationnaires **indépendants de n_a** (2 (c)), puisque toute grandeur par pas y est proportionnelle à 1/n_a. La composée laisse une dépendance de 1,5 % sur K/I entre n = 1 et n = 52.
- **Proposition** : une règle unique, **linéaire**, pour les trois natures. Le cadre déclare, en les chiffrant, les deux grandeurs qui dépendent alors de n_a : la fraction annuelle résorbée par une vitesse, et le rendement d'un replacement pas à pas (4,07–4,08 % pour 4 %).
- L'autre lecture (composée pour les taux, linéaire pour les flux, au choix pour les vitesses) est à décrire au § 6 par `monnaie` : **point frontière, le mainteneur tranche**.

Seconde déclaration (2 (c), 7 (c)). Le test zéro définit le ratio « stock au PIB annuel » comme **stock d'ouverture / (n_a × flux du pas)**, la restitution au tour comme stock de clôture / Σ des 12 tours. Les deux diffèrent par un facteur dû à la croissance dans l'année : 14,2857 contre 14,1552 (12 pas) ou 14,1461 (52 pas), soit 0,9 à 1,0 % pour g = 2 %. Le cadre publie ce facteur.

#### Q3 — Matrices et instruments (critères 1, 10, 11 et 14)

**Liste déclarée des instruments du socle (11 (b) amendé).** Six instruments financiers, chacun avec un émetteur unique, et deux actifs réels sans émetteur (K, IN). Sont absents mais non interdits :
- les billets C (sans billets : **M = D, H = Res**) ;
- les avances A^G : sans elles, la seule porte de monnaie centrale vers l'État est l'**achat de titres par la banque centrale**, et le compte du Trésor ne devient jamais négatif ;
- le crédit aux ménages, les actions et l'immobilier (J6) ;
- le reste du monde (J5 : une colonne, sans réécriture).

| Instrument | Émetteur (−) | Détenteurs (+) | Unité | Fenêtre | Intérêt (encours d'ouverture, versé chaque pas, taux annuel converti une fois) |
|---|---|---|---|---|---|
| D dépôts | banque | ménages D_H, entreprises D_F | u.m. | ouverture | i_D (fiche 7) |
| L crédits | entreprises | banque | u.m. | ouverture | i_L (fiche 7) |
| B titres publics | État | ménages B_H, banque B_Bk, BC B_CB | u.m. | ouverture | i_B, taux de la dernière date de décision, déclaré comme date de fixation (instabilité 3 traitée) |
| Res réserves | banque centrale | banque | u.m. | ouverture | i_res (fiche 8) |
| L^CB refinancement | banque | banque centrale | u.m. | ouverture | i_CB (fiche 8) |
| M^G compte du Trésor | **banque centrale** (proposition, voir plus bas) | État | u.m. | ouverture | aucun (déclaré) |
| K, IN capital fixe et stocks | actifs réels, sans émetteur | entreprises | u.m. | ouverture | sans objet |

**Matrice des bilans** (stocks à l'ouverture du pas, u.m. ; + actif, − passif ; D = D_H + D_F, B = B_H + B_Bk + B_CB) :

| Poste | Ménages | Entreprises | Banque | Banque centrale | État | Σ ligne |
|---|---|---|---|---|---|---|
| Capital fixe p_K K | | +K | | | | +K |
| Stocks p·IN | | +IN | | | | +IN |
| Dépôts | +D_H | +D_F | −D | | | 0 |
| Crédits | | −L | +L | | | 0 |
| Titres publics | +B_H | | +B_Bk | +B_CB | −B | 0 |
| Réserves | | | +Res | −Res | | 0 |
| Refinancement | | | −L^CB | +L^CB | | 0 |
| Compte du Trésor | | | | −M^G | +M^G | 0 |
| Valeur nette | −V_H | −V_F | −E^Bk | −E^CB | −V_G | −(K + IN) |
| **Σ colonne** | 0 | 0 | 0 | 0 | 0 | 0 |

Valeurs nettes : V_H = D_H + B_H ; V_F = K + IN + D_F − L ; E^Bk = L + B_Bk + Res − D − L^CB ; E^CB = B_CB + L^CB − Res − M^G ; V_G = M^G − B. Leur somme vaut K + IN. Contre-épreuve numérique : toutes les colonnes et toutes les lignes financières à 0,0 ; Σ V = 860 = K + IN.

**Matrice des flux de transactions** (u.m. par pas ; + reçu, − versé ; entreprises en deux sous-colonnes, courant et capital ; la variation d'un actif détenu compte −, celle d'un passif émis compte +). **Les colonnes ΔM et ΔH sont écrites sous la lecture (i), compte du Trésor à la banque centrale.** La ligne 19 est scindée : **19a**, marché primaire (émission ou rachat par l'État) ; **19b**, opérations de la banque centrale sur le marché secondaire (exposants p et s ; ΔB_H = ΔB_H^p − ΔB_H^s, ΔB_Bk = ΔB_Bk^p − ΔB_Bk^s, ΔB_CB = ΔB_CB^p + ΔB_H^s + ΔB_Bk^s) — constats 1 et 3 de `monnaie`, acceptés par `macro` :

| Ligne | Ménages | Entr. courant | Entr. capital | Banque | BC | État | Σ | ΔM | ΔH |
|---|---|---|---|---|---|---|---|---|---|
| 1 Consommation C | −C | +C | | | | | 0 | 0 | 0 |
| 2 Dépense publique G | | +G | | | | −G | 0 | + | + |
| 3 Investissement I | | +I | −I | | | | 0 | 0 | 0 |
| 4 Variation des stocks ΔIN | | +ΔIN | −ΔIN | | | | 0 | 0 | 0 |
| 5 Salaires WB | +WB | −WB | | | | | 0 | 0 | 0 |
| 6 Transferts Tr | +Tr | | | | | −Tr | 0 | + | + |
| 7 Impôts T | −T_H | −T_F | | | | +T | 0 | − | − |
| 8 Amortissement δ p_K K | | −δK | +δK | | | | 0 | 0 | 0 |
| 9 Intérêts sur crédits i_L L | | −i_L L | | +i_L L | | | 0 | − | 0 |
| 10 Intérêts sur dépôts i_D D | +i_D D_H | +i_D D_F | | −i_D D | | | 0 | + | 0 |
| 11 Intérêts sur titres i_B B | +i_B B_H | | | +i_B B_Bk | +i_B B_CB | −i_B B | 0 | + (part B_H) | + (parts B_H, B_Bk) |
| 12 Intérêts sur réserves i_res Res | | | | +i_res Res | −i_res Res | | 0 | 0 | + |
| 13 Intérêts sur refinancement i_CB L^CB | | | | −i_CB L^CB | +i_CB L^CB | | 0 | 0 | − |
| 14 Dividendes des entreprises Div_F | +Div_F | −Div_F | | | | | 0 | 0 | 0 |
| 15 Dividendes de la banque Div_Bk | +Div_Bk | | | −Div_Bk | | | 0 | + | 0 |
| 16 Versement du résultat de la BC Π^CB | | | | | −Π^CB | +Π^CB | 0 | 0 | 0 |
| 17 Δ Dépôts | −ΔD_H | | −ΔD_F | +ΔD | | | 0 | | |
| 18 Δ Crédits | | | +ΔL | −ΔL | | | 0 | + | 0 |
| 19a Émission ou rachat primaire | −ΔB_H^p | | | −ΔB_Bk^p | −ΔB_CB^p | +ΔB | 0 | − (part B_H^p) | − (parts B_H^p, B_Bk^p) ; **0** (part B_CB^p : M^G et B_CB montent dans le même bilan) |
| 19b Achats ou ventes de la BC, marché secondaire | +ΔB_H^s | | | +ΔB_Bk^s | −(ΔB_H^s + ΔB_Bk^s) | | 0 | + (part ménages) ; 0 (part banque) | + (les deux parts) |
| 20 Δ Réserves | | | | −ΔRes | +ΔRes | | 0 | | |
| 21 Δ Refinancement | | | | +ΔL^CB | −ΔL^CB | | 0 | 0 | + |
| 22 Δ Compte du Trésor | | | | | +ΔM^G | −ΔM^G | 0 | | |
| **Σ colonne** | 0 | 0 | 0 | 0 | 0 | 0 | | | |

Contraintes budgétaires (sommes de colonnes) :
- ménages : ΔD_H = WB + Tr + i_D D_H + i_B B_H + Div_F + Div_Bk − C − T_H − ΔB_H ;
- entreprises : ΔD_F = (C + G + I + ΔIN − WB − T_F − i_L L − Div_F − δK + i_D D_F) + (δK − I − ΔIN) + ΔL ;
- banque : ΔRes = (i_L L + i_B B_Bk + i_res Res − i_D D − i_CB L^CB − Div_Bk) + ΔD − ΔL − ΔB_Bk + ΔL^CB ;
- banque centrale : ΔRes = (i_B B_CB + i_CB L^CB − i_res Res − Π^CB) + ΔB_CB + ΔL^CB − ΔM^G ;
- État : ΔM^G = T + Π^CB − G − Tr − i_B B + ΔB.

Contre-épreuve numérique :
- les six colonnes sont à 0,0 ;
- ΔRes vu de la banque = ΔRes vu de la BC = 7,226 ;
- E^Bk et E^CB de clôture sont identiques par le stock et par les flux (108,71 ; 15,0) ;
- ΔM = ΔD = 17,016, recomposé par les portes = 17,016 ; ΔH = ΔRes = 9,226, recomposé par les portes = 9,226, la part B_CB de 19a comptant 0 (M^G et B_CB montent ensemble de 1,0). Contre-épreuve refaite par `macro` sur la matrice scindée (souscription primaire de la BC 1,0 ; achats secondaires 1,5 aux ménages et 0,5 à la banque) : Σ 19a = Σ 19b = 0,0 ; colonnes à 0,0 ; E^Bk 108,71 et E^CB 15,0 par le stock et par les flux.

**Portes de la monnaie (11 (c)), liste exhaustive.**
- ΔM = ΔD varie par :
  - la ligne 18 (crédit net) ;
  - les lignes 2, 6, 7, 11 (part B_H) et 19a (part B_H^p) : paiements nets de l'État aux ménages et aux entreprises ;
  - les lignes 9, 10 et 15 : intérêts et dividendes nets de la banque ;
  - la ligne 19b, part ménages.
- ΔH = ΔRes varie par :
  - la ligne 21 ;
  - la ligne 19a (parts B_H^p et B_Bk^p émis ; la part B_CB^p compte 0) ;
  - la ligne 19b (achats de la BC, parts ménages et banque) ;
  - les lignes 12 et 13 ;
  - les lignes 2, 6, 7 et 11 (parts B_H et B_Bk) : tout paiement entre M^G et un compte tenu à la banque.
- Toute autre ligne est un transfert entre détenteurs. Le test « ΔM et ΔH recalculés depuis la matrice = variation des postes » est le contrôle du script #19.

**Aucun solde résiduel (10).**
- Chaque instrument est tenu **une fois** dans le noyau, comme position (détenteur, émetteur) : la ligne de la matrice des bilans somme à zéro par construction, sans tolérance.
- Chaque poste de clôture vaut l'ouverture plus la somme des lignes de flux nommées qui le touchent, appliquées par le noyau.
- ΔL^CB n'a qu'une source, la ligne 21 : un **flux décidé** en phase 8 par le bloc banque, dont la règle relève de la fiche 7. Aucune règle « si Res < 0 ».
- E^Bk et E^CB sont calculés **deux fois** (par le stock et par les flux) ; l'écart entre les deux est l'identité vérifiée.

**Compte du Trésor (11 (d)) : deux lectures.**
- (i) **À la banque centrale** (proposition de `macro`). Chaque impôt draine des réserves et chaque dépense en crée ; la ligne 21 est vivante dès le socle, et le taux directeur atteint le coût de la banque par un flux visible. C'est un mécanisme perçu par le joueur, qui justifie la ligne au sens du critère 6.
- (ii) **À la banque** (forme v2.0). Aucun paiement de l'État ne touche Res ; la ligne 21 serait morte au socle.

`macro` recommande (i) ; **`monnaie` se prononce au § 6**.

**Règles de caisse.**
- Moyens de paiement : dépôt (ménages, entreprises), réserves (banque), compte du Trésor (État).
- Un payeur ne paie pas plus que son moyen de paiement : la part non payée est une **ligne de flux nommée** du bloc (rationnement déclaré ou capitalisation nommée), jamais un découvert ni un ajout au principal.
- L'ordre de priorité des paiements est déclaré par chaque fiche de bloc.
- Le cadre impose que le crédit (phase 3) précède les règlements.
- **Découvert intra-pas déclaré** (constat 4 de `monnaie`, accepté). La banque règle en réserves les impôts (phase 6), les souscriptions (phase 7) et i_CB L^CB (phase 8 (a)) avant le refinancement (8 (c)) : Res peut donc être **négatif entre les phases** d'un même pas. La contrainte Res ≥ 0 est vérifiée **à la clôture** (phase 9), après 8 (c). Le refinancement (ligne 21) est un flux décidé qui couvre au moins la position négative, au taux i_CB, en phase 8 (c). Ce n'est pas la règle v2.0 (l. 1282–1283), qui corrigeait un solde : ici la ligne, le taux et la phase sont nommés, et la position négative intra-pas est un état déclaré, non un poste ajusté.
- **Encaisse de l'État et phase de l'émission** : point ouvert à deux positions (constat 5 de `monnaie`), voir le § 6.4 et le § 5, lecture (f).

#### Q4 — Tolérances et échelle (critère 9)

**Forme unique.** |résidu| ≤ ε × S, où S est la **somme des valeurs absolues de tous les postes du bilan contrôlé** :
- banque : L + B_Bk + Res + D + L^CB + |E^Bk| ;
- BC : B_CB + L^CB + Res + M^G + |E^CB|.

**Contrôles de la forme.**
- Sous ×100 : le ratio passe de 0 à 0 sur un bilan de 1,34e7 puis 1,34e9.
- Sous E^CB = 100, 0, −50 : S vaut 2 400, 2 400, 2 500, contre `max(1, |E_cb|)` = 100, 1, 50 en v2.0.

**Deux identités, vérifiées à la fin de chaque phase.**
- (a) **Par pas** : au plus 30 opérandes ; borne (n−1)·eps·S ≈ 6,7e−15 S ; résidu observé ≤ 2,6e−16 S sur 200 termes. D'où **ε = 1e−12**, avec une marge supérieure à 100.
- (b) **Cumulée** (valeur nette par les flux depuis t = 0 contre valeur nette par le stock) :
  - pire cas 30·n_pas·eps·S = 4,8e−12 S (720 pas) et 2,1e−11 S (3 120 pas), **au-dessus de 1e−12** : le pire cas n'est pas le critère ;
  - mesuré (5 postes, 30 flux par pas, S ≈ 1e7, 20 graines) : résidu maximal 3,3e−15 S (720 pas) et 8,3e−15 S (3 120 pas) selon `macro`, 3,3e−15 et 6,4e−15 selon `monnaie` ;
  - **ε_V = 1e−12 tient par la mesure, marge ≥ 100 sur 60 ans pour les trois options** ; le test J2 vérifie l'accumulation réelle sur la fenêtre longue (constat 6 de `monnaie`, accepté) ;
  - le fait J2 venait d'une compensation (Res recalculé par différence), mécanisme absent ici.

Aucune tolérance sur un flux, aucune constante absolue, aucun `max(1, ·)`.

#### Q5 — Ordre des phases et empreinte de l'état (critères 12 et 13)

| Phase | Contenu | Écrivent | Lisent (ouverture ou phases antérieures) | Lignes de flux |
|---|---|---|---|---|
| 0 Ouverture | indice t ; prédicat date de décision (de t seul) | moteur | clôture t−1 | — |
| 1 Décision (si date de décision) | lecture des **leviers** ; salaires ; anticipations ; indice des prix et glissement (registre) ; règle de taux | leviers, travail, banque centrale, prix | ouverture, registre | — |
| 2 Plans | production visée, demande de travail, budget de consommation, investissement visé, dépense publique du pas | production, ménages, investissement, finances publiques | 1 | — |
| 3 Crédit | demande et offre | investissement, banque | 2 | 18 |
| 4 Production et travail | emploi, production, stocks ; salaires | production, travail | 2, 3 | 5 |
| 5 Marché des biens | ventes C, G, I ; prix du pas ; variation des stocks | prix, production | 2, 4 | 1, 2, 3, 4 |
| 6 Revenus et impôts | intérêts sur L, D, B ; impôts ; transferts ; dividendes ; amortissement | finances publiques, banque, investissement, ménages | ouverture, 1, 5 | 6–11, 14, 15 |
| 7 Titres publics | émission ou rachat ; souscriptions ; achats décidés de la BC | finances publiques, ménages, banque, banque centrale | 6 | 19 |
| 8 Monnaie centrale | (a) intérêts sur Res et L^CB ; (b) versement du résultat de la BC (résultat du tour, lignes exécutées) ; (c) position de réserves après tous les règlements → refinancement décidé | banque centrale, banque | tout ce qui précède | 12, 13, 16, puis 21 |
| 9 Clôture | identités par pas et cumulées ; double calcul de E^Bk, E^CB ; mise à jour du registre ; t + 1 | noyau, moteur | tout | — |

**Contreparties de règlement.** Les lignes 17, 20 et 22 ne sont pas des flux décidés : ce sont les contreparties de règlement des autres lignes, appliquées par le noyau.

**Dépendances.** La matrice de dépendance est **triangulaire**. Aucune ligne touchant Res n'est exécutée après 8 (c), et les intérêts publics (phase 6) précèdent le refinancement. Res ≥ 0 est une identité de clôture, non de phase (constat 4).

**Dates d'effet (12 (c), 12 (d)).** Un levier saisi au tour n est lu en phase 1 du premier pas du tour, avant tout flux ; l'ordre de saisie est sans effet.
- Taux directeur → intérêts BC (phase 8) du même pas : **k = 0**.
- Taux d'imposition → impôts (phase 6) : délai 0.
- Dépense publique → achats (phase 5) : délai 0, contrepartie visible le même tour.

**Variables d'état imposées par le calendrier (13).**
- L'indice t.
- Un registre de l'indice des prix aux 12 (C, E) ou 13 (D) dernières dates de décision, **imposé** (la règle de taux lit le glissement annuel, fiche 8 ; constat 7 de `monnaie`, accepté), de longueur fixe, valeur stationnaire P/(1+π̄)^{k/12}.
- Le résultat cumulé de la BC sur le tour : 0 variable sous C, 1 sous D et E.

Total : C, 1 + 12 = 13 ; D, 1 + 13 + 1 = 15 ; E, 1 + 12 + 1 = 14. Dans les trois cas, la date de décision se déduit de t seul et la frontière de tour coïncide avec une frontière de pas.

**Décompte de simplicité (critère 6).**

| Élément du cadre | A v1.5 | B v2.0 | C | D | E |
|---|---|---|---|---|---|
| Paramètres | 52, 4, 1/52 ; bornes numériques | WEEKS, DECISION_WEEKS, 13 ; 1e−9, 1e−8, 64·eps… | n_a = 12, n_m = 1, ε, ε_V (4) | 52, 4, ε, ε_V (4) | 52, motif (12 entiers), ε, ε_V |
| Bornes du cadre | 6 (l. 489) | `max(1, ·)` × 3 | **0** | 0 | 0 |
| Postes | ≥ 20 | ≈ 14 | 6 + 2 réels | idem | idem |
| Lignes de flux | non tabulées | non tabulées | 22 | 22 | 22 |
| Phases | 8 | 10 sections | 9 | 9 | 9 |
| Variables d'état calendaires | non spécifiées | historiques | 13 | 15 | 14 |
| Dates de décision / mois calendaires | 12 ou 13 (ambigu) | 13 | 12 = 12 | 13 ≠ 12 | 12 = 12 |
| Pas par an | 52 | 52 | 12 | 52 | 52 |

**Rubriques 6 et 7 communes à C, D, E.** Aucune instabilité connue n'est réintroduite : la 16 est exclue par Q4, les 2 et 3 par la liste d'instruments et la date de fixation, la 15 par l'absence de borne. Défauts propres :
- E : dents de scie 4/5 sur les flux mensuels ;
- D : 13 tours par an ;
- C : perte de la granularité infra-mensuelle.

Les cinq bilans sont couverts par les deux matrices, sans solde résiduel, avec la valeur nette calculée deux fois.

## 4. Tableau comparatif

Renvois : 3.A-k, 3.B-k = rubrique k ; 3.X-Q1 = colonne de l'option X au tableau calendaire ; 3.N-Qk = question k du socle commun.

| Critère | A. v1.5 | B. v2.0 | C. mensuel | D. 13 × 4 | E. 4/5 |
|---|---|---|---|---|---|
| 1 Cohérence stock-flux | non : matrice absente (3.A-2, 6) | partielle : Res résiduel (3.B-2, 6) | oui, vérifié (3.N-Q3) | idem | idem |
| 2 État stationnaire indépendant du pas | non : 48 ≠ 52 (3.A-3) | non : D1 préparé (3.B-3) | oui, exact avec la règle linéaire (3.N-Q2) | oui | oui, flux mensuel non constant (3.E) |
| 3 Stabilité | 15 ; 2, 3 (3.A-6) | 16 réintroduite (S+O), 2 (3.B-6) | aucune (3.N) | aucune | aucune |
| 4 Coût | 1 ms par pas, non mesuré (3.A-5) | 308,6 ms par semaine (3.B-4) | 4,33 ms par pas ; 43 ms par tour à 10 pays (3.C-Q1) | 1 ms ; 40 ms | 1 ms ; 50 ms |
| 5 Lisibilité | effet au tick suivant ; tours ambigus (3.A-8) | deux dates d'effet non déclarées (3.B-8) | tout au tour, k = 0 (3.N-Q5) | 13 tours sans mois (3.D-Q1) | dents de scie 4/5 (3.E-Q1) |
| 6 Simplicité | ≥ 20 postes, 6 bornes | historiques, 3 `max(1,·)` | **le plus simple** : 4 paramètres, 0 borne, 13 variables | 13 tours, 15 variables | motif de 12 entiers, 14 variables |
| 7 Calendrier et conversions | (a) non ; (b) composée seule ; (c) non défini | (a) division par 13 ; (b) trois règles dispersées | (a) oui ; (b) règle unique déclarée ; (c) tour = pas | (a), (b) oui ; (c) « un an » = 13 tours | (a), (b) oui ; (c) flux mensuel non comparable |
| 8 Rapport pas / tour | 4 ticks ; 12 ou 13 tours | 4 ; 13 | 1 ; 12 ; formule | 4 ; 13 ; tableau | 4 ou 5 ; 12 ; tableau |
| 9 Tolérances | aucune (3.A-6) | absolues (3.B-2, 4) | ε = 1e−12 × S ; marge ≥ 100 par la mesure (3.N-Q4) | idem | idem |
| 10 Aucun solde résiduel | non spécifié | non (l. 1278–1283, 562, 1633) | oui (3.N-Q3) | idem | idem |
| 11 Matrices, instruments, portes, Trésor | sans matrice ; A^G, E^CB omis ; Trésor ambigu | Trésor à la banque ; A^G gratuit | 6 instruments financiers ; portes listées ; Trésor à la BC proposé (3.N-Q3) | idem | idem |
| 12 Ordre des phases | Finance avant État ; décisions en fin de mois | k = 0 (impôts), 1 pas (taux) | 9 phases triangulaires ; k = 0 (3.N-Q5) | idem | idem |
| 13 Empreinte de l'état | non spécifiée | historiques dans l'état | 13 variables | 15 | 14 |
| 14 Instruments porteurs d'intérêt | coupon figé prévu ; avances | intérêts dus capitalisés ; position nette ; versement sur dus | iX exact par an avec la règle linéaire (3.N-Q2, Q3) | idem | idem |

## 5. Avis de l'expert pilote

*`macro`, 30/09/2026.*

**Recommandation : option C** (pas mensuel unique : 12 pas par an, décision à chaque pas), **combinée au socle commun § 3.N** : règle de conversion linéaire unique, six instruments financiers et deux actifs réels, les deux matrices ci-dessus, tolérance ε = 1e−12 × échelle, neuf phases, compte du Trésor à la banque centrale. Classement : C > E > D > B > A.

Critère par critère :
- **1, 10, 11, 14** : C, D, E à égalité ; A et B écartés.
- **2** : indépendance de n_a exacte avec la règle linéaire.
- **3** : B réintroduit l'instabilité 16.
- **4** : non discriminant (52 ms par pays-an). C donne 4,33 ms par pas aux blocs, soit une marge quatre fois plus large, et 720 pas au lieu de 3 120 sur 60 ans. (L'argument d'une accumulation d'arrondi « six fois plus faible » tombe avec le constat 6 : la marge se mesure, elle est ≥ 100 pour les trois options.)
- **5** : C est la seule option où tout ce que le joueur lit est ce que le moteur calcule (pas = tour) ; D impose 13 tours sans mois, E des dents de scie 4/5.
- **6** (règle d'arbitrage) : à exigences comptables égales, C a le moins de paramètres, de variables d'état et de pas, et aucune irrégularité. D et E n'ajoutent aucune identité vérifiable ; leur dynamique infra-mensuelle n'est perçue que si un bloc l'exploite, ce qu'aucune fiche n'a demandé.
- **7, 8** : C satisfait 7 (a) trivialement et 8 sans tableau.
- **9, 12, 13** : C a la marge d'arrondi la plus large et le moins de variables.

**Réserves et conditions, seuils écrits avant l'essai.**
1. J2, identités : |résidu| ≤ 1e−12 × S à la fin de chaque phase, par pas et en cumul, sur 720 pas sans choc ; le pire cas théorique (30·n·eps) dépasse ε_V dès 720 pas et n'est pas le critère, c'est l'accumulation mesurée qui l'est ; toute violation est un défaut, jamais un motif d'élargir ε.
2. J2, invariance d'unité : sous ×100, résidu/S ≤ 1e−12, et les champs économiques diffèrent de moins de 1e−10 en relatif.
3. J2, budget du noyau seul : ≤ 0,5 ms par pas mensuel sur la plateforme de référence (`test_budget.py`, `semaines_par_pas = 52/12`).
4. J3, état stationnaire : les ratios du script d'`outils/` égalent ceux du moteur à t = 0 à 1e−9 près ; leur dérive sur 60 ans reste dans les bandes O1 ; le facteur vers le ratio « 12 tours cumulés » (0,9 % pour g = 2 %) est publié.
5. Fidélité : si une fiche (J3, J6) établit par un fait qu'un mécanisme exige une dynamique infra-mensuelle, le choix se rouvre par une décision M-m citant M22. n_a et n_m restent des **paramètres déclarés** (pas des drapeaux de mode).

**Lectures possibles, à trancher par le mainteneur.**
- (a) **Conversion** : règle linéaire unique (`macro`) contre composée pour les taux (`monnaie`).
- (b) **Compte du Trésor** : à la banque centrale (ligne 21 vivante) contre à la banque (ligne 21 morte).
- (c) **Délai du taux** : k = 0 (recommandé ; la v2.0 avait k = 1 pas pour le taux).
- (d) **Versement du résultat de la BC** : chaque tour sans troncature (recommandé : une perte est un versement négatif) contre versement des seuls résultats positifs (borne à déclarer, fiche 8).
- (e) **Ratio stationnaire** : stock / (n_a × flux du pas) pour le test zéro (recommandé), stock / Σ 12 tours pour la restitution ; le facteur entre les deux est publié.
- (f) **Phase de l'émission de titres publics** (constat 5 de `monnaie`). Les deux positions exigent une encaisse M^G résolue ; elles diffèrent par sa taille et par la date du rationnement.

| | (α) `macro` : émission en phase 7, après les règlements | (β) `monnaie` : émission en phase 3, avec le crédit |
|---|---|---|
| Ce qu'émet l'État | le **besoin réalisé** du pas : ΔB = G + Tr + i_B B − T − Π^CB + (M^G* − M^G d'ouverture) | un **besoin planifié** : ΔB = G^plan + Tr^plan + i_B B − T^plan + (M^G* − M^G d'ouverture), T^plan étant une variable (par ex. les impôts du pas précédent) |
| Triangularité | intacte : la phase 7 lit les phases 5 et 6 | intacte : la phase 3 lit les plans de la phase 2 ; souscriptions décidées sur les plans |
| État stationnaire de M^G | M^G* couvre les paiements bruts d'un pas avant les impôts, au plus (G + Tr + i_B B)/n_a ; M^G de clôture = M^G* à chaque pas ; sous C, environ **un mois de dépenses publiques** | M^G* réduit à la couverture de G plus l'écart T − T^plan ; M^G de clôture **non constant**, corrigé à l'émission suivante ; sous C, une fraction de mois |
| Simplicité (critère 6) | 1 stock résolu, aucune variable de plan ; 9 phases | 1 stock résolu **plus** T^plan (et Π^plan), soit une variable d'état ou une règle de prévision de plus ; **8 phases** |
| Ce que voit le joueur | un placement raté laisse M^G sous M^G* ; le rationnement de la dépense frappe le **tour suivant** : signal précurseur d'un tour | un placement raté rationne la dépense **le tour même** : signal et effet simultanés |
| Réserves intra-pas | l'État injecte avant de drainer : Res positif ou faiblement négatif entre les phases | l'émission draine avant les injections : Res plus souvent négatif entre les phases (couvert par le constat 4) |

`macro` préfère (α) : une variable de moins et un M^G exactement stationnaire, forme que le script de J1 (M19) calcule sans simulation. `monnaie` préfère (β) : aucune encaisse résiduelle à justifier, rationnement immédiat. À exigences comptables égales, le principe de simplicité penche pour (α) ; la lisibilité peut peser pour (β). Sous (β), les phases deviennent : 0 Ouverture ; 1 Décision ; 2 Plans (plus T^plan) ; 3 Crédit et financement public (lignes 18, 19a, 19b) ; 4 Production et travail ; 5 Marché des biens ; 6 Revenus et impôts ; 7 Monnaie centrale (12, 13, 16, puis 21) ; 8 Clôture. Les dates d'effet sont inchangées.

**Ce que C coûte en fidélité.** Aucune dynamique infra-mensuelle : la contrainte de caisse hebdomadaire de la v1.5 (l. 488), les marchés hebdomadaires ou une ruée bancaire en jours (J6) ne sont représentables qu'au mois, et le plus court délai du modèle est un tour. Au regard de la littérature retrouvée (trimestrielle au plus fin), C ne coûte rien. Au regard de la v1.5 et de la v2.0, il abandonne une granularité qu'aucun fait mesuré de G à K n'a exploitée : tous les verdicts y portent sur des fenêtres de 260 semaines et plus, et la décision y est déjà mensuelle.

## 6. Avis de l'expert consulté (sujets frontière)

*`monnaie`, 30/09/2026 (issue #16), sur la fiche à la tête `758273a`. Mesures par `uv run python -` le 30/09/2026.*

### 6.1 Conversion (lecture (a))

**Chiffres de `macro` reproduits à l'identique.**
- Intérêts versés dans l'année :
  - en linéaire, 4,0000 % pour n = 1, 4, 12, 13, 52 ;
  - en composé, 3,9414 / 3,9285 / 3,9280 / 3,9236 % (n = 4, 12, 13, 52).
- Rendement d'un agent qui replace chaque intérêt :
  - en linéaire, 4,0742 / 4,0747 / 4,0795 % (n = 12, 13, 52) ;
  - en composé, 4,0000 % pour tout n.
- K/(n·I), avec g = 2 % et δ = 5 % :
  - en linéaire, 14,2857 pour tout n ;
  - en composé, 14,1208 / 14,0840 / 14,0825 / 14,0698.

Une « composée » pour un taux de sortie (amortissement) admet deux écritures, 1 − (1 − δ)^{1/n} ou (1+δ)^{1/n} − 1 ; la seconde donne 14,5052. C'est un argument de plus contre la composée : deux formules pour une même nature.

**Lecture.** Le critère B12 raisonnait sur un intérêt **capitalisé**. Ce n'est pas le cas du socle pour les crédits, les titres et le refinancement : l'intérêt y est payé depuis un dépôt ou des réserves (14 (a)). Pour ces instruments, `macro` a raison.

**Nuance à déclarer.** Pour les **dépôts** et les **réserves**, l'intérêt est crédité dans l'instrument lui-même : un encours laissé en place se capitalise par construction. Sous la règle linéaire, son rendement annuel effectif est de 4,0742 % (12 pas) ou 4,0795 % (52 pas) pour 4 % affiché. L'écart est imperceptible et ne touche aucun état stationnaire annuel.

**Avis : ralliement à la règle linéaire unique pour les trois natures**, à trois conditions déclarées dans `eq:moteur-conversion-taux` ou à côté :
1. le tableau Q2 tel quel, avec les deux grandeurs dépendantes de n_a chiffrées (le replacement est automatique pour D et Res) ;
2. un **taux réel annuel** restitué et testé (bande O1) défini par r = i − π, exactement comme le fait le moteur : la formule de Fisher exacte n'est pas celle du moteur et ne doit pas être celle du test ;
3. une vitesse λ ≥ 1 par an n'a pas d'équivalent composé : la linéaire est la seule règle qui admette toute vitesse. La dépendance de la transition à n_a est admise, puisqu'elle ne change pas l'état d'arrivée.

Aucun désaccord résiduel avec `macro`.

### 6.2 Compte du Trésor (lecture (b))

**Avis : à la banque centrale (i)**, avec `macro`.
- C'est la seule lecture où le coût du refinancement atteint la banque par un flux visible dès le socle : la ligne 21 est vivante et le taux directeur a une assiette.
- Sans A^G, la monétisation est visible (achat de titres par la BC), ce qui rend lisible la dominance budgétaire (Sargent et Wallace, 1981).
- Coût : l'État tient une encaisse M^G positive (voir 6.4, constat 5).

Les colonnes ΔM/ΔH de la matrice des flux sont écrites sous cette lecture : la fiche doit le dire.

### 6.3 Versement du résultat de la BC (lecture (d))

**Avis : chaque tour, sans troncature** (une perte est un versement négatif), avec `macro`.
- E^CB reste égal à sa valeur initiale résolue : aucune borne, et le double calcul est trivial.
- Le résultat est la somme des lignes exécutées 12, 13 et de la part B_CB de la ligne 11. Sous C, aucune variable « résultat cumulé » n'est nécessaire.
- Un versement négatif est un paiement de M^G vers E^CB, soumis à la règle de caisse de l'État : à déclarer.
- La troncature (borne, avec une règle de recapitalisation) est réservée à J6, par une décision citant celle-ci. Aucune source vérifiée ne tranche entre les deux pour un jeu.

### 6.4 Relecture des matrices, des tolérances et des phases

**Contre-épreuve exécutée.**
- ΔRes vu de la banque = ΔRes vu de la BC (écart 7e−15).
- E^CB de clôture identique par le stock et par les flux.
- ΔH recomposé par les portes = ΔRes, à condition de compter à 0 la part B_CB de la ligne 19 pour un achat primaire.

| N° | Emplacement | Constat | Correction proposée |
|---|---|---|---|
| 1 | Matrice des flux, ligne 19, colonne ΔH « + (B_CB) » | Vrai seulement pour un achat de la BC sur le marché secondaire. Pour une souscription **primaire**, M^G et B_CB montent dans le même bilan : ΔH = 0 ; H ne naît que quand l'État dépense | Scinder en **19a**, émission ou rachat primaire (ΔM − part B_H ; ΔH − parts B_H, B_Bk ; 0 part B_CB), et **19b**, opérations de la BC sur le marché secondaire (avec les ménages : ΔM +, ΔH + ; avec la banque : ΔM 0, ΔH +) |
| 2 | Portes de ΔH | Omet la part B_H émis, pourtant portée dans la matrice | « ligne 19a (parts B_H et B_Bk émis) ; ligne 19b (achats de la BC) » |
| 3 | En-tête des colonnes ΔM/ΔH | Les signes supposent le Trésor à la BC sans le dire | Ajouter « colonnes écrites sous la lecture (i) » |
| 4 | Règles de caisse et phases | **Réserves négatives intra-pas non déclarées.** La banque règle en réserves les impôts (phase 6), les souscriptions (phase 7) et i_CB L^CB (8 a) **avant** le refinancement (8 c) | Déclarer : Res peut être négatif **entre les phases** d'un même pas (découvert intrajournalier) ; Res ≥ 0 est vérifié à la clôture, après 8 (c) ; le refinancement est un flux décidé qui couvre au moins la position négative, à i_CB. Ce n'est pas la règle v2.0, car c'est une ligne nommée, à un taux nommé, dans une phase nommée |
| 5 | « L'émission de titres (phase 7) reconstitue le compte du Trésor » | L'État paie G (phase 5), Tr et i_B B (phase 6) **avant** d'émettre (phase 7). Sans A^G ni découvert, il doit tenir une encaisse M^G au moins égale aux dépenses nettes du pas. **Point frontière, deux positions** | (α) `macro` : garder la phase 7 après la phase 6 et faire de M^G un stock stationnaire résolu, publié. (β) `monnaie` : placer l'émission avec le crédit (phase 3, « le financement précède les règlements »), les souscriptions étant lues sur les plans de la phase 2. `monnaie` préfère (β) : aucune encaisse résiduelle à justifier, et une émission rationnée rationne aussitôt la dépense. **Le mainteneur tranche** |
| 6 | Q4 (b), borne pire cas | La borne n_pas × eps × S suppose une seule opération arrondie par pas. Avec 30 opérandes, le pire cas vaut 4,8e−12 S (720 pas) et 2,1e−11 S (3 120 pas), **au-dessus de ε_V = 1e−12**. Mesuré (5 postes, 30 flux par pas, S ≈ 1e7, 20 graines) : 3,3e−15 S (720 pas), 6,4e−15 S (3 120 pas) | ε_V = 1e−12 tient par la **mesure**, pas par le pire cas. Réécrire : « pire cas 30·n·eps ; mesuré ≤ 1e−14 S sur 3 120 pas ; ε_V = 1e−12 avec une marge ≥ 100 » ; le test J2 vérifie l'accumulation réelle |
| 7 | Q5, registre de l'indice | La règle de taux le lira : la variable est acquise, pas conditionnelle | Compter le registre comme imposé : C, 1 + 12 |

**Vérifiés sans constat.**
- Bilans : un émetteur par instrument, expressions de E^Bk et E^CB, Σ V = K + IN.
- Flux : lignes 9, 10, 12, 13, 15, 16, 20 à 22 ; contraintes budgétaires.
- Tolérances : échelles S ; ε = 1e−12 par pas.
- Phases : triangularité, et aucune ligne touchant Res après 8 (c), sous réserve du constat 4.

**Point hors cadre, pour les fiches 8 et 9.** Avec i_B au taux de la dernière date de décision et k = 0, toute la dette publique est à taux variable mensuel : une hausse du taux directeur frappe le budget de l'État dès le tour même. C'est défendable au socle, mais la fiche 9 dira si un encours à taux fixe est introduit.

### 6.5 Préférence entre C, D et E

**C**, avec `macro`, pour des raisons propres au domaine monétaire :
- sous C, le glissement annuel lu par la règle de taux est exactement P_t / P_{t−12} − 1, sur 12 valeurs, aux dates que lit le joueur. Sous D il y aurait 13 périodes sans mois ; sous E, des flux et des intérêts mensuels qui oscillent de +25 % / −20 %, illisibles pour une règle de taux et pour la prime souveraine ;
- une constatation mensuelle de la position de réserves et un refinancement mensuel suffisent au corridor ;
- coût de fidélité assumé : les ruées (Diamond et Dybvig, 1983) et les crises de change se joueront au mois. Si une fiche J6 établit un besoin infra-mensuel, la réserve 5 de `macro` s'applique.

Aucun désaccord avec `macro` sur (a) à (e) ni sur le classement. Un seul point reste ouvert à deux positions : le constat 5.

## 7. Avis de `jeu`

*`jeu`, 30/09/2026 (issue #16), sur la fiche à la tête `758273a`.*

**Chiffres.** Aucun chiffre nouveau. Ceux du § 3 ont été recalculés par `uv run python -c` le 30/09/2026 :
- écart entre un tour de 5 et un tour de 4 semaines : 5/4 − 1 = +25 % ; 4/5 − 1 = −20 % ;
- durée de calcul d'un tour pour N = 1 / 4 / 10 pays : 4,33 / 17,33 / 43,33 ms (C) ; 4 / 16 / 40 ms (D) ; 5 / 20 / 50 ms au plus (E) ;
- partie de 5 à 10 ans : 60 à 120 tours (C, E), 65 à 130 tours (D) ;
- 60 ans d'un pays : 3 120 ms quelle que soit l'option.

**Question ludique de la fiche.** Le cadre n'ouvre aucun levier et ne crée aucune asymétrie entre pays. Il fixe la **résolution temporelle de l'information** (ce que le joueur lit à chaque tour) et celle de l'**action** (une décision par tour). La question est donc unique : que gagne ou que perd le joueur quand la résolution du moteur (le pas) diffère de celle de sa décision (le tour) ?

### 7.A Option A — v1.5 (brièvement)

- **Ce que voit le joueur** : l'année vaut 48 ou 52 ticks selon la lecture, si bien que la date affichée et la fenêtre du glissement annuel ne coïncident pas. Un levier saisi en « fin de mois » agit au tick suivant, c'est-à-dire au tour suivant : délai d'un tour non déclaré.
- **Leviers** : sans matrice des flux, leur contrepartie comptable n'est pas montrable.
- **Stratégies** : sans objet.
- **Risques** :
  - bornes absolues (l. 489) qui coupent une réponse sans que le joueur sache pourquoi ;
  - seigneuriage assis sur le stock, un effet sans coût lisible.
- **Verdict** : **à revoir**.

### 7.B Option B — v2.0 (brièvement)

- **Ce que voit le joueur** : 13 dates de décision par an, sans mois ; deux dates d'effet différentes et non déclarées (impôts k = 0, taux k = 1 pas).
- **Leviers** : aucun catalogue. `Res` et `L_cb` sont résiduels : le coût du refinancement n'est jamais un flux que le joueur voit décider.
- **Stratégies** : sans objet.
- **Risques** :
  - historiques dans l'état : pas de reprise exacte, donc pas de contrefactuel apparié, et le test O2 est impossible ;
  - tolérances absolues.
- **Verdict** : **à revoir**.

### 7.C Option C — pas mensuel unique

- **Ce que voit le joueur**
  - Une date (année, mois). Tout ce qui est restitué au tour est exactement ce que le moteur calcule au pas.
  - Tout délai d'un bloc est un nombre entier de tours, et le glissement annuel compare simplement le tour n au tour n − 12.
- **Un tour comme plus court délai suffit-il pour 5 (b) ?** Oui, et c'est la seule option où la distinction est nette.
  - Un effet « instantané » change le flux du tour n dès le tour n ; un effet « différé d'un tour » apparaît au tour n + 1. Ce sont deux colonnes distinctes de la restitution.
  - Sous D et E, un bloc peut déclarer un délai de 1 à 3 pas que la restitution au tour ne distingue pas de l'instantané, précisément ce que 5 (b) interdit.
  - C rend cette interdiction **structurelle** ; D et E la laissent à la discipline de chaque fiche.
- **Délai k = 0 sur les trois leviers types, avec contrepartie le même tour**
  - *Taux directeur* : lignes 12 et 13 puis versement de la BC (ligne 16) le même mois. Le joueur voit le coût pour la banque centrale et pour son budget.
  - *Taux d'imposition* : les dépôts des ménages baissent et le compte du Trésor monte, le même tour.
  - *Dépense publique* : le compte du Trésor baisse, puis l'émission de titres suit, le même tour.
  - **Condition** : k ne mesure que le premier flux d'intérêt. La transmission du taux directeur à i_L, i_D, à l'investissement et à l'emploi relève des fiches 7 à 9. Elle doit être déclarée en tours entiers au § 9, sinon k = 0 fera croire que la politique monétaire agit en un mois.
- **Effet de lisibilité propre à C** (lecture du tableau Q5, à vérifier par le test O2 à J4) : une hausse de dépense publique au tour n se lit d'abord dans les ventes et la variation des stocks du tour n, puis dans la production au tour n + 1. Sous D et E, ce délai se produit à l'intérieur du tour et disparaît dans le cumul.
- **Leviers et stratégies** : sans objet, parce que le cadre n'offre aucun levier. Le versement de la banque centrale est celui du mois, sans lissage caché.
- **Risques**
  - *Réponse imperceptible* : aucune du fait du cadre. Une vitesse annuelle λ convertie en λ/12 doit rester ≤ 12 pour un ajustement monotone, contre ≤ 52 en hebdomadaire. Les mécanismes hebdomadaires de la v1.5 (l. 488–489) seront réécrits au mois. C'est un gain : aucun mécanisme ne peut être plus rapide que ce que le joueur voit.
  - *Piège irréversible sans signal* : aucun créé par le cadre. Une crise qui naît et se dénoue entre deux dates de décision serait, pour le joueur, un piège sans recours, quelle que soit la finesse du pas. Une crise étalée sur plusieurs tours laisse un signal et un tour pour agir (O3).
  - *Comportement contre-intuitif* : aucun. Le registre de 12 valeurs, résolu à l'état initial, donne un glissement annuel lisible dès le tour 1.
- **Verdict** : **lisible**.

### 7.D Option D — hebdomadaire, 13 dates de 4 semaines

- **Ce que voit le joueur** : « période 5 de l'année 2 » ; 13 tours par an ; glissement annuel sur 13 tours.
- **Irrégularité** : perceptible en permanence, mais cognitive et apprise une fois.
  - Tout délai exprimé en mois se traduit en 13/12 de tour (« 6 mois » ≈ 6,5 tours).
  - Il y a 8 % de décisions de plus par année simulée.
- **Exigence non tenue** : D ne satisfait pas l'exigence maintenue du critère 8, « le joueur lit une date (année, mois) ». Il n'a pas de mois à afficher, et M4 dit « tour mensuel ». Rebaptiser les 13 périodes en pseudo-mois serait une tromperie.
- **Plus court délai** : ¼ de tour, invisible pour le joueur.
- **Risques**
  - Comportement contre-intuitif : « l'année a 13 mois ».
  - Le versement de la BC devient un cumul intra-tour que le joueur ne voit pas se former.
- **Verdict** : **à revoir**.

### 7.E Option E — hebdomadaire, mois de 4 ou 5 semaines

- **Ce que voit le joueur** : le bon calendrier (année, mois, 12 tours). Mais **tout flux cumulé sur le tour** vaut +25 % en mars, juin, septembre et décembre par rapport au mois précédent, et −20 % le mois suivant.
- **Irrégularité** : perceptible sur chaque indicateur de flux, à chaque trimestre, pour toute la partie.
  - Un levier qui déplace la dépense publique d'un point de PIB (environ 1 % du flux mensuel) se cherche dans un bruit calendaire de ±20–25 %.
  - Le critère 7 (c) interdit la seule correction possible, la normalisation.
  - Le joueur perd la lecture mois contre mois, précisément celle qu'exige 5 (b). Ce n'est pas une irrégularité apprise une fois comme en D : c'est un **bruit permanent**.
- **Plus court délai** : ¼ ou ⅕ de tour, invisible pour le joueur.
- **Risques** : réponse imperceptible, le défaut central ; comportement contre-intuitif (« les impôts ont bondi de 25 % en mars sans que j'aie rien fait »).
- **Verdict** : **à revoir**.

### Durée de calcul d'un tour (critère 4 (c))

Elle n'est pas discriminante : 43,3 / 40 / 50 ms pour 10 pays, contre un seuil de 1 s. Au J4, un scénario apparié de 10 ans (2 × 120 tours) prend environ 1 s sous C (2 × 120 × 4,33 ms = 1 039 ms), ce qui rend la comparaison avec et sans levier interactive.

### Préférence motivée

**Option C**, comme `macro`, mais pour une autre raison. Une résolution du moteur plus fine que la résolution de la décision n'apporte rien au joueur et crée deux risques :
- des délais de bloc que la restitution ne distingue pas de l'instantané (5 (b)) ;
- des événements qui naissent et se dénouent entre deux tours, sans recours (O3).

Sous C, ce que le joueur voit, ce qu'il décide et ce que le moteur calcule ont la même résolution.

**Classement** : C > E > D sur la lettre des critères, puisque D ne tient pas l'exigence « année, mois ». Sur le seul coût perceptif, E est la pire.

**Conditions demandées au § 9** (aucune n'est une réserve sur C) :
1. Chaque fiche de bloc déclare ses délais de transmission en tours entiers, avec la contrepartie visible le même tour. Pour le taux directeur, k = 0 (premier intérêt) et le délai de transmission à i_L, i_D (fiche 7) sont deux grandeurs distinctes du catalogue.
2. Chaque vitesse annuelle λ respecte λ ≤ 12 (ajustement monotone sous conversion linéaire à 12 pas). Tout mécanisme hebdomadaire de la v1.5 est réécrit au mois, ou écarté.
3. Le test O2 de J4 compare, pour chaque levier, le tour n aux tours n − 1 et n + 1 du contrôle apparié.

**Lectures du § 5, vues du joueur**
- (b) Compte du Trésor à la banque centrale : préféré, parce que le refinancement devient un flux que le joueur voit naître de ses propres paiements.
- (c) k = 0 : préféré.
- (d) Versement de la BC sans troncature : préféré. Une perte versée en négatif est un coût lisible ; une troncature est un coût caché.
- (a) et (e) : pas d'avis ludique, la différence (0,9 à 1,5 %) étant sous le seuil de perception.

## 8. Décision du mainteneur

- **Numéro** : M22 (reporté dans `docs/feuille-de-route.md`, § 4).
- **Date** : 30/09/2026.
- **Option retenue** : **C**, pas mensuel unique (12 pas par an, un pas = un tour, décision à chaque pas), combinée au socle commun du § 3.N tel que corrigé par les constats de `monnaie` (§ 6.4). Lectures du § 5 :
  - (a) règle de conversion **linéaire unique** pour les taux, les flux et les vitesses, avec les trois conditions de `monnaie` (§ 6.1) ;
  - (b) compte du Trésor tenu **à la banque centrale** ;
  - (c) **k = 0** : un changement de taux s'applique dès le tour de la décision ;
  - (d) résultat de la banque centrale versé **chaque tour, sans troncature** (une perte est un versement négatif) ;
  - (e) ratio stationnaire = stock d'ouverture / (12 × flux du pas), le facteur vers le ratio sur 12 tours étant publié ;
  - (f) émission des titres publics **après les règlements** (position (α), phase 7), avec une encaisse M^G stationnaire résolue.
- **Motifs** : le mainteneur a retenu les recommandations concordantes de `macro`, `monnaie` et `jeu` (§ 5 à 7) et, sur le seul point de désaccord (f), la position conforme au principe de simplicité (une variable de moins, encaisse exactement stationnaire, un tour d'alerte pour le joueur). Motifs dans ses propres mots : à compléter par le mainteneur s'il le souhaite.
- **Conditions et réserves** : les cinq réserves du § 5, avec leurs seuils écrits avant l'essai (identités et invariance d'unité à J2, budget du noyau seul à J2, état stationnaire à J3, réouverture par une décision M-m citant M22 si un fait établit un besoin infra-mensuel) ; les trois conditions de `jeu` (§ 7) pour le § 9.
- **Ce qui est écarté et pourquoi** : A (v1.5 : matrice des flux absente, 48 ≠ 52, bornes absolues) ; B (v2.0 : soldes résiduels, tolérances absolues, historiques dans l'état) ; D (13 tours par an sans mois : l'exigence « année, mois » du critère 8 n'est pas tenue) ; E (bruit calendaire de ±20–25 % sur les flux mensuels) ; la conversion composée pour les taux (intérêts versés inexacts, ratios stationnaires dépendant du pas) ; le compte du Trésor à la banque (refinancement inerte au socle) ; la troncature du versement de la banque centrale (réservée à J6) ; l'émission avant les règlements (β : une variable de prévision de plus). Ces pistes alimentent `sec:ecartees` de la spécification (#18).

## 9. Conséquences de la décision

Non instruit.

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 30/09/2026 | Ouverture (issue #15) ; § 1 et § 2 proposés | `macro`, `monnaie`, `jeu` ; session principale |
| 30/09/2026 | Liste courte (14), principe de simplicité et amendements ; **critères validés** (issue #15) | mainteneur |
| 30/09/2026 | Instruction déposée (§ 3 à 5, issue #16) | `macro` |
| 30/09/2026 | Avis de `jeu` (§ 7, issue #16) | `jeu` |
| 30/09/2026 | Avis de `monnaie` (§ 6, issue #16) ; sept constats sur le § 3.N | `monnaie` |
| 30/09/2026 | Constats 1 à 4, 6 et 7 intégrés au § 3.N ; constat 5 porté au § 5, lecture (f) ; statut « avis rendus » | `macro` ; session principale |
| 30/09/2026 | Décision M22 (option C, lectures (a) à (f)) | mainteneur |
