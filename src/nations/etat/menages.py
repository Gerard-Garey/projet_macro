"""Variable d'état du bloc 5, ménages (radical `menages`) : le revenu disponible du pas
précédent YD_{t−1} (schéma v4).

Contrat : ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1), point 1 (P127 : suffixe
`_m1` pour toute variable d'état qui retient une grandeur du pas) ; spécification,
`sec:menages-revenu` et `tab:menages-phases` ; fiche `docs/blocs/menages.md`, § 9.1 et
§ 9.4 ; issue #60. YD_t est écrit en phase 9, groupe des blocs (H7, sur les montants exécutés
du pas, décision M29) ; à l'ouverture du pas t, `YD_m1` vaut YD_{t−1}, lu par le bloc en
phase 2 (H2). Unité « u.m. par pas », nominale. Valeur stationnaire et initiale :
YD_0/Γ̄ (`sec:menages-stationnaire`, « État initial résolu » ; clé `YD_m1` de `ouverture()`
du script d'état stationnaire).

Domaine (point 1) : **finitude seule, déclarée**, sans condition de signe (YD < 0 est possible
si les impôts excèdent les revenus ; le plancher de H5 le traite) ; elle est contrôlée par
`schema.defaut_de_domaine` pour toute variable `float`, d'où aucune entrée dans `DOMAINES`.
"""

from __future__ import annotations

from nations.etat.variables import Invariance, scalaire

RADICAL = "menages"

VARIABLES = (
    scalaire("YD_m1", RADICAL, "9", "u.m. par pas",
             "YD_{t−1} = YD_t/Γ̄ (sec:menages-stationnaire)", Invariance.NOMINAL),
)

# Domaines au chargement : aucun au-delà de la finitude (point 1), contrôlée par le schéma.
DOMAINES: dict = {}
