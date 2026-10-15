"""Relevé du coût de calcul d'un pas : la seconde mesure publiée du jalon J2 (#98).

`ReleveDuCout` est un observateur (ADR 0012, E1) : il lit l'horloge à
`demarrer`, puis à chaque fin de pas (`FinDePas`) ; il ignore les clôtures de
phase (`ClotureDePhase`), refuse tout autre événement (`TypeError`, comme
`ReleveDesResidus`), ne lit rien d'autre et n'a aucun effet sur la
trajectoire. Il publie le **coût par pas** :

- définition : durée écoulée entre `demarrer` et la dernière fin de pas
  relevée, divisée par le nombre de pas relevés ; elle couvre tout ce que
  l'appelant exécute entre ces deux instants (au jalon J2 : `executer_pas`,
  soit l'ordonnanceur, le noyau et le registre, sur des propositions
  précalculées puis rejouées) ;
- unité : milliseconde par pas mensuel, pour un pays ;
- dénominateur : nombre de pas clos relevés ;
- fenêtre : les pas relevés, du premier au dernier.

L'horloge est un argument du constructeur (`time.perf_counter` par défaut),
ce qui permet de vérifier le calcul sur une horloge d'essai.
"""

from __future__ import annotations

import time
from collections.abc import Callable

from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import Evenement, FinDePas
from nations.observation.residus import Grandeur


class ReleveDuCout:
    """Observateur qui relève l'horloge à chaque fin de pas, après `demarrer`."""

    __slots__ = ("_debut", "_fins", "_horloge", "_pas")

    def __init__(self, horloge: Callable[[], float] = time.perf_counter) -> None:
        self._horloge = horloge
        self._debut: float | None = None
        # Instants des fins de pas et pas clos relevés, dans l'ordre.
        self._fins: list[float] = []
        self._pas: list[int] = []

    def demarrer(self) -> None:
        """Lit l'horloge au début de la fenêtre ; refusé une seconde fois."""
        if self._debut is not None:
            raise RuntimeError("relevé du coût déjà démarré")
        self._debut = self._horloge()

    def relever(self, evenement: Evenement) -> None:
        if type(evenement) is ClotureDePhase:
            return
        if type(evenement) is not FinDePas:
            raise TypeError(f"événement d'observation inconnu : {type(evenement).__name__}")
        if self._debut is None:
            raise RuntimeError("fin de pas relevée avant le démarrage du relevé du coût")
        self._fins.append(self._horloge())
        self._pas.append(evenement.t)

    def pas(self) -> tuple[int, ...]:
        """Pas clos relevés."""
        return tuple(self._pas)

    def cout_par_pas(self) -> float:
        """Coût moyen d'un pas, en millisecondes : (dernière fin − début) / nombre de pas."""
        if not self._fins:
            raise RuntimeError("aucun pas clos relevé")
        return (self._fins[-1] - self._debut) * 1e3 / len(self._fins)

    def grandeur(self) -> Grandeur:
        """La grandeur publiée, avec la fenêtre effectivement relevée."""
        if self._pas:
            fenetre = f"pas {self._pas[0]} à {self._pas[-1]} ({len(self._pas)} pas clos relevés)"
        else:
            fenetre = "aucun pas clos relevé"
        return Grandeur(
            "coût par pas",
            "durée entre le démarrage du relevé et la dernière fin de pas, divisée par le "
            "nombre de pas clos relevés",
            "ms par pas mensuel, pour un pays", "nombre de pas clos relevés", fenetre)
