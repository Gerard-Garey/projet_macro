"""Socle complet : blocs 2 à 9 réels, aucun bloc d'essai (#132, rang 3 de J3-d2).

**Banc** (critère « Branche » de la feuille de route, § 1 ; ADR 0013, annotation du 15/11/2026
(J3-d2), point 6) : `socle.blocs_du_socle_complet()`, tables alignées sur le sentier du script
(`socle.parametres_du_sentier`, θ_G résolu compris), n_a = 12, **ν_G = 1,15 passé explicitement**
au script (défaut ν_G = 1, hors domaine), π* ∈ {0 ; 2 % ; 10 %}, état initial du script
(`socle.etat_initial`, la résolution par `scenarios/` relevant de J3-e). Étiquette : `ETIQUETTE`.
Les chocs sont injectés **par composition dans `tests/`** (F1) : une sous-classe du bloc 9 réel
dont les méthodes d'étape lisent une table modifiée (`bloc_9_compose`), des entrées de scénario
(ς_B), un état initial modifié (r̂*, D_H) ; jamais par un drapeau dans `src/`.

**Critères, écrits avant l'essai (§ 1, précisions du rang 1a, P156 à P164), non déplacés** :
- **Branche** : 720 pas sans choc, max_t |x_t/x̄_t − 1| ≤ 1e−9 pour la liste de P94 étendue aux
  blocs 5 et 6 (J3-d1) et au bloc 9 (F4, P161 : G^plan, G, T_H, T^cou, T_F, Tr, lignes 11b et
  11c, M^G, M^G*, Em, ΔB^prim_Bk, ΔB^prim_CB, B, B_Bk/B, dette consolidée/(n_a PIB), Y^HS) ;
  nullités calculées (`socle.est_nulle`), **au bit** pour celles de F3 (T_F, T_{F,t−1}, T^e_F,
  Tr, ligne 6, B_H, 11a, 19a-ménages, ΔB^prim_CB, B_CB, 11c, E^CB, parts de E13), à 1e−12 S^G
  pour T^cou, à 1e−12 S^CB pour Res (test de signe) ; plafond de E1 inactif (G^plan = plan non
  plafonné) ; hors seuil sans erreur de code : condition d'arrêt de la branche ;
- **état stationnaire** (F2) : au pas 0 du moteur, grandeurs du bloc 9 égales à `un_pas` du
  script à 1e−10 relatif ;
- **un seul calcul du besoin d'émission par pas** (test de décompte) ;
- **caisse** (critère 11, P158), **parts non payées** (critère 12, F9, P157), **placement raté**
  (P90), **bornes** (critère 16), **couverture** sur le moteur (F6, F7), **C59** (P156, P160),
  **reprise** (critère 2) : seuils au docstring de chaque test.

Réaffirmés avec le bloc 9 réel (P162) : « Délais » des fiches 5 et 6, signe et date exacts sur la
chaîne E3, E6, E5 → H6, F3.

Publiés sans verdict (lignes (b)) : marge de caisse (h_max), retour après −5 % à n_a = 52 (appel
direct, critère 11), θ_H aux deux sens (C52), temps de doublement sous φ = 0 (C62 : choc de 1 %,
F11, et régime linéaire, décision du mainteneur du 15/11/2026), marge de
`sec:finances_publiques-caisse`. Aucune mesure ici ne vaut résultat final (J3-e).
"""

import dataclasses
import math

import pytest

from nations.blocs import finances_publiques as bloc_9
from nations.blocs import investissement as bloc_6
from nations.blocs import menages as bloc_5
from nations.blocs.finances_publiques import FinancesPubliques
from nations.etat import schema
from nations.etat.sauvegarde import charger, sauvegarder
from nations.moteur import ordonnanceur as ordo
from nations.moteur.conversions import TauxDeFlux, par_pas
from nations.moteur.diagnostics import RefusDuMoteur
from nations.moteur.parametres import varier
from nations.moteur.parametres.cadre import CADRE, PAS_PAR_AN
from nations.moteur.phases import PHASES
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.diagnostics import DefautComptable
from nations.noyau.grand_livre import ClotureDePhase, FluxPropose, ouvrir_pas
from nations.observation.observateur import FinDePas

N_A = PAS_PAR_AN.valeur
NB_PAS = 720
EPS = CADRE.tolerance_identite_pas
ETIQUETTE = "socle complet : blocs 2 à 9 réels, aucun bloc d'essai ; ν_G = 1,15"
# Seuils écrits avant l'essai (§ 1 ; P156 à P164).
SEUIL_RELATIF = 1e-9
SEUIL_NUL = 1e-12
SEUIL_SCRIPT = 1e-10
SEUIL_FLUX = 1e-12
SEUIL_C59_TRAJECTOIRE = 1e-10
TOURS_DU_CHOC = 12
DELAI_DE_DESACTIVATION = 12
# Caisse (P158) : hausses au-delà de la marge, par π̄.
AU_DELA_DE_LA_MARGE = {0.0: 1.25, 0.02: 1.25, 0.10: 1.60}


# --------------------------------------------------------------------------
# Banc
# --------------------------------------------------------------------------


class Releve:
    """Observateur : par pas, montant exécuté de chaque ligne (clé = ligne) et ses termes (clé
    `<ligne>:termes`), les contreparties 17, 20 et 22 cumulées sur les clôtures du pas, variables
    du pas, grandeurs d'ouverture et état t + 1."""

    def __init__(self):
        self.pas = []
        self._montants = {}

    def relever(self, e):
        if type(e) is ClotureDePhase:
            for ligne, termes in e.montants:
                if cat.LIGNE[ligne].contrepartie:
                    # Contreparties de règlement (17, 20, 22) : exécutées à chaque clôture,
                    # cumulées sur le pas.
                    self._montants[ligne] = (self._montants.get(ligne, 0.0)
                                             + sum(x for _, x in termes))
                    continue
                self._montants[ligne] = sum(x for _, x in termes)
                self._montants[f"{ligne}:termes"] = dict(termes)
        elif type(e) is FinDePas:
            self.pas.append({**self._montants, "t": e.t, "variables": dict(e.variables_du_pas),
                             "grandeurs": dict(e.grandeurs_ouverture), "etat": e.etat})
            self._montants = {}


class _VueAvecParametres:
    """Vue d'un bloc dont les paramètres sont remplacés (composition d'essai, F1) ; tout le reste
    est la vue du moteur."""

    __slots__ = ("_vue", "parametres")

    def __init__(self, vue, parametres):
        self._vue = vue
        self.parametres = parametres

    def __getattr__(self, nom):
        return getattr(self._vue, nom)


def bloc_9_compose(modifier):
    """Bloc 9 réel dont chaque méthode d'étape lit la table `finances_publiques` rendue par
    `modifier(t, table)` (t : pas d'ouverture) ; sous-classe sans attribut d'instance, même
    déclaration (composition dans `tests/`, jamais un drapeau dans `src/`, F1)."""
    espace = {"__slots__": ()}
    for siege in FinancesPubliques.declaration.sieges:
        nom = f"phase_{siege.etape}"

        def methode(self, vue, _methode=getattr(FinancesPubliques, nom)):
            p = vue.parametres
            table = modifier(vue.ouverture.t, p.finances_publiques)
            if table is not p.finances_publiques:
                vue = _VueAvecParametres(vue, dataclasses.replace(p, finances_publiques=table))
            _methode(self, vue)
        espace[nom] = methode
    return type("FinancesPubliquesComposee", (FinancesPubliques,), espace)()


def blocs(socle, bloc_9=None):
    rendus = socle.blocs_du_socle_complet()
    if bloc_9 is None:
        return rendus
    return tuple(bloc_9 if b.declaration.radical == "finances_publiques" else b for b in rendus)


def assembler(socle, sentier, bloc_9=None, parametres=None):
    tables = socle.parametres_du_sentier(sentier) if parametres is None else parametres
    return ordo.assembler(PHASES, blocs(socle, bloc_9), tables, socle.ENTREES_DU_SOCLE)


def derouler(socle, sentier, nb_pas, *, bloc_9=None, initial=None, parametres=None,
             varsigma_B=None, observateur=None):
    """`nb_pas` pas du socle complet ; `varsigma_B` : t → ς_{B,t} (placement raté), nul sinon."""
    o = assembler(socle, sentier, bloc_9, parametres)
    etat = socle.etat_initial(sentier) if initial is None else initial
    releve = Releve() if observateur is None else observateur
    for _ in range(nb_pas):
        part = 0.0 if varsigma_B is None else varsigma_B(etat.t)
        etat = ordo.executer_pas(etat, socle.entrees_du_tour(varsigma_B=part), o, releve)
    return etat, releve


def choc_de_theta_G(facteur, debut=0, duree=TOURS_DU_CHOC):
    """Table modifiée : θ_G × `facteur` aux pas [debut ; debut + duree[ (tours debut + 1 à
    debut + duree)."""
    def modifier(t, table):
        if debut <= t < debut + duree:
            return varier(table, theta_G=table.theta_G * facteur)
        return table
    return modifier


@pytest.fixture(scope="module")
def banc(socle):
    """π* → (sentier, état initial, relevé) : 720 pas sans choc du socle complet."""
    rendus = {}
    for pi in socle.POINTS_PI:
        sentier = socle.sentier(pi)
        _, releve = derouler(socle, sentier, NB_PAS)
        rendus[pi] = (sentier, socle.etat_initial(sentier), releve)
    return rendus


def _positions(etat):
    return {q: getattr(etat, q) for q in cat.NOMS_POSTES}


def _module_j3d1():
    import importlib.util
    import sys
    from pathlib import Path
    nom = "test_stationnarite_j3d1_du_socle_complet"
    if nom not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            nom, Path(__file__).with_name("test_stationnarite_j3d1.py"))
        module = importlib.util.module_from_spec(spec)
        sys.modules[nom] = module
        spec.loader.exec_module(module)
    return sys.modules[nom]


# --------------------------------------------------------------------------
# Grandeurs du bloc 9 (F4, P161)
# --------------------------------------------------------------------------

DEFINITIONS_DU_BLOC_9 = {
    "G^plan": "plan de dépense (E1), u.m. par pas ; sentier nominal",
    "G (ligne 2)": "dépense exécutée, u.m. par pas ; sentier nominal",
    "T_H (E3)": "impôt des ménages, u.m. par pas ; sentier nominal",
    "ligne 11b": "intérêts sur titres de la banque, u.m. par pas ; sentier nominal",
    "M^G (ouverture)": "compte du Trésor d'ouverture, u.m. ; position du sentier",
    "M^G*": "encaisse visée (E8), u.m. ; sentier nominal",
    "Em": "besoin d'émission (E9), u.m. par pas ; sentier nominal",
    "ΔB^prim_Bk (19a-banque)": "souscription de la banque (E11), u.m. par pas ; sentier nominal",
    "B (ouverture)": "dette brute d'ouverture B_H + B_Bk + B_CB, u.m. ; positions du sentier",
    "B_Bk/B": "part de la banque dans la dette d'ouverture, fraction ; (1 − θ_CB)",
    "dette consolidée/(n_a PIB)": "(B − M^G − E^CB) d'ouverture/(n_a PIB du pas), années ; script",
    "Y^HS (état)": "assiette Y^HS_t retenue (E12), u.m. par pas ; sentier nominal",
}
# Nulles de F3 : clé de `GRANDEURS_NULLES_DU_SOCLE_COMPLET` ou de J3-d1 → (valeur du pas,
# échelle de publication) ; jugées au bit.
NULLES_AU_BIT = ("T_F (E5)", "T^e_F", "Tr (E6)", "ligne 6", "transferts non versés (E13)", "B_H",
                 "ligne 11a", "ligne 19a-ménages", "ΔB^prim_CB (19a-BC)", "B_CB", "ligne 11c",
                 "E^CB (V^flux)", "perte non couverte (E13)", "T_F_m1", "ligne 7 T_F")


def grandeurs_du_bloc_9(socle, pas, initial, sentier):
    """Grandeurs du bloc 9 : nom → [(t, x_t, x̄_t)] (relatives), et nulles : nom → [(t, x_t, 0)]
    (T^cou rapportée à S^G ; les nulles au bit, valeurs brutes)."""
    e = sentier.e
    ouvertures = [initial] + [p["etat"] for p in pas[:-1]]
    g = {cle: [] for cle in (*DEFINITIONS_DU_BLOC_9, "T^cou (E4)",
                             *(c for c in NULLES_AU_BIT if c not in ("T_F_m1", "ligne 7 T_F")))}
    dette = (e["B"] - e["M_G"]) / (N_A * e["PIB"])
    b_bk = 1.0 - sentier.par.theta_CB
    for t, p in enumerate(pas):
        v, o, f = p["variables"], ouvertures[t], p["etat"]

        def nominal(cle, t=t):
            return sentier.valeur(cle, socle.NOMINAL, t)

        B = o.B_H + o.B_Bk + o.B_CB
        pib = p["1"] + p["2"] + p["3"] + p["4"]
        e_cb = o.B_CB + o.L_CB - o.Res - o.M_G
        g["G^plan"].append((t, v["G_plan"], nominal("G_plan")))
        g["G (ligne 2)"].append((t, p["2"], nominal("G")))
        g["T_H (E3)"].append((t, v["T_H"], nominal("T_H")))
        g["ligne 11b"].append((t, p["11b"], nominal("l11b")))
        g["M^G (ouverture)"].append((t, o.M_G, socle.position_d_ouverture(sentier, "M_G", t)))
        g["M^G*"].append((t, v["M_G_etoile"], nominal("M_G_star")))
        g["Em"].append((t, v["Em"], nominal("Em")))
        g["ΔB^prim_Bk (19a-banque)"].append((t, p["19a-banque"], nominal("dB_Bk")))
        g["B (ouverture)"].append((t, B, sum(socle.position_d_ouverture(sentier, q, t)
                                             for q in ("B_H", "B_Bk", "B_CB"))))
        g["B_Bk/B"].append((t, o.B_Bk / B, b_bk))
        g["dette consolidée/(n_a PIB)"].append((t, (B - o.M_G - e_cb) / (N_A * pib), dette))
        g["Y^HS (état)"].append((t, f.Y_HS_m1, socle.valeur_d_ouverture(sentier, "Y_HS_m1",
                                                                         t + 1)))
        s_g = idt.echelle_bilan(_positions(o), "etat")
        g["T^cou (E4)"].append((t, v["T_cou"] / s_g, 0.0))
        g["T_F (E5)"].append((t, v["T_F"], 0.0))
        g["T^e_F"].append((t, v["T_e_F"], 0.0))
        g["Tr (E6)"].append((t, v["Tr"], 0.0))
        g["ligne 6"].append((t, p["6"], 0.0))
        g["transferts non versés (E13)"].append((t, v["Tr_non_verses"], 0.0))
        g["B_H"].append((t, f.B_H, 0.0))
        g["ligne 11a"].append((t, p["11a"], 0.0))
        g["ligne 19a-ménages"].append((t, p["19a-ménages"], 0.0))
        g["ΔB^prim_CB (19a-BC)"].append((t, p["19a-BC"], 0.0))
        g["B_CB"].append((t, f.B_CB, 0.0))
        g["ligne 11c"].append((t, p["11c"], 0.0))
        g["E^CB (V^flux)"].append((t, getattr(f, cat.VALEUR_NETTE_FLUX["banque_centrale"]), 0.0))
        g["perte non couverte (E13)"].append((t, v["perte_non_couverte"], 0.0))
    return g


def juger(socle, sentier, initial, releve):
    """Relevé du critère « Branche » sur le socle complet : (séries, nulles, pires, hors seuil)."""
    j3d1 = _module_j3d1()
    tables = socle.parametres_du_sentier(sentier)
    resolues = {**socle.valeurs_resolues(sentier), **socle.valeurs_resolues_p94(sentier)}
    series = {}
    for cle, serie in {**socle.grandeurs_b(releve.pas, initial, sentier),
                       **socle.grandeurs_p94(releve.pas, initial, sentier)}.items():
        series[cle] = [(t, x, resolues[cle]) for t, x in serie]
    for nom in j3d1.ETATS_P94:
        series[nom] = [(t, getattr(p["etat"], nom), socle.valeur_d_ouverture(sentier, nom, t + 1))
                       for t, p in enumerate(releve.pas)]
    blocs_5_6 = j3d1.grandeurs_des_blocs_5_et_6(socle, releve.pas, initial, sentier)
    del blocs_5_6["T^cou"]  # relevée sous « T^cou (E4) », au même dénominateur S^G
    series.update(blocs_5_6)
    series.update(grandeurs_du_bloc_9(socle, releve.pas, initial, sentier))
    nulles = {cle for cle in series if socle.est_nulle(cle, tables, sentier)}
    assert {c for c, s in series.items() if all(r == 0.0 for _, _, r in s)} <= nulles
    assert set(NULLES_AU_BIT) <= nulles
    pires = {}
    for cle, serie in series.items():
        assert serie and serie[-1][0] == NB_PAS - 1, cle
        if cle in nulles:
            pires[cle] = max(abs(x) for _, x, _ in serie)
        else:
            pires[cle] = max(abs(x / r - 1.0) for _, x, r in serie)
    hors = {c: x for c, x in pires.items()
            if x > (0.0 if c in NULLES_AU_BIT else SEUIL_NUL if c in nulles else SEUIL_RELATIF)}
    return series, nulles, pires, hors


# --------------------------------------------------------------------------
# Critère « Branche » : stationnarité du socle complet, nullités, état du script
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_stationnarite_du_socle_complet(banc, socle, pi, publier):
    """Critère « Branche » (P94 étendue, F4, P161 ; F3, P121) : max_t |x_t/x̄_t − 1| ≤ 1e−9 sur
    720 pas ; nullités de F3 au bit ; T^cou ≤ 1e−12 S^G ; Res (H) et autres nulles ≤ 1e−12 à leur
    échelle ; ϱ̄_L au bit ; plafond de E1 inactif à chaque pas (G^plan = plan non plafonné).
    Hors seuil sans erreur de code : condition d'arrêt de la branche."""
    sentier, initial, releve = banc[pi]
    series, nulles, pires, hors = juger(socle, sentier, initial, releve)
    j3d1 = _module_j3d1()
    assert all(x == r for _, x, r in series["ϱ̄_L (état)"])
    assert all(p["variables"]["G_plan"] == p["variables"]["G_vise"] for p in releve.pas)
    fenetres, _ = j3d1.derive_par_fenetre(socle, sentier, releve)
    definitions = {**j3d1.DEFINITIONS, **DEFINITIONS_DU_BLOC_9}
    publier(f"Stationnarité du socle complet, π* = {100 * pi:g} %, 720 pas ({ETIQUETTE})", [
        "verdict : " + ("NON TENU (condition d'arrêt du § 1)" if hors else "tenu")
        + " ; seuils 1e−9 relatif, 1e−12 pour une nulle à son échelle, 0 au bit (F3)",
        *(f"{c} : {pires[c]:.1e} " + ("(nulle au bit, |x|)" if c in NULLES_AU_BIT else
                                      "(nulle, |x|)" if c in nulles else "(relatif)")
          + (f" — {definitions[c]}" if c in definitions else "") for c in series),
        "dérive des positions par fenêtre de 360 pas : " + " | ".join(
            f"pas {360 * w}–{360 * (w + 1) - 1} : {x:.1e} ({q})"
            for w, (x, q) in sorted(fenetres.items())),
        "plafond de E1 : inactif aux 720 pas (G^plan = plan non plafonné, au bit)",
    ])
    assert not hors, hors


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_etat_stationnaire_egal_au_script_sur_le_moteur(banc, socle, pi):
    """F2, n_a = 12 sur le moteur : au pas 0, G^plan, T_H, M^G*, Em, Y^HS, lignes 2, 11b et
    19a-banque égaux à `un_pas` du script à 1e−10 relatif ; T^cou ≤ 1e−12 S^G ; Tr = 0."""
    sentier, initial, releve = banc[pi]
    p, s = releve.pas[0], sentier.s
    v = p["variables"]
    for x, cle in ((v["G_plan"], "G_plan"), (v["T_H"], "T_H"), (v["M_G_etoile"], "M_G_star"),
                   (v["Em"], "Em"), (p["etat"].Y_HS_m1, "Y_HS"), (p["2"], "G"),
                   (p["11b"], "l11b"), (p["19a-banque"], "dB_Bk")):
        assert abs(x / s[cle] - 1.0) <= SEUIL_SCRIPT, cle
    assert abs(v["T_cou"]) <= SEUIL_NUL * idt.echelle_bilan(_positions(initial), "etat")
    assert v["Tr"] == 0.0


def test_un_seul_calcul_du_besoin_d_emission_par_pas(socle, monkeypatch):
    """Critère de #132 (ADR 0013, annotation du 15/11/2026, point 5) : la fonction balisée E9
    (`besoin_d_emission`) est appelée une fois par pas sur le moteur, et les trois lignes 19a
    du pas reposent sur ce même Em (E10, E11 au bit), θ_CB (phase 1) et ς_B (phase 0) lus dans
    les variables du pas : sentier θ_CB = 0,5, placement raté ς_B = 0,3 au pas 5."""
    appels = []
    original = bloc_9.besoin_d_emission

    def compter(*args):
        appels.append(args)
        return original(*args)
    monkeypatch.setattr(bloc_9, "besoin_d_emission", compter)
    sentier = socle.sentier(0.02, theta_CB=0.5)
    _, releve = derouler(socle, sentier, 24, varsigma_B=lambda t: 0.3 if t == 5 else 0.0)
    assert len(appels) == 24
    for p in releve.pas:
        v = p["variables"]
        Em, theta, part = v["Em"], v["theta_CB"], v["varsigma_B"]
        assert theta == 0.5 and part == (0.3 if p["t"] == 5 else 0.0)
        assert p["19a-BC"] == theta * Em
        assert p["19a-banque"] == (1.0 - part) * (Em - theta * Em)
        assert p["19a-ménages"] == 0.0


# --------------------------------------------------------------------------
# Cas à la main (critère 1) et lecture de Π^CB (P90)
# --------------------------------------------------------------------------


def test_cas_a_la_main_depense_accrue_de_dix_pour_cent(socle, publier):
    """Critère 1 de la fiche 9 (classe (a)), θ_CB = 0,5, dépense accrue de 10 % sur un pas
    (θ_G × 1,1 au pas 0), π* = 2 % : lignes 2, 6, 7, 11b, 11c, 16, 19a recalculées à la main sur
    l'ouverture et les variables de la phase 1, lignes 20 et 22 égales aux variations de Res et
    de M^G ; valeur nette de l'État égale par le stock et par les flux ; E^CB = 0 par le stock
    de clôture (C58) ; à 1e−12 S du secteur."""
    sentier = socle.sentier(0.02, theta_CB=0.5)
    o = socle.etat_initial(sentier)
    f, r = derouler(socle, sentier, 1, bloc_9=bloc_9_compose(choc_de_theta_G(1.10, 0, 1)))
    p, v = r.pas[0], r.pas[0]["variables"]
    tables = socle.parametres_du_sentier(sentier).finances_publiques
    s_g = idt.echelle_bilan(_positions(o), "etat")
    s_cb = idt.echelle_bilan(_positions(o), "banque_centrale")
    s_bk = idt.echelle_bilan(_positions(o), "banque")
    i_pas = par_pas(TauxDeFlux(v["i_CB"]))
    gamma_e = p["grandeurs"]["Gamma_e"]
    attendus = {
        "2": (v["G_plan"], s_g),
        "6": (0.0, s_g),
        "7": (tables.tau_H * gamma_e * o.Y_HS_m1 + v["T_cou"], s_g),
        "11b": (i_pas * o.B_Bk, s_g),
        "11c": (i_pas * o.B_CB, s_g),
        "16": (i_pas * (o.B_CB + o.L_CB - o.Res), s_cb),
    }
    PB = attendus["2"][0] + attendus["11b"][0] + attendus["11c"][0]
    Em = PB - attendus["7"][0] - attendus["16"][0] + tables.nu_G * PB - o.M_G
    attendus["19a-BC"] = (0.5 * Em, s_g)
    attendus["19a-banque"] = (0.5 * Em, s_g)
    attendus["19a-ménages"] = (0.0, s_g)
    attendus["20"] = (f.Res - o.Res, s_bk)
    attendus["22"] = (f.M_G - o.M_G, s_g)
    ecarts = {ligne: abs(p[ligne] - x) / echelle for ligne, (x, echelle) in attendus.items()}
    assert v["G_plan"] == v["G_vise"] and v["theta_CB"] == 0.5
    assert all(x <= SEUIL_FLUX for x in ecarts.values()), ecarts
    v_etat = (idt.valeur_nette_stock(_positions(f), "etat"),
              getattr(f, cat.VALEUR_NETTE_FLUX["etat"]))
    assert abs(v_etat[0] - v_etat[1]) <= SEUIL_FLUX * s_g
    e_cb = idt.valeur_nette_stock(_positions(f), "banque_centrale")
    assert abs(e_cb) <= SEUIL_FLUX * s_cb
    publier(f"Cas à la main, θ_CB = 0,5, dépense +10 % sur un pas, π* = 2 % ({ETIQUETTE})", [
        " ; ".join(f"ligne {ligne} : {x:.1e}" for ligne, x in ecarts.items()) + " (/S)",
        f"V^G par le stock − par les flux : {(v_etat[0] - v_etat[1]) / s_g:.1e} S^G ; E^CB de "
        f"clôture par le stock : {e_cb / s_cb:.1e} S^CB"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_lecture_de_pi_cb_en_phase_1(socle, pi):
    """P90, « Lecture de Π^CB » (X1 réaffirmée par le bloc 9 réel) : la ligne 16 exécutée en 8 (b)
    et E9 en phase 7 lisent le Π^CB écrit en phase 1, au bit ; sous un choc de taux (r̂* + 0,01
    dans l'ouverture), la ligne 16 suit Π^CB du pas, à 1e−12 relatif."""
    sentier = socle.sentier(pi)
    initial = socle.etat_initial(sentier)
    for etat in (initial, dataclasses.replace(initial,
                                              r_hat_etoile=initial.r_hat_etoile + 0.01)):
        _, r = derouler(socle, sentier, 12, initial=etat)
        for p in r.pas:
            v = p["variables"]
            assert p["16"] == v["Pi_CB"]
            interets = p["11a"] + p["11b"] + p["11c"]
            Em = bloc_9.besoin_d_emission(p["2"], p["6"], interets, p["7"], v["Pi_CB"],
                                          v["M_G_etoile"], (initial if p["t"] == 0 else
                                                            r.pas[p["t"] - 1]["etat"]).M_G)
            assert Em == v["Em"]


# --------------------------------------------------------------------------
# Caisse (critère 11, P158)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("n_a", [4, 12, 52])
@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_caisse_hausse_de_dix_pour_cent_par_appel_direct(socle, pi, n_a, publier):
    """Critère 11 (P158) : sur l'état résolu (n_a ∈ {4 ; 12 ; 52}), une hausse de 10 % de la
    dépense d'un tour au suivant n'est pas rationnée par E1 : G^plan_{t+1} = Γ̄ G (1,1), l'encaisse
    d'ouverture du tour suivant étant ν_G PB ; marge publiée h_max = ν_G/(Γ̄ s_G) − 1, s_G =
    G/PB (forme exacte de `macro`)."""
    es = socle.script()
    par = dataclasses.replace(es.Parametres(), pi_cible=pi, n_a=n_a, nu_G=socle.NU_G)
    e = es.etat_stationnaire(par)
    M_G_suivant = par.nu_G * e["PB"]
    vise = e["Gam"] * e["G"] * 1.10
    assert bloc_9.plan_de_depense(M_G_suivant, vise) == vise
    h_max = par.nu_G / (e["Gam"] * e["G"] / e["PB"]) - 1.0
    assert h_max > 0.10
    publier(f"Caisse, marge h_max = ν_G/(Γ̄ s_G) − 1, π̄ = {100 * pi:g} %, n_a = {n_a} "
            "(appel direct de E1 sur l'état résolu, sans verdict)",
            [f"h_max = {100 * h_max:.2f} % ; +10 % servi sans rationnement"])


def _actif(p):
    return p["variables"]["G_plan"] < p["variables"]["G_vise"]


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_caisse_sur_le_moteur(socle, pi, publier):
    """Critère 11 (P158), n_a = 12 : (i) +10 % au tour 2 seul ; (ii) −5 % aux tours 1 à 12 puis
    retour : aucun rationnement de caisse (G^plan = plan non plafonné à chaque pas), dépense
    exécutée rapportée à la dépense demandée égale à 1 à 1e−12 ; (iii) au-delà de la marge (+25 %
    à π̄ ∈ {0 ; 2 %}, +60 % à 10 %, tours 1 à 12) : G^plan = max(0 ; M^G_t) exactement au tour du
    choc, noyau sans arrêt, plafond levé sous 12 tours, sans réactivation."""
    sentier = socle.sentier(pi)
    lignes = []
    for nom, modifier in (("+10 % au tour 2", choc_de_theta_G(1.10, debut=1, duree=1)),
                          ("−5 % aux tours 1 à 12", choc_de_theta_G(0.95))):
        _, r = derouler(socle, sentier, 120, bloc_9=bloc_9_compose(modifier))
        assert not any(_actif(p) for p in r.pas), nom
        pire = max(abs(p["2"] / p["variables"]["G_vise"] - 1.0) for p in r.pas)
        assert pire <= SEUIL_FLUX, nom
        lignes.append(f"{nom} : aucun rationnement ; max |G/G^demandée − 1| = {pire:.1e}")
    facteur = AU_DELA_DE_LA_MARGE[pi]
    initial = socle.etat_initial(sentier)
    _, r = derouler(socle, sentier, 120, bloc_9=bloc_9_compose(choc_de_theta_G(facteur)))
    assert len(r.pas) == 120
    premier = r.pas[0]
    assert premier["variables"]["G_plan"] == max(0.0, initial.M_G) and _actif(premier)
    actifs = [p["t"] for p in r.pas if _actif(p)]
    leve = next(t for t in range(len(r.pas)) if not _actif(r.pas[t]))
    assert leve <= TOURS_DU_CHOC
    assert all(t < leve for t in actifs)  # sans réactivation
    lignes.append(f"×{facteur:g} aux tours 1 à 12 : plafond actif aux pas {actifs[0]} à "
                  f"{actifs[-1]} ({len(actifs)} pas), levé au pas {leve}, jamais réactivé ; "
                  "aucun arrêt du noyau")
    publier(f"Caisse sur le moteur, π* = {100 * pi:g} % ({ETIQUETTE})", lignes)


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_caisse_retour_apres_moins_cinq_pour_cent_publie_a_52(socle, pi, publier):
    """Critère 11 (P158), « retour après 12 tours à −5 % », jugé sur le moteur à n_a = 12
    (`test_caisse_sur_le_moteur`), **publié à n_a = 52**, sans verdict, par appel direct de E1
    sur l'état résolu du script : le moteur ne tourne qu'à n_a = 12 (`PAS_PAR_AN`, lu à
    l'import par `conversions.par_pas` et par la taille du registre des prix). Au retour,
    l'encaisse d'ouverture est ν_G PB du dernier tour du choc et le plan revient à Γ̄ G : marge
    au retour h_ret = ν_G (PB − 0,05 G)/(Γ̄ G) − 1, forme statique approchée, aux prix et aux
    intérêts du sentier (la réponse des prix pendant les 12 tours du choc est ignorée) ; à
    n_a = 12, elle est publiée contre la marge mesurée sur le moteur au pas 12,
    M^G_12/G^demandée_12 − 1, qui en donne l'erreur."""
    es = socle.script()
    lignes = []
    for n_a in (12, 52):
        par = dataclasses.replace(es.Parametres(), pi_cible=pi, n_a=n_a, nu_G=socle.NU_G)
        e = es.etat_stationnaire(par)
        M_G_retour = par.nu_G * (e["PB"] - 0.05 * e["G"])
        vise = e["Gam"] * e["G"]
        servi = bloc_9.plan_de_depense(M_G_retour, vise)
        lignes.append(f"n_a = {n_a} (appel direct de E1, forme statique approchée) : h_ret = "
                      f"{100 * (M_G_retour / vise - 1):.2f} % ; G^plan/G^demandée au retour = "
                      f"{servi / vise:.12f}")
    sentier = socle.sentier(pi)
    _, r = derouler(socle, sentier, TOURS_DU_CHOC + 1,
                    bloc_9=bloc_9_compose(choc_de_theta_G(0.95)))
    M_G_12 = r.pas[TOURS_DU_CHOC - 1]["etat"].M_G
    v = r.pas[TOURS_DU_CHOC]["variables"]
    lignes.append(f"n_a = 12, moteur : M^G_12/G^demandée_12 − 1 = "
                  f"{100 * (M_G_12 / v['G_vise'] - 1):.2f} % ; G^plan/G^demandée au pas 12 = "
                  f"{v['G_plan'] / v['G_vise']:.12f}")
    publier(f"Caisse, retour après 12 tours à −5 %, π̄ = {100 * pi:g} % (n_a = 52 publié par "
            f"appel direct ; {ETIQUETTE} pour n_a = 12 ; sans verdict)", lignes)


# --------------------------------------------------------------------------
# Délais des fiches 5 et 6 sur la chaîne réelle (P162), θ_H (C52)
# --------------------------------------------------------------------------

TOUR_DU_LEVIER = 5
NB_PAS_DES_DELAIS = 9
SEUIL_DELAIS = 1e-12


def levier_au_tour(n, **valeurs):
    """Table modifiée : paramètres du bloc 9 `valeurs` au seul pas `n` (tour n + 1)."""
    def modifier(t, table):
        return varier(table, **valeurs) if t == n else table
    return modifier


def _premier_ecart(base, choc, lire):
    """Premier pas où `lire(p)` diffère au bit de la base, et le signe de l'écart."""
    for t, (a, b) in enumerate(zip(base.pas, choc.pas, strict=True)):
        if lire(a) != lire(b):
            return t, math.copysign(1.0, lire(b) - lire(a))
    return None, 0.0


def _plan(p):
    return p["variables"]["C_plan"]


def test_delais_des_fiches_5_et_6_sur_la_chaine_reelle(socle, publier):
    """P162, réaffirmation avec le bloc 9 réel des « Délais » des fiches 5 (critères 2 (d) et
    12 (b)) et 6 (C35, critère 12 (b)), signe et date exacts, levier au seul tour n = 5, π* = 2 %,
    chaîne réelle E3, E6, E5 → H6, F3 :
    - impôt des ménages (τ_H + 0,01, E3) : ligne 7 plus haute au tour n ; C^plan (H5) et ligne 1
      (H6) inchangés au bit jusqu'au tour n, modifiés au tour n + 1, signe − ;
    - transferts (θ_Tr = 0,001, E6) : ligne 6 au tour n ; C^plan et ligne 1 au tour n + 1,
      signe + ;
    - impôt des entreprises (τ_F = 0,01, E5) : Div_F (F3, ligne 14) du tour n identique au bit ;
      D_F de clôture du tour n abaissé de ΔT = T_{F,n} à 1e−12 S^F ; Div_F du tour n + 1 abaissé
      de ΔT (1 + Γ^e + i_D/n_a) (rattrapage, impôt anticipé, intérêts sur les dépôts
      d'ouverture), à 1e−12 relatif."""
    sentier = socle.sentier(0.02)
    n = TOUR_DU_LEVIER
    _, base = derouler(socle, sentier, NB_PAS_DES_DELAIS)
    mesures = {}
    lignes = []
    for nom, valeurs, ligne, signe in (("impôt des ménages (τ_H + 0,01)",
                                         {"tau_H": sentier.par.tau_H + 0.01}, "7", -1.0),
                                        ("transferts (θ_Tr = 0,001)", {"theta_Tr": 0.001}, "6",
                                         1.0)):
        _, choc = derouler(socle, sentier, NB_PAS_DES_DELAIS,
                           bloc_9=bloc_9_compose(levier_au_tour(n, **valeurs)))
        mesures[f"{nom}, ligne {ligne}"] = (_premier_ecart(base, choc, lambda p, q=ligne: p[q]),
                                            (n, 1.0))
        mesures[f"{nom}, C^plan (H5)"] = (_premier_ecart(base, choc, _plan), (n + 1, signe))
        mesures[f"{nom}, ligne 1 (H6)"] = (_premier_ecart(base, choc, lambda p: p["1"]),
                                           (n + 1, signe))
    _, t_f = derouler(socle, sentier, NB_PAS_DES_DELAIS,
                      bloc_9=bloc_9_compose(levier_au_tour(n, tau_F=0.01)))
    delta_T = t_f.pas[n]["variables"]["T_F"]
    e_b, e_c = base.pas[n]["etat"], t_f.pas[n]["etat"]
    s_f = idt.echelle_bilan(_positions(e_b), "entreprises")
    ecart_d_f = abs((e_b.D_F - e_c.D_F) - delta_T) / s_f
    gamma_e = base.pas[n + 1]["grandeurs"]["Gamma_e"]
    baisse = base.pas[n + 1]["14"] - t_f.pas[n + 1]["14"]
    attendu = delta_T * (1.0 + gamma_e + par_pas(TauxDeFlux(e_b.i_D)))
    ecart_div = abs(baisse / attendu - 1.0)
    mesures["impôt des entreprises (τ_F = 0,01), ligne 14 (F3)"] = (
        _premier_ecart(base, t_f, lambda p: p["14"]), (n + 1, -1.0))
    lignes += [f"{nom} : premier tour modifié {m[0]}, signe {m[1]:+.0f} (attendu : tour {a[0]}, "
               f"signe {a[1]:+.0f})" for nom, (m, a) in mesures.items()]
    lignes.append(f"impôt des entreprises : ΔT = {delta_T:.6e} ; D_F de clôture du tour {n} − ΔT "
                  f"à {ecart_d_f:.1e} S^F ; Div_F du tour {n + 1} − {baisse / delta_T:.12f} ΔT "
                  f"(attendu 1 + Γ^e + i_D/n_a = {attendu / delta_T:.12f}, écart "
                  f"{ecart_div:.1e})")
    publier(f"Délais des fiches 5 et 6 sur la chaîne réelle E3, E6, E5 → H6, F3, levier au tour "
            f"{n}, π* = 2 % ({ETIQUETTE})", lignes)
    for nom, (mesure, attendu_) in mesures.items():
        assert mesure == attendu_, nom
    assert delta_T > 0.0 and t_f.pas[n]["14"] == base.pas[n]["14"]
    assert ecart_d_f <= SEUIL_DELAIS and ecart_div <= SEUIL_DELAIS


def _colonne_des_menages(p, ligne):
    """Montant exécuté de la ligne `ligne` dans la colonne des ménages (signé)."""
    somme = 0.0
    for terme in cat.LIGNE[ligne].termes:
        if terme.colonne_plus == "menages":
            somme += p[f"{ligne}:termes"][terme.nom]
        elif terme.colonne_moins == "menages":
            somme -= p[f"{ligne}:termes"][terme.nom]
    return somme


LIGNES_DU_REVENU = ("5", "6", "7", "10", "11a", "14", "15")


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_theta_H_aux_deux_sens(socle, pi, publier):
    """C52 (critère 14 (c) de la fiche 9), ligne (b), publiée sans verdict, θ_H aux deux sens :
    - **part d'une vente imprévue** qui atteint les ménages : ΔDiv_F/ΔG au tour n = 5 (ligne 14
      sur ligne 2, dépense θ_G × 1,01 au seul tour n contre le contrôle apparié, moteur) ;
      repère de la maquette (fiche 9, § 3.C-4) : 0,4983 ;
    - **au sens de la l. 1543** (ΔYD/Δ(p·y), production marginale non vendue), par appel direct
      de F3 et de H7 sur les montants du tour n du contrôle : Δy = 1e−3 y, ΔWB = UC Δy, Δ(p·y)
      = p Δy, ΔL = 0 (F2 finance la masse salariale d'une production invendue sur le
      dividende) ; F3 recalculé égal au bit à la ligne 14 avant la variation ; repère : 0 sous
      C-HS. Le rayon de la boucle de `sec:menages` refait avec les impôts n'est pas mesuré ici."""
    sentier = socle.sentier(pi)
    n = TOUR_DU_LEVIER
    _, base = derouler(socle, sentier, n + 1)
    _, g = derouler(socle, sentier, n + 1,
                    bloc_9=bloc_9_compose(choc_de_theta_G(1.01, debut=n, duree=1)))
    pb, pg = base.pas[n], g.pas[n]
    theta_vente = (pg["14"] - pb["14"]) / (pg["2"] - pb["2"])
    o = base.pas[n - 1]["etat"]
    v = pb["variables"]
    D_F = max(0.0, o.D_F)
    entrees = dict(D_F=D_F, Delta_L=pb["18"], C=pb["1"], G=pb["2"], WB=pb["5"],
                   interets_L=par_pas(TauxDeFlux(o.i_L)) * o.L,
                   interets_D_F=par_pas(TauxDeFlux(o.i_D)) * D_F, T_e_F=v["T_e_F"],
                   D_etoile_F=v["D_etoile_F"])
    assert bloc_6.dividendes(**entrees) == pb["14"]
    delta_y = 1e-3 * v["y"]
    delta_WB = v["UC"] * delta_y
    div_varie = bloc_6.dividendes(**{**entrees, "WB": pb["5"] + delta_WB})
    montants = {ligne: _colonne_des_menages(pb, ligne) for ligne in LIGNES_DU_REVENU}
    yd = bloc_5.revenu_disponible(tuple(montants[ligne] for ligne in LIGNES_DU_REVENU))
    varies = {**montants, "5": montants["5"] + delta_WB,
              "14": montants["14"] + (div_varie - pb["14"])}
    yd_varie = bloc_5.revenu_disponible(tuple(varies[ligne] for ligne in LIGNES_DU_REVENU))
    theta_1543 = (yd_varie - yd) / (v["p"] * delta_y)
    publier(f"θ_H (C52), π* = {100 * pi:g} % ({ETIQUETTE} ; sans verdict)", [
        f"part de la vente imprévue ΔDiv_F/ΔG au tour {n} (moteur) : {theta_vente:.4f} "
        "(repère de la maquette : 0,4983)",
        f"θ_H au sens de la l. 1543, ΔYD/Δ(p·y) par appel direct de F3 et H7 : "
        f"{theta_1543:.2e} (ΔWB/Δ(p·y) = {delta_WB / (v['p'] * delta_y):.4f}, ΔDiv_F/Δ(p·y) = "
        f"{(div_varie - pb['14']) / (v['p'] * delta_y):.4f} ; repère : 0 sous C-HS)"])


# --------------------------------------------------------------------------
# Parts non payées (critère 12, F9, P157), placement raté (P90), bornes (critère 16)
# --------------------------------------------------------------------------


def test_transferts_non_verses_par_appel_direct(socle):
    """F9 : θ_Tr > 0 (0,01) déclaré en appel direct, sur l'état résolu inchangé (θ_Tr = 0) :
    plafond de E6 large, Tr = Tr^lev et rien de non versé ; compte du Trésor ramené à la moitié
    du plan : Tr < Tr^lev, part non versée Tr^lev − Tr > 0 enregistrée (E13), Tr ≥ 0."""
    es = socle.script()
    par = dataclasses.replace(es.Parametres(), pi_cible=0.02, nu_G=socle.NU_G)
    e = es.etat_stationnaire(par)
    o = es.ouverture(e, par)
    y_pot = bloc_9.production_potentielle(o["pr"], par.U_eq, o["N_pa"])
    Tr_lev = bloc_9.transferts_vises(o["registre"][0], e["pis"], 0.01, y_pot)
    interets = e["i_CB"] / N_A * e["B"]
    Tr = bloc_9.transferts(Tr_lev, o["M_G"], e["T_H"], interets, e["G"])
    assert Tr == Tr_lev and bloc_9.part_non_payee(Tr_lev, Tr) == (Tr_lev, 0.0)
    G_plan = 0.5 * o["M_G"]
    Tr = bloc_9.transferts(Tr_lev, 0.5 * G_plan, 0.0, interets, G_plan)
    paye, non_verse = bloc_9.part_non_payee(Tr_lev, Tr)
    assert Tr == 0.0 and paye == 0.0 and non_verse == Tr_lev > 0.0


def test_perte_non_couverte_par_appel_direct():
    """P157, cas (ii), par appel direct sur le grand livre : perte de la banque centrale égale à
    deux fois l'encaisse (C60, Π^CB = −20, M^G = 10), montant couvert déclaré par E13 sur
    max(0 ; M^{G,8a}) : le noyau exécute −mc ; ΔE^CB_t = −(perte non couverte)_t à 1e−12 S^CB,
    par les flux (V^flux) et par le stock."""
    ouverture = {"D_H": 100.0, "D_F": 50.0, "L": 100.0, "B_H": 0.0, "B_Bk": 0.0, "B_CB": 0.0,
                 "Res": 2000.0, "L_CB": 0.0, "M_G": 10.0, "K": 50.0, "IN": 10.0}
    v = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(ouverture, s) for s in cat.SECTEURS}
    variables = {nom: 0.0 for nom in (v_.nom for v_ in schema.VARIABLES_DES_BLOCS)}
    variables.update(v_e=1.0, IN_vol=1.0, pr=1.0, K_vol=1.0, W=1.0, N=1.0, N_pa=1.0, ti=0.1)
    etat = schema.EtatPays(identifiant="A", graine=1, t=0, registre_prix=(1.0,) * 13,
                           **ouverture, **v, **variables)

    @dataclasses.dataclass(frozen=True)
    class _Cadre:
        tolerance_identite_pas: float = EPS
        tolerance_identite_cumulee: float = CADRE.tolerance_identite_cumulee
    gl = ouvrir_pas(etat, _Cadre())
    Pi_CB = -par_pas(TauxDeFlux(0.12)) * ouverture["Res"]  # −20 : i_CB > 0, Res ≫ L^CB + B_CB
    perte = 0.0 - Pi_CB
    for phase in cat.PHASES:
        for ligne in cat.LIGNES_DE_LA_PHASE[phase]:
            if ligne.proposant is None:
                continue
            termes = {t.nom: 0.0 for t in ligne.termes}
            if ligne.identifiant == "12":
                termes["ires_Res"] = perte
            if ligne.identifiant == "16":
                termes["Pi_CB"] = Pi_CB
            gl.proposer(FluxPropose(ligne.identifiant, termes, ligne.proposant))
        if phase == "8b":
            mc, non_couverte = bloc_9.part_non_payee(perte, gl.position("M_G"))
            gl.declarer_montant_couvert("16", mc, "finances_publiques")
        gl.clore_phase(phase)
    assert (mc, non_couverte) == (10.0, 10.0)
    s_cb = gl.echelle("banque_centrale")
    v_flux = gl.valeur_nette_flux("banque_centrale")
    assert abs((v_flux - v["V_flux_banque_centrale"]) + non_couverte) <= SEUIL_FLUX * s_cb
    assert abs(gl.valeur_nette_stock("banque_centrale") - v_flux) <= SEUIL_FLUX * s_cb
    assert gl.montant_execute_ligne("16") == -mc


def test_impot_superieur_aux_depots_defaut_declare(socle):
    """Critère 12, cas (iii) : un impôt des ménages supérieur à leurs dépôts produit le défaut
    déclaré (`sec:finances_publiques-caisse`) : arrêt typé du noyau (`DefautComptable`) à la
    clôture de la phase 6, contrôle de caisse des ménages ; jamais un ajustement."""
    sentier = socle.sentier(0.02)
    initial = socle.etat_initial(sentier)
    # Assiette d'ouverture × 100 : l'impôt du pas (τ_H Γ^e Y^HS_{t−1}) dépasse les dépôts
    # d'ouverture (36 impôts du sentier) augmentés des revenus du pas.
    etat = dataclasses.replace(initial, Y_HS_m1=100.0 * initial.Y_HS_m1)
    with pytest.raises(DefautComptable) as defaut:
        derouler(socle, sentier, 1, initial=etat)
    d = defaut.value
    assert (d.t, d.phase, d.secteur, d.moyen, d.ligne) == (0, "6", "menages", "D_H", "7")
    assert d.regle == "eq:noyau-caisse-nette" and d.lignes_debitrices == ("7",)
    assert d.position_debut > 0.0 > d.position_fin


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_placement_rate_de_moitie_sur_un_tour(socle, pi, publier):
    """P90, « Placement raté » ; critère 12 : ς_B = 0,5 au pas 5 : M^G de clôture = M^G* − ς_B
    (Em − ΔB^prim_CB) à 1e−12 S^G ; Res L^CB = 0 exactement à la clôture (B7) ; aucun arrêt, aucune
    part non payée ; au pas suivant, plafond de E1 publié (actif ou non)."""
    sentier = socle.sentier(pi)
    _, r = derouler(socle, sentier, 24, varsigma_B=lambda t: 0.5 if t == 5 else 0.0)
    p = r.pas[5]
    v, f = p["variables"], p["etat"]
    attendu = v["M_G_etoile"] - 0.5 * (v["Em"] - p["19a-BC"])
    s_g = idt.echelle_bilan(_positions(r.pas[4]["etat"]), "etat")
    assert abs(f.M_G - attendu) <= SEUIL_FLUX * s_g
    assert all(q["etat"].Res * q["etat"].L_CB == 0.0 for q in r.pas)
    assert all(q["variables"]["perte_non_couverte"] == 0.0
               and q["variables"]["Tr_non_verses"] == 0.0 for q in r.pas)
    actifs = [q["t"] for q in r.pas if _actif(q)]
    publier(f"Placement raté de moitié au pas 5, π* = {100 * pi:g} % ({ETIQUETTE})", [
        f"M^G de clôture − (M^G* − ς_B (Em − ΔB^prim_CB)) = {f.M_G - attendu:.1e} u.m. "
        f"(S^G = {s_g:.3e}) ; M^G/M^G* = {f.M_G / v['M_G_etoile']:.6f}",
        "plafond de E1 actif aux pas : " + (str(actifs) if actifs else "aucun")])


@pytest.mark.parametrize("nom, choc", [
    ("placement raté de moitié aux tours 1 à 12", "placement"),
    ("dépense doublée aux tours 1 à 12", "depense")])
def test_bornes_plafond_desactive_sous_douze_tours(socle, nom, choc, publier):
    """Critère 16 (bornes), π* = 2 % : sous un placement raté de moitié ou une dépense doublée aux
    tours 1 à 12, le plafond de E1 est désactivé au plus tard 12 tours après la fin du choc, sans
    réactivation ; aucun arrêt du noyau."""
    sentier = socle.sentier(0.02)
    if choc == "placement":
        _, r = derouler(socle, sentier, 120,
                        varsigma_B=lambda t: 0.5 if t < TOURS_DU_CHOC else 0.0)
    else:
        _, r = derouler(socle, sentier, 120, bloc_9=bloc_9_compose(choc_de_theta_G(2.0)))
    actifs = [p["t"] for p in r.pas if _actif(p)]
    fin = TOURS_DU_CHOC - 1 + DELAI_DE_DESACTIVATION
    assert all(t <= fin for t in actifs), actifs[-5:]
    publier(f"Bornes, {nom}, π* = 2 % ({ETIQUETTE})", [
        "plafond de E1 actif aux pas : " + (f"{actifs[0]} à {actifs[-1]} ({len(actifs)} pas)"
                                             if actifs else "aucun")
        + f" ; limite écrite : pas {fin}"])


# --------------------------------------------------------------------------
# Couverture sur le moteur (F6, F7)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_couverture_d_un_choc_de_taux_au_tour_n(socle, pi):
    """F6 : r̂* relevé de 0,01 dans l'état d'ouverture (i_CB du tour relevé de Δ), contre le
    contrôle : au tour n seul, Div_Bk (ligne 15) varie de Δ (B_Bk + Res − L^CB)/n_a, T^cou reprend
    Δ A/n_a, A = B − M^G − E^CB, et le revenu disponible des ménages ne varie pas (B_H = 0), à
    1e−12 relatif ; les autres revenus des ménages sont inchangés au bit."""
    sentier = socle.sentier(pi)
    initial = socle.etat_initial(sentier)
    _, c = derouler(socle, sentier, 1)
    _, s = derouler(socle, sentier, 1,
                    initial=dataclasses.replace(initial, r_hat_etoile=initial.r_hat_etoile + 0.01))
    pc, ps = c.pas[0], s.pas[0]
    delta = par_pas(TauxDeFlux(ps["variables"]["i_CB"] - pc["variables"]["i_CB"]))
    o = initial
    A = o.B_H + o.B_Bk + o.B_CB - o.M_G - (o.B_CB + o.L_CB - o.Res - o.M_G)
    d_div = ps["15"] - pc["15"]
    d_cou = ps["variables"]["T_cou"] - pc["variables"]["T_cou"]
    assert abs(d_div / (delta * (o.B_Bk + o.Res - o.L_CB)) - 1.0) <= SEUIL_FLUX
    assert abs(d_cou / (delta * A) - 1.0) <= SEUIL_FLUX
    assert abs(ps["etat"].YD_m1 / pc["etat"].YD_m1 - 1.0) <= SEUIL_FLUX
    for ligne in ("5", "6", "10", "11a", "14"):
        assert ps[f"{ligne}:termes"] == pc[f"{ligne}:termes"], ligne


def test_ligne_11c_egale_au_premier_terme_de_pi_cb(socle):
    """F7 : sous θ_CB = 0,5 (B_CB > 0), la ligne 11c (E7) égale au bit le premier terme de Π^CB
    (BC6, i_B B_CB/n_a), à chaque pas."""
    sentier = socle.sentier(0.02, theta_CB=0.5)
    initial = socle.etat_initial(sentier)
    _, r = derouler(socle, sentier, 24)
    ouvertures = [initial] + [p["etat"] for p in r.pas[:-1]]
    assert initial.B_CB > 0.0
    for o, p in zip(ouvertures, r.pas):
        assert p["11c"] == par_pas(TauxDeFlux(p["variables"]["i_CB"])) * o.B_CB


# --------------------------------------------------------------------------
# C59 : neutralité de ν_G et de θ_CB (P156, P160)
# --------------------------------------------------------------------------


def _reelles(p, o):
    """Grandeurs réelles et revenus non financiers comparés par C59 : production, prix, taux,
    salaires, dividende des entreprises, revenu disponible, dette consolidée/(n_a PIB)."""
    v = p["variables"]
    pib = p["1"] + p["2"] + p["3"] + p["4"]
    e_cb = o.B_CB + o.L_CB - o.Res - o.M_G
    return {"y": v["y"], "p": v["p"], "i_CB": v["i_CB"], "WB": p["5"], "Div_F": p["14"],
            "YD": p["etat"].YD_m1,
            "dette consolidée/(n_a PIB)": (o.B_H + o.B_Bk + o.B_CB - o.M_G - e_cb) / (N_A * pib)}


def _ecart_c59(socle, ref, autre, initiaux):
    pires = {}
    for t, (a, b) in enumerate(zip(ref.pas, autre.pas, strict=True)):
        oa = initiaux[0] if t == 0 else ref.pas[t - 1]["etat"]
        ob = initiaux[1] if t == 0 else autre.pas[t - 1]["etat"]
        xa, xb = _reelles(a, oa), _reelles(b, ob)
        for cle in xa:
            pires[cle] = max(pires.get(cle, 0.0), abs(xb[cle] / xa[cle] - 1.0))
    return pires


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_c59_neutralite_de_nu_G(socle, pi, publier):
    """C59 (P156) : ν_G ∈ {1,1 ; 1,2} contre la référence 1,15, chacun depuis son état résolu,
    720 pas : production, prix, taux, revenus non financiers et dette consolidée égaux à 1e−10
    relatif. (L'écart de M^G, B_Bk et L^CB à Δν_G PB se juge sur la marche de ν_G, où PB est
    commun aux deux trajectoires : `test_c59_marche_de_nu_G_en_cours_de_trajectoire`.)"""
    ref_s = socle.sentier(pi)
    _, ref = derouler(socle, ref_s, NB_PAS)
    lignes = []
    for nu_G in (1.1, 1.2):
        s = socle.sentier(pi, nu_G=nu_G)
        _, autre = derouler(socle, s, NB_PAS)
        pires = _ecart_c59(socle, ref, autre, (socle.etat_initial(ref_s), socle.etat_initial(s)))
        assert max(pires.values()) <= SEUIL_C59_TRAJECTOIRE, pires
        lignes.append(f"ν_G = {nu_G:g} : max relatif sur 720 pas " + " ; ".join(
            f"{c} {x:.1e}" for c, x in pires.items()))
    publier(f"C59, neutralité de ν_G, π* = {100 * pi:g} % ({ETIQUETTE})", lignes)


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_c59_neutralite_de_theta_CB(socle, pi, publier):
    """C59 et « Neutralité de s_CB » de la fiche 8 (P160) : θ_CB ∈ {0,05 ; 0,5} contre 0, 720 pas :
    allocations (production, prix, taux, revenus, dette consolidée) égales à 1e−10 relatif ; à la
    clôture de 8c, Res = max(0 ; B_CB − M^G − E^CB) et L^CB = max(0 ; M^G + E^CB − B_CB) à
    ε S^CB."""
    ref_s = socle.sentier(pi)
    _, ref = derouler(socle, ref_s, NB_PAS)
    lignes = []
    for theta_CB in (0.05, 0.5):
        s = socle.sentier(pi, theta_CB=theta_CB)
        initial = socle.etat_initial(s)
        _, autre = derouler(socle, s, NB_PAS)
        pires = _ecart_c59(socle, ref, autre, (socle.etat_initial(ref_s), initial))
        assert max(pires.values()) <= SEUIL_C59_TRAJECTOIRE, pires
        pire_bc = 0.0
        for p in autre.pas:
            f = p["etat"]
            e_cb = getattr(f, cat.VALEUR_NETTE_FLUX["banque_centrale"])
            s_cb = idt.echelle_bilan(_positions(f), "banque_centrale")
            pire_bc = max(pire_bc, abs(f.Res - max(0.0, f.B_CB - f.M_G - e_cb)) / s_cb,
                          abs(f.L_CB - max(0.0, f.M_G + e_cb - f.B_CB)) / s_cb)
        assert pire_bc <= EPS
        lignes.append(f"θ_CB = {theta_CB:g} : max relatif sur 720 pas " + " ; ".join(
            f"{c} {x:.1e}" for c, x in pires.items())
            + f" ; Res et L^CB à leur forme exacte : {pire_bc:.1e} S^CB")
    publier(f"C59, neutralité de θ_CB (et de s_CB, P160), π* = {100 * pi:g} % ({ETIQUETTE})",
            lignes)


def test_c59_marche_de_nu_G_en_cours_de_trajectoire(socle, publier):
    """C59 (P156) : ν_G porté de 1,15 à 1,2 au pas 360, π* = 2 % : grandeurs réelles et revenus
    non financiers égaux au contrôle à 1e−10 relatif sur 720 pas ; à la clôture du pas 360, M^G,
    B_Bk et L^CB écartés du contrôle de Δν_G PB_360 à 1e−12 S (PB commun : ouverture identique)."""
    sentier = socle.sentier(0.02)
    _, ref = derouler(socle, sentier, NB_PAS)

    def marche(t, table):
        return varier(table, nu_G=1.2) if t >= 360 else table
    _, autre = derouler(socle, sentier, NB_PAS, bloc_9=bloc_9_compose(marche))
    initial = socle.etat_initial(sentier)
    pires = _ecart_c59(socle, ref, autre, (initial, initial))
    assert max(pires.values()) <= SEUIL_C59_TRAJECTOIRE, pires
    a, b = ref.pas[360], autre.pas[360]
    PB = a["2"] + a["6"] + a["11a"] + a["11b"] + a["11c"]
    assert PB == b["2"] + b["6"] + b["11a"] + b["11b"] + b["11c"]
    delta = (1.2 - socle.NU_G) * PB
    s_ref = max(idt.echelle_bilan(_positions(ref.pas[359]["etat"]), q) for q in cat.SECTEURS)
    ecarts = {q: (getattr(b["etat"], q) - getattr(a["etat"], q)) - delta
              for q in ("M_G", "B_Bk", "L_CB")}
    assert all(abs(x) <= SEUIL_FLUX * s_ref for x in ecarts.values()), ecarts
    publier(f"C59, marche de ν_G 1,15 → 1,2 au pas 360, π* = 2 % ({ETIQUETTE})", [
        "max relatif sur 720 pas : " + " ; ".join(f"{c} {x:.1e}" for c, x in pires.items()),
        "écarts de M^G, B_Bk, L^CB à Δν_G PB_360 (/S) : " + " ; ".join(
            f"{q} {x / s_ref:.1e}" for q, x in ecarts.items())])


# --------------------------------------------------------------------------
# Reprise (critère 2), publications (b)
# --------------------------------------------------------------------------


class Empreinte:
    def __init__(self):
        self.evenements = []

    def relever(self, e):
        self.evenements.append(e)


def test_reprise_exacte_sous_phi_nul_et_placement_rate(socle):
    """Critère 2 (phases et empreinte) : reprise exacte, y compris sous φ = 0 et ς_B ≠ 0 :
    sauvegarde v5 rechargée aux pas 1 et 30 d'une trajectoire de 60 pas (ς_B = 0,3 aux pas 10 à
    40) ; clôtures et états identiques au bit à ceux de la trajectoire continue."""
    sentier = socle.sentier(0.02)
    tables = socle.parametres_du_sentier(sentier)
    tables = dataclasses.replace(tables, finances_publiques=varier(tables.finances_publiques,
                                                                   phi=0.0))

    def part(t):
        return 0.3 if 10 <= t <= 40 else 0.0
    continu = Empreinte()
    fin, _ = derouler(socle, sentier, 60, parametres=tables, varsigma_B=part,
                      observateur=continu)
    for k in (1, 30):
        avant, apres = Empreinte(), Empreinte()
        milieu, _ = derouler(socle, sentier, k, parametres=tables, varsigma_B=part,
                             observateur=avant)
        document = sauvegarder([milieu])
        assert b'"version": 5' in document and b'"Y_HS_m1"' in document
        repris, = charger(document)
        assert repris == milieu
        fin_reprise, _ = derouler(socle, sentier, 60 - k, initial=repris, parametres=tables,
                                  varsigma_B=part, observateur=apres)
        assert sauvegarder([fin_reprise]) == sauvegarder([fin]), k
        assert avant.evenements + apres.evenements == continu.evenements, k


def _sous_phi_nul(socle, sentier):
    tables = socle.parametres_du_sentier(sentier)
    return dataclasses.replace(tables, finances_publiques=varier(tables.finances_publiques,
                                                                 phi=0.0))


def _ecarts_de_taux_sous_phi_nul(socle, sentier, facteur, nb_pas):
    """Choc θ_G × `facteur` aux tours 1 à 12 contre un contrôle apparié, tous deux sous φ = 0 :
    (|Δi_CB| par pas sur les pas relevés de la trajectoire choquée, arrêt publié)."""
    tables = _sous_phi_nul(socle, sentier)
    _, c = derouler(socle, sentier, nb_pas, parametres=tables)
    s = Releve()
    arret = f"aucun arrêt sur {nb_pas} pas"
    try:
        derouler(socle, sentier, nb_pas, parametres=tables, observateur=s,
                 bloc_9=bloc_9_compose(choc_de_theta_G(facteur)))
    except (RefusDuMoteur, DefautComptable) as refus:
        # Divergence de la boucle sous φ = 0 (régime explosif déclaré, `sec:finances_publiques-
        # impots`) : la trajectoire choquée sort d'un domaine ; fait publié, sans verdict.
        arret = f"arrêt au pas {len(s.pas)} : {refus}"
    return [abs(a["variables"]["i_CB"] - b["variables"]["i_CB"])
            for a, b in zip(c.pas, s.pas)], arret


@pytest.mark.parametrize("pi", [0.02, 0.10])
def test_temps_de_doublement_sous_phi_nul(socle, pi, publier):
    """C62 (F11), ligne (b), publié sans verdict : sous φ = 0 (« intérêts financés par le
    déficit »), choc G^plan +1 % aux tours 1 à 12 contre un contrôle apparié sous φ = 0 ; écart
    de i_CB, ρ̂ = (max_{tours 600 à 720} |écart| / max_{tours 240 à 360} |écart|)^{1/360},
    temps de doublement ln 2/ln ρ̂ (si ρ̂ > 1), les deux fenêtres de 120 pas. Valeurs de la
    maquette : 382 et 63 tours. Une
    sortie de domaine de la trajectoire choquée (régime explosif) est publiée avec son pas, la
    seconde fenêtre étant alors les 120 derniers pas relevés ; si l'arrêt laisse moins de deux
    fenêtres disjointes après le pas 240, la mesure est publiée sans ρ̂. Un choc de 1 % sort du
    régime linéaire (à 10 %, arrêt de la trajectoire choquée) : la valeur publiée n'est pas une
    racine ; la mesure en régime linéaire est `test_temps_de_doublement_en_regime_lineaire`
    (décision du mainteneur du 15/11/2026 : les deux mesures sont publiées)."""
    sentier = socle.sentier(pi)
    ecarts, arret = _ecarts_de_taux_sous_phi_nul(socle, sentier, 1.01, NB_PAS)
    fin = len(ecarts)
    titre = (f"C62, temps de doublement sous φ = 0, choc de 1 %, π* = {100 * pi:g} % "
             f"({ETIQUETTE} ; sans verdict)")
    if fin < 360 + 120:
        publier(titre, [f"trajectoire choquée arrêtée avant deux fenêtres disjointes de 120 "
                        f"pas après le pas 240 ({fin} pas relevés) : aucun ρ̂ publié ; {arret}"])
        return
    premier, dernier = max(ecarts[240:360]), max(ecarts[fin - 120:fin])
    duree = (fin - 60) - 300  # entre les centres des deux fenêtres de 120 pas
    rho = (dernier / premier) ** (1.0 / duree) if premier > 0.0 else math.nan
    doublement = math.log(2.0) / math.log(rho) if rho > 1.0 else math.inf
    publier(titre, [
        f"ρ̂ = {rho:.6f} ; temps de doublement = {doublement:.0f} tours "
        f"(maquette : {382 if pi == 0.02 else 63}) ; |Δi_CB| tours 240–360 : "
        f"{premier:.2e}, {fin - 120}–{fin} : {dernier:.2e} ; {arret}",
        "choc de 1 % hors du régime linéaire : "
        + ("31 tours à 10 % n'est pas une racine : sortie du régime linéaire"
           if pi == 0.10 else "valeur à lire contre la mesure en régime linéaire")])


# Mesure complémentaire de C62 en régime linéaire (décision du mainteneur du 15/11/2026).
FACTEUR_LINEAIRE = 1.0 + 1e-6
NB_PAS_LINEAIRE = 2700
FENETRE_LINEAIRE = 120
DEBUT_DES_FENETRES = NB_PAS_LINEAIRE % FENETRE_LINEAIRE  # 60 : la dernière finit au pas 2 700


@pytest.mark.parametrize("pi", [0.02, 0.10])
def test_temps_de_doublement_en_regime_lineaire(socle, pi, publier):
    """C62 (F11), mesure complémentaire en régime linéaire, publiée sans verdict : sous φ = 0,
    choc θ_G × (1 + 1e−6) aux tours 1 à 12 contre un contrôle apparié sous φ = 0, 2 700 pas ;
    |Δi_CB| maximal sur des fenêtres de 120 pas [60 + 120 k ; 180 + 120 k[ jusqu'au pas 2 700,
    ρ̂ d'une fenêtre = (max de la fenêtre / max de la précédente)^{1/120}, temps de doublement
    ln 2/ln ρ̂. Une fenêtre que l'arrêt de la trajectoire choquée laisse incomplète n'est pas
    publiée ; l'arrêt l'est. Repères de `macro`, non à reproduire : environ 1,001819 (381 tours)
    à 2 %, 1,011038 (63 tours) à 10 %."""
    sentier = socle.sentier(pi)
    ecarts, arret = _ecarts_de_taux_sous_phi_nul(socle, sentier, FACTEUR_LINEAIRE,
                                                 NB_PAS_LINEAIRE)
    debuts = [d for d in range(DEBUT_DES_FENETRES, NB_PAS_LINEAIRE, FENETRE_LINEAIRE)
              if d + FENETRE_LINEAIRE <= len(ecarts)]
    maxima = [max(ecarts[d:d + FENETRE_LINEAIRE]) for d in debuts]
    lignes = []
    for d, avant, apres in zip(debuts[1:], maxima, maxima[1:]):
        rho = (apres / avant) ** (1.0 / FENETRE_LINEAIRE) if avant > 0.0 else math.nan
        doublement = math.log(2.0) / math.log(rho) if rho > 1.0 else math.inf
        lignes.append(f"pas {d}–{d + FENETRE_LINEAIRE - 1} : max |Δi_CB| = {apres:.3e} ; "
                      f"ρ̂ = {rho:.6f} ; temps de doublement = {doublement:.0f} tours")
    publier(f"C62 en régime linéaire, choc θ_G × (1 + 1e−6), φ = 0, π* = {100 * pi:g} % "
            f"({ETIQUETTE} ; sans verdict ; repère de `macro` : "
            f"{'1,001819 (381 tours)' if pi == 0.02 else '1,011038 (63 tours)'})",
            [*lignes, arret])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_marge_de_caisse_des_menages_publiee(banc, socle, pi, publier):
    """`sec:finances_publiques-caisse`, ligne (b) reçue des fiches 5 et 6, publiée sans verdict :
    dépôts d'ouverture des ménages rapportés à l'impôt du pas (36 à n_a = 12, ν_H = 1 an,
    τ_H = 0,25, script) ; revenu disponible égal à la somme des lignes 5, 6, 7, 10, 11a, 14 et 15
    de la colonne des ménages à 1e−12 S^H (fiche 5, « Revenu par le grand livre »)."""
    _, initial, releve = banc[pi]
    ouvertures = [initial] + [p["etat"] for p in releve.pas[:-1]]
    rapports = [o.D_H / p["variables"]["T_H"] for o, p in zip(ouvertures, releve.pas)]
    pire = 0.0
    for o, p in zip(ouvertures, releve.pas):
        somme = 0.0
        for ligne in ("5", "6", "7", "10", "11a", "14", "15"):
            termes = p[f"{ligne}:termes"]
            for terme in cat.LIGNE[ligne].termes:
                if terme.colonne_plus == "menages":
                    somme += termes[terme.nom]
                elif terme.colonne_moins == "menages":
                    somme -= termes[terme.nom]
        s_h = idt.echelle_bilan(_positions(o), "menages")
        pire = max(pire, abs(p["etat"].YD_m1 - somme) / s_h)
    assert pire <= SEUIL_FLUX
    publier(f"Marge de caisse des ménages, π* = {100 * pi:g} % ({ETIQUETTE} ; sans verdict)", [
        f"D_H d'ouverture / T_H du pas : min {min(rapports):.4f}, max {max(rapports):.4f} ; "
        f"YD = Σ lignes de la colonne des ménages à {pire:.1e} S^H"])
