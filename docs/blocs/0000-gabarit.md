---
bloc: <nom du bloc, tel que dans l'inventaire README.md>
module: src/nations/blocs/<module>.py
expert pilote: macro | monnaie
experts consultés: <monnaie | macro, pour les sujets frontière ; toujours jeu>
statut: à instruire | en instruction | avis rendus | décidée (M-n) | spécifiée | implémentée
décision: M-n (date) | —
issue: #<n>
---

# Fiche comparative — <bloc>

> **Gabarit à valider par le mainteneur avant la première fiche** (issue #6, critère d'acceptation). Copier sous `docs/blocs/<module>.md`, en gardant les rubriques et leur ordre. Toute rubrique sans contenu porte la mention « non instruit » ou « non mesuré », jamais un vide.

Une fiche comparative instruit **l'origine de l'approche** d'un bloc (`docs/exigences.md` § 2.3) : la spécification v1.5, le moteur v2.0, ou une approche nouvelle. Elle est **instruite par l'expert pilote**, commentée par `jeu` et par l'expert consulté sur les sujets frontière, et **décidée par le mainteneur** (décision M-n, reportée dans `docs/feuille-de-route.md`). Aucune approche n'entre dans le moteur ni dans la spécification sans cette décision. Les agents n'écrivent pas la fiche dans le dépôt : elle figure dans leur compte rendu et la session principale la commite.

Règles de rigueur (`CLAUDE.md`, « Rigueur ») : un chiffre se remesure ou cite sa source ; une équation de la v1.5 n'a jamais été garantie exécutée ; un comportement de la v2.0 ne vaut que sous son profil (état D1) et avec ses défauts connus ; chaque référence est une publication retrouvée. Citer `archive/v1.5/…` avec numéro d'équation et section, `archive/v2.0/…` avec fichier et ligne.

## 1. Question posée

- **Ce que le bloc doit produire** : les variables nouvelles et les flux proposés qu'il rend au noyau, avec pour chaque grandeur sa définition, son unité, son dénominateur et sa fenêtre.
- **Ce qu'il lit** : variables d'ouverture venant d'autres blocs ; leviers du joueur qui le touchent.
- **Frontières** : blocs voisins et sujets partagés (inflation, crédit, dette publique), avec l'expert consulté.
- **Ce que la fiche ne tranche pas** : périmètre exclu, renvoyé à une autre fiche ou à un jalon ultérieur.

## 2. Critères d'évaluation, écrits avant l'instruction

Liste fermée des critères sur lesquels les options seront comparées, fixée **avant** de mesurer. Au minimum :

| Critère | Ce qui est attendu | Comment on le vérifie |
|---|---|---|
| Cohérence stock-flux | Tout flux quitte un bilan et entre dans un autre ; identités touchées bouclées sans solde résiduel | Matrice des flux de l'option |
| État stationnaire | Calculable à la main ; ne dépend pas d'une vitesse d'ajustement | Calcul donné dans la fiche |
| Stabilité | Aucune instabilité connue réintroduite sans fait nouveau | Liste des instabilités d'`archive/` |
| Coût de calcul | Compatible avec 1 ms par pays-semaine ; aucune optimisation itérative à chaque pas | Décompte d'opérations ou mesure |
| Lisibilité pour le joueur | Effet identifiable, délai et coût perceptibles à l'échelle d'une partie | Avis de `jeu` |
| Nombre de paramètres et de bornes | Le moins possible ; toute borne déclarée, mécanisme préféré à la borne | Décompte |
| <critère propre au bloc> | | |

## 3. Options

Une sous-section par option, dans l'ordre : **A. v1.5**, **B. v2.0**, puis **C, D… approches nouvelles** (au moins une quand la littérature en offre une pertinente). Si la v1.5 et la v2.0 coïncident, le dire et ne traiter qu'une option en le signalant. Chaque option comporte les huit rubriques ci-dessous, dans cet ordre.

### 3.A Option A — v1.5

1. **Source exacte** : `archive/v1.5/Nations_et_Marches_v1_5.tex`, équations (n) et section § x.y ; pour la v2.0, `archive/v2.0/<fichier>:<ligne>` ; pour une approche nouvelle, la référence retrouvée (auteur, année, titre, et l'endroit qui soutient l'équation).
2. **Équations** : écrites en LaTeX, avec leurs variables (définition, unité, fenêtre) et leurs paramètres (valeur d'origine, unité). Statut épistémique proposé pour chacune : *dérivée*, *approchée*, *choix de conception*.
3. **État stationnaire impliqué** : calcul à la main quand c'est possible (ratios de stocks, taux réel, inflation, part salariale selon le bloc) ; sinon « non calculable à la main », et pourquoi.
4. **Comportement mesuré et sa source** : ce que l'option a produit quand elle a été exécutée, avec le rapport ou la commande qui l'établit (synthèse des faits mesurés d'`archive/`, ou `uv run …` sur le moteur v3 quand une maquette existe). Sinon : « non mesuré ». Un chiffre de la v1.5 provenant de son prototype est un chiffre **rapporté**, pas mesuré.
5. **Coût de calcul** : opérations par pas, boucles, résolutions numériques ; verdict au regard du budget de 1 ms par pays-semaine.
6. **Défauts connus et instabilités documentées** : chaque défaut avec sa source (fichier et ligne, fait mesuré, table des chantiers de la v1.5) ; dire si l'option réintroduit une instabilité connue.
7. **Identités de bilan touchées** : bilans concernés (ménages, entreprises, banque, banque centrale, État), flux qui les relient, soldes calculés comme résidus s'il y en a (à justifier ou à proscrire).
8. **Ce que le joueur en percevrait** : indicateur qui bouge, délai, ampleur, levier ouvert ou fermé ; à soumettre à `jeu`.

### 3.B Option B — v2.0

Mêmes huit rubriques.

### 3.C Option C — <approche nouvelle : nom>

Mêmes huit rubriques. La référence est vérifiée ; si la littérature ne permet pas de conclure sur un point, l'écrire.

## 4. Tableau comparatif

Une ligne par critère du § 2, une colonne par option ; chaque cellule renvoie à la rubrique du § 3 qui l'établit. Aucune cellule sans renvoi.

| Critère | A. v1.5 | B. v2.0 | C. <nouvelle> |
|---|---|---|---|
| | | | |

## 5. Avis de l'expert pilote

- **Recommandation** : l'option, ou la combinaison d'options, et ses motifs, critère par critère.
- **Réserves et conditions** : ce qu'il faudra vérifier au premier essai (critères écrits avant l'essai, avec seuils).
- **Deux lectures possibles** : si la spécification v1.5 ou une source admet deux lectures, les décrire et donner un avis ; le mainteneur tranche.
- **Ce que l'option retenue coûte en fidélité** si elle s'écarte de la littérature.

## 6. Avis de l'expert consulté (sujets frontière)

Rubrique présente quand le bloc touche l'inflation, le crédit ou la dette publique ; sinon « sans objet ». Position de `monnaie` ou de `macro` sur la part du sujet qui lui revient. En cas de désaccord avec l'expert pilote, les deux positions sont décrites ; le mainteneur tranche.

## 7. Avis de `jeu`

Pour chaque option : ce que le joueur voit et comprend (indicateur, délai, ampleur) ; leviers ouverts ou fermés et leur coût perceptible ; stratégies rendues possibles ou dominantes ; risques (réponse imperceptible, effet instantané sans coût, piège irréversible sans signal, comportement contre-intuitif). Préférence motivée, distinguée de celle de l'expert pilote.

## 8. Décision du mainteneur

- **Numéro** : M-n (reporté dans `docs/feuille-de-route.md`, § 4).
- **Date** :
- **Option retenue** : A, B, C, ou combinaison précisée équation par équation.
- **Motifs** : en quelques lignes, dans les mots du mainteneur.
- **Conditions et réserves** : ce qui devra être vérifié, et à quel jalon.
- **Ce qui est écarté et pourquoi** : alimente la section « pistes écartées » de la spécification.

Avant cette rubrique, le statut de la fiche est au plus « avis rendus ». Une décision ne se réécrit pas : une révision fait l'objet d'une nouvelle décision M-m, datée, qui cite la précédente.

## 9. Conséquences de la décision

- **Labels d'équation** à créer : `eq:<module>-<nom>` pour chaque équation retenue, avec son statut et sa provenance (`docs/specification/CONVENTIONS.md` § 2).
- **Paramètres** : liste (nom dans le code, valeur, unité, source) à porter dans la table de calibration.
- **Interfaces** : variables lues et rendues, flux proposés au noyau ; ce que les blocs voisins doivent fournir.
- **Tests attendus** : propriétés (signe, délai, ordre de grandeur), pas de valeurs à reproduire ; identités à vérifier.
- **Surface de spécification** : sections du plan fixe touchées.
- **Issues** : titres proposés pour la spécification (`docwriter`) et l'implémentation (`coder`).

## 10. Historique de la fiche

| Date | Événement | Auteur |
|---|---|---|
| | Ouverture (issue #n) | |
| | Instruction déposée | expert pilote |
| | Avis de `jeu` | `jeu` |
| | Décision M-n | mainteneur |
