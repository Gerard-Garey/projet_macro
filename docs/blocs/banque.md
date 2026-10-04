---
bloc: Banque commerciale
module: src/nations/blocs/banque.py
expert pilote: monnaie
experts consultés: macro (demande de crédit des entreprises : frontière crédit ; placement de la dette publique, avec la fiche 9) ; jeu
statut: spécifiée
décision: M31 (04/10/2026)
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

*Instruit par `monnaie` (expert pilote) le 04/10/2026, sur la fiche à l'état `5f2f2d6` (branche `claude/j1-monnaie-etat`, PR #77). Les numéros de ligne de `docs/specification/nations_et_marches.tex` sont ceux de cet état. Ceux d'`archive/` ont été vérifiés le même jour. Aucun chiffre de ce paragraphe n'est un résultat du moteur v3, qui n'exécute rien : ce sont des formes fermées ou des sorties de maquette.*

### 3.0 Conventions de l'instruction

**Découpage par question** (gabarit § 3).
- Le bloc tranche sept questions largement indépendantes (§ 1.5, Q1 à Q7).
- Les options A (v1.5) et B (v2.0) sont instruites en entier.
- Sur Q4 (placement), Q5 (offre), Q6 (propriétaires des lignes), Q7 (leviers), les phases et la règle de caisse, les contrats hérités ne laissent qu'une forme compatible : C19, C22, C25, C27, C31 et la lecture (a) de M28. Cette forme est instruite une fois, comme socle commun des options nouvelles (§ 3.N).
- Les options nouvelles diffèrent sur Q1 (transmission), Q2 (refinancement et réserves) et Q3 (fonds propres et distribution) :
  - l'option C (corridor explicite à position nette) répond aux trois ;
  - l'option D (banque des modèles de Godley et Lavoie) aussi ;
  - des variantes à une seule question (§ 3.V) se combinent avec C.
- La variante sans retard R sert de référence (`docs/exigences.md` § 2.7).

**Transposition de A et B dans le cadre v3** (hypothèses déclarées) :
- une banque et un seul bien (J = 1) ;
- taux annuels convertis linéairement, x/n_a. La v1.5 écrit « par tick », et la v2.0 convertit géométriquement (`model.py` l. 40, `wk(r) = (1 + r)^{1/52} − 1`) ;
- lectures ramenées aux phases v3, lignes de `tab:matrice-flux`.

**Calibration indicative.** Ce sont des hypothèses, pas des faits.

| Grandeur | Valeur | Source |
|---|---|---|
| g ; δ ; t̄u ; κ_j ; lv\* ; ν_F ; μ̄ ; σ_j | 2 % ; 5 % ; 0,8 ; 1,6 an ; 0,4 ; 1/6 an ; 0,25 ; 1,4/12 an | fiches 2 et 6 (`sec:investissement-stationnaire` l. 1853) |
| Taux directeur stationnaire | i_CB = (1 + r̄)(1 + π̄) − 1, avec r̄ = 1 % | hypothèse de la fiche 6 (l. 1708) ; la forme sera fixée par la fiche 8 (critère 5 (c)) |
| V_H/(12 PIB) = ν_H·YD^HS/PIB | 0,7 (variantes 0,6 et 0,8) | illustration de la fiche 9 (§ 1, point 1) |
| M^G\* | un pas de paiements bruts égaux à 25 % du PIB du pas, soit M^G\*/(12 PIB) = 0,020833 | hypothèse ; la règle relève de la fiche 9 (critère 11) |
| B_CB ; E^CB | 0 ; 0 | s_CB = 0 (hypothèse) ; forme (ii) de la fiche 8 (critère 2 (a)) |
| i_B ; i_res | i_CB du tour ; i_CB | option (i) de M33, recommandation commune ; corridor de largeur nulle (hypothèse, fiche 8) |
| ϖ_L ; ϖ_D (écarts) | 2 % ; 1 % ; variante basse 0,4 % ; 0,214 % | v1.5 l. 2264 (R) ; la variante basse est calée sur un rendement des fonds propres de 10 % à π̄ = 2 % (hypothèse) |
| ϑ (fonds propres visés sur crédits) | 0,10 | hypothèse, entre les 8 % de Bâle (1988) et 1,3 × 0,09 de la v2.0 (`model.py` l. 221 et 1164) |

**Ratios amont recalculés** (maquette `f7_stat.py`, formes de `sec:production-stationnaire` l. 750-760 et de `sec:investissement-stationnaire`).
- À π̄ = 2 % et 10 %, la maquette redonne exactement les chiffres de la fiche 6 (l. 749-753) : L/(12 PIB) = 0,62204 et 0,33439 ; D_F/(12 PIB) = 0,16605 et 0,16492 ; K/(12 PIB) = 1,55510 et 0,83598.
- À π̄ = 0, valeurs que la fiche 6 ne publie pas : L = 0,80037 et D_F = 0,16636.
- À π̄ = 2 % et n_a = 4 / 52 : L = 0,621423 / 0,622275.

**Mesures exécutées.** Le détail (commandes et sorties) figure au compte rendu, sous le titre de même nom.
- `uv run python outils/verifier_matrices.py --strict` : 9 / 28 / 28 lignes, 44 / 62 / 31 termes, « Aucun écart. », code 0. Aucune option recommandée ne change ces tables.
- Maquettes dans un répertoire temporaire (`mktemp -d`), sans aucun import d'`archive/` : `f7_stat.py` (états stationnaires), `f7_dyn.py` (exemple daté, dates de Div_Bk, règle de la v2.0), `f7_cas.py` (cas à la main en fractions exactes), `f7_plancher.py` (scénario de plancher).
- Aucun prototype exécuté, aucune remesure de statut V : la décision ne dépend d'aucun chiffre de la v2.0 qu'il faudrait remesurer (critère 18 (b)).

**Littérature.**

*Lue* :
- W. Whitesell, « Monetary Policy Implementation Without Averaging or Rate Corridors », FEDS 2006-22, Federal Reserve Board, p. 4 et 5.
  - p. 4 : « In a rate corridor regime, the central bank's lending rate provides a ceiling for overnight interest rates while its deposit rate provides a floor (Woodford, 2001). […] in the absence of reserve requirements […] the demand for such balances should equal zero at that rate. »
  - p. 5 : en pratique, la demande au taux cible est positive, et les taux sont volatils dans le corridor.
- M. McLeay, A. Radia et R. Thomas, « Money creation in the modern economy », *Bank of England Quarterly Bulletin* 2014 Q1, p. 14-27, résumé lu (EconPapers) : les banques ne « multiplient » pas la monnaie centrale ; le crédit crée les dépôts.
- G. de Bondt, « Retail bank interest rate pass-through: new evidence at the euro area level », ECB Working Paper 136, 2002, résumé lu (RePEc) : la transmission en un mois atteint au plus environ 50 % ; à long terme, elle est proche de 100 %, surtout pour les taux du crédit.
- I. Drechsler, A. Savov et P. Schnabl, « The Deposits Channel of Monetary Policy », *Quarterly Journal of Economics* 132(4), 2017, p. 1819-1876, résumé lu (NBER w22152) : quand le taux directeur monte, les banques élargissent l'écart sur les dépôts.
- W. Godley et M. Lavoie, *Monetary Economics*, 2007, chap. 7 (modèle BMW), 10 (INSOUT) et 11 (GROWTH), lus par les reproductions du paquet R `sfcr` de J. Macalós. Livre non lu. Lignes citées :
  - `gl5-bmw.Rmd` l. 47, 60-61, 79 ;
  - `gl7-insout.Rmd` l. 69, 332-335, 349-376, 508-532 ;
  - `gl8-growth.Rmd` l. 185-217.

*Existence vérifiée, contenu non lu* :
- W. Whitesell, « Interest rate corridors and reserves », *Journal of Monetary Economics* 53(6), 2006, p. 1177-1195. RePEc n'affiche aucun résumé ; ScienceDirect et la copie en ligne sont bloqués par le proxy.
- W. Poole, *Journal of Finance* 23(5), 1968, p. 769-791.
- B. J. Moore, *Horizontalists and Verticalists*, Cambridge University Press, 1988 (thèse rapportée par des résumés secondaires).
- G. de Bondt, *German Economic Review* 6(1), 2005, p. 37-78.
- T. Keister, A. Martin et J. McAndrews, « Divorcing Money from Monetary Policy », *FRBNY Economic Policy Review* 14(2), 2008, p. 41-56 : début du résumé et mention d'un « floor system » lus dans un extrait de moteur de recherche.
- Comité de Bâle, 1988 : le ratio de 8 % est lu dans un extrait de moteur de recherche ; le PDF de la BRI est inaccessible (le proxy renvoie du HTML).

*Ce que la littérature permet de conclure* :
- La transmission complète en un tour est plus rapide que ce que mesure de Bondt (2002).
- Un écart des dépôts constant ignore le « canal des dépôts » (Drechsler et al., 2017).
- Le corridor sans exigence de réserves implique une demande nulle de réserves au taux cible (Whitesell, FEDS 2006-22, p. 4).
- Elle ne permet pas de conclure sur le niveau du rendement des fonds propres ni sur le taux de distribution des banques : aucune source n'a été cherchée à ce jalon, à faire au J3 (critère 17).

**Statut des faits de la première tentative** (critère 18).

| Fait | Source | Statut |
|---|---|---|
| Res obtenu comme solde du bilan bancaire, partie négative reportée sur L_cb | `model.py` l. 1278-1283 ; copies l. 556-557, 1574-1575, 1631-1632 | L |
| L_cb jamais remboursé (cliquet) | toutes les affectations de `L_cb` ne font que l'augmenter : l. 551 (0), 557, 1283, 1575, 1632, 1863 (grep au compte rendu) | L (lecture de `monnaie`, 04/10/2026) |
| Échecs d'invariance de `Res` et `L_cb` aux tolérances héritées | `archive/faits_mesures_G_K.md` § 5, G2 | S+O |
| Premier franchissement de `Res` en semaine 910, de `L_cb` en semaine 1 154 | idem, J2 et K2b | S (O jusqu'à 920) |
| Arrêt en semaine 824 sous redénomination ×100 | idem, K2c | S+O |
| Taux apparents d'emprunt (13,22 %) et de dépôt (8,177 %) | idem § 3, G-T | S+O ; résultat du modèle v2.0, pas un fait établi |
| Seuls `adv_interest=True` et `residual_tolerance='stock_aware'` sont établis dans le profil D1 ; `mL`, `mD`, `rho1`, `kappa_CAR` y sont inconnus | idem § 1.1 ; défauts de `Params` l. 221 | non établis |
| « Falaise » sans émission d'actions ; crédit bloqué sans recapitalisation (chômage de 68 %) ; cycle de Minsky « qui émerge » | v1.5 l. 1138, 1143, 1141 | R ; le cycle de Minsky est un récit |
| Ping-pong du ratio de liquidité sous des bandes serrées (INSOUT) | `gl7-insout.Rmd` l. 508-532 | rapporté par une reproduction tierce, non exécuté |

**Notation proposée** (critère 16).
- Commande : boucle `grep -c "\\<symbole>\b"` sur la spécification.
- Sortie : `varsigma 0`, `varpi 0`, `vartheta 0`, `chi 1`, `theta` employé (θ_H), `omega` 14.
- Symboles proposés :
  - ϖ_L, ϖ_D : écarts du crédit et des dépôts au taux directeur, par an, taux de flux. La fiche 4 proscrit ϖ « sans indice distinctif » (`prix.md` l. 212) ; ici il porte un indice. Alternative : ψ_L, ψ_D ;
  - ϑ : fonds propres visés, fraction des crédits de clôture ;
  - ς_{L,t} : part refusée de la hausse de crédit demandée, entrée de scénario ;
  - ς_{B,t} : part non souscrite du reliquat de l'émission, entrée de scénario.
- Aucun n'entre en collision avec les indices réservés ni avec `tab:symboles`. Sont proscrits :
  - m^L, m^D (m est la propension de la demande induite) ;
  - κ^CAR (κ_j est pris) ;
  - ϱ_1, ϱ_2 (ϱ_L est pris) ;
  - ℓ_j (ℓ est l'indice de ligne) ;
  - toute marque en s (indice des secteurs).

### 3.A Option A — v1.5

1. **Source.** `archive/v1.5/Nations_et_Marches_v1_5.tex`, section « Banque commerciale et monnaie endogène » (`sec:banques`).
   - Taux bancaires : l. 1102-1105, avec leur lecture l. 1106-1111.
   - Plafond et rationnement : l. 1112-1123.
   - `eq:bankeq` : l. 1124-1131, lecture l. 1132-1139.
   - Insolvabilité et recapitalisation : l. 1140-1143.
   - Côté banque centrale :
     - réserves rémunérées à i^CB − Δ : l. 984 et 997 ;
     - réserves obligatoires ϱ^res : l. 985 ;
     - `eq:ecb` : l. 998-1005 ;
     - ruée : l. 1406.
   - Placement :
     - limite de 40 % du bilan : l. 1520 ;
     - intérêts publics impayés capitalisés : l. 1522 ;
     - adjudication : l. 1525.
   - Calibration : l. 2262 (ℓ̄ = 0,6) ; l. 2263-2264 (κ^CAR de 8 à 10 % « Bâle » ; m^L, m^D = 2 %, 1 %) ; l. 2316 (révision v0.9 : 0,01 et 0,01) ; l. 2320, 2336-2338.
   - Ces équations n'ont jamais été garanties exécutées.
2. **Équations** (notation v1.5).
   - i^L_j = i^CB + m^L + ϱ_1(ℓ_j − ℓ̄)^+ + ϱ_2 ρ̂^NPL et i^D = (i^CB − m^D)^+ (l. 1103-1104). Choix de conception.
   - L^max = E^Bk/κ^CAR ; Λ^Bk = min(1, (L^max − L)/ΣΔL^dem)^+, qui multiplie l'investissement (l. 1114-1115 et 1123).
   - ΔE^Bk = i^L L − i^D D − i^CB L^CB + i^B B^Bk − Pertes − Div^Bk + ΔE^ém (l. 1126).
   - Div^Bk = ϖ^Bk·clip(CAR/(1,3κ^CAR); 1; 3)·(E^Bk − Ē^Bk)^+, avec ϖ^Bk = 5 % par semaine (l. 1127 et 2337).
     - Ē^Bk n'est défini nulle part. **Interprétation** : soit un niveau, soit 1,3κ^CAR·L, forme de la v2.0.
   - ΔE^ém = min(1,3κ(L + …) − E ; 2 % des dépôts par semaine) quand 0 < CAR < 1,1κ (l. 1128).
   - Recapitalisation publique :
     - seuil : E^Bk < ½κ^CAR L (l. 1137 et 2338) ;
     - montant : 1,2κ^CAR L ;
     - fréquence : au plus une fois par an (l. 1143).
   - La banque absorbe la dette émise jusqu'à 40 % de son bilan (l. 1520).
   - Aucune règle ne fixe Res ni L^CB hors d'une ruée (l. 1406 : « réserves, puis refinancement »).
3. **État stationnaire impliqué.**
   - **Écarts** : i_L − i_CB = m^L, la prime de levier étant inerte. Sous la règle F de M28, L/K = lv\* = 0,4 et L/(pK^vol) = 0,311 ; les deux restent sous ℓ̄ = 0,6.
   - **Plancher de i^D** : à π̄ = 0 et r̄ = 1 %, i_CB = 1,0000 % = m^D (révision v0.9). Le plancher est exactement à sa limite.
   - **Fonds propres** : forme fermée sous l'interprétation Ē = 1,3κL (voir 3.B-3). Elle **dépend de la vitesse** ϖ^Bk. Sous l'interprétation « niveau », il n'y a pas d'ancre en ratio.
   - **Res et L^CB** : non déterminés.
   - **Limite de 40 %** (part des titres publics dans l'actif de la banque, maquette, hypothèses du § 3.0) : 0,173, 0,345 et 0,636 à π̄ = 0, 2 % et 10 %. La limite est **active à l'état stationnaire à 10 %**, et à 2 % si YD^HS/PIB = 0,8 (0,407).
4. **Comportement mesuré.** Non mesuré en v3. Les chiffres du prototype de la v1.5 sont rapportés (R) : l. 1138, 1143, 1520 (chômage passant de 5 à 26 % sous plafond sans demande élastique).
5. **Coût.** Une quarantaine d'opérations par pas, sans itération. Conforme.
6. **Défauts et instabilités.**
   - (i) **Écart stock-flux** : `eq:ecb` paie i^res sur les réserves (l. 1000), mais `eq:bankeq` (l. 1126) ne reçoit pas cet intérêt. Le paiement de la banque centrale n'a pas de receveur.
   - (ii) Aucune règle pour Res et L^CB, qui seraient des soldes : instabilité 16 si l'on transpose.
   - (iii) Prime sur le levier de l'emprunteur et sur les créances douteuses : contraire à C28.
   - (iv) Plafond L^max et rationnement Λ^Bk :
     - instabilité 15 ;
     - rouvre M28, lecture (a) (aucun plafond au socle).
   - (v) La limite de 40 % devient active à l'état stationnaire sous C30 : instabilité 15 et placement raté permanent.
   - (vi) Distribution par ajustement partiel : la vitesse fixe l'état d'arrivée.
   - (vii) Émission d'actions et recapitalisation dans le socle. Ce sont des instruments ou lignes absents, à renvoyer au J6.
   - (viii) Intérêts impayés capitalisés dans la dette (l. 1522), contraire à la règle de caisse (l. 481).
   - (ix) L'effet de ϱ^res sur le crédit n'est écrit dans aucune équation : seul Res^ex = Res − ϱ^res D est défini (l. 1416).
7. **Identités de bilan.**
   - Banque et banque centrale.
   - Lignes 9, 10, 11b, 13, 15, 18 et 19a, plus des lignes nouvelles : pertes, actions bancaires, recapitalisation. Ce sont des contrats partagés.
   - Res est implicitement résiduel : solde interdit (critère 1 (b)).
   - La valeur nette de la banque n'est calculée que par les flux, sans contrôle par le stock.
8. **Ce que le joueur percevrait.**
   - Leviers κ^CAR et ϱ^res (l. 985 et 1561), lisibles.
   - Le plafond est une falaise : le rationnement apparaît d'un coup.
   - L'écart de taux bouge peu au socle.
9. **Empreinte sur l'état.**
   - ρ̂^NPL : mémoire sans vitesse déclarée.
   - Date du dernier sauvetage.
   - E^Bk, poste du noyau.
   - i_L et i_D ne sont pas des variables d'état : ils sont immédiats.

### 3.B Option B — v2.0

1. **Source** (statut L, `archive/v2.0/prototype/model.py`).
   - Paramètres : l. 221 (`mL = mD = 0,01`, `rho1 = 0,05`, `rho2 = 0,5`, `kappa_CAR = 0,09`) ; l. 121 (`ell_bar = 0,6`) ; l. 246 (`phi_liq = 0`) ; l. 286 (`phi_Bbank = 0,4`, `bank_issue`, `recap_thresh`, `adv_interest`, `div_coverage`).
   - Taux :
     - i_D : l. 735-737 et 802 ;
     - i_L : l. 1972-1974.
   - Crédit :
     - intérêts des crédits et part impayée capitalisée : l. 1009-1017 ;
     - capacité de prêt et allocation par secteur : l. 899-904, 1976-1981.
   - Fonds propres :
     - recapitalisation : l. 1139-1147 ;
     - émission d'actions : l. 1149-1155 ;
     - ratio de liquidité : l. 1156-1162 ;
     - dividendes : l. 1164-1167.
   - Bilan de banque centrale :
     - coupon impayé capitalisé : l. 1176-1180 ;
     - charge de refinancement et rémunération des réserves : l. 1185-1190.
   - Placement : l. 1220-1246.
   - Réserves résiduelles : l. 1278-1283.
   - Les valeurs de ces paramètres dans D1 ne sont pas établies (critère 18 (d)).
2. **Équations.**
   - i_D = max(i_cb − mD; 0) si E_bank > 0, sinon 0, servi aux seuls dépôts des ménages (l. 735). Les dépôts des entreprises ne sont pas rémunérés.
   - i_L = i_cb + mL + rho1·max(ell − ell_bar; 0), avec ell = Loans/(prix du capital × K), au prix courant (l. 1973-1974).
   - Intérêts hebdomadaires à `wk(r)`, conversion géométrique (l. 40).
   - Crédit :
     - plafond `credit_room` = max(E_bank/kappa_CAR − dette; 0) (l. 1981) ;
     - servi aux secteurs dans l'ordre de leur indice j, premier arrivé (l. 899-904) ;
     - refusé si ell ≥ ell_bar + 0,4 (l. 901) ;
     - `Lam_bank` multiplie l'investissement (l. 865, 1977).
   - Dividendes : 0,05 × clip(car/(1,3κ); 1; 3) × max(E − 1,3κL; 0) par semaine (l. 1164-1167).
   - Émission d'actions sous 1,1κL, plafonnée à 2 % des dépôts des ménages (l. 1149-1155).
   - Recapitalisation (l. 1139-1145) :
     - déclenchement : E < 0, ou E < 0,5κL ;
     - montant : 1,2κL − E ;
     - fréquence : au plus une fois par an.
   - Placement : ménages, puis banque jusqu'à 0,4 × dépôts − B_bank si E > 0 (l. 1225 et 1239). Sinon le rationnement de la dépense ρ_G baisse de 0,1 par semaine et remonte de 0,02 (l. 1244-1246).
   - Res = D + L_cb + E − Loans − B_bank (l. 1280) ; si Res < 0, L_cb += −Res (l. 1282-1283).
   - Réserves rémunérées seulement si `assets`, sur min(Res; B_cb + AG + L_cb) (l. 1187-1190).
3. **État stationnaire impliqué.**
   - Fonds propres (maquette `f7_dyn.py`, marge hebdomadaire hors rendement de E de 2,5 % par an, hypothèse) :
     - forme : E/L = (s + φf·1,3κ)/(γ_w + φf − i_w) ;
     - valeurs : **0,13306 / 0,12554 / 0,12142** pour φ = 0,025 / 0,05 / 0,10 par semaine. La vitesse de distribution fixe l'arrivée.
   - L_cb n'a **aucune ancre** : c'est un cliquet.
   - Res est un solde.
   - Limite de détention :
     - à 2 %, B_Bk/D = 0,378 pour une limite de 0,4, marge de 0,022 ;
     - à 10 %, 0,676 : **active**.
4. **Comportement mesuré.**
   - G2 (S+O), J2 et K2b (S, O jusqu'à 920), K2c (S+O) : instabilité 16.
   - H2 (S+O) passe sur 260 semaines.
   - G-T (S+O) : taux apparents de 13,22 % et 8,177 %, résultats du modèle.
5. **Coût.** Une boucle sur les secteurs pour le crédit, sans itération. Conforme.
6. **Défauts et instabilités.**
   - Réserves résiduelles (instabilité 16).
   - Cliquet de L_cb : Res·L_cb > 0 possible, la banque payant i_cb sur un refinancement inutile.
   - Sept drapeaux de mode : `bank_issue`, `div_coverage`, `adv_interest`, `spread_excl_cb`, `phi_liq`, `assets`, `residual_tolerance`.
   - Conversion géométrique des intérêts, contraire à M22 (a).
   - Coupure de i_D si E ≤ 0.
   - Intérêts et coupons impayés capitalisés dans le principal.
   - Rationnement du crédit dans l'ordre des secteurs, qui dépend de l'ordre des identifiants.
   - Plafond de crédit et limite de détention (instabilité 15).
   - Prime sur le levier de l'emprunteur (C28).
7. **Identités de bilan.**
   - E_bank est tenu par un journal de flux (`bank_equity.change_book`, l. 48) et Res par différence : le contrôle est circulaire (ADR 0005, Contexte).
   - Lignes nouvelles : actions, recapitalisation, capitalisations.
8. **Ce que le joueur percevrait.** Aucun levier bancaire. Le rationnement et le cliquet sont invisibles. Les dépôts des entreprises ne rapportent rien.
9. **Empreinte sur l'état.** `last_recap`, `rhoG`, `_bank_shares`, `bank_failed`, `zombie`, et un historique (ADR 0005, Contexte).

### 3.N Socle commun des options nouvelles (Q4 à Q7, phases, règle de caisse)

**N-1. Propriétaires et phases** (critères 1 (a) et 3).
- Lignes proposées par le bloc 7 :
  - 9 (receveur), 10 et 15, en phase 6 ;
  - 21, en phase 8 (c) ;
  - 19a-banque en phase 7 seulement sous la variante de M33.
- Sous A8, le bloc 9 propose les trois lignes 19a, et la banque ne siège pas en phase 7.
- Lignes reçues : 11b (bloc 9) ; 12 et 13 (bloc 8, phase 8 (a)) ; 18 (bloc 6, lecture (a) de M28) ; 19b-banque (bloc 8).

| Phase | Le bloc 7 lit | Le bloc 7 écrit ou propose | Autres blocs (6, 8, 9) |
|---|---|---|---|
| 0 | — | publie dans l'état d'ouverture i_{L,t}, i_{D,t} et les entrées de scénario ς_{L,t}, ς_{B,t} | moteur |
| 1 | — | rien | bloc 8 : i_CB,t, i_res,t, Π^CB_t (et s_CB sous A8) ; i_B,t ≡ i_CB,t (option (i)) |
| 3 | — | rien | bloc 6 : ligne 18 = (1 − ς_{L,t})·max(ΔL^d; 0) + min(ΔL^d; 0) ; publie la demande non satisfaite |
| 6 | ouverture (L_t, B_Bk,t, Res_t, L^CB_t, D_{H,t}, D_{F,t}, E_t, i_{L,t}, i_{D,t}) ; phase 1 (i_CB, i_res, i_B) ; ligne 18 exécutée en phase 3, d'où L_{t+1} | Π^Bk_t ; lignes 9, 10 et 15 | bloc 6 : lignes 8 et 14 (F3 recalcule 9 et 10 sur l'ouverture) ; bloc 9 : 6, 7, 11a à 11c. Aucun ordre interne |
| 7 | rien sous A8 ; sous la variante, le besoin (bloc 9) et 19a-BC (bloc 8) | rien sous A8 ; 19a-banque sous la variante | bloc 9 : lignes 19a (A8) ; bloc 8 : 19b-banque |
| 8 (c) | Res après 8 (b), au grand livre ; L^CB_t ; i_CB,t | ligne 21 ; i_{L,t+1} et i_{D,t+1} | bloc 8 en (a) et (b) |
| 9 | — | rien | noyau : Res_{t+1} ≥ 0, E^Bk calculé deux fois |

- La matrice des lectures est triangulaire.
- Écrire i_L et i_D en 8 (c) est une **interprétation**. L'ADR 0009, point 4 (l. 43), désigne cette phase quand toutes les entrées la précèdent. Il faut ajouter la mention dans la colonne « Contenu » de la ligne 8 de `tab:phases`, retouche à qualifier par `architect`.
- La banque n'écrit plus rien en phase 3. Il en va de même en phase 7 sous A8. La retirer des écrivains de ces phases est une retouche de forme, sur le précédent de M29 qui a retiré les ménages de la phase 7.

**N-2. Offre de crédit** (critère 7).
- (a) Le crédit est servi au taux affiché, à la demande, sans plafond. Le remboursement est accepté (ligne 18 négative).
- (b) **C31** : ς_{L,t} est une entrée exogène par tour, de valeur stationnaire 0, publiée à l'ouverture. Elle ne porte que sur la hausse demandée. Ce n'est ni un drapeau ni une règle à seuil. Le scénario « refus de la moitié pendant 12 tours » s'écrit ς_{L,t} = 0,5 aux tours 1 à 12.
- (c) **#57** : limite déclarée au socle, forme transmise au J6. La part non payée de la ligne 9 aurait deux formes possibles :
  - capitalisation nommée : ligne « intérêts capitalisés », L monte sans mouvement de dépôts, sans effet sur M ;
  - perte imputée à E^Bk : ligne « créances passées en perte », L et E^Bk baissent.

  L'accélérateur compatible avec C28 est la variante V4 (§ 3.V). La contrainte D_F ≥ 0, inactive au socle (fiche 6), garantit que la ligne 9 est payée.
- (d) **Monnaie endogène** : le crédit crée les dépôts (ligne 18, porte de M, signe +). L'offre ne dépend pas des réserves : ni multiplicateur, ni réserves obligatoires. C'est conforme au résumé de McLeay et al. (2014).

**N-3. Placement des titres publics** (critère 6).
- (a) **C19** : 19a-banque = (1 − ς_{B,t})·(besoin − 19a-BC), reliquat de l'équation d'émission (l. 499-500), jamais un solde du bilan bancaire.
  - En cas de rachat, la banque revend ; B_Bk ≥ 0 est une contrainte de conservation, inactive.
  - La part ς_{B,t} non souscrite laisse M^G sous M^G\* : c'est le placement raté du cadre (l. 502), et le rationnement frappe le tour suivant.
- (c) **C22** : aucune limite de détention au socle. La banque absorbe tout le reliquat, et c'est déclaré.
  - Un plafond de type v1.5 ou v2.0 serait actif à l'état stationnaire à π̄ = 10 % (3.A-3, 3.B-3).
  - Le risque de renouvellement relève du J6.
- (d) 19b-banque : la banque est contrepartie passive, au pair.
- (e) **C25** : la règle est compatible avec l'ordre « besoin de l'État, puis banque centrale, puis reliquat de la banque », sous A8 comme sous la variante.

**N-4. Règle de caisse** (critère 1 (d)).

| La banque… | Lignes | Moyen de paiement | Phase |
|---|---|---|---|
| paie | 19a-banque | réserves | 7 |
| paie | 13 | réserves | 8 (a) |
| reçoit | 11b | réserves | 6 |
| reçoit | 12 | réserves | 8 (a) |
| paie par création de dépôts | 10, 15 | dépôts | 6 |
| reçoit par débit de dépôts | 9 | dépôts des entreprises | 6 |

- Ordre de priorité déclaré : 10 et 15 (création de dépôts), puis les paiements en réserves, dans l'ordre des phases.
- **Aucune part ne peut rester impayée** : le découvert intra-pas est admis (l. 485), et le refinancement de 8 (c) est sans plafond ni collatéral au socle (déclaration commune avec la fiche 8). Aucune ligne de part non payée n'est donc nécessaire pour la banque.

**N-5. Leviers** (Q7). Aucun au socle. Les leviers prudentiels (ϑ réglementaire, réserves obligatoires) sont renvoyés au J6, avec les pertes qu'ils gouvernent (#57).

### 3.C Option C — corridor explicite à position nette, écarts constants, fonds propres ancrés (nouvelle)

1. **Source.**
   - Le cadre lui-même : l. 450, 481-489 et 491-502.
   - Corridor : Whitesell, FEDS 2006-22, p. 4. La facilité de prêt fait le plafond, celle de dépôt le plancher ; sans exigence de réserves, la demande de réserves est nulle au taux cible. L'article du *JME* (2006) n'a pas été lu.
   - Crédit servi à la demande et cible de fonds propres sur les crédits : Godley et Lavoie (2007), GROWTH, équations 11.88 et 11.99 (`gl8-growth.Rmd` l. 185 et 204). L'ajustement est ici complet, sans la vitesse β_b de 11.100.
   - Dividende résiduel : FD_b = F_b − FU_b (11.103, l. 209).
2. **Équations.**
   - (C1), choix de conception :

     i_{L,t+1} = i_{CB,t} + ϖ_L, i_{D,t+1} = i_{CB,t} − ϖ_D.

     Écrites en 8 (c), lues à l'ouverture du tour t + 1 (C27).
   - (C2), dérivée de la définition de E^Bk (l. 255) :

     n_a·Π^Bk_t = i_{L,t} L_t + i_{B,t} B_{Bk,t} + i_{res,t} Res_t − i_{D,t}(D_{H,t} + D_{F,t}) − i_{CB,t} L^CB_t.

     Tous les termes reposent sur l'ouverture et la phase 1. Le résultat est calculé en phase 6, comme Π^CB l'est en phase 1 (l. 495).
   - (C3), choix de conception ; le plancher est une contrainte de domaine :

     Div_{Bk,t} = max{0 ; E^Bk_t + Π^Bk_t − ϑ·L_{t+1}}, avec L_{t+1} = L_t + ligne 18 exécutée.

   - (C4), choix de conception sans paramètre. N_t = Res_t^{(8b)} − L^CB_t est la position nette après 8 (b).

     L^CB_{t+1} = max(−N_t; 0), d'où ligne 21 = L^CB_{t+1} − L^CB_t et Res_{t+1} = max(N_t; 0).

   - Paramètres : ϖ_L et ϖ_D (par an, taux de flux) ; ϑ (fraction).
   - Conditions de domaine : ϑ > 0 et la condition d'existence de 3.C-3.
3. **État stationnaire impliqué** (formes fermées ; valeurs au § 3.E).
   - i_L − i_CB = ϖ_L et i_CB − i_D = ϖ_D, pour tout π̄ et tout n_a.
   - E^Bk/L = ϑ exactement.
   - **À chaque clôture**, hors placement raté :
     - L^CB = max(M^G\* + E^CB − B_CB; 0) et Res = max(B_CB − M^G\* − E^CB; 0) ;
     - en effet Res − L^CB = B_CB − M^G − E^CB (bilan de la banque centrale), M^G = M^G\* après la phase 8 (b) (position α), et E^CB est constant (M22 (d)).
     - Sans titres à la banque centrale : H = 0 et L^CB = M^G\*.
   - Bilan de la banque :
     - B_Bk = V_H + D_F − L + ϑL + E^CB + M^G\* − B_CB ;
     - M = D_H + D_F = V_H + D_F.
   - Résultat :
     - sous i_B = i_res = i_CB, n_a·Π^Bk = i_CB·E + ϖ_L·L + ϖ_D·D, soit un rendement des fonds propres ROE = i_CB + (ϖ_L + ϖ_D·D/L)/ϑ ;
     - Div/Π = 1 − n_a(Γ̄ − 1)/ROE.
   - **Condition d'existence** (dividende positif) : ϑ·i_CB + ϖ_L + ϖ_D·D/L > ϑ·n_a(Γ̄ − 1).
     - Avec des écarts nuls, elle échoue dès que r̄ < g : marge −0,000947 à 2 %.
     - Avec les écarts du § 3.0, elle tient avec une marge de +0,0330.
   - Aucune vitesse n'entre dans ces formes. La dépendance à n_a passe par Γ̄ seul : Div/Π = 0,892301 / 0,892616 / 0,892737 pour n_a = 4 / 12 / 52.
4. **Comportement mesuré.** Non mesuré sur un moteur. Maquettes (§ 3.0) :
   - le cas à la main (§ 3.K) boucle en fractions exactes ;
   - scénario « i_CB au plancher (0) pendant 12 tours » (`f7_plancher.py`, stocks sur leur sentier) :
     - écarts de 2 % et 1 % : Div ≥ 0 jamais active ;
     - écarts bas (rendement de 10 %) : active aux tours 1 à 3 seulement, puis E/L revient à 0,100000 sans réactivation.
5. **Coût.** Une trentaine d'opérations par pas : cinq produits pour Π, trois pour Div, quatre pour les lignes 9 et 10, deux comparaisons pour la ligne 21, deux additions pour les taux. Aucune itération. Conforme, très au-dessous de 0,48 ms.
6. **Défauts et instabilités.**
   - Aucune instabilité connue réintroduite :
     - n° 16 : aucun solde résiduel ;
     - n° 15 : aucun plafond ni limite ;
     - n° 4 : aucun taux naturel estimé.
   - Défauts déclarés :
     - (i) transmission complète en un tour, plus rapide que les mesures de de Bondt (2002) ;
     - (ii) écart des dépôts constant, sans canal des dépôts (Drechsler et al., 2017) ;
     - (iii) i_D devient négatif si i_CB < ϖ_D (lecture (d)) ;
     - (iv) Div_Bk lit en phase 6 les lignes 12 et 13 calculées sur l'ouverture et la phase 1. Une part impayée de la ligne 9 (J6) rendrait Π^Bk surestimé ; Div devrait alors lire les montants exécutés ;
     - (v) sans coûts d'exploitation, des écarts de 2 % et 1 % donnent un rendement des fonds propres de 37 %. La calibration au J3 doit le traiter (critère 17).
7. **Identités de bilan.**
   - Matrice des flux de l'option : 3.K.
   - Aucun poste n'est obtenu par différence :
     - L ne bouge que par la ligne 18 ;
     - B_Bk par 19a-banque et 19b-banque ;
     - D par la ligne 17 ;
     - Res par la ligne 20 ;
     - L^CB par la ligne 21.
   - E^Bk est calculé deux fois.
   - Positions intra-pas : Res < 0 entre les phases 6 et 8 (c), résorbé par la ligne 21. Res_{t+1} ≥ 0 tient par la forme de C4.
   - Res·L^CB = 0 à la clôture.
   - Les signatures de `tab:portes-monnaie` restent inchangées (lecture (b) de M22).
8. **Ce que le joueur percevrait.**
   - Un point de taux directeur décidé au tour n :
     - le résultat de la banque monte dès le tour n, de Δ(B − M^G − E^CB)/n_a ;
     - i_L et i_D bougent d'exactement 1 point au tour n + 1 ;
     - le revenu des ménages monte de 0,43 % par tour en équilibre partiel (§ 3.L).
   - Indicateurs proposés, sur deux niveaux :
     - **tableau du tour** : i_L et i_D, ouverture, % par an, une décimale, avec leurs écarts au taux directeur ; crédit nouveau et demande non satisfaite, u.m. et % de la demande du tour ; masse monétaire, clôture rapportée aux 12 derniers PIB, facteur 1,0216 publié ;
     - **fiche détaillée** : Π^Bk et Div_Bk sur 12 tours, et rendement des fonds propres d'ouverture ; E^Bk/L à la clôture ; Res, L^CB et B_Bk en % du PIB annuel ; rendement réel des dépôts i_D − π (l. 214).
   - Aucun levier propre. Ces éléments sont à soumettre à `jeu`.
9. **Empreinte sur l'état.**
   - Deux variables d'état du bloc : i_L et i_D, par an, de valeurs stationnaires i_CB + ϖ_L et i_CB − ϖ_D.
   - Aucun historique, aucun tirage. Les entrées de scénario ς sont des données du scénario.
   - Variante : une seule variable, i_{CB,t−1} ; non retenue, parce que l'ADR 0009 nomme i_L et i_D.

### 3.D Option D — banque de Godley et Lavoie (BMW, INSOUT, GROWTH), nouvelle

1. **Source.** Godley et Lavoie (2007), lus par reproduction ; livre non lu.
   - BMW (chap. 7) : `gl5-bmw.Rmd` l. 47, 60-61, 79, 164-165.
   - INSOUT (chap. 10) : `gl7-insout.Rmd` l. 69, 171-191, 332-335, 349-376, 508-532.
   - GROWTH (chap. 11) : `gl8-growth.Rmd` l. 185-217, avec les équations 11.88 à 11.108, et l. 229, 268-271.
2. **Équations.**
   - **BMW** : L^s = L^d ; M^s = M^s_{−1} + ΔL^s ; r_m = r_l. Ni écart, ni résultat, ni fonds propres.
   - **INSOUT** :
     - réserves : H_b = ρ_1 M1 + ρ_2 M2 (l. 349) ;
     - titres, solde du bilan : B_b = A + M − L − H_b (l. 358) ;
     - avances : A = (bot·M − B_b^N)·1{BLR^N < bot} (l. 356-357) ;
     - taux des dépôts : r_m = r_{m,−1} + ζ_m(1{BLR < bot} − 1{BLR > top}) + ζ_b Δr_b (l. 364-366) ;
     - taux du crédit : r_l = r_{l,−1} + ζ_l(1{BPM < botpm} − 1{BPM > toppm}) + Δr_b (l. 368-370) ;
     - titres de la banque centrale, solde : B_cb = B_s − B_h − B_b (l. 332) ;
     - résultat entièrement distribué (l. 69).
   - **GROWTH** :
     - crédit servi à la demande (11.88) ;
     - réserves obligatoires (11.90) ;
     - titres, solde du bilan (11.92) ;
     - taux des dépôts à indicatrices (11.94-11.97) ;
     - r_l = r_m + ADDL (11.98), ADDL visant un résultat-cible (11.104, 11.106) ;
     - fonds propres visés OF^T = NCAR·L_{−1} (11.99), atteints par ajustement partiel β_b (11.100) ;
     - FD_b = F_b − FU_b (11.103), avec FU_b = F_b − λ_b Y_{−1} (11.107).
3. **État stationnaire impliqué.**
   - BMW transposé, avec ϑ = ϖ = 0 :
     - le dividende n'est jamais positif à l'état stationnaire quand r̄ < g ;
     - à la première baisse de taux, Π_n = Δ(D − L)/n_a < 0 dès que D > L, d'où E^Bk < 0 : insolvabilité au socle.
   - INSOUT et GROWTH :
     - tout ratio BLR compris entre bot et top est stationnaire : **continuum** ;
     - OF/L = β_b·NCAR/(γ + β_b), dérivé à la main : la vitesse fixe l'arrivée ;
     - ADDL dépend de λ_b·Y/L et de Γ̄ : écart non superneutre.
4. **Comportement mesuré.** Non mesuré en v3. La reproduction rapporte un « ping-pong » du ratio de liquidité quand les bandes sont serrées (l. 508-532 ; source tierce, non exécutée).
5. **Coût.** Une vingtaine d'opérations. Conforme.
6. **Défauts et instabilités.**
   - Au moins six indicatrices à seuil libre : bot, top, botpm, toppm, et les bandes de ±0,05 de GROWTH. Le ping-pong est l'analogue de l'instabilité 15.
   - Continuum d'équilibres (critère 9).
   - Réserves obligatoires (Q7 écartée).
   - Titres de la banque (11.92) et de la banque centrale (l. 332) obtenus par différence : contraire au critère 1 (b) et à C25, puisque la banque centrale y est l'acheteur résiduel.
   - Apports retenus dans C : crédit à la demande, cible de fonds propres sur les crédits, dividende résiduel.
7. **Identités de bilan.** Cohérentes dans leurs propres matrices, mais B_b et B_cb sont des soldes.
8. **Ce que le joueur percevrait.** Un taux des dépôts qui saute par crans quand un ratio invisible sort de sa bande. C'est opaque.
9. **Empreinte sur l'état.** r_m, r_l, OF^e, deux retards de BPM et NPL^e.

### 3.V Variantes à une question, combinables avec C

- **V1 — Ajustement partiel des taux** (Q1).
  - Forme : i_{X,t+1} = i_{X,t} + (λ_X/n_a)(i_{CB,t} ± ϖ_X − i_{X,t}), avec λ_X ∈ ]0; n_a]. λ_X = n_a redonne C.
  - Le point fixe ne dépend pas de λ (critère 9 tenu). La racine propre vaut 1 − λ/n_a.
  - Le seuil (d1) de `jeu` tient si et seulement si λ/n_a ≥ 0,5.
  - Plus fidèle à de Bondt (2002), mais ajoute deux paramètres pour un retard de quelques tours. Lecture (c).
- **V2 — Encaisse de réserves visée** (Q2).
  - Forme : Res_{t+1} = max(N_t; ρ_R·D_{t+1}), et L^CB_{t+1} = Res_{t+1} − N_t.
  - Conséquences :
    - Res·L^CB > 0 ;
    - coût (i_CB − i_res)ρ_R D pour la banque ;
    - H/(12 PIB) = ρ_R × 0,866 ;
    - l'absence d'arbitrage exige i_res ≤ i_CB, forme (ii), transmise à la fiche 8.
  - Aucun mécanisme du socle déterministe ne motive une demande de réserves positive (Whitesell, FEDS 2006-22, p. 4). Écartée par simplicité.
  - Un remboursement partiel de L^CB à vitesse donnée ferait un intégrateur dont la vitesse fixerait l'arrivée : écarté, critères 2 (a) et 9.
- **V3 — Taux de distribution fixe d** (Q3).
  - Forme : E/L = (ϖ_L + ϖ_D D/L)/(n_a(Γ̄ − 1)/(1 − d) − i_CB).
  - Valeurs : 0,164 / 0,093 / 0,044 à π̄ = 0 / 2 % / 10 % pour d = 0,9 ; 1,04 / 0,69 / 0,38 pour d = 0,5.
  - C'est une ancre, mais elle dépend fortement de π̄ et des écarts, et elle n'existe que sous une condition. La valeur ϑ = 0 de C correspond au cas BMW.
- **V4 — Écart sur l'insuffisance de fonds propres** (accélérateur bancaire).
  - Forme : ϖ_{L,t} = ϖ_L + φ_E·max(ϑ − E_t/L_t; 0). Compatible avec C28, puisqu'il lit l'état de la banque.
  - Inerte au socle : E = ϑL, sauf trois tours au plus dans le scénario de plancher.
  - Transmise au J6 avec #57.
- **R — Sans retard.** i_{L,t} = i_{CB,t} + ϖ_L, lu dans le tour.
  - Aucune variable d'état. Au tour n, ΔΠ^Bk = ΔE/n_a seulement.
  - Contredit C27, la lecture (b) de M28, les motifs de M30 et P2 (critère 15 de la fiche 8 : I^vol bougerait au tour 1).
  - Gardée comme référence seulement.

### 3.K Cas à la main (critères 1, 2, 6 et 7), option C, un pas

Le calcul est fait par `f7_cas.py`, en fractions exactes.
- Ouverture : L = 600, B_Bk = 290, Res = 0, L^CB = 20, D_H = 700, D_F = 110, d'où E = 60 ; M^G = M^G\* = 20 ; B_CB = 0.
- Taux : i_CB passe de 3 % à 4 % au tour même ; i_L = 5 % et i_D = 2 % sont lus à l'ouverture ; i_B = i_res = 4 % ; ϑ = 0,1.
- Flux : crédit demandé de 10 ; G = 30 ; impôts de 28 (20 sur les ménages, 8 sur les entreprises).

| Ligne | Phase | Banque | Montant |
|---|---|---|---|
| 18 | 3 | −ΔL | 10 |
| 9 | 6 | + | 2,5 |
| 10 | 6 | − | 1,35 (ménages 1,16667 ; entreprises 0,18333) |
| 11b | 6 | + | 0,96667 |
| 15 | 6 | − | 1,05, car Π^Bk = 2,05 et 60 + 2,05 − 0,1 × 610 = 1,05 |
| 19a-banque | 7 | − | 2,9 = 30 + 0,96667 − 28 − Π^CB (0,06667) + 0 |
| 12 ; 13 | 8 (a) | + ; − | 0 ; 0,06667 |
| 21 | 8 (c) | + | 0, car la position après 8 (b) vaut 0 |

- Clôture : L = 610, B_Bk = 292,9, Res = 0, L^CB = 20, D_H = 682,21667, D_F = 139,68333.
- **E^Bk vaut 61 par le stock comme par les flux** (60 + 2,05 − 1,05), et E/L = 0,100000.
- La contrainte budgétaire ΔL + ΔB_Bk + ΔRes − (ΔD + ΔL^CB) − (Π − Div) vaut **0 exactement**. E^CB = 0 et Res·L^CB = 0.
- **Position négative** : si M^G\* passe à 20,5, alors 19a-banque = 3,4, Res après 8 (b) = −0,5, ligne 21 = +0,5, et L^CB = 20,5 = M^G\*.
- **Position positive**, cumulée avec la position négative (M^G\* = 20,5) : si la banque centrale achète en outre 25 de titres à la banque (19b-banque), la position après 8 (b) vaut +24,5 et la position nette +4,5. La ligne 21 vaut −20 : L^CB = 0 et Res = 4,5 = B_CB − M^G\*. Sur le cas de base seul (M^G\* = 20), la position nette vaut +5 et Res = 5. Le refinancement est remboursé avant toute détention de réserves : **#26, point 5, clos sous la forme (i)**. *(Précision du 04/10/2026, validation de la spécification.)*
- **Refus de moitié** (ς_L = 0,5) : ligne 18 = 5, Div = 1,55, E = 60,5 = 0,1 × 605 ; la contrainte budgétaire vaut 0.
- **C29 sur ce cas** : ΔΠ^Bk = 0,01 × (B_Bk + Res − L^CB)/12 = 0,225 = 0,01 × (D + E − L)/12.

### 3.E État stationnaire de l'option C (critère 8)

Maquette `f7_stat.py`, hypothèses du § 3.0, n_a = 12. Les ratios sont des stocks d'ouverture rapportés à 12 fois le PIB du pas ; Π est annuel, rapporté au PIB annuel.

| Grandeur | π̄ = 0 | 2 % | 10 % |
|---|---|---|---|
| i_CB ; i_L ; i_D | 1,00 ; 3,00 ; 0,00 % | 3,02 ; 5,02 ; 2,02 % | 11,10 ; 13,10 ; 10,10 % |
| L | 0,80037 | 0,62204 | 0,33439 |
| M = D_H + D_F | 0,86636 | 0,86605 | 0,86492 |
| E^Bk (= ϑL) | 0,08004 | 0,06220 | 0,03344 |
| B_Bk (= B, sans titres à la banque centrale) | 0,16686 | 0,32705 | 0,58480 |
| L^CB ; Res | 0,02083 ; 0 | 0,02083 ; 0 | 0,02083 ; 0 |
| B − M^G − E^CB | 0,14603 | 0,30622 | 0,56397 |
| Π^Bk ; rendement des fonds propres | 0,02547 ; 31,82 % | 0,02298 ; 36,94 % | 0,01905 ; 56,97 % |
| Div/Π | 0,93772 | 0,89262 | 0,79695 |
| B_Bk / actif de la banque | 0,1725 | 0,3446 | 0,6362 |
| Rendement réel des dépôts i_D − π̄ | 0,00 % | +0,02 % | +0,10 % |
| Impôt d'inflation net des déposants / YD : [n_a((1 + π̄)^{1/n_a} − 1) − i_D]·V_H/(n_a YD) | 0 | −0,037 % | −0,485 % |

- **C30** : entre 2 % et 10 %, B/PIB monte de +0,2578, soit +0,2865 venant des entreprises et −0,0288 venant des fonds propres de la banque (ϑΔL). Côté ménages, rien ne change à YD^HS/PIB donné. Le total est publié par la fiche 9.
- **État initial résolu** :
  - i_{L,0} = i_CB,0 + ϖ_L ; i_{D,0} = i_CB,0 − ϖ_D ;
  - E^Bk_0 = ϑL_0 ;
  - L^CB_0 et Res_0 donnés par les formes de 3.C-3 ;
  - B_{Bk,0} = B_0 − B_CB,0 ;
  - B_0 est tiré de l'identité de la fiche 9.
- **#44** : sous l'écart additif et un i_CB de Fisher, ϱ̄_L = r̄ + ϖ_L/(1 + π\*), soit 3,000 / 2,961 / 2,818 % à r̄ = 1 % (lecture (b)).

### 3.L Exemple daté et lisibilité (critère 13)

i_CB est relevé d'un point aux tours 1 à 12. Équilibre partiel : stocks sur leur sentier, π̄ = 2 %, option C, `f7_dyn.py`.

| Tour | i_L, i_D | Π^Bk (écart à Π) | Div_Bk | ROE annualisé | YD des ménages |
|---|---|---|---|---|---|
| 1 | 0 | +13,33 % | +14,94 % | +4,92 points | +0,429 % |
| 2, 3, 12 | +1,0 point | +2,71 % | +3,04 % | +1,00 point | +0,429 % |
| 13 | +1,0 point | −10,62 % | −11,90 % | −3,92 points | 0 |
| 24 | 0 | 0 | 0 | 0 | 0 |

- (d1) i_L et i_D bougent de 1,0 point, soit dix crans, au tour n + 1 : le seuil est tenu.
- (d2) Le rendement des fonds propres sur 12 tours monte de +1,33 point ; l'écart du tour 12 vaut +1,00 point.
- (d3) Décomposition de ΔYD, partie par partie :
  - au tour 1, Div_Bk porte 100 % de l'écart ;
  - aux tours 2, 3 et 12 : ligne 10 +229 % ; Div_Bk +20 % ; dividendes des entreprises (règle F, fiche 6) −149 %.
- Au total, ΔYD = Δ·(B − M^G − E^CB)/n_a dès le tour n : c'est le canal rentier, égal à la dette publique consolidée.
- Sous l'option (iii) de i_B (i_CB d'ouverture), le saut du tour n devient −Δ·L^CB/n_a, soit −0,9 % de Π.
- Délais :
  - taux du tour n → lignes 12 et 13 au tour n → Π^Bk et Div_Bk au tour n ;
  - i_L et i_D au tour n + 1 → plans au tour n + 1 → consommation au tour n + 2 (C35).
- Contreparties visibles :
  - un achat 19b-banque fait baisser B_Bk et L^CB, puis fait monter Res seulement au-delà de M^G\* + E^CB − B_CB. M ne change pas, ni Π^Bk si i_B = i_res = i_CB ;
  - une dépense publique fait monter B_Bk (19a-banque) et D_F ; Res et L^CB restent inchangés à la clôture tant que M^G\* ne bouge pas.
- Perceptibilité (e) :
  - (i) deux crans dans les 12 tours, tenu ;
  - (ii) pic au tour 2 ;
  - (iii) le bloc n'a aucune dynamique lente.

## 4. Tableau comparatif

| Critère | A (v1.5) | B (v2.0) | C (nouvelle) | D (Godley-Lavoie) | R (sans retard) |
|---|---|---|---|---|---|
| 1 (a) Lignes | lignes nouvelles (actions, recapitalisation, pertes), contrats partagés (3.A-7) | idem, plus des capitalisations (3.B-7) | 9, 10, 15, 21 ; 19a selon M33 ; aucune ligne nouvelle (3.N-1) | 9, 10, 15 ; titres résiduels (3.D-7) | comme C |
| 1 (b) Aucun solde résiduel | **écart** : Res indéterminé (3.A-6) | **échec** : l. 1280 (3.B-6) | conforme (3.K) | **écart** : B_b obtenu par différence (3.D-6) | conforme |
| 1 (c) Contrainte budgétaire | **écart** : i^res Res sans receveur (3.A-6 (i)) | écart : contrôle circulaire (3.B-7) | exacte, 0 (3.K) | conforme dans G&L | conforme |
| 1 (d) Règle de caisse | écart (l. 1522) | écart (l. 1012-1017, 1180) | conforme, aucune part impayée possible (3.N-4) | sans objet | conforme |
| 2 (a) Ligne 21, ancres | absente | cliquet sans ancre | position nette, formes fermées (3.C-3) | seuil (avances) | comme C |
| 2 (b) Découvert sans intérêt | non écrit | sans objet | déclaré (3.C-7) | sans objet | comme C |
| 2 (c) Arbitrage (#26, point 5) | forme (ii) par Δ ≥ 0, sans règle | Res·L_cb > 0 possible | **forme (i), clos** (3.K) | conditionnel | comme C |
| 2 (d) Corridor | — | — | instruit ; FEDS 2006-22 lu, *JME* non lu (3.0) | — | — |
| 3 (a) Phase de i_L, i_D | immédiate : écart C27 | immédiate : écart | 8 (c), interprétation (3.N-1) | retard d'une période | **viole C27** (3.V) |
| 3 (b) Phase 3 | Λ^Bk lit la demande : rouvre M28 | `credit_room` : rouvre M28 | conforme | conforme | conforme |
| 3 (c) Phase 6 | — | hebdomadaire | conforme (3.C-2) | conforme | conforme |
| 3 (d) Phase 7 | limite de 40 % | ménages, puis banque | compatible, A8 recommandé (3.N-3) | banque centrale résiduelle : écart C25 | comme C |
| 3 (e) Phase 8 (c) | non | solde de fin de pas | conforme | — | comme C |
| 3 (f) Triangularité | non vérifiable | — | conforme (3.N-1) | conforme | conforme |
| 4 (a) Transmission | immédiate | immédiate | complète au tour n + 1 (3.C-2) | indirecte, par bandes | au tour n |
| 4 (b) Plancher | (·)^+ à seuil libre, à sa limite à π̄ = 0 (3.A-3) | max(·; 0) et coupure si E ≤ 0 | aucun ; i_D < 0 si i_CB < ϖ_D (lecture (d)) | aucun | comme C |
| 4 (c) C28 et superneutralité | **échec** (prime ℓ, NPL) | **échec** (rho1) | conforme, écarts exacts (3.E) | **échec** (ADDL) | conforme |
| 4 (d) Mesures | — | — | C29 : +13,3 % puis +2,7 % ; i_D − π̄ = 0 / 0,02 / 0,10 % ; impôt d'inflation net de 0 à −0,49 % (3.E, 3.L) | — | ΔΠ_n = ΔE/n_a |
| 5 (a) Ancre de E | dépend de ϖ^Bk | **0,133 / 0,126 / 0,121** (3.B-3) | ϑ exact | β_b·NCAR/(γ + β_b) | comme C |
| 5 (b) Date de Div | la semaine même | idem | même tour ; écart de calendrier chiffré (lecture (e)) | même période | comme C |
| 5 (c) Div ≥ 0 | (E − Ē)^+ | max(0; ·) | domaine ; Div/Π = 0,893 ; actif aux tours 1 à 3 du plancher sous écarts bas (3.C-4) | BMW : E < 0 à la première baisse | comme C |
| 5 (d) Hors socle | dans le socle : **écart** | dans le socle : **écart** | renvoyé au J6 | NPL au J6 | comme C |
| 6 (a) Reliquat | jusqu'à la limite | jusqu'à la limite | conforme (3.N-3) | **écart** (solde) | comme C |
| 6 (b) B_Bk/PIB | identité, tant que la limite est inactive | idem | 0,167 / 0,327 / 0,585 (3.E) | — | comme C |
| 6 (c) Limite | 40 % du bilan, **active à 10 %** | 0,4 × D, **active à 10 %**, marge de 0,022 à 2 % | aucune, déclarée ; dispositif ς_B | aucune | comme C |
| 6 (d) 19b-banque | — | — | passive, au pair | — | comme C |
| 6 (e) C25 | — | ménages en premier | compatible | **écart** | comme C |
| 7 (a) Offre | **plafond** | **plafond**, secteurs par ordre | conforme | conforme (11.88) | conforme |
| 7 (b) C31 | non prévu | non prévu | ς_L (3.N-2) | non prévu | comme C |
| 7 (c) #57 | accélérateur dans le socle | idem | limite déclarée ; V4 au J6 | NPL | comme C |
| 7 (d) Monnaie endogène | ΔL = ΔD, mais plafond | crédit crée le dépôt (l. 904) | déclarée (3.N-2) | ΔM = ΔL (BMW) | comme C |
| 8 (a) Formes fermées | non | non | oui (3.E) | non (continuum) | oui |
| 8 (b) Vitesses et n_a | échec | échec | aucune vitesse ; n_a par Γ̄ seul (3.C-3) | échec | conforme |
| 8 (c) C30 | — | — | déclarée (3.E) | — | comme C |
| 8 (d) Ne fixe ni i_CB ni B/PIB | conforme | conforme | conforme | r_m endogène | conforme |
| 9 Vitesses | **échec** | **échec** | conforme ; V1 conforme | **échec** | conforme |
| 10 (a) Instabilités connues | n° 15, et n° 16 si transposée | n° 15 et 16 (S+O) | aucune | analogue du n° 15 | aucune |
| 10 (b) Boucle propre | stable, arrivée fonction de la vitesse | idem | module 0 (3.C-4) | cycles de bandes | module 0 |
| 10 (c) Écart endogène | inerte sous F | idem | sans objet ; V4 au J6 | ADDL, non mesuré | sans objet |
| 10 (d) Boucle avec la règle de taux | fiche 8 | fiche 8 | fiche 8 | fiche 8 | fiche 8 |
| 11 Test zéro | non passable | instable (n° 16) | préalable tenu (3.E) | bandes | préalable tenu |
| 12 Bornes à seuil libre | environ 11 | environ 13, plus 7 drapeaux | **0** ; 4 contraintes sans paramètre (3.C-9) | 6 ou plus | 0 |
| 13 (a) Indicateurs | κ^CAR | aucun | deux niveaux (3.C-8) | opaques | comme C |
| 13 (b) Délais | immédiats | immédiats | tours entiers (3.L) | une période | tour n, contredit C35 |
| 13 (c) Tableau des leviers | 2 leviers | aucun | aucun levier propre (3.L) | réserves obligatoires | comme C |
| 13 (d) Ampleur | — | — | d1 tenu ; d2 +1,33 point ; d3 publié (3.L) | — | d1 dès le tour n |
| 13 (e) Perceptibilité | — | — | tenue (3.L) | — | tenue |
| 14 Paramètres / bornes / état | environ 16 / 11 / 3 | environ 18 / 13 / 5, 7 drapeaux | 3 et 2 entrées / 0 / 2 | environ 11 / 6 / 5 | 2 / 0 / 0 |
| 15 Coût | conforme | conforme | conforme, environ 30 opérations | conforme | conforme |
| 16 Notation | collisions m, κ, ϱ, ℓ, Λ | idem | aucune collision (grep, 3.0) | r, ρ, β, λ pris | comme C |
| 17 Calibration | R (l. 2263-2264) | défauts, non D1 | sources du § 3.0 ; ROE et distribution non trouvés | — | — |
| 18 Faits | R | L, S+O, S | — | source tierce | — |

## 5. Avis de l'expert pilote

*`monnaie`, 04/10/2026.*

**Recommandation : l'option C**, avec le socle commun du § 3.N :
- écarts constants au taux directeur, écrits en 8 (c) et lus au tour suivant ;
- refinancement sur la position nette, Res·L^CB = 0, sans paramètre ;
- fonds propres ancrés à ϑ·L par un dividende résiduel versé le tour même ;
- crédit à la demande, sans plafond, avec le dispositif de scénario ς_L ;
- reliquat de l'émission sans limite, avec le dispositif ς_B, sous la forme A8 ;
- aucun levier au socle.

**Motifs, critère par critère.**
- Elle est la seule option sans solde résiduel, avec une contrainte budgétaire exacte et aucune part impayée possible (critère 1).
- Res et L^CB ont des formes fermées à chaque clôture, fixées par le bilan de la banque centrale, ce qui clôt #26, point 5, sous la forme (i) (critère 2).
- Les phases relèvent d'une interprétation, sans ordre nouveau (critère 3).
- Les écarts sont exacts et superneutres (critère 4).
- L'ancre ϑ est exacte et indépendante des vitesses (critères 5 et 9).
- Le reliquat est souscrit sans limite ; une limite serait active à l'état stationnaire à 10 % (critère 6).
- L'offre suit C27 (critère 7).
- Aucune instabilité connue n'est réintroduite et aucune borne à seuil libre n'est ajoutée (critères 10 et 12).
- Les seuils d1 et e de `jeu` sont tenus (critère 13).
- C'est l'option la plus simple : 3 paramètres et 2 variables d'état (critère 14).

**Options écartées.**
- A et B : critères 1 (b), 2 (a), 4 (c), 5 (a), 6 (c), 7 (a), 9 et 12.
- D : critères 4 (c), 5 (a), 9 et 12. On en garde le crédit à la demande, la cible de fonds propres sur les crédits et le dividende résiduel.
- V2 et V3 : simplicité, et dépendance à π̄ pour V3.
- R : référence seulement.
- V4 : transmise au J6.

**Lectures soumises au mainteneur.** Pour chacune, je donne mon avis ; le mainteneur tranche.
- **(a) l. 450 face à la l. 489.** La l. 450 dit : « aucune règle ne corrige un solde de réserves négatif en l'ajoutant au refinancement ».
  - (i) Elle interdit le calcul de Res par différence suivi du report de sa partie négative (v2.0). Une ligne 21 décidée sur la position tenue au grand livre lui est conforme.
  - (ii) Elle interdit toute règle ΔL^CB ≥ −Res^{(8b)}. Mais alors elle contredit la l. 489 (« couvre au moins la position négative »).
  - Avis : (i). `docwriter` précise la l. 450 dans `sec:banque`.
- **(b) Forme de l'écart.**
  - (i) Additif : critère 4 (c) au pied de la lettre. Le taux réel du crédit ϱ̄_L dépend alors de π\*, à 3,000 / 2,961 / 2,818 %. Cet écart de 0,18 point entre 0 et 10 % est une norme, pas une allocation.
  - (ii) Multiplicatif de Fisher : écart réel invariant, mais il échoue au critère 4 (c) tel qu'écrit.
  - Avis : (i), avec la dépendance déclarée et transmise à la fiche 8 (critère 13 (b)).
- **(c) Vitesse de transmission.**
  - (i) Complète en un tour.
  - (ii) Partielle, variante V1 : un paramètre λ, pas un drapeau. Le seuil d1 n'est tenu que si λ/n_a ≥ 0,5.
  - Avis : (i) au socle.
- **(d) Plancher de i_D.**
  - (i) Aucun : i_D vaut −1 % pendant le scénario de plancher sous des écarts de 2 % et 1 %, −0,214 % sous les écarts bas.
  - (ii) Plancher à 0 : borne à seuil libre, active dans ce scénario.
  - Avis : (i).
- **(e) Date de Div_Bk.**
  - (i) Le tour même : ΔYD = Δ(B − M^G − E^CB)/n_a dès le tour n, soit 2,55e−4 en unités de 12 × PIB par pas.
  - (ii) Le tour suivant : 0 au tour n, puis 4,59e−4 au tour n + 1.
  - Avis : (i), qui tient la règle de caisse et les variables d'état sans retard supplémentaire.
- **(f) Propriétaire des lignes 19a (M33).** Avis : A8, sur le modèle de la lecture (a) de M28 : le prêteur publie ses conditions, l'emprunteur propose la ligne.
- **(g) Référence de l'écart quand la banque est en position longue.** Avec un corridor non nul et des réserves positives, le coût marginal de la banque devient i_res.
  - Avis : référence i_CB, avec un corridor de largeur nulle au socle, à transmettre à la fiche 8.
  - Sinon, l'écart lirait le taux marginal sur la position d'ouverture : une bascule, à éviter.
- **(h) Variables d'état.** i_L et i_D (deux), conformes à l'ADR 0009, ou i_{CB,t−1} (une). Avis : i_L et i_D.

**Réserves, avec leurs critères écrits avant l'essai** (J3, sauf mention) :
1. Un pas sans choc depuis l'état résolu laisse à leurs formes fermées du § 3.E, à 1e−10 près en relatif, pour π̄ = π\* ∈ {0 ; 2 % ; 10 %} et n_a ∈ {4 ; 12 ; 52} :
   - i_L − i_CB = ϖ_L et i_CB − i_D = ϖ_D ;
   - E^Bk/L = ϑ ;
   - Res·L^CB = 0 ;
   - L^CB et Res.
2. Le cas du § 3.K est reproduit par appel direct, à 1e−12 × S^Bk près, dans ses quatre variantes : base, position négative, position positive, refus de moitié.
3. C29, par appel direct en équilibre partiel : ΔΠ^Bk au tour n vaut Δ·(B − M^G − E^CB)/n_a, et ΔE/n_a ensuite, à 1e−12 près en relatif.
4. Dans les scénarios « i_CB au plancher pendant 12 tours », « +5 points pendant 12 tours » et « refus de moitié pendant 12 tours », la contrainte Div_Bk ≥ 0 est inactive, ou désactivée au plus tard 12 tours après la fin du choc, sans réactivation.
5. Res_{t+1} ≥ 0 tient à chaque pas.
6. Test zéro : bandes du critère 11 ; nullité de Res à 1e−12 × S^Bk près sans titres à la banque centrale.
7. Coût du bloc d'au plus 0,48 ms par pays-pas.
8. Calibration de ϖ_L, ϖ_D et ϑ sur des sources lues (critère 17). Des écarts de 2 % et 1 % donnent un rendement des fonds propres de 37 %, faute de coûts d'exploitation au socle.

**Ce que l'option coûte en fidélité.**
- Une transmission plus rapide que celle mesurée par de Bondt (2002).
- Aucun canal des dépôts (Drechsler et al., 2017) : un écart des dépôts qui varierait avec le taux violerait le critère 4 (c).
- Aucune demande de réserves (Whitesell, FEDS 2006-22, p. 5 : elle est positive en pratique).
- Aucun cycle du capital bancaire au socle (J6).

**Conditions transmises.**
- À la fiche 8 :
  - largeur du corridor nulle au socle, ou lecture (g) ;
  - allocation sans plafond ni collatéral ;
  - i_res ≤ i_CB au titre du signe de Π^CB, et non de l'arbitrage, que C clôt ;
  - L^CB = max(M^G\* + E^CB − B_CB; 0) ;
  - un achat de titres jusqu'à M^G\* + E^CB − B_CB ne fait que réduire L^CB.
- À la fiche 9 :
  - ϑL entre dans l'identité de la dette ;
  - B_Bk/actif vaut 0,17 / 0,34 / 0,64 à 0 / 2 % / 10 % ;
  - dispositif ς_B ;
  - le signe de C29 dépend de la règle de i_B.
- À la fiche 6 : ligne 18 = (1 − ς_L)ΔL^d⁺ + ΔL^d⁻.
- Au J6 : V4 et la ligne de part non payée de #57.

**Questions pour `macro`** (§ 6) :
1. La lecture de F1 sous ς_L, avec la demande non satisfaite publiée par le bloc 6, convient-elle ?
2. Confirmez-vous le bloc 7 comme propriétaire de la ligne 9, F3 recalculant les lignes 9 et 10 sur l'ouverture ?
3. Pour la part non payée de la ligne 9 (#57, J6), préférez-vous la capitalisation nommée ou la perte imputée à E^Bk ?
4. Acceptez-vous que E^Bk = ϑL entre dans l'identité de la dette de la fiche 9, pour +0,080 / +0,062 / +0,033 année de PIB ?
5. La forme ΔYD = Δ·(B − M^G − E^CB)/n_a dès le tour n est-elle cohérente avec b/(1 + ib) de la fiche 5 ?
6. Pour calibrer les écarts sans coûts d'exploitation (rendement des fonds propres à 37 % sous 2 % et 1 %), faut-il caler sur la marge nette d'intérêt ou sur le rendement des fonds propres ?
7. Quel est l'effet de Div_Bk versé le tour même sur θ_H et sur la boucle conjointe ?
8. Les lectures (b) et (e) vous conviennent-elles ?

**Questions pour `jeu`** (§ 7) :
1. Les deux niveaux d'indicateurs du point 3.C-8, rendement des fonds propres compris, vous conviennent-ils ?
2. C29 : le résultat de la banque monte de 13 % au tour de la décision, puis baisse de 11 % au tour du retour. Faut-il le restituer seulement sur 12 tours, avec une infobulle ?
3. Taux des dépôts négatif au plancher (lecture (d)) : l'acceptez-vous, ou préférez-vous un plancher à 0 ?
4. Un achat de titres reste invisible sur Res et sur Π^Bk tant que B_CB < M^G\* : est-ce un problème de lisibilité avant le J6 ?
5. Comment nommer les événements de scénario « refus de crédit » (ς_L) et « placement raté » (ς_B) ?
6. Transmission complète ou partielle (lecture (c)) : quelle préférence, vu la limite du seuil d1 à λ/n_a = 0,5 ?
7. Le revenu des ménages monte de 0,43 % par tour pendant le taux haut puis revient à 0 au tour de retour (§ 3.L) : ce signe et cette ampleur sont-ils explicables au joueur, au regard de #56 ?

## 6. Avis de l'expert consulté

*Rédigé par `macro` (expert consulté pour la frontière crédit, le bouclage stock-flux et l'état stationnaire) le 04/10/2026. Avis porté sur la fiche à l'état `0e3fb17` (branche `claude/j1-monnaie-etat`, PR #77). Les numéros de ligne de `docs/specification/nations_et_marches.tex` sont ceux de cet état. Les conditions nouvelles sont numérotées C38 à C44 (§ 6.5), sous réserve de l'ordre réel d'intégration.*

*Sources lues :*
- *fiche 7 : § 1 à § 5 ;*
- *fiche 6 : § 3.N (F1 à F3), § 3.E, § 3.F, § 6.1, § 6.3 (C27 à C31), § 8 (M28), § 9.1, § 9.2 et § 9.4 ;*
- *fiche 9 : § 1 (identité de la dette, identité de Domar) et § 1.4 ;*
- *fiche 5 : § 6.1, Q1 (l. 1037 à 1044) et Q3 (l. 1121 à 1141) ;*
- *spécification : l. 440 à 450 (`sec:cadre-identites`), l. 479 à 502 (`sec:cadre-caisse`), l. 703 à 705 (ρ̄_K), l. 745 à 765 (`sec:production-stationnaire`), l. 1542 à 1546 (`sec:menages`), l. 1843 à 1867 (`sec:investissement-stationnaire`), l. 1877 et 1895 (`sec:investissement-conditions`) ;*
- *issue #55.*

*Calculs : maquette propre de `macro`, écrite sans reprendre les scripts de `monnaie` et sans importer `archive/`, dans un répertoire créé par `mktemp -d` (commandes et sorties au compte rendu de `macro` du 04/10/2026). Avant toute grandeur nouvelle, elle reproduit les chiffres publiés de la fiche 6 : ρ̄_K, ρ̄_IN, K, L, D_F, V_F, taux de distribution, distribution à x = 3 (−0,07314) et x_max (2,933 et 2,853). Les sorties de maquette sont des résultats de modèle, sans statut de fait.*

### 6.1 Réponses aux huit questions de `monnaie`

**Q1 — F1 sous ς_L. La lecture convient, sans rouvrir M28. Le crédit refusé est en partie redemandé par F1, ce qui est à déclarer.**
1. **F1 est inchangée.** Seule sa clause « ligne 18 » (fiche 6 § 9.1, `eq:investissement-demande-credit`) devient ΔL_t = (1 − ς_{L,t})·max(ΔL^d_t ; 0) + min(ΔL^d_t ; 0), ce qui redonne ΔL^d_t pour ς_L = 0. M28 l'a prévu : l'offre de crédit de la fiche 7 relève de C27 et « le refus partiel reste un scénario déclaré », sans rouvrir M28 (fiche 6 § 9.3). La spécification cite déjà « le dispositif du bloc banque, condition C31 » (l. 1895).
2. **Triangularité.** ς_{L,t} est une entrée de scénario publiée à l'ouverture. Le bloc 6 la lit en phase 3 sans lire de réponse de la banque : le critère 3 (b) est tenu. F3 lit la ligne 18 exécutée : le refus tombe sur Div_F, puis sur D_F, jamais sur l'investissement (§ 3.F de la fiche 6).
3. **Fait de maquette à déclarer.** F1 vise un niveau, L = lv\*·K : le crédit refusé au tour t est redemandé au tour t + 1. Scénario ς_L = 0,5 aux tours 1 à 12 ; chiffres en unités du crédit nouveau de base du tour.

   | Tour | Demande | Accordé | Écart de Div_F |
   |---|---|---|---|
   | 1 | 1,000 | 0,500 | −0,500 |
   | 2 | 1,498 | 0,749 | −0,251 |
   | 3 | 1,747 | 0,873 | −0,127 |
   | 4 | 1,871 | 0,935 | −0,065 |
   | 12 | 1,993 | 0,997 | −0,0035 |
   | 13 | 1,993 | 1,993 | **+0,993** |
   | 14 et suivants | 1 | 1 | 0 |

   - Le manque d'encours plafonne à un tour de crédit nouveau.
   - Sur le cas à la main de la fiche 6 (crédit de base 3,096 ; Div_F 7,827), cela fait −19,8 % de Div_F au tour 1 et +39,3 % au tour 13.
4. **Conséquences.**
   - La « demande non satisfaite » publiée reste à 50 % d'une demande gonflée par le report, alors que l'effet sur les entreprises s'éteint en environ quatre tours (§ 6.6).
   - La mesure de C31 (l. 1895 : Div_F ≥ 0 et D_F ≥ 0 inactives) tient. Elle doit publier le rebond du tour 13.

**Q2 — Propriétaire de la ligne 9 : je confirme le bloc 7, avec un test d'égalité.**
1. C'est ma recommandation de la fiche 6 (§ 9.4, l. 1975). Elle est cohérente avec la ligne 10, que le bloc 7 propose déjà (fiche 5, critère 1 (a)).
2. F3 recalcule i_{L,t}L_t/n_a et i_{D,t}D_{F,t}/n_a (`eq:investissement-dividendes`) sur les mêmes entrées que C2 : encours d'ouverture et taux d'ouverture. Ces taux sont des variables d'état du bloc 7, que le bloc 6 lit dès la phase 2 (fiche 6 § 9.4, l. 1961). Les deux montants sont donc égaux par construction, sans ordre interne en phase 6.
3. Le propriétaire de la ligne (bloc 7) n'est pas le payeur (les entreprises, bloc 6). La règle de caisse rattache la part non payée au **bloc payeur** (l. 481). L'ordre de priorité des entreprises reste celui de F3 : WB, puis intérêts et impôts, puis Div_F.
4. Condition C41 (§ 6.5) : l'égalité est testée à chaque pas au J3. Une part impayée, au J6, la romprait : F3 et Div_Bk devraient alors lire les montants exécutés (défaut (iv) du § 3.C-6).

**Q3 — Part non payée de la ligne 9 (#57, J6) : je préfère la capitalisation nommée, ligne du bloc 6.**
1. **Le cadre la nomme** : « la part non payée est une ligne de flux nommée du bloc payeur (rationnement déclaré, ou capitalisation nommée) » (l. 481). La perte imputée à E^Bk n'est pas une part non payée du payeur. C'est une décision du créancier (passer une créance en perte), qui exige une règle de valorisation, donc un comportement.
2. **Le résultat de la banque reste juste.** En comptabilité d'engagement, l'intérêt capitalisé est un produit : Π^Bk, calculé en phase 6, reste exact, et Div_Bk n'a pas à relire de montants exécutés. Le défaut (iv) du § 3.C-6 disparaît ; il demeure sous la perte imputée.
3. **F1 la résorbe sans paramètre.** La capitalisation porte L au-dessus de lv\*·K. Au tour suivant, F1 demande un remboursement, qui cède sur Div_F puis sur D_F (§ 3.F de la fiche 6). Aucune vitesse n'est ajoutée.
4. **Limite.** Une capitalisation répétée est une dette qui paie ses intérêts par de la dette. Sa borne est une règle de passage en perte, au J6, avec V4 (#57). Ce n'est pas un retour au défaut de la v2.0 (intérêts impayés capitalisés silencieusement dans le principal, `archive/v2.0/prototype/model.py` l. 1009 à 1017) : la ligne est nommée.

**Q4 — E^Bk = ϑL dans l'identité de la dette : j'accepte. Ce n'est pas un choix, c'est l'identité.**
1. La somme des valeurs nettes de `tab:matrice-bilans` donne B − M^G = V_H + (D_F − L) + E^Bk + E^CB (fiche 9 § 1, point 1). Sous l'option C : B − M^G = V_H + D_F − (1 − ϑ)L + E^CB.
2. **Remesure.** ϑL/(12 PIB) vaut 0,08004 / 0,06220 / 0,03344 à π̄ = 0 / 2 % / 10 %. Avec B tiré de l'identité, le bilan de la banque reboucle : E^Bk par le stock moins ϑL vaut 1,4e−17, −6,9e−17 et 1,1e−16.
3. **Conséquences pour la fiche 9** (C42) :
   - l'illustration de son § 1, point 1, écrite sous E^Bk = 0, passe de 0,244 à **0,30622** an à π̄ = 2 % et YD^HS/PIB = 0,7 ;
   - le déficit stationnaire de Domar augmente de n_a(Γ̄ − 1)·ϑL/(12 PIB), soit **0,159 / 0,247 / 0,387 % du PIB** à 0 / 2 / 10 % ;
   - C30 : entre 2 % et 10 %, B/PIB monte de +0,25775, dont +0,2865 du côté des entreprises et −0,0288 du côté de la banque (ϑΔL), comme au § 3.E ;
   - deux passages de la spécification prennent le terme E^Bk : la phrase « sans titres détenus par les ménages et sans fonds propres de la banque » (l. 1867), et le b de `sec:menages` (l. 1546 ; fiche 9, critère 21). On a b = ν − (L − D_F − E^Bk)/(n_a Y_o), forme déjà écrite par `monnaie` (fiche 5, l. 1128).
4. E^Bk/PIB dépend de π̄ par L/PIB, comme L lui-même. C'est déclaré (C30), non une dérive.

**Q5 — ΔYD = Δ·(B − M^G − E^CB)/n_a dès le tour n : c'est cohérent avec b/(1 + ib), et plus précis.**
1. **Algèbre**, sous quatre hypothèses : stocks sur leur sentier ; Div_Bk et Div_F résiduels, versés le tour même ; contraintes Div ≥ 0 inactives ; i_B = i_res = i_CB du tour.
   - Le revenu de capital des ménages vaut alors **i_CB·NPD/n_a − (Γ̄ − 1)ϑL par pas**, avec NPD = B − M^G − E^CB, quels que soient ϖ_L et ϖ_D. Les écarts se compensent entre la ligne 10, Div_F et Div_Bk.
   - Vérification en maquette à π̄ = 2 % : 0,00678016 PIB du pas pour (ϖ_L, ϖ_D) = (0, 0), (2 %, 1 %), (0,4 %, 0,214 %) et (5 %, 3 %).
2. **Conséquence : dYD/di_CB = NPD/n_a**, effet linéaire.
   - Au tour n, il passe par Div_Bk seul (lignes 11b, 12 et 13).
   - Aux tours suivants, il passe par trois canaux : la ligne 10 (+D_H), Div_F (−(L − D_F)) et Div_Bk (+E^Bk). Leurs parts valent +228,6 %, −148,9 % et +20,3 % à 2 %, comme au § 3.L.
3. **Lien avec la fiche 5.** Si YD = Y_o + i·NPD/n_a, alors b/(1 + ib) = NPD/(n_a YD), c'est-à-dire la semi-élasticité du revenu. La consommation de long terme la reprend à dette donnée, puisque la cible est V_H = ν n_a YD^HS. Trois précisions :
   - i est i_CB, et non i_D ;
   - Y_o est le revenu hors intérêts, net de la rétention (Γ̄ − 1)ϑL ;
   - le numérateur est la dette consolidée NPD, qui contient Res − L^CB (fiche 9, critère 21).

   « Dès le tour n » vaut sous l'option (i) de i_B. Sous l'option (iii), le saut du tour n change de signe (−Δ·L^CB/n_a, § 3.L).
4. **Fait nouveau de maquette : la semi-élasticité dépend fortement de π̄**, par NPD/PIB (C30). Elle vaut **+0,209 / +0,429 / +0,735 % de YD par point** à π̄ = 0 / 2 / 10 %. Le canal rentier est 3,5 fois plus fort à 10 % qu'à 0. Transmis à la fiche 8 (C14, C36) et à #56 (C43, C44).

**Q6 — Calibration des écarts : ni sur le rendement des fonds propres, ni d'abord sur la marge nette d'intérêt. Je recommande les écarts de taux observés, la marge nette servant de contrôle.**
1. **Au socle, les écarts ne touchent pas le revenu agrégé des ménages** (Q5, point 1). Ils n'agissent que par quatre voies :
   - **la composition des dividendes.** Sous (2 %, 1 %), le taux de distribution des entreprises passe de 0,56853 à **0,50480** à 2 %, et de 0,39995 à **0,36359** à 10 %. x_max, au-delà duquel la contrainte Div_F ≥ 0 s'active, passe de 2,933 à **2,660** ans à 2 %, et de 2,853 à **2,697** à 10 % (#55, C38) ;
   - **le niveau de ϱ̄_L** : 2,961 % au lieu de 1 % à 2 %. La calibration ζ ≈ σ/(ϱ̄_L + δ) (fiche 6 § 9.2) en est multipliée par 0,754 (C39) ;
   - **les marges des contraintes** Div_Bk ≥ 0 et Div_F ≥ 0 ;
   - **l'affichage** : i_L, i_D, rendement réel des dépôts.
2. **Ce sont des prix vus par les agents, donc ils se calent sur des prix** : l'écart du taux des crédits nouveaux aux entreprises au taux directeur, et celui du taux directeur au taux des dépôts. Sources candidates, **non lues** : statistiques de taux d'intérêt des institutions financières monétaires de la BCE ; séries de la Réserve fédérale. À lire au J3 (critère 17).
3. **La marge nette d'intérêt du modèle** (Π^Bk rapporté à l'actif) vaut 2,633 / 2,421 / 2,072 % par an sous (2 %, 1 %) à π̄ = 0 / 2 / 10 %. C'est un contrôle, pas une cible : elle mêle les écarts et la composition de l'actif, qui dépend de π̄ (C30).
4. **Le rendement des fonds propres n'est pas calibrable au socle.**
   - Sans coûts d'exploitation, sans pertes et sans impôt sur la banque, c'est un artefact.
   - Il n'est pas superneutre : la variante basse, calée à 10 % à π̄ = 2 %, donne 7,32 % à 0 et 20,64 % à 10 %.
   - Caler sur lui forcerait des écarts de 0,4 et 0,2 point, qui sous-estimeraient le coût du crédit des entreprises.

   S'il est restitué, ce doit être avec la mention « sans coûts d'exploitation ni pertes », ou remplacé par la marge nette dans la fiche détaillée (avis de `jeu`).

**Q7 — Effet de Div_Bk versé le tour même sur θ_H et sur la boucle conjointe.**
1. **θ_H est inchangé.** θ_H est la part de la valeur de la production marginale du pas qui atteint le revenu des ménages (l. 1542).
   - Π^Bk ne dépend que des encours d'ouverture et des taux de la phase 1.
   - La rétention ϑL_{t+1} ne dépend que de la ligne 18, que F1 tire de K_t et du plan de la phase 2 (fondé sur y_{t−1}).
   - Donc ∂Div_Bk/∂y_t = 0, et θ_H reste fixé par les fiches 6 et 9 (fiche 9, critère 14 (c)).
2. **Couplage du crédit avec Div_Bk, dans le pas** : ∂Div_Bk/∂I^plan = −ϑ·lv\* = −0,04. La banque retient 10 % du crédit qui finance Div_F (F3). C'est une fuite faible et stabilisante, à déclarer.
3. **Rendement marginal de la richesse des ménages.** Div_Bk reverse ϖ_D sur chaque dépôt supplémentaire placé en titres : le rendement marginal est donc i_CB, non i_D.
   - Propension de long terme des ménages (`sec:menages`, l. 1544), à π̄ = 2 % : 0,79234 (θ_H = 0,8) et 0,99043 (θ_H = 1) avec i_CB = 3,02 %. On aurait 0,78442 et 0,98052 en prenant i_D = 2,02 %.
   - La maquette conjointe doit prendre i_CB (C43) : fiche 8, critère 11 ; fiche 9, critères 8 (c) et 14 (c).
4. **Délai du canal rentier.** Le plan des ménages du tour n + 1 lit YD_n, Div_Bk du tour n compris (M29). Sous la lecture (e) (i), la consommation répond donc **dès le tour n + 1**, en même temps que l'investissement, et non au seul tour n + 2. La chaîne de C35 et celle du § 3.L (« consommation au tour n + 2 ») sont à compléter.
5. **Effet net à l'impact au tour n + 1**, en équilibre partiel. Hypothèses : α_Y = 0,6 ; η_r = 2 ; I/PIB du § 3.E de la fiche 6 ; YD^HS/PIB = 0,7 ; ϑ = 0,1.

   | π̄ | Effet net, lecture (e) (i) | Effet net, lecture (e) (ii) |
   |---|---|---|
   | 0 | −0,189 % du PIB par point | −0,277 % |
   | 2 % | −0,087 % | −0,271 % |
   | 10 % | **+0,089 %** | −0,250 % |

   - À inflation stationnaire haute, la première réponse de la demande à une hausse de taux est expansionniste. C'est un résultat de maquette, non un fait.
   - Le gain statique (C14, C36) reste réglé par la règle budgétaire (C23). Transmis à la fiche 8 et à #56 (C44).

**Q8 — Lectures (b) et (e) : j'accepte (i) dans les deux cas.**
- **(b) Écart additif.**
  - Les écarts sont neutres pour le revenu agrégé (Q5). S-ζ ne lit que ϱ_L − ϱ̄_L = (i_L − ī_L)/(1 + π\*).
  - La forme de l'écart n'agit donc que par le niveau de ϱ̄_L (C39) et par la distribution des entreprises (C38).
  - La forme multiplicative échouerait au critère 4 (c), écrit avant l'essai.
- **(e) Div_Bk le tour même.** Trois motifs :
  - **symétrie avec F3**, où Div_F est versé en phase 6 du tour de son résultat ;
  - **consolidation exacte dans le tour** : la hausse de la charge d'intérêts de l'État au tour n (ligne 11b) devient le revenu des ménages au tour n. C'est l'hypothèse de distribution complète dans le pas qui fonde la forme b/(1 + ib) de la fiche 5 ;
  - **aucune variable d'état ni aucun artefact de calendrier.** Sous (ii), Div_F change au tour n + 1, mais Div_Bk du tour n n'arrive qu'au tour n + 1. Le revenu des ménages reçoit 0 au tour n, puis (2·NPD − E^Bk)·Δ/n_a au tour n + 1, soit 1,80 fois le régime, puis le régime. Le même empilement, de signe opposé, se produit au tour du retour. C'est un artefact de décalage entre les deux sociétés, non un mécanisme.

  Coût de (i) : la consommation répond dès le tour n + 1 (Q7, point 4). C'est déclaré.

### 6.2 Contrôle des chiffres de mon domaine (remesure indépendante)

| Grandeur | Publiée | Remesure de `macro` | Verdict |
|---|---|---|---|
| ρ̄_K à 2 % et 10 % (l. 705) | 0,7786 ; 0,4214 | 0,77862 ; 0,42144 | conforme |
| ρ̄_IN à 2 % et 10 % (l. 755) | 0,996057 ; 0,981246 | idem | conforme |
| K/(12 PIB) à 0 ; 2 % ; 10 % | — ; 1,55510 ; 0,83598 | 2,00092 ; 1,55510 ; 0,83598 | conforme |
| L/(12 PIB) | 0,80037 (§ 3.0) ; 0,62204 ; 0,33439 | idem | conforme |
| L à n_a = 4 et 52 (2 %) | 0,621423 ; 0,622275 | idem | conforme |
| D_F/(12 PIB) | 0,16636 ; 0,16605 ; 0,16492 | idem | conforme |
| L − D_F ; V_F à 2 % et 10 % | 0,45598 et 0,16947 ; 1,19174 et 0,75713 | idem (à 0 : 0,63401 ; 1,46007) | conforme |
| Distribution des entreprises, taux de Fisher égaux | 0,56853 ; 0,39995 ; −0,07314 à x = 3 | idem (à 0 : 0,68966) | conforme |
| x_max, Div_F ≥ 0 (#55) | 2,933 ; 2,853 | idem | conforme |
| E^Bk = ϑL ; M ; B_Bk (§ 3.E) | 0,08004 / 0,06220 / 0,03344 ; 0,86636 / 0,86605 / 0,86492 ; 0,16686 / 0,32705 / 0,58480 | idem | conforme |
| B − M^G − E^CB | 0,14603 / 0,30622 / 0,56397 | idem | conforme |
| Π^Bk/PIB ; rendement des fonds propres ; Div/Π | 0,02547 / 0,02298 / 0,01905 ; 31,82 / 36,94 / 56,97 % ; 0,93772 / 0,89262 / 0,79695 | idem | conforme |
| Div/Π à n_a = 4, 12 et 52 | 0,892301 / 0,892616 / 0,892737 | idem | conforme |
| B_Bk/actif | 0,1725 / 0,3446 / 0,6362 | idem | conforme |
| Condition d'existence à 2 % | −0,000947 (écarts nuls) ; +0,0330 | −0,000947 ; +0,03298 | conforme |
| Impôt d'inflation net / YD | 0 / −0,037 / −0,485 % | idem | conforme |
| C29 : saut du tour n ; tours suivants | +13,33 % ; +2,71 % de Π | idem | conforme |
| ΔYD/YD par point à 2 % ; parts aux tours n + 1 et suivants | 0,429 % ; +229 / +20 / −149 % | 0,429 % ; +228,6 / +20,3 / −148,9 % | conforme |
| C30 : ΔB entre 2 % et 10 % | +0,2578 ; +0,2865 ; −0,0288 | +0,25775 ; +0,2865 ; −0,0288 | conforme |
| ϱ̄_L à 0, 2 % et 10 % (#44) | 3,000 / 2,961 / 2,818 % | idem | conforme |
| Cas du § 3.K (à la main) | E = 60 ; Π = 2,05 ; Div = 1,05 ; 19a = 2,9 ; Res après 8 (b) = 0 ; ΔD = 11,9 | idem ; contrainte budgétaire nulle | conforme |

Aucun écart. Les grandeurs nouvelles de cet avis (distribution des entreprises sous écarts, x_max, effet net au tour n + 1, propension de long terme) sont des résultats de maquette, sous les hypothèses du § 3.0.

### 6.3 Lectures (a) à (h) du § 5 : avis de `macro`

- **(a) l. 450 face à la l. 489 : (i).**
  - Toute règle qui couvre une position négative « ajoute » cette position au refinancement. La lecture (ii) contredirait donc la l. 489.
  - Ce que protège la l. 450, c'est le critère 1 (b) : aucun poste obtenu par différence. Res est tenu au grand livre et mû par la ligne 20 ; la ligne 21 est un flux décidé.
  - Rédaction proposée à `docwriter` : « aucune règle ne calcule les réserves comme solde du bilan bancaire pour en reporter la partie négative sur le refinancement ; la ligne 21 est décidée par la règle du bloc banque à partir de la position tenue au grand livre ». Le mainteneur tranche.
- **(b) : (i)** (Q8).
- **(c) : pas d'objection à (i) au socle.** V1 ne change aucune forme fermée de mon domaine : le point fixe ne dépend pas de λ. Sous (e) (i), la lecture (c) (i) rend l'impulsion rentière immédiate, que V1 lisserait. À juger à la fiche 8.
- **(d) : (i).**
  - Un plancher de i_D déplace du revenu de la ligne 10 vers Div_Bk, sans effet sur le revenu agrégé tant que Div_Bk ≥ 0 est inactive (Q5).
  - Ce serait une borne à seuil libre, active dans le scénario de plancher, sans gain macroéconomique. Le socle n'a pas de billets, donc aucun motif d'arbitrage.
- **(e) : (i)** (Q8).
- **(f) : A8.** C'est la recommandation commune de `macro` et `monnaie` (critère 1 (a)) : l'emprunteur propose sa ligne, sur le modèle de la lecture (a) de M28. C'est une modification, avec ADR, à M33.
- **(g) : sans objection.** La lecture est inerte au socle : Res = 0 à chaque clôture tant que B_CB < M^G\* + E^CB (§ 3.C-3).
- **(h) : i_L et i_D.** C'est ce que lit le bloc 6 : « i_{L,t} (état du bloc 7, C27) » (fiche 6 § 9.4, l. 1961). Avec i_{CB,t−1} seul, le bloc 6 devrait reconstruire i_L, donc connaître ϖ_L.

### 6.4 Avis général

**Favorable à l'option C, avec le socle commun du § 3.N.** Motifs dans mon domaine :
- **Cohérence stock-flux** : aucun solde résiduel, contrainte budgétaire exacte (cas du § 3.K recalculé), E^Bk calculé deux fois.
- **État stationnaire** : formes fermées sans vitesse, toutes reproduites (§ 6.2).
- **Identités de la dette et de Domar** : elles restent en forme fermée avec ϑL.
- **Frontière crédit** : conforme à M28 (lecture (a), F1 et F3 inchangées).
- **Canal rentier** : la banque reverse intégralement son résultat marginal, si bien que ce canal vaut exactement i_CB·NPD/n_a. C'est la forme la plus nette pour #56 et C14.

**Réserves**, sans désaccord avec `monnaie` :
1. La chaîne des délais est à compléter : la consommation répond dès le tour n + 1 par Div_Bk (Q7, point 4 ; C43).
2. Le taux de distribution des entreprises, x_max et la calibration de ζ sont à recalculer avec les écarts (C38, C39).
3. La calibration se fait sur des prix, et le rendement des fonds propres n'est pas une cible (Q6).
4. La « demande non satisfaite » sous ς_L inclut le report (Q1, § 6.6).

### 6.5 Conditions transmises

- **C38 (fiche 6, script d'état stationnaire du J3, #55).**
  - Le taux de distribution des entreprises et x_max se calculent avec i_L = i_CB + ϖ_L et i_D = i_CB − ϖ_D : 0,50480 et 0,36359 ; x_max = 2,660 et 2,697 ans à π̄ = 2 % et 10 %.
  - Seuils de Div_F ≥ 0 en écart de taux réel : −7,13 / −3,56 / −1,68 points à ζ = 4 / 8 / 17, au lieu de −9,57 / −4,79 / −2,25. À ζ = 17, le test « distribution positive sous −2 points » (l. 1895) échouerait. *Annotation du 04/10/2026 (`macro`, avis sur la validation de `sec:banque`) : ces seuils sont calculés à taux nominaux du crédit et des dépôts inchangés ; si la baisse du taux réel abaisse aussi i_L et i_D, écarts constants, la borne de ζ passe de 14,26 à 17,85 et ζ = 17 tient le critère « −2 points » (dividendes de 0,3 % des ventes). La lecture du critère (ϱ_L seul ou taux directeur, écarts compris) est à fixer avant l'essai du J3.*
    *Annotation du 04/10/2026 (`monnaie`, validation de la spécification) : −3,56 se lit −3,57 (−3,5657 remesuré).*
  - Les chiffres de la l. 1863, calculés à « taux du crédit et des dépôts de Fisher », gardent cette hypothèse déclarée ou sont mis à jour à la décision.
- **C39 (fiche 6, calibration de ζ, M28 § 9.2).** ζ ≈ σ/(ϱ̄_L + δ) se calcule avec ϱ̄_L écart compris : 2,961 % à 2 %, soit un facteur 0,754 sur ζ à σ donné par rapport à ϱ̄_L = 1 %.
- **C40 (fiche 6, clause « ligne 18 » de F1, dans M28).**
  - Ligne 18 = (1 − ς_L)·max(ΔL^d ; 0) + min(ΔL^d ; 0) ; F1 inchangée.
  - La mesure de C31 publie la décroissance de l'effet sur Div_F (−50 / −25 / −13 % du crédit de base aux tours 1 à 3) et le rebond du tour 13.
- **C41 (fiches 6 et 7, J3).** À chaque pas, l'intérêt recalculé par F3 égale les lignes 9 et 10 (part des entreprises) exécutées, à 1e−12 × S^Bk près. Une part non payée (J6) est le déclencheur de la lecture des montants exécutés.
- **C42 (fiche 9).**
  - Identité : B − M^G = V_H + D_F − (1 − ϑ)L + E^CB.
  - Illustration du § 1 : 0,30622 an à 2 %.
  - Déficit de Domar : +0,159 / 0,247 / 0,387 % du PIB.
  - La l. 1867 et le b de la l. 1546 (critère 21) prennent E^Bk.
- **C43 (fiches 8 et 9, boucle conjointe : fiche 8, critère 11 ; fiche 9, critères 8 (c) et 14 (c)).**
  - Le rendement marginal de la richesse des ménages est i_CB.
  - θ_H est inchangé par la banque ; le couplage −ϑ·lv\*·ΔI^plan est déclaré.
  - Le canal rentier vaut 0,209 / 0,429 / 0,735 % de YD par point.
  - La consommation répond dès le tour n + 1 sous (e) (i). C35 et C16 sont complétées en conséquence.
- **C44 (fiche 8, C14, et #56).** L'effet net en équilibre partiel au tour n + 1 vaut −0,189 / −0,087 / +0,089 % du PIB par point à π̄ = 0 / 2 / 10 %. Il est remesuré dans la boucle conjointe, avec la règle budgétaire, avant l'ouverture du levier de taux.
- **Au J3 (critère 17).** ϖ_L et ϖ_D se calent sur des écarts de taux observés, sources lues. La marge nette d'intérêt sert de contrôle ; le rendement des fonds propres n'est pas une cible.

### 6.6 Points signalés à `jeu` (non tranchés)

- **Refus de crédit.** La « demande non satisfaite » reste à 50 % pendant les 12 tours, mais l'effet sur les dividendes s'éteint en environ quatre tours, et rebondit au tour 13. Additionner les montants refusés tour par tour surestimerait le choc d'environ onze fois. Je suggère de restituer aussi le manque d'encours (L/K face à lv\*).
- **Écarts de taux.** Ils ne changent pas le revenu agrégé des ménages : seule la composition de leur revenu bouge.
- **Rendement des fonds propres.** Les 37 % sont un artefact, sans coûts d'exploitation ni pertes.
- **Premier effet d'une hausse de taux.** Sous (e) (i), la consommation réagit dès le tour n + 1. À inflation haute, la première réponse nette de la demande est positive (C44).

### 6.7 Constat hors du périmètre (fiche 6 et spécification, section décidée)

- `sec:investissement-conditions` (l. 1877) et `investissement.md` § 9.2 (l. 1914) écrivent : « distribution dans [0,2 ; 0,9], soit un capital de moins de 2,933 ans ». Or 2,933 est le seuil de Div_F ≥ 0 (#55).
- La borne de 0,2 correspond à x < **2,707** ans à 2 % et à **2,482** à 10 % (taux de Fisher égaux), et à 2,469 et 2,356 sous les écarts de l'option C.
- C'est un écart de rédaction, sans effet sur M28. Un commentaire sur #55 est proposé au compte rendu de `macro`.

## 7. Avis de `jeu`

*`jeu`, 04/10/2026 (issue #71, jalon 2), sur la fiche à l'état `0e3fb17` (branche `claude/j1-monnaie-etat`, PR #77). Réponses aux sept questions de `monnaie` (§ 5).*

**Chiffres.** Aucun moteur n'existe encore. J'ai recalculé les formes fermées de l'option C, indépendamment de `monnaie`, à partir des ratios amont du § 3.E (deux scripts hors dépôt, 04/10/2026, sans import du dépôt ni d'`archive/`). Ils retrouvent les valeurs des § 3.E et 3.L : rendement des fonds propres 31,82 / 36,94 / 56,97 % ; écart de Π^Bk +13,33 % au tour 1, +2,71 % aux tours 2 à 12, −10,62 % au tour 13 ; revenu des ménages +0,429 %. Les hypothèses sont celles du § 3.0 ; le revenu disponible YD = 0,714 est une lecture de `jeu`. Les chiffres nouveaux de cet avis viennent des mêmes scripts.

**Question ludique de la fiche.** Le bloc n'ouvre aucun levier. Il est le tuyau par lequel le taux directeur atteint les entreprises, les épargnants et le Trésor. Trois questions en découlent :
- la transmission se voit-elle, au bon tour, sans faux signal ?
- les gagnants et les perdants d'une décision de taux sont-ils nommables ?
- un levier qui le traverse (achats de titres, dépense publique) a-t-il un effet identifiable ?

### 7.A, 7.B, 7.D, 7.V et 7.R (brièvement)

- **A : à revoir.** Les leviers κ^CAR et ϱ^res paraissent lisibles, mais l'effet de ϱ^res n'est écrit nulle part (3.A-6 (ix)) : c'est un levier mort. Le plafond est une falaise (instabilité 15). L'insolvabilité et la recapitalisation sont au socle, sans signal précurseur.
- **B : à revoir.** Aucun levier. Le rationnement est servi dans l'ordre des indices des secteurs, invisible et injuste entre secteurs. Le cliquet de L_cb est invisible.
- **D : à revoir.** Les taux sautent par crans quand un ratio que le joueur ne voit pas sort de sa bande.
- **V1** : acceptable seulement si λ/n_a ≥ 0,5. À 0,25, le tour n + 1 ne transmet que 0,25 point (seuil d1 manqué). **V2** : sans intérêt ludique. **V3** : à revoir, la norme de fonds propres se déplace avec l'inflation (0,164 / 0,093 / 0,044). **V4** : à garder pour le J6, avec #57 ; E^Bk/L sous ϑ y serait un signal précurseur naturel d'un resserrement du crédit (O3).
- **R : hors classement.** Référence ; contredit la grammaire des délais (C27, C35).

### 7.C Option C — écarts constants, refinancement sur la position nette, fonds propres ancrés

- **Récit en une phrase** : « la banque prête à qui le demande au taux directeur plus un écart fixe, rémunère les dépôts au taux directeur moins un écart fixe, applique tout changement au tour suivant, garde des fonds propres égaux à une part fixe de ses crédits et distribue le reste ». Une seule phrase, sans exception cachée.
- **Ce que voit le joueur** (taux directeur +1 point aux tours 1 à 12, π̄ = 2 %) :
  - taux du crédit et des dépôts : +1,0 point au tour 2, soit dix crans ; dès le tour 1 si les taux annoncés sont affichés (condition 1) ;
  - revenu des ménages : +0,429 % à chaque tour de 1 à 12, 0 dès le tour 13 ; aucun reste ;
  - résultat de la banque sur 12 tours : +3,59 % (fenêtre 1-12), puis −0,89 % sur la fenêtre 13-24, contrecoup du saut d'un tour (C29) ;
  - rendement des fonds propres sur 12 tours : +1,33 point (d2).
- **Gagnants et perdants d'une hausse de taux** : l'État paie plus d'intérêts (ligne 11b) ; les épargnants touchent davantage (intérêts des dépôts, dividendes de la banque) ; les entreprises endettées perdent (leurs dividendes reculent). Effet symétrique au retour : aucune remise à zéro gratuite.
- **Leviers qui traversent le bloc** :
  - *taux directeur* : direct, un tour de délai, contrepartie visible le tour même (charge d'intérêts de l'État, résultat de la banque) ;
  - *dépense publique* : B_Bk et dépôts des entreprises montent le tour même ; Res et L^CB inchangés ;
  - *achats de titres de la banque centrale* : **neutres au socle**, en deçà comme au-delà de M^G\*. Avec i_B = i_res = i_CB, l'écart de Π^Bk vaut −3,5e−18 pour un achat de 0,01 (12 × PIB) et −6,9e−18 pour 0,03 > M^G\*. Seuls B_Bk, L^CB et Res changent. C'est un levier sans effet identifiable (O2) : condition 6.
- **Stratégies.**
  - Aucune stratégie interne à la banque : elle n'a ni levier ni borne.
  - *Dette sans contrainte de financement* : la banque souscrit tout le reliquat de l'émission, sans limite, au taux que fixe le même joueur. Cela renforce #78 ; un pays sans règle peut financer un déficit permanent sans coût perceptible tant que i_B < g.
  - *Canal rentier et inflation* : l'écart de revenu des ménages par point de taux est proportionnel à B − M^G : 0,146 / 0,306 / 0,564 % du PIB à π̄ = 0 / 2 / 10 %. Il est 1,84 fois plus fort à 10 % qu'à 2 % : là où il faut casser l'inflation, la hausse du taux enrichit le plus les ménages (#56).
- **Risques.**
  - *Indicateurs morts* : écarts au taux directeur, E^Bk/L (= ϑ exactement), L^CB (= M^G\*) et Res (= 0) sont constants par construction.
  - *Faux signal d'un tour* : au tour de la décision, l'écart affiché à l'ouverture se réduit d'un point, comme si la banque rognait sa marge.
  - *Niveau du rendement des fonds propres* : 37 % à 2 %, 57 % à 10 % ; le joueur y lirait une rente bancaire qui n'est qu'une hypothèse de calibration (3.C-6 (v)).
  - *Signe net du taux* : non établi (#56) ; l'option C retient la transmission complète aux dépôts, hypothèse sous laquelle la maquette de #56 inversait le signe.
- **Verdict : lisible**, sous les conditions 1 à 9.

### Réponses aux sept questions de `monnaie`

1. **Deux niveaux d'indicateurs : à clarifier.**
   - Au tableau du tour, « écarts au taux directeur » est remplacé par les **taux du crédit et des dépôts annoncés pour le tour suivant**, écrits en 8 (c) ; la transmission se lit au tour même de la décision.
   - Le **rendement réel des dépôts** i_D − π monte au tableau du tour : quasi nul à l'état stationnaire quelle que soit l'inflation (0,00 / +0,02 / +0,10 %), il ne bouge que si le taux s'écarte de sa règle. C'est le signal de l'épargnant.
   - La demande non satisfaite n'apparaît qu'avec l'événement de scénario (réponse 5).
   - Le rendement des fonds propres reste dans la fiche détaillée, sur 12 tours seulement, avec son niveau normal à l'inflation mesurée et la mention « sans coûts d'exploitation au socle » jusqu'à la calibration du J3.
   - E^Bk/L, Res, L^CB et B_Bk restent dans la fiche détaillée comme bilan ; E^Bk/L porte la mention « constant par règle au socle ».
2. **Saut de C29 : lisible, sur 12 tours, avec une infobulle qui annonce les deux moitiés.** Le saut est interne à la banque : le revenu des ménages reste lisse, Div_Bk prenant le relais de la ligne 10 au seul tour 1. Le contrecoup laisse −0,89 % sur la fenêtre 13-24. Texte proposé : « Le tour où le taux directeur change, la banque paie et reçoit déjà le nouveau taux sur ses titres et son refinancement, mais ses taux de crédit et de dépôt ne changent qu'au tour suivant : son résultat fait un saut d'un tour, que le retour du taux compense à l'identique. »
3. **Taux des dépôts négatif : lisible, accord pour la lecture (d)(i), sans plancher.** Sans billets au socle, rien ne permet aux ménages d'échapper à un taux négatif. Un plancher à 0 serait une borne sans mécanisme nommable. Le tableau affiche alors : « taux des dépôts négatif : au socle, aucun billet ne permet aux ménages d'y échapper ».
4. **Achat de titres invisible : lisible pour la banque (B_Bk et L^CB bougent), à revoir pour le levier.** La neutralité est totale, au-delà de M^G\* aussi, sous i_B = i_res = i_CB. Condition 6, transmise à la fiche 8.
5. **Noms des événements de scénario.**
   - ς_L : « **Restriction du crédit bancaire** (événement externe, tours a à b) : les banques refusent x % des nouveaux crédits demandés ; demande non satisfaite : y u.m., absorbée par les dividendes et les dépôts des entreprises ; investissement non touché ».
   - ς_B : « **Adjudication non couverte** (événement externe, tours a à b) : x % de la dette émise ce tour n'a pas trouvé preneur ; encaisse du Trésor sous sa cible ; dépenses rationnées au tour suivant ».
   - Les deux portent la mention « scénario, sans signe précurseur au socle ». « Crise » est réservé aux types de crise du J6 (O3). « Resserrement » serait confondu avec une hausse de taux. « Placement raté » reste le terme interne.
6. **Transmission : complète, lecture (c)(i).** Récit en une phrase ; avec les taux annoncés, l'effet se voit au tour de la décision. V1 à λ/n_a = 0,5 transmet 0,5 / 0,75 / 0,875 / 0,94 point aux tours n + 1 à n + 4 : un délai que le joueur ne distinguera pas des autres, pour deux paramètres. V1 reste une option de calibration au J3, sous d1 (λ/n_a ≥ 0,5), si des sources lues l'imposent.
7. **Revenu des ménages +0,43 % : à clarifier.**
   - Le mécanisme est explicable et symétrique : « taux haut : l'État paie, les épargnants touchent, les entreprises endettées perdent ».
   - Le signe macroéconomique ne l'est pas encore (#56). L'option C confirme l'hypothèse de transmission complète aux dépôts sous laquelle le signe s'inversait.
   - Le canal croît avec la dette nette et avec l'inflation (×1,84 entre 2 % et 10 %).
   - Conditions 4 et 5. Toute correction est un choix de conception, dont `monnaie` et `macro` diraient le coût en fidélité ; je n'en propose pas.

### Indicateurs (critère 13 (a))

| Indicateur | Niveau | Verdict | Motif ou point à clarifier |
|---|---|---|---|
| i_L, i_D en vigueur ce tour | tableau du tour | **lisible** | % par an, une décimale |
| i_L, i_D annoncés pour le tour suivant | tableau du tour | **à ajouter** | Transmission visible au tour de la décision |
| Écarts au taux directeur | fiche détaillée | **hors du tableau** | Constants par construction ; faux signal d'un tour au tableau |
| Rendement réel des dépôts i_D − π | tableau du tour | **à ajouter** | Signal de l'épargnant ; mention si i_D < 0 |
| Crédit nouveau | tableau du tour | **lisible** | — |
| Demande non satisfaite | événement | **à clarifier** | Affichée avec l'événement « Restriction du crédit bancaire » seulement |
| Masse monétaire au PIB | tableau du tour | **lisible** | Facteur de fenêtre publié |
| Π^Bk et Div_Bk | fiche détaillée | **à clarifier** | Sur 12 tours seulement ; infobulle C29 (réponse 2) |
| Rendement des fonds propres | fiche détaillée | **à clarifier** | 12 tours ; niveau normal à l'inflation mesurée ; mention « sans coûts d'exploitation » jusqu'au J3 |
| E^Bk/L | fiche détaillée | **hors du tableau** | Égal à ϑ par règle ; utile au J6 (V4) |
| Res, L^CB, B_Bk au PIB | fiche détaillée | **lisible** | Bilan ; contrepartie des achats de titres |
| Décomposition de ΔYD (d3) et charge d'intérêts de l'État | tableau du tour, avec la fiche 5 | **à ajouter** | Côte à côte, pour #56 |

### Préférence motivée

- **Ma préférence va à C**, comme celle de `monnaie`.
  - **Mes motifs propres** :
    - une règle en une phrase ;
    - des taux annonçables un tour à l'avance ;
    - d1 tenu avec dix crans et e (i) tenu ;
    - aucun plancher ni plafond invisible ;
    - des normes que n'importe quelle vitesse laisse en place ;
    - des gagnants et perdants nommables ;
    - aucune remise à zéro gratuite.
  - **Les motifs de `monnaie`**, que je ne juge pas : critères 1 à 12 et 14 à 18.
- **Faiblesses ludiques**, déclarables, aucune rédhibitoire au socle :
  - quatre indicateurs constants ;
  - un rendement des fonds propres invraisemblable avant calibration ;
  - des achats de titres neutres ;
  - une dette publique absorbée sans limite (#78) ;
  - un canal rentier qui croît avec l'inflation (#56).
- **Classement** : C > V1 (λ/n_a ≥ 0,5) > V3 > D > B > A. R est hors classement.
- **Lectures du § 5** : (b) additive, accord (0,18 point entre 0 et 10 %, moins de deux crans) ; (c)(i) et (d)(i), accord ; (e)(i), accord (YD lisse, alors que (ii) crée un trou au tour n puis un pic au tour n + 1) ; (g), accord (une bascule de référence serait invisible) ; (a), (f) et (h) sans enjeu ludique.
- **Coût en fidélité** : aucun écart à la littérature demandé. Taux annoncés, rendement réel des dépôts, retrait des indicateurs constants et libellés d'événements sont des choix de restitution.

### Conditions demandées au § 9

1. **Taux annoncés pour le tour suivant** au tableau du tour, à côté des taux en vigueur ; écarts au taux directeur dans la fiche détaillée seulement.
2. **Rendement réel des dépôts** au tableau du tour, avec la mention « taux des dépôts négatif : au socle, aucun billet ne permet aux ménages d'y échapper » quand i_D < 0.
3. **Π^Bk, Div_Bk et rendement des fonds propres sur 12 tours seulement**, avec l'infobulle C29 (réponse 2), le niveau normal à l'inflation mesurée et la mention « sans coûts d'exploitation au socle » jusqu'à la calibration du J3. E^Bk/L porte la mention « constant par règle au socle ».
4. **Tableau levier → indicateur → délai → contrepartie** (critère 13 (c)) :

   | Levier | Indicateur | Délai | Contrepartie |
   |---|---|---|---|
   | Taux directeur | i_L, i_D annoncés ; revenu des ménages | annoncés au tour n, appliqués au tour n + 1 ; revenu dès le tour n | Charge d'intérêts de l'État, résultat de la banque, dividendes des entreprises, le tour n |
   | Dépense publique | B_Bk ; dépôts des entreprises | tour n | Dette publique détenue par la banque |
   | Achats de titres de la banque centrale | B_Bk, L^CB, Res | tour n | Aucun effet sur les taux, la monnaie ni le résultat de la banque au socle (déclaré) |

   *Annotation du 04/10/2026 (`monnaie`, validation de la spécification) : les dividendes des entreprises ne changent qu'au tour n + 1 (F3 lit i_L et i_D d'ouverture) ; au tour n, la contrepartie est la charge d'intérêts de l'État et le résultat de la banque, si le taux des titres suit le taux directeur du tour. L'encadré `joueur` de `sec:banque` est rédigé ainsi.*

5. **Décomposition de ΔYD** (intérêts des dépôts, dividendes de la banque, dividendes des entreprises) affichée à côté de la charge d'intérêts de l'État. L'essai de #56 inclut π̄ = 10 % et un archétype à dette élevée, le canal rentier y étant 1,84 fois plus fort qu'à 2 %.
6. **Fiche 8, levier « achats de titres »** : ouvert au J4 seulement avec un canal (corridor non nul, prime ou durée, fiche 9), sinon affiché comme « opération de bilan, sans effet sur les taux ni sur la monnaie au socle ».
7. **Événements de scénario** nommés « Restriction du crédit bancaire » (ς_L) et « Adjudication non couverte » (ς_B), avec leur durée, leur ampleur et la mention « scénario, sans signe précurseur au socle » ; le libellé joueur entre au glossaire.
8. **#78** : mention que la banque souscrit tout le reliquat sans limite au socle (C22), au taux fixé par le joueur.
9. **J6** (#57) : V4, avec E^Bk/L sous ϑ comme signal précurseur d'un resserrement du crédit endogène.

### Seuils (critère 13 (d) et (e), adoptés le 04/10/2026)

- (d1) tenu : +1,0 point, dix crans, au tour n + 1.
- (d2) +1,33 point sur 12 tours ; +1,00 point au tour 12.
- (d3) publié (§ 3.L).
- (e)(i) tenu par i_L et i_D ; (e)(ii) pic au tour 2, au tour 1 avec les taux annoncés ; (e)(iii) aucune dynamique lente.
- Aucun seuil nouveau proposé.

**Issue proposée par `jeu`** (création soumise au mainteneur ; corps dans le compte rendu de la session, PR #77) : « J4 — restitution du bloc banque commerciale : taux annoncés, rendement réel des dépôts, résultat sur 12 tours, indicateurs constants hors du tableau ».

## 8. Décision du mainteneur

- **Numéro** : M31 (reporté dans `docs/feuille-de-route.md`, § 4), prise seule, avant la paire des fiches 8 et 9 (P14).
- **Date** : 04/10/2026.
- **Option retenue** : **C**, avec le socle commun du § 3.N :
  - taux des crédits et des dépôts à écart constant du taux directeur, i_L = i_CB + ϖ_L et i_D = i_CB − ϖ_D, écrits en phase 8 (c), lus au tour suivant (variables d'état i_L et i_D du bloc 7) ;
  - refinancement (ligne 21) décidé sur la position nette de réserves après la phase 8 (b) : à la clôture, Res·L^CB = 0, sans paramètre ;
  - fonds propres ancrés à ϑ·L par un dividende résiduel Div_Bk, versé le tour même ;
  - crédit servi à la demande, sans plafond ; deux entrées de scénario déclarées (ς_L, refus de crédit ; ς_B, placement raté), valeur stationnaire nulle ;
  - aucun levier bancaire propre au socle (renvoi au J6).
- **Lectures du § 5**, toutes selon l'avis commun de `monnaie`, `macro` et `jeu` : (a) (i), la l. 450 n'interdit que le calcul de Res par différence suivi du report de sa partie négative, `docwriter` la précise dans `sec:banque` ; (b) (i), écart additif, dépendance de ϱ̄_L à π\* déclarée et transmise à la fiche 8 ; (c) (i), transmission complète en un tour ; (d) (i), aucun plancher de i_D au socle ; (e) (i), Div_Bk versé le tour même ; (g) écart référencé à i_CB, corridor de largeur nulle au socle, transmis à la fiche 8 ; (h) variables d'état i_L et i_D. **La lecture (f)** (propriétaire des lignes 19a, A8 ou variante) **reste à M33**, avec les fiches 8 et 9 : la propriété de la ligne 19a-banque est conditionnelle jusque-là.
- **Motifs** : le mainteneur a retenu la recommandation de `monnaie`, à laquelle `macro` (§ 6, favorable sous quatre réserves) et `jeu` (§ 7, lisible sous neuf conditions) se rangent. Motifs dans ses propres mots : à compléter par le mainteneur s'il le souhaite.
- **Conditions et réserves** : les réserves du § 5 ; les conditions C38 à C44 de `macro` (§ 6.5) ; les neuf conditions de restitution de `jeu` (§ 7).
- **Ce qui est écarté et pourquoi** : A, B et D (§ 4 et § 7 : levier mort, cliquet de refinancement, taux à crans, plafond en falaise) ; V1 gardée comme option de calibration au J3, sous λ/n_a ≥ 0,5, non comme mode ; V3 (norme de fonds propres dépendant de l'inflation) ; V4 renvoyée au J6 avec #57.
- **Issues et commentaires liés**, sur accord du mainteneur du 04/10/2026 : issue **#79** (restitution J4 du bloc banque, proposée par `jeu`) ; commentaires sur #78 (souscription sans limite du reliquat) et sur #55 (seuil de distribution de la l. 1877, `macro`, § 6.7).

## 9. Conséquences de la décision

*Rédigé par `monnaie` (expert pilote), 04/10/2026, d'après M31 (§ 8), sur la fiche à l'état `320bfbb` (branche `claude/j1-monnaie-etat`, PR #77). Les numéros de ligne de `docs/specification/nations_et_marches.tex` sont ceux de `320bfbb`. La spécification n'a pas changé depuis `0e3fb17`, état lu par `macro` et `jeu` (`git diff --stat 0e3fb17 320bfbb -- docs/specification/` : vide).*

*Conventions :*
- *« B1 » à « B8 » désignent les équations du bloc 7 retenues par M31. Elles remplacent les identifiants (C1) à (C4) du § 3.C, qui entreraient en collision avec les conditions C1 à C44 (`grep -c '\bC2\b'` sur la spécification : 8). Aucun identifiant B1 à B8 n'existe dans la spécification (`grep -c` : 0).*
- *La position nette de réserves après la phase 8 (b) s'écrit Res^{8b}_t − L^{CB}_t, sans symbole propre : N est pris (emploi, `sec:travail`).*
- *Conversions (ADR 0008, I.1) : i_L, i_D, i_CB, i_res, i_B, ϖ_L et ϖ_D sont des taux de flux annuels convertis linéairement (x/n_a) ; π̄, π\* et g sont géométriques ; Γ̄ = [(1 + g)(1 + π̄)]^{1/n_a}.*
- *Le § 9 ne décide rien : il traduit le § 8, les réserves du § 5, les conditions C38 à C44 (§ 6.5) et les conditions 1 à 9 de `jeu` (§ 7). Tout ce qui dépend de M32 (corridor, i_res) ou de M33 (lecture (f), règle de i_B) est signalé comme conditionnel.*

### 9.1 Équations retenues et labels

**Au jalon J1, aucun label** (convention de #42, jalon 4, suivie par `sec:investissement` ; la spécification compte 0 `\label{eq:` à `320bfbb`). `sec:banque` est écrite en encadrés `proposee` citant M31, en `equation*` (`CONVENTIONS.md` § 4.1). Chaque mécanisme y est repéré par son identifiant B1 à B8, avec son label prévu en `\texttt{}`, sur le modèle de `sec:investissement` (l. 1680-1690).

**Labels à créer au J3**, avec `src/nations/blocs/banque.py` (radical `banque`, `CONVENTIONS.md` § 2.1). `coder` pose une balise par label ; `docwriter` retire l'encadré et pose le label dans le même passage.

| Label | Id. | Ce que l'équation détermine | Équation | Phase | Statut | Provenance | Couche |
|---|---|---|---|---|---|---|---|
| `eq:banque-taux-credit` | B1 | taux des crédits du pas suivant, variable d'état | i_{L,t+1} = i_{CB,t} + ϖ_L | 8 (c) | choix de conception | nouvelle, option C (§ 3.C-2, (C1)) ; écart additif, lecture (b) (i) ; transmission complète en un tour, lecture (c) (i) ; écart référencé à i_CB, lecture (g) ; M31 | `blocs/` |
| `eq:banque-taux-depots` | B2 | taux des dépôts du pas suivant, variable d'état | i_{D,t+1} = i_{CB,t} − ϖ_D, sans plancher | 8 (c) | choix de conception | idem ; aucun plancher, lecture (d) (i) ; M31 | `blocs/` |
| `eq:banque-interets-credits` | B3 | ligne 9 | i_{L,t}·L_t/n_a (taux et encours d'ouverture) | 6 | dérivée (ligne 9 du cadre, l. 349) | propriétaire : bloc 7 (Q6 ; recommandation de la fiche 6, § 9.4 ; confirmée par `macro`, § 6.1, Q2) ; M31. Payeur : les entreprises (bloc 6), dont la priorité des paiements reste celle de F3 | `blocs/` |
| `eq:banque-interets-depots` | B4 | ligne 10 | i_{D,t}·(D_{H,t} + D_{F,t})/n_a | 6 | dérivée (ligne 10, l. 350) | fiche 5, critère 1 (a) ; M31 | `blocs/` |
| `eq:banque-resultat` | B5 | résultat de la banque du pas | Π^{Bk}_t = [i_{L,t}L_t + i_{B,t}B_{Bk,t} + i_{res,t}Res_t − i_{D,t}(D_{H,t} + D_{F,t}) − i_{CB,t}L^{CB}_t]/n_a, soit lignes 9 + 11b + 12 − 10 − 13 | 6 | dérivée (définition de E^Bk, l. 255 ; colonne de la banque de `tab:matrice-flux`) | § 3.C-2, (C2). Calculé en phase 6 sur l'ouverture et la phase 1, comme Π^CB l'est en phase 1 (l. 495) ; M31. Date de i_B conditionnelle à M33 | `blocs/` |
| `eq:banque-dividendes` | B6 | ligne 15, dividende résiduel | Div_{Bk,t} = max{0 ; E^{Bk}_t + Π^{Bk}_t − ϑ·L_{t+1}}, avec L_{t+1} = L_t + ligne 18 exécutée (phase 3) | 6 | choix de conception ; max{0, ·} : contrainte de domaine (critère 5 (c)) | § 3.C-2, (C3). Cible de fonds propres sur les crédits et dividende résiduel de GROWTH (Godley et Lavoie, 2007, chap. 11, éq. 11.99 et 11.103, lus par reproduction, `gl8-growth.Rmd` l. 204 et 209), à ajustement complet, sans la vitesse β_b de 11.100. Versé le tour même, lecture (e) (i) ; M31 | `blocs/` |
| `eq:banque-refinancement` | B7 | ligne 21 | ligne 21 = max(L^{CB}_t − Res^{8b}_t ; 0) − L^{CB}_t, d'où L^{CB}_{t+1} = max(L^{CB}_t − Res^{8b}_t ; 0). Res^{8b}_t est la position de réserves après la phase 8 (b), lue au grand livre | 8 (c) | choix de conception, sans paramètre | § 3.C-2, (C4). Lecture (a) (i) de la l. 450 ; forme (i) du critère 2 (c), qui clôt #26, point 5. Demande nulle de réserves dans un corridor sans exigence de réserves : W. Whitesell, FEDS 2006-22, p. 4 (lu) ; M31 | `blocs/` |
| `eq:banque-souscription-titres` | B8 | ligne 19a-banque, **seulement sous la variante de M33** | ligne 19a-banque = (1 − ς_{B,t})·(besoin d'émission du pas − ligne 19a-BC), reliquat de l'équation d'émission (l. 498-501) | 7, après les blocs 9 et 8 | choix de conception | C19, C22, C25 (§ 3.N-3) ; M31 ; propriété conditionnelle à M33 | `blocs/` |

**Les deux branches de la lecture (f), à M33.**
- **Branche A8** (recommandation de `monnaie` et de `macro`) :
  - le bloc 9 propose les trois lignes 19a. La règle de B8 est alors une équation du bloc 9, de label `eq:finances_publiques-…`, nommée par la fiche 9 ;
  - le bloc 7 n'a pas de label B8, et la banque ne siège pas en phase 7 ;
  - ς_{B,t} reste une entrée de scénario du placement, publiée à l'ouverture parmi les conditions de la banque et lue par le bloc 9.
  - Le bloc 7 a alors **sept labels**.
- **Branche variante** (interprétation, note à la table de la fiche 1) :
  - le bloc 7 propose 19a-banque (B8) en phase 7, après le besoin publié par le bloc 9 et la souscription 19a-BC du bloc 8, dans l'ordre C25 ;
  - le bloc 7 a alors **huit labels**.
- Dans les deux branches, la forme de la règle est la même. Seuls changent son propriétaire, son label et `tab:phases` (§ 9.4).

**Ce qui n'a pas de label.**
- **Res_{t+1}.** Res_{t+1} = max(Res^{8b}_t − L^{CB}_t ; 0) est la conséquence de B7 par la ligne 20, contrepartie de règlement appliquée par le noyau (l. 319). C'est une dérivation, sans balise.
- **Ligne 18.** Elle reste proposée par le bloc 6. Sa clause devient ΔL_t = (1 − ς_{L,t})·max(ΔL^d_t ; 0) + min(ΔL^d_t ; 0) (C40). C'est une retouche de F1 (`eq:investissement-demande-credit`, l. 1773), non une équation du bloc 7.
- **Entrées de scénario ς_{L,t} et ς_{B,t}.** Ce sont des données du scénario, publiées à l'ouverture, non des équations.
- **Ligne 19b-banque.** Elle est proposée par le bloc 8 ; la banque en est la contrepartie passive, au pair (§ 3.N-3 (d)). *Précision du 04/10/2026 (ADR 0011 accepté, lecture (i) de 19b, décision du mainteneur ; `docs/feuille-de-route.md` § 4) : au socle, la ligne 19b n'a **aucun proposant** (achats de la banque centrale au J6) et l'État est le seul écrivain de la phase 7 ; la lecture (f) est tranchée par A8 (M33), la branche « variante » des § 9.4 et § 9.8 est sans objet. Les tableaux du § 9.4 gardent leur rédaction d'origine ; `sec:banque` est mise à jour par `docwriter`. Notation : s_CB devient θ_CB.*
- **Contrôle mécanique.** Les huit labels vérifient l'expression régulière de `CONVENTIONS.md` § 2.1, `eq:[a-z][a-z0-9_]*-[a-z0-9]+(-[a-z0-9]+)*`. Contrôle par `uv run --no-project python` dans un répertoire `mktemp -d` : huit « True ».

### 9.2 Paramètres

À porter dans `tab:calibration` au J1, sans `\code{}` avant le code. Les noms sont des propositions.

| Symbole | Nom proposé | Valeur | Unité | Source | Équation |
|---|---|---|---|---|---|
| ϖ_L | `ecart_taux_credit` | 0,02 (indicative) ; variante basse 0,004 | par an, taux de flux, conversion linéaire | **calibré au J3** sur l'écart observé entre le taux des crédits nouveaux aux entreprises et le taux directeur. Sources candidates, non lues : statistiques de taux d'intérêt des institutions financières monétaires de la BCE ; séries de la Réserve fédérale (`macro`, § 6.1, Q6). La marge nette d'intérêt est un contrôle ; le rendement des fonds propres n'est pas une cible. Valeur indicative : v1.5 l. 2263-2264 (R ; révisée à 0,01 l. 2316) | B1 |
| ϖ_D | `ecart_taux_depots` | 0,01 (indicative) ; variante basse 0,00214 | par an, taux de flux, conversion linéaire | **calibré au J3** sur l'écart observé entre le taux directeur et le taux des dépôts, mêmes sources candidates. Valeur indicative : v1.5 l. 2264 (R) | B2 |
| ϑ | `fonds_propres_vises` | 0,10 (hypothèse) | fraction des crédits de clôture | hypothèse, entre les 8 % de Bâle 1988 (lu dans un extrait de moteur de recherche, PDF de la BRI inaccessible) et 1,3 × 0,09 de la v2.0 (`model.py` l. 221 et 1164, L). **Calibré au J3** (critère 17) | B6 |

**Conditions déclarées, contrôlées au chargement, jamais par écrêtage** :
- ϑ > 0 (§ 3.C-2).
- **Condition d'existence** (dividende stationnaire positif, § 3.C-3) : ϑ·i_CB + ϖ_L + ϖ_D·D/L > ϑ·n_a(Γ̄ − 1).
  - Elle est contrôlée par le script d'état stationnaire.
  - Marge de +0,0330 à π̄ = 2 % sous (2 %, 1 %) ; elle échoue sous des écarts nuls dès que r̄ < g (−0,000947 à 2 %).
- Entrées de scénario : ς_{L,t}, ς_{B,t} ∈ [0 ; 1].
- La fiche ne déclare aucune condition de signe sur ϖ_L et ϖ_D : la condition d'existence les contraint.

**Ce qui n'est pas un paramètre** :
- i_CB, i_res (fiche 8 ; corridor de largeur nulle au socle, lecture (g), transmis à M32) ; i_B et sa date de fixation (fiche 9, M33) ;
- M^{G\*} (fiche 9) ; E^CB_0 (fiche 8) ;
- ς_{L,t}, ς_{B,t} : entrées de scénario par tour, de valeur stationnaire 0, publiées à l'ouverture. Ni drapeau ni règle à seuil (ADR 0002) ;
- E^{Bk}_0, L^{CB}_0, Res_0, i_{L,0}, i_{D,0} : valeurs de l'état initial résolu (§ 9.4).

**Décompte (critère 14)** :
- 3 paramètres (ϖ_L, ϖ_D, ϑ) et 2 entrées de scénario (ς_L, ς_B).
- 2 variables d'état (i_L, i_D).
- 0 borne à seuil libre.
- 4 contraintes sans paramètre :
  - Res_{t+1} ≥ 0 (identité de clôture du cadre, l. 487-489) et L^{CB}_{t+1} ≥ 0, tenues par la forme de B7 ;
  - Div_Bk ≥ 0, de domaine ;
  - B_Bk ≥ 0, de conservation, inactive.
- Lignes : 9, 10, 15 et 21, plus 19a-banque sous la variante.
- Aucun drapeau, aucun tirage, aucun historique.

### 9.3 Conditions et réserves

**Lectures de M31 que la section reprend** (§ 8) :
- **(a) (i).** La l. 450 n'interdit que le calcul de Res par différence suivi du report de sa partie négative ; B7 décide la ligne 21 sur la position tenue au grand livre.
- **(b) (i)** : écart additif. ϱ̄_L dépend de π\* : 3,000 / 2,961 / 2,818 % à π\* = 0 / 2 / 10 % et r̄ = 1 % (§ 3.E, #44). Dépendance déclarée, transmise à la fiche 8.
- **(c) (i)** : transmission complète en un tour.
- **(d) (i)** : aucun plancher de i_D.
- **(e) (i)** : Div_Bk versé le tour même.
- **(g)** : écart référencé à i_CB, corridor de largeur nulle au socle, transmis à M32.
- **(h)** : variables d'état i_L et i_D.
- **(f)** : renvoyée à M33 (§ 9.1, deux branches).

**Conditionnel à M32 et M33.**
- Règle de i_B (options (i), (ii), (iii), (β)), à M33. Sous (i), i_B ≡ i_CB du tour, et le saut de Π^Bk au tour de la décision vaut +Δ·(B − M^G − E^CB)/n_a (C29). Sous (iii), il vaut −Δ·L^{CB}/n_a (§ 3.L).
- Largeur du corridor et i_res, à M32. Sous un corridor non nul, B7 reste inchangée et Res·L^CB = 0 tient. Seule change la rémunération de Res > 0 (ligne 12), active seulement si B_CB > M^{G\*} + E^CB.
- Propriétaire de 19a-banque, à M33 (§ 9.1).

**Réserves du § 5, et où elles sont tenues** (§ 9.6) :
1. Formes fermées après un pas sans choc : test « État stationnaire ».
2. Cas du § 3.K, quatre variantes : test « Cas à la main ».
3. C29 : test « C29 ».
4. Div_Bk ≥ 0 sous les scénarios adverses : test « Bornes ».
5. Res_{t+1} ≥ 0 à chaque pas : test « Réserves et refinancement ».
6. Test zéro : test « Test zéro ».
7. Coût du bloc d'au plus 0,48 ms : test « Coût ».
8. Calibration de ϖ_L, ϖ_D et ϑ sur des sources lues : § 9.2 et test « Calibration ».

**Défauts déclarés, qui sont le coût en fidélité de l'option** (§ 3.C-6 et § 5). Ils vont aux `\limites` de B1, B2 et B6 et à l'encadré `portee`.
- Transmission plus rapide que celle que mesure de Bondt (2002) : au plus 50 % environ en un mois (résumé lu).
- Écart des dépôts constant, sans canal des dépôts (Drechsler, Savov et Schnabl, 2017, résumé lu).
- Aucune demande de réserves. Whitesell (FEDS 2006-22, p. 5) la dit positive en pratique.
- i_D < 0 si i_CB < ϖ_D : −1 % au plancher sous (2 %, 1 %).
- Rendement des fonds propres de 37 % à π̄ = 2 %. C'est un artefact sans coûts d'exploitation, pertes ni impôt sur la banque. Il n'est pas superneutre (31,82 / 36,94 / 56,97 %, § 3.E ; remesuré par `macro`, § 6.2, et par `jeu`, § 7).
- Aucun cycle du capital bancaire au socle.
- Π^Bk de B5 lit les lignes 9 et 12 recalculées, non exécutées. C'est exact tant qu'aucune part ne reste impayée, ce qu'assure au socle la contrainte D_F ≥ 0, inactive (§ 3.N-2 (c)) ; correction de `monnaie` du 04/10/2026, qui remplace « ce que démontre le § 3.N-4 ». Une part impayée de la ligne 9 (J6) obligerait B5 et B6 à lire les montants exécutés (§ 3.C-6 (iv) ; C41).

**Ce qui reste paramétrable sans rouvrir M31** (visa de l'expert pilote) :
- les valeurs de ϖ_L, ϖ_D et ϑ, dans les conditions du § 9.2 ;
- la variante V1 (ajustement partiel, λ_X ∈ ]0 ; n_a], λ_X = n_a redonnant B1 et B2) : option de calibration du J3, sous λ/n_a ≥ 0,5 (seuil d1), seulement si des sources lues l'imposent, jamais comme mode. *Lecture de `monnaie`* : comme elle change la forme de B1 et B2 et ajoute deux paramètres, son adoption est soumise au mainteneur.

**Par une décision citant M31** :
- un plancher de i_D (borne à seuil libre, lecture (d)) ;
- une limite de détention de titres (C22 ; active à l'état stationnaire à π̄ = 10 %, § 3.A-3 et 3.B-3) ;
- une encaisse de réserves visée (V2) ;
- un écart sur l'insuffisance de fonds propres (V4) et la ligne nommée de part non payée de la ligne 9 (#57, J6). `macro` préfère la capitalisation nommée, ligne du bloc 6 (§ 6.1, Q3) ; non tranché ;
- un levier prudentiel ou des réserves obligatoires (J6, Q7) ;
- un plafond de crédit (rouvre aussi M28 ; instabilité 15).

**Conditions de `macro` (§ 6.5)** : leur traitement est au § 9.7, leurs tests au § 9.6.

### 9.4 Propriétaires et phases des lignes de `tab:matrice-flux`

**Lignes de la colonne « Banque »** (l. 349-367) :

| Ligne | Propriétaire (propose) | Phase | Règle | Moyen de paiement de la banque | Statut |
|---|---|---|---|---|---|
| 9 | bloc 7 | 6 | B3 | reçoit par débit des dépôts des entreprises | décidé (M31, Q6) |
| 10 | bloc 7 | 6 | B4 | paie par création de dépôts | décidé |
| 11b | bloc 9 | 6 | ligne reçue | reçoit en réserves | contrat existant |
| 12, 13 | bloc 8 | 8 (a) | lignes reçues | 12 reçue, 13 payée en réserves | contrat existant |
| 15 | bloc 7 | 6 | B6 | paie par création de dépôts | décidé |
| 17 | noyau | — | contrepartie de règlement | — | inchangé (l. 319) |
| 18 | bloc 6 | 3 | F1, clause modifiée par C40 (ς_L) | crée des dépôts | M28, lecture (a) ; C40 |
| 19a-banque | **A8** : bloc 9 ; **variante** : bloc 7 (B8) | 7 | (1 − ς_B)·(besoin − 19a-BC) | paie en réserves | **conditionnel à M33** |
| 19b-banque | bloc 8 | 7 | ligne reçue, au pair | reçoit en réserves | fiche 8 |
| 20 | noyau | — | contrepartie de règlement | — | inchangé |
| 21 | bloc 7 | 8 (c) | B7 | — | décidé |

Ni ligne ni poste nouveau. `tab:matrice-flux`, `tab:portes-monnaie` et `tab:matrice-bilans` sont inchangées. Sortie de `uv run python outils/verifier_matrices.py --strict` à `320bfbb` : « tab:matrice-bilans : 9 lignes, 6 colonnes, 44 termes ; tab:matrice-flux : 28 lignes, 6 colonnes, 62 termes ; tab:portes-monnaie : 28 lignes, 3 colonnes, 31 termes ; Aucun écart. », code 0.

**Phases du bloc 7** :

| Phase | Le bloc 7 lit | Le bloc 7 écrit ou propose | Autres blocs |
|---|---|---|---|
| 0 | — | rien. L'ouverture contient i_{L,t}, i_{D,t} (écrits en 8 (c) du pas précédent) et les entrées de scénario ς_{L,t}, ς_{B,t} | moteur |
| 1 | — | rien | bloc 8 : i_CB, i_res, Π^CB (et s_CB sous A8) ; i_B selon M33 |
| 3 | — | **rien** | bloc 6 : ligne 18 (C40) ; demande non satisfaite publiée |
| 6 | ouverture (L_t, B_{Bk,t}, Res_t, L^{CB}_t, D_{H,t}, D_{F,t}, E^{Bk}_t, i_{L,t}, i_{D,t}) ; phase 1 (i_CB, i_res, i_B) ; ligne 18 exécutée en phase 3, d'où L_{t+1} | Π^{Bk}_t (B5) ; lignes 9 (B3), 10 (B4) et 15 (B6) | bloc 6 : lignes 8 et 14 (F3 recalcule 9 et 10 sur l'ouverture) ; bloc 9 : 6, 7, 11a à 11c. Aucun ordre interne |
| 7 | **A8** : rien. **Variante** : besoin (bloc 9), 19a-BC (bloc 8), ς_{B,t} | **A8** : rien. **Variante** : 19a-banque (B8) | **A8** : bloc 9, lignes 19a ; bloc 8, 19b-banque. **Variante** : ordre « État, puis banque centrale, puis banque » (C25) |
| 8 (c) | Res^{8b}_t au grand livre (montant exécuté, ADR 0009) ; L^{CB}_t ; i_{CB,t} | ligne 21 (B7) ; i_{L,t+1} (B1), i_{D,t+1} (B2) | bloc 8 en (a) et (b) |
| 9 | — | rien. La banque n'entre pas dans le groupe de la phase 9 | noyau : Res_{t+1} ≥ 0, E^Bk calculé deux fois |

- **Triangularité.**
  - En phase 6, le bloc ne lit rien de ce qu'un autre bloc écrit dans la phase ; L_{t+1} vient de la phase 3.
  - En phase 8 (c), il ne lit que des montants exécutés.
  - En phase 3, il ne lit pas la demande (lecture (a) de M28).
- **Phase de i_L et i_D.** Selon l'ADR 0009, point 4 (l. 43), la phase 8 (c) est désignée parce que toutes les entrées de B1 et B2 la précèdent (i_CB en phase 1). Chaque variable est écrite une fois par pas, par son propriétaire. Aucun lecteur ne la lit sous son indice daté avant le pas suivant.
- **Règle de caisse de la banque** (§ 3.N-4) :
  - ordre de priorité déclaré : 10 et 15, par création de dépôts ; puis les paiements en réserves, dans l'ordre des phases (19a-banque en 7, 13 en 8 (a)) ;
  - aucune part ne peut rester impayée : le découvert intra-pas est admis (l. 485), et B7 couvre toute position négative, sans plafond ni collatéral (condition transmise à la fiche 8) ;
  - le découvert intra-pas ne porte pas d'intérêt ; seule la ligne 13, assise sur L^{CB} d'ouverture, rémunère le refinancement (#26, point 4).
- **Variables d'état et état initial résolu.**
  - i_L et i_D, par an, de valeurs stationnaires i_CB + ϖ_L et i_CB − ϖ_D.
  - i_{L,0} = i_{CB,0} + ϖ_L et i_{D,0} = i_{CB,0} − ϖ_D, où i_{CB,0} est le taux résolu de la fiche 8.
  - E^{Bk}_0 = ϑL_0.
  - L^{CB}_0 = max(M^{G\*} + E^CB_0 − B_{CB,0} ; 0) et Res_0 = max(B_{CB,0} − M^{G\*} − E^CB_0 ; 0).
  - B_{Bk,0} = B_0 − B_{CB,0}, où B_0 vient de l'identité de la dette (fiche 9 ; C42).
- **Interfaces avec les blocs voisins** :

| Bloc | Le bloc 7 lit | Le bloc 7 rend | Contrat |
|---|---|---|---|
| 5, ménages | rien | i_D (état) ; lignes 10 et 15, montants exécutés lus par YD_t en phase 9 (M29) | C20, C21 ; C43 (délai) |
| 6, investissement | ligne 18 exécutée (L_{t+1}, pour B6) | i_L, i_D (état, lus en phases 2 et 6) ; ς_{L,t} publiée à l'ouverture ; ligne 9 | C27 à C31 ; C38 à C41 |
| 8, banque centrale | i_CB, i_res (phase 1) ; lignes 12, 13 et 19b-banque | ligne 21 ; Res, L^CB | corridor (lecture (g)), allocation sans plafond, #26 pts 4 et 5 |
| 9, État | i_B ; ligne 11b ; besoin d'émission et 19a-BC (variante) | 19a-banque (variante) ou ς_B publiée (A8) ; E^{Bk} = ϑL dans l'identité de la dette | C19, C22, C25 ; C42 ; M33 |

### 9.5 Restitution

Les conditions de `jeu` (§ 7) sont reprises telles quelles. Leur mise en œuvre au J4 relève de l'issue **#79** ; la couche `observation/` lit l'état et les montants exécutés, sans effet sur la trajectoire.

1. **Taux annoncés pour le tour suivant** au tableau du tour, à côté des taux en vigueur. Les écarts au taux directeur ne figurent que dans la fiche détaillée.
   *Mise en œuvre* : i_{L,t+1} et i_{D,t+1} sont écrits en 8 (c) du tour t (B1, B2) ; la transmission se lit au tour de la décision.
2. **Rendement réel des dépôts** au tableau du tour. Quand i_D < 0, il porte la mention « taux des dépôts négatif : au socle, aucun billet ne permet aux ménages d'y échapper ».
   *Mise en œuvre* : indicateur déjà défini dans `sec:menages-restitution` (l. 1612, i_D − π_t, π_t glissement annuel). `sec:banque` y renvoie sans le redéfinir.
3. **Π^Bk, Div_Bk et rendement des fonds propres sur 12 tours seulement.** Ils portent l'infobulle C29, le niveau normal à l'inflation mesurée et la mention « sans coûts d'exploitation au socle » jusqu'à la calibration du J3. E^Bk/L porte la mention « constant par règle au socle ».
   *Mise en œuvre*, définitions proposées à `jeu` pour #79 :
   - rendement des fonds propres : moyenne sur 12 tours de n_a·Π^{Bk}_t/E^{Bk}_t, avec E^{Bk} d'ouverture ;
   - taux de distribution : ΣDiv_Bk/ΣΠ^Bk sur 12 tours.
   Ces deux formes n'ont pas de facteur de fenêtre : leurs niveaux normaux sont les formes fermées du § 3.C-3.
4. **Tableau levier → indicateur → délai → contrepartie** (critère 13 (c)) : repris tel quel du § 7 dans l'encadré `joueur` de `sec:banque`, avec le délai complété par C43 (le revenu des ménages dès le tour n ; la consommation dès le tour n + 1, par Div_Bk). ; dividendes des entreprises au tour n + 1 (annotation du § 7).
5. **Décomposition de ΔYD** (intérêts des dépôts, dividendes de la banque, dividendes des entreprises), affichée à côté de la charge d'intérêts de l'État.
   *Mise en œuvre* : montants exécutés des lignes 10, 15 et 14, et ligne 11b. L'essai de #56 inclut π̄ = 10 % et un archétype à dette élevée (§ 9.6, J4).
6. **Fiche 8, levier « achats de titres »** : ouvert au J4 seulement avec un canal ; sinon affiché comme « opération de bilan, sans effet sur les taux ni sur la monnaie au socle ». Transmis à la fiche 8 (§ 9.7).
7. **Événements de scénario** :
   - « Restriction du crédit bancaire » (ς_L) et « Adjudication non couverte » (ς_B) ;
   - avec leur durée, leur ampleur et la mention « scénario, sans signe précurseur au socle » ;
   - libellés joueur à porter au glossaire (`CONTEXT.md`, `architect`) ; « placement raté » reste le terme interne.
8. **#78** : mention que la banque souscrit tout le reliquat sans limite au socle (C22), au taux fixé par le joueur. Elle figure dans l'encadré `portee`.
9. **J6 (#57)** : V4, avec E^Bk/L sous ϑ comme signal précurseur d'un resserrement endogène du crédit. Transmis (§ 9.7).

**Grandeurs restituées.** Niveaux normaux de la maquette `f7_stat.py` (§ 3.E), remesurés par `macro` (§ 6.2) et par `jeu` (§ 7), pour g = 2 %, π̄ = π\* = 2 %, puis 10 %, à la calibration indicative. Ils seront republiés par le script d'état stationnaire au J3.

| Grandeur | Définition | Unité | Dénominateur | Fenêtre | Niveau normal (2 % ; 10 %) |
|---|---|---|---|---|---|
| i_L, i_D en vigueur ; annoncés | B1, B2 | % par an, une décimale | — | ouverture ; écrits en 8 (c) | 5,02 et 2,02 % ; 13,10 et 10,10 % |
| Écarts au taux directeur (fiche détaillée) | i_L − i_CB ; i_CB − i_D | points par an | — | le tour | ϖ_L ; ϖ_D (constants) |
| Rendement réel des dépôts | i_D − π_t (l. 1612) | points par an | — | le tour | +0,02 ; +0,10 point (i_D − π̄) |
| Crédit nouveau ; demande non satisfaite (événement) | ligne 18 ; (ΔL^d − ΔL)/ΔL^d | u.m. par tour ; fraction | demande du tour | le tour | — ; 0 au socle |
| Masse monétaire | (D_H + D_F) de clôture / ΣPIB | années | PIB des 12 derniers tours | clôture | 0,86605 ; 0,86492 en définition du test zéro, à multiplier par le facteur de fenêtre publié (1,0216 à 2 %, l. 232) |
| Rendement des fonds propres | moyenne sur 12 tours de n_aΠ^{Bk}/E^{Bk} | % par an | E^{Bk} d'ouverture | 12 tours seulement | 36,94 % ; 56,97 % |
| Π^Bk, Div_Bk ; taux de distribution | sommes sur 12 tours ; ΣDiv/ΣΠ | u.m. ; fraction | ΣΠ^Bk | 12 tours seulement | Div/Π : 0,89262 ; 0,79695 |
| E^Bk/L | clôture | fraction | L de clôture | clôture | ϑ (constant par règle) |
| Res, L^CB, B_Bk | clôture / ΣPIB | années | PIB des 12 derniers tours | clôture | Res 0 ; L^CB 0,02083 ; B_Bk 0,32705 et 0,58480 en définition du test zéro |

### 9.6 Tests prévus au J3, puis au J4

Chaque test énonce une propriété et un seuil écrits avant l'essai : réserves 1 à 8 du § 5, critères 1 à 15, conditions C38 à C44.

| Jalon | Test | Propriété | Seuil |
|---|---|---|---|
| J3 | État stationnaire (critère 8 ; réserve 1) | Un pas sans choc depuis l'état résolu laisse i_L − i_CB = ϖ_L, i_CB − i_D = ϖ_D, E^Bk/L = ϑ et Res·L^CB = 0, et L^CB, Res, B_Bk, M/(12 PIB) à leurs formes fermées (§ 3.C-3), pour π̄ = π\* ∈ {0 ; 2 % ; 10 %} et n_a ∈ {4 ; 12 ; 52}. Div/Π à π̄ = 2 % vaut 0,892301 / 0,892616 / 0,892737 pour n_a = 4 / 12 / 52 | 1e−10 relatif |
| J3 | Superneutralité des écarts (critère 4 (c)) | Écarts et E^Bk/L identiques entre π̄ = 0, 2 % et 10 % ; dépendance de L, B_Bk et E^Bk au PIB envers π̄ déclarée (C30) et égale aux formes fermées | 1e−10 |
| J3 | Cas à la main (critère 1 ; réserve 2) | Appel direct des fonctions du bloc sur le cas du § 3.K et ses trois variantes (position négative, position positive cumulée avec la position négative, refus de moitié). Lignes 9, 10, 15 et 21 ; E^Bk par le stock et par les flux ; contrainte budgétaire ΔL + ΔB_Bk + ΔRes − (ΔD + ΔL^CB) − (Π − Div) = 0 | 1e−12 × S^{Bk} |
| J3 | Réserves et refinancement (critère 2 ; réserve 5) | À chaque pas, Res_{t+1} ≥ 0 et Res·L^CB = 0 à la clôture ; L^CB = max(M^{G\*} + E^CB − B_CB ; 0) hors placement raté ; un achat 19b-banque rembourse L^CB avant toute détention de réserves (#26, point 5) | exact (Res ≥ 0) ; 1e−12 × S^{Bk} |
| J3 | Résultat et lignes exécutées (C41 ; § 3.C-6 (iv)) | Π^Bk de B5 égal à la somme des lignes 9 + 11b + 12 − 10 − 13 exécutées. Les intérêts que F3 recalcule (i_L L/n_a ; i_D D_F/n_a) égalent les lignes 9 et 10 (part des entreprises) exécutées | 1e−12 × S^{Bk}, à chaque pas |
| J3 | C29 (réserve 3) | Appel direct, équilibre partiel, i_B = i_res = i_CB du tour : ΔΠ^Bk au tour n vaut Δ·(B − M^G − E^CB)/n_a, puis ΔE/n_a aux tours suivants | 1e−12 relatif |
| J3 | Boucle propre (critère 10 (b)) | Taux et demande exogènes, E^Bk_0 = 0,9·ϑL_0 : dès le premier pas où Div_Bk > 0, E^{Bk}_{t+1} = ϑL_{t+1} (module 0) | 1e−12 relatif |
| J3 | Bornes (critère 12 ; réserve 4) | Scénarios « i_CB au plancher (0) pendant 12 tours », « i_CB + 5 points pendant 12 tours », « ς_L = 0,5 pendant 12 tours ». i_D = i_CB − ϖ_D exactement, même négatif (aucun plancher) | Div_Bk ≥ 0 inactive, ou désactivée au plus tard 12 tours après la fin du choc, sans réactivation ; i_D exact à 1e−15 |
| J3 | Refus de crédit (C31, C40 ; fiche 6) | ς_L = 0,5 aux tours 1 à 12 : ligne 18 = (1 − ς_L)·max(ΔL^d ; 0) + min(ΔL^d ; 0). La demande non satisfaite est publiée. Effet sur Div_F, en unités du crédit nouveau de base : −50, −25 et −13 % aux tours 1 à 3. Rebond au tour 13 publié | ligne 18 exacte ; Div_F ≥ 0 et D_F ≥ 0 selon le test « Bornes » de la fiche 6 (l. 1895) |
| J3 | Placement raté (ς_B ; fiche 9, critères 12 (b) et 16 (c)) | ς_B = x au tour n : M^G clôt sous M^{G\*} de la part non souscrite ; Res et L^CB suivent B7 sans solde résiduel. Le lecteur de ς_B dépend de M33 | 1e−12 × S^{Bk} |
| J3 | Neutralité des achats de titres (avis de `jeu`) | i_B = i_res = i_CB : un achat 19b-banque de x laisse Π^Bk, M et les taux inchangés. B_Bk baisse de x ; L^CB baisse de min(x ; L^CB) ; Res ne monte qu'au-delà de M^{G\*} + E^CB − B_CB | 1e−12 relatif |
| J3 | Monnaie endogène (critère 7 (d)) | Le crédit servi égale (1 − ς_L) fois la hausse demandée, quels que soient Res et L^CB d'ouverture ; ΔM = ΔL par la ligne 18 | exact |
| J3 | Phases (critère 3) | Phase 3 : aucune écriture du bloc 7. Phase 6 : lectures limitées à l'ouverture, à la phase 1 et à la ligne 18 exécutée. Phase 8 (c) : Res^{8b} lue au grand livre. i_L, i_D écrits une seule fois par pas, en 8 (c) | aucune lecture hors ordre |
| J3 | Empreinte (critère 14) | Deux variables d'état (i_L, i_D) ; aucun historique, aucun tirage ; reprise de sauvegarde exacte, y compris d'une partie où ς ≠ 0 | décompte exact ; trajectoire identique |
| J3 | Coût (critère 15 ; réserve 7) | Part du bloc dans `tests/invariants/test_budget.py` | ≤ 0,48 ms par pays-pas |
| J3 | Vitesses (critère 9) | Le bloc n'a aucune vitesse. Dans les branches ×0,5 et ×2 des vitesses des autres blocs (boucle conjointe de la fiche 8), écarts, E^Bk/L, L^CB/(12 PIB) et Res au point fixe identiques entre branches | 1e−6 relatif après H = max(720 ; 20 demi-vies) pas, H déclaré avant l'essai |
| J3 | Test zéro (critère 11 ; réserve 6) | 720 pas sans choc depuis l'état résolu ; moyennes par blocs de 60 pas | bandes du critère 11, à confirmer avec O1 avant l'essai (M19) : M/(12 PIB) ±10 % relatif ; E^Bk/L ±10 % ; écarts ±0,1 point ; B_Bk bande commune avec la fiche 9 ; Res nulle à 1e−12 × S^{Bk} sans titres à la banque centrale |
| J3 | Calibration (critère 17 ; réserve 8) | ϖ_L, ϖ_D sur des écarts observés, sources lues et datées ; ϑ sur une source lue. Marge nette d'intérêt publiée comme contrôle (2,633 / 2,421 / 2,072 % à 0 / 2 / 10 % sous (2 %, 1 %), `macro` § 6.1, Q6). Le rendement des fonds propres n'est pas une cible. Condition d'existence vérifiée | sources citées, ou « non trouvée » |
| J3 | (d1) (critère 13 (d)) | Équilibre partiel, i_CB + 1 point aux tours 1 à 12 | i_L et i_D + 1,0 point au tour n + 1 (au moins 0,5) ; écart à d1 publié, sans écarter |
| J3 | (d2), (d3) | Même choc | rendement des fonds propres sur 12 tours publié (+1,33 point en maquette ; +1,00 au tour 12) ; parts de ΔYD aux tours 2, 3 et 12 publiées |
| J3, avec les fiches 8 et 9 | C43 | Boucle conjointe : rendement marginal de la richesse des ménages égal à i_CB ; θ_H inchangé par la banque ; couplage −ϑ·lv\*·ΔI^plan ; canal rentier de 0,209 / 0,429 / 0,735 % de YD par point ; consommation modifiée dès le tour n + 1 | signe et date exacts ; chiffres republiés par le script |
| J4 | C44 et #56 (condition 5 de `jeu`) | Effet net d'une hausse de taux en boucle conjointe, avec la règle budgétaire, à π̄ = 0, 2 et 10 % et sur un archétype à dette élevée, avant l'ouverture du levier de taux | critères écrits avant l'essai par `monnaie` et `macro` (#56) |
| J4 | (e) perceptibilité | Scénario apparié (O2), i_CB + 1 point aux tours 1 à 12 | (e) (i) deux crans en 12 tours ; (ii) pic au plus tard au tour 24 ; (iii) aucune dynamique lente du bloc |
| J4 | Restitution (conditions 1 à 7, #79) | Niveaux normaux restitués égaux à ceux du script | 1e−9 relatif |

### 9.7 Conditions transmises

**Fiche 6 (`macro`), conditions de M28 complétées** :
- **C38.** Taux de distribution et x_max recalculés avec i_L = i_CB + ϖ_L et i_D = i_CB − ϖ_D :
  - distribution : 0,50480 et 0,36359 ; x_max : 2,660 et 2,697 ans, à π̄ = 2 % et 10 % ;
  - seuils de Div_F ≥ 0 en écart de taux réel : −7,13 / −3,57 / −1,68 points à ζ = 4 / 8 / 17. À ζ = 17, le test « distribution positive sous −2 points » (l. 1895) échouerait : c'est une contrainte de calibration de ζ au J3 ; *Correction de `monnaie` (validation de la spécification, 04/10/2026) : le seuil pour ζ = 8 vaut −3,5657, soit −3,57 à l'arrondi ; la fiche écrivait −3,56.* *Annotation du 04/10/2026 (`macro`, avis sur la validation de `sec:banque`) : ces seuils sont calculés à taux nominaux du crédit et des dépôts inchangés ; si la baisse du taux réel abaisse aussi i_L et i_D, écarts constants, la borne de ζ passe de 14,26 à 17,85 et ζ = 17 tient le critère « −2 points » (dividendes de 0,3 % des ventes). La lecture du critère (ϱ_L seul ou taux directeur, écarts compris) est à fixer avant l'essai du J3.*
  - les chiffres de la l. 1859 (distribution 0,56853 ; 0,39995), calculés sous l'hypothèse de la l. 1853 (« taux du crédit et des dépôts de Fisher »), gardent cette hypothèse déclarée ou sont mis à jour. *Correction de référence* : le § 6.5 de `macro` cite la « l. 1863 » ; à `0e3fb17` comme à `320bfbb`, l'hypothèse est à la l. 1853 et les valeurs à la l. 1859.
- **C39.** ζ ≈ σ/(ϱ̄_L + δ) se calcule avec ϱ̄_L écart compris (2,961 % à 2 %), soit un facteur 0,754.
- **C40.** Clause « ligne 18 » de F1 (l. 1773) : ΔL_t = (1 − ς_{L,t})·max(ΔL^d_t ; 0) + min(ΔL^d_t ; 0) ; F1 inchangée. La mesure de C31 publie la décroissance de l'effet et le rebond du tour 13.
- **C41.** Égalité des intérêts recalculés par F3 et des lignes exécutées (§ 9.6).

**Fiche 5 (`macro`)** :
- **C42.** b = ν − (L − D_F − E^Bk)/(n_a Y_o) (l. 1546).
- **C43.** Délais : le plan des ménages du tour n + 1 lit YD_n, Div_Bk du tour n compris, puis la ligne 10 au taux du tour n + 1. La chaîne C35 (l. 1813) est complétée.

**Fiche 8 (`monnaie`, M32)** :
- largeur du corridor nulle au socle, ou lecture (g) : écart référencé à i_CB ;
- allocation du refinancement sans plafond ni collatéral au socle ;
- i_res ≤ i_CB, au titre du signe de Π^CB et non de l'arbitrage, que B7 clôt ;
- L^CB = max(M^{G\*} + E^CB − B_CB ; 0) ; un achat de titres jusqu'à M^{G\*} + E^CB − B_CB ne fait que réduire L^CB ;
- levier « achats de titres » (condition 6 de `jeu`) ;
- dépendance de ϱ̄_L à π\* (lecture (b), #44) ;
- C43 (fiche 8, critère 11) et C44 (C14, #56).

**Fiche 9 (`macro`, M33)** :
- **C42.** Identité B − M^G = V_H + D_F − (1 − ϑ)L + E^CB. L'illustration du § 1 passe à 0,30622 an à 2 %. Le déficit de Domar augmente de 0,159 / 0,247 / 0,387 % du PIB.
- B_Bk/actif vaut 0,1725 / 0,3446 / 0,6362.
- Dispositif ς_B, et son lecteur selon la lecture (f).
- Le signe de C29 dépend de la règle de i_B.
- Condition 8 de `jeu` (#78).
- Ordre C25 sous la variante.

**J6 (#57)** :
- V4 et la condition 9 de `jeu` ;
- la ligne nommée de part non payée de la ligne 9, que `macro` préfère sous la forme d'une capitalisation nommée, ligne du bloc 6 (§ 6.1, Q3). Le bloc 7 lirait alors les montants exécutés si la perte imputée était retenue ;
- l'insolvabilité, la recapitalisation et les actions bancaires.

**`architect`** :
- retouches de `tab:phases` (§ 9.8) à qualifier, dont la mention de i_{L,t+1} et i_{D,t+1} en 8 (c), signalée au § 3.N-1 ;
- annotation éventuelle de l'ADR 0009 (l. 19 et 43) : la fiche 7 désigne la phase 8 (c) ;
- ADR d'architecture si A8 est retenue à M33 (feuille de route, P14) ;
- `CONTEXT.md` : « écart de taux bancaire », « fonds propres visés », « position nette de réserves », « dividende résiduel de la banque », « Restriction du crédit bancaire », « Adjudication non couverte » ;
- statut de l'inventaire (`docs/blocs/README.md`).

**`jeu`** :
- #79 ;
- définitions proposées du rendement des fonds propres et du taux de distribution sur 12 tours (§ 9.5, condition 3), à confirmer.

**#26 (rang 11 de la feuille de route)** :
- point 4 : déclaration du découvert sans intérêt (l. 485) ;
- point 5 : clos par B7, forme (i).

### 9.8 Surface d'impact documentaire (pour `docwriter`)

Encadrés `proposee` citant M31, sans label (§ 9.1). Numéros de ligne à `320bfbb`.

**`sec:banque`**, à écrire à la place du texte d'attente (l. 1993-1996) :
- encadré de décision M31 :
  - option C et socle commun du § 3.N ;
  - lectures (a) à (e), (g) et (h) ;
  - (f) conditionnelle à M33, avec les deux branches du § 9.1 ;
- tableau des identifiants B1 à B8, avec phase, statut et label prévu, sur le modèle des l. 1680-1690 ;
- taux (B1, B2) :
  - écart additif ; transmission complète en un tour ; écriture en 8 (c), lecture à l'ouverture (C27) ;
  - `\limites` : de Bondt (2002), Drechsler et al. (2017), i_D < 0 sans plancher (borne à seuil libre écartée), dépendance de ϱ̄_L à π\* ;
- lignes 9 et 10 (B3, B4) : propriétaire, payeur, priorité des paiements des entreprises (F3) ;
- résultat et dividende (B5, B6) :
  - Π^Bk sur l'ouverture et la phase 1 ; ancre E^Bk/L = ϑ, indépendante des vitesses ; Div_Bk ≥ 0 de domaine, avec sa marge ; condition d'existence ;
  - `\limites` : ROE sans coûts d'exploitation, défaut (iv) au J6 ;
- refinancement (B7) :
  - position lue au grand livre ; Res_{t+1} = max(·) par la ligne 20 ; Res·L^CB = 0 ; formes fermées de L^CB et Res ; #26, points 4 et 5 ;
  - `\limites` : aucune demande de réserves (Whitesell, FEDS 2006-22, p. 4-5) ;
- placement (B8 sous la variante, ou renvoi à la règle du bloc 9 sous A8) : C19, C22 (aucune limite, déclarée), C25, 19b-banque passive au pair ;
- offre de crédit : C27, ς_L (C31, C40), monnaie endogène (McLeay, Radia et Thomas, 2014, résumé lu), aucun multiplicateur ;
- règle de caisse et priorité des paiements de la banque (§ 9.4) ;
- phases (tableau du § 9.4) ;
- état stationnaire :
  - formes fermées du § 3.C-3 et tableau du § 3.E ;
  - dépendance à n_a par Γ̄ seule ; C30 ; état initial résolu (§ 9.4) ;
- conditions et tests du J3 (§ 9.2, § 9.6) ;
- grandeurs restituées et niveaux normaux (§ 9.5) ;
- encadré `joueur` : tableau levier → indicateur → délai → contrepartie (condition 4 de `jeu`, complétée par C43) ;
- encadré `portee` :
  - une banque ; ni billets, ni réserves obligatoires, ni actions bancaires, ni pertes, insolvabilité ou recapitalisation (J6) ;
  - reliquat souscrit sans limite (#78) ; aucun levier bancaire ;
  - V4 et #57 au J6 ; aucune borne à seuil libre ; aucun tirage.

**Passages existants à retoucher** :
- **l. 450 (lecture (a) (i)).** Remplacer la seconde proposition par la rédaction de `macro` (§ 6.3 (a)) : « aucune règle ne calcule les réserves comme solde du bilan bancaire pour en reporter la partie négative sur le refinancement ; la ligne 21 est décidée par la règle du bloc banque à partir de la position tenue au grand livre ».
- **l. 485.** Ajouter : le découvert intra-pas ne porte pas d'intérêt ; seule la ligne 13, assise sur L^{CB} d'ouverture, rémunère le refinancement (#26, point 4).
- **l. 489.** Préciser que la règle du bloc banque couvre exactement la position négative et qu'une position positive rembourse d'abord le refinancement (renvoi à B7).
- **`tab:phases` (l. 528-537)** :
  - l. 531, phase 3 : retirer « banque » des écrivains ; contenu « demande de crédit, sur les conditions publiées à l'ouverture ». Retouche de forme, sur le précédent de M29 ;
  - l. 535, phase 7 : **A8** → écrivains « État, banque centrale », banque retirée ; **variante** → « État, puis banque centrale, puis banque » (C25). Retouche conditionnelle à M33 ;
  - l. 536, phase 8 : contenu (c) complété par « taux des crédits et des dépôts du pas suivant » (§ 3.N-1, retouche à qualifier par `architect`) ;
  - l. 528, phase 0 : la mention des entrées de scénario ς relève du rang 9 (#69), à voir avec `architect`.
- **l. 1546 (`sec:menages-conditions`, C42 et C43)** :
  - b = ν − (L − D_F − E^Bk)/(n_a Y_o) ; i est i_CB ;
  - « structure non remesurée ici » renvoie désormais à la fiche 7, § 6.1, Q5 (remesure de `macro`) ;
  - le taux des dépôts monte au tour n + 1 d'une décision du tour n, les dividendes de la banque dès le tour n.
- **l. 1628 (`sec:menages-restitution`)** : même précision de date, qui relie la décision de taux à i_D au tour n + 1 et à Div_Bk au tour n.
- **l. 1773 (F1)** : clause de la ligne 18 réécrite selon C40 ; l. 1792 : « la ligne 18 vaut la demande, hors scénario ς_L ».
- **l. 1811** : propriétaire de la ligne 9, le bloc banque (M31).
- **l. 1813 (C35)** : chaîne complétée par C43 (plan des ménages dès le tour n + 1 par Div_Bk).
- **l. 1853 et 1859 (C38)** : hypothèse des taux de Fisher déclarée, ou valeurs sous écarts (0,50480 ; 0,36359).
- **l. 1867 (C42)** : la phrase « sans titres détenus par les ménages et sans fonds propres de la banque, la richesse des ménages moins les crédits nets des dépôts des entreprises » prend E^Bk : « sans titres détenus par les ménages, la richesse des ménages moins les crédits nets des dépôts des entreprises, plus les fonds propres de la banque, ϑL ».
- **l. 1877** : x_max à 2,660 ans sous les écarts (C38). Le constat sur la borne de 0,2 (fiche 7, § 6.7 ; #55) reste hors de cette retouche.
- **l. 1905** : « écrites en fin de tour » devient « écrites en phase 8 (c) » ; propriétaire de la ligne 9 : bloc banque (M31).
- **l. 850 et l. 2033 (`tab:leviers-cadre`)** : transmission du taux directeur aux taux bancaires « un tour, complète (décision M31) ».
- **`tab:calibration` (l. 2087-2128)** : encadré « paramètres du bloc banque commerciale, décision M31 » ; lignes ϖ_L, ϖ_D et ϑ (§ 9.2) ; aucune borne.
- **`tab:symboles` (glossaire, l. 2373 et suivantes)** :
  - ϖ_L, ϖ_D, ϑ, ς_{L,t}, ς_{B,t}, Π^{Bk}, Res^{8b} ;
  - collisions vérifiées (`grep -c` à `0e3fb17` : `varsigma` 0, `varpi` 0, `vartheta` 0) ; ϖ porte toujours un indice (`prix.md` l. 212) ;
  - ne pas introduire N pour la position nette.
- **`sec:ecartees`**, sous-section « Banque commerciale (décision M31) » :
  - A (plafond, prime sur le levier, écrêtages, Res indéterminé) ;
  - B (Res résiduel, instabilité 16 ; cliquet de L_cb ; drapeaux) ;
  - D (indicatrices à bandes, continuum, titres par différence) ;
  - R (référence) ; V2, V3 ;
  - plancher de i_D ; limite de détention ; lecture (c) (ii) hors calibration.
- **`tab:instabilites`, paragraphe après la l. 2346** : le bloc ne réintroduit ni la 16 (aucun solde résiduel), ni la 15 (aucun plafond ni limite), ni la 4 (aucun taux naturel estimé).
- **`sec:changements-v3x` (l. 90-116)** : une ligne 13 « Banque commerciale (décision M31), proposée ».
- **`tab:correspondance`** : inchangée, aucun label au J1.
- **Inchangées** : `tab:matrice-flux`, `tab:portes-monnaie` et `tab:matrice-bilans` (sortie de `verifier_matrices.py` au § 9.4) ; `tab:instruments` (l. 275-280). Le principe « intérêt assis sur l'encours brut, jamais sur une position nette » (l. 242) est respecté : B7 porte sur un flux de refinancement, non sur un intérêt.

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 04/10/2026 | Ouverture (issue #71) ; § 1 et § 2 proposés (jalon 1), en attente de validation des critères par le mainteneur | `monnaie` ; session principale |
| 04/10/2026 | Relecture croisée intégrée (avis de `macro`, `monnaie` et `jeu`, une relance ciblée ; qualifications d'`architect`) ; options ouvertes marquées « à trancher par le mainteneur » | `macro` ; `monnaie` ; `jeu` ; `architect` ; session principale |
| 04/10/2026 | Critères validés par le mainteneur (jalon 1 de #71 terminé), amendements adoptés consignés au § 2 | mainteneur ; session principale |
| 04/10/2026 | Jalon 2, première partie : § 3 à § 5 instruits (options A à D et socle commun, tableau comparatif, recommandation de l'option C) ; § 6 et § 7 à rendre | `monnaie` ; session principale |
| 04/10/2026 | Jalon 2, seconde partie : avis de `macro`, expert consulté (§ 6, favorable à C, conditions C38 à C44), et de `jeu` (§ 7, C lisible sous neuf conditions) ; fiche « avis rendus » | `macro` ; `jeu` ; session principale |
| 04/10/2026 | Décision du mainteneur : option C (M31) ; lectures (a) à (e), (g), (h) selon l'avis commun ; (f) renvoyée à M33 | mainteneur ; session principale |
| 04/10/2026 | § 9 rédigé (conséquences de M31 : équations B1 à B8, paramètres, phases, restitution, tests du J3, conditions transmises, surface d'impact pour `sec:banque`) | `monnaie` ; session principale |
| 04/10/2026 | Validation de `sec:banque` par `monnaie` (avec corrections) ; corrections de la fiche : C38 (−3,57), variante « position positive » du § 3.K, annotation de la condition 4 de `jeu`, localisation de la l. 1546, § 9.3 ; retrait d'un en-tête parasite introduit au commit `481c279` | `monnaie` ; session principale |
| 04/10/2026 | Annotation de C38 (§ 6.5 et § 9.7) : seuils calculés à taux nominaux inchangés (`macro`) | `macro` ; session principale |
| 04/10/2026 | Section `sec:banque` rédigée par `docwriter` (`12e1c4d`, corrections `2b24827` et retouches suivantes), validée par `monnaie` ; jalon 4 de #71 terminé, fiche « spécifiée » | `docwriter` ; `monnaie` ; session principale |
| 04/10/2026 | Lecture (f) tranchée par M33 : A8 (le bloc 9 propose les trois lignes 19a ; la banque ne siège plus en phase 7) ; `sec:banque` à mettre à jour (branche variante retirée) | mainteneur ; session principale |
