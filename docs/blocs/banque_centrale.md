---
bloc: Banque centrale et anticipations
module: src/nations/blocs/banque_centrale.py
expert pilote: monnaie
experts consultés: macro (prix et salaires : frontière inflation ; fermeture du niveau d'activité et dette publique, avec la fiche 9) ; jeu
statut: décidée (M32)
décision: M32 (04/10/2026)
issue: #72
---

# Fiche comparative — Banque centrale et anticipations

> Fiche ouverte à partir du gabarit `0000-gabarit.md` (validé à l'usage, M20), sur le modèle de forme de la fiche 6 « investissement et financement des entreprises » (critères validés le 03/10/2026). Jalon 1 de l'issue #72 : § 1 et § 2 seuls ; les rubriques suivantes portent « à instruire (jalon 2) ». Décidée par paire avec la fiche 9 « État et dette » (M32 et M33, numéros sous réserve de l'ordre réel des décisions ; P14, 04/10/2026) ; instruite une fois la fiche 7 « avis rendus ». Ses critères sont validés par le mainteneur avec ceux des fiches 7 et 9, avant tout commit d'instruction.

Une fiche comparative instruit **l'origine de l'approche** d'un bloc (`docs/exigences.md` § 2.3) : la spécification v1.5, le moteur v2.0, ou une approche nouvelle. Elle est **instruite par l'expert pilote**, commentée par `jeu` et par l'expert consulté que désigne `README.md`, et **décidée par le mainteneur** (décision M-n, reportée dans `docs/feuille-de-route.md`). Aucune approche n'entre dans le moteur ni dans la spécification sans cette décision. Les agents n'écrivent pas la fiche dans le dépôt : elle figure dans leur compte rendu et la session principale la commite. Un **bloc-cadre** (temps et comptabilité) n'est pas un module de `blocs/` : sa fiche instruit ce que le cadre **définit** (conventions, matrices, règles), non des flux proposés ; les adaptations que cela impose sont signalées rubrique par rubrique.

Règles de rigueur (`CLAUDE.md`, « Rigueur ») : un chiffre se remesure ou cite sa source ; une équation de la v1.5 n'a jamais été garantie exécutée ; un comportement de la v2.0 ne vaut que sous son profil (état D1, **non versé** : aucun fait ne peut y être remesuré) et avec ses défauts connus ; chaque fait de la première tentative porte son **statut** S+O, O, R, L, V ou V+O (`CONTEXT.md`, « Statut d'un fait » ; un fait V sur le prototype v2.0 reste un fait de la première tentative, non un résultat v3) ; chaque référence est une publication retrouvée. Citer `archive/v1.5/…` avec numéro d'équation et section, ou avec le **numéro de ligne du `.tex`** quand section ou équation ne sont pas identifiables sans compiler ; `archive/v2.0/…` avec fichier et ligne. **Principe de simplicité** (adopté par le mainteneur le 30/09/2026, fiche « temps et comptabilité » § 2 ; `CONTEXT.md`) : à exigences comptables égales, l'option la plus simple pour le joueur et pour le moteur est préférée ; toute complexité se justifie par une identité qu'elle rend vérifiable ou par un mécanisme perçu à l'échelle d'une partie ; une simplification ne supprime ni une contrepartie comptable visible d'un levier ni une grandeur restituée au tour ; les identités, les tolérances relatives, le déterminisme, les invariants de l'ADR 0002 et la concordance ne se simplifient pas.

## 1. Question posée

*Rédigé par `monnaie` (expert pilote), 04/10/2026, sur la spécification à l'état `10391a1` (branche `claude/j1-monnaie-etat`, PR #77). Les numéros de ligne de `docs/specification/nations_et_marches.tex` sont ceux de cet état.*

Le bloc tient la banque centrale du pays et la formation des anticipations d'inflation. En phase 1, il arrête :
- le taux directeur i_CB et le taux des réserves i_res, par le levier du joueur ou par la règle ;
- le résultat de la banque centrale Π^CB (calcul fixé par le cadre, l. 491-495) ;
- l'anticipation π^e et, selon l'option, la crédibilité et l'état de l'action intégrale de la règle ;
- la cible en vigueur du pas suivant, π*_{t+1}, depuis son levier (ADR 0010, pt 3).

Il propose aussi :
- les intérêts sur réserves et sur refinancement (lignes 12 et 13, phase 8 (a)) ;
- le versement du résultat (ligne 16, phase 8 (b)) ;
- ses achats de titres (lignes 19a-BC et 19b, phase 7).

Ses fonds propres E^CB sont sa valeur nette, calculée deux fois. Le bloc est le second terme de la frontière inflation, avec les fiches 3 et 4. Il détient, avec la fiche 9, la fermeture du niveau d'activité (#44). Il lit les fiches 3 à 7 et débloque la fiche 9 (`docs/blocs/README.md` § 3, rang 8). Sous M22, un pas est un tour.

### 1.1 Contrats hérités

| Contrat | Source | Ce qu'il impose à la fiche 8 | Ce qui le rouvrirait |
|---|---|---|---|
| Calendrier, décisions, conversions | M22 ; ADR 0005, pts 2, 4, 5 et 11 ; ADR 0008, I.1 à I.4 ; `sec:cadre-calendrier` (l. 188, 190-202, 214) | Les leviers et les règles sont lus en phase 1, avant tout flux. i_CB et i_res sont des taux de flux (conversion linéaire) ; π*, π^e et π̄ sont des taux d'inflation (conversion géométrique, (G)). Le glissement est mesuré, jamais converti. Un taux décidé au tour n porte les lignes 12 et 13 du tour n. Le taux réel restitué et testé est r = i − π (l. 214) | Décision citant M22 (et M25 pour (G)) |
| Phase de l'indice des prix (M26) | ADR 0008, II.1 à II.7 ; `sec:cadre-calendrier` (l. 216-220) | L'indice est le prix du tour, écrit en phase 5. La règle lit en phase 1 le dernier prix connu P_{t−1} et le glissement π_{t−1} = P_{t−1}/P_{t−13} − 1 (registre de 13 niveaux). La date de formation de π^e reste à la fiche 8 (II.5). Le critère de la clause de réouverture II.7 est écrit ici, avant l'essai | Clause II.7 : décision citant M26, M24 et M22, et nouvel ADR |
| Cible en vigueur (M30) | ADR 0010 ; `sec:cadre-calendrier` (l. 222-226) | π*_t est une variable d'état par pays, lue à l'ouverture (délai d'un tour). π*_{t+1} est écrite en phase 1 par le bloc 8 depuis son levier, sans changer l'interface des blocs 5 et 6 ni `tab:phases`. Γ^e est calculé par le moteur. Condition de réouverture : délai d'un tour déterminant pour la stabilité (analogue de II.7) | Décision citant M30, M27 et M28 |
| Bilan et lignes de la banque centrale | `tab:matrice-bilans` (l. 302-305) ; E^CB développée l. 255 ; `tab:matrice-flux` (l. 353-368) ; `tab:portes-monnaie` (l. 379, 422-437) | Actif : B_CB, L^CB. Passif : Res, M^G. E^CB = B_CB + L^CB − Res − M^G. Lignes 11c, 12, 13, 16, 19a-BC, 19b-ménages, 19b-banque, 20, 21 et 22. Une souscription primaire 19a-BC ne crée pas de monnaie centrale ; H ne naît que quand l'État dépense (l. 379) | Décision citant M22 |
| Résultat versé chaque tour | `sec:cadre-caisse` (l. 491-495) ; ADR 0005, pt 12 (lecture (d)) | Π^CB = i_B B_CB/n_a + i_CB L^CB/n_a − i_res Res/n_a, calculé en phase 1 et versé en 8 (b), sans troncature. Une perte est un versement négatif, soumis à la règle de caisse de l'État. E^CB reste à sa valeur initiale résolue. La troncature est réservée au J6 | Décision citant M22 |
| Compte du Trésor, pas d'avances | `sec:cadre-bilans` (l. 242, 247) ; `tab:instabilites` (l. 2316, 2336) | Le compte du Trésor est tenu à la banque centrale, sans intérêt. Les avances au Trésor sont absentes du socle : la seule porte de monnaie centrale vers l'État est l'achat de titres (instabilité 2 écartée par construction) | Décision citant M22 |
| Émission (α) | `sec:cadre-caisse` (l. 497-502) | L'État émet en phase 7 le besoin réalisé, Π^CB compris. M^{G*} est résolu par la fiche 9. L'émission n'est pas un levier du socle | Décision citant M22 |
| Phases | `tab:phases` (l. 529, 535, 536) ; ADR 0009 | Phase 1 : « moteur (leviers), travail, banque centrale ». Phase 7 : « État, banque, banque centrale », ordre à fixer par leurs fiches. Phase 8 : banque centrale en (a) et (b). Une variable d'état de bloc est écrite une fois par pas, dans une phase où le bloc siège après ses entrées, sinon en phase 9 | Décision citant M22 (et M29), et ADR |
| Salaires (M25) | `travail.md` § 6.3 (C1 à C8), § 8 ; `sec:travail` | Règle SN, coefficient 1 sur π^e : courbe de long terme verticale, U* = U^eq. π^e est lu à l'ouverture par le bloc 3 (lecture (a)). U^eq est un paramètre du bloc 3, lu à sa source | M25 |
| Prix (M26) | `prix.md` § 6.4 (C9 à C13) ; `sec:prix-conditions` | Option M : aucune anticipation consommée, aucun canal de coût du taux. Racine unitaire du niveau nominal. Le bloc 4 n'apporte pas de second ancrage | M26 |
| Ménages (M27) | `menages.md` § 6.3 et § 6.5 (C14 à C18, C26) ; `sec:menages-inflation` (l. 1450-1459) ; `sec:menages-conditions` | Les ménages lisent π*, jamais π̄ ni le registre (lecture (c)). B_H ≡ 0. Canal du taux rentier seul, de signe positif. Domaine du levier de cible : π* < 85,12 % par an à la calibration (l. 1459). Clause C26 | M27 |
| Investissement (M28) | `investissement.md` § 6.3 et § 6.6 (C32 à C37), § 8 ; `sec:investissement-conditions` (l. 1905) | S-ζ : canal permanent du taux par tu\*. ϱ_L = (1 + i_L)/(1 + π*) − 1 (S1). ϱ̄_L est une constante résolue, dont la source relève de #44. C36 dans la rédaction retenue par M28 | M28 |
| Banque commerciale (M31, à venir) | fiche 7, critères 2 et 4 | Transmission i_CB → i_L, i_D (lus au tour n + 1) ; règle du refinancement ; corridor (#26, pt 5) | M31 |
| Bornes | #38, lecture (ii) ; `CONVENTIONS.md` § 2.4 | « Le plancher à zéro d'un taux nominal est à seuil libre » : paramètre, motif et activité déclarés | Décision citant #38 |
| Statut des faits | P1 (03/10/2026) ; `CONTEXT.md` | Statuts S+O, O, R, L, V et V+O. L'état D1 n'est pas versé | — |

### 1.2 Ce que le bloc doit produire

Les symboles **ne sont pas fixés** (critère 22). Sont déjà pris :
- k (intrant) ;
- c (indice des pays) ;
- r (taux réel ex post, i − π) ;
- ρ̄_K et ρ̄_IN ;
- ν_H et ν_F ;
- ϱ_L.

| Grandeur | Définition | Unité | Dénominateur | Fenêtre |
|---|---|---|---|---|
| i_CB | Taux directeur, taux du refinancement (ligne 13), arrêté en phase 1 par le levier ou la règle | par an, taux de flux | — | phase 1 ; le tour |
| i_res | Taux des réserves (ligne 12) ; sa relation à i_CB (corridor) est déclarée | par an, taux de flux | — | phase 1 |
| Prescription de la règle | Taux qu'indique la règle au tour, restitué même quand le joueur fixe le taux (C9) | par an | — | phase 1 |
| π^e | Glissement annuel anticipé de P sur les 12 tours à venir ; variable d'état d'ouverture du bloc 8, lue par le bloc 3 (C5) | par an, taux d'inflation (G) | — | ouverture ; valeur stationnaire π̄ |
| Crédibilité (si l'option en a une) | Variable d'état ; valeur stationnaire explicite (C8) | sans dimension | — | ouverture |
| État de l'action intégrale | Taux naturel estimé, ou écart cumulé du niveau des prix à son sentier (C2) | par an ; ou points de log | — | ouverture ; valeur initiale r̄ |
| π*_{t+1} | Cible du pas suivant, écrite en phase 1 depuis le levier (ADR 0010, pt 3) | par an, taux d'inflation | — | phase 1 |
| Π^CB | Résultat de la banque centrale (l. 493), calculé en phase 1 | u.m. par pas | — | phase 1 ; versé en 8 (b) |
| Lignes 12 et 13 | i_res Res/n_a et i_CB L^CB/n_a, sur l'encours d'ouverture | u.m. par pas | — | phase 8 (a) |
| Lignes 19a-BC et 19b | Souscription primaire et achats décidés ; 19b-ménages nulle sous B_H ≡ 0 | u.m. par pas | besoin d'émission ; B_Bk | phase 7 |
| E^CB | Valeur nette, calculée deux fois | u.m. ; années de PIB | 12 × PIB nominal du pas | ouverture |
| H = Res | Monnaie centrale | années de PIB | idem | ouverture ; clôture |
| Taux réel | Forme lue par la règle (critère 5) ; forme restituée r = i − π (l. 214) | points par an | — | le tour |
| Écart d'inflation | π_{t−1} − π*_t ; écart du niveau des prix à son sentier, si la règle en lit un | points ; points de log | — | le tour |

### 1.3 Ce qu'il lit

- **Ouverture** :
  - le registre de l'indice des prix (P_{t−1}, π_{t−1}) ;
  - le chômage du tour précédent, U_{t−1}, depuis les variables du bloc 3 ;
  - ses variables d'état (π^e_t, crédibilité, état de l'action intégrale) ;
  - π*_t ;
  - les postes B_CB, L^CB, Res et M^G ;
  - i_B (bloc 9), qu'emploie Π^CB.
- **Phase 1** : les leviers du tour (taux directeur, cible, achats de titres, choix de suivre la prescription de la règle). Jamais W_t (C5), jamais p_t ni une grandeur du pas.
- **Phase 7** : le besoin d'émission (bloc 9), si la souscription 19a-BC en dépend, dans l'ordre de C25.
- **Phase 8 (a)** : les encours d'ouverture.
- **Décisions qui le contraignent** : M22 (ADR 0005) ; M24 (ADR 0007) ; M25 ; M26 (ADR 0008) ; M27 ; M28 ; M29 (ADR 0009) ; M30 (ADR 0010) ; décisions du 02/10/2026 sur #23 et du 03/10/2026 sur #38 ; M31 (fiche 7) quand elle sera prise.

### 1.4 Frontières

- **Travail et salaires, prix (fiches 3 et 4, `macro`) : frontière inflation.**
  - Chez `macro` : formation des salaires (SN) et des prix (M).
  - Chez `monnaie` : loi de π^e, crédibilité et règle de taux.
  - Critères 4, 8, 11, 12 et 14 (a) ; avis de `macro` au § 6.
- **Ménages et investissement (fiches 5 et 6, `macro`)** :
  - π* lue (M27, M28, M30) ;
  - canal taux → demande (C14, C34, C36) ;
  - superneutralité (C15) ;
  - délais (C16, C35) ;
  - changement de cible (C32, C33, #54).

  Critères 6, 11, 13, 14 et 16.
- **Banque commerciale (fiche 7, `monnaie`)** : transmission i_CB → i_L, i_D ; refinancement (ligne 21) ; corridor (#26, pt 5) ; achats à la banque (19b-banque). Critère 3.
- **État et dette (fiche 9, `macro` ; `monnaie` consulté) : fermeture du niveau d'activité et dette publique.** Ce qui revient à chaque fiche :
  - **#44** : la fiche 8 déclare si la fermeture est monétaire (r̄ résolu par l'action intégrale, C2 et C3) et écrit r̄ dans l'état initial ; la fiche 9 déclare si elle est budgétaire. La déclaration est commune (paire M32-M33) ; le script d'état stationnaire de la branche n° 4 bis la résout ;
  - **C36** : critère de la fiche 8 (gain statique, point fixe, arrivée, aucune rampe), jugé avec la règle de la fiche 9 ;
  - **C37** (reprise du surcroît d'intérêts) et **C23** (règle face à la charge d'intérêts) : fiche 9 ;
  - **C25** (ordre de la phase 7) : la fiche 9 l'écrit ; la fiche 8 déclare ses décisions 19a-BC et 19b et leur place dans cet ordre ;
  - **#56** : propriété attendue écrite par `monnaie` et `macro` (critère 15), essai au J4 ;
  - **#26, point 1** : la fiche 8 nomme la ligne de la perte non payée de la banque centrale ; la fiche 9 fixe la règle de caisse de l'État et la recapitalisation. **#26, point 3** (M^{G*}) : fiche 9 ;
  - **i_B** : règle et date de fixation à la fiche 9. Contrainte du cadre : Π^CB, calculé en phase 1, lit i_B. Si i_B suit i_CB du tour, il est écrit en phase 1 par un bloc qui y siège. Le bloc 9 n'y siège pas : options, qualifications d'`architect` et recommandation commune (i) au critère 4 (f) (amendé le 04/10/2026), choix à M33 ;
  - avances au Trésor et dominance budgétaire (Sargent et Wallace, 1981) : absentes du socle. Le financement des intérêts par le déficit est un régime déclaré (C37), non une référence.
- **`jeu`** : critères 16 et 19 ; avis au § 7.

### 1.5 Ce que la fiche ne tranche pas, et questions ouvertes

**Hors du périmètre** :
- les régimes de souveraineté B à E et le change (J5 ; #64) ;
- l'hyperinflation, la fuite devant la monnaie, la réforme monétaire et l'économie effondrée (J6 ; C18 ; v1.5 `eq:reform`) ;
- les billets et les avances au Trésor (absents) ;
- la calibration (J3 ; #45, #55, #62) ;
- les bandes du test zéro : proposées ici, confirmées avec O1 avant l'essai (M19).

**Questions ouvertes à instruire** :
- **Q1 — Règle de taux** (C2, C6, C10) : forme (règle de Taylor ; action intégrale sur l'écart d'inflation ; terme de niveau des prix) ; mesure lue ; terme d'activité ; lissage ; plancher.
- **Q2 — Loi des anticipations** (C1, C4, C5, C7, C12) : forme adaptative ou hybride (v1.5, v2.0), apprentissage à gain constant, ancrage sous C2 ; phase de formation ; gain.
- **Q3 — Crédibilité** (C8) : présente ou non ; forme ; valeur stationnaire.
- **Q4 — Cible** (#54, #61) : levier ou paramètre ; domaine ; effet d'un changement (C33). Avis concordants de `jeu` et `monnaie` : π* paramètre au socle, levier au J4 seulement après le verdict de #54 (critère 16) ; un délai d'annonce de plus d'un tour modifierait l'ADR 0010 (signalé, non proposé).
- **Q5 — Corridor et i_res** (#26, pt 5).
- **Q6 — Bilan de la banque centrale** (#26, pts 1 et 2).
- **Q7 — Achats de titres** (C17) : 19a-BC et 19b-banque ; comme leviers, nuls au socle, renvoyés au J6 avec une prime de terme ou de risque (avis de `jeu`, accepté par `monnaie`) ; la part s_CB (A8) reste un paramètre de l'archétype, non un levier.
- **Q8 — Fermeture du niveau d'activité** (#44).
- **Q9 — Forme du taux réel** (#49).
- **Q10 — Clause II.7** (C10) et clause analogue de l'ADR 0010.
- **Q11 — Variantes à instruire** :
  - **A (v1.5)** :
    - `eq:taylor` (l. 1016-1024), taux naturel estimé intégral écrêté à [−0,01 ; 0,06] (l. 1020) ;
    - `eq:expect` (l. 1149) et `eq:cred` (l. 1150-1151) ;
    - bilan, `eq:ecb` (l. 998-1005) ;
    - leviers de l'encadré « joueur » (l. 984-991).
  - **B (v2.0)** :
    - taux naturel `anchored`, intégrateur à fuite dans une bande de ±0,01 (`policies.py` l. 55-63) ;
    - π^e (`model.py` l. 1300) ;
    - crédibilité (l. 1305-1308).

    Profil D1 (faits § 1.1) : `rstar_mode='anchored'`, `rstar_anchor='deposit_wedge'`, `rstar_band=0,01`, `rho_i=0,7`. Le défaut de `Params` est `rstar_mode='legacy'` (l. 290).
  - **C (nouvelle)** : règle à action intégrale sans fuite (C2), avec une loi d'apprentissage à gain constant (piste de la feuille de route § 5). Référence candidate : Evans et Honkapohja (2001), *Learning and Expectations in Macroeconomics*, Princeton University Press (existence vérifiée, contenu non lu).
  - **D (nouvelle)** : corridor explicite (piste § 5), avec la fiche 7.
  - **Une variante sans retard** comme référence (`docs/exigences.md` § 2.7).

### 1.6 Conditions et issues reçues : traitement

| Élément reçu | Source | Traitement | Où | Raison |
|---|---|---|---|---|
| C1 — aucune erreur d'anticipation stationnaire | fiche 3 § 6.3 | retenu | critère 8 (a) | Verticalité de SN ; sinon U* dépend de λ_w (fiche 3, critère 4) |
| C2 — action intégrale sans fuite, fait nouveau contre l'instabilité 4 | fiche 3 § 6.3 | retenu | critères 6 (a), 11 (a) | π̄ = π* quel que soit r̄ ; instabilité 4 |
| C3 — état initial résolu | fiche 3 § 6.3 | retenu | critère 6 (b) | Exigence d'un état initial résolu (`docs/exigences.md` § 2.6) |
| C4 — lecture (G), cible comparée au glissement | fiche 3 § 6.3 ; ADR 0008, I | retenu | critères 5 (a), (d), 8 | M25 (b) |
| C5 — π^e variable d'état d'ouverture ; jamais W_t | fiche 3 § 6.3 | retenu | critères 4 (a), 8 (b) | Lecture (a) de M25 |
| C6 — terme d'activité sur U^eq, sans coefficient d'Okun importé | fiche 3 § 6.3 | retenu | critère 4 (e) | Source unique de U^eq |
| C7 — calibration conjointe de λ_e et de λ_w·β ; ratio de sacrifice restitué | fiche 3 § 6.3 ; #45 | retenu : gain déclaré ici, calibré au J3 | critères 8 (d), 19 (a) | #45 rangée au J3 |
| C8 — crédibilité à valeur stationnaire explicite ; pas de loi à seuil ; intention du mainteneur à reconfirmer | fiche 3 § 6.3 | retenu | critères 9, 10 | Loi K1a (`model.py` l. 1305) ; intention du 17/09/2026 |
| C9 — même information que le joueur ; prescription restituée | fiche 4 § 6.4 | retenu | critères 4 (a), 19 (a) | ADR 0008, II.2 |
| C10 — contenu du fait nouveau de C2 ; clause II.7 | fiche 4 § 6.4 ; ADR 0008, II.7 | retenu | critères 11 (b), 12 | Clause de M26 |
| C11 — retour du niveau des prix | fiche 4 § 6.4 | retenu, soumis à `jeu` | critère 6 (e) | Dépendance à l'histoire visible par le joueur |
| C12 — phase de formation de π^e (condition de Barro et Gordon) | fiche 4 § 6.4 | retenu | critère 8 (c) | Délai prix → anticipation → salaire de 1 ou 2 tours |
| C13 — ni canal direct π^e → p, ni canal de coût | fiche 4 § 6.4 | retenu | critère 14 (a) | M26 |
| C14 — condition de signe | fiche 5 § 6.3 | retenu | critère 11 (c) | Canal rentier positif (fiche 5) |
| C15 — superneutralité | fiche 5 § 6.3 | retenu, avec #49 | critère 13 | Tolérance fixée ici, avant l'essai |
| C16 — élasticités et délais des ménages | fiche 5 § 6.3 et § 6.5 | retenu comme entrée | critères 11 (a), 14 (f) | — |
| C17 — assouplissement quantitatif à la banque seule | fiche 5 § 6.3 | retenu, déclaré à `jeu` | critère 14 (g) | B_H ≡ 0 |
| C18 — haute inflation, fuite des dépôts | fiche 5 § 6.3 et § 6.5 | transmis au J6 | § 1.5 | Exige un actif de fuite absent du socle |
| C26 — réouverture de la Q10 de la fiche 5 vers (b) | fiche 5 § 6.5 | retenu comme clause | critère 11 (d) | Décision citant M27 (et M28) si elle joue |
| C32 — une seule lecture de l'inflation | fiche 6 § 6.3 | retenu | critère 14 (b) | M27 et M28 |
| C33 — effets d'un changement de cible | fiche 6 § 6.3 | retenu (déclaration) | critère 14 (c) | Signes opposés sur l'investissement et la consommation |
| C34 — canaux du taux déplacés ensemble | fiche 6 § 6.3 | retenu | critères 11 (c), 14 (d), 15 | Le plan seul ne suffit pas |
| C35 — délais | fiche 6 § 6.3 et § 9.10 | retenu (forme révisée sous le délai d'un tour de M30) | critère 14 (e) | — |
| C36 — gain statique et stationnarité de l'action intégrale | fiche 6 § 6.3, § 6.6 et § 8 (rédaction retenue par M28) | retenu ; jugé avec la règle de la fiche 9 | critère 6 (d) | Parenté avec l'instabilité 4 |
| ADR 0010, pt 3 ; #61 — le bloc 8 écrit π*_{t+1} en phase 1 | ADR 0010 ; #61 | retenu ; le reste de #61 (forme dans `moteur/` et `etat/`) relève du J2 et du J3 | critère 4 (c) | Contrat accepté (M30) |
| ADR 0010, condition de réouverture (délai d'un tour de la cible) | ADR 0010 | retenu en mesure, sous la forme du critère II.7 | critère 12 | Ajout proposé par `monnaie` |
| #24, volet « banque centrale » | #24 | retenu ; la session ferme #24 après le jalon 4 si la fiche répond | critère 5 (a), (b) | Volet « prix » tranché par M25 (b) et M26 |
| #49 — forme du taux réel | #49 | retenu ; fermée si la fiche tranche la forme, sinon ouverte jusqu'au test de C15 (J3) | critères 5 (c), 13 | Trois formes coexistent déjà (critère 13) |
| #54 — essai d'aller-retour de la cible | #54 | retenu : critères écrits ici ; essai par maquette au jalon 2 si π* est un levier, sinon au J3 ou au J4 | critère 16 | Exclure une stratégie dominante |
| #64 — π* lue au socle et C26 | #64 | retenu pour le régime A ; régimes B, D et E transmis au J5 | critères 5 (e), 11 (d) | Pas de cible propre hors du régime A |
| #44 — variable de fermeture du niveau d'activité | #44 | retenu, avec la fiche 9 ; se ferme à la branche n° 4 bis | critère 6 (c) | P16 (a) |
| #26, point 1 — perte non payée (côté banque centrale) | #26 | retenu ; recapitalisation à la fiche 9 | critère 2 (b) | Règle de caisse du cadre (l. 481) |
| #26, point 2 — E^CB sous croissance nominale | #26 | retenu ; bandes du test zéro avec `macro` | critère 2 (a) | Le ratio n'est pas stationnaire sous M22 (d) |
| #26, point 5 — corridor | #26 | retenu, coordonné avec la fiche 7 | critère 3 | L'arbitrage dépend de i_res et de la règle de la banque |
| #56 — signe net d'une hausse de taux | #56 | retenu : propriété attendue écrite ici, texte commun de `monnaie` et `macro` au critère 15 de la fiche 8 ; essai au J4 | critère 15 | Le résultat de maquette dépend de la règle budgétaire |
| #45 — gain d'apprentissage | #45 ; C7 | gain déclaré ici, calibration transmise au J3 | critère 8 (d) | — |
| Pistes « corridor explicite » et « apprentissage à gain constant » | feuille de route § 5 | options à instruire | § 1.5, Q11 ; critères 3 (c), 8 (e) | — |
| Défauts de la v2.0 : inflation de référence à 4 %, crédibilité nulle sur 60 ans, taux réel à 5 % | `archive/faits_mesures_G_K.md` § 2 et § 4 | retenus comme exigences négatives | critères 6 (a), 9 (c), 10 (b) | Intégrateur à fuite et loi à seuil |

## 2. Critères d'évaluation, écrits avant l'instruction

**Statut** : proposés par `monnaie` le 04/10/2026, **validés par le mainteneur le 04/10/2026**, avec les amendements ci-dessous (jalon 1 de #72), avec ceux des fiches 7 et 9 (P14). La liste est fermée : elle ne se déplace pas après observation (`docs/exigences.md` § 2.5). Un amendement adopté avant l'instruction se consigne sous le tableau. Seuils reconduits des fiches 2 à 6, à confirmer :
- 1e−10 en relatif ;
- 0,48 ms par pays-pas ;
- 12 tours pour la désactivation d'une borne.

Les seuils de C36 sont repris tels que M28 les a retenus.

Correspondance avec le gabarit :

| Critère du gabarit | Critère de la fiche |
|---|---|
| 1 | 1 (et 2) |
| 2 | 6 et 7 |
| 3 | 11 (et 12) |
| 4 | 21 |
| 5 | 19 |
| 6 | 18 et 20 |

Critères propres au bloc : 2 à 5, 8 à 10, 12 à 17, 22 à 24.

Sont des **exigences** (ils peuvent écarter une option) :
- 1 à 9 ;
- 10, sous réserve de la reconfirmation de l'intention du mainteneur ;
- 11 (a), (c) et (d) ;
- 12 (procédure et verdict) ;
- 13 ;
- 14 (a) à (e) et (g) ;
- 15, exigence au J4 avant l'ouverture du levier de taux ;
- 16 (verdict) ;
- 17, 18 ;
- 19 (b) ;
- 20 (sans historique ni drapeau) ;
- 21 (sans itération) ;
- 22 et 24.

Sont des **mesures** :
- 11 (b), dont la période et la demi-vie ;
- les grandeurs publiées du critère 12 ;
- 14 (f) ;
- 19 (a), (c), (d) et (e) ;
- 20 et 21 (décomptes) ;
- 23.

| N° | Critère | Ce qui est attendu (seuil ou forme du verdict) | Par quoi on le vérifie | Qui | Quand |
|---|---|---|---|---|---|
| 1 | Cohérence stock-flux (gabarit 1 ; `monnaie`) — **exigence** | (a) **Lignes proposées** par le bloc : 12 et 13 en 8 (a) ; 16 en 8 (b) ; 19b-banque en phase 7 ; 19a-BC proposée par le bloc 9 (A8) ou par le bloc 8, tranché à M31-M33 ; dans le premier cas, le bloc 8 écrit en phase 1 sa part s_CB du besoin (19b-ménages nulle sous B_H ≡ 0). **Propriétaire des lignes 19a, à trancher par le mainteneur (choix à M33)** : (A8) le bloc 9 propose les trois lignes 19a, la part s_CB étant écrite par le bloc 8 en phase 1 et la banque retirée de la phase 7 — recommandée par `monnaie` et `macro` ; **modification** (`temps_comptabilite.md:838`, ADR 0009 l. 84 : décision citant M22 et M29, ADR d'architecture) ; (variante) chaque détenteur propose sa part, le bloc 9 publie le besoin, ordre État → banque centrale → banque fixé par les fiches — **interprétation**, note à la table de la fiche 1. La propriété de 19a-banque dans M31 reste conditionnelle. **Lignes reçues** : 11c (bloc 9) ; 21 (bloc 7) ; 20 et 22, contreparties de règlement. Signatures de `tab:portes-monnaie` inchangées. Toute ligne nouvelle (avances au Trésor, part non payée, recapitalisation, réserves obligatoires) est un contrat partagé : décision citant M22. (b) **Π^CB** est calculé en phase 1 selon l. 493, sur des encours d'ouverture et des taux de la phase 1, jamais sur une grandeur intra-pas (l. 495). E^CB est calculé deux fois, par le stock (l. 255) et par les flux (Π^CB − ligne 16). Aucun poste n'est obtenu par différence (défaut v2.0 : fonds propres de la banque centrale posés égaux à actifs − passifs, ADR 0005, Contexte). (c) **Contrainte budgétaire de la banque centrale**, écrite sur un pas depuis sa colonne de `tab:matrice-flux` : ΔB_CB + ΔL^CB = ΔRes + ΔM^G + Π^CB − ligne 16, avec ΔB_CB = ΔB_CB^prim + ΔB_H^sec + ΔB_Bk^sec | Matrice des flux de l'option ; cas à la main sur un pas où i_CB monte d'un point et la banque centrale achète x u.m. de titres à la banque (lignes 12, 13, 16, 19b-banque, 20, 21, 22 ; E^CB par le stock et par les flux). Si une table change : `uv run python outils/verifier_matrices.py --strict <copie>`, sortie citée avant et après | `monnaie` | fiche ; J3 (identités, ε = 1e−12 × S^CB) |
| 2 | Bilan de la banque centrale : fonds propres et perte (#26, pts 1 et 2 ; `monnaie` ; `macro` pour les bandes) — **exigence** | (a) **#26, point 2** : sous M22 (d), E^CB reste à sa valeur initiale. E^CB/(12 PIB) décroît donc au rythme de la croissance nominale : il ne vaut plus que 0,0929 de sa valeur initiale après 60 ans à g = π̄ = 2 %, 0,3048 à π̄ = 0 et 0,0010 à π̄ = 10 % (calcul [(1 + g)(1 + π̄)]^{−60}). La fiche retient l'une de trois formes, avec son effet sur le test zéro. La forme (i) n'est admise que si chaque ratio qu'elle fait dériver (dette au numérateur du test zéro, Res, L^CB, H) reste dans sa bande sur 720 pas, dérive chiffrée avant l'essai ; sinon, forme (ii), E^CB_0 = 0, seule valeur stationnaire sous M22 (d), un poste déclaré étant résolu en conséquence. (i) ratio déclaré non stationnaire, sa dérive sur B − M^G au PIB (identité du critère 5 (b) de la fiche 9) et sur L^CB ou Res au PIB chiffrée sur 720 pas et portée dans les bandes du test zéro avec `macro` ; si (i) était retenue, la dette nette de la fiche 9 perdrait E^CB_0 × (1 − 0,0929)/(12 PIB_0) en 60 ans à g = π̄ = 2 % ; (ii) E^CB_0 = 0, seule valeur dont le ratio est stationnaire sous M22 (d) ; un poste déclaré (par exemple B_CB,0) est résolu en conséquence ; (iii) rétention d'une part du résultat, décision citant M22 (d). Recommandation commune de `monnaie` et `macro` : (ii) ; choix à trancher par le mainteneur. (b) **#26, point 1** : une perte (Π^CB < 0) que le compte du Trésor ne couvre pas en 8 (b) a une **ligne nommée** (rationnement déclaré du versement, avec l'effet sur E^CB) ou une règle de recapitalisation, décidée avec la fiche 9. La fiche dit si le cas peut se produire sous la position α hors d'un placement raté. Identité : Π^CB = [i_CB(E^CB + M^G) + (i_CB − i_res)Res + (i_B − i_CB)B_CB]/n_a, sur les encours d'ouverture. Π^CB ≥ 0 si i_B = i_CB, i_res ≤ i_CB, plancher de i_CB ≥ 0 (critère 18 (a)) et E^CB ≥ 0. La fiche dit laquelle de ces conditions l'option viole, s'il y en a une ; une variante de durée (critère 10 de la fiche 9) rend i_B ≠ i_CB et rouvre le point 1 de #26 | Formes fermées ; cas à la main (placement raté, perte) | `monnaie` ; `macro` (bandes, identité de la dette) | fiche ; J3 |
| 3 | Corridor et taux des réserves (#26, pt 5 ; piste « corridor explicite » ; `monnaie`) — **exigence** | (a) La relation entre i_res et i_CB est déclarée : égalité ; écart fixe i_res = i_CB − Δ^res, Δ^res ≥ 0 déclaré (v1.5 l. 984 et 997) ; ou autre. La fiche dit quel taux est le levier « taux directeur ». (b) **#26, point 5** : aucun arbitrage « emprunter au taux i_CB pour placer en réserves rémunérées ». Soit la règle de refinancement de la fiche 7 le borne (critère 2 (c) de la fiche 7), soit i_res ≤ i_CB est exigé ici. Le verdict cite la décision M31. (c) La piste « corridor explicite » est instruite avec la fiche 7 (option D) et sa référence lue. (d) H/(12 PIB) stationnaire et le signe stationnaire de Π^CB sont écrits en forme fermée, et L^CB/(12 PIB), en fonction de M^{G*}/PIB (fiche 9, critère 11) : chaque impôt draine des réserves vers M^G ; bilan de la banque centrale, Res − L^CB = B_CB − M^G − E^CB, d'où, sous Res·L^CB = 0 et E^CB = 0, L^CB = max(M^{G*} − B_CB ; 0) et Res = max(B_CB − M^{G*} ; 0). Sans titres à la banque centrale, H = 0 (bande H du critère 17, amendement A9) | Formes ; cas à la main | `monnaie` | fiche |
| 4 | Contrats hérités, phases et lectures (§ 1.1 ; C5, C6, C9 ; ADR 0008, II.2 ; ADR 0010, pt 3 ; #61 ; `monnaie`, `macro` pour (d) et (e)) — **exigence** | (a) La règle lit en phase 1 l'état d'ouverture : π_{t−1} et P_{t−1} (registre ; ADR 0008, II.2 et II.6), U_{t−1}, π^e_t, π*_t et ses variables d'état. Elle ne lit jamais W_t, ni p_t, ni aucune grandeur du pas (C5). Elle dispose de la même information que le joueur, et sa prescription est restituée (C9). (b) i_CB et i_res sont arrêtés en phase 1 et portent les lignes 12 et 13 du tour (délai du premier flux nul, ADR 0005, pt 11). Π^CB est calculé en phase 1 (l. 495). (c) **ADR 0010, pt 3 (#61)** : le bloc 8 écrit π*_{t+1} en phase 1, une fois par pas, depuis son levier ; l'interface de lecture des blocs 5 et 6 et `tab:phases` sont inchangées ; le moteur cesse d'être propriétaire provisoire. (d) **Ordre de la phase 1** (`tab:phases` l. 529, « moteur (leviers), travail, banque centrale ») : s'il forme π^e avant la règle (C12), le bloc 8 le déclare comme ordre interne au bloc, sans ordre nouveau entre blocs. Le bloc 3 lit π^e à l'ouverture (lecture (a), M25). (e) **C6** : un terme d'activité éventuel s'écrit a_U(U^eq − U_{t−1}), avec U^eq lu au bloc 3. Aucun coefficient d'Okun importé (fiche 3 § 6.1, Q6 : la v2.0 prenait `okun` = 2 quand M24 donne dU/d ln y = −0,95). Aucun chômage hystérétique (hypothèse réfutée 7). (f) **i_B** : sous l'option (i) de la fiche 9 (critère 13 (c)), Π^CB lit i_CB de la phase 1 et aucun bloc n'écrit i_B ; sous (ii), i_B se déduit de i_CB en phase 1 par la même lecture ; sous (iii), Π^CB lit le i_B d'ouverture. La prime i_B − i_CB est déclarée : nulle au socle, ou paramètre déclaré ; une prime endogène relève du J6. Option (β), le bloc 9 écrit i_B en phase 1 : **modification** (cycle bloc 8 → 9 → 8 en phase 1 ; décision citant M22, M29 et M30, ADR d'architecture). Qualifications d'`architect` : (i) est une **interprétation**, `tab:phases` inchangée, à condition d'être déclarée une seule fois dans `sec:finances_publiques` comme identité de notation du socle, sans label `eq:` ni équation exécutée, tout lecteur lisant i_CB ; (iii) contredit probablement la l. 483 (hypothèse à vérifier). Recommandation commune de `macro` et `monnaie` : (i). Choix à M33, **à trancher par le mainteneur**. (g) Phase 7 : les décisions 19a-BC et 19b prennent place dans l'ordre de C25. (h) La matrice des lectures reste triangulaire | Tableau phase → lit / écrit pour les phases 0, 1, 7, 8 et 9, avec les blocs 3, 5, 6, 7 et 9 ; triangularité vérifiée à la main | `monnaie` ; `macro` ((d), (e)) | fiche ; J2 |
| 5 | Mesure de l'inflation, cible et taux réel (#24, volet « banque centrale » ; #49 ; C4 ; #64 pour le régime A ; `monnaie`) — **exigence** | (a) **#24** : la cible se compare au glissement annuel du registre, π_{t−1}, sans conversion (lecture (ii) de #24, sous (G)). Toute mesure d'une inflation par pas s'annualise géométriquement (l. 202). (b) **Glissement stationnaire, calculé à la main** : sous C2, π̄ = π*. À π* = 2 %, le facteur par pas vaut (1,02)^{1/12} = 1,00165158 et le glissement 2,0000 %. Une cible convertie linéairement (lecture (i) de #24, écartée par M25 (b)) donnerait 2,0184 % ; à π* = 10 %, 10,4713 % au lieu de 10 % (commande au compte rendu du 04/10/2026). (c) **#49, forme du taux réel lu par la règle**, déclarée parmi : (i) r = i − π (cadre, l. 214) ; (ii) rendement réel exact d'un encours rémunéré linéairement, n_a ln(1 + i/n_a) − ln(1 + π) ; (iii) taux de Fisher annuel, (1 + i)/(1 + π) − 1 (forme de S1, bloc 6). Écarts remesurés : la forme (ii) dépasse r = i − π de 0,0131 point à i = 4 %, π̄ = 2 %, et de 0,4094 point à i = 12 %, π̄ = 10 % (n_a = 12). Si l. 214 change, décision citant M22 (ADR 0005, pt 5). La tolérance de C15 en découle (critère 13). (d) **C4** : π^e est un glissement anticipé, en lecture (G). Le stockage de ln(1 + π^e) est examiné (domaine π^e > −1 par construction). (e) **Régime A (#64)** : la cible lue par les blocs 5 et 6 est la cible en vigueur π*_t du pays (ADR 0010). Les régimes B, D et E sont renvoyés au J5 | Calcul à la main ; formes écrites | `monnaie` ; `macro` (avis sur (c)) | fiche |
| 6 | Action intégrale, état stationnaire et fermeture (gabarit 2 ; C2, C3, C11, C36 ; #44 ; `monnaie`, `macro` pour (c) et (d)) — **exigence** | (a) **C2** : π̄ = π* dans tout état stationnaire, indépendamment de r̄ et des vitesses, démontré à la main pour chaque option. Contre-exemples à chiffrer : règle de Taylor à taux naturel fixe, π̄ − π* = (r̄ − r*)/a_π ; intégrateur à fuite de la v2.0 (`policies.py` l. 62-63, L), π̄ − π* = (r̄ − ancre)/(a_π + gain), fonction d'un rapport de vitesses (fiche 3 § 6.1, Q5). (b) **C3**, état initial résolu : r*_0 = r̄ ; π^e_0 = π̄ = π* ; i_0 = r̄ + π̄ dans la forme du taux réel du critère 5 ; crédibilité à sa valeur stationnaire à écart nul. Condition d'existence déclarée, r̄ + π* ≥ plancher du taux ; sinon la résolution échoue de façon visible. (c) **#44, avec la fiche 9** : la variable de fermeture du niveau d'activité est déclarée. Deux lectures (fiche 6 § 9.3) : (1) r̄ paramètre et position budgétaire résolue ; (2) r̄ résolu à G/PIB donné. ϱ̄_L s'en déduit par l'écart de la fiche 7. Forme fermée écrite pour le script de la branche n° 4 bis. Le comptage est commun avec la fiche 9 (critère 4 (b)) : tableau « équation stationnaire → grandeur qu'elle détermine » pour les blocs 2 à 9, rang plein exigé. **Une seule action intégrale par condition stationnaire** : sous la verticale de M25, tout état stationnaire a U = U^eq ; une action intégrale budgétaire sur l'écart d'activité laisse une racine unitaire quelle que soit la règle de taux (avec C2 : continuum (r̄, G/PIB) ; avec r* paramètre : π̄ ≠ π* en plus). Une option qui les cumule est écartée (fiche 9, critère 6 (b)). La persistance de la fiche 9, critère 6 (d) (écart de production sous la moitié de son pic en au plus 60 tours après une dépense publique +1 % aux tours 1 à 12), est mesurée sur la même maquette, sous la règle de taux de chaque option. Sous C2, les lectures (1) et (2) sont deux inversions de calibration d'une même fermeture monétaire : après un choc permanent, r̄ se déplace et G/PIB reste à son paramètre. Une fermeture budgétaire dynamique exige que l'action intégrale passe de la règle de taux à la règle budgétaire (critère 6 (a) (ii) de la fiche 9), ce qui rouvre M25 (porteur de C2). Aucune action intégrale budgétaire sur l'activité n'est compatible avec ce critère (maquette du 04/10/2026, commande au compte rendu). (d) **C36**, dans la rédaction retenue par M28 (`sec:investissement-conditions` l. 1905) : (i) gain statique de la demande totale au taux réel strictement négatif, tous canaux réunis ; (ii-a) r̄ et π̄ résolus par point fixe, identiques à 1e−6 près en relatif dans les branches ×0,5 et ×2 de toutes les vitesses, avec π̄ = π* ; (ii-b) après une dépense publique accrue de 1 % de façon permanente, arrivée simulée à moins de 1e−3 en au plus 20 demi-vies de la racine dominante ; (iii) aucune rampe : module dominant inférieur à 1 hors de la racine nominale et de tout état inerte déclaré, et (ii-b) satisfait. Jugé avec la règle de référence de la fiche 9 (C37). Maquette avec ζ ∈ {4 ; 8} (ordre de grandeur retenu à M28, hypothèse). « Dépense publique accrue de 1 % » s'entend d'un déplacement de l'ancre de dépense de la règle budgétaire de référence, ou du levier de dépense si la règle n'en a pas, défini une fois pour les fiches 6, 8 et 9. Un « état inerte déclaré » ne peut être aucune grandeur qui entre dans un ratio testé : une racine unitaire sur un tel ratio est un continuum. (e) **C11** : retour du niveau des prix écrit pour l'option. Si r̄ est inchangé après un choc, P revient sur son sentier ; si r̄ se déplace de Δr̄, le niveau est déplacé de Δr̄/(gain intégral) (fiche 4 § 6.3). Déclaré et soumis à `jeu` | Calcul à la main ; maquette pour (d) (commande et sortie citées) | `monnaie` ; `macro` ((c), (d)) | fiche ; branche n° 4 bis ((c)) ; J3 |
| 7 | Aucune vitesse ne détermine l'état d'arrivée (gabarit 2 ; `docs/exigences.md` § 2.7 ; `monnaie`) — **exigence** | (a) Aucune vitesse de la règle (a_π, gain intégral, lissage), de la loi d'anticipation (λ_e) ou de la crédibilité, ni la durée du pas, n'apparaît dans les formes fermées du critère 6. (b) **Forme de l'essai** : les demi-vies mesurées en maquette pour l'action intégrale vont de 218 à 632 tours (fiche 6 § 6.6, résultats de maquette). Une simulation de 720 pas ne peut donc pas tenir 1e−6. Sur la maquette conjointe (A4), puis au J3, dans chaque branche où une vitesse ou un gain est ×0,5 et ×2 (λ ≤ n_a) : (i) **point fixe** résolu, identique entre branches à 1e−6 près en relatif, avec π̄ = π* ; (ii) **module dominant < 1**, hors racine nominale et hors état inerte déclaré, aucun n'entrant dans un ratio testé ; (iii) **arrivée simulée** après chacun de trois chocs — dépense publique +1 % aux tours 1 à 12 ; marche de π* de +1 point ; π^e +1 point au tour 0 — : écart relatif de chaque ratio au point fixe de sa branche, et entre branches, d'au plus **1e−6 après H = max(720 ; 20 demi-vies de la racine dominante mesurée) pas**, H déclaré avant l'essai ; (iv) après une dépense publique +1 % permanente, arrivée au point fixe déplacé à moins de 1e−3 en au plus 20 demi-vies (C36 (ii-b), rédaction de M28). Le choc « dépense publique » est un déplacement de l'ancre de dépense de la règle de référence, ou du levier, défini une fois pour les fiches 6, 8 et 9. L'amendement de la fiche 6 (2 160 pas) reste en vigueur. Lieu d'exécution des simulations à horizon H (CI, job séparé ou hors CI, sortie publiée) fixé au plan de J3 (`architect` : au plafond de 52/12 ms par pays-pas, H = 12 640 pas coûte 54,8 s par simulation) | Calcul à la main ; au J3, script contre moteur | `monnaie` | fiche ; J3 |
| 8 | Anticipations (C1, C4, C5, C7, C12 ; #45 ; piste « apprentissage à gain constant » ; `monnaie`, `macro` pour (c)) — **exigence** | (a) **C1** : π^e = π̄ dans tout état stationnaire, pour toute valeur des paramètres de la loi, démontré à la main. Contre-exemple : loi de la v2.0 (`model.py` l. 1300, L), π^e = 2,200 % pour π̄ = 3 %, π* = 2 %, λ = 0,2, cred = 0,8 (fiche 3 § 6.1, Q1, calcul de la fiche). Un terme d'ancrage vers π* n'est admis que si C2 garantit π̄ = π*. Le terme quantitatif υ(g_M − g_Y − π^e) (v1.5 `eq:expect` l. 1149 ; v2.0 `ups`) est examiné : n'est-il sans erreur stationnaire que si M/PIB est stationnaire ? (b) **C5** : π^e est une variable d'état d'ouverture du bloc 8, lue par le bloc 3. Unité : par an, glissement anticipé sur 12 tours. Valeur stationnaire : π̄. (c) **C12** : phase de formation déclarée parmi les trois de la fiche 4 (§ 6.4), avec le délai prix → anticipation → salaire (1 ou 2 tours). Condition de Barro et Gordon : la π^e consommée au tour n ne lit aucun levier du tour n (Barro et Gordon, 1983, *JPE* 91(4), 589-610 ; résumé du document NBER w0807 lu, fiche 4 § 6.1). Une formation après la phase 5 (groupe de la phase 9) retouche `tab:phases` : décision citant M22 et M29, et ADR. (d) **C7, #45** : gain λ_e déclaré (par an, vitesse, conversion linéaire, λ_e ≤ n_a), calibré au J3 avec λ_w·β sur un ratio de sacrifice sourcé. L'approximation 1/(λ_e λ_w β) point-année de chômage par point de désinflation (fiche 3 § 6.1, Q7) est publiée pour chaque option. (e) **Piste « apprentissage à gain constant »**, instruite comme option (Evans et Honkapohja, 2001). Sa propriété stationnaire (convergence de l'estimateur vers π̄ dans un état stationnaire déterministe) est démontrée dans la fiche, non citée de mémoire | Démonstrations ; calcul à la main | `monnaie` ; `macro` ((c), délai salarial) | fiche ; J3 ((d)) |
| 9 | Crédibilité (C8 ; `monnaie`) — **exigence** | (a) Si l'option a une crédibilité, sa valeur stationnaire est explicite à écart nul et indépendante des vitesses. (b) Elle n'a aucun effet stationnaire (C1) : elle n'agit qu'en transition. (c) **Aucune loi à seuil sans fait nouveau** : loi K1a de la v2.0 (`model.py` l. 1305, L ; bonus seulement si l'écart est inférieur à 1 point) et v1.5 `eq:cred` (l. 1150-1151). Faits : crédibilité nulle sur 3 120 semaines dans le contrôle de D1 (O) ; la loi prédit exactement les valeurs mesurées en K1 (O), « la crédibilité est un relais, pas le verrou » (`archive/faits_mesures_G_K.md` § 4, K1a). (d) Bornes : clip à [0 ; 1], contrainte de domaine si la crédibilité est un poids. Le plafond 1 − ν_9 M^hist (v1.5 l. 1151 ; v2.0 l. 1306) relève de la réforme monétaire (J6) : écarté du socle ou déclaré. (e) L'option « sans crédibilité » est instruite comme comparaison (principe de simplicité). (f) Pour `jeu` : la crédibilité, si elle est retenue, est un indicateur visible ; son gain et sa perte sont perceptibles ; aucun piège irréversible sans signal | Formes fermées ; calcul à la main | `monnaie` ; `jeu` ((f)) | fiche |
| 10 | Effet de long terme de la politique monétaire sur l'inflation (intention du mainteneur du 17/09/2026, **à reconfirmer** ; C8 ; `monnaie`) — **exigence** si l'intention est reconfirmée | (a) Le mainteneur reconfirme, à la validation de ces critères, qu'une politique monétaire sans effet de long terme sur l'inflation est un défaut ; au socle, l'effet passe par la cible et par le taux, la monnaie étant endogène. (b) Si c'est reconfirmé : (i) une cible relevée d'un point de façon permanente relève π̄ d'un point, à 1e−6 près au point fixe, avec U* inchangé (verticalité, M25), la masse monétaire croissant à M/PIB stationnaire ; (ii) un taux directeur tenu durablement par le joueur sous r̄ + π* (règle désactivée) écarte le glissement de π* vers le haut, symétriquement vers le bas au-dessus ; signe et tour du premier écart publiés. **Persistance** (exigence : intention du 17/09/2026 reconfirmée par le mainteneur le 04/10/2026, critère 10 (a)) : tant que le taux est tenu, l'écart du glissement à π* ne se résorbe pas (au tour 120, même signe et au moins un cran d'affichage, 0,1 point). La trajectoire est classée sans présomption : *dérive continue* (écart croissant entre les tours 60 et 120), *nouveau palier* (π̄ ≠ π*, état stationnaire publié) ou *retour* (écart résorbé). Un retour signale une ancre nominale non monétaire (par exemple un plan de dépense en u.m., fiche 9, Q10) : son canal est identifié et le cas est porté au mainteneur au titre de (a). Maquettes indicatives de `monnaie` et de `macro` (04/10/2026) : sous une demande lisant π* (M27, M28), racine unitaire (dérive linéaire) sans effet de niveau, palier avec effet de niveau θ = 1, oscillation si la dépense est un plan en u.m. ; explosif seulement si la demande lisait i − π ; (iii) le régime de la v2.0 n'est pas reproduit : inflation moyenne de 4,048 % pour une cible de 2 % (G1, S+O) ; biais d'environ 2 points indépendant de la cible (J1a, S+O) ; taux réel directeur de 5,12 % (D1, R) | Point fixe ; maquette (signe et date) | `monnaie` ; mainteneur ((a)) | validation des critères ((a)) ; fiche ; J3 |
| 11 | Stabilité de la boucle conjointe : fait nouveau contre l'instabilité 4 (gabarit 3 ; C2, C10, C14, C26 ; `monnaie`, `macro` pour les blocs 3 à 6 et 9) — **exigence** pour (a), (c) et (d), **mesure** pour (b) | (a) **Fait nouveau exigé par C2** (instabilité 4, « estimateur du taux naturel sans ancre ni bande », R). Rayon spectral de la **boucle conjointe complète**, hors de la racine unitaire du niveau nominal (`sec:prix-conditions`) et de tout état inerte déclaré, **strictement inférieur à 1**. Il est exigé : à la calibration indicative ; dans chaque branche où une vitesse ou un gain est ×0,5 et ×2 (λ ≤ n_a) ; dans les deux régimes de l'emploi ; pour θ_H = 0,8 et 1 (fiche 5), et pour θ_H effectif sous chaque règle budgétaire candidate (fiche 9, critère 14 (c)) ; plancher inactif. La boucle comprend : salaires SN (M25) ; prix M (M26) ; ménages C lisant π* (M27) ; investissement S-ζ et F (M28) ; transmission de la fiche 7 (M31) ; chaque règle budgétaire candidate de la fiche 9 (au moins la reprise intégrale T9 et la règle que recommande `macro`) ; règle de taux, loi de π^e et crédibilité de l'option. La divergence de C2 sous le régime « intérêts financés par le déficit » est publiée comme mesure (fiche 9, critère 9 (d)) ; elle ne fait pas échouer l'exigence, qui porte sur la règle budgétaire de référence. (b) **Contenu de C10**, publié pour chaque option : délai de lecture (1 tour sous M26 (c)) ; mesure lue ; signe du canal taux → demande (fiches 5, 6 et 9) ; loi d'anticipation ; ψ_ξ et λ_μ ; plancher ; grille ×0,5 et ×2 ; module, demi-vie et **période de la racine dominante, comparée à une partie (60 à 120 tours)**. Sous le régime déclaré de financement des intérêts par le déficit (fiche 9, critère 9 (d)), la divergence de C2 est chiffrée (tour où i_CB s'écarte d'un point de sa valeur stationnaire) et transmise à `jeu`. (c) **C14** : gain statique ∂(demande totale)/∂r < 0 à la calibration, tous canaux réunis (C34), et rayon inférieur à 1. Son échec est le fait nouveau qui rouvre la substitution intertemporelle (fiche 5, Q3, point 4). (d) **C26** : si une option fait lire π^e aux ménages (lecture (b) de la Q10 de la fiche 5), les trois conditions de la clause sont vérifiées (`sec:menages-inflation` l. 1455). Sinon la clause est déclarée « non déclenchée » | Linéarisation en forme fermée ou maquette (`uv run python`, commande et sortie citées), avec une contre-épreuve indépendante (précédent de l'instabilité 17) ; `tab:instabilites`. Une seule maquette conjointe, versionnée au compte rendu, sert aux critères 6 (d), 11, 12, 15 et 16 de cette fiche et aux critères 6, 8 (c) et (d), 9 et 18 de la fiche 9. | `monnaie` ; `macro` | fiche (jalon 2) ; J3 (remesure sur le socle) |
| 12 | Clause de réouverture de la phase de P_t (ADR 0008, II.7 ; C10 ; `monnaie`) — **exigence** de procédure ; verdict publié au jalon 2 | **Grandeurs.** ρ_c : rayon spectral, hors de la racine nominale, de la boucle conjointe du critère 11 sous la lecture en vigueur (c) (la règle lit π_{t−1} en phase 1). ρ_b : même boucle, mêmes paramètres, sous la lecture (b) (la règle lit π_t, p_t et UC passés en phase 1 ; ADR 0008, II.7, forme). **Domaine déclaré avant l'essai.** D : liste finie des calibrations candidates de la règle de chaque option (coefficients et mesure lue — glissement, ou variation sur le tour annualisée géométriquement), écrite au § 3 avant tout calcul de ρ_b. G : la calibration indicative des blocs 2 à 7 et 9, plus chaque vitesse ×0,5 et ×2. **Verdict.** Le délai d'un tour est **déterminant** si et seulement si aucune calibration de D ne donne ρ_c < 1 sur toute la grille G, alors qu'au moins une donne ρ_b < 1 sur toute G. Sinon il est **non déterminant**, et la calibration retenue est prise parmi celles qui donnent ρ_c < 1 sur G. **Publication** (mesure) : ρ_c et ρ_b, avec demi-vies et périodes, à la calibration retenue, quel que soit le verdict. **Conséquence.** « Déterminant » déclenche la clause : décision citant M26, M24 et M22, et nouvel ADR remplaçant la partie II. « Non déterminant » laisse M26 en l'état. Verdict rendu au jalon 2 sur la calibration indicative, **réévalué au J3** avec le même critère sur la calibration retenue (C7, #45) ; un changement de verdict au J3 est une décision citant M26 et M32. **Clause analogue de l'ADR 0010** (conditions de réouverture) : même critère, avec ρ_1 (cible lue au tour n + 1, en vigueur) et ρ_0 (cible lue au tour n), publié en mesure | Maquette du critère 11 sous les deux lectures ; commande et sortie citées ; contre-épreuve indépendante | `monnaie` ; `macro` (blocs 3 et 4) ; mainteneur (décision si déterminant) | fiche (jalon 2) ; J3 |
| 13 | Superneutralité (C15 ; #49 ; `monnaie`, `macro` pour les blocs 5 et 6) — **exigence** | (a) Pour π̄ = π* ∈ {0 ; 2 % ; 10 %}, r̄ et les allocations réelles (C/Y_o, V_H/(n_a YD^HS), K^vol/(n_a y), tu, ti) **égalent leurs formes fermées à 1e−10 près en relatif** (script contre moteur). Sont exactement invariantes, à 1e−10, les grandeurs dont la forme fermée ne dépend pas de π̄ : V_H/(n_a YD^HS) = ν_H, K^vol/(n_a y), tu, U = U^eq. Les autres ont une dépendance déclarée, chiffrée et attribuée à sa source : terme croisé des ménages, s_HS de 1,9819 à 1,9977 % (l. 1513) ; forme du taux lue par chaque bloc ; assiette nominale des impôts (fiche 9, Q8). Un seuil de matérialité de l'écart entre π̄ = 0 et 10 % (r̄ en points de base, allocations en points de PIB) est fixé par le mainteneur **avant l'essai** (adopté le 04/10/2026, sur proposition de `monnaie` : moins d'un cran d'affichage, 0,1 point, sur r̄ et sur chaque allocation exprimée en % du PIB, entre π̄ = 0 et 10 %). (b) **Formes du taux réel** : quatre coexistent — r = i − π (l. 214, restituée et testée au test zéro) ; ϱ_L de Fisher sur π* (S1) ; rendement exact n_a ln(1 + i/n_a) − ln(1 + π) ; taux réel implicite du revenu de Haig-Simons, i_D − n_a π*^pas (l. 1578). La fiche déclare celle que la règle tient invariante (avis de `macro` : Fisher sur π*, forme de S1). Les trois autres sont publiées avec leur dépendance à π̄ en forme fermée (pour une forme de Fisher tenue à 1 % : 1,0000 / 1,0200 / 1,1000 % ; 0,9996 / 1,0359 / 1,5180 % ; 1,0000 / 1,0381 / 1,5310 %). Lecture de la l. 214 : précision rédactionnelle selon `architect` (« testé » = bande O1 du test zéro, `temps_comptabilite.md:568` ; annotation datée de l'ADR 0005, pt 5) ; devient une modification (décision citant M22 et M25) si la forme restituée ou testée change. Lecture retenue par le mainteneur le 04/10/2026 : précision rédactionnelle. (c) Les ratios en u.m. qui dépendent de π̄ par la valeur comptable (C30 ; fiche 7, critère 8 (c)) sont déclarés, non testés comme allocations. Un impôt assis sur les intérêts nominaux (fiche 9, Q8) rend le rendement réel après impôt dépendant de π̄ à taux réel avant impôt donné : la dépendance est déclarée | Formes fermées ; au J3, script d'état stationnaire (extension du test T2) | `monnaie` ; `macro` | fiche ; J3 |
| 14 | Canaux du taux, changement de cible et délais (C13, C16, C17, C32 à C35 ; `monnaie`) — **exigence** pour (a) à (e) et (g), **mesure** pour (f) | (a) **C13** : aucun canal direct π^e → p ni canal de coût du taux, dans le bloc 8 comme dans le bloc 4. (b) **C32** : une seule lecture de l'inflation pour les ménages et les entreprises (π*). (c) **C33** : les effets d'un changement de cible sont déclarés : −1,98 % du plan d'investissement et +0,55 % du budget des ménages par point de baisse de π*, à taux du crédit donné ; effet net à l'impact de +0,085 à +0,193 point de PIB (fiche 6 § 6.3, chiffres de la fiche, non remesurés ici). (d) **C34** : dans toute mesure, les canaux du taux sont déplacés ensemble (plan, intérêts des lignes 9 et 10, dividendes de la banque). (e) **C35**, forme révisée sous M30 (fiche 6 § 9.10) : décision du tour n (taux ou cible) → i_L, i_D et π* lus à l'ouverture du tour n + 1 → plans du tour n + 1 ; intérêts des lignes 9 et 10 au tour n + 1 → plan des ménages au tour n + 2. (f) **C16** : élasticités des ménages, entrées du critère 11. (g) **C17** : au socle, l'assouplissement quantitatif passe par la seule ligne 19b-banque : Res monte, B_Bk baisse, M est inchangée. Une souscription 19a-BC ne crée de monnaie centrale que lorsque l'État dépense (l. 379). Déclaré à `jeu` | Formes ; cas à la main | `monnaie` | fiche |
| 15 | Signe net d'une hausse de taux (#56 ; **critère partagé avec la fiche 9, écrit une seule fois ici, texte commun de `monnaie` et `macro`, seuils de `jeu`** ; frontières inflation et dette publique) — **mesure** à la fiche (jalon 2), **exigence** au J4 pour P1 et P2, avant l'ouverture du levier de taux ; propriété écrite avant l'essai | **Configuration de référence.** Depuis l'état résolu ; contrôle apparié (même état, même graine, mêmes leviers) ; i_CB exogène (règle de taux désactivée) ; i_B selon sa règle (fiche 9, critère 13 (c)) ; π* inchangée ; règle budgétaire de référence de la fiche 9 (C37) ; tous canaux du taux déplacés ensemble (C34). (A) i_CB +1 point aux tours 1 à 12, puis retour à sa valeur stationnaire ; (B) +1 point maintenu 120 tours ; le contrôle garde i_CB à sa valeur stationnaire. Sous un taux exogène, l'inflation n'a plus d'ancre monétaire après le choc : sa dérive éventuelle est déclarée (critère 10 (b) (ii)), non attribuée à la transmission. **Configuration de référence de la branche (A), décidée par le mainteneur le 04/10/2026** : règle de taux en vigueur, taux décidé supérieur d'un point à sa prescription aux tours 1 à 12 (préférence de `macro`, ancre nominale) ; la variante à i_CB exogène est publiée en mesure. La configuration ci-dessous vaut pour la branche (B) et pour cette variante. **Publiés sans seuil** : y, P, C^vol, I^vol et glissement aux tours 1, 2, 3, 12, 36 et 120 ; écart cumulé de production des tours 1 à 12 ; tour du premier écart de chaque grandeur. **P1, signe** — (A) écart cumulé de production des tours 1 à 12 strictement négatif, et P_36 < P_36^réf ; (B) P_120 < P_120^réf et glissement du tour 120 inférieur à celui du contrôle ; y_36 et y_120 publiés sans exigence de signe. **P2, délai** : aucun écart de y, C^vol, I^vol ni P au tour 1 (production visée et prix du tour lus sur l'ouverture, N2 à N4 et P1 à P3 du bloc prix ; plans lus sur l'ouverture, C35). Si la règle budgétaire lit un taux de la phase 1, l'écart de G^vol au tour 1 est déclaré, sa contrepartie étant la variation des stocks. Premier écart de I^vol au tour 2 ; de C^vol et de y au plus tard au tour 3 ; de P au plus tôt au tour 2 (aucun canal de coût, C13). **P3, ordre de grandeur** (mesure) : en (A), écart maximal de production des tours 1 à 36 par point de taux d'au moins 0,2 %, et écart maximal de glissement d'au moins 0,1 point avant le tour 36 (planchers de perceptibilité de `jeu`) ; en (B), écart maximal de production des tours 1 à 36 d'au plus 4,3 % par point (pic de la production industrielle pour un choc permanent de 100 pb selon l'approche de Romer et Romer, 2004, rapporté par Coibion, 2011, NBER w17034, qui juge l'effet « most likely medium », −1,6 % par l'approche hybride ; l'ampleur est contestée et la production industrielle n'est pas la production totale). Hors fourchette, le constat va à `jeu` et au mainteneur. Sur la maquette minimale (κ = λ = 0,1, illustratifs), le plancher de glissement de 0,1 point n'est pas atteint (0,041 à 0,058 point, `macro`) : constat transmis à `jeu` et au mainteneur. **Régime déclaré** : sous un financement des intérêts par le déficit (fiche 9, critère 9 (d)), le signe peut s'inverser ; c'est la dominance budgétaire déclarée, publiée, non un échec de P1. **Configurations publiées en mesure** : (i) **pays joué** : l'essai est refait avec les leviers budgétaires tenus à leur valeur initiale dans leur unité, sans règle (fiche 9, critère 19) ; le signe de P1 y est publié, et la restitution montre au joueur la charge d'intérêts et le revenu des ménages par source ; (ii) **écart à la prescription** : règle de taux en vigueur, taux décidé supérieur d'un point à sa prescription aux tours 1 à 12, état de l'action intégrale jamais réinitialisé (critère 19 (c)). **Verdict** : P1 et P2 tenus ou non, sous la configuration de référence. Si P1 échoue, `monnaie` et `macro` décrivent les options (transmission, règle budgétaire, η_r, ζ) et leur coût en fidélité ; le mainteneur tranche avant l'ouverture du levier | Maquette conjointe unique (critère 11), commande et sortie citées ; scénario apparié au J4 | `monnaie` ; `macro` ; `jeu` (borne basse de P3, restitution) ; mainteneur (si P1 échoue) | propriété : fiche ; mesure : jalon 2 ; exigence : J4 |
| 16 | Essai d'aller-retour de la cible (#54 ; `monnaie` ; `jeu` pour le seuil d'affichage) — **exigence** (verdict), conditionnée à ce que π* soit un levier (Q4) | **Essai** (issue #54), depuis l'état résolu, règle de taux endogène, régimes de hausse et de baisse de l'emploi, délai d'un tour de M30 : (1) marche π* −1 point (de 2 % à 1 %) : C, y, π et i_D aux tours 1, 3, 12, 24 et 60, effets cumulés sur C et y aux tours 12 et 24, tour du changement de signe ; (2) aller-retour −1 point au tour t, +1 point au tour t + k, pour k = 1, 3 et 12 ; (3) même essai sous cible nominale, en maquette seulement (variante non retenue par M27), pour chiffrer l'apport de la cible de Haig-Simons ; (4) mêmes essais (1) et (2) avec la règle de taux désactivée, taux tenu par le joueur à sa valeur initiale (avis de `jeu`). **Grandeurs** : G_h(X) = Σ_{t=1}^{h}(X_t − X_t^réf)/Σ_{t=1}^{h} X_t^réf, pour X ∈ {y, C^vol} et h ∈ {12 ; 24 ; 60} ; coût visible c_24 = écart absolu maximal de π_t − π_t^réf sur les tours 1 à 24 (glissement annuel, points), avec l'écart de π^e et de crédibilité si l'option en a. **Coût visible** : écart de glissement au contrôle d'au moins **0,2 point pendant au moins 3 tours consécutifs** sur les tours 1 à 24 (seuil de `jeu`, aligné sur M26) ; l'écart maximal c_24 reste publié. Le coût au sens du score relève du J7. **Verdict**, pour chaque k et chaque régime : « **stimulant gratuit** » si G_24(y) > 0, G_60(y) ≥ 0 et aucun coût visible ; « **arbitrage avec coût visible** » si G_24(y) > 0 et coût visible ; « **non rentable** » si G_24(y) ≤ 0. Mesure : aller-retour répété (période 2k sur 120 tours), écart moyen de production et c publiés. Le verdict « stimulant gratuit » est aussi rendu si, en aller-retour répété de période 2k sur 120 tours, l'écart moyen de production est positif alors que l'écart de glissement reste sous le seuil de coût visible. **Conséquence** : un « stimulant gratuit » pour au moins un couple (k, régime) oblige la fiche à comparer des contreparties (délai d'entrée en vigueur, fréquence de révision du levier, coût de crédibilité par la lecture (b) et C26), avec leur coût en fidélité ; le mainteneur tranche. Restitution au J4 : signe et ampleur à l'impact, puis effet net à 12 tours | Maquette du critère 11 ; commande et sortie citées | `monnaie` ; `jeu` (seuil) | fiche (jalon 2) si π* est un levier ; sinon J3 ou J4 |
| 17 | Test zéro (O1 ; `docs/exigences.md` § 2.6 ; `monnaie`) — **exigence**, mesurée au J3 | 720 pas sans choc depuis l'état résolu, plusieurs graines, moyennes par blocs de 60 pas. **Bandes proposées**, à confirmer par le mainteneur avec O1 avant l'essai (M19). Glissement dans π* ± 0,1 point : le point de départ d'O1, 2 ± 1 point (`docs/exigences.md` § 1.3), porte sur un niveau ; depuis l'état résolu, l'écart attendu est nul. Taux réel directeur r = i − π dans r̄ ± 0,1 point (O1 : 1,5 à 3 %, porte sur le niveau résolu). π^e − π̄ dans ± 0,1 point. Crédibilité dans ± 0,01. H/(12 PIB) à ±10 % en relatif quand sa valeur stationnaire est non nulle ; nullité à 1e−12 × S^CB près quand la règle la rend nulle ; B_CB/B ±1 point, bande commune avec la fiche 9 (critère 15). E^CB/(12 PIB) selon la forme retenue au critère 2 (a). Toute dérive depuis l'état résolu est un défaut | Préalable : critères 6 et 7 ; au J3, test zéro du socle | `monnaie` ; mainteneur (bandes) ; `macro` (E^CB, #26 pt 2) | J3 |
| 18 | Bornes (gabarit 6 ; #38, lecture (ii) ; `CONVENTIONS.md` § 2.4 ; `monnaie`) — **exigence** | (a) **Plancher du taux directeur** : borne à seuil libre (`CONVENTIONS.md` § 2.4), déclarée avec sa valeur, son motif, son activité à l'état stationnaire et la condition d'existence r̄ + π* ≥ plancher. (b) Écrêtages de la première tentative classés, non repris sans motif : v1.5 plafond ī (l. 1018), (·)^+ (l. 1019), clip du taux naturel estimé à [−0,01 ; 0,06] (l. 1020) et de π^s (l. 1021) ; v2.0 clip de π^e à [−0,1 ; 12] (`model.py` l. 1307), bande du taux naturel ±0,01 (`policies.py` l. 63), plafond de crédibilité (l. 1306). (c) **Instabilité 15** : aucune borne n'est active à l'état stationnaire ni sous les scénarios O2. Scénarios adverses : dépense publique −5 % pendant 12 tours, dimensionnée pour porter le taux au plancher ; marche de cible de ±1 point. Une borne qui s'y active cesse de l'être **au plus tard 12 tours après la fin du choc** et ne se réactive pas sans nouveau choc (seuil reconduit). Un plancher actif plus longtemps est publié avec sa durée et constitue un échec, sauf motif adopté par le mainteneur avant l'essai | Décompte des bornes par option, avec leur classement ; au J3 ou au J4, scénarios | `monnaie` ; mainteneur (classement) | fiche ; J3 ou J4 |
| 19 | Lisibilité et leviers (gabarit 5 ; C7, C9, C11 ; `monnaie`, à soumettre à `jeu`) — **exigence** pour (b), **mesure** pour (a), (c), (d) et (e) | (a) **Indicateurs au tour**, chacun avec sa définition, son unité, son dénominateur et sa fenêtre : glissement et cible ; π^e ; crédibilité ; i_CB et taux réel r = i − π ; **taux indiqué par la règle** et écart du taux décidé à celui-ci (C9) ; H au PIB ; Π^CB et E^CB ; ratio de sacrifice dans le scénario O2 (C7), grandeur de documentation et de scénario O2, non indicateur au tour (avis de `jeu`). (b) **Délais en tours entiers** : i_CB → lignes 12 et 13 au tour n (délai nul) → i_L et i_D au tour n + 1 → plans au tour n + 1, consommation au tour n + 2 (C35) ; π* → plans au tour n + 1 (M30) ; achats de titres → Res et B_Bk au tour n. La contrepartie est visible le même tour. (c) **Leviers** : taux directeur (et i_res selon le corridor) ; cible π*, si c'est un levier ; achats de titres (19a-BC, 19b-banque), s'ils sont retenus. « Suivre la règle » est une **valeur du levier**, non un drapeau de mode : la règle est calculée à chaque pas et sa prescription restituée. Pour chaque levier : type, unité, phase de lecture, premier flux modifié, délai, contrepartie (`tab:leviers`). L'état de l'action intégrale suit la même loi que la règle soit suivie ou non ; il n'est jamais réinitialisé. Le taux indiqué par la règle, restitué à chaque tour, annonce le taux qu'appliquerait un retour à la règle. Un levier sans effet identifiable sur un indicateur du tableau du tour au socle (achats de titres sous C17) n'est pas ouvert au J4 ; il est renvoyé au J6 avec la prime de terme ou de risque. (d) **Ampleur** : seuils à proposer par `jeu`. Signes contre-intuitifs déclarés : canal rentier (fiche 5) ; désinflation annoncée qui relève la consommation (C33) ; retour du niveau des prix (C11) ; absence de l'« énigme des prix » (fiche 4 § 6.1, Q5). (e) **Perceptibilité à l'échelle d'une partie** (mesure ; avis de `jeu`, accepté par `macro` et `monnaie`), définie avant l'essai : (i) au moins un indicateur du tableau du tour s'écarte du contrôle apparié d'au moins **deux crans d'affichage** (0,2 point pour un taux, un glissement ou un ratio affiché en % à une décimale ; 0,2 % pour un niveau) dans les **12 tours** qui suivent la décision ; (ii) le pic de l'écart survient au plus tard au **tour 24** ; (iii) toute dynamique de demi-vie supérieure à **60 tours** est déclarée, avec l'écart résiduel qu'elle laisse au tour 60 sur le glissement et sur la production. Un écart résiduel supérieur à un cran au tour 60 est signalé à `jeu` comme transition non attribuable. | Tableau du § 9 (« Interfaces ») ; avis de `jeu` (§ 7) ; au J4, scénario apparié (O2) | `jeu` ; `monnaie` | fiche ; J4 |
| 20 | Simplicité, empreinte sur l'état, déterminisme (gabarit 6 et rubrique 9 ; principe de simplicité ; `monnaie`) — **mesure** (décompte) et **exigence** (sans historique ni drapeau) | Décompte par option : paramètres, bornes, variables d'état (π^e, crédibilité, état de l'action intégrale, taux retardé si lissage), lignes et phases touchées, chacun justifié. Chaque variable d'état a son unité et sa valeur stationnaire. Aucun historique : l'historique des prix de la v2.0 (ADR 0005, Contexte) est remplacé par le registre de 13 niveaux. Aucun drapeau : `rstar_mode` et `rstar_anchor` (`model.py` l. 290 et 373 ; `policies.py` l. 58, L) et la branche `wsps2` de π^e (`model.py` l. 1301) ne sont pas repris comme modes (ADR 0002). Aucun tirage | Tableau de décompte | `monnaie` | fiche ; J2 (reprise exacte) |
| 21 | Coût de calcul (gabarit 4 ; `monnaie`) — **exigence** (aucune itération) et **mesure** (décompte) | Aucune itération ni optimisation à chaque pas (ADR 0002) ; aucune résolution de point fixe dans le pas (le point fixe du critère 6 relève du script d'état stationnaire). Décompte des opérations. **Part indicative : 0,48 ms par pays-pas** (reconduite) | Décompte ; au J3, `tests/invariants/test_budget.py` | `monnaie` ; `audit` | fiche ; J3 |
| 22 | Notation (`CONVENTIONS.md` § 5.2 ; décision du 02/10/2026 sur #23 ; `monnaie`) — **exigence** | Chaque symbole a un seul sens. En particulier : le gain intégral ne s'écrit pas k (intrant) ; la crédibilité ne s'écrit pas c (indice des pays) ; les ν_1 à ν_9 de la v1.5 se distinguent de ν_H et ν_F ; r reste le taux réel ex post i − π, et le taux naturel estimé reçoit sa propre marque ; ρ_i (lissage, v1.5) se distingue de ρ̄_K et de ρ̄_IN ; Δ^res et υ sont à confirmer. π^e, π*, π*_t, π̄, π_t, i_CB, i_res, E^CB et Π^CB gardent leur sens ; est aussi pris : b (dette nette hors banque centrale, `sec:menages`) | Liste confrontée à `tab:symboles` (commande `grep` et sortie citées) | `monnaie` ; `docwriter` | fiche ; section proposée |
| 23 | Calibrabilité et faits établis (`monnaie`) — **mesure** | Paramètres calibrés sur des sources retrouvées et datées : coefficients de la règle, gain d'apprentissage, ratio de sacrifice, ampleur et délai des effets du taux. Sources candidates, avec leur statut : Taylor (1993), *Carnegie-Rochester Conference Series on Public Policy* 39, 195-214, lu, p. 202 (fiche 4 § 6.1) ; Barro et Gordon (1983), résumé NBER lu ; Orphanides (2001), *AER* 91(4), extrait ; Ball (1994), existence vérifiée (fiche 3 § 6.1, Q7) ; Evans et Honkapohja (2001), existence vérifiée ; Romer et Romer (2004), résumé lu. **Contestés** : le niveau du taux naturel ; l'ampleur du ratio de sacrifice ; l'ampleur des effets du taux. Un résultat de la v1.5 ou de la v2.0 n'est pas un fait établi (inflation de 4 %, taux réel de 5 %) | Sources citées ; « non trouvée » le cas échéant | `monnaie` | fiche ; J3 |
| 24 | Remesure des faits de la première tentative (décision P1 du 03/10/2026 ; `CONTEXT.md` ; `monnaie`) — **exigence** de procédure | (a) Chaque fait porte son statut : G1 (S+O) ; D1 sur 60 ans (R) ; crédibilité du contrôle (O) ; I1, J1a, J1b, K1 (S+O) ; K1a (L et O) ; G-T (S+O). (b) Toute remesure (statut V) passe par un script d'`outils/` exécuté **dans un processus séparé** (invariant 4), revu par `audit`, avec ses critères écrits avant l'essai. (c) Un fait V sur le prototype v2.0 reste un fait de la première tentative. (d) Lectures de code (L) avec la branche active et les coefficients effectifs. Profil D1 : `rstar_mode='anchored'`, `rstar_anchor='deposit_wedge'`, `rstar_band=0,01`, `rho_i=0,7` (faits § 1.1). Les valeurs par défaut de `Params` (l. 229, 290, 303) ne sont pas celles de D1 | Liste des faits et statuts ; commande, sortie et commit | `monnaie` ; `coder` ; `audit` | fiche (jalon 2) |

### Amendements adoptés

Décisions du mainteneur du 04/10/2026, prises avant l'instruction, sur les questions des experts (validation groupée des critères des fiches 7, 8 et 9, P14) :

- **Critères** : la liste est validée telle qu'amendée par la relecture croisée du 04/10/2026 (avis de `macro`, `monnaie` et `jeu` ; qualifications d'`architect`), avec la nature de chaque critère (exigence ou mesure) ; les seuils reconduits et les seuils de `jeu` sont adoptés.
- **Options marquées « à trancher par le mainteneur » au choix M31 à M33** (propriétaire des lignes 19a, règle de i_B, règle de M^{G*} et lecture du contrôle de caisse, forme de E^CB) : instruites telles qu'écrites, avec leur qualification (interprétation ou modification) ; elles se décident aux décisions de fiche, non à cette validation.
- **Critère 15 (#56)** : la configuration de référence de la branche (A) est **la règle de taux en vigueur, le taux décidé dépassant sa prescription d'un point aux tours 1 à 12** (préférence de `macro` : l'inflation garde une ancre nominale ; c'est le geste du joueur) ; le taux exogène est publié en mesure.
- **Critère 13 (C15, #49)** : seuil de matérialité adopté avant l'essai : moins d'un cran d'affichage (0,1 point) sur r̄ et sur chaque allocation exprimée en % du PIB, entre π̄ = 0 et 10 %. La l. 214 (`r = i − π`) se lit comme une précision rédactionnelle (« testé » = bande O1 du test zéro) : annotation datée de l'ADR 0005, point 5, sans décision M-n.
- **Critère 10 (a)** : l'intention du 17/09/2026 (politique monétaire par une cible d'inflation et un taux directeur) est reconfirmée ; la persistance du critère 10 (b) (ii) est donc une **exigence**.

## 3. Options

*Instruit par `monnaie` (expert pilote) le 04/10/2026, sur la fiche à l'état `320bfbb` (branche `claude/j1-monnaie-etat`, PR #77). Aucun chiffre de ce paragraphe n'est un résultat du moteur v3, qui n'exécute rien. Ce sont des formes fermées ou des sorties d'une maquette conjointe (§ 3.0), donc des résultats de modèle, non des faits.*

### 3.0 Conventions, maquette conjointe, mesures et littérature

**Découpage par question** (gabarit § 3). Le bloc tranche onze questions (§ 1.5).
- Les options A (v1.5) et B (v2.0) sont instruites en entier.
- Sur Q4 à Q10, les contrats hérités (M22 à M31) ne laissent qu'une forme compatible, à une lecture près chacune. Cette forme est instruite une fois, comme socle commun (§ 3.N).
- Les options nouvelles diffèrent sur Q1 (règle), Q2 et Q3 (anticipations, crédibilité) :
  - **C** : action intégrale sans fuite, sous la forme de Fisher sur π\*, avec une anticipation adaptative, c'est-à-dire un apprentissage à gain constant de la moyenne ;
  - **C-h, C-c, C-g** : variantes de Q2 et Q3 combinables avec C (ancrage constant, crédibilité d'état revue, gain endogène) ;
  - **D** : corridor explicite, variante de Q5 ;
  - **T** : règle de Taylor à taux naturel fixe, contre-exemple de Q1 ;
  - **R** : référence sans retard (`docs/exigences.md` § 2.7).

**Maquette conjointe unique** (critère 11). Elle sert aussi aux critères 6 (d), 12, 15 et 16, et aux critères 6, 8 et 9 de la fiche 9. Pas mensuel, n_a = 12, niveaux en u.m. et u.v.

Elle exécute les équations des sections décidées :
- N1 à N11 (M24) ;
- T1 à T6 (M25) ;
- P1 à P4 (M26) ;
- H2 à H7 (M27) ;
- S1 à S7, F1 à F4 (M28) ;
- l'option C de M31, soit C1 à C4 de la fiche 7 : écarts constants, ligne 21 sur la position nette, Div_Bk résiduel.

Elle exécute aussi le cadre :
- l'émission en position α (l. 497-502) ;
- Π^CB (l. 493) ;
- le registre de 13 niveaux ;
- π\*_t en vigueur (M30).

Le bloc 9, non instruit, y est **provisoire et déclaré** :
- G^plan = P_{t−1}(1 + π\*^pas)·s_G·ŷ_t (volume indexé sur la production potentielle ŷ_t = pr_t(1 − U^eq)N^pa_t) ;
- T_H = τ·WB_t, avec τ = 0,25 ;
- T_F = Tr = 0 ;
- M^G\*_t = G_t + i_B B_t/n_a (m = 1) ;
- A8, s_CB = 0, i_B = i_res = i_CB, E^CB = 0.

Trois réglages budgétaires sont mesurés :
- **T9** (référence provisoire, fiche 6 § 6.6) : prélèvement forfaitaire (i_CB − i_ref)·(B − M^G − E^CB)/n_a, en phase 6 ;
- **pays joué** : leviers tenus, aucune reprise (régime « intérêts financés par le déficit ») ;
- **sensibilité** : T_H assis sur le revenu avant impôt retardé (τ·Γ^e·Y^pre_{t−1}) et T9 en taux réel (i_ref suivant la cible selon Fisher).

Calibration indicative des blocs 2 à 7 : celle de `tab:calibration`, avec ζ = 4 (variante 8), ϖ_L = 2 %, ϖ_D = 1 % et ϑ = 0,10 (fiche 7 § 3.0), g = 2 %, g_N = 0,5 %, r̄ = 1 % (Fisher). L'état initial est **résolu**, lecture (1) de #44 : r̄ donné, s_G résolu.

Contrôles de la maquette (`chk1.py`, `chk3.py`) :
- elle reproduit les ratios publiés : L/(12 PIB) = 0,62204 / 0,33439 / 0,80037 ; D_F = 0,16605 ; K = 1,55510 ; I/PIB = 13,945 % ; ρ̄_K = 0,77862 ;
- un pas depuis l'état résolu laisse l'état normalisé inchangé à 3,6e−15 près ;
- E^Bk et E^CB, calculés par le stock et par les flux, coïncident à 2e−15 près ;
- l'application normalisée ne dépend pas de t (3,6e−15).

**Méthode spectrale.** Le jacobien est calculé par différences centrées sur l'état normalisé (nominaux divisés par P̄_t·Ȳ_t). En sont retirés les états exogènes (pr, N^pa, π\*) et les états inutilisés par l'option. La racine nominale (|λ − 1| ≤ 1e−11) est écartée. Les deux régimes de T4 (hausse, baisse) sont linéarisés séparément ; en baisse, N ≥ N\* par construction, donc y = y\*. *(Précisé le 04/10/2026, C48 : avant cette date, la paire complexe et le rayon en pays joué à 10 % venaient d'une dérivée au coude de T4 (régime « automatique »), et la linéarisation de la baisse gardait un second coude, y = min{y\*, pr·N} pris à l'égalité ; les rayons réels dominants, insensibles au régime, sont inchangés.)*

**Domaine D du critère 12**, écrit dans `run5.py` avant tout calcul de ρ_b : a_π ∈ {0,5 ; 1,5} × k_I ∈ {0,1 ; 0,25 ; 0,5}/an × a_U ∈ {0 ; 0,5} × mesure lue ∈ {glissement π_{t−1} ; variation du tour annualisée géométriquement}, soit 24 calibrations.

**Grille G** :
- calibration indicative ;
- chaque vitesse ×0,5 et ×2 : λ_v, λ_IN, λ_w, λ_N, λ_μ, λ_H, λ_ti, λ_e ;
- chaque gain ×0,5 et ×2 : k_I, a_π, a_U, ψ_ξ, β, η_r ;
- toutes les vitesses ×0,5, puis ×2 ;
- deux régimes de l'emploi.

**Littérature.**

*Lue* :
- L. Gáti, « Monetary policy & anchored expectations: an endogenous gain learning model », ECB Working Paper 2685, juillet 2022 :
  - p. 13-14, équations (22) et (23) : gain endogène k_t = g(f_{t|t−1}), lisse et convexe (g_f·f ≥ 0), qui emboîte le gain constant comme cas particulier ;
  - p. 19-20 : « the consensus in the literature on estimating learning gains is that if the true model is one with constant gain learning, then the gain lies between 0.01-0.05 » (données trimestrielles) ; Milani (2007) : 0,0183 ; Branch et Evans (2006) : 0,062 ; Erceg et Levin (2003) : 0,13 ; valeur de référence 0,05.
- Lues par les fiches précédentes et reprises ici : Taylor (1993), p. 202 (fiche 4) ; Barro et Gordon (1983), résumé NBER (fiche 4) ; Whitesell, FEDS 2006-22, p. 4 (fiche 7) ; Leeper (1991) et Bohn (1998), résumés (fiche 6) ; Coibion (2011), NBER w17034 (critère 15).

*Retrouvée par extraits de moteur de recherche seulement (PDF bloqué par le proxy)* : Evans, « Adaptive Learning in Macroeconomics », notes de cours (Oxford, 2020) et « Theories of Learning and Economic Policy » (2021), Université de l'Oregon. Extrait relevé : les anticipations adaptatives sont un cas particulier de l'apprentissage par moindres carrés à gain constant dont le seul régresseur est une constante. **À relire à la source avant toute citation dans la spécification.**

*Existence vérifiée, contenu non lu* :
- Evans et Honkapohja (2001), *Learning and Expectations in Macroeconomics* ;
- Orphanides et Williams (2004) ;
- Carvalho et al. (2021) ;
- Ball (1994) ;
- Keister, Martin et McAndrews (2008) ;
- Sargent et Wallace (1981).

*Ce que la littérature permet de conclure* :
- la loi adaptative de C est un apprentissage à gain constant de la moyenne (source à relire) ;
- un gain de 0,01 à 0,05 par trimestre correspond, en conversion linéaire d'une vitesse, à λ_e ≈ 0,04 à 0,2 par an ; la référence de 0,05 par trimestre donne λ_e = 0,2 par an ;
- l'ancrage dépendant de l'état (gain croissant avec l'erreur de prévision) a un appui empirique (Gáti 2022, p. 14).

Elle **ne permet pas** de calibrer une « crédibilité » distincte du gain.

**Statut des faits de la première tentative** (critère 24).

| Fait | Statut |
|---|---|
| G1 | S+O |
| D1 sur 60 ans, décomposition du taux réel | R |
| Crédibilité nulle du contrôle | O |
| J1a, J1b, K1, I1 | S+O |
| K1a | L et O |
| G-T (`a_pi` = 1,5 actif dans D1) | S+O |
| Lectures de `model.py` l. 224-229, 289-293, 1294-1308, 1366-1379 et de `policies.py` l. 43-71 | L, le 04/10/2026 |

Aucune remesure V n'a été faite.

### 3.A Option A — v1.5

1. **Source.** `archive/v1.5/Nations_et_Marches_v1_5.tex` :
   - `eq:taylor`, l. 1016-1024, et ses ajouts v0.9, l. 1030 ;
   - `eq:expect` et `eq:cred`, l. 1149-1151, et leur lecture l. 1156-1161 ;
   - `eq:ecb`, l. 998-1005 ;
   - encadré « joueur », l. 984-991 ;
   - calibration, l. 2265-2268 et 2315.
2. **Équations.**
   - Règle :
     - i_t = min(ρ_i i_{t−1} + (1 − ρ_i) i†_t ; ī) ;
     - i† = [r̂\* + min(π^e, π^s + 0,5) + a_π(π^s − π\*) + a_y ŷ]⁺ ;
     - r̂\*_{t+1} = clip(r̂\* + λ_r(π^s − π\*) ; −0,01 ; 0,06) ;
     - π^s = EMA(λ_s) de 12·clip(ln P_t/P_{t−1}).

     Paramètres : a_π = 1,5 ; a_y = 0,5 ; λ_r = 0,02 par mois ; λ_s = 0,10 ; ρ_i = 0,95 ; ī = 1. Choix de conception.
   - Anticipations : π^e_{t+1} = π^e + λ_π(π − π^e) + c(π\* − π^e) + υ(g^M − g^Y − π^e), avec λ_π = 0,2 par mois et υ = 0,05 par mois.
   - Crédibilité : c_{t+1} = clip(c + ν_1·1[|π − π\*| < ε̄] − ν_2|π − π\*| − ν_3·1[ΔA^G > 0] − … ; 0 ; 1 − ν_9 M^hist), avec ν_1 = 0,01, ν_2 = 0,5, ν_3 = 0,2.
   - Bilan : rémunération i^CB − Δ^res sur min(Res ; B^CB + A^G + L^CB), dividende Σ assorti d'un report des pertes.
3. **État stationnaire.**
   - Pour r̄ ∈ ]−1 % ; 6 %[, le clip est inactif. L'intégrateur de r̂\* est alors sans fuite, mais il compare π^s, une **variation logarithmique annualisée**, à π\*. Il impose donc ln(1 + π̄) = π\*, soit π̄ = e^{π\*} − 1 : 2,0201 % pour 2 % et 10,517 % pour 10 % (échec du critère 5 (a)).
   - Hors de la bande, le clip borne r̂\*, et π̄ − π\* = (r̄ − r̂\*_borne)/a_π dépend de r̄.
   - La crédibilité stationnaire vaut **1, posée par la borne du clip** : bonus actif à écart nul.
   - π^e = π̄ exige que υ porte sur une croissance géométrique. Sous g^M − g^Y en log ×12 : π^e − π̄ = υ(ln(1 + π̄) − π̄)/(λ + c + υ) = −7,9e−6 à 2 % (échec de C1 au pied de la lettre).
   - Hors de la cible, π^e = (λπ̄ + cπ\* + υπ̄)/(λ + c + υ).
4. **Comportement mesuré.**
   - Prototype v1.5 (R, l. 1030) : « inflation revient à 2,1 % », « r̂\* ≈ 0,7 % ».
   - Maquette, transposition **au meilleur cas** (cible comparée à ln(1 + π\*), υ en croissance géométrique), sous T9 : rayon 0,999480 à 2 % (demi-vie 1 332 tours), 0,999334 à 0 et 0,999851 à 10 % ; pire valeur sur G 0,999529 ; stable.
   - Avec c = 1 par mois, π^e a une racine propre de −0,25 (alternance d'un tour sur l'autre), sans effet dominant.
5. **Coût.** Une cinquantaine d'opérations, sans itération. Conforme.
6. **Défauts.**
   - Mesure en log contre une cible en glissement (critères 5 (a) et 6 (a)).
   - Loi à seuil (critère 9 (c)).
   - Crédibilité tenue par sa borne à l'état stationnaire (critère 18 (c), instabilité 15).
   - Écrêtages libres : ī, (·)⁺, clip de r̂\* et de π^s, min(π^e, π^s + 0,5) ; six au total.
   - Avances (ν_3) et M^hist (J6).
   - Rémunération sur min(·), soit un solde ; Δ^res non nul.
   - Lissage ρ_i : une variable d'état de plus.
7. **Identités.**
   - `eq:ecb` paie i^res sans receveur côté banque (fiche 7 § 3.A-6 (i)).
   - Le dividende Σ reporte des pertes : la valeur nette varie. C'est contraire à M22 (d) (versement chaque tour, sans troncature).
8. **Joueur.** Leviers : taux, réserves obligatoires, QE, avances, change, cible, mode « pilote automatique ». Une crédibilité qui ne monte que dans une bande de 1 point : effet de falaise.
9. **Empreinte.** r̂\*, π^s, i_{t−1}, π^e, c, M^hist, et M_{t−1}, y_{t−2} pour υ : sept variables d'état.

### 3.B Option B — v2.0 (profil D1)

1. **Source** (L).
   - `archive/v2.0/prototype/model.py` :
     - l. 224-229 : `a_pi` = 0,5 par défaut, mais 1,5 actif dans D1 (G-T, S+O ; hypothèse réfutée 6) ; `a_y` = 0,5 ; `okun` = 2 ; `rho_i` = 0,7 ; `lam0` = 0,2 ; `ups` = 0,05 ; `nu1`, `nu2`, `nu3` ; `eps_bar` = 0,01 ;
     - l. 289-293 : `lam_rstar` = 0,02 ; `rstar_band` = 0,01 ; `rstar_reversion` = 1 par an ;
     - l. 1294-1308 : π_s, π^e, crédibilité ;
     - l. 1366-1379 : la règle.
   - `policies.py` l. 43-71 : ancre et intégrateur à fuite.
   - Pas de décision : 4 semaines (`DECISION_WEEKS` = 4, l. 36).
2. **Équations.**
   - Taux naturel : r̂\*_{t+1} = clip(A + (r̂\* − A)e^{−1/13} + 0,02(π_s − π\*) ; A ± 0,01).
   - Règle : i^cible = [r̂\* + min(π^e, π_s + 0,5) + 1,5(π_s − π\*) − 0,5·2(u − u_n)]⁺, lissée par 0,7.
   - Anticipations : Δπ^e = [0,2(π − π^e) + c(π\* − π^e) + 0,05(g_M − g_Y − π^e)]/13.
   - Crédibilité : loi K1a, l. 1305.
   - Bornes : π^e dans [−0,1 ; 12].
3. **État stationnaire** (calcul à la main ; G_I = 0,02/(1 − e^{−1/13}) = 0,2702).
   - Quand c = 0, π^e = π̄ et π̄ − π\* = (r̄ − A − a_y·écart)/(a_π + G_I) : une **vitesse** (0,02, ρ_rev) fixe l'arrivée (échec des critères 6 (a) et 7).
   - Remesure de cohérence sur la décomposition D1 (R) : r̂\* − A = 0,514 = 0,2702 × écart, soit un écart lu de **1,90 point**, cohérent avec une inflation d'environ 4 % (G1 : 4,048 %, S+O). La règle lisant le log annualisé, s'y ajoute e^{π\*} − 1.
   - Sous cet écart supérieur à 1 point, le bonus de crédibilité est éteint : c décroît de ν_2·|écart| par an jusqu'à 0. C'est la crédibilité nulle de D1 (O) et la loi K1a (L, O).
4. **Comportement mesuré.**
   - G1 : 4,048 % (S+O) ; J1a : biais d'environ 2 points indépendant de la cible (S+O) ; J1b, K1 (S+O) ; D1 : taux réel de 5,12 % (R).
   - Maquette, au meilleur cas (A = r̄, donc π̄ = π\*, c = 1), sous T9 : rayon 0,998245 à 2 % (demi-vie 395 tours). **Pire valeur sur G : 1,0135 (période de 16,0 tours, λ_w ×2, régime de baisse) : instable.**
5. **Coût.** Conforme.
6. **Défauts.**
   - Intégrateur à fuite et bande (critère 6 (a)).
   - Loi à seuil.
   - Drapeaux `rstar_mode`, `rstar_anchor`, `wsps2`.
   - Écrêtages : bande, π^e, crédibilité, (·)⁺, `i_max`.
   - Ancre « deposit_wedge » importée du ménage de la v2.0, sans équivalent v3.
   - Historique des prix.
   - Instabilité 4 : l'ancre et la bande en étaient le remède, mais elles ont produit le biais (J1a).
7. **Identités.** Fonds propres de la banque centrale par différence (ADR 0005, Contexte) ; résultat tronqué (`model.py` l. 1208, écarté par M22 (d)).
8. **Joueur.** Une crédibilité à 0 pour toujours (O), illisible.
9. **Empreinte.** r̂\*, π_s, i_{t−1}, π^e, c, M_{t−1}, Y_{t−1}, M^hist, et l'historique des prix.

### 3.N Socle commun des options nouvelles (Q4 à Q10)

- **N-1, cible (Q4).** π\* est un paramètre au socle ; le bloc 8 reconduit π\*_{t+1} = π\*_t en phase 1 (ADR 0010, pt 3 ; #61). Le levier ouvre au J4 sur le verdict de #54 ; mesure indicative au § 3.C-4.
- **N-2, corridor (Q5).** Largeur nulle, i_res = i_CB (M31 (g)). Le levier « taux directeur » est i_CB, taux du refinancement et des réserves. #26, pt 5, est clos par la forme (i) de M31.
- **N-3, bilan (Q6).**
  - **Forme (ii), E^CB_0 = 0** : seule valeur dont le ratio est stationnaire sous M22 (d). Remesure de [(1 + g)(1 + π̄)]^{−60} : 0,3048 / 0,0929 / 0,0010 à π̄ = 0 / 2 / 10 %.
  - Π^CB = [i_CB(E^CB + M^G) + (i_CB − i_res)Res + (i_B − i_CB)B_CB]/n_a = i_CB·M^G/n_a ≥ 0 si et seulement si i_CB ≥ 0.
  - **#26, pt 1** : sans plancher (lecture (b) du § 5), une perte i_CB·M^G/n_a < 0 est possible. Elle est compensée par l'émission en position α, sauf placement raté. La part non versée serait alors une **ligne nommée « versement rationné du résultat »**, avec E^CB réduit, à décider avec la fiche 9.
  - Formes fermées de C, avec les grandeurs de la maquette : H = Res = max(B_CB − M^G\* − E^CB ; 0) = 0 ; L^CB = M^G\* = 0,017536 année de PIB à 2 %.
- **N-4, achats (Q7).** 19b-banque nulle ; s_CB = 0, paramètre d'archétype. Achats neutres sous i_B = i_res = i_CB (fiche 7 § 7, condition 6). Non ouverts au J4.
- **N-5, fermeture (Q8, #44).** Fermeture **monétaire** : r̄ est résolu par l'action intégrale (C2). Les lectures (1) et (2) inversent une même fermeture. État initial en lecture (1) : r̄ = 1 % de Fisher, s_G résolu.
- **N-6, taux réel lu (Q9, #49).** Forme de Fisher sur π\*, 1 + i = (1 + r̂\*)(1 + π\*), cohérente avec S1 : ϱ_L − ϱ̄_L = (i_L − i_{L,0})/(1 + π\*). Le taux restitué reste r = i − π (l. 214). Sous C2, la forme ne touche ni l'arrivée ni les allocations, seulement la valeur de r̂\* affichée.
- **N-7, phases.**
  - Phase 1 : π_{t−1} et P_{t−1} au registre ; puis la règle, π^e_{t+1}, π\*_{t+1} et Π^CB ; ordre interne au bloc.
  - Phase 7 : rien sous A8.
  - Phase 8 : (a) lignes 12 et 13 ; (b) ligne 16.
  - Aucun ordre nouveau entre blocs ; matrice des lectures triangulaire.
- **N-8, critère 1 (c), cas à la main.** Cas du § 3.K de la fiche 7, i_CB de 3 à 4 %, achat de 25 de titres à la banque en phase 7, M^G\* = 20.
  - Lignes : 13 = 0,04 × 20/12 = 0,06667 ; 12 = 0 ; Π^CB = 0,06667 = ligne 16 ; 21 = −20.
  - Clôture : B_CB = 25 ; L^CB = 0 ; Res = 5 ; M^G = 20.
  - E^CB : 25 + 0 − 5 − 20 = 0 par le stock ; 0 + 0,06667 − 0,06667 = 0 par les flux.
  - Contrainte budgétaire : ΔB_CB + ΔL^CB = 25 − 20 = 5 = ΔRes + ΔM^G + Π^CB − ligne 16 = 5 + 0 + 0.

  Calcul à la main, non rejoué en fractions exactes.

### 3.C Option C — action intégrale sans fuite (Fisher sur π\*) et anticipation à gain constant (nouvelle)

1. **Source.**
   - Taylor (1993), p. 202 : forme proportionnelle.
   - Action intégrale : v1.5 l. 1030 (« terme intégral »), sans clip ni log.
   - Loi d'anticipation : apprentissage à gain constant de la moyenne (Evans ; voir § 3.0) ; gain calé sur Gáti (2022), p. 19-20.
2. **Équations** (choix de conception, sauf mention).
   - (C1) 1 + i_t = (1 + r̂\*_t)(1 + π\*_t) + a_π(π_{t−1} − π\*_t).
   - (C2) r̂\*_{t+1} = r̂\*_t + (k_I/n_a)(π_{t−1} − π\*_t).
   - (C3) π^e_{t+1} = π^e_t + (λ_e/n_a)(π_{t−1} − π^e_t), en phase 1. C'est l'apprentissage à gain constant de la moyenne (*approchée*).
   - (C4) i_res = i_B = i_CB ; Π^CB par la l. 493 ; π\*_{t+1} = π\*_t.

   **Calibration retenue** (critère 12) : a_π = 0,5 ; k_I = 0,25 par an ; λ_e = 0,2 par an (Gáti) ; mesure : glissement ; aucun terme d'activité ; aucun plancher (lecture (b)).
3. **État stationnaire** (à la main).
   - (C2) impose π̄ = π\* quels que soient r̄, a_π, k_I et λ_e.
   - (C3) donne π^e = π̄ pour tout λ_e > 0 (C1).
   - (C1) donne r̂\* = (1 + i)/(1 + π\*) − 1 = r̄.
   - Aucune vitesse n'entre. Condition d'existence : aucune, sans plancher.
   - Taux réel de l'état initial : r̄ = 1 %, i = 3,02 % ; r = i − π̄ = 1,02 %.
   - Glissement stationnaire : (1,02)^{1/12} = 1,00165158, soit 2,0000 %. Une conversion linéaire donnerait 2,0184 % ; à 10 %, 10,4713 %.
4. **Comportement mesuré** (maquette ; sorties au § « Mesures »).
   - **Rayon, sous T9** :
     - 0,999413 à 2 %, réel, demi-vie de 1 181 tours ; 0,999270 à 0 ; 0,999814 à 10 % ;
     - pire valeur sur G : 0,999551 (k_I ×0,5) ; ζ = 8 : 0,999307 ;
     - racine dominante portée par K^vol, B_Bk et D_H ;
     - cycle perceptible, par régime de T4 : paire de module 0,8651 et de **période 18,8 tours** (demi-vie 4,8 tours) en hausse ; 0,9130 et **période 20,8 tours** (demi-vie 7,6 tours) en baisse ; mêmes valeurs à 0,01 près à 0 et 10 % *(corrigé le 04/10/2026, C48 : 0,8779, période 18,7 tours, demi-vie 5,3 tours, dérivée au coude de T4, linéarisation d'aucun des deux régimes)* ;
     - sous T_H sur le revenu retardé et T9 réel : 0,997482 (demi-vie 275 tours).
   - **Pays joué (sans reprise)** : 1,002307 / 1,007481 (1,007482 en hausse) / 1,019719 en hausse et 1,019685 en baisse à 0 / 2 / 10 % *(corrigé le 04/10/2026, C48 : 1,019711 à 10 %, au coude de T4)*. Après une dépense publique +1 % aux tours 1 à 12, i_CB s'écarte d'un point au tour **1 024 / 323 / 107** : dominance budgétaire déclarée (critère 11 (b)).
   - **Arrivée (critère 7 et C36)**, 27 branches, H = 20 demi-vies (17 228 à 30 893 pas) :
     - écarts au point fixe : G +1 % aux tours 1 à 12 au plus 3,3e−8 ; π^e +1 point au plus 9,0e−8 ; marche de cible +1 point au plus 7,8e−9 ; **tous sous 1e−6** ;
     - G +1 % permanent : au plus 5,9e−4 après 20 demi-vies (seuil 1e−3) ;
     - point fixe identique entre branches par construction : aucune vitesse dans le solveur.
   - **Gain statique** de la demande au taux (C36 (i)) : **−0,026 % de y par point**, quasi compensé. Un point de ϱ_L retire 0,0056 y d'investissement et ajoute 0,0053 y de consommation, les dividendes de F3 redistribuant l'investissement non fait. D'où, après G +1 % permanent, **Δr̄ = +918 pb**, atteint en rampe : i +0,76 point au tour 120, +2,78 au tour 600, +9,36 à l'arrivée ; écart de glissement de +0,24 point pendant plus de 120 tours. Sous T_H sur le revenu retardé : gain de −0,23 % par point, Δr̄ = +97 pb, i +0,67 point au tour 120.
   - **#56, branche (A) de référence** (règle en vigueur, +1 point aux tours 1 à 12, T9, 2 %) :
     - cumul de production aux tours 1 à 12 : **−0,160 %** ; P_36 < P_36^réf. **P1 tenu.**
     - premiers écarts : I^vol au tour 2 ; y, C^vol et P au tour 3 ; aucun au tour 1. **P2 tenu.**
     - écart maximal de y sur les tours 1 à 36 : 0,254 % (plancher 0,2 %) ; de glissement : 0,39 point. **P3 tenu.**
     - branche (B) : P_120 −1,81 % ; glissement −0,15 point ; écart maximal de y 0,256 % (plafond 4,3 %).
     - Mêmes verdicts à 0 et 10 %.
     - **Pays joué : P1 inversé à 2 % et 10 %** (cumul +0,016 % et +0,181 %), tenu à 0 (−0,089 %).
   - **C44 remesurée au tour n + 1** : d(C + I)/PIB = −0,203 / −0,098 / +0,081 % en pays joué (`macro` en équilibre partiel : −0,189 / −0,087 / +0,089) ; −0,277 / −0,271 / −0,250 % sous T9.
   - **Critère 10 (b) (ii)**, taux tenu −1 point, T9 :
     - premier écart au tour 3 ; glissement +0,412 au tour 12, +0,159 au tour 60, **+0,155 au tour 120** : persistance tenue ;
     - classement **« nouveau palier »** : π̄ = **2,0847 %**, U = U^eq, I/PIB 14,50 % au lieu de 13,95, C/PIB 64,90 au lieu de 65,46, tu = 0,769, atteint vers 2 400 tours ;
     - le palier de long terme (0,085 point) est inférieur à un cran. L'ancre nominale non monétaire partielle vient des plans indexés sur π\* (M27, M28) ;
     - en pays joué : **dérive continue de signe inversé** (−0,305 point au tour 120).
   - **#54, indicatif** (π\* n'est pas un levier) :
     - aller-retour −1 puis +1 pour k = 1, 3 et 12 : **« non rentable » partout** (G_24(y) de −0,015 à −0,104 %), sous T9 nominal, T9 réel, assiette élargie, règle endogène ou taux tenu ;
     - aller-retour répété : écart moyen de production de −0,04 à −0,13 % ;
     - aucun « stimulant gratuit » ; essai (3) non fait ;
     - ratio de sacrifice : 2,08 point-années par point (T9 réel), contre 1/(λ_e λ_w β) = 2,5.
   - **Critère 6 (d)** : pic de production +0,268 % au tour 6 ; sous la moitié du pic dès le tour 23 (seuil 60).
   - **Critère 18 (c)**, plancher à 0 en variante :
     - G −5 % : plancher jamais atteint (taux minimal 1,45 %) ;
     - G −15 % et −25 % : actif aux tours 11 à 19 et 8 à 21, désactivé 7 et 9 tours après la fin du choc, sans réactivation.
   - **Clause II.7, critère 12** : 6 calibrations sur 24 ont ρ_c < 1 sur toute G, 9 ont ρ_b < 1. **Verdict : non déterminant.**
     - Remesuré par régime le 04/10/2026 (C48) : décomptes (6 et 9 sur 24) et verdict inchangés, sous T9 comme sous T_H sur le revenu retardé et T9 réel.
     - Toutes les calibrations a_π = 1,5 échouent, sous (c) comme sous (b), en baisse : 1,018868 à λ_w ×2, période 17,7 tours (c) ; 1,016903, période 16,8 tours (b) ; elles sont stables en hausse *(corrigé le 04/10/2026, C48 : 1,0299, période d'environ 16 tours, obtenu avec le second coude y = min{y\*, pr·N} dans la linéarisation de la baisse)*.
     - La mesure « variation du tour » échoue sous (c) quand toutes les vitesses sont ×2.
     - Même verdict sous T_H sur le revenu retardé et T9 réel.
     - À la calibration retenue : ρ_c = 0,999413 (1 181 tours, réel) ; ρ_b = 0,999414 (1 182) ; paire perceptible en hausse 0,8651, période 18,8 (c), contre 0,8564, période 17,4 (b) ; en baisse 0,9130, période 20,8 (c), contre 0,9103, période 19,9 (b) *(corrigé le 04/10/2026, C48 : 0,8779, période 18,7 (c), contre 0,8737, période 17,4 (b), au coude de T4)*.
   - **Clause de l'ADR 0010** : ρ_1 = ρ_0 par construction. π\* est une entrée exogène, absente de la rétroaction ; mesuré identique.
5. **Coût.** Environ 35 opérations par pas, sans itération ; très au-dessous de 0,48 ms. La maquette Python complète du socle coûte 38 µs par pas.
6. **Défauts.**
   - Instabilité 4 : le fait nouveau exigé par C2 est établi en maquette (rayon inférieur à 1 sur G, arrivée), **sous T9 seulement**.
   - Racine dominante très lente (1 181 tours), traîne de r̂\* après tout choc.
   - Gain statique quasi nul : r̄ hypersensible (C15, critère 13 ; § 4).
   - a_π borné (1,5 est instable sur G) : principe de Taylor non tenu à court terme ; la stabilisation de long terme vient de l'action intégrale.
   - Sans plancher, i_CB peut être négatif (lecture (b)).
7. **Identités.** Lignes 12, 13 et 16 ; E^CB par le stock et par les flux (N-8) ; aucun solde. Portes de la monnaie inchangées.
8. **Joueur.**
   - Taux indiqué par la règle et r̂\* (« taux neutre estimé ») restitués.
   - Écart du taux décidé à la prescription.
   - Un cycle de 18,8 tours en hausse et de 20,8 tours en baisse *(corrigé le 04/10/2026, C48 : 18,7 tours, au coude de T4)* ; une traîne lente au-delà de 60 tours (résidu au tour 60 : π +0,006 point, y +0,005 %).
   - Le niveau des prix revient vers son sentier (C11) : −0,106 % au tour 60, −0,059 % au tour 240.
9. **Empreinte.** Deux variables d'état : r̂\* (par an, valeur stationnaire r̄) et π^e (par an, valeur stationnaire π̄). Aucune crédibilité, aucun historique, aucun tirage.

### 3.V Variantes à une question, combinables avec C

- **C-h, ancrage constant c̄** : π^e_{t+1} = π^e + (λ_e/n_a)[(1 − c̄)(π_{t−1} − π^e) + c̄(π\*_{t+1} − π^e)].
  - C1 exact sous C2.
  - Rayon 0,999443 ; pire valeur sur G 0,999587.
  - Taux tenu : palier semblable (+0,143 au tour 120).
  - Un paramètre de plus, aucune variable d'état.
- **C-c, crédibilité d'état revue** : c_{t+1} = c + (λ_c/n_a)[c̄/(1 + ((π_{t−1} − π\*)/κ_c)²) − c].
  - Valeur stationnaire c̄ explicite, sans seuil ; dérivée nulle à écart nul, donc inerte au premier ordre.
  - Rayon et pire valeur identiques à C-h.
  - G +5 % : c descend à 0,23 au tour 18, revient à 0,48 au tour 60.
  - Trois paramètres et un état ; aucune source ne la calibre.
- **C-g, gain endogène** (Gáti 2022, (22)-(23)) : k = λ_e + (λ_max − λ_e)(1 − e^{−(f/κ_f)²}), avec f = π_{t−1} − π^e.
  - Rayon identique à C.
  - Sous G +5 % : π^e +1,23 point au tour 12 et production −1,76 % (désancrage).
  - Deux paramètres, aucun état.
- **D, corridor explicite** : i_res = i_CB − Δ^res. Inerte au socle (Res = 0 tant que B_CB < M^G\* + E^CB) ; un paramètre ; transmis au J6 avec le levier d'achats.
- **T, Taylor à r\* fixe** : π̄ − π\* = (r̄ − r\*)/a_π, soit **2 points par point d'erreur sur r\* à a_π = 0,5**. Rayon 0,998007 si r\* = r̄ exactement. Écarté au titre du critère 6 (a).
- **Formation de π^e en phase 9** (délai prix → salaire d'un tour au lieu de deux) : rayon identique (0,999413). Elle retouche `tab:phases` (décision citant M22 et M29, ADR). Non retenue.
- **R, sans retard** (π^e ≡ π\*, règle en lecture (b)) : rayon 0,999469. Référence seulement.

## 4. Tableau comparatif

Abréviations : « ×2 » renvoie à la grille G du critère 12 (vitesses et gains ×0,5 et ×2) ; « h » désigne une demi-vie en tours.

| Critère | A (v1.5) | B (v2.0) | C (recommandée) | C-h / C-c / C-g | D, T, R |
|---|---|---|---|---|---|
| 1 Stock-flux | écart : `eq:ecb` sans receveur, Σ avec report (3.A-7) | écart : E^CB par différence (3.B-7) | conforme (N-8) | comme C | D : comme C ; T, R : comme C |
| 2 E^CB, perte | report des pertes, contraire à M22 (d) | troncature | (ii) ; perte possible si i < 0, ligne nommée (N-3) | comme C | comme C |
| 3 Corridor | Δ^res non nul, sur min(·) | — | largeur nulle (N-2) | comme C | D : inerte au socle |
| 4 Phases et lectures | écart : lit π du pas | historique | conforme (N-7) | phase 9 : retouche de `tab:phases` | R : viole la lecture (c) |
| 5 Mesure et cible | **échec** : log contre glissement, π̄ = e^{π\*} − 1 | **échec** (idem) | conforme ; Fisher sur π\* (N-6) | comme C | comme C |
| 6 (a) C2 | intégral, mais clip et log | **échec** : fuite (3.B-3) | conforme (3.C-3) | conforme | T : **échec** |
| 6 (b) C3 | non | non (D1 préparé) | conforme | conforme | — |
| 6 (c) #44 | — | — | monétaire, lecture (1) (N-5) | idem | — |
| 6 (d) C36 | non mesuré (transposition) | — | (i) tenu, gain −0,026 %/pt ; (ii-a), (ii-b), (iii) tenus sous T9 ; **échec en pays joué** | idem | — |
| 7 Vitesses | dépend du clip | **échec** | conforme ; arrivée < 1e−6 ; G permanent 5,9e−4 | comme C | — |
| 8 Anticipations | **échec** de C1 (υ, c) | **échec** (2,2 contre 3) | conforme ; λ_e = 0,2 ; phase 1 | conforme sous C2 | R : C1 trivial |
| 9 Crédibilité | **échec** : seuil, borne active | **échec** : seuil (K1a) | sans objet (option sans crédibilité) | C-c : conforme ; C-g : ancrage sans état | — |
| 10 (b) (i) Cible +1 point | biais e^{π\*} | biais d'environ 2 points | conforme (marche : arrivée 7,8e−9) | conforme | — |
| 10 (b) (ii) Persistance | non mesuré | non mesuré | **tenue** : +0,155 au tour 120, palier 2,085 % ; pays joué : signe inversé | C-h : +0,143 | — |
| 10 (b) (iii) Régime v2.0 | non reproduit | — | non reproduit | — | — |
| 11 (a) Rayon | 0,99948 ; pire sur G 0,99953 | pire sur G **1,0135** | 0,999413 ; pire sur G 0,999551 ; à 0 et 10 %, ζ = 4 et 8 : inférieur à 1 | 0,99944 à 0,99947 | T : 0,998 |
| 11 (b) Contenu de C10 | — | — | délai 1 ; glissement ; période 18,8 (hausse) et 20,8 (baisse) *(corrigé le 04/10/2026, C48 : 18,7)* ; h 1 181 ; pays joué : tours 1 024 / 323 / 107 | — | — |
| 11 (c) C14 | — | — | gain statique négatif mais quasi nul | — | — |
| 11 (d) C26 | non déclenchée | non déclenchée | non déclenchée | non déclenchée | non déclenchée |
| 12 II.7 | — | — | **non déterminant** | — | R = (b) |
| 13 C15 | — | — | **échec** pour toutes les options : r̄ de −7,9 % à −17,7 % (T9 nominal), de 5,7 % à 2,6 % (T9 réel), contre 1 % ; source hors bloc 8 | idem | idem |
| 14 Canaux et délais | — | — | (a), (b), (d), (e), (g) conformes ; C33 déclarée ; C^vol dès n + 1 en pays joué | idem | — |
| 15 #56 | — | — | P1, P2, P3 tenus sous T9 ; P1 inversé en pays joué à 2 et 10 % | — | — |
| 16 #54 | — | — | indicatif : non rentable partout | — | — |
| 17 Test zéro | J3 | instable | préalable tenu | — | — |
| 18 Bornes | six écrêtages, dont un actif à l'état stationnaire | cinq ou plus | 0 (plancher en lecture) ; variante : désactivé en 9 tours au plus | 0 | — |
| 19 Lisibilité | crédibilité en falaise | crédibilité nulle | prescription, r̂\*, π^e − π\* | C-c : indicateur | — |
| 20 Empreinte | sept états | huit états et historique | deux états | C-c : trois ; C-g : deux | T : un |
| 21 Coût | conforme | conforme | conforme (environ 35 opérations) | conforme | conforme |
| 22 Notation | collisions (k, c, ν, ρ_i) | — | r̂\* ; k_I ; λ_e : zéro occurrence dans le `.tex` (grep) | — | — |
| 23 Calibrabilité | Taylor (1993) | — | λ_e : Gáti (2022, lu) ; a_π et k_I : sans source | — | — |
| 24 Faits | R | L, S+O, O | — | — | — |

## 5. Avis de l'expert pilote

*`monnaie`, 04/10/2026.*

**Recommandation : option C**, avec le socle commun du § 3.N :
- action intégrale sans fuite sous la forme de Fisher sur π\*, lisant le glissement ;
- a_π = 0,5, k_I = 0,25 par an ;
- anticipation adaptative, c'est-à-dire apprentissage à gain constant de la moyenne, avec λ_e = 0,2 par an, formée en phase 1 ;
- aucune crédibilité au socle ; l'indicateur d'ancrage restitué est π^e − π\*.

**Motifs, critère par critère.**
- C est la seule option qui tient à la fois π̄ = π\* et π^e = π̄ sans vitesse ni borne (critères 5 à 8).
- Son rayon est inférieur à 1 sur toute la grille, dans les deux régimes, à 0, 2 et 10 %, et pour ζ = 4 et 8, sous T9 (critère 11 (a)) : c'est le fait nouveau qui lève l'instabilité 4 sous la règle de référence.
- Elle a deux variables d'état et aucune borne (critères 18 et 20).
- A et B échouent aux critères 5, 6 (a), 8 et 9 ; B est en outre instable sur G.
- T laisse un biais de 2 points par point d'erreur sur r\*.

**Réserves, critères écrits avant l'essai, au J3 :**
1. Rayon de la boucle conjointe inférieur à 1 sur G, sous la règle budgétaire que retiendra M33.
2. Arrivée à 1e−6 en 20 demi-vies.
3. a_π ∈ ]0 ; 1,5[ contrôlé au chargement de la table de calibration.
4. Formes fermées de 3.C-3 à 1e−10 près.
5. Persistance du critère 10 (b) (ii) remesurée.

**Ce qui dépasse le bloc 8 et que je porte au mainteneur** (aucune option du bloc ne le change, la forme de la règle n'entrant pas dans l'état stationnaire) :
- **(1) Gain statique quasi nul.** Avec T_H sur WB, il vaut −0,026 % de y par point : r̄ dérive de +9 points après G +1 % permanent, en rampe (+0,76 point au tour 120), et le critère 13 (C15) échoue largement. Il dépend surtout de l'assiette de T_H et de la forme de T9 (fiche 9) : −0,23 % par point sous l'assiette élargie.
- **(2) Pays joué sans reprise.** Il est explosif sous toute règle à action intégrale (doublement de l'écart en 93 tours à 2 %, en 36 tours à 10 %). #56 s'y inverse : dominance budgétaire. C'est la condition C37 portée au pays joué.
- **(3) Faible effet de long terme d'un taux tenu.** Un taux tenu un point plus bas ne laisse qu'un palier d'inflation de +0,085 point à long terme (+0,155 point au tour 120), à cause de l'indexation des plans sur π\* (M27, M28). C'est à confronter à l'intention reconfirmée du 17/09/2026.

**Lectures soumises au mainteneur** (mon avis entre parenthèses) :
- (a) Taux de la règle au-dessus du principe de Taylor (a_π = 1,5), instable sur G, contre **a_π = 0,5** (0,5).
- (b) **Aucun plancher de i_CB au socle** (cohérent avec M31 (d) et l'absence de billets), contre un plancher à 0, borne à seuil libre mesurée au critère 18 (c) (aucun plancher).
- (c) **Crédibilité.** Quatre formes : aucune ; c̄ constant ; C-c ; C-g (aucune au socle ; C-g, adossée à une source, au J4 ou au J6 si `jeu` demande un indicateur d'ancrage).
- (d) **Formation de π^e en phase 1** (aucun changement de tables) ou en phase 9 (phase 1).
- (e) **#44** : état initial en lecture (1), r̄ donné et s_G résolu, ou en lecture (2) (lecture (1)).

**Points renvoyés à M33** (avis, non tranchés) :
- lignes 19a : A8 ;
- i_B : option (i), i_B ≡ i_CB ;
- M^G\* : renvoyé à la fiche 9, sans effet sur les revenus sous i_res = i_B = i_CB ;
- E^CB : forme (ii) ;
- fermeture : monétaire.

**Coût en fidélité.**
- Le principe de Taylor n'est pas tenu à court terme.
- L'inflation a une persistance adaptative.
- Aucune crédibilité au socle.
- La traîne est séculaire et la sensibilité de r̄ extrême ; cela relève des fiches 6 et 9.

**Questions pour `macro`** (§ 6) :
1. Quelle assiette de T_H et quelle forme de T9 (nominale ou réelle) retenez-vous ? Le gain statique, Δr̄ et C15 en dépendent d'un facteur 10.
2. Le palier de +0,085 point (taux tenu −1 point) relève-t-il de l'indexation des plans sur π\* ? Faut-il le porter au titre du critère 10 (a) ?
3. Quelle règle du pays joué neutralise la divergence (reprise automatique, ou levier d'impôt défini net des intérêts) ?
4. θ_H effectif vaut 0,498 à l'impact (F3) : est-ce cohérent avec la fiche 9 ?
5. Acceptez-vous λ_e = 0,2 par an (ratio de sacrifice de 2,1 point-années) pour la calibration conjointe de #45 ?
6. Le partage de C30 entre consommation et investissement explique-t-il la compensation de 95 % du gain statique ?

**Questions pour `jeu`** (§ 7) :
1. Un cycle d'environ 19 tours et une traîne séculaire : est-ce lisible ?
2. Une rampe du taux de +0,76 point en 120 tours après une dépense publique permanente : est-ce acceptable ?
3. Indicateur d'ancrage π^e − π\* ou crédibilité d'état C-c ?
4. Un taux directeur négatif sans plancher : l'acceptez-vous ?
5. En pays joué, la hausse de taux est expansionniste à 2 et 10 % : faut-il l'afficher, ou exiger la reprise ?
6. #54 « non rentable » partout : suffit-il pour ouvrir le levier de cible au J4 ?
7. Restituer r̂\* (« taux neutre estimé ») et la prescription ?

> **État du jalon 2 (04/10/2026)** : instruction **partielle**. Restent à faire : la contre-épreuve indépendante de la maquette conjointe (critère 11), l'essai (3) du critère 16 (#54, sous cible nominale) et toute remesure de statut V sur le prototype v2.0 (critère 24 (b)). La maquette conjointe de `monnaie` (scripts `f8_modele.py`, `run1.py` à `run17.py`, `chk1.py` à `chk3.py`) est conservée hors du dépôt par la session ; son versement au compte rendu ou dans `outils/` (par `coder`, puis `audit`) est à décider.

## 6. Avis de l'expert consulté

*Rédigé par `macro` (expert consulté pour la frontière inflation côté prix et salaires, la fermeture du niveau d'activité et la dette publique, avec la fiche 9 dont il est pilote) le 04/10/2026. Avis porté sur la fiche à l'état `f07d02f` (branche `claude/j1-monnaie-etat`, PR #77). Les conditions nouvelles sont numérotées C45 à C50 (§ 6.6), sous réserve de l'ordre réel d'intégration.*

*Sources lues :*
- *fiche 8 : § 1 à § 5 ;*
- *fiche 9 : critères 5, 6, 9, 11, 13 et 14 ;*
- *fiche 7 : § 6 ;*
- *spécification :*
  - *`sec:cadre-calendrier`, `sec:cadre-bilans`, `sec:cadre-flux`, `sec:cadre-caisse`, `sec:cadre-phases` (l. 180 à 541) ;*
  - *équations N1 à N11, T1 à T6, P1 à P4, H2 à H7, S1 à S7, F1 à F4, B1 à B8 ;*
  - *l. 1543 (θ_H) et `tab:calibration` ;*
- *constats de `jeu` transmis le 04/10/2026.*

*Calculs : maquette propre de `macro`, écrite depuis la spécification dans un répertoire créé par `mktemp -d`. Elle n'importe ni la maquette de `monnaie` ni `archive/`. Elle reprend les hypothèses déclarées par `monnaie` au § 3.0 :*
- *bloc 9 provisoire : T9, T_H = τ·WB avec τ = 0,25, M^G\* = G + i_B B/n_a, G en volume indexé sur la production potentielle ;*
- *A8 avec s_CB = 0, et i_B = i_res = i_CB ;*
- *option C avec a_π = 0,5, k_I = 0,25 par an et λ_e = 0,2 par an ;*
- *ζ = 4, ϖ_L = 2 %, ϖ_D = 1 %, ϑ = 0,10 ;*
- *état initial résolu en lecture (1) de #44.*

*Les deux régimes de T4 sont linéarisés séparément. L'état est normalisé par le dernier prix connu et la production potentielle, ce qui retire la racine nominale. Les fonds propres E^CB et E^Bk sont rattachés aux identités de bilan, ce qui exclut toute perturbation hors bilan. Les sorties de la maquette sont des résultats de modèle, sans statut de fait. Coût : 15,2 µs par pas.*

### 6.1 Réponses aux six questions de `monnaie`

**Q1 — Assiette de T_H et forme de T9.**

Ma recommandation, provisoire et à trancher à M33 : pour la maquette conjointe et l'instruction de la fiche 9, prendre **T9 réel**, avec **T_H assis sur le revenu avant impôt retardé**.

1. **T9 doit être réel.**
   - Sous T9 nominal, le taux de référence est fixe en nominal. Un changement de cible prélève alors Δπ × (B − M^G − E^CB)/n_a sur les ménages, un impôt forfaitaire sans motif.
   - Mesure, à s_G et ϱ̄_L tenus à leurs valeurs de π\* = 2 % :
     - sous T9 nominal, r̄ vaut −7,87 % à π\* = 0 et −17,69 % à π\* = 10 % ;
     - sous T9 réel, il vaut +5,73 % et +2,60 % (`c15.py`) ;
     - la référence est 1 %.
   - La reprise doit donc porter sur le surcroît de **taux réel** : le taux de référence suit π\* par Fisher (C45).
2. **L'assiette fixe le gain statique, et avec lui toute la dynamique de long terme de la règle à action intégrale.** Mesures à π̄ = 2 % :

   | Grandeur | T_H = τ·WB, T9 | T_H sur le revenu avant impôt retardé, T9 réel |
   |---|---|---|
   | Gain statique (% de y par point de i) | −0,0259 | −0,2216 |
   | Δr̄ après G +1 % permanent (Fisher) | +918 pb | +97 pb |
   | i au tour 120 ; au tour 600 | +0,76 ; +2,78 points | +0,67 ; +1,09 point |
   | Glissement − π\* aux tours 60 / 120 / 240 / 600 | +0,238 / +0,238 / +0,224 / +0,160 | +0,219 / +0,165 / +0,086 / −0,007 |
   | Inflation excédentaire cumulée, Δr̄/k_I | 36,7 point-années | 3,9 point-années |
   | Palier, taux tenu −1 point (critère 10 (b) (ii)) | +0,085 point | +0,615 point |
   | Rayon sous la règle de référence | 0,999413 | 0,997482 |

   - L'identité de la quatrième ligne est exacte sous C2 : r̂\* doit se déplacer de Δr̄, et il ne se déplace que par k_I·Σ(π_{t−1} − π\*)/n_a.
   - Seuls un gain statique plus fort ou un k_I plus grand réduisent donc la traîne. C'est la réponse au constat (1) de `jeu` : sous l'assiette élargie, l'écart reste au-dessus d'un cran au tour 120 (+0,165), puis passe sous un cran au tour 240 (+0,086).
3. **Pourquoi l'assiette joue autant.**
   - Sous l'assiette WB, l'investissement qu'une hausse de taux évite retourne aux ménages par Div_F, et n'est pas imposé (Q6).
   - Sous l'assiette élargie :
     - un quart de ce dividende est prélevé ;
     - l'impôt sur les intérêts, ajouté à T9, rend le canal rentier net négatif, soit −τ·Δi·(B − M^G − E^CB)/n_a.
4. **Réserves** :
   - sous l'assiette élargie, le critère 13 échoue encore (§ 6.3) ;
   - à π\* = 0, la recherche de racines trouve **deux valeurs stationnaires de r̄** dans [−60 % ; +100 %] (+5,20 % et −15,44 % sous T9 nominal ; +3,11 % et −21,53 % sous T9 réel). L'unicité est à examiner au comptage du critère 4 (b) de la fiche 9 ;
   - un impôt sur les intérêts nominaux rend le rendement réel après impôt dépendant de π̄. C'est déjà déclaré au critère 13 (c).

**Q2 — Palier de +0,085 point.**

Oui, il relève à mon avis de l'indexation des plans en u.m. sur π\* :
- S4 et F2 ;
- l'entretien γ^e de H3 et H4 ;
- G^plan.

Un excès de π sur π\* y devient une baisse du volume demandé. Le palier vaut à peu près le gain statique × Δi, rapporté à cette sensibilité.

La mesure le confirme : sous l'assiette élargie (gain multiplié par 8,5), le même taux tenu donne un palier de +0,615 point (+0,402 au tour 120), au lieu de +0,085 (`palier.py`).

Je n'ai pas testé la neutralisation de l'indexation : c'est une hypothèse cohérente avec la mesure. Les deux régimes donnent un « nouveau palier », sans « retour », et l'exigence du critère 10 (b) (ii) est tenue au tour 120 (+0,155 et +0,402).

Je recommande de le porter au mainteneur au titre du critère 10 (a), comme information, non comme échec : l'effet de long terme d'un taux tenu existe, son ampleur est réglée par la règle budgétaire.

**Q3 — Règle du pays joué qui neutralise la divergence.**

Il faut **une reprise automatique et quasi intégrale du surcroît d'intérêts réels**. Rayon selon la part φ de T9 reprise (`joue.py`) :

| φ | 0 | 0,5 | 0,75 | 0,9 | 1 |
|---|---|---|---|---|---|
| π̄ = 2 % | 1,007482 | 1,003141 | 1,001130 | 1,000033 | 0,999413 |
| π̄ = 10 % | 1,019719 | 1,008420 | 1,003738 | 1,001249 | 0,999814 |

- L'assiette élargie seule, sans reprise, ne suffit pas : 1,001642 à 2 % et 1,010681 à 10 %.
- Avec T9 réel, elle tient : 0,997482 et 0,998306.
- Un levier d'impôt « défini net des intérêts » ne neutralise la divergence que s'il finance automatiquement le surcroît d'intérêts. C'est alors T9 sous un autre nom.

Je rejoins `jeu` : **la valeur par défaut du levier budgétaire devrait être une règle avec reprise**, et « leviers tenus » un écart déclaré (régime « intérêts financés par le déficit », fiche 9, critère 9 (d)), avec la charge d'intérêts restituée.

Constat (2) de `jeu` reproduit : à π̄ = 10 %, une hausse d'un point aux tours 1 à 12 donne +1,45 point de glissement au tour 120 et +36,95 au tour 240. C'est à instruire à la fiche 9 (critères 9 (d) et 19) et à trancher à M33 (C47).

**Q4 — θ_H effectif de 0,498.**

Ce chiffre n'est pas le θ_H de la l. 1543, qui est la part de la valeur de la production marginale qui atteint le revenu des ménages dans le pas.

Je le reproduis comme **ΔDiv_F/ΔG au tour 1**, soit 0,4983 :
- au tour 1, la production ne varie pas (Δy = 0) ;
- le PIB ne monte que de la marge, soit ΔPIB/ΔG = 0,2018 ;
- F2 garde en dépôts environ ν_F·λ_v ≈ 0,5 de la vente imprévue.

C'est cohérent avec F, mais c'est un autre objet. La fiche 9 publiera les deux grandeurs (critère 14 (c)) :
- la part d'une vente imprévue qui atteint les ménages ;
- θ_H au sens de la l. 1543, sous chaque règle. Sous T_H = τ·WB, sa part salariale vaut (1 − τ)·UC/p = 0,6. Le reste n'est pas mesuré.

**Q5 — λ_e = 0,2 par an pour #45.**

Je l'accepte comme valeur indicative de la maquette, non comme calibration.
- La racine dominante y est insensible : 0,999411 à λ_e = 0,1 et 0,999414 à 0,4.
- λ_w = 1 est déjà déclarée au-dessus des ordres de grandeur sourcés (`tab:calibration`). Si le J3 la baisse, 1/(λ_e λ_w β) monte d'autant. La calibration reste conjointe au J3.
- Je n'ai pas remesuré le ratio de sacrifice de 2,08. Je ne cite aucun ratio empirique (Ball, 1994, non lu).

**Q6 — Compensation de 95 % du gain statique.**

Elle ne vient pas de C30, qui ne joue que sur la dépendance à π̄ (critère 13). Elle vient de F3 et de la norme stationnaire des ménages.
- À l'état stationnaire de plein emploi, C^vol + I^vol + G^vol = v.
- Un point de taux retire 0,00537 y d'investissement en volume et ajoute 0,00512 y de consommation, soit un rapport de 0,953.
- F1 et F2 fixent le crédit et les dépôts. F3 verse donc l'investissement non fait en dividendes.
- La propension stationnaire des ménages au revenu vaut 1 − γ̄·n_a ν_H/(1 + n_a ν_H π\*^pas) = 0,961 à 2 % (calcul à la main). Le revenu disponible reprend donc environ 99 % de l'investissement non fait (déduit, non mesuré séparément).
- Sous T9, le canal rentier est neutralisé. Rien ne fait alors dépendre l'épargne des ménages du taux (M27).

Par point de ϱ_L, je trouve 0,00548 et 0,00522 y, contre 0,0056 et 0,0053 publiés. L'écart de 2 % peut venir d'une dérivée contre une différence d'un point ; il n'est pas éclairci.

### 6.2 Contre-épreuve indépendante (critère 11)

| Grandeur | Publiée (`monnaie`) | Remesure de `macro` | Verdict |
|---|---|---|---|
| K/(12 PIB) à 0 / 2 / 10 % | — / 1,55510 / — | 2,00092 / 1,55510 / 0,83598 | reproduite |
| L/(12 PIB) ; D_F/(12 PIB) | 0,80037 / 0,62204 / 0,33439 ; 0,16605 | idem ; 0,16636 / 0,16605 / 0,16492 | reproduite |
| I/PIB ; M^G\*/(12 PIB) à 2 % | 13,945 % ; 0,017536 | 13,94 % ; 0,017536 | reproduite |
| Résidu d'un pas ; E^Bk stock − flux | 3,6e−15 ; 2e−15 | ≤ 3,6e−15 ; ≤ 1,7e−15 | reproduite |
| Rayon sous T9 à 0 / 2 / 10 % | 0,999270 / 0,999413 / 0,999814 | idem, dans les deux régimes | reproduite (écart < 1e−6) |
| Paire complexe | 0,8779, période 18,7 | hausse : 0,8651, période 18,84, h 4,8 ; baisse : 0,9130, période 20,84, h 7,6 ; 0,8779 et 18,75 seulement en dérivant au coude de T4 | **non reproduite : artefact** (C48) |
| Pays joué à 0 / 2 / 10 % | 1,002307 / 1,007481 / 1,019711 | 1,002307 / 1,007481 (baisse ; hausse 1,007482) / hausse 1,019719, baisse 1,019685 ; 1,019711 au coude | reproduite à 0 et 2 % ; à 10 %, même artefact |
| Tour où i s'écarte d'un point en pays joué | 1 024 / 323 / 107 | idem | reproduite |
| Gain statique ; Δr̄ après G +1 % permanent | −0,026 % ; +918 pb | −0,0259 % ; +918 pb (Fisher ; +936 pb en i) | reproduite |
| Rampe de i aux tours 120 / 600 | +0,76 / +2,78 | idem | reproduite |
| Arrivée après G +1 % permanent, 20 demi-vies | ≤ 5,9e−4 (27 branches) | 4,8e−5 sur i, H = 23 610, calibration seule | reproduite (une branche) |
| Assiette élargie : gain ; Δr̄ ; i au tour 120 ; rayon | −0,23 % ; +97 pb ; +0,67 ; 0,997482 | −0,2216 % ; +97 pb ; +0,67 ; 0,997482 | reproduite (gain à 0,01 près, non éclairci) |
| #56 (A) à 2 % : cumul ; P_36 ; premiers écarts ; P3 | −0,160 % ; P_36 < réf ; I^vol au tour 2, y, C^vol et P au tour 3 ; 0,254 % et 0,39 point | idem (P_36 −0,138 %) | reproduite |
| #56 (B) : P_120 ; glissement ; écart maximal de y | −1,81 % ; −0,15 ; 0,256 % | idem | reproduite |
| #56 en pays joué à 0 / 2 / 10 % | −0,089 / +0,016 / +0,181 % | −0,088 / +0,016 / +0,181 % | reproduite (3e chiffre à 0 %) |
| Critère 10 (b) (ii) | tour 3 ; +0,412 / +0,159 / +0,155 ; palier 2,0847 % | idem ; 2,0847 % (dérive 1e−9 sur 1 000 tours) | reproduite |
| Taux tenu en pays joué, tour 120 | −0,305 | −0,305 (−0,542 au tour 600) | reproduite |
| Constats de `jeu` | +0,24 point aux tours 60 à 240 ; +0,165 au tour 120 (assiette élargie) ; +1,45 / +37 en pays joué | +0,238 / +0,224 / +0,160 aux tours 60 / 240 / 600 ; +0,165 ; +1,45 / +36,95 | reproduite |
| Critère 13, r̄ à π\* = 0 / 10 % | −7,9 / −17,7 % (T9 nominal) ; 5,7 / 2,6 % (T9 réel) | −7,87 / −17,69 % ; +5,73 / +2,60 % | reproduite |
| θ_H effectif | 0,498 | 0,4983 = ΔDiv_F/ΔG au tour 1 | reproduite (lecture : Q4) |
| Pire valeur sur G, k_I ×0,5 | 0,999551 | 0,999551 | reproduite |
| a_π = 1,5 | 1,0299 (λ_w ×2, période d'environ 16) | instable : 1,018868 en baisse, période 17,7 ; stable en hausse | signe reproduit ; 1,0299 non reproduit (configuration non identifiée) |

**Non mesuré** :
- la grille du critère 12 (24 calibrations × G) ;
- l'arrivée sur les 27 branches ;
- #54 et l'essai (3) du critère 16 ;
- C44 dans la boucle ;
- les variantes C-h, C-c, C-g, D, T, R, et les options A et B ;
- ζ = 8 ;
- le critère 6 (d) ;
- le plancher (critère 18 (c)) ;
- le ratio de sacrifice.

### 6.3 Critère 13 (C15) : conséquence pour M32-M33 et instruction de la fiche 9

1. **Je confirme que la source de l'échec est hors du bloc 8.**
   - Sous la fermeture monétaire, le bloc 8 ne fixe que π̄ = π\*.
   - r̄ est fixé par l'équilibre stationnaire de la demande des blocs 5, 6, 7 et 9. Son déplacement entre deux cibles vaut, en ordre de grandeur, la dépendance de la demande privée à π̄ à taux donné, divisée par le gain statique.
   - Numérateur, en lecture (1) à r̄ = 1 % : s_G = 0,201144 / 0,202599 / 0,202482 à π̄ = 0 / 2 / 10 %. Dénominateur : −0,026 % par point.
   - Aucune option du bloc 8 ne change ce rapport : aucun paramètre de la règle n'entre dans l'état stationnaire.
2. **Pour la décision par paire**, je recommande :
   - que M32 retienne l'option du bloc 8 sur ses propres critères ;
   - que le critère 13 reste ouvert comme **condition de M33** : la fiche 9 doit montrer une règle qui le tient au seuil adopté, ou établir qu'aucune ne le peut.
3. **Dans ce dernier cas, deux voies sont au mainteneur** :
   - une correction prospective du critère 13, l'ancien verdict restant publié ;
   - la réouverture d'une sensibilité de l'épargne au taux, côté ménages (fiche 5, Q3, point 4) ou côté distribution des entreprises.

   Le critère 11 (c) (C14) est tenu au pied de la lettre, puisque le gain est négatif. Je ne propose pas d'y ajouter un seuil après observation.
4. **Ce que la fiche 9 doit instruire**, sur la même maquette :
   - (a) T9 sous forme réelle (C45) ;
   - (b) au moins trois assiettes : WB, revenu avant impôt retardé, et l'une ou l'autre avec T9 réel. Pour chacune : gain statique, Δr̄, critère 13, palier du critère 10 (b) (ii), Δr̄/k_I, rayon et #56 ;
   - (c) le seuil φ\* de reprise partielle ;
   - (d) une règle de rappel de la dette, proportionnelle seulement, sans action intégrale sur l'activité (critère 6 (b)) ;
   - (e) la décomposition de la dépendance de la demande privée à π̄ : C30, H3, impôt d'inflation sur les dépôts, forme de T9, impôt sur les intérêts nominaux ;
   - (f) l'unicité de r̄ stationnaire ;
   - (g) θ_H sous ses deux définitions ;
   - (h) la valeur par défaut du levier budgétaire en pays joué.

### 6.4 Lectures (a) à (e) du § 5 : avis de `macro`

- **(a) a_π = 0,5.**
  - Sous a_π = 1,5 et λ_w ×2, la boucle salaires-prix est instable en baisse : 1,018868, période 17,7 tours.
  - Sous a_π = 0,5, elle est stable sur les cas que j'ai mesurés : λ_w ×2 et k_I ×0,5 et ×2.
  - La stabilisation de long terme vient de l'action intégrale.
- **(b) Aucun plancher.** Sans billets, aucun arbitrage ne le motive au socle. Je signale à `jeu` que i_D = i_CB − ϖ_D devient négatif dès que i_CB < 1 %.
- **(c) Aucune crédibilité au socle.**
  - Ni C-h ni C-c n'ont d'effet stationnaire.
  - C1 tient sans elles, et la règle SN reste exacte.
  - C-g change la dynamique salariale : à instruire au J4 ou au J6 seulement.
- **(d) Formation en phase 1.**
  - Elle laisse `tab:phases` inchangée.
  - Le délai prix → anticipation → salaire est de deux tours, et la condition de Barro et Gordon tient : la π^e consommée au tour n est formée en phase 1 du tour n − 1, sur π_{n−2}.
  - Le rayon est identique sous la formation en phase 9 (`monnaie`).
- **(e) Lecture (1) de #44.** C'est la seule bien conditionnée sous la règle actuelle :
  - en lecture (1), s_G varie de 0,026 % de y par point de r̄ : choisir r̄ est presque libre ;
  - en lecture (2), r̄ varierait d'environ 38 points par point de PIB de G.

### 6.5 Avis général

**Favorable à l'option C**, avec le socle commun du § 3.N.
- Formes fermées sans vitesse.
- Rayon inférieur à 1 dans les deux régimes à 0, 2 et 10 %.
- Arrivée tenue et #56 tenue, sous T9.
- Tout est reproduit indépendamment, sauf la paire complexe.

**Réserves**, sans désaccord sur l'option :
1. Paire complexe et pays joué à 10 % à republier par régime (C48).
2. La stabilité et l'ampleur de long terme dépendent d'une reprise quasi intégrale des intérêts réels et de l'assiette de T_H. C'est l'objet de M33, que je porte à la fiche 9.
3. Le critère 13 échoue pour une raison qui relève de la fiche 9 et des fiches 5 et 6 (§ 6.3).

### 6.6 Conditions transmises

- **C45 (fiche 9)** : toute reprise du surcroît d'intérêts porte sur le taux réel. Le taux de référence de T9 suit π\* par Fisher.
- **C46 (fiche 9)** : pour chaque règle candidate, publier :
  - le gain statique et Δr̄ après G +1 % permanent ;
  - l'inflation excédentaire cumulée Δr̄/k_I (identité exacte sous C2) ;
  - le palier du critère 10 (b) (ii) et le critère 13.
- **C47 (fiche 9, `jeu`, M33)** : stabilité du pays joué seulement pour φ ≥ 0,9 environ (2 %) et φ > 0,9 (10 %). Valeur par défaut du levier budgétaire avec reprise ; « leviers tenus » est un écart déclaré.
- **C48 (fiche 8, `monnaie`)** : chaque régime de T4 est linéarisé séparément, jamais par différences au coude. Republier :
  - la paire complexe : 0,8651, période 18,84 en hausse ; 0,9130, période 20,84 en baisse ;
  - le rayon en pays joué à 10 % : 1,019719 en hausse ; 1,019685 en baisse ;
  - et vérifier les grandeurs du critère 12.
- **C49 (fiche 9, critère 4 (b))** : unicité de r̄ stationnaire sous l'assiette élargie (deux racines à π\* = 0).
- **C50 (fiche 9, critère 14 (c))** : θ_H publié sous ses deux définitions. La part d'une vente imprévue vaut 0,498 sous F2 ; θ_H au sens de la l. 1543 est à mesurer.

### 6.7 Points signalés à `jeu` (non tranchés)

- Le cycle perceptible est de 18,8 tours (hausse) et 20,8 tours (baisse), avec des demi-vies de 4,8 et 7,6 tours. La lecture « environ 19 tours » tient.
- Après une dépense publique permanente, la traîne d'inflation est de 36,7 point-années sous l'assiette WB, contre 3,9 sous l'assiette élargie : c'est l'assiette qui la décide.
- En pays joué sans reprise, une hausse de taux est inflationniste à moyen terme et explosive à 10 %.

## 7. Avis de `jeu`

*`jeu`, 04/10/2026 (issue #72, jalon 2), sur la fiche à l'état `f07d02f` (branche `claude/j1-monnaie-etat`, PR #77). Réponses aux sept questions de `monnaie` (§ 5, l. 684-691).*

**Chiffres.** Aucun moteur n'existe encore. J'ai rejoué la maquette conjointe de `monnaie` (§ 3.0), importée sans modification, avec mes propres scénarios vus du joueur (cinq scripts hors dépôt, 04/10/2026). Mes remesures retrouvent les valeurs du § 3.C-4 :
- i +0,76 point au tour 120 après une dépense publique +1 % permanente ;
- glissement +0,155 point au tour 120 sous taux tenu −1 point ;
- rayon 0,999413.

Les chiffres nouveaux de cet avis viennent des mêmes scripts. Ce sont des résultats de maquette, sous le bloc 9 provisoire (T9 nominal, T_H sur WB, sauf mention), et non des faits. Le cran d'affichage est de 0,1 point. La fenêtre de partie va de 60 à 120 tours (`docs/exigences.md`, O5 : scénarios de 5 à 10 ans).

**Question ludique de la fiche.** Le bloc porte le premier levier macroéconomique du joueur, le taux directeur, et la boussole qui l'accompagne, la règle. Quatre questions en découlent :
- l'écart à la règle a-t-il un effet perceptible, au bon tour et avec le bon signe ?
- la règle est-elle un conseil fiable, ou garde-t-elle une mémoire que le joueur ne voit pas ?
- les anticipations ont-elles un indicateur qui annonce le coût d'une désinflation ?
- existe-t-il un piège, une remise à zéro gratuite ou un signe inversé sans explication ?

### 7.A, 7.B, 7.T, 7.D et 7.R (brièvement)

- **A : à revoir.**
  - La crédibilité ne monte que dans une bande d'un point : effet de falaise (§ 3.A-8, l. 427).
  - Six écrêtages font autant de murs invisibles.
  - Le catalogue de leviers (QE, avances, réserves obligatoires) est sans effet au socle.
- **B : à revoir.**
  - Une crédibilité nulle pour toujours est un indicateur mort (§ 3.B-8, l. 463).
  - Avec un biais de deux points, le joueur verrait la banque centrale manquer sa cible en suivant sa règle.
  - B est instable sur G.
- **T : à revoir.** Deux points d'inflation de biais permanent par point d'erreur sur r\* (§ 3.V, l. 585) : la règle suivie manque la cible pour toujours.
- **D : sans objet au socle.** Le corridor est inerte (Res = 0). À reprendre au J6 avec le levier d'achats.
- **R : hors classement.** C'est une référence.
- **Formation de π^e en phase 9 : sans enjeu ludique.** Le rayon est identique ; un délai d'un tour au lieu de deux ne se voit pas.

### 7.C Option C — action intégrale sans fuite, anticipation à gain constant

- **Récit en une phrase** : « la banque centrale fixe le taux à son taux neutre plus la cible, corrigés de la moitié de l'écart d'inflation, et relève son taux neutre tant que l'inflation dépasse la cible ; les anticipations rattrapent l'inflation observée d'environ un cinquième par an ». Il n'y a ni seuil, ni borne, ni crédibilité cachée.
- **Ce que voit le joueur** (taux décidé un point au-dessus de la prescription aux tours 1 à 12, π\* = 2 %) :
  - glissement : −0,013 point au tour 3, −0,36 au tour 12, minimum −0,39 au tour 14, puis rebond à +0,25 au tour 24. Les écarts restent sous un cran dès le tour 31 ;
  - production : −0,11 % au tour 3, −0,25 % au tour 6, rebond à +0,17 % au tour 18, sous un cran dès le tour 21 ;
  - consommation : +0,30 % au tour 12 (canal rentier, #56) ;
  - la prescription baisse de 3,02 à 2,81 % pendant l'écart et désigne le taux de retour ; r̂\* bouge de −0,075 point au plus, sous un cran ;
  - critère 19 (e) tenu : (i) deux crans dans les 12 tours, sur le glissement et la production ; (ii) pic au tour 14 ; (iii) résidu au tour 60 de +0,005 point de glissement et de +0,005 % de production.
- **Gagnants et perdants** : ceux de la fiche 7 (§ 7.C). Une hausse de taux enrichit les épargnants et alourdit la charge d'intérêts de l'État.
- **Aucune remise à zéro gratuite.**
  - Le joueur tient le taux un point bas pendant 120 tours : glissement +0,41 au tour 12, +0,155 au tour 120, consommation −0,52 %.
  - Pendant ce temps, la prescription monte jusqu'à 3,56 %, soit 1,54 point au-dessus du taux tenu. Revenir à la règle coûte une récession annoncée : production −0,29 % et glissement −0,44 au tour 136. La prescription en a affiché le prix à chaque tour.
- **Stratégies.**
  - « Suivre la règle » est viable.
  - « S'écarter puis revenir » se paie au retour, au prix affiché.
  - « Tenir le taux bas » produit de l'inflation sans relance : la production revient à +0,005 % au tour 120.
  - Aucune stratégie dominante n'apparaît dans les scénarios joués.
- **Risques.**
  - *Cible manquée en suivant la règle* : après une dépense publique +1 % permanente, glissement +0,24 point aux tours 60 à 240, +0,16 au tour 600 (réponse 2).
  - *Mémoire de la règle* : r̂\* garde la trace des écarts passés pendant des siècles (réponse 7).
  - *Signe inversé en pays joué* (réponse 5).
  - *Cible abaissée qui relève l'inflation* (réponse 6).
- **Verdict : lisible**, sous les conditions 1 à 10.

### 7.V Variantes de crédibilité

- **C-h : sans intérêt ludique.** Le c̄ ajouté est invisible du joueur ; palier semblable (+0,143 au tour 120).
- **C-c : à revoir au socle.**
  - C'est une jauge de 0 à 1, attrayante pour le joueur, mais inerte au premier ordre (l. 575).
  - Aucune source ne la calibre (l. 578) ; elle redouble π^e − π\* sans conséquence propre identifiable.
  - Une jauge sans mécanisme nommable est décorative.
- **C-g : à garder pour le J6.**
  - Le gain qui croît avec l'erreur de prévision fait du laisser-aller inflationniste un coût non linéaire : π^e +1,23 point et production −1,76 % sous G +5 % (l. 581).
  - C'est un mécanisme de crise, « désancrage », adossé à une source (Gáti, 2022). Son signal précurseur naturel est π^e − π\*.
  - Au socle, il ferait apparaître des ruptures avant que le joueur ait appris l'indicateur.

### Réponses aux sept questions de `monnaie`

1. **Cycle d'environ 19 tours et traîne séculaire.**
   - **Cycle : lisible.** Le joueur voit un dépassement puis un rebond, et rien de plus.
     - Sous une dépense publique +1 % aux tours 1 à 12 : glissement +0,50 au tour 12, −0,26 aux tours 24 à 27, sous un cran dès le tour 32 ; production +0,27 % au tour 6, −0,25 % au tour 18.
     - Un seul changement de signe au-dessus d'un cran en 120 tours, dans le scénario d'écart à la prescription.
   - **Traîne : à clarifier.**
     - Après un choc transitoire, elle reste sous un cran : i +0,06 point aux tours 60 à 120 (l. 563).
     - Après un choc permanent, elle devient un écart visible et durable (réponse 2).
2. **Rampe du taux après une dépense publique permanente.**
   - **Dans la fenêtre de partie : à clarifier.**
     - i +0,76 point et r̂\* +0,63 point au tour 120.
     - Si r̂\* est restitué, le récit est explicable : « l'État dépense durablement plus, le taux neutre monte ».
   - **À revoir pour ce qui l'accompagne.**
     - Le glissement reste à +0,24 point (deux crans) pendant toute la partie et au-delà : +0,16 au tour 600 (l. 523).
     - Le joueur qui suit la règle voit la banque centrale manquer sa cible pendant des décennies, et seul un écart à la règle y remédie.
     - Sous l'assiette élargie avec T9 réel, l'écart est de +0,165 au tour 120 et de +0,086 au tour 240.
     - Un Δr̄ de +9 points à l'horizon long serait absurde au simulateur du J4.
   - **Ma préférence ludique** va à l'assiette élargie (question 1 de `monnaie` à `macro`) ; c'est un choix de la fiche 9.
   - **k_I à calibrer au J3.** Avec k_I = 1 par an, l'écart tombe à +0,10 au tour 120 et le rebond du cycle passe de +0,27 à +0,35. Je n'ai mesuré que la calibration et la branche λ_w ×2 dans les deux régimes (rayon de 0,999269 à 1), non la grille G complète.
3. **Indicateur d'ancrage π^e − π\* ou crédibilité C-c : π^e − π\*, lisible.**
   - Il ignore les écarts courts : au plus 0,055 point sous un écart de 12 tours à la prescription.
   - Il réagit aux écarts persistants : +0,21 point au tour 120 après une dépense permanente.
   - Il signale ainsi le coût d'une désinflation future, avec un ratio de sacrifice de 2,1 point-années (l. 541).
   - Nom proposé : « écart d'ancrage des anticipations ».
   - C-c est à écarter au socle (§ 7.V).
4. **Taux directeur négatif sans plancher : lisible, avec mention ; accord pour la lecture (b).**
   - À π\* = 2 %, il faut une dépense publique −10 % pendant 12 tours pour descendre à −0,10 %, pendant 3 tours.
   - À π\* = 0 %, une dépense −5 % suffit : minimum −0,52 %, 8 tours.
   - Un plancher serait une borne sans mécanisme nommable.
   - Mention : « taux directeur négatif : au socle, aucun billet ne permet d'y échapper ». C'est la même règle que pour i_D à la fiche 7 (§ 7, réponse 3).
5. **Pays joué, hausse de taux expansionniste : à revoir. L'afficher ne suffit pas.**
   - À 2 %, un taux décidé un point au-dessus de la prescription pendant 12 tours relève le glissement (+0,05 au tour 12, +0,145 au tour 24) et la consommation (+0,49 %).
   - À 10 %, la même hausse donne +1,45 point d'inflation au tour 120 et +37 points au tour 240. Le taux directeur atteint 53 %.
   - C'est un piège irréversible, déclenché par le geste même qui combat l'inflation, sans signal précurseur.
   - Ma préférence ludique est que la **valeur par défaut du levier budgétaire soit une règle avec reprise des intérêts**, symétrique de « suivre la règle » pour le taux (critère 19 (c)).
   - Les leviers tenus sans reprise seraient alors un écart déclaré, avec :
     - la mention « charge d'intérêts financée par le déficit » ;
     - un précurseur : l'écart de r̂\* à sa valeur initiale, et la charge d'intérêts croissante au PIB.
   - Décision de la fiche 9 (M33).
6. **#54 « non rentable » partout : nécessaire, non suffisant pour ouvrir le levier de cible au J4.**
   - Le verdict exclut un stimulant gratuit, non un levier illisible.
   - Marche de la cible de 2 à 1 % (mesure indicative) :
     - le taux directeur **baisse** de 0,51 point au tour 2 (terme de Fisher sur π\*, demi-écart a_π = 0,5) ;
     - le glissement **monte** à 2,52 % au tour 12 (2,13 % sous T9 réel) ;
     - au tour 120, il est encore à 1,62 / 1,31 / 1,21 % selon le réglage budgétaire ;
     - π^e dépasse la nouvelle cible de 0,46 à 0,78 point au tour 120 ;
     - en pays joué, le glissement atteint 6,41 % au tour 240.
   - Le levier a donc un signe inversé à l'impact et n'atteint pas sa cible dans la fenêtre de partie.
   - Ma préférence ludique : **π\* reste un paramètre au J4**. Je corrige l'avis concordant de la l. 136, qui conditionnait le levier au seul verdict de #54.
   - L'ouverture serait conditionnée à deux critères écrits avant l'essai :
     - (a) le glissement s'écarte de l'ancienne cible dans le sens de la nouvelle au plus tard au tour 24, sans la dépasser de plus d'un cran dans l'autre sens ;
     - (b) au moins la moitié du changement est atteinte au tour 120.
   - Pourquoi la règle baisse le taux quand la cible baisse (a_π < 1), et si une autre forme du terme de Fisher l'éviterait : question de fond pour `monnaie`, non tranchée ici.
7. **Restituer la prescription et r̂\*.**
   - **Prescription et écart du taux décidé : lisible.** C'est la boussole du joueur et l'annonce du prix d'un retour à la règle.
   - **r̂\*, « taux neutre estimé » : à clarifier.** Après 120 tours de taux tenu bas, un joueur qui revient à l'ancien taux plutôt qu'à la règle voit :
     - le glissement revenir à la cible (−0,01 point) ;
     - r̂\* rester à 1,35 % au tour 360, contre r̄ = 1 % ;
     - la prescription rester 0,35 à 0,39 point au-dessus du taux qui tient la cible.
   - Le mot « estimé » promet une estimation qui se corrige ; r̂\* est la mémoire des écarts passés.
   - Libellé proposé : « **taux neutre retenu par la règle** », avec l'infobulle « monte tant que l'inflation dépasse la cible, baisse tant qu'elle est en dessous ; garde la mémoire des écarts passés ».

### Indicateurs (critère 19 (a))

| Indicateur | Niveau | Verdict | Motif ou point à clarifier |
|---|---|---|---|
| Glissement et cible | tableau du tour | **lisible** | % par an, une décimale |
| i_CB et taux réel r = i − π | tableau du tour | **lisible** | — |
| Taux indiqué par la règle, écart du taux décidé | tableau du tour | **lisible** | Annonce le prix d'un retour à la règle |
| r̂\* | tableau du tour | **à clarifier** | Libellé « taux neutre retenu par la règle » et infobulle de mémoire (réponse 7) ; porte les chocs permanents |
| π^e et π^e − π\* | tableau du tour | **lisible** | « Écart d'ancrage des anticipations » ; ne bouge qu'aux écarts persistants |
| Crédibilité | — | **sans objet** | Aucune au socle (C-g au J6) |
| H au PIB | fiche détaillée | **hors du tableau** | H = Res = 0 au socle (N-3, l. 474) : indicateur mort |
| Π^CB et E^CB | fiche détaillée | **à clarifier** | E^CB = 0 constant, mention « constant par construction au socle » ; Π^CB = i_CB·M^G/n_a, négatif si le taux l'est |
| Ratio de sacrifice | documentation, scénario O2 | **lisible** | 2,1 point-années par point, non au tableau |
| Retour du niveau des prix (C11) | documentation | **lisible** | −0,106 % au tour 60, sous deux crans d'un niveau ; non affiché |

### Préférence motivée

- **Ma préférence va à C**, comme celle de `monnaie`.
  - **Mes motifs propres** :
    - une règle en une phrase ;
    - une prescription qui affiche le prix d'un écart ;
    - aucune remise à zéro gratuite ;
    - aucun plancher ni seuil invisible ;
    - un cycle lisible en un rebond ;
    - un indicateur d'ancrage qui ne bouge que lorsqu'il le faut.
  - **Les motifs de `monnaie`**, que je ne juge pas : critères 1 à 18 et 20 à 24.
- **Faiblesses ludiques** : trois sont à traiter hors du bloc 8, une est déclarable.
  - La cible est manquée en suivant la règle après un choc budgétaire permanent : fiche 9, assiette (réponse 2).
  - La hausse de taux est inversée et explosive en pays joué : fiche 9, défaut du levier budgétaire (réponse 5).
  - La cible abaissée relève l'inflation : π\* reste un paramètre (réponse 6).
  - Déclarable : la mémoire de r̂\* (réponse 7).
- **Classement** : C > C-g (J6) > C-h ≈ phase 9 > C-c > T > A > B. D sans objet ; R hors classement.
- **Lectures du § 5.**
  - (a) a_π = 0,5 : accord. Le principe de Taylor est sans enjeu ludique visible ; l'instabilité sur G en a un.
  - (b) aucun plancher : accord.
  - (c) aucune crédibilité au socle : accord. C-g au J6, non au J4.
  - (d) phase 1 : accord.
  - (e) sans enjeu ludique.
- **Coût en fidélité** : aucun écart à la littérature demandé. Libellés, mentions, niveau d'affichage et maintien de π\* comme paramètre sont des choix de restitution. Le défaut du levier budgétaire relève de la fiche 9.

### Conditions demandées au § 9

1. **Prescription et écart du taux décidé à la prescription** au tableau du tour. « Suivre la règle » est une valeur du levier ; après un écart, la prescription annonce le saut du retour.
2. **r̂\* au tableau du tour**, libellé « taux neutre retenu par la règle », avec son infobulle de mémoire et son écart à la valeur initiale.
3. **π^e et « écart d'ancrage des anticipations » π^e − π\*** au tableau du tour.
4. **Mention du taux directeur négatif** quand i_CB < 0 (réponse 4).
5. **Pays joué** (fiche 9, M33) :
   - valeur par défaut du levier budgétaire avec reprise des intérêts ;
   - à défaut, la mention « charge d'intérêts financée par le déficit » et un précurseur affiché ;
   - le signe inversé d'une hausse de taux, déclaré dans l'aide.
6. **π\* reste un paramètre au J4.** L'ouverture du levier est soumise aux critères (a) et (b) de la réponse 6, écrits avant l'essai, en plus du verdict de #54.
7. **Tableau levier → indicateur → délai → contrepartie** (critère 19 (c)) :

   | Levier | Indicateur | Délai | Contrepartie |
   |---|---|---|---|
   | Taux directeur (écart à la prescription) | prescription ; i_L, i_D annoncés ; glissement ; production | lignes 12 et 13 au tour n ; i_L, i_D au tour n + 1 ; production au tour 3 ; glissement au tour 3, deux crans avant le tour 12 | charge d'intérêts de l'État, revenu des ménages et Π^CB au tour n ; r̂\* au tour n + 1 |
   | Suivre la règle | taux indiqué par la règle | tour n | saut annoncé par l'écart affiché |

8. **Signes contre-intuitifs déclarés dans l'aide** :
   - taux tenu bas : la consommation baisse (canal rentier, −0,52 % au tour 120) ;
   - cible abaissée : le taux baisse et l'inflation monte à l'impact (mesure indicative) ;
   - retour du niveau des prix (C11) ;
   - absence de l'« énigme des prix ».
9. **Bilan de la banque centrale dans la fiche détaillée** : H, Res et E^CB portent la mention « constant par construction au socle » ; Π^CB est restitué.
10. **Choc budgétaire permanent** : le scénario O2 du J4 publie l'écart de glissement aux tours 60 et 120 et le chemin de r̂\*. Au-delà d'un cran au tour 60, le cas est signalé (critère 19 (e) (iii)).

### Seuils (critère 19 (d) et (e))

- (e) (i) tenu : −0,36 point de glissement au tour 12 ; production −0,25 % au tour 6.
- (e) (ii) tenu : pic au tour 14.
- (e) (iii) déclaré : demi-vie de 1 181 tours ; résidu au tour 60 sous un cran pour un choc transitoire. Pour un choc budgétaire permanent, +0,24 point au tour 60 : au-delà d'un cran, signalé (réponse 2).
- (d) aucun seuil nouveau. Les critères (a) et (b) de la réponse 6 sont proposés pour l'ouverture du levier de cible.

**Issue proposée par `jeu`** (création soumise au mainteneur ; corps dans le compte rendu de la session, PR #77) : « J4 — restitution du bloc banque centrale : prescription et écart, taux neutre retenu par la règle, écart d'ancrage, taux négatif, bilan constant hors du tableau ». Commentaires proposés sur #54 (critères d'ouverture du levier de cible) et sur #73 (défaut du levier budgétaire en pays joué).

## 8. Décision du mainteneur

- **Numéro** : M32 (reporté dans `docs/feuille-de-route.md`, § 4), prise par paire avec M33 (fiche 9, P14).
- **Date** : 04/10/2026.
- **Option retenue** : **C**, avec le socle commun du § 3.N :
  - règle de taux à action intégrale sans fuite, sous la forme de Fisher sur π\*, lisant le glissement : a_π = 0,5, k_I = 0,25 par an (valeurs indicatives, calibrées au J3) ;
  - anticipation adaptative (apprentissage à gain constant de la moyenne), λ_e = 0,2 par an, formée en phase 1 ;
  - aucune crédibilité au socle (C-g gardée pour le J4 ou le J6) ; indicateur d'ancrage π^e − π\* restitué ;
  - aucun plancher de i_CB au socle ; corridor de largeur nulle (i_res = i_CB) ; E^CB_0 = 0 (forme (ii)) ;
  - fermeture monétaire du niveau d'activité (#44), état initial en lecture (1) ;
  - π\* paramètre au socle et au J4 : le levier de cible ne s'ouvre qu'après le verdict de #54 **et** les deux critères de `jeu` (§ 7, réponse 6), écrits avant l'essai.
- **Lectures du § 5**, toutes selon l'avis commun de `monnaie`, `macro` et `jeu` : (a) a_π = 0,5 ; (b) aucun plancher ; (c) aucune crédibilité au socle ; (d) formation de π^e en phase 1 ; (e) lecture (1) de #44.
- **Critère 13 (C15)** : échec déclaré comme **défaut connu du socle** (voie (c) de `monnaie`, avis favorable de `macro`) ; critère gardé tel qu'écrit ; dépendance attribuée à trois conventions hors des blocs 8 et 9 (C30, conversion linéaire, écarts nominaux ; résidu 0,019 point une fois les trois neutralisées) ; codé en échec attendu au J3 ; issue de suivi. Aucune réouverture sur cette branche.
- **Motifs** : le mainteneur a retenu la recommandation de `monnaie`, à laquelle `macro` (§ 6, contre-épreuve indépendante) et `jeu` (§ 7) se rangent. Motifs dans ses propres mots : à compléter par le mainteneur s'il le souhaite.
- **Conditions et réserves** : réserves du § 5 ; C45 à C50 (`macro`, § 6.6) ; C48 levée ; conditions 1 à 10 de `jeu` (§ 7).
- **Ce qui est écarté et pourquoi** : A et B (critères 5, 6 (a), 8, 9 ; B instable sur G) ; T (biais de 2 points par point d'erreur sur r\*) ; C-c (jauge sans mécanisme) ; D (inerte au socle, J6) ; a_π = 1,5 (instable sur G) ; formation de π^e en phase 9 (retouche de `tab:phases` sans gain).
- **Points tranchés avec M33** (fiche 9, § 8) : A8, i_B ≡ i_CB, M^G\* et contrôle de caisse, couverture des intérêts.

## 9. Conséquences de la décision

*Rédigé par `monnaie` (expert pilote) le 04/10/2026, d'après M32 (§ 8) et les points tranchés avec M33 (`finances_publiques.md` § 8). Rédaction faite sur la fiche à l'état `9cc1ead` (branche `claude/j1-monnaie-etat`, PR #77).*

*Numéros de ligne.* Ils renvoient à `docs/specification/nations_et_marches.tex` à l'état `9cc1ead`. Ils diffèrent de ceux des § 1 à § 7, lus à `10391a1` : `git diff --stat 10391a1 9cc1ead` donne 401 insertions, 27 suppressions. Correspondances vérifiées sur le contenu :

| `10391a1` | `9cc1ead` | Contenu |
|---|---|---|
| l. 214 | l. 215 | r = i − π |
| l. 493 | l. 494 | Π^CB |
| l. 502 | l. 503 | M^G\* |
| l. 529 | l. 530 | phase 1 |
| l. 535 | l. 536 | phase 7 |
| l. 2064 | l. 2411 | paramètres du cadre |

*Conventions.*
- *Identifiants.* « BC1 » à « BC9 » désignent les équations du bloc 8 retenues par M32. Ils remplacent les identifiants (C1) à (C4) du § 3.C-2, qui entreraient en collision avec les conditions C1 à C63 (`grep -c '\bC2\b'` sur la spécification : 8). `grep -rnoI '\bBC[0-9]\+\b' docs/ CONTEXT.md` ne trouve aucune occurrence.
- *Conversions* (ADR 0008, I.1 ; l. 190-202) :
  - i_CB, i_res et i_B sont des taux de flux annuels, convertis linéairement (x/n_a) ;
  - k_I et λ_e sont des vitesses ou gains annuels, convertis linéairement (k_I/n_a, λ_e/n_a) ;
  - π\*, π^e et π̄ sont des taux d'inflation, convertis géométriquement ;
  - le glissement π_{t−1} est mesuré, jamais converti ;
  - r̂\* et r̄ sont des taux réels annuels de Fisher sur π\* (N-6). Ils n'entrent que dans le produit annuel de BC1 et ne sont jamais convertis par pas.
- *Statut des chiffres.* Ce sont des résultats de maquette, non des faits. Chaque chiffre porte la section de la fiche qui le publie. Les chiffres marqués « remesuré » ont été recalculés le 04/10/2026 par `uv run --no-project python` (calcul à la main en forme fermée, sorties au compte rendu de la session).
- *Portée.* Le § 9 ne décide rien. Il traduit :
  - M32 ;
  - les points tranchés avec M33 ;
  - les réserves du § 5 ;
  - C45 à C50 (§ 6.6) ;
  - les conditions 1 à 10 de `jeu` (§ 7) ;
  - les conditions C59 à C62 de la fiche 9 (§ 6.6) qui touchent le bloc 8.

  Tout point qui exigerait une décision nouvelle est signalé comme question. Ce qui relève de l'ADR d'architecture d'A8 est cité comme « ADR 0011 (proposé) ».

### 9.1 Équations retenues et labels

**Au jalon J1, aucun label.** C'est la convention de #42, suivie par `sec:investissement` et `sec:banque`. La spécification compte 0 `\label{eq:` à `9cc1ead`, et `concordance_spec_moteur.py --strict` affiche « Aucun écart ».

`sec:banque_centrale` est écrite en encadrés `proposee` citant M32, en `equation*` (`CONVENTIONS.md` § 4.1). Chaque mécanisme y est repéré par son identifiant et son label prévu en `\texttt{}`, sur le modèle du tableau `tab:banque-equations` (l. 2024-2043).

**Labels à créer au J3**, avec `src/nations/blocs/banque_centrale.py` (radical `banque_centrale`, `CONVENTIONS.md` § 2.1, l. 60). `coder` pose une balise par label ; `docwriter` retire l'encadré et pose le label dans le même passage.

| Label | Id. | Ce que l'équation détermine | Équation | Phase | Statut | Provenance | Couche |
|---|---|---|---|---|---|---|---|
| `eq:banque_centrale-regle-taux` | BC1 | taux indiqué par la règle (prescription), et taux directeur du tour | 1 + i^règle_t = (1 + r̂\*_t)(1 + π\*_t) + a_π(π_{t−1} − π\*_t). Sous la valeur « suivre la règle » du levier, i_{CB,t} = i^règle_t ; sinon i_{CB,t} est la valeur décidée (levier ouvert au J4) | 1 | choix de conception | § 3.C-2 (C1) ; forme de Fisher sur π\* (N-6, #49) ; mesure lue : glissement π_{t−1} (#24, lecture (ii)) ; aucun terme d'activité ; aucun plancher (lecture (b)) ; forme proportionnelle : Taylor (1993), p. 202 ; M32 | `blocs/` |
| `eq:banque_centrale-taux-neutre` | BC2 | taux neutre retenu par la règle, au pas suivant (variable d'état) | r̂\*_{t+1} = r̂\*_t + (k_I/n_a)(π_{t−1} − π\*_t) | 1 | choix de conception | § 3.C-2 (C2) ; action intégrale sans fuite (C2 de la fiche 3) ; « terme intégral » de la v1.5 (l. 1030), sans clip ni logarithme. Même loi que la règle soit suivie ou non, jamais réinitialisée (critère 19 (c)) ; M32 | `blocs/` |
| `eq:banque_centrale-anticipation` | BC3 | anticipation d'inflation du pas suivant (variable d'état lue à l'ouverture par le bloc 3) | π^e_{t+1} = π^e_t + (λ_e/n_a)(π_{t−1} − π^e_t) | 1 | choix de conception | § 3.C-2 (C3) ; apprentissage à gain constant de la moyenne (Evans, notes de cours, lues par extraits seulement : **à relire à la source avant toute citation**, § 3.0) ; gain : Gáti (2022), p. 19-20 (lu) ; formation en phase 1, lecture (d) ; aucune crédibilité, lecture (c) ; M32 | `blocs/` |
| `eq:banque_centrale-cible` | BC4 | cible en vigueur du pas suivant (variable d'état) | π\*_{t+1} = π\*_t | 1 | choix de conception | ADR 0010, point 3 ; N-1 ; π\* reste un paramètre au socle et au J4 (M32). Le levier de cible reste fermé jusqu'au verdict de #54 et aux critères (a) et (b) de `jeu` (§ 7, réponse 6) | `blocs/` |
| `eq:banque_centrale-part-souscription` | BC5 | part de la banque centrale dans la souscription primaire, lue par le bloc 9 en phase 7 | s_{CB,t} = s_CB (paramètre d'archétype) | 1 | choix de conception | A8 (M33 ; ADR 0011, proposé) ; N-4 ; neutre sous i_B = i_res = i_CB (C59) ; levier au J6 | `blocs/` |
| `eq:banque_centrale-resultat` | BC6 | résultat de la banque centrale du pas | Π^CB_t = [i_{B,t}B_{CB,t} + i_{CB,t}L^CB_t − i_{res,t}Res_t]/n_a, sur les encours d'ouverture. Au socle (i_B ≡ i_res ≡ i_CB) : Π^CB_t = i_{CB,t}(E^CB_t + M^G_t)/n_a = i_{CB,t}M^G_t/n_a sous E^CB = 0 | 1 | dérivée (cadre, l. 494) | M22, lecture (d) ; ADR 0005, point 12 ; encours d'ouverture et taux de la phase 1 (l. 496) ; identité de N-3 ; M32 et M33 | `blocs/` |
| `eq:banque_centrale-interets-reserves` | BC7 | ligne 12 | i_{res,t}Res_t/n_a, soit i_{CB,t}Res_t/n_a au socle | 8 (a) | dérivée (ligne 12, l. 355) | M22 ; corridor de largeur nulle (N-2 ; M31, lecture (g)) ; ligne nulle au socle tant que Res = 0 | `blocs/` |
| `eq:banque_centrale-interets-refinancement` | BC8 | ligne 13 | i_{CB,t}L^CB_t/n_a | 8 (a) | dérivée (ligne 13, l. 356) | M22, lecture (c) : délai nul (l. 484) | `blocs/` |
| `eq:banque_centrale-versement-resultat` | BC9 | ligne 16 | ligne 16 = Π^CB_t, versée sans troncature. Une perte est un versement négatif, payé par le compte du Trésor | 8 (b) | dérivée (l. 492-496) | M22, lecture (d). La part non couverte d'une perte est la ligne nommée « perte de la banque centrale non couverte » du bloc 9 (C60, M33) | `blocs/` |

**Ordre interne de la phase 1** (critère 4 (d)) :
- BC1 précède BC6, puisque Π^CB lit i_{CB,t} ;
- BC2, BC3, BC4 et BC5 ne lisent que l'ouverture et sont sans ordre entre eux ;
- le bloc lit le levier de taux que le moteur lit en phase 1 : « moteur (leviers) » le précède (§ 9.4).

**Ce qui n'a pas de label** :
- **i_res ≡ i_CB.** Corridor de largeur nulle (M32 ; N-2). C'est une identité de notation du socle, déclarée une seule fois dans `sec:banque_centrale`, sans label ni équation exécutée, sur le modèle de i_B ≡ i_CB (M33). Tout lecteur lit i_CB, et la ligne 12 garde sa notation (l. 355). La forme (identité ou variable écrite en phase 1) est un point de forme pour `architect` (question 2).
- **i_B ≡ i_CB.** Déclarée dans `sec:finances_publiques` (M33), non répétée ici.
- **E^CB.** Calculée deux fois par le noyau : par le stock (l. 256), et par les flux, E^CB_{t+1} = E^CB_t + Π^CB_t − ligne 16 exécutée. Seul le montant exécuté de la ligne 16, lu au grand livre, entre dans le calcul par les flux. La part non couverte d'une perte (C60) réduit donc E^CB sans ligne de monnaie.
- **Res et L^CB.** Positions tenues au grand livre, mues par les lignes 12, 13, 19a, 19b, 20 et 21. Leurs formes fermées (critère 3 (d) ; § 9.4) sont des dérivations.
- **Ligne 19a-BC.** Proposée par le bloc 9 (A8) : 19a-BC = s_{CB,t} × besoin d'émission.
- **Lignes 19b-ménages et 19b-banque.** Aucune n'est proposée au socle (N-4, N-7 : achats non ouverts, renvoyés au J6). Ce point est à concilier avec la fiche 7 (question 1).
- **Grandeurs de restitution** : taux réel r = i − π (l. 215), écart à la prescription, écart d'ancrage π^e − π\*. Elles relèvent de `observation/` (§ 9.5).
- **Contrôle mécanique.** Les neuf labels vérifient l'expression régulière de `CONVENTIONS.md` § 2.1 (l. 62). Contrôle par `uv run --no-project python` dans un répertoire temporaire : neuf « True ».

### 9.2 Paramètres

À porter dans `tab:calibration` au J1, sans `\code{}` avant le code. Les noms sont des propositions.

| Symbole | Nom proposé | Valeur | Unité | Source | Équation |
|---|---|---|---|---|---|
| a_π | `coefficient_ecart_inflation` | 0,5 (indicative) | sans dimension : points de taux par point d'écart du glissement | **choix de conception, sans source** (§ 4, critère 23). La forme proportionnelle est celle de Taylor (1993, p. 202), mais la réponse totale à l'inflation vaut ici a_π < 1 : le principe de Taylor n'est pas tenu à court terme (§ 3.C-6). **Calibré au J3** | BC1 |
| k_I | `gain_integral` | 0,25 par an (indicative) | par an, gain, conversion linéaire (k_I/n_a = 0,020833 par pas, remesuré) | **choix de conception, sans source** (§ 4, critère 23). k_I = 1 est mesuré par `jeu` sur la calibration et la branche λ_w ×2 seulement (§ 7, réponse 2). **Calibré au J3** | BC2 |
| λ_e | `gain_anticipation` | 0,2 par an (indicative) | par an, vitesse, conversion linéaire (λ_e/n_a = 0,016667 par pas, remesuré) | Gáti (2022), p. 19-20 : gain de 0,05 par trimestre, soit 0,2 par an en conversion linéaire (§ 3.0). **Calibré au J3** avec λ_w·β sur un ratio de sacrifice sourcé (C7, #45) | BC3 |
| s_CB | `part_souscription_banque_centrale` | 0 au socle | fraction du besoin d'émission | A8 (M33) ; paramètre d'archétype ; levier au J6 (N-4) | BC5 |
| r̄ | `taux_reel_neutre_initial` | 0,01 (indicative) | par an, taux réel de Fisher sur π\*, (1 + i_{CB,0}) = (1 + r̄)(1 + π\*) | lecture (1) de #44, M32 : r̄ donné, s_G résolu (N-5). Niveau du taux naturel contesté (critère 23). Repris comme r^ref par T9 (fiche 9, § 3.C-2). **Calibré au J3** | état initial (§ 9.4) |

π\* figure déjà dans `tab:calibration` (l. 2453). Seuls changent son propriétaire et sa source (§ 9.8).

**Conditions déclarées, contrôlées au chargement, jamais par écrêtage** :
- **0 < a_π < 1,5** (réserve 3 du § 5). Toutes les calibrations à a_π = 1,5 sont instables sur G en régime de baisse (§ 3.C-4, clause II.7).
- **k_I > 0.** k_I = 0 redonnerait la règle à taux naturel fixe (variante T, écartée) : biais de 2 points par point d'erreur sur r\* (§ 3.V).
- **0 < λ_e ≤ n_a** (l. 215).
- **0 ≤ s_CB ≤ 1** (M33). Au-delà de m·M^G/B, soit 0,0686 × m à 2 %, Res > 0 et L^CB = 0 à la clôture (C59 ; fiche 9 § 6.4, complément, point 2). C'est un changement de position, non une condition.
- **Condition d'existence : aucune**, sans plancher (§ 3.C-3).
- **Domaine de r̄.** La racine parasite de r̄ (r̄ ≤ −7,5 % à π̄ = 0 sous C-HS) est exclue par une condition de domaine déclarée en `\limites` du bloc 9 (C51, « r̄ > −5 % par exemple », fiche 9 § 3.C-6).

**Ce qui n'est pas un paramètre** :
- i_CB et i^règle (phase 1 ; BC1) ; i_res et i_B (identités) ;
- r̂\*_0, π^e_0, i_{CB,0}, E^CB_0 = 0, B_{CB,0}, L^CB_0 et Res_0, valeurs de l'état initial résolu (§ 9.4) ;
- U^eq : **non lu** par le bloc, puisque la règle n'a aucun terme d'activité (M32) ;
- m (bloc 9, M33) ;
- ς_{B,t}, entrée de scénario lue par le bloc 9 sous A8.

**Décompte (critère 20)** :
- 3 paramètres de comportement (a_π, k_I, λ_e), 1 paramètre d'archétype (s_CB) et 1 paramètre d'état initial (r̄).
- 2 variables d'état nouvelles :
  - r̂\*, par an, valeur stationnaire r̄ ;
  - π^e, par an, valeur stationnaire π̄ = π\*.
- 1 variable d'état reprise du moteur : π\*_t (ADR 0010, point 3).
- 0 borne à seuil libre. 4 contraintes de domaine, contrôlées au chargement.
- Lignes proposées : 12, 13 et 16.
- Aucun drapeau, aucun tirage, aucun historique. La règle lit π_{t−1} au registre (ADR 0008, II.6).
- Environ 35 opérations par pas, sans itération (§ 3.C-5).

### 9.3 Conditions et réserves

**Lectures de M32 que la section reprend** (§ 8) :
- (a) a_π = 0,5 ;
- (b) aucun plancher de i_CB ;
- (c) aucune crédibilité au socle (C-g gardée pour le J4 ou le J6) ;
- (d) formation de π^e en phase 1, d'où un délai prix → anticipation → salaire de deux tours. La π^e consommée au tour n est formée en phase 1 du tour n − 1, sur π_{n−2}, et la condition de Barro et Gordon tient (`macro`, § 6.4 (d)) ;
- (e) lecture (1) de #44.

**Points tranchés avec M33, et leur effet sur le bloc 8** :
- **A8.**
  - Le bloc 8 écrit s_{CB,t} en phase 1 (BC5).
  - Il ne propose aucune ligne 19a et ne siège pas en phase 7 au socle (N-7).
  - La lecture (f) de M31 est tranchée. **Modification** de contrat (`temps_comptabilite.md:838`, ADR 0009 l. 84), portée par l'ADR 0011 (proposé).
- **i_B ≡ i_CB.**
  - BC6 se réduit à i_CB(E^CB + M^G)/n_a.
  - s_CB est neutre pour les revenus (C59), avec une prime nulle déclarée (J6).
  - Lignes 11b et 11c au taux du tour, délai 0.
- **E^CB_0 = 0** (forme (ii) du critère 2 (a)). C'est la seule forme dont le ratio est stationnaire sous M22 (d) (N-3).
  - Π^CB ≥ 0 tant que i_CB ≥ 0.
  - Sans plancher, une perte est possible si i_CB < 0. Elle est couverte par l'émission en position α (−Π^CB entre dans le besoin de la phase 7, fiche 9 N-3), sauf si le placement rate le même tour.
  - Dans ce cas, la ligne nommée C60 du bloc 9 réduit E^CB, et E^CB < 0 est déclaré.
  - La recapitalisation relève du J6.
- **Contrôle de caisse en lecture nette.** Sans effet sur le bloc 8. La banque en est exclue (découvert intra-pas, l. 486-490).
- **M^G\* = m × paiements bruts, m > 1.**
  - Sous E^CB = 0 et s_CB = 0, Res = 0 et L^CB = M^G = m·P à la clôture.
  - Passer de m = 1 à 1,1 relève L^CB d'environ 0,0019 année de PIB à 2 % (fiche 9 § 6.4, complément, point 2).
  - L'effet sur les revenus est nul sous i_B = i_CB. C'est une algèbre, **non mesurée** : m n'est pas un paramètre de `m9.py`.
- **Règle budgétaire de référence : C-HS**, avec la couverture intégrale (φ = 1) comme valeur par défaut. C'est la règle sous laquelle les critères 6 (d), 7, 11, 15 et 17 se jugent au J3 et au J4.

**Chiffres de référence de la règle retenue sous C-HS** (`finances_publiques.md` § 3.C-4, mesures de `macro`). Ils remplacent comme référence ceux du § 3.C-4 de cette fiche, obtenus sous T9 nominal et assiette WB, qui restent publiés.

| Grandeur | Sous T9 nominal, assiette WB (§ 3.C-4) | Sous C-HS (fiche 9 § 3.C-4) |
|---|---|---|
| Rayon à 0 / 2 / 10 % (deux régimes) | 0,999270 / 0,999413 / 0,999814 | 0,997497 / 0,997486 / 0,997558 |
| Demi-vie dominante | 1 181 tours | 275 tours (remesuré depuis le rayon : 275,4) |
| Grille G | pire valeur 0,999551 | 31 branches toutes sous 1, pire valeur 0,998883 ; ζ = 8 : 0,996234 |
| Gain statique (% de y par point de i) | −0,0259 | −0,2208 |
| Δr̄ après G +1 % permanent ; Δr̄/k_I | +918 pb ; 36,7 point-années | +96 pb ; 3,8 point-années |
| Glissement − π\* aux tours 60 / 120 / 240 / 600 (G +1 % permanent) | +0,238 / +0,238 / +0,224 / +0,160 (§ 6.1) | +0,214 / +0,161 / +0,085 / −0,006 |
| Taux tenu −1 point, tour 120 | +0,155 (palier 2,0847 %) | +0,396 (nouveau palier, +0,596 au tour 2 400) |
| #56 (A) : cumul des tours 1 à 12 ; P_36 | −0,160 ; −0,138 % | −0,216 ; −0,226 % |
| #56 (B) : P_120 ; glissement | −1,81 % ; −0,151 | −3,72 % ; −0,385 |
| Pays joué (φ = 0) à 2 / 10 % | 1,007482 / 1,019719 | 1,001818 / 1,011036 ; doublement de l'écart en 382 / 63 tours (fiche 9 § 6.4) |

**Non mesurés sous C-HS**, à remesurer au J3 :
- la paire complexe (cycle de 18,8 et 20,8 tours sous T9, § 3.C-4) ;
- le verdict de la clause II.7. Il a été remesuré sous l'assiette du revenu avant impôt retardé avec T9 réel, voisine de C-HS : « non déterminant » (§ 3.C-4) ;
- #54 et l'essai (3) ;
- les scénarios de perceptibilité de `jeu` (§ 7).

**Critère 13 (C15) : défaut connu du socle** (M32, voie (c) ; #80). Sous C-HS, en lecture (α) :
- r̄ vaut 1,536 % à π\* = 0 et 1,075 % à π\* = 10 % : écart de 0,461 point entre les bornes, 0,74 point au maximum sur [0 ; 10 %] ;
- une marche de cible de 2 à 3 % déplace r̄ de −0,12 point (fiche 9 § 6.3, point 4).

Le seuil adopté est de 0,1 point. La dépendance vient de trois conventions hors des blocs 8 et 9 :
- C30 (M28) ;
- la conversion linéaire des taux de flux (M22 ; ADR 0008, I.2) ;
- les écarts nominaux (M31).

Une fois les trois neutralisées, le résidu vaut 0,019 point. Toute réouverture partielle aggrave l'écart (C61). Le critère est codé en **échec attendu** au J3 (§ 9.6). Aucune réouverture sur la branche n° 4.

**Réserves du § 5, et où elles sont tenues** (§ 9.6) :
1. Rayon de la boucle conjointe inférieur à 1 sur G, sous C-HS : test « Stabilité ».
2. Arrivée à 1e−6 en 20 demi-vies : test « Vitesses ».
3. a_π ∈ ]0 ; 1,5[ contrôlé au chargement : § 9.2 et test « Calibration ».
4. Formes fermées de 3.C-3 à 1e−10 : test « État stationnaire ».
5. Persistance du critère 10 (b) (ii) : test « Persistance ».

**Défauts déclarés, coût en fidélité de l'option** (§ 3.C-6, § 5). Ils vont aux `\limites` de BC1 à BC3 et à l'encadré `portee`.
1. **Principe de Taylor non tenu à court terme** (a_π = 0,5 < 1). La stabilisation de long terme vient de l'action intégrale.
2. **Persistance adaptative de l'inflation.**
   - Ratio de sacrifice de 2,08 point-années par point (T9 réel, § 3.C-4), contre 1/(λ_e λ_w β) = 1/(0,2 × 1 × 2) = 2,5 (remesuré).
   - Ratio non cité dans la littérature : Ball (1994) n'a pas été lu.
3. **Aucune crédibilité** au socle.
4. **Racine dominante lente.**
   - Demi-vie de 275 tours sous C-HS. Après un choc permanent, r̂\* traîne : glissement +0,214 au tour 60, au-delà d'un cran, signalé (condition 10).
   - Hors de la boucle conjointe, π^e seule résorbe 18,3 % d'un écart par an, soit une demi-vie de 41,2 tours (remesuré : 1 − (1 − 0,2/12)^12 = 0,1826). Le récit de `jeu`, « environ un cinquième par an », est cohérent.
5. **Mémoire de r̂\*.** Après 120 tours de taux tenu un point bas, r̂\* vaut encore 1,35 % au tour 360, contre r̄ = 1 % (§ 7, réponse 7, sous T9 nominal).
6. **Taux directeur négatif possible**, sans billet pour y échapper.
   - i_D < 0 dès que i_CB < ϖ_D = 1 % (§ 6.4 (b)).
   - Π^CB < 0 si i_CB < 0 (C60).
7. **Une cible abaissée baisse le taux à l'impact.** C'est la question de fond que `jeu` adresse à `monnaie` (§ 7, réponse 6), instruite ici en forme fermée, sans décision.
   - Sous BC1, ∂(1 + i^règle)/∂π\* = (1 + r̂\*) − a_π = 1,01 − 0,5 = 0,51 (remesuré). Cela redonne la baisse de 0,51 point du tour 2 mesurée par `jeu`.
   - Le signe s'inverserait seulement si a_π > 1 + r̂\*, valeurs exclues par la condition a_π < 1,5 dans la mesure où a_π = 1,5 est instable sur G.
   - Toute autre forme du terme de Fisher modifierait M32. Elle est à instruire avec #54, avant l'ouverture du levier de cible.
8. **Pays joué sans reprise (φ = 0) explosif** sous toute règle à action intégrale : une hausse de taux y est inflationniste à moyen terme. C'est un régime déclaré de la fiche 9 (M33), non une référence.
9. **Faible effet de long terme d'un taux tenu sous T9 nominal**, porté au mainteneur au titre du critère 10 (a) (§ 5, point (3)). Sous C-HS, le palier vaut +0,396 au tour 120, au-dessus du cran : l'exigence de persistance est tenue.

**Ce qui reste paramétrable sans rouvrir M32** (visa de l'expert pilote) :
- les valeurs de a_π, k_I, λ_e et r̄, dans les conditions du § 9.2 ;
- s_CB par archétype, dans [0 ; 1].

**Par une décision citant M32** :
- un plancher de i_CB (borne à seuil libre, lecture (b) ; critère 18) ;
- une crédibilité (C-h, C-c) ou le gain endogène C-g (J4 ou J6) ;
- un terme d'activité, a_U ≠ 0 (C6 : sur U^eq lu au bloc 3, sans coefficient d'Okun importé) ;
- un corridor non nul (variante D, J6) ;
- l'ouverture du levier de cible (#54 et critères (a), (b) de `jeu`) ;
- le levier d'achats de titres (J6) ;
- a_π ≥ 1,5 ;
- la formation de π^e en phase 9 (qui cite aussi M22 et M29, avec ADR).

### 9.4 Propriétaires et phases des lignes de `tab:matrice-flux`

**Lignes de la colonne « BC »** (l. 354-369) :

| Ligne | Propriétaire (propose) | Phase | Règle | Moyen de paiement côté banque centrale | Statut |
|---|---|---|---|---|---|
| 11c | bloc 9 | 6 | i_B B_CB/n_a, avec i_B ≡ i_CB | reçue sur le compte du Trésor, sans réserves | M33 |
| 12 | bloc 8 | 8 (a) | BC7 | crée des réserves | M32 |
| 13 | bloc 8 | 8 (a) | BC8 | draine des réserves | M32 |
| 16 | bloc 8 | 8 (b) | BC9 ; part non couverte d'une perte : ligne nommée du bloc 9 (C60), en dernier | compte du Trésor, sans réserves | M32 ; M33 |
| 19a-BC | **bloc 9** (A8) | 7 | s_{CB,t} × besoin (s_{CB,t} écrit par le bloc 8 en phase 1) | crédite le compte du Trésor, sans monnaie centrale (l. 379) | M33 ; ADR 0011 (proposé) |
| 19b-ménages | aucun au socle | — | nulle (B_H ≡ 0) | — | M27 |
| 19b-banque | **aucun au socle** (N-4, N-7) | 7 au J6 | levier d'achats au J6 | crée des réserves | M32 ; à concilier avec la fiche 7 (question 1) |
| 20, 22 | noyau | — | contreparties de règlement (l. 319) | — | inchangé |
| 21 | bloc 7 | 8 (c) | B7 | — | M31 |

Ni ligne ni poste nouveau du fait du bloc 8 : `tab:matrice-flux`, `tab:portes-monnaie` et `tab:matrice-bilans` sont inchangées. Sortie de `uv run python outils/verifier_matrices.py --strict` à `9cc1ead` : « tab:matrice-bilans : 9 lignes, 6 colonnes, 44 termes ; tab:matrice-flux : 28 lignes, 6 colonnes, 62 termes ; tab:portes-monnaie : 28 lignes, 3 colonnes, 31 termes ; Aucun écart. », code 0.

La forme de la ligne nommée C60 (ligne de la matrice sans montant monétaire, ou registre du noyau) relève de la fiche 9 § 9 et du contrat partagé décidé par M33. Pour le bloc 8, il suffit que E^CB par les flux lise la ligne 16 exécutée.

**Phases du bloc 8** :

| Phase | Le bloc 8 lit | Le bloc 8 écrit ou propose | Autres blocs |
|---|---|---|---|
| 0 | — | rien. L'ouverture contient r̂\*_t, π^e_t, π\*_t, le registre, B_{CB,t}, L^CB_t, Res_t et M^G_t | moteur (Γ^e_t sur π\*_t, ADR 0010) |
| 1 | ouverture : π_{t−1} (registre), π\*_t, r̂\*_t, π^e_t, B_{CB,t}, L^CB_t, Res_t ; levier de taux lu par le moteur dans la phase. Jamais W_t, p_t ni U_{t−1} | i^règle_t et i_{CB,t} (BC1), r̂\*_{t+1} (BC2), π^e_{t+1} (BC3), π\*_{t+1} (BC4), s_{CB,t} (BC5), Π^CB_t (BC6) | moteur (leviers) avant le bloc 8 ; bloc 3 : W_t, sur π^e_t d'ouverture, sans lecture mutuelle |
| 2 à 6 | — | rien | blocs 7 et 9 lisent i_{CB,t} en phase 6 (lignes 9 et 10 sur i_L, i_D d'ouverture ; 11a à 11c sur i_B ≡ i_CB) |
| 7 | — | **rien** (A8, N-7) | bloc 9 : lignes 19a, en lisant s_{CB,t} et Π^CB_t de la phase 1 |
| 8 (a) | Res_t, L^CB_t (ouverture) ; i_{CB,t} | lignes 12 (BC7) et 13 (BC8) | — |
| 8 (b) | Π^CB_t | ligne 16 (BC9) | bloc 9 : part non couverte (C60) |
| 8 (c) | — | rien | bloc 7 : ligne 21 (B7), i_{L,t+1}, i_{D,t+1} |
| 9 | — | rien. Le bloc n'entre pas dans le groupe de la phase 9 | noyau : E^CB calculé deux fois, Res_{t+1} ≥ 0 |

**Triangularité** (critère 4 (h)) :
- En phase 1, le bloc ne lit que l'ouverture et le levier.
- Le bloc 3 ne lit rien de ce que le bloc 8 écrit dans la phase : il lit π^e_t à l'ouverture (lecture (a), M25).
- En phase 7, le bloc 9 lit des variables de la phase 1.
- En phase 8 (a) et (b), le bloc lit l'ouverture et la phase 1.
- Aucun ordre nouveau entre blocs. Seul est déclaré l'ordre « moteur (leviers), puis banque centrale », déjà implicite (§ 9.8).

**Phase des variables d'état.** r̂\*_{t+1}, π^e_{t+1} et π\*_{t+1} sont écrites une fois par pas, en phase 1, où le bloc siège après toutes leurs entrées (ADR 0009, point 4). Aucun lecteur ne les lit sous leur indice daté avant le pas suivant.

**État initial résolu** (C3, critère 6 (b) ; lecture (1) de #44) :
- r̂\*_0 = r̄ ; π^e_0 = π\*_0 = π\* ; i_{CB,0} = (1 + r̄)(1 + π\*) − 1, soit 1,00 / 3,02 / 11,10 % à π\* = 0 / 2 / 10 % et r̄ = 1 % (remesuré) ;
- registre stationnaire P_{t−u} = P_t(1 + π\*)^{−u/n_a} (l. 220), d'où π_{−1} = π\* et i^règle_0 = i_{CB,0} exactement ;
- E^CB_0 = 0 ; B_{CB,0} = s_CB·B_0, soit 0 au socle ; L^CB_0 = max(M^G\*_0 + E^CB_0 − B_{CB,0} ; 0) = M^G\*_0 ; Res_0 = max(B_{CB,0} − M^G\*_0 − E^CB_0 ; 0) = 0 (critère 3 (d)) ;
- formes fermées : π̄ = π\* quels que soient r̄, a_π, k_I et λ_e (C2) ; π^e = π̄ (C1) ; r̂\* = r̄. Aucune vitesse n'entre (critère 7 (a)) ;
- Π^CB = i_CB·M^G/n_a ≥ 0.

**Interfaces avec les blocs voisins** :

| Bloc | Le bloc 8 lit | Le bloc 8 rend | Contrat |
|---|---|---|---|
| moteur | leviers (phase 1) ; registre ; π\*_t | π\*_{t+1} (BC4) | ADR 0010 ; M30 |
| 3, travail | rien (U_{t−1} non lu au socle) | π^e_t à l'ouverture | C1, C5, C12 ; M25 |
| 4, prix | rien | rien (aucun canal π^e → p ni canal de coût) | C9 à C13 ; M26 |
| 5 et 6, ménages et investissement | rien | π\*_t (par le moteur, Γ^e) ; i_CB, par le bloc 7 | C14, C32 à C36 ; M27, M28 |
| 7, banque | rien | i_{CB,t} en phase 1 (i_res ≡ i_CB) ; lignes 12 et 13 ; refinancement sans plafond ni collatéral | M31, lecture (g) ; fiche 7 § 9.7 |
| 9, État | rien | i_{CB,t}, lu comme i_B ; Π^CB_t ; s_{CB,t} (phase 1) ; ligne 16 (8 (b)) | A8, C25, C59, C60 ; M33 |

### 9.5 Restitution

Les conditions de `jeu` (§ 7) sont reprises telles quelles. Leur mise en œuvre au J4 relève de l'issue **#81**. La couche `observation/` lit l'état et les montants exécutés, sans effet sur la trajectoire.

1. **Prescription et écart du taux décidé**, au tableau du tour. « Suivre la règle » est une valeur du levier (BC1). Après un écart, la prescription annonce le saut du retour.
   *Mise en œuvre* : i^règle_t est calculé à chaque pas, que la règle soit suivie ou non. L'écart affiché vaut i_{CB,t} − i^règle_t.
2. **r̂\* au tableau du tour**, libellé « taux neutre retenu par la règle », avec :
   - l'infobulle « monte tant que l'inflation dépasse la cible, baisse tant qu'elle est en dessous ; garde la mémoire des écarts passés » ;
   - son écart à la valeur initiale, r̂\*_t − r̄.
3. **π^e et « écart d'ancrage des anticipations », π^e − π\***, au tableau du tour.
4. **Mention du taux directeur négatif** quand i_CB < 0 : « taux directeur négatif : au socle, aucun billet ne permet d'y échapper ».
5. **Pays joué** : décidé par M33.
   - Couverture des intérêts : levier distinct du barème, à deux valeurs. « Couverture intégrale » est la règle et la valeur par défaut. « Intérêts financés par le déficit » est un écart déclaré, avec la mention et deux précurseurs.
   - Le signe inversé d'une hausse de taux sous φ = 0 est déclaré dans l'aide.
   - Restitution à l'issue #82.
6. **π\* reste un paramètre au J4** (M32). L'ouverture du levier est soumise au verdict de #54 et aux critères (a) et (b) de `jeu` (§ 7, réponse 6), écrits avant l'essai.
7. **Tableau levier → indicateur → délai → contrepartie** (critère 19 (c)), repris tel quel du § 7 dans l'encadré `joueur` de `sec:banque_centrale`.
   - Complément sous i_B ≡ i_CB : la charge d'intérêts de l'État (lignes 11a à 11c) et T9 bougent au tour n (fiche 9 § 7, condition 8).
   - Complément C43 (fiche 7) : la consommation bouge dès le tour n + 1, par Div_Bk.
8. **Signes contre-intuitifs déclarés dans l'aide** :
   - taux tenu bas : la consommation baisse (canal rentier) ;
   - cible abaissée : le taux baisse et l'inflation monte à l'impact (§ 9.3, défaut 7) ;
   - retour du niveau des prix (C11) ;
   - absence de l'« énigme des prix ».
9. **Bilan de la banque centrale dans la fiche détaillée** : H, Res et E^CB portent la mention « constant par construction au socle ». Π^CB et L^CB sont restitués.
10. **Choc budgétaire permanent** : le scénario O2 du J4 publie l'écart de glissement aux tours 60 et 120 et le chemin de r̂\*.
    - Constat de maquette sous C-HS : +0,214 / +0,161 (#81).
    - Au-delà d'un cran au tour 60, le cas est signalé (critère 19 (e) (iii)).

**Grandeurs restituées.** Niveaux normaux pour g = 2 %, r̄ = 1 %, π̄ = π\* = 0 / 2 / 10 %, à m = 1. Ils seront republiés par le script d'état stationnaire au J3, avec la valeur de m fixée avant l'essai.

| Grandeur | Définition | Unité | Dénominateur | Fenêtre | Niveau normal (0 ; 2 ; 10 %) |
|---|---|---|---|---|---|
| Glissement et cible | π_t (l. 219) ; π\*_t | % par an, une décimale | — | phase 5 ; ouverture | π\* |
| i_CB ; taux réel r = i − π | BC1 ; l. 215 | % par an | — | le tour | 1,00 ; 3,02 ; 11,10 % et 1,00 ; 1,02 ; 1,10 % (remesuré) |
| Prescription ; écart du taux décidé | i^règle_t ; i_{CB,t} − i^règle_t | % par an ; points | — | le tour | = i_CB ; 0 |
| Taux neutre retenu par la règle ; écart à la valeur initiale | r̂\*_t ; r̂\*_t − r̄ | % par an ; points | — | ouverture | 1 % ; 0 |
| π^e ; écart d'ancrage | π^e_t ; π^e_t − π\*_t | % par an ; points | — | ouverture | π\* ; 0 |
| Π^CB (fiche détaillée) | somme sur 12 tours / PIB des 12 derniers tours | % du PIB | PIB des 12 derniers tours | 12 tours | 0,0183 ; 0,0571 ; 0,2537 % (remesuré : i_CB × M^G/(n_a PIB), avec M^G/(n_a PIB) = 0,018282 / 0,018904 / 0,022857, fiche 9 N-2) ; ×m environ sous M33 |
| L^CB (fiche détaillée) | clôture / ΣPIB | années | PIB des 12 derniers tours | clôture | M^G/(n_a PIB) multiplié par le facteur de fenêtre 1,0108 / 1,0216 / 1,0638 (remesuré, formule de la l. 230) |
| H = Res ; E^CB (fiche détaillée) | clôture | années | idem | clôture | 0 ; 0 (« constant par construction au socle ») |
| Ratio de sacrifice | point-années de chômage par point de désinflation | point-années | — | scénario O2, documentation | 2,08 en maquette sous T9 réel ; 1/(λ_e λ_w β) = 2,5 |

### 9.6 Tests prévus au J3, puis au J4

Chaque test énonce une propriété et un seuil écrits avant l'essai. Ils couvrent les réserves 1 à 5 du § 5, les critères 1 à 24, les conditions C45 à C50 et C59 à C61.

| Jalon | Test | Propriété | Seuil |
|---|---|---|---|
| J3 | État stationnaire (critères 6 (a), (b), 8 (a) ; réserve 4) | Un pas sans choc depuis l'état résolu laisse r̂\* = r̄, π^e = π\*, i_CB = i^règle = (1 + r̄)(1 + π\*) − 1, Π^CB = i_CB(M^G + E^CB)/n_a, Res = 0 et L^CB = M^G\* (s_CB = 0), pour π\* ∈ {0 ; 2 % ; 10 %} et n_a ∈ {4 ; 12 ; 52} | 1e−10 relatif |
| J3 | Cas à la main (critère 1 (c) ; N-8) | Appel direct de BC1 à BC9 sur le cas de N-8 (i_CB de 3 à 4 %, achat de 25 à la banque, M^G\* = 20) : lignes 12, 13 et 16 ; E^CB par le stock et par les flux ; contrainte budgétaire ΔB_CB + ΔL^CB = ΔRes + ΔM^G + Π^CB − ligne 16. Le cas n'a pas été rejoué en fractions exactes (N-8) | 1e−12 × S^CB |
| J3 | Résultat et lignes exécutées (critères 1 (b), 4 (b)) | À chaque pas, Π^CB_t de la phase 1 égale 11c + 13 − 12 exécutées. Π^CB ne lit aucune grandeur intra-pas | 1e−12 × S^CB |
| J3 | Neutralité de s_CB (C59) | Sous i_B = i_res = i_CB, s_CB ∈ {0 ; 0,05 ; borne m·M^G/B ; 0,5} : trajectoires réelles et revenus identiques ; au-delà de la borne, Res > 0 et L^CB = 0 à la clôture | 1e−12 relatif |
| J3 | Perte (critère 2 (b) ; C60) | (i) i_CB < 0 sans placement raté : perte couverte par l'émission, E^CB inchangée ; (ii) i_CB < 0 et ς_B > 0 le même tour : ligne nommée = part non couverte, E^CB = −part, par le stock et par les flux (cas (ii) du critère 12 de la fiche 9) | 1e−12 × S^CB |
| J3 | Phases (critère 4) | r̂\*, π^e et π\*_{t+1} écrits une seule fois, en phase 1 ; aucune lecture de W_t, p_t ni U_{t−1} ; aucune écriture du bloc 8 en phases 2 à 7 ; aucune ligne 19b proposée au socle | aucune lecture hors ordre |
| J3 | Cible (ADR 0010 ; critère 4 (c)) | À levier fermé, π\*_{t+1} = π\*_t à chaque pas ; trajectoire identique à celle du moteur propriétaire provisoire (ADR 0010, Conséquences, test (4)) | exact |
| J3 | Stabilité (critère 11 (a) ; réserve 1) | Rayon de la boucle conjointe, hors racine nominale, sous C-HS (φ = 1), dans les deux régimes de T4 linéarisés séparément (C48), sur G et à π̄ ∈ {0 ; 2 ; 10 %}, ζ ∈ {4 ; 8}. Période et demi-vie publiées (11 (b)) | < 1 |
| J3 | Vitesses (critère 7 ; C36 ; réserve 2) | Branches ×0,5 et ×2 de a_π, k_I, λ_e et des vitesses des autres blocs : point fixe identique ; arrivée après les trois chocs (G +1 % aux tours 1 à 12, marche de π\* de +1 point, π^e +1 point) ; G +1 % permanent | 1e−6 après H = max(720 ; 20 demi-vies), soit 5 500 pas sous C-HS, H déclaré avant l'essai ; 1e−3 en 20 demi-vies pour le choc permanent |
| J3 | Gain statique (critère 6 (d) (i), 11 (c)) | ∂(demande)/∂r < 0, tous canaux réunis (C34) | < 0 (−0,2208 %/pt en maquette) |
| J3 | Clause II.7 (critère 12) | ρ_c et ρ_b sur D × G à la calibration retenue ; verdict ; clause de l'ADR 0010 (ρ_1 = ρ_0 par construction, π\* exogène) | verdict publié ; « déterminant » ⇒ décision citant M26, M24, M22 et M32 |
| J3 | Cible relevée (critère 10 (b) (i)) | Marche de π\* de +1 point : π̄ +1 point au point fixe, U\* inchangé, M/PIB stationnaire | 1e−6 |
| J3 | Persistance (critère 10 (b) (ii) ; réserve 5) | Taux tenu −1 point : premier écart au tour 3 au plus tard ; glissement au tour 120 supérieur d'au moins un cran à π\*, de même signe ; classement publié (sous C-HS, maquette : « nouveau palier », +0,396) | ≥ +0,1 point au tour 120 |
| J3 | **Superneutralité (critère 13 ; C15)** | Écart de r̄ et de chaque allocation en % du PIB entre π̄ = 0 et 10 %, sous les formes fermées de l'option. **Codé en échec attendu (`xfail`, strict), avec renvoi à #80** ; un succès inattendu fait échouer la batterie. Toute réouverture de C30, de la conversion ou des écarts remesure les trois sources ensemble (C61) | < 0,1 point (non tenu : 0,461 point aux bornes, 0,74 au maximum en maquette) |
| J3 | C46 | Pour C-HS : gain statique, Δr̄ après G +1 % permanent, Δr̄/k_I (identité exacte sous BC2), palier du critère 10 (b) (ii) et critère 13, publiés par le script | republiés ; Δr̄/k_I à 1e−6 |
| J3 | Bornes (critère 18) | Aucune borne. Scénarios G −5 % pendant 12 tours et marche de ±1 point : i_CB égale exactement la prescription, même négative | exact ; taux minimal publié |
| J3 | Test zéro (critère 17) | 720 pas sans choc, moyennes par blocs de 60 pas ; bandes à confirmer avec O1 avant l'essai (M19), voir question 3 | glissement π\* ± 0,1 ; π^e − π̄ ± 0,1 ; H nulle à 1e−12 × S^CB ; B_CB/B ± 1 point (0 au socle) ; E^CB nulle |
| J3 | Empreinte et coût (critères 20, 21) | Deux variables d'état nouvelles, plus π\*_t ; reprise de sauvegarde exacte ; part du bloc dans `tests/invariants/test_budget.py` | décompte exact ; ≤ 0,48 ms par pays-pas |
| J3 | Calibration (critère 23 ; C7, #45) | a_π, k_I et λ_e calés avec λ_w·β sur un ratio de sacrifice sourcé ; contrôle 0 < a_π < 1,5 et k_I > 0 au chargement | sources citées, ou « non trouvée » |
| J3 ou J4 | #54 (critère 16) | Essais (1), (2) et (4) depuis l'état résolu ; essai (3) en maquette ; critères (a) et (b) de `jeu` | verdict avant l'ouverture du levier de cible |
| J4 | #56 (critère 15) | Configuration (A) de référence : règle en vigueur, taux supérieur d'un point à la prescription aux tours 1 à 12, sous C-HS, à π̄ = 0, 2 et 10 % et sur un archétype à dette élevée ; pays joué (φ = 0) en mesure | P1 et P2 tenus, exigence avant l'ouverture du levier de taux ; P3 publié |
| J4 | Perceptibilité (critère 19 (e) ; O2) | Même choc apparié | deux crans en 12 tours ; pic au plus tard au tour 24 ; demi-vie supérieure à 60 tours déclarée avec le résidu au tour 60 |
| J4 | Restitution (conditions 1 à 10, #81) | Niveaux normaux restitués égaux à ceux du script | 1e−9 relatif |

### 9.7 Conditions transmises

**Conditions de `macro` (§ 6.6)** :
- **C45** (fiche 9) : **levée par M33**. T9 est réel, avec un taux de référence de Fisher sur π\*.
- **C46** (fiche 9) : publiée pour cinq règles (fiche 9 § 3.C-4). Republiée au J3 par le script pour C-HS (§ 9.6).
- **C47** (fiche 9, `jeu`, M33) : **levée par M33**. Couverture intégrale par défaut ; φ = 0 en écart déclaré ; φ jamais continu (C62).
- **C48** (fiche 8) : **levée** (§ 10, 04/10/2026). La règle « un régime de T4 à la fois » est reconduite aux tests du J3.
- **C49** (fiche 9) : suivie par C51. Condition de domaine de r̄ en `\limites` du bloc 9 ; voisinage dynamique à mesurer au J3.
- **C50** (fiche 9) : publiée (fiche 9 § 3.C-4) — 0,4983 en part d'une vente, 0 au sens de la l. 1543 sous C-HS. La boucle de `sec:menages` est à refaire avec les impôts (C52).

**Conditions de la fiche 9 qui touchent le bloc 8** (§ 6.6) :
- C59 : test « Neutralité de s_CB », et borne déclarée au § 9.2 ;
- C60 : test « Perte », et ligne 16 exécutée dans E^CB ;
- C61 : test « Superneutralité » ;
- C62 : φ n'est pas un levier continu (restitution, #82).

**Fiche 7 (`monnaie`, M31)** :
- **lecture (f) tranchée par A8** : `sec:banque` à mettre à jour (§ 9.8). Le bloc 7 n'a plus que **sept labels** (B1 à B7) ; B8 devient une équation du bloc 9 ;
- corridor de largeur nulle et i_res ≡ i_CB : **décidés** (M32) ;
- i_res ≤ i_CB : tenue avec égalité ;
- allocation du refinancement sans plafond ni collatéral : **acceptée** ;
- dépendance de ϱ̄_L à π\* (lecture (b)) : déclarée ;
- levier « achats de titres » (condition 6 de `jeu`) : **non ouvert au J4**, renvoyé au J6 (M32) ;
- ligne 19b-banque, que la fiche 7 attribue au bloc 8 en phase 7 (§ 9.4) : sans proposant au socle selon N-7 (question 1).

**Fiches 3 et 4 (`macro`)** :
- C1, C2, C5 et C12 tenues : π^e formée en phase 1, délai de deux tours ;
- C9 : prescription restituée ;
- C10 : contenu publié ; clause II.7 « non déterminante », réévaluée au J3 ;
- C11 : retour du niveau des prix déclaré (−0,106 % au tour 60, § 3.C-8) ;
- C13 : aucun canal de coût.

**Fiches 5 et 6 (`macro`)** :
- C14 : gain statique négatif ;
- C15 : défaut connu (#80) ;
- C26 : « non déclenchée » (les ménages lisent π\*) ;
- C32 : une seule lecture (π\*) ;
- C33 : effets d'un changement de cible déclarés, π\* paramètre ;
- C34 à C36 : tests du J3 ;
- C43 (délai du canal rentier) : test du J3, avec les fiches 7 et 9.

**J4** :
- #81 (restitution) ;
- #54, avec les critères (a) et (b) de `jeu` ;
- #56 en exigence avant l'ouverture du levier de taux ;
- « suivre la règle » comme valeur du levier de taux.

**J5** : régimes de souveraineté B à E et change ; cible lue hors du régime A (#64).

**J6** :
- C-g (gain endogène, « désancrage ») ;
- corridor D ;
- leviers d'achats (19b-banque) et de souscription (s_CB) ;
- prime i_B ≠ i_CB, avec le coût de portage de l'encaisse (i_B − i_CB)(m − 1)P/n_a (fiche 9 § 6.4) ;
- troncature du versement et recapitalisation (C60) ;
- plancher de i_CB si des billets sont introduits ;
- hyperinflation et réforme monétaire.

**`architect`** :
- **ADR 0011 (proposé)** :
  - propriétaire des lignes 19a ;
  - s_CB écrit en phase 1 ;
  - banque et banque centrale retirées de la phase 7 au socle (question 1) ;
  - `tab:phases`, l. 536 ; `temps_comptabilite.md:838` ; ADR 0009 l. 84.
- **Annotation de l'ADR 0010** (rang 9, #69) :
  - le bloc 8 devient propriétaire de π\*_t dès le J3 et écrit π\*_{t+1} = π\*_t, le levier de cible étant fermé au socle et au J4 (M32) ;
  - source du paramètre π\* (question 2) ;
  - la clause de réouverture de l'ADR 0010 n'est pas déclenchée (ρ_1 = ρ_0, § 3.C-4).
- **Annotation de l'ADR 0005, point 13** (m > 1, M33). Le point 5 (l. 215, précision rédactionnelle adoptée le 04/10/2026, critère 13 (b)) reste à annoter s'il ne l'est pas : je ne trouve pas d'annotation datée du point 5 dans l'ADR 0005 (`grep -n 'testé\|r = i\|i − π'` : aucune annotation).
- **`CONTEXT.md`** : « taux indiqué par la règle (prescription) », « taux neutre retenu par la règle », « écart d'ancrage des anticipations », « action intégrale sans fuite », « apprentissage à gain constant », « part de souscription de la banque centrale ».
- **Statut de l'inventaire** (`docs/blocs/README.md`).

**Issues** :
- #44 : se ferme à la branche n° 4 bis (fermeture monétaire, lecture (1)) ;
- #24, volet « banque centrale », et #49 : tranchés par M32 (glissement ; Fisher sur π\*). Clôture possible après le jalon 4 de #72 ;
- #26 :
  - point 1 : C60 (M33) ;
  - point 2 : forme (ii), M32 ;
  - points 4 et 5 : M31 ;
  - tableau de réponses au rang 11 ;
- #45 : J3 ;
- #61 : bloc 8 propriétaire ; le reste relève du J2 et du J3.

### 9.8 Surface d'impact documentaire (pour `docwriter`)

Encadrés `proposee` citant M32 (et M33 pour les points partagés), sans label (§ 9.1). Numéros de ligne à `9cc1ead`.

**`sec:banque_centrale`**, à écrire à la place du texte d'attente (l. 2346-2349) :
- **encadré de décision M32** : option C et socle commun du § 3.N ; lectures (a) à (e) ; points tranchés avec M33 (A8, i_B ≡ i_CB, E^CB_0 = 0) ; critère 13 en défaut connu (#80) ;
- **tableau des identifiants BC1 à BC9**, avec phase, statut et label prévu, sur le modèle de `tab:banque-equations` (l. 2024-2043) ;
- **règle de taux (BC1, BC2)** :
  - forme de Fisher sur π\* ; mesure lue : glissement π_{t−1} ;
  - prescription et levier (« suivre la règle », valeur du levier) ; action intégrale jamais réinitialisée ;
  - aucun terme d'activité, aucun plancher ;
  - identité i_res ≡ i_CB (corridor de largeur nulle) ;
  - `\limites` : principe de Taylor non tenu à court terme ; mémoire de r̂\* ; taux négatif sans billets ; cible abaissée qui baisse le taux (défaut 7, avec la dérivée 0,51) ;
- **anticipations (BC3)** :
  - apprentissage à gain constant de la moyenne ; gain de Gáti (2022), p. 19-20 ;
  - **ne citer Evans qu'après lecture à la source** (§ 3.0) ;
  - phase 1, délai de deux tours, condition de Barro et Gordon ;
  - aucune crédibilité (C-g au J4 ou J6) ;
  - C1 : π^e = π̄ démontré ;
- **cible (BC4)** : renvoi à `sec:cadre-calendrier` (l. 223) ; paramètre au socle et au J4 ; conditions d'ouverture du levier ;
- **bilan et résultat (BC5 à BC9)** :
  - s_CB (A8) ; Π^CB (renvoi à la l. 494) et sa forme réduite ;
  - lignes 12, 13 et 16 ; E^CB_0 = 0 et calcul deux fois ;
  - perte et C60 ; formes fermées de Res et L^CB, y compris sous m > 1 ;
- **phases** : tableau du § 9.4 ;
- **état stationnaire** : C2, C1, r̂\* = r̄ ; fermeture monétaire, lecture (1) de #44 ; aucune vitesse ; état initial résolu ;
- **conditions et stabilité** :
  - chiffres de référence sous C-HS (§ 9.3, avec renvoi à `sec:finances_publiques`) ;
  - clause II.7 « non déterminante » ; clause de l'ADR 0010 ;
  - C36 ; critère 13 en défaut connu ; tests du J3 (§ 9.6) ;
- **grandeurs restituées** (§ 9.5) ;
- **encadré `joueur`** : tableau de la condition 7 de `jeu`, complété (§ 9.5) ;
- **encadré `portee`** :
  - ni billets, ni avances, ni crédibilité, ni plancher, ni levier d'achats (J6) ;
  - π\* paramètre ; régimes B à E (J5) ; hyperinflation (J6) ;
  - aucun tirage, aucun historique.

**Passages existants à retoucher** :
- **l. 223 et 227 (`sec:cadre-calendrier`)** : « jusqu'à la fiche … ; ensuite, le bloc banque centrale … l'écrira depuis son levier » devient « le bloc banque centrale et anticipations, propriétaire, écrit π\*_{t+1} = π\*_t (décision M32 : levier de cible fermé au socle et au J4) ». Annotation de l'ADR 0010 en parallèle (rang 9).
- **l. 494-496 (`sec:cadre-caisse`)** :
  - « Les fonds propres E^CB restent à leur valeur initiale résolue » devient « … nulle (E^CB_0 = 0, décisions M32 et M33), sauf la part non couverte d'une perte, ligne nommée du bloc État et dette (C60), qui les réduit » ;
  - la phrase sur la perte renvoie à cette ligne.
- **l. 503** (M^G\*, « n'excède pas » ; « n'est pas un paramètre ») et **l. 2411** (« l'encaisse stationnaire du Trésor M^G\*, variable de l'état initial résolu ») : modifications de M33, à la charge de la fiche 9 § 9. Ici, seule la cohérence avec L^CB = m·P (§ 9.3) est à vérifier.
- **l. 2411** : « La décision M30 ajoute la cible d'inflation déclarée π\*, paramètre typé à source unique du moteur » est à ajuster selon la question 2.
- **`tab:phases`** :
  - l. 530, phase 1 :
    - contenu complété par « taux neutre retenu par la règle et anticipation du pas suivant ; part de souscription primaire de la banque centrale (décision M33, A8) » ;
    - écrivains « moteur (leviers), puis travail, banque centrale » : le bloc 8 lit le levier lu par le moteur dans la phase. Retouche de forme à qualifier par `architect` ;
  - l. 536, phase 7 : selon l'ADR 0011 (proposé) et la question 1, écrivains « État » ; contenu « souscriptions (19a, proposées par le bloc État et dette) ; achats décidés de la banque centrale (19b, jalon J6) » ;
  - l. 529, phase 0 : sans objet pour le bloc 8. ς_{B,t} est lue par le bloc 9 sous A8 ; la ligne 0 relève de #69 (Γ^e) et de la fiche 9 ;
  - l. 532, phase 3 : la colonne « Écrivent » porte encore « investissement, banque », alors que la fiche 7 (§ 9.8) retire la banque des écrivains. Constat hors du bloc 8, à vérifier par la session.
- **`sec:banque` (lecture (f) tranchée par A8)** :
  - l. 2009 : « renvoyée à … M33 » devient « tranchée par M33 : A8 » ;
  - l. 2011-2012 : **branche « variante » à retirer**, la branche A8 devient le texte ;
  - l. 2040 : ligne B8 retirée ; renvoi au label du bloc État et dette ; **sept labels** ;
  - l. 2122-2135 (`sec:banque-placement`) : la règle du reliquat devient une équation du bloc État et dette, à laquelle la sous-section renvoie ;
  - l. 2130 : « ligne 19a-BC, décidée par le bloc banque centrale » devient « proposée par le bloc État et dette, part s_CB écrite par le bloc banque centrale en phase 1 » ;
  - l. 2132 : la ligne 19b « est proposée par le bloc banque centrale » devient « aucune n'est proposée au socle (levier au jalon J6) » (question 1) ; ς_{B,t} est lue par le bloc État et dette ;
  - l. 2135 : provenance M33 ;
  - l. 2157 et 2161 : phase 7 retirée ;
  - l. 2169 : 19a-banque retirée des lignes proposées ; 19b-banque reçue au J6 seulement ;
  - l. 2190 : « i_{res,t} » devient l'identité i_res ≡ i_CB, et « i_{B,t} selon la règle du bloc État et dette » devient « i_B ≡ i_CB (M33) » ;
  - l. 2193 : ligne de la phase 7 réduite à « rien » ;
  - l. 2058 : « hypothèse transmise » devient « décision M32 » ;
  - l. 2059 et 2214 : « la forme … relève du bloc banque centrale » devient « forme de Fisher sur π\* (décision M32) » ;
  - l. 2116 : « condition transmise » devient « acceptée (M32) » ;
  - l. 2229 : i_{CB,0} = (1 + r̄)(1 + π\*) − 1 ;
  - l. 2265 : « selon la lecture (f) » devient « lu par le bloc État et dette (A8) » ;
  - l. 2325 : le levier « achats de titres » n'est **pas ouvert au J4** (M32 ; J6).
- **l. 279-280 (`tab:instruments`)** : i_res ≡ i_CB au socle.
- **l. 1020 (`sec:travail-stationnaire`)** : fermeture monétaire, lecture (1) de #44 — r̄ paramètre, part de la dépense résolue (M32-M33).
- **l. 1185 (`sec:prix-conditions`)** : verdict de la clause, « non déterminant » à la calibration indicative (fiche 8 § 3.C-4), réévalué au J3.
- **l. 1456 (C26)** : « non déclenchée » (M32).
- **l. 1460, 1907 et 2265** : renvoi aux réponses du § 9.7.
- **l. 1519** : « la relation de Fisher que retiendra le bloc » devient « la forme de Fisher sur π\* retenue par M32 ».
- **`tab:leviers-cadre`, l. 2380** :
  - « dans la mesure où leur taux suit le taux directeur » devient « leur taux étant le taux directeur au socle (i_B ≡ i_CB, M33) » ;
  - contrepartie : ligne 16 = i_CB(M^G + E^CB)/n_a.
- **`tab:leviers`, l. 2399** : ligne « Taux directeur » — type : valeur numérique ou « suivre la règle » ; unité : % par an ; délai : 0 tour ; contrepartie : lignes 11a à 11c, 12, 13 et 16. Mention « cible : paramètre au socle et au J4 », « achats de titres : J6 ». Avis de `jeu` à la revue finale (rang 12).
- **`tab:calibration`** :
  - encadré « paramètres du bloc banque centrale et anticipations, décision M32 », sur le modèle de la l. 2435 ;
  - lignes a_π, k_I, λ_e, s_CB et r̄ (§ 9.2) ; aucune borne ;
  - l. 2453 (π\*) : « reconduite par le moteur jusqu'au bloc » devient « écrite par le bloc banque centrale (reconduction, M32) ; levier fermé au J4 » ;
  - **l. 2461 (U^eq)** : « lue à source unique par le bloc banque centrale et anticipations » est faux sous M32 (aucun terme d'activité) : « non lue par la règle de taux au socle ».
- **`tab:symboles`** (l. 2760-2863) :
  - nouvelles entrées : i^règle_t, r̂\*_t, r̄, a_π, k_I, λ_e, s_{CB,t} ;
  - l. 2766 (i_X) : i_res ≡ i_CB et i_B ≡ i_CB au socle ;
  - l. 2818 (π^e_t) : renvoi à BC3 (`sec:banque_centrale`) ;
  - l. 2832 (π\*) : écrite par le bloc banque centrale (BC4) ;
  - l. 2794 (Π^CB) : renvoi à BC6 ;
  - collisions vérifiées par `grep -c -F` à `9cc1ead` : `k_I`, `a_\pi`, `\lambda_e`, `\hat`, `s_{\mathit{CB}}` et `i^{\mathrm{ref}}` : 0 chacun ; `\bar r` : 2 (l. 2214, sens identique). Points de notation : question 4.
- **`sec:ecartees`**, sous-section « Banque centrale et anticipations (décision M32) » :
  - A : mesure en log contre glissement, six écrêtages, loi à seuil, avances (ν_3) ;
  - B : intégrateur à fuite et bande, loi K1a, drapeaux, pire valeur sur G de 1,0135 ;
  - T : 2 points de biais par point d'erreur sur r\* ;
  - C-h, C-c ; D (J6) ; R (référence) ;
  - a_π = 1,5 ; formation de π^e en phase 9 ; plancher à 0 ; terme d'activité.
- **`tab:instabilites`, paragraphe après la l. 2715** :
  - le bloc réintroduit la **forme** de l'instabilité 4 (estimateur du taux naturel sans ancre ni bande), avec le fait nouveau exigé : rayon inférieur à 1 sur G dans les deux régimes, sous T9 (§ 3.C-4, contre-épreuve de `macro` § 6.2) et sous C-HS (fiche 9 § 3.C-4), à remesurer au J3 ;
  - il ne réintroduit ni la 2 (aucune avance), ni la 15 (aucune borne), ni une loi de crédibilité à seuil (K1a) ;
  - la divergence sous φ = 0 est un régime déclaré.
- **`sec:changements-v3x`** (l. 90-116) : ligne 14, « Banque centrale et anticipations (décision M32), proposée », et retouches A8 de `sec:banque` et `tab:phases`.
- **`tab:correspondance`** : inchangée, aucun label au J1.
- **`tab:chantiers`** : inchangée, aucun mécanisme essayé sur le moteur v3.
- **Inchangées** : `tab:matrice-flux`, `tab:portes-monnaie` et `tab:matrice-bilans` du fait du bloc 8 (sortie de `verifier_matrices.py` au § 9.4). La forme de la ligne C60 relève de la fiche 9.

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| 04/10/2026 | Ouverture (issue #72) ; § 1 et § 2 proposés (jalon 1), en attente de validation des critères par le mainteneur | `monnaie` ; session principale |
| 04/10/2026 | Relecture croisée intégrée (avis de `macro`, `monnaie` et `jeu`, une relance ciblée ; qualifications d'`architect`) ; options ouvertes marquées « à trancher par le mainteneur » | `macro` ; `monnaie` ; `jeu` ; `architect` ; session principale |
| 04/10/2026 | Critères validés par le mainteneur (jalon 1 de #72 terminé), amendements adoptés consignés au § 2 | mainteneur ; session principale |
| 04/10/2026 | Jalon 2, première partie (partielle) : § 3 à § 5 instruits (options A, B, C et variantes, socle commun, tableau comparatif, recommandation de l'option C) ; contre-épreuve, essai (3) de #54 et remesure V restants ; § 6 et § 7 à rendre | `monnaie` ; session principale |
| 04/10/2026 | Avis de `jeu` (§ 7) : option C lisible sous dix conditions ; π\* paramètre au J4 (le verdict de #54 ne suffit pas) ; défaut du levier budgétaire en pays joué renvoyé à la fiche 9 | `jeu` ; session principale |
| 04/10/2026 | Avis de `macro`, expert consulté (§ 6), favorable à C, et contre-épreuve indépendante (critère 11) : tout reproduit sauf la paire complexe (artefact de linéarisation au coude de T4, C48) ; conditions C45 à C50 ; fiche « avis rendus », sous réserve de C48 | `macro` ; session principale |
| 04/10/2026 | C48 levée : paire complexe, pays joué à 10 % et a_π = 1,5 republiés par régime de T4 (§ 3.0, § 3.C-4, § 3.C-8, § 4) ; second coude de la linéarisation de la baisse identifié ; critère 12 remesuré, verdict inchangé. Les chiffres du § 6.2 (contre-épreuve de `macro`) sont confirmés | `monnaie` ; session principale |
| 04/10/2026 | Décision du mainteneur : M32, prise par paire (M32-M33) ; voir § 8 | mainteneur ; session principale |
| 04/10/2026 | Issues créées sur accord du mainteneur : #80 (critère 13), #81 (restitution J4 banque centrale), #82 (restitution J4 État et dette) ; commentaires publiés sur #54, #73 et #55 | session principale |
| 04/10/2026 | § 9 rédigé (conséquences de M32 et des points tranchés avec M33 : équations BC1 à BC9 et labels prévus, paramètres, chiffres de référence sous C-HS, phases sous A8, restitution, tests du J3 et du J4 avec le critère 13 en échec attendu (#80), conditions transmises, surface d'impact pour `sec:banque_centrale`, `sec:banque` et `tab:phases`) ; renvois à l'ADR d'A8 rapportés à l'ADR 0011 (proposé) par la session | `monnaie` ; session principale |
