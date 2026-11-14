"""Bloc 4, prix, dans le socle partiel d'essai : lignes « J3 » de classe (b) et tests de P54 (#51).

Classe (b) du classement du rang 1a de J3-b (synthèse en commentaire de la PR
#117, § 1) : état stationnaire (ξ en écart absolu, P66) ; T2 (b) sur les blocs
2 à 4 réels (P56) ; vitesses ; phases ; identité P15 (deux prix distants de
1 %) ; stationnarité partielle B1 à B7, B12, B13, B24 et ξ (P66, P67) ; la
ligne « Coût » est tenue par `tests/invariants/test_budget.py` (P57), qui
mesure tout bloc réel de `src/nations/blocs/`.

**Tests imposés par le visa de `macro` sur P54** (synthèse du rang 1a, § 4) :
- une **implémentation de référence de l'option (i)**, fonction pure de ce
  module (`reference_option_i`), écrite sans les fonctions du moteur : T2 avec
  pr_{t−1} = pr_t (1 + g_pr)^{−1/n_a} et P_{t−1} lu au registre, P2 avec
  ln(P_{t−1}/UC_{t−1}) ; évaluée sur l'état d'ouverture de chaque pas de la
  trajectoire du moteur, elle est comparée à W_t, μ̃_t et p_t du moteur à
  1e−12 sur 720 pas, aux trois π*, avec un choc G + 1 % aux tours 1 à 12, aux
  vitesses des blocs 2 à 4 de la calibration, × 0,5 et × 2 ;
- l'**invariant à chaque pas** |μ̃_t − ln(p_t/UC_t)| ≤ 1e−12, sur les mêmes
  trajectoires ;
- à l'ouverture, μ̃ = ln(1 + μ̄) (état initial du socle, tiré d'`ouverture` du
  script).

Le test d'alternance étendu est en classe (c), renvoyé à #114 ; sa pré-mesure à
m = 0 (plans nominaux exogènes) est publiée ici sans verdict.

Les blocs réels de la production (#113), du travail (#50) et des prix
remplacent les blocs d'essai de leur radical ; les cinq autres sont des blocs
d'essai sur le sentier. **Étiquettes** : toute mesure dynamique porte « plans
nominaux exogènes » et l'étiquette du socle (`socle_partiel.ETIQUETTE`) ; elle ne vaut pas
verdict de boucle fermée ni de boucle conjointe T3 ↔ BC3.
"""

import dataclasses
import math

import pytest

from nations.blocs.prix import Prix
from nations.blocs.production import Production
from nations.blocs.travail import Travail
from nations.moteur import ordonnanceur as ordo
from nations.moteur.contrat_bloc import Lecture
from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres import varier
from nations.moteur.parametres.cadre import CADRE, PAS_PAR_AN
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas
from nations.observation.residus import ReleveDesResidus

N_A = PAS_PAR_AN.valeur
NB_PAS = 720
# Seuils écrits avant l'essai (fiche 4, § 9.6 ; fiche 3, § 9.6 pour T2 ; P54, P66, P67).
SEUIL_UN_PAS = 1e-10
SEUIL_720_PAS = 1e-9
SEUIL_NUL = 1e-12
SEUIL_T2 = 1e-10
SEUIL_VITESSES = 1e-6
SEUIL_P54 = 1e-12
EPS = CADRE.tolerance_identite_pas
EPS_V = CADRE.tolerance_identite_cumulee
REGLES_PAR_PAS = ("eq:noyau-somme-ligne", "eq:noyau-somme-colonne", "eq:noyau-cloture-poste",
                  "eq:noyau-variation-monnaie", "eq:noyau-variation-monnaie-centrale")
VITESSES = {"production": ("lambda_v", "lambda_IN"), "travail": ("lambda_w", "lambda_N"),
            "prix": ("lambda_mu",)}


def etiquettes(socle):
    """Étiquettes des mesures dynamiques : plans nominaux exogènes, étiquette du socle à
    bloc d'essai 8 (`socle.ETIQUETTE`, jamais écrite en dur)."""
    return f"plans nominaux exogènes ; {socle.ETIQUETTE}"


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


class Double:
    def __init__(self, *observateurs):
        self.observateurs = observateurs

    def relever(self, e):
        for observateur in self.observateurs:
            observateur.relever(e)


def ecart(x, reference):
    """|x/x̄ − 1| ; pour une valeur résolue nulle, |x| (P66)."""
    return abs(x) if reference == 0.0 else abs(x / reference - 1.0)


def ordonnanceur(socle, sentier, parametres=None, reels=None, **options):
    """Socle partiel où les blocs réels 2 à 4 remplacent leurs blocs d'essai."""
    parametres = socle.PARAMETRES_DE_REFERENCE if parametres is None else parametres
    reels = (Production(), Travail(), Prix()) if reels is None else reels
    return socle.ordonnanceur(sentier, parametres, reels=reels, **options)


def derouler(socle, sentier, nb_pas, initial=None, observateur=None, **options):
    releve = Releve()
    initial = socle.etat_initial(sentier) if initial is None else initial
    o = releve if observateur is None else Double(releve, observateur)
    socle.derouler(initial, nb_pas, ordonnanceur(socle, sentier, **options), o)
    return initial, releve


def chocs_g(facteur, debut, fin):
    def chocs(nom, t):
        return facteur if nom == "G_plan" and debut <= t <= fin else 1.0
    return chocs


def parametres_aux_vitesses(socle, facteur):
    """Tables du moteur aux vitesses des blocs 2 à 4 multipliées par `facteur` (constructeur
    validé)."""
    p = socle.PARAMETRES_DE_REFERENCE
    tables = {}
    for radical, noms in VITESSES.items():
        table = getattr(p, radical)
        tables[radical] = varier(table, **{n: facteur * getattr(table, n).valeur for n in noms})
    return dataclasses.replace(p, **tables)


@pytest.fixture(scope="module")
def trajectoires(socle):
    """Une trajectoire de 720 pas par π*, depuis l'état résolu, sans choc, blocs 2 à 4 réels."""
    return {pi: (socle.sentier(pi),) + derouler(socle, socle.sentier(pi), NB_PAS)
            for pi in socle.POINTS_PI}


# --------------------------------------------------------------------------
# P54 : implémentation de référence de l'option (i) ; invariant de μ̃
# --------------------------------------------------------------------------


def reference_option_i(o, parametres):
    """Option (i) de P54, fonction pure, sans les fonctions du moteur : à partir de l'état
    d'ouverture `o` du pas t et des tables, rend (W_t, μ̃_t, p_t) par T2 (pr_{t−1} =
    pr_t (1 + g_pr)^{−1/n_a}, P_{t−1} dernier prix connu du registre), T3, N2, N8 (UC),
    P1, P2 (ln(P_{t−1}/UC_{t−1}), UC_{t−1} = W_{t−1}/pr_{t−1}) et P3."""
    n = parametres.cadre.pas_par_an
    production, travail, prix = parametres.production, parametres.travail, parametres.prix
    g_pr = production.g_pr.valeur
    pr_prec = o.pr * (1.0 + g_pr) ** (-1.0 / n)
    P_prec = o.registre_prix[0]
    omega = o.W / (P_prec * pr_prec)  # T2, option (i)
    omega_etoile = 1.0 / (1.0 + prix.mu_bar)
    ln_W = (math.log(o.W) + (math.log(1.0 + g_pr) + math.log(1.0 + o.pi_e)) / n
            + travail.lambda_w.valeur / n
            * (math.log(omega_etoile / omega) - travail.beta * (o.U - travail.U_eq)))  # T3
    W = math.exp(ln_W)
    UC = W / o.pr  # N8
    xi = 1.0 - o.IN_vol / (n * production.sigma * o.v_e)  # P1, N2
    UC_prec = o.W / pr_prec
    lam = prix.lambda_mu.valeur / n
    mu = ((1.0 - lam) * math.log(P_prec / UC_prec)
          + lam * (math.log(1.0 + prix.mu_bar) + prix.psi_xi * xi))  # P2, option (i)
    return W, mu, UC * math.exp(mu)  # P3


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_p54_option_i_de_reference_et_invariant_de_mu(socle, pi, publier):
    """P54 (visa de `macro`) : sur 720 pas, choc G + 1 % aux tours 1 à 12, vitesses des blocs
    2 à 4 × 1, × 0,5 et × 2 : (1) l'option (i) de référence, évaluée sur l'ouverture de chaque
    pas, égale W_t et p_t du moteur à 1e−12 relatif et μ̃_t à 1e−12 en absolu ; (2) invariant
    |μ̃_t − ln(p_t/UC_t)| ≤ 1e−12 à chaque pas ; (3) μ̃ = ln(1 + μ̄) à l'ouverture du pas 0."""
    sentier = socle.sentier(pi)
    lignes = []
    for facteur in (1.0, 0.5, 2.0):
        parametres = parametres_aux_vitesses(socle, facteur)
        initial, releve = derouler(socle, sentier, NB_PAS, parametres=parametres,
                                   chocs_des_plans=chocs_g(1.01, 1, 12))
        assert initial.mu_tilde == math.log(1.0 + parametres.prix.mu_bar)
        ouvertures = [initial] + [p["etat"] for p in releve.pas[:-1]]
        pires = dict.fromkeys(("W", "μ̃", "p", "invariant"), 0.0)
        for o, p in zip(ouvertures, releve.pas, strict=True):
            v = p["variables"]
            W, mu, prix = reference_option_i(o, parametres)
            pires["W"] = max(pires["W"], ecart(v["W_suivant"], W))
            pires["μ̃"] = max(pires["μ̃"], abs(v["mu_tilde_suivant"] - mu))
            pires["p"] = max(pires["p"], ecart(v["p"], prix))
            pires["invariant"] = max(pires["invariant"],
                                     abs(v["mu_tilde_suivant"] - math.log(v["p"] / v["UC"])))
        # Le choc a bien écarté la marge de sa valeur normale (garde de l'essai).
        assert abs(releve.pas[13]["variables"]["mu_tilde_suivant"] - initial.mu_tilde) > 1e-5
        for nom, x in pires.items():
            assert x <= SEUIL_P54, (facteur, nom, x)
        lignes.append(f"vitesses × {facteur:g} : " + " ; ".join(
            f"{n} {x:.1e}" for n, x in pires.items()))
    publier(f"Bloc 4, P54 : option (i) de référence et invariant de μ̃, π* = {100 * pi:g} %, "
            f"choc G + 1 % aux tours 1 à 12, 720 pas ({etiquettes(socle)})",
            lignes + ["W, p : écart relatif ; μ̃, invariant : écart absolu (seuil 1e−12)"])


# --------------------------------------------------------------------------
# État stationnaire, T2 (b), stationnarité partielle
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_un_pas_depuis_l_etat_resolu(trajectoires, socle, pi, publier):
    """Fiche 4, § 9.6, « État stationnaire » : un pas sans choc depuis l'état résolu laisse
    μ̃ = ln(1 + μ̄) et p en hausse de (1 + π̄)^{1/n_a} à 1e−10 relatif, ξ = 0 à 1e−10 en
    absolu ; P = p au bit."""
    sentier, initial, releve = trajectoires[pi]
    v = releve.pas[0]["variables"]
    mu_bar = socle.PARAMETRES_DE_REFERENCE.prix.mu_bar
    ecarts = {"μ̃": ecart(v["mu_tilde_suivant"], math.log(1.0 + mu_bar)),
              "p": ecart(v["p"] / initial.registre_prix[0], (1.0 + pi) ** (1.0 / N_A)),
              "ξ (absolu)": abs(v["xi"])}
    for nom, x in ecarts.items():
        assert x <= SEUIL_UN_PAS, (nom, x)
    assert v["P"] == v["p"]
    publier(f"Bloc 4, un pas depuis l'état résolu, π* = {100 * pi:g} % ({etiquettes(socle)})", [
        " ; ".join(f"{n} {x:.1e}" for n, x in ecarts.items()) + " (seuil 1e−10)"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_t2_b_dernier_prix_connu(trajectoires, socle, pi, publier):
    """Fiche 3, § 9.6, T2 (b), et fiche 4, § 9.6, T2, correction prospective P56 (n_a = 12) :
    blocs 2 à 4 réels, plans nominaux exogènes sur le sentier : après un pas, W et p sur leur
    sentier à 1e−10 relatif ; après 720 pas, |U − U^eq|/U^eq ≤ 1e−10."""
    sentier, _, releve = trajectoires[pi]
    v0 = releve.pas[0]["variables"]
    ecarts = {"W (pas 1)": ecart(v0["W_suivant"], socle.valeur_d_ouverture(sentier, "W", 1)),
              "p (pas 1)": ecart(v0["p"], sentier.valeur("p", socle.PRIX, 0)),
              "U (pas 720)": ecart(releve.pas[-1]["etat"].U,
                                   socle.PARAMETRES_DE_REFERENCE.travail.U_eq)}
    for nom, x in ecarts.items():
        assert x <= SEUIL_T2, (nom, x)
    publier(f"Blocs 3 et 4, T2 (b), π* = {100 * pi:g} % ({etiquettes(socle)} ; blocs 2 à 4 réels)", [
        " ; ".join(f"{n} {x:.1e}" for n, x in ecarts.items()) + " (seuil 1e−10)"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_variables_d_etat_sur_leur_sentier_720_pas(trajectoires, socle, pi):
    """Les variables d'état des blocs 2 à 4 restent sur leur sentier à 1e−9 relatif sur 720
    pas (critère de #112 étendu aux blocs réels)."""
    sentier, _, releve = trajectoires[pi]
    noms = ("v_e", "IN_vol", "pr", "K_vol", "W", "U", "N", "N_pa", "mu_tilde")
    for t, p in enumerate(releve.pas):
        for nom in noms:
            assert ecart(getattr(p["etat"], nom),
                         socle.valeur_d_ouverture(sentier, nom, t + 1)) <= SEUIL_720_PAS, nom


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_stationnarite_partielle(trajectoires, socle, pi, publier):
    """P67 : max sur 720 pas de |x_t/x̄ − 1| ≤ 1e−9 pour B1 à B7, B12, B13 et B24, blocs 2 à 4
    réels, depuis l'état résolu, sans choc ; B4 à B7, B13 et B24 dès le pas 11 (D13) ; P66 :
    une grandeur de valeur résolue nulle (B7 à π* = 0, ξ) se juge en valeur absolue,
    |x_t| ≤ 1e−12. Relèvent du bloc 4 : B6 (marge), B7 (glissement) et ξ ; B12 et B13 lisent
    p et le PIB."""
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
    assert (resolues["B7"] == 0.0) == (pi == 0.0)
    publier(f"Bloc 4, stationnarité partielle (P67), π* = {100 * pi:g} %, 720 pas "
            f"({etiquettes(socle)} ; blocs 2 à 4 réels)",
            ["max |x_t/x̄ − 1| (|x_t| si x̄ = 0, P66) : "
             + " ; ".join(f"{c} {x:.1e}" for c, x in pires.items())])


# --------------------------------------------------------------------------
# Vitesses ; identité P15
# --------------------------------------------------------------------------


def test_vitesses_ne_determinent_pas_l_etat_d_arrivee(socle, publier):
    """Fiche 4, § 9.6, « Vitesses » (réserve 2) : G + 1 % aux tours 1 à 12 ; branches λ_μ × 0,5
    et × 2 (constructeur validé) ; après 720 pas, l'écart relatif de la marge p/UC − 1 et de
    ΣWB/ΣVA (12 derniers tours) entre les deux branches est d'au plus 1e−6, et celui de ξ, de
    valeur résolue nulle, d'au plus 1e−6 en absolu (P66)."""
    sentier = socle.sentier(0.02)
    p = socle.PARAMETRES_DE_REFERENCE
    finales = {}
    for facteur in (0.5, 2.0):
        table = varier(p.prix, lambda_mu=facteur * p.prix.lambda_mu.valeur)
        _, releve = derouler(socle, sentier, NB_PAS, parametres=dataclasses.replace(
            p, prix=table), chocs_des_plans=chocs_g(1.01, 1, 12))
        v = releve.pas[-1]["variables"]
        fenetre = releve.pas[-N_A:]
        finales[facteur] = {"marge": v["p"] / v["UC"] - 1.0,
                            "ΣWB/ΣVA": sum(q["5"] for q in fenetre)
                            / sum(q["1"] + q["2"] + q["3"] + q["4"] for q in fenetre),
                            "ξ": v["xi"]}
        assert abs(releve.pas[13]["variables"]["xi"]) > 1e-4  # le choc a écarté ξ de 0
    ecarts = {"marge": ecart(finales[0.5]["marge"], finales[2.0]["marge"]),
              "ΣWB/ΣVA": ecart(finales[0.5]["ΣWB/ΣVA"], finales[2.0]["ΣWB/ΣVA"]),
              "ξ (absolu)": abs(finales[0.5]["ξ"] - finales[2.0]["ξ"])}
    for nom, x in ecarts.items():
        assert x <= SEUIL_VITESSES, (nom, x)
    publier(f"Bloc 4, vitesses λ_μ × 0,5 et × 2 après un choc G + 1 % sur 12 tours "
            f"({etiquettes(socle)})", ["écart après 720 pas : "
                                + " ; ".join(f"{n} {x:.1e}" for n, x in ecarts.items())
                                + " (seuil 1e−6)"])


def test_identite_p15_deux_prix_distants_de_un_pour_cent(socle, publier):
    """Fiche 4, § 9.6, « Identité » (cas P15) : deux pas 0 dont les prix sont distants de 1 %
    (μ̃ d'ouverture relevée de Δ = ln(1,01)/(1 − λ_μ/n_a + λ_w/n_a), qui relève μ̃_0 de
    (1 − λ_μ/n_a)Δ par P2 et ln W_0 de (λ_w/n_a)Δ par T2 et T3) : dans les deux, les identités
    du noyau tiennent à ε × S (lignes, colonnes, clôtures, monnaie, identité cumulée), la somme des
    soldes financiers des cinq secteurs est nulle et la valeur nette des entreprises est égale
    par les flux et par le stock, à 1e−12 × S."""
    sentier = socle.sentier(0.02)
    base = socle.etat_initial(sentier)
    p = socle.PARAMETRES_DE_REFERENCE
    lam_mu, lam_w = p.prix.lambda_mu.valeur / N_A, p.travail.lambda_w.valeur / N_A
    releve_prix = {}
    lignes = []
    for nom, initial in (("sentier", base), ("+1 %", dataclasses.replace(
            base, mu_tilde=base.mu_tilde + math.log(1.01) / (1.0 - lam_mu + lam_w)))):
        residus = ReleveDesResidus()
        _, releve = derouler(socle, sentier, 1, initial=initial, observateur=residus)
        apres = releve.pas[0]["etat"]
        releve_prix[nom] = releve.pas[0]["variables"]["p"]
        for regle in REGLES_PAR_PAS:
            assert residus.maximum(regle)[0] <= EPS, (nom, regle)
        assert residus.maximum("eq:noyau-tolerance-cumulee")[0] <= EPS_V, nom
        positions = {q: getattr(apres, q) for q in cat.NOMS_POSTES}
        ouverture = {q: getattr(initial, q) for q in cat.NOMS_POSTES}
        echelles = [idt.echelle_bilan(positions, s) for s in cat.SECTEURS]
        S = min(x for x in echelles if x > 0.0)
        reels = (positions["K"] - ouverture["K"]) + (positions["IN"] - ouverture["IN"])
        soldes = sum(getattr(apres, cat.VALEUR_NETTE_FLUX[s])
                     - getattr(initial, cat.VALEUR_NETTE_FLUX[s]) for s in cat.SECTEURS) - reels
        entreprises = abs(getattr(apres, cat.VALEUR_NETTE_FLUX["entreprises"])
                          - idt.valeur_nette_stock(positions, "entreprises")) \
            / idt.echelle_bilan(positions, "entreprises")
        assert abs(soldes) / S <= SEUIL_NUL and entreprises <= SEUIL_NUL, (nom, soldes, entreprises)
        lignes.append(f"{nom} : |Σ soldes|/S_min {abs(soldes) / S:.1e} ; "
                      f"|V_F flux − V_F stock|/S_F {entreprises:.1e}")
    assert abs(releve_prix["+1 %"] / releve_prix["sentier"] / 1.01 - 1.0) <= 1e-12
    publier(f"Bloc 4, identité P15, deux prix distants de 1 % au pas 0 ({etiquettes(socle)})",
            lignes + ["seuil 1e−12 × S"])


# --------------------------------------------------------------------------
# Phases : aucune lecture hors ordre (refus de l'assemblage)
# --------------------------------------------------------------------------


def _fautif(lecture):
    """Bloc des prix dont le siège déclare en plus la lecture `lecture`."""
    sieges = tuple(dataclasses.replace(s, lit=s.lit + (lecture,)) for s in Prix.declaration.sieges)
    declaration = dataclasses.replace(Prix.declaration, sieges=sieges)
    return type("PrixFautif", (Prix,), {"__slots__": (), "declaration": declaration})()


@pytest.mark.parametrize("lecture, motif", [
    # Les ventes du pas : écrites par le bloc 2 après le bloc prix (groupe suivant).
    (Lecture("5", "v"), "« v » : triangularité"),
    # Un volume servi : idem.
    (Lecture("5", "C_vol"), "« C_vol » : triangularité"),
    # W_t : la phase 1 n'est pas dans la colonne « Lisent » de la phase 5.
    (Lecture("1", "W_suivant"), "« W_suivant » : phase 1 hors de la colonne « Lisent »"),
])
def test_phases_lecture_hors_ordre_refusee(socle, lecture, motif):
    """Fiche 4, § 9.6, « Phases » : la déclaration du bloc est acceptée par `assembler` ; une
    lecture hors ordre ajoutée au siège est refusée (`DefautDeDeclaration`), avant tout pas."""
    sentier = socle.sentier(0.02)
    ordonnanceur(socle, sentier)
    blocs = socle.blocs(sentier, reels=(Production(), Travail(), _fautif(lecture)))
    with pytest.raises(DefautDeDeclaration, match=motif):
        ordo.assembler(socle.PHASES, blocs, socle.PARAMETRES_DE_REFERENCE, socle.SANS_ENTREES)


# --------------------------------------------------------------------------
# Pré-mesure de l'alternance étendue (classe (c), #114), sans verdict
# --------------------------------------------------------------------------


def changements_de_signe(serie, seuil=1e-12):
    signes = [math.copysign(1.0, x) for x in serie if abs(x) > seuil]
    return sum(1 for a, b in zip(signes, signes[1:]) if a != b)


def test_pre_mesure_de_l_alternance_sans_verdict(socle, publier):
    """Fiche 4, § 9.6, « Alternance étendue », classe (c) (renvoyée à #114) : pré-mesure à m = 0
    (plans nominaux exogènes), publiée sans verdict : G + 1 % au seul tour 1 ; sur les tours 2
    à 13, changements de signe de (a) l'écart de ln p au sentier sans choc et (b) l'écart de la
    variation mensuelle Δln p, |x| ≤ 1e−12 ignorées. Seule assertion : le choc a écarté le
    prix."""
    sentier = socle.sentier(0.02)
    _, base = derouler(socle, sentier, 14)
    _, choc = derouler(socle, sentier, 14, chocs_des_plans=chocs_g(1.01, 1, 1))
    ln_b = [math.log(p["variables"]["p"]) for p in base.pas]
    ln_c = [math.log(p["variables"]["p"]) for p in choc.pas]
    niveau = [ln_c[t] - ln_b[t] for t in range(2, 14)]
    variation = [(ln_c[t] - ln_c[t - 1]) - (ln_b[t] - ln_b[t - 1]) for t in range(2, 14)]
    assert max(abs(x) for x in niveau) > 1e-6
    publier(f"Bloc 4, alternance étendue, pré-mesure à m = 0, sans verdict ({etiquettes(socle)})", [
        f"changements de signe sur les tours 2 à 13 : (a) niveau {changements_de_signe(niveau)} ; "
        f"(b) variation mensuelle {changements_de_signe(variation)} (maquette de la synthèse du "
        "rang 1a : (a) 0 et (b) 1) ; renvoyé à #114 pour le verdict"])
