"""Bloc 3, travail et salaires : lignes « J3 » de la fiche 3 (§ 9.6) en appel direct (#50).

Classe (a) du classement du rang 1a de J3-b (synthèse en commentaire de la PR
#117, § 1) : T2 (a) ; boucle propre 5 (b) ; borne N ≤ N^pa ; rétention
(identité et ΔIN) ; asymétrie de C ; empreinte. S'y ajoutent la déclaration du
bloc (`tab:travail-phases`, lectures fermées de l'annotation du 13/11/2026,
point 2.5 : π^e lue à l'ouverture, jamais π* ni Γ^e) et la cohérence des
conversions de T4 par appel direct (forme mixte écartée, pouvoir
discriminant). Seuils écrits avant l'essai (fiche 3, § 9.6 ;
`sec:travail-conditions`), non déplacés. Chaque test appelle les fonctions
pures de `nations.blocs.travail` (et de `nations.blocs.production` pour la
rétention et la borne), sans le moteur.

T2 (a) porte sur n_a ∈ {4 ; 12 ; 52} (P56) : les fonctions pures reçoivent des
taux déjà convertis au pas, que le test calcule lui-même pour n_a ≠ 12 (le
moteur ne s'exécute qu'à n_a = 12, M22) ; l'état d'ouverture est celui du
script d'état stationnaire au même n_a.
"""

import ast
import inspect
import math
from dataclasses import replace

import numpy as np
import pytest

from nations.blocs import production as bloc_production
from nations.blocs import travail as bloc
from nations.etat import schema
from nations.moteur.contrat_bloc import OUVERTURE, REGISTRE, Lecture
from nations.moteur.conversions import facteur_par_pas, par_pas
from nations.moteur.parametres import TauxDeCroissance, varier
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE

TABLE = PARAMETRES_DE_REFERENCE.travail
MU_BAR = PARAMETRES_DE_REFERENCE.prix.mu_bar
G_PR = PARAMETRES_DE_REFERENCE.production.g_pr.valeur
N_A = PARAMETRES_DE_REFERENCE.cadre.pas_par_an
# Seuils écrits avant l'essai (fiche 3, § 9.6).
SEUIL_T2 = 1e-10
SEUIL_FORMES = 1e-8
SEUIL_BORNE = 1e-12
SEUIL_RETENTION = 1e-12
SEUIL_CONVERSIONS = 1e-10


# --------------------------------------------------------------------------
# T2 (a) : U* = U^eq sur l'état stationnaire, π̄ ∈ {0 ; 2 % ; 10 %}, n_a ∈ {4 ; 12 ; 52}
# --------------------------------------------------------------------------


def chomage_stationnaire(es, pi, n_a, decalage_de_mu=0.0):
    """U* tel que T3, évaluée sur l'ouverture stationnaire du script (π^e = π̄, μ̃ = ln(1 + μ̄)),
    fasse croître W du facteur du sentier [(1 + g_pr)(1 + π̄)]^{1/n_a} : T3 est affine en
    U_{t−1}, U* s'obtient de deux évaluations. `decalage_de_mu` simule la lecture fautive
    (P_{t−2} au lieu de P_{t−1} : ω_{t−1} multiplié par (1 + π̄)^{1/n_a})."""
    par = replace(es.Parametres(), pi_cible=pi, n_a=n_a, nu_G=1.15)
    o = es.ouverture(es.etat_stationnaire(par), par)
    facteur_pr = (1.0 + par.g_pr) ** (1.0 / n_a)
    facteur_pi = (1.0 + o["pi_e"]) ** (1.0 / n_a)
    cible = math.log(((1.0 + par.g_pr) * (1.0 + pi)) ** (1.0 / n_a))
    omega = bloc.salaire_relatif(o["mu_tilde_m1"] - decalage_de_mu)

    def h(U):
        W = bloc.salaire(o["W_m1"], facteur_pr, facteur_pi, par.lambda_w / n_a,
                         bloc.norme_de_part_salariale(par.mu_bar), omega, par.beta, U, par.U_eq)
        return math.log(W / o["W_m1"]) - cible

    a, b = par.U_eq, par.U_eq + 0.01
    return a - h(a) * (b - a) / (h(b) - h(a)), par


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
@pytest.mark.parametrize("n_a", [4, 12, 52])
def test_t2_a_chomage_stationnaire_egal_au_chomage_d_equilibre(stationnaire, pi, n_a):
    """Fiche 3, § 9.6, T2 (a) : U* = U^eq à 1e−10 relatif, règles SN (T2 sous P54, T3) sur
    l'ouverture stationnaire du script, aux trois π̄ et aux trois n_a."""
    U_etoile, par = chomage_stationnaire(stationnaire, pi, n_a)
    assert abs(U_etoile - par.U_eq) / par.U_eq <= SEUIL_T2


def test_t2_a_pouvoir_discriminant_de_la_lecture_fautive(stationnaire):
    """La lecture fautive (P_{t−2}) déplace U* de −ln(1 + π̄)/(n_a β) : −0,0825 point (2 %,
    n_a = 12) et −1,1914 point (10 %, n_a = 4), valeurs publiées (`sec:travail-salaire`,
    fiche 3, § 9.6), reproduites à leurs décimales ; le cas π̄ = 0 ne discrimine pas."""
    for pi, n_a, publie in ((0.02, 12, -0.0825), (0.10, 4, -1.1914)):
        decalage = math.log(1.0 + pi) / n_a
        U_fautif, par = chomage_stationnaire(stationnaire, pi, n_a, decalage)
        forme = -math.log(1.0 + pi) / (n_a * par.beta)
        assert abs((U_fautif - par.U_eq) - forme) <= 1e-12
        assert round(100.0 * (U_fautif - par.U_eq), 4) == publie
    U_fautif, par = chomage_stationnaire(stationnaire, 0.0, 12, 0.0)
    assert abs(U_fautif - par.U_eq) / par.U_eq <= SEUIL_T2


# --------------------------------------------------------------------------
# Boucle propre 5 (b) : prix et demande exogènes
# --------------------------------------------------------------------------


def jacobienne_de_la_boucle_propre(table):
    """Carte d'un pas (x, n) ↦ (x, n)_{t+1}, x = ln(W/W̄), n = N/N̄ (sentier, g_N = 0),
    composée de T2, T3, T4 et T5 : prix, productivité et demande de travail exogènes sur le
    sentier, μ̃_{t−1} = ln(p pr/W) = ln(1 + μ̄) − x (prix exogène, identité de P54), π^e = π̄.
    Point d'évaluation en régime de baisse de l'emploi (n = 1,001 : effectif excédentaire),
    où T4 est affine ; différences centrées, pas 1e−6."""
    lam_w, lam_N = par_pas(table.lambda_w), par_pas(table.lambda_N)
    facteur_N = facteur_par_pas(table.g_N)
    N_barre, N_pa = 1.0 - table.U_eq, 1.0
    mu = math.log(1.0 + MU_BAR)
    f_pr, f_pi = facteur_par_pas(TauxDeCroissance(G_PR)), facteur_par_pas(TauxDeCroissance(0.02))

    def carte(z):
        x, n = z
        W = bloc.salaire(1.0, f_pr, f_pi, lam_w, bloc.norme_de_part_salariale(MU_BAR),
                         bloc.salaire_relatif(mu - x), table.beta,
                         bloc.chomage(n * N_barre, N_pa), table.U_eq)
        N = bloc.emploi(N_barre, n * N_barre, N_pa, facteur_N, lam_N)
        return np.array([x + math.log(W / (f_pr * f_pi)), N / (facteur_N * N_barre)])

    z0 = np.array([0.0, 1.001])
    jac = np.empty((2, 2))
    for j in range(2):
        h = np.zeros(2)
        h[j] = 1e-6
        jac[:, j] = (carte(z0 + h) - carte(z0 - h)) / 2e-6
    return jac


# (facteur des vitesses, valeur propre de W publiée, de N publiée, demi-vie de N publiée)
VARIANTES = [
    (1.0, 0.91667, 0.70833, 2.01),
    (0.5, 0.95833, 0.85417, 4.40),
    (2.0, 0.83333, 0.41667, 0.79),
]


@pytest.mark.parametrize("facteur, publiee_w, publiee_n, demi_vie", VARIANTES)
def test_boucle_propre_valeurs_propres(facteur, publiee_w, publiee_n, demi_vie):
    """Fiche 3, § 9.6, « Boucle propre (5 (b)) » : valeurs propres réelles, égales aux formes
    fermées 1 − λ_w/n_a et 1 − λ_N/n_a à 1e−8 et aux valeurs publiées à 5 décimales ; module
    < 1 aux trois calibrations ; demi-vie de l'emploi (2,01 / 4,40 / 0,79 tours) à 2
    décimales, dans [2 ; 4] tours à la calibration seule."""
    table = varier(TABLE, lambda_w=facteur * TABLE.lambda_w.valeur,
                   lambda_N=facteur * TABLE.lambda_N.valeur)
    jac = jacobienne_de_la_boucle_propre(table)
    assert abs(jac[1, 0]) <= 1e-12  # triangulaire : N ne dépend pas de W
    valeurs = np.linalg.eigvals(jac)
    assert np.all(np.imag(valeurs) == 0.0) and np.all(np.abs(valeurs) < 1.0)
    vp_w, vp_n = jac[0, 0], jac[1, 1]
    assert abs(vp_w - (1.0 - table.lambda_w.valeur / N_A)) <= SEUIL_FORMES
    assert abs(vp_n - (1.0 - table.lambda_N.valeur / N_A)) <= SEUIL_FORMES
    assert round(vp_w, 5) == publiee_w and round(vp_n, 5) == publiee_n
    demi = math.log(2.0) / -math.log(vp_n)
    assert round(demi, 2) == demi_vie
    if facteur == 1.0:
        assert 2.0 <= demi <= 4.0


# --------------------------------------------------------------------------
# Borne N ≤ N^pa ; rétention ; asymétrie de C
# --------------------------------------------------------------------------


def test_borne_inactive_a_l_etat_resolu():
    """Fiche 3, § 9.6, « Borne » (a) : à l'état résolu (N_{t−1} = N̄(1 + g_N)^{−1/n_a},
    N* = N̄, N^pa = N̄/(1 − U^eq)), N = N* à 1e−12 et N < N^pa strictement (exact), avec la marge
    U^eq : U = U^eq à 1e−12 relatif ; à g_N = 0 et à g_N = 0,005."""
    for g_N in (0.0, 0.005):
        facteur_N = facteur_par_pas(TauxDeCroissance(g_N))
        N_pa = 1.0
        N_barre = (1.0 - TABLE.U_eq) * N_pa
        N = bloc.emploi(N_barre, N_barre / facteur_N, N_pa, facteur_N, par_pas(TABLE.lambda_N))
        assert N < N_pa
        assert abs(N / N_barre - 1.0) <= SEUIL_BORNE
        assert abs(bloc.chomage(N, N_pa) / TABLE.U_eq - 1.0) <= SEUIL_BORNE


def test_borne_active_par_appel_direct():
    """Fiche 3, § 9.6, « Borne » (b) : N* = 1,02 N^pa, N = N^pa et U = 0 exactement ; production
    visée non réalisée 1 − y/y* = 1 − 1/1,02 = 1,96 % à 1e−12 relatif (N5 du bloc 2)."""
    N_pa, pr = 1.0, 1.0016515813
    N_etoile = 1.02 * N_pa
    N = bloc.emploi(N_etoile, N_pa, N_pa, 1.0, par_pas(TABLE.lambda_N))
    assert N == N_pa and bloc.chomage(N, N_pa) == 0.0
    y_etoile = pr * N_etoile
    y = bloc_production.production_du_pas(y_etoile, pr, N)
    non_realisee = 1.0 - y / y_etoile
    assert abs(non_realisee / (1.0 - 1.0 / 1.02) - 1.0) <= SEUIL_BORNE
    assert round(100.0 * non_realisee, 2) == 1.96


def test_retention_identite_et_variation_des_stocks():
    """Fiche 3, § 9.6, « Rétention » (identité et ΔIN) : un pas avec N = 1,02 N*, obtenu par T4
    depuis un effectif excédentaire : WB − UC·y = W(N − y/pr), égal à 1,961 % de WB, à 1e−12
    relatif ; ΔIN (N8, ligne 4) identique au bit au cas N = N*, la production étant y* dans
    les deux cas."""
    lam = par_pas(TABLE.lambda_N)
    W, pr, N_etoile = 0.80132, 1.0016515813, 0.95
    N_prec = (1.02 - lam) * N_etoile / (1.0 - lam)
    N = bloc.emploi(N_etoile, N_prec, 10.0, 1.0, lam)
    assert abs(N / (1.02 * N_etoile) - 1.0) <= SEUIL_RETENTION
    y_etoile = pr * N_etoile
    stocks = {}
    for cas, emploi_du_pas in (("retention", N), ("sans", N_etoile)):
        y = bloc_production.production_du_pas(y_etoile, pr, emploi_du_pas)
        assert y == y_etoile
        UC = bloc_production.cout_unitaire(W, pr)
        WB = bloc.masse_salariale(W, emploi_du_pas)
        disponible = bloc_production.disponible(1.3, y)
        stocks[cas] = bloc_production.variation_des_stocks(
            1.0, UC, y, disponible, bloc_production.stock_en_volume(disponible, 0.9 * y))
        if cas == "retention":
            excedent = W * (emploi_du_pas - y / pr)
            assert abs((WB - UC * y) - excedent) / WB <= SEUIL_RETENTION
            assert abs((WB - UC * y) / WB / (1.0 - 1.0 / 1.02) - 1.0) <= SEUIL_RETENTION
            assert round(100.0 * excedent / WB, 3) == 1.961
    assert stocks["retention"] == stocks["sans"]


def test_asymetrie_de_c_structure_exacte():
    """Fiche 3, § 9.6, « Asymétrie de C » : par appel direct de T4 sur 20 000 tirages (graine
    20261113), borne inactive : si N* ≥ (1 + g_N)^{1/n_a} N_{t−1}, alors N = N* exactement ;
    sinon N* < N < (1 + g_N)^{1/n_a} N_{t−1} ; à g_N = 0 et à g_N = 0,005."""
    rng = np.random.default_rng(20261113)
    lam = par_pas(TABLE.lambda_N)
    hausses = baisses = 0
    for g_N in (0.0, 0.005):
        facteur_N = facteur_par_pas(TauxDeCroissance(g_N))
        for N_prec, rapport in zip(10.0 ** rng.uniform(-3, 3, 10_000),
                                   rng.uniform(0.5, 1.5, 10_000), strict=True):
            N_prec = float(N_prec)
            N_etoile = float(rapport) * facteur_N * N_prec
            N = bloc.emploi(N_etoile, N_prec, 10.0 * max(N_etoile, N_prec), facteur_N, lam)
            if N_etoile >= facteur_N * N_prec:
                assert N == N_etoile
                hausses += 1
            else:
                assert N_etoile < N < facteur_N * N_prec
                baisses += 1
    assert hausses > 0 and baisses > 0


def test_coherence_des_conversions_forme_mixte_ecartee():
    """Fiche 3, § 9.6, « Cohérence des conversions » (pouvoir discriminant, appel direct de
    T4) : à g_N = 0,005, N* croissant de (1 + g_N)^{1/n_a} par pas, la forme retenue (facteur
    géométrique) garde N = N* (|N/N* − 1| ≤ 1e−10 sur 720 pas) ; la forme mixte (facteur
    linéaire 1 + g_N/n_a) laisse un sureffectif stationnaire de 2,3e−6 à λ_N = 3,5 (5,0e−6 à
    λ_N = 1,9092), valeurs publiées (`sec:travail-population`), reproduites à 2 chiffres."""
    g_N = 0.005
    taux = varier(TABLE, g_N=g_N).g_N
    geometrique = facteur_par_pas(taux)
    lineaire = 1.0 + g_N / N_A  # forme mixte écartée, écrite ici pour l'essai seulement
    for lambda_N, publie in ((3.5, 2.3e-6), (1.9092, 5.0e-6)):
        lam = lambda_N / N_A
        pires = {}
        for nom, facteur in (("geometrique", geometrique), ("lineaire", lineaire)):
            N_prec, N_etoile, pire = 1.0 / geometrique, 1.0, 0.0
            for _ in range(720):
                N = bloc.emploi(N_etoile, N_prec, 1e9, facteur, lam)
                ecart_du_pas = abs(N / N_etoile - 1.0)
                # géométrique : maximum sur 720 pas ; linéaire : valeur stationnaire (dernier pas)
                pire = max(pire, ecart_du_pas) if nom == "geometrique" else ecart_du_pas
                N_prec, N_etoile = N, N_etoile * geometrique
            pires[nom] = pire
        assert pires["geometrique"] <= SEUIL_CONVERSIONS
        assert float(f"{pires['lineaire']:.1e}") == publie, pires


# --------------------------------------------------------------------------
# Empreinte et déclaration
# --------------------------------------------------------------------------


def test_empreinte_quatre_variables_sans_registre_ni_tirage():
    """Fiche 3, § 9.6, « Empreinte » : W, U, N, N^pa au radical `travail`, scalaires (aucun
    historique), W écrite en phase 1, U, N et N^pa en phase 4 ; aucune lecture du registre ;
    le module n'importe que `math`, `contrat_bloc` et `conversions` (aucun générateur
    aléatoire) ; le bloc n'a pas d'attribut d'instance."""
    variables = [v for v in schema.VARIABLES_DES_BLOCS if v.proprietaire == "travail"]
    assert [(v.nom, v.phase_ecriture) for v in variables] == [
        ("W", "1"), ("U", "4"), ("N", "4"), ("N_pa", "4")]
    assert all(v.type is float and v.longueur == 1 for v in variables)
    sieges = {s.etape: s for s in bloc.Travail.declaration.sieges}
    assert sieges["1"].etat == ("W",) and set(sieges["4"].etat) == {"U", "N", "N_pa"}
    assert not any(lu.source == REGISTRE for s in sieges.values() for lu in s.lit)
    arbre = ast.parse(inspect.getsource(bloc))
    importes = {n.module for n in ast.walk(arbre) if isinstance(n, ast.ImportFrom)}
    importes |= {a.name for n in ast.walk(arbre) if isinstance(n, ast.Import) for a in n.names}
    assert importes == {"__future__", "math", "nations.moteur.contrat_bloc",
                        "nations.moteur.conversions"}
    instance = bloc.Travail()
    assert not hasattr(instance, "__dict__") and bloc.Travail.__slots__ == ()


def test_declaration_conforme_a_tab_travail_phases():
    """`tab:travail-phases` et ADR 0012, annotation du 13/11/2026, points 2.2 et 2.5 : phases 1
    et 4 ; en phase 1, lectures de l'ouverture seules, exactement W, U, μ̃ et π^e (jamais π*
    ni Γ^e à la place de π^e, ni le registre) ; en phase 4, N* (phase 2), W_t (phase 1),
    N et N^pa d'ouverture, aucune lecture de y, y^cap ni tu ; ligne 5 seule proposée."""
    sieges = {s.etape: s for s in bloc.Travail.declaration.sieges}
    assert tuple(sieges) == ("1", "4")
    assert set(sieges["1"].lit) == {Lecture(OUVERTURE, n) for n in ("W", "U", "mu_tilde", "pi_e")}
    assert set(sieges["4"].lit) == {Lecture(OUVERTURE, "N"), Lecture(OUVERTURE, "N_pa"),
                                    Lecture("1", "W_suivant"), Lecture("2", "N_etoile")}
    lus = {lu.nom for s in sieges.values() for lu in s.lit}
    assert not lus & {"y", "y_cap", "tu", "pi_etoile", "Gamma_e", "gamma_e"}
    assert [s.propose for s in sieges.values()] == [(), ("5",)]
    assert all(s.ecrit == () and s.couvre == () for s in sieges.values())
