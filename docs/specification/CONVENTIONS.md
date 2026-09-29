# Conventions de la spécification v3

Règles obligatoires pour écrire et modifier `docs/specification/nations_et_marches.tex`, la spécification de *Nations & Marchés* (moteur v3). Elles s'imposent à `docwriter`, seul agent qui écrit dans `docs/specification/`, et à toute session qui y touche. Elles mettent en œuvre `docs/exigences.md` § 3 (exigences documentaires) et s'inspirent des conventions LaTeX du dépôt public `Gerard-Garey/outil_usp` (`docs/latex/CONVENTIONS.md`), adaptées à un document de conception économique compilé en XeLaTeX.

Ce fichier est tenu par `architect`. Une convention ne change que par une mise à jour datée de ce fichier, renvoyant à l'ADR ou à la décision du mainteneur qui la motive. Le vocabulaire est celui de `CONTEXT.md`.

Trois choses priment, dans cet ordre (`docs/exigences.md` § 1.2) :
1. la **concordance exacte** entre la spécification et le moteur : toute équation active est documentée, toute équation documentée est exécutée ;
2. la **reproductibilité** : un chiffre du document se remesure ;
3. la **lisibilité** pour un lecteur qui n'a pas accès au code, joueur compris.

## 1. Structure : le plan fixe

### 1.1 Plan du document

Le document est un **fichier unique**, `nations_et_marches.tex`, dans la forme de la spécification v1.5 (`archive/v1.5/Nations_et_Marches_v1_5.tex`) : classe `article`, encadrés `tcolorbox`, tables `longtable`. Le plan ci-dessous est fixe : l'ordre des sections et leurs titres ne changent pas d'une version à l'autre ; une section s'ajoute à l'emplacement réservé, ne se déplace pas. Chaque section porte un label `sec:<nom>`.

| Ordre | Section | Label | Contenu | Jalon |
|---|---|---|---|---|
| — | Page de titre, résumé, table des matières | — | Version, date, périmètre exécuté | J1 |
| 0 | **Ce qui change en v3.x** (une table par version, la plus récente en tête) | `sec:changements-v3x` | Modification, section touchée, ce que le moteur ou l'audit a révélé (§ 4.4) | J1 |
| 1 | Objet, principes et lecture du document | `sec:objet` | Les cinq principes de conception (`docs/exigences.md` § 2.1) ; comment lire une équation et son encadré ; les trois statuts épistémiques | J1 |
| 2 | Cadre : temps, entités, comptabilité | `sec:cadre` | Entités et indices ; convention calendaire ; matrice des bilans et **matrice des flux de transactions sous forme de tableau** ; identités et tolérances ; règles de caisse ; ordre des phases d'un pas | J1 |
| 3 à 10 | **Un bloc par section**, dans l'ordre de l'inventaire `docs/blocs/README.md` : production et stocks ; travail et salaires ; prix ; ménages ; investissement et financement des entreprises ; banque commerciale ; banque centrale et anticipations ; État et dette | `sec:<bloc>` (même radical que les labels d'équation, § 2.1) | Équations avec encadré « Lecture », statut, provenance, paramètres | J1 |
| 11 | Leviers du joueur (socle) | `sec:leviers` | Catalogue des leviers de l'économie fermée : levier, type, unité, délai, contrepartie comptable | J1, J4 |
| 12 | État stationnaire résolu et calibration | `sec:calibration` | Table de calibration (§ 4.3) ; état stationnaire recalculable à la main ; test zéro et ses bandes, écrites avant l'essai | J1, J3 |
| 13 | Validation : tests, propriétés, faits mesurés | `sec:validation` | Ce que le moteur produit, avec la commande qui le produit ; distinction produit / établi / contesté | J3 |
| 14 | *Réservé* : économie ouverte et régimes de souveraineté | `sec:ouverture` | Commerce, change, balance des paiements, régimes A à E | J5 |
| 15 | *Réservé* : actifs et crises financières | `sec:crises` | Actifs, ruées, défaut, hyperinflation, économie effondrée | J6 |
| 16 | *Réservé* : systèmes économiques, soutien politique, jeu | `sec:jeu` | Planification, nationalisation, score, conditions de fin | J7 |
| 17 | Pistes écartées | `sec:ecartees` | Reprises de `docs/exigences.md` § 2.8, puis complétées par les fiches comparatives | J1 |
| 18 | État des chantiers ouverts | `sec:chantiers` | Ce qui a été essayé et pourquoi cela a échoué (§ 4.4) | J1 |
| A | Correspondance équations ↔ code | `sec:correspondance` | Table label ↔ module et fonction, générée ou vérifiée par le script de concordance | J1 |
| B | Glossaire de la notation | `sec:glossaire` | Table des symboles (§ 5.3) | J1 |

Les sections *réservées* figurent dans le squelette avec une phrase qui dit leur jalon ; elles ne contiennent aucune équation avant la décision du mainteneur qui les ouvre. L'ordre « pistes écartées » puis « chantiers » suit celui de la v1.5 (§ 17–18 de la v1.5), qui plaçait la feuille de route dans le document : la feuille de route de la v3 est hors document (`docs/feuille-de-route.md`) et n'y est pas reproduite.

### 1.2 Structure d'une section de bloc

Chaque section de bloc (3 à 10) suit le même déroulé :
1. **Rôle du bloc** : ce qu'il lit (état d'ouverture), ce qu'il rend (flux proposés, variables nouvelles), les blocs avec lesquels il partage une frontière ;
2. **Équations**, chacune avec son gabarit (§ 2) ;
3. **Paramètres du bloc** : renvoi à la table de calibration, jamais une seconde table ;
4. **Leviers** qui touchent le bloc : encadré `joueur` (hérité de la v1.5), renvoi au catalogue ;
5. **Ce que le moteur ne fait pas** : encadré de portée, où les simplifications assumées sont nommées.

### 1.3 Renvois

- Tout renvoi passe par `\ref`, `\eqref` ou `\autoref` sur un label nommé : **aucun numéro d'équation, de section, de table ou de page écrit en dur**. La v1.5 en contenait (« (41) et (43) ») et ils ont survécu à une renumérotation ; c'est l'un des défauts relevés dans son inventaire.
- Seule exception : la **citation d'un document archivé et figé** (v1.5, v2.0), dont les numéros ne bougent plus : on écrit « v1.5, éq. (35), § 8.1 ». Ces citations ne renvoient jamais à une équation du présent document.
- Familles de labels : `eq:` (équations, § 2.1), `sec:` (sections), `tab:` (tables), `fig:` (figures). Minuscules ASCII, mots séparés par un tiret.
- Un label ne se renomme pas. Si une équation est retirée, son label disparaît du document et sa balise du code dans le **même commit**, et la table « Ce qui change » le consigne.

## 2. Gabarit d'équation

### 2.1 Label

Chaque équation numérotée porte un label `eq:<bloc>-<nom>` :
- `<bloc>` est le radical du module de `src/nations/blocs/` visé par l'inventaire `docs/blocs/README.md` (`production`, `travail`, `prix`, `menages`, `investissement`, `banque`, `banque_centrale`, `finances_publiques`) ; pour les identités comptables du cadre, `noyau` ; pour l'ordonnanceur et le calendrier, `moteur` ;
- `<nom>` décrit ce que l'équation détermine (`eq:prix-cout-unitaire`, `eq:menages-consommation`, `eq:banque_centrale-regle-taux`) ;
- minuscules ASCII, chiffres admis, mots séparés par un tiret ; le tiret bas n'apparaît que dans le radical du module. Expression régulière du script de concordance : `eq:[a-z][a-z0-9_]*-[a-z0-9]+(-[a-z0-9]+)*`.

Une équation qui ne porte pas de label n'est pas numérotée (`equation*`) : c'est un rappel, une définition intermédiaire ou une dérivation, jamais une règle exécutée par le moteur. Dans la v1.5, 18 équations numérotées sur 65 n'avaient pas de label : cette situation est interdite ici.

### 2.2 Balise de code

Le moteur porte, pour chaque label, **exactement une** balise de commentaire `# eq:<bloc>-<nom>` dans `src/`, sur la ligne qui précède l'instruction où l'équation est calculée. Réciproquement, chaque balise du code a son label dans la spécification. Le script `outils/concordance_spec_moteur.py --strict` le vérifie en CI (`docs/exigences.md` § 3.3) ; un écart relevé en cours de branche se corrige aussitôt par un commit `docs:` minimal (règle 9 de `CLAUDE.md`).

Une équation qui se calcule en plusieurs endroits du code est un défaut de code (localité), pas un motif de dédoubler la balise. Une équation de la spécification que le moteur n'exécute pas encore ne porte pas de label `eq:` : elle est présentée dans une section **proposée** (§ 4.1).

### 2.3 Forme LaTeX

```latex
\begin{equation}\label{eq:prix-cout-unitaire}
  c^u_{j,t} = \frac{W_{j,t}\,(1+\tau_S)\,L_{j,t} + \sum_k p_{k,t}\,X_{kj,t}}{Y_{j,t}}
\end{equation}
\begin{lecture}[coût unitaire de production]
\variables $c^u_{j,t}$ : coût unitaire du secteur $j$ au pas $t$, en unités monétaires par unité de bien ; $W_{j,t}$ : salaire nominal par pas ; …
\sens Le coût unitaire additionne le coût du travail chargé et le coût des intrants, rapportés à la production du pas.
\hyp Rendements constants sur le pas ; intrants payés au prix du pas courant.
\limites Ne comprend ni le coût du capital ni les impôts sur la production, portés par la marge (\eqref{eq:prix-marge}).
\tracabilite{dérivée}{v1.5, éq. (21), § 6.2 ; retenue par la décision M-n}{nations.blocs.prix.cout_unitaire}
\end{lecture}
```

L'encadré **« Lecture »** est l'environnement `lecture` de la v1.5, en **quatre rubriques, dans cet ordre, toutes présentes** :
1. `\variables` : chaque symbole de l'équation, avec sa définition, son **unité**, son **dénominateur** s'il s'agit d'un ratio, et sa **fenêtre** (ouverture ou clôture du pas, moyenne mobile et sa longueur) ;
2. `\sens` (« Ce que dit l'équation ») : en langage courant, lisible par un joueur ;
3. `\hyp` : ce que l'équation suppose ;
4. `\limites` : ce qu'elle ne fait pas, les cas où elle est fausse, les bornes qui s'y appliquent.

L'encadré se termine par une **ligne de traçabilité** obligatoire, `\tracabilite{<statut>}{<provenance>}{<objet du code>}`. Ce n'est pas une cinquième rubrique de lecture ; c'est le lien avec `docs/exigences.md` § 2.4 et § 3.2 :
- **statut** : `dérivée`, `approchée` ou `choix de conception`, sans autre valeur ;
- **provenance** : `v1.5, éq. (n), § x.y` ; `v2.0, \code{archive/v2.0/…}` avec la fonction ; ou `nouvelle : <référence retrouvée>` ; suivie de la **décision du mainteneur** qui l'a retenue (`décision M-n`, `docs/feuille-de-route.md`) et du renvoi à la fiche comparative du bloc ;
- **objet du code** : nom qualifié du module ou de la fonction qui porte la balise, vérifié par le script de concordance (§ 5.4).

Une équation dont le statut est « choix de conception » ne cite aucune référence théorique à son appui ; une équation « dérivée » dit de quel problème ou de quelle identité elle dérive, et où la dérivation est donnée (dans le document, ou dans le cours au jalon J8). La v1.5 encadrait déjà deux équations « choix de conception, pas résultat théorique » (v1.5, éq. (41) et (43)) : c'est cet usage qui est généralisé.

### 2.4 Paramètres

Chaque paramètre d'une équation figure **une fois** dans la table de calibration (`sec:calibration`, `tab:calibration`), avec : symbole, nom du paramètre dans le code (`\code{…}`), valeur, unité, source (référence retrouvée, fait mesuré avec sa commande, ou « choix de conception »), et label de l'équation qui l'emploie. Un paramètre retiré sort de la table et du glossaire dans le même commit que l'équation qui l'employait ; la v1.5 en gardait quatre en usage après retrait (s₇, s₅, λ₂, θ₆).

Toute **borne** (plancher, plafond, saturation, `clip`) est un paramètre déclaré, présent dans la table et dans les `\limites` de l'équation bornée ; le document dit pourquoi un mécanisme n'a pas été préféré à la borne (`docs/exigences.md` § 2.7).

## 3. Préambule

- Le préambule est celui de la v1.5 (lignes 1 à 57 de `archive/v1.5/Nations_et_Marches_v1_5.tex`, tout ce qui précède `\title`, ligne 58), **recopié tel quel et intouché** ; le titre, le sous-titre et la date (lignes 58 à 62 de la v1.5) sont propres à chaque version et portent « version 3.x » et le périmètre exécuté : `\documentclass[11pt,a4paper]{article}`, `fontspec` avec Latin Modern, `polyglossia` en français, `amsmath`, `tcolorbox`, `longtable`, `hyperref`, `tikz`, les environnements `lecture`, `design`, `lit`, `joueur`, `vic`, les macros `\variables`, `\sens`, `\hyp`, `\limites`, `\pos`, `\clip`, `\ind`, `\og`, `\fg`.
- Les ajouts propres à la v3 sont regroupés **après** ce préambule, dans un bloc délimité par les commentaires `% ---- Compléments v3 : début ----` et `% ---- Compléments v3 : fin ----`. Au squelette, ce bloc contient au moins :
  - `\newcommand{\code}[1]{\texttt{\detokenize{#1}}}` : cite un objet du code (§ 5.4) ; `\detokenize` permet d'écrire l'identifiant exactement comme dans le code, tiret bas compris, ce que le script relit ;
  - `\newcommand{\tracabilite}[3]{…}` : ligne de traçabilité (§ 2.3) ;
  - un environnement `proposee` (tcolorbox) pour les sections proposées (§ 4.1) ;
  - un environnement `portee` (tcolorbox) pour les encadrés « ce que le moteur ne fait pas ».
- Le bloc de compléments ne change que sur mise à jour de ce fichier ; `docwriter` n'y ajoute rien de sa propre initiative. Aucun paquet n'est retiré du préambule v1.5 même s'il semble inutilisé (`tikz` sert aux figures de bilans).
- La compilation est **XeLaTeX** ; le document ne doit dépendre d'aucun paquet absent de MiKTeX (poste local) ou de TeX Live avec `texlive-xetex`, `texlive-lang-french`, `texlive-latex-extra`, `texlive-fonts-recommended` et `fonts-lmodern` (session cloud). Le préambule v1.5 gère déjà l'absence de `dsfont`.

## 4. Contenu : invariants

### 4.1 Le document décrit le moteur exécuté

- Une équation numérotée est une équation **exécutée** par `src/nations/`, dans la configuration de référence, avec les coefficients de la table de calibration. Avant d'écrire qu'un mécanisme agit, vérifier qu'il est actif (`CLAUDE.md`, « Rigueur »).
- Un mécanisme décidé par le mainteneur mais pas encore codé s'écrit dans un encadré `proposee`, sans label `eq:`, avec le numéro de la décision M-n et l'issue qui le réalisera. L'encadré disparaît quand le code arrive et que l'équation reçoit son label.
- Un mécanisme non décidé n'entre pas dans le document : il reste dans la fiche comparative (`docs/blocs/`).

### 4.2 Statuts épistémiques et chiffres

- Trois choses ne se confondent jamais (`docs/exigences.md` § 2.4) : ce que le **modèle produit** (se recalcule, ne porte pas de source, cite la commande qui le produit) ; ce qui est **établi** (source et date) ; ce qui est **contesté** (les positions sont nommées). Un résultat du modèle n'est jamais présenté comme un fait empirique.
- Un **chiffre ne se recopie pas, il se remesure** : tout chiffre issu du moteur est accompagné, dans le document ou dans la section de validation, de la commande `uv run …` qui le produit et du commit ; le compte rendu de `docwriter` dit comment il l'a remesuré. Un chiffre qui vient d'une source se vérifie contre elle.
- Une **grandeur** porte sa définition, son unité, son dénominateur et sa fenêtre, dans les tableaux comme dans les critères. Un ratio de stock dit sur quel PIB (annuel, nominal, courant) il est rapporté ; un taux dit s'il est annualisé ; une moyenne dit sa longueur.
- Un **critère** (bande du test zéro, seuil d'un test de mécanisme) s'écrit avant l'essai et ne se déplace pas après observation ; une correction de critère mal posé est prospective et l'ancien verdict reste publié dans la section de validation.
- Toute **référence** est une publication retrouvée, citée avec auteur, année, titre ; aucune page ni formule n'est inventée. Quand la littérature ne permet pas de conclure, le document l'écrit.

### 4.3 Conservation

- Aucun développement, justification, mesure ou référence n'est supprimé sans raison. Quand un passage est retiré parce qu'il est faux, le compte rendu de `docwriter` le cite intégralement, avec ce qui le remplace et pourquoi ; la table « Ce qui change » en garde la trace.
- Un passage correct reste tel quel : la mission de `docwriter` est d'élever la précision dans le plan existant, pas de réorganiser.
- La **liste des instabilités connues** de la première tentative (synthèse des faits mesurés d'`archive/`) est reprise dans `sec:chantiers` dès le squelette et tenue à jour : une instabilité ne se réintroduit pas sans fait nouveau et test (`docs/exigences.md` § 2.8).

### 4.4 Tables de version et chantiers

- Chaque version commence par une table **« Ce qui change en v3.x »** (colonnes fixes : numéro, modification, section touchée, ce que le moteur ou l'audit a révélé), la plus récente en tête, celles des versions antérieures conservées à la suite.
- Chaque version se termine par l'**état des chantiers ouverts**, table à colonnes fixes (version d'ouverture, chantier, état : ouvert / partiel / clos, ce qui a été essayé et pourquoi cela a échoué). Un chantier clos reste dans la table.
- Les **décomptes** (nombre d'équations, de paramètres, de tests, de labels) ne s'écrivent pas en toutes lettres dans la prose : ils se lisent dans les tables et sont vérifiés par le script de concordance. La v1.5 affichait quatre totaux de tests discordants (26, 36, 37, 43).

## 5. Typographie et notations

### 5.1 Langue et typographie

- Français avec accents, y compris dans les titres, les commentaires LaTeX et les labels de figures. Guillemets français par `\og` et `\fg` (macros du préambule v1.5) ; `polyglossia` place les espaces insécables des signes doubles.
- Virgule décimale en mode mathématique : `0{,}05`, jamais `0.05`. Pourcentage : `5\,\%`. Points : « pt » pour un point de pourcentage, « pb » pour un point de base, toujours en toutes lettres à la première occurrence d'une section.
- Unités et fenêtres écrites après la valeur : « 0,02 par an », « 2 semaines de ventes », « ratio au PIB annuel nominal ».
- Les noms de blocs, de phases et de leviers sont ceux de `CONTEXT.md`, tels quels.
- Aucun nom de pays réel : les configurations sont des archétypes anonymisés (`docs/exigences.md` § 2.9).

### 5.2 Notations

- **Un symbole a un seul sens dans tout le document**, et un sens a un seul symbole. La v1.5 employait λ₀, λ₁, ϖ, ς et ω dans plusieurs sens : chaque réemploi est proscrit et se résout par un indice distinctif.
- Indices fixes : pays $i$, secteur $j$ (et $k$ pour un intrant), strate de ménages $h$, pas $t$. Un indice n'est jamais réutilisé pour autre chose.
- Convention temporelle : $x_t$ est la valeur **d'ouverture** du pas $t$ et $x_{t+1}$ celle de clôture, sauf mention explicite dans `\variables`. Une variable de flux est datée du pas où le flux s'exécute.
- **Taux** : toujours exprimés en base annuelle dans le document ; la conversion au pas est donnée une fois, dans `sec:cadre`, par une équation labellisée `eq:moteur-conversion-taux`, et n'est jamais recalculée localement.
- Opérateurs du préambule : `\pos{x}` pour la partie positive, `\clip{x}{a}{b}` pour une borne, `\ind` pour l'indicatrice, `\E` pour l'espérance, `\sgn` pour le signe.
- Une variable **anticipée** porte l'exposant $e$ ($\pi^e_t$), une **cible** l'exposant $\ast$ ($\pi^\ast$), une valeur de **long terme ou stationnaire** une barre ($\bar q$). Ces trois marques ne se cumulent qu'avec explication.

### 5.3 Table des symboles

Le glossaire de la notation (`sec:glossaire`, `tab:symboles`) est le **registre** des symboles : tout symbole employé dans une équation y figure, avec définition, unité, bloc, et label de l'équation qui le définit ; tout symbole qui y figure est employé. `docwriter` le parcourt à chaque passage (surface d'impact, entrée 9). Un symbole y entre dans le même commit que l'équation qui l'introduit.

### 5.4 Citer le code : `\code{…}`

- Un objet du code se cite par `\code{nom.qualifie}` : un module (`\code{nations.blocs.prix}`), une fonction ou une classe (`\code{nations.blocs.prix.cout_unitaire}`), un paramètre (`\code{nations.moteur.parametres.taux_marge}`), un script (`\code{outils/concordance_spec_moteur.py}`). Le nom est écrit exactement comme dans le code ; `\detokenize` évite d'échapper les tirets bas.
- Le script de concordance vérifie que chaque nom cité **existe** dans `src/` ou `outils/` (analyse statique, sans import), et que chaque troisième argument de `\tracabilite` désigne l'objet qui porte la balise du label correspondant.
- Un nom qui n'existe plus est un écart bloquant en CI : la citation se corrige dans le commit `docs:` minimal.
- La prose n'emploie jamais un nom de code sans `\code{}` ; réciproquement, `\code{}` ne sert pas à la mise en valeur d'autre chose (mot anglais, terme du jeu).

## 6. Convention calendaire : question ouverte

La convention calendaire n'est **pas tranchée**. Elle relève de la fiche comparative « temps et comptabilité » (`docs/blocs/temps_comptabilite.md`), première à instruire, et de la décision M-n du mainteneur qui la clora. Jusqu'à cette décision :

- le document emploie les termes de `CONTEXT.md` (**pas**, **date de décision**, **tour**) sans leur attacher de durée ;
- aucun coefficient « par semaine » ou « par mois » n'est écrit ; les paramètres de vitesse sont exprimés **par an** et convertis par `eq:moteur-conversion-taux` une fois la durée du pas fixée.

L'inventaire de la v1.5 (annexe A de la passation du 29/09/2026) relève une **incohérence interne** que la fiche devra lever :
- v1.5 § 3.4 « Temps » : le tick est une semaine, le mois compte 4 ticks, les taux sont convertis par $(1+i)^{1/52}-1$ ;
- 4 ticks × 12 mois = 48 ticks, alors que la conversion des taux, les moyennes mobiles d'un an ($\lambda_q = 1/52$) et le glissement de l'indice des prix supposent 52 ; le document ne dit pas comment l'année de 52 semaines se répartit en 12 mois de 4 ;
- le moteur v2.0 prend 13 dates de décision par an (`DECISION_WEEKS = 4`, 52/4), soit un « mois » qui n'en est pas un.

Options que la fiche devra au moins comparer, sans que ce fichier en préfère aucune : pas mensuel unique (12 pas par an, décisions à chaque pas) ; pas hebdomadaire avec 52 pas et 13 dates de décision de 4 semaines ; pas hebdomadaire avec mois calendaires de 4 ou 5 semaines. Le budget de calcul est fixé par pays-semaine (`CLAUDE.md`) : la fiche dira comment il se lit si le pas est mensuel. Le tour du jeu est mensuel (décision du mainteneur du 29/09/2026), ce qui contraint le rapport entre pas et tour, pas la durée du pas.

## 7. PDF versionné et compilation

- Le PDF `docs/specification/nations_et_marches.pdf` est **versionné** et recompilé à chaque modification du `.tex`, dans le **même commit** `docs:`. Un `.tex` modifié sans son PDF est un commit incomplet.
- Compilation : XeLaTeX, trois passes au moins, jusqu'à disparition de « Rerun to get cross-references right » dans le journal. La procédure sera fixée par la skill `compiler-doc` (`.claude/skills/compiler-doc/SKILL.md`), à créer sur le modèle d'`outil_usp` : elle n'existe pas encore dans ce dépôt.
- Contrôles du journal, comparés à l'état d'avant la modification : aucune ligne commençant par `!` ; aucune occurrence de `undefined` (renvoi ou citation) ; les `Overfull` et `Underfull` nouveaux sont listés dans le compte rendu ; nombre de pages et table des matières comparés.
- Chaîne de composition nommée dans le compte rendu : MiKTeX sur le poste local, TeX Live en session cloud.
- Les fichiers auxiliaires (`.aux`, `.log`, `.out`, `.toc`) ne sont pas versionnés.

## 8. Manière de modifier

- Les modifications sont **ciblées** : on corrige le passage, pas le chapitre. Un diff lisible vaut mieux qu'une réécriture.
- Avant de modifier un passage, relever **ce qu'il affirme** et **ce qui y renvoie** (labels, tables de synthèse, glossaire, table de calibration, table de correspondance), puis parcourir la surface d'impact de la fiche `docwriter` entrée par entrée.
- `docwriter` intervient **une fois par branche, en fin de branche**, à partir des surfaces d'impact listées par `coder` dans ses commits (règle 9 de `CLAUDE.md`), avec un commit `docs:` par issue. Exceptions : commit préparatoire, document qui porte la décision et précède le code (jalon J1), écart de concordance en CI.
- Une question de fond (deux lectures possibles, équation douteuse) va à l'expert pilote du bloc, désigné par `docs/blocs/README.md` ; elle ne se tranche pas par la rédaction.
- Une modification qui change ce que le moteur calcule passe d'abord par le code et son visa (`CLAUDE.md`, « Changements de résultats ») ; la spécification suit, elle ne précède pas, sauf section proposée (§ 4.1).

## 9. Ce que vérifie le script de concordance

Contrat attendu d'`outils/concordance_spec_moteur.py --strict` (mis en place par l'issue #4 ; le détail de mise en œuvre revient à `coder`) :

1. l'ensemble des `\label{eq:…}` du `.tex` et l'ensemble des balises `# eq:…` de `src/` sont égaux, chaque élément apparaissant exactement une fois de chaque côté ;
2. chaque label respecte l'expression régulière du § 2.1 et son radical de bloc est un module de `src/nations/blocs/` (ou `noyau`, `moteur`) ;
3. chaque équation numérotée (`\begin{equation}` sans étoile) porte un label ; chaque environnement `lecture` contient `\variables`, `\sens`, `\hyp`, `\limites` puis `\tracabilite`, dans cet ordre ;
4. le premier argument de `\tracabilite` est l'un des trois statuts ; le deuxième cite une décision `M-` ;
5. chaque `\code{…}` désigne un objet existant de `src/` ou `outils/` ; le troisième argument de `\tracabilite` désigne le module ou la fonction qui contient la balise du label ;
6. aucun numéro d'équation en dur : motif `\(\d+\)` hors des citations « v1.5, éq. (n) » et « v2.0 » ;
7. tout paramètre de la table de calibration cité par `\code{}` existe dans `src/nations/moteur/` ; tout symbole du glossaire est employé dans au moins une équation, et réciproquement (quand la table est balisée pour le permettre).

Un contrôle mécanique récurrent qui n'est pas dans cette liste appelle une issue, pas un agent (principe 7 des workflows).

## Historique des conventions

| Date | Modification | Motif |
|---|---|---|
| 2026-09-29 | Création (issue #6, branche `claude/fondations`) | Jalon J0 ; préparation de la spécification du socle (J1) |
