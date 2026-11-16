"""Empreintes SHA-256 des trajectoires des bancs d'essai (#144 ; P173, P184, P187).

**Objet.** Le critère « Branche » de la branche « forme du code » (feuille de
route, § 1) exige des trajectoires **identiques au bit** avant et après chaque
commit `code:`. Ce script produit, de façon déterministe, une empreinte par
banc et par π*, une par banc et une globale ; deux versions du moteur ont les
mêmes trajectoires si leurs empreintes sont égales (principe 7 des workflows :
un contrôle mécanique est un script). Encodage décidé par le mainteneur le
16/11/2026 (le lien avec l'empreinte de J3-d2 `d9931c92…f654`, dont la
méthode n'a pas été consignée, est abandonné).

**Bancs** (`BANCS`, dans cet ordre ; n_a = 12, ν_G = 1,15 passé au script de
l'état stationnaire par `socle_partiel.sentier`, son défaut ν_G = 1 étant hors
domaine ; π* ∈ {0 ; 2 % ; 10 %} ; 720 pas depuis `socle_partiel.etat_initial`,
entrées ς_L = ς_B = 0 sauf mention) :

- `socle complet` : blocs 2 à 9 réels, sans choc
  (`tests/invariants/test_socle_complet.py`, `derouler`) ;
- `socle complet D` (P184, choisi par `macro`), « dépense au-delà de la
  marge » : bloc 9 réel composé `bloc_9_compose(choc_de_theta_G(
  AU_DELA_DE_LA_MARGE[π*]))` (θ_G × 1,25 à 0 et 2 %, × 1,60 à 10 %, pas 0 à
  11), scénario de `test_caisse_sur_le_moteur` ; lie le plafond de E1, Π^CB < 0
  en phase 8 (b) à π* = 0 et le plancher de F3 ;
- `socle complet BF` (P184, choisi par `macro`), « placement raté puis
  transferts, titres à la banque centrale » : variante à θ_CB = 0,5 (P184) du
  second déroulé de `test_placement_rate_de_moitie_sur_un_tour` (le test joue
  le sentier par défaut) : ς_B = 0,5 au pas 5, bloc 9 réel composé
  `bloc_9_compose(levier_au_tour(6, theta_Tr=TRANSFERTS_APRES_LE_PLACEMENT))` ;
  lie ς_B > 0 dans E11, le plafond de E6, la part non payée de E13 et le terme
  11c de E7 ;
- `P87` : blocs 2, 3, 4, 7 et 8 réels, blocs d'essai 5, 6 et 9, émission X3,
  λ_e de la table (`tests/invariants/test_boucle_t3_bc3.py`, contrôle sans
  choc) ;
- `J3-d1 X4 seule`, `J3-d1 X4 + X3` : blocs 2 à 8 réels, bloc d'essai 9 avec
  la couverture X4, seule ou composée avec X3
  (`tests/invariants/test_stationnarite_j3d1.py`, `options_du_banc`) ;
- `J3-d1 sans X4` : blocs 2 à 8 réels, bloc d'essai 9 sans option
  (contre-épreuve du même module) ;
- `essai pur` : huit blocs d'essai (`tests/invariants/test_socle_partiel.py`).

Les fonctions de construction et les scénarios sont ceux des tests, chargés
par leur chemin sous la racine choisie ; aucun n'est recopié (seuls le pas 5
et la part 0,5 du placement raté, écrits en ligne dans le test, sont repris).

**Refus** (`BancNonConforme`, code de sortie 2, jamais une empreinte) :
module introuvable à l'import (`ImportError`, par exemple un fichier de
`src/nations/blocs/` absent de la version « avant » extraite) ; banc dont les
blocs ne sont pas, dans l'ordre canonique, un par radical, réels exactement
pour `BLOCS_REELS_ATTENDUS` (`blocs_reels()` saute en silence un module
absent) ; paquet `nations` chargé hors de `<racine>/src`. Un bloc est **réel**
si sa classe est définie dans `nations.blocs.<radical>` (`type(bloc).__module__`,
test strict : une sous-classe d'un bloc réel définie ailleurs est refusée) ;
seule exception, le bloc 9 composé des bancs D et BF (`BANCS_A_BLOC_9_COMPOSE`) :
classe définie dans le module des scénarios du socle complet
(`MODULE_DU_SOCLE_COMPLET`), de base directe unique la classe réelle (P185, m-a).

**Arrêt du moteur = écart de trajectoire** (code 1) : toute autre exception levée pendant la
construction, l'assemblage ou le déroulé d'un banc (défaut comptable, refus
du moteur ou de proposition, erreur de code d'une version mutée) est
consignée pour ce banc et ce π* (type, message, pas atteint) à la place de
l'empreinte ; une mutation peut arrêter le moteur plutôt que changer une
empreinte.

**Ce que l'empreinte hache**, par banc et par π*, un n-uplet encodé par
événement, dans l'ordre du relevé :

1. `("I", état initial)` ;
2. chaque clôture de phase : `("C", t, phase, montants)`, montants =
   n-uplet de (ligne, n-uplet de (nom du terme, montant)) dans l'ordre du
   noyau ; les rapports de contrôle (résidus) ne sont pas hachés : ce sont
   des diagnostics, pas la trajectoire ;
3. chaque fin de pas : `("F", t, état t + 1, variables)`, variables = n-uplet
   de (nom, valeur) **trié par nom** (un réordonnancement de l'inscription ne
   change pas l'empreinte ; un ajout ou un retrait la change).

Un état est le n-uplet des (nom, valeur) de ses champs, dans l'ordre de
`nations.etat.schema.CHAMPS`. **Sous-empreintes**, pour localiser un écart :
`etats` (I et états des F), `montants` (C), `variables` (variables des F), et
`grandeurs` (grandeurs calculées à l'ouverture, n-uplet trié par nom, par fin
de pas). `grandeurs` est publiée et comparée (écart signalé à part, code 3)
mais **n'entre ni dans l'empreinte du banc ni dans la globale** : ce sont des
fonctions de l'état, et #144 (points 2 et 3) en ajoute et en retire sans
changer la trajectoire (P186, P189).

**Variables exclues** (`--exclure-variables`, P187) : pour juger un commit qui
ajoute et déclare une variable du pas (`etats` et `montants` égaux au bit,
variables préexistantes égales), les variables du pas nommées sont retirées du
n-uplet `variables` des fins de pas, donc de la sous-empreinte `variables`, de
l'empreinte du banc à π* et des empreintes agrégées ; `etats`, `montants` et
`grandeurs` sont inchangés. Sans l'option, rien ne change au bit. Les noms
exclus sont consignés (`variables_exclues`, triés) et affichés ; avec
exclusion, chaque banc et π* porte aussi `variables_sans_exclusion` (la
sous-empreinte sans retrait) et `exclues_presentes` (noms exclus relevés),
informatifs, non comparés (un banc arrêté garde `exclues_presentes`, relevé
jusqu'à l'arrêt). Refus (code 2) : nom exclu qui n'est une variable du pas
d'aucun banc mesuré (faute de frappe : jamais une exclusion silencieuse ;
contrôle après le déroulé ; si un banc s'est arrêté, un nom non relevé n'est
pas conclu inconnu : il est consigné à part (`exclues_non_etablies`, remarque
distincte des arrêts, non décomptée parmi eux) et l'arrêt donne le code 1) ;
comparaison à une référence mesurée **avec** exclusion, quelles que soient les exclusions de la mesure
(elle porte par construction les variables exclues, dont la valeur n'est pas
hachée : P187 non jugeable). Seule une référence sans exclusion est
comparable à une mesure avec exclusion, si les variables exclues en sont
absentes. La référence ne garde que des empreintes : l'absence s'établit,
par banc et π* où une variable exclue est relevée, par l'égalité de son
`variables` à celui de la mesure ; l'égalité à `variables_sans_exclusion`
prouve la présence (refus, une seule suffit) ; sinon l'absence n'est pas
établie et l'écart de `variables` donne le code 1. Un critère tenu (code 0
ou 3) avec exclusion, contre une référence sans exclusion, établit donc
l'absence des variables exclues dans la référence, partout où la mesure les
relève.

**Pays.** Un seul pays (« A ») par banc ; s'il y en avait plusieurs (J5), ils
seraient hachés dans l'ordre canonique de leur identifiant (refus sinon).

**Encodage binaire** (`encoder`, version `VERSION_DE_L_ENCODAGE`), sans
ambiguïté de concaténation, chaque valeur précédée d'une étiquette d'un
octet :

- `float` : `d` + 8 octets IEEE 754 petit-boutiste (`struct` `<d`), donc au
  bit (−0,0 ≠ 0,0, aucune conversion décimale) ;
- `bool` : `b` + un octet 0 ou 1 (testé avant `int`) ;
- `int` : `i` + longueur (`<I`) + écriture décimale ASCII (entiers de
  taille quelconque, la graine compris) ;
- `str` : `s` + longueur en octets (`<I`) + UTF-8 ;
- `tuple` : `t` + nombre d'éléments (`<I`) + chaque élément ;
- tout autre type est refusé (`TypeError`), jamais converti.

**Empreintes agrégées.** Empreinte d'un banc : SHA-256 de, pour chaque π*
dans l'ordre de `POINTS_PI`, `encoder(π*)` suivi des 32 octets de
l'empreinte du banc à π*. Empreinte globale : SHA-256 de, pour chaque banc
dans l'ordre de `BANCS`, `encoder(nom)` suivi de la même suite. Un banc
arrêté n'a pas d'empreinte agrégée.

**Usage.**

    uv run python outils/empreintes_des_bancs.py [--racine DOSSIER] [--pas N]
        [--bancs NOM …] [--ecrire FICHIER] [--comparer FICHIER]
        [--exclure-variables NOM …]

`--racine` : arbre à mesurer (par défaut le dépôt) ; pour une version
« avant », l'extraire **avec `src/`, `tests/` et `outils/`**
(`git archive <sha> src tests outils | tar -x -C DOSSIER`) ; `src/` de cette
racine est placé en tête de `sys.path`, et le script refuse de tourner si le
paquet `nations` chargé n'en vient pas. `--ecrire` écrit les empreintes en
JSON ; `--comparer` les compare à un JSON écrit par `--ecrire` (mêmes bancs,
même nombre de pas, même version d'encodage). Codes de sortie :

- 0 : conforme (trajectoires et grandeurs d'ouverture identiques) ;
- 1 : une empreinte de trajectoire diffère (empreinte, `etats`, `montants`,
  `variables`, banc, globale, ou version, pas, π*, bancs), ou arrêt du moteur ;
  tous les écarts sont listés, ceux des grandeurs d'ouverture compris ;
- 2 : refus (banc non conforme, racine invalide, fichier illisible, variable
  exclue inconnue ou présente dans la référence, référence mesurée avec
  exclusion) ;
- 3 : trajectoires identiques, seules les sous-empreintes `grandeurs`
  diffèrent (ajout ou retrait de grandeurs d'ouverture, P186, P189) : critère
  tenu, écart à déclarer dans le commit.

Avec `--exclure-variables`, les codes 0 et 3 valent tous deux « critère de
P187 tenu » (variable du pas ajoutée, trajectoire préexistante identique) :
3 si, en plus, les grandeurs d'ouverture diffèrent, 0 sinon.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import struct
import sys
from pathlib import Path

RACINE_DU_DEPOT = Path(__file__).resolve().parents[1]
VERSION_DE_L_ENCODAGE = 2
NB_PAS = 720
SOCLE_COMPLET = "socle complet"
SOCLE_COMPLET_D = "socle complet D"
SOCLE_COMPLET_BF = "socle complet BF"
P87 = "P87"
X4_SEULE = "J3-d1 X4 seule"
X4_X3 = "J3-d1 X4 + X3"
SANS_X4 = "J3-d1 sans X4"
ESSAI_PUR = "essai pur"
BANCS = (SOCLE_COMPLET, SOCLE_COMPLET_D, SOCLE_COMPLET_BF, P87, X4_SEULE, X4_X3, SANS_X4,
         ESSAI_PUR)
# Placement raté du banc BF (`test_placement_rate_de_moitie_sur_un_tour`) : part ς_B au pas.
PAS_DU_PLACEMENT_RATE = 5
PART_NON_SOUSCRITE = 0.5
THETA_CB_DU_BANC_BF = 0.5
# Radicaux des blocs réels attendus par banc ; les autres radicaux sont des blocs d'essai.
_BLOCS_2_A_8 = frozenset({"production", "travail", "prix", "menages", "investissement",
                          "banque", "banque_centrale"})
_BLOCS_2_A_9 = _BLOCS_2_A_8 | {"finances_publiques"}
BLOCS_REELS_ATTENDUS = {
    SOCLE_COMPLET: _BLOCS_2_A_9,
    SOCLE_COMPLET_D: _BLOCS_2_A_9,
    SOCLE_COMPLET_BF: _BLOCS_2_A_9,
    P87: frozenset({"production", "travail", "prix", "banque", "banque_centrale"}),
    X4_SEULE: _BLOCS_2_A_8,
    X4_X3: _BLOCS_2_A_8,
    SANS_X4: _BLOCS_2_A_8,
    ESSAI_PUR: frozenset(),
}
PARTIES = ("etats", "montants", "variables")
HORS_EMPREINTE = ("grandeurs",)
# Bancs dont le bloc 9 est le bloc réel composé dans `tests/` (`bloc_9_compose`), et nom sous
# lequel le module des scénarios du socle complet est chargé (P185, m-a).
BANCS_A_BLOC_9_COMPOSE = frozenset({SOCLE_COMPLET_D, SOCLE_COMPLET_BF})
RADICAL_DU_BLOC_COMPOSE = "finances_publiques"
MODULE_DU_SOCLE_COMPLET = "empreintes_socle_complet"
# Codes de sortie (voir le docstring du module).
CONFORME, ECART, REFUS, GRANDEURS_SEULES = 0, 1, 2, 3


class BancNonConforme(RuntimeError):
    """Refus : module introuvable, banc dont les blocs ne sont pas ceux attendus (bloc
    manquant, bloc d'essai à la place d'un bloc réel ou l'inverse, radical en trop), ou racine
    dont le paquet `nations` ne vient pas de `src/`."""


# --------------------------------------------------------------------------
# Encodage
# --------------------------------------------------------------------------


def encoder(valeur: object) -> bytes:
    """Encodage binaire sans ambiguïté d'une valeur de type de base (voir le docstring du
    module) ; tout autre type est refusé."""
    if type(valeur) is float:
        return b"d" + struct.pack("<d", valeur)
    if type(valeur) is bool:
        return b"b" + (b"\x01" if valeur else b"\x00")
    if type(valeur) is int:
        texte = str(valeur).encode("ascii")
        return b"i" + struct.pack("<I", len(texte)) + texte
    if type(valeur) is str:
        texte = valeur.encode("utf-8")
        return b"s" + struct.pack("<I", len(texte)) + texte
    if type(valeur) is tuple:
        return b"t" + struct.pack("<I", len(valeur)) + b"".join(encoder(x) for x in valeur)
    raise TypeError(f"type {type(valeur).__name__} non encodable : refusé, jamais converti")


class Hacheur:
    """Observateur du moteur : hache la trajectoire relevée (flux complet, un n-uplet par
    événement, et sous-empreintes par partie). Ne rend rien et n'agit pas sur la trajectoire ;
    `pas` compte les fins de pas relevées (pas atteint en cas d'arrêt)."""

    def __init__(self, champs, cloture, fin_de_pas, exclues=frozenset()):
        self._champs = tuple(champs)
        self._cloture = cloture
        self._fin_de_pas = fin_de_pas
        self._exclues = frozenset(exclues)
        self.pas = 0
        self.complet = hashlib.sha256()
        self.parties = {p: hashlib.sha256() for p in PARTIES + HORS_EMPREINTE}
        # Avec exclusion seulement (P187) : `variables` sans exclusion, et noms exclus relevés.
        self.sans_exclusion = hashlib.sha256() if self._exclues else None
        self.exclues_presentes = set()

    def n_uplet_d_etat(self, etat) -> tuple:
        return tuple((nom, getattr(etat, nom)) for nom in self._champs)

    def initial(self, etat) -> None:
        n_uplet = self.n_uplet_d_etat(etat)
        self.complet.update(encoder(("I", n_uplet)))
        self.parties["etats"].update(encoder(n_uplet))

    def relever(self, e) -> None:
        if type(e) is self._cloture:
            montants = tuple((ligne, tuple(termes)) for ligne, termes in e.montants)
            self.complet.update(encoder(("C", e.t, e.phase, montants)))
            self.parties["montants"].update(encoder((e.t, e.phase, montants)))
        elif type(e) is self._fin_de_pas:
            etat = self.n_uplet_d_etat(e.etat)
            toutes = tuple(sorted(e.variables_du_pas, key=lambda paire: paire[0]))
            variables = toutes
            if self._exclues:
                variables = tuple(p for p in toutes if p[0] not in self._exclues)
                self.exclues_presentes.update(p[0] for p in toutes if p[0] in self._exclues)
                self.sans_exclusion.update(encoder((e.t, toutes)))
            grandeurs = tuple(sorted(e.grandeurs_ouverture, key=lambda paire: paire[0]))
            self.complet.update(encoder(("F", e.t, etat, variables)))
            self.parties["etats"].update(encoder((e.t, etat)))
            self.parties["variables"].update(encoder((e.t, variables)))
            self.parties["grandeurs"].update(encoder((e.t, grandeurs)))
            self.pas += 1
        else:
            raise TypeError(f"événement {type(e).__name__} inconnu : refusé")


# --------------------------------------------------------------------------
# Chargement de la racine et des bancs
# --------------------------------------------------------------------------


class Racine:
    """Modules d'une racine : paquet `nations` de `<racine>/src`, et modules de
    `tests/invariants/` qui construisent les bancs, chargés par leur chemin."""

    def __init__(self, racine: Path):
        racine = Path(racine).resolve()
        source = racine / "src"
        if not (source / "nations").is_dir():
            raise BancNonConforme(f"{racine} : pas de src/nations/ (extraire l'arbre avec src/)")
        if str(source) not in sys.path[:1]:
            sys.path.insert(0, str(source))
        try:
            import nations
            origine = Path(nations.__file__).resolve()
            if source not in origine.parents:
                raise BancNonConforme(f"paquet nations chargé depuis {origine}, hors de "
                                      f"{source} : refusé (une seule racine par processus)")
            from nations.etat.schema import CHAMPS
            from nations.moteur import ordonnanceur
            from nations.moteur.phases import PHASES
            from nations.noyau.grand_livre import ClotureDePhase
            from nations.observation.observateur import FinDePas
            invariants = racine / "tests" / "invariants"
            self.socle = _charger("socle_partiel", invariants / "socle_partiel.py")
            self.complet = _charger(MODULE_DU_SOCLE_COMPLET,
                                    invariants / "test_socle_complet.py")
            self.boucle = _charger("empreintes_boucle_t3_bc3",
                                   invariants / "test_boucle_t3_bc3.py")
            self.j3d1 = _charger("empreintes_stationnarite_j3d1",
                                 invariants / "test_stationnarite_j3d1.py")
        except ImportError as erreur:
            raise BancNonConforme(f"module introuvable sous {racine} : {erreur} (extraire "
                                  "l'arbre complet : src, tests, outils)") from erreur
        self.racine = racine
        self.champs = CHAMPS
        self.ordo = ordonnanceur
        self.phases = PHASES
        self.cloture = ClotureDePhase
        self.fin_de_pas = FinDePas

    def construire(self, banc: str, pi: float):
        """(blocs, état initial, dérouler) du banc `banc` à π* = `pi` ; `dérouler(observateur,
        nb_pas)` joue le banc par la fonction de déroulé de son test."""
        s, c = self.socle, self.complet
        if banc in (SOCLE_COMPLET, SOCLE_COMPLET_D, SOCLE_COMPLET_BF):
            sentier = (s.sentier(pi, theta_CB=THETA_CB_DU_BANC_BF) if banc == SOCLE_COMPLET_BF
                       else s.sentier(pi))
            bloc_9, placement = None, None
            if banc == SOCLE_COMPLET_D:
                bloc_9 = c.bloc_9_compose(c.choc_de_theta_G(c.AU_DELA_DE_LA_MARGE[pi]))
            elif banc == SOCLE_COMPLET_BF:
                bloc_9 = c.bloc_9_compose(c.levier_au_tour(
                    PAS_DU_PLACEMENT_RATE + 1, theta_Tr=c.TRANSFERTS_APRES_LE_PLACEMENT))

                def placement(t):
                    return PART_NON_SOUSCRITE if t == PAS_DU_PLACEMENT_RATE else 0.0

            def derouler(observateur, nb_pas):
                c.derouler(s, sentier, nb_pas, bloc_9=bloc_9, varsigma_B=placement,
                           observateur=observateur)
            return c.blocs(s, bloc_9), s.etat_initial(sentier), derouler
        if banc == P87:
            lam = self.boucle.LAMBDA_DE_LA_TABLE
            sentier = s.sentier(pi, lambda_e=lam)
            tables = s.parametres_du_sentier(sentier, self.boucle.parametres(pi, lam))
            blocs = s.blocs(sentier, reels=self.boucle.reels(), **s.emission_x3())
        else:
            sentier = s.sentier(pi)
            tables = s.parametres_du_sentier(sentier)
            if banc in (X4_SEULE, X4_X3):
                nom = {X4_SEULE: self.j3d1.X4_SEULE, X4_X3: self.j3d1.X4_X3}[banc]
                options = self.j3d1.options_du_banc(s, nom)
                blocs = s.blocs(sentier, reels=s.blocs_reels(), **options)
            elif banc == SANS_X4:
                blocs = s.blocs(sentier, reels=s.blocs_reels())
            elif banc == ESSAI_PUR:
                blocs = s.blocs(sentier)
            else:
                raise BancNonConforme(f"banc {banc!r} inconnu (bancs : {', '.join(BANCS)})")
        initial = s.etat_initial(sentier)

        def derouler(observateur, nb_pas):
            o = self.ordo.assembler(self.phases, blocs, tables, s.ENTREES_DU_SOCLE)
            s.derouler(initial, nb_pas, o, observateur)
        return blocs, initial, derouler


def _charger(nom: str, chemin: Path):
    """Module chargé par son chemin ; un module de même nom venu d'un autre chemin est refusé."""
    if nom in sys.modules:
        deja = Path(sys.modules[nom].__file__).resolve()
        if deja != chemin.resolve():
            raise BancNonConforme(f"module {nom} déjà chargé depuis {deja}, non {chemin}")
        return sys.modules[nom]
    if not chemin.is_file():
        raise BancNonConforme(f"{chemin} absent (extraire l'arbre avec tests/)")
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    sys.modules[nom] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        del sys.modules[nom]
        raise
    return module


def _est_reel(bloc, banc: str) -> bool:
    """Bloc réel : sa classe est définie dans `nations.blocs.<radical>` (test strict sur
    `type(bloc).__module__`). Seule exception (P185, m-a) : le bloc 9 composé des bancs D et
    BF, dont la classe est définie dans le module des scénarios du socle complet et a pour base
    directe unique la classe réelle du bloc 9."""
    radical = bloc.declaration.radical
    module = f"nations.blocs.{radical}"
    classe = type(bloc)
    if classe.__module__ == module:
        return True
    if banc not in BANCS_A_BLOC_9_COMPOSE or radical != RADICAL_DU_BLOC_COMPOSE:
        return False
    if classe.__module__ != MODULE_DU_SOCLE_COMPLET or len(classe.__bases__) != 1:
        return False
    base, = classe.__bases__
    reel = sys.modules.get(module)
    return (base.__module__ == module and reel is not None
            and getattr(reel, base.__name__, None) is base)


def verifier_blocs(banc: str, blocs, radicaux: tuple[str, ...]) -> None:
    """Refus bruyant (`BancNonConforme`) si les blocs du banc ne sont pas, dans l'ordre
    canonique, un bloc par radical de `radicaux`, réels exactement pour
    `BLOCS_REELS_ATTENDUS[banc]`."""
    trouves = tuple(b.declaration.radical for b in blocs)
    if trouves != tuple(radicaux):
        manquants = sorted(set(radicaux) - set(trouves))
        raise BancNonConforme(f"banc {banc} : radicaux {trouves}, attendus {tuple(radicaux)}"
                              + (f" ; manquants : {manquants}" if manquants else ""))
    reels = {b.declaration.radical for b in blocs if _est_reel(b, banc)}
    attendus = BLOCS_REELS_ATTENDUS[banc]
    if reels != attendus:
        raise BancNonConforme(
            f"banc {banc} : blocs réels {sorted(reels)}, attendus {sorted(attendus)} ; "
            f"manquants : {sorted(attendus - reels)} ; en trop : {sorted(reels - attendus)} "
            "(module de src/nations/blocs/ absent ? refusé, jamais ignoré en silence)")


def empreinte_du_banc(racine: Racine, banc: str, pi: float, nb_pas: int,
                      exclues=()) -> dict:
    """Empreintes (flux complet et parties, hexadécimales) du banc `banc` à π* = `pi` sur
    `nb_pas` pas, variables du pas nommées dans `exclues` retirées (P187 ; s'y ajoutent alors
    `variables_sans_exclusion` et `exclues_presentes`) ; en cas d'arrêt,
    `{"arret": {type, message, pas}}` à la place."""
    hacheur = Hacheur(racine.champs, racine.cloture, racine.fin_de_pas, exclues)
    try:
        blocs, initial, derouler = racine.construire(banc, pi)
        verifier_blocs(banc, blocs, racine.socle.RADICAUX)
        etats = (initial,)
        if [e.identifiant for e in etats] != sorted(e.identifiant for e in etats):
            raise BancNonConforme("pays hors de l'ordre canonique (identifiant)")
        hacheur.initial(initial)
        derouler(hacheur, nb_pas)
    except (BancNonConforme, ImportError) as erreur:
        if isinstance(erreur, ImportError):
            raise BancNonConforme(f"banc {banc} : module introuvable : {erreur}") from erreur
        raise
    # Arrêt du moteur ou erreur de code d'une version mutée : consigné comme écart (code 1),
    # jamais ignoré ; toute exception est voulue ici (m-1 de l'audit du rang 1a).
    except Exception as erreur:  # noqa: BLE001
        arret = {"arret": {"type": type(erreur).__name__, "message": str(erreur),
                           "pas": hacheur.pas}}
        if exclues:
            arret["exclues_presentes"] = sorted(hacheur.exclues_presentes)
        return arret
    valeurs = {"empreinte": hacheur.complet.hexdigest(),
               **{p: h.hexdigest() for p, h in hacheur.parties.items()}}
    if exclues:
        valeurs["variables_sans_exclusion"] = hacheur.sans_exclusion.hexdigest()
        valeurs["exclues_presentes"] = sorted(hacheur.exclues_presentes)
    return valeurs


def _cle_pi(pi: float) -> str:
    return repr(pi)


def agreger(paires) -> str:
    """SHA-256 de la suite ordonnée (encoder(clé) + 32 octets de l'empreinte)."""
    h = hashlib.sha256()
    for cle, hexa in paires:
        h.update(encoder(cle) + bytes.fromhex(hexa))
    return h.hexdigest()


def empreintes(racine: Racine, bancs=BANCS, nb_pas: int = NB_PAS, exclues=()) -> dict:
    """Document des empreintes : variables exclues (P187), bancs → π* → empreintes, empreintes
    par banc, globale (None si un banc s'est arrêté), arrêts (les seuls arrêts réels), noms
    exclus non relevés avant un arrêt (`exclues_non_etablies`, remarque à part). Refus
    (`BancNonConforme`) si un nom exclu n'est une variable du pas d'aucun banc mesuré, à aucun
    π* ni aucun pas, sans qu'aucun banc se soit arrêté."""
    exclues = tuple(sorted(set(exclues)))
    points = tuple(racine.socle.POINTS_PI)
    par_banc, globales_par_banc, arrets = {}, {}, []
    for banc in bancs:
        par_banc[banc] = {_cle_pi(pi): empreinte_du_banc(racine, banc, pi, nb_pas, exclues)
                          for pi in points}
        arretes = [pi for pi, v in par_banc[banc].items() if "arret" in v]
        arrets += [f"{banc}, π* = {pi} : arrêt au pas {par_banc[banc][pi]['arret']['pas']}, "
                   f"{par_banc[banc][pi]['arret']['type']} : "
                   f"{par_banc[banc][pi]['arret']['message']}" for pi in arretes]
        globales_par_banc[banc] = None if arretes else agreger(
            (pi, par_banc[banc][_cle_pi(pi)]["empreinte"]) for pi in points)
    presentes = {nom for par_pi in par_banc.values() for v in par_pi.values()
                 for nom in v.get("exclues_presentes", ())}
    inconnues = [nom for nom in exclues if nom not in presentes]
    # Un banc arrêté a pu s'arrêter avant de relever le nom : inconnu non conclu, consigné à
    # part (ce n'est pas un arrêt) ; l'arrêt est un écart (code 1).
    non_etablies = inconnues if arrets else []
    if inconnues and not arrets:
        raise BancNonConforme(
            f"variables exclues {inconnues} : variable du pas d'aucun banc mesuré "
            f"({', '.join(bancs)}, {nb_pas} pas) ; refusé, jamais une exclusion silencieuse")
    complets = all(h is not None for h in globales_par_banc.values())
    return {
        "version_encodage": VERSION_DE_L_ENCODAGE,
        "variables_exclues": list(exclues),
        "nb_pas": nb_pas,
        "points_pi": list(points),
        "bancs": par_banc,
        "par_banc": globales_par_banc,
        "globale": agreger((b, globales_par_banc[b]) for b in bancs) if complets else None,
        "arrets": arrets,
        "exclues_non_etablies": non_etablies,
        # Information, non comparée.
        "plateforme": {"python": platform.python_version(), "systeme": platform.system(),
                       "machine": platform.machine()},
    }


def comparer(mesure: dict, reference: dict) -> list[str]:
    """Écarts de trajectoire entre deux documents (liste vide si identiques), plateforme et
    grandeurs d'ouverture exclues (`comparer_grandeurs`) ; un arrêt est un écart."""
    ecarts = []
    for cle in ("version_encodage", "nb_pas", "points_pi"):
        if mesure.get(cle) != reference.get(cle):
            ecarts.append(f"{cle} : mesuré {mesure.get(cle)!r}, référence {reference.get(cle)!r}")
    if ecarts:
        return ecarts
    if list(mesure["bancs"]) != list(reference["bancs"]):
        return [f"bancs : mesurés {list(mesure['bancs'])}, référence {list(reference['bancs'])}"]
    for banc, par_pi in mesure["bancs"].items():
        for pi, valeurs in par_pi.items():
            ref = reference["bancs"][banc].get(pi, {})
            if "arret" in valeurs or "arret" in ref:
                # Seul le contenu de l'arrêt se compare : `exclues_presentes` (avec exclusion)
                # est informatif.
                if valeurs.get("arret") != ref.get("arret"):
                    ecarts.append(f"{banc}, π* = {pi}, arrêt : mesuré {valeurs.get('arret')}, "
                                  f"référence {ref.get('arret')}")
                continue
            for partie in ("empreinte", *PARTIES):
                if valeurs[partie] != ref.get(partie):
                    ecarts.append(f"{banc}, π* = {pi}, {partie} : mesuré {valeurs[partie]}, "
                                  f"référence {ref.get(partie)}")
    for banc, hexa in mesure["par_banc"].items():
        if hexa != reference["par_banc"].get(banc):
            ecarts.append(f"{banc}, empreinte du banc : mesuré {hexa}, "
                          f"référence {reference['par_banc'].get(banc)}")
    if mesure["globale"] != reference["globale"]:
        ecarts.append(f"globale : mesuré {mesure['globale']}, référence {reference['globale']}")
    return ecarts


class ExclusionIncompatible(ValueError):
    """Refus de comparer (code 2) : exclusions de la mesure et de la référence incompatibles."""


def verifier_exclusions(mesure: dict, reference: dict) -> list[str]:
    """Comparabilité des exclusions (P187 : seules des variables absentes de la référence
    s'excluent) ; rend les π* où l'absence des variables exclues dans la référence n'a pu être
    établie (comparaison menée, écart en code 1).

    - référence mesurée avec exclusion (clé `variables_exclues` non vide), quelles que soient
      les exclusions de la mesure, mêmes noms compris : refus (`ExclusionIncompatible`) ; elle
      porte par construction les variables exclues, dont la valeur n'est pas hachée, et des
      exclusions symétriques masqueraient leur écart ;
    - ni l'une ni l'autre avec exclusion (une référence sans clé n'en exclut aucune) :
      comparaison ordinaire ;
    - référence sans exclusion, mesure avec : comparable seulement si les variables exclues
      sont **absentes** de la référence. La référence ne garde que des empreintes ; par banc
      et π* où une variable exclue est relevée dans la mesure : `variables` de la référence
      égale à `variables_sans_exclusion` de la mesure (la référence porte les variables
      exclues) : refus, une seule présence suffit ; égale à `variables` de la mesure : absence
      établie ; ni l'une ni l'autre : absence non établie, consignée (`variables` diffère de
      toute façon : écart, code 1). Un critère tenu (code 0 ou 3) établit donc l'absence
      partout où la mesure relève une variable exclue."""
    mes = list(mesure.get("variables_exclues", []))
    ref = list(reference.get("variables_exclues", []))
    if ref:
        raise ExclusionIncompatible(
            f"référence mesurée avec exclusion ({ref} ; mesure : {mes or 'sans exclusion'}) : "
            "elle porte par construction les variables exclues, P187 non jugeable ; "
            "comparaison refusée (mesurer la référence sans exclusion)")
    if not mes:
        return []
    presentes, non_etablies = [], []
    for banc, par_pi in mesure.get("bancs", {}).items():
        for pi, valeurs in par_pi.items():
            r = reference.get("bancs", {}).get(banc, {}).get(pi, {})
            if not valeurs.get("exclues_presentes") or "arret" in valeurs or "arret" in r:
                continue
            if r.get("variables") == valeurs["variables_sans_exclusion"]:
                presentes.append(f"{banc}, π* = {pi}")
            elif r.get("variables") != valeurs["variables"]:
                non_etablies.append(f"{banc}, π* = {pi}, variables exclues "
                                    f"{valeurs['exclues_presentes']} : absence dans la "
                                    "référence non établie")
    if presentes:
        raise ExclusionIncompatible(
            f"variables exclues {mes} présentes dans la référence (sans exclusion) : "
            f"{' ; '.join(presentes)} ; comparaison refusée (P187 : seules des variables "
            "absentes de la référence s'excluent)")
    return non_etablies


def comparer_grandeurs(mesure: dict, reference: dict) -> list[str]:
    """Écarts des seules sous-empreintes `grandeurs` (grandeurs calculées à l'ouverture, hors
    empreinte du banc), pour les bancs et π* communs aux deux documents et sans arrêt ; le
    reste relève de `comparer`."""
    ecarts = []
    for banc, par_pi in mesure.get("bancs", {}).items():
        for pi, valeurs in par_pi.items():
            ref = reference.get("bancs", {}).get(banc, {}).get(pi, {})
            if "arret" in valeurs or "arret" in ref:
                continue
            for partie in HORS_EMPREINTE:
                if valeurs.get(partie) != ref.get(partie):
                    ecarts.append(f"{banc}, π* = {pi}, {partie} (grandeurs d'ouverture, hors "
                                  f"empreinte du banc) : mesuré {valeurs.get(partie)}, "
                                  f"référence {ref.get(partie)}")
    return ecarts


def afficher(document: dict, racine: Path) -> None:
    print(f"Empreintes SHA-256 des bancs ({document['nb_pas']} pas, encodage "
          f"v{document['version_encodage']}, racine {racine})")
    if document["variables_exclues"]:
        print(f"  variables du pas exclues (P187) : {', '.join(document['variables_exclues'])}")
    for banc, par_pi in document["bancs"].items():
        for pi, valeurs in par_pi.items():
            texte = valeurs.get("empreinte") or (
                f"ARRÊT au pas {valeurs['arret']['pas']} ({valeurs['arret']['type']})")
            print(f"  {banc:<18} π* = {float(pi):<5g} {texte}")
    for banc, hexa in document["par_banc"].items():
        print(f"  {banc:<18} banc       {hexa}")
    print(f"  globale                       {document['globale']}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        epilog="codes de sortie : 0 conforme ; 1 écart de trajectoire ou arrêt du moteur ; "
               "2 refus (banc non conforme, racine invalide, fichier illisible, variable "
               "exclue inconnue ou présente dans la référence, référence mesurée avec "
               "exclusion) ; 3 trajectoires identiques, grandeurs d'ouverture différentes "
               "(P186, P189) ; avec --exclure-variables, 0 et 3 valent tous deux critère de "
               "P187 tenu (3 si en plus les grandeurs d'ouverture diffèrent)")
    parser.add_argument("--racine", type=Path, default=RACINE_DU_DEPOT,
                        help="arbre à mesurer (src/, tests/, outils/) ; défaut : le dépôt")
    parser.add_argument("--pas", type=int, default=NB_PAS, help=f"nombre de pas (défaut {NB_PAS})")
    parser.add_argument("--bancs", nargs="+", choices=BANCS, default=list(BANCS),
                        help="bancs à mesurer, dans l'ordre de BANCS")
    parser.add_argument("--ecrire", type=Path, help="écrire les empreintes en JSON")
    parser.add_argument("--comparer", type=Path,
                        help="comparer à un JSON écrit par --ecrire (code 1 si une trajectoire "
                             "diffère, 3 si seules les grandeurs d'ouverture diffèrent)")
    parser.add_argument("--exclure-variables", nargs="+", default=[], metavar="NOM",
                        help="variables du pas retirées de la sous-empreinte variables et des "
                             "empreintes qui en dépendent (P187) ; nom inconnu refusé (code 2)")
    args = parser.parse_args(argv)
    if args.pas < 1:
        parser.error("--pas doit être ≥ 1")
    bancs = tuple(b for b in BANCS if b in args.bancs)
    try:
        reference = (json.loads(args.comparer.read_text(encoding="utf-8"))
                     if args.comparer else None)
    except (OSError, ValueError) as erreur:
        print(f"refus : référence illisible ({erreur})", file=sys.stderr)
        return REFUS
    try:
        racine = Racine(args.racine)
        document = empreintes(racine, bancs, args.pas, args.exclure_variables)
    except BancNonConforme as erreur:
        print(f"refus : {erreur}", file=sys.stderr)
        return REFUS
    afficher(document, racine.racine)
    if args.ecrire:
        args.ecrire.write_text(json.dumps(document, ensure_ascii=False, indent=1) + "\n",
                               encoding="utf-8")
    code = CONFORME
    if document["arrets"]:
        print(f"ARRÊT du moteur ({len(document['arrets'])}) :", file=sys.stderr)
        for ligne in document["arrets"]:
            print(f"  {ligne}", file=sys.stderr)
        code = ECART
    if document["exclues_non_etablies"]:
        print(f"variables exclues non relevées avant l'arrêt "
              f"({len(document['exclues_non_etablies'])}) : "
              f"{', '.join(document['exclues_non_etablies'])} ; inconnues non établies",
              file=sys.stderr)
    if reference is not None:
        try:
            non_etablies = verifier_exclusions(document, reference)
        except ExclusionIncompatible as erreur:
            print(f"refus : {erreur}", file=sys.stderr)
            return REFUS
        ecarts = comparer(document, reference)
        grandeurs = comparer_grandeurs(document, reference)
        if ecarts:
            print(f"ÉCART de trajectoire à {args.comparer} "
                  f"({len(ecarts) + len(grandeurs) + len(non_etablies)}) :",
                  file=sys.stderr)
            for ligne in ecarts + grandeurs + non_etablies:
                print(f"  {ligne}", file=sys.stderr)
            return ECART
        if code != CONFORME:
            return code
        if grandeurs:
            print(f"trajectoires identiques, grandeurs d'ouverture différentes de "
                  f"{args.comparer} ({len(grandeurs)}) : écart à déclarer (P186, P189)",
                  file=sys.stderr)
            for ligne in grandeurs:
                print(f"  {ligne}", file=sys.stderr)
            return GRANDEURS_SEULES
        print(f"identique à {args.comparer}")
    return code


if __name__ == "__main__":
    sys.exit(main())
