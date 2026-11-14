"""Variables d'état du bloc 6, investissement et financement des entreprises (radical
`investissement`) : la part d'investissement visée ti, la production du pas précédent y_{t−1},
l'impôt des entreprises du pas précédent T_{F,t−1} et la norme résolue du taux réel du crédit
ϱ̄_L (schéma v4).

Contrat : ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1), point 1 (P127 : suffixe `_m1`
pour toute variable d'état qui retient une grandeur du pas ; P128 : ϱ̄_L variable d'état du bloc,
recopiée de l'ouverture à chaque pas, en phase 2, contrat C2 inchangé) ; spécification,
`sec:investissement-phases`, `tab:investissement-phases` et `sec:investissement-stationnaire`
(« État initial résolu ») ; fiche `docs/blocs/investissement.md`, § 9.2 et § 9.4 ; issue #67.
Valeurs stationnaires et initiales : clés `ti`, `y_m1`, `T_F_m1` et `rho_bar_L` de `ouverture()`
du script d'état stationnaire (le script nomme `rho_bar_L` ce que le schéma nomme
`varrho_bar_L`).

- `ti` (phase 5, S6) : ti_t, fraction de la production attendue, sans dimension ;
- `y_m1` (phase 5) : y_t retenue comme y_{t−1} du pas suivant, u.v. par pas, volume ;
- `T_F_m1` (phase 9, groupe des blocs ; décision M29) : montant exécuté de la ligne 7 dans la
  colonne des entreprises, T_{F,t}, retenu comme T_{F,t−1}, u.m. par pas, nominale ; nulle au
  socle (τ_F = 0, M33) ;
- `varrho_bar_L` (phase 2, recopie) : ϱ̄_L = ϱ_{L,0}, constante résolue, par an, taux de Fisher
  employé en base annuelle sans conversion (unité de r̄ et de r̂*).

Domaines au chargement (point 1 ; visa de `macro` au rang 4), refusés par
`schema.defaut_de_domaine` sous la forme « <valeur> hors du domaine <condition> », qui refuse
aussi `NaN`, sans écrêtage : **ti > 0** et **y_m1 ≥ 0**, condition de forme qui tient
I^{vol,plan} ≥ 0 par S3 et I^plan ≥ 0 par S4 avec P_{t−1} > 0 (point 4 ; P120) ; T_F_m1 et
varrho_bar_L : **finitude seule, déclarée** (T_F < 0 possible sous un résultat avant impôt
négatif ; ϱ̄_L sans condition de signe), contrôlée par le schéma pour toute variable `float`.
"""

from __future__ import annotations

from nations.etat.variables import Invariance, scalaire

RADICAL = "investissement"

VARIABLES = (
    scalaire("ti", RADICAL, "5", "fraction",
             "ti_0 = (n_a[(1 + g)^{1/n_a} − 1] + δ) κ/t̄u (sec:investissement-stationnaire)",
             Invariance.SANS_DIMENSION),
    scalaire("y_m1", RADICAL, "5", "u.v. par pas",
             "y_{−1} = y_0/(1 + g)^{1/n_a} (sec:investissement-stationnaire)",
             Invariance.VOLUME),
    scalaire("T_F_m1", RADICAL, "9", "u.m. par pas",
             "T_{F,−1} = T_{F,0}/Γ̄ (sec:investissement-stationnaire) ; nulle au socle (M33)",
             Invariance.NOMINAL),
    scalaire("varrho_bar_L", RADICAL, "2", "par an, taux de croissance",
             "ϱ̄_L = ϱ_{L,0} = r̄ + ϖ_L/(1 + π*) (sec:banque-taux ; "
             "sec:investissement-stationnaire)", Invariance.SANS_DIMENSION),
)

# Domaines au chargement : nom → (condition en clair, prédicat de la condition).
DOMAINES = {
    "ti": ("ti > 0 (S3 : I^{vol,plan} ≥ 0 par la forme ; S6 : forme exponentielle)",
           lambda x: x > 0.0),
    "y_m1": ("y_{t−1} ≥ 0 (S3 : I^{vol,plan} ≥ 0 par la forme)", lambda x: x >= 0.0),
}
