---
bloc: Banque commerciale
module: src/nations/blocs/banque.py
expert pilote: monnaie
experts consultés: macro (demande de crédit des entreprises : frontière crédit ; placement de la dette publique, avec la fiche 9) ; jeu
statut: en instruction
décision: —
issue: #71
---

# Fiche comparative — Banque commerciale

> Fiche ouverte à partir du gabarit `0000-gabarit.md` (validé à l'usage, M20), sur le modèle de forme de la fiche 6 « investissement et financement des entreprises » (critères validés le 03/10/2026). Jalon 1 de l'issue #71 : § 1 et § 2 seuls ; les rubriques suivantes portent « à instruire (jalon 2) ». Décidée seule (M31, numéro sous réserve de l'ordre réel des décisions), avant la paire des fiches 8 et 9 (P14, 04/10/2026) ; ses critères sont validés par le mainteneur avec ceux des fiches 8 et 9, avant tout commit d'instruction.

Une fiche comparative instruit **l'origine de l'approche** d'un bloc (`docs/exigences.md` § 2.3) : la spécification v1.5, le moteur v2.0, ou une approche nouvelle. Elle est **instruite par l'expert pilote**, commentée par `jeu` et par l'expert consulté que désigne `README.md`, et **décidée par le mainteneur** (décision M-n, reportée dans `docs/feuille-de-route.md`). Aucune approche n'entre dans le moteur ni dans la spécification sans cette décision. Les agents n'écrivent pas la fiche dans le dépôt : elle figure dans leur compte rendu et la session principale la commite. Un **bloc-cadre** (temps et comptabilité) n'est pas un module de `blocs/` : sa fiche instruit ce que le cadre **définit** (conventions, matrices, règles), non des flux proposés ; les adaptations que cela impose sont signalées rubrique par rubrique.

Règles de rigueur (`CLAUDE.md`, « Rigueur ») : un chiffre se remesure ou cite sa source ; une équation de la v1.5 n'a jamais été garantie exécutée ; un comportement de la v2.0 ne vaut que sous son profil (état D1, **non versé** : aucun fait ne peut y être remesuré) et avec ses défauts connus ; chaque fait de la première tentative porte son **statut** S+O, O, R, L, V ou V+O (`CONTEXT.md`, « Statut d'un fait » ; un fait V sur le prototype v2.0 reste un fait de la première tentative, non un résultat v3) ; chaque référence est une publication retrouvée. Citer `archive/v1.5/…` avec numéro d'équation et section, ou avec le **numéro de ligne du `.tex`** quand section ou équation ne sont pas identifiables sans compiler ; `archive/v2.0/…` avec fichier et ligne. **Principe de simplicité** (adopté par le mainteneur le 30/09/2026, fiche « temps et comptabilité » § 2 ; `CONTEXT.md`) : à exigences comptables égales, l'option la plus simple pour le joueur et pour le moteur est préférée ; toute complexité se justifie par une identité qu'elle rend vérifiable ou par un mécanisme perçu à l'échelle d'une partie ; une simplification ne supprime ni une contrepartie comptable visible d'un levier ni une grandeur restituée au tour ; les identités, les tolérances relatives, le déterminisme, les invariants de l'ADR 0002 et la concordance ne se simplifient pas.

## 1. Question posée

*Rédigé par `monnaie` (expert pilote), 04/10/2026, sur la spécification à l'état `10391a1` (branche `claude/j1-monnaie-etat`, PR #77). Les numéros de ligne de `docs/specification/nations_et_marches.tex` sont ceux de cet état.*

Le bloc tient la banque commerciale représentative du pays (une seule banque au socle). Il fixe :
- les taux affichés du crédit et des dépôts, i_L et i_D, à partir du taux directeur ;
- les intérêts sur crédits et sur dépôts (lignes 9 et 10, phase 6) et les dividendes de la banque (ligne 15, phase 6) ;
- sa souscription de titres publics (ligne 19a-banque, phase 7), reliquat de l'émission ;
- son refinancement auprès de la banque centrale (ligne 21, phase 8 (c)) ;
- les conditions d'offre de crédit publiées à l'ouverture (la ligne 18 est proposée par le bloc 6, lecture (a) de la Q7, M28).

Ses fonds propres E^Bk sont sa valeur nette, calculée deux fois par le noyau. Ses réserves Res et son refinancement L^CB sont des postes du noyau, mus par des lignes nommées. Le bloc est la seconde moitié de la frontière crédit. Il débloque la fiche 8 (refinancement, corridor) et la fiche 9 (placement de la dette, C25) (`docs/blocs/README.md` § 3, rang 7). Sous M22, un pas est un tour (n_a = 12, n_m = 1).

### 1.1 Contrats hérités

| Contrat | Source | Ce qu'il impose à la fiche 7 | Ce qui le rouvrirait |
|---|---|---|---|
| Calendrier, conversions, intérêts | M22 ; ADR 0005, pts 4, 5 et 11 ; ADR 0008, I.1 et I.2 ; `sec:cadre-calendrier` (l. 190-196, 214) ; `sec:cadre-caisse` (l. 483) | i_L, i_D, i_res et i_CB sont des taux de flux, convertis linéairement (x/n_a). Tout intérêt est assis sur l'encours brut d'ouverture et versé à chaque pas. Le délai du premier flux d'intérêt est nul pour les lignes 12 et 13. Le taux réel restitué et testé est r = i − π (l. 214) | Décision M-m citant M22 |
| Instruments et bilans | `tab:instruments` (l. 275-280) ; `tab:matrice-bilans` (l. 298-307) ; E^Bk développée l. 255 | La banque émet D_H, D_F et L^CB et détient L, B_Bk et Res. E^Bk = L + B_Bk + Res − D_H − D_F − L^CB est sa seule grandeur résiduelle, calculée deux fois. Sans billets, M = D_H + D_F et H = Res (l. 246). Au socle : ni actions bancaires, ni crédit aux ménages, ni réserves obligatoires (l. 244-250) | Décision citant M22 (instrument ou ligne nouvelle) |
| Lignes de la banque | `tab:matrice-flux` (l. 349-367) ; `tab:portes-monnaie` (l. 418-436) | Colonne de la banque : lignes 9, 10, 11b, 12, 13, 15, 17, 18, 19a-banque, 19b-banque, 20 et 21. Portes de M : 9 (−), 10 (+), 15 (+), 18 (+). Portes de H : 11b, 12, 13, 19a-banque, 19b-banque, 21. Les lignes 17 et 20 sont des contreparties de règlement, jamais décidées (l. 319) | Décision citant M22 |
| Aucun solde résiduel | `sec:cadre-identites` (l. 444-450) ; ADR 0005, pt 8 | Chaque poste de clôture vaut l'ouverture plus les lignes nommées. ΔL^CB n'a qu'une source, la ligne 21, flux décidé en 8 (c). « Aucune règle ne corrige un solde de réserves négatif en l'ajoutant au refinancement » (l. 450). C'est l'inverse de la v2.0, où `Res` est obtenu par différence du bilan bancaire puis reporté sur `L_cb` (`archive/v2.0/prototype/model.py` l. 1280-1283, copies l. 557 et 1574, L) | Décision citant M22 |
| Découvert intra-pas et refinancement | `sec:cadre-caisse` (l. 485-489) ; ADR 0005, pt 10 | Res peut être négatif entre les phases. Res_{t+1} ≥ 0 est une identité de clôture (phase 9). Le refinancement de la phase 8 (c), au taux i_CB, couvre au moins la position négative ; « la règle qui le fixe relève du bloc banque » (l. 489) | Décision citant M22 |
| Règle de caisse | `sec:cadre-caisse` (l. 481) | La banque paie en réserves l'État et la banque centrale. Un payeur ne paie pas plus que son moyen de paiement, et la part non payée est une ligne nommée du bloc payeur. Le bloc déclare son ordre de priorité des paiements. Le crédit précède les règlements | Décision citant M22 si une ligne s'ajoute |
| Phases | `tab:phases` (l. 529-537) ; `sec:cadre-phases` (l. 510, 512) ; ADR 0007 ; ADR 0009 (M29) | La banque écrit en phase 3 (« investissement, banque »), 6 (« État, banque, investissement »), 7 (« État, banque, banque centrale », ordre « à fixer par leurs fiches ») et 8 (c). Elle ne siège pas en phase 1. Les phases 3 et 6 n'ont pas d'ordre interne. Le groupe de la phase 9 est « ménages, investissement ». Une variable d'état de bloc est écrite une fois par pas, dans une phase où le bloc siège après ses entrées, sinon en phase 9 (l. 512). Ajouter la banque au groupe de la phase 9, déclarer un ordre en phase 3 ou 6, ou faire siéger la banque en phase 1 modifie `tab:phases` | Décision citant M22 (et M29), et ADR |
| Résultat de la banque centrale | `sec:cadre-caisse` (l. 491-495) ; ADR 0005, pt 12 | Π^CB est calculé en phase 1, sur des encours d'ouverture et des taux arrêtés en phase 1, et versé en 8 (b). Les lignes 12 et 13 s'exécutent en 8 (a), avant le refinancement | Décision citant M22 |
| Émission (α) et placement | `sec:cadre-caisse` (l. 497-502) ; ADR 0005, pt 13 | L'État émet en phase 7 le besoin réalisé du pas. Un placement raté laisse M^G sous M^{G*}, et la dépense est rationnée au tour suivant | Décision citant M22 |
| Fiche 6 (M28) | `investissement.md` § 6.3 (C27 à C31), § 8, § 9.4 (l. 1975 et 1991) ; `sec:investissement-conditions` (l. 1905) | Lecture (a) de la Q7 : la banque publie ses conditions à l'ouverture et le bloc 6 propose seul la ligne 18. i_L et i_D sont lus à l'ouverture. Pas de plafond au socle ; le refus partiel est un scénario déclaré. Le propriétaire de la ligne 9 est à fixer avec la fiche 7 (recommandation de `macro` : le bloc 7) | M28 |
| Fiche 5 (M27) | `menages.md` § 6.3 (C19 à C22), critère 1 (a), § 9.4 (l. 1727) | B_H ≡ 0 : la banque est la seule détentrice privée de la dette. Les lignes 10 et 15 sont proposées par le bloc 7. YD_t est lu au grand livre en phase 9 (M29), Div_Bk compris. Seul le canal rentier du taux existe | M27 |
| Bornes | #38, lecture (ii) ; `CONVENTIONS.md` § 2.4 | Une borne à seuil libre a un paramètre déclaré et un motif contre un mécanisme. Une contrainte de conservation est déclarée dans les `\limites`, avec son activité à l'état stationnaire et un test. « Le plancher à zéro d'un taux nominal est à seuil libre » | Décision citant #38 |
| Statut des faits | P1 (03/10/2026) ; `CONTEXT.md` | Statuts S+O, O, R, L, V et V+O. L'état D1 n'est pas versé | — |

### 1.2 Ce que le bloc doit produire

Les symboles **ne sont pas fixés** : ils le seront à l'instruction, sous le critère 16. Plusieurs sont déjà pris :
- m (propension de la demande induite, `sec:investissement-conditions` l. 1877) ;
- κ_j (capital par production normale, fiche 2) ;
- ϱ_L (taux réel du crédit anticipé, fiche 6) ;
- ℓ (indice de ligne) et k (intrant).

| Grandeur | Définition | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| i_L, i_D | Taux affichés du crédit et des dépôts. Variables d'état du bloc, écrites une fois par pas à partir de i_CB du tour, lues à l'ouverture du tour suivant (C27) | par an, taux de flux | — | ouverture ; le tour |
| Écarts de taux | i_L − i_CB et i_CB − i_D | points par an | — | le tour ; valeur stationnaire |
| Ligne 9 | i_L·L/n_a, si le bloc en est propriétaire | u.m. par pas | — | le pas, phase 6 |
| Ligne 10 | i_D·(D_H + D_F)/n_a | u.m. par pas | — | le pas, phase 6 |
| Résultat Π^Bk | Lignes 9 + 11b + 12 − 10 − 13 du pas, assises sur les encours d'ouverture | u.m. par pas ; fraction par an | E^Bk d'ouverture (rentabilité des fonds propres) | le pas ; 12 tours |
| Dividendes Div_Bk (ligne 15) | Distribution aux ménages ; règle et date à déclarer (C21) | u.m. par pas ; fraction | Π^Bk | phase 6 ; 12 tours |
| Fonds propres E^Bk | Valeur nette, par le stock et par les flux (Π^Bk − Div_Bk) | u.m. ; fraction | L d'ouverture, ou actif total (à déclarer) | ouverture ; clôture |
| Conditions d'offre | Taux, part refusée d'un scénario (C31), toute règle d'octroi, publiés à l'ouverture | — ; fraction | demande du pas | ouverture |
| Crédit nouveau (ligne 18 exécutée) | Égal à la demande sous C27 ; la demande non satisfaite est publiée avec le bloc 6 | u.m. par pas ; fraction | demande du pas | phase 3 |
| Souscription (ligne 19a-banque) | Reliquat déclaré de l'émission (C19) | u.m. par pas | besoin d'émission du pas | phase 7 |
| Ventes à la banque centrale (ligne 19b-banque) | Contrepartie des achats décidés par la banque centrale (C17) | u.m. par pas | — | phase 7 |
| Refinancement (ligne 21) | ΔL^CB décidé sur la position de réserves après tous les règlements | u.m. par pas | — | phase 8 (c) |
| Res, L^CB, B_Bk | Postes du noyau ; Res_{t+1} ≥ 0 à la clôture | u.m. ; années de PIB | test zéro : 12 × PIB nominal du pas ; restitution : PIB des 12 derniers tours | ouverture ; clôture |
| Masse monétaire M = D_H + D_F | Passif de la banque | années de PIB | idem | ouverture ; clôture |
| Rendement réel des dépôts | i_D − π, forme du cadre (l. 214) ; « impôt d'inflation net » des déposants (C20) | points par an ; u.m. par pas | — | le tour ; valeur stationnaire |
| Variables d'état du bloc | i_L, i_D et toute variable de règle (écart lissé, cible de fonds propres) | unité propre | — | ouverture |

### 1.3 Ce qu'il lit

- **Ouverture** :
  - ses variables d'état (i_L, i_D) ;
  - les postes L, D_H, D_F, B_Bk, Res et L^CB, et E^Bk calculé par le noyau ;
  - i_B du tour : lu à l'ouverture ou en phase 1 selon la règle de i_B (fiche 8, critère 4 (f) ; fiche 9, critère 13 (c)). Options : (i) i_B ≡ i_CB du tour ; (ii) écart constant ; (iii) i_CB d'ouverture ; (β) bloc 9 en phase 1 ; recommandation commune de `macro` et `monnaie` : (i) ; choix à M33, à trancher par le mainteneur ;
  - le registre de l'indice des prix, seulement si une règle lit une inflation.
- **Phase 1** : i_CB et i_res du tour (bloc 8). Aucun levier propre au socle sans décision (Q7).
- **Phase 3** : rien sous la lecture (a) de M28. La banque ne lit pas la demande du pas.
- **Phase 6** : rien de ce qu'un autre bloc écrit dans la phase (pas d'ordre interne). Les lignes 9, 10 et 15 reposent sur l'ouverture et la phase 1.
- **Phase 7** : le besoin d'émission (bloc 9), puis la souscription et les achats décidés de la banque centrale (bloc 8), dans l'ordre de C25 à déclarer dans `tab:phases`.
- **Phase 8 (c)** : la position de réserves après 8 (a) et 8 (b), lue en montants exécutés au grand livre (ADR 0009).
- **Décisions qui le contraignent** : M22 (ADR 0005) ; M24 (ADR 0007) ; M27 ; M28 ; M29 (ADR 0009) ; M30 (ADR 0010, sans effet direct sur le bloc) ; décisions du 02/10/2026 sur #23 (indices) et du 03/10/2026 sur #38 (bornes).

### 1.4 Frontières

- **Investissement et financement (fiche 6, `macro`) : frontière crédit.**
  - Chez `macro` : la demande de crédit (F1), le financement, et l'usage d'un refus (F3, qui le reporte sur Div_F).
  - Chez `monnaie` : l'offre, i_L, les fonds propres et le rationnement.
  - Lignes 18 et 9. Critères 3 (b) et 7 ; avis de `macro` au § 6.
- **Ménages (fiche 5, `macro`)** : i_D (C20) ; Div_Bk et sa date (C21) ; les dépôts, passif de la banque. Critères 4 et 5.
- **Banque centrale et anticipations (fiche 8, `monnaie`)** :
  - i_CB et i_res ;
  - le corridor (#26, pt 5) ;
  - les lignes 12, 13 et 16, exécutées par le bloc 8 en 8 (a) et 8 (b) ;
  - les achats 19a-BC et 19b-banque (C17) ;
  - l'allocation du refinancement ;
  - les canaux et délais du taux (C34, C35).

  Critères 2, 4 (d) et 6 (d).
- **État et dette (fiche 9, `macro` ; `monnaie` consulté) : frontière dette publique.** Ce qui revient à chaque fiche :
  - **C19 et C22** : fiche 7 (règle de souscription de la banque, limite de détention) ;
  - **C25** (ordre de la phase 7) : critère de la fiche 9. La fiche 7 en vérifie la compatibilité (critère 6 (e)) et le déclare avec les fiches 8 et 9 dans `tab:phases` ;
  - équation d'émission, besoin, M^{G*}, i_B et sa date de fixation, prime souveraine : fiche 9 ;
  - **C36** : critère de la fiche 8, jugé avec la règle de la fiche 9 (C37). La fiche 7 fournit la transmission (critère 4) et la date de Div_Bk (critère 5), deux des canaux de C34 ;
  - **#44** : fiches 8 et 9. La fiche 7 n'y entre que par l'écart i_L − i_CB, qui relie le taux réel de fermeture au taux réel du crédit ϱ̄_L du bloc 6 ;
  - impôt sur la banque (la colonne de la banque n'a pas de ligne 7 au socle) et recapitalisation de la banque (J6) : fiche 9 et J6.
- **`jeu`** : critère 13 ; avis au § 7.

### 1.5 Ce que la fiche ne tranche pas, et questions ouvertes

**Hors du périmètre** :
- la règle de taux, i_res et le corridor côté banque centrale (fiche 8) ;
- i_B, l'émission et la prime souveraine (fiche 9) ;
- les pertes sur crédits, faillites, insolvabilité et recapitalisation de la banque, ruées, accélérateur financier (J6 ; #57) ;
- plusieurs banques, le marché interbancaire, les billets, le crédit aux ménages, les actions bancaires (absents ; les ajouter est une décision citant M22) ;
- les valeurs de calibration (J3) ;
- les bandes du test zéro : proposées ici, confirmées avec O1 avant l'essai (M19).

**Questions ouvertes à instruire** :
- **Q1 — Transmission** (C20, C27, C28, C29). Forme de i_L et i_D en fonction de i_CB : écart constant, écart fonction de l'état propre de la banque (E^Bk/L), ajustement partiel. Plancher éventuel. Phase d'écriture : 8 (c), ou phase 9, ce qui retouche `tab:phases`.
- **Q2 — Refinancement et réserves** (#26, pts 4 et 5). Règle de la ligne 21 :
  - couverture exacte de la position négative ;
  - usage d'une position positive (remboursement de L^CB, encaisse visée) ;
  - allocation sans plafond ;
  - découvert intra-pas sans intérêt ;
  - arbitrage du corridor.
- **Q3 — Fonds propres et distribution** (C21). Règle et date de Div_Bk ; ancre de E^Bk sous croissance nominale ; Div_Bk ≥ 0.
- **Q4 — Placement** (C19, C22, C25). Reliquat, limite de détention, ordre de la phase 7.
- **Q5 — Offre** (C27, C28, C31, #57). Offre au taux affiché ; dispositif de refus du scénario de C31 ; place d'un accélérateur financier ; ligne nommée de part non payée.
- **Q6 — Propriétaires des lignes 9, 10 et 15** (recommandation de la fiche 6 : lignes 9 et 10 au bloc 7).
- **Q7 — Leviers** : aucun levier propre au socle, ou un levier prudentiel (ratio de fonds propres, réserves obligatoires : v1.5 l. 985 et l. 1815). Par défaut, renvoi au **J6** (et non au J4) : un levier prudentiel n'est ouvert qu'avec le risque qu'il gouverne (pertes sur crédits, #57). Les réserves obligatoires sont écartées tant que l'offre de crédit ne dépend pas des réserves (C27).
- **Q8 — Variantes à instruire** :
  - **A (v1.5)** :
    - taux bancaires, l. 1103 : i^L_j = i^CB + m^L + ϱ_1(ℓ_j − ℓ̄)^+ + ϱ_2 ρ̂^NPL et i^D = (i^CB − m^D)^+ ;
    - plafond de fonds propres, l. 1114 ;
    - compte de résultat, dividende et émission d'actions, `eq:bankeq`, l. 1124-1131 ;
    - banque insolvable et recapitalisation, l. 1140 et 1143.
  - **B (v2.0)**, `model.py` :
    - i_D = max(i_cb − mD, 0) si E_bank > 0, l. 735 et 802 ;
    - i_L, l. 1972-1974 ;
    - paramètres, l. 221 (mL = mD = 0,01 ; kappa_CAR = 0,09) ;
    - réserves résiduelles, l. 1280-1283 ;
    - recapitalisation, émission d'actions et dividendes, l. 1139-1167 ;
    - capacité de prêt, l. 1832 et 1981.

    La branche active et les coefficients de D1 se vérifient avant toute citation. Parmi les drapeaux bancaires, la synthèse des faits (§ 1.1) n'établit que `adv_interest=True` et `residual_tolerance='stock_aware'`. Les valeurs par défaut de `Params` (l. 246, 286) ne sont pas celles de D1.
  - **C (nouvelle) : corridor explicite** (feuille de route § 5), réserves et refinancement comme flux décidés. Référence candidate : Whitesell (2006), « Interest rate corridors and reserves », *Journal of Monetary Economics* 53(6), 1177-1195 (existence vérifiée par moteur de recherche, texte non lu).
  - **Au moins une autre approche** : la banque des modèles de Godley et Lavoie (2007), chap. 7, « A Simple Model with Private Bank Money », et chap. 10, « A Model with both Inside and Outside Money ». Titres vérifiés sur la table des matières d'EconPapers ; contenu non lu, à lire à l'instruction.
  - **Une variante sans retard** (transmission dans le tour), comme référence (`docs/exigences.md` § 2.7).

### 1.6 Conditions et issues reçues : traitement

| Élément reçu | Source | Traitement | Où | Raison |
|---|---|---|---|---|
| C19 — placement sous B_H ≡ 0, reliquat déclaré | fiche 5 § 6.3 | retenu | critères 6 (a), 1 (b), 2 (a) | Condition de M27 ; supprime les postes obtenus par différence (défaut v2.0) |
| C20 — taux des dépôts : transmission déclarée, marge réglée par un mécanisme | fiche 5 § 6.3 | retenu | critère 4 (a), (b), (d) | Les ménages n'ont pas d'actif concurrent : la règle fixe seule le rendement réel des dépôts |
| C21 — délai de Div_Bk | fiche 5 § 6.3 | retenu | critère 5 (b) | Fixe le calendrier de la compensation du canal rentier (YD_t lu au grand livre, M29) |
| C22 — limite de détention de titres | fiche 5 § 6.3 | retenu ; le risque de renouvellement est transmis au J6 | critère 6 (c) | Une limite est une borne ; son activation est le placement raté du cadre (l. 502) |
| C27 — offre au taux affiché ; i_L, i_D variables d'état lues à l'ouverture | fiche 6 § 6.3 | retenu | critères 3 (a), (b), 7 (a) | Lecture (a) de M28 |
| C28 — écart i_L − i_CB sans prime sur le levier de l'emprunteur | fiche 6 § 6.3 | retenu ; l'accélérateur de Bernanke, Gertler et Gilchrist est transmis au J6, avec #57 | critère 4 (c) | Superneutralité ; une prime sur L/K comptable est inerte sous F |
| C29 — marge pendant le tour d'une décision | fiche 6 § 6.3 | retenu | critères 4 (d), 13 (b) | Effet visible sur Π^Bk le tour même |
| C30 — bilans fonction de π̄ | fiche 6 § 6.3 | retenu ; test avec C15 (fiche 8) ; B/PIB à la fiche 9 | critère 8 (c) | Dépendance déclarée, non dérive |
| C31 — robustesse du bloc 6 au refus de crédit | fiche 6 § 6.3 | retenu pour le dispositif ; la mesure est un critère de la fiche 6 (`sec:investissement-conditions` l. 1895) | critère 7 (b) | Le bloc 7 fournit le choc de scénario |
| Propriétaire de la ligne 9 | fiche 6 § 9.4 | retenu, tranché à M31 | critères 1 (a), 3 (c) | Recommandation de `macro` (bloc 7), cohérente avec la ligne 10 |
| #26, point 4 — découvert intra-pas sans intérêt | #26 | retenu | critère 2 (b) | Déclaration sans ligne nouvelle |
| #26, point 5 — corridor | #26 | retenu sous condition : clos ici si la règle de la ligne 21 borne le refinancement, sinon transmis à la fiche 8 (i_res ≤ i_CB) | critère 2 (c) | L'arbitrage dépend à la fois de la règle de la banque et de i_res |
| #57 — accélérateur financier ; ligne de part non payée de D_F | #57 et commentaire de `macro` | retenu pour l'instruction ; forme transmise au J6, limite déclarée | critère 7 (c) | Aucune grandeur de levier ni de valeur nette des entreprises n'est utilisable au socle (C28) |
| Piste « corridor explicite » | feuille de route § 5 | option à instruire | § 1.5, Q8 ; critère 2 (d) | Réserves et refinancement comme flux décidés (ADR 0001) |
| C25 — ordre de la phase 7 | fiche 5 § 6.3 (fiche 9) | transmis (critère de la fiche 9) ; compatibilité vérifiée ici | critère 6 (e) | La fiche 9 écrit l'équation d'émission |
| C34, C35 — canaux et délais du taux | fiche 6 § 6.3 (fiche 8) | transmis à la fiche 8 ; la fiche 7 en fournit la transmission et la date de Div_Bk | critères 4 et 5 | Mesure de la boucle conjointe à la fiche 8 |
| Défauts de la v2.0 : réserves et refinancement résiduels, tolérances non homogènes | ADR 0001 ; `archive/faits_mesures_G_K.md` § 5 | retenus comme exigences négatives | critères 1 (b), 10 (a) | Instabilité 16 (S+O) |

## 2. Critères d'évaluation, écrits avant l'instruction

**Statut** : proposés par `monnaie` le 04/10/2026, **validés par le mainteneur le 04/10/2026**, avec les amendements ci-dessous (jalon 1 de #71), avec ceux des fiches 8 et 9 (P14). La liste est fermée : elle ne se déplace pas après observation (`docs/exigences.md` § 2.5). Un amendement adopté avant l'instruction se consigne sous le tableau. Seuils reconduits des fiches 2 à 6, à confirmer :
- 1e−10 en relatif (critère 8) ;
- 1e−6 après H = max(720 ; 20 demi-vies de la racine dominante mesurée) pas (critère 9, critère commun des vitesses) ;
- 0,48 ms par pays-pas (critère 15) ;
- 12 tours pour la désactivation d'une borne (critère 12 (c)).

Correspondance avec le gabarit :

| Critère du gabarit | Critère de la fiche |
|---|---|
| 1 | 1 (et 2) |
| 2 | 8 et 9 |
| 3 | 10 |
| 4 | 15 |
| 5 | 13 |
| 6 | 12 et 14 |

Critères propres au bloc : 2, 3, 4, 5, 6, 7, 11, 16, 17 et 18.

Sont des **exigences** (ils peuvent écarter une option) :
- 1 à 3 ;
- 4 (a) à (c) ;
- 5, 6 ;
- 7 (a) à (c) ;
- 8 à 12 ;
- 13 (b) ;
- 14 (sans historique ni drapeau) ;
- 15 (sans itération) ;
- 16 et 18.

Sont des **mesures** (elles décrivent sans écarter) :
- 4 (d), 7 (d) ;
- la période et la demi-vie du critère 10 ;
- 13 (a), (c), (d) et (e) ;
- 14 et 15 (décomptes) ;
- 17.

| N° | Critère | Ce qui est attendu (seuil ou forme du verdict) | Par quoi on le vérifie | Qui | Quand |
|---|---|---|---|---|---|
| 1 | Cohérence stock-flux (gabarit 1 ; `monnaie`) — **exigence** | (a) **Lignes proposées** par le bloc, avec leur phase : 10 et 15 en phase 6 ; 9 en phase 6 si le bloc en est propriétaire (critère 3) ; 19a-banque en phase 7 si M31-M33 en fait une ligne du bloc 7 ; sinon ligne reçue, proposée par le bloc 9 comme reliquat sous les conditions publiées par la banque (recommandation de `monnaie`) ; 21 en phase 8 (c). **Propriétaire des lignes 19a, à trancher par le mainteneur (choix à M33)** : (A8) le bloc 9 propose les trois lignes 19a, la part s_CB étant écrite par le bloc 8 en phase 1 et la banque retirée de la phase 7 — recommandée par `monnaie` et `macro` ; **modification** (`temps_comptabilite.md:838`, ADR 0009 l. 84 : décision citant M22 et M29, ADR d'architecture) ; (variante) chaque détenteur propose sa part, le bloc 9 publie le besoin, ordre État → banque centrale → banque fixé par les fiches — **interprétation**, note à la table de la fiche 1. La propriété de 19a-banque dans M31 reste conditionnelle. **Lignes reçues** : 11b (bloc 9) ; 12 et 13 (bloc 8, 8 (a)) ; 18 (proposée par le bloc 6, lecture (a) de M28) ; 19b-banque (bloc 8). Signatures de `tab:portes-monnaie` inchangées. Toute ligne ou tout poste nouveau (part non payée, recapitalisation, actions bancaires, réserves obligatoires, impôt sur la banque) est déclaré avec sa phase et sa signature : c'est un contrat partagé, donc une décision citant M22. (b) **Aucun solde résiduel** : L ne varie que par la ligne 18 ; B_Bk par 19a-banque et 19b-banque ; D_H + D_F par la ligne 17 ; Res par la ligne 20 ; L^CB par la ligne 21. Aucun de ces postes n'est obtenu par différence du bilan (défaut v2.0, `model.py` l. 1280-1283, L). E^Bk est calculé deux fois, par le stock (l. 255) et par les flux (Π^Bk − Div_Bk). (c) **Contrainte budgétaire de la banque**, écrite sur un pas : ΔL + ΔB_Bk + ΔRes = ΔD_H + ΔD_F + ΔL^CB + Π^Bk − Div_Bk, avec Π^Bk = lignes 9 + 11b + 12 − 10 − 13. (d) **Règle de caisse de la banque** : paiements en réserves (19a-banque en phase 7, 13 en 8 (a)) ; recettes en réserves (11b en phase 6, 12 en 8 (a)) ; paiements par création de dépôts (10, 15) ; ordre de priorité. La part non payée a une ligne nommée, ou la fiche démontre qu'aucune part ne peut rester impayée au socle (refinancement sans plafond, critère 2 (a)) | Matrice des flux de l'option, en tableau. Cas à la main sur un pas où i_CB monte d'un point au tour même : lignes 9, 10, 11b, 12, 13, 15, 19a-banque et 21 ; Res et L^CB à la clôture ; E^Bk par le stock et par les flux. Si une table change : `uv run python outils/verifier_matrices.py --strict <copie>`, sortie citée avant et après | `monnaie` ; `macro` ((a), ligne 9) | fiche ; J3 (identités, ε = 1e−12 × S^Bk, M22) |
| 2 | Réserves, refinancement et corridor (#26, pts 4 et 5 ; `sec:cadre-caisse` l. 485-489 ; piste « corridor explicite » ; `monnaie`) — **exigence** | (a) **Règle de la ligne 21**, écrite comme flux décidé en 8 (c) à partir de la position de réserves après tous les règlements (montants exécutés, ADR 0009). Elle couvre au moins la position négative (l. 489) et dit ce que la banque fait d'une position positive (remboursement de L^CB, encaisse visée). L'allocation par la banque centrale est sans plafond ni collatéral au socle, déclarée avec la fiche 8 ; une limite relève du J6, par décision. Res et L^CB ont chacun une ancre : leurs rapports stationnaires à 12 × PIB nominal du pas sont écrits en forme fermée ; aucun intégrateur sans ancre. Ces formes fermées sont écrites en fonction de M^{G*}/PIB (fiche 9, critère 11) : chaque impôt draine des réserves vers M^G ; bilan de la banque centrale, Res − L^CB = B_CB − M^G − E^CB, d'où, sous Res·L^CB = 0 et E^CB = 0, L^CB = max(M^{G*} − B_CB ; 0) et Res = max(B_CB − M^{G*} ; 0) ; sans titres à la banque centrale, H = 0. (b) **#26, point 4** : le découvert intra-pas des réserves ne porte pas d'intérêt. Seule la ligne 13, assise sur L^CB d'ouverture, rémunère le refinancement. C'est déclaré dans la règle de caisse, sans ligne nouvelle. (c) **#26, point 5** : aucun arbitrage « emprunter en 8 (c) pour placer en réserves rémunérées ». Verdict sous l'une de deux formes : (i) la règle de (a) borne le refinancement (par exemple L^CB_{t+1} > 0 ⇒ Res_{t+1} = 0, sans paramètre), et le point 5 est clos par la fiche 7 ; (ii) sinon, la condition i_res ≤ i_CB est transmise à la fiche 8 comme exigence. (d) La piste « corridor explicite » est instruite comme option, avec sa référence lue, et comparée aux options A et B sur (a) à (c) | Règle écrite. Cas à la main sur un pas : position négative de x u.m. après la phase 8 (b), puis position positive ; Res et L^CB à la clôture. Formes fermées | `monnaie` | fiche ; J3 (Res_{t+1} ≥ 0 à chaque pas ; Res·L^CB = 0 à la clôture sous (c) (i)) |
| 3 | Contrats hérités, phases et lectures (§ 1.1 ; ADR 0005, 0007, 0009 ; lecture (a) de la Q7 de M28 ; C27 ; `monnaie`, `macro` pour (b)) — **exigence** | (a) **i_L et i_D** : variables d'état du bloc, avec leur propriétaire (bloc 7), leur phase d'écriture et leur date de lecture (ouverture du tour suivant, C27). Phase d'écriture : 8 (c), où la banque siège après la phase 1 qui fixe i_CB ; la mention de i_L et i_D dans la colonne « Contenu » de la ligne 8 de `tab:phases` est une retouche à qualifier par `architect`. Ou phase 9, ce qui ajoute la banque au groupe de `tab:phases` : décision citant M22 et M29, et ADR. Res et L^CB ont pour propriétaire le noyau et sont mus par les lignes 20 et 21 ; leur date de lecture est déclarée pour chaque lecteur. (b) **Phase 3** (lecture (a) de M28) : la banque publie ses conditions à l'ouverture et ne lit pas la demande du pas ; aucun ordre interne en phase 3. (c) **Phase 6** : les lignes 9, 10 et 15 reposent sur les encours d'ouverture, les taux d'ouverture et ceux de la phase 1. Div_Bk ne lit rien de ce qu'un autre bloc écrit dans la phase. (d) **Phase 7** : la souscription 19a-banque vient après le besoin de l'État et les décisions de la banque centrale (C25). L'ordre interne de la phase 7, « à fixer par leurs fiches » (`tab:phases` l. 535), est déclaré avec les fiches 8 et 9 ; le déclarer retouche `tab:phases` (contrat partagé : décision citant M22, et ADR si l'ordre est nouveau). (e) **Phase 8 (c)** : la règle lit la position de réserves après 8 (a) et 8 (b), au grand livre. (f) La matrice des lectures reste triangulaire | Tableau phase → lit / écrit pour les phases 0, 3, 6, 7, 8 (c) et 9, avec les blocs 6, 8 et 9 ; triangularité vérifiée à la main | `monnaie` ; `macro` ((b)) | fiche ; J2 (test de triangularité de l'ordonnanceur) |
| 4 | Taux des dépôts et du crédit : transmission et marges (C20, C27, C28, C29 ; `monnaie`) — **exigence** pour (a) à (c), **mesure** pour (d) | (a) **Règle de transmission déclarée** : forme de i_L et de i_D en fonction de i_CB (et de i_res si la fiche 8 sépare les deux) ; écarts stationnaires ; délai en tours entiers (taux décidé au tour n, i_L et i_D lus au tour n + 1, C27 et C35). (b) **Marges réglées par un mécanisme, non par une borne** (C20). Un plancher du taux des dépôts (v1.5 l. 1103 ; v2.0 `max(i_cb − mD, 0)`, l. 735 et 802, L) est une borne à seuil libre (`CONVENTIONS.md` § 2.4) : il est déclaré, avec son motif contre un mécanisme et son activité à l'état stationnaire, ou écarté. (c) **C28** : aucune prime sur le levier de l'emprunteur au socle. Contre-exemples : v1.5 ϱ_1(ℓ_j − ℓ̄)^+ et ϱ_2 ρ̂^NPL (l. 1103) ; v2.0 `rho1·max(ell − ell_bar, 0)` (l. 1974, L). Un mécanisme d'écart, s'il existe, lit l'état propre de la banque (E^Bk/L), est déclaré, et est superneutre : écarts i_L − i_CB et i_CB − i_D stationnaires identiques à 1e−10 près pour π̄ = π* ∈ {0 ; 2 % ; 10 %}. (d) **Mesures** : C29, effet d'une hausse d'un point de i_CB sur Π^Bk au tour de la décision (lignes 12 et 13 sur Res et L^CB d'ouverture), au tour suivant (lignes 9 et 10), et sur Div_Bk selon sa date ; C20, rendement réel stationnaire des dépôts i_D − π̄ et « impôt d'inflation net » des déposants, à π̄ = 0, 2 % et 10 % | Formes écrites ; calcul à la main | `monnaie` ; `macro` (avis, frontière crédit) | fiche ; J3 |
| 5 | Fonds propres et distribution (C21 ; `monnaie`) — **exigence** | (a) **E^Bk a une ancre** : un ratio stationnaire de fonds propres (E^Bk/L, ou sur l'actif, dénominateur déclaré), écrit en forme fermée et indépendant des vitesses. Sous croissance nominale, la rétention couvre exactement la croissance de E^Bk : Π^Bk − Div_Bk = (Γ̄ − 1)E^Bk par pas, avec Γ̄ = [(1 + g)(1 + π̄)]^{1/n_a}. Des fonds propres au gré des profits, sans ancre, sont un continuum d'équilibres : refusé. (b) **C21** : date de Div_Bk (même tour que Π^Bk, ou tour suivant) déclarée en tours entiers. Elle fixe le calendrier de la compensation en équilibre général du canal rentier (fiche 5, Q3, point 1). L'écart de calendrier entre les deux dates est chiffré sur une hausse d'un point de i_CB. (c) **Div_Bk ≥ 0** est classée (`CONVENTIONS.md` § 2.4). Un dividende négatif serait un apport des ménages, sans instrument au socle (actions bancaires absentes) : c'est une contrainte de domaine, inactive à l'état stationnaire, avec sa marge chiffrée. (d) **Hors du socle** : l'insolvabilité (E^Bk < 0), la recapitalisation (v1.5 l. 1140 et 1143 ; v2.0 l. 1139-1150) et l'émission d'actions (v1.5 `eq:bankeq`, ΔE^ém, l. 1128) sont renvoyées au J6, avec la limite déclarée | Formes fermées ; cas à la main du critère 1 | `monnaie` | fiche ; J3 |
| 6 | Placement des titres publics (C19, C22, C25 ; frontière dette publique ; `monnaie`, avis de `macro`) — **exigence** | (a) **C19** : sous B_H ≡ 0, la souscription 19a-banque est le reliquat déclaré de l'équation d'émission, besoin − 19a-BC (l. 499-500), jamais un solde du bilan bancaire. (b) B_Bk/(12 × PIB nominal du pas) stationnaire est écrit en forme fermée à partir de B/PIB (fiche 9) et de B_CB. C30 : sa dépendance à π̄ est écrite par l'identité de la dette (fiche 9, critère 5 (b)) : côté entreprises, −Δ(L − D_F) = +0,287 année de PIB entre 2 % et 10 % (chiffre de la fiche 6) ; côté ménages, V_H/(12 YD) passe de 0,980566 à 0,912667 (ν_H = 1 an) ; côté banque, ΔE^Bk selon l'ancre du critère 5 (a). Le total est publié par la fiche 9. Le terme E^CB de l'identité tombe sous E^CB_0 = 0 (fiche 8, critère 2 (a), forme (ii)). (c) **C22** : une limite de détention, si elle existe, est déclarée (paramètre ou base, `CONVENTIONS.md` § 2.4), avec son activité à l'état stationnaire chiffrée ; son activation est le placement raté du cadre (l. 502). Sans limite au socle, la banque absorbe tout le reliquat : c'est déclaré. Le risque de renouvellement relève du J6. Sans limite au socle, un dispositif de scénario, sur le modèle de C31 (part du reliquat non souscrite, entrée exogène par tour, valeur stationnaire 0, publiée), rend exécutables les scénarios de placement raté de la fiche 9 (critères 12 (b) et 16 (c)). Ce n'est ni un drapeau de mode ni une règle à seuil. (d) **19b-banque** : la banque est contrepartie passive des achats décidés de la banque centrale (C17), au pair (titres courts sans prix de marché au socle) : déclaré. (e) **C25** (critère de la fiche 9) : la fiche 7 vérifie que sa règle est compatible avec l'ordre « besoin de l'État, puis banque centrale, puis reliquat de la banque » | Équations ; cas à la main : émission de x u.m., souscription de la banque centrale y, reliquat x − y ; Res avant 8 (c) | `monnaie` ; `macro` (avis) | fiche ; J3 |
| 7 | Offre de crédit et rationnement (C27, C31, #57 ; frontière crédit ; `monnaie`, avis de `macro`) — **exigence** pour (a) à (c), **mesure** pour (d) | (a) **C27** : prix affiché, quantité à la demande, sans plafond au socle ; remboursement accepté (ligne 18 négative). Un plafond quantitatif (v1.5 L^max = E^Bk/κ^CAR, l. 1114 ; v2.0 capacité de prêt, l. 1832 et 1981, L) est une borne à seuil libre exposée à l'instabilité 15 : hors du socle, sauf décision citant M28. (b) **C31** : le refus partiel est un **choc de scénario**. C'est une entrée exogène par tour (part refusée, valeur stationnaire 0), publiée à l'ouverture parmi les conditions et lue par le bloc 6 en phase 3 (lecture (a)). Ce n'est ni un drapeau de mode ni une règle à seuil (ADR 0002). La demande non satisfaite est publiée. Le refus est restitué au joueur comme un événement externe nommé, avec sa durée et la demande non satisfaite (avis de `jeu`). Le scénario « refus de la moitié du crédit pendant 12 tours » est exécutable sur le bloc 6 (`sec:investissement-conditions` l. 1895). (c) **#57**. La fiche instruit deux éléments, chacun avec le contrat qu'il rouvre : la place d'un accélérateur financier (écart lu sur E^Bk/L par i_L, compatible avec C28 ; ou facteur de disponibilité du crédit dans le plan du bloc 6, qui rouvrirait M28) ; la **ligne nommée de part non payée** des entreprises (intérêts de la ligne 9 non payés : capitalisation nommée, ou perte imputée à E^Bk). Verdict attendu : « limite déclarée au socle, forme transmise au J6 » (aucune crise de crédit n'atteint l'investissement au socle, fiche 6 § 3.F), ou « retenu au socle », motivé. (d) **Monnaie endogène** : le crédit crée les dépôts (ligne 18, porte de M, signe +). Sous C27, l'offre ne dépend pas des réserves ; l'absence de contrainte de réserves (multiplicateur) est déclarée | Tableau de l'interface (conditions publiées, demande, ligne 18, phase) ; cas à la main du critère 1 avec un refus de moitié | `monnaie` ; `macro` | fiche ; J3 (C31) ; J6 (#57) |
| 8 | État stationnaire en forme fermée (gabarit 2 ; `monnaie` ; `macro` pour le bouclage conjoint) — **exigence** | (a) Trajectoire de référence des fiches 3 à 6 : volumes en hausse de γ = (1 + g)^{1/n_a} − 1 par pas, prix de (1 + π̄)^{1/n_a} − 1 par pas. Valeurs stationnaires en forme fermée, sans simulation : i_L, i_D et leurs écarts à i_CB ; Π^Bk/E^Bk ; Div_Bk/Π^Bk ; E^Bk/L ; Res, L^CB, B_Bk et D_H + D_F rapportés à 12 × PIB nominal du pas ; rendement réel des dépôts. Valeurs de l'état initial résolu : E^Bk_0, Res_0, L^CB_0, i_{L,0}, i_{D,0}. (b) Indépendance envers les vitesses ; dépendance envers n_a déclarée et chiffrée pour n_a ∈ {4 ; 12 ; 52} (ADR 0008, I.6). (c) **C30** : les grandeurs du bilan bancaire qui dépendent de π̄ (L/(12 PIB) de 0,622 à 0,334 entre π̄ = 2 % et 10 %, fiche 6 § 6.3, chiffres de la fiche) sont écrites en forme fermée à π̄ ∈ {0 ; 2 % ; 10 %}, déclarées, et testées avec C15 (fiche 8). (d) Le bloc ne fixe ni i_CB (fiche 8) ni B/PIB (fiche 9) | Calcul à la main. Au J3, un pas sans choc depuis l'état résolu laisse les variables d'état et les ratios du bloc sur leur sentier à **1e−10 près en relatif** (seuil des fiches 2 à 6, reconduit), pour π̄ = π* ∈ {0 ; 2 % ; 10 %} et n_a ∈ {4 ; 12 ; 52} | `monnaie` ; `macro` (bouclage) | fiche ; J3 |
| 9 | Aucune vitesse ne détermine l'état d'arrivée (`docs/exigences.md` § 2.7 ; `monnaie`) — **exigence** | (a) Aucune vitesse du bloc (ajustement de i_L et de i_D, distribution, remboursement de L^CB) ni la durée du pas n'apparaît dans les formes fermées du critère 8. (b) E^Bk, Res et L^CB ont chacun une ancre (critères 2 et 5). (c) Si une dépendance subsiste, elle est écrite et chiffrée pour chaque vitesse ×0,5 et ×2, avec la condition qui la supprime | Calcul à la main. Sur la maquette conjointe (A4), puis au J3, dans chaque branche où une vitesse ou un gain est ×0,5 et ×2 (λ ≤ n_a) : (i) **point fixe** résolu, identique entre branches à 1e−6 près en relatif, avec π̄ = π* ; (ii) **module dominant < 1**, hors racine nominale et hors état inerte déclaré, aucun n'entrant dans un ratio testé ; (iii) **arrivée simulée** après chacun de trois chocs — dépense publique +1 % aux tours 1 à 12 ; marche de π* de +1 point ; π^e +1 point au tour 0 — : écart relatif de chaque ratio au point fixe de sa branche, et entre branches, d'au plus **1e−6 après H = max(720 ; 20 demi-vies de la racine dominante mesurée) pas**, H déclaré avant l'essai ; (iv) après une dépense publique +1 % permanente, arrivée au point fixe déplacé à moins de 1e−3 en au plus 20 demi-vies (C36 (ii-b), rédaction de M28). Le choc « dépense publique » est un déplacement de l'ancre de dépense de la règle de référence, ou du levier, défini une fois pour les fiches 6, 8 et 9. L'amendement de la fiche 6 (2 160 pas) reste en vigueur. Lieu d'exécution des simulations à horizon H (CI, job séparé ou hors CI, sortie publiée) fixé au plan de J3 (`architect` : au plafond de 52/12 ms par pays-pas, H = 12 640 pas coûte 54,8 s par simulation) | `monnaie` | fiche ; J3 |
| 10 | Stabilité (gabarit 3 ; `monnaie`) — **exigence** pour le rayon spectral ; **mesure** pour la période et la demi-vie | (a) **Instabilités connues** (`tab:instabilites`, l. 2315-2331), non réintroduites sans fait nouveau : n° 16, tolérances absolues sur des soldes résiduels (G2, J2, K2c, S+O ; mécanisme L, `model.py` l. 1280-1283) ; n° 15, un plafond produit un cycle, pour tout plafond de crédit ou de détention ; n° 4, si un écart lit un taux naturel estimé. Le cycle de Minsky « qui émerge sans être scripté » de la v1.5 (l. 1141) est un récit R, non un fait mesuré. (b) **Boucle propre du bloc** (E^Bk, écart endogène éventuel, Res et L^CB), à taux directeur et demande exogènes : modules strictement inférieurs à 1 à la calibration proposée et pour chaque vitesse ×0,5 et ×2 ; demi-vie en tours ; période si les racines sont complexes. (c) Si l'écart de taux est endogène (E^Bk/L) : la boucle écart → i_L → plan d'investissement → crédit → E^Bk/L, avec le bloc 6 sous F, a un rayon spectral inférieur à 1 aux mêmes grilles. (d) La boucle conjointe avec la règle de taux est mesurée à la fiche 8 (C10), avec la transmission de la fiche 7 | `tab:instabilites` ; valeurs propres à la main ou par `uv run python`, commande et sortie citées | `monnaie` | fiche ; J3 ; fiche 8 ((d)) |
| 11 | Test zéro des ratios du bloc (O1 ; `docs/exigences.md` § 2.6 ; `monnaie`) — **exigence**, mesurée au J3 | 720 pas sans choc depuis l'état résolu, plusieurs graines, moyennes par blocs de 60 pas. **Bandes proposées**, à confirmer par le mainteneur avec O1 avant l'essai (M19) : masse monétaire D_H + D_F d'ouverture / (12 × PIB nominal du pas), ±10 % en relatif (« monnaie/PIB à ±10 % », point de départ d'O1, `docs/exigences.md` § 1.3) ; fonds propres sur crédits, ±10 % en relatif ; écarts i_L − i_CB et i_CB − i_D, ±0,1 point ; B_Bk/(12 PIB), bande commune avec B/PIB de la fiche 9 ; Res et L^CB, ±10 % en relatif de leur rapport à 12 × PIB quand leur valeur stationnaire est non nulle, nullité à 1e−12 × S^Bk près quand la règle la rend nulle. Toute dérive depuis l'état résolu est un défaut | Au stade de la fiche, le préalable (critère 8) ; au J3, test zéro du socle | `monnaie` ; mainteneur (bandes) | J3 |
| 12 | Bornes (gabarit 6 ; #38, lecture (ii) ; `CONVENTIONS.md` § 2.4 ; `monnaie`) — **exigence** | (a) Chaque borne de chaque option est classée par le critère de tri de `CONVENTIONS.md` § 2.4 : Res_{t+1} ≥ 0 (identité de clôture du cadre) ; L ≥ 0 (conservation, fiche 6) ; Div_Bk ≥ 0 (domaine, critère 5) ; plancher de i_D ou de i_L (seuil libre) ; plafond de crédit (seuil libre, critère 7) ; limite de détention de titres (seuil libre ou base, critère 6) ; écrêtages de la v1.5 ((·)^+ l. 1103 ; clip de Div^Bk l. 1127) et de la v2.0 (`max(…, 0)` l. 735 et 802 ; `np.clip` l. 1166). (b) Un mécanisme est préféré à la borne. (c) **Instabilité 15** : aucune borne n'est active à l'état stationnaire ni sous les scénarios O2. Scénarios adverses : i_CB abaissé à son plancher pendant 12 tours ; i_CB relevé de 5 points pendant 12 tours ; refus de la moitié du crédit pendant 12 tours (C31). Une borne qui s'y active cesse de l'être **au plus tard 12 tours après la fin du choc** et ne se réactive pas sans nouveau choc (seuil reconduit) | Décompte des bornes par option, avec leur classement ; cas à la main ; au J3 ou au J4, scénarios | `monnaie` ; mainteneur (classement) | fiche ; J3 ou J4 |
| 13 | Lisibilité pour le joueur (gabarit 5 ; `monnaie`, à soumettre à `jeu`) — **exigence** pour (b), **mesure** pour (a), (c), (d) et (e) | (a) **Indicateurs au tour**, chacun avec sa définition, son unité, son dénominateur et sa fenêtre : i_L, i_D et leurs écarts au taux directeur ; rendement réel des dépôts ; crédit nouveau et demande non satisfaite (avec la fiche 6) ; masse monétaire au PIB (clôture / 12 derniers tours ; facteur 1,0216 publié pour un ratio en u.m., `sec:cadre-calendrier` l. 228-232) ; fonds propres sur crédits ; Π^Bk et Div_Bk sur 12 tours ; Res et L^CB ; B_Bk au PIB. Les niveaux normaux sont publiés par le script d'état stationnaire. Les indicateurs sont rangés en deux niveaux : **tableau du tour** (i_L, i_D et leurs écarts au taux directeur ; crédit nouveau et demande non satisfaite ; masse monétaire au PIB) et **fiche détaillée de la banque** (Π^Bk et Div_Bk sur 12 tours, fonds propres sur crédits, Res, L^CB, B_Bk au PIB). (b) **Délais en tours entiers** : taux directeur décidé au tour n → lignes 12 et 13 au tour n (délai du premier flux nul) → Π^Bk au tour n → i_L et i_D au tour n + 1 → plans du tour n + 1, consommation au tour n + 2 (C35). Contrepartie visible le même tour : résultat de la banque, réserves, refinancement. Aucun effet plus rapide que le tour sans contrepartie. (c) Tableau levier → indicateur → délai → contrepartie pour le taux directeur, les achats de titres de la banque centrale (19b-banque) et la dépense publique (19a-banque). Leviers propres du bloc : aucun au socle sans décision (Q7) ; aucun drapeau de mode. (d) **Ampleur** : variation de Π^Bk et de Div_Bk pour un point de taux directeur, perceptible à l'échelle d'une partie (60 à 120 tours). **Seuils de `jeu`** (mesure, écrits avant l'essai) : (d1) pour i_CB +1 point maintenu, i_L et i_D s'écartent du contrôle d'au moins 0,5 point (cinq crans) au tour n + 1 ; (d2) le rendement des fonds propres de la banque sur 12 tours est restitué en points, et son écart au tour 12 est publié ; (d3) la part de Div_Bk et des intérêts des dépôts dans la variation du revenu disponible des ménages aux tours 2, 3 et 12 est publiée, pour que le signe de #56 soit explicable au joueur. Le saut de Π^Bk au seul tour de la décision (C29) n'est restitué que dans la fenêtre de 12 tours, avec une infobulle. d1 reste une mesure, non une exigence (la complétude de la transmission est contestée, critère 17) : un écart à d1 est publié et transmis à `jeu`, sans écarter d'option (`monnaie`). Un signe contre-intuitif (marge gonflée ou comprimée au tour de la décision, C29) est déclaré. (e) **Perceptibilité à l'échelle d'une partie** (mesure ; avis de `jeu`, accepté par `macro` et `monnaie`), définie avant l'essai : (i) au moins un indicateur du tableau du tour s'écarte du contrôle apparié d'au moins **deux crans d'affichage** (0,2 point pour un taux, un glissement ou un ratio affiché en % à une décimale ; 0,2 % pour un niveau) dans les **12 tours** qui suivent la décision ; (ii) le pic de l'écart survient au plus tard au **tour 24** ; (iii) toute dynamique de demi-vie supérieure à **60 tours** est déclarée, avec l'écart résiduel qu'elle laisse au tour 60 sur le glissement et sur la production. Un écart résiduel supérieur à un cran au tour 60 est signalé à `jeu` comme transition non attribuable. | Tableau du § 9 (« Interfaces ») ; exemple daté à la main, i_CB +1 point aux tours 1 à 12, indicateurs aux tours 1, 2, 3, 12, 13 et 24 ; avis de `jeu` (§ 7) ; au J4, scénario apparié (O2) | `jeu` ; `monnaie` (exemple daté) | fiche ; J4 |
| 14 | Simplicité, empreinte sur l'état, déterminisme (gabarit 6 et rubrique 9 ; principe de simplicité ; `monnaie`) — **mesure** (décompte) et **exigence** (sans historique ni drapeau) | Décompte par option : paramètres, bornes, variables d'état, lignes et phases touchées, chacun justifié par une identité vérifiable ou un mécanisme perçu. Chaque variable d'état a son unité et sa valeur stationnaire. Une seule règle par mécanisme : les drapeaux bancaires de la v2.0 (`bank_issue`, `spread_excl_cb`, `adv_interest`, `div_coverage`, `model.py` l. 286 ; `phi_liq`, l. 246 ; L) ne sont pas repris comme modes (ADR 0002). Aucun tirage, ou un tirage par la graine du pays, déclaré | Tableau de décompte ; liste des variables d'état | `monnaie` | fiche ; J2 (reprise exacte) |
| 15 | Coût de calcul (gabarit 4 ; `monnaie`) — **exigence** (aucune itération) et **mesure** (décompte) | Aucune itération ni optimisation à chaque pas (ADR 0002). Décompte des opérations par pas. **Part indicative : 0,48 ms par pays-pas** (reconduite des fiches 2 à 6) | Décompte dans la fiche ; au J3, `tests/invariants/test_budget.py` | `monnaie` ; `audit` | fiche ; J3 |
| 16 | Notation (`CONVENTIONS.md` § 5.2 ; décision du 02/10/2026 sur #23 ; `monnaie`) — **exigence** | Chaque symbole a un seul sens et n'entre en collision ni avec les indices réservés (c, j, k, h, t ; s, ℓ, u) ni avec `tab:symboles`. À renommer en particulier : les marges m^L et m^D de la v1.5 (m est la propension de la demande induite) ; κ^CAR (κ_j est pris) ; ϱ_1, ϱ_2 et ϱ^res (ϱ_L est pris) ; le levier ℓ_j (ℓ est l'indice de ligne) ; Λ^Bk. E^Bk, Π^Bk, Div_Bk, i_L, i_D, i_res, i_CB, L^CB et Res gardent leur sens (`tab:instruments`). Est aussi pris : b (dette nette hors banque centrale, `sec:menages`) | Liste des symboles confrontée à `tab:symboles` (commande `grep` et sortie citées) | `monnaie` ; `docwriter` (section) | fiche ; section proposée |
| 17 | Calibrabilité et faits établis (`monnaie`) — **mesure** | Les paramètres se calibrent sur des ordres de grandeur établis, chacun avec sa source retrouvée et sa date : marges d'intermédiation ; vitesse et complétude de la transmission du taux directeur aux taux des dépôts et du crédit ; ratio de fonds propres ; rentabilité des fonds propres ; taux de distribution. La complétude de la transmission est **contestée** : la v1.5 la déclare « en réalité partielle et retardée » (l. 1110) sans source. κ^CAR = 0,09 (v2.0 l. 221) est un choix de la première tentative ; « 8 % dans les accords de Bâle » (v1.5 l. 1118) est à vérifier contre sa source. Un résultat de la v1.5 ou de la v2.0 n'est pas un fait établi : ainsi le taux apparent d'emprunt (13,22 %) et des dépôts (8,18 %) de G-T (S+O), résultats du modèle v2.0. Une source introuvable est déclarée | Sources citées ; « non trouvée » le cas échéant | `monnaie` | fiche ; J3 (calibration) |
| 18 | Remesure des faits de la première tentative (décision P1 du 03/10/2026 ; `CONTEXT.md` ; `monnaie`) — **exigence** de procédure | (a) Chaque fait cité porte son statut (S+O, O, R, L, V, V+O). Les faits établis sur D1 ne sont pas remesurables, D1 n'étant pas versé. (b) Toute remesure (statut V) passe par un script d'`outils/` qui exécute le prototype **dans un processus séparé, jamais par import** (invariant 4), revu par `audit` (circuit 3). Ses critères sont écrits dans la fiche avant l'essai et son verdict est publié, même défavorable. (c) Un fait V sur le prototype v2.0 reste un fait de la première tentative. (d) Les lectures de code (L) citent fichier et ligne, avec la branche active et les coefficients effectifs. Dans D1, seuls `adv_interest=True` et `residual_tolerance='stock_aware'` sont établis parmi les réglages bancaires (`archive/faits_mesures_G_K.md` § 1.1) ; les valeurs de `mL`, `mD`, `kappa_CAR`, `bank_issue` et `div_coverage` dans D1 ne le sont pas | Liste des faits et statuts ; commande, sortie et commit de chaque script | `monnaie` ; `coder` ; `audit` | fiche (jalon 2) |

### Amendements adoptés

Décisions du mainteneur du 04/10/2026, prises avant l'instruction, sur les questions des experts (validation groupée des critères des fiches 7, 8 et 9, P14) :

- **Critères** : la liste est validée telle qu'amendée par la relecture croisée du 04/10/2026 (avis de `macro`, `monnaie` et `jeu` ; qualifications d'`architect`), avec la nature de chaque critère (exigence ou mesure) ; les seuils reconduits et les seuils de `jeu` sont adoptés.
- **Options marquées « à trancher par le mainteneur » au choix M31 à M33** (propriétaire des lignes 19a, règle de i_B, règle de M^{G*} et lecture du contrôle de caisse, forme de E^CB) : instruites telles qu'écrites, avec leur qualification (interprétation ou modification) ; elles se décident aux décisions de fiche, non à cette validation.
- **Critère 9 et seuils de `jeu` (critère 13 (d))** : adoptés en mesure, comme écrits.

## 3. Options

À instruire (jalon 2).

## 4. Tableau comparatif

À instruire (jalon 2).

## 5. Avis de l'expert pilote

À instruire (jalon 2).

## 6. Avis de l'expert consulté

À instruire (jalon 2).

## 7. Avis de `jeu`

À instruire (jalon 2).

## 8. Décision du mainteneur

À instruire (jalon 2).

## 9. Conséquences de la décision

À instruire (jalon 2).

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 04/10/2026 | Ouverture (issue #71) ; § 1 et § 2 proposés (jalon 1), en attente de validation des critères par le mainteneur | `monnaie` ; session principale |
| 04/10/2026 | Relecture croisée intégrée (avis de `macro`, `monnaie` et `jeu`, une relance ciblée ; qualifications d'`architect`) ; options ouvertes marquées « à trancher par le mainteneur » | `macro` ; `monnaie` ; `jeu` ; `architect` ; session principale |
| 04/10/2026 | Critères validés par le mainteneur (jalon 1 de #71 terminé), amendements adoptés consignés au § 2 | mainteneur ; session principale |
