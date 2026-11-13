"""Bloc 2, production et stocks (radical `production`).

Contrat : décision M24 (option C, J = 1 ; lectures (a) à (g), (f) révisée par
M25 (b)) ; M26 (UC écrit en phase 2) ; spécification, `sec:production` et
`tab:production-phases` ; fiche `docs/blocs/production.md`, § 9.1 à 9.6 ;
ADR 0012, annotation du 13/11/2026 (noms, lectures, tables, g) ; issue #113.

**Équations.** N1 à N11 de la spécification sont des fonctions pures du
module, appelables directement, qui reçoivent des scalaires (taux déjà
convertis au pas) ; les méthodes de phase lisent la vue, convertissent les
taux par `nations.moteur.conversions` seulement, appellent ces fonctions et
écrivent. Les labels `eq:production-…` (fiche, § 9.1) et leurs balises sont
posés ensemble au passage de `docwriter` (P62) : d'ici là, chaque équation est
repérée par son identifiant N1 à N11.

**Phases** (`tab:production-phases` ; ADR 0012, annotation du 13/11/2026,
points 2.2 et 2.5) :

- phase 2 : N2, N3, N4, N8 (UC) ; lit l'ouverture (v^e, IN^vol, pr), W_t
  (phase 1) et (1 + g)^{1/n_a} (phase 0) ; écrit `IN_vol_etoile`, `y_etoile`,
  `N_etoile`, `UC` ; ne lit aucun autre plan de la phase 2 ;
- phase 4 : N5, N11 ; lit N_t, écrit avant lui par le bloc travail (ordre
  « travail, puis production », ADR 0007), y* (phase 2), l'ouverture (pr,
  K^vol) ; écrit `y`, `y_cap`, `tu` ;
- phase 5 : N6, N7, N8 (ligne 4), N9, N10, N1 ; lit p_t, écrit avant lui par
  le bloc prix, les plans de dépense en u.m. (phase 2), UC (phase 2), y
  (phase 4), (1 + g)^{1/n_a} (phase 0) et l'ouverture (v^e, IN^vol, IN, pr,
  K^vol) ; écrit `v` et les volumes servis `C_vol`, `I_vol`, `G_vol`, propose
  la ligne 4 et écrit les quatre variables d'état (v^e, IN^vol, pr, K^vol).

**Bornes**, toutes déclarées, sans paramètre (`sec:production-conditions`) :
le plancher y* ≥ 0 (N3), la technique y ≤ pr·N (N5) et la disponibilité
v ≤ IN^vol + y (N6) ; aucune autre.

**Exactitude en double précision** (ADR 0012, annotation du 13/11/2026,
points 1.7 et 1.8 ; P72) : le disponible IN^vol + y est calculé une fois, et
v = min(d ; disponible) comme IN^vol_{t+1} = disponible − v portent sur la
même valeur flottante, si bien que IN^vol_{t+1} ≥ 0 exactement ; la ligne 4
s'écrit sous la forme B, ΔIN = cm·IN^vol_{t+1} − IN_t, algébriquement
équivalente à UC·y − cm·v par N7, qui tient IN_{t+1} = IN_t + ΔIN ≥ 0
exactement (monotonie de l'arrondi) et nul à l'épuisement.

**N11.** La capacité normale y^cap = K^vol/(n_a κ) s'écrit K^vol × (1/κ)/n_a :
1/κ, production annuelle normale par unité de capital, est un taux annuel de
flux, converti au pas par la seule conversion linéaire (`par_pas`), comme le
suggère l'annotation du 13/11/2026, point 3.6. Aucune division par n_a hors de
`conversions` ; la liste d'exemptions du test « conversion unique » n'est pas
élargie.
"""

from __future__ import annotations

from nations.moteur.contrat_bloc import OUVERTURE, DeclarationDeBloc, Lecture, Siege
from nations.moteur.conversions import TauxDeFlux, facteur_par_pas, par_pas

# --------------------------------------------------------------------------
# Équations N1 à N11 : fonctions pures
# --------------------------------------------------------------------------


def ventes_anticipees(v_e: float, d: float, facteur_g: float, lambda_v_pas: float) -> float:
    """N1 : v^e_{t+1} = (1 + g)^{1/n_a} [(1 − λ_v/n_a) v^e_t + (λ_v/n_a) d_t], u.v. par pas ;
    `lambda_v_pas` = λ_v/n_a."""
    # eq:production-ventes-anticipees
    return facteur_g * ((1.0 - lambda_v_pas) * v_e + lambda_v_pas * d)


def stock_cible(v_e: float, sigma: float, n_a: int) -> float:
    """N2 : IN^vol*_t = n_a σ v^e_t, u.v. (σ en années de ventes)."""
    # eq:production-stock-cible
    return n_a * sigma * v_e


def production_visee(v_e: float, IN_vol_etoile: float, IN_vol: float, facteur_g: float,
                     lambda_IN_pas: float) -> float:
    """N3 : y*_t = max{0 ; v^e + [(1 + g)^{1/n_a} − 1] IN^vol* + (λ_IN/n_a)(IN^vol* − IN^vol)},
    u.v. par pas ; `lambda_IN_pas` = λ_IN/n_a. Plancher y* ≥ 0 : borne physique déclarée,
    sans paramètre, inactive à l'état stationnaire."""
    # eq:production-visee
    return max(0.0, v_e + (facteur_g - 1.0) * IN_vol_etoile
               + lambda_IN_pas * (IN_vol_etoile - IN_vol))


def demande_de_travail(y_etoile: float, pr: float) -> float:
    """N4 : N*_t = y*_t/pr_t, personnes."""
    # eq:production-demande-travail
    return y_etoile / pr


def production_du_pas(y_etoile: float, pr: float, N: float) -> float:
    """N5 : y_t = min{y*_t ; pr_t N_t}, u.v. par pas. Technique y ≤ pr·N : borne déclarée,
    ses deux termes égaux à l'état stationnaire."""
    # eq:production-realisee
    return min(y_etoile, pr * N)


def capacite(K_vol: float, rendement_normal_pas: float) -> float:
    """N11 : y^cap_t = K^vol_t/(n_a κ), u.v. par pas ; `rendement_normal_pas` = (1/κ)/n_a,
    taux de flux 1/κ converti au pas."""
    # eq:production-capacite
    return K_vol * rendement_normal_pas


def taux_d_utilisation(y: float, y_cap: float) -> float:
    """N11 : tu_t = y_t/y^cap_t, fraction ; sans plafond."""
    return y / y_cap


def disponible(IN_vol: float, y: float) -> float:
    """Disponible du pas, IN^vol_t + y_t (N6, N7), calculé une fois."""
    return IN_vol + y


def demande_adressee(d_H: float, d_F: float, d_G: float) -> float:
    """N6 : d_t = d_H + d_F + d_G, u.v. par pas, servie ou non (lue aussi par N1)."""
    return d_H + d_F + d_G


def ventes(d: float, d_H: float, d_F: float, d_G: float,
           disponible_du_pas: float) -> tuple[float, float, float, float]:
    """N6 : (v, v_H, v_F, v_G) ; v = min{d ; IN^vol + y}, chaque acheteur servi au même taux
    v/d (rationnement proportionnel, sans priorité) ; ventes et volumes servis nuls si d = 0.
    Disponibilité v ≤ IN^vol + y : borne déclarée."""
    # eq:production-ventes
    v = min(d, disponible_du_pas)
    if d == 0.0:
        return v, 0.0, 0.0, 0.0
    return v, v / d * d_H, v / d * d_F, v / d * d_G


def stock_en_volume(disponible_du_pas: float, v: float) -> float:
    """N7 : IN^vol_{t+1} = (IN^vol_t + y_t) − v_t, u.v., sur le disponible calculé une fois."""
    # eq:production-stock-volume
    return disponible_du_pas - v


def cout_unitaire(W: float, pr: float) -> float:
    """N8 : UC_t = W_t/pr_t, u.m. par u.v. (coût salarial, J = 1, sans intrants)."""
    # eq:production-cout-unitaire
    return W / pr


def variation_des_stocks(IN: float, UC: float, y: float, disponible_du_pas: float,
                         IN_vol_suivant: float) -> float:
    """N8, ligne 4, forme B (P72) : cm_t = (IN_t + UC_t y_t)/(IN^vol_t + y_t), puis
    ΔIN_t = cm_t IN^vol_{t+1} − IN_t, u.m. par pas ; ΔIN = 0 si IN^vol_t + y_t = 0."""
    # eq:production-variation-stocks
    if disponible_du_pas == 0.0:
        return 0.0
    cm = (IN + UC * y) / disponible_du_pas
    return cm * IN_vol_suivant - IN


def productivite_suivante(pr: float, facteur_pr: float) -> float:
    """N9 : pr_{t+1} = pr_t (1 + g_pr)^{1/n_a} ; `facteur_pr` = (1 + g_pr)^{1/n_a}."""
    # eq:production-productivite
    return pr * facteur_pr


def capital_en_volume(K_vol: float, delta_pas: float, I_vol: float) -> float:
    """N10 : K^vol_{t+1} = (1 − δ/n_a) K^vol_t + I^vol_t, u.v. ; `delta_pas` = δ/n_a ;
    I^vol_t : volume livré à l'investissement, après rationnement (N6)."""
    # eq:production-capital-volume
    return (1.0 - delta_pas) * K_vol + I_vol


# --------------------------------------------------------------------------
# Bloc
# --------------------------------------------------------------------------


def _ouverture(*champs: str) -> tuple[Lecture, ...]:
    return tuple(Lecture(OUVERTURE, champ) for champ in champs)


class Production:
    """Bloc 2 : phases 2, 4 et 5 ; aucun attribut d'instance."""

    __slots__ = ()
    declaration = DeclarationDeBloc("production", (
        Siege("2", ("IN_vol_etoile", "y_etoile", "N_etoile", "UC"),
              _ouverture("v_e", "IN_vol", "pr") + (Lecture("0", "facteur_g"),
                                                   Lecture("1", "W_suivant")),
              (), (), ()),
        Siege("4", ("y", "y_cap", "tu"),
              _ouverture("pr", "K_vol") + (Lecture("2", "y_etoile"), Lecture("4", "N_suivant")),
              (), (), ()),
        Siege("5", ("v", "C_vol", "I_vol", "G_vol"),
              _ouverture("v_e", "IN_vol", "IN", "pr", "K_vol")
              + (Lecture("0", "facteur_g"), Lecture("2", "C_plan"), Lecture("2", "I_plan"),
                 Lecture("2", "G_plan"), Lecture("2", "UC"), Lecture("4", "y"),
                 Lecture("5", "p")),
              ("4",), (), ("v_e", "IN_vol", "pr", "K_vol")),
    ))

    def phase_2(self, vue) -> None:
        """Plans : stock cible, production visée, demande de travail, coût unitaire."""
        table = vue.parametres.production
        v_e = vue.ouverture.v_e
        pr = vue.ouverture.pr
        IN_vol_etoile = stock_cible(v_e, table.sigma, vue.parametres.cadre.pas_par_an)
        y_etoile = production_visee(v_e, IN_vol_etoile, vue.ouverture.IN_vol,
                                    vue.lire("facteur_g"), par_pas(table.lambda_IN))
        vue.ecrire_pas("IN_vol_etoile", IN_vol_etoile)
        vue.ecrire_pas("y_etoile", y_etoile)
        vue.ecrire_pas("N_etoile", demande_de_travail(y_etoile, pr))
        vue.ecrire_pas("UC", cout_unitaire(vue.lire("W_suivant"), pr))

    def phase_4(self, vue) -> None:
        """Production du pas sur l'emploi effectif, capacité normale, taux d'utilisation."""
        y = production_du_pas(vue.lire("y_etoile"), vue.ouverture.pr, vue.lire("N_suivant"))
        rendement = par_pas(TauxDeFlux(1.0 / vue.parametres.production.kappa))
        y_cap = capacite(vue.ouverture.K_vol, rendement)
        vue.ecrire_pas("y", y)
        vue.ecrire_pas("y_cap", y_cap)
        vue.ecrire_pas("tu", taux_d_utilisation(y, y_cap))

    def phase_5(self, vue) -> None:
        """Ventes et rationnement, stocks en volume et en valeur (ligne 4), productivité,
        capital en volume, ventes anticipées."""
        p = vue.lire("p")
        y = vue.lire("y")
        d_H, d_F, d_G = vue.lire("C_plan") / p, vue.lire("I_plan") / p, vue.lire("G_plan") / p
        d = demande_adressee(d_H, d_F, d_G)
        disponible_du_pas = disponible(vue.ouverture.IN_vol, y)
        v, v_H, v_F, v_G = ventes(d, d_H, d_F, d_G, disponible_du_pas)
        IN_vol_suivant = stock_en_volume(disponible_du_pas, v)
        vue.ecrire_pas("v", v)
        vue.ecrire_pas("C_vol", v_H)
        vue.ecrire_pas("I_vol", v_F)
        vue.ecrire_pas("G_vol", v_G)
        vue.proposer("4", {"Delta_IN": variation_des_stocks(
            vue.ouverture.IN, vue.lire("UC"), y, disponible_du_pas, IN_vol_suivant)})
        table = vue.parametres.production
        vue.ecrire_etat("v_e", ventes_anticipees(vue.ouverture.v_e, d,
                                                 vue.lire("facteur_g"), par_pas(table.lambda_v)))
        vue.ecrire_etat("IN_vol", IN_vol_suivant)
        vue.ecrire_etat("pr", productivite_suivante(vue.ouverture.pr,
                                                    facteur_par_pas(table.g_pr)))
        vue.ecrire_etat("K_vol", capital_en_volume(
            vue.ouverture.K_vol, par_pas(vue.parametres.investissement.delta), v_F))
