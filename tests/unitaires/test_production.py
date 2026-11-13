"""Bloc 2, production et stocks : lignes « J3 » de la fiche 2 (§ 9.6) en appel direct (#113).

Classe (a) du classement du rang 1a de J3-b (synthèse en commentaire de la PR
#117, § 1) : boucle propre (linéarisation de N1 à N7, demande en volume
exogène, N = N* ; 0,75 et 0,87356), plancher N3, technique N5, empreinte. S'y
ajoutent, par appel direct de N8, les propriétés de la forme B de la ligne 4
(P72 : IN_{t+1} ≥ 0 exactement, zéro exact à l'épuisement ; équivalence
algébrique avec UC·y − cm·v, rapportée au stock disponible, P73). Seuils écrits
avant l'essai (fiche 2, § 9.6 ; `sec:production-conditions`), non déplacés.
Chaque test appelle les fonctions pures de `nations.blocs.production`, sans
le moteur.
"""

import ast
import inspect
import math

import numpy as np
import pytest

from nations.blocs import production as bloc
from nations.etat import schema
from nations.moteur.conversions import facteur_par_pas, par_pas
from nations.moteur.parametres import TauxDeCroissance, varier
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE

TABLE = PARAMETRES_DE_REFERENCE.production
N_A = PARAMETRES_DE_REFERENCE.cadre.pas_par_an
G = ((1.0 + TABLE.g_pr.valeur) * (1.0 + PARAMETRES_DE_REFERENCE.travail.g_N.valeur) - 1.0)
FACTEUR_G = facteur_par_pas(TauxDeCroissance(G))
GAMMA = FACTEUR_G - 1.0


# --------------------------------------------------------------------------
# Boucle propre (classe (a)) : N1 à N7, demande exogène, N = N*
# --------------------------------------------------------------------------


def carte_n1_n7(table, d_barre=1.0, pr=1.0):
    """Carte d'un pas (v^e, IN^vol) ↦ (v^e, IN^vol)_{t+1}, ramenée au sentier (÷ (1 + g)^{1/n_a}),
    composée des fonctions pures N1 à N7 : demande en volume d = d̄ exogène sur sa tendance,
    emploi égal à la demande de travail (N = N*), demande servie."""
    lam_v, lam_in = par_pas(table.lambda_v), par_pas(table.lambda_IN)

    def carte(x):
        v_e, IN_vol = x
        cible = bloc.stock_cible(v_e, table.sigma, N_A)
        y_etoile = bloc.production_visee(v_e, cible, IN_vol, FACTEUR_G, lam_in)
        y = bloc.production_du_pas(y_etoile, pr, bloc.demande_de_travail(y_etoile, pr))
        disponible = bloc.disponible(IN_vol, y)
        v, _, _, _ = bloc.ventes(d_barre, d_barre, 0.0, 0.0, disponible)
        suivant = (bloc.ventes_anticipees(v_e, d_barre, FACTEUR_G, lam_v),
                   bloc.stock_en_volume(disponible, v))
        return np.array(suivant) / FACTEUR_G

    return carte, np.array([d_barre, N_A * table.sigma * d_barre])


def valeurs_propres_n1_n7(table):
    """Valeurs propres de la carte au point fixe : différences centrées, pas relatif 1e−6."""
    carte, x0 = carte_n1_n7(table)
    assert np.max(np.abs(carte(x0) - x0) / x0) <= 1e-14  # point fixe ramené au sentier
    jac = np.empty((2, 2))
    for j in range(2):
        h = np.zeros(2)
        h[j] = 1e-6 * x0[j]
        jac[:, j] = (carte(x0 + h) - carte(x0 - h)) / (2.0 * h[j])
    return np.linalg.eigvals(jac)


# Variations des vitesses par le constructeur validé : calibration, × 0,5, × 2 ; valeurs
# publiées (`sec:production-conditions`), à leurs décimales.
VARIANTES = [
    (1.0, (0.75, 4), (0.87356, 5)),
    (0.5, (0.875, 3), (0.9360, 4)),
    (2.0, (0.5, 1), (0.7488, 4)),
]


@pytest.mark.parametrize("facteur, publiee_v, publiee_in", VARIANTES)
def test_boucle_propre_valeurs_propres_reelles_dans_l_intervalle(facteur, publiee_v, publiee_in):
    """Fiche 2, § 9.6, « Boucle propre » : valeurs propres réelles dans ]0 ; 1[, égales aux
    formes fermées 1 − λ_v/n_a et (1 − λ_IN/n_a)/(1 + g)^{1/n_a} à 1e−8, et aux valeurs
    publiées à leurs décimales (0,75 et 0,87356 à la calibration), pour la calibration et les
    vitesses × 0,5 et × 2."""
    table = varier(TABLE, lambda_v=facteur * TABLE.lambda_v.valeur,
                   lambda_IN=facteur * TABLE.lambda_IN.valeur)
    valeurs = valeurs_propres_n1_n7(table)
    assert np.all(np.imag(valeurs) == 0.0)
    reelles = sorted(np.real(valeurs))
    assert all(0.0 < x < 1.0 for x in reelles)
    formes = sorted([1.0 - table.lambda_v.valeur / N_A,
                     (1.0 - table.lambda_IN.valeur / N_A) / FACTEUR_G])
    assert max(abs(a - b) for a, b in zip(reelles, formes, strict=True)) <= 1e-8
    publiees = sorted([publiee_v, publiee_in])
    for x, (valeur, decimales) in zip(reelles, publiees, strict=True):
        assert round(x, decimales) == valeur, (x, valeur)


# --------------------------------------------------------------------------
# Plancher N3 (borne y* ≥ 0) et technique N5 (borne y ≤ pr·N)
# --------------------------------------------------------------------------


def _plancher(f, v_e=1.0, pr=1.0):
    """N3 avec IN^vol = IN^vol* + f·E, E = (n_a/λ_IN)(v^e + γ IN^vol*) ; rend (y*, N*, y, IN^vol)."""
    lam_in = par_pas(TABLE.lambda_IN)
    cible = bloc.stock_cible(v_e, TABLE.sigma, N_A)
    excedent = (v_e + GAMMA * cible) / lam_in
    IN_vol = cible + f * excedent
    y_etoile = bloc.production_visee(v_e, cible, IN_vol, FACTEUR_G, lam_in)
    N_etoile = bloc.demande_de_travail(y_etoile, pr)
    return y_etoile, N_etoile, bloc.production_du_pas(y_etoile, pr, N_etoile), IN_vol


def test_plancher_inactif_sous_le_seuil_et_a_l_etat_resolu():
    """Fiche 2, § 9.6, « Plancher » : f = 0,99, y* > 0 ; à l'état résolu (IN^vol = IN^vol*),
    y* > 0."""
    y_etoile, N_etoile, y, _ = _plancher(0.99)
    assert y_etoile > 0.0 and N_etoile > 0.0 and y > 0.0
    y_etoile, _, _, _ = _plancher(0.0)
    assert y_etoile > 0.0


def test_plancher_actif_au_dela_du_seuil():
    """f = 1,01 : y* = 0, N* = 0 et y = 0 exactement, jamais négatifs ; au pas suivant, IN^vol
    baisse des ventes (N7)."""
    y_etoile, N_etoile, y, IN_vol = _plancher(1.01)
    assert y_etoile == 0.0 and N_etoile == 0.0 and y == 0.0
    assert math.copysign(1.0, y_etoile) == 1.0
    disponible = bloc.disponible(IN_vol, y)
    v, _, _, _ = bloc.ventes(1.0, 1.0, 0.0, 0.0, disponible)
    assert v == 1.0
    assert bloc.stock_en_volume(disponible, v) == IN_vol - v < IN_vol


def test_technique_trois_cas():
    """Fiche 2, § 9.6, « Technique » : (a) N = N* : y = y* = pr·N à 1e−12 ; (b) N = 0,9 N* :
    y = pr·N < y* ; (c) N = 1,1 N* : y = y* < pr·N ; toujours y ≤ pr·N."""
    pr, y_etoile = 1.0016515813, 1.0023122
    N_etoile = bloc.demande_de_travail(y_etoile, pr)
    y = bloc.production_du_pas(y_etoile, pr, N_etoile)
    assert abs(y / y_etoile - 1.0) <= 1e-12 and abs(y / (pr * N_etoile) - 1.0) <= 1e-12
    y = bloc.production_du_pas(y_etoile, pr, 0.9 * N_etoile)
    assert y == pr * (0.9 * N_etoile) < y_etoile
    y = bloc.production_du_pas(y_etoile, pr, 1.1 * N_etoile)
    assert y == y_etoile < pr * (1.1 * N_etoile)
    for facteur in (0.0, 0.5, 0.9, 1.0, 1.1, 2.0):
        N = facteur * N_etoile
        assert bloc.production_du_pas(y_etoile, pr, N) <= pr * N


# --------------------------------------------------------------------------
# Ventes et rationnement (N6), forme B de la ligne 4 (N8, P72, P73)
# --------------------------------------------------------------------------


def test_rationnement_proportionnel_et_demande_nulle():
    """N6 : demande supérieure de 10 % au disponible, chaque acheteur servi au même taux v/d
    (à 2 ulp près), v égal au disponible exactement ; demande nulle, ventes et volumes servis
    nuls."""
    d_H, d_F, d_G = 0.62, 0.17, 0.21
    d = bloc.demande_adressee(d_H, d_F, d_G)
    disponible = d / 1.1
    v, v_H, v_F, v_G = bloc.ventes(d, d_H, d_F, d_G, disponible)
    assert v == disponible and bloc.stock_en_volume(disponible, v) == 0.0
    for servi, demande in ((v_H, d_H), (v_F, d_F), (v_G, d_G)):
        assert abs(servi / demande - v / d) <= 2 * math.ulp(v / d)
    assert bloc.ventes(0.0, 0.0, 0.0, 0.0, 1.0) == (0.0, 0.0, 0.0, 0.0)


def _tirages(rng, n):
    """Pas d'épuisement tirés à graine explicite : IN^vol, y, UC et le rapport ρ = IN/(UC IN^vol)
    sur plusieurs ordres de grandeur ; v = disponible."""
    IN_vol = 10.0 ** rng.uniform(-6, 3, n)
    y = 10.0 ** rng.uniform(-6, 3, n)
    UC = 10.0 ** rng.uniform(-3, 3, n)
    rho = rng.uniform(0.5, 1.0, n)
    return IN_vol, y, UC, rho * UC * IN_vol


def test_forme_b_epuisement_zero_exact_et_jamais_negatif():
    """P72 : à l'épuisement (v = IN^vol + y), IN^vol_{t+1} = 0 et IN_{t+1} = IN_t + ΔIN = 0
    exactement ; sur des pas tirés au hasard (graine 20261113), IN_{t+1} ≥ 0 exactement, qu'il
    y ait épuisement ou non."""
    rng = np.random.default_rng(20261113)
    for IN_vol, y, UC, IN in zip(*_tirages(rng, 20_000), strict=True):
        IN_vol, y, UC, IN = float(IN_vol), float(y), float(UC), float(IN)
        disponible = bloc.disponible(IN_vol, y)
        v, _, _, _ = bloc.ventes(2.0 * disponible, disponible, disponible, 0.0, disponible)
        IN_vol_suivant = bloc.stock_en_volume(disponible, v)
        assert IN_vol_suivant == 0.0
        delta = bloc.variation_des_stocks(IN, UC, y, disponible, IN_vol_suivant)
        assert IN + delta == 0.0
        # Hors épuisement : une fraction quelconque vendue.
        v = disponible * float(rng.uniform(0.0, 1.0))
        IN_vol_suivant = bloc.stock_en_volume(disponible, v)
        assert IN_vol_suivant >= 0.0
        assert IN + bloc.variation_des_stocks(IN, UC, y, disponible, IN_vol_suivant) >= 0.0


def test_forme_b_egale_la_forme_d_origine_rapportee_au_stock_disponible():
    """P72, P73 : ΔIN = cm IN^vol_{t+1} − IN (forme B) et UC y − cm v (forme d'origine) sont
    égales à 1e−12 près rapportées à IN_t + UC_t y_t ; IN_{t+1} = cm IN^vol_{t+1} au même
    seuil ; ΔIN = 0 si le disponible est nul."""
    rng = np.random.default_rng(20261114)
    pire_equivalence = pire_valorisation = 0.0
    for IN_vol, y, UC, IN in zip(*_tirages(rng, 20_000), strict=True):
        IN_vol, y, UC, IN = float(IN_vol), float(y), float(UC), float(IN)
        disponible = bloc.disponible(IN_vol, y)
        v = disponible * float(rng.uniform(0.0, 1.0))
        IN_vol_suivant = bloc.stock_en_volume(disponible, v)
        delta = bloc.variation_des_stocks(IN, UC, y, disponible, IN_vol_suivant)
        cm = (IN + UC * y) / disponible
        echelle = IN + UC * y
        pire_equivalence = max(pire_equivalence, abs(delta - (UC * y - cm * v)) / echelle)
        pire_valorisation = max(pire_valorisation, abs(IN + delta - cm * IN_vol_suivant) / echelle)
    assert pire_equivalence <= 1e-12 and pire_valorisation <= 1e-12
    assert bloc.variation_des_stocks(0.0, 2.0, 0.0, 0.0, 0.0) == 0.0


# --------------------------------------------------------------------------
# Empreinte : quatre variables d'état, aucun historique, aucun tirage
# --------------------------------------------------------------------------


def test_empreinte_quatre_variables_sans_historique_ni_tirage():
    """Fiche 2, § 9.6, « Empreinte » : quatre variables d'état au radical `production` (J = 1),
    scalaires (aucun historique), écrites en phase 5 par le bloc ; le module n'importe que
    `contrat_bloc` et `conversions` (aucun générateur aléatoire) ; le bloc n'a pas d'attribut
    d'instance."""
    variables = [v for v in schema.VARIABLES_DES_BLOCS if v.proprietaire == "production"]
    assert [v.nom for v in variables] == ["v_e", "IN_vol", "pr", "K_vol"]
    assert all(v.type is float and v.longueur == 1 and v.phase_ecriture == "5"
               for v in variables)
    siege_5 = next(s for s in bloc.Production.declaration.sieges if s.etape == "5")
    assert siege_5.etat == ("v_e", "IN_vol", "pr", "K_vol")
    arbre = ast.parse(inspect.getsource(bloc))
    importes = {n.module for n in ast.walk(arbre) if isinstance(n, ast.ImportFrom)}
    importes |= {a.name for n in ast.walk(arbre) if isinstance(n, ast.Import) for a in n.names}
    assert importes == {"__future__", "nations.moteur.contrat_bloc",
                        "nations.moteur.conversions"}
    instance = bloc.Production()
    assert not hasattr(instance, "__dict__") and bloc.Production.__slots__ == ()


def test_declaration_conforme_a_tab_production_phases():
    """`tab:production-phases` et ADR 0012, annotation du 13/11/2026, points 2.2 et 2.5 :
    phases 2, 4 et 5 ; N_t lu en phase 4 (écrit avant par le bloc travail), p_t en phase 5
    (écrit avant par le bloc prix) ; aucune lecture d'un plan de la phase 2 en phase 2 ; ligne
    4 seule proposée ; aucune lecture de W en phase 5."""
    sieges = {s.etape: s for s in bloc.Production.declaration.sieges}
    assert tuple(sieges) == ("2", "4", "5")
    lus = {e: {(lu.source, lu.nom) for lu in s.lit} for e, s in sieges.items()}
    assert not any(source == "2" for source, _ in lus["2"])
    assert ("4", "N_suivant") in lus["4"] and ("5", "p") in lus["5"]
    assert not any(nom == "W_suivant" for _, nom in lus["5"])
    assert ("ouverture", "IN") in lus["5"]
    assert [s.propose for s in sieges.values()] == [(), (), ("4",)]
