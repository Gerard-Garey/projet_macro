"""Relevé des résidus des identités du noyau : la mesure du jalon J2 (ADR 0012, E2).

`ReleveDesResidus` est un observateur (E1) : il tient, hors de l'état, pour
chaque clôture de phase, le rapport résidu / S de chaque identité vérifiée
(instance la plus éloignée de zéro, `ClotureDePhase.rapports`) et, en phase 9,
l'écart |V^stock − V^flux| / S de chaque secteur. Il publie deux grandeurs,
chacune avec sa définition, son unité, son dénominateur et sa fenêtre
(`grandeurs`) :

- le **maximum sur la fenêtre** du rapport résidu / S, par identité ;
- la **trajectoire de l'accumulation** de l'identité cumulée
  (`eq:noyau-tolerance-cumulee`), par secteur, un point par pas.

Unité : sans dimension (résidu / S). Dénominateur : S, échelle du bilan
évaluée à l'ouverture du pas (P33 (a)) ; pour une identité de ligne, le plus
petit S des secteurs touchés (lecture (α)). Fenêtre : les pas relevés, du
premier au dernier, nommés par `grandeurs` ; la mesure du jalon la porte à 720
pas (#98).

Les relevés sont datés par (t, phase) : après une reprise, un relevé neuf
continue la série, et la concaténation des deux relevés égale, bit à bit, le
relevé d'une trajectoire sans interruption (C96-3), S étant recalculée à
l'ouverture de chaque pas.
"""

from __future__ import annotations

from dataclasses import dataclass

from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import Evenement, FinDePas

# Règle de l'identité cumulée, telle que la nomment les rapports de la phase 9.
IDENTITE_CUMULEE = "eq:noyau-tolerance-cumulee"


@dataclass(frozen=True, slots=True)
class Grandeur:
    """Une grandeur publiée : définition, unité, dénominateur, fenêtre."""

    nom: str
    definition: str
    unite: str
    denominateur: str
    fenetre: str


class ReleveDesResidus:
    """Observateur qui relève les rapports résidu / S de chaque clôture (E2)."""

    __slots__ = ("_pas", "_releves")

    def __init__(self) -> None:
        # (t, phase, règle, objet, rapport), dans l'ordre des clôtures.
        self._releves: list[tuple[int, str, str, str, float]] = []
        # Pas clos relevés (FinDePas), dans l'ordre.
        self._pas: list[int] = []

    def relever(self, evenement: Evenement) -> None:
        if type(evenement) is ClotureDePhase:
            for regle, objet, rapport in evenement.rapports:
                self._releves.append((evenement.t, evenement.phase, regle, objet, rapport))
        elif type(evenement) is FinDePas:
            self._pas.append(evenement.t)
        else:
            raise TypeError(f"événement d'observation inconnu : {type(evenement).__name__}")

    def releves(self) -> tuple[tuple[int, str, str, str, float], ...]:
        """Tous les relevés : (t, phase, règle, objet, rapport résidu / S)."""
        return tuple(self._releves)

    def pas(self) -> tuple[int, ...]:
        """Pas clos relevés."""
        return tuple(self._pas)

    def maximum(self, regle: str) -> tuple[float, int | None, str | None, str | None]:
        """Maximum sur la fenêtre du rapport résidu / S d'une identité : (rapport, t, phase, objet).

        Le premier relevé qui atteint le maximum ; un rapport nul et trois
        `None` si tous les relevés de la règle sont nuls, ou s'il n'y en a aucun.
        """
        pire: tuple[float, int | None, str | None, str | None] = (0.0, None, None, None)
        for t, phase, nom, objet, rapport in self._releves:
            if nom == regle and pire[0] < rapport:
                pire = (rapport, t, phase, objet)
        return pire

    def accumulation(self, secteur: str) -> tuple[tuple[int, float], ...]:
        """Trajectoire de |V^stock − V^flux| / S du secteur : (t, rapport), un point par pas."""
        return tuple((t, rapport) for t, phase, nom, objet, rapport in self._releves
                     if nom == IDENTITE_CUMULEE and objet == secteur)

    def grandeurs(self) -> tuple[Grandeur, Grandeur]:
        """Les deux grandeurs publiées, avec la fenêtre effectivement relevée."""
        if self._pas:
            fenetre = (f"pas {self._pas[0]} à {self._pas[-1]} ({len(self._pas)} pas clos "
                       "relevés)")
        else:
            fenetre = "aucun pas clos relevé"
        denominateur = ("S, échelle du bilan du secteur évaluée à l'ouverture du pas ; pour une "
                        "identité de ligne, plus petit S des secteurs touchés (lecture (α))")
        return (
            Grandeur("résidu / S maximal, par identité",
                     "maximum, sur toutes les clôtures de phase de la fenêtre, du rapport "
                     "|résidu| / S de l'instance la plus éloignée de zéro de chaque identité",
                     "sans dimension", denominateur, fenetre),
            Grandeur("accumulation de l'identité cumulée, par secteur",
                     "|V^stock − V^flux| / S à la clôture de la phase 9 de chaque pas",
                     "sans dimension", "S, échelle du bilan du secteur évaluée à l'ouverture "
                     "du pas", fenetre),
        )
