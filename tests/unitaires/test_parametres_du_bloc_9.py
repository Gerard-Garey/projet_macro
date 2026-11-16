"""Table de paramètres du bloc 9, État et dette (#132 ; P165 ; ADR 0013, annotation du 15/11/2026,
point 8).

Chaque test énonce une propriété : noms, unités, labels ; type `float` ; domaine refusé sans
écrêtage à toute construction (`sec:finances_publiques-conditions`) ; une seule maison par
paramètre (U^eq au travail, r̄ et θ_CB à la banque centrale) ; valeurs indicatives égales à
celles du script d'état stationnaire (H3.3), sauf ν_G = 1,15 (valeur retenue, le défaut du
script, 1, étant hors domaine) et θ_G, résolu par le script à π* = 2 % ; refus du même ensemble
que le script ; place dans `EnsembleDesParametres`.
"""

import dataclasses
import math

import pytest

from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres import finances_publiques as table_9
from nations.moteur.parametres import varier
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE, EnsembleDesParametres

TABLE = table_9.FINANCES_PUBLIQUES
DECLARATIONS = table_9.PARAMETRES_DES_FINANCES_PUBLIQUES
ATTENDUS = {"nu_G": (1.15, "sans dimension"), "theta_Tr": (0.0, "fraction"),
            "tau_H": (0.25, "fraction"), "tau_F": (0.0, "fraction"),
            "phi": (1.0, "sans dimension")}


def test_noms_ordre_unites_et_labels():
    """P165 : ν_G, θ_G, θ_Tr, τ_H, τ_F, φ, dans cet ordre, `float`, chacun avec une source et au
    moins un label `eq:finances_publiques-…` ; table gelée ; dernier champ de l'ensemble."""
    assert [p.nom for p in DECLARATIONS] == ["nu_G", "theta_G", "theta_Tr", "tau_H", "tau_F",
                                             "phi"]
    for p in DECLARATIONS:
        if p.nom in ATTENDUS:
            assert (p.valeur, p.unite) == ATTENDUS[p.nom], p.nom
        assert p.source and all(e.startswith("eq:finances_publiques-") for e in p.etiquettes)
        assert type(getattr(TABLE, p.nom)) is float
    assert table_9.THETA_G.unite == "fraction"
    with pytest.raises(dataclasses.FrozenInstanceError):
        TABLE.nu_G = 1.2
    assert [f.name for f in dataclasses.fields(EnsembleDesParametres)][-1] == "finances_publiques"
    assert PARAMETRES_DE_REFERENCE.finances_publiques is TABLE


def test_une_seule_maison_par_parametre():
    """H3.3 : aucun nom de la table n'est dans une autre table ; U^eq (E1, E6) reste au travail,
    r̄ (E4) et θ_CB (E10) à la banque centrale, lus par la vue."""
    noms = {p.nom for p in DECLARATIONS}
    for f in dataclasses.fields(EnsembleDesParametres):
        if f.name in ("cadre", "finances_publiques"):
            continue
        autre = getattr(PARAMETRES_DE_REFERENCE, f.name)
        assert not noms & {g.name for g in dataclasses.fields(autre)}, f.name
    assert hasattr(PARAMETRES_DE_REFERENCE.travail, "U_eq")
    assert hasattr(PARAMETRES_DE_REFERENCE.banque_centrale, "r_bar")


HORS_DOMAINE = [("nu_G", 1.0), ("nu_G", 0.9), ("nu_G", math.nan), ("nu_G", math.inf),
                ("theta_G", -1e-12), ("theta_G", math.nan), ("theta_Tr", -0.01),
                ("tau_H", 1.0), ("tau_H", -1e-12), ("tau_F", 1.0), ("tau_F", -0.1),
                ("phi", 0.5), ("phi", -1.0), ("phi", 2.0), ("phi", math.nan)]


@pytest.mark.parametrize("nom, valeur", HORS_DOMAINE)
def test_domaine_refuse_a_toute_construction(nom, valeur):
    """`sec:finances_publiques-conditions` : 0 ≤ τ_H < 1, 0 ≤ τ_F < 1, θ_G ≥ 0, θ_Tr ≥ 0,
    φ ∈ {0 ; 1}, ν_G > 1 ; hors domaine, `DefautDeDeclaration` qui nomme le paramètre, jamais un
    écrêtage, par `varier` comme par `dataclasses.replace`."""
    with pytest.raises(DefautDeDeclaration, match=f"« {nom} ».*domaine"):
        varier(TABLE, **{nom: valeur})
    with pytest.raises(DefautDeDeclaration, match=nom):
        dataclasses.replace(TABLE, **{nom: valeur})


def test_bornes_admises():
    """Bornes incluses : τ_H = τ_F = θ_G = θ_Tr = 0, φ = 0 et 1 ; bornes exclues voisines : ν_G
    juste au-dessus de 1, τ_H et τ_F juste sous 1."""
    varier(TABLE, tau_H=0.0, tau_F=0.0, theta_G=0.0, theta_Tr=0.0, phi=0.0)
    varier(TABLE, nu_G=math.nextafter(1.0, 2.0), tau_H=math.nextafter(1.0, 0.0),
           tau_F=math.nextafter(1.0, 0.0), phi=1.0)


def test_valeurs_indicatives_egales_a_celles_du_script(stationnaire):
    """H3.3 : θ_Tr, τ_H, τ_F et φ valent au bit les défauts de `Parametres` du script ; ν_G vaut la
    valeur retenue 1,15, le défaut du script (1, point de référence) étant hors domaine ; θ_G vaut
    au bit le θ_G résolu par le script à π* = 2 % et ν_G = 1,15 (indépendant de ν_G, C59)."""
    defaut = stationnaire.Parametres()
    for nom in ("theta_Tr", "tau_H", "tau_F", "phi"):
        assert getattr(defaut, nom).hex() == getattr(TABLE, nom).hex(), nom
    assert defaut.nu_G == 1.0 and TABLE.nu_G == 1.15
    for nu_G in (1.0, 1.15):
        par = dataclasses.replace(defaut, pi_cible=0.02, nu_G=nu_G)
        assert stationnaire.etat_stationnaire(par)["theta_G"].hex() == TABLE.theta_G.hex()


def test_table_et_script_refusent_le_meme_ensemble(stationnaire):
    """Les domaines de la table refusent ce que le script refuse (τ_H, τ_F hors de [0 ; 1[,
    θ_Tr < 0, φ ∉ {0 ; 1}, ν_G < 1) ; ν_G = 1 est refusé par la table et admis par le script comme
    point de référence de la forme fermée, déclaré (décision du 05/10/2026)."""
    base = dataclasses.replace(stationnaire.Parametres(), nu_G=1.15)
    stationnaire.controler_domaine(base)
    for nom, valeur in (("tau_H", 1.0), ("tau_F", -0.1), ("theta_Tr", -0.01), ("phi", 0.5),
                        ("nu_G", 0.9)):
        with pytest.raises(DefautDeDeclaration):
            varier(TABLE, **{nom: valeur})
        with pytest.raises(stationnaire.HorsDomaine):
            stationnaire.controler_domaine(dataclasses.replace(base, **{nom: valeur}))
    declares = stationnaire.controler_domaine(dataclasses.replace(base, nu_G=1.0))
    assert any("ν_G = 1" in d for d in declares)
    with pytest.raises(DefautDeDeclaration):
        varier(TABLE, nu_G=1.0)


def test_ensemble_refuse_une_autre_table():
    """H3.5 : le champ `finances_publiques` de l'ensemble est de type exact."""
    with pytest.raises(DefautDeDeclaration, match="finances_publiques"):
        dataclasses.replace(PARAMETRES_DE_REFERENCE,
                            finances_publiques=PARAMETRES_DE_REFERENCE.menages)
