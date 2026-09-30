"""Invariant : `archive/` n'est jamais importée (CLAUDE.md, invariant 4).

Deux contrôles complémentaires :

- **statique** (`ast`), sur tous les modules Python de `src/`, `tests/` et
  `outils/` : aucune instruction `import archive…` ni `from archive… import …` ;
  aucun `importlib.import_module` ni `__import__` d'un nom dont le premier
  composant est `archive` ; aucun `spec_from_file_location`, `run_path` ou
  `SourceFileLoader` dont un argument littéral est un chemin qui passe par un
  dossier `archive` ; aucun `exec` ni `compile` (fonctions natives) dont un
  argument littéral contient le mot `archive` ; aucun ajout de `archive` au
  chemin de recherche des modules (`sys.path` : appel `append`, `insert`,
  `extend`, affectation, affectation augmentée ou par tranche) ;
- **dynamique** : tous les sous-modules de `nations` sont importés, puis aucun
  module chargé (`sys.modules`) ne provient d'un fichier sous `archive/`.
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
APPELS_PAR_CHEMIN = {"spec_from_file_location", "run_path", "SourceFileLoader"}
APPELS_DE_CODE = {"exec", "compile"}
APPELS_SUR_LE_CHEMIN = {"append", "insert", "extend"}


def _litteraux(noeud: ast.AST) -> list[str]:
    """Chaînes littérales contenues dans un nœud."""
    return [
        n.value for n in ast.walk(noeud)
        if isinstance(n, ast.Constant) and isinstance(n.value, str)
    ]


def _chemin_par_archive(noeud: ast.AST) -> bool:
    """Vrai si un littéral du nœud est un chemin qui passe par `archive`."""
    return any("archive" in re.split(r"[/\\]", s) for s in _litteraux(noeud))


def _module_d_archive(noeud: ast.AST) -> bool:
    """Vrai si un littéral du nœud est un nom de module de premier composant `archive`."""
    return any(s.split(".")[0] == "archive" for s in _litteraux(noeud))


def _est_sys_path(noeud: ast.AST) -> bool:
    return ast.unparse(noeud) == "sys.path"


def _nom_appele(appel: ast.Call) -> str:
    fonction = appel.func
    if isinstance(fonction, ast.Attribute):
        return fonction.attr
    if isinstance(fonction, ast.Name):
        return fonction.id
    return ""


def importations_d_archive(source: str) -> list[int]:
    """Lignes où le source importe `archive` ou l'ajoute au chemin des modules."""
    lignes = []
    for noeud in ast.walk(ast.parse(source)):
        if isinstance(noeud, ast.Import):
            if any(a.name.split(".")[0] == "archive" for a in noeud.names):
                lignes.append(noeud.lineno)
        elif isinstance(noeud, ast.ImportFrom):
            if noeud.level == 0 and (noeud.module or "").split(".")[0] == "archive":
                lignes.append(noeud.lineno)
        elif isinstance(noeud, ast.Call):
            nom = _nom_appele(noeud)
            arguments = ast.Tuple(elts=[*noeud.args, *(k.value for k in noeud.keywords)])
            if nom in APPELS_PAR_NOM_DE_MODULE and _module_d_archive(arguments):
                lignes.append(noeud.lineno)
            elif nom in APPELS_PAR_CHEMIN and _chemin_par_archive(arguments):
                lignes.append(noeud.lineno)
            elif (
                nom in APPELS_DE_CODE
                and isinstance(noeud.func, ast.Name)
                and any(re.search(r"\barchive\b", s) for s in _litteraux(arguments))
            ):
                lignes.append(noeud.lineno)
            elif (
                nom in APPELS_SUR_LE_CHEMIN
                and isinstance(noeud.func, ast.Attribute)
                and _est_sys_path(noeud.func.value)
                and _chemin_par_archive(arguments)
            ):
                lignes.append(noeud.lineno)
        elif isinstance(noeud, (ast.Assign, ast.AugAssign)):
            cibles = noeud.targets if isinstance(noeud, ast.Assign) else [noeud.target]
            vise_le_chemin = any(
                _est_sys_path(c) or (isinstance(c, ast.Subscript) and _est_sys_path(c.value))
                for c in cibles
            )
            if vise_le_chemin and _chemin_par_archive(noeud.value):
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
    ],
)
def test_le_controle_admet_ce_qui_n_importe_pas(source):
    # Lire un fichier d'archive (fiche comparative) n'est pas l'importer.
    assert importations_d_archive(source) == []
