"""Listes des batteries de vérification tenues identiques (issue #28, décision P9).

Trois documents énoncent les batteries : `CLAUDE.md` (« Commandes »), la
liste `BATTERIES` de `.claude/workflows/circuit-technique.js` et `README.md`
(« Batteries de vérification »). Contrôle mécanique par script (principe 7
des workflows) : chaque liste est lue dans son fichier, dans son ordre, puis
comparée aux autres ; chaque batterie doit aussi être une étape de la CI.
"""

import re
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[2]


def bloc_apres(texte, ancre, fichier):
    """Lignes non vides du premier bloc ``` qui suit la première `ancre`."""
    debut = texte.find(ancre)
    assert debut >= 0, f"{fichier} : ancre « {ancre} » absente"
    bloc = re.search(r"^```[^\n]*\n(.*?)^```", texte[debut:], re.M | re.S)
    assert bloc, f"{fichier} : aucun bloc de code après « {ancre} »"
    return [ligne.strip() for ligne in bloc.group(1).splitlines() if ligne.strip()]


def batteries_claude():
    texte = (RACINE / "CLAUDE.md").read_text(encoding="utf-8")
    section = texte[texte.index("## Commandes"):]
    return bloc_apres(section, "Batteries de vérification", "CLAUDE.md")


def batteries_readme():
    texte = (RACINE / "README.md").read_text(encoding="utf-8")
    section = texte[texte.index("## Commandes"):]
    return bloc_apres(section, "Batteries de vérification", "README.md")


def batteries_workflow():
    texte = (RACINE / ".claude" / "workflows" / "circuit-technique.js").read_text(
        encoding="utf-8")
    liste = re.search(r"^const BATTERIES = \[(.*?)^\]", texte, re.M | re.S)
    assert liste, "circuit-technique.js : liste BATTERIES absente"
    return re.findall(r"'([^']*)'", liste.group(1))


def etapes_ci():
    """Commandes `run:` d'une ligne de la CI, `--locked` retiré."""
    texte = (RACINE / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    commandes = re.findall(r"^\s*run: (?![|>])(.+)$", texte, re.M)
    return [c.strip().replace("uv run --locked ", "uv run ") for c in commandes]


def test_listes_lues_non_vides_et_sans_doublon():
    for lire in (batteries_claude, batteries_workflow, batteries_readme):
        liste = lire()
        assert liste, lire.__name__
        assert len(set(liste)) == len(liste), (lire.__name__, liste)
        assert all(b.startswith("uv run ") for b in liste), (lire.__name__, liste)


def test_batteries_claude_et_workflow_identiques():
    assert batteries_workflow() == batteries_claude()


@pytest.mark.xfail(reason="#28 : README.md aligné par docwriter en fin de branche "
                          "(règle 9) ; marque retirée au commit docs: de README")
def test_batteries_readme_identiques():
    assert batteries_readme() == batteries_claude()


def test_chaque_batterie_est_une_etape_de_la_ci():
    manquantes = [b for b in batteries_claude() if b not in etapes_ci()]
    assert not manquantes, manquantes
