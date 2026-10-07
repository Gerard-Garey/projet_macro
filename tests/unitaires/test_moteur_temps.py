"""Moteur : calendrier, conversions, paramètres typés, registre de l'indice des prix (issue #97).

Contrat : ADR 0012, C3, F1 à F3 ; ADR 0005, points 1 à 4 et 18 ; ADR 0008,
parties I et II ; critères de #97 et leurs compléments du rang 1b (C97-1 à
C97-3). Chaque test énonce une propriété. Le registre sur une trajectoire
(C97-1, C97-2) est testé avec l'ordonnanceur (`test_moteur_ordonnanceur.py`).
"""

import ast
import math
import struct
from pathlib import Path

import pytest

from nations.etat import schema
from nations.etat.unites import UNITES
from nations.moteur import calendrier, registre
from nations.moteur.conversions import facteur_par_pas, par_pas
from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.ouverture import GRANDEURS_OUVERTURE, GrandeurOuverture
from nations.moteur.parametres import (
    ENTIER_STRICTEMENT_POSITIF,
    Domaine,
    Parametre,
    TauxDeCroissance,
    TauxDeFlux,
    taux_du_parametre,
)
from nations.moteur.parametres.cadre import (
    CADRE,
    PARAMETRES_DU_CADRE,
    PAS_PAR_AN,
    PAS_PAR_TOUR,
    TOLERANCE_IDENTITE_CUMULEE,
    TOLERANCE_IDENTITE_PAS,
)

RACINE = Path(__file__).resolve().parents[2]
MOTEUR = RACINE / "src" / "nations" / "moteur"
N_A = PAS_PAR_AN.valeur

# Taux annuels d'essai : nuls, petits, courants, grands, négatifs.
TAUX = (0.0, 1e-9, 0.005, 0.02, 0.04, 0.1, 0.5, 1.0, 3.0, -0.02, -0.3, -0.9)


def bits(x):
    return struct.pack("<d", x)


# --------------------------------------------------------------------------
# Paramètres du cadre (F1, F2 ; ADR 0005, point 18)
# --------------------------------------------------------------------------


def test_quatre_parametres_du_cadre():
    """n_a = 12, n_m = 1, ε = ε_V = 1e−12 (M22), chacun avec unité, source et étiquette."""
    assert [(p.nom, p.symbole, p.valeur, p.unite) for p in PARAMETRES_DU_CADRE] == [
        ("pas_par_an", "n_a", 12, "pas par an"),
        ("pas_par_tour", "n_m", 1, "pas par tour"),
        ("tolerance_identite_pas", "ε", 1e-12, "sans dimension"),
        ("tolerance_identite_cumulee", "ε_V", 1e-12, "sans dimension"),
    ]
    for p in PARAMETRES_DU_CADRE:
        assert "M22" in p.source
        assert p.etiquettes and all(e.startswith("eq:") for e in p.etiquettes)
        assert p.unite in UNITES
    assert TOLERANCE_IDENTITE_PAS.etiquettes == ("eq:noyau-tolerance-pas",)
    assert TOLERANCE_IDENTITE_CUMULEE.etiquettes == ("eq:noyau-tolerance-cumulee",)
    assert PAS_PAR_TOUR.etiquettes == ("eq:moteur-date-decision",)
    assert set(PAS_PAR_AN.etiquettes) == {
        "eq:moteur-calendrier-date", "eq:moteur-conversion-taux",
        "eq:moteur-conversion-croissance", "eq:moteur-registre-prix", "eq:moteur-glissement"}


def test_cadre_engendre_des_declarations_et_lu_par_le_noyau():
    """`CADRE` porte les quatre valeurs sous leur nom, aux types que le noyau exige."""
    for p in PARAMETRES_DU_CADRE:
        assert getattr(CADRE, p.nom) is p.valeur
    assert type(CADRE.tolerance_identite_pas) is float
    assert type(CADRE.tolerance_identite_cumulee) is float
    with pytest.raises(AttributeError):
        CADRE.pas_par_an = 4


def test_registre_du_schema_de_n_a_plus_un_niveaux():
    """Le registre du schéma d'état a n_a + 1 niveaux (ADR 0008, II.3)."""
    assert registre.NIVEAUX == N_A + 1 == schema.NIVEAUX_DU_REGISTRE
    assert schema.VARIABLE["registre_prix"].longueur == registre.NIVEAUX


@pytest.mark.parametrize("champ, valeur, motif", [
    ("unite", "mètres", "vocabulaire"),
    ("valeur", 0, "domaine"),
    ("valeur", 12.0, "domaine"),
    ("valeur", True, "domaine"),
    ("source", "", "source"),
    ("etiquettes", (), "label"),
    ("etiquettes", ("moteur-x",), "label"),
    ("nom", "pas par an", "nom"),
])
def test_parametre_refuse_hors_domaine_ou_vocabulaire(champ, valeur, motif):
    """F1 : un paramètre hors domaine, d'unité inconnue, sans source ni label est refusé."""
    champs = {"nom": "pas_par_an", "symbole": "n_a", "valeur": 12, "unite": "pas par an",
              "source": "M22", "etiquettes": ("eq:moteur-conversion-taux",),
              "domaine": ENTIER_STRICTEMENT_POSITIF}
    Parametre(**champs)
    champs[champ] = valeur
    with pytest.raises(DefautDeDeclaration, match=motif):
        Parametre(**champs)


@pytest.mark.parametrize("parametre, valeur", [
    (PAS_PAR_AN, 0), (PAS_PAR_TOUR, 2), (PAS_PAR_TOUR, 0),
    (TOLERANCE_IDENTITE_PAS, 0.0), (TOLERANCE_IDENTITE_PAS, -1e-12),
    (TOLERANCE_IDENTITE_PAS, math.inf), (TOLERANCE_IDENTITE_CUMULEE, math.nan),
])
def test_domaines_du_cadre(parametre, valeur):
    """Les domaines déclarés du cadre refusent, jamais n'écrêtent."""
    with pytest.raises(DefautDeDeclaration, match="domaine"):
        Parametre(parametre.nom, parametre.symbole, valeur, parametre.unite, parametre.source,
                  parametre.etiquettes, parametre.domaine)


def _taux(unite):
    return Parametre("i", "i", 0.04, unite, "essai", ("eq:moteur-conversion-taux",),
                     Domaine("float", lambda x: type(x) is float))


def test_type_du_taux_construit_depuis_l_unite():
    """F2 : l'unité porte la nature, le type porte la conversion."""
    assert type(taux_du_parametre(_taux("par an, taux de flux"))) is TauxDeFlux
    assert type(taux_du_parametre(_taux("par an, taux de croissance"))) is TauxDeCroissance
    with pytest.raises(DefautDeDeclaration, match="pas un taux"):
        taux_du_parametre(_taux("sans dimension"))


# --------------------------------------------------------------------------
# Conversions (F2 ; critère de #97)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("x", TAUX)
def test_somme_des_x_sur_n_a_sur_n_a_pas_vaut_x(x):
    """Σ des X/n_a sur n_a pas = X, à 1e−12 relatif (critère de #97)."""
    somme = 0.0
    for _ in range(N_A):
        somme += par_pas(TauxDeFlux(x))
    assert abs(somme - x) <= 1e-12 * abs(x)


@pytest.mark.parametrize("x", [x for x in TAUX if x > -1.0])
def test_produit_de_n_a_facteurs_vaut_un_plus_x(x):
    """Π de n_a facteurs (1 + x)^{1/n_a} = 1 + x, à 1e−12 relatif (critère de #97)."""
    produit = 1.0
    for _ in range(N_A):
        produit *= facteur_par_pas(TauxDeCroissance(x))
    assert abs(produit - (1.0 + x)) <= 1e-12 * (1.0 + x)


def test_deux_pour_cent_par_an_donnent_0_16516_pour_cent_par_pas():
    """`sec:cadre-calendrier` : 2 % par an donnent 0,16516 % par pas à n_a = 12."""
    assert round((facteur_par_pas(TauxDeCroissance(0.02)) - 1.0) * 100, 5) == 0.16516
    assert par_pas(TauxDeFlux(0.04)) == 0.04 / 12


def test_chaque_conversion_n_accepte_que_son_type():
    """ADR 0008, I.3 : aucune conversion à argument de nature ; le mauvais type est refusé."""
    with pytest.raises(TypeError, match="TauxDeFlux attendu"):
        par_pas(TauxDeCroissance(0.02))
    with pytest.raises(TypeError, match="TauxDeCroissance attendu"):
        facteur_par_pas(TauxDeFlux(0.02))
    with pytest.raises(TypeError):
        par_pas(0.02)
    with pytest.raises(TypeError):
        facteur_par_pas(0.02)


@pytest.mark.parametrize("valeur", [-1.0, -2.0, math.inf, math.nan, 1])
def test_taux_de_croissance_hors_domaine(valeur):
    with pytest.raises(DefautDeDeclaration):
        TauxDeCroissance(valeur)


def test_conversions_seules_a_diviser_par_n_a_dans_le_moteur():
    """Aucune division ni puissance par `PAS_PAR_AN` ou `pas_par_an` hors des deux conversions.

    Contrôle textuel restreint à `src/nations/moteur/` (celui de tout `src/`
    relève de #98) : toute opération `/`, `//` ou `**` dont un opérande
    nomme n_a, hors de `par_pas` et `facteur_par_pas`, est un écart.
    """
    def nomme_n_a(noeud):
        # Un indice (`registre[PAS_PAR_AN.valeur]`) n'est pas un diviseur.
        if isinstance(noeud, ast.Subscript):
            return False
        if (isinstance(noeud, ast.Name) and noeud.id in ("PAS_PAR_AN", "pas_par_an", "N_A")) or (
                isinstance(noeud, ast.Attribute) and noeud.attr == "pas_par_an"):
            return True
        return any(nomme_n_a(enfant) for enfant in ast.iter_child_nodes(noeud))

    ecarts = []
    for chemin in sorted(MOTEUR.rglob("*.py")):
        arbre = ast.parse(chemin.read_text(encoding="utf-8"))
        permis = {id(n) for f in ast.walk(arbre) if isinstance(f, ast.FunctionDef)
                  and f.name in ("par_pas", "facteur_par_pas") for n in ast.walk(f)}
        for noeud in ast.walk(arbre):
            if (isinstance(noeud, ast.BinOp)
                    and isinstance(noeud.op, (ast.Div, ast.FloorDiv, ast.Pow))
                    and id(noeud) not in permis and nomme_n_a(noeud.right)):
                ecarts.append(f"{chemin.name}:{noeud.lineno}")
    assert ecarts == []


# --------------------------------------------------------------------------
# Calendrier (critères de #97 et C97-3)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("tour, annee, mois", [
    (1, 1, 1), (12, 1, 12), (13, 2, 1), (25, 3, 1), (24, 2, 12), (721, 61, 1),
])
def test_date_d_un_tour(tour, annee, mois):
    """Tour 13 = mois 1 de l'année 2 ; tour 25 = mois 1 de l'année 3 (égalités exactes)."""
    assert calendrier.date(calendrier.pas_du_tour(tour)) == (annee, mois)


@pytest.mark.parametrize("t, attendu", [(0, (1, 1)), (11, (1, 12)), (12, (2, 1))])
def test_bornes_du_calendrier(t, attendu):
    """C97-3 : t = 0, 11, 12 donnent (1, 1), (1, 12), (2, 1)."""
    assert calendrier.date(t) == attendu


def test_tour_et_pas_reciproques():
    """t = n − 1, pour tous les tours de 60 ans."""
    for t in range(721):
        assert calendrier.pas_du_tour(calendrier.tour_du_pas(t)) == t
        assert calendrier.tour_du_pas(t) == t + 1


def test_date_de_decision_a_tout_pas():
    """Sous n_m = 1, tout pas est une date de décision, déduite de t seul."""
    assert all(calendrier.est_date_de_decision(t) for t in range(721))


@pytest.mark.parametrize("fonction", [calendrier.date, calendrier.est_date_de_decision,
                                      calendrier.tour_du_pas])
@pytest.mark.parametrize("t", [-1, 1.0, True])
def test_calendrier_refuse_un_pas_hors_domaine(fonction, t):
    with pytest.raises(ValueError):
        fonction(t)


def test_grandeurs_d_ouverture_du_j2():
    """C3 : date affichée et prédicat de date de décision, chacun avec label et unité."""
    assert [(g.nom, g.label) for g in GRANDEURS_OUVERTURE] == [
        ("annee", "eq:moteur-calendrier-date"), ("mois", "eq:moteur-calendrier-date"),
        ("date_de_decision", "eq:moteur-date-decision")]
    # Rangs et prédicat : « sans dimension », le type portant la nature ; le
    # vocabulaire des unités n'est pas étendu (annotation du 07/10/2026, point 6).
    assert {g.unite for g in GRANDEURS_OUVERTURE} == {"sans dimension"}

    class Ouverture:
        t = 25

    valeurs = {}
    for g in GRANDEURS_OUVERTURE:
        valeurs[g.nom] = g.fonction(Ouverture(), CADRE, valeurs)
    assert valeurs == {"annee": 3, "mois": 2, "date_de_decision": True}
    with pytest.raises(ValueError, match="unité"):
        GrandeurOuverture("x", lambda e, p, g: 0, None, "mois")


# --------------------------------------------------------------------------
# Registre : fonctions (F3) ; trajectoire : test_moteur_ordonnanceur.py
# --------------------------------------------------------------------------


def niveaux(pi_barre, dernier=1.0):
    """Registre stationnaire : P_{t−u} = P_{t−1} (1 + π̄)^{−(u−1)/n_a}, u = 1 … 13."""
    return tuple(dernier * (1.0 + pi_barre) ** (-(u - 1) / N_A) for u in range(1, N_A + 2))


def test_lectures_du_registre():
    """dernier prix P_{t−1} ; glissement P_{t−1}/P_{t−13} − 1 ; variation sur le tour P_{t−1}/P_{t−2} − 1."""
    r = tuple(float(100 - u) for u in range(1, 14))
    assert registre.dernier_prix(r) == 99.0
    assert registre.glissement(r) == 99.0 / 87.0 - 1.0
    assert registre.variation_sur_le_tour(r) == 99.0 / 98.0 - 1.0


@pytest.mark.parametrize("pi_barre", [0.0, 0.02, 0.10])
def test_glissement_stationnaire_egal_a_pi_barre(pi_barre):
    """Sur un registre stationnaire, (1 + π_{t−1})/(1 + π̄) − 1 est nul à 1e−12 près."""
    assert abs((1.0 + registre.glissement(niveaux(pi_barre))) / (1.0 + pi_barre) - 1.0) <= 1e-12


def test_avancer_copie_sans_calcul():
    """C97-2 : (P_t, P_{t−1}, …, P_{t−12}) bit à bit ; P_{t−13} sort."""
    r = tuple(1.0 + 0.1 * u + 1e-17 * u for u in range(13))
    p = 0.1 + 0.2
    suivant = registre.avancer(r, p)
    assert [bits(x) for x in suivant] == [bits(p)] + [bits(x) for x in r[:12]]


@pytest.mark.parametrize("registre_faux", [(1.0,) * 12, (1.0,) * 14, [1.0] * 13])
def test_registre_de_mauvaise_forme_refuse(registre_faux):
    for fonction in (registre.dernier_prix, registre.glissement, registre.variation_sur_le_tour):
        with pytest.raises(ValueError):
            fonction(registre_faux)
    with pytest.raises(ValueError):
        registre.avancer(registre_faux, 1.0)


@pytest.mark.parametrize("prix", [0.0, -1.0, math.inf, math.nan, 1])
def test_avancer_refuse_un_indice_hors_domaine(prix):
    with pytest.raises(ValueError):
        registre.avancer((1.0,) * 13, prix)


def test_seul_le_registre_indexe_le_registre_dans_le_moteur():
    """F3 : hors de `registre.py`, aucun indice ni tranche appliqué à `registre_prix`."""
    ecarts = []
    for chemin in sorted(MOTEUR.rglob("*.py")):
        if chemin.name == "registre.py":
            continue
        for noeud in ast.walk(ast.parse(chemin.read_text(encoding="utf-8"))):
            if isinstance(noeud, ast.Subscript) and "registre" in ast.unparse(noeud.value):
                ecarts.append(f"{chemin.name}:{noeud.lineno}")
    assert ecarts == []
