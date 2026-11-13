"""Contrôle statique des lectures des blocs (P58 ; ADR 0012, annotation du 13/11/2026, point 5).

Décision du mainteneur du 13/11/2026 (P58, P59) : les lectures de l'ouverture,
des positions et du registre sont contrôlées **statiquement**, sans filtre à
l'exécution. Le test lit l'arbre syntaxique de chaque module de
`src/nations/blocs/` (hors `__init__.py`) ; chaque module porte un seul bloc,
dont le radical est le nom du module.

1. **Relevé**, dans chaque méthode `phase_<étape>`, sur son paramètre de vue :
   `vue.ouverture.<champ>` (champ de `schema.CHAMPS`) ; `vue.grand_livre.position`,
   `montant_execute` et `montant_execute_ligne` ; `vue.dernier_prix()`,
   `vue.glissement()`, `vue.variation_sur_le_tour()` ; `vue.lire`,
   `vue.ecrire_pas`, `vue.ecrire_etat`, `vue.proposer`,
   `vue.declarer_montant_couvert`.
2. **Vérification** : pour chaque siège, l'ensemble relevé égale l'ensemble
   déclaré, source par source ; une méthode sans siège ou un siège sans méthode
   est un écart.
3. **Refus**, partout dans le module : `getattr`, `setattr`, `delattr`, `vars`,
   `globals`, `locals`, `eval`, `exec`, `__import__`, `__dict__` ; un nom qui
   n'est pas un littéral ; la vue, `vue.ouverture` ou `vue.grand_livre` hors
   d'un accès relevé ; `vue.grand_livre.ouverture`, `.echelle`,
   `.valeur_nette_stock`, `.valeur_nette_flux` ; l'importation d'un module de
   `nations.moteur` autre que `contrat_bloc` et `conversions`, de `tests` ou
   d'`outils` ; `global`, `nonlocal` et toute affectation dont la cible est un
   attribut.
4. **Hors du contrôle** : `vue.parametres` (lecture de paramètres, que B2 ne
   déclare pas).
5. **Le contrôle sait échouer** : un module fictif par forme refusée, et une
   déclaration en trop ou en moins.

Garde-fou (point 6 (a)) : aucun module de `src/` n'importe `tests` ni `outils`.
"""

import ast
import importlib
import types
from pathlib import Path

import pytest

from nations.etat import schema
from nations.moteur.contrat_bloc import (
    GRAND_LIVRE,
    LECTURES_DU_REGISTRE,
    OUVERTURE,
    REGISTRE,
    DeclarationDeBloc,
)

RACINE = Path(__file__).resolve().parents[2]
BLOCS = RACINE / "src" / "nations" / "blocs"
SRC = RACINE / "src"

# Méthodes de la vue relevées : nom → catégorie du siège.
METHODES_DE_LA_VUE = {"lire": "pas", "ecrire_pas": "ecrit", "ecrire_etat": "etat",
                      "proposer": "propose", "declarer_montant_couvert": "couvre"}
METHODES_DU_GRAND_LIVRE = ("position", "montant_execute", "montant_execute_ligne")
REFUSES_DU_GRAND_LIVRE = ("ouverture", "echelle", "valeur_nette_stock", "valeur_nette_flux")
NOMS_REFUSES = frozenset({"getattr", "setattr", "delattr", "vars", "globals", "locals", "eval",
                          "exec", "__import__"})
MOTEUR_ADMIS = frozenset({"nations.moteur.contrat_bloc", "nations.moteur.conversions"})
CATEGORIES = ("ouverture", "grand_livre", "registre", "pas", "ecrit", "etat", "propose",
              "couvre")


def declares(siege) -> dict[str, set[str]]:
    """Ensembles déclarés d'un siège, par catégorie."""
    sources = {OUVERTURE: "ouverture", GRAND_LIVRE: "grand_livre", REGISTRE: "registre"}
    rendus = {c: set() for c in CATEGORIES}
    for lecture in siege.lit:
        rendus[sources.get(lecture.source, "pas")].add(lecture.nom)
    rendus["ecrit"] = set(siege.ecrit)
    rendus["etat"] = set(siege.etat)
    rendus["propose"] = set(siege.propose)
    rendus["couvre"] = set(siege.couvre)
    return rendus


def _module_importe(noeud: ast.AST, paquet: str) -> list[str]:
    """Noms complets des modules qu'importe une instruction d'importation."""
    if isinstance(noeud, ast.Import):
        return [a.name for a in noeud.names]
    base = noeud.module or ""
    if noeud.level:
        parties = paquet.split(".")
        base = ".".join(parties[:len(parties) - noeud.level + 1] + ([base] if base else []))
    return [base] + [f"{base}.{a.name}" for a in noeud.names]


def _import_refuse(nom: str) -> bool:
    racine = nom.split(".")[0]
    if racine in ("tests", "outils"):
        return True
    if nom == "nations.moteur":
        return True
    if nom.startswith("nations.moteur."):
        return not any(nom == m or nom.startswith(m + ".") for m in MOTEUR_ADMIS)
    return False


def _cibles(noeud: ast.AST) -> list[ast.AST]:
    """Cibles d'affectation d'un nœud (affectations, boucles, `with`, compréhensions)."""
    if isinstance(noeud, ast.Assign):
        return list(noeud.targets)
    if isinstance(noeud, (ast.AugAssign, ast.AnnAssign)):
        return [noeud.target]
    if isinstance(noeud, (ast.For, ast.AsyncFor, ast.comprehension)):
        return [noeud.target]
    if isinstance(noeud, (ast.With, ast.AsyncWith)):
        return [i.optional_vars for i in noeud.items if i.optional_vars is not None]
    return []


def _litteral(appel: ast.Call) -> str | None:
    if appel.args and isinstance(appel.args[0], ast.Constant) and type(
            appel.args[0].value) is str:
        return appel.args[0].value
    return None


def _relever_methode(fonction: ast.FunctionDef, parents: dict) -> tuple[dict, list[str]]:
    """Relevé d'une méthode `phase_<étape>` sur son paramètre de vue, et écarts de forme."""
    releve = {c: set() for c in CATEGORIES}
    ecarts = []
    if len(fonction.args.args) < 2:
        return releve, [f"{fonction.name} : paramètre de vue absent"]
    vue = fonction.args.args[1].arg
    for noeud in ast.walk(fonction):
        if not (isinstance(noeud, ast.Name) and noeud.id == vue):
            continue
        ligne = f"{fonction.name}, ligne {noeud.lineno}"
        p1 = parents.get(noeud)
        if not isinstance(noeud.ctx, ast.Load) or not (
                isinstance(p1, ast.Attribute) and p1.value is noeud):
            ecarts.append(f"{ligne} : la vue utilisée hors d'un accès relevé")
            continue
        p2 = parents.get(p1)
        if p1.attr == "ouverture":
            if isinstance(p2, ast.Attribute) and p2.value is p1 and isinstance(p2.ctx, ast.Load):
                if p2.attr not in schema.CHAMPS:
                    ecarts.append(f"{ligne} : champ d'ouverture inconnu {p2.attr!r}")
                releve["ouverture"].add(p2.attr)
            else:
                ecarts.append(f"{ligne} : vue.ouverture utilisée hors d'un accès relevé")
        elif p1.attr == "grand_livre":
            if isinstance(p2, ast.Attribute) and p2.attr in REFUSES_DU_GRAND_LIVRE:
                ecarts.append(f"{ligne} : vue.grand_livre.{p2.attr} refusée")
            elif (isinstance(p2, ast.Attribute) and p2.attr in METHODES_DU_GRAND_LIVRE
                  and isinstance(parents.get(p2), ast.Call) and parents[p2].func is p2):
                nom = _litteral(parents[p2])
                if nom is None:
                    ecarts.append(f"{ligne} : nom non littéral dans vue.grand_livre.{p2.attr}")
                else:
                    releve["grand_livre"].add(nom)
            else:
                ecarts.append(f"{ligne} : vue.grand_livre utilisée hors d'un accès relevé")
        elif p1.attr == "parametres":
            if not (isinstance(p2, ast.Attribute) and p2.value is p1):
                ecarts.append(f"{ligne} : vue.parametres hors d'un accès à une table")
        elif p1.attr in LECTURES_DU_REGISTRE or p1.attr in METHODES_DE_LA_VUE:
            if not (isinstance(p2, ast.Call) and p2.func is p1):
                ecarts.append(f"{ligne} : vue.{p1.attr} hors d'un appel")
            elif p1.attr in LECTURES_DU_REGISTRE:
                releve["registre"].add(p1.attr)
            else:
                nom = _litteral(p2)
                if nom is None:
                    ecarts.append(f"{ligne} : nom non littéral dans vue.{p1.attr}")
                else:
                    releve[METHODES_DE_LA_VUE[p1.attr]].add(nom)
        else:
            ecarts.append(f"{ligne} : accès inconnu vue.{p1.attr}")
    return releve, ecarts


def analyser(texte: str, radical: str, declaration: DeclarationDeBloc | None) -> list[str]:
    """Écarts du module de bloc `radical` (texte source) à sa déclaration ; liste vide si
    conforme. `declaration` : celle du bloc du module (`None` si le module n'en porte pas)."""
    arbre = ast.parse(texte)
    parents = {enfant: noeud for noeud in ast.walk(arbre) for enfant in ast.iter_child_nodes(noeud)}
    paquet = f"nations.blocs.{radical}"
    ecarts = []
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Name) and noeud.id in NOMS_REFUSES:
            ecarts.append(f"ligne {noeud.lineno} : {noeud.id} refusé")
        elif isinstance(noeud, ast.Attribute) and noeud.attr == "__dict__":
            ecarts.append(f"ligne {noeud.lineno} : accès à __dict__ refusé")
        elif isinstance(noeud, (ast.Global, ast.Nonlocal)):
            ecarts.append(f"ligne {noeud.lineno} : {type(noeud).__name__.lower()} refusé")
        elif isinstance(noeud, (ast.Import, ast.ImportFrom)):
            for nom in _module_importe(noeud, paquet):
                if _import_refuse(nom):
                    ecarts.append(f"ligne {noeud.lineno} : importation de {nom} refusée")
        for cible in _cibles(noeud):
            for sous in ast.walk(cible):
                if isinstance(sous, ast.Attribute):
                    ecarts.append(f"ligne {sous.lineno} : affectation à un attribut refusée")
    if declaration is None:
        return ecarts + ["aucun bloc déclaré dans le module"]
    if declaration.radical != radical:
        ecarts.append(f"radical {declaration.radical!r} : {radical!r} (nom du module) attendu")
    methodes = [n for classe in ast.walk(arbre) if isinstance(classe, ast.ClassDef)
                for n in classe.body if isinstance(n, ast.FunctionDef)
                and n.name.startswith("phase_")]
    if len({parents[m] for m in methodes}) > 1:
        ecarts.append("méthodes d'étape dans plusieurs classes : un seul bloc par module")
    sieges = {s.etape: s for s in declaration.sieges}
    vues = set()
    for methode in methodes:
        etape = methode.name.removeprefix("phase_")
        vues.add(etape)
        releve, formes = _relever_methode(methode, parents)
        ecarts += formes
        if etape not in sieges:
            ecarts.append(f"{methode.name} : méthode sans siège")
            continue
        attendus = declares(sieges[etape])
        for categorie in CATEGORIES:
            for nom in sorted(releve[categorie] - attendus[categorie]):
                ecarts.append(f"{methode.name} : {categorie} {nom!r} faite, non déclarée")
            for nom in sorted(attendus[categorie] - releve[categorie]):
                ecarts.append(f"{methode.name} : {categorie} {nom!r} déclarée, jamais faite")
    for etape in sieges:
        if etape not in vues:
            ecarts.append(f"siège {etape} sans méthode phase_{etape}")
    return ecarts


def declaration_du_module(module: types.ModuleType, radical: str) -> DeclarationDeBloc | None:
    """Déclaration de l'unique classe du module qui porte une `DeclarationDeBloc`."""
    trouvees = [c.declaration for c in vars(module).values() if isinstance(c, type)
                and type(c.__dict__.get("declaration")) is DeclarationDeBloc]
    if len(trouvees) > 1:
        raise AssertionError(f"{radical} : un seul bloc par module attendu")
    return trouvees[0] if trouvees else None


def analyser_texte(texte: str, radical: str = "prix") -> list[str]:
    """Analyse d'un module fictif : sa déclaration est lue en l'exécutant dans un module neuf."""
    module = types.ModuleType(f"nations.blocs.{radical}")
    exec(compile(texte, f"<{radical}>", "exec"), module.__dict__)  # module fictif d'essai
    return analyser(texte, radical, declaration_du_module(module, radical))


# --------------------------------------------------------------------------
# Les modules de src/nations/blocs/
# --------------------------------------------------------------------------


def modules_de_blocs() -> list[Path]:
    return sorted(p for p in BLOCS.glob("*.py") if p.name != "__init__.py")


def test_controle_statique_des_blocs_du_moteur():
    """Chaque module de `src/nations/blocs/` porte un seul bloc, dont le radical est le nom du
    module, et ses lectures, écritures et lignes faites égalent celles qu'il déclare."""
    ecarts = []
    for chemin in modules_de_blocs():
        radical = chemin.stem
        module = importlib.import_module(f"nations.blocs.{radical}")
        ecarts += [f"{radical} : {e}" for e in analyser(
            chemin.read_text(encoding="utf-8"), radical, declaration_du_module(module, radical))]
    assert ecarts == []


def imports_hors_de_src(chemin: Path) -> list[str]:
    """Importations de `tests` ou d'`outils` par un fichier."""
    rendus = []
    for noeud in ast.walk(ast.parse(chemin.read_text(encoding="utf-8"))):
        if isinstance(noeud, (ast.Import, ast.ImportFrom)):
            noms = ([a.name for a in noeud.names] if isinstance(noeud, ast.Import)
                    else [noeud.module or ""])
            rendus += [n for n in noms if n.split(".")[0] in ("tests", "outils")]
    return rendus


def test_aucun_module_de_src_n_importe_tests_ni_outils():
    """Garde-fou (annotation du 13/11/2026, point 6 (a)) : rien dans `src/` ne connaît les blocs
    d'essai, le générateur ni les doublures : aucune importation de `tests` ni d'`outils`."""
    ecarts = {str(p.relative_to(RACINE)): imports_hors_de_src(p) for p in SRC.rglob("*.py")}
    assert {k: v for k, v in ecarts.items() if v} == {}


def test_le_garde_fou_d_imports_sait_echouer(tmp_path):
    fichier = tmp_path / "f.py"
    fichier.write_text("import tests.invariants.socle_partiel\nfrom outils import x\n"
                       "import nations\n", encoding="utf-8")
    assert imports_hors_de_src(fichier) == ["tests.invariants.socle_partiel", "outils"]


# --------------------------------------------------------------------------
# Le contrôle sait échouer : modules fictifs
# --------------------------------------------------------------------------

CONFORME = '''
import math

from nations.moteur.contrat_bloc import DeclarationDeBloc, Lecture, Siege
from nations.moteur.conversions import par_pas


def marge(mu_prec, xi, lam, mu_bar, psi):
    return (1.0 - lam) * mu_prec + lam * (math.log(1.0 + mu_bar) + psi * xi)


class Prix:
    __slots__ = ()
    declaration = DeclarationDeBloc("prix", (
        Siege("5", ("p", "P", "xi"),
              (Lecture("ouverture", "IN_vol"), Lecture("ouverture", "mu_tilde"),
               Lecture("2", "IN_vol_etoile"), Lecture("2", "UC")),
              (), (), ("mu_tilde",)),
    ))

    def phase_5(self, vue):
        lam = par_pas(vue.parametres.prix.lambda_mu)
        xi = 1.0 - vue.ouverture.IN_vol / vue.lire("IN_vol_etoile")
        mu = marge(vue.ouverture.mu_tilde, xi, lam, vue.parametres.prix.mu_bar,
                   vue.parametres.prix.psi_xi)
        p = vue.lire("UC") * math.exp(mu)
        vue.ecrire_pas("p", p)
        vue.ecrire_pas("P", p)
        vue.ecrire_pas("xi", xi)
        vue.ecrire_etat("mu_tilde", mu)
'''


def test_un_module_conforme_passe():
    assert analyser_texte(CONFORME) == []


# (remplacement dans le module conforme, motif attendu d'un écart)
MUTATIONS = [
    ("xi = 1.0 - vue.ouverture.IN_vol", "xi = 1.0 - getattr(vue.ouverture, 'IN_vol')",
     "getattr refusé"),
    ("xi = 1.0 - vue.ouverture.IN_vol", "xi = 1.0 - vue.ouverture.__dict__['IN_vol']",
     "__dict__"),
    ("xi = 1.0 - vue.ouverture.IN_vol", "o = vue.ouverture\n        xi = 1.0 - o.IN_vol",
     "vue.ouverture utilisée hors d'un accès relevé"),
    ("        vue.ecrire_pas(\"xi\", xi)\n",
     "        vue.ecrire_pas(\"xi\", xi)\n        aide(vue)\n", "la vue utilisée hors"),
    ("        vue.ecrire_pas(\"xi\", xi)\n",
     "        vue.ecrire_pas(\"xi\", xi)\n        return vue\n", "la vue utilisée hors"),
    ("vue.lire(\"UC\")", "vue.lire(\"U\" + \"C\")", "nom non littéral dans vue.lire"),
    ("vue.ecrire_pas(\"xi\", xi)", "nom = \"xi\"\n        vue.ecrire_pas(nom, xi)",
     "nom non littéral dans vue.ecrire_pas"),
    ("vue.ecrire_pas(\"xi\", xi)", "vue.ecrire_pas(\"xi\", vue.grand_livre.echelle(\"banque\"))",
     "vue.grand_livre.echelle refusée"),
    ("vue.ecrire_pas(\"xi\", xi)", "vue.ecrire_pas(\"xi\", vue.grand_livre.ouverture(\"IN\"))",
     "vue.grand_livre.ouverture refusée"),
    ("vue.ecrire_pas(\"xi\", xi)",
     "vue.ecrire_pas(\"xi\", vue.grand_livre.valeur_nette_stock(\"etat\"))",
     "valeur_nette_stock refusée"),
    ("vue.ecrire_pas(\"xi\", xi)", "vue.ecrire_pas(\"xi\", vue.grand_livre.position(\"IN\"))",
     "grand_livre 'IN' faite, non déclarée"),
    ("vue.ecrire_pas(\"xi\", xi)", "vue.ecrire_pas(\"xi\", vue.glissement())",
     "registre 'glissement' faite, non déclarée"),
    ("vue.ecrire_pas(\"xi\", xi)", "vue.ecrire_pas(\"xi\", vue.ouverture.W)",
     "ouverture 'W' faite, non déclarée"),
    ("vue.ecrire_pas(\"xi\", xi)", "vue.ecrire_pas(\"xi\", vue.ouverture.S_banque)",
     "champ d'ouverture inconnu"),
    ("        vue.ecrire_pas(\"xi\", xi)\n", "", "ecrit 'xi' déclarée, jamais faite"),
    ("(Lecture(\"ouverture\", \"IN_vol\"),", "(Lecture(\"ouverture\", \"IN_vol\"), "
     "Lecture(\"ouverture\", \"K_vol\"),", "ouverture 'K_vol' déclarée, jamais faite"),
    ("Lecture(\"2\", \"UC\")),", "Lecture(\"2\", \"UC\"), Lecture(\"registre\", \"dernier_prix\")),",
     "registre 'dernier_prix' déclarée, jamais faite"),
    ("(), (), (\"mu_tilde\",)", "(\"4\",), (), (\"mu_tilde\",)", "propose '4' déclarée"),
    ("    def phase_5(self, vue):", "    def phase_4(self, vue):\n        return None\n\n"
     "    def phase_5(self, vue):", "phase_4 : méthode sans siège"),
    ("    def phase_5(self, vue):", "    def phase_6(self, vue):", "siège 5 sans méthode"),
    ("from nations.moteur.conversions import par_pas",
     "from nations.moteur.conversions import par_pas\nfrom nations.moteur import ordonnanceur",
     "importation de nations.moteur.ordonnanceur refusée"),
    ("from nations.moteur.conversions import par_pas",
     "from nations.moteur.conversions import par_pas\n"
     "from nations.moteur.parametres.prix import PRIX", "importation de nations.moteur.parametres"),
    # Importations placées dans une fonction jamais appelée : le module fictif s'exécute
    # sans les résoudre, le contrôle les lit dans l'arbre syntaxique.
    ("import math\n", "import math\n\n\ndef _jamais():\n    import tests.invariants\n",
     "importation de tests.invariants refusée"),
    ("import math\n", "import math\n\n\ndef _jamais():\n"
     "    from outils import etat_stationnaire\n", "importation de outils refusée"),
    ("import math\n", "import math\nimport nations.moteur\n",
     "importation de nations.moteur refusée"),
    ("import math\n", "import math\nfrom nations import moteur\n",
     "importation de nations.moteur refusée"),
    ("import math\n", "import math\nCOMPTEUR = 0\n\n\ndef compter():\n    global COMPTEUR\n"
     "    COMPTEUR += 1\n", "global refusé"),
    ("        vue.ecrire_pas(\"xi\", xi)\n",
     "        vue.ecrire_pas(\"xi\", xi)\n        self.dernier = xi\n",
     "affectation à un attribut refusée"),
    ("        vue.ecrire_pas(\"xi\", xi)\n",
     "        vue.ecrire_pas(\"xi\", xi)\n        Prix.memoire = xi\n",
     "affectation à un attribut refusée"),
    ("        vue.ecrire_pas(\"xi\", xi)\n",
     "        vue.ecrire_pas(\"xi\", xi)\n        exec(\"x = 1\")\n", "exec refusé"),
    ("        vue.ecrire_pas(\"xi\", xi)\n",
     "        vue.ecrire_pas(\"xi\", xi)\n        vue = None\n", "la vue utilisée hors"),
    ("        vue.ecrire_pas(\"xi\", xi)\n",
     "        vue.ecrire_pas(\"xi\", xi)\n        livre = vue.grand_livre\n",
     "vue.grand_livre utilisée hors d'un accès relevé"),
]


@pytest.mark.parametrize("avant, apres, motif", MUTATIONS,
                         ids=[m[2][:40] for m in MUTATIONS])
def test_le_controle_statique_sait_echouer(avant, apres, motif):
    """Une forme refusée, une lecture faite non déclarée, une déclaration jamais faite, une
    méthode sans siège ou un siège sans méthode font échouer le contrôle."""
    assert avant in CONFORME
    texte = CONFORME.replace(avant, apres, 1)
    texte = texte.replace("class Prix:", "def aide(v):\n    return v\n\n\nclass Prix:", 1)
    ecarts = analyser_texte(texte)
    assert any(motif in e for e in ecarts), ecarts


def test_module_sans_bloc_ou_de_radical_faux():
    assert analyser_texte("X = 1\n") == ["aucun bloc déclaré dans le module"]
    assert any("nom du module" in e for e in analyser_texte(CONFORME, radical="travail"))
