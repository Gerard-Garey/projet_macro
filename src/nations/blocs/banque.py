"""Bloc 7, banque commerciale (radical `banque`).

Contrat : décision M31 (option C : écarts additifs au taux directeur, transmission
complète en un tour, fonds propres ancrés par un dividende résiduel, refinancement
sur la position nette de réserves, crédit à la demande ; lectures (a) à (h)) et
M33 (la banque ne siège pas en phase 7 ; ADR 0011) ; spécification, `sec:banque`,
`tab:banque-equations` et `tab:banque-phases` ; fiche `docs/blocs/banque.md`,
§ 9.1 à 9.6 ; ADR 0013, annotation du 14/11/2026, points 3 à 6 et 9 (P93, P96) ;
issue #90 et ses amendements (critères du 07/10/2026, critère 4 : contrat de
poussière, part du bloc 7 de #103).

**Équations.** B1 à B7 de la spécification sont des fonctions pures du module,
appelables directement, qui reçoivent des scalaires (taux d'intérêt déjà
convertis au pas, sauf B1 et B2, qui écrivent des taux annuels) ; les méthodes
de phase lisent la vue, convertissent les taux par `nations.moteur.conversions`
seulement, appellent ces fonctions et écrivent. Chaque équation porte sa balise
`eq:banque-…` (fiche, § 9.1 ; `tab:banque-equations`) et garde son identifiant
B1 à B7.

**Formes exécutées** (ADR 0013, annotation du 14/11/2026, points 5 et 9) :

- B7 en **forme −min**, ΔL^CB_t = −min(Res^{8b}_t ; L^CB_t), algébriquement
  égale à max(L^CB_t − Res^{8b}_t ; 0) − L^CB_t telle qu'écrite (A8.1) : la
  ligne 20 du noyau ajoute ce flottant même à la position lue, d'où
  Res_{t+1} ≥ 0, L^CB_{t+1} ≥ 0 et Res_{t+1} L^CB_{t+1} = 0 exactement ;
- B3 à B5 sur les **taux du tour au pas** : i_L et i_D d'ouverture, i_CB du tour
  (phase 1), convertis par `par_pas` ; i_B ≡ i_res ≡ i_CB sont des identités de
  notation (ADR 0011, P6 ; aucune variable `i_res` ni `i_B`) ;
- **contrat de poussière** (critère 4 du 07/10/2026 ; ADR 0012, A8) : D_H et D_F,
  moyens de paiement soumis à la lecture nette du contrôle de caisse, sont lus en
  max(0 ; ·) dans B4 et B5 ; les réserves en sont exclues (découvert intra-pas
  légitime), comme L, B_Bk et L^CB, qui ne sont pas des moyens de paiement ;
- **E^Bk_t** (B6) est calculé par le bloc depuis les six positions d'ouverture,
  L + B_Bk + Res − D_H − D_F − L^CB, sans lecture de valeur nette (H5.3 fermé) ;
  il porte les positions telles quelles (identité de bilan, non lecture d'un
  moyen de paiement) ; un test le compare à `valeur_nette_stock`.

**Phases** (`tab:banque-phases` ; annotation du 14/11/2026, point 5) :

- phase 6, avec les blocs 6 et 9 (aucune lecture mutuelle) : lit l'ouverture (L,
  B_Bk, Res, L^CB, D_H, D_F, i_L, i_D), `i_CB` (phase 1) et le montant exécuté
  de la ligne 18 (phase 3) ; B3, B4, B5, B6 ; écrit la variable du pas `Pi_Bk`
  et propose les lignes 9, 10 et 15 ;
- phase 8 (c) : lit la position de réserves `Res` au grand livre (après 8 (b),
  A3.3), L^CB d'ouverture et `i_CB` (phase 1) ; propose la ligne 21 (B7), puis
  écrit les états `i_L` et `i_D` du pas suivant (B1, B2).

Aucune écriture en phases 0 à 5, 7 et 9 ; aucune ligne 18 ni 19a (proposées par
les blocs 6 et 9). **Bornes** : aucune borne à seuil libre
(`sec:banque-conditions`) : ni plancher du taux des dépôts, ni plafond de crédit ;
le plancher du dividende est une contrainte de domaine, sans paramètre.
"""

from __future__ import annotations

from nations.moteur.contrat_bloc import GRAND_LIVRE, OUVERTURE, DeclarationDeBloc, Lecture, Siege
from nations.moteur.conversions import TauxDeFlux, par_pas

# --------------------------------------------------------------------------
# Équations B1 à B7 : fonctions pures
# --------------------------------------------------------------------------


def taux_des_credits_suivant(i_CB: float, varpi_L: float) -> float:
    """B1 : i_{L,t+1} = i_CB,t + ϖ_L, par an, taux de flux (écart additif, transmission en un
    tour) ; i_CB,t écrit en phase 1."""
    # eq:banque-taux-credit
    return i_CB + varpi_L


def taux_des_depots_suivant(i_CB: float, varpi_D: float) -> float:
    """B2 : i_{D,t+1} = i_CB,t − ϖ_D, par an, taux de flux, sans plancher (lecture (d))."""
    # eq:banque-taux-depots
    return i_CB - varpi_D


def interets_sur_credits(i_L_pas: float, L: float) -> float:
    """B3 : ligne 9 = i_{L,t} L_t/n_a, u.m. par pas, sur le taux et l'encours d'ouverture ;
    `i_L_pas` converti au pas."""
    # eq:banque-interets-credits
    return i_L_pas * L


def interets_sur_depots(i_D_pas: float, D_H: float, D_F: float) -> tuple[float, float]:
    """B4 : ligne 10 = i_{D,t} D_{H,t}/n_a + i_{D,t} D_{F,t}/n_a, u.m. par pas, ses deux termes
    (ménages, entreprises) ; `i_D_pas` converti au pas, D_H et D_F reçus en max(0 ; ·)."""
    # eq:banque-interets-depots
    return i_D_pas * D_H, i_D_pas * D_F


def resultat(i_L_pas: float, L: float, i_B_pas: float, B_Bk: float, i_res_pas: float,
             Res: float, i_D_pas: float, D_H: float, D_F: float, i_CB_pas: float,
             L_CB: float) -> float:
    """B5 : Π^Bk_t = [i_L L + i_B B_Bk + i_res Res − i_D (D_H + D_F) − i_CB L^CB]/n_a, u.m. par
    pas, sur les encours d'ouverture ; taux reçus convertis au pas (i_B ≡ i_res ≡ i_CB), D_H et
    D_F reçus en max(0 ; ·)."""
    # eq:banque-resultat
    return i_L_pas * L + i_B_pas * B_Bk + i_res_pas * Res - i_D_pas * (D_H + D_F) \
        - i_CB_pas * L_CB


def dividendes(E_Bk: float, Pi_Bk: float, vartheta: float, L: float, Delta_L: float) -> float:
    """B6 : Div_{Bk,t} = max{0 ; E^Bk_t + Π^Bk_t − ϑ L_{t+1}}, L_{t+1} = L_t + ΔL_t, u.m. par
    pas ; ΔL_t est la ligne 18 exécutée en phase 3. Le plancher est une contrainte de domaine."""
    # eq:banque-dividendes
    return max(0.0, E_Bk + Pi_Bk - vartheta * (L + Delta_L))


def refinancement(Res_8b: float, L_CB: float) -> float:
    """B7, forme −min exécutée : ligne 21 = ΔL^CB_t = −min(Res^{8b}_t ; L^CB_t), u.m. par pas,
    égale à max(L^CB_t − Res^{8b}_t ; 0) − L^CB_t ; Res^{8b}_t lue au grand livre après 8 (b)."""
    # eq:banque-refinancement
    return -min(Res_8b, L_CB)


def fonds_propres(L: float, B_Bk: float, Res: float, D_H: float, D_F: float,
                  L_CB: float) -> float:
    """E^Bk_t = L + B_Bk + Res − D_H − D_F − L^CB, u.m., sur les six positions d'ouverture du
    bilan de la banque (`sec:cadre-bilans`), dans l'ordre de `catalogue.POSTES_DU_BILAN` ;
    définition du cadre, non une équation du bloc (aucune balise)."""
    return -D_H - D_F + L + B_Bk + Res - L_CB


# --------------------------------------------------------------------------
# Bloc
# --------------------------------------------------------------------------


def _ouverture(*champs: str) -> tuple[Lecture, ...]:
    return tuple(Lecture(OUVERTURE, champ) for champ in champs)


class Banque:
    """Bloc 7 : phases 6 et 8 (c) ; aucun attribut d'instance."""

    __slots__ = ()
    declaration = DeclarationDeBloc("banque", (
        Siege("6", ("Pi_Bk",),
              _ouverture("L", "B_Bk", "Res", "L_CB", "D_H", "D_F", "i_L", "i_D")
              + (Lecture("1", "i_CB"), Lecture(GRAND_LIVRE, "18")),
              ("9", "10", "15"), (), ()),
        Siege("8c", (), (Lecture(GRAND_LIVRE, "Res"),) + _ouverture("L_CB")
              + (Lecture("1", "i_CB"),), ("21",), (), ("i_L", "i_D")),
    ))

    def phase_6(self, vue) -> None:
        """Intérêts sur crédits (ligne 9) et sur dépôts (ligne 10), résultat et dividende
        (ligne 15)."""
        L = vue.ouverture.L
        B_Bk = vue.ouverture.B_Bk
        Res = vue.ouverture.Res
        L_CB = vue.ouverture.L_CB
        # Contrat de poussière : D_H et D_F, soumis à la lecture nette, lus en max(0 ; ·).
        D_H = max(0.0, vue.ouverture.D_H)
        D_F = max(0.0, vue.ouverture.D_F)
        i_L_pas = par_pas(TauxDeFlux(vue.ouverture.i_L))
        i_D_pas = par_pas(TauxDeFlux(vue.ouverture.i_D))
        # i_B ≡ i_res ≡ i_CB : un seul taux du tour, converti au pas.
        i_pas = par_pas(TauxDeFlux(vue.lire("i_CB")))
        iD_DH, iD_DF = interets_sur_depots(i_D_pas, D_H, D_F)
        Pi_Bk = resultat(i_L_pas, L, i_pas, B_Bk, i_pas, Res, i_D_pas, D_H, D_F, i_pas, L_CB)
        # E^Bk_t sur les six positions d'ouverture telles quelles (identité de bilan).
        E_Bk = fonds_propres(L, B_Bk, Res, vue.ouverture.D_H, vue.ouverture.D_F, L_CB)
        vue.ecrire_pas("Pi_Bk", Pi_Bk)
        vue.proposer("9", {"iL_L": interets_sur_credits(i_L_pas, L)})
        vue.proposer("10", {"iD_DH": iD_DH, "iD_DF": iD_DF})
        vue.proposer("15", {"Div_Bk": dividendes(
            E_Bk, Pi_Bk, vue.parametres.banque.vartheta, L,
            vue.grand_livre.montant_execute_ligne("18"))})

    def phase_8c(self, vue) -> None:
        """Refinancement (ligne 21), puis taux des crédits et des dépôts du pas suivant."""
        table = vue.parametres.banque
        vue.proposer("21", {"Delta_LCB": refinancement(vue.grand_livre.position("Res"),
                                                       vue.ouverture.L_CB)})
        i_CB = vue.lire("i_CB")
        vue.ecrire_etat("i_L", taux_des_credits_suivant(i_CB, table.varpi_L.valeur))
        vue.ecrire_etat("i_D", taux_des_depots_suivant(i_CB, table.varpi_D.valeur))
