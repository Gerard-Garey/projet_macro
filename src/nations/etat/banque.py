"""Variables d'état du bloc 7, banque commerciale (radical `banque`) : les taux des
crédits i_L et des dépôts i_D (schéma v3).

Contrat : ADR 0013, annotation du 14/11/2026, points 3 et 4 (P96 ; #90) ;
spécification, `sec:banque-taux` et `tab:banque-phases`. i_L et i_D sont écrits
en phase 8 (c) du pas t (B1, B2), sur le taux directeur du tour ; à l'ouverture
du pas t, `i_L` vaut i_{L,t} et `i_D` vaut i_{D,t}, lus par la banque en phase 6
(B3 à B5) et, au J3-d, par le bloc investissement (phases 2 et 6, condition
C27). Unité « par an, taux de flux », convertie au pas par la seule conversion
linéaire. Valeurs stationnaires et initiales : i_CB + ϖ_L et i_CB − ϖ_D
(`sec:banque-stationnaire`, « État initial résolu »).

Domaine (point 4) : **finitude seule, déclarée**, sans condition de signe (i_D
est négatif dès que i_CB < ϖ_D, sans plancher : M31, lecture (d)) ; elle est
contrôlée par `schema.defaut_de_domaine` pour toute variable `float`, d'où
aucune entrée dans `DOMAINES`.
"""

from __future__ import annotations

from nations.etat.variables import Invariance, scalaire

RADICAL = "banque"

VARIABLES = (
    scalaire("i_L", RADICAL, "8c", "par an, taux de flux",
             "i_{L,t} = i_CB + ϖ_L (sec:banque-stationnaire)", Invariance.SANS_DIMENSION),
    scalaire("i_D", RADICAL, "8c", "par an, taux de flux",
             "i_{D,t} = i_CB − ϖ_D (sec:banque-stationnaire)", Invariance.SANS_DIMENSION),
)

# Domaines au chargement : aucun au-delà de la finitude (point 4), contrôlée par le schéma.
DOMAINES: dict = {}
