"""Variable d'état du bloc 9, État et dette (radical `finances_publiques`) : l'assiette de l'impôt
des ménages Y^HS_{t−1} (schéma v5).

Contrat : ADR 0013, annotation du 15/11/2026 (rang 1b de J3-d2), point 2 (P127 : suffixe `_m1`
pour toute variable d'état qui retient une grandeur du pas) ; spécification,
`sec:finances_publiques-assiette`, `sec:finances_publiques-phases` et
`tab:finances_publiques-phases` ; fiche `docs/blocs/finances_publiques.md`, § 9.4 ; issue #132.
Y^HS_t est écrite par le bloc en **phase 7** (E12, ADR 0011, point P3), jamais dans le groupe de
la phase 9 ; à l'ouverture du pas t, `Y_HS_m1` vaut Y^HS_{t−1}, lue par le bloc en phase 2 (E3).
Unité « u.m. par pas », nominale. Valeur stationnaire et initiale : Y^HS_0/Γ̄
(`sec:finances_publiques-assiette`, `\\limites` ; clé `Y_HS_m1` de `ouverture()` du script d'état
stationnaire).

Domaine (point 2) : **finitude seule, déclarée**, sans condition de signe (T^cou et l'érosion des
dépôts admettent Y^HS < 0) ; elle est contrôlée par `schema.defaut_de_domaine` pour toute
variable `float`, d'où aucune entrée dans `DOMAINES`.
"""

from __future__ import annotations

from nations.etat.variables import Invariance, scalaire

RADICAL = "finances_publiques"

VARIABLES = (
    scalaire("Y_HS_m1", RADICAL, "7", "u.m. par pas",
             "Y^HS_{t−1} = Y^HS_t/Γ̄ (sec:finances_publiques-assiette)", Invariance.NOMINAL),
)

# Domaines au chargement : aucun au-delà de la finitude (point 2), contrôlée par le schéma.
DOMAINES: dict = {}
