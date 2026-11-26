"""Tables de paramètres des blocs 2 à 4 et 6, ensemble des tables (issues #112, #67).

Contrat : ADR 0012, F1 et F2, et annotation du 13/11/2026, point 3 (P63, P65,
P68 à P71) ; synthèse du rang 1a de J3-b, § 3 (unités) ; table du bloc 6 complétée (ADR 0013,
annotation du 14/11/2026 (rang 1b de J3-d1), point 2 ; P80 ; #67). Chaque test énonce une
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
from nations.moteur.parametres import (
    banque,
    banque_centrale,
    investissement,
    prix,
    production,
    travail,
)
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
    # Bloc 6 (rang 4 de J3-d1, #67) : η_r et ζ sans dimension, sur le précédent de β (point 2).
    "tu_bar": "fraction", "lambda_ti": "par an, taux de flux", "eta_r": "sans dimension",
    "zeta": "sans dimension", "lv_etoile": "fraction", "nu_F": "années",
}

# Noms du script d'état stationnaire qui diffèrent de ceux des tables (point 2 : le script nomme
# `lv` ce que la table nomme `lv_etoile`).
NOMS_DU_SCRIPT = {"lv_etoile": "lv"}


def test_vingt_parametres_un_seul_par_maison():
    """Point 3 : λ_v, λ_IN, σ, g_pr, κ ; λ_w, β, U^eq, λ_N, g_N ; μ̄, λ_μ, ψ_ξ ; δ, puis (ADR 0013,
    annotation du 14/11/2026 (rang 1b de J3-d1), point 2 ; #67) t̄u, λ_ti, η_r, ζ, lv*, ν_F. Un
    nom n'apparaît que dans une table (g_pr dans la production, μ̄ dans les prix, δ dans
    l'investissement, P68)."""
    assert [[p.nom for p in d] for _, _, d in TABLES] == [
        ["lambda_v", "lambda_IN", "sigma", "g_pr", "kappa"],
        ["lambda_w", "beta", "U_eq", "lambda_N", "g_N"],
        ["mu_bar", "lambda_mu", "psi_xi"],
        ["delta", "tu_bar", "lambda_ti", "eta_r", "zeta", "lv_etoile", "nu_F"],
    ]
    noms = [p.nom for p in DECLARATIONS]
    assert len(noms) == len(set(noms)) == 20
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
    (production.PRODUCTION, "kappa", 1e-320),
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
    # Bloc 6 (sec:investissement-conditions ; rang 4 de J3-d1, #67).
    (investissement.INVESTISSEMENT, "tu_bar", 0.0), (investissement.INVESTISSEMENT, "tu_bar", -0.8),
    (investissement.INVESTISSEMENT, "tu_bar", math.inf),
    (investissement.INVESTISSEMENT, "lambda_ti", 0.0),
    (investissement.INVESTISSEMENT, "lambda_ti", N_A + 1e-9),
    (investissement.INVESTISSEMENT, "lambda_ti", -0.02),
    (investissement.INVESTISSEMENT, "eta_r", -1e-12), (investissement.INVESTISSEMENT, "eta_r", math.nan),
    (investissement.INVESTISSEMENT, "zeta", -5e-324), (investissement.INVESTISSEMENT, "zeta", -4.0),
    # Bornes hautes η_r, ζ ≤ 20 (P139).
    (investissement.INVESTISSEMENT, "eta_r", math.nextafter(20.0, 21.0)),
    (investissement.INVESTISSEMENT, "zeta", math.nextafter(20.0, 21.0)),
    (investissement.INVESTISSEMENT, "zeta", math.inf),
    (investissement.INVESTISSEMENT, "lv_etoile", -5e-324),
    (investissement.INVESTISSEMENT, "lv_etoile", 1.0), (investissement.INVESTISSEMENT, "lv_etoile", 1.5),
    (investissement.INVESTISSEMENT, "nu_F", 0.0), (investissement.INVESTISSEMENT, "nu_F", -1.0 / 6.0),
    (investissement.INVESTISSEMENT, "nu_F", math.inf),
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
    # Bloc 6 : λ_ti = n_a, η_r = 0 et 20, ζ = 0 et 20, lv* = 0 inclus ; lv* juste sous 1, t̄u et ν_F juste
    # au-dessus de 0 admis.
    varier(investissement.INVESTISSEMENT, lambda_ti=float(N_A), eta_r=0.0, zeta=0.0, lv_etoile=0.0)
    varier(investissement.INVESTISSEMENT, eta_r=20.0, zeta=20.0)  # bornes hautes incluses (P139)
    varier(investissement.INVESTISSEMENT, lv_etoile=math.nextafter(1.0, 0.0), tu_bar=5e-324,
           nu_F=5e-324)


def test_ensemble_des_tables():
    """Point 3.5 (P69) : un champ par table, chacune de son type exact ; ni champ de mode ni
    de doublure (annotation du 13/11/2026, point 6 (b)) ; variation contrôlée. J3-c (ADR 0013,
    annotation du 14/11/2026, point 6 ; H3.5) : `banque` et `banque_centrale` à la suite. J3-d1
    (annotation du 14/11/2026 (rang 1b de J3-d1), point 2) : `menages` entre `prix` et
    `investissement`. J3-d2 (annotation du 15/11/2026 (rang 1b de J3-d2), point 8 ; P165) :
    `finances_publiques`, dernier."""
    from nations.moteur.parametres import finances_publiques, menages
    noms = ["cadre", "production", "travail", "prix", "menages", "investissement", "banque",
            "banque_centrale", "finances_publiques"]
    assert [f.name for f in dataclasses.fields(EnsembleDesParametres)] == noms
    p = PARAMETRES_DE_REFERENCE
    assert (p.cadre, p.production, p.travail, p.prix, p.menages, p.investissement, p.banque,
            p.banque_centrale, p.finances_publiques) == (
        CADRE, production.PRODUCTION, travail.TRAVAIL, prix.PRIX, menages.MENAGES,
        investissement.INVESTISSEMENT, banque.BANQUE, banque_centrale.BANQUE_CENTRALE,
        finances_publiques.FINANCES_PUBLIQUES)
    for nom in noms:
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
        nom = NOMS_DU_SCRIPT.get(p.nom, p.nom)
        assert hasattr(defaut, nom), p.nom
        valeur = getattr(defaut, nom)
        assert type(valeur) is float and valeur.hex() == p.valeur.hex(), p.nom
    assert travail.G_N.valeur == defaut.g_N == 0.0
    for p in DECLARATIONS:
        unite_script = stationnaire.DECLARATIONS[NOMS_DU_SCRIPT.get(p.nom, p.nom)][0]
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


def test_kappa_sous_normal_refuse_par_le_script_comme_par_la_table(stationnaire):
    """#125, point 5 : κ > 0 et 1/κ fini, refusé par le script comme par la table du bloc 2 ;
    κ = 1e−320 (1/κ infini) refusé par les deux ; κ = 5,6e−309 (1/κ fini) et la calibration
    admis par les deux (la borne inférieure de κ relève du point 6, J3-e2)."""
    base = dataclasses.replace(stationnaire.Parametres(), nu_G=1.15)
    for valeur in (1e-320, 0.0, -1.6):
        with pytest.raises(DefautDeDeclaration, match="« kappa »"):
            varier(production.PRODUCTION, kappa=valeur)
        with pytest.raises(stationnaire.HorsDomaine, match="kappa"):
            stationnaire.controler_domaine(dataclasses.replace(base, kappa=valeur))
    for valeur in (5.6e-309, 1.6):
        varier(production.PRODUCTION, kappa=valeur)
        stationnaire.controler_domaine(dataclasses.replace(base, kappa=valeur))


def test_taux_de_croissance_refuses_un_a_un_par_le_script_comme_par_les_tables(stationnaire):
    """1 + g_pr > 0 et 1 + g_N > 0, chacun (`TAUX_DE_CROISSANCE_ANNUEL`) : g_pr = g_N = −1,5,
    de produit (1 + g_pr)(1 + g_N) > 0, est refusé par le script comme par les tables ; un
    taux à −1 ou en deçà aussi."""
    base = dataclasses.replace(stationnaire.Parametres(), nu_G=1.15)
    for champs in ({"g_pr": -1.5, "g_N": -1.5}, {"g_pr": -1.0}, {"g_N": -1.0}, {"g_N": -2.0}):
        with pytest.raises(stationnaire.HorsDomaine, match=r"1 \+ g_(pr|N) > 0"):
            stationnaire.controler_domaine(dataclasses.replace(base, **champs))
        for nom, valeur in champs.items():
            table = production.PRODUCTION if nom == "g_pr" else travail.TRAVAIL
            with pytest.raises(DefautDeDeclaration, match=f"« {nom} »"):
                varier(table, **{nom: valeur})
    stationnaire.controler_domaine(dataclasses.replace(base, g_pr=-0.5, g_N=-0.5))
    varier(production.PRODUCTION, g_pr=-0.5)
    varier(travail.TRAVAIL, g_N=-0.5)


@pytest.mark.parametrize("nom", ["eta_r", "zeta"])
def test_borne_haute_de_eta_r_et_zeta_dans_le_script_comme_dans_la_table(stationnaire, nom):
    """P139 : 0 ≤ η_r, ζ ≤ 20, refusés par le script comme par la table du bloc 6, aux
    frontières : 20 + 1 ulp et −1 ulp refusés par les deux ; 20 et 0 admis par les deux."""
    base = dataclasses.replace(stationnaire.Parametres(), nu_G=1.15)
    for valeur in (math.nextafter(20.0, math.inf), math.nextafter(0.0, -math.inf)):
        with pytest.raises(DefautDeDeclaration, match=f"« {nom} »"):
            varier(investissement.INVESTISSEMENT, **{nom: valeur})
        with pytest.raises(stationnaire.HorsDomaine, match=f"0 ≤ {nom} ≤ 20"):
            stationnaire.controler_domaine(dataclasses.replace(base, **{nom: valeur}))
    for valeur in (20.0, 0.0):
        varier(investissement.INVESTISSEMENT, **{nom: valeur})
        stationnaire.controler_domaine(dataclasses.replace(base, **{nom: valeur}))


def test_lambda_v_strict_dans_le_script_comme_dans_la_table(stationnaire):
    """P70 : λ_v = n_a est refusée par le script comme par la table (domaine strict) ; λ_v =
    11,999 est admise par les deux."""
    base = dataclasses.replace(stationnaire.Parametres(), nu_G=1.15)
    assert base.n_a == N_A
    with pytest.raises(DefautDeDeclaration, match="strict"):
        varier(production.PRODUCTION, lambda_v=float(N_A))
    with pytest.raises(stationnaire.HorsDomaine, match="domaine strict, P70"):
        stationnaire.controler_domaine(dataclasses.replace(base, lambda_v=float(N_A)))
    varier(production.PRODUCTION, lambda_v=11.999)
    stationnaire.controler_domaine(dataclasses.replace(base, lambda_v=11.999))
