"""Bloc 4, prix : lignes « J3 » de la fiche 4 (§ 9.6) en appel direct (#51).

Classe (a) du classement du rang 1a de J3-b (synthèse en commentaire de la PR
#117, § 1) : T2 (a) ; boucle propre (0,9) ; positivité ; empreinte (μ̃). S'y
ajoute la déclaration du bloc (`tab:prix-phases`, lectures fermées de
l'annotation du 13/11/2026, point 2.5 : ni ventes, ni demande, ni plan, ni
registre ; premier groupe de la phase 5). Seuils écrits avant l'essai (fiche 4,
§ 9.6 ; `sec:prix-conditions`), non déplacés. Chaque test appelle les
fonctions pures de `nations.blocs.prix` (et de `nations.blocs.production` et
`nations.blocs.travail` pour T2 (a)), sans le moteur.

T2 (a) porte sur n_a ∈ {4 ; 12 ; 52} (P56) : les fonctions pures reçoivent des
taux déjà convertis au pas, que le test calcule lui-même pour n_a ≠ 12 ;
l'état d'ouverture est celui du script d'état stationnaire au même n_a.
"""

import ast
import inspect
import math
from dataclasses import replace

import pytest

from nations.blocs import prix as bloc
from nations.blocs import production as bloc_production
from nations.blocs import travail as bloc_travail
from nations.etat import schema
from nations.moteur.contrat_bloc import OUVERTURE, REGISTRE, Lecture
from nations.moteur.conversions import par_pas
from nations.moteur.parametres import varier
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.moteur.phases import PHASES

TABLE = PARAMETRES_DE_REFERENCE.prix
N_A = PARAMETRES_DE_REFERENCE.cadre.pas_par_an
# Seuils écrits avant l'essai (fiche 4, § 9.6 ; fiche 3, § 9.6 pour T2).
SEUIL_T2 = 1e-10
SEUIL_FORMES = 1e-8


# --------------------------------------------------------------------------
# T2 (a) : un pas des règles SN et M sur l'ouverture stationnaire, n_a ∈ {4 ; 12 ; 52}
# --------------------------------------------------------------------------


def un_pas_des_regles_sn_et_m(es, pi, n_a):
    """Un pas des règles des blocs 3 et 4 (T2, T3 ; P1 à P3) et de N2, N8 du bloc 2, appelées
    directement sur l'ouverture stationnaire du script à (π̄, n_a) ; rend (W_0, p_0, μ̃_0, ξ_0,
    U*, paramètres, ouverture), U* étant le chômage d'ouverture qui fait croître W, au pas
    suivant, du facteur du sentier (T3 affine en U, deux évaluations)."""
    par = replace(es.Parametres(), pi_cible=pi, n_a=n_a, nu_G=1.15)
    o = es.ouverture(es.etat_stationnaire(par), par)
    f_pr = (1.0 + par.g_pr) ** (1.0 / n_a)
    f_pi = (1.0 + o["pi_e"]) ** (1.0 / n_a)
    lam_w, lam_mu = par.lambda_w / n_a, par.lambda_mu / n_a
    omega_etoile = bloc_travail.norme_de_part_salariale(par.mu_bar)

    def salaire(W_prec, mu_prec, U_prec):
        return bloc_travail.salaire(W_prec, f_pr, f_pi, lam_w, omega_etoile,
                                    bloc_travail.salaire_relatif(mu_prec), par.beta, U_prec,
                                    par.U_eq)

    W0 = salaire(o["W_m1"], o["mu_tilde_m1"], o["U_m1"])
    UC0 = bloc_production.cout_unitaire(W0, o["pr"])
    cible = bloc_production.stock_cible(o["ve"], par.sigma, n_a)
    xi0 = bloc.tension_sur_les_stocks(o["IN_vol"], cible)
    mu0 = bloc.marge(o["mu_tilde_m1"], xi0, lam_mu, par.mu_bar, par.psi_xi)
    p0 = bloc.prix_du_pas(UC0, mu0)
    # Pas 1 : W croît du facteur du sentier si et seulement si U_0 = U*.
    facteur_W = ((1.0 + par.g_pr) * (1.0 + pi)) ** (1.0 / n_a)

    def h(U):
        return math.log(salaire(W0, mu0, U) / W0) - math.log(facteur_W)

    a, b = par.U_eq, par.U_eq + 0.01
    U_etoile = a - h(a) * (b - a) / (h(b) - h(a))
    return W0, p0, mu0, xi0, U_etoile, par, o


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
@pytest.mark.parametrize("n_a", [4, 12, 52])
def test_t2_a_regles_sn_et_m(stationnaire, pi, n_a):
    """Fiche 4, § 9.6, T2 (test commun avec la fiche 3), partie (a), règle M : sur l'ouverture
    stationnaire du script à (π̄, n_a), un pas des règles laisse ξ = 0 (1e−10 en absolu),
    μ̃ = ln(1 + μ̄), W et p sur leur sentier (facteurs [(1 + g_pr)(1 + π̄)]^{1/n_a} et
    (1 + π̄)^{1/n_a}) à 1e−10 relatif, et le chômage stationnaire U* = U^eq à 1e−10 relatif."""
    W0, p0, mu0, xi0, U_etoile, par, o = un_pas_des_regles_sn_et_m(stationnaire, pi, n_a)
    assert abs(xi0) <= SEUIL_T2
    assert abs(mu0 / math.log(1.0 + par.mu_bar) - 1.0) <= SEUIL_T2
    facteur_W = ((1.0 + par.g_pr) * (1.0 + pi)) ** (1.0 / n_a)
    assert abs(W0 / (o["W_m1"] * facteur_W) - 1.0) <= SEUIL_T2
    assert abs(p0 / (o["registre"][0] * (1.0 + pi) ** (1.0 / n_a)) - 1.0) <= SEUIL_T2
    assert abs(U_etoile - par.U_eq) / par.U_eq <= SEUIL_T2


# --------------------------------------------------------------------------
# Boucle propre : coûts et tension exogènes
# --------------------------------------------------------------------------


# (facteur de λ_μ, valeur propre publiée, demi-vie publiée en tours ; `sec:prix-conditions`)
VARIANTES = [(1.0, 0.9, 6.58), (0.5, 0.95, 13.51), (2.0, 0.8, 3.11)]


@pytest.mark.parametrize("facteur, publiee, demi_vie", VARIANTES)
def test_boucle_propre_valeur_propre(facteur, publiee, demi_vie):
    """Fiche 4, § 9.6, « Boucle propre » : à coûts et tension exogènes, dμ̃_t/dμ̃_{t−1} = 1 −
    λ_μ/n_a (différence centrée, pas 1e−6), égale à la forme fermée à 1e−8 et à la valeur
    publiée (0,9 ; 0,95 ; 0,8) ; module < 1 ; demi-vie publiée (6,58 / 13,51 / 3,11 tours) à 2
    décimales."""
    table = varier(TABLE, lambda_mu=facteur * TABLE.lambda_mu.valeur)
    lam = par_pas(table.lambda_mu)
    mu0, h = math.log(1.0 + table.mu_bar), 1e-6
    derivee = (bloc.marge(mu0 + h, 0.0, lam, table.mu_bar, table.psi_xi)
               - bloc.marge(mu0 - h, 0.0, lam, table.mu_bar, table.psi_xi)) / (2.0 * h)
    assert abs(derivee - (1.0 - table.lambda_mu.valeur / N_A)) <= SEUIL_FORMES
    assert abs(derivee) < 1.0 and round(derivee, 5) == publiee
    assert round(math.log(2.0) / -math.log(derivee), 2) == demi_vie


# --------------------------------------------------------------------------
# Positivité
# --------------------------------------------------------------------------


@pytest.mark.parametrize("stock, xi_attendue", [(0.0, 1.0), (10.0, -9.0)])
def test_positivite(stock, xi_attendue):
    """Fiche 4, § 9.6, « Positivité » : stock nul (ξ = 1) et stock à dix fois sa cible (ξ = −9) :
    ξ exacte, p > 0 et fini par la forme exponentielle, au premier pas et après 720 pas de
    tension maintenue (la marge tend vers ln(1 + μ̄) + ψ_ξ ξ, sans borne)."""
    cible, UC = 1.4, 0.8
    xi = bloc.tension_sur_les_stocks(stock * cible, cible)
    assert xi == xi_attendue
    lam, mu = par_pas(TABLE.lambda_mu), math.log(1.0 + TABLE.mu_bar)
    for _ in range(720):
        mu = bloc.marge(mu, xi, lam, TABLE.mu_bar, TABLE.psi_xi)
        p = bloc.prix_du_pas(UC, mu)
        assert p > 0.0 and math.isfinite(p)
    assert abs(mu - (math.log(1.0 + TABLE.mu_bar) + TABLE.psi_xi * xi)) <= 1e-12


def test_indice_egal_au_prix():
    """P4 : P_t ≡ p_t (J = 1), au bit."""
    for p in (1e-300, 0.8, 1.0016515813, 1e300):
        assert bloc.indice_des_prix(p) == p


# --------------------------------------------------------------------------
# Empreinte et déclaration
# --------------------------------------------------------------------------


def test_empreinte_une_variable_d_etat_mu_tilde():
    """Fiche 4, § 9.6, « Empreinte » : une seule variable d'état propre, μ̃ (§ 9.1, P54),
    scalaire, écrite en phase 5 ; aucune lecture du registre ; le module n'importe que
    `math`, `contrat_bloc` et `conversions` (aucun générateur aléatoire) ; le bloc n'a pas
    d'attribut d'instance."""
    variables = [v for v in schema.VARIABLES_DES_BLOCS if v.proprietaire == "prix"]
    assert [(v.nom, v.phase_ecriture, v.type, v.longueur) for v in variables] == [
        ("mu_tilde", "5", float, 1)]
    (siege,) = bloc.Prix.declaration.sieges
    assert siege.etat == ("mu_tilde",)
    assert not any(lu.source == REGISTRE for lu in siege.lit)
    arbre = ast.parse(inspect.getsource(bloc))
    importes = {n.module for n in ast.walk(arbre) if isinstance(n, ast.ImportFrom)}
    importes |= {a.name for n in ast.walk(arbre) if isinstance(n, ast.Import) for a in n.names}
    assert importes == {"__future__", "math", "nations.moteur.contrat_bloc",
                        "nations.moteur.conversions"}
    instance = bloc.Prix()
    assert not hasattr(instance, "__dict__") and bloc.Prix.__slots__ == ()


def test_declaration_conforme_a_tab_prix_phases():
    """`tab:prix-phases` et ADR 0012, annotation du 13/11/2026, points 2.2, 2.3 et 2.5 : phase 5
    seule, premier groupe ; lectures exactement IN^vol et μ̃ d'ouverture, IN^vol* et UC de la
    phase 2 (ni v, ni d, ni plan, ni registre, ni W) ; écrit ξ, p et P ; aucune ligne."""
    (siege,) = bloc.Prix.declaration.sieges
    assert siege.etape == "5"
    etape_5 = next(e for phase in PHASES for e in phase.etapes if e.identifiant == "5")
    assert etape_5.groupes[0] == ("prix",)
    assert set(siege.lit) == {Lecture(OUVERTURE, "IN_vol"), Lecture(OUVERTURE, "mu_tilde"),
                              Lecture("2", "IN_vol_etoile"), Lecture("2", "UC")}
    assert not {lu.nom for lu in siege.lit} & {"v", "d", "C_plan", "I_plan", "G_plan", "W",
                                               "W_suivant", "C_vol", "I_vol", "G_vol"}
    assert set(siege.ecrit) == {"xi", "p", "P"}
    assert siege.propose == () and siege.couvre == ()
