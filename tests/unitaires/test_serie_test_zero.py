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


def relever_un_pas(serie, k, o, **modifs):
    """Relève le pas synthétique k (clôture puis fin de pas), variables modifiées par `modifs`."""
    serie.relever(ClotureDePhase(k, "6", (), tuple(
        (ligne, ((ligne, x),)) for ligne, x in montants(k).items())))
    serie.relever(FinDePas(k, o[k + 1], tuple({**variables(k), **modifs}.items()), ()))


@pytest.mark.parametrize("valeur", [math.nan, math.inf, -math.inf])
def test_valeur_non_finie_refusee_a_l_enregistrement(releve, valeur):
    """Une valeur non finie est refusée à l'enregistrement (`ValueError` nommant la grandeur et le
    pas), jamais tenue dans la série ; le pas refusé n'enregistre aucune valeur et abandonne ses
    montants : il se rejoue depuis ses clôtures de phase, aux valeurs du calcul à la main."""
    o, _ = releve
    serie = SerieDuTestZero(o[0], pas_par_an=N_A, r_bar=R_BAR)
    with pytest.raises(ValueError, match=r"pas 0 : B3 = .*non finie"):
        relever_un_pas(serie, 0, o, U_suivant=valeur)
    assert serie.pas() == () and all(serie.serie(cle) == () for cle in GRANDEURS)
    with pytest.raises(ValueError, match="lignes non exécutées"):
        serie.relever(FinDePas(0, o[1], tuple(variables(0).items()), ()))
    relever_un_pas(serie, 0, o)
    assert serie.serie("B12") == ((0, a_la_main(o, 0)["B12"]),)


def test_valeur_non_finie_d_une_grandeur_sur_12_tours_refusee(releve):
    """P non fini n'entre que dans B7 (puis B9) : les pas 0 à 10 sont relevés, le pas 11, premier
    pas de B7, est refusé en nommant B7, et la série garde ses 11 pas."""
    o, _ = releve
    serie = SerieDuTestZero(o[0], pas_par_an=N_A, r_bar=R_BAR)
    for k in range(N_A - 1):
        relever_un_pas(serie, k, o, P=math.nan)
    with pytest.raises(ValueError, match=r"pas 11 : B7 = nan"):
        relever_un_pas(serie, N_A - 1, o, P=math.nan)
    assert serie.pas() == tuple(range(N_A - 1))
    assert serie.serie("B9") == () and len(serie.serie("B1")) == N_A - 1


def test_ecarts_maximaux_nan_au_pire(releve):
    """Un écart NaN est le pire, jamais ignoré par la comparaison (mesure de l'audit : série
    [(0, 1), (1, NaN), (2, 1 + 1e−15)] → (1,11e−15 ; 2) avant correction). La garde
    d'enregistrement est contournée à dessein (défense en profondeur des jugements)."""
    o, _ = releve
    serie = SerieDuTestZero(o[0], pas_par_an=N_A, r_bar=R_BAR)
    serie._series["B1"].extend([(0, 1.0), (1, math.nan), (2, 1.0 + 1e-15), (3, math.inf)])
    # NaN au-dessus de inf : un inf qui précède le NaN ne l'emporte pas.
    serie._series["B2"].extend([(0, math.inf), (1, math.nan)])
    for methode in (serie.ecart_relatif_maximal, serie.ecart_absolu_maximal):
        pire, t = methode("B1", 1.0, avant=3)
        assert math.isnan(pire) and t == 1, methode
        pire, t = methode("B1", 1.0, avant=4)
        assert math.isnan(pire) and t == 1, methode
        pire, t = methode("B2", 1.0, avant=2)
        assert math.isnan(pire) and t == 1, methode


def test_b17_sans_objet_a_credit_nul(releve):
    """L d'ouverture nul (lv* = 0, dans le domaine) : B17 n'est pas relevée (rapport sans objet,
    ni NaN ni `ZeroDivisionError`) ; les autres grandeurs le sont, B14 à 0."""
    o, _ = releve
    o_nul = [dataclasses.replace(x, L=0.0) for x in o]
    serie = SerieDuTestZero(o_nul[0], pas_par_an=N_A, r_bar=R_BAR)
    for k in range(2):
        relever_un_pas(serie, k, o_nul)
    assert serie.serie("B17") == ()
    assert serie.serie("B14") == ((0, 0.0), (1, 0.0))
    assert all(len(serie.serie(cle)) == 2 for cle in GRANDEURS
               if cle != "B17" and cle not in SUR_12_TOURS)


@pytest.mark.parametrize("pas_par_an, erreur", [
    (0, ValueError), (-1, ValueError), (4, ValueError), (13, ValueError),
    (12.0, TypeError), (True, TypeError)])
def test_pas_par_an_controle(releve, pas_par_an, erreur):
    """n_a : `int` égal à la longueur du registre de prix moins un (n_a + 1 prix)."""
    o, _ = releve
    assert len(o[0].registre_prix) == N_A + 1
    with pytest.raises(erreur):
        SerieDuTestZero(o[0], pas_par_an=pas_par_an, r_bar=R_BAR)


@pytest.mark.parametrize("r_bar, erreur", [
    (math.nan, ValueError), (math.inf, ValueError), (-math.inf, ValueError), (0, TypeError)])
def test_r_bar_controle(releve, r_bar, erreur):
    """r̄ : flottant fini."""
    o, _ = releve
    with pytest.raises(erreur):
        SerieDuTestZero(o[0], pas_par_an=N_A, r_bar=r_bar)


def cloture(k, t=None):
    """Clôture de phase portant les montants du pas k, datée du pas `t` (k par défaut)."""
    return ClotureDePhase(k if t is None else t, "6", (), tuple(
        (ligne, ((ligne, x),)) for ligne, x in montants(k).items()))


def test_fin_de_pas_hors_de_l_ouverture_stockee_refusee(releve):
    """La fin du pas t suit l'état d'ouverture du pas t stocké (fin.t = ouverture.t) : une fin de
    pas d'un autre pas est refusée, sans valeur enregistrée, et les montants du pas en cours sont
    abandonnés (une fin du pas 0 ne les lit pas ensuite)."""
    o, _ = releve
    serie = SerieDuTestZero(o[0], pas_par_an=N_A, r_bar=R_BAR)
    serie.relever(cloture(0))
    with pytest.raises(ValueError, match="fin du pas 1 reçue sur l'état d'ouverture du pas 0"):
        serie.relever(FinDePas(1, o[2], tuple(variables(1).items()), ()))
    assert serie.pas() == ()
    with pytest.raises(ValueError, match="lignes non exécutées"):
        serie.relever(FinDePas(0, o[1], tuple(variables(0).items()), ()))
    relever_un_pas(serie, 0, o)  # rejoué depuis ses clôtures : accepté
    assert serie.serie("B12") == ((0, a_la_main(o, 0)["B12"]),)


def test_cloture_de_phase_d_un_autre_pas_refusee(releve):
    """Mesure de l'audit : une clôture du pas 1 sur l'ouverture du pas 0 était acceptée, et la fin
    du pas 0 lisait ses montants (B12 faux). Elle est refusée ; la fin du pas 0 qui suit, sans
    clôture du pas 0, l'est aussi (lignes non exécutées) ; rejoué, le pas 0 est juste."""
    o, _ = releve
    serie = SerieDuTestZero(o[0], pas_par_an=N_A, r_bar=R_BAR)
    with pytest.raises(ValueError, match="clôture de phase du pas 1 reçue sur l'état "
                                         "d'ouverture du pas 0"):
        serie.relever(cloture(1))
    with pytest.raises(ValueError, match="lignes non exécutées"):
        serie.relever(FinDePas(0, o[1], tuple(variables(0).items()), ()))
    relever_un_pas(serie, 0, o)
    assert serie.serie("B12") == ((0, a_la_main(o, 0)["B12"]),)


def test_ligne_relevee_deux_fois_abandonne_les_montants(releve):
    """Refus d'une ligne relevée deux fois : les montants du pas en cours sont abandonnés, le pas
    se rejoue depuis ses clôtures (sans nouveau refus « relevée deux fois »)."""
    o, _ = releve
    serie = SerieDuTestZero(o[0], pas_par_an=N_A, r_bar=R_BAR)
    serie.relever(cloture(0))
    with pytest.raises(ValueError, match="relevée deux fois"):
        serie.relever(cloture(0))
    relever_un_pas(serie, 0, o)
    assert serie.serie("B12") == ((0, a_la_main(o, 0)["B12"]),)
