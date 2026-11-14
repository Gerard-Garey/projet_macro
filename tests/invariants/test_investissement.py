"""Bloc 6, investissement et financement des entreprises, dans le socle partiel d'essai : lignes de
classe (b) de la fiche 6 (#67), lignes (c) des fiches 7 et 8 qui n'attendaient que le bloc 6
(P90, P122), lignes de la fiche 5 reportées du rang 3 (canal des dividendes F3 des délais) et
mesures publiées de classe (a).

Classe (b) du classement du rang 1a de J3-d1 (avis de `macro`, § 1 ; fiche 6, § 9.6) : état
stationnaire du pas complet (P77 : moteur à n_a = 12 aux trois π*, valeurs de référence du script
`outils/etat_stationnaire.py`, jamais recopiées) ; superneutralité (C15 ; C30) ; bornes (a) ;
délais ; ajouts du 14/11 (b) et (c) ; ϱ̄_L tenue au bit (P128). Lignes (c) de la fiche 7 reçues
par #67 (`bf76979`, P90) : partie F3 de « Résultat et lignes exécutées », ς_L de « Bornes » et
de « Monnaie endogène », « Refus de crédit », partie ς ≠ 0 de « Empreinte ». La fiche 8 n'en a
aucune pour le bloc 6. Fiche 5 (report du rang 3, accord de `macro`) : canal des dividendes F3
des délais. Mesures (a) publiées : (d1), (d2), frontière de la double précision des bornes (b).
Coût : `test_budget.py` (P57, part de chaque bloc réel).

**Étiquettes** : blocs 2 à 8 réels, bloc d'essai 9 (plans de l'État exogènes, émission aux
montants du sentier, E3 et X4 inactives) ; aucune mesure ici ne vaut verdict de la stationnarité
partielle de la branche (banc à couverture X4, rang 5) ni de la boucle conjointe (#114).
Seuils écrits avant l'essai (fiche 6, § 9.6 ; fiche 7, § 9.6 ; critère de #67), non déplacés.
"""

import math

import pytest

from nations.blocs import investissement as bloc
from nations.etat.sauvegarde import charger, sauvegarder
from nations.moteur.conversions import TauxDeFlux, par_pas
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas

N_A = PARAMETRES_DE_REFERENCE.cadre.pas_par_an
NB_PAS = 720
TABLE = PARAMETRES_DE_REFERENCE.investissement
ETIQUETTES = "blocs 2 à 8 réels, bloc d'essai 9 (E3 et X4 inactives)"
# Seuils écrits avant l'essai (fiche 6, § 9.6 ; fiche 7, § 9.6).
SEUIL_UN_PAS = 1e-10  # relatif
SEUIL_S1 = 1e-15  # relatif (ajout du 14/11, (b))
SEUIL_LIGNES = 1e-12  # × S (C41, résultat et lignes exécutées)
SEUIL_LEVIER = 1e-12  # relatif (Endettement)
SEUIL_DELAIS = 1e-12  # relatif (montants des délais)
SEUIL_D1 = 0.01  # |e_I(t)| ≥ 1,0 % aux tours 1 à 12
SEUIL_D2 = 0.5  # e_I(120)/e_I(12) ≥ 0,5
BANDE_DE_DISTRIBUTION = (0.2, 0.9)  # #55
TOUR_DU_CHOC = 5
NB_PAS_DES_DELAIS = 9
TOURS_DU_REFUS = range(1, 13)  # tours 1 à 12 (C31)


class Releve:
    """Observateur d'essai : par pas, montants exécutés par ligne (total et termes), variables du
    pas, grandeurs d'ouverture, état t + 1."""

    def __init__(self):
        self.pas = []
        self._montants = {}

    def relever(self, e):
        if type(e) is ClotureDePhase:
            for ligne, termes in e.montants:
                self._montants[ligne] = sum(x for _, x in termes)
                self._montants[f"{ligne}:termes"] = dict(termes)
                # Termes par phase (une contrepartie de règlement, ligne 17, s'exécute à chaque
                # phase où un moyen de paiement varie).
                self._montants[f"{e.phase}/{ligne}"] = dict(termes)
        elif type(e) is FinDePas:
            self.pas.append({**self._montants, "t": e.t, "variables": dict(e.variables_du_pas),
                             "grandeurs": dict(e.grandeurs_ouverture), "etat": e.etat})
            self._montants = {}


def ecart(x, reference):
    """|x/x̄ − 1| ; pour une valeur de référence nulle, |x|."""
    return abs(x) if reference == 0.0 else abs(x / reference - 1.0)


def derouler(socle, sentier, nb_pas, initial=None, reels=None, refus=None, parametres=None,
             **options):
    releve = Releve()
    initial = socle.etat_initial(sentier) if initial is None else initial
    o = socle.ordonnanceur(sentier, PARAMETRES_DE_REFERENCE if parametres is None else parametres,
                           reels=socle.blocs_reels() if reels is None else reels, **options)
    socle.derouler(initial, nb_pas, o, releve, refus)
    return initial, releve


def sans(socle, *radicaux):
    """Blocs réels de `blocs_reels()` hors des radicaux nommés (gardés d'essai)."""
    return tuple(b for b in socle.blocs_reels() if b.declaration.radical not in radicaux)


@pytest.fixture(scope="module")
def trajectoires(socle):
    """Socle partiel, blocs réels 2 à 8, 720 pas, π* ∈ {0 ; 2 ; 10 %}."""
    rendus = {}
    for pi in socle.POINTS_PI:
        sentier = socle.sentier(pi)
        assert [b.declaration.radical for b in socle.blocs_reels()] == [
            "production", "travail", "prix", "menages", "investissement", "banque",
            "banque_centrale"]
        initial, releve = derouler(socle, sentier, NB_PAS)
        rendus[pi] = (sentier, initial, releve)
    return rendus


def _ouvertures(initial, releve):
    return [initial] + [p["etat"] for p in releve.pas[:-1]]


# --------------------------------------------------------------------------
# État stationnaire du pas complet (réserve 1 ; P77), superneutralité, bornes (a)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_un_pas_depuis_l_etat_resolu_egal_au_script(socle, trajectoires, pi):
    """Fiche 6, § 9.6, « État stationnaire » (classe (b)) : un pas sans choc depuis l'état
    initial résolu laisse ti, y_{t−1} sur leur sentier (facteurs 1 et (1 + g)^{1/n_a}), avec
    L/K = lv*, D_F/(n_a P_{t−1}(1 + π^{∗,pas})^2 v^e_{t+1}) = ν_F, K^vol/(n_a y) = κ/t̄u et
    tu = tu* = t̄u ; ϱ_L, tu*, I^{vol,plan}, I^plan, ΔL^d, D*_F et les lignes 3, 8, 14 et 18
    égaux au script ; à 1e−10 relatif, n_a = 12. T_{F,t−1}, T^e_F : nuls, nullité calculée sur τ_F
    du bloc d'essai 9 (`sentier.par.tau_F`, P121), jugés au bit."""
    sentier, initial, releve = trajectoires[pi]
    p = releve.pas[0]
    v, s, e = p["variables"], sentier.s, p["etat"]
    for nom, cle in (("varrho_L", "rho_L"), ("tu_etoile", "tu_star"), ("I_vol_plan", "I_vol_plan"),
                     ("I_plan", "I_plan"), ("Delta_L_d", "dL_d"), ("D_etoile_F", "D_F_star")):
        assert ecart(v[nom], s[cle]) <= SEUIL_UN_PAS, nom
    for ligne, cle in (("3", "I"), ("8", "amort"), ("14", "Div_F"), ("18", "dL")):
        assert ecart(p[ligne], s[cle]) <= SEUIL_UN_PAS, ligne
    assert ecart(e.ti, initial.ti) <= SEUIL_UN_PAS
    assert ecart(e.ti, s["ti_1"]) <= SEUIL_UN_PAS
    assert ecart(e.y_m1, socle.valeur_d_ouverture(sentier, "y_m1", 1)) <= SEUIL_UN_PAS
    assert e.varrho_bar_L == initial.varrho_bar_L
    assert ecart(e.L / e.K, TABLE.lv_etoile) <= SEUIL_UN_PAS
    D_etoile = v["D_etoile_F"]
    assert ecart(e.D_F, D_etoile) <= SEUIL_UN_PAS
    pis = p["grandeurs"]["pi_etoile_pas"]
    assert ecart(e.D_F / (N_A * initial.registre_prix[0] * (1.0 + pis) ** 2 * v["v_e_suivant"]),
                 TABLE.nu_F) <= SEUIL_UN_PAS
    kappa = PARAMETRES_DE_REFERENCE.production.kappa
    assert ecart(initial.K_vol / (N_A * v["y"]), kappa / TABLE.tu_bar) <= SEUIL_UN_PAS
    assert ecart(v["tu"], TABLE.tu_bar) <= SEUIL_UN_PAS
    assert ecart(v["tu_etoile"], TABLE.tu_bar) <= SEUIL_UN_PAS
    assert sentier.par.tau_F == 0.0
    assert e.T_F_m1 == 0.0 and v["T_e_F"] == 0.0


def test_superneutralite_des_grandeurs_reelles(trajectoires, publier):
    """Fiche 6, § 9.6, « Superneutralité » (C15 ; C30), classe (b) : pour π̄ = π* ∈ {0 ; 2 ;
    10 %}, au pas 0 du moteur, K^vol/(n_a y), tu et ti identiques à 1e−10 (relatif, contre
    π* = 2 %) ; les grandeurs nominales sur leurs valeurs du script (test précédent)."""
    reels = {}
    for pi, (sentier, initial, releve) in trajectoires.items():
        p = releve.pas[0]
        reels[pi] = {"K^vol/(n_a y)": initial.K_vol / (N_A * p["variables"]["y"]),
                     "tu": p["variables"]["tu"], "ti": p["etat"].ti}
    lignes = []
    for nom in ("K^vol/(n_a y)", "tu", "ti"):
        pire = max(ecart(reels[pi][nom], reels[0.02][nom]) for pi in reels)
        lignes.append(f"{nom} : {reels[0.02][nom]!r} ; écart max entre π* : {pire:.1e}")
        assert pire <= SEUIL_UN_PAS, nom
    publier(f"Bloc 6, superneutralité au pas 0 ({ETIQUETTES})", lignes)


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_bornes_a_a_l_etat_resolu(trajectoires, pi, publier):
    """Fiche 6, § 9.6, « Bornes » (a), classe (b) : au pas 0 depuis l'état résolu, Div_F > 0,
    D_F > 0, L > 0 et taux de distribution Div_F/(Div_F + FU) dans [0,2 ; 0,9] (#55), FU par la
    variation de la valeur nette des entreprises (sans actions ni réévaluation)."""
    sentier, initial, releve = trajectoires[pi]
    p = releve.pas[0]
    positions = {q: getattr(initial, q) for q in cat.NOMS_POSTES}
    suivantes = {q: getattr(p["etat"], q) for q in cat.NOMS_POSTES}
    FU = (idt.valeur_nette_stock(suivantes, "entreprises")
          - idt.valeur_nette_stock(positions, "entreprises"))
    div = p["14"]
    distribution = div / (div + FU)
    publier(f"Bloc 6, bornes (a) à π* = {pi:.0%} ({ETIQUETTES})", [
        f"Div_F = {div:.6g} ; FU = {FU:.6g} ; distribution = {distribution:.5f} ; "
        f"script : {sentier.e['Div_F'] / (sentier.e['Div_F'] + sentier.e['FU']):.5f}"])
    assert div > 0.0 and initial.D_F > 0.0 and initial.L > 0.0
    assert BANDE_DE_DISTRIBUTION[0] <= distribution <= BANDE_DE_DISTRIBUTION[1]


# --------------------------------------------------------------------------
# Lectures sur 720 pas : S1 (ajout (b)), ϱ̄_L (P128), π* (ajout (c)), C41 (fiche 7, F3),
# ligne 18 (fiche 7, monnaie endogène), levier (Endettement)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_lectures_et_identites_sur_720_pas(trajectoires, pi, publier):
    """Sur 720 pas, blocs 2 à 8 réels :
    - ajout du 14/11 (b) : ϱ_{L,t} = (1 + i_{L,t})/(1 + π*_t) − 1, i_L et π* de l'ouverture, à
      1e−15 relatif ;
    - P128 : ϱ̄_L égale au bit à sa valeur initiale à chaque pas ;
    - ajout du 14/11 (c) : à cible constante, π*_t constante au bit ;
    - fiche 7, « Résultat et lignes exécutées », partie F3 (C41) : les intérêts que F3 recalcule,
      i_L L/n_a et i_D max(0 ; D_F)/n_a sur l'ouverture, égaux aux lignes 9 et 10 (part des
      entreprises) exécutées, à 1e−12 × S^Bk ;
    - fiche 7, « Monnaie endogène », partie ς_L (ς_L = 0) : ligne 18 = (1 − ς_L) max(ΔL^d ; 0)
      + min(ΔL^d ; 0), exacte ;
    - fiche 6, « Endettement » (7 (d)), partie levier : L_{t+1}/K_{t+1} = lv* à 1e−12 relatif à
      chaque pas où le plan nominal est servi (v = d, aucun rationnement)."""
    sentier, initial, releve = trajectoires[pi]
    ouvertures = _ouvertures(initial, releve)
    pire_s1 = pire_lignes = pire_levier = 0.0
    servis = 0
    for t, p in enumerate(releve.pas):
        o, v, e = ouvertures[t], p["variables"], p["etat"]
        attendu = (1.0 + o.i_L) / (1.0 + o.pi_etoile) - 1.0
        pire_s1 = max(pire_s1, ecart(v["varrho_L"], attendu))
        assert e.varrho_bar_L == initial.varrho_bar_L
        assert e.pi_etoile == initial.pi_etoile
        s_bk = idt.echelle_bilan({q: getattr(o, q) for q in cat.NOMS_POSTES}, "banque")
        l9 = par_pas(TauxDeFlux(o.i_L)) * o.L
        l10 = par_pas(TauxDeFlux(o.i_D)) * max(0.0, o.D_F)
        pire_lignes = max(pire_lignes, abs(p["9"] - l9) / s_bk,
                          abs(p["10:termes"]["iD_DF"] - l10) / s_bk)
        assert p["18"] == bloc.credit_servi(0.0, v["Delta_L_d"])
        # Plan servi : aucun rationnement (N6), v = d < IN^vol + y.
        if v["v"] < v["y"] + o.IN_vol:
            servis += 1
            pire_levier = max(pire_levier, ecart(e.L / e.K, TABLE.lv_etoile))
    publier(f"Bloc 6, lectures et identités sur 720 pas, π* = {pi:.0%} ({ETIQUETTES})", [
        f"S1 : {pire_s1:.1e} rel. (seuil 1e−15) ; lignes 9 et 10 contre F3 : {pire_lignes:.1e} "
        f"× S^Bk (seuil 1e−12) ; levier : {pire_levier:.1e} rel. sur {servis} pas servis "
        "(seuil 1e−12)"])
    assert pire_s1 <= SEUIL_S1
    assert pire_lignes <= SEUIL_LIGNES
    assert servis == NB_PAS and pire_levier <= SEUIL_LEVIER


# --------------------------------------------------------------------------
# Délais (C35 ; critère 12 (b)), classe (b), quelques tours
# --------------------------------------------------------------------------


def _premier_ecart(base, choc, nom):
    """Premier tour où la variable du pas `nom` diffère au bit de la base, et le signe."""
    for t, (a, b) in enumerate(zip(base.pas, choc.pas, strict=True)):
        x, y = a["variables"][nom], b["variables"][nom]
        if x != y:
            return t, math.copysign(1.0, y - x)
    return None, 0.0


def _premiere_ligne(base, choc, ligne):
    for t, (a, b) in enumerate(zip(base.pas, choc.pas, strict=True)):
        if a[ligne] != b[ligne]:
            return t, math.copysign(1.0, b[ligne] - a[ligne])
    return None, 0.0


def test_delais_du_taux_de_la_cible_de_la_depense_et_de_l_impot(socle, publier):
    """Fiche 6, § 9.6, « Délais » (C35 ; critère 12 (b) ; annotation du 14/11/2026 ; correction
    prospective du 04/10/2026), choc au tour n = 5, signe et date exacts, montants à 1e−12 :
    - taux du crédit relevé d'un point au tour n (i_{L,n+1}, bloc d'essai 7) : I^plan inchangé au
      bit au tour n ; au tour n + 1, I^{vol,plan}/I^{vol,plan,réf} = e^{−η_r Δϱ}, Δϱ = Δi_L/(1 + π*) ;
    - cible abaissée d'un point au tour n (π*_{n+1}, bloc d'essai 8) : plans et T^e_F du tour n
      identiques au bit, modifiés au tour n + 1 (T_F rendu non nul par une règle de ligne 7, dans
      la base comme sous le choc) ;
    - dépense publique + 1 % au tour n (plan du bloc d'essai 9) : Div_F modifié au tour n (+) ;
      I^plan inchangé au bit au tour n + 1, modifié au tour n + 2 ; au tour n + 1, aucun
      rationnement et I^vol/I^vol,réf = p^réf/p ;
    - impôt des entreprises relevé de ΔT au seul tour n (règle de ligne 7) : D_F d'ouverture du
      tour n + 1 abaissé de ΔT (1e−12 × S^F), Div_F du tour n identique au bit, Div_F du tour
      n + 1 abaissé de ΔT (rattrapage) + Γ^e ΔT (impôt anticipé) + i_D ΔT/n_a (intérêts sur les
      dépôts d'ouverture), à 1e−12 relatif."""
    sentier = socle.sentier(0.02)
    n = TOUR_DU_CHOC
    lignes = []
    # Taux du crédit (bloc d'essai 7, i_L relevé d'un point à l'ouverture de n + 1).
    sans_7 = sans(socle, "banque")

    def taux(vue, s, t):
        return s.valeur("i_L_1", socle.CONSTANTE, t) + (0.01 if t == n else 0.0)
    _, base_7 = derouler(socle, sentier, NB_PAS_DES_DELAIS, reels=sans_7)
    _, choc_7 = derouler(socle, sentier, NB_PAS_DES_DELAIS, reels=sans_7, regles={"i_L": taux})
    assert _premier_ecart(base_7, choc_7, "I_plan") == (n + 1, -1.0)
    vb, vc = base_7.pas[n + 1]["variables"], choc_7.pas[n + 1]["variables"]
    d_rho = vc["varrho_L"] - vb["varrho_L"]
    assert ecart(d_rho, 0.01 / (1.0 + 0.02)) <= 1e-12
    rapport = vc["I_vol_plan"] / vb["I_vol_plan"]
    assert ecart(rapport, math.exp(-TABLE.eta_r * d_rho)) <= SEUIL_DELAIS
    lignes.append(f"taux : I^plan modifié au tour {n + 1} ; rapport {rapport:.10f}, "
                  f"e^(−η_r Δϱ) = {math.exp(-TABLE.eta_r * d_rho):.10f}")
    # Cible (bloc d'essai 8), avec T_F non nul (règle de ligne 7 : T_F = 1 % de Div_F du sentier).
    sans_8 = sans(socle, "banque_centrale")

    def impot_f(vue, s):
        t = vue.ouverture.t
        return {"T_H": s.valeur("T_H", socle.NOMINAL, t),
                "T_F": 0.01 * s.valeur("Div_F", socle.NOMINAL, t)}

    def cible(vue, s, t):
        return vue.ouverture.pi_etoile - (0.01 if t == n else 0.0)
    _, base_8 = derouler(socle, sentier, NB_PAS_DES_DELAIS, reels=sans_8, lignes={"7": impot_f})
    _, choc_8 = derouler(socle, sentier, NB_PAS_DES_DELAIS, reels=sans_8, lignes={"7": impot_f},
                         regles={"pi_etoile": cible})
    for nom in ("I_plan", "T_e_F"):
        assert _premier_ecart(base_8, choc_8, nom)[0] == n + 1, nom
    lignes.append(f"cible : I^plan et T^e_F modifiés au tour {n + 1} (signes "
                  f"{_premier_ecart(base_8, choc_8, 'I_plan')[1]:+.0f} et "
                  f"{_premier_ecart(base_8, choc_8, 'T_e_F')[1]:+.0f})")
    # Dépense publique (plan du bloc d'essai 9).
    _, base = derouler(socle, sentier, NB_PAS_DES_DELAIS)
    _, g = derouler(socle, sentier, NB_PAS_DES_DELAIS,
                    chocs_des_plans={"G_plan": lambda t: 1.01 if t == n else 1.0})
    assert _premiere_ligne(base, g, "14") == (n, 1.0)
    assert _premier_ecart(base, g, "I_plan") == (n + 2, 1.0)
    pb, pg = base.pas[n + 1], g.pas[n + 1]
    ouverture_g = g.pas[n]["etat"]
    assert pg["variables"]["v"] < pg["variables"]["y"] + ouverture_g.IN_vol  # aucun rationnement
    volumes = pg["variables"]["I_vol"] / pb["variables"]["I_vol"]
    prix = pb["variables"]["p"] / pg["variables"]["p"]
    assert ecart(volumes, prix) <= SEUIL_DELAIS
    lignes.append(f"dépense publique : Div_F modifié au tour {n} (+), I^plan au tour {n + 2} ; "
                  f"au tour {n + 1}, volumes {volumes:.12f}, inverse des prix {prix:.12f}")
    # Impôt des entreprises au seul tour n (règle de ligne 7).
    delta_T = 0.1 * sentier.valeur("Div_F", socle.NOMINAL, n)

    def impot_choc(vue, s):
        t = vue.ouverture.t
        return {"T_H": s.valeur("T_H", socle.NOMINAL, t),
                "T_F": s.valeur("T_F", socle.NOMINAL, t) + (delta_T if t == n else 0.0)}
    _, t_f = derouler(socle, sentier, NB_PAS_DES_DELAIS, lignes={"7": impot_choc})
    e_b, e_c = base.pas[n]["etat"], t_f.pas[n]["etat"]
    s_f = idt.echelle_bilan({q: getattr(e_b, q) for q in cat.NOMS_POSTES}, "entreprises")
    assert abs((e_b.D_F - e_c.D_F) - delta_T) <= SEUIL_DELAIS * s_f
    assert t_f.pas[n]["14"] == base.pas[n]["14"]
    gamma_e = base.pas[n + 1]["grandeurs"]["Gamma_e"]
    i_d = par_pas(TauxDeFlux(e_b.i_D))
    baisse = base.pas[n + 1]["14"] - t_f.pas[n + 1]["14"]
    attendu = delta_T * (1.0 + gamma_e + i_d)
    assert ecart(baisse, attendu) <= SEUIL_DELAIS
    lignes.append(f"impôt des entreprises : D_F d'ouverture du tour {n + 1} − ΔT ; Div_F du tour "
                  f"{n + 1} − {baisse / delta_T:.12f} ΔT (attendu 1 + Γ^e + i_D/n_a = "
                  f"{attendu / delta_T:.12f})")
    publier(f"Bloc 6, délais, choc au tour {n} ({ETIQUETTES} ; blocs 7 ou 8 d'essai pour le "
            "taux et la cible)", lignes)


def test_canal_des_dividendes_des_delais_de_la_fiche_5(socle, publier):
    """Fiche 5, § 9.6, « Délais », canal des dividendes (F3), reporté du rang 3 à #67 (accord de
    `macro`) : dépense publique + 1 % au tour n (plan du bloc d'essai 9), blocs 5 et 6 réels :
    dividende des entreprises (ligne 14) modifié au tour n, signe + ; budget des ménages C^plan
    modifié au tour n + 1, signe + (YD_n relevé par Div_F) ; signe et date exacts. Texte du
    critère : annotation du 04/10/2026 (« dividende au tour n, budget au tour n + 1 »)."""
    sentier = socle.sentier(0.02)
    n = TOUR_DU_CHOC
    _, base = derouler(socle, sentier, NB_PAS_DES_DELAIS)
    _, g = derouler(socle, sentier, NB_PAS_DES_DELAIS,
                    chocs_des_plans={"G_plan": lambda t: 1.01 if t == n else 1.0})
    dividende = _premiere_ligne(base, g, "14")
    budget = _premier_ecart(base, g, "C_plan")
    revenu = [b["etat"].YD_m1 - a["etat"].YD_m1 for a, b in zip(base.pas, g.pas, strict=True)]
    publier(f"Fiche 5, délais, canal des dividendes F3, G + 1 % au tour {n} ({ETIQUETTES})", [
        f"ligne 14 : premier tour modifié {dividende} ; C^plan : premier tour modifié {budget} ; "
        f"ΔYD_{n} = {revenu[n]:.6g} (attendu : tour {n}, + ; tour {n + 1}, +)"])
    assert dividende == (n, 1.0)
    assert budget == (n + 1, 1.0)
    assert revenu[n] > 0.0


# --------------------------------------------------------------------------
# Fiche 7, lignes (c) reçues par #67 : refus de crédit (C31, C40), bornes, empreinte
# --------------------------------------------------------------------------


def _refus(t):
    return 0.5 if t in TOURS_DU_REFUS else 0.0


def test_refus_de_credit(socle, publier):
    """Fiche 7, § 9.6, « Refus de crédit » (C31, C40 ; fiche 6) et parties ς_L de « Bornes » et
    de « Monnaie endogène » : ς_L = 0,5 aux tours 1 à 12 (entrée de scénario du tour) :
    - ligne 18 = (1 − ς_L) max(ΔL^d ; 0) + min(ΔL^d ; 0), exacte, à chaque tour ; demande non
      satisfaite ΔL^d − ΔL publiée ;
    - effet sur Div_F, en unités du crédit nouveau de base, aux tours 1 à 3 (repères de la fiche
      7 : −50, −25 et −13 %) et rebond au tour 13 publiés, sans verdict ;
    - part directe du refus, Δligne 18/ΔL_base, publiée (−0,5 au tour 1, puis (1 − ς_L) fois une
      demande qui a changé) ;
    - « Monnaie endogène », partie ς_L ≠ 0 : à la clôture de la phase 3, la variation de
      D_H + D_F (ligne 17 de la phase 3) égale au bit le montant exécuté de la ligne 18 ;
    - Div_F ≥ 0 et D_F ≥ 0 (lecture nette) inactives, ou désactivées au plus tard 12 tours après
      la fin du choc, sans réactivation (fiche 6, « Bornes » (c), partie ς_L) ; Div_Bk ≥ 0 de
      même (fiche 7, « Bornes », partie ς_L).
    Les montants (effets sur Div_F, part directe, rebond) sont publiés **sans verdict** : les
    repères −50, −25 et −13 % de la fiche 7 viennent de la maquette en équilibre partiel (avis de
    `monnaie`, rang 4)."""
    sentier = socle.sentier(0.02)
    nb = 40
    _, base = derouler(socle, sentier, nb)
    _, refus = derouler(socle, sentier, nb, refus=_refus)
    lignes = []
    actifs = {"Div_F": [], "D_F": [], "Div_Bk": []}
    for t, (a, b) in enumerate(zip(base.pas, refus.pas, strict=True)):
        demande = b["variables"]["Delta_L_d"]
        assert b["18"] == bloc.credit_servi(_refus(t), demande)
        variation_des_depots = sum(b["3/17"].values())
        assert variation_des_depots == b["18"], t
        if b["14"] == 0.0:
            actifs["Div_F"].append(t)
        if b["etat"].D_F <= 0.0:
            actifs["D_F"].append(t)
        if b["15"] == 0.0:
            actifs["Div_Bk"].append(t)
        if t in (1, 2, 3, 13):
            effet = (b["14"] - a["14"]) / a["18"]
            directe = (b["18"] - a["18"]) / a["18"]
            lignes.append(f"tour {t} : ς_L = {_refus(t)} ; demande non satisfaite "
                          f"{demande - b['18']:.6g} ; Δligne 18/ΔL_base = {directe:+.3f} ; "
                          f"ΔDiv_F/ΔL_base = {effet:+.1%}")
    lignes.append(f"bornes actives (tours) : {actifs}")
    publier(f"Fiche 7, refus de crédit ς_L = 0,5 aux tours 1 à 12 ({ETIQUETTES} ; montants "
            "sans verdict)", lignes)
    fin = max(TOURS_DU_REFUS)
    for nom, tours in actifs.items():
        assert all(t <= fin + 12 for t in tours), nom


def test_reprise_exacte_sous_refus_de_credit(socle):
    """Fiche 7, § 9.6, « Empreinte », partie ς ≠ 0 : sauvegarde au tour 6 d'une partie où
    ς_L = 0,5 aux tours 1 à 12, rechargée et reprise avec le même scénario : états de clôture
    identiques au bit à ceux d'une trajectoire continue de 24 pas."""
    sentier = socle.sentier(0.02)
    o = socle.ordonnanceur(sentier, reels=socle.blocs_reels())
    continu = Releve()
    fin_continue = socle.derouler(socle.etat_initial(sentier), 24, o, continu, _refus)
    milieu = socle.derouler(socle.etat_initial(sentier), 6, o, Releve(), _refus)
    repris, = charger(sauvegarder([milieu]))
    assert repris == milieu
    reprise = Releve()
    fin_reprise = socle.derouler(repris, 18, o, reprise, _refus)
    assert sauvegarder([fin_reprise]) == sauvegarder([fin_continue])
    assert [p["etat"] for p in reprise.pas] == [p["etat"] for p in continu.pas[6:]]


# --------------------------------------------------------------------------
# Mesures (a) publiées : (d1), (d2), frontière des bornes (b)
# --------------------------------------------------------------------------


def _equilibre_partiel(eta_r, zeta, choc, tours, lambda_ti=TABLE.lambda_ti.valeur):
    """I^vol_t (t = 1…tours) en équilibre partiel, à π* = 2 % et n_a = 12 : production et prix
    sur leur sentier (y_t = y_0 (1 + g)^{t/n_a}), plan servi en volume ; S2, S3, S6 du bloc et
    N10, N11 (K^vol, tu) ; Δϱ_t = choc(t)."""
    from nations.moteur.conversions import facteur_par_pas
    from nations.moteur.parametres import TauxDeCroissance
    kappa = PARAMETRES_DE_REFERENCE.production.kappa
    delta_pas = par_pas(TABLE.delta)
    f_g = facteur_par_pas(TauxDeCroissance(0.02)) * facteur_par_pas(TauxDeCroissance(0.0))
    y0 = 1.0
    ti = (N_A * (f_g - 1.0) + TABLE.delta.valeur) * kappa / TABLE.tu_bar
    K_vol = N_A * kappa * y0 / TABLE.tu_bar
    y_m1 = y0 / f_g
    serie = []
    for t in range(tours):
        d_rho = choc(t + 1)
        tu_etoile = bloc.utilisation_visee(TABLE.tu_bar, zeta, d_rho, 0.0)
        I_vol = bloc.plan_en_volume(ti, f_g, y_m1, eta_r, d_rho, 0.0)
        y = y0 * f_g ** t
        tu = y / (K_vol * par_pas(TauxDeFlux(1.0 / kappa)))
        ti = bloc.part_visee_suivante(ti, lambda_ti / N_A, tu, tu_etoile)
        K_vol = (1.0 - delta_pas) * K_vol + I_vol
        y_m1 = y
        serie.append(I_vol)
    return serie


def test_seuils_d1_et_d2_en_equilibre_partiel(publier):
    """Fiche 6, § 9.6, (d1) et (d2) (critère 12 (d), M28), classe (a) : Δϱ_L = +1 point aux
    tours 1 à 12 : |e_I(t)| ≥ 1,0 % à chacun des tours 1 à 12, valeurs publiées pour η_r × 0,5 et
    × 2 ; même choc maintenu 120 tours : e_I(120)/e_I(12) ≥ 0,5. e_I(t) = I^vol_t/I^vol,réf_t − 1,
    même état, chemin de référence sans choc. Appel direct des fonctions du bloc et de N10, N11."""
    lignes = []
    ref = _equilibre_partiel(TABLE.eta_r, TABLE.zeta, lambda t: 0.0, 120)
    for facteur in (0.5, 1.0, 2.0):
        eta = TABLE.eta_r * facteur
        ref_eta = _equilibre_partiel(eta, TABLE.zeta, lambda t: 0.0, 12)
        temp = _equilibre_partiel(eta, TABLE.zeta, lambda t: 0.01 if t <= 12 else 0.0, 12)
        e = [temp[t] / ref_eta[t] - 1.0 for t in range(12)]
        lignes.append(f"(d1) η_r = {eta:g} : min |e_I| aux tours 1 à 12 = {min(map(abs, e)):.4%}")
        if facteur == 1.0:
            assert min(map(abs, e)) >= SEUIL_D1
    maintenu = _equilibre_partiel(TABLE.eta_r, TABLE.zeta, lambda t: 0.01, 120)
    e12 = maintenu[11] / ref[11] - 1.0
    e120 = maintenu[119] / ref[119] - 1.0
    lignes.append(f"(d2) e_I(1) = {maintenu[0] / ref[0] - 1.0:.4%} ; e_I(12) = {e12:.4%} ; "
                  f"e_I(120) = {e120:.4%} ; rapport = {e120 / e12:.4f}")
    assert e120 / e12 >= SEUIL_D2
    publier("Bloc 6, (d1) et (d2) en équilibre partiel (ζ = 4, λ_ti = 0,02, π* = 2 %)", lignes)


def _evaluer(fonction, *arguments):
    """Valeur rendue, ou nom de l'exception levée."""
    try:
        return fonction(*arguments)
    except ArithmeticError as erreur:
        return type(erreur).__name__


def test_frontiere_de_la_double_precision_des_bornes_b(publier):
    """Fiche 6, § 9.6, « Bornes » (b), lues « pour toute entrée dans le domaine déclaré » (P139) :
    frontière publiée, sans verdict ; par appel direct des fonctions pures, l'exponentielle de S3
    et de S6 sous-dépasse (plan ou part nuls) au-delà d'un argument d'environ −745 et déborde
    au-delà d'environ +709 (`math.exp` lève `OverflowError`, que le moteur traduit en
    `DepassementNumerique` : test suivant). Le lot de 10^5 tirages dans le domaine déclaré est
    jugé par `tests/unitaires/test_investissement.py`."""
    mesures = [
        ("plan, −η_r Δϱ = +746", _evaluer(bloc.plan_en_volume, 0.14, 1.0, 1.0, 746.0, -1.0, 0.0)),
        ("plan, −η_r Δϱ = −746", _evaluer(bloc.plan_en_volume, 0.14, 1.0, 1.0, 746.0, 1.0, 0.0)),
        ("part, (λ/n_a)(tu − tu*) = −746",
         _evaluer(bloc.part_visee_suivante, 0.14, 1.0, 0.0, 746.0)),
        ("part, (λ/n_a)(tu − tu*) = −700",
         _evaluer(bloc.part_visee_suivante, 0.14, 1.0, 0.0, 700.0)),
        ("tu*, ζ Δϱ = +710", _evaluer(bloc.utilisation_visee, 0.8, 710.0, 1.0, 0.0)),
    ]
    publier("Bloc 6, bornes (b), frontière de la double précision (sans verdict)",
            [f"{nom} : {valeur!r}" for nom, valeur in mesures])
    assert mesures[0][1] == "OverflowError" and mesures[4][1] == "OverflowError"
    assert mesures[1][1] == 0.0 and mesures[2][1] == 0.0 and mesures[3][1] > 0.0


# --------------------------------------------------------------------------
# Fiche 5, boucle conjointe (b-x), reportée du rang 3 à #67 : mesure de décroissance
# --------------------------------------------------------------------------

NB_PAS_DE_LA_BOUCLE = 2400
FENETRE_DE_LA_BOUCLE = 240


def _ratios_reels(releve):
    """Grandeurs réelles relevées par pas (aucune n'a la racine nominale) : tu, U, ti, K^vol/y,
    C^plan/YD^e, D_H/YD_{t−1}, D_F/L, IN^vol/v."""
    rendus = []
    for p in releve.pas:
        v, e = p["variables"], p["etat"]
        rendus.append({"tu": v["tu"], "U": v["U_suivant"], "ti": e.ti, "K/y": e.K_vol / v["y"],
                       "C/YD": v["C_plan"] / v["YD_e"], "D_H/YD": e.D_H / e.YD_m1,
                       "D_F/L": e.D_F / e.L, "IN/v": e.IN_vol / v["v"]})
    return rendus


def _vitesses(facteur):
    import dataclasses
    from nations.moteur.parametres import varier
    p = PARAMETRES_DE_REFERENCE
    if facteur == 1.0:
        return p
    return dataclasses.replace(
        p, production=varier(p.production, lambda_v=p.production.lambda_v.valeur * facteur,
                             lambda_IN=p.production.lambda_IN.valeur * facteur),
        travail=varier(p.travail, lambda_w=p.travail.lambda_w.valeur * facteur,
                       lambda_N=p.travail.lambda_N.valeur * facteur),
        prix=varier(p.prix, lambda_mu=p.prix.lambda_mu.valeur * facteur),
        menages=varier(p.menages, lambda_H=p.menages.lambda_H.valeur * facteur),
        investissement=varier(p.investissement,
                              lambda_ti=p.investissement.lambda_ti.valeur * facteur))


def test_boucle_conjointe_b_x_de_la_fiche_5(socle, publier):
    """Fiche 5, § 9.6, « Boucle conjointe » (critère 5 (c) ; réserve 3), partie (b-x) reportée du
    rang 3 à #67 (avis de `macro`, rang 1a, § 1) : blocs 2 à 6 réels (F de la fiche 6 compris),
    blocs 7 et 8 d'essai (taux exogène, π^e = π* exogène), bloc d'essai 9 ; π* = 2 %, régime de
    l'état résolu (U = U^eq, régime B ; le régime H n'est pas atteint sur ce banc et n'est pas
    mesuré). **Mesure de décroissance, pas un calcul de valeur propre** : la carte d'un pas de
    `outils/linearisation.py` tient le registre fixe, alors que S4 et F2 lisent P_{t−1} ; G^plan
    × 1,001 au pas 0, écart des grandeurs réelles (`_ratios_reels`) au contrôle apparié, enveloppe
    par fenêtres de 240 pas, module apparent de la dernière fenêtre (pas 2 160 à 2 399). Racine
    nominale hors de la mesure (grandeurs réelles seules). Publié aux vitesses des blocs 2 à 6
    × 0,5 et × 2, **régime B, sans verdict (#114 ; P140)**."""
    sentier = socle.sentier(0.02)
    reels = sans(socle, "banque", "banque_centrale")
    lignes = []
    for facteur in (0.5, 1.0, 2.0):
        series = []
        for choc in (1.0, 1.001):
            _, releve = derouler(socle, sentier, NB_PAS_DE_LA_BOUCLE, reels=reels,
                                 parametres=_vitesses(facteur),
                                 chocs_des_plans={"G_plan": lambda t, c=choc: c if t == 0 else 1.0})
            series.append(_ratios_reels(releve))
        d = [max(abs(b[k] / a[k] - 1.0) for k in a) for a, b in zip(*series, strict=True)]
        enveloppe = [max(d[i:i + FENETRE_DE_LA_BOUCLE])
                     for i in range(0, NB_PAS_DE_LA_BOUCLE, FENETRE_DE_LA_BOUCLE)]
        module = (enveloppe[-1] / enveloppe[-2]) ** (1.0 / FENETRE_DE_LA_BOUCLE)
        lignes.append(f"vitesses × {facteur} : enveloppe {enveloppe[1]:.1e} (pas 240) → "
                      f"{enveloppe[-1]:.1e} (pas 2 160) ; module apparent {module:.5f}")
        assert math.isfinite(module)
    publier("Fiche 5, boucle conjointe (b-x), π* = 2 %, blocs 2 à 6 réels, 7 et 8 d'essai "
            "(mesure de décroissance ; régime B ; sans verdict, #114)", lignes)


# --------------------------------------------------------------------------
# Fiche 6, lignes (b-x) : vitesses (2 160 pas), endettement, formes fermées, hors cible ; boucle
# propre (a)
# --------------------------------------------------------------------------

HORIZONS_DES_VITESSES = (720, 2160, 6480)
SEUIL_VITESSES = 1e-6  # relatif, après 2 160 pas (critère amendé)
SEUIL_FORMES_FERMEES = 1e-6  # relatif, après 24 000 pas
NB_PAS_DES_FORMES_FERMEES = 24_000
NB_PAS_DE_L_ENDETTEMENT = 2160
SEUIL_DEPOTS = 1e-6  # relatif, après 2 160 pas


def _ratios_de_la_fiche_6(releve, initial, t):
    """Ratios du critère « Vitesses » au pas t (définitions du § 9.4 de la fiche 6) : K/Y (ii) =
    p_t K^vol_{t+1}/ΣPIB ; tu_t ; I/PIB = ΣI/ΣPIB ; L/K de clôture ; D_F de clôture/ΣPIB ;
    distribution ΣDiv_F/Σ(Div_F + FU), FU par la variation de la valeur nette des entreprises ;
    sommes sur les 12 tours t − 11 à t, PIB du pas = lignes 1 à 4."""
    fenetre = range(t - N_A + 1, t + 1)
    ouvertures = [initial] + [p["etat"] for p in releve.pas]

    def valeur_nette(e):
        return idt.valeur_nette_stock({q: getattr(e, q) for q in cat.NOMS_POSTES}, "entreprises")
    pib = sum(releve.pas[k]["1"] + releve.pas[k]["2"] + releve.pas[k]["3"] + releve.pas[k]["4"]
              for k in fenetre)
    div = sum(releve.pas[k]["14"] for k in fenetre)
    fu = sum(valeur_nette(ouvertures[k + 1]) - valeur_nette(ouvertures[k]) for k in fenetre)
    p, e = releve.pas[t], releve.pas[t]["etat"]
    return {"K/Y (ii)": p["variables"]["p"] * e.K_vol / pib, "tu": p["variables"]["tu"],
            "I/PIB": sum(releve.pas[k]["3"] for k in fenetre) / pib, "L/K": e.L / e.K,
            "D_F/(12 PIB)": e.D_F / pib, "distribution": div / (div + fu)}


def _hausse_de_g_pendant_12_tours(t):
    return 1.01 if 1 <= t <= 12 else 1.0


def test_vitesses_de_la_fiche_6(socle, publier):
    """Fiche 6, § 9.6, « Vitesses » (critère 6, amendé : 2 160 pas), classe (b-x) : G + 1 % aux
    tours 1 à 12 (plan du bloc d'essai 9), taux exogène (blocs 7 et 8 d'essai), prix endogènes
    (P123), π* = 2 % ; branches λ_ti × 0,5 et × 2 ; écart relatif entre branches de K/Y (ii), tu,
    I/PIB, L/K, D_F/(12 PIB) et distribution au plus 1e−6 après 2 160 pas. Écarts à 720 et à
    6 480 pas publiés sans verdict (critère d'origine ; P123)."""
    sentier = socle.sentier(0.02)
    reels = sans(socle, "banque", "banque_centrale")
    branches = []
    for facteur in (0.5, 2.0):
        import dataclasses
        from nations.moteur.parametres import varier
        parametres = dataclasses.replace(PARAMETRES_DE_REFERENCE, investissement=varier(
            TABLE, lambda_ti=TABLE.lambda_ti.valeur * facteur))
        initial, releve = derouler(socle, sentier, HORIZONS_DES_VITESSES[-1], reels=reels,
                                   parametres=parametres,
                                   chocs_des_plans={"G_plan": _hausse_de_g_pendant_12_tours})
        branches.append({h: _ratios_de_la_fiche_6(releve, initial, h - 1)
                         for h in HORIZONS_DES_VITESSES})
    lignes = []
    for h in HORIZONS_DES_VITESSES:
        ecarts = {k: ecart(branches[0][h][k], branches[1][h][k]) for k in branches[0][h]}
        lignes.append(f"{h} pas : " + " ; ".join(f"{k} {x:.1e}" for k, x in ecarts.items())
                      + (" (verdict, seuil 1e−6)" if h == 2160 else " (sans verdict)"))
        if h == 2160:
            pire = ecarts
    publier("Bloc 6, vitesses (λ_ti × 0,5 contre × 2), G + 1 % aux tours 1 à 12, π* = 2 % "
            "(blocs 2 à 6 réels, taux exogène, prix endogènes ; P123)", lignes)
    for k, x in pire.items():
        assert x <= SEUIL_VITESSES, k


def _taux_releve(socle, hausse):
    """Règle d'essai du bloc 7 : i_{L,t+1} = valeur du sentier + `hausse`, dès le pas 0 (taux
    exogène relevé de façon permanente à l'ouverture du pas 1)."""
    def regle(vue, s, t):
        return s.valeur("i_L_1", socle.CONSTANTE, t) + hausse
    return regle


def _ligne_9_sur_l_ouverture(vue, sentier):
    """B3 sur l'ouverture, pour le bloc d'essai 7 : ligne 9 = i_{L,t} L_t/n_a."""
    return {"iL_L": par_pas(TauxDeFlux(vue.ouverture.i_L)) * vue.ouverture.L}


def _ligne_10_sur_l_ouverture(vue, sentier):
    """B4 sur l'ouverture, pour le bloc d'essai 7 : ligne 10 = i_{D,t} max(0 ; D)/n_a."""
    i_pas = par_pas(TauxDeFlux(vue.ouverture.i_D))
    return {"iD_DH": i_pas * max(0.0, vue.ouverture.D_H),
            "iD_DF": i_pas * max(0.0, vue.ouverture.D_F)}


# Règles d'essai des lignes 9 et 10 du bloc d'essai 7 : intérêts sur les encours et les taux
# d'ouverture (B3, B4), pour qu'un taux relevé par règle d'essai soit aussi payé (sans elles, les
# lignes restent aux montants du sentier et F3, qui recalcule les intérêts, laisse l'écart dans
# les dépôts).
INTERETS_SUR_L_OUVERTURE = {"9": _ligne_9_sur_l_ouverture, "10": _ligne_10_sur_l_ouverture}


@pytest.fixture(scope="module")
def endettement(socle):
    """i_L relevé de 2 points de façon permanente (bloc d'essai 7, taux exogène, lignes 9 et 10
    sur l'ouverture ; bloc d'essai 8), π* = 2 %, blocs 2 à 6 réels, 2 160 pas.

    **Réserve déclarée** (avis de `monnaie`, rang 4) : le bloc d'essai 7 garde le dividende de la
    banque (ligne 15) au sentier ; le surplus d'intérêt payé par les entreprises reste donc à la
    banque, au lieu de revenir aux ménages par B6. Le levier et la distribution des entreprises
    n'en dépendent pas ; la demande des ménages, si."""
    sentier = socle.sentier(0.02)
    reels = sans(socle, "banque", "banque_centrale")
    initial, releve = derouler(socle, sentier, NB_PAS_DE_L_ENDETTEMENT, reels=reels,
                               regles={"i_L": _taux_releve(socle, 0.02)},
                               lignes=INTERETS_SUR_L_OUVERTURE)
    ouvertures = _ouvertures(initial, releve) + [releve.pas[-1]["etat"]]
    dernier = releve.pas[-1]
    pib = dernier["1"] + dernier["2"] + dernier["3"] + dernier["4"]
    return {"sentier": sentier, "releve": releve, "ouvertures": ouvertures,
            "depots": ouvertures[-2].D_F / (N_A * pib),
            "forme": sentier.e["D_F"] / (N_A * sentier.e["PIB"])}


def test_endettement_sous_un_taux_releve_de_deux_points(endettement, publier):
    """Fiche 6, § 9.6, « Endettement » (7 (d)), classe (b-x) : i_L relevé de 2 points de façon
    permanente (bloc d'essai 7, taux exogène, lignes 9 et 10 sur l'ouverture ; bloc d'essai 8),
    π* = 2 %, 2 160 pas : L_{t+1}/K_{t+1} = lv* à 1e−12 relatif à chaque pas où le plan nominal
    est servi ; distribution positive (Div_F > 0) à chaque pas. Dépôts au PIB : publiés ici,
    jugés par le test suivant."""
    releve, ouvertures = endettement["releve"], endettement["ouvertures"]
    pire_levier, servis = 0.0, 0
    for t, p in enumerate(releve.pas):
        v, e = p["variables"], p["etat"]
        assert p["14"] > 0.0, t
        if v["v"] < v["y"] + ouvertures[t].IN_vol:
            servis += 1
            pire_levier = max(pire_levier, ecart(e.L / e.K, TABLE.lv_etoile))
    depots, forme = endettement["depots"], endettement["forme"]
    publier("Bloc 6, endettement, i_L + 2 points permanent (blocs 2 à 6 réels, taux exogène)", [
        f"levier : {pire_levier:.1e} rel. sur {servis} pas servis (seuil 1e−12) ; Div_F > 0 à "
        f"chaque pas ; D_F/(n_a PIB) au pas 2 159 : {depots:.9f}, forme fermée {forme:.9f}, "
        f"écart {ecart(depots, forme):.1e} (seuil 1e−6 ; verdict : test suivant)"])
    assert servis > 0 and pire_levier <= SEUIL_LEVIER


@pytest.mark.xfail(strict=True, reason=(
    "#139 : critère « Endettement » de la fiche 6 (dépôts au PIB à 1e−6 après 2 160 pas) non "
    "tenu sur le banc (b-x) sous i_L + 2 points permanent, convergence oscillante lente vers la "
    "forme fermée (P140) ; critère non déplacé, correction prospective réservée au mainteneur"))
def test_endettement_depots_sur_leur_forme_fermee_apres_2160_pas(endettement):
    """Fiche 6, § 9.6, « Endettement » (7 (d)), partie dépôts : D_F d'ouverture/(n_a PIB du pas)
    (convention de B12) sur sa forme fermée, ν_F p v^e/(p v + ΔIN) du script, qui ne lit pas le
    taux, à 1e−6 relatif après 2 160 pas. Non tenu (P140, issue #139) : échec attendu strict ; la
    correction prospective proposée par `macro` est réservée au mainteneur."""
    assert ecart(endettement["depots"], endettement["forme"]) <= SEUIL_DEPOTS


@pytest.fixture(scope="module")
def formes_fermees(socle):
    """Fiche 6, § 9.6, « Formes fermées » (b) : blocs 2 à 6 réels, taux exogène (blocs 7 et 8
    d'essai), Δϱ_L = +1 point permanent (i_L + 0,01 (1 + π*)), π* = 2 %, branches λ_ti × 0,5,
    × 1 et × 2, 24 000 pas : (tu, K^vol/(n_a y)) au dernier pas, et Δϱ effectif."""
    import dataclasses
    from nations.moteur.parametres import varier
    sentier = socle.sentier(0.02)
    reels = sans(socle, "banque", "banque_centrale")
    rendus = {}
    for facteur in (0.5, 1.0, 2.0):
        parametres = dataclasses.replace(PARAMETRES_DE_REFERENCE, investissement=varier(
            TABLE, lambda_ti=TABLE.lambda_ti.valeur * facteur))
        initial, releve = derouler(socle, sentier, NB_PAS_DES_FORMES_FERMEES, reels=reels,
                                   parametres=parametres,
                                   regles={"i_L": _taux_releve(socle, 0.01 * 1.02)})
        p = releve.pas[-1]
        ouverture = releve.pas[-2]["etat"]
        rendus[facteur] = {"tu": p["variables"]["tu"],
                           "x": ouverture.K_vol / (N_A * p["variables"]["y"]),
                           "d_rho": p["variables"]["varrho_L"] - initial.varrho_bar_L}
        del releve
    return rendus


def test_formes_fermees_sous_un_ecart_de_taux_permanent(formes_fermees, publier):
    """Fiche 6, § 9.6, « Formes fermées » (b), classe (b-x) : après 24 000 pas, tu sur
    t̄u e^{ζΔϱ} et K^vol/(n_a y) sur (κ/t̄u) e^{−ζΔϱ}, à 1e−6 relatif, dans chacune des branches
    λ_ti × 0,5, × 1 et × 2 (Δϱ effectif lu au dernier pas, i_L/(1 + π*) exact au point près)."""
    kappa = PARAMETRES_DE_REFERENCE.production.kappa
    lignes = []
    for facteur, m in formes_fermees.items():
        tu = TABLE.tu_bar * math.exp(TABLE.zeta * m["d_rho"])
        x = kappa / TABLE.tu_bar * math.exp(-TABLE.zeta * m["d_rho"])
        lignes.append(f"λ_ti × {facteur} : Δϱ = {m['d_rho']:.12f} ; tu {m['tu']:.10f} contre "
                      f"{tu:.10f} ({ecart(m['tu'], tu):.1e}) ; x {m['x']:.10f} contre {x:.10f} "
                      f"({ecart(m['x'], x):.1e})")
        assert ecart(m["tu"], tu) <= SEUIL_FORMES_FERMEES, facteur
        assert ecart(m["x"], x) <= SEUIL_FORMES_FERMEES, facteur
    publier("Bloc 6, formes fermées sous Δϱ = +1 point permanent, 24 000 pas (blocs 2 à 6 réels, "
            "taux exogène)", lignes)


def _carte_capital_et_part(facteur):
    """Boucle propre (7 (b)) : carte (K^vol, ti) ramenée au sentier, demande, prix et taux
    exogènes (y_t sur son sentier, Δϱ = 0), par S2, S3, S6 du bloc et N10, N11 ; π* = 2 %."""
    from nations.moteur.conversions import facteur_par_pas
    from nations.moteur.parametres import TauxDeCroissance
    kappa = PARAMETRES_DE_REFERENCE.production.kappa
    f_g = facteur_par_pas(TauxDeCroissance(0.02)) * facteur_par_pas(TauxDeCroissance(0.0))
    delta_pas = par_pas(TABLE.delta)
    lam = TABLE.lambda_ti.valeur * facteur / N_A
    y = 1.0  # y_t ramenée au sentier ; y_{t−1} = y/f_g

    def carte(K_vol, ti):
        tu = y / (K_vol * par_pas(TauxDeFlux(1.0 / kappa)))
        I_vol = bloc.plan_en_volume(ti, f_g, y / f_g, TABLE.eta_r, 0.0, 0.0)
        tu_etoile = bloc.utilisation_visee(TABLE.tu_bar, TABLE.zeta, 0.0, 0.0)
        return ((1.0 - delta_pas) * K_vol + I_vol) / f_g, bloc.part_visee_suivante(
            ti, lam, tu, tu_etoile)
    K0 = N_A * kappa * y / TABLE.tu_bar
    ti0 = (N_A * (f_g - 1.0) + TABLE.delta.valeur) * kappa / TABLE.tu_bar
    return carte, (K0, ti0)


def test_boucle_propre_du_capital_et_de_la_part_visee(publier):
    """Fiche 6, § 9.6, « Boucle propre » (7 (b)), classe (a) : demande, prix et taux exogènes,
    module dominant de la paire (K^vol, ti), par différences finies centrées (pas relatif 1e−6)
    de la carte ramenée au sentier ; < 1 à la calibration et pour λ_ti × 0,5 et × 2 ; demi-vie et
    période publiées (repères de la spécification : 0,99793 ; 0,99923 ; 0,9971 complexe)."""
    import numpy as np
    lignes = []
    for facteur in (0.5, 1.0, 2.0):
        carte, x0 = _carte_capital_et_part(facteur)
        point = np.array(x0)
        assert np.allclose(carte(*x0), x0, rtol=1e-12)
        j = np.zeros((2, 2))
        for k in range(2):
            h = 1e-6 * point[k]
            haut, bas = point.copy(), point.copy()
            haut[k] += h
            bas[k] -= h
            j[:, k] = (np.array(carte(*haut)) - np.array(carte(*bas))) / (2 * h)
        valeurs = np.linalg.eigvals(j)
        dominante = valeurs[np.argmax(abs(valeurs))]
        module = abs(dominante)
        demi_vie = math.log(0.5) / math.log(module)
        angle = abs(np.angle(dominante))
        periode = 2 * math.pi / angle if angle > 1e-12 else math.inf
        lignes.append(f"λ_ti × {facteur} : valeurs propres {np.round(valeurs, 6)} ; module "
                      f"{module:.5f} ; demi-vie {demi_vie:.0f} tours ; période {periode:.0f}")
        assert module < 1.0, facteur
    publier("Bloc 6, boucle propre (K^vol, ti), demande, prix et taux exogènes, π* = 2 %", lignes)


def test_hors_cible_durable(socle, publier):
    """Fiche 6, § 9.6, « Hors cible durable » (§ 9.7 (a)), classe (b-x) : prix exogènes sur le
    sentier à π̄ = 10 % (bloc d'essai 4, μ̃ = ln(p/UC)), cible π* = 2 % (état et bloc d'essai 8),
    i_L de Fisher à r = 1 % sur le sentier à 10 % (bloc d'essai 7), norme ϱ̄_L de l'état résolu
    à 2 % ; blocs 2, 3, 5 et 6 réels ; après 24 000 pas, tu et x = K^vol/(n_a y) sur t̄u e^{ζΔϱ}
    et (κ/t̄u) e^{−ζΔϱ} à 1e−6 relatif, Δϱ = ϱ_L − ϱ̄_L (7,92 points attendus)."""
    import dataclasses
    sentier = socle.sentier(0.10)
    norme = socle.sentier(0.02).o["rho_bar_L"]
    reels = sans(socle, "prix", "banque", "banque_centrale")
    initial = dataclasses.replace(socle.etat_initial(sentier), pi_etoile=0.02,
                                  varrho_bar_L=norme)
    options = socle.prix_exogene_marge_identite()
    _, releve = derouler(socle, sentier, NB_PAS_DES_FORMES_FERMEES, initial=initial, reels=reels,
                         **options)
    p = releve.pas[-1]
    d_rho = p["variables"]["varrho_L"] - norme
    kappa = PARAMETRES_DE_REFERENCE.production.kappa
    tu = TABLE.tu_bar * math.exp(TABLE.zeta * d_rho)
    x = kappa / TABLE.tu_bar * math.exp(-TABLE.zeta * d_rho)
    x_moteur = releve.pas[-2]["etat"].K_vol / (N_A * p["variables"]["y"])
    publier("Bloc 6, hors cible durable (π̄ = 10 %, π* = 2 %, prix exogènes), 24 000 pas", [
        f"Δϱ = {d_rho:.6f} ; tu {p['variables']['tu']:.10f} contre {tu:.10f} "
        f"({ecart(p['variables']['tu'], tu):.1e}) ; x {x_moteur:.10f} contre {x:.10f} "
        f"({ecart(x_moteur, x):.1e})"])
    assert ecart(p["variables"]["tu"], tu) <= SEUIL_FORMES_FERMEES
    assert ecart(x_moteur, x) <= SEUIL_FORMES_FERMEES


def test_depassement_de_l_exponentielle_refuse_par_le_moteur(socle):
    """P139 : au pas, un dépassement de l'exponentielle de S2 (ζ (ϱ_L − ϱ̄_L) > 709, ici
    i_{L,0} = 1 000 par an, hors de tout domaine plausible mais fini) arrête le pas par
    `DepassementNumerique`, refus typé du moteur qui nomme le pas, la phase 2 et le bloc
    investissement, et non par une `OverflowError` nue."""
    import dataclasses
    from nations.moteur import ordonnanceur as ordo
    from nations.moteur.diagnostics import DepassementNumerique
    sentier = socle.sentier(0.02)
    initial = dataclasses.replace(socle.etat_initial(sentier), i_L=1000.0)
    o = socle.ordonnanceur(sentier, reels=socle.blocs_reels())
    with pytest.raises(DepassementNumerique) as refus:
        ordo.executer_pas(initial, socle.ENTREES_SANS_SCENARIO, o, Releve())
    assert (refus.value.t, refus.value.etape, refus.value.bloc) == (0, "2", "investissement")
