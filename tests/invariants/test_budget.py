"""Invariant : budget de calcul d'au plus 1 ms par pays-semaine ; coût du noyau seul (J2).

`CLAUDE.md`, invariant 3, et `docs/exigences.md` § 4.4. Deux mesures :

- **coût du noyau seul** (critère de passage de J2, M19 ; ADR 0005, point 19 ;
  ADR 0012, E3 ; définition C98-1 de #98) : durée des appels à l'ordonnanceur,
  au noyau et au registre, sur des propositions précalculées par le
  générateur de #98 puis rejouées, divisée par 720 pas ; en ms par pas
  mensuel, pour un pays ; moyenne sur 720 pas, meilleure de 5 répétitions ;
  relevée par `nations.observation.cout.ReleveDuCout` ; seuil écrit avant
  l'essai : 0,5 ms par pas mensuel, **sur la plateforme de référence** (CI
  GitHub Actions, Linux, ADR 0003, M16), où il est contrôlé ; ailleurs, la
  mesure est publiée et le test se termine par un `skip` qui le dit ; la
  marge est publiée ;
- **budget du socle complet** (1 ms par pays-semaine) : critère du J3 (M19),
  inactif (skip) jusqu'aux premiers blocs ; la mesure elle-même est prête et
  testée ;
- **part d'un bloc dans le coût** (P57, définie avant l'essai ; synthèse du rang
  1a de J3-b, § 2) : durée cumulée des appels de l'ordonnanceur aux méthodes
  d'étape du bloc, de l'entrée au retour, instrumentée dans `tests/` seulement
  par enveloppe des méthodes déclarées ; ni l'ordonnanceur hors de ces appels,
  ni le noyau, ni le registre, ni les blocs d'essai, ni l'observateur (nul) ;
  coût du chronomètre publié, non soustrait ; socle partiel d'essai, π* = 2 %,
  n_a = 12, ν_G = 1,15, 720 pas sans choc ; part = min sur 5 répétitions de
  (Σ durées / 720), en ms par pas mensuel ; critère 0,48 ms, alerte non
  bloquante 0,2760 ms = (52/12/1,60 − 0,5)/8, verdict sur la plateforme de
  référence seulement ; projection cumulée publiée sans seuil : coût du noyau
  seul + Σ des parts mesurées + (8 − k) × 0,276, à comparer à 2,708 ms.
"""

import math
import os
import sys
import time
import types
from collections.abc import Callable

import pytest

from nations.moteur import ordonnanceur as ordo
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.moteur.phases import PHASES
from nations.noyau import grand_livre as gl_module
from nations.observation.cout import ReleveDuCout
from nations.observation.observateur import FinDePas, ObservateurNul

pytestmark = pytest.mark.budget

# Mesures du module reprises par une autre mesure du même module (coût du noyau seul,
# lu par la projection cumulée de la part des blocs) ; écrites par le test qui les mesure.
_MESURES_DU_MODULE: dict[str, float] = {}

# Budget : secondes de calcul par pays et par semaine simulée.
BUDGET_S_PAR_PAYS_SEMAINE = 1e-3
# Seuil du coût du noyau seul, en ms par pas mensuel, pour un pays (ADR 0005,
# point 19, écrit avant l'essai).
SEUIL_NOYAU_SEUL_MS_PAR_PAS = 0.5
NB_PAS_DU_COUT = 720
REPETITIONS_DU_COUT = 5
GRAINE_DU_COUT = 20261007
# Plateforme de référence des résultats (ADR 0003, M16) : exécuteur Linux de
# GitHub Actions ; l'image est consignée avec la mesure (ImageOS, ImageVersion).
PLATEFORME_DE_REFERENCE = os.environ.get("GITHUB_ACTIONS") == "true" and sys.platform == "linux"


def secondes_par_pays_semaine(
    executer_pas: Callable[[], None],
    nb_pas: int,
    nb_pays: int,
    semaines_par_pas: float,
) -> float:
    """Temps moyen de calcul par pays-semaine sur `nb_pas` pas.

    `executer_pas` déroule un pas pour `nb_pays` pays ; `semaines_par_pas`
    convertit la durée du pas en semaines (pas mensuel, M22 ;
    `docs/specification/CONVENTIONS.md` § 6).
    """
    if nb_pas <= 0 or nb_pays <= 0 or semaines_par_pas <= 0:
        raise ValueError("nb_pas, nb_pays et semaines_par_pas doivent être positifs")
    debut = time.perf_counter()
    for _ in range(nb_pas):
        executer_pas()
    duree = time.perf_counter() - debut
    return duree / (nb_pas * nb_pays * semaines_par_pas)


def test_mesure_rapporte_au_pays_semaine():
    # Un pas factice de durée connue : 2 pays, pas de 4 semaines.
    def pas_factice():
        time.sleep(0.008)

    mesure = secondes_par_pays_semaine(pas_factice, nb_pas=5, nb_pays=2, semaines_par_pas=4)
    # 8 ms par pas / (2 pays x 4 semaines) = 1 ms, au moins (sleep ne rend
    # jamais avant l'échéance) ; borne haute large pour l'ordonnanceur du système.
    assert 1e-3 <= mesure < 5e-3


def test_mesure_refuse_un_denominateur_nul():
    with pytest.raises(ValueError):
        secondes_par_pays_semaine(lambda: None, nb_pas=0, nb_pays=1, semaines_par_pas=1)


@pytest.mark.skip(
    reason="budget du socle complet : critère du jalon J3 (M19), mesuré dès les premiers "
    "blocs, avec la marge mesurée sur la plateforme de référence (ADR 0003)"
)
def test_budget_par_pays_semaine():
    # À compléter quand l'ordonnanceur existe : état initial résolu d'un
    # archétype, puis `secondes_par_pays_semaine(<pas du moteur>, ...)`
    # comparé à BUDGET_S_PAR_PAYS_SEMAINE multiplié par la marge mesurée.
    raise NotImplementedError


# --------------------------------------------------------------------------
# Coût du noyau seul (J2, #98)
# --------------------------------------------------------------------------


def propositions_du_generateur(generateur, monkeypatch, graine, nb_pas):
    """Propositions, montants couverts et indices des prix de `nb_pas` pas du générateur.

    Relevés par des espions du grand livre et dans les fins de pas, hors de
    toute mesure de temps : {t: {ligne: montants}}, {t: c}, {t: P_t}.
    """
    proposer = gl_module.GrandLivre.proposer
    declarer = gl_module.GrandLivre.declarer_montant_couvert
    propositions, couverts, prix = {}, {}, {}

    def proposer_espion(self, flux):
        proposer(self, flux)
        propositions.setdefault(self._t, {})[flux.ligne] = dict(flux.montants)

    def declarer_espion(self, ligne, montant, payeur):
        declarer(self, ligne, montant, payeur)
        couverts[self._t] = montant

    class Prix:
        def relever(self, evenement):
            if type(evenement) is FinDePas:
                prix[evenement.t] = dict(evenement.variables_du_pas)[ordo.INDICE_DES_PRIX]

    with monkeypatch.context() as m:
        m.setattr(gl_module.GrandLivre, "proposer", proposer_espion)
        m.setattr(gl_module.GrandLivre, "declarer_montant_couvert", declarer_espion)
        final = generateur.derouler(generateur.etat_initial(graine), nb_pas,
                                    generateur.ordonnanceur(), Prix())
    return propositions, couverts, prix, final


def blocs_rejoues(generateur, propositions, couverts, prix):
    """Les huit pseudo-blocs, réduits à rejouer les propositions précalculées.

    Mêmes déclarations que le générateur ; chaque méthode de phase propose les
    montants relevés pour ses lignes, déclare le montant couvert relevé, écrit
    P_t relevé et reconduit les variables d'état des blocs (schéma v2) à leur
    valeur d'ouverture, comme le générateur ; les tables relevées sont des
    attributs de classe en lecture seule (aucun attribut d'instance).
    """
    tables = types.MappingProxyType({"propositions": propositions, "couverts": couverts,
                                     "prix": prix})

    def methode(etape):
        def agir(self, vue):
            siege = self.sieges[etape]
            t = vue.ouverture.t
            du_pas = self.tables["propositions"][t]
            for ligne in siege.propose:
                vue.proposer(ligne, du_pas[ligne])
            if siege.couvre and t in self.tables["couverts"]:
                vue.declarer_montant_couvert("16", self.tables["couverts"][t])
            if ordo.INDICE_DES_PRIX in siege.ecrit:
                vue.ecrire_pas(ordo.INDICE_DES_PRIX, self.tables["prix"][t])
            # Variables d'état du schéma v2, reconduites comme par le générateur.
            for nom in siege.etat:
                vue.ecrire_etat(nom, getattr(vue.ouverture, nom))
        return agir

    blocs = []
    for classe in generateur.PSEUDO_BLOCS:
        declaration = classe.declaration
        espace = {"__slots__": (), "declaration": declaration, "tables": tables,
                  "sieges": types.MappingProxyType({s.etape: s for s in declaration.sieges})}
        for siege in declaration.sieges:
            espace[f"phase_{siege.etape}"] = methode(siege.etape)
        blocs.append(type(classe.__name__ + "Rejoue", (), espace)())
    return blocs


def test_cout_du_noyau_seul(generateur, monkeypatch, publier):
    """Coût du noyau seul ≤ 0,5 ms par pas mensuel (ADR 0005, point 19 ; C98-1) : ordonnanceur,
    noyau et registre sur 720 pas de propositions rejouées, meilleure de 5 répétitions."""
    generateur.doubler_19b(monkeypatch)
    propositions, couverts, prix, final = propositions_du_generateur(
        generateur, monkeypatch, GRAINE_DU_COUT, NB_PAS_DU_COUT)
    assert len(propositions) == NB_PAS_DU_COUT
    assert all(len(p) == 25 for p in propositions.values())
    o = ordo.assembler(PHASES, blocs_rejoues(generateur, propositions, couverts, prix),
                       PARAMETRES_DE_REFERENCE, generateur.DECLARATION_DES_ENTREES)
    initial = generateur.etat_initial(GRAINE_DU_COUT)
    entrees = [generateur.entrees(GRAINE_DU_COUT, t) for t in range(NB_PAS_DU_COUT)]
    # Le rejeu reproduit la trajectoire du générateur, bit à bit.
    etat = initial
    for t in range(NB_PAS_DU_COUT):
        etat = ordo.executer_pas(etat, entrees[t], o, ObservateurNul())
    assert etat == final
    couts = []
    for _ in range(REPETITIONS_DU_COUT):
        releve = ReleveDuCout()
        etat = initial
        releve.demarrer()
        for t in range(NB_PAS_DU_COUT):
            etat = ordo.executer_pas(etat, entrees[t], o, releve)
        assert releve.pas() == tuple(range(NB_PAS_DU_COUT))
        couts.append(releve.cout_par_pas())
    cout = min(couts)
    _MESURES_DU_MODULE["noyau_seul"] = cout
    grandeur = releve.grandeur()
    publier("Coût du noyau seul (C98-1 ; ADR 0005, point 19)", [
        f"définition : {grandeur.definition} ; ordonnanceur, noyau et registre sur des "
        "propositions précalculées puis rejouées (25 propositions par pas, plus le montant "
        "couvert les pas où la ligne 16 est négative)",
        f"unité : {grandeur.unite} ; dénominateur : {grandeur.denominateur} ; fenêtre : "
        f"{grandeur.fenetre} ; statistique : moyenne, meilleure de {REPETITIONS_DU_COUT} "
        "répétitions",
        f"C = {cout:.4f} ms par pas (répétitions : "
        + ", ".join(f"{c:.4f}" for c in couts) + ")",
        f"seuil {SEUIL_NOYAU_SEUL_MS_PAR_PAS} ms : marge {SEUIL_NOYAU_SEUL_MS_PAR_PAS - cout:.4f} "
        f"ms, rapport seuil / C = {SEUIL_NOYAU_SEUL_MS_PAR_PAS / cout:.2f}",
        "plateforme : " + (
            f"référence (GitHub Actions, {os.environ.get('ImageOS', '?')} "
            f"{os.environ.get('ImageVersion', '?')}), seuil contrôlé" if PLATEFORME_DE_REFERENCE
            else "hors référence (ADR 0003, M16), seuil non contrôlé"),
    ])
    if not PLATEFORME_DE_REFERENCE:
        verdict = "≤" if cout <= SEUIL_NOYAU_SEUL_MS_PAR_PAS else ">"
        pytest.skip(f"C = {cout:.4f} ms {verdict} {SEUIL_NOYAU_SEUL_MS_PAR_PAS} ms, hors référence : "
                    "seuil du coût du noyau seul contrôlé sur la plateforme de référence seulement "
                    "(CI GitHub Actions, ADR 0003, M16) ; mesure publiée")
    assert cout <= SEUIL_NOYAU_SEUL_MS_PAR_PAS


# --------------------------------------------------------------------------
# Part d'un bloc dans le coût (P57, #112)
# --------------------------------------------------------------------------

# Critère et alerte de la part d'un bloc, en ms par pas mensuel (P57, écrits avant l'essai).
SEUIL_PART_MS_PAR_PAS = 0.48
ALERTE_PART_MS_PAR_PAS = 0.2760
# Budget du socle complet en ms par pas mensuel, marge m = 0,60 comprise (#105, #107).
BUDGET_DU_SOCLE_MS_PAR_PAS = 2.708
NB_BLOCS_DU_SOCLE = 8
PI_DE_LA_PART = 0.02


def envelopper(bloc, durees: list) -> object:
    """Le bloc, dont chaque méthode d'étape déclarée est enveloppée d'un chronomètre qui ajoute
    à `durees[0]` la durée de l'appel, de l'entrée au retour, et compte l'appel dans
    `durees[1]` ; sous-classe sans attribut d'instance (`__slots__` vide), même déclaration."""
    classe = type(bloc)
    espace = {"__slots__": ()}
    for siege in bloc.declaration.sieges:
        nom = f"phase_{siege.etape}"

        def chronometre(self, vue, _methode=getattr(classe, nom)):
            debut = time.perf_counter()
            try:
                _methode(self, vue)
            finally:
                durees[0] += time.perf_counter() - debut
                durees[1] += 1
        espace[nom] = chronometre
    return type(classe.__name__ + "Chronometre", (classe,), espace)()


def mesurer_part(socle, radical: str, reels=()) -> tuple[float, list[float], int]:
    """Part du bloc `radical` (ms par pas, min sur 5 répétitions de Σ durées / 720), ses
    répétitions et le nombre d'appels par répétition, sur le socle partiel d'essai à π* = 2 %
    où les blocs réels `reels` remplacent les blocs d'essai de leur radical."""
    sentier = socle.sentier(PI_DE_LA_PART)
    parts, appels = [], None
    for _ in range(REPETITIONS_DU_COUT):
        durees = [0.0, 0]
        blocs = socle.blocs(sentier, reels=reels)
        blocs = tuple(envelopper(b, durees) if b.declaration.radical == radical else b
                      for b in blocs)
        o = ordo.assembler(PHASES, blocs, PARAMETRES_DE_REFERENCE, socle.SANS_ENTREES)
        socle.derouler(socle.etat_initial(sentier), NB_PAS_DU_COUT, o, ObservateurNul())
        parts.append(durees[0] * 1e3 / NB_PAS_DU_COUT)
        appels = durees[1]
    return min(parts), parts, appels


def cout_du_chronometre_par_appel(nb: int = 100_000) -> float:
    """Durée relevée par le chronomètre autour d'un appel vide, en ms (moyenne sur `nb` appels,
    meilleure de 5) : coût publié, non soustrait (P57)."""
    meilleur = math.inf
    for _ in range(REPETITIONS_DU_COUT):
        durees = [0.0, 0]

        class Vide:
            __slots__ = ()

            def phase_0(self, vue):
                return None

        Vide.declaration = types.SimpleNamespace(sieges=(types.SimpleNamespace(etape="0"),))
        bloc = envelopper(Vide(), durees)
        for _ in range(nb):
            bloc.phase_0(None)
        meilleur = min(meilleur, durees[0] * 1e3 / nb)
    return meilleur


def test_instrument_de_la_part_d_un_bloc(socle, publier):
    """L'enveloppe ne change pas la trajectoire (états identiques au bit) et compte chaque appel
    d'étape du bloc une fois : 720 × nombre de sièges ; la part est positive et au plus le coût
    du pas entier. Mesure de contrôle sur un bloc d'essai (production), sans verdict."""
    sentier = socle.sentier(PI_DE_LA_PART)
    durees = [0.0, 0]
    blocs = tuple(envelopper(b, durees) if b.declaration.radical == "production" else b
                  for b in socle.blocs(sentier))
    o = ordo.assembler(PHASES, blocs, PARAMETRES_DE_REFERENCE, socle.SANS_ENTREES)
    debut = time.perf_counter()
    fin = socle.derouler(socle.etat_initial(sentier), NB_PAS_DU_COUT, o, ObservateurNul())
    total = time.perf_counter() - debut
    reference = socle.derouler(socle.etat_initial(sentier), NB_PAS_DU_COUT,
                               socle.ordonnanceur(sentier), ObservateurNul())
    assert fin == reference
    nb_sieges = len(socle.declaration_d_essai("production").sieges)
    assert durees[1] == NB_PAS_DU_COUT * nb_sieges
    assert 0.0 < durees[0] <= total
    part, parts, _ = mesurer_part(socle, "production")
    chrono = cout_du_chronometre_par_appel()
    publier("Part d'un bloc dans le coût : instrument (P57), bloc d'essai de la production", [
        f"part du bloc d'essai (contrôle de l'instrument, sans verdict) : {part:.4f} ms par pas "
        "(répétitions : " + ", ".join(f"{x:.4f}" for x in parts) + ")",
        f"coût du chronomètre : {chrono * 1e3:.3f} µs par appel, {nb_sieges} appels par pas, soit "
        f"{chrono * nb_sieges:.4f} ms par pas, publié, non soustrait",
    ])


def test_part_de_chaque_bloc_reel(socle, publier):
    """P57 : part de chaque bloc réel de `src/nations/blocs/` ≤ 0,48 ms par pas mensuel
    (alerte non bloquante au-dessus de 0,2760 ms) sur la plateforme de référence ; projection
    cumulée publiée sans seuil. Avant le premier bloc réel (#113), la mesure est publiée vide
    et le test se termine par un saut qui le dit."""
    reels = socle.blocs_reels()
    lignes, parts = [], {}
    for bloc in reels:
        radical = bloc.declaration.radical
        part, repetitions, appels = mesurer_part(socle, radical, reels)
        parts[radical] = part
        alerte = " ; ALERTE (> 0,2760 ms, non bloquante)" if part > ALERTE_PART_MS_PAR_PAS else ""
        lignes.append(f"{radical} : {part:.4f} ms par pas (répétitions : "
                      + ", ".join(f"{x:.4f}" for x in repetitions)
                      + f" ; {appels // NB_PAS_DU_COUT} appels par pas){alerte}")
    k = len(parts)
    noyau = _MESURES_DU_MODULE.get("noyau_seul")
    if noyau is None:
        projection = "coût du noyau seul non mesuré dans cette session : projection non publiée"
    else:
        total = noyau + sum(parts.values()) + (NB_BLOCS_DU_SOCLE - k) * ALERTE_PART_MS_PAR_PAS
        projection = (f"projection cumulée = {noyau:.4f} (noyau seul) + {sum(parts.values()):.4f} "
                      f"(Σ des {k} parts) + {NB_BLOCS_DU_SOCLE - k} × {ALERTE_PART_MS_PAR_PAS} = "
                      f"{total:.4f} ms par pas, à comparer à {BUDGET_DU_SOCLE_MS_PAR_PAS} ms "
                      "(sans seuil)")
    publier("Part de chaque bloc réel dans le coût (P57)", [
        "définition : durée cumulée des appels aux méthodes d'étape du bloc, socle partiel "
        "d'essai, π* = 2 %, 720 pas, min sur 5 répétitions ; ms par pas mensuel",
        *(lignes or ["aucun bloc réel dans src/nations/blocs/"]),
        projection,
        "plateforme : " + ("référence, critère contrôlé" if PLATEFORME_DE_REFERENCE
                           else "hors référence (ADR 0003, M16), critère non contrôlé"),
    ])
    if not reels:
        pytest.skip("aucun bloc réel dans src/nations/blocs/ : part d'un bloc mesurée dès le "
                    "premier (#113) ; mesure publiée")
    if not PLATEFORME_DE_REFERENCE:
        pytest.skip("part d'un bloc contrôlée sur la plateforme de référence seulement (CI "
                    "GitHub Actions, ADR 0003, M16) ; mesure publiée")
    for radical, part in parts.items():
        assert part <= SEUIL_PART_MS_PAR_PAS, radical

