"""Socle complet : blocs 2 à 9 réels, aucun bloc d'essai (#132, rang 3 de J3-d2).

**Banc** (critère « Branche » de la feuille de route, § 1 ; ADR 0013, annotation du 15/11/2026
(J3-d2), point 6) : `socle.blocs_du_socle_complet()`, tables alignées sur le sentier du script
(`socle.parametres_du_sentier`, θ_G résolu compris), n_a = 12, **ν_G = 1,15 passé explicitement**
au script (défaut ν_G = 1, hors domaine), π* ∈ {0 ; 2 % ; 10 %}, état initial résolu par
`nations.scenarios.initial.etat_initial` aux tables du sentier (`socle.etat_initial`, #175).
Étiquette : `ETIQUETTE`.
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
  **reprise** (critère 2) : seuils au docstring de chaque test ;
- **endettement, dépôts** de la fiche 6 sous ϖ_L + 2 points (#139, critère de #169 ; P324,
  P330) : seuil au docstring du test ;
- **bornes (c)** de la fiche 6 sous le refus de la moitié du crédit aux tours 1 à 12 (#140,
  P150) : critère au docstring du test ;
- **#131, point 2** (mesure, constat sans verdict du modèle ; protocole de `monnaie` écrit avant
  l'essai, `17c26c2`) : terme de Jensen de BC2 sous les formes (A), bloc 8 réel, et (L), BC2 en
  log par sous-classe du bloc 8 dans `tests/` ; seuls les contrôles de validité K1 à K4 sont
  assertés, la classification (F), (C) ou (I) est publiée.

Réaffirmés avec le bloc 9 réel (P162) : « Délais » des fiches 5 et 6, signe et date exacts sur la
chaîne E3, E6, E5 → H6, F3.

Publiés sans verdict (lignes (b)) : marge de caisse (h_max), retour après −5 % à n_a = 52 (appel
direct, critère 11), θ_H aux deux sens (C52), racine dominante et temps de doublement sous φ = 0
(C62 : choc de 1 %, F11, et régime linéaire, décision du mainteneur du 15/11/2026 ; racine
identifiée sur le moteur, maquette en regard, #166), marge de
`sec:finances_publiques-caisse`, et, remesurés à la table T1 (#171) : nombre de tours de
rationnement au retour d'une baisse de 5 % sous une encaisse visée à ν_G = 1 (n°1, P274, bloc 9
dérivé dans `tests/`), premier pas d'un écart d'un point du taux directeur sous φ = 0 (n°4),
P_36 d'une hausse de taux d'un point aux tours 1 à 12 sous φ ∈ {0 ; 1} (n°6, P275).
Aucune mesure ici ne vaut résultat final (J3-e).
"""

import dataclasses
import math
from typing import NamedTuple

import numpy as np
import pytest

from nations.blocs import banque_centrale as bloc_8
from nations.blocs import finances_publiques as bloc_9
from nations.blocs import investissement as bloc_6
from nations.blocs import menages as bloc_5
from nations.blocs.banque_centrale import BanqueCentrale, taux_indique_par_la_regle
from nations.blocs.finances_publiques import FinancesPubliques
from nations.etat import prix, schema
from nations.etat.sauvegarde import charger, sauvegarder
from nations.etat.variables import Invariance
from nations.moteur import calendrier, registre
from nations.moteur import ordonnanceur as ordo
from nations.moteur.conversions import TauxDeFlux, par_pas
from nations.moteur.diagnostics import ArretMoteur, RefusDuMoteur
from nations.moteur.parametres import varier
from nations.moteur.parametres.cadre import CADRE, PAS_PAR_AN
from nations.moteur.phases import PHASES
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.diagnostics import ArretNoyau, DefautComptable
from nations.noyau.grand_livre import ClotureDePhase, FluxPropose, ouvrir_pas
from nations.observation.observateur import FinDePas
from nations.scenarios import initial as initial_du_scenario

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


class ReleveParPhase(Releve):
    """`Releve`, plus, par pas, les montants exécutés de chaque clôture dans l'ordre des phases
    (critère 12 : postes après chaque phase)."""

    def __init__(self):
        super().__init__()
        self.clotures = []
        self._clotures_du_pas = []

    def relever(self, e):
        if type(e) is ClotureDePhase:
            self._clotures_du_pas.append((e.phase, e.montants))
        elif type(e) is FinDePas:
            self.clotures.append(self._clotures_du_pas)
            self._clotures_du_pas = []
        super().relever(e)


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
             varsigma_B=None, varsigma_L=None, observateur=None):
    """`nb_pas` pas du socle complet ; `varsigma_B` : t → ς_{B,t} (placement raté), `varsigma_L` :
    t → ς_{L,t} (refus de crédit, C31), t pas d'ouverture, nuls sinon."""
    o = assembler(socle, sentier, bloc_9, parametres)
    etat = socle.etat_initial(sentier) if initial is None else initial
    releve = Releve() if observateur is None else observateur
    for _ in range(nb_pas):
        part = 0.0 if varsigma_B is None else varsigma_B(etat.t)
        refus = 0.0 if varsigma_L is None else varsigma_L(etat.t)
        etat = ordo.executer_pas(etat, socle.entrees_du_tour(varsigma_L=refus, varsigma_B=part),
                                 o, releve)
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
    nulles = {cle for cle in series if socle.est_nulle(cle, tables, sentier, initial)}
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


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_conditions_jointes_tenues_a_chaque_cloture(banc, pi):
    """#122 ; ADR 0015, point 12.3 (S6) : `etat_de_cloture` n'évalue pas les conditions jointes,
    qui doivent tenir par la forme de N8. Sur 720 pas sans choc, `defaut_des_conditions_jointes`
    est sans défaut sur l'état initial et sur chaque état de clôture ; l'état du pas 720 est
    sauvegardé puis rechargé (contrôle complet de la reprise), égal à lui-même."""
    _, initial, releve = banc[pi]
    assert len(releve.pas) == NB_PAS
    for etat in (initial, *(p["etat"] for p in releve.pas)):
        champs = {nom: getattr(etat, nom) for nom in schema.CHAMPS}
        assert schema.defaut_des_conditions_jointes(champs) is None, etat.t
    final = releve.pas[-1]["etat"]
    assert final.t == NB_PAS
    assert charger(sauvegarder([final])) == (final,)


def _contre_exemples(socle, tables, initial):
    """Clé de `GRANDEURS_NULLES_DU_SOCLE_COMPLET` → [(tables, ouverture)] où une seule des
    conditions de son libellé tombe : tables du bloc 9 ou du bloc 8 variées, ou ouverture
    exécutée déplacée d'une position ou d'une variable d'état."""
    def bloc_9(**valeurs):
        return dataclasses.replace(tables, finances_publiques=varier(tables.finances_publiques,
                                                                    **valeurs))

    def bloc_8(**valeurs):
        return dataclasses.replace(tables, banque_centrale=varier(tables.banque_centrale,
                                                                  **valeurs))

    def ouverture(**valeurs):
        return dataclasses.replace(initial, **valeurs)
    impose, transferts, theta_CB = bloc_9(tau_F=0.01), bloc_9(theta_Tr=0.01), bloc_8(theta_CB=0.5)
    e_cb = {cat.VALEUR_NETTE_FLUX["banque_centrale"]: 1.0}
    return {
        "T_F (E5)": [(impose, initial)],
        "T^e_F": [(impose, initial), (tables, ouverture(T_F_m1=1.0))],
        "Tr (E6)": [(transferts, initial)],
        "ligne 6": [(transferts, initial)],
        "transferts non versés (E13)": [(transferts, initial)],
        "B_H": [(tables, ouverture(B_H=1.0))],
        "ligne 11a": [(tables, ouverture(B_H=1.0))],
        "ΔB^prim_CB (19a-BC)": [(theta_CB, initial)],
        "B_CB": [(theta_CB, initial), (tables, ouverture(B_CB=1.0))],
        "ligne 11c": [(theta_CB, initial), (tables, ouverture(B_CB=1.0))],
        "E^CB (V^flux)": [(tables, ouverture(**e_cb)), (tables, ouverture(Res=1.0)),
                          (tables, ouverture(L_CB=-1.0)), (tables, ouverture(B_CB=-1.0))],
        "perte non couverte (E13)": [(tables, ouverture(Res=1.0)), (tables, ouverture(L_CB=-1.0)),
                                     (tables, ouverture(B_CB=-1.0))],
        "T^cou (E4)": [(tables, ouverture(r_hat_etoile=initial.r_hat_etoile + 0.01))],
    }


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_nullites_du_socle_complet_calculees_sur_l_ouverture_executee(socle, pi):
    """Réserve de la revue finale de J3-d2 (prédicats partiels, M4) : chaque nullité de
    `GRANDEURS_NULLES_DU_SOCLE_COMPLET` est vraie sur les tables et l'état initial du banc, et
    fausse dès qu'une seule condition de son libellé tombe (`_contre_exemples`) : le classement
    lit l'état d'ouverture exécuté, ce n'est pas une déclaration. La ligne 19a-ménages, règle E10
    (M27), n'a pas de contre-exemple sur les tables ni sur l'ouverture : son prédicat évalue la
    fonction du bloc. Sans ouverture, le classement est refusé."""
    sentier = socle.sentier(pi)
    tables = socle.parametres_du_sentier(sentier)
    initial = socle.etat_initial(sentier)
    nulles = socle.GRANDEURS_NULLES_DU_SOCLE_COMPLET
    assert all(socle.est_nulle(c, tables, sentier, initial) for c in nulles)
    contre = _contre_exemples(socle, tables, initial)
    assert set(contre) == set(nulles) - {"ligne 19a-ménages"}
    for cle, cas in contre.items():
        for t, o in cas:
            assert not socle.est_nulle(cle, t, sentier, o), cle
    with pytest.raises(TypeError):
        socle.est_nulle("B_H", tables, sentier)


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


def test_un_seul_calcul_des_interets_sur_titres_par_pas(socle, monkeypatch):
    """Critère de #150, point 1 (ADR 0013, annotation du 16/11/2026, point 4) : la fonction
    balisée E7 (`interets_sur_titres`) est appelée une fois par pas sur le moteur, en phase 2 ;
    les lignes 11a à 11c proposées en phase 6 sont, au bit, les trois termes écrits en phase 2
    (`iB_BH`, `iB_BBk`, `iB_BCB`), sur les encours d'ouverture, et leur somme forme le plafond
    de E6 ; scénario du banc BF (sentier θ_CB = 0,5, ligne 11c non nulle ; placement raté
    ς_B = 0,5 au pas 5 ; transferts ouverts au seul pas 6, plafond de E6 liant)."""
    appels = []
    original = bloc_9.interets_sur_titres

    def compter(*args):
        appels.append(args)
        return original(*args)
    monkeypatch.setattr(bloc_9, "interets_sur_titres", compter)
    sentier = socle.sentier(0.02, theta_CB=0.5)
    initial = socle.etat_initial(sentier)
    _, releve = derouler(
        socle, sentier, 24, initial=initial, varsigma_B=lambda t: 0.5 if t == 5 else 0.0,
        bloc_9=bloc_9_compose(levier_au_tour(6, theta_Tr=TRANSFERTS_APRES_LE_PLACEMENT)))
    assert len(appels) == 24
    assert any(p["variables"]["Tr"] < p["variables"]["Tr_lev"] for p in releve.pas)
    ouvertures = (initial,) + tuple(p["etat"] for p in releve.pas[:-1])
    for p, o, (i_pas, *encours) in zip(releve.pas, ouvertures, appels, strict=True):
        v = p["variables"]
        assert i_pas == par_pas(TauxDeFlux(v["i_CB"])) and encours == [o.B_H, o.B_Bk, o.B_CB]
        assert (p["11a"], p["11b"], p["11c"]) == (v["iB_BH"], v["iB_BBk"], v["iB_BCB"])
        assert v["iB_BCB"] > 0.0 and v["iB_BBk"] > 0.0
        assert v["Tr"] == bloc_9.transferts(v["Tr_lev"], o.M_G, v["T_H"],
                                            v["iB_BH"] + v["iB_BBk"] + v["iB_BCB"], v["G_plan"])


def test_domaine_d_une_variable_d_etat_de_bloc_controle_une_fois_par_pas(socle, monkeypatch):
    """Critère de #144, point 1 (ADR 0013, annotation du 16/11/2026, point 1) : sur le socle
    complet, `defaut_de_domaine` est appelée une fois par pas pour chaque variable d'état d'un
    bloc (à l'écriture, par `Vue.ecrire_etat`), et une fois par pas pour chaque autre champ
    (à la clôture, par `etat_de_cloture`) ; trajectoire inchangée au bit."""
    nb_pas = 4
    # Le moteur seul : la fabrique de `FinDePas` du `conftest` (contrôle complet propre aux
    # tests) est retirée, sans quoi chaque champ serait compté une fois de plus par pas.
    monkeypatch.setattr(ordo, "FinDePas", FinDePas)
    sentier = socle.sentier(0.02)
    initial = socle.etat_initial(sentier)
    # Tables alignées hors du compte : `parametres_du_sentier` résout θ_G par
    # `scenarios.etat_initial`, qui construit un `EtatPays` (contrôle de construction, hors pas).
    tables = socle.parametres_du_sentier(sentier)
    temoin, _ = derouler(socle, sentier, nb_pas, initial=initial, parametres=tables)
    appels = []
    original = schema.defaut_de_domaine

    def compter(nom, valeur):
        appels.append(nom)
        return original(nom, valeur)
    monkeypatch.setattr(schema, "defaut_de_domaine", compter)
    final, _ = derouler(socle, sentier, nb_pas, initial=initial, parametres=tables)
    assert final == temoin
    blocs = {v.nom for v in schema.VARIABLES_DES_BLOCS}
    assert len(blocs) == 20
    compte = {nom: appels.count(nom) for nom in schema.CHAMPS}
    assert compte == {nom: nb_pas for nom in schema.CHAMPS}
    assert len(appels) == nb_pas * len(schema.CHAMPS)


# --------------------------------------------------------------------------
# Domaine de représentabilité de μ̃ et refus de division (#158 ; ADR 0016, points 10, 11, 18.1)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("mu_tilde", [700.0, -709.0, prix.BORNE_MU_TILDE,
                                      -prix.BORNE_MU_TILDE])
def test_mu_tilde_extreme_dans_le_domaine_resultat_fini_ou_arret_type(socle, mu_tilde):
    """Critère 3 de `macro` (#158), écrit avant l'essai : avec μ̃_{−1} dans le domaine, aux
    valeurs de l'issue (700, −709) et aux bornes ±ln(DBL_MAX), chargé par `dataclasses.replace`
    de l'état résolu, le pas 0 du socle complet (π* = 2 %) rend un état fini (contrôlé par le
    constructeur), ou s'arrête par un arrêt typé, `ArretMoteur` ou `ArretNoyau` ; jamais une
    exception brute (critère « aucune exception brute ne sort du moteur », point 11)."""
    sentier = socle.sentier(0.02)
    initial = dataclasses.replace(socle.etat_initial(sentier), mu_tilde=mu_tilde)
    try:
        suivant, _ = derouler(socle, sentier, 1, initial=initial)
    except (ArretMoteur, ArretNoyau):
        return
    assert all(math.isfinite(getattr(suivant, v.nom)) for v in schema.VARIABLES
               if v.type is float)


def test_sigma_infime_arret_par_le_domaine_de_mu_tilde_en_phase_5(socle):
    """Critère 4 de `macro` (#158), écrit avant l'essai : avec σ = 1e−12 (table de production),
    depuis l'état résolu à ces tables, socle complet, π* = 2 %, la trajectoire s'arrête par le
    refus du domaine de μ̃ à l'écriture en phase 5 (`Vue.ecrire_etat`) : `RefusDuMoteur` qui
    nomme le bloc prix, l'étape « 5 » et « mu_tilde », et non par une division par zéro du bloc
    production (la `ZeroDivisionError` brute d'avant #158, p_t = UC_t e^{μ̃_t} = 0 en
    arithmétique flottante)."""
    sentier = socle.sentier(0.02)
    tables = socle.parametres_du_sentier(sentier)
    tables = dataclasses.replace(tables, production=varier(tables.production, sigma=1e-12))
    resolu = initial_du_scenario.etat_initial(tables, socle.normalisation_du_sentier(sentier),
                                              identifiant="A", graine=socle.GRAINE)
    with pytest.raises(RefusDuMoteur) as refus:
        derouler(socle, sentier, 12, initial=resolu.etat, parametres=resolu.parametres)
    assert type(refus.value) is RefusDuMoteur
    assert (refus.value.etape, refus.value.bloc, refus.value.nom) == ("5", "prix", "mu_tilde")
    assert isinstance(refus.value.t, int) and 0 <= refus.value.t < 12  # pas dans l'horizon déroulé
    assert "|μ̃| ≤ ln(DBL_MAX)" in str(refus.value)


def test_mu_tilde_au_dela_du_domaine_refuse_avec_son_nom_avant_le_prix(socle):
    """Constat m2 de l'audit de #158, décision du mainteneur du 27/11/2026 (μ̃ écrit avant le
    prix) : avec ψ_ξ = 1e6 et IN^vol_{−1} réduit de moitié dans l'état résolu à ces tables
    (ξ_0 = 0,5, μ̃_0 ≈ 5e4 > ln(DBL_MAX)), socle complet, π* = 2 %, le pas 0 s'arrête par le
    refus du domaine de μ̃ à son écriture (`Vue.ecrire_etat`) : `RefusDuMoteur` exact qui nomme
    l'étape « 5 », le bloc prix et « mu_tilde », et non par le `DepassementNumerique` anonyme
    de exp(μ̃_0) (P3), que rendait l'ordre d'écriture précédent."""
    sentier = socle.sentier(0.02)
    tables = socle.parametres_du_sentier(sentier)
    tables = dataclasses.replace(tables, prix=varier(tables.prix, psi_xi=1e6))
    resolu = initial_du_scenario.etat_initial(tables, socle.normalisation_du_sentier(sentier),
                                              identifiant="A", graine=socle.GRAINE)
    initial = dataclasses.replace(resolu.etat, IN_vol=0.5 * resolu.etat.IN_vol)
    with pytest.raises(RefusDuMoteur) as refus:
        derouler(socle, sentier, 1, initial=initial, parametres=resolu.parametres)
    assert type(refus.value) is RefusDuMoteur
    assert (refus.value.t, refus.value.etape, refus.value.bloc, refus.value.nom) == (
        0, "5", "prix", "mu_tilde")
    assert "|μ̃| ≤ ln(DBL_MAX)" in str(refus.value)


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


# Cliquet de l'encaisse égale à un pas de paiements (#171, n°1 ; P274) : `sec:ecartees`,
# « Encaisse égale à un pas de paiements (ν_G = 1) », « une baisse temporaire de 5 % reste
# rationnée 79 tours après son retour », mesuré à la calibration indicative sur la maquette de la
# fiche 9 (« G −5 % pendant 12 tours, puis retour », m = 1, π̄ = 0 : tours 13 à 90).
NU_G_UNITAIRE = 1.0
NB_PAS_DU_CLIQUET = 120


class _TableAEncaisseVisee:
    """Table du bloc 9 dont ν_G est remplacé, tout le reste étant lu sur la table réelle : la
    table refuse ν_G ≤ 1 (domaine déclaré, une décision citant M33), d'où cette vue d'essai."""

    __slots__ = ("_table", "nu_G")

    def __init__(self, table, nu_G):
        self._table = table
        self.nu_G = nu_G

    def __getattr__(self, nom):
        return getattr(self._table, nom)


class _ParametresAEncaisseVisee:
    """Ensemble des paramètres dont la table du bloc 9 est `_TableAEncaisseVisee`."""

    __slots__ = ("_parametres", "finances_publiques")

    def __init__(self, parametres, table, nu_G):
        self._parametres = parametres
        self.finances_publiques = _TableAEncaisseVisee(table, nu_G)

    def __getattr__(self, nom):
        return getattr(self._parametres, nom)


def bloc_9_a_encaisse_visee(nu_G, modifier):
    """Bloc 9 dérivé dans `tests/` (P274) : `bloc_9_compose(modifier)`, dont la phase 7, seule
    lectrice de ν_G au moteur (E8, `encaisse_visee`), lit ν_G = `nu_G` sur la table modifiée ;
    sous-classe sans attribut d'instance, même déclaration, aucun drapeau dans `src/`."""
    compose = type(bloc_9_compose(modifier))

    def phase_7(self, vue):
        p = vue.parametres
        table = modifier(vue.ouverture.t, p.finances_publiques)
        FinancesPubliques.phase_7(
            self, _VueAvecParametres(vue, _ParametresAEncaisseVisee(p, table, nu_G)))
    return type("FinancesPubliquesAEncaisseVisee", (compose,),
                {"__slots__": (), "phase_7": phase_7})()


def _nu_G_effectif(p):
    """ν_G lu par E8 au pas relevé `p` : M^G* rapportée aux paiements bruts exécutés du pas
    (lignes 2, 6, 11a à 11c)."""
    paiements = sum(p[ligne] for ligne in ("2", "6", "11a", "11b", "11c"))
    return p["variables"]["M_G_etoile"] / paiements


def test_cliquet_de_l_encaisse_egale_a_un_pas_de_paiements(socle, publier):
    """#171, n°1 (P274), banc écrit avant l'essai : socle complet, π̄ = 0, encaisse visée à
    ν_G = 1 par le bloc 9 dérivé (`bloc_9_a_encaisse_visee`), état initial résolu à ν_G = 1,15
    (la table refuse ν_G ≤ 1), G visée × 0,95 aux tours 1 à 12 (pas 0 à 11) puis retour,
    120 pas ; pas où le plafond de E1 est actif (G^plan < G^visée). Propriétés : témoin sans
    choc au même ν_G jamais plafonné ; sous le choc, plafond inactif pendant la baisse, actif
    au retour (pas 12, tour 13), sur des pas contigus, jamais réactivé une fois levé. Publiés :
    nombre de pas actifs, premier et dernier pas et tours, levée dans la fenêtre ou censure."""
    sentier = socle.sentier(0.0)
    _, temoin = derouler(socle, sentier, NB_PAS_DU_CLIQUET,
                         bloc_9=bloc_9_a_encaisse_visee(NU_G_UNITAIRE, lambda t, table: table))
    assert len(temoin.pas) == NB_PAS_DU_CLIQUET
    assert not any(_actif(p) for p in temoin.pas)
    assert all(abs(_nu_G_effectif(p) - NU_G_UNITAIRE) <= SEUIL_FLUX for p in temoin.pas)
    _, r = derouler(socle, sentier, NB_PAS_DU_CLIQUET,
                    bloc_9=bloc_9_a_encaisse_visee(NU_G_UNITAIRE, choc_de_theta_G(0.95)))
    assert len(r.pas) == NB_PAS_DU_CLIQUET
    assert all(abs(_nu_G_effectif(p) - NU_G_UNITAIRE) <= SEUIL_FLUX for p in r.pas)
    actifs = [p["t"] for p in r.pas if _actif(p)]
    assert actifs and actifs[0] == TOURS_DU_CHOC
    assert actifs == list(range(actifs[0], actifs[-1] + 1))
    leve = actifs[-1] + 1
    servi = min(r.pas[t]["variables"]["G_plan"] / r.pas[t]["variables"]["G_vise"]
                for t in actifs)
    def marge_du_temoin(t):
        """1 − G^visée/M^G d'ouverture du pas t (état de fin du pas t − 1)."""
        return 1.0 - temoin.pas[t]["variables"]["G_vise"] / temoin.pas[t - 1]["etat"].M_G
    marge = marge_du_temoin(NB_PAS_DU_CLIQUET - 1)
    marge_avant_retour = marge_du_temoin(TOURS_DU_CHOC - 1)
    # Réserve R1 du visa de `macro` : le régime ν_G = 1 du témoin est atteint avant le retour
    # (marge stationnaire du pas 11 au pas 119, celle du script à ν_G = 1).
    assert math.isclose(marge_avant_retour, marge, rel_tol=1e-9)
    publier("Cliquet de l'encaisse égale à un pas de paiements (ν_G = 1, bloc 9 dérivé, P274), "
            f"π̄ = 0, G visée × 0,95 aux tours 1 à 12, {NB_PAS_DU_CLIQUET} pas ({ETIQUETTE} pour "
            "l'état initial résolu et les tables ; E8 à ν_G = 1)", [
                (f"témoin sans choc : plafond de E1 jamais actif ; marge 1 − G^visée/M^G "
                 f"d'ouverture au pas {TOURS_DU_CHOC - 1} = {marge_avant_retour:.6f}, au pas "
                 f"{NB_PAS_DU_CLIQUET - 1} = {marge:.6f}"),
                f"plafond de E1 actif aux pas {actifs[0]} à {actifs[-1]} (tours "
                f"{calendrier.tour_du_pas(actifs[0])} à {calendrier.tour_du_pas(actifs[-1])}) : "
                f"{len(actifs)} pas après le retour ; min G^plan/G^visée = {servi:.6f} ; "
                + (f"levé au pas {leve}, jamais réactivé" if leve < NB_PAS_DU_CLIQUET
                   else f"encore actif au pas {NB_PAS_DU_CLIQUET - 1} (fenêtre censurée)")])


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
    entrees = dict(D_F=o.D_F, Delta_L=pb["18"], C=pb["1"], G=pb["2"], WB=pb["5"],
                   interets_L=par_pas(TauxDeFlux(o.i_L)) * o.L,
                   i_D_pas=par_pas(TauxDeFlux(o.i_D)), T_e_F=v["T_e_F"],
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


def test_perte_non_couverte_par_appel_direct(publier):
    """P157, cas (ii), par appel direct sur le grand livre : perte de la banque centrale égale à
    deux fois l'encaisse (C60, Π^CB = −20, M^{G,8a} = 10), combinée à un placement raté total
    (lignes 19a nulles), montant couvert déclaré par E13 sur max(0 ; M^{G,8a}) : le noyau exécute
    −mc ; ΔE^CB_t = −(perte non couverte)_t à 1e−12 S^CB, par les flux (V^flux) et par le stock.
    Sous-points du critère 12 (décision du mainteneur du 15/11/2026), postes publiés après chaque
    phase : intérêts sur titres de la banque (ligne 11b, 1 u.m. sur B_Bk = 100, M^G d'ouverture
    11) payés en entier en phase 6 avant la ligne 16, réduite en 8 (b) (ordre de priorité) ;
    ΔB = Σ lignes 19a (aucun intérêt capitalisé) ; D_H, D_F, M^G ≥ 0 à la clôture de chaque phase
    (aucun découvert implicite), M^G nul exactement après 8 (b)."""
    ouverture = {"D_H": 100.0, "D_F": 50.0, "L": 100.0, "B_H": 0.0, "B_Bk": 100.0, "B_CB": 0.0,
                 "Res": 2000.0, "L_CB": 0.0, "M_G": 11.0, "K": 50.0, "IN": 10.0}
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
    i_pas = par_pas(TauxDeFlux(0.12))
    Pi_CB = -i_pas * ouverture["Res"]  # −20 : i_CB > 0, Res ≫ L^CB + B_CB
    perte = 0.0 - Pi_CB
    interets_Bk = i_pas * ouverture["B_Bk"]  # 1 : M^{G,8a} = 11 − 1 = 10 = perte/2
    postes = []
    for phase in cat.PHASES:
        for ligne in cat.LIGNES_DE_LA_PHASE[phase]:
            if ligne.proposant is None:
                continue
            termes = {t.nom: 0.0 for t in ligne.termes}
            if ligne.identifiant == "11b":
                termes["iB_BBk"] = interets_Bk
            if ligne.identifiant == "12":
                termes["ires_Res"] = perte
            if ligne.identifiant == "16":
                termes["Pi_CB"] = Pi_CB
            gl.proposer(FluxPropose(ligne.identifiant, termes, ligne.proposant))
        if phase == "8b":
            mc, non_couverte = bloc_9.part_non_payee(perte, gl.position("M_G"))
            gl.declarer_montant_couvert("16", mc, "finances_publiques")
        gl.clore_phase(phase)
        postes.append((phase, {q: gl.position(q) for q in ("D_H", "D_F", "M_G", "B_H", "B_Bk",
                                                           "B_CB")}))
    assert (mc, non_couverte) == (10.0, 10.0)
    s_cb = gl.echelle("banque_centrale")
    v_flux = gl.valeur_nette_flux("banque_centrale")
    assert abs((v_flux - v["V_flux_banque_centrale"]) + non_couverte) <= SEUIL_FLUX * s_cb
    assert abs(gl.valeur_nette_stock("banque_centrale") - v_flux) <= SEUIL_FLUX * s_cb
    assert gl.montant_execute_ligne("16") == -mc
    # Critère 12 : ordre de priorité, intérêt non capitalisé, aucun découvert.
    assert cat.LIGNE["11b"].phase == "6" and cat.LIGNE["16"].phase == "8b"
    assert gl.montant_execute_ligne("11b") == interets_Bk
    for poste, ligne in EMISSIONS.items():
        assert postes[-1][1][poste] - ouverture[poste] == gl.montant_execute_ligne(ligne) == 0.0
    assert all(x[q] >= 0.0 for _, x in postes for q in PAYEURS_NON_BANCAIRES)
    assert dict(postes)["6"]["M_G"] == ouverture["M_G"] - interets_Bk
    assert dict(postes)["8b"]["M_G"] == 0.0
    publier("Perte de la banque centrale égale à deux fois l'encaisse, placement raté total "
            "(appel direct sur le grand livre ; critère 12, postes après chaque phase)", [
                " ; ".join(f"{phase} : M^G {x['M_G']:g}, D_H {x['D_H']:g}, D_F {x['D_F']:g}, "
                           f"B {x['B_H'] + x['B_Bk'] + x['B_CB']:g}" for phase, x in postes),
                f"ligne 11b payée {gl.montant_execute_ligne('11b'):g} (proposée {interets_Bk:g}) ; "
                f"ligne 16 exécutée {gl.montant_execute_ligne('16'):g} (proposée {Pi_CB:g}) ; "
                f"perte non couverte {non_couverte:g}"])


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


# Critère 12 (`sec:finances_publiques-conditions`, « Parts non payées » ; fiche 9, § 9.6) :
# payeurs non bancaires et leur secteur, lecture nette du contrôle de caisse (ε S du payeur à
# l'ouverture, `eq:noyau-caisse-nette`) ; la banque paie en réserves, dont le découvert intra-pas
# est couvert en 8 (c) (Res_{t+1} ≥ 0 strict en phase 9, `eq:noyau-reserves-cloture`).
PAYEURS_NON_BANCAIRES = {"D_H": "menages", "D_F": "entreprises", "M_G": "etat"}
# Lignes 19a et poste de titres qu'elles font varier (19b sans proposant au socle).
EMISSIONS = {"B_H": "19a-ménages", "B_Bk": "19a-banque", "B_CB": "19a-BC"}


def postes_apres_chaque_phase(ouverture, clotures):
    """Postes à la clôture de chaque phase d'un pas : [(phase, positions)], reconstruits depuis
    les positions d'ouverture et les montants exécutés de chaque clôture par les variations et
    les règlements des termes du catalogue (les contreparties 17, 20 et 22 ne font que relever
    les règlements, déjà appliqués)."""
    positions = _positions(ouverture)
    rendus = []
    for phase, montants in clotures:
        for ligne, termes in montants:
            if cat.LIGNE[ligne].contrepartie:
                continue
            x = dict(termes)
            for terme in cat.LIGNE[ligne].termes:
                for poste, c in terme.variations + terme.reglement:
                    positions[poste] += c * x[terme.nom]
        rendus.append((phase, dict(positions)))
    return rendus


def controler_le_critere_12(initial, releve):
    """Critère 12 sur une trajectoire du moteur relevée par `ReleveParPhase` ; rend les mesures
    publiées : marge minimale de chaque payeur non bancaire, à son échelle, sur toutes les phases.
    - **postes après chaque phase** : reconstruits (`postes_apres_chaque_phase`), ceux de la
      phase 9 égaux au bit à l'état t + 1 ;
    - **aucun découvert implicite** : D_H, D_F, M^G ≥ −ε S du payeur à la clôture de chaque phase,
      Res ≥ 0 à la clôture de la phase 9 ;
    - **aucun intérêt capitalisé** : ΔB_H, ΔB_Bk, ΔB_CB du pas égaux aux lignes 19a-ménages,
      19a-banque, 19a-BC à 1e−12 S^G, lignes 11a à 11c égales au bit à E7 sur l'ouverture
      (i_CB/n_a fois l'encours, versés, non ajoutés au principal) ;
    - **ordre de priorité exact** (`sec:finances_publiques-caisse`) : dépense plafonnée par le seul
      compte d'ouverture, G^plan = min(max(0 ; M^G) ; G^vise) ; intérêts versés en entier ;
      transferts sur le reste, Tr = min(Tr^lev ; max(0 ; M^G + T_H − i_CB B/n_a − G^plan)),
      ligne 6 = Tr, part non versée Tr^lev − Tr ; ligne 16 en dernier, −min(|Π^CB| ;
      max(0 ; M^{G,8a})) si Π^CB < 0, Π^CB sinon ; ces formes sont recalculées ici, au bit,
      sans appeler les fonctions du bloc."""
    assert [cat.LIGNE[ligne].phase for ligne in ("2", "11a", "11b", "11c", "6", "16")] == [
        "5", "6", "6", "6", "6", "8b"]
    ouvertures = [initial] + [p["etat"] for p in releve.pas[:-1]]
    marges = dict.fromkeys(PAYEURS_NON_BANCAIRES, math.inf)
    for o, p, clotures in zip(ouvertures, releve.pas, releve.clotures, strict=True):
        v, f = p["variables"], p["etat"]
        echelles = {s: idt.echelle_bilan(_positions(o), s) for s in cat.SECTEURS}
        postes = postes_apres_chaque_phase(o, clotures)
        assert [phase for phase, _ in postes] == list(cat.PHASES)
        assert postes[-1][1] == _positions(f), p["t"]
        for _, x in postes:
            for moyen, payeur in PAYEURS_NON_BANCAIRES.items():
                marges[moyen] = min(marges[moyen], x[moyen] / echelles[payeur])
                assert x[moyen] >= -EPS * echelles[payeur], (p["t"], moyen)
        assert f.Res >= 0.0
        for poste, ligne in EMISSIONS.items():
            assert abs((getattr(f, poste) - getattr(o, poste)) - p[ligne]) <= (
                SEUIL_FLUX * echelles["etat"]), (p["t"], poste)
        i_pas = par_pas(TauxDeFlux(v["i_CB"]))
        assert (p["11a"], p["11b"], p["11c"]) == (i_pas * o.B_H, i_pas * o.B_Bk, i_pas * o.B_CB)
        interets = p["11a"] + p["11b"] + p["11c"]
        assert v["G_plan"] == min(max(0.0, o.M_G), v["G_vise"])
        assert v["Tr"] == min(v["Tr_lev"], max(0.0, o.M_G + v["T_H"] - interets - v["G_plan"]))
        assert p["6"] == v["Tr"] and v["Tr_non_verses"] == v["Tr_lev"] - v["Tr"]
        M_G_8a = dict(postes)["8a"]["M_G"]
        if v["Pi_CB"] < 0.0:
            couvert = min(-v["Pi_CB"], max(0.0, M_G_8a))
            assert p["16"] == -couvert
            assert v["perte_non_couverte"] == -v["Pi_CB"] - couvert
        else:
            assert p["16"] == v["Pi_CB"] and v["perte_non_couverte"] == 0.0
    return marges


# θ_Tr au pas 6 : Tr^lev ≈ 2,3 G, au-delà du plafond de E6 (Tr/Tr^lev de 0,45 à 0,50 aux trois
# π*, mesure publiée par le test).
TRANSFERTS_APRES_LE_PLACEMENT = 0.5


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_placement_rate_de_moitie_sur_un_tour(socle, pi, publier):
    """P90, « Placement raté » ; critère 12, cas (i) : ς_B = 0,5 au pas 5 : M^G de clôture = M^G*
    − ς_B (Em − ΔB^prim_CB) à 1e−12 S^G ; Res L^CB = 0 exactement à la clôture (B7) ; aucun arrêt,
    aucune part non payée ; au pas suivant, plafond de E1 publié (actif ou non). Sous-points du
    critère 12 (décision du mainteneur du 15/11/2026), `controler_le_critere_12`, sur cette
    trajectoire et sur une seconde où les transferts sont ouverts au seul pas 6 (θ_Tr = 0,5,
    composition dans `tests/`) : Tr réduit sous Tr^lev au pas 6, intérêts 11a à 11c payés en
    entier, part non versée enregistrée (E13)."""
    sentier = socle.sentier(pi)
    initial = socle.etat_initial(sentier)

    def part(t):
        return 0.5 if t == 5 else 0.0
    _, r = derouler(socle, sentier, 24, varsigma_B=part, observateur=ReleveParPhase())
    p = r.pas[5]
    v, f = p["variables"], p["etat"]
    attendu = v["M_G_etoile"] - 0.5 * (v["Em"] - p["19a-BC"])
    s_g = idt.echelle_bilan(_positions(r.pas[4]["etat"]), "etat")
    assert abs(f.M_G - attendu) <= SEUIL_FLUX * s_g
    assert all(q["etat"].Res * q["etat"].L_CB == 0.0 for q in r.pas)
    assert all(q["variables"]["perte_non_couverte"] == 0.0
               and q["variables"]["Tr_non_verses"] == 0.0 for q in r.pas)
    marges = controler_le_critere_12(initial, r)
    _, rt = derouler(socle, sentier, 24, varsigma_B=part, observateur=ReleveParPhase(),
                     bloc_9=bloc_9_compose(levier_au_tour(
                         6, theta_Tr=TRANSFERTS_APRES_LE_PLACEMENT)))
    vt = rt.pas[6]["variables"]
    assert vt["Tr"] < vt["Tr_lev"] and vt["Tr_non_verses"] > 0.0
    assert all(q["variables"]["Tr"] == q["variables"]["Tr_lev"] for q in rt.pas if q["t"] != 6)
    marges_tr = controler_le_critere_12(initial, rt)
    actifs = [q["t"] for q in r.pas if _actif(q)]
    publier(f"Placement raté de moitié au pas 5, π* = {100 * pi:g} % ({ETIQUETTE})", [
        f"M^G de clôture − (M^G* − ς_B (Em − ΔB^prim_CB)) = {f.M_G - attendu:.1e} u.m. "
        f"(S^G = {s_g:.3e}) ; M^G/M^G* = {f.M_G / v['M_G_etoile']:.6f}",
        "plafond de E1 actif aux pas : " + (str(actifs) if actifs else "aucun"),
        "critère 12, postes après chaque phase, marge minimale du payeur (position/S) : "
        + " ; ".join(f"{q} {x:.3e}" for q, x in marges.items()),
        f"avec θ_Tr = {TRANSFERTS_APRES_LE_PLACEMENT:g} au pas 6 : Tr/Tr^lev = "
        f"{vt['Tr'] / vt['Tr_lev']:.4f}, intérêts payés en entier ; marge minimale : "
        + " ; ".join(f"{q} {x:.3e}" for q, x in marges_tr.items())])


@pytest.mark.parametrize("nom, choc", [
    ("placement raté de moitié aux tours 1 à 12", "placement"),
    ("dépense doublée aux tours 1 à 12", "depense")])
def test_bornes_plafond_desactive_sous_douze_tours(socle, nom, choc, publier):
    """Critère 16 (bornes), π* = 2 % : sous un placement raté de moitié ou une dépense doublée aux
    tours 1 à 12, le plafond de E1 est désactivé au plus tard 12 tours après la fin du choc, sans
    réactivation : les pas où il est actif forment un intervalle d'entiers consécutifs qui
    commence au premier pas où le choc atteint E1, celui du choc pour la dépense (θ_G lu en
    phase 2 du tour même), le suivant pour le placement (ς_B agit en phase 7, M^G est lu en
    phase 2 du tour suivant) ; la dépense doublée active le plafond (au-delà de la marge de
    caisse, P158) ; aucun arrêt du noyau."""
    sentier = socle.sentier(0.02)
    if choc == "placement":
        _, r = derouler(socle, sentier, 120,
                        varsigma_B=lambda t: 0.5 if t < TOURS_DU_CHOC else 0.0)
        premier = 1
    else:
        _, r = derouler(socle, sentier, 120, bloc_9=bloc_9_compose(choc_de_theta_G(2.0)))
        premier = 0
        assert any(_actif(p) for p in r.pas)
    actifs = [p["t"] for p in r.pas if _actif(p)]
    fin = TOURS_DU_CHOC - 1 + DELAI_DE_DESACTIVATION
    assert all(t <= fin for t in actifs), actifs[-5:]
    assert not actifs or actifs == list(range(premier, actifs[-1] + 1)), actifs
    publier(f"Bornes, {nom}, π* = 2 % ({ETIQUETTE})", [
        "plafond de E1 actif aux pas : " + (f"{actifs[0]} à {actifs[-1]} ({len(actifs)} pas)"
                                             if actifs else "aucun")
        + f" ; limite écrite : pas {fin}"])


# Placement raté (ς_B = 1) aux pas 5 à 7, θ_Tr composé à tous les pas : #153, critère 1.
PAS_DU_PLACEMENT_RATE_153 = (5, 6, 7)
NB_PAS_153 = 36


@pytest.mark.parametrize("pi, theta_Tr", [(0.02, 0.3), (0.10, 0.2), (0.10, 0.3)])
def test_tresor_vide_sans_arret_echelle_de_repli(socle, pi, theta_Tr, monkeypatch, publier):
    """#153, critère 1 (avis de `monnaie`, § 1.4, écrit avant l'essai ; ADR 0016, I) : ς_B = 1
    aux pas 5 à 7 et θ_Tr composé à tous les pas (`bloc_9_compose`) vident le compte du Trésor
    (S^CB effondrée) ; 36 pas sans aucun `ArretNoyau` (l'appel lèverait). À π* = 10 %,
    θ_Tr = 0,3 (avant le repli : `DefautComptable` au pas 7, phase 6, ligne 20, S = 0) : le
    montant de la ligne 20 au pas 7, phase 6, est nul, et sa porte ΔH est contrôlée à
    min(S^Bk, S^CB) de l'ouverture du pas 7, > 0, avec |résidu| ≤ ε S. θ_Tr ≥ 0,35 exclu :
    arrêt de l'identité cumulée sous échelle effondrée, #195, hors périmètre. À l'ancienne
    règle (échelle nulle sans repli), seul le cas 10 %, θ_Tr = 0,3 s'arrête dans ce banc
    (mesuré par `audit`, mutant « repli absent ») : les deux autres cas sont un contrôle
    « sans arrêt », pas un témoin de régression ; l'arrêt au pas 8 que l'issue cite pour
    2 %, θ_Tr = 0,3 venait d'une configuration de J3-d2 non reproduite à cette tête."""
    controles = []
    origine = idt.verifier_identites

    def espion(regle, residus, echelles, objets, epsilon, *, t, phase):
        if (t, phase, regle.nom) == (7, "6", idt.VARIATION_MONNAIE_CENTRALE.nom):
            controles.extend((o[1], r, s) for r, s, o in zip(residus, echelles, objets,
                                                             strict=True))
        return origine(regle, residus, echelles, objets, epsilon, t=t, phase=phase)
    monkeypatch.setattr(idt, "verifier_identites", espion)
    sentier = socle.sentier(pi)
    etat, r = derouler(
        socle, sentier, NB_PAS_153, observateur=ReleveParPhase(),
        bloc_9=bloc_9_compose(lambda t, table: varier(table, theta_Tr=theta_Tr)),
        varsigma_B=lambda t: 1.0 if t in PAS_DU_PLACEMENT_RATE_153 else 0.0)
    assert etat.t == NB_PAS_153
    ouverture_7 = _positions(r.pas[6]["etat"])
    s_cb = idt.echelle_bilan(ouverture_7, "banque_centrale")
    attendue = min(idt.echelle_bilan(ouverture_7, "banque"), s_cb)
    (porte,) = [(residu, s) for ligne, residu, s in controles if ligne == "20"]
    montants = dict(next(m for ph, m in r.clotures[7] if ph == "6"))
    if (pi, theta_Tr) == (0.10, 0.3):
        assert all(x == 0.0 for _, x in montants["20"])
        assert porte[1] == attendue > 0.0
        assert abs(porte[0]) <= CADRE.tolerance_identite_pas * porte[1]
    publier(f"#153, Trésor vidé, π* = {100 * pi:g} %, θ_Tr = {theta_Tr:g} ({ETIQUETTE})", [
        f"{NB_PAS_153} pas sans arrêt ; pas 7, phase 6, ligne 20 : montant "
        f"{sum(x for _, x in montants['20']):.3e}, échelle {porte[1]:.3e} "
        f"(min(S^Bk, S^CB) = {attendue:.3e}, S^CB = {s_cb:.3e}), "
        f"|résidu|/S = {abs(porte[0]) / porte[1]:.2e}"])


# --------------------------------------------------------------------------
# Couverture sur le moteur (F6, F7)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_couverture_d_un_choc_de_taux_au_tour_n(socle, pi):
    """F6 : r̂* relevé de 0,01 dans l'état d'ouverture (i_CB du tour relevé de Δ), contre le
    contrôle : au tour n seul, Div_Bk (ligne 15) varie de Δ (B_Bk + Res − L^CB)/n_a, T^cou reprend
    Δ A/n_a, A = B − M^G − E^CB, et le revenu disponible des ménages ne varie pas (B_H = 0), à
    1e−12 relatif ; les autres revenus des ménages sont inchangés au bit. Critère de la décision
    du mainteneur du 04/10/2026 (`sec:finances_publiques-conditions`, « Couverture ») : assiette
    Y^HS écrite en phase 7 du tour 1 (E12) égale à celle du contrôle, et part au barème de
    l'impôt du tour 2, τ_H Γ^e_2 Y^HS_1 (E3), inchangée, à 1e−12 relatif, sur deux pas."""
    sentier = socle.sentier(pi)
    initial = socle.etat_initial(sentier)
    _, c = derouler(socle, sentier, 2)
    _, s = derouler(socle, sentier, 2,
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
    assert abs(ps["etat"].Y_HS_m1 / pc["etat"].Y_HS_m1 - 1.0) <= SEUIL_FLUX
    tau_H = socle.parametres_du_sentier(sentier).finances_publiques.tau_H
    bareme_c = tau_H * c.pas[1]["grandeurs"]["Gamma_e"] * c.pas[0]["etat"].Y_HS_m1
    bareme_s = tau_H * s.pas[1]["grandeurs"]["Gamma_e"] * s.pas[0]["etat"].Y_HS_m1
    assert abs(bareme_s / bareme_c - 1.0) <= SEUIL_FLUX
    # La part au barème est bien celle de l'impôt exécuté du tour 2 : T_H − T^cou (E3).
    for r, bareme in ((c, bareme_c), (s, bareme_s)):
        v2 = r.pas[1]["variables"]
        assert abs((v2["T_H"] - v2["T_cou"]) / bareme - 1.0) <= SEUIL_FLUX


# Hausse de taux d'un point pendant 12 tours sous φ ∈ {0 ; 1} (#171, n°6 ; fiche 9, Q2, table φ ;
# critère écrit avant l'essai par `monnaie`, décision P275). Configuration (A) du critère 15 de la
# fiche 8 : règle de taux en vigueur, taux décidé = prescription + 1 point aux tours 1 à 12,
# action intégrale jamais réinitialisée. Les colonnes φ ∈ {0,1 ; 0,25 ; 0,5} sont hors du domaine
# du levier (M33) et renvoyées à #111 : non mesurées.
HAUSSE_DE_TAUX = 0.01
PAS_DE_P36 = 35  # tour 36 = pas 35 (tour k = pas k − 1, `sec:cadre-calendrier`)


def _hausse_de_taux_d_un_point(socle, sentier, tables):
    """Contrôle et trajectoire choquée, mêmes tables, depuis `socle.etat_initial`, sur
    `PAS_DE_P36` + 1 pas ; injection par composition sur l'état d'ouverture : r̂* += Δ à
    l'ouverture du pas 0, retiré à l'ouverture du pas 12, Δ = 0,01/(1 + π*), d'où +0,01 exact
    sur (1 + r̂*)(1 + π*) dans BC1. BC2 étant additive en r̂*, la composante Δ se conserve sous
    l'action intégrale, qui n'est pas réinitialisée. Rend (relevé du contrôle, relevé du choc,
    Δ, arrêt du choc ou None)."""
    initial = socle.etat_initial(sentier)
    delta = HAUSSE_DE_TAUX / (1.0 + initial.pi_etoile)
    _, c = derouler(socle, sentier, PAS_DE_P36 + 1, parametres=tables)
    o = assembler(socle, sentier, parametres=tables)
    s = Releve()
    etat, arret = initial, None
    try:
        for t in range(PAS_DE_P36 + 1):
            if t in (0, TOURS_DU_CHOC):
                signe = 1.0 if t == 0 else -1.0
                etat = dataclasses.replace(etat, r_hat_etoile=etat.r_hat_etoile + signe * delta)
            etat = ordo.executer_pas(etat, socle.entrees_du_tour(), o, s)
    except (RefusDuMoteur, DefautComptable) as refus:
        arret = f"non mesurable (arrêt au pas {len(s.pas)} : {refus})"
    assert [p["t"] for p in s.pas] == list(range(len(s.pas)))
    return c, s, delta, arret


def _verifier_l_injection(c, s, initial, delta, a_pi):
    """Assertions du banc (critère de `monnaie`), à 1e−12 relatif : pas 0, i_CB choqué − contrôle
    = 0,01 ; pas 1 à 11, i_CB = BC1 sur l'ouverture choquée avec r̂* − Δ, + 0,01 ; pas 12,
    i_CB = BC1 sur l'ouverture (Δ retiré)."""
    d0 = s.pas[0]["variables"]["i_CB"] - c.pas[0]["variables"]["i_CB"]
    assert abs(d0 / HAUSSE_DE_TAUX - 1.0) <= SEUIL_NUL, d0
    ouvertures = [initial] + [p["etat"] for p in s.pas[:-1]]
    for t in range(1, TOURS_DU_CHOC + 1):
        o, i_cb = ouvertures[t], s.pas[t]["variables"]["i_CB"]
        # État de fin du pas t − 1 : il porte encore Δ aux pas 1 à 12 ; au pas 12, Δ est retiré
        # à l'ouverture exécutée, et la prescription est lue sans hausse.
        hausse = HAUSSE_DE_TAUX if t < TOURS_DU_CHOC else 0.0
        attendu = taux_indique_par_la_regle(o.r_hat_etoile - delta, o.pi_etoile,
                                            registre.glissement(o.registre_prix), a_pi) + hausse
        assert abs(i_cb / attendu - 1.0) <= SEUIL_NUL, (t, i_cb, attendu)


@pytest.mark.parametrize("pi", [0.02, 0.10])
def test_p36_d_une_hausse_de_taux_aux_deux_valeurs_de_phi(socle, pi, publier):
    """#171, n°6 (fiche 9, Q2, table φ, colonnes φ ∈ {0 ; 1} ; critère écrit avant l'essai par
    `monnaie`, décision P275) : P_36 = 100 (p^choc_36/p^contrôle_36 − 1), en %, p = indice des
    prix du tour (phase 5), au tour 36 (pas 35), contre le contrôle apparié (même état initial
    résolu, mêmes tables T1, sans choc), choc (A) du critère 15 de la fiche 8 injecté par
    `_hausse_de_taux_d_un_point`. Propriétés : (1) φ = 1 : P_36 < 0 ; (2) P_36(φ = 0) >
    P_36(φ = 1) ; (3) publiés sans verdict : P_36 aux deux φ, écart de r̂* (choqué − contrôle) à
    l'ouverture du pas 35. Un arrêt du moteur sous φ = 0 avant le pas 35 est publié « non
    mesurable », sans verdict sur (2). L'écart 10 % − 2 % se lit sur les deux publications."""
    sentier = socle.sentier(pi)
    initial = socle.etat_initial(sentier)
    a_pi = socle.parametres_du_sentier(sentier).banque_centrale.a_pi
    mesures, lignes = {}, []
    for phi, tables in ((1.0, socle.parametres_du_sentier(sentier)),
                        (0.0, _sous_phi_nul(socle, sentier))):
        assert tables.finances_publiques.phi == phi
        c, s, delta, arret = _hausse_de_taux_d_un_point(socle, sentier, tables)
        if arret is not None:
            assert phi == 0.0, arret  # sous φ = 1, un arrêt n'est pas une mesure admise
            mesures[phi] = None
            lignes.append(f"φ = {phi:g} : P_36 {arret}")
            continue
        _verifier_l_injection(c, s, initial, delta, a_pi)
        assert s.pas[PAS_DE_P36]["t"] == c.pas[PAS_DE_P36]["t"] == PAS_DE_P36
        p36 = 100.0 * (s.pas[PAS_DE_P36]["variables"]["p"]
                       / c.pas[PAS_DE_P36]["variables"]["p"] - 1.0)
        d_r_hat = s.pas[PAS_DE_P36 - 1]["etat"].r_hat_etoile - c.pas[PAS_DE_P36 - 1][
            "etat"].r_hat_etoile
        mesures[phi] = p36
        lignes.append(f"φ = {phi:g} : P_36 = {p36:+.3f} % ({p36:+.6e}) ; r̂* choqué − contrôle à "
                      f"l'ouverture du pas {PAS_DE_P36} = {d_r_hat:+.4e} par an")
    publier(f"P_36 d'une hausse de taux d'un point aux tours 1 à 12, π* = {100 * pi:g} % "
            f"({ETIQUETTE} ; table T1 ; #171, n°6)", lignes)
    assert mesures[1.0] < 0.0, mesures  # (1) : un échec est une condition d'arrêt, pas un xfail
    if mesures[0.0] is not None:
        assert mesures[0.0] > mesures[1.0], mesures  # (2)


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
    (Δi_CB signé par pas, choqué moins contrôle, sur les pas relevés de la trajectoire choquée,
    arrêt publié)."""
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
    # Rang k de la série = pas t = k de la trajectoire choquée (tour k + 1, `sec:cadre-calendrier`)
    # : les deux trajectoires partent de l'état initial, pas 0 (#171, n°4).
    assert [p["t"] for p in s.pas] == list(range(len(s.pas)))
    assert [p["t"] for p in c.pas] == list(range(len(c.pas)))
    return [b["variables"]["i_CB"] - a["variables"]["i_CB"]
            for a, b in zip(c.pas, s.pas)], arret


# Identification de la racine dominante sur la série Δi_CB du moteur (#166 ; critère des tests C62
# précisé avant l'essai, décision M34, feuille de route § 1) : prédiction linéaire (méthode de
# Prony), x_t = a_1 x_{t−1} + a_2 x_{t−2} ajusté par moindres carrés, racines de
# z² − a_1 z − a_2. Elle remplace le rapport de maxima sur des fenêtres, qui suppose une racine
# dominante réelle et mesure la phase d'une paire complexe lente, non son module
# (`docs/blocs/calibration.md` § 3.13.2). Fenêtre : seconde moitié des pas où |Δi_CB| n'a pas
# crû de plus de `CROISSANCE_LINEAIRE` fois son maximum des `PAS_D_AMPLITUDE` premiers pas (choc
# et suites immédiates), pour rester dans le régime linéaire et laisser s'éteindre les racines
# dominées. Ordre 2 et facteur 30, mesurés à ζ = 8 sur la série du choc de 1e−6, à l'état E1
# (`8df010b` : ϑ = 0,10, ν_H = 1, λ_w = 1) : à π* = 10 %, la racine identifiée vaut 1,0096618 au
# facteur 30 et reste à 3e−6 près jusqu'au facteur 200 (1,0096651, max |Δi_CB| de la fenêtre
# 9,4e−5) ; au facteur 300, l'harmonique de la non-linéarité (≈ λ²) l'emporte (1,0155), et 1,0203
# au facteur 1 000 : marge d'environ ×6,7 ; à π* = 2 %, la fenêtre n'atteint aucun de ces facteurs
# sur 2 700 pas (1,0000351 partout). Remesuré à la table T1 (rang 8 de la calibration, #166) : à
# π* = 10 %, 1,0082166 au facteur 30 (pas 270 à 540), 1,0082170 à 100, 1,0082175 à 200, 1,0082180
# à 300 (max |Δi_CB| de la fenêtre 6,5e−5), puis 1,01858 au facteur 1 000 (pas 484 à 968) : marge
# d'environ ×10 ; à π* = 2 %, aucun facteur atteint sur 2 700 pas (1,0008907 partout).
ORDRE_PRONY = 2
PAS_D_AMPLITUDE = 24
CROISSANCE_LINEAIRE = 30.0
PAS_MINIMAL_DE_LA_FENETRE = 60


class Identification(NamedTuple):
    """Résultat de `racine_dominante` : racine (None si aucune), fenêtre [debut ; fin[, résidu
    relatif de l'ajustement, motif du refus (None si une racine est identifiée)."""

    racine: complex | None
    debut: int | None
    fin: int | None
    residu: float | None
    motif: str | None


def _sans_racine(motif):
    return Identification(None, None, None, None, motif)


def racine_dominante(ecarts):
    """Racine dominante de la série signée `ecarts` (Prony, ordre 2, fenêtre ci-dessus), de plus
    grand module et d'argument ≥ 0. Aucune racine, avec son motif, si la série compte moins de
    `PAS_D_AMPLITUDE` pas, si l'amplitude de référence est nulle ou non finie, si la fenêtre
    compte moins de `PAS_MINIMAL_DE_LA_FENETRE` pas, si son maximum est nul ou non fini, ou si
    la cible de l'ajustement (fenêtre privée de ses `ORDRE_PRONY` premiers pas) est de norme
    nulle : le résidu relatif n'y est pas défini (#172)."""
    x = np.asarray(ecarts, dtype=float)
    if len(x) < PAS_D_AMPLITUDE:
        return _sans_racine(f"série de {len(x)} pas, moins de {PAS_D_AMPLITUDE}")
    reference = float(np.max(np.abs(x[:PAS_D_AMPLITUDE])))
    if not (math.isfinite(reference) and reference > 0.0):
        return _sans_racine(f"amplitude de référence des {PAS_D_AMPLITUDE} premiers pas nulle ou "
                            f"non finie ({reference!r})")
    au_dela = np.flatnonzero(~(np.abs(x) <= CROISSANCE_LINEAIRE * reference))
    fin = int(au_dela[0]) if au_dela.size else len(x)
    debut = fin // 2
    if fin - debut < PAS_MINIMAL_DE_LA_FENETRE:
        return _sans_racine(f"fenêtre de {fin - debut} pas (pas {debut} à {fin - 1}), moins de "
                            f"{PAS_MINIMAL_DE_LA_FENETRE}")
    echelle = float(np.max(np.abs(x[debut:fin])))
    if not (math.isfinite(echelle) and echelle > 0.0):
        return _sans_racine(f"maximum de la fenêtre nul ou non fini ({echelle!r})")
    serie = x[debut:fin] / echelle
    regresseurs = np.column_stack([serie[ORDRE_PRONY - j - 1:len(serie) - j - 1]
                                   for j in range(ORDRE_PRONY)])
    cible = serie[ORDRE_PRONY:]
    norme_cible = float(np.linalg.norm(cible))
    if not norme_cible > 0.0:
        return _sans_racine(f"cible de l'ajustement de norme nulle (pas {debut + ORDRE_PRONY} à "
                            f"{fin - 1})")
    a, *_ = np.linalg.lstsq(regresseurs, cible, rcond=None)
    residu = float(np.linalg.norm(cible - regresseurs @ a) / norme_cible)
    racine = complex(max(np.roots(np.concatenate([[1.0], -a])), key=abs))
    return Identification(complex(racine.real, abs(racine.imag)), debut, fin, residu, None)


def test_racine_dominante_sur_des_series_synthetiques():
    """`racine_dominante` (#166), sur des séries de racines connues :
    - une paire complexe lente de période plus longue que la fenêtre (1,0001 ∠ ±0,2°, avec une
      racine dominée de 0,99) et une racine réelle explosive (1,01, avec 0,998) sont retrouvées
      à 1e−8 sur le module et la partie imaginaire ;
    - λᵗ + ε λ²ᵗ + 0,998ᵗ (harmonique quadratique, λ = 1,01) : la fenêtre s'arrête quand |x| a
      crû de 30 fois ; à ε = 1e−6, l'harmonique y reste petite et λ est retrouvée à 1e−5 près
      (mesuré : 1,0100011) ; à ε = 1e−2, elle déplace la racine identifiée de plus de 5e−3 vers
      λ² (mesuré : 1,0178), limite de la méthode hors du régime linéaire ;
    - aucune racine, motif à l'appui, pour une série vide ou trop courte, une amplitude de
      référence nulle ou non finie, une fenêtre trop courte (croissance rapide, ou pas non fini
      qui l'arrête), un maximum de fenêtre nul, une cible de l'ajustement de norme nulle (fenêtre
      non nulle sur ses seuls `ORDRE_PRONY` premiers pas : résidu 0/0, NaN avant #172)."""
    t = np.arange(NB_PAS_LINEAIRE)
    paire = 1.0001 * np.exp(1j * math.radians(0.2))
    for serie, attendue in (((paire ** t).real + 0.5 * 0.99 ** t, paire),
                            (1e-6 * (1.01 ** t + 0.998 ** t), complex(1.01, 0.0))):
        r = racine_dominante(serie)
        assert r.motif is None
        assert abs(abs(r.racine) - abs(attendue)) <= 1e-8
        assert abs(r.racine.imag - attendue.imag) <= 1e-8
        assert 0 < r.debut < r.fin <= len(serie) and r.residu <= 1e-6
    lam = 1.01
    r = racine_dominante(lam ** t + 1e-6 * lam ** (2 * t) + 0.998 ** t)
    assert r.motif is None and abs(r.racine - lam) <= 1e-5, r
    r = racine_dominante(lam ** t + 1e-2 * lam ** (2 * t) + 0.998 ** t)
    assert r.motif is None and lam + 5e-3 < r.racine.real < lam ** 2, r
    nan_dans_la_fenetre = 1.01 ** t[:600]
    nan_dans_la_fenetre[100] = math.nan  # un pas non fini arrête la fenêtre
    for serie, motif in (([], "série de 0 pas"), (np.ones(10), "série de 10 pas"),
                         (np.zeros(600), "amplitude de référence"),
                         (np.r_[math.inf, np.ones(599)], "amplitude de référence"),
                         (1.1 ** t[:200], "fenêtre de"),
                         (nan_dans_la_fenetre, "fenêtre de")):
        r = racine_dominante(serie)
        assert r.racine is None and r.motif.startswith(motif), (motif, r)
    r = racine_dominante(np.r_[np.ones(PAS_D_AMPLITUDE), np.zeros(400)])
    assert r.racine is None and r.motif.startswith("maximum de la fenêtre"), r
    # 200 pas : fenêtre [100 ; 200[, non nulle aux seuls pas 100 et 101.
    cible_nulle = np.r_[np.ones(PAS_D_AMPLITUDE), np.zeros(100 - PAS_D_AMPLITUDE),
                        np.ones(ORDRE_PRONY), np.zeros(100 - ORDRE_PRONY)]
    r = racine_dominante(cible_nulle)
    assert r.racine is None and r.motif.startswith("cible de l'ajustement de norme nulle"), r


def _racine_publiee(z):
    """Module, argument (degrés, ±), période (tours) si complexe, temps de doublement si |z| > 1."""
    argument = math.degrees(math.atan2(z.imag, z.real))
    texte = f"|λ| = {abs(z):.7f}, arg = ±{argument:.4f}°"
    if z.imag != 0.0:
        texte += f" (période {360.0 / argument:.0f} tours)"
    if abs(z) > 1.0:
        return texte + f" ; temps de doublement = {math.log(2.0) / math.log(abs(z)):.0f} tours"
    return texte + " ; aucun doublement (|λ| ≤ 1)"


def _maquette_en_regard(maquette, pi):
    """Racine de la maquette conjointe (lecture (c), pire des deux régimes de T4, φ = 0)."""
    par = dataclasses.replace(maquette.parametres_socle(pi), phi=0.0)
    lue = max((maquette.lectures(par, regime).suivante for regime in ("hausse", "baisse")), key=abs)
    return ("maquette (lecture (c), pire des deux régimes de T4, φ = 0) : "
            + _racine_publiee(complex(lue.real, abs(lue.imag))))


@pytest.mark.parametrize("pi", [0.02, 0.10])
def test_temps_de_doublement_sous_phi_nul(socle, maquette, pi, publier):
    """C62 (F11), ligne (b), publié sans verdict : sous φ = 0 (« intérêts financés par le
    déficit »), choc G^plan +1 % aux tours 1 à 12 contre un contrôle apparié sous φ = 0, 720 pas.
    Le choc de 1 % sort du régime linéaire : aucune racine n'est identifiée sur le moteur
    (décision de la session, reprise du rang 4 de la calibration) ; sont publiés le maximum de
    |Δi_CB| sur les pas 240 à 359 et sur les 120 derniers pas relevés, la racine de la maquette
    pour mémoire et l'arrêt de la trajectoire choquée avec son pas, sans valeur attendue (critère
    précisé avant l'essai, M34, feuille de route § 1). La racine du moteur est publiée par
    `test_temps_de_doublement_en_regime_lineaire` (décision du mainteneur du 15/11/2026 : les
    deux mesures sont publiées)."""
    ecarts, arret = _ecarts_de_taux_sous_phi_nul(socle, socle.sentier(pi), 1.01, NB_PAS)
    fin = len(ecarts)
    maxima = (f"max |Δi_CB| pas 240 à 359 : {max(map(abs, ecarts[240:360])):.3e} ; "
              f"pas {fin - 120} à {fin - 1} : {max(map(abs, ecarts[fin - 120:fin])):.3e}"
              if fin >= 360 else f"{fin} pas relevés : aucun maximum publié")
    publier(f"C62 sous φ = 0, choc de 1 %, π* = {100 * pi:g} % ({ETIQUETTE} ; sans verdict)", [
        "choc de 1 % hors du régime linéaire : aucune racine identifiée sur le moteur ; la racine "
        "du moteur est publiée par `test_temps_de_doublement_en_regime_lineaire`",
        maxima, _premier_ecart_d_un_point(ecarts),
        f"{_maquette_en_regard(maquette, pi)} (pour mémoire)", arret])


# Écart d'un point du taux directeur à la trajectoire de contrôle (#171, n°4 ; `sec:finances_
# publiques-conditions`, C62, « s'écartant d'un point […] au pas 182 », publié à la calibration
# indicative) : |Δi_CB| ≥ 0,01 en fraction par an.
UN_POINT = 0.01


def _premier_ecart_d_un_point(ecarts):
    """Premier pas t où |Δi_CB| ≥ `UN_POINT`, avec son tour (t + 1) et sa date (année, mois),
    `sec:cadre-calendrier` ; ou son absence sur les pas relevés. Mesure, sans verdict."""
    assert ecarts and all(math.isfinite(x) for x in ecarts), "série Δi_CB vide ou non finie"
    t = next((k for k, x in enumerate(ecarts) if abs(x) >= UN_POINT), None)
    if t is None:
        return (f"|Δi_CB| < {UN_POINT:g} (un point) aux {len(ecarts)} pas relevés (max "
                f"{max(map(abs, ecarts)):.3e}) : aucun écart d'un point")
    annee, mois = calendrier.date(t)
    precedent = f"{abs(ecarts[t - 1]):.4e} au pas {t - 1}" if t else "aucun pas précédent"
    return (f"premier écart d'un point (|Δi_CB| ≥ {UN_POINT:g}) : pas t = {t}, tour "
            f"{calendrier.tour_du_pas(t)} (année {annee}, mois {mois}) ; |Δi_CB| = "
            f"{abs(ecarts[t]):.4e} (contre {precedent})")


# Mesure complémentaire de C62 en régime linéaire (décision du mainteneur du 15/11/2026).
FACTEUR_LINEAIRE = 1.0 + 1e-6
NB_PAS_LINEAIRE = 2700


@pytest.mark.parametrize("pi", [0.02, 0.10])
def test_temps_de_doublement_en_regime_lineaire(socle, maquette, pi, publier):
    """C62 (F11), mesure complémentaire en régime linéaire, publiée sans verdict : sous φ = 0,
    choc θ_G × (1 + 1e−6) aux tours 1 à 12 contre un contrôle apparié sous φ = 0, 2 700 pas ;
    racine dominante identifiée sur la série Δi_CB du moteur (`racine_dominante`, #166 : module,
    argument, temps de doublement si le module dépasse 1), ou motif de son absence ; racine de la
    maquette conjointe en regard ; arrêt publié avec son pas, sans valeur attendue (critère
    précisé avant l'essai, M34, feuille de route § 1)."""
    ecarts, arret = _ecarts_de_taux_sous_phi_nul(socle, socle.sentier(pi), FACTEUR_LINEAIRE,
                                                 NB_PAS_LINEAIRE)
    r = racine_dominante(ecarts)
    moteur = (f"moteur : aucune racine identifiée ({r.motif})" if r.racine is None else
              f"moteur (Prony, ordre {ORDRE_PRONY}, pas {r.debut} à {r.fin - 1}, résidu relatif "
              f"{r.residu:.1e}) : {_racine_publiee(r.racine)}")
    publier(f"C62 en régime linéaire, choc θ_G × (1 + 1e−6), φ = 0, π* = {100 * pi:g} % "
            f"({ETIQUETTE} ; sans verdict)", [moteur, _maquette_en_regard(maquette, pi), arret])


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


# --------------------------------------------------------------------------
# Fiche 6, « Endettement », dépôts, sous ϖ_L + 2 points (#139, critère de #169 ; P324, P330)
# --------------------------------------------------------------------------

VARPI_L_CHOQUE = 0.04  # par an, taux de flux ; ϖ_L = 0,02 au sentier (table du bloc 7)
NB_PAS_DE_L_ENDETTEMENT = 6720
FENETRE_DE_L_ENDETTEMENT = range(6480, 6720)  # t ∈ [6 480 ; 6 720[
PAS_DU_CRITERE_D_ORIGINE = 2159  # écart publié sans verdict (critère d'origine, #139)
SEUIL_DEPOTS = 1e-6  # relatif, max sur la fenêtre (critère de #169, écrit avant l'essai)


class ReleveDeL_Endettement:
    """Observateur léger (6 720 pas) : par pas t, D_F d'ouverture, PIB du pas (lignes 1 à 4
    exécutées, convention de B15), ligne 14 (Div_F), L/K de clôture, plan nominal servi
    (v < y + IN^vol d'ouverture, définition du test du banc partiel) et valeur nette des
    entreprises de clôture ; variables et état de clôture du dernier pas."""

    def __init__(self, initial):
        self._ouverture = initial
        self._montants = {}
        self.depots, self.pib, self.div, self.levier, self.servi, self.valeur_nette = (
            [], [], [], [], [], [])
        self.variables = {}
        self.cloture = None

    def relever(self, e):
        if type(e) is ClotureDePhase:
            for ligne, termes in e.montants:
                if ligne in ("1", "2", "3", "4", "14"):
                    self._montants[ligne] = sum(x for _, x in termes)
        elif type(e) is FinDePas:
            o, f, v = self._ouverture, e.etat, dict(e.variables_du_pas)
            self.depots.append(o.D_F)
            self.pib.append(sum(self._montants[ligne] for ligne in ("1", "2", "3", "4")))
            self.div.append(self._montants["14"])
            self.levier.append(f.L / f.K)
            self.servi.append(v["v"] < v["y"] + o.IN_vol)
            self.valeur_nette.append(idt.valeur_nette_stock(_positions(f), "entreprises"))
            self.variables, self.cloture = v, f
            self._ouverture, self._montants = f, {}


@pytest.fixture(scope="module")
def endettement_sous_varpi_L(socle):
    """Socle complet, π* = 2 %, ϖ_L porté de 0,02 à 0,04 par an dans la table du bloc 7 dès le
    pas 0 et maintenu (tables du sentier, table `banque` remplacée : composition dans `tests/`,
    F1), depuis l'état initial résolu aux tables du sentier, 6 720 pas."""
    sentier = socle.sentier(0.02)
    tables = socle.parametres_du_sentier(sentier)
    assert tables.banque.varpi_L.valeur == 0.02
    choquees = dataclasses.replace(tables, banque=varier(tables.banque, varpi_L=VARPI_L_CHOQUE))
    initial = socle.etat_initial(sentier)
    releve = ReleveDeL_Endettement(initial)
    derouler(socle, sentier, NB_PAS_DE_L_ENDETTEMENT, parametres=choquees, observateur=releve)
    return sentier, tables, releve


def test_endettement_depots_sous_varpi_L_releve_de_deux_points(endettement_sous_varpi_L,
                                                                publier):
    """Fiche 6, § 9.6, « Endettement » (7 (d)), partie dépôts, sur le socle complet (#139, critère
    de #169, P324, P330, écrit avant l'essai) : ϖ_L + 2 points dès le pas 0, π* = 2 % ;
    x_t = D_F d'ouverture du pas t/(n_a PIB_t), PIB_t = lignes 1 à 4 exécutées au pas t (B15),
    en années de PIB ; référence x* = D_F/(n_a PIB) de la résolution (forme fermée
    ν_F p v^e/(p v + ΔIN) du script, qui ne lit pas le taux), lue sur le sentier ; critère :
    max sur t ∈ [6 480 ; 6 720[ de |x_t/x* − 1| ≤ 1e−6. Publiés sans verdict : écart au pas 2 159
    (critère d'origine), levier (L/K de clôture sur lv*, pas où le plan nominal est servi) et
    distribution (Div_F > 0 ; ΣDiv_F/Σ(Div_F + FU) sur les 12 tours 6 708 à 6 719), Δi_{L,t+1},
    Δi_CB, Δi_{D,t+1} et Δr̂*_{t+1} au pas 6 719 (i_L et i_D du pas suivant, écrits en 8c, i_CB du
    pas, r̂* du pas suivant écrit par le bloc 8, contre leurs valeurs résolues), et l'écart
    relatif de Δr̂*_{t+1} à −Δϖ_L/(1 + π*). Probance publiée (lecture A de P330, visa du
    mainteneur du 28/11/2026, formulation de `monnaie`) : tenu ; probant pour le retour sur x* en
    boucle fermée et pour l'indépendance de x* à un taux des dépôts durablement abaissé avec le
    taux directeur (Δi_D = Δi_CB = −2 points) ; non probant pour un i_L durablement relevé : sous
    l'action intégrale de la règle (BC2) et ϱ̄_L constante (P128), le taux neutre retenu absorbe
    ϖ_L, Δr̂* = −Δϖ_L/(1 + π*) (Δi_{L,t+1} et Δr̂* mesurés au pas 6 719). L'ancien verdict
    (banc partiel, 2 160 pas) reste publié :
    `test_investissement.py::test_endettement_depots_sur_leur_forme_fermee_apres_2160_pas`."""
    sentier, tables, r = endettement_sous_varpi_L
    x_etoile = sentier.e["D_F"] / (N_A * sentier.e["PIB"])
    x = [d / (N_A * pib) for d, pib in zip(r.depots, r.pib)]
    assert len(x) == NB_PAS_DE_L_ENDETTEMENT
    pire = max(abs(x[t] / x_etoile - 1.0) for t in FENETRE_DE_L_ENDETTEMENT)
    t_pire = max(FENETRE_DE_L_ENDETTEMENT, key=lambda t: abs(x[t] / x_etoile - 1.0))
    origine = x[PAS_DU_CRITERE_D_ORIGINE] / x_etoile - 1.0
    lv = tables.investissement.lv_etoile
    servis = [abs(k / lv - 1.0) for k, s in zip(r.levier, r.servi) if s]
    dernier = NB_PAS_DE_L_ENDETTEMENT - 1
    fenetre = range(dernier - N_A + 1, dernier + 1)
    div = sum(r.div[k] for k in fenetre)
    fu = r.valeur_nette[dernier] - r.valeur_nette[fenetre[0] - 1]
    delta_i_L = r.variables["i_L_suivant"] - sentier.s["i_L_1"]
    delta_i_CB = r.variables["i_CB"] - sentier.s["i_CB"]
    delta_i_D = r.cloture.i_D - sentier.s["i_D_1"]
    delta_r_hat = r.cloture.r_hat_etoile - sentier.s["r_hat_1"]
    # Absorption attendue par le taux neutre retenu : −Δϖ_L/(1 + π*) (lecture A de P330).
    absorption = -(VARPI_L_CHOQUE - tables.banque.varpi_L.valeur) / (1.0 + sentier.pi)
    publier(f"Fiche 6, endettement (dépôts), ϖ_L + 2 points dès le pas 0, π* = 2 %, 6 720 pas "
            f"({ETIQUETTE} ; #139, critère de #169)", [
        f"x* = {x_etoile:.12f} (résolution) ; max |x_t/x* − 1| sur [6 480 ; 6 720[ : {pire:.2e} "
        f"(pas {f'{t_pire:_}'.replace('_', ' ')} ; seuil 1e−6, verdict)",
        f"écart au pas 2 159 (critère d'origine, sans verdict) : {origine:.2e}",
        f"levier : max |L/K/lv* − 1| {max(servis) if servis else float('nan'):.1e} sur "
        f"{len(servis)} pas servis sur {NB_PAS_DE_L_ENDETTEMENT} (sans verdict)",
        f"distribution : Div_F min {min(r.div):.6e}, Div_F ≤ 0 à {sum(d <= 0.0 for d in r.div)} "
        f"pas ; ΣDiv_F/Σ(Div_F + FU) sur les pas 6 708 à 6 719 : {div / (div + fu):.6f} "
        f"(sans verdict)",
        f"au pas 6 719 : Δi_{{L,t+1}} = {delta_i_L:+.6e}, Δi_CB = {delta_i_CB:+.6e}, "
        f"Δi_{{D,t+1}} = {delta_i_D:+.6e}, Δr̂*_{{t+1}} = {delta_r_hat:+.6e} par an, contre la "
        f"résolution ; Δr̂*_{{t+1}}/(−Δϖ_L/(1 + π*)) − 1 = {delta_r_hat / absorption - 1.0:+.2e} "
        f"(sans verdict)",
        # Probance du verdict (lecture A de P330), publiée telle quelle si le critère est tenu.
        f"tenu ; probant pour le retour sur x* en boucle fermée et pour l'indépendance de x* à "
        f"un taux des dépôts durablement abaissé avec le taux directeur (Δi_D = Δi_CB = −2 "
        f"points) ; non probant pour un i_L durablement relevé : sous l'action intégrale de la "
        f"règle (BC2) et ϱ̄_L constante (P128), le taux neutre retenu absorbe ϖ_L, "
        f"Δr̂* = −Δϖ_L/(1 + π*) (Δi_{{L,t+1}} = {delta_i_L:+.6e}, Δr̂* = {delta_r_hat:+.6e} au "
        f"pas 6 719)" if pire <= SEUIL_DEPOTS
        else "non tenu (probance de la lecture A de P330 sans objet)"])
    assert pire <= SEUIL_DEPOTS


# --------------------------------------------------------------------------
# Fiche 6, « Bornes » (c), refus de la moitié du crédit aux tours 1 à 12 (#140, P150)
# --------------------------------------------------------------------------

PART_REFUSEE = 0.5  # ς_L, part refusée de la hausse demandée (C31)
PAS_DU_REFUS = range(12)  # pas 0 à 11, tours 1 à 12 (tour n = pas n − 1)
FENETRE_DES_BORNES = range(24)  # A ⊂ [0 ; 23] (critère de #140, écrit avant l'essai)


def _refus_de_moitie(t):
    return PART_REFUSEE if t in PAS_DU_REFUS else 0.0


@pytest.fixture(scope="module")
def refus_de_moitie(socle):
    """π* → (relevé, arrêt) : socle complet, ς_L = 0,5 aux pas 0 à 11 puis 0 (entrée de scénario,
    composition dans `tests/`, F1), depuis l'état initial résolu, 720 pas ; `arrêt` : l'exception
    du noyau ou du moteur qui a interrompu la trajectoire, `None` sinon."""
    rendus = {}
    for pi in socle.POINTS_PI:
        releve, arret = Releve(), None
        try:
            derouler(socle, socle.sentier(pi), NB_PAS, varsigma_L=_refus_de_moitie,
                     observateur=releve)
        except (ArretNoyau, ArretMoteur) as e:
            arret = e
        rendus[pi] = (releve, arret)
    return rendus


def _intervalle_dans_la_fenetre(actifs):
    """Critère de #140 : A vide, ou A ⊂ [0 ; 23] intervalle d'entiers consécutifs."""
    return not actifs or (actifs[0] >= FENETRE_DES_BORNES[0]
                          and actifs[-1] <= FENETRE_DES_BORNES[-1]
                          and actifs == list(range(actifs[0], actifs[-1] + 1)))


def _pas_actifs(choc):
    """Borne → liste des pas où elle est active (plancher de Div_F ; D_F ≥ 0 en lecture nette)."""
    return {"plancher de Div_F (ligne 14 = 0)": [p["t"] for p in choc if p["14"] == 0.0],
            "D_F ≥ 0 (D_F de clôture ≤ 0)": [p["t"] for p in choc if p["etat"].D_F <= 0.0]}


def _ensemble_publie(a):
    """« actif à aucun pas » ; « actif aux pas a à b (n pas) » si A est un intervalle d'entiers
    consécutifs ; la liste exacte sinon."""
    if not a:
        return "actif à aucun pas"
    if a == list(range(a[0], a[-1] + 1)):
        return f"actif aux pas {a[0]} à {a[-1]} ({len(a)} pas)"
    return f"actif aux pas {a} ({len(a)} pas)"


def _probance_des_bornes(choc, controle):
    """Lignes de probance de #140, sans seuil, sur les n = len(choc) pas déroulés (720 hors
    arrêt), appariés pas à pas au contrôle."""
    n = len(choc)
    if n == 0:
        return ["aucun pas déroulé : probance sans objet"]
    pas, fenetre = range(n), range(min(n, len(FENETRE_DES_BORNES)))
    t_div = min(pas, key=lambda t: choc[t]["14"])
    t_rap = min(pas, key=lambda t: choc[t]["14"] / controle[t]["14"])
    d_f = [p["etat"].D_F / idt.echelle_bilan(_positions(p["etat"]), "entreprises") for p in choc]
    t_df = min(pas, key=lambda t: d_f[t])
    baisses = [choc[t]["variables"]["I_vol_plan"] / controle[t]["variables"]["I_vol_plan"] - 1.0
               for t in fenetre]
    t_i = min(fenetre, key=lambda t: baisses[t])
    non_satisfaite = sum(p["variables"]["Delta_L_d"] - p["18"] for p in choc)
    servi_au_controle = sum(controle[t]["18"] for t in PAS_DU_REFUS)
    ecarts = [controle[t]["etat"].L - choc[t]["etat"].L for t in pas]
    t_l = max(fenetre, key=lambda t: ecarts[t])
    relatifs = [ecarts[t] / controle[t]["etat"].L for t in pas]
    t_r, fin = max(pas, key=lambda t: relatifs[t]), n - 1
    ln_p = math.log(choc[fin]["variables"]["p"] / controle[fin]["variables"]["p"])
    div_bk = [p["t"] for p in choc if p["15"] == 0.0]
    return [
        *(f"{nom} : {_ensemble_publie(a)}" for nom, a in _pas_actifs(choc).items()),
        f"ligne 14 (Div_F) : min {choc[t_div]['14']:.6e} u.m. par pas (pas {t_div}) ; "
        f"min ligne 14/contrôle {choc[t_rap]['14'] / controle[t_rap]['14']:.6f} (pas {t_rap})",
        f"D_F/S^F de clôture : min {d_f[t_df]:.6f} (pas {t_df})",
        f"I^{{vol,plan}}/contrôle − 1 sur les pas 0 à {fenetre[-1]} : plus forte baisse "
        f"{baisses[t_i]:+.4%} (pas {t_i})",
        f"demande de crédit non satisfaite cumulée (Σ(ΔL^d − ligne 18), {n} pas ; le cumul "
        f"inclut le report (redemandes)) : {non_satisfaite:.6e} u.m., "
        f"{non_satisfaite / servi_au_controle:.4f} fois le crédit nouveau cumulé du contrôle "
        f"(Σ ligne 18) des pas 0 à 11",
        f"écart de stock maximal max_t (L^c_t − L^choc_t), L de clôture, pas 0 à "
        f"{fenetre[-1]} : {ecarts[t_l]:.6e} u.m., {ecarts[t_l] / servi_au_controle:.4f} fois le "
        f"même dénominateur (pas {t_l})",
        f"écart relatif de stock (L^c_t − L^choc_t)/L^c_t : max {relatifs[t_r]:.4e} (pas {t_r}) ; "
        f"au pas {fin} {relatifs[fin]:.4e}, ln(p^choc/p^c) {ln_p:.4e} ; résidu terminal : effet "
        f"de niveau des prix (la règle cible l'inflation, pas le niveau)",
        "Div_Bk = 0 (ligne 15, fiche 7) aux pas : " + (str(div_bk) if div_bk else "aucun")]


def test_critere_des_bornes_de_140_sur_des_ensembles_synthetiques():
    """Prédicat du critère de #140 sur des ensembles de pas actifs écrits à la main : vide,
    intervalles inclus dans [0 ; 23] admis ; trou (réactivation), débordement après 23 refusés."""
    admis = ([], [0], [23], list(range(24)), list(range(3, 9)))
    refuses = ([0, 2], [5, 6, 8], [23, 24], [24], list(range(10, 30)))
    assert all(_intervalle_dans_la_fenetre(a) for a in admis)
    assert not any(_intervalle_dans_la_fenetre(a) for a in refuses)


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_bornes_c_sous_le_refus_de_la_moitie_du_credit(banc, refus_de_moitie, pi, publier):
    """Fiche 6, § 9.6, « Bornes » (c), partie refus de crédit (C31), sur le socle complet (#140,
    critère de P150, écrit avant l'essai) : ς_L,t = 0,5 aux pas 0 à 11 (tours 1 à 12), 0 ensuite ;
    contrôle apparié (même banc sans choc, `banc`) ; 720 pas. Bornes surveillées : plancher du
    dividende des entreprises, active au pas t si la ligne 14 exécutée = 0 ; D_F ≥ 0 en lecture
    nette, active si D_F de clôture ≤ 0. Critère : 720 pas sans arrêt du noyau ni du moteur ;
    pour chaque borne, l'ensemble A des pas actifs est vide, ou A ⊂ [0 ; 23] et A est un
    intervalle d'entiers consécutifs. Contrôle du scénario : ligne 18 = clause de F1 sous ς_L,
    au bit, à chaque pas. Probance (intention reportée, P150), publiée sans seuil : nombre de pas
    actifs ; min de la ligne 14 (u.m. par pas) et du rapport ligne 14/contrôle ; min de D_F/S^F
    de clôture ; plus forte baisse relative de I^{vol,plan} contre le contrôle sur les pas 0 à
    23 ; demande de crédit non satisfaite cumulée Σ(ΔL^d − ligne 18) sur 720 pas (u.m., et
    rapportée au crédit nouveau cumulé du contrôle, Σ ligne 18, sur les pas 0 à 11), qui inclut
    le report : F1 vise un niveau et redemande au pas suivant le crédit refusé, chaque redemande
    est comptée (réserve de `macro`, décision du mainteneur) ; à côté, sans seuil, l'écart de
    stock maximal max_t (L^c_t − L^choc_t) sur les pas 0 à 23 (fenêtre du refus et de la
    désactivation), L stock de crédit des entreprises à la clôture, en u.m. et rapporté au même
    dénominateur, avec son pas ; l'écart relatif (L^c_t − L^choc_t)/L^c_t, max sur 720 pas avec
    son pas, et sa valeur au dernier pas à côté de ln(p^choc/p^c) au même pas : le résidu
    terminal est un effet de niveau des prix, la règle ciblant l'inflation et non le niveau
    (avis de `macro`) ; pas où Div_Bk = 0 (ligne 15, fiche 7). Si
    aucune borne ne s'active : « tenu, non probant pour le délai de désactivation » (verdict
    visé par le mainteneur le 28/11/2026 ; non probant de façon structurelle, le refus ne
    portant que sur la hausse demandée et le crédit refusé étant redemandé : suite à #210). En
    cas d'arrêt, le pas atteint, l'arrêt et la probance sur la partie déroulée sont publiés
    avant l'échec."""
    releve, arret = refus_de_moitie[pi]
    if arret is not None:
        publier(f"Fiche 6, bornes (c), refus de la moitié du crédit, π* = {100 * pi:g} % : "
                f"arrêt capté ({ETIQUETTE} ; #140)", [
            f"pas atteint : {len(releve.pas)} sur {NB_PAS} ; arrêt : {arret!r}",
            *_probance_des_bornes(releve.pas, banc[pi][2].pas)])
    assert arret is None, f"arrêt au pas {len(releve.pas)} : {arret!r}"
    controle = banc[pi][2].pas
    choc = releve.pas
    assert len(choc) == len(controle) == NB_PAS
    for p in choc:
        assert p["18"] == bloc_6.credit_servi(_refus_de_moitie(p["t"]),
                                              p["variables"]["Delta_L_d"]), p["t"]
    actifs = _pas_actifs(choc)
    tenu = all(_intervalle_dans_la_fenetre(a) for a in actifs.values())
    nb_actifs = sum(len(a) for a in actifs.values())
    publier(f"Fiche 6, bornes (c), refus de la moitié du crédit aux pas 0 à 11 (tours 1 à 12), "
            f"π* = {100 * pi:g} %, 720 pas ({ETIQUETTE} ; #140, critère de P150)", [
        *_probance_des_bornes(choc, controle),
        f"pas actifs (deux bornes) : {nb_actifs} ; verdict : "
        + ("non tenu" if not tenu else "tenu" if nb_actifs
           else "tenu, non probant pour le délai de désactivation")])
    assert tenu, actifs


# --------------------------------------------------------------------------
# #131, point 2 : terme de Jensen de BC2 sur le socle complet, formes (A) et (L) (mesure)
# --------------------------------------------------------------------------
# Protocole de `monnaie`, écrit avant l'essai (feuille de route, historique, partie J,
# complément du rang 1 de la ligne 14, `17c26c2`) ; constat sans verdict du modèle : seuls les
# contrôles de validité K1 à K4 sont assertés (concluant / non concluant).

PI_131 = 0.02
LAMBDAS_131 = (0.1, 0.2, 0.4)
CHOCS_131 = (0.01, -0.01)  # Δ sur π^e_0, fraction par an ; contrôle apparié Δ = 0
H_131 = 14_228  # 40 demi-vies de 355,69 tours (branche λ_e = 0,1, M3)
H_PRIME_131 = 10_671  # horizon de K4
FENETRE_131 = 12  # moyennes sur [H − 12 ; H − 1]
SEUIL_K3 = 1e-11  # absolu, fraction par an
SEUIL_K4_R = 1e-7  # point de % par an
SEUIL_K4_L = 4e-9  # sans dimension (log)
EPSILON_R = 1e-6  # point de % par an
EPSILON_L = 4e-8  # sans dimension (log)
NB_PAS_K2 = 720
ARITHMETIQUE, LOG = "(A)", "(L)"


def taux_neutre_suivant_en_log(r_hat, pi_prec, pi_etoile, a_I_pas):
    """BC2 en log, forme (L) de #131 : r̂*_{t+1} = r̂*_t + (a_I/n_a)[ln(1 + π_{t−1}) −
    ln(1 + π*_t)], par an ; même signature que `bloc_8.taux_neutre_suivant`. Essai dans `tests/`,
    sans balise d'équation (la forme exécutée par le moteur reste BC2 arithmétique)."""
    return r_hat + a_I_pas * (math.log1p(pi_prec) - math.log1p(pi_etoile))


def bloc_8_compose(taux_neutre):
    """Bloc 8 réel dont la phase 1 calcule le taux neutre par `taux_neutre` (signature de
    `bloc_8.taux_neutre_suivant`) ; sous-classe sans attribut d'instance, même déclaration
    (composition dans `tests/`, précédent `bloc_9_compose`, jamais un drapeau dans `src/`, F1).
    Le corps est une copie de `BanqueCentrale.phase_1` où seul l'appel de BC2 change : sa
    fidélité est soumise à K2 (`test_131_k2_sous_classe_arithmetique_au_bit`)."""

    def phase_1(self, vue):
        table = vue.parametres.banque_centrale
        pi_prec = vue.glissement()
        pi_etoile = vue.ouverture.pi_etoile
        r_hat = vue.ouverture.r_hat_etoile
        i_regle = bloc_8.taux_indique_par_la_regle(r_hat, pi_etoile, pi_prec, table.a_pi)
        i_CB = i_regle
        vue.ecrire_pas("i_regle", i_regle)
        vue.ecrire_pas("i_CB", i_CB)
        vue.ecrire_etat("r_hat_etoile",
                        taux_neutre(r_hat, pi_prec, pi_etoile, par_pas(table.a_I)))
        vue.ecrire_etat("pi_e", bloc_8.anticipation_suivante(vue.ouverture.pi_e, pi_prec,
                                                             par_pas(table.lambda_e)))
        vue.ecrire_etat("pi_etoile", bloc_8.cible_suivante(pi_etoile))
        vue.ecrire_pas("theta_CB", bloc_8.part_a_l_emission(table.theta_CB))
        i_pas = par_pas(TauxDeFlux(i_CB))
        vue.ecrire_pas("Pi_CB", bloc_8.resultat(i_pas, vue.ouverture.B_CB, i_pas,
                                                vue.ouverture.L_CB, i_pas, vue.ouverture.Res))

    return type("BanqueCentraleComposee", (BanqueCentrale,),
                {"__slots__": (), "phase_1": phase_1})()


def _ordonnanceur_131(socle, sentier, forme):
    """Socle complet aux tables du sentier ; bloc 8 réel sous (A), composé en log sous (L)."""
    rendus = socle.blocs_du_socle_complet()
    if forme == LOG:
        bc = bloc_8_compose(taux_neutre_suivant_en_log)
        rendus = tuple(bc if b.declaration.radical == "banque_centrale" else b for b in rendus)
    return ordo.assembler(PHASES, rendus, socle.parametres_du_sentier(sentier),
                          socle.ENTREES_DU_SOCLE)


class _ReleveDe131:
    """Observateur léger : par pas t, r̂*_{t+1} (état t + 1) et P_t (tête du registre t + 1)."""

    __slots__ = ("prix", "r_hat")

    def __init__(self, etat):
        self.r_hat = [etat.r_hat_etoile]  # r̂*_t d'ouverture, t = 0, …, H
        self.prix = []  # P_t, t = 0, …, H − 1

    def relever(self, e):
        if type(e) is FinDePas:
            self.r_hat.append(e.etat.r_hat_etoile)
            self.prix.append(e.etat.registre_prix[0])


class Trajectoire131(NamedTuple):
    r_hat: list
    prix: list  # P_k, k = −13, …, H − 1 (indice k + 13)
    a_I_pas: float
    pi_etoile: float
    arret: Exception | None
    etat: schema.EtatPays  # état d'ouverture du pas H (dernier état atteint si arrêt)


def _trajectoire_131(socle, forme, lambda_e, delta, nb_pas=H_131):
    sentier = socle.sentier(PI_131, lambda_e=lambda_e)
    o = _ordonnanceur_131(socle, sentier, forme)
    etat = socle.etat_initial(sentier, choc_pi_e0=delta)
    releve = _ReleveDe131(etat)
    passe = tuple(reversed(etat.registre_prix))  # P_{−13}, …, P_{−1}
    entrees = socle.entrees_du_tour()
    arret = None
    try:
        for _ in range(nb_pas):
            etat = ordo.executer_pas(etat, entrees, o, releve)
    except (ArretNoyau, ArretMoteur) as e:
        arret = e
    table = socle.parametres_du_sentier(sentier).banque_centrale
    return Trajectoire131(releve.r_hat, list(passe) + releve.prix, par_pas(table.a_I),
                          socle.etat_initial(sentier).pi_etoile, arret, etat)


@pytest.fixture(scope="module")
def mesure_131(socle):
    """(forme, λ_e, Δ) → `Trajectoire131` : 18 trajectoires de H pas (12 essais, 6 contrôles
    Δ = 0), π* = 2 %, depuis l'état initial résolu aux tables du sentier à λ_e."""
    return {(forme, lam, delta): _trajectoire_131(socle, forme, lam, delta)
            for forme in (ARITHMETIQUE, LOG) for lam in LAMBDAS_131
            for delta in (0.0, *CHOCS_131)}


def _moyenne_de_fenetre(serie, fin):
    """Moyenne de `serie` (indexée par t) sur [fin − 12 ; fin − 1]."""
    return math.fsum(serie[fin - FENETRE_131:fin]) / FENETRE_131


def _r_et_l(essai, controle, fin):
    """R (point de % par an) et L (log) sur [fin − 12 ; fin − 1] ; P_t à l'indice t + 13."""
    r = 100.0 * _moyenne_de_fenetre([a - b for a, b in zip(essai.r_hat, controle.r_hat)], fin)
    ln_p = [math.log(a / b) for a, b in zip(essai.prix[13:], controle.prix[13:])]
    return r, _moyenne_de_fenetre(ln_p, fin)


def _ln_p_sur_p_etoile(traj, p_0, k):
    """ln(P_k/P*_k), P*_k = P_0 (1 + π*)^{k/n_a}."""
    return math.log(traj.prix[k + 13] / p_0) - k / N_A * math.log1p(traj.pi_etoile)


def _glissements(traj, nb_pas):
    """π_{t−1} = P_{t−1}/P_{t−13} − 1, t = 0, …, nb_pas − 1 (même calcul que le registre)."""
    return [traj.prix[t + 12] / traj.prix[t] - 1.0 for t in range(nb_pas)]


def _jensen(traj, nb_pas=H_131):
    """J_H = (a_I/n_a) Σ_{t<H} [π_{t−1} − ln(1 + π_{t−1}) − (π* − ln(1 + π*))], fraction."""
    pe = traj.pi_etoile - math.log1p(traj.pi_etoile)
    return traj.a_I_pas * math.fsum(p - math.log1p(p) - pe for p in _glissements(traj, nb_pas))


def _residu_telescopique(traj, forme, p_0, nb_pas=H_131):
    """K3 : r̂*_H − r̂*_0 − (a_I/n_a)[Σ_{k=H−13}^{H−2} ln(P_k/P*_k) − Σ_{k=−13}^{−2}
    ln(P_k/P*_k)], moins J_H sous (A) ; fraction par an."""
    fin = math.fsum(_ln_p_sur_p_etoile(traj, p_0, k) for k in range(nb_pas - 13, nb_pas - 1))
    debut = math.fsum(_ln_p_sur_p_etoile(traj, p_0, k) for k in range(-13, -1))
    residu = traj.r_hat[nb_pas] - traj.r_hat[0] - traj.a_I_pas * (fin - debut)
    return residu - _jensen(traj, nb_pas) if forme == ARITHMETIQUE else residu


def _delta_131(delta):
    return "0 (contrôle)" if delta == 0.0 else f"{delta:+g}"


def _p_0(mesure_131, forme, lambda_e):
    """P_0 simulé du contrôle apparié (forme, λ_e, Δ = 0), ancre de P* : indice des prix du pas 0
    (indice 13 de `prix`)."""
    return mesure_131[forme, lambda_e, 0.0].prix[13]


def _exiger_k1(mesure_131):
    """K3, K4 et la publication supposent les 18 trajectoires menées à H : sinon, non concluant
    (K1), sans lever d'`IndexError`."""
    if any(t.arret is not None for t in mesure_131.values()):
        pytest.skip("non concluant : K1")


def _au_bit(valeur):
    """Forme comparable au bit (K2) : chaque flottant par `float.hex` (−0,0 distinct de +0,0, NaN
    égal à lui-même), récursivement dans les n-uplets, listes et dictionnaires (clés triées par
    `repr`)."""
    if isinstance(valeur, float):
        return float.hex(valeur)
    if isinstance(valeur, (tuple, list)):
        return tuple(_au_bit(x) for x in valeur)
    if isinstance(valeur, dict):
        return tuple(sorted(((k, _au_bit(x)) for k, x in valeur.items()),
                            key=lambda kx: repr(kx[0])))
    return valeur


def test_131_k2_sous_classe_arithmetique_au_bit(socle):
    """K2 (#131) : `bloc_8_compose(bloc_8.taux_neutre_suivant)` reproduit au bit le bloc 8 réel,
    λ_e = 0,2, Δ = +0,01, 720 pas : à chaque pas, états de fin de pas (tous les champs du
    schéma), variables du pas, grandeurs d'ouverture et montants exécutés de chaque ligne (et
    leurs termes) du relevé, flottants comparés par `float.hex`."""
    sentier = socle.sentier(PI_131, lambda_e=0.2)
    tables = socle.parametres_du_sentier(sentier)
    rendus = socle.blocs_du_socle_complet()
    compose = bloc_8_compose(bloc_8.taux_neutre_suivant)
    assert type(compose) is not BanqueCentrale and isinstance(compose, BanqueCentrale)
    composes = tuple(compose if b.declaration.radical == "banque_centrale" else b
                     for b in rendus)
    suites = []
    for blocs_du_banc in (rendus, composes):
        o = ordo.assembler(PHASES, blocs_du_banc, tables, socle.ENTREES_DU_SOCLE)
        etat = socle.etat_initial(sentier, choc_pi_e0=0.01)
        releve = Releve()
        for _ in range(NB_PAS_K2):
            etat = ordo.executer_pas(etat, socle.entrees_du_tour(), o, releve)
        suites.append([_au_bit({**{k: v for k, v in p.items() if k != "etat"},
                                "etat": [getattr(p["etat"], c) for c in schema.CHAMPS]})
                       for p in releve.pas])
    reel, compose_ = suites
    assert len(reel) == len(compose_) == NB_PAS_K2
    for t, (a, b) in enumerate(zip(reel, compose_)):
        assert a == b, f"pas {t}"


def test_131_k1_aucun_arret_ni_refus(mesure_131, publier):
    """K1 (#131) : aucun arrêt du noyau ni refus du moteur sur les 18 trajectoires de H pas."""
    arrets = {cle: (len(t.prix) - 13, t.arret) for cle, t in mesure_131.items()
              if t.arret is not None}
    if arrets:
        publier("#131, K1 : arrêts captés (non concluant)",
                [f"{cle} : pas atteint {pas} ; {arret!r}" for cle, (pas, arret) in arrets.items()])
    assert not arrets


def test_131_k3_identites_telescopiques(mesure_131, publier):
    """K3 (#131) : identités télescopiques à 1e−11 (absolu, fraction par an) sur les 18
    trajectoires ; sous (L), r̂*_H − r̂*_0 = (a_I/n_a)[Σ_{k=H−13}^{H−2} ln(P_k/P*_k) −
    Σ_{k=−13}^{−2} ln(P_k/P*_k)] ; sous (A), même écart plus le terme de Jensen J_H."""
    _exiger_k1(mesure_131)
    residus = {(forme, lam, delta): _residu_telescopique(t, forme, _p_0(mesure_131, forme, lam))
               for (forme, lam, delta), t in mesure_131.items()}
    publier(f"#131, K3 : résidus des identités télescopiques, H = {H_131} pas, seuil "
            f"{SEUIL_K3:g} (fraction par an ; {ETIQUETTE})",
            [f"{forme}, λ_e = {lam:g}, Δ = {_delta_131(delta)} : {r:+.3e}"
             for (forme, lam, delta), r in residus.items()])
    assert all(abs(r) <= SEUIL_K3 for r in residus.values()), residus


def _mesures_131(mesure_131, fin=H_131):
    """(forme, λ_e, Δ) → (R, L) à l'horizon `fin`, Δ ≠ 0."""
    return {(forme, lam, delta): _r_et_l(mesure_131[forme, lam, delta],
                                         mesure_131[forme, lam, 0.0], fin)
            for forme in (ARITHMETIQUE, LOG) for lam in LAMBDAS_131 for delta in CHOCS_131}


def test_131_k4_arrivee_atteinte(mesure_131, publier):
    """K4 (#131) : |R_H − R_{H′}| ≤ 1e−7 point et |L_H − L_{H′}| ≤ 4e−9, H′ = 10 671, sur les
    12 essais. Tenu à H (mesure du rang 4 de la ligne 14) : l'extension unique à 2H que prévoit
    le protocole n'est pas codée ; un échec ici est « non concluant », et l'extension se déclare
    alors par un commit (au-delà, rapport au mainteneur)."""
    _exiger_k1(mesure_131)
    a_h, a_hp = _mesures_131(mesure_131), _mesures_131(mesure_131, H_PRIME_131)
    ecarts = {cle: (a_h[cle][0] - a_hp[cle][0], a_h[cle][1] - a_hp[cle][1]) for cle in a_h}
    publier(f"#131, K4 : R_H − R_H′ (point) et L_H − L_H′, H = {H_131}, H′ = {H_PRIME_131} "
            f"(seuils {SEUIL_K4_R:g} point, {SEUIL_K4_L:g} ; {ETIQUETTE})",
            [f"{forme}, λ_e = {lam:g}, Δ = {delta:+g} : {dr:+.3e} point ; {dl:+.3e}"
             for (forme, lam, delta), (dr, dl) in ecarts.items()])
    assert all(abs(dr) <= SEUIL_K4_R and abs(dl) <= SEUIL_K4_L
               for dr, dl in ecarts.values()), ecarts


def classer_131(r_par_cle):
    """Classification d'une forme (#131, constat) : `r_par_cle` : (λ_e, Δ) → R (point).

    Classes testées dans cet ordre de priorité, la première vérifiée l'emporte :
    1. (F) si max |R| ≤ ε_R ; testée en premier, elle rend aussi (F) quand max |R| ≤ ε_R alors
       que D_R > ε_R pour un signe (possible puisque D_R ≤ 2 max |R|), cas que le protocole de
       `monnaie` ne tranche pas ;
    2. (C) si D_R > ε_R pour un signe au moins ;
    3. (I) si |R| > ε_R partout (et donc D_R ≤ ε_R pour les deux signes) ;
    4. « non classée » sinon (aucun D_R > ε_R, |R| ≤ ε_R pour une clé au moins, max |R| > ε_R) :
       issue ajoutée hors protocole, qui n'existe que pour rendre le prédicat total et ne change
       aucun classement des trois classes du protocole."""
    d_r = {delta: max(r_par_cle[lam, delta] for lam in LAMBDAS_131)
           - min(r_par_cle[lam, delta] for lam in LAMBDAS_131) for delta in CHOCS_131}
    if max(abs(r) for r in r_par_cle.values()) <= EPSILON_R:
        return "(F) r̂* fixé par la boucle", d_r
    if any(d > EPSILON_R for d in d_r.values()):
        return "(C) continuum de r̂* au socle complet", d_r
    if all(abs(r) > EPSILON_R for r in r_par_cle.values()):
        return "(I) écart permanent indépendant de λ_e", d_r
    return "non classée", d_r


def test_classer_131_sur_des_valeurs_synthetiques():
    """Prédicat de classification de #131 sur des valeurs écrites à la main."""
    def valeurs(f):
        return {(lam, d): f(lam, d) for lam in LAMBDAS_131 for d in CHOCS_131}
    assert classer_131(valeurs(lambda lam, d: 1e-7))[0].startswith("(F)")
    assert classer_131(valeurs(lambda lam, d: 1e-4 * lam))[0].startswith("(C)")
    assert classer_131(valeurs(lambda lam, d: 1e-4 + 1e-8 * lam))[0].startswith("(I)")
    assert classer_131(valeurs(lambda lam, d: 1e-4 if d > 0 else 1e-8))[0] == "non classée"
    # max |R| ≤ ε_R et D_R > ε_R (± 0,9 ε_R aux λ_e extrêmes) : (F), priorité de (F) sur (C)
    bord = valeurs(lambda lam, d: {0.1: 0.9, 0.2: 0.0, 0.4: -0.9}[lam] * EPSILON_R)
    classe, d_r = classer_131(bord)
    assert all(d > EPSILON_R for d in d_r.values()) and classe.startswith("(F)")


def _arrivee_a_l_echelle_nominale(etat, etat_c):
    """Réserve R4 de `monnaie` (#131, hors protocole, sans seuil) : écarts de l'état `etat` à
    l'état apparié du contrôle `etat_c`, rapportés à ln(P/P_c), P = tête du registre des prix.

    Rend (ln(P/P_c), (max |x/x_c − 1|, nom) des variables d'état réelles et sans dimension
    (invariance `VOLUME` ou `SANS_DIMENSION`), (max |ln(x/x_c) − ln(P/P_c)|, nom) des variables
    nominales (`NOMINAL` : positions, V^flux, variables nominales des blocs) et des niveaux du
    registre des prix (`INDICE`), noms des variables nulles aux deux états, écartées). Le
    compteur de pas `t` (entier) est écarté ; un rapport nul, négatif ou de dénominateur nul
    rend +inf."""
    ln_p = math.log(etat.registre_prix[0] / etat_c.registre_prix[0])
    reels, nominaux, nulles = [], [], []
    for v in schema.VARIABLES:
        if v.type is int:
            continue
        a, b = getattr(etat, v.nom), getattr(etat_c, v.nom)
        paires = (tuple((f"{v.nom}[{k}]", x, y) for k, (x, y) in enumerate(zip(a, b)))
                  if v.type is tuple else ((v.nom, a, b),))
        for nom, x, y in paires:
            if x == 0.0 and y == 0.0:
                nulles.append(nom)
            elif v.invariance in (Invariance.NOMINAL, Invariance.INDICE):
                q = x / y if y != 0.0 else math.inf
                nominaux.append((abs(math.log(q) - ln_p) if 0.0 < q < math.inf else math.inf,
                                 nom))
            else:
                reels.append((abs(x / y - 1.0) if y != 0.0 else math.inf, nom))
    return ln_p, max(reels), max(nominaux), nulles


def test_131_mesure_du_terme_de_jensen_publiee(mesure_131, socle, publier):
    """#131, point 2 (constat sans verdict du modèle, visa `monnaie`) : à π* = 2 %, par forme
    ((A) bloc 8 réel, (L) BC2 en log), λ_e ∈ {0,1 ; 0,2 ; 0,4} et Δ = ± 1 point sur π^e_0, moyennes
    sur [H − 12 ; H − 1], H = 14 228 pas : R = r̂*_t − r̂*_t,c (point de % par an), r̂*_t,c − r̄ ;
    L = ln(P_t/P_t,c), ln(P_t/P*_t) avec P*_t = P_0 (1 + π*)^{t/n_a}, P_0 simulé du contrôle
    apparié ; coefficient en Δ², R/Δ² (R et Δ en fraction), et L/Δ² (hors protocole) ; D_R =
    max_λ R − min_λ R par signe ; sous (A), J_H − J_H,c ; contrôle de `monnaie` (rang 2)
    r̂*_{∞,c} − [ϱ̄_L − ϖ_L/(1 + π*)], r̂*_{∞,c} moyenne du contrôle sur la même fenêtre.
    Classification par forme (ε_R = 1e−6 point) et, sous (L), niveau des prix « ramené au
    sentier » si max |L| ≤ ε_L = 4e−8. Sous (A), réserve R4 de `monnaie` (hors protocole, sans
    seuil) : à l'état d'ouverture du pas H, par λ_e et par signe, écart maximal des grandeurs
    réelles et sans dimension au contrôle apparié et des grandeurs nominales et positions à
    ln(P/P_c) (`_arrivee_a_l_echelle_nominale`). Aucune assertion : la validité est jugée par
    K1 à K4 (non concluant si K1 ne l'est pas)."""
    _exiger_k1(mesure_131)
    mesures = _mesures_131(mesure_131)
    for forme in (ARITHMETIQUE, LOG):
        lignes = []
        for lam in LAMBDAS_131:
            sentier = socle.sentier(PI_131, lambda_e=lam)
            controle = mesure_131[forme, lam, 0.0]
            p_0 = _p_0(mesure_131, forme, lam)
            r_c = _moyenne_de_fenetre(controle.r_hat, H_131)
            p_c = _moyenne_de_fenetre(
                [_ln_p_sur_p_etoile(controle, p_0, t) for t in range(H_131)], H_131)
            norme = sentier.s["rho_bar_L"] - sentier.par.varpi_L / (1.0 + PI_131)
            lignes.append(
                f"λ_e = {lam:g}, contrôle : r̂*_c − r̄ = {100 * (r_c - sentier.par.rbar):+.3e} "
                f"point ; r̂*_∞,c − [ϱ̄_L − ϖ_L/(1 + π*)] = {100 * (r_c - norme):+.3e} point ; "
                f"ln(P_c/P*) = {p_c:+.3e}")
            for delta in CHOCS_131:
                essai = mesure_131[forme, lam, delta]
                r, ln_p = mesures[forme, lam, delta]
                p_e = _moyenne_de_fenetre(
                    [_ln_p_sur_p_etoile(essai, p_0, t) for t in range(H_131)], H_131)
                jensen = (f" ; J_H − J_H,c = {_jensen(essai) - _jensen(controle):+.3e}"
                          if forme == ARITHMETIQUE else "")
                lignes.append(
                    f"λ_e = {lam:g}, Δ = {delta:+g} : R = {r:+.4e} point ; "
                    f"R/Δ² (R et Δ en fraction) = {r / 100 / delta ** 2:+.3e} ; "
                    f"L = {ln_p:+.4e} ; L/Δ² = {ln_p / delta ** 2:+.4e} ; "
                    f"ln(P/P*) = {p_e:+.4e}" + jensen)
        classe, d_r = classer_131({(lam, d): mesures[forme, lam, d][0]
                                   for lam in LAMBDAS_131 for d in CHOCS_131})
        lignes.append("D_R (point) : " + " ; ".join(f"Δ = {d:+g} : {v:.4e}"
                                                    for d, v in d_r.items()))
        max_l = max(abs(mesures[forme, lam, d][1]) for lam in LAMBDAS_131 for d in CHOCS_131)
        d_l = {d: max(mesures[forme, lam, d][1] for lam in LAMBDAS_131)
               - min(mesures[forme, lam, d][1] for lam in LAMBDAS_131) for d in CHOCS_131}
        lignes.append(f"max |L| = {max_l:.4e} ; D_L : "
                      + " ; ".join(f"Δ = {d:+g} : {v:.4e}" for d, v in d_l.items()))
        lignes.append(f"classification : {classe}")
        if forme == ARITHMETIQUE:
            lignes.append("arrivée = état du contrôle remis à une autre échelle nominale (racine "
                          "nominale) ; état d'ouverture du pas H, hors protocole, sans seuil :")
            nulles = set()
            for lam in LAMBDAS_131:
                for delta in CHOCS_131:
                    ln_p, (e_r, n_r), (e_n, n_n), zeros = _arrivee_a_l_echelle_nominale(
                        mesure_131[forme, lam, delta].etat, mesure_131[forme, lam, 0.0].etat)
                    nulles.update(zeros)
                    lignes.append(
                        f"λ_e = {lam:g}, Δ = {delta:+g} : ln(P/P_c) = {ln_p:+.4e} ; réelles et "
                        f"sans dimension, max |x/x_c − 1| = {e_r:.2e} ({n_r}) ; nominales et "
                        f"positions, max |ln(x/x_c) − ln(P/P_c)| = {e_n:.2e} ({n_n})")
            lignes.append("nulles aux deux états, écartées : " + ", ".join(sorted(nulles)))
        if forme == LOG:
            lignes.append("niveau des prix : " + ("ramené au sentier" if max_l <= EPSILON_L
                                                  else "non ramené au sentier (max |L| > ε_L)"))
        publier(f"#131, point 2, forme {forme}, π* = 2 %, H = {H_131} pas, moyennes sur "
                f"[H − 12 ; H − 1] ({ETIQUETTE} ; constat sans verdict du modèle)", lignes)
