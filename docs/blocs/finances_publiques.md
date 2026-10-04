---
bloc: État et dette
module: src/nations/blocs/finances_publiques.py
expert pilote: macro
experts consultés: monnaie (placement de la dette et prime : frontière dette publique) ; jeu
statut: décidée (M33)
décision: M33 (04/10/2026)
issue: #73
---

# Fiche comparative — État et dette

> Fiche ouverte à partir du gabarit `0000-gabarit.md` (validé à l'usage, M20), sur le modèle de forme des fiches 5 « ménages » et 6 « investissement et financement des entreprises » (M27, M28). Jalon 1 de l'issue #73 : § 1 et § 2 seuls ; les rubriques suivantes portent « à instruire (jalon 2) ». La fiche est **décidée par paire avec la fiche 8** « banque centrale et anticipations » (décision P14 du 04/10/2026 ; numéros M32 et M33 sous réserve de l'ordre réel des décisions). Ses critères sont validés avec ceux des fiches 7 et 8, en tête de branche, avant tout commit d'instruction. Son instruction (jalon 2) attend que la fiche 8 soit « avis rendus » (`docs/feuille-de-route.md` § 1, rang 6).

Une fiche comparative instruit **l'origine de l'approche** d'un bloc (`docs/exigences.md` § 2.3) : la spécification v1.5, le moteur v2.0, ou une approche nouvelle. Elle est **instruite par l'expert pilote**, commentée par `jeu` et par l'expert consulté que désigne `README.md`, et **décidée par le mainteneur** (décision M-n, reportée dans `docs/feuille-de-route.md`). Aucune approche n'entre dans le moteur ni dans la spécification sans cette décision. Les agents n'écrivent pas la fiche dans le dépôt : elle figure dans leur compte rendu et la session principale la commite. Un **bloc-cadre** (temps et comptabilité) n'est pas un module de `blocs/` : sa fiche instruit ce que le cadre **définit** (conventions, matrices, règles), non des flux proposés ; les adaptations que cela impose sont signalées rubrique par rubrique.

Règles de rigueur (`CLAUDE.md`, « Rigueur ») :
- un chiffre se remesure ou cite sa source ;
- une équation de la v1.5 n'a jamais été garantie exécutée ;
- un comportement de la v2.0 ne vaut que sous son profil (état D1, **non versé** : aucun fait ne peut y être remesuré) et avec ses défauts connus ;
- chaque fait de la première tentative porte son **statut** S+O, O, R, L, V ou V+O (`CONTEXT.md`, « Statut d'un fait ») ; un fait V sur le prototype v2.0 reste un fait de la première tentative, non un résultat v3 ;
- chaque référence est une publication retrouvée ;
- citer `archive/v1.5/…` avec numéro d'équation et section, ou avec le **numéro de ligne du `.tex`** quand section ou équation ne sont pas identifiables sans compiler ; citer `archive/v2.0/…` avec fichier et ligne.

**Principe de simplicité** (adopté par le mainteneur le 30/09/2026, fiche « temps et comptabilité » § 2 ; `CONTEXT.md`) :
- à exigences comptables égales, l'option la plus simple pour le joueur et pour le moteur est préférée ;
- toute complexité se justifie par une identité qu'elle rend vérifiable ou par un mécanisme perçu à l'échelle d'une partie ;
- une simplification ne supprime ni une contrepartie comptable visible d'un levier ni une grandeur restituée au tour ;
- les identités, les tolérances relatives, le déterminisme, les invariants de l'ADR 0002 et la concordance ne se simplifient pas.

## 1. Question posée

*Rédigé par `macro` (expert pilote), 04/10/2026, sur la spécification à l'état `10391a1` (branche `claude/j1-monnaie-etat`, PR #77). Les numéros de ligne sans fichier renvoient à `docs/specification/nations_et_marches.tex` à cet état.*

Le bloc porte le secteur de l'État du socle. Il comprend :
- **les dépenses** : la dépense publique, plan en u.m. écrit en phase 2 (« dépense publique du pas », `tab:phases`, l. 530) puis ligne 2 exécutée en phase 5 sur le volume servi ; les transferts aux ménages (ligne 6, phase 6) ;
- **les recettes** : les impôts des ménages et des entreprises (ligne 7, phase 6) ;
- **la charge d'intérêts** sur les titres publics, au taux i_B (lignes 11a à 11c, phase 6), et la réception du résultat de la banque centrale (ligne 16, phase 8 (b)), dont le montant est calculé par le bloc 8 en phase 1 (l. 495) ;
- **l'émission** des titres publics en phase 7, après les règlements (M22, lecture (f), position α) : ligne 19a, avec un compte du Trésor M^G qui clôt le pas à l'encaisse M^G\* (l. 497 à 502) ;
- **le solde public, la dette publique et la règle budgétaire de référence** (pays non joués, test zéro) ;
- **les leviers budgétaires du joueur** : taux d'imposition, dépense publique, transferts (`tab:leviers-cadre`, l. 2034 à 2036). L'émission n'est pas un levier du socle (l. 502 et 2017).

C'est le dernier bloc du socle : il « clôt le bouclage stock-flux » (`docs/blocs/README.md` § 3, rang 9 ; `sec:finances_publiques`, l. 2008). Deux identités, dérivées du cadre, structurent la fiche.

1. **La dette publique n'est pas un paramètre libre à l'état stationnaire.** Dans `tab:matrice-bilans` (l. 298 à 307), la somme des valeurs nettes vaut K + IN. On en tire, avec B = B_H + B_Bk + B_CB :
   - B − M^G = V_H + (D_F − L) + E^Bk + E^CB ;
   - autrement dit, la dette nette de l'encaisse égale la richesse financière nette du secteur privé, plus les fonds propres de la banque et de la banque centrale.
   - Les fiches décidées fixent déjà deux termes :
     - V_H = ν_H n_a YD^HS (M27) ;
     - L − D_F (M28) : (L − D_F)/(12 × PIB) vaut 0,456 à π̄ = 2 % et 0,169 à 10 % (condition C30, `investissement.md` l. 1397).
   - *Illustration*, sous les hypothèses ν_H = 1 an, E^Bk = E^CB = 0 et π̄ = 2 % : si YD^HS/PIB vaut 0,6, 0,7 ou 0,8, (B − M^G)/(12 × PIB) vaut 0,144, 0,244 ou 0,344 an.
   - Une règle qui vise la dette fait donc d'un autre instrument son résultat (fiche 6 § 3.E, l. 784).
2. **Le solde stationnaire est fixé par la dette et la croissance nominale** (identité de Domar, dérivée de la formule d'émission des l. 499 et 500). Sur la trajectoire de référence, B et M^G croissent du facteur Γ̄ par pas, si M^G\* croît comme le PIB (critère 11). On a alors :
   - Déficit_t = G + Tr + i_B B/n_a − T_H − T_F − Π^CB = (Γ̄ − 1)(B_t − M^G_t) ;
   - en part du PIB annuel, n_a(Γ̄ − 1) × (B − M^G)/(12 × PIB), soit **3,9671 %** de la dette nette à g = π̄ = 2 % et n_a = 12 ;
   - 3,9802 % et 3,9620 % à n_a = 4 et 52 ; 11,5667 % à π̄ = 10 % et n_a = 12 (commande au compte rendu de `macro` du 04/10/2026).

   Le solde n'est donc pas un paramètre libre non plus.

Il reste au bloc à dire quel instrument porte le résultat, et quelle variable ferme le niveau d'activité (#44, avec la fiche 8). Sous M22, un pas est un tour (n_a = 12, n_m = 1) : toute fenêtre exprimée en pas l'est aussi en tours.

### 1.1 Contrats hérités

| Contrat | Source | Ce qu'il impose à la fiche 9 | Ce qui le rouvrirait |
|---|---|---|---|
| Calendrier, conversions et phases | M22 ; ADR 0005 ; ADR 0008, I.2 ; `tab:phases` (l. 528 à 537) ; `sec:cadre-phases` (l. 510) | **Pas et conversions** : pas mensuel, n_a = 12. i_B est un taux de flux, converti linéairement (i_B B/n_a). Les vitesses de la règle budgétaire sont linéaires, avec λ ≤ n_a. Les taux de croissance et d'inflation (indexation d'un plan, croissance d'une cible) sont géométriques. **Phases** : plan de dépense en phase 2 ; ligne 2 en phase 5, après prix et production (l. 533) ; lignes 6, 7 et 11a à 11c en phase 6, **sans ordre interne** (l. 510 et 534) ; émission en phase 7, l'ordre « État, banque, banque centrale » restant « à fixer par leurs fiches » (l. 535) ; ligne 16 en 8 (b) (l. 536). Neuf phases triangulaires, aucune résolution simultanée | Décision citant M22 ; un ADR pour tout ordre interne nouveau |
| Compte du Trésor et émission après les règlements | M22, lectures (b) et (f) ; ADR 0005, points 9 et 13 ; `sec:cadre-caisse` (l. 497 à 502) | **Compte du Trésor** : M^G est tenu à la banque centrale, sans intérêt ; chaque impôt draine des réserves, chaque dépense publique en crée. **Émission** : en phase 7, l'État émet le besoin réalisé du pas (formule des l. 499 et 500), et M^G clôt à M^G\*. **Encaisse M^G\*** (l. 502) : elle « n'excède pas les paiements bruts d'un pas avant impôts » ; elle « n'est pas un paramètre : c'est une variable de l'état initial résolu », calculée « selon la règle du bloc État et dette » ; un placement raté laisse M^G sous M^G\*, et le rationnement de la dépense frappe le tour suivant. L'émission n'est pas un levier. La position β, émission avant les règlements, est écartée (ADR 0005, options écartées, l. 80) | Décision citant M22 |
| Résultat de la banque centrale | M22, lecture (d) ; ADR 0005, point 12 ; l. 491 à 495 | Π^CB est versé chaque tour, sans troncature ; il est calculé en phase 1 sur des encours d'ouverture. Une perte est un versement négatif, payé depuis M^G et soumis à la règle de caisse de l'État. E^CB reste à sa valeur initiale résolue. Troncature et recapitalisation sont réservées au J6 | Décision citant M22 |
| Intérêts et durée de la dette | M22, lecture (c) ; ADR 0005, point 11, et § Conséquences (l. 89) ; l. 483 et 548 | Intérêt assis sur l'encours brut d'ouverture. Toute la dette porte le taux de la dernière date de décision. Au socle, aucun encours à taux fixe, qui « relèverait du bloc État et dette » | Décision citant M22 (C24) |
| Instruments et portefeuille | M22 ; ADR 0005, point 7 ; M27, lecture (c) ; l. 1441 | **Instruments** : ni avances au Trésor ni billets ; la seule porte de monnaie centrale vers l'État est l'achat de titres par la banque centrale. **Portefeuille** : B_H ≡ 0 ; les lignes 11a, 19a-ménages et 19b-ménages restent à montant nul, sans retrait (un retrait exigerait une décision citant M22) ; le placement est assuré par la banque et la banque centrale | Décision citant M22 ou M27 |
| Matrices et portes de la monnaie | `tab:matrice-flux` (l. 341 à 368) ; `tab:portes-monnaie` (l. 410 à 437) ; sortie de `verifier_matrices.py --strict` à `10391a1` : 9 / 28 / 28 lignes, 44 / 62 / 31 termes, « Aucun écart » | La colonne de l'État porte les lignes 2, 6, 7, 11a à 11c, 16, 19a (trois souscripteurs) et 22. La ligne 22 est une contrepartie de règlement, appliquée par le noyau. Aucune ligne ni aucun poste n'est ajouté sans décision. La CI bloque une table dont une ligne ne somme pas à zéro | Décision citant M22, et un ADR |
| Règles de caisse | `sec:cadre-caisse` (l. 481) ; ADR 0005, point 10 | L'État paie sur M^G. Un payeur ne paie pas plus que son moyen de paiement ; la part non payée est une ligne nommée du bloc payeur, jamais un découvert implicite ni un ajout au principal. Le bloc déclare son ordre de priorité. La date du contrôle de caisse dans une phase sans ordre interne n'est pas fixée (constat de la fiche 5, § 9.8, `menages.md` l. 1978) | Décision citant M22 |
| Dates d'effet des leviers | M22 ; `tab:leviers-cadre` (l. 2033 à 2036) | Taux d'imposition : ligne 7, phase 6, délai 0. Dépense publique : ligne 2, phase 5, délai 0. Transferts : ligne 6, phase 6, délai 0. Les contreparties visibles le même tour sont listées | Décision du mainteneur citant M22 |
| Variables d'état et phase 9 | M29 ; ADR 0009 ; l. 512 | Une variable d'état assise sur un flux lit le montant exécuté, au grand livre. Elle est écrite en phase 9 si aucune phase du bloc ne convient | Décision citant M29 |
| Cible d'inflation et facteur du moteur | M30 ; ADR 0010 ; l. 222 | Toute lecture de la cible porte sur π\*_t d'ouverture. Γ^e est calculé par le moteur et n'est jamais recalculé | Décision citant M30 |
| Bornes | #38, lecture (ii) ; `CONVENTIONS.md` § 2.4 | Une borne à seuil libre a un paramètre déclaré et un motif contre un mécanisme. Une contrainte de conservation n'a pas de paramètre : elle est déclarée dans les `\limites`, avec son activité à l'état stationnaire et un test | Décision citant #38 |
| Fiche 3 (M25) | M25 ; l. 977 | Les allocations de chômage (ligne 6) et les cotisations et impôts sur les salaires (ligne 7) relèvent du bloc 9. La relation salaires – chômage est verticale (U^eq) : l'état stationnaire exige y = pr(1 − U^eq)N^pa (#44) | M25 |
| Fiche 5 (M27) | Critère 10 (`menages.md` l. 188) ; § 6.3 (l. 1221 à 1224) ; § 9.4 (l. 1729) ; § 9.8 (l. 1976 à 1979) ; `sec:menages` (l. 1478, 1542, 1638) | **Lecture de H7** : H7 a une forme symbolique ; T_H et Tr sont lus au grand livre en phase 9 ; transferts et impôts du tour n agissent sur le budget du tour n + 1. **Comportement** : aucun comportement ricardien ; V_H = ν_H n_a YD^HS. **Insuffisance de dépôts pour la ligne 7** : rationnement déclaré (impôt non recouvré), sans créance fiscale. **Conditions** C23 à C25 | M27 |
| Fiche 6 (M28) | § 3.E (`investissement.md` l. 773 à 791) ; § 6.3 (C30, C36) ; § 6.6 (C37) ; § 9.8 (l. 2291) ; `sec:investissement` (l. 1779, 1865) | **Impôt des entreprises** : l'assiette de T_F comprend la ligne 8 comptable ; T_F tombe sur Div_F, jamais sur l'investissement ; impôt anticipé T^e_F = Γ^e T_{F,t−1} (F4), exécuté et retenu en phase 9, avec un rattrapage au tour n + 1. **Dette** : B/PIB porte le solde des normes privées ; si la règle vise B/PIB, le taux d'impôt est son résultat. **Taux réel ϱ̄_L** : deux lectures (l. 1865). **Terme ζ** : il sort de la spécification si la fiche 9 retient un autre canal de niveau (M28). **Condition** C37 | M28 |
| Statut des faits | Décision P1 du 03/10/2026 ; `CONTEXT.md` | Statuts S+O, O, R, L, V ou V+O. L'état D1 n'est pas versé | — |

### 1.2 Ce que le bloc doit produire

Les symboles **ne sont pas fixés** : ils le seront à l'instruction, sous le critère 21. **PIB nominal du pas** : PIB_t = C_t + G_t + I_t + ΔIN_t (lignes 1 à 4), en u.m. par pas. C'est la définition déjà employée par la fiche 6 (« p v + ΔIN », l. 1853).

| Grandeur | Définition | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| Plan de dépense publique | Budget de dépense du pas, fixé en phase 2 | u.m. par pas | — | le pas, phase 2 |
| Dépense exécutée G ; taux d'exécution | p_t·v_{G,t}, ligne 2, phase 5 ; G/plan | u.m. par pas ; fraction | plan du pas | le tour ; 12 tours |
| Transferts Tr | Ligne 6, phase 6 | u.m. par pas | — | le tour ; 12 tours |
| Impôts T_H, T_F ; taux apparents | Ligne 7, phase 6 ; impôt rapporté à son assiette déclarée | u.m. par pas ; fraction | assiette | le tour ; 12 tours |
| Charge d'intérêts, brute et nette | i_B B/n_a (lignes 11a à 11c) ; i_B B/n_a − Π^CB | u.m. par pas ; part du PIB | PIB nominal sur 12 tours | 12 tours |
| Solde primaire | T_H + T_F − G − Tr | u.m. par pas ; part du PIB | PIB nominal sur 12 tours | 12 tours |
| Solde public | Solde primaire − i_B B/n_a + Π^CB = −(ΔB − ΔM^G) | u.m. par pas ; part du PIB | PIB nominal sur 12 tours | 12 tours |
| Émission | ΔB^prim par souscripteur, ligne 19a, phase 7 | u.m. par pas | — | le pas |
| Encaisse du Trésor M^G ; encaisse M^G\* | Ouverture ; clôture ; rapport aux paiements bruts du pas | u.m. ; tours de paiements | paiements bruts du pas | ouverture, clôture |
| Dette publique | Brute B ; nette de l'encaisse B − M^G ; consolidée État et banque centrale B − M^G − E^CB = B_H + B_Bk + Res − L^CB ; part détenue par la banque centrale B_CB/B | u.m. ; années de PIB ; fraction | test zéro : 12 × PIB du pas ; restitution : somme des 12 derniers PIB | ouverture (test zéro) ; clôture (restitution) |
| Taux des titres i_B | Taux de la dernière date de décision (l. 483) ; règle à déclarer avec `monnaie` | par an, taux de flux | — | phase 1 |
| Variables d'état du bloc, si l'option en a | Par exemple : dépense du pas précédent, taux apparent de la dette, impôt retardé | unité propre | — | ouverture |
| Parts non payées, si lignes nommées | Dépense rationnée ; impôt non recouvré ; perte de la banque centrale non versée | u.m. par pas | — | le pas |

### 1.3 Ce qu'il lit

- **Ouverture** :
  - B_Bk et B_CB (B_H ≡ 0) ; M^G ; ses variables d'état ;
  - π\*_t et Γ^e (moteur) ;
  - le dernier prix connu P_{t−1}, s'il en a besoin.
- **Phase 1** :
  - les leviers, lus par le moteur ;
  - les taux arrêtés par le bloc 8, pour i_B ;
  - Π^CB, calculé par le bloc 8 (l. 495).
- **Phase 2** : aucun autre plan (phase sans ordre interne).
- **Phase 4** : WB_t et N_t, comme assiettes ou bases d'allocations.
- **Phase 5** :
  - p_t et v_{G,t}, pour proposer la ligne 2 après les blocs 4 et 2 ;
  - C_t, I_t et ΔIN_t, comme assiette éventuelle de T_F.
- **Phase 6** : rien de ce qu'un autre bloc y écrit, puisque la phase n'a pas d'ordre interne (critère 2 (c)).
- **Phase 7** :
  - les positions exécutées des phases 5 et 6, qui donnent le besoin réalisé ;
  - un ordre interne avec la banque et la banque centrale (C25).
- **Phase 9** : les montants exécutés du pas, au grand livre (M29).
- **Leviers du joueur** : taux d'imposition, dépense publique, transferts. Aucun autre sans décision.
- **Décisions qui le contraignent** :
  - M13, M19 (critère de J1), M22 (ADR 0005), M24 (ADR 0007), M25 et M26 (ADR 0008), M27, M28, M29 (ADR 0009), M30 (ADR 0010) ;
  - décision du 03/10/2026 sur #38 ;
  - P14 (décision par paire) et P16 (a) (script d'état stationnaire à la branche n° 4 bis).

### 1.4 Frontières

**Blocs décidés**
- **Ménages (fiche 5, M27)** : le bloc 5 lit T_H, Tr, i_B et la ligne 19a-ménages (nulle). Les hypothèses provisoires de `sec:menages` sont à remplacer, et l'impôt non recouvré à déclarer. Critères 12 et 14.
- **Investissement (fiche 6, M28)** :
  - le bloc 6 lit G (ligne 2) et T_F ; l'assiette de T_F est fixée ;
  - B/PIB est le résultat des normes privées (§ 3.E) ;
  - ϱ̄_L reste entre deux lectures (l. 1865) ;
  - condition C37 ; le terme ζ n'est garanti que si la fiche 9 ne retient pas un autre canal de niveau.

  Critères 4, 5, 6, 9 et 14.
- **Travail (fiche 3, M25)** : la verticale U^eq ; allocations de chômage et cotisations. Critères 6 et 14.

**Blocs en instruction, tenus par `monnaie`**
- **Banque commerciale (fiche 7)** :
  - C19 : la banque souscrit le reliquat ;
  - C22 : limite de détention, dont l'activation est le placement raté ;
  - E^Bk entre dans l'identité de la dette.

  Critères 5, 12 et 13.
- **Banque centrale et anticipations (fiche 8, décidée par paire)**. Critères 5, 6, 8, 9, 11, 12, 13 et 18.

**Frontière dette publique** (`docs/blocs/README.md` § 2, l. 31) :
- chez `macro` : le solde, la dynamique de la dette et la règle budgétaire ;
- chez `monnaie` : le placement (banque, banque centrale) et la prime.

**`jeu`** : critère 17 et avis au § 7.

**Points de frontière à coordonner avec la fiche 8**. `macro` n'a pas consulté `monnaie` à ce jalon ; ces points sont à reprendre dans le jalon 1 de la fiche 8 ou à sa validation :
- (a) **#44** :
  - quelle variable ferme le niveau d'activité ;
  - un tableau de comptage commun ;
  - **une seule action intégrale par condition stationnaire** : sous la verticale de M25, U = U^eq tient dans tout état stationnaire ; une action intégrale sur l'activité n'ajoute aucune équation, seulement une inconnue (critères 6 (b) et 4 (b), amendés le 04/10/2026) ;
  - les deux lectures de ϱ̄_L (l. 1865).
- (b) **C36 et C37** : mesure conjointe, sur la même maquette, avec ζ dans l'ordre de grandeur de M28 (4 à 8, hypothèse).
- (c) **#56** : la propriété attendue est écrite une seule fois, avant l'essai. `macro` en propose le texte au critère 18.
- (d) **i_B** :
  - `tab:instruments` (l. 277) en confie la règle à `sec:finances_publiques`, mais la prime relève de `monnaie` ;
  - à fixer : rapport à i_CB, prime nulle ou mécanisme, date.
- (e) **Π^CB négatif et E^CB** (#26, points 1 et 2) :
  - ligne nommée ou règle de recapitalisation, et quel bloc la propose ;
  - effet sur l'identité B − M^G.
- (f) **Phase 7 (C25)** : souscription primaire et achats décidés de la banque centrale (19a-BC, 19b-banque).
- (g) **M^G\* et réserves** : chaque impôt draine des réserves ; l'effet du niveau de M^G\* sur Res et L^CB à la clôture (légende de `tab:leviers-cadre`, l. 2024).
- (h) **Dominance budgétaire** (pays joué, intérêts financés par le déficit) et divergence de C2 (`monnaie`, fiche 6 § 6.6, l. 1540 et 1550).
- (i) **Symbole de la dette** : `sec:menages` emploie déjà b pour « la dette publique nette détenue hors banque centrale en années de revenu hors intérêts » (l. 1546).

### 1.5 Ce que la fiche ne tranche pas, et questions ouvertes

**Hors du périmètre**
- **Défaut, restructuration, prime souveraine endogène, plafond indicatif** (v1.5, `eq:spread` l. 1223, `eq:default` l. 1528, plafond l. 1539 à 1541) : J6, `monnaie`.
- **Avances au Trésor, monétisation, billets** : absents du socle (ADR 0005, point 7) ; instabilité 2.
- **Dette en devise, tarifs** : J5.
- **Composition de la dépense et effets d'offre** (investissement public, éducation, santé, capital public ; v1.5 l. 1472 à 1480) : aucun levier d'offre au socle (M28 ; #37, ouverte jusqu'au J7).
- **Recettes multiples de la v1.5** (l. 1452 à 1470) :
  - fiscalité de la consommation : renvoyée au catalogue des leviers du J4 (fiche 5, Q11) ;
  - capitation, capacité administrative et courbe de Laffer : décrites au § 3 comme éléments de l'option A, leur retrait est motivé.
- **Entreprises publiques, nationalisation** : J7.
- **Strates de ménages** : fiche 5, variante D, J4.
- **Calibration** : J3. Les bandes du test zéro sont confirmées avec O1 avant l'essai (M19).

**Questions ouvertes à instruire**
- **Q1 — Règle budgétaire de référence.** Options à instruire :
  - **A (v1.5)** :
    - facteur des achats `eq:fiscrule` (l. 1513 à 1518) ;
    - recettes (l. 1457 à 1470) ;
    - contrainte `eq:gbc` et dynamique `eq:debtdyn` (l. 1500 à 1503) ;
    - taux apparent `eq:iapp` (l. 1484 à 1490) ;
    - placement (l. 1520 à 1527).
  - **B (v2.0)**, branche active de D1 : `tax_rule=True`, `fiscal_rule=False` (`archive/faits_mesures_G_K.md` l. 11) :
    - multiplicateur des impôts sur le revenu (`policies.py` l. 73 à 96) ;
    - émission vers une encaisse égale à `gov_cash_ratio` × PIB annuel (`model.py` l. 1215, `gov_cash_ratio` = 0,04 par défaut, l. 201) ;
    - placement aux ménages, puis à la banque dans sa limite (l. 1220 à 1244).
  - **Nouvelles** :
    - reprise intégrale de la charge d'intérêts (« T9 », fiche 6 § 3.L, l. 934) ;
    - réaction de Bohn (fiche 6 § 6.6) ;
    - instrument ancré sur l'activité (finance fonctionnelle, Lerner, 1943) ;
    - dépense et taux d'imposition fixés, forme des modèles SIM et PC de Godley et Lavoie (2007), lus par reproduction.
- **Q2 — Instrument qui porte le résultat** : dépense, taux d'imposition des ménages ou transferts (critères 4 et 5).
- **Q3 — Fermeture du niveau d'activité** (#44, avec la fiche 8 ; critère 6).
- **Q4 — Charge d'intérêts** (C23, C37 ; critère 9).
- **Q5 — Durée de la dette** (C24 ; critère 10).
- **Q6 — Encaisse M^G\* et contrôle de caisse** (#26, point 3 ; P2 ; critère 11).
- **Q7 — Ordre des paiements de l'État et parts non payées** (#26, point 1 ; critère 12).
- **Q8 — Assiettes et phases des impôts et transferts** : T_H sur WB_t (phase 4), sur YD_{t−1} ou autre ; cotisations ; allocations ; T_F selon la fiche 6 (critères 2 et 14).
- **Q9 — Phase 7 et taux des titres** (C25 ; i_B avec `monnaie` ; critère 13).
- **Q10 — Forme du plan de dépense.** Trois formes candidates :
  - part du PIB passé, prolongée par Γ^e ;
  - volume indexé ;
  - autre.

  Sous M24 (g), un plan en u.m. a une élasticité de −1 du volume au prix du pas. La gratuité de la sur-commande est à traiter (#53 ; critère 17 (e)).
- **Q11 — Règle de référence et leviers du joueur** (pays joué ou non joué), sans drapeau de mode (critère 19).
- **Q12 — Restitution** : dette brute ou nette ; soldes ; charge d'intérêts (critères 5 et 17).

### 1.6 Conditions et issues reçues : traitement

Chaque élément listé par #73 est **retenu**, **écarté** ou **transmis**, avec sa raison. Les éléments que les fiches décidées ont transmis à la fiche 9 sans figurer dans #73 suivent, sous la ligne de séparation.

| Élément | Source | Traitement | Où | Raison |
|---|---|---|---|---|
| C23, règle face à la charge d'intérêts | Fiche 5 § 6.3 (`menages.md` l. 1222) | Retenu | Critère 9 (a) | Elle fixe le signe de long terme du canal rentier (Auclert, 2017, p. 17, lu par `monnaie`) |
| C24, durée de la dette | Fiche 5 § 6.3 (l. 1223) ; ADR 0005, § Conséquences (l. 89) | Retenu | Critère 10 | Variante instruite ; si elle est retenue, la décision cite M22 (l. 548) |
| C25, ordre de la phase 7 sous B_H ≡ 0 | Fiche 5 § 6.3 (l. 1224) | Retenu, avec les fiches 7 et 8 | Critère 13 | L'ordre de la phase 7 reste « à fixer par leurs fiches » (l. 535). La variante de Tobin est transmise au J6 |
| C36, gain statique et stationnarité de l'action intégrale | Fiche 6 § 6.3 (`investissement.md` l. 1408 à 1413) ; rédaction de M28 (l. 1849) | Retenu comme mesure conjointe ; la règle de taux reste à la fiche 8 | Critères 8 (d) et 9 (c) | M28 : « côté monétaire, C36 se juge avec la règle de la fiche 9 » |
| C37, qui paie le surcroît d'intérêts | Fiche 6 § 6.6 (l. 1531 à 1541) | Retenu (exigence) | Critère 9 (b) | Sans reprise budgétaire, aucun ζ testé ne tient C36 (fiche 6 § 5 et § 6.6, maquettes) |
| Règle visant B/PIB sans surdétermination | Fiche 6 § 3.E (l. 783 et 784) | Retenu | Critères 4 (b) et 5 | Identité de la dette (§ 1, point 1) |
| Grandeurs lues par le bloc 5 ; hypothèses provisoires | Fiche 5, critère 10 (`menages.md` l. 188) ; `sec:menages` l. 1542 | Retenu | Critère 14 | La fiche 5 a écrit ses formes symboliques pour que la fiche 9 ne la réécrive pas |
| #26, point 1 : perte de la banque centrale non payée | #26 | Retenu côté État ; transmis à la fiche 8 côté banque centrale (E^CB, recapitalisation) | Critère 12 (c) ; point (e) du § 1.4 | Répartition décidée par P13 : point 1 → fiches 8 et 9 |
| #26, point 3 : règle de M^G\* | #26 ; renvoi du mainteneur du 02/10/2026 | Retenu | Critère 11 | L'illustration du point 3 est reproduite (5,69 à 25,80 ans, commande au compte rendu) |
| P2 : notation de M^G\* | Décision du 03/10/2026 ; commentaire sur #26 | Retenu | Critères 11 (d) et 21 | La marque ∗ (cible) et « stationnaire » (barre) se cumulent sans explication (`CONVENTIONS.md` § 5.2 ; l. 502, 2064, 2410) |
| #44, variable de fermeture du niveau d'activité | #44 et ses commentaires | Retenu pour les variantes budgétaires ; fermeture déclarée avec la fiche 8 | Critère 6 | P14 ; #44 se ferme à la n° 4 bis (P16 (a)) |
| #56, propriété attendue avant l'essai | #56 | Retenu comme critère partagé : texte commun de `monnaie` et `macro` au critère 15 de la fiche 8 | Critère 18 | #56 demande une propriété écrite par `monnaie` et `macro` avant l'essai |
| — | — | — | — | — |
| Insuffisance de dépôts pour la ligne 7 | Fiche 5 § 9.8 (l. 1978) ; `sec:menages` l. 1441 | Retenu | Critère 12 (d) | Le traitement compatible avec le socle est une ligne nommée du bloc 9 |
| Gratuité de la sur-commande (#53) | Fiche 2 § 7 (`production.md` l. 914) ; fiche 5, condition 9 de `jeu` (`menages.md` l. 1468) | Retenu | Critère 17 (e) | « Soit supprimée, soit rendue visible et coûteuse (fiche 9, J4) » |
| Assiette et date de T_F | Fiche 6 § 9.8 (`investissement.md` l. 2291) | Retenu | Critère 14 (b) | Contrat de la fiche 6 (F3, F4) |
| Dépendance de B/PIB à π̄ (C30) | Fiche 6 § 6.3 (l. 1397) | Retenu (mesure) | Critère 5 (d) | Renvoi explicite à la fiche 9 |
| #26, point 2 : E^CB constant en niveau | #26 ; P13 (point 2 → #72) | Transmis à la fiche 8 ; la fiche 9 porte E^CB dans son identité | Critère 5 (b) ; point (e) du § 1.4 | Décision de P13 |
| Allocations de chômage, cotisations | l. 977 | Retenu comme options de Tr et de T_H | Critère 14 (e) | Renvoi de `sec:travail` |
| Capital public, effets d'offre de la dépense | Fiche 6, critère 10 (a) ; #37 | Écarté au socle ; transmis au J7 | § 1.5 | M28 : aucun levier d'offre au socle |
| Fiscalité de la consommation | Fiche 5, Q11 | Écartée du socle ; transmise au catalogue du J4 | § 1.5 | Amendement de la fiche 5, Q11 |
| Avances au Trésor ; prime et défaut | ADR 0005, point 7 ; v1.5 l. 1223, 1528 | Écartés du socle ; transmis à J5 et J6 (`monnaie`) | § 1.5 | Instruments absents (M22) ; instabilité 2 |

## 2. Critères d'évaluation, écrits avant l'instruction

**Statut** : proposés par `macro` le 04/10/2026, **validés par le mainteneur le 04/10/2026**, avec les amendements ci-dessous avec ceux des fiches 7 et 8 (P14), avant tout commit d'instruction (jalon 1 de #73). La liste est fermée : elle ne se déplace pas après observation (`docs/exigences.md` § 2.5). Un amendement adopté avant l'instruction se consigne sous le tableau.

Correspondance avec le gabarit :

| Critère du gabarit | Critère de la fiche |
|---|---|
| 1 | 1 |
| 2 | 4, 5 et 7 |
| 3 | 8 |
| 4 | 20 |
| 5 | 17 |
| 6 | 16 et 19 |

Critères propres au bloc : 2, 3, 6, 9 à 15, 18, 21, 22 et 23.

**Exigences** (elles peuvent écarter une option) :
- 1 à 3 ;
- 4 (a) à (c) ;
- 5 (a) à (c) ;
- 6 ;
- 7 ;
- 8 (a) à (d), pour le rayon spectral ;
- 9 (a) à (c) ;
- 10 (a) et (b) ;
- 11 (a) à (c) ;
- 12 ; 13 ; 14 ; 15 ; 16 ;
- 17 (b) et (e) ;
- 18 au J4 ;
- 19 (sans historique, état caché ni drapeau) ;
- 20 (sans itération) ;
- 21 et 23.

**Mesures** (elles décrivent sans écarter) :
- 4 (d) et 5 (d) ;
- 8 : période et demi-vie, et (e) ;
- 9 (d) ; 10 (c) ;
- 11 (d), qui est une lecture soumise au mainteneur ;
- 17 (a), (c), (d), (f), (g) et (h) ;
- 18 à la fiche ;
- 19 et 20 (décomptes) ;
- 22.

| N° | Critère | Ce qui est attendu (seuil ou forme du verdict) | Par quoi on le vérifie | Qui | Quand |
|---|---|---|---|---|---|
| 1 | Cohérence stock-flux (gabarit 1 ; `macro`) — **exigence** | (a) **Lignes proposées par le bloc** : 2 (G = p_t·v_{G,t}, phase 5, après les blocs 4 et 2 ; État −, entreprises « courant » +) ; 6 (Tr) et 7 (T_H, T_F), en phase 6 ; 11a à 11c (intérêts payés, phase 6 ; 11a nulle) ; 19a (montant émis en phase 7, réparti entre souscripteurs selon l'ordre du critère 13). **Propriétaire des lignes 19a, à trancher par le mainteneur (choix à M33)** : (A8) le bloc 9 propose les trois lignes 19a, la part s_CB étant écrite par le bloc 8 en phase 1 et la banque retirée de la phase 7 — recommandée par `monnaie` et `macro` ; **modification** (`temps_comptabilite.md:838`, ADR 0009 l. 84 : décision citant M22 et M29, ADR d'architecture) ; (variante) chaque détenteur propose sa part, le bloc 9 publie le besoin, ordre État → banque centrale → banque fixé par les fiches — **interprétation**, note à la table de la fiche 1. La propriété de 19a-banque dans M31 reste conditionnelle. Reçue : ligne 16 (bloc 8, phase 8 (b)). Contrepartie : ligne 22 (noyau). Signatures de `tab:portes-monnaie` inchangées. Toute ligne ajoutée (part non payée, critère 12) est déclarée avec sa phase et sa signature : c'est un contrat partagé, donc une décision citant M22. (b) B et M^G ne varient que par leurs lignes ; aucun poste n'est obtenu par différence ; V_G = M^G − B est calculée par le stock et par les flux. (c) La contrainte budgétaire de l'État est écrite sur un pas : ΔB − ΔM^G = G + Tr + i_B B/n_a − T_H − T_F − Π^CB. (d) L'identité de la dette (§ 1, point 1), dérivée de `tab:matrice-bilans`, est écrite et contrôlée sur le cas à la main | Matrice des flux de l'option, en tableau. **Cas à la main sur un pas** : dépense publique +10 %, souscription primaire d'un montant décidé par la banque centrale, reliquat par la banque ; lignes 2, 6, 7, 11b, 11c, 16, 19a, 20 et 22 ; B, M^G, Res ; V_G par le stock et par les flux. Si une table change : `uv run python outils/verifier_matrices.py --strict <copie>`, sortie citée avant et après | `macro` ; `monnaie` (19a, 11c, 16) | fiche ; J3 (identités, ε = 1e−12 × S, M22) |
| 2 | Contrats hérités, phases et lectures (§ 1.1 ; ADR 0005, 0008, 0009 ; `macro` ; `monnaie` pour (d)) — **exigence** | (a) Le plan de dépense de la phase 2 ne lit que l'ouverture et la phase 1 (ni plan de la phase 2, ni revenu du pas). (b) La ligne 2 est proposée en phase 5, après les blocs 4 et 2, sur v_{G,t} (M24 (g)) ; le bloc ne lit ni C ni I du pas pour la proposer. (c) **Phase 6 sans ordre interne** : T_H, T_F, Tr et les intérêts se calculent sur l'ouverture, les phases 1 à 5 et les taux de la phase 1. Une assiette qui lirait une ligne de la phase 6 (intérêts reçus, dividendes) exige un ordre interne de la phase 6, donc une décision citant M22 et un ADR. (d) **Phase 7** : le besoin réalisé se lit sur les positions exécutées des phases 5 et 6, avec Π^CB de la phase 1 (l. 495) ; l'ordre interne (critère 13) est déclaré pour report dans `tab:phases` (l. 535). (e) Une variable d'état assise sur un flux prend le montant exécuté ; elle est écrite en phase 9 si nécessaire (M29). (f) Les dates d'effet des trois leviers de `tab:leviers-cadre` sont confirmées, ou une révision est proposée. (g) Chaque taux annuel est classé selon l'ADR 0008, I.2. (h) La matrice des lectures reste triangulaire | Tableau phase → lit / écrit, par option ; triangularité vérifiée à la main | `macro` ; `monnaie` ((d)) | fiche ; J2 (test de triangularité de l'ordonnanceur) |
| 3 | Relevé des lignes de `tab:matrice-flux` (critère d'acceptation de #73 ; `macro`) — **exigence** | Chacune des **28 lignes** reçoit : le bloc qui la propose et sa phase, concordante avec la colonne « Lignes » de `tab:phases` ; ou « contrepartie de règlement » (17, 20, 22) ; ou « montant nul au socle », avec la décision qui le fixe (11a, 19a-ménages, 19b-ménages : M27). **Verdict** : zéro ligne sans bloc qui la propose ; zéro ligne à deux propriétaires. Les lignes dont le propriétaire relève des fiches 7 et 8 (9, 10, 12, 13, 15, 16, 19b-banque, 21 ; la souscription des lignes 19a-banque et 19a-BC) sont reprises de M31 et M32, ou signalées « en attente » avec la fiche qui les tient | Tableau au § 9 de la fiche. Décompte des lignes par `uv run python outils/verifier_matrices.py --strict` (28) ; lecture de la colonne « Lignes » de `tab:phases` (l. 528 à 537). Commandes et sorties citées | `macro` ; `monnaie` (lignes des blocs 7 et 8) | fiche, § 9, après M31 à M33 (jalon 4 de #73) |
| 4 | État stationnaire en forme fermée, sans surdétermination (gabarit 2 ; fiche 6 § 3.E ; `macro`) — **exigence** pour (a) à (c), **mesure** pour (d) | (a) **Trajectoire de référence** des fiches 3 à 6 : volumes en hausse de γ = (1 + g)^{1/n_a} − 1 par pas, prix de (1 + π̄)^{1/n_a} − 1, nominal Γ̄. Chaque grandeur du bloc a sa valeur stationnaire en forme fermée, sans simulation : G/PIB, Tr/PIB, taux d'imposition apparents, solde primaire, solde public, charge d'intérêts brute et nette, dette (critère 5), M^G\*/PIB (critère 11), B_CB/B (avec la fiche 8). Chaque variable d'état a sa valeur stationnaire, d'où se déduit l'état initial résolu, sans préparation. (b) **Comptage** : tableau « équation stationnaire → grandeur qu'elle détermine » pour le socle (blocs 2 à 9). Il comprend le supermultiplicateur (fiche 6 § 3.E, l. 775), l'identité de la dette, la condition de fermeture (critère 6), les ancres de la règle budgétaire (G/PIB, taux d'imposition, transferts, cible de dette ou de solde) et r̄ (fiche 8). **Verdict** : autant d'ancres que d'inconnues. Aucune grandeur ancrée deux fois : viser à la fois un taux d'impôt et B/PIB surdétermine l'état (fiche 6, l. 784). Aucune ancre manquante : une règle sur ΔB ou sur le solde sans ancre de niveau laisse un continuum. L'identité de Domar (§ 1, point 2) est montrée redondante (loi de Walras) et n'est pas comptée comme une équation de plus. (c) **Indépendance envers n_a** : les dépendances par n_a(Γ̄ − 1) (3,9802 %, 3,9671 % et 3,9620 % à n_a = 4, 12 et 52, g = π̄ = 2 %) et par le facteur de fenêtre sont déclarées et chiffrées ; toute autre est écrite avec la condition qui la supprime. (d) **Dépendance à π̄**, chiffrée à π̄ = π\* ∈ {0 ; 2 % ; 10 %}. La non-superneutralité est déclarée (avec C15 de la fiche 8) | Calcul à la main dans la fiche ; script d'état stationnaire de la branche n° 4 bis (P16 (a)). **Au J3** : un pas sans choc depuis l'état résolu laisse les variables d'état du bloc sur leur trajectoire à 1e−10 près en relatif (seuil reconduit) ; ratios du script égaux à ceux du moteur à t = 0 à 1e−9 près (ADR 0005, point 20) | `macro` ; `monnaie` ((b) pour r̄ ; (d) pour C15) | fiche ; n° 4 bis ; J3 |
| 5 | Ratio dette publique / PIB stationnaire (critère de passage de J1, M19 ; `macro`) — **exigence** pour (a) à (c), **mesure** pour (d) | (a) **Définition publiée**. Numérateurs possibles :<br>– dette brute B = B_H + B_Bk + B_CB ;<br>– dette nette de l'encaisse, B − M^G ;<br>– dette consolidée de l'État et de la banque centrale, B − M^G − E^CB = B_H + B_Bk + Res − L^CB.<br>La fiche dit lequel est le ratio du critère de J1, lequel est restitué et lequel entre au test zéro. **Dénominateur** : PIB nominal (§ 1.2). **Unité** : années de PIB. **Fenêtre au test zéro** : stock d'ouverture / (12 × PIB du pas) (M22, lecture (e)). **Fenêtre à la restitution** : stock de clôture / somme des 12 derniers PIB, avec un facteur de fenêtre de 1,0216 à π̄ = 2 % et 1,0638 à 10 % (n_a = 12), et de 1,0250 et 1,0203 à n_a = 4 et 52 (π̄ = 2 %). **Choix** : numérateur du test zéro et du critère de J1 (M19) : dette consolidée B − M^G − E^CB = B_H + B_Bk + Res − L^CB (égale à B − M^G sous E^CB_0 = 0) ; indicateur montré au joueur : dette brute, fin du mois, en % du PIB des 12 derniers mois, à une décimale ; en infobulle, dette nette de l'encaisse et part détenue par la banque centrale ; la dette consolidée n'est restituée que dans la fiche détaillée. Le ratio du test zéro (stock d'ouverture / 12 × PIB du pas) n'est jamais affiché à côté du ratio restitué : le facteur de fenêtre (1,0216 à 2 %, 1,0638 à 10 %) ferait voir deux dettes différentes. La bande de ±0,02 année de PIB (critère 15) porte sur la dette consolidée. (b) **Forme fermée**, tirée de l'identité du § 1 : (B − M^G)/(12 PIB) = ν_H·YD^HS/PIB − (L − D_F)/(12 PIB) + (E^Bk + E^CB)/(12 PIB). Chaque terme est renvoyé à sa fiche (5, 6, 7, 8). (c) **Valeurs publiées** à π̄ = π\* ∈ {0 ; 2 % ; 10 %} et n_a ∈ {4 ; 12 ; 52}, avec le solde stationnaire (Domar) ; la fiche dit quel paramètre fixe le ratio. (d) **Dépendance à π̄** chiffrée : la condition C30 en donne déjà +0,287 année de PIB entre 2 % et 10 %, par le seul côté des entreprises. Pour mémoire, la v1.5 rapporte une première cible de dette rapportée par erreur à 52 fois le PIB annuel (l. 1518, R) : l'unité de la cible se vérifie | Calcul à la main ; le script de la n° 4 bis publie le ratio (M19), ses valeurs égales à celles de la fiche aux chiffres publiés | `macro` ; `monnaie` (E^CB, B_CB) | fiche ; n° 4 bis (critère de J1) ; J3 |
| 6 | Fermeture du niveau d'activité (#44, avec la fiche 8 ; `macro`, `monnaie`, `jeu` pour (d)) — **exigence** | (a) **Au moins deux fermetures instruites** :<br>– (i) **monétaire** : r̄ résolu (condition C3), la règle budgétaire ne visant aucune grandeur d'activité ;<br>– (ii) **budgétaire** : la règle budgétaire porte l'action intégrale sans fuite sur l'écart d'inflation (ou de niveau des prix) et la règle de taux a un r\* paramètre sans action intégrale ; la règle budgétaire porte alors C2, ce qui rouvre M25 quant au porteur de C2. Une réponse budgétaire *proportionnelle* à l'écart d'activité (stabilisateur) est compatible avec (i) : elle laisse G/PIB à son paramètre à l'état stationnaire. Une action intégrale budgétaire sur l'écart d'activité n'est pas une fermeture : sous la verticale de M25, U = U^eq tient dans tout état stationnaire quelle que soit π̄ (maquette de `monnaie` du 04/10/2026 : racine unitaire, arrivée fonction du gain budgétaire ; π̄ ≠ π\* si r\* est un paramètre). Les deux lectures de ϱ̄_L (l. 1865) sont deux inversions de calibration de (i) : elles fixent l'état initial, non la grandeur qui se déplace après un choc permanent. (ii) instruite pour mémoire, non admissible pour un pays joué (avis concordants de `macro` et `monnaie`) ; la retenir rouvre C2 (décision citant M25, sans ADR, qualification d'`architect`).<br>S'y ajoutent les deux lectures de ϱ̄_L (l. 1865) : « taux réel stationnaire posé en paramètre, la dépense publique initiale étant résolue », ou « taux réel résolu à part de la dépense publique dans le PIB donnée ». (b) **Une seule action intégrale par condition stationnaire.** Les conditions stationnaires indépendantes sont π̄ = π\* (ancre nominale) et l'égalité de la demande à y = pr(1 − U^eq)N^pa (une équation en r̄, G/PIB…). U = U^eq n'en est pas une de plus. Deux actions intégrales sur π̄ = π\*, ou une action intégrale sur l'activité, laissent un continuum (r̄, G/PIB) choisi par l'histoire et les gains. **Verdict** : rang plein du comptage du critère 4 (b), et, sur la maquette conjointe, le critère commun des vitesses (critère 7) tenu dans les branches ×0,5 et ×2 de chaque gain, avec ses trois chocs. Le choc de dépense seul ne suffit pas (dans la maquette de `monnaie`, le cumul « C2 + action intégrale budgétaire sur l'inflation » est de plus instable quand les deux gains sont ×2). (c) La fermeture est déclarée avec la fiche 8, à M32 et M33 ; #44 se ferme avec le script de la n° 4 bis. (d) **Persistance**, critère de `jeu` (commentaire de #44 ; `sec:menages` l. 1564), reconduit : après une hausse de la dépense publique ou des transferts aux tours 1 à 12, l'écart de production revient sous la moitié de son pic en **au plus 60 tours**, sous la fermeture retenue | Comptage du critère 4 ; formes fermées. Pour (d), maquette conjointe (blocs 2 à 6 décidés, règle de la fiche 9, règle de taux de la fiche 8), commande et sortie citées, puis scénario au J3 | `macro` ; `monnaie` ; `jeu` ((d)) ; mainteneur | fiche, avec la fiche 8 ; M32-M33 ; n° 4 bis ; J3 ((d)) |
| 7 | Aucune vitesse d'ajustement ne détermine l'état d'arrivée (`docs/exigences.md` § 2.7 ; `macro`) — **exigence** | (a) Ni les gains de réaction de la règle budgétaire, ni les vitesses, ni la durée du pas n'apparaissent dans les formes fermées des critères 4 et 5. **Cas à examiner explicitement** :<br>– (i) **v1.5**, `eq:fiscrule` (l. 1513 à 1518) : facteur proportionnel des achats sur b\* − b, φ_b = 0,3 ; l'écart stationnaire à b\* dépend-il de φ_b ?<br>– (ii) **v2.0**, `update_taxes` (`policies.py` l. 73 à 96 ; actif dans D1, `tax_rule=True`, faits l. 11) : le déficit visé est le déficit de croissance moins 0,20 × l'écart de dette nette (`tax_debt_feedback`, `model.py` l. 297), à la vitesse `tax_adjust_speed` (l. 298) ; l'arrivée n'est exacte que si la croissance estimée (l. 86, lissée et écrêtée) égale la croissance réalisée, à vérifier ;<br>– (iii) **règle de Bohn** : la part reprise du surcroît d'intérêts, φ_B/(g − i + φ_B), est une hypothèse de `monnaie` (fiche 6 § 6.6, l. 1490), à établir ;<br>– (iv) **reprise T9**, sans vitesse.<br>Toute dépendance subsistante est écrite et chiffrée pour un gain divisé et multiplié par 2, avec la condition qui la supprime (terme de tendance, comme à la l. 617). (b) Aucun intégrateur sans ancre (critère 4 (b)) | Calcul à la main. Sur la maquette conjointe (A4), puis au J3, dans chaque branche où une vitesse ou un gain est ×0,5 et ×2 (λ ≤ n_a) : (i) **point fixe** résolu, identique entre branches à 1e−6 près en relatif, avec π̄ = π\* ; (ii) **module dominant < 1**, hors racine nominale et hors état inerte déclaré, aucun n'entrant dans un ratio testé ; (iii) **arrivée simulée** après chacun de trois chocs — dépense publique +1 % aux tours 1 à 12 ; marche de π\* de +1 point ; π^e +1 point au tour 0 — : écart relatif de chaque ratio au point fixe de sa branche, et entre branches, d'au plus **1e−6 après H = max(720 ; 20 demi-vies de la racine dominante mesurée) pas**, H déclaré avant l'essai ; (iv) après une dépense publique +1 % permanente, arrivée au point fixe déplacé à moins de 1e−3 en au plus 20 demi-vies (C36 (ii-b), rédaction de M28). Le choc « dépense publique » est un déplacement de l'ancre de dépense de la règle de référence, ou du levier, défini une fois pour les fiches 6, 8 et 9. L'amendement de la fiche 6 (2 160 pas) reste en vigueur. Lieu d'exécution des simulations à horizon H (CI, job séparé ou hors CI, sortie publiée) fixé au plan de J3 (`architect` : au plafond de 52/12 ms par pays-pas, H = 12 640 pas coûte 54,8 s par simulation) | `macro` | fiche ; J3 |
| 8 | Stabilité (gabarit 3 ; `macro` ; `monnaie` pour (d) et (e)) — **exigence** pour (a) à (d) quant au rayon spectral, **mesure** pour la période, la demi-vie et (e) | (a) **Instabilités connues** (`archive/faits_mesures_G_K.md` l. 225 à 243), non réintroduites sans fait nouveau :<br>– n° 2 : avances au Trésor sans intérêt ;<br>– n° 3 : coupon de consolidation au taux du moment, pour toute variante de durée (critère 10) ;<br>– n° 5 : dividende de trésorerie sans règle fiscale (v2.0 : `treasury_rebate_speed`, `model.py` l. 203, interdit avec `tax_rule`, l. 379 et 380) ;<br>– n° 4 : estimateur de r\* sans ancre, si la fermeture lit un taux ;<br>– n° 15 : un plafond produit un cycle (v1.5, facteur écrêté à [0,6 ; 1,6], l. 1515 ; v2.0, exécution des dépenses `rhoG` écrêtée à [0,2 ; 1], `model.py` l. 1244) ;<br>– n° 16.<br>Résultats de maquette v3 discutés (fiche 6 § 6.6, maquette de `monnaie` ; ce ne sont pas des faits de la première tentative) : une cible intégrale de B/PIB est explosive pour tous les ζ testés ; une règle de Bohn localement stable manque l'arrivée dans deux cas sur quatre ; T9 suffit. (b) **Boucle propre** (dette et règle), revenus privés et taux exogènes : modules strictement inférieurs à 1 à la calibration et pour chaque gain multiplié par 0,5 et par 2 ; demi-vie et période publiées. (c) **Boucle conjointe avec les blocs 2 à 6** (N1 à N7, T2 à T4, P1 à P3, H2 à H6, S-ζ et F), taux exogène : rayon spectral strictement inférieur à 1 à la calibration (exigence) ; aux gains ×0,5 et ×2, module, demi-vie et période publiés (mesure) ; θ_H effectif sous la règle retenue (critère 14). (d) **Boucle complète avec la règle de taux de la fiche 8** : C36 (critère 9 (c)). (e) Le couple « règle de taux – règle budgétaire » est situé dans la classification de Leeper (1991) en politiques actives et passives (cité par `monnaie`, fiche 6 § 6.6, résumé lu) | Faits § 6 à 8, puis `tab:instabilites`. Valeurs propres calculées à la main ou par `uv run python`, commande et sortie citées | `macro` ; `monnaie` ((d), (e)) | fiche ; J3 |
| 9 | Charge d'intérêts : C23, C37 et C36 (fiches 5 et 6 ; `macro`, `monnaie`, `jeu` pour (d)) — **exigence** pour (a) à (c), **mesure** pour (d) | (a) **C23** : la règle de référence déclare sa réponse à la charge d'intérêts (forme, délai en tours, part reprise à fréquence nulle), et le signe de long terme du canal rentier qui en résulte (`sec:menages` l. 1546). (b) **C37** : la règle de référence (test zéro, pays non joués) reprend aux agents privés, à fréquence nulle, le surcroît d'intérêts sur B qu'entraîne une hausse durable du taux. Elle doit garantir que C36 (i) tient, tous canaux réunis, et que l'arrivée existe après G +1 % permanent. (c) **C36**, rédaction de M28 (`investissement.md` l. 1849) :<br>– (i) gain statique de la demande totale au taux réel strictement négatif ;<br>– (ii-a) r̄ et π̄ résolus par point fixe à 1e−6 près en relatif dans chaque branche ×0,5 et ×2 de toutes les vitesses, avec π̄ = π\* ;<br>– (ii-b) arrivée simulée après G +1 % permanent, à moins de 1e−3 en relatif, en au plus 20 demi-vies de la racine dominante ;<br>– (iii) module dominant inférieur à 1, hors racine nominale et hors état inerte déclaré, **et** (ii-b) satisfait.<br>C36 est mesurée à la fiche sur maquette, avec ζ de 4 à 8 (hypothèse de M28), puis au J3 sur le moteur. (d) **Régime « intérêts financés par le déficit »** (pays joué) : déclaré comme dominance budgétaire (Leeper, 1991), non comme référence ; ses conséquences (gain positif de la demande au taux, divergence de C2) sont chiffrées sur la maquette ; sa disponibilité pour le joueur est soumise à `jeu` et au mainteneur | Maquette conjointe (fiches 2 à 6 décidées, règle de la fiche 9, règle de taux de la fiche 8), commandes et sorties citées ; au J3, test C36 de la fiche 6 (§ 9.6). Une seule maquette conjointe, versionnée au compte rendu, sert aux critères 6 (d), 11, 12, 15 et 16 de la fiche 8 et aux critères 6, 8 (c) et (d), 9 et 18 de cette fiche. | `macro` ; `monnaie` ; `jeu` ((d)) | fiche, avec la fiche 8 ; M32-M33 ; J3 |
| 10 | Durée de la dette : C24 (fiche 5 ; ADR 0005, § Conséquences ; `macro`, `monnaie`) — **exigence** pour (a) et (b), **mesure** pour (c) | (a) **Variante de référence** : toute la dette au taux de la dernière date de décision (M22 ; l. 548). (b) **Au moins une variante** avec une part à taux fixe ou une maturité moyenne (v1.5, `eq:iapp`, l. 1484 à 1490 : taux apparent à mémoire, fraction refinancée 1/T̄ plus déficit/B, dette consolidée avec la banque centrale). Pour chaque variante :<br>– le contrat qu'elle rouvre (décision citant M22 ; lignes 11a à 11c ; sortie de `verifier_matrices.py`) ;<br>– ses variables d'état : un taux apparent agrégé, de valeur stationnaire i_B sous taux constant, sans historique de cohortes ;<br>– son effet sur la vitesse du canal rentier (C24) et sur C36 ;<br>– l'examen de l'instabilité n° 3.<br>(c) La part détenue par la banque centrale « se reprice » immédiatement (v1.5, l. 1493) : frontière avec la fiche 8, mesurée | Formes fermées ; maquette pour (b), commande et sortie citées | `macro` ; `monnaie` | fiche ; M33 |
| 11 | Encaisse du Trésor M^G\* (#26, point 3 ; P2 ; ADR 0005, point 13 ; `macro`) — **exigence** pour (a) à (c), **mesure** pour (d) et (e) | (a) **Une règle de M^G\*** qui donne un ratio M^G\*/PIB stationnaire : option sans paramètre : M^G\*_t = paiements bruts exécutés du pas (G_t + Tr_t + i_B B_t/n_a), lus en phase 7 ; option à paramètre : m × paiements bruts, m ∈ ]0 ; 1] déclaré. Une encaisse de niveau fixe est écartée sauf fait nouveau : sous croissance nominale, la dépense de la phase 5 finit par la dépasser. L'illustration de #26 est reproduite : rationnement après 5,69 ans (croissance nominale de 4 %, dépense égale à 80 % des paiements bruts) à 25,80 ans (2 %, 60 %). La règle ne lit que des grandeurs disponibles en phase 7. (b) **Contrôle de caisse inactif à l'état stationnaire, marge chiffrée.** M^G_t = M^G\*_{t−1} couvre les paiements qui précèdent les recettes. Avec M^G\*_t = m × P_t (P : paiements bruts du pas), deux lectures du contrôle dans la phase 6, sans ordre interne, sont à instruire :<br>– (i) **net par phase** : m ≥ Γ̄ × max{s_G ; 1 − T/P}, s_G étant la part de G dans P ; à g = π̄ = 2 % et n_a = 12, Γ̄ − 1 = 0,3306 % ;<br>– (ii) **brut, paiements avant recettes** : m ≥ Γ̄ > 1, ce qui contredit la borne de la l. 502 (« n'excède pas les paiements bruts d'un pas ») et demande une décision citant M22.<br>La lecture (i) est la seule compatible avec une phase sans ordre interne ; elle s'écrit dans `sec:cadre-caisse` pour tous les payeurs (fiche 5 § 9.8). Sous m = 1, marge 1 − Γ̄ s_G publiée ; une hausse de dépense d'un tour au suivant supérieure à 1/s_G − 1 est rationnée au premier tour (critère 12 (b)).<br>(c) **Contrat partagé** : la l. 502 et la l. 2064 disent que M^G\* « n'est pas un paramètre ». La fiche déclare si sa règle introduit un paramètre du bloc ; `architect` qualifie l'effet sur l'ADR 0005 (point 13). Avis de `monnaie` : m = 1 est une interprétation du point 13 ; m libre en est une modification. **Qualification d'`architect`** : m = 1 est une **interprétation** (annotation datée de l'ADR 0005, point 13) ; m libre : deux lectures de la l. 2064, le mainteneur tranche ; m > 1 est une **modification**. Contrôle de caisse : la lecture nette est une **interprétation à deux conditions** — première condition, la banque est exclue (découvert intra-pas, l. 485, ADR 0005, point 10) ; seconde condition, la contrainte nette est tenue par le plan du payeur en phase 2, le noyau ne faisant qu'une vérification de fin de phase ; sinon **modification** (décision citant M22 et M29, ADR d'architecture). Règle de M^G\* et lecture du contrôle de caisse décidées ensemble, à M33 (**à trancher par le mainteneur**). (d) **P2**, deux lectures :<br>– (i) garder M^{G\*}, marque de cible cohérente avec une encaisse visée à chaque pas, renommer « encaisse stationnaire » en « encaisse visée » et l'expliquer dans `tab:symboles` (l. 2410) ;<br>– (ii) noter la valeur stationnaire par la barre.<br>Avis au § 5. (e) Effet de M^G\* sur les réserves : une hausse de M^G\* de x réduit Res − L^CB de x à la clôture, à B_CB et E^CB donnés (identité A9 ; légende de `tab:leviers-cadre`, l. 2024). | Forme fermée ; cas à la main sur 24 tours de croissance nominale ; au J3, aucun rationnement sur 720 pas | `macro` ; `monnaie` ((e)) ; `architect` ((c)) ; `docwriter` ((d), dans la section) | fiche ; M33 ; J3 |
| 12 | Ordre des paiements de l'État et parts non payées (#26, point 1 ; fiche 5 § 9.8 ; ADR 0005, points 10, 12 et 13 ; `macro`, `monnaie` pour (b) et (c)) — **exigence** | (a) **Ordre de priorité déclaré** : ligne 2 (phase 5) ; lignes 6, 11b et 11c (phase 6) ; ligne 16 négative (phase 8 (b)). (b) **Placement raté** (limite de détention de la banque, C22 de la fiche 7) : M^G clôt sous M^G\*. La fiche dit quelle dépense du tour suivant est rationnée et par quel mécanisme, par exemple un plafond du plan sur l'encaisse d'ouverture, sur le modèle du budget des ménages ; le signal précède d'un tour (l. 502). (c) **#26, point 1, côté État** : montrer à la main que sous α l'émission compte −Π^CB, calculé en phase 1, si bien qu'une perte de la banque centrale est couverte sauf placement raté. Dans ce cas, la part non versée est une ligne nommée (versement rationné, E^CB réduit) ou une règle de recapitalisation, décidée avec la fiche 8. (d) **Impôt non recouvré** (fiche 5 § 9.8 ; entreprises, D_F ≥ 0) : ligne nommée du bloc 9, sans créance fiscale, instrument absent. (e) Aucun découvert implicite, aucune avance, aucun intérêt impayé capitalisé dans le principal (pratique de la v1.5, l. 1522). (f) Chaque ligne nouvelle passe par une décision citant M22 et une sortie de `verifier_matrices.py --strict` avant et après (`cmp`) ; toutes sont inactives à l'état stationnaire, marge chiffrée | Cas à la main, postes après chaque phase : (i) placement raté de moitié sur un tour ; (ii) perte de la banque centrale égale à deux fois M^G, avec la condition de Π^CB ≥ 0 qu'elle viole (fiche 8, critère 2 (b)), combinée à un placement raté (sinon l'émission couvre la perte) ; (iii) impôt des ménages supérieur à leurs dépôts | `macro` ; `monnaie` ((b), (c)) ; `architect` ((f)) | fiche ; J3 ou J4 (scénarios adverses) |
| 13 | Phase 7, émission et placement (C25 ; frontière dette publique ; `macro`, `monnaie`) — **exigence** | (a) **C25, ordre interne** : besoin de l'État, puis souscription primaire et achats décidés de la banque centrale, puis reliquat de la banque (19a-banque = besoin − 19a-BC ; C19). La ligne 19b n'est jamais en acheteur passif. La Q5 de la fiche 5 est sans objet (B_H ≡ 0). La variante de Tobin est transmise au J6. Propriétaire unique de chaque ligne 19a déclaré (critère 3). **Propriétaire des lignes 19a, à trancher par le mainteneur (choix à M33)** : (A8) le bloc 9 propose les trois lignes 19a, la part s_CB étant écrite par le bloc 8 en phase 1 et la banque retirée de la phase 7 (s_CB ∈ [0 ; 1] contrainte de domaine déclarée, jamais un écrêtage ; limite C22 éventuelle et part refusée du scénario publiées par la banque à l'ouverture ; conditions de `macro`) — recommandée par `monnaie` et `macro` ; **modification** (`temps_comptabilite.md:838`, ADR 0009 l. 84 : décision citant M22 et M29, ADR d'architecture) ; (variante) chaque détenteur propose sa part, le bloc 9 publie le besoin, ordre État → banque centrale → banque fixé par les fiches — **interprétation**, note à la table de la fiche 1. La propriété de 19a-banque dans M31 reste conditionnelle. (b) La formule d'émission des l. 499 et 500 est reprise, ou une révision est proposée par une décision citant M22. (c) **i_B** (prime : `monnaie`). Règle déclarée parmi :<br>– (i) i_B ≡ i_CB du tour, grandeur dérivée : aucune variable d'état, aucun siège du bloc 9 en phase 1, « dernière date de décision » = phase 1 du tour, prime nulle déclarée ;<br>– (ii) i_B = i_CB + écart constant, paramètre avec son motif ;<br>– (iii) i_B = i_CB d'ouverture, variable d'état.<br>Pour chacune : délai du premier flux des lignes 11b et 11c (0 sous (i), 1 sous (iii) ; `tab:leviers-cadre`) ; position par rapport au corridor, i_res ≤ i_B ≤ i_CB, déclarée (cohérence avec une future règle de portefeuille, J6) ; signe de Π^CB (fiche 8, critère 2 (b)). La prime endogène (v1.5 `eq:spread`, l. 1223) relève du J6. Option (β), le bloc 9 écrit i_B en phase 1 : **modification** (cycle bloc 8 → 9 → 8 en phase 1 ; décision citant M22, M29 et M30, ADR d'architecture). Qualifications d'`architect` : (i) est une **interprétation**, `tab:phases` inchangée, à condition d'être déclarée une seule fois dans `sec:finances_publiques` comme identité de notation du socle, sans label `eq:` ni équation exécutée, tout lecteur lisant i_CB ; (iii) contredit probablement la l. 483 (hypothèse à vérifier). Recommandation commune de `macro` et `monnaie` : (i). Choix à M33, **à trancher par le mainteneur**. (d) La limite de détention de la banque (C22), si la fiche 7 la retient, et sa conséquence (critère 12 (b)). (e) Report dans `tab:phases`, ligne 7, sans cycle | Tableau de la phase 7 (qui lit, qui écrit, quelle ligne) ; triangularité | `macro` ; `monnaie` | fiche, avec les fiches 7 et 8 ; M31 à M33 |
| 14 | Grandeurs lues par les blocs 5 et 6 (fiche 5, critère 10 ; fiche 6 § 9.8 ; `macro`) — **exigence** | (a) **Tableau des grandeurs lues**, chacune avec sa phase et sa date :<br>– par le bloc 5 : T_H (ligne 7), Tr (ligne 6), i_B (ligne 11a, nulle), ligne 19a-ménages (nulle) ;<br>– par le bloc 6 : G (ligne 2, phase 5) et T_F (ligne 7).<br>Les formes symboliques de H7, de F3 et de F4 sont conservées : la fiche 9 choisit ses règles sans réécrire les fiches 5 et 6. (b) **Impôt des entreprises** (fiche 6 § 9.8, l. 2291) : assiette avec la ligne 8 comptable ; T_F tombe sur Div_F, jamais sur l'investissement ; rattrapage au tour n + 1 ; assiette calculable sans lire la phase 6. (c) **Hypothèses provisoires remplacées** (fiche 5, critère 10 (c)) : la boucle conjointe de `sec:menages` (l. 1542) est « sans impôts ni transferts », avec θ_H = 0,8 ou 1. La fiche publie θ_H effectif sous sa règle et la part m_G de la propension totale m (fiche 5, critère 6 ; réserve 3 de la fiche 2), puis refait, ou fait refaire, le rayon de la boucle conjointe. (d) Aucune anticipation ricardienne (l. 1638), sauf option déclarée. (e) Allocations de chômage et cotisations (l. 977) : options de Tr et de T_H, avec leur assiette et leur phase | Tableau (bloc, ligne, phase, date) ; maquette conjointe pour (c) | `macro` | fiche |
| 15 | Test zéro des ratios du bloc (`docs/exigences.md` § 2.6 ; O1 ; `macro`) — **exigence**, mesurée au J3 | Sur 60 ans (720 pas) sans choc depuis l'état résolu, pour plusieurs graines, la moyenne par blocs de 5 ans (60 pas) de chaque ratio reste dans sa bande. **Bandes proposées**, à confirmer avec O1 avant l'essai (M19) :<br>– dette publique / PIB (numérateur du critère 5) : **±0,02 année de PIB**, en absolu, parce que c'est une différence de stocks (critère 5 (b)) ;<br>– solde public / PIB sur 12 tours : ±0,2 point ;<br>– M^G\*/PIB : ±2 % en relatif ;<br>– B_CB/B : ±1 point, bande commune avec la fiche 8.<br>**Aucune part non payée** ni rationnement de la dépense sur les 720 pas. B_H/V_H est sans objet (B_H ≡ 0). Pour mémoire, sans valeur de référence :<br>– la v1.5 rapporte une dette passée de 0,61 à 0,04 en 60 ans sans règle, et de 0,40 à 0,45 avec `eq:fiscrule` (l. 1518, R) ;<br>– la v2.0 rapporte une dette publique nette de 62,4225 % du PIB dans le contrôle de F3 (faits § 8, R).<br>Toute dérive depuis l'état résolu est un défaut | Au stade de la fiche, le préalable (critère 4) ; au J3, test zéro du socle | `macro` ; mainteneur (bandes) | J3 |
| 16 | Bornes (gabarit 6 ; #38, lecture (ii) ; `CONVENTIONS.md` § 2.4 ; `macro`) — **exigence** | (a) **Chaque borne est classée.** M^G ≥ 0 est une contrainte de conservation (sans avances). G^plan ≥ 0, Tr ≥ 0 et un taux d'imposition dans [0 ; 1[ sont des conditions déclarées, jamais des écrêtages. Un plafond du plan de dépense sur l'encaisse (critère 12 (b)) est une borne à seuil libre dont le seuil est une base (lecture (i) de la fiche 5, § 9.2). Exemples de la première tentative à classer :<br>– v1.5 : facteur écrêté à [0,6 ; 1,6] (l. 1515) ;<br>– v2.0 : multiplicateur d'impôt dans [0 ; 3] (`model.py` l. 296 ; `policies.py` l. 93) ; taux d'impôt au plus 0,90 (`policies.py` l. 32) ; croissance estimée dans [−0,10 ; 0,20] (l. 86) ; exécution des dépenses dans [0,2 ; 1] (`model.py` l. 1244) ; résultat de la banque centrale tronqué à ses valeurs positives (l. 1208), écarté par M22 (d).<br>(b) Un mécanisme est préféré à une borne. (c) **Instabilité 15** : aucune borne active à l'état stationnaire ni dans les scénarios O2 (dépense publique +1 % et +5 %, taux d'imposition +1 point). Scénarios adverses : placement raté de moitié pendant 12 tours ; dépense doublée pendant 12 tours (#53). Une borne activée cesse de l'être **au plus tard 12 tours après la fin du choc**, sans réactivation (seuil reconduit) | Décompte et classement des bornes par option ; cas à la main ; scénarios au J3 ou au J4 | `macro` ; mainteneur (seuil de (c)) | fiche ; J3 ou J4 |
| 17 | Lisibilité pour le joueur (gabarit 5 ; `macro`, à soumettre à `jeu`) — **exigence** pour (b) et (e), **mesure** pour (a), (c), (d), (f), (g) et (h) | (a) **Indicateurs au tour**, chacun avec définition, unité, dénominateur et fenêtre : dette brute et nette / PIB ; soldes primaire et public / PIB (12 tours) ; charge d'intérêts nette / PIB et i_B ; émission du tour par souscripteur ; encaisse en tours de paiements ; part de la dette détenue par la banque centrale ; dépense demandée et exécutée ; parts non payées. Les niveaux normaux sont publiés par le script de la n° 4 bis, avec le facteur de fenêtre d'un stock en u.m. (1,0216 à 2 %). **Indicateur de soutenabilité** (avis de `jeu`, définition de `macro`) : solde primaire stabilisant, défini comme i_B B/n_a − Π^CB − (Γ^e − 1)(B − M^G) par pas (égal à [i/n_a − (Γ^e − 1)](B − M^G) sous i_B = i_res = i_CB et E^CB = 0), en part du PIB sur 12 tours, et écart au solde primaire réalisé ; écart i_B − croissance nominale annuelle, sur 12 tours. Le signe de r − g est un point contesté (critère 22). (b) **Délais en tours entiers** :<br>– du levier au premier flux : délai 0 (`tab:leviers-cadre`) ;<br>– vers les ménages et les entreprises : fiches 5 et 6 (budget au tour n + 1 ; dividendes au tour n) ;<br>– puis vers le solde et la dette ;<br>– du taux directeur à la charge d'intérêts (lignes 11b, 11c, 16) : délai 0.<br>La contrepartie est visible le même tour ; aucun effet plus rapide que le tour sans contrepartie. (c) Tableau levier → indicateur → délai → contrepartie, pour les trois leviers et pour le taux directeur vu du budget. (d) **Ampleur** : effet d'une hausse d'un point du taux d'imposition des ménages et d'une dépense publique +1 % et +5 % pendant 12 tours sur le solde, la dette et la production, perceptible à l'échelle d'une partie. **Seuils de `jeu`** (mesure, avant l'essai) : (d1) taux d'imposition des ménages +1 point : solde public / PIB (12 tours) en hausse d'au moins 0,2 point au tour 12, écart de production d'au moins 0,1 % avant le tour 12 ; (d2) dépense publique +1 % pendant 12 tours : écart maximal de production d'au moins 0,1 % ; +5 % : d'au moins 0,5 % ; (d3) dépense publique +5 % pendant 12 tours : dette / PIB restituée en hausse d'au moins 0,5 point au tour 12, et toujours au-dessus du contrôle au tour 60 en configuration de pays joué (aucun effacement gratuit de la dette) ; sous la règle, le tour où l'écart repasse sous la moitié de son maximum est publié. (e) **Gratuité de la sur-commande** (#53 ; `production.md` l. 914 ; `menages.md` l. 1468) : la part non servie de la dépense est soit supprimée, soit rendue visible et coûteuse ; la fiche propose le mécanisme, `jeu` le juge, essai au J4. (f) Dominance budgétaire (critère 9 (d)) : lisible si l'indicateur de soutenabilité de (a) et la décomposition du revenu des ménages par source sont restitués (avis de `jeu`). (g) Signes contre-intuitifs déclarés : hausse de taux qui accroît le revenu des ménages ; changement de cible. (h) **Perceptibilité à l'échelle d'une partie** (mesure ; avis de `jeu`, accepté par `macro` et `monnaie`), définie avant l'essai : (i) au moins un indicateur du tableau du tour s'écarte du contrôle apparié d'au moins **deux crans d'affichage** (0,2 point pour un taux, un glissement ou un ratio affiché en % à une décimale ; 0,2 % pour un niveau) dans les **12 tours** qui suivent la décision ; (ii) le pic de l'écart survient au plus tard au **tour 24** ; (iii) toute dynamique de demi-vie supérieure à **60 tours** est déclarée, avec l'écart résiduel qu'elle laisse au tour 60 sur le glissement et sur la production. Un écart résiduel supérieur à un cran au tour 60 est signalé à `jeu` comme transition non attribuable. | Tableau du § 9, « Interfaces ». Exemple daté à la main : dépense publique +1 % aux tours 1 à 12, avec G, émission, M^G, solde, dette / PIB et production aux tours 1, 2, 3, 4, 9, 13, 14, 18 et 24. Avis de `jeu` (§ 7) ; au J4, scénario apparié (O2) | `jeu` ; `macro` (exemple daté) | fiche ; J4 |
| 18 | Signe net d'une hausse de taux (#56) — **critère partagé, écrit une seule fois au critère 15 de la fiche 8** (texte commun de `macro` et `monnaie`) — **mesure** à la fiche, **exigence** au J4 | La fiche 9 fournit la règle budgétaire de référence (C37), la règle de i_B et la configuration de pays joué (critère 19). Pour chaque règle candidate, elle publie P1 et P2, et la configuration de pays joué du critère 15 de la fiche 8, sur la maquette conjointe, avec la part du surcroît d'intérêts reprise à fréquence nulle (critère 9 (a)). La propriété ne se modifie qu'à la fiche 8, par un amendement commun adopté avant l'essai | Maquette conjointe ; scénario apparié au J4 | `macro` ; `monnaie` | fiche (mesure) ; J4 (exigence) |
| 19 | Simplicité, empreinte sur l'état, déterminisme, leviers sans drapeau (gabarit 6 et rubrique 9 ; principe de simplicité ; `macro`, `jeu` pour les leviers) — **mesure** (décompte) et **exigence** (sans historique, état caché ni drapeau) | **Décompte** par option : paramètres, bornes, variables d'état, lignes et phases touchées. Chaque élément est justifié ; chaque variable d'état a son unité et sa valeur stationnaire. **Aucun historique ni état caché** : `update_taxes` lit les quatre dernières semaines d'un historique (`policies.py` l. 82 et 83) et un `getattr` avec valeur par défaut (l. 86), ce qui est exclu (ADR 0002). **Une seule règle par mécanisme** : `fiscal_rule`, `tax_rule`, `fiscal_on_net_debt` et `treasury_redeem_all` (`model.py` l. 202, 206, 249 et 294) ne sont pas repris comme drapeaux. **Règle de référence et leviers du joueur** : le joueur fixe directement la dépense, le taux d'imposition des ménages et les transferts ; « suivre la règle » est une **valeur de chaque levier**, non un drapeau de mode, et la prescription de la règle est restituée à chaque tour (comme le taux indiqué par la règle, fiche 8, C9). La partie commence sur la règle, depuis l'état résolu. L'unité de chaque levier est telle qu'un levier inchangé laisse l'état stationnaire (part du PIB tendanciel ou volume indexé, Q10). Quand le joueur ne suit pas la règle, le surcroît d'intérêts est financé par le déficit ; c'est déclaré et restitué (critère 9 (d), critère 17 (f)). Avis de `jeu` : préférence pour cette forme. La règle de référence agit par ses instruments déclarés ; un levier fixé par le joueur sort de la règle pour cet instrument, et les conséquences (par exemple le surcroît d'intérêts financé par le déficit sous T9 si le taux d'imposition est fixé) sont restituées. (exigence) un levier inchangé laisse l'état stationnaire ; un plan de dépense en u.m. fixe est écarté. « Le joueur peut la désactiver » (v1.5, l. 1518) n'est pas repris comme drapeau ; la forme est soumise à `jeu`. Aucun tirage, ou un tirage par la graine du pays, déclaré | Tableau de décompte ; liste des variables d'état | `macro` ; `jeu` (leviers) | fiche ; J2 (reprise exacte) |
| 20 | Coût de calcul (gabarit 4 ; invariant 3 ; `macro`) — **exigence** (aucune itération) et **mesure** (décompte) | Aucune itération ni optimisation à chaque pas (ADR 0002). Un placement qui ferait monter le taux « jusqu'à équilibre » (v1.5, l. 1525) est écarté ou écrit en forme fermée. Décompte des opérations par pas. **Part indicative proposée** : 0,48 ms par pays-pas, celle des blocs 2 à 6 ((52/12 − 0,5)/8) | Décompte dans la fiche ; au J3, `tests/invariants/test_budget.py` | `macro` ; `audit` | fiche ; J3 |
| 21 | Notation (`CONVENTIONS.md` § 5.2 ; décision du 02/10/2026 sur #23 ; `macro`) — **exigence** | Chaque symbole a un seul sens ; aucune collision avec les indices réservés (c, j, k, h, t ; s, ℓ, u) ni avec `tab:symboles`. **Déjà pris** : S, s, m, A, β, θ_H, r, G (dépense et marque de secteur), T_H, T_F, T^e_F. Le symbole du ratio de dette est harmonisé avec le b de `sec:menages` (l. 1546), sur la dette consolidée, numérateur du canal rentier (le b de la l. 1546, « dette publique nette détenue hors banque centrale », omet Res − L^CB) : précision de définition d'une section décidée, rédigée par `docwriter`, approuvée par le mainteneur. M^G\* suit la lecture retenue de P2 (critère 11 (d)). Un taux d'imposition, un gain de réaction et une cible de dette reçoivent des symboles vérifiés par `grep -c -F` sur le `.tex`, sortie citée | Liste des symboles confrontée à `tab:symboles` | `macro` ; `docwriter` (section) | fiche ; section proposée |
| 22 | Calibrabilité et faits établis (`macro`) — **mesure** | Les paramètres se calibrent sur des ordres de grandeur établis, chacun avec sa source retrouvée et sa date : dette publique / PIB, solde, charge d'intérêts, G/PIB, transferts/PIB, taux de prélèvement, encaisse du Trésor en mois de dépense. Statistiques publiques à retrouver ; aucune configuration n'est associée à un pays réel. Points **contestés**, séparés : multiplicateur budgétaire ; signe de r − g. **Sources**, existence vérifiée, **non lues à ce jalon** :<br>– Domar (1944), *American Economic Review* 34, 798-827 ;<br>– Lerner (1943), « Functional Finance and the Federal Debt », *Social Research* 10 (pages non vérifiées, 38-51 ou 38-57 selon les sources) ;<br>– Blanchard (2019), *American Economic Review* 109(4), 1197-1229.<br>Lues par `monnaie` (fiche 6 § 6.6), en résumé seulement, non lues par `macro` :<br>– Bohn (1998), *Quarterly Journal of Economics* 113(3), 949-963 ;<br>– Leeper (1991), *Journal of Monetary Economics* 27(1), 129-147.<br>Godley et Lavoie (2007), chap. 3 et 4 (secteur public des modèles SIM et PC), connus par les reproductions `sfcr` déjà citées dans la spécification, livre non lu. Blanchard (1990), cité par la v1.5 (l. 1507), n'a pas été retrouvé à ce jalon. Un résultat de la v1.5 ou de la v2.0 n'est pas un fait établi | Sources citées ; « non trouvée » le cas échéant | `macro` | fiche ; J3 (calibration) |
| 23 | Remesure des faits de la première tentative (décision P1 du 03/10/2026 ; `CONTEXT.md` ; `macro`) — **exigence** de procédure | (a) Chaque fait cité porte son statut ; les faits établis sur D1 ne sont pas remesurables. (b) Toute remesure (statut V) passe par un script d'`outils/` qui exécute le prototype dans un processus séparé, jamais par import (invariant 4). Le script est revu par `audit` (circuit 3), avec ses critères écrits avant l'essai et son verdict publié même défavorable. (c) Un fait V sur le prototype v2.0 reste un fait de la première tentative. (d) Les lectures de code (L) citent fichier et ligne, avec la branche active et les coefficients effectifs. Dans D1 : `tax_rule=True`, `fiscal_rule=False`, `treasury_redeem_all=True` (faits l. 11). Les valeurs dans D1 de `tax_debt_feedback`, `tax_adjust_speed`, `gov_cash_ratio`, `b_target` et `phi_Bbank` ne sont pas établies par la synthèse. Les chiffres du prototype de la v1.5 sont rapportés (R) | Liste des faits et statuts ; commande, sortie et commit de chaque script | `macro` ; `coder` ; `audit` | fiche (jalon 2) |

### Amendements adoptés

Décisions du mainteneur du 04/10/2026, prises avant l'instruction, sur les questions des experts (validation groupée des critères des fiches 7, 8 et 9, P14) :

- **Critères** : la liste est validée telle qu'amendée par la relecture croisée du 04/10/2026 (avis de `macro`, `monnaie` et `jeu` ; qualifications d'`architect`), avec la nature de chaque critère (exigence ou mesure) ; les seuils reconduits et les seuils de `jeu` sont adoptés.
- **Options marquées « à trancher par le mainteneur » au choix M31 à M33** (propriétaire des lignes 19a, règle de i_B, règle de M^{G*} et lecture du contrôle de caisse, forme de E^CB) : instruites telles qu'écrites, avec leur qualification (interprétation ou modification) ; elles se décident aux décisions de fiche, non à cette validation.
- **Critère 18 (#56)** : renvoi au critère 15 de la fiche 8, dont la branche (A) de référence est la règle de taux en vigueur plus un écart d'un point à la prescription.

## 3. Options

*Rédigé par `macro` (expert pilote), 04/10/2026, sur l'état `3edff4e` (branche `claude/j1-monnaie-etat`, PR #77). Les numéros de ligne de la spécification renvoient à `docs/specification/nations_et_marches.tex` à cet état. Les numéros de ligne de la v1.5 renvoient à `archive/v1.5/Nations_et_Marches_v1_5.tex`.*

### 3.0 Conventions, maquette conjointe, mesures et littérature

**Découpage par question** (gabarit § 3).
- Les options A (v1.5) et B (v2.0) sont instruites en entier.
- Sur Q5 à Q10 et Q12, les contrats hérités (M22 à M31) ne laissent qu'une forme compatible, à une lecture près chacune. Cette forme est instruite une fois, comme socle commun (§ 3.N).
- Les options nouvelles diffèrent sur Q1 à Q4 (règle de référence, instrument, fermeture, charge d'intérêts) et sur Q8 pour l'assiette de T_H. Il y en a six :
  - **C** : reprise réelle T9, en quatre variantes d'assiette : C-WB, C-Y, C-Yhi, C-HS ;
  - **D** : rappel proportionnel de la dette (forme de Bohn), ajouté à C ou seul ;
  - **E** : leviers tenus, forme SIM/PC de Godley et Lavoie. C'est le « pays joué » des fiches 6 et 8 ;
  - **F** : fermeture budgétaire sur le taux neutre (nouvelle) ;
  - **L** : finance fonctionnelle (Lerner), instruite par argument ;
  - **V** : variante de durée de la dette, à taux apparent ; elle se combine avec C.

**Maquette conjointe unique** (critère 11 de la fiche 8 ; critères 6, 8 (c) et (d), 9 et 18 de cette fiche).
- Fichier : `m9.py`, extension de la maquette indépendante de `macro` pour la fiche 8 (`maquette_f8_macro/m.py`), copiée dans le bloc-notes de la session (`…/scratchpad/maquette_f9/`). Empreinte : `sha256sum m9.py`, début `cbe8da70131a4464`.
- Avec les paramètres par défaut, m9.py reproduit m.py à 9,7e−14 près en relatif sur 300 pas, dans trois réglages (`cmp_m.py`). C'est donc le même code pour les fiches 8 et 9 ; les options du bloc 9 s'activent par paramètre.
- Elle exécute les équations décidées :
  - N1 à N11, T1 à T6, P1 à P4, H2 à H7, S1 à S7, F1 à F4 ;
  - l'option C de M31 (fiche 7) et l'option C de la fiche 8 (a_π = 0,5, k_I = 0,25 par an, λ_e = 0,2 par an) ;
  - le cadre : émission en position α, Π^CB, registre de 13 niveaux, π\*_t.
- Bloc 9, commun à toutes les options :
  - plan de dépense en volume indexé sur la production potentielle : G^plan_t = P_{t−1}(1 + π\*^pas)·s_G·ŷ_t ;
  - T_F = Tr = 0 ;
  - M^G\* égale aux paiements bruts du pas (m = 1) ;
  - A8 avec une part s_CB de la banque centrale (0 sauf mention) ;
  - i_B = i_res = i_CB ; E^CB_0 = 0.
- Calibration indicative :
  - celle de `tab:calibration`, avec ζ = 4 (variante 8), ϖ_L = 2 %, ϖ_D = 1 %, ϑ = 0,10, g = 2 %, g_N = 0,5 %, τ = 0,25 ;
  - r̄ = 1 % (Fisher), état initial résolu en lecture (1) de #44 : r̄ donné, s_G résolu.
- **Contrôles**, sur 10 réglages × 3 cibles (`chk9.py`) :
  - un pas depuis l'état résolu laisse l'état normalisé inchangé à 3,6e−15 près ;
  - E^Bk calculé par le stock et par les flux coïncide à 3,1e−15 près ; E^CB = 0 à 5,6e−17 près (s_CB = 0). Avec s_CB ∈ {0,25 ; 0,5 ; 1}, π̄ ∈ {0 ; 2 ; 10 %}, G +10 % au tour 1 et 24 pas : |E^CB|/B ≤ 1,2e−16 (`c58.py`), après correction du diagnostic de `m9.py:209` (C58).
- **Méthode spectrale** : celle de la fiche 8 (§ 3.0). Les deux régimes de T4 sont linéarisés séparément, la racine nominale est retirée, et les états inertes de chaque option sont retirés.
- Coût : 22,1 µs par pas pour la maquette entière, sous C-Y ; 21,0 µs sous F (`ratios.py`).

**Mesures exécutées** (04/10/2026). Commandes : `cd …/scratchpad/maquette_f9 && /home/user/projet_macro/.venv/bin/python <script>`, avec l'interpréteur du `.venv` du projet, le même que `uv run python`.

| Script | Objet |
|---|---|
| `chk9.py` | Stationnarité et identités, 30 cas |
| `tab.py` | Gain statique, Δr̄, racines du critère 13, assiettes C |
| `decomp.py`, `decomp2.py` | Décomposition de la dépendance à π̄ (§ 3.Q) |
| `tab2.py` | Rayons, #56, palier, options A, B, C, D, E, V |
| `tab3.py` | φ\*, gain et arrivée sous D |
| `tabF.py`, `simF.py`, `arr9.py` | Option F ; chocs permanents ; taux tenu long |
| `jeu9.py` | Seuils de `jeu`, θ_H, arrivée |
| `hs.py`, `grid.py`, `final_hs.py` | Option C-HS : critère 13, grille, ratios, scénarios |
| `ratios.py`, `uniq.py`, `main9.py`, `cmp_m.py` | Ratios stationnaires, unicité de r̄, cas à la main, concordance des maquettes |

Aucune mesure n'a été recalculée par un autre agent. Toutes sont des **résultats de modèle**, sans statut de fait.

**Littérature.**
- *Retrouvée, contenu lu par résumé seulement* :
  - H. Bohn, « The Behavior of U.S. Public Debt and Deficits », *QJE* 113(3), 1998, p. 949-963. Le résumé, retrouvé par moteur de recherche (PDF bloqué par le proxy, deux miroirs essayés), dit : « the primary surplus is an increasing function of the debt-GDP ratio », sur 1916-1995. Cela soutient la *forme* de l'option D, pas une valeur de pente.
  - E. M. Leeper (1991), *JME* 27(1), p. 129-147 : lu par `monnaie` en résumé (fiche 6 § 6.6), non lu par `macro`.
- *Existence vérifiée, non lus* :
  - M. Feldstein, « Inflation, Income Taxes, and the Rate of Interest: A Theoretical Analysis », *AER* 66(5), 1976, p. 809-830 (le non-neutralisme d'un impôt sur les intérêts nominaux) ;
  - Domar (1944) ; Lerner (1943) ; Blanchard (2019) (critère 22).
- *Lus par reproduction* : Godley et Lavoie (2007), chap. 3 (SIM), par la reproduction `sfcr` déjà citée dans `sec:menages`.
- *Ce que la littérature permet de conclure* :
  - la forme « surplus primaire croissant avec la dette » est documentée empiriquement (Bohn) ;
  - le non-neutralisme d'un impôt sur intérêts nominaux est une identité arithmétique, montrée ici (§ 3.Q) sans appui de littérature lue.
- *Ce qu'elle ne permet pas* : calibrer φ_b, ni départager les assiettes.

**Statut des faits de la première tentative** (critère 23).

| Fait | Statut |
|---|---|
| D1 : `tax_rule=True`, `fiscal_rule=False`, `treasury_redeem_all=True` (faits l. 11) | S+O |
| Dette 0,61 → 0,04 sans règle ; 0,40 à 0,45 avec `eq:fiscrule` (v1.5, l. 1518) | R |
| Dette publique nette de 62,4225 % du PIB (F3) ; monétisation, 293,0506 % (faits l. 277) | R |
| Lectures de `policies.py` l. 25-96 et de `model.py` l. 195-210, 288-300, 375-382, 508, 1200-1250, 1400 | L, le 04/10/2026 |

Aucune remesure V n'a été faite.

### 3.A Option A — v1.5

1. **Source exacte.** Dans `archive/v1.5/Nations_et_Marches_v1_5.tex`, § `sec:etat` :
   - recettes (l. 1457 à 1470) et capacité administrative (l. 1471) ;
   - `eq:iapp` (l. 1484 à 1490) ;
   - `eq:gbc` et `eq:debtdyn` (l. 1500 à 1503) ;
   - `eq:fiscrule` (l. 1513 à 1518) ;
   - placement v1.2 et trésorerie v0.9 (l. 1520 à 1527) ;
   - `eq:default` et plafond indicatif (l. 1528 à 1541).
2. **Équations.**
   - Facteur des achats : φ^fisc_t = clip(1 + φ_b(b\* − b_t), 0,6, 1,6), avec φ_b = 0,3 et b\* = 0,6 (*choix de conception*). Il multiplie les achats, l'investissement public et les minima.
   - Recettes : impôts du travail par strate, du capital distribué, des sociétés, TVA, tarifs, capitation, le tout multiplié par ε^adm(1 − ε^ev τ̄²), forme de Laffer (*approchée*).
   - Taux apparent : i^app_{t+1} = (1 − θ_t) i^app_t + θ_t i^B_t, avec θ = 1/T̄ + déficit⁺/B (*approchée*).
   - Contrainte budgétaire : `eq:gbc` (*dérivée*).
   - Placement : « le taux monte jusqu'à équilibre » ; rationnement ρ^G = min(1, T^disp/D^prev) ; intérêts impayés capitalisés (l. 1522).
   - **Forme retenue sur la maquette**, déclarée : G^plan multiplié par 1 + φ_A(b̄ − b_t), sans écrêtage (inactif près de l'état stationnaire), sans T9, avec b_t la dette nette d'ouverture sur 12 × le PIB potentiel au prix attendu. La cible b\* est remplacée par la valeur résolue b̄ : sinon l'état initial n'est pas stationnaire.
3. **État stationnaire impliqué.**
   - Avec b\* ≠ b̄, le facteur stationnaire vaut 1 + φ_b(b\* − b̄) ≠ 1. L'écart stationnaire à b\* dépend donc de φ_b (critère 7 (a) (i)). La dette reste fixée par les normes privées (identité du § 1), b\* n'est pas atteinte, et G/PIB porte l'écart.
   - En v3, la seule lecture stationnaire est b\* = b̄. Mais après tout choc permanent (marche de π\*, G +1 %), l'arrivée dépend encore de φ_A : continuum par le gain, comme sous D (§ 3.D-3).
4. **Comportement mesuré.**
   - R (v1.5, l. 1518) : dette 0,61 → 0,04 en 60 ans sans règle, 0,40 à 0,45 avec elle ; une première version rapportait la cible à 52 fois le PIB annuel.
   - Maquette (`tab2.py`), rayon dans les deux régimes :

     | φ_A | π̄ = 0 | 2 % | 10 % |
     |---|---|---|---|
     | 0,15 | 0,999033 | 1,005479 | 1,018550 |
     | 0,3 | 0,998371 | **1,003214** | 1,017313 |
     | 0,6 | 0,997472 | 0,999366 | 1,014580 |

   - #56 (A) à 2 % : P_36 > P_36^réf (+0,201 / +0,165 / +0,097 %), signe inversé.
   - Taux tenu un point bas : glissement −0,220 / −0,144 / −0,021 au tour 120, signe inversé (critère 10 (b) (ii) de la fiche 8).
   - **La règle de la v1.5, à sa pente d'origine, est instable dans la boucle conjointe v3 à 2 % et à 10 %.** Un rappel par les achats ne reprend pas le surcroît d'intérêts à fréquence nulle (C37).
5. **Coût de calcul.** Négligeable pour le facteur et `eq:iapp`. Le placement « jusqu'à équilibre » est une itération par pas, exclue (critère 20). La capacité administrative et le terme de Laffer sont en forme fermée.
6. **Défauts connus.**
   - L'écrêtage [0,6 ; 1,6] est une borne à seuil libre (instabilité 15) ;
   - capitalisation des intérêts impayés (exclue, critère 12 (e)) ;
   - placement itératif ;
   - avances au Trésor dans T^disp (instabilité 2, exclue par M22) ;
   - prime et défaut : J6 ;
   - sans T9, C37 n'est pas tenue (mesure ci-dessus).
7. **Identités de bilan touchées.**
   - Lignes 2, 6, 7, 11a à 11c, 16 et 19a, comme le socle.
   - Les avances (ΔA^G) et la capitalisation créent un poste hors des portes de `tab:portes-monnaie` (ADR 0005, point 7) : incompatible sans décision citant M22.
   - Le rationnement ρ^G est une part non payée sans ligne nommée.
8. **Ce que le joueur en percevrait.**
   - Une dépense qui baisse quand la dette monte : lisible.
   - Mais la reprise passe par les achats, et non par l'impôt : un choc de taux devient expansionniste (signe inversé).
   - L'écrêtage fait un mur invisible. À soumettre à `jeu`.
9. **Empreinte sur l'état.**
   - Facteur : aucune variable d'état ; b_t se lit sur l'ouverture.
   - `eq:iapp` : une variable d'état i^app, de valeur stationnaire i_B (§ 3.V).
   - Le rationnement v0.9 exige T^disp, une prévision des recettes : un état caché à déclarer.

### 3.B Option B — v2.0 (branche active de D1 : `tax_rule=True`)

1. **Source exacte.**
   - `archive/v2.0/prototype/policies.py:73-96` (`update_taxes`) ; l. 30-32 (taux plafonnés à 0,90) ; l. 86 (croissance estimée, écrêtée dans [−0,10 ; 0,20]) ; l. 89 (déficit visé) ; l. 93-94 (multiplicateur écrêté dans [0 ; 3], vitesse).
   - `archive/v2.0/prototype/model.py` : l. 201 (`gov_cash_ratio` = 0,04) ; l. 202 (`treasury_redeem_all`) ; l. 297-298 (`tax_debt_feedback` = 0,20, `tax_adjust_speed` = 1 par an) ; l. 379-380 (interdiction du dividende de trésorerie sous `tax_rule`) ; l. 1208 (Π^CB tronqué) ; l. 1215 (encaisse visée = `gov_cash_ratio` × PIB) ; l. 1220-1244 (placement : ménages, puis banque dans sa limite, puis ρ^G écrêté dans [0,2 ; 1]) ; l. 1248 (rachat) ; l. 508 et 1400 (i_B = i_app ; i_B = i_cb + min(prime, prime_max)).
   - Statut L.
2. **Équations.**
   - Déficit visé : d\* = 52 (b\* − k)(1 − e^{−g_n/52}) − κ(b^net − (b\* − k)), avec κ = 0,20 par an.
   - Multiplicateur : x ← x + (1 − e^{−λ_τ/52})·[clip(x + (d − d\*)/base, 0, 3) − x], avec λ_τ = 1 par an.
   - Ces équations lisent les quatre dernières semaines d'un historique (l. 82-83) et un `getattr` avec valeur par défaut (l. 86).
   - **Forme v3 retenue sur la maquette**, déclarée :
     - τ_{t+1} = τ_t + (λ_τ/n_a)(d_t − d\*_t)/base_t, avec d\*_t = n_a(Γ^e − 1) b̄ − κ(b_t − b̄) ;
     - grandeurs rapportées au PIB potentiel du pas au prix attendu, assiette WB, sans T9 ;
     - sans historique ni écrêtage ;
     - Γ^e du moteur remplace la croissance estimée.
   - Statut : *choix de conception* (contrôleur PI sur la dette).
3. **État stationnaire impliqué.**
   - À l'arrêt, d = d\* ⇒ b̄ = b\* exactement, si Γ^e égale la croissance réalisée. Sous la v2.0, l'arrivée n'est exacte que si la croissance estimée (lissée et écrêtée, l. 86) égale la croissance réalisée : vérifié non exact hors de la trajectoire de référence (lecture, critère 7 (a) (ii)).
   - Comptage : B **ancre la dette** ; τ est son résultat. Le rang est plein avec r̄ résolu par la demande. Mais la dette dépend de π̄ (C30 : +0,287 année de PIB entre 2 et 10 %) : une cible réelle b̄ fixe alors le taux réel, et les deux dépendances se cumulent dans r̄ (mesure ci-dessous).
4. **Comportement mesuré.**
   - R (D1) : dette publique nette de 62,4225 % du PIB (contrôle F3). Coût de la monétisation sous barèmes figés (faits l. 277).
   - Maquette (`tab2.py`, `simF.py`), rayon dans les deux régimes, κ = 0,2 :

     | λ_τ | π̄ = 0 | 2 % | 10 % |
     |---|---|---|---|
     | 0,5 | 0,997082 | 0,997156 | 0,997261 |
     | 1 | 0,997080 | 0,997149 | 0,997244 |
     | 2 | 0,997079 | 0,997146 | 0,997235 |

     **Stable.** Ce n'est pas la cible intégrale de B/PIB « explosive pour tous les ζ » de la fiche 6 § 6.6 : la forme est PI sur la dette, via le déficit.
   - #56 à λ_τ = 1 : (A) écart cumulé −0,033 %, P_36 −0,228 % ; (B) P_120 −2,49 %, glissement −0,295.
   - Taux tenu −1 point : palier +0,302 au tour 120.
   - G +1 % permanent : glissement −0,011 au tour 60 ; Δi +0,075 point au tour 2 400 ; Δτ = +0,00279.
   - **Marche de π\* de 2 à 3 % : r̄ de Fisher passe de 1 % à −1,03 % au tour 2 400.** Le critère 13 est très loin.
5. **Coût de calcul.**
   - Forme v3 : quelques opérations par pas.
   - La v2.0 lit une moyenne sur quatre semaines d'historique, exclue par l'ADR 0002.
6. **Défauts connus.**
   - Historique et `getattr` (critère 19).
   - Quatre écrêtages : multiplicateur [0 ; 3], taux ≤ 0,90, croissance [−0,10 ; 0,20], ρ^G [0,2 ; 1] (instabilité 15).
   - Π^CB tronqué (écarté par M22 (d)).
   - Instabilité 5 évitée par l'interdiction croisée (l. 379-380).
   - Drapeaux `tax_rule`, `fiscal_rule`, `fiscal_on_net_debt`, `treasury_redeem_all`.
   - Encaisse en part du PIB annuel, au lieu des paiements du pas (critère 11 : une encaisse de 4 % du PIB annuel vaut à peu près ½ mois de PIB).
7. **Identités de bilan touchées.**
   - Lignes du socle.
   - Le placement aux ménages (B_H > 0) contredit M27 (B_H ≡ 0).
   - Le rachat (`redeem_public_debt`) est une ligne 19a négative.
   - Le rationnement ρ^G n'a pas de ligne nommée.
8. **Ce que le joueur en percevrait.**
   - Un multiplicateur d'impôt qui bouge sans levier du joueur : boîte noire.
   - Un choc de dépense presque sans effet sur l'inflation, l'impôt l'ayant compensé (glissement −0,011).
   - Une cible de dette qui fait bouger le taux réel de deux points par point de cible.
9. **Empreinte sur l'état.**
   - Une variable d'état τ (taux de prélèvement, sans dimension, de valeur stationnaire résolue).
   - La v2.0 ajoute un historique de quatre semaines et l'état `tax_scale`.

### 3.N Socle commun des options nouvelles (Q5 à Q10, Q12)

**N-1, Q9 : i_B et phase 7.**
- Recommandation commune, celle du § 2, critère 13 (c) : **(i) i_B ≡ i_CB**.
  - Grandeur dérivée, prime nulle déclarée, délai 0 des lignes 11b et 11c.
  - Position dans le corridor : i_res = i_B = i_CB.
  - Π^CB = i_CB(B_CB + L^CB − Res)/n_a ; sous E^CB_0 = 0, Π^CB = i_CB·M^G/n_a, négatif si i_CB < 0.
- Phase 7 sous A8 :
  - besoin de l'État (formule l. 497 à 500), puis 19a-BC = s_CB × besoin (s_CB écrit par le bloc 8 en phase 1), puis 19a-banque = reliquat (C19) ;
  - les trois lignes 19a sont proposées par le bloc 9 ;
  - 19b n'est jamais en acheteur passif ;
  - triangulaire : la phase 7 lit les phases 5 et 6 et Π^CB de la phase 1.
- Instruit, avis au § 5, non tranché.

**N-2, Q6 : M^G\*.**
- Option sans paramètre : **M^G\*_t = G_t + Tr_t + i_B B_t/n_a**, paiements bruts exécutés, lus en phase 7 (m = 1).
- M^G\*/(12 PIB) sous C-HS à n_a = 12 : 0,018282 / 0,018904 / 0,022857 à π̄ = 0 / 2 / 10 %. Valeurs à n_a = 4 et 52 au § 3.C-3.
- Contrôle de caisse en lecture nette, (i), marge 1 − Γ̄ max{s_G ; 1 − T/P} (où P désigne les paiements bruts du pas, critère 11) :

  | π̄ | 0 | 2 % | 10 % |
  |---|---|---|---|
  | Marge (C-HS) | **0,0037** | 0,0334 | 0,2061 |

  - À n_a = 4 et 52, à π̄ = 0 : 0,0019 et 0,0044.
  - Le contrôle est inactif à l'état stationnaire, mais **la marge plafonne la hausse de G d'un tour au suivant** à 1/(Γ̄ s_G) − 1.
  - À π̄ = 2 %, une dépense +5 % est rationnée au premier tour d'environ 1,5 % de G (1,05 × 0,9666 = 1,0149). À π̄ = 0, toute hausse au-delà de 0,37 % l'est.
  - Cas à la main (`main9.py`, G +10 %) : G/M^G d'ouverture = 1,0642, le plan serait rationné de 6 %.
  - La maquette n'exécute pas ce plafond ; les scénarios de `jeu` (§ 3.C-8) sont donc mesurés sans lui.
- Effet sur les réserves (critère 11 (e)) : sous E^CB = 0 et Res = 0, L^CB = M^G. Une hausse de M^G\* de x relève L^CB de x (cas à la main : L^CB = 0,281969 avec M^G = 0,316582 et B_CB = 0,034613).

**N-3, Q7 : ordre des paiements et parts non payées.**
- Ordre déclaré :
  1. **plan de dépense plafonné en phase 2 sur l'encaisse d'ouverture**, G^plan_t ≤ M^G_t. C'est une borne à seuil libre dont le seuil est une base, sur le modèle de H5 ;
  2. phase 6 : intérêts (11b, 11c) prioritaires, puis Tr ; la part de Tr non versée devient la ligne nommée « transferts non versés » ;
  3. ligne 16 négative en 8 (b), dernière ; la part non versée devient la ligne nommée « perte de la banque centrale non couverte », qui réduit E^CB (à décider avec la fiche 8).
- Impôt non recouvré (ménages, entreprises) : ligne nommée du bloc 9, sans créance.
- Sous α, une perte de la banque centrale est couverte par l'émission. Montré à la main : −Π^CB entre dans le besoin de la phase 7, et Π^CB est calculé en phase 1. Elle n'est donc non couverte que si le placement rate.
- **Non mesuré** : cas à la main (i) à (iii) du critère 12, postes après chaque phase, renvoyés au J3.

**N-4, Q5 : durée de la dette.**
- Référence : toute la dette au taux de la dernière date de décision (M22, l. 548). Variante V au § 3.V.

**N-5, Q10 : forme du plan de dépense.**
- **Volume indexé sur la production potentielle, au prix attendu** : G^plan_t = P_{t−1}(1 + π\*^pas_t)·s_G·ŷ_t, avec ŷ_t = pr_t(1 − U^eq)N^pa_t.
  - Unité du levier : s_G, en part du potentiel en volume.
  - Un levier inchangé laisse l'état stationnaire (critère 19). Pas d'ancre nominale en u.m. (critère 10 (b) (ii) de la fiche 8).
- Sur-commande (#53) : la part non servie (rationnement proportionnel du bloc production) n'est pas payée.
  - Elle est **bornée par le plafond de caisse** (N-3).
  - Son coût est l'éviction proportionnelle de C et de I au même tour.
  - Elle est visible par « dépense demandée et exécutée ».
  - Proposition soumise à `jeu`.

**N-6, Q8 : T_F, Tr, cotisations.**
- T_F suit le contrat de la fiche 6 : assiette avec la ligne 8, chute sur Div_F, T^e_F = Γ^e T_{F,t−1}, rattrapage au tour n + 1. Taux τ_F, valeur indicative 0 au socle ; à trancher, puisque l'assiette HS de T_H impose déjà les dividendes distribués.
- Tr en part du PIB potentiel nominal (levier), valeur indicative 0 au test zéro.
- Allocations de chômage (l. 977) : variante de stabilisateur proportionnel, compatible avec la fermeture (i). **Non mesurée.**
- T_F > 0 et Tr > 0 : **non mesurés** sur la maquette.

**N-7, Q12 : restitution.**
- Choix adopté au § 2 : dette brute de clôture sur la somme des 12 derniers PIB, à une décimale.
- Sous C-HS à 2 % : 0,27564 × 1,0216 = **28,2 % du PIB affiché**, contre 0,25674 année de PIB pour la dette consolidée du test zéro.

### 3.C Option C — reprise réelle du surcroît d'intérêts (T9 réel), quatre assiettes (nouvelle)

1. **Source exacte.**
   - Nouvelle : fiche 6 § 3.L (T9, l. 934) et § 6.6 (C37) ; fiche 8 § 6.6 (C45, C46) ; assiette de Haig-Simons transposée de H3 (`sec:menages`, l. 1410).
   - Godley et Lavoie (2007, chap. 9, DISINF), lus par reproduction.
2. **Équations** (phase 6, lues sur l'ouverture et les phases 1 à 5, sans ordre interne).
   - T_{H,t} = τ_H·A_t + φ·(i_B,t − i^ref_t)·(B_t − M^G_t − E^CB)/n_a, avec i^ref_t = (1 + r^ref)(1 + π\*_t) − 1 (T9 réel, C45) et φ = 1. Statut *choix de conception*.
   - r^ref = r̄ de l'état résolu. T9 est nul à l'état stationnaire de référence.
   - Les quatre assiettes A_t, toutes lues sur l'ouverture pour respecter le critère 2 (c) :

     | Variante | Assiette A_t |
     |---|---|
     | C-WB | WB_t (phase 4) |
     | C-Y | Γ^e Y^pre_{H,t−1}, avec Y^pre = WB + i_D D_H/n_a + Div_F + Div_Bk |
     | C-Yhi | Γ^e (WB + Div_F + Div_Bk)_{t−1} |
     | **C-HS** | Γ^e (Y^pre_{H,t−1} − π\*^pas D_{H,t−1}) : revenu de Haig-Simons avant impôt, les intérêts n'étant imposés qu'au-delà de l'érosion des dépôts par l'inflation visée |

   - « C-WB nominal » (T9 de référence nominale) est la règle provisoire de la fiche 8.
3. **État stationnaire impliqué.**
   - T9 = 0. La dette consolidée est fixée par l'identité (critère 5 (b)) : (B − M^G − E^CB)/(12 PIB) = ν_H·YD^HS/PIB − (L − D_F)/(12 PIB) + E^Bk/(12 PIB).
   - Vérifié sous C-HS à 2 % : 0,6505 − 0,4560 + 0,0622 = 0,2567, contre 0,25674 mesuré.
   - Solde de Domar : déficit/PIB = n_a(Γ̄ − 1) × dette consolidée, soit 3,9671 % × 0,25674 = 1,0185 %, égal à la mesure.
   - **C'est l'assiette qui fixe la dette**, par YD^HS/PIB.
   - Valeurs (`final_hs.py`, `ratios.py`), avec r̄ = 1 % et s_G résolu :

     | C-HS | n_a | π̄ = 0 | 2 % | 10 % |
     |---|---|---|---|---|
     | Dette brute B/(n_a PIB) | 12 | 0,11712 | 0,27564 | 0,53299 |
     | Dette consolidée (B − M^G)/(n_a PIB) | 4 | 0,09466 | 0,25237 | 0,49978 |
     | | 12 | **0,09884** | **0,25674** | **0,51013** |
     | | 52 | 0,10045 | 0,25844 | 0,51438 |
     | M^G/(n_a PIB) | 12 | 0,018282 | 0,018904 | 0,022857 |
     | Déficit / PIB (Domar) | 12 | 0,1959 % | 1,0185 % | 5,9005 % |
     | Solde primaire / PIB | 12 | −0,0971 % | −0,2432 % | −0,2381 % |
     | Charge d'intérêts brute / nette (PIB) | 12 | 0,1171 / 0,0988 % | 0,8324 / 0,7754 % | 5,9162 / 5,6625 % |
     | G/PIB ; T_H/PIB | 12 | 21,86 ; 21,76 % | 21,93 ; 21,68 % | 21,78 ; 21,54 % |
     | YD^HS/PIB | 12 | 0,6528 | 0,6505 | 0,6462 |

   - Sous C-WB à 2 % : dette consolidée 0,27403 ; sous C-Y : 0,25351.
   - **Paramètre qui fixe le ratio** : ν_H (fiche 5), avec les normes de la fiche 6 et ϑ. **La dépendance à π̄** (+0,253 entre 2 et 10 % sous C-HS) vient de C30 et de YD^HS (critère 5 (d)).
   - La dette du socle (environ 26 % du PIB à 2 %) est basse au regard des ordres de grandeur publics. **Non sourcé ici** : c'est une question de calibration au J3 (critère 22).
4. **Comportement mesuré** (π̄ = 2 % sauf mention ; `tab.py`, `tab2.py`, `tab3.py`, `hs.py`, `uniq.py`, `final_hs.py`, `grid.py`).

   | Grandeur | C-WB nominal | C-WB réel | C-Y réel | C-Yhi réel | **C-HS réel** |
   |---|---|---|---|---|---|
   | Gain statique, % de y par point de i | −0,0259 | −0,0259 | −0,2216 | −0,0599 | **−0,2208** |
   | Δr̄ après G +1 % permanent | +918 pb | +918 pb | +97 pb | +322 pb | **+96 pb** |
   | Δr̄/k_I, point-années | 36,7 | 36,7 | 3,9 | 12,9 | **3,8** |
   | Critère 13 : r̄ à π\* = 0 / 10 % (paramètres de 2 %) | −7,87 / −17,69 % | +5,73 / +2,60 % | +3,11 / −3,09 % | +3,55 / +1,92 % | **+1,536 / +1,075 %** |
   | Critère 13 : écart de C/PIB à 0 / 10 % | −5,80 / −16,02 pt | +2,55 / +0,34 pt | +1,27 / −2,99 pt | +1,49 / −0,01 pt | +0,435 / −0,473 pt |
   | Racines de r̄ dans [−60 ; 100 %] à 0 / 2 / 10 % | une / une / une | une / une / une | −21,53 et +3,11 / −26,95 et +1,00 / −40,80 et −3,09 | −7,54 et +3,55 / −14,79 et +1,00 / −39,04 et +1,92 | −20,63 et +1,54 / −26,65 et +1,00 / −40,49 et +1,08 |
   | Palier, taux tenu −1 point, tours 60 / 120 | +0,159 / +0,155 | idem | +0,367 / +0,402 | +0,104 / +0,100 | +0,363 / **+0,396** |
   | Rayon à 0 / 2 / 10 % (deux régimes) | 0,999270 / 0,999413 / 0,999814 | idem | 0,997497 / 0,997482 / 0,997537 | 0,999098 / 0,998517 (période 3 737) / 0,997761 | **0,997497 / 0,997486 / 0,997558** |
   | Demi-vie dominante | 1 181 tours | 1 181 | 275 | 467 | **275** |
   | #56 (A) : écart cumulé des tours 1 à 12 ; P_36 | −0,160 ; −0,138 % | idem | −0,216 ; −0,227 % | −0,134 ; −0,073 % | −0,216 ; −0,226 % |
   | #56 (B) : P_120 ; glissement | −1,81 % ; −0,151 | idem | −3,76 % ; −0,391 | −1,24 % ; −0,096 | −3,72 % ; −0,385 |
   | φ\* (rayon = 1) à 0 / 2 / 10 % | — | 0,709 / 0,905 / 0,986 | ≤ 0 / 0,112 / 0,454 | 0,702 / 0,764 / 0,806 | ≤ 0 / **0,131** / **0,487** |
   | Pays joué (φ = 0) à 2 / 10 % | 1,007482 / 1,019719 | idem | 1,001642 / 1,010681 | 1,007929 / 1,018494 | 1,001818 / 1,011036 |

   - Les valeurs de la fiche 8 (§ 6.1 et 6.2) sont reproduites : −0,0259 ; +918 pb ; 36,7 ; −0,2216 ; +97 pb ; 3,9 ; 0,999413 ; 0,997482 ; −7,87 / −17,69 ; +5,73 / +2,60 ; 3,11 et −21,53.
   - **Sous C-HS** (`final_hs.py`) :
     - après G +1 % permanent, arrivée sur i à 1,9e−8 en relatif au tour 5 500 (20 demi-vies) ;
     - glissement +0,214 / +0,161 / +0,085 / −0,006 aux tours 60 / 120 / 240 / 600 ;
     - Δi +0,652 point au tour 120 ;
     - marche de π\* de 2 à 3 % : glissement 2,949 % au tour 120, 3,0000 au tour 2 400 ; r̄ de Fisher 0,8788 % ;
     - taux tenu −1 point : +0,014 au tour 3, +0,580 au tour 12, +0,396 au tour 120, +0,596 au tour 2 400. C'est un **nouveau palier**.
   - **Grille G sous C-HS** (`grid.py`), 31 branches, chaque vitesse et chaque gain ×0,5 et ×2, deux régimes : toutes sous 1, pire cas 0,998883 (toutes vitesses ×0,5). ζ = 8 : 0,996234.
   - **θ_H (C50)**, sous les deux définitions (`jeu9.py`, `final_hs.py`) :
     - part d'une vente imprévue qui atteint les ménages (ΔDiv_F/ΔG au tour 1) : 0,4983, quelle que soit l'assiette ;
     - θ_H au sens de la l. 1543 (ΔYD/Δ(p·y), production marginale non vendue) : −0,2000 sous C-WB, −τ·UC/p ; 0,0000 sous C-Y et C-HS. F2 finance la masse salariale d'une production invendue sur le dividende : ΔWB/Δ(py) = 0,80, ΔDiv_F/Δ(py) = −0,80.
     - Les hypothèses provisoires θ_H = 0,8 ou 1 de `sec:menages` ne sont donc pas celles du socle sous F2 : la propension opérante est la part de la vente, 0,498.
5. **Coût de calcul.** Une assiette et T9 : une dizaine d'opérations. Sans itération. 22,1 µs par pas pour la maquette entière.
6. **Défauts connus.**
   - Aucune instabilité connue réintroduite : ni avance, ni coupon de consolidation, ni dividende de trésorerie.
   - C-WB : traîne d'inflation de 36,7 point-années et φ\* de 0,905 à 0,986.
   - C-Y : impôt sur les intérêts nominaux, d'où le critère 13 dégradé (−3,09 % à 10 %).
   - Deux racines de r̄ sous C-Y, C-Yhi et C-HS (C49) : la seconde est à r̄ ≤ −7,5 % à 0 % et ≤ −14,8 % à 2 %. **Aucune n'est dans le domaine de la fiche 8** : une condition de domaine, r̄ > −5 % par exemple, à déclarer en `\limites`, sélectionne la racine. Son voisinage dynamique n'est pas mesuré.
7. **Identités de bilan touchées.**
   - Lignes 2, 7 (T9 compris), 11b, 11c, 16 et 19a ; aucune ligne ajoutée.
   - Cas à la main (`main9.py`, C-Y, s_CB = 0,5, G +10 %) :
     - ligne 2 : 0,306275 ; ligne 7 : 0,275426 ; ligne 11b : 0,010307 ; ligne 11c : 0 (B_CB d'ouverture nul) ; ligne 16 : 0,000724 ; 19a-banque = 19a-BC = 0,034613 ;
     - ΔV_G par le stock = par les flux = −0,040431486786, écart −2,8e−16 ;
     - M^G de clôture = M^G\* = 0,316582 ; E^CB = 0 (stock de clôture, `main9.py` corrigé : 0,00e+00 ; la sortie de `18d2868` affichait ~~−3,46e−02~~, diagnostic qui sommait B_CB d'ouverture avec des postes de clôture, C58) ; E^Bk stock − flux = −2,0e−15.
8. **Ce que le joueur en percevrait** (C-HS ; `final_hs.py` ; mesures sans le plafond de caisse de N-2).
   - Taux d'imposition +1 point :
     - production −0,838 % au tour 8 (moitié du pic au tour 15) ;
     - solde sur 12 tours +0,791 point au tour 12 ;
     - dette restituée −0,529 point au tour 12, −2,441 au tour 60.
   - Dépense +1 % pendant 12 tours : production +0,290 % au tour 6, moitié au tour 12 ; dette +0,095 point au tour 12.
   - Dépense +5 % pendant 12 tours : production +1,445 % ; solde −0,944 point ; dette **+0,473** point au tour 12, +0,599 au tour 60.
   - Transferts +0,2 % du PIB potentiel mensuel pendant 12 tours : production +0,175 % au tour 7, moitié au tour 14 (critère 6 (d) tenu).
   - Une hausse de taux alourdit l'impôt (T9) le tour même : la reprise est visible.
9. **Empreinte sur l'état.**
   - C-Y, C-Yhi et C-HS : une variable d'état assise sur un flux (Y^pre_{t−1} ou sa variante, u.m. par pas, valeur stationnaire Y^pre/Γ̄), écrite en phase 9 au montant exécuté (M29).
   - C-WB : aucune.
   - T9 : aucune (r^ref est une constante de l'état résolu).

### 3.D Option D — rappel proportionnel de la dette (forme de Bohn), nouvelle

1. **Source exacte.** Bohn (1998), résumé retrouvé : forme qualitative seulement. Demande de la fiche 8 § 6.3 (d).
2. **Équation.** T^rap_t = (φ_b/n_a)·[(B − M^G − E^CB)_t − b̄·n_a·P_{t−1}(1 + π\*^pas)ŷ_t], ajouté à T_H. Proportionnel, sans action intégrale. Statut *choix de conception*.
3. **État stationnaire impliqué.**
   - À la référence, b = b̄ et T^rap = 0.
   - Après tout choc permanent, la dette d'arrivée reste fixée par les normes privées, et T^rap ≠ 0 en permanence : **l'arrivée dépend de φ_b**.
4. **Comportement mesuré** (`tab2.py`, `tab3.py`).
   - Avec C-Y réel :

     | φ_b (par an) | 0,05 | 0,1 | 0,2 |
     |---|---|---|---|
     | Rayon à 2 % | 0,997282 | 0,997234 | 0,997204 |
     | Gain statique (% de y par point) | −0,3401 | −0,4477 | −0,6361 |
     | Δr̄ après G +1 % permanent | +64,2 pb | +48,9 pb | +34,5 pb |
     | r̄ à π\* = 3 % | −0,237 % | −0,452 % | −0,655 % |

     L'écart d'arrivée entre branches dépasse de loin 1e−6 : **le critère 7 (iii) échoue**.
   - Sans T9 (D0) :
     - φ_b = 0,1 : 0,998096 à 2 %, **1,006585 à 10 %** ;
     - φ_b = 0,3 : 0,997085 et 0,999740.
5. **Coût de calcul.** Négligeable.
6. **Défauts connus.** Continuum d'arrivées indexé par le gain (`docs/exigences.md` § 2.7). Sans T9, instable à 10 % pour φ_b = 0,1.
7. **Identités de bilan touchées.** Ligne 7 seulement.
8. **Ce que le joueur en percevrait.** « Plus de dette, plus d'impôt » : lisible. Mais l'état d'arrivée dépend d'un réglage caché.
9. **Empreinte sur l'état.** Aucune variable d'état (b̄ est une constante de l'état résolu).

### 3.E Option E — leviers tenus, forme SIM/PC (pays joué, « intérêts financés par le déficit »)

1. **Source exacte.** Godley et Lavoie (2007, chap. 3, SIM ; chap. 4, PC), par reproduction `sfcr` : G exogène, taux d'imposition fixe.
2. **Équations.** T_H = τ_H·A_t ; G^plan selon N-5 ; aucune reprise (φ = 0).
3. **État stationnaire impliqué.** Le même que C à la référence, puisque T9 y est nul. Après un choc de taux, le surcroît d'intérêts est financé par le déficit.
4. **Comportement mesuré** (`tab2.py`, `final_hs.py`).
   - Rayons (WB / Y / Yhi / HS) :

     | | WB | Y | Yhi | HS |
     |---|---|---|---|---|
     | π̄ = 2 % | 1,007482 | 1,001642 | 1,007929 | 1,001818 |
     | π̄ = 10 % | 1,019719 | 1,010681 | 1,018494 | 1,011036 |
     | π̄ = 0 | 1,002307 | 0,997894 | 1,003219 | non mesuré |

   - #56 (A) sous E-HS :
     - à 0 % : écart cumulé −0,136 %, P_36 −0,110 % ;
     - à 2 % : −0,053 % et **P_36 +0,033 %**, P1 échoue ;
     - à 10 % : +0,085 % et +0,463 %.
   - Scénarios : G +5 % pendant 12 tours, dette +0,603 point au tour 12 et +1,073 au tour 60 (au-dessus du contrôle) ; taux d'imposition +1 point, production moitié du pic au tour 34.
5. **Coût de calcul.** Négligeable.
6. **Défauts connus.** Divergence de C2 (dominance budgétaire, critère 9 (d)). Lecture de Leeper (1991) au § 3.N-8 ci-dessous, par analogie et non établie.
7. **Identités de bilan touchées.** Celles du socle.
8. **Ce que le joueur en percevrait.** Une hausse de taux inflationniste à moyen terme, explosive à 10 %. C'est le piège signalé par `jeu` (fiche 8 § 7, réponse 5).
9. **Empreinte sur l'état.** Aucune.

### 3.F Option F — fermeture budgétaire sur le taux neutre (nouvelle)

1. **Source exacte.** Nouvelle. L'idée est voisine de la finance fonctionnelle : le taux réel est fixé, le budget règle la demande. Aucune référence lue ne la soutient sous cette forme.
2. **Équation.**
   - τ_{H,t+1} = τ_{H,t} + (k_F/n_a)(r̂\*_t − r^ref), en phase 9, avec C-Y réel.
   - Le bloc 9 lit r̂\*, variable d'état d'ouverture du bloc 8.
   - Statut *choix de conception*.
3. **État stationnaire impliqué.**
   - Il y a deux actions intégrales et deux conditions : π̄ = π\* (bloc 8) et r̄ = r^ref (bloc 9). τ_H est fixé par l'égalité de la demande au potentiel. Le rang est plein.
   - r̄ est indépendant de π̄ et des gains. G/y, I/y, tu, ti et V_H/(n_a YD^HS) sont invariants : **c'est la seule option qui tient le critère 13 par construction.**
   - La fermeture est nouvelle, ni (i) ni (ii) du critère 6 (a). C2 reste au bloc 8.
4. **Comportement mesuré** (`tabF.py`, `simF.py`, `arr9.py`).
   - Rayon sous C-Y réel :

     | k_F | 0,003 | 0,01 | 0,03 | 0,1 | 0,3 |
     |---|---|---|---|---|---|
     | π̄ = 2 % | 0,999045 | 0,998184 | 0,998267 (période 793) | 0,998951 | 0,999969 |
     | π̄ = 0 | 0,998894 | 0,998234 | 0,998866 | 0,999462 | **1,000432** |
     | π̄ = 10 % | 0,999223 | 0,998267 | 0,998009 | 0,997949 | 0,999031 |

   - Sous l'assiette WB : instable dès k_F = 0,03 (1,000097).
   - Marche de π\* de 2 à 3 % : r̄ = 1,0007 % au tour 2 400 (k_F = 0,01).
   - G +1 % permanent : Δi au tour 2 400 = −0,001 point, Δτ_H = +0,00256 ; arrivée sur i à 3,0e−8.
   - #56 : (A) −0,216 %, P_36 −0,225 % ; (B) P_120 −3,57 %.
   - **Taux tenu −1 point (k_F = 0,01) : glissement +0,345 au tour 120, −0,591 au tour 600, +1,045 au tour 1 200, +3,238 au tour 2 400 : oscillation divergente.** Sous un taux tenu, r̂\* intègre encore l'écart d'inflation sans agir sur le taux, et le budget devient une double action intégrale sur l'inflation.
5. **Coût de calcul.** 21,0 µs par pas pour la maquette entière.
6. **Défauts connus.**
   - Instable dès que le levier de taux est tenu : c'est l'usage du joueur.
   - Le budget devient alors l'ancre nominale. C'est le cas « retour » du critère 10 (b) (ii) de la fiche 8, ici divergent.
   - Lecture croisée d'une variable d'état du bloc 8 par le bloc 9 : contrat partagé.
   - Cycle long, de 66 ans.
7. **Identités de bilan touchées.** Ligne 7.
8. **Ce que le joueur en percevrait.**
   - Après un choc permanent, l'impôt paie la dépense et r̂\* revient à sa référence. Cela répond à la « mémoire de r̂\* » de `jeu`.
   - Mais tenir le taux fait diverger l'économie sans signal.
9. **Empreinte sur l'état.** τ_H, variable d'état (sans dimension, valeur stationnaire résolue).

### 3.L Option L — finance fonctionnelle (Lerner, 1943), instruite par argument

- Une action intégrale budgétaire sur l'écart d'activité est exclue par le critère 6 (b) : sous la verticale de M25, elle n'ajoute aucune équation et laisse un continuum.
- La version proportionnelle (stabilisateur) est compatible avec la fermeture (i). Elle est déjà présente sous les assiettes C-Y et C-HS (impôt pro-cyclique) et sous l'allocation de chômage (N-6).
- La version « taux fixé, budget sur la demande » est l'option F.
- **Non mesurée séparément** : rubriques 2 à 9 sans objet, parce que l'option se ramène à F ou à N-6.

### 3.V Variante V — durée de la dette, à taux apparent (C24, critère 10 (b))

1. **Source exacte.** v1.5, `eq:iapp`, l. 1484 à 1490.
2. **Équation.** i^app_{t+1} = [i^app_t(B_t − B_t/(n_a T̄)) + i_CB,t(B_t/(n_a T̄) + émission⁺_t)]/(B_t + émission⁺_t), avec T̄ = 5 ans. i_B = i^app pour les lignes 11b et 11c, et pour T9.
3. **État stationnaire impliqué.** i^app = i_B. Aucun effet stationnaire.
4. **Comportement mesuré.**
   - Rayons : C-Y réel 0,997503 ; C-HS 0,997507 (contre 0,997482 et 0,997486 sans la variante).
   - Pays joué C-Y : 1,001125 à 2 % et 1,006981 à 10 % (contre 1,001642 et 1,010681) ; pays joué C-HS : 1,001266.
   - #56 (A) sous C-Y : −0,191 % et −0,207 %.
   - La variante **ralentit le canal rentier sans stabiliser le pays joué**.
5. **Coût de calcul.** Négligeable.
6. **Défauts connus.**
   - Pas de coupon de consolidation : l'instabilité 3 n'est pas réintroduite (moyenne pondérée, sans coupon au taux du moment).
   - La part détenue par la banque centrale « se reprice » immédiatement (critère 10 (c)) : non modélisé ici (B_CB = 0).
7. **Identités de bilan touchées.** Lignes 11b et 11c : leur taux n'est plus celui de la dernière décision. C'est une décision citant M22 (l. 548), puisque `tab:leviers-cadre` voit son délai changer.
8. **Ce que le joueur en percevrait.** Une hausse de taux qui pèse sur la charge d'intérêts sur plusieurs années.
9. **Empreinte sur l'état.** i^app (par an, valeur stationnaire i_B), sans cohortes.

### 3.Q Dépendance de la demande privée à π̄ et critère 13 (C15) (fiche 8 § 6.3 (e))

**Décomposition** (`decomp.py`, `decomp2.py`). Grandeur mesurée : Δs_G entre π̄ = 0 et 10 % à r̄ = 1 % donné, en fraction de y. Trois canaux sont neutralisés à la main (pour la mesure seulement) :
- **C30** : capital et stocks à la valeur comptable de π̄ = 2 % ;
- **conversion** : taux annuels convertis exactement, (1 + i)^{1/n_a} − 1, au lieu de i/n_a (ADR 0008, I.2) ;
- **écarts réels** : ϖ_L et ϖ_D proportionnels à 1 + π̄, dans le revenu stationnaire et dans le taux réel du crédit lu par S-ζ. *Corrigé le 04/10/2026 (C57)* : la mesure de `18d2868` ne neutralisait les écarts que dans le revenu, qui est neutre en agrégat. Le canal opérant est ϱ_L − r = ϖ_L/(1 + π̄).

| Assiette | Base | C30 neutralisé | Conversion exacte | C30 + conversion | Les trois |
|---|---|---|---|---|---|
| WB | +0,00134 | −0,00141 | +0,00411 | +0,00002 | +0,00002 |
| Yhi | +0,00023 | −0,00182 | +0,00295 | −0,00011 | +0,00004 |
| Y | +0,01618 | +0,01415 | +0,01808 | — | +0,01507 |
| HS | +0,00109 (s_G : 0,218474 / 0,219573 / 0,219568) | — | — | — | — |

Ce tableau est mesuré en lecture (1) : ϱ̄_L est résolu à chaque π̄. Il ne voit donc pas le canal des écarts par S-ζ, et sa colonne « les trois » vaut « C30 + conversion ». Le critère 13 se lit sur r̄ en lecture (α), ci-dessous.

- **Les deux sources dominantes sont C30 (fiches 2 et 6) et la conversion linéaire (cadre).** Elles sont de signes opposés et se compensent en partie.
- Sous l'assiette Y, l'impôt sur les intérêts nominaux domine.
- H3 (Haig-Simons) ne laisse pas de résidu mesurable au-delà de 2e−5 y.
- T9 nominal, au lieu de réel : −7,87 / −17,69 % au lieu de +5,73 / +2,60 % (assiette WB).

**r̄ au critère 13** (paramètres de 2 % fixés) :
- tel quel : C-HS +1,536 / +1,075 % (écart de 0,46 point entre 0 et 10 %) ; C-WB réel +5,73 / +2,60 % ;
- les trois canaux neutralisés **complètement** (C57, `c57.py`, `c57b.py`) : C-HS 1,004 / 0,985 %, soit **0,019 point** ; C-WB 1,017 / 0,936 % (0,081) ; C-Yhi 1,014 / 0,948 % (0,066) ; C-Y 2,396 / −4,654 % (impôt sur les intérêts nominaux).
- valeurs de `18d2868`, neutralisation incomplète, maintenues barrées : ~~C-WB 0,978 / 1,078 % (0,100 point) ; C-HS 0,976 / 1,088 % (0,112 point) ; C-Yhi 0,913 / 1,311 % ; C-Y 2,369 / −4,526 %~~.
- profil C-HS tel quel, r̄ à π\* = 0 / 1 / 2 / 3 / 4 / 6 / 10 % : 1,536 / 1,203 / 1,000 / 0,878 / 0,813 / 0,799 / 1,075 % ; non monotone ; écart maximal 0,74 point ; une marche de cible de 2 à 3 % déplace r̄ de −0,12 point.
- contribution de chaque source, les deux autres neutralisées, en r̄(10 %) − r̄(0) : C30 −1,30 ; conversion +0,43 ; écarts +0,11. Toute neutralisation partielle aggrave l'écart.

**Conclusion.**
- Aucune règle de la fiche 9 qui garde la fermeture (i) ne tient le critère 13 au seuil adopté. La meilleure, C-HS, divise l'écart par 20 par rapport à C-WB nominal, mais le seuil demande de toucher la fiche 6 (C30), le cadre (ADR 0008) et la fiche 7 (écarts nominaux), toutes trois ensemble. Il serait alors tenu (0,019 point). ~~et encore il ne serait que frôlé~~ (corrigé, C57).
- La seule règle qui le tient (F) diverge sous taux tenu (§ 3.F).


## 4. Tableau comparatif

Abréviations : « ok » = tenu ; « échec » = non tenu ; « mesure » = critère de mesure, valeur publiée ; « n. m. » = non mesuré. Les renvois portent sur le § 3. La colonne C-HS est l'option recommandée ; « C autres » regroupe C-WB, C-Y et C-Yhi.

| Critère | A. v1.5 | B. v2.0 | C-HS | C autres | D. rappel | E. leviers tenus | F. taux neutre |
|---|---|---|---|---|---|---|---|
| 1 (a)-(d) flux et identités | avances et capitalisation hors portes (A-7) | B_H > 0, rachats (B-7) | ok, cas à la main 2,8e−16 (C-7) | ok (C-7) | ok (D-7) | ok (E-7) | ok (F-7) |
| 2 phases et lectures | ρ^G lit des recettes prévues (A-9) | historique (B-1) | ok : assiette retardée, ouverture (C-2) | WB lu en phase 4 (C-2) | ok | ok | lit r̂\* du bloc 8 : contrat partagé (F-6) |
| 3 relevé des 28 lignes | jalon 4 | jalon 4 | jalon 4 | jalon 4 | jalon 4 | jalon 4 | jalon 4 |
| 4 (a) forme fermée | b\* ≠ b̄ (A-3) | ok si Γ^e (B-3) | ok (C-3) | ok (C-3) | ok à la référence (D-3) | ok (E-3) | ok (F-3) |
| 4 (b) comptage | rang plein, continuum après choc (A-3) | dette ancrée, τ résultat (B-3) | rang plein, r̄ résolu ; racine parasite r̄ < −7 % (C-6) | idem | arrivée fonction de φ_b (D-4) | rang plein | rang plein, 2 intégrateurs pour 2 conditions (F-3) |
| 4 (c) n_a | n. m. | n. m. | Domar 3,98 / 3,97 / 3,96 %, fenêtre déclarée (C-3) | C-WB et C-Y mesurées (`ratios.py`) | n. m. | idem C | n. m. |
| 4 (d) dépendance à π̄ | n. m. | r̄ −2,03 pt par point de π\* (B-4) | +0,253 année de PIB entre 2 et 10 % (C-3) | C-Y +0,241 (`ratios.py`) | mesure | idem C | r̄ invariant (F-4) |
| 5 (a)-(c) ratio de dette | b\* fixe (A-3) | b̄ visé (B-3) | 0,09884 / **0,25674** / 0,51013, consolidée (C-3) | C-WB 0,27403 ; C-Y 0,25351 | idem C | idem C | idem C |
| 5 (d) | n. m. | n. m. | mesure (C-3) | mesure | — | — | — |
| 6 (a)-(c) fermeture | (i) avec continuum | (i) + ancre de dette | (i), lecture (1) | (i) | (i), arrivée fonction du gain | (i) | fermeture nouvelle (F-3) |
| 6 (d) persistance ≤ 60 tours | n. m. | n. m. | ok : tours 12 et 14 (C-8) | ok | n. m. | ok : tours 14 à 55 (E-4) | n. m. |
| 7 vitesses et arrivée | **échec** (A-3) | ok à Γ^e exact (B-3) | ok : aucun gain du bloc 9 ; grille 31 branches (C-4) | ok | **échec** : r̄(3 %) de −0,24 à −0,66 % (D-4) | ok | ok à la référence ; instable sous taux tenu (F-4) |
| 8 (a) instabilités connues | 2, 15 (A-6) | 5 évitée, 15 (B-6) | aucune (C-6) | aucune | aucune | dominance déclarée | nouvelle, sous taux tenu (F-6) |
| 8 (b) boucle propre | Domar, rayon < 1 sous r̄ < g | idem | (1 + i^ref/n_a)/Γ̄ = 0,999214 à 2 % | idem | 0,99088 (φ_b = 0,1) | 0,999214 | idem C |
| 8 (c) boucle conjointe | **1,003214** (A-4) | 0,997149 (B-4) | 0,997486 ; pire 0,998883 (C-4) | 0,997482 à 0,999413 | 0,997234 | **1,001818 à 1,007929** | 0,998184 |
| 8 (d) avec la règle de la fiche 8 | échec | ok | ok | ok | ok | échec | ok, sauf taux tenu |
| 8 (e) Leeper | budget passif, mal réglé | passif | passif (C37) | passif | passif | actif : dominance | budget sur la demande |
| 9 (a) C23 | réponse sur les achats | réponse par τ, délai | reprise intégrale à délai 0 ; canal rentier nul à fréquence nulle | idem | idem + rappel | aucune : rentier positif | idem C |
| 9 (b) C37 | échec | partiel (B-4) | ok | ok | ok | échec | ok |
| 9 (c) C36 (i)-(iii) | échec | ok | ok : gain −0,2208, arrivée 1,9e−8 (C-4) | ok (C-WB très lent) | (i) ok, (ii-a) échec | échec | ok, sauf taux tenu |
| 9 (d) dominance budgétaire | — | — | voir E | voir E | — | mesure (E-4) | — |
| 10 (a)-(b) durée | `eq:iapp` (A-2) | i_app (l. 508) | variante V (§ 3.V) | idem | idem | V pays joué 1,001125 | — |
| 10 (c) part de la banque centrale | n. m. | n. m. | n. m. (B_CB = 0) | n. m. | n. m. | n. m. | n. m. |
| 11 (a)-(c) M^G\* | T^disp | 4 % du PIB annuel (B-6) | m = 1 ; marge 0,37 / 3,34 / 20,6 % (N-2) | idem | idem | idem | idem |
| 11 (d) P2 | — | — | avis § 5 | — | — | — | — |
| 11 (e) | — | — | L^CB = M^G (N-2) | idem | idem | idem | idem |
| 12 parts non payées | ρ^G implicite, capitalisation (A-6) | ρ^G écrêté (B-6) | ordre déclaré (N-3) ; cas (i) à (iii) n. m. | idem | idem | idem | idem |
| 13 phase 7 et i_B | « jusqu'à équilibre » (A-5) | ménages et banque (B-7) | A8, i_B ≡ i_CB (N-1) | idem | idem | idem | idem |
| 14 grandeurs lues ; θ_H | — | — | θ vente 0,498 ; θ_H 0 (C-4) | θ_H −0,20 sous WB | — | — | — |
| 15 test zéro | n. m. | n. m. | préalable : un pas 3,6e−15 (§ 3.0) ; au J3 | idem | idem | idem | idem |
| 16 bornes | écrêtage [0,6 ; 1,6] (A-6) | 4 écrêtages (B-6) | plafond du plan sur M^G (base), domaine de r̄ (C-6) | idem | idem | idem | idem |
| 17 (a)-(c) | — | — | § 3.C-8 et § 5 | — | — | — | — |
| 17 (d) seuils de `jeu` | — | — | d1 ok ; d2 ok ; **d3 0,473 < 0,5 sous la règle** ; pays joué 0,603 ok (C-8, E-4) | C-Y 0,489 ; C-WB 0,376 | — | ok | idem C-Y |
| 17 (e) sur-commande | rationnement ρ^G | ρ^G | plafond de caisse et éviction (N-5) | idem | idem | idem | idem |
| 18 #56 (P1, P2) | **échec** : P_36 +0,165 % | ok | ok : −0,216 / −0,226 % ; −3,72 % | ok | ok | échec à 2 et 10 % | ok |
| 19 simplicité, sans drapeau | écrêtage, T^disp | historique, 4 drapeaux | 1 paramètre (τ_H) + T9 ; 1 état | 0 ou 1 état | + φ_b | aucun | + k_F, état τ |
| 20 coût | itération (A-5) | ok | 22,1 µs par pas | idem | idem | idem | 21,0 µs |
| 21 notation | — | — | § 5 (symboles proposés) | — | — | — | — |
| 22 calibrabilité | — | — | dette basse, environ 26 % (C-3) | — | — | — | — |
| 23 statut des faits | § 3.0 | § 3.0 | — | — | — | — | — |
| **13 de la fiche 8 (C15)** | n. m. | **échec** (r̄ −1,03 % à 3 %) | **échec** : 0,46 point (§ 3.Q) | échec : de 3,1 à 9,2 points | échec | idem C | **ok** par construction (F-3) |


## 5. Avis de l'expert pilote

### Recommandation

**Option C-HS**, avec le socle commun du § 3.N.
- **Règle de référence** (test zéro, pays non joués), sous la fermeture monétaire (i), lecture (1) de #44 :
  - plan de dépense en volume indexé sur la production potentielle (s_G résolu) ;
  - impôt des ménages au taux τ_H, assis sur le revenu de Haig-Simons avant impôt, retardé d'un tour, Γ^e(Y^pre_{t−1} − π\*^pas D_{H,t−1}) ;
  - reprise intégrale et réelle du surcroît d'intérêts : T9 avec i^ref de Fisher sur π\*, φ = 1 ;
  - Tr et τ_F en leviers, à valeur indicative nulle au test zéro.
- **Motifs, critère par critère** :
  - critère 9 : gain statique −0,2208 % de y par point de taux, Δr̄ +96 pb, traîne d'inflation de 3,8 point-années (contre 36,7) ;
  - critère 8 : rayon 0,997486, stable à 0, 2 et 10 %, pire cas de la grille 0,998883 ;
  - critère 18 : #56 tenue ;
  - critère 7 : aucun gain du bloc 9 ;
  - critère 13 : la plus faible dépendance à π̄ des options sûres, et aucun impôt sur les intérêts nominaux (critère 13 (c)) ;
  - critère 19 : un paramètre et une variable d'état.
- **Valeur par défaut du levier budgétaire en pays joué** (C47) : « suivre la règle » = C-HS avec T9.
  - φ\* sous l'assiette HS : 0,131 à 2 % et 0,487 à 10 % ; ≤ 0 à 0 %. L'assiette HS donne donc **une marge de stabilité que l'assiette WB n'a pas** (φ\* de 0,905 à 0,986).
  - « Leviers tenus » (E) est un écart déclaré, avec la mention « charge d'intérêts financée par le déficit » : instable à 2 % (1,001818) et à 10 %.
- **Écartées** :
  - A, instable à sa pente d'origine ;
  - B, qui fait de la dette l'ancre du taux réel (r̄ −2,03 points par point de cible), avec un historique et des drapeaux ;
  - D, arrivée fonction de φ_b (critère 7) ;
  - F, divergente sous taux tenu.

### Critère 13 de la fiche 8 (C15), réponse demandée

**Établi sur la maquette** : aucune règle recommandable de la fiche 9 ne le tient au seuil de 0,1 point. C-HS en est à 0,46 point sur r̄ et à ±0,45 point sur C/PIB. Les sources restantes sont hors de la fiche 9 (§ 3.Q). La seule règle qui le tient, F, diverge sous taux tenu.

Voies au mainteneur, comme au § 6.3 de la fiche 8 :
- (a) une correction prospective du critère 13, l'ancien verdict restant publié ;
- (b) la réouverture conjointe de C30 (M28), de la conversion linéaire (M22, ADR 0008) et des écarts nominaux (M31, critère 4 (c) de la fiche 7) : résidu de 0,019 point. Toute réouverture partielle aggrave l'écart. ~~Même alors, l'écart est de 0,10 à 0,11 point : la voie (b) ne suffit pas seule.~~ (corrigé, C57).
- (c) voie de `monnaie` (§ 6.3) : critère gardé, échec déclaré comme défaut connu, codé en échec attendu au J3, issue. Avis de `macro` (relance du 04/10/2026) : favorable.

Je ne propose aucun seuil nouveau.

**Deux lectures du critère 13** (à trancher) :
- (α) paramètres fixés (s_G fixé, r̄ résidu) : lecture appliquée ci-dessus ;
- (β) état résolu à chaque π\* en lecture (1), r̄ donné : r̄ est alors invariant par construction ; s_G +0,110 point de 0 à 10 % ; C/PIB −0,662 point, dont la valorisation des stocks (C30). Mesure : `uv run python` sur `lib9`, sortie au compte rendu.

Avis : (α) est la seule lecture qui teste quelque chose.

### Options renvoyées à M33 (avis, non tranchées)

- **Lignes 19a** : A8, comme recommandé au § 2. Il exige que s_CB soit écrit par le bloc 8 en phase 1 ; le cas à la main (C-7) le montre exécutable et triangulaire.
- **i_B** : (i) i_B ≡ i_CB. La variante V (taux apparent) n'apporte pas de stabilité au pays joué (§ 3.V) ; je la renvoie au J6 avec la prime.
- **M^G\* et contrôle de caisse** : m = 1 (interprétation), avec la lecture nette du contrôle.
  - Constat : la marge plafonne une hausse de dépense au premier tour à 0,37 % à π̄ = 0, 3,34 % à 2 % et 20,6 % à 10 %. La dépense +5 % du scénario de `jeu` serait rationnée d'environ 1,5 % au premier tour à 2 %.
  - Si `jeu` juge ce rationnement non lisible, m > 1 est une **modification** (borne de la l. 502, décision citant M22). À trancher avec `jeu`.
- **E^CB_0 = 0** : favorable. La dette consolidée égale alors B − M^G, et Π^CB = i_CB M^G/n_a.
- **P2** : lecture (i), garder M^G\* comme encaisse visée.

### Réserves et conditions (à vérifier au premier essai)

Numérotées C51 à C56 sous réserve de l'ordre réel d'intégration.
- **C51 (C49)** : la racine parasite de r̄ (≤ −7,5 %) est exclue par une condition de domaine déclarée en `\limites`. Son voisinage dynamique est à mesurer au J3.
- **C52 (C50)** : θ_H est republié au sens de la l. 1543 (0 sous HS) et sous le sens « vente imprévue » (0,498). La boucle de `sec:menages` est à refaire avec les impôts.
- **C53** : la maquette n'exécute ni le plafond de caisse, ni Tr > 0, ni τ_F > 0. Le J3 mesure le scénario G +5 % avec le plafond.
- **C54 (critère 17 (d3))** : la dette restituée monte de 0,473 point au tour 12 sous la règle, sous le seuil de 0,5 point. Elle monte de 0,603 point en pays joué. Je signale l'écart à `jeu` sans changer le seuil.
- **C55** : ratio de dette bas (environ 26 % du PIB) : calibration de ν_H au J3, sur des sources (critère 22).
- **C56** : symboles proposés au critère 21 :
  - τ_H, Y^{pre}_H, i^{ref} (ou ϱ^{ref}) et T^{rep} pour la reprise : 0 occurrence chacun dans le `.tex` (`grep -c -F`) ;
  - s_G : 4 occurrences de la chaîne, dont « mesures_G_K » ; à vérifier par `docwriter` ;
  - m est déjà pris : le multiplicateur d'encaisse, s'il existe, prendra κ_G (0 occurrence).
- **C57 et C58** : corrections reçues de `monnaie` et intégrées au § 3.Q, au § 3.0 et au § 3.C-7 (04/10/2026), remesurées par `macro`.

### Lectures possibles

- (a) Assiette HS contre assiette Y : un écart de dynamique de 0,1 % au plus ; HS supprime l'impôt sur la part inflationniste des intérêts. Avis : HS.
- (b) T_F : τ_F = 0 au socle, l'assiette HS imposant les dividendes distribués, contre un τ_F actif. Avis : τ_F levier, valeur indicative 0.

### Questions pour `monnaie`

1. A8 et i_B ≡ i_CB sous C-HS : accord ? Π^CB = i_CB M^G/n_a est négatif si i_CB < 0 : quelle ligne pour la part non couverte ?
2. T9 réel reste non nul dans les états déplacés (r̄ ≠ r^ref après un choc permanent) : est-ce compatible avec la règle SN de la fiche 8 ?
3. Les écarts ϖ_L et ϖ_D nominaux sont l'une des trois sources du critère 13 : accepteriez-vous des écarts réels (décision citant M31) ?
4. Option F : la lecture de r̂\* par le bloc 9 est-elle recevable ? Partagez-vous le constat de divergence sous taux tenu ?
5. Leeper : C-HS est-elle « passive » au sens de Leeper (1991), et E « active » ?
6. B est stable ici, contrairement à la cible intégrale de B/PIB de la fiche 6 § 6.6 : différence de forme (PI sur le déficit) ou de maquette ?
7. Valeur stationnaire de s_CB (B_CB/B) sous l'option C de la fiche 8 ?
8. Variante V : la part détenue par la banque centrale qui se reprice immédiatement (critère 10 (c)) suffit-elle à la renvoyer au J6 ?

### Questions pour `jeu`

1. L'assiette de Haig-Simons, « impôt sur le revenu ; les intérêts ne sont imposés qu'au-delà de l'inflation visée », est-elle lisible ? Quel libellé pour T9 (« reprise des intérêts ») ?
2. Valeur par défaut « suivre la règle » avec reprise, et « leviers tenus » en écart déclaré : faut-il exposer la part reprise φ comme levier, puisque φ\* vaut 0,13 à 2 % et 0,49 à 10 % ?
3. M^G\* = paiements bruts : une hausse de dépense au-delà de 3,3 % (2 %) ou de 0,37 % (π\* = 0) est rationnée au premier tour. Coût visible acceptable, ou faut-il m > 1 ?
4. Sur-commande (#53) : plafond de caisse et éviction proportionnelle de C et de I, avec « dépense demandée et exécutée » : suffisant ?
5. Seuil (d3) : 0,473 point sous la règle, 0,603 en pays joué : lecture du seuil ?
6. Après une dépense permanente : glissement +0,161 au tour 120 et +0,085 au tour 240 (contre +0,238 et +0,224) : acceptable ?
7. Taux tenu un point bas : palier +0,396 au tour 120 puis +0,596 au tour 2 400 : un nouveau palier lisible ?
8. Option F : elle ramène le taux neutre à sa référence après un choc permanent, mais diverge si le taux est tenu. Confirmez-vous qu'elle est à écarter ?

### Recommandation en une phrase

Retenir C-HS (reprise réelle intégrale des intérêts, impôt sur le revenu de Haig-Simons retardé, dépense en volume indexée sur la production potentielle) comme règle de référence et valeur par défaut du levier budgétaire, avec le socle commun (A8, i_B ≡ i_CB, M^G\* = paiements bruts, E^CB_0 = 0), et porter au mainteneur le constat qu'aucune règle recommandable de la fiche 9 ne tient le critère 13.

## 6. Avis de l'expert consulté

*Rédigé par `monnaie` le 04/10/2026, comme expert consulté sur trois sujets :*
- *la frontière dette publique : placement, prime, i_B ;*
- *la banque centrale : Π^CB, s_CB, M^G\* ;*
- *la règle de taux et l'option F.*

*Avis porté sur la fiche à l'état `18d2868` (branche `claude/j1-monnaie-etat`, PR #77). Les conditions nouvelles sont numérotées C57 à C63 (§ 6.6), à la suite de C51 à C56 du § 5, sous réserve de l'ordre réel d'intégration.*

*Sources lues :*
- *fiche 9 : § 1 (identités de la dette et de Domar), § 1.1, § 1.4, critères 6 et 8 à 13 avec leurs amendements, § 3 à § 5 ;*
- *fiche 8 : critères 2 et 13, § 5, § 6.3, § 6.6 ;*
- *fiche 7 : critère 4 (c), § 6.1 (Q5, Q8) ;*
- *fiche 6 : § 6.6 et l. 1476 (cible intégrale de B/PIB) ;*
- *fiche 3 : forme SN (`travail.md` l. 324) ;*
- *ADR 0008, I.2 ;*
- *maquette conjointe de `macro` (`m9.py`, empreinte `cbe8da70131a4464`, et `lib9.py`), lue en entier.*

*Calculs :*
- *Les essais sont faits dans un répertoire créé par `mktemp -d` (`…/scratchpad/mon9.Jgu8/`, scripts `qa.py` à `qj.py`, sorties `*.out`). Commande : `/home/user/projet_macro/.venv/bin/python <script>`.*
- *Ils importent `m9.py` et `lib9.py` de `macro` sans les modifier, avec une exception : une copie de `m9.py` ajoute une seule ligne, la règle intégrale pure de la Q6 (`diff` : ligne 191).*
- *Ce sont des **ré-exécutions du même code**, pas une contre-épreuve indépendante.*
- *Les sorties sont des résultats de modèle, sans statut de fait.*

### 6.1 Réponses aux huit questions de `macro`

**Q1 — A8 et i_B ≡ i_CB sous C-HS : accord. Un Π^CB négatif est couvert par l'émission sous α ; la ligne nommée ne joue qu'en cas de placement raté.**
1. **Neutralité de la composition du bilan de la banque centrale.**
   - Sous (i) et i_res = i_CB, l'identité du critère 2 (b) de la fiche 8 se réduit à Π^CB = i_CB(M^G + E^CB)/n_a, quels que soient B_CB, L^CB et Res.
   - Mesure (`qb.py`) : avec s_CB = 0,05 puis 0,5 au lieu de 0, l'écart relatif maximal sur y, p, i, C, YD et T_H, sur 240 tours, vaut 2,2e−16 puis 3,3e−16.
2. **Signe de Π^CB.**
   - Sous E^CB = 0, Π^CB < 0 si et seulement si i_CB < 0.
   - C'est atteignable : la règle n'a pas de plancher (fiche 8, lecture (b)), et i_CB stationnaire vaut 1 % à π̄ = 0.
   - Mesure (`qb.py`), avec i_CB tenu à −0,5 % pendant six tours :
     - Π^CB = −1,18e−4 par pas, soit i_CB·M^G/n_a ;
     - M^G clôt à M^G\* (écart 0) ;
     - E^CB par le stock de clôture vaut 0.
   - Le besoin de la phase 7 contient −Π^CB (`m9.py:184`), calculé en phase 1 (`m9.py:118`). La perte est donc financée par l'émission avant la ligne 16 de 8 (b).
3. **Part non couverte.** Elle n'existe que si deux conditions se réunissent au même tour : i_CB < 0, et un placement raté (entrée ς_B de M31, ou limite C22).
   - J'approuve le point 3 de N-3 : une ligne nommée « perte de la banque centrale non couverte », proposée par le bloc 9 (payeur) en 8 (b), en dernier, sans créance. Sa contrepartie est une baisse de E^CB : la banque centrale constate la perte.
   - À déclarer : ensuite E^CB < 0, et ce niveau reste constant sous M22 (d).
     - Π^CB devient négatif même à i_CB > 0 dès que −E^CB > M^G.
     - La condition E^CB ≥ 0 du critère 2 (b) de la fiche 8 est rompue.
     - La recapitalisation relève du J6.
   - Cas à la main (ii) du critère 12, au J3 (C60).

**Q2 — T9 réel non nul dans les états déplacés : compatible avec la règle de salaire SN (M25) et avec la règle de taux de la fiche 8.**
1. **Mesure** (`qc.py`, `qh.py`), après G +1 % permanent, au tour 5 500 :
   - π − π\* = −1,0e−10 ; prescription − i = 0 ;
   - U − U^eq = −1,1e−11 ; part salariale rapportée à la référence : 5,7e−13 ;
   - Δi = +0,981 point (Fisher : +0,96, soit les +96 pb de `macro`) ;
   - T9/PIB = +0,276 % en permanence ; T_H/PIB = 22,16 %, contre 21,68 %.
2. **Raisons.**
   - SN lit π^e, U et la part salariale avant impôt : T9 n'y entre pas.
   - La règle de la fiche 8 lit π et r̂\* : T9 n'y entre pas non plus.
   - T9 est une fonction de niveau de i − i^ref, sans action intégrale, avec φ fixe : aucun continuum.
   - r^ref est une constante de l'état résolu, non une estimation. T9 ne lit donc aucun estimateur sans ancre (instabilité 4), contrairement à F (Q4).
3. **Deux déclarations.**
   - (a) Après un choc permanent, l'impôt apparent reste déplacé (T9 ≠ 0). T9 doit être restitué à part (§ 6.7).
   - (b) Sous taux tenu, T9 transmet le taux au budget : il devient négatif si le taux est tenu bas. Cela contribue au palier mesuré par `macro`, +0,396 au tour 120 et +0,596 au tour 2 400, contre +0,155 et +0,085 sous la règle provisoire (non remesuré ici).
     - Cela rapproche le modèle de l'intention du 17/09/2026 (fiche 8 § 5, point (3)).

**Q3 — Écarts ϖ réels : non pris seuls. Une décision citant M31 n'a de sens que dans un ensemble.**
1. **La mesure du § 3.Q est à corriger.**
   - L'option `spreadreal` (`m9.py:44`) met à l'échelle ϖ dans le revenu stationnaire seulement.
   - Or les écarts sont neutres pour le revenu agrégé (fiche 7 § 6.1, Q5). La neutralisation n'a donc rien mesuré : r̄ est identique à quatre décimales (`qa.py`).
   - Le canal réel est le taux du crédit lu par S-ζ. Avec un écart nominal, ϱ_L = r + ϖ_L/(1 + π̄), qui dépend de π̄ (`m9.py:127` ; `lib9.py:5, 20, 26`).
   - Avec ϖ_L(1 + π\*)/1,02, ϱ_L − r est invariant.
2. **Mesures** (lecture (α), C-HS ; `qe.py`, `qg.py`, `qj.py`) :

   | Neutralisé | r̄ à π\* = 0 | r̄ à 10 % | Écart |
   |---|---|---|---|
   | rien | 1,5363 % | 1,0750 % | 0,461 |
   | écarts, complets | 1,5697 | 1,0018 | 0,568 |
   | C30 + conversion | 0,9757 | 1,0879 | −0,112 |
   | conversion + écarts | 1,6086 | 0,3121 | 1,297 |
   | C30 + écarts | 0,9729 | 1,4025 | −0,430 |
   | **les trois, complets** | **1,0039** | **0,9853** | **0,019** |

3. **Fond économique.**
   - Un écart réel constant est la cohérence de Fisher exacte avec S1, qui lit ϱ_L sous forme de Fisher.
   - Aucune source que j'ai lue n'établit la dépendance de long terme des écarts à l'inflation.
   - Côté dépôts, Drechsler, Savov et Schnabl (2017, *QJE* 132(4), p. 1819-1876 ; résumé retrouvé, texte non lu) trouvent que les banques américaines **élargissent** l'écart sur dépôts quand le taux directeur monte. Cela ne soutient ni l'écart nominal constant, ni l'écart réel constant. **Contesté** à long terme.
4. **Contrat.**
   - Des écarts réels contrediraient la lettre du critère 4 (c) de la fiche 7, que j'ai écrit : écarts i_L − i_CB et i_CB − i_D identiques à 1e−10 près pour π̄ ∈ {0 ; 2 ; 10 %}.
   - Ils contrediraient aussi M31 (écart constant).
   - Il faudrait une correction prospective de ce critère et une décision citant M31 (C63).
5. **Verdict : non.** Seuls, ils aggravent l'écart (0,461 → 0,568). Ils ne servent qu'à l'intérieur de la voie (b) complète (§ 6.3).

**Q4 — Option F : la lecture de r̂\* est recevable techniquement, mais l'option est à écarter, car elle réintroduit l'instabilité 4 par le budget.**
1. **Techniquement**, r̂\* est une variable d'état d'ouverture du bloc 8 : la lecture est triangulaire, sans cycle. Mais elle transforme un estimateur interne du bloc 8 en contrat d'interface, que la fiche 8 n'a pas publié comme tel.
2. **Divergence confirmée** (`qc.py`, k_F = 0,01, taux tenu −1 point) :
   - glissement +0,345 / −0,591 / +1,045 / +3,238 aux tours 120 / 600 / 1 200 / 2 400 ;
   - prescription − taux tenu = +2,10 / +0,78 / +1,73 / +4,95 points.
3. **Mécanisme.**
   - Sous taux tenu, r̂\* intègre encore l'écart d'inflation sans agir sur le taux : c'est un estimateur sans ancre, l'instabilité 4 du critère 8 (a).
   - F intègre cet estimateur dans τ_H. On obtient une double action intégrale sur l'inflation, portée par le budget.
4. **Pas de contournement admissible.**
   - Geler r̂\* sous taux tenu serait un drapeau de mode (ADR 0002).
   - F deviendrait en outre inerte précisément quand le joueur se sert du levier de taux.

**Q5 — Leeper : la classification ne vaut que par analogie, et le mécanisme diffère.**
1. **Ce que je sais du texte.**
   - Leeper (1991), *JME* 27(1), p. 129-147 : existence vérifiée (IDEAS, sans résumé) ; texte non lu.
   - Selon le résumé retrouvé par moteur de recherche : le taux répond à l'inflation, un impôt forfaitaire répond à la dette réelle, et deux régimes en découlent, monnaie active et budget passif, ou budget actif et monnaie passive.
2. **C-HS est « passive » par analogie.** Le solde primaire absorbe le surcroît d'intérêts que la politique monétaire induit (φ = 1), si bien que le signe de #56 est tenu.
   - Mais T9 ne répond pas au niveau de la dette (∂T9/∂b = i − i^ref = 0 à la référence) : au sens de Leeper, la réponse à la dette est nulle.
   - La dette est stable par r̄ < g (boucle propre 0,999214) et par les normes privées. Le modèle de Leeper, sans croissance, ne couvre pas ce cas.
3. **E est « active » par analogie.** Mais sa divergence (1,001818 à 2 %) ne vient pas d'une dette explosive, puisque la boucle de Domar est stable. Elle vient de la boucle rentière combinée à l'action intégrale monétaire.
4. **Côté monétaire**, a_π = 0,5 < 1 et l'ancre vient de l'action intégrale : ni l'un ni l'autre n'est dans Leeper.
5. **Rédaction proposée** : « dominance budgétaire, par analogie avec Leeper (1991) ; mécanisme : canal rentier, non explosion de la dette ».

**Q6 — Option B stable, contrairement à la cible intégrale de la fiche 6 : c'est une différence de forme, établie sur la même maquette.**
1. **Mesure.** Copie de `m9.py` à une ligne : τ ← τ + (k_B/n_a)(b − b̄), forme de la fiche 6 l. 1476, sans T9 (`qd.py`).

   | Réglage | Rayon | Période |
   |---|---|---|
   | k_B = 0,05 | 1,004152 | 484 tours |
   | k_B = 0,2 | 1,004713 | 235 tours |
   | k_B = 1 | 1,008681 | 106 tours |
   | Option B (λ_τ = 1), même maquette | 0,997149 | — |
   | Intégrale pure k_B = 0,2 avec T9 HS | 0,998976, stable mais lent | 235 tours |

   L'intégrale pure est explosive et oscillante, comme à la fiche 6 § 6.6.
2. **Explication.**
   - La dette intègre les déficits. Une action intégrale seule sur la dette fait donc une double intégration, d'où l'oscillation.
   - La cible de déficit de B donne d − d\* ≈ n_a Δb + (n_a(Γ − 1) + κ)(b − b̄) : un terme proportionnel sur b, qui amortit.
   - De plus, comme le déficit contient i_B B/n_a, B reprend la charge d'intérêts avec un délai 1/λ_τ : c'est un T9 implicite.
3. **Aucun désaccord avec la fiche 6.** B reste écartée pour les motifs du § 5.

**Q7 — Valeur stationnaire de s_CB : 0 au socle. B_CB/B tend vers s_CB, ce qui est neutre pour les allocations mais pas pour la position dans le corridor.**
1. **Convergence.** Sous A8 en croissance équilibrée, B_CB/B tend vers s_CB.
   - Mesure : 0,0274 au tour 240 pour s_CB = 0,05, depuis B_CB,0 = 0.
   - C'est conforme à s_CB(1 − Γ̄^−240) = 0,05 × 0,547.
2. **Seuil de position.** Au-delà de s_CB = M^G/B, soit 0,0686 à 2 % sous C-HS, la banque centrale détient plus de titres que le compte du Trésor.
   - On passe alors à Res > 0 et L^CB = 0 à la clôture. À s_CB = 0,5 : Res/M^G = 2,99 au tour 240.
   - Sans effet sur les revenus sous i_res = i_CB, mais la position nette de la banque (ligne 21, M31) change de signe. À déclarer (C59).
3. **Recommandation.** s_CB est un paramètre d'archétype, valant 0 au test zéro (fiche 8 § 1.5, Q7). Des valeurs non nulles ne prennent sens qu'au J6, avec la prime, quand elles cessent d'être neutres.

**Q8 — Variante V : renvoi au J6 approuvé, mais pas pour ce seul motif.**
1. Le critère 10 (c) est **vide au socle** : avec s_CB = 0, B_CB ≡ 0, et il n'y a rien à « repricer ».
2. Les motifs réels sont :
   - (a) aucun gain de stabilité pour le pays joué : 1,001266 contre 1,001818 (mesure de `macro`) ;
   - (b) i_B ≠ i_CB ajoute (i_B − i_CB)B_CB/n_a à Π^CB. Cela rouvre le point 1 de #26 et la condition Π^CB ≥ 0, et rend s_CB non neutre. C'est donc un levier d'achats, qui relève du J6 ;
   - (c) une décision citant M22 (l. 548) serait nécessaire ;
   - (d) un taux apparent rétrospectif, sans prime ni anticipations, n'est pas une structure par terme. Il est à instruire avec la prime.

### 6.2 Contrôle des chiffres de mon domaine (ré-exécution du même code)

| Grandeur | Publiée (§ 3 à 5) | Ré-exécution | Verdict |
|---|---|---|---|
| r̄ critère 13, C-HS, (α) | +1,536 / +1,075 % | +1,5363 / +1,0750 % | conforme |
| C/PIB, écart de 0 à 10 % | +0,435 / −0,473 | 0,908 | conforme |
| C30 + conversion neutralisés | 0,976 / 1,088 % | 0,9757 / 1,0879 % | conforme |
| « Les trois » neutralisés | 0,112 point | 0,112 en neutralisation incomplète ; **0,019 en neutralisation complète** | **écart de méthode** (Q3) |
| Option F, taux tenu, glissement | +0,345 / −0,591 / +1,045 / +3,238 | idem | conforme |
| φ\* sous HS à 2 % et 10 % | 0,131 / 0,487 | 0,1305 / 0,4871 | conforme |
| Pays joué E-HS | 1,001818 / 1,011036 | idem | conforme |
| Option B (λ_τ = 1) | 0,997149 | idem | conforme |
| Marche de π\* de 2 à 3 %, r̄ | 0,8788 % (tour 2 400, simulation) | 0,8784 % (stationnaire) | conforme |
| E^CB, cas à la main de C-7 (s_CB = 0,5) | « E^CB = 0 » | `main9.py` affiche −3,46e−02 ; le stock de clôture donne 0 | **écart de traçabilité** (C58) |

L'écart de traçabilité E^CB vient du diagnostic `ECB` de `m9.py:209`, qui somme B_CB d'**ouverture** avec L^CB, Res et M^G de clôture.
- Mesure (`qf.py`) : la sortie vaut −1,5e−03 et −1,5e−02 au tour 240 pour s_CB = 0,05 et 0,5, contre 2e−16 et 4e−16 par le stock de clôture.
- La dynamique n'est pas atteinte. Le contrôle du § 3.0 (« E^CB = 0 à 5,6e−17 ») ne vaut que pour s_CB = 0.

### 6.3 Critère 13 de la fiche 8 (C15) : avis pour la décision par paire

1. **Verdict (α) publié : échec.**
   - L'écart de r̄ vaut 0,461 point entre π̄ = 0 et 10 %. Celui de C/PIB vaut 0,908 point.
   - La lecture (β) échoue aussi, sur s_G (+0,110 point) et sur C/PIB (−0,662 point), mesures de `macro` non refaites : la lecture ne change pas le verdict.
   - **Avis : (α)**, seule lecture qui teste une statique comparative à paramètres structurels fixés. En (β), s_G, levier budgétaire, devient une variable de calibration.
2. **Diagnostic de `macro` : accord sur l'attribution, désaccord sur le résidu.**
   - La dépendance vient entièrement de trois conventions hors des blocs 8 et 9 : C30 (M28), la conversion linéaire des taux de flux (M22, ADR 0005 point 4, confirmée par l'ADR 0008, I.2) et les écarts nominaux (M31).
   - Une fois les trois complètement neutralisés, l'écart maximal de r̄ sur [0 ; 10 %] vaut 0,019 point (`qi.py`), et non 0,11. Ni C-HS ni la règle de la fiche 8 ne laissent de résidu matériel.
3. **Contribution de chaque source, les deux autres neutralisées** (r̄ à π\* = 0 / 1 / 2 / 3 / 4 / 10 %, `qj.py`) :

   | Source gardée | 0 | 1 % | 2 % | 3 % | 4 % | 10 % |
   |---|---|---|---|---|---|---|
   | C30 seule | 1,609 | 1,244 | 1,000 | 0,827 | 0,697 | 0,312 |
   | Conversion seule | 0,973 | 0,983 | 1,000 | 1,025 | 1,057 | 1,402 |
   | Écarts seuls | 0,976 | 0,988 | 1,000 | 1,012 | 1,023 | 1,088 |

   - C30 domine (−1,30 point). C'est une non-neutralité comptable porteuse de sens : le levier et les stocks sont à la valeur comptable.
   - La conversion (+0,43) est un artefact de convention. Les écarts pèsent +0,11.
   - **Les effets se compensent.** Rouvrir une seule convention, ou deux, porte l'écart entre 0,43 et 1,30 point (tableau de la Q3).
4. **Le critère, mesuré aux bornes, sous-estime la dépendance.** Le profil tel quel est non monotone (`qi.py`) :
   - r̄ = 1,536 / 1,203 / 1,000 / 0,878 / 0,813 / 0,799 / 1,075 % à π\* = 0 / 1 / 2 / 3 / 4 / 6 / 10 % ;
   - l'écart maximal vaut 0,74 point ;
   - **une marche de cible de 2 à 3 % déplace r̄ de −0,12 point**, au-delà du cran d'affichage. Ce point est à porter à `jeu`, avant l'ouverture du levier de cible (#54).
5. **Deux lectures du « seuil de matérialité ».** J'ai proposé ce seuil.
   - Mon intention était un seuil sur la **dépendance totale** : moins d'un cran d'affichage.
   - Le texte admet une seconde lecture, où le seuil fixerait ce qu'il faut attribuer. L'adopter après observation déplacerait le critère : je ne la soutiens pas.
6. **Voies pour la décision par paire.**
   - **(a) Correction prospective**, l'ancien verdict restant publié : le seuil de 0,1 point porterait sur le résidu, une fois les conventions déclarées neutralisées dans le script de mesure.
     - Elle serait tenue (0,019).
     - Mais elle change ce qui est testé et laisse une dépendance perceptible près de la référence (point 4).
   - **(b) Réouverture.** Seule la réouverture conjointe des trois conventions atteint le seuil :
     - M28 (C30, `macro`) ;
     - M22 / ADR 0008 I.2 (conversion, `architect`) ;
     - M31 et le critère 4 (c) de la fiche 7 (écarts, `monnaie`).
     - Toute réouverture partielle aggrave l'écart. Le coût est élevé, et C30 n'est pas un artefact.
   - **(b′) Écarts réels seuls** : écartée (0,568 point).
   - **(c) Ma recommandation : garder le critère 13 tel qu'écrit et décider M33 avec l'échec déclaré comme défaut connu du socle.**
     - Le défaut est attribué, chiffré par source et suivi par une issue (proposée en fin de compte rendu).
     - Il est codé en échec attendu au script d'état stationnaire du J3 (P16 (a)).
     - Aucune réouverture n'a lieu sur cette branche. L'issue instruit, au J3, s'il faut traiter C30 ou la conversion, avec une remesure conjointe (C61).
     - **Motif** : le critère protège une propriété perceptible en jeu (point 4). Le redéfinir pour qu'il passe la masquerait. (a) reste acceptable si elle est rédigée pour ce qu'elle est.
7. **M32.** Retenir l'option C de la fiche 8 sur ses propres critères : l'échec du critère 13 ne lui est pas imputable (fiche 8 § 6.3, point 2, confirmé).

### 6.4 Options renvoyées à M33 et stabilité du pays joué

- **A8 : favorable.**
  - s_CB est écrit par le bloc 8 en phase 1. C'est un paramètre d'archétype, valant 0 au socle, avec une contrainte de domaine [0 ; 1].
  - La position Res/L^CB est déclarée au-delà de M^G/B (Q7).
- **i_B ≡ i_CB, lecture (i) : favorable.**
  - Prime nulle déclarée ; corridor dégénéré au socle (i_res = i_B = i_CB) ; délai 0 des lignes 11b et 11c.
  - C'est ce qui rend Π^CB = i_CB(M^G + E^CB)/n_a et s_CB neutre (Q1, Q7).
  - Prime, durée et achats au J6 (Q8).
- **M^G\* = paiements bruts, m = 1, lecture nette : favorable comme interprétation.**
  - **Du côté monétaire, m est neutre pour les revenus sous (i).** Un surcroît x d'encaisse est financé par x de titres :
    - l'État paie i_B x/n_a et en reçoit i_CB x/n_a par Π^CB ;
    - la banque finance x par L^CB, reçoit i_B x et paie i_CB x.
    - Le solde est nul. C'est une algèbre : m n'est pas un paramètre de `m9.py`, donc **non mesuré**.
  - Seul le niveau de L^CB change : L^CB = M^G − B_CB (cas de `main9.py` : 0,316582 − 0,034613 = 0,281969).
  - Le plafond de premier tour dépend de π̄ : 0,37 % à 0, 3,34 % à 2 %, 20,6 % à 10 %. C'est une question de `jeu`. Si `jeu` demande m > 1, je n'ai pas d'objection monétaire ; c'est une modification de la l. 502 citant M22.
- **E^CB_0 = 0 : favorable.** C'est la forme (ii) du critère 2 (a) de la fiche 8, et la condition de Π^CB ≥ 0 à i_CB ≥ 0.
- **P2 : (i)**, garder M^G\* au sens d'encaisse visée.
- **Stabilité du pays joué.**
  - φ\* est confirmé : ≤ 0 / 0,1305 / 0,4871 à π̄ = 0 / 2 / 10 %.
  - Sans reprise (E-HS), l'écart double en 382 tours (≈ 32 ans) à 2 % et en **63 tours (≈ 5 ans) à 10 %** (`qg.py`).
  - Recommandation, en trois points :
    - la reprise est automatique (φ = 1), et le levier d'impôt du joueur est τ_H, T9 s'y ajoutant ;
    - φ n'est **pas** exposé comme levier, son seuil de stabilité bougeant avec π̄ : ce serait un mur invisible ;
    - « leviers tenus » ne serait qu'un écart déclaré, sur avis de `jeu`, avec l'indicateur « charge d'intérêts financée par le déficit ».

*Complément de `monnaie` du 04/10/2026, après l'avis de `jeu` (§ 7) :*

**M^G\* et le multiplicateur m, après l'avis de `jeu` (cliquet à π̄ = 0)**

1. **Je reçois le constat de `jeu` sans le remesurer.** `jeu` l'a mesuré sur une copie de `m9.py` à laquelle il a ajouté le plafond G^plan ≤ M^G d'ouverture :
   - une baisse de 5 % pendant 12 tours, suivie d'un retour, reste rationnée 79 tours à π̄ = 0 ;
   - m = 1,1 supprime tout rationnement dans ces scénarios.

   Le mécanisme est confirmé par la forme fermée. Le plafond limite la hausse de G d'un tour au suivant à m/(Γ̄·s_G) − 1, où s_G = G/P (P : paiements bruts du pas) vaut 0,99467 à π̄ = 0, 0,96342 à 2 % et 0,78637 à 10 %. À π̄ = 0, les intérêts ne pèsent presque rien dans P, si bien que la dépense ne peut presque pas remonter.

2. **Effet sur Res et L^CB (critère 11 (e)).**
   - Sous E^CB = 0, s_CB = 0 et la position nette de la banque (M31), Res reste nul à la clôture et L^CB = M^G = m·P.
   - Passer de m = 1 à m = 1,1 relève L^CB de 0,1·P, soit environ +0,0019 année de PIB à 2 %. Pour mémoire, M^G/(12 PIB) vaut 0,018904 à m = 1.
   - L'identité du critère 11 (e) tient : Res − L^CB baisse de (m − 1)P.
   - Le seuil de s_CB au-delà duquel Res devient positif monte avec m : il vaut m·M^G/B, soit 0,0686 × m à 2 % (C59 à lire avec ce facteur).

3. **Effet sur les revenus : nul au socle.**
   - Sous i_B = i_res = i_CB, l'encaisse supplémentaire est financée par des titres.
   - L'État paie i_B(m − 1)P/n_a et reçoit autant par Π^CB, qui vaut i_CB·M^G/n_a.
   - La banque finance les titres par L^CB, au même taux.
   - Ce résultat vient d'une algèbre et n'est pas mesuré : m n'est pas un paramètre de `m9.py`.
   - **Au J6** (prime, durée, i_B ≠ i_CB), le portage de l'encaisse coûtera (i_B − i_CB)(m − 1)P/n_a par pas. Ce coût est à déclarer.

4. **Valeur de m : un calcul de premier tour sur la forme fermée, non une mesure.**
   - Pour la propriété « hausse de 10 % de la dépense d'un tour au suivant sans rationnement », il faut m ≥ 1,10·Γ̄·s_G, soit **1,0959** à π̄ = 0, 1,0633 à 2 % et 0,8733 à 10 %.
   - Pour le retour après une baisse de 5 %, il faut environ m ≥ Γ̄·s_G/0,95, soit 1,0488 à π̄ = 0. Ce calcul est approché : P a baissé pendant la phase basse.
   - **m = 1,1 tient donc la propriété de `jeu` avec 0,4 % de marge seulement à π̄ = 0.** Il faut confirmer m sur la maquette avec plafond, en particulier pour une cible inférieure à 0 si le levier de cible le permet.
   - Je recommande de fixer m à partir de la propriété écrite par `jeu`, avant l'essai, avec une marge déclarée, plutôt que de retenir 1,1 tel quel.

5. **Qualification.** m > 1 contredit deux passages de la spécification : la l. 502 (« n'excède pas les paiements bruts d'un pas ») et la l. 2064 (M^G\* « n'est pas un paramètre »). C'est une **modification**, ce qui exige :
   - une décision citant M22 ;
   - une annotation du point 13 de l'ADR 0005 par `architect`, dont la qualification range déjà m > 1 en modification ;
   - le constat que m est un paramètre déclaré du bloc 9.

   Je n'ai pas trouvé de règle sans paramètre qui tienne la propriété : une telle règle porterait de toute façon un niveau de marge.

**Couverture des intérêts (T9) en levier distinct : accord avec `jeu`, et amendement de C62**

- **Accord** sur la forme proposée par `jeu` : un levier propre, distinct du barème τ_H, à deux valeurs.
  - « Couverture intégrale » (φ = 1) : valeur de la règle et valeur par défaut.
  - « Intérêts financés par le déficit » (φ = 0) : écart déclaré, accompagné de ses deux précurseurs.
  - Un changement du barème garde la couverture.
- **Ce qui reste exclu, c'est un curseur continu.** Le seuil de stabilité φ\* vaut ≤ 0 / 0,13 / 0,49 à π̄ = 0 / 2 / 10 %. Les mesures de `jeu` montrent aussi qu'à φ = 0,5 et 10 %, le taux directeur devient presque inerte (P_36 −0,015 %).
- **C62, rédaction amendée** : « φ n'est pas un levier continu. La couverture des intérêts est un levier distinct du barème, à deux valeurs, 1 par défaut et 0 en écart déclaré. Sont publiés φ\* par π̄, et les temps de doublement sous φ = 0 : 382 tours à 2 % et 63 tours à 10 %. »
- À signaler : à 10 %, φ = 0 double l'écart en 5 ans environ. L'affichage des précurseurs n'est donc pas facultatif.

### 6.5 Avis général

**Favorable à l'option C-HS**, avec le socle commun du § 3.N (A8, i_B ≡ i_CB, M^G\* = paiements bruts en lecture nette, E^CB_0 = 0). Motifs dans mon domaine :
- elle neutralise le canal rentier à fréquence nulle sans lire d'estimateur (contrairement à F) ;
- elle est compatible avec SN et avec la règle de la fiche 8 dans les états déplacés (Q2) ;
- elle laisse Π^CB et s_CB neutres ;
- elle tient le signe de #56.

**Écartées** : A et B (§ 5) ; F, qui réintroduit l'instabilité 4 (Q4) ; V, renvoyée au J6 (Q8).

**Réserves** :
1. Le critère 13 est en échec, et je recommande la voie (c) (§ 6.3).
2. Il faut corriger le § 3.Q et le § 3.C-7 (C57, C58).
3. Pays joué : la reprise est automatique, sans levier φ (§ 6.4).

### 6.6 Conditions transmises

- **C57 (fiche 9, § 3.Q et § 5, `macro`).**
  - Republier la décomposition avec des écarts réels complets : revenu et taux réel du crédit lu par S-ζ (`m9.py:127`, `lib9.py:5, 20, 26`).
  - Résidu des trois sources : 0,019 point, au lieu de 0,112. Publier aussi le tableau par source et le profil de r̄ sur [0 ; 10 %].
- **C58 (fiche 9, § 3.0 et § 3.C-7, `macro`).**
  - Calculer E^CB par le stock de clôture (diagnostic de `m9.py:209`).
  - Citer pour le cas à la main une sortie qui affiche 0, non −3,46e−02.
  - Refaire le contrôle « E^CB = 0 » avec s_CB > 0.
- **C59 (fiches 8 et 9, J3).**
  - Tester la neutralité de s_CB sous i_B = i_res = i_CB.
  - Déclarer la borne s_CB ≤ M^G/B (0,0686 à 2 %), au-delà de laquelle Res > 0 et L^CB = 0 à la clôture.
- **C60 (fiche 9, critère 12 (c) ; fiche 8, critère 2 (b) ; J3).**
  - Ligne « perte de la banque centrale non couverte » : bloc 9, 8 (b), en dernier, sans créance, contrepartie −ΔE^CB.
  - Elle n'est active que si i_CB < 0 et que le placement rate au même tour. Ensuite, E^CB < 0 est déclaré, et la condition Π^CB ≥ 0 est rompue.
  - Cas (ii) du critère 12. Recapitalisation au J6.
- **C61 (critère 13, toute réouverture de C30, de la conversion ou des écarts).** Remesurer le critère conjointement sur les trois sources : elles se compensent, et une réouverture isolée aggrave l'écart (jusqu'à 1,30 point).
- **C62 (fiche 9, `jeu`, J4).** φ n'est pas un levier. Publier φ\* par π̄, ainsi que les temps de doublement de E (382 et 63 tours).
- **C63 (fiche 7, critère 4 (c)).** Si des écarts réels sont retenus un jour, corriger le critère de façon prospective (lettre nominale) et prendre une décision citant M31.

### 6.7 Points signalés à `jeu` (non tranchés)

- **Taux neutre et cible.** Une marche de cible de 2 à 3 % déplace r̄ de −0,12 point, et de +0,54 point de 2 à 0 % (§ 6.3, point 4). C'est perceptible au cran d'affichage.
- **Impôt apparent après un choc permanent.** T9 reste à +0,28 % du PIB : à restituer à part (« reprise des intérêts »).
- **Pays joué sans reprise à cible haute.** L'écart double en 5 ans environ à 10 %.
- **Plafond de caisse.** Il dépend de π̄ (0,37 % à 3,34 % à 0 et 2 %) ; m > 1 n'a pas de coût monétaire au socle.

## 7. Avis de `jeu`

*`jeu`, 04/10/2026 (issue #73, jalon 2), sur la fiche à l'état `18d2868` (branche `claude/j1-monnaie-etat`, PR #77). Réponses aux huit questions de `macro` (§ 5, l. 950 à 959).*

**Chiffres.**
- Aucun moteur n'existe encore. J'ai rejoué la maquette conjointe `m9.py` de `macro` (§ 3.0, empreinte `cbe8da70131a4464`), copiée sans modification dans un répertoire temporaire, avec mes propres scénarios vus du joueur (neuf scripts hors dépôt, 04/10/2026, interpréteur du `.venv` du projet).
- **Deux ajouts déclarés**, sur une copie distincte, pour les questions 3 et 4 :
  - le plafond du plan de dépense sur l'encaisse d'ouverture, G^plan_t ≤ M^G_t (§ 3.N-3 (1), l. 551), que la maquette n'exécute pas (C53) ;
  - une encaisse visée M^G\* = m × paiements bruts, avec m = 1 ou 1,1, et une variante indexée sur la dépense tendancielle.

  Sans ces ajouts, la copie reproduit `m9.py`.
- **Mes remesures retrouvent** les valeurs du § 3 :
  - dette restituée +0,473 point au tour 12 et +0,599 au tour 60 (G +5 % pendant 12 tours) ;
  - glissement +0,214 / +0,161 / +0,085 / −0,006 aux tours 60 / 120 / 240 / 600 (G +1 % permanente) ;
  - palier +0,580 au tour 12 et +0,396 au tour 120 (taux tenu −1 point) ;
  - rayons du pays joué 1,001818 et 1,011036 ;
  - option F : +0,345 / −0,591 / +1,045 / +3,238 aux tours 120 / 600 / 1 200 / 2 400.
- Ce sont des résultats de maquette, non des faits. Le cran d'affichage est de 0,1 point. La fenêtre de partie va de 60 à 120 tours (`docs/exigences.md`, O5, l. 41).

**Question ludique de la fiche.** Le bloc porte les trois leviers budgétaires du joueur et la contrepartie de tous les autres : chaque décision finit dans le solde et la dette. Quatre questions en découlent :
- chaque levier budgétaire a-t-il un effet identifiable, au bon tour, avec un coût visible ?
- la règle de référence est-elle une boussole que le joueur peut suivre ou quitter instrument par instrument, sans basculer à son insu dans un autre régime ?
- la dette porte-t-elle la trace des décisions, sans effacement gratuit ni signe trompeur ?
- un mécanisme comptable (encaisse, sur-commande) crée-t-il un mur ou un cliquet invisible ?

### 7.A, 7.B, 7.D, 7.E, 7.F, 7.L et 7.V (brièvement)

- **A : à revoir.**
  - Une dépense qui baisse quand la dette monte est lisible (§ 3.A-8, l. 453).
  - Mais l'écrêtage [0,6 ; 1,6] fait un mur invisible.
  - L'option est instable à 2 % (1,003214).
  - Une hausse de taux y devient expansionniste.
- **B : à revoir.**
  - Le taux d'imposition bouge sans levier du joueur : c'est une boîte noire.
  - La cible de dette devient un levier caché du taux réel (−2,03 points par point de cible).
  - L'option repose sur un historique et des drapeaux (critère 19).
- **D : à revoir.** « Plus de dette, plus d'impôt » est lisible, mais l'arrivée dépend d'un gain que le joueur ne voit pas (§ 3.D-8, l. 702).
- **E (leviers tenus, intérêts financés par le déficit) : à revoir comme valeur par défaut ; lisible comme écart déclaré** (réponse 2).
  - À 2 %, une hausse de taux d'un point pendant 12 tours relève P_36 de +0,033 %.
  - Après G +5 % pendant 12 tours :
    - à 2 %, la dérive est lente mais visible : i +0,68 point et dette +1,32 point au tour 120 ;
    - à 10 %, elle est explosive : glissement +1,09 point au tour 120, +5,95 au tour 240.
- **F : à écarter** (réponse 8).
- **L : sans objet**, ramenée à F ou à N-6.
- **V : à garder pour le J6.**
  - Une hausse de taux qui pèse sur plusieurs années serait un mécanisme lisible.
  - Mais la variante ôte la contrepartie du tour même (T9 et lignes 11b et 11c au délai 0), et elle ne stabilise pas le pays joué (§ 3.V).

### 7.C Option C-HS — reprise réelle intégrale, assiette de Haig-Simons retardée

- **Récit en une phrase** : « l'État dépense une part constante de la production potentielle et impose le revenu des ménages du mois précédent ; quand le taux des titres dépasse son niveau de référence, l'impôt couvre le surcroît d'intérêts, et il le rend quand le taux est en dessous ». Il n'y a ni seuil, ni gain caché, ni état d'arrivée réglé par une vitesse.
- **Ce que voit le joueur** (π̄ = 2 %, sans plafond de caisse, sauf mention) :
  - *taux d'imposition +1 point* : production −0,838 % au tour 8, solde sur 12 tours +0,791 point au tour 12, dette −0,529 point au tour 12 (§ 3.C-8, l. 664) ; en permanence : glissement −1,25 point au tour 12, dette −2,44 au tour 60 et −10,97 au tour 600, consommation −0,96 % au tour 60 ;
  - *dépense +5 % pendant 12 tours* :
    - production +1,445 % au tour 6, puis **−1,41 % au tour 18** ;
    - glissement +2,82 points au tour 12, puis −1,58 au tour 24 ;
    - taux directeur +1,55 point au tour 12 ;
    - dette +0,473 point au tour 12, au plus +0,693 au tour 30, sous la moitié de ce maximum au tour 193 ;
  - *hausse de taux d'un point* : T9 de +0,257 % du PIB dès le tour même. C'est la dette consolidée (0,257 année de PIB) multipliée par l'écart de taux.
- **Gagnants et perdants d'une hausse de taux.**
  - Au tour 1, le revenu disponible des ménages ne bouge pas (+0,000 %) : le supplément de dividendes de la banque est repris exactement par T9.
  - Au tour 12, il recule de 0,43 %, parce que les dividendes des entreprises endettées baissent.
  - Sous E, il **monte** de 0,39 %.
  - Le récit devient : « taux haut : l'État reprend aux contribuables ce qu'il verse aux épargnants ; les entreprises endettées perdent ».
  - Le signe contre-intuitif de #56 disparaît sous la règle.
- **Aucune remise à zéro gratuite** dans la fenêtre de partie.
  - Après une dépense transitoire, la dette reste au-dessus du contrôle jusqu'au tour 193 au moins à la moitié de son maximum. Elle revient ensuite vers le ratio que fixent les normes privées (identité du § 1).
  - C'est une transition longue, à déclarer, non un effacement.
  - Une consolidation permanente, à l'inverse, baisse durablement la dette : −11 à −16 points au tour 1 200.
- **Stratégies.**
  - Relance financée par le déficit : production d'abord, puis inflation, hausse des taux et contrecoup au tour 18.
  - Relance financée par l'impôt (G +1 % permanente et taux d'imposition +0,253 point) : aucune traîne d'inflation (+0,002 point au tour 60), mais la consommation recule de 0,33 %.
  - Consolidation : dette en baisse et désinflation (−0,84 point au tour 60).
  - Ces trois approches sont viables, avec des coûts différents et visibles. Aucune n'est dominante dans les scénarios joués.
- **Risques.**
  - *Fixer le barème éteint-il T9 ?* Le critère 19 (l. 316) le laisse lire ainsi (réponse 2, condition 1).
  - *Cliquet de l'encaisse à basse inflation* (réponse 3).
  - *Dette qui baisse quand on dépense, à 10 %* (réponse 5).
  - *Relance suivie d'une récession au tour 18* : elle est explicable par la hausse du taux (+1,55 point), à dire dans l'aide.
  - *Fenêtre longue* : après G −5 % permanente, la consommation est à −2,92 % au tour 600, alors qu'elle était à +0,02 % au tour 120. Le signe est contre-intuitif hors de la fenêtre de partie. Je le signale à `macro` pour le simulateur de 60 ans (J4), sans le juger.
- **Verdict : lisible**, sous les conditions 1 à 9.
- **Autres assiettes.**
  - C-WB est **à revoir** : traîne de 36,7 point-années, que j'avais signalée à la fiche 8.
  - C-Y est **à clarifier** : elle impose les intérêts nominaux, d'où une dépendance à l'inflation que le joueur ne peut pas attribuer.
  - C-Yhi est acceptable, mais sa traîne est plus longue (12,9 point-années).

### Réponses aux huit questions de `macro`

1. **Assiette et libellé de T9 : à clarifier.**
   - *Assiette.* Le libellé « Impôt sur le revenu des ménages » convient, avec l'infobulle : « porte sur les salaires, dividendes et intérêts du mois précédent ; les intérêts des dépôts n'y entrent qu'au-delà de l'inflation visée ».
   - Le retard d'un tour se dit dans l'infobulle : une récession ne réduit l'impôt qu'au tour suivant.
   - Le tableau du tour montre le **barème** τ_H, qui est le levier, et le **taux apparent**, c'est-à-dire l'impôt rapporté à l'assiette. Les deux ne coïncident que si T9 est nul.
   - *T9.* « Reprise des intérêts » est ambigu (reprise de quoi ?). Je propose « **couverture des intérêts** », avec l'infobulle : « quand le taux des titres publics dépasse son niveau de référence (taux réel de référence plus cible d'inflation), l'impôt couvre le surcroît d'intérêts payé sur la dette ; en dessous, il le rend ».
   - Ordre de grandeur à afficher : « un point de taux au-dessus de la référence = dette/PIB × 1 point du PIB d'impôt par an ». Mesure : +0,257 % du PIB au tour 1, pour une dette consolidée de 0,257 année de PIB.
   - Le taux de référence i^ref s'affiche à côté de i_B.
2. **φ comme levier : à revoir s'il est continu ; lisible en levier distinct à deux valeurs.**
   - Mesure, rayon et P_36 après une hausse de taux d'un point pendant 12 tours :

     | φ | 0 | 0,1 | 0,25 | 0,5 | 1 |
     |---|---|---|---|---|---|
     | π̄ = 2 % : rayon | 1,001818 | 1,000575 | 0,999076 | 0,997792 | 0,997486 |
     | π̄ = 2 % : P_36 | +0,033 % | +0,001 % | −0,045 % | −0,112 % | −0,226 % |
     | π̄ = 10 % : rayon | 1,011036 | 1,008794 | 1,005564 | 0,999488 | 0,997558 |
     | π̄ = 10 % : P_36 | +0,463 % | +0,327 % | +0,164 % | −0,015 % | −0,248 % |

   - Un curseur φ aurait une zone dangereuse qui se déplace avec l'inflation, sans signal. À φ = 0,5 et 10 %, le taux directeur devient presque inerte (P_36 −0,015 %) : le budget désactiverait en silence le levier monétaire.
   - **Préférence** : la couverture des intérêts est un **levier propre**, distinct du barème, à deux valeurs.
     - « Couverture intégrale » (φ = 1) : valeur de la règle et valeur par défaut.
     - « Aucune couverture : intérêts financés par le déficit » (φ = 0) : écart déclaré, avec la mention et deux précurseurs, l'écart au solde primaire stabilisant et l'écart de r̂\* à sa valeur initiale.
   - Le joueur qui change le barème τ_H **garde** la couverture.
   - C'est une lecture du critère 19, dont l'exemple (« sous T9 si le taux d'imposition est fixé ») laisse lire l'inverse. Elle est soumise au mainteneur.
   - Ce n'est pas un drapeau de mode : c'est une valeur de levier, d'un paramètre déjà présent (φ).
3. **Rationnement au premier tour sous m = 1 : à revoir.**
   - Mesure avec le plafond G^plan ≤ M^G d'ouverture (ajout déclaré) :

     | Scénario | π̄ = 0, m = 1 | π̄ = 2 %, m = 1 | m = 1,1 (0 et 2 %) |
     |---|---|---|---|
     | G +5 % pendant 12 tours | rationnée les 12 tours (exécuté/demandé 0,956 au tour 1) | tour 1 seul (0,985) | aucun rationnement |
     | G +10 % pendant 12 tours | 12 tours (0,913) ; **même effet que +5 %** | tours 1 et 2 (0,941 ; 0,972) | aucun |
     | G +20 % et +100 % | volume de G +2,0 % au tour 6 dans les deux cas | volume +19,0 % au tour 6 dans les deux cas | — |
     | G −5 % pendant 12 tours, puis retour | **rationnée 79 tours** (13 à 90) ; production −2,96 % ; dette −11,8 points au tour 60, contre −0,67 sans plafond | 2 tours (13 et 14) | aucun |

   - À π̄ = 2 %, le coût est lisible s'il est affiché : un tour de rationnement pour +5 %.
   - À π̄ = 0, le levier de dépense sature dès +0,37 % par tour. Une baisse temporaire devient un **cliquet** : on ne peut plus revenir au niveau antérieur pendant 79 tours, sans aucun signal. C'est un piège irréversible à l'échelle d'une partie, et une asymétrie artificielle entre pays peu et très inflationnistes.
   - Une encaisse indexée sur la dépense tendancielle (m = 1) supprime presque le cliquet (10 tours à π̄ = 0) mais rationne toute hausse pendant 12 tours : ce n'est pas la solution.
   - **Préférence** : m > 1, par exemple 1,1 (M^G/(12 PIB) passe de 0,0183 à 0,0201 à π̄ = 0), ce qui est une **modification** (l. 502, décision citant M22, § 5, l. 917). Une autre règle conviendrait si elle tient la propriété suivante, que je propose d'écrire avant l'essai du J3 : « aucun rationnement de caisse pour une hausse de dépense de 10 % d'un tour au suivant, ni au retour d'une baisse de 5 % pendant 12 tours, à π̄ ∈ {0 ; 2 ; 10 %} ».
   - Si m = 1 est retenu, le plafond de trésorerie du tour s'affiche **dans la saisie du levier**, avant la décision.
4. **Sur-commande (#53) : à clarifier.**
   - Le rationnement proportionnel du bloc production ne mord presque jamais : seulement 5 % de dépense non servie pour G doublée pendant 12 tours.
   - Le vrai coût est le prix. Le plan est en u.m. au prix attendu, si bien que l'inflation ronge le volume (glissement +11,6 points au tour 12 pour G +20 %, sans plafond).
   - Sous plafond de caisse à 2 %, l'excès au-delà d'environ 3,3 % par tour est coupé à la saisie.
   - La sur-commande n'est donc pas gratuite. Mais « dépense demandée et exécutée » ne dit pas **pourquoi** l'exécution manque : il faut décomposer l'écart en trois causes, à savoir le plafond de trésorerie (phase 2), le prix plus haut que prévu (volume obtenu sous le volume visé) et la production non servie (phase 5).
   - L'éviction de C et de I se lit sur leurs volumes, qui sont déjà au tableau.
5. **Seuil d3 : lisible ; le seuil ne bouge pas.**
   - *Lecture du texte* (critère 17 (d3), l. 314) : le seuil de 0,5 point au tour 12 et l'exigence « au-dessus du contrôle au tour 60 » portent sur la « configuration de pays joué ». Sous la règle, seul le tour de demi-retour est publié.
   - E tient le seuil : +0,603 au tour 12, +1,073 au tour 60. C-HS publie :
     - +0,473 au tour 12, soit 4,7 crans, au-dessus des deux crans du critère (h) ;
     - +0,599 au tour 60 ;
     - un maximum de +0,693 au tour 30, sous sa moitié au tour 193 (+0,471 et +0,585 avec le plafond de caisse).
   - L'intention du seuil (pas d'effacement gratuit, effet perceptible) est tenue sous la règle.
   - La valeur par défaut du levier devient la règle, alors que d3 a été écrit quand le pays joué tenait ses leviers. Je ne propose pas de déplacer le seuil.
   - **Fait nouveau, à 10 %** : sous C-HS, la dette restituée **baisse** au tour 12 (−0,153 point) et ne repasse au-dessus du contrôle qu'au tour 23. Sous E, elle monte de +0,084. L'encours, lui, monte (+2,16 %), mais le PIB nominal monte plus vite (glissement +3,0 points) et T9 suit le taux. Le joueur y lirait « dépenser réduit la dette ».
   - Ce n'est pas un critère : c'est une infobulle (condition 6). L'archétype à 10 % entre dans le scénario O2 du J4.
6. **Traîne après une dépense permanente : à clarifier.**
   - Sous C-HS : +0,214 / +0,161 / +0,085 aux tours 60 / 120 / 240, avec un taux directeur à +0,65 point au tour 120. Sous la règle provisoire de la fiche 8 : +0,238 et +0,224.
   - L'écart reste au-dessus d'un cran au tour 60 : il est signalé au titre du critère 17 (h) (iii).
   - Il est **attribuable** : la même dépense financée par le barème (+0,253 point) ne laisse que +0,002 au tour 60 et −0,006 au tour 120, au prix d'une consommation à −0,33 %.
   - Le récit au joueur : « une dépense permanente financée par le déficit entretient l'inflation et fait monter le taux pendant des années ; financée par l'impôt, elle évince la consommation ».
   - Condition 7 : l'aide le dit, et le solde primaire stabilisant le montre.
7. **Palier sous taux tenu : lisible.**
   - Taux tenu un point bas :
     - glissement +0,58 au tour 12, de +0,36 à +0,43 entre les tours 24 et 120 ;
     - production +0,21 % au tour 12, +0,04 % au tour 120.
   - Le récit tient en une phrase : « un taux tenu bas donne une inflation durablement plus haute, sans relance durable ».
   - La dérive vers +0,54 au tour 600 sort de la fenêtre de partie et reste sous deux crans.
   - La consommation à −0,48 % au tour 120 reste un signe contre-intuitif à déclarer (fiche 8, condition 8) : l'inflation ronge l'épargne, que les ménages reconstituent.
8. **Option F : à écarter, confirmé.**
   - Dans la fenêtre de partie, F ne se distingue pas de C-HS : après G +1 % permanente, glissement +0,139 au tour 120, contre +0,161, et barème déplacé de +0,03 point. Son avantage, ramener le taux neutre à sa référence, est donc imperceptible.
   - Son défaut est un piège à retardement dans le simulateur de 60 ans. Sous taux tenu, le glissement passe à −0,59 au tour 600, +1,05 au tour 1 200 et +3,24 au tour 2 400, avec un barème qui bouge seul de +0,59 puis −1,56 point.
   - Tenir le taux est un geste ordinaire du joueur, et l'impôt qui bouge seul est la boîte noire de B.

### Critère 19 : verdict par option

| Option | Décompte (§ 4, l. 556) | « Suivre la règle » comme valeur de levier | Prescription restituable au tour | Verdict |
|---|---|---|---|---|
| A | écrêtage, T^disp | sur G, multiplicatif | oui, mais avec un mur à 0,6 et 1,6 | **à revoir** |
| B | historique, 4 drapeaux, état τ | sur τ, qui bouge seul | trajectoire de τ, cible de dette qui fixe r̄ | **à revoir** |
| C-HS | 1 paramètre, T9, 1 état | s_G et τ_H constants, couverture intégrale | triviale (niveaux) plus montant de T9 | **lisible**, sous les conditions 1 et 2 |
| C-WB / C-Y / C-Yhi | 0 ou 1 état | idem | idem | à revoir / à clarifier / lisible |
| D | + φ_b | idem plus rappel | oui, mais l'arrivée dépend de φ_b | **à revoir** |
| E | aucun | absence de règle | solde stabilisant | **lisible comme écart déclaré** ; à revoir comme valeur par défaut |
| F | + k_F, état τ | τ déplacé par la règle | divergence hors fenêtre | **à écarter** |

### Indicateurs (critère 17 (a))

| Indicateur | Niveau | Verdict | Motif ou point à clarifier |
|---|---|---|---|
| Dette brute, fin du mois, en % du PIB des 12 derniers mois | tableau du tour | **lisible** | 28,2 % à 2 % ; infobulle : dette nette et part de la banque centrale ; infobulle « le PIB nominal croît plus vite que la dette » quand le ratio baisse alors que l'encours monte (réponse 5) |
| Soldes primaire et public sur 12 tours | tableau du tour | **lisible** | — |
| Solde primaire stabilisant et écart au solde réalisé | tableau du tour | **lisible** | Précurseur de l'écart « aucune couverture » |
| Charge d'intérêts nette, i_B et i^ref | tableau du tour | **à clarifier** | i^ref affiché à côté de i_B (réponse 1) |
| Couverture des intérêts (T9) en % du PIB | tableau du tour | **à ajouter** | Ligne distincte de l'impôt ; règle « dette/PIB × écart de taux » |
| Barème τ_H et taux apparent | tableau du tour | **à clarifier** | Deux lignes (réponse 1) |
| Dépense demandée, exécutée et causes de l'écart | tableau du tour | **à clarifier** | Plafond de trésorerie, prix, non servi (réponse 4) |
| Plafond de trésorerie du tour | saisie du levier | **à ajouter si m = 1** | Annonce le rationnement avant la décision (réponse 3) |
| i_B − croissance nominale | fiche détaillée | **à clarifier** | Point contesté (critère 22) : jamais présenté comme une règle de soutenabilité |
| Encaisse en tours de paiements | fiche détaillée | **hors du tableau** | Vaut m par construction : indicateur mort |
| Émission par souscripteur ; part de la banque centrale | fiche détaillée | **lisible** | B_CB = 0 au socle, mention « constant au socle » |
| Parts non payées | événement | **lisible** | Avec « Adjudication non couverte » (fiche 7, condition 7) |

### Préférence motivée

- **Ma préférence va à C-HS**, comme celle de `macro`.
  - **Mes motifs propres** :
    - une règle en une phrase ;
    - une hausse de taux qui ne distribue plus de revenu aux épargnants aux frais du déficit (ΔYD = 0 au tour 1) ;
    - trois approches budgétaires viables, aux coûts visibles ;
    - aucune remise à zéro gratuite dans la fenêtre de partie ;
    - le piège de la fiche 8 (réponse 5) fermé par défaut.
  - **Les motifs de `macro`**, que je ne juge pas : critères 1 à 16, 18 et 20 à 23.
- **Deux réserves** qui conditionnent ma préférence et que `macro` n'a pas posées :
  - la couverture des intérêts doit être un levier distinct du barème ;
  - m = 1 crée un cliquet à basse inflation.
- **Classement** : C-HS > C-Y > C-Yhi > D > C-WB > B > A. F est écartée. E est hors classement, comme écart déclaré. L et V sont hors classement (V au J6).
- **Lectures du § 5.** (a) HS : accord. (b) τ_F comme levier de valeur 0 : sans enjeu ludique au socle. P2 (i) : sans enjeu ludique.
- **Coût en fidélité.**
  - Le levier distinct de couverture et m > 1 sont des **choix de conception**. `macro` dira ce qu'ils coûtent : pour m, la borne de la l. 502 ; pour la couverture, la lecture du critère 19.
  - Libellés, infobulles et décomposition de l'exécution sont des choix de restitution.

### Conditions demandées au § 9

1. **Couverture des intérêts, levier distinct du barème**, à deux valeurs : « couverture intégrale », qui est la règle et la valeur par défaut, et « aucune couverture : intérêts financés par le déficit », écart déclaré avec mention et précurseurs. Changer le barème ne touche pas la couverture. Lecture du critère 19 soumise au mainteneur.
2. **Encaisse du Trésor sans cliquet** : m > 1, ou une règle qui tient la propriété de la réponse 3. À défaut, le plafond de trésorerie s'affiche dans la saisie du levier.
3. **Libellés** : « impôt sur le revenu des ménages », avec l'infobulle de l'assiette et du retard ; « couverture des intérêts », avec son infobulle et i^ref.
4. **Barème et taux apparent** sur deux lignes ; T9 en ligne propre, en % du PIB.
5. **Dépense demandée, exécutée et causes de l'écart** (trésorerie, prix, non servi), avec les volumes de C et de I.
6. **Infobulle de la dette** quand le ratio baisse alors que l'encours monte ; un archétype à π̄ = 10 % dans le scénario O2 du J4.
7. **Aide** : une dépense permanente non financée entretient l'inflation et le taux (réponse 6) ; une relance est suivie d'un contrecoup au tour 18 ; un taux tenu bas réduit la consommation (fiche 8, condition 8).
8. **Tableau levier → indicateur → délai → contrepartie** (critère 17 (c)) :

   | Levier | Indicateur | Délai | Contrepartie |
   |---|---|---|---|
   | Barème τ_H | impôt, solde, production, glissement | impôt au tour n, sur l'assiette du tour n − 1 ; production à son pic au tour 8 | revenu disponible des ménages au tour n, consommation au tour n + 1 |
   | Dépense publique | dépense exécutée, production, dette | tour n ; production au tour 3 ; glissement en deux crans avant le tour 12 | émission et dépôts des entreprises au tour n ; plafond de trésorerie si m = 1 |
   | Transferts | revenu disponible des ménages, production | tour n ; production au tour 7 | solde et émission au tour n |
   | Couverture des intérêts | T9, solde stabilisant | tour n | revenu disponible des ménages au tour n ; signe d'une hausse de taux |
   | Taux directeur, vu du budget | charge d'intérêts, T9 | tour n | revenu des épargnants repris par T9 au tour n |

9. **Fenêtre longue** : pour le simulateur de 60 ans, `macro` dit si la consommation à −2,92 % au tour 600 après G −5 % permanente est un comportement à déclarer.

### Seuils (critère 17 (d) et (h))

- (d1) tenu : solde +0,791 point au tour 12 ; production −0,838 % au tour 8.
- (d2) tenu : +0,290 % (G +1 %) ; +1,445 % (G +5 %).
- (d3) tenu en pays joué (E) : +0,603 au tour 12, +1,073 au tour 60. Publié sous la règle : +0,473 au tour 12, +0,599 au tour 60, demi-retour au tour 193. Non tenu à 10 % dans les deux configurations (−0,153 et +0,084). C'est une mesure publiée, non un déplacement de seuil.
- (h) (i) tenu par les trois leviers.
- (h) (ii) tenu : pic de production au tour 6 ou 8, pic du glissement au tour 12.
- (h) (iii) déclaré : demi-vie dominante de 275 tours. Écarts signalés au tour 60 :
  - production −0,116 % (G +5 % pendant 12 tours) ;
  - glissement +0,214 (G +1 % permanente), attribuable (réponse 6).
- Aucun seuil nouveau. La propriété de la réponse 3 est proposée pour l'essai du J3, à écrire avant lui.

**Issue proposée par `jeu`** (création soumise au mainteneur ; corps dans le compte rendu de la session, PR #77) : « J4 — restitution du bloc État et dette : couverture des intérêts distincte du barème, assiette libellée, dépense demandée et causes de l'écart, solde stabilisant ». Commentaire proposé sur #73 : cliquet de l'encaisse sous m = 1 à basse inflation.

## 8. Décision du mainteneur

- **Numéro** : M33 (reporté dans `docs/feuille-de-route.md`, § 4), prise par paire avec M32 (fiche 8, P14), citant M22, M25, M28, M29 et M31 pour les contrats qu'elle touche.
- **Date** : 04/10/2026.
- **Option retenue** : **C-HS** :
  - reprise réelle intégrale du surcroît d'intérêts (T9 réel : taux de référence indexé sur π\* par Fisher, C45) ;
  - impôt des ménages assis sur le revenu de Haig-Simons du tour précédent ;
  - dépense en volume indexée sur la production potentielle ;
  - règle de référence et **valeur par défaut** des leviers budgétaires (« suivre la règle » est une valeur de chaque levier).
- **Couverture des intérêts** : levier **distinct du barème τ_H**, à deux valeurs — « couverture intégrale » (φ = 1, règle et défaut) et « intérêts financés par le déficit » (φ = 0, écart déclaré, avec la mention et deux précurseurs) ; changer le barème ne touche pas la couverture ; φ n'est jamais un curseur continu. Lecture du critère 19 retenue par le mainteneur (avis de `jeu`, accepté par `macro` et `monnaie`).
- **Socle commun avec M32** :
  - **lignes 19a : A8** — le bloc 9 propose les trois lignes 19a ; la part s_CB est écrite par le bloc 8 en phase 1 (paramètre d'archétype, 0 au socle, domaine [0 ; 1]) ; la banque ne siège plus en phase 7. **Modification** de contrat (`temps_comptabilite.md:838`, ADR 0009) : décision citant M22 et M29, **ADR d'architecture** (consultation Fable, routage § 4.1) ; la lecture (f) de M31 est ainsi tranchée ;
  - **i_B ≡ i_CB du tour** (option (i)) : identité de notation du socle, déclarée une seule fois dans `sec:finances_publiques`, sans label `eq:` ; prime nulle déclarée (J6) ;
  - **E^CB_0 = 0** ; ligne nommée « perte de la banque centrale non couverte » (C60) ;
  - **contrôle de caisse en lecture nette**, écrit dans `sec:cadre-caisse` aux deux conditions d'`architect` (banque exclue ; contrainte tenue par le plan du payeur, vérification du noyau en fin de phase) ;
  - **encaisse visée M^G\* = m × paiements bruts avec m > 1** : m est un paramètre déclaré du bloc 9, fixé **avant l'essai** du J3, avec une marge déclarée, pour tenir la propriété de `jeu` (aucun rationnement de caisse pour une hausse de dépense de 10 % d'un tour au suivant, ni au retour d'une baisse de 5 % pendant 12 tours, à π̄ ∈ {0 ; 2 ; 10 %} ; borne algébrique m ≥ 1,0965 à π̄ = 0). **Modification** de la l. 502 et de la l. 2064 et du point 13 de l'ADR 0005 : décision citant M22 ;
  - P2 : lecture (i), M^G\* encaisse visée.
- **Critère 13 de la fiche 8** : voie (c), voir M32.
- **Critère « −2 points » de la fiche 6** (essai du J3, #55) : la baisse porte sur le taux directeur, écarts du bloc banque constants (borne ζ < 17,85) ; précision prospective, écrite avant l'essai.
- **Motifs** : le mainteneur a retenu la recommandation de `macro`, à laquelle `monnaie` (§ 6) et `jeu` (§ 7, sous deux conditions, toutes deux retenues) se rangent. Motifs dans ses propres mots : à compléter par le mainteneur s'il le souhaite.
- **Conditions et réserves** : réserves du § 5 ; C51 à C56 ; C57 et C58 intégrées ; C59 à C63 (`monnaie`, C62 amendée) ; conditions 1 à 9 de `jeu`.
- **Ce qui est écarté et pourquoi** : A (instable dans la boucle conjointe), B (dette ancre du taux réel), C-WB (traîne de 36,7 point-années), C-Y (impôt sur les intérêts nominaux), D (arrivée réglée par un gain), E comme valeur par défaut (divergence), F (instabilité 4 réintroduite par le budget), V (J6).

## 9. Conséquences de la décision

À instruire (jalon 2).

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 04/10/2026 | Ouverture (issue #73) ; § 1 et § 2 proposés (jalon 1), en attente de validation des critères par le mainteneur | `macro` ; session principale |
| 04/10/2026 | Relecture croisée intégrée (avis de `macro`, `monnaie` et `jeu`, une relance ciblée ; qualifications d'`architect`) ; options ouvertes marquées « à trancher par le mainteneur » | `macro` ; `monnaie` ; `jeu` ; `architect` ; session principale |
| 04/10/2026 | Critères validés par le mainteneur (jalon 1 de #73 terminé), amendements adoptés consignés au § 2 | mainteneur ; session principale |
| 04/10/2026 | Jalon 2, première partie : § 3 à § 5 instruits (huit options sur la maquette conjointe unique des fiches 8 et 9 ; recommandation de l'option C-HS) ; § 6 et § 7 à rendre | `macro` ; session principale |
| 04/10/2026 | Avis de `jeu` (§ 7) : C-HS lisible sous neuf conditions, dont deux soumises au mainteneur (couverture des intérêts en levier distinct du barème ; encaisse sans cliquet, m > 1 ou propriété équivalente) ; F écartée | `jeu` ; session principale |
| 04/10/2026 | Avis de `monnaie`, expert consulté (§ 6) : favorable à C-HS ; critère 13 de la fiche 8 : résidu des trois conventions 0,019 point (contre 0,112, C57), voie (c) recommandée (échec déclaré, défaut connu, échec attendu au J3) ; conditions C57 à C63 ; fiche « avis rendus », sous réserve de C57 et C58 | `monnaie` ; session principale |
| 04/10/2026 | Complément de `monnaie` au § 6.4 : aucune objection monétaire à m > 1 (modification de la l. 502, décision citant M22) ; accord avec `jeu` sur la couverture des intérêts en levier distinct à deux valeurs ; C62 amendée | `monnaie` ; session principale |
| 04/10/2026 | C57 et C58 intégrées (remesurées par `macro`) : résidu du critère 13 à 0,019 point, profil de r̄, contributions par source ; diagnostic E^CB corrigé. Avis de `macro` : favorable à la voie (c), au levier de couverture à deux valeurs et à m > 1 | `macro` ; `monnaie` ; session principale |
| 04/10/2026 | Décision du mainteneur : M33, prise par paire (M32-M33) ; voir § 8 | mainteneur ; session principale |
| 04/10/2026 | Issues créées sur accord du mainteneur : #80 (critère 13), #81 (restitution J4 banque centrale), #82 (restitution J4 État et dette) ; commentaires publiés sur #54, #73 et #55 | session principale |
