"""Invariant : `archive/` n'est jamais modifiée (CLAUDE.md, invariant 4).

Le SHA-256 de chaque fichier de `archive/`, lu en binaire tel qu'il est dans
l'arbre de travail, est comparé au manifeste `archive_sha256.txt` (voisin de
ce fichier ; format de `sha256sum` : `<empreinte>  <chemin depuis la racine>`,
une ligne par fichier, triée par chemin). Un fichier manquant, ajouté ou
modifié fait échouer le test.

Sont exclus les deux documents rédigés d'`archive/`, tenus à jour avec le
projet : `README.md` et `faits_mesures_G_K.md`.

Le manifeste vaut pour des fichiers en fins de ligne LF (`.gitattributes`) ;
les PDF sont binaires. Il ne se régénère que sur décision du mainteneur, avec
la modification d'`archive/` qu'il consigne.
"""

import hashlib
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
ARCHIVE = RACINE / "archive"
MANIFESTE = Path(__file__).resolve().parent / "archive_sha256.txt"
EXCLUS = ("archive/README.md", "archive/faits_mesures_G_K.md")


def lire_manifeste() -> dict[str, str]:
    """Empreintes attendues, par chemin relatif à la racine du dépôt."""
    attendues = {}
    for ligne in MANIFESTE.read_text(encoding="utf-8").splitlines():
        empreinte, chemin = ligne.split("  ", 1)
        attendues[chemin] = empreinte
    return attendues


def empreintes_actuelles() -> dict[str, str]:
    """Empreintes des fichiers d'`archive/`, hors documents rédigés."""
    actuelles = {}
    for chemin in sorted(ARCHIVE.rglob("*")):
        relatif = chemin.relative_to(RACINE).as_posix()
        if chemin.is_file() and relatif not in EXCLUS:
            actuelles[relatif] = hashlib.sha256(chemin.read_bytes()).hexdigest()
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
