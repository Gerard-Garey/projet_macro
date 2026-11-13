"""Tables de paramètres des blocs 2 à 4 et δ, ensemble des tables (issue #112).

Contrat : ADR 0012, F1 et F2, et annotation du 13/11/2026, point 3 (P63, P65,
P68 à P71) ; synthèse du rang 1a de J3-b, § 3 (unités). Chaque test énonce une
propriété : unité du vocabulaire fermé, type porté par l'unité, domaine refusé
sans écrêtage à toute construction, une seule maison par paramètre, égalité des
valeurs indicatives avec le script d'état stationnaire (P63).
"""

import dataclasses
import math

import pytest

from nations.etat.unites import UNITES
from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.ordonnanceur import DeclarationDesEntrees, assembler
from nations.moteur.parametres import TauxDeCroissance, TauxDeFlux, varier
from nations.moteur.parametres import investissement, prix, production, travail
from nations.moteur.parametres.cadre import CADRE, PAS_PAR_AN
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE, EnsembleDesParametres
from nations.moteur.phases import PHASES

N_A = PAS_PAR_AN.valeur

# (module, table de référence, déclarations), dans l'ordre des blocs.
TABLES = (
    (production, production.PRODUCTION, production.PARAMETRES_DE_LA_PRODUCTION),
    (travail, travail.TRAVAIL, travail.PARAMETRES_DU_TRAVAIL),
    (prix, prix.PRIX, prix.PARAMETRES_DES_PRIX),
    (investissement, investissement.INVESTISSEMENT, investissement.PARAMETRES_DE_L_INVESTISSEMENT),
)
DECLARATIONS = tuple(p for _, _, declarations in TABLES for p in declarations)

# Unités de la synthèse du rang 1a (§ 3 ; P65).
UNITES_ATTENDUES = {
    "lambda_v": "par an, taux de flux", "lambda_IN": "par an, taux de flux",
    "lambda_w": "par an, taux de flux", "lambda_N": "par an, taux de flux",
    "lambda_mu": "par an, taux de flux", "delta": "par an, taux de flux",
    "sigma": "années", "kappa": "années",
    "g_pr": "par an, taux de croissance", "g_N": "par an, taux de croissance",
    "U_eq": "fraction", "mu_bar": "fraction",
    "beta": "sans dimension", "psi_xi": "sans dimension",
}


def test_quatorze_parametres_un_seul_par_maison():
    """Point 3 : λ_v, λ_IN, σ, g_pr, κ ; λ_w, β, U^eq, λ_N, g_N ; μ̄, λ_μ, ψ_ξ ; δ. Un nom
    n'apparaît que dans une table (g_pr dans la production, μ̄ dans les prix, δ dans
    l'investissement, P68)."""
    assert [[p.nom for p in d] for _, _, d in TABLES] == [
        ["lambda_v", "lambda_IN", "sigma", "g_pr", "kappa"],
        ["lambda_w", "beta", "U_eq", "lambda_N", "g_N"],
        ["mu_bar", "lambda_mu", "psi_xi"],
        ["delta"],
    ]
    noms = [p.nom for p in DECLARATIONS]
    assert len(noms) == len(set(noms)) == 14
    assert not {f.name for f in dataclasses.fields(CADRE)} & set(noms)


def test_unites_du_vocabulaire_ferme_sources_et_labels():
    """P65 : unité du vocabulaire fermé, celle de la synthèse ; chaque paramètre a une source et
    au moins un label `eq:` de son bloc ou d'un bloc lecteur."""
    for p in DECLARATIONS:
        assert p.unite in UNITES
        assert p.unite == UNITES_ATTENDUES[p.nom], p.nom
        assert p.source
        assert p.etiquettes and all(
            e.startswith(("eq:production-", "eq:travail-", "eq:prix-", "eq:investissement-"))
            for e in p.etiquettes), p.nom


def test_table_de_reference_type_porte_par_l_unite():
    """F2 : un taux annuel est porté sous le type de sa nature, lu dans l'unité ; tout autre
    paramètre en `float` ; la table de référence porte les valeurs indicatives."""
    for module, table, declarations in TABLES:
        assert type(table).DECLARATIONS == declarations
        assert [f.name for f in dataclasses.fields(table)] == [p.nom for p in declarations]
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


# Valeurs hors domaine (point 3.2 ; P70, P71), refusées à toute construction.
HORS_DOMAINE = [
    (production.PRODUCTION, "lambda_v", 0.0), (production.PRODUCTION, "lambda_v", float(N_A)),
    (production.PRODUCTION, "lambda_v", -1.0), (production.PRODUCTION, "lambda_v", math.nan),
    (production.PRODUCTION, "lambda_IN", 0.0), (production.PRODUCTION, "lambda_IN", N_A + 1e-9),
    (production.PRODUCTION, "sigma", 0.0), (production.PRODUCTION, "sigma", -0.1),
    (production.PRODUCTION, "kappa", 0.0), (production.PRODUCTION, "kappa", math.inf),
    (production.PRODUCTION, "g_pr", -1.0), (production.PRODUCTION, "g_pr", -2.0),
    (travail.TRAVAIL, "lambda_w", 0.0), (travail.TRAVAIL, "lambda_w", 13.0),
    (travail.TRAVAIL, "lambda_N", -3.5), (travail.TRAVAIL, "beta", 0.0),
    (travail.TRAVAIL, "U_eq", 0.0), (travail.TRAVAIL, "U_eq", 1.0),
    (travail.TRAVAIL, "U_eq", -0.05), (travail.TRAVAIL, "g_N", -1.0),
    (prix.PRIX, "mu_bar", 0.0), (prix.PRIX, "mu_bar", -0.1), (prix.PRIX, "mu_bar", -1.0),
    (prix.PRIX, "lambda_mu", 0.0), (prix.PRIX, "lambda_mu", 12.5),
    (prix.PRIX, "psi_xi", -1e-12), (prix.PRIX, "psi_xi", math.nan),
    (investissement.INVESTISSEMENT, "delta", 0.0),
    (investissement.INVESTISSEMENT, "delta", float(N_A)),
]


@pytest.mark.parametrize("table, nom, valeur", HORS_DOMAINE)
def test_domaine_refuse_par_le_constructeur_valide(table, nom, valeur):
    """Hors domaine : `DefautDeDeclaration` qui nomme le paramètre, jamais un écrêtage, par
    `varier` comme par `dataclasses.replace` sur la valeur typée."""
    with pytest.raises(DefautDeDeclaration, match=f"« {nom} ».*(domaine|taux)"):
        varier(table, **{nom: valeur})
    unite = next(p.unite for p in type(table).DECLARATIONS if p.nom == nom)
    if unite == "par an, taux de flux" and math.isfinite(valeur):
        with pytest.raises(DefautDeDeclaration, match=f"« {nom} ».*domaine"):
            dataclasses.replace(table, **{nom: TauxDeFlux(valeur)})
    elif unite not in ("par an, taux de flux", "par an, taux de croissance"):
        with pytest.raises(DefautDeDeclaration, match=f"« {nom} ».*domaine"):
            dataclasses.replace(table, **{nom: valeur})


@pytest.mark.parametrize("nom, motif", [
    ("U_eq", "condition de conception et d'existence de l'état stationnaire"),
    ("mu_bar", "condition de conception et d'existence de l'état stationnaire"),
    ("sigma", "domaine de définition"), ("kappa", "domaine de définition"),
    ("lambda_v", "strict"),
])
def test_motif_du_refus_nomme_la_nature(nom, motif):
    """P71 : U^eq > 0 et μ̄ > 0 sont refusés comme un domaine, le motif les nommant conditions
    de conception et d'existence ; σ, κ, domaines de définition ; λ_v, domaine strict (P70)."""
    table = next(t for _, t, d in TABLES if nom in {p.nom for p in d})
    with pytest.raises(DefautDeDeclaration, match=motif):
        varier(table, **{nom: 0.0})


def test_type_faux_refuse_meme_dans_le_domaine():
    """La nature d'un taux n'est jamais choisie au site d'appel (F2) : un `float` pour un taux,
    un taux de l'autre nature ou un taux pour un `float` sont refusés."""
    for nom, valeur in (("lambda_v", 3.0), ("lambda_v", TauxDeCroissance(3.0)),
                        ("g_pr", TauxDeFlux(0.02)), ("sigma", TauxDeFlux(0.1)), ("kappa", 2)):
        with pytest.raises(DefautDeDeclaration, match=f"« {nom} »"):
            dataclasses.replace(production.PRODUCTION, **{nom: valeur})
    with pytest.raises(DefautDeDeclaration, match="inconnu"):
        varier(production.PRODUCTION, lambda_x=1.0)


@pytest.mark.parametrize("facteur", [0.5, 2.0])
def test_vitesses_multipliees_admises(facteur):
    """Variations de test (#112, point 2) : chaque vitesse × 0,5 et × 2 reste dans son domaine
    et passe le constructeur validé, à la valeur exacte demandée."""
    vitesses = {production.PRODUCTION: ("lambda_v", "lambda_IN"),
                travail.TRAVAIL: ("lambda_w", "lambda_N"), prix.PRIX: ("lambda_mu",)}
    for table, noms in vitesses.items():
        varie = varier(table, **{n: getattr(table, n).valeur * facteur for n in noms})
        for n in noms:
            assert getattr(varie, n) == TauxDeFlux(getattr(table, n).valeur * facteur)


def test_bornes_admises():
    """Bornes incluses : λ = n_a pour les vitesses autres que λ_v, ψ_ξ = 0, g_N = 0 ; bornes
    exclues voisines admises : λ_v juste sous n_a, U^eq juste au-dessus de 0."""
    varier(production.PRODUCTION, lambda_IN=float(N_A), lambda_v=math.nextafter(N_A, 0.0))
    varier(travail.TRAVAIL, lambda_w=float(N_A), lambda_N=float(N_A), g_N=0.0, U_eq=5e-324)
    varier(prix.PRIX, lambda_mu=float(N_A), psi_xi=0.0, mu_bar=5e-324)
    varier(investissement.INVESTISSEMENT, delta=math.nextafter(N_A, 0.0))


def test_ensemble_des_tables():
    """Point 3.5 (P69) : un champ par table, chacune de son type exact ; ni champ de mode ni
    de doublure (annotation du 13/11/2026, point 6 (b)) ; variation contrôlée."""
    assert [f.name for f in dataclasses.fields(EnsembleDesParametres)] == [
        "cadre", "production", "travail", "prix", "investissement"]
    p = PARAMETRES_DE_REFERENCE
    assert (p.cadre, p.production, p.travail, p.prix, p.investissement) == (
        CADRE, production.PRODUCTION, travail.TRAVAIL, prix.PRIX, investissement.INVESTISSEMENT)
    for nom in ("cadre", "production", "travail", "prix", "investissement"):
        with pytest.raises(DefautDeDeclaration, match=nom):
            dataclasses.replace(p, **{nom: object()})
    with pytest.raises(DefautDeDeclaration, match="travail"):
        dataclasses.replace(p, travail=production.PRODUCTION)
    varie = dataclasses.replace(p, prix=varier(prix.PRIX, mu_bar=0.3))
    assert varie.prix.mu_bar == 0.3 and varie.production is p.production


def test_assembler_refuse_un_autre_objet_que_l_ensemble():
    """P69 : `assembler` (signature inchangée) refuse l'ancien objet `CADRE` ou tout autre objet,
    avant tout contrôle des blocs."""
    for parametres in (CADRE, None, production.PRODUCTION):
        with pytest.raises(DefautDeDeclaration, match="EnsembleDesParametres attendu"):
            assembler(PHASES, [], parametres, DeclarationDesEntrees((), ()))


def test_valeurs_indicatives_egales_a_celles_du_script(stationnaire):
    """P63 (#112, point 7) : valeurs en un seul jeu ; chaque paramètre des tables vaut, au bit,
    la valeur par défaut du même nom dans `Parametres` de `outils/etat_stationnaire.py`, g_N = 0
    compris ; l'unité des taux annuels est la même nature."""
    defaut = stationnaire.Parametres()
    for p in DECLARATIONS:
        assert hasattr(defaut, p.nom), p.nom
        valeur = getattr(defaut, p.nom)
        assert type(valeur) is float and valeur.hex() == p.valeur.hex(), p.nom
    assert travail.G_N.valeur == defaut.g_N == 0.0
    for p in DECLARATIONS:
        unite_script = stationnaire.DECLARATIONS[p.nom][0]
        if p.unite == "par an, taux de croissance":
            assert unite_script == p.unite, p.nom


def test_domaines_des_tables_et_du_script_refusent_le_meme_ensemble(stationnaire):
    """P71 : U^eq ≤ 0 et μ̄ ≤ 0 sont refusés par le script dès le chargement de ses paramètres,
    comme par les tables ; la calibration passe les deux."""
    base = dataclasses.replace(stationnaire.Parametres(), nu_G=1.15)
    stationnaire.controler_domaine(base)
    for table, nom in ((travail.TRAVAIL, "U_eq"), (prix.PRIX, "mu_bar")):
        for valeur in (0.0, -1e-9, -0.5):
            with pytest.raises(DefautDeDeclaration):
                varier(table, **{nom: valeur})
            with pytest.raises(stationnaire.HorsDomaine):
                stationnaire.controler_domaine(dataclasses.replace(base, **{nom: valeur}))
