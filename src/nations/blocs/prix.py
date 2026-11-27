"""Bloc 4, prix (radical `prix`).

Contrat : décision M26 (option M, base UC écrite par le bloc 2 en phase 2,
terme ξ, lecture (c) de P_t) ; spécification, `sec:prix` et `tab:prix-phases` ;
fiche `docs/blocs/prix.md`, § 9.1 à 9.6 ; ADR 0008, partie II (registre de 13
niveaux, P_t entré au registre par le moteur en phase 9) ; ADR 0012,
annotation du 13/11/2026 (noms, lectures, tables ; point 1.4 pour μ̃) ;
décision P54 (μ̃ variable d'état du bloc 4, visa de `macro` sous conditions) ;
issue #51.

**Équations.** P1 à P4 de la spécification sont des fonctions pures du
module, appelables directement, qui reçoivent des scalaires (taux déjà
convertis au pas) ; la méthode de phase lit la vue, convertit λ_μ par
`nations.moteur.conversions` seulement, appelle ces fonctions et écrit. Les
labels `eq:prix-…` (fiche, § 9.1 ; `eq:prix-indice`, P34 (a)) et leurs balises
sont posés ensemble (P62, rang 8 de J3-b) ; chaque équation porte sa balise
et garde son identifiant P1 à P4.

**P2 sous P54, option (ii)** : la marge d'ouverture ln(p_{t−1}/UC_{t−1}) est la
variable d'état μ̃_{t−1}, écrite au pas précédent par ce bloc : μ̃_t =
(1 − λ_μ/n_a) μ̃_{t−1} + (λ_μ/n_a)[ln(1 + μ̄) + ψ_ξ ξ_t]. P3 donne
μ̃_t = ln(p_t/UC_t) par construction (à l'arrondi près) : c'est la valeur
écrite, lue au pas suivant par ce bloc (P2) et par le bloc 3
(ω_{t−1} = exp(−μ̃_{t−1}), T2). Aucun recalcul de pr_{t−1} (N9 n'est pas
inversée), aucune lecture du registre. À l'état initial résolu,
μ̃_{−1} = ln(1 + μ̄) (`sec:prix-stationnaire`).

**Phase** (`tab:prix-phases` ; ADR 0012, annotation du 13/11/2026, points 2.2,
2.3 et 2.5) : phase 5, premier groupe ; lit l'ouverture (IN^vol, μ̃) et la
phase 2 (IN^vol*, UC, écrits par le bloc 2, sans recalcul) ; écrit l'état
`mu_tilde` (d'abord, voir « Bornes »), ξ, p et l'indice P (P4 : P_t ≡ p_t sous
J = 1, dans la même méthode) ; aucune ligne de flux ; ni les ventes, ni la
demande adressée, ni un plan.

**Bornes** : aucune (`sec:prix-conditions`). p_t > 0 découle de la forme
exponentielle en arithmétique exacte ; ξ n'est pas écrêtée. En double
précision, μ̃ a un domaine de représentabilité, |μ̃| ≤ ln(DBL_MAX)
(`nations.etat.prix.DOMAINES` ; ADR 0016, point 18.1 ; #158), contrôlé à
l'écriture de `mu_tilde`, qui précède le calcul de p : un μ̃_t hors domaine est
refusé par `RefusDuMoteur` nommant « mu_tilde », jamais par le
`DepassementNumerique` anonyme de exp(μ̃_t) (P3) ; dans ce domaine,
UC_t exp(μ̃_t) peut encore valoir 0,0 par sous-dépassement (UC_t = 1e−17,
μ̃_t = −ln(DBL_MAX)), et la division par p du bloc production est alors
refusée par le moteur (`DivisionParZero`, ADR 0016, point 10.1).
"""

from __future__ import annotations

import math

from nations.moteur.contrat_bloc import OUVERTURE, DeclarationDeBloc, Lecture, Siege
from nations.moteur.conversions import par_pas

# --------------------------------------------------------------------------
# Équations P1 à P4 : fonctions pures
# --------------------------------------------------------------------------


def tension_sur_les_stocks(IN_vol: float, IN_vol_etoile: float) -> float:
    """P1 : ξ_t = 1 − IN^vol_t/IN^vol*_t, fraction du stock cible ; IN^vol* lu dans N2, sans
    recalcul."""
    # eq:prix-tension-stocks
    return 1.0 - IN_vol / IN_vol_etoile


def marge(mu_tilde_prec: float, xi: float, lambda_mu_pas: float, mu_bar: float,
          psi_xi: float) -> float:
    """P2 (P54, option (ii)) : μ̃_t = (1 − λ_μ/n_a) μ̃_{t−1} + (λ_μ/n_a)[ln(1 + μ̄) + ψ_ξ ξ_t],
    sans dimension ; `lambda_mu_pas` = λ_μ/n_a."""
    # eq:prix-marge
    return ((1.0 - lambda_mu_pas) * mu_tilde_prec
            + lambda_mu_pas * (math.log(1.0 + mu_bar) + psi_xi * xi))


def prix_du_pas(UC: float, mu_tilde: float) -> float:
    """P3 : ln p_t = ln UC_t + μ̃_t, soit p_t = UC_t exp(μ̃_t), u.m. par u.v. ; p > 0 par la
    forme exponentielle en arithmétique exacte, sans plancher (en double précision, 0,0 par
    sous-dépassement est possible ; voir « Bornes » au docstring du module)."""
    # eq:prix-prix-du-pas
    return UC * math.exp(mu_tilde)


def indice_des_prix(p: float) -> float:
    """P4 : P_t ≡ p_t (J = 1), u.m. par u.v. ; entré au registre par le moteur en phase 9."""
    # eq:prix-indice
    return p


# --------------------------------------------------------------------------
# Bloc
# --------------------------------------------------------------------------


class Prix:
    """Bloc 4 : phase 5, premier groupe ; aucun attribut d'instance."""

    __slots__ = ()
    declaration = DeclarationDeBloc("prix", (
        Siege("5", ("xi", "p", "P"),
              (Lecture(OUVERTURE, "IN_vol"), Lecture(OUVERTURE, "mu_tilde"),
               Lecture("2", "IN_vol_etoile"), Lecture("2", "UC")),
              (), (), ("mu_tilde",)),
    ))

    def phase_5(self, vue) -> None:
        """Tension sur les stocks, marge, prix du pas et indice des prix."""
        table = vue.parametres.prix
        xi = tension_sur_les_stocks(vue.ouverture.IN_vol, vue.lire("IN_vol_etoile"))
        mu_tilde = marge(vue.ouverture.mu_tilde, xi, par_pas(table.lambda_mu), table.mu_bar,
                         table.psi_xi)
        # μ̃_t écrit avant le calcul de p (décision du mainteneur du 27/11/2026, constat m2 ;
        # #158) : un μ̃_t hors de son domaine de représentabilité est refusé avec son nom par
        # `Vue.ecrire_etat` avant que exp(μ̃_t) (P3) ne déborde en `DepassementNumerique`
        # anonyme. Sans effet sur les valeurs : le bloc lit μ̃_{t−1} à l'ouverture, et la
        # valeur écrite n'est lue, sous `mu_tilde_suivant`, que par l'observation (C2).
        vue.ecrire_etat("mu_tilde", mu_tilde)
        p = prix_du_pas(vue.lire("UC"), mu_tilde)
        vue.ecrire_pas("xi", xi)
        vue.ecrire_pas("p", p)
        vue.ecrire_pas("P", indice_des_prix(p))
