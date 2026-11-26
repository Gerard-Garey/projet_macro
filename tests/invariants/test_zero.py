"""Test zéro du jalon J3 depuis l'état initial de `scenarios/` (#176) : A1, A2, B1 à B26, F1, C1.

**Banc** : huit blocs réels (`socle.blocs_du_socle_complet()`, aucun bloc d'essai), tables de
référence (table T1, décision M34) à π* ∈ {0 ; 2 % ; 10 %} par `varier`, état initial et tables
alignées (θ_G résolu) rendus par `nations.scenarios.initial.etat_initial` à la normalisation de
référence, graine 0, sans choc ni scénario (ς_L = ς_B = 0), n_a = 12, ν_G = 1,15 de la table.
Série : `nations.observation.serie_test_zero.SerieDuTestZero` (définitions de
`tab:criteres-j3`). Fenêtres : P, les 120 premiers pas (blocs 1 et 2) ; L, 720 pas (blocs 1 à 12)
de la même trajectoire, verdicts publiés côte à côte.

**Critères, écrits avant l'essai** (`tab:criteres-j3`, inchangés ; #176 ; ADR 0015, point 2 ;
P248, P249), non déplacés après observation :
- **A1** (transcription) : chaque valeur de `tab:etat-stationnaire`, script (`Calculs.v` sur ses
  `Parametres`) contre moteur, à 1e−9 relatif, t = 0, aux trois π* ; côté moteur, un stock se lit
  sur l'`EtatPays` et les tables rendus par `scenarios/`, un flux sur le pas 0 exécuté ;
- **A2** (équilibre des règles) : max_t |x_t/x̄ − 1| ≤ 1e−9 sur chaque pas de P puis de L, pour B1
  à B26 et r̂*, aux trois π* ; x̄ : centre calculé par `scenarios.initial.resolution` ; grandeur
  nulle (liste déclarée, nullité calculée, `socle.est_nulle`) : max_t |x_t| ≤ 1e−12, rapportée à
  S^CB pour B19 ;
- **B1 à B26** : à π* = 2 %, moyenne de chaque bloc de 60 pas, sur P et L, dans [c − x ; c + x]
  (demi-largeurs de la table) ; égalités jugées à chaque pas (B17, B18 (i), identité et grandeurs
  nulles de B19, B26) ; centre c calculé par `scenarios/` à la table T1, jamais recopié, et son
  égalité à la colonne « valeur résolue » de `tab:criteres-j3`, à la précision de publication
  (demi-unité de la dernière décimale, règle de `comparer` du script), contrôlée ;
- **F1** : graines {0 ; 1 ; 2^63}, sans perturbation, π* = 2 %, L : trajectoire identique au bit
  (sauvegarde de chaque état, graine ramenée à 0) ;
- **C1** : 0 événement à chaque pas de L, à π* = 2 % (mesure publiée aux deux autres π*) ;
- **observation sans effet** (ADR 0014, E1) : sauvegardes identiques à l'octet, à chaque pas, sous
  la série et sous `ObservateurNul`, aux trois π*, sur 720 pas.

Les verdicts sont des résultats finaux, soumis au mainteneur, publiés tous (échecs compris) par la
fixture `publier`.
"""

import dataclasses
import math
import re
from pathlib import Path

import pytest

from nations.blocs import banque as bloc_7
from nations.blocs import production as bloc_2
from nations.etat.sauvegarde import sauvegarder
from nations.moteur import ordonnanceur as ordo
from nations.moteur.conversions import TauxDeFlux, par_pas
from nations.moteur.diagnostics import ArretMoteur, DefautDeDeclaration
from nations.moteur.parametres import varier
from nations.moteur.parametres.ensemble import PARAMETRES_DE_REFERENCE
from nations.moteur.phases import PHASES
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.noyau.diagnostics import DefautComptable
from nations.noyau.grand_livre import ClotureDePhase
from nations.observation.observateur import FinDePas, ObservateurNul
from nations.observation.serie_test_zero import (
    GRANDEURS,
    LONGUEUR_DU_BLOC,
    SUR_12_TOURS,
    SerieDuTestZero,
    ratio_au_pib_annuel,
    richesse_sur_revenu_annuel,
)
from nations.scenarios import initial

RACINE = Path(__file__).resolve().parents[2]
SPECIFICATION = RACINE / "docs" / "specification" / "nations_et_marches.tex"
POINTS_PI = (0.0, 0.02, 0.10)
PI_DES_BANDES = 0.02
NB_P, NB_L = 120, 720
GRAINE = 0
GRAINES_F1 = (0, 1, 2 ** 63)
# Seuils écrits avant l'essai (`tab:criteres-j3`).
SEUIL_A1 = 1e-9
SEUIL_A2 = 1e-9
SEUIL_NUL = 1e-12
SEUIL_EGALITE = 1e-12
# Premier pas d'une grandeur sur 12 tours (D13).
PREMIER_PAS_SUR_12_TOURS = PARAMETRES_DE_REFERENCE.cadre.pas_par_an - 1


# --------------------------------------------------------------------------
# Banc
# --------------------------------------------------------------------------


def tables(pi):
    """Tables de référence (T1, M34) à π* = `pi`."""
    return dataclasses.replace(PARAMETRES_DE_REFERENCE, banque_centrale=varier(
        PARAMETRES_DE_REFERENCE.banque_centrale, pi_etoile=pi))


def resolu(pi, graine=GRAINE):
    """État initial et tables alignées rendus par `scenarios.etat_initial`."""
    return initial.etat_initial(tables(pi), initial.NORMALISATION_DE_REFERENCE,
                                identifiant="A", graine=graine)


class Releve:
    """Observateur d'essai : par pas, montants exécutés des lignes (hors contreparties de
    règlement), variables du pas et état t + 1."""

    def __init__(self):
        self.pas = []
        self._montants = {}

    def relever(self, e):
        if type(e) is ClotureDePhase:
            for ligne, termes in e.montants:
                if not cat.LIGNE[ligne].contrepartie:
                    self._montants[ligne] = sum(x for _, x in termes)
        elif type(e) is FinDePas:
            self.pas.append({**self._montants, "t": e.t, "variables": dict(e.variables_du_pas),
                             "etat": e.etat})
            self._montants = {}


class Ensemble:
    """Observateur qui transmet chaque événement, dans l'ordre, à chacun de ses observateurs."""

    def __init__(self, *observateurs):
        self.observateurs = observateurs

    def relever(self, e):
        for o in self.observateurs:
            o.relever(e)


def derouler(socle, ei, nb_pas, observateur):
    """`nb_pas` pas du socle complet depuis l'état initial résolu `ei` ; rend les états t + 1 et,
    le cas échéant, l'arrêt du moteur (exception relevée, `None` sinon)."""
    o = ordo.assembler(PHASES, socle.blocs_du_socle_complet(), ei.parametres,
                       socle.ENTREES_DU_SOCLE)
    etats, etat = [], ei.etat
    for _ in range(nb_pas):
        try:
            etat = ordo.executer_pas(etat, socle.ENTREES_SANS_SCENARIO, o, observateur)
        except (ArretMoteur, DefautComptable) as arret:
            return etats, arret
        etats.append(etat)
    return etats, None


@pytest.fixture(scope="module")
def trajectoires(socle):
    """π* → (état initial résolu, série, relevé, arrêt) : 720 pas sans choc."""
    rendus = {}
    for pi in POINTS_PI:
        ei = resolu(pi)
        serie = SerieDuTestZero(ei.etat, pas_par_an=ei.parametres.cadre.pas_par_an,
                                r_bar=ei.parametres.banque_centrale.r_bar.valeur)
        releve = Releve()
        _, arret = derouler(socle, ei, NB_L, Ensemble(serie, releve))
        rendus[pi] = (ei, serie, releve, arret)
    return rendus


# --------------------------------------------------------------------------
# Centres : calculés par `scenarios/` (résolution aux tables, conventions de sélection)
# --------------------------------------------------------------------------


def centres(parametres):
    """Valeur résolue x̄ de chaque grandeur de `GRANDEURS`, sur la résolution de
    `scenarios.initial.resolution` aux tables `parametres` (mêmes définitions que la série)."""
    r = initial.resolution(parametres, initial.NORMALISATION_DE_REFERENCE)
    e, x, n, ou = r.etat, r.entrees, r.entrees.pas_par_an, r.ouverture
    # Grandeurs de B19 sur l'ouverture résolue, rapportées à S^CB (positions sous leur nom).
    s_cb = idt.echelle_bilan({nom: getattr(ou, nom) for nom in cat.NOMS_POSTES},
                             "banque_centrale")
    return {
        "B1": e.IN_vol / e.v, "B2": e.tu, "B3": e.U, "B4": e.WB / e.PIB, "B5": x.g_pr,
        "B6": e.p / e.UC - 1.0, "B7": e.p / r.ouverture.registre[n - 1] - 1.0, "B8": 0.0,
        "B9": e.i_CB - x.pi_etoile, "B10": richesse_sur_revenu_annuel(e.V_H, e.YD, n),
        "B11": 1.0 - e.C / e.YD, "B12": ratio_au_pib_annuel(e.p * e.K_vol, e.PIB, n),
        "B13": e.I / e.PIB, "B14": e.L / e.K, "B15": ratio_au_pib_annuel(e.D_F, e.PIB, n),
        "B16": ratio_au_pib_annuel(e.D_H + e.D_F, e.PIB, n), "B17": e.E_Bk / e.L,
        "B18 (i) ϖ_L": x.varpi_L, "B18 (i) ϖ_D": x.varpi_D,
        "B18 (ii) ϖ_L": x.varpi_L, "B18 (ii) ϖ_D": x.varpi_D,
        "B19 M^G": ratio_au_pib_annuel(e.M_G, e.PIB, n), "B19 Res (H)": ou.Res / s_cb,
        "B19 E^CB": ou.E_CB / s_cb, "B19 B_CB": ou.B_CB / s_cb,
        "B19 identité": (ou.L_CB + ou.B_CB - ou.Res - ou.M_G - ou.E_CB) / s_cb,
        "B20": ratio_au_pib_annuel(e.B_Bk, e.PIB, n),
        "B21": ratio_au_pib_annuel(e.D_c, e.PIB, n),
        "B22": (e.G + e.Tr + e.interets - e.T_H - e.T_F - e.Pi_CB) / e.PIB,
        "B24": e.g, "B25": 0.0, "B26": 0.0, "r̂*": e.r_hat,
    }


def test_centres_couvrent_les_grandeurs_de_la_serie():
    """Chaque grandeur de la série a son centre, et réciproquement."""
    assert set(centres(tables(PI_DES_BANDES))) == set(GRANDEURS)


# --------------------------------------------------------------------------
# Bandes de `tab:criteres-j3` : nature (relative, absolue, égalité par pas), demi-largeur
# --------------------------------------------------------------------------

RELATIVE, ABSOLUE, EGALITE = "rel.", "abs.", "égalité par pas"
# Ligne de la table → (clés de la série, nature, demi-largeur, seuil d'égalité) ; demi-largeur en
# fraction (1 pt = 0,01).
BANDES = {
    "B1": (("B1",), RELATIVE, 0.10), "B2": (("B2",), ABSOLUE, 0.02),
    "B3": (("B3",), ABSOLUE, 0.005), "B4": (("B4",), ABSOLUE, 0.01),
    "B5": (("B5",), ABSOLUE, 0.001), "B6": (("B6",), ABSOLUE, 0.005),
    "B7": (("B7",), ABSOLUE, 0.001), "B8": (("B8",), ABSOLUE, 0.001),
    "B9": (("B9",), ABSOLUE, 0.001), "B10": (("B10",), RELATIVE, 0.02),
    "B11": (("B11",), ABSOLUE, 0.005), "B12": (("B12",), RELATIVE, 0.10),
    "B13": (("B13",), ABSOLUE, 0.01), "B14": (("B14",), RELATIVE, 0.10),
    "B15": (("B15",), RELATIVE, 0.10), "B16": (("B16",), RELATIVE, 0.10),
    "B17": (("B17",), EGALITE, SEUIL_EGALITE),
    "B18 (i)": (("B18 (i) ϖ_L", "B18 (i) ϖ_D"), EGALITE, SEUIL_EGALITE),
    "B18 (ii)": (("B18 (ii) ϖ_L", "B18 (ii) ϖ_D"), ABSOLUE, 0.001),
    "B19": (("B19 M^G",), RELATIVE, 0.02),
    "B19 (identité, grandeurs nulles)": (("B19 Res (H)", "B19 E^CB", "B19 B_CB",
                                          "B19 identité"), EGALITE, SEUIL_EGALITE),
    "B20": (("B20",), ABSOLUE, 0.02), "B21": (("B21",), ABSOLUE, 0.02),
    "B22": (("B22",), ABSOLUE, 0.002), "B24": (("B24",), ABSOLUE, 0.001),
    "B25": (("B25",), ABSOLUE, 0.001), "B26": (("B26",), EGALITE, 0.0),
}


def test_bandes_couvrent_b1_a_b26():
    """Chaque grandeur B de la série a une bande, B23 (fusionnée dans B19) exceptée ; r̂* n'est
    jugée que par A2 (et par B25)."""
    cles = {c for cles, _, _ in BANDES.values() for c in cles}
    assert cles == set(GRANDEURS) - {"r̂*"}
    numeros = {int(re.match(r"B(\d+)", ligne).group(1)) for ligne in BANDES}
    assert numeros == set(range(1, 27)) - {23}


def juger_bande(serie, cle, c, nature, demi, nb_blocs):
    """(pire, détail, tenu) : pour une bande, le plus grand écart des moyennes des `nb_blocs`
    premiers blocs de 60 pas au centre (relatif pour « rel. ») ; pour une égalité, le plus grand
    écart absolu à chaque pas des `nb_blocs` × 60 premiers pas."""
    if nature == EGALITE:
        valeurs = [(t, x) for t, x in serie.serie(cle) if t < nb_blocs * LONGUEUR_DU_BLOC]
        pire, t = max(((abs(x - c), t) for t, x in valeurs), key=lambda p: p[0])
        return pire, f"max_t |x − c| = {pire:.2e} (pas {t})", pire <= demi
    moyennes = serie.moyennes_par_bloc(cle)[:nb_blocs]
    assert len(moyennes) == nb_blocs, cle
    if nature == RELATIVE:
        ecarts = [abs(m.moyenne / c - 1.0) for m in moyennes]
    else:
        ecarts = [abs(m.moyenne - c) for m in moyennes]
    b = max(range(nb_blocs), key=lambda i: ecarts[i])
    detail = (f"pire bloc {b + 1} (pas {moyennes[b].premier}–{moyennes[b].dernier}, "
              f"{moyennes[b].nombre} valeurs) : moyenne {moyennes[b].moyenne!r}, écart "
              f"{ecarts[b]:.2e}")
    return ecarts[b], detail, ecarts[b] <= demi


def test_bandes_b1_a_b26(trajectoires, publier):
    """B1 à B26, π* = 2 %, P (blocs 1 et 2) et L (blocs 1 à 12), côte à côte."""
    ei, serie, _, arret = trajectoires[PI_DES_BANDES]
    assert arret is None, arret
    c = centres(ei.parametres)
    lignes, non_tenues = [], []
    for ligne, (cles, nature, demi) in BANDES.items():
        for cle in cles:
            verdicts = []
            for fenetre, nb_blocs in (("P", NB_P // LONGUEUR_DU_BLOC),
                                      ("L", NB_L // LONGUEUR_DU_BLOC)):
                pire, detail, tenu = juger_bande(serie, cle, c[cle], nature, demi, nb_blocs)
                verdicts.append(f"{fenetre} : {'tenu' if tenu else 'NON TENU'}, {detail}")
                if not tenu:
                    non_tenues.append((ligne, cle, fenetre, pire))
            g = GRANDEURS[cle]
            lignes.append(f"{ligne} [{cle}] {g.definition} ({g.unite} ; {g.denominateur} ; "
                          f"{g.fenetre}) ; c = {c[cle]!r} ; {nature} ± {demi:g} — "
                          + " | ".join(verdicts))
    publier("Test zéro, bandes B1 à B26, π* = 2 %, depuis scenarios.etat_initial (#176)", [
        "verdict : " + ("NON TENU : " + repr(non_tenues) if non_tenues else
                        "B1 à B26 tenues sur P et sur L"), *lignes])
    assert not non_tenues, non_tenues


# --------------------------------------------------------------------------
# Centre égal à la colonne « valeur résolue » de `tab:criteres-j3`
# --------------------------------------------------------------------------


def _cellules_de_la_table_j3():
    """Ligne B de `tab:criteres-j3` → cellule « Valeur résolue ; seuil », lues dans la source."""
    texte = SPECIFICATION.read_text(encoding="utf-8")
    debut = texte.index(r"\label{tab:criteres-j3}")
    corps = texte[debut:texte.index(r"\end{longtable}", debut)]
    cellules = {}
    for ligne in corps.splitlines():
        m = re.match(r"(B\d+) & ", ligne)
        if m:
            cellules[m.group(1)] = [c.strip() for c in ligne.split(" & ")][3]
    return cellules


def _sans_barre(texte):
    """Texte d'une cellule sans ses valeurs barrées (`\\barre{…}`, accolades équilibrées)."""
    while (i := texte.find(r"\barre{")) >= 0:
        j, profondeur = i + len(r"\barre{"), 1
        while profondeur:
            profondeur += {"{": 1, "}": -1}.get(texte[j], 0)
            j += 1
        texte = texte[:i] + texte[j:]
    return texte


def _nombres(texte):
    """Nombres écrits à la française dans un texte LaTeX (« 0{,}15 » et « 0,15 »)."""
    return re.findall(r"\d+(?:,\d+)?", texte.replace("{,}", ","))


# Ligne B → (clés de la série, facteur d'unité de la publication) ; « % » et « pt » : × 100. B26
# publie « 0 exactement » ; B18 publie (ii) « 2 et 1 pt » ; B19 et B17 leur première valeur.
PUBLICATION = {
    "B1": (("B1",), 1), "B2": (("B2",), 1), "B3": (("B3",), 100), "B4": (("B4",), 1),
    "B5": (("B5",), 100), "B6": (("B6",), 1), "B7": (("B7",), 100), "B8": (("B8",), 100),
    "B9": (("B9",), 100), "B10": (("B10",), 1), "B11": (("B11",), 100), "B12": (("B12",), 1),
    "B13": (("B13",), 100), "B14": (("B14",), 1), "B15": (("B15",), 1), "B16": (("B16",), 1),
    "B17": (("B17",), 1), "B18": (("B18 (ii) ϖ_L", "B18 (ii) ϖ_D"), 100),
    "B19": (("B19 M^G",), 1), "B20": (("B20",), 1), "B21": (("B21",), 1),
    "B22": (("B22",), 100), "B24": (("B24",), 100), "B25": (("B25",), 100),
    "B26": (("B26",), 100),
}


def _cellules_a_de_la_table_j3():
    """Lignes A1 et A2 de `tab:criteres-j3` → cellule « Valeur résolue ; seuil »."""
    texte = SPECIFICATION.read_text(encoding="utf-8")
    debut = texte.index(r"\label{tab:criteres-j3}")
    corps = texte[debut:texte.index(r"\end{longtable}", debut)]
    return {m.group(1): [c.strip() for c in ligne.split(" & ")][3]
            for ligne in corps.splitlines() if (m := re.match(r"(A\d) & ", ligne))}


def _decimal(texte):
    """Nombre écrit à la française dans une cellule LaTeX (« 0{,}02 » → 0,02)."""
    return float(texte.replace("{,}", ",").replace(",", "."))


def _puissance_de_dix(texte):
    """Valeur de la première puissance de dix « 10^{-n} » d'un texte, ou `None`."""
    m = re.search(r"10\^\{-(\d+)\}", texte)
    return None if m is None else 10.0 ** -int(m.group(1))


def bande_publiee(texte):
    """(nature, demi-largeur en fraction) lue dans une cellule « valeur ; seuil » : « ±x % rel. »
    → relative x/100 ; « ±x pt » → absolue x/100 ; « ±x année » ou « ±x » nu → absolue x ;
    sinon « 10^{-n} … près » → égalité par pas à 10^{-n} ; « exactement » → égalité exacte."""
    m = re.search(r"\\pm ([\d{},]+)(\\,\\%)?\$\s*(rel\.|pt|année)?", texte)
    if m is not None:
        x = _decimal(m.group(1))
        if m.group(3) == "rel.":
            assert m.group(2), texte
            return RELATIVE, x / 100
        if m.group(3) == "pt":
            return ABSOLUE, x / 100
        return ABSOLUE, x
    if (x := _puissance_de_dix(texte)) is not None:
        return EGALITE, x
    if "exactement" in texte:
        return EGALITE, 0.0
    raise AssertionError(f"seuil illisible : {texte}")


def test_bandes_et_seuils_lus_dans_la_table():
    """Natures et demi-largeurs de `BANDES`, seuils d'A1, d'A2 et des égalités : égaux à ceux de
    la cellule « valeur ; seuil » de `tab:criteres-j3`, lus dans la source (jamais recopiés sans
    contrôle). B18 se lit en (i) et (ii), B19 en ratio puis identité et grandeurs nulles."""
    cellules = {ligne: _sans_barre(c) for ligne, c in _cellules_de_la_table_j3().items()}
    lues = {}
    for ligne in BANDES:
        numero = ligne.split()[0]
        texte = cellules[numero]
        if ligne == "B18 (i)":
            texte = texte.split("(ii)")[0]
        elif ligne == "B18 (ii)":
            texte = texte.split("(ii)")[1]
        elif ligne == "B19":
            texte = texte.split("identité")[0]
        elif ligne.startswith("B19 ("):
            texte = texte.split("identité")[1]
        lues[ligne] = bande_publiee(texte)
    attendues = {ligne: (nature, demi) for ligne, (_, nature, demi) in BANDES.items()}
    assert {k: (n, round(x, 15)) for k, (n, x) in lues.items()} == {
        k: (n, round(x, 15)) for k, (n, x) in attendues.items()}
    assert lues["B17"] == (EGALITE, SEUIL_EGALITE)
    a = _cellules_a_de_la_table_j3()
    assert _puissance_de_dix(a["A1"]) == SEUIL_A1 and "rel." in a["A1"]
    seuil_a2, nulles_a2 = a["A2"].split(";")
    assert _puissance_de_dix(seuil_a2) == SEUIL_A2
    assert _puissance_de_dix(nulles_a2) == SEUIL_NUL


def test_centres_egaux_a_la_colonne_publiee(socle, publier):
    """Centre c (scenarios, table T1, π* = 2 %) égal à la valeur résolue publiée, à la demi-unité
    de sa dernière décimale (`comparer` du script, décision du 05/10/2026, point 2)."""
    es = socle.script()
    c = centres(tables(PI_DES_BANDES))
    cellules = _cellules_de_la_table_j3()
    assert set(cellules) == {f"B{k}" for k in range(1, 27)}
    lignes, ecarts = [], []
    for ligne, (cles, facteur) in PUBLICATION.items():
        texte = _sans_barre(cellules[ligne])
        if ligne == "B18":
            publiees = _nombres(texte.split("(ii)")[1])[:2]
        else:
            publiees = _nombres(texte.split(";")[0])[:1]
        assert len(publiees) == len(cles), (ligne, texte)
        for cle, publie in zip(cles, publiees, strict=True):
            ecart, seuil, egal = es.comparer(publie, facteur * c[cle])
            lignes.append(f"{ligne} [{cle}] : publiée {publie}, centre × {facteur} = "
                          f"{facteur * c[cle]!r}, écart {ecart:.1e}, seuil {seuil:.1e} : "
                          + ("égal" if egal else "ÉCART"))
            if not egal:
                ecarts.append((ligne, cle, publie, facteur * c[cle]))
    publier("Test zéro, centres des bandes contre tab:criteres-j3 (#176)", [
        "verdict : " + ("ÉCART : " + repr(ecarts) if ecarts else
                        "égaux à la précision de publication"), *lignes])
    assert not ecarts, ecarts


# --------------------------------------------------------------------------
# A2 : stationnarité exacte
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", POINTS_PI)
def test_a2_stationnarite_exacte(trajectoires, socle, pi, publier):
    """A2 : max_t |x_t/x̄ − 1| ≤ 1e−9 sur chaque pas de P, puis de L ; grandeur nulle (nullité
    calculée, `socle.est_nulle`) : max_t |x_t| ≤ 1e−12 (S^CB pour B19, déjà dans la série)."""
    ei, serie, _, arret = trajectoires[pi]
    assert arret is None, arret
    c = centres(ei.parametres)
    sentier = socle.sentier(pi)
    nulles = {cle for cle in GRANDEURS if socle.est_nulle(cle, ei.parametres, sentier)}
    assert {cle for cle, x in c.items() if x == 0.0} <= nulles
    lignes, hors = [], []
    for cle in GRANDEURS:
        mesures = []
        for fenetre, nb in (("P", NB_P), ("L", NB_L)):
            valeurs = [(t, x) for t, x in serie.serie(cle) if t < nb]
            premier = PREMIER_PAS_SUR_12_TOURS if cle in SUR_12_TOURS else 0
            assert valeurs[0][0] == premier and valeurs[-1][0] == nb - 1, cle
            if cle in nulles:
                pire, t = serie.ecart_absolu_maximal(cle, 0.0, avant=nb)
                seuil = SEUIL_NUL
            else:
                pire, t = serie.ecart_relatif_maximal(cle, c[cle], avant=nb)
                seuil = SEUIL_A2
            mesures.append(f"{fenetre} : {pire:.1e} (pas {t})")
            if pire > seuil:
                hors.append((cle, fenetre, pire))
        lignes.append(f"{cle} : " + ("nulle, max |x|" if cle in nulles else "max |x/x̄ − 1|")
                      + f", x̄ = {c[cle]!r} — " + " | ".join(mesures))
    publier(f"Test zéro, A2 (stationnarité exacte), π* = {100 * pi:g} %, P et L (#176)", [
        "verdict : " + ("NON TENU : " + repr(hors) if hors else "tenu")
        + " ; seuils 1e−9 relatif, 1e−12 pour une grandeur nulle (S^CB pour B19)", *lignes])
    assert not hors, hors


# --------------------------------------------------------------------------
# A1 : transcription
# --------------------------------------------------------------------------


def _valeur_du_moteur(cle, nu_G, ei, releve):
    """Valeur côté moteur d'une ligne de `tab:etat-stationnaire`, dans l'unité du script : stock
    sur l'`EtatPays` et les tables de `scenarios/`, flux sur le pas 0 exécuté. Rend
    `(valeur, lecture)` ; `None` pour une ligne que les tables du moteur refusent."""
    o, p, n = ei.etat, ei.parametres, ei.parametres.cadre.pas_par_an
    if nu_G != p.finances_publiques.nu_G:
        return None
    q = releve.pas[0]
    v = q["variables"]
    pib = q["1"] + q["2"] + q["3"] + q["4"]
    positions = {nom: getattr(o, nom) for nom in cat.NOMS_POSTES}
    B = o.B_H + o.B_Bk + o.B_CB
    e_cb = idt.valeur_nette_stock(positions, "banque_centrale")
    if cle == "dette_brute_affichee":
        # Restitution : stock de clôture du pas 11 sur la somme des PIB des pas 0 à 11.
        clos = releve.pas[n - 1]["etat"]
        somme = math.fsum(r["1"] + r["2"] + r["3"] + r["4"] for r in releve.pas[:n])
        return (100 * (clos.B_H + clos.B_Bk + clos.B_CB) / somme,
                ("lue au pas 11, non à t = 0 : B de clôture du pas 11 sur la somme des PIB des "
                 "pas 0 à 11 (les 12 PIB antérieurs à t = 0 n'existent pas sur le moteur) ; "
                 "dépend donc de la stationnarité des pas 0 à 11 (A2)"))
    formules = {
        "K_vol_sur_y": (ratio_au_pib_annuel(o.K_vol, v["y"], n), "K^vol (état) ; y (pas 0)"),
        "K_courant": (ratio_au_pib_annuel(v["p"] * o.K_vol, pib, n),
                      "K^vol (état) ; p, PIB (pas 0)"),
        "K_comptable": (ratio_au_pib_annuel(o.K, pib, n), "K (état) ; PIB (pas 0)"),
        "part_salariale": (q["5"] / pib, "WB/PIB du pas 0"),
        "rbar": (100 * p.banque_centrale.r_bar.valeur, "r̄ (table)"),
        "i_CB": (100 * v["i_CB"], "i_CB (pas 0)"),
        "r_restitue": (100 * (v["i_CB"] - o.pi_etoile), "i_CB (pas 0) − π* (état)"),
        "rho_L": (100 * o.varrho_bar_L, "ϱ̄_L (état)"),
        "glissement": (100 * (o.registre_prix[0] / o.registre_prix[n] - 1.0),
                       "P_{−1}/P_{−13} − 1 (registre de l'état)"),
        "hausse_prix_pas": (100 * (o.registre_prix[0] / o.registre_prix[1] - 1.0),
                            "P_{−1}/P_{−2} − 1 (registre de l'état)"),
        "theta_G": (p.finances_publiques.theta_G, "θ_G (table alignée)"),
        "I_sur_PIB": (100 * q["3"] / pib, "I/PIB du pas 0"),
        "masse_monetaire": (ratio_au_pib_annuel(o.D_H + o.D_F, pib, n),
                            "D_H + D_F (état) ; PIB (pas 0)"),
        "dette_consolidee": (ratio_au_pib_annuel(B - o.M_G - e_cb, pib, n),
                             "B − M^G − E^CB (état) ; PIB (pas 0)"),
        "dette_brute": (ratio_au_pib_annuel(B, pib, n), "B (état) ; PIB (pas 0)"),
        "deficit_i": (100 * (q["2"] + q["6"] + q["11a"] + q["11b"] + q["11c"] - q["7"]
                             - q["16"]) / pib, "lignes 2, 6, 11a à 11c, 7, 16 du pas 0"),
        "primaire": (100 * (q["7"] - q["2"] - q["6"]) / pib, "lignes 7, 2, 6 du pas 0"),
    }
    return formules[cle]


@pytest.mark.parametrize("pi", POINTS_PI)
def test_a1_transcription(trajectoires, socle, pi, publier):
    """A1 : chaque valeur de `tab:etat-stationnaire`, script contre moteur, ≤ 1e−9 relatif à
    t = 0 ; valeur du script nulle : moteur égal au bit (écart relatif non défini). La ligne
    « dette brute, ν_G = 1 » est hors du domaine de la table (ν_G > 1) : publiée non évaluable,
    le refus de la table étant vérifié."""
    es = socle.script()
    calc = es.Calculs(es.Parametres())
    ei, _, releve, arret = trajectoires[pi]
    assert arret is None, arret
    lignes, hors, non_evaluees = [], [], []
    for nom, cle, nu, _, _ in es._TAB_ETAT:
        script = calc.v(pi=pi, nu=nu)[cle]
        moteur = _valeur_du_moteur(cle, nu, ei, releve)
        if moteur is None:
            with pytest.raises(DefautDeDeclaration):
                varier(ei.parametres.finances_publiques, nu_G=nu)
            non_evaluees.append(nom)
            lignes.append(f"{nom} : script {script!r} ; NON ÉVALUABLE sur le moteur "
                          f"(ν_G = {nu:g} refusé par la table, domaine ν_G > 1)")
            continue
        valeur, lecture = moteur
        if script == 0.0:
            ecart, tenu = abs(valeur), valeur == 0.0
            mesure = f"écart absolu {ecart:.1e} (script nul : égalité au bit)"
        else:
            ecart = abs(valeur / script - 1.0)
            tenu = ecart <= SEUIL_A1
            mesure = f"écart relatif {ecart:.1e}"
        lignes.append(f"{nom} : script {script!r} ; moteur {valeur!r} [{lecture}] ; {mesure} : "
                      + ("tenu" if tenu else "NON TENU"))
        if not tenu:
            hors.append((nom, script, valeur))
    publier(f"Test zéro, A1 (transcription), π* = {100 * pi:g} %, t = 0 (#176)", [
        "verdict : " + ("NON TENU : " + repr(hors) if hors else "tenu")
        + f" sur {len(es._TAB_ETAT) - len(non_evaluees)} lignes sur {len(es._TAB_ETAT)} ; "
        + (f"la 19e ({non_evaluees[0]}) non évaluable par construction (ν_G = 1 hors du domaine de "
           "la table)" if non_evaluees else "toutes évaluées")
        + " ; « dette brute affichée » lue au pas 11 et dépendante d'A2 (décisions du "
        "mainteneur du 26/11/2026)", *lignes])
    assert not hors, hors


# --------------------------------------------------------------------------
# C1 : aucune crise
# --------------------------------------------------------------------------


def _regime(etat):
    """Régime de la banque : refinancement (L^CB > 0), réserves (Res > 0), les deux ou aucun."""
    return (etat.L_CB > 0.0, etat.Res > 0.0)


# Catégories de C1 (`tab:criteres-j3`), dans l'ordre de publication.
CATEGORIES_C1 = (
    "demande non servie, rationnement des biens (N6 : v < d)",
    "plan des ménages, rationnement de la caisse (H5 : C^plan ≠ C^règle)",
    "plafond de E1, rationnement de la caisse (G^plan ≠ G^visé)",
    "plafond de E6 (Tr ≠ Tr^lev)",
    "part non payée (E13 : transferts non versés ou perte non couverte)",
    "plancher du dividende de la banque actif (B6)",
    "changement de régime entre réserves et refinancement",
    "N ≤ N^pa active (T4 : N = N^pa)",
    "y* ≥ 0 active (N3 : y* = 0)",
    "arrêt du noyau ou du moteur",
)


def evenements_c1(ei, releve, arret):
    """Événements de C1 par catégorie (`CATEGORIES_C1`) : [(t, détail)], lus sur les variables du
    pas, les montants exécutés, l'état d'ouverture et l'état t + 1, et la table ϑ du bloc 7 ;
    formes des blocs (N3, N6, T4, H5, E1, E6, E13, B6) réévaluées sur les mêmes opérandes ;
    `arret` : exception du moteur relevée pendant le déroulement, ou `None`."""
    vartheta = ei.parametres.banque.vartheta
    ev = {k: [] for k in CATEGORIES_C1}
    noms = CATEGORIES_C1
    ouverture = ei.etat
    for q in releve.pas:
        t, v, e = q["t"], q["variables"], q["etat"]
        p = v["p"]
        d = bloc_2.demande_adressee(v["C_plan"] / p, v["I_plan"] / p, v["G_plan"] / p)
        if v["v"] < d:
            ev[noms[0]].append((t, f"v = {v['v']!r} < d = {d!r}"))
        if v["C_plan"] != v["C_regle"]:
            ev[noms[1]].append((t, f"C^plan = {v['C_plan']!r}, C^règle = {v['C_regle']!r}"))
        if v["G_plan"] != v["G_vise"]:
            ev[noms[2]].append((t, f"G^plan = {v['G_plan']!r}, G^visé = {v['G_vise']!r}"))
        if v["Tr"] != v["Tr_lev"]:
            ev[noms[3]].append((t, f"Tr = {v['Tr']!r}, Tr^lev = {v['Tr_lev']!r}"))
        if v["Tr_non_verses"] != 0.0 or v["perte_non_couverte"] != 0.0:
            ev[noms[4]].append((t, f"{v['Tr_non_verses']!r}, {v['perte_non_couverte']!r}"))
        o = ouverture
        E_Bk = bloc_7.fonds_propres(o.L, o.B_Bk, o.Res, o.D_H, o.D_F, o.L_CB)
        argument = E_Bk + v["Pi_Bk"] - vartheta * (o.L + q["18"])
        if argument < 0.0:
            ev[noms[5]].append((t, f"E^Bk + Π^Bk − ϑ L_(t+1) = {argument!r}"))
        if _regime(e) != _regime(o):
            ev[noms[6]].append((t, f"{_regime(o)} → {_regime(e)}"))
        if v["N_suivant"] >= o.N_pa:
            ev[noms[7]].append((t, f"N = {v['N_suivant']!r}, N^pa = {o.N_pa!r}"))
        if v["y_etoile"] <= 0.0:
            ev[noms[8]].append((t, f"y* = {v['y_etoile']!r}"))
        ouverture = e
    if arret is not None:
        ev[noms[9]].append((len(releve.pas), repr(arret)))
    return ev


def activations_sans_verdict(releve, ouverture):
    """Réserve R2 de `monnaie` (mesure publiée, sans verdict) : par pas, activation du plancher de
    F3 (argument de Div_F, recalculé sur les opérandes de la phase 6 du bloc 6, négatif) et de la
    lecture en max(0 ; ·) des dépôts d'ouverture (D_H < 0 ou D_F < 0 : ligne 10 et Π^Bk, B4 et
    B5)."""
    plancher_f3, depots = [], []
    for q in releve.pas:
        t, v, o = q["t"], q["variables"], ouverture
        D_F_net = max(0.0, o.D_F)
        argument = (D_F_net + q["18"] + q["1"] + q["2"] - q["5"]
                    - par_pas(TauxDeFlux(o.i_L)) * o.L + par_pas(TauxDeFlux(o.i_D)) * D_F_net
                    - v["T_e_F"] - v["D_etoile_F"])
        if argument < 0.0:
            plancher_f3.append((t, argument))
        else:  # recalcul fidèle : égal au bit à la ligne 14 exécutée (mesuré sur 24 pas)
            assert argument == q["14"], (t, argument, q["14"])
        if o.D_H < 0.0 or o.D_F < 0.0:
            depots.append((t, (o.D_H, o.D_F)))
        ouverture = q["etat"]
    return {"plancher de F3 actif (Div_F ≥ 0)": plancher_f3,
            "max(0 ; ·) des dépôts actif (ligne 10, Π^Bk : D_H < 0 ou D_F < 0)": depots}


@pytest.mark.parametrize("pi", POINTS_PI)
def test_c1_aucune_crise(trajectoires, pi, publier):
    """C1 : 0 événement à chaque pas de L, verdict à π* = 2 % seulement (décision du mainteneur
    du 26/11/2026) ; nombre publié aux trois π*. Publiées sans verdict (R2 de `monnaie`) : les
    activations du plancher de F3 et du max(0 ; ·) des dépôts."""
    ei, _, releve, arret = trajectoires[pi]
    ev = evenements_c1(ei, releve, arret)
    total = sum(len(x) for x in ev.values())
    jugee = pi == PI_DES_BANDES
    publier(f"Test zéro, C1 (aucune crise), π* = {100 * pi:g} %, {len(releve.pas)} pas de L "
            f"(#176)", [
        ("verdict : " + ("tenu" if total == 0 else "NON TENU") if jugee
         else "mesure publiée, sans verdict (C1 jugé à π* = 2 %)")
        + f" ; {total} événement(s) ; nombre d'événements, chaque pas de L",
        *(f"{nom} : {len(x)}" + (f", premier au pas {x[0][0]} ({x[0][1]})" if x else "")
          for nom, x in ev.items()),
        *(f"sans verdict (R2 de monnaie) — {nom} : {len(x)} pas"
          + (f", premier au pas {x[0][0]} ({x[0][1]!r})" if x else "")
          for nom, x in activations_sans_verdict(releve, ei.etat).items())])
    assert len(releve.pas) == NB_L
    if jugee:
        assert total == 0, {k: x[:3] for k, x in ev.items() if x}


class _ReleveConstruit:
    """Relevé d'essai construit à la main (`pas` : liste de pas au format de `Releve`)."""

    def __init__(self, pas):
        self.pas = pas


def test_c1_compte_un_evenement_par_categorie(trajectoires):
    """Sur un relevé construit à partir du pas 0 stationnaire (π* = 2 %), une perturbation par
    pas, chacune d'une seule catégorie, plus un arrêt : chaque catégorie compte exactement un
    événement, au pas perturbé. Le pas « N6 » sert 90 % de la demande (un critère relâché à
    v < 0,5 d ne le compterait pas)."""
    ei, _, releve, _ = trajectoires[PI_DES_BANDES]
    base = releve.pas[0]
    v0 = base["variables"]
    p = v0["p"]
    d = bloc_2.demande_adressee(v0["C_plan"] / p, v0["I_plan"] / p, v0["G_plan"] / p)
    assert v0["v"] == d  # pas de base sans événement (vérifié aussi ci-dessous)
    perturbations = [
        {"v": 0.9 * d},
        {"C_regle": v0["C_regle"] * 1.01},
        {"G_vise": v0["G_vise"] * 1.01},
        {"Tr_lev": 1e-3},
        {"Tr_non_verses": 1e-3},
        {"Pi_Bk": -1e3},
        None,  # régime : état t + 1 en réserves, au dernier pas
        {"N_suivant": ei.etat.N_pa},
        {"y_etoile": 0.0},
    ]
    pas = [{**base, "t": 0, "variables": dict(v0)}]
    for k, modif in enumerate(perturbations, start=1):
        if modif is None:
            continue
        pas.append({**base, "t": k, "variables": {**v0, **modif}})
    k_regime = len(perturbations) + 1
    etat_reserves = dataclasses.replace(base["etat"], Res=1.0, L_CB=0.0)
    pas.append({**base, "t": k_regime, "variables": dict(v0), "etat": etat_reserves})
    ev = evenements_c1(ei, _ReleveConstruit(pas), RuntimeError("arrêt d'essai"))
    attendus = {nom: [k] for k, nom in enumerate(CATEGORIES_C1[:9], start=1)}
    attendus[CATEGORIES_C1[6]] = [k_regime]
    attendus[CATEGORIES_C1[9]] = [len(pas)]
    assert {nom: [t for t, _ in x] for nom, x in ev.items()} == attendus


# --------------------------------------------------------------------------
# F1 : indépendance à la graine
# --------------------------------------------------------------------------


def test_f1_independance_a_la_graine(socle, publier):
    """F1 : graines {0 ; 1 ; 2^63}, π* = 2 %, 720 pas : sauvegardes de chaque état identiques à
    l'octet, la graine (champ d'identité) ramenée à 0."""
    documents = {}
    for graine in GRAINES_F1:
        ei = resolu(PI_DES_BANDES, graine)
        etats, arret = derouler(socle, ei, NB_L, ObservateurNul())
        assert arret is None, arret
        assert all(e.graine == graine for e in etats)
        documents[graine] = [sauvegarder([dataclasses.replace(e, graine=0)]) for e in etats]
    differents = [(g, next(t for t, (a, b) in enumerate(zip(documents[0], documents[g],
                                                             strict=True)) if a != b))
                  for g in GRAINES_F1[1:] if documents[g] != documents[0]]
    publier("Test zéro, F1 (indépendance à la graine), π* = 2 %, L (#176)", [
        "verdict : " + ("NON TENU, premier pas différent : " + repr(differents) if differents
                        else "tenu") + " ; graines 0, 1, 2^63 ; trajectoire (sauvegarde de "
        "chaque état, graine ramenée à 0) identique au bit sur 720 pas"])
    assert not differents


# --------------------------------------------------------------------------
# Observation sans effet ; propriétés de la série
# --------------------------------------------------------------------------


@pytest.mark.parametrize("pi", POINTS_PI)
def test_observation_sans_effet(socle, pi):
    """ADR 0014, E1 : sauvegardes identiques à l'octet, à chaque pas de 720, sous la série du test
    zéro et sous `ObservateurNul`."""
    ei = resolu(pi)
    serie = SerieDuTestZero(ei.etat, pas_par_an=ei.parametres.cadre.pas_par_an,
                            r_bar=ei.parametres.banque_centrale.r_bar.valeur)
    sous_serie, arret = derouler(socle, ei, NB_L, serie)
    assert arret is None
    sous_nul, arret = derouler(socle, ei, NB_L, ObservateurNul())
    assert arret is None
    assert [sauvegarder([e]) for e in sous_serie] == [sauvegarder([e]) for e in sous_nul]
    assert serie.pas() == tuple(range(NB_L))


def test_moyennes_par_bloc_et_premier_pas_des_douze_tours(trajectoires):
    """Blocs complets de 60 pas depuis le premier pas relevé ; une grandeur sur 12 tours compte
    49 valeurs au premier bloc (pas 11 à 59), 60 ensuite ; moyenne = fsum des valeurs / nombre."""
    _, serie, _, _ = trajectoires[PI_DES_BANDES]
    for cle in ("B1", "B4"):
        moyennes = serie.moyennes_par_bloc(cle)
        assert [(m.premier, m.dernier) for m in moyennes] == [
            (60 * b, 60 * b + 59) for b in range(12)]
        assert [m.nombre for m in moyennes] == [49 if cle == "B4" else 60] + [60] * 11
        valeurs = [x for t, x in serie.serie(cle) if 60 <= t < 120]
        assert moyennes[1].moyenne == math.fsum(valeurs) / 60
    assert len(serie.moyennes_par_bloc("B1", longueur=700)) == 1


def test_serie_refuse_un_evenement_inconnu_et_une_ligne_non_executee():
    """La série refuse un événement inconnu et une fin de pas sans les lignes qu'elle lit."""
    ei = resolu(PI_DES_BANDES)
    serie = SerieDuTestZero(ei.etat, pas_par_an=12, r_bar=0.01)
    with pytest.raises(TypeError):
        serie.relever(object())
    with pytest.raises(ValueError, match="lignes non exécutées"):
        serie.relever(FinDePas(0, ei.etat, (), ()))
    with pytest.raises(TypeError):
        SerieDuTestZero(object(), pas_par_an=12, r_bar=0.01)


def test_ratio_au_pib_annuel():
    """eq:observation-ratio-pib-annuel : stock rapporté à n_a fois le flux du pas."""
    assert ratio_au_pib_annuel(24.0, 1.0, 12) == 2.0
    assert ratio_au_pib_annuel(6.0, 0.5, 12) == 1.0
