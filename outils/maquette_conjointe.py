"""Maquette linéarisée de la boucle conjointe des blocs 2 à 9 : rayons et périodes cités (issue #65).

Contrat : issue #65 et son amendement du 05/10/2026 (P23 (a) : blocs 2 à 9,
une seule maquette conjointe, linéarisée autour de l'état stationnaire de
`outils/etat_stationnaire.py`). Pour chaque rayon spectral, période, demi-vie
et frontière de stabilité que la spécification
(`docs/specification/nations_et_marches.tex`) cite pour une boucle conjointe,
le script rend la valeur publiée, la valeur remesurée, l'écart et les lignes
de la spécification où le chiffre est écrit.

**Indépendance.** Le script n'importe ni `src/` ni `archive/`. Les cartes
d'un pas sont écrites depuis les règles des encadrés de la spécification,
repérées par leur identifiant (N1 à N11, T1 à T6, P1 à P4, H2 à H7, S1 à S7,
F1 à F4, B1 à B7, BC1 à BC9, E1 à E13) ; seuls l'état stationnaire du socle
complet, les paramètres de la table de calibration et la règle de
comparaison aux valeurs publiées viennent de `outils/etat_stationnaire.py`.
La carte du socle est une seconde transcription des règles, indépendante de
`etat_stationnaire.un_pas` : un test vérifie que les deux rendent la même
clôture depuis l'état initial résolu.

**Méthode.** Chaque maquette est une carte d'un pas x_t ↦ x_{t+1} sur les
variables d'état d'ouverture, évaluée au pas 0 depuis l'état stationnaire.
Les grandeurs qui croissent sur le sentier sont ramenées à la tendance : une
grandeur en u.m. est divisée par Γ̄ = [(1 + g)(1 + π̄)]^{1/n_a}, un volume
par (1 + g)^{1/n_a}, un prix par (1 + π̄)^{1/n_a} (un logarithme est diminué
du logarithme du facteur) ; les taux, les parts et le chômage ne le sont
pas. L'état stationnaire est alors un point fixe de la carte détendue, ce
que le script contrôle (résidu publié). La jacobienne est calculée par
différences finies centrées, pas relatif `PAS_RELATIF` = 1e−6 de l'échelle
de chaque variable (son module, avec un plancher par famille : PIB du pas
pour les montants, production pour les volumes, 0,01 pour les taux), puis
mise à l'échelle (S⁻¹ J S, mêmes valeurs propres). Le rayon spectral est le
plus grand module des valeurs propres, hors de la racine nominale quand la
maquette la porte (une valeur propre telle que |λ − 1| ≤ 1e−8,
`sec:prix-conditions`), exclue une fois et contrôlée. La période d'une
racine complexe est 2π/|arg λ| tours ; la demi-vie d'une racine de module
inférieur à 1 est ln 0,5/ln |λ| tours. Une frontière de stabilité est
cherchée par bissection déterministe (`ITERATIONS_BISSECTION` pas) sur un
intervalle encadrant déclaré, le rayon y changeant de côté de 1 une seule
fois (contrôlé aux bornes). Coude de la règle d'emploi T4 : à l'état
stationnaire, N* égale la rétention, et les deux régimes de l'emploi sont
linéarisés séparément (hausse : N = N* ; baisse : N = rétention), comme le
fait la spécification ; N ≥ N* donne y = y* dans les deux (N5). Les autres
bornes (min et max) sont inactives à l'état stationnaire et gardées telles
quelles dans les cartes, sauf le plancher de B6 dans la configuration
« fiche » des variantes de F (deux branches, ci-dessous) ; un coude franchi
se lit sur l'écart des jacobiennes avant et arrière (`TOL_COUDE`).

**Maquettes.** Les chiffres cités ont été mesurés sur des maquettes dont les
hypothèses sont écrites dans le paragraphe qui les cite ; chaque relevé
nomme la sienne, et les paragraphes où il est cité (`Chiffre.ou`) ; une
valeur barrée (`\\barre`) n'est plus un chiffre publié (`sans_barres`) :
- `offre` : production N1 à N7, emploi égal à la demande de travail, demande
  d_t = A + m y_{t−1} (`sec:travail-conditions`) ; avec la règle de prix P1
  à P3 à coût unitaire exogène, plans en u.m. au prix du pas précédent
  prolongé de la cible (`sec:prix-conditions`) ; avec les règles de salaire
  T2 et T3, anticipation exogène égale à π̄ (boucle salaires -- prix) ;
- `investissement` : N1 à N7, S3 et S6, demande A + m y_{t−1} + I^{vol,plan},
  prix et taux exogènes (`sec:investissement-conditions`) ;
- `menages` : N1 à N7, T2 à T4 (deux régimes), P1 à P3, H2 à H6,
  anticipation exogène égale à π̄, dépense autonome en u.m. au prix du pas
  précédent prolongé de la cible, sans impôts ni transferts, i_D = 3 %
  (`sec:menages-conditions`, `sec:menages-inflation`, instabilité 17) ;
- `socle` : blocs 2 à 9 complets, linéarisés autour de l'état initial résolu
  d'`etat_stationnaire.etat_stationnaire` à ν_G = `NU_G` (valeur retenue),
  sous la règle budgétaire de référence (φ = 1)
  (`sec:banque_centrale-conditions`, `sec:finances_publiques-conditions`).
  E^CB et E^Bk y sont des états clos par les flux : la carte porte des
  directions qui violent les identités de bilan (`IDENTITES_SOCLE`), dont
  les gradients sont vecteurs propres à gauche de valeur propre 1/Γ̄. Le
  rayon relevé est la lecture (c), retenue par le mainteneur le 15/10/2026 :
  rayon sur la variété des identités, hors de la racine nominale et des
  racines en 1/Γ̄ des stocks tenus en niveau (E^CB, B_CB : ligne de la
  jacobienne égale à e_i/Γ̄), déclarées avec leur multiplicité et leur
  cause ; le rayon brut et celui de la variété sont publiés à côté
  (`lectures`). La grille du socle est la grille G de
  `docs/blocs/banque_centrale.md` (l. 340-345), écart déclaré en
  `ABSENTS_GRILLE`, augmentée de ζ ×0,5 et ×2 (`AJOUTS_GRILLE`, verdicts
  publiés sur les deux grilles) ; la marge conjointe de β, a_π et η_r
  (facteur commun à la frontière) et la couverture φ de E4 (φ*, table φ)
  sont mesurées sur la même carte ;
- `socle`, variantes écartées de F (fiche 6, § 3.N ; `sec:ecartees`) :
  seconde écriture, indépendante de `outils/contre_epreuve_financement.py`
  (#66), depuis les définitions de la fiche ; configurations « socle » et
  « fiche » (i_L = i_D = 3 %, ϑ = 0, τ_H = τ_F = 0), taux directeur selon
  BC1 ou tenu (avec ou sans π^e ancré), deux régimes de T4, λ_ti de base et
  ×2 ; les variantes sont les quatre écritures du levier sur p K^vol, les
  dépôts sur les ventes du pas et leur combinaison (`FINANCEMENTS`). L'état stationnaire d'une variante est celui d'`etat_stationnaire` au
  levier comptable (ou à ν_F) qui donne la cible de la variante
  (`parametres_etat`). Dans « fiche », B6 est à son coude (E^Bk = Π^Bk = 0) :
  ses deux branches sont linéarisées séparément, comme les deux régimes de
  T4, et l'écart des jacobiennes avant et arrière est publié pour chaque
  carte (`ecart_avant_arriere`).

Hypothèses de maquette que la spécification ne définit pas, déclarées
(questions à l'expert pilote dans le compte rendu de #65) :
- θ_H = 1 (« résultat courant des entreprises versé dans le pas ») se lit
  YD = p v + UC (y − v) + i_D V_H/n_a, stock valorisé au coût unitaire du
  pas ; la lecture au coût moyen pondéré de N8 est publiée à côté ;
- la lecture (a) (« glissement mesuré dans le terme d'entretien ») lit le
  glissement π_{t−1} dans γ^e et donc aussi dans Γ^e = 1 + γ^e de H2 ; la
  lecture de l'entretien seul est publiée à côté.

Usage : `uv run python outils/maquette_conjointe.py [--json FICHIER]`.
Codes de sortie : 0 si chaque carte tient son point fixe (résidu ≤
`TOL_POINT_FIXE` ; au socle, sur chaque carte de `cas_controles`), chaque
racine nominale attendue est trouvée, la variété
des identités est invariante (≤ `TOL_GAUCHE`, socle et variantes), aucun
coude n'est franchi par les différences finies (≤ `TOL_COUDE`) et les
racines en 1/Γ̄ de la variété sont celles des stocks `TENUS_ATTENDUS`
et la racine nominale est trouvée sur chaque carte du socle dont une
lecture (c) est publiée (`cas_controles`, `controles_tenus`), quels que soient les écarts aux valeurs publiées (ils
sont publiés : le visa relève de l'expert pilote et du mainteneur) ; 2
sinon. Déterministe : deux
exécutions donnent une sortie identique à l'octet.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import sys
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path

import numpy as np

RACINE = Path(__file__).resolve().parents[1]
SPEC = RACINE / "docs" / "specification" / "nations_et_marches.tex"


def _charger_etat_stationnaire():
    """Module `etat_stationnaire`, voisin de ce script, chargé par son chemin (`outils/` n'est pas un paquet)."""
    nom = "etat_stationnaire"
    if nom in sys.modules:
        return sys.modules[nom]
    chemin = Path(__file__).resolve().parent / (nom + ".py")
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    sys.modules[nom] = module
    spec.loader.exec_module(module)
    return module


es = _charger_etat_stationnaire()

# --- Méthode commune --------------------------------------------------------------

PAS_RELATIF = 1e-6  # pas des différences finies centrées, relatif à l'échelle de la variable
TOL_RACINE_NOMINALE = 1e-8  # |λ − 1| de la racine nominale (sec:prix-conditions, sec:menages-conditions)
TOL_POINT_FIXE = 1e-10  # résidu du point fixe de la carte détendue, relatif à l'échelle de chaque variable
ITERATIONS_BISSECTION = 40
NU_G = es.NU_G_RETENU  # ν_G retenu (décision du mainteneur du 05/10/2026, #84)
PLANCHER_TAUX = 0.01  # échelle plancher d'un taux ou d'une part, par an ou fraction

# Familles de variables : (nature, facteur de tendance sur un pas). « mult » : la valeur est divisée par le
# facteur ; « log » : le logarithme est diminué du logarithme du facteur.


@dataclass(frozen=True)
class Carte:
    """Carte d'un pas sur les variables d'état, avec son point stationnaire et sa détendance."""

    noms: tuple[str, ...]
    x0: np.ndarray  # état d'ouverture du pas 0, sur le sentier stationnaire
    echelle: np.ndarray  # échelle de chaque variable (pas des différences finies, résidus)
    log: np.ndarray  # booléens : variable en logarithme
    facteur: np.ndarray  # facteur de tendance d'un pas, par variable
    pas: object  # x_t ↦ x_{t+1}, en niveaux (ou logarithmes), au pas 0
    racine_nominale: bool  # la maquette porte une racine nominale (niveau des prix et des montants)

    def detendue(self, x: np.ndarray) -> np.ndarray:
        """x_{t+1} ramené à la tendance du pas 0."""
        y = np.asarray(self.pas(x), dtype=float)
        return np.where(self.log, y - np.log(self.facteur), y / self.facteur)


def residu_point_fixe(carte: Carte) -> float:
    """Plus grand écart du point fixe, relatif à l'échelle de chaque variable."""
    return float(np.max(np.abs(carte.detendue(carte.x0) - carte.x0) / carte.echelle))


def jacobienne(carte: Carte) -> np.ndarray:
    """Jacobienne de la carte détendue au point stationnaire, différences centrées, mise à l'échelle S⁻¹ J S."""
    k = len(carte.x0)
    J = np.empty((k, k))
    for j in range(k):
        h = PAS_RELATIF * carte.echelle[j]
        e = np.zeros(k)
        e[j] = h
        J[:, j] = (carte.detendue(carte.x0 + e) - carte.detendue(carte.x0 - e)) / (2 * h)
    return J * carte.echelle[None, :] / carte.echelle[:, None]


@dataclass(frozen=True)
class Spectre:
    rayon: float
    racine: complex  # racine dominante, hors racine nominale
    periode: float | None  # tours, si la racine dominante est complexe
    demi_vie: float | None  # tours, si |λ| < 1
    ecart_nominal: float | None  # |λ − 1| de la racine nominale exclue
    residu: float  # résidu du point fixe


def spectre(carte: Carte) -> Spectre:
    """Rayon spectral, hors racine nominale si la maquette la porte, avec période et demi-vie."""
    valeurs = np.linalg.eigvals(jacobienne(carte))
    valeurs = sorted(valeurs, key=lambda z: (-abs(z), z.real, z.imag))
    ecart_nominal = None
    if carte.racine_nominale:
        i = min(range(len(valeurs)), key=lambda q: abs(valeurs[q] - 1))
        ecart_nominal = float(abs(valeurs[i] - 1))
        valeurs = valeurs[:i] + valeurs[i + 1:]
    lam = complex(valeurs[0])
    rayon = abs(lam)
    periode = 2 * math.pi / abs(math.atan2(lam.imag, lam.real)) if abs(lam.imag) > 1e-12 else None
    demi_vie = math.log(0.5) / math.log(rayon) if 0 < rayon < 1 else None
    return Spectre(rayon, lam, periode, demi_vie, ecart_nominal, residu_point_fixe(carte))


def frontiere(rayon_de, bas: float, haut: float) -> float:
    """Valeur du paramètre où le rayon passe 1, par bissection sur [bas ; haut] encadrant (contrôlé)."""
    r_bas, r_haut = rayon_de(bas), rayon_de(haut)
    if not (r_bas - 1) * (r_haut - 1) < 0:
        raise ValueError(f"intervalle non encadrant : rayon {r_bas!r} et {r_haut!r} aux bornes {bas} et {haut}")
    stable_en_bas = r_bas < 1
    for _ in range(ITERATIONS_BISSECTION):
        milieu = 0.5 * (bas + haut)
        if (rayon_de(milieu) < 1) == stable_en_bas:
            bas = milieu
        else:
            haut = milieu
    return 0.5 * (bas + haut)


def _carte(variables: list[tuple[str, float, float, bool, float]], pas, racine_nominale: bool) -> Carte:
    """Assemble une carte depuis (nom, valeur, échelle plancher, en logarithme, facteur de tendance)."""
    noms = tuple(v[0] for v in variables)
    x0 = np.array([v[1] for v in variables], dtype=float)
    plancher = np.array([v[2] for v in variables], dtype=float)
    log = np.array([v[3] for v in variables], dtype=bool)
    facteur = np.array([v[4] for v in variables], dtype=float)
    echelle = np.where(log, 1.0, np.maximum(np.abs(x0), plancher))
    return Carte(noms, x0, echelle, log, facteur, pas, racine_nominale)


BASE = es.Parametres()


def _cadre(par, n_a: int | None = None) -> dict[str, float]:
    """Facteurs du cadre (sec:cadre-calendrier) : croissance g, facteurs par pas, à la cible de `par`."""
    n = par.n_a if n_a is None else n_a
    g = (1 + par.g_pr) * (1 + par.g_N) - 1
    Gr = (1 + g) ** (1 / n)
    Pp = (1 + par.pi_cible) ** (1 / n)
    return {"n": n, "g": g, "Gr": Gr, "Pp": Pp, "Gam": Gr * Pp, "gam": Gr * Pp - 1, "pis": Pp - 1}


# --- Maquette « offre » : production, stocks, emploi, prix, salaires ---------------------


@lru_cache(maxsize=None)
def carte_offre(m: float, prix: str = "fige", salaires: bool = False, lambda_v: float = BASE.lambda_v,
                lambda_IN: float = BASE.lambda_IN, lambda_mu: float = BASE.lambda_mu,
                psi_xi: float = BASE.psi_xi, lambda_w: float = BASE.lambda_w) -> Carte:
    """Production N1 à N7, emploi égal à la demande de travail, demande induite d_t = A + m y_{t−1}.

    `prix` : « fige » (prix tenu sur la tendance, sec:travail-conditions), « regle » (P1 à P3,
    sec:prix-conditions) ou « marge » (marge constante μ̄, comparaison de la boucle salaires -- prix).
    Sous un prix endogène, les plans sont en u.m. au prix du pas précédent prolongé de la cible,
    P_{t−1}(1 + π^pas)(A + m y_{t−1}), et la demande en volume est le plan divisé par p_t (N6).
    `salaires` : règles T2 et T3, anticipation exogène π^e = π* ; sinon coût unitaire exogène.
    """
    par = BASE
    c = _cadre(par)
    n, Gr, Pp, Gam = c["n"], c["Gr"], c["Pp"], c["Gam"]
    sig, mub, Ueq = par.sigma, par.mu_bar, par.U_eq
    v = 1.0
    y = v * (1 + n * sig * (Gr - 1))
    IN = n * sig * v
    y_m1 = y / Gr
    A = v - m * y_m1  # demande autonome en volume, résolue pour d = v
    pr = par.pr_0
    p = par.p_0
    W = p / (1 + mub) * pr
    N_pa = (y / pr) / (1 - Ueq)  # U = U^eq à l'état stationnaire
    variables = [("ve", v, v, False, Gr), ("IN_vol", IN, v, False, Gr), ("y_m1", y_m1, v, False, Gr)]
    if prix != "fige":
        variables.append(("lnP_m1", math.log(p / Pp), 1.0, True, Pp))
    if salaires:
        variables += [("lnW_m1", math.log(W / Gam), 1.0, True, Gam), ("U_m1", Ueq, PLANCHER_TAUX, False, 1.0)]
    idx = {nom: i for i, (nom, *_) in enumerate(variables)}

    def pas(x):
        ve, IN_vol, ym1 = x[idx["ve"]], x[idx["IN_vol"]], x[idx["y_m1"]]
        IN_star = n * sig * ve  # N2
        y_star = ve + (Gr - 1) * IN_star + lambda_IN / n * (IN_star - IN_vol)  # N3
        yy = y_star  # N4, N5 : emploi égal à la demande de travail
        sortie = {}
        if salaires:
            lW_m1, U_m1 = x[idx["lnW_m1"]], x[idx["U_m1"]]
            pr_m1 = pr / Gr
            omega = math.exp(lW_m1 - x[idx["lnP_m1"]]) / pr_m1  # T2
            lW = (lW_m1 + (math.log(1 + par.g_pr) + math.log(1 + par.pi_cible)) / n
                  + lambda_w / n * (math.log(1 / (1 + mub) / omega) - par.beta * (U_m1 - Ueq)))  # T3
            sortie["lnW_m1"] = lW
            sortie["U_m1"] = 1 - (yy / pr) / N_pa  # T4 (régime de hausse), T5
            lUC, lUC_m1 = lW - math.log(pr), lW_m1 - math.log(pr_m1)
        else:
            lUC = math.log(W / pr)
            lUC_m1 = lUC - math.log(Pp)
        if prix == "fige":
            d = A + m * ym1
        else:
            lP_m1 = x[idx["lnP_m1"]]
            if prix == "regle":
                xi = 1 - IN_vol / IN_star  # P1
                mu_t = (1 - lambda_mu / n) * (lP_m1 - lUC_m1) + lambda_mu / n * (math.log(1 + mub) + psi_xi * xi)  # P2
                lp = lUC + mu_t  # P3
            else:
                lp = lUC + math.log(1 + mub)
            d = math.exp(lP_m1) * Pp * (A + m * ym1) / math.exp(lp)  # N6 : plan en u.m. divisé par p_t
            sortie["lnP_m1"] = lp  # P4
        v_t = d  # N6, disponibilité inactive
        sortie["ve"] = Gr * ((1 - lambda_v / n) * ve + lambda_v / n * d)  # N1
        sortie["IN_vol"] = IN_vol + yy - v_t  # N7
        sortie["y_m1"] = yy
        return [sortie[nom] for nom, *_ in variables]

    return _carte(variables, pas, racine_nominale=salaires)


# --- Maquette « investissement » : boucle réduite investissement -- demande ---------------------


@lru_cache(maxsize=None)
def carte_investissement(m: float, ans: float = 2.0, lambda_ti: float = BASE.lambda_ti) -> Carte:
    """N1 à N7, S3 et S6 ; demande A + m y_{t−1} + I^{vol,plan} ; prix et taux exogènes (ϱ_L = ϱ̄_L).

    `ans` : capital en années de production, κ/t̄u ; σ = 1,4/12 an (sec:investissement-conditions).
    """
    par = BASE
    c = _cadre(par)
    n, Gr = c["n"], c["Gr"]
    sig, delta, tub = par.sigma, par.delta, par.tu_bar
    kappa = ans * tub
    v = 1.0
    y = v * (1 + n * sig * (Gr - 1))
    IN = n * sig * v
    y_m1 = y / Gr
    K_vol = n * kappa * y / tub  # tu = t̄u
    I_vol = (Gr - 1 + delta / n) * K_vol  # N10 sur le sentier
    ti = I_vol / y  # S3 : I^{vol,plan} = ti Gr y_{t−1} = I_vol
    A = v - m * y_m1 - I_vol
    variables = [("ve", v, v, False, Gr), ("IN_vol", IN, v, False, Gr), ("y_m1", y_m1, v, False, Gr),
                 ("K_vol", K_vol, v, False, Gr), ("ti", ti, PLANCHER_TAUX, False, 1.0)]

    def pas(x):
        ve, IN_vol, ym1, Kv, ti_t = x
        IN_star = n * sig * ve  # N2
        yy = ve + (Gr - 1) * IN_star + par.lambda_IN / n * (IN_star - IN_vol)  # N3, N5
        I_plan = ti_t * Gr * ym1  # S3, ϱ_L = ϱ̄_L
        d = A + m * ym1 + I_plan
        tu = yy / (Kv / (n * kappa))  # N11
        return [Gr * ((1 - par.lambda_v / n) * ve + par.lambda_v / n * d),  # N1
                IN_vol + yy - d,  # N7
                yy,
                (1 - delta / n) * Kv + I_plan,  # N10
                ti_t * math.exp(lambda_ti / n * (tu - tub))]  # S6, t̄u* = t̄u

    return _carte(variables, pas, racine_nominale=False)


# --- Maquette « ménages » : production, travail, prix et ménages -----------------------------

LECTURES = ("cible", "a", "a_entretien", "hs_glissement", "hs_glissement_pas")
RESULTATS = ("cout_unitaire", "cout_moyen")


@lru_cache(maxsize=None)
def carte_menages(theta_H: float = 0.8, regime: str = "hausse", lecture: str = "cible", h: float = 1.0,
                  nu_H: float = BASE.nu_H, n_a: int = 12, vitesses: float = 1.0, i_D: float = 0.03,
                  resultat: str = "cout_unitaire") -> Carte:
    """Blocs production (N1 à N8), travail (T2 à T6), prix (P1 à P3) et ménages (H2 à H6), sec:menages-conditions.

    Anticipation exogène π^e = π* ; dépense autonome (État et investissement) en u.m. au prix du pas
    précédent prolongé de la cible ; sans impôts ni transferts ; i_D exogène. `theta_H` : 0,8, les ménages
    reçoivent les salaires et les intérêts de leurs dépôts ; 1, aussi le résultat courant des entreprises,
    p v + UC (y − v) − WB (`resultat` = « cout_unitaire ») ou p v + ΔIN − WB au coût moyen de N8
    (« cout_moyen »). `lecture` : « cible » (H2 à H4 de la spécification) ; « a », richesse visée sur le
    revenu nominal, V* = ν_H n_a YD^e, et inflation lue sur le glissement π_{t−1} dans γ^e, donc dans
    Γ^e = 1 + γ^e de H2, avec un poids `h` (correction partielle) ; « a_entretien », même chose, le
    glissement n'entrant que dans le terme d'entretien de H4 ; « hs_glissement », richesse de Haig-Simons,
    π^{*,pas} de H3 et γ^e (H2, H4) lus sur le glissement ; « hs_glissement_pas », π^{*,pas} de H3 seul lu
    sur le glissement. `vitesses` multiplie λ_v, λ_IN, λ_w, λ_N, λ_μ et λ_H.
    """
    if lecture not in LECTURES or resultat not in RESULTATS or regime not in ("hausse", "baisse"):
        raise ValueError(f"maquette ménages : lecture {lecture!r}, résultat {resultat!r}, régime {regime!r}")
    par = BASE
    c = _cadre(par, n_a)
    n, g, Gr, Pp, Gam, gam, pis = c["n"], c["g"], c["Gr"], c["Pp"], c["Gam"], c["gam"], c["pis"]
    pi = par.pi_cible
    sig, mub, Ueq = par.sigma, par.mu_bar, par.U_eq
    lv, lIN, lw, lN = (vitesses * par.lambda_v, vitesses * par.lambda_IN, vitesses * par.lambda_w,
                       vitesses * par.lambda_N)
    lmu, lH = vitesses * par.lambda_mu, vitesses * par.lambda_H
    distribue = theta_H == 1.0
    if theta_H not in (0.8, 1.0):
        raise ValueError(f"θ_H = {theta_H!r} : 0,8 ou 1 attendu")
    # État stationnaire de la maquette (formes fermées).
    v = 1.0
    y = v * (1 + n * sig * (Gr - 1))
    IN_vol = n * sig * v
    p = 1.0
    UC = p / (1 + mub)
    pr = 1.0
    W = UC * pr
    N = y / pr
    N_pa = N / (1 - Ueq)
    IN = es.rho_IN(n, sig, g, pi) * UC * IN_vol  # valeur comptable des stocks (N8)
    dIN = gam * IN
    WB = W * N
    if distribue:
        Y_o = p * v + UC * (y - v) if resultat == "cout_unitaire" else p * v + dIN
    else:
        Y_o = WB
    # Richesse stationnaire : C = YD − γ̄ V (entretien) égale à la règle H4, YD = Y_o + i_D V/n_a.
    if lecture in ("a", "a_entretien"):
        D_H = nu_H * n * Y_o / (1 - nu_H * i_D)  # V* = ν_H n_a YD
    else:
        D_H = nu_H * n * Y_o / (1 + nu_H * n * pis - nu_H * i_D)  # V* = ν_H n_a (YD − π^pas V)
    YD = Y_o + i_D * D_H / n
    C = YD - gam * D_H
    autonome = p * v - C  # dépense autonome en u.m. au pas 0
    registre = [math.log(p) - u * math.log(Pp) for u in range(1, n + 2)]  # ln P_{t−u}
    variables = [("ve", v, v, False, Gr), ("IN_vol", IN_vol, v, False, Gr)]
    variables += [(f"lnP_{u}", registre[u - 1], 1.0, True, Pp) for u in range(1, n + 2)]
    variables += [("lnW_m1", math.log(W / Gam), 1.0, True, Gam), ("N_m1", N, N, False, 1.0),
                  ("D_H", D_H, D_H, False, Gam), ("YD_m1", YD / Gam, YD, False, Gam), ("IN", IN, IN, False, Gam)]
    idx = {nom: i for i, (nom, *_) in enumerate(variables)}
    i_P = idx["lnP_1"]

    def pas(x):
        ve, INv = x[idx["ve"]], x[idx["IN_vol"]]
        lP = x[i_P:i_P + n + 1]
        lW_m1, N_m1, DH, YD_m1, IN_nom = (x[idx[k]] for k in ("lnW_m1", "N_m1", "D_H", "YD_m1", "IN"))
        # Phase 1 : salaires (T2, T3), π^e = π*.
        U_m1 = 1 - N_m1 / N_pa
        pr_m1 = pr / Gr
        omega = math.exp(lW_m1 - lP[0]) / pr_m1  # T2
        lW = (lW_m1 + (math.log(1 + par.g_pr) + math.log(1 + pi)) / n
              + lw / n * (math.log(1 / (1 + mub) / omega) - par.beta * (U_m1 - Ueq)))  # T3
        Wt = math.exp(lW)
        # Phase 2 : plans (N2 à N4, N8, H2 à H5).
        IN_star = n * sig * ve  # N2
        y_star = ve + (Gr - 1) * IN_star + lIN / n * (IN_star - INv)  # N3
        N_star = y_star / pr  # N4
        UCt = Wt / pr  # N8
        pi_m = math.exp(lP[0] - lP[n]) - 1  # glissement du tour précédent (registre)
        pi_lu = pi + h * (pi_m - pi)
        gam_lu = ((1 + g) * (1 + pi_lu)) ** (1 / n) - 1
        pis_lu = (1 + pi_lu) ** (1 / n) - 1
        if lecture == "cible":
            YDe = Gam * YD_m1  # H2
            V_star = nu_H * n * (YDe - pis * DH)  # H3
            entretien = gam
        elif lecture == "a":
            YDe = (1 + gam_lu) * YD_m1
            V_star = nu_H * n * YDe
            entretien = gam_lu
        elif lecture == "a_entretien":
            YDe = Gam * YD_m1
            V_star = nu_H * n * YDe
            entretien = gam_lu
        elif lecture == "hs_glissement":
            YDe = (1 + gam_lu) * YD_m1
            V_star = nu_H * n * (YDe - pis_lu * DH)
            entretien = gam_lu
        else:  # hs_glissement_pas
            YDe = Gam * YD_m1
            V_star = nu_H * n * (YDe - pis_lu * DH)
            entretien = gam
        C_plan = min(DH, max(0.0, YDe - entretien * DH - lH / n * (V_star - DH)))  # H4, H5
        # Phase 4 : emploi (T4, un régime), production (N5 : y = y*, N ≥ N*).
        N_t = N_star if regime == "hausse" else (1 - lN / n) * N_m1 + lN / n * N_star  # T4, g_N = 0
        y_t = y_star
        WB_t = Wt * N_t  # T6
        # Phase 5 : prix (P1 à P3), ventes (N6, N7), consommation (H6).
        xi = 1 - INv / IN_star  # P1
        lUC_m1 = lW_m1 - math.log(pr_m1)
        mu_t = (1 - lmu / n) * (lP[0] - lUC_m1) + lmu / n * (math.log(1 + mub) + par.psi_xi * xi)  # P2
        lp = math.log(UCt) + mu_t  # P3
        p_t = math.exp(lp)
        A_plan = math.exp(lP[0]) * Pp * autonome  # plan autonome en u.m., au prix précédent prolongé
        d = (C_plan + A_plan) / p_t  # N6
        v_t = min(d, INv + y_t)
        C_t = p_t * v_t * C_plan / (C_plan + A_plan)  # H6
        cm = (IN_nom + UCt * y_t) / (INv + y_t)  # N8
        dIN_t = UCt * y_t - cm * v_t
        # Phase 6 et 9 : revenu disponible (H7).
        if distribue:
            Y_o_t = p_t * v_t + (UCt * (y_t - v_t) if resultat == "cout_unitaire" else dIN_t)
        else:
            Y_o_t = WB_t
        YD_t = Y_o_t + i_D * DH / n
        sortie = [Gr * ((1 - lv / n) * ve + lv / n * d),  # N1
                  INv + y_t - v_t]  # N7
        sortie += [lp] + list(lP[:n])  # P4, avancée du registre
        sortie += [lW, N_t, DH + YD_t - C_t, YD_t, IN_nom + dIN_t]
        return sortie

    return _carte(variables, pas, racine_nominale=True)


# --- Maquette « socle » : blocs 2 à 9 -------------------------------------------------------

NOMINAUX = ("W_m1", "IN", "K", "T_F_m1", "L", "D_F", "YD_m1", "D_H", "E_Bk", "L_CB", "Res", "B_Bk", "B_CB",
            "M_G", "E_CB", "Y_HS_m1")
VOLUMES = ("ve", "IN_vol", "K_vol", "y_m1")
TAUX = ("U_m1", "ti", "i_L", "i_D", "r_hat", "pi_e")


@lru_cache(maxsize=None)
def etat_socle(par) -> tuple[dict, dict]:
    """État résolu d'`etat_stationnaire` et ouverture du pas 0 (`ouverture`), pour `par`."""
    e = es.etat_stationnaire(par)
    return e, es.ouverture(e, par)


# Variantes écartées de la règle de financement F (fiche 6, § 3.N ; sec:ecartees), seconde écriture depuis
# leurs définitions (issues #65 et #66). « Levier sur p K^vol » : la cible de crédit de F1 est
# lv*·p_lu·K_lu au lieu de lv*·[(1 − δ/n_a)K + p̂ I^{vol,plan}], selon les quatre écritures de la fiche :
# prix p̂_t = p_{t−1}(1 + π*)^{1/n_a} ou p_{t−1}, capital d'ouverture K^vol_t ou après investissement
# (1 − δ/n_a)K^vol_t + I^{vol,plan}_t. « Dépôts sur les ventes du pas » : la cible de F2 est ν_F n_a p_t v_t
# au lieu de ν_F n_a p_{t−1}(1 + π*)^{2/n_a} v^e_{t+1}, levier comptable. Combinaison des deux (première ligne du
# tableau de la fiche, 1,4925) : levier sur p K^vol dans l'écriture de la précision de la fiche (L^cible =
# lv*·p̂_t·K^vol_t d'ouverture) et dépôts sur les ventes du pas.
LEVIERS_PK = {"levier_pK.p_hat.ouverture": ("p_hat", "ouverture"),
              "levier_pK.p_prec.ouverture": ("p_prec", "ouverture"),
              "levier_pK.p_hat.apres": ("p_hat", "apres"), "levier_pK.p_prec.apres": ("p_prec", "apres")}
LEVIER_PK_DEPOTS_VENTES = "levier_pK.p_hat.ouverture+depots_ventes"
FINANCEMENTS = ("F",) + tuple(LEVIERS_PK) + ("depots_ventes", LEVIER_PK_DEPOTS_VENTES)


def ecritures_financement(financement: str) -> tuple[str | None, bool]:
    """Écriture du levier sur p K^vol (clé de `LEVIERS_PK`, None : F1 retenue) et dépôts sur les ventes du pas."""
    if financement == LEVIER_PK_DEPOTS_VENTES:
        return "levier_pK.p_hat.ouverture", True
    if financement in LEVIERS_PK:
        return financement, False
    if financement in ("F", "depots_ventes"):
        return None, financement == "depots_ventes"
    raise ValueError(f"financement {financement!r}")
TAUX_SOCLE = ("regle", "exogene", "exogene_ancre")
# B6 : « regle », max(0, ·) tel qu'écrit ; « verse », argument sans plancher ; « plancher », dividende nul.
# Les deux dernières sont les deux branches du coude de B6, linéarisées séparément là où il est atteint à
# l'état stationnaire (ϑ = 0 et i_L = i_D = i_CB : E^Bk = Π^Bk = 0, configuration « fiche »).
BRANCHES_B6 = ("regle", "verse", "plancher")


def parametres_etat(par, financement: str = "F"):
    """Paramètres dont l'état résolu d'`etat_stationnaire` est le point stationnaire de la variante de F.

    `etat_stationnaire` résout la règle F retenue, L = lv K et D_F = ν_F n_a p v. Sous une variante, la cible
    au point stationnaire vaut L_{t+1} = Γ̄ L_t (resp. D_{F,t+1} = Γ̄ D_{F,t}) : le levier comptable (resp.
    ν_F) de l'état est celui qui donne ce stock, la règle de la variante gardant lv* (resp. ν_F) déclaré.
    K, K^vol, p et v ne dépendent ni de lv ni de ν_F (formes fermées, étapes 2 et 3). Le résidu du point
    fixe de la carte contrôle cette résolution.
    """
    levier, depots_ventes = ecritures_financement(financement)
    if financement == "F":
        return par
    e = es.etat_stationnaire(par)
    c = _cadre(par)
    etat = par
    if levier is not None:
        prix, capital = LEVIERS_PK[levier]
        p_lu = e["p"] if prix == "p_hat" else e["p"] / c["Pp"]  # P_{t−1} = p/(1 + π̄)^{1/n_a}
        K_lu = e["K_vol"] if capital == "ouverture" else (1 - par.delta / par.n_a) * e["K_vol"] + e["I_vol"]
        etat = replace(etat, lv=par.lv * p_lu * K_lu / (c["Gam"] * e["K"]))
    if depots_ventes:
        etat = replace(etat, nu_F=par.nu_F / c["Gam"])  # D_{F,t+1} = ν_F n_a p v, D_{F,t} = D_{F,t+1}/Γ̄
    return etat


@lru_cache(maxsize=None)
def carte_socle(par, regime: str = "hausse", taux: str = "regle", financement: str = "F",
                B6: str = "regle") -> Carte:
    """Blocs 2 à 9 du socle, sur l'ouverture de l'état initial résolu (`etat_stationnaire.ouverture`).

    Variables d'état : registre de l'indice (n_a + 1 niveaux), N_{t−1}, U_{t−1}, W_{t−1}, v^e, IN^vol,
    IN, K^vol, K, ti, y_{t−1}, T_{F,t−1}, L, D_F, YD_{t−1}, D_H, i_L, i_D, E^Bk, L^CB, Res, B_Bk, B_CB,
    M^G, E^CB, r̂*, π^e, Y^HS_{t−1}. Exogènes, tenues sur leur sentier : pr, N^pa (T1, N9), la cible
    (BC4, levier fermé), θ_G (levier), ϱ̄_L (constante de l'état), B_H ≡ 0 (C42).

    `taux` : « regle » (BC1 à BC3) ; « exogene », taux directeur tenu à sa valeur stationnaire (BC1 et BC2
    hors de la boucle, d'où i_L et i_D constants par B1 et B2), anticipation adaptative BC3 gardée ;
    « exogene_ancre », de plus π^e tenu à π* (BC3 hors de la boucle, comme la maquette `menages`).
    `financement` : F retenue ou une variante écartée (`FINANCEMENTS`), sur l'état de `parametres_etat`.
    `B6` : `BRANCHES_B6`.
    """
    if regime not in ("hausse", "baisse") or taux not in TAUX_SOCLE or financement not in FINANCEMENTS \
            or B6 not in BRANCHES_B6:
        raise ValueError(f"régime {regime!r}, taux {taux!r}, financement {financement!r}, B6 {B6!r}")
    levier, depots_ventes = ecritures_financement(financement)
    e, o = etat_socle(parametres_etat(par, financement))
    n = par.n_a
    c = _cadre(par)
    Gr, Pp, Gam = c["Gr"], c["Pp"], c["Gam"]
    G_N = (1 + par.g_N) ** (1 / n)
    echelle_nom = e["PIB"]
    variables = [(f"P_{u}", o["registre"][u - 1], o["registre"][u - 1], False, Pp) for u in range(1, n + 2)]
    variables.append(("N_m1", o["N_m1"], o["N_m1"], False, G_N))
    for nom in ("U_m1", "W_m1", "ve", "IN_vol", "IN", "K_vol", "K", "ti", "y_m1", "T_F_m1", "L", "D_F",
                "YD_m1", "D_H", "i_L", "i_D", "E_Bk", "L_CB", "Res", "B_Bk", "B_CB", "M_G", "E_CB", "r_hat",
                "pi_e", "Y_HS_m1"):
        if nom in NOMINAUX:
            variables.append((nom, o[nom], echelle_nom, False, Gam))
        elif nom in VOLUMES:
            variables.append((nom, o[nom], e["y"], False, Gr))
        else:
            variables.append((nom, o[nom], PLANCHER_TAUX, False, 1.0))
    idx = {nom: i for i, (nom, *_) in enumerate(variables)}
    pr, N_pa, pi_c, theta_G, rho_bar = o["pr"], o["N_pa"], o["pi_cible"], o["theta_G"], o["rho_bar_L"]

    def pas(x):
        s = {nom: x[i] for nom, i in idx.items()}
        P = [s[f"P_{u}"] for u in range(1, n + 2)]
        # Phase 0 : facteurs du moteur sur la cible d'ouverture (sec:cadre-calendrier).
        Gam_e = ((1 + c["g"]) * (1 + pi_c)) ** (1 / n)
        gam_e, pis = Gam_e - 1, (1 + pi_c) ** (1 / n) - 1
        # Phase 1 : salaire (T2, T3) ; règle de taux et anticipation (BC1 à BC3, BC6).
        pi_prec = P[0] / P[n] - 1
        pr_m1 = pr / ((1 + par.g_pr) ** (1 / n))
        omega = s["W_m1"] / (P[0] * pr_m1)  # T2
        W = math.exp(math.log(s["W_m1"]) + (math.log(1 + par.g_pr) + math.log(1 + s["pi_e"])) / n
                     + par.lambda_w / n * (math.log(1 / (1 + par.mu_bar) / omega)
                                           - par.beta * (s["U_m1"] - par.U_eq)))  # T3
        if taux == "regle":
            i_CB = (1 + s["r_hat"]) * (1 + pi_c) + par.a_pi * (pi_prec - pi_c) - 1  # BC1
            r_hat_1 = s["r_hat"] + par.a_I / n * (pi_prec - pi_c)  # BC2
        else:
            i_CB, r_hat_1 = e["i_CB"], e["r_hat"]  # taux directeur tenu, BC1 et BC2 hors de la boucle
        if taux == "exogene_ancre":
            pi_e_1 = e["pi_e"]  # anticipation ancrée sur la cible, BC3 hors de la boucle
        else:
            pi_e_1 = s["pi_e"] + par.lambda_e / n * (pi_prec - s["pi_e"])  # BC3
        Pi_CB = i_CB * (s["B_CB"] + s["L_CB"] - s["Res"]) / n  # BC6, i_B = i_res = i_CB
        # Phase 2 : plans (N2 à N4, N8, H2 à H5, S1 à S4, E1, E3, E4, E6).
        IN_star = n * par.sigma * s["ve"]  # N2
        y_star = max(0.0, s["ve"] + (Gr - 1) * IN_star + par.lambda_IN / n * (IN_star - s["IN_vol"]))  # N3
        N_star = y_star / pr  # N4
        UC = W / pr  # N8
        YD_e = Gam_e * s["YD_m1"]  # H2
        V_H = s["D_H"]  # B_H ≡ 0
        V_star = par.nu_H * n * (YD_e - pis * V_H)  # H3
        C_plan = min(s["D_H"], max(0.0, YD_e - gam_e * V_H - par.lambda_H / n * (V_star - V_H)))  # H4, H5
        rho_L = (1 + s["i_L"]) / (1 + pi_c) - 1  # S1
        tu_star = par.tu_bar * math.exp(par.zeta * (rho_L - rho_bar))  # S2
        I_plan = P[0] * (1 + pis) * s["ti"] * Gr * s["y_m1"] * math.exp(-par.eta_r * (rho_L - rho_bar))  # S3, S4
        y_pot = pr * (1 - par.U_eq) * N_pa
        G_plan = min(s["M_G"], P[0] * (1 + pis) * theta_G * y_pot)  # E1
        B = s["B_Bk"] + s["B_CB"]  # B_H ≡ 0
        i_ref = (1 + par.rbar) * (1 + pi_c) - 1
        T_cou = par.phi * (i_CB - i_ref) * (B - s["M_G"] - s["E_CB"]) / n  # E4
        T_H = par.tau_H * Gam_e * s["Y_HS_m1"] + T_cou  # E3
        Tr_lev = P[0] * (1 + pis) * par.theta_Tr * y_pot
        Tr = min(Tr_lev, max(0.0, s["M_G"] + T_H - i_CB * B / n - G_plan))  # E6
        # Phase 3 : crédit (F1), sans refus.
        if levier is not None:
            prix, capital = LEVIERS_PK[levier]
            p_hat = P[0] * (1 + pis)
            p_lu = p_hat if prix == "p_hat" else P[0]
            K_lu = s["K_vol"] if capital == "ouverture" else (1 - par.delta / n) * s["K_vol"] + I_plan / p_hat
            dL_d = par.lv * p_lu * K_lu - s["L"]  # variante écartée : levier sur p K^vol
        else:
            dL_d = par.lv * ((1 - par.delta / n) * s["K"] + I_plan) - s["L"]
        dL = (1 - par.varsigma_L) * max(dL_d, 0.0) + min(dL_d, 0.0)
        # Phase 4 : emploi (T4, un régime ; borne N^pa inactive), production (N5 : y = y*), N11.
        if regime == "hausse":
            N = N_star
        else:
            N = G_N * (1 - par.lambda_N / n) * s["N_m1"] + par.lambda_N / n * N_star
        N = min(N_pa, N)
        U = 1 - N / N_pa  # T5
        WB = W * N  # T6
        y = y_star
        tu = y / (s["K_vol"] / (n * par.kappa))  # N11
        # Phase 5 : prix (P1 à P4), ventes (N6, N7), acheteurs (H6, S5, E2), N1, N8 à N10, S6.
        xi = 1 - s["IN_vol"] / IN_star  # P1
        UC_m1 = s["W_m1"] / pr_m1
        mu_t = ((1 - par.lambda_mu / n) * math.log(P[0] / UC_m1)
                + par.lambda_mu / n * (math.log(1 + par.mu_bar) + par.psi_xi * xi))  # P2
        p = UC * math.exp(mu_t)  # P3
        d_H, d_F, d_G = C_plan / p, I_plan / p, G_plan / p  # N6
        d = d_H + d_F + d_G
        v = min(d, s["IN_vol"] + y)
        C, I, G = p * v / d * d_H, p * v / d * d_F, p * v / d * d_G  # H6, S5, E2
        cm = (s["IN"] + UC * y) / (s["IN_vol"] + y)  # N8
        dIN = UC * y - cm * v
        ve_1 = Gr * ((1 - par.lambda_v / n) * s["ve"] + par.lambda_v / n * d)  # N1
        K_vol_1 = (1 - par.delta / n) * s["K_vol"] + v / d * d_F  # N10
        ti_1 = s["ti"] * math.exp(par.lambda_ti / n * (tu - tu_star))  # S6
        # Phase 6 : amortissement, intérêts, impôt des entreprises, dividendes (S7, B3 à B6, E5, F2 à F4).
        amort = par.delta * s["K"] / n  # S7
        l9 = s["i_L"] * s["L"] / n  # B3
        l10_H, l10_F = s["i_D"] * s["D_H"] / n, s["i_D"] * s["D_F"] / n  # B4
        T_F = par.tau_F * (C + G + I + dIN - WB - amort - l9 + l10_F)  # E5
        if depots_ventes:
            D_F_star = par.nu_F * n * p * v  # variante écartée : dépôts visés sur les ventes du pas
        else:
            D_F_star = par.nu_F * n * P[0] * (1 + pis) ** 2 * ve_1  # F2
        T_F_e = Gam_e * s["T_F_m1"]  # F4
        Div_F = max(0.0, s["D_F"] + dL + C + G - WB - l9 + l10_F - T_F_e - D_F_star)  # F3
        L_1 = s["L"] + dL
        Pi_Bk = (s["i_L"] * s["L"] + i_CB * s["B_Bk"] + i_CB * s["Res"] - s["i_D"] * (s["D_H"] + s["D_F"])
                 - i_CB * s["L_CB"]) / n  # B5
        arg_B6 = s["E_Bk"] + Pi_Bk - par.vartheta * L_1
        Div_Bk = {"regle": max(0.0, arg_B6), "verse": arg_B6, "plancher": 0.0}[B6]  # B6
        l11b, l11c = i_CB * s["B_Bk"] / n, i_CB * s["B_CB"] / n  # E7, ligne 11a nulle
        # Phase 7 : émission (E8 à E11), revenu de Haig-Simons (E12).
        PB = G + Tr + i_CB * B / n  # E8
        Em = G + Tr + i_CB * B / n - T_H - T_F - Pi_CB + par.nu_G * PB - s["M_G"]  # E9
        dB_CB = par.theta_CB * Em  # E10
        dB_Bk = (1 - par.varsigma_B) * (Em - dB_CB)  # E11
        Y_HS = WB + l10_H + Div_F + Div_Bk - pis * s["D_H"] - T_cou  # E12
        # Phase 8 : compte du Trésor, réserves et refinancement (BC7 à BC9, B7), taux du pas suivant (B1, B2).
        M_G_8a = s["M_G"] - G - Tr + T_H + T_F - l11b - l11c + dB_Bk + dB_CB
        Res_8b = s["Res"] + G + Tr - T_H - T_F + l11b + i_CB * s["Res"] / n - i_CB * s["L_CB"] / n - dB_Bk
        L_CB_1 = max(s["L_CB"] - Res_8b, 0.0)  # B7
        Res_1 = Res_8b + (L_CB_1 - s["L_CB"])
        # Phase 9 : revenu disponible (H7), registre, postes de clôture par les flux.
        YD = WB + Tr - T_H + l10_H + Div_F + Div_Bk  # H7
        suivant = {
            "N_m1": N, "U_m1": U, "W_m1": W, "ve": ve_1, "IN_vol": s["IN_vol"] + y - v, "IN": s["IN"] + dIN,
            "K_vol": K_vol_1, "K": s["K"] + I - amort, "ti": ti_1, "y_m1": y, "T_F_m1": T_F, "L": L_1,
            "D_F": s["D_F"] + dL - WB + C + G - l9 + l10_F - T_F - Div_F, "YD_m1": YD,
            "D_H": s["D_H"] + YD - C, "i_L": i_CB + par.varpi_L, "i_D": i_CB - par.varpi_D,
            "E_Bk": s["E_Bk"] + Pi_Bk - Div_Bk, "L_CB": L_CB_1, "Res": Res_1, "B_Bk": s["B_Bk"] + dB_Bk,
            "B_CB": s["B_CB"] + dB_CB, "M_G": M_G_8a + Pi_CB, "E_CB": s["E_CB"], "r_hat": r_hat_1,
            "pi_e": pi_e_1, "Y_HS_m1": Y_HS,
        }
        registre = [p] + P[:n]
        return registre + [suivant[nom] for nom, *_ in variables[n + 1:]]

    return _carte(variables, pas, racine_nominale=True)


def parametres_socle(pi: float = 0.02, n_a: int = 12, facteurs: dict[str, float] | None = None):
    """Paramètres du socle : calibration indicative, ν_G retenu, π* = π̄ et vitesses multipliées."""
    par = replace(BASE, pi_cible=pi, n_a=n_a, nu_G=NU_G)
    if facteurs:
        par = replace(par, **{k: getattr(par, k) * f for k, f in sorted(facteurs.items())})
    return par


def parametres_fiche(pi: float = 0.02):
    """Configuration « fiche » des variantes de F : hypothèses de la fiche 6, § 3.N, sur le socle.

    i_L = i_D = 3 % (ϖ_L = ϖ_D = 0 et r̄ tel que i_CB = (1 + r̄)(1 + π̄) − 1 = 3 %, d'où T^cou nul à l'état
    stationnaire), ϑ = 0, τ_H = τ_F = 0 ; le reste comme `parametres_socle`.
    """
    return replace(parametres_socle(pi), varpi_L=0.0, varpi_D=0.0, vartheta=0.0, tau_H=0.0, tau_F=0.0,
                   rbar=1.03 / (1 + pi) - 1)


def rayon_socle(pi: float = 0.02, facteurs: tuple[tuple[str, float], ...] = ()) -> dict[str, Spectre]:
    """Spectre brut du socle dans les deux régimes de l'emploi."""
    par = parametres_socle(pi, facteurs=dict(facteurs))
    return {regime: spectre(carte_socle(par, regime)) for regime in ("hausse", "baisse")}


# Identités de bilan portées par les états du socle (sec:cadre-identites), coefficients sur les stocks
# d'ouverture : bilan de la banque centrale (actif B_CB + L^CB, passif Res + M^G + E^CB) et bilan des banques
# (actif L + B_Bk + Res, passif D_H + D_F + L^CB + E^Bk). E^CB et E^Bk sont des états de la carte, clos par
# les flux : la jacobienne contient donc des directions qui violent ces identités.
IDENTITES_SOCLE = (
    ("bilan de la banque centrale", (("B_CB", 1.0), ("L_CB", 1.0), ("Res", -1.0), ("M_G", -1.0), ("E_CB", -1.0))),
    ("bilan des banques", (("L", 1.0), ("B_Bk", 1.0), ("Res", 1.0), ("D_H", -1.0), ("D_F", -1.0), ("L_CB", -1.0),
                           ("E_Bk", -1.0))),
)
TOL_RACINE_MULTIPLE = 1e-7  # |λ − 1/Γ̄| d'une valeur propre comptée en 1/Γ̄ (dispersion mesurée ≤ 3e−9 à h = 1e−6)
TOL_NOYAU = 1e-8  # valeur singulière de S⁻¹JS − I/Γ̄ comptée dans le noyau (multiplicité géométrique)
TOL_GAUCHE = 1e-8  # |gJ − g/Γ̄|/|g| : variété des identités invariante (mesuré ≤ 2e−10, six cas du socle)
TOL_COUDE = 1e-3  # écart des jacobiennes avant et arrière (mises à l'échelle) : aucun coude franchi
# Stocks tenus en niveau : ligne de S⁻¹JS égale à e_i/Γ̄ à TOL_NOYAU près (stock que rien ne fait varier,
# ramené à la tendance). Au socle, E^CB (Π^CB entièrement versé, BC9) et B_CB (θ_CB = 0, E10).
TENUS_ATTENDUS = ("B_CB", "E_CB")


@dataclass(frozen=True)
class LecturesSocle:
    """Lectures du rayon du socle : brute, sur la variété des identités, et lecture (c) retenue.

    Lecture (c) (décision du mainteneur du 15/10/2026) : rayon sur la variété des identités, hors de la racine
    nominale et des racines en 1/Γ̄ des stocks tenus en niveau, déclarées avec leur multiplicité et leur cause.
    """

    inv_gamma: float  # 1/Γ̄, racine d'un stock nominal tenu en niveau, ramené à la tendance
    rayon_brut: float  # spectre de la carte entière, hors racine nominale
    multiplicite_brute: int  # valeurs propres telles que |λ − 1/Γ̄| ≤ TOL_RACINE_MULTIPLE
    noyau_brut: int  # valeurs singulières de S⁻¹JS − I/Γ̄ inférieures à TOL_NOYAU
    rayon_variete: float  # spectre restreint au noyau des gradients des identités, hors racine nominale
    multiplicite_variete: int
    suivante: complex  # lecture (c) : plus grande racine de la variété hors de 1/Γ̄ et de la racine nominale
    tenus_en_niveau: tuple[str, ...]  # cause des racines en 1/Γ̄ de la variété : stocks tenus en niveau
    residu_gauche: float  # max |g J − g/Γ̄|/|g| : gradient vecteur propre à gauche, la variété est invariante
    residu_identites: float  # max |g·x0|/(|g| PIB) à l'état initial
    ecart_nominal: float  # |λ − 1| de la racine nominale exclue du spectre de la variété

    @property
    def rayon_c(self) -> float:
        return abs(self.suivante)


def gradients_identites(carte: Carte) -> np.ndarray:
    """Gradients des identités de bilan (une ligne par identité), sur les variables de la carte du socle."""
    G = np.zeros((len(IDENTITES_SOCLE), len(carte.x0)))
    for ligne, (_, coefs) in enumerate(IDENTITES_SOCLE):
        for nom, a in coefs:
            G[ligne, carte.noms.index(nom)] = a
    return G


def jacobienne_unilaterale(carte: Carte, signe: int) -> np.ndarray:
    """Jacobienne avant (signe = +1) ou arrière (−1), même pas que `jacobienne`, mise à l'échelle S⁻¹ J S."""
    k = len(carte.x0)
    J = np.empty((k, k))
    f0 = carte.detendue(carte.x0)
    for j in range(k):
        h = signe * PAS_RELATIF * carte.echelle[j]
        e = np.zeros(k)
        e[j] = h
        J[:, j] = (carte.detendue(carte.x0 + e) - f0) / h
    return J * carte.echelle[None, :] / carte.echelle[:, None]


def ecart_avant_arriere(carte: Carte) -> float:
    """max |J⁺ − J⁻| : d'ordre h hors coude (mesuré ≤ 1e−4 au socle), d'ordre 1 si un coude est franchi."""
    return float(np.max(np.abs(jacobienne_unilaterale(carte, 1) - jacobienne_unilaterale(carte, -1))))


def jacobiennes_carte(carte: Carte, par) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """S⁻¹JS, sa restriction Qᵀ(S⁻¹JS)Q au noyau des gradients mis à l'échelle, ces gradients et 1/Γ̄.

    La restriction est exacte si le noyau est invariant, c'est-à-dire si chaque gradient est vecteur propre
    à gauche (contrôlé par `LecturesSocle.residu_gauche`).
    """
    J = jacobienne(carte)
    Gs = gradients_identites(carte) * carte.echelle[None, :]  # coordonnées mises à l'échelle
    _, _, Vt = np.linalg.svd(Gs)
    Q = Vt[len(IDENTITES_SOCLE):].T  # base orthonormée du noyau des gradients
    return J, Q.T @ J @ Q, Gs, 1 / _cadre(par)["Gam"]


def jacobiennes_socle(pi: float, regime: str) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """`jacobiennes_carte` du socle à π̄ = π* = `pi`."""
    par = parametres_socle(pi)
    return jacobiennes_carte(carte_socle(par, regime), par)


def _sans_nominale(valeurs):
    valeurs = sorted(valeurs, key=lambda z: (-abs(z), z.real, z.imag))
    i = min(range(len(valeurs)), key=lambda q: abs(valeurs[q] - 1))
    return valeurs[:i] + valeurs[i + 1:]


@lru_cache(maxsize=None)
def lectures(par, regime: str = "hausse", taux: str = "regle", financement: str = "F",
             B6: str = "regle") -> LecturesSocle:
    """Spectre brut, spectre restreint à la variété des identités et lecture (c) d'une carte du socle."""
    carte = carte_socle(par, regime, taux, financement, B6)
    J, J_var, Gs, inv = jacobiennes_carte(carte, par)
    k = len(carte.x0)
    G = gradients_identites(carte)
    PIB = etat_socle(parametres_etat(par, financement))[0]["PIB"]
    residu_identites = float(np.max(np.abs(G @ carte.x0) / np.linalg.norm(G, axis=1)) / PIB)
    residu_gauche = float(np.max(np.linalg.norm(Gs @ J - Gs * inv, axis=1) / np.linalg.norm(Gs, axis=1)))
    valeurs_variete = np.linalg.eigvals(J_var)
    ecart_nominal = float(np.min(np.abs(valeurs_variete - 1)))
    brutes, variete = _sans_nominale(np.linalg.eigvals(J)), _sans_nominale(valeurs_variete)
    multiple = lambda vs: sum(abs(z - inv) <= TOL_RACINE_MULTIPLE for z in vs)  # noqa: E731
    noyau = int(np.sum(np.linalg.svd(J - inv * np.eye(k), compute_uv=False) <= TOL_NOYAU))
    suivante = next(z for z in variete if abs(z - inv) > TOL_RACINE_MULTIPLE)
    tenus = tuple(sorted(nom for i, nom in enumerate(carte.noms)
                         if np.max(np.abs(J[i] - inv * np.eye(k)[i])) <= TOL_NOYAU))
    return LecturesSocle(inv, abs(brutes[0]), multiple(brutes), noyau, abs(variete[0]), multiple(variete),
                         complex(suivante), tenus, residu_gauche, residu_identites, ecart_nominal)


def lectures_socle(pi: float, regime: str) -> LecturesSocle:
    """`lectures` du socle à π̄ = π* = `pi`, règle budgétaire de référence."""
    return lectures(parametres_socle(pi), regime)


def rayon_c(par) -> float:
    """Lecture (c) du rayon, pire des deux régimes de l'emploi."""
    return max(lectures(par, regime).rayon_c for regime in ("hausse", "baisse"))


def nature_racine(z: complex) -> tuple[str, float | None]:
    """Nature d'une racine et période en tours : complexe (2π/|arg λ|), réelle négative (2), réelle positive."""
    if abs(z.imag) > 1e-12:
        return "complexe", 2 * math.pi / abs(math.atan2(z.imag, z.real))
    return ("réelle négative", 2.0) if z.real < 0 else ("réelle positive", None)


# Grille G de la fiche du bloc banque centrale (docs/blocs/banque_centrale.md, l. 340-345) : calibration
# indicative ; chaque vitesse ×0,5 et ×2 ; chaque gain ×0,5 et ×2 ; toutes les vitesses ×0,5, puis ×2 (les
# gains n'y entrent pas) ; deux régimes de l'emploi. k_I de la fiche est `a_I` (BC2).
VITESSES_GRILLE = ("lambda_v", "lambda_IN", "lambda_w", "lambda_N", "lambda_mu", "lambda_H", "lambda_ti",
                   "lambda_e")
GAINS_GRILLE = ("a_I", "a_pi", "psi_xi", "beta", "eta_r")
# Écart déclaré à la grille de la fiche : a_U n'est pas un paramètre du socle (absent de
# `etat_stationnaire.Parametres` ; BC1 sans terme d'activité sous M32), ses deux branches manquent (29 branches).
ABSENTS_GRILLE = ("a_U",)
# Ajout prospectif à la grille (décision du mainteneur du 15/10/2026) : ζ ×0,5 et ×2 (ζ ∈ {2 ; 4 ; 8}), verdicts
# publiés sur la grille G (29 branches) et sur la grille G augmentée (31 branches).
AJOUTS_GRILLE = ("zeta",)
# Marge conjointe (mesure publiée, relevée depuis sa citation) : gains de la boucle salaire -- taux réel multipliés ensemble.
GAINS_ENSEMBLE = ("beta", "a_pi", "eta_r")
BORNES_MARGE = (1.0, 2.0)  # intervalle encadrant du facteur commun (contrôlé par `frontiere`)


def branches_grille() -> tuple[tuple[str, tuple[tuple[str, float], ...]], ...]:
    """Branches de la grille G (banque_centrale.md, l. 340-345), sans a_U (absent du socle)."""
    branches: list[tuple[str, tuple[tuple[str, float], ...]]] = [("calibration", ())]
    for nom in VITESSES_GRILLE + GAINS_GRILLE:
        for f in (0.5, 2.0):
            branches.append((f"{nom} ×{f:g}", ((nom, f),)))
    for f in (0.5, 2.0):
        branches.append((f"vitesses ×{f:g}", tuple((nom, f) for nom in VITESSES_GRILLE)))
    return tuple(branches)


def branches_ajoutees() -> tuple[tuple[str, tuple[tuple[str, float], ...]], ...]:
    """Branches ajoutées à la grille G : ζ ×0,5 et ×2."""
    return tuple((f"{nom} ×{f:g}", ((nom, f),)) for nom in AJOUTS_GRILLE for f in (0.5, 2.0))


def branches_complementaires() -> tuple[tuple[str, tuple[tuple[str, float], ...]], ...]:
    """Mesures hors grille : β, a_π, η_r ensemble ×0,5 et ×2."""
    return tuple((f"{', '.join(GAINS_ENSEMBLE)} ×{f:g}", tuple((nom, f) for nom in GAINS_ENSEMBLE))
                 for f in (0.5, 2.0))


def _pire(branches) -> tuple[tuple[str, float], ...]:
    return tuple((nom, rayon_c(parametres_socle(0.02, facteurs=dict(fac)))) for nom, fac in branches)


@lru_cache(maxsize=None)
def grille_socle() -> tuple[tuple[str, float], ...]:
    """Grille G puis branches ajoutées, à π̄ = 2 % : lecture (c), pire des deux régimes, par branche."""
    return _pire(branches_grille() + branches_ajoutees())


def verdicts_grille(grille: tuple[tuple[str, float], ...] | None = None) -> dict[str, dict[str, object]]:
    """Verdicts sur la grille G (29 branches) et sur la grille G augmentée de ζ (31 branches).

    `grille` : (branche, rayon) dans l'ordre de `grille_socle`, par défaut `grille_socle()`.
    """
    grille = grille_socle() if grille is None else grille
    sortie = {}
    for nom, nb in (("G", len(branches_grille())), ("G + zeta", len(grille))):
        partie = grille[:nb]
        pire = max(partie, key=lambda x: x[1])
        sortie[nom] = {"branches": nb, "stables": sum(r < 1 for _, r in partie), "pire": pire[1],
                       "branche_pire": pire[0]}
    return sortie


@lru_cache(maxsize=None)
def complements_socle() -> tuple[tuple[str, float], ...]:
    """Mesures complémentaires à π̄ = 2 %, hors grille : lecture (c), pire des deux régimes, par branche."""
    return _pire(branches_complementaires())


def _ensemble(f: float):
    return parametres_socle(0.02, facteurs={nom: f for nom in GAINS_ENSEMBLE})


@lru_cache(maxsize=None)
def marge_conjointe() -> dict[str, object]:
    """Facteur commun de β, a_π et η_r où la lecture (c) passe 1 (pire des deux régimes, π̄ = 2 %), bissection.

    Rend aussi, au facteur 2, la racine (c) de chaque régime : rayon, nature et période.
    """
    f = frontiere(lambda x: rayon_c(_ensemble(x)), *BORNES_MARGE)
    regimes = {}
    for regime in ("hausse", "baisse"):
        z = lectures(_ensemble(2.0), regime).suivante
        nature, periode = nature_racine(z)
        regimes[regime] = {"rayon": abs(z), "nature": nature, "periode": periode}
    return {"facteur": f, "x2": regimes}


@lru_cache(maxsize=None)
def frontiere_marge(regime: str) -> float:
    """Facteur commun de β, a_π et η_r où la lecture (c) d'un seul régime de l'emploi passe 1 (π̄ = 2 %),
    bissection sur `BORNES_MARGE`."""
    return frontiere(lambda x: lectures(_ensemble(x), regime).rayon_c, *BORNES_MARGE)


def _ensemble_sans_aI(f_aI: float = 1e-3):
    """β, a_π et η_r ×2 et a_I ×`f_aI` (0,001 par défaut), π̄ = 2 % : branche où la boucle proportionnelle
    subsiste quand a_I tend vers 0."""
    return parametres_socle(0.02, facteurs={nom: 2.0 for nom in GAINS_ENSEMBLE} | {"a_I": f_aI})


def ecart_racine_reelle(f_aI: float) -> float | None:
    """1 − racine (c) du régime de hausse, β, a_π et η_r ×2 et a_I ×`f_aI`, π̄ = 2 % ; sans objet (None) si
    cette racine n'est pas réelle positive (mode nominal lent, proportionnel à a_I quand a_I tend vers 0)."""
    z = lectures(_ensemble_sans_aI(f_aI), "hausse").suivante
    return 1 - z.real if nature_racine(z)[0] == "réelle positive" else None


def module_paire(valeurs) -> float | None:
    """Module de la plus grande paire complexe (|Im λ| > 1e−12) ; sans objet (None) si le spectre est réel."""
    return max((abs(z) for z in valeurs if abs(z.imag) > 1e-12), default=None)


# --- Couverture des intérêts φ (bloc 9, E4) -----------------------------------------------------

PHI_TABLE = (0.0, 0.1, 0.25, 0.5)  # φ de la table de la fiche 9 (finances_publiques.md, § 7), φ = 1 : socle


def rayon_phi(pi: float, phi: float) -> float:
    """Lecture (c), pire des deux régimes, à couverture φ (E4) ; l'état résolu ne dépend pas de φ (T^cou nul)."""
    return rayon_c(replace(parametres_socle(pi), phi=phi))


@lru_cache(maxsize=None)
def phi_star(pi: float) -> float:
    """Couverture minimale qui stabilise : φ où la lecture (c) passe 1, bissection sur [0 ; 1]."""
    return frontiere(lambda phi: rayon_phi(pi, phi), 0.0, 1.0)


def doublement(rayon: float) -> float | None:
    """Temps de doublement d'un écart, ln 2/ln |λ| tours ; sans objet si |λ| ≤ 1."""
    return math.log(2) / math.log(rayon) if rayon > 1 else None


# --- Variantes écartées de F : seconde écriture (#65, #66) ------------------------------------------

CONFIGURATIONS_F = {"fiche": parametres_fiche, "socle": parametres_socle}
B6_CONFIGURATION = {"fiche": ("verse", "plancher"), "socle": ("regle",)}  # coude de B6 atteint dans « fiche »
LAMBDA_TI_F = (1.0, 2.0)  # facteur de λ_ti : base et ×2 (λ_ti = 0,04, vitesse des rayons de la fiche)


@lru_cache(maxsize=None)
def variantes_F() -> tuple[dict[str, object], ...]:
    """Lecture (c) de chaque variante de F, π̄ = 2 % : configuration, taux, B6, λ_ti, régime de T4.

    Le contrôle des coudes (`ecart_avant_arriere`) est publié pour chaque carte ; dans la configuration
    « fiche », il est aussi publié sur B6 tel qu'écrit (« regle »), pour montrer le coude que les deux branches
    linéarisées séparément évitent.
    """
    sortie = []
    for config, parametres in CONFIGURATIONS_F.items():
        for f_ti in LAMBDA_TI_F:
            par = parametres(0.02)
            par = replace(par, lambda_ti=par.lambda_ti * f_ti)
            for taux in TAUX_SOCLE:
                for B6 in B6_CONFIGURATION[config]:
                    for financement in FINANCEMENTS:
                        for regime in ("hausse", "baisse"):
                            x = lectures(par, regime, taux, financement, B6)
                            carte = carte_socle(par, regime, taux, financement, B6)
                            nature, periode = nature_racine(x.suivante)
                            ligne = {"configuration": config, "lambda_ti": par.lambda_ti, "taux": taux, "B6": B6,
                                     "financement": financement, "regime": regime, "rayon": x.rayon_c,
                                     "racine": [x.suivante.real, x.suivante.imag], "nature": nature,
                                     "periode": periode, "rayon_brut": x.rayon_brut,
                                     "coude": ecart_avant_arriere(carte),
                                     "residu": residu_point_fixe(carte), "residu_gauche": x.residu_gauche}
                            # B6 écrit : même carte pour les deux branches, publiée une fois.
                            if B6 == B6_CONFIGURATION["fiche"][0] and config == "fiche":
                                ligne["coude_B6_ecrit"] = ecart_avant_arriere(
                                    carte_socle(par, regime, taux, financement, "regle"))
                            sortie.append(ligne)
    return tuple(sortie)


def cas_controles() -> tuple[tuple[str, object, str, str, str, str], ...]:
    """Cartes du socle dont la lecture (c) est publiée, pour les contrôles du code de sortie (`controles_tenus`).

    (étiquette, paramètres, régime, taux, financement, B6) : six cas du socle (π̄ = 0, 2 et 10 %), grille G
    augmentée (π̄ = 2 %), mesures complémentaires, table φ et φ* (π̄ = 2 et 10 %), marge conjointe (frontière
    des deux régimes, frontière du régime de hausse, ×2, ×2 avec a_I ×0,001 et ×0,01), grille G augmentée à
    π̄ = 0 et 10 %, variantes de F. Ordre fixe ; un cas présent dans deux familles est contrôlé deux fois.
    """
    cas = []
    regimes = ("hausse", "baisse")
    for pi in (0.0, 0.02, 0.10):
        cas += [(f"socle π̄ = {pi:g}", parametres_socle(pi), r, "regle", "F", "regle") for r in regimes]
    for nom, fac in branches_grille() + branches_ajoutees() + branches_complementaires():
        cas += [(f"grille {nom}", parametres_socle(0.02, facteurs=dict(fac)), r, "regle", "F", "regle")
                for r in regimes]
    for pi in (0.02, 0.10):
        for phi in PHI_TABLE + (phi_star(pi),):
            cas += [(f"φ = {phi:g}, π̄ = {pi:g}", replace(parametres_socle(pi), phi=phi), r, "regle", "F", "regle")
                    for r in regimes]
    for f in (marge_conjointe()["facteur"], frontiere_marge("hausse"), 2.0):
        cas += [(f"marge ×{f:g}", _ensemble(f), r, "regle", "F", "regle") for r in regimes]
    for f_aI, nom in ((1e-3, "0,001"), (1e-2, "0,01")):
        cas += [(f"marge ×2, a_I ×{nom}", _ensemble_sans_aI(f_aI), r, "regle", "F", "regle") for r in regimes]
    for pi in (0.0, 0.10):
        for nom, fac in branches_grille() + branches_ajoutees():
            cas += [(f"grille {nom}, π̄ = {pi:g}", parametres_socle(pi, facteurs=dict(fac)), r, "regle", "F", "regle")
                    for r in regimes]
    for config, parametres in CONFIGURATIONS_F.items():
        for f_ti in LAMBDA_TI_F:
            par = parametres(0.02)
            par = replace(par, lambda_ti=par.lambda_ti * f_ti)
            for taux in TAUX_SOCLE:
                for B6 in B6_CONFIGURATION[config]:
                    for financement in FINANCEMENTS:
                        cas += [(f"variante {config} λ_ti = {par.lambda_ti:g} {taux} B6 {B6} {financement}", par, r,
                                 taux, financement, B6) for r in regimes]
    return tuple(cas)


def tenus_et_nominales() -> tuple[int, list[str], float]:
    """Sur `cas_controles` : nombre de cas, cas dont les racines en 1/Γ̄ de la variété ne sont pas celles de
    `TENUS_ATTENDUS` (multiplicité comprise), plus grand |λ − 1| de la racine nominale."""
    cas = cas_controles()
    hors, nominale = [], 0.0
    for etiquette, par, regime, taux, financement, B6 in cas:
        x = lectures(par, regime, taux, financement, B6)
        nominale = max(nominale, x.ecart_nominal)
        if x.tenus_en_niveau != TENUS_ATTENDUS or x.multiplicite_variete != len(TENUS_ATTENDUS):
            hors.append(f"{etiquette} {regime} : {x.multiplicite_variete} en 1/Γ̄, tenus {list(x.tenus_en_niveau)}")
    return len(cas), hors, nominale


def residu_cas_controles() -> float:
    """Plus grand résidu du point fixe (`residu_point_fixe`) sur les cartes de `cas_controles`."""
    return max(residu_point_fixe(carte_socle(par, regime, taux, financement, B6))
               for _, par, regime, taux, financement, B6 in cas_controles())


# --- Relevé des chiffres cités --------------------------------------------------------------


@dataclass(frozen=True)
class Chiffre:
    """Un chiffre cité par la spécification et sa remesure."""

    ident: str
    publie: str  # tel qu'écrit dans la spécification, virgule décimale
    motif: str  # chaîne cherchée dans le texte LaTeX
    nature: str  # rayon, période, demi-vie, frontière, marge, écart à 1
    maquette: str
    hypothese: str
    calcul: object  # () -> float
    # Paragraphes (labels de `PARAGRAPHES`) et fiches (fichiers de `LIGNES_FICHES`) où le chiffre est cité :
    # le motif n'est cherché que là, et un nombre recensé n'est couvert que par un chiffre qui y déclare son
    # paragraphe (un nombre égal cité ailleurs, pour une autre grandeur, ne passe pas par coïncidence).
    ou: tuple[str, ...] = ()


def _r(carte_de):
    return lambda: spectre(carte_de()).rayon


def _per(carte_de):
    return lambda: spectre(carte_de()).periode


M4 = (0.5, 0.6, 0.7, 0.8)


def _moins(a: float, b: float | None) -> float | None:
    return None if b is None else a - b


def _mise_a_echelle(x: float | None, exposant: int) -> float | None:
    """x en unités de 10^-exposant ; sans objet (None) reste sans objet."""
    return None if x is None else x * 10 ** exposant


def _extremes(fonction, valeurs, quel):
    """Extrême sur `valeurs` ; sans objet (None) si une valeur l'est (racine réelle, rayon ≥ 1)."""
    def calcul():
        xs = [fonction(x) for x in valeurs]
        return None if any(x is None for x in xs) else (min if quel == "min" else max)(xs)
    return calcul


def releve() -> list[Chiffre]:
    """Liste des chiffres cités, dans l'ordre de la spécification, avec leur calcul."""
    L: list[Chiffre] = []
    courant: list[tuple[str, ...]] = [()]  # paragraphes de citation du groupe en cours (`ou` par défaut)

    def ajouter(ident, publie, nature, maquette, hypothese, calcul, motif=None, ou=None):
        L.append(Chiffre(ident, publie, motif or publie, nature, maquette, hypothese, calcul,
                         courant[0] if ou is None else ou))

    # sec:travail-conditions : boucle combinée production -- stocks -- emploi, prix figé ; les bornes (m = 0,5
    # et 0,8) sont rappelées par sec:prix-conditions.
    courant[0] = ("sec:travail-conditions",)
    for m, r, per in zip(M4, ("0,9279", "0,9452", "0,9612", "0,9762"), ("68,9", "72,9", "80,7", "95,8")):
        ou = ("sec:travail-conditions", "sec:prix-conditions") if m in (0.5, 0.8) else None
        ajouter(f"travail.rayon.m{m}", r, "rayon", "offre", f"prix figé, m = {m}", _r(lambda m=m: carte_offre(m)),
                ou=ou)
        ajouter(f"travail.periode.m{m}", per, "période", "offre", f"prix figé, m = {m}",
                _per(lambda m=m: carte_offre(m)), ou=ou)
    ajouter("travail.marge_bande.m0.8", "0,16", "marge", "offre", "96 tours moins la période à m = 0,8",
            lambda: _moins(96, spectre(carte_offre(0.8)).periode), motif="marge de 0,16")
    for quel, pub in (("min", "141,9"), ("max", "184,5")):
        ajouter(f"travail.periode.vitesses÷2.{quel}", pub, "période", "offre", "λ_v, λ_IN ÷ 2, m = 0,5 à 0,8",
                _extremes(lambda m: spectre(carte_offre(m, lambda_v=1.5, lambda_IN=0.75)).periode, M4, quel))
    for quel, pub in (("min", "34,3"), ("max", "52,2")):
        ajouter(f"travail.periode.vitesses×2.{quel}", pub, "période", "offre", "λ_v, λ_IN × 2, m = 0,5 à 0,8",
                _extremes(lambda m: spectre(carte_offre(m, lambda_v=6.0, lambda_IN=3.0)).periode, M4, quel))

    # sec:prix-conditions : boucle prix -- stocks -- demande.
    courant[0] = ("sec:prix-conditions",)
    for m, r, per in zip(M4, ("0,9420", "0,9535", "0,9658", "0,9783"), ("93,8", "94,3", "100,4", "115,5")):
        ajouter(f"prix.rayon.m{m}", r, "rayon", "offre", f"règle P1 à P3, coût exogène, m = {m}",
                _r(lambda m=m: carte_offre(m, "regle")))
        ajouter(f"prix.periode.m{m}", per, "période", "offre", f"règle P1 à P3, coût exogène, m = {m}",
                _per(lambda m=m: carte_offre(m, "regle")))
    variantes_prix = (
        ("vitesses÷2", {"lambda_v": 1.5, "lambda_IN": 0.75}, ("0,9700", "0,9878"), ("169", "218")),
        ("vitesses×2", {"lambda_v": 6.0, "lambda_IN": 3.0}, ("0,8791", "0,9647"), ("43", "60")),
        ("psi×2", {"psi_xi": 1.0}, ("0,9534", "0,9813"), None),
        ("lambda_mu÷2", {"lambda_mu": 0.6}, ("0,9400", "0,9733"), None),
        ("lambda_mu×2", {"lambda_mu": 2.4}, ("0,9477", "0,9808"), None),
    )
    for nom, kw, rayons, periodes in variantes_prix:
        for quel, pub in zip(("min", "max"), rayons):
            ajouter(f"prix.rayon.{nom}.{quel}", pub, "rayon", "offre", f"règle P1 à P3, {nom}, m = 0,5 à 0,8",
                    _extremes(lambda m, kw=kw: spectre(carte_offre(m, "regle", **kw)).rayon, M4, quel))
        if periodes:
            for quel, pub in zip(("min", "max"), periodes):
                ajouter(f"prix.periode.{nom}.{quel}", pub, "période", "offre",
                        f"règle P1 à P3, {nom}, m = 0,5 à 0,8",
                        _extremes(lambda m, kw=kw: spectre(carte_offre(m, "regle", **kw)).periode, M4, quel),
                        motif=f"{periodes[0]} à {periodes[1]}")
    ajouter("prix.frontiere_psi", "13{,}0", "frontière", "offre", "ψ_ξ où le rayon passe 1, m = 0,8",
            lambda: frontiere(lambda p: spectre(carte_offre(0.8, "regle", psi_xi=p)).rayon, 10.0, 20.0))
    ajouter("prix.frontiere_psi.vitesses×2", "4{,}875", "frontière", "offre",
            "ψ_ξ où le rayon passe 1, m = 0,8, λ_v et λ_IN × 2",
            lambda: frontiere(lambda p: spectre(carte_offre(0.8, "regle", lambda_v=6.0, lambda_IN=3.0,
                                                            psi_xi=p)).rayon, 2.0, 8.0))
    ajouter("prix.rayon.psi10.m0.8", "0,9949", "rayon", "offre", "ψ_ξ = 10, m = 0,8",
            _r(lambda: carte_offre(0.8, "regle", psi_xi=10.0)))

    # sec:prix-conditions : boucle salaires -- prix.
    for m, r in zip(M4, ("0,8969", "0,9068", "0,9225", "0,9385")):
        ajouter(f"salaires_prix.rayon.m{m}", r, "rayon", "offre", f"P1 à P3, T2, T3, π^e = π̄, m = {m}",
                _r(lambda m=m: carte_offre(m, "regle", True)))
    variantes_sp = (
        ("toutes÷2", {"lambda_v": 1.5, "lambda_IN": 0.75, "lambda_mu": 0.6, "lambda_w": 0.5}, ("0,9479", "0,9714")),
        ("toutes×2", {"lambda_v": 6.0, "lambda_IN": 3.0, "lambda_mu": 2.4, "lambda_w": 2.0}, ("0,8070", "0,8583")),
        ("lambda_w×2", {"lambda_w": 2.0}, ("0,9322", "0,9351")),
        ("psi×2", {"psi_xi": 1.0}, ("0,9163", "0,9346")),
    )
    for nom, kw, rayons in variantes_sp:
        for quel, pub in zip(("min", "max"), rayons):
            ajouter(f"salaires_prix.rayon.{nom}.{quel}", pub, "rayon", "offre",
                    f"P1 à P3, T2, T3, {nom}, m = 0,5 à 0,8",
                    _extremes(lambda m, kw=kw: spectre(carte_offre(m, "regle", True, **kw)).rayon, M4, quel))
    ajouter("salaires_prix.rayon.marge_constante.m0.6", "0,9172", "rayon", "offre",
            "marge constante μ̄, T2, T3, m = 0,6", _r(lambda: carte_offre(0.6, "marge", True)))
    ajouter("salaires_prix.racine_nominale", "10^{-9}", "racine nominale", "offre",
            "plus grand |λ − 1| de la racine nominale, m = 0,5 à 0,8",
            lambda: max(spectre(carte_offre(m, "regle", True)).ecart_nominal for m in M4),
            motif="au plus $10^{-9}$")

    # sec:menages-conditions : boucle conjointe (lecture de la cible).
    courant[0] = ("sec:menages-conditions",)
    for th, pubs in ((0.8, ("0,9640", "0,9617")), (1.0, ("0,9564", "0,9537"))):
        for regime, pub in zip(("hausse", "baisse"), pubs):
            ajouter(f"menages.rayon.theta{th}.{regime}", pub, "rayon", "menages",
                    f"lecture de la cible, θ_H = {th}, régime de {regime}",
                    _r(lambda th=th, regime=regime: carte_menages(th, regime)))
    for regime, pub in (("hausse", "0,9563"), ("baisse", "0,9535")):
        ajouter(f"menages.rayon.theta1.0.cout_moyen.{regime}", pub, "rayon", "menages",
                f"lecture de la cible, θ_H = 1, stocks au coût moyen pondéré de N8, régime de {regime}",
                _r(lambda regime=regime: carte_menages(1.0, regime, resultat="cout_moyen")))

    # sec:menages-inflation et instabilité 17 : lectures sur le glissement.
    courant[0] = ("sec:menages-inflation",)
    for th, pubs in ((0.8, ("1,030357", "1,005801")), (1.0, ("1,059130", "1,060998"))):
        for regime, pub in zip(("hausse", "baisse"), pubs):
            ajouter(f"menages_inflation.a_entretien.theta{th}.{regime}", pub, "rayon", "menages",
                    f"lecture (a), glissement dans le seul terme d'entretien de H4, θ_H = {th}, régime de {regime}",
                    _r(lambda th=th, regime=regime: carte_menages(th, regime, "a_entretien")))
    ins = ("sec:menages-inflation", "tab:instabilites")
    for lecture, th, pubs in (("hs_glissement", 0.8, ("0,9967", "0,9742")), ("hs_glissement", 1.0, ("1,0231", "1,0271")),
                              ("hs_glissement_pas", 0.8, ("0,9823", "0,9748")),
                              ("hs_glissement_pas", 1.0, ("1,0223", "1,0218"))):
        for regime, pub in zip(("hausse", "baisse"), pubs):
            ajouter(f"menages_inflation.{lecture}.theta{th}.{regime}", pub, "rayon", "menages",
                    f"{lecture}, θ_H = {th}, régime de {regime}",
                    _r(lambda lecture=lecture, th=th, regime=regime: carte_menages(th, regime, lecture)),
                    ou=ins if (lecture, th) == ("hs_glissement_pas", 1.0) else None)
    hs_pas = [(th, regime) for th in (0.8, 1.0) for regime in ("hausse", "baisse")]
    for quel, pub in (("min", "49"), ("max", "60")):
        ajouter(f"menages_inflation.hs_glissement_pas.periode.{quel}", pub, "période", "menages",
                "hs_glissement_pas, deux θ_H, deux régimes",
                _extremes(lambda a: spectre(carte_menages(a[0], a[1], "hs_glissement_pas")).periode, hs_pas, quel),
                motif="49 à 60", ou=ins)
    lect_a = [(th, regime) for th in (0.8, 1.0) for regime in ("hausse", "baisse")]
    for quel, pub in (("min", "17"), ("max", "19")):
        ajouter(f"menages_inflation.a.periode.{quel}", pub, "période", "menages",
                "lecture (a), deux θ_H, deux régimes",
                _extremes(lambda a: spectre(carte_menages(a[0], a[1], "a")).periode, lect_a, quel),
                motif="17 à 19 tours", ou=ins)
    courant[0] = ("tab:instabilites",)
    for th, pubs in ((0.8, ("1,0275", "1,0029")), (1.0, ("1,0561", "1,0580"))):
        for regime, pub in zip(("hausse", "baisse"), pubs):
            ajouter(f"instabilite17.a.theta{th}.{regime}", pub, "rayon", "menages",
                    f"lecture (a), θ_H = {th}, régime de {regime}",
                    _r(lambda th=th, regime=regime: carte_menages(th, regime, "a")))
    ajouter("instabilite17.frontiere_nu_H", "0{,}586", "frontière", "menages",
            "ν_H où le rayon passe 1, lecture (a), θ_H = 0,8, régime de hausse",
            lambda: frontiere(lambda nu: spectre(carte_menages(0.8, "hausse", "a", nu_H=nu)).rayon, 0.3, 1.0))
    ajouter("instabilite17.frontiere_h", "0{,}604", "frontière", "menages",
            "poids h où le rayon passe 1, lecture (a), θ_H = 0,8, régime de hausse",
            lambda: frontiere(lambda h: spectre(carte_menages(0.8, "hausse", "a", h=h)).rayon, 0.3, 1.0))
    ajouter("instabilite17.a.n_a4.hausse", "1,0415", "rayon", "menages",
            "lecture (a), θ_H = 0,8, régime de hausse, n_a = 4 (valeur de la fiche ; la spécification cite aussi "
            "la contre-épreuve, ligne suivante ; la valeur à retenir revient à macro)",
            _r(lambda: carte_menages(0.8, "hausse", "a", n_a=4)), ou=("sec:changements-v3x",))
    ajouter("instabilite17.a.n_a4.hausse.contre_epreuve", "1,09", "rayon", "menages",
            "lecture (a), θ_H = 0,8, régime de hausse, n_a = 4 (contre-épreuve citée par la spécification)",
            _r(lambda: carte_menages(0.8, "hausse", "a", n_a=4)), motif="1,09 contre", ou=("sec:changements-v3x",))

    # sec:investissement-conditions : boucle investissement -- demande (boucle réduite).
    courant[0] = ("sec:investissement-conditions",)
    M3 = (0.6, 0.7, 0.8)
    for nom, lti, pubs in (("calibration", BASE.lambda_ti, ("0,9975", "0,9977", "0,9986")),
                           ("lambda_ti÷2", BASE.lambda_ti / 2, ("0,9992", "0,9991", "0,9987")),
                           ("lambda_ti×2", BASE.lambda_ti * 2, ("0,9978", "0,9983", "1,0003"))):
        for m, pub in zip(M3, pubs):
            ajouter(f"investissement.rayon.{nom}.m{m}", pub, "rayon", "investissement",
                    f"2 ans de capital, {nom}, m = {m}", _r(lambda m=m, lti=lti: carte_investissement(m, 2.0, lti)))
    for ans, ms, pubs in ((2.0, M3, ("0,157", "0,097", "0,036")), (3.0, (0.6, 0.7), ("0,077", "0,037"))):
        for m, pub in zip(ms, pubs):
            ajouter(f"investissement.frontiere_lambda_ti.{ans:g}ans.m{m}", pub, "frontière", "investissement",
                    f"λ_ti où le rayon passe 1, {ans:g} ans de capital, m = {m}",
                    lambda m=m, ans=ans: frontiere(lambda l: spectre(carte_investissement(m, ans, l)).rayon,
                                                   0.005, 0.5),
                    ou=("sec:investissement-conditions", "tab:calibration") if ans == 2.0 else None)
    ajouter("investissement.racine_lente", "0{,}99255", "rayon", "forme fermée",
            "(1 − δ/n_a)/[(1 + g)^{1/n_a}(1 + π̄)^{1/n_a}], π̄ = 2 % (non une maquette)",
            lambda: (1 - BASE.delta / 12) / (_cadre(BASE)["Gam"]))

    # sec:banque_centrale-conditions et sec:finances_publiques-conditions : socle, blocs 2 à 9, lecture (c).
    # Les valeurs barrées (\barre, anciennes E12) ne sont pas recensées ; la fiche 9 garde les siennes (φ = 1).
    socle_bc, socle_fp = ("sec:banque_centrale-conditions",), ("sec:finances_publiques-conditions",)
    courant[0] = socle_bc + socle_fp
    for pi, pub in ((0.0, "0,997390"), (0.02, "0,997118"), (0.10, "0,997045")):
        for regime in ("hausse", "baisse"):
            ajouter(f"socle.rayon.pi{pi:g}.{regime}", pub, "rayon", "socle",
                    f"blocs 2 à 9, π̄ = π* = {pi:.0%}, ν_G = {NU_G:g}, régime de {regime}, lecture (c) : variété des "
                    f"identités, hors des racines en 1/Γ̄ des stocks tenus en niveau ({', '.join(TENUS_ATTENDUS)}, "
                    "déclarées à part)",
                    lambda pi=pi, regime=regime: lectures_socle(pi, regime).rayon_c)
    # Racine dominante à 10 % : paire complexe, relevée en régime de hausse (période de la spécification).
    ajouter("socle.racine.pi0.1.hausse.reelle", "0,997043", "racine", "socle",
            "partie réelle de la racine dominante (c), π̄ = 10 %, régime de hausse",
            lambda: lectures_socle(0.10, "hausse").suivante.real, ou=socle_bc)
    ajouter("socle.racine.pi0.1.hausse.imaginaire", "0,001732", "racine", "socle",
            "|partie imaginaire| de la racine dominante (c), π̄ = 10 %, régime de hausse",
            lambda: abs(lectures_socle(0.10, "hausse").suivante.imag), ou=socle_bc)
    ajouter("socle.racine.pi0.1.baisse.imaginaire", "0,001731", "racine", "socle",
            "|partie imaginaire| de la racine dominante (c), π̄ = 10 %, régime de baisse",
            lambda: abs(lectures_socle(0.10, "baisse").suivante.imag), ou=socle_bc)
    ajouter("socle.periode.pi0.1.hausse", "3617", "période", "socle",
            "2π/|arg λ| de la racine dominante (c), π̄ = 10 %, régime de hausse",
            lambda: nature_racine(lectures_socle(0.10, "hausse").suivante)[1], motif="3\\,617", ou=socle_bc)
    ajouter("socle.demi_vie.pi0.02", "240", "demi-vie", "socle",
            "ln 0,5/ln du rayon à 2 % (lecture (c), régime de hausse)",
            lambda: math.log(0.5) / math.log(lectures_socle(0.02, "hausse").rayon_c), motif="240")
    ajouter("socle.demi_vie.pi0", "265", "demi-vie", "socle",
            "ln 0,5/ln du rayon à 0 % (lecture (c), régime de hausse)",
            lambda: math.log(0.5) / math.log(lectures_socle(0.0, "hausse").rayon_c), motif="265", ou=socle_bc)
    for pi, pub in ((0.0, "0,998351"), (0.02, "0,996705"), (0.10, "0,990453")):
        ajouter(f"socle.inv_gamma.pi{pi:g}", pub, "racine", "socle",
                f"1/Γ̄ à π̄ = {pi:.0%}, racine double des stocks tenus en niveau ({', '.join(TENUS_ATTENDUS)})",
                lambda pi=pi: lectures_socle(pi, "hausse").inv_gamma, ou=socle_bc)
    ajouter("socle.grille.pire", "0,998732", "rayon", "socle",
            f"pire branche de la grille G (banque_centrale.md, l. 340-345 : {len(VITESSES_GRILLE)} vitesses et "
            f"{len(GAINS_GRILLE)} gains ×0,5 et ×2, toutes les vitesses ×0,5 et ×2 ; {len(branches_grille())} "
            f"branches, sans {', '.join(ABSENTS_GRILLE)} ; deux régimes ; lecture (c))",
            lambda: verdicts_grille()["G"]["pire"])
    ajouter("socle.grille.vitesses÷2", "0,998437", "rayon", "socle",
            "toutes les vitesses de la grille G ×0,5, pire des deux régimes, lecture (c)",
            lambda: dict(grille_socle())["vitesses ×0.5"], ou=socle_bc)
    ajouter("socle.grille_zeta.pire", "0,998802", "rayon", "socle",
            f"pire branche de la grille G augmentée de {', '.join(AJOUTS_GRILLE)} ×0,5 et ×2 "
            f"({len(grille_socle())} branches, deux régimes, lecture (c))",
            lambda: verdicts_grille()["G + zeta"]["pire"])
    # Les deux grilles jugées aux trois π̄ (décision du mainteneur du 15/10/2026) : π̄ = 2 % ci-dessus.
    for pi, pub_g, pub_z in ((0.0, "0,998702", "0,998742"), (0.10, "0,998772", "0,998885")):
        grille_pi = lambda pi=pi: tuple((nom, rayon_c(parametres_socle(pi, facteurs=dict(fac))))
                                        for nom, fac in branches_grille() + branches_ajoutees())
        ajouter(f"socle.grille.pire.pi{pi:g}", pub_g, "rayon", "socle",
                f"pire branche de la grille G, π̄ = π* = {pi:.0%}, deux régimes, lecture (c)",
                lambda g=grille_pi: verdicts_grille(g())["G"]["pire"], ou=socle_bc)
        ajouter(f"socle.grille_zeta.pire.pi{pi:g}", pub_z, "rayon", "socle",
                f"pire branche de la grille G augmentée de {', '.join(AJOUTS_GRILLE)} ×0,5 et ×2, "
                f"π̄ = π* = {pi:.0%}, deux régimes, lecture (c)",
                lambda g=grille_pi: verdicts_grille(g())["G + zeta"]["pire"], ou=socle_bc)
    ajouter("socle.marge_conjointe.facteur", "1,7135", "frontière", "socle",
            f"facteur commun de {', '.join(GAINS_ENSEMBLE)} où la lecture (c) passe 1, pire des deux régimes, "
            "π̄ = 2 %", lambda: marge_conjointe()["facteur"])
    ajouter("socle.marge_conjointe.facteur.hausse", "1,9921", "frontière", "socle",
            f"facteur commun de {', '.join(GAINS_ENSEMBLE)} où la lecture (c) du régime de hausse passe 1, "
            "π̄ = 2 %", lambda: frontiere_marge("hausse"))
    for regime, pub, per in (("baisse", "1,027785", "19,3"), ("hausse", "1,000644", "17,0")):
        ajouter(f"socle.marge_conjointe.x2.{regime}", pub, "rayon", "socle",
                f"{', '.join(GAINS_ENSEMBLE)} ×2, régime de {regime}, lecture (c), π̄ = 2 %",
                lambda regime=regime: marge_conjointe()["x2"][regime]["rayon"], ou=socle_bc)
        ajouter(f"socle.marge_conjointe.x2.{regime}.periode", per, "période", "socle",
                f"{', '.join(GAINS_ENSEMBLE)} ×2, régime de {regime}, période de la paire complexe (c)",
                lambda regime=regime: marge_conjointe()["x2"][regime]["periode"], ou=socle_bc)
    ajouter("socle.marge_conjointe.x0.5", "0,998047", "rayon", "socle",
            f"{', '.join(GAINS_ENSEMBLE)} ×0,5, pire des deux régimes, lecture (c), π̄ = 2 %",
            lambda: rayon_c(_ensemble(0.5)), ou=socle_bc)
    ajouter("socle.marge_conjointe.x2.a_I÷1000", "1,0265", "rayon", "socle",
            f"{', '.join(GAINS_ENSEMBLE)} ×2 et a_I ×0,001, pire des deux régimes, lecture (c), π̄ = 2 %",
            lambda: rayon_c(_ensemble_sans_aI()), ou=socle_bc)
    ajouter("socle.marge_conjointe.x2.a_I÷1000.hausse", "0,999994", "rayon", "socle",
            f"{', '.join(GAINS_ENSEMBLE)} ×2 et a_I ×0,001, régime de hausse, π̄ = 2 %, lecture (c), racine "
            "réelle",
            lambda: lectures(_ensemble_sans_aI(), "hausse").rayon_c, ou=socle_bc)
    # Écart à 1 de cette racine réelle, publié en 10⁻⁶ (a_I ÷ 1000) et en 10⁻⁵ (a_I ÷ 100) : remesure mise
    # à l'échelle de la puissance de dix publiée.
    for nom, f_aI, exposant in (("a_I÷1000", 1e-3, 6), ("a_I÷100", 1e-2, 5)):
        ajouter(f"socle.marge_conjointe.x2.{nom}.hausse.ecart", "6,2", "écart à 1", "socle",
                f"{', '.join(GAINS_ENSEMBLE)} ×2 et a_I ×{f_aI:g}, régime de hausse, π̄ = 2 % : "
                f"1 − racine réelle de la lecture (c), en 10^-{exposant}",
                lambda f_aI=f_aI, exposant=exposant: _mise_a_echelle(ecart_racine_reelle(f_aI), exposant),
                motif=f"6{{,}}2 \\cdot 10^{{-{exposant}}}", ou=socle_bc)
    # Module de la paire complexe, non le rayon (c) : celui-ci est porté par une racine réelle (0,999994).
    ajouter("socle.marge_conjointe.x2.a_I÷1000.hausse.paire", "0,9993", "racine", "socle",
            f"{', '.join(GAINS_ENSEMBLE)} ×2 et a_I ×0,001, régime de hausse, π̄ = 2 % : module de la plus grande "
            "paire complexe du spectre restreint à la variété des identités",
            lambda: module_paire(np.linalg.eigvals(
                jacobiennes_carte(carte_socle(_ensemble_sans_aI(), "hausse"), _ensemble_sans_aI())[1])),
            ou=socle_bc)

    # sec:finances_publiques-impots, sec:ecartees et fiche 9 (finances_publiques.md, § 7) : couverture φ (E4).
    # La table de la fiche 9 est antérieure à l'amendement de E12 du 04/10/2026 : ses valeurs non nulles en φ
    # sont des écarts déclarés par la spécification (valeurs barrées) ; la fiche ne les barre pas.
    impots, ecartees = ("sec:finances_publiques-impots",), ("sec:ecartees",)
    fiche9 = ("docs/blocs/finances_publiques.md",)
    for pi, pub in ((0.02, "0,174"), (0.10, "0,650")):
        ajouter(f"finances.phi_star.pi{pi:g}", pub, "frontière", "socle",
                f"couverture φ de E4 où la lecture (c) passe 1, pire des deux régimes, π̄ = {pi:.0%}",
                lambda pi=pi: phi_star(pi), ou=impots + ecartees)
    table_phi = {0.02: ("1,001818", "1,000575", "0,999076", "0,997792", "0,997486"),
                 0.10: ("1,011036", "1,008794", "1,005564", "0,999488", "0,997558")}
    for pi, pubs in table_phi.items():
        for phi, pub in zip(PHI_TABLE + (1.0,), pubs):
            ajouter(f"finances.rayon.phi{phi:g}.pi{pi:g}", pub, "rayon", "socle",
                    f"couverture φ = {phi:g} (E4), π̄ = {pi:.0%}, pire des deux régimes, lecture (c)"
                    + ("" if phi == 0.0 else " ; valeur de la fiche 9, mesurée avant l'amendement de E12"),
                    lambda pi=pi, phi=phi: rayon_phi(pi, phi), ou=fiche9 + (impots if phi == 0.0 else ()))
    for pi, pub in ((0.02, "0,998471"), (0.10, "1,002898")):
        ajouter(f"finances.rayon.phi0.5.pi{pi:g}.specification", pub, "rayon", "socle",
                f"couverture φ = 0,5 (E4), π̄ = {pi:.0%}, pire des deux régimes, lecture (c)",
                lambda pi=pi: rayon_phi(pi, 0.5), ou=impots)
    ajouter("finances.rayon.phi0.5.pi0.1.ecartees", "1,0029", "rayon", "socle",
            "couverture φ = 0,5 (E4), π̄ = 10 %, pire des deux régimes, lecture (c)",
            lambda: rayon_phi(0.10, 0.5), motif="rayon 1,0029", ou=ecartees)
    for pi, pub, motif in ((0.02, "382", "382"), (0.10, "63", "63 tours")):
        ajouter(f"finances.doublement.phi0.pi{pi:g}", pub, "doublement", "socle",
                f"ln 2/ln du rayon à φ = 0, π̄ = {pi:.0%} (pays joué, lecture (c))",
                lambda pi=pi: doublement(rayon_phi(pi, 0.0)), motif=motif, ou=impots)
    return L


# --- Lignes de la spécification et recensement ------------------------------------------------

# Paragraphes où la spécification cite des rayons et des périodes de boucles conjointes : (section ou
# tableau, en-tête qui identifie la ligne du paragraphe dans le source LaTeX).
PARAGRAPHES = (
    ("sec:travail-conditions", r"\textbf{Boucle combinée production"),
    ("sec:prix-conditions", r"\textbf{Boucle prix -- stocks -- demande.}"),
    ("sec:prix-conditions", r"\textbf{Boucle salaires -- prix.}"),
    ("sec:menages-inflation", r"\item \textbf{Stabilité.}"),
    ("sec:menages-conditions", r"\textbf{Boucle conjointe.}"),
    ("sec:investissement-conditions", r"\textbf{Boucle investissement -- demande.}"),
    ("sec:banque_centrale-conditions", r"\textbf{Stabilité, mesurée en maquette}"),
    ("sec:finances_publiques-conditions", r"\textbf{Stabilité, mesurée en maquette}"),
    ("tab:calibration", r"$\lambda_{\mathit{ti}}$ &"),
    ("tab:instabilites", "17 & "),
    ("sec:changements-v3x", "1,0415"),
    ("sec:finances_publiques-impots", r"\emph{Pays joué}"),
    ("sec:ecartees", r"\textbf{Couverture des intérêts en curseur continu}"),
)

# Lignes des fiches comparatives où sont publiés des chiffres du relevé que la spécification ne cite pas :
# (fichier relatif à la racine, début exact de la ligne). Table φ de la fiche 9 (finances_publiques.md, § 7,
# « Réponses aux huit questions de `macro` », point 2).
LIGNES_FICHES = (
    ("docs/blocs/finances_publiques.md", "     | π̄ = 2 % : rayon |"),
    ("docs/blocs/finances_publiques.md", "     | π̄ = 10 % : rayon |"),
)

# Nombres recensés dans ces paragraphes qui ne sont ni un rayon, ni une période, ni une demi-vie, ni une
# frontière de boucle conjointe : valeurs d'entrée de la maquette, autres grandeurs (trajectoires simulées,
# gains statiques, formes fermées), hors objet de #65. Clé : (section ou tableau, nombre tel que recensé).
_ENTREE_M = "entrée de la maquette : propension m"
EXCLUS: dict[tuple[str, str], str] = {
    ("sec:travail-conditions", "0,5"): _ENTREE_M,
    ("sec:travail-conditions", "0,6"): _ENTREE_M,
    ("sec:travail-conditions", "0,7"): _ENTREE_M,
    ("sec:travail-conditions", "0,8"): _ENTREE_M,
    ("sec:travail-conditions", "96"): "borne de la bande de périodes exigée (critère), non une mesure",
    ("sec:prix-conditions", "0,5"): _ENTREE_M,
    ("sec:prix-conditions", "0,6"): _ENTREE_M,
    ("sec:prix-conditions", "0,7"): _ENTREE_M,
    ("sec:prix-conditions", "0,8"): _ENTREE_M,
    ("sec:prix-conditions", "96"): "borne de la bande de périodes exigée (critère), non une mesure",
    ("sec:prix-conditions", "1,7"): "écart de la période relevée à m = 0,6 à la borne de 96 tours (96 − 94,3)",
    ("sec:menages-inflation", "0,93"): "effet d'un point de glissement sur le budget, non une valeur propre",
    ("sec:menages-conditions", "0,8"): "entrée de la maquette : θ_H",
    ("sec:menages-conditions", "0,498"): "part d'une vente imprévue versée aux ménages, non remesurée ici (fiche 9)",
    ("sec:investissement-conditions", "1,4"): "entrée de la maquette : σ = 1,4/12 an",
    ("sec:investissement-conditions", "0,6"): _ENTREE_M,
    ("sec:investissement-conditions", "0,7"): _ENTREE_M,
    ("sec:investissement-conditions", "0,8"): _ENTREE_M,
    ("sec:investissement-conditions", "0,1396"): "gain de basse fréquence, forme fermée, non une valeur propre",
    ("sec:investissement-conditions", "0,834"): "trajectoire simulée du taux d'utilisation, non une valeur propre",
    ("sec:investissement-conditions", "0,836"): "trajectoire simulée du taux d'utilisation, non une valeur propre",
    ("sec:investissement-conditions", "0,788"): "trajectoire simulée du taux d'utilisation, non une valeur propre",
    ("sec:investissement-conditions", "0,7985"): "trajectoire simulée du taux d'utilisation, non une valeur propre",
    ("sec:investissement-conditions", "0,861"): "part de la production versée aux ménages, cas à la main",
    ("sec:banque_centrale-conditions", "0,5"): "constante ln 0,5 de la demi-vie ; entrée : facteur commun 0,5",
    ("sec:banque_centrale-conditions", "0,22"): "gain statique de la demande au taux réel (C36, #88), non un rayon",
    ("sec:banque_centrale-conditions", "0,42"): "couverture des intérêts à l'arrivée, forme fermée (#88)",
    ("sec:banque_centrale-conditions", "0,21"): "couverture des intérêts à l'arrivée, forme fermée (#88)",
    ("sec:banque_centrale-conditions", "1,01"): "entrée : part de la dépense visée multipliée par 1,01",
    ("sec:banque_centrale-conditions", "1,15"): "entrée : ν_G retenu",
    ("sec:banque_centrale-conditions", "0,214"): "écart du glissement à la cible au tour 60, trajectoire simulée",
    ("sec:banque_centrale-conditions", "0,161"): "écart du glissement à la cible au tour 120, trajectoire simulée",
    ("sec:banque_centrale-conditions", "1,034773"): "mesure hors outil, ancienne E12 (sans −T^cou, script de la "
                                                    "rédaction non versionné) : la maquette n'a pas cette variante",
    ("sec:banque_centrale-conditions", "1,009006"): "mesure hors outil, ancienne E12 (sans −T^cou, variante non "
                                                    "versionnée)",
    ("sec:finances_publiques-conditions", "0,2208"): "gain statique de la demande au taux réel (C36, #88)",
    ("sec:finances_publiques-conditions", "0,42"): "couverture des intérêts à l'arrivée, forme fermée (#88)",
    ("sec:finances_publiques-conditions", "0,21"): "couverture des intérêts à l'arrivée, forme fermée (#88)",
    ("sec:finances_publiques-conditions", "1,01"): "entrée : part de la dépense visée multipliée par 1,01",
    ("sec:finances_publiques-conditions", "1,15"): "entrée : ν_G retenu",
    ("sec:finances_publiques-conditions", "1,9"): "écart d'arrivée simulé au tour 5 500 (1,9e−8), trajectoire",
    ("sec:finances_publiques-conditions", "0,396"): "palier du glissement sous un taux tenu, trajectoire simulée",
    ("sec:finances_publiques-conditions", "0,596"): "palier du glissement sous un taux tenu, trajectoire simulée",
    ("tab:calibration", "0,02"): "entrée : λ_ti indicative",
    ("tab:calibration", "0,6"): _ENTREE_M,
    ("tab:calibration", "0,7"): _ENTREE_M,
    ("tab:calibration", "0,8"): _ENTREE_M,
    ("tab:instabilites", "0,4"): "entrée : λ_H",
    ("sec:finances_publiques-impots", "1,632"): "taux réel neutre de l'état stationnaire, forme fermée (#80)",
    ("sec:finances_publiques-impots", "1,146"): "taux réel neutre de l'état stationnaire, forme fermée (#80)",
    ("sec:finances_publiques-impots", "0,976"): "écart du taux réel neutre sur l'intervalle, forme fermée (#80)",
    ("sec:finances_publiques-impots", "0,253"): "dette consolidée stationnaire, forme fermée",
    ("sec:finances_publiques-impots", "0,28"): "couverture hors de l'état de référence, non remesurée (#88)",
    ("sec:finances_publiques-impots", "0,42"): "couverture des intérêts à l'arrivée, forme fermée (#88)",
    ("sec:finances_publiques-impots", "0,21"): "couverture des intérêts à l'arrivée, forme fermée (#88)",
    ("sec:finances_publiques-impots", "1,01"): "entrée : part de la dépense visée multipliée par 1,01",
    ("sec:finances_publiques-impots", "1,15"): "entrée : ν_G retenu",
    ("sec:finances_publiques-impots", "0,5"): "entrée : couverture φ = 0,5",
    ("sec:finances_publiques-impots", "0,1"): "pas du balayage de la fonction de fermeture, en point",
    ("sec:finances_publiques-impots", "0,05"): "pas d'une grille de balayage citée auparavant, en point",
}


def lire_spec() -> list[str]:
    return SPEC.read_text(encoding="utf-8").splitlines()


BARRE = "\\barre{"


def sans_barres(ligne: str) -> str:
    """Ligne dont chaque valeur barrée, `\\barre{…}` (CONVENTIONS.md, § 3 et § 4.3), est remplacée par des blancs.

    Une valeur barrée a été remplacée par une remesure : elle n'est plus un chiffre publié, ni recensée ni
    cherchée. Les accolades sont appariées (`\\barre{$-20{,}63$}`) ; une accolade échappée (`\\{`, `\\}`) ne
    compte pas. Un seul parcours de la ligne, de gauche à droite. Un `\\barre{` non refermé est une erreur.
    """
    morceaux, i = [], 0
    while (j := ligne.find(BARRE, i)) >= 0:
        k, profondeur = j + len(BARRE), 1
        while k < len(ligne) and profondeur:
            if ligne[k] == "\\":
                k += 2
                continue
            profondeur += {"{": 1, "}": -1}.get(ligne[k], 0)
            k += 1
        if profondeur:
            raise ValueError(f"\\barre non refermé à la colonne {j + 1} : {ligne[j:j + 40]!r}")
        morceaux += [ligne[i:j], " " * (k - j)]
        i = k
    return "".join(morceaux) + ligne[i:]


def bornes_section(lignes: list[str], label: str) -> tuple[int, int]:
    """Lignes (indices 0) de la section ou du tableau `label`.

    Un tableau long va de son label (dans sa légende, en tête) à sa fin ; une section, de son titre à la
    section suivante de même niveau ou de niveau supérieur.
    """
    debut = next(i for i, l in enumerate(lignes) if f"\\label{{{label}}}" in l)
    if label.startswith("tab:"):
        fin = next(i for i in range(debut, len(lignes)) if "\\end{longtable}" in lignes[i])
        return debut, fin + 1
    titre = next(i for i in range(debut, -1, -1) if re.match(r"\\(sub)*section", lignes[i]))
    niveau = re.match(r"\\((?:sub)*)section", lignes[titre]).group(1).count("sub")
    fin_motif = re.compile(r"^\\(?:sub){0,%d}section" % niveau)
    fin = next((i for i in range(debut + 1, len(lignes)) if fin_motif.match(lignes[i])), len(lignes))
    return debut, fin


def lignes_paragraphes(lignes: list[str]) -> list[tuple[str, int]]:
    """(section, numéro de ligne, base 1) de chaque paragraphe de `PARAGRAPHES`."""
    sortie = []
    for label, entete in PARAGRAPHES:
        debut, fin = bornes_section(lignes, label)
        trouve = [i for i in range(debut, fin) if entete in lignes[i]]
        if label.startswith("tab:instabilites"):
            trouve = [i for i in trouve if lignes[i].startswith(entete)]
        if not trouve:
            raise LookupError(f"paragraphe introuvable : {label}, {entete!r}")
        sortie.append((label, trouve[0] + 1))
    return sortie


def recenser(lignes: list[str]) -> list[tuple[str, int, str]]:
    """Nombres décimaux et périodes en tours des paragraphes de `PARAGRAPHES` : (section, ligne, nombre).

    Les valeurs barrées ne sont pas recensées (`sans_barres`).
    """
    sortie = []
    for label, num in lignes_paragraphes(lignes):
        texte = sans_barres(lignes[num - 1])
        for m in re.finditer(r"\d+(?:\{,\}|,)\d+", texte):
            sortie.append((label, num, m.group(0).replace("{,}", ",")))
        # Période en tours ; séparateur des milliers « \, » (3\,617 tours, recensé 3617).
        for m in re.finditer(r"(\d+(?:\\,\d{3})*(?:\{,\}|,)?\d*)(?:\s|~|\\,)+tours", texte):
            sortie.append((label, num, m.group(1).replace("{,}", ",").replace("\\,", "")))
    vus = set()
    return [x for x in sortie if not (x in vus or vus.add(x))]


def lire_fiches() -> dict[str, list[str]]:
    return {f: (RACINE / f).read_text(encoding="utf-8").splitlines() for f in sorted({f for f, _ in LIGNES_FICHES})}


def lignes_fiches(fiches: dict[str, list[str]]) -> list[tuple[str, int]]:
    """(fichier, numéro de ligne, base 1) de chaque ligne de `LIGNES_FICHES`, trouvée une seule fois."""
    sortie = []
    for fichier, debut in LIGNES_FICHES:
        trouve = [i + 1 for i, l in enumerate(fiches[fichier]) if l.startswith(debut)]
        if len(trouve) != 1:
            raise LookupError(f"ligne de fiche introuvable ou non unique : {fichier}, {debut!r} ({trouve})")
        sortie.append((fichier, trouve[0]))
    return sortie


def recenser_fiches(fiches: dict[str, list[str]]) -> list[tuple[str, int, str]]:
    """Nombres décimaux des lignes de `LIGNES_FICHES` : (fichier, ligne, nombre)."""
    return [(f, num, m.group(0)) for f, num in lignes_fiches(fiches)
            for m in re.finditer(r"\d+,\d+", fiches[f][num - 1])]


def lignes_du_motif_fiches(fiches: dict[str, list[str]], motif: str, ou: tuple[str, ...]) -> list[str]:
    """« fichier:ligne » des lignes de `LIGNES_FICHES` des fichiers de `ou` où le motif est écrit (même règle
    que `lignes_du_motif`)."""
    expression = re.compile(r"(?<![\d,])" + re.escape(motif.replace("{,}", ",")) + r"(?!\d)")
    return [f"{Path(f).name}:{num}" for f, num in lignes_fiches(fiches)
            if f in ou and expression.search(fiches[f][num - 1])]


def lignes_du_motif(lignes: list[str], motif: str, ou: tuple[str, ...]) -> list[tuple[str, int]]:
    """(section, numéro de ligne, base 1) des paragraphes recensés des sections de `ou` où le motif est écrit,
    comme nombre entier, hors valeurs barrées (`sans_barres`).

    Un motif qui commence ou finit par un chiffre ne se lit pas à l'intérieur d'un autre nombre
    (« 275 » ne se trouve pas dans « 1,0275 »).
    """
    expression = re.compile(r"(?<![\d,])" + re.escape(motif.replace("{,}", ",")) + r"(?!\d)")
    return [(label, num) for label, num in _paragraphes(tuple(lignes))
            if label in ou and expression.search(sans_barres(lignes[num - 1]).replace("{,}", ","))]


@lru_cache(maxsize=4)
def _paragraphes(lignes: tuple[str, ...]) -> tuple[tuple[str, int], ...]:
    return tuple(lignes_paragraphes(list(lignes)))


# --- Calcul et affichage ----------------------------------------------------------------------


def evaluer(c: Chiffre, lignes: list[str], fiches: dict[str, list[str]] | None = None) -> dict[str, object]:
    """Remesure d'un chiffre ; une remesure sans objet (None : racine réelle, rayon ≥ 1) est publiée telle quelle."""
    valeur = c.calcul()
    if valeur is None:
        ecart, verdict = None, "sans objet"
    else:
        valeur = float(valeur)
        if c.nature == "racine nominale":
            ok, ecart = valeur <= 1e-9, valeur - 1e-9
        else:
            ecart, _, ok = es.comparer(c.publie.replace("{,}", ","), valeur)
        verdict = "reproduit" if ok else "écart"
    return {
        "ident": c.ident, "nature": c.nature, "maquette": c.maquette, "hypothese": c.hypothese,
        "publie": c.publie.replace("{,}", ","), "remesure": valeur, "ecart": ecart, "verdict": verdict,
        "reproduit": verdict == "reproduit",
        "lignes": sorted({num for _, num in lignes_du_motif(lignes, c.motif, c.ou)}),
        "lignes_fiches": lignes_du_motif_fiches(lire_fiches() if fiches is None else fiches, c.motif, c.ou),
    }


def calculer() -> dict[str, object]:
    lignes, fiches = lire_spec(), lire_fiches()
    resultats = [evaluer(c, lignes, fiches) for c in releve()]
    variantes = variantes_F()
    residus = {
        "offre": max(residu_point_fixe(carte_offre(m, p, s)) for m in M4 for p, s in
                     (("fige", False), ("regle", False), ("regle", True), ("marge", True))),
        "investissement": max(residu_point_fixe(carte_investissement(m, a)) for m in (0.6, 0.7, 0.8)
                              for a in (2.0, 3.0)),
        "menages": max(residu_point_fixe(carte_menages(th, r, l)) for th in (0.8, 1.0)
                       for r in ("hausse", "baisse") for l in LECTURES),
        "socle": max(residu_point_fixe(carte_socle(parametres_socle(pi), r)) for pi in (0.0, 0.02, 0.10)
                     for r in ("hausse", "baisse")),
        "variantes_F": max(v["residu"] for v in variantes),
        "cas_controles": residu_cas_controles(),
    }
    n_cas, hors_tenus, nominale_cas = tenus_et_nominales()
    nominales = {
        "socle": max(s.ecart_nominal for pi in (0.0, 0.02, 0.10) for s in rayon_socle(pi).values()),
        "menages": max(spectre(carte_menages(th, r)).ecart_nominal for th in (0.8, 1.0) for r in ("hausse", "baisse")),
        "variete_cas_controles": nominale_cas,
    }
    socle = {f"{pi:g}": {r: {"rayon": s.rayon, "racine": [s.racine.real, s.racine.imag], "periode": s.periode,
                            "demi_vie": s.demi_vie} for r, s in rayon_socle(pi).items()} for pi in (0.0, 0.02, 0.10)}
    lect = {f"{pi:g}": {r: _lectures_dict(lectures_socle(pi, r))
                        | {"coude": ecart_avant_arriere(carte_socle(parametres_socle(pi), r))}
                        for r in ("hausse", "baisse")} for pi in (0.0, 0.02, 0.10)}
    controles = {
        "residu_gauche": max(x["residu_gauche"] for regimes in lect.values() for x in regimes.values()),
        "residu_gauche_variantes": max(v["residu_gauche"] for v in variantes),
        "coude": max(x["coude"] for regimes in lect.values() for x in regimes.values()),
        "coude_variantes": max(v["coude"] for v in variantes),
        "tenus_en_niveau": sorted({tuple(x["tenus_en_niveau"]) for regimes in lect.values()
                                   for x in regimes.values()}),
        "cas_controles": n_cas,
        "tenus_hors_attendus": hors_tenus,
    }
    marge = marge_conjointe()
    return {"releve": resultats, "residus": residus, "racines_nominales": nominales, "socle": socle,
            "lectures_socle": lect, "controles": controles, "grille_socle": grille_socle(),
            "verdicts_grille": verdicts_grille(), "complements_socle": complements_socle(),
            "marge_conjointe": marge, "absents_grille": ABSENTS_GRILLE, "ajouts_grille": AJOUTS_GRILLE,
            "variantes_F": list(variantes),
            "recensement": recenser(lignes) + recenser_fiches(fiches)}


def _lectures_dict(x: LecturesSocle) -> dict[str, object]:
    return {"inv_gamma": x.inv_gamma, "rayon_brut": x.rayon_brut, "multiplicite_brute": x.multiplicite_brute,
            "noyau_brut": x.noyau_brut, "rayon_variete": x.rayon_variete,
            "multiplicite_variete": x.multiplicite_variete, "suivante": [x.suivante.real, x.suivante.imag],
            "rayon_c": x.rayon_c, "tenus_en_niveau": list(x.tenus_en_niveau), "residu_gauche": x.residu_gauche,
            "residu_identites": x.residu_identites, "ecart_nominal": x.ecart_nominal}


def controles_tenus(r: dict[str, object]) -> list[str]:
    """Contrôles dont dépend le code de sortie ; liste vide si tous sont tenus."""
    echecs = []
    pire = max(r["residus"].values())
    if not pire <= TOL_POINT_FIXE:
        echecs.append(f"point fixe non tenu : résidu {pire!r} > {TOL_POINT_FIXE:g}")
    if not max(r["racines_nominales"].values()) <= TOL_RACINE_NOMINALE:
        echecs.append(f"racine nominale non trouvée : {r['racines_nominales']!r}")
    c = r["controles"]
    for cle in ("residu_gauche", "residu_gauche_variantes"):
        if not c[cle] <= TOL_GAUCHE:
            echecs.append(f"variété des identités non invariante ({cle}) : {c[cle]!r} > {TOL_GAUCHE:g}")
    for cle in ("coude", "coude_variantes"):
        if not c[cle] <= TOL_COUDE:
            echecs.append(f"coude franchi par les différences finies ({cle}) : {c[cle]!r} > {TOL_COUDE:g}")
    for pi, regimes in r["lectures_socle"].items():
        for regime, x in regimes.items():
            if tuple(x["tenus_en_niveau"]) != TENUS_ATTENDUS or x["multiplicite_variete"] != len(TENUS_ATTENDUS):
                echecs.append(f"racines en 1/Γ̄ de la variété à π̄ = {pi}, {regime} : {x['multiplicite_variete']} "
                              f"pour les stocks tenus en niveau {x['tenus_en_niveau']} (attendu {TENUS_ATTENDUS})")
    for cas in c["tenus_hors_attendus"]:
        echecs.append(f"racines en 1/Γ̄ de la variété hors des stocks tenus attendus {TENUS_ATTENDUS} : {cas}")
    return echecs


def _f(x: float | None, chiffres: int = 6) -> str:
    if x is None:
        return "—"
    return f"{x:.{chiffres}f}".replace(".", ",")


def _z(z) -> str:
    return f"{_f(z[0])} {'+' if z[1] >= 0 else '−'} {_f(abs(z[1]))} i"


def afficher(r: dict[str, object], sortie=None) -> None:
    sortie = sortie or sys.stdout
    p = lambda *a: print(*a, file=sortie)  # noqa: E731
    p("Maquette linéarisée de la boucle conjointe (issue #65)")
    p(f"Pas des différences finies : {PAS_RELATIF:g} relatif ; racine nominale |λ − 1| ≤ {TOL_RACINE_NOMINALE:g} ; "
      f"ν_G = {NU_G:g}")
    p("")
    p("Résidus du point fixe (relatifs) : " + " ; ".join(f"{k} {v:.1e}" for k, v in r["residus"].items()))
    p("Racine nominale, plus grand |λ − 1| : " + " ; ".join(f"{k} {v:.1e}" for k, v in r["racines_nominales"].items()))
    c = r["controles"]
    p(f"Variété invariante, max |gJ − g/Γ̄|/|g| : socle {c['residu_gauche']:.1e}, variantes de F "
      f"{c['residu_gauche_variantes']:.1e} (≤ {TOL_GAUCHE:g}) ; coudes, max |J⁺ − J⁻| : socle {c['coude']:.1e}, "
      f"variantes de F {c['coude_variantes']:.1e} (≤ {TOL_COUDE:g})")
    p(f"Stocks tenus en niveau ({', '.join(TENUS_ATTENDUS)}, multiplicité {len(TENUS_ATTENDUS)}) et racine nominale "
      f"de la variété, contrôlés sur {c['cas_controles']} cartes (socle, grille, compléments, φ, marge, variantes "
      f"de F) : {len(c['tenus_hors_attendus'])} hors attendu")
    p("")
    p(f"{'chiffre':58} {'publié':>9} {'remesuré':>12} {'écart':>12}  verdict   lignes")
    for x in r["releve"]:
        verdict = {"reproduit": "reproduit", "écart": "ÉCART"}.get(x["verdict"], x["verdict"])
        lignes = ", ".join([str(n) for n in x["lignes"]] + x["lignes_fiches"]) or "—"
        remesure = "sans objet" if x["remesure"] is None else _f(x["remesure"])
        p(f"{x['ident']:58} {x['publie']:>9} {remesure:>12} {_f(x['ecart']):>12}  {verdict:10} {lignes}")
    p("")
    p("Socle (blocs 2 à 9) : racine dominante brute, période et demi-vie")
    for pi, regimes in r["socle"].items():
        for regime, s in regimes.items():
            p(f"  π̄ = {float(pi):>4.0%} {regime:7} rayon {_f(s['rayon'])} racine {_z(s['racine'])}  période "
              f"{_f(s['periode'], 1)} demi-vie {_f(s['demi_vie'], 1)}")
    p("Socle : lectures du rayon ; lecture (c) retenue (décision du 15/10/2026) : variété des identités, hors des "
      "racines en 1/Γ̄ des stocks tenus en niveau, déclarées")
    p(f"  multiplicité : |λ − 1/Γ̄| ≤ {TOL_RACINE_MULTIPLE:g} ; noyau : valeurs singulières de S⁻¹JS − I/Γ̄ "
      f"≤ {TOL_NOYAU:g} ; variété : noyau des gradients de « "
      + " » et « ".join(nom for nom, _ in IDENTITES_SOCLE) + " » ; stock tenu en niveau : ligne de S⁻¹JS égale "
      f"à e_i/Γ̄ (≤ {TOL_NOYAU:g})")
    for pi, regimes in r["lectures_socle"].items():
        for regime, s in regimes.items():
            p(f"  π̄ = {float(pi):>4.0%} {regime:7} 1/Γ̄ {_f(s['inv_gamma'])} | brut : rayon {_f(s['rayon_brut'])}, "
              f"{s['multiplicite_brute']} en 1/Γ̄ (noyau {s['noyau_brut']}) | variété : rayon "
              f"{_f(s['rayon_variete'])}, {s['multiplicite_variete']} en 1/Γ̄, stocks tenus en niveau "
              f"{', '.join(s['tenus_en_niveau']) or 'aucun'} | (c) : {_f(s['rayon_c'])}, racine {_z(s['suivante'])} "
              f"| |gJ − g/Γ̄| {s['residu_gauche']:.1e}, |g·x0| {s['residu_identites']:.1e}, coude {s['coude']:.1e}")
    p(f"Grille du socle à π̄ = 2 % (banque_centrale.md, l. 340-345 ; lecture (c), pire des deux régimes ; absents "
      f"du socle : {', '.join(r['absents_grille'])} ; ajoutés : {', '.join(r['ajouts_grille'])} ×0,5 et ×2) :")
    for nom, rayon in r["grille_socle"]:
        p(f"  {nom:24} {_f(rayon)}")
    for nom, v in r["verdicts_grille"].items():
        p(f"  verdict, grille {nom} : {v['stables']} branches sur {v['branches']} de rayon < 1, pire "
          f"{_f(v['pire'])} ({v['branche_pire']})")
    p("Mesures complémentaires hors grille (lecture (c), pire des deux régimes, π̄ = 2 %) :")
    for nom, rayon in r["complements_socle"]:
        p(f"  {nom:24} {_f(rayon)}")
    m = r["marge_conjointe"]
    p(f"Marge conjointe de {', '.join(GAINS_ENSEMBLE)} (facteur commun, lecture (c), pire des deux régimes, π̄ = 2 %) "
      f": frontière ×{_f(m['facteur'], 4)} (bissection sur [{BORNES_MARGE[0]:g} ; {BORNES_MARGE[1]:g}]) ; à ×2 : "
      + " ; ".join(f"{regime} {_f(x['rayon'])}, {x['nature']}, période {_f(x['periode'], 1)}"
                   for regime, x in m["x2"].items()))
    p("")
    p("Variantes écartées de F, seconde écriture (fiche 6, § 3.N ; π̄ = 2 % ; lecture (c) ; « fiche » : "
      "i_L = i_D = 3 %, ϑ = 0, τ_H = τ_F = 0 ; coude de B6 en « fiche », deux branches)")
    p(f"  {'config.':6} {'λ_ti':>5} {'taux':13} {'B6':8} {'financement':28} {'régime':7} {'rayon':>9} "
      f"{'nature':16} {'période':>8} {'coude':>8}")
    for v in r["variantes_F"]:
        coude = f"{v['coude']:.1e}" + (f" (B6 écrit {v['coude_B6_ecrit']:.1e})" if "coude_B6_ecrit" in v else "")
        p(f"  {v['configuration']:6} {_f(v['lambda_ti'], 2):>5} {v['taux']:13} {v['B6']:8} {v['financement']:28} "
          f"{v['regime']:7} {_f(v['rayon']):>9} {v['nature']:16} {_f(v['periode'], 1):>8} {coude}")
    ecarts = [x for x in r["releve"] if x["verdict"] == "écart"]
    sans_objet = [x for x in r["releve"] if x["verdict"] == "sans objet"]
    p("")
    p(f"{len(r['releve'])} chiffres relevés ; {sum(x['reproduit'] for x in r['releve'])} reproduits à la dernière "
      f"décimale publiée ; {len(ecarts)} écarts : {', '.join(x['ident'] for x in ecarts) or 'aucun'} ; "
      f"{len(sans_objet)} sans objet : {', '.join(x['ident'] for x in sans_objet) or 'aucun'}")


def main(arguments: list[str] | None = None) -> int:
    analyseur = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    analyseur.add_argument("--json", default=None, help="écrit aussi les résultats en JSON dans ce fichier")
    args = analyseur.parse_args(arguments)
    r = calculer()
    afficher(r)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=1, sort_keys=True, default=str)
            f.write("\n")
    echecs = controles_tenus(r)
    for echec in echecs:
        print(echec, file=sys.stderr)
    return 2 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
