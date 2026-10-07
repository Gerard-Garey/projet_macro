"""Identités stock-flux, échelle des bilans, tolérances et contrôle de signe.

Contrat : ADR 0012, A3.1, A5 et point 8 (décidé le 07/10/2026, (iii-b)) ;
spécification, `sec:cadre-identites` et `sec:cadre-caisse` ; fiche
« temps et comptabilité », § 9.1 (onze identités du noyau).

Chaque identité a ici sa fonction ; le grand livre les appelle à chaque
clôture de phase, et en phase 9 pour la couche noyau.

- `echelle_bilan` : S d'un secteur, somme des valeurs absolues de ses postes,
  valeur nette comprise, évaluée **à l'ouverture du pas** (P33 (a)) ;
- `valeur_nette_stock`, `valeur_nette_flux` : V calculée deux fois ;
- `dans_la_tolerance` : forme commune des contrôles par pas, |r| ≤ ε × S,
  jamais |r| / S ≤ ε (une échelle nulle ne divise pas) ;
- `residu_somme_ligne`, `residu_somme_colonne`, `residu_cloture_poste` : les
  résidus des identités par pas ;
- `residu_variation_monnaie` (ΔM) et `residu_variation_monnaie_centrale` (ΔH) :
  une fonction par identité, qui sert à la fois la porte ligne par ligne et le
  contrôle du pas en phase 9 ;
- `verifier_identite` : contrôle d'un résidu à ε × S, défaut sinon ;
- `verifier_tolerance_cumulee` : |V^stock − V^flux| ≤ ε_V × S ;
- `verifier_reserves_cloture` : Res_{t+1} ≥ 0, strict ;
- `verifier_caisse` : lecture nette des moyens de paiement des payeurs non
  bancaires, x + ε × S_payeur ≥ 0.

La fermeture du système, Σ_s V^stock_s = K + IN, n'est pas contrôlée ici :
c'est une tautologie de la tenue par positions (chaque instrument est +1 chez
son détenteur, −1 chez son émetteur), qu'aucun flux ne peut violer ; elle est
vérifiée par les tests (ADR 0012, annotation du 07/10/2026, point 4).

**Contrôle de signe** (ADR 0012, point 8, dernier alinéa) : toute comparaison
d'un montant à zéro dans `nations.noyau` passe par la seule fonction
`controle_de_signe`. Le domaine de chaque contrôle est une **propriété
déclarée de sa règle** (`Regle.domaine`), fixée par la structure de la
position contrôlée : ce n'est pas un drapeau de mode. Un test textuel vérifie
qu'aucune autre comparaison de signe n'existe dans `src/nations/noyau/`.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import Enum

from nations.noyau.catalogue import (
    MOYENS_LECTURE_NETTE,
    POSTES_DU_BILAN,
    POSTES_MONNAIE,
    POSTES_MONNAIE_CENTRALE,
)
from nations.noyau.diagnostics import DefautComptable


class Domaine(Enum):
    """Domaine de signe d'un contrôle, déclaré par sa règle."""

    POSITIF_OU_NUL = "x ≥ 0"
    POSITIF_OU_NUL_A_EPSILON_S = "x + ε × S ≥ 0"
    STRICTEMENT_POSITIF = "x > 0"
    STRICTEMENT_NEGATIF = "x < 0"


@dataclass(frozen=True, slots=True)
class Regle:
    """Une règle de contrôle : nom (label `eq:` s'il existe) et domaine de signe."""

    nom: str
    domaine: Domaine | None


# Identités par pas (forme |r| ≤ ε × S) et cumulée (ε_V × S).
SOMME_LIGNE = Regle("eq:noyau-somme-ligne", None)
SOMME_COLONNE = Regle("eq:noyau-somme-colonne", None)
CLOTURE_POSTE = Regle("eq:noyau-cloture-poste", None)
VARIATION_MONNAIE = Regle("eq:noyau-variation-monnaie", None)
VARIATION_MONNAIE_CENTRALE = Regle("eq:noyau-variation-monnaie-centrale", None)
TOLERANCE_CUMULEE = Regle("eq:noyau-tolerance-cumulee", None)

# Contrôles de signe, chacun avec son domaine déclaré (ADR 0012, A5 et point 8).
# Res_{t+1} : une seule ligne (21) la touche dans la phase contrôlée, forme
# exacte : strict. Lecture nette (D_H, D_F, M^G) : plusieurs lignes par phase,
# sommées par le noyau, sans forme exacte : −ε × S_payeur.
RESERVES_CLOTURE = Regle("eq:noyau-reserves-cloture", Domaine.POSITIF_OU_NUL)
CAISSE = Regle("eq:noyau-caisse-nette", Domaine.POSITIF_OU_NUL_A_EPSILON_S)
# Domaines d'interface : échelle à l'ouverture (ADR 0012, point 11 ; finie,
# en plus, par l'annotation du 07/10/2026, point 5), tolérances reçues, sens
# des montants proposés (A2), montant couvert et perte de la ligne 16 (A3.2),
# débit d'un moyen de paiement (diagnostic).
ECHELLE = Regle("eq:noyau-echelle-bilan", Domaine.STRICTEMENT_POSITIF)
TOLERANCE_POSITIVE = Regle("domaine des tolérances", Domaine.STRICTEMENT_POSITIF)
SENS_DU_MONTANT = Regle("sens du montant de la ligne", Domaine.POSITIF_OU_NUL)
MONTANT_COUVERT = Regle("domaine du montant couvert", Domaine.POSITIF_OU_NUL)
# c ≤ |Π| s'écrit |Π| − c ≥ 0, strict : la soustraction de deux flottants est
# nulle si et seulement s'ils sont égaux, et l'arrondi est monotone, si bien
# que le signe de fl(|Π| − c) est exactement celui de |Π| − c.
MONTANT_COUVERT_AU_PLUS_LA_PERTE = Regle("montant couvert au plus la perte, |Π| − c ≥ 0",
                                         Domaine.POSITIF_OU_NUL)
PERTE = Regle("ligne 16 négative", Domaine.STRICTEMENT_NEGATIF)
DEBIT = Regle("débit d'un moyen de paiement", Domaine.STRICTEMENT_NEGATIF)


def controle_de_signe(x: float, regle: Regle, epsilon: float, echelle: float) -> bool:
    """Vrai si x est dans le domaine de signe déclaré par la règle.

    Seule comparaison de signe du noyau. Sous `POSITIF_OU_NUL_A_EPSILON_S`, le
    contrôle s'écrit x + ε × S ≥ 0, S étant l'échelle du bilan du payeur
    évaluée à l'ouverture du pas ; les autres domaines ignorent ε et S. Un NaN
    n'est dans aucun domaine.
    """
    domaine = regle.domaine
    if domaine is Domaine.POSITIF_OU_NUL:
        return x >= 0.0
    if domaine is Domaine.POSITIF_OU_NUL_A_EPSILON_S:
        return x + epsilon * echelle >= 0.0
    if domaine is Domaine.STRICTEMENT_POSITIF:
        return x > 0.0
    if domaine is Domaine.STRICTEMENT_NEGATIF:
        return x < 0.0
    raise ValueError(f"règle sans domaine de signe : {regle.nom}")


def dans_la_tolerance(residu: float, echelle: float, epsilon: float) -> bool:
    """Forme commune des identités par pas : |résidu| ≤ ε × S (NaN : faux)."""
    return abs(residu) <= epsilon * echelle


def valeur_nette_stock(positions: Mapping[str, float], secteur: str) -> float:
    """V par le stock : actifs moins passifs du bilan du secteur, dans l'ordre des postes."""
    v = 0.0
    for poste, signe in POSTES_DU_BILAN[secteur]:
        v += signe * positions[poste]
    return v


def valeur_nette_flux(v_flux: float, resultat: float) -> float:
    """V par les flux : V^flux_{t+1} = V^flux_t + résultat net de distribution du pas.

    Le résultat est la somme des lignes 1 à 16 de la colonne du secteur
    (sous-colonne courante pour les entreprises) : les lignes 17 à 22 sont
    des échanges d'actifs, sans effet sur la valeur nette.
    """
    return v_flux + resultat


def echelle_bilan(positions: Mapping[str, float], secteur: str) -> float:
    """S d'un secteur : somme des valeurs absolues de ses postes, valeur nette comprise."""
    s = 0.0
    for poste, _ in POSTES_DU_BILAN[secteur]:
        s += abs(positions[poste])
    return s + abs(valeur_nette_stock(positions, secteur))


def residu_somme_ligne(cellules: Mapping[str, float]) -> float:
    """Somme des cellules d'une ligne exécutée, dans l'ordre des colonnes."""
    r = 0.0
    for v in cellules.values():
        r += v
    return r


def residu_somme_colonne(courant: float, capital: float) -> float:
    """Somme d'une colonne de secteur (les deux sous-colonnes des entreprises réunies)."""
    return courant + capital


def residu_cloture_poste(position: float, ouverture: float, cumul: float) -> float:
    """Clôture moins (ouverture plus somme des lignes exécutées qui touchent le poste)."""
    return position - (ouverture + cumul)


def residu_variation_monnaie(signes_et_montants: Iterable[tuple[tuple[int, int], float]],
                             variations: Mapping[str, float]) -> float:
    """ΔM : Σ sgn_M × montant, moins Δ(D_H + D_F).

    `signes_et_montants` donne, pour chaque ligne (ou chaque terme d'une
    contrepartie de règlement), sa signature (ΔM, ΔH) et son montant signé ;
    `variations` donne la variation des postes, un poste absent valant zéro.
    Une ligne seule donne la porte ligne par ligne ; toutes les lignes du pas
    et la variation depuis l'ouverture donnent le contrôle du pas.
    """
    recompose = 0.0
    for signature, montant in signes_et_montants:
        recompose += signature[0] * montant
    variation = 0.0
    for poste in POSTES_MONNAIE:
        if poste in variations:
            variation += variations[poste]
    return recompose - variation


def residu_variation_monnaie_centrale(
        signes_et_montants: Iterable[tuple[tuple[int, int], float]],
        variations: Mapping[str, float]) -> float:
    """ΔH : Σ sgn_H × montant, moins ΔRes (mêmes arguments que `residu_variation_monnaie`)."""
    recompose = 0.0
    for signature, montant in signes_et_montants:
        recompose += signature[1] * montant
    variation = 0.0
    for poste in POSTES_MONNAIE_CENTRALE:
        if poste in variations:
            variation += variations[poste]
    return recompose - variation


def verifier_identite(residu: float, echelle: float, epsilon: float, regle: Regle, *,
                      t: int, phase: str, secteur: str | None = None,
                      ligne: str | None = None, terme: str | None = None) -> float:
    """Contrôle |résidu| ≤ ε × S ; rend résidu / S, ou lève `DefautComptable`."""
    return verifier_identites(regle, [residu], [echelle], [(secteur, ligne, terme)], epsilon,
                              t=t, phase=phase)[1]


def verifier_identites(regle: Regle, residus: list[float], echelles: list[float],
                       objets: list[tuple[str | None, str | None, str | None]],
                       epsilon: float, *, t: int, phase: str) -> tuple[str, float]:
    """Contrôle une famille d'instances d'une identité, chacune à |r| ≤ ε × S.

    `objets` donne, pour chaque instance, (secteur, ligne, terme) du
    diagnostic. Rend l'instance la plus éloignée de zéro et son résidu / S,
    ou lève `DefautComptable` à la première instance hors tolérance. Un appel
    par famille et par clôture : le coût du noyau seul reste sous son seuil.
    """
    pire_objet = ""
    pire = 0.0
    for residu, echelle, objet in zip(residus, echelles, objets, strict=True):
        if not dans_la_tolerance(residu, echelle, epsilon):
            secteur, ligne, terme = objet
            raise DefautComptable(
                "identité violée au-delà de la tolérance relative à l'échelle du bilan",
                t=t, phase=phase, regle=regle.nom, secteur=secteur, ligne=ligne, terme=terme,
                residu=residu, echelle=echelle, tolerance=epsilon)
        # Sous la tolérance, une échelle nulle impose un résidu nul.
        rapport = 0.0 if residu == 0.0 else abs(residu) / echelle
        if pire < rapport:
            pire, pire_objet = rapport, objet[2] or objet[1] or objet[0] or ""
    return pire_objet, pire


def verifier_tolerance_cumulee(v_stock: float, v_flux: float, echelle: float,
                               epsilon_v: float, *, t: int, secteur: str) -> float:
    """|V^stock − V^flux| ≤ ε_V × S, S à l'ouverture du pas ; rend l'écart / S."""
    return verifier_identite(v_stock - v_flux, echelle, epsilon_v, TOLERANCE_CUMULEE,
                             t=t, phase="9", secteur=secteur)


def verifier_reserves_cloture(reserves: float, echelle_banque: float, *, t: int) -> None:
    """Res_{t+1} ≥ 0, strict, sans tolérance ; un découvert de clôture est un défaut."""
    if not controle_de_signe(reserves, RESERVES_CLOTURE, 0.0, echelle_banque):
        raise DefautComptable(
            "réserves de clôture négatives : le refinancement de la phase 8 (c) ne couvre "
            "pas le découvert intra-pas",
            t=t, phase="9", regle=RESERVES_CLOTURE.nom, secteur="banque", moyen="Res",
            residu=reserves, echelle=echelle_banque)


def verifier_caisse(positions: Mapping[str, float], echelles: Mapping[str, float],
                    epsilon: float, *, t: int, phase: str, positions_debut: Mapping[str, float],
                    mouvements_par_ligne: Mapping[str, Mapping[str, float]]) -> None:
    """Lecture nette : x_p + ε × S_p ≥ 0 pour chaque payeur non bancaire p, en fin de phase.

    p parcourt ménages (D_H), entreprises (D_F) et État (M^G), dans l'ordre de
    `MOYENS_LECTURE_NETTE` ; S_p est l'échelle du bilan du payeur, évaluée à
    l'ouverture du pas ; la banque et la banque centrale sont exclues. Le noyau
    vérifie, il n'ordonne ni ne rationne (ADR 0011, P4) ; la position n'est
    jamais ramenée à zéro. Le diagnostic nomme la phase, le payeur, le moyen,
    ses positions de début et de fin de phase rapportées à S, et les lignes de
    la phase qui le débitent : celles dont le mouvement net sur le moyen
    (`mouvements_par_ligne`, ligne → poste → mouvement) est strictement
    négatif, relevées seulement en cas de défaut.
    """
    for moyen, payeur in MOYENS_LECTURE_NETTE:
        position = positions[moyen]
        echelle_payeur = echelles[payeur]
        if controle_de_signe(position, CAISSE, epsilon, echelle_payeur):
            continue
        lignes_debitrices = tuple(
            ligne for ligne, mouvements in mouvements_par_ligne.items()
            if moyen in mouvements and controle_de_signe(mouvements[moyen], DEBIT, epsilon,
                                                         echelle_payeur))
        raise DefautComptable(
            "moyen de paiement d'un payeur non bancaire négatif en fin de phase",
            t=t, phase=phase, regle=CAISSE.nom, secteur=payeur, moyen=moyen,
            position_debut=positions_debut[moyen] / echelle_payeur,
            position_fin=position / echelle_payeur,
            lignes_debitrices=lignes_debitrices,
            ligne=", ".join(lignes_debitrices) or None,
            residu=position, echelle=echelle_payeur, tolerance=epsilon)
