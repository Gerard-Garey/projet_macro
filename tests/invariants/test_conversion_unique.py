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
  part par `test_aucun_douze_litteral_dans_src` (#102) : aucun littéral 12 ni
  12.0, à quelque place de l'arbre que ce soit (opérande, argument d'appel,
  constante de module, facteur non direct), dans `src/` hors de
  `EXEMPTION_DOUZE` (la déclaration de n_a).

Le **calcul de date sur l'entier t** (`divmod`, `//`, `%` par n_a ou n_m) est
admis dans `nations.moteur.calendrier` seulement, par la liste d'exemptions
**fermée et nommée** `EXEMPTIONS_CALENDRIER` ; ailleurs, c'est un écart.
Les divisions par n_a et les puissances en 1/n_a des formes fermées du
résolveur de l'état stationnaire (`nations.scenarios.stationnaire`) sont
admises par une troisième liste **fermée et nommée**, `EXEMPTIONS_STATIONNAIRE`
(ADR 0015, point 13 ; décision S1, qui modifie ADR 0014, F2).
Le ratio au PIB annuel du test zéro (`eq:observation-ratio-pib-annuel`), stock d'ouverture
rapporté à n_a fois le flux du pas, est une division par n_a × flux qui n'est pas une
conversion de taux : il est admis dans sa seule fonction d'`observation/` par une quatrième
liste **fermée et nommée**, `EXEMPTIONS_OBSERVATION` (#176 ; visée par le mainteneur le
26/11/2026 ; modifie ADR 0014, F2, comme S1), avec la richesse des ménages de B10.
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
# Résolveur de l'état stationnaire, module feuille de `scenarios/` (ADR 0015, point 13 ; décision S1 ;
# modifie ADR 0014, F2) : ses formes fermées sont écrites à n_a quelconque et évaluées par le script
# d'état stationnaire à n_a ∈ {4 ; 12 ; 52}, ce que les conversions du moteur ne servent pas ; l'identité
# au bit avec le script exige l'ordre de ses opérations. Seules ces fonctions, nommées une à une ; le reste
# de `nations.scenarios`, comme tout `src/`, reste sous la règle commune, et le littéral 12 sans exemption.
EXEMPTIONS_STATIONNAIRE = {
    ("nations.scenarios.stationnaire", "facteurs"): "puissance en n_a",
    ("nations.scenarios.stationnaire", "rho_IN"): "puissance en n_a",
    ("nations.scenarios.stationnaire", "rho_K"): "puissance en n_a",
    ("nations.scenarios.stationnaire", "etat_stationnaire"): "division par n_a",
    ("nations.scenarios.stationnaire", "ouverture"): "puissance en n_a",
}
# Série du test zéro (#176 ; exemption visée par le mainteneur le 26/11/2026) : le ratio au PIB annuel
# (`eq:observation-ratio-pib-annuel`, M22, lecture (e)) et la richesse des ménages de B10 (stock sur
# n_a fois YD, M27, sans balise), deux définitions de ratios, non des conversions de taux. Seules ces
# deux fonctions ; le reste d'`observation/` (moyennes de 12 tours comprises) reste sous la règle commune.
EXEMPTIONS_OBSERVATION = {
    ("nations.observation.serie_test_zero", "ratio_au_pib_annuel"): "division par n_a",
    ("nations.observation.serie_test_zero", "richesse_sur_revenu_annuel"): "division par n_a",
}
EXEMPTIONS = {**EXEMPTIONS_CONVERSIONS, **EXEMPTIONS_CALENDRIER, **EXEMPTIONS_STATIONNAIRE,
              **EXEMPTIONS_OBSERVATION}

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
    """Aucune division ni puissance par n_a hors des deux conversions et des formes fermées du
    résolveur ; aucune division entière par n_a ou n_m hors du calendrier ; chaque exemption sert."""
    releves = releves_de_src()
    assert ecarts(releves) == []
    assert {(r[0], r[1]) for r in releves} == set(EXEMPTIONS)


def test_exemptions_fermees_et_nommees():
    """Les exemptions sont les deux conversions, les deux fonctions du calendrier, les cinq
    fonctions du résolveur de l'état stationnaire (ADR 0015, point 13), le ratio au PIB annuel
    du test zéro et la richesse des ménages de B10 (`richesse_sur_revenu_annuel`) (#176), sans
    recouvrement."""
    assert set(EXEMPTIONS_CONVERSIONS) == {("nations.moteur.conversions", "par_pas"),
                                           ("nations.moteur.conversions", "facteur_par_pas")}
    assert set(EXEMPTIONS_CALENDRIER) == {("nations.moteur.calendrier", "date"),
                                          ("nations.moteur.calendrier", "est_date_de_decision")}
    assert set(EXEMPTIONS_STATIONNAIRE) == {("nations.scenarios.stationnaire", nom) for nom in (
        "facteurs", "rho_IN", "rho_K", "etat_stationnaire", "ouverture")}
    assert set(EXEMPTIONS_OBSERVATION) == {("nations.observation.serie_test_zero", nom) for nom in (
        "ratio_au_pib_annuel", "richesse_sur_revenu_annuel")}
    assert len(EXEMPTIONS) == len(EXEMPTIONS_CONVERSIONS) + len(EXEMPTIONS_CALENDRIER) + len(
        EXEMPTIONS_STATIONNAIRE) + len(EXEMPTIONS_OBSERVATION)


def test_l_exemption_du_ratio_ne_couvre_que_sa_fonction():
    """Une division par n_a ailleurs dans la série du test zéro, ou dans un autre module
    d'`observation/`, est un écart ; une puissance en 1/n_a dans la fonction exemptée aussi."""
    texte = "def _clore(x, pas_par_an):\n    return x / pas_par_an\n"
    assert ecarts(releves_du_texte("nations.observation.serie_test_zero", texte)) == [
        ("nations.observation.serie_test_zero", "_clore", "division par n_a", 2)]
    texte = "def ratio_au_pib_annuel(x, y, pas_par_an):\n    return x / (pas_par_an * y)\n"
    assert ecarts(releves_du_texte("nations.observation.residus", texte)) == [
        ("nations.observation.residus", "ratio_au_pib_annuel", "division par n_a", 2)]
    texte = "def ratio_au_pib_annuel(x, pas_par_an):\n    return x ** (1 / pas_par_an)\n"
    assert ecarts(releves_du_texte("nations.observation.serie_test_zero", texte)) == [
        ("nations.observation.serie_test_zero", "ratio_au_pib_annuel", "puissance en n_a", 2)]


def test_l_exemption_du_resolveur_ne_couvre_que_ses_fonctions():
    """Une division par n_a dans une autre fonction du résolveur, ou dans un autre module de
    `scenarios/`, est un écart ; une division dans une fonction exemptée pour la puissance aussi."""
    texte = "def relever_conditions(x, n_a):\n    return x / n_a\n"
    assert ecarts(releves_du_texte("nations.scenarios.stationnaire", texte)) == [
        ("nations.scenarios.stationnaire", "relever_conditions", "division par n_a", 2)]
    texte = "def etat_stationnaire(x, n_a):\n    return x / n_a\n"
    assert ecarts(releves_du_texte("nations.scenarios.initial", texte)) == [
        ("nations.scenarios.initial", "etat_stationnaire", "division par n_a", 2)]
    texte = "def ouverture(x, n_a):\n    return x / n_a\n"
    assert ecarts(releves_du_texte("nations.scenarios.stationnaire", texte)) == [
        ("nations.scenarios.stationnaire", "ouverture", "division par n_a", 2)]


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
# Littéral 12 : hors du critère « conversion unique », contrôlé à part (#102)
# --------------------------------------------------------------------------

# Seul fichier de `src/` où un littéral 12 est admis : la déclaration typée de n_a
# (`pas_par_an`). L'exemption est fermée et doit servir.
EXEMPTION_DOUZE = "src/nations/moteur/parametres/cadre.py"


def _douze(noeud):
    """Le nœud est-il le littéral 12 ou 12.0, quelle que soit son écriture (`0xC`, `1.2e1`) ?
    Un booléen n'en est pas un ; le signe unaire est porté par un nœud parent."""
    return (isinstance(noeud, ast.Constant) and type(noeud.value) in (int, float)
            and noeud.value == 12)


def douzes_du_texte(texte):
    """Lignes de tous les littéraux 12 ou 12.0 du texte, quelle que soit leur place dans
    l'arbre : opérande, argument d'appel (positionnel ou nommé), constante de module,
    facteur non direct, indice, valeur par défaut."""
    return sorted(n.lineno for n in ast.walk(ast.parse(texte)) if _douze(n))


def _douzes_de_src():
    return [(chemin.relative_to(RACINE).as_posix(), ligne)
            for chemin in sorted(SRC.rglob("*.py"))
            for ligne in douzes_du_texte(chemin.read_text(encoding="utf-8"))]


def test_aucun_douze_litteral_dans_src():
    """Aucun n_a écrit en dur : aucun littéral 12 ni 12.0 dans `src/` hors de
    `EXEMPTION_DOUZE` (ADR 0012, F1 ; critère de #102, écrit avant l'essai)."""
    assert [(f, n) for f, n in _douzes_de_src() if f != EXEMPTION_DOUZE] == []


def test_l_exemption_du_douze_sert():
    """L'exemption a un objet : le fichier existe et porte au moins un littéral 12."""
    assert (RACINE / EXEMPTION_DOUZE).is_file()
    assert any(f == EXEMPTION_DOUZE for f, _ in _douzes_de_src())


@pytest.mark.parametrize("texte, ligne", [
    # Opérandes directs (#98).
    ("def f(x):\n    return x / 12\n", 2),
    ("def f(x):\n    return x / 12.0\n", 2),
    ("def f(x):\n    return x / -12\n", 2),
    ("def f(t):\n    return t // 12\n", 2),
    ("def f(t):\n    return t % 12\n", 2),
    ("def f(x):\n    return (1 + x) ** 12 - 1\n", 2),
    ("def f(x):\n    x /= 12\n    return x\n", 2),
    ("def f(t):\n    return divmod(t, 12)\n", 2),
    # Formes de #102 : constante de module, appels, conversion, argument nommé,
    # facteurs non directs.
    ("DOUZE = 12\ndef f(x):\n    return x / DOUZE\n", 1),
    ("import numpy as np\nnp.divide(y, 12)\n", 2),
    ("import operator\noperator.truediv(y, 12)\n", 2),
    ("import math\nmath.pow(y, 12)\n", 2),
    ("import math\nmath.fmod(t, 12)\n", 2),
    ("def f(y):\n    return y / float(12)\n", 2),
    ("def f(t):\n    return divmod(t, b=12)\n", 2),
    ("def f(x):\n    return x / (2 * 12)\n", 2),
    ("def f(x, y):\n    return 12 * x / y\n", 2),
    # Autres places et écritures.
    ("def f(x):\n    return x * 12\n", 2),
    ("def f(x):\n    return x + 12\n", 2),
    ("def f(r, x):\n    return r[12] / x\n", 2),
    ("def f(x, n=12):\n    return x / n\n", 1),
    ("def f(x):\n    return x / 0xC\n", 2),
    ("def f(x):\n    return x / 1.2e1\n", 2),
])
def test_le_controle_du_douze_releve_les_formes_adverses(texte, ligne):
    """Chaque forme est relevée, à sa ligne."""
    assert douzes_du_texte(texte) == [ligne]


@pytest.mark.parametrize("texte", [
    "def f(x):\n    return x / 13\n",
    "def f(x):\n    return x / PAS_PAR_AN.valeur\n",
    "def f(t):\n    return divmod(t, 7)\n",
    "def f(x):\n    return x / True\n",
    "def f(x):\n    return abs(x) < 1e-12\n",
    "LIGNE = \"12\"\n",
    "# 12 en commentaire\nx = 1\n",
])
def test_le_controle_du_douze_ne_releve_pas_le_reste(texte):
    """Autre nombre, n_a nommé, booléen, 1e-12, chaîne « 12 », commentaire : non relevés."""
    assert douzes_du_texte(texte) == []
