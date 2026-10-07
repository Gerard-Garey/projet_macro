"""Grand livre d'un pays : ouvrir un pas, proposer un flux, clore une phase.

Contrat : ADR 0012, A2 à A5 (interface étroite, règlement dérivé, identités)
et A7 (scalaires Python en double précision). Le grand livre est le **seul
endroit où un flux monétaire s'exécute**. Trois opérations d'écriture :

- `ouvrir_pas(etat_ouverture, parametres_cadre) → GrandLivre` (phase 0), seul
  constructeur du grand livre : copie le pas t (entier), les onze positions
  et les cinq V^flux de l'état d'ouverture, évalue l'échelle S de chaque
  secteur **une fois** (P33 (a)) et contrôle les domaines de l'état chargé
  (S finie et > 0 ; Res ≥ 0 ; D_H, D_F, M^G ≥ −ε × S) ;
- `proposer(flux)` et `declarer_montant_couvert(ligne, montant, payeur)` :
  enregistrent, sans rien exécuter ;
- `clore_phase(phase) → ClotureDePhase` : exécute les propositions de la phase
  dans l'**ordre canonique du catalogue** (lignes, puis termes, puis postes),
  quel que soit l'ordre d'arrivée, règle chaque terme le long de l'arbre des
  comptes, dérive les contreparties 17, 20 et 22, puis vérifie les identités.
  Une clôture sans ligne (aucune ligne du catalogue dans sa phase) ne change
  aucune position : ses contrôles par phase sont sautés, et la clôture rendue
  est égale à celle d'un calcul complet ; la couche noyau de la phase 9 n'est
  jamais sautée (ADR 0012, annotation du 07/10/2026, point 6).

Les lectures sont seules publiques ; aucune méthode n'affecte un poste, et
toute affectation d'attribut est refusée (`RefusDeProposition`). Un refus
d'appel laisse le grand livre inchangé. Après un défaut ou un refus levé à la
clôture, le grand livre est arrêté : il refuse tout appel, et aucun état
t + 1 n'est assemblé. Le grand livre ne survit pas au pas : `clore_pas` rend
les variables d'état du noyau pour l'assemblage de l'état t + 1.

Le noyau ne convertit aucun taux et ne lit pas n_a : les montants lui arrivent
en u.m. par pas, convertis par les blocs.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Protocol

from nations.noyau import identites as idt
from nations.noyau.catalogue import (
    COLONNE_DE_RESULTAT,
    COLONNES,
    CONTREPARTIES,
    COUPLES_MONTANT_COUVERT,
    LIGNE,
    LIGNES,
    LIGNES_A_MONTANT_COUVERT,
    LIGNES_DE_LA_PHASE,
    NOMS_POSTES,
    PHASES,
    POSTES,
    POSTES_MONNAIE,
    POSTES_MONNAIE_CENTRALE,
    SECTEUR_DE_COLONNE,
    SECTEURS,
    SIGNATURE_DU_MOYEN,
    VALEUR_NETTE_FLUX,
    Ligne,
)
from nations.noyau.diagnostics import ArretNoyau, DefautComptable, RefusDeProposition

# Moyens de paiement, dans l'ordre des contreparties de règlement (17, 20, 22).
MOYENS_DE_PAIEMENT = tuple(t.poste_regle for ligne in CONTREPARTIES for t in ligne.termes)
# Objets des diagnostics des sommes de colonnes, dans l'ordre de SECTEURS.
_OBJETS_SECTEURS = [(s, None, None) for s in SECTEURS]
# Dernière clôture qui exécute des lignes : les contreparties de règlement,
# cumulées sur le pas, se lisent après elle.
_DERNIERE_EXECUTION = "8c"
# Postes des deux identités de la monnaie, dont la variation sur le pas est
# contrôlée en phase 9.
_POSTES_DES_PORTES = POSTES_MONNAIE + POSTES_MONNAIE_CENTRALE
# Rapport d'une famille sans instance, ou dont toutes les instances sont nulles.
_RAPPORT_NUL = ("", 0.0)


def _sans_ligne(phase: str) -> bool:
    """Prédicat structurel d'une clôture sans ligne : aucune ligne du catalogue dans la phase."""
    return not LIGNES_DE_LA_PHASE[phase]


def _echelle_de_ligne(cellules: Mapping[str, float], echelles: Mapping[str, float]) -> float:
    """Échelle d'une ligne (point 9, lecture (α)) : plus petit S des secteurs qui y ont un
    montant non nul ; aucun : 0, et le résidu doit alors être nul."""
    echelle = math.inf
    for colonne, v in cellules.items():
        if v != 0.0:
            echelle = min(echelle, echelles[SECTEUR_DE_COLONNE[colonne]])
    return 0.0 if echelle == math.inf else echelle


def _cellules_de_resultat(ligne: Ligne) -> tuple[tuple[str, tuple[tuple[str, float], ...]], ...]:
    """(secteur, ((terme, ±1), …)) pour chaque secteur dont la colonne de résultat porte un
    terme de la ligne, dans l'ordre de SECTEURS puis des termes."""
    cellules = []
    for s in SECTEURS:
        colonne = COLONNE_DE_RESULTAT[s]
        coefficients = tuple((t.nom, 1.0 if t.colonne_plus == colonne else -1.0)
                             for t in ligne.termes if colonne in (t.colonne_plus, t.colonne_moins))
        if coefficients:
            cellules.append((s, coefficients))
    return tuple(cellules)


# Contreparties de règlement, décrites une fois : identifiant, et pour chaque
# terme (nom, moyen de paiement réglé, colonnes + et −, signature du moyen).
_TERMES_DES_CONTREPARTIES = tuple(
    (ligne.identifiant, tuple((t.nom, t.poste_regle, t.colonne_plus, t.colonne_moins,
                               SIGNATURE_DU_MOYEN[t.poste_regle]) for t in ligne.termes))
    for ligne in CONTREPARTIES)

# Cellules de résultat des lignes 1 à 16, dans l'ordre canonique : V^flux s'en
# déduit en phase 9 sans reconstruire les six colonnes de chaque ligne.
_CELLULES_DE_RESULTAT = tuple((ligne.identifiant, _cellules_de_resultat(ligne))
                              for ligne in LIGNES if ligne.resultat)


class EtatOuverture(Protocol):
    """Ce que le noyau lit de l'état d'ouverture (schéma complet : #96).

    `t`, les onze positions (noms de `catalogue.NOMS_POSTES`) et les cinq
    V^flux (noms de `catalogue.VALEUR_NETTE_FLUX`), en `float`.
    """

    t: int


class ParametresCadre(Protocol):
    """Les deux tolérances du cadre, sans dimension (paramètres typés : #97)."""

    tolerance_identite_pas: float
    tolerance_identite_cumulee: float


@dataclass(frozen=True, slots=True)
class FluxPropose:
    """Un flux proposé, immuable : ligne, montant de chaque terme, proposant.

    Le proposant est le radical du bloc, apposé par la vue du bloc (ADR 0012,
    A2 et B2). Les montants sont en u.m. par pas, nommés par les termes de la
    ligne (`catalogue.Terme.nom`).
    """

    ligne: str
    montants: Mapping[str, float]
    proposant: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "montants", MappingProxyType(dict(self.montants)))


@dataclass(frozen=True, slots=True)
class ClotureDePhase:
    """Valeur immuable décrivant une clôture (destinée à `observation/`).

    - `rapports` : pour chaque règle vérifiée, (règle, objet, |résidu| / S) de
      l'instance la plus éloignée de zéro (objet vide si toutes sont nulles) ;
      en phase 9, s'y ajoutent une entrée par secteur pour l'identité cumulée
      et une pour ΔM et ΔH du pas ;
    - `montants` : montants exécutés dans la phase, par ligne et par terme,
      contreparties de règlement de la phase comprises ; vide pour une clôture
      sans ligne.
    """

    t: int
    phase: str
    rapports: tuple[tuple[str, str, float], ...]
    montants: tuple[tuple[str, tuple[tuple[str, float], ...]], ...]


@dataclass(frozen=True, slots=True)
class ClotureDuPas:
    """Variables d'état du noyau au pas t + 1 : onze positions et cinq V^flux."""

    t: int
    variables: Mapping[str, float]


def _verifier_tolerance(nom: str, valeur: object) -> float:
    """Une tolérance reçue est un `float` fini strictement positif ; refus sinon."""
    if type(valeur) is not float or not math.isfinite(valeur) or not idt.controle_de_signe(
            valeur, idt.TOLERANCE_POSITIVE, 0.0, 0.0):
        raise RefusDeProposition(f"tolérance {nom} hors domaine : {valeur!r}",
                                 regle=idt.TOLERANCE_POSITIVE.nom)
    return valeur


def ouvrir_pas(etat_ouverture: EtatOuverture, parametres_cadre: ParametresCadre) -> GrandLivre:
    """Ouvre le pas (phase 0) : lecture figée de l'état, échelles, domaines de l'état chargé."""
    epsilon = _verifier_tolerance("ε", parametres_cadre.tolerance_identite_pas)
    epsilon_v = _verifier_tolerance("ε_V", parametres_cadre.tolerance_identite_cumulee)
    t = etat_ouverture.t
    if type(t) is not int:
        raise RefusDeProposition(f"pas t : entier attendu, {t!r} lu", phase="0")
    ouverture = {}
    for nom in NOMS_POSTES:
        valeur = getattr(etat_ouverture, nom)
        if type(valeur) is not float or not math.isfinite(valeur):
            raise RefusDeProposition(f"position {nom} : float fini attendu, {valeur!r} lu",
                                     t=t, phase="0", terme=nom)
        ouverture[nom] = valeur
    v_flux = {}
    for s in SECTEURS:
        valeur = getattr(etat_ouverture, VALEUR_NETTE_FLUX[s])
        if type(valeur) is not float or not math.isfinite(valeur):
            raise RefusDeProposition(f"{VALEUR_NETTE_FLUX[s]} : float fini attendu, {valeur!r} lu",
                                     t=t, phase="0", secteur=s)
        v_flux[s] = valeur
    echelles = {}
    for s in SECTEURS:
        echelle = idt.echelle_bilan(ouverture, s)
        # Condition de domaine à l'ouverture (ADR 0012, A3.1 (ii), point 11 ;
        # annotation du 07/10/2026, point 5) : S finie et > 0. Une échelle
        # nulle, infinie ou non définie est un défaut, jamais un repli.
        if not math.isfinite(echelle) or not idt.controle_de_signe(
                echelle, idt.ECHELLE, epsilon, echelle):
            raise DefautComptable("échelle du bilan nulle, infinie ou non définie à l'ouverture",
                                  t=t, phase="0", regle=idt.ECHELLE.nom, secteur=s,
                                  echelle=echelle)
        echelles[s] = echelle
    # Domaines de l'état chargé, avant la phase 1 (critère 17 de #95) : à t = 0,
    # à la reprise et à chaque pas.
    if not idt.controle_de_signe(ouverture["Res"], idt.RESERVES_CLOTURE, epsilon,
                                 echelles["banque"]):
        raise DefautComptable("réserves d'ouverture négatives", t=t, phase="0",
                              regle=idt.RESERVES_CLOTURE.nom, secteur="banque", moyen="Res",
                              residu=ouverture["Res"], echelle=echelles["banque"])
    idt.verifier_caisse(ouverture, echelles, epsilon, t=t, phase="0", positions_debut=ouverture,
                        mouvements_par_ligne={})
    return _construire(t, epsilon, epsilon_v, ouverture, v_flux, echelles)


def _construire(t: int, epsilon: float, epsilon_v: float, ouverture: dict[str, float],
                v_flux: dict[str, float], echelles: dict[str, float]) -> GrandLivre:
    """Constructeur privé, appelé par `ouvrir_pas` seul, après les contrôles de domaine."""
    livre = object.__new__(GrandLivre)
    poser = object.__setattr__
    poser(livre, "_t", t)
    poser(livre, "_epsilon", epsilon)
    poser(livre, "_epsilon_v", epsilon_v)
    poser(livre, "_ouverture", MappingProxyType(dict(ouverture)))
    poser(livre, "_positions", dict(ouverture))
    poser(livre, "_cumul", dict.fromkeys(NOMS_POSTES, 0.0))
    poser(livre, "_echelles", MappingProxyType(dict(echelles)))
    poser(livre, "_v_flux", MappingProxyType(dict(v_flux)))
    poser(livre, "_v_flux_suivant", {})
    poser(livre, "_propositions", {})
    poser(livre, "_declarations", {})
    poser(livre, "_executes", {})
    poser(livre, "_rang", 0)
    poser(livre, "_arrete", False)
    poser(livre, "_clos", False)
    # Rapport de `eq:noyau-cloture-poste` à la dernière clôture : une clôture
    # sans ligne le reprend, ses positions et ses cumuls étant inchangés. À
    # l'ouverture, positions = ouverture et cumuls nuls : résidus exactement nuls.
    poser(livre, "_rapport_poste", _RAPPORT_NUL)
    # Échelles des contrôles groupés : S de chaque secteur ; pour chaque
    # poste, le plus petit S des deux bilans qui le tiennent, et ce bilan.
    poser(livre, "_echelles_secteurs", [echelles[s] for s in SECTEURS])
    echelles_postes, objets_postes = [], []
    for poste in POSTES:
        bilan = poste.detenteur
        if poste.emetteur is not None and echelles[poste.emetteur] < echelles[bilan]:
            bilan = poste.emetteur
        echelles_postes.append(echelles[bilan])
        objets_postes.append((bilan, None, poste.nom))
    poser(livre, "_echelles_postes", echelles_postes)
    poser(livre, "_objets_postes", objets_postes)
    return livre


class GrandLivre:
    """Grand livre d'un pays pour un pas ; construit par `ouvrir_pas` seul.

    L'appel direct de la classe est refusé : il contournerait les contrôles de
    domaine de l'ouverture (ADR 0012, annotation du 07/10/2026, point 5).
    """

    __slots__ = (
        "_arrete",
        "_clos",
        "_cumul",
        "_declarations",
        "_echelles",
        "_echelles_postes",
        "_echelles_secteurs",
        "_epsilon",
        "_epsilon_v",
        "_executes",
        "_objets_postes",
        "_ouverture",
        "_positions",
        "_propositions",
        "_rang",
        "_rapport_poste",
        "_t",
        "_v_flux",
        "_v_flux_suivant",
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise RefusDeProposition("grand livre construit uniquement par ouvrir_pas")

    def __setattr__(self, nom: str, valeur: object) -> None:
        raise RefusDeProposition(
            f"affectation de « {nom} » refusée : un poste ne change que par une ligne de flux "
            "nommée, exécutée à la clôture de sa phase")

    def __delattr__(self, nom: str) -> None:
        raise RefusDeProposition(f"suppression de « {nom} » refusée")

    # ------------------------------------------------------------------
    # Contrôles d'appel
    # ------------------------------------------------------------------

    def _phase_courante(self) -> str:
        """Phase ouverte aux propositions ; refus si le pas est arrêté ou clos."""
        if self._arrete:
            raise RefusDeProposition("grand livre arrêté par un diagnostic : aucun appel admis",
                                     t=self._t)
        if self._clos or self._rang == len(PHASES):
            raise RefusDeProposition("pas déjà clos : aucune phase ouverte", t=self._t)
        return PHASES[self._rang]

    def phase_courante(self) -> str:
        """Phase dont la clôture est la prochaine (de `"1"` à `"9"`)."""
        return self._phase_courante()

    def _refus(self, message: str, **champs: object) -> RefusDeProposition:
        return RefusDeProposition(message, t=self._t, **champs)

    def _controler_part(self, identifiant: str, phase: str, flux: FluxPropose,
                        couvert: float) -> None:
        """Domaine du montant couvert face au montant proposé (ADR 0012, A3.2).

        Appelé au second des deux appels, avant tout enregistrement : un refus
        laisse le grand livre inchangé.
        """
        montant = 0.0
        for v in flux.montants.values():
            montant += v
        if not idt.controle_de_signe(montant, idt.PERTE, self._epsilon, 0.0):
            raise self._refus("montant couvert déclaré sur une ligne 16 non négative",
                              phase=phase, ligne=identifiant, regle=idt.PERTE.nom,
                              residu=montant)
        if not idt.controle_de_signe(-montant - couvert, idt.MONTANT_COUVERT_AU_PLUS_LA_PERTE,
                                     self._epsilon, 0.0):
            raise self._refus("montant couvert supérieur à la perte |Π| : refusé, jamais écrêté",
                              phase=phase, ligne=identifiant,
                              regle=idt.MONTANT_COUVERT_AU_PLUS_LA_PERTE.nom, residu=couvert)

    # ------------------------------------------------------------------
    # Écritures
    # ------------------------------------------------------------------

    def proposer(self, flux: FluxPropose) -> None:
        """Enregistre un flux proposé pour la phase courante, ou le refuse."""
        phase = self._phase_courante()
        identifiant = flux.ligne
        if identifiant not in LIGNE:
            raise self._refus("ligne inconnue du catalogue", phase=phase, ligne=identifiant)
        ligne = LIGNE[identifiant]
        if ligne.contrepartie:
            raise self._refus("contrepartie de règlement : dérivée par le noyau, jamais proposée",
                              phase=phase, ligne=identifiant)
        if ligne.proposant is None:
            raise self._refus("ligne sans proposant au socle", phase=phase, ligne=identifiant,
                              secteur=flux.proposant)
        if flux.proposant != ligne.proposant:
            raise self._refus(f"proposant {flux.proposant!r} au lieu de {ligne.proposant!r}",
                              phase=phase, ligne=identifiant, secteur=flux.proposant)
        if ligne.phase != phase:
            precision = " ; aucun flux en phase 9" if phase == "9" else ""
            raise self._refus(f"ligne de la phase {ligne.phase}, proposée en phase {phase}"
                              + precision, phase=phase, ligne=identifiant)
        if identifiant in self._propositions:
            raise self._refus("seconde proposition de la ligne dans le pas", phase=phase,
                              ligne=identifiant, secteur=flux.proposant)
        attendus = [t.nom for t in ligne.termes]
        for nom in attendus:
            if nom not in flux.montants:
                raise self._refus("terme manquant", phase=phase, ligne=identifiant, terme=nom)
        for nom in flux.montants:
            if nom not in attendus:
                raise self._refus("terme en trop", phase=phase, ligne=identifiant, terme=nom)
        for nom in attendus:
            x = flux.montants[nom]
            if type(x) is not float or not math.isfinite(x):
                raise self._refus(f"montant {x!r} : float fini attendu", phase=phase,
                                  ligne=identifiant, terme=nom)
            if not ligne.admet_negatif and not idt.controle_de_signe(
                    x, idt.SENS_DU_MONTANT, self._epsilon, 0.0):
                raise self._refus("montant négatif sur une ligne qui ne l'admet pas",
                                  phase=phase, ligne=identifiant, terme=nom,
                                  regle=idt.SENS_DU_MONTANT.nom, residu=x)
        if identifiant in self._declarations:
            self._controler_part(identifiant, phase, flux, self._declarations[identifiant][0])
        self._propositions[identifiant] = flux

    def declarer_montant_couvert(self, ligne: str, montant: float, payeur: str) -> None:
        """Le bloc payeur déclare le montant couvert c d'une ligne négative (ADR 0012, A3.2).

        Admis pour la seule liste fermée des couples (ligne, payeur), dans la
        phase de la ligne, une fois, avec 0 ≤ c ≤ |Π| et Π < 0 ; le domaine
        face à Π est contrôlé au second des deux appels, quel que soit l'ordre.
        Le noyau exécutera −c, sans calculer ni la part ni la couverture. La
        déclaration est obligatoire quand la ligne proposée est strictement
        négative : son absence est un refus à la clôture de la phase.
        """
        phase = self._phase_courante()
        if (ligne, payeur) not in COUPLES_MONTANT_COUVERT:
            raise self._refus("couple (ligne, payeur) hors de la liste fermée des montants "
                              "couverts", phase=phase, ligne=ligne, secteur=payeur)
        if LIGNE[ligne].phase != phase:
            raise self._refus(f"montant couvert déclaré en phase {phase}, ligne de la phase "
                              f"{LIGNE[ligne].phase}", phase=phase, ligne=ligne, secteur=payeur)
        if ligne in self._declarations:
            raise self._refus("seconde déclaration du montant couvert", phase=phase, ligne=ligne,
                              secteur=payeur)
        if type(montant) is not float or not math.isfinite(montant):
            raise self._refus(f"montant couvert {montant!r} : float fini attendu", phase=phase,
                              ligne=ligne, secteur=payeur)
        if not idt.controle_de_signe(montant, idt.MONTANT_COUVERT, self._epsilon, 0.0):
            raise self._refus("montant couvert négatif : refusé, jamais écrêté", phase=phase,
                              ligne=ligne, secteur=payeur, regle=idt.MONTANT_COUVERT.nom,
                              residu=montant)
        if ligne in self._propositions:
            self._controler_part(ligne, phase, self._propositions[ligne], montant)
        self._declarations[ligne] = (montant, payeur)

    def clore_phase(self, phase: str) -> ClotureDePhase:
        """Exécute la phase, vérifie ses identités et rend sa clôture (ADR 0012, A3.3)."""
        attendue = self._phase_courante()
        if phase != attendue:
            raise self._refus(f"clôture de la phase {phase} demandée, phase {attendue} attendue",
                              phase=attendue)
        try:
            cloture = self._executer(phase)
        except ArretNoyau:
            object.__setattr__(self, "_arrete", True)
            raise
        object.__setattr__(self, "_rang", self._rang + 1)
        return cloture

    def clore_pas(self) -> ClotureDuPas:
        """Variables d'état du noyau au pas t + 1, après la clôture de la phase 9."""
        if self._arrete:
            raise self._refus("grand livre arrêté par un diagnostic : aucun état t + 1")
        if self._clos or self._rang != len(PHASES):
            raise self._refus("pas non clos : la phase 9 doit être close avant l'assemblage")
        object.__setattr__(self, "_clos", True)
        variables = {nom: self._positions[nom] for nom in NOMS_POSTES}
        for s in SECTEURS:
            variables[VALEUR_NETTE_FLUX[s]] = self._v_flux_suivant[s]
        return ClotureDuPas(self._t + 1, MappingProxyType(variables))

    # ------------------------------------------------------------------
    # Exécution et identités
    # ------------------------------------------------------------------

    def _executer(self, phase: str) -> ClotureDePhase:
        t = self._t
        if _sans_ligne(phase):
            # Clôture sans ligne : aucune position ne change. Ses rapports sont
            # ceux d'un calcul complet (familles vides ou résidus nuls ; clôture
            # des postes reprise de la dernière clôture), et sa caisse est celle
            # de la dernière clôture, déjà contrôlée.
            rapports = [
                (idt.SOMME_LIGNE.nom, *_RAPPORT_NUL),
                (idt.SOMME_COLONNE.nom, *_RAPPORT_NUL),
                (idt.CLOTURE_POSTE.nom, *self._rapport_poste),
                (idt.VARIATION_MONNAIE.nom, *_RAPPORT_NUL),
                (idt.VARIATION_MONNAIE_CENTRALE.nom, *_RAPPORT_NUL),
            ]
            if phase == "9":
                rapports.extend(self._couche_noyau())
            return ClotureDePhase(t, phase, tuple(rapports), ())
        eps = self._epsilon
        echelles = self._echelles
        positions = self._positions
        cumul = self._cumul
        lignes = LIGNES_DE_LA_PHASE[phase]
        # Ligne oubliée : refus à la clôture de sa phase, jamais un zéro implicite.
        # Ligne strictement négative à montant couvert non déclaré : même refus
        # (ADR 0012, annotation du 07/10/2026, point 2 ; prédicat de PERTE).
        for ligne in lignes:
            identifiant = ligne.identifiant
            if ligne.proposant is not None and identifiant not in self._propositions:
                raise self._refus("ligne non proposée dans sa phase (une proposition nulle est "
                                  "explicite)", phase=phase, ligne=identifiant,
                                  secteur=ligne.proposant)
            if identifiant in LIGNES_A_MONTANT_COUVERT and identifiant not in self._declarations:
                montant = 0.0
                for v in self._propositions[identifiant].montants.values():
                    montant += v
                if idt.controle_de_signe(montant, idt.PERTE, eps, 0.0):
                    raise self._refus("ligne strictement négative sans déclaration du montant "
                                      "couvert (déclaration obligatoire)", phase=phase,
                                      ligne=identifiant, regle=idt.PERTE.nom, residu=montant)
        debut = {moyen: positions[moyen] for moyen in MOYENS_DE_PAIEMENT}
        colonnes = dict.fromkeys(COLONNES, 0.0)
        reglement_phase = dict.fromkeys(MOYENS_DE_PAIEMENT, 0.0)
        mouvements_par_ligne = {}
        montants_phase = []
        # Résidus des identités de ligne, contrôlés par famille après l'exécution.
        r_ligne, s_ligne, o_ligne = [], [], []
        r_porte_m, r_porte_h = [], []
        for ligne in lignes:
            identifiant = ligne.identifiant
            if ligne.proposant is None:
                # 19b : aucun proposant au socle, rien n'est exécuté.
                self._executes[identifiant] = {t_.nom: 0.0 for t_ in ligne.termes}
                continue
            proposes = self._propositions[identifiant].montants
            if identifiant in self._declarations:
                # Montant couvert c : le noyau exécute −c (ligne à un terme).
                executes = {ligne.termes[0].nom: -self._declarations[identifiant][0]}
            else:
                executes = {t_.nom: proposes[t_.nom] for t_ in ligne.termes}
            cellules: dict[str, float] = {}
            mouvements: dict[str, float] = {}
            montant = 0.0
            for terme in ligne.termes:
                x = executes[terme.nom]
                montant += x
                plus, moins = terme.colonne_plus, terme.colonne_moins
                cellules[plus] = cellules[plus] + x if plus in cellules else x
                cellules[moins] = cellules[moins] - x if moins in cellules else -x
                for poste, c in terme.variations:
                    positions[poste] += c * x
                    cumul[poste] += c * x
                for poste, c in terme.reglement:
                    positions[poste] += c * x
                    cumul[poste] += c * x
                    mouvements[poste] = mouvements[poste] + c * x if poste in mouvements \
                        else c * x
            self._executes[identifiant] = executes
            montants_phase.append((identifiant, tuple(executes.items())))
            mouvements_par_ligne[identifiant] = mouvements
            r_ligne.append(idt.residu_somme_ligne(cellules))
            s_ligne.append(_echelle_de_ligne(cellules, echelles))
            o_ligne.append((None, identifiant, None))
            # Portes à l'exécution, ligne par ligne, montant signé (M95-2).
            signe_et_montant = ((ligne.signature, montant),)
            r_porte_m.append(idt.residu_variation_monnaie(signe_et_montant, mouvements))
            r_porte_h.append(idt.residu_variation_monnaie_centrale(signe_et_montant, mouvements))
            for colonne, v in cellules.items():
                colonnes[colonne] += v
            for poste, m in mouvements.items():
                reglement_phase[poste] += m
        # Contreparties de règlement (17, 20, 22), routées depuis les mouvements
        # des moyens de paiement, jamais calculées comme reste d'une colonne.
        # Leurs portes comparent leur montant, lu « poste » (SIGNATURE_DU_MOYEN),
        # à la variation de leurs moyens de paiement sur la phase. Dans un
        # calcul complet d'une clôture sans ligne, elles n'ont aucun montant.
        if lignes:
            executes_du_pas = self._executes
            for identifiant, termes in _TERMES_DES_CONTREPARTIES:
                if identifiant not in executes_du_pas:
                    executes_du_pas[identifiant] = {nom: 0.0 for nom, *_ in termes}
                cumuls = executes_du_pas[identifiant]
                cellules = {}
                du_pas = []
                signes_et_montants = []
                variations = {}
                for nom, poste, plus, moins, signature in termes:
                    m = reglement_phase[poste]
                    cumuls[nom] += m
                    du_pas.append((nom, m))
                    signes_et_montants.append((signature, m))
                    variations[poste] = positions[poste] - debut[poste]
                    cellules[plus] = cellules[plus] + m if plus in cellules else m
                    cellules[moins] = cellules[moins] - m if moins in cellules else -m
                    colonnes[plus] += m
                    colonnes[moins] -= m
                montants_phase.append((identifiant, tuple(du_pas)))
                r_ligne.append(idt.residu_somme_ligne(cellules))
                s_ligne.append(_echelle_de_ligne(cellules, echelles))
                o_ligne.append((None, identifiant, None))
                r_porte_m.append(idt.residu_variation_monnaie(signes_et_montants, variations))
                r_porte_h.append(idt.residu_variation_monnaie_centrale(signes_et_montants, variations))
        rapports = []
        rapports.append((idt.SOMME_LIGNE.nom, *idt.verifier_identites(
            idt.SOMME_LIGNE, r_ligne, s_ligne, o_ligne, eps, t=t, phase=phase)))
        # Sommes de colonnes, à l'échelle du secteur (entreprises réunies).
        r_colonne = [
            idt.residu_somme_colonne(colonnes["menages"], 0.0),
            idt.residu_somme_colonne(colonnes["entreprises_courant"],
                                     colonnes["entreprises_capital"]),
            idt.residu_somme_colonne(colonnes["banque"], 0.0),
            idt.residu_somme_colonne(colonnes["banque_centrale"], 0.0),
            idt.residu_somme_colonne(colonnes["etat"], 0.0),
        ]
        rapports.append((idt.SOMME_COLONNE.nom, *idt.verifier_identites(
            idt.SOMME_COLONNE, r_colonne, self._echelles_secteurs, _OBJETS_SECTEURS, eps,
            t=t, phase=phase)))
        # Clôture = ouverture + lignes, poste par poste, dans chacun des deux
        # bilans qui tiennent la position, chacun à son échelle : contrôler au
        # plus petit des deux S équivaut à contrôler dans les deux.
        ouverture = self._ouverture
        r_poste = [idt.residu_cloture_poste(positions[nom], ouverture[nom], cumul[nom])
                   for nom in NOMS_POSTES]
        rapport_poste = idt.verifier_identites(
            idt.CLOTURE_POSTE, r_poste, self._echelles_postes, self._objets_postes, eps,
            t=t, phase=phase)
        object.__setattr__(self, "_rapport_poste", rapport_poste)
        rapports.append((idt.CLOTURE_POSTE.nom, *rapport_poste))
        # Portes à l'exécution, ligne par ligne, contreparties comprises, à
        # l'échelle de la ligne (point 9, (α)).
        rapports.append((idt.VARIATION_MONNAIE.nom, *idt.verifier_identites(
            idt.VARIATION_MONNAIE, r_porte_m, s_ligne, o_ligne, eps, t=t, phase=phase)))
        rapports.append((idt.VARIATION_MONNAIE_CENTRALE.nom, *idt.verifier_identites(
            idt.VARIATION_MONNAIE_CENTRALE, r_porte_h, s_ligne, o_ligne, eps, t=t,
            phase=phase)))
        # Lecture nette du contrôle de caisse (payeurs non bancaires).
        idt.verifier_caisse(positions, echelles, eps, t=t, phase=phase, positions_debut=debut,
                            mouvements_par_ligne=mouvements_par_ligne)
        if phase == "9":
            rapports.extend(self._couche_noyau())
        return ClotureDePhase(t, phase, tuple(rapports), tuple(montants_phase))

    def _couche_noyau(self) -> list[tuple[str, str, float]]:
        """Phase 9, couche noyau : valeurs nettes, Res_{t+1} ≥ 0, ΔM et ΔH du pas.

        Rend les rapports résidu / S : un par secteur pour l'identité cumulée,
        un pour ΔM et un pour ΔH du pas.
        """
        t = self._t
        eps = self._epsilon
        echelles = self._echelles
        positions = self._positions
        ouverture = self._ouverture
        executes_du_pas = self._executes
        rapports = []
        # V par les flux, à partir des seuls montants exécutés des lignes 1 à
        # 16, colonne de résultat (sous-colonne courante des entreprises),
        # dans l'ordre canonique ; V par le stock, à partir des seules positions.
        resultats = dict.fromkeys(SECTEURS, 0.0)
        for identifiant, cellules in _CELLULES_DE_RESULTAT:
            executes = executes_du_pas[identifiant]
            for secteur, coefficients in cellules:
                cellule = 0.0
                for nom, c in coefficients:
                    cellule += c * executes[nom]
                resultats[secteur] += cellule
        for s in SECTEURS:
            v_flux = idt.valeur_nette_flux(self._v_flux[s], resultats[s])
            self._v_flux_suivant[s] = v_flux
            v_stock = idt.valeur_nette_stock(positions, s)
            rapports.append((idt.TOLERANCE_CUMULEE.nom, s, idt.verifier_tolerance_cumulee(
                v_stock, v_flux, echelles[s], self._epsilon_v, t=t, secteur=s)))
        idt.verifier_reserves_cloture(positions["Res"], echelles["banque"], t=t)
        # ΔM et ΔH du pas, recomposés par les signatures des lignes exécutées,
        # face à la variation des postes depuis l'ouverture.
        signes_et_montants = []
        for ligne in LIGNES:
            if ligne.contrepartie:
                continue
            montant = 0.0
            for v in executes_du_pas[ligne.identifiant].values():
                montant += v
            signes_et_montants.append((ligne.signature, montant))
        variations = {poste: positions[poste] - ouverture[poste] for poste in _POSTES_DES_PORTES}
        rapports.append((idt.VARIATION_MONNAIE.nom, "pas", idt.verifier_identite(
            idt.residu_variation_monnaie(signes_et_montants, variations), echelles["banque"],
            eps, idt.VARIATION_MONNAIE, t=t, phase="9", secteur="banque")))
        rapports.append((idt.VARIATION_MONNAIE_CENTRALE.nom, "pas", idt.verifier_identite(
            idt.residu_variation_monnaie_centrale(signes_et_montants, variations),
            echelles["banque_centrale"], eps, idt.VARIATION_MONNAIE_CENTRALE, t=t, phase="9",
            secteur="banque_centrale")))
        return rapports

    # ------------------------------------------------------------------
    # Lectures seules
    # ------------------------------------------------------------------

    def _phase_close(self, phase: str) -> bool:
        return PHASES.index(phase) < self._rang

    def _lecture_executee(self, ligne: str) -> dict[str, float]:
        if ligne not in LIGNE:
            raise self._refus("ligne inconnue du catalogue", ligne=ligne)
        phase = LIGNE[ligne].phase if LIGNE[ligne].phase is not None else _DERNIERE_EXECUTION
        if not self._phase_close(phase):
            raise self._refus(f"montant exécuté lu avant la clôture de la phase {phase} : "
                              "refusé, jamais un zéro", ligne=ligne)
        return self._executes[ligne]

    def montant_execute(self, ligne: str, colonne: str) -> float:
        """Montant exécuté de la ligne dans une colonne (cellule de `tab:matrice-flux`)."""
        if colonne not in COLONNES:
            raise self._refus(f"colonne inconnue : {colonne!r}", ligne=ligne)
        executes = self._lecture_executee(ligne)
        cellule = 0.0
        for terme in LIGNE[ligne].termes:
            if terme.colonne_plus == colonne:
                cellule += executes[terme.nom]
            elif terme.colonne_moins == colonne:
                cellule -= executes[terme.nom]
        return cellule

    def montant_execute_ligne(self, ligne: str) -> float:
        """Montant exécuté de la ligne : somme signée de ses termes (`tab:portes-monnaie`)."""
        executes = self._lecture_executee(ligne)
        montant = 0.0
        for terme in LIGNE[ligne].termes:
            montant += executes[terme.nom]
        return montant

    def position(self, poste: str) -> float:
        """Position courante : ouverture plus lignes exécutées des phases closes."""
        return self._positions[poste]

    def ouverture(self, poste: str) -> float:
        """Position de l'état d'ouverture, figée pendant le pas."""
        return self._ouverture[poste]

    def echelle(self, secteur: str) -> float:
        """Échelle S du bilan du secteur, évaluée à l'ouverture du pas."""
        return self._echelles[secteur]

    def valeur_nette_stock(self, secteur: str) -> float:
        """V par le stock, sur les positions courantes."""
        return idt.valeur_nette_stock(self._positions, secteur)

    def valeur_nette_flux(self, secteur: str) -> float:
        """V^flux_{t+1}, disponible après la clôture de la phase 9."""
        if not self._phase_close("9"):
            raise self._refus("V^flux du pas lue avant la clôture de la phase 9",
                              secteur=secteur)
        return self._v_flux_suivant[secteur]
