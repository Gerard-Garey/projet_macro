"""Bloc 5, ménages (radical `menages`).

Contrat : décision M27 (option C : cible de richesse avec terme de tendance, ménage
représentatif ; inflation lue sur la cible déclarée π*, jamais sur π̄ ni sur le glissement ;
richesse visée sur le revenu de Haig-Simons ; budget plafonné en phase 2 ; B_H ≡ 0 au socle),
M29 (revenu disponible calculé en phase 9, ménages retirés des écrivains de la phase 7) et M30
(cible lue à l'ouverture ; Γ^e, γ^e et π^{∗,pas} calculés par le moteur) ; spécification,
`sec:menages` et `tab:menages-phases` ; fiche `docs/blocs/menages.md`, § 9.1 à 9.6 et § 9.10 ;
ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1), points 1, 2, 4 et 6 (P120, P126,
P127) ; issue #60.

**Équations.** H2 à H7 de la spécification sont des fonctions pures du module, appelables
directement, qui reçoivent des scalaires (λ_H déjà converti au pas) ; les méthodes de phase
lisent la vue, convertissent λ_H par `nations.moteur.conversions` seulement, appellent ces
fonctions et écrivent. H1 (Γ^e, γ^e, π^{∗,pas}) est une grandeur du moteur
(`nations.moteur.ouverture`, P119) : le bloc la lit sous `Gamma_e`, `gamma_e` et
`pi_etoile_pas` (source `"0"`), sans la recalculer. Les labels `eq:menages-…` de H2 à H7
(fiche, § 9.1 ; `tab:menages-equations`) et leurs balises ont été posés ensemble au passage
de `docwriter` (rang 6 de J3-d1, P62) ; l'identifiant H2 à H7 ne sert plus qu'au renvoi à la
fiche.

**Lecture nette** (ADR 0013, annotation du 14/11/2026 (rang 1b de J3-d1), point 4 ; ADR 0012,
A8.2 ; #103) : D_H, moyen de paiement soumis à la lecture nette du contrôle de caisse, est lu
en D̃_H = max(0 ; D_H) par H5 (plafond) et dans la richesse sous la lecture nette,
Ṽ_H = D̃_H + B_H, par H3 et H4 (V_H garde le seul sens de valeur nette du bilan) ;
une poussière d'arrondi sous zéro ne fait donc ni un plan négatif (refusé par `PlanHorsDomaine`)
ni une richesse négative. B_H est lu tel quel (≡ 0 au socle, M27, lecture (c)). Le plan est borné
exactement, C^plan ≤ max(0 ; D_H) ; la ligne 1 exécutée, p·v_H, peut le dépasser d'un ulp
(point 6, P126 : poussière admise sous la lecture nette).

**Phases** (`tab:menages-phases`) :

- phase 2 : lit l'ouverture (D_H, B_H, YD_m1) et les grandeurs du moteur (Γ^e, γ^e,
  π^{∗,pas}) ; H2 à H5 ; écrit les variables du pas `YD_e`, `V_etoile_H`, `C_regle` et
  `C_plan` (vers le bloc production) ; aucun revenu du pas, aucun plan, ni le registre ;
- phase 5, après les blocs prix et production : lit p_t et le volume servi C^vol_t ;
  propose la ligne 1 (H6) ;
- phase 9, groupe des blocs (M29) : lit au grand livre les montants exécutés, dans la
  colonne des ménages, des lignes 5, 6, 7, 10, 11a, 14 et 15, et écrit la variable d'état
  `YD_m1` du pas suivant (H7), sans flux.

Aucune écriture en phases 0, 1, 3, 4, 6 à 8. **Bornes** : une borne à seuil libre, le plafond
de H5 sur les dépôts d'ouverture, sans champ de table (décision du 03/10/2026, lecture (i)) ;
une contrainte de conservation, le plancher de H5 (`sec:menages-conditions`).
"""

from __future__ import annotations

from nations.moteur.contrat_bloc import (
    GRAND_LIVRE,
    OUVERTURE,
    DeclarationDeBloc,
    Lecture,
    Siege,
)
from nations.moteur.conversions import par_pas

# Lignes de la colonne des ménages que somme H7, dans l'ordre de `tab:matrice-flux`.
LIGNES_DU_REVENU = ("5", "6", "7", "10", "11a", "14", "15")

# --------------------------------------------------------------------------
# Équations H2 à H7 : fonctions pures
# --------------------------------------------------------------------------


def revenu_attendu(Gamma_e: float, YD_m1: float) -> float:
    """H2 : YD^e_t = Γ^e_t YD_{t−1}, u.m. par pas ; Γ^e_t lu du moteur (H1), sans recalcul."""
    # eq:menages-revenu-attendu
    return Gamma_e * YD_m1


def richesse_visee(nu_H: float, n_a: int, YD_e: float, pi_etoile_pas: float,
                   V_H_net: float) -> float:
    """H3 : V*_{H,t} = ν_H n_a (YD^e_t − π^{∗,pas}_t Ṽ_{H,t}), u.m. ; ν_H en années, n_a y
    est un changement d'unité (années → pas), non une conversion ; `V_H_net` = Ṽ_{H,t} =
    max(0 ; D_H) + B_H, lecture nette (non la valeur nette V_H du bilan)."""
    # eq:menages-richesse-visee
    return nu_H * n_a * (YD_e - pi_etoile_pas * V_H_net)


def plan_de_la_regle(YD_e: float, gamma_e: float, V_H_net: float, lambda_H_pas: float,
                     V_etoile_H: float) -> float:
    """H4 : C^règle_t = YD^e_t − γ^e_t Ṽ_{H,t} − (λ_H/n_a)(V*_{H,t} − Ṽ_{H,t}), u.m.
    par pas ; `V_H_net` = Ṽ_{H,t}, lecture nette (H3) ; `lambda_H_pas` = λ_H/n_a, converti
    par `par_pas`."""
    # eq:menages-plan-consommation
    return YD_e - gamma_e * V_H_net - lambda_H_pas * (V_etoile_H - V_H_net)


def budget_de_consommation(D_H_net: float, C_regle: float) -> float:
    """H5 : C^plan_t = min{D̃_{H,t} ; max{0 ; C^règle_t}}, u.m. par pas ; `D_H_net` =
    D̃_{H,t} = max(0 ; D_H), lecture nette, d'où C^plan ≥ 0 exactement. Plafond : borne à seuil
    libre sur les dépôts d'ouverture ; plancher : contrainte de conservation, sans paramètre."""
    # eq:menages-budget-consommation
    return min(D_H_net, max(0.0, C_regle))


def consommation(p: float, C_vol: float) -> float:
    """H6 : C_t = p_t v_{H,t}, ligne 1, u.m. par pas ; v_{H,t} = C^vol_t servi par le bloc
    production (N6), p_t écrit par le bloc prix en phase 5."""
    # eq:menages-consommation
    return p * C_vol


def revenu_disponible(montants: tuple[float, ...]) -> float:
    """H7 : YD_t = Σ_ℓ f_{ℓ,H,t}, ℓ ∈ {5, 6, 7, 10, 11a, 14, 15}, u.m. par pas ; `montants` :
    montants exécutés de ces lignes dans la colonne des ménages (signés : la ligne 7 y est
    −T_H), dans l'ordre de `LIGNES_DU_REVENU`, sommés dans cet ordre."""
    # eq:menages-revenu-disponible
    total = 0.0
    for montant in montants:
        total += montant
    return total


# --------------------------------------------------------------------------
# Bloc
# --------------------------------------------------------------------------


class Menages:
    """Bloc 5 : phases 2, 5 et 9 ; aucun attribut d'instance."""

    __slots__ = ()
    declaration = DeclarationDeBloc("menages", (
        Siege("2", ("YD_e", "V_etoile_H", "C_regle", "C_plan"),
              (Lecture(OUVERTURE, "D_H"), Lecture(OUVERTURE, "B_H"),
               Lecture(OUVERTURE, "YD_m1"), Lecture("0", "Gamma_e"), Lecture("0", "gamma_e"),
               Lecture("0", "pi_etoile_pas")),
              (), (), ()),
        Siege("5", (), (Lecture("5", "p"), Lecture("5", "C_vol")), ("1",), (), ()),
        Siege("9", (), tuple(Lecture(GRAND_LIVRE, ligne) for ligne in LIGNES_DU_REVENU),
              (), (), ("YD_m1",)),
    ))

    def phase_2(self, vue) -> None:
        """Revenu attendu, richesse visée, plan de la règle et budget de consommation."""
        table = vue.parametres.menages
        # Lecture nette (point 4) : D̃_H = max(0 ; D_H), dans Ṽ_H (H3, H4) et dans le
        # plafond (H5) ; Ṽ_H n'est pas la valeur nette V_H du bilan.
        D_H_net = max(0.0, vue.ouverture.D_H)
        V_H_net = D_H_net + vue.ouverture.B_H
        YD_e = revenu_attendu(vue.lire("Gamma_e"), vue.ouverture.YD_m1)
        V_etoile_H = richesse_visee(table.nu_H, vue.parametres.cadre.pas_par_an, YD_e,
                                    vue.lire("pi_etoile_pas"), V_H_net)
        C_regle = plan_de_la_regle(YD_e, vue.lire("gamma_e"), V_H_net,
                                   par_pas(table.lambda_H), V_etoile_H)
        vue.ecrire_pas("YD_e", YD_e)
        vue.ecrire_pas("V_etoile_H", V_etoile_H)
        vue.ecrire_pas("C_regle", C_regle)
        vue.ecrire_pas("C_plan", budget_de_consommation(D_H_net, C_regle))

    def phase_5(self, vue) -> None:
        """Consommation exécutée (ligne 1), au prix du pas sur le volume servi."""
        vue.proposer("1", {"C": consommation(vue.lire("p"), vue.lire("C_vol"))})

    def phase_9(self, vue) -> None:
        """Revenu disponible du pas, sur les montants exécutés de la colonne des ménages ; état
        du pas suivant."""
        # Lectures littérales, une par ligne, dans l'ordre de `LIGNES_DU_REVENU` (contrôle
        # statique des lectures : aucun nom de lecture calculé).
        vue.ecrire_etat("YD_m1", revenu_disponible((
            vue.grand_livre.montant_execute("5", "menages"),
            vue.grand_livre.montant_execute("6", "menages"),
            vue.grand_livre.montant_execute("7", "menages"),
            vue.grand_livre.montant_execute("10", "menages"),
            vue.grand_livre.montant_execute("11a", "menages"),
            vue.grand_livre.montant_execute("14", "menages"),
            vue.grand_livre.montant_execute("15", "menages"))))
