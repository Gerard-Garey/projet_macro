"""Les deux conversions d'un taux annuel au pas, et elles seules.

Contrat : ADR 0012, F2 ; ADR 0005, point 4 (annoté le 03/10/2026) ; ADR 0008,
partie I ; spécification, `sec:cadre-calendrier`, « Deux conversions, selon
la nature du taux ».

- `par_pas(TauxDeFlux)` : conversion **linéaire**, x/n_a, pour les taux
  d'intérêt, les flux annuels et les vitesses d'ajustement ;
- `facteur_par_pas(TauxDeCroissance)` : conversion **géométrique**,
  (1 + x)^{1/n_a}, facteur par pas d'un niveau qui croît au taux annuel x
  (croissance, inflation).

Chacune n'accepte que son type, construit depuis l'unité du taux
(`nations.moteur.parametres.taux_du_parametre`) : aucune fonction ne prend la
nature en argument (ADR 0008, I.3). Ce sont les deux seuls endroits de `src/`
où un taux est divisé par n_a ou élevé à la puissance 1/n_a (test « conversion
unique » de #98). Le noyau ne convertit rien : les montants lui arrivent en
u.m. par pas.
"""

from __future__ import annotations

from nations.moteur.parametres import TauxDeCroissance, TauxDeFlux
from nations.moteur.parametres.cadre import PAS_PAR_AN


def par_pas(taux: TauxDeFlux) -> float:
    """Taux de flux par pas : x^pas = x^an / n_a (conversion linéaire)."""
    if type(taux) is not TauxDeFlux:
        raise TypeError(f"par_pas : TauxDeFlux attendu, {type(taux).__name__} reçu")
    return taux.valeur / PAS_PAR_AN.valeur


def facteur_par_pas(taux: TauxDeCroissance) -> float:
    """Facteur de croissance par pas : 1 + x^pas = (1 + x^an)^{1/n_a} (conversion géométrique)."""
    if type(taux) is not TauxDeCroissance:
        raise TypeError(f"facteur_par_pas : TauxDeCroissance attendu, {type(taux).__name__} reçu")
    return (1.0 + taux.valeur) ** (1.0 / PAS_PAR_AN.valeur)
