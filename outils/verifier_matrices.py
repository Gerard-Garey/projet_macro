"""Vérification des matrices des bilans et des flux, lues dans la spécification.

Contrat : convention d'écriture des matrices de `docs/blocs/temps_comptabilite.md`,
§ 9.7 (commit `8fa2614`), reprise dans le commentaire de l'issue #19. Le
script relit les tables `tab:matrice-bilans`, `tab:matrice-flux` et
`tab:portes-monnaie` de la spécification (des `longtable`) **sans rien
importer du moteur**, et vérifie **terme à terme**, sans valeur numérique :

- (a) chaque ligne des deux matrices est nulle : chaque terme y apparaît
  exactement une fois en `+` et une fois en `-` ;
- (b) chaque colonne de `tab:matrice-bilans` est nulle, au même sens (ligne
  de valeur nette et colonne « Réel » comprises) ;
- (c) chaque colonne de secteur de `tab:matrice-flux` contient **une fois**
  son poste de règlement (`POSTES_DE_REGLEMENT`), qu'elle définit ; les deux
  sous-colonnes des entreprises sont réunies. Ce que (c) vérifie en propre est
  ce **placement** : un poste absent de la colonne de son secteur, ou présent
  plusieurs fois, est un écart que (a) ne relève pas. L'égalité terme à terme
  de ΔRes tiré de la colonne de la banque (ΔD_H et ΔD_F substitués) et de ΔRes
  tiré de la colonne de la banque centrale (ΔM^G substitué) est aussi
  contrôlée, mais elle découle de la nullité des lignes (a) : elle n'échoue
  pas seule ;
- (d) ΔM recomposé depuis `tab:portes-monnaie` (Σ signe × montant, lignes
  « poste » exclues) = ΔD_H + ΔD_F, et ΔH recomposé = ΔRes, terme à terme ; le
  montant de chaque ligne, toujours écrit (lignes « poste » comprises), est la
  somme des termes positifs de la ligne de `tab:matrice-flux` de même
  identifiant, et les deux tables ont les mêmes identifiants de ligne.

Le point 6 de la convention (unité, fenêtre et convention de signe en tête de
chaque table) **n'est pas vérifié** par le script : il relève de la relecture.

**Grammaire d'une cellule** (§ 9.7, point 1). Une cellule de matrice est
vide, `0`, ou une somme de termes signés en mode mathématique, d'un seul
tenant : `$-D_H - B_H$`.
- Chaque terme porte son signe (`+`, `-` ou `−`), le premier compris ; un
  terme sans signe est un écart.
- Parenthèses, crochets, `=`, `\\left`, `\\right`, `\\frac`, `\\sum`, `\\pm`
  et `\\mp` sont refusés : une cellule ne factorise rien. Une commande est
  comparée par son nom entier (`\\leftarrow`, `\\pmb` sont admis).
- Un exposant ou un indice signé s'écrit entre accolades (`x^{-1}`) ; `x^-1`
  est refusé (« exposant ou indice signé sans accolades »), car il se lirait
  comme deux termes.
- Le script ne décompose pas un produit : `i_D D_H` est un terme. Un signe
  après `\\cdot` ou `\\times` est refusé (« signe après l'opérateur de
  produit ») : le signe d'un produit se porte en tête du terme. Un opérateur
  en fin de cellule est refusé (« facteur manquant »).
- Deux écritures d'un même terme sont confondues si elles ne diffèrent que par
  les espaces, les espaces fins (`\\,`, `\\;`, `\\!`, `\\:`, `~`), les
  accolades d'un seul symbole (`B_{H}` = `B_H`) ou les commandes de police
  `\\mathit`, `\\mathrm`, `\\text`, `\\textrm` et `\\textit` (`\\mathit{Res}`
  = `Res`). Toute autre différence les distingue : l'ordre des indices et
  exposants est significatif (`B_H^{\\mathrm{prim}}` ≠ `B^{\\mathrm{prim}}_H`).
- Les secteurs (`SECTEURS`, reconnus à l'en-tête de colonne), leurs postes de
  règlement (`POSTES_DE_REGLEMENT`) et les lignes marquées « poste »
  (`LIGNES_POSTE`) sont déclarés en tête du script.

**Structure d'une table.** Les zones d'une `longtable` sont délimitées par
`\\endfirsthead`, `\\endhead`, `\\endfoot` et `\\endlastfoot`. Une note est
une ligne d'une seule cellule qui commence par `\\multicolumn` (« Suite de la
page précédente ») : c'est la seule ligne ignorée dans les têtes et le corps.
La première ligne qui contient `&` dans la première zone de tête (fermée par
`\\endfirsthead` ou `\\endhead`) est l'en-tête ; après lui, toute ligne de
cette tête autre qu'une note est un écart, qu'elle ait une cellule ou
plusieurs. Chacune des autres zones de tête (têtes répétées) porte au moins
une ligne qui contient `&` (sinon « tête répétée sans ligne d'en-tête »), et
toute ligne autre qu'une note, d'une cellule comme de plusieurs, y est
comparée au premier en-tête (« en-tête répété différent du premier
en-tête »). Limite : une ligne d'une seule cellule placée avant l'en-tête de
la première tête n'est pas relevée, qu'elle soit une note ou non. Les
zones de pied (fermées par `\\endfoot` ou `\\endlastfoot`) sont ignorées : ni
données ni en-tête. Le corps est la zone qui suit le dernier marqueur ; sans
marqueur de tête, il suit l'en-tête. Les filets (`\\toprule`, `\\midrule`…)
sont ignorés avec leurs seuls arguments (`[…]` optionnel ; `[…](…){…}` pour
`\\cmidrule`), de même qu'une ligne faite d'un seul `\\multicolumn` (note). La première colonne porte
l'étiquette de la ligne ; son premier mot est l'identifiant (`11a`,
`19a-ménages`). Les colonnes de secteur se reconnaissent à leur en-tête
(`SECTEURS`) ; une colonne Σ est un écart (§ 9.7, point 3). Dans
`tab:portes-monnaie`, les colonnes sont reconnues à « montant », « ΔM » et
« ΔH » ; un signe vaut `+`, `-`, `−`, `0` ou `poste`. Sur les lignes de
`LIGNES_POSTE` (17 et 20, § 9.7, point 5), les deux signes sont `poste`,
exigé ; ailleurs, `poste` est refusé. Le montant n'a pas d'exception : vide, il
est un écart ; écrit, il est vérifié, sur les lignes « poste » comme ailleurs.

Si aucune des trois tables n'est présente, le script le dit (« aucune matrice
trouvée ») et sort avec le code 0 ; si une partie seulement l'est, les tables
absentes sont des écarts.

Le texte non composé est retiré avant l'analyse par `preparer_tex_et_anomalies`
du script de concordance (numéros de ligne conservés) ; une
anomalie de ce retrait (un `\\iffalse` non refermé) est un écart `structure`.

Usage : `uv run python outils/verifier_matrices.py [--strict] [fichier.tex]`
(défaut : `docs/specification/nations_et_marches.tex`). Sans `--strict`, le
script rend compte et sort avec le code 0 ; avec `--strict`, tout écart donne
le code 1. Un fichier absent, illisible ou non UTF-8 donne un message
`fichier : …` sur la sortie d'erreur et le code 1, avec ou sans `--strict`.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
TEX_DEFAUT = RACINE / "docs" / "specification" / "nations_et_marches.tex"


def _charger_concordance():
    """Module `concordance_spec_moteur`, voisin de ce script, chargé par son chemin.

    `outils/` n'est pas un paquet ; le module déjà chargé (par les tests) est
    réutilisé.
    """
    nom = "concordance_spec_moteur"
    if nom in sys.modules:
        return sys.modules[nom]
    chemin = Path(__file__).resolve().parent / (nom + ".py")
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    sys.modules[nom] = module
    spec.loader.exec_module(module)
    return module


_concordance = _charger_concordance()
preparer_tex = _concordance.preparer_tex
preparer_tex_et_anomalies = _concordance.preparer_tex_et_anomalies
numero_ligne = _concordance.numero_ligne
lire_arguments = _concordance.lire_arguments
environnements = _concordance.environnements

LABEL_BILANS = "tab:matrice-bilans"
LABEL_FLUX = "tab:matrice-flux"
LABEL_PORTES = "tab:portes-monnaie"
LABELS = (LABEL_BILANS, LABEL_FLUX, LABEL_PORTES)

# Secteurs de `tab:matrice-flux`, reconnus au début de l'en-tête normalisé
# (minuscules, sans accents ni commandes). L'ordre compte : « banque
# centrale » avant « banque ». Les colonnes « entr… » sont réunies.
SECTEURS = (
    ("menages", ("menages",)),
    ("entreprises", ("entr",)),
    ("banque_centrale", ("banque centrale", "bc")),
    ("banque", ("banque",)),
    ("etat", ("etat",)),
)
NOMS_SECTEURS = {
    "menages": "ménages", "entreprises": "entreprises", "banque": "banque",
    "banque_centrale": "banque centrale", "etat": "État",
}
# Poste de règlement de chaque secteur (§ 9.7, point 7 (c)), en écriture LaTeX ;
# comparé après normalisation (`normaliser_terme`).
POSTES_DE_REGLEMENT = {
    "menages": r"\Delta D_H",
    "entreprises": r"\Delta D_F",
    "etat": r"\Delta M^G",
    "banque": r"\Delta Res",
    "banque_centrale": r"\Delta Res",
}
# Lignes de `tab:portes-monnaie` qui portent les postes de règlement (ΔD_H +
# ΔD_F et ΔRes) : leurs deux signes sont « poste », exigé ; les autres lignes
# le refusent (§ 9.7, point 5).
LIGNES_POSTE = ("17", "20")
# Colonne propre à `tab:matrice-bilans` (actifs réels, § 9.7, point 3).
COLONNE_REEL = "reel"

MARQUEURS_TETE = re.compile(r"\\(endfirsthead|endhead|endfoot|endlastfoot)(?![A-Za-z])")
# Filets et sauts de page effacés avant la lecture, avec leurs seuls arguments :
# `[épaisseur]` optionnel pour les filets de booktabs, `\addlinespace` et les
# sauts de page, `[…](…){…}` pour `\cmidrule`. Un groupe `{…}` ou `(…)` qui
# suit un autre filet est le début de la ligne suivante : il est gardé (#27).
FILETS = re.compile(
    r"\\cmidrule(?![A-Za-z])\s*(?:\[[^\]]*\])?\s*(?:\([^)]*\))?\s*(?:\{[^{}]*\})?"
    r"|\\(?:toprule|midrule|bottomrule|addlinespace|nopagebreak|pagebreak)(?![A-Za-z])"
    r"\s*(?:\[[^\]]*\])?"
    r"|\\(?:hline|newpage)(?![A-Za-z])"
)
ESPACES_FINS = re.compile(r"\\[,;!: ]|~|\\quad(?![A-Za-z])|\\qquad(?![A-Za-z])")
POLICES = re.compile(r"\\(?:mathit|mathrm|text|textrm|textit)\s*\{([^{}]*)\}")
ACCOLADE_SIMPLE = re.compile(r"([_^])\{([A-Za-z0-9]|\\[A-Za-z]+)\}")
INTERDITS = ("(", ")", "[", "]", "=", r"\left", r"\right", r"\frac", r"\sum", r"\pm", r"\mp")
# Opérateurs de produit : un signe qui les suit appartient au facteur, pas à la
# somme (`a\cdot -b` se lirait comme deux termes `a\cdot` et `-b`) ; refusé.
PRODUITS = (r"\cdot", r"\times")
SIGNES = {"+": 1, "-": -1, "−": -1}


@dataclass(frozen=True)
class Ecart:
    """Un écart : point vérifié (`format`, `structure`, `a` à `d`), emplacement, message."""

    regle: str
    emplacement: str
    message: str


@dataclass(frozen=True)
class Terme:
    """Un terme signé d'une cellule : signe, clé normalisée, écriture d'origine."""

    signe: int
    nom: str
    texte: str


@dataclass
class Cellule:
    """Une cellule : texte d'origine, emplacement `fichier:ligne`, termes lus."""

    texte: str
    emplacement: str
    termes: list[Terme] = field(default_factory=list)
    mal_formee: bool = False


@dataclass
class Ligne:
    """Une ligne du corps d'une table : étiquette, identifiant, cellules suivantes."""

    etiquette: str
    identifiant: str
    emplacement: str
    cellules: list[Cellule]


@dataclass
class Colonne:
    """Une colonne d'en-tête : texte affiché, clé normalisée, emplacement."""

    texte: str
    cle: str
    emplacement: str


@dataclass
class Table:
    """Une table lue : label, emplacement, colonnes (hors étiquette) et lignes."""

    label: str
    emplacement: str
    colonnes: list[Colonne]
    lignes: list[Ligne]

    def nb_termes(self) -> int:
        return sum(len(c.termes) for l in self.lignes for c in l.cellules)


@dataclass
class Rapport:
    """Résultat : écarts, décomptes par table, tables absentes, points non vérifiés."""

    ecarts: list[Ecart] = field(default_factory=list)
    # label -> (lignes, colonnes hors étiquette, termes)
    decomptes: dict[str, tuple[int, int, int]] = field(default_factory=dict)
    absentes: list[str] = field(default_factory=list)
    non_verifies: list[str] = field(default_factory=list)

    @property
    def aucune_matrice(self) -> bool:
        return len(self.absentes) == len(LABELS)


# --------------------------------------------------------------------------
# Lecture des cellules
# --------------------------------------------------------------------------


def normaliser_terme(texte: str) -> str:
    """Clé d'un terme : espaces, espaces fins, polices et accolades simples retirés."""
    s = ESPACES_FINS.sub("", texte)
    s = re.sub(r"\s+", "", s)
    precedent = None
    while precedent != s:
        precedent = s
        s = POLICES.sub(r"\1", s)
        s = s.replace("{}", "")
        s = ACCOLADE_SIMPLE.sub(r"\1\2", s)
    return s


def _accolades_equilibrees(texte: str) -> bool:
    profondeur = 0
    i = 0
    while i < len(texte):
        car = texte[i]
        if car == "\\":
            i += 2
            continue
        if car == "{":
            profondeur += 1
        elif car == "}":
            profondeur -= 1
            if profondeur < 0:
                return False
        i += 1
    return profondeur == 0


def _decouper_termes(corps: str) -> list[tuple[str, str]]:
    """Découpe une somme aux signes de niveau supérieur : [(signe, texte du terme)].

    Le texte qui précède le premier signe est rendu avec un signe vide.
    """
    morceaux: list[tuple[str, str]] = []
    signe = ""
    debut = 0
    profondeur = 0
    i = 0
    while i < len(corps):
        car = corps[i]
        if car == "\\":
            i += 2
            continue
        if car == "{":
            profondeur += 1
        elif car == "}":
            profondeur -= 1
        elif car in SIGNES and profondeur == 0:
            morceaux.append((signe, corps[debut:i]))
            signe = car
            debut = i + 1
        i += 1
    morceaux.append((signe, corps[debut:]))
    # Le premier morceau est vide quand la cellule commence par un signe.
    if not morceaux[0][1].strip():
        morceaux = morceaux[1:]
    return morceaux


def lire_cellule(texte: str) -> tuple[list[tuple[int, str, str]], str | None]:
    """Termes d'une cellule de matrice : ([(signe, clé, écriture)], erreur ou None)."""
    s = texte.strip()
    if s in ("", "0", "$0$"):
        return [], None
    dollars = len(re.findall(r"(?<!\\)\$", s))
    if not (s.startswith("$") and s.endswith("$") and dollars == 2):
        return [], "cellule hors du mode mathématique : attendu une seule formule $…$"
    corps = ESPACES_FINS.sub(" ", s[1:-1])
    if not corps.strip():
        return [], "formule vide : écrire une cellule vide ou 0"
    if corps.strip() == "0":
        return [], None
    for interdit in INTERDITS:
        # Une commande se compare par son nom entier : `\leftarrow`, `\rightarrow`
        # et `\pmb` ne sont pas `\left`, `\right` et `\pm` (#27).
        motif = (re.escape(interdit) + r"(?![A-Za-z])" if interdit.startswith("\\")
                 else re.escape(interdit))
        if re.search(motif, corps):
            return [], (f"« {interdit} » interdit : une cellule est une somme signée "
                        "de termes simples, développée (§ 9.7, point 1)")
    if not _accolades_equilibrees(corps):
        return [], "accolades déséquilibrées"
    termes = []
    morceaux = _decouper_termes(corps)
    for rang, (signe, brut) in enumerate(morceaux):
        # `x^-1` se découperait en `x^` et `-1` : le signe appartient à l'exposant.
        if normaliser_terme(brut).endswith(("^", "_")):
            return [], (f"exposant ou indice signé sans accolades après « {brut.strip()} » "
                        "(écrire par exemple x^{-1})")
        if normaliser_terme(brut).endswith(PRODUITS) and rang == len(morceaux) - 1:
            # Opérateur en fin de cellule : aucun signe ne le suit (#27).
            return [], f"facteur manquant après l'opérateur de produit de « {brut.strip()} »"
        if normaliser_terme(brut).endswith(PRODUITS):
            return [], (f"signe après l'opérateur de produit de « {brut.strip()} » : le signe "
                        "se porte en tête du terme (écrire par exemple -a\\cdot b)")
        if signe == "":
            return [], f"terme sans signe explicite : « {brut.strip()} »"
        cle = normaliser_terme(brut)
        if not cle:
            return [], "terme vide (signe isolé ou doublé)"
        if cle == "0":
            return [], "terme nul dans une somme"
        termes.append((SIGNES[signe], cle, brut.strip()))
    return termes, None


def lire_signe(texte: str) -> tuple[int | None, str | None]:
    """Signe d'une cellule de `tab:portes-monnaie` : (+1, 0, -1 ou None = poste, erreur)."""
    s = texte_simple(texte).replace(" ", "")
    if s in ("+",):
        return 1, None
    if s in ("-", "−"):
        return -1, None
    if s == "0":
        return 0, None
    if s == "poste":
        return None, None
    return 0, f"signe illisible « {texte.strip()} » : attendu +, -, 0 ou poste"


# --------------------------------------------------------------------------
# Lecture des tables
# --------------------------------------------------------------------------


def texte_simple(texte: str) -> str:
    """Texte d'en-tête ou d'étiquette : commandes et délimiteurs retirés.

    `\\Delta` devient « Δ » ; les autres noms de commande sont retirés, leurs
    arguments conservés.
    """
    s = texte.replace("\\Delta", "Δ").replace("\\Sigma", "Σ")
    s = re.sub(r"\\[A-Za-z]+\*?", " ", s)
    s = re.sub(r"[{}$]", " ", s).replace("~", " ")
    return re.sub(r"\s+", " ", s).strip()


def cle_entete(texte: str) -> str:
    """En-tête normalisé : texte simple, minuscules, sans accents (Δ et Σ gardés)."""
    s = texte_simple(texte).lower().replace("δ", "Δ").replace("σ", "Σ")
    decompose = unicodedata.normalize("NFKD", s)
    return "".join(c for c in decompose if not unicodedata.combining(c))


def secteur(cle: str) -> str | None:
    """Secteur d'une colonne de `tab:matrice-flux` d'après son en-tête normalisé."""
    for nom, prefixes in SECTEURS:
        for prefixe in prefixes:
            # « bc » seul ou suivi d'un mot ; les autres préfixes, en début d'en-tête.
            if cle == prefixe or cle.startswith(prefixe + " ") or (
                    prefixe != "bc" and cle.startswith(prefixe)):
                return nom
    return None


def _separer(texte: str, debut: int, fin: int, separateur: str) -> list[tuple[int, int]]:
    """Intervalles de `texte[debut:fin]` séparés par `separateur` de niveau supérieur.

    `separateur` vaut `\\\\` (fin de ligne ; un `*` et un argument `[…]`
    optionnels qui suivent sont sautés) ou `&` (séparateur de cellules ; `\\&`
    n'en est pas un). Les groupes `{…}` et les environnements imbriqués ne sont
    pas coupés.
    """
    intervalles = []
    profondeur = 0
    courant = debut
    i = debut
    while i < fin:
        if texte.startswith("\\begin{", i) or texte.startswith("\\end{", i):
            profondeur += 1 if texte.startswith("\\begin{", i) else -1
            fermante = texte.find("}", i)
            i = fin if fermante < 0 else fermante + 1
            continue
        car = texte[i]
        if car == "\\":
            if separateur == "\\\\" and texte.startswith("\\\\", i) and profondeur == 0:
                intervalles.append((courant, i))
                i += 2
                if i < fin and texte[i] == "*":
                    i += 1
                j = i
                while j < fin and texte[j] in " \t\n":
                    j += 1
                if j < fin and texte[j] == "[":
                    fermant = texte.find("]", j)
                    if 0 <= fermant < fin:
                        i = fermant + 1
                courant = i
                continue
            i += 2
            continue
        if car == "{":
            profondeur += 1
        elif car == "}":
            profondeur -= 1
        elif car == "&" and separateur == "&" and profondeur == 0:
            intervalles.append((courant, i))
            courant = i + 1
        i += 1
    intervalles.append((courant, fin))
    return intervalles


def _debut_utile(texte: str, debut: int, fin: int) -> int:
    """Position du premier caractère non blanc de l'intervalle (ou son début)."""
    i = debut
    while i < fin and texte[i] in " \t\n":
        i += 1
    return i if i < fin else debut


def lire_table(texte: str, label: str, chemin: str) -> tuple[Table | None, list[Ecart]]:
    """Lit la `longtable` qui porte `\\label{label}` ; `None` si elle est absente."""
    positions = [m.start() for m in re.finditer(r"\\label\{" + re.escape(label) + r"\}", texte)]
    if not positions:
        return None, []
    def ou(position: int) -> str:
        return f"{chemin}:{numero_ligne(texte, position)}"

    ecarts = []
    if len(positions) > 1:
        for p in positions[1:]:
            ecarts.append(Ecart("structure", ou(p), f"label {label} répété"))
    position = positions[0]
    englobant = [e for e in environnements(texte, ("longtable",)) if e[1] < position < e[3]]
    if not englobant:
        return None, ecarts + [Ecart("structure", ou(position),
                                     f"{label} n'est pas dans un environnement longtable")]
    _, debut_env, debut_contenu, fin = englobant[-1]
    lu = lire_arguments(texte, debut_contenu, 1)
    debut = lu[1] if lu is not None else debut_contenu
    # Texte de travail : filets et marqueurs de tête effacés, positions conservées.
    travail = texte[:debut] + FILETS.sub(lambda m: " " * len(m.group(0)), texte[debut:fin]) + texte[fin:]
    marqueurs = [m for m in MARQUEURS_TETE.finditer(travail, debut, fin)]
    for m in marqueurs:
        travail = travail[:m.start()] + " " * (m.end() - m.start()) + travail[m.end():]
    bornes = [debut] + [m.end() for m in marqueurs] + [fin]
    # Chaque zone est fermée par un marqueur, sauf la dernière (le corps). Les
    # zones fermées par `\endfirsthead` ou `\endhead` sont des têtes ; celles
    # fermées par `\endfoot` ou `\endlastfoot` sont des pieds, ignorés.
    tetes = [(bornes[k], bornes[k + 1]) for k, m in enumerate(marqueurs)
             if m.group(1) in ("endfirsthead", "endhead")]
    zone_corps = (bornes[-2], bornes[-1])

    def lignes_de(zone: tuple[int, int]) -> list[tuple[int, int]]:
        rangs = []
        for a, b in _separer(travail, zone[0], zone[1], "\\\\"):
            contenu = travail[a:b]
            if not contenu.strip() or "\\caption" in contenu:
                continue
            rangs.append((a, b))
        return rangs

    tete = lignes_de(tetes[0] if tetes else zone_corps)
    entete = next(((a, b) for a, b in tete if _separer(travail, a, b, "&")[1:]), None)
    if entete is None:
        return None, ecarts + [Ecart("structure", ou(debut_env), f"{label} : en-tête introuvable")]
    if tetes:
        corps = lignes_de(zone_corps)
        # Première tête : après l'en-tête, seule une note `\multicolumn` d'une
        # cellule est admise, comme dans le corps et les têtes répétées (une
        # ligne de données placée là échapperait à toute vérification).
        for a, b in tete:
            if a <= entete[0]:
                continue
            cellules_tete = _separer(travail, a, b, "&")
            premiere_tete = travail[cellules_tete[0][0]:cellules_tete[0][1]].strip()
            if len(cellules_tete) == 1 and premiere_tete.startswith("\\multicolumn"):
                continue  # note sur toute la largeur
            nature = ("ligne à cellules" if len(cellules_tete) > 1
                      else "ligne d'une cellule hors note \\multicolumn")
            ecarts.append(Ecart("structure", ou(_debut_utile(travail, a, b)),
                                f"{label} : {nature} dans la première tête, après l'en-tête"))
    else:
        corps = [r for r in tete if r[0] > entete[0]]
    cellules_entete = _separer(travail, entete[0], entete[1], "&")
    colonnes = [
        Colonne(texte_simple(travail[a:b]), cle_entete(travail[a:b]),
                ou(_debut_utile(travail, a, b)))
        for a, b in cellules_entete[1:]
    ]
    # En-têtes répétés (têtes suivant la première) : chaque tête porte au moins
    # une ligne à cellules, et chaque ligne est identique au premier en-tête ;
    # seule une note `\multicolumn` d'une cellule (« Suite de la page
    # précédente ») est ignorée, comme dans le corps.
    cles = [cle_entete(travail[a:b]) for a, b in cellules_entete]
    for zone in tetes[1:]:
        rangs = lignes_de(zone)
        if not any(_separer(travail, a, b, "&")[1:] for a, b in rangs):
            ecarts.append(Ecart("structure", ou(_debut_utile(travail, zone[0], zone[1])),
                                f"{label} : tête répétée sans ligne d'en-tête"))
        for a, b in rangs:
            cellules_repetees = _separer(travail, a, b, "&")
            premiere_repetee = travail[cellules_repetees[0][0]:cellules_repetees[0][1]].strip()
            if len(cellules_repetees) == 1 and premiere_repetee.startswith("\\multicolumn"):
                continue  # note sur toute la largeur
            repetees = [cle_entete(travail[c:d]) for c, d in cellules_repetees]
            if repetees != cles:
                ecarts.append(Ecart("structure", ou(_debut_utile(travail, a, b)),
                                    f"{label} : en-tête répété différent du premier en-tête"))
    lignes = []
    for a, b in corps:
        cellules = _separer(travail, a, b, "&")
        premiere = travail[cellules[0][0]:cellules[0][1]].strip()
        if len(cellules) == 1 and premiere.startswith("\\multicolumn"):
            continue  # note sur toute la largeur
        emplacement = ou(_debut_utile(travail, a, b))
        etiquette = texte_simple(premiere)
        identifiant = etiquette.split(" ")[0] if etiquette else ""
        if len(cellules) - 1 > len(colonnes):
            ecarts.append(Ecart("format", emplacement,
                                f"{label}, ligne « {etiquette} » : {len(cellules) - 1} cellules "
                                f"pour {len(colonnes)} colonnes"))
        lues = [Cellule(travail[c:d].strip(), ou(_debut_utile(travail, c, d)))
                for c, d in cellules[1:len(colonnes) + 1]]
        while len(lues) < len(colonnes):
            lues.append(Cellule("", emplacement))
        lignes.append(Ligne(etiquette, identifiant, emplacement, lues))
    return Table(label, ou(position), colonnes, lignes), ecarts


def lire_termes(table: Table, ecarts: list[Ecart]) -> None:
    """Lit les termes de chaque cellule d'une matrice ; une cellule mal formée est un écart."""
    for ligne in table.lignes:
        for colonne, cellule in zip(table.colonnes, ligne.cellules):
            termes, erreur = lire_cellule(cellule.texte)
            if erreur is not None:
                cellule.mal_formee = True
                ecarts.append(Ecart(
                    "format", cellule.emplacement,
                    f"{table.label}, ligne « {ligne.etiquette} », colonne « {colonne.texte} » : "
                    f"{erreur} (cellule « {cellule.texte} »)"))
                continue
            cellule.termes = [Terme(s, n, t) for s, n, t in termes]


# --------------------------------------------------------------------------
# Vérifications
# --------------------------------------------------------------------------


def nullite(termes: list[Terme]) -> list[str]:
    """Termes qui n'apparaissent pas exactement une fois en + et une fois en −."""
    plus: Counter[str] = Counter()
    moins: Counter[str] = Counter()
    ecritures: dict[str, str] = {}
    for t in termes:
        (plus if t.signe > 0 else moins)[t.nom] += 1
        ecritures.setdefault(t.nom, t.texte)
    messages = []
    for nom, ecriture in ecritures.items():
        if (plus[nom], moins[nom]) != (1, 1):
            messages.append(f"terme « {ecriture} » : {plus[nom]} fois en +, {moins[nom]} fois "
                            "en − (attendu : une fois chacun)")
    return messages


def verifier_lignes(table: Table, ecarts: list[Ecart]) -> None:
    """Point (a) : chaque ligne est nulle terme à terme."""
    for ligne in table.lignes:
        if any(c.mal_formee for c in ligne.cellules):
            continue
        termes = [t for c in ligne.cellules for t in c.termes]
        for message in nullite(termes):
            ecarts.append(Ecart("a", ligne.emplacement,
                                f"{table.label}, ligne « {ligne.etiquette} » : {message}"))


def verifier_colonnes_bilans(table: Table, ecarts: list[Ecart]) -> None:
    """Point (b) : chaque colonne de la matrice des bilans est nulle terme à terme."""
    for j, colonne in enumerate(table.colonnes):
        cellules = [l.cellules[j] for l in table.lignes]
        if any(c.mal_formee for c in cellules):
            continue
        for message in nullite([t for c in cellules for t in c.termes]):
            ecarts.append(Ecart("b", colonne.emplacement,
                                f"{table.label}, colonne « {colonne.texte} » : {message}"))


def verifier_colonnes_sigma(table: Table, ecarts: list[Ecart]) -> None:
    """Les colonnes Σ sont supprimées (§ 9.7, point 3)."""
    for colonne in table.colonnes:
        if "Σ" in colonne.cle or colonne.cle.startswith("somme"):
            ecarts.append(Ecart("structure", colonne.emplacement,
                                f"{table.label} : colonne « {colonne.texte} » ; les colonnes Σ "
                                "sont supprimées (§ 9.7, point 3)"))


Expression = dict[str, int]


def _ajouter(cible: Expression, source: Expression, facteur: int) -> None:
    for nom, coefficient in source.items():
        cible[nom] = cible.get(nom, 0) + facteur * coefficient


def _reduite(expression: Expression) -> Expression:
    return {nom: c for nom, c in expression.items() if c != 0}


def _ecritures(table: Table) -> dict[str, str]:
    ecritures: dict[str, str] = {}
    for ligne in table.lignes:
        for cellule in ligne.cellules:
            for t in cellule.termes:
                ecritures.setdefault(t.nom, t.texte)
    return ecritures


def _comparer(gauche: Expression, droite: Expression, ecritures: dict[str, str],
              quoi_gauche: str, quoi_droite: str) -> list[str]:
    """Différences terme à terme entre deux expressions réduites."""
    gauche, droite = _reduite(gauche), _reduite(droite)
    messages = []
    for nom in list(dict.fromkeys(list(gauche) + list(droite))):
        a, b = gauche.get(nom, 0), droite.get(nom, 0)
        if a != b:
            messages.append(f"terme « {ecritures.get(nom, nom)} » : coefficient {a:+d} "
                            f"{quoi_gauche}, {b:+d} {quoi_droite}")
    return messages


def postes_de_reglement(table: Table, ecarts: list[Ecart]) -> dict[str, Expression] | None:
    """Point (c) : expression du poste de règlement de chaque secteur.

    Rend, par secteur, l'expression du poste tirée de sa colonne (colonne
    nulle résolue en ce poste), les postes des ménages, des entreprises et de
    l'État étant substitués dans celles de la banque et de la banque centrale ;
    `None` si la table ne le permet pas (écarts relevés).
    """
    colonnes_par_secteur: dict[str, list[int]] = {}
    complet = True
    for j, colonne in enumerate(table.colonnes):
        if "Σ" in colonne.cle:
            continue  # écart relevé par verifier_colonnes_sigma
        nom = secteur(colonne.cle)
        if nom is None:
            complet = False
            ecarts.append(Ecart("c", colonne.emplacement,
                                f"{table.label} : colonne « {colonne.texte} » ; secteur non "
                                "reconnu (ménages, entreprises, banque, banque centrale ou BC, État)"))
            continue
        colonnes_par_secteur.setdefault(nom, []).append(j)
    for nom in NOMS_SECTEURS:
        if nom not in colonnes_par_secteur:
            complet = False
            ecarts.append(Ecart("c", table.emplacement,
                                f"{table.label} : colonne du secteur {NOMS_SECTEURS[nom]} absente"))
    if not complet:
        return None
    postes = {nom: normaliser_terme(p) for nom, p in POSTES_DE_REGLEMENT.items()}
    brutes: dict[str, Expression] = {}
    for nom in NOMS_SECTEURS:
        termes = [t for l in table.lignes for j in colonnes_par_secteur[nom]
                  for t in l.cellules[j].termes]
        occurrences = [t for t in termes if t.nom == postes[nom]]
        emplacement = table.colonnes[colonnes_par_secteur[nom][0]].emplacement
        if len(occurrences) != 1:
            complet = False
            ecarts.append(Ecart("c", emplacement,
                                f"{table.label}, colonne {NOMS_SECTEURS[nom]} : le poste de "
                                f"règlement {POSTES_DE_REGLEMENT[nom]} y apparaît "
                                f"{len(occurrences)} fois (attendu : une fois)"))
            continue
        # Colonne nulle : signe × poste + reste = 0, donc poste = −signe × reste.
        signe = occurrences[0].signe
        expression: Expression = {}
        for t in termes:
            if t is not occurrences[0]:
                _ajouter(expression, {t.nom: t.signe}, -signe)
        brutes[nom] = expression
    if not complet:
        return None
    substituables = {postes[n]: brutes[n] for n in ("menages", "entreprises", "etat")}
    resultat = {n: _reduite(brutes[n]) for n in ("menages", "entreprises", "etat")}
    for nom in ("banque", "banque_centrale"):
        expression: Expression = {}
        for terme, coefficient in brutes[nom].items():
            if terme in substituables:
                _ajouter(expression, substituables[terme], coefficient)
            else:
                _ajouter(expression, {terme: coefficient}, 1)
        resultat[nom] = _reduite(expression)
    ecritures = _ecritures(table)
    for nom, expression in resultat.items():
        restants = [t for t in expression if t in set(postes.values())]
        for t in restants:
            complet = False
            ecarts.append(Ecart("c", table.emplacement,
                                f"{table.label} : le poste de règlement « {ecritures.get(t, t)} » "
                                f"reste dans l'expression tirée de la colonne "
                                f"{NOMS_SECTEURS[nom]}"))
    for message in _comparer(resultat["banque"], resultat["banque_centrale"], ecritures,
                             "par la colonne banque", "par la colonne banque centrale"):
        complet = False
        ecarts.append(Ecart("c", table.emplacement,
                            f"{table.label} : ΔRes diffère selon la colonne ; {message}"))
    return resultat if complet else None


def verifier_portes(portes: Table, flux: Table, reglement: dict[str, Expression] | None,
                    ecarts: list[Ecart]) -> None:
    """Point (d) : ΔM et ΔH recomposés depuis `tab:portes-monnaie`."""
    cles = [c.cle for c in portes.colonnes]
    j_montant = next((j for j, c in enumerate(cles) if c.startswith("montant")), None)
    j_m = next((j for j, c in enumerate(cles) if re.search(r"Δ\s*m\b", c)), None)
    j_h = next((j for j, c in enumerate(cles) if re.search(r"Δ\s*h\b", c)), None)
    manquantes = [nom for nom, j in (("montant", j_montant), ("ΔM", j_m), ("ΔH", j_h)) if j is None]
    if manquantes:
        ecarts.append(Ecart("structure", portes.emplacement,
                            f"{portes.label} : colonne(s) {', '.join(manquantes)} introuvable(s)"))
        return
    lignes_flux = {}
    for ligne in flux.lignes:
        if not ligne.identifiant:
            ecarts.append(Ecart("d", ligne.emplacement,
                                f"{flux.label} : ligne sans identifiant"))
        elif ligne.identifiant in lignes_flux:
            ecarts.append(Ecart("d", ligne.emplacement,
                                f"{flux.label} : identifiant « {ligne.identifiant} » répété"))
        else:
            lignes_flux[ligne.identifiant] = ligne
    vues: set[str] = set()
    delta_m: Expression = {}
    delta_h: Expression = {}
    lisible = True
    for ligne in portes.lignes:
        ident = ligne.identifiant
        if ident in vues:
            ecarts.append(Ecart("d", ligne.emplacement,
                                f"{portes.label} : identifiant « {ident} » répété"))
            continue
        vues.add(ident)
        if ident not in lignes_flux:
            ecarts.append(Ecart("d", ligne.emplacement,
                                f"{portes.label} : ligne « {ident} » absente de {flux.label}"))
            continue
        signes = []
        for j in (j_m, j_h):
            valeur, erreur = lire_signe(ligne.cellules[j].texte)
            if erreur is None and valeur is None and ident not in LIGNES_POSTE:
                erreur = (f"« poste » réservé aux lignes {' et '.join(LIGNES_POSTE)} "
                          "(postes de règlement)")
            elif erreur is None and valeur is not None and ident in LIGNES_POSTE:
                erreur = (f"« poste » exigé sur les lignes {' et '.join(LIGNES_POSTE)} "
                          f"(postes de règlement), lu « {ligne.cellules[j].texte.strip()} »")
            if erreur is not None:
                lisible = False
                ecarts.append(Ecart("format", ligne.cellules[j].emplacement,
                                    f"{portes.label}, ligne « {ident} » : {erreur}"))
            signes.append(valeur)
        cellule = ligne.cellules[j_montant]
        if not cellule.texte.strip():
            lisible = False
            ecarts.append(Ecart("d", cellule.emplacement,
                                f"{portes.label}, ligne « {ident} » : montant vide ; il "
                                f"s'écrit toujours (somme des termes positifs de la ligne "
                                f"de {flux.label})"))
            continue
        termes, erreur = lire_cellule(cellule.texte)
        if erreur is not None:
            lisible = False
            ecarts.append(Ecart("format", cellule.emplacement,
                                f"{portes.label}, ligne « {ident} », montant : {erreur} "
                                f"(cellule « {cellule.texte} »)"))
            continue
        cellule.termes = [Terme(s, n, t) for s, n, t in termes]
        positifs = Counter(t.nom for c in lignes_flux[ident].cellules for t in c.termes
                           if t.signe > 0)
        montant = Counter(n for s, n, _ in termes if s > 0)
        if any(s < 0 for s, _, _ in termes) or montant != positifs:
            lisible = False
            ecarts.append(Ecart("d", cellule.emplacement,
                                f"{portes.label}, ligne « {ident} » : le montant n'est pas la "
                                f"somme des termes positifs de la ligne de {flux.label}"))
            continue
        for cible, signe in ((delta_m, signes[0]), (delta_h, signes[1])):
            if signe is not None:
                _ajouter(cible, dict(montant), signe)
    for ident, ligne in lignes_flux.items():
        if ident not in vues:
            ecarts.append(Ecart("d", ligne.emplacement,
                                f"{flux.label} : ligne « {ident} » absente de {portes.label}"))
    if not lisible or reglement is None:
        return
    ecritures = _ecritures(flux)
    delta_d: Expression = {}
    _ajouter(delta_d, reglement["menages"], 1)
    _ajouter(delta_d, reglement["entreprises"], 1)
    for message in _comparer(delta_m, delta_d, ecritures,
                             "dans ΔM recomposé", "dans ΔD_H + ΔD_F"):
        ecarts.append(Ecart("d", portes.emplacement, f"{portes.label} : ΔM ; {message}"))
    for message in _comparer(delta_h, reglement["banque"], ecritures,
                             "dans ΔH recomposé", "dans ΔRes"):
        ecarts.append(Ecart("d", portes.emplacement, f"{portes.label} : ΔH ; {message}"))


def _relatif(chemin: Path) -> str:
    try:
        return chemin.resolve().relative_to(RACINE).as_posix()
    except ValueError:
        return str(chemin)


def verifier(tex: Path) -> Rapport:
    """Lit les trois tables de `tex` et applique les points (a) à (d)."""
    rapport = Rapport()
    chemin = _relatif(tex)
    texte, anomalies = preparer_tex_et_anomalies(tex.read_text(encoding="utf-8"))
    # Anomalie de la préparation (un `\iffalse` non refermé) : écart de structure.
    for position, message in anomalies:
        rapport.ecarts.append(Ecart("structure", f"{chemin}:{numero_ligne(texte, position)}",
                                    message))
    tables: dict[str, Table] = {}
    for label in LABELS:
        table, ecarts = lire_table(texte, label, chemin)
        rapport.ecarts.extend(ecarts)
        if table is None:
            if not ecarts:
                rapport.absentes.append(label)
            continue
        tables[label] = table
    if rapport.aucune_matrice:
        return rapport
    for label in rapport.absentes:
        rapport.ecarts.append(Ecart("structure", chemin,
                                    f"table {label} absente (les trois tables vont ensemble)"))
    lignes_non_nulles = False
    for label in (LABEL_BILANS, LABEL_FLUX):
        if label in tables:
            lire_termes(tables[label], rapport.ecarts)
            verifier_colonnes_sigma(tables[label], rapport.ecarts)
            avant = len(rapport.ecarts)
            verifier_lignes(tables[label], rapport.ecarts)
            if label == LABEL_FLUX:
                lignes_non_nulles = len(rapport.ecarts) > avant
    if LABEL_BILANS in tables:
        verifier_colonnes_bilans(tables[LABEL_BILANS], rapport.ecarts)
    reglement = None
    flux = tables.get(LABEL_FLUX)
    if flux is not None:
        # (c) et (d) supposent des lignes lisibles et nulles : sinon, chaque
        # défaut de ligne se répercuterait en une série d'écarts dérivés.
        if any(c.mal_formee for l in flux.lignes for c in l.cellules):
            rapport.non_verifies.append("(c) et (d) : cellules mal formées dans " + LABEL_FLUX)
        elif lignes_non_nulles:
            rapport.non_verifies.append("(c) et (d) : lignes non nulles dans " + LABEL_FLUX)
        else:
            reglement = postes_de_reglement(flux, rapport.ecarts)
    if flux is not None and LABEL_PORTES in tables and not rapport.non_verifies:
        verifier_portes(tables[LABEL_PORTES], flux, reglement, rapport.ecarts)
    for label, table in tables.items():
        rapport.decomptes[label] = (len(table.lignes), len(table.colonnes), table.nb_termes())
    return rapport


# --------------------------------------------------------------------------
# Programme
# --------------------------------------------------------------------------


def afficher(rapport: Rapport, tex: Path, sortie=None) -> None:
    """Sortie lisible : décomptes, puis écarts numérotés avec `fichier:ligne`."""
    sortie = sortie if sortie is not None else sys.stdout
    print("Matrices des bilans et des flux (temps_comptabilite.md, § 9.7)", file=sortie)
    if rapport.aucune_matrice and not rapport.ecarts:
        print(f"  aucune matrice trouvée dans {_relatif(tex)} "
              f"({', '.join(LABELS)} absents) : rien à vérifier.", file=sortie)
        return
    for label in LABELS:
        if label in rapport.decomptes:
            lignes, colonnes, termes = rapport.decomptes[label]
            print(f"  {label} : {lignes} lignes, {colonnes} colonnes, {termes} termes",
                  file=sortie)
    for note in rapport.non_verifies:
        print(f"  non vérifié : {note}", file=sortie)
    if not rapport.ecarts:
        print("Aucun écart.", file=sortie)
        return
    print(f"{len(rapport.ecarts)} écart(s) :", file=sortie)
    for n, e in enumerate(rapport.ecarts, start=1):
        print(f"  {n}. [{e.regle}] {e.emplacement} : {e.message}", file=sortie)


def main(arguments: list[str] | None = None) -> int:
    """Point d'entrée : rend 1 en mode strict si un écart est relevé, 0 sinon."""
    analyseur = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    analyseur.add_argument("--strict", action="store_true",
                           help="code de sortie non nul en cas d'écart")
    analyseur.add_argument("tex", nargs="?", type=Path, default=TEX_DEFAUT,
                           help="spécification LaTeX (défaut : %(default)s)")
    options = analyseur.parse_args(arguments)
    try:
        rapport = verifier(options.tex)
    except OSError as erreur:
        # Fichier absent ou illisible : message d'une ligne, sans trace (#27).
        print(f"fichier : {_relatif(options.tex)} : lecture impossible "
              f"({erreur.strerror or erreur})", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        # Fichier présent mais non UTF-8 : même message, sans trace (#27).
        print(f"fichier : {_relatif(options.tex)} : lecture impossible "
              "(encodage non UTF-8)", file=sys.stderr)
        return 1
    afficher(rapport, options.tex)
    return 1 if options.strict and rapport.ecarts else 0


if __name__ == "__main__":
    # La console Windows n'est pas toujours en UTF-8 : sortie forcée en UTF-8.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
