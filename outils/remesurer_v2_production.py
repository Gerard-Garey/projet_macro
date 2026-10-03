"""Remesure, sur le prototype v2.0, des faits de la fiche « production et stocks ».

Contrat : fiche `docs/blocs/production.md` § 9.7 (remesure S1, issue #34 ;
critères écrits par `macro` avant l'essai). Le script
exécute le prototype v2.0 **dans un processus séparé, sur une copie
temporaire**, jamais par import (CLAUDE.md, invariant 4) : `archive/` n'est ni
importée ni modifiée, et la copie est vérifiée contre le manifeste
`tests/invariants/archive_sha256.txt` avant toute exécution.

**Objet.** Sous le profil par défaut du prototype (valeurs par défaut de la
classe `Params`, sans le profil D1, non versé ; `reference_parameters()` est
inutilisable, `config/reference.json` étant absent), remesurer :

- le ratio stocks / ventes stationnaire ;
- la part des semaines où la borne `excess > 0` joue : `model.py` l. 923
  (monde) et l. 946 (économie fermée, `world is None`, branche exécutée),
  identiques ;
- la sensibilité de ce ratio à `mu_ema` (l. 1418) et à `lam_inv_2` (l. 644),
  multipliés par 0,5 et par 2.

**Branches.** `nominal` (aucune surcharge), `mu_x0.5`, `mu_x2`, `lam_x0.5`,
`lam_x2` : le pilote construit `Economy(Params(**kw), seed=graine)`, où `kw`
ne contient que la surcharge de la branche, égale au facteur multiplié par la
valeur par défaut lue dans `Params()` ; puis il appelle `step()` semaine par
semaine, `annees × 52` fois.

**Grandeurs** (par branche, par année de 52 semaines, par secteur : 0
alimentation, 1 énergie, 2 consommation, 3 équipement ; moyenne des semaines
de l'année ; une semaine passée en effondrement, `collapsed` vrai avant ou
après le pas, est exclue et décomptée) :

- `sinv_sur_q` : Sinv / Q, en semaines de ventes ; Sinv stock de produits
  finis en fin de semaine (l. 1000), Q = min(D, S) ventes de la semaine
  (l. 948) ;
- `sinv_sur_cible` : Sinv / (s* · Q̄), sans unité ; Sinv et Q̄ (l. 1418) en fin
  de semaine, soit les valeurs que la borne compare la semaine suivante ;
- `part_excess_positif` : part des semaines où excess = max(Sinv − s* · Q̄, 0)
  > 0 strictement, Sinv et Q̄ pris à l'ouverture de la semaine, comme l. 923
  et l. 946 ;
- `part_d_sup_s` : part des semaines où D > S (`_dbg[0]`, `_dbg[1]`, l. 1072) ;
- `rationnement_relatif` : (D − Q) / D, sans unité ;
- `y_sur_yhat` : Y / Ŷ, Y production effective (l. 680, lue dans
  `_diag_cu['Y']`, actif sous `wsps2`), Ŷ production planifiée (`_dbgL[2]`,
  l. 660).

Un rapport de dénominateur nul, négatif ou non fini, un rapport non fini, et
une indicatrice dont un opérande n'est pas fini, sont omis de la moyenne ; le
nombre de valeurs retenues et omises est publié par grandeur, secteur et année
(`effectifs`) ; une année sans valeur donne `null`.

**Critères, écrits avant l'essai** (fiche § 9.7 ; verdicts publiés quel que
soit le résultat) :

- **fenêtre** : années numérotées 31 à 60, soit t ∈ [30, 60[ ans ; la
  grandeur de fenêtre est la moyenne des moyennes annuelles ;
- **semaines exclues** : une semaine d'effondrement est exclue ; leur nombre
  dans la fenêtre est publié avec chaque verdict ; une année sans semaine
  valide rend le verdict « non évaluable » (en plus du § 9.7, restitution
  propre au script : le drapeau `effondrement_dans_fenetre` signale une
  fenêtre qui contient un effondrement ; le verdict se calcule quand même) ;
- **critère (i)** : branche nominale ; dans chacun des secteurs consommation
  (2) et équipement (3), Sinv/(s*·Q̄) < 0,99 et part des semaines avec
  excess > 0 inférieure à 5 %. La prédiction informative, issue du bloc seul,
  est d'environ 0,93 ; elle n'entre pas dans le seuil ;
- **critère (ii)** : pour chaque vitesse, écart relatif
  |r(× 2) − r(× 0,5)|/|r(× 0,5)| > 1e−6, avec r = Sinv/Q sur la même
  fenêtre, dans chacun des deux secteurs ; le verdict global exige les deux
  vitesses. r étant un rapport stock sur ventes, non négatif : r(× 0,5) =
  r(× 2) = 0 donne un écart nul (« non satisfait ») ; r(× 0,5) = 0 seul rend
  l'écart indéfini, et la vitesse « non évaluable » (restitution propre au
  script, décision du mainteneur du 03/10/2026) ;
- **statut du fait** : « remesuré le <date>, profil par défaut, non D1 ».
  Une fenêtre que la simulation ne couvre pas, ou une branche non remesurée
  (« non remesurable »), donne le verdict « non évaluable ».

**Exécution.** Le prototype importe `scipy` (`wealth_utility.py`), absent de
l'environnement du projet : le pilote tourne dans un environnement `uv`
isolé (`COMMANDE_PILOTE`), numpy à la version de l'environnement du projet,
scipy à la version déclarée. Si une branche ne s'exécute pas, l'exception
est consignée et la branche déclarée « non remesurable ».

Usage : `uv run python outils/remesurer_v2_production.py --sortie f.json
[--annees 60] [--graine 0] [--branches nominal mu_x2 …] [--archive dossier]
[--delai secondes]`. Code de sortie : 0 si toutes les branches sont
remesurées, 1 si une branche ne l'est pas, 2 si `--archive` n'est pas un
dossier existant du dépôt ou si les empreintes de la copie ne sont pas
conformes au manifeste (rien n'est exécuté, aucun JSON n'est écrit).
"""

import argparse
import datetime
import hashlib
import importlib.metadata
import inspect
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
ARCHIVE_DEFAUT = RACINE / "archive" / "v2.0" / "prototype"
MANIFESTE = RACINE / "tests" / "invariants" / "archive_sha256.txt"
CACHE = "__pycache__"
SEMAINES_PAR_AN = 52
SECTEURS = ("alimentation", "energie", "consommation", "equipement")
GRANDEURS = (
    "sinv_sur_q",
    "sinv_sur_cible",
    "part_excess_positif",
    "part_d_sup_s",
    "rationnement_relatif",
    "y_sur_yhat",
)
# Surcharges de chaque branche : paramètre de `Params` -> facteur appliqué à
# sa valeur par défaut.
BRANCHES = {
    "nominal": {},
    "mu_x0.5": {"mu_ema": 0.5},
    "mu_x2": {"mu_ema": 2.0},
    "lam_x0.5": {"lam_inv_2": 0.5},
    "lam_x2": {"lam_inv_2": 2.0},
}
# Critère (i) : années numérotées 31 à 60 (t dans [30 ans, 60 ans[), secteurs
# consommation et équipement.
FENETRE = (31, 60)
SECTEURS_CRITERES = ("consommation", "equipement")
SEUIL_SINV_SUR_CIBLE = 0.99
SEUIL_PART_EXCESS = 0.05
SEUIL_ECART_RELATIF = 1e-6
VITESSES = {"mu_ema": ("mu_x0.5", "mu_x2"), "lam_inv_2": ("lam_x0.5", "lam_x2")}
VERSION_SCIPY = "1.18.1"
MENTION = "remesuré le {date}, profil par défaut, non D1"
PROFIL = "valeurs par défaut de Params (prototype v2.0), sans le profil D1"


def rapport(num, den) -> list[float | None]:
    """Rapports terme à terme ; `None` (omis et compté) si le dénominateur est
    nul, négatif ou non fini, ou si le rapport n'est pas fini. Recopiée dans le
    pilote."""
    valeurs = [
        float(a) / float(b) if float(b) > 0 and math.isfinite(float(b)) else None
        for a, b in zip(num, den)
    ]
    return [v if v is not None and math.isfinite(v) else None for v in valeurs]


def indicatrice(gauche, droite) -> list[float | None]:
    """1.0 si gauche > droite, 0.0 sinon, terme à terme ; `None` (omise et
    comptée) si un opérande n'est pas fini. Recopiée dans le pilote."""
    return [
        float(float(g) > float(d)) if math.isfinite(float(g)) and math.isfinite(float(d)) else None
        for g, d in zip(gauche, droite)
    ]


# Pilote exécuté par `python -c` dans le répertoire temporaire qui contient la
# copie `prototype/` (importée comme paquet, comme `python -m prototype.simulate`).
# Arguments : surcharges (JSON), années, graine, fichier de sortie. `rapport`
# et `indicatrice` y sont recopiées depuis ce module (`inspect.getsource`).
PILOTE = r'''
import json, math, platform, sys
import numpy as np
import scipy
from prototype.model import Economy, Params, WEEKS, MODEL_VERSION

facteurs = json.loads(sys.argv[1])
annees, graine, sortie = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
defaut = vars(Params())
kw = {nom: float(defaut[nom]) * facteur for nom, facteur in facteurs.items()}
e = Economy(Params(**kw), seed=graine)
p = e.p


''' + inspect.getsource(rapport) + "\n\n" + inspect.getsource(indicatrice) + r'''

semaines = []
for _ in range(annees * WEEKS):
    sinv_ouverture = e.Sinv.copy()
    qbar_ouverture = e.Qbar.copy()
    effondre = e.collapsed
    e.step()
    if effondre or e.collapsed:
        semaines.append(None)
        continue
    D, S = e._dbg[0], e._dbg[1]
    Q = np.minimum(D, S)
    semaines.append(dict(
        sinv_sur_q=rapport(e.Sinv, Q),
        sinv_sur_cible=rapport(e.Sinv, p.s_star * e.Qbar),
        # excess = max(Sinv - s* Qbar, 0) > 0 (l. 923, l. 946), à l'ouverture.
        part_excess_positif=indicatrice(sinv_ouverture, p.s_star * qbar_ouverture),
        part_d_sup_s=indicatrice(D, S),
        rationnement_relatif=rapport(D - Q, D),
        y_sur_yhat=rapport(e._diag_cu["Y"], e._dbgL[2]),
    ))

with open(sortie, "w", encoding="utf-8") as f:
    json.dump(dict(
        surcharges=kw,
        semaines_par_an=WEEKS,
        version_modele=MODEL_VERSION,
        versions=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__),
        semaines=semaines,
    ), f, allow_nan=False)
'''


class EmpreintesNonConformes(Exception):
    """La copie du prototype diffère du manifeste d'`archive/`."""


class PrototypeIntrouvable(Exception):
    """`--archive` n'est pas un dossier existant du dépôt."""


def analyser_arguments(arguments: list[str] | None = None) -> argparse.Namespace:
    analyseur = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    analyseur.add_argument("--annees", type=int, default=60, help="durée simulée, en années de 52 semaines")
    analyseur.add_argument("--graine", type=int, default=0, help="graine passée à Economy")
    analyseur.add_argument(
        "--branches", nargs="+", choices=tuple(BRANCHES), default=list(BRANCHES),
        help="branches à exécuter (défaut : toutes)",
    )
    analyseur.add_argument("--sortie", type=Path, required=True, help="fichier JSON écrit")
    analyseur.add_argument("--archive", type=Path, default=ARCHIVE_DEFAUT, help="dossier du prototype v2.0")
    analyseur.add_argument(
        "--delai", type=float, default=None,
        help="délai maximal par branche, en secondes (défaut : 120 + 60 × années)",
    )
    args = analyseur.parse_args(arguments)
    if args.annees < 1:
        analyseur.error("--annees doit être au moins 1")
    if args.delai is None:
        args.delai = 120.0 + 60.0 * args.annees
    elif not args.delai > 0:
        analyseur.error("--delai doit être positif")
    # Ordre canonique, sans doublon.
    args.branches = [nom for nom in BRANCHES if nom in args.branches]
    return args


def empreintes(dossier: Path) -> dict[str, str]:
    """SHA-256 des fichiers de `dossier`, par chemin relatif, hors `__pycache__`."""
    resultat = {}
    for chemin in sorted(dossier.rglob("*")):
        relatif = chemin.relative_to(dossier)
        if chemin.is_file() and CACHE not in relatif.parts:
            resultat[relatif.as_posix()] = hashlib.sha256(chemin.read_bytes()).hexdigest()
    return resultat


def empreintes_attendues(manifeste: Path, prefixe: str) -> dict[str, str]:
    """Empreintes du manifeste sous `prefixe` (chemin depuis la racine du dépôt)."""
    attendues = {}
    for ligne in manifeste.read_text(encoding="utf-8").splitlines():
        empreinte, chemin = ligne.split("  ", 1)
        if chemin.startswith(prefixe + "/"):
            attendues[chemin[len(prefixe) + 1:]] = empreinte
    return attendues


def verifier_empreintes(copie: Path, prefixe: str, manifeste: Path = MANIFESTE) -> dict[str, str]:
    """Empreintes de la copie, si elles sont conformes au manifeste ; sinon
    `EmpreintesNonConformes` (fichier manquant, ajouté ou modifié)."""
    attendues = empreintes_attendues(manifeste, prefixe)
    actuelles = empreintes(copie)
    if not attendues:
        raise EmpreintesNonConformes(f"aucune empreinte sous {prefixe} dans {manifeste.name}")
    manquants = sorted(set(attendues) - set(actuelles))
    ajoutes = sorted(set(actuelles) - set(attendues))
    modifies = sorted(c for c in set(attendues) & set(actuelles) if attendues[c] != actuelles[c])
    if manquants or ajoutes or modifies:
        raise EmpreintesNonConformes(
            f"manquants {manquants}, ajoutés {ajoutes}, modifiés {modifies}"
        )
    return actuelles


def prefixe_du_manifeste(dossier: Path) -> str:
    """Chemin du dossier depuis la racine du dépôt, tel que l'écrit le manifeste ;
    `PrototypeIntrouvable` si le dossier n'existe pas ou est hors du dépôt."""
    absolu = dossier.resolve()
    if not absolu.is_dir():
        raise PrototypeIntrouvable(f"{dossier} : dossier inexistant")
    if not absolu.is_relative_to(RACINE):
        raise PrototypeIntrouvable(f"{dossier} : hors du dépôt {RACINE}")
    return absolu.relative_to(RACINE).as_posix()


def commande_pilote() -> list[str]:
    """Interpréteur du pilote : environnement `uv` isolé, numpy à la version
    du projet, scipy à la version déclarée (`VERSION_SCIPY`)."""
    return [
        "uv", "run", "--no-project", "--python", platform.python_version(),
        "--with", f"numpy=={importlib.metadata.version('numpy')}",
        "--with", f"scipy=={VERSION_SCIPY}",
        "python",
    ]


def lancer_branche(
    repertoire: Path, branche: str, annees: int, graine: int, delai: float,
    commande: list[str] | None = None,
) -> dict:
    """Exécute le pilote d'une branche dans `repertoire` (qui contient la copie
    `prototype/`) ; rend la sortie brute du pilote, ou lève `RuntimeError`."""
    sortie = repertoire / f"semaines_{branche}.json"
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    processus = subprocess.run(
        [*(commande or commande_pilote()), "-c", PILOTE,
         json.dumps(BRANCHES[branche]), str(annees), str(graine), str(sortie)],
        cwd=repertoire, env=env, capture_output=True, text=True, timeout=delai,
    )
    if processus.returncode != 0:
        raise RuntimeError(
            f"code de sortie {processus.returncode} : {processus.stderr.strip()[-2000:]}"
        )
    return json.loads(sortie.read_text(encoding="utf-8"))


def _moyenne(valeurs: list[float | None]) -> tuple[float | None, int, int]:
    """Moyenne des valeurs finies, nombre de valeurs retenues et omises
    (`None` : dénominateur nul ou négatif, ou rapport non fini)."""
    presentes = [v for v in valeurs if v is not None and math.isfinite(v)]
    moyenne = math.fsum(presentes) / len(presentes) if presentes else None
    return moyenne, len(presentes), len(valeurs) - len(presentes)


def agreger(semaines: list[dict | None], semaines_par_an: int = SEMAINES_PAR_AN) -> list[dict]:
    """Moyennes annuelles par grandeur et par secteur des relevés hebdomadaires,
    avec, par grandeur et secteur, le nombre de valeurs retenues et omises
    (`effectifs`)."""
    if len(semaines) % semaines_par_an:
        raise ValueError(f"{len(semaines)} semaines : pas un nombre entier d'années")
    annees = []
    for debut in range(0, len(semaines), semaines_par_an):
        bloc = semaines[debut:debut + semaines_par_an]
        valides = [s for s in bloc if s is not None]
        calculs = {
            secteur: {g: _moyenne([s[g][j] for s in valides]) for g in GRANDEURS}
            for j, secteur in enumerate(SECTEURS)
        }
        annees.append(dict(
            annee=debut // semaines_par_an + 1,
            semaines_valides=len(valides),
            semaines_exclues=len(bloc) - len(valides),
            secteurs={
                secteur: {g: m for g, (m, _, _) in par_g.items()}
                for secteur, par_g in calculs.items()
            },
            effectifs={
                secteur: {g: dict(retenues=r, omises=o) for g, (_, r, o) in par_g.items()}
                for secteur, par_g in calculs.items()
            },
        ))
    return annees


def moyenne_fenetre(annees: list[dict], grandeur: str, secteur: str, fenetre=FENETRE) -> float | None:
    """Moyenne des moyennes annuelles des années numérotées `fenetre[0]` à
    `fenetre[1]` incluses ; `None` si une année manque ou n'a pas de valeur."""
    par_annee = {a["annee"]: a["secteurs"][secteur][grandeur] for a in annees}
    valeurs = [par_annee.get(n) for n in range(fenetre[0], fenetre[1] + 1)]
    if any(v is None for v in valeurs):
        return None
    return math.fsum(valeurs) / len(valeurs)


def semaines_exclues_fenetre(annees: list[dict] | None, fenetre=FENETRE) -> int | None:
    """Semaines d'effondrement exclues dans les années de la fenêtre présentes ;
    `None` si la branche n'est pas remesurée."""
    if annees is None:
        return None
    return sum(a["semaines_exclues"] for a in annees if fenetre[0] <= a["annee"] <= fenetre[1])


def _effondrement(*nombres: int | None) -> bool:
    """Vrai si la fenêtre contient au moins une semaine d'effondrement exclue."""
    return any(n is not None and n > 0 for n in nombres)


def _annees_remesurees(branches: dict, nom: str) -> list[dict] | None:
    branche = branches.get(nom)
    return branche["annees"] if branche and branche["statut"] == "remesuré" else None


def verdict_i(branches: dict, fenetre=FENETRE) -> dict:
    """Critère (i), branche nominale."""
    texte = (
        "(i) branche nominale, années 31 à 60 ; dans chacun des secteurs "
        "consommation et équipement, Sinv/(s*·Q̄) < 0,99 et part des semaines "
        "avec excess > 0 inférieure à 5 % (prédiction informative ≈ 0,93, "
        "hors seuil)"
    )
    annees = _annees_remesurees(branches, "nominal")
    valeurs = {
        secteur: {
            g: moyenne_fenetre(annees, g, secteur, fenetre) if annees else None
            for g in ("sinv_sur_cible", "part_excess_positif")
        }
        for secteur in SECTEURS_CRITERES
    }
    if any(v is None for s in valeurs.values() for v in s.values()):
        verdict = "non évaluable"
    elif all(
        s["sinv_sur_cible"] < SEUIL_SINV_SUR_CIBLE and s["part_excess_positif"] < SEUIL_PART_EXCESS
        for s in valeurs.values()
    ):
        verdict = "satisfait"
    else:
        verdict = "non satisfait"
    exclues = semaines_exclues_fenetre(annees, fenetre)
    return dict(critere=texte, fenetre=list(fenetre), valeurs=valeurs, verdict=verdict,
                semaines_exclues=exclues, effondrement_dans_fenetre=_effondrement(exclues))


def ecart_relatif(a: float, b: float) -> float | None:
    """|b − a| / |a|, `a` étant la branche ×0,5 ; 0 si a = b = 0, `None`
    (écart indéfini, secteur « non évaluable ») si seul `a` est nul. r = Sinv/Q
    est un rapport stock sur ventes, non négatif."""
    if a == 0:
        return 0.0 if b == 0 else None
    return abs(b - a) / abs(a)


def verdict_ii(branches: dict, fenetre=FENETRE) -> dict:
    """Critère (ii), une vitesse à la fois."""
    texte = (
        "(ii) pour chaque vitesse, écart relatif |r(× 2) − r(× 0,5)|/|r(× 0,5)| "
        "> 1e−6, r = Sinv/Q sur les années 31 à 60, dans chacun des secteurs "
        "consommation et équipement ; le verdict global exige les deux vitesses"
    )
    par_vitesse = {}
    for vitesse, (moitie, double) in VITESSES.items():
        a_m, a_d = _annees_remesurees(branches, moitie), _annees_remesurees(branches, double)
        valeurs = {}
        evaluable, satisfait = True, True
        for secteur in SECTEURS_CRITERES:
            r_m = moyenne_fenetre(a_m, "sinv_sur_q", secteur, fenetre) if a_m else None
            r_d = moyenne_fenetre(a_d, "sinv_sur_q", secteur, fenetre) if a_d else None
            if r_m is None or r_d is None:
                evaluable = False
                valeurs[secteur] = dict(x0_5=r_m, x2=r_d, ecart_relatif=None)
                continue
            ecart = ecart_relatif(r_m, r_d)
            valeurs[secteur] = dict(x0_5=r_m, x2=r_d, ecart_relatif=ecart)
            if ecart is None:
                evaluable = False
                continue
            satisfait &= ecart > SEUIL_ECART_RELATIF
        verdict = ("satisfait" if satisfait else "non satisfait") if evaluable else "non évaluable"
        exclues = {
            moitie: semaines_exclues_fenetre(a_m, fenetre),
            double: semaines_exclues_fenetre(a_d, fenetre),
        }
        par_vitesse[vitesse] = dict(
            valeurs=valeurs, verdict=verdict, semaines_exclues=exclues,
            effondrement_dans_fenetre=_effondrement(*exclues.values()),
        )
    verdicts = {v["verdict"] for v in par_vitesse.values()}
    if "non évaluable" in verdicts:
        global_ = "non évaluable"
    else:
        global_ = "satisfait" if verdicts == {"satisfait"} else "non satisfait"
    return dict(
        critere=texte, fenetre=list(fenetre), vitesses=par_vitesse, verdict=global_,
        effondrement_dans_fenetre=any(v["effondrement_dans_fenetre"] for v in par_vitesse.values()),
    )


def rediger(contexte: dict, branches: dict, fenetre=FENETRE) -> dict:
    """Document JSON complet : contexte, branches, verdicts des critères."""
    return dict(
        contexte=contexte,
        branches=branches,
        criteres=dict(i=verdict_i(branches, fenetre), ii=verdict_ii(branches, fenetre)),
    )


def _sans_infini(x):
    """Remplace les flottants non finis par `None` (JSON strict)."""
    if isinstance(x, float) and not math.isfinite(x):
        return None
    if isinstance(x, dict):
        return {k: _sans_infini(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_sans_infini(v) for v in x]
    return x


def ecrire(document: dict, chemin: Path) -> None:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(
        json.dumps(_sans_infini(document), ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def remesurer(args: argparse.Namespace, commande: list[str] | None = None) -> dict:
    """Copie, vérification des empreintes, une exécution par branche, agrégation."""
    prefixe = prefixe_du_manifeste(args.archive)
    branches = {}
    versions = None
    version_modele = None
    with tempfile.TemporaryDirectory(prefix="remesure_v2_") as temporaire:
        repertoire = Path(temporaire)
        copie = repertoire / "prototype"
        shutil.copytree(args.archive, copie, ignore=shutil.ignore_patterns(CACHE))
        sha = verifier_empreintes(copie, prefixe)
        for nom in args.branches:
            try:
                brut = lancer_branche(repertoire, nom, args.annees, args.graine, args.delai, commande)
            except Exception as exc:  # consignée : le fait est déclaré non remesurable
                branches[nom] = dict(statut="non remesurable", exception=f"{type(exc).__name__}: {exc}")
                continue
            versions = brut["versions"]
            branches[nom] = dict(
                statut="remesuré",
                surcharges=brut["surcharges"],
                annees=agreger(brut["semaines"], brut["semaines_par_an"]),
            )
            version_modele = brut["version_modele"]
    contexte = dict(
        mention=MENTION.format(date=datetime.date.today().isoformat()),
        profil=PROFIL,
        graine=args.graine,
        annees=args.annees,
        prototype=prefixe,
        version_modele=version_modele,
        empreintes_sha256=sha,
        versions=dict(
            pilote=versions,
            script=dict(python=platform.python_version()),
        ),
        grandeurs=list(GRANDEURS),
        secteurs=list(SECTEURS),
    )
    return rediger(contexte, branches)


def main(arguments: list[str] | None = None) -> int:
    args = analyser_arguments(arguments)
    try:
        document = remesurer(args)
    except PrototypeIntrouvable as exc:
        print(f"prototype introuvable, rien n'est exécuté : {exc}", file=sys.stderr)
        return 2
    except EmpreintesNonConformes as exc:
        print(f"empreintes non conformes au manifeste, rien n'est exécuté : {exc}", file=sys.stderr)
        return 2
    ecrire(document, args.sortie)
    non_remesurees = [n for n, b in document["branches"].items() if b["statut"] != "remesuré"]
    for nom, branche in document["branches"].items():
        print(f"{nom} : {branche['statut']}")
    for cle, critere in document["criteres"].items():
        print(f"critère ({cle}) : {critere['verdict']}")
    print(f"écrit : {args.sortie}")
    return 1 if non_remesurees else 0


if __name__ == "__main__":
    sys.exit(main())
