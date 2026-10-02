"""Invariant : `archive/` n'est jamais modifiée (CLAUDE.md, invariant 4).

Le SHA-256 de chaque fichier de `archive/`, lu en binaire tel qu'il est dans
l'arbre de travail, est comparé au manifeste `archive_sha256.txt` (voisin de
ce fichier ; format de `sha256sum` : `<empreinte>  <chemin depuis la racine>`,
une ligne par fichier, triée par chemin). Un fichier manquant, ajouté ou
modifié fait échouer le test.

Sont exclus les deux documents rédigés d'`archive/`, tenus à jour avec le
projet : `README.md` et `faits_mesures_G_K.md`, ainsi que tout fichier situé
sous un dossier `__pycache__` : le cache de compilation que crée l'exécution
du prototype v2.0, ignoré par Git (`.gitignore`), n'est pas une modification
d'`archive/` (issue #13). Tout autre fichier ajouté reste détecté.

Le manifeste vaut pour des fichiers en fins de ligne LF (`.gitattributes`) ;
les PDF sont binaires. Il ne se régénère que sur décision du mainteneur, avec
la modification d'`archive/` qu'il consigne.
"""

import hashlib
import shutil
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
ARCHIVE = RACINE / "archive"
MANIFESTE = Path(__file__).resolve().parent / "archive_sha256.txt"
EXCLUS = ("archive/README.md", "archive/faits_mesures_G_K.md")
CACHE = "__pycache__"


def lire_manifeste() -> dict[str, str]:
    """Empreintes attendues, par chemin relatif à la racine du dépôt."""
    attendues = {}
    for ligne in MANIFESTE.read_text(encoding="utf-8").splitlines():
        empreinte, chemin = ligne.split("  ", 1)
        attendues[chemin] = empreinte
    return attendues


def empreintes_actuelles(racine: Path = RACINE) -> dict[str, str]:
    """Empreintes des fichiers de `racine/archive/`, hors documents rédigés
    et hors cache de compilation (`__pycache__`)."""
    actuelles = {}
    for chemin in sorted((racine / "archive").rglob("*")):
        relatif = chemin.relative_to(racine)
        if chemin.is_file() and relatif.as_posix() not in EXCLUS and CACHE not in relatif.parts:
            actuelles[relatif.as_posix()] = hashlib.sha256(chemin.read_bytes()).hexdigest()
    return actuelles


def test_manifeste_trie_et_sans_doublon():
    chemins = [ligne.split("  ", 1)[1] for ligne in MANIFESTE.read_text(encoding="utf-8").splitlines()]
    assert chemins == sorted(set(chemins))


def test_archive_conforme_au_manifeste():
    attendues = lire_manifeste()
    actuelles = empreintes_actuelles()
    manquants = sorted(set(attendues) - set(actuelles))
    ajoutes = sorted(set(actuelles) - set(attendues))
    modifies = sorted(c for c in set(attendues) & set(actuelles) if attendues[c] != actuelles[c])
    assert (manquants, ajoutes, modifies) == ([], [], [])


def copie_archive(tmp_path: Path) -> Path:
    """Copie d'`archive/` sous `tmp_path`, qui joue le rôle de racine."""
    shutil.copytree(ARCHIVE, tmp_path / "archive", ignore=shutil.ignore_patterns(CACHE))
    return tmp_path


def test_cache_de_compilation_ignore(tmp_path):
    """Un `__pycache__/*.pyc` sous `archive/` ne change pas les empreintes (#13)."""
    racine = copie_archive(tmp_path)
    avant = empreintes_actuelles(racine)
    cache = racine / "archive" / "v2.0" / "prototype" / CACHE
    cache.mkdir(parents=True, exist_ok=True)
    (cache / "x.cpython-312.pyc").write_bytes(b"\x00cache")
    assert empreintes_actuelles(racine) == avant


def test_ajout_hors_cache_detecte(tmp_path):
    """Un fichier ajouté hors `__pycache__`, même `.pyc`, reste détecté (#13)."""
    racine = copie_archive(tmp_path)
    avant = empreintes_actuelles(racine)
    for ajout in ("v2.0/prototype/ajout.py", "v2.0/prototype/ajout.pyc"):
        (racine / "archive" / ajout).write_bytes(b"ajout")
    ajoutes = sorted(set(empreintes_actuelles(racine)) - set(avant))
    assert ajoutes == ["archive/v2.0/prototype/ajout.py", "archive/v2.0/prototype/ajout.pyc"]
