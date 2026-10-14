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
  testée.
"""

import os
import sys
import time
import types
from collections.abc import Callable

import pytest

from nations.moteur import ordonnanceur as ordo
from nations.moteur.parametres.cadre import CADRE
from nations.moteur.phases import PHASES
from nations.noyau import grand_livre as gl_module
from nations.observation.cout import ReleveDuCout
from nations.observation.observateur import FinDePas, ObservateurNul

pytestmark = pytest.mark.budget

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
    montants relevés pour ses lignes, déclare le montant couvert relevé et
    écrit P_t relevé ; les tables relevées sont des attributs de classe en
    lecture seule (aucun attribut d'instance).
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
    o = ordo.assembler(PHASES, blocs_rejoues(generateur, propositions, couverts, prix), CADRE,
                       generateur.DECLARATION_DES_ENTREES)
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
