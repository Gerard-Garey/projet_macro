"""Grandeurs calculées à l'ouverture du pas (phase 0).

Contrat : ADR 0012, C3 ; ADR 0010 (mécanisme seulement, P34 (a)). Une
grandeur calculée à l'ouverture (`GrandeurOuverture`) est calculée **une
fois par pas, dans l'ordre de `GRANDEURS_OUVERTURE`**, par une fonction de
l'état d'ouverture, des paramètres et des grandeurs qui la précèdent
(triangulaire) ; elle est déposée dans l'espace du pas sous son nom, lisible
par tout bloc dès la phase 1 (source `"0"`). Ce n'est **jamais une variable
d'état** : elle n'est pas sauvegardée.

Au J2, la séquence porte la date affichée (année, mois) et le prédicat de date
de décision ; au J3, #61 y ajoute Γ^e_t, γ^e_t et π^{∗,pas}_t, sans changer
aucune signature.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

from nations.etat.unites import UNITES
from nations.moteur import calendrier

# Préfixe d'un label d'équation (`CONVENTIONS.md` § 2.1).
_PREFIXE_DE_LABEL = "eq:"


@dataclass(frozen=True, slots=True)
class GrandeurOuverture:
    """Une grandeur calculée à l'ouverture (C3), immuable.

    - `nom` : nom dans l'espace du pas ;
    - `fonction` : (état d'ouverture, paramètres, grandeurs déjà calculées) → valeur ;
    - `label` : label `eq:` de l'équation qui la définit, ou `None` ;
    - `unite` : dans `UNITES`.
    """

    nom: str
    fonction: Callable[[object, object, Mapping[str, object]], object]
    label: str | None
    unite: str

    def __post_init__(self) -> None:
        if not self.nom.isidentifier() or not self.nom.isascii():
            raise ValueError(f"nom de grandeur d'ouverture invalide : {self.nom!r}")
        if self.label is not None and not self.label.startswith(_PREFIXE_DE_LABEL):
            raise ValueError(f"{self.nom} : label {self.label!r} invalide")
        if self.unite not in UNITES:
            raise ValueError(f"{self.nom} : unité {self.unite!r} hors du vocabulaire")


def _annee(etat: object, parametres: object, grandeurs: Mapping[str, object]) -> int:
    return calendrier.date(etat.t)[0]


def _mois(etat: object, parametres: object, grandeurs: Mapping[str, object]) -> int:
    return calendrier.date(etat.t)[1]


def _date_de_decision(etat: object, parametres: object, grandeurs: Mapping[str, object]) -> bool:
    return calendrier.est_date_de_decision(etat.t)


GRANDEURS_OUVERTURE = (
    # Année et mois affichés : des rangs, non des durées (« années » reste l'unité
    # des durées et des horizons) ; leur type porte la nature (annotation du
    # 07/10/2026, point 6).
    GrandeurOuverture("annee", _annee, "eq:moteur-calendrier-date", "sans dimension"),
    GrandeurOuverture("mois", _mois, "eq:moteur-calendrier-date", "sans dimension"),
    GrandeurOuverture("date_de_decision", _date_de_decision, "eq:moteur-date-decision",
                      "sans dimension"),
)
