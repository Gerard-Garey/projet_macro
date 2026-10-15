"""Diagnostics d'arrêt du moteur : des exceptions typées, à champs structurés.

Contrat : ADR 0012, B3, B4 et F1 ; même forme que les diagnostics du noyau
(`nations.noyau.diagnostics`, A6). Deux familles, dérivées de `ArretMoteur` :

- `DefautDeDeclaration`, levée **avant le premier pas** : déclaration d'un
  paramètre hors de son domaine ou de son vocabulaire (F1, F2), déclaration
  de bloc refusée par le contrôle statique de l'assemblage (B3) ;
- `RefusDuMoteur`, levée **au moment de l'appel**, pendant un pas : écriture
  d'une variable du pas non déclarée ou déjà écrite, lecture d'une variable
  non déclarée ou non encore écrite, écriture d'une variable d'état hors de
  son propriétaire, de sa phase ou de son type, variable d'état non écrite à
  la couche moteur de la phase 9, entrées du tour non déclarées (B4, C2, B5).

Le moteur ne rattrape jamais un arrêt pour continuer, ni du noyau ni le sien :
l'état d'ouverture reste intact (gelé), et aucun état t + 1 n'est rendu.
"""

from __future__ import annotations


class ArretMoteur(Exception):
    """Arrêt du moteur, avec ses champs structurés.

    Champs : pas `t` ; `etape` (phase ou sous-phase : `"8b"`) ; `bloc`
    (radical de l'écrivain, `moteur` compris) ; `nom` (variable, paramètre,
    ligne ou lecture en cause). Un champ sans objet vaut `None`.
    """

    def __init__(
        self,
        message: str,
        *,
        t: int | None = None,
        etape: str | None = None,
        bloc: str | None = None,
        nom: str | None = None,
    ) -> None:
        self.t = t
        self.etape = etape
        self.bloc = bloc
        self.nom = nom
        self.message = message
        super().__init__(self._composer())

    def _composer(self) -> str:
        """Message en français qui nomme le pas, l'étape, le bloc et le nom renseignés."""
        parties = []
        if self.t is not None:
            parties.append(f"pas {self.t}")
        if self.etape is not None:
            parties.append(f"phase {self.etape}")
        if self.bloc is not None:
            parties.append(f"bloc {self.bloc}")
        if self.nom is not None:
            parties.append(f"« {self.nom} »")
        tete = ", ".join(parties)
        return f"{tete} : {self.message}" if tete else self.message


class DefautDeDeclaration(ArretMoteur):
    """Déclaration refusée avant le premier pas : paramètre (F1) ou assemblage (B3)."""


class RefusDuMoteur(ArretMoteur):
    """Refus levé au moment de l'appel, pendant un pas (B4, C2, B5)."""
