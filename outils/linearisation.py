"""Linéarisation numérique de la carte d'un pas du moteur autour du sentier stationnaire (#112).

Contrat : issue #112, point 4 ; synthèse du rang 1a de J3-b (lignes « boucle
propre » des fiches 2 à 4, classe (a)) ; puis critère S1 de `tab:criteres-j3`
(J3-f). Critère d'acceptation, écrit avant l'essai : la linéarisation retrouve
une valeur propre connue en forme fermée sur un cas d'essai, à 1e−8
(`tests/unitaires/test_linearisation.py`, `tests/invariants/test_socle_partiel.py`).

**Carte d'un pas.** `carte_du_moteur` fait de `executer_pas` une carte
x_t ↦ x_{t+1} sur des variables d'état scalaires nommées (positions,
variables des blocs), les autres champs de l'état d'ouverture tenus à leur
valeur ; les V^flux sont recalculées égales à V^stock des positions
perturbées, pour que l'état d'ouverture reste cohérent (le noyau arrêterait
sinon sur l'identité cumulée). Le registre n'est pas une variable de la carte.

**Ramenée au sentier.** Une grandeur qui croît sur le sentier est divisée par
son facteur de tendance sur un pas, lu dans son **unité** (`FACTEURS_PAR_UNITE`) :
u.m. par Γ̄ = [(1 + g)(1 + π̄)]^{1/n_a} ; u.v. et u.v. par pas par
(1 + g)^{1/n_a} ; productivité (u.v. par personne et par pas) par
(1 + g_pr)^{1/n_a} ; personnes par (1 + g_N)^{1/n_a} ; salaire (u.m. par
personne et par pas) par [(1 + g_pr)(1 + π̄)]^{1/n_a} ; prix par
(1 + π̄)^{1/n_a} ; fraction, sans dimension et taux par 1. L'invariance
d'unité de la déclaration (ADR 0012, C1) ne suffit pas à fixer la tendance :
N et N^pa sont des volumes au sens de la redénomination mais croissent au taux
g_N, pr au taux g_pr. g = (1 + g_pr)(1 + g_N) − 1 est lue dans les tables de
l'ensemble des paramètres ; π̄ est un argument. Les facteurs passent par la
seule conversion géométrique du moteur (`facteur_par_pas`).

**Jacobienne.** Différences finies centrées, pas relatif `PAS_RELATIF` = 1e−6
de l'échelle de chaque variable (son module à l'état stationnaire, avec un
plancher déclaré pour une variable nulle), puis mise à l'échelle S⁻¹ J S, qui
garde les valeurs propres (même méthode que `outils/maquette_conjointe.py`).
Le résidu du point fixe est publié : une carte dont l'état d'ouverture n'est
pas un point fixe ramené au sentier n'a pas de linéarisation au sens de S1.
Aucune boucle n'itère jusqu'à un point fixe : 2k + 1 évaluations de la carte
pour k variables.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Callable, Sequence
from dataclasses import dataclass

import numpy as np

from nations.etat import schema
from nations.moteur.conversions import facteur_par_pas
from nations.moteur.ordonnanceur import EntreesDuTour, executer_pas
from nations.moteur.parametres import TauxDeCroissance
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.observation.observateur import ObservateurNul

PAS_RELATIF = 1e-6  # pas des différences finies, relatif à l'échelle de chaque variable
PLANCHER_D_ECHELLE = 1.0  # échelle d'une variable nulle à l'état stationnaire (déclarée)

# Tendance de chaque unité sur un pas : (exposant de 1 + g_pr, de 1 + g_N, de 1 + π̄), le facteur
# étant [(1 + g_pr)^a (1 + g_N)^b (1 + π̄)^c]^{1/n_a}.
FACTEURS_PAR_UNITE = {
    "u.m.": (1, 1, 1),
    "u.m. par pas": (1, 1, 1),
    "u.v.": (1, 1, 0),
    "u.v. par pas": (1, 1, 0),
    "u.v. par personne et par pas": (1, 0, 0),
    "personnes": (0, 1, 0),
    "u.m. par personne et par pas": (1, 0, 1),
    "u.m. par u.v.": (0, 0, 1),
    "fraction": (0, 0, 0),
    "sans dimension": (0, 0, 0),
    "par an, taux de croissance": (0, 0, 0),
}


def facteur_de_tendance(unite: str, parametres: object, pi_barre: float) -> float:
    """Facteur de tendance d'une grandeur de cette unité sur un pas, sur le sentier à π̄."""
    if unite not in FACTEURS_PAR_UNITE:
        raise ValueError(f"unité {unite!r} : tendance non déclarée")
    a, b, c = FACTEURS_PAR_UNITE[unite]
    croissance = ((1.0 + parametres.production.g_pr.valeur) ** a
                  * (1.0 + parametres.travail.g_N.valeur) ** b * (1.0 + pi_barre) ** c)
    return facteur_par_pas(TauxDeCroissance(croissance - 1.0))


@dataclass(frozen=True)
class Carte:
    """Carte d'un pas ramenée au sentier : noms, point d'ouverture x0, échelles, x ↦ x_{t+1}/f."""

    noms: tuple[str, ...]
    x0: np.ndarray
    echelle: np.ndarray
    detendue: Callable[[np.ndarray], np.ndarray]


def carte_du_moteur(etat: object, ordonnanceur: object, noms: Sequence[str], pi_barre: float,
                    entrees: EntreesDuTour = EntreesDuTour((), ())) -> Carte:
    """Carte de `executer_pas` sur les variables d'état scalaires `noms` (positions, variables
    des blocs ; ni V^flux, recalculées, ni registre), autour de l'état d'ouverture `etat`,
    chaque variable ramenée au sentier par le facteur de son unité."""
    noms = tuple(noms)
    for nom in noms:
        variable = schema.VARIABLE.get(nom)
        if variable is None or variable.type is not float or nom in cat.VALEUR_NETTE_FLUX.values():
            raise ValueError(f"{nom!r} : variable d'état scalaire hors V^flux attendue")
    facteurs = np.array([facteur_de_tendance(schema.VARIABLE[n].unite, ordonnanceur.parametres,
                                             pi_barre) for n in noms])
    x0 = np.array([getattr(etat, n) for n in noms], dtype=float)
    echelle = np.where(np.abs(x0) > 0.0, np.abs(x0), PLANCHER_D_ECHELLE)

    def detendue(x: np.ndarray) -> np.ndarray:
        champs = {n: float(v) for n, v in zip(noms, x, strict=True)}
        positions = {p: champs.get(p, getattr(etat, p)) for p in cat.NOMS_POSTES}
        champs.update({cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(positions, s)
                       for s in cat.SECTEURS})
        suivant = executer_pas(dataclasses.replace(etat, **champs), entrees, ordonnanceur,
                               ObservateurNul())
        return np.array([getattr(suivant, n) for n in noms], dtype=float) / facteurs

    return Carte(noms, x0, echelle, detendue)


def residu_point_fixe(carte: Carte) -> float:
    """Plus grand écart du point fixe ramené au sentier, relatif à l'échelle de chaque variable."""
    return float(np.max(np.abs(carte.detendue(carte.x0) - carte.x0) / carte.echelle))


def jacobienne(carte: Carte, pas_relatif: float = PAS_RELATIF) -> np.ndarray:
    """Jacobienne de la carte ramenée au sentier au point x0, différences centrées, mise à
    l'échelle S⁻¹ J S (mêmes valeurs propres que J)."""
    k = len(carte.x0)
    jac = np.empty((k, k))
    for j in range(k):
        h = pas_relatif * carte.echelle[j]
        e = np.zeros(k)
        e[j] = h
        jac[:, j] = (carte.detendue(carte.x0 + e) - carte.detendue(carte.x0 - e)) / (2.0 * h)
    return jac * carte.echelle[None, :] / carte.echelle[:, None]


def valeurs_propres(carte: Carte, pas_relatif: float = PAS_RELATIF) -> np.ndarray:
    """Valeurs propres de la jacobienne, par module décroissant (puis parties réelle et
    imaginaire), ordre déterministe."""
    valeurs = np.linalg.eigvals(jacobienne(carte, pas_relatif))
    return np.array(sorted(valeurs, key=lambda z: (-abs(z), z.real, z.imag)))
