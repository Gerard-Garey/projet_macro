"""Catalogue des lignes de la matrice des flux, des postes et de l'arbre des comptes.

Contrat : ADR 0012, A1, A2 et A4 ; spécification, `tab:matrice-bilans`,
`tab:matrice-flux`, `tab:portes-monnaie` et `tab:phases`. Ce module est la
**seule source** du catalogue dans le moteur ; un test le compare terme à terme
aux tables de la spécification, lues par `outils/verifier_matrices.py`.

- **Postes** : onze positions (détenteur, émetteur), dont deux actifs réels
  sans émetteur (K, IN) ; chacune tenue une fois (ADR 0005, points 7 et 8).
- **Lignes** : 28 lignes (1 à 10, 11a à 11c, 12 à 18, 19a et 19b par
  contrepartie, 20 à 22), décrites par leurs **termes simples**. Un terme
  apparaît une fois en + (colonne qui reçoit) et une fois en − (colonne qui
  verse) ; un flux proposé donne le montant de chaque terme, si bien qu'une
  ligne somme à zéro par construction (A2).
- **Règlement** : chaque terme d'une ligne décidée est un paiement de la
  colonne en − vers la colonne en +, réglé le long de l'**arbre des comptes**
  (ménages et entreprises tiennent un compte à la banque, la banque et l'État
  à la banque centrale). Les lignes 17, 20 et 22 sont les contreparties de
  règlement : jamais proposées, elles sont dérivées par le noyau des
  mouvements des moyens de paiement des deux parties (A4).
- **Signatures** (ΔM, ΔH) : jamais saisies, dérivées du règlement, et
  comparées par un test à `tab:portes-monnaie`.

Les identifiants de ligne sont ceux de la spécification (`"11a"`,
`"19a-ménages"`) ; les colonnes et les secteurs portent les radicaux ASCII
ci-dessous.
"""

from __future__ import annotations

from dataclasses import dataclass

# --------------------------------------------------------------------------
# Secteurs, colonnes, postes
# --------------------------------------------------------------------------

# Secteurs (bilans) dans l'ordre de `tab:matrice-bilans`.
SECTEURS = ("menages", "entreprises", "banque", "banque_centrale", "etat")

# Colonnes de `tab:matrice-flux`, dans l'ordre de la table ; les entreprises
# ont deux sous-colonnes, réunies dans leur bilan.
COLONNES = (
    "menages", "entreprises_courant", "entreprises_capital",
    "banque", "banque_centrale", "etat",
)
SECTEUR_DE_COLONNE = {
    "menages": "menages",
    "entreprises_courant": "entreprises",
    "entreprises_capital": "entreprises",
    "banque": "banque",
    "banque_centrale": "banque_centrale",
    "etat": "etat",
}
# Colonnes qui portent le résultat du secteur (V^flux) : sous-colonne
# courante pour les entreprises (ADR 0012, A5).
COLONNE_DE_RESULTAT = {
    "menages": "menages",
    "entreprises": "entreprises_courant",
    "banque": "banque",
    "banque_centrale": "banque_centrale",
    "etat": "etat",
}


@dataclass(frozen=True, slots=True)
class Poste:
    """Une position du grand livre : nom, détenteur (+), émetteur (−), écriture.

    `emetteur` vaut `None` pour un actif réel (K, IN), sans contrepartie.
    """

    nom: str
    detenteur: str
    emetteur: str | None
    ecriture: str


# Onze positions (ADR 0012, A1), en u.m., à l'ouverture du pas.
POSTES = (
    Poste("D_H", "menages", "banque", r"D_H"),
    Poste("D_F", "entreprises", "banque", r"D_F"),
    Poste("L", "banque", "entreprises", r"L"),
    Poste("B_H", "menages", "etat", r"B_H"),
    Poste("B_Bk", "banque", "etat", r"B_{\mathit{Bk}}"),
    Poste("B_CB", "banque_centrale", "etat", r"B_{\mathit{CB}}"),
    Poste("Res", "banque", "banque_centrale", r"\mathit{Res}"),
    Poste("L_CB", "banque_centrale", "banque", r"L^{\mathit{CB}}"),
    Poste("M_G", "etat", "banque_centrale", r"M^G"),
    Poste("K", "entreprises", None, r"K"),
    Poste("IN", "entreprises", None, r"\mathit{IN}"),
)
NOMS_POSTES = tuple(p.nom for p in POSTES)
POSTE = {p.nom: p for p in POSTES}

# Postes de chaque bilan, avec leur signe (+1 actif, −1 passif), dans l'ordre
# de POSTES.
POSTES_DU_BILAN = {
    s: tuple((p.nom, 1.0 if p.detenteur == s else -1.0)
             for p in POSTES if s in (p.detenteur, p.emetteur))
    for s in SECTEURS
}

# Variable d'état V^flux de chaque secteur (propriétaire : noyau ; ADR 0012, A5).
VALEUR_NETTE_FLUX = {s: f"V_flux_{s}" for s in SECTEURS}

# Arbre des comptes (ADR 0012, A4) : le compte que chaque secteur tient, et le
# secteur qui le tient ; la banque centrale est la racine.
COMPTES = {
    "menages": ("D_H", "banque"),
    "entreprises": ("D_F", "banque"),
    "banque": ("Res", "banque_centrale"),
    "etat": ("M_G", "banque_centrale"),
    "banque_centrale": None,
}

# Moyens de paiement soumis à la lecture nette du contrôle de caisse, avec leur
# payeur (ADR 0012, A5 : ménages, entreprises, État ; banque et banque
# centrale exclues).
MOYENS_LECTURE_NETTE = (("D_H", "menages"), ("D_F", "entreprises"), ("M_G", "etat"))

# Postes de la masse monétaire (M = D_H + D_F) et de la monnaie centrale
# (H = Res), sans billets au socle (`sec:cadre-portes`).
POSTES_MONNAIE = ("D_H", "D_F")
POSTES_MONNAIE_CENTRALE = ("Res",)

# Signature (ΔM, ΔH) par unité de chaque moyen de paiement de l'arbre des
# comptes : c'est la lecture « poste » de `tab:portes-monnaie` pour les
# contreparties de règlement (17 porte D_H et D_F, 20 porte Res, 22 porte M^G),
# qui sert leurs portes à l'exécution (ADR 0012, A5, « contreparties comprises »).
SIGNATURE_DU_MOYEN = {
    compte[0]: (int(compte[0] in POSTES_MONNAIE), int(compte[0] in POSTES_MONNAIE_CENTRALE))
    for compte in COMPTES.values() if compte is not None
}

# Ordre des clôtures d'un pas : onze clôtures (ADR 0012, A3.3).
PHASES = ("1", "2", "3", "4", "5", "6", "7", "8a", "8b", "8c", "9")

# Couples (ligne, bloc payeur) qui admettent un montant couvert déclaré
# (ADR 0012, A3.2) : liste fermée, réduite au socle à la perte de la banque
# centrale payée par l'État.
COUPLES_MONTANT_COUVERT = frozenset({("16", "finances_publiques")})
# Lignes de ces couples : une telle ligne proposée strictement négative exige
# la déclaration de son montant couvert (ADR 0012, annotation du 07/10/2026,
# point 2).
LIGNES_A_MONTANT_COUVERT = frozenset(ligne for ligne, _ in COUPLES_MONTANT_COUVERT)


def chemin_de_reglement(payeur: str, beneficiaire: str) -> tuple[tuple[str, float], ...]:
    """Mouvements des moyens de paiement pour un paiement d'une unité.

    Le paiement remonte l'arbre des comptes depuis le payeur jusqu'à
    l'ancêtre commun (chaque compte quitté baisse), puis redescend vers le
    bénéficiaire (chaque compte atteint monte) : entre ménages et État, D_H,
    Res et M^G bougent ensemble ; entre banque et État, Res et M^G ; entre
    banque centrale et banque, Res seule ; à l'intérieur d'un secteur, rien.
    """
    def montee(secteur: str) -> list[str]:
        chaine = [secteur]
        while COMPTES[chaine[-1]] is not None:
            chaine.append(COMPTES[chaine[-1]][1])
        return chaine

    haut_payeur = montee(payeur)
    haut_beneficiaire = montee(beneficiaire)
    ancetre = next(s for s in haut_payeur if s in haut_beneficiaire)
    mouvements = []
    for s in haut_payeur[:haut_payeur.index(ancetre)]:
        mouvements.append((COMPTES[s][0], -1.0))
    for s in reversed(haut_beneficiaire[:haut_beneficiaire.index(ancetre)]):
        mouvements.append((COMPTES[s][0], 1.0))
    return tuple(mouvements)


# --------------------------------------------------------------------------
# Termes et lignes
# --------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Terme:
    """Un terme simple d'une ligne de `tab:matrice-flux`.

    - `nom` : nom du terme dans un flux proposé (ASCII) ;
    - `ecriture` : écriture LaTeX de la spécification, comparée par le test ;
    - `colonne_plus` (reçoit) et `colonne_moins` (verse) ;
    - `variations` : postes d'instrument ou d'actif réel que le terme fait
      varier, avec leur coefficient par unité de montant ;
    - `reglement` : mouvements des moyens de paiement par unité de montant,
      dérivés de l'arbre des comptes (vide pour une contrepartie de règlement) ;
    - `poste_regle` : pour une contrepartie de règlement (17, 20, 22), le
      moyen de paiement dont la variation fait le montant ; `None` sinon.
    """

    nom: str
    ecriture: str
    colonne_plus: str
    colonne_moins: str
    variations: tuple[tuple[str, float], ...]
    reglement: tuple[tuple[str, float], ...]
    poste_regle: str | None


@dataclass(frozen=True, slots=True)
class Ligne:
    """Une ligne du catalogue.

    - `identifiant` : celui de la spécification (`"7"`, `"11a"`, `"19a-banque"`) ;
    - `phase` : clôture où elle s'exécute (`tab:phases`) ; `None` pour une
      contrepartie de règlement, appliquée dans chaque phase ;
    - `proposant` : radical du bloc proposant au socle ; `None` pour une
      contrepartie de règlement et pour les lignes 19b (aucun proposant au
      socle, ADR 0011) ;
    - `admet_negatif` : sens du montant que la ligne admet ; une ligne qui ne
      l'admet pas refuse un terme négatif (ADR 0012, A2 et A8) ;
    - `resultat` : ligne de résultat (1 à 16), qui entre dans V^flux ;
    - `contrepartie` : contrepartie de règlement (17, 20, 22) ;
    - `signature` : (ΔM, ΔH) par unité de montant, dérivée du règlement ;
      `None` pour les lignes « poste » (17, 20).
    """

    identifiant: str
    libelle: str
    termes: tuple[Terme, ...]
    phase: str | None
    proposant: str | None
    admet_negatif: bool
    resultat: bool
    contrepartie: bool
    signature: tuple[int, int] | None


def _terme(nom: str, ecriture: str, plus: str, moins: str,
           variations: tuple[tuple[str, float], ...] = ()) -> Terme:
    """Terme d'une ligne décidée : règlement dérivé de l'arbre des comptes."""
    reglement = chemin_de_reglement(SECTEUR_DE_COLONNE[moins], SECTEUR_DE_COLONNE[plus])
    return Terme(nom, ecriture, plus, moins, variations, reglement, None)


def _terme_de_reglement(nom: str, ecriture: str, poste: str) -> Terme:
    """Terme d'une contrepartie de règlement : variation d'un moyen de paiement.

    Variation d'un actif détenu −, d'un passif émis + (`tab:matrice-flux`) ;
    les dépôts des entreprises sont réglés dans leur sous-colonne capital.
    """
    p = POSTE[poste]
    moins = "entreprises_capital" if p.detenteur == "entreprises" else p.detenteur
    return Terme(nom, ecriture, p.emetteur, moins, (), (), poste)


def _signature(termes: tuple[Terme, ...], contrepartie: bool) -> tuple[int, int] | None:
    """Signature (ΔM, ΔH) d'une ligne, dérivée du règlement de ses termes.

    Une ligne porte une seule signature (§ 9.7, point 4) : des termes de
    signatures différentes sont une erreur du catalogue. Une contrepartie qui
    porte un poste de la monnaie ou de la monnaie centrale est une ligne
    « poste » (`None`) ; la ligne 22 ne fait varier ni M ni H.
    """
    if contrepartie:
        postes = {t.poste_regle for t in termes}
        if postes & set(POSTES_MONNAIE + POSTES_MONNAIE_CENTRALE):
            return None
        return (0, 0)
    signatures = set()
    for t in termes:
        d_m = sum(int(c) for p, c in t.reglement if p in POSTES_MONNAIE)
        d_h = sum(int(c) for p, c in t.reglement if p in POSTES_MONNAIE_CENTRALE)
        signatures.add((d_m, d_h))
    if len(signatures) != 1:
        raise ValueError(f"termes de signatures différentes : {sorted(signatures)}")
    return signatures.pop()


def _ligne(identifiant: str, libelle: str, termes: tuple[Terme, ...], phase: str | None,
           proposant: str | None, admet_negatif: bool, resultat: bool,
           contrepartie: bool = False) -> Ligne:
    return Ligne(identifiant, libelle, termes, phase, proposant, admet_negatif, resultat,
                 contrepartie, _signature(termes, contrepartie))


_M, _FC, _FK, _BK, _CB, _G = COLONNES

# Les 28 lignes, dans l'ordre de `tab:matrice-flux` ; c'est l'ordre canonique
# d'exécution (ADR 0012, A3.3). Proposants : sections « Lignes de flux » des
# blocs de la spécification. Lignes admettant un montant négatif, liste fermée
# (ADR 0012, annotation du 07/10/2026, point 1) : variation des stocks (4),
# impôts (7, par ligne : le terme de couverture des intérêts T^cou est de signe
# quelconque), intérêts sous un taux négatif (9 à 13 ; aucun plancher du taux
# directeur au socle), perte de la banque centrale (16), remboursement (18,
# 21), rachat net ou vente (19a, 19b) ; toutes les autres le refusent.
LIGNES = (
    _ligne("1", "Consommation", (_terme("C", r"C", _FC, _M),), "5", "menages", False, True),
    _ligne("2", "Dépense publique", (_terme("G", r"G", _FC, _G),), "5",
           "finances_publiques", False, True),
    _ligne("3", "Investissement", (_terme("I", r"I", _FC, _FK, (("K", 1.0),)),), "5",
           "investissement", False, True),
    _ligne("4", "Variation des stocks",
           (_terme("Delta_IN", r"\Delta \mathit{IN}", _FC, _FK, (("IN", 1.0),)),), "5",
           "production", True, True),
    _ligne("5", "Salaires", (_terme("WB", r"\mathit{WB}", _M, _FC),), "4", "travail",
           False, True),
    _ligne("6", "Transferts", (_terme("Tr", r"\mathit{Tr}", _M, _G),), "6",
           "finances_publiques", False, True),
    _ligne("7", "Impôts", (_terme("T_H", r"T_H", _G, _M), _terme("T_F", r"T_F", _G, _FC)), "6",
           "finances_publiques", True, True),
    _ligne("8", "Amortissement",
           (_terme("deltaK", r"\delta K/n_a", _FK, _FC, (("K", -1.0),)),), "6",
           "investissement", False, True),
    _ligne("9", "Intérêts sur crédits", (_terme("iL_L", r"i_L L/n_a", _BK, _FC),), "6",
           "banque", True, True),
    _ligne("10", "Intérêts sur dépôts",
           (_terme("iD_DH", r"i_D D_H/n_a", _M, _BK), _terme("iD_DF", r"i_D D_F/n_a", _FC, _BK)),
           "6", "banque", True, True),
    _ligne("11a", "Intérêts sur titres, ménages",
           (_terme("iB_BH", r"i_B B_H/n_a", _M, _G),), "6", "finances_publiques", True, True),
    _ligne("11b", "Intérêts sur titres, banque",
           (_terme("iB_BBk", r"i_B B_{\mathit{Bk}}/n_a", _BK, _G),), "6",
           "finances_publiques", True, True),
    _ligne("11c", "Intérêts sur titres, banque centrale",
           (_terme("iB_BCB", r"i_B B_{\mathit{CB}}/n_a", _CB, _G),), "6",
           "finances_publiques", True, True),
    _ligne("12", "Intérêts sur réserves",
           (_terme("ires_Res", r"i_{\mathit{res}} \mathit{Res}/n_a", _BK, _CB),), "8a",
           "banque_centrale", True, True),
    _ligne("13", "Intérêts sur refinancement",
           (_terme("iCB_LCB", r"i_{\mathit{CB}} L^{\mathit{CB}}/n_a", _CB, _BK),), "8a",
           "banque_centrale", True, True),
    _ligne("14", "Dividendes des entreprises", (_terme("Div_F", r"\mathit{Div}_F", _M, _FC),),
           "6", "investissement", False, True),
    _ligne("15", "Dividendes de la banque",
           (_terme("Div_Bk", r"\mathit{Div}_{\mathit{Bk}}", _M, _BK),), "6", "banque", False,
           True),
    _ligne("16", "Versement du résultat de la banque centrale",
           (_terme("Pi_CB", r"\Pi^{\mathit{CB}}", _G, _CB),), "8b", "banque_centrale", True,
           True),
    _ligne("17", "Δ Dépôts",
           (_terme_de_reglement("Delta_DH", r"\Delta D_H", "D_H"),
            _terme_de_reglement("Delta_DF", r"\Delta D_F", "D_F")),
           None, None, True, False, contrepartie=True),
    _ligne("18", "Δ Crédits", (_terme("Delta_L", r"\Delta L", _FK, _BK, (("L", 1.0),)),), "3",
           "investissement", True, False),
    _ligne("19a-ménages", "Émission primaire, ménages",
           (_terme("Delta_BH_prim", r"\Delta B_H^{\mathrm{prim}}", _G, _M, (("B_H", 1.0),)),),
           "7", "finances_publiques", True, False),
    _ligne("19a-banque", "Émission primaire, banque",
           (_terme("Delta_BBk_prim", r"\Delta B_{\mathit{Bk}}^{\mathrm{prim}}", _G, _BK,
                   (("B_Bk", 1.0),)),),
           "7", "finances_publiques", True, False),
    _ligne("19a-BC", "Émission primaire, banque centrale",
           (_terme("Delta_BCB_prim", r"\Delta B_{\mathit{CB}}^{\mathrm{prim}}", _G, _CB,
                   (("B_CB", 1.0),)),),
           "7", "finances_publiques", True, False),
    _ligne("19b-ménages", "Achats de la banque centrale aux ménages",
           (_terme("Delta_BH_sec", r"\Delta B_H^{\mathrm{sec}}", _M, _CB,
                   (("B_H", -1.0), ("B_CB", 1.0))),),
           "7", None, True, False),
    _ligne("19b-banque", "Achats de la banque centrale à la banque",
           (_terme("Delta_BBk_sec", r"\Delta B_{\mathit{Bk}}^{\mathrm{sec}}", _BK, _CB,
                   (("B_Bk", -1.0), ("B_CB", 1.0))),),
           "7", None, True, False),
    _ligne("20", "Δ Réserves", (_terme_de_reglement("Delta_Res", r"\Delta \mathit{Res}", "Res"),),
           None, None, True, False, contrepartie=True),
    _ligne("21", "Δ Refinancement",
           (_terme("Delta_LCB", r"\Delta L^{\mathit{CB}}", _BK, _CB, (("L_CB", 1.0),)),), "8c",
           "banque", True, False),
    _ligne("22", "Δ Compte du Trésor", (_terme_de_reglement("Delta_MG", r"\Delta M^G", "M_G"),),
           None, None, True, False, contrepartie=True),
)

LIGNE = {ligne.identifiant: ligne for ligne in LIGNES}
IDENTIFIANTS = tuple(ligne.identifiant for ligne in LIGNES)
CONTREPARTIES = tuple(ligne for ligne in LIGNES if ligne.contrepartie)
# Lignes décidées de chaque clôture, dans l'ordre canonique.
LIGNES_DE_LA_PHASE = {
    phase: tuple(ligne for ligne in LIGNES if ligne.phase == phase) for phase in PHASES
}
