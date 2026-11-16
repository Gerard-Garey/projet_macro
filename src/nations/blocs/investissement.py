"""Bloc 6, investissement et financement des entreprises (radical `investissement`).

Contrat : décision M28 (option S-ζ avec la règle de financement F : taux réel du crédit anticipé
lu sur la cible déclarée, taux d'utilisation visé fonction de son niveau, plan d'investissement en
part de la production attendue, part visée ajustée sur l'écart du taux d'utilisation, levier visé
sur le capital comptable, dépôts visés, impôt anticipé, dividende résiduel ; lectures (a) à (g)),
M29 (impôt des entreprises du pas retenu en phase 9), M30 (cible lue à l'ouverture ; Γ^e et
π^{∗,pas} calculés par le moteur) et M31 (lignes 9 et 10 proposées par le bloc banque) ;
spécification, `sec:investissement`, `tab:investissement-equations` et
`tab:investissement-phases` ; fiche `docs/blocs/investissement.md`, § 9.1 à 9.6 et § 9.10 ;
ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1), points 1 à 4 (P127, P128, P80, P120) ;
issue #67.

**Équations.** S1 à S7 et F1 à F4 de la spécification sont des fonctions pures du module,
appelables directement, qui reçoivent des scalaires (taux et vitesses déjà convertis au pas) ;
les méthodes de phase lisent la vue, convertissent par `nations.moteur.conversions` seulement,
appellent ces fonctions et écrivent. Γ^e_t, π^{∗,pas}_t et (1 + g)^{1/n_a} (`facteur_g`) sont des
grandeurs du moteur (phase 0), lues sans recalcul. Les douze labels `eq:investissement-…` (fiche,
§ 9.1 ; `tab:investissement-equations`) et leurs balises ont été posés ensemble au passage de
`docwriter` (rang 6 de J3-d1, P62) ; l'identifiant S1 à S7 ou F1 à F4 ne sert plus qu'au renvoi
à la fiche.

**Lecture nette** (ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1), point 4 ; ADR 0012,
A8.2 ; #103) : D_F, moyen de paiement soumis à la lecture nette du contrôle de caisse, est lu en
max(0 ; D_F) par F3, dans le terme de dépôts et dans les intérêts, comme B4. Localité (#142) :
la phase 6 passe D_F brut, et seule la fonction balisée F3 applique max(0 ; ·). K et L ne sont
pas des moyens de paiement et sont lus tels quels.

**Plans dans leur domaine par la forme** (point 4 ; P120) : I^{vol,plan} ≥ 0 tient par S3
(ti > 0 et y_{t−1} ≥ 0, domaines de l'état ; exponentielle positive), I^plan ≥ 0 par S4
(P_{t−1} > 0, domaine du registre ; 1 + π^{∗,pas} > 0) ; ti_{t+1} > 0 par la forme exponentielle
de S6 ; ces bornes (b) se lisent « pour toute entrée dans le domaine déclaré » (P139 : domaines
de l'état et de la table, 0 ≤ η_r, ζ ≤ 20). En double précision, `math.exp` lève
`OverflowError` au-delà d'un argument d'environ 709 (S2, S3, S6) : le moteur la traduit en
`DepassementNumerique`, refus typé qui nomme le pas, l'étape et le bloc (P139) ; un
sous-dépassement rend 0, dans le domaine du plan, et un ti_{t+1} nul est refusé par le domaine
de l'état. **K ≥ 0** (point 3 ; P80) : la ligne 8 s'écrit c K_t, c = δ/n_a converti par `par_pas`,
sur K d'ouverture, si bien que K_{t+1} = fl(fl(K_t + I_t) − fl(c K_t)) ≥ 0 par monotonie de
l'arrondi (c < 1 par le domaine de δ, I_t ≥ 0 par S4 et N6).

**Phases** (`tab:investissement-phases`) :

- phase 2 : lit l'ouverture (ti, y_{t−1}, ϱ̄_L, i_L, π*_t), le registre (P_{t−1}) et les
  grandeurs du moteur (`facteur_g`, `pi_etoile_pas`) ; S1 à S4 ; écrit `varrho_L`,
  `tu_etoile`, `I_vol_plan` et `I_plan` (vers le bloc production), et recopie ϱ̄_L
  (`varrho_bar_L`, P128) ; ne lit aucun autre plan de la phase ;
- phase 3 : lit son plan de la phase 2, K et L d'ouverture, δ/n_a (grandeur du moteur
  `delta_pas`, #144, point 2) et la part refusée ς_{L,t} (entrée de scénario `varsigma_L`,
  publiée en phase 0, nulle hors scénario) ; F1 ; écrit `Delta_L_d`
  et propose la ligne 18 ;
- phase 5, après les blocs prix et production : lit p_t, le volume servi I^vol_t, tu_t et y_t
  (phase 4), tu*_t (phase 2) ; propose la ligne 3 (S5) ; écrit ti_{t+1} (S6) et y_t, retenue
  comme `y_m1` ;
- phase 6 : lit l'ouverture (K, L, D_F, i_L, i_D, T_{F,t−1}), le registre, les grandeurs du
  moteur (Γ^e, π^{∗,pas}, δ/n_a), les montants exécutés des lignes 18, 5, 1 et 2 dans la colonne des
  entreprises (cellules signées, engagement 6 de #132) et v^e_{t+1}
  (`v_e_suivant`, phase 5) ; S7, F2, F4, F3 ; écrit `D_etoile_F` et `T_e_F`, propose les
  lignes 8 et 14 ; ne lit ni l'impôt ni les intérêts exécutés du pas ;
- phase 9, groupe des blocs (M29) : lit au grand livre le montant exécuté de la ligne 7 dans la
  colonne courante des entreprises et écrit `T_F_m1` du pas suivant, sans flux.

Aucune écriture en phases 0, 1, 4, 7 et 8. **Bornes** (`sec:investissement-conditions`) : aucune
borne à seuil libre ; le plancher de F3 est une contrainte de domaine, sans paramètre.
"""

from __future__ import annotations

import math

from nations.moteur.contrat_bloc import (
    GRAND_LIVRE,
    OUVERTURE,
    REGISTRE,
    DeclarationDeBloc,
    Lecture,
    Siege,
)
from nations.moteur.conversions import TauxDeFlux, par_pas

# --------------------------------------------------------------------------
# Équations S1 à S7 et F1 à F4 : fonctions pures
# --------------------------------------------------------------------------


def taux_reel_du_credit(i_L: float, pi_etoile: float) -> float:
    """S1 : ϱ_{L,t} = (1 + i_{L,t})/(1 + π*_t) − 1, par an, forme exacte de Fisher, employé en
    base annuelle sans conversion ; i_L et π*_t lus à l'ouverture."""
    # eq:investissement-taux-reel-credit
    return (1.0 + i_L) / (1.0 + pi_etoile) - 1.0


def utilisation_visee(tu_bar: float, zeta: float, varrho_L: float,
                      varrho_bar_L: float) -> float:
    """S2 : tu*_t = t̄u exp[ζ(ϱ_{L,t} − ϱ̄_L)], fraction de la capacité normale ; ζ, élasticité de
    niveau, sans conversion ; tu* > 0 par la forme, sans plafond."""
    # eq:investissement-utilisation-visee
    return tu_bar * math.exp(zeta * (varrho_L - varrho_bar_L))


def plan_en_volume(ti: float, facteur_g: float, y_m1: float, eta_r: float, varrho_L: float,
                   varrho_bar_L: float) -> float:
    """S3 : I^{vol,plan}_t = ti_t (1 + g)^{1/n_a} y_{t−1} exp[−η_r(ϱ_{L,t} − ϱ̄_L)], u.v. par pas ;
    `facteur_g` = (1 + g)^{1/n_a}, grandeur du moteur ; ≥ 0 par la forme (ti > 0, y_{t−1} ≥ 0)."""
    # eq:investissement-plan
    return ti * facteur_g * y_m1 * math.exp(-eta_r * (varrho_L - varrho_bar_L))


def plan_nominal(P_m1: float, pi_etoile_pas: float, I_vol_plan: float) -> float:
    """S4 : I^plan_t = P_{t−1}(1 + π^{∗,pas}_t) I^{vol,plan}_t, u.m. par pas ; P_{t−1} lu au
    registre, π^{∗,pas}_t du moteur."""
    # eq:investissement-plan-nominal
    return P_m1 * (1.0 + pi_etoile_pas) * I_vol_plan


def investissement_execute(p: float, I_vol: float) -> float:
    """S5 : I_t = p_{j,t} I^vol_t, ligne 3, u.m. par pas ; I^vol_t = v_{F,j,t}, volume servi par
    le bloc production (N6), p_t écrit par le bloc prix en phase 5."""
    # eq:investissement-depense
    return p * I_vol


def part_visee_suivante(ti: float, lambda_ti_pas: float, tu: float, tu_etoile: float) -> float:
    """S6 : ti_{t+1} = ti_t exp[(λ_ti/n_a)(tu_t − tu*_t)], fraction ; `lambda_ti_pas` = λ_ti/n_a,
    converti par `par_pas` ; > 0 par la forme exponentielle."""
    # eq:investissement-part-visee
    return ti * math.exp(lambda_ti_pas * (tu - tu_etoile))


def amortissement(delta_pas: float, K: float) -> float:
    """S7 : ligne 8 = δ K_t/n_a, u.m. par pas, sur la valeur comptable d'ouverture ;
    `delta_pas` = δ/n_a, converti par `par_pas`, sous la forme c K_t du point 3 (P80)."""
    # eq:investissement-amortissement
    return delta_pas * K


def demande_de_credit(lv_etoile: float, delta_pas: float, K: float, I_plan: float,
                      L: float) -> float:
    """F1 : ΔL^d_t = lv*[(1 − δ/n_a) K_t + I^plan_t] − L_t, u.m. par pas, sur K et L d'ouverture
    et le plan de la phase 2."""
    # eq:investissement-demande-credit
    return lv_etoile * ((1.0 - delta_pas) * K + I_plan) - L


def credit_servi(varsigma_L: float, Delta_L_d: float) -> float:
    """F1 : ligne 18, ΔL_t = (1 − ς_{L,t}) max(ΔL^d_t ; 0) + min(ΔL^d_t ; 0), u.m. par pas ;
    ς_{L,t} part refusée de la hausse demandée (entrée de scénario, nulle hors scénario) ; un
    remboursement est accepté."""
    # eq:investissement-credit-servi
    return (1.0 - varsigma_L) * max(Delta_L_d, 0.0) + min(Delta_L_d, 0.0)


def depots_vises(nu_F: float, n_a: int, P_m1: float, pi_etoile_pas: float,
                 v_e_suivant: float) -> float:
    """F2 : D*_{F,t+1} = ν_F n_a P_{t−1}(1 + π^{∗,pas}_t)^2 v^e_{t+1}, u.m. ; ν_F en années, n_a y
    est un changement d'unité (années → pas), non une conversion ; v^e_{t+1} écrite en phase 5
    par le bloc production."""
    # eq:investissement-depots-vises
    return nu_F * n_a * P_m1 * (1.0 + pi_etoile_pas) ** 2 * v_e_suivant


def impot_anticipe(Gamma_e: float, T_F_m1: float) -> float:
    """F4 : T^e_{F,t} = Γ^e_t T_{F,t−1}, u.m. par pas ; Γ^e_t lu du moteur, sans recalcul."""
    # eq:investissement-impot-anticipe
    return Gamma_e * T_F_m1


def dividendes(D_F: float, Delta_L: float, C: float, G: float, WB: float, interets_L: float,
               i_D_pas: float, T_e_F: float, D_etoile_F: float) -> float:
    """F3 : Div_{F,t} = max{0 ; D̃_{F,t} + ΔL_t + C_t + G_t − WB_t − i_{L,t} L_t/n_a
    + i_{D,t} D̃_{F,t}/n_a − T^e_{F,t} − D*_{F,t+1}}, u.m. par pas, ligne 14, versée en dernier ;
    intérêts recalculés sur les encours et les taux d'ouverture (`interets_L` = i_L L/n_a ;
    `i_D_pas` = i_D/n_a, converti par `par_pas`) ; D_F reçu brut, lu ici en D̃_F = max(0 ; D_F),
    dans le terme de dépôts et dans les intérêts (lecture nette ; #142), comme E5. Le plancher est
    une contrainte de domaine de la ligne 14 (M28 (e)), sans paramètre."""
    # eq:investissement-dividendes
    D_F_net = max(0.0, D_F)
    interets_D_F = i_D_pas * D_F_net
    return max(0.0, D_F_net + Delta_L + C + G - WB - interets_L + interets_D_F - T_e_F
               - D_etoile_F)


def sortie(cellule: float) -> float:
    """Montant d'une sortie lue dans la colonne des entreprises : opposé de la cellule signée
    (débit, −x), écrit 0,0 − cellule comme `impot_retenu` ; exact (l'opposé d'un flottant l'est).
    Lecture, non une équation."""
    return 0.0 - cellule


def impot_retenu(cellule_7_F: float) -> float:
    """T_{F,t} retenu comme T_{F,t−1} du pas suivant (M29) : opposé du montant exécuté de la
    ligne 7 dans la colonne courante des entreprises (−T_F), écrit 0,0 − cellule pour rendre
    0,0 et non −0,0 sous une ligne nulle. Tenue d'état, non une équation (fiche 6, § 9.1)."""
    return 0.0 - cellule_7_F


# --------------------------------------------------------------------------
# Bloc
# --------------------------------------------------------------------------


def _ouverture(*champs: str) -> tuple[Lecture, ...]:
    return tuple(Lecture(OUVERTURE, champ) for champ in champs)


class Investissement:
    """Bloc 6 : phases 2, 3, 5, 6 et 9 ; aucun attribut d'instance."""

    __slots__ = ()
    declaration = DeclarationDeBloc("investissement", (
        Siege("2", ("varrho_L", "tu_etoile", "I_vol_plan", "I_plan"),
              _ouverture("ti", "y_m1", "varrho_bar_L", "i_L", "pi_etoile")
              + (Lecture(REGISTRE, "dernier_prix"), Lecture("0", "facteur_g"),
                 Lecture("0", "pi_etoile_pas")),
              (), (), ("varrho_bar_L",)),
        Siege("3", ("Delta_L_d",),
              _ouverture("K", "L") + (Lecture("0", "delta_pas"), Lecture("0", "varsigma_L"),
                                      Lecture("2", "I_plan")),
              ("18",), (), ()),
        Siege("5", (),
              _ouverture("ti") + (Lecture("5", "p"), Lecture("5", "I_vol"), Lecture("4", "tu"),
                                  Lecture("4", "y"), Lecture("2", "tu_etoile")),
              ("3",), (), ("ti", "y_m1")),
        Siege("6", ("D_etoile_F", "T_e_F"),
              _ouverture("K", "L", "D_F", "i_L", "i_D", "T_F_m1")
              + (Lecture(REGISTRE, "dernier_prix"), Lecture("0", "Gamma_e"),
                 Lecture("0", "pi_etoile_pas"), Lecture("0", "delta_pas"),
                 Lecture(GRAND_LIVRE, "18"),
                 Lecture(GRAND_LIVRE, "5"), Lecture(GRAND_LIVRE, "1"), Lecture(GRAND_LIVRE, "2"),
                 Lecture("5", "v_e_suivant")),
              ("8", "14"), (), ()),
        Siege("9", (), (Lecture(GRAND_LIVRE, "7"),), (), (), ("T_F_m1",)),
    ))

    def phase_2(self, vue) -> None:
        """Taux réel du crédit anticipé, taux d'utilisation visé, plan en volume et en u.m. ;
        recopie de la norme ϱ̄_L."""
        table = vue.parametres.investissement
        varrho_bar_L = vue.ouverture.varrho_bar_L
        varrho_L = taux_reel_du_credit(vue.ouverture.i_L, vue.ouverture.pi_etoile)
        I_vol_plan = plan_en_volume(vue.ouverture.ti, vue.lire("facteur_g"), vue.ouverture.y_m1,
                                    table.eta_r, varrho_L, varrho_bar_L)
        vue.ecrire_pas("varrho_L", varrho_L)
        vue.ecrire_pas("tu_etoile", utilisation_visee(table.tu_bar, table.zeta, varrho_L,
                                                      varrho_bar_L))
        vue.ecrire_pas("I_vol_plan", I_vol_plan)
        vue.ecrire_pas("I_plan", plan_nominal(vue.dernier_prix(), vue.lire("pi_etoile_pas"),
                                              I_vol_plan))
        # ϱ̄_L, constante résolue, tenue avec l'état et jamais recalculée (P128).
        vue.ecrire_etat("varrho_bar_L", varrho_bar_L)

    def phase_3(self, vue) -> None:
        """Demande de crédit et crédit servi (ligne 18)."""
        table = vue.parametres.investissement
        Delta_L_d = demande_de_credit(table.lv_etoile, vue.lire("delta_pas"), vue.ouverture.K,
                                      vue.lire("I_plan"), vue.ouverture.L)
        vue.ecrire_pas("Delta_L_d", Delta_L_d)
        vue.proposer("18", {"Delta_L": credit_servi(vue.lire("varsigma_L"), Delta_L_d)})

    def phase_5(self, vue) -> None:
        """Investissement exécuté (ligne 3), part visée du pas suivant, production retenue."""
        vue.proposer("3", {"I": investissement_execute(vue.lire("p"), vue.lire("I_vol"))})
        vue.ecrire_etat("ti", part_visee_suivante(
            vue.ouverture.ti, par_pas(vue.parametres.investissement.lambda_ti), vue.lire("tu"),
            vue.lire("tu_etoile")))
        vue.ecrire_etat("y_m1", vue.lire("y"))

    def phase_6(self, vue) -> None:
        """Amortissement (ligne 8), dépôts visés, impôt anticipé, puis dividende résiduel
        (ligne 14), en dernier."""
        table = vue.parametres.investissement
        L = vue.ouverture.L
        P_m1 = vue.dernier_prix()
        pi_etoile_pas = vue.lire("pi_etoile_pas")
        D_etoile_F = depots_vises(table.nu_F, vue.parametres.cadre.pas_par_an, P_m1,
                                  pi_etoile_pas, vue.lire("v_e_suivant"))
        T_e_F = impot_anticipe(vue.lire("Gamma_e"), vue.ouverture.T_F_m1)
        # Intérêts recalculés sur les encours et les taux d'ouverture (M31, C41), non lus.
        interets_L = par_pas(TauxDeFlux(vue.ouverture.i_L)) * L
        vue.ecrire_pas("D_etoile_F", D_etoile_F)
        vue.ecrire_pas("T_e_F", T_e_F)
        vue.proposer("8", {"deltaK": amortissement(vue.lire("delta_pas"), vue.ouverture.K)})
        # Engagement 6 de #132 (ADR 0013, annotation du 15/11/2026 (J3-d2), point 7) : chaque
        # montant est lu dans la cellule des entreprises (`montant_execute`, signée : + crédité, −
        # débité), sous-colonne capital pour la ligne 18, courante pour les lignes 1, 2 et 5 ;
        # la sortie WB en est l'opposé (`sortie`). Lecture nette (point 4 ; localité, #142) :
        # D_F passé brut à F3, qui le lit en max(0 ; ·) dans le terme de dépôts et les intérêts.
        vue.proposer("14", {"Div_F": dividendes(
            vue.ouverture.D_F, vue.grand_livre.montant_execute("18", "entreprises_capital"),
            vue.grand_livre.montant_execute("1", "entreprises_courant"),
            vue.grand_livre.montant_execute("2", "entreprises_courant"),
            sortie(vue.grand_livre.montant_execute("5", "entreprises_courant")), interets_L,
            par_pas(TauxDeFlux(vue.ouverture.i_D)), T_e_F, D_etoile_F)})

    def phase_9(self, vue) -> None:
        """Impôt des entreprises exécuté du pas, retenu pour le pas suivant (M29)."""
        vue.ecrire_etat("T_F_m1", impot_retenu(
            vue.grand_livre.montant_execute("7", "entreprises_courant")))
