# Conventions de la spécification v3

Règles obligatoires pour écrire et modifier `docs/specification/nations_et_marches.tex`, la spécification de *Nations & Marchés* (moteur v3). Elles s'imposent à `docwriter`, seul agent qui écrit dans `docs/specification/`, et à toute session qui y touche. Elles mettent en œuvre `docs/exigences.md` § 3 (exigences documentaires) et s'inspirent des conventions LaTeX du dépôt public `Gerard-Garey/outil_usp` (`docs/latex/CONVENTIONS.md`), adaptées à un document de conception économique compilé en XeLaTeX.

Ce fichier est tenu par `docwriter` (décision du mainteneur du 30/09/2026). Une convention ne change que par une mise à jour datée de ce fichier, renvoyant à l'ADR ou à la décision du mainteneur qui la motive. Le vocabulaire est celui de `CONTEXT.md`.

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
- Seule exception : la **citation d'un document archivé et figé** (v1.5, v2.0), dont les numéros ne bougent plus : on écrit « v1.5, éq. (35), § 8.1 ». Forme exacte reconnue par le script (§ 9, règle 6) : `v1.5` ou `v2.0`, virgule, `éq.` ou `éqs.`, puis le numéro entre parenthèses ; espace ordinaire ou `~` admis entre ces éléments ; des numéros supplémentaires s'ajoutent par « , » ou « et » (« v1.5, éqs. (41) et (43) »). Une mention d'un document archivé hors de cette forme est relevée, comme tout numéro entre parenthèses en dehors des exemptions du § 9, règle 6. Ces citations ne renvoient jamais à une équation du présent document.
- Une énumération dans la prose s'écrit avec `enumerate`, jamais par des numéros entre parenthèses « (1) », « (2) » : le script les relèverait comme des numéros en dur.
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

Le moteur porte, pour chaque label, **exactement une** balise de commentaire `# eq:<bloc>-<nom>` dans `src/`, **seule sur sa ligne**, la ligne qui précède l'instruction où l'équation est calculée. Réciproquement, chaque balise du code a son label dans la spécification. Le script `outils/concordance_spec_moteur.py --strict` le vérifie en CI (`docs/exigences.md` § 3.3) ; un écart relevé en cours de branche se corrige aussitôt par un commit `docs:` minimal (règle 9 de `CLAUDE.md`).

Ce que le script tient pour une balise : tout commentaire Python qui commence par un ou plusieurs `#`, des espaces facultatifs, puis `eq:` (motif `^#+\s*eq:`). Chaque commentaire de cette forme compte pour l'unicité : une équation mentionnée dans un second commentaire `# eq:…` (rappel, explication) crée un doublon et un écart ; un commentaire qui ne commence pas par `eq:` après les `#` n'est pas une balise (`# voir eq:prix-marge` évoque l'équation sans la baliser). Une balise placée en fin d'une ligne de code (`x = … # eq:…`) est un écart : elle va seule sur la ligne précédente.

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
\tracabilite{dérivée}{v1.5, éq. (21), § 6.2 ; retenue par la décision Mn}{nations.blocs.prix.cout_unitaire}
\end{lecture}
```

(`Mn` tient ici la place du numéro de la décision, par exemple `M16` ; notation au § 2.3, « provenance ».)

Chaque équation numérotée qui porte un label est **immédiatement suivie** de son encadré `lecture`, avant l'équation numérotée suivante (§ 9, règle 8) ; un environnement multiligne (`align`…) qui porte plusieurs labels est suivi d'un encadré par label, ou d'un encadré unique qui les commente tous, mais jamais d'une autre équation numérotée avant le premier encadré.

L'encadré **« Lecture »** est l'environnement `lecture` de la v1.5, en **quatre rubriques, dans cet ordre, toutes présentes** :
1. `\variables` : chaque symbole de l'équation, avec sa définition, son **unité**, son **dénominateur** s'il s'agit d'un ratio, et sa **fenêtre** (ouverture ou clôture du pas, moyenne mobile et sa longueur) ;
2. `\sens` (« Ce que dit l'équation ») : en langage courant, lisible par un joueur ;
3. `\hyp` : ce que l'équation suppose ;
4. `\limites` : ce qu'elle ne fait pas, les cas où elle est fausse, les bornes qui s'y appliquent.

L'encadré se termine par une **ligne de traçabilité** obligatoire, `\tracabilite{<statut>}{<provenance>}{<objet du code>}`. Ce n'est pas une cinquième rubrique de lecture ; c'est le lien avec `docs/exigences.md` § 2.4 et § 3.2 :
- **statut** : `dérivée`, `approchée` ou `choix de conception`, sans autre valeur ;
- **provenance** : `v1.5, éq. (n), § x.y` ; pour la v2.0, le chemin du fichier sous `archive/v2.0/` et la fonction, écrits en `\texttt{}` (jamais en `\code{}`, réservé aux objets de `src/` et `outils/`, § 5.4), ou la forme « v2.0, éq. (n) » du § 1.3 quand la pièce archivée numérote l'équation citée ; ou `nouvelle : <référence retrouvée>` ; suivie de la **décision du mainteneur** qui l'a retenue et du renvoi à la fiche comparative du bloc. La décision s'écrit sous sa **forme canonique `Mn`** (`M16`, comme dans `docs/feuille-de-route.md` et les ADR) ; « M-n » n'est que la désignation générique d'une décision quelconque dans la prose de ce fichier et des fiches. Le script reconnaît les deux graphies (§ 9, règle 4) ;
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
- La compilation est **XeLaTeX** ; le document ne doit dépendre d'aucun paquet absent de MiKTeX (poste local) ou de TeX Live tel qu'installé en CI et en session cloud, c'est-à-dire des paquets `texlive-xetex`, `texlive-lang-french`, `texlive-latex-recommended`, `texlive-latex-extra`, `texlive-pictures`, `texlive-fonts-recommended` et `fonts-lmodern`. Cette liste est celle du job « Compilation de la spécification » de `.github/workflows/ci.yml` et de la variable `PAQUETS_TEXLIVE` du hook `.claude/hooks/preparer_latex.sh` ; les trois se tiennent identiques. Le préambule v1.5 gère déjà l'absence de `dsfont` (`texlive-fonts-extra`, non installé).

## 4. Contenu : invariants

### 4.1 Le document décrit le moteur exécuté

- Une équation numérotée est une équation **exécutée** par `src/nations/`, dans la configuration de référence, avec les coefficients de la table de calibration. Avant d'écrire qu'un mécanisme agit, vérifier qu'il est actif (`CLAUDE.md`, « Rigueur »).
- Un mécanisme décidé par le mainteneur mais pas encore codé s'écrit dans un encadré `proposee`, sans label `eq:`, avec le numéro de la décision (`Mn`, § 2.3) et l'issue qui le réalisera. L'encadré disparaît quand le code arrive et que l'équation reçoit son label.
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

## 6. Convention calendaire : tranchée (M22)

La convention calendaire est **tranchée** par la décision M22 du mainteneur (30/09/2026), consignée dans l'ADR 0005 (`docs/adr/0005-calendrier-et-cadre-comptable.md`) sur la fiche comparative « temps et comptabilité » (`docs/blocs/temps_comptabilite.md`, § 8). Elle est écrite dans `sec:cadre` de la spécification, sous-section « Calendrier et règle de conversion », en section proposée (§ 4.1) jusqu'au jalon J2. Pour la rédaction du document :

- le **pas** est un mois simulé : n_a = 12 pas par an, n_m = 1 pas par tour ; tout pas est une **date de décision** ; le **tour** n est le pas n − 1 et s'affiche en (année, mois) ; les termes sont ceux de `CONTEXT.md` ;
- taux, flux annuels et vitesses d'ajustement s'écrivent **par an** et se convertissent au pas par la seule **règle linéaire** x/n_a, `eq:moteur-conversion-taux` (label posé au J2, avec sa balise) ; aucun coefficient « par semaine » ni « par mois » n'est écrit ailleurs, et une fenêtre « d'un an » vaut exactement n_a pas ;
- dans la matrice des flux, un intérêt ou un amortissement s'écrit taux annuel × encours d'ouverture / n_a (`$i_L L/n_a$`, `$\delta K/n_a$`) : c'est la règle de conversion appliquée, non une seconde conversion ; un tel produit reste un terme simple au sens du § 9 ;
- toute vitesse d'ajustement annuelle λ respecte λ ≤ n_a ; les deux grandeurs qui dépendent de n_a (fraction annuelle résorbée par une vitesse, rendement d'un encours dont l'intérêt est crédité dans l'instrument) sont chiffrées dans `sec:cadre`.

L'incohérence que ce paragraphe relevait avant la décision est levée : v1.5 § 3.4 « Temps », tick hebdomadaire, mois de 4 ticks et conversion par $(1+i)^{1/52}-1$, soit 48 ticks par an selon le calendrier contre 52 selon la conversion ; moteur v2.0, 13 dates de décision par an (`DECISION_WEEKS = 4`). Elle est consignée dans l'ADR 0005 (§ Contexte) et, avec les autres options écartées (pas hebdomadaire à 13 dates de 4 semaines, pas hebdomadaire à mois de 4 ou 5 semaines), dans `sec:ecartees`. Le budget de calcul, fixé par pays-semaine (M13), se lit 52/12 ms par pays-pas. Changer n_a, n_m ou la règle de conversion demande une décision M-m citant M22.

## 7. PDF versionné et compilation

- Le PDF `docs/specification/nations_et_marches.pdf` est **versionné** et recompilé à chaque modification du `.tex`, dans le **même commit** `docs:`. Un `.tex` modifié sans son PDF est un commit incomplet.
- La procédure de compilation est **portée par le script `outils/compiler_specification.sh`** (`bash outils/compiler_specification.sh [fichier.tex]`, défaut `docs/specification/nations_et_marches.tex`), exécuté par la skill `compiler-doc` (`.claude/skills/compiler-doc/SKILL.md`) sur le poste local et en session cloud, et par le job CI « Compilation de la spécification » (`.github/workflows/ci.yml`). Ni la skill ni la CI ne refont la procédure à la main (principe 7 des workflows). Le script :
  - enchaîne les passes XeLaTeX (`-interaction=nonstopmode -halt-on-error`), **trois au moins, cinq au plus**, jusqu'à disparition de toute demande de relance dans le journal, reconnue par le motif `Rerun to get|Rerun LaTeX` (« Rerun to get cross-references right » de LaTeX, « Table widths have changed. Rerun LaTeX. » de `longtable`) ; si la cinquième passe en demande encore une, un renvoi oscille et le script échoue ;
  - échoue sur toute ligne du journal commençant par `!` et sur toute occurrence de `undefined` (renvoi ou citation indéfini) ;
  - compte et liste les `Overfull` et `Underfull`, sans échouer ;
  - rend 0 si toutes les passes aboutissent (PDF produit) et que le journal final est propre, 1 sinon (et aussi si `xelatex` ou le `.tex` est introuvable) ; il affiche en tête la chaîne de composition (`xelatex --version`).
- Ce que la skill ajoute au script : la comparaison à l'état d'avant la modification (`Overfull` et `Underfull` **nouveaux**, listés dans le compte rendu et corrigés s'ils dépassent 10 pt sur les lignes modifiées ; nombre de pages et table des matières), la chaîne de composition nommée dans le compte rendu (MiKTeX sur le poste local, TeX Live en session cloud), puis la concordance `--strict` et le contrôle que le `.tex` et le `.pdf` sont modifiés ensemble.
- `xelatex` est rendu disponible par le hook `SessionStart` `.claude/hooks/preparer_latex.sh` : MiKTeX ajouté au `PATH` sur le poste local ; en session cloud, rien n'est installé au démarrage, la skill lance `bash .claude/hooks/preparer_latex.sh --installer` (TeX Live par `apt`, paquets du § 3) au moment de compiler.
- Les fichiers auxiliaires (`.aux`, `.log`, `.out`, `.toc`) ne sont pas versionnés.

## 8. Manière de modifier

- Les modifications sont **ciblées** : on corrige le passage, pas le chapitre. Un diff lisible vaut mieux qu'une réécriture.
- Avant de modifier un passage, relever **ce qu'il affirme** et **ce qui y renvoie** (labels, tables de synthèse, glossaire, table de calibration, table de correspondance), puis parcourir la surface d'impact de la fiche `docwriter` entrée par entrée.
- `docwriter` intervient **une fois par branche, en fin de branche**, à partir des surfaces d'impact listées par `coder` dans ses commits (règle 9 de `CLAUDE.md`), avec un commit `docs:` par issue. Exceptions : commit préparatoire, document qui porte la décision et précède le code (jalon J1), écart de concordance en CI.
- Une question de fond (deux lectures possibles, équation douteuse) va à l'expert pilote du bloc, désigné par `docs/blocs/README.md` ; elle ne se tranche pas par la rédaction.
- Une modification qui change ce que le moteur calcule passe d'abord par le code et son visa (`CLAUDE.md`, « Changements de résultats ») ; la spécification suit, elle ne précède pas, sauf section proposée (§ 4.1).

## 9. Ce que vérifie le script de concordance

Contrat d'`outils/concordance_spec_moteur.py --strict` (issue #4) ; le script des matrices, qui le complète, est décrit à la fin de ce paragraphe. Le script relit le `.tex` et le code **sans rien importer** (analyse textuelle du `.tex` ; `tokenize` et `ast` pour le Python de `src/` et `outils/`). Sans `--strict`, il rend compte et sort avec le code 0 ; avec `--strict`, tout écart donne le code 1. Chaque écart est rapporté avec le numéro de la règle ci-dessous, l'emplacement `fichier:ligne` et un message.

**Texte analysé.** Avant l'analyse, le `.tex` est débarrassé de ce qui n'est pas composé, les positions et numéros de ligne étant conservés : environnements `verbatim`, `verbatim*`, `lstlisting` et `comment` ; `\verb|…|` ; commentaires (`%` non échappé jusqu'à la fin de ligne) ; blocs `\iffalse … \fi` (conditions imbriquées comprises). Un label ou un `\code{}` placé dans l'un de ces passages n'est donc pas vu ; un numéro en dur qui s'y trouve n'est pas relevé.

1. **Égalité et unicité.** L'ensemble des `\label{eq:…}` du `.tex` et l'ensemble des balises `# eq:…` de `src/` sont égaux, chaque élément apparaissant exactement une fois de chaque côté. Une balise est un commentaire Python qui vérifie `^#+\s*eq:` (§ 2.2) ; chaque commentaire de cette forme compte pour l'unicité ; une balise en fin de ligne de code est un écart (elle va seule sur la ligne qui précède l'instruction).
2. **Format.** Chaque label, du `.tex` comme du code, respecte l'expression régulière du § 2.1 et son radical de bloc est `noyau`, `moteur` ou un module de `src/nations/blocs/` (fichier `.py` ou paquet).
3. **Équations numérotées et encadrés.** Chaque équation numérotée porte un label ; les environnements contrôlés sont `equation`, `align`, `gather`, `multline`, `flalign`, `alignat` et `eqnarray`, sans étoile. `equation` et `multline` n'ont qu'un numéro, quel que soit le nombre de lignes : ils portent un label, aucun s'ils sont marqués `\nonumber` ou `\notag`. Dans `align`, `gather`, `flalign`, `alignat` et `eqnarray`, **un label par ligne numérotée**. Seuls les `\\` de niveau supérieur séparent les lignes : ceux d'un environnement imbriqué (`cases`, `aligned`, `matrix`, `pmatrix`, `array`…) ou d'un groupe `{…}` ne comptent pas ; une ligne vide (après un `\\` final) ne compte pas ; une ligne portant `\notag` ou `\nonumber` n'est pas numérotée. Le script relève le **manque** de labels (moins de labels que de lignes numérotées), pas leur excès. Un `\label{eq:…}` placé hors de tout environnement contrôlé (dans le texte, ou dans une forme étoilée comme `equation*`) est un écart ; en revanche, un label placé dans un environnement contrôlé mais sur une ligne non numérotée (`equation` marquée `\nonumber`, ligne d'`align` marquée `\notag`), ou un second label dans une `equation`, **n'est pas relevé aujourd'hui** : c'est une faute de rédaction que la relecture doit voir (issue #12 pour l'étendre au script). Chaque environnement `lecture` contient `\variables`, `\sens`, `\hyp`, `\limites` puis `\tracabilite`, une fois chacune et dans cet ordre.
4. **Traçabilité.** Le premier argument de `\tracabilite` est l'un des trois statuts (`dérivée`, `approchée`, `choix de conception`) ; le deuxième cite au moins une décision du mainteneur, sous l'une de deux formes : « décision Mn » (`décision` ou `Décision`, puis espaces ou `~`) ou « (Mn) » entre parenthèses ; la forme canonique `Mn` (`M16`, § 2.3) comme la graphie `M-16` sont acceptées. Chaque numéro ainsi cité doit figurer dans le tableau des décisions de `docs/feuille-de-route.md` (son § 4 ; le script lit les lignes de tableau qui commencent par `| Mn |`) ; une feuille de route absente est un écart. Une mention nue (« agrégat M2 ») n'est pas une décision. Une décision par mention : plusieurs décisions s'écrivent « décision M3, décision M16 » ou « (M3) … (M16) » ; le pluriel « décisions M3 et M16 » et la forme groupée « (M3, M16) » ne sont pas reconnus (aucune décision lue, donc écart), et dans « décision M3 et M16 » seul M3 est lu et vérifié (décision du mainteneur du 30/09/2026).
5. **Objets du code.** Chaque `\code{…}` désigne un objet existant de `src/` ou `outils/` (chemin de fichier ou de dossier sous ces racines, module, ou nom pointé résolu objet par objet : fonction, classe, affectation ou importation de niveau module, corps de classe) ; un `\code{…}` dont l'argument contient `#` n'est pas vérifié. Le troisième argument de `\tracabilite` s'écrit en **nom nu** (la macro l'enveloppe déjà dans `\code` : `\tracabilite{…}{…}{\code{x}}` est un écart) et désigne le module ou la fonction qui porte la balise du label de l'équation que l'encadré commente (la dernière équation numérotée qui le précède, sans autre encadré entre les deux).
6. **Numéros en dur.** Aucun numéro entre parenthèses `\(\d+\)` hors du mode mathématique : `$…$`, `$$…$$`, `\(…\)`, `\[…\]` et les environnements `equation`, `align`, `gather`, `multline`, `flalign`, `alignat`, `eqnarray` et leurs formes étoilées (`$f(2)$` n'est pas un numéro d'équation). Hors du mode mathématique, sont exemptés : une année de 1000 à 2099 (« Godley et Lavoie (2007) ») ; un exposant ou un indice, c'est-à-dire un numéro immédiatement précédé de `^`, `_`, `^{` ou `_{` (`^{(2)}`, `_(3)`), tout autre contexte étant relevé (`\textbf{(3)}` l'est) ; la citation exacte d'une équation archivée, « v1.5, éq. (n) » ou « v2.0, éq. (n) » dans la forme du § 1.3 (`éq.` ou `éqs.`, espace ou `~`, numéros supplémentaires par « , » ou « et »). Une énumération « (1), (2) » est relevée (employer `enumerate`) ; une mention d'archive hors de ce motif est relevée.
7. **Table de calibration et glossaire.** Tout paramètre de la table `tab:calibration` cité par `\code{}` est dans `src/nations/moteur/` (nom qui commence par `nations.moteur.`). Le contrôle du glossaire (tout symbole de `tab:symboles` employé dans au moins une équation, et réciproquement) **n'est pas mis en œuvre** tant que la table des symboles n'est pas balisée pour le permettre ; la sortie du script le signale à chaque exécution (« règle 7, glossaire : non vérifié »). Le baliser et étendre le script relève d'une issue.
8. **Encadré après l'équation.** Chaque équation numérotée qui porte un label `eq:` est suivie de son encadré `lecture`, avant l'équation numérotée suivante (§ 2.3).

La sortie donne aussi les décomptes (labels, balises, équations numérotées, encadrés, `\code`) : ce sont eux, et non la prose, qui portent les totaux (§ 4.4). Un contrôle mécanique récurrent qui n'est pas dans cette liste appelle une issue, pas un agent (principe 7 des workflows).

### Script des matrices

À côté de la concordance, `outils/verifier_matrices.py` (issue #19) vérifie les trois tables du cadre (`sec:cadre`) : `tab:matrice-bilans`, `tab:matrice-flux` et `tab:portes-monnaie`, toutes trois des `longtable`. Son contrat est la convention d'écriture des matrices fixée sur accord du mainteneur le 30/09/2026 (`docs/blocs/temps_comptabilite.md` § 9.7, commit `8fa2614`). Usage : `uv run python outils/verifier_matrices.py [--strict] [fichier.tex]` (défaut : la spécification). Sans `--strict`, il rend compte et sort avec le code 0 ; avec `--strict`, tout écart donne le code 1. Si aucune des trois tables n'est présente, il le dit (« aucune matrice trouvée ») et sort avec le code 0 ; si une partie seulement l'est, les tables absentes sont des écarts. Il relit le `.tex` sans rien importer du moteur, après le même retrait du texte non composé que la concordance, et donne pour chaque table ses décomptes (lignes, colonnes hors étiquette, termes). Il est exécuté par la batterie `tests/unitaires` (`test_matrices.py`), qui le lance en `--strict` sur la spécification.

**Écriture d'une cellule.**
- Une cellule de matrice est vide, `0`, ou une somme de **termes simples** signés, en une seule formule `$…$` : `$-D_H - B_H$`. Un terme simple est un encours, un flux, le produit d'un taux par l'encours d'un seul détenteur, ou la variation d'un encours ; le script ne décompose pas un produit (`i_L L/n_a`, `\delta K/n_a` sont des termes).
- Chaque terme porte son signe (`+`, `-` ou `−`), le premier compris ; un terme sans signe est un écart. Parenthèses, crochets, `=`, `\left`, `\right`, `\frac`, `\sum`, `\pm` et `\mp` sont refusés : une cellule ne factorise rien. Un exposant ou un indice signé s'écrit entre accolades (`x^{-1}`).
- Aucun agrégat dans une cellule : $D$, $B$, $T$, $\Delta D$, $\Delta B$ et leurs intérêts s'écrivent développés par détenteur (`$-D_H - D_F$`) ; les agrégats se définissent dans le texte.
- Deux écritures d'un même terme sont confondues si elles ne diffèrent que par les espaces, les espaces fins (`\,`, `\;`, `\!`, `\:`, `~`), les accolades d'un seul symbole (`B_{H}` = `B_H`) ou les commandes `\mathit`, `\mathrm`, `\text`, `\textrm`, `\textit` ; toute autre différence les distingue, y compris l'ordre des indices et exposants (`B_H^p` ≠ `B^p_H`).

**Structure des tables.**
- Les zones d'une `longtable` sont délimitées par `\endfirsthead`, `\endhead`, `\endfoot` et `\endlastfoot` ; la première ligne à plusieurs cellules de la première tête est l'en-tête, les en-têtes répétés lui sont identiques (une note d'une seule cellule, « Suite de la page précédente », est ignorée) ; les pieds sont ignorés ; les filets, la ligne de `\caption` et une ligne faite d'un seul `\multicolumn` sont ignorés.
- La première colonne porte l'étiquette de la ligne ; son premier mot est l'identifiant (`11a`, `19a-ménages`), identique dans `tab:matrice-flux` et `tab:portes-monnaie`.
- `tab:matrice-bilans` : une colonne par secteur, puis une colonne « Réel » (actifs réels : −K et −IN sur leurs lignes, +K + IN sur la ligne de valeur nette) ; valeur nette développée secteur par secteur.
- `tab:matrice-flux` : colonnes reconnues à leur en-tête (« Ménages », « Entr. … » pour les deux sous-colonnes des entreprises, « Banque », « Banque centrale » ou « BC », « État ») ; une seule signature (ΔM, ΔH) par ligne, les lignes à parts de signatures différentes étant scindées (11a/b/c, 19a-ménages/banque/BC, 19b-ménages/banque).
- Aucune colonne Σ dans les deux matrices.
- `tab:portes-monnaie`, table non sommée : colonnes « Montant », « ΔM », « ΔH » ; le montant est la somme des termes positifs de la ligne de même identifiant de `tab:matrice-flux`, toujours écrit ; un signe vaut `+`, `-`, `−` ou `0`, et `poste` sur les lignes 17 et 20 (postes de règlement), exigé là et refusé ailleurs.
- En tête de chaque table (légende) : unité, fenêtre et convention de signe. Ce point **n'est pas vérifié** par le script : il relève de la relecture.

**Ce que le script vérifie**, terme à terme et sans valeur numérique :
- (a) chaque ligne des deux matrices est nulle : chaque terme y apparaît exactement une fois en `+` et une fois en `−` ;
- (b) chaque colonne de `tab:matrice-bilans` est nulle au même sens, ligne de valeur nette et colonne « Réel » comprises ;
- (c) chaque colonne de secteur de `tab:matrice-flux` contient une fois son poste de règlement : ΔD_H (ménages), ΔD_F (entreprises, sous-colonnes réunies), ΔRes (banque et banque centrale), ΔM^G (État) ; ΔRes tiré de la colonne de la banque (ΔD_H et ΔD_F substitués) et ΔRes tiré de la colonne de la banque centrale (ΔM^G substitué) coïncident, égalité qui découle des lignes nulles ;
- (d) ΔM recomposé depuis `tab:portes-monnaie` (somme des montants par leur signe, lignes « poste » exclues) égale ΔD_H + ΔD_F, et ΔH recomposé égale ΔRes ; les deux tables ont les mêmes identifiants de ligne.

(c) et (d) ne sont pas vérifiés quand des cellules de `tab:matrice-flux` sont mal formées ou que ses lignes ne sont pas nulles : la sortie le signale (« non vérifié »), pour ne pas démultiplier un même défaut.

## Historique des conventions

| Date | Modification | Motif |
|---|---|---|
| 2026-09-29 | Création (issue #6, branche `claude/fondations`) | Jalon J0 ; préparation de la spécification du socle (J1) |
| 2026-09-29 | § 3 : liste des paquets TeX Live alignée sur `ci.yml` et le hook ; § 7 : procédure portée par `outils/compiler_specification.sh` ; § 2.2, § 1.3 et § 9 : contrat du script de concordance tel qu'implémenté (balise `^#+\s*eq:`, environnements multilignes, exemptions de la règle 6, règle 8, texte analysé, glossaire non vérifié) ; § 2.3 : forme canonique `Mn` des décisions (issue #4, branche `claude/fondations`) | Surface d'impact documentaire de l'issue #4 ; ADR 0003 et 0004, § Conséquences |
| 2026-09-30 | § 7 : motif de relance `Rerun to get\|Rerun LaTeX` (message de `longtable` compris) ; § 9 : règle 3 (`multline` à un numéro, `\nonumber` et `\notag`, seul le manque de label relevé), règle 4 (« décision Mn » ou « (Mn) », une décision par mention, numéro vérifié dans la feuille de route), règle 5 (nom nu dans `\tracabilite`), règle 6 (mode mathématique exempté, exposant et indice limités à `^`, `_`, `^{`, `_{`) (issue #4, branche `claude/fondations`) | Contrat aligné sur les corrections du script (eda7278, 4651b5f, 878fc6f) ; décision du mainteneur du 30/09/2026 sur les décisions multiples |
| 2026-09-30 | § 6 : convention calendaire tranchée (pas mensuel, n_a = 12, n_m = 1, règle de conversion linéaire unique, écriture des intérêts et de l'amortissement dans la matrice des flux, λ ≤ n_a) (issue #17, branche `claude/j1-temps-comptabilite`) | Décision M22 du mainteneur ; ADR 0005 |
| 2026-09-30 | § 9 : script des matrices `outils/verifier_matrices.py` cité à côté de la concordance, avec son usage, l'écriture d'une cellule, la structure des tables et ce qu'il vérifie (issue #19, branche `claude/j1-temps-comptabilite`) | Convention d'écriture des matrices fixée sur accord du mainteneur le 30/09/2026 (fiche « temps et comptabilité » § 9.7, commit `8fa2614`) ; décision M22 |
