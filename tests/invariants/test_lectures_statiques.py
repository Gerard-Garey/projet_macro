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
3. **Liste blanche des importations** (P81 (b), #121), partout dans le module :
   un module de bloc n'importe que ce que `IMPORTATIONS_ADMISES` déclare, nom par
   nom (`from base import X`, `base` résolue contre `nations.blocs` pour une
   importation relative), et n'importe entier que `MODULES_ENTIERS_ADMIS`
   (`import math`). Tout le reste est refusé : un module de `nations` importé
   entier (`import nations.moteur.contrat_bloc`, `from nations.moteur import
   conversions`, `from . import travail`), l'étoile, `sys`, `builtins`,
   `operator`, `importlib`, `tests`, `outils`… Depuis `conversions`, la **liste
   fermée** `NOMS_DE_CONVERSIONS` (constat M2 de l'audit du rang 4, #112). Les
   noms natifs (`builtins`, importé implicitement) suivent la même règle : seuls
   ceux de `NATIFS_ADMIS` sont admis, comme nom quel qu'en soit l'usage.
4. **Refus d'accès par chaîne ou par introspection**, partout dans le module :
   `getattr`, `setattr`, `delattr`, `vars`, `globals`, `locals`, `eval`, `exec`,
   `__import__`, comme nom, comme attribut ou comme nom importé ; tout nom
   spécial (`__x__`, dont `__builtins__`), sauf l'affectation de `__slots__` ;
   tout attribut privé ou spécial (`_x`, dont `__getattribute__`, `__globals__`,
   `__dict__`) et tout attribut d'introspection des cadres, codes, générateurs et
   traces (`PREFIXES_D_INTROSPECTION`), y compris comme attribut d'un motif de
   classe (`case C(attr=…)`) ; `format` et `format_map` (une chaîne de format lit
   attributs et indices par leur nom) ; un nom de lecture qui n'est pas un
   littéral ; la vue, `vue.ouverture` ou `vue.grand_livre` hors d'un accès relevé ;
   `vue.grand_livre.ouverture`, `.echelle`, `.valeur_nette_stock`,
   `.valeur_nette_flux` ; `global`, `nonlocal` et toute affectation dont la cible
   est un attribut.
5. **Aucun recalcul de Γ^e** (critère de #61 ; ADR 0013, annotation du 14/11/2026,
   point 7) : Γ^e = `facteur_g` · f(π*) et π^{∗,pas} = f(π*) − 1 sont des grandeurs
   d'ouverture que la phase 0 calcule seule ; un bloc les lit (`Gamma_e`, `gamma_e`,
   `pi_etoile_pas`). Aucun nom admis ne les calcule (`nations.moteur.ouverture` hors de
   la liste blanche, `NOMS_DE_CONVERSIONS` inchangée). Est refusée la **reconstruction
   de f(π*) = (1 + π*)^{1/n_a}**, sur une grandeur qui **dépend de π*** :
   - `facteur_par_pas` (sous son nom ou renommé à l'importation) ;
   - `x ** e` ou `x **= e` dont la base en dépend et dont l'exposant n'est pas un entier
     littéral (`(1 + π*) ** 2` est admis) ; toute puissance dont l'exposant contient le
     logarithme d'une telle grandeur (`math.e ** (log(1 + π*)/n_a)`) ;
   - `math.exp`, `exp2`, `expm1` dont l'argument contient un appel `math.log`, `log1p`,
     `log2` ou `log10` sur une telle grandeur, ou un identifiant lié à un tel appel
     (`y = math.log(1 + π*)` puis `math.exp(y/n_a)`) ;
   - `math.pow` dont la base en dépend et dont l'exposant n'est pas un entier littéral ;
   - `math.sqrt` et `math.cbrt` sur une telle grandeur (racines).
   Une exponentielle ou un logarithme sans cette composition reste admis (S2 du bloc 6,
   tu* = tū·exp[ζ(ϱ_L − ϱ̄_L)], avec ϱ_L = (1 + i_L)/(1 + π*) − 1). `facteur_par_pas` et
   les fonctions surveillées de `math` ne s'emploient qu'appelés directement
   (`p = math.pow` refusé). Dépend de π* une expression qui contient un attribut
   `pi_etoile` (`vue.ouverture.pi_etoile`, `vue.parametres.banque_centrale.pi_etoile`) ou un
   identifiant marqué. Est marqué : la cible d'une affectation (`=`, annotée, augmentée,
   `:=`, `for`, compréhension, `with … as`, capture d'un `case`) d'une expression qui en
   dépend ; le paramètre dont la valeur par défaut en dépend ; le paramètre d'une
   fonction, méthode ou lambda du module appelée avec un argument qui en dépend (lambda
   liée à un nom ou appelée sur place ; nom lié à un appelable ou à une méthode par une
   affectation, `conv = convertir`, `m = self.convertir`, suivi) ; tout paramètre de tout
   appelable du module pour un appel indirect (`h[0](x)`, `d['c'](x)`, appel d'un nom qui
   n'est ni un appelable du module, ni natif, ni importé, ni une classe, comme un
   paramètre qui reçoit une fonction : marquage par excès) ; le nom d'une fonction ou d'une lambda qui rend ou produit une
   valeur qui en dépend. Fermeture d'un graphe des liaisons, sur les identifiants du module
   sans distinction de portée (un homonyme est marqué aussi, et les homonymes appelables
   sont réunis), en O(taille de l'arbre + appels + paramètres des définitions). **Hors du
   critère**, déclaré et fixé par `test_formes_hors_du_critere_de_gamma_e` : une valeur
   rangée dans un conteneur par une méthode (`t.append(π*)`) ; aucune affectation à un
   attribut n'est admise (point 4). La conversion linéaire d'une grandeur qui dépend de π*
   reste admise (BC6 convertit i_CB).
6. **π* lue dans l'état seulement** (réserve R2 de `monnaie`, rang 3 de J3-c ;
   ADR 0010 : tout bloc lit la cible en vigueur π*_t, variable d'état écrite par
   BC4, jamais la cible déclarée de la table, qui n'est que sa valeur initiale ;
   #91) : tout attribut `pi_etoile` qui n'est pas lu sur `<vue>.ouverture` est
   refusé, partout dans le module (`vue.parametres.banque_centrale.pi_etoile`,
   une table liée à un nom, `c.pi_etoile`, un paramètre de fonction,
   `p.banque_centrale.pi_etoile`, un motif de classe `case C(pi_etoile=…)`).
   `vue.ouverture.pi_etoile` reste soumise au relevé (point 2) et au point 5.
7. **Hors du contrôle** : `vue.parametres` (lecture de paramètres, que B2 ne
   déclare pas), sauf le point 6.
8. **Le contrôle sait échouer** : un module fictif par forme refusée, et une
   déclaration en trop ou en moins ; un essai par contournement connu (#121).

Garde-fou (point 6 (a)) : aucun module de `src/` n'importe `tests` ni `outils`.
"""

import ast
import dataclasses
import builtins
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
# Liste blanche des importations d'un module de bloc (P81 (b), #121) : liste fermée, toute
# importation absente est refusée. Chaque entrée est justifiée par son usage dans un bloc.
CONVERSIONS = "nations.moteur.conversions"
# Noms admis depuis `nations.moteur.conversions` (liste fermée, constat M2 de l'audit du rang 4,
# #112) : les deux conversions et les deux types qu'elles acceptent. Toute autre importation du
# module (lui-même, ou un nom qu'il réexporte, comme `PAS_PAR_AN`) est refusée : n_a ne se lit
# que par la vue (`vue.parametres.cadre`), et un taux ne se convertit que par ces deux fonctions.
NOMS_DE_CONVERSIONS = frozenset({"par_pas", "facteur_par_pas", "TauxDeFlux", "TauxDeCroissance"})
IMPORTATIONS_ADMISES = {
    # Annotations différées, sans effet à l'exécution (les trois blocs).
    "__future__": frozenset({"annotations"}),
    # La déclaration d'un bloc : ses trois classes et les trois sources d'une lecture autres
    # qu'une étape (ADR 0012, B2, B3). Ni les fonctions de l'ordonnanceur
    # (`methode_de_l_etape`), ni les réexportations (`dataclass`).
    "nations.moteur.contrat_bloc": frozenset({"DeclarationDeBloc", "Siege", "Lecture",
                                              "OUVERTURE", "REGISTRE", "GRAND_LIVRE"}),
    # Les conversions d'un taux annuel au pas (ADR 0013, F2).
    CONVERSIONS: NOMS_DE_CONVERSIONS,
}
# Modules importés entiers : `math` (exp, log des équations des prix et du travail), qui n'expose
# que des fonctions numériques pures et aucune voie vers un autre module.
MODULES_ENTIERS_ADMIS = frozenset({"math"})
# Noms natifs admis (le module `builtins`, importé implicitement, est soumis à la même liste
# blanche) : les conversions et constructeurs de types des équations et des annotations (`float`,
# `int`, `str`, `tuple`), les deux bornes du travail et de la production (`min`, `max`).
NATIFS_ADMIS = frozenset({"float", "int", "str", "tuple", "min", "max"})
# Noms natifs de Python 3.12 (`requires-python`, ADR 0003), liste figée et déclarée : les noms
# non spéciaux de `builtins` sous `python -S`, plus les six que `site` y ajoute (`copyright`,
# `credits`, `exit`, `help`, `license`, `quit`). Figée plutôt que lue par `dir(builtins)`, qui
# dépend de `site` et de l'interpréteur : le verdict du contrôle n'en dépend plus. Figée plutôt
# que remplacée par la règle « tout nom chargé non lié dans le module est refusé » : une liaison
# morte (`if False: type = 0`) ou postérieure à la lecture rend la lecture au natif, et seule la
# connaissance des noms natifs ferme ces formes. `test_liste_des_natifs_complete` vérifie
# qu'aucun natif de l'interpréteur n'y manque.
NATIFS = frozenset({
    "ArithmeticError", "AssertionError", "AttributeError", "BaseException",
    "BaseExceptionGroup", "BlockingIOError", "BrokenPipeError", "BufferError", "BytesWarning",
    "ChildProcessError", "ConnectionAbortedError", "ConnectionError",
    "ConnectionRefusedError", "ConnectionResetError", "DeprecationWarning", "EOFError",
    "Ellipsis", "EncodingWarning", "EnvironmentError", "Exception", "ExceptionGroup", "False",
    "FileExistsError", "FileNotFoundError", "FloatingPointError", "FutureWarning",
    "GeneratorExit", "IOError", "ImportError", "ImportWarning", "IndentationError",
    "IndexError", "InterruptedError", "IsADirectoryError", "KeyError", "KeyboardInterrupt",
    "LookupError", "MemoryError", "ModuleNotFoundError", "NameError", "None",
    "NotADirectoryError", "NotImplemented", "NotImplementedError", "OSError", "OverflowError",
    "PendingDeprecationWarning", "PermissionError", "ProcessLookupError", "RecursionError",
    "ReferenceError", "ResourceWarning", "RuntimeError", "RuntimeWarning",
    "StopAsyncIteration", "StopIteration", "SyntaxError", "SyntaxWarning", "SystemError",
    "SystemExit", "TabError", "TimeoutError", "True", "TypeError", "UnboundLocalError",
    "UnicodeDecodeError", "UnicodeEncodeError", "UnicodeError", "UnicodeTranslateError",
    "UnicodeWarning", "UserWarning", "ValueError", "Warning", "ZeroDivisionError", "abs",
    "aiter", "all", "anext", "any", "ascii", "bin", "bool", "breakpoint", "bytearray",
    "bytes", "callable", "chr", "classmethod", "compile", "complex", "copyright", "credits",
    "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "exit", "filter",
    "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash", "help", "hex",
    "id", "input", "int", "isinstance", "issubclass", "iter", "len", "license", "list",
    "locals", "map", "max", "memoryview", "min", "next", "object", "oct", "open", "ord",
    "pow", "print", "property", "quit", "range", "repr", "reversed", "round", "set",
    "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super", "tuple", "type",
    "vars", "zip"
})
# Attributs d'introspection des cadres (`f_back`, `f_globals`), codes (`co_`), générateurs,
# coroutines et générateurs asynchrones (`gi_frame`, `cr_frame`, `ag_frame`) et traces
# (`tb_frame`) : sans aucun nom spécial, `gi_frame.f_back.f_globals` rend les globales de
# l'appelant du bloc.
PREFIXES_D_INTROSPECTION = ("f_", "co_", "gi_", "cr_", "ag_", "tb_")
# Méthodes de chaîne qui lisent attributs et indices par leur nom (`"{0.x[k]}".format(o)`).
FORMATS = frozenset({"format", "format_map"})
# Paquet contre lequel se résout une importation relative d'un module de bloc.
PAQUET_DES_BLOCS = "nations.blocs"
CATEGORIES = ("ouverture", "grand_livre", "registre", "pas", "ecrit", "etat", "propose",
              "couvre")
# Point 5 (#61) : la cible en vigueur π*, champ d'ouverture et paramètre du bloc 8 sous ce nom
# (ADR 0013, annotation du 14/11/2026, point 2), et la conversion géométrique qui en ferait
# f(π*), donc Γ^e = `facteur_g` · f(π*).
CIBLE = "pi_etoile"
CONVERSION_GEOMETRIQUE = "facteur_par_pas"
# Fonctions de `math` par lesquelles f(π*) = (1 + π*)^{1/n_a} se reconstruirait sans
# `facteur_par_pas` (C2 de `monnaie` ; R1 de l'audit de la reprise du rang 3 de J3-c) : racines
# sur une grandeur qui dépend de π* ; exponentielles d'un logarithme de π*
# (exp(log(1 + π*)/n_a)) ; `pow` à exposant non entier littéral. Une exponentielle sans
# logarithme de π* (S2 du bloc 6, tu* = tū·exp[ζ(ϱ_L − ϱ̄_L)]) est admise. Chacune ne s'emploie
# qu'appelée directement (`p = math.pow` refusé).
RACINES = frozenset({"sqrt", "cbrt"})
EXPONENTIELLES = frozenset({"exp", "exp2", "expm1"})
LOGARITHMES = frozenset({"log", "log1p", "log2", "log10"})
FONCTIONS_DE_MATH_SURVEILLEES = RACINES | EXPONENTIELLES | LOGARITHMES | {"pow"}
MOTIF_PUISSANCE = "puissance d'une grandeur qui dépend de π* refusée (recalcul de f(π*))"
MOTIF_MATH = "sur une grandeur qui dépend de π* refusé (recalcul de f(π*))"
# Point 6 (R2 de `monnaie`) : π* ne se lit que dans l'état d'ouverture.
MOTIF_CIBLE_HORS_DE_L_ETAT = ("π* lue hors de l'état d'ouverture refusée (tout bloc lit π*_t, "
                              "vue.ouverture.pi_etoile ; ADR 0010 ; R2 de monnaie)")


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


def _importations(noeud: ast.AST) -> list[tuple[str, str | None]]:
    """(module, nom) de chaque importation d'une instruction : nom `None` pour un module importé
    entier (`import base`), `X` pour `from base import X` (`*` pour l'étoile)."""
    if isinstance(noeud, ast.Import):
        return [(a.name, None) for a in noeud.names]
    base = noeud.module or ""
    if noeud.level:
        # Résolution contre le paquet du module (`nations.blocs`), non contre le module lui-même :
        # `from ..moteur import parametres` désigne `nations.moteur.parametres`. Au-delà de
        # `nations`, le nom garde ses points de tête, hors de toute liste blanche.
        parties = PAQUET_DES_BLOCS.split(".")
        if noeud.level > len(parties):
            base = "." * noeud.level + base
        else:
            base = ".".join(parties[:len(parties) - noeud.level + 1] + ([base] if base else []))
    return [(base, a.name) for a in noeud.names]


def _importation_admise(module: str, nom: str | None) -> bool:
    if nom is None:
        return module in MODULES_ENTIERS_ADMIS
    return nom in IMPORTATIONS_ADMISES.get(module, frozenset())


def _libelle(module: str, nom: str | None) -> str:
    """`base.X` pour `from base import X` (`...X` pour `from ... import X`), `base` sinon."""
    if nom is None:
        return module
    return f"{module}{'' if module.endswith('.') else '.'}{nom}"


def _special(nom: str) -> bool:
    return nom.startswith("__") and nom.endswith("__")


def _attribut_refuse(nom: str) -> str | None:
    """Motif du refus d'un nom d'attribut (attribut lu, écrit ou motif de classe), `None` si
    admis."""
    if nom in NOMS_REFUSES:
        return f"attribut {nom} refusé"
    if nom.startswith("_"):
        return f"attribut privé ou spécial {nom} refusé"
    if nom.startswith(PREFIXES_D_INTROSPECTION):
        return f"attribut d'introspection {nom} refusé"
    if nom in FORMATS:
        return f"attribut {nom} refusé (accès par chaîne)"
    return None


def _nom_refuse(noeud: ast.Name) -> str | None:
    """Motif du refus d'un nom, `None` si admis."""
    if noeud.id in NOMS_REFUSES:
        return f"{noeud.id} refusé"
    if _special(noeud.id):
        if noeud.id == "__slots__" and isinstance(noeud.ctx, ast.Store):
            return None
        return f"nom spécial {noeud.id} refusé"
    if noeud.id in NATIFS and noeud.id not in NATIFS_ADMIS:
        return f"nom natif {noeud.id} hors de la liste blanche"
    return None


def _cible_hors_de_l_etat(noeud: ast.Attribute) -> bool:
    """Point 6 (R2) : vrai si l'attribut `pi_etoile` n'est pas lu sur `<nom>.ouverture`."""
    valeur = noeud.value
    return not (isinstance(valeur, ast.Attribute) and valeur.attr == "ouverture"
                and isinstance(valeur.value, ast.Name))


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


def _signature_exacte(fonction: ast.FunctionDef) -> bool:
    """Signature `(self, vue)` exacte : ni paramètre positionnel seul, ni nommé seul, ni `*args`,
    ni `**kwargs`, ni valeur par défaut. Sinon la vue relevée (`args.args[1]`) peut ne pas être
    celle que passe l'ordonnanceur (`def phase_5(self, v, /, vue=None)`, constat M1 (b) de
    l'audit de #121)."""
    a = fonction.args
    return ([p.arg for p in a.args] == ["self", "vue"] and not a.posonlyargs
            and not a.kwonlyargs and a.vararg is None and a.kwarg is None and not a.defaults
            and not a.kw_defaults)


def _est_phase(nom: str | None) -> bool:
    return nom is not None and nom.startswith("phase_")


def _liaisons_de_phase(arbre: ast.AST, parents: dict) -> list[str]:
    """Écarts de liaison d'un nom `phase_*` (constat M1 (a) et (c) de l'audit de #121) : un nom
    `phase_*` ne se lie que par un `def` unique, sans décorateur, dans le corps d'une classe ;
    toute autre liaison (affectation, `AnnAssign`, importation, motif, `except … as`, paramètre,
    classe, `def` hors d'une classe ou répété) est refusée. Les classes ne portent ni
    décorateur ni mot-clé (`metaclass=`)."""
    ecarts = []
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.ClassDef):
            if noeud.decorator_list:
                ecarts.append(f"ligne {noeud.lineno} : décorateur de la classe {noeud.name} "
                              "refusé")
            if noeud.keywords:
                ecarts.append(f"ligne {noeud.lineno} : mot-clé de la classe {noeud.name} refusé")
            vus = set()
            for membre in noeud.body:
                if isinstance(membre, ast.FunctionDef) and _est_phase(membre.name):
                    if membre.name in vus:
                        ecarts.append(f"ligne {membre.lineno} : {membre.name} défini deux fois")
                    vus.add(membre.name)
                    if membre.decorator_list:
                        ecarts.append(f"ligne {membre.lineno} : décorateur de {membre.name} "
                                      "refusé")
        if isinstance(noeud, ast.FunctionDef):
            if _est_phase(noeud.name) and not isinstance(parents.get(noeud), ast.ClassDef):
                ecarts.append(f"ligne {noeud.lineno} : {noeud.name} défini hors du corps "
                              "d'une classe")
            continue
        if isinstance(noeud, ast.Name) and not isinstance(noeud.ctx, ast.Load):
            nom = noeud.id
        elif isinstance(noeud, ast.alias):
            nom = noeud.asname or noeud.name.split(".")[0]
        elif isinstance(noeud, (ast.AsyncFunctionDef, ast.ClassDef, ast.MatchAs, ast.MatchStar,
                                ast.ExceptHandler, ast.TypeVar, ast.ParamSpec,
                                ast.TypeVarTuple)):
            nom = noeud.name
        elif isinstance(noeud, ast.MatchMapping):
            nom = noeud.rest
        elif isinstance(noeud, ast.arg):
            nom = noeud.arg
        else:
            continue
        if _est_phase(nom):
            ecarts.append(f"ligne {noeud.lineno} : liaison de {nom} hors d'un def de classe "
                          "refusée")
    return ecarts


def _identifiants_cibles(cible: ast.AST) -> set[str]:
    """Noms liés par une cible d'affectation (n-uplets et étoiles compris)."""
    return {n.id for n in ast.walk(cible) if isinstance(n, ast.Name)}


def _identifiants_du_motif(motif: ast.AST) -> set[str]:
    """Noms liés par un motif de `case` (`case y`, `case [*y]`, `case {**y}`, `case C(x=y)`)."""
    noms = set()
    for n in ast.walk(motif):
        if isinstance(n, (ast.MatchAs, ast.MatchStar)) and n.name is not None:
            noms.add(n.name)
        elif isinstance(n, ast.MatchMapping) and n.rest is not None:
            noms.add(n.rest)
    return noms


def _depend_de_la_cible(expression: ast.AST | None, marques: set[str]) -> bool:
    """Vrai si l'expression contient un attribut `pi_etoile`, ou un nom ou un attribut marqué
    (nom qui dépend de π*, fonction ou méthode qui en rend une valeur)."""
    if expression is None:
        return False
    for n in ast.walk(expression):
        if isinstance(n, ast.Attribute) and (n.attr == CIBLE or n.attr in marques):
            return True
        if isinstance(n, ast.Name) and n.id in marques:
            return True
    return False


def _references(expression: ast.AST | None) -> tuple[bool, set[str]]:
    """(contient un attribut `pi_etoile`, identifiants référencés : noms et attributs)."""
    if expression is None:
        return False, set()
    cible, noms = False, set()
    for n in ast.walk(expression):
        if isinstance(n, ast.Attribute):
            cible = cible or n.attr == CIBLE
            noms.add(n.attr)
        elif isinstance(n, ast.Name):
            noms.add(n.id)
    return cible, noms


def _appelables(arbre: ast.AST) -> dict[str, list[ast.AST]]:
    """Appelables du module par nom : `def` (fonctions et méthodes, homonymes réunis) et lambdas
    liées à un nom ; un nom lié à un autre par une affectation de nom à nom
    (`conv = convertir`, `:=`, affectation annotée) ou à un attribut (`m = self.convertir`)
    partage ses appelables (classes d'union, sans ordre : un alias écrit avant sa source est
    suivi)."""
    parent: dict[str, str] = {}

    def racine(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    definitions: dict[str, list[ast.AST]] = {}
    for n in ast.walk(arbre):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            definitions.setdefault(n.name, []).append(n)
        paires = ()
        if isinstance(n, ast.Assign):
            paires = ((c, n.value) for c in n.targets)
        elif isinstance(n, (ast.AnnAssign, ast.NamedExpr)) and n.value is not None:
            paires = ((n.target, n.value),)
        for cible, valeur in paires:
            for nom in _identifiants_cibles(cible):
                if isinstance(valeur, ast.Lambda):
                    definitions.setdefault(nom, []).append(valeur)
                elif isinstance(valeur, (ast.Name, ast.Attribute)):
                    source = valeur.id if isinstance(valeur, ast.Name) else valeur.attr
                    parent[racine(nom)] = racine(source)
    par_classe: dict[str, list[ast.AST]] = {}
    for nom, liste in definitions.items():
        par_classe.setdefault(racine(nom), []).extend(liste)
    noms = set(parent) | set(definitions)
    return {nom: par_classe[racine(nom)] for nom in noms if racine(nom) in par_classe}


def _positionnels(definition: ast.AST) -> list[str]:
    """Paramètres positionnels, sans un `self` de tête : une méthode est appelée par un attribut
    (`self.m(x)`) ou par un alias lié (`m = self.m ; m(x)`), qui ne passent pas `self` ; un appel
    explicite `Classe.m(self, x)` décale les arguments au-delà des positionnels, d'où tous les
    paramètres (ci-dessous). `self` n'est jamais marqué."""
    a = definition.args
    noms = [p.arg for p in a.posonlyargs + a.args]
    return noms[1:] if noms[:1] == ["self"] else noms


def _tous_les_parametres(definition: ast.AST) -> set[str]:
    a = definition.args
    return ({p.arg for p in a.posonlyargs + a.args + a.kwonlyargs} | {
        p.arg for p in (a.vararg, a.kwarg) if p is not None}) - {"self"}


def _est_un_entier_litteral(n: ast.AST) -> bool:
    """Exposant entier écrit en littéral (`2`, `-1`), non booléen."""
    if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
        n = n.operand
    return isinstance(n, ast.Constant) and type(n.value) is int


def _noms_de_math(arbre: ast.AST) -> set[str]:
    """Noms sous lesquels `math` est importé entier (`import math`, `import math as m`)."""
    return {a.asname or a.name for n in ast.walk(arbre) if isinstance(n, ast.Import)
            for a in n.names if a.name == "math"}


def _fonction_de_math(n: ast.AST, modules_math: set[str]) -> str | None:
    """`f` si `n` est l'attribut `math.f`, sinon `None`."""
    if (isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)
            and n.value.id in modules_math):
        return n.attr
    return None


@dataclasses.dataclass(frozen=True)
class _Graphe:
    """Graphe des liaisons d'un module (point 5) : arêtes identifiant référencé → identifiants
    liés, et liste des liaisons (valeur, identifiants liés) dont partent les graines."""

    aretes: dict
    liaisons: list
    noeuds_d_appel: set


def _graphe_des_liaisons(arbre: ast.AST, parents: dict) -> _Graphe:
    """Graphe construit en un parcours de l'arbre. Un appel lie chaque argument à un **nœud
    d'appel** (appelable, position ou mot-clé), relié une seule fois aux paramètres de cette
    position de tous les appelables du même nom ; un appel indirect (`h[0](x)`, `d['c'](x)`,
    `f()(x)`, ou un nom qui n'est ni un appelable du module, ni natif, ni importé, ni une
    classe : paramètre qui reçoit une fonction, `def app(g, x): return g(x)`) lie ses arguments
    à tous les paramètres de tous les appelables du module : coût en
    O(taille de l'arbre + appels + paramètres des définitions), homonymes compris."""
    appelables = _appelables(arbre)
    tous_les_appelables = [n for n in ast.walk(arbre)
                           if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))]
    # Noms connus qui ne désignent pas un appelable du module : natifs, noms importés, classes.
    connus = NATIFS | {a.asname or a.name.split(".")[0] for n in ast.walk(arbre)
                       if isinstance(n, (ast.Import, ast.ImportFrom)) for a in n.names} | {
        n.name for n in ast.walk(arbre) if isinstance(n, ast.ClassDef)}
    aretes: dict[str, set[str]] = {}
    liaisons: list[tuple[ast.AST, set[str]]] = []
    noeuds_d_appel: set[str] = set()

    def lier(valeur: ast.AST | None, lies: set[str]) -> None:
        if valeur is None:
            return
        lies = lies - {"self"}
        liaisons.append((valeur, lies))
        for nom in _references(valeur)[1]:
            aretes.setdefault(nom, set()).update(lies)

    def noeud(cle: str, definitions: list[ast.AST], selon) -> str:
        """Nœud d'appel `cle` (préfixe `\\0`, hors des identifiants Python), relié une fois aux
        paramètres que `selon(definition)` désigne dans chaque définition."""
        nom = "\0" + cle
        if nom not in noeuds_d_appel:
            noeuds_d_appel.add(nom)
            aretes.setdefault(nom, set()).update(
                p for d in definitions for p in selon(d) if p != "self")
        return nom

    def appel(n: ast.Call) -> None:
        if isinstance(n.func, ast.Lambda):
            definitions, cle = [n.func], f"lambda@{id(n.func)}"
        elif isinstance(n.func, (ast.Name, ast.Attribute)) and (
                (nom := n.func.id if isinstance(n.func, ast.Name) else n.func.attr)
                in appelables):
            definitions, cle = appelables[nom], nom
        elif isinstance(n.func, ast.Attribute) or (
                isinstance(n.func, ast.Name) and n.func.id in connus):
            # Méthode d'un objet (`t.append`, `vue.lire`) ou nom connu : aucun appelable du
            # module n'est désigné.
            return
        else:
            definitions, cle = tous_les_appelables, "indirect"
        tous = noeud(f"{cle}*", definitions, _tous_les_parametres)
        for i, argument in enumerate(n.args):
            if isinstance(argument, ast.Starred) or cle == "indirect":
                lier(argument, {tous})
                continue
            lier(argument, {noeud(f"{cle}#{i}", definitions, lambda d, i=i: (
                [p[i]] if i < len(p := _positionnels(d)) else _tous_les_parametres(d)))})
        for mot in n.keywords:
            if mot.arg is None or cle == "indirect":
                lier(mot.value, {tous})
                continue
            lier(mot.value, {noeud(f"{cle}={mot.arg}", definitions, lambda d, k=mot.arg: (
                [k] if k in _tous_les_parametres(d) else _tous_les_parametres(d)))})

    noms_des_appelables: dict[int, set[str]] = {}
    for nom, definitions in appelables.items():
        for d in definitions:
            noms_des_appelables.setdefault(id(d), set()).add(nom)
    for n in ast.walk(arbre):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            a = n.args
            positionnels = a.posonlyargs + a.args
            for p, defaut in zip(positionnels[len(positionnels) - len(a.defaults):], a.defaults):
                lier(defaut, {p.arg})
            for p, defaut in zip(a.kwonlyargs, a.kw_defaults):
                lier(defaut, {p.arg})
            if isinstance(n, ast.Lambda):
                lier(n.body, noms_des_appelables.get(id(n), set()))
        elif isinstance(n, (ast.Return, ast.Yield, ast.YieldFrom)):
            englobante = parents.get(n)
            while englobante is not None and not isinstance(
                    englobante, (ast.FunctionDef, ast.AsyncFunctionDef)):
                englobante = parents.get(englobante)
            if englobante is not None:
                lier(n.value, {englobante.name})
        elif isinstance(n, ast.Assign):
            for c in n.targets:
                lier(n.value, _identifiants_cibles(c))
        elif isinstance(n, (ast.AnnAssign, ast.AugAssign, ast.NamedExpr)):
            lier(n.value, _identifiants_cibles(n.target))
        elif isinstance(n, (ast.For, ast.AsyncFor, ast.comprehension)):
            lier(n.iter, _identifiants_cibles(n.target))
        elif isinstance(n, ast.withitem) and n.optional_vars is not None:
            lier(n.context_expr, _identifiants_cibles(n.optional_vars))
        elif isinstance(n, ast.Match):
            for cas in n.cases:
                lier(n.subject, _identifiants_du_motif(cas.pattern))
        if isinstance(n, ast.Call):
            appel(n)
    return _Graphe(aretes, liaisons, noeuds_d_appel)


def _fermeture(graphe: _Graphe, est_graine) -> set[str]:
    """Identifiants atteints depuis les liaisons dont la valeur satisfait `est_graine`."""
    marques: set[str] = set()
    for valeur, lies in graphe.liaisons:
        if est_graine(valeur):
            marques |= lies
    a_suivre = list(marques)
    while a_suivre:
        for suivant in graphe.aretes.get(a_suivre.pop(), ()):
            if suivant not in marques:
                marques.add(suivant)
                a_suivre.append(suivant)
    return marques - graphe.noeuds_d_appel


def _contient_un_attribut_cible(valeur: ast.AST) -> bool:
    return any(isinstance(n, ast.Attribute) and n.attr == CIBLE for n in ast.walk(valeur))


def _marques_de_la_cible(arbre: ast.AST, parents: dict) -> set[str]:
    """Identifiants du module qui dépendent de π* (point 5) : fermeture du graphe des liaisons
    depuis les identifiants liés à une expression qui contient un attribut `pi_etoile`."""
    return _fermeture(_graphe_des_liaisons(arbre, parents), _contient_un_attribut_cible)


def _contient_un_log_de(valeur: ast.AST, marques: set[str], logarithmes: set[str],
                        modules_math: set[str]) -> bool:
    """Vrai si `valeur` contient un appel `math.log*` sur une grandeur marquée, ou un identifiant
    de `logarithmes` (lié à un tel appel)."""
    for n in ast.walk(valeur):
        if (isinstance(n, ast.Call) and _fonction_de_math(n.func, modules_math) in LOGARITHMES
                and any(_depend_de_la_cible(x, marques)
                        for x in n.args + [k.value for k in n.keywords])):
            return True
        if isinstance(n, ast.Name) and n.id in logarithmes:
            return True
    return False


def _recalculs_de_gamma_e(arbre: ast.AST, parents: dict) -> list[str]:
    """Écarts du point 5 : reconstruction de f(π*) = (1 + π*)^{1/n_a}, donc de Γ^e ou de
    π^{∗,pas}, dans un bloc (voir le docstring du module, point 5)."""
    alias = {a.asname or a.name for n in ast.walk(arbre) if isinstance(n, ast.ImportFrom)
             for module, nom in _importations(n) if module == CONVERSIONS
             for a in n.names if a.name == nom == CONVERSION_GEOMETRIQUE}
    modules_math = _noms_de_math(arbre)
    graphe = _graphe_des_liaisons(arbre, parents)
    marques = _fermeture(graphe, _contient_un_attribut_cible)
    # Identifiants liés au logarithme d'une grandeur marquée (y = math.log(1 + π*)).
    logarithmes = _fermeture(graphe, lambda v: _contient_un_log_de(v, marques, set(),
                                                                    modules_math))

    def log_de_la_cible(x: ast.AST) -> bool:
        return _contient_un_log_de(x, marques, logarithmes, modules_math)

    lire = "lire Gamma_e, gamma_e ou pi_etoile_pas, #61"
    ecarts = []
    for n in ast.walk(arbre):
        if isinstance(n, ast.Name) and n.id in alias and isinstance(n.ctx, ast.Load):
            appel = parents.get(n)
            if not (isinstance(appel, ast.Call) and appel.func is n):
                ecarts.append(f"ligne {n.lineno} : {n.id} employé hors d'un appel direct")
            elif any(_depend_de_la_cible(x, marques)
                     for x in appel.args + [k.value for k in appel.keywords]):
                ecarts.append(f"ligne {n.lineno} : {n.id} sur une grandeur qui dépend de π* "
                              f"refusé (recalcul de Γ^e ou de π^{{∗,pas}} : {lire})")
        elif isinstance(n, (ast.BinOp, ast.AugAssign)) and isinstance(n.op, ast.Pow):
            base, exposant = (n.left, n.right) if isinstance(n, ast.BinOp) else (n.target, n.value)
            if (_depend_de_la_cible(base, marques) and not _est_un_entier_litteral(exposant)) \
                    or log_de_la_cible(exposant):
                ecarts.append(f"ligne {n.lineno} : {MOTIF_PUISSANCE} ({lire})")
        elif (fonction := _fonction_de_math(n, modules_math)) in FONCTIONS_DE_MATH_SURVEILLEES:
            appel = parents.get(n)
            if not (isinstance(appel, ast.Call) and appel.func is n):
                ecarts.append(f"ligne {n.lineno} : math.{fonction} employé hors d'un appel "
                              "direct")
                continue
            arguments = appel.args + [k.value for k in appel.keywords]
            if fonction in RACINES:
                refus = any(_depend_de_la_cible(x, marques) for x in arguments)
            elif fonction == "pow":
                refus = (len(appel.args) == 2 and _depend_de_la_cible(appel.args[0], marques)
                         and not _est_un_entier_litteral(appel.args[1])) or any(
                    log_de_la_cible(x) for x in arguments) or (
                    len(appel.args) != 2 and any(_depend_de_la_cible(x, marques)
                                                 for x in arguments))
            elif fonction in EXPONENTIELLES:
                refus = any(log_de_la_cible(x) for x in arguments)
            else:
                refus = False
            if refus:
                ecarts.append(f"ligne {n.lineno} : math.{fonction} {MOTIF_MATH} ({lire})")
    return ecarts


def _relever_methode(fonction: ast.FunctionDef, parents: dict) -> tuple[dict, list[str]]:
    """Relevé d'une méthode `phase_<étape>` sur son paramètre de vue, et écarts de forme."""
    releve = {c: set() for c in CATEGORIES}
    ecarts = []
    if not _signature_exacte(fonction):
        return releve, [f"{fonction.name} : signature (self, vue) exacte attendue"]
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
    ecarts = []
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Name) and (motif := _nom_refuse(noeud)):
            ecarts.append(f"ligne {noeud.lineno} : {motif}")
        elif isinstance(noeud, ast.Attribute) and (motif := _attribut_refuse(noeud.attr)):
            ecarts.append(f"ligne {noeud.lineno} : {motif}")
        elif isinstance(noeud, ast.MatchClass):
            ecarts += [f"ligne {noeud.lineno} : motif de classe, {motif}"
                       for nom in noeud.kwd_attrs if (motif := _attribut_refuse(nom))]
            ecarts += [f"ligne {noeud.lineno} : motif de classe, {MOTIF_CIBLE_HORS_DE_L_ETAT}"
                       for nom in noeud.kwd_attrs if nom == CIBLE]
        elif isinstance(noeud, ast.alias) and noeud.name in NOMS_REFUSES:
            ecarts.append(f"ligne {noeud.lineno} : importation du nom {noeud.name} refusée")
        elif isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and _special(
                noeud.name):
            ecarts.append(f"ligne {noeud.lineno} : définition spéciale {noeud.name} refusée")
        elif isinstance(noeud, (ast.Global, ast.Nonlocal)):
            ecarts.append(f"ligne {noeud.lineno} : {type(noeud).__name__.lower()} refusé")
        elif isinstance(noeud, (ast.Import, ast.ImportFrom)):
            for module, nom in _importations(noeud):
                if not _importation_admise(module, nom):
                    ecarts.append(f"ligne {noeud.lineno} : importation de "
                                  f"{_libelle(module, nom)} refusée")
        if isinstance(noeud, ast.Attribute) and noeud.attr == CIBLE and _cible_hors_de_l_etat(
                noeud):
            ecarts.append(f"ligne {noeud.lineno} : {MOTIF_CIBLE_HORS_DE_L_ETAT}")
        for cible in _cibles(noeud):
            for sous in ast.walk(cible):
                if isinstance(sous, ast.Attribute):
                    ecarts.append(f"ligne {sous.lineno} : affectation à un attribut refusée")
    ecarts += _recalculs_de_gamma_e(arbre, parents)
    if declaration is None:
        return ecarts + ["aucun bloc déclaré dans le module"]
    if declaration.radical != radical:
        ecarts.append(f"radical {declaration.radical!r} : {radical!r} (nom du module) attendu")
    ecarts += _liaisons_de_phase(arbre, parents)
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
     "    from outils import etat_stationnaire\n",
     "importation de outils.etat_stationnaire refusée"),
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
    # Contournements par un autre nom (audit léger de #112, C1) : chacun est jugé par sa règle.
    ("import math\n", "import math\n\n\ndef _jamais():\n    import importlib\n"
     "    return importlib.import_module('nations.moteur.parametres.prix')\n",
     "importation de importlib refusée"),
    ("import math\n", "import math\n\n\ndef _jamais(o):\n    import builtins\n"
     "    return builtins.getattr(o, 'real')\n", "attribut getattr refusé"),
    ("import math\n", "import math\n\n\ndef _jamais(o):\n"
     "    from builtins import getattr as lire_attr\n    return lire_attr(o, 'real')\n",
     "importation du nom getattr refusée"),
    # `from base import X` jugé sur `base.X` (C2) : un module du moteur hors des admis.
    ("import math\n", "import math\nfrom nations.moteur import parametres\n",
     "importation de nations.moteur.parametres refusée"),
    # Importations relatives, résolues contre le paquet `nations.blocs` (audit de #112, A1) ;
    # placées dans une fonction jamais appelée, comme ci-dessus.
    ("import math\n", "import math\n\n\ndef _jamais():\n    from ..moteur import parametres\n",
     "importation de nations.moteur.parametres refusée"),
    ("import math\n", "import math\n\n\ndef _jamais():\n    from .. import moteur\n",
     "importation de nations.moteur refusée"),
    ("import math\n", "import math\n\n\ndef _jamais():\n"
     "    from ..moteur.parametres import prix\n",
     "importation de nations.moteur.parametres.prix refusée"),
    ("import math\n", "import math\n\n\ndef _jamais():\n"
     "    from ...outils import etat_stationnaire\n",
     "importation de ...outils.etat_stationnaire refusée"),
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


def test_from_moteur_import_juge_sur_base_point_nom():
    """C2, sous la liste blanche (P81 (b), #121) : `from base import X` est jugé sur `base.X`.
    Un module de `nations` importé entier est refusé, `contrat_bloc` compris (`from
    nations.moteur import contrat_bloc`) : seuls ses noms déclarés s'importent ; chaque nom hors
    de la liste est refusé sous son nom complet, et lui seul."""
    refuse = CONFORME.replace("import math\n", "import math\n\nfrom nations.moteur import "
                              "contrat_bloc, conversions, ordonnanceur\n", 1)
    assert [e for e in analyser_texte(refuse) if "importation" in e] == [
        "ligne 4 : importation de nations.moteur.contrat_bloc refusée",
        "ligne 4 : importation de nations.moteur.conversions refusée",
        "ligne 4 : importation de nations.moteur.ordonnanceur refusée"]
    noms = CONFORME.replace("import math\n", "import math\n\nfrom nations.moteur.contrat_bloc "
                            "import GRAND_LIVRE, methode_de_l_etape, REGISTRE, dataclass\n", 1)
    assert [e for e in analyser_texte(noms) if "importation" in e] == [
        "ligne 4 : importation de nations.moteur.contrat_bloc.methode_de_l_etape refusée",
        "ligne 4 : importation de nations.moteur.contrat_bloc.dataclass refusée"]


def test_importation_relative_resolue_contre_nations_blocs():
    """A1 : une importation relative est résolue contre `nations.blocs`, puis jugée par la liste
    blanche : `from ..moteur.contrat_bloc import Siege` et `from ..moteur.conversions import
    facteur_par_pas` sont admis ; `from ..moteur import contrat_bloc` (module entier) et `from .
    import travail` (un autre bloc, `nations.blocs.travail`) sont refusés."""
    admis = CONFORME.replace("import math\n", "import math\n\n\ndef _jamais():\n"
                             "    from ..moteur.contrat_bloc import Siege as S\n"
                             "    from ..moteur.conversions import facteur_par_pas\n"
                             "    return S, facteur_par_pas(S)\n", 1)
    assert analyser_texte(admis) == []
    refuse = CONFORME.replace("import math\n", "import math\n\n\ndef _jamais():\n"
                              "    from ..moteur import contrat_bloc\n"
                              "    from . import travail\n"
                              "    return contrat_bloc, travail\n", 1)
    assert [e for e in analyser_texte(refuse) if "importation" in e] == [
        "ligne 6 : importation de nations.moteur.contrat_bloc refusée",
        "ligne 7 : importation de nations.blocs.travail refusée"]


def test_module_sans_bloc_ou_de_radical_faux():
    assert analyser_texte("X = 1\n") == ["aucun bloc déclaré dans le module"]
    assert any("nom du module" in e for e in analyser_texte(CONFORME, radical="travail"))


# --------------------------------------------------------------------------
# Liste fermée des noms de `conversions` (constat M2 de l'audit du rang 4, #112)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("importation", [
    "from nations.moteur.conversions import PAS_PAR_AN",
    "from nations.moteur.conversions import par_pas, PAS_PAR_AN",
    "from nations.moteur.conversions import PAS_PAR_AN as N",
    "from nations.moteur.conversions import *",
    "import nations.moteur.conversions",
    "import nations.moteur.conversions as conv",
    "from nations.moteur import conversions",
    "from ..moteur.conversions import PAS_PAR_AN",
    "from ..moteur import conversions",
    "from nations.moteur.conversions.x import y",
])
def test_conversions_hors_de_la_liste_fermee_refusees(importation):
    """Depuis `nations.moteur.conversions`, seuls les noms de `NOMS_DE_CONVERSIONS` sont admis :
    un nom réexporté (`PAS_PAR_AN`, sous son nom ou renommé), l'étoile, le module entier (sous
    toute forme, relative comprise) sont refusés, ce qui ferme la lecture de n_a hors de la
    vue (placés dans une fonction jamais appelée : le module fictif s'exécute sans les
    résoudre ; l'étoile, admise au seul niveau du module, y est placée)."""
    if importation.endswith("*"):
        texte = CONFORME.replace("import math\n", f"import math\n{importation}\n", 1)
    else:
        texte = CONFORME.replace("import math\n", "import math\n\n\ndef _jamais():\n"
                                 f"    {importation}\n", 1)
    ecarts = [e for e in analyser_texte(texte) if "importation" in e]
    assert ecarts and all("nations.moteur.conversions" in e for e in ecarts), ecarts


def test_conversions_noms_de_la_liste_fermee_admis():
    """Les quatre noms de la liste fermée sont admis, sous leur nom ou renommés."""
    texte = CONFORME.replace(
        "from nations.moteur.conversions import par_pas\n",
        "from nations.moteur.conversions import (\n    TauxDeCroissance,\n    TauxDeFlux,\n"
        "    facteur_par_pas,\n    par_pas,\n)\n"
        "from nations.moteur.conversions import par_pas as pp\n", 1)
    assert analyser_texte(texte) == []
    assert NOMS_DE_CONVERSIONS == {"par_pas", "facteur_par_pas", "TauxDeFlux",
                                   "TauxDeCroissance"}


def test_les_blocs_du_moteur_n_importent_de_conversions_que_la_liste_fermee():
    """Mesure sur `src/nations/blocs/` : chaque nom importé de `conversions` par un bloc est dans
    la liste fermée (le contrôle d'ensemble le refuserait sinon) ; la liste ne contient que des
    noms définis ou réexportés par le module."""
    import nations.moteur.conversions as module

    assert all(hasattr(module, nom) for nom in NOMS_DE_CONVERSIONS)
    for chemin in modules_de_blocs():
        for noeud in ast.walk(ast.parse(chemin.read_text(encoding="utf-8"))):
            if isinstance(noeud, ast.ImportFrom) and noeud.module == CONVERSIONS:
                assert {a.name for a in noeud.names} <= NOMS_DE_CONVERSIONS, chemin.name


# --------------------------------------------------------------------------
# Liste blanche des importations (P81 (b), #121)
# --------------------------------------------------------------------------


def test_liste_blanche_fermee_et_declaree():
    """La liste blanche est fermée et déclarée : ses entrées sont exactement celles-ci, chaque
    nom admis existe dans son module, chaque module entier admis s'importe, chaque nom natif
    admis est un nom natif."""
    assert IMPORTATIONS_ADMISES == {
        "__future__": {"annotations"},
        "nations.moteur.contrat_bloc": {"DeclarationDeBloc", "Siege", "Lecture", "OUVERTURE",
                                        "REGISTRE", "GRAND_LIVRE"},
        "nations.moteur.conversions": NOMS_DE_CONVERSIONS,
    }
    assert MODULES_ENTIERS_ADMIS == {"math"}
    assert NATIFS_ADMIS == {"float", "int", "str", "tuple", "min", "max"}
    for module, noms in IMPORTATIONS_ADMISES.items():
        objet = importlib.import_module(module)
        assert all(hasattr(objet, nom) for nom in noms), module
    assert all(importlib.import_module(m) for m in MODULES_ENTIERS_ADMIS)
    assert NATIFS_ADMIS <= NATIFS


def test_liste_des_natifs_complete():
    """La liste figée `NATIFS` contient tout nom natif non spécial de l'interpréteur qui exécute
    le test (avec ou sans `site`) : un natif ajouté par une version de Python fait échouer ce
    test, non le contrôle des blocs."""
    assert {n for n in dir(builtins) if not _special(n)} <= NATIFS


def test_les_blocs_du_moteur_passent_la_liste_blanche():
    """Test positif : chaque module de `src/nations/blocs/` (les blocs 2 à 4 aujourd'hui, sans
    liste figée), tel qu'il est, passe le contrôle ; toutes ses importations sont dans la liste
    blanche."""
    assert modules_de_blocs()
    for chemin in modules_de_blocs():
        module = importlib.import_module(f"nations.blocs.{chemin.stem}")
        texte = chemin.read_text(encoding="utf-8")
        assert analyser(texte, chemin.stem, declaration_du_module(module, chemin.stem)) == []
        for noeud in ast.walk(ast.parse(texte)):
            if isinstance(noeud, (ast.Import, ast.ImportFrom)):
                assert all(_importation_admise(m, n) for m, n in _importations(noeud))


def _avant_la_classe(corps: str) -> tuple[tuple[str, str], ...]:
    """Remplacement qui insère `corps` avant la classe du module conforme."""
    return (("class Prix:", corps + "\n\nclass Prix:"),)


# Contournements connus (#121 : corps, commentaires des 13/11/2026), et ceux relevés en
# l'implémentant ou par l'audit (M1) : (nom, remplacements dans le module conforme, motif
# attendu d'un écart). Chacun est réel à l'exécution et était admis par le contrôle (mesures
# des comptes rendus de `coder`, rang 2 de J3-c). Les corps ajoutés avant la classe sont dans
# une fonction jamais appelée.
CONTOURNEMENTS = [
    ("builtins_indice", _avant_la_classe(
        "def _jamais(o):\n    return __builtins__['getattr'](o, 'real')\n"),
     "nom spécial __builtins__ refusé"),
    ("sys_modules", _avant_la_classe(
        "import sys\n\n\ndef _jamais():\n"
        "    return sys.modules['nations.moteur.parametres.cadre'].PAS_PAR_AN.valeur\n"),
     "importation de sys refusée"),
    ("operator_attrgetter", _avant_la_classe(
        "import operator\n\n\ndef _jamais(o):\n    return operator.attrgetter('real')(o)\n"),
     "importation de operator refusée"),
    ("getattribute", _avant_la_classe(
        "def _jamais(o):\n    return o.__getattribute__('real')\n"),
     "attribut privé ou spécial __getattribute__ refusé"),
    ("import_pointe_sous_nations", _avant_la_classe(
        "import nations.moteur.contrat_bloc\n\n\ndef _jamais():\n"
        "    return nations.moteur.parametres.cadre.PAS_PAR_AN.valeur\n"),
     "importation de nations.moteur.contrat_bloc refusée"),
    ("globals_d_une_conversion", _avant_la_classe(
        "def _jamais():\n    return par_pas.__globals__['PAS_PAR_AN'].valeur\n"),
     "attribut privé ou spécial __globals__ refusé"),
    # Relevés au rang 2 de J3-c.
    ("chaine_de_format", _avant_la_classe(
        "def _jamais():\n"
        "    return float('{0.__globals__[PAS_PAR_AN].valeur}'.format(par_pas))\n"),
     "attribut format refusé"),
    ("cadre_de_l_appelant", _avant_la_classe(
        "def _jamais():\n    def gen():\n"
        "        yield boite[0].gi_frame.f_back.f_back.f_globals\n"
        "    boite = [None]\n    boite[0] = gen()\n    return next(boite[0])\n"),
     "attribut d'introspection gi_frame refusé"),
    ("motif_de_classe", _avant_la_classe(
        "def _jamais(o):\n    match o:\n        case float(__class__=c):\n            return c\n"),
     "motif de classe, attribut privé ou spécial __class__ refusé"),
    ("natif_hors_liste", _avant_la_classe("def _jamais(o):\n    return type(o)\n"),
     "nom natif type hors de la liste blanche"),
    ("ouverture_de_fichier", _avant_la_classe(
        "def _jamais():\n    return open('p.txt').read()\n"),
     "nom natif open hors de la liste blanche"),
    ("definition_speciale", _avant_la_classe(
        "class _Lecteur:\n    def __getattr__(self, nom):\n        return nom\n"),
     "définition spéciale __getattr__ refusée"),
    # Contournements du relevé (constat M1 de l'audit de #121) : la vue réelle lue hors de
    # l'analyse. Chacun lisait `K_vol` sans le déclarer, la méthode appelée comme par
    # l'ordonnanceur.
    ("reaffectation_dans_la_classe", (
        ("class Prix:", "def _lire(self, v):\n    return v.ouverture.K_vol\n\n\nclass Prix:"),
        ("        vue.ecrire_etat(\"mu_tilde\", mu)\n",
         "        vue.ecrire_etat(\"mu_tilde\", mu)\n\n    phase_5 = _lire\n")),
     "liaison de phase_5 hors d'un def de classe refusée"),
    ("annotation_dans_la_classe", (
        ("class Prix:", "def _lire(self, v):\n    return v.ouverture.K_vol\n\n\nclass Prix:"),
        ("        vue.ecrire_etat(\"mu_tilde\", mu)\n",
         "        vue.ecrire_etat(\"mu_tilde\", mu)\n\n    phase_5: object = _lire\n")),
     "liaison de phase_5 hors d'un def de classe refusée"),
    ("def_repete", (
        ("        vue.ecrire_etat(\"mu_tilde\", mu)\n",
         "        vue.ecrire_etat(\"mu_tilde\", mu)\n\n    def phase_5(self, vue):\n"
         "        return None\n"),),
     "phase_5 défini deux fois"),
    ("positionnels_seuls", (
        ("    def phase_5(self, vue):", "    def phase_5(self, v, /, a=None, vue=None):"),),
     "phase_5 : signature (self, vue) exacte attendue"),
    ("decorateur_de_methode", (
        ("class Prix:", "def _deco(f):\n    def g(self, v):\n        k = v.ouverture.K_vol\n"
         "        return f(self, v)\n    return g\n\n\nclass Prix:"),
        ("    def phase_5(self, vue):", "    @_deco\n    def phase_5(self, vue):")),
     "décorateur de phase_5 refusé"),
    ("decorateur_de_classe", (
        ("class Prix:", "def _deco(c):\n    return c\n\n\n@_deco\nclass Prix:"),),
     "décorateur de la classe Prix refusé"),
    ("metaclasse", (
        ("class Prix:", "class _M(type):\n    pass\n\n\nclass Prix(metaclass=_M):"),),
     "mot-clé de la classe Prix refusé"),
    ("phase_hors_de_la_classe", (
        ("class Prix:", "def phase_7(self, vue):\n    return vue\n\n\nclass Prix:"),),
     "phase_7 défini hors du corps d'une classe"),
]


@pytest.mark.parametrize("remplacements, motif", [c[1:] for c in CONTOURNEMENTS],
                         ids=[c[0] for c in CONTOURNEMENTS])
def test_contournement_refuse(tmp_path, remplacements, motif):
    """Chaque contournement, écrit dans un module de bloc factice (`prix.py` sous `tmp_path`),
    fait échouer le contrôle."""
    texte = CONFORME
    for avant, apres in remplacements:
        assert avant in texte
        texte = texte.replace(avant, apres, 1)
    chemin = tmp_path / "prix.py"
    chemin.write_text(texte, encoding="utf-8")
    ecarts = analyser_texte(chemin.read_text(encoding="utf-8"), chemin.stem)
    assert any(motif in e for e in ecarts), ecarts


def test_slots_admis_en_affectation_seulement():
    """`__slots__ = ()` (contrat de bloc : aucun attribut d'instance) est le seul nom spécial
    admis, et seulement comme cible d'affectation."""
    assert "    __slots__ = ()\n" in CONFORME
    lu = CONFORME.replace("def marge(", "def _jamais():\n    return Prix.__slots__\n\n\n"
                          "def marge(", 1)
    assert any("__slots__ refusé" in e for e in analyser_texte(lu))
    nom = CONFORME.replace("def marge(", "def _jamais():\n    return __slots__\n\n\n"
                           "def marge(", 1)
    assert any("nom spécial __slots__ refusé" in e for e in analyser_texte(nom))


# --------------------------------------------------------------------------
# Aucun recalcul de Γ^e (point 5 ; critère de #61)
# --------------------------------------------------------------------------

# Le module conforme, la conversion géométrique et son type importés.
AVEC_FACTEUR = CONFORME.replace(
    "from nations.moteur.conversions import par_pas\n",
    "from nations.moteur.conversions import TauxDeCroissance, facteur_par_pas, par_pas\n", 1)
# Point d'insertion d'une forme dans `phase_5`, avant la première écriture.
AVANT_ECRITURE = "        vue.ecrire_pas(\"p\", p)\n"
MOTIF_GAMMA_E = "facteur_par_pas sur une grandeur qui dépend de π* refusé"

# (forme insérée dans `phase_5`, fonctions ajoutées au module) : chacune recalcule f(π*).
RECALCULS = [
    ("        f = facteur_par_pas(TauxDeCroissance(vue.ouverture.pi_etoile))\n", ""),
    ("        f = facteur_par_pas(vue.parametres.banque_centrale.pi_etoile)\n", ""),
    ("        c = vue.parametres.banque_centrale\n        f = facteur_par_pas(c.pi_etoile)\n", ""),
    ("        x = vue.ouverture.pi_etoile\n        y = 1.0 * x\n"
     "        f = facteur_par_pas(TauxDeCroissance(y))\n", ""),
    ("        y = 0.0\n        y += vue.ouverture.pi_etoile\n"
     "        f = facteur_par_pas(TauxDeCroissance(y))\n", ""),
    ("        if (y := vue.ouverture.pi_etoile) > -1.0:\n"
     "            f = facteur_par_pas(TauxDeCroissance(y))\n", ""),
    ("        for y in (vue.ouverture.pi_etoile,):\n"
     "            f = facteur_par_pas(TauxDeCroissance(y))\n", ""),
    ("        f = [facteur_par_pas(TauxDeCroissance(y)) for y in (vue.ouverture.pi_etoile,)]\n",
     ""),
    ("        f = facteur_par_pas(taux=TauxDeCroissance(vue.ouverture.pi_etoile))\n", ""),
    # Par une fonction du module : paramètre marqué à l'appel, ou valeur rendue marquée.
    ("        f = convertir(vue.ouverture.pi_etoile)\n",
     "def convertir(x):\n    return facteur_par_pas(TauxDeCroissance(x))\n"),
    ("        f = convertir(x=vue.ouverture.pi_etoile)\n",
     "def convertir(x):\n    return facteur_par_pas(TauxDeCroissance(x))\n"),
    ("        f = convertir(*(vue.ouverture.pi_etoile,))\n",
     "def convertir(x):\n    return facteur_par_pas(TauxDeCroissance(x))\n"),
    ("        f = facteur_par_pas(TauxDeCroissance(cible(vue.parametres)))\n",
     "def cible(p):\n    return p.banque_centrale.pi_etoile.valeur\n"),
    ("        f = facteur_par_pas(TauxDeCroissance(relais(cible(vue.parametres))))\n",
     "def cible(p):\n    return p.banque_centrale.pi_etoile.valeur\n\n\n"
     "def relais(x):\n    return x\n"),
    # Méthode du bloc appelée par `self`.
    ("        f = self.convertir(vue.ouverture.pi_etoile)\n", "METHODE"),
]
METHODE = ("    def convertir(self, x):\n"
           "        return facteur_par_pas(TauxDeCroissance(x))\n\n")


def _avec_forme(forme: str, fonctions: str) -> str:
    texte = AVEC_FACTEUR.replace(AVANT_ECRITURE, forme + AVANT_ECRITURE, 1)
    if fonctions == "LIT_LA_CIBLE":
        # Lecture de π* d'ouverture déclarée dans le siège de la phase 5 (forme admise).
        return texte.replace('(Lecture("ouverture", "IN_vol"),',
                             '(Lecture("ouverture", "IN_vol"), Lecture("ouverture", "pi_etoile"),',
                             1)
    if fonctions == "METHODE":
        return texte.replace("    def phase_5(self, vue):", METHODE + "    def phase_5(self, vue):",
                             1)
    if fonctions:
        return texte.replace("class Prix:", fonctions + "\n\nclass Prix:", 1)
    return texte


# Contournements relevés par l'audit du rang 3 (m1), désormais suivis : lambda, alias d'une
# fonction, valeur par défaut, capture d'un `case`.
RECALCULS += [
    ("        h = lambda x: facteur_par_pas(TauxDeCroissance(x))\n"
     "        f = h(vue.parametres.banque_centrale.pi_etoile.valeur)\n", ""),
    ("        f = (lambda x: facteur_par_pas(TauxDeCroissance(x)))(vue.ouverture.pi_etoile)\n",
     ""),
    ("        conv = convertir\n        f = conv(vue.ouverture.pi_etoile)\n",
     "def convertir(x):\n    return facteur_par_pas(TauxDeCroissance(x))\n"),
    ("        f = conv(vue.ouverture.pi_etoile)\n        conv = convertir\n",
     "def convertir(x):\n    return facteur_par_pas(TauxDeCroissance(x))\n"),
    ("        def k(y=vue.ouverture.pi_etoile):\n"
     "            return facteur_par_pas(TauxDeCroissance(y))\n        f = k()\n", ""),
    ("        def k(*, y=vue.ouverture.pi_etoile):\n"
     "            return facteur_par_pas(TauxDeCroissance(y))\n        f = k()\n", ""),
    ("        match vue.ouverture.pi_etoile:\n            case y:\n"
     "                f = facteur_par_pas(TauxDeCroissance(y))\n", ""),
    ("        match (vue.ouverture.pi_etoile,):\n            case (*y,):\n"
     "                f = facteur_par_pas(TauxDeCroissance(y[0]))\n", ""),
    # Fonction imbriquée : son retour marque son nom, non celui de la fonction englobante.
    ("        def interne():\n            return vue.ouverture.pi_etoile\n"
     "        f = facteur_par_pas(TauxDeCroissance(interne()))\n", ""),
]


@pytest.mark.parametrize("forme, fonctions", RECALCULS)
def test_recalcul_de_gamma_e_refuse(forme, fonctions):
    """Point 5 (critère de #61) : `facteur_par_pas` sur une grandeur qui dépend de π*, sous
    chaque forme de liaison déclarée, est refusé ; Γ^e et π^{∗,pas} ne se lisent que dans
    l'espace du pas."""
    ecarts = analyser_texte(_avec_forme(forme, fonctions))
    assert any(MOTIF_GAMMA_E in e for e in ecarts), ecarts


@pytest.mark.parametrize("forme, motif", [
    ("        g = facteur_par_pas\n", "facteur_par_pas employé hors d'un appel direct"),
    ("        g = (facteur_par_pas,)[0]\n", "facteur_par_pas employé hors d'un appel direct"),
])
def test_conversion_geometrique_hors_d_un_appel_direct_refusee(forme, motif):
    """Point 5 : `facteur_par_pas` ne se lie ni ne se passe (`g = facteur_par_pas`, puis
    `g(…)` échapperait au contrôle) ; il s'emploie appelé directement."""
    ecarts = analyser_texte(_avec_forme(forme, ""))
    assert any(motif in e for e in ecarts), ecarts


# π* lue dans l'état d'ouverture, seule forme admise (point 6, R2 de `monnaie`) : les formes
# refusées ci-dessous ne portent que le point 5 (et le relevé, la lecture n'y étant pas
# déclarée) ; les formes admises déclarent la lecture (`_avec_forme_lisant_la_cible`).
PI = "vue.ouverture.pi_etoile"
N_A_VUE = "vue.parametres.cadre.pas_par_an"


@pytest.mark.parametrize("forme, motif", [
    (f"        f = (1.0 + {PI}) ** (1.0 / {N_A_VUE})\n", MOTIF_PUISSANCE),
    (f"        f = (1.0 + {PI}) ** (1 / 12)\n", MOTIF_PUISSANCE),
    (f"        y = 1.0 + {PI}\n        y **= 0.5\n", MOTIF_PUISSANCE),
    (f"        f = math.e ** (math.log(1.0 + {PI}) / {N_A_VUE})\n", MOTIF_PUISSANCE),
    (f"        f = math.exp(math.log(1.0 + {PI}) / {N_A_VUE})\n", "math.exp " + MOTIF_MATH),
    (f"        f = math.exp(par_pas(TauxDeFlux(math.log1p({PI}))))\n", "math.exp " + MOTIF_MATH),
    (f"        y = math.log(1.0 + {PI})\n        f = math.expm1(y / {N_A_VUE})\n",
     "math.expm1 " + MOTIF_MATH),
    (f"        f = math.pow(1.0 + {PI}, 1.0 / {N_A_VUE})\n", "math.pow " + MOTIF_MATH),
    (f"        f = math.pow(1.0 + {PI}, 1 / 12)\n", "math.pow " + MOTIF_MATH),
    (f"        f = math.sqrt(1.0 + {PI})\n", "math.sqrt " + MOTIF_MATH),
    (f"        f = math.cbrt(1.0 + {PI})\n", "math.cbrt " + MOTIF_MATH),
    # R2 de l'audit de la reprise : une fonction surveillée de `math` s'emploie appelée
    # directement.
    (f"        p = math.pow\n        f = p(1.0 + {PI}, 0.5)\n",
     "math.pow employé hors d'un appel direct"),
])
def test_reconstruction_de_f_pi_etoile_refusee(forme, motif):
    """Point 5 (C2 de `monnaie` ; R1 de l'audit de la reprise du rang 3) : (1 + π*)^{1/n_a}
    par `**`, `**=`, `math.pow` à exposant non entier littéral, exp(log(1 + π*)/n_a), ou une
    racine (`sqrt`, `cbrt`) d'une grandeur qui dépend de π*, est refusée."""
    texte = _avec_forme(forme, "").replace(
        "import TauxDeCroissance, facteur_par_pas, par_pas",
        "import TauxDeCroissance, TauxDeFlux, facteur_par_pas, par_pas", 1)
    ecarts = analyser_texte(texte)
    assert any(motif in e for e in ecarts), ecarts


@pytest.mark.parametrize("forme", [
    # S1 puis S2 du bloc 6 (spécification, `sec:investissement`) : ϱ_L = (1 + i_L)/(1 + π*) − 1,
    # tu* = tū·exp[ζ(ϱ_L − ϱ̄_L)] ; test anti-régression du faux positif R1.
    f"        rho = (1.0 + 0.05) / (1.0 + {PI}) - 1.0\n"
    "        tu_vise = 0.8 * math.exp(2.0 * (rho - 0.03))\n",
    # Puissance entière d'une grandeur qui dépend de π* : aucune racine.
    f"        ecart = (1.0 + {PI}) ** 2\n",
    f"        ecart = (1.0 + {PI}) ** -1 + math.pow(1.0 + {PI}, 3)\n",
    # Logarithme seul, sans exponentielle (ln(1 + π*), taux réel en logarithme).
    f"        lr = math.log(1.0 + {PI})\n",
    # Exponentielle d'un taux par pas qui ne passe pas par le logarithme de π*.
    f"        k = math.exp(par_pas(TauxDeFlux({PI})))\n",
])
def test_formes_sans_reconstruction_de_f_pi_etoile_admises(forme):
    """Point 5 : seule la reconstruction de f(π*) est refusée ; une exponentielle ou une
    puissance entière d'une grandeur qui dépend de π* reste admise (π* lue dans l'état
    d'ouverture et déclarée, point 6)."""
    texte = _avec_forme(forme, "LIT_LA_CIBLE").replace(
        "import TauxDeCroissance, facteur_par_pas, par_pas",
        "import TauxDeCroissance, TauxDeFlux, facteur_par_pas, par_pas", 1)
    assert analyser_texte(texte) == []


def test_formes_hors_du_critere_de_gamma_e():
    """Point 5, limite déclarée : une valeur qui dépend de π* rangée dans un conteneur par une
    méthode (`t.append(π*)`) n'est pas suivie ; la forme est admise par le contrôle. Le test
    fixe cette limite : s'il échoue, le contrôle a été étendu et le docstring doit l'être
    aussi."""
    texte = _avec_forme(
        f"        t = [0.0]\n        t.append({PI})\n"
        "        f = facteur_par_pas(TauxDeCroissance(t[1]))\n", "LIT_LA_CIBLE")
    assert analyser_texte(texte) == []


# Contournements de la reprise du rang 3 (m1 puis R2), suivis : ordre supérieur, lambda ou
# fonction rangée dans un n-uplet ou un dictionnaire, alias de méthode.
CONVERTIR = "def convertir(u):\n    return facteur_par_pas(TauxDeCroissance(u))\n"


@pytest.mark.parametrize("forme, fonctions", [
    (f"        f = appliquer(convertir, {PI})\n",
     CONVERTIR + "\n\ndef appliquer(g, w):\n    return g(w)\n"),
    ("        h = (lambda z: facteur_par_pas(TauxDeCroissance(z)),)\n"
     f"        f = h[0]({PI})\n", ""),
    ("        d = {'c': lambda z: facteur_par_pas(TauxDeCroissance(z))}\n"
     f"        f = d['c']({PI})\n", ""),
    (f"        h = (convertir,)\n        f = h[0]({PI})\n", CONVERTIR),
    (f"        m = self.convertir\n        f = m({PI})\n", "METHODE"),
])
def test_recalcul_par_appel_indirect_refuse(forme, fonctions):
    """Point 5 (R2 de l'audit de la reprise du rang 3) : un appel indirect (indice, appel d'un
    paramètre) lie ses arguments à tous les paramètres des appelables du module ; un alias de
    méthode partage ses appelables : le recalcul de f(π*) qui s'y cache est refusé."""
    ecarts = analyser_texte(_avec_forme(forme, fonctions))
    assert any(MOTIF_GAMMA_E in e for e in ecarts), ecarts


def test_puissance_et_math_sans_pi_etoile_admises():
    """Point 5 : la puissance et `math` sur une grandeur qui ne dépend pas de π* restent
    admises (la marge du bloc 4 emploie `math.exp` et `math.log`)."""
    texte = _avec_forme("        k = (1.0 + vue.ouverture.IN_vol) ** 2.0 + math.log(2.0)\n", "")
    assert [e for e in analyser_texte(texte) if "π*" in e] == []


def test_recalcul_sous_un_autre_nom_refuse():
    """Point 5 : la conversion renommée à l'importation est suivie sous son nouveau nom."""
    texte = _avec_forme("        f = fpp(TauxDeCroissance(vue.ouverture.pi_etoile))\n", "")
    texte = texte.replace("import TauxDeCroissance, facteur_par_pas, par_pas",
                          "import TauxDeCroissance, par_pas\n"
                          "from nations.moteur.conversions import facteur_par_pas as fpp", 1)
    ecarts = analyser_texte(texte)
    assert any("fpp sur une grandeur qui dépend de π* refusé" in e for e in ecarts), ecarts


@pytest.mark.parametrize("forme, fonctions", [
    # Une conversion géométrique sans π* ; π* lue sans conversion (BC1 lit le taux annuel) ; la
    # conversion linéaire d'une grandeur qui dépend de π* (BC6 convertit i_CB), hors du critère.
    # π* lue dans l'état d'ouverture (point 6, R2 de `monnaie` : forme réécrite au rang 4 de
    # J3-c, la lecture dans la table étant refusée).
    ("        f = facteur_par_pas(vue.parametres.production.g_pr)\n", ""),
    ("        c = vue.ouverture.pi_etoile\n        k = (1.0 + c) * 1.01\n", "LIT_LA_CIBLE"),
    ("        c = vue.ouverture.pi_etoile\n"
     "        k = par_pas(vue.parametres.prix.lambda_mu) * c\n", "LIT_LA_CIBLE"),
])
def test_formes_sans_recalcul_admises(forme, fonctions):
    """Point 5 : seule la conversion géométrique d'une grandeur qui dépend de π* est
    refusée."""
    assert analyser_texte(_avec_forme(forme, fonctions)) == []


@pytest.mark.parametrize("forme, fonctions", [
    ("        c = vue.parametres.banque_centrale.pi_etoile.valeur\n        k = (1.0 + c) * 1.01\n",
     ""),
    ("        c = vue.parametres.banque_centrale.pi_etoile\n", ""),
    ("        table = vue.parametres.banque_centrale\n        c = table.pi_etoile.valeur\n", ""),
    ("        c = cible(vue.parametres)\n",
     "def cible(p):\n    return p.banque_centrale.pi_etoile.valeur\n"),
    ("        c = cible(vue.parametres.banque_centrale)\n",
     "def cible(t):\n    match t:\n        case float(pi_etoile=x):\n            return x\n"
     "    return 0.0\n"),
])
def test_cible_lue_hors_de_l_etat_refusee(forme, fonctions):
    """Point 6 (réserve R2 de `monnaie`, rang 3 de J3-c ; ADR 0010) : un bloc lit la cible en
    vigueur π*_t dans l'état d'ouverture ; toute lecture de `pi_etoile` ailleurs que sur
    `vue.ouverture` (la table du bloc 8 par la vue, liée à un nom, passée à une fonction, ou
    un motif de classe) est refusée, même sans conversion."""
    ecarts = analyser_texte(_avec_forme(forme, fonctions))
    assert any(MOTIF_CIBLE_HORS_DE_L_ETAT in e for e in ecarts), ecarts


def test_cible_lue_dans_l_etat_admise():
    """Point 6 : `vue.ouverture.pi_etoile`, déclarée, est la forme admise ; non déclarée, elle
    est refusée par le relevé (point 2), non par le point 6."""
    forme = "        c = vue.ouverture.pi_etoile\n        k = (1.0 + c) * 1.01\n"
    assert analyser_texte(_avec_forme(forme, "LIT_LA_CIBLE")) == []
    ecarts = analyser_texte(_avec_forme(forme, ""))
    assert ecarts == ["phase_5 : ouverture 'pi_etoile' faite, non déclarée"]


def test_aucun_nom_admis_ne_calcule_gamma_e():
    """Critère de #61 : Γ^e n'est pas dans les noms admis. La fonction qui le calcule est dans
    `nations.moteur.ouverture`, module hors de la liste blanche ; `NOMS_DE_CONVERSIONS` ne
    contient que les deux conversions et leurs types ; son importation est refusée."""
    from nations.moteur import ouverture

    fonction = next(g.fonction for g in ouverture.GRANDEURS_OUVERTURE if g.nom == "Gamma_e")
    assert fonction.__module__ == "nations.moteur.ouverture"
    assert "nations.moteur.ouverture" not in IMPORTATIONS_ADMISES
    assert not any(n in NOMS_DE_CONVERSIONS for n in (fonction.__name__, "Gamma_e", "gamma_e",
                                                      "pi_etoile_pas"))
    texte = CONFORME.replace("import math\n", "import math\n\n\ndef _jamais():\n"
                             f"    from nations.moteur.ouverture import {fonction.__name__}\n",
                             1)
    assert any(f"importation de nations.moteur.ouverture.{fonction.__name__} refusée" in e
               for e in analyser_texte(texte))


def test_cout_de_la_fermeture_au_pire_cas():
    """Coût de la fermeture de `_marques_de_la_cible` : une chaîne de 2 000 liaisons écrites
    dans l'ordre inverse de leur dépendance (le pire cas d'un point fixe par passes, qui ne
    marquerait qu'un identifiant par passe) est jugée en moins de 5 s ; la fermeture parcourt
    chaque arête une fois (mesure dans le compte rendu de #61). Homonymes : voir
    `test_cout_des_homonymes`."""
    import time

    n = 2000
    lignes = [f"        x{k} = x{k - 1}\n" for k in range(n, 0, -1)]
    forme = "".join(lignes) + "        x0 = 0.0\n" + "        x0 = vue.ouverture.pi_etoile\n" \
        + f"        f = facteur_par_pas(TauxDeCroissance(x{n}))\n"
    texte = _avec_forme(forme, "")
    debut = time.perf_counter()
    ecarts = analyser(texte, "prix", None)
    duree = time.perf_counter() - debut
    assert any(MOTIF_GAMMA_E in e for e in ecarts)
    assert duree < 5.0, duree


def test_cout_des_homonymes():
    """m3 de l'audit du rang 3 : 2 000 fonctions homonymes appelées 2 000 fois (51,7 s quand
    chaque appel parcourait chaque définition) sont jugées en moins de 5 s : un nœud d'appel par
    position, relié une fois aux paramètres des homonymes."""
    import time

    k = m = 2000
    fonctions = "".join(f"def h(a{i}, b{i}):\n    return a{i}\n\n\n" for i in range(k))
    forme = "".join(f"        y{j} = h(vue.ouverture.pi_etoile, {j})\n" for j in range(m)) \
        + "        f = facteur_par_pas(TauxDeCroissance(y0))\n"
    texte = _avec_forme(forme, fonctions)
    debut = time.perf_counter()
    ecarts = analyser(texte, "prix", None)
    duree = time.perf_counter() - debut
    assert any(MOTIF_GAMMA_E in e for e in ecarts)
    assert duree < 5.0, duree
