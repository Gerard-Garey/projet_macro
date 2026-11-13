"""Bloc 3, travail et salaires (radical `travail`).

Contrat : décision M25 (option C, λ_N = 3,5, salaire SN, lectures (a) à (f),
(w1), lecture (G) des taux annuels) ; spécification, `sec:travail` et
`tab:travail-phases` ; fiche `docs/blocs/travail.md`, § 9.1 à 9.6 ; ADR 0012,
annotation du 13/11/2026 (noms, lectures, tables ; point 1.4 pour μ̃) ;
décision P54 (μ̃ variable d'état du bloc 4, visa de `macro` sous conditions) ;
issue #50.

**Équations.** T1 à T6 de la spécification sont des fonctions pures du
module, appelables directement, qui reçoivent des scalaires (taux déjà
convertis au pas) ; les méthodes de phase lisent la vue, convertissent les
taux par `nations.moteur.conversions` seulement, appellent ces fonctions et
écrivent. Les labels `eq:travail-…` (fiche, § 9.1) et leurs balises sont
posés ensemble au passage de `docwriter` (P62) : d'ici là, chaque équation est
repérée par son identifiant T1 à T6.

**T2 sous P54, option (ii)** : ω_{t−1} = exp(−μ̃_{t−1}), μ̃_{t−1} étant la marge
en logarithme d'ouverture, variable d'état du bloc 4. Sous J = 1 sans intrants,
UC_{t−1}/p_{t−1} = W_{t−1}/(p_{t−1} pr_{t−1}) = exp(−μ̃_{t−1}) : c'est T2, sans
recalculer pr_{t−1} (N9 n'est pas inversée) ni lire p_{t−1} au registre.

**T3 sous forme exponentiée** : W_t = W_{t−1} · exp(Δ), Δ étant le membre de
droite de T3 moins ln W_{t−1} ; c'est T3 exactement (aucune approximation), et
W_t > 0 découle de la forme, sans borne. Les deux taux de croissance (g_pr et
π^e) passent par la seule conversion géométrique, ln[(1 + x)^{1/n_a}] =
(1/n_a) ln(1 + x) ; λ_w par la conversion linéaire.

**π^e** : lue à l'ouverture (π^e_t, variable d'état du bloc 8, formée au pas
précédent ; lecture (a) de M25) ; jamais π* ni Γ^e à sa place (avis de
`monnaie`, synthèse du rang 1a, § 9). Son unité dans le schéma est « par an,
taux de croissance » : elle est convertie comme telle.

**Phases** (`tab:travail-phases` ; ADR 0012, annotation du 13/11/2026,
points 2.2 et 2.5) :

- phase 1 : T2, T3 ; lit l'ouverture (W, U, μ̃, π^e) ; écrit l'état `W` (W_t,
  lu sous `W_suivant`) ;
- phase 4, avant le bloc 2 : T4, T5, T6, T1 ; lit N*_t (phase 2), W_t
  (phase 1) et l'ouverture (N, N^pa) ; écrit les états `N`, `U`, `N_pa` et
  propose la ligne 5.

**Borne**, déclarée, sans paramètre (`sec:travail-conditions`) : la contrainte
de conservation N ≤ N^pa (T4) ; aucune autre. Avec elle, T5 tient
0 ≤ U ≤ 1 exactement en double précision (N/N^pa ≤ 1 par monotonie de
l'arrondi, U = 0 exactement si N = N^pa), domaine du schéma v2 vérifié à chaque
clôture (annotation du 13/11/2026, point 1.7).
"""

from __future__ import annotations

import math

from nations.moteur.contrat_bloc import OUVERTURE, DeclarationDeBloc, Lecture, Siege
from nations.moteur.conversions import TauxDeCroissance, facteur_par_pas, par_pas

# --------------------------------------------------------------------------
# Équations T1 à T6 : fonctions pures
# --------------------------------------------------------------------------


def population_active_suivante(N_pa: float, facteur_N: float) -> float:
    """T1 : N^pa_{t+1} = N^pa_t (1 + g_N)^{1/n_a}, personnes ; `facteur_N` = (1 + g_N)^{1/n_a}."""
    # eq:travail-population-active
    return N_pa * facteur_N


def salaire_relatif(mu_tilde_prec: float) -> float:
    """T2 : ω_{t−1} = W_{t−1}/(P_{t−1} pr_{t−1}) = exp(−μ̃_{t−1}), sans dimension (J = 1, sans
    intrants ; P54, option (ii))."""
    # eq:travail-salaire-relatif
    return math.exp(-mu_tilde_prec)


def norme_de_part_salariale(mu_bar: float) -> float:
    """ω* = 1/(1 + μ̄), sans dimension (lecture (w1) de M25)."""
    return 1.0 / (1.0 + mu_bar)


def salaire(W_prec: float, facteur_pr: float, facteur_pi_e: float, lambda_w_pas: float,
            omega_etoile: float, omega_prec: float, beta: float, U_prec: float,
            U_eq: float) -> float:
    """T3 : ln W_t = ln W_{t−1} + (1/n_a)[ln(1 + g_pr) + ln(1 + π^e_t)]
    + (λ_w/n_a)[ln(ω*/ω_{t−1}) − β(U_{t−1} − U^eq)], u.m. par personne et par pas ;
    `facteur_pr` = (1 + g_pr)^{1/n_a}, `facteur_pi_e` = (1 + π^e_t)^{1/n_a},
    `lambda_w_pas` = λ_w/n_a. Forme exponentiée : W_t = W_{t−1} exp(Δ)."""
    # eq:travail-salaire
    delta = (math.log(facteur_pr) + math.log(facteur_pi_e)
             + lambda_w_pas * (math.log(omega_etoile / omega_prec) - beta * (U_prec - U_eq)))
    return W_prec * math.exp(delta)


def emploi(N_etoile: float, N_prec: float, N_pa: float, facteur_N: float,
           lambda_N_pas: float) -> float:
    """T4 : N_t = min{N^pa_t ; max{N*_t ; (1 + g_N)^{1/n_a}(1 − λ_N/n_a) N_{t−1}
    + (λ_N/n_a) N*_t}}, personnes ; `lambda_N_pas` = λ_N/n_a. N ≤ N^pa : contrainte de
    conservation, déclarée, sans paramètre, inactive à l'état stationnaire."""
    # eq:travail-emploi
    retenu = facteur_N * (1.0 - lambda_N_pas) * N_prec + lambda_N_pas * N_etoile
    return min(N_pa, max(N_etoile, retenu))


def chomage(N: float, N_pa: float) -> float:
    """T5 : U_t = 1 − N_t/N^pa_t, fraction de la population active."""
    # eq:travail-chomage
    return 1.0 - N / N_pa


def masse_salariale(W: float, N: float) -> float:
    """T6 : WB_t = W_t N_t, u.m. par pas (ligne 5)."""
    # eq:travail-masse-salariale
    return W * N


# --------------------------------------------------------------------------
# Bloc
# --------------------------------------------------------------------------


def _ouverture(*champs: str) -> tuple[Lecture, ...]:
    return tuple(Lecture(OUVERTURE, champ) for champ in champs)


class Travail:
    """Bloc 3 : phases 1 et 4 ; aucun attribut d'instance."""

    __slots__ = ()
    declaration = DeclarationDeBloc("travail", (
        Siege("1", (), _ouverture("W", "U", "mu_tilde", "pi_e"), (), (), ("W",)),
        Siege("4", (),
              _ouverture("N", "N_pa") + (Lecture("1", "W_suivant"), Lecture("2", "N_etoile")),
              ("5",), (), ("U", "N", "N_pa")),
    ))

    def phase_1(self, vue) -> None:
        """Salaire relatif d'ouverture et salaire nominal du pas."""
        table = vue.parametres.travail
        W = salaire(vue.ouverture.W, facteur_par_pas(vue.parametres.production.g_pr),
                    facteur_par_pas(TauxDeCroissance(vue.ouverture.pi_e)),
                    par_pas(table.lambda_w), norme_de_part_salariale(vue.parametres.prix.mu_bar),
                    salaire_relatif(vue.ouverture.mu_tilde), table.beta, vue.ouverture.U,
                    table.U_eq)
        vue.ecrire_etat("W", W)

    def phase_4(self, vue) -> None:
        """Emploi effectif, chômage, masse salariale (ligne 5), population active suivante."""
        table = vue.parametres.travail
        facteur_N = facteur_par_pas(table.g_N)
        N_pa = vue.ouverture.N_pa
        N = emploi(vue.lire("N_etoile"), vue.ouverture.N, N_pa, facteur_N,
                   par_pas(table.lambda_N))
        vue.ecrire_etat("N", N)
        vue.ecrire_etat("U", chomage(N, N_pa))
        vue.proposer("5", {"WB": masse_salariale(vue.lire("W_suivant"), N)})
        vue.ecrire_etat("N_pa", population_active_suivante(N_pa, facteur_N))
