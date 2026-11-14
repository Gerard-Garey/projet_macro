"""Tables de paramètres des blocs 7 (banque) et 8 (banque centrale) (issue #61, rang 3 de J3-c).

Contrat : ADR 0012, F1 et F2 ; ADR 0013, annotation du 14/11/2026, points 2 et 6
(P96) ; synthèse du rang 1a de J3-c, § 6. Chaque test énonce une propriété : noms,
unités et domaines de l'annotation, type porté par l'unité, domaine refusé sans
écrêtage à toute construction, une seule maison par paramètre, égalité des
valeurs indicatives avec le script d'état stationnaire (H3.3), le script nommant
`pi_cible` et `rbar` ce que la table nomme `pi_etoile` et `r_bar`.
"""

import dataclasses
import math

import pytest

from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres import TauxDeCroissance, TauxDeFlux, varier
from nations.moteur.parametres import (
    banque,
    banque_centrale,
    investissement,
    prix,
    production,
    travail,
)
from nations.moteur.parametres.cadre import PAS_PAR_AN

N_A = PAS_PAR_AN.valeur

TABLES = (
    (banque.BANQUE, banque.PARAMETRES_DE_LA_BANQUE),
    (banque_centrale.BANQUE_CENTRALE, banque_centrale.PARAMETRES_DE_LA_BANQUE_CENTRALE),
)
DECLARATIONS = tuple(p for _, declarations in TABLES for p in declarations)

# Annotation du 14/11/2026, point 6 : nom → (valeur, unité).
ATTENDUS = {
    "varpi_L": (0.02, "par an, taux de flux"), "varpi_D": (0.01, "par an, taux de flux"),
    "vartheta": (0.10, "fraction"),
    "a_pi": (0.5, "sans dimension"), "a_I": (0.25, "par an, taux de flux"),
    "lambda_e": (0.2, "par an, taux de flux"), "theta_CB": (0.0, "fraction"),
    "pi_etoile": (0.02, "par an, taux de croissance"),
    "r_bar": (0.01, "par an, taux de croissance"),
}
# Noms du script (`Parametres` de `outils/etat_stationnaire.py`) qui diffèrent (point 6).
NOMS_DU_SCRIPT = {"pi_etoile": "pi_cible", "r_bar": "rbar"}


def test_noms_ordre_valeurs_et_unites_de_l_annotation():
    """Point 6 : trois paramètres de la banque, six de la banque centrale, dans l'ordre de
    l'annotation, aux valeurs et unités déclarées ; aucune unité nouvelle (P96)."""
    assert [[p.nom for p in d] for _, d in TABLES] == [
        ["varpi_L", "varpi_D", "vartheta"],
        ["a_pi", "a_I", "lambda_e", "theta_CB", "pi_etoile", "r_bar"]]
    for p in DECLARATIONS:
        assert (p.valeur, p.unite) == ATTENDUS[p.nom], p.nom
        assert p.source


def test_labels_du_bloc_ou_de_gamma_e():
    """Chaque paramètre porte au moins un label `eq:` de son bloc (fiches 7 et 8, § 9.1) ; π*
    porte ceux des équations qui la lisent, BC1, BC2 et BC4, et celui de Γ^e
    (`eq:moteur-croissance-nominale-attendue`, ADR 0010)."""
    for table, declarations in TABLES:
        radical = "banque_centrale" if table is banque_centrale.BANQUE_CENTRALE else "banque"
        for p in declarations:
            assert p.etiquettes and all(
                e.startswith(f"eq:{radical}-") or e == "eq:moteur-croissance-nominale-attendue"
                for e in p.etiquettes), p.nom
    # π* est lue par BC1 (règle), BC2 (taux neutre, C1 de `monnaie`), BC4 (cible) et Γ^e.
    assert banque_centrale.PI_ETOILE.etiquettes == (
        "eq:banque_centrale-cible", "eq:banque_centrale-regle-taux",
        "eq:banque_centrale-taux-neutre", "eq:moteur-croissance-nominale-attendue")


def test_une_seule_maison_par_parametre():
    """Aucun nom des tables des blocs 7 et 8 n'est dans une autre table : π* n'a qu'une maison."""
    autres = {p.nom for module, nom in ((production, "PARAMETRES_DE_LA_PRODUCTION"),
                                        (travail, "PARAMETRES_DU_TRAVAIL"),
                                        (prix, "PARAMETRES_DES_PRIX"),
                                        (investissement, "PARAMETRES_DE_L_INVESTISSEMENT"))
              for p in getattr(module, nom)}
    noms = [p.nom for p in DECLARATIONS]
    assert len(noms) == len(set(noms)) == 9
    assert not set(noms) & autres


def test_type_porte_par_l_unite():
    """F2 : un taux annuel est porté sous le type de sa nature, lu dans l'unité ; tout autre
    paramètre en `float` ; la table est gelée."""
    for table, declarations in TABLES:
        assert type(table).DECLARATIONS == declarations
        for p in declarations:
            valeur = getattr(table, p.nom)
            if p.unite == "par an, taux de flux":
                assert type(valeur) is TauxDeFlux and valeur.valeur == p.valeur
            elif p.unite == "par an, taux de croissance":
                assert type(valeur) is TauxDeCroissance and valeur.valeur == p.valeur
            else:
                assert type(valeur) is float and valeur == p.valeur
        with pytest.raises(dataclasses.FrozenInstanceError):
            setattr(table, declarations[0].nom, declarations[0].valeur)


BC = banque_centrale.BANQUE_CENTRALE
BK = banque.BANQUE
# Valeurs hors domaine (point 6), refusées à toute construction.
HORS_DOMAINE = [
    (BC, "a_pi", 0.0), (BC, "a_pi", 1.5), (BC, "a_pi", -0.5), (BC, "a_pi", math.nan),
    (BC, "a_I", 0.0), (BC, "a_I", -0.25),
    (BC, "lambda_e", 0.0), (BC, "lambda_e", N_A + 1e-9), (BC, "lambda_e", -0.2),
    (BC, "theta_CB", -1e-12), (BC, "theta_CB", 1.0000000000000002),
    (BC, "pi_etoile", -1.0), (BC, "pi_etoile", -2.0), (BC, "pi_etoile", math.nan),
    (BC, "pi_etoile", math.inf),
    (BC, "r_bar", -0.05), (BC, "r_bar", -1.0), (BC, "r_bar", math.nan),
    (BK, "vartheta", 0.0), (BK, "vartheta", -0.1),
    (BK, "varpi_L", math.inf), (BK, "varpi_D", math.nan),
]


@pytest.mark.parametrize("table, nom, valeur", HORS_DOMAINE)
def test_domaine_refuse_par_le_constructeur_valide(table, nom, valeur):
    """Hors domaine : `DefautDeDeclaration` qui nomme le paramètre, jamais un écrêtage."""
    with pytest.raises(DefautDeDeclaration, match=f"« {nom} ».*(domaine|taux)"):
        varier(table, **{nom: valeur})


def test_bornes_et_signes_admis():
    """Bornes incluses : λ_e = n_a (P65), θ_CB = 0 et 1 ; bornes exclues voisines : r̄ juste
    au-dessus de −5 % (C51), π* juste au-dessus de −1, a_π juste sous 1,5 ; ϖ_L et ϖ_D sans
    condition de signe (négatifs admis, nuls admis)."""
    varier(BC, lambda_e=float(N_A), theta_CB=0.0)
    varier(BC, theta_CB=1.0, r_bar=math.nextafter(-0.05, 0.0),
           pi_etoile=math.nextafter(-1.0, 0.0), a_pi=math.nextafter(1.5, 0.0))
    varie = varier(BK, varpi_L=-0.03, varpi_D=-0.01)
    assert varie.varpi_L == TauxDeFlux(-0.03) and varie.varpi_D == TauxDeFlux(-0.01)
    varier(BK, varpi_L=0.0, varpi_D=0.0, vartheta=5e-324)


def test_valeurs_indicatives_egales_a_celles_du_script(stationnaire):
    """H3.3 : chaque paramètre des deux tables vaut, au bit, la valeur par défaut de
    `Parametres` du script, sous le nom du script (`pi_cible`, `rbar` pour `pi_etoile`,
    `r_bar`) ; le script n'est pas renommé."""
    defaut = stationnaire.Parametres()
    for p in DECLARATIONS:
        nom = NOMS_DU_SCRIPT.get(p.nom, p.nom)
        valeur = getattr(defaut, nom)
        assert type(valeur) is float and valeur.hex() == p.valeur.hex(), p.nom
    for nom in NOMS_DU_SCRIPT:
        assert not hasattr(defaut, nom)


def test_domaines_des_tables_et_du_script_refusent_le_meme_ensemble(stationnaire):
    """Les domaines de la table du bloc 8 et de ϑ refusent ce que le script refuse : r̄ ≤ −5 %
    (C51), a_π hors de ]0 ; 1,5[, a_I ≤ 0, θ_CB hors de [0 ; 1], ϑ ≤ 0 ; la calibration passe
    les deux."""
    base = dataclasses.replace(stationnaire.Parametres(), nu_G=1.15)
    stationnaire.controler_domaine(base)
    for table, nom, valeur in ((BC, "r_bar", -0.05), (BC, "r_bar", -0.2), (BC, "a_pi", 0.0),
                               (BC, "a_pi", 1.5), (BC, "a_I", 0.0), (BC, "theta_CB", -0.1),
                               (BC, "theta_CB", 1.1), (BK, "vartheta", 0.0)):
        with pytest.raises(DefautDeDeclaration):
            varier(table, **{nom: valeur})
        with pytest.raises(stationnaire.HorsDomaine):
            stationnaire.controler_domaine(
                dataclasses.replace(base, **{NOMS_DU_SCRIPT.get(nom, nom): valeur}))
