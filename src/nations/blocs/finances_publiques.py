"""Bloc 9, État et dette (radical `finances_publiques`).

Contrat : décision M33 (option C-HS : dépense indexée sur la production potentielle et plafonnée
par l'encaisse d'ouverture ; impôt des ménages sur leur revenu de Haig-Simons retardé, net de la
couverture des intérêts ; couverture réelle des intérêts, levier à deux valeurs ; transferts et
impôt des entreprises en leviers, nuls au socle ; i_B ≡ i_CB ; émission après les règlements vers
une encaisse visée ν_G PB_t ; lignes 19a proposées par ce bloc, lecture A8 ; parts non payées
enregistrées), ADR 0011 (phase 7, points P1 à P4) et M29 ; spécification,
`sec:finances_publiques`, `tab:finances_publiques-equations` et `tab:finances_publiques-phases`,
qui fait foi (E12 en phase 7, E13 à deux parts ; la fiche 9, § 9.1, 9.4 et 9.6, est en retard) ;
fiche `docs/blocs/finances_publiques.md` ; ADR 0013, annotation du 15/11/2026 (rang 1b de J3-d2),
points 1 à 5 ; issue #132 et ses six engagements.

**Équations.** E1 à E13 de la spécification sont des fonctions pures du module, appelables
directement, qui reçoivent des scalaires (taux déjà convertis au pas) ; les méthodes de phase
lisent la vue, convertissent par `nations.moteur.conversions` seulement, appellent ces fonctions
et écrivent. Γ^e_t et π^{∗,pas}_t sont des grandeurs du moteur (phase 0), lues sans recalcul.
Chaque équation porte la balise de son label (`tab:finances_publiques-equations`), posé dans la
spécification avec son encadré « Lecture » depuis `a059d10` (P62) ; E13 garde un label malgré ses
deux parts. i_B ≡ i_CB est une identité de notation (`sec:finances_publiques-taux`), sans balise
ni variable.

**Lecture nette** (ADR 0012, A8.2 ; ADR 0013, annotation du 15/11/2026, point 4 ; engagements 2
à 4) : M^G, D_H et D_F, moyens de paiement soumis à la lecture nette du contrôle de caisse, sont
lus en max(0 ; ·) **dans les fonctions balisées** (localité ; aucun max(0 ; ·) dans les méthodes
de phase) : E1 lit max(0 ; M^G) ; E5 lit D̃_F = max(0 ; D_F) ; E12 lit D̃_H = max(0 ; D_H) ; E13
lit max(0 ; M^{G,8a}). **Lectures brutes**, liste fermée, chacune déclarée à son site de lecture :
E6 (M^G dans le plafond des transferts, sous le max(0 ; ·) extérieur), E9 (M^G, la poussière est
absorbée à l'émission du pas) et l'assiette de E4 (B − M^G − E^CB, où M^G s'annule
algébriquement). Toute autre lecture brute de D_H, D_F ou M^G est un défaut (test
`tests/unitaires/test_finances_publiques.py`).

**Un seul calcul du besoin d'émission par pas** (point 5) : la méthode de la phase 7 calcule E8
et E9 une fois et propose les trois lignes 19a sur le même Em_t, sans attribut d'instance ni
variable d'état.

**Un seul calcul des intérêts sur titres par pas** (ADR 0013, annotation du 16/11/2026, point 4 ;
#150, point 1) : la méthode de la phase 2 calcule E7 une fois et écrit ses trois termes en
variables du pas, sous les noms des termes des lignes 11a à 11c (`iB_BH`, `iB_BBk`, `iB_BCB`),
contrôlés en finitude seulement (i_CB peut être négatif) ; le plafond de E6 en forme la somme, et
la phase 6 les lit et les propose, sans relire i_CB ni les encours de titres : le plafond de E6 et
les lignes 11a à 11c reposent sur les mêmes valeurs.

**Phases** (`tab:finances_publiques-phases`) :

- phase 2 : lit l'ouverture (M^G, pr, N^pa, Y^HS_{t−1}, π*_t, B_H, B_Bk, B_CB, L^CB, Res), le
  registre (P_{t−1}), les grandeurs du moteur (Γ^e, π^{∗,pas}), i_CB (phase 1) et les paramètres
  (table du bloc 9, U^eq du travail, r̄ de la banque centrale) ; E1, E4, E3, E7, E6 ; écrit
  `G_vise`, `G_plan` (vers le bloc production ; `DOMAINES_DU_PAS`), `T_cou`, `T_H`, `Tr_lev`,
  `Tr` et les trois termes de E7, `iB_BH`, `iB_BBk` et `iB_BCB` ;
- phase 5, après les blocs prix et production : lit p_t et le volume servi G^vol_t ; propose la
  ligne 2 (E2) ;
- phase 6 : lit ses calculs de la phase 2 (T_H, Tr^lev, Tr et les trois termes de E7),
  l'ouverture (K, L, D_F, i_L, i_D), les montants exécutés des lignes 1 à 5 et δ ; E5, E13
  (première part) ; écrit `T_F` et `Tr_non_verses`, propose les lignes 6, 7 (T_H + T_F) et 11a à
  11c (termes de E7 de la phase 2) ; ne lit rien de ce qu'un autre bloc écrit dans la phase ;
- phase 7, seul écrivain : lit les montants exécutés des lignes 2, 6, 7, 11a à 11c, puis 5, 10,
  14 et 15 (colonne des ménages), M^G et D_H d'ouverture, ς_{B,t} (phase 0), π^{∗,pas}, θ_CB et
  Π^CB (phase 1), T^cou (phase 2) et ν_G ; E8 à E11, puis E12 ; écrit `M_G_etoile` et `Em`,
  propose les lignes 19a-BC, 19a-ménages et 19a-banque, écrit l'état `Y_HS_m1` ;
- phase 8 (b), sans ordre avec le bloc 8 : lit Π^CB (phase 1) et M^{G,8a} au grand livre ; E13
  (seconde part) ; déclare le montant couvert de la ligne 16 si Π^CB < 0 ; écrit
  `perte_non_couverte`.

Aucune écriture en phases 0, 1, 3, 4 et 9. **Bornes** (`sec:finances_publiques-conditions`) : une
borne à seuil libre dont le seuil est une base, le plafond de E1 ; contraintes sans paramètre :
le plafond de E6 et le max(0 ; ·) de E13, de conservation ; le max(0 ; ·) de M^G dans E1, borne
de domaine du contrat de poussière.
"""

from __future__ import annotations

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
# Définitions sans balise propre (renvois)
# --------------------------------------------------------------------------


def production_potentielle(pr: float, U_eq: float, N_pa: float) -> float:
    """y^pot_t = pr_t (1 − U^eq) N^pa_t, u.v. par pas ; définition de E1, reprise par E6 (renvoi
    `eq:finances_publiques-plan-depense`, non une balise)."""
    return pr * (1.0 - U_eq) * N_pa


def taux_de_reference(r_bar: float, pi_cible: float) -> float:
    """i^ref_t = (1 + r̄)(1 + π*_t) − 1, par an, taux de flux ; définition de E4 (renvoi
    `eq:finances_publiques-couverture-interets`, non une balise) ; r̄, taux réel de Fisher sur la
    cible, n'est jamais converti par pas."""
    return (1.0 + r_bar) * (1.0 + pi_cible) - 1.0


# --------------------------------------------------------------------------
# Équations E1 à E13 : fonctions pures
# --------------------------------------------------------------------------


def plan_de_depense(M_G: float, G_vise: float) -> float:
    """E1 : G^plan_t = min{max{0 ; M^G_t} ; P_{t−1}(1 + π^{∗,pas}_t) θ_G y^pot_t}, u.m. par pas ;
    `G_vise` = P_{t−1}(1 + π^{∗,pas}_t) θ_G y^pot_t (plan non plafonné, `depense_visee`) ; M^G
    reçu brut, lu en max(0 ; ·) ici (lecture nette, engagement 2) : G^plan ≥ 0 exactement, +0 sous
    une poussière. Plafond : borne à seuil libre dont le seuil est une base."""
    # eq:finances_publiques-plan-depense
    return min(max(0.0, M_G), G_vise)


def depense_visee(P_m1: float, pi_etoile_pas: float, theta_G: float, y_pot: float) -> float:
    """Plan non plafonné de E1, P_{t−1}(1 + π^{∗,pas}_t) θ_G y^pot_t, u.m. par pas (« demandé »
    du critère 11, P158) ; membre de E1 (renvoi `eq:finances_publiques-plan-depense`)."""
    return P_m1 * (1.0 + pi_etoile_pas) * theta_G * y_pot


def depense(p: float, G_vol: float) -> float:
    """E2 : G_t = p_t v_{G,t}, ligne 2, u.m. par pas ; v_G servi par le bloc production (N6), p_t
    écrit par le bloc prix en phase 5."""
    # eq:finances_publiques-depense
    return p * G_vol


def impot_des_menages(tau_H: float, Gamma_e: float, Y_HS_m1: float, T_cou: float) -> float:
    """E3 : T_{H,t} = τ_H Γ^e_t Y^HS_{t−1} + T^cou_t, u.m. par pas, part des ménages de la
    ligne 7 ; Γ^e_t lu du moteur, sans recalcul."""
    # eq:finances_publiques-impot-menages
    return tau_H * Gamma_e * Y_HS_m1 + T_cou


def couverture_des_interets(phi: float, ecart_pas: float, B_H: float, B_Bk: float, B_CB: float,
                            L_CB: float, Res: float, M_G: float) -> float:
    """E4 : T^cou_t = φ (i_CB,t − i^ref_t)(B_t − M^G_t − E^CB_t)/n_a, u.m. par pas, de signe
    quelconque ; `ecart_pas` = (i_CB − i^ref)/n_a, converti par `par_pas`. Assiette sur les
    positions d'ouverture, E^CB = B_CB + L^CB − Res − M^G sur les quatre positions de la banque
    centrale, sans lecture de valeur nette (précédent d'E^Bk, P107). **Lecture brute de M^G**
    (exception d'identité, ADR 0013, annotation du 15/11/2026, point 4) : M^G s'annule
    algébriquement, et la lecture brute garde l'identité avec le canal rentier (ligne 15)."""
    # eq:finances_publiques-couverture-interets
    fonds_propres_cb = B_CB + L_CB - Res - M_G
    assiette = B_H + B_Bk + B_CB - M_G - fonds_propres_cb
    return phi * ecart_pas * assiette


def impot_des_entreprises(tau_F: float, C: float, G: float, I: float, Delta_IN: float, WB: float,
                          amortissement: float, interets_L: float, i_D_pas: float,
                          D_F: float) -> float:
    """E5 : T_{F,t} = τ_F Π^av_{F,t}, Π^av = C + G + I + ΔIN − WB − δK/n_a − i_L L/n_a
    + i_D D̃_F/n_a, u.m. par pas ; C à WB : montants exécutés des lignes 1 à 5 ; `amortissement`
    = δK/n_a et `interets_L` = i_L L/n_a recalculés sur l'ouverture, comme F3 ; D_F reçu brut,
    lu en D̃_F = max(0 ; D_F) ici (lecture nette, engagement 3)."""
    # eq:finances_publiques-impot-entreprises
    resultat_avant_impot = (C + G + I + Delta_IN - WB - amortissement - interets_L
                            + i_D_pas * max(0.0, D_F))
    return tau_F * resultat_avant_impot


def transferts_vises(P_m1: float, pi_etoile_pas: float, theta_Tr: float, y_pot: float) -> float:
    """Tr^lev_t = P_{t−1}(1 + π^{∗,pas}_t) θ_Tr y^pot_t, u.m. par pas ; membre de E6 (renvoi
    `eq:finances_publiques-transferts`)."""
    return P_m1 * (1.0 + pi_etoile_pas) * theta_Tr * y_pot


def transferts(Tr_lev: float, M_G: float, T_H: float, interets: float, G_plan: float) -> float:
    """E6 : Tr_t = min{Tr^lev_t ; max(0 ; M^G_t + T_{H,t} − i_CB B_t/n_a − G^plan_t)}, u.m. par
    pas ; `interets` = i_CB B_t/n_a, somme des trois termes de E7. **Lecture brute de M^G** dans
    le plafond (exception d'identité, ADR 0013, annotation du 15/11/2026, point 4 ; lecture (ii)
    de `monnaie`), sous le max(0 ; ·) extérieur, qui tient Tr ≥ 0."""
    # eq:finances_publiques-transferts
    return min(Tr_lev, max(0.0, M_G + T_H - interets - G_plan))


def interets_sur_titres(i_CB_pas: float, B_H: float, B_Bk: float,
                        B_CB: float) -> tuple[float, float, float]:
    """E7 : lignes 11a, 11b, 11c = i_CB B_H/n_a, i_CB B_Bk/n_a, i_CB B_CB/n_a, u.m. par pas, au
    taux du tour (i_B ≡ i_CB), converti au pas, sur les encours d'ouverture."""
    # eq:finances_publiques-interets-titres
    return i_CB_pas * B_H, i_CB_pas * B_Bk, i_CB_pas * B_CB


def encaisse_visee(nu_G: float, G: float, Tr: float, interets: float) -> float:
    """E8 : M^{G*}_t = ν_G PB_t, PB_t = G_t + Tr_t + i_CB B_t/n_a, u.m. ; montants exécutés des
    lignes 2, 6 et 11a à 11c."""
    # eq:finances_publiques-encaisse-visee
    return nu_G * (G + Tr + interets)


def besoin_d_emission(G: float, Tr: float, interets: float, T: float, Pi_CB: float,
                      M_G_etoile: float, M_G: float) -> float:
    """E9 : Em_t = G_t + Tr_t + i_CB B_t/n_a − T_{H,t} − T_{F,t} − Π^CB_t + M^{G*}_t − M^G_t,
    u.m. par pas ; `T` = ligne 7 exécutée (T_H + T_F), Π^CB_t de la phase 1.
    **Lecture brute de M^G** (exception d'identité, ADR 0013, annotation du 15/11/2026, point 4) :
    la poussière est absorbée à l'émission du pas. Appelée une fois par pas (point 5)."""
    # eq:finances_publiques-besoin-emission
    return G + Tr + interets - T - Pi_CB + M_G_etoile - M_G


def souscriptions_banque_centrale_et_menages(theta_CB: float, Em: float) -> tuple[float, float]:
    """E10 : (ΔB^prim_CB, ΔB^prim_H) = (θ_CB,t Em_t ; 0), lignes 19a-BC et 19a-ménages, u.m. par
    pas ; θ_CB,t écrit par le bloc 8 en phase 1 ; ligne 19a-ménages à montant nul (M27)."""
    # eq:finances_publiques-souscription-banque-centrale
    return theta_CB * Em, 0.0


def souscription_banque(varsigma_B: float, Em: float, Delta_B_CB: float) -> float:
    """E11 : ΔB^prim_Bk = (1 − ς_{B,t})(Em_t − ΔB^prim_CB), ligne 19a-banque, u.m. par pas ;
    reliquat déclaré (C19) ; même forme sous Em < 0 (rachat, P159)."""
    # eq:finances_publiques-souscription-banque
    return (1.0 - varsigma_B) * (Em - Delta_B_CB)


def assiette_de_l_impot(WB: float, interets_D_H: float, Div_F: float, Div_Bk: float,
                        pi_etoile_pas: float, D_H: float, T_cou: float) -> float:
    """E12 : Y^HS_t = WB_t + i_D D̃_H/n_a + Div_F + Div_Bk − π^{∗,pas}_t D̃_H − T^cou_t, u.m. par
    pas ; montants exécutés des lignes 5, 10, 14 et 15 dans la colonne des ménages ; D_H reçu
    brut, lu en D̃_H = max(0 ; D_H) ici (lecture nette, engagement 3) ; T^cou de la phase 2."""
    # eq:finances_publiques-assiette-impot
    return WB + interets_D_H + Div_F + Div_Bk - pi_etoile_pas * max(0.0, D_H) - T_cou


def part_non_payee(du: float, disponible: float) -> tuple[float, float]:
    """E13 : (payé, non payé) = (min(dû ; max(0 ; disponible)) ; dû − payé), u.m. par pas, pour
    les deux parts : transferts non versés, Tr^lev_t − Tr_t (dû Tr^lev, disponible Tr, payé par
    E6 en phase 2) ; perte non couverte |Π^CB_t| − mc_t, mc_t = min(|Π^CB_t| ; max(0 ;
    M^{G,8a}_t)) (dû |Π^CB|, disponible M^{G,8a}, lu en max(0 ; ·) ici). Contrainte de
    conservation, sans paramètre ; 0 ≤ payé ≤ dû pour dû ≥ 0."""
    # eq:finances_publiques-parts-non-payees
    paye = min(du, max(0.0, disponible))
    return paye, du - paye


# --------------------------------------------------------------------------
# Bloc
# --------------------------------------------------------------------------


def _ouverture(*champs: str) -> tuple[Lecture, ...]:
    return tuple(Lecture(OUVERTURE, champ) for champ in champs)


def _grand_livre(*lignes: str) -> tuple[Lecture, ...]:
    return tuple(Lecture(GRAND_LIVRE, ligne) for ligne in lignes)


class FinancesPubliques:
    """Bloc 9 : phases 2, 5, 6, 7 et 8 (b) ; aucun attribut d'instance."""

    __slots__ = ()
    declaration = DeclarationDeBloc("finances_publiques", (
        Siege("2", ("G_vise", "G_plan", "T_cou", "T_H", "Tr_lev", "Tr", "iB_BH", "iB_BBk",
                    "iB_BCB"),
              _ouverture("M_G", "pr", "N_pa", "Y_HS_m1", "pi_etoile", "B_H", "B_Bk", "B_CB",
                         "L_CB", "Res")
              + (Lecture(REGISTRE, "dernier_prix"), Lecture("0", "Gamma_e"),
                 Lecture("0", "pi_etoile_pas"), Lecture("1", "i_CB")),
              (), (), ()),
        Siege("5", (), (Lecture("5", "p"), Lecture("5", "G_vol")), ("2",), (), ()),
        Siege("6", ("T_F", "Tr_non_verses"),
              (Lecture("2", "T_H"), Lecture("2", "Tr_lev"), Lecture("2", "Tr"),
               Lecture("2", "iB_BH"), Lecture("2", "iB_BBk"), Lecture("2", "iB_BCB"))
              + _ouverture("K", "L", "D_F", "i_L", "i_D")
              + _grand_livre("1", "2", "3", "4", "5"),
              ("6", "7", "11a", "11b", "11c"), (), ()),
        Siege("7", ("M_G_etoile", "Em"),
              _ouverture("M_G", "D_H")
              + (Lecture("0", "varsigma_B"), Lecture("0", "pi_etoile_pas"),
                 Lecture("1", "theta_CB"), Lecture("1", "Pi_CB"), Lecture("2", "T_cou"))
              + _grand_livre("2", "6", "7", "11a", "11b", "11c", "5", "10", "14", "15"),
              ("19a-ménages", "19a-banque", "19a-BC"), (), ("Y_HS_m1",)),
        Siege("8b", ("perte_non_couverte",), (Lecture("1", "Pi_CB"), Lecture(GRAND_LIVRE, "M_G")),
              (), ("16",), ()),
    ))

    def phase_2(self, vue) -> None:
        """Plan de dépense (E1), couverture des intérêts (E4), impôt des ménages (E3), intérêts sur
        titres (E7, calculés une fois par pas, écrits en variables du pas), transferts (E6) ; ne
        lit que l'ouverture, la phase 1, le registre et le moteur."""
        table = vue.parametres.finances_publiques
        P_m1 = vue.dernier_prix()
        pi_etoile_pas = vue.lire("pi_etoile_pas")
        i_CB = vue.lire("i_CB")
        y_pot = production_potentielle(vue.ouverture.pr, vue.parametres.travail.U_eq,
                                       vue.ouverture.N_pa)
        G_vise = depense_visee(P_m1, pi_etoile_pas, table.theta_G, y_pot)
        # E1 lit max(0 ; M^G) dans sa fonction (lecture nette) ; E6 et l'assiette de E4 lisent
        # M^G brut (exceptions d'identité, ADR 0013, annotation du 15/11/2026, point 4).
        G_plan = plan_de_depense(vue.ouverture.M_G, G_vise)
        i_ref = taux_de_reference(vue.parametres.banque_centrale.r_bar.valeur,
                                  vue.ouverture.pi_etoile)
        T_cou = couverture_des_interets(
            table.phi, par_pas(TauxDeFlux(i_CB - i_ref)), vue.ouverture.B_H, vue.ouverture.B_Bk,
            vue.ouverture.B_CB, vue.ouverture.L_CB, vue.ouverture.Res, vue.ouverture.M_G)
        T_H = impot_des_menages(table.tau_H, vue.lire("Gamma_e"), vue.ouverture.Y_HS_m1, T_cou)
        Tr_lev = transferts_vises(P_m1, pi_etoile_pas, table.theta_Tr, y_pot)
        iB_BH, iB_BBk, iB_BCB = interets_sur_titres(par_pas(TauxDeFlux(i_CB)), vue.ouverture.B_H,
                                                    vue.ouverture.B_Bk, vue.ouverture.B_CB)
        # i_CB B_t/n_a de E6 : somme des trois termes de E7, dans l'ordre des lignes 11a à 11c,
        # celle que la phase 7 relit au grand livre ; la phase 6 propose ces mêmes termes.
        interets = iB_BH + iB_BBk + iB_BCB
        vue.ecrire_pas("G_vise", G_vise)
        vue.ecrire_pas("G_plan", G_plan)
        vue.ecrire_pas("T_cou", T_cou)
        vue.ecrire_pas("T_H", T_H)
        vue.ecrire_pas("Tr_lev", Tr_lev)
        vue.ecrire_pas("Tr", transferts(Tr_lev, vue.ouverture.M_G, T_H, interets, G_plan))
        vue.ecrire_pas("iB_BH", iB_BH)
        vue.ecrire_pas("iB_BBk", iB_BBk)
        vue.ecrire_pas("iB_BCB", iB_BCB)

    def phase_5(self, vue) -> None:
        """Dépense exécutée (ligne 2), au prix du pas sur le volume servi."""
        vue.proposer("2", {"G": depense(vue.lire("p"), vue.lire("G_vol"))})

    def phase_6(self, vue) -> None:
        """Transferts (ligne 6) et part non versée (E13), impôts (ligne 7 : E3, E5), intérêts sur
        titres (lignes 11a à 11c : termes de E7 calculés en phase 2, lus sans recalcul)."""
        table = vue.parametres.finances_publiques
        i_D_pas = par_pas(TauxDeFlux(vue.ouverture.i_D))
        # E5 : intérêts et amortissement recalculés sur l'ouverture, comme F3 ; D_F reçu brut, lu
        # en max(0 ; ·) dans la fonction (lecture nette).
        T_F = impot_des_entreprises(
            table.tau_F, vue.grand_livre.montant_execute_ligne("1"),
            vue.grand_livre.montant_execute_ligne("2"), vue.grand_livre.montant_execute_ligne("3"),
            vue.grand_livre.montant_execute_ligne("4"), vue.grand_livre.montant_execute_ligne("5"),
            par_pas(vue.parametres.investissement.delta) * vue.ouverture.K,
            par_pas(TauxDeFlux(vue.ouverture.i_L)) * vue.ouverture.L, i_D_pas, vue.ouverture.D_F)
        Tr = vue.lire("Tr")
        _, Tr_non_verses = part_non_payee(vue.lire("Tr_lev"), Tr)
        vue.ecrire_pas("T_F", T_F)
        vue.ecrire_pas("Tr_non_verses", Tr_non_verses)
        vue.proposer("6", {"Tr": Tr})
        vue.proposer("7", {"T_H": vue.lire("T_H"), "T_F": T_F})
        vue.proposer("11a", {"iB_BH": vue.lire("iB_BH")})
        vue.proposer("11b", {"iB_BBk": vue.lire("iB_BBk")})
        vue.proposer("11c", {"iB_BCB": vue.lire("iB_BCB")})

    def phase_7(self, vue) -> None:
        """Encaisse visée (E8) et besoin d'émission (E9), calculés une fois ; souscriptions (E10,
        E11), lignes 19a ; assiette de l'impôt du pas suivant (E12), variable d'état."""
        G = vue.grand_livre.montant_execute_ligne("2")
        Tr = vue.grand_livre.montant_execute_ligne("6")
        interets = (vue.grand_livre.montant_execute_ligne("11a")
                    + vue.grand_livre.montant_execute_ligne("11b")
                    + vue.grand_livre.montant_execute_ligne("11c"))
        M_G_etoile = encaisse_visee(vue.parametres.finances_publiques.nu_G, G, Tr, interets)
        # E9 lit M^G brut (exception d'identité, point 4) : la poussière est absorbée ici.
        Em = besoin_d_emission(G, Tr, interets, vue.grand_livre.montant_execute_ligne("7"),
                               vue.lire("Pi_CB"), M_G_etoile, vue.ouverture.M_G)
        Delta_B_CB, Delta_B_H = souscriptions_banque_centrale_et_menages(vue.lire("theta_CB"), Em)
        vue.ecrire_pas("M_G_etoile", M_G_etoile)
        vue.ecrire_pas("Em", Em)
        vue.proposer("19a-ménages", {"Delta_BH_prim": Delta_B_H})
        vue.proposer("19a-banque", {"Delta_BBk_prim": souscription_banque(
            vue.lire("varsigma_B"), Em, Delta_B_CB)})
        vue.proposer("19a-BC", {"Delta_BCB_prim": Delta_B_CB})
        # E12 : D_H reçu brut, lu en max(0 ; ·) dans la fonction (lecture nette).
        vue.ecrire_etat("Y_HS_m1", assiette_de_l_impot(
            vue.grand_livre.montant_execute("5", "menages"),
            vue.grand_livre.montant_execute("10", "menages"),
            vue.grand_livre.montant_execute("14", "menages"),
            vue.grand_livre.montant_execute("15", "menages"),
            vue.lire("pi_etoile_pas"), vue.ouverture.D_H, vue.lire("T_cou")))

    def phase_8b(self, vue) -> None:
        """Perte de la banque centrale non couverte (E13, seconde part) : montant couvert déclaré
        au noyau dès que Π^CB < 0 (A3.2), sans ordre avec le bloc 8."""
        Pi_CB = vue.lire("Pi_CB")
        if Pi_CB < 0.0:
            montant_couvert, perte_non_couverte = part_non_payee(
                0.0 - Pi_CB, vue.grand_livre.position("M_G"))
            vue.declarer_montant_couvert("16", montant_couvert)
        else:
            perte_non_couverte = 0.0
        vue.ecrire_pas("perte_non_couverte", perte_non_couverte)
