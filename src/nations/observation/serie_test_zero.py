"""Série du test zéro : grandeurs B1 à B26 de `tab:criteres-j3` et r̂*, relevées hors de l'état (#176).

`SerieDuTestZero` est un observateur (ADR 0012, E1 ; ADR 0014, E1) : il lit les montants
exécutés des clôtures de phase (`ClotureDePhase`) et, à chaque fin de pas (`FinDePas`), les
variables du pas et l'état t + 1 ; l'état d'ouverture du pas t est l'état reçu à la
construction (pas 0) ou celui de la fin du pas précédent. Il tient, hors de l'état, une valeur
par pas et par grandeur, puis publie les moyennes par bloc de 60 pas et les écarts maximaux à
une valeur de référence. Il ne lit ni table ni bloc : le nombre de pas par an et r̄ (pour
B25) lui sont donnés. Il n'a **aucun effet sur la trajectoire** (test de suppression : sauvegardes
identiques à l'octet sous cette série et sous `ObservateurNul`).

Définitions, unités, dénominateurs et fenêtres : `GRANDEURS` (une `Grandeur` par clé), celles de
`tab:criteres-j3`, inchangées. Conventions :
- **ouverture** : stock de l'état d'ouverture du pas t ; un ratio au PIB annuel est ce stock
  rapporté à n_a fois le flux du pas (`ratio_au_pib_annuel`, M22, lecture (e)) ; PIB du pas :
  lignes 1 à 4 exécutées, C + G + I + ΔIN ;
- **12 tours** : fenêtre des n_a derniers pas relevés, pas courant compris, évaluée dès le
  n_a-ième pas relevé (pas 11 d'une série partie du pas 0, D13) ; une valeur au pas t − n_a
  antérieure au premier pas relevé (pas −1) est lue sur l'état d'ouverture du premier pas
  (salaire W, dernier prix connu P_{t−1}, production retenue y_{t−1}) ;
- **pas** : valeur du pas t, ou de l'état t + 1 pour une variable d'état écrite au pas t.

Grandeurs nulles de B19 (Res, H = Res sans billets, E^CB par les flux, B_CB, résidu de
l'identité) : rapportées à S^CB de l'état t + 1 (`identites.echelle_bilan`).
"""

from __future__ import annotations

import math
import types
from dataclasses import dataclass

from nations.etat.schema import EtatPays
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import Evenement, FinDePas
from nations.observation.residus import Grandeur

# Longueur d'un bloc de la moyenne des lignes B, en pas (`tab:criteres-j3`, conventions de lecture).
LONGUEUR_DU_BLOC = 60

# Lignes dont la série lit le montant exécuté (somme des termes) : 1 à 4 (PIB), 5 (WB), 6 (Tr),
# 7 (T_H + T_F), 11a à 11c (i_CB B/n_a, E7) et 16 (Π^CB).
LIGNES_LUES = ("1", "2", "3", "4", "5", "6", "7", "11a", "11b", "11c", "16")


def ratio_au_pib_annuel(stock: float, flux_du_pas: float, pas_par_an: int) -> float:
    """Ratio au PIB annuel du test zéro : stock d'ouverture rapporté à n_a fois le flux du pas
    (M22, lecture (e) ; `sec:cadre-calendrier`), en années de flux. Division par n_a × flux :
    exemption nommée du test « conversion unique » (ce n'est pas une conversion de taux)."""
    # eq:observation-ratio-pib-annuel
    return stock / (pas_par_an * flux_du_pas)


def richesse_sur_revenu_annuel(V_H: float, YD: float, pas_par_an: int) -> float:
    """B10 : richesse d'ouverture des ménages rapportée à n_a fois le revenu disponible du pas,
    en années de revenu disponible. Ce n'est pas un ratio au PIB annuel au sens du cadre (M27 ;
    `sec:menages-restitution`) : aucune balise. Division par n_a × YD : exemption nommée du test
    « conversion unique » (ce n'est pas une conversion de taux)."""
    return V_H / (pas_par_an * YD)


def _positions(etat: EtatPays) -> dict[str, float]:
    """Onze positions de l'état, par accès nommés (aucun accès dynamique ; liste égale aux postes
    du catalogue, contrôlée à l'importation)."""
    return {"D_H": etat.D_H, "D_F": etat.D_F, "L": etat.L, "B_H": etat.B_H, "B_Bk": etat.B_Bk,
            "B_CB": etat.B_CB, "Res": etat.Res, "L_CB": etat.L_CB, "M_G": etat.M_G, "K": etat.K,
            "IN": etat.IN}


if set(cat.NOMS_POSTES) != {
        "D_H", "D_F", "L", "B_H", "B_Bk", "B_CB", "Res", "L_CB", "M_G", "K", "IN"}:
    raise AssertionError("série du test zéro : les positions lues diffèrent des postes du catalogue")
# La valeur nette par les flux de la banque centrale est lue sous ce nom (`cat.VALEUR_NETTE_FLUX`).
if cat.VALEUR_NETTE_FLUX["banque_centrale"] != "V_flux_banque_centrale":
    raise AssertionError("série du test zéro : V^flux de la banque centrale renommée au catalogue")


_OUV, _PAS, _DOUZE = "ouverture", "pas", "12 tours"
_PIB12 = "12 PIB (n_a fois le PIB nominal du pas, lignes 1 à 4)"
# Clé → définition, unité, dénominateur, fenêtre (`tab:criteres-j3`, colonnes 2 et 3).
GRANDEURS: types.MappingProxyType[str, Grandeur] = types.MappingProxyType({g.nom: g for g in (
    Grandeur("B1", "stock d'ouverture en volume sur ventes du pas, IN^vol/v", "pas de ventes", "v",
             _OUV),
    Grandeur("B2", "taux d'utilisation y/y^cap", "fraction", "y^cap", _PAS),
    Grandeur("B3", "taux de chômage U (état t + 1, écrit au pas t)", "fraction", "N^pa", _PAS),
    Grandeur("B4", "part salariale ΣWB/ΣVA, VA = lignes 1 à 4", "fraction", "valeur ajoutée",
             _DOUZE),
    Grandeur("B5", "croissance du salaire réel (W_t/p_t)/(W_{t−12}/p_{t−12}) − 1",
             "fraction par an", "W/p de t − 12", _DOUZE),
    Grandeur("B6", "marge p/UC − 1, moyenne de 12 tours", "fraction", "UC", _DOUZE),
    Grandeur("B7", "glissement P_t/P_{t−12} − 1", "fraction par an", "P_{t−12}", _DOUZE),
    Grandeur("B8", "ancrage π^e − π* (état t + 1)", "fraction par an", "—", _PAS),
    Grandeur("B9", "taux réel restitué r = i_CB − π, π de B7", "fraction par an", "—",
             "pas (dès le premier pas de B7)"),
    Grandeur("B10", "richesse des ménages V_H/(12 YD), V_H = valeur nette d'ouverture",
             "années de revenu disponible", "12 fois YD du pas", _OUV),
    Grandeur("B11", "taux d'épargne nominal 1 − ΣC/ΣYD, C = ligne 1", "fraction",
             "revenu disponible", _DOUZE),
    Grandeur("B12", "capital au prix courant p K^vol/(12 PIB)", "années de PIB", _PIB12, _OUV),
    Grandeur("B13", "taux d'investissement ΣI/ΣPIB, I = ligne 3", "fraction", "PIB", _DOUZE),
    Grandeur("B14", "levier L/K", "fraction", "K", _OUV),
    Grandeur("B15", "dépôts des entreprises D_F/(12 PIB)", "années de PIB", _PIB12, _OUV),
    Grandeur("B16", "masse monétaire (D_H + D_F)/(12 PIB)", "années de PIB", _PIB12, _OUV),
    Grandeur("B17", "fonds propres de la banque E^Bk/L, E^Bk = valeur nette d'ouverture",
             "fraction", "L", _OUV),
    Grandeur("B18 (i) ϖ_L", "i_{L,t+1} − i_CB,t (état t + 1, taux du tour)", "fraction par an",
             "—", "chaque pas"),
    Grandeur("B18 (i) ϖ_D", "i_CB,t − i_{D,t+1} (taux du tour, état t + 1)", "fraction par an",
             "—", "chaque pas"),
    Grandeur("B18 (ii) ϖ_L", "écart contemporain i_{L,t} − i_CB,t (ouverture, taux du tour)",
             "fraction par an", "—", "pas, jugé par bloc"),
    Grandeur("B18 (ii) ϖ_D", "écart contemporain i_CB,t − i_{D,t} (taux du tour, ouverture)",
             "fraction par an", "—", "pas, jugé par bloc"),
    Grandeur("B19 M^G", "encaisse du Trésor M^G/(12 PIB)", "années de PIB", _PIB12, _OUV),
    Grandeur("B19 Res (H)", "réserves Res (monnaie centrale H = Res, sans billets), état t + 1",
             "sans dimension (u.m. sur S^CB)", "S^CB de l'état t + 1", _PAS),
    Grandeur("B19 E^CB", "fonds propres de la banque centrale par les flux (V^flux), état t + 1",
             "sans dimension (u.m. sur S^CB)", "S^CB de l'état t + 1", _PAS),
    Grandeur("B19 B_CB", "titres de la banque centrale B_CB, état t + 1",
             "sans dimension (u.m. sur S^CB)", "S^CB de l'état t + 1", _PAS),
    Grandeur("B19 identité", "résidu L^CB + B_CB − Res − M^G − E^CB (E^CB par les flux), état t + 1",
             "sans dimension (u.m. sur S^CB)", "S^CB de l'état t + 1", _PAS),
    Grandeur("B20", "titres de la banque B_Bk/(12 PIB)", "années de PIB", _PIB12, _OUV),
    Grandeur("B21", "dette consolidée (B − M^G − E^CB)/(12 PIB), E^CB = valeur nette d'ouverture",
             "années de PIB", _PIB12, _OUV),
    Grandeur("B22", "déficit public Σ(G + Tr + i_CB B/n_a − T_H − T_F − Π^CB)/ΣPIB, lignes 2, 6, "
             "11a à 11c, 7 et 16", "fraction du PIB", "PIB", _DOUZE),
    Grandeur("B24", "croissance de la production y_t/y_{t−12} − 1", "fraction par an",
             "y de t − 12", _DOUZE),
    Grandeur("B25", "taux neutre retenu par la règle r̂* − r̄ (état t + 1)", "fraction par an",
             "—", _PAS),
    Grandeur("B26", "taux directeur et prescription i_CB − i^règle", "fraction par an", "—",
             _PAS),
    Grandeur("r̂*", "taux neutre retenu par la règle r̂* (état t + 1)", "fraction par an", "—",
             _PAS),
)})

# Grandeurs évaluées sur 12 tours, dès le n_a-ième pas relevé (D13) ; B9 lit π de B7.
SUR_12_TOURS = frozenset({"B4", "B5", "B6", "B7", "B9", "B11", "B13", "B22", "B24"})


@dataclass(frozen=True, slots=True)
class MoyenneDeBloc:
    """Moyenne d'une grandeur sur un bloc de pas : premier et dernier pas du bloc, nombre de
    valeurs relevées dans le bloc (moins que sa longueur pour une grandeur sur 12 tours au
    premier bloc) et moyenne (somme exacte arrondie une fois, `math.fsum`, sur ce nombre)."""

    premier: int
    dernier: int
    nombre: int
    moyenne: float


class SerieDuTestZero:
    """Observateur : une valeur par pas et par grandeur de `GRANDEURS`, hors de l'état."""

    __slots__ = ("_W", "_fenetre", "_montants", "_ouverture", "_p", "_pas", "_pas_par_an",
                 "_r_bar", "_series", "_y")

    def __init__(self, ouverture: EtatPays, *, pas_par_an: int, r_bar: float) -> None:
        if type(ouverture) is not EtatPays:
            raise TypeError(f"EtatPays d'ouverture attendu, {type(ouverture).__name__} reçu")
        self._ouverture = ouverture
        self._pas_par_an = pas_par_an
        self._r_bar = r_bar
        self._montants: dict[str, float] = {}
        self._series: dict[str, list[tuple[int, float]]] = {nom: [] for nom in GRANDEURS}
        self._pas: list[int] = []
        # Par pas relevé : (PIB, WB, I, C, YD, numérateur du déficit, p/UC − 1).
        self._fenetre: list[tuple[float, float, float, float, float, float, float]] = []
        # Salaire, prix et production, en tête la valeur du pas −1 lue à l'ouverture du premier pas.
        self._W = [ouverture.W]
        self._p = [ouverture.registre_prix[0]]
        self._y = [ouverture.y_m1]

    def relever(self, evenement: Evenement) -> None:
        if type(evenement) is ClotureDePhase:
            for ligne, termes in evenement.montants:
                if ligne in LIGNES_LUES:
                    if ligne in self._montants:
                        raise ValueError(f"pas {evenement.t} : ligne {ligne} relevée deux fois "
                                         "dans le pas (une seule exécution attendue)")
                    self._montants[ligne] = sum(x for _, x in termes)
            return
        if type(evenement) is not FinDePas:
            raise TypeError(f"événement d'observation inconnu : {type(evenement).__name__}")
        self._clore(evenement)

    def _ajouter(self, nom: str, t: int, valeur: float) -> None:
        self._series[nom].append((t, valeur))

    def _clore(self, fin: FinDePas) -> None:
        t, e, o, n = fin.t, fin.etat, self._ouverture, self._pas_par_an
        manquantes = [ligne for ligne in LIGNES_LUES if ligne not in self._montants]
        if manquantes:
            raise ValueError(f"pas {t} : lignes non exécutées, lues par la série du test zéro : "
                             + ", ".join(manquantes))
        m, v = self._montants, dict(fin.variables_du_pas)
        pib = m["1"] + m["2"] + m["3"] + m["4"]
        positions = _positions(o)
        deficit = m["2"] + m["6"] + (m["11a"] + m["11b"] + m["11c"]) - m["7"] - m["16"]
        self._fenetre.append((pib, m["5"], m["3"], m["1"], v["YD_m1_suivant"], deficit,
                              v["p"] / v["UC"] - 1.0))
        self._W.append(v["W_suivant"])
        self._p.append(v["p"])
        self._y.append(v["y"])
        self._pas.append(t)
        ajouter = self._ajouter

        ajouter("B1", t, o.IN_vol / v["v"])
        ajouter("B2", t, v["y"] / v["y_cap"])
        ajouter("B3", t, v["U_suivant"])
        ajouter("B8", t, e.pi_e - e.pi_etoile)
        ajouter("B10", t, richesse_sur_revenu_annuel(
            idt.valeur_nette_stock(positions, "menages"), v["YD_m1_suivant"], n))
        ajouter("B12", t, ratio_au_pib_annuel(v["p"] * o.K_vol, pib, n))
        ajouter("B14", t, o.L / o.K)
        ajouter("B15", t, ratio_au_pib_annuel(o.D_F, pib, n))
        ajouter("B16", t, ratio_au_pib_annuel(o.D_H + o.D_F, pib, n))
        ajouter("B17", t, idt.valeur_nette_stock(positions, "banque") / o.L)
        ajouter("B18 (i) ϖ_L", t, e.i_L - v["i_CB"])
        ajouter("B18 (i) ϖ_D", t, v["i_CB"] - e.i_D)
        ajouter("B18 (ii) ϖ_L", t, o.i_L - v["i_CB"])
        ajouter("B18 (ii) ϖ_D", t, v["i_CB"] - o.i_D)
        ajouter("B19 M^G", t, ratio_au_pib_annuel(o.M_G, pib, n))
        s_cb = idt.echelle_bilan(_positions(e), "banque_centrale")
        # E^CB par les flux (V^flux), non par le bilan : l'identité n'est pas une tautologie.
        e_cb_flux = e.V_flux_banque_centrale
        ajouter("B19 Res (H)", t, e.Res / s_cb)
        ajouter("B19 E^CB", t, e_cb_flux / s_cb)
        ajouter("B19 B_CB", t, e.B_CB / s_cb)
        ajouter("B19 identité", t, (e.L_CB + e.B_CB - e.Res - e.M_G - e_cb_flux) / s_cb)
        ajouter("B20", t, ratio_au_pib_annuel(o.B_Bk, pib, n))
        dette = (o.B_H + o.B_Bk + o.B_CB) - o.M_G - idt.valeur_nette_stock(positions,
                                                                         "banque_centrale")
        ajouter("B21", t, ratio_au_pib_annuel(dette, pib, n))
        ajouter("B25", t, e.r_hat_etoile - self._r_bar)
        ajouter("B26", t, v["i_CB"] - v["i_regle"])
        ajouter("r̂*", t, e.r_hat_etoile)

        k = len(self._fenetre)  # pas relevés, pas courant compris
        if k >= n:
            fenetre = self._fenetre[k - n:]
            somme_pib = math.fsum(f[0] for f in fenetre)
            ajouter("B4", t, math.fsum(f[1] for f in fenetre) / somme_pib)
            ajouter("B13", t, math.fsum(f[2] for f in fenetre) / somme_pib)
            ajouter("B11", t, 1.0 - math.fsum(f[3] for f in fenetre)
                    / math.fsum(f[4] for f in fenetre))
            ajouter("B22", t, math.fsum(f[5] for f in fenetre) / somme_pib)
            # Moyenne des n_a valeurs de la fenêtre (len(fenetre) = n_a).
            ajouter("B6", t, math.fsum(f[6] for f in fenetre) / len(fenetre))
            # Indice k dans _W, _p, _y : pas courant ; k − n_a : pas t − n_a (−1 au pas 11).
            ajouter("B5", t, (self._W[k] / self._p[k]) / (self._W[k - n] / self._p[k - n]) - 1.0)
            ajouter("B24", t, self._y[k] / self._y[k - n] - 1.0)
            glissement = v["P"] / o.registre_prix[n - 1] - 1.0
            ajouter("B7", t, glissement)
            ajouter("B9", t, v["i_CB"] - glissement)

        self._ouverture = e
        self._montants = {}

    def pas(self) -> tuple[int, ...]:
        """Pas clos relevés."""
        return tuple(self._pas)

    def serie(self, nom: str) -> tuple[tuple[int, float], ...]:
        """Valeurs relevées d'une grandeur de `GRANDEURS` : (t, valeur), une par pas évalué."""
        return tuple(self._series[nom])

    def moyennes_par_bloc(self, nom: str,
                          longueur: int = LONGUEUR_DU_BLOC) -> tuple[MoyenneDeBloc, ...]:
        """Moyennes de la grandeur sur les blocs **complets** de `longueur` pas, comptés depuis le
        premier pas relevé : bloc b = pas [t_0 + b·longueur ; t_0 + (b + 1)·longueur − 1]."""
        if not self._pas:
            return ()
        t_0 = self._pas[0]
        complets = len(self._pas) // longueur
        par_bloc: list[list[float]] = [[] for _ in range(complets)]
        for t, x in self._series[nom]:
            b = (t - t_0) // longueur
            if b < complets:
                par_bloc[b].append(x)
        return tuple(MoyenneDeBloc(t_0 + b * longueur, t_0 + (b + 1) * longueur - 1, len(xs),
                                   math.fsum(xs) / len(xs))
                     for b, xs in enumerate(par_bloc) if xs)

    def ecart_relatif_maximal(self, nom: str, reference: float,
                              avant: int) -> tuple[float, int | None]:
        """A2 : max |x_t/x̄ − 1| sur les pas t < `avant`, et le premier pas qui l'atteint (0 et
        `None` sans valeur)."""
        pire: tuple[float, int | None] = (0.0, None)
        for t, x in self._series[nom]:
            if t >= avant:
                break
            ecart = abs(x / reference - 1.0)
            if pire[1] is None or pire[0] < ecart:
                pire = (ecart, t)
        return pire

    def ecart_absolu_maximal(self, nom: str, reference: float,
                             avant: int) -> tuple[float, int | None]:
        """A2 (grandeur nulle) et égalités par pas : max |x_t − x̄| sur les pas t < `avant`, et le
        premier pas qui l'atteint (0 et `None` sans valeur)."""
        pire: tuple[float, int | None] = (0.0, None)
        for t, x in self._series[nom]:
            if t >= avant:
                break
            ecart = abs(x - reference)
            if pire[1] is None or pire[0] < ecart:
                pire = (ecart, t)
        return pire
