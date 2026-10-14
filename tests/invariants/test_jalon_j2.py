"""Invariants et mesures du jalon J2 sur le générateur de flux (issue #98).

Contrat : critères de passage de J2 (M19 ; ADR 0005, point 19, annoté le
07/10/2026) ; ADR 0012, Conséquences (« Pour #98 ») et annotations ; critères
complémentaires du rang 1b validés le 07/10/2026 (commentaires de #98 :
définitions de A et de C, critères 1 à 12 du générateur, complément du point
8). Chaque test énonce une **propriété** (seuil, signe, égalité bit à bit,
couverture), jamais une valeur à reproduire ; les seuils sont ceux de l'ADR
0005, point 19, inchangés : toute violation est un défaut, jamais un motif
d'élargir ε ou ε_V.

Les trajectoires de 720 pas sur `GRAINES` sont déroulées une fois par module
(`trajectoires`) : un `Compteur` (observateur d'essai) et des espions du grand
livre, en lecture seule (ouverture, positions à chaque clôture, montant
proposé et montant couvert de la ligne 16), en tirent, graine par graine, les
décomptes de couverture et les résidus de l'oracle des portes ; aucun n'a
d'effet sur la trajectoire (test de suppression de #96).
"""

import collections
import dataclasses
import math
import statistics
import struct
from pathlib import Path

import pytest

from nations.etat.sauvegarde import charger, sauvegarder
from nations.moteur import ordonnanceur as ordo
from nations.moteur import registre
from nations.moteur.contrat_bloc import GRAND_LIVRE, OUVERTURE, Lecture
from nations.moteur.conversions import par_pas
from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres import TauxDeFlux
from nations.moteur.parametres.cadre import CADRE, PAS_PAR_AN
from nations.moteur.phases import PHASES, Phase
from nations.noyau import catalogue as cat
from nations.noyau import grand_livre as gl_module
from nations.noyau import identites as idt
from nations.noyau.diagnostics import DefautComptable
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas, ObservateurNul
from nations.observation.residus import ReleveDesResidus

# Fenêtre et graines (critère C98-1 : 720 pas, au moins 20 graines).
NB_PAS = 720
GRAINES = tuple(range(20261007, 20261007 + 20))
EPS = CADRE.tolerance_identite_pas
EPS_V = CADRE.tolerance_identite_cumulee
SPECIFICATION = Path(__file__).resolve().parents[2] / "docs/specification/nations_et_marches.tex"

LIGNES_DECIDEES = tuple(ligne.identifiant for ligne in cat.LIGNES if not ligne.contrepartie)
LIGNES_A_DEUX_SIGNES = tuple(ligne.identifiant for ligne in cat.LIGNES
                             if ligne.admet_negatif and not ligne.contrepartie)
CONTREPARTIES = tuple(ligne.identifiant for ligne in cat.CONTREPARTIES)
SECTEURS_DE_COLONNE = cat.SECTEUR_DE_COLONNE


def bits(x):
    return struct.pack("<d", x).hex()


def echelles(positions):
    return {s: idt.echelle_bilan(positions, s) for s in cat.SECTEURS}


def positions_de(etat):
    return {nom: getattr(etat, nom) for nom in cat.NOMS_POSTES}


# --------------------------------------------------------------------------
# Compteur : décomptes d'une graine, sans effet sur la trajectoire
# --------------------------------------------------------------------------


class Compteur:
    """Observateur d'essai : relevé des résidus et décomptes de couverture d'une graine.

    Il reçoit les clôtures et les fins de pas (moteur), les positions à
    chaque clôture et les propositions de la ligne 16 (espions du grand
    livre). Il ne garde que des compteurs et des extrêmes.
    """

    def __init__(self, portes):
        self.releve = ReleveDesResidus()
        self.portes = portes
        self.non_nulles = collections.Counter()
        self.negatives = collections.Counter()
        self.positives = collections.Counter()
        self.decouvert = collections.Counter()
        self.cas_b7 = collections.Counter()
        self.cas_16 = collections.Counter()
        self.u_exact = True
        # Ligne 16 négative : M^G de clôture de 8 (b) hors de sa forme exacte, et pas
        # où M^{G,8a} était déjà en poussière négative (phase 7 : plusieurs lignes).
        self.m_g_8b_hors_forme = 0
        self.m_g_8a_poussiere = 0
        # Pire |M^{G,8a}| / S_État des cas de poussière, et poussière hors du domaine
        # −ε × S_État (oracle indépendant du contrôle de caisse du noyau).
        self.pire_poussiere_8a = 0.0
        self.poussiere_hors_domaine = 0
        self.m_g_6_poussiere = 0
        self.brut_au_dela = 0
        self.r_max = dict.fromkeys(cat.SECTEURS, 0.0)
        self.porte_phase = 0.0
        self.porte_pas = 0.0
        self.montants_non_generiques = 0
        self.montants = 0
        self.pas_clos = []
        self._executes = {}
        self._positions_courantes = None
        self._avant = None
        self._ouverture = None
        self._s = None
        self._pi = None
        self._couvert = None
        self._phase_positions = {}

    # Espions du grand livre
    def ouverture(self, livre):
        self._ouverture = {p: livre.ouverture(p) for p in cat.NOMS_POSTES}
        self._avant = dict(self._ouverture)
        self._s = {s: livre.echelle(s) for s in cat.SECTEURS}
        self._executes = collections.defaultdict(float)
        self._pi = None
        self._couvert = None
        self._phase_positions = {}

    def proposition(self, flux):
        if flux.ligne == "16":
            self._pi = flux.montants["Pi_CB"]

    def montant_couvert(self, montant):
        self._couvert = montant

    def apres_cloture(self, phase, livre):
        positions = {p: livre.position(p) for p in cat.NOMS_POSTES}
        self._phase_positions[phase] = positions
        self._positions_courantes = positions

    # Observateur du moteur
    def relever(self, evenement):
        self.releve.relever(evenement)
        if type(evenement) is ClotureDePhase:
            self._cloture(evenement)
        elif type(evenement) is FinDePas:
            self._fin_de_pas(evenement)

    def _cloture(self, c):
        apres = self._positions_courantes
        avant = self._avant
        # Oracle des portes par phase : signes lus dans tab:portes-monnaie.
        d_m = d_h = 0.0
        operandes = dict.fromkeys(cat.SECTEURS, 0.0)
        for ligne, termes in c.montants:
            montant = 0.0
            for _, x in termes:
                montant += x
                self.montants += 1
                if x != 0.0 and _bits_significatifs(x) < 24:
                    self.montants_non_generiques += 1
            self._executes[ligne] += montant
            signe_m, signe_h = self.portes[ligne]
            if signe_m is not None:
                d_m += signe_m * montant
                d_h += signe_h * montant
            for terme in cat.LIGNE[ligne].termes:
                x = abs(dict(termes)[terme.nom])
                operandes[SECTEURS_DE_COLONNE[terme.colonne_plus]] += x
                operandes[SECTEURS_DE_COLONNE[terme.colonne_moins]] += x
        s_min = min(self._s.values())
        if c.montants:
            r_m = d_m - ((apres["D_H"] - avant["D_H"]) + (apres["D_F"] - avant["D_F"]))
            r_h = d_h - (apres["Res"] - avant["Res"])
            self.porte_phase = max(self.porte_phase, abs(r_m) / s_min, abs(r_h) / s_min)
        for s in cat.SECTEURS:
            self.r_max[s] = max(self.r_max[s], operandes[s] / self._s[s])
        if c.phase in ("6", "7", "8a") and apres["Res"] < 0.0:
            self.decouvert[c.phase] += 1
        if c.phase == "6":
            if apres["M_G"] < 0.0:
                self.m_g_6_poussiere += 1
            executes = dict(c.montants)
            brut = dict(executes["6"])["Tr"]
            for ligne in ("11a", "11b", "11c"):
                brut += max(0.0, sum(v for _, v in executes[ligne]))
            brut += max(0.0, -dict(executes["7"])["T_H"]) + max(0.0, -dict(executes["7"])["T_F"])
            if brut > max(0.0, avant["M_G"]):
                self.brut_au_dela += 1
        if c.phase == "8b":
            res, l_cb = apres["Res"], apres["L_CB"]
            self.cas_b7["Res < 0" if res < 0.0 else "0 ≤ Res ≤ L^CB" if res <= l_cb
                        else "Res > L^CB"] += 1
            if self._pi is not None and self._pi < 0.0:
                perte = -self._pi
                execute = self._executes["16"]
                c_ = self._couvert
                u = perte - c_
                self.u_exact &= (execute - self._pi == u) and (execute == -c_)
                # Forme exacte (ADR 0012, A3.2 ; lecture validée le 14/10/2026) : si
                # M^{G,8a} ≥ 0, M^G après 8 (b) = fl(M^{G,8a} − c) ≥ 0, nul quand la perte
                # sature ; sinon M^{G,8a} est une poussière admise (≥ −ε × S_État), c = 0
                # et M^G passe telle quelle. Les cas de poussière sont classés à part.
                avant_8b = self._phase_positions["8a"]["M_G"]
                if avant_8b >= 0.0:
                    exacte = apres["M_G"] >= 0.0 and (c_ != avant_8b or apres["M_G"] == 0.0)
                    self.cas_16["u = 0" if u == 0.0 else "u = |Π|" if c_ == 0.0
                                else "0 < u < |Π|"] += 1
                else:
                    self.m_g_8a_poussiere += 1
                    s_g = self._s["etat"]
                    self.poussiere_hors_domaine += not avant_8b >= -EPS * s_g
                    self.pire_poussiere_8a = max(self.pire_poussiere_8a, -avant_8b / s_g)
                    exacte = c_ == 0.0 and apres["M_G"] == avant_8b
                    self.cas_16["poussière (c = 0)"] += 1
                self.m_g_8b_hors_forme += not exacte
        self._avant = apres

    def _fin_de_pas(self, fin):
        self.pas_clos.append(fin.t)
        for ligne in cat.IDENTIFIANTS:
            m = self._executes[ligne]
            if m != 0.0:
                self.non_nulles[ligne] += 1
            if m < 0.0:
                self.negatives[ligne] += 1
            if m > 0.0:
                self.positives[ligne] += 1
        # Portes du pas : depuis l'ouverture, toutes les lignes du pas.
        d_m = d_h = 0.0
        for ligne, montant in self._executes.items():
            signe_m, signe_h = self.portes[ligne]
            if signe_m is not None:
                d_m += signe_m * montant
                d_h += signe_h * montant
        e = fin.etat
        o = self._ouverture
        r_m = d_m - ((e.D_H - o["D_H"]) + (e.D_F - o["D_F"]))
        r_h = d_h - (e.Res - o["Res"])
        s_min = min(self._s.values())
        self.porte_pas = max(self.porte_pas, abs(r_m) / s_min, abs(r_h) / s_min)


def _bits_significatifs(x):
    """Nombre de bits significatifs de la mantisse d'un flottant normal non nul."""
    mantisse = struct.unpack("<Q", struct.pack("<d", x))[0] & ((1 << 52) - 1)
    if mantisse == 0:
        return 1
    return 53 - ((mantisse & -mantisse).bit_length() - 1)


def lire_portes(matrices):
    """Signes (ΔM, ΔH) par ligne, lus dans tab:portes-monnaie (None, None : ligne « poste »)."""
    texte = SPECIFICATION.read_text(encoding="utf-8")
    table, ecarts = matrices.lire_table(texte, matrices.LABEL_PORTES, str(SPECIFICATION))
    assert table is not None and ecarts == []
    portes = {}
    for ligne in table.lignes:
        _, signe_m, signe_h = ligne.cellules
        sm, erreur_m = matrices.lire_signe(signe_m.texte)
        sh, erreur_h = matrices.lire_signe(signe_h.texte)
        assert erreur_m is None and erreur_h is None
        portes[ligne.identifiant] = (sm, sh)
    return portes


def espionner(monkeypatch, compteur):
    """Espions du grand livre, en lecture seule : ouverture, propositions, clôtures."""
    ouvrir, proposer = gl_module.ouvrir_pas, gl_module.GrandLivre.proposer
    declarer, clore = (gl_module.GrandLivre.declarer_montant_couvert,
                       gl_module.GrandLivre.clore_phase)

    def ouvrir_espion(etat, parametres):
        livre = ouvrir(etat, parametres)
        compteur.ouverture(livre)
        return livre

    def proposer_espion(self, flux):
        proposer(self, flux)
        compteur.proposition(flux)

    def declarer_espion(self, ligne, montant, payeur):
        declarer(self, ligne, montant, payeur)
        compteur.montant_couvert(montant)

    def clore_espion(self, phase):
        cloture = clore(self, phase)
        compteur.apres_cloture(phase, self)
        return cloture

    monkeypatch.setattr(ordo, "ouvrir_pas", ouvrir_espion)
    monkeypatch.setattr(gl_module.GrandLivre, "proposer", proposer_espion)
    monkeypatch.setattr(gl_module.GrandLivre, "declarer_montant_couvert", declarer_espion)
    monkeypatch.setattr(gl_module.GrandLivre, "clore_phase", clore_espion)


@dataclasses.dataclass
class Bilan:
    """Ce qu'on garde d'une graine : le compteur, les états initial et final, et des décomptes
    et extrêmes tirés des états t + 1."""

    compteur: Compteur
    etat_initial: object
    etat_final: object
    regimes: collections.Counter
    transitions: collections.Counter
    produit_res_lcb_nul: bool
    reserves_positives: bool
    e_cb_signes: collections.Counter
    prix_signes: collections.Counter
    bandes: dict


def derouler_graine(generateur, portes, graine):
    """Une trajectoire de NB_PAS pas, observée par un Compteur et les espions du grand livre."""
    compteur = Compteur(portes)
    regimes, transitions = collections.Counter(), collections.Counter()
    e_cb, prix = collections.Counter(), collections.Counter()
    bandes = {cle: [math.inf, -math.inf] for cle in generateur.BANDES}
    produit_nul = reserves_positives = True
    with pytest.MonkeyPatch.context() as mp:
        generateur.doubler_19b(mp)
        espionner(mp, compteur)
        o = generateur.ordonnanceur()
        etat = initial = generateur.etat_initial(graine)
        regime_precedent = None
        for _ in range(NB_PAS):
            suivant = generateur.derouler(etat, 1, o, compteur)
            regime = ("Res > 0, L^CB = 0" if suivant.Res > 0.0 and suivant.L_CB == 0.0
                      else "Res = 0, L^CB > 0" if suivant.Res == 0.0 and suivant.L_CB > 0.0
                      else "Res = 0, L^CB = 0")
            regimes[regime] += 1
            if regime_precedent is not None and regime != regime_precedent:
                transitions[(regime_precedent, regime)] += 1
            regime_precedent = regime
            produit_nul &= suivant.Res * suivant.L_CB == 0.0
            reserves_positives &= suivant.Res >= 0.0
            v = idt.valeur_nette_stock(positions_de(suivant), "banque_centrale")
            e_cb["négatif" if v < 0.0 else "positif"] += 1
            variation = suivant.registre_prix[0] - etat.registre_prix[0]
            prix["baisse" if variation < 0.0 else "hausse"] += 1
            s = echelles(positions_de(suivant))
            for (poste, secteur), extremes in bandes.items():
                rapport = getattr(suivant, poste) / s[secteur]
                extremes[0] = min(extremes[0], rapport)
                extremes[1] = max(extremes[1], rapport)
            etat = suivant
    return Bilan(compteur, initial, etat, regimes, transitions, produit_nul, reserves_positives,
                 e_cb, prix, bandes)


@pytest.fixture(scope="module")
def portes(matrices):
    return lire_portes(matrices)


@pytest.fixture(scope="module")
def trajectoires(generateur, portes):
    """Les trajectoires de NB_PAS pas, une par graine de GRAINES."""
    return {graine: derouler_graine(generateur, portes, graine) for graine in GRAINES}


def fraction(n):
    return n / NB_PAS


# --------------------------------------------------------------------------
# Fenêtre, identités, accumulation (C98-1)
# --------------------------------------------------------------------------


def test_fenetre_publiee_de_720_pas_clos(trajectoires):
    """La fenêtre des mesures est exactement 720 pas clos, t = 0 à 719, sur chaque graine."""
    assert len(trajectoires) >= 20
    for bilan in trajectoires.values():
        assert bilan.compteur.releve.pas() == tuple(range(NB_PAS))
        assert bilan.compteur.pas_clos == list(range(NB_PAS))
        assert bilan.etat_final.t == NB_PAS
        assert all(len(bilan.compteur.releve.accumulation(s)) == NB_PAS for s in cat.SECTEURS)


REGLES_PAR_PAS = ("eq:noyau-somme-ligne", "eq:noyau-somme-colonne", "eq:noyau-cloture-poste",
                  "eq:noyau-variation-monnaie", "eq:noyau-variation-monnaie-centrale")


def test_identites_par_pas_et_cumulee_sur_720_pas(trajectoires, publier):
    """Identités par pas ≤ ε × S et identité cumulée ≤ ε_V × S, à chaque clôture, 720 pas."""
    lignes = []
    for regle in REGLES_PAR_PAS:
        pire = max(b.compteur.releve.maximum(regle)[0] for b in trajectoires.values())
        assert pire <= EPS
        lignes.append(f"{regle} : résidu / S maximal {pire:.3e} (seuil {EPS:g})")
    publier("Identités par pas sur 720 pas, 20 graines (max sur graines, clôtures, instances)",
            lignes)


def test_accumulation_publiee(trajectoires, publier):
    """A ≤ ε_V, strictement positive sur au moins une graine (critère 11) ; publiée avec sa
    médiane par graine et sa marge 1e−12 / A (C98-1)."""
    par_graine = {g: b.compteur.releve.accumulation_maximale() for g, b in trajectoires.items()}
    maxima = [rapport for rapport, _, _ in par_graine.values()]
    a = max(maxima)
    graine, (_, t, secteur) = max(par_graine.items(), key=lambda kv: kv[1][0])
    assert a <= EPS_V
    assert a > 0.0
    mediane = statistics.median(maxima)
    publier("Accumulation A de l'identité cumulée (C98-1)", [
        "définition : max sur les graines, les secteurs s et les pas t < 720 de "
        "|V^stock_{s,t+1} − V^flux_{s,t+1}| / S_{s,t}",
        "unité : sans dimension ; dénominateur : S_{s,t}, échelle du bilan à l'ouverture du "
        f"pas ; fenêtre : 720 pas depuis l'état initial du générateur, {len(maxima)} graines",
        f"A = {a:.3e} (graine {graine}, pas {t}, secteur {secteur})",
        f"médiane par graine = {mediane:.3e}",
        f"marge 1e−12 / A = {EPS_V / a:.1f}",
    ])


# --------------------------------------------------------------------------
# Couverture du générateur (critères 4 à 9)
# --------------------------------------------------------------------------


def test_couverture_des_lignes(trajectoires, publier):
    """Critère 4 : chaque ligne décidée non nulle sur ≥ 90 % des pas ; chaque ligne à deux sens
    prend chacun sur ≥ 5 % des pas ; les contreparties 17, 20 et 22 sont non nulles."""
    lignes = []
    for graine, bilan in trajectoires.items():
        c = bilan.compteur
        non_nulles = {ligne: fraction(c.non_nulles[ligne]) for ligne in cat.IDENTIFIANTS}
        for ligne in LIGNES_DECIDEES:
            assert non_nulles[ligne] >= 0.9, (graine, ligne)
        for ligne in LIGNES_A_DEUX_SIGNES:
            assert fraction(c.negatives[ligne]) >= 0.05, (graine, ligne)
            assert fraction(c.positives[ligne]) >= 0.05, (graine, ligne)
        for ligne in CONTREPARTIES:
            assert c.non_nulles[ligne] > 0, (graine, ligne)
        pire = min(LIGNES_DECIDEES, key=non_nulles.get)
        signe = min(LIGNES_A_DEUX_SIGNES,
                    key=lambda li: min(c.negatives[li], c.positives[li]))
        lignes.append(
            f"graine {graine} : non nulle ≥ {non_nulles[pire]:.1%} (ligne {pire}) ; sens "
            f"minoritaire ≥ {fraction(min(c.negatives[signe], c.positives[signe])):.1%} "
            f"(ligne {signe}) ; contreparties non nulles "
            + ", ".join(f"{li} {non_nulles[li]:.0%}" for li in CONTREPARTIES))
    publier("Couverture des lignes par graine (critère 4)", lignes)


def test_regimes_de_la_banque_centrale(trajectoires, publier):
    """Critère 5 : L^CB > 0 avec Res = 0, Res > 0 avec L^CB = 0, transitions dans les deux sens ;
    E^CB des deux signes ; Res_{t+1} ≥ 0 et Res_{t+1}·L^CB_{t+1} = 0 exactement (critère 6)."""
    lignes = []
    for graine, b in trajectoires.items():
        assert b.regimes["Res = 0, L^CB > 0"] > 0 and b.regimes["Res > 0, L^CB = 0"] > 0, graine
        assert b.transitions[("Res = 0, L^CB > 0", "Res > 0, L^CB = 0")] > 0, graine
        assert b.transitions[("Res > 0, L^CB = 0", "Res = 0, L^CB > 0")] > 0, graine
        assert b.e_cb_signes["négatif"] > 0 and b.e_cb_signes["positif"] > 0, graine
        assert b.produit_res_lcb_nul and b.reserves_positives, graine
        lignes.append(f"graine {graine} : " + ", ".join(
            f"{r} {n}" for r, n in sorted(b.regimes.items()))
                      + f" ; transitions {sum(b.transitions.values())} ; E^CB < 0 sur "
                      f"{fraction(b.e_cb_signes['négatif']):.0%} des pas")
    publier("Régimes de la banque centrale par graine (critère 5)", lignes)


def test_decouvert_intra_pas_et_trois_cas_de_b7(trajectoires, publier):
    """Critère 6 : découvert (Res < 0) en fin des phases 6, 7 et 8 (a) sur ≥ 25 % des pas
    chacune ; les trois cas de B7 couverts."""
    lignes = []
    for graine, b in trajectoires.items():
        c = b.compteur
        for phase in ("6", "7", "8a"):
            assert fraction(c.decouvert[phase]) >= 0.25, (graine, phase)
        assert set(c.cas_b7) == {"Res < 0", "0 ≤ Res ≤ L^CB", "Res > L^CB"}, graine
        lignes.append(f"graine {graine} : découvert " + ", ".join(
            f"phase {p} {fraction(c.decouvert[p]):.0%}" for p in ("6", "7", "8a"))
                      + " ; B7 " + ", ".join(f"{k} {n}" for k, n in sorted(c.cas_b7.items())))
    publier("Découvert intra-pas et cas de B7 par graine (critère 6)", lignes)


def test_ligne_16_negative_et_montant_couvert(trajectoires, publier):
    """Critère 7 et complément du point 8 : ligne 16 négative sur ≥ 10 % des pas, cas u = 0,
    0 < u < |Π| et u = |Π| hors poussière ; exécuté = −c et exécuté − proposé = u, bit à bit ;
    M^G de clôture de 8 (b) = fl(M^{G,8a} − c) ≥ 0 exactement, nul quand la perte sature, si
    M^{G,8a} ≥ 0 ; sinon M^{G,8a} est une poussière dans le domaine −ε × S_État (oracle
    indépendant), c = 0 et M^G inchangée (lecture validée par le mainteneur le 14/10/2026)."""
    lignes = []
    totaux = collections.Counter()
    pire_poussiere = 0.0
    for graine, b in trajectoires.items():
        c = b.compteur
        assert fraction(sum(c.cas_16.values())) >= 0.1, graine
        assert c.u_exact, graine
        assert c.m_g_8b_hors_forme == 0, graine
        assert c.poussiere_hors_domaine == 0, graine
        pire_poussiere = max(pire_poussiere, c.pire_poussiere_8a)
        totaux.update(c.cas_16)
        lignes.append(f"graine {graine} : ligne 16 proposée négative sur "
                      f"{fraction(sum(c.cas_16.values())):.0%} des pas ; "
                      + ", ".join(f"{k} {n}" for k, n in sorted(c.cas_16.items())))
    assert {"u = 0", "0 < u < |Π|", "u = |Π|"} <= set(totaux)
    lignes.append(f"cas de poussière M^(G,8a) < 0 : {totaux['poussière (c = 0)']} sur toutes "
                  f"les graines ; pire |M^(G,8a)| / S_État = {pire_poussiere:.3e} "
                  f"(domaine ε = {EPS:g})")
    publier("Ligne 16 négative et montant couvert par graine (critère 7)", lignes)


def test_ligne_16_trois_cas_par_graine(trajectoires):
    """Critère 7 : les trois cas du montant couvert sur chaque graine, hors cas de poussière."""
    for graine, b in trajectoires.items():
        assert {"u = 0", "0 < u < |Π|", "u = |Π|"} <= set(b.compteur.cas_16) <= {
            "u = 0", "0 < u < |Π|", "u = |Π|", "poussière (c = 0)"}, graine


def test_lecture_nette_exercee(trajectoires, publier):
    """Critère 8 : des paiements bruts de l'État en phase 6 dépassent son encaisse de début de
    phase et sont couverts par les recettes de la même phase (la trajectoire passe le contrôle
    de caisse) ; une encaisse en poussière négative (E6 saturée, plusieurs lignes) passe."""
    brut = {g: b.compteur.brut_au_dela for g, b in trajectoires.items()}
    poussiere = {g: b.compteur.m_g_6_poussiere for g, b in trajectoires.items()}
    assert all(n > 0 for n in brut.values())
    assert sum(poussiere.values()) > 0
    publier("Lecture nette exercée (critère 8)", [
        "pas où les paiements bruts de l'État en phase 6 dépassent M^G de début de phase : "
        + ", ".join(f"{n}" for n in brut.values()),
        "pas où M^G est en poussière négative en fin de phase 6 (E6 saturée) : "
        + ", ".join(f"{n}" for n in poussiere.values()),
    ])


def test_prix_ecrit_en_phase_5_des_deux_signes(trajectoires):
    """Critère 9 : P_t écrit en phase 5 (`"P"`), variations des deux signes sur chaque graine."""
    for graine, b in trajectoires.items():
        assert b.prix_signes["baisse"] > 0 and b.prix_signes["hausse"] > 0, graine


# --------------------------------------------------------------------------
# Ordres de grandeur, absence de dégénérescence (critères 10 et 11)
# --------------------------------------------------------------------------


def test_ordres_de_grandeur(trajectoires, generateur, publier):
    """Critère 10 : bilans d'environ 1e7 u.m. ; croissance nominale d'environ 4 % par an ;
    opérandes bruts d'au plus 10 S par secteur et par phase ; R publié par bilan."""
    s0 = echelles(positions_de(generateur.etat_initial(GRAINES[0])))
    assert all(1e6 <= s <= 1e8 for s in s0.values())
    r_max = dict.fromkeys(cat.SECTEURS, 0.0)
    croissances = []
    for b in trajectoires.values():
        for s in cat.SECTEURS:
            r_max[s] = max(r_max[s], b.compteur.r_max[s])
        croissances.append((b.etat_final.K / b.etat_initial.K) ** (PAS_PAR_AN.valeur / NB_PAS)
                           - 1.0)
    assert all(r <= 10.0 for r in r_max.values())
    assert all(0.03 <= g <= 0.05 for g in croissances)
    publier("Ordres de grandeur (critère 10)", [
        "S à l'ouverture du pas 0 : " + ", ".join(f"{s} {v:.2e}" for s, v in s0.items()),
        "croissance nominale de K, par an : " + f"{min(croissances):.2%} à {max(croissances):.2%}",
        "R = Σ|opérandes| / S_ouverture, max sur les phases, pas et graines : "
        + ", ".join(f"{s} {r:.2f}" for s, r in r_max.items()),
    ])


def test_dynamique_bornee_et_montants_generiques(trajectoires, generateur, publier):
    """Critère 11 : chaque rapport poste / S reste dans sa bande déclarée (`BANDES`) ; les
    montants sont des flottants génériques (≥ 24 bits significatifs)."""
    lignes = []
    for (poste, secteur), (bas, haut) in generateur.BANDES.items():
        mini = min(b.bandes[(poste, secteur)][0] for b in trajectoires.values())
        maxi = max(b.bandes[(poste, secteur)][1] for b in trajectoires.values())
        assert bas <= mini and maxi <= haut, (poste, secteur, mini, maxi)
        lignes.append(f"{poste} / S_{secteur} : [{mini:.3g} ; {maxi:.3g}] dans [{bas} ; {haut}]")
    for graine, b in trajectoires.items():
        assert b.compteur.montants_non_generiques <= 0.001 * b.compteur.montants, graine
    publier("Bandes des rapports poste / S (critère 11)", lignes)


# --------------------------------------------------------------------------
# Portes de la monnaie, oracle indépendant (C98-5, critère 12)
# --------------------------------------------------------------------------


def test_oracle_des_portes_lit_la_specification(portes):
    """L'oracle lit tab:portes-monnaie (lecteur de verifier_matrices), jamais le catalogue :
    28 lignes, 17 et 20 « poste », 22 sans effet monétaire."""
    assert len(portes) == 28
    assert portes["17"] == portes["20"] == (None, None)
    assert portes["22"] == (0, 0)


def test_portes_par_phase_et_par_pas(trajectoires, publier):
    """ΔM = ΔD_H + ΔD_F et ΔH = ΔRes, par phase et par pas, ≤ ε × S, S le plus petit des S
    du pas (lecture (α), au plus strict)."""
    phase = max(b.compteur.porte_phase for b in trajectoires.values())
    pas = max(b.compteur.porte_pas for b in trajectoires.values())
    assert phase <= EPS and pas <= EPS
    publier("Portes de la monnaie, oracle tab:portes-monnaie (C98-5)", [
        f"par phase : résidu / S_min maximal {phase:.3e} ; par pas : {pas:.3e} (seuil {EPS:g})"])


# --------------------------------------------------------------------------
# Générateur : contrat des blocs (critères 1 à 3, 9)
# --------------------------------------------------------------------------


def test_tirages_fonction_pure_de_graine_et_pas(generateur):
    """Critère 1 : mêmes (graine, t), mêmes tirages, quel que soit l'ordre des appels."""
    a = [generateur.tirages(g, t) for g in GRAINES[:3] for t in (0, 1, 719)]
    b = [generateur.tirages(g, t) for g in reversed(GRAINES[:3]) for t in (719, 1, 0)]
    assert a == b[::-1]
    assert generateur.tirages(GRAINES[0], 0) != generateur.tirages(GRAINES[0], 1)
    assert all(type(x) is float for x in generateur.tirages(GRAINES[0], 0).values())


def test_pseudo_blocs_conformes_au_contrat(generateur, monkeypatch):
    """Critères 2, 3 et 9 : huit pseudo-blocs sans attribut d'instance, sièges de PHASES, lignes
    décidées seulement (25 propositions et une déclaration de montant couvert), `"P"` en
    phase 5 par `prix` ; l'assemblage les accepte."""
    generateur.doubler_19b(monkeypatch)
    blocs = generateur.blocs()
    sieges_de_phases = {(r, e.identifiant) for phase in PHASES for e in phase.etapes
                        for g in e.groupes for r in g if r not in ("moteur", "noyau")}
    assert {(b.declaration.radical, s.etape) for b in blocs
            for s in b.declaration.sieges} == sieges_de_phases
    assert len(blocs) == 8
    propose = [li for b in blocs for s in b.declaration.sieges for li in s.propose]
    couvre = [li for b in blocs for s in b.declaration.sieges for li in s.couvre]
    assert sorted(propose) == sorted(LIGNES_DECIDEES)
    assert len(propose) == 25 and couvre == ["16"]
    assert not set(propose) & set(CONTREPARTIES)
    ecrit_p = [(b.declaration.radical, s.etape) for b in blocs for s in b.declaration.sieges
               if ordo.INDICE_DES_PRIX in s.ecrit]
    assert ecrit_p == [("prix", "5")]
    for b in blocs:
        assert not hasattr(b, "__dict__")
    generateur.ordonnanceur()


def test_generateur_lit_des_montants_executes(generateur):
    """Les lectures du générateur comprennent des montants exécutés (ligne 5), contrôlés par la
    colonne « Lisent »."""
    lectures = {(b.declaration.radical, s.etape, lu.nom) for b in generateur.blocs()
                for s in b.declaration.sieges for lu in s.lit if lu.source == "grand_livre"
                and lu.nom in cat.LIGNE}
    assert ("menages", "5", "5") in lectures and ("finances_publiques", "6", "5") in lectures


def test_colonne_lisent_controle_les_lectures_du_generateur(generateur, monkeypatch):
    """Retirer la phase 4 de la colonne « Lisent » de la phase 5 fait refuser le générateur
    (montant exécuté de la ligne 5 lu en phase 5)."""
    generateur.doubler_19b(monkeypatch)
    phases = tuple(Phase(p.numero, p.nom, p.etapes, tuple(x for x in p.lisent if x != 4))
                   if p.numero == 5 else p for p in PHASES)
    with pytest.raises(DefautDeDeclaration, match="Lisent"):
        ordo.assembler(phases, generateur.blocs(), CADRE, generateur.DECLARATION_DES_ENTREES)


@pytest.mark.parametrize("lire, erreur, motif", [
    (lambda lecteur: lecteur.position("L"), "LectureNonDeclaree", "'L'"),
    (lambda lecteur: lecteur.caisse("M_G"), "LectureNonDeclaree", "'M_G'"),
    (lambda lecteur: lecteur.position("D_H"), "ContratDePoussiere", "max"),
    (lambda lecteur: lecteur.caisse("B_H"), "ContratDePoussiere", "lecture nette"),
    (lambda lecteur: lecteur.ouverture("D_H"), "ContratDePoussiere", "caisse_ouverture"),
    (lambda lecteur: lecteur.ouverture("M_G"), "ContratDePoussiere", "caisse_ouverture"),
    (lambda lecteur: lecteur.caisse_ouverture("K"), "ContratDePoussiere", "lecture nette"),
    (lambda lecteur: lecteur.caisse_ouverture("D_F"), "LectureNonDeclaree", "'D_F'"),
])
def test_lectures_du_generateur_controlees(generateur, monkeypatch, lire, erreur, motif):
    """Une lecture absente du siège, ou un moyen de paiement à lecture nette lu sans
    max(0 ; ·), arrête le pseudo-bloc (contrat des blocs ; ADR 0012, A8)."""
    generateur.doubler_19b(monkeypatch)

    class MenagesIndiscrets(generateur.Menages):
        __slots__ = ()

        def phase_5(self, vue):
            lire(self._lecteur(vue, "5"))

    o = generateur.ordonnanceur({"menages": MenagesIndiscrets})
    with pytest.raises(getattr(generateur, erreur), match=motif):
        generateur.derouler(generateur.etat_initial(GRAINES[0]), 1, o, ObservateurNul())


def test_moyens_de_paiement_lus_en_caisse(generateur):
    """Contrat de poussière (A8) : les pseudo-blocs lisent D_H, D_F et M^G au grand livre, et
    D_H et D_F à l'ouverture, toujours en max(0 ; ·) (`caisse`, `caisse_ouverture`) : le
    lecteur refuse toute autre lecture de ces trois postes, quelle que soit la source."""
    lus = {(lu.source, lu.nom) for b in generateur.blocs() for s in b.declaration.sieges
           for lu in s.lit}
    assert generateur.MOYENS_LUS_EN_CAISSE == {"D_H", "D_F", "M_G"}
    assert {(GRAND_LIVRE, m) for m in generateur.MOYENS_LUS_EN_CAISSE} <= lus
    assert {(OUVERTURE, "D_H"), (OUVERTURE, "D_F")} <= lus


# --------------------------------------------------------------------------
# Permutation de 8 (b) et homogénéité nominale (critères 7 et 12)
# --------------------------------------------------------------------------


class Empreinte:
    """Observateur d'essai : empreinte bit à bit des clôtures et des états."""

    def __init__(self, facteur=1.0):
        self.facteur = facteur
        self.evenements = []

    def relever(self, e):
        f = self.facteur
        if type(e) is ClotureDePhase:
            self.evenements.append((e.t, e.phase, tuple((r, o, bits(x)) for r, o, x in e.rapports),
                                    tuple((li, tuple((n, bits(x / f)) for n, x in m))
                                          for li, m in e.montants)))
        else:
            etat = e.etat
            self.evenements.append((e.t, tuple(bits(getattr(etat, n) / f)
                                               for n in cat.NOMS_POSTES),
                                    tuple(bits(x / f) for x in etat.registre_prix)))


class Double:
    """Observateur d'essai qui transmet chaque événement à plusieurs observateurs."""

    def __init__(self, *observateurs):
        self.observateurs = observateurs

    def relever(self, evenement):
        for observateur in self.observateurs:
            observateur.relever(evenement)


FENETRE_DE_PERMUTATION = 240


def test_permutation_de_8b_bit_a_bit(generateur, monkeypatch, portes):
    """Critère 7 : l'ordre d'appel de (banque centrale, État) en 8 (b) laisse clôtures et états
    identiques bit à bit, sur une fenêtre où la ligne 16 est négative et couverte des trois
    façons (affirmé dans la fenêtre même, hors cas de poussière)."""
    generateur.doubler_19b(monkeypatch)
    reference, compteur = Empreinte(), Compteur(portes)
    espionner(monkeypatch, compteur)
    generateur.derouler(generateur.etat_initial(GRAINES[0]), FENETRE_DE_PERMUTATION,
                        generateur.ordonnanceur(), Double(reference, compteur))
    assert {"u = 0", "0 < u < |Π|", "u = |Π|"} <= set(compteur.cas_16)
    canonique = ordo._ordre_du_groupe
    monkeypatch.setattr(ordo, "_ordre_du_groupe", lambda g: tuple(reversed(canonique(g))))
    o = generateur.ordonnanceur()
    assert [d.radical for d, _ in dict(o.etapes)["8b"]] == ["finances_publiques",
                                                            "banque_centrale"]
    permute = Empreinte()
    generateur.derouler(generateur.etat_initial(GRAINES[0]), FENETRE_DE_PERMUTATION, o, permute)
    assert permute.evenements == reference.evenements


@pytest.mark.parametrize("graine", GRAINES[:3])
def test_homogeneite_sous_128_bit_a_bit(generateur, monkeypatch, graine):
    """Critère 12 (C98-4) : sous une redénomination ×128, la trajectoire est identique bit à
    bit (montants, positions, registre divisés par 128 ; rapports résidu / S inchangés)."""
    generateur.doubler_19b(monkeypatch)
    o = generateur.ordonnanceur()
    un = Empreinte()
    generateur.derouler(generateur.etat_initial(graine), NB_PAS, o, un)
    cent_vingt_huit = Empreinte(128.0)
    generateur.derouler(generateur.redenominer(generateur.etat_initial(graine), 128.0), NB_PAS, o,
                        cent_vingt_huit)
    assert cent_vingt_huit.evenements == un.evenements


@pytest.mark.parametrize("graine", GRAINES[:5])
def test_invariance_d_unite_sous_100(generateur, monkeypatch, graine, publier):
    """Invariance ×100 (ADR 0005, point 19, annoté) : résidu / S ≤ 1e−12 ; champs nominaux à
    |x^{×100} − 100 x| ≤ 1e−10 × 100 S_s ; registre et glissement à 1e−10 en relatif.

    S_s est pris sur l'état t + 1 comparé, c'est-à-dire à l'ouverture du pas suivant (lecture
    retenue, sans effet numérique sur le verdict) ; pour une position, le plus petit S des deux
    bilans qui la tiennent."""
    generateur.doubler_19b(monkeypatch)
    o = generateur.ordonnanceur()
    releve = ReleveDesResidus()
    e1 = generateur.etat_initial(graine)
    e100 = generateur.redenominer(e1, 100.0)
    pire_champ = pire_registre = pire_glissement = 0.0
    for _ in range(NB_PAS):
        e1 = generateur.derouler(e1, 1, o, ObservateurNul())
        e100 = generateur.derouler(e100, 1, o, releve)
        s = echelles(positions_de(e1))
        for poste in cat.POSTES:
            echelle = min(s[poste.detenteur], s[poste.emetteur]) if poste.emetteur else s[
                poste.detenteur]
            ecart = abs(getattr(e100, poste.nom) - 100.0 * getattr(e1, poste.nom))
            pire_champ = max(pire_champ, ecart / (100.0 * echelle))
        for secteur in cat.SECTEURS:
            nom = cat.VALEUR_NETTE_FLUX[secteur]
            ecart = abs(getattr(e100, nom) - 100.0 * getattr(e1, nom))
            pire_champ = max(pire_champ, ecart / (100.0 * s[secteur]))
        for x100, x1 in zip(e100.registre_prix, e1.registre_prix, strict=True):
            pire_registre = max(pire_registre, abs(x100 / (100.0 * x1) - 1.0))
        g1, g100 = registre.glissement(e1.registre_prix), registre.glissement(e100.registre_prix)
        pire_glissement = max(pire_glissement, abs(g100 - g1) / abs(g1))
    for regle in REGLES_PAR_PAS + ("eq:noyau-tolerance-cumulee",):
        assert releve.maximum(regle)[0] <= EPS
    assert pire_champ <= 1e-10 and pire_registre <= 1e-10 and pire_glissement <= 1e-10
    publier(f"Invariance ×100, graine {graine}, 720 pas", [
        f"champs nominaux : max |x^×100 − 100 x| / (100 S_s) = {pire_champ:.3e} (seuil 1e−10)",
        f"registre : {pire_registre:.3e} ; glissement : {pire_glissement:.3e} (seuil 1e−10)"])


# --------------------------------------------------------------------------
# Reprise à la frontière de tour (D4)
# --------------------------------------------------------------------------


def test_reprise_a_la_frontiere_de_tour_bit_a_bit(generateur, monkeypatch):
    """Sauvegarde après la phase 9 du pas 359, rechargée : la trajectoire et le relevé des
    résidus jusqu'au pas 719 sont identiques bit à bit à ceux d'une trajectoire continue."""
    generateur.doubler_19b(monkeypatch)
    o = generateur.ordonnanceur()
    graine = GRAINES[0]
    continu, releve_continu = Empreinte(), ReleveDesResidus()

    fin_continue = generateur.derouler(generateur.etat_initial(graine), NB_PAS, o,
                                       Double(continu, releve_continu))
    # Un pas intercalé, sur une autre graine, décale d'un pas tout état caché du
    # processus (compteur, cache) : sinon, un état de période divisant 720 échapperait.
    generateur.derouler(generateur.etat_initial(GRAINES[1]), 1, o, ObservateurNul())
    avant, releve_avant = Empreinte(), ReleveDesResidus()
    milieu = generateur.derouler(generateur.etat_initial(graine), NB_PAS // 2, o,
                                 Double(avant, releve_avant))
    repris, = charger(sauvegarder([milieu]))
    apres, releve_apres = Empreinte(), ReleveDesResidus()
    fin_reprise = generateur.derouler(repris, NB_PAS - NB_PAS // 2, o, Double(apres, releve_apres))
    assert sauvegarder([fin_reprise]) == sauvegarder([fin_continue])
    assert avant.evenements + apres.evenements == continu.evenements
    assert [bits(x) for *_, x in releve_avant.releves() + releve_apres.releves()] == [
        bits(x) for *_, x in releve_continu.releves()]
    assert releve_avant.pas() + releve_apres.pas() == tuple(range(NB_PAS))


def test_decisions_differentes_apres_reprise_divergent_en_phase_1(generateur, monkeypatch):
    """D4 : après la reprise, un levier différent ne change rien avant la phase 1 du pas repris
    (grandeurs d'ouverture et entrée de scénario identiques) ; la première différence est en
    phase 1 (levier et taux directeur), puis dans les montants exécutés."""
    generateur.doubler_19b(monkeypatch)
    o = generateur.ordonnanceur()
    graine, reprise = GRAINES[1], 360
    milieu = generateur.derouler(generateur.etat_initial(graine), reprise, o, ObservateurNul())
    repris, = charger(sauvegarder([milieu]))
    memes, autres = [], []

    class Garde:
        def __init__(self, liste):
            self.liste = liste

        def relever(self, e):
            self.liste.append(e)

    generateur.derouler(repris, 1, o, Garde(memes))
    generateur.derouler(repris, 1, o, Garde(autres), decalage=lambda t: 0.01)
    fin_memes, fin_autres = memes[-1], autres[-1]
    assert fin_memes.grandeurs_ouverture == fin_autres.grandeurs_ouverture
    # Étape d'écriture de chaque variable du pas : entrées (moteur) puis sièges.
    etape = {generateur.SCENARIO: "0", generateur.LEVIER: "1"}
    for b in generateur.blocs():
        for s in b.declaration.sieges:
            etape.update(dict.fromkeys(s.ecrit, s.etape))
    rang = {e: k for k, e in enumerate(("0",) + cat.PHASES)}
    differences = [etape[n] for (n, x), (_, y) in zip(fin_memes.variables_du_pas,
                                                      fin_autres.variables_du_pas, strict=True)
                   if x != y]
    differences += [c1.phase for c1, c2 in zip(memes[:-1], autres[:-1], strict=True) if c1 != c2]
    assert differences and min(differences, key=rang.get) == "1"
    assert dict(fin_memes.variables_du_pas)[generateur.SCENARIO] == dict(
        fin_autres.variables_du_pas)[generateur.SCENARIO]
    assert dict(fin_memes.variables_du_pas)["i_CB"] != dict(fin_autres.variables_du_pas)["i_CB"]
    assert sauvegarder([fin_memes.etat]) != sauvegarder([fin_autres.etat])


# --------------------------------------------------------------------------
# Capitalisation annuelle (C98-2)
# --------------------------------------------------------------------------


def test_capitalisation_annuelle(generateur, monkeypatch, publier):
    """Sur n_a pas, la somme des intérêts versés sur un encours constant vaut i·X ; un intérêt
    crédité dans l'encours rend (1 + i/n_a)^{n_a} − 1 sur l'année ; à 1e−12 en relatif.

    Configuration dédiée : les pseudo-blocs proposent toutes leurs lignes à zéro, sauf les
    intérêts sur titres des ménages (11a, encours B_H constant) et les intérêts sur les dépôts
    des entreprises (10, crédités dans D_F, seule ligne qui touche D_F).
    """
    generateur.doubler_19b(monkeypatch)
    n_a = PAS_PAR_AN.valeur
    i_b, i_d = 0.0371, 0.0237

    class Capitalisation(generateur._PseudoBloc):
        __slots__ = ()

        def _agir(self, vue, etape):
            siege = next(s for s in self.declaration.sieges if s.etape == etape)
            for ligne in siege.propose:
                montants = {t.nom: 0.0 for t in cat.LIGNE[ligne].termes}
                if ligne == "11a":
                    montants["iB_BH"] = par_pas(TauxDeFlux(i_b)) * vue.ouverture.B_H
                elif ligne == "10":
                    # D_F à l'ouverture se lit en max(0 ; ·) (contrat de poussière, A8).
                    montants["iD_DF"] = par_pas(TauxDeFlux(i_d)) * max(0.0, vue.ouverture.D_F)
                vue.proposer(ligne, montants)
            for nom in siege.ecrit:
                vue.ecrire_pas(nom, vue.dernier_prix() if nom == ordo.INDICE_DES_PRIX else 1.0)

    def classe_dediee(classe):
        espace = {"__slots__": (), "declaration": classe.declaration}
        for siege in classe.declaration.sieges:
            espace[f"phase_{siege.etape}"] = (
                lambda etape: lambda self, vue: self._agir(vue, etape))(siege.etape)
        return type(classe.__name__ + "Dediee", (Capitalisation,), espace)

    o = generateur.ordonnanceur({c.declaration.radical: classe_dediee(c)
                                 for c in generateur.PSEUDO_BLOCS})
    etat = generateur.etat_initial(GRAINES[0])
    d_f0, b_h = etat.D_F, etat.B_H
    verses = []

    class Interets:
        def relever(self, e):
            if type(e) is ClotureDePhase and e.phase == "6":
                verses.append(dict(dict(e.montants)["11a"])["iB_BH"])

    etat = generateur.derouler(etat, n_a, o, Interets())
    somme = 0.0
    for x in verses:
        somme += x
    rendement = (1.0 + i_d / n_a) ** n_a - 1.0
    assert len(verses) == n_a and etat.B_H == b_h
    assert abs(somme / (i_b * b_h) - 1.0) <= 1e-12
    assert abs((etat.D_F / d_f0 - 1.0) / rendement - 1.0) <= 1e-12
    publier("Capitalisation annuelle (C98-2)", [
        f"Σ des intérêts sur {n_a} pas / (i X) − 1 = {somme / (i_b * b_h) - 1.0:.1e}",
        f"intérêt crédité dans l'encours : rendement annuel (D_F,{n_a} / D_F,0 − 1) / "
        f"((1 + i/n_a)^n_a − 1) − 1 = {(etat.D_F / d_f0 - 1.0) / rendement - 1.0:.1e}",
        f"rendement déclaré, (1 + i/n_a)^n_a − 1 à i = {i_d} : {rendement:.12f}"])


# --------------------------------------------------------------------------
# Variantes en échec (critères 6 et 8 ; ADR 0012, point 8)
# --------------------------------------------------------------------------


def _derouler_jusqu_a_l_arret(generateur, o, nb_pas=NB_PAS, graine=GRAINES[0]):
    with pytest.raises(DefautComptable) as defaut:
        generateur.derouler(generateur.etat_initial(graine), nb_pas, o, ObservateurNul())
    return defaut.value


def _publier_defaut(publier, nom, defaut):
    publier(f"Variante en échec : {nom}", [
        f"arrêt au pas {defaut.t}, phase {defaut.phase}, {defaut.regle} ; résidu {defaut.residu:.6e} "
        f"u.m., S = {defaut.echelle:.6e}, résidu / S = {defaut.rapport:.3e}"])


def test_b7_sous_couverte_est_un_defaut(generateur, monkeypatch, publier):
    """C98-6 : une banque qui ne refinance que 99,9 % de son découvert arrête le moteur en
    phase 9 sur Res_{t+1} ≥ 0 (strict)."""
    generateur.doubler_19b(monkeypatch)

    class BanqueSousCouverte(generateur.Banque):
        __slots__ = ()

        def phase_8c(self, vue):
            livre = vue.grand_livre
            reserves, refinancement = livre.position("Res"), livre.position("L_CB")
            vue.proposer("21", {"Delta_LCB": -min(reserves, refinancement) if reserves >= 0.0
                                else -0.999 * reserves})

    defaut = _derouler_jusqu_a_l_arret(generateur, generateur.ordonnanceur(
        {"banque": BanqueSousCouverte}))
    assert (defaut.phase, defaut.regle) == ("9", "eq:noyau-reserves-cloture")
    _publier_defaut(publier, "B7 sous-couverte (99,9 % du découvert)", defaut)


def test_b7_sous_forme_litterale_arrete_sur_l_arrondi(generateur, monkeypatch, publier):
    """Critère 6 : B7 écrite max(L^CB − Res^{8b} ; 0) − L^CB, algébriquement égale à −min, laisse
    Res_{t+1} < 0 par arrondi : arrêt en phase 9 sur un résidu sous ε × S^Bk, que seul le
    contrôle strict détecte ; d'où la forme −min du générateur (et de #90)."""
    generateur.doubler_19b(monkeypatch)

    class BanqueLitterale(generateur.Banque):
        __slots__ = ()

        def phase_8c(self, vue):
            livre = vue.grand_livre
            reserves, refinancement = livre.position("Res"), livre.position("L_CB")
            vue.proposer("21", {"Delta_LCB": max(refinancement - reserves, 0.0)
                                - refinancement})

    defaut = _derouler_jusqu_a_l_arret(generateur, generateur.ordonnanceur(
        {"banque": BanqueLitterale}))
    assert (defaut.phase, defaut.regle) == ("9", "eq:noyau-reserves-cloture")
    assert -EPS * defaut.echelle <= defaut.residu < 0.0
    _publier_defaut(publier, "B7 sous forme littérale", defaut)


def _variante_menages(generateur):
    """Impôt des ménages : 1,1 fois leur caisse de début de phase 6, si bien que D_H en fin de
    phase 6 vaut −(0,1 × caisse de début de phase − entrées des ménages de la phase 6) : un
    découvert de 10 % de la caisse diminué des entrées. La phase 7 le rétablirait (rachat aux
    ménages de titres pour 0,2 fois leur caisse d'ouverture, prémisse affirmée par le test),
    mais l'exécution s'arrête en phase 6, à la clôture où la caisse est négative."""
    base = generateur.FinancesPubliques.declaration
    ajouts = {"6": (Lecture(GRAND_LIVRE, "D_H"),), "7": (Lecture(OUVERTURE, "D_H"),)}
    sieges = tuple(dataclasses.replace(s, lit=s.lit + ajouts.get(s.etape, ()))
                   for s in base.sieges)

    class EtatVariante(generateur.FinancesPubliques):
        __slots__ = ()
        declaration = dataclasses.replace(base, sieges=sieges)

        def impot_des_menages(self, lecteur, impot):
            return 1.1 * lecteur.caisse("D_H")

        def titres_des_menages(self, lecteur, emission):
            # Rachat aux ménages de titres pour 0,2 fois leur caisse d'ouverture.
            return emission - 0.2 * lecteur.caisse_ouverture("D_H")
    return {"finances_publiques": EtatVariante}


def _variante_entreprises(generateur):
    """Dividendes des entreprises : toute leur caisse de début de phase 6, plus 0,1 S."""
    class InvestissementVariante(generateur.Investissement):
        __slots__ = ()

        def phase_6(self, vue):
            livre = vue.grand_livre
            vue.proposer("8", {"deltaK": generateur.DELTA_PAS * vue.ouverture.K})
            vue.proposer("14", {"Div_F": livre.position("D_F")
                                + 0.1 * livre.echelle("entreprises")})
    return {"investissement": InvestissementVariante}


def _variante_etat(generateur, en_sus):
    """E6 saturée chaque pas (plan de transferts sans limite), plus `en_sus` × S_État."""
    class EtatVariante(generateur.FinancesPubliques):
        __slots__ = ()

        def plan_de_transferts(self, plan):
            return math.inf

        def transferts(self, lecteur, transferts, plafond):
            return transferts + en_sus * lecteur.echelle("etat")
    return {"finances_publiques": EtatVariante}


@pytest.mark.parametrize("variante, moyen, secteur", [
    ("menages", "D_H", "menages"),
    ("entreprises", "D_F", "entreprises"),
    ("etat", "M_G", "etat"),
])
def test_variante_en_echec_par_moyen_de_paiement(generateur, monkeypatch, variante, moyen,
                                                  secteur, publier):
    """Critère 8 : une variante par moyen de paiement soumis à la lecture nette, qui paie au-delà
    de sa caisse en phase 6 (M^G : 1e−6 × S_État au-delà de E6 saturée) : arrêt en phase 6,
    payeur et moyen nommés ; une caisse que la phase 7 rétablirait (ménages) n'y change rien."""
    generateur.doubler_19b(monkeypatch)
    remplacer = {"menages": _variante_menages, "entreprises": _variante_entreprises,
                 "etat": lambda g: _variante_etat(g, 1e-6)}[variante](generateur)
    defaut = _derouler_jusqu_a_l_arret(generateur, generateur.ordonnanceur(remplacer), nb_pas=3)
    assert (defaut.phase, defaut.regle, defaut.secteur, defaut.moyen) == (
        "6", "eq:noyau-caisse-nette", secteur, moyen)
    if variante == "menages":
        # Prémisse « rétablie en phase 7 » : le rachat de la variante (0,2 × D_H d'ouverture,
        # l'émission de base étant ≤ 0 sur une caisse nulle) moins la plus forte vente
        # possible de la banque centrale aux ménages (2 % de B_H) couvre le découvert.
        initial = generateur.etat_initial(GRAINES[0])
        assert defaut.t == 0 and defaut.residu < 0.0
        assert 0.2 * initial.D_H - 0.02 * initial.B_H + defaut.residu > 0.0
    _publier_defaut(publier, f"caisse {moyen} ({secteur})", defaut)


def test_e6_saturee_poussiere_negative_admise(generateur, monkeypatch, portes, publier):
    """ADR 0012, Conséquences (point 8) : E6 saturée à chaque pas laisse M^G en poussière, de
    signe quelconque (plusieurs lignes) ; une poussière négative passe le contrôle."""
    generateur.doubler_19b(monkeypatch)
    compteur = Compteur(portes)
    espionner(monkeypatch, compteur)
    o = generateur.ordonnanceur(_variante_etat(generateur, 0.0))
    generateur.derouler(generateur.etat_initial(GRAINES[0]), NB_PAS, o, compteur)
    assert compteur.m_g_6_poussiere > 0
    publier("E6 saturée à chaque pas (point 8)", [
        f"pas où M^G est en poussière négative en fin de phase 6 : {compteur.m_g_6_poussiere} "
        f"sur {NB_PAS}, sans arrêt"])
