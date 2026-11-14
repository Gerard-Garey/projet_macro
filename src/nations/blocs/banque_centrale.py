"""Bloc 8, banque centrale et anticipations (radical `banque_centrale`).

Contrat : décision M32 (option C : action intégrale sans fuite, Fisher sur la
cible ; anticipation adaptative formée en phase 1 ; cible reconduite ; corridor
de largeur nulle ; lectures (a) à (e)) et M33 (part à l'émission, lignes 19a ;
ADR 0011) ; spécification, `sec:banque_centrale`, `tab:banque_centrale-equations`
et `tab:banque_centrale-phases` ; fiche `docs/blocs/banque_centrale.md`, § 9.1 à
9.6 ; ADR 0013, annotation du 14/11/2026, points 3 à 9 (P92, P96) ; issue #91.

**Équations.** BC1 à BC9 de la spécification sont des fonctions pures du
module, appelables directement, qui reçoivent des scalaires (taux déjà
convertis au pas) ; les méthodes de phase lisent la vue, convertissent les
taux par `nations.moteur.conversions` seulement, appellent ces fonctions et
écrivent. Chaque équation porte sa balise `eq:banque_centrale-…` (fiche, § 9.1)
et garde son identifiant BC1 à BC9.

**Formes exécutées** (ADR 0013, annotation du 14/11/2026, points 5, 8 et 9) :

- BC1 : i_CB,t = i^règle_t au socle (levier de taux fermé jusqu'au J4) ;
- BC3 en **forme convexe**, π^e_{t+1} = (1 − c) π^e_t + c π_{t−1}, c = λ_e/n_a
  (P92), algébriquement égale à BC3 telle qu'écrite. Sous 0 < λ_e ≤ n_a,
  π^e_t > −1 et 1 + π_{t−1} > 0, elle n'a rendu aucun π^e_{t+1} ≤ −1 sur les
  tirages de `tests/unitaires/test_banque_centrale.py` (10^6 tirages et un lot
  adverse sur les bords), où la forme littérale π^e + c(π − π^e) rend −1 sur
  le seul lot adverse : c'est une mesure, non une preuve. La précondition
  1 + π_{t−1} > 0 est tenue par `Vue.glissement()`, qui refuse un glissement
  hors de ce domaine, −1 exactement compris, ou non fini, sans écrêtage ;
- BC6 sous sa **forme générale**, (i_B B_CB + i_CB L^CB − i_res Res)/n_a, sur
  les encours d'ouverture et le taux du tour ; i_B ≡ i_res ≡ i_CB sont des
  identités de notation (ADR 0011, P6 ; aucune variable `i_res` ni `i_B`) : les
  trois taux reçus sont i_CB converti au pas. La forme « au socle »,
  i_CB (E^CB + M^G)/n_a, est une identité de bilan vérifiée par test, non
  exécutée (elle lirait une valeur nette, H5.3) ;
- BC7 : ligne 12 au taux i_res ≡ i_CB.

**Phases** (`tab:banque_centrale-phases` ; annotation du 14/11/2026, point 5) :

- phase 1, second groupe, avec le bloc 3 (aucune lecture mutuelle) : lit
  l'ouverture (π*, r̂*, π^e, B_CB, L^CB, Res) et le glissement du registre ;
  jamais W_t, p_t ni U_{t−1}. BC1, puis BC2 à BC5 (ouverture seule), puis BC6,
  qui lit le taux du tour ; écrit les variables du pas `i_regle`, `i_CB`,
  `theta_CB`, `Pi_CB` et les états `r_hat_etoile`, `pi_e`, `pi_etoile` ;
- phase 8 (a) : lit l'ouverture (Res, L^CB) et `i_CB` (phase 1) ; propose les
  lignes 12 (BC7) et 13 (BC8) ;
- phase 8 (b) : lit `Pi_CB` (phase 1) ; propose la ligne 16 (BC9).

Aucune écriture en phases 2 à 7 ; aucune ligne 19b. **Bornes** : aucune
(`sec:banque_centrale-conditions`) : ni plancher du taux directeur, ni écrêtage
du taux neutre ou de l'anticipation ; un taux négatif donne une prescription,
un résultat et une ligne 16 négatifs.
"""

from __future__ import annotations

from nations.moteur.contrat_bloc import OUVERTURE, REGISTRE, DeclarationDeBloc, Lecture, Siege
from nations.moteur.conversions import TauxDeFlux, par_pas

# --------------------------------------------------------------------------
# Équations BC1 à BC9 : fonctions pures
# --------------------------------------------------------------------------


def taux_indique_par_la_regle(r_hat: float, pi_etoile: float, pi_prec: float,
                              a_pi: float) -> float:
    """BC1 : 1 + i^règle_t = (1 + r̂*_t)(1 + π*_t) + a_π(π_{t−1} − π*_t), par an, taux de flux ;
    au socle, i_CB,t = i^règle_t. r̂*_t et π*_t lus à l'ouverture, π_{t−1} au registre."""
    # eq:banque_centrale-regle-taux
    return (1.0 + r_hat) * (1.0 + pi_etoile) + a_pi * (pi_prec - pi_etoile) - 1.0


def taux_neutre_suivant(r_hat: float, pi_prec: float, pi_etoile: float,
                        a_I_pas: float) -> float:
    """BC2 : r̂*_{t+1} = r̂*_t + (a_I/n_a)(π_{t−1} − π*_t), par an, taux de croissance ;
    `a_I_pas` = a_I/n_a. Action intégrale sans fuite : ni rappel, ni réinitialisation."""
    # eq:banque_centrale-taux-neutre
    return r_hat + a_I_pas * (pi_prec - pi_etoile)


def anticipation_suivante(pi_e: float, pi_prec: float, c: float) -> float:
    """BC3, forme convexe (P92) : π^e_{t+1} = (1 − c) π^e_t + c π_{t−1}, c = λ_e/n_a, par an,
    taux de croissance ; égale à π^e_t + (λ_e/n_a)(π_{t−1} − π^e_t)."""
    # eq:banque_centrale-anticipation
    return (1.0 - c) * pi_e + c * pi_prec


def cible_suivante(pi_etoile: float) -> float:
    """BC4 : π*_{t+1} = π*_t, par an, taux de croissance (cible reconduite, levier fermé)."""
    # eq:banque_centrale-cible
    return pi_etoile


def part_a_l_emission(theta_CB: float) -> float:
    """BC5 : θ_CB,t = θ_CB, fraction du besoin d'émission, lue par le bloc 9 en phase 7."""
    # eq:banque_centrale-part-souscription
    return theta_CB


def resultat(i_B_pas: float, B_CB: float, i_CB_pas: float, L_CB: float, i_res_pas: float,
             Res: float) -> float:
    """BC6, forme générale : Π^CB_t = (i_B B_CB + i_CB L^CB − i_res Res)/n_a, u.m. par pas, sur
    les encours d'ouverture ; les taux reçus sont convertis au pas (i_B ≡ i_res ≡ i_CB)."""
    # eq:banque_centrale-resultat
    return i_B_pas * B_CB + i_CB_pas * L_CB - i_res_pas * Res


def interets_sur_reserves(i_res_pas: float, Res: float) -> float:
    """BC7 : ligne 12 = i_res Res/n_a, u.m. par pas (i_res ≡ i_CB), sur l'encours d'ouverture."""
    # eq:banque_centrale-interets-reserves
    return i_res_pas * Res


def interets_sur_refinancement(i_CB_pas: float, L_CB: float) -> float:
    """BC8 : ligne 13 = i_CB L^CB/n_a, u.m. par pas, sur l'encours d'ouverture."""
    # eq:banque_centrale-interets-refinancement
    return i_CB_pas * L_CB


def versement_du_resultat(Pi_CB: float) -> float:
    """BC9 : ligne 16 = Π^CB_t, u.m. par pas, versée sans troncature ; une perte est un versement
    négatif, payé par le compte du Trésor."""
    # eq:banque_centrale-versement-resultat
    return Pi_CB


# --------------------------------------------------------------------------
# Bloc
# --------------------------------------------------------------------------


def _ouverture(*champs: str) -> tuple[Lecture, ...]:
    return tuple(Lecture(OUVERTURE, champ) for champ in champs)


class BanqueCentrale:
    """Bloc 8 : phases 1, 8 (a) et 8 (b) ; aucun attribut d'instance."""

    __slots__ = ()
    declaration = DeclarationDeBloc("banque_centrale", (
        Siege("1", ("i_regle", "i_CB", "theta_CB", "Pi_CB"),
              _ouverture("pi_etoile", "r_hat_etoile", "pi_e", "B_CB", "L_CB", "Res")
              + (Lecture(REGISTRE, "glissement"),),
              (), (), ("pi_e", "r_hat_etoile", "pi_etoile")),
        Siege("8a", (), _ouverture("Res", "L_CB") + (Lecture("1", "i_CB"),), ("12", "13"), (), ()),
        Siege("8b", (), (Lecture("1", "Pi_CB"),), ("16",), (), ()),
    ))

    def phase_1(self, vue) -> None:
        """Règle de taux, taux neutre, anticipation, cible, part à l'émission et résultat."""
        table = vue.parametres.banque_centrale
        pi_prec = vue.glissement()
        pi_etoile = vue.ouverture.pi_etoile
        r_hat = vue.ouverture.r_hat_etoile
        i_regle = taux_indique_par_la_regle(r_hat, pi_etoile, pi_prec, table.a_pi)
        # Au socle, le taux directeur du tour est la prescription (BC1 ; levier fermé).
        i_CB = i_regle
        vue.ecrire_pas("i_regle", i_regle)
        vue.ecrire_pas("i_CB", i_CB)
        vue.ecrire_etat("r_hat_etoile",
                        taux_neutre_suivant(r_hat, pi_prec, pi_etoile, par_pas(table.a_I)))
        vue.ecrire_etat("pi_e", anticipation_suivante(vue.ouverture.pi_e, pi_prec,
                                                      par_pas(table.lambda_e)))
        vue.ecrire_etat("pi_etoile", cible_suivante(pi_etoile))
        vue.ecrire_pas("theta_CB", part_a_l_emission(table.theta_CB))
        # i_B ≡ i_res ≡ i_CB : un seul taux du tour, converti au pas.
        i_pas = par_pas(TauxDeFlux(i_CB))
        vue.ecrire_pas("Pi_CB", resultat(i_pas, vue.ouverture.B_CB, i_pas, vue.ouverture.L_CB,
                                         i_pas, vue.ouverture.Res))

    def phase_8a(self, vue) -> None:
        """Intérêts sur réserves (ligne 12) et sur refinancement (ligne 13)."""
        i_pas = par_pas(TauxDeFlux(vue.lire("i_CB")))
        vue.proposer("12", {"ires_Res": interets_sur_reserves(i_pas, vue.ouverture.Res)})
        vue.proposer("13", {"iCB_LCB": interets_sur_refinancement(i_pas, vue.ouverture.L_CB)})

    def phase_8b(self, vue) -> None:
        """Versement du résultat à l'État (ligne 16)."""
        vue.proposer("16", {"Pi_CB": versement_du_resultat(vue.lire("Pi_CB"))})
