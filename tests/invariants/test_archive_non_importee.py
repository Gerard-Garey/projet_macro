"""Invariant : `archive/` n'est jamais importée (CLAUDE.md, invariant 4).

Deux contrôles complémentaires :

- **statique** (`ast`), sur tous les modules Python de `src/`, `tests/` et
  `outils/` : aucune instruction `import archive…` ni `from archive… import …` ;
  aucun `importlib.import_module` ni `__import__` d'un nom dont le premier
  composant est `archive` ; aucun `spec_from_file_location`, `run_path`,
  `SourceFileLoader`, `site.addsitedir` ou `zipimport.zipimporter` dont un
  argument littéral est un chemin qui passe par un dossier `archive` ou par
  un composant `archive.zip` (issue #75) ; aucun `exec` ni `compile`
  (fonctions natives, appelées par leur nom ou comme attribut ou indiçage de
  `builtins`, `__builtins__` ou d'un de leurs alias) dont un argument
  littéral contient le mot `archive` (issue #33) ; chacun de ces appels est
  aussi reconnu sous un alias de la fonction (`from … import … as`,
  affectation `f = importlib.import_module`, `getattr(objet, 'nom')`), suivi
  jusqu'à point fixe (issue #75) ; aucun ajout de `archive` au
  chemin de recherche des modules (`sys.path` : appel `append`, `insert`,
  `extend`, affectation, affectation augmentée ou par tranche) ; un nom (ou
  attribut) affecté depuis une expression qui contient un tel chemin, un tel
  nom de module ou un nom déjà marqué est marqué à son tour, jusqu'à point
  fixe, et compte dans ces appels comme le littéral lui-même (issue #9) ;
- **dynamique** : tous les sous-modules de `nations` sont importés, puis aucun
  module chargé (`sys.modules`) ne provient d'un fichier sous `archive/`.

Lire un fichier d'archive (fiche comparative) reste permis : seuls les appels
qui importent ou exécutent du code dans le processus sont contrôlés. Exécuter
le prototype dans un processus séparé (`subprocess`) reste permis aussi : les
fiches du J1 remesurent des faits en le lançant (issue #33).

Limites acceptées du contrôle statique (décision du mainteneur du 02/10/2026,
issue #9, sans issue de suivi) : un chemin vers `archive` n'est pas suivi
à travers un retour de fonction, un paramètre ou sa valeur par défaut, un
littéral découpé (`'arch' + 'ive'`), ni d'un module à l'autre ; la portée est
ignorée (un nom marqué l'est dans tout le module : marquage prudent).
Les alias de fonctions et du module `builtins` (issue #75) ont les mêmes
limites ; un alias de module (`import runpy as r`, puis `r.run_path(…)`)
reste relevé, l'appel étant reconnu par son seul nom d'attribut. Ne sont pas
suivis (issue #75) : un nom de fonction ou d'attribut construit
(`getattr(b, 'ex' + 'ec')`), un accès par `vars(…)` ou `__dict__`, un alias
de `sys` ou de `sys.path` (`import sys as s`, `from sys import path`), un
chemin dont le composant d'archive porte une autre extension que `.zip`,
un alias par affectation déstructurée (`f, g = importlib.import_module,
exec`), un `:=` employé comme fonction appelée, une boucle `for` sur des
fonctions, une fonction passée en argument (`functools.partial`, `map`),
`__builtins__.get('exec')`, un attribut de classe lu par la classe
(`class C: imp = …`, puis `C.imp(…)`), un composant `archive.zip` écrit dans
une autre casse (`ARCHIVE.ZIP`).
"""

import ast
import importlib
import pkgutil
import re
import sys
import types
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[2]
ARCHIVE = RACINE / "archive"
DOSSIERS = ("src", "tests", "outils")
APPELS_PAR_NOM_DE_MODULE = {"import_module", "__import__"}
APPELS_PAR_CHEMIN = {
    "spec_from_file_location", "run_path", "SourceFileLoader", "addsitedir", "zipimporter",
}
APPELS_DE_CODE = {"exec", "compile"}
APPELS_SUR_LE_CHEMIN = {"append", "insert", "extend"}
APPELS_CONTROLES = APPELS_PAR_NOM_DE_MODULE | APPELS_PAR_CHEMIN | APPELS_DE_CODE
# Composant de chemin qui désigne l'archive : le dossier, ou son paquet zip,
# importable par `zipimport` ou `sys.path` (issue #75).
COMPOSANT_D_ARCHIVE = re.compile(r"archive(\.zip)?")


def _cle(noeud: ast.AST) -> str | None:
    """Clé d'un nom ou d'un attribut (`ARCHIVE`, `self.racine`), sinon `None`."""
    if isinstance(noeud, (ast.Name, ast.Attribute)):
        return ast.unparse(noeud)
    return None


def _cles_de_cible(cible: ast.AST) -> list[str]:
    """Clés marquées par une cible d'affectation : la cible elle-même, jamais
    l'objet dont elle est un attribut (`self.source` ne marque pas `self`).

    Nom ou attribut : sa clé ; tuple, liste ou étoile : les clés de leurs
    éléments ; indiçage (`d['a']`, `l[0:0]`) : la clé du conteneur, sans ses
    préfixes (`os.environ['A']` marque `os.environ`, pas `os`).
    """
    if isinstance(cible, (ast.Name, ast.Attribute)):
        return [ast.unparse(cible)]
    if isinstance(cible, (ast.Tuple, ast.List)):
        return [cle for e in cible.elts for cle in _cles_de_cible(e)]
    if isinstance(cible, ast.Starred):
        return _cles_de_cible(cible.value)
    if isinstance(cible, ast.Subscript) and (cle := _cle(cible.value)) is not None:
        return [cle]
    return []


def _affectations(arbre: ast.AST) -> list[tuple[ast.AST, ast.AST]]:
    """Couples (cible, valeur) des liaisons de nom de l'arbre : affectation
    simple, annotée, augmentée ou `:=` ; boucle `for` et compréhension (valeur :
    l'itérable) ; `with … as` (valeur : l'expression de contexte)."""
    couples = []
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Assign):
            couples += [(c, noeud.value) for c in noeud.targets]
        elif isinstance(noeud, (ast.AnnAssign, ast.AugAssign, ast.NamedExpr)):
            if noeud.value is not None:
                couples.append((noeud.target, noeud.value))
        elif isinstance(noeud, (ast.For, ast.AsyncFor, ast.comprehension)):
            couples.append((noeud.target, noeud.iter))
        elif isinstance(noeud, ast.withitem) and noeud.optional_vars is not None:
            couples.append((noeud.optional_vars, noeud.context_expr))
    return couples


def _litteraux(noeud: ast.AST) -> list[str]:
    """Chaînes littérales contenues dans un nœud."""
    return [
        n.value for n in ast.walk(noeud)
        if isinstance(n, ast.Constant) and isinstance(n.value, str)
    ]


def _cite_un_nom_marque(noeud: ast.AST, marques: frozenset[str]) -> bool:
    """Vrai si le nœud lit un nom ou un attribut marqué."""
    return any(_cle(n) in marques for n in ast.walk(noeud))


def _chemin_par_archive(noeud: ast.AST, marques: frozenset[str] = frozenset()) -> bool:
    """Vrai si un littéral du nœud est un chemin qui passe par `archive` ou
    `archive.zip`, ou si le nœud lit un nom marqué."""
    return (
        any(
            COMPOSANT_D_ARCHIVE.fullmatch(composant)
            for s in _litteraux(noeud)
            for composant in re.split(r"[/\\]", s)
        )
        or _cite_un_nom_marque(noeud, marques)
    )


def _module_d_archive(noeud: ast.AST, marques: frozenset[str] = frozenset()) -> bool:
    """Vrai si un littéral du nœud est un nom de module de premier composant
    `archive`, ou si le nœud lit un nom marqué."""
    return (
        any(s.split(".")[0] == "archive" for s in _litteraux(noeud))
        or _cite_un_nom_marque(noeud, marques)
    )


def noms_marques(arbre: ast.AST) -> frozenset[str]:
    """Noms et attributs liés à une expression qui désigne `archive`.

    Une liaison (voir `_affectations`) marque sa cible si sa valeur contient un
    chemin qui passe par `archive`, un nom de module de premier composant
    `archive`, ou un nom déjà marqué ; on itère jusqu'à point fixe. Seule la
    cible est marquée (voir `_cles_de_cible`) ; les cibles déstructurées
    (`a, b = …`) le sont toutes.

    Limites acceptées (décision du mainteneur du 02/10/2026, issue #9) : aucune
    propagation par un retour de fonction, un paramètre ou sa valeur par
    défaut, un littéral découpé, ni entre modules ; la portée est ignorée, un
    nom marqué l'est dans tout le module (marquage prudent).
    """
    affectations = _affectations(arbre)
    marques: frozenset[str] = frozenset()
    while True:
        nouvelles = set(marques)
        for cible, valeur in affectations:
            if _chemin_par_archive(valeur, marques) or _module_d_archive(valeur, marques):
                nouvelles.update(_cles_de_cible(cible))
        if nouvelles == marques:
            return marques
        marques = frozenset(nouvelles)


def _est_sys_path(noeud: ast.AST) -> bool:
    return ast.unparse(noeud) == "sys.path"


def _texte(noeud: ast.AST) -> str | None:
    """Valeur d'une chaîne littérale, sinon `None`."""
    if isinstance(noeud, ast.Constant) and isinstance(noeud.value, str):
        return noeud.value
    return None


Designation = tuple[str, bool]


def _fonctions_designees(
    noeud: ast.AST, alias: dict[str, set[Designation]], natifs: frozenset[str]
) -> set[Designation]:
    """Fonctions que peut désigner une expression : couples (nom d'origine,
    native), native voulant dire « du module `builtins` » ; vide si
    l'expression n'est pas reconnue.

    Formes reconnues (issue #75) : un nom seul (`exec`, natif) ; un attribut
    (`importlib.import_module`), natif si son objet est un nom de `natifs`
    (`builtins`, `__builtins__` et leurs alias) ; un indiçage littéral d'un nom
    de `natifs` (`__builtins__['exec']`) ; `getattr(objet, 'nom')` ; et, pour
    un nom ou un attribut, les fonctions dont il est l'alias (`alias`). La
    portée étant ignorée, un nom seul `compile` reste natif même s'il est aussi
    importé d'un autre module (`from re import compile`) : lecture prudente.
    """
    designees = set(alias.get(_cle(noeud) or "", set()))
    if isinstance(noeud, ast.Name):
        designees.add((noeud.id, True))
    elif isinstance(noeud, ast.Attribute):
        designees.add((noeud.attr, ast.unparse(noeud.value) in natifs))
    elif (
        isinstance(noeud, ast.Subscript)
        and ast.unparse(noeud.value) in natifs
        and (nom := _texte(noeud.slice)) is not None
    ):
        designees.add((nom, True))
    elif (
        isinstance(noeud, ast.Call)
        and ast.unparse(noeud.func) == "getattr"
        and len(noeud.args) >= 2
        and (nom := _texte(noeud.args[1])) is not None
    ):
        designees.add((nom, ast.unparse(noeud.args[0]) in natifs))
    return designees


def _designe_builtins(
    noeud: ast.AST, alias: dict[str, set[Designation]], natifs: frozenset[str]
) -> bool:
    """Vrai si l'expression désigne le module `builtins` : un nom de `natifs`,
    ou son importation par nom (`__import__('builtins')`)."""
    if _cle(noeud) in natifs:
        return True
    return (
        isinstance(noeud, ast.Call)
        and any(
            nom in APPELS_PAR_NOM_DE_MODULE
            for nom, _ in _fonctions_designees(noeud.func, alias, natifs)
        )
        and len(noeud.args) >= 1
        and _texte(noeud.args[0]) == "builtins"
    )


def alias_des_appels(
    arbre: ast.AST,
) -> tuple[dict[str, set[Designation]], frozenset[str]]:
    """Alias des fonctions contrôlées et noms du module `builtins` (issue #75).

    Rend `(alias, natifs)` :
    - `alias` associe à un nom (ou attribut) les fonctions de
      `APPELS_CONTROLES` qu'il désigne (voir `_fonctions_designees`) : par
      `from importlib import import_module as f`, `from builtins import exec as
      e`, ou par une affectation dont la valeur désigne une telle fonction (`f
      = importlib.import_module`, `e = __builtins__['exec']`, `g = e`) ;
    - `natifs` contient `builtins`, `__builtins__`, leurs alias d'importation
      (`import builtins as b`) et les noms affectés depuis l'un d'eux (`b =
      builtins`, `b = __import__('builtins')`).

    Les deux ne font que croître, sur un domaine fini : le point fixe est
    atteint. Mêmes limites que `noms_marques`, sauf les cibles déstructurées,
    qui ne sont pas suivies (seules les cibles nom et attribut le sont) : portée ignorée (un nom qui
    désigne deux fonctions dans le module les désigne toutes deux), aucun suivi
    par un retour de fonction, un paramètre, ni d'un module à l'autre.
    """
    alias: dict[str, set[Designation]] = {}
    natifs = {"builtins", "__builtins__"}
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            natifs.update(a.asname for a in noeud.names if a.name == "builtins" and a.asname)
        elif isinstance(noeud, ast.ImportFrom) and noeud.level == 0:
            for a in noeud.names:
                if a.name in APPELS_CONTROLES:
                    alias.setdefault(a.asname or a.name, set()).add(
                        (a.name, noeud.module == "builtins")
                    )
    affectations = [
        (ast.unparse(cible), valeur)
        for cible, valeur in _affectations(arbre)
        if isinstance(cible, (ast.Name, ast.Attribute))
    ]
    while True:
        taille = len(natifs) + sum(len(d) for d in alias.values())
        for cle, valeur in affectations:
            if _designe_builtins(valeur, alias, frozenset(natifs)):
                natifs.add(cle)
            designees = {
                d for d in _fonctions_designees(valeur, alias, frozenset(natifs))
                if d[0] in APPELS_CONTROLES
            }
            if designees:
                alias.setdefault(cle, set()).update(designees)
        if len(natifs) + sum(len(d) for d in alias.values()) == taille:
            return alias, frozenset(natifs)


def importations_d_archive(source: str) -> list[int]:
    """Lignes où le source importe `archive` ou l'ajoute au chemin des modules."""
    lignes = []
    arbre = ast.parse(source)
    marques = noms_marques(arbre)
    alias, natifs = alias_des_appels(arbre)
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            if any(a.name.split(".")[0] == "archive" for a in noeud.names):
                lignes.append(noeud.lineno)
        elif isinstance(noeud, ast.ImportFrom):
            if noeud.level == 0 and (noeud.module or "").split(".")[0] == "archive":
                lignes.append(noeud.lineno)
        elif isinstance(noeud, ast.Call):
            designees = _fonctions_designees(noeud.func, alias, natifs)
            noms = {nom for nom, _ in designees}
            arguments = ast.Tuple(elts=[*noeud.args, *(k.value for k in noeud.keywords)])
            if noms & APPELS_PAR_NOM_DE_MODULE and _module_d_archive(arguments, marques):
                lignes.append(noeud.lineno)
            elif noms & APPELS_PAR_CHEMIN and _chemin_par_archive(arguments, marques):
                lignes.append(noeud.lineno)
            elif (
                any(nom in APPELS_DE_CODE and natif for nom, natif in designees)
                and (
                    any(re.search(r"\barchive\b", s) for s in _litteraux(arguments))
                    or _cite_un_nom_marque(arguments, marques)
                )
            ):
                lignes.append(noeud.lineno)
            elif (
                isinstance(noeud.func, ast.Attribute)
                and noeud.func.attr in APPELS_SUR_LE_CHEMIN
                and _est_sys_path(noeud.func.value)
                and _chemin_par_archive(arguments, marques)
            ):
                lignes.append(noeud.lineno)
        elif isinstance(noeud, (ast.Assign, ast.AugAssign)):
            cibles = noeud.targets if isinstance(noeud, ast.Assign) else [noeud.target]
            vise_le_chemin = any(
                _est_sys_path(c) or (isinstance(c, ast.Subscript) and _est_sys_path(c.value))
                for c in cibles
            )
            if vise_le_chemin and _chemin_par_archive(noeud.value, marques):
                lignes.append(noeud.lineno)
    return sorted(set(lignes))


def modules_du_depot() -> list[Path]:
    return sorted(p for d in DOSSIERS for p in (RACINE / d).rglob("*.py"))


def test_aucun_module_n_importe_archive():
    fautifs = []
    for chemin in modules_du_depot():
        for ligne in importations_d_archive(chemin.read_text(encoding="utf-8")):
            fautifs.append(f"{chemin.relative_to(RACINE).as_posix()}:{ligne}")
    assert fautifs == [], "archive/ importée : " + ", ".join(fautifs)


def test_le_controle_parcourt_des_modules():
    # Garde-fou : un contrôle qui ne lit rien passerait toujours.
    noms = {p.relative_to(RACINE).as_posix() for p in modules_du_depot()}
    assert "src/nations/__init__.py" in noms
    assert "outils/concordance_spec_moteur.py" in noms


def modules_charges_depuis_archive(modules: dict) -> list[str]:
    """Modules de `modules` (forme de `sys.modules`) dont le fichier est sous `archive/`."""
    archive = ARCHIVE.resolve()
    fautifs = []
    for nom, module in sorted(modules.items()):
        # Les modules natifs n'ont pas d'attribut __file__.
        fichier = vars(module).get("__file__") if hasattr(module, "__dict__") else None
        if fichier and archive in Path(fichier).resolve().parents:
            fautifs.append(f"{nom} ({fichier})")
    return fautifs


def test_aucun_module_charge_ne_vient_d_archive():
    import nations

    importes = [
        importlib.import_module(info.name).__name__
        for info in pkgutil.walk_packages(nations.__path__, prefix="nations.")
    ]
    # Garde-fou : les sous-paquets sont bien parcourus.
    assert {"nations.noyau", "nations.blocs", "nations.observation"} <= set(importes)
    fautifs = modules_charges_depuis_archive(dict(sys.modules))
    assert fautifs == [], "module chargé depuis archive/ : " + ", ".join(fautifs)


def test_le_controle_dynamique_detecte_un_module_d_archive():
    faux = types.ModuleType("moteur_v2")
    faux.__file__ = str(ARCHIVE / "v2.0" / "moteur_v2.py")
    assert modules_charges_depuis_archive({"moteur_v2": faux, "sys": sys}) == [
        f"moteur_v2 ({faux.__file__})"
    ]


@pytest.mark.parametrize(
    "source",
    [
        "import archive",
        "import archive.v2_0.moteur as m",
        "from archive.v2_0 import moteur",
        "import importlib\nimportlib.import_module('archive.v2_0.moteur')",
        "__import__('archive')",
        "import importlib.util\nimportlib.util.spec_from_file_location('m', 'archive/v2.0/moteur.py')",
        "import runpy\nrunpy.run_path('archive/v2.0/moteur.py')",
        "from importlib.machinery import SourceFileLoader\nSourceFileLoader('m', 'archive/v2.0/m.py').load_module()",
        "exec(open('archive/v2.0/moteur.py').read())",
        "exec('import archive')",
        "code = compile(open('archive/v2.0/moteur.py').read(), 'm', 'exec')",
        "import sys\nsys.path.insert(0, 'archive/v2.0')",
        "import sys\nsys.path += ['archive/v2.0']",
        "import sys\nsys.path[0:0] = ['archive']",
        "import sys\nsys.path = ['archive'] + sys.path",
        "import sys\nfrom pathlib import Path\nsys.path.append(str(Path('..') / 'archive'))",
        # Chemin ou nom de module construit dans une variable (issue #9).
        "import runpy\nfrom pathlib import Path\nARCHIVE = Path(__file__).parents[1] / 'archive'\n"
        "runpy.run_path(str(ARCHIVE / 'v2.0' / 'moteur.py'))",
        "import sys\nfrom pathlib import Path\nV2 = Path('archive') / 'v2.0'\nsys.path.insert(0, str(V2))",
        "import sys\nfrom pathlib import Path\nRACINE = Path('.')\nARCHIVE = RACINE / 'archive'\n"
        "V2 = ARCHIVE / 'v2.0'\nPROTOTYPE = V2 / 'prototype'\nsys.path.append(str(PROTOTYPE))",
        "import sys\nV2: str = 'archive/v2.0'\nsys.path = [V2] + sys.path",
        "import os, sys\ndossier = os.path.join('..', 'archive')\nsys.path += [dossier]",
        "import importlib\nnom = 'archive.v2_0'\nimportlib.import_module(nom + '.moteur')",
        "chemin = 'archive/v2.0/moteur.py'\nexec(open(chemin).read())",
        "import runpy\nfrom pathlib import Path\nclass Mesure:\n"
        "    def __init__(self):\n        self.source = Path('archive') / 'v2.0'\n"
        "    def lancer(self):\n        runpy.run_path(str(self.source / 'moteur.py'))",
        "import sys\nif (v2 := 'archive/v2.0'):\n    sys.path.insert(0, v2)",
        # Liaison par une boucle, une compréhension ou un `with … as` (issue #9).
        "import sys\nfor dossier in ['archive/v2.0']:\n    sys.path.insert(0, dossier)",
        "import sys\nchemins = ['archive/v2.0']\n[sys.path.append(c) for c in chemins]",
        "with open('archive/v2.0/moteur.py') as f:\n    exec(f.read())",
        # Appels non relevés avant l'issue #33 : un par appel.
        "import site\nsite.addsitedir('archive/v2.0')",
        "import zipimport\nzipimport.zipimporter('archive/v2.0.zip')",
        "import builtins\nbuiltins.exec(open('archive/v2.0/m.py').read())",
        "import builtins\nbuiltins.compile(open('archive/v2.0/m.py').read(), 'm', 'exec')",
        # Les mêmes, par un nom marqué (propagation de l'issue #9).
        "import site\nfrom pathlib import Path\nV2 = Path('archive') / 'v2.0'\nsite.addsitedir(str(V2))",
        "import zipimport\nZIP = 'archive/v2.0.zip'\nzipimport.zipimporter(ZIP).load_module('m')",
        "import builtins\nchemin = 'archive/v2.0/m.py'\nbuiltins.exec(open(chemin).read())",
        # Formes non relevées avant l'issue #75 : alias de la fonction appelée.
        "from importlib import import_module as f\nf('archive.v2_0.moteur')",
        "from runpy import run_path as lancer\nlancer('archive/v2.0/moteur.py')",
        "from site import addsitedir as ajouter\najouter('archive/v2.0')",
        "from builtins import exec as e\ne(open('archive/v2.0/m.py').read())",
        "import importlib\nf = importlib.import_module\nf('archive.v2_0')",
        "e = exec\ng = e\ng(open('archive/v2.0/m.py').read())",
        "import importlib\nf = getattr(importlib, 'import_module')\nf('archive.v2_0')",
        # Alias du module `builtins` (issue #75).
        "import builtins as b\nb.exec(open('archive/v2.0/m.py').read())",
        "import builtins\nb = builtins\nb.compile(open('archive/v2.0/m.py').read(), 'm', 'exec')",
        "b = __import__('builtins')\nb.exec(open('archive/v2.0/m.py').read())",
        "import builtins\ngetattr(builtins, 'exec')(open('archive/v2.0/m.py').read())",
        # `__builtins__`, module ou dictionnaire selon le contexte (issue #75).
        "__builtins__.exec(open('archive/v2.0/m.py').read())",
        "__builtins__['exec'](open('archive/v2.0/m.py').read())",
        "e = __builtins__['compile']\ne(open('archive/v2.0/m.py').read(), 'm', 'exec')",
        # Chemin par `archive.zip` (issue #75).
        "import zipimport\nzipimport.zipimporter('archive.zip')",
        "import sys\nsys.path.insert(0, 'archive.zip')",
        "import sys\nsys.path.append('archive.zip/v2.0')",
        "import runpy\nrunpy.run_path('../archive.zip')",
        "import importlib\nclass Mesure:\n    def __init__(self):\n"
        "        self.importer = importlib.import_module\n"
        "    def lancer(self):\n        self.importer('archive.v2_0')",
    ],
)
def test_le_controle_detecte_une_importation(source):
    assert importations_d_archive(source) != []


@pytest.mark.parametrize(
    "source",
    [
        "from . import archive_locale",
        "import archives_nationales",
        "import importlib\nimportlib.import_module('nations.archive')",
        "chemin = 'archive/v1.5/Nations_et_Marches_v1_5.tex'",
        "open('archive/v1.5/lisez-moi.md')",
        "import re\nmotif = re.compile('archive')",
        "import sys\nsys.path.append('src')",
        # Un nom marqué qui n'atteint aucun appel d'importation (issue #9).
        "from pathlib import Path\nARCHIVE = Path('archive')\ntexte = (ARCHIVE / 'v1.5' / 'a.tex').read_text()",
        "import sys\nfrom pathlib import Path\nARCHIVE = Path('archive')\nSRC = Path('src')\n"
        "sys.path.insert(0, str(SRC))",
        # Marquer un attribut ou un indiçage ne marque pas l'objet de base (issue #9).
        "import sys\nfrom pathlib import Path\nclass Mesure:\n    def __init__(self):\n"
        "        self.arch = Path('archive')\n        self.src = Path('src')\n"
        "    def preparer(self):\n        sys.path.insert(0, str(self.src))",
        "import os, sys\nos.environ['A'] = 'archive/v2.0'\nsys.path.insert(0, os.path.join('src'))",
        # Hors du contrôle (issue #33) : exécution dans un processus séparé, et
        # appels de #33 sur un chemin ou un code hors d'`archive`.
        "import subprocess, sys\nsubprocess.run([sys.executable, 'archive/v2.0/m.py'])",
        "import site\nsite.addsitedir('src')",
        "import zipimport\nzipimport.zipimporter('dist/nations.zip')",
        "import builtins\nbuiltins.exec('x = 1')",
        # Formes de l'issue #75 hors d'`archive`, ou homonymes non natifs.
        "from importlib import import_module as f\nf('nations.archive')",
        "from re import compile as c\nmotif = c('archive')",
        "import re\nc = re.compile\nmotif = c('archive')",
        "import builtins as b\nb.exec('x = 1')",
        "__builtins__['exec']('x = 1')",
        "import zipimport\nzipimport.zipimporter('dist/archive_v2.zip')",
        "open('archive.zip', 'rb')",
        "import sys\nsys.path.append('archive.txt')",
        # Alias circulaires sans fonction contrôlée : le point fixe est atteint.
        "a = b\nb = a\na('archive')",
    ],
)
def test_le_controle_admet_ce_qui_n_importe_pas(source):
    # Lire un fichier d'archive (fiche comparative) n'est pas l'importer.
    assert importations_d_archive(source) == []


def test_marquer_sys_path_ne_marque_pas_sys():
    # La tranche est détectée (ligne 2), pas l'appel qui lit un autre attribut de `sys`.
    source = "import sys\nsys.path[0:0] = ['archive']\nsys.path.insert(0, sys.prefix)"
    assert importations_d_archive(source) == [2]
