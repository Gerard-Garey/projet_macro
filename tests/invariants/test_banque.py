"""Bloc 7, banque commerciale, dans le socle partiel d'essai : lignes de classe (b) (#90).

Classe (b) du classement du rang 1a de J3-c (synthèse en commentaire de la PR
#129, § 1 ; fiche 7, § 9.6) : état stationnaire (P77 : moteur à n_a = 12 aux
trois π*, valeurs de référence du script `outils/etat_stationnaire.py`, jamais
recopiées) ; superneutralité des écarts ; parties (b) de « Réserves et
refinancement » (à chaque clôture ; identité B19), « Résultat et lignes
exécutées » (Π^Bk égal aux lignes 9 + 11b + 12 − 10 − 13 exécutées), « Phases »
(lecture hors ordre refusée à l'assemblage) et « Empreinte » (reprise exacte,
tenue par `test_socle_partiel.py` avec tous les blocs réels ; coût, par
`test_budget.py`). S'y ajoutent le **câblage en phase** de B1 à B7 hors du point
fixe, comparé au bit à une forme recalculée par le test (leçon de l'audit du
rang 4), B7 dans ses trois cas dans le moteur, E^Bk du bloc comparé à
`valeur_nette_stock` à chaque ouverture, et l'écart du bloc réel au bloc d'essai
7 sur 720 pas. Seuils écrits avant l'essai (fiche 7, § 9.6 ;
`sec:banque-conditions`), non déplacés.

Les blocs réels de la production, du travail, des prix, de la banque et de la
banque centrale remplacent les blocs d'essai de leur radical ; les blocs 5, 6 et
9 sont des blocs d'essai sur le sentier (bloc 9 : E1 et E2). **Étiquettes** :
toute mesure dynamique porte « plans nominaux exogènes » ; aucune mesure ici ne
vaut verdict de la boucle T3 ↔ BC3 (P87, rang 6), de la stationnarité partielle
étendue (P94, rang 6) ni de la boucle conjointe (#114).
"""

import dataclasses
import math

import pytest

from nations.blocs.banque import Banque, fonds_propres
from nations.blocs.banque_centrale import BanqueCentrale
from nations.blocs.prix import Prix
from nations.blocs.production import Production
from nations.blocs.travail import Travail
from nations.moteur import ordonnanceur as ordo
from nations.moteur.contrat_bloc import GRAND_LIVRE, Lecture
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
ETIQUETTES = "plans nominaux exogènes ; blocs 2, 3, 4, 7 et 8 réels"
# Seuils écrits avant l'essai (fiche 7, § 9.6 ; P94 pour l'écart au bloc d'essai).
SEUIL_UN_PAS = 1e-10
SEUIL_BK = 1e-12  # × S^Bk
SEUIL_CB = 1e-12  # × S^CB
SEUIL_ECART_AU_BLOC_D_ESSAI = 1e-9  # × S du secteur
LIGNES_RELEVEES = ("9", "10", "11b", "12", "13", "15", "18", "21")


class Releve:
    """Observateur d'essai : par pas, montants exécutés des lignes relevées (par terme et total),
    variables du pas, état t + 1."""

    def __init__(self):
        self.pas = []
        self._montants = {}

    def relever(self, e):
        if type(e) is ClotureDePhase:
            for ligne, termes in e.montants:
                if ligne in LIGNES_RELEVEES:
                    self._montants[ligne] = sum(x for _, x in termes)
                    for nom, x in termes:
                        self._montants[f"{ligne}:{nom}"] = x
        elif type(e) is FinDePas:
            self.pas.append({**self._montants, "t": e.t, "variables": dict(e.variables_du_pas),
                             "etat": e.etat})
            self._montants = {}


def ecart(x, reference):
    """|x/x̄ − 1| ; pour une valeur de référence nulle, |x|."""
    return abs(x) if reference == 0.0 else abs(x / reference - 1.0)


def positions(etat):
    return {nom: getattr(etat, nom) for nom in cat.NOMS_POSTES}


def echelle(etat, secteur):
    """S du secteur à l'ouverture (`eq:noyau-echelle-bilan`)."""
    return idt.echelle_bilan(positions(etat), secteur)


def reels():
    return (Production(), Travail(), Prix(), Banque(), BanqueCentrale())


def derouler(socle, sentier, nb_pas, initial=None, blocs_reels=None, **options):
    releve = Releve()
    initial = socle.etat_initial(sentier) if initial is None else initial
    o = socle.ordonnanceur(sentier, reels=reels() if blocs_reels is None else blocs_reels,
                           **options)
    socle.derouler(initial, nb_pas, o, releve)
    return initial, releve


@pytest.fixture(scope="module")
def trajectoires(socle):
    """Une trajectoire de 720 pas par π*, depuis l'état résolu, sans choc, blocs 2, 3, 4, 7 et 8
    réels."""
    return {pi: (socle.sentier(pi),) + derouler(socle, socle.sentier(pi), NB_PAS)
            for pi in socle.POINTS_PI}


# --------------------------------------------------------------------------
# État stationnaire (P77), superneutralité des écarts
# --------------------------------------------------------------------------


def _un_pas(sentier, initial, releve):
    """Grandeurs du bloc après un pas depuis l'état résolu, avec leur valeur du script."""
    s, par = sentier.s, sentier.par
    p, apres = releve.pas[0], releve.pas[0]["etat"]
    i_CB = p["variables"]["i_CB"]
    E_1 = idt.valeur_nette_stock(positions(apres), "banque")
    return {
        "i_L − i_CB = ϖ_L": (apres.i_L - i_CB, par.varpi_L),
        "i_CB − i_D = ϖ_D": (i_CB - apres.i_D, par.varpi_D),
        "i_L,1 (script)": (apres.i_L, s["i_L_1"]),
        "E^Bk_1/L_1 = ϑ": (E_1 / apres.L, par.vartheta),
        "L^CB_1 (script)": (apres.L_CB, s["L_CB_1"]),
        "B_Bk,1 (script)": (apres.B_Bk, s["B_Bk_1"]),
        "M_1 = D_H + D_F (script)": (apres.D_H + apres.D_F, s["D_H_1"] + s["D_F_1"]),
        "ligne 9 (script)": (p["9"], s["l9"]),
        "ligne 10 (script)": (p["10"], s["l10_H"] + s["l10_F"]),
        "Π^Bk (script)": (p["variables"]["Pi_Bk"], s["Pi_Bk"]),
        "ligne 15 (script)": (p["15"], s["Div_Bk"]),
        "Div/Π (script)": (p["15"] / p["variables"]["Pi_Bk"], s["Div_Bk"] / s["Pi_Bk"]),
    }


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_un_pas_depuis_l_etat_resolu_egal_au_script(trajectoires, pi, publier):
    """Fiche 7, § 9.6, « État stationnaire », sous P77 (n_a = 12, π* ∈ {0 ; 2 % ; 10 %}) : un pas
    sans choc depuis l'état résolu laisse i_L − i_CB = ϖ_L, i_CB − i_D = ϖ_D, E^Bk/L = ϑ, le
    refinancement, les titres de la banque, la masse monétaire, les lignes 9, 10 et 15, Π^Bk et
    Div/Π aux valeurs du script (`un_pas`), à 1e−10 relatif ; Res_1 L^CB_1 = 0 et Res_1 = 0
    exactement (B7 en −min)."""
    sentier, initial, releve = trajectoires[pi]
    apres = releve.pas[0]["etat"]
    assert apres.Res == 0.0 and apres.Res * apres.L_CB == 0.0
    ecarts = {nom: ecart(x, ref) for nom, (x, ref) in _un_pas(sentier, initial, releve).items()}
    for nom, x in ecarts.items():
        assert x <= SEUIL_UN_PAS, (nom, x)
    publier(f"Bloc 7, un pas depuis l'état résolu, π* = {100 * pi:g} % ({ETIQUETTES})", [
        " ; ".join(f"{n} {x:.1e}" for n, x in ecarts.items())
        + " (seuil 1e−10) ; Res_1 = 0 et Res_1 L^CB_1 = 0 exactement"])


def test_superneutralite_des_ecarts(trajectoires, publier):
    """Fiche 7, § 9.6, « Superneutralité des écarts » (critère 4 (c)), sous P77 : après un pas
    depuis l'état résolu, les écarts i_L − i_CB et i_CB − i_D et le rapport E^Bk/L sont égaux
    entre π* = 0, 2 % et 10 %, à 1e−10 (relatif aux écarts et à ϑ)."""
    valeurs = {}
    for pi, (sentier, initial, releve) in trajectoires.items():
        g = _un_pas(sentier, initial, releve)
        valeurs[pi] = {n: g[n][0] for n in ("i_L − i_CB = ϖ_L", "i_CB − i_D = ϖ_D",
                                            "E^Bk_1/L_1 = ϑ")}
    pires = {}
    for nom in valeurs[0.02]:
        xs = [v[nom] for v in valeurs.values()]
        pires[nom] = (max(xs) - min(xs)) / abs(valeurs[0.02][nom])
        assert pires[nom] <= SEUIL_UN_PAS, (nom, xs)
    publier(f"Bloc 7, superneutralité des écarts entre π* = 0, 2 et 10 % ({ETIQUETTES})", [
        " ; ".join(f"{n} : écart relatif {x:.1e}" for n, x in pires.items())
        + " (seuil 1e−10)"])


# --------------------------------------------------------------------------
# Réserves et refinancement, résultat et lignes exécutées, E^Bk, 720 pas
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_reserves_et_refinancement_a_chaque_cloture(trajectoires, pi, publier):
    """Fiche 7, § 9.6, « Réserves et refinancement », partie (b), sur 720 pas : à chaque clôture,
    Res ≥ 0, L^CB ≥ 0 et Res L^CB = 0 exactement (V4 de P87) ; identité B19 sans titres ni fonds
    propres à la banque centrale : Res = 0 et L^CB = M^G à 1e−12 × S^CB."""
    _, initial, releve = trajectoires[pi]
    pire = 0.0
    for p in releve.pas:
        e = p["etat"]
        assert e.Res >= 0.0 and e.L_CB >= 0.0 and e.Res * e.L_CB == 0.0, p["t"]
        S = echelle(e, "banque_centrale")
        pire = max(pire, abs(e.Res) / S, abs(e.L_CB - e.M_G) / S)
    assert pire <= SEUIL_CB
    publier(f"Bloc 7, réserves et refinancement, π* = {100 * pi:g} %, 720 pas ({ETIQUETTES})", [
        f"Res L^CB = 0 exactement à chaque clôture ; max(|Res|, |L^CB − M^G|)/S^CB = {pire:.1e} "
        "(seuil 1e−12)"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_resultat_egal_aux_lignes_executees(trajectoires, pi, publier):
    """Fiche 7, § 9.6, « Résultat et lignes exécutées », partie (b) (C41, part de la banque) : à
    chaque pas, Π^Bk écrit en phase 6 (B5) égale les lignes 9 + 11b + 12 − 10 − 13 exécutées, à
    1e−12 × S^Bk (S^Bk à l'ouverture du pas), sur 720 pas. La partie F3 relève du bloc 6."""
    _, initial, releve = trajectoires[pi]
    ouvertures = [initial] + [p["etat"] for p in releve.pas[:-1]]
    pire = 0.0
    for o, p in zip(ouvertures, releve.pas):
        lignes = p["9"] + p["11b"] + p["12"] - p["10"] - p["13"]
        pire = max(pire, abs(p["variables"]["Pi_Bk"] - lignes) / echelle(o, "banque"))
    assert pire <= SEUIL_BK
    publier(f"Bloc 7, résultat et lignes exécutées, π* = {100 * pi:g} %, 720 pas ({ETIQUETTES})",
            [f"max |Π^Bk − (9 + 11b + 12 − 10 − 13)|/S^Bk = {pire:.1e} (seuil 1e−12)"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_fonds_propres_du_bloc_egaux_a_la_valeur_nette_du_noyau(trajectoires, pi, publier):
    """ADR 0013, annotation du 14/11/2026, point 5 : E^Bk calculé par le bloc sur les six positions
    d'ouverture (`fonds_propres`) égale `valeur_nette_stock` de la banque à l'ouverture, à ε ×
    S^Bk, à chaque pas sur 720 pas (au bit : même ordre de sommation, publié)."""
    _, initial, releve = trajectoires[pi]
    ouvertures = [initial] + [p["etat"] for p in releve.pas]
    pire, au_bit = 0.0, 0
    for o in ouvertures:
        e_bloc = fonds_propres(o.L, o.B_Bk, o.Res, o.D_H, o.D_F, o.L_CB)
        e_noyau = idt.valeur_nette_stock(positions(o), "banque")
        pire = max(pire, abs(e_bloc - e_noyau) / echelle(o, "banque"))
        au_bit += e_bloc == e_noyau
    assert pire <= 1e-12
    publier(f"Bloc 7, E^Bk sur six positions et valeur nette du noyau, π* = {100 * pi:g} % "
            f"({ETIQUETTES})", [f"max |E^Bk − V^stock|/S^Bk = {pire:.1e} (seuil ε = 1e−12) ; "
                                f"égaux au bit à {au_bit} ouvertures sur {len(ouvertures)}"])


# --------------------------------------------------------------------------
# Câblage en phase hors du point fixe, au bit ; B7 dans ses trois cas
# --------------------------------------------------------------------------


def _hors_du_point_fixe(initial, part, decalage_i_L=0.01, decalage_i_D=-0.005):
    """État hors du sentier : la banque centrale détient x = `part` × L^CB_0 de titres pris à la
    banque, payés en réserves (B_CB = Res = x, B_Bk − x ; valeurs nettes inchangées) ; i_L et
    i_D décalés de leur valeur résolue, d'où i_L, i_D et i_CB distincts de leur sentier."""
    x = part * initial.L_CB
    return dataclasses.replace(initial, B_Bk=initial.B_Bk - x, B_CB=initial.B_CB + x,
                               Res=initial.Res + x, i_L=initial.i_L + decalage_i_L,
                               i_D=initial.i_D + decalage_i_D)


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
@pytest.mark.parametrize("part", [0.5, 2.0])
def test_cablage_des_phases_6_et_8c_hors_du_point_fixe(socle, pi, part):
    """Leçon de l'audit du rang 4 (M1) : les méthodes de phase passent à B1 à B7 les bonnes entrées.
    Depuis un état hors du point fixe (Res_0 = B_CB,0 > 0, i_L,0 et i_D,0 décalés), après un pas,
    au bit, contre les formes recalculées par le test sans appeler le bloc :
    ligne 9 = (i_L,0/12) L_0 (B3) ; ligne 10 = (i_D,0/12) D_H,0 et (i_D,0/12) D_F,0 (B4) ;
    Π^Bk = (i_L,0/12) L + (i/12) B_Bk + (i/12) Res − (i_D,0/12)(D_H + D_F) − (i/12) L^CB, i =
    i_CB du tour (B5) ; ligne 15 = max(0 ; E_0 + Π − ϑ(L_0 + ligne 18 exécutée)), E_0 =
    `valeur_nette_stock` (B6) ; i_L,1 = i_CB + ϖ_L, i_D,1 = i_CB − ϖ_D (B1, B2). B7 : pour
    `part` = 0,5, remboursement partiel (0 < Res^{8b} < L^CB_0), Res_1 = 0 exactement et L^CB_1
    = L^CB_0 + ligne 21 > 0 ; pour `part` = 2, remboursement total, ligne 21 = −L^CB_0 et
    L^CB_1 = 0 exactement, Res_1 > 0."""
    sentier = socle.sentier(pi)
    initial = _hors_du_point_fixe(socle.etat_initial(sentier), part)
    _, releve = derouler(socle, sentier, 1, initial=initial)
    p, o = releve.pas[0], initial
    v, apres = p["variables"], p["etat"]
    table = socle.PARAMETRES_DE_REFERENCE.banque
    i = v["i_CB"] / 12
    iL, iD = o.i_L / 12, o.i_D / 12
    assert len({o.i_L, o.i_D, v["i_CB"]}) == 3 and o.Res > 0.0 and o.B_Bk != o.Res
    assert p["9:iL_L"].hex() == (iL * o.L).hex()
    assert p["10:iD_DH"].hex() == (iD * o.D_H).hex()
    assert p["10:iD_DF"].hex() == (iD * o.D_F).hex()
    pi_bk = iL * o.L + i * o.B_Bk + i * o.Res - iD * (o.D_H + o.D_F) - i * o.L_CB
    assert v["Pi_Bk"].hex() == pi_bk.hex()
    E_0 = idt.valeur_nette_stock(positions(o), "banque")
    div = max(0.0, E_0 + pi_bk - table.vartheta * (o.L + p["18"]))
    assert div > 0.0 and p["15"].hex() == div.hex()
    assert apres.i_L.hex() == (v["i_CB"] + table.varpi_L.valeur).hex()
    assert apres.i_D.hex() == (v["i_CB"] - table.varpi_D.valeur).hex()
    if part < 1.0:
        assert -o.L_CB < p["21"] < 0.0
        assert apres.Res == 0.0 and apres.L_CB == o.L_CB + p["21"] and apres.L_CB > 0.0
    else:
        assert p["21"] == -o.L_CB and apres.L_CB == 0.0 and apres.Res > 0.0


def _sans_plan_de_consommation_au_premier_pas(nom, t):
    return 0.0 if (nom, t) == ("C_plan", 0) else 1.0


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_contrat_de_poussiere_dans_le_moteur(socle, pi):
    """Critère 4 du 07/10/2026 (part du bloc 7 de #103), dans le moteur : depuis un état où les
    dépôts des ménages ont été échangés contre des titres (B_H = D_H,0 ; la banque perd ce passif,
    valeurs nettes recalculées, V^flux = V^stock) et où il reste D_H = −1e−11, poussière admise
    par la lecture nette du noyau (D_H + ε S^ménages ≥ 0), plan de consommation nul au premier
    pas (sinon les ménages ne paieraient pas la ligne 1) : la phase 6 lit D_H en max(0 ; ·), d'où
    terme de la ligne 10 des ménages nul exactement et Π^Bk sans ce terme ; E^Bk, identité de
    bilan, porte la position telle quelle ; au bit, contre les formes recalculées par le test."""
    sentier = socle.sentier(pi)
    e0 = socle.etat_initial(sentier)
    pos = positions(e0)
    pos["B_H"], pos["D_H"] = e0.B_H + e0.D_H, -1e-11
    v_flux = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(pos, s) for s in cat.SECTEURS}
    o = dataclasses.replace(e0, **pos, **v_flux)
    assert o.D_H + 1e-12 * idt.echelle_bilan(pos, "menages") >= 0.0
    _, releve = derouler(socle, sentier, 1, initial=o,
                         chocs_des_plans=_sans_plan_de_consommation_au_premier_pas)
    p = releve.pas[0]
    v, table = p["variables"], socle.PARAMETRES_DE_REFERENCE.banque
    i, iL, iD = v["i_CB"] / 12, o.i_L / 12, o.i_D / 12
    assert p["10:iD_DH"] == 0.0 and p["10:iD_DF"].hex() == (iD * o.D_F).hex()
    pi_bk = iL * o.L + i * o.B_Bk + i * o.Res - iD * (0.0 + o.D_F) - i * o.L_CB
    assert v["Pi_Bk"].hex() == pi_bk.hex()
    E_0 = idt.valeur_nette_stock(positions(o), "banque")
    assert E_0 != idt.valeur_nette_stock({**positions(o), "D_H": 0.0}, "banque")
    assert p["15"].hex() == max(0.0, E_0 + pi_bk - table.vartheta * (o.L + p["18"])).hex()


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_plancher_du_dividende_actif_dans_le_moteur(socle, pi):
    """B6, plancher de domaine, dans le moteur (m2 de l'audit, reprise du rang 5) : depuis un état
    où la banque a cédé aux ménages des titres pour la moitié de ses fonds propres (B_Bk − E/2,
    B_H + E/2 ; valeurs nettes recalculées, V^flux = V^stock), E^Bk_0 + Π^Bk − ϑ L_1 < 0 : la
    ligne 15 exécutée vaut 0 exactement (sans le plancher, elle serait négative, ce que la ligne
    15 n'admet pas) et E^Bk_1 = E^Bk_0 + Π^Bk par le stock, à ε × S^Bk."""
    sentier = socle.sentier(pi)
    e0 = socle.etat_initial(sentier)
    pos = positions(e0)
    cession = 0.5 * idt.valeur_nette_stock(pos, "banque")
    pos["B_Bk"], pos["B_H"] = e0.B_Bk - cession, e0.B_H + cession
    v_flux = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(pos, s) for s in cat.SECTEURS}
    o = dataclasses.replace(e0, **pos, **v_flux)
    _, releve = derouler(socle, sentier, 1, initial=o)
    p = releve.pas[0]
    table = socle.PARAMETRES_DE_REFERENCE.banque
    E_0 = idt.valeur_nette_stock(positions(o), "banque")
    assert E_0 + p["variables"]["Pi_Bk"] - table.vartheta * (o.L + p["18"]) < 0.0
    assert p["15"] == 0.0
    E_1 = idt.valeur_nette_stock(positions(p["etat"]), "banque")
    assert abs(E_1 - (E_0 + p["variables"]["Pi_Bk"])) <= 1e-12 * echelle(o, "banque")


@pytest.mark.parametrize("scenario", ["taux nul", "taux + 5 points"])
def test_bornes_plancher_inactif_publie(socle, scenario, publier):
    """Réserve R3 de `monnaie` (fiche 7, § 9.6, « Bornes », partie (a)) : en équilibre partiel
    (encours de la banque du script à π* = 2 %, n_a = 12, × Γ̄ par pas ; crédit exécuté L (Γ̄ −
    1) ; i_L, i_D par B1 et B2 au tour suivant ; E^Bk_{t+1} = E^Bk_t + Π − Div), taux directeur à
    0, ou relevé de 5 points, aux tours 1 à 12, fenêtre de 48 pas : le plancher de B6 reste
    inactif à chaque pas (Div_Bk > 0) ; Div/Π au plus bas sur la fenêtre est publié. Appel direct
    des fonctions du bloc, sans le moteur ; publié ici, où vit la fixture `publier`."""
    from nations.blocs import banque as bloc
    es = socle.script()
    par = dataclasses.replace(es.Parametres(), pi_cible=0.02, n_a=12, nu_G=1.15)
    e = es.etat_stationnaire(par)
    o, gam, i0 = es.ouverture(e, par), e["Gam"], e["i_CB"]
    choc = 0.0 if scenario == "taux nul" else i0 + 0.05
    i_L, i_D, E = o["i_L"], o["i_D"], o["E_Bk"]
    rapports = []
    for t in range(48):
        f = gam ** t
        enc = {k: o[k] * f for k in ("L", "B_Bk", "Res", "L_CB", "D_H", "D_F")}
        i = choc if 1 <= t <= 12 else i0
        Pi = bloc.resultat(i_L / 12, enc["L"], i / 12, enc["B_Bk"], i / 12, enc["Res"], i_D / 12,
                           enc["D_H"], enc["D_F"], i / 12, enc["L_CB"])
        Div = bloc.dividendes(E, Pi, par.vartheta, enc["L"], enc["L"] * (gam - 1.0))
        assert Div > 0.0, (scenario, t)
        rapports.append((Div / Pi, t))
        E = E + Pi - Div
        i_L = bloc.taux_des_credits_suivant(i, par.varpi_L)
        i_D = bloc.taux_des_depots_suivant(i, par.varpi_D)
    bas, t_bas = min(rapports)
    publier(f"Bloc 7, bornes, {scenario} aux tours 1 à 12, équilibre partiel, π* = 2 %", [
        f"plancher de B6 inactif sur les 48 pas (Div_Bk > 0 à chaque pas) ; Div/Π au plus bas "
        f"{bas:.4f} au pas {t_bas} (fenêtre : pas 0 à 47)"])


def _rendements_en_equilibre_partiel(es, par, e, i_cb):
    """Rendement des fonds propres de la banque n_a Π^Bk_t/E^Bk_t (% par an, E^Bk d'ouverture
    du tour), pas 0 à 12, en équilibre partiel (forme de `test_bornes_plancher_inactif_publie`) :
    encours de la banque du script × Γ̄ par pas, crédit exécuté L (Γ̄ − 1), taux directeur
    `i_cb(t)`, i_L et i_D par B1 et B2 au tour suivant, E^Bk_{t+1} = E^Bk_t + Π − Div. Appel
    direct des fonctions du bloc 7."""
    from nations.blocs import banque as bloc
    o, gam = es.ouverture(e, par), e["Gam"]
    i_L, i_D, E = o["i_L"], o["i_D"], o["E_Bk"]
    rendements = []
    for t in range(13):
        f = gam ** t
        enc = {k: o[k] * f for k in ("L", "B_Bk", "Res", "L_CB", "D_H", "D_F")}
        i = i_cb(t)
        Pi = bloc.resultat(par_pas(TauxDeFlux(i_L)), enc["L"], par_pas(TauxDeFlux(i)),
                           enc["B_Bk"], par_pas(TauxDeFlux(i)), enc["Res"],
                           par_pas(TauxDeFlux(i_D)), enc["D_H"], enc["D_F"],
                           par_pas(TauxDeFlux(i)), enc["L_CB"])
        Div = bloc.dividendes(E, Pi, par.vartheta, enc["L"], enc["L"] * (gam - 1.0))
        rendements.append(100.0 * N_A * Pi / E)
        E = E + Pi - Div
        i_L = bloc.taux_des_credits_suivant(i, par.varpi_L)
        i_D = bloc.taux_des_depots_suivant(i, par.varpi_D)
    return rendements


def test_d2_rendement_des_fonds_propres_sur_12_tours_publie(socle, publier):
    """(d2) de `jeu` (fiche 7, § 7 et § 9.6, critère 13 (d) ; classe (a), appel direct) : taux
    directeur relevé d'un point aux tours 1 à 12 depuis l'état résolu à π* = 2 % (n_a = 12), en
    équilibre partiel, contre un contrôle apparié au taux inchangé. Rendement des fonds propres
    sur 12 tours, définition de `tab:banque-restitution` : moyenne sur les tours 1 à 12 de
    n_a Π^Bk_t/E^Bk_t, % par an, E^Bk d'ouverture ; publié en points (écart au contrôle), avec
    son écart au tour 12 et la valeur du script (`valeurs(...)["d2"]`). La fiche ne fixe aucun
    seuil à (d2) (« restitué en points, et son écart au tour 12 est publié ») : mesure publiée
    sans verdict. Publié ici, où vit la fixture `publier`."""
    es = socle.script()
    par = dataclasses.replace(es.Parametres(), pi_cible=0.02, n_a=12, nu_G=1.15)
    e = es.etat_stationnaire(par)
    i0 = e["i_CB"]
    choc = _rendements_en_equilibre_partiel(es, par, e,
                                            lambda t: i0 + 0.01 if 1 <= t <= 12 else i0)
    controle = _rendements_en_equilibre_partiel(es, par, e, lambda t: i0)
    ecarts = [c - k for c, k in zip(choc, controle, strict=True)]
    d2 = sum(ecarts[1:13]) / 12
    script = es.valeurs(e, par)["d2"]
    assert math.isfinite(d2) and math.isfinite(ecarts[12])
    publier("Bloc 7, (d2), i_CB + 1 point aux tours 1 à 12, équilibre partiel, π* = 2 %", [
        f"rendement des fonds propres sur 12 tours (moyenne des tours 1 à 12 de n_a Π^Bk/E^Bk, "
        f"% par an, E^Bk d'ouverture), écart au contrôle : {d2:+.4f} point ; écart au tour 12 : "
        f"{ecarts[12]:+.4f} point ; tour 1 : {ecarts[1]:+.4f} point (C29) ; script : "
        f"{script:+.4f} point ; mesure sans seuil (fiche 7, § 9.6)"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_b7_decouvert_couvert_sur_le_sentier(trajectoires, pi):
    """B7, premier cas, dans le moteur : sur le sentier, la position après 8 (b) est négative (le
    refinancement croît comme les paiements) ; la ligne 21 la couvre exactement : ligne 21 > 0,
    Res_1 = 0 et L^CB_1 = L^CB_0 + ligne 21, exactement, à chaque pas sur 720 pas."""
    _, initial, releve = trajectoires[pi]
    ouvertures = [initial] + [p["etat"] for p in releve.pas[:-1]]
    for o, p in zip(ouvertures, releve.pas):
        assert p["21"] > 0.0 and p["etat"].Res == 0.0
        assert p["etat"].L_CB == o.L_CB + p["21"]


# --------------------------------------------------------------------------
# Écart au bloc d'essai 7, sur 720 pas (substitution dans le socle partiel)
# --------------------------------------------------------------------------

GRANDEURS_COMPAREES = (("L_CB", "banque"), ("Res", "banque"), ("B_Bk", "banque"),
                       ("D_H", "banque"), ("D_F", "banque"), ("M_G", "etat"),
                       ("V_flux_banque", "banque"), ("V_flux_menages", "menages"),
                       ("V_flux_entreprises", "entreprises"), ("i_L", None), ("i_D", None))


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_ecart_au_bloc_d_essai_sur_720_pas(trajectoires, socle, pi, publier):
    """Le bloc 7 réel remplace le bloc d'essai 7 dans le socle partiel (blocs 2, 3, 4 et 8 réels) :
    sur 720 pas sans choc depuis l'état résolu, aucun arrêt du noyau, et l'écart au bloc d'essai
    (lignes 9, 10, 15 au sentier, B7 en −min, i_L et i_D au sentier) reste sous le seuil de P94,
    1e−9 × S du secteur pour les positions et les V^flux, 1e−9 relatif à ϖ pour i_L et i_D ;
    écarts publiés. Le bloc d'essai ne lit pas l'état réel : l'écart mesure la dérive d'arrondi
    du socle hors du sentier exact du script, non une erreur du bloc."""
    sentier, initial, releve = trajectoires[pi]
    _, essai = derouler(socle, sentier, NB_PAS,
                        blocs_reels=(Production(), Travail(), Prix(), BanqueCentrale()))
    table = socle.PARAMETRES_DE_REFERENCE.banque
    pires = {}
    for p, q in zip(releve.pas, essai.pas):
        a, b = p["etat"], q["etat"]
        for nom, secteur in GRANDEURS_COMPAREES:
            ref = echelle(b, secteur) if secteur else table.varpi_D.valeur
            pires[nom] = max(pires.get(nom, 0.0), abs(getattr(a, nom) - getattr(b, nom)) / ref)
    assert len(releve.pas) == len(essai.pas) == NB_PAS
    for nom, x in pires.items():
        assert x <= SEUIL_ECART_AU_BLOC_D_ESSAI, (nom, x)
    publier(f"Bloc 7 réel contre bloc d'essai 7, π* = {100 * pi:g} %, 720 pas ({ETIQUETTES})", [
        " ; ".join(f"{n} {x:.1e}" for n, x in pires.items())
        + " (max sur 720 pas de |réel − essai|/S du secteur, ou /ϖ_D pour i_L, i_D ; seuil "
          "1e−9)"])


# --------------------------------------------------------------------------
# Phases : lecture hors ordre refusée à l'assemblage (partie (b))
# --------------------------------------------------------------------------


def _fautif(etape, lecture):
    """Bloc 7 réel dont le siège de `etape` déclare en plus `lecture`."""
    sieges = tuple(dataclasses.replace(s, lit=s.lit + (lecture,)) if s.etape == etape else s
                   for s in Banque.declaration.sieges)
    declaration = dataclasses.replace(Banque.declaration, sieges=sieges)
    return type("BanqueFautive", (Banque,), {"__slots__": (), "declaration": declaration})()


@pytest.mark.parametrize("etape, lecture, motif", [
    ("6", Lecture(GRAND_LIVRE, "13"), "lu avant la clôture"),
    ("6", Lecture(GRAND_LIVRE, "19a-banque"), "lu avant la clôture"),
    ("6", Lecture(GRAND_LIVRE, "21"), "lu avant la clôture"),
    ("8c", Lecture(GRAND_LIVRE, "21"), "lu avant la clôture"),
])
def test_phases_lecture_hors_ordre_refusee(socle, etape, lecture, motif):
    """Fiche 7, § 9.6, « Phases », partie (b) : en phase 6, les lignes 13 (8 (a)), 19a-banque (7) et
    21 (8 (c)) ne sont pas lisibles ; en 8 (c), la ligne 21 que le bloc propose non plus ; une
    lecture déclarée hors ordre est refusée à l'assemblage (`DefautDeDeclaration`)."""
    sentier = socle.sentier(0.02)
    blocs = socle.blocs(sentier, reels=(Production(), Travail(), Prix(), BanqueCentrale(),
                                        _fautif(etape, lecture)))
    with pytest.raises(DefautDeDeclaration, match=motif):
        ordo.assembler(socle.PHASES, blocs, socle.parametres_du_sentier(sentier),
                       socle.SANS_ENTREES)


def test_conversion_des_taux_au_pas_par_la_seule_conversion_lineaire():
    """Les taux d'intérêt de B3 à B5 sont convertis au pas par `par_pas` (x/n_a), seule conversion
    linéaire (`eq:moteur-conversion-taux`) : la forme du test, x/12, lui est égale au bit."""
    for x in (0.0502, -0.01, 0.111, 0.0302):
        assert par_pas(TauxDeFlux(x)).hex() == (x / 12).hex()
