"""Générateur déterministe de flux du jalon J2 : huit pseudo-blocs sous le contrat de bloc (#98).

Contrat : ADR 0012, G5 et Conséquences (« Pour #98 ») ; critères 1 à 12 du
générateur, écrits avant l'essai au rang 1b et validés par le mainteneur le
07/10/2026 (commentaires de l'issue #98), avec le complément du point 8. En
J2, aucun bloc n'existe : ce module en tient lieu pour exercer le noyau, le
moteur et le registre. Ce n'est **pas** un modèle économique : ses règles
sont des règles d'essai, continues, bornées et homogènes de degré 1 dans les
grandeurs nominales ; aucune n'est une règle de la spécification, sauf les
formes exactes imposées (B7 et le montant couvert de la ligne 16) et les
plafonds à une ligne écrits en min/max sur la position lue (E1, H5).

**Contrat des blocs, tenu ligne à ligne** :

- huit pseudo-blocs, un par radical de `PHASES`, chacun siégeant exactement
  dans les étapes où `tab:phases` le déclare (critère 3) ; aucun attribut
  d'instance (`__slots__` vide, déclaration en attribut de classe) ;
- **déterminisme sans état caché** (critère 1) : les tirages d'un pas sont une
  fonction pure de (graine, t), `tirages` ; rien ne persiste d'un pas à
  l'autre ; la graine et t sont lus dans l'état d'ouverture ;
- **lectures déclarées** : chaque lecture passe par un `_Lecteur`, qui refuse
  toute lecture absente du siège ; `assembler` contrôle les lectures
  déclarées (triangularité, colonne « Lisent », montants exécutés compris) ;
- **lignes décidées seulement** (critère 2) : jamais 17, 20 ni 22 ; positions
  lues en lecture seule ;
- **P_t en phase 5** (critère 9) : le pseudo-bloc `prix` écrit `"P"` ;
- **B7 sous la forme exacte** −min(Res^{8b} ; L^CB) (critère 6) ;
- **montant couvert** c = min(|Π| ; max(0 ; M^{G,8a})) déclaré par l'État pour
  une ligne 16 négative (critère 7, complément du point 8) ;
- **contrat de poussière** : toute règle qui lit D_H, D_F ou M^G les lit en
  max(0 ; ·) (ADR 0012, A8) ; les saturations à une ligne (E1, salaires,
  B7, E13) s'écrivent en min/max sur la position lue.

**Sortie du socle** (critère 4) : B_H > 0, θ_CB > 0 (émission vers la banque
centrale), taux de signe quelconque, transferts non nuls, perte de la banque
centrale ; les lignes 19b passent par la **déclaration d'essai** `doubler_19b`,
double du catalogue dans les espaces de noms du grand livre et de
l'ordonnanceur, jamais une modification de `catalogue.py` (ADR 0012,
annotation du 07/10/2026, point 3). Le proposant `finances_publiques` y est un
**artefact d'essai** imposé par `tab:phases` (seul écrivain de la phase 7) : il
ne préjuge pas du proposant de 19b au J6, et aucun test n'en fait une
propriété.

**Écart déclaré** : les lignes 12 et 13 du générateur ne suivent pas la
spécification (base de l'intérêt ; voir `BanqueCentrale.phase_8a`).

**Ordres de grandeur** (critère 10) : niveaux d'ouverture tirés de l'état
stationnaire du socle (`outils/etat_stationnaire.py`, π* = 2 %, n_a = 12, en
PIB du pas), multipliés par `ECHELLE` = 1e6, d'où des bilans d'environ 1e7 ;
croissance nominale tenue par l'investissement, `CROISSANCE_NOMINALE` = 4 %
par an. L'échelle nominale de référence de chaque règle est le capital
d'ouverture K (aucune constante nominale absolue : une redénomination par une
puissance de deux donne une trajectoire identique bit à bit, critère 12).

**Régimes de la banque centrale** (critère 5) : la position nette de réserves
Q = Res − L^CB, que la ligne 21 ne change pas, est pilotée par l'État en
phase 7 vers une cible le plus souvent négative (refinancement, Res = 0),
parfois positive (excédent, L^CB = 0) ; le capital E^CB de la banque centrale
est piloté par la ligne 16 vers une cible de signe quelconque.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import replace

import numpy as np

from nations.etat.schema import EtatPays
from nations.moteur import ordonnanceur as ordo
from nations.moteur.contrat_bloc import (
    GRAND_LIVRE,
    OUVERTURE,
    REGISTRE,
    DeclarationDeBloc,
    Lecture,
    Siege,
)
from nations.moteur.conversions import facteur_par_pas, par_pas
from nations.moteur.ordonnanceur import (
    INDICE_DES_PRIX,
    DeclarationDesEntrees,
    EntreesDuTour,
    Ordonnanceur,
    assembler,
)
from nations.moteur.parametres import TauxDeCroissance, TauxDeFlux
from nations.moteur.parametres.cadre import CADRE, PAS_PAR_AN
from nations.moteur.phases import PHASES
from nations.noyau import catalogue as cat
from nations.noyau import grand_livre as gl_module
from nations.noyau import identites as idt

# --------------------------------------------------------------------------
# Constantes d'essai (sans dimension, sauf ECHELLE)
# --------------------------------------------------------------------------

# Unité monétaire des niveaux d'ouverture : un PIB du pas vaut 1e6 u.m.
ECHELLE = 1e6
# Niveaux d'ouverture, en PIB du pas : état stationnaire du socle à π* = 2 %,
# n_a = 12 (`outils/etat_stationnaire.py --json`, clé « 1.0 ; 0.02 ; 12 » des
# niveaux), hors du socle pour B_H, B_CB et M^G (critère 4).
NIVEAUX_INITIAUX = {
    "D_H": 7.4261196186995395, "D_F": 1.89561692833578, "L": 7.100972469699887,
    "B_H": 0.98765432109876, "B_Bk": 3.1466612165393895, "B_CB": 1.2345678901234567,
    "Res": 0.0, "L_CB": 0.21579989223396775, "M_G": 1.5432109876543211,
    "K": 17.752431174249715, "IN": 1.0573599615648457,
}
# Inflation d'essai de l'indice des prix et croissance nominale du capital, par an.
INFLATION = 0.02
CROISSANCE_NOMINALE = 0.04
AMORTISSEMENT = 0.05
F_PRIX = facteur_par_pas(TauxDeCroissance(INFLATION))
G_PAS = facteur_par_pas(TauxDeCroissance(CROISSANCE_NOMINALE)) - 1.0
DELTA_PAS = par_pas(TauxDeFlux(AMORTISSEMENT))
# PIB du pas rapporté au capital, et cibles rapportées au capital (état
# stationnaire du socle, B_H, M^G, Q et E^CB hors du socle).
Y_SUR_K = 1.0 / NIVEAUX_INITIAUX["K"]
CIBLE_IN = NIVEAUX_INITIAUX["IN"] * Y_SUR_K
CIBLE_L = NIVEAUX_INITIAUX["L"] * Y_SUR_K
CIBLE_B_H = 1.0 * Y_SUR_K
CIBLE_V_H = (NIVEAUX_INITIAUX["D_H"] + 1.0) * Y_SUR_K
CIBLE_V_F = (NIVEAUX_INITIAUX["D_F"] + NIVEAUX_INITIAUX["K"] + NIVEAUX_INITIAUX["IN"]
             - NIVEAUX_INITIAUX["L"]) * Y_SUR_K
CIBLE_V_BK = 0.7100972469699887 * Y_SUR_K
CIBLE_M_G = 1.5 * Y_SUR_K
CIBLE_Q = 1.0 * Y_SUR_K
CIBLE_E_CB = 0.3 * Y_SUR_K
# Valeur nette de l'État : celle que les autres cibles laissent, K + IN moins
# les valeurs nettes visées des quatre autres secteurs (E^CB à sa cible moyenne).
CIBLE_V_G = 1.0 + CIBLE_IN - CIBLE_V_H - CIBLE_V_F - CIBLE_V_BK - 0.5 * CIBLE_E_CB

# Taux directeur d'essai (levier du joueur, lu en phase 1) : moyenne,
# amplitude et période (pas) d'une oscillation, plus un bruit ; de signe
# quelconque (critère 4 : lignes d'intérêts des deux signes).
TAUX_MOYEN, TAUX_AMPLITUDE, TAUX_PERIODE, TAUX_BRUIT = 0.015, 0.04, 96, 0.003

# Tirages du pas, tous uniformes sur [0 ; 1[, dans un ordre fixe.
NOMS_DES_TIRAGES = (
    "salaire", "activite", "propension", "investissement", "impot", "impot_F", "depense",
    "transferts", "credit", "prix", "stocks", "marge_L", "marge_D", "titres_H",
    "achats_H", "achats_Bk", "regime", "capital_CB",
)

# Bandes déclarées des rapports poste / S du bilan du détenteur (critère 11),
# en fraction de S, écrites avant l'essai depuis les cibles ci-dessus ; une
# position nulle à la cible a une bande de part et d'autre de zéro.
# Les bornes hautes de B_CB / S et de L_CB / S ne contraignent pas : quand
# E^CB ≥ 0, S_CB = 2 (B_CB + L_CB), si bien que chaque rapport est au plus 0,5
# (structurel, déclaré ; les bandes ne sont pas modifiées).
BANDES = {
    ("D_H", "menages"): (0.2, 0.6),
    ("B_H", "menages"): (0.0, 0.2),
    ("D_F", "entreprises"): (0.0, 0.15),
    ("K", "entreprises"): (0.3, 0.6),
    ("IN", "entreprises"): (0.0, 0.1),
    ("L", "banque"): (0.1, 0.5),
    ("B_Bk", "banque"): (0.0, 0.3),
    ("Res", "banque"): (0.0, 0.1),
    ("B_CB", "banque_centrale"): (-0.2, 0.6),
    ("L_CB", "banque_centrale"): (0.0, 0.5),
    ("M_G", "etat"): (-1e-12, 0.3),
}


def tirages(graine: int, t: int) -> dict[str, float]:
    """Tirages du pas t : fonction pure de (graine, t), un générateur à graine explicite par pas."""
    valeurs = np.random.default_rng((graine, t)).random(len(NOMS_DES_TIRAGES)).tolist()
    return dict(zip(NOMS_DES_TIRAGES, valeurs, strict=True))


def centre(u: float) -> float:
    """Tirage uniforme ramené sur [−1 ; 1[."""
    return 2.0 * u - 1.0


# --------------------------------------------------------------------------
# Entrées du tour : levier (taux directeur) et entrée de scénario
# --------------------------------------------------------------------------

LEVIER = "taux_directeur"
SCENARIO = "prime_titres"
DECLARATION_DES_ENTREES = DeclarationDesEntrees((SCENARIO,), (LEVIER,))


def taux_directeur(graine: int, t: int, decalage: float = 0.0) -> float:
    """Levier d'essai : taux directeur annuel du pas t, fonction pure de (graine, t)."""
    bruit = float(np.random.default_rng((graine, t, 1)).random())
    dephasage = 2.0 * math.pi * float(np.random.default_rng((graine, 0, 2)).random())
    return (TAUX_MOYEN + decalage
            + TAUX_AMPLITUDE * math.sin(2.0 * math.pi * t / TAUX_PERIODE + dephasage)
            + TAUX_BRUIT * centre(bruit))


def entrees(graine: int, t: int, decalage: float = 0.0) -> EntreesDuTour:
    """Entrées du tour t : prime des titres publics (scénario, phase 0) et levier (phase 1)."""
    prime = 0.005 * np.random.default_rng((graine, t, 3)).random()
    return EntreesDuTour(((SCENARIO, float(prime)),),
                         ((LEVIER, taux_directeur(graine, t, decalage)),))


# --------------------------------------------------------------------------
# Lectures contrôlées contre le siège
# --------------------------------------------------------------------------


class LectureNonDeclaree(AssertionError):
    """Un pseudo-bloc a lu une grandeur que son siège ne déclare pas."""


class ContratDePoussiere(AssertionError):
    """Un pseudo-bloc a lu un moyen de paiement soumis à la lecture nette sans max(0 ; ·)."""


# Moyens de paiement soumis à la lecture nette (D_H, D_F, M^G) : toute règle
# les lit en max(0 ; ·) (ADR 0012, A8, contrat de poussière).
MOYENS_LUS_EN_CAISSE = frozenset(moyen for moyen, _ in cat.MOYENS_LECTURE_NETTE)


class _Lecteur:
    """Lectures d'un pseudo-bloc dans une étape, chacune contrôlée contre son siège.

    Objet local à l'appel de la méthode de phase (rien ne persiste).
    """

    __slots__ = ("_lit", "_vue")

    def __init__(self, vue: ordo.Vue, siege: Siege) -> None:
        self._vue = vue
        self._lit = frozenset(siege.lit)

    def _verifier(self, source: str, nom: str) -> None:
        if Lecture(source, nom) not in self._lit:
            raise LectureNonDeclaree(f"lecture non déclarée : ({source!r}, {nom!r})")

    def ouverture(self, nom: str) -> object:
        """Champ de l'état d'ouverture qui n'est pas un moyen de paiement à lecture nette."""
        if nom in MOYENS_LUS_EN_CAISSE:
            raise ContratDePoussiere(f"{nom} d'ouverture se lit par `caisse_ouverture`, "
                                     "en max(0 ; ·)")
        self._verifier(OUVERTURE, nom)
        return getattr(self._vue.ouverture, nom)

    def caisse_ouverture(self, nom: str) -> float:
        """Moyen de paiement à lecture nette (D_H, D_F, M^G) de l'état d'ouverture, en
        max(0 ; ·) : il peut valoir jusqu'à −ε × S à l'ouverture (A8)."""
        if nom not in MOYENS_LUS_EN_CAISSE:
            raise ContratDePoussiere(f"{nom} n'est pas un moyen de paiement à lecture nette")
        self._verifier(OUVERTURE, nom)
        return max(0.0, getattr(self._vue.ouverture, nom))

    def position(self, poste: str) -> float:
        """Position courante d'un poste qui n'est pas un moyen de paiement à lecture nette."""
        if poste in MOYENS_LUS_EN_CAISSE:
            raise ContratDePoussiere(f"{poste} se lit par `caisse`, en max(0 ; ·)")
        self._verifier(GRAND_LIVRE, poste)
        return self._vue.grand_livre.position(poste)

    def caisse(self, poste: str) -> float:
        """Moyen de paiement à lecture nette (D_H, D_F, M^G), lu en max(0 ; ·) (A8)."""
        if poste not in MOYENS_LUS_EN_CAISSE:
            raise ContratDePoussiere(f"{poste} n'est pas un moyen de paiement à lecture nette")
        self._verifier(GRAND_LIVRE, poste)
        return max(0.0, self._vue.grand_livre.position(poste))

    def execute(self, ligne: str) -> float:
        self._verifier(GRAND_LIVRE, ligne)
        return self._vue.grand_livre.montant_execute_ligne(ligne)

    def pas(self, etape: str, nom: str) -> object:
        self._verifier(etape, nom)
        return self._vue.lire(nom)

    def registre(self, nom: str) -> float:
        self._verifier(REGISTRE, nom)
        return getattr(self._vue, nom)()

    def echelle(self, secteur: str) -> float:
        """Échelle S d'un bilan à l'ouverture : non déclarable (B2), exemptée de la colonne
        « Lisent » (annotation du 07/10/2026, point 10, R2)."""
        return self._vue.grand_livre.echelle(secteur)

    def tirages(self) -> dict[str, float]:
        return tirages(self.ouverture("graine"), self.ouverture("t"))

    def production(self) -> float:
        """PIB du pas de référence, Y = K_ouverture / 17,75 (u.m. par pas)."""
        return Y_SUR_K * self.ouverture("K")


def _ouv(*noms: str) -> tuple[Lecture, ...]:
    return tuple(Lecture(OUVERTURE, nom) for nom in noms)


def _gl(*noms: str) -> tuple[Lecture, ...]:
    return tuple(Lecture(GRAND_LIVRE, nom) for nom in noms)


def _siege(etape: str, ecrit: Sequence[str] = (), lit: Sequence[Lecture] = (),
           propose: Sequence[str] = (), couvre: Sequence[str] = ()) -> Siege:
    return Siege(etape, tuple(ecrit), tuple(lit), tuple(propose), tuple(couvre), ())


# Lectures communes : tirages du pas (graine, t) et échelle nominale (K).
_BASE = _ouv("graine", "t", "K")


class _PseudoBloc:
    """Base des pseudo-blocs : aucun attribut d'instance, sièges en attribut de classe."""

    __slots__ = ()
    declaration: DeclarationDeBloc

    def _lecteur(self, vue: ordo.Vue, etape: str) -> _Lecteur:
        siege = next(s for s in self.declaration.sieges if s.etape == etape)
        return _Lecteur(vue, siege)


def _declaration(radical: str, *sieges: Siege) -> DeclarationDeBloc:
    return DeclarationDeBloc(radical, sieges)


# --------------------------------------------------------------------------
# Règles partagées par deux pseudo-blocs (sous-phase 8 (b), sans lecture mutuelle)
# --------------------------------------------------------------------------


def perte_ou_profit_de_la_banque_centrale(lecteur: _Lecteur) -> float:
    """Π de la ligne 16 : écart du capital E^CB après 8 (a) à sa cible du pas.

    Calculé par la banque centrale (proposant) et par l'État (payeur) depuis
    les mêmes lectures : les deux rendent le même flottant, sans se lire.
    """
    e_cb = (lecteur.position("B_CB") + lecteur.position("L_CB") - lecteur.position("Res")
            - lecteur.caisse("M_G"))
    cible = CIBLE_E_CB * lecteur.ouverture("K") * (0.5 + centre(lecteur.tirages()["capital_CB"]))
    return e_cb - cible


_LECTURES_PI = _BASE + _gl("B_CB", "L_CB", "Res", "M_G")


# --------------------------------------------------------------------------
# Les huit pseudo-blocs
# --------------------------------------------------------------------------


class Production(_PseudoBloc):
    """Activité (phase 2), production (phase 4), variation des stocks (ligne 4, phase 5)."""

    __slots__ = ()
    declaration = _declaration(
        "production",
        _siege("2", ecrit=("activite",), lit=_BASE + (Lecture("1", "i_CB"),)),
        _siege("4", ecrit=("production",), lit=(Lecture("4", "emploi"),)),
        _siege("5", lit=_BASE + _ouv("IN") + (Lecture("2", "activite"),
                                              Lecture("4", "production"),
                                              Lecture("5", INDICE_DES_PRIX)),
               propose=("4",)),
    )

    def phase_2(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "2")
        i_cb = lecteur.pas("1", "i_CB")
        vue.ecrire_pas("activite", 1.0 + 0.03 * centre(lecteur.tirages()["activite"])
                       - 0.2 * i_cb)

    def phase_4(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "4")
        vue.ecrire_pas("production", lecteur.pas("4", "emploi"))

    def phase_5(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "5")
        lecteur.pas("5", INDICE_DES_PRIX)
        k = lecteur.ouverture("K")
        stocks = lecteur.ouverture("IN")
        # Stocks pilotés vers leur cible ; l'écart de production au plan
        # (production / activité prévue en phase 2 − 1, nul ici) s'y ajoute.
        delta = (0.1 * (CIBLE_IN * k - stocks) + G_PAS * stocks
                 + 0.03 * stocks * centre(lecteur.tirages()["stocks"])
                 + 0.1 * stocks * (lecteur.pas("4", "production") / lecteur.pas("2", "activite")
                                   - 1.0))
        vue.proposer("4", {"Delta_IN": delta})


class Travail(_PseudoBloc):
    """Part salariale (phase 1), emploi et salaires (ligne 5, phase 4)."""

    __slots__ = ()
    declaration = _declaration(
        "travail",
        _siege("1", ecrit=("part_salariale",), lit=_BASE),
        _siege("4", ecrit=("emploi",), lit=_BASE + _gl("D_F") + (
            Lecture("1", "part_salariale"), Lecture("2", "activite")), propose=("5",)),
    )

    def phase_1(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "1")
        vue.ecrire_pas("part_salariale",
                       0.76 * (1.0 + 0.05 * centre(lecteur.tirages()["salaire"])))

    def phase_4(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "4")
        activite = lecteur.pas("2", "activite")
        vue.ecrire_pas("emploi", activite)
        plan = lecteur.pas("1", "part_salariale") * activite * lecteur.production()
        # Saturation à une ligne (ligne 5 seule touche D_F en phase 4), sur la
        # position lue en max(0 ; ·) : exacte.
        vue.proposer("5", {"WB": min(plan, lecteur.caisse("D_F"))})


class Prix(_PseudoBloc):
    """Indice des prix P_t, écrit en phase 5 sous le nom `"P"` (critère 9)."""

    __slots__ = ()
    declaration = _declaration(
        "prix",
        _siege("5", ecrit=(INDICE_DES_PRIX,), lit=_ouv("graine", "t") + (
            Lecture(REGISTRE, "dernier_prix"),)),
    )

    def phase_5(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "5")
        bruit = 0.003 * centre(tirages(lecteur.ouverture("graine"), lecteur.ouverture("t"))["prix"])
        vue.ecrire_pas(INDICE_DES_PRIX, lecteur.registre("dernier_prix") * F_PRIX * (1.0 + bruit))


class Menages(_PseudoBloc):
    """Propension (phase 2) et consommation (ligne 1, phase 5) ; rien en phase 9."""

    __slots__ = ()
    declaration = _declaration(
        "menages",
        _siege("2", ecrit=("propension",), lit=_BASE + (Lecture("0", "mois"),)),
        _siege("5", lit=_BASE + _gl("D_H", "B_H", "5") + (Lecture("2", "propension"),),
               propose=("1",)),
        _siege("9"),
    )

    def phase_2(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "2")
        lecteur.pas("0", "mois")
        vue.ecrire_pas("propension", 0.8 + 0.1 * centre(lecteur.tirages()["propension"]))

    def phase_5(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "5")
        depots = lecteur.caisse("D_H")
        richesse = depots + lecteur.position("B_H")
        plan = max(0.0, lecteur.pas("2", "propension") * lecteur.execute("5")
                   + 0.1 * lecteur.production()
                   + 0.2 * (richesse - CIBLE_V_H * lecteur.ouverture("K")))
        # H5 : consommation plafonnée aux dépôts, saturation à une ligne.
        vue.proposer("1", {"C": min(plan, depots)})

    def phase_9(self, vue: ordo.Vue) -> None:
        return None


class Investissement(_PseudoBloc):
    """Plan (phase 2), crédit (ligne 18), investissement (ligne 3), amortissement et dividendes
    (lignes 8, 14) ; rien en phase 9."""

    __slots__ = ()
    declaration = _declaration(
        "investissement",
        _siege("2", ecrit=("taux_investissement",), lit=_BASE + (Lecture("1", "i_CB"),)),
        _siege("3", lit=_BASE + _ouv("L") + (Lecture("2", "taux_investissement"),),
               propose=("18",)),
        _siege("5", lit=_BASE + (Lecture("2", "taux_investissement"),), propose=("3",)),
        _siege("6", lit=_ouv("K") + _gl("D_F", "K", "IN", "L"), propose=("8", "14")),
        _siege("9"),
    )

    def phase_2(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "2")
        i_cb = lecteur.pas("1", "i_CB")
        vue.ecrire_pas("taux_investissement",
                       1.0 + 0.5 * centre(lecteur.tirages()["investissement"]) - 2.0 * i_cb)

    def phase_3(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "3")
        credits = lecteur.ouverture("L")
        # Crédit piloté vers sa cible, augmenté avec le plan d'investissement.
        delta = (0.05 * (CIBLE_L * lecteur.ouverture("K") - credits)
                 + credits * (G_PAS * lecteur.pas("2", "taux_investissement")
                              + 0.01 * centre(lecteur.tirages()["credit"])))
        vue.proposer("18", {"Delta_L": delta})

    def phase_5(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "5")
        k = lecteur.ouverture("K")
        vue.proposer("3", {"I": max(0.0, k * (DELTA_PAS + G_PAS)
                                    * lecteur.pas("2", "taux_investissement"))})

    def phase_6(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "6")
        k = lecteur.ouverture("K")
        vue.proposer("8", {"deltaK": DELTA_PAS * k})
        depots = lecteur.caisse("D_F")
        valeur = depots + lecteur.position("K") + lecteur.position("IN") - lecteur.position("L")
        dividendes = min(max(0.0, 0.5 * (valeur - CIBLE_V_F * k)), 0.5 * depots)
        vue.proposer("14", {"Div_F": dividendes})

    def phase_9(self, vue: ordo.Vue) -> None:
        return None


class Banque(_PseudoBloc):
    """Intérêts et dividendes de la banque (lignes 9, 10, 15, phase 6) ; B7 (ligne 21, 8 (c))."""

    __slots__ = ()
    declaration = _declaration(
        "banque",
        _siege("6", lit=_BASE + _ouv("L", "D_H", "D_F", "B_Bk") + _gl(
            "L", "B_Bk", "Res", "D_H", "D_F", "L_CB") + (Lecture("1", "i_CB"),),
               propose=("9", "10", "15")),
        _siege("8c", lit=_gl("Res", "L_CB"), propose=("21",)),
    )

    def phase_6(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "6")
        u = lecteur.tirages()
        i_cb = lecteur.pas("1", "i_CB")
        i_l = TauxDeFlux(i_cb + 0.015 + 0.002 * centre(u["marge_L"]))
        i_d = TauxDeFlux(i_cb - 0.01 + 0.002 * centre(u["marge_D"]))
        interets_l = par_pas(i_l) * lecteur.ouverture("L")
        interets_dh = par_pas(i_d) * lecteur.caisse_ouverture("D_H")
        interets_df = par_pas(i_d) * lecteur.caisse_ouverture("D_F")
        vue.proposer("9", {"iL_L": interets_l})
        vue.proposer("10", {"iD_DH": interets_dh, "iD_DF": interets_df})
        valeur = (lecteur.position("L") + lecteur.position("B_Bk") + lecteur.position("Res")
                  - lecteur.caisse("D_H") - lecteur.caisse("D_F") - lecteur.position("L_CB"))
        marge = interets_l - interets_dh - interets_df + par_pas(
            TauxDeFlux(i_cb)) * lecteur.ouverture("B_Bk")
        dividendes = max(0.0, marge + 0.3 * (valeur - CIBLE_V_BK * lecteur.ouverture("K")))
        vue.proposer("15", {"Div_Bk": dividendes})

    def phase_8c(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "8c")
        # B7 sous la forme exacte (ADR 0012, A5 ; #90) : Res_{t+1}·L^CB_{t+1} = 0.
        vue.proposer("21", {"Delta_LCB": -min(lecteur.position("Res"),
                                              lecteur.position("L_CB"))})


class BanqueCentrale(_PseudoBloc):
    """Taux directeur (phase 1, levier), intérêts (lignes 12, 13, 8 (a)), résultat (16, 8 (b))."""

    __slots__ = ()
    declaration = _declaration(
        "banque_centrale",
        _siege("1", ecrit=("i_CB",), lit=(Lecture("1", LEVIER),)),
        _siege("8a", lit=_gl("Res", "L_CB") + (Lecture("1", "i_CB"),), propose=("12", "13")),
        _siege("8b", lit=_LECTURES_PI, propose=("16",)),
    )

    def phase_1(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "1")
        vue.ecrire_pas("i_CB", lecteur.pas("1", LEVIER))

    def phase_8a(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "8a")
        i_cb = lecteur.pas("1", "i_CB")
        reserves = lecteur.position("Res")
        # Écart déclaré à la spécification (lignes 12 et 13 de tab:matrice-flux,
        # l. 365-366 et 506 ; refinancement et découvert, l. 502 et 2145 ; résultat
        # de la banque, l. 2125), où la base est la position d'ouverture : ici, la
        # ligne 12 porte sur Res après la phase 7 (de signe quelconque) et la
        # ligne 13 sur L^CB augmenté du découvert de la phase 7. Motif : sous
        # Res_t·L^CB_t = 0 (B7), l'une des deux bases d'ouverture est nulle à
        # chaque pas, ce qui est incompatible avec le critère 4 (ligne non nulle
        # sur ≥ 90 % des pas). Conséquence : le découvert est facturé deux fois
        # (par la ligne 13 ici, et par le refinancement de la ligne 21 qui le
        # couvre). Le seuil de 90 % vaut pour ce générateur, non pour le futur
        # bloc `banque_centrale`.
        vue.proposer("12", {"ires_Res": par_pas(TauxDeFlux(i_cb - 0.0025)) * reserves})
        vue.proposer("13", {"iCB_LCB": par_pas(TauxDeFlux(i_cb)) * (
            lecteur.position("L_CB") + max(0.0, -reserves))})

    def phase_8b(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "8b")
        vue.proposer("16", {"Pi_CB": perte_ou_profit_de_la_banque_centrale(lecteur)})


class FinancesPubliques(_PseudoBloc):
    """Plans (phase 2), dépense (ligne 2), transferts, impôts, intérêts (6, 7, 11a à 11c),
    émission et achats de la banque centrale (19a, 19b), montant couvert (16, 8 (b))."""

    __slots__ = ()
    declaration = _declaration(
        "finances_publiques",
        _siege("2", ecrit=("taux_impot", "part_depense"), lit=_BASE),
        _siege("5", lit=_BASE + _gl("M_G") + (Lecture("2", "part_depense"),), propose=("2",)),
        _siege("6", lit=_BASE + _ouv("B_H", "B_Bk", "B_CB") + _gl("M_G", "5") + (
            Lecture("1", "i_CB"), Lecture("0", SCENARIO), Lecture("2", "taux_impot")),
               propose=("6", "7", "11a", "11b", "11c")),
        _siege("7", lit=_BASE + _ouv("B_H", "B_Bk", "L_CB") + _gl("Res", "M_G", "D_H"),
               propose=("19a-ménages", "19a-banque", "19a-BC", "19b-ménages", "19b-banque")),
        _siege("8b", lit=_LECTURES_PI, couvre=("16",)),
    )

    def phase_2(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "2")
        u = lecteur.tirages()
        vue.ecrire_pas("taux_impot", 0.35 + 0.45 * centre(u["impot"]))
        vue.ecrire_pas("part_depense", 0.2 * (1.0 + 0.2 * centre(u["depense"])))

    def phase_5(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "5")
        plan = lecteur.pas("2", "part_depense") * lecteur.production()
        # E1 : dépense plafonnée à l'encaisse, saturation à une ligne.
        vue.proposer("2", {"G": min(plan, lecteur.caisse("M_G"))})

    def phase_6(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "6")
        u = lecteur.tirages()
        y = lecteur.production()
        taux = TauxDeFlux(lecteur.pas("1", "i_CB") + 0.005 + lecteur.pas("0", SCENARIO))
        i_bh = par_pas(taux) * lecteur.ouverture("B_H")
        i_bbk = par_pas(taux) * lecteur.ouverture("B_Bk")
        i_bcb = par_pas(taux) * lecteur.ouverture("B_CB")
        interets = i_bh + i_bbk + i_bcb
        encaisse = lecteur.caisse("M_G")
        impot_f = 0.02 * y * (1.0 + 0.5 * centre(u["impot_F"]))
        # Impôt des ménages de signe quelconque, au moins ce qui couvre les
        # intérêts au-delà de la moitié de l'encaisse (l'État reste solvable).
        # Règle budgétaire d'essai : l'impôt corrige l'écart de la valeur nette
        # de l'État à sa cible.
        valeur = (encaisse - lecteur.ouverture("B_H") - lecteur.ouverture("B_Bk")
                  - lecteur.ouverture("B_CB"))
        impot_h = self.impot_des_menages(lecteur, max(
            lecteur.pas("2", "taux_impot") * lecteur.execute("5")
            - 0.2 * (valeur - CIBLE_V_G * lecteur.ouverture("K")),
            interets - impot_f - 0.5 * encaisse))
        # E6 : transferts plafonnés à l'encaisse après impôts et intérêts ;
        # position touchée par plusieurs lignes : poussière admise (A5).
        plafond = max(0.0, encaisse + impot_h + impot_f - interets)
        transferts = self.transferts(lecteur, min(self.plan_de_transferts(
            0.05 * y * (1.0 + centre(u["transferts"]))), plafond), plafond)
        vue.proposer("6", {"Tr": transferts})
        vue.proposer("7", {"T_H": impot_h, "T_F": impot_f})
        vue.proposer("11a", {"iB_BH": i_bh})
        vue.proposer("11b", {"iB_BBk": i_bbk})
        vue.proposer("11c", {"iB_BCB": i_bcb})

    # Points de variante (critère 8) : une variante d'essai les redéfinit dans
    # une sous-classe ; le générateur les laisse à l'identité.
    def impot_des_menages(self, lecteur: _Lecteur, impot: float) -> float:
        return impot

    def plan_de_transferts(self, plan: float) -> float:
        return plan

    def transferts(self, lecteur: _Lecteur, transferts: float, plafond: float) -> float:
        return transferts

    def titres_des_menages(self, lecteur: _Lecteur, emission: float) -> float:
        return emission

    def phase_7(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "7")
        u = lecteur.tirages()
        k = lecteur.ouverture("K")
        b_h = lecteur.ouverture("B_H")
        b_bk = lecteur.ouverture("B_Bk")
        # Excursion du pas : intensité w ∈ [0 ; 1], nulle sur 85 % des pas.
        w = max(0.0, u["regime"] - 0.85) / 0.15
        # Position nette de réserves visée : négative hors excursion (refinancement),
        # positive dès w > 0,23 et pleine dès w = 0,5, avant que l'encaisse visée
        # ne devienne faible (bilan de la banque centrale B_CB = E^CB + Q + M^G).
        cible_q = CIBLE_Q * k * (-1.0 + 2.2 * min(1.0, 2.0 * w))
        # Encaisse visée : nulle au-delà de w = 0,8 (pas « secs », ligne 16 non
        # couverte), faible en deçà (couverture partielle), pleine hors excursion.
        encaisse = lecteur.caisse("M_G")
        cible_m_g = CIBLE_M_G * k * max(0.0, 1.0 - 1.25 * w) ** 2
        # Achats (+) ou ventes (−) de la banque centrale sur le marché secondaire.
        y_h = 0.02 * centre(u["achats_H"]) * b_h
        y_bk = 0.02 * centre(u["achats_Bk"]) * b_bk
        x_h = self.titres_des_menages(lecteur, min(
            0.2 * (CIBLE_B_H * k - b_h) + 0.01 * b_h * centre(u["titres_H"]) + y_h,
            0.5 * lecteur.caisse("D_H")))
        cible_res = cible_q + lecteur.ouverture("L_CB")
        x_bk = lecteur.position("Res") - cible_res - x_h + y_h + y_bk
        x_cb = cible_m_g - encaisse - x_h - x_bk
        vue.proposer("19a-ménages", {"Delta_BH_prim": x_h})
        vue.proposer("19a-banque", {"Delta_BBk_prim": x_bk})
        vue.proposer("19a-BC", {"Delta_BCB_prim": x_cb})
        vue.proposer("19b-ménages", {"Delta_BH_sec": y_h})
        vue.proposer("19b-banque", {"Delta_BBk_sec": y_bk})

    def phase_8b(self, vue: ordo.Vue) -> None:
        lecteur = self._lecteur(vue, "8b")
        perte = perte_ou_profit_de_la_banque_centrale(lecteur)
        if perte < 0.0:
            # E13 : montant couvert c = min(|Π| ; max(0 ; M^{G,8a})), déclaré par
            # le payeur ; le noyau exécute −c (ADR 0012, A3.2, point 8).
            vue.declarer_montant_couvert("16", min(-perte, lecteur.caisse("M_G")))


PSEUDO_BLOCS = (Production, Travail, Prix, Menages, Investissement, Banque, BanqueCentrale,
                FinancesPubliques)


def blocs(remplacer: dict[str, type] | None = None) -> tuple[_PseudoBloc, ...]:
    """Les huit pseudo-blocs ; `remplacer` substitue une classe (variante) à un radical."""
    classes = {c.declaration.radical: c for c in PSEUDO_BLOCS}
    if remplacer:
        classes.update(remplacer)
    return tuple(classe() for classe in classes.values())


def ordonnanceur(remplacer: dict[str, type] | None = None) -> Ordonnanceur:
    """Ordonnanceur du générateur (sous la déclaration d'essai de 19b, `doubler_19b`)."""
    return assembler(PHASES, blocs(remplacer), CADRE, DECLARATION_DES_ENTREES)


# --------------------------------------------------------------------------
# Déclaration d'essai des lignes 19b (ADR 0012, G5 ; annotation du 07/10/2026, point 3)
# --------------------------------------------------------------------------

LIGNES_19B = ("19b-ménages", "19b-banque")
PROPOSANT_19B = "finances_publiques"


def doubler_19b(monkeypatch) -> None:
    """Double du catalogue, le temps d'un essai : 19b proposées par `finances_publiques`.

    Objets neufs dans les espaces de noms de `grand_livre` et `ordonnanceur`
    seulement ; `catalogue.py`, `cat.LIGNE` et `cat.LIGNES_DE_LA_PHASE` sont
    intacts. Le proposant `finances_publiques` est un artefact d'essai imposé
    par `tab:phases` (la phase 7 a un seul écrivain, ADR 0011) : il ne préjuge
    pas du choix du proposant de 19b au J6, et aucun test n'en fait une
    propriété.
    """
    doubles = {i: replace(cat.LIGNE[i], proposant=PROPOSANT_19B) for i in LIGNES_19B}
    lignes = tuple(doubles.get(ligne.identifiant, ligne) for ligne in cat.LIGNES)
    ligne = {**cat.LIGNE, **doubles}
    par_phase = {phase: tuple(doubles.get(x.identifiant, x) for x in lignes_de_phase)
                 for phase, lignes_de_phase in cat.LIGNES_DE_LA_PHASE.items()}
    for module in (gl_module, ordo):
        monkeypatch.setattr(module, "LIGNE", ligne)
        monkeypatch.setattr(module, "LIGNES", lignes)
        monkeypatch.setattr(module, "LIGNES_DE_LA_PHASE", par_phase)


# --------------------------------------------------------------------------
# État initial et redénomination
# --------------------------------------------------------------------------


def registre_stationnaire(pi_barre: float = INFLATION) -> tuple[float, ...]:
    """P_{t−u} = (1 + π̄)^{−(u−1)/n_a}, u = 1 … n_a + 1, P_{t−1} = 1."""
    n_a = PAS_PAR_AN.valeur
    return tuple((1.0 + pi_barre) ** (-(u - 1) / n_a) for u in range(1, n_a + 2))


def etat_initial(graine: int) -> EtatPays:
    """État d'ouverture du pas 0 : niveaux stationnaires × ECHELLE, V^flux = V^stock."""
    positions = {nom: v * ECHELLE for nom, v in NIVEAUX_INITIAUX.items()}
    v_flux = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(positions, s)
              for s in cat.SECTEURS}
    return EtatPays(identifiant="A", graine=graine, t=0, registre_prix=registre_stationnaire(),
                    **positions, **v_flux)


# Champs nominaux de l'état (positions et V^flux) et indice (registre).
CHAMPS_NOMINAUX = cat.NOMS_POSTES + tuple(cat.VALEUR_NETTE_FLUX[s] for s in cat.SECTEURS)


def redenominer(etat: EtatPays, facteur: float) -> EtatPays:
    """Redénomination : champs nominaux et registre multipliés par `facteur`."""
    champs = {nom: getattr(etat, nom) * facteur for nom in CHAMPS_NOMINAUX}
    return replace(etat, registre_prix=tuple(x * facteur for x in etat.registre_prix), **champs)


def derouler(etat: EtatPays, nb_pas: int, o: Ordonnanceur, observateur,
             decalage: Callable[[int], float] = lambda t: 0.0) -> EtatPays:
    """Déroule `nb_pas` pas depuis `etat`, entrées du tour du générateur."""
    for _ in range(nb_pas):
        t = etat.t
        etat = ordo.executer_pas(etat, entrees(etat.graine, t, decalage(t)), o, observateur)
    return etat
