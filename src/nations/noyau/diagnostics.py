"""Diagnostics d'arrêt du noyau : des exceptions typées, à champs structurés.

Contrat : ADR 0012, A6. Deux familles, dérivées de `ArretNoyau` :

- `RefusDeProposition`, levée **au moment de l'appel** : proposition ou
  déclaration hors du catalogue, de la phase, du domaine ou du proposant
  déclaré ; lecture avant clôture ; affectation hors d'une ligne ; appel hors
  de l'ordre des clôtures ; ligne oubliée, relevée à la clôture de sa phase ;
- `DefautComptable`, levée **à la clôture** : identité, caisse, réserves de
  clôture, valeur nette, échelle nulle.

Le noyau ne rationne ni n'ajuste jamais : une violation arrête l'exécution, et
le diagnostic remonte à l'appelant. Le moteur ne rattrape jamais un
`ArretNoyau` pour continuer (ADR 0012, A6 ; ADR 0011, P4).
"""

from __future__ import annotations

import math


def rapport_a_l_echelle(residu: float, echelle: float) -> float:
    """|résidu| / S, sans division par une échelle nulle.

    Une échelle nulle ne survient que pour une ligne dont aucun montant n'est
    non nul (ADR 0012, point 9) : le résidu y est alors nul par construction,
    et le rapport vaut 0 ; un résidu non nul sur une échelle nulle vaut l'infini.
    """
    try:
        return abs(residu) / echelle
    except ZeroDivisionError:
        return 0.0 if residu == 0.0 else math.inf


class ArretNoyau(Exception):
    """Arrêt du noyau, avec ses champs structurés (ADR 0012, A6).

    Champs : pas `t` ; `phase` (sous-phase comprise : `"8b"`) ; `regle`
    (label `eq:` de l'identité ou nom de la règle) ; `secteur` (ou payeur) ;
    `ligne` et `terme` s'il y a lieu ; `residu`, `echelle` (S), `rapport`
    (résidu / S) et `tolerance` (ε ou ε_V) pour une identité ; `moyen`
    (moyen de paiement), `position_debut` et `position_fin` de phase
    rapportées à S, et `lignes_debitrices` (lignes de la phase qui débitent
    le moyen) pour un défaut de caisse. Un champ sans objet vaut `None`.
    """

    def __init__(
        self,
        message: str,
        *,
        t: int | None = None,
        phase: str | None = None,
        regle: str | None = None,
        secteur: str | None = None,
        ligne: str | None = None,
        terme: str | None = None,
        residu: float | None = None,
        echelle: float | None = None,
        tolerance: float | None = None,
        moyen: str | None = None,
        position_debut: float | None = None,
        position_fin: float | None = None,
        lignes_debitrices: tuple[str, ...] | None = None,
    ) -> None:
        self.t = t
        self.phase = phase
        self.regle = regle
        self.secteur = secteur
        self.ligne = ligne
        self.terme = terme
        self.residu = residu
        self.echelle = echelle
        self.rapport = (None if residu is None or echelle is None
                        else rapport_a_l_echelle(residu, echelle))
        self.tolerance = tolerance
        self.moyen = moyen
        self.position_debut = position_debut
        self.position_fin = position_fin
        self.lignes_debitrices = lignes_debitrices
        self.message = message
        super().__init__(self._composer())

    def _composer(self) -> str:
        """Message en français qui nomme le pas, la phase et les champs renseignés."""
        parties = []
        if self.t is not None:
            parties.append(f"pas {self.t}")
        if self.phase is not None:
            parties.append(f"phase {self.phase}")
        if self.regle is not None:
            parties.append(self.regle)
        tete = ", ".join(parties)
        details = []
        if self.secteur is not None:
            details.append(f"secteur {self.secteur}")
        if self.ligne is not None:
            details.append(f"ligne {self.ligne}")
        if self.terme is not None:
            details.append(f"terme {self.terme}")
        if self.moyen is not None:
            details.append(f"moyen de paiement {self.moyen}")
        if self.position_debut is not None:
            details.append(f"position en début de phase {self.position_debut!r} × S")
        if self.position_fin is not None:
            details.append(f"position en fin de phase {self.position_fin!r} × S")
        if self.lignes_debitrices is not None:
            details.append("lignes de la phase qui le débitent : "
                           + (", ".join(self.lignes_debitrices) or "aucune"))
        if self.residu is not None:
            details.append(f"résidu {self.residu!r}")
        if self.echelle is not None:
            details.append(f"S {self.echelle!r}")
        if self.rapport is not None:
            details.append(f"résidu/S {self.rapport!r}")
        if self.tolerance is not None:
            details.append(f"tolérance {self.tolerance!r}")
        texte = self.message
        if tete:
            texte = f"{tete} : {texte}"
        if details:
            texte = f"{texte} ({' ; '.join(details)})"
        return texte


class RefusDeProposition(ArretNoyau):
    """Refus levé au moment de l'appel (ADR 0012, A3.2 et A6)."""


class DefautComptable(ArretNoyau):
    """Défaut relevé à la clôture d'une phase (ADR 0012, A5 et A6)."""
