"""Variable d'état du bloc 4, prix (radical `prix`), schéma v2.

Contrat : ADR 0012, G1 (a), et annotation du 13/11/2026, points 1.2 et 1.4
(P54, visa de `macro` sous conditions). μ̃ est la marge en logarithme,
μ̃_t = ln(p_t/UC_t) par construction (P2 puis P3), écrite en phase 5 ; à
l'ouverture du pas t, `mu_tilde` vaut μ̃_{t−1}, lue par `prix` (P2) et par
`travail` (ω_{t−1} = exp(−μ̃_{t−1}), T2). Valeur stationnaire : ln(1 + μ̄)
(`sec:prix-stationnaire`).

Domaine au chargement : un **domaine de représentabilité**, sans contenu
économique (ADR 0016, points 16 à 18.1 ; décision du mainteneur du
27/11/2026, point 2 ; #158) : |μ̃| ≤ ln(DBL_MAX), borne calculée depuis
`sys.float_info.max`, jamais écrite en littéral. Propriété garantie :
**finitude** de e^{μ̃} (P3) et de e^{−μ̃} (T2), non leur normalité (e^{−L}
est sous-normal). μ̃ reste de signe quelconque (ADR 0012, annotation du
13/11/2026, point 1.7, étendu par l'ADR 0016, point 18.1). Refusé par
`schema.defaut_de_domaine` sous la forme « <valeur> hors du domaine
<condition> », qui refuse aussi `NaN` et ±∞, sans écrêtage : par
`ValueError` à la construction d'un `EtatPays`, par `SauvegardeRefusee` à la
reprise, par `RefusDuMoteur` à l'écriture en phase 5 (`Vue.ecrire_etat`).
"""

from __future__ import annotations

import math
import sys

from nations.etat.variables import Invariance, scalaire

RADICAL = "prix"

VARIABLES = (
    scalaire("mu_tilde", RADICAL, "5", "sans dimension",
             "μ̃_{t−1} = ln(1 + μ̄) (sec:prix-stationnaire)", Invariance.SANS_DIMENSION),
)

# Borne du domaine de représentabilité de μ̃ : L = ln(DBL_MAX). Pour |x| ≤ L, exp(x) et exp(−x)
# sont finis ; exp(nextafter(L, +∞)) déborde (ADR 0016, point 17.1 : calculée, jamais un littéral).
BORNE_MU_TILDE = math.log(sys.float_info.max)

# Domaines au chargement : nom → (condition en clair, prédicat de la condition).
DOMAINES = {
    "mu_tilde": ("|μ̃| ≤ ln(DBL_MAX) (e^{μ̃} et e^{−μ̃} finis : eq:prix-prix-du-pas, "
                 "eq:travail-salaire-relatif)",
                 lambda x: -BORNE_MU_TILDE <= x <= BORNE_MU_TILDE),
}
