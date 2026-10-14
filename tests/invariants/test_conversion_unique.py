"""Invariant : conversion unique des taux au pas, lue sur l'arbre syntaxique de `src/` (#98).

Contrat : ADR 0012, F2, et annotation du 07/10/2026 (questions de `coder` sur
#97), point 4, critère écrit avant l'essai ; fiche « temps et comptabilité »,
§ 9.8, point 6. Est un **écart**, hors des deux conversions
(`nations.moteur.conversions.par_pas` et `facteur_par_pas`) :

- toute **division réelle** (`/`, `/=`, `operator.truediv`, `numpy.divide`…)
  dont le **diviseur est** n_a (`PAS_PAR_AN.valeur`, `pas_par_an`, `n_a`, ou
  un nom qui leur est lié par une affectation simple), n_a pouvant y être un
  facteur (`2 * n_a`) ; une division par un élément **indexé** par n_a
  (`registre[0] / registre[PAS_PAR_AN.valeur]`) n'en est pas une ;
- toute **puissance** (`**`, `pow`, `math.pow`, `numpy.power`…) dont
  l'exposant contient 1/n_a, ou a n_a pour facteur (annualisation inverse,
  point 5 de la même annotation, écrite avec son premier consommateur).

Un nom est lié à n_a (ou n_m) par une **affectation simple** (`=`, affectation
annotée, affectation de n-uplet terme à terme, `:=`), par un **import renommé**
(`from … import PAS_PAR_AN as N`) ou par la **valeur par défaut d'un
paramètre** ; un **attribut** l'est par une affectation simple ou annotée
(`self.n = PAS_PAR_AN.valeur`, puis `x / self.n`) ; une liaison vaut quel que
soit son ordre dans le texte (`M = N` écrit avant `N = PAS_PAR_AN.valeur`) ;
une conversion `float(n_a)` ou `int(n_a)` est traversée ; `n_a ** -1`
(puissance négative constante) est une division par n_a.

**Hors du critère**, déclarés (et fixés par `test_formes_hors_du_critere`) :
- la liaison par une boucle (`for n in (PAS_PAR_AN.valeur,)`), ou par toute
  autre construction que celles qui précèdent ;
- un exposant `Fraction(1, PAS_PAR_AN.valeur)` (ou tout appel qui construit
  1/n_a sans `/` ni puissance négative) ;
- les arguments nommés des fonctions de division (`np.divide(x1=x,
  x2=PAS_PAR_AN.valeur)`) : seul le second argument positionnel est lu ;
- le littéral `12` (ou `12.0`). Le critère écrit avant l'essai nomme n_a par son
  paramètre (`PAS_PAR_AN.valeur`, `pas_par_an`, `n_a`) ; un diviseur littéral ne
  se distingue pas, sur l'arbre, d'un autre 12, et un n_a écrit en dur est un
  autre défaut (paramètre non typé, ADR 0012, F1). Ce défaut est contrôlé à
  part par `test_aucun_douze_litteral_dans_src` : aucun littéral 12 ni 12.0
  n'est opérande de `/`, `//`, `%`, `**` (ni de leur forme augmentée), ni
  argument de `divmod`, dans `src/`.

Le **calcul de date sur l'entier t** (`divmod`, `//`, `%` par n_a ou n_m) est
admis dans `nations.moteur.calendrier` seulement, par la liste d'exemptions
**fermée et nommée** `EXEMPTIONS_CALENDRIER` ; ailleurs, c'est un écart.
Chaque exemption doit servir (une exemption sans objet est un écart de la
liste elle-même).
"""

import ast
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[2]
SRC = RACINE / "src"

# Noms de n_a et de n_m (attribut, nom simple, constante du cadre).
NOMS_N_A = frozenset({"pas_par_an", "n_a", "PAS_PAR_AN"})
NOMS_N_M = frozenset({"pas_par_tour", "n_m", "PAS_PAR_TOUR"})

# Exemptions fermées et nommées : (module, fonction) → nature d'opération admise.
EXEMPTIONS_CONVERSIONS = {
    ("nations.moteur.conversions", "par_pas"): "division par n_a",
    ("nations.moteur.conversions", "facteur_par_pas"): "puissance en n_a",
}
EXEMPTIONS_CALENDRIER = {
    ("nations.moteur.calendrier", "date"): "division entière par n_a ou n_m",
    ("nations.moteur.calendrier", "est_date_de_decision"): "division entière par n_a ou n_m",
}
EXEMPTIONS = {**EXEMPTIONS_CONVERSIONS, **EXEMPTIONS_CALENDRIER}

# Fonctions appelées qui divisent ou élèvent à une puissance leur second argument.
_APPELS_DIVISION = frozenset({"truediv", "divide", "true_divide"})
_APPELS_DIVISION_ENTIERE = frozenset({"floordiv", "floor_divide", "mod", "remainder", "fmod",
                                      "divmod"})
_APPELS_PUISSANCE = frozenset({"pow", "power", "float_power"})


def _nom_appele(appel):
    fonction = appel.func
    if isinstance(fonction, ast.Name):
        return fonction.id
    if isinstance(fonction, ast.Attribute):
        return fonction.attr
    return None


class Detecteur(ast.NodeVisitor):
    """Relève les divisions et puissances par n_a (ou n_m) d'un module, avec leur fonction.

    Les alias (affectations simple, annotée, de n-uplet et `:=`, imports
    renommés, valeurs par défaut des paramètres, attributs affectés) sont
    relevés avant le parcours, par un point fixe sur les liaisons du module :
    l'ordre du texte n'importe pas. Les fermetures de n_a et de n_m avancent en
    parallèle, chacune indépendamment de l'autre ; après k tours, chacune
    contient au moins les noms liés par une chaîne de k liaisons, et une chaîne
    a au plus L liaisons : chacune se stabilise en au plus L tours, et un
    dernier tour sans ajout l'atteste, soit au plus L + 1 tours de L liaisons. La portée n'est pas suivie :
    un alias vaut dans tout le module (au plus strict) ; un attribut lié
    (`self.n`) vaut pour tout attribut de même nom (`autre.n`), noté `.n`.
    """

    def __init__(self, module, arbre):
        self.module = module
        self.pile = []
        self.releves = []
        # Divisions de l'exposant d'une puissance relevée : relevées avec elle.
        self.absorbees = set()
        self.alias_n_a, self.alias_n_m = set(), set()
        liaisons = [liaison for n in ast.walk(arbre) for liaison in _liaisons(n)]
        nouveau = True
        while nouveau:
            nouveau = False
            for nom, valeur in liaisons:
                for noms, alias in ((NOMS_N_A, self.alias_n_a), (NOMS_N_M, self.alias_n_m)):
                    if nom not in alias and self._mention(valeur, noms, alias):
                        alias.add(nom)
                        nouveau = True

    @staticmethod
    def _mention(noeud, noms, alias):
        """Le nœud désigne-t-il n_a (ou n_m) lui-même ? (`float(·)`, `int(·)` traversés)"""
        if (isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Name)
                and noeud.func.id in ("float", "int") and len(noeud.args) == 1
                and not noeud.keywords):
            return Detecteur._mention(noeud.args[0], noms, alias)
        if isinstance(noeud, ast.Name):
            return noeud.id in noms or noeud.id in alias
        if isinstance(noeud, ast.Attribute):
            if noeud.attr in noms or "." + noeud.attr in alias:
                return True
            return noeud.attr == "valeur" and Detecteur._mention(noeud.value, noms, alias)
        return False

    def _inverse(self, noeud, noms, alias):
        """Le nœud est-il n_a ** k, k constante négative (soit une division par n_a) ?"""
        if not (isinstance(noeud, ast.BinOp) and isinstance(noeud.op, ast.Pow)):
            return False
        k = noeud.right
        if isinstance(k, ast.UnaryOp) and isinstance(k.op, ast.USub) and isinstance(
                k.operand, ast.Constant):
            negatif = isinstance(k.operand.value, (int, float)) and k.operand.value > 0
        else:
            negatif = isinstance(k, ast.Constant) and isinstance(k.value, (int, float)) and (
                k.value < 0)
        return negatif and self._facteur(noeud.left, noms, alias)

    def _facteur(self, noeud, noms, alias):
        """n_a (ou n_m) est-il un facteur du nœud (produits et quotients, signe compris) ?"""
        if isinstance(noeud, ast.UnaryOp):
            return self._facteur(noeud.operand, noms, alias)
        if isinstance(noeud, ast.BinOp) and isinstance(noeud.op, (ast.Mult, ast.Div)):
            return self._facteur(noeud.left, noms, alias) or self._facteur(noeud.right, noms,
                                                                              alias)
        return self._mention(noeud, noms, alias)

    def _par_n_a(self, noeud):
        return self._facteur(noeud, NOMS_N_A, self.alias_n_a)

    def _par_n_a_ou_n_m(self, noeud):
        return self._par_n_a(noeud) or self._facteur(noeud, NOMS_N_M, self.alias_n_m)

    def _exposant_en_n_a(self, exposant):
        """L'exposant contient-il 1/n_a, ou n_a pour facteur ? (indices exclus)"""
        if self._par_n_a(exposant):
            return True
        a_voir = [exposant]
        while a_voir:
            noeud = a_voir.pop()
            if isinstance(noeud, ast.Subscript):
                a_voir.append(noeud.value)
                continue
            if isinstance(noeud, ast.BinOp) and isinstance(noeud.op, ast.Div) and self._par_n_a(
                    noeud.right):
                return True
            if self._inverse(noeud, NOMS_N_A, self.alias_n_a):
                return True
            a_voir.extend(ast.iter_child_nodes(noeud))
        return False

    def _absorber(self, exposant):
        self.absorbees.update(id(n) for n in ast.walk(exposant) if isinstance(n, ast.BinOp))

    def _relever(self, noeud, nature):
        fonction = ".".join(self.pile) if self.pile else "<module>"
        self.releves.append((self.module, fonction, nature, noeud.lineno))

    def _visiter_portee(self, noeud):
        self.pile.append(noeud.name)
        self.generic_visit(noeud)
        self.pile.pop()

    visit_FunctionDef = visit_AsyncFunctionDef = visit_ClassDef = _visiter_portee

    def _operation(self, noeud, op, droite):
        if id(noeud) in self.absorbees:
            return
        if isinstance(op, ast.Div) and self._par_n_a(droite):
            self._relever(noeud, "division par n_a")
        elif isinstance(noeud, ast.BinOp) and self._inverse(noeud, NOMS_N_A, self.alias_n_a):
            self._relever(noeud, "division par n_a")
        elif isinstance(op, (ast.FloorDiv, ast.Mod)) and self._par_n_a_ou_n_m(droite):
            self._relever(noeud, "division entière par n_a ou n_m")
        elif isinstance(op, ast.Pow) and self._exposant_en_n_a(droite):
            self._relever(noeud, "puissance en n_a")
            self._absorber(droite)

    def visit_BinOp(self, noeud):
        self._operation(noeud, noeud.op, noeud.right)
        self.generic_visit(noeud)

    def visit_AugAssign(self, noeud):
        self._operation(noeud, noeud.op, noeud.value)
        self.generic_visit(noeud)

    def visit_Call(self, noeud):
        nom = _nom_appele(noeud)
        if nom is not None and len(noeud.args) >= 2:
            second = noeud.args[1]
            if nom in _APPELS_DIVISION and self._par_n_a(second):
                self._relever(noeud, "division par n_a")
            elif nom in _APPELS_DIVISION_ENTIERE and self._par_n_a_ou_n_m(second):
                self._relever(noeud, "division entière par n_a ou n_m")
            elif nom in _APPELS_PUISSANCE and self._exposant_en_n_a(second):
                self._relever(noeud, "puissance en n_a")
                self._absorber(second)
        self.generic_visit(noeud)


def _liaisons(noeud):
    """(nom lié, valeur) que lie un nœud : affectations, import renommé, défauts de paramètres."""
    if isinstance(noeud, ast.Assign):
        for cible in noeud.targets:
            yield from _cibles(cible, noeud.value)
    elif isinstance(noeud, ast.AnnAssign) and noeud.value is not None:
        yield from _cibles(noeud.target, noeud.value)
    elif isinstance(noeud, ast.NamedExpr):
        yield from _cibles(noeud.target, noeud.value)
    elif isinstance(noeud, ast.ImportFrom):
        for alias in noeud.names:
            if alias.asname:
                yield alias.asname, ast.Name(alias.name)
    elif isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        a = noeud.args
        positionnels = a.posonlyargs + a.args
        for arg, defaut in zip(positionnels[len(positionnels) - len(a.defaults):], a.defaults):
            yield arg.arg, defaut
        for arg, defaut in zip(a.kwonlyargs, a.kw_defaults):
            if defaut is not None:
                yield arg.arg, defaut


def _cibles(cible, valeur):
    """Nom simple, attribut (noté `.attr`), ou n-uplet terme à terme quand la valeur est un
    n-uplet de même longueur."""
    if isinstance(cible, ast.Name):
        yield cible.id, valeur
    elif isinstance(cible, ast.Attribute):
        yield "." + cible.attr, valeur
    elif isinstance(cible, (ast.Tuple, ast.List)) and isinstance(valeur, (ast.Tuple, ast.List)) \
            and len(cible.elts) == len(valeur.elts):
        for c, v in zip(cible.elts, valeur.elts):
            yield from _cibles(c, v)


def releves_du_texte(module, texte):
    arbre = ast.parse(texte)
    detecteur = Detecteur(module, arbre)
    detecteur.visit(arbre)
    return detecteur.releves


def releves_de_src(racine=SRC):
    releves = []
    for chemin in sorted(racine.rglob("*.py")):
        module = ".".join(chemin.relative_to(racine).with_suffix("").parts)
        releves += releves_du_texte(module, chemin.read_text(encoding="utf-8"))
    return releves


def ecarts(releves):
    """Relevés non couverts par une exemption de même nature."""
    return [r for r in releves if EXEMPTIONS.get((r[0], r[1])) != r[2]]


def test_conversion_unique_dans_src():
    """Aucune division ni puissance par n_a hors des deux conversions ; aucune division entière
    par n_a ou n_m hors du calendrier ; chaque exemption sert."""
    releves = releves_de_src()
    assert ecarts(releves) == []
    assert {(r[0], r[1]) for r in releves} == set(EXEMPTIONS)


def test_exemptions_fermees_et_nommees():
    """Les exemptions sont les deux conversions et les deux fonctions du calendrier."""
    assert set(EXEMPTIONS_CONVERSIONS) == {("nations.moteur.conversions", "par_pas"),
                                           ("nations.moteur.conversions", "facteur_par_pas")}
    assert set(EXEMPTIONS_CALENDRIER) == {("nations.moteur.calendrier", "date"),
                                          ("nations.moteur.calendrier", "est_date_de_decision")}


@pytest.mark.parametrize("texte, nature", [
    ("def f(x):\n    return x / PAS_PAR_AN.valeur\n", "division par n_a"),
    ("def f(x):\n    return x / CADRE.pas_par_an\n", "division par n_a"),
    ("def f(x, n_a):\n    return x / (2 * n_a)\n", "division par n_a"),
    ("def f(x):\n    x /= PAS_PAR_AN.valeur\n    return x\n", "division par n_a"),
    ("N = PAS_PAR_AN.valeur\ndef f(x):\n    return x / N\n", "division par n_a"),
    ("def f(x):\n    return operator.truediv(x, PAS_PAR_AN.valeur)\n", "division par n_a"),
    ("def f(x):\n    return np.divide(x, PAS_PAR_AN.valeur)\n", "division par n_a"),
    ("def f(x):\n    return (1 + x) ** (1 / PAS_PAR_AN.valeur)\n", "puissance en n_a"),
    ("def f(x):\n    return (1 + x) ** PAS_PAR_AN.valeur - 1\n", "puissance en n_a"),
    ("def f(x):\n    return pow(1 + x, 1.0 / n_a)\n", "puissance en n_a"),
    ("def f(x):\n    return math.pow(1 + x, -1 / PAS_PAR_AN.valeur)\n", "puissance en n_a"),
    ("def f(t):\n    return divmod(t, PAS_PAR_AN.valeur)\n", "division entière par n_a ou n_m"),
    ("def f(t):\n    return t // PAS_PAR_AN.valeur\n", "division entière par n_a ou n_m"),
    ("def f(t):\n    return t % PAS_PAR_TOUR.valeur\n", "division entière par n_a ou n_m"),
    # Formes adverses : alias annotés, renommés, par défaut, par n-uplet, `:=`, conversions,
    # puissance négative.
    ("N: int = PAS_PAR_AN.valeur\ndef f(x):\n    return x / N\n", "division par n_a"),
    ("from nations.moteur.parametres.cadre import PAS_PAR_AN as P\n"
     "def f(x):\n    return x / P.valeur\n", "division par n_a"),
    ("def f(x, n=PAS_PAR_AN.valeur):\n    return x / n\n", "division par n_a"),
    ("def f(x, *, n=CADRE.pas_par_an):\n    return x / n\n", "division par n_a"),
    ("a, n = 1.0, PAS_PAR_AN.valeur\ndef f(x):\n    return x / n\n", "division par n_a"),
    ("def f(x):\n    if (n := PAS_PAR_AN.valeur):\n        return x / n\n", "division par n_a"),
    ("def f(x):\n    return x / float(PAS_PAR_AN.valeur)\n", "division par n_a"),
    ("def f(x):\n    return x * PAS_PAR_AN.valeur ** -1\n", "division par n_a"),
    ("def f(x):\n    return x * float(n_a) ** -1.0\n", "division par n_a"),
    ("def f(x):\n    return (1 + x) ** (PAS_PAR_AN.valeur ** -1)\n", "puissance en n_a"),
    ("def f(t, n=PAS_PAR_TOUR.valeur):\n    return t % int(n)\n",
     "division entière par n_a ou n_m"),
    # Attributs liés par affectation simple, annotée ou de n-uplet ; alias à ordre inversé.
    ("def f(o, x):\n    o.n = PAS_PAR_AN.valeur\n    return x / o.n\n", "division par n_a"),
    ("def f(o, x):\n    o.n: int = PAS_PAR_AN.valeur\n    return x / o.n\n", "division par n_a"),
    ("def f(o, x):\n    o.a, o.n = 1.0, PAS_PAR_AN.valeur\n    return x / o.n\n",
     "division par n_a"),
    ("M = N\nN = PAS_PAR_AN.valeur\ndef f(x):\n    return x / M\n", "division par n_a"),
    # Ordre inversé à même profondeur (`ast.walk` parcourt en largeur) : `o.m = M` est vu
    # avant `M = …`.
    ("def f(t, o):\n    o.m = M\n    M = PAS_PAR_TOUR.valeur\n    return t % o.m\n",
     "division entière par n_a ou n_m"),
])
def test_le_detecteur_releve_les_ecarts(texte, nature):
    """Chaque forme d'écart est relevée, avec sa nature et sa fonction."""
    assert [(f, n) for _, f, n, _ in releves_du_texte("m", texte)] == [("f", nature)]


@pytest.mark.parametrize("texte", [
    "def f(r):\n    return r[0] / r[PAS_PAR_AN.valeur] - 1.0\n",
    "def f(x):\n    return x / (PAS_PAR_AN.valeur + 1)\n",
    "NIVEAUX = PAS_PAR_AN.valeur + 1\ndef f(x):\n    return x / NIVEAUX\n",
    "def f(x):\n    return x * PAS_PAR_AN.valeur\n",
    "def f(x, y):\n    return x / y\n",
    "def f(x):\n    return (1 + x) ** 2\n",
    "def f(x):\n    return x * PAS_PAR_AN.valeur ** 2\n",
    "def f(x, n=PAS_PAR_AN.valeur + 1):\n    return x / n\n",
    "def f(x):\n    return x / 12\n",
    "def f(o, x):\n    o.n = PAS_PAR_AN.valeur + 1\n    return x / o.n\n",
    "M = N\nN = PAS_PAR_AN.valeur + 1\ndef f(x):\n    return x / M\n",
])
def test_le_detecteur_ne_releve_pas_le_reste(texte):
    """Division par un élément indexé par n_a, par n_a + 1, produit, autres puissances : admis."""
    assert releves_du_texte("m", texte) == []


def test_un_ecart_hors_des_exemptions_est_signale():
    """Une division par n_a dans `registre`, ou une division entière dans `ordonnanceur`, est un
    écart, même dans un module qui a une autre exemption."""
    texte = "def glissement(r):\n    return r[0] / PAS_PAR_AN.valeur\n"
    assert ecarts(releves_du_texte("nations.moteur.registre", texte)) == [
        ("nations.moteur.registre", "glissement", "division par n_a", 2)]
    texte = "def date(t):\n    return (1 + t) ** (1 / PAS_PAR_AN.valeur)\n"
    assert ecarts(releves_du_texte("nations.moteur.calendrier", texte)) == [
        ("nations.moteur.calendrier", "date", "puissance en n_a", 2)]


def test_un_attribut_lie_dans_une_methode_est_releve_avec_sa_classe():
    """`self.n` lié dans `__init__`, divisé dans une autre méthode : relevé dans `C.f`."""
    texte = ("class C:\n    def __init__(self):\n        self.n = PAS_PAR_AN.valeur\n"
             "    def f(self, x):\n        return x / self.n\n")
    assert [(f, n) for _, f, n, _ in releves_du_texte("m", texte)] == [("C.f",
                                                                         "division par n_a")]


@pytest.mark.parametrize("texte", [
    "def f(x):\n    for n in (PAS_PAR_AN.valeur,):\n        return x / n\n",
    "def f(x):\n    return (1 + x) ** Fraction(1, PAS_PAR_AN.valeur)\n",
    "def f(x):\n    return np.divide(x1=x, x2=PAS_PAR_AN.valeur)\n",
])
def test_formes_hors_du_critere(texte):
    """Formes déclarées hors du critère dans la docstring du module : non relevées. Si l'une
    d'elles vient à l'être, la docstring est à mettre à jour avec ce test."""
    assert releves_du_texte("m", texte) == []


# --------------------------------------------------------------------------
# Littéral 12 : hors du critère « conversion unique », contrôlé à part
# --------------------------------------------------------------------------

_OPERATEURS_DOUZE = (ast.Div, ast.FloorDiv, ast.Mod, ast.Pow)


def _douze(noeud):
    """Le nœud est-il le littéral 12 ou 12.0 (signe unaire compris) ?"""
    if isinstance(noeud, ast.UnaryOp) and isinstance(noeud.op, (ast.USub, ast.UAdd)):
        noeud = noeud.operand
    return (isinstance(noeud, ast.Constant) and type(noeud.value) in (int, float)
            and noeud.value == 12)


def douzes_du_texte(texte):
    """Lignes où un littéral 12 est opérande direct de `/`, `//`, `%`, `**` (forme augmentée
    comprise) ou argument positionnel de `divmod`."""
    lignes = []
    for n in ast.walk(ast.parse(texte)):
        if isinstance(n, ast.BinOp) and isinstance(n.op, _OPERATEURS_DOUZE):
            operandes = (n.left, n.right)
        elif isinstance(n, ast.AugAssign) and isinstance(n.op, _OPERATEURS_DOUZE):
            operandes = (n.value,)
        elif isinstance(n, ast.Call) and _nom_appele(n) == "divmod":
            operandes = n.args
        else:
            continue
        if any(_douze(o) for o in operandes):
            lignes.append(n.lineno)
    return sorted(lignes)


def test_aucun_douze_litteral_dans_src():
    """Aucun n_a écrit en dur : aucun littéral 12 ni 12.0 opérande de `/`, `//`, `%`, `**`, ni
    argument de `divmod`, dans `src/` (ADR 0012, F1)."""
    trouves = [(chemin.relative_to(RACINE).as_posix(), ligne)
               for chemin in sorted(SRC.rglob("*.py"))
               for ligne in douzes_du_texte(chemin.read_text(encoding="utf-8"))]
    assert trouves == []


@pytest.mark.parametrize("texte", [
    "def f(x):\n    return x / 12\n",
    "def f(x):\n    return x / 12.0\n",
    "def f(x):\n    return x / -12\n",
    "def f(t):\n    return t // 12\n",
    "def f(t):\n    return t % 12\n",
    "def f(x):\n    return (1 + x) ** 12 - 1\n",
    "def f(x):\n    x /= 12\n    return x\n",
    "def f(t):\n    return divmod(t, 12)\n",
])
def test_le_controle_du_douze_releve_les_formes_adverses(texte):
    """Chaque forme est relevée, à sa ligne."""
    assert douzes_du_texte(texte) == [2]


@pytest.mark.parametrize("texte", [
    "def f(x):\n    return x * 12\n",
    "def f(x):\n    return x + 12\n",
    "def f(r, x):\n    return r[12] / x\n",
    "def f(x):\n    return x / 13\n",
    "def f(x):\n    return x / PAS_PAR_AN.valeur\n",
    "def f(t):\n    return divmod(t, 7)\n",
    "def f(x):\n    return x / True\n",
])
def test_le_controle_du_douze_ne_releve_pas_le_reste(texte):
    """Produit, somme, indice 12, autre diviseur, n_a nommé : non relevés."""
    assert douzes_du_texte(texte) == []
