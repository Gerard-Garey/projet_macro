"""Protocole d'observation : ce que le moteur relève, sans effet sur la trajectoire.

Contrat : ADR 0012, E1. Le moteur (#97), et lui seul, appelle
`observateur.relever(evenement)` après chaque clôture de phase (une
`ClotureDePhase` du noyau) et après l'assemblage de l'état t + 1 (une
`FinDePas`). Les événements sont des valeurs immuables ; `relever` ne rend
rien. Aucun module de `noyau/`, `etat/` ou `blocs/` n'importe `observation/`,
et le moteur n'en importe que le présent protocole : aucun contrôle ne lit un
relevé (test du graphe d'imports). Test de suppression : une trajectoire
observée par `ObservateurNul` ou par un enregistreur donne des sauvegardes
identiques à l'octet.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from nations.etat.schema import EtatPays
from nations.noyau.grand_livre import ClotureDePhase


@dataclass(frozen=True, slots=True)
class FinDePas:
    """Fin du pas t : l'état t + 1 assemblé (ADR 0012, B5.3 et E1).

    Le moteur (#97) y ajoutera les variables du pas et les grandeurs calculées
    à l'ouverture ; les montants exécutés des lignes sont déjà dans les
    clôtures de phase relevées.
    """

    t: int
    etat: EtatPays


Evenement = ClotureDePhase | FinDePas


class Observateur(Protocol):
    """Un observateur reçoit des valeurs immuables et ne rend rien."""

    def relever(self, evenement: Evenement) -> None: ...


class ObservateurNul:
    """Observateur par défaut du moteur : ne fait rien."""

    __slots__ = ()

    def relever(self, evenement: Evenement) -> None:
        return None
