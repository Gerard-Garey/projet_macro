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
    """Fin du pas t : l'état t + 1 assemblé, les variables du pas et les grandeurs calculées à
    l'ouverture (ADR 0012, B5.3 et E1 ; annotation du 07/10/2026, point 2).

    - `etat` : état d'ouverture du pas t + 1 ;
    - `variables_du_pas` : (nom, valeur) des variables du pas écrites
      (entrées du tour, variables des blocs, valeurs du pas suivant des
      variables d'état sous `<nom>_suivant`), grandeurs d'ouverture exclues ;
    - `grandeurs_ouverture` : (nom, valeur) des grandeurs calculées à
      l'ouverture du pas t.

    Valeurs de types de base (`float`, `int`, `bool`, n-uplet de `float`),
    dans l'ordre d'inscription à l'assemblage, qui ne dépend pas de l'ordre
    de la liste de blocs. Les montants exécutés des lignes sont dans les
    clôtures de phase relevées.
    """

    t: int
    etat: EtatPays
    variables_du_pas: tuple[tuple[str, object], ...]
    grandeurs_ouverture: tuple[tuple[str, object], ...]


Evenement = ClotureDePhase | FinDePas


class Observateur(Protocol):
    """Un observateur reçoit des valeurs immuables et ne rend rien."""

    def relever(self, evenement: Evenement) -> None: ...


class ObservateurNul:
    """Observateur par défaut du moteur : ne fait rien."""

    __slots__ = ()

    def relever(self, evenement: Evenement) -> None:
        return None
