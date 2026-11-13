"""Socle partiel d'essai : huit blocs d'essai sur le sentier, schéma v2 (issue #112).

Critères d'acceptation de #112, écrits avant l'essai (issue #112 ; P52, P66,
P67 ; synthèse du rang 1a de J3-b, § 6) : 720 pas depuis l'état résolu, aux
trois π* ∈ {0 ; 2 % ; 10 %}, sans arrêt du noyau, identités à ε × S ; chaque
variable d'état sur son sentier à 1e−10 relatif après un pas et à 1e−9 sur
720 pas ; **stationnarité partielle** (P67) : B1 à B7, B12, B13 et B24 à 1e−9
relatif sur 720 pas, B4 à B7 et B24 (et B13, fenêtre de 12 tours) dès le pas
11 (D13), une grandeur de valeur résolue nulle jugée en valeur absolue,
|x| ≤ 1e−12 (P66 : B7 à π* = 0, ξ) ; reprise au bit à la frontière de tour
sous le schéma v2 ; invariance × 100 sur les variables nouvelles ; permutation
des blocs d'un groupe identique au bit ; bijection propriétaire ↔ écrivain
pour chaque variable nouvelle.

Ces mesures portent l'étiquette « π^e exogène (bloc d'essai) » (réserve de
`monnaie`) : le socle partiel ne vaut pas verdict de boucle conjointe. Tant
qu'aucun bloc réel n'y est substitué, elles éprouvent le moteur (noyau,
ordonnanceur, registre, schéma v2) sur le sentier, pas un bloc.
"""

import dataclasses
import math

import pytest

from nations.etat import schema
from nations.etat.sauvegarde import charger, sauvegarder
from nations.moteur import ordonnanceur as ordo
from nations.moteur.conversions import par_pas
from nations.moteur.diagnostics import DefautDeDeclaration
from nations.moteur.parametres import varier
from nations.moteur.parametres.cadre import CADRE, PAS_PAR_AN
from nations.moteur.phases import ETAPES, MOTEUR, NOYAU
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
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
    les dix variables d'état écrites chacune par son propriétaire ; l'assemblage les accepte."""
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
def test_720_pas_sans_arret_et_identites(trajectoires, pi, publier):
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
        "étiquette : π^e exogène (bloc d'essai) ; aucun bloc réel",
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
    publier(f"Variables d'état sur le sentier, π* = {100 * pi:g} % (π^e exogène, bloc d'essai)", [
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
    publier(f"Positions sur le sentier, π* = {100 * pi:g} % (π^e exogène, bloc d'essai)", [
        "max sur 720 pas : " + " ; ".join(f"{n} {x:.1e}" for n, x in pires.items())])


# --------------------------------------------------------------------------
# Stationnarité partielle (P66, P67)
# --------------------------------------------------------------------------


def grandeurs_b(tr):
    """B1 à B7, B12, B13, B24 et ξ relevées sur la trajectoire du moteur, définitions de
    `tab:criteres-j3` : (t, valeur) par grandeur ; fenêtres de 12 tours dès le pas 11."""
    pas, initial = tr.releve.pas, tr.initial
    ouvertures = [initial] + [p["etat"] for p in pas[:-1]]
    g = {cle: [] for cle in ("B1", "B2", "B3", "B4", "B5", "B6", "B7", "B12", "B13", "B24",
                              "xi")}
    for t, p in enumerate(pas):
        v, o = p["variables"], ouvertures[t]
        pib = p["1"] + p["2"] + p["3"] + p["4"]
        g["B1"].append((t, o.IN_vol / v["v"]))
        g["B2"].append((t, v["y"] / v["y_cap"]))
        g["B3"].append((t, v["U_suivant"]))
        g["B12"].append((t, v["p"] * o.K_vol / (N_A * pib)))
        g["xi"].append((t, v["xi"]))
        if t < PREMIER_PAS_SUR_12_TOURS:
            continue
        fenetre = pas[t - N_A + 1:t + 1]
        g["B4"].append((t, sum(q["5"] for q in fenetre)
                        / sum(q["1"] + q["2"] + q["3"] + q["4"] for q in fenetre)))
        if t - N_A >= 0:
            w0, p0, y0 = (pas[t - N_A]["variables"][n] for n in ("W_suivant", "p", "y"))
        else:  # t − 12 = −1 : salaire, prix et production d'ouverture du pas 0
            w0, p0, y0 = initial.W, initial.registre_prix[0], float(tr.sentier.o["y_m1"])
        g["B5"].append((t, (v["W_suivant"] / v["p"]) / (w0 / p0) - 1.0))
        g["B6"].append((t, sum(q["variables"]["p"] / q["variables"]["UC"] - 1.0
                               for q in fenetre) / N_A))
        g["B7"].append((t, v["P"] / o.registre_prix[N_A - 1] - 1.0))
        g["B13"].append((t, sum(q["3"] for q in fenetre)
                         / sum(q["1"] + q["2"] + q["3"] + q["4"] for q in fenetre)))
        g["B24"].append((t, v["y"] / y0 - 1.0))
    return g


def valeurs_resolues(socle, sentier):
    """Valeurs résolues du script (`valeurs`, état `e`, paramètres), même définition."""
    e, par = sentier.e, sentier.par
    v = socle.script().valeurs(e, par)
    return {"B1": v["IN_sur_v"], "B2": v["tu"], "B3": v["U"], "B4": v["part_salariale"],
            "B5": par.g_pr, "B6": e["p"] / e["UC"] - 1.0, "B7": v["glissement"] / 100.0,
            "B12": v["K_courant"], "B13": v["I_sur_PIB"] / 100.0, "B24": e["g"], "xi": 0.0}


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
def test_stationnarite_partielle(trajectoires, socle, pi, publier):
    """P67 : max sur 720 pas de |x_t/x̄ − 1| ≤ 1e−9 pour B1 à B7, B12, B13 et B24, depuis
    l'état résolu, sans choc ; P66 : une grandeur de valeur résolue nulle (B7 à π* = 0, ξ) se
    juge en valeur absolue, |x_t| ≤ 1e−12."""
    tr = trajectoires[pi]
    releves = grandeurs_b(tr)
    resolues = valeurs_resolues(socle, tr.sentier)
    pires = {}
    for cle, serie in releves.items():
        assert serie and serie[-1][0] == NB_PAS - 1
        if cle in ("B4", "B5", "B6", "B7", "B13", "B24"):
            assert serie[0][0] == PREMIER_PAS_SUR_12_TOURS
        pires[cle] = max(ecart(x, resolues[cle]) for _, x in serie)
        seuil = SEUIL_NUL if resolues[cle] == 0.0 else SEUIL_720_PAS
        assert pires[cle] <= seuil, (cle, pires[cle], resolues[cle])
    assert (resolues["B7"] == 0.0) == (pi == 0.0)
    publier(f"Stationnarité partielle (P67), π* = {100 * pi:g} %, 720 pas (π^e exogène, bloc d'essai)", [
        "max |x_t/x̄ − 1| (|x_t| si x̄ = 0, P66) : "
        + " ; ".join(f"{c} {x:.1e}" for c, x in pires.items())])


# --------------------------------------------------------------------------
# Reprise, invariance × 100, permutation d'un groupe
# --------------------------------------------------------------------------


def test_reprise_a_la_frontiere_de_tour_sous_le_schema_v2(socle):
    """D4 : sauvegarde v2 après la phase 9 du pas 359, rechargée : trajectoire, clôtures et
    états identiques au bit à ceux d'une trajectoire continue, variables des blocs comprises."""
    sentier = socle.sentier(0.02)
    o = socle.ordonnanceur(sentier)
    continu = Empreinte()
    fin_continue = socle.derouler(socle.etat_initial(sentier), NB_PAS, o, continu)
    avant, apres = Empreinte(), Empreinte()
    milieu = socle.derouler(socle.etat_initial(sentier), NB_PAS // 2, o, avant)
    document = sauvegarder([milieu])
    assert b'"version": 2' in document and b'"mu_tilde"' in document
    repris, = charger(document)
    assert repris == milieu
    fin_reprise = socle.derouler(repris, NB_PAS - NB_PAS // 2, o, apres)
    assert sauvegarder([fin_reprise]) == sauvegarder([fin_continue])
    assert avant.evenements + apres.evenements == continu.evenements


def test_invariance_sous_100_des_variables_nouvelles(socle, publier):
    """ADR 0005, point 19 ; ADR 0012, annotation du 13/11/2026, point 1.3 : sous une
    redénomination × 100 (état initial et sentier nominal × 100), W est multipliée par 100 et
    les neuf autres variables nouvelles sont inchangées, à 1e−10 relatif sur 720 pas ;
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
    # Un autre bloc de la même étape l'écrit à la place de son propriétaire.
    autre = next(r for r in socle.RADICAUX if r != v.proprietaire
                 and v.phase_ecriture in socle.etapes_du(r))
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
    reste dans le domaine 1 + π^e > 0 du schéma v2."""
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


@pytest.mark.parametrize("pi", [0.0, 0.02, 0.10])
@pytest.mark.parametrize("lambda_v", [3.0, 6.0, 1.5])
def test_linearisation_retrouve_une_valeur_propre_connue(socle, linearisation, pi, lambda_v,
                                                         publier):
    """Critère de #112 : sur un cas d'essai, la linéarisation de la carte d'un pas du moteur
    retrouve à 1e−8 des valeurs propres connues en forme fermée. Cas : le bloc d'essai de la
    production suit N1 pour v^e, demande d exogène sur le sentier, λ_v lue dans la table par la
    vue (référence 3, puis × 2 et × 0,5 par le constructeur validé) : v^e ramenée au sentier a
    la valeur propre 1 − λ_v/n_a ; chaque position, aux flux exogènes, a 1/Γ̄ ; les variables
    écrites au sentier, 0."""
    sentier = socle.sentier(pi)
    p = socle.PARAMETRES_DE_REFERENCE
    parametres = dataclasses.replace(p, production=varier(p.production, lambda_v=lambda_v))

    def n1(vue, sentier, t):
        lam = par_pas(vue.parametres.production.lambda_v)
        demande = sentier.valeur("v", socle.VOLUME, t)
        return sentier.facteurs[socle.VOLUME] * ((1.0 - lam) * vue.ouverture.v_e + lam * demande)

    o = socle.ordonnanceur(sentier, parametres, regles={"v_e": n1})
    postes = ("D_H", "D_F", "L", "B_Bk", "L_CB", "M_G", "K", "IN")
    noms = tuple(v.nom for v in schema.VARIABLES_DES_BLOCS) + postes
    carte = linearisation.carte_du_moteur(socle.etat_initial(sentier), o, noms, pi)
    assert linearisation.residu_point_fixe(carte) <= SEUIL_NUL
    valeurs = linearisation.valeurs_propres(carte)
    attendues = sorted([1.0 - lambda_v / N_A] + [1.0 / sentier.facteurs[socle.NOMINAL]]
                       * len(postes) + [0.0] * (len(noms) - len(postes) - 1), reverse=True)
    ecart_max = float(max(abs(valeurs - attendues)))
    assert ecart_max <= 1e-8
    if (pi, lambda_v) == (0.02, 3.0):
        publier("Linéarisation de la carte d'un pas (#112, point 4), π* = 2 %, λ_v = 3", [
            f"valeur propre de v^e : {valeurs[len(postes)].real:.12f} (1 − λ_v/n_a = 0,75) ; "
            f"1/Γ̄ = {1.0 / sentier.facteurs[socle.NOMINAL]:.12f} (multiplicité {len(postes)}) ; "
            f"écart maximal aux formes fermées {ecart_max:.1e} (seuil 1e−8)"])

