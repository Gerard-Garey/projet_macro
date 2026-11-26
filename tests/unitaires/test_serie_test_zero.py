"""Série du test zéro hors stationnarité (#176, réserve majeure de l'audit léger du rang 6).

Événements synthétiques, **non stationnaires**, sur 14 pas : chaque montant, chaque variable du
pas et chaque position change d'un pas à l'autre, fonds propres de la banque centrale non nuls
(E^CB = B_CB + L^CB − Res − M^G ≠ 0 à l'ouverture, V^flux ≠ 0). Chaque grandeur de la série est
comparée à une valeur calculée à la main, par sa formule développée (`tab:criteres-j3`) sur les
mêmes entrées. Mutants visés (tués) : B4 et B6 réduits au pas courant, B21 sans E^CB.
"""

import dataclasses
import math

import pytest

from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.noyau import identites as idt
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas
from nations.observation.serie_test_zero import GRANDEURS, SUR_12_TOURS, SerieDuTestZero
from nations.scenarios import initial

N_A = 12
NB_PAS = 14
R_BAR = 0.01
TOLERANCE = 1e-13  # relative : écarts d'arrondi seuls (ordre des sommes)


def montants(k):
    """Lignes lues par la série au pas k (u.m. par pas), non stationnaires."""
    return {"1": 10.0 + k, "2": 3.0 + 0.5 * k, "3": 2.0 + 0.1 * k * k, "4": 0.2 * (-1) ** k,
            "5": 6.0 + 0.3 * k + 0.05 * k * k, "6": 0.1 * k, "7": 4.0 + 0.2 * k,
            "11a": 0.01 * k, "11b": 0.3, "11c": 0.02, "16": 0.05 + 0.01 * k}


def variables(k):
    """Variables du pas k, non stationnaires (p/UC varie : la marge de B6 change à chaque pas)."""
    p = 1.0 + 0.01 * k + 0.002 * k * k
    return {"v": 5.0 + k, "y": 5.5 + 0.2 * k + 0.01 * k * k, "y_cap": 7.0 + 0.1 * k,
            "U_suivant": 0.05 + 0.001 * k, "YD_m1_suivant": 9.0 + 0.4 * k, "p": p, "P": p,
            "UC": 0.6 + 0.005 * k, "W_suivant": 0.62 + 0.01 * k + 0.001 * k * k,
            "i_CB": 0.03 + 0.001 * k, "i_regle": 0.03 + 0.0012 * k}


def ouverture(base, k):
    """État d'ouverture du pas k (état de fin du pas k − 1), non stationnaire, E^CB ≠ 0."""
    return dataclasses.replace(
        base, t=k, IN_vol=1.3 + 0.01 * k, K_vol=22.0 + 0.5 * k, L=7.0 + 0.1 * k,
        K=17.0 + 0.3 * k, D_F=1.9 + 0.02 * k, D_H=8.0 + 0.1 * k, M_G=0.25 + 0.01 * k,
        B_Bk=4.3 + 0.05 * k, B_CB=0.5 + 0.02 * k, L_CB=0.3 + 0.01 * k, Res=0.1 + 0.005 * k,
        B_H=0.1 + 0.001 * k, i_L=0.05 + 0.001 * k, i_D=0.02 + 0.0005 * k,
        pi_e=0.02 + 0.0001 * k, r_hat_etoile=0.01 + 0.0001 * k,
        V_flux_banque_centrale=0.07 + 0.001 * k, W=0.6 + 0.01 * k, y_m1=5.4 + 0.2 * k,
        registre_prix=tuple((1.0 + 0.003 * k) / (1.0 + 0.004 * j) ** (1 + 0.1 * k)
                            for j in range(1, N_A + 2)))


@pytest.fixture(scope="module")
def releve():
    """(ouvertures o_0 à o_14, série relevée sur 14 pas synthétiques)."""
    base = initial.etat_initial(PARAMETRES_DE_REFERENCE, initial.NORMALISATION_DE_REFERENCE,
                                identifiant="A", graine=0).etat
    o = [ouverture(base, k) for k in range(NB_PAS + 1)]
    serie = SerieDuTestZero(o[0], pas_par_an=N_A, r_bar=R_BAR)
    for k in range(NB_PAS):
        serie.relever(ClotureDePhase(k, "6", (), tuple(
            (ligne, ((ligne, x),)) for ligne, x in montants(k).items())))
        serie.relever(FinDePas(k, o[k + 1], tuple(variables(k).items()), ()))
    return o, serie


def a_la_main(o, k):
    """Valeurs de chaque grandeur au pas k, formules développées de `tab:criteres-j3`."""
    m, v, a, e = montants(k), variables(k), o[k], o[k + 1]
    pib = m["1"] + m["2"] + m["3"] + m["4"]
    s_cb = idt.echelle_bilan({q: getattr(e, q) for q in (
        "D_H", "D_F", "L", "B_H", "B_Bk", "B_CB", "Res", "L_CB", "M_G", "K", "IN")},
        "banque_centrale")
    x = {
        "B1": a.IN_vol / v["v"], "B2": v["y"] / v["y_cap"], "B3": v["U_suivant"],
        "B8": e.pi_e - e.pi_etoile,
        "B10": (a.D_H + a.B_H) / (12 * v["YD_m1_suivant"]),
        "B12": v["p"] * a.K_vol / (12 * pib), "B14": a.L / a.K, "B15": a.D_F / (12 * pib),
        "B16": (a.D_H + a.D_F) / (12 * pib),
        "B17": (a.L + a.B_Bk + a.Res - a.D_H - a.D_F - a.L_CB) / a.L,
        "B18 (i) ϖ_L": e.i_L - v["i_CB"], "B18 (i) ϖ_D": v["i_CB"] - e.i_D,
        "B18 (ii) ϖ_L": a.i_L - v["i_CB"], "B18 (ii) ϖ_D": v["i_CB"] - a.i_D,
        "B19 M^G": a.M_G / (12 * pib),
        "B19 Res (H)": e.Res / s_cb, "B19 E^CB": e.V_flux_banque_centrale / s_cb,
        "B19 B_CB": e.B_CB / s_cb,
        "B19 identité": (e.L_CB + e.B_CB - e.Res - e.M_G - e.V_flux_banque_centrale) / s_cb,
        "B20": a.B_Bk / (12 * pib),
        # B − M^G − E^CB, E^CB = B_CB + L^CB − Res − M^G : B_H + B_Bk + Res − L^CB.
        "B21": (a.B_H + a.B_Bk + a.Res - a.L_CB) / (12 * pib),
        "B25": e.r_hat_etoile - R_BAR, "B26": v["i_CB"] - v["i_regle"], "r̂*": e.r_hat_etoile,
    }
    if k >= N_A - 1:
        f = range(k - N_A + 1, k + 1)
        pibs = [sum(montants(j)[ligne] for ligne in ("1", "2", "3", "4")) for j in f]
        x["B4"] = sum(montants(j)["5"] for j in f) / sum(pibs)
        x["B13"] = sum(montants(j)["3"] for j in f) / sum(pibs)
        x["B11"] = 1 - sum(montants(j)["1"] for j in f) / sum(variables(j)["YD_m1_suivant"]
                                                             for j in f)
        x["B22"] = sum(montants(j)["2"] + montants(j)["6"] + montants(j)["11a"]
                       + montants(j)["11b"] + montants(j)["11c"] - montants(j)["7"]
                       - montants(j)["16"] for j in f) / sum(pibs)
        x["B6"] = sum(variables(j)["p"] / variables(j)["UC"] - 1 for j in f) / 12
        if k - N_A >= 0:
            w0, p0, y0 = (variables(k - N_A)[n] for n in ("W_suivant", "p", "y"))
        else:  # pas −1 : ouverture du premier pas
            w0, p0, y0 = o[0].W, o[0].registre_prix[0], o[0].y_m1
        x["B5"] = (v["W_suivant"] / v["p"]) / (w0 / p0) - 1
        x["B24"] = v["y"] / y0 - 1
        x["B7"] = v["P"] / a.registre_prix[11] - 1
        x["B9"] = v["i_CB"] - x["B7"]
    return x


def test_chaque_grandeur_egale_au_calcul_a_la_main(releve):
    """Toutes les grandeurs, à chaque pas évalué (dès le pas 11 sur 12 tours), égales au calcul
    à la main à 1e−13 près en relatif (absolu pour une valeur nulle)."""
    o, serie = releve
    for cle in GRANDEURS:
        valeurs = dict(serie.serie(cle))
        premier = N_A - 1 if cle in SUR_12_TOURS else 0
        assert sorted(valeurs) == list(range(premier, NB_PAS)), cle
        for k, x in valeurs.items():
            attendu = a_la_main(o, k)[cle]
            assert math.isclose(x, attendu, rel_tol=TOLERANCE, abs_tol=1e-15), (cle, k, x, attendu)


def test_entrees_non_stationnaires_discriminantes(releve):
    """Les entrées discriminent les mutants : WB/PIB et p/UC du pas courant diffèrent de leur
    valeur sur 12 tours, et E^CB d'ouverture n'est pas nul."""
    o, _ = releve
    for k in range(N_A - 1, NB_PAS):
        m, v, x = montants(k), variables(k), a_la_main(o, k)
        assert abs(m["5"] / (m["1"] + m["2"] + m["3"] + m["4"]) / x["B4"] - 1) > 1e-3
        assert abs((v["p"] / v["UC"] - 1) / x["B6"] - 1) > 1e-3
        e_cb = o[k].B_CB + o[k].L_CB - o[k].Res - o[k].M_G
        assert abs(e_cb) > 0.1


def test_ligne_relevee_deux_fois_dans_le_pas_refusee(releve):
    """Une ligne lue déjà relevée dans le pas est refusée, jamais écrasée."""
    o, _ = releve
    serie = SerieDuTestZero(o[0], pas_par_an=N_A, r_bar=R_BAR)
    cloture = ClotureDePhase(0, "6", (), (("7", (("T_H", 1.0),)),))
    serie.relever(cloture)
    with pytest.raises(ValueError, match="relevée deux fois"):
        serie.relever(cloture)


def test_ecarts_maximaux_sur_les_pas_anterieurs(releve):
    """`ecart_relatif_maximal` et `ecart_absolu_maximal` ne lisent que les pas t < `avant`."""
    _, serie = releve
    xs = dict(serie.serie("B1"))
    ref = xs[0]
    pire, t = serie.ecart_relatif_maximal("B1", ref, avant=5)
    assert (pire, t) == max(((abs(xs[k] / ref - 1), k) for k in range(5)), key=lambda p: p[0])
    pire, t = serie.ecart_absolu_maximal("B1", ref, avant=NB_PAS)
    assert (pire, t) == max(((abs(xs[k] - ref), k) for k in range(NB_PAS)), key=lambda p: p[0])
    assert serie.ecart_absolu_maximal("B4", 0.0, avant=N_A - 1) == (0.0, None)
