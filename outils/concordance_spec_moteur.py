"""Concordance entre la spécification et le moteur.

Contrat : `docs/specification/CONVENTIONS.md`, § 9. Le script relit la
spécification (`docs/specification/nations_et_marches.tex`) et le code
(`src/`, `outils/`) **sans rien importer** (analyse textuelle du `.tex`,
analyse `tokenize` et `ast` du Python) et relève les écarts :

1. labels `\\label{eq:…}` et balises `# eq:…` : mêmes ensembles, chaque
   élément une seule fois de chaque côté ; une balise est un commentaire qui
   commence par un ou plusieurs `#` puis `eq:`, seul sur sa ligne (sur la
   ligne qui précède l'instruction, `CONVENTIONS.md` § 2.2) : une balise en
   fin de ligne de code est un écart ;
2. format des labels (expression régulière de `CONVENTIONS.md` § 2.1) et
   radical de bloc existant (`noyau`, `moteur` ou module de
   `src/nations/blocs/`) ;
3. chaque équation numérotée porte un label : `equation` et `multline`
   portent un seul numéro, donc exactement un label, sauf `\\nonumber` ou
   `\\notag` (aucun) ; dans les autres environnements multilignes, un label
   par ligne numérotée (seuls comptent les `\\\\` de niveau supérieur, pas
   ceux de `cases`, `aligned`, `matrix`, `array`…), contrôlé ligne par
   ligne : une ligne numérotée sans label est un manque, un second label sur
   une même ligne numérotée est un excès, un label sur une ligne marquée
   `\\notag` ou `\\nonumber` est un écart (pour `equation` et `multline`,
   la ligne est l'environnement entier) ; chaque encadré `lecture`
   contient `\\variables`, `\\sens`, `\\hyp`, `\\limites` puis `\\tracabilite`,
   dans cet ordre ;
4. statut de `\\tracabilite` (`dérivée`, `approchée` ou `choix de
   conception`) et décision du mainteneur citée dans la provenance, sous la
   forme « décision Mn » ou « (Mn) » (tiret admis : « M-n » ; espace ou `~`
   après « décision ») ; chaque numéro cité doit figurer dans le tableau des
   décisions de `docs/feuille-de-route.md` (lignes qui commencent par
   `| Mn |`). Une mention nue (« agrégat M2 ») n'est pas une décision ; une
   feuille de route absente est un écart ;
5. chaque `\\code{…}` désigne un objet existant de `src/` ou `outils/` ; le
   troisième argument de `\\tracabilite` est un nom nu (la macro l'enveloppe
   déjà dans `\\code` : `\\tracabilite{…}{…}{\\code{x}}` est un écart) et
   désigne le module ou la fonction qui porte la balise du label ;
6. aucun numéro entre parenthèses écrit en dur hors du mode mathématique
   (`$…$`, `$$…$$`, `\\(…\\)`, `\\[…\\]`, environnements `equation`, `align`,
   `gather`, `multline`, `flalign`, `alignat`, `eqnarray` et leurs formes
   étoilées : `$f(2)$` n'est pas un numéro d'équation), sauf :
   - une année (quatre chiffres, de 1000 à 2099 : « Godley et Lavoie
     (2007) ») ;
   - la citation exacte d'un document archivé : « v1.5, éq. (n) » ou
     « v2.0, éq. (n) », éventuellement suivie de « et (m) » ou « , (m) » ;
   - un exposant ou un indice : texte précédent terminé par `^`, `_`, `^{`
     ou `_{` (`\\textbf{(3)}` est relevé) ;
7. les paramètres cités par `\\code{…}` dans la table de calibration
   (`tab:calibration`) sont dans `src/nations/moteur/`. Le contrôle du
   glossaire attend que la table soit balisée pour le permettre : il n'est
   pas encore mis en œuvre, et la sortie le signale ;
8. chaque équation labellisée est suivie de son encadré `lecture`, avant
   l'équation numérotée suivante.

Avant l'analyse, le `.tex` est débarrassé de ce qui n'est pas composé : les
environnements `verbatim`, `verbatim*`, `lstlisting` et `comment`, les
`\\verb|…|` et les commentaires (`%` non échappé), retirés en un seul
parcours de gauche à droite (le premier ouvert l'emporte : un
`\\begin{verbatim}` cité dans un commentaire n'ouvre rien), puis les blocs
`\\iffalse … \\fi`. Dans un bloc, seules comptent pour l'appariement des
`\\fi` les conditions primitives de TeX et d'ε-TeX et les noms déclarés
hors d'un bloc par `\\newif` ou copiés d'une condition par `\\let`
(`\\ifbool`, `\\iftoggle`… n'en sont pas). Une copie de `\\iffalse` par
`\\let` ouvre un bloc comme `\\iffalse`. Un `\\else` du bloc lui-même le
ferme : la branche `\\else`, que TeX compose, est analysée. Un `\\iffalse`
cité par `\\let` ou écrit dans le corps d'une définition (`\\newcommand`,
`\\renewcommand`, `\\providecommand`, `\\newenvironment`,
`\\renewenvironment`, `\\def`, `\\gdef`) n'ouvre pas de bloc. Un `\\iffalse`
non refermé, ou dont la branche `\\else` n'a pas de `\\fi`, n'efface rien
lui-même (les blocs complets qui le suivent sont effacés) : c'est un écart
(règle 0, texte analysé), et la suite est analysée.
Limite : seules les commandes de définition listées ci-dessus sont
reconnues. Un `\\iffalse` écrit dans le corps de `\\DeclareRobustCommand`,
de `\\NewDocumentCommand` (ou d'une autre commande de `xparse`), ou cité par
`\\expandafter\\let\\csname …\\endcsname\\iffalse`, ouvre encore un bloc ;
`\\string\\iffalse` est lu comme un `\\iffalse`.

Usage : `uv run python outils/concordance_spec_moteur.py [--strict]`. Sans
`--strict`, le script rend compte et sort avec le code 0 ; avec `--strict`,
tout écart donne le code de sortie 1.
"""

from __future__ import annotations

import argparse
import ast
import io
import re
import sys
import tokenize
from dataclasses import dataclass, field
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
TEX_DEFAUT = RACINE / "docs" / "specification" / "nations_et_marches.tex"

# Expression régulière des labels d'équation (CONVENTIONS.md, § 2.1).
MOTIF_LABEL = re.compile(r"eq:[a-z][a-z0-9_]*-[a-z0-9]+(-[a-z0-9]+)*")
# Radicaux admis hors des modules de blocs (CONVENTIONS.md, § 2.1).
RADICAUX_TRANSVERSES = ("noyau", "moteur")
STATUTS = ("dérivée", "approchée", "choix de conception")
# Décision du mainteneur citée dans une provenance : « décision Mn » ou
# « (Mn) », tiret admis (« M-n », CONVENTIONS.md ; « Mn », feuille de route).
MOTIF_DECISION = re.compile(r"\b[dD]écision[\s~]+M-?(\d+)\b|\(M-?(\d+)\)")
# Ligne du tableau des décisions de la feuille de route : « | Mn | … ».
MOTIF_LIGNE_DECISION = re.compile(r"^\|\s*M(\d+)\s*\|", re.MULTILINE)
FEUILLE_DE_ROUTE = Path("docs") / "feuille-de-route.md"
RUBRIQUES_LECTURE = ("variables", "sens", "hyp", "limites", "tracabilite")
ENVIRONNEMENTS_NUMEROTES = (
    "equation", "align", "gather", "multline", "flalign", "alignat", "eqnarray",
)
# Environnements à un seul numéro, quel que soit le nombre de lignes.
ENVIRONNEMENTS_UN_NUMERO = ("equation", "multline")
# Balise de code : commentaire qui commence par « eq: » (un ou plusieurs #).
MOTIF_BALISE = re.compile(r"^#+\s*eq:(\S*)")
# Règle 6 : numéro entre parenthèses, et ses exemptions (année ; citation
# exacte d'un document archivé, CONVENTIONS.md § 1.3).
MOTIF_NUMERO = re.compile(r"\(\d+\)")
MOTIF_ANNEE = re.compile(r"\((?:1\d{3}|20\d{2})\)")
MOTIF_CITATION_ARCHIVE = re.compile(
    r"v(?:1\.5|2\.0),[\s~]*éqs?\.[\s~]*\(\d+\)(?:[\s~]*(?:,|et)[\s~]*\(\d+\))*"
)
# Environnements dont le contenu n'est pas composé comme du LaTeX.
ENVIRONNEMENTS_VERBATIM = ("verbatim", "verbatim*", "lstlisting", "comment")


@dataclass(frozen=True)
class Ecart:
    """Un écart de concordance : règle du contrat (§ 9), emplacement, message."""

    regle: int
    emplacement: str
    message: str


@dataclass(frozen=True)
class Balise:
    """Une balise `# eq:<label>` du code et les portées qui la contiennent."""

    label: str
    fichier: Path
    ligne: int
    # Noms qualifiés du module et des fonctions ou classes qui contiennent la
    # balise (ou qu'elle précède immédiatement).
    portees: frozenset[str]


@dataclass
class Rapport:
    """Résultat d'une vérification : écarts et décomptes."""

    ecarts: list[Ecart] = field(default_factory=list)
    nb_labels: int = 0
    nb_balises: int = 0
    nb_codes: int = 0
    nb_lectures: int = 0
    nb_equations: int = 0


# --------------------------------------------------------------------------
# Lecture du .tex
# --------------------------------------------------------------------------


def _blanchir(texte: str, debut: int, fin: int) -> str:
    """Remplace `texte[debut:fin]` par des espaces, fins de ligne conservées."""
    blanc = "".join("\n" if c == "\n" else " " for c in texte[debut:fin])
    return texte[:debut] + blanc + texte[fin:]


def _blanchir_zones(texte: str, zones: list[tuple[int, int]]) -> str:
    """Blanchit des intervalles `(début, fin)` disjoints, rangés dans l'ordre."""
    morceaux = []
    precedent = 0
    for debut, fin in zones:
        morceaux.append(texte[precedent:debut])
        morceaux.append("".join("\n" if c == "\n" else " " for c in texte[debut:fin]))
        precedent = fin
    morceaux.append(texte[precedent:])
    return "".join(morceaux)


def retirer_commentaires_et_verbatim(texte: str) -> str:
    """Efface commentaires, environnements verbatim et `\\verb|…|`, en un parcours.

    Le texte est lu une seule fois, de gauche à droite, comme TeX le lit : le
    premier de ces passages ouvert l'emporte. Un `%` non échappé efface la fin
    de sa ligne, `\\begin{verbatim}` cité compris ; dans un verbatim ou un
    `\\verb`, un `%` est un caractère comme un autre. Une barre oblique inverse
    et le caractère qui la suit forment un jeton : `\\%` n'ouvre pas de
    commentaire, `\\\\%` en ouvre un. Un verbatim sans fin n'est pas effacé.
    Un commentaire est supprimé, un verbatim remplacé par des espaces ; les fins
    de ligne sont conservées, pour que les positions restent traduisibles en
    numéros de ligne.
    """
    noms = "|".join(re.escape(n) for n in ENVIRONNEMENTS_VERBATIM)
    debut_verbatim = re.compile(r"\\begin\{(" + noms + r")\}")
    verb = re.compile(r"\\verb\*?([^A-Za-z\s*]).*?\1")
    special = re.compile(r"[%\\]")
    morceaux = []
    copie = 0  # début du texte pas encore recopié
    i = 0
    while (m := special.search(texte, i)) is not None:
        i = m.start()
        if texte[i] == "%":
            fin = texte.find("\n", i)
            fin = len(texte) if fin < 0 else fin
            morceaux.append(texte[copie:i])
            copie = i = fin
            continue
        fin = None
        env = debut_verbatim.match(texte, i)
        if env is not None:
            fermeture = "\\end{" + env.group(1) + "}"
            trouve = texte.find(fermeture, env.end())
            if trouve >= 0:
                fin = trouve + len(fermeture)
        if fin is None and (v := verb.match(texte, i)) is not None:
            fin = v.end()
        if fin is None:
            i += 2
            continue
        morceaux.append(texte[copie:i])
        morceaux.append("".join("\n" if c == "\n" else " " for c in texte[i:fin]))
        copie = i = fin
    morceaux.append(texte[copie:])
    return "".join(morceaux)


# Conditions de TeX (primitives) et d'ε-TeX (`\ifdefined`, `\ifcsname`,
# `\iffontchar`) : seules elles, et les noms déclarés par `\newif` ou copiés
# d'une condition par `\let`, ouvrent une condition dont TeX apparie le
# `\fi` quand il saute un bloc `\iffalse`. `\ifbool`, `\iftoggle`, `\ifdef…`, `\ifstrequal` (etoolbox), `\ifthenelse` (ifthen) ou
# `\iff` (symbole) n'en sont pas.
CONDITIONS_PRIMITIVES = frozenset({
    "if", "ifcat", "ifnum", "ifdim", "ifodd", "ifvmode", "ifhmode", "ifmmode",
    "ifinner", "ifvoid", "ifhbox", "ifvbox", "ifx", "ifeof", "iftrue", "iffalse",
    "ifcase", "ifdefined", "ifcsname", "iffontchar",
})


MESSAGE_IFFALSE_NON_REFERME = ("\\iffalse non refermé (aucun \\fi apparié) : "
                               "la suite est analysée")


def retirer_iffalse(texte: str) -> tuple[str, list[tuple[int, str]]]:
    """Efface les blocs `\\iffalse … \\fi`, conditions imbriquées comprises.

    Le texte est lu de gauche à droite. Un `\\newif\\ifnom` lu hors d'un bloc
    déclare `\\ifnom` comme condition pour la suite ; écrit dans un bloc, il
    n'est pas exécuté et ne déclare rien. Dans un bloc, seules comptent les
    conditions de `CONDITIONS_PRIMITIVES` et les noms déjà déclarés. Un
    `\\iffalse` sans son `\\fi` n'efface rien lui-même (les blocs complets
    qui le suivent sont effacés) : il est rendu comme anomalie
    `(position, message)`, et la lecture reprend après lui.

    Hors d'un bloc, `\\let\\nom<cible>` (`=` admis) donne à `\\nom` la nature
    de la cible, comme TeX : condition si la cible en est une (primitive,
    déclarée ou copiée), copie de `\\iffalse` si la cible est `\\iffalse` ou
    l'une de ses copies, ni l'une ni l'autre sinon. Une copie de `\\iffalse`
    ouvre un bloc comme `\\iffalse`, et compte dans un bloc comme toute
    condition.

    Un `\\else` au niveau du bloc (pas celui d'une condition imbriquée) le
    ferme : seul le texte de `\\iffalse` à `\\else` compris est effacé, et la
    branche `\\else`, que TeX compose, est relue hors bloc ; son `\\fi` reste
    dans le texte rendu, comme celui de toute condition hors bloc. Pour le
    trouver, les conditions composées sont comptées hors bloc ; une branche
    `\\else` sans `\\fi` laisse le bloc non refermé : son `\\iffalse` est
    lu comme un `\\iffalse` sans `\\fi` (même anomalie, même texte rendu),
    la lecture reprenant juste après lui.

    Hors d'un bloc, la cible de `\\let` et le corps d'une définition
    (`\\newcommand`, `\\renewcommand`, `\\providecommand`, étoilées ou non,
    `\\def`, `\\gdef` ; les deux corps de `\\newenvironment` et
    `\\renewenvironment`, étoilées ou non) ne sont pas exécutés quand TeX les
    lit : un `\\iffalse` qui s'y trouve n'ouvre pas de bloc, et un `\\newif`
    n'y déclare rien. Dans un bloc, TeX compte les conditions sans lire les
    définitions : elles y sont comptées.

    Limite : seules les définitions de `definitions` sont reconnues. Un
    `\\iffalse` dans le corps de `\\DeclareRobustCommand`, de
    `\\NewDocumentCommand` (ou d'une autre commande de `xparse`), ou cité par
    `\\expandafter\\let\\csname …\\endcsname\\iffalse`, ouvre encore un bloc ;
    `\\string\\iffalse` est lu comme un `\\iffalse` (ouvre un bloc, ou rend
    l'anomalie d'un `\\iffalse` sans `\\fi`).

    Comme dans `retirer_commentaires_et_verbatim`, une barre oblique inverse
    et le caractère qui la suit forment un jeton : un mot n'est une commande
    que précédé d'un nombre impair de barres (`\\\\iffalse` est un saut de
    ligne suivi du mot « iffalse »). La déclaration admet des accolades
    (`\\newif{\\ifnom}`).
    """
    # Les paires `\\` qui précèdent le jeton sont consommées hors du groupe
    # `jeton` : seule la barre restante ouvre la commande. Tout mot de
    # commande est lu, car `\let` peut faire d'un nom quelconque une condition.
    jeton = re.compile(r"(?<!\\)(?:\\\\)*(?P<jeton>\\(?P<nom>[A-Za-z@]+))(?![A-Za-z@])")
    declaration = re.compile(r"\s*(\{\s*)?\\(?P<nom>if[A-Za-z@]+)(?![A-Za-z@])(?(1)\s*\})")
    # Commande définie (mot ou symbole), et ce qui précède le corps.
    commande = r"\\(?:[A-Za-z@]+|[^A-Za-z@])"
    cible_let = re.compile(
        r"\s*\\(?P<nom>[A-Za-z@]+|[^A-Za-z@])\s*=?\s*\\(?P<cible>[A-Za-z@]+|[^A-Za-z@])")
    tete_def = re.compile(r"\s*" + commande + r"[^{]*")
    tete_newcommand = re.compile(
        r"\*?\s*(?:\{\s*" + commande + r"\s*\}|" + commande + r")(?:\s*\[[^\]]*\]){0,2}")
    tete_environnement = re.compile(r"\*?\s*\{[^{}]*\}(?:\s*\[[^\]]*\]){0,2}")
    definitions = {"def": (tete_def, 1), "gdef": (tete_def, 1),
                   "newcommand": (tete_newcommand, 1), "renewcommand": (tete_newcommand, 1),
                   "providecommand": (tete_newcommand, 1),
                   "newenvironment": (tete_environnement, 2),
                   "renewenvironment": (tete_environnement, 2)}
    def lire(non_refermes: set[int]):
        """Une lecture ; les `\\iffalse` de `non_refermes` sont lus sans `\\fi`.

        Rend le texte rendu, les anomalies et la position du premier
        `\\iffalse` dont la branche `\\else` n'a pas de `\\fi` (`None` sinon).
        """
        conditions = set(CONDITIONS_PRIMITIVES)  # primitives, `\newif` et `\let`
        fausses = {"iffalse"}  # `\iffalse` et ses copies par `\let` : ouvrent un bloc
        zones = []
        anomalies = []
        # Branches `\else` composées en attente de leur `\fi` : (niveau des
        # conditions composées à l'ouverture, position du `\iffalse`) ; `niveau`
        # compte les conditions composées encore ouvertes.
        branches: list[tuple[int, int]] = []
        niveau = 0
        position = 0
        while (m := jeton.search(texte, position)) is not None:
            position = m.end()
            nom = m.group("nom")
            if nom == "newif":
                d = declaration.match(texte, m.end())
                if d is not None:
                    conditions.add(d.group("nom"))
                    position = d.end()
                continue
            if nom == "let":
                if (c := cible_let.match(texte, m.end())) is not None:
                    # Comme TeX : la copie prend la nature de la cible.
                    nouveau, cible = c.group("nom"), c.group("cible")
                    conditions.discard(nouveau)
                    fausses.discard(nouveau)
                    if cible in conditions:
                        conditions.add(nouveau)
                    if cible in fausses:
                        fausses.add(nouveau)
                    position = c.end()
                continue
            if nom in definitions:
                tete, nombre = definitions[nom]
                t = tete.match(texte, m.end())
                if t is not None and (corps := lire_arguments(texte, t.end(), nombre)) is not None:
                    position = corps[1]
                continue
            if nom == "fi":
                if niveau > 0:
                    niveau -= 1
                    if branches and branches[-1][0] == niveau:
                        branches.pop()
                continue
            if nom not in fausses:
                if nom in conditions:
                    niveau += 1
                continue
            if m.start("jeton") in non_refermes:
                anomalies.append((m.start("jeton"), MESSAGE_IFFALSE_NON_REFERME))
                continue
            profondeur = 1
            for j in jeton.finditer(texte, m.end()):
                nom_j = j.group("nom")
                if nom_j == "fi":
                    profondeur -= 1
                elif nom_j == "else" and profondeur == 1:
                    # La branche `\else` est composée : relue hors bloc, elle
                    # attend son `\fi`.
                    profondeur = 0
                    branches.append((niveau, m.start("jeton")))
                    niveau += 1
                elif nom_j in conditions:
                    profondeur += 1
                if profondeur == 0:
                    zones.append((m.start("jeton"), j.end()))
                    position = j.end()
                    break
            else:
                anomalies.append((m.start("jeton"), MESSAGE_IFFALSE_NON_REFERME))
        if branches:
            return None, None, branches[0][1]
        return _blanchir_zones(texte, zones), sorted(anomalies), None

    # Une branche `\else` sans `\fi` : le bloc n'est pas refermé. Son
    # `\iffalse` est alors lu comme un `\iffalse` sans `\fi`, et la lecture
    # recommence : tout ce qui le suit (premier bloc compris, et ses `\newif`
    # et `\let`) est relu, comme après tout `\iffalse` non refermé. La
    # lecture qui précède ce `\iffalse` est inchangée. Les branches ouvertes
    # avant lui ont toutes été refermées avant lui (sinon, plus anciennes, elles
    # seraient restées sous lui dans la pile), et le restent à la relecture :
    # une nouvelle marque suit donc strictement la précédente. D'où au plus
    # une relecture par `\iffalse`, plus la dernière lecture. Le filtre des
    # marques plus loin que la nouvelle est défensif : il n'agit jamais.
    non_refermes: set[int] = set()
    while True:
        rendu, anomalies, a_relire = lire(non_refermes)
        if a_relire is None:
            return rendu, anomalies
        non_refermes = {x for x in non_refermes if x < a_relire} | {a_relire}


def preparer_tex_et_anomalies(texte: str) -> tuple[str, list[tuple[int, str]]]:
    """Texte composé et anomalies `(position, message)` de sa préparation.

    Commentaires et verbatim sont retirés en un parcours, puis les blocs
    `\\iffalse` ; les numéros de ligne sont conservés (pas les positions : un
    commentaire est supprimé). La position d'une anomalie se lit dans le texte
    rendu ; une anomalie (un `\\iffalse` non refermé) est un écart pour
    l'appelant.
    """
    return retirer_iffalse(retirer_commentaires_et_verbatim(texte))


def preparer_tex(texte: str) -> str:
    """Texte composé : sans verbatim, commentaires ni blocs `\\iffalse`.

    Les numéros de ligne sont conservés ; les anomalies sont lues par
    `preparer_tex_et_anomalies`.
    """
    return preparer_tex_et_anomalies(texte)[0]


def lignes_de_niveau_superieur(corps: str) -> list[str]:
    """Découpe un environnement multiligne aux `\\\\` de niveau supérieur.

    Les `\\\\` d'un environnement imbriqué (`cases`, `aligned`, `matrix`,
    `pmatrix`, `array`…) ou d'un groupe entre accolades ne séparent pas les
    lignes numérotées.
    """
    lignes = []
    profondeur = 0
    debut = 0
    i = 0
    while i < len(corps):
        ouvrant = corps.startswith("\\begin{", i)
        if ouvrant or corps.startswith("\\end{", i):
            profondeur += 1 if ouvrant else -1
            fermante = corps.find("}", i)
            i = len(corps) if fermante < 0 else fermante + 1
            continue
        car = corps[i]
        if car == "\\":
            if corps.startswith("\\\\", i) and profondeur == 0:
                lignes.append(corps[debut:i])
                debut = i + 2
            i += 2
            continue
        if car == "{":
            profondeur += 1
        elif car == "}":
            profondeur -= 1
        i += 1
    lignes.append(corps[debut:])
    return lignes


def numero_ligne(texte: str, position: int) -> int:
    """Numéro de ligne (à partir de 1) d'une position du texte."""
    return texte.count("\n", 0, position) + 1


def lire_arguments(texte: str, position: int, nombre: int) -> tuple[list[str], int] | None:
    """Lit `nombre` arguments entre accolades à partir de `position`.

    Les accolades imbriquées sont équilibrées ; les espaces entre arguments
    sont admis. Rend les arguments et la position qui suit le dernier, ou
    `None` si les arguments sont incomplets.
    """
    arguments = []
    i = position
    for _ in range(nombre):
        while i < len(texte) and texte[i] in " \t\n":
            i += 1
        if i >= len(texte) or texte[i] != "{":
            return None
        profondeur = 0
        debut = i + 1
        while i < len(texte):
            car = texte[i]
            if car == "\\":
                i += 2
                continue
            if car == "{":
                profondeur += 1
            elif car == "}":
                profondeur -= 1
                if profondeur == 0:
                    break
            i += 1
        if i >= len(texte):
            return None
        arguments.append(texte[debut:i])
        i += 1
    return arguments, i


def environnements(texte: str, noms: tuple[str, ...]) -> list[tuple[str, int, int, int]]:
    """Environnements non étoilés `noms` : (nom, début, début du contenu, fin)."""
    trouves = []
    motif = re.compile(r"\\begin\{(" + "|".join(noms) + r")\}")
    for m in motif.finditer(texte):
        nom = m.group(1)
        fin = texte.find("\\end{" + nom + "}", m.end())
        if fin < 0:
            fin = len(texte)
        trouves.append((nom, m.start(), m.end(), fin))
    return trouves


def nom_cite(argument: str) -> str:
    """Nom d'objet d'un argument, débarrassé d'un éventuel `\\code{…}`."""
    m = re.fullmatch(r"\s*\\code\{([^{}]*)\}\s*", argument)
    return (m.group(1) if m else argument).strip()


def zones_mathematiques(texte: str) -> list[tuple[int, int]]:
    """Intervalles `(début, fin)` du texte composés en mode mathématique.

    Environnements mathématiques (`ENVIRONNEMENTS_NUMEROTES`, formes étoilées
    comprises), puis, hors de ceux-ci, `$…$`, `$$…$$`, `\\(…\\)` et `\\[…\\]`.
    Une barre oblique inverse et le caractère qui la suit forment un jeton :
    `\\$` n'ouvre ni ne ferme de mode mathématique, et `\\\\[2pt]` n'est pas
    un `\\[`.
    """
    zones = []
    noms = "|".join(ENVIRONNEMENTS_NUMEROTES)
    for m in re.finditer(r"\\begin\{(" + noms + r")(\*?)\}", texte):
        fin = texte.find("\\end{" + m.group(1) + m.group(2) + "}", m.end())
        zones.append((m.start(), len(texte) if fin < 0 else fin))
    hors_env = texte
    for debut, fin in zones:
        hors_env = _blanchir(hors_env, debut, fin)
    fermants = {"$": "$", "$$": "$$", "\\(": "\\)", "\\[": "\\]"}
    i = 0
    while i < len(hors_env):
        if hors_env.startswith("$$", i):
            ouvrant = "$$"
        elif hors_env[i] == "$":
            ouvrant = "$"
        elif hors_env.startswith("\\(", i) or hors_env.startswith("\\[", i):
            ouvrant = hors_env[i:i + 2]
        else:
            i += 2 if hors_env[i] == "\\" else 1
            continue
        debut = i
        i += len(ouvrant)
        fermant = fermants[ouvrant]
        while i < len(hors_env) and not hors_env.startswith(fermant, i):
            i += 2 if hors_env[i] == "\\" else 1
        i = min(len(hors_env), i + len(fermant))
        zones.append((debut, i))
    return sorted(zones)


def lire_decisions(racine: Path) -> set[int] | None:
    """Numéros des décisions de `docs/feuille-de-route.md` (`None` si absente)."""
    chemin = racine / FEUILLE_DE_ROUTE
    if not chemin.is_file():
        return None
    return {int(n) for n in MOTIF_LIGNE_DECISION.findall(chemin.read_text(encoding="utf-8"))}


# --------------------------------------------------------------------------
# Lecture du code (analyse statique, sans import)
# --------------------------------------------------------------------------


class IndexCode:
    """Index statique des modules de `src/` et `outils/` et de leurs objets."""

    def __init__(self, racine: Path, src: Path, outils: Path) -> None:
        self.racine = racine
        self.src = src
        self.outils = outils
        self.modules: dict[str, Path] = {}
        self._arbres: dict[Path, ast.Module | None] = {}
        for base, prefixe in ((src, ""), (outils, "outils")):
            if not base.is_dir():
                continue
            for chemin in sorted(base.rglob("*.py")):
                parties = list(chemin.relative_to(base).with_suffix("").parts)
                if parties[-1] == "__init__":
                    parties = parties[:-1]
                if prefixe:
                    parties = [prefixe, *parties]
                if parties:
                    self.modules[".".join(parties)] = chemin

    def arbre(self, chemin: Path) -> ast.Module | None:
        """Arbre syntaxique d'un fichier, ou `None` s'il ne s'analyse pas."""
        if chemin not in self._arbres:
            try:
                self._arbres[chemin] = ast.parse(chemin.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeDecodeError):
                self._arbres[chemin] = None
        return self._arbres[chemin]

    def nom_module(self, chemin: Path) -> str | None:
        """Nom qualifié du module d'un fichier indexé."""
        for nom, fichier in self.modules.items():
            if fichier == chemin:
                return nom
        return None

    def existe(self, nom: str) -> bool:
        """Vrai si `nom` désigne un fichier, un module ou un objet du code.

        Un chemin (qui contient `/`) doit désigner un fichier ou un dossier
        existant sous `src/` ou `outils/`. Un nom pointé est résolu par le plus
        long préfixe qui est un module, puis objet par objet dans l'arbre
        syntaxique (fonctions, classes, affectations et importations de
        niveau module, puis corps de classe).
        """
        if "/" in nom:
            chemin = (self.racine / nom).resolve()
            dans_code = any(
                chemin == base.resolve() or base.resolve() in chemin.parents
                for base in (self.src, self.outils)
            )
            return dans_code and chemin.exists()
        parties = nom.split(".")
        for i in range(len(parties), 0, -1):
            prefixe = ".".join(parties[:i])
            if prefixe in self.modules:
                arbre = self.arbre(self.modules[prefixe])
                return arbre is not None and _resoudre(arbre.body, parties[i:])
        return False

    def fichiers_src(self) -> list[Path]:
        """Fichiers Python de `src/`, dans un ordre canonique."""
        return sorted(self.src.rglob("*.py")) if self.src.is_dir() else []


def _noms_definis(corps: list[ast.stmt]) -> dict[str, ast.stmt]:
    """Noms définis par une suite d'instructions (en descendant dans if/try)."""
    noms: dict[str, ast.stmt] = {}
    for noeud in corps:
        if isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            noms[noeud.name] = noeud
        elif isinstance(noeud, ast.Assign):
            for cible in noeud.targets:
                for n in ast.walk(cible):
                    if isinstance(n, ast.Name):
                        noms[n.id] = noeud
        elif isinstance(noeud, ast.AnnAssign) and isinstance(noeud.target, ast.Name):
            noms[noeud.target.id] = noeud
        elif isinstance(noeud, (ast.Import, ast.ImportFrom)):
            for alias in noeud.names:
                noms[(alias.asname or alias.name).split(".")[0]] = noeud
        elif isinstance(noeud, ast.If):
            noms.update(_noms_definis(noeud.body))
            noms.update(_noms_definis(noeud.orelse))
        elif isinstance(noeud, ast.Try):
            noms.update(_noms_definis(noeud.body))
            for gestionnaire in noeud.handlers:
                noms.update(_noms_definis(gestionnaire.body))
            noms.update(_noms_definis(noeud.orelse))
            noms.update(_noms_definis(noeud.finalbody))
    return noms


def _resoudre(corps: list[ast.stmt], parties: list[str]) -> bool:
    """Vrai si la suite `parties` se résout dans `corps` (classes imbriquées)."""
    if not parties:
        return True
    noeud = _noms_definis(corps).get(parties[0])
    if noeud is None:
        return False
    if len(parties) == 1:
        return True
    return isinstance(noeud, ast.ClassDef) and _resoudre(noeud.body, parties[1:])


def _portees_definitions(arbre: ast.Module) -> list[tuple[str, int, int, ast.AST]]:
    """Fonctions et classes d'un module : (nom qualifié local, début, fin, nœud).

    Le début inclut les décorateurs.
    """
    portees = []

    def parcourir(corps: list[ast.stmt], prefixe: str) -> None:
        for noeud in corps:
            if isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                nom = prefixe + noeud.name
                debut = min([noeud.lineno] + [d.lineno for d in noeud.decorator_list])
                portees.append((nom, debut, noeud.end_lineno or noeud.lineno, noeud))
                parcourir(noeud.body, nom + ".")
            else:
                for enfant in ast.iter_child_nodes(noeud):
                    if isinstance(enfant, ast.stmt):
                        parcourir([enfant], prefixe)

    parcourir(arbre.body, "")
    return portees


def extraire_balises(index: IndexCode) -> tuple[list[Balise], list[Ecart]]:
    """Balises `# eq:…` des commentaires de `src/`, avec leurs portées."""
    balises: list[Balise] = []
    ecarts: list[Ecart] = []
    for chemin in index.fichiers_src():
        source = chemin.read_text(encoding="utf-8")
        emplacement_fichier = _relatif(chemin, index.racine)
        try:
            jetons = list(tokenize.generate_tokens(io.StringIO(source).readline))
        except (tokenize.TokenError, SyntaxError) as erreur:
            ecarts.append(Ecart(1, emplacement_fichier, f"fichier illisible par tokenize : {erreur}"))
            continue
        arbre = index.arbre(chemin)
        definitions = _portees_definitions(arbre) if arbre is not None else []
        module = index.nom_module(chemin) or emplacement_fichier
        ignores = (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                   tokenize.DEDENT, tokenize.ENCODING)
        for k, jeton in enumerate(jetons):
            if jeton.type != tokenize.COMMENT:
                continue
            m = MOTIF_BALISE.match(jeton.string)
            if m is None:
                continue
            ligne = jeton.start[0]
            if jeton.line[:jeton.start[1]].strip():
                ecarts.append(Ecart(
                    1, f"{emplacement_fichier}:{ligne}",
                    f"eq:{m.group(1)} : balise en fin de ligne de code ; la placer seule "
                    "sur la ligne qui précède l'instruction (CONVENTIONS.md § 2.2)",
                ))
            # Ligne de la première instruction qui suit la balise.
            suivante = next((j.start[0] for j in jetons[k + 1:] if j.type not in ignores), None)
            portees = {module}
            for nom, debut, fin, _ in definitions:
                if debut <= ligne <= fin or debut == suivante:
                    portees.add(module + "." + nom)
            balises.append(Balise("eq:" + m.group(1), chemin, ligne, frozenset(portees)))
    return balises, ecarts


def _relatif(chemin: Path, racine: Path) -> str:
    """Chemin affiché, relatif à la racine du dépôt quand c'est possible."""
    try:
        return chemin.resolve().relative_to(racine.resolve()).as_posix()
    except ValueError:
        return chemin.as_posix()


# --------------------------------------------------------------------------
# Vérification
# --------------------------------------------------------------------------


def radicaux_admis(src: Path) -> set[str]:
    """Radicaux de labels admis : `noyau`, `moteur` et modules de blocs."""
    admis = set(RADICAUX_TRANSVERSES)
    blocs = src / "nations" / "blocs"
    if blocs.is_dir():
        for chemin in blocs.iterdir():
            if chemin.suffix == ".py" and chemin.stem != "__init__":
                admis.add(chemin.stem)
            elif chemin.is_dir() and (chemin / "__init__.py").exists():
                admis.add(chemin.name)
    return admis


def verifier(tex: Path, racine: Path, src: Path, outils: Path) -> Rapport:
    """Applique le contrat de `CONVENTIONS.md` § 9 et rend le rapport."""
    rapport = Rapport()
    index = IndexCode(racine, src, outils)
    nom_tex = _relatif(tex, racine)

    balises, ecarts_code = extraire_balises(index)
    rapport.ecarts.extend(ecarts_code)
    rapport.nb_balises = len(balises)

    anomalies: list[tuple[int, str]] = []
    if not tex.is_file():
        rapport.ecarts.append(Ecart(1, nom_tex, "spécification introuvable"))
        texte = ""
    else:
        texte, anomalies = preparer_tex_et_anomalies(tex.read_text(encoding="utf-8"))

    def ou(position: int) -> str:
        return f"{nom_tex}:{numero_ligne(texte, position)}"

    # --- Texte analysé (règle 0) : anomalies de la préparation -------------
    for position, message in anomalies:
        rapport.ecarts.append(Ecart(0, ou(position), message))

    # --- Règle 3 (équations numérotées) et relevé des labels ---------------
    labels: list[tuple[str, int]] = [
        ("eq:" + m.group(1), m.start())
        for m in re.finditer(r"\\label\{eq:([^{}]*)\}", texte)
    ]
    rapport.nb_labels = len(labels)
    equations = environnements(texte, ENVIRONNEMENTS_NUMEROTES)
    rapport.nb_equations = len(equations)
    labels_par_equation: list[tuple[int, list[str]]] = []
    for nom, debut, contenu, fin in equations:
        dedans = [(lab, pos) for lab, pos in labels if contenu <= pos < fin]
        corps = texte[contenu:fin]
        if nom in ENVIRONNEMENTS_UN_NUMERO:
            # Un seul numéro : l'environnement entier est une seule ligne,
            # contrôlée comme celles des environnements multilignes.
            lignes = [(contenu, corps)]
        else:
            # Une ligne par `\\` de niveau supérieur : chaque morceau commence
            # deux caractères après la fin du précédent (le séparateur).
            lignes, position = [], contenu
            for ligne in lignes_de_niveau_superieur(corps):
                lignes.append((position, ligne))
                position += len(ligne) + 2
        attendus = etiquetees = 0
        for position, ligne in lignes:
            if nom not in ENVIRONNEMENTS_UN_NUMERO and not ligne.strip():
                continue  # ligne vide après un `\\` final
            siens = [(lab, pos) for lab, pos in dedans
                     if position <= pos < position + len(ligne)]
            if re.search(r"\\(notag|nonumber)\b", ligne):
                for label, pos in siens:
                    rapport.ecarts.append(Ecart(
                        3, ou(pos),
                        f"{label} sur une ligne non numérotée ({nom}, "
                        "\\notag ou \\nonumber)",
                    ))
                continue
            attendus += 1
            if siens:
                etiquetees += 1
            for label, pos in siens[1:]:
                rapport.ecarts.append(Ecart(
                    3, ou(pos),
                    f"{label} en excès : second label eq: d'une même ligne "
                    f"numérotée ({nom})",
                ))
        if etiquetees < attendus:
            rapport.ecarts.append(Ecart(
                3, ou(debut),
                f"équation numérotée ({nom}) sans label eq: "
                f"({etiquetees} label(s) pour {attendus} ligne(s) numérotée(s))",
            ))
        labels_par_equation.append((fin, [lab for lab, _ in dedans]))
    for label, position in labels:
        if not any(contenu <= position < fin for _, _, contenu, fin in equations):
            rapport.ecarts.append(Ecart(
                3, ou(position), f"{label} hors d'une équation numérotée",
            ))

    # --- Règle 2 : format et radical ---------------------------------------
    admis = radicaux_admis(src)
    for label, position in labels:
        _verifier_format(label, ou(position), admis, rapport.ecarts)
    for balise in balises:
        _verifier_format(
            balise.label, f"{_relatif(balise.fichier, racine)}:{balise.ligne}", admis, rapport.ecarts,
        )

    # --- Règle 1 : égalité des ensembles, unicité ---------------------------
    positions_labels: dict[str, list[int]] = {}
    for label, position in labels:
        positions_labels.setdefault(label, []).append(position)
    balises_par_label: dict[str, list[Balise]] = {}
    for balise in balises:
        balises_par_label.setdefault(balise.label, []).append(balise)
    for label in sorted(positions_labels):
        positions = positions_labels[label]
        if len(positions) > 1:
            rapport.ecarts.append(Ecart(
                1, ou(positions[1]), f"{label} : label présent {len(positions)} fois dans la spécification",
            ))
        if label not in balises_par_label:
            rapport.ecarts.append(Ecart(1, ou(positions[0]), f"{label} : aucune balise dans src/"))
    for label in sorted(balises_par_label):
        occurrences = balises_par_label[label]
        if len(occurrences) > 1:
            lieux = ", ".join(f"{_relatif(b.fichier, racine)}:{b.ligne}" for b in occurrences)
            rapport.ecarts.append(Ecart(
                1, lieux, f"{label} : balise présente {len(occurrences)} fois dans src/",
            ))
        if label not in positions_labels:
            b = occurrences[0]
            rapport.ecarts.append(Ecart(
                1, f"{_relatif(b.fichier, racine)}:{b.ligne}",
                f"{label} : balise sans label dans la spécification",
            ))

    # --- Règles 3, 4 et 5 : encadrés « Lecture » ---------------------------
    decisions = lire_decisions(racine)
    if decisions is None:
        rapport.ecarts.append(Ecart(
            4, _relatif(racine / FEUILLE_DE_ROUTE, racine),
            "feuille de route introuvable : décisions M- invérifiables",
        ))
    lectures = environnements(texte, ("lecture",))
    rapport.nb_lectures = len(lectures)
    for _, debut, contenu, fin in lectures:
        corps = texte[contenu:fin]
        _verifier_lecture(corps, contenu, debut, texte, ou, index, balises_par_label,
                          labels_par_equation, lectures, decisions, rapport.ecarts)

    # --- Règle 5 : chaque \code{…} désigne un objet existant ---------------
    codes = [(m.group(1), m.start()) for m in re.finditer(r"\\code\{([^{}]*)\}", texte)
             if "#" not in m.group(1)]
    rapport.nb_codes = len(codes)
    for nom, position in codes:
        if not index.existe(nom.strip()):
            rapport.ecarts.append(Ecart(
                5, ou(position), f"\\code{{{nom}}} ne désigne aucun objet de src/ ni outils/",
            ))

    # --- Règle 6 : numéros d'équation en dur -------------------------------
    citations = [(c.start(), c.end()) for c in MOTIF_CITATION_ARCHIVE.finditer(texte)]
    maths = zones_mathematiques(texte)
    for m in MOTIF_NUMERO.finditer(texte):
        if MOTIF_ANNEE.fullmatch(m.group(0)):
            continue
        if texte.endswith(("^", "_", "^{", "_{"), 0, m.start()):
            continue
        if any(debut <= m.start() and m.end() <= fin for debut, fin in citations):
            continue
        if any(debut <= m.start() < fin for debut, fin in maths):
            continue
        rapport.ecarts.append(Ecart(
            6, ou(m.start()), f"numéro écrit en dur {m.group(0)} : employer \\eqref ou \\ref",
        ))

    # --- Règle 8 : chaque équation labellisée suivie de son encadré --------
    for k, (nom, debut, contenu, fin) in enumerate(equations):
        if not any(contenu <= pos < fin for _, pos in labels):
            continue
        suivante = equations[k + 1][1] if k + 1 < len(equations) else len(texte)
        if not any(fin < d < suivante for _, d, _, _ in lectures):
            rapport.ecarts.append(Ecart(
                8, ou(debut),
                f"équation labellisée ({nom}) sans encadré lecture avant l'équation numérotée suivante",
            ))

    # --- Règle 7 : paramètres de la table de calibration -------------------
    m_cal = re.search(r"\\label\{tab:calibration\}", texte)
    if m_cal is not None:
        for _, debut, contenu, fin in environnements(texte, ("longtable", "table", "tabular")):
            if debut <= m_cal.start() <= fin:
                for nom, position in codes:
                    if contenu <= position < fin and not nom.strip().startswith("nations.moteur."):
                        rapport.ecarts.append(Ecart(
                            7, ou(position),
                            f"paramètre \\code{{{nom}}} de la table de calibration hors de src/nations/moteur/",
                        ))
                break
    return rapport


def _verifier_format(label: str, emplacement: str, admis: set[str], ecarts: list[Ecart]) -> None:
    """Règle 2 : format du label et radical de bloc existant."""
    if not MOTIF_LABEL.fullmatch(label):
        ecarts.append(Ecart(2, emplacement, f"{label} : format invalide ({MOTIF_LABEL.pattern})"))
        return
    radical = label[len("eq:"):].split("-", 1)[0]
    if radical not in admis:
        ecarts.append(Ecart(
            2, emplacement,
            f"{label} : radical « {radical} » ni noyau, ni moteur, ni module de src/nations/blocs/",
        ))


def _verifier_lecture(corps, contenu, debut, texte, ou, index, balises_par_label,
                      labels_par_equation, lectures, decisions, ecarts) -> None:
    """Règles 3 à 5 pour un encadré `lecture` (rubriques, traçabilité)."""
    positions = {}
    for rubrique in RUBRIQUES_LECTURE:
        trouves = [m.start() for m in re.finditer(r"\\" + rubrique + r"(?![A-Za-z])", corps)]
        if len(trouves) != 1:
            ecarts.append(Ecart(
                3, ou(debut), f"encadré lecture : \\{rubrique} présent {len(trouves)} fois (attendu : 1)",
            ))
        if trouves:
            positions[rubrique] = trouves[0]
    presents = [r for r in RUBRIQUES_LECTURE if r in positions]
    if sorted(presents, key=positions.__getitem__) != presents:
        ecarts.append(Ecart(
            3, ou(debut),
            "encadré lecture : rubriques hors de l'ordre \\variables, \\sens, \\hyp, \\limites, \\tracabilite",
        ))
    if "tracabilite" not in positions:
        return
    position = contenu + positions["tracabilite"] + len("\\tracabilite")
    lus = lire_arguments(texte, position, 3)
    if lus is None:
        ecarts.append(Ecart(4, ou(position), "\\tracabilite : trois arguments attendus"))
        return
    (statut, provenance, objet), _ = lus
    statut = " ".join(statut.split())
    if statut not in STATUTS:
        ecarts.append(Ecart(4, ou(position), f"\\tracabilite : statut « {statut} » hors de {STATUTS}"))
    citees = [int(m.group(1) or m.group(2)) for m in MOTIF_DECISION.finditer(provenance)]
    if not citees:
        ecarts.append(Ecart(
            4, ou(position),
            "\\tracabilite : aucune décision citée dans la provenance (« décision Mn » ou « (Mn) »)",
        ))
    elif decisions is not None:
        for numero in citees:
            if numero not in decisions:
                ecarts.append(Ecart(
                    4, ou(position),
                    f"\\tracabilite : décision M{numero} absente du tableau des décisions de {FEUILLE_DE_ROUTE.as_posix()}",
                ))
    if re.search(r"\\code(?![A-Za-z])", objet):
        ecarts.append(Ecart(
            5, ou(position),
            "\\tracabilite enveloppe déjà son troisième argument dans \\code : écrire le nom nu",
        ))
    nom = nom_cite(objet)
    if not index.existe(nom):
        ecarts.append(Ecart(5, ou(position), f"\\tracabilite : {nom} ne désigne aucun objet de src/ ni outils/"))
    # Équation que l'encadré commente : la dernière équation numérotée qui se
    # termine avant lui, sans autre encadré entre les deux.
    precedentes = [(fin, labs) for fin, labs in labels_par_equation if fin < debut]
    if not precedentes:
        return
    fin_eq, labs = precedentes[-1]
    if any(fin_eq < d < debut for _, d, _, _ in lectures):
        return
    for label in labs:
        for balise in balises_par_label.get(label, []):
            if nom not in balise.portees:
                ecarts.append(Ecart(
                    5, ou(position),
                    f"\\tracabilite : {nom} ne contient pas la balise de {label} "
                    f"(portées : {', '.join(sorted(balise.portees))})",
                ))


# --------------------------------------------------------------------------
# Programme
# --------------------------------------------------------------------------


def afficher(rapport: Rapport, sortie=None) -> None:
    """Sortie lisible : décomptes, puis écarts triés par règle et emplacement."""
    sortie = sortie if sortie is not None else sys.stdout
    print("Concordance spécification ↔ moteur (CONVENTIONS.md, § 9)", file=sortie)
    print(
        f"  labels eq: {rapport.nb_labels} ; balises # eq: {rapport.nb_balises} ; "
        f"équations numérotées {rapport.nb_equations} ; encadrés lecture {rapport.nb_lectures} ; "
        f"\\code {rapport.nb_codes}",
        file=sortie,
    )
    print("  règle 7, glossaire : non vérifié (table des symboles pas encore balisée)", file=sortie)
    if not rapport.ecarts:
        print("Aucun écart.", file=sortie)
        return
    print(f"{len(rapport.ecarts)} écart(s) :", file=sortie)
    for e in sorted(rapport.ecarts, key=lambda e: (e.regle, e.emplacement, e.message)):
        print(f"  [règle {e.regle}] {e.emplacement} : {e.message}", file=sortie)


def main(arguments: list[str] | None = None) -> int:
    """Point d'entrée : rend 1 en mode strict si un écart est relevé, 0 sinon."""
    analyseur = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    analyseur.add_argument("--strict", action="store_true",
                           help="code de sortie non nul en cas d'écart")
    analyseur.add_argument("--tex", type=Path, default=TEX_DEFAUT,
                           help="spécification LaTeX (défaut : %(default)s)")
    analyseur.add_argument("--racine", type=Path, default=RACINE,
                           help="racine du dépôt, qui contient src/ et outils/")
    options = analyseur.parse_args(arguments)
    racine = options.racine
    rapport = verifier(options.tex, racine, racine / "src", racine / "outils")
    afficher(rapport)
    return 1 if options.strict and rapport.ecarts else 0


if __name__ == "__main__":
    # La console Windows n'est pas toujours en UTF-8 : sortie forcée en UTF-8.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
