"""Bloc 3, travail et salaires, dans le socle partiel d'essai : lignes « J3 » de classe (b) (#50).

Classe (b) du classement du rang 1a de J3-b (synthèse en commentaire de la PR
#117, § 1) : état stationnaire ; T2 (b) ; cohérence des conversions, exécutée
à g_N = 0,005 par le constructeur validé, sur un sentier du script à
g_N = 0,005 (P63) ; vitesses ; rétention (résultat par ΔV_F) ; délais (dont
la variante du bloc d'essai 8 à π^e choqué) ; phases ; stationnarité partielle
B1 à B7, B12, B13, B24 et ξ (P66, P67) ; la ligne « Coût » est tenue par
`tests/invariants/test_budget.py` (P57), qui mesure tout bloc réel de
`src/nations/blocs/`. S'y ajoute la cohérence de U avec N et N^pa (T5) sur
l'état résolu et sur une sauvegarde rechargée (recommandation de `macro`,
ADR 0012, annotation du 13/11/2026, point 1.7). Seuils écrits avant l'essai
(fiche 3, § 9.6, correction prospective P56 ; P66, P67), non déplacés.

Les blocs réels de la production (#113) et du travail remplacent les blocs
d'essai de leur radical ; les six autres sont des blocs d'essai sur le sentier.
Le bloc d'essai des prix garde p_t sur le sentier et écrit μ̃_t = ln(p_t/UC_t)
(`socle.prix_exogene_marge_identite`, identité de P54 sous un prix exogène) :
T2 lit alors ω_{t−1} = UC_{t−1}/p_{t−1}, et la correction d'erreur du salaire
n'est pas coupée. T2 (b) se lit ici sur les blocs 2 et 3 réels, le prix étant
exogène ; sa lecture sur les blocs 2 à 4 réels vient avec le bloc 4 (#51).

**Étiquettes** : toute mesure dynamique porte « plans nominaux exogènes » et
l'étiquette du socle (`socle_partiel.ETIQUETTE`, par `etiquettes`) ; elle ne vaut pas verdict de boucle fermée ni de
boucle conjointe T3 ↔ BC3 (réserve de `monnaie`, synthèse du rang 1a, § 8).
"""

import dataclasses

import pytest

from nations.blocs.production import Production
from nations.blocs.travail import Travail, chomage
from nations.etat.sauvegarde import charger, sauvegarder
from nations.moteur import ordonnanceur as ordo
from nations.moteur.contrat_bloc import Lecture
from nations.moteur.conversions import facteur_par_pas
from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres import varier
from nations.moteur.parametres.cadre import PAS_PAR_AN
from nations.noyau import catalogue as cat
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas

N_A = PAS_PAR_AN.valeur
NB_PAS = 720
# Seuils écrits avant l'essai (fiche 3, § 9.6 ; P66, P67).
SEUIL_UN_PAS = 1e-10
SEUIL_720_PAS = 1e-9
SEUIL_NUL = 1e-12
SEUIL_T2 = 1e-10
SEUIL_CONVERSIONS = 1e-10
SEUIL_VITESSES = 1e-6
SEUIL_RETENTION = 1e-12
VARIABLES_DU_BLOC = ("W", "U", "N", "N_pa")
G_N_D_ESSAI = 0.005


def etiquettes(socle):
    """Étiquettes des mesures dynamiques : plans nominaux exogènes, étiquette du socle à
    bloc d'essai 8 (`socle.ETIQUETTE`, jamais écrite en dur), prix exogène."""
    return f"plans nominaux exogènes ; {socle.ETIQUETTE} ; prix exogène"


class Releve:
    """Observateur d'essai : par pas, montants exécutés des lignes 1 à 5, variables du pas et
    état t + 1."""

    def __init__(self):
        self.pas = []
        self._montants = {}

    def relever(self, e):
        if type(e) is ClotureDePhase:
            for ligne, termes in e.montants:
                if ligne in ("1", "2", "3", "4", "5"):
                    self._montants[ligne] = sum(x for _, x in termes)
        elif type(e) is FinDePas:
            self.pas.append({**self._montants, "t": e.t, "variables": dict(e.variables_du_pas),
                             "etat": e.etat})
            self._montants = {}


def ecart(x, reference):
    """|x/x̄ − 1| ; pour une valeur résolue nulle, |x| (P66)."""
    return abs(x) if reference == 0.0 else abs(x / reference - 1.0)


def options(socle, **autres):
    """Options du socle : prix exogène, μ̃ = ln(p/UC) ; plus les options de l'essai."""
    rendues = socle.prix_exogene_marge_identite()
    for cle in ("declarations", "regles"):
        rendues[cle] = {**rendues[cle], **autres.pop(cle, {})}
    return {**rendues, **autres}


def ordonnanceur(socle, sentier, parametres=None, reels=None, **autres):
    """Socle partiel où les blocs réels de la production et du travail remplacent leurs blocs
    d'essai."""
    parametres = socle.PARAMETRES_DE_REFERENCE if parametres is None else parametres
    reels = (Production(), Travail()) if reels is None else reels
    return socle.ordonnanceur(sentier, parametres, reels=reels, **options(socle, **autres))


def derouler(socle, sentier, nb_pas, initial=None, **autres):
    releve = Releve()
    initial = socle.etat_initial(sentier) if initial is None else initial
    socle.derouler(initial, nb_pas, ordonnanceur(socle, sentier, **autres), releve)
    return initial, releve


def parametres_a_g_n(socle, g_N):
    """Tables du moteur à g_N donné, par le constructeur validé (P63)."""
    p = socle.PARAMETRES_DE_REFERENCE
    return dataclasses.replace(p, travail=varier(p.travail, g_N=g_N))


@pytest.fixture(scope="module")
def trajectoires(socle):
    """Une trajectoire de 720 pas par π*, depuis l'état résolu, sans choc, blocs 2 et 3 réels."""
    return {pi: (socle.sentier(pi),) + derouler(socle, socle.sentier(pi), NB_PAS)
            for pi in socle.POINTS_PI}


# --------------------------------------------------------------------------
# État stationnaire, T2 (b), stationnarité partielle
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_un_pas_depuis_l_etat_resolu(trajectoires, socle, pi, publier):
    """Fiche 3, § 9.6, « État stationnaire » : un pas sans choc depuis l'état résolu laisse W
    (facteur [(1 + g_pr)(1 + π̄)]^{1/n_a}), N et N^pa (facteur (1 + g_N)^{1/n_a}) sur leur
    trajectoire et U = U^eq, à 1e−10 relatif ; N = N* à 1e−10."""
    sentier, _, releve = trajectoires[pi]
    apres, v = releve.pas[0]["etat"], releve.pas[0]["variables"]
    ecarts = {nom: ecart(getattr(apres, nom), socle.valeur_d_ouverture(sentier, nom, 1))
              for nom in VARIABLES_DU_BLOC}
    ecarts["U/U^eq"] = ecart(apres.U, socle.PARAMETRES_DE_REFERENCE.travail.U_eq)
    ecarts["N/N*"] = ecart(v["N_suivant"], v["N_etoile"])
    for nom, x in ecarts.items():
        assert x <= SEUIL_UN_PAS, (nom, x)
    publier(f"Bloc 3, un pas depuis l'état résolu, π* = {100 * pi:g} % ({etiquettes(socle)})", [
        "|x_1/x̄_1 − 1| : " + " ; ".join(f"{n} {x:.1e}" for n, x in ecarts.items())
        + " (seuil 1e−10)"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_variables_du_bloc_sur_leur_sentier_720_pas(trajectoires, socle, pi):
    """Les quatre variables d'état du bloc restent sur leur sentier à 1e−9 relatif sur 720 pas
    (critère de #112 étendu au bloc réel)."""
    sentier, _, releve = trajectoires[pi]
    for t, p in enumerate(releve.pas):
        for nom in VARIABLES_DU_BLOC:
            assert ecart(getattr(p["etat"], nom),
                         socle.valeur_d_ouverture(sentier, nom, t + 1)) <= SEUIL_720_PAS


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_t2_b_dernier_prix_connu(trajectoires, socle, pi, publier):
    """Fiche 3, § 9.6, T2 (b), correction prospective P56 (n_a = 12, π̄ ∈ {0 ; 2 % ; 10 %}),
    blocs 2 et 3 réels, prix exogène : après un pas, W et p sur leur sentier à 1e−10 relatif ;
    après 720 pas, |U − U^eq|/U^eq ≤ 1e−10. La lecture fautive (p_{t−2}) donnerait 1,65e−2
    et 7,94e−2 sur U à 2 % et 10 %, et 1,375e−4 et 6,617e−4 sur W au premier pas (maquette de
    `macro`, mesure du modèle). **Mesure complémentaire, prix exogène**, sans valeur de verdict
    au sens de P56 : le verdict de T2 (b) est celui du socle blocs 2 à 4 réels
    (`tests/invariants/test_prix.py`) ; la ligne « p (pas 1) » est ici tautologique, le prix
    étant exogène (avis de `macro`, 13/11/2026)."""
    sentier, _, releve = trajectoires[pi]
    v0 = releve.pas[0]["variables"]
    ecarts = {"W (pas 1)": ecart(v0["W_suivant"], socle.valeur_d_ouverture(sentier, "W", 1)),
              "p (pas 1)": ecart(v0["p"], sentier.valeur("p", socle.PRIX, 0)),
              "U (pas 720)": ecart(releve.pas[-1]["etat"].U,
                                   socle.PARAMETRES_DE_REFERENCE.travail.U_eq)}
    for nom, x in ecarts.items():
        assert x <= SEUIL_T2, (nom, x)
    publier(f"Bloc 3, T2 (b), mesure complémentaire sans verdict, π* = {100 * pi:g} % "
            f"({etiquettes(socle)} ; blocs 2 et 3 réels)", [
        " ; ".join(f"{n} {x:.1e}" for n, x in ecarts.items()) + " (seuil 1e−10)"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_stationnarite_partielle(trajectoires, socle, pi, publier):
    """P67 : max sur 720 pas de |x_t/x̄ − 1| ≤ 1e−9 pour B1 à B7, B12, B13 et B24, blocs 2 et 3
    réels, depuis l'état résolu, sans choc ; B4 à B7, B13 et B24 dès le pas 11 (D13) ; P66 :
    une grandeur de valeur résolue nulle (B7 à π* = 0, ξ) se juge en valeur absolue,
    |x_t| ≤ 1e−12. Relèvent du bloc 3 : B3 (chômage), B4 (part salariale, ligne 5), B5
    (salaire réel) ; B12 et B13 lisent le PIB, où entre la ligne 4 valorisée au coût du bloc 3."""
    sentier, initial, releve = trajectoires[pi]
    releves = socle.grandeurs_b(releve.pas, initial, sentier)
    resolues = socle.valeurs_resolues(sentier)
    pires = {}
    for cle, serie in releves.items():
        assert serie and serie[-1][0] == NB_PAS - 1
        if cle in socle.SUR_12_TOURS:
            assert serie[0][0] == socle.PREMIER_PAS_SUR_12_TOURS
        pires[cle] = max(ecart(x, resolues[cle]) for _, x in serie)
        seuil = SEUIL_NUL if resolues[cle] == 0.0 else SEUIL_720_PAS
        assert pires[cle] <= seuil, (cle, pires[cle], resolues[cle])
    publier(f"Bloc 3, stationnarité partielle (P67), π* = {100 * pi:g} %, 720 pas "
            f"({etiquettes(socle)} ; blocs 2 et 3 réels)",
            ["max |x_t/x̄ − 1| (|x_t| si x̄ = 0, P66) : "
             + " ; ".join(f"{c} {x:.1e}" for c, x in pires.items())])


def test_coherence_de_u_avec_n_et_n_pa(trajectoires, socle):
    """T5 (ADR 0012, annotation du 13/11/2026, point 1.7, recommandation de `macro`) : à
    l'ouverture, U_{t−1} = 1 − N_{t−1}/N^pa_{t−1}, avec N^pa_{t−1} = N^pa_t (1 + g_N)^{−1/n_a},
    à 1e−12 relatif, sur l'état résolu et sur l'état du pas 720 sauvegardé puis rechargé."""
    _, initial, releve = trajectoires[0.02]
    recharge = charger(sauvegarder([releve.pas[-1]["etat"]]))[0]
    assert recharge == releve.pas[-1]["etat"]
    facteur_N = facteur_par_pas(socle.PARAMETRES_DE_REFERENCE.travail.g_N)
    for etat in (initial, recharge):
        assert ecart(etat.U, chomage(etat.N, etat.N_pa / facteur_N)) <= SEUIL_NUL


# --------------------------------------------------------------------------
# Cohérence des conversions (lecture (G)) : g_N = 0,005
# --------------------------------------------------------------------------


def test_coherence_des_conversions_a_g_n_positif(socle, publier):
    """Fiche 3, § 9.6, « Cohérence des conversions » : même test d'état stationnaire à
    g_N = 0,005 (tables du moteur par le constructeur validé, sentier du script au même g_N ;
    P63) : après un pas, |N/N* − 1| ≤ 1e−10, et W, N, N^pa, U sur leur sentier à 1e−10. Le
    plus grand écart |N/N* − 1| sur 720 pas est publié, sans verdict."""
    sentier = socle.sentier(0.02, g_N=G_N_D_ESSAI)
    initial, releve = derouler(socle, sentier, NB_PAS,
                               parametres=parametres_a_g_n(socle, G_N_D_ESSAI))
    assert sentier.facteurs[socle.PERSONNES] > 1.0
    v, apres = releve.pas[0]["variables"], releve.pas[0]["etat"]
    assert ecart(v["N_suivant"], v["N_etoile"]) <= SEUIL_CONVERSIONS
    for nom in VARIABLES_DU_BLOC:
        assert ecart(getattr(apres, nom), socle.valeur_d_ouverture(sentier, nom, 1)) \
            <= SEUIL_UN_PAS, nom
    pire = max(ecart(p["variables"]["N_suivant"], p["variables"]["N_etoile"])
               for p in releve.pas)
    publier(f"Bloc 3, cohérence des conversions, g_N = 0,005, π* = 2 % ({etiquettes(socle)})", [
        f"|N/N* − 1| : pas 1 {ecart(v['N_suivant'], v['N_etoile']):.1e} (seuil 1e−10) ; "
        f"max sur 720 pas {pire:.1e} (publié, sans verdict)"])


# --------------------------------------------------------------------------
# Vitesses ; rétention par ΔV_F ; délais
# --------------------------------------------------------------------------


def chocs_g(facteur, debut, fin):
    def chocs(nom, t):
        return facteur if nom == "G_plan" and debut <= t <= fin else 1.0
    return chocs


def grandeurs_finales(releve):
    """U, N/N*, ω = W/(p pr) et ΣWB/ΣVA sur les 12 derniers tours, au dernier pas."""
    dernier = releve.pas[-1]
    v, ouverture = dernier["variables"], releve.pas[-2]["etat"]
    fenetre = releve.pas[-N_A:]
    return {"U": v["U_suivant"], "N/N*": v["N_suivant"] / v["N_etoile"],
            "ω": v["W_suivant"] / (v["p"] * ouverture.pr),
            "ΣWB/ΣVA": sum(q["5"] for q in fenetre)
            / sum(q["1"] + q["2"] + q["3"] + q["4"] for q in fenetre)}


def test_vitesses_ne_determinent_pas_l_etat_d_arrivee(socle, publier):
    """Fiche 3, § 9.6, « Vitesses » (critère 4) : G + 1 % aux tours 1 à 12 ; branches λ_w et
    λ_N × 0,5 et × 2 (constructeur validé) ; après 720 pas, l'écart relatif de U, N/N*, ω et
    ΣWB/ΣVA entre les deux branches est d'au plus 1e−6."""
    sentier = socle.sentier(0.02)
    p = socle.PARAMETRES_DE_REFERENCE
    finales = {}
    for facteur in (0.5, 2.0):
        table = varier(p.travail, lambda_w=facteur * p.travail.lambda_w.valeur,
                       lambda_N=facteur * p.travail.lambda_N.valeur)
        _, releve = derouler(socle, sentier, NB_PAS, parametres=dataclasses.replace(
            p, travail=table), chocs_des_plans=chocs_g(1.01, 1, 12))
        finales[facteur] = grandeurs_finales(releve)
        # Le choc a bien écarté l'emploi et le salaire du sentier pendant son cours.
        assert ecart(releve.pas[12]["etat"].N, socle.valeur_d_ouverture(sentier, "N", 13)) > 1e-4
        assert ecart(releve.pas[14]["etat"].W, socle.valeur_d_ouverture(sentier, "W", 15)) > 1e-5
    ecarts = {n: ecart(finales[0.5][n], finales[2.0][n]) for n in finales[0.5]}
    for nom, x in ecarts.items():
        assert x <= SEUIL_VITESSES, (nom, x)
    publier(f"Bloc 3, vitesses λ_w et λ_N × 0,5 et × 2 après un choc G + 1 % sur 12 tours "
            f"({etiquettes(socle)})", ["écart relatif après 720 pas : "
                                + " ; ".join(f"{n} {x:.1e}" for n, x in ecarts.items())
                                + " (seuil 1e−6)"])


def test_retention_resultat_par_la_valeur_nette(socle, publier):
    """Fiche 3, § 9.6, « Rétention » (résultat par ΔV_F) : état d'ouverture où N_{t−1} est tel
    que T4 donne N_0 = 1,02 N*_0 (effectif excédentaire), U_{t−1} = U^eq : la masse salariale
    dépasse celle du sentier de W(N − y/pr) = 1,961 % de WB, ΔIN (ligne 4) est inchangée au
    bit, et la valeur nette des entreprises (V^flux) baisse d'autant, à 1e−12 relatif à WB."""
    sentier = socle.sentier(0.02)
    base = socle.etat_initial(sentier)
    lam = socle.PARAMETRES_DE_REFERENCE.travail.lambda_N.valeur / N_A
    N_etoile = float(sentier.s["N_star"])
    excedentaire = dataclasses.replace(base, N=(1.02 - lam) * N_etoile / (1.0 - lam))
    _, sans = derouler(socle, sentier, 1)
    _, avec = derouler(socle, sentier, 1, initial=excedentaire)
    s, a = sans.pas[0], avec.pas[0]
    v = a["variables"]
    assert abs(v["N_suivant"] / (1.02 * v["N_etoile"]) - 1.0) <= SEUIL_RETENTION
    assert a["4"] == s["4"] and v["y"] == s["variables"]["y"] == v["y_etoile"]
    excedent = v["W_suivant"] * (v["N_suivant"] - v["y"] / base.pr)
    WB = a["5"]
    assert abs((WB - s["5"]) - excedent) / WB <= SEUIL_RETENTION
    assert abs(excedent / WB / (1.0 - 1.0 / 1.02) - 1.0) <= SEUIL_RETENTION
    nom = cat.VALEUR_NETTE_FLUX["entreprises"]
    baisse = getattr(s["etat"], nom) - getattr(a["etat"], nom)
    assert abs(baisse - excedent) / WB <= SEUIL_RETENTION
    publier(f"Bloc 3, rétention (N = 1,02 N*, un pas) ({etiquettes(socle)})", [
        f"W(N − y/pr)/WB = {excedent / WB:.6f} (1 − 1/1,02 = {1 - 1 / 1.02:.6f}) ; baisse de "
        f"V_F rapportée à l'excédent − 1 = {baisse / excedent - 1.0:.1e} ; ligne 4 inchangée "
        "au bit"])


@pytest.mark.parametrize("facteur", [1.01, 0.99])
def test_delais_d_un_choc_de_depense_publique(socle, facteur):
    """Fiche 3, § 9.6, « Délais » : G au tour n = 6 seulement : emploi inchangé (au bit) jusqu'au
    tour n, du signe du choc au tour n + 1 ; salaire inchangé jusqu'au tour n + 1, du signe du
    choc au tour n + 2."""
    sentier, n = socle.sentier(0.02), 6
    _, base = derouler(socle, sentier, n + 3)
    _, choc = derouler(socle, sentier, n + 3, chocs_des_plans=chocs_g(facteur, n, n))
    signe = 1.0 if facteur > 1.0 else -1.0

    def serie(releve, nom):
        return [p["variables"][nom] for p in releve.pas]

    N_b, N_c = serie(base, "N_suivant"), serie(choc, "N_suivant")
    W_b, W_c = serie(base, "W_suivant"), serie(choc, "W_suivant")
    assert N_c[:n + 1] == N_b[:n + 1] and signe * (N_c[n + 1] - N_b[n + 1]) > 0.0
    assert W_c[:n + 2] == W_b[:n + 2] and signe * (W_c[n + 2] - W_b[n + 2]) > 0.0


@pytest.mark.parametrize("choc", [0.01, -0.01])
def test_delais_d_un_choc_d_anticipation(socle, choc, publier):
    """Fiche 3, § 9.6, « Délais », variante du bloc d'essai 8 à π^e choqué (synthèse du rang
    1a, § 8) : π^e d'ouverture du tour n + 1 = 7 relevée de `choc` : W inchangé (au bit)
    jusqu'au tour n, modifié du signe du choc au tour n + 1, de
    (1 + π* + choc)^{1/n_a}/(1 + π*)^{1/n_a} à 1e−12 près (tous les autres termes de T3 étant
    inchangés à ce tour)."""
    sentier, n = socle.sentier(0.02), 6
    _, base = derouler(socle, sentier, n + 2)
    _, choque = derouler(socle, sentier, n + 2, choc_pi_e=lambda t: choc if t == n + 1 else 0.0)
    assert choque.pas[n]["etat"].pi_e == base.pas[n]["etat"].pi_e + choc
    W_b = [p["variables"]["W_suivant"] for p in base.pas]
    W_c = [p["variables"]["W_suivant"] for p in choque.pas]
    assert W_c[:n + 1] == W_b[:n + 1]
    rapport = W_c[n + 1] / W_b[n + 1]
    attendu = ((1.0 + 0.02 + choc) / 1.02) ** (1.0 / N_A)
    assert (rapport - 1.0) * choc > 0.0 and abs(rapport / attendu - 1.0) <= 1e-12
    publier(f"Bloc 3, délai d'un choc de π^e de {100 * choc:+g} point au tour 7 ({etiquettes(socle)})",
            [f"W_7/W̄_7 − 1 = {rapport - 1.0:.6e} (attendu {attendu - 1.0:.6e}) ; W inchangé au "
             "bit aux tours 0 à 6"])


# --------------------------------------------------------------------------
# Phases : aucune lecture hors ordre (refus de l'assemblage)
# --------------------------------------------------------------------------


def _fautif(etape, lecture):
    """Bloc du travail dont le siège `etape` déclare en plus la lecture `lecture`."""
    sieges = tuple(dataclasses.replace(s, lit=s.lit + (lecture,)) if s.etape == etape else s
                   for s in Travail.declaration.sieges)
    declaration = dataclasses.replace(Travail.declaration, sieges=sieges)
    return type("TravailFautif", (Travail,), {"__slots__": (), "declaration": declaration})()


@pytest.mark.parametrize("etape, lecture, motif", [
    # N* en phase 1 : écrit plus tard (phase 2).
    ("1", Lecture("2", "N_etoile"), "« N_etoile » : triangularité"),
    # La production du pas en phase 4 : écrite après le bloc travail (groupe suivant).
    ("4", Lecture("4", "y"), "« y » : triangularité"),
    # Le prix du pas en phase 4 : écrit plus tard (phase 5).
    ("4", Lecture("5", "p"), "« p » : triangularité"),
])
def test_phases_lecture_hors_ordre_refusee(socle, etape, lecture, motif):
    """Fiche 3, § 9.6, « Phases » : la déclaration du bloc est acceptée par `assembler` ; une
    lecture hors ordre ajoutée à un siège est refusée (`DefautDeDeclaration`), avant tout pas."""
    sentier = socle.sentier(0.02)
    ordonnanceur(socle, sentier)
    blocs = socle.blocs(sentier, reels=(Production(), _fautif(etape, lecture)))
    with pytest.raises(DefautDeDeclaration, match=motif):
        ordo.assembler(socle.PHASES, blocs, socle.PARAMETRES_DE_REFERENCE, socle.SANS_ENTREES)

