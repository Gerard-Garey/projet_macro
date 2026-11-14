"""Bloc 2, production et stocks, dans le socle partiel d'essai : lignes « J3 » de classe (b) (#113).

Classe (b) du classement du rang 1a de J3-b (synthèse en commentaire de la PR
#117, § 1) : état stationnaire ; vitesses (critère 4) ; délai ; identité de
volume ; disponibilité ; valorisation (P73) ; phases ; stationnarité partielle
B1, B2 et B24 (P67) ; la ligne « Coût » est tenue par
`tests/invariants/test_budget.py` (P57), qui mesure tout bloc réel de
`src/nations/blocs/`. Seuils écrits avant l'essai (fiche 2, § 9.6, précision
du 13/11/2026 ; issue #113), non déplacés.

Le bloc réel `nations.blocs.production.Production` remplace le bloc d'essai de
son radical (`socle.blocs(..., reels=...)`) ; les sept autres blocs sont des
blocs d'essai sur le sentier. **Étiquettes** : toute mesure dynamique porte
« plans nominaux exogènes » et l'étiquette du socle (`socle_partiel.ETIQUETTE`) ; elle ne vaut
pas verdict de boucle fermée (S1, #114). Les lignes « Délai » et « Vitesses »
font suivre à l'emploi la demande de travail (règle d'essai du bloc travail,
N = N*, hypothèse de la boucle propre, `sec:production-conditions` ; masse
salariale de la ligne 5 restée au montant du sentier) : avec
l'emploi du sentier, la technique y ≤ pr·N plafonnerait la production au
sentier et aucune hausse ne serait observable.
"""

import dataclasses
import math

import pytest

from nations.blocs.production import Production
from nations.moteur import ordonnanceur as ordo
from nations.moteur.contrat_bloc import Lecture
from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres import varier
from nations.moteur.parametres.cadre import PAS_PAR_AN
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas

N_A = PAS_PAR_AN.valeur
NB_PAS = 720
# Seuils écrits avant l'essai (fiche 2, § 9.6 ; P67, P73).
SEUIL_UN_PAS = 1e-10
SEUIL_720_PAS = 1e-9
SEUIL_IDENTITE = 1e-12
SEUIL_VALORISATION = 1e-12
SEUIL_VITESSES = 1e-6
PREMIER_PAS_SUR_12_TOURS = N_A - 1
VARIABLES_DU_BLOC = ("v_e", "IN_vol", "pr", "K_vol")


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


def ecart(x, reference):
    return abs(x / reference - 1.0)


def ordonnanceur(socle, sentier, parametres=None, **options):
    """Socle partiel d'essai où le bloc réel de la production remplace son bloc d'essai."""
    parametres = socle.PARAMETRES_DE_REFERENCE if parametres is None else parametres
    return socle.ordonnanceur(sentier, parametres, reels=(Production(),), **options)


def emploi_egal_a_la_demande(socle):
    """Règle d'essai du bloc travail : N_t = N*_t (lu en phase 4, écrit par le bloc 2 en phase
    2), déclaration d'essai complétée de cette lecture."""
    propre = socle.declaration_d_essai("travail")
    sieges = tuple(dataclasses.replace(s, lit=s.lit + (Lecture("2", "N_etoile"),))
                   if s.etape == "4" else s for s in propre.sieges)
    return {"declarations": {"travail": dataclasses.replace(propre, sieges=sieges)},
            "regles": {"N": lambda vue, sentier, t: vue.lire("N_etoile")}}


def derouler(socle, sentier, nb_pas, initial=None, **options):
    releve = Releve()
    initial = socle.etat_initial(sentier) if initial is None else initial
    socle.derouler(initial, nb_pas, ordonnanceur(socle, sentier, **options), releve)
    return initial, releve


def ouvertures(initial, releve):
    """États d'ouverture des pas 0 à nb_pas (le dernier : clôture du dernier pas)."""
    return [initial] + [p["etat"] for p in releve.pas]


@pytest.fixture(scope="module")
def trajectoires(socle):
    """Une trajectoire de 720 pas par π*, depuis l'état résolu, sans choc, bloc réel."""
    return {pi: (socle.sentier(pi),) + derouler(socle, socle.sentier(pi), NB_PAS)
            for pi in socle.POINTS_PI}


# --------------------------------------------------------------------------
# État stationnaire : un pas, puis 720 pas (classe (b))
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_un_pas_depuis_l_etat_resolu(trajectoires, socle, pi, publier):
    """Fiche 2, § 9.6, « État stationnaire » : un pas sans choc depuis l'état résolu laisse v^e,
    IN^vol, IN, pr et K^vol sur leur sentier à 1e−10 relatif ; IN/(UC IN^vol) = ρ̄_IN à 1e−10
    à l'ouverture des pas 0 et 1 (UC du pas lu en phase 2)."""
    sentier, initial, releve = trajectoires[pi]
    apres = releve.pas[0]["etat"]
    ecarts = {nom: ecart(getattr(apres, nom), socle.valeur_d_ouverture(sentier, nom, 1))
              for nom in VARIABLES_DU_BLOC}
    ecarts["IN"] = ecart(apres.IN, socle.position_d_ouverture(sentier, "IN", 1))
    rho = sentier.e["rho_IN"]
    for t, etat in enumerate((initial, apres)):
        uc = releve.pas[t]["variables"]["UC"]
        ecarts[f"rho_IN (pas {t})"] = ecart(etat.IN / (uc * etat.IN_vol), rho)
    for nom, x in ecarts.items():
        assert x <= SEUIL_UN_PAS, (nom, x)
    publier(f"Bloc 2, un pas depuis l'état résolu, π* = {100 * pi:g} % ({etiquettes(socle)})", [
        "|x_1/x̄_1 − 1| : " + " ; ".join(f"{n} {x:.1e}" for n, x in ecarts.items())
        + " (seuil 1e−10)"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_variables_du_bloc_sur_leur_sentier_720_pas(trajectoires, socle, pi):
    """Les quatre variables d'état du bloc et la position IN restent sur leur sentier à 1e−9
    relatif sur 720 pas (critère de #112 étendu au bloc réel)."""
    sentier, _, releve = trajectoires[pi]
    for t, p in enumerate(releve.pas):
        for nom in VARIABLES_DU_BLOC:
            assert ecart(getattr(p["etat"], nom),
                         socle.valeur_d_ouverture(sentier, nom, t + 1)) <= SEUIL_720_PAS
        assert ecart(p["etat"].IN, socle.position_d_ouverture(sentier, "IN", t + 1)) \
            <= SEUIL_720_PAS


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_stationnarite_partielle_b1_b2_b24(trajectoires, socle, pi, publier):
    """P67 : B1 (stock d'ouverture rapporté aux ventes du pas), B2 (taux d'utilisation y/y^cap)
    et B24 (glissement annuel de la production, dès le pas 11, D13) à 1e−9 relatif de leurs
    valeurs résolues sur 720 pas, depuis l'état résolu, sans choc."""
    sentier, initial, releve = trajectoires[pi]
    resolues = socle.script().valeurs(sentier.e, sentier.par)
    reference = {"B1": resolues["IN_sur_v"], "B2": resolues["tu"], "B24": sentier.e["g"]}
    etats = ouvertures(initial, releve)
    pires = dict.fromkeys(reference, 0.0)
    for t, p in enumerate(releve.pas):
        v = p["variables"]
        pires["B1"] = max(pires["B1"], ecart(etats[t].IN_vol / v["v"], reference["B1"]))
        pires["B2"] = max(pires["B2"], ecart(v["y"] / v["y_cap"], reference["B2"]))
        if t >= PREMIER_PAS_SUR_12_TOURS:
            y0 = (releve.pas[t - N_A]["variables"]["y"] if t >= N_A
                  else float(sentier.o["y_m1"]))
            pires["B24"] = max(pires["B24"], ecart(v["y"] / y0 - 1.0, reference["B24"]))
    for cle, x in pires.items():
        assert x <= SEUIL_720_PAS, (cle, x)
    publier(f"Bloc 2, stationnarité partielle (P67), π* = {100 * pi:g} %, 720 pas ({etiquettes(socle)})",
            ["max |x_t/x̄ − 1| : " + " ; ".join(f"{c} {x:.1e}" for c, x in pires.items())
             + " (seuil 1e−9)"])


# --------------------------------------------------------------------------
# Identité de volume, valorisation (P73)
# --------------------------------------------------------------------------


def _identite_et_valorisation(initial, releve):
    """Plus grands écarts : identité de volume |y − v − ΔIN^vol| / y ; valorisation
    |IN_{t+1} − cm_t IN^vol_{t+1}| / (IN_t + UC_t y_t) ; et IN_{t+1} − IN_t égal au bit à la
    ligne 4 exécutée."""
    etats = ouvertures(initial, releve)
    pire_volume = pire_valeur = 0.0
    for t, p in enumerate(releve.pas):
        o, s, v = etats[t], etats[t + 1], p["variables"]
        pire_volume = max(pire_volume, abs(v["y"] - v["v"] - (s.IN_vol - o.IN_vol)) / v["y"])
        cm = (o.IN + v["UC"] * v["y"]) / (o.IN_vol + v["y"])
        pire_valeur = max(pire_valeur, abs(s.IN - cm * s.IN_vol) / (o.IN + v["UC"] * v["y"]))
        assert s.IN == o.IN + p["4"], t  # IN ne varie que par la ligne 4
    return pire_volume, pire_valeur


def chocs_g(facteur, debut, fin):
    def chocs(nom, t):
        return facteur if nom == "G_plan" and debut <= t <= fin else 1.0
    return chocs


def test_identite_de_volume_et_valorisation(trajectoires, socle, publier):
    """Fiche 2, § 9.6 : identité de volume y = v + (IN^vol_{t+1} − IN^vol_t) à 1e−12 relatif ;
    valorisation, IN ne varie que par la ligne 4 (au bit) et IN_{t+1} = cm_t IN^vol_{t+1} à
    1e−12 rapporté à IN_t + UC_t y_t (P73) ; sur les trois trajectoires sans choc et sous un
    choc G de ± 1 % aux pas 1 à 12 (emploi égal à la demande de travail, masse salariale du
    sentier ; à + 5 %, la caisse de l'État, plans d'essai exogènes, passe sous zéro au pas 4 et
    le noyau arrête, dès + 2 % au pas 10 ; un choc négatif n'arrête rien : limite du socle
    d'essai, renvoyée à #114)."""
    lignes = []
    cas = {f"π* = {100 * pi:g} %": (initial, releve)
           for pi, (_, initial, releve) in trajectoires.items()}
    sentier = socle.sentier(0.02)
    for facteur in (1.01, 0.99):
        cas[f"choc G × {facteur:g}"] = derouler(socle, sentier, 120,
                                                chocs_des_plans=chocs_g(facteur, 1, 12),
                                                **emploi_egal_a_la_demande(socle))
    for nom, (initial, releve) in cas.items():
        volume, valeur = _identite_et_valorisation(initial, releve)
        assert volume <= SEUIL_IDENTITE and valeur <= SEUIL_VALORISATION, (nom, volume, valeur)
        lignes.append(f"{nom} : volume {volume:.1e}, valorisation {valeur:.1e}")
    publier(f"Bloc 2, identité de volume et valorisation (P73) ({etiquettes(socle)})",
            lignes + ["seuils 1e−12 ; IN_{t+1} − IN_t = ligne 4 au bit"])


# --------------------------------------------------------------------------
# Disponibilité : épuisement du stock (P72), rationnement proportionnel
# --------------------------------------------------------------------------


def test_disponibilite_epuisement_zero_exact(socle, publier):
    """Fiche 2, § 9.6, « Disponibilité », et précision du 13/11/2026 (P72) : état d'ouverture au
    stock réduit au dixième de son sentier (IN^vol et IN, V^flux recalculées), demande des trois
    acheteurs supérieure de 10 % au disponible au pas 0 : même taux de service pour chaque
    acheteur (à 2 ulp près), IN^vol = 0 et IN = 0 **exactement** à la clôture, lignes 1 à 3 au
    prix du pas sur les volumes servis (la demande non servie n'est pas un flux) ; puis 24 pas
    sans arrêt, IN^vol ≥ 0 et IN ≥ 0 à chaque clôture."""
    sentier = socle.sentier(0.02)
    base = socle.etat_initial(sentier)
    positions = {p: getattr(base, p) for p in cat.NOMS_POSTES}
    positions["IN"] = base.IN / 10.0
    v_flux = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(positions, s)
              for s in cat.SECTEURS}
    initial = dataclasses.replace(base, IN_vol=base.IN_vol / 10.0, IN=positions["IN"], **v_flux)
    s = sentier.s
    # Production du pas 0 : technique active (y* > pr N, le stock étant bas), y = pr_0 N_0.
    y0 = initial.pr * s["N"]
    disponible = initial.IN_vol + y0
    demande = (s["C_plan"] + s["I_plan"] + s["G_plan"]) / s["p"]
    k = 1.1 * disponible / demande

    def chocs(nom, t):
        return k if t == 0 else 1.0

    _, releve = derouler(socle, sentier, 25, initial, chocs_des_plans=chocs)
    p0, v = releve.pas[0], releve.pas[0]["variables"]
    assert v["y"] == y0 < v["y_etoile"]
    d = {b: v[plan] / v["p"] for b, plan in (("C", "C_plan"), ("I", "I_plan"), ("G", "G_plan"))}
    assert abs(sum(d.values()) / disponible - 1.1) <= 1e-12
    assert v["v"] == disponible
    for b, ligne in (("C", "1"), ("I", "3"), ("G", "2")):
        assert abs(v[f"{b}_vol"] / d[b] - v["v"] / sum(d.values())) <= 2 * math.ulp(1.0)
        assert p0[ligne] == v["p"] * v[f"{b}_vol"]
        assert d[b] - v[f"{b}_vol"] > 0.0
    assert p0["etat"].IN_vol == 0.0 and p0["etat"].IN == 0.0
    assert initial.IN > 0.0 and p0["4"] == -initial.IN
    for p in releve.pas:
        assert p["etat"].IN_vol >= 0.0 and p["etat"].IN >= 0.0
    publier(f"Bloc 2, épuisement du stock (P72) ({etiquettes(socle)})", [
        f"d / disponible = {sum(d.values()) / disponible:.15f} ; IN^vol_1 = "
        f"{p0['etat'].IN_vol!r}, IN_1 = {p0['etat'].IN!r} ; ligne 4 = −IN_0 au bit ; 25 pas "
        "sans arrêt"])


# --------------------------------------------------------------------------
# Délai et vitesses (emploi égal à la demande de travail)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("facteur", [1.01, 0.99])
def test_delai_d_un_choc_de_demande(socle, facteur):
    """Fiche 2, § 9.6, « Délai » : choc de la dépense publique au tour n = 6 seulement :
    production inchangée au tour n (au bit), ventes du signe du choc et stock de clôture de
    signe opposé au tour n, production du signe du choc au tour n + 1."""
    sentier, n = socle.sentier(0.02), 6
    emploi = emploi_egal_a_la_demande(socle)
    _, base = derouler(socle, sentier, n + 2, **emploi)
    _, choc = derouler(socle, sentier, n + 2, chocs_des_plans=chocs_g(facteur, n, n), **emploi)
    signe = 1.0 if facteur > 1.0 else -1.0
    b, c = base.pas[n], choc.pas[n]
    assert c["variables"]["y"] == b["variables"]["y"]
    assert signe * (c["variables"]["v"] - b["variables"]["v"]) > 0.0
    assert signe * (c["etat"].IN_vol - b["etat"].IN_vol) < 0.0
    assert signe * (choc.pas[n + 1]["variables"]["y"] - base.pas[n + 1]["variables"]["y"]) > 0.0
    for t in range(n):
        assert choc.pas[t]["variables"]["y"] == base.pas[t]["variables"]["y"]


def test_vitesses_n_determinent_pas_l_etat_d_arrivee(socle, publier):
    """Fiche 2, § 9.6, « Vitesses » (critère 4) : choc G + 1 % aux tours 1 à 12 ; branches
    λ_v et λ_IN × 0,5 et × 2 (constructeur validé) ; après 720 pas, l'écart relatif du rapport
    des stocks aux ventes et de y/v entre les deux branches est d'au plus 1e−6."""
    sentier = socle.sentier(0.02)
    p = socle.PARAMETRES_DE_REFERENCE
    ratios = {}
    for facteur in (0.5, 2.0):
        table = varier(p.production, lambda_v=facteur * p.production.lambda_v.valeur,
                       lambda_IN=facteur * p.production.lambda_IN.valeur)
        initial, releve = derouler(socle, sentier, NB_PAS,
                                   parametres=dataclasses.replace(p, production=table),
                                   chocs_des_plans=chocs_g(1.01, 1, 12),
                                   **emploi_egal_a_la_demande(socle))
        dernier = releve.pas[-1]
        ouverture = releve.pas[-2]["etat"]
        v = dernier["variables"]
        ratios[facteur] = (ouverture.IN_vol / v["v"], v["y"] / v["v"])
        # Le choc a bien écarté la trajectoire du sentier pendant son cours.
        assert ecart(releve.pas[12]["etat"].IN_vol,
                     socle.valeur_d_ouverture(sentier, "IN_vol", 13)) > 1e-4
    ecarts = [ecart(a, b) for a, b in zip(ratios[0.5], ratios[2.0], strict=True)]
    assert max(ecarts) <= SEUIL_VITESSES
    publier(f"Bloc 2, vitesses × 0,5 et × 2 après un choc G + 1 % sur 12 tours ({etiquettes(socle)} ; "
            "N = N*)", [f"écart relatif après 720 pas : stocks / ventes {ecarts[0]:.1e}, y/v "
                        f"{ecarts[1]:.1e} (seuil 1e−6)"])


# --------------------------------------------------------------------------
# Phases : aucune lecture hors ordre (refus de l'assemblage)
# --------------------------------------------------------------------------


def _fautif(etape, lecture):
    """Bloc de la production dont le siège `etape` déclare en plus la lecture `lecture`."""
    sieges = tuple(dataclasses.replace(s, lit=s.lit + (lecture,)) if s.etape == etape else s
                   for s in Production.declaration.sieges)
    declaration = dataclasses.replace(Production.declaration, sieges=sieges)
    return type("ProductionFautive", (Production,), {"__slots__": (),
                                                     "declaration": declaration})()


@pytest.mark.parametrize("etape, lecture, motif", [
    # Un autre plan de la phase 2, écrit par un bloc du même groupe.
    ("2", Lecture("2", "G_plan"), "« G_plan » : triangularité"),
    # Le prix du pas en phase 4 : écrit plus tard (phase 5).
    ("4", Lecture("5", "p"), "« p » : triangularité"),
    # W_t en phase 5 : la phase 1 n'est pas dans la colonne « Lisent » de la phase 5.
    ("5", Lecture("1", "W_suivant"), "« W_suivant » : phase 1 hors de la colonne « Lisent »"),
])
def test_phases_lecture_hors_ordre_refusee(socle, etape, lecture, motif):
    """Fiche 2, § 9.6, « Phases » : la déclaration du bloc est acceptée par `assembler` ; une
    lecture hors ordre ajoutée à un siège est refusée (`DefautDeDeclaration`), avant tout pas."""
    sentier = socle.sentier(0.02)
    ordonnanceur(socle, sentier)
    blocs = socle.blocs(sentier, reels=(_fautif(etape, lecture),))
    with pytest.raises(DefautDeDeclaration, match=motif):
        ordo.assembler(socle.PHASES, blocs, socle.PARAMETRES_DE_REFERENCE, socle.SANS_ENTREES)


def test_le_bloc_reel_est_trouve_par_le_socle(socle):
    """`blocs_reels` rend un bloc par module de `src/nations/blocs/`, dans l'ordre des
    radicaux, dont celui de `production.py` en tête ; substitués à leurs blocs d'essai, ils sont
    assemblés avec les autres."""
    reels = socle.blocs_reels()
    modules = sorted(p.stem for p in (socle.RACINE / "src" / "nations" / "blocs").glob("*.py")
                     if p.name != "__init__.py")
    assert sorted(b.declaration.radical for b in reels) == modules
    assert type(reels[0]) is Production
    blocs = socle.blocs(socle.sentier(0.02), reels=reels)
    assert [b.declaration.radical for b in blocs] == list(socle.RADICAUX)
    assert type(blocs[0]) is Production
    ordo.assembler(socle.PHASES, blocs, socle.PARAMETRES_DE_REFERENCE, socle.SANS_ENTREES)
