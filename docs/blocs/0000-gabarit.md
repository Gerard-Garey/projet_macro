---
bloc: <nom du bloc, tel que dans l'inventaire README.md>
module: src/nations/blocs/<module>.py | transverse : src/nations/noyau/ et src/nations/moteur/ (bloc-cadre ; radicaux de labels `noyau` et `moteur`)
expert pilote: macro | monnaie
experts consultés: <monnaie | macro, sur le sujet que README.md désigne ; toujours jeu>
statut: à instruire | en instruction | avis rendus | décidée (M-n) | spécifiée | implémentée
décision: M-n (date) | —
issue: #<n>
---

# Fiche comparative — <bloc>

> **Gabarit validé à l'usage (M20)** sur la première fiche, « temps et comptabilité » (M22) : version retouchée d'après les retours de l'issue #17, **validée par le mainteneur le 30/09/2026**. Copier sous le nom de fiche que donne l'inventaire `README.md` § 1 (colonne « Fiche »), en gardant les rubriques et leur ordre. Toute rubrique sans contenu porte la mention « non instruit », « non mesuré » ou « sans objet, parce que … », jamais un vide.

Une fiche comparative instruit **l'origine de l'approche** d'un bloc (`docs/exigences.md` § 2.3) : la spécification v1.5, le moteur v2.0, ou une approche nouvelle. Elle est **instruite par l'expert pilote**, commentée par `jeu` et par l'expert consulté que désigne `README.md`, et **décidée par le mainteneur** (décision M-n, reportée dans `docs/feuille-de-route.md`). Aucune approche n'entre dans le moteur ni dans la spécification sans cette décision. Les agents n'écrivent pas la fiche dans le dépôt : elle figure dans leur compte rendu et la session principale la commite. Un **bloc-cadre** (temps et comptabilité) n'est pas un module de `blocs/` : sa fiche instruit ce que le cadre **définit** (conventions, matrices, règles), non des flux proposés ; les adaptations que cela impose sont signalées rubrique par rubrique.

Règles de rigueur (`CLAUDE.md`, « Rigueur ») : un chiffre se remesure ou cite sa source ; une équation de la v1.5 n'a jamais été garantie exécutée ; un comportement de la v2.0 ne vaut que sous son profil (état D1, **non versé** : aucun fait ne peut y être remesuré) et avec ses défauts connus ; chaque fait de la première tentative porte son **statut** S+O, O, R ou L (`CONTEXT.md`, « Statut d'un fait ») ; chaque référence est une publication retrouvée. Citer `archive/v1.5/…` avec numéro d'équation et section, ou avec le **numéro de ligne du `.tex`** quand section ou équation ne sont pas identifiables sans compiler ; `archive/v2.0/…` avec fichier et ligne. **Principe de simplicité** (adopté par le mainteneur le 30/09/2026, fiche « temps et comptabilité » § 2 ; `CONTEXT.md`) : à exigences comptables égales, l'option la plus simple pour le joueur et pour le moteur est préférée ; toute complexité se justifie par une identité qu'elle rend vérifiable ou par un mécanisme perçu à l'échelle d'une partie ; une simplification ne supprime ni une contrepartie comptable visible d'un levier ni une grandeur restituée au tour ; les identités, les tolérances relatives, le déterminisme, les invariants de l'ADR 0002 et la concordance ne se simplifient pas.

## 1. Question posée

- **Ce que le bloc doit produire** : les variables nouvelles et les flux proposés qu'il rend au noyau — pour un bloc-cadre, les **conventions, matrices et règles** qu'il définit — avec pour chaque grandeur sa définition, son unité, son dénominateur et sa fenêtre (exprimée en pas, et en tours quand le joueur la lit).
- **Ce qu'il lit** : variables d'ouverture venant d'autres blocs ; leviers du joueur qui le touchent ; décisions du mainteneur déjà prises qui le contraignent (M-n).
- **Frontières** : blocs voisins et sujets partagés (inflation, crédit, dette publique), avec l'expert consulté et, pour chacun, les critères du § 2 qui lui reviennent.
- **Ce que la fiche ne tranche pas** : périmètre exclu, renvoyé à une autre fiche ou à un jalon ultérieur ; ce que la fiche laisse ouvert pour qu'un ajout ultérieur (ligne, colonne, instrument) ne réécrive pas ce qu'elle fixe.

## 2. Critères d'évaluation, écrits avant l'instruction

Liste fermée des critères sur lesquels les options seront comparées, fixée **avant** de mesurer et **validée par le mainteneur** (point de décision de l'issue d'ouverture, consigné au § 10). Elle ne se déplace pas après observation ; un amendement adopté avant l'instruction est consigné sous le tableau, avec son origine, et prévaut sur le texte qu'il modifie. Chaque critère porte entre parenthèses **qui l'a proposé** (`macro`, `monnaie`, `jeu`, mainteneur) ; un critère peut se subdiviser en lettres (a), (b)… quand plusieurs experts en précisent des aspects distincts. Un critère est une **exigence** (il peut écarter une option) ou une **mesure** (il décrit sans écarter) : le dire. Colonnes : ce qui est attendu, avec le **seuil ou la forme du verdict** ; par quoi on le vérifie (script d'`outils/`, calcul à la main donné dans la fiche, test, avis) ; **qui** vérifie ; **quand** (à la fiche : décompte ou calcul à la main ; J2 à J4 : mesure par test ou scénario).

| N° | Critère | Ce qui est attendu (seuil ou forme du verdict) | Par quoi on le vérifie | Qui | Quand |
|---|---|---|---|---|---|
| 1 | Cohérence stock-flux | Tout flux quitte un bilan et entre dans un autre ; identités touchées bouclées sans solde résiduel ; la valeur nette, seule grandeur résiduelle, calculée deux fois (stock et flux) | Matrice des flux de l'option, écrite en tableau ; script des matrices (issue #19) | expert pilote ; `monnaie` pour la banque et la banque centrale | fiche ; J2 (test d'identité) |
| 2 | État stationnaire | Calculable à la main ou par le script d'`outils/`, sans simulation ; ne dépend ni d'une vitesse d'ajustement ni de la durée du pas | Calcul donné dans la fiche | expert pilote | fiche ; J3 (script contre moteur à t = 0) |
| 3 | Stabilité | Aucune instabilité connue réintroduite sans fait nouveau | Liste des instabilités d'`archive/faits_mesures_G_K.md` § 6, puis `tab:instabilites` de la spécification | expert pilote | fiche |
| 4 | Coût de calcul | Compatible avec 52/12 ms par pays-pas (1 ms par pays-semaine, M13, M22) ; aucune optimisation itérative à chaque pas | Décompte d'opérations par pas (fiche) ; `tests/invariants/test_budget.py` | expert pilote ; `audit` | fiche (décompte) ; J3 (mesure) |
| 5 | Lisibilité pour le joueur | Effet identifiable, délai en tours entiers et coût perceptibles à l'échelle d'une partie (60 à 120 tours) ; aucun effet plus rapide que le tour sans contrepartie visible le même tour | Tableau **levier → indicateur → délai en tours → contrepartie comptable** (§ 9, « Interfaces ») ; avis de `jeu` (§ 7) ; scénario apparié (test O2) | `jeu` | fiche (tableau) ; J4 (scénario) |
| 6 | Simplicité : paramètres, bornes, postes, lignes de flux, phases, variables d'état | Le moins possible ; toute borne déclarée, mécanisme préféré à la borne ; chaque élément justifié par une identité vérifiable ou un mécanisme perçu (principe de simplicité) | Décompte par option, en tableau, avec la justification de chaque élément | expert pilote | fiche |
| n | <critère propre au bloc> | | | | |

## 3. Options

Une sous-section par option, dans l'ordre : **A. v1.5**, **B. v2.0**, puis **C, D… approches nouvelles** (au moins une quand la littérature en offre une pertinente). Si la v1.5 et la v2.0 coïncident, le dire et ne traiter qu'une option en le signalant. Chaque option comporte les neuf rubriques ci-dessous, dans cet ordre.

**Découpage par question** (admis quand la fiche le motive, en tête du § 3) : quand un bloc tranche plusieurs questions indépendantes (pour un bloc-cadre : calendrier, conversions, matrices, tolérances, phases), les options nouvelles peuvent ne différer que sur une question et partager un **socle commun** sur les autres, instruit une fois dans une sous-section propre (« 3.N ») avec laquelle chacune se combine ; les options A et B restent instruites en entier. Le tableau du § 4 renvoie alors à la colonne de l'option ou à la question du socle.

**Mesures et littérature** (en tête du § 3) : liste des mesures exécutées (commande, date), avec mention de celles qu'un autre agent ou la session principale a recalculées ; liste des **sources cherchées**, en distinguant celles qui ont été lues de celles qui n'ont pas été accessibles (proxy, accès payant), et ce que la littérature retrouvée permet ou ne permet pas de conclure.

### 3.A Option A — v1.5

1. **Source exacte** : `archive/v1.5/Nations_et_Marches_v1_5.tex`, équations (n) et section § x.y, ou numéro de ligne du `.tex` ; pour la v2.0, `archive/v2.0/<fichier>:<ligne>` ; pour une approche nouvelle, la référence retrouvée (auteur, année, titre, et l'endroit qui soutient l'équation).
2. **Équations** : écrites en LaTeX, avec leurs variables (définition, unité, fenêtre) et leurs paramètres (valeur d'origine, unité). Statut épistémique proposé pour chacune : *dérivée*, *approchée*, *choix de conception*. Pour un bloc-cadre : conventions, matrices et règles, en tableaux.
3. **État stationnaire impliqué** : calcul à la main quand c'est possible (ratios de stocks, taux réel, inflation, part salariale selon le bloc) ; sinon « non calculable à la main », et pourquoi ; ou « sans objet, parce que … » (bloc-cadre), en disant alors ce que le cadre impose à l'état stationnaire (valeur stationnaire des variables retardées, fenêtres).
4. **Comportement mesuré et sa source** : ce que l'option a produit quand elle a été exécutée, avec le rapport ou la commande qui l'établit (synthèse des faits mesurés d'`archive/`, ou `uv run …` sur le moteur v3 quand une maquette existe), chaque fait avec son **statut S+O, O, R ou L**. Sinon : « non mesuré ». Un chiffre de la v1.5 provenant de son prototype est un chiffre **rapporté** (R), pas mesuré ; l'état D1 de la v2.0 n'est pas versé.
5. **Coût de calcul** : opérations par pas, boucles, résolutions numériques ; verdict au regard du budget de 52/12 ms par pays-pas (1 ms par pays-semaine).
6. **Défauts connus et instabilités documentées** : chaque défaut avec sa source (fichier et ligne, fait mesuré avec statut, table des chantiers de la v1.5) ; dire si l'option réintroduit une instabilité connue.
7. **Identités de bilan touchées** : bilans concernés (ménages, entreprises, banque, banque centrale, État), flux qui les relient et leur ligne dans la matrice des flux ; **soldes résiduels, hors valeur nette** (à proscrire ; la valeur nette est calculée par le stock et par les flux, l'identité entre les deux étant le contrôle) ; **positions intra-pas admises** (un poste qui peut être négatif entre deux phases, avec la phase qui le résorbe et l'identité de clôture qui le vérifie) ; pour les lignes qui font varier M ou H, la **lecture sous laquelle les colonnes ΔM / ΔH sont écrites** (localisation du compte du Trésor, existence des billets). Pour un bloc-cadre : « sans objet, parce que … » n'est admis que si les matrices sont données ailleurs dans la fiche.
8. **Ce que le joueur en percevrait** : indicateur qui bouge, délai en tours, ampleur, levier ouvert ou fermé ; à soumettre à `jeu`.
9. **Empreinte sur l'état** : variables d'état retardées que l'option exige, chacune avec son nombre de pas, son unité et sa valeur stationnaire explicite ; variables cumulées (résultat sur une fenêtre) ; aucun historique (ADR 0002). *Rubrique ajoutée en fin de liste (retour de `monnaie`, #17) pour ne pas renuméroter les huit rubriques d'origine.*

### 3.B Option B — v2.0

Mêmes neuf rubriques.

### 3.C Option C — <approche nouvelle : nom>

Mêmes neuf rubriques. La référence est vérifiée ; si la littérature ne permet pas de conclure sur un point, l'écrire.

## 4. Tableau comparatif

Une ligne par critère du § 2 (et par lettre quand le critère en a), une colonne par option ; chaque cellule renvoie à la rubrique du § 3 qui l'établit (option et rubrique, ou question du socle commun). Aucune cellule sans renvoi. Les critères de jouabilité peuvent renvoyer au § 7.

| Critère | A. v1.5 | B. v2.0 | C. <nouvelle> |
|---|---|---|---|
| | | | |

## 5. Avis de l'expert pilote

- **Recommandation** : l'option, ou la combinaison d'options, et ses motifs, critère par critère.
- **Réserves et conditions** : ce qu'il faudra vérifier au premier essai (critères écrits avant l'essai, avec seuils et jalon).
- **Lectures possibles** : si la spécification v1.5, une source ou les experts admettent deux positions sur un point, les décrire côte à côte (lettres (a), (b)…), donner un avis ; le mainteneur tranche.
- **Ce que l'option retenue coûte en fidélité** si elle s'écarte de la littérature ou de la première tentative.

## 6. Avis de l'expert consulté

Rubrique présente dès que `README.md` § 1 désigne un expert consulté pour le bloc (sujets frontière : inflation, crédit, dette publique ; ou tout autre sujet que l'inventaire nomme) ; sinon « sans objet ». Position de `monnaie` ou de `macro` sur la part du sujet qui lui revient : chiffres de l'expert pilote reproduits ou contestés, constats sur les options (emplacement, constat, correction proposée), avis sur chaque lecture du § 5. En cas de désaccord avec l'expert pilote, les deux positions sont décrites ; le mainteneur tranche. Les constats acceptés par l'expert pilote sont intégrés au § 3 avec renvoi au constat ; ceux qui restent ouverts deviennent une lecture du § 5.

## 7. Avis de `jeu`

Pour chaque option : ce que le joueur voit et comprend (indicateur, délai en tours, ampleur) ; leviers ouverts ou fermés et leur coût perceptible ; stratégies rendues possibles ou dominantes, ou « sans objet, parce que … » (bloc transverse qui n'ouvre aucun levier) ; risques (réponse imperceptible, effet instantané sans coût, piège irréversible sans signal, comportement contre-intuitif). Préférence motivée, distinguée de celle de l'expert pilote ; conditions demandées au § 9 ; avis sur chaque lecture du § 5 vue du joueur.

## 8. Décision du mainteneur

- **Numéro** : M-n (reporté dans `docs/feuille-de-route.md`, § 4).
- **Date** :
- **Option retenue** : A, B, C, ou combinaison précisée équation par équation (ou question par question, lecture par lecture).
- **Motifs** : en quelques lignes, dans les mots du mainteneur ; s'il retient les recommandations concordantes des experts sans autre motif, le dire.
- **Conditions et réserves** : ce qui devra être vérifié, et à quel jalon (seuils repris du § 5 et du § 7).
- **Ce qui est écarté et pourquoi** : alimente la section « pistes écartées » de la spécification.

Avant cette rubrique, le statut de la fiche est au plus « avis rendus ». Une décision ne se réécrit pas : une révision fait l'objet d'une nouvelle décision M-m, datée, qui cite la précédente.

## 9. Conséquences de la décision

- **Labels d'équation** à créer : `eq:<module>-<nom>` pour chaque équation retenue, avec son statut et sa provenance (`docs/specification/CONVENTIONS.md` § 2).
- **Paramètres** : liste (nom dans le code, valeur, unité, source) à porter dans la table de calibration.
- **Ce qui reste paramétrable après la décision** : les paramètres déclarés dont la valeur peut changer par une décision M-m ultérieure sans rouvrir celle-ci, et ceux dont le changement la rouvre ; aucun drapeau de mode (ADR 0002).
- **Interfaces** : variables lues et rendues, flux proposés au noyau avec leur ligne de la matrice des flux et leur phase ; ce que les blocs voisins doivent fournir ; pour chaque **levier**, la phase de lecture, le premier flux modifié, le **délai en tours** et la contrepartie comptable visible le même tour (tableau du critère 5).
- **Tests attendus** : propriétés (signe, délai, ordre de grandeur), pas de valeurs à reproduire ; identités à vérifier ; jalon de chaque test.
- **Surface de spécification** : sections du plan fixe touchées.
- **Issues** : titres proposés pour la spécification (`docwriter`) et l'implémentation (`coder`).

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| | Ouverture (issue #n) ; § 1 et § 2 proposés | expert pilote, experts consultés, `jeu` ; session principale |
| | Critères validés (issue #n) | mainteneur |
| | Instruction déposée (§ 3 à 5) | expert pilote |
| | Avis de l'expert consulté (§ 6) | `monnaie` ou `macro` |
| | Avis de `jeu` (§ 7) | `jeu` |
| | Constats intégrés ; statut « avis rendus » | expert pilote ; session principale |
| | Décision M-n | mainteneur |
