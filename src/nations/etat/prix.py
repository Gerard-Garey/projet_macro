"""Variable d'état du bloc 4, prix (radical `prix`), schéma v2.

Contrat : ADR 0012, G1 (a), et annotation du 13/11/2026, points 1.2 et 1.4
(P54, visa de `macro` sous conditions). μ̃ est la marge en logarithme,
μ̃_t = ln(p_t/UC_t) par construction (P2 puis P3), écrite en phase 5 ; à
l'ouverture du pas t, `mu_tilde` vaut μ̃_{t−1}, lue par `prix` (P2) et par
`travail` (ω_{t−1} = exp(−μ̃_{t−1}), T2). Valeur stationnaire : ln(1 + μ̄)
(`sec:prix-stationnaire`). Aucun domaine au-delà du type : μ̃ est de signe
quelconque (point 1.7).
"""

from __future__ import annotations

from nations.etat.variables import Invariance, scalaire

RADICAL = "prix"

VARIABLES = (
    scalaire("mu_tilde", RADICAL, "5", "sans dimension",
             "μ̃_{t−1} = ln(1 + μ̄) (sec:prix-stationnaire)", Invariance.SANS_DIMENSION),
)

# Domaines au chargement : aucun (μ̃ de signe quelconque).
DOMAINES: dict = {}
