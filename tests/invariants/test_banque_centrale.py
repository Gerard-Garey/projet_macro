"""Bloc 8, banque centrale et anticipations, dans le socle partiel d'essai : lignes de classe (b) (#91).

Classe (b) du classement du rang 1a de J3-c (synthèse en commentaire de la PR
#129, § 1 ; fiche 8, § 9.6) : état stationnaire (P77 : moteur à n_a = 12 aux
trois π*, valeurs de référence du script `outils/etat_stationnaire.py`, jamais
recopiées) ; résultat et lignes exécutées ; cible (ADR 0010, test 4) ; parties
(b) de « Phases » (lecture hors ordre refusée à l'assemblage), « Bornes »
(G^plan −5 % aux tours 1 à 12, marche de cible de ±1 point, taux négatif) et
« Empreinte » (reprise exacte, tenue par `test_socle_partiel.py` avec tous les
blocs réels, et la part du bloc, par `test_budget.py`). S'y ajoutent les blocs
d'essai 9 E1 (couverture de la ligne 16 sur Π^CB lu en phase 1) et E2 (lignes
11a à 11c selon E7), P95. Seuils écrits avant l'essai (fiche 8, § 9.6), non
déplacés.

Les blocs réels de la production, du travail, des prix et de la banque centrale
remplacent les blocs d'essai de leur radical ; la banque (bloc 7, B7 en −min) et
les blocs 5, 6 et 9 sont des blocs d'essai sur le sentier. **Étiquettes** :
toute mesure dynamique porte « plans nominaux exogènes » ; la boucle T3 ↔ BC3
est fermée (blocs 3 et 8 réels), mais aucune mesure ici ne vaut verdict de la
boucle T3 ↔ BC3 (P87, rang 6) ni de la boucle conjointe de la fiche 8 (#114).
"""

import dataclasses

import pytest

from nations.blocs.banque_centrale import BanqueCentrale, taux_indique_par_la_regle
from nations.blocs.prix import Prix
from nations.blocs.production import Production
from nations.blocs.travail import Travail
from nations.moteur import ordonnanceur as ordo
from nations.moteur.contrat_bloc import Lecture
from nations.moteur.conversions import par_pas
from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres import TauxDeFlux
from nations.moteur.parametres.cadre import PAS_PAR_AN
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas

N_A = PAS_PAR_AN.valeur
NB_PAS = 720
ETIQUETTES = "plans nominaux exogènes ; blocs 2, 3, 4 et 8 réels ; bloc 7 d'essai"
# Seuils écrits avant l'essai (fiche 8, § 9.6).
SEUIL_UN_PAS = 1e-10
SEUIL_720_PAS = 1e-9
SEUIL_CB = 1e-12  # × S^CB
LIGNES_DU_BLOC = ("11a", "11b", "11c", "12", "13", "16")
VARIABLES_DU_BLOC = ("pi_e", "r_hat_etoile", "pi_etoile")


class Releve:
    """Observateur d'essai : par pas, montants exécutés des lignes 11a à 16, variables du pas,
    état t + 1."""

    def __init__(self):
        self.pas = []
        self._montants = {}

    def relever(self, e):
        if type(e) is ClotureDePhase:
            for ligne, termes in e.montants:
                if ligne in LIGNES_DU_BLOC:
                    self._montants[ligne] = sum(x for _, x in termes)
        elif type(e) is FinDePas:
            self.pas.append({**self._montants, "t": e.t, "variables": dict(e.variables_du_pas),
                             "etat": e.etat})
            self._montants = {}


def ecart(x, reference):
    """|x/x̄ − 1| ; pour une valeur de référence nulle, |x|."""
    return abs(x) if reference == 0.0 else abs(x / reference - 1.0)


def positions(etat):
    return {nom: getattr(etat, nom) for nom in cat.NOMS_POSTES}


def echelle_cb(etat):
    """S^CB à l'ouverture : somme des valeurs absolues des postes du bilan de la banque
    centrale, valeur nette comprise (`eq:noyau-echelle-bilan`)."""
    return idt.echelle_bilan(positions(etat), "banque_centrale")


def reels():
    return (Production(), Travail(), Prix(), BanqueCentrale())


def derouler(socle, sentier, nb_pas, initial=None, **options):
    releve = Releve()
    initial = socle.etat_initial(sentier) if initial is None else initial
    o = socle.ordonnanceur(sentier, reels=reels(), **options)
    socle.derouler(initial, nb_pas, o, releve)
    return initial, releve


@pytest.fixture(scope="module")
def trajectoires(socle):
    """Une trajectoire de 720 pas par π*, depuis l'état résolu, sans choc, blocs 2, 3, 4 et 8
    réels."""
    return {pi: (socle.sentier(pi),) + derouler(socle, socle.sentier(pi), NB_PAS)
            for pi in socle.POINTS_PI}


# --------------------------------------------------------------------------
# État stationnaire (P77) et résultat
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_un_pas_depuis_l_etat_resolu_egal_au_script(trajectoires, pi, publier):
    """Fiche 8, § 9.6, « État stationnaire », sous P77 (n_a = 12, π* ∈ {0 ; 2 % ; 10 %}) : un
    pas sans choc depuis l'état résolu laisse r̂* = r̄, π^e = π*, i_CB = i^règle = (1 + r̄)(1 +
    π*) − 1, Π^CB = i_CB (M^G + E^CB)/n_a, Res = 0 et L^CB = `L_CB_1` du script, à 1e−10
    relatif (Res nul : |Res| ≤ 1e−12 × S^CB) ; chaque valeur comparée au script (`un_pas`), et
    i_CB égal à i^règle exactement."""
    sentier, initial, releve = trajectoires[pi]
    s, par = sentier.s, sentier.par
    v, apres = releve.pas[0]["variables"], releve.pas[0]["etat"]
    assert v["i_CB"] == v["i_regle"]
    E_CB = idt.valeur_nette_stock(positions(initial), "banque_centrale")
    ecarts = {
        "r̂*_1 (script)": ecart(apres.r_hat_etoile, s["r_hat_1"]),
        "r̂*_1/r̄": ecart(apres.r_hat_etoile, par.rbar),
        "π^e_1 (script)": ecart(apres.pi_e, s["pi_e_1"]),
        "π^e_1/π*": ecart(apres.pi_e, pi),
        "i_CB (script)": ecart(v["i_CB"], s["i_CB"]),
        "i_CB (forme fermée)": ecart(v["i_CB"], (1 + par.rbar) * (1 + pi) - 1),
        "Π^CB (script)": ecart(v["Pi_CB"], s["Pi_CB"]),
        "Π^CB (au socle)": ecart(v["Pi_CB"], v["i_CB"] * (initial.M_G + E_CB) / N_A),
        "L^CB_1 (script)": ecart(apres.L_CB, s["L_CB_1"]),
    }
    for nom, x in ecarts.items():
        assert x <= SEUIL_UN_PAS, (nom, x)
    res = abs(apres.Res) / echelle_cb(initial)
    assert res <= SEUIL_CB
    publier(f"Bloc 8, un pas depuis l'état résolu, π* = {100 * pi:g} % ({ETIQUETTES})", [
        " ; ".join(f"{n} {x:.1e}" for n, x in ecarts.items())
        + f" (seuil 1e−10) ; |Res_1|/S^CB {res:.1e} (seuil 1e−12)"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_etat_initial_resolu_du_bloc_8(socle, pi):
    """Critère de #91 « L^CB_0 = M^G_0 » et état initial résolu du bloc
    (`sec:banque_centrale-stationnaire`) : r̂*_0 = r̄, π^e_0 = π*_0 = π*, E^CB_0 = 0, B_CB,0 =
    θ_CB B_0 = 0 au socle, Res_0 = 0 et L^CB_0 = M^G_0, égal à l'encaisse M^G_0 du script
    (`etat_stationnaire`, jamais un chiffre recopié) ; registre stationnaire, d'où π_{−1} =
    π* à 1e−15 et i^règle_0 = i_CB,0 = (1 + r̄)(1 + π*) − 1 à 1e−15 relatif."""
    sentier = socle.sentier(pi)
    initial = socle.etat_initial(sentier)
    par = sentier.par
    assert initial.r_hat_etoile == par.rbar
    assert initial.pi_e == initial.pi_etoile == pi
    assert idt.valeur_nette_stock(positions(initial), "banque_centrale") == 0.0
    assert initial.B_CB == par.theta_CB * (initial.B_H + initial.B_Bk + initial.B_CB) == 0.0
    assert initial.Res == 0.0
    assert initial.L_CB == initial.M_G == sentier.e["M_G"]
    pi_prec = initial.registre_prix[0] / initial.registre_prix[N_A] - 1.0
    assert abs(pi_prec - pi) <= 1e-15
    i_0 = taux_indique_par_la_regle(initial.r_hat_etoile, initial.pi_etoile, pi_prec, par.a_pi)
    assert abs(i_0 / ((1.0 + par.rbar) * (1.0 + pi) - 1.0) - 1.0) <= 1e-15


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_cablage_de_bc2_bc3_et_bc8_hors_du_point_fixe(socle, pi):
    """Constat M1 de l'audit du rang 4 : les méthodes de phase passent à BC2, BC3 et BC8 les bonnes
    entrées. Depuis l'état résolu, π^e_0 = π̄ + 1 point, π*_0 = π̄ − 0,5 point et r̂*_0 = r̄,
    d'où π^e_0, π*_0 et π_{−1} (lu au registre d'ouverture) distincts ; après un pas, au bit :
    π^e_1 = (1 − c) π^e_0 + c π_{−1}, c = λ_e/12 (BC3) ; r̂*_1 = r̂*_0 + (a_I/12)(π_{−1} − π*_0)
    (BC2) ; ligne 13 exécutée = (i_CB/12) L^CB_0 (BC8, sur le refinancement, non les réserves) ;
    formes recalculées par le test, sans appeler le bloc."""
    sentier = socle.sentier(pi)
    initial = dataclasses.replace(socle.etat_initial(sentier), pi_e=pi + 0.01,
                                  pi_etoile=pi - 0.005)
    _, releve = derouler(socle, sentier, 1, initial=initial)
    table = socle.PARAMETRES_DE_REFERENCE.banque_centrale
    pi_prec = initial.registre_prix[0] / initial.registre_prix[N_A] - 1.0
    assert len({pi_prec, initial.pi_e, initial.pi_etoile}) == 3
    c = table.lambda_e.valeur / 12
    apres, v = releve.pas[0]["etat"], releve.pas[0]["variables"]
    assert apres.pi_e.hex() == ((1.0 - c) * initial.pi_e + c * pi_prec).hex()
    assert apres.r_hat_etoile.hex() == (
        initial.r_hat_etoile + table.a_I.valeur / 12 * (pi_prec - initial.pi_etoile)).hex()
    assert initial.L_CB > 0.0 and initial.Res == 0.0
    assert releve.pas[0]["13"].hex() == (v["i_CB"] / 12 * initial.L_CB).hex()


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_variables_du_bloc_sur_leur_sentier_720_pas(trajectoires, socle, pi):
    """π^e, r̂* et π* restent sur leur sentier (π^e = π*, r̂* = r̄, π* constante) à 1e−9 relatif
    sur 720 pas, la boucle T3 ↔ BC3 fermée ; π* exactement."""
    sentier, initial, releve = trajectoires[pi]
    for t, p in enumerate(releve.pas):
        for nom in VARIABLES_DU_BLOC:
            assert ecart(getattr(p["etat"], nom),
                         socle.valeur_d_ouverture(sentier, nom, t + 1)) <= SEUIL_720_PAS, (t, nom)
        assert p["etat"].pi_etoile == initial.pi_etoile
        assert p["variables"]["i_CB"] == p["variables"]["i_regle"]


def _resultat_et_lignes(releve, initial):
    """max_t |Π^CB_t − (11c + 13 − 12)_t| / S^CB_t et max_t des écarts des lignes 11a à 11c à E7
    (i_CB/n_a × encours d'ouverture), rapportés à S^CB_t."""
    ouvertures = [initial] + [p["etat"] for p in releve.pas[:-1]]
    pire, pire_e7 = 0.0, 0.0
    for o, p in zip(ouvertures, releve.pas):
        S = echelle_cb(o)
        v = p["variables"]
        pire = max(pire, abs(v["Pi_CB"] - (p["11c"] + p["13"] - p["12"])) / S)
        i_pas = par_pas(TauxDeFlux(v["i_CB"]))
        for ligne, encours in (("11a", o.B_H), ("11b", o.B_Bk), ("11c", o.B_CB)):
            pire_e7 = max(pire_e7, abs(p[ligne] - i_pas * encours) / S)
    return pire, pire_e7


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_resultat_egal_aux_lignes_executees(trajectoires, pi, publier):
    """Fiche 8, § 9.6, « Résultat et lignes exécutées » : à chaque pas, Π^CB_t écrit en phase 1
    égale les lignes 11c + 13 − 12 exécutées, à 1e−12 × S^CB, sur 720 pas ; la ligne 16
    exécutée égale Π^CB (BC9) ; les lignes 11a à 11c du bloc d'essai 9 suivent E7 (E2)."""
    _, initial, releve = trajectoires[pi]
    pire, pire_e7 = _resultat_et_lignes(releve, initial)
    assert pire <= SEUIL_CB and pire_e7 <= SEUIL_CB
    assert all(p["16"] == p["variables"]["Pi_CB"] for p in releve.pas)
    publier(f"Bloc 8, résultat et lignes exécutées, π* = {100 * pi:g} %, 720 pas ({ETIQUETTES})",
            [f"max |Π^CB − (11c + 13 − 12)|/S^CB = {pire:.1e} ; max |ligne 11x − E7|/S^CB = "
             f"{pire_e7:.1e} (seuil 1e−12)"])


def _avec_titres_a_la_banque_centrale(initial, part=0.2, decalage_r_hat=0.01):
    """État hors du sentier : la banque centrale détient `part` des titres de la banque, payés en
    réserves (B_CB = Res = x, B_Bk − x ; valeurs nettes inchangées), et r̂*_0 = r̄ + décalage,
    d'où i_CB hors du sentier."""
    x = part * initial.B_Bk
    return dataclasses.replace(initial, B_Bk=initial.B_Bk - x, B_CB=initial.B_CB + x,
                               Res=initial.Res + x,
                               r_hat_etoile=initial.r_hat_etoile + decalage_r_hat)


def test_e2_et_resultat_avec_titres_et_reserves(socle, publier):
    """Bloc d'essai 9, E2 (P95), et forme générale de BC6 hors du socle : B_CB > 0, Res > 0 et
    i_CB hors du sentier à l'ouverture ; sur 6 pas, les lignes 11a à 11c exécutées suivent E7
    au taux du tour lu en phase 1, et Π^CB = 11c + 13 − 12 exécutées, à 1e−12 × S^CB ; la
    ligne 11c et la ligne 12 ne sont pas nulles au premier pas. Horizon court : hors du
    sentier, les plans nominaux exogènes du banc vident le compte du Trésor (arrêt du noyau
    mesuré au pas 16, ligne 2) ; même cause que P87 (e), hors de P87 : l'essai ne le juge
    pas."""
    sentier = socle.sentier(0.02)
    initial = _avec_titres_a_la_banque_centrale(socle.etat_initial(sentier))
    _, releve = derouler(socle, sentier, 6, initial=initial)
    assert releve.pas[0]["11c"] > 0.0 and releve.pas[0]["12"] > 0.0
    pire, pire_e7 = _resultat_et_lignes(releve, initial)
    assert pire <= SEUIL_CB and pire_e7 <= SEUIL_CB
    publier(f"Bloc 8 et bloc d'essai 9 (E2), B_CB = Res = 20 % de B_Bk, r̂*_0 = r̄ + 1 point, "
            f"6 pas ({ETIQUETTES})", [
                f"max |Π^CB − (11c + 13 − 12)|/S^CB = {pire:.1e} ; max |ligne 11x − E7|/S^CB "
                f"= {pire_e7:.1e} (seuil 1e−12)"])


# --------------------------------------------------------------------------
# Cible (ADR 0010, test 4), bornes, taux négatif et E1
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_cible_identique_a_celle_du_proprietaire_provisoire(trajectoires, socle, pi):
    """Fiche 8, § 9.6, « Cible » (ADR 0010, test 4) : à levier fermé, π*_{t+1} = π*_t à chaque
    pas, et la trajectoire de π* du bloc réel est identique au bit à celle du bloc d'essai 8
    (BC4 reconduite depuis l'ouverture, propriétaire provisoire du rang 3), sur 720 pas."""
    sentier, initial, releve = trajectoires[pi]
    essai = Releve()
    socle.derouler(initial, NB_PAS, socle.ordonnanceur(
        sentier, reels=(Production(), Travail(), Prix())), essai)
    assert [p["etat"].pi_etoile for p in releve.pas] == [p["etat"].pi_etoile for p in essai.pas]
    assert all(p["etat"].pi_etoile == initial.pi_etoile for p in releve.pas)


def _r_hat_identite(initial, releve, a_I):
    """|r̂*_T − r̂*_0 − (a_I/n_a) Σ_t (π_{t−1} − π*_t)| : BC2 accumulée sur la trajectoire, π_{t−1}
    lu au registre de chaque ouverture."""
    ouvertures = [initial] + [p["etat"] for p in releve.pas[:-1]]
    somme = sum(o.registre_prix[0] / o.registre_prix[N_A] - 1.0 - o.pi_etoile for o in ouvertures)
    return abs(releve.pas[-1]["etat"].r_hat_etoile - initial.r_hat_etoile - a_I / N_A * somme)


@pytest.mark.parametrize("pi_0", [0.01, 0.03])
def test_marche_de_cible_prescription_exacte(socle, pi_0, publier):
    """Fiche 8, § 9.6, « Bornes » (marche de cible) et « Cible » : sur le sentier à π̄ = 2 %, une
    cible en vigueur π*_0 = 2 % ± 1 point est reconduite au bit sur 36 pas ; i_CB égale
    exactement la prescription à chaque pas ; à l'impact, une cible abaissée baisse la
    prescription de [(1 + r̂*) − a_π] point par point de cible (`sec:banque_centrale-regle`) ;
    BC2 accumule l'écart (r̂*_T − r̂*_0 = (a_I/n_a) Σ(π_{t−1} − π*), à 1e−12) ; aucun arrêt du
    noyau sur 36 pas (au-delà, les plans nominaux exogènes du banc vident le compte du Trésor :
    arrêt mesuré au pas 72 pour π*_0 = 1 % ; même cause que P87 (e), hors de P87). Taux
    minimal publié, sur la fenêtre des 36 pas."""
    sentier = socle.sentier(0.02)
    initial = dataclasses.replace(socle.etat_initial(sentier), pi_etoile=pi_0)
    _, releve = derouler(socle, sentier, 36, initial=initial)
    assert all(p["etat"].pi_etoile == pi_0 for p in releve.pas)
    assert all(p["variables"]["i_CB"] == p["variables"]["i_regle"] for p in releve.pas)
    table = socle.PARAMETRES_DE_REFERENCE.banque_centrale
    impact = (releve.pas[0]["variables"]["i_regle"] - sentier.s["i_CB"]) / (pi_0 - 0.02)
    assert impact == pytest.approx((1 + initial.r_hat_etoile) - table.a_pi, rel=1e-9)
    identite = _r_hat_identite(initial, releve, table.a_I.valeur)
    assert identite <= 1e-12
    minimum = min(p["variables"]["i_CB"] for p in releve.pas)
    publier(f"Bloc 8, marche de cible π*_0 = {100 * pi_0:g} % sur le sentier à 2 %, 36 pas "
            f"({ETIQUETTES})", [
                f"i_CB = i^règle au bit ; ∂i^règle/∂π* à l'impact {impact:.6f} ; identité de "
                f"BC2 {identite:.1e} ; taux directeur minimal sur les 36 pas {100 * minimum:.4f} % "
                f"par an"])


def _g_plan_reduit(nom, t):
    return 0.95 if nom == "G_plan" and t < 12 else 1.0


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_bornes_depense_reduite_prescription_exacte(socle, pi, publier):
    """Fiche 8, § 9.6, « Bornes », partie (b) : sous une dépense publique G^plan réduite de 5 %
    aux tours 1 à 12, le taux directeur égale exactement la prescription à chaque pas, sur 120
    pas, sans plancher ; aucun arrêt du noyau ; taux minimal publié."""
    sentier = socle.sentier(pi)
    _, releve = derouler(socle, sentier, 120, chocs_des_plans=_g_plan_reduit)
    assert all(p["variables"]["i_CB"] == p["variables"]["i_regle"] for p in releve.pas)
    minimum = min(p["variables"]["i_CB"] for p in releve.pas)
    publier(f"Bloc 8, G^plan −5 % aux tours 1 à 12, π* = {100 * pi:g} %, 120 pas "
            f"({ETIQUETTES})", [f"i_CB = i^règle au bit ; taux directeur minimal "
                                f"{100 * minimum:.6f} % par an"])


def test_taux_negatif_perte_versee_et_couverte_par_e1(socle, publier):
    """Fiche 8, § 9.6, « Bornes » (taux négatif) et partie (a) de « Perte » dans le moteur ; bloc
    d'essai 9, E1 (P95) : à π* = 0, r̂*_0 = −3 % donne une prescription négative ; i_CB l'égale
    exactement, sans plancher ; Π^CB < 0 ; la ligne 16 proposée et exécutée égale Π^CB, sans
    troncature, le bloc d'essai 9 en déclarant le montant couvert sur Π^CB lu en phase 1 ; la
    couverture intégrale (compte du Trésor suffisant) laisse E^CB inchangée, par le stock, à
    1e−12 × S^CB ; 12 pas, aucun arrêt du noyau. La couverture partielle et C60 relèvent du bloc
    9 (J3-d)."""
    sentier = socle.sentier(0.0)
    initial = dataclasses.replace(socle.etat_initial(sentier), r_hat_etoile=-0.03)
    _, releve = derouler(socle, sentier, 12, initial=initial)
    v = releve.pas[0]["variables"]
    assert v["i_CB"] == v["i_regle"] < 0.0
    assert v["Pi_CB"] < 0.0
    ouvertures = [initial] + [p["etat"] for p in releve.pas[:-1]]
    for o, p in zip(ouvertures, releve.pas):
        assert p["variables"]["i_CB"] == p["variables"]["i_regle"]
        assert p["16"] == p["variables"]["Pi_CB"]
        e_avant = idt.valeur_nette_stock(positions(o), "banque_centrale")
        e_apres = idt.valeur_nette_stock(positions(p["etat"]), "banque_centrale")
        assert abs(e_apres - e_avant) <= SEUIL_CB * echelle_cb(o)
    publier(f"Bloc 8, taux négatif (π* = 0, r̂*_0 = −3 %), 12 pas ({ETIQUETTES})", [
        f"i_CB = i^règle = {100 * v['i_CB']:.4f} % par an ; Π^CB = {v['Pi_CB']:.3e} u.m. ; "
        "ligne 16 exécutée = Π^CB (E1) ; E^CB inchangée"])


# --------------------------------------------------------------------------
# Phases : lecture hors ordre refusée à l'assemblage (partie (b))
# --------------------------------------------------------------------------


def _fautif(etape, lecture):
    """Bloc 8 réel dont le siège de `etape` déclare en plus `lecture`."""
    sieges = tuple(dataclasses.replace(s, lit=s.lit + (lecture,)) if s.etape == etape else s
                   for s in BanqueCentrale.declaration.sieges)
    declaration = dataclasses.replace(BanqueCentrale.declaration, sieges=sieges)
    return type("BanqueCentraleFautive", (BanqueCentrale,), {"__slots__": (),
                                                             "declaration": declaration})()


@pytest.mark.parametrize("etape, lecture, motif", [
    ("1", Lecture("1", "W_suivant"), "triangularité"),
    ("1", Lecture("5", "p"), "triangularité"),
    ("1", Lecture("4", "U_suivant"), "triangularité"),
])
def test_phases_lecture_hors_ordre_refusee(socle, etape, lecture, motif):
    """Fiche 8, § 9.6, « Phases », partie (b) : W_t (même groupe de la phase 1), p_t (phase 5) et
    U de la phase 4 ne sont pas lisibles en phase 1 ; une lecture déclarée hors ordre est refusée
    à l'assemblage (`DefautDeDeclaration`)."""
    sentier = socle.sentier(0.02)
    blocs = socle.blocs(sentier, reels=(Production(), Travail(), Prix(),
                                        _fautif(etape, lecture)))
    with pytest.raises(DefautDeDeclaration, match=motif):
        ordo.assembler(socle.PHASES, blocs, socle.parametres_du_sentier(sentier),
                       socle.SANS_ENTREES)
