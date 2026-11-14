"""Boucle T3 ↔ BC3 (P87), stationnarité partielle étendue (P94) et bloc d'essai 9 E3 (P95).

Rang 6 de J3-c (#91, #90). **Banc** (P87) : socle partiel d'essai, blocs 2, 3,
4, 7 et 8 réels, plans nominaux exogènes (blocs d'essai 5, 6 et 9) ; bloc
d'essai 9 avec E1, E2 et **E3** (émission selon E8 à E11, `emission_e3`, P95) ;
n_a = 12, ν_G = 1,15, π* ∈ {0 ; 2 % ; 10 %}. **Étiquette** de toute mesure :
`ETIQUETTE`. Aucune mesure ici ne vaut verdict de la boucle conjointe de la
fiche 8 (#114).

**Critères, écrits avant l'essai (P87, feuille de route § 4 ; compléments du
14/11/2026 en commentaire de la PR #129), non déplacés.** Chocs : π^e_0 ± 1
point injecté à l'ouverture (`etat_initial(choc_pi_e0=…)`), et G^plan × 1,01
aux tours 1 à 12 (pas 0 à 11, comme `test_banque_centrale.py`), chacun contre
un contrôle apparié sans choc, à chaque π*.

- **Communs** : π^e_1 − π^e_1,contrôle = (1 − c) Δ à 1e−15 et du signe de Δ
  (délai : π^e_1 ne lit que π_{−1}, inchangé) ; r̂*_T − r̂*_0 = (a_I/n_a) Σ(π_{t−1}
  − π*_t) à 1e−12 sur tout l'horizon ; π^e > −1 à chaque ouverture ; aucun
  arrêt du noyau.
- **Sur 720 pas** (λ_e = 0,2, valeur de la table) : V1, π^e_{t+1} = (1 − c) π^e_t
  + c π_{t−1}, implémentation de référence du test, à 1e−15 ; V2, délai de deux
  tours : si P diffère du contrôle pour la première fois au pas k, π^e
  d'ouverture ne s'écarte de (1 − c)^t Δ qu'au pas k + 2 (à 1e−15 jusqu'au pas
  k + 1 compris), lecture de `sec:banque_centrale` (« formée en phase 1 du tour
  n − 1 sur π_{n−2} ») ; V3, i_CB − i^règle = 0 exactement ; V4, Res L^CB = 0
  exactement à chaque clôture de pas ; V5, moyennes des pas 660 à 719 de B3
  (± 0,5 point), B7, B8, B9 et B25 (± 0,1 point) autour de leur valeur résolue
  (`tab:criteres-j3`) ; V6, max_{600 ≤ t < 720} |x| ≤ 0,1 max_{0 ≤ t < 720} |x|
  pour x1 = π^e − π^e_contrôle (ouverture), x2 = glissement sur 12 tours −
  glissement du contrôle, x3 = U − U_contrôle (fraction de N^pa), x4 =
  ln(p/p_contrôle).
- **De `macro`** : (a) signes, lecture écrite avant la mesure : sous Δ = ± 1
  point, W_0 (salaire écrit au pas 0) et p_0 s'écartent du contrôle du signe de
  Δ, et U − U_contrôle n'est jamais du signe opposé sur les 24 premiers pas et
  s'en écarte au moins une fois (canal : π^e → salaire → coût → prix ; plans
  nominaux exogènes, d'où volume demandé et emploi en baisse sous une hausse) ;
  (c) pour λ_e ∈ {0,1 ; 0,2 ; 0,4}, sur les pas 2 148 à 2 159 d'une fenêtre de
  2 160 pas, |π^e − π^e_contrôle| ≤ 1e−6, |U − U_contrôle| ≤ 1e−6 et
  |x/x_contrôle − 1| ≤ 1e−6 pour P, W et v^e ; (e) « non concluant (banc) » si
  le noyau s'arrête (`test_e_aucun_arret_du_noyau`).
- **Publiés sans verdict** : demi-vie, ratio de sacrifice (seuil à #114),
  asymétrie des deux chocs, r̂* − r̄. **Décisions du mainteneur du 14/11/2026**
  (rang 6 de J3-c) : le « ratio de sacrifice » devient le **coût en chômage
  d'un choc d'anticipations de ± 1 point** (D3, `ETIQUETTE_SANS_TAUX`), publié
  avec sa valeur analytique 1/(λ_e λ_w β (1 + π*)) ; r̂* − r̄ au pas 2 159 est
  publié aux trois λ_e comme **continuum propre au banc** (D2,
  `ETIQUETTE_CONTINUUM`). Contrôle prospectif de `macro`, sans déplacer (a) :
  ln(W_0/W_0,c) = ln((1 + π* + Δ)/(1 + π*))/n_a à 1e−15 (coefficient effectif de
  T3).

**P94** : B1 à B7, B12, B13, B24 (`grandeurs_b`), B8, B9, B16, B17, B18 (i),
B19, B20, B25, B26, D (`grandeurs_p94`, D = Div_Bk/Π^Bk, P77) et les états i_L,
i_D, r̂*, π^e, π*, sur le contrôle du banc, 720 pas, à 1e−9 relatif, une
grandeur de valeur résolue nulle à 1e−12 en valeur absolue (rapportée à S^CB
pour les grandeurs nulles de B19). **D1** (décision du mainteneur du
14/11/2026) : une grandeur est nulle si elle figure dans la liste déclarée
`socle.GRANDEURS_NULLES` et que sa valeur, calculée en arithmétique exacte sur
les tables de l'essai, est nulle ; jamais sur la valeur flottante du script.
"""

import dataclasses
import math
import types

import pytest

from nations.blocs.banque import Banque
from nations.blocs.banque_centrale import BanqueCentrale
from nations.blocs.prix import Prix
from nations.blocs.production import Production
from nations.blocs.travail import Travail
from nations.moteur.parametres import varier
from nations.moteur.parametres.cadre import PAS_PAR_AN
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.diagnostics import DefautComptable
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas

N_A = PAS_PAR_AN.valeur
ETIQUETTE = ("plans nominaux exogènes ; blocs 2, 3, 4, 7 et 8 réels ; bloc d'essai 9 avec E1 à "
             "E3")
CHOC = 0.01
# Horizons et fenêtres écrits avant l'essai (P87).
NB_PAS = 720
NB_PAS_LONG = 2160
FENETRE_V5 = range(660, 720)
DEBUT_V6 = 600
FENETRE_C = range(2148, 2160)
PAS_DES_SIGNES = 24
LAMBDAS = (0.1, 0.2, 0.4)
LAMBDA_DE_LA_TABLE = PARAMETRES_DE_REFERENCE.banque_centrale.lambda_e.valeur
# Seuils écrits avant l'essai (P87, P94).
SEUIL_BC3 = 1e-15
SEUIL_R_HAT = 1e-12
DEMI_BANDE_B3 = 0.005
DEMI_BANDE = 0.001
RAPPORT_V6 = 0.1
SEUIL_C = 1e-6
SEUIL_P94 = 1e-9
SEUIL_NUL = 1e-12
# Seuil de `tab:criteres-j3` pour B17 et B18 (i), publié à côté de P94 (constat m5 de l'audit).
SEUIL_TAB_CRITERES_J3 = 1e-12
# Ancien classement des grandeurs nulles (|x̄| ≤ 1e−12), remplacé par D1 ; gardé pour la
# vérification que le classement exact ne change aucun verdict.
SEUIL_DU_CLASSEMENT_FLOTTANT = 1e-12
# Contrôle prospectif de `macro` sur le coefficient effectif de T3 (item 7 du rang 6).
SEUIL_T3 = 1e-15
ETIQUETTE_SANS_TAUX = "banc sans canal du taux"
ETIQUETTE_CONTINUUM = ("continuum propre au banc (exigences.md § 2.7), terme de Jensen de BC2, "
                       "banc sans canal du taux ; issue #131")
CHOCS = {"π^e_0 + 1 point": (CHOC, False), "π^e_0 − 1 point": (-CHOC, False),
         "G^plan × 1,01 aux tours 1 à 12": (0.0, True)}
CHOCS_DE_PI_E = ("π^e_0 + 1 point", "π^e_0 − 1 point")
CONTROLE = "contrôle"


def reels():
    return (Production(), Travail(), Prix(), Banque(), BanqueCentrale())


def _g_plan_accru(nom, t):
    return 1.01 if nom == "G_plan" and t < 12 else 1.0


def parametres(pi, lambda_e):
    """Tables de référence, table du bloc 8 à π* = π̄ du sentier et λ_e = `lambda_e` (R1)."""
    p = PARAMETRES_DE_REFERENCE
    return dataclasses.replace(p, banque_centrale=varier(p.banque_centrale, pi_etoile=pi,
                                                         lambda_e=lambda_e))


def ordonnanceur(socle, sentier, lambda_e, choc_g=False):
    options = socle.emission_e3()
    if choc_g:
        options["chocs_des_plans"] = _g_plan_accru
    return socle.ordonnanceur(sentier, parametres(sentier.pi, lambda_e), reels=reels(),
                              **options)


class Serie:
    """Observateur d'essai compact : par pas t, grandeurs de l'état t + 1 et variables du pas."""

    ETAT = ("pi_e", "U", "W", "v_e", "r_hat_etoile", "pi_etoile", "Res", "L_CB")
    PAS = ("p", "P", "i_CB", "i_regle", "y")

    def __init__(self):
        self.valeurs = {nom: [] for nom in self.ETAT + self.PAS + ("glissement",)}

    def relever(self, e):
        if type(e) is FinDePas:
            for nom in self.ETAT:
                self.valeurs[nom].append(getattr(e.etat, nom))
            variables = dict(e.variables_du_pas)
            for nom in self.PAS:
                self.valeurs[nom].append(variables[nom])
            registre = e.etat.registre_prix
            # Glissement du pas t, P_t/P_{t−12} − 1, lu au registre de l'état t + 1 ; c'est π_t
            # que lit BC3 au pas t + 1.
            self.valeurs["glissement"].append(registre[0] / registre[N_A] - 1.0)


@dataclasses.dataclass
class Essai:
    initial: object
    serie: Serie
    arret: str | None

    def __getitem__(self, nom):
        return self.serie.valeurs[nom]

    def ouverture_pi_e(self):
        """π^e d'ouverture des pas 0 à T − 1."""
        return [self.initial.pi_e] + self["pi_e"][:-1]

    def pi_prec(self):
        """π_{t−1} lu par BC3 au pas t (glissement du registre d'ouverture)."""
        r = self.initial.registre_prix
        return [r[0] / r[N_A] - 1.0] + self["glissement"][:-1]


def executer(socle, pi, lambda_e, nb_pas, choc_pi_e0=0.0, choc_g=False):
    """Un essai du banc ; un arrêt du noyau est relevé (P87 (e)), non propagé."""
    sentier = socle.sentier(pi)
    initial = socle.etat_initial(sentier, choc_pi_e0=choc_pi_e0)
    serie = Serie()
    try:
        socle.derouler(initial, nb_pas, ordonnanceur(socle, sentier, lambda_e, choc_g), serie)
        arret = None
    except DefautComptable as defaut:
        arret = f"pas {len(serie.valeurs['U'])} : {defaut}"
    return Essai(initial, serie, arret)


@pytest.fixture(scope="module")
def bancs(socle):
    """(π*, λ_e, essai) → Essai : contrôle et chocs ± 1 point de π^e_0 sur 2 160 pas à chaque λ_e
    de (c) ; choc de G^plan sur 720 pas à λ_e de la table. Les critères de 720 pas lisent les
    720 premiers pas des essais de 2 160 pas à λ_e = 0,2 (même trajectoire, déterministe)."""
    rendus = {}
    for pi in socle.POINTS_PI:
        for lam in LAMBDAS:
            rendus[pi, lam, CONTROLE] = executer(socle, pi, lam, NB_PAS_LONG)
            for nom in CHOCS_DE_PI_E:
                rendus[pi, lam, nom] = executer(socle, pi, lam, NB_PAS_LONG,
                                                choc_pi_e0=CHOCS[nom][0])
        rendus[pi, LAMBDA_DE_LA_TABLE, "G^plan × 1,01 aux tours 1 à 12"] = executer(
            socle, pi, LAMBDA_DE_LA_TABLE, NB_PAS, choc_g=True)
    return rendus


def _concluant(essai):
    if essai.arret is not None:
        pytest.skip(f"non concluant (banc), P87 (e) : arrêt du noyau, {essai.arret}")


def ecarts_au_controle(essai, controle, nb_pas=NB_PAS):
    """x1 à x4 de V6 sur les pas 0 à `nb_pas` − 1 (compléments du 14/11/2026 à P87)."""
    x1 = [a - b for a, b in zip(essai.ouverture_pi_e()[:nb_pas],
                                controle.ouverture_pi_e()[:nb_pas])]
    x2 = [a - b for a, b in zip(essai["glissement"][:nb_pas], controle["glissement"][:nb_pas])]
    x3 = [a - b for a, b in zip(essai["U"][:nb_pas], controle["U"][:nb_pas])]
    x4 = [math.log(a / b) for a, b in zip(essai["p"][:nb_pas], controle["p"][:nb_pas])]
    return {"x1 (π^e)": x1, "x2 (glissement)": x2, "x3 (U)": x3, "x4 (ln p)": x4}


# --------------------------------------------------------------------------
# (e) et communs
# --------------------------------------------------------------------------


def test_e_aucun_arret_du_noyau(bancs, publier):
    """P87, communs et (e) : aucun arrêt du noyau sur aucun essai du banc ; sinon, verdict
    « non concluant (banc) », publié avec le pas et le diagnostic."""
    arrets = {cle: e.arret for cle, e in bancs.items() if e.arret is not None}
    verdict = "non concluant (banc)" if arrets else "aucun arrêt"
    publier(f"Boucle T3 ↔ BC3 (P87), (e), {len(bancs)} essais ({ETIQUETTE})", [
        f"verdict : {verdict}"] + [f"{cle} : {a}" for cle, a in arrets.items()])
    assert not arrets, f"non concluant (banc), P87 (e) : {arrets}"


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_communs_delai_signe_identite_de_r_hat_et_domaine(bancs, pi, publier):
    """P87, communs : π^e_1 − π^e_1,contrôle = (1 − c) Δ à 1e−15, du signe de Δ (nul sous le
    choc de G^plan) ; r̂*_T − r̂*_0 = (a_I/n_a) Σ(π_{t−1} − π*_t) à 1e−12 sur tout l'horizon de
    chaque essai ; π^e > −1 à chaque ouverture."""
    a_I = PARAMETRES_DE_REFERENCE.banque_centrale.a_I.valeur
    pire_delai, pire_identite = 0.0, 0.0
    for (p, lam, nom), essai in bancs.items():
        if p != pi:
            continue
        _concluant(essai)
        controle = bancs[pi, lam, CONTROLE]
        delta = CHOCS[nom][0] if nom != CONTROLE else 0.0
        c = lam / N_A
        ecart_1 = essai["pi_e"][0] - controle["pi_e"][0]
        pire_delai = max(pire_delai, abs(ecart_1 - (1.0 - c) * delta))
        assert abs(ecart_1 - (1.0 - c) * delta) <= SEUIL_BC3, (lam, nom)
        if delta == 0.0:
            assert ecart_1 == 0.0, (lam, nom)
        else:
            assert math.copysign(1.0, ecart_1) == math.copysign(1.0, delta), (lam, nom)
        ouvertures_pi_etoile = [essai.initial.pi_etoile] + essai["pi_etoile"][:-1]
        somme = sum(x - y for x, y in zip(essai.pi_prec(), ouvertures_pi_etoile))
        identite = abs(essai["r_hat_etoile"][-1] - essai.initial.r_hat_etoile
                       - a_I / N_A * somme)
        pire_identite = max(pire_identite, identite)
        assert identite <= SEUIL_R_HAT, (lam, nom, identite)
        assert min(essai.ouverture_pi_e() + essai["pi_e"][-1:]) > -1.0
    publier(f"Boucle T3 ↔ BC3 (P87), communs, π* = {100 * pi:g} % ({ETIQUETTE})", [
        f"max |π^e_1 − π^e_1,contrôle − (1 − c) Δ| = {pire_delai:.1e} (seuil 1e−15), signe de Δ ; "
        f"max |r̂*_T − r̂*_0 − (a_I/n_a) Σ(π_{{t−1}} − π*)| = {pire_identite:.1e} (seuil 1e−12) ; "
        "π^e > −1 à chaque ouverture"])


# --------------------------------------------------------------------------
# V1 à V6 (720 pas, λ_e de la table)
# --------------------------------------------------------------------------


def _essais_720(bancs, pi, avec_controle=False):
    noms = tuple(CHOCS) + ((CONTROLE,) if avec_controle else ())
    return {nom: bancs[pi, LAMBDA_DE_LA_TABLE, nom] for nom in noms}


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_v1_bc3_egale_une_implementation_de_reference(bancs, pi):
    """V1 : à chaque pas des 720, π^e_{t+1} = (1 − c) π^e_t + c π_{t−1}, c = λ_e/12, recalculé par
    le test sur l'ouverture et le registre, à 1e−15, contrôle compris."""
    c = LAMBDA_DE_LA_TABLE / 12
    for nom, essai in _essais_720(bancs, pi, avec_controle=True).items():
        _concluant(essai)
        triplets = zip(essai.ouverture_pi_e(), essai.pi_prec(), essai["pi_e"])
        for t, (pi_e, pi_prec, suivant) in enumerate(list(triplets)[:NB_PAS]):
            assert abs(suivant - ((1.0 - c) * pi_e + c * pi_prec)) <= SEUIL_BC3, (nom, t)


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_v2_delai_de_deux_tours(bancs, pi, publier):
    """V2 : k, premier pas où P_t diffère du contrôle ; π^e d'ouverture − contrôle égale
    (1 − c)^t Δ à 1e−15 aux pas 0 à k + 1 et s'en écarte au pas k + 2 (prix au pas k → π^e
    formée en phase 1 du pas k + 1 → consommée au pas k + 2)."""
    c = LAMBDA_DE_LA_TABLE / 12
    lignes = []
    for nom, essai in _essais_720(bancs, pi).items():
        _concluant(essai)
        controle = bancs[pi, LAMBDA_DE_LA_TABLE, CONTROLE]
        delta = CHOCS[nom][0]
        k = next(t for t, (a, b) in enumerate(zip(essai["P"], controle["P"])) if a != b)
        residus = [a - b - (1.0 - c) ** t * delta for t, (a, b) in enumerate(
            zip(essai.ouverture_pi_e(), controle.ouverture_pi_e()))]
        assert max(abs(r) for r in residus[:k + 2]) <= SEUIL_BC3, nom
        assert abs(residus[k + 2]) > SEUIL_BC3, nom
        lignes.append(f"{nom} : P s'écarte au pas {k}, π^e d'ouverture au pas {k + 2} "
                      f"(résidu {residus[k + 2]:.2e})")
    publier(f"Boucle T3 ↔ BC3 (P87), V2, π* = {100 * pi:g} % ({ETIQUETTE})", lignes)


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_v3_v4_prescription_et_reserves_exactes(bancs, pi):
    """V3 : i_CB − i^règle = 0 exactement à chaque pas ; V4 : Res L^CB = 0 exactement à chaque
    clôture de pas (Res ≥ 0, L^CB ≥ 0) ; 720 pas, chocs et contrôle."""
    for nom, essai in _essais_720(bancs, pi, avec_controle=True).items():
        _concluant(essai)
        assert all(a - b == 0.0 for a, b in zip(essai["i_CB"][:NB_PAS], essai["i_regle"][:NB_PAS]))
        for res, l_cb in zip(essai["Res"][:NB_PAS], essai["L_CB"][:NB_PAS]):
            assert res >= 0.0 and l_cb >= 0.0 and res * l_cb == 0.0, nom


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_v5_moyennes_des_pas_660_a_719_dans_les_bandes(bancs, socle, pi, publier):
    """V5 : moyennes des pas 660 à 719 de chaque essai choqué dans les bandes de `tab:criteres-j3`
    autour de la valeur résolue du script : B3 (U, fraction de N^pa) ± 0,5 point ; B7 (glissement)
    ; B8 (π^e − π*) ; B9 (i_CB − π, π de B7) ; B25 (r̂* − r̄), ± 0,1 point."""
    sentier = socle.sentier(pi)
    resolues = socle.valeurs_resolues(sentier)
    centres = {"B3": (resolues["B3"], DEMI_BANDE_B3), "B7": (resolues["B7"], DEMI_BANDE),
               "B8": (0.0, DEMI_BANDE), "B9": (sentier.e["i_CB"] - pi, DEMI_BANDE),
               "B25": (0.0, DEMI_BANDE)}
    lignes = []
    for nom, essai in _essais_720(bancs, pi).items():
        _concluant(essai)
        fenetre = list(FENETRE_V5)
        serie = {"B3": [essai["U"][t] for t in fenetre],
                 "B7": [essai["glissement"][t] for t in fenetre],
                 "B8": [essai["pi_e"][t] - essai["pi_etoile"][t] for t in fenetre],
                 "B9": [essai["i_CB"][t] - essai["glissement"][t] for t in fenetre],
                 "B25": [essai["r_hat_etoile"][t] - sentier.par.rbar for t in fenetre]}
        ecarts = {}
        for cle, (centre, demi) in centres.items():
            ecarts[cle] = sum(serie[cle]) / len(fenetre) - centre
            assert abs(ecarts[cle]) <= demi, (nom, cle, ecarts[cle])
        lignes.append(f"{nom} : écart de la moyenne au centre, en point : " + " ; ".join(
            f"{c} {100 * x:+.2e}" for c, x in ecarts.items()))
    publier(f"Boucle T3 ↔ BC3 (P87), V5, π* = {100 * pi:g} %, pas 660 à 719 ({ETIQUETTE})",
            lignes + ["demi-bandes : B3 0,5 point ; B7, B8, B9, B25 0,1 point"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_v6_decroissance_des_ecarts_au_controle(bancs, pi, publier):
    """V6 : max_{600 ≤ t < 720} |x| ≤ 0,1 × max_{0 ≤ t < 720} |x| pour x1 à x4, écarts au contrôle
    apparié."""
    lignes = []
    for nom, essai in _essais_720(bancs, pi).items():
        _concluant(essai)
        controle = bancs[pi, LAMBDA_DE_LA_TABLE, CONTROLE]
        rapports = {}
        for x, serie in ecarts_au_controle(essai, controle).items():
            maximum = max(abs(v) for v in serie)
            fin = max(abs(v) for v in serie[DEBUT_V6:NB_PAS])
            assert maximum > 0.0, (nom, x)
            rapports[x] = fin / maximum
            assert fin <= RAPPORT_V6 * maximum, (nom, x, fin, maximum)
        lignes.append(f"{nom} : max_[600, 720) |x| / max |x| : " + " ; ".join(
            f"{x} {r:.2e}" for x, r in rapports.items()))
    publier(f"Boucle T3 ↔ BC3 (P87), V6, π* = {100 * pi:g} % ({ETIQUETTE})",
            lignes + ["seuil 0,1"])


# --------------------------------------------------------------------------
# (a) signes et (c) arrivée indépendante de la vitesse (`macro`)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_a_signes_de_w0_p0_et_u(bancs, pi, publier):
    """(a), lecture écrite avant la mesure (docstring du module) : sous Δ = ± 1 point de π^e_0,
    W_0 − W_0,contrôle et p_0 − p_0,contrôle du signe de Δ ; U − U_contrôle jamais du signe opposé
    sur les pas 0 à 23, et non nul au moins une fois."""
    lignes = []
    for nom in CHOCS_DE_PI_E:
        essai = bancs[pi, LAMBDA_DE_LA_TABLE, nom]
        _concluant(essai)
        controle = bancs[pi, LAMBDA_DE_LA_TABLE, CONTROLE]
        signe = math.copysign(1.0, CHOCS[nom][0])
        d_w = essai["W"][0] / controle["W"][0] - 1.0
        d_p = essai["p"][0] / controle["p"][0] - 1.0
        d_u = [a - b for a, b in zip(essai["U"][:PAS_DES_SIGNES], controle["U"][:PAS_DES_SIGNES])]
        assert d_w * signe > 0.0 and d_p * signe > 0.0, nom
        assert all(x * signe >= 0.0 for x in d_u) and any(x != 0.0 for x in d_u), nom
        premier = next(t for t, x in enumerate(d_u) if x != 0.0)
        lignes.append(f"{nom} : W_0/W_0,c − 1 = {d_w:+.3e} ; p_0/p_0,c − 1 = {d_p:+.3e} ; U − U_c "
                      f"du signe de Δ dès le pas {premier}, extrême {max(d_u, key=abs):+.3e} "
                      "(fraction de N^pa)")
    publier(f"Boucle T3 ↔ BC3 (P87), (a) signes, π* = {100 * pi:g} % ({ETIQUETTE})", lignes)


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_c_arrivee_independante_de_la_vitesse(bancs, pi, publier):
    """(c) (`docs/exigences.md` § 2.7) : pour λ_e ∈ {0,1 ; 0,2 ; 0,4}, sur les pas 2 148 à 2 159
    de 2 160 pas, chaque choc de π^e_0 revient au contrôle apparié de même λ_e : |π^e − π^e_c|
    ≤ 1e−6 par an, |U − U_c| ≤ 1e−6 (fraction de N^pa), |x/x_c − 1| ≤ 1e−6 pour P, W et v^e."""
    lignes = []
    for lam in LAMBDAS:
        controle = bancs[pi, lam, CONTROLE]
        _concluant(controle)
        for nom in CHOCS_DE_PI_E:
            essai = bancs[pi, lam, nom]
            _concluant(essai)
            ecarts = {
                "π^e": max(abs(essai["pi_e"][t] - controle["pi_e"][t]) for t in FENETRE_C),
                "U": max(abs(essai["U"][t] - controle["U"][t]) for t in FENETRE_C)}
            for x in ("P", "W", "v_e"):
                ecarts[x] = max(abs(essai[x][t] / controle[x][t] - 1.0) for t in FENETRE_C)
            for x, e in ecarts.items():
                assert e <= SEUIL_C, (lam, nom, x, e)
            lignes.append(f"λ_e = {lam:g}, {nom} : " + " ; ".join(
                f"{x} {e:.1e}" for x, e in ecarts.items()))
    publier(f"Boucle T3 ↔ BC3 (P87), (c), π* = {100 * pi:g} %, pas 2 148 à 2 159 ({ETIQUETTE})",
            lignes + ["seuil 1e−6"])


# --------------------------------------------------------------------------
# Publiés sans verdict : demi-vie, ratio de sacrifice, asymétrie, r̂* − r̄
# --------------------------------------------------------------------------


def demi_vie_lente(serie, debut=360, fin=600):
    """Demi-vie, en pas, de la racine lente, tirée de la pente de ln |x| entre les pas `debut` et
    `fin` ; « non définie » si x change de signe ou s'annule sur la fenêtre."""
    fenetre = serie[debut:fin + 1]
    if any(v == 0.0 for v in fenetre) or len({math.copysign(1.0, v) for v in fenetre}) > 1:
        return None
    pente = (math.log(abs(serie[fin])) - math.log(abs(serie[debut]))) / (fin - debut)
    return math.log(0.5) / pente if pente < 0.0 else None


def demi_vie_au_seuil(serie):
    """Premier pas à partir duquel |x| reste sous la moitié de son maximum."""
    seuil = 0.5 * max(abs(v) for v in serie)
    dernier = max((t for t, v in enumerate(serie) if abs(v) > seuil), default=-1)
    return dernier + 1


def test_publies_sans_verdict(bancs, socle, publier):
    """P87, publiés sans verdict (aucune assertion de seuil) : demi-vie (x1 et x3 ; racine lente
    par la pente de ln |x| sur les pas 360 à 600, et premier pas sous la moitié du maximum) ;
    asymétrie entre + 1 et − 1 point (rapport des pics de |x| et max |x_+ + x_−| / max |x_+|) ;
    r̂* − r̄ en fin de fenêtre (pas 719 et 2 159), choc et contrôle. Le « ratio de sacrifice »
    de P87 est publié sous son nom de D3 par
    `test_publie_cout_en_chomage_d_un_choc_d_anticipations`."""
    lam = LAMBDA_DE_LA_TABLE
    for pi in socle.POINTS_PI:
        controle = bancs[pi, lam, CONTROLE]
        _concluant(controle)
        r_bar = socle.sentier(pi).par.rbar
        lignes = []
        ecarts = {}
        for nom in CHOCS:
            essai = bancs[pi, lam, nom]
            _concluant(essai)
            ecarts[nom] = ecarts_au_controle(essai, controle)
            demi = []
            for x in ("x1 (π^e)", "x3 (U)"):
                lente = demi_vie_lente(ecarts[nom][x])
                texte = "non définie" if lente is None else f"{lente:.1f} pas"
                demi.append(f"{x} : racine lente {texte}, sous la moitié du pic dès le pas "
                            f"{demi_vie_au_seuil(ecarts[nom][x])}")
            lignes.append(f"{nom}, demi-vie : " + " ; ".join(demi))
            fins = [f"pas 719 : {100 * (essai['r_hat_etoile'][NB_PAS - 1] - r_bar):+.3e} point"]
            if len(essai["r_hat_etoile"]) == NB_PAS_LONG:
                fins.append(f"pas 2 159 : {100 * (essai['r_hat_etoile'][-1] - r_bar):+.3e} point")
            lignes.append(f"{nom}, r̂* − r̄ : " + " ; ".join(fins))
        asym = []
        for x in ("x2 (glissement)", "x3 (U)", "x4 (ln p)"):
            p, m = ecarts["π^e_0 + 1 point"][x], ecarts["π^e_0 − 1 point"][x]
            pic_p, pic_m = max(abs(v) for v in p), max(abs(v) for v in m)
            somme = max(abs(a + b) for a, b in zip(p, m))
            asym.append(f"{x} : pic + / pic − = {pic_p / pic_m:.4f}, max |x_+ + x_−| / pic + = "
                        f"{somme / pic_p:.3e}")
        lignes.append("asymétrie ± 1 point : " + " ; ".join(asym))
        r_c = controle["r_hat_etoile"]
        lignes.append(f"contrôle, r̂* − r̄ : pas 719 {100 * (r_c[NB_PAS - 1] - r_bar):+.3e} "
                      f"point ; pas 2 159 {100 * (r_c[-1] - r_bar):+.3e} point")
        publier(f"Boucle T3 ↔ BC3 (P87), publiés sans verdict, π* = {100 * pi:g} %, λ_e = "
                f"{lam:g} ({ETIQUETTE})", lignes)


def cout_en_chomage(essai, controle, delta, nb_pas):
    """D3 : coût en chômage d'un choc d'anticipations, Σ_{t<nb_pas} (U − U_c)/n_a rapporté au
    choc Δ de π^e_0, en années-point de chômage par point de π^e_0 (U en fraction de N^pa) ; et
    variante en production, Σ_{t<nb_pas} (1 − y/y_c)/n_a rapporté à Δ, en années-point de
    production réalisée N5 par point. Écarts au contrôle apparié."""
    s_u = sum(a - b for a, b in zip(essai["U"][:nb_pas], controle["U"][:nb_pas])) / N_A
    s_y = sum(1.0 - a / b for a, b in zip(essai["y"][:nb_pas], controle["y"][:nb_pas])) / N_A
    return s_u / delta, s_y / delta


def cout_analytique(pi, lambda_e):
    """D3 : valeur analytique 1/(λ_e λ_w β (1 + π*)), λ_w et β lus dans la table du bloc 3."""
    travail = PARAMETRES_DE_REFERENCE.travail
    return 1.0 / (lambda_e * travail.lambda_w.valeur * travail.beta * (1.0 + pi))


def test_publie_cout_en_chomage_d_un_choc_d_anticipations(bancs, socle, publier):
    """D3 (décision du mainteneur du 14/11/2026), publié sans verdict ni seuil : coût en chômage
    d'un choc d'anticipations de ± 1 point (ex-« ratio de sacrifice » de P87), années-point de
    chômage par point de π^e_0, écart au contrôle apparié, aux trois λ_e et aux trois π*, sur
    720 pas, et sur 2 160 pas à λ_e = 0,1 (troncature) ; valeur analytique
    1/(λ_e λ_w β (1 + π*)) à côté ; variante en production réalisée N5."""
    for pi in socle.POINTS_PI:
        lignes = []
        for lam in LAMBDAS:
            controle = bancs[pi, lam, CONTROLE]
            _concluant(controle)
            horizons = (NB_PAS, NB_PAS_LONG) if lam == min(LAMBDAS) else (NB_PAS,)
            for nb_pas in horizons:
                chomage, production = {}, {}
                for nom in CHOCS_DE_PI_E:
                    essai = bancs[pi, lam, nom]
                    _concluant(essai)
                    chomage[nom], production[nom] = cout_en_chomage(essai, controle,
                                                                    CHOCS[nom][0], nb_pas)
                moyenne = sum(chomage.values()) / len(chomage)
                lignes.append(
                    f"λ_e = {lam:g}, {nb_pas} pas : chômage + 1 → "
                    f"{chomage['π^e_0 + 1 point']:.4f}, − 1 → {chomage['π^e_0 − 1 point']:.4f}, "
                    f"moyenne {moyenne:.4f} ; analytique 1/(λ_e λ_w β (1 + π*)) = "
                    f"{cout_analytique(pi, lam):.4f} ; variante en production réalisée N5 "
                    f"(1 − y/y_c) : + 1 → {production['π^e_0 + 1 point']:.4f}, − 1 → "
                    f"{production['π^e_0 − 1 point']:.4f}")
        publier(f"Coût en chômage d'un choc d'anticipations de ± 1 point (D3), années-point de "
                f"chômage par point de π^e_0, écart au contrôle apparié, π* = {100 * pi:g} % "
                f"({ETIQUETTE_SANS_TAUX} ; {ETIQUETTE})",
                lignes + ["sans seuil ; 720 pas tronquent la queue à λ_e = 0,1"])


def test_publie_continuum_de_r_hat(bancs, socle, publier):
    """D2 (décision du mainteneur du 14/11/2026), publié sans verdict : r̂* − r̄ au pas 2 159, en
    point, pour λ_e ∈ {0,1 ; 0,2 ; 0,4} et les chocs ± 1 point de π^e_0, aux trois π*."""
    for pi in socle.POINTS_PI:
        r_bar = socle.sentier(pi).par.rbar
        lignes = []
        for lam in LAMBDAS:
            valeurs = []
            for nom in CHOCS_DE_PI_E:
                essai = bancs[pi, lam, nom]
                _concluant(essai)
                assert len(essai["r_hat_etoile"]) == NB_PAS_LONG
                valeurs.append(f"{nom} : {100 * (essai['r_hat_etoile'][-1] - r_bar):+.4e} point")
            lignes.append(f"λ_e = {lam:g} : " + " ; ".join(valeurs))
        publier(f"r̂* − r̄ au pas 2 159 (D2), π* = {100 * pi:g} % ({ETIQUETTE_CONTINUUM} ; "
                f"{ETIQUETTE})", lignes + ["sans verdict"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_controle_prospectif_du_coefficient_de_t3(bancs, pi, publier):
    """Proposition de `macro` (rang 6 de J3-c), contrôle prospectif qui ne déplace pas le
    critère (a) : sous Δ = ± 1 point de π^e_0, seul le terme ln(1 + π^e_0)/n_a de T3 diffère au
    pas 0 (W_{−1}, ω_{−1} et U_{−1} sont ceux du contrôle), d'où ln(W_0/W_0,c) =
    ln((1 + π* + Δ)/(1 + π*))/n_a à 1e−15 : coefficient effectif 1/n_a de π^e dans T3."""
    lignes = []
    for nom in CHOCS_DE_PI_E:
        essai = bancs[pi, LAMBDA_DE_LA_TABLE, nom]
        _concluant(essai)
        controle = bancs[pi, LAMBDA_DE_LA_TABLE, CONTROLE]
        delta = CHOCS[nom][0]
        mesure = math.log(essai["W"][0] / controle["W"][0])
        attendue = math.log((1.0 + pi + delta) / (1.0 + pi)) / N_A
        assert abs(mesure - attendue) <= SEUIL_T3, (nom, mesure, attendue)
        lignes.append(f"{nom} : ln(W_0/W_0,c) = {mesure:+.6e}, attendu {attendue:+.6e}, "
                      f"écart {abs(mesure - attendue):.1e} (seuil 1e−15)")
    publier(f"Boucle T3 ↔ BC3, contrôle prospectif du coefficient de T3, π* = {100 * pi:g} % "
            f"({ETIQUETTE})", lignes)


# --------------------------------------------------------------------------
# Bloc d'essai 9, E3 (P95)
# --------------------------------------------------------------------------


class ReleveE3:
    """Observateur d'essai : par pas, montants exécutés des lignes lues et proposées par E3,
    variables du pas et état t + 1."""

    LIGNES = ("2", "6", "7", "11a", "11b", "11c", "19a-ménages", "19a-banque", "19a-BC")

    def __init__(self):
        self.pas = []
        self._montants = {}

    def relever(self, e):
        if type(e) is ClotureDePhase:
            for ligne, termes in e.montants:
                if ligne in self.LIGNES:
                    self._montants[ligne] = sum(x for _, x in termes)
        elif type(e) is FinDePas:
            self.pas.append({**self._montants, "variables": dict(e.variables_du_pas),
                             "etat": e.etat})
            self._montants = {}


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
@pytest.mark.parametrize("choc", ["π^e_0 + 1 point", "G^plan × 1,01 aux tours 1 à 12"])
def test_e3_emission_selon_e8_a_e11(socle, pi, choc, publier):
    """E3 (P95), sur 36 pas sous choc : les lignes 19a exécutées égalent E10 et E11 recalculées
    par le test sur les lignes 2, 6, 7 et 11a à 11c exécutées, Π^CB et θ_CB du pas et M^G
    d'ouverture (au bit, même ordre d'opérations) ; ligne 19a-ménages nulle ; et le compte du
    Trésor de clôture vaut M^G*_t = ν_G PB_t à 1e−12 × S^G (`sec:finances_publiques-emission` :
    « après son versement en phase 8 (b), le compte du Trésor vaut M^G*_t »)."""
    delta, choc_g = CHOCS[choc]
    sentier = socle.sentier(pi)
    initial = socle.etat_initial(sentier, choc_pi_e0=delta)
    releve = ReleveE3()
    socle.derouler(initial, 36, ordonnanceur(socle, sentier, LAMBDA_DE_LA_TABLE, choc_g), releve)
    nu_g, varsigma = sentier.par.nu_G, sentier.par.varsigma_B
    ouvertures = [initial] + [p["etat"] for p in releve.pas[:-1]]
    pire = 0.0
    for o, p in zip(ouvertures, releve.pas):
        v = p["variables"]
        pb = p["2"] + p["6"] + (p["11a"] + p["11b"] + p["11c"])
        visee = nu_g * pb
        besoin = pb - p["7"] - v["Pi_CB"] + visee - o.M_G
        part_cb = v["theta_CB"] * besoin
        assert p["19a-BC"].hex() == part_cb.hex()
        assert p["19a-banque"].hex() == ((1.0 - varsigma) * (besoin - part_cb)).hex()
        assert p["19a-ménages"] == 0.0
        e = p["etat"]
        s_g = idt.echelle_bilan({q: getattr(e, q) for q in cat.NOMS_POSTES}, "etat")
        pire = max(pire, abs(e.M_G - visee) / s_g)
    assert pire <= SEUIL_NUL
    publier(f"Bloc d'essai 9, E3, {choc}, π* = {100 * pi:g} %, 36 pas ({ETIQUETTE})", [
        f"lignes 19a = E10, E11 au bit ; max |M^G_{{t+1}} − ν_G PB_t|/S^G = {pire:.1e} "
        "(seuil 1e−12)"])


def _vue_de_souscription(sentier, theta_cb):
    """Vue d'essai des fonctions de souscription d'E3 : lignes 2, 6, 7 et 11a à 11c exécutées
    (montants du pas 0 du sentier, dépense accrue de 1 % pour que Em ≠ Em du sentier), Π^CB et
    θ_CB du pas (θ_CB = `theta_cb`) et M^G d'ouverture."""
    s, o = sentier.s, sentier.o
    i_pas = s["i_CB"] / N_A
    montants = {"2": 1.01 * s["G"], "6": s["Tr"], "7": s["T_H"] + s["T_F"],
                "11a": i_pas * o["B_H"], "11b": i_pas * o["B_Bk"], "11c": i_pas * o["B_CB"]}
    pas = {"Pi_CB": s["Pi_CB"], "theta_CB": theta_cb}
    return types.SimpleNamespace(
        grand_livre=types.SimpleNamespace(montant_execute_ligne=montants.__getitem__),
        lire=pas.__getitem__, ouverture=types.SimpleNamespace(M_G=o["M_G"])), montants, pas


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_e3_souscriptions_hors_du_socle(socle, pi):
    """Constat m1 de l'audit du rang 6 : au socle, θ_CB = 0 et ς_B = 0 laissent survivre une
    mutation « E11 sans la part de la banque centrale ». Appel direct des fonctions de
    souscription d'E3 sur une vue d'essai, θ_CB,t = 0,3 lu en phase 1 (la table garde θ_CB = 0)
    et ς_B = 0,2 : E10, 19a-BC = θ_CB,t Em_t et 19a-ménages = 0 ; E11, 19a-banque =
    (1 − ς_B)(Em_t − 19a-BC), dans l'ordre C25 (besoin, part de la banque centrale, reliquat),
    contre une forme recalculée par le test, à 1e−15 × |Em_t|."""
    theta_cb, varsigma = 0.3, 0.2
    base = socle.sentier(pi)
    sentier = dataclasses.replace(base, par=dataclasses.replace(base.par, varsigma_B=varsigma))
    vue, m, pas = _vue_de_souscription(sentier, theta_cb)
    pb = m["2"] + m["6"] + m["11a"] + m["11b"] + m["11c"]
    em = pb - m["7"] - pas["Pi_CB"] + sentier.par.nu_G * pb - base.o["M_G"]
    part_cb = theta_cb * em
    reliquat = em - part_cb
    attendus = {"19a-BC": part_cb, "19a-ménages": 0.0, "19a-banque": (1.0 - varsigma) * reliquat}
    rendus = {"19a-BC": socle._souscription_banque_centrale(vue, sentier)["Delta_BCB_prim"],
              "19a-ménages": socle._souscription_menages(vue, sentier)["Delta_BH_prim"],
              "19a-banque": socle._souscription_banque(vue, sentier)["Delta_BBk_prim"]}
    assert em > 0.0 and base.par.theta_CB == 0.0
    for ligne, attendu in attendus.items():
        assert abs(rendus[ligne] - attendu) <= 1e-15 * abs(em), (ligne, rendus[ligne], attendu)
    # Part non souscrite ς_B (Em − θ_CB Em), sans souscription des ménages (M27).
    non_souscrit = em - sum(rendus.values())
    assert abs(non_souscrit - varsigma * (1.0 - theta_cb) * em) <= 1e-15 * abs(em)


def test_options_sans_bloc_d_essai_refusees(socle):
    """Constat m3 de l'audit du rang 6 : une règle d'essai de ligne dont le proposant est
    remplacé par un bloc réel, une ligne qu'aucun siège ne propose, ou une déclaration d'un
    radical remplacé par un bloc réel, est refusée par une exception, jamais ignorée."""
    sentier = socle.sentier(0.02)
    e3 = socle.emission_e3()
    # Ligne 21, proposée par la banque, remplacée par le bloc réel.
    with pytest.raises(socle.OptionSansBlocDEssai, match="remplacé par un bloc réel"):
        socle.blocs(sentier, reels=(Banque(),), lignes={"21": lambda vue, s: {}})
    # Déclaration du bloc 8 alors que le bloc réel le remplace.
    with pytest.raises(socle.OptionSansBlocDEssai, match="remplacé par un bloc réel"):
        socle.blocs(sentier, reels=(BanqueCentrale(),),
                    declarations={"banque_centrale": socle.declaration_d_essai(
                        "banque_centrale")})
    # Ligne 19a-BC sans siège qui la propose : déclaration du bloc 9 privée de cette ligne.
    propre = socle.declaration_d_essai("finances_publiques")
    sans = dataclasses.replace(propre, sieges=tuple(
        dataclasses.replace(s, propose=tuple(x for x in s.propose if x != "19a-BC"))
        for s in propre.sieges))
    with pytest.raises(socle.OptionSansBlocDEssai, match="qu'aucun de ses sièges ne propose"):
        socle.blocs(sentier, lignes=e3["lignes"], declarations={"finances_publiques": sans})
    # Ligne absente du catalogue ; radical inconnu.
    with pytest.raises(socle.OptionSansBlocDEssai, match="absente du catalogue"):
        socle.blocs(sentier, lignes={"99z": lambda vue, s: {}})
    with pytest.raises(socle.OptionSansBlocDEssai, match="inconnu"):
        socle.blocs(sentier, declarations={"commerce": propre})
    # Les options d'E3 restent admises sous les blocs réels du banc.
    assert len(socle.blocs(sentier, reels=reels(), **e3)) == len(socle.RADICAUX)


# --------------------------------------------------------------------------
# Stationnarité partielle étendue (P94)
# --------------------------------------------------------------------------


class Releve:
    """Observateur d'essai : par pas, montants exécutés des lignes 1 à 5 et 15, variables du pas
    et état t + 1 (forme attendue par `grandeurs_b` et `grandeurs_p94`)."""

    def __init__(self):
        self.pas = []
        self._montants = {}

    def relever(self, e):
        if type(e) is ClotureDePhase:
            for ligne, termes in e.montants:
                if ligne in ("1", "2", "3", "4", "5", "15"):
                    self._montants[ligne] = sum(x for _, x in termes)
        elif type(e) is FinDePas:
            self.pas.append({**self._montants, "t": e.t, "variables": dict(e.variables_du_pas),
                             "etat": e.etat})
            self._montants = {}


def ecart(x, reference, nulle):
    """|x/x̄ − 1| ; pour une grandeur nulle en arithmétique exacte (`nulle`, D1 :
    `socle.est_nulle`), |x| (P66, P94). Le classement ne lit pas x̄ : le script rend i_D à
    π* = 0 à l'arrondi près, (1 + r̄)(1 + 0) − 1 − ϖ_D = 8,7e−18 sous r̄ = ϖ_D = 0,01, valeur
    nulle en exact ; un écart relatif à un résidu d'arrondi n'a pas de sens."""
    return abs(x) if nulle else abs(x / reference - 1.0)


ETATS_P94 = ("i_L", "i_D", "r_hat_etoile", "pi_e", "pi_etoile")


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_p94_stationnarite_partielle_etendue(socle, pi, publier):
    """P94 : sur le contrôle du banc (720 pas sans choc depuis l'état résolu), max sur les pas de
    |x_t/x̄ − 1| ≤ 1e−9 pour B1 à B7, B12, B13, B24, B8, B9, B16, B17, B18 (i), B19, B20, B25,
    B26 et D, et pour les états i_L, i_D, r̂*, π^e, π* contre leur sentier ; une grandeur nulle
    en arithmétique exacte sur les tables de l'essai (D1, liste déclarée
    `socle.GRANDEURS_NULLES`), |x_t| ≤ 1e−12 (B19 : rapportée à S^CB). Vérifie que le
    classement exact égale l'ancien classement flottant (|x̄| ≤ 1e−12), si bien qu'aucun verdict
    ne change. Publie à côté l'échec relatif d'i_D à π* = 0, et, pour B17 et B18 (i), le
    verdict au seuil 1e−12 de `tab:criteres-j3` (constat m5 ; P94 prime pour le verdict)."""
    sentier = socle.sentier(pi)
    tables = parametres(pi, LAMBDA_DE_LA_TABLE)
    initial = socle.etat_initial(sentier)
    releve = Releve()
    socle.derouler(initial, NB_PAS, ordonnanceur(socle, sentier, LAMBDA_DE_LA_TABLE), releve)
    releves = {**socle.grandeurs_b(releve.pas, initial, sentier),
               **socle.grandeurs_p94(releve.pas, initial, sentier)}
    resolues = {**socle.valeurs_resolues(sentier), **socle.valeurs_resolues_p94(sentier)}
    for nom in ETATS_P94:
        releves[nom] = [(t, getattr(p["etat"], nom)) for t, p in enumerate(releve.pas)]
    references = {cle: resolues[cle] for cle in resolues}
    references.update({nom: socle.valeur_d_ouverture(sentier, nom, 1) for nom in ETATS_P94})
    # D1 : classement exact, et sa concordance avec l'ancien classement flottant.
    assert set(socle.GRANDEURS_NULLES) <= set(releves)
    nulles = {cle for cle in releves if socle.est_nulle(cle, tables)}
    nulles_flottantes = {cle for cle in releves
                         if abs(references[cle]) <= SEUIL_DU_CLASSEMENT_FLOTTANT}
    assert nulles == nulles_flottantes, (nulles ^ nulles_flottantes)

    def sentier_de(cle, t):
        if cle in ETATS_P94:
            return socle.valeur_d_ouverture(sentier, cle, t + 1)
        return resolues[cle]

    pires = {}
    for cle, serie in releves.items():
        assert serie and serie[-1][0] == NB_PAS - 1, cle
        if cle in socle.SUR_12_TOURS + ("B9",):
            assert serie[0][0] == socle.PREMIER_PAS_SUR_12_TOURS, cle
        pires[cle] = max(ecart(x, sentier_de(cle, t), cle in nulles) for t, x in serie)
    for cle, pire in pires.items():
        assert pire <= (SEUIL_NUL if cle in nulles else SEUIL_P94), (cle, pire, references[cle])
    lignes = ["max |x_t/x̄ − 1| (|x_t| si x̄ nulle en exact, D1 ; B19 nulles /S^CB) : "
              + " ; ".join(f"{c} {x:.1e}" for c, x in pires.items()),
              "nulles en exact (D1), égales au classement flottant |x̄| ≤ 1e−12 : "
              + " ; ".join(f"{c} ({socle.GRANDEURS_NULLES[c][0]})"
                           for c in socle.GRANDEURS_NULLES if c in nulles)]
    if "i_D" in nulles:
        serie = releves["i_D"]
        relatif = max(abs(x / sentier_de("i_D", t) - 1.0) for t, x in serie)
        absolu = max(abs(x) for _, x in serie)
        lignes.append(f"i_D, nulle en exact (r̄ = ϖ_D), x̄ du script = "
                      f"{references['i_D']:.1e} : écart relatif {relatif:.1f} (seuil 1e−9, non "
                      f"applicable) ; écart absolu {absolu:.1e} (seuil 1e−12, tenu)")
    for cle in ("B17", "B18 (i) ϖ_L", "B18 (i) ϖ_D"):
        absolu = max(abs(x - resolues[cle]) for _, x in releves[cle])
        verdict = "tenu" if absolu <= SEUIL_TAB_CRITERES_J3 else "non tenu"
        lignes.append(f"{cle} : P94 (verdict du test) {pires[cle]:.1e} relatif, seuil 1e−9, "
                      f"tenu ; tab:criteres-j3, max |x − x̄| = {absolu:.1e}, seuil 1e−12, "
                      f"{verdict}")
    publier(f"Stationnarité partielle étendue (P94), π* = {100 * pi:g} %, 720 pas ({ETIQUETTE})",
            lignes)
