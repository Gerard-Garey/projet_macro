"""Socle partiel d'essai : un bloc d'essai sur le sentier par radical (#112, point 3 ; P52).

Contrat : décision P52 du mainteneur (13/11/2026) ; ADR 0012, annotation du
13/11/2026, points 2 et 6 ; synthèse du rang 1a de J3-b (commentaire de la
PR #117), § 6, § 8 et § 9. Ce module vit dans `tests/` seulement : **rien dans
`src/` ne le connaît** (ni drapeau de mode, ni état caché, ni interface qui le
distingue, ADR 0002). Ses blocs implémentent le contrat de bloc sous les huit
radicaux réels et passent par `assembler` comme des blocs réels ; un bloc réel
(#113, #50, #51) se substitue au bloc d'essai de son radical (`blocs(...,
reels=...)`).

**Sentier.** Chaque bloc d'essai propose ses lignes et écrit ses variables aux
valeurs du sentier stationnaire, tirées de `outils/etat_stationnaire.py` : les
valeurs du pas 0 viennent de `un_pas(ouverture(e))` (flux, variables du pas,
valeurs du pas suivant des variables d'état) et l'état initial de
`ouverture(e)` ; la valeur du pas t est la valeur du pas 0 multipliée par
facteur^t, le facteur par pas étant celui de la grandeur sur le sentier :

- volume (u.v.) : (1 + g)^{1/n_a} ; productivité : (1 + g_pr)^{1/n_a} ;
- personnes : (1 + g_N)^{1/n_a} ;
- prix (u.m. par u.v.) : (1 + π̄)^{1/n_a} ; salaire par personne :
  ((1 + g_pr)(1 + π̄))^{1/n_a} ;
- montant nominal (u.m. par pas) : Γ̄ = ((1 + g)(1 + π̄))^{1/n_a} ;
- grandeur sans dimension (U, tu, ξ, μ̃, i_L, i_D, π^e, r̂*, π*, i_CB, θ_CB) : 1.

Les facteurs sont ceux du script (`facteurs`), non ceux du moteur : le bloc
d'essai ne lit pas `facteur_g`, qu'aucun bloc réel ne remplace.

**Exigences du rang 1a (§ 8).** Les blocs d'essai acheteurs (ménages,
investissement, État) écrivent leurs plans en u.m. sur le sentier (C^plan,
I^plan, G^plan, phase 2), exogènes et à chocs possibles (`chocs_des_plans`), et
proposent les lignes 1 à 3 **au prix p_t du pas sur les volumes servis par le
bloc 2** (`p` × `C_vol`, `I_vol`, `G_vol`, lus en phase 5), non aux montants
du sentier. Le bloc d'essai 8 a une variante à π^e choqué (`choc_pi_e`),
injecté dans l'état d'ouverture : π^e_0 dans l'état initial, π^e_{t+1} écrite
en phase 1. **Réserve de `monnaie`** : hors du sentier, le bloc d'essai à
π^e = π* coupe la boucle T3 ↔ BC3 ; toute mesure dynamique faite sur ce socle
avec le bloc d'essai 8 et sans les options d'E3 porte l'étiquette `ETIQUETTE` et ne
vaut pas verdict de boucle conjointe ; une mesure où le bloc 8 est réel ou E3
active porte l'étiquette de son banc (réserve mineure de `monnaie`, rang 6).
Le bloc d'essai 8 écrit aussi la cible en vigueur π*_{t+1} = π*_t, **lue à
l'ouverture** (`vue.ouverture.pi_etoile`, lecture déclarée), par la règle
d'essai `REGLES_PAR_DEFAUT` (BC4 à levier fermé ; M30 ; ADR 0013, annotation du
14/11/2026, point 6 ; #61) : sur le sentier, elle reste à la valeur `pi_cible_1`
du script ; hors du sentier (π*_0 ≠ π̄), elle reste à π*_0.

**Variables du pas** : noms, écrivains, étapes et lecteurs de l'annotation du
13/11/2026, point 2.2, et de l'annotation du 14/11/2026 de l'ADR 0013, point 5
(bloc 8 : `i_regle`, `i_CB`, `theta_CB`, `Pi_CB`, écrits en phase 1 aux valeurs du
sentier par le bloc d'essai 8, par BC1, BC5 et BC6 par le bloc réel, #91).

**Bloc d'essai 9 (P95, rang 4 de J3-c)** : E1, il déclare le montant couvert de
la ligne 16 sur Π^CB **lu en phase 1** (`Pi_CB`, variable du pas du bloc 8), non
sur le sentier ; E2, il propose les lignes 11a à 11c selon E7, au taux du tour
`i_CB` lu en phase 1, converti au pas, sur les encours d'ouverture B_H, B_Bk et
B_CB. **E3 (P95, rang 6 de J3-c)**, pour les essais avec choc, par les options
de `emission_e3()` : il propose les trois lignes 19a selon E8 à E11
(`sec:finances_publiques-emission`) sur les lignes 2, 6, 7 et 11a à 11c
exécutées, Π^CB et θ_CB lus en phase 1 et M^G d'ouverture, ν_G et ς_B du
sentier ; sans ces options, l'émission reste aux montants du sentier (cas
d'essai de la linéarisation, où les positions ont des flux exogènes).

**Tables des blocs 7 et 8 (réserve R1 de `monnaie`, rang 4 de J3-c ; étendue
par décision du mainteneur à la revue finale de J3-c)** : `ordonnanceur` aligne
les tables de référence des blocs 7 et 8 sur les paramètres avec lesquels le
script a construit le sentier (`parametres_du_sentier` ; ϖ_L, ϖ_D, ϑ, a_π, a_I,
λ_e, θ_CB, π*, r̄), si bien que l'état initial (π*_0 = π̄ du script) égale la
table à chaque π* ; une table des blocs 7 ou 8 passée par l'appelant n'est
jamais écrasée : gardée si chacun de ces paramètres égale celui du sentier,
refusée sinon (`TableHorsDuSentier`). La banque propose la ligne 21 sous la forme exacte de
B7, −min(Res^{8b} ; L^CB), par la fonction du bloc 7 (`nations.blocs.banque.refinancement`),
sur les positions lues au grand livre (le noyau arrête sur une
poussière de réserves) ; l'État déclare le montant couvert de la ligne 16 si
elle est négative (jamais sur le sentier).

**Échelle nominale** : `echelle` multiplie chaque grandeur nominale du sentier
(montants, prix, salaire, positions, registre) ; l'invariance × 100 compare un
socle à `echelle = 100` à 100 fois le socle à `echelle = 1`.
"""

from __future__ import annotations

import importlib
import importlib.util
import math
import sys
import types
from collections.abc import Callable, Sequence
from dataclasses import dataclass, fields, replace
from fractions import Fraction
from pathlib import Path

from nations.blocs.banque import refinancement
from nations.etat import schema
from nations.etat.schema import EtatPays
from nations.moteur import ordonnanceur as ordo
from nations.moteur.contrat_bloc import (
    GRAND_LIVRE,
    OUVERTURE,
    DeclarationDeBloc,
    Lecture,
    Siege,
)
from nations.moteur.conversions import TauxDeFlux, par_pas
from nations.moteur.ordonnanceur import INDICE_DES_PRIX, DeclarationDesEntrees, EntreesDuTour
from nations.moteur.parametres import TauxDeCroissance, varier
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.moteur.phases import PHASES
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt

RACINE = Path(__file__).resolve().parents[2]
ETIQUETTE = "π^e exogène (bloc d'essai 8) ; émission aux montants du sentier (E3 inactive)"
GRAINE = 20261113
NU_G = 1.15  # ν_G retenu (décision du mainteneur du 05/10/2026, #84) ; synthèse du rang 1a, § 6
POINTS_PI = (0.0, 0.02, 0.10)
SANS_ENTREES = DeclarationDesEntrees((), ())
ENTREES_VIDES = EntreesDuTour((), ())


def script():
    """Module `outils/etat_stationnaire.py`, chargé par son chemin (`outils/` n'est pas un paquet)."""
    nom = "etat_stationnaire"
    if nom in sys.modules:
        return sys.modules[nom]
    spec = importlib.util.spec_from_file_location(nom, RACINE / "outils" / "etat_stationnaire.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[nom] = module
    spec.loader.exec_module(module)
    return module


# --------------------------------------------------------------------------
# Sentier stationnaire du script
# --------------------------------------------------------------------------

# Classes de grandeurs et leur facteur par pas sur le sentier.
VOLUME, PRODUCTIVITE, PERSONNES, PRIX, SALAIRE, NOMINAL, CONSTANTE = (
    "volume", "productivite", "personnes", "prix", "salaire", "nominal", "constante")
NOMINALES = frozenset({PRIX, SALAIRE, NOMINAL})


@dataclass(frozen=True)
class Sentier:
    """Sentier stationnaire du script à π̄ = π* : paramètres, état résolu `e`, ouverture `o`,
    pas 0 `s` et facteurs par pas, par classe de grandeur."""

    pi: float
    par: object
    e: dict
    o: dict
    s: dict
    facteurs: dict

    def valeur(self, cle: str, classe: str, t: int, echelle: float = 1.0) -> float:
        """Valeur du pas t d'une grandeur du pas 0 `s[cle]`, de classe `classe`."""
        base = self.s[cle] * (echelle if classe in NOMINALES else 1.0)
        return base * self.facteurs[classe] ** t


def sentier(pi: float, **variations: float) -> Sentier:
    """Sentier du script à π̄ = π* = `pi`, ν_G = 1,15, autres paramètres par défaut (égaux aux
    tables du moteur, P63) ou variés par `variations` (noms de `Parametres` du script)."""
    es = script()
    par = replace(es.Parametres(), pi_cible=pi, nu_G=NU_G, **variations)
    es.controler_domaine(par)
    e = es.etat_stationnaire(par)
    o = es.ouverture(e, par)
    s = dict(es.un_pas(o, par))
    # Volumes servis (N6) : p_t × volume servi = montant des lignes 1 à 3.
    s["C_vol"], s["I_vol"], s["G_vol"] = s["C"] / s["p"], s["I"] / s["p"], s["G"] / s["p"]
    # Part de la banque centrale à l'émission (BC5), paramètre que `un_pas` ne publie pas.
    s["theta_CB"] = par.theta_CB
    n = par.n_a
    f = es.facteurs(par)
    facteurs = {
        VOLUME: f["Gr"], PRODUCTIVITE: (1 + par.g_pr) ** (1 / n),
        PERSONNES: (1 + par.g_N) ** (1 / n), PRIX: f["Pp"],
        SALAIRE: ((1 + par.g_pr) * (1 + pi)) ** (1 / n), NOMINAL: f["Gam"], CONSTANTE: 1.0,
    }
    return Sentier(pi, par, e, o, s, facteurs)


# Variables du pas des blocs d'essai : nom → (clé du pas 0 du script, classe), par
# (radical, étape) ; noms de l'annotation du 13/11/2026, point 2.2.
VARIABLES_DU_PAS = {
    ("production", "2"): {"y_etoile": ("y_star", VOLUME), "IN_vol_etoile": ("IN_star", VOLUME),
                          "N_etoile": ("N_star", PERSONNES), "UC": ("UC", PRIX)},
    ("production", "4"): {"y": ("y", VOLUME), "y_cap": ("y_cap", VOLUME),
                          "tu": ("tu", CONSTANTE)},
    ("production", "5"): {"v": ("v", VOLUME), "C_vol": ("C_vol", VOLUME),
                          "I_vol": ("I_vol", VOLUME), "G_vol": ("G_vol", VOLUME)},
    ("prix", "5"): {"p": ("p", PRIX), INDICE_DES_PRIX: ("p", PRIX), "xi": ("xi", CONSTANTE)},
    # Bloc 8 (ADR 0013, annotation du 14/11/2026, point 5) : i^règle = i_CB au socle.
    ("banque_centrale", "1"): {"i_regle": ("i_CB", CONSTANTE), "i_CB": ("i_CB", CONSTANTE),
                               "theta_CB": ("theta_CB", CONSTANTE), "Pi_CB": ("Pi_CB", NOMINAL)},
    # Bloc 7 (ADR 0013, annotation du 14/11/2026, point 5) : Π^Bk, écrit en phase 6 (B5).
    ("banque", "6"): {"Pi_Bk": ("Pi_Bk", NOMINAL)},
    ("menages", "2"): {"C_plan": ("C_plan", NOMINAL)},
    ("investissement", "2"): {"I_plan": ("I_plan", NOMINAL)},
    ("finances_publiques", "2"): {"G_plan": ("G_plan", NOMINAL)},
}

# Valeurs du pas suivant des variables d'état (C2) : nom → (clé du pas 0, classe).
VARIABLES_D_ETAT = {
    "v_e": ("ve_1", VOLUME), "IN_vol": ("IN_vol_1", VOLUME), "pr": ("pr_1", PRODUCTIVITE),
    "K_vol": ("K_vol_1", VOLUME), "W": ("W", SALAIRE), "U": ("U", CONSTANTE),
    "N": ("N", PERSONNES), "N_pa": ("N_pa_1", PERSONNES), "mu_tilde": ("mu_tilde", CONSTANTE),
    "i_L": ("i_L_1", CONSTANTE), "i_D": ("i_D_1", CONSTANTE), "pi_e": ("pi_e_1", CONSTANTE),
    "r_hat_etoile": ("r_hat_1", CONSTANTE), "pi_etoile": ("pi_cible_1", CONSTANTE),
}
if set(VARIABLES_D_ETAT) != {v.nom for v in schema.VARIABLES_DES_BLOCS}:
    raise AssertionError("socle partiel : une variable d'état du schéma sans valeur du sentier")

# Valeur à l'ouverture du pas 0 de chaque variable d'état (clé de `ouverture`).
OUVERTURE_DES_VARIABLES = {
    "v_e": "ve", "IN_vol": "IN_vol", "pr": "pr", "K_vol": "K_vol", "W": "W_m1", "U": "U_m1",
    "N": "N_m1", "N_pa": "N_pa", "mu_tilde": "mu_tilde_m1", "i_L": "i_L", "i_D": "i_D",
    "pi_e": "pi_e", "r_hat_etoile": "r_hat", "pi_etoile": "pi_cible",
}

# Lignes proposées aux montants du sentier : ligne → {terme: clé du pas 0}, classe nominale.
# Les lignes 1 à 3 (acheteurs, p × volume servi), 11a à 11c (E7, bloc d'essai 9, E2) et 21 (B7,
# forme exacte) n'y sont pas.
LIGNES_DU_SENTIER = {
    "4": {"Delta_IN": "dIN"}, "5": {"WB": "WB"}, "6": {"Tr": "Tr"},
    "7": {"T_H": "T_H", "T_F": "T_F"}, "8": {"deltaK": "amort"}, "9": {"iL_L": "l9"},
    "10": {"iD_DH": "l10_H", "iD_DF": "l10_F"}, "12": {"ires_Res": "l12"},
    "13": {"iCB_LCB": "l13"}, "14": {"Div_F": "Div_F"}, "15": {"Div_Bk": "Div_Bk"},
    "16": {"Pi_CB": "l16"}, "18": {"Delta_L": "dL"}, "19a-ménages": {"Delta_BH_prim": "dB_H"},
    "19a-banque": {"Delta_BBk_prim": "dB_Bk"}, "19a-BC": {"Delta_BCB_prim": "dB_CB"},
}

# Acheteurs : (radical, ligne, terme, volume servi lu, plan écrit en phase 2).
ACHETEURS = (("menages", "1", "C", "C_vol", "C_plan"),
             ("investissement", "3", "I", "I_vol", "I_plan"),
             ("finances_publiques", "2", "G", "G_vol", "G_plan"))

# Lignes 11a à 11c (E7), proposées par le bloc d'essai 9 (E2) : ligne → (terme, encours
# d'ouverture des titres).
INTERETS_SUR_TITRES = {"11a": ("iB_BH", "B_H"), "11b": ("iB_BBk", "B_Bk"),
                       "11c": ("iB_BCB", "B_CB")}


# --------------------------------------------------------------------------
# Déclarations des blocs d'essai
# --------------------------------------------------------------------------


def etapes_du(radical: str) -> tuple[str, ...]:
    """Étapes où `tab:phases` déclare le radical, dans l'ordre d'exécution."""
    return tuple(e.identifiant for phase in PHASES for e in phase.etapes
                 if any(radical in g for g in e.groupes))


def _lignes_proposees(radical: str, etape: str) -> tuple[str, ...]:
    if etape not in cat.LIGNES_DE_LA_PHASE:
        return ()
    return tuple(ligne.identifiant for ligne in cat.LIGNES_DE_LA_PHASE[etape]
                 if ligne.proposant == radical)


def _etat_de(radical: str, etape: str) -> tuple[str, ...]:
    return tuple(v.nom for v in schema.VARIABLES_DES_BLOCS
                 if v.proprietaire == radical and v.phase_ecriture == etape)


def _lectures(radical: str, etape: str) -> tuple[Lecture, ...]:
    lectures = [Lecture(OUVERTURE, "t")]
    for acheteur, _, _, volume, _ in ACHETEURS:
        if (radical, etape) == (acheteur, "5"):
            lectures += [Lecture("5", "p"), Lecture("5", volume)]
    if (radical, etape) == ("banque", "8c"):
        lectures += [Lecture(GRAND_LIVRE, "Res"), Lecture(GRAND_LIVRE, "L_CB")]
    if (radical, etape) == ("finances_publiques", "6"):
        # E2 : lignes 11a à 11c selon E7, au taux du tour sur les encours d'ouverture.
        lectures += [Lecture("1", "i_CB")] + [Lecture(OUVERTURE, encours) for _, encours
                                              in INTERETS_SUR_TITRES.values()]
    if (radical, etape) == ("finances_publiques", "8b"):
        # E1 : montant couvert de la ligne 16 sur Π^CB lu en phase 1.
        lectures += [Lecture(GRAND_LIVRE, "M_G"), Lecture("1", "Pi_CB")]
    if (radical, etape) == ("banque_centrale", "1"):
        lectures.append(Lecture(OUVERTURE, "pi_etoile"))
    return tuple(lectures)


def declaration_d_essai(radical: str) -> DeclarationDeBloc:
    """Déclaration du bloc d'essai d'un radical : un siège par étape de `tab:phases`."""
    sieges = []
    for etape in etapes_du(radical):
        sieges.append(Siege(
            etape, tuple(VARIABLES_DU_PAS.get((radical, etape), {})),
            _lectures(radical, etape), _lignes_proposees(radical, etape),
            ("16",) if (radical, etape) == ("finances_publiques", "8b") else (),
            _etat_de(radical, etape)))
    return DeclarationDeBloc(radical, tuple(sieges))


# --------------------------------------------------------------------------
# Blocs d'essai
# --------------------------------------------------------------------------


class _BlocDEssai:
    """Base des blocs d'essai : aucun attribut d'instance ; la déclaration et le réglage
    (sentier, échelle, chocs) sont des attributs de classe en lecture seule."""

    __slots__ = ()
    declaration: DeclarationDeBloc
    reglage: types.MappingProxyType

    def _agir(self, vue: ordo.Vue, etape: str) -> None:
        r = self.reglage
        sentier, echelle = r["sentier"], r["echelle"]
        radical = self.declaration.radical
        siege = r["sieges"][etape]
        t = vue.ouverture.t
        # Variables d'état : valeur du pas suivant sur le sentier ; π^e éventuellement choquée.
        # Une règle d'essai (`regles`) remplace la valeur du sentier d'une variable.
        for nom in siege.etat:
            cle, classe = VARIABLES_D_ETAT[nom]
            if nom in r["regles"]:
                valeur = r["regles"][nom](vue, sentier, t)
            else:
                valeur = sentier.valeur(cle, classe, t, echelle)
            if nom == "pi_e":
                valeur += r["choc_pi_e"](t + 1)
            vue.ecrire_etat(nom, valeur)
        # Variables du pas, dont les plans des acheteurs, éventuellement choqués.
        for nom, (cle, classe) in VARIABLES_DU_PAS.get((radical, etape), {}).items():
            valeur = sentier.valeur(cle, classe, t, echelle)
            if nom in ("C_plan", "I_plan", "G_plan"):
                valeur *= r["chocs_des_plans"](nom, t)
            vue.ecrire_pas(nom, valeur)
        # Lignes : acheteurs au prix du pas sur les volumes servis ; B7 sous forme exacte ;
        # les autres aux montants du sentier.
        # Une règle d'essai de ligne (`lignes`) prime sur toute autre forme : jamais ignorée.
        for ligne in siege.propose:
            acheteur = next((a for a in ACHETEURS if a[1] == ligne), None)
            if ligne in r["lignes"]:
                vue.proposer(ligne, r["lignes"][ligne](vue, sentier))
            elif acheteur is not None:
                _, _, terme, volume, _ = acheteur
                vue.proposer(ligne, {terme: vue.lire("p") * vue.lire(volume)})
            elif ligne in INTERETS_SUR_TITRES:
                terme, encours = INTERETS_SUR_TITRES[ligne]
                i_pas = par_pas(TauxDeFlux(vue.lire("i_CB")))
                vue.proposer(ligne, {terme: i_pas * getattr(vue.ouverture, encours)})
            elif ligne == "21":
                # B7 du bloc 7 (`refinancement`), L^CB lue au grand livre en 8 (c) : seule la
                # ligne 21 touche L^CB, sa position y égale donc l'ouverture que lit le bloc réel.
                livre = vue.grand_livre
                vue.proposer("21", {"Delta_LCB": refinancement(livre.position("Res"),
                                                               livre.position("L_CB"))})
            else:
                vue.proposer(ligne, {terme: sentier.valeur(cle, NOMINAL, t, echelle)
                                     for terme, cle in LIGNES_DU_SENTIER[ligne].items()})
        if siege.couvre:
            # E1 : Π^CB du pas, lu en phase 1 ; une perte est un résultat négatif.
            perte = vue.lire("Pi_CB")
            if perte < 0.0:
                vue.declarer_montant_couvert(
                    "16", min(-perte, max(0.0, vue.grand_livre.position("M_G"))))


def _choc_nul(t: int) -> float:
    return 0.0


def _plans_sans_choc(nom: str, t: int) -> float:
    return 1.0


def classe_d_essai(radical: str, sentier: Sentier, *, echelle: float = 1.0,
                   choc_pi_e: Callable[[int], float] = _choc_nul,
                   chocs_des_plans: Callable[[str, int], float] = _plans_sans_choc,
                   regles: dict | None = None, lignes: dict | None = None,
                   declaration: DeclarationDeBloc | None = None) -> type:
    """Classe du bloc d'essai d'un radical ; `declaration` remplace sa déclaration (essais de
    refus à l'assemblage) ; `regles` donne, pour une variable d'état du radical, une règle
    d'essai (vue, sentier, t) → valeur du pas suivant, à la place du sentier (cas d'essai de
    la linéarisation) ; `lignes` donne, pour une ligne proposée par le radical, une règle
    d'essai (vue, sentier) → montants par terme, à la place du sentier (E3)."""
    declaration = declaration_d_essai(radical) if declaration is None else declaration
    proposees = {ligne for s in declaration.sieges for ligne in s.propose}
    orphelines = sorted(set(lignes or {}) - proposees)
    if orphelines:
        raise OptionSansBlocDEssai(
            f"bloc d'essai {radical} : règle d'essai pour les lignes {orphelines}, qu'aucun de "
            "ses sièges ne propose : refusée, jamais ignorée en silence")
    reglage = types.MappingProxyType({
        "sentier": sentier, "echelle": echelle, "choc_pi_e": choc_pi_e,
        "chocs_des_plans": chocs_des_plans, "regles": types.MappingProxyType(regles or {}),
        "lignes": types.MappingProxyType(lignes or {}),
        "sieges": types.MappingProxyType({s.etape: s for s in declaration.sieges})})
    espace = {"__slots__": (), "declaration": declaration, "reglage": reglage}
    for siege in declaration.sieges:
        espace[f"phase_{siege.etape}"] = (
            lambda etape: lambda self, vue: self._agir(vue, etape))(siege.etape)
    nom = "".join(m.capitalize() for m in radical.split("_")) + "DEssai"
    return type(nom, (_BlocDEssai,), espace)


RADICAUX = ("production", "travail", "prix", "menages", "investissement", "banque",
            "banque_centrale", "finances_publiques")


def _cible_reconduite(vue: ordo.Vue, sentier: Sentier, t: int) -> float:
    """BC4 à levier fermé : π*_{t+1} = π*_t, lue à l'ouverture du pas."""
    return vue.ouverture.pi_etoile


# Règles d'essai appliquées sauf remplacement par `regles` : la cible en vigueur est reconduite
# depuis l'ouverture, non tirée du sentier (constat M1 de l'audit du rang 3 de J3-c : la valeur
# du sentier rendait le critère π*_{t+1} = π*_t infalsifiable).
REGLES_PAR_DEFAUT = types.MappingProxyType({"pi_etoile": _cible_reconduite})


class OptionSansBlocDEssai(ValueError):
    """Refus explicite (constat m3 de l'audit du rang 6 de J3-c) : une règle d'essai de ligne
    (`lignes`) ou une déclaration (`declarations`) vise un radical que `reels` remplace par un
    bloc réel, ou une ligne qu'aucun siège du bloc d'essai ne propose ; elle serait sinon
    ignorée en silence."""


def blocs(sentier: Sentier, *, echelle: float = 1.0,
          choc_pi_e: Callable[[int], float] = _choc_nul,
          chocs_des_plans: Callable[[str, int], float] = _plans_sans_choc,
          regles: dict | None = None, lignes: dict | None = None,
          reels: Sequence[object] = (),
          declarations: dict | None = None) -> tuple[object, ...]:
    """Les huit blocs : un bloc d'essai par radical, sauf ceux que `reels` fournit (un bloc
    réel par radical, #113, #50, #51) ; `declarations` remplace la déclaration d'un radical ;
    `regles` : variable d'état → règle d'essai, passée au bloc de son propriétaire, ajoutée à
    `REGLES_PAR_DEFAUT` (et prioritaire sur elles) ; `lignes` : ligne → règle d'essai, passée
    au bloc d'essai de son proposant (E3). Une clé de `lignes` ou de `declarations` dont le
    radical est remplacé par un bloc réel, ou une ligne qu'aucun siège ne propose, est refusée
    (`OptionSansBlocDEssai`)."""
    remplaces = {b.declaration.radical: b for b in reels}
    for radical in declarations or {}:
        if radical not in RADICAUX or radical in remplaces:
            raise OptionSansBlocDEssai(
                f"déclaration d'essai pour le radical {radical!r}, "
                + ("remplacé par un bloc réel" if radical in remplaces else "inconnu")
                + " : refusée, jamais ignorée en silence")
    for ligne in lignes or {}:
        if ligne not in cat.LIGNE:
            raise OptionSansBlocDEssai(f"règle d'essai pour la ligne {ligne!r}, absente du "
                                       "catalogue : refusée")
        if cat.LIGNE[ligne].proposant in remplaces:
            raise OptionSansBlocDEssai(
                f"règle d'essai pour la ligne {ligne}, proposée par "
                f"{cat.LIGNE[ligne].proposant}, remplacé par un bloc réel : refusée, jamais "
                "ignorée en silence")
    regles = {**REGLES_PAR_DEFAUT, **(regles or {})}
    rendus = []
    for radical in RADICAUX:
        if radical in remplaces:
            rendus.append(remplaces[radical])
            continue
        propres = {nom: regle for nom, regle in regles.items()
                   if schema.VARIABLE[nom].proprietaire == radical}
        siennes = {ligne: regle for ligne, regle in (lignes or {}).items()
                   if cat.LIGNE[ligne].proposant == radical}
        classe = classe_d_essai(radical, sentier, echelle=echelle, choc_pi_e=choc_pi_e,
                                chocs_des_plans=chocs_des_plans, regles=propres,
                                lignes=siennes, declaration=(declarations or {}).get(radical))
        rendus.append(classe())
    return tuple(rendus)


def blocs_reels() -> tuple[object, ...]:
    """Les blocs réels de `src/nations/blocs/`, dans l'ordre des radicaux : un module par
    radical, dont l'unique classe déclarée sous ce radical est instanciée (ADR 0012, annotation
    du 13/11/2026, point 5 : chaque module porte un seul bloc, dont le radical est le nom du
    module). Au rang 6 de J3-c : la production (#113), le travail (#50), les prix (#51), la
    banque (#90) et la banque centrale (#91)."""
    dossier = RACINE / "src" / "nations" / "blocs"
    rendus = []
    for radical in RADICAUX:
        if not (dossier / f"{radical}.py").exists():
            continue
        module = importlib.import_module(f"nations.blocs.{radical}")
        classes = [c for c in vars(module).values() if isinstance(c, type)
                   and type(getattr(c, "declaration", None)) is DeclarationDeBloc
                   and c.declaration.radical == radical and c.__module__ == module.__name__]
        if len(classes) != 1:
            raise AssertionError(f"nations.blocs.{radical} : un seul bloc attendu, "
                                 f"{len(classes)} trouvés")
        rendus.append(classes[0]())
    return tuple(rendus)


# Paramètres des tables des blocs 7 et 8 que lit le script pour construire le sentier : radical
# → {champ de la table: nom dans `Parametres` du script} (le script nomme `pi_cible` et `rbar` ce
# que la table du bloc 8 nomme `pi_etoile` et `r_bar`).
PARAMETRES_DES_TABLES_DU_SENTIER = types.MappingProxyType({
    "banque": types.MappingProxyType({"varpi_L": "varpi_L", "varpi_D": "varpi_D",
                                      "vartheta": "vartheta"}),
    "banque_centrale": types.MappingProxyType({"a_pi": "a_pi", "a_I": "a_I",
                                               "lambda_e": "lambda_e", "theta_CB": "theta_CB",
                                               "pi_etoile": "pi_cible", "r_bar": "rbar"}),
})
if any(set(noms) != {f.name for f in fields(getattr(PARAMETRES_DE_REFERENCE, radical))}
       for radical, noms in PARAMETRES_DES_TABLES_DU_SENTIER.items()):
    raise AssertionError("socle partiel : un paramètre des blocs 7 ou 8 sans valeur du sentier")


class TableHorsDuSentier(ValueError):
    """Refus explicite (réserve R1 de `monnaie`, étendue par décision du mainteneur à la revue
    finale de J3-c) : une table du bloc 7 ou du bloc 8 passée par l'appelant porte un paramètre
    (ϖ_L, ϖ_D, ϑ ; a_π, a_I, λ_e, θ_CB, π*, r̄) différent de la valeur avec laquelle le script a
    construit le sentier."""


def _valeur_de_champ(valeur) -> float:
    """Valeur brute d'un champ de table : un taux typé rend sa valeur, un `float` lui-même."""
    return valeur.valeur if isinstance(valeur, (TauxDeFlux, TauxDeCroissance)) else valeur


def parametres_du_sentier(sentier: Sentier, parametres=PARAMETRES_DE_REFERENCE):
    """Réserve R1 de `monnaie`, étendue aux tables des blocs 7 et 8 : les tables `parametres`,
    dont celles des blocs 7 et 8 portent les valeurs avec lesquelles le script a construit le
    sentier (`sentier.par`, `PARAMETRES_DES_TABLES_DU_SENTIER`) ; π* du sentier est la valeur
    initiale de l'état π*_0. Table par table : une table de référence (inchangée) est alignée
    sur le sentier (`varier`, paramètres du script) ; une table de l'appelant est gardée telle
    quelle, et refusée (`TableHorsDuSentier`) si un de ses paramètres diffère de celui du
    sentier : jamais écrasée en silence. Sans écart, `parametres` est rendu tel quel."""
    alignees = {}
    for radical, noms in PARAMETRES_DES_TABLES_DU_SENTIER.items():
        table = getattr(parametres, radical)
        du_sentier = {champ: getattr(sentier.par, nom) for champ, nom in noms.items()}
        if table == getattr(PARAMETRES_DE_REFERENCE, radical):
            alignee = varier(table, **du_sentier)
            if alignee != table:
                alignees[radical] = alignee
            continue
        ecarts = {champ: (_valeur_de_champ(getattr(table, champ)), valeur)
                  for champ, valeur in du_sentier.items()
                  if _valeur_de_champ(getattr(table, champ)) != valeur}
        if ecarts:
            raise TableHorsDuSentier(
                f"table du bloc {radical} de l'appelant hors du sentier, (table, sentier) : "
                + " ; ".join(f"{champ} = {a!r}, {b!r}" for champ, (a, b) in ecarts.items())
                + " : refusée (R1), jamais alignée en silence")
    return replace(parametres, **alignees) if alignees else parametres


def ordonnanceur(sentier: Sentier, parametres=PARAMETRES_DE_REFERENCE, **options):
    """Ordonnanceur du socle partiel d'essai, aux tables de référence par défaut, les tables des
    blocs 7 et 8 alignées sur le sentier ou refusées (R1, `parametres_du_sentier`)."""
    return ordo.assembler(PHASES, blocs(sentier, **options),
                          parametres_du_sentier(sentier, parametres), SANS_ENTREES)


# --------------------------------------------------------------------------
# État initial résolu et déroulement
# --------------------------------------------------------------------------


def etat_initial(sentier: Sentier, *, echelle: float = 1.0, graine: int = GRAINE,
                 choc_pi_e0: float = 0.0, identifiant: str = "A") -> EtatPays:
    """État d'ouverture du pas 0 tiré de `ouverture` du script : positions, V^flux = V^stock,
    registre P_{−u} = P_0 (1 + π̄)^{−u/n_a}, variables d'état des blocs ; nominaux × `echelle`."""
    o = sentier.o
    positions = {nom: float(o[nom]) * echelle for nom in cat.NOMS_POSTES}
    v_flux = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(positions, s)
              for s in cat.SECTEURS}
    variables = {}
    for v in schema.VARIABLES_DES_BLOCS:
        valeur = float(o[OUVERTURE_DES_VARIABLES[v.nom]])
        if v.invariance is schema.Invariance.NOMINAL:
            valeur *= echelle
        variables[v.nom] = valeur
    variables["pi_e"] += choc_pi_e0
    registre = tuple(float(x) * echelle for x in o["registre"])
    return EtatPays(identifiant=identifiant, graine=graine, t=0, registre_prix=registre,
                    **positions, **v_flux, **variables)


def derouler(etat: EtatPays, nb_pas: int, o, observateur) -> EtatPays:
    """Déroule `nb_pas` pas depuis `etat`, sans entrée de tour."""
    for _ in range(nb_pas):
        etat = ordo.executer_pas(etat, ENTREES_VIDES, o, observateur)
    return etat


def valeur_d_ouverture(sentier: Sentier, nom: str, t: int, echelle: float = 1.0) -> float:
    """Valeur sur le sentier d'une variable d'état à l'ouverture du pas t : sa valeur à
    l'ouverture du pas 0 multipliée par facteur^t."""
    classe = VARIABLES_D_ETAT[nom][1]
    base = float(sentier.o[OUVERTURE_DES_VARIABLES[nom]])
    if classe in NOMINALES:
        base *= echelle
    return base * sentier.facteurs[classe] ** t


def position_d_ouverture(sentier: Sentier, poste: str, t: int, echelle: float = 1.0) -> float:
    """Position sur le sentier à l'ouverture du pas t : position d'ouverture × Γ̄^t."""
    return float(sentier.o[poste]) * echelle * sentier.facteurs[NOMINAL] ** t


# --------------------------------------------------------------------------
# Stationnarité partielle (P66, P67) : grandeurs de `tab:criteres-j3`
# --------------------------------------------------------------------------

PAS_PAR_AN = PARAMETRES_DE_REFERENCE.cadre.pas_par_an
# Premier pas jugé des grandeurs sur 12 tours (D13).
PREMIER_PAS_SUR_12_TOURS = PAS_PAR_AN - 1
# Grandeurs sur une fenêtre de 12 tours, jugées dès le pas 11 (P67, D13).
SUR_12_TOURS = ("B4", "B5", "B6", "B7", "B13", "B24")


def grandeurs_b(pas: list, initial: EtatPays, sentier: Sentier) -> dict:
    """B1 à B7, B12, B13, B24 et ξ relevées sur une trajectoire du moteur, définitions de
    `tab:criteres-j3` : (t, valeur) par grandeur ; fenêtres de 12 tours dès le pas 11. `pas` :
    par pas, montants exécutés des lignes 1 à 5 (clés "1" à "5"), variables du pas
    (`variables`) et état t + 1 (`etat`)."""
    n_a = PAS_PAR_AN
    ouvertures = [initial] + [p["etat"] for p in pas[:-1]]
    g = {cle: [] for cle in ("B1", "B2", "B3", "B4", "B5", "B6", "B7", "B12", "B13", "B24",
                              "xi")}
    for t, p in enumerate(pas):
        v, o = p["variables"], ouvertures[t]
        pib = p["1"] + p["2"] + p["3"] + p["4"]
        g["B1"].append((t, o.IN_vol / v["v"]))
        g["B2"].append((t, v["y"] / v["y_cap"]))
        g["B3"].append((t, v["U_suivant"]))
        g["B12"].append((t, v["p"] * o.K_vol / (n_a * pib)))
        g["xi"].append((t, v["xi"]))
        if t < PREMIER_PAS_SUR_12_TOURS:
            continue
        fenetre = pas[t - n_a + 1:t + 1]
        g["B4"].append((t, sum(q["5"] for q in fenetre)
                        / sum(q["1"] + q["2"] + q["3"] + q["4"] for q in fenetre)))
        if t - n_a >= 0:
            w0, p0, y0 = (pas[t - n_a]["variables"][n] for n in ("W_suivant", "p", "y"))
        else:  # t − 12 = −1 : salaire, prix et production d'ouverture du pas 0
            w0, p0, y0 = initial.W, initial.registre_prix[0], float(sentier.o["y_m1"])
        g["B5"].append((t, (v["W_suivant"] / v["p"]) / (w0 / p0) - 1.0))
        g["B6"].append((t, sum(q["variables"]["p"] / q["variables"]["UC"] - 1.0
                               for q in fenetre) / n_a))
        g["B7"].append((t, v["P"] / o.registre_prix[n_a - 1] - 1.0))
        g["B13"].append((t, sum(q["3"] for q in fenetre)
                         / sum(q["1"] + q["2"] + q["3"] + q["4"] for q in fenetre)))
        g["B24"].append((t, v["y"] / y0 - 1.0))
    return g


def valeurs_resolues(sentier: Sentier) -> dict:
    """Valeurs résolues du script (`valeurs`, état `e`, paramètres), même définition."""
    e, par = sentier.e, sentier.par
    v = script().valeurs(e, par)
    return {"B1": v["IN_sur_v"], "B2": v["tu"], "B3": v["U"], "B4": v["part_salariale"],
            "B5": par.g_pr, "B6": e["p"] / e["UC"] - 1.0, "B7": v["glissement"] / 100.0,
            "B12": v["K_courant"], "B13": v["I_sur_PIB"] / 100.0, "B24": e["g"], "xi": 0.0}


# --------------------------------------------------------------------------
# Règle d'essai du bloc prix : prix exogène sur le sentier, μ̃_t = ln(p_t/UC_t)
# --------------------------------------------------------------------------


def prix_exogene_marge_identite(echelle: float = 1.0) -> dict:
    """Options de `blocs` : le bloc d'essai des prix garde p_t sur le sentier et écrit
    μ̃_t = ln(p_t/UC_t), UC_t étant celui du bloc 2 réel (lu en phase 2), déclaration d'essai
    complétée de cette lecture. C'est l'identité de P54 (« un prix administré écrit
    μ̃_t = ln(p_t/UC_t) », synthèse du rang 1a, § 4) : sous un prix exogène, ω_{t−1} =
    exp(−μ̃_{t−1}) lu par le bloc 3 vaut UC_{t−1}/p_{t−1}, et la boucle de correction du
    salaire n'est pas coupée par le bloc d'essai (sans elle, μ̃ resterait à ln(1 + μ̄) et le
    salaire nominal aurait une racine unitaire, propriété du socle, non du bloc 3)."""
    propre = declaration_d_essai("prix")
    sieges = tuple(replace(s, lit=s.lit + (Lecture("2", "UC"),)) if s.etape == "5" else s
                   for s in propre.sieges)

    def marge(vue, sentier, t):
        return math.log(sentier.valeur("p", PRIX, t, echelle) / vue.lire("UC"))

    return {"declarations": {"prix": replace(propre, sieges=sieges)},
            "regles": {"mu_tilde": marge}}


# --------------------------------------------------------------------------
# Bloc d'essai 9, E3 (P95, rang 6 de J3-c) : émission selon E8 à E11
# --------------------------------------------------------------------------

# Lignes exécutées que lit E3 (`sec:finances_publiques-emission`, « variables ») : dépense (2),
# transferts (6), impôts (7, T_H + T_F) et intérêts sur titres (11a à 11c, E7).
LIGNES_LUES_PAR_E3 = ("2", "6", "7", "11a", "11b", "11c")


def besoin_d_emission(vue: ordo.Vue, sentier: Sentier) -> tuple[float, float]:
    """E8 et E9 sur les montants exécutés des phases 5 et 6, Π^CB lu en phase 1 et M^G
    d'ouverture : PB_t = G_t + Tr_t + Σ lignes 11a à 11c (i_CB B_t/n_a, E7) ; M^G*_t = ν_G PB_t ;
    Em_t = PB_t − (T_H + T_F) − Π^CB_t + M^G*_t − M^G_t. Rend (Em_t, M^G*_t), u.m. par pas et
    u.m. ; ν_G du sentier (1,15, `NU_G`). Appelé par les règles 19a-BC et 19a-banque, une fois
    chacune par pas, sur les mêmes lectures : un calcul unique demanderait un état caché dans le
    bloc d'essai ; le même Em_t des deux appels est vérifié au bit
    (`test_e3_un_meme_em_par_pas_pour_19a_bc_et_19a_banque`)."""
    livre = vue.grand_livre
    interets = sum(livre.montant_execute_ligne(ligne) for ligne in ("11a", "11b", "11c"))
    paiements_bruts = (livre.montant_execute_ligne("2") + livre.montant_execute_ligne("6")
                       + interets)
    encaisse_visee = sentier.par.nu_G * paiements_bruts
    besoin = (paiements_bruts - livre.montant_execute_ligne("7") - vue.lire("Pi_CB")
              + encaisse_visee - vue.ouverture.M_G)
    return besoin, encaisse_visee


def _souscription_banque_centrale(vue: ordo.Vue, sentier: Sentier) -> dict:
    """E10 : ligne 19a-BC = θ_CB,t Em_t, θ_CB,t lu en phase 1 (BC5)."""
    besoin, _ = besoin_d_emission(vue, sentier)
    return {"Delta_BCB_prim": vue.lire("theta_CB") * besoin}


def _souscription_menages(vue: ordo.Vue, sentier: Sentier) -> dict:
    """E10 : ligne 19a-ménages à montant nul (M27)."""
    return {"Delta_BH_prim": 0.0}


def _souscription_banque(vue: ordo.Vue, sentier: Sentier) -> dict:
    """E11 : ligne 19a-banque = (1 − ς_B)(Em_t − θ_CB,t Em_t), reliquat déclaré (C19), ς_B du
    sentier (0 au socle)."""
    besoin, _ = besoin_d_emission(vue, sentier)
    part_cb = vue.lire("theta_CB") * besoin
    return {"Delta_BBk_prim": (1.0 - sentier.par.varsigma_B) * (besoin - part_cb)}


def emission_e3() -> dict:
    """Options de `blocs` : le bloc d'essai 9 propose les lignes 19a selon E8 à E11 (E3, P95),
    déclaration d'essai complétée des lectures de E3 en phase 7 (lignes exécutées
    `LIGNES_LUES_PAR_E3`, Π^CB et θ_CB de la phase 1, M^G d'ouverture). Après le versement de
    Π^CB en 8 (b), le compte du Trésor vaut M^G*_t (`sec:finances_publiques-emission`) : sous
    un choc, l'émission absorbe l'écart des paiements, que les montants du sentier laissaient
    au compte du Trésor. Mesure du rang 6 (blocs 2, 3, 4, 7 et 8 réels, 720 pas) : l'arrêt
    du compte du Trésor en phase 5 hors du sentier (marche de cible π*_0 = 1 %, pas 72 ; cas
    E2, pas 16) disparaît sous E3, mais les dépôts des entreprises s'épuisent plus tard en
    phase 4 (pas 186 et 295) : plans nominaux exogènes des blocs d'essai 5 et 6."""
    propre = declaration_d_essai("finances_publiques")
    lectures = (tuple(Lecture(GRAND_LIVRE, ligne) for ligne in LIGNES_LUES_PAR_E3)
                + (Lecture("1", "Pi_CB"), Lecture("1", "theta_CB"), Lecture(OUVERTURE, "M_G")))
    sieges = tuple(replace(s, lit=s.lit + lectures) if s.etape == "7" else s
                   for s in propre.sieges)
    return {"declarations": {"finances_publiques": replace(propre, sieges=sieges)},
            "lignes": {"19a-BC": _souscription_banque_centrale,
                       "19a-ménages": _souscription_menages,
                       "19a-banque": _souscription_banque}}


# --------------------------------------------------------------------------
# Stationnarité partielle étendue (P94, rang 6 de J3-c) : grandeurs des blocs 7 et 8
# --------------------------------------------------------------------------

# Grandeurs nulles de B19 (ligne B19 de `tab:criteres-j3`), jugées en u.m. rapportées à S^CB :
# réserves (Res ; H, monnaie centrale, égale à Res au socle, sans billets), fonds propres (par
# les flux, V^flux) et titres de la banque centrale, et résidu de l'identité L^CB + B_CB = Res +
# M^G + E^CB.
NULLES_DE_B19 = ("B19 Res (H)", "B19 E^CB", "B19 B_CB", "B19 identité")


def grandeurs_p94(pas: list, initial: EtatPays, sentier: Sentier) -> dict:
    """Grandeurs ajoutées par P94 à la stationnarité partielle, définitions de
    `tab:criteres-j3` : (t, valeur) par grandeur. `pas` : par pas, montants exécutés des lignes
    1 à 4 et 15 (clés "1" à "4", "15"), variables du pas (`variables`) et état t + 1 (`etat`).

    - B8, π^e − π* (point, pas) : état t + 1 ;
    - B9, r = i_CB − π, π de B7 (P_t/P_{t−12} − 1), dès le pas 11 (D13) ;
    - B16, B19 (M^G), B20 : stock d'ouverture du pas t rapporté à n_a × PIB du pas (lignes 1 à
      4), convention de B12 ; B17, E^Bk/L à l'ouverture (`valeur_nette_stock`) ;
    - B18 (i) : i_{L,t+1} − i_CB,t = ϖ_L et i_CB,t − i_{D,t+1} = ϖ_D (i_L, i_D de l'état t + 1,
      écrits en 8 (c) sur i_CB du tour) ;
    - B19, grandeurs nulles (`NULLES_DE_B19`), rapportées à S^CB de l'état t + 1, E^CB par les
      flux (V^flux de la banque centrale) ;
    - B25, r̂* − r̄, état t + 1 ; B26, i_CB − i^règle ;
    - D, part distribuée du résultat de la banque Div_Bk/Π^Bk (ligne 15 exécutée sur Π^Bk
      écrit en 6, P77) ;
    - états i_L, i_D, r̂*, π^e, π* de l'état t + 1 (comparés au sentier par
      `valeur_d_ouverture`, hors de ce relevé)."""
    n_a = PAS_PAR_AN
    ouvertures = [initial] + [p["etat"] for p in pas[:-1]]
    r_bar = sentier.par.rbar
    g = {cle: [] for cle in ("B8", "B9", "B16", "B17", "B18 (i) ϖ_L", "B18 (i) ϖ_D", "B19 M^G",
                              *NULLES_DE_B19, "B20", "B25", "B26", "D")}
    for t, p in enumerate(pas):
        v, o, e = p["variables"], ouvertures[t], p["etat"]
        pib_annuel = n_a * (p["1"] + p["2"] + p["3"] + p["4"])
        g["B8"].append((t, e.pi_e - e.pi_etoile))
        if t >= PREMIER_PAS_SUR_12_TOURS:
            g["B9"].append((t, v["i_CB"] - (v["P"] / o.registre_prix[n_a - 1] - 1.0)))
        g["B16"].append((t, (o.D_H + o.D_F) / pib_annuel))
        g["B17"].append((t, idt.valeur_nette_stock({q: getattr(o, q) for q in cat.NOMS_POSTES},
                                                   "banque") / o.L))
        g["B18 (i) ϖ_L"].append((t, e.i_L - v["i_CB"]))
        g["B18 (i) ϖ_D"].append((t, v["i_CB"] - e.i_D))
        g["B19 M^G"].append((t, o.M_G / pib_annuel))
        positions = {q: getattr(e, q) for q in cat.NOMS_POSTES}
        s_cb = idt.echelle_bilan(positions, "banque_centrale")
        # E^CB par les flux (V^flux, cumul des flux du noyau), non par le bilan : l'identité
        # n'est pas alors une tautologie de la valeur nette par le stock.
        e_cb = getattr(e, cat.VALEUR_NETTE_FLUX["banque_centrale"])
        g["B19 Res (H)"].append((t, e.Res / s_cb))
        g["B19 E^CB"].append((t, e_cb / s_cb))
        g["B19 B_CB"].append((t, e.B_CB / s_cb))
        g["B19 identité"].append((t, (e.L_CB + e.B_CB - e.Res - e.M_G - e_cb) / s_cb))
        g["B20"].append((t, o.B_Bk / pib_annuel))
        g["B25"].append((t, e.r_hat_etoile - r_bar))
        g["B26"].append((t, v["i_CB"] - v["i_regle"]))
        g["D"].append((t, p["15"] / v["Pi_Bk"]))
    return g


def valeurs_resolues_p94(sentier: Sentier) -> dict:
    """Valeurs résolues du script (état `e`, paramètres) des grandeurs de `grandeurs_p94`,
    jamais recopiées : grandeurs nulles à 0 (B8, B25, B26, grandeurs nulles de B19)."""
    e, par = sentier.e, sentier.par
    annuel = par.n_a * e["PIB"]
    return {"B8": 0.0, "B9": e["i_CB"] - sentier.pi, "B16": (e["D_H"] + e["D_F"]) / annuel,
            "B17": e["E_Bk"] / e["L"], "B18 (i) ϖ_L": par.varpi_L, "B18 (i) ϖ_D": par.varpi_D,
            "B19 M^G": e["M_G"] / annuel, **dict.fromkeys(NULLES_DE_B19, 0.0),
            "B20": e["B_Bk"] / annuel, "B25": 0.0, "B26": 0.0, "D": e["Div_Bk"] / e["Pi_Bk"]}


# --------------------------------------------------------------------------
# Grandeurs nulles de P94 en arithmétique exacte (décision D1 du mainteneur du 14/11/2026)
# --------------------------------------------------------------------------


def _exact(x) -> Fraction:
    """Valeur exacte d'un flottant de table (`Fraction` du double, sans arrondi décimal)."""
    return Fraction(getattr(x, "valeur", x))


def _taux_de_depot_exact(t) -> Fraction:
    """i_D = i_CB − ϖ_D, i_CB = (1 + r̄)(1 + π*) − 1 (BC1 au point fixe, B2), en exact."""
    bc = t.banque_centrale
    return ((1 + _exact(bc.r_bar)) * (1 + _exact(bc.pi_etoile)) - 1
            - _exact(t.banque.varpi_D))


# Liste déclarée des grandeurs de P94 nulles en arithmétique exacte : clé de `grandeurs_b`,
# `grandeurs_p94` ou état de P94 → (raison, valeur exacte sur les tables `t`). Une grandeur y
# est jugée nulle (|x_t| ≤ 1e−12) si et seulement si sa valeur exacte est nulle aux tables de
# l'essai ; toute autre grandeur est jugée en relatif (1e−9). Le classement ne lit jamais la
# valeur flottante du script (D1 : i_D à π* = 0 vaut 8,7e−18 au script, 0 en exact).
GRANDEURS_NULLES = types.MappingProxyType({
    "B7": ("glissement sur 12 tours = π* sur le sentier ; nul à π* = 0",
           lambda t: _exact(t.banque_centrale.pi_etoile)),
    "B8": ("π^e = π* sur le sentier (point fixe de BC3, π^e_0 = π̄ = π*)",
           lambda t: Fraction(0)),
    "B25": ("r̂* = r̄ sur le sentier (BC2 au point fixe, π_{t−1} = π*)",
            lambda t: Fraction(0)),
    "B26": ("i_CB = i^règle (BC1, aucun écart de prescription)", lambda t: Fraction(0)),
    "xi": ("ξ = 0 à l'état stationnaire (bloc 4)", lambda t: Fraction(0)),
    "B19 Res (H)": (("Res = 0 : banque en refinancement net, L^CB > 0, B7 en −min ; H = Res, "
                     "sans billets"), lambda t: Fraction(0)),
    "B19 E^CB": ("fonds propres de la banque centrale nuls : Π^CB versé en entier (ligne 16)",
                 lambda t: Fraction(0)),
    "B19 B_CB": ("B_CB = θ_CB B (BC5, E10), sans achat (ligne 19b, J6) ; nul sous θ_CB = 0",
                 lambda t: _exact(t.banque_centrale.theta_CB)),
    "B19 identité": ("résidu de l'identité L^CB + B_CB = Res + M^G + E^CB",
                     lambda t: Fraction(0)),
    "pi_e": ("π^e = π* sur le sentier ; nulle à π* = 0",
             lambda t: _exact(t.banque_centrale.pi_etoile)),
    "pi_etoile": ("cible en vigueur π* ; nulle à π* = 0",
                  lambda t: _exact(t.banque_centrale.pi_etoile)),
    "i_D": ("i_D = (1 + r̄)(1 + π*) − 1 − ϖ_D ; nul à π* = 0 parce que r̄ = ϖ_D",
            _taux_de_depot_exact),
})


def est_nulle(cle: str, tables) -> bool:
    """D1 : la grandeur `cle` est nulle en arithmétique exacte aux tables `tables`
    (`GRANDEURS_NULLES`)."""
    return cle in GRANDEURS_NULLES and GRANDEURS_NULLES[cle][1](tables) == 0
