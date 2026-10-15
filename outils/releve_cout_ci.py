"""Relevé du coût du noyau seul C dans des journaux du job « Tests » de la CI (#105).

**Objet.** L'issue #105 demande de relever C sur N exécutions au même commit
et de publier le minimum, la médiane et le maximum, avec l'image de
l'exécuteur (ADR 0003, point 4 : marge mesurée avant d'être fixée). Ce
script fait le relevé (CLAUDE.md, principe 7 des workflows : un contrôle
mécanique est un script).

**Entrées.** Un ou plusieurs chemins : un fichier est lu tel quel ; un
répertoire fournit ses fichiers `*.txt` (journaux bruts téléchargés de
GitHub Actions, un par job). Les horodatages en tête de ligne
(`2026-10-15T05:54:23.3663214Z `) sont retirés avant l'analyse.

**Extraction, par journal :**

- `run` : identifiant d'exécution lu dans le nom de fichier
  (`run_<run_id>_job_<job_id>.txt`), sinon absent ;
- `commit` : SHA imprimé par l'étape de checkout, ligne qui suit
  `git log -1 --format=%H` ; à défaut, ligne `fetch … +<sha>:refs/…` ; à
  défaut, la valeur de `--commit` ;
- `image` : ligne `ImageOS=<os> ImageVersion=<version>` de l'étape « Image de
  l'exécuteur » (publiée `<os> <version>`) ;
- `C` et ses répétitions : ligne
  `C = <x> ms par pas (répétitions : <r1>, …)` publiée par
  `tests/invariants/test_budget.py::test_cout_du_noyau_seul` (ms par pas
  mensuel, pour un pays ; moyenne sur 720 pas, meilleure de 5 répétitions).

**Refus** (code de sortie 2, message sur la sortie d'erreur) : aucun journal ;
un journal sans C, sans image, ou avec plusieurs lignes C ou image ; C
différent du minimum de ses répétitions ; un journal sans commit lisible
quand `--commit` n'est pas donné ; des journaux à commits différents, ou un
commit lu qui ne commence pas par `--commit` ; deux journaux au même run ; un
même fichier donné deux fois (chemins comparés après `Path.resolve()`).

**Sortie.** Un tableau par exécution (triées par run, les journaux sans run en
dernier, par chemin), puis le minimum, la médiane et le maximum de C et le
rapport max / min, sur l'ensemble et par image (images en ordre
lexicographique). Le commit affiché est le commit lu dans les journaux,
complet ; `--commit` n'est affiché que si aucun journal ne porte de commit.
`--json` remplace le texte par le même contenu en JSON.

Bibliothèque standard seulement ; n'importe ni `src/` ni `archive/`.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

HORODATAGE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z ?")
NOM_RUN = re.compile(r"run_(\d+)")
LIGNE_IMAGE = re.compile(r"^ImageOS=(\S+) ImageVersion=(\S+)$")
LIGNE_C = re.compile(
    r"^\s*C = (\d+(?:\.\d+)?) ms par pas \(répétitions : (\d+(?:\.\d+)?(?:, \d+(?:\.\d+)?)*)\)\s*$"
)
COMMANDE_SHA = "git log -1 --format=%H"
LIGNE_SHA = re.compile(r"^([0-9a-f]{40})$")
FETCH_SHA = re.compile(r"\sfetch\s.*\+([0-9a-f]{40}):refs/")
COMMIT_DECLARE = re.compile(r"^[0-9a-f]{7,40}$")


class JournalRefuse(ValueError):
    """Journal ou ensemble de journaux inexploitable ; le message dit pourquoi."""


@dataclass(frozen=True)
class Releve:
    """Relevé d'un journal. `run` vaut None si le nom de fichier ne le porte pas."""

    chemin: str
    run: int | None
    commit: str
    commit_source: str  # "journal" ou "--commit"
    image: str
    c_ms: float
    repetitions_ms: tuple[float, ...]


def lignes_sans_horodatage(texte: str) -> list[str]:
    return [HORODATAGE.sub("", ligne.rstrip("\r")) for ligne in texte.split("\n")]


def commit_du_journal(lignes: list[str]) -> str | None:
    """SHA du checkout : ligne après `git log -1 --format=%H`, sinon ligne de fetch."""
    for i, ligne in enumerate(lignes):
        if ligne.rstrip().endswith(COMMANDE_SHA) and i + 1 < len(lignes):
            trouve = LIGNE_SHA.match(lignes[i + 1].strip())
            if trouve:
                return trouve.group(1)
    for ligne in lignes:
        trouve = FETCH_SHA.search(ligne)
        if trouve:
            return trouve.group(1)
    return None


def lire_journal(chemin: Path, commit_declare: str | None = None) -> Releve:
    """Extrait le relevé d'un journal ; lève JournalRefuse s'il est incomplet."""
    lignes = lignes_sans_horodatage(chemin.read_text(encoding="utf-8", errors="replace"))

    images = [m for m in (LIGNE_IMAGE.match(l) for l in lignes) if m]
    if not images:
        raise JournalRefuse(f"{chemin} : aucune ligne « ImageOS=… ImageVersion=… »")
    if len({m.groups() for m in images}) > 1:
        raise JournalRefuse(f"{chemin} : plusieurs images différentes")

    lignes_c = [m for m in (LIGNE_C.match(l) for l in lignes) if m]
    if not lignes_c:
        raise JournalRefuse(f"{chemin} : aucune ligne « C = … ms par pas (répétitions : …) »")
    if len(lignes_c) > 1:
        raise JournalRefuse(f"{chemin} : {len(lignes_c)} lignes C, relevé ambigu")
    c_texte, rep_texte = lignes_c[0].groups()
    c_ms = float(c_texte)
    repetitions = tuple(float(r) for r in rep_texte.split(", "))
    if c_ms != min(repetitions):
        raise JournalRefuse(
            f"{chemin} : C = {c_texte} n'est pas le minimum des répétitions ({rep_texte})"
        )

    commit = commit_du_journal(lignes)
    source = "journal"
    if commit is None:
        if commit_declare is None:
            raise JournalRefuse(f"{chemin} : aucun commit lisible ; le déclarer par --commit")
        commit, source = commit_declare, "--commit"
    elif commit_declare is not None and not commit.startswith(commit_declare):
        raise JournalRefuse(f"{chemin} : commit {commit} différent du commit déclaré {commit_declare}")

    trouve = NOM_RUN.search(chemin.name)
    return Releve(
        chemin=str(chemin),
        run=int(trouve.group(1)) if trouve else None,
        commit=commit,
        commit_source=source,
        image=" ".join(images[0].groups()),
        c_ms=c_ms,
        repetitions_ms=repetitions,
    )


def fichiers_des_chemins(chemins: list[Path]) -> list[Path]:
    """Journaux désignés par les chemins ; refuse un même fichier atteint deux fois."""
    fichiers: list[Path] = []
    for chemin in chemins:
        if chemin.is_dir():
            fichiers.extend(sorted(p for p in chemin.glob("*.txt") if p.is_file()))
        elif chemin.is_file():
            fichiers.append(chemin)
        else:
            raise JournalRefuse(f"{chemin} : ni fichier ni répertoire")
    if not fichiers:
        raise JournalRefuse("aucun journal")
    vus: dict[Path, Path] = {}
    for fichier in fichiers:
        absolu = fichier.resolve()
        if absolu in vus:
            raise JournalRefuse(f"{fichier} : même journal que {vus[absolu]}, donné deux fois")
        vus[absolu] = fichier
    return fichiers


def cle_canonique(releve: Releve) -> tuple:
    """Tri par run croissant ; journaux sans run en dernier, par chemin."""
    return (releve.run is None, releve.run or 0, releve.chemin)


def relever(chemins: list[Path], commit_declare: str | None = None) -> list[Releve]:
    """Relevés triés en ordre canonique ; refuse un ensemble incohérent."""
    if commit_declare is not None:
        commit_declare = commit_declare.lower()
        if not COMMIT_DECLARE.match(commit_declare):
            raise JournalRefuse(f"--commit {commit_declare} : 7 à 40 chiffres hexadécimaux attendus")
    releves = sorted(
        (lire_journal(f, commit_declare) for f in fichiers_des_chemins(chemins)), key=cle_canonique
    )
    commits = sorted({r.commit for r in releves if r.commit_source == "journal"})
    if len(commits) > 1:
        raise JournalRefuse("journaux à commits différents : " + ", ".join(commits))
    runs = [r.run for r in releves if r.run is not None]
    if len(runs) != len(set(runs)):
        raise JournalRefuse("plusieurs journaux pour un même run")
    return releves


def statistiques(valeurs: list[float]) -> dict:
    """Minimum, médiane, maximum et rapport max / min d'une série de C (ms par pas)."""
    mini, maxi = min(valeurs), max(valeurs)
    return {
        "n": len(valeurs),
        "minimum_ms": mini,
        "mediane_ms": statistics.median(valeurs),
        "maximum_ms": maxi,
        "rapport_max_min": maxi / mini if mini > 0 else None,
    }


def synthese(releves: list[Releve]) -> dict:
    # Un commit lu commence par --commit (vérifié par relever) : le lu, complet,
    # tient lieu du préfixe déclaré.
    lus = {r.commit for r in releves if r.commit_source == "journal"}
    commits = sorted(lus or {r.commit for r in releves})
    images = sorted({r.image for r in releves})
    return {
        "grandeur": (
            "C, coût du noyau seul (test_cout_du_noyau_seul) ; unité : ms par pas mensuel, "
            "pour un pays ; fenêtre : 720 pas ; statistique par exécution : moyenne, "
            "meilleure de 5 répétitions"
        ),
        "commit": commits[0] if len(commits) == 1 else commits,
        "executions": [asdict(r) for r in releves],
        "ensemble": statistiques([r.c_ms for r in releves]),
        "par_image": {i: statistiques([r.c_ms for r in releves if r.image == i]) for i in images},
    }


def format_rapport(rapport: float | None) -> str:
    return "—" if rapport is None else f"{rapport:.2f}"


def texte(resultat: dict) -> str:
    sortie = [f"Grandeur : {resultat['grandeur']}", f"Commit : {resultat['commit']}", ""]
    sortie.append("| Run | Commit | Image | C (ms par pas) | Répétitions (ms par pas) |")
    sortie.append("|---|---|---|---|---|")
    for r in resultat["executions"]:
        run = "—" if r["run"] is None else str(r["run"])
        commit = r["commit"][:7] + (" (--commit)" if r["commit_source"] == "--commit" else "")
        reps = ", ".join(f"{x:.4f}" for x in r["repetitions_ms"])
        sortie.append(f"| {run} | {commit} | {r['image']} | {r['c_ms']:.4f} | {reps} |")
    sortie.append("")
    sortie.append("| Population | N | Minimum | Médiane | Maximum | Max / min |")
    sortie.append("|---|---|---|---|---|---|")
    lignes = [("ensemble", resultat["ensemble"])] + [
        (f"image {i}", s) for i, s in resultat["par_image"].items()
    ]
    for nom, s in lignes:
        sortie.append(
            f"| {nom} | {s['n']} | {s['minimum_ms']:.4f} | {s['mediane_ms']:.4f} "
            f"| {s['maximum_ms']:.4f} | {format_rapport(s['rapport_max_min'])} |"
        )
    return "\n".join(sortie)


def main(arguments: list[str] | None = None) -> int:
    analyseur = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    analyseur.add_argument("chemins", nargs="+", type=Path, help="journaux ou répertoires de journaux (*.txt)")
    analyseur.add_argument(
        "--commit",
        help="commit attendu (7 à 40 chiffres hexadécimaux) ; attribué aux journaux qui n'en portent pas",
    )
    analyseur.add_argument("--json", action="store_true", help="sortie JSON au lieu du texte")
    args = analyseur.parse_args(arguments)
    try:
        resultat = synthese(relever(args.chemins, args.commit))
    except JournalRefuse as refus:
        print(f"refusé : {refus}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(resultat, ensure_ascii=False, indent=2))
    else:
        print(texte(resultat))
    return 0


if __name__ == "__main__":
    sys.exit(main())
