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
- grandeur sans dimension (U, tu, ξ, μ̃, π^e) : 1.

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
porte l'étiquette `ETIQUETTE` et ne vaut pas verdict de boucle conjointe.

**Variables du pas** : noms, écrivains, étapes et lecteurs de l'annotation du
13/11/2026, point 2.2. La banque propose la ligne 21 sous la forme exacte de
B7, −min(Res^{8b} ; L^CB), sur les positions lues (le noyau arrête sur une
poussière de réserves) ; l'État déclare le montant couvert de la ligne 16 si
elle est négative (jamais sur le sentier).

**Échelle nominale** : `echelle` multiplie chaque grandeur nominale du sentier
(montants, prix, salaire, positions, registre) ; l'invariance × 100 compare un
socle à `echelle = 100` à 100 fois le socle à `echelle = 1`.
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
import types
from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from pathlib import Path

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
from nations.moteur.ordonnanceur import INDICE_DES_PRIX, DeclarationDesEntrees, EntreesDuTour
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.moteur.phases import PHASES
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt

RACINE = Path(__file__).resolve().parents[2]
ETIQUETTE = "π^e exogène (bloc d'essai)"
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
    ("menages", "2"): {"C_plan": ("C_plan", NOMINAL)},
    ("investissement", "2"): {"I_plan": ("I_plan", NOMINAL)},
    ("finances_publiques", "2"): {"G_plan": ("G_plan", NOMINAL)},
}

# Valeurs du pas suivant des variables d'état (C2) : nom → (clé du pas 0, classe).
VARIABLES_D_ETAT = {
    "v_e": ("ve_1", VOLUME), "IN_vol": ("IN_vol_1", VOLUME), "pr": ("pr_1", PRODUCTIVITE),
    "K_vol": ("K_vol_1", VOLUME), "W": ("W", SALAIRE), "U": ("U", CONSTANTE),
    "N": ("N", PERSONNES), "N_pa": ("N_pa_1", PERSONNES), "mu_tilde": ("mu_tilde", CONSTANTE),
    "pi_e": ("pi_e_1", CONSTANTE),
}
if set(VARIABLES_D_ETAT) != {v.nom for v in schema.VARIABLES_DES_BLOCS}:
    raise AssertionError("socle partiel : une variable d'état du schéma sans valeur du sentier")

# Valeur à l'ouverture du pas 0 de chaque variable d'état (clé de `ouverture`).
OUVERTURE_DES_VARIABLES = {
    "v_e": "ve", "IN_vol": "IN_vol", "pr": "pr", "K_vol": "K_vol", "W": "W_m1", "U": "U_m1",
    "N": "N_m1", "N_pa": "N_pa", "mu_tilde": "mu_tilde_m1", "pi_e": "pi_e",
}

# Lignes proposées aux montants du sentier : ligne → {terme: clé du pas 0}, classe nominale.
# Les lignes 1 à 3 (acheteurs, p × volume servi) et 21 (B7, forme exacte) n'y sont pas.
LIGNES_DU_SENTIER = {
    "4": {"Delta_IN": "dIN"}, "5": {"WB": "WB"}, "6": {"Tr": "Tr"},
    "7": {"T_H": "T_H", "T_F": "T_F"}, "8": {"deltaK": "amort"}, "9": {"iL_L": "l9"},
    "10": {"iD_DH": "l10_H", "iD_DF": "l10_F"}, "11a": {"iB_BH": "l11a"},
    "11b": {"iB_BBk": "l11b"}, "11c": {"iB_BCB": "l11c"}, "12": {"ires_Res": "l12"},
    "13": {"iCB_LCB": "l13"}, "14": {"Div_F": "Div_F"}, "15": {"Div_Bk": "Div_Bk"},
    "16": {"Pi_CB": "l16"}, "18": {"Delta_L": "dL"}, "19a-ménages": {"Delta_BH_prim": "dB_H"},
    "19a-banque": {"Delta_BBk_prim": "dB_Bk"}, "19a-BC": {"Delta_BCB_prim": "dB_CB"},
}

# Acheteurs : (radical, ligne, terme, volume servi lu, plan écrit en phase 2).
ACHETEURS = (("menages", "1", "C", "C_vol", "C_plan"),
             ("investissement", "3", "I", "I_vol", "I_plan"),
             ("finances_publiques", "2", "G", "G_vol", "G_plan"))


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
    if (radical, etape) == ("finances_publiques", "8b"):
        lectures.append(Lecture(GRAND_LIVRE, "M_G"))
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
        for ligne in siege.propose:
            acheteur = next((a for a in ACHETEURS if a[1] == ligne), None)
            if acheteur is not None:
                _, _, terme, volume, _ = acheteur
                vue.proposer(ligne, {terme: vue.lire("p") * vue.lire(volume)})
            elif ligne == "21":
                livre = vue.grand_livre
                vue.proposer("21", {"Delta_LCB": -min(livre.position("Res"),
                                                      livre.position("L_CB"))})
            else:
                vue.proposer(ligne, {terme: sentier.valeur(cle, NOMINAL, t, echelle)
                                     for terme, cle in LIGNES_DU_SENTIER[ligne].items()})
        if siege.couvre:
            perte = sentier.valeur("l16", NOMINAL, t, echelle)
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
                   regles: dict | None = None,
                   declaration: DeclarationDeBloc | None = None) -> type:
    """Classe du bloc d'essai d'un radical ; `declaration` remplace sa déclaration (essais de
    refus à l'assemblage) ; `regles` donne, pour une variable d'état du radical, une règle
    d'essai (vue, sentier, t) → valeur du pas suivant, à la place du sentier (cas d'essai de
    la linéarisation)."""
    declaration = declaration_d_essai(radical) if declaration is None else declaration
    reglage = types.MappingProxyType({
        "sentier": sentier, "echelle": echelle, "choc_pi_e": choc_pi_e,
        "chocs_des_plans": chocs_des_plans, "regles": types.MappingProxyType(regles or {}),
        "sieges": types.MappingProxyType({s.etape: s for s in declaration.sieges})})
    espace = {"__slots__": (), "declaration": declaration, "reglage": reglage}
    for siege in declaration.sieges:
        espace[f"phase_{siege.etape}"] = (
            lambda etape: lambda self, vue: self._agir(vue, etape))(siege.etape)
    nom = "".join(m.capitalize() for m in radical.split("_")) + "DEssai"
    return type(nom, (_BlocDEssai,), espace)


RADICAUX = ("production", "travail", "prix", "menages", "investissement", "banque",
            "banque_centrale", "finances_publiques")


def blocs(sentier: Sentier, *, echelle: float = 1.0,
          choc_pi_e: Callable[[int], float] = _choc_nul,
          chocs_des_plans: Callable[[str, int], float] = _plans_sans_choc,
          regles: dict | None = None, reels: Sequence[object] = (),
          declarations: dict | None = None) -> tuple[object, ...]:
    """Les huit blocs : un bloc d'essai par radical, sauf ceux que `reels` fournit (un bloc
    réel par radical, #113, #50, #51) ; `declarations` remplace la déclaration d'un radical ;
    `regles` : variable d'état → règle d'essai, passée au bloc de son propriétaire."""
    remplaces = {b.declaration.radical: b for b in reels}
    rendus = []
    for radical in RADICAUX:
        if radical in remplaces:
            rendus.append(remplaces[radical])
            continue
        propres = {nom: regle for nom, regle in (regles or {}).items()
                   if schema.VARIABLE[nom].proprietaire == radical}
        classe = classe_d_essai(radical, sentier, echelle=echelle, choc_pi_e=choc_pi_e,
                                chocs_des_plans=chocs_des_plans, regles=propres,
                                declaration=(declarations or {}).get(radical))
        rendus.append(classe())
    return tuple(rendus)


def blocs_reels() -> tuple[object, ...]:
    """Les blocs réels de `src/nations/blocs/`, dans l'ordre des radicaux : un module par
    radical, dont l'unique classe déclarée sous ce radical est instanciée (ADR 0012, annotation
    du 13/11/2026, point 5 : chaque module porte un seul bloc, dont le radical est le nom du
    module). En J3-b : la production (#113), puis le travail (#50) et les prix (#51)."""
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


def ordonnanceur(sentier: Sentier, parametres=PARAMETRES_DE_REFERENCE, **options):
    """Ordonnanceur du socle partiel d'essai, aux tables de référence par défaut."""
    return ordo.assembler(PHASES, blocs(sentier, **options), parametres, SANS_ENTREES)


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
