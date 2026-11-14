"""Socle partiel d'essai : huit blocs d'essai sur le sentier, schéma v3 (issues #112, #61).

Critères d'acceptation de #112, écrits avant l'essai (issue #112 ; P52, P66,
P67 ; synthèse du rang 1a de J3-b, § 6) : 720 pas depuis l'état résolu, aux
trois π* ∈ {0 ; 2 % ; 10 %}, sans arrêt du noyau, identités à ε × S ; chaque
variable d'état sur son sentier à 1e−10 relatif après un pas et à 1e−9 sur
720 pas ; **stationnarité partielle** (P67) : B1 à B7, B12, B13 et B24 à 1e−9
relatif sur 720 pas, B4 à B7 et B24 (et B13, fenêtre de 12 tours) dès le pas
11 (D13), une grandeur de valeur résolue nulle jugée en valeur absolue,
|x| ≤ 1e−12 (P66 : B7 à π* = 0, ξ) ; reprise au bit à la frontière de tour
sous le schéma v2, puis v3 (#61) ; invariance × 100 sur les variables nouvelles ; permutation
des blocs d'un groupe identique au bit ; bijection propriétaire ↔ écrivain
pour chaque variable nouvelle.

Ces mesures portent l'étiquette du socle (`socle_partiel.ETIQUETTE`) (réserve de
`monnaie`) : le socle partiel ne vaut pas verdict de boucle conjointe. Tant
qu'aucun bloc réel n'y est substitué, elles éprouvent le moteur (noyau,
ordonnanceur, registre, schéma v3) sur le sentier, pas un bloc.

Critères de #61 (feuille de route § 1, écrits avant l'essai) éprouvés ici :
π*_{t+1} = π*_t exactement à levier fermé (bloc d'essai 8, BC4 ; M30 ; ADR 0013,
annotation du 14/11/2026, point 6), π*_t lue à l'ouverture, y compris hors du
sentier ; Γ^e de la phase 0 égal à [(1 + g)(1 + π*)]^{1/n_a} à 1e−15 relatif à
chaque pas ; reprise exacte en v3.
"""

import dataclasses
import math

import pytest

from nations.etat import schema
from nations.etat.sauvegarde import charger, sauvegarder
from nations.moteur import ordonnanceur as ordo
from nations.moteur.conversions import par_pas
from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres import TauxDeFlux, varier
from nations.moteur.parametres.cadre import CADRE, PAS_PAR_AN
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.moteur.phases import ETAPES, MOTEUR, NOYAU
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.diagnostics import DefautComptable
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas, ObservateurNul
from nations.observation.residus import ReleveDesResidus

N_A = PAS_PAR_AN.valeur
NB_PAS = 720
EPS = CADRE.tolerance_identite_pas
EPS_V = CADRE.tolerance_identite_cumulee
REGLES_PAR_PAS = ("eq:noyau-somme-ligne", "eq:noyau-somme-colonne", "eq:noyau-cloture-poste",
                  "eq:noyau-variation-monnaie", "eq:noyau-variation-monnaie-centrale")
# Seuils écrits avant l'essai (#112 ; P66, P67).
SEUIL_UN_PAS = 1e-10
SEUIL_720_PAS = 1e-9
SEUIL_NUL = 1e-12
# Premier pas jugé des grandeurs sur 12 tours (D13).
PREMIER_PAS_SUR_12_TOURS = N_A - 1


class Releve:
    """Observateur d'essai : par pas, montants exécutés des lignes 1 à 5, variables du pas,
    grandeurs d'ouverture et état t + 1."""

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
                             "grandeurs": dict(e.grandeurs_ouverture), "etat": e.etat})
            self._montants = {}


class Empreinte:
    """Observateur d'essai : empreinte exacte des clôtures (`repr` des montants et rapports) et
    des états t + 1 (document de sauvegarde)."""

    def __init__(self):
        self.evenements = []

    def relever(self, e):
        if type(e) is ClotureDePhase:
            self.evenements.append((e.t, e.phase, repr(e.rapports), repr(e.montants)))
        else:
            self.evenements.append((e.t, sauvegarder([e.etat]), repr(e.variables_du_pas),
                                    repr(e.grandeurs_ouverture)))


class Double:
    def __init__(self, *observateurs):
        self.observateurs = observateurs

    def relever(self, e):
        for observateur in self.observateurs:
            observateur.relever(e)


@dataclasses.dataclass
class Trajectoire:
    sentier: object
    initial: object
    releve: Releve
    residus: ReleveDesResidus


@pytest.fixture(scope="module")
def trajectoires(socle):
    """Une trajectoire de 720 pas par π*, depuis l'état résolu, sans choc."""
    rendues = {}
    for pi in socle.POINTS_PI:
        sentier = socle.sentier(pi)
        initial = socle.etat_initial(sentier)
        releve, residus = Releve(), ReleveDesResidus()
        socle.derouler(initial, NB_PAS, socle.ordonnanceur(sentier), Double(releve, residus))
        rendues[pi] = Trajectoire(sentier, initial, releve, residus)
    return rendues


def ecart(x, reference):
    """|x/x̄ − 1| ; pour une valeur résolue nulle, |x| (P66)."""
    return abs(x) if reference == 0.0 else abs(x / reference - 1.0)


# --------------------------------------------------------------------------
# Contrat : huit blocs d'essai, rien dans src/ ne les connaît
# --------------------------------------------------------------------------


def test_huit_blocs_d_essai_conformes_au_contrat(socle):
    """Un bloc d'essai par radical, sans attribut d'instance, un siège par étape où
    `tab:phases` le déclare ; toutes les lignes à proposant au socle proposées une fois ;
    les quatorze variables d'état écrites chacune par son propriétaire ; l'assemblage les accepte."""
    sentier = socle.sentier(0.02)
    blocs = socle.blocs(sentier)
    assert [b.declaration.radical for b in blocs] == list(socle.RADICAUX)
    sieges = {(r, e.identifiant) for e in ETAPES for g in e.groupes for r in g
              if r not in (MOTEUR, NOYAU)}
    assert {(b.declaration.radical, s.etape) for b in blocs for s in b.declaration.sieges} == sieges
    proposees = sorted(li for b in blocs for s in b.declaration.sieges for li in s.propose)
    assert proposees == sorted(li.identifiant for li in cat.LIGNES if li.proposant is not None)
    ecrites = {nom: (b.declaration.radical, s.etape) for b in blocs
               for s in b.declaration.sieges for nom in s.etat}
    assert ecrites == {v.nom: (v.proprietaire, v.phase_ecriture)
                       for v in schema.VARIABLES_DES_BLOCS}
    for b in blocs:
        assert not hasattr(b, "__dict__")
    socle.ordonnanceur(sentier)


# --------------------------------------------------------------------------
# 720 pas sans arrêt, identités ; variables d'état et positions sur le sentier
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_720_pas_sans_arret_et_identites(trajectoires, socle, pi, publier):
    """720 pas depuis l'état résolu sans arrêt du noyau ; identités par pas ≤ ε × S et
    identité cumulée ≤ ε_V × S à chaque clôture."""
    tr = trajectoires[pi]
    assert [p["t"] for p in tr.releve.pas] == list(range(NB_PAS))
    maxima = {regle: tr.residus.maximum(regle)[0]
              for regle in REGLES_PAR_PAS + ("eq:noyau-tolerance-cumulee",)}
    for regle in REGLES_PAR_PAS:
        assert maxima[regle] <= EPS, regle
    assert maxima["eq:noyau-tolerance-cumulee"] <= EPS_V
    publier(f"Socle partiel d'essai, π* = {100 * pi:g} %, 720 pas", [
        f"étiquette : {socle.ETIQUETTE} ; aucun bloc réel",
        "résidu / S maximal : " + " ; ".join(f"{r.removeprefix('eq:noyau-')} {x:.2e}"
                                            for r, x in maxima.items())])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_croissance_tendancielle_du_moteur_egale_au_script(trajectoires, pi):
    """Annotation du 13/11/2026, point 4 : g et (1 + g)^{1/n_a}, calculés une fois par pas en
    phase 0 depuis les tables de référence, égalent au bit g et le facteur de volume du script
    (`facteurs`), à chaque pas."""
    tr = trajectoires[pi]
    f = tr.sentier.facteurs
    attendu_g = (1 + tr.sentier.par.g_pr) * (1 + tr.sentier.par.g_N) - 1
    for p in tr.releve.pas:
        assert p["grandeurs"]["g"].hex() == attendu_g.hex()
        assert p["grandeurs"]["facteur_g"].hex() == f["volume"].hex()


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_cible_en_vigueur_constante_et_gamma_e_de_la_phase_0(trajectoires, pi, publier):
    """Critères de #61 : à levier fermé, π*_{t+1} = π*_t exactement sur 720 pas (bloc d'essai
    8, BC4 ; M30 ; ADR 0013, annotation du 14/11/2026, point 6), à la valeur du paramètre de
    la table du bloc 8 (alignée sur π̄, R1 : `test_table_du_bloc_8_alignee_sur_la_cible`) ;
    Γ^e, calculé en phase 0 sur π*_t lue à l'ouverture, égale [(1 + g)(1 + π*)]^{1/n_a} à
    1e−15 relatif et le facteur nominal Γ̄ du script à 1e−15 relatif, à chaque pas ;
    γ^e = Γ^e − 1."""
    tr = trajectoires[pi]
    assert tr.initial.pi_etoile == pi
    if pi == 0.02:
        assert tr.initial.pi_etoile == PARAMETRES_DE_REFERENCE.banque_centrale.pi_etoile.valeur
    ouvertures = [tr.initial] + [p["etat"] for p in tr.releve.pas]
    assert all(e.pi_etoile == tr.initial.pi_etoile for e in ouvertures)
    pire_direct = pire_script = 0.0
    for t, p in enumerate(tr.releve.pas):
        g = p["grandeurs"]
        direct = ((1.0 + g["g"]) * (1.0 + ouvertures[t].pi_etoile)) ** (1.0 / N_A)
        pire_direct = max(pire_direct, abs(g["Gamma_e"] / direct - 1.0))
        pire_script = max(pire_script, abs(g["Gamma_e"] / tr.sentier.facteurs["nominal"] - 1.0))
        assert g["gamma_e"] == g["Gamma_e"] - 1.0
        assert g["Gamma_e"] == tr.releve.pas[0]["grandeurs"]["Gamma_e"]
    assert pire_direct <= 1e-15 and pire_script <= 1e-15
    publier(f"Γ^e de la phase 0, π* = {100 * pi:g} %, 720 pas (#61)", [
        f"max |Γ^e / [(1 + g)(1 + π*)]^(1/n_a) − 1| = {pire_direct:.2e} ; "
        f"max |Γ^e / Γ̄ du script − 1| = {pire_script:.2e} (seuil 1e−15) ; π* constante"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_table_du_bloc_8_alignee_sur_la_cible(socle, pi):
    """Réserve R1 de `monnaie` (rang 3 de J3-c ; #91) : l'ordonnanceur du socle partiel porte la
    table du bloc 8 alignée sur la cible du sentier (`varier(banque_centrale, pi_etoile=π̄)`) ;
    l'état initial égale la table à chaque π* : π*_0 = π* de la table (valeur initiale de la
    cible en vigueur, BC4) et r̂*_0 = r̄ de la table ; les autres tables sont celles de
    référence, et les autres paramètres du bloc 8 inchangés."""
    sentier = socle.sentier(pi)
    initial = socle.etat_initial(sentier)
    table = socle.ordonnanceur(sentier).parametres.banque_centrale
    assert initial.pi_etoile == table.pi_etoile.valeur == pi
    assert initial.r_hat_etoile == table.r_bar.valeur
    reference = PARAMETRES_DE_REFERENCE
    assert socle.parametres_du_sentier(sentier) == dataclasses.replace(
        reference, banque_centrale=varier(reference.banque_centrale, pi_etoile=pi))
    assert dataclasses.replace(table, pi_etoile=reference.banque_centrale.pi_etoile) == \
        reference.banque_centrale


# Variations d'essai des paramètres des tables des blocs 7 et 8 : (radical, champ de la table,
# nom dans `Parametres` du script, valeur du sentier varié, autre valeur de l'appelant).
VARIATIONS_DES_TABLES_7_ET_8 = (
    ("banque", "varpi_L", "varpi_L", 0.03, 0.025),
    ("banque", "varpi_D", "varpi_D", 0.015, 0.005),
    ("banque", "vartheta", "vartheta", 0.12, 0.08),
    ("banque_centrale", "a_pi", "a_pi", 0.6, 0.4),
    ("banque_centrale", "a_I", "a_I", 0.3, 0.2),
    ("banque_centrale", "lambda_e", "lambda_e", 0.4, 0.1),
    ("banque_centrale", "theta_CB", "theta_CB", 0.1, 0.2),
    ("banque_centrale", "pi_etoile", "pi_cible", 0.05, 0.03),
    ("banque_centrale", "r_bar", "rbar", 0.015, 0.005),
)


def _sentier_varie(socle, nom, valeur):
    """Sentier du script à π̄ = 2 % dont le paramètre `nom` (script) vaut `valeur` ; π* est
    l'argument `pi` de `sentier`."""
    return socle.sentier(valeur) if nom == "pi_cible" else socle.sentier(0.02, **{nom: valeur})


@pytest.mark.parametrize("radical, champ, nom, valeur, autre", VARIATIONS_DES_TABLES_7_ET_8)
def test_tables_de_reference_des_blocs_7_et_8_alignees_sur_le_sentier(socle, radical, champ,
                                                                      nom, valeur, autre):
    """Réserve R1 de `monnaie`, étendue par décision du mainteneur (revue finale de J3-c) : sur
    un sentier construit à un paramètre des blocs 7 ou 8 différent de la table de référence
    (ex. `sentier(0.02, varpi_L=0.03)`), la table de référence de son bloc est alignée sur le
    sentier (`varier(table, champ=valeur)`), l'autre table et les autres paramètres restent ceux
    de référence ; l'ordonnanceur porte la table alignée."""
    sentier = _sentier_varie(socle, nom, valeur)
    reference = PARAMETRES_DE_REFERENCE
    attendu = dataclasses.replace(
        reference, **{radical: varier(getattr(reference, radical), **{champ: valeur})})
    assert socle.parametres_du_sentier(sentier) == attendu
    assert socle.ordonnanceur(sentier).parametres == attendu


@pytest.mark.parametrize("radical, champ, nom, valeur, autre", VARIATIONS_DES_TABLES_7_ET_8)
def test_table_de_l_appelant_hors_du_sentier_refusee(socle, radical, champ, nom, valeur,
                                                     autre):
    """Réserve R1 de `monnaie`, étendue par décision du mainteneur (revue finale de J3-c) : une
    table des blocs 7 ou 8 passée par l'appelant n'est jamais alignée en silence ; refusée
    (`TableHorsDuSentier`, le champ nommé) si un seul de ses paramètres diffère de la valeur
    avec laquelle le script a construit le sentier, que le sentier soit varié (table à une autre
    valeur) ou de référence (table variée seule) ; gardée telle quelle (même objet) si tous ses
    paramètres égalent ceux du sentier."""
    reference = PARAMETRES_DE_REFERENCE

    def de_l_appelant(x):
        return dataclasses.replace(
            reference, **{radical: varier(getattr(reference, radical), **{champ: x})})

    for sentier, table in ((_sentier_varie(socle, nom, valeur), de_l_appelant(autre)),
                           (socle.sentier(0.02), de_l_appelant(valeur))):
        with pytest.raises(socle.TableHorsDuSentier, match=f"{champ} = .*refusée"):
            socle.ordonnanceur(sentier, table)
    parametres = de_l_appelant(valeur)
    assert socle.ordonnanceur(_sentier_varie(socle, nom, valeur), parametres).parametres \
        is parametres


@pytest.mark.parametrize("pi_0", [0.03, 0.0, -0.5])
def test_cible_en_vigueur_hors_du_sentier_reconduite_au_bit(socle, pi_0, publier):
    """Constat M1 de l'audit du rang 3 : le critère π*_{t+1} = π*_t doit pouvoir échouer. Sur le
    sentier à π̄ = 2 %, un état initial à π*_0 ≠ π̄ garde π*_t = π*_0 au bit sur 720 pas (le
    bloc d'essai 8 lit π*_t à l'ouverture, non le sentier), et Γ^e de la phase 0 suit π*_0 à
    1e−15 de la forme directe ; aucun bloc ne lit π* ni Γ^e, et le noyau ne s'arrête pas."""
    sentier = socle.sentier(0.02)
    initial = dataclasses.replace(socle.etat_initial(sentier), pi_etoile=pi_0)
    releve = Releve()
    socle.derouler(initial, NB_PAS, socle.ordonnanceur(sentier), releve)
    assert all(p["etat"].pi_etoile == pi_0 for p in releve.pas)
    pire = max(abs(p["grandeurs"]["Gamma_e"]
                   / ((1.0 + p["grandeurs"]["g"]) * (1.0 + pi_0)) ** (1.0 / N_A) - 1.0)
               for p in releve.pas)
    assert pire <= 1e-15
    publier(f"Cible hors du sentier (M1 de l'audit), π̄ = 2 %, π*_0 = {100 * pi_0:g} %", [
        f"π*_t = π*_0 au bit sur {NB_PAS} pas ; max |Γ^e/direct − 1| = {pire:.2e}"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_variables_d_etat_sur_leur_sentier(trajectoires, socle, pi, publier):
    """Chaque variable d'état des blocs à l'ouverture du pas t égale sa valeur d'ouverture du
    pas 0 × facteur^t à 1e−10 relatif après un pas et à 1e−9 sur 720 pas."""
    tr = trajectoires[pi]
    pires = {}
    for nom in socle.VARIABLES_D_ETAT:
        ecarts = [ecart(getattr(p["etat"], nom), socle.valeur_d_ouverture(tr.sentier, nom, t + 1))
                  for t, p in enumerate(tr.releve.pas)]
        assert ecarts[0] <= SEUIL_UN_PAS, nom
        pires[nom] = max(ecarts)
        assert pires[nom] <= SEUIL_720_PAS, nom
    publier(f"Variables d'état sur le sentier, π* = {100 * pi:g} % ({socle.ETIQUETTE})", [
        "max sur 720 pas de |x_t / (x̄_0 facteur^t) − 1| : "
        + " ; ".join(f"{n} {x:.1e}" for n, x in pires.items())])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_positions_sur_le_sentier(trajectoires, socle, pi, publier):
    """Les onze positions, closes par le noyau sur les flux du sentier, restent sur le sentier
    (position d'ouverture × Γ̄^t) à 1e−9 relatif ; une position nulle (B_H, B_CB, Res) reste
    nulle à 1e−12 × S de son détenteur."""
    tr = trajectoires[pi]
    pires = {}
    for poste in cat.POSTES:
        pire = 0.0
        for t, p in enumerate(tr.releve.pas):
            x = getattr(p["etat"], poste.nom)
            reference = socle.position_d_ouverture(tr.sentier, poste.nom, t + 1)
            if reference == 0.0:
                positions = {q: getattr(p["etat"], q) for q in cat.NOMS_POSTES}
                pire = max(pire, abs(x) / idt.echelle_bilan(positions, poste.detenteur))
            else:
                pire = max(pire, ecart(x, reference))
        pires[poste.nom] = pire
        assert pire <= (SEUIL_NUL if float(tr.sentier.o[poste.nom]) == 0.0 else SEUIL_720_PAS)
    publier(f"Positions sur le sentier, π* = {100 * pi:g} % ({socle.ETIQUETTE})", [
        "max sur 720 pas : " + " ; ".join(f"{n} {x:.1e}" for n, x in pires.items())])


# --------------------------------------------------------------------------
# Stationnarité partielle (P66, P67)
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_stationnarite_partielle(trajectoires, socle, pi, publier):
    """P67 : max sur 720 pas de |x_t/x̄ − 1| ≤ 1e−9 pour B1 à B7, B12, B13 et B24, depuis
    l'état résolu, sans choc ; P66 : une grandeur de valeur résolue nulle (B7 à π* = 0, ξ) se
    juge en valeur absolue, |x_t| ≤ 1e−12."""
    tr = trajectoires[pi]
    releves = socle.grandeurs_b(tr.releve.pas, tr.initial, tr.sentier)
    resolues = socle.valeurs_resolues(tr.sentier)
    pires = {}
    for cle, serie in releves.items():
        assert serie and serie[-1][0] == NB_PAS - 1
        if cle in ("B4", "B5", "B6", "B7", "B13", "B24"):
            assert serie[0][0] == PREMIER_PAS_SUR_12_TOURS
        pires[cle] = max(ecart(x, resolues[cle]) for _, x in serie)
        seuil = SEUIL_NUL if resolues[cle] == 0.0 else SEUIL_720_PAS
        assert pires[cle] <= seuil, (cle, pires[cle], resolues[cle])
    assert (resolues["B7"] == 0.0) == (pi == 0.0)
    publier(f"Stationnarité partielle (P67), π* = {100 * pi:g} %, 720 pas ({socle.ETIQUETTE})", [
        "max |x_t/x̄ − 1| (|x_t| si x̄ = 0, P66) : "
        + " ; ".join(f"{c} {x:.1e}" for c, x in pires.items())])


# --------------------------------------------------------------------------
# Reprise, invariance × 100, permutation d'un groupe
# --------------------------------------------------------------------------


def test_reprise_a_la_frontiere_de_tour_sous_le_schema_v3(socle):
    """D4 : sauvegarde v3 après la phase 9 du pas 359, rechargée : trajectoire, clôtures et
    états identiques au bit à ceux d'une trajectoire continue, variables des blocs comprises,
    π* comprise (critère de #61)."""
    sentier = socle.sentier(0.02)
    o = socle.ordonnanceur(sentier)
    continu = Empreinte()
    fin_continue = socle.derouler(socle.etat_initial(sentier), NB_PAS, o, continu)
    avant, apres = Empreinte(), Empreinte()
    milieu = socle.derouler(socle.etat_initial(sentier), NB_PAS // 2, o, avant)
    document = sauvegarder([milieu])
    assert b'"version": 3' in document and b'"mu_tilde"' in document
    assert b'"pi_etoile"' in document
    repris, = charger(document)
    assert repris == milieu
    fin_reprise = socle.derouler(repris, NB_PAS - NB_PAS // 2, o, apres)
    assert sauvegarder([fin_reprise]) == sauvegarder([fin_continue])
    assert avant.evenements + apres.evenements == continu.evenements


def test_invariance_sous_100_des_variables_nouvelles(socle, publier):
    """ADR 0005, point 19 ; ADR 0012, annotation du 13/11/2026, point 1.3 : sous une
    redénomination × 100 (état initial et sentier nominal × 100), W est multipliée par 100 et
    les treize autres variables nouvelles sont inchangées, à 1e−10 relatif sur 720 pas ;
    positions et registre multipliés par 100 à 1e−10 relatif."""
    sentier = socle.sentier(0.02)
    un, cent = Releve(), Releve()
    socle.derouler(socle.etat_initial(sentier), NB_PAS, socle.ordonnanceur(sentier), un)
    socle.derouler(socle.etat_initial(sentier, echelle=100.0), NB_PAS,
                   socle.ordonnanceur(sentier, echelle=100.0), cent)
    pire_nouvelles = pire_positions = pire_registre = 0.0
    for p1, p100 in zip(un.pas, cent.pas, strict=True):
        e1, e100 = p1["etat"], p100["etat"]
        for v in schema.VARIABLES_DES_BLOCS:
            facteur = 100.0 if v.invariance is schema.Invariance.NOMINAL else 1.0
            pire_nouvelles = max(pire_nouvelles,
                                 ecart(getattr(e100, v.nom), facteur * getattr(e1, v.nom)))
        for poste in cat.NOMS_POSTES:
            if getattr(e1, poste) != 0.0:
                pire_positions = max(pire_positions,
                                     ecart(getattr(e100, poste), 100.0 * getattr(e1, poste)))
            else:
                assert getattr(e100, poste) == 0.0
        for x100, x1 in zip(e100.registre_prix, e1.registre_prix, strict=True):
            pire_registre = max(pire_registre, ecart(x100, 100.0 * x1))
    assert pire_nouvelles <= SEUIL_UN_PAS
    assert pire_positions <= SEUIL_UN_PAS and pire_registre <= SEUIL_UN_PAS
    assert [v.nom for v in schema.VARIABLES_DES_BLOCS
            if v.invariance is schema.Invariance.NOMINAL] == ["W"]
    publier("Invariance ×100 du socle partiel d'essai, π* = 2 %, 720 pas", [
        f"variables nouvelles : {pire_nouvelles:.1e} ; positions : {pire_positions:.1e} ; "
        f"registre : {pire_registre:.1e} (seuil 1e−10)"])


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_reprise_avec_les_blocs_reels(socle, pi):
    """D4, blocs réels (`blocs_reels` : blocs 2, 3, 4, 7 et 8) substitués à leurs blocs
    d'essai : sauvegarde v3 rechargée, reprise à la frontière de tour des pas 1, 359 et 361
    (la reprise du bloc d'essai est au pas 360) : clôtures et états identiques au bit à ceux d'une
    trajectoire continue de 720 pas."""
    reels = socle.blocs_reels()
    assert reels
    sentier = socle.sentier(pi)
    o = socle.ordonnanceur(sentier, reels=reels)
    continu = Empreinte()
    fin_continue = socle.derouler(socle.etat_initial(sentier), NB_PAS, o, continu)
    for k in (1, NB_PAS // 2 - 1, NB_PAS // 2 + 1):
        avant, apres = Empreinte(), Empreinte()
        milieu = socle.derouler(socle.etat_initial(sentier), k, o, avant)
        repris, = charger(sauvegarder([milieu]))
        assert repris == milieu
        fin_reprise = socle.derouler(repris, NB_PAS - k, o, apres)
        assert sauvegarder([fin_reprise]) == sauvegarder([fin_continue]), k
        assert avant.evenements + apres.evenements == continu.evenements, k


def test_invariance_sous_100_avec_les_blocs_reels(socle, publier):
    """ADR 0005, point 19, blocs réels (`blocs_reels` : blocs 2, 3, 4, 7 et 8) substitués à
    leurs blocs d'essai : sous une redénomination × 100, W est multipliée par 100 et les
    treize autres variables nouvelles sont inchangées, à 1e−10 relatif sur 720 pas ; positions et
    registre × 100 à 1e−10 relatif."""
    reels = socle.blocs_reels()
    # Libellé publié « blocs réels 2, 3, 4, 7 et 8 » tenu par la mesure.
    assert [b.declaration.radical for b in reels] == ["production", "travail", "prix",
                                                    "banque", "banque_centrale"]
    sentier = socle.sentier(0.02)
    un, cent = Releve(), Releve()
    socle.derouler(socle.etat_initial(sentier), NB_PAS,
                   socle.ordonnanceur(sentier, reels=reels), un)
    socle.derouler(socle.etat_initial(sentier, echelle=100.0), NB_PAS,
                   socle.ordonnanceur(sentier, echelle=100.0, reels=reels), cent)
    pire_nouvelles = pire_positions = pire_registre = 0.0
    for p1, p100 in zip(un.pas, cent.pas, strict=True):
        e1, e100 = p1["etat"], p100["etat"]
        for v in schema.VARIABLES_DES_BLOCS:
            facteur = 100.0 if v.invariance is schema.Invariance.NOMINAL else 1.0
            pire_nouvelles = max(pire_nouvelles,
                                 ecart(getattr(e100, v.nom), facteur * getattr(e1, v.nom)))
        for poste in cat.NOMS_POSTES:
            if getattr(e1, poste) != 0.0:
                pire_positions = max(pire_positions,
                                     ecart(getattr(e100, poste), 100.0 * getattr(e1, poste)))
            else:
                assert getattr(e100, poste) == 0.0
        for x100, x1 in zip(e100.registre_prix, e1.registre_prix, strict=True):
            pire_registre = max(pire_registre, ecart(x100, 100.0 * x1))
    assert pire_nouvelles <= SEUIL_UN_PAS
    assert pire_positions <= SEUIL_UN_PAS and pire_registre <= SEUIL_UN_PAS
    publier("Invariance ×100, blocs réels 2, 3, 4, 7 et 8 substitués, π* = 2 %, 720 pas", [
        f"variables nouvelles : {pire_nouvelles:.1e} ; positions : {pire_positions:.1e} ; "
        f"registre : {pire_registre:.1e} (seuil 1e−10)"])


def test_permutation_des_blocs_d_un_groupe_identique_au_bit(socle, monkeypatch):
    """B5.2 : l'ordre d'appel des blocs d'un groupe (ordre canonique inversé) laisse clôtures,
    variables du pas et états identiques au bit sur 120 pas ; l'ordre de la liste passée à
    `assembler` aussi."""
    sentier = socle.sentier(0.02)
    reference = Empreinte()
    socle.derouler(socle.etat_initial(sentier), 120, socle.ordonnanceur(sentier), reference)
    liste = Empreinte()
    o = ordo.assembler(socle.PHASES, tuple(reversed(socle.blocs(sentier))),
                       socle.PARAMETRES_DE_REFERENCE, socle.SANS_ENTREES)
    socle.derouler(socle.etat_initial(sentier), 120, o, liste)
    monkeypatch.setattr(ordo, "_ordre_du_groupe", lambda groupe: tuple(sorted(groupe,
                                                                              reverse=True)))
    inverse = Empreinte()
    socle.derouler(socle.etat_initial(sentier), 120, socle.ordonnanceur(sentier), inverse)
    assert any(len(g) > 1 for e in ETAPES for g in e.groupes)
    assert liste.evenements == reference.evenements
    assert inverse.evenements == reference.evenements


# --------------------------------------------------------------------------
# Bijection propriétaire ↔ écrivain des variables nouvelles
# --------------------------------------------------------------------------


def _avec_etat(declaration, etape, etat):
    sieges = tuple(dataclasses.replace(s, etat=etat) if s.etape == etape else s
                   for s in declaration.sieges)
    return dataclasses.replace(declaration, sieges=sieges)


def _assembler_avec(socle, declarations):
    sentier = socle.sentier(0.02)
    return ordo.assembler(socle.PHASES, socle.blocs(sentier, declarations=declarations),
                          socle.PARAMETRES_DE_REFERENCE, socle.SANS_ENTREES)


@pytest.mark.parametrize("nom", [v.nom for v in schema.VARIABLES_DES_BLOCS])
def test_bijection_proprietaire_ecrivain(socle, nom):
    """C1, B3 : chaque variable nouvelle sans écrivain est refusée à l'assemblage ; écrite par un
    autre bloc de la même étape, ou par son propriétaire hors de sa phase, aussi."""
    v = schema.VARIABLE[nom]
    propre = socle.declaration_d_essai(v.proprietaire)
    siege = next(s for s in propre.sieges if s.etape == v.phase_ecriture)
    sans = _avec_etat(propre, v.phase_ecriture, tuple(n for n in siege.etat if n != nom))
    with pytest.raises(DefautDeDeclaration, match=f"« {nom} ».*sans propriétaire qui l'écrive"):
        _assembler_avec(socle, {v.proprietaire: sans})
    # Un autre bloc de la même étape l'écrit à la place de son propriétaire ; en 8 (c), la banque
    # est le seul écrivain de `tab:phases` (i_L, i_D, #90) : le cas n'existe pas.
    autres = [r for r in socle.RADICAUX if r != v.proprietaire
              and v.phase_ecriture in socle.etapes_du(r)]
    assert autres or (v.proprietaire, v.phase_ecriture) == ("banque", "8c")
    for autre in autres[:1]:
        intrus = socle.declaration_d_essai(autre)
        siege_intrus = next(s for s in intrus.sieges if s.etape == v.phase_ecriture)
        intrus = _avec_etat(intrus, v.phase_ecriture, siege_intrus.etat + (nom,))
        with pytest.raises(DefautDeDeclaration, match=f"« {nom} ».*écrite par un autre bloc"):
            _assembler_avec(socle, {v.proprietaire: sans, autre: intrus})
    # Son propriétaire l'écrit dans une autre de ses étapes.
    autres_etapes = [e for e in socle.etapes_du(v.proprietaire) if e != v.phase_ecriture]
    if autres_etapes:
        ailleurs = next(s for s in sans.sieges if s.etape == autres_etapes[0])
        deplace = _avec_etat(sans, autres_etapes[0], ailleurs.etat + (nom,))
        with pytest.raises(DefautDeDeclaration, match=f"« {nom} ».*hors de sa phase"):
            _assembler_avec(socle, {v.proprietaire: deplace})


# --------------------------------------------------------------------------
# Acheteurs au prix du pas ; variante à π^e choqué
# --------------------------------------------------------------------------


def test_acheteurs_au_prix_du_pas_sur_les_volumes_servis(socle):
    """Synthèse du rang 1a, § 8 : sous un choc des plans (G^plan + 1 % aux pas 1 à 12, C^plan
    − 2 % au pas 3), les plans écrits suivent le choc, mais les lignes 1 à 3 restent
    p_t × volume servi (lu au bloc 2), au bit, et non les plans."""
    sentier = socle.sentier(0.02)

    def chocs(nom, t):
        if nom == "G_plan" and 1 <= t <= 12:
            return 1.01
        if nom == "C_plan" and t == 3:
            return 0.98
        return 1.0

    base, choque = Releve(), Releve()
    socle.derouler(socle.etat_initial(sentier), 24, socle.ordonnanceur(sentier), base)
    socle.derouler(socle.etat_initial(sentier), 24,
                   socle.ordonnanceur(sentier, chocs_des_plans=chocs), choque)
    for t, (p0, p1) in enumerate(zip(base.pas, choque.pas, strict=True)):
        v = p1["variables"]
        assert p1["1"] == v["p"] * v["C_vol"]
        assert p1["3"] == v["p"] * v["I_vol"]
        assert p1["2"] == v["p"] * v["G_vol"]
        assert v["G_plan"] == p0["variables"]["G_plan"] * chocs("G_plan", t)
        assert v["C_plan"] == p0["variables"]["C_plan"] * chocs("C_plan", t)
        assert (p1["1"], p1["2"], p1["3"]) == (p0["1"], p0["2"], p0["3"])


def test_variante_du_bloc_8_a_pi_e_choque(socle, publier):
    """Synthèse du rang 1a, § 8 : π^e choquée, injectée dans l'état d'ouverture (π^e_0 dans
    l'état initial, π^e_{t+1} écrite en phase 1) ; π^e d'ouverture suit le choc déclaré, et
    reste dans le domaine 1 + π^e > 0 du schéma v3."""
    sentier = socle.sentier(0.02)

    def choc(t):
        return 0.01 if 5 <= t <= 16 else 0.0

    releve = Releve()
    initial = socle.etat_initial(sentier, choc_pi_e0=choc(0))
    socle.derouler(initial, 24, socle.ordonnanceur(sentier, choc_pi_e=choc), releve)
    ouvertures = [initial.pi_e] + [p["etat"].pi_e for p in releve.pas]
    for t, pi_e in enumerate(ouvertures):
        assert abs(pi_e - (0.02 + choc(t))) <= 1e-15, t
    with pytest.raises(ValueError, match="1 \\+ π\\^e > 0"):
        socle.etat_initial(sentier, choc_pi_e0=-1.02)
    publier("Variante du bloc d'essai 8 à π^e choqué", [
        f"étiquette : {socle.ETIQUETTE} ; π^e d'ouverture = π* + 1 point aux pas 5 à 16"])


def test_etat_initial_tire_de_l_ouverture_du_script(socle):
    """L'état initial vient de `ouverture` du script : positions, registre, variables des blocs
    (μ̃ = ln(1 + μ̄), π^e = π̄) ; V^flux = V^stock ; il passe les domaines du schéma v2 aux
    trois π*."""
    for pi in socle.POINTS_PI:
        sentier = socle.sentier(pi)
        e = socle.etat_initial(sentier)
        assert e.mu_tilde == math.log(1 + sentier.par.mu_bar)
        assert e.pi_e == pi and e.U == sentier.par.U_eq
        assert e.registre_prix == tuple(sentier.o["registre"])
        for s in cat.SECTEURS:
            assert getattr(e, cat.VALEUR_NETTE_FLUX[s]) == idt.valeur_nette_stock(
                {p: getattr(e, p) for p in cat.NOMS_POSTES}, s)


def test_observateur_nul_meme_trajectoire(socle):
    """E1 : la trajectoire ne dépend pas de l'observateur."""
    sentier = socle.sentier(0.10)
    o = socle.ordonnanceur(sentier)
    a = socle.derouler(socle.etat_initial(sentier), 60, o, ObservateurNul())
    b = socle.derouler(socle.etat_initial(sentier), 60, o, Empreinte())
    assert sauvegarder([a]) == sauvegarder([b])


# --------------------------------------------------------------------------
# Linéarisation de la carte d'un pas du moteur (#112, point 4)
# --------------------------------------------------------------------------


# Positions de la carte du cas d'essai : intérieures à leur domaine sur le sentier (non nulles).
POSTES_LINEARISES = ("D_H", "D_F", "L", "B_Bk", "L_CB", "M_G", "K", "IN")


def _regle_n1(socle):
    """Règle d'essai de v^e : N1, demande d exogène sur le sentier, λ_v lue dans la table."""
    def n1(vue, sentier, t):
        lam = par_pas(vue.parametres.production.lambda_v)
        demande = sentier.valeur("v", socle.VOLUME, t)
        return sentier.facteurs[socle.VOLUME] * ((1.0 - lam) * vue.ouverture.v_e + lam * demande)
    return n1


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
@pytest.mark.parametrize("lambda_v", [3.0, 6.0, 1.5])
def test_linearisation_retrouve_une_valeur_propre_connue(socle, linearisation, pi, lambda_v,
                                                         publier):
    """Critère de #112 : sur un cas d'essai, la linéarisation de la carte d'un pas du moteur
    retrouve à 1e−8 des valeurs propres connues en forme fermée. Cas : le bloc d'essai de la
    production suit N1 pour v^e, demande d exogène sur le sentier, λ_v lue dans la table par la
    vue (référence 3, puis × 2 et × 0,5 par le constructeur validé) : v^e ramenée au sentier a
    la valeur propre 1 − λ_v/n_a ; chaque position, aux flux exogènes, a 1/Γ̄ ; π*, reconduite
    depuis l'ouverture (BC4), 1 ; les variables écrites au sentier, 0."""
    sentier = socle.sentier(pi)
    p = socle.PARAMETRES_DE_REFERENCE
    parametres = dataclasses.replace(p, production=varier(p.production, lambda_v=lambda_v))
    o = socle.ordonnanceur(sentier, parametres, regles={"v_e": _regle_n1(socle)})
    postes = POSTES_LINEARISES
    noms = tuple(v.nom for v in schema.VARIABLES_DES_BLOCS) + postes
    carte = linearisation.carte_du_moteur(socle.etat_initial(sentier), o, noms, pi)
    assert linearisation.residu_point_fixe(carte) <= SEUIL_NUL
    valeurs = linearisation.valeurs_propres(carte)
    # π* reconduite depuis l'ouverture (BC4 à levier fermé) : valeur propre 1, racine unitaire
    # de la cible en vigueur, qu'aucun bloc ne ramène (constat M1 de l'audit du rang 3 de J3-c).
    attendues = sorted([1.0, 1.0 - lambda_v / N_A] + [1.0 / sentier.facteurs[socle.NOMINAL]]
                       * len(postes) + [0.0] * (len(noms) - len(postes) - 2), reverse=True)
    ecart_max = float(max(abs(valeurs - attendues)))
    assert ecart_max <= 1e-8
    if (pi, lambda_v) == (0.02, 3.0):
        publier("Linéarisation de la carte d'un pas (#112, point 4), π* = 2 %, λ_v = 3", [
            f"valeur propre de v^e : {valeurs[len(postes) + 1].real:.12f} (1 − λ_v/n_a = 0,75) ; "
            f"1/Γ̄ = {1.0 / sentier.facteurs[socle.NOMINAL]:.12f} (multiplicité {len(postes)}) ; "
            f"écart maximal aux formes fermées {ecart_max:.1e} (seuil 1e−8)"])


def test_linearisation_tendance_lue_dans_l_unite_a_croissance_demographique(socle, linearisation,
                                                                            publier):
    """Q2 de `macro` (#112) : à g_N = 0,005 (constructeur validé, sentier du script au même
    g_N) et π* = 2 %, pr, N et N^pa, W et v^e ont des facteurs de tendance distincts ; la
    tendance lue d'après l'unité ramène chaque variable au point fixe (résidu ≤ 1e−12) et donne
    les valeurs propres de la forme fermée à 1e−8 (1 − λ_v/n_a, 1/Γ̄, 0). Facteurs attendus,
    mesurés par `macro` : 1,001651581302 (pr), 1,000415714845 (N, N^pa), 1,003305890325 (W)."""
    pi, g_n = 0.02, 0.005
    sentier = socle.sentier(pi, g_N=g_n)
    p = socle.PARAMETRES_DE_REFERENCE
    parametres = dataclasses.replace(p, travail=varier(p.travail, g_N=g_n))
    o = socle.ordonnanceur(sentier, parametres, regles={"v_e": _regle_n1(socle)})
    facteurs = {n: linearisation.facteur_de_tendance(schema.VARIABLE[n].unite, parametres, pi)
                for n in ("pr", "N", "N_pa", "W", "v_e")}
    attendus = {"pr": 1.001651581302, "N": 1.000415714845, "N_pa": 1.000415714845,
                "W": 1.003305890325}
    for nom, attendu in attendus.items():
        assert abs(facteurs[nom] - attendu) <= 1e-12, nom
    # v^e croît au taux g : (1 + g_pr)(1 + g_N), distinct de pr seule.
    assert facteurs["v_e"] == pytest.approx(facteurs["pr"] * facteurs["N"], rel=1e-14, abs=0.0)
    assert facteurs["v_e"] - facteurs["pr"] > 4e-4
    postes = POSTES_LINEARISES
    noms = tuple(v.nom for v in schema.VARIABLES_DES_BLOCS) + postes
    carte = linearisation.carte_du_moteur(socle.etat_initial(sentier), o, noms, pi)
    residu = linearisation.residu_point_fixe(carte)
    assert residu <= SEUIL_NUL
    valeurs = linearisation.valeurs_propres(carte)
    # π* reconduite depuis l'ouverture (BC4 à levier fermé) : valeur propre 1, racine unitaire
    # de la cible en vigueur, qu'aucun bloc ne ramène (constat M1 de l'audit du rang 3 de J3-c).
    attendues = sorted([1.0, 1.0 - 3.0 / N_A] + [1.0 / sentier.facteurs[socle.NOMINAL]]
                       * len(postes) + [0.0] * (len(noms) - len(postes) - 2), reverse=True)
    ecart_max = float(max(abs(valeurs - attendues)))
    assert ecart_max <= 1e-8
    publier("Linéarisation à g_N = 0,005, π* = 2 %, λ_v = 3 (#112, Q2 de `macro`)", [
        f"facteurs par pas : pr {facteurs['pr']:.12f}, N et N^pa {facteurs['N']:.12f}, "
        f"W {facteurs['W']:.12f}, v^e {facteurs['v_e']:.12f} ; résidu du point fixe "
        f"{residu:.1e} ; écart maximal aux formes fermées {ecart_max:.1e} (seuil 1e−8)"])


def test_linearisation_refuse_franchement_une_variable_au_bord_de_son_domaine(socle,
                                                                             linearisation):
    """C3 (#112) : la différence centrée n'est pas définie au bord d'un domaine strict. Res = 0
    sur le sentier, perturbée de −h, fait arrêter le noyau (`DefautComptable`) : refus franc,
    jamais une valeur propre. Le traitement de Res, B_H et B_CB revient à S1 (J3-f)."""
    sentier = socle.sentier(0.02)
    etat = socle.etat_initial(sentier)
    assert etat.Res == 0.0
    carte = linearisation.carte_du_moteur(etat, socle.ordonnanceur(sentier), ("Res",), 0.02)
    with pytest.raises(DefautComptable):
        linearisation.jacobienne(carte)


# --------------------------------------------------------------------------
# Règles d'essai de ligne (`lignes`) sur les lignes d'acheteur et d'intérêts sur titres
# --------------------------------------------------------------------------


class ReleveDesLignes:
    """Observateur d'essai : par pas, montants exécutés des lignes 2 et 11b (total des termes)."""

    LIGNES = ("2", "11b")

    def __init__(self):
        self.pas = []
        self._montants = {}

    def relever(self, e):
        if type(e) is ClotureDePhase:
            for ligne, termes in e.montants:
                if ligne in self.LIGNES:
                    self._montants[ligne] = sum(x for _, x in termes)
        elif type(e) is FinDePas:
            self.pas.append(self._montants)
            self._montants = {}


def test_regle_de_ligne_prime_sur_acheteur_et_interets_sur_titres(socle):
    """Constat m6 de l'audit du rang 6 de J3-c (m-T3 de la revue finale) : une règle d'essai de
    ligne (`lignes`) prime sur toute autre forme du bloc d'essai, y compris sur une ligne
    d'acheteur (ligne 2, p × G^vol) et sur une ligne d'intérêts sur titres (11b, E7) ; sur 3 pas
    du socle à blocs d'essai, π* = 2 %, chaque règle est appelée une fois par pas et son montant,
    distinct de la forme par défaut (× 1,001), est exécuté au bit."""
    appels = {"2": [], "11b": []}

    def depense(vue, sentier):
        defaut = vue.lire("p") * vue.lire("G_vol")
        appels["2"].append((defaut, 1.001 * defaut))
        return {"G": 1.001 * defaut}

    def interets(vue, sentier):
        defaut = par_pas(TauxDeFlux(vue.lire("i_CB"))) * vue.ouverture.B_Bk
        appels["11b"].append((defaut, 1.001 * defaut))
        return {"iB_BBk": 1.001 * defaut}

    sentier = socle.sentier(0.02)
    releve = ReleveDesLignes()
    socle.derouler(socle.etat_initial(sentier), 3,
                   socle.ordonnanceur(sentier, lignes={"2": depense, "11b": interets}), releve)
    for ligne, rendus in appels.items():
        assert len(rendus) == 3, ligne
        for t, (defaut, regle) in enumerate(rendus):
            assert regle != defaut and defaut > 0.0, (ligne, t)
            assert releve.pas[t][ligne].hex() == regle.hex(), (ligne, t)
