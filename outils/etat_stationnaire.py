"""État stationnaire du socle sous forme fermée : grille, contrôles et valeurs publiées.

Contrat : issue #84 (critère de passage du jalon J1, décision M19) et ses
critères écrits avant l'essai, déposés en commentaires de l'issue le
05/10/2026 : décisions du mainteneur (elles priment), part de `macro` (blocs 1
à 6 et 9, fermeture #44), part de `monnaie` (blocs 7 et 8, mesure de #80,
niveaux bancaires de #83). Les formes sont celles des sections
`sec:<bloc>-stationnaire` de `docs/specification/nations_et_marches.tex`,
citées par leur label ; les règles (N1 à N11, T1 à T6, P1 à P4, H2 à H7, S1 à
S7, F1 à F4, B1 à B7, BC1 à BC9, E1 à E13) sont celles des encadrés des
sections des blocs, repérées par leur identifiant.

**Imports.** Le script importe la bibliothèque standard et, de `nations`, le
seul module feuille `nations.scenarios.stationnaire`, maison unique des formes
fermées (ADR 0015, points 1 et 14 ; décisions P247 et S2) : `facteurs`,
`rho_IN`, `rho_K`, `etat_stationnaire`, `controler_etat` et `ouverture` en
sont les adaptateurs, à signatures inchangées. Il n'importe ni `archive/` ni
aucun autre module de `nations`. Ce qui reste indépendant du résolveur et
hors de `src/` : `un_pas`, `residus_des_regles`, `matrices` et la table des
valeurs publiées ; la stationnarité exacte du moteur depuis l'état résolu
(critère A2) contrôle l'équilibre des règles, et la comparaison du moteur à
t = 0 au script (critère A1) la transcription (ADR 0015, point 2 ; ADR 0005,
point 20, annoté). Il est déterministe : deux exécutions donnent une sortie
identique à l'octet.

**Aucune simulation.** L'état stationnaire est calculé en formes fermées,
dans un ordre triangulaire (part de `macro`, § 3) : cadre et taux, offre,
financement des entreprises, banque, ménages et impôt (forme fermée linéaire
de la richesse), fermeture (part de la dépense publique résolue, première
lecture de #44, décision M32, lecture (e)), dette (forme fermée linéaire de
l'encaisse). Aucune boucle, aucun point fixe. Les règles sont ensuite
**évaluées une fois** sur l'état d'ouverture (`un_pas`) : c'est la seconde
route des contrôles (résidus des règles, matrices, contrôle C42, B7 sur le
grand livre, B5, B6), pas une itération dans le temps.

**Seule résolution numérique** : r̄ en lecture (α), pour la mesure de #80
(`mesure_alpha`), par balayage puis bissection déterministe (part de
`monnaie`, § 4 ; tol_F = 1e−12).

**Lecture (α) de #80 : lecture A de i^ref, norme ϱ̄_L de S2 fixée**
(décision du mainteneur du 05/10/2026). Les paramètres structurels sont ceux
de l'état résolu à π* = 2 %, r̄ = 1 %, au même n_a : la part de la dépense
publique θ_G et la norme ϱ̄_L du bloc investissement (« constante tenue avec
l'état et jamais recalculée », `sec:investissement-taux`) ; le taux de
référence de E4 garde le paramètre r̄ = 1 % (lecture A). Sous la lecture A,
une norme ϱ̄_L recalculée à chaque r̄ rend θ_G indépendant de r̄ (la
couverture des intérêts T^cou neutralise le canal rentier, propriété testée),
si bien que l'équation de (α) n'aurait aucune racine hors de π* = 2 % : la
norme fixée est la seule lecture où (α) est définie. Allocations du verdict
(liste L2, critère 13 (a) de la fiche 8) : C/Y_o, ti et tu sous le seuil de
0,1 point, V_H/(n_a YD^HS) en invariance exacte ; les autres allocations sont
publiées en mesure (`ALLOCATIONS_VERDICT`, `ALLOCATIONS_INVARIANTES`,
`ALLOCATIONS_MESUREES`).

**Grille.** π̄ = π* ∈ {0 ; 2 ; 10 %} × n_a ∈ {4 ; 12 ; 52} × ν_G : ν_G = 1
(point de référence déclaré, hors du domaine ν_G > 1 de la table, admis pour
la publication et jamais comme valeur de table), forme fermée en ν_G
(coefficients publiés), valeur retenue ν_G = 1,15 (décision du mainteneur du
05/10/2026 ; option `--nu-g-retenu`, qui refuse 1 ; ν_G,min et la marge de la
propriété J-ν sont publiés sur toute la grille). Croissance : g_pr = 2 %, g_N = 0 (décision du 05/10/2026, point 1).
Un point de référence (ν_G = 1) où le plafond de E1 est actif n'est pas refusé : il est publié comme constat
déclaré, sans valeur d'état ni résidu (décision de `macro`, option (b)) ; les autres refus y restent bloquants.

**Valeurs publiées.** Chaque valeur publiée de la spécification que les
critères listent est comparée à sa dernière décimale publiée : arrondi au plus
proche, |écart| ≤ 0,5 unité de la dernière décimale, dans l'unité publiée
(décision du 05/10/2026, point 2). Un écart est **publié**, jamais masqué :
la colonne « verdict » dit « écart » et l'explication l'accompagne avec son
statut : écrite avant l'essai, établie après l'essai (et testée), ou cause
non établie.

Usage : `uv run python outils/etat_stationnaire.py [--nu-g-retenu X] [--json
FICHIER]`. Codes de sortie : 0 si l'état se résout sur toute la grille et que
le plus grand résidu des contrôles est ≤ 1e−12, quels que soient les écarts
aux valeurs publiées (ils sont publiés, le visa relève du mainteneur) et les
constats (q1, point de référence hors domaine) ; 1 sur un refus de domaine (`HorsDomaine`) ; 2 si le plus
grand résidu dépasse 1e−12 (la sortie est alors publiée en entier).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, fields, replace

from nations.scenarios import stationnaire as resolveur

# --- Paramètres ---------------------------------------------------------------


class HorsDomaine(ValueError):
    """Refus explicite d'un paramètre ou d'un état hors de son domaine (jamais d'écrêtage)."""


class MinimumNonEncadre(HorsDomaine):
    """Refus de `minimum_delta_r_alpha_en_zeta` (#173, P273) : r̄_α(0) − r̄_α(2 %) ne change pas de signe sur
    l'intervalle de ζ ou n'y est pas fini (point anguleux non encadré ; minimum non localisé par cette méthode), le
    croisement trouvé n'est pas minimal, Δr̄_α n'y est pas plus bas qu'aux deux bornes (minimum aux bornes, P281),
    un r̄_α n'est pas fini là où Δr̄_α est évaluée, ou (#191, P320) la lecture (α) refuse un ζ évalué, la bissection
    s'arrête avant la largeur demandée (précision de la machine, itérations) ou un voisin du contrôle de minimum local
    sort de l'intervalle. `motif` décrit le refus.

    `table_publiees` publie la ligne « refusée », motif à l'appui, au lieu d'interrompre la table : une variante de
    paramètres (bords du domaine, rachat net) se calcule en entier, sans valeur NaN silencieuse. Comme « état non
    publié », c'est un constat publié et non un refus de domaine des paramètres : le code de sortie n'en dépend pas.
    """

    def __init__(self, motif: str) -> None:
        super().__init__(f"minimum de Δr̄_α en ζ : {motif}")
        self.motif = motif


class ReferenceNonPubliee(Exception):
    """Point de référence ν_G = 1 dont le plafond de E1 est actif : constat déclaré, état non publié.

    Ce n'est pas un refus (décision de `macro`, option (b)) : `calculer` publie
    le constat et le code de sortie reste celui des colonnes ν_G > 1. `marge`
    est la marge relative 1 − Γ̄ (G/PB)/ν_G du point.
    """

    def __init__(self, pi: float, n_a: int, marge: float) -> None:
        super().__init__(f"π̄ = {pi!r}, n_a = {n_a} : {constat_reference(marge)}")
        self.pi, self.n_a, self.marge = pi, n_a, marge


def constat_reference(marge: float) -> str:
    """Texte du constat déclaré d'un point de référence hors domaine (décision de `macro`, option (b))."""
    return f"point de référence hors domaine : plafond de E1 actif (marge = {marge:.6g}), état non publié"


@dataclass(frozen=True)
class Parametres:
    """Paramètres de la configuration de référence R (`tab:calibration`, valeurs indicatives).

    Chaque champ est déclaré dans `DECLARATIONS` (unité, source, équation).
    """

    n_a: int = 12
    g_pr: float = 0.02
    g_N: float = 0.0
    pi_cible: float = 0.02
    rbar: float = 0.01
    sigma: float = 1.4 / 12
    kappa: float = 1.6
    tu_bar: float = 0.8
    delta: float = 0.05
    mu_bar: float = 0.60
    U_eq: float = 0.05
    lv: float = 0.4
    nu_F: float = 1 / 6
    varpi_L: float = 0.02
    varpi_D: float = 0.01
    vartheta: float = 0.15
    nu_H: float = 1.1
    tau_H: float = 0.25
    tau_F: float = 0.0
    theta_Tr: float = 0.0
    theta_CB: float = 0.0
    phi: float = 1.0
    nu_G: float = 1.0
    zeta: float = 8.0
    eta_r: float = 2.0
    lambda_ti: float = 0.02
    lambda_v: float = 3.0
    lambda_IN: float = 1.5
    lambda_w: float = 0.18
    beta: float = 2.0
    lambda_N: float = 3.5
    lambda_mu: float = 1.2
    psi_xi: float = 0.5
    lambda_H: float = 0.4
    a_pi: float = 0.5
    a_I: float = 0.25
    lambda_e: float = 0.2
    varsigma_L: float = 0.0
    varsigma_B: float = 0.0
    p_0: float = 1.0
    pr_0: float = 1.0
    N_pa_0: float = 1.0


# nom : (unité, source, équation)
DECLARATIONS: dict[str, tuple[str, str, str]] = {
    "n_a": ("pas par an", "décision M22", "sec:cadre-calendrier"),
    "g_pr": ("par an, taux de croissance", "décision du mainteneur du 05/10/2026 (#84, point 1, lecture I1)", "N9"),
    "g_N": ("par an, taux de croissance", "décision du mainteneur du 05/10/2026 (#84, point 1, lecture I1)", "T1"),
    "pi_cible": ("par an, taux de croissance (inflation)", "tab:calibration ; π̄ = π* (C2)", "BC4"),
    "rbar": ("par an, taux réel de Fisher sur la cible",
             ("choix de conception, niveau contesté (critère 23 de la fiche 8 ; P208) ; fourchette lue de −0,5 % à "
              "+1,0 % (BCE, Economic Bulletin 1/2025, encadré « Natural rate estimates for the euro area: insights, "
              "uncertainties and shortcomings », fin 2024, lu le 16/11/2026) et de 0,9 % à 1,9 % (Réserve fédérale, "
              "Summary of Economic Projections du 16/09/2026, tableau 1, lu le 16/11/2026 : étendue des projections "
              "de long terme du taux des fonds fédéraux, 2,9 à 3,9 %, moins l'inflation PCE de long terme projetée, "
              "2,0 %) ; fourchette d'ensemble de −0,5 % à +1,9 % ; tab:calibration ; décision M34"),
             "BC1, E4"),
    "sigma": ("années de ventes", "tab:calibration (indicative)", "N2"),
    "kappa": ("années", "tab:calibration (indicative)", "N11"),
    "tu_bar": ("fraction de la capacité normale", "tab:calibration (indicative)", "S2"),
    "delta": ("par an, taux de flux", "tab:calibration (hypothèse)", "N10, S7"),
    "mu_bar": ("fraction du coût unitaire",
               ("K. Bodnár et M. Mohr, « The development of the wage share in the euro area since the start of "
                "the pandemic », BCE, Economic Bulletin 4/2023, encadré, note du graphique A, consulté le "
                "16/11/2026 : part salariale de la zone euro, rémunération des salariés corrigée des indépendants "
                "sur la valeur ajoutée brute au prix de base, moyenne 1998-2023, 62,4 % ; écart au coût des "
                "facteurs contesté (AMECO ALCD2, EA20, 1998-2023 : 63,11 %, consulté le 16/11/2026) ; "
                "μ̄ = 0,60 ⇒ ω̄ = 1/(1 + μ̄) = 0,625 ; tab:calibration ; décision M34"),
               "P2, T3"),
    "U_eq": ("fraction de la population active", "tab:calibration (hypothèse)", "T3, E1"),
    "lv": ("fraction du capital comptable", "tab:calibration (hypothèse)", "F1"),
    "nu_F": ("années de ventes", "tab:calibration (hypothèse)", "F2"),
    "varpi_L": ("par an, taux de flux",
                ("BCE, statistiques de taux d'intérêt des IFM (MIR), indicateur composite du coût de l'emprunt des "
                 "sociétés non financières, affaires nouvelles (ECB/MIR/M.U2.B.A2I.AM.R.A.2240.EUR.N), moins le taux "
                 "du jour le jour de la zone euro (EONIA, moyenne mensuelle, ECB/FM/M.U2.EUR.4F.MM.EONIA.HSTA, "
                 "jusqu'en septembre 2019, puis €STR, moyenne mensuelle des observations quotidiennes, "
                 "ECB/EST/B.EU000A2X2A25.WT), zone euro, moyenne mensuelle 2003-2024 : "
                 "2,09 points (encours : 2,30) ; DBnomics, consulté le 16/11/2026 ; arrondi au point ; "
                 "tab:calibration ; décision M34 ; M31"),
                "B1"),
    "varpi_D": ("par an, taux de flux",
                ("BCE, MIR et BSI : taux des dépôts des ménages et des sociétés non financières (à vue, à terme, à "
                 "préavis), pondéré par les encours de la BSI, moins le taux du jour le jour (EONIA puis €STR) ; taux "
                 "des MIR : dépôts à vue des ménages et des SNF (L21…2250.EUR.N, L21…2240.EUR.N), dépôts à terme, "
                 "encours (L22.A…2250.EUR.O, L22.A…2240.EUR.O), dépôts à préavis de 3 mois au plus des ménages "
                 "(L23.D…2250.EUR.N, employé aussi pour les SNF) ; poids de la BSI : "
                 "ECB/BSI/M.U2.N.A.{L21,L22,L23}.A.1.U2.{2250,2240}.Z01.E ; zone "
                 "euro : 0,85 point (2003-01 à 2008-08) et 1,93 point (2022-07 à 2024-12), fenêtres de taux "
                 "positifs ; moyenne 2003-2024 de −0,05 point, dominée par les taux négatifs, écartée ; fenêtre "
                 "contestée ; écart dépendant du régime (limite de B2, #167) ; DBnomics, consulté le 16/11/2026 ; "
                 "tab:calibration ; décision M34 ; M31"),
                "B2"),
    "vartheta": ("fraction des crédits de clôture",
                 ("BCE, statistiques de supervision bancaire (MSU), ratio CET1 des établissements importants "
                  "(ECB/SUP/Q.B01.W0._Z.I4008._T.SII._Z._Z._Z.PCT.C), moyenne 2015T3-2024T4 : 14,75 % des actifs "
                  "pondérés des risques, arrondi ; DBnomics, consulté le 16/11/2026 ; dénominateur : ϑ rapporte les "
                  "fonds propres aux crédits, et non aux actifs pondérés des risques ; les deux ratios coïncident, "
                  "pour la banque du modèle, sous les pondérations de l'accord de Bâle de 1988 (crédits aux "
                  "entreprises pondérés à 100 %, titres publics et réserves à 0 % ; Comité de Bâle sur le contrôle "
                  "bancaire, International Convergence of Capital Measurement and Capital Standards, juillet 1988, "
                  "§ 44 et annexe 2, lus le 16/11/2026) ; sous Bâle III, les crédits aux entreprises y sont pondérés "
                  "en moyenne à moins de 100 % (approches internes) : rapporté aux crédits, le ratio observé serait "
                  "inférieur à 14,75 % ; écart non mesuré : le niveau est contesté ; tab:calibration ; décision M34"),
                 "B6"),
    "nu_H": ("années de revenu de Haig-Simons",
             ("Eurostat, comptes annuels des secteurs (SEC 2010 ; nasa_10_f_bs, nasa_10_nf_tr), ménages et ISBLSM "
              "(S14_S15), numéraire et dépôts (F.2, actif, non consolidé) sur revenu disponible brut (B.6g, prix "
              "courants), EA21, moyenne 2001-2023 : 1,076 an ; consulté le 16/11/2026 ; définition déclarée : V_H "
              "(dépôts seuls, sans passif) sur le revenu disponible annuel, rapport comparé à B10, d'où "
              "ν_H = R/(1 − R n_a π^{∗,pas}) à π* = 2 % : 1,0995, arrondi à 1,1 ; contrôle stock-flux : acquisition "
              "nette de F.2 sur B.6g, 4,32 % (2002-2023), contre 4,27 % d'épargne nominale dans le modèle ; écart "
              "déclaré : B.6g contient l'excédent des logements et le revenu mixte ; tab:calibration ; décision M34"),
             "H3"),
    "tau_H": ("fraction de l'assiette", "tab:calibration (indicative)", "E3"),
    "tau_F": ("fraction de l'assiette", "sec:finances_publiques-stationnaire (nul au socle)", "E5"),
    "theta_Tr": ("fraction de la production potentielle", "sec:finances_publiques-stationnaire (nul au socle)", "E6"),
    "theta_CB": ("fraction du besoin d'émission", "tab:calibration (0 au socle)", "BC5, E10"),
    "phi": ("sans dimension, {0 ; 1}", "sec:finances_publiques-stationnaire (φ = 1)", "E4"),
    "nu_G": ("multiple des paiements bruts d'un pas", "grille de #84 (ν_G = 1 : point de référence)", "E8"),
    "zeta": ("par unité de taux réel annuel",
             ("R. Klump, P. McAdam et A. Willman, « The normalized CES production function: theory and empirics », "
              "BCE, Working Paper Series n° 1294, février 2011, tableau 2, p. 30, lu le 16/11/2026 : élasticité de "
              "substitution de la zone euro 0,7 (1970-2003) et 0,95-1,05 (1970-1997), « generally below unity » ; "
              "S. Gilchrist et E. Zakrajšek, « Investment and the Cost of Capital: New Evidence from the Corporate Bond "
              "Market », NBER Working Paper 13174, juin 2007, p. 21, lu le 16/11/2026 : firmes américaines émettrices "
              "d'obligations (zone : États-Unis ; fenêtre : non relevée par la fiche), élasticité de long terme du "
              "capital au coût d'usage égale à 1 ; fourchette lue de σ de 0,5 à 1,0, niveau contesté ; ζ = 8 ⇒ σ ≈ 0,64 "
              "sous ζ = σ/(ϱ̄_L + δ) (hypothèse) ; tab:calibration ; décision M34"),
             "S2"),
    "eta_r": ("par unité de taux réel annuel", "tab:calibration (indicative)", "S3"),
    "lambda_ti": ("par an, vitesse", "tab:calibration (indicative)", "S6"),
    "lambda_v": ("par an, vitesse", "tab:calibration (indicative)", "N1"),
    "lambda_IN": ("par an, vitesse", "tab:calibration (indicative)", "N3"),
    "lambda_w": ("par an, vitesse",
                 ("choix déclaré, sources lues : pente λ_w β = 0,36 point de hausse annuelle du salaire par point "
                  "d'écart de chômage (β = 2), égale à la pente de l'écart de chômage dans un panel de 19 pays de la "
                  "zone euro (−0,364, glissement annuel de la rémunération par salarié, 2000T1-2018T4 ; F. Tagliati, «"
                  " Wage growth in the euro area: a Phillips curve analysis using panel data », encadré 2, tableau A, "
                  "dans C. Nickel, E. Bobeica, G. Koester, E. Lis et M. Porqueddu (dir.), « Understanding low wage "
                  "growth in the euro area and European countries », BCE, Occasional Paper 232, septembre 2019, révisé"
                  " en décembre 2020) et dans la fourchette de 0,29 à 0,40 des États-Unis (J. Galí, « The Return of "
                  "the Wage Phillips Curve », NBER Working Paper 15758, février 2010, tableau 1, colonnes 6 et 8, ×4 ;"
                  " gains des salariés de production et hors encadrement, données trimestrielles, 1964T1-2009T3, "
                  "2007T4 pour la colonne 8) ; correction annuelle 0,166, sous la correction européenne de 0,25 (O. J."
                  " Blanchard et L. F. Katz, « Wage Dynamics: Reconciling Theory and Evidence », NBER Working Paper "
                  "6924, février 1999, p. 5, fréquence présumée annuelle) ; vitesse contestée : la persistance "
                  "régionale américaine (0,60 à 0,81, D. G. Blanchflower et A. J. Oswald, « The Wage Curve Reloaded »,"
                  " NBER Working Paper 11338, 2005, p. 11 et 15) est tenue pour une borne haute ; consulté le "
                  "16/11/2026 ; tab:calibration ; décision M34"),
                 "T3"),
    "beta": ("par unité de taux de chômage", "tab:calibration (indicative)", "T3"),
    "lambda_N": ("par an, vitesse", "tab:calibration", "T4"),
    "lambda_mu": ("par an, vitesse", "tab:calibration (indicative)", "P2"),
    "psi_xi": ("sans dimension", "tab:calibration (indicative)", "P2"),
    "lambda_H": ("par an, vitesse",
                 ("choix de conception dans la fourchette lue : dépense totale, durables compris, de 50 à 90 % d'un "
                  "versement sur le trimestre de réception (J. A. Parker, N. S. Souleles, D. S. Johnson et R. "
                  "McClelland, « Consumer Spending and the Economic Stimulus Payments of 2008 », NBER Working Paper "
                  "16684, janvier 2011, résumé lu le 16/11/2026 ; États-Unis, 2008 ; période du chiffre à confirmer "
                  "sur l'article) ; dépense cumulée d'une aubaine sur 3 tours de 0,605 à ν_H = 1,1 ; correspondance : "
                  "hypothèse, contestée (versements annoncés, données américaines, ménage représentatif) ; "
                  "tab:calibration ; décision M34"),
                 "H4"),
    "a_pi": ("points de taux par point d'écart", "tab:calibration (indicative)", "BC1"),
    "a_I": ("par an, gain", "tab:calibration (indicative)", "BC2"),
    "lambda_e": ("par an, vitesse", "tab:calibration (indicative)", "BC3"),
    "varsigma_L": ("fraction, entrée de scénario", "nulle hors scénario (décision M31)", "F1"),
    "varsigma_B": ("fraction, entrée de scénario", "nulle hors scénario (décision M33)", "E11"),
    "p_0": ("u.m. par u.v.", "normalisation (numéraire), part de `macro` § 0", "sec:production"),
    "pr_0": ("u.v. par personne et par pas", "normalisation, part de `macro` § 0", "N9"),
    "N_pa_0": ("personnes", "donnée d'échelle, part de `macro` § 0", "T1"),
}

# Vitesses et gains : aucun n'entre dans l'état d'arrivée (propriété P1 de
# `macro`, propriété 4 de `monnaie`). ζ et η_r sont des élasticités de niveau
# (`sec:investissement-stationnaire`) : ils n'entrent pas dans l'état de la
# lecture (e) (Δϱ = 0), mais entrent dans la mesure (α), où Δϱ ≠ 0.
VITESSES = (
    "lambda_v", "lambda_IN", "lambda_w", "beta", "lambda_N", "lambda_mu", "psi_xi",
    "lambda_H", "lambda_ti", "a_pi", "a_I", "lambda_e",
)
ELASTICITES_DE_NIVEAU = ("eta_r", "zeta")

# Tolérances déclarées.
TOL_IDENTITE = 1e-12  # ε de `sec:cadre-identites`, relatif à l'échelle S
TOL_F = 1e-12  # résidu de F en lecture (α), fraction de la production
LARGEUR_BISSECTION = 1e-14  # fraction par an
ITERATIONS_MAX = 200
ZETA_MINIMUM_BORNES = (2.0, 200.0)  # intervalle de recherche du minimum de Δr̄_α en ζ (#173, P273)
TOL_ZETA_MINIMUM = 1e-3  # largeur finale de la bissection en ζ (#173, P273)
SEUIL_SUPERNEUTRALITE = 0.001  # 0,1 point (critère 13 de la fiche 8) ; allocations : liste L2, après `mesure_alpha`

POINTS_PI = (0.0, 0.02, 0.10)
POINTS_NA = (4, 12, 52)
PROFIL_PI = (0.0, 0.01, 0.02, 0.03, 0.04, 0.06, 0.10)
NU_G_PROPOSES = (1.1, 1.15)  # valeurs proposées par `jeu` (fiche 9, § 7 ; décision du 05/10/2026, point 7)
NU_G_RETENU = 1.15  # valeur retenue, troisième colonne ν_G de la grille (décision du mainteneur du 05/10/2026, #84)
MARGE_J_NU = 0.03  # propriété J-ν (formulation de `jeu`)
HAUSSE_J_NU = 1.10
# Borne déclarée des normalisations p_0, pr_0, N^pa_0 et de leur produit p_0 pr_0 N^pa_0 (échelle nominale). C'est
# une borne de l'outil numérique, non du modèle : l'état est homogène de degré un en ces échelles (propriété testée),
# elle ne restreint donc aucun ratio. Elle reste nécessaire après le passage du contrôle « Res · L^CB » à une forme
# relative : sans elle, chaque normalisation seule sort de la plage des flottants (encours sommés, multipliés par
# n_a) vers 1e305 (valeurs publiées non finies, refus aux messages trompeurs) et perd la précision des contrôles dès
# 1e−311 (nombres dénormaux) ; la borne garde plus de 200 ordres de grandeur de marge de part et d'autre.
BORNE_ECHELLE = (1e-100, 1e100)
TOL_BORNE_ECHELLE = 4 * sys.float_info.epsilon  # arrondi du produit de trois flottants (égalité à la borne admise)


def controler_domaine(par: Parametres) -> list[str]:
    """Contrôle les paramètres au chargement ; lève `HorsDomaine`, rend les points déclarés.

    Conditions des sections `*-conditions` des blocs 2 à 9 (part de `macro`,
    § 6 ; part de `monnaie`, § 6.1). ν_G = 1 est admis comme point de
    référence de la forme fermée et déclaré dans la liste rendue.
    """
    declares: list[str] = []
    n = par.n_a
    if not (isinstance(n, int) and n >= 1):
        raise HorsDomaine(f"n_a = {n!r} : entier ≥ 1 attendu")
    for champ in fields(par):  # NaN et ±∞ : refus avant tout calcul (aucune division par zéro ni dépassement)
        if not math.isfinite(getattr(par, champ.name)):
            raise HorsDomaine(f"{champ.name} = {getattr(par, champ.name)!r} : valeur finie attendue")
    # λ_v : domaine strict, comme dans la table du moteur (`nations.moteur.parametres.production`, P70).
    if not 0 < par.lambda_v < n:
        raise HorsDomaine(f"lambda_v = {par.lambda_v!r} : 0 < λ_v < n_a = {n} attendu (domaine strict, P70)")
    for nom in ("lambda_IN", "lambda_w", "lambda_N", "lambda_mu", "lambda_H", "lambda_ti", "lambda_e"):
        val = getattr(par, nom)
        if not 0 < val <= n:
            raise HorsDomaine(f"{nom} = {val!r} : 0 < λ ≤ n_a = {n} attendu (sec:cadre-calendrier)")
    if not par.beta > 0:
        raise HorsDomaine(f"beta = {par.beta!r} : β > 0 attendu (sec:travail-conditions)")
    if not par.psi_xi >= 0:
        raise HorsDomaine(f"psi_xi = {par.psi_xi!r} : ψ_ξ ≥ 0 attendu (sec:prix-conditions)")
    if not par.pi_cible > -1:
        raise HorsDomaine(f"pi_cible = {par.pi_cible!r} : π* > −1 attendu (sec:menages-conditions)")
    if not 0 < par.nu_H * par.lambda_H < 1:
        raise HorsDomaine(f"ν_H λ_H = {par.nu_H * par.lambda_H!r} : 0 < ν_H λ_H < 1 attendu (sec:menages-conditions)")
    # Facteurs de croissance contrôlés avant toute racine n_a-ième : une base négative donnerait un complexe
    # (`TypeError` à la comparaison suivante) au lieu d'un refus. Chaque taux séparément, comme le domaine
    # `TAUX_DE_CROISSANCE_ANNUEL` des tables (`nations.moteur.parametres.production` et `.travail`) : le
    # produit (1 + g_pr)(1 + g_N) > 0 admettrait g_pr = g_N = −1,5, que les tables refusent.
    for nom in ("g_pr", "g_N"):
        if not 1 + getattr(par, nom) > 0:
            raise HorsDomaine(f"{nom} = {getattr(par, nom)!r} : 1 + {nom} > 0 attendu (taux de croissance)")
    gamma_e = ((1 + par.g_pr) * (1 + par.g_N) * (1 + par.pi_cible)) ** (1 / n) - 1
    pis = (1 + par.pi_cible) ** (1 / n) - 1
    coefficient = par.lambda_H / n + par.nu_H * par.lambda_H * pis - gamma_e
    if not coefficient > 0:
        raise HorsDomaine(f"coefficient de richesse = {coefficient!r} : > 0 attendu (sec:menages-conditions)")
    if not 0 <= par.tau_H < 1:
        raise HorsDomaine(f"tau_H = {par.tau_H!r} : 0 ≤ τ_H < 1 attendu (sec:finances_publiques-conditions)")
    if not 0 <= par.tau_F < 1:
        raise HorsDomaine(f"tau_F = {par.tau_F!r} : 0 ≤ τ_F < 1 attendu (sec:finances_publiques-conditions)")
    if not par.theta_Tr >= 0:
        raise HorsDomaine(f"theta_Tr = {par.theta_Tr!r} : θ_Tr ≥ 0 attendu (sec:finances_publiques-conditions)")
    if par.phi not in (0.0, 1.0):
        raise HorsDomaine(f"phi = {par.phi!r} : φ ∈ {{0 ; 1}} attendu (sec:finances_publiques-conditions)")
    if par.nu_G == 1.0:
        declares.append("ν_G = 1 : point de référence de la forme fermée, hors du domaine ν_G > 1 de la table "
                        "(décision du 05/10/2026, point 4)")
    elif not par.nu_G > 1:
        raise HorsDomaine(f"nu_G = {par.nu_G!r} : ν_G > 1 attendu (ν_G = 1 admis comme point de référence) "
                          "(sec:finances_publiques-conditions)")
    if not par.rbar > -0.05:
        raise HorsDomaine(f"rbar = {par.rbar!r} : r̄ > −5 % attendu (condition C51)")
    if not 0 < par.delta / n < 1:
        raise HorsDomaine(f"δ/n_a = {par.delta / n!r} : 0 < δ/n_a < 1 attendu (sec:investissement-conditions)")
    if not 0 <= par.lv < 1:
        raise HorsDomaine(f"lv = {par.lv!r} : 0 ≤ lv* < 1 attendu (sec:investissement-conditions)")
    for nom in ("nu_F", "tu_bar"):
        if not getattr(par, nom) > 0:
            raise HorsDomaine(f"{nom} = {getattr(par, nom)!r} : > 0 attendu")
    # κ ≥ DBL_MIN et σ ≥ DBL_MIN : domaines de représentabilité (flottants normaux, sans contenu économique),
    # borne calculée depuis `sys.float_info.min`, à l'identique de la table du bloc 2
    # (`nations.moteur.parametres.production`), de sorte que script et table refusent le même ensemble (ADR 0016,
    # points 17.3 et 18.2 ; #125, points 5 et 6). Ils contiennent κ > 0, σ > 0 et 1/κ fini (1/DBL_MIN ≈ 4,49e307).
    if not par.kappa >= sys.float_info.min:
        raise HorsDomaine(f"kappa = {par.kappa!r} : κ ≥ DBL_MIN attendu (domaine de représentabilité : κ normal, "
                          "d'où 1/κ fini ; y^cap = K^vol/(n_a κ), N11)")
    if not par.sigma >= sys.float_info.min:
        raise HorsDomaine(f"sigma = {par.sigma!r} : σ ≥ DBL_MIN attendu (domaine de représentabilité : σ normal ; "
                          "IN^vol* = n_a σ v^e, dénominateur de ξ)")
    # Borne haute 20 de η_r et ζ (P139) : refusée ici comme dans la table du bloc 6
    # (`nations.moteur.parametres.investissement`), de sorte que script et table refusent le même ensemble.
    for nom in ("eta_r", "zeta"):
        if not 0 <= getattr(par, nom) <= 20:
            raise HorsDomaine(f"{nom} = {getattr(par, nom)!r} : 0 ≤ {nom} ≤ 20 attendu (sec:investissement-conditions ; "
                              "borne haute P139)")
    # U^eq > 0 et μ̄ > 0 : conditions de conception et d'existence de l'état stationnaire, non domaines de
    # définition (décision du mainteneur du 13/11/2026, P71) ; refusées ici comme dans les tables du moteur
    # (`nations.moteur.parametres.travail` et `.prix`), de sorte que script et tables refusent le même ensemble.
    if not 0 < par.U_eq < 1:
        raise HorsDomaine(f"U_eq = {par.U_eq!r} : 0 < U^eq < 1 attendu (condition de conception et d'existence de "
                          "l'état stationnaire, P71)")
    if not par.mu_bar > 0:
        raise HorsDomaine(f"mu_bar = {par.mu_bar!r} : μ̄ > 0 attendu (condition de conception et d'existence de "
                          "l'état stationnaire, P71 ; elle contient 1 + μ̄ > 0, μ̃ = ln(1 + μ̄))")
    if not par.vartheta > 0:
        raise HorsDomaine(f"vartheta = {par.vartheta!r} : ϑ > 0 attendu (sec:banque-conditions)")
    if not 0 < par.a_pi < 1.5:
        raise HorsDomaine(f"a_pi = {par.a_pi!r} : 0 < a_π < 1,5 attendu (sec:banque_centrale-conditions)")
    if not par.a_I > 0:
        raise HorsDomaine(f"a_I = {par.a_I!r} : a_I > 0 attendu (sec:banque_centrale-conditions)")
    if not 0 <= par.theta_CB <= 1:
        raise HorsDomaine(f"theta_CB = {par.theta_CB!r} : 0 ≤ θ_CB ≤ 1 attendu (sec:banque_centrale-conditions)")
    for nom in ("varsigma_L", "varsigma_B"):
        val = getattr(par, nom)
        if not 0 <= val <= 1:
            raise HorsDomaine(f"{nom} = {val!r} : dans [0 ; 1] attendu (sec:banque-conditions)")
        if val != 0:
            raise HorsDomaine(f"{nom} = {val!r} : nul à l'état stationnaire (placement réussi, "
                              "sec:banque-stationnaire)")
    for nom in ("p_0", "pr_0", "N_pa_0"):
        if not getattr(par, nom) > 0:
            raise HorsDomaine(f"{nom} = {getattr(par, nom)!r} : > 0 attendu (normalisation)")
    # Borne déclarée des normalisations (voir `BORNE_ECHELLE`) ; une valeur égale à la borne à l'arrondi près passe.
    bas, haut = BORNE_ECHELLE
    for nom, val in (("p_0", par.p_0), ("pr_0", par.pr_0), ("N_pa_0", par.N_pa_0),
                     ("p_0 pr_0 N^pa_0", par.p_0 * par.pr_0 * par.N_pa_0)):
        if not bas * (1 - TOL_BORNE_ECHELLE) <= val <= haut * (1 + TOL_BORNE_ECHELLE):
            raise HorsDomaine(f"{nom} = {val!r} : dans [{bas:g} ; {haut:g}] attendu "
                              "(borne déclarée des normalisations)")
    return declares


# --- Formes fermées : adaptateurs du résolveur ----------------------------------
#
# Les formes fermées ont une seule maison, le module feuille `nations.scenarios.stationnaire` (ADR 0015, points 1
# et 14 ; P247). Les fonctions ci-dessous gardent les signatures du script et ses refus (`HorsDomaine`, mêmes
# messages) : `Parametres` → `EntreesStationnaires` par `CORRESPONDANCE_DES_ENTREES`, appel du module, résultat
# remis en dictionnaire dans l'ordre des champs, qui est l'ordre d'origine des clés.

# Champ d'`EntreesStationnaires` (nom des tables du moteur) → champ de `Parametres` (nom du script).
CORRESPONDANCE_DES_ENTREES: dict[str, str] = {
    "pas_par_an": "n_a", "g_pr": "g_pr", "sigma": "sigma", "kappa": "kappa", "g_N": "g_N", "U_eq": "U_eq",
    "mu_bar": "mu_bar", "nu_H": "nu_H", "delta": "delta", "tu_bar": "tu_bar", "lv_etoile": "lv", "nu_F": "nu_F",
    "zeta": "zeta", "eta_r": "eta_r", "varpi_L": "varpi_L", "varpi_D": "varpi_D", "vartheta": "vartheta",
    "pi_etoile": "pi_cible", "r_bar": "rbar", "theta_CB": "theta_CB", "tau_H": "tau_H", "tau_F": "tau_F",
    "theta_Tr": "theta_Tr", "phi": "phi", "nu_G": "nu_G", "p_0": "p_0", "pr_0": "pr_0", "N_pa_0": "N_pa_0",
}

# Message du refus `HorsDomaine` de chaque condition d'existence (`resolveur.CONDITIONS_D_EXISTENCE`).
MESSAGES_DES_CONDITIONS = {
    "D1": lambda v: f"D1 = {v!r} : 1 − ν_H n_a (1 − τ_H) c > 0 attendu (pôle de la richesse)",
    "D2": lambda v: f"D2 = {v!r} : 1 − ν_G i_CB/(n_a Γ̄) > 0 attendu (existence de l'encaisse)",
    "existence_dividende_banque": lambda v: (f"condition d'existence du dividende de la banque : n_a Π^Bk − n_a γ̄ "
                                             f"E^Bk = {v!r} < 0 (sec:banque-stationnaire)"),
    "Div_F": lambda v: f"Div_F = {v!r} < 0 : dividende stationnaire ≥ 0 attendu (plancher de F3 non contraignant)",
    "theta_G": lambda v: (f"θ_G = {v!r} : θ_G > 0 attendu (demande autonome A = θ_G > 0, part de `macro`, § 6 ; "
                          "sec:finances_publiques-conditions)"),
    "marge_plafond_E1": lambda v: (f"plafond de E1 : ν_G PB − Γ̄ G = {v!r} ≤ 0 attendu > 0 (marge 1 − Γ̄ (G/PB)/ν_G "
                                   "≤ 0, sec:finances_publiques-conditions)"),
    "B": lambda v: f"B = {v!r} : dette brute ≥ 0 attendue (sec:finances_publiques-conditions)",
    "B_Bk": lambda v: f"B_Bk = {v!r} : titres de la banque ≥ 0 attendus (sec:finances_publiques-conditions)",
    "B_CB": lambda v: f"B_CB = {v!r} : titres de la banque centrale ≥ 0 attendus (sec:finances_publiques-conditions)",
    "B_H": lambda v: f"B_H = {v!r} : titres des ménages nuls attendus au socle (C42)",
}


def entrees_stationnaires(par: Parametres) -> resolveur.EntreesStationnaires:
    """Entrées du résolveur lues sur les paramètres du script (`CORRESPONDANCE_DES_ENTREES`)."""
    return resolveur.EntreesStationnaires(**{champ: getattr(par, nom)
                                             for champ, nom in CORRESPONDANCE_DES_ENTREES.items()})


def _en_dictionnaire(valeur: resolveur.Facteurs | resolveur.EtatStationnaire | resolveur.Ouverture
                     ) -> dict[str, object]:
    """Valeur immuable du résolveur (n-uplet nommé) remise en dictionnaire, dans l'ordre de ses champs."""
    return valeur._asdict()


def _etat_du_dictionnaire(e: dict[str, float]) -> resolveur.EtatStationnaire:
    """État du résolveur reconstruit d'un dictionnaire d'état (clés en surnombre ignorées)."""
    return resolveur.EtatStationnaire(**{nom: e[nom] for nom in resolveur.EtatStationnaire._fields})


def _refuser(conditions: tuple[resolveur.ConditionViolee, ...], par: Parametres,
             ecartees: frozenset[str] = frozenset()) -> None:
    """Lève `HorsDomaine` sur la première condition violée, hors des conditions écartées.

    Au point de référence ν_G = 1, hors du domaine ν_G > 1 de la table, le plafond de E1 n'est pas un refus :
    sa marge est rendue (`marge_E1_montant`) et `calculer` publie le point comme constat déclaré, sans valeur
    d'état (décision de `macro`, option (b)). Ce cas reste dans le script (ADR 0015, point 6.3).
    """
    for condition in conditions:
        if condition.identifiant in ecartees:
            continue
        if condition.identifiant == "marge_plafond_E1" and par.nu_G == 1.0:
            continue
        raise HorsDomaine(MESSAGES_DES_CONDITIONS[condition.identifiant](condition.valeur))


def facteurs(par: Parametres, pi: float | None = None) -> dict[str, float]:
    """Facteurs du cadre (`sec:cadre-calendrier`) : G_r, Π_p, Γ̄, γ̄, π^pas, g (`resolveur.facteurs`)."""
    return _en_dictionnaire(resolveur.facteurs(par.n_a, par.g_pr, par.g_N, par.pi_cible if pi is None else pi))


def rho_IN(n: int, sigma: float, g: float, pi: float) -> float:
    """ρ̄_IN, valeur comptable des stocks rapportée au coût du pas (`resolveur.rho_IN`)."""
    return resolveur.rho_IN(n, sigma, g, pi)


def rho_K(n: int, delta: float, g: float, pi: float) -> float:
    """ρ̄_K, valeur comptable du capital rapportée au prix courant (`resolveur.rho_K`)."""
    return resolveur.rho_K(n, delta, g, pi)


def facteur_restitue(n: int, x: float) -> float:
    """Facteur du ratio restitué sur 12 tours (`sec:cadre-calendrier`), x : croissance annuelle du stock."""
    return n * (1 + x) ** (1 / n) / sum((1 + x) ** (-u / n) for u in range(n))


def etat_stationnaire(par: Parametres, r_neutre: float | None = None, rho_bar_L: float | None = None,
                      controler: bool = True) -> dict[str, float]:
    """État stationnaire en formes fermées (`resolveur.etat_stationnaire`), ordre triangulaire de `macro` (§ 3).

    `r_neutre` : taux réel neutre de l'état (r̂* = r̄ de BC1) ; par défaut le
    paramètre r̄ (lecture (e)). Le taux de référence de E4 lit toujours le
    paramètre `par.rbar` (lecture A). `rho_bar_L` : norme ϱ̄_L de S2 ; par
    défaut ϱ_L de l'état (`resolveur.taux`, Δϱ = 0, état initial résolu). Rend
    les niveaux d'ouverture du pas 0 et les flux du pas 0, en u.m., u.v. et
    personnes. `controler` : lever `HorsDomaine` sur les conditions des formes
    fermées (`resolveur.relever_conditions` : D1, D2, existence du dividende de
    la banque, Div_F ≥ 0, θ_G > 0, marge du plafond de E1 > 0 pour ν_G > 1,
    B ≥ 0, B_Bk ≥ 0, B_CB ≥ 0, B_H = 0). Au point de référence ν_G = 1, le
    plafond de E1 n'est pas un refus (`_refuser`) ; les autres conditions y
    restent des refus. Un pôle exact (D1 = 0 ou D2 = 0) est refusé quel que soit
    `controler`. Deux changements de type hors domaine depuis l'extraction (#175,
    commit 1), déclarés : (i) au pôle exact sous `controler=False`, `HorsDomaine`
    au lieu de `ZeroDivisionError` ; (ii) sous `controler=True`, si D1 ≤ 0 (ou
    NaN) et p·y_pot = 0, `ZeroDivisionError` au lieu de `HorsDomaine` sur D1 : le
    résolveur calcule θ_G = G/(p·y_pot) avant le relevé des conditions, alors que
    l'ancien code refusait D1 avant ce calcul. Les deux cas sont hors du domaine
    de `controler_domaine` (p_0, pr_0 > 0, U^eq < 1 ; aucun pôle sur la grille).
    Em ≤ 0 n'est pas un refus : Em = γ̄ B a le signe de γ̄ (rachat
    net si γ̄ < 0).
    """
    entrees = entrees_stationnaires(par)
    r = par.rbar if r_neutre is None else r_neutre
    rho_bar = resolveur.taux(entrees, r).rho_L if rho_bar_L is None else rho_bar_L
    try:
        etat = resolveur.etat_stationnaire(entrees, r, rho_bar)
    except resolveur.EtatStationnaireInexistant as refus:
        _refuser(refus.conditions, par)
        raise
    if controler:
        _refuser(resolveur.relever_conditions(etat), par)
    return _en_dictionnaire(etat)


def controler_etat(e: dict[str, float], par: Parametres) -> None:
    """Conditions de l'état résolu `e` (formes fermées, en montants) ; lève `HorsDomaine`.

    Appelée seule sur un état donné ; `etat_stationnaire` (contrôle activé) juge les mêmes conditions. D1 et D2
    n'y sont pas jugées (elles le sont par `etat_stationnaire`, à la résolution).
    """
    _refuser(resolveur.relever_conditions(_etat_du_dictionnaire(e)), par, ecartees=frozenset({"D1", "D2"}))


# --- Une évaluation des règles sur l'état d'ouverture --------------------------


def ouverture(e: dict[str, float], par: Parametres) -> dict[str, object]:
    """État d'ouverture du pas 0, tel que les sections le résolvent (« État initial résolu » ; `resolveur.ouverture`).

    `mu_tilde_m1` est la marge en logarithme d'ouverture μ̃_{−1} = ln(1 + μ̄), variable d'état du bloc 4 du
    schéma v2 (ADR 0012, annotation du 13/11/2026, point 1.4 ; P54, #112) ; `un_pas` ne la lit pas (P2 y garde
    ln(P_{t−1}/UC_{t−1}), égal à 1e−15 près). Le registre est rendu en liste.
    """
    o = _en_dictionnaire(resolveur.ouverture(_etat_du_dictionnaire(e), entrees_stationnaires(par)))
    o["registre"] = list(o["registre"])
    return o


def un_pas(o: dict[str, object], par: Parametres) -> dict[str, float]:
    """Évalue une fois chaque règle du pas 0 sur l'ouverture `o`, dans l'ordre des phases (`tab:phases`).

    Ce n'est pas une itération dans le temps : c'est la seconde route des
    contrôles. Rend les flux exécutés et les postes de clôture.
    """
    n = par.n_a
    s: dict[str, float] = {}
    P = o["registre"]
    # Phase 0 : facteurs du moteur sur la cible d'ouverture.
    g = (1 + par.g_pr) * (1 + par.g_N) - 1
    pi_c = o["pi_cible"]
    Gam_e = ((1 + g) * (1 + pi_c)) ** (1 / n)
    gam_e = Gam_e - 1
    pis = (1 + pi_c) ** (1 / n) - 1
    Gr = (1 + g) ** (1 / n)
    # Phase 1 : salaires (T2, T3), banque centrale (BC1 à BC6).
    pi_prec = P[0] / P[n] - 1  # π_{t−1} = P_{t−1}/P_{t−1−n_a} − 1
    pr_m1 = o["pr"] * (1 + par.g_pr) ** (-1 / n)
    omega_m1 = o["W_m1"] / (P[0] * pr_m1)  # T2, forme (i) déclarée (voir P2, phase 5)
    omega_c = 1 / (1 + par.mu_bar)
    lnW = (math.log(o["W_m1"]) + (math.log(1 + par.g_pr) + math.log(1 + o["pi_e"])) / n
           + par.lambda_w / n * (math.log(omega_c / omega_m1) - par.beta * (o["U_m1"] - par.U_eq)))  # T3
    W = math.exp(lnW)
    i_CB = (1 + o["r_hat"]) * (1 + pi_c) + par.a_pi * (pi_prec - pi_c) - 1  # BC1
    s["r_hat_1"] = o["r_hat"] + par.a_I / n * (pi_prec - pi_c)  # BC2
    c_e = par.lambda_e / n
    s["pi_e_1"] = (1 - c_e) * o["pi_e"] + c_e * pi_prec  # BC3, forme convexe exécutée (P92, P93)
    s["pi_cible_1"] = pi_c  # BC4
    theta_CB = par.theta_CB  # BC5
    Pi_CB = (i_CB * o["B_CB"] + i_CB * o["L_CB"] - i_CB * o["Res"]) / n  # BC6, i_B = i_res = i_CB
    s.update(i_CB=i_CB, W=W, Pi_CB=Pi_CB, pi_prec=pi_prec)
    # Phase 2 : plans.
    IN_star = n * par.sigma * o["ve"]  # N2
    y_star = max(0.0, o["ve"] + (Gr - 1) * IN_star + par.lambda_IN / n * (IN_star - o["IN_vol"]))  # N3
    N_star = y_star / o["pr"]  # N4
    UC = W / o["pr"]  # N8 (coût unitaire)
    YD_e = Gam_e * o["YD_m1"]  # H2
    V_H = o["D_H"] + o["B_H"]
    V_star = par.nu_H * n * (YD_e - pis * V_H)  # H3
    C_regle = YD_e - gam_e * V_H - par.lambda_H / n * (V_star - V_H)  # H4
    C_plan = min(o["D_H"], max(0.0, C_regle))  # H5
    rho_L = (1 + o["i_L"]) / (1 + pi_c) - 1  # S1
    tu_star = par.tu_bar * math.exp(par.zeta * (rho_L - o["rho_bar_L"]))  # S2
    I_vol_plan = o["ti"] * Gr * o["y_m1"] * math.exp(-par.eta_r * (rho_L - o["rho_bar_L"]))  # S3
    I_plan = P[0] * (1 + pis) * I_vol_plan  # S4
    y_pot = o["pr"] * (1 - par.U_eq) * o["N_pa"]
    G_plan = min(o["M_G"], P[0] * (1 + pis) * o["theta_G"] * y_pot)  # E1
    B = o["B_H"] + o["B_Bk"] + o["B_CB"]
    i_ref = (1 + par.rbar) * (1 + pi_c) - 1
    T_cou = par.phi * (i_CB - i_ref) * (B - o["M_G"] - o["E_CB"]) / n  # E4
    T_H = par.tau_H * Gam_e * o["Y_HS_m1"] + T_cou  # E3
    Tr_lev = P[0] * (1 + pis) * par.theta_Tr * y_pot  # E6
    Tr = min(Tr_lev, max(0.0, o["M_G"] + T_H - i_CB * B / n - G_plan))
    s.update(IN_star=IN_star, y_star=y_star, N_star=N_star, UC=UC, YD_e=YD_e, V_star=V_star, C_regle=C_regle,
             C_plan=C_plan, rho_L=rho_L, tu_star=tu_star, I_vol_plan=I_vol_plan, I_plan=I_plan, G_plan=G_plan,
             T_cou=T_cou, T_H=T_H,
             Tr=Tr, Tr_lev=Tr_lev, plafond_E6=o["M_G"] + T_H - i_CB * B / n - G_plan)
    # Phase 3 : crédit (F1).
    dL_d = par.lv * ((1 - par.delta / n) * o["K"] + I_plan) - o["L"]
    dL = (1 - par.varsigma_L) * max(dL_d, 0.0) + min(dL_d, 0.0)
    # ΔL^d publiée à côté de ΔL (précédent de P93 ; avis de macro, rang 1a de J3-d1, § 2).
    s["dL_d"] = dL_d
    s["dL"] = dL
    # Phase 4 : travail, puis production (T1, T4 à T6, N5, N11).
    s["N_pa_1"] = o["N_pa"] * (1 + par.g_N) ** (1 / n)  # T1
    N = min(o["N_pa"], max(N_star, (1 + par.g_N) ** (1 / n) * (1 - par.lambda_N / n) * o["N_m1"]
                           + par.lambda_N / n * N_star))  # T4
    U = 1 - N / o["N_pa"]  # T5
    WB = W * N  # T6
    y = min(y_star, o["pr"] * N)  # N5
    y_cap = o["K_vol"] / (n * par.kappa)  # N11
    tu = y / y_cap
    s.update(N=N, U=U, WB=WB, y=y, y_cap=y_cap, tu=tu)
    # Phase 5 : prix (P1 à P4), puis production (N1, N6 à N10), puis acheteurs (H6, S5, E2), S6.
    xi = 1 - o["IN_vol"] / IN_star  # P1
    # P2 et T2 sous la forme (i) : marge d'ouverture ln(P_{t−1}/UC_{t−1}) tirée du registre et de W_{t−1},
    # forme indépendante déclarée (#125, point 3) ; le moteur lit l'état μ̃_{t−1} (P54, option (ii)). Égales
    # à l'arrondi près sur l'état résolu, les deux formes divergent sur un état où μ̃ ≠ ln(P/UC).
    UC_m1 = o["W_m1"] / pr_m1
    mu_t = ((1 - par.lambda_mu / n) * math.log(P[0] / UC_m1)
            + par.lambda_mu / n * (math.log(1 + par.mu_bar) + par.psi_xi * xi))  # P2
    p = UC * math.exp(mu_t)  # P3 ; P4 : P_t ≡ p
    d_H, d_F, d_G = C_plan / p, I_plan / p, G_plan / p  # N6
    d = d_H + d_F + d_G
    if d == 0.0:
        # Le moteur rend des ventes et des volumes servis nuls à d = 0 (`nations.blocs.production.ventes`) ;
        # le script, qui sert chaque acheteur au taux v/d, refuse ce point au lieu de le couvrir (#125, point 4).
        raise HorsDomaine("N6 : demande adressée d = 0, taux de service v/d non défini (le moteur rend des "
                          "volumes servis nuls ; état hors du domaine du script)")
    disponible = o["IN_vol"] + y  # calculé une fois : v et IN^vol_{t+1} sur la même valeur
    v = min(d, disponible)
    v_H, v_F, v_G = v / d * d_H, v / d * d_F, v / d * d_G
    IN_vol_1 = disponible - v  # N7
    cm = (o["IN"] + UC * y) / disponible  # N8
    dIN = cm * IN_vol_1 - o["IN"]  # N8, forme B (P72) : ΔIN = cm IN^vol_{t+1} − IN_t
    pr_1 = o["pr"] * (1 + par.g_pr) ** (1 / n)  # N9
    K_vol_1 = (1 - par.delta / n) * o["K_vol"] + v_F  # N10
    ve_1 = Gr * ((1 - par.lambda_v / n) * o["ve"] + par.lambda_v / n * d)  # N1
    C = p * v_H  # H6
    I = p * v_F  # S5
    G = p * v_G  # E2
    ti_1 = o["ti"] * math.exp(par.lambda_ti / n * (tu - tu_star))  # S6
    s.update(xi=xi, mu_tilde=mu_t, p=p, d=d, v=v, IN_vol_1=IN_vol_1, dIN=dIN, pr_1=pr_1, K_vol_1=K_vol_1,
             ve_1=ve_1, C=C, I=I, G=G, ti_1=ti_1, IN_1=o["IN"] + dIN)
    # Phase 6 : revenus et impôts (S7, B3, B4, E5, F2 à F4, B5, B6, E7).
    amort = par.delta * o["K"] / n  # S7
    l9 = o["i_L"] * o["L"] / n  # B3
    l10_H = o["i_D"] * o["D_H"] / n  # B4
    l10_F = o["i_D"] * o["D_F"] / n
    Pi_av = C + G + I + dIN - WB - amort - l9 + l10_F  # E5
    T_F = par.tau_F * Pi_av
    D_F_star = par.nu_F * n * P[0] * (1 + pis) ** 2 * ve_1  # F2
    T_F_e = Gam_e * o["T_F_m1"]  # F4
    Div_F = max(0.0, o["D_F"] + dL + C + G - WB - l9 + l10_F - T_F_e - D_F_star)  # F3
    L_1 = o["L"] + dL
    Pi_Bk = (o["i_L"] * o["L"] + i_CB * o["B_Bk"] + i_CB * o["Res"] - o["i_D"] * (o["D_H"] + o["D_F"])
             - i_CB * o["L_CB"]) / n  # B5
    Div_Bk = max(0.0, o["E_Bk"] + Pi_Bk - par.vartheta * L_1)  # B6
    l11a = i_CB * o["B_H"] / n  # E7
    l11b = i_CB * o["B_Bk"] / n
    l11c = i_CB * o["B_CB"] / n
    s.update(amort=amort, l9=l9, l10_H=l10_H, l10_F=l10_F, Pi_av=Pi_av, T_F=T_F, D_F_star=D_F_star, T_F_e=T_F_e,
             Div_F=Div_F, Pi_Bk=Pi_Bk, Div_Bk=Div_Bk, l11a=l11a, l11b=l11b, l11c=l11c, L_1=L_1)
    # Phase 7 : titres publics (E8 à E12).
    PB = G + Tr + i_CB * B / n  # E8
    M_G_star = par.nu_G * PB
    Em = G + Tr + i_CB * B / n - T_H - T_F - Pi_CB + M_G_star - o["M_G"]  # E9
    dB_CB = theta_CB * Em  # E10
    dB_H = 0.0
    dB_Bk = (1 - par.varsigma_B) * (Em - dB_CB)  # E11
    Y_HS = WB + o["i_D"] * o["D_H"] / n + Div_F + Div_Bk - pis * o["D_H"] - T_cou  # E12
    s.update(PB=PB, M_G_star=M_G_star, Em=Em, dB_CB=dB_CB, dB_H=dB_H, dB_Bk=dB_Bk, Y_HS=Y_HS)
    # Phase 8 : (a) lignes 12 et 13 ; (b) ligne 16, E13 ; (c) B7, B1, B2.
    l12 = i_CB * o["Res"] / n  # BC7
    l13 = i_CB * o["L_CB"] / n  # BC8
    l16 = Pi_CB  # BC9
    M_G_8a = o["M_G"] - G - Tr + T_H + T_F - l11a - l11b - l11c + dB_H + dB_Bk + dB_CB
    perte_non_couverte = max(0.0, -Pi_CB - M_G_8a)  # E13
    tr_non_verses = Tr_lev - Tr
    # Position de réserves après tous les règlements : lignes 2, 6, 7, 11a (compte du Trésor ↔ banque),
    # 11b, 12, −13, −19a-banque (19b-banque nulle au socle).
    Res_8b = o["Res"] + G + Tr - T_H - T_F + l11a + l11b + l12 - l13 - dB_Bk
    # B7 en forme −min, algébriquement égale à max(L^CB − Res^8b ; 0) − L^CB (P93 ; ADR 0013, annotation
    # du 14/11/2026, point 9) : Res_{t+1} et L^CB_{t+1} ≥ 0 et Res_{t+1} L^CB_{t+1} = 0 exactement.
    dL_CB = -min(Res_8b, o["L_CB"])  # B7
    L_CB_1 = o["L_CB"] + dL_CB
    Res_1 = Res_8b + dL_CB
    s.update(l12=l12, l13=l13, l16=l16, M_G_8a=M_G_8a, perte_non_couverte=perte_non_couverte,
             tr_non_verses=tr_non_verses, Res_8b=Res_8b, L_CB_1=L_CB_1, dL_CB=dL_CB, Res_1=Res_1,
             i_L_1=i_CB + par.varpi_L, i_D_1=i_CB - par.varpi_D)  # B1, B2
    # Phase 9 : revenu disponible (H7), registre.
    YD = WB + Tr - T_H + l10_H + l11a + Div_F + Div_Bk  # H7
    s["YD"] = YD
    s["P_0"] = p
    # Postes de clôture, par les flux (aucun poste n'est obtenu par différence).
    s["D_H_1"] = o["D_H"] + WB - C + Tr - T_H + l10_H + l11a + Div_F + Div_Bk - dB_H
    s["D_F_1"] = o["D_F"] + dL - WB + C + G - l9 + l10_F - T_F - Div_F
    s["K_1"] = o["K"] + I - amort
    s["B_Bk_1"] = o["B_Bk"] + dB_Bk
    s["B_CB_1"] = o["B_CB"] + dB_CB
    s["B_H_1"] = o["B_H"] + dB_H
    s["M_G_1"] = M_G_8a + l16
    s["E_Bk_1_flux"] = o["E_Bk"] + Pi_Bk - Div_Bk
    s["E_CB_1_flux"] = o["E_CB"] + Pi_CB - l16
    s["E_Bk_1_stock"] = L_1 + s["B_Bk_1"] + Res_1 - s["D_H_1"] - s["D_F_1"] - L_CB_1
    s["E_CB_1_stock"] = s["B_CB_1"] + L_CB_1 - Res_1 - s["M_G_1"]
    return s


# --- Résidus des règles, identités, matrices et routes doubles -------------------


def _residu(obtenu: float, attendu: float, echelle: float) -> float:
    """|obtenu − attendu| rapporté à max(|attendu|, échelle) : relatif, jamais absolu."""
    return abs(obtenu - attendu) / max(abs(attendu), echelle)


def residus_des_regles(e: dict[str, float], s: dict[str, float], par: Parametres) -> dict[str, float]:
    """Propriété P2 de `macro` : chaque règle évaluée une fois rend la valeur du pas suivant sur le sentier.

    Échelles : PIB du pas pour un flux, n_a·PIB pour un stock en u.m., 1 pour
    un taux (fraction par an) ou un rapport sans dimension, la grandeur
    elle-même pour un volume, un prix ou un effectif.
    """
    n = par.n_a
    Gam, Gr = e["Gam"], e["Gr"]
    flux, stock = e["PIB"], n * e["PIB"]
    paires = {
        # (obtenu, attendu, échelle)
        "N1 v^e_{t+1} = G_r v^e": (s["ve_1"], Gr * e["ve"], 0.0),
        "N2 IN^vol* = IN^vol": (s["IN_star"], e["IN_vol"], 0.0),
        "N3 y* = y": (s["y_star"], e["y"], 0.0),
        "N4 N* = N": (s["N_star"], e["N"], 0.0),
        "N5 y = pr N": (s["y"], e["y"], 0.0),
        "N6 v = d": (s["v"], e["v"], 0.0),
        "N7 IN^vol_{t+1} = G_r IN^vol": (s["IN_vol_1"], Gr * e["IN_vol"], 0.0),
        "N8 UC": (s["UC"], e["UC"], 0.0),
        "N8 ΔIN": (s["dIN"], e["dIN"], flux),
        "N8 IN_{t+1} = Γ̄ IN": (s["IN_1"], Gam * e["IN"], stock),
        "N9 pr_{t+1}": (s["pr_1"], Gr * e["pr"], 0.0),
        "N10 K^vol_{t+1} = G_r K^vol": (s["K_vol_1"], Gr * e["K_vol"], 0.0),
        "N11 tu": (s["tu"], e["tu"], 1.0),
        "T1 N^pa_{t+1}": (s["N_pa_1"], e["N_pa"] * (1 + par.g_N) ** (1 / n), 0.0),
        "T3 W_t": (s["W"], e["W"], 0.0),
        "T4 N_t": (s["N"], e["N"], 0.0),
        "T5 U_t = U^eq": (s["U"], par.U_eq, 1.0),
        "T6 WB": (s["WB"], e["WB"], flux),
        "P1 ξ = 0": (s["xi"], 0.0, 1.0),
        "P2 μ̃ = ln(1 + μ̄)": (s["mu_tilde"], math.log(1 + par.mu_bar), 1.0),
        "P3 p_t": (s["p"], e["p"], 0.0),
        "H2 YD^e = YD": (s["YD_e"], e["YD"], flux),
        "H3 V* = V_H": (s["V_star"], e["V_H"], stock),
        "H4 C^règle = C": (s["C_regle"], e["C"], flux),
        "H5 C^plan = C": (s["C_plan"], e["C"], flux),
        "H6 C": (s["C"], e["C"], flux),
        "H7 YD": (s["YD"], e["YD"], flux),
        "S1 ϱ_L": (s["rho_L"], e["rho_L"], 1.0),
        "S2 tu* = tu": (s["tu_star"], e["tu"], 1.0),
        "S3-S4 I^plan = I": (s["I_plan"], e["I"], flux),
        "S5 I": (s["I"], e["I"], flux),
        "S6 ti_{t+1} = ti": (s["ti_1"], e["ti"], 1.0),
        "S7 amortissement": (s["amort"], par.delta * e["K"] / n, flux),
        "S7 K_{t+1} = Γ̄ K": (s["K_1"], Gam * e["K"], stock),
        "F1 ΔL = γ̄ L": (s["dL"], e["dL"], flux),
        "F2 D*_F = Γ̄ D_F": (s["D_F_star"], Gam * e["D_F"], stock),
        "F3 Div_F": (s["Div_F"], e["Div_F"], flux),
        "F4 T^e_F = T_F": (s["T_F_e"], e["T_F"], flux),
        "B1 i_L": (s["i_L_1"], e["i_L"], 1.0),
        "B2 i_D": (s["i_D_1"], e["i_D"], 1.0),
        "B5 Π^Bk": (s["Pi_Bk"], e["Pi_Bk"], flux),
        "B6 Div_Bk": (s["Div_Bk"], e["Div_Bk"], flux),
        "B7 L^CB_{t+1} = Γ̄ L^CB": (s["L_CB_1"], Gam * e["L_CB"], stock),
        "BC1 i_CB = i^règle": (s["i_CB"], e["i_CB"], 1.0),
        "BC2 r̂*_{t+1} = r̂*": (s["r_hat_1"], e["r_hat"], 1.0),
        "BC3 π^e_{t+1} = π^e": (s["pi_e_1"], e["pi_e"], 1.0),
        "BC4 π*_{t+1} = π*": (s["pi_cible_1"], par.pi_cible, 1.0),
        "BC6 Π^CB": (s["Pi_CB"], e["Pi_CB"], flux),
        "E1 G^plan = G": (s["G_plan"], e["G"], flux),
        "E2 G": (s["G"], e["G"], flux),
        "E3 T_H": (s["T_H"], e["T_H"], flux),
        "E4 T^cou": (s["T_cou"], e["T_cou"], flux),
        "E5 T_F": (s["T_F"], e["T_F"], flux),
        "E6 Tr": (s["Tr"], e["Tr"], flux),
        "E8 M^G* = Γ̄ M^G": (s["M_G_star"], Gam * e["M_G"], stock),
        "E9 Em = γ̄ B": (s["Em"], e["gam"] * e["B"], flux),
        "E11 ΔB_Bk": (s["dB_Bk"], e["gam"] * e["B_Bk"], flux),
        "E12 Y^HS": (s["Y_HS"], e["Y_HS"], flux),
        "E13 parts non payées nulles": (s["perte_non_couverte"] + s["tr_non_verses"], 0.0, flux),
        "registre π_{t−1} = π*": (s["pi_prec"], par.pi_cible, 1.0),
        "P4 P_t/P_{t−n_a} − 1 = π*": (s["P_0"] / ouverture(e, par)["registre"][n - 1] - 1, par.pi_cible, 1.0),
    }
    return {nom: _residu(o, a, ech) for nom, (o, a, ech) in paires.items()}


SECTEURS = ("H", "F_courant", "F_capital", "Bk", "CB", "G")


def echelle_CB(e: dict[str, float]) -> float:
    """Échelle S^CB du bilan de la banque centrale : B^CB + L^CB + |Res| + M^G (routes doubles, complémentarité)."""
    return e["B_CB"] + e["L_CB"] + abs(e["Res"]) + e["M_G"]


def matrices(e: dict[str, float], s: dict[str, float], par: Parametres) -> dict[str, object]:
    """Matrices des bilans (ouverture) et des flux (pas 0), `tab:matrice-bilans` et `tab:matrice-flux`.

    Les flux décidés viennent des règles évaluées une fois (`un_pas`) ; les
    postes de règlement (lignes 17, 20, 22) viennent de la forme fermée
    (croissance Γ̄ des encours) : une colonne nulle prouve l'accord des deux
    routes, elle n'est pas nulle par construction. Les sommes sont rapportées
    à l'échelle S (`sec:cadre-identites`) : somme des valeurs absolues des
    postes du bilan contrôlé, valeur nette comprise.
    """
    # Bilans d'ouverture, colonnes de secteur ; la colonne « Réel » solde les actifs réels.
    gam = e["gam"]
    E_Bk = e["L"] + e["B_Bk"] + e["Res"] - e["D_H"] - e["D_F"] - e["L_CB"]
    E_CB = e["B_CB"] + e["L_CB"] - e["Res"] - e["M_G"]
    V_G = e["M_G"] - e["B_H"] - e["B_Bk"] - e["B_CB"]
    bil = {
        "capital": {"F": e["K"], "Reel": -e["K"]},
        "stocks": {"F": e["IN"], "Reel": -e["IN"]},
        "depots": {"H": e["D_H"], "F": e["D_F"], "Bk": -e["D_H"] - e["D_F"]},
        "credits": {"F": -e["L"], "Bk": e["L"]},
        "titres": {"H": e["B_H"], "Bk": e["B_Bk"], "CB": e["B_CB"], "G": -e["B_H"] - e["B_Bk"] - e["B_CB"]},
        "reserves": {"Bk": e["Res"], "CB": -e["Res"]},
        "refinancement": {"Bk": -e["L_CB"], "CB": e["L_CB"]},
        "compte_tresor": {"CB": -e["M_G"], "G": e["M_G"]},
        "valeur_nette": {"H": -e["V_H"], "F": -e["V_F"], "Bk": -E_Bk, "CB": -E_CB, "G": -V_G,
                         "Reel": e["K"] + e["IN"]},
    }
    cols_bil = ("H", "F", "Bk", "CB", "G", "Reel")
    # Postes de règlement : forme fermée (Γ̄ × ouverture).
    dD_H, dD_F, dM_G = gam * e["D_H"], gam * e["D_F"], gam * e["M_G"]
    dRes = s["Res_1"] - e["Res"]
    flx = {
        "1": {"H": -s["C"], "F_courant": s["C"]},
        "2": {"F_courant": s["G"], "G": -s["G"]},
        "3": {"F_courant": s["I"], "F_capital": -s["I"]},
        "4": {"F_courant": s["dIN"], "F_capital": -s["dIN"]},
        "5": {"H": s["WB"], "F_courant": -s["WB"]},
        "6": {"H": s["Tr"], "G": -s["Tr"]},
        "7": {"H": -s["T_H"], "F_courant": -s["T_F"], "G": s["T_H"] + s["T_F"]},
        "8": {"F_courant": -s["amort"], "F_capital": s["amort"]},
        "9": {"F_courant": -s["l9"], "Bk": s["l9"]},
        "10": {"H": s["l10_H"], "F_courant": s["l10_F"], "Bk": -s["l10_H"] - s["l10_F"]},
        "11a": {"H": s["l11a"], "G": -s["l11a"]},
        "11b": {"Bk": s["l11b"], "G": -s["l11b"]},
        "11c": {"CB": s["l11c"], "G": -s["l11c"]},
        "12": {"Bk": s["l12"], "CB": -s["l12"]},
        "13": {"Bk": -s["l13"], "CB": s["l13"]},
        "14": {"H": s["Div_F"], "F_courant": -s["Div_F"]},
        "15": {"H": s["Div_Bk"], "Bk": -s["Div_Bk"]},
        "16": {"CB": -s["l16"], "G": s["l16"]},
        "17": {"H": -dD_H, "F_capital": -dD_F, "Bk": dD_H + dD_F},
        "18": {"F_capital": s["dL"], "Bk": -s["dL"]},
        "19a-menages": {"H": -s["dB_H"], "G": s["dB_H"]},
        "19a-banque": {"Bk": -s["dB_Bk"], "G": s["dB_Bk"]},
        "19a-BC": {"CB": -s["dB_CB"], "G": s["dB_CB"]},
        "19b-menages": {"H": 0.0, "CB": -0.0},
        "19b-banque": {"Bk": 0.0, "CB": -0.0},
        "20": {"Bk": -dRes, "CB": dRes},
        "21": {"Bk": s["dL_CB"], "CB": -s["dL_CB"]},
        "22": {"CB": dM_G, "G": -dM_G},
    }
    # Échelles.
    S_secteur_bil = {c: sum(abs(bil[l].get(c, 0.0)) for l in bil) for c in cols_bil}
    S_total = sum(S_secteur_bil.values())
    S_Bk = e["L"] + e["B_Bk"] + abs(e["Res"]) + e["D_H"] + e["D_F"] + e["L_CB"] + abs(E_Bk)
    # La colonne CB de la matrice des bilans porte aussi sa valeur nette −E^CB : |E^CB| s'ajoute à l'échelle commune.
    S_CB = echelle_CB(e) + abs(E_CB)
    lignes_bil = {l: abs(sum(v.values())) / S_total for l, v in bil.items()}
    colonnes_bil = {c: abs(sum(bil[l].get(c, 0.0) for l in bil)) / S_total for c in cols_bil}
    lignes_flx = {l: abs(sum(v.values())) / S_total for l, v in flx.items()}
    secteurs_flx = {}
    for c, cles in (("H", ("H",)), ("F", ("F_courant", "F_capital")), ("Bk", ("Bk",)), ("CB", ("CB",)), ("G", ("G",))):
        tot = sum(flx[l].get(k, 0.0) for l in flx for k in cles)
        S_c = S_Bk if c == "Bk" else S_CB if c == "CB" else max(S_secteur_bil[c if c != "F" else "F"], 1e-300)
        secteurs_flx[c] = abs(tot) / S_c
    # Valeur nette calculée deux fois : stock de clôture (Γ̄ × ouverture) et flux du pas.
    FU_regle = s["C"] + s["G"] + s["I"] + s["dIN"] - s["WB"] - s["T_F"] - s["amort"] - s["l9"] + s["l10_F"] - s["Div_F"]
    V_flux = {
        "H": e["V_H"] + s["YD"] - s["C"],
        "F": e["V_F"] + FU_regle,
        "Bk": s["E_Bk_1_flux"],
        "CB": s["E_CB_1_flux"],
        "G": V_G + s["T_H"] + s["T_F"] + s["l16"] - s["G"] - s["Tr"] - s["l11a"] - s["l11b"] - s["l11c"],
    }
    V_stock = {"H": e["Gam"] * e["V_H"], "F": e["Gam"] * e["V_F"], "Bk": s["E_Bk_1_stock"],
               "CB": s["E_CB_1_stock"], "G": e["Gam"] * V_G}
    valeurs_nettes = {c: abs(V_flux[c] - V_stock[c]) / (S_Bk if c == "Bk" else S_CB if c == "CB" else S_secteur_bil[c])
                      for c in V_flux}
    somme_vn = abs(sum(V_stock.values()) - e["Gam"] * (e["K"] + e["IN"])) / S_total
    return {
        "bilans": bil, "flux": flx, "S_total": S_total, "S_Bk": S_Bk, "S_CB": S_CB,
        "lignes_bilans": lignes_bil, "colonnes_bilans": colonnes_bil, "lignes_flux": lignes_flx,
        "secteurs_flux": secteurs_flx, "valeurs_nettes": valeurs_nettes, "somme_valeurs_nettes": somme_vn,
    }


def routes_doubles(e: dict[str, float], s: dict[str, float], par: Parametres) -> dict[str, float]:
    """Contrôles par deux routes indépendantes (part de `monnaie`, § 6.3), rapportés à S^Bk ou à S^CB."""
    n = par.n_a
    gam = e["gam"]
    S_Bk = e["L"] + e["B_Bk"] + abs(e["Res"]) + e["D_H"] + e["D_F"] + e["L_CB"] + e["E_Bk"]
    S_CB = echelle_CB(e)
    deficit_flux = s["G"] + s["Tr"] + s["l11a"] + s["l11b"] + s["l11c"] - s["T_H"] - s["T_F"] - s["l16"]
    return {
        # 1. Route de l'État : (Γ̄ − 1) B = Em (E9 à E11), contre B_Bk par C42.
        "C42 : (Γ̄ − 1) B_Bk (C42) contre Em (E9, E11)": abs(s["dB_Bk"] - gam * e["B_Bk"]) / S_Bk,
        "C42 : déficit par les flux contre γ̄ (B − M^G − E^CB)": abs(deficit_flux - gam * e["D_c"]) / S_Bk,
        # 2. B7 sur la position du grand livre.
        "B7 : Res^8b − L^CB = −M^G*": abs(s["Res_8b"] - e["L_CB"] + s["M_G_star"]) / S_CB,
        "B7 : L^CB_{t+1} = Γ̄ L^CB": abs(s["L_CB_1"] - e["Gam"] * e["L_CB"]) / S_CB,
        "B7 : Res_{t+1} = 0": abs(s["Res_1"]) / S_CB,
        # 3. Π^Bk par B5 (cinq encours) contre la forme réduite.
        "B5 : forme brute contre forme réduite": abs(s["Pi_Bk"] - (e["i_CB"] * e["E_Bk"] + par.varpi_L * e["L"]
                                                               + par.varpi_D * (e["D_H"] + e["D_F"])) / n) / S_Bk,
        # 4. Div_Bk par B6 contre 1 − n_a(Γ̄ − 1)/rendement des fonds propres ; sans fonds propres (lv* = 0), le
        # rendement est sans objet et la forme se lit Div_Bk = Π^Bk.
        "B6 : contre (1 − n_a(Γ̄ − 1)/ROE) Π^Bk": abs(s["Div_Bk"] - (
            (1 - n * gam / (n * e["Pi_Bk"] / e["E_Bk"])) * e["Pi_Bk"] if e["E_Bk"] != 0 else e["Pi_Bk"])) / S_Bk,
        # Fonds propres par le stock et par les flux.
        "E^Bk de clôture : stock contre flux": abs(s["E_Bk_1_stock"] - s["E_Bk_1_flux"]) / S_Bk,
        # Complémentarité Res · L^CB = 0, écrite min(|Res|, |L^CB|)/S_CB : nulle si et seulement si l'un des deux
        # encours l'est, rapportée à l'échelle du bilan (et non à son carré, qui sort de la plage des flottants).
        "Res · L^CB (ouverture)": min(abs(e["Res"]), abs(e["L_CB"])) / S_CB,
    }


# --- Grandeurs publiées -----------------------------------------------------------


@dataclass(frozen=True)
class Grandeur:
    """Grandeur publiée : définition, unité, dénominateur, fenêtre (exigences, § 2)."""

    ident: str
    definition: str
    unite: str
    denominateur: str
    fenetre: str
    source: str


OUV, PAS, AN = "ouverture du pas", "pas (= rapport sur 12 tours)", "annuelle"


def _caisse(e, par):
    """Marges de la lecture nette du contrôle de caisse (`sec:cadre-caisse`), flux d'un pas stationnaire."""
    n = par.n_a
    DH4 = e["D_H"] + e["WB"]
    DH5 = DH4 - e["C"]
    DH6 = DH5 + e["Tr"] - e["T_H"] + e["i_D"] * e["D_H"] / n + e["Div_F"] + e["Div_Bk"]
    DF3 = e["D_F"] + e["dL"]
    DF4 = DF3 - e["WB"]
    MG5 = e["M_G"] - e["G"]
    MG6 = MG5 + e["T_H"] + e["T_F"] - e["Tr"] - e["interets"]
    MG7 = e["M_G_star"] - e["Pi_CB"]
    return {"DH4": DH4 / e["D_H"], "DH5": DH5 / e["D_H"], "DH6": DH6 / e["D_H"],
            "DF4": DF4 / e["D_F"], "MG5": MG5 / e["M_G"], "MG6": MG6 / e["M_G"], "MG7": MG7 / e["M_G"],
            "MG8b": e["M_G_star"] / e["M_G"],
            "nu_F_min": (e["WB"] - e["dL"]) / (n * e["p"] * e["v"])}


def _rapport(numerateur: float, denominateur: float) -> float:
    """Rapport publié ; « sans objet » (NaN, affiché comme tel) si le dénominateur est nul (bord fermé du domaine)."""
    return numerateur / denominateur if denominateur != 0 else math.nan


def valeurs(e: dict[str, float], par: Parametres) -> dict[str, float]:
    """Valeurs des grandeurs de `GRANDEURS` en un point, dans l'unité publiée.

    Un rapport dont le dénominateur est nul sur un bord fermé du domaine (lv* = 0 : L = E^Bk = 0 ; τ_H = 0 :
    T_H = 0) est publié « sans objet », jamais par une exception.
    """
    n = par.n_a
    P = e["PIB"]
    A = n * P  # PIB annuel du test zéro
    pi = par.pi_cible
    o = ouverture(e, par)  # registre et salaire d'ouverture, en formes fermées (aucune règle évaluée ici)
    caisse = _caisse(e, par)
    hausse_W = ((1 + par.g_pr) * (1 + pi)) ** (1 / n) - 1
    roe = _rapport(n * e["Pi_Bk"], e["E_Bk"])
    actif_Bk = e["L"] + e["B_Bk"] + e["Res"]
    D_c = e["D_c"] / A
    v_H, l, d_F, e_Bk = e["V_H"] / A, e["L"] / A, e["D_F"] / A, e["E_Bk"] / A
    YD_an = e["YD"] / P  # revenu disponible annuel rapporté au PIB annuel
    PiBk = e["Pi_Bk"] / P
    nu_min = HAUSSE_J_NU * e["Gam"] * e["G"] / (e["X"] + HAUSSE_J_NU * e["Gam"] * e["G"] * e["a"])
    nu_J = HAUSSE_J_NU * e["Gam"] * e["G"] / ((1 - MARGE_J_NU) * e["X"] + HAUSSE_J_NU * e["Gam"] * e["G"] * e["a"])
    x_stock = (1 + e["g"]) * (1 + pi) - 1
    v = {
        "Gamma": e["Gam"], "gamma_pas": 100 * e["gam"], "pi_pas": 100 * e["pis"],
        "glissement": 100 * (e["p"] / o["registre"][n - 1] - 1),
        "facteur_stock": facteur_restitue(n, x_stock), "facteur_volume": facteur_restitue(n, e["g"]),
        "i_CB": 100 * e["i_CB"], "i_L": 100 * e["i_L"], "i_D": 100 * e["i_D"], "i_ref": 100 * e["i_ref"],
        "rbar": 100 * e["r_neutre"], "r_restitue": 100 * (e["i_CB"] - pi), "rho_L": 100 * e["rho_L"],
        "r_exact": 100 * (n * math.log(1 + e["i_CB"] / n) - math.log(1 + pi)),
        "r_HS": 100 * (e["i_CB"] - n * e["pis"]),
        "rendement_reel_depots": 100 * (e["i_D"] - pi),
        "T_cou": 100 * e["T_cou"] / P,
        "y_sur_v": e["y_sur_v"], "IN_sur_v": e["IN_vol"] / e["v"], "rho_IN": e["rho_IN"],
        "dIN_sur_IN": 100 * e["dIN"] / e["IN"], "tu": e["tu"],
        "marge_disponibilite": (e["IN_vol"] + e["y"] - e["v"]) / e["v"],
        "K_vol_sur_y": e["K_vol"] / (n * e["y"]), "K_courant": e["p"] * e["K_vol"] / A, "K_comptable": e["K"] / A,
        "rho_K": e["rho_K"], "ecart_valorisation": 100 * (e["rho_K"] - 1),
        "ecart_valorisation_cloture": 100 * (e["rho_K"] * e["Pp"] - 1),
        "U": e["U"], "omega": e["W"] / (e["p"] * e["pr"]),
        "hausse_salaire_pas": 100 * hausse_W,
        "hausse_salaire_an": 100 * ((1 + hausse_W) ** n - 1),
        "part_salariale": e["WB"] / P, "ecart_part_salariale": 100 * (1 / (1 + par.mu_bar) - e["WB"] / P),
        "xi": 1 - e["IN_vol"] / (n * par.sigma * e["ve"]), "mu_tilde": math.log(e["p"] / e["UC"]),
        "hausse_prix_pas": 100 * (e["p"] / o["registre"][0] - 1),
        "richesse_HS": e["V_H"] / (n * (e["YD"] - e["pis"] * e["V_H"])), "richesse_YD": e["V_H"] / (n * e["YD"]),
        "epargne": 100 * (1 - e["C"] / e["YD"]), "epargne_maintien": 100 * e["pis"] * e["V_H"] / e["YD"],
        "epargne_reelle": 100 * (e["gam"] - e["pis"]) * e["V_H"] / e["YD"],
        "epargne_residu": abs((1 - e["C"] / e["YD"]) - e["gam"] * e["V_H"] / e["YD"]),
        "C_sur_YD": e["C"] / e["YD"], "epargne_visee": 100 * (1 - e["C"] / (e["YD"] - e["pis"] * e["V_H"])),
        "marge_plafond_mois": e["D_H"] / e["C"] * 12 / n, "V_H_sur_YD": e["V_H"] / e["YD"],
        "plancher_budget": e["C"] / e["YD"],
        "impot_inflation": 100 * (n * e["pis"] - e["i_D"]) * e["V_H"] / (n * e["YD"]),
        "ti": e["ti"], "I_sur_PIB": 100 * e["I"] / P, "L_sur_K": e["L"] / e["K"],
        "D_F_sur_ventes": e["D_F"] / (n * e["p"] * e["ve"]), "credits": l, "credits_nets": (e["L"] - e["D_F"]) / A,
        "depots_F": d_F, "V_F": e["V_F"] / A, "FU_sur_V_F": 100 * e["FU"] / e["V_F"],
        "distribution": e["Div_F"] / (e["Div_F"] + e["FU"]), "Div_F_sur_ventes": 100 * e["Div_F"] / (e["p"] * e["v"]),
        "levier_courant": par.lv * e["rho_K"],
        "e_Bk": e_Bk, "E_sur_L": _rapport(e["E_Bk"], e["L"]), "masse_monetaire": (e["V_H"] + e["D_F"]) / A,
        "reserves": e["Res"] / A, "refinancement": e["L_CB"] / A, "titres_Bk": e["B_Bk"] / A,
        "Pi_Bk": 100 * PiBk, "roe": 100 * roe, "part_distribuee_Bk": _rapport(e["Div_Bk"], e["Pi_Bk"]),
        "existence_Bk": e["existence_Bk"], "part_titres": e["B_Bk"] / actif_Bk,
        "marge_nette": 100 * n * e["Pi_Bk"] / actif_Bk, "domar_E_Bk": 100 * n * e["gam"] * e_Bk,
        "couplage": -par.vartheta * par.lv,
        "canal_rentier": 100 * 0.01 * D_c / YD_an, "part_v_H": 100 * _rapport(v_H, D_c),
        "part_entreprises": -100 * _rapport(l - d_F, D_c), "part_E_Bk": 100 * _rapport(e_Bk, D_c),
        "saut_C29": 100 * _rapport(0.01 * D_c, PiBk), "saut_C29_suite": 100 * _rapport(0.01 * e_Bk, PiBk),
        "d2": 100 * (_rapport(0.01 * D_c, e_Bk) + 11 * 0.01) / 12,
        "pi_e": 100 * e["pi_e"], "r_hat": 100 * e["r_hat"],
        "Pi_CB": 100 * e["Pi_CB"] / P, "monnaie_centrale": e["Res"] / A, "E_CB": e["E_CB"] / A,
        "titres_CB": e["B_CB"] / A,
        "theta_G": e["theta_G"], "G_sur_PIB": 100 * e["G"] / P, "T_H_sur_PIB": 100 * e["T_H"] / P,
        "G_sur_PB": e["G"] / e["PB"], "Y_HS": e["Y_HS"] / P, "YD_HS": e["YD_HS"] / P,
        "taux_apparent": 100 * e["T_H"] / e["Y_HS"], "encaisse": e["M_G"] / A,
        "dette_brute": e["B"] / A, "dette_consolidee": D_c, "decomp_v_H": v_H, "decomp_entreprises": -(l - d_F),
        "decomp_E_Bk": e_Bk, "domar_facteur": 100 * n * e["gam"], "deficit_i": 100 * n * e["gam"] * D_c,
        "deficit_ii": 100 * (e["G"] + e["Tr"] + e["interets"] - e["T_H"] - e["T_F"] - e["Pi_CB"]) / P,
        "primaire": 100 * (e["T_H"] + e["T_F"] - e["G"] - e["Tr"]) / P,
        "primaire_stabilisant": 100 * (e["i_CB"] * e["D_c"] / n - e["gam"] * e["D_c"]) / P,
        "interets_bruts": 100 * e["interets"] / P, "interets_nets": 100 * (e["interets"] - e["Pi_CB"]) / P,
        "Em": 100 * e["Em"] / P, "dette_brute_affichee": 100 * e["B"] / A * facteur_restitue(n, x_stock),
        "marge_E1": 1 - e["Gam"] * (e["G"] / e["PB"]) / par.nu_G,
        "hausse_admissible": 100 * (par.nu_G / (e["Gam"] * e["G"] / e["PB"]) - 1),
        "borne_nu_G": HAUSSE_J_NU * e["Gam"] * e["G"] / e["PB"],
        "retour_approche": e["Gam"] * (e["G"] / e["PB"]) / (1 - 0.05 * e["G"] / e["PB"]),
        "nu_G_min": nu_min, "nu_G_J": nu_J, "marge_J_nu": 1 - HAUSSE_J_NU * e["Gam"] * (e["G"] / e["PB"]) / par.nu_G,
        "a": e["a"], "x": (e["G"] + e["Tr"]) / P, "nu_G_max_D2": 1 / e["a"] if e["a"] > 0 else math.inf,
        "multiplicateur_nu": par.nu_G * (1 - e["a"]) / (1 - par.nu_G * e["a"]),
        "D_H_sur_T_H": _rapport(e["D_H"], e["T_H"]),
        "plafond_E6": (e["M_G"] + e["T_H"] - e["interets"] - e["G"]) / e["PB"],
        "caisse_DH4": caisse["DH4"], "caisse_DH5": caisse["DH5"], "caisse_DH6": caisse["DH6"],
        "caisse_DF4": caisse["DF4"], "nu_F_min": caisse["nu_F_min"],
        "caisse_MG5": caisse["MG5"], "caisse_MG6": caisse["MG6"], "caisse_MG7": caisse["MG7"],
        "caisse_MG8b": caisse["MG8b"], "Div_F_marge": e["Div_F"] / (e["p"] * e["v"]),
        "D1": e["D1"], "D2": e["D2"], "A_autonome": e["theta_G"],
    }
    return v


GRANDEURS: tuple[Grandeur, ...] = (
    # Cadre
    Grandeur("Gamma", "Γ̄ = [(1 + g)(1 + π̄)]^{1/n_a}", "sans dimension", "—", "pas", "sec:cadre-calendrier"),
    Grandeur("gamma_pas", "γ̄ = Γ̄ − 1, croissance nominale par pas", "% par pas", "—", "pas", "sec:cadre-calendrier"),
    Grandeur("pi_pas", "π^pas = (1 + π*)^{1/n_a} − 1", "% par pas", "—", "pas", "sec:cadre-calendrier"),
    Grandeur("glissement", "π̄ = P_t/P_{t−n_a} − 1, glissement sur le registre stationnaire", "% par an", "—",
             "n_a tours", "sec:cadre-calendrier"),
    Grandeur("facteur_stock", "facteur du ratio restitué d'un stock en u.m. (x = (1 + g)(1 + π̄) − 1)",
             "sans dimension", "—", "12 tours (n_a = 12 seulement)", "sec:cadre-calendrier"),
    Grandeur("facteur_volume", "facteur du ratio restitué d'un ratio en volume (x = g)", "sans dimension", "—",
             "12 tours (n_a = 12 seulement)", "sec:cadre-calendrier"),
    # Taux
    Grandeur("i_CB", "taux directeur i_CB = (1 + r̄)(1 + π*) − 1 = i^règle", "% par an", "—", "le tour",
             "sec:banque_centrale-stationnaire"),
    Grandeur("i_L", "taux des crédits i_CB + ϖ_L", "% par an", "—", "ouverture", "sec:banque-stationnaire"),
    Grandeur("i_D", "taux des dépôts i_CB − ϖ_D", "% par an", "—", "ouverture", "sec:banque-stationnaire"),
    Grandeur("i_ref", "taux de référence de E4, (1 + r̄)(1 + π*) − 1", "% par an", "—", "le tour",
             "sec:finances_publiques-impots"),
    Grandeur("rbar", "r̄, taux réel neutre (Fisher sur la cible), paramètre en lecture (e)", "% par an", "—",
             "état stationnaire", "sec:banque_centrale-stationnaire"),
    Grandeur("r_restitue", "r = i_CB − π̄, taux réel restitué", "% par an", "—", "le tour", "sec:cadre-calendrier"),
    Grandeur("rho_L", "ϱ_L = (1 + i_L)/(1 + π*) − 1, taux réel du crédit anticipé (= ϱ̄_L)", "% par an", "—",
             "état stationnaire", "sec:investissement-taux"),
    Grandeur("r_exact", "taux réel exact n_a ln(1 + i_CB/n_a) − ln(1 + π̄) (M8)", "% par an", "—", "état stationnaire",
             "fiche 8, critère 13 (b)"),
    Grandeur("r_HS", "taux réel « Haig-Simons » i_CB − n_a π^pas (M8, forme sur i_CB déclarée)", "% par an", "—",
             "état stationnaire", "décision du 05/10/2026, point 6"),
    Grandeur("rendement_reel_depots", "i_D − π̄", "point par an", "—", "le tour", "sec:banque-stationnaire"),
    Grandeur("T_cou", "couverture des intérêts T^cou", "% du PIB", "PIB du pas", PAS, "sec:finances_publiques-impots"),
    # Production
    Grandeur("y_sur_v", "production rapportée aux ventes y/v", "sans dimension", "ventes du pas", "pas",
             "sec:production-stationnaire"),
    Grandeur("IN_sur_v", "stock d'ouverture en volume rapporté aux ventes du pas, n_a σ", "pas de ventes",
             "ventes du pas", OUV, "sec:production-stationnaire"),
    Grandeur("rho_IN", "ρ̄_IN = IN/(UC IN^vol)", "sans dimension", "UC · IN^vol", OUV, "sec:production-stationnaire"),
    Grandeur("dIN_sur_IN", "ΔIN/IN", "% par pas", "IN d'ouverture", "pas", "sec:production-stationnaire"),
    Grandeur("tu", "taux d'utilisation y/y^cap = t̄u e^{ζΔϱ}", "fraction de la capacité normale", "y^cap", "pas",
             "sec:investissement-stationnaire"),
    Grandeur("marge_disponibilite", "marge de la disponibilité (IN^vol + y − v)/v", "sans dimension", "ventes du pas",
             "pas", "sec:production-ventes"),
    Grandeur("K_vol_sur_y", "K/Y (a) en volume : K^vol/(n_a y)", "années de production", "n_a y", OUV,
             "sec:investissement-stationnaire ; fiche 2, § 3.N-5"),
    Grandeur("K_courant", "K/Y (b) au prix courant : p K^vol/(n_a PIB)", "années de PIB", "n_a PIB", OUV,
             "sec:investissement-stationnaire"),
    Grandeur("K_comptable", "K/Y (c) comptable : K/(n_a PIB)", "années de PIB", "n_a PIB", OUV,
             "sec:investissement-stationnaire"),
    Grandeur("rho_K", "ρ̄_K = K/(p K^vol)", "sans dimension", "p K^vol", OUV, "sec:production-capital"),
    Grandeur("ecart_valorisation", "écart de valorisation ρ̄_K − 1", "%", "p K^vol", OUV, "sec:investissement-lignes"),
    Grandeur("ecart_valorisation_cloture", "capital de clôture au prix du tour, ρ̄_K Π^pas − 1", "%",
             "p_t K^vol_{t+1}", "clôture", "sec:investissement-lignes"),
    # Travail, prix
    Grandeur("U", "chômage Ū = U^eq (marge de N ≤ N^pa)", "fraction de la population active", "N^pa", "pas",
             "sec:travail-stationnaire"),
    Grandeur("omega", "salaire relatif W/(p pr) = ω̄", "sans dimension", "p pr", "pas", "sec:travail-stationnaire"),
    Grandeur("hausse_salaire_pas", "hausse du salaire nominal [(1 + g_pr)(1 + π̄)]^{1/n_a} − 1 (T3 : résidu en P2)",
             "% par pas", "W_{t−1}", "pas", "sec:travail-stationnaire"),
    Grandeur("hausse_salaire_an", "glissement annuel du salaire (1 + x)^{n_a} − 1", "% par an", "W_{t−n_a}",
             "n_a tours", "sec:travail-stationnaire"),
    Grandeur("part_salariale", "part salariale ΣWB/Σ(p v + ΔIN)", "sans dimension", "valeur ajoutée",
             "12 tours (= rapport du pas)", "sec:travail-stationnaire"),
    Grandeur("ecart_part_salariale", "ω̄ − part salariale", "point", "valeur ajoutée", "12 tours",
             "sec:travail-stationnaire"),
    Grandeur("xi", "tension sur les stocks ξ̄ = 1 − IN^vol/(n_a σ v^e) (P1 : résidu en P2)", "sans dimension",
             "IN^vol*", "pas", "sec:prix-stationnaire"),
    Grandeur("mu_tilde", "marge d'ouverture μ̃ = ln(p/UC) = ln(1 + μ̄) (règle P2 : résidu en P2)", "sans dimension",
             "—", "pas", "sec:prix-stationnaire"),
    Grandeur("hausse_prix_pas", "hausse du prix par pas p_t/P_{t−1} − 1 sur le registre (P3 : résidu en P2)",
             "% par pas", "P_{t−1}", "pas", "sec:prix-stationnaire"),
    # Ménages
    Grandeur("richesse_HS", "V_H/[n_a (YD − π^pas V_H)] = ν_H", "années de revenu de Haig-Simons",
             "n_a (YD − π^pas V_H)", OUV, "sec:menages-stationnaire"),
    Grandeur("richesse_YD", "V_H/(n_a YD)", "années de revenu disponible", "n_a YD", OUV, "sec:menages-stationnaire"),
    Grandeur("epargne", "taux d'épargne nominal 1 − C/YD", "% du revenu disponible", "YD", PAS,
             "sec:menages-stationnaire"),
    Grandeur("epargne_maintien", "dont maintien face à l'inflation π^pas V_H/YD", "point de YD", "YD", PAS,
             "sec:menages-stationnaire"),
    Grandeur("epargne_reelle", "dont épargne réelle (γ̄ − π^pas) V_H/YD", "point de YD", "YD", PAS,
             "sec:menages-stationnaire"),
    Grandeur("epargne_residu", "résidu de la décomposition |1 − C/YD − γ̄ V_H/YD|", "sans dimension", "YD", PAS,
             "sec:menages-conditions (≤ 1e−12)"),
    Grandeur("C_sur_YD", "C/YD", "sans dimension", "YD", PAS, "sec:menages-stationnaire"),
    Grandeur("epargne_visee", "taux d'épargne visé 1 − C/(YD − π^pas V_H)", "% du revenu de Haig-Simons",
             "YD − π^pas V_H", PAS, "sec:menages-stationnaire"),
    Grandeur("marge_plafond_mois", "marge du plafond du budget D_H/C", "mois de consommation (12/n_a pas)", "C du pas",
             OUV, "sec:menages-plan"),
    Grandeur("plancher_budget", "plancher du budget : C^règle/YD (> 0)", "sans dimension", "YD", PAS,
             "sec:menages-plan"),
    Grandeur("V_H_sur_YD", "V_H rapporté au revenu disponible du pas, YD_0", "pas de revenu", "YD du pas", OUV,
             "sec:menages-stationnaire"),
    Grandeur("impot_inflation", "impôt d'inflation net des déposants [n_a π^pas − i_D] V_H/(n_a YD)",
             "% du revenu disponible", "YD", PAS, "sec:banque-stationnaire"),
    # Investissement
    Grandeur("ti", "part d'investissement visée ti", "fraction de la production attendue", "y", "pas",
             "sec:investissement-stationnaire"),
    Grandeur("I_sur_PIB", "taux d'investissement I/PIB", "% du PIB", "PIB du pas", PAS,
             "sec:investissement-stationnaire"),
    Grandeur("L_sur_K", "levier L/K = lv*", "fraction du capital comptable", "K", OUV,
             "sec:investissement-stationnaire"),
    Grandeur("D_F_sur_ventes", "dépôts D_F/(n_a p v^e) = ν_F", "années de ventes", "n_a p v^e", OUV,
             "sec:investissement-stationnaire"),
    Grandeur("credits", "crédits l = L/(n_a PIB)", "années de PIB", "n_a PIB", OUV, "sec:investissement-stationnaire"),
    Grandeur("credits_nets", "crédits nets des dépôts (L − D_F)/(n_a PIB)", "années de PIB", "n_a PIB", OUV,
             "sec:investissement-stationnaire"),
    Grandeur("depots_F", "dépôts des entreprises d_F", "années de PIB", "n_a PIB", OUV,
             "sec:investissement-stationnaire"),
    Grandeur("V_F", "valeur nette des entreprises V_F/(n_a PIB)", "années de PIB", "n_a PIB", OUV,
             "sec:investissement-stationnaire"),
    Grandeur("FU_sur_V_F", "profits non distribués FU/V_F", "% par pas", "V_F", "pas",
             "sec:investissement-stationnaire"),
    Grandeur("distribution", "taux de distribution Div_F/(Div_F + FU) (bande [0,2 ; 0,9] de #55, publiée sans refus)",
             "sans dimension", "résultat net", PAS, "sec:investissement-stationnaire"),
    Grandeur("Div_F_sur_ventes", "dividendes rapportés aux ventes Div_F/(p v) (marge de Div_F ≥ 0)", "% des ventes",
             "p v", PAS, "sec:investissement-stationnaire"),
    Grandeur("levier_courant", "levier au prix courant lv* ρ̄_K", "fraction de p K^vol", "p K^vol", OUV,
             "sec:investissement-stationnaire"),
    # Banque
    Grandeur("e_Bk", "fonds propres de la banque e_Bk = ϑ l", "années de PIB", "n_a PIB", OUV,
             "sec:banque-stationnaire"),
    Grandeur("E_sur_L", "E^Bk/L = ϑ", "fraction", "L", OUV, "sec:banque-stationnaire"),
    Grandeur("masse_monetaire", "masse monétaire M = v_H + d_F", "années de PIB", "n_a PIB", OUV,
             "sec:banque-stationnaire"),
    Grandeur("reserves", "réserves Res/(n_a PIB)", "années de PIB", "n_a PIB", OUV, "sec:banque-stationnaire"),
    Grandeur("refinancement", "refinancement l^CB = L^CB/(n_a PIB) = M^G_0/(n_a PIB)", "années de PIB", "n_a PIB", OUV,
             "sec:banque-stationnaire (#83)"),
    Grandeur("titres_Bk", "titres de la banque b_Bk = B_Bk/(n_a PIB)", "années de PIB", "n_a PIB", OUV,
             "sec:banque-stationnaire (#83)"),
    Grandeur("Pi_Bk", "résultat de la banque Π^Bk/PIB", "% du PIB", "PIB du pas", PAS, "sec:banque-stationnaire"),
    Grandeur("roe", "rendement des fonds propres n_a Π^Bk/E^Bk, brut, nominal, sans charges d'exploitation, pertes "
             "ni impôt (Π^Bk ne contient que les marges d'intérêt ; décision M34)", "% par an", "E^Bk d'ouverture", PAS,
             "sec:banque-stationnaire"),
    Grandeur("part_distribuee_Bk", "part distribuée Div_Bk/Π^Bk (marge de Div_Bk ≥ 0)", "sans dimension", "Π^Bk", PAS,
             "sec:banque-stationnaire"),
    Grandeur("existence_Bk", "marge de la condition d'existence ϑ i_CB + ϖ_L + ϖ_D D/L − ϑ n_a(Γ̄ − 1)", "par an", "—",
             "état stationnaire", "sec:banque-stationnaire"),
    Grandeur("part_titres", "part des titres dans l'actif b_Bk/(l + b_Bk + res)", "fraction", "actif d'ouverture", OUV,
             "sec:banque-stationnaire (#83)"),
    Grandeur("marge_nette", "marge nette d'intérêt : ratio Π^Bk/actif, n_a Π^Bk/(L + B_Bk + Res) (décision M34)",
             "% par an", "actif d'ouverture", PAS,
             "sec:banque-stationnaire (#83)"),
    Grandeur("domar_E_Bk", "déficit de Domar dû aux fonds propres n_a(Γ̄ − 1) e_Bk", "% du PIB", "PIB annuel",
             "état stationnaire", "sec:banque-conditions"),
    Grandeur("couplage", "couplage ∂Div_Bk/∂I^plan = −ϑ lv*", "sans dimension", "—", "—", "sec:banque-conditions"),
    Grandeur("canal_rentier", "hausse du revenu disponible par point de taux, 0,01 c/(YD/PIB)",
             "% du revenu disponible", "YD", "équilibre partiel", "sec:banque-stationnaire"),
    Grandeur("part_v_H", "part des intérêts des dépôts v_H/c", "%", "c", "équilibre partiel",
             "sec:banque-stationnaire"),
    Grandeur("part_entreprises", "part des dividendes des entreprises −(l − d_F)/c", "%", "c", "équilibre partiel",
             "sec:banque-stationnaire"),
    Grandeur("part_E_Bk", "part du dividende de la banque e_Bk/c", "%", "c", "équilibre partiel",
             "sec:banque-stationnaire"),
    Grandeur("saut_C29", "saut d'un tour du résultat, par point : 0,01 c/(Π^Bk/PIB)", "% du résultat", "Π^Bk",
             "tour n", "sec:banque-conditions (C29)"),
    Grandeur("saut_C29_suite", "ensuite : 0,01 e_Bk/(Π^Bk/PIB)", "% du résultat", "Π^Bk", "tours suivants",
             "sec:banque-conditions (C29)"),
    Grandeur("d2", "(d2) rendement des fonds propres sur 12 tours : [0,01 c/e_Bk + 11 × 0,01]/12", "point", "—",
             "12 tours", "sec:banque-conditions"),
    # Banque centrale
    Grandeur("pi_e", "anticipation π^e (BC3 au point fixe)", "% par an", "—", OUV, "sec:banque_centrale-stationnaire"),
    Grandeur("r_hat", "taux neutre retenu r̂* (BC2 au point fixe)", "% par an", "—", OUV,
             "sec:banque_centrale-stationnaire"),
    Grandeur("Pi_CB", "résultat de la banque centrale Π^CB/PIB = i_CB (m + e_CB)", "% du PIB", "PIB du pas", PAS,
             "sec:banque_centrale-stationnaire"),
    Grandeur("monnaie_centrale", "monnaie centrale H = Res", "années de PIB", "n_a PIB", OUV,
             "sec:banque_centrale-stationnaire"),
    Grandeur("E_CB", "fonds propres de la banque centrale", "années de PIB", "n_a PIB", OUV,
             "sec:banque_centrale-stationnaire"),
    Grandeur("titres_CB", "titres de la banque centrale B_CB/(n_a PIB) (à sa borne par θ_CB = 0)", "années de PIB",
             "n_a PIB", OUV, "sec:banque_centrale-stationnaire"),
    # État
    Grandeur("theta_G", "part de la dépense publique θ_G = G/(p y^pot), résolue (#44, lecture (e))",
             "fraction de la production potentielle", "p y^pot", "pas", "sec:finances_publiques-stationnaire"),
    Grandeur("A_autonome", "part de la demande autonome dans la production, A = θ_G (> 0)",
             "fraction de la production", "y", "pas", "part de `macro`, § 6"),
    Grandeur("G_sur_PIB", "dépense publique G/PIB", "% du PIB", "PIB du pas", PAS,
             "sec:finances_publiques-stationnaire"),
    Grandeur("T_H_sur_PIB", "impôt des ménages T_H/PIB", "% du PIB", "PIB du pas", PAS,
             "sec:finances_publiques-stationnaire"),
    Grandeur("G_sur_PB", "G/PB", "sans dimension", "paiements bruts du pas", "pas", "sec:finances_publiques-depense"),
    Grandeur("Y_HS", "assiette Y^HS/PIB", "fraction du PIB", "PIB du pas", PAS, "sec:finances_publiques-stationnaire"),
    Grandeur("YD_HS", "revenu disponible de Haig-Simons YD^HS/PIB = YD/PIB − π^pas V_H/PIB", "fraction du PIB",
             "PIB du pas", PAS, "sec:finances_publiques-stationnaire"),
    Grandeur("taux_apparent", "taux apparent de l'impôt T_H/Y^HS (= barème τ_H sous T^cou = 0)", "% de l'assiette",
             "Y^HS", PAS, "sec:finances_publiques-restitution"),
    Grandeur("dette_consolidee", "dette consolidée (B − M^G − E^CB)/(n_a PIB)", "années de PIB", "n_a PIB", OUV,
             "sec:finances_publiques-stationnaire (C42)"),
    Grandeur("decomp_v_H", "décomposition : V_H/(n_a PIB)", "années de PIB", "n_a PIB", OUV,
             "sec:finances_publiques-stationnaire (C42)"),
    Grandeur("decomp_entreprises", "décomposition : −(L − D_F)/(n_a PIB)", "années de PIB", "n_a PIB", OUV,
             "sec:finances_publiques-stationnaire (C42)"),
    Grandeur("decomp_E_Bk", "décomposition : E^Bk/(n_a PIB)", "années de PIB", "n_a PIB", OUV,
             "sec:finances_publiques-stationnaire (C42)"),
    Grandeur("dette_brute", "dette brute B/(n_a PIB), à ν_G du point", "années de PIB", "n_a PIB", OUV,
             "sec:finances_publiques-stationnaire"),
    Grandeur("encaisse", "encaisse M^G/(n_a PIB) = m(ν_G)", "années de PIB", "n_a PIB", OUV,
             "sec:finances_publiques-emission"),
    Grandeur("domar_facteur", "n_a(Γ̄ − 1)", "% par an", "—", "annuelle", "sec:finances_publiques-stationnaire"),
    Grandeur("deficit_i", "déficit de Domar (i) : n_a(Γ̄ − 1) × dette consolidée", "% du PIB", "PIB annuel", PAS,
             "sec:finances_publiques-stationnaire"),
    Grandeur("deficit_ii", "déficit (ii) par les flux (G + Tr + i_CB B/n_a − T_H − T_F − Π^CB)/PIB", "% du PIB",
             "PIB du pas", PAS, "sec:finances_publiques-stationnaire"),
    Grandeur("primaire", "solde primaire (T_H + T_F − G − Tr)/PIB", "% du PIB", "PIB du pas", PAS,
             "sec:finances_publiques-stationnaire"),
    Grandeur("primaire_stabilisant", "solde primaire stabilisant (i_CB/n_a − γ̄)(B − M^G)/PIB ; écart au réalisé nul",
             "% du PIB", "PIB du pas", PAS, "sec:finances_publiques-restitution"),
    Grandeur("interets_bruts", "charge d'intérêts brute i_CB B/(n_a PIB)", "% du PIB", "PIB du pas", PAS,
             "sec:finances_publiques-stationnaire"),
    Grandeur("interets_nets", "charge d'intérêts nette du résultat de la banque centrale", "% du PIB", "PIB du pas",
             PAS, "sec:finances_publiques-stationnaire"),
    Grandeur("Em", "besoin d'émission Em/PIB = γ̄ B/PIB : signe de γ̄, rachat net si γ̄ < 0", "% du PIB", "PIB du pas",
             PAS,
             "sec:finances_publiques-emission"),
    Grandeur("dette_brute_affichee", "dette brute affichée : dette brute × facteur d'un stock en u.m.", "% du PIB",
             "Σ des 12 PIB", "12 tours (n_a = 12 seulement)", "sec:finances_publiques-restitution"),
    Grandeur("D_H_sur_T_H", "dépôts des ménages rapportés à l'impôt du pas", "pas d'impôt", "T_H du pas", OUV,
             "sec:finances_publiques-caisse"),
    Grandeur("plafond_E6", "marge du plafond de E6 (M^G + T_H − i_CB B/n_a − G^plan)/PB", "sans dimension", "PB",
             "phase 2", "sec:finances_publiques-transferts"),
    # ν_G : forme fermée et propriété J-ν
    Grandeur("marge_E1", "marge du plafond de E1 : 1 − Γ̄ (G/PB)/ν_G", "fraction de l'encaisse d'ouverture", "M^G",
             "phase 2", "sec:finances_publiques-depense"),
    Grandeur("hausse_admissible", "hausse de dépense admissible en un tour ν_G/(Γ̄ G/PB) − 1", "%", "G du pas",
             "un tour", "sec:finances_publiques-depense ; propriété J-ν"),
    Grandeur("borne_nu_G", "borne 1,10 Γ̄ G/PB(ν_G du point)", "sans dimension", "—", "un tour",
             "sec:finances_publiques-emission"),
    Grandeur("retour_approche", "retour après une baisse de 5 % : Γ̄ (G/PB)/(1 − 0,05 G/PB), calcul approché",
             "sans dimension", "—", "—", "sec:finances_publiques-emission"),
    Grandeur("nu_G_min", "ν_G,min exact : 1,10 Γ̄ G/(X + 1,10 Γ̄ G a), X = G + Tr + i_CB (B − M^G)/n_a",
             "sans dimension", "—", "un tour", "part de `macro`, § 4"),
    Grandeur("nu_G_J", "ν_G minimal pour m_ν ≥ 0,03 : 1,10 Γ̄ G/(0,97 X + 1,10 Γ̄ G a)", "sans dimension", "—",
             "un tour", "propriété J-ν (décision du 05/10/2026, point 7)"),
    Grandeur("marge_J_nu", "marge J-ν m_ν = 1 − 1,10 Γ̄ (G/PB)/ν_G, à ν_G du point", "sans dimension", "—", "un tour",
             "propriété J-ν"),
    Grandeur("a", "a = i_CB/(Γ̄ n_a), coefficient de la forme fermée en ν_G", "sans dimension", "—", "—",
             "part de `monnaie`, § 2"),
    Grandeur("x", "x = (G + Tr)/PIB, coefficient de la forme fermée en ν_G", "fraction du PIB", "PIB du pas", PAS,
             "part de `monnaie`, § 2"),
    Grandeur("nu_G_max_D2", "ν_G maximal de D2 : 1/a (inf si a ≤ 0 : D2 sans borne)", "sans dimension", "—", "—", "part de `macro`, § 4 (D2)"),
    Grandeur("multiplicateur_nu", "effet de ν_G sur le refinancement ν_G(1 − a)/(1 − ν_G a)", "sans dimension",
             "refinancement à ν_G = 1", "—", "sec:banque-stationnaire (K22)"),
    # Caisse, domaine
    Grandeur("caisse_DH4", "D_H en fin de phase 4 / D_H d'ouverture", "sans dimension", "D_H d'ouverture", "phase 4",
             "sec:cadre-caisse"),
    Grandeur("caisse_DH5", "D_H en fin de phase 5 / D_H d'ouverture", "sans dimension", "D_H d'ouverture", "phase 5",
             "sec:cadre-caisse"),
    Grandeur("caisse_DH6", "D_H en fin de phase 6 / D_H d'ouverture", "sans dimension", "D_H d'ouverture", "phase 6",
             "sec:cadre-caisse"),
    Grandeur("caisse_DF4", "q1 : D_F en fin de phase 4 (D_F + ΔL − WB)/D_F", "sans dimension", "D_F d'ouverture",
             "phase 4", "sec:cadre-caisse (P24)"),
    Grandeur("nu_F_min", "q1 : ν_F,min = (WB − ΔL)/(n_a p v)", "années de ventes", "n_a p v", "phase 4",
             "sec:cadre-caisse (P24)"),
    Grandeur("caisse_MG5", "M^G en fin de phase 5 / M^G (= marge de E1)", "sans dimension", "M^G d'ouverture",
             "phase 5", "sec:cadre-caisse"),
    Grandeur("caisse_MG6", "M^G en fin de phase 6 / M^G", "sans dimension", "M^G d'ouverture", "phase 6",
             "sec:cadre-caisse"),
    Grandeur("caisse_MG7", "M^G en fin de phase 7 (M^G* − Π^CB) / M^G", "sans dimension", "M^G d'ouverture", "phase 7",
             "sec:cadre-caisse"),
    Grandeur("caisse_MG8b", "M^G en fin de sous-phase 8 (b) / M^G = Γ̄", "sans dimension", "M^G d'ouverture",
             "phase 8 (b)", "sec:cadre-caisse"),
    Grandeur("Div_F_marge", "marge de Div_F ≥ 0 : Div_F/(p v)", "fraction des ventes", "p v", PAS,
             "sec:investissement-financement"),
    Grandeur("D1", "D1 : 1 − ν_H n_a (1 − τ_H) c, dénominateur de la richesse", "sans dimension", "—", "—",
             "part de `macro`, § 4"),
    Grandeur("D2", "D2 : 1 − ν_G a, dénominateur de l'encaisse", "sans dimension", "—", "—", "part de `macro`, § 4"),
)


# --- Fermeture (#44) et mesure de #80 ----------------------------------------------


def sensibilite_fermeture(par: Parametres, h: float = 1e-4) -> dict[str, float]:
    """dθ_G/dr̄ en lecture (e) (P8 de `macro`, M14 de `monnaie`), par différence centrée de pas h.

    r̄ varie comme paramètre : le taux de référence de E4 et la norme ϱ̄_L le
    suivent (état initial résolu à chaque r̄). L'erreur déclarée est l'écart
    de Richardson |D(h) − D(h/2)| × 4/3.
    """
    def theta(r, quoi):
        return etat_stationnaire(replace(par, rbar=r))[quoi]

    def derivee(pas, quoi):
        return (theta(par.rbar + pas, quoi) - theta(par.rbar - pas, quoi)) / (2 * pas)

    def g_pib(r):
        e = etat_stationnaire(replace(par, rbar=r))
        return e["G"] / e["PIB"]

    d_h = derivee(h, "theta_G")
    d_h2 = derivee(h / 2, "theta_G")
    dG = (g_pib(par.rbar + h) - g_pib(par.rbar - h)) / (2 * h)
    return {
        "dtheta_G_dr": d_h,  # fraction de y par unité de r̄ = % de la production par point de r̄
        "erreur": abs(d_h - d_h2) * 4 / 3,
        "dG_PIB_dr": dG,
        "points_r_par_point_PIB": 1 / dG if dG != 0 else math.inf,
        "pas": h,
    }


def _theta_alpha(par: Parametres, r: float, rho_bar: float) -> float:
    """θ_G de l'état stationnaire à r̄ = r, norme ϱ̄_L fixée, sans contrôle de domaine (balayage)."""
    try:
        return etat_stationnaire(par, r_neutre=r, rho_bar_L=rho_bar, controler=False)["theta_G"]
    except (ZeroDivisionError, OverflowError):
        return math.nan


def resoudre_alpha(par: Parametres, theta_cible: float, rho_bar: float) -> dict[str, object]:
    """Racines de F(r̄) = θ_G(r̄ ; π*, n_a) − θ_G* (part de `monnaie`, § 4), par `racines_balayage`."""
    def F(r):
        return _theta_alpha(par, r, rho_bar) - theta_cible

    return racines_balayage(F)


def racine_unique(res: dict[str, object], contexte: str) -> dict[str, float]:
    """Rend la racine du domaine C51 ; refus (`HorsDomaine`) s'il n'y en a pas exactement une, ou s'il y a un pôle."""
    if len(res["dans_domaine"]) != 1 or res["poles"]:
        raise HorsDomaine(f"lecture (α), {contexte} : {len(res['dans_domaine'])} racine(s) dans (−5 % ; 100 %] au "
                          f"lieu d'une ; racines {[x['r'] for x in res['racines']]!r} ; pôles {res['poles']!r}")
    return res["dans_domaine"][0]


def racines_balayage(F) -> dict[str, object]:
    """Racines et pôles d'une fonction F de r̄ (fraction par an) sur [−60 % ; 100 %].

    Balayage au pas de 0,1 point (1 601 points), puis bissection de chaque
    intervalle de changement de signe jusqu'à une largeur de 1e−14, au plus
    200 itérations (au-delà : échec explicite). Un intervalle dont la limite
    garde |F| > tol_F est un pôle. Une évaluation qui échoue (division par
    zéro, dépassement) vaut NaN et n'ouvre aucun intervalle.
    """
    def F_(r):
        try:
            return F(r)
        except (ZeroDivisionError, OverflowError):
            return math.nan

    grille = [-0.60 + k * 0.001 for k in range(1601)]
    valeurs_F = [F_(r) for r in grille]
    racines: list[dict[str, float]] = []
    poles: list[float] = []
    for r, f in zip(grille, valeurs_F, strict=True):
        if f == 0.0:
            racines.append({"r": r, "F": 0.0, "iterations": 0})
    for k in range(len(grille) - 1):
        fa, fb = valeurs_F[k], valeurs_F[k + 1]
        if math.isnan(fa) or math.isnan(fb) or fa == 0.0 or fb == 0.0 or fa * fb > 0:
            continue
        a, b = grille[k], grille[k + 1]
        iterations = 0
        while b - a > LARGEUR_BISSECTION:
            if iterations >= ITERATIONS_MAX:
                raise HorsDomaine(f"bissection non convergée en {ITERATIONS_MAX} itérations sur [{a!r} ; {b!r}]")
            m = (a + b) / 2
            if m in (a, b):  # précision de la machine atteinte
                break
            fm = F_(m)
            iterations += 1
            if math.isnan(fm):
                break
            if (fa < 0) == (fm < 0):
                a, fa = m, fm
            else:
                b = m
        r_k = (a + b) / 2
        f_k = F_(r_k)
        if abs(f_k) <= TOL_F:
            racines.append({"r": r_k, "F": f_k, "iterations": iterations})
        else:
            poles.append(r_k)
    racines.sort(key=lambda x: x["r"])
    dans_domaine = [x for x in racines if -0.05 < x["r"] <= 1.00]
    return {"racines": racines, "poles": poles, "dans_domaine": dans_domaine}


def mesure_alpha(par: Parametres, pi: float, n_a: int, lecture_ref: str = "A") -> dict[str, object]:
    """r̄_α(π*) en lecture (α) : θ_G et ϱ̄_L de l'état résolu à π* = 2 %, r̄ = 1 %, au même n_a.

    `lecture_ref` : « A » (retenue) — E4 garde le paramètre r̄ = 1 %. La
    lecture B (i^ref suit r̄_α) n'est pas dans le script : elle se mesure une
    fois, hors du script, si A ne reproduit pas les valeurs publiées
    (décision du 05/10/2026, point 5).
    """
    if lecture_ref != "A":
        raise HorsDomaine("seule la lecture A de i^ref est mise en œuvre (décision du 05/10/2026, point 5)")
    base = replace(par, pi_cible=0.02, n_a=n_a, rbar=0.01)
    e0 = etat_stationnaire(base)
    point = replace(base, pi_cible=pi)
    res = resoudre_alpha(point, e0["theta_G"], e0["rho_L"])
    racine = racine_unique(res, f"π* = {pi!r}, n_a = {n_a}")
    r_a = racine["r"]
    e = etat_stationnaire(point, r_neutre=r_a, rho_bar_L=e0["rho_L"])
    return {
        "pi": pi, "n_a": n_a, "r_alpha": r_a, "F": racine["F"], "iterations": racine["iterations"],
        "racines": [x["r"] for x in res["racines"]], "poles": res["poles"],
        "theta_G": e["theta_G"], "d_rho": e["d_rho"], "allocations": allocations_alpha(e, n_a),
    }


# Allocations de la lecture (α), liste L2 (critère 13 (a) de la fiche 8 ; décision du mainteneur du 05/10/2026) :
# verdict sous le seuil de 0,1 point, invariance exacte (1e−12 relatif), mesures publiées sans verdict.
ALLOCATIONS_VERDICT = ("C/Y_o", "ti", "tu")
ALLOCATIONS_INVARIANTES = ("V_H/(n_a YD^HS)",)
ALLOCATIONS_MESUREES = (
    "I^vol/y", "K^vol/(n_a y)", "C/PIB", "G/PIB", "I/PIB", "ΔIN/PIB", "ΔIN/PIB volume", "ΔIN/PIB prix",
    "C/(p v)", "G/(p v)", "I/(p v)", "ΔIN/(p v)", "T^cou/PIB",
)
TOL_INVARIANCE = 1e-12  # invariance exacte, relative
# Sensibilité à ζ (décision de `macro`, complément de #84) : le verdict reste jugé à ζ du paramètre (8, M34) ; l'étendue
# des allocations de la liste L2 est publiée en mesure sur ζ ∈ {4 ; 8}, et à ζ = 2 en illustration, sans verdict. Les
# allocations qui en dépendent (par r̄_α) sont mesurées, non supposées. `ZETA_PLAGE` n'est pas une plage de la table :
# la table T1 retient le seul ζ = 8 (M34, #55) ; (4 ; 8) réunit la valeur de la calibration indicative et celle de T1.
# La sortie le dit : « calibration indicative ; table T1 » (libellé visé par `macro`, #172).
ZETA_PLAGE = (4.0, 8.0)
ZETA_ILLUSTRATION = 2.0

GRANDEURS_ALPHA: tuple[Grandeur, ...] = (
    Grandeur("r_alpha", "r̄_α(π*), racine de θ_G(r̄ ; π*, n_a) = θ_G* ; lecture A de i^ref (E4 garde r̄ = 1 %), "
             "norme ϱ̄_L de S2 fixée à sa valeur de l'état résolu à π* = 2 %, r̄ = 1 %, au même n_a (décision du "
             "mainteneur du 05/10/2026, #80)", "% par an", "—", "état stationnaire",
             "sec:banque_centrale-conditions ; fiche 9 § 3.Q"),
    Grandeur("C/Y_o", "C/Y_o, Y_o = YD − i_D V_H/n_a (verdict)", "sans dimension", "Y_o du pas", PAS,
             "fiche 8, critère 13 (a), liste L2"),
    Grandeur("ti", "part d'investissement visée ti (verdict ; dépend de η_r)", "fraction de la production attendue",
             "y", "pas", "fiche 8, critère 13 (a), liste L2"),
    Grandeur("tu", "taux d'utilisation tu = t̄u e^{ζΔϱ} (verdict)", "fraction de la capacité normale", "y^cap", "pas",
             "fiche 8, critère 13 (a), liste L2"),
    Grandeur("V_H/(n_a YD^HS)", "richesse sur revenu de Haig-Simons (invariance exacte, = ν_H)",
             "années de revenu de Haig-Simons", "n_a YD^HS", OUV, "fiche 8, critère 13 (a), liste L2"),
    Grandeur("I^vol/y", "part d'investissement réalisée I^vol/y (mesure, à côté de ti)", "fraction de la production",
             "y", "pas", "décision du 05/10/2026"),
    Grandeur("K^vol/(n_a y)", "capital en volume K^vol/(n_a y) = κ/tu (mesure)", "années de production", "n_a y", OUV,
             "fiche 8, critère 13 (a), liste L2"),
    Grandeur("C/PIB", "C/PIB (mesure)", "fraction du PIB", "PIB du pas", PAS, "liste L2"),
    Grandeur("G/PIB", "G/PIB (mesure)", "fraction du PIB", "PIB du pas", PAS, "liste L2"),
    Grandeur("I/PIB", "I/PIB (mesure)", "fraction du PIB", "PIB du pas", PAS, "liste L2"),
    Grandeur("ΔIN/PIB", "ΔIN/PIB = γ̄ IN/PIB (mesure)", "fraction du PIB", "PIB du pas", PAS, "liste L2"),
    Grandeur("ΔIN/PIB volume", "part en volume de ΔIN : (G_r − 1) IN/PIB", "fraction du PIB", "PIB du pas", PAS,
             "liste L2, décomposition de ΔIN"),
    Grandeur("ΔIN/PIB prix", "part de prix de ΔIN : G_r (Π^pas − 1) IN/PIB", "fraction du PIB", "PIB du pas", PAS,
             "liste L2, décomposition de ΔIN"),
    Grandeur("C/(p v)", "C/(p v) (mesure)", "fraction des ventes", "p v", PAS, "liste L2, version sur p v"),
    Grandeur("G/(p v)", "G/(p v) (mesure)", "fraction des ventes", "p v", PAS, "liste L2, version sur p v"),
    Grandeur("I/(p v)", "I/(p v) (mesure)", "fraction des ventes", "p v", PAS, "liste L2, version sur p v"),
    Grandeur("ΔIN/(p v)", "ΔIN/(p v) (mesure)", "fraction des ventes", "p v", PAS, "liste L2, version sur p v"),
    Grandeur("T^cou/PIB", "couverture des intérêts T^cou/PIB (mesure)", "fraction du PIB", "PIB du pas", PAS,
             "sec:finances_publiques-impots"),
)


def allocations_alpha(e: dict[str, float], n_a: int) -> dict[str, float]:
    """Allocations de la liste L2 en un état (fractions, sans dimension)."""
    P = e["PIB"]
    pv = e["p"] * e["v"]
    Y_o = e["YD"] - e["i_D"] * e["V_H"] / n_a
    return {
        "C/Y_o": e["C"] / Y_o, "ti": e["ti"], "tu": e["tu"], "V_H/(n_a YD^HS)": e["V_H"] / (n_a * e["YD_HS"]),
        "I^vol/y": e["I_vol"] / e["y"], "K^vol/(n_a y)": e["K_vol"] / (n_a * e["y"]),
        "C/PIB": e["C"] / P, "G/PIB": e["G"] / P, "I/PIB": e["I"] / P, "ΔIN/PIB": e["dIN"] / P,
        "ΔIN/PIB volume": (e["Gr"] - 1) * e["IN"] / P, "ΔIN/PIB prix": e["Gr"] * e["pis"] * e["IN"] / P,
        "C/(p v)": e["C"] / pv, "G/(p v)": e["G"] / pv, "I/(p v)": e["I"] / pv, "ΔIN/(p v)": e["dIN"] / pv,
        "T^cou/PIB": e["T_cou"] / P,
    }


def _etendue(vals) -> float:
    """Étendue max − min ; NaN dès qu'une valeur n'est pas finie (#188). `max` et `min` ignorent un NaN qui n'est pas
    en tête : la valeur non finie serait masquée, comme dans `_delta_r_alpha` avant `94246ac`. Sur des valeurs
    finies, identique bit à bit à `max(vals) - min(vals)`."""
    vals = list(vals)
    if not all(math.isfinite(x) for x in vals):
        return math.nan
    return max(vals) - min(vals)


def superneutralite(par: Parametres) -> dict[str, object]:
    """Critère 13 de la fiche 8 (#80), lecture (α) pour le verdict, (β) en mesure (part de `monnaie`, § 7).

    Calculé au ν_G de `par` (ν_G retenu par `Calculs`), comme `mesure_alpha` et `sensibilite_fermeture`.
    """
    grille = {pi: mesure_alpha(par, pi, 12) for pi in PROFIL_PI}
    autres = {n: {pi: mesure_alpha(par, pi, n) for pi in POINTS_PI} for n in (4, 52)}

    def ecart(d, quoi=None):
        vals = [d[pi]["r_alpha"] if quoi is None else d[pi]["allocations"][quoi] for pi in POINTS_PI]
        return _etendue(vals)

    beta = {pi: etat_stationnaire(replace(par, pi_cible=pi, n_a=12, rbar=0.01)) for pi in POINTS_PI}
    theta_beta = [beta[pi]["theta_G"] for pi in POINTS_PI]
    alloc_b = {pi: allocations_alpha(b, 12) for pi, b in beta.items()}
    alloc_beta = {q: _etendue(a[q] for a in alloc_b.values())
                  for q in ALLOCATIONS_VERDICT + ALLOCATIONS_INVARIANTES + ALLOCATIONS_MESUREES}
    profil = [grille[pi]["r_alpha"] for pi in PROFIL_PI]
    toutes = ALLOCATIONS_VERDICT + ALLOCATIONS_INVARIANTES + ALLOCATIONS_MESUREES
    par_zeta = {z: {pi: mesure_alpha(replace(par, zeta=z), pi, 12) for pi in POINTS_PI}
                for z in (ZETA_ILLUSTRATION,) + ZETA_PLAGE}
    dependantes = [q for q in toutes if any(
        abs(par_zeta[z][pi]["allocations"][q] - par_zeta[ZETA_PLAGE[0]][pi]["allocations"][q])
        > TOL_INVARIANCE * abs(par_zeta[ZETA_PLAGE[0]][pi]["allocations"][q]) for z in par_zeta for pi in POINTS_PI)]
    return {
        "zeta": {z: {"r_alpha": {pi: d[pi]["r_alpha"] for pi in POINTS_PI}, "delta_r_alpha": ecart(d),
                     "allocations": {q: ecart(d, q) for q in toutes}} for z, d in par_zeta.items()},
        "dependantes_de_zeta": dependantes,
        "alpha": grille,
        "delta_r_alpha": ecart(grille),
        "delta_r_alpha_n_a": {n: ecart(autres[n]) for n in (4, 52)},
        "alpha_n_a": autres,
        "ecart_bornes": grille[0.10]["r_alpha"] - grille[0.0]["r_alpha"],
        "ecart_profil": _etendue(profil),
        "marche_2_3": grille[0.03]["r_alpha"] - grille[0.02]["r_alpha"],
        "allocations": {q: ecart(grille, q) for q in ALLOCATIONS_VERDICT + ALLOCATIONS_INVARIANTES
                        + ALLOCATIONS_MESUREES},
        "invariance": {q: ecart(grille, q) / abs(grille[0.02]["allocations"][q]) for q in ALLOCATIONS_INVARIANTES},
        "C_PIB_relatif_2": {pi: grille[pi]["allocations"]["C/PIB"] - grille[0.02]["allocations"]["C/PIB"]
                            for pi in (0.0, 0.10)},
        "beta_theta_G": _etendue(theta_beta),
        "beta_allocations": alloc_beta,
    }


# --- Illustration du bloc 7 (catégorie B de `monnaie`) ------------------------------


def banque_formes(e: dict[str, float], par: Parametres, v_H: float, m: float) -> dict[str, float]:
    """Formes du bloc 7 (`sec:banque-stationnaire`) appelées avec v_H et m donnés.

    l et d_F sont ceux de `e`, non arrondis. Sert à la contre-épreuve (B-1),
    avec v_H = 0,7 et m = 0,25/12, et à la republication (B-2, #83), avec v_H
    résolu et m par E8 ; θ_CB = 0, E^CB = 0.
    """
    n = par.n_a
    A = n * e["PIB"]
    l, d_F = e["L"] / A, e["D_F"] / A
    e_Bk = par.vartheta * l
    c = v_H + d_F - (1 - par.vartheta) * l
    b_Bk = c + m
    Mm = v_H + d_F
    Pi = e["i_CB"] * e_Bk + par.varpi_L * l + par.varpi_D * Mm  # Π^Bk/PIB, annuel sur annuel
    roe = _rapport(Pi, e_Bk)
    YD_an = v_H * (1 + par.nu_H * n * e["pis"]) / par.nu_H  # V_H/(n YD) = ν_H/(1 + ν_H n π^pas)
    return {
        "M": Mm, "b_Bk": b_Bk, "refinancement": m, "c": c, "Pi_Bk": 100 * Pi, "roe": 100 * roe,
        "part_distribuee": 1 - _rapport(n * e["gam"] * e_Bk, Pi), "part_titres": _rapport(b_Bk, l + b_Bk),
        "marge_nette": 100 * Pi / (l + b_Bk),
        "existence": _rapport(Pi - n * e["gam"] * e_Bk, l),
        "canal_rentier": 100 * 0.01 * c / YD_an, "part_v_H": 100 * _rapport(v_H, c),
        "part_entreprises": -100 * _rapport(l - d_F, c), "part_E_Bk": 100 * _rapport(e_Bk, c),
        "saut_C29": 100 * _rapport(0.01 * c, Pi), "saut_C29_suite": 100 * _rapport(0.01 * e_Bk, Pi),
        "d2": 100 * (_rapport(0.01 * c, e_Bk) + 11 * 0.01) / 12, "l": l, "d_F": d_F, "e_Bk": e_Bk,
    }


# --- Valeurs publiées et comparaison à la dernière décimale -------------------------


class Calculs:
    """Points de calcul mis en cache (états, valeurs, mesure (α), fermeture), à paramètres de base fixés.

    `nu_g_retenu` : ν_G auquel la mesure de #80 et la fermeture sont calculées (`NU_G_RETENU` par défaut).
    """

    def __init__(self, base: Parametres, nu_g_retenu: float = NU_G_RETENU) -> None:
        self.base = base
        self.nu_g_retenu = nu_g_retenu
        self._etats: dict[tuple, tuple[dict[str, float], Parametres]] = {}
        self._valeurs: dict[tuple, dict[str, float]] = {}
        self._alpha: dict[str, object] | None = None
        self._fermeture: dict[str, float] | None = None
        self._r_alpha_zeta: dict[tuple[float, float], float] = {}

    def par(self, pi: float = 0.02, na: int = 12, nu: float = 1.0, cfg: str = "R") -> Parametres:
        p = replace(self.base, pi_cible=pi, n_a=na, nu_G=nu)
        if cfg == "C-F":  # configuration de contrôle du bloc 6 : écarts nuls (non admissible)
            p = replace(p, varpi_L=0.0, varpi_D=0.0)
        return p

    def etat(self, pi: float = 0.02, na: int = 12, nu: float = 1.0, cfg: str = "R") -> dict[str, float]:
        """État du point ; lève `ReferenceNonPubliee` au point de référence ν_G = 1 si le plafond de E1 est actif."""
        cle = (pi, na, nu, cfg)
        if cle not in self._etats:
            p = self.par(pi, na, nu, cfg)
            e = etat_stationnaire(p, controler=(cfg == "R"))
            self._etats[cle] = (e, p)
        e = self._etats[cle][0]
        if cfg == "R" and nu == 1.0 and not e["marge_E1_montant"] > 0:
            raise ReferenceNonPubliee(pi, na, 1 - e["Gam"] * (e["G"] / e["PB"]) / nu)
        return e

    def v(self, pi: float = 0.02, na: int = 12, nu: float = 1.0, cfg: str = "R") -> dict[str, float]:
        cle = (pi, na, nu, cfg)
        if cle not in self._valeurs:
            self._valeurs[cle] = valeurs(self.etat(pi, na, nu, cfg), self.par(pi, na, nu, cfg))
        return self._valeurs[cle]

    def banque(self, pi: float = 0.02, na: int = 12, v_H: float | None = None, m: float | None = None,
               nu: float = 1.0, **ecarts) -> dict[str, float]:
        """Formes du bloc 7 : illustration (v_H, m donnés) ou republication (v_H et m résolus)."""
        e = self.etat(pi, na, nu)
        p = replace(self.par(pi, na, nu), **ecarts)
        A = na * e["PIB"]
        # Variante des écarts : l et d_F ne dépendent pas des écarts (bloc 6) ; seules les formes du bloc 7 les lisent.
        return banque_formes(e, p, e["V_H"] / A if v_H is None else v_H, e["M_G"] / A if m is None else m)

    # La mesure de #80 et la fermeture sont calculées à ν_G = `nu_g_retenu`, dans le domaine ν_G > 1 où le
    # plafond de E1 est un refus. Leurs sorties y sont identiques bit à bit à celles de ν_G = 1 : θ_G est fixé
    # avant l'entrée de ν_G dans l'ordre triangulaire (C59 ; `test_alpha_et_fermeture_identiques_a_nu_G_1`).
    def alpha(self) -> dict[str, object]:
        if self._alpha is None:
            self._alpha = superneutralite(replace(self.base, nu_G=self.nu_g_retenu))
        return self._alpha

    def fermeture(self) -> dict[str, float]:
        if self._fermeture is None:
            self._fermeture = sensibilite_fermeture(self.par(nu=self.nu_g_retenu))
        return self._fermeture

    def r_alpha(self, pi: float, zeta: float) -> float:
        """r̄_α(π*) en lecture (α) à ζ donné, n_a = 12, ν_G = `nu_g_retenu` (valeurs publiées hors du profil)."""
        cle = (pi, zeta)
        if cle not in self._r_alpha_zeta:
            p = replace(self.base, nu_G=self.nu_g_retenu, zeta=zeta)
            self._r_alpha_zeta[cle] = mesure_alpha(p, pi, 12)["r_alpha"]
        return self._r_alpha_zeta[cle]


ILL = {"v_H": 0.7, "m": 0.25 / 12}  # entrées d'illustration de `sec:banque-stationnaire`
EXPL_B2 = ("V_H résolu par le bloc ménages au lieu de 0,7 ; M^G* par E8, avec le délai Γ̄ et les intérêts de PB, "
           "au lieu de 0,25/12 (part de `monnaie`, § 5, B-2, écrite avant l'essai)")
EXPL_C = "règle C-HS de M33 au lieu de la maquette à impôt sur WB (part de `monnaie`, § 5, C, écrite avant l'essai)"

# Explications des écarts historiques de catégorie A (complément de #84) : établies après l'essai et testées
# (`test_explication_*`), ou cause non établie. Le statut est écrit dans le texte publié.
_ETABLIE = "établie après l'essai : "
_NON_ETABLIE = "cause non établie : maquette perdue (visa du 05/10/2026)"
EXPLICATIONS_ECARTS: dict[tuple[str, str], str] = {
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, n_a = 4"): _ETABLIE + "σ en pas dans la maquette",
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, n_a = 52"): _ETABLIE + "σ en pas dans la maquette",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 0 %, n_a = 4"): _ETABLIE + "σ en pas dans la maquette",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 10 %, n_a = 4"): _ETABLIE + "σ en pas dans la maquette",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 0 %, n_a = 52"): _ETABLIE + "σ en pas dans la maquette",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 10 %, n_a = 52"): _ETABLIE + "σ en pas dans la maquette",
    ("sec:finances_publiques-stationnaire", "Y^HS/PIB à 2 %"): _ETABLIE + "publié recalculé depuis T_H/PIB arrondi",
    ("sec:finances_publiques-emission ; tab:calibration", "marge J-ν à ν_G = 1,1, 0 %, %"):
        _ETABLIE + "publié sur G/PB à ν_G = 1",
    ("sec:finances_publiques-depense", "G/PB à 2 %"): _NON_ETABLIE,
    ("sec:finances_publiques-depense", "G/PB à 10 %"): _NON_ETABLIE,
    ("sec:finances_publiques-depense", "marge de E1 à 10 %"): _NON_ETABLIE,
    ("sec:finances_publiques-emission", "borne de ν_G à 10 %"): _NON_ETABLIE,
}
# Valeurs publiées dont le NaN du script signifie « aucune » (aucune racine hors du domaine C51), non « sans objet ».
SANS_RACINE = ("racine parasite à 0 %, %", "racine parasite à 2 %, %", "racine parasite à 10 %, %")
AUCUNE = "aucune"  # valeur publiée « aucune racine » : égale si et seulement si le script ne trouve aucune racine


def _racine_parasite(calc: Calculs, pi: float) -> float:
    """Racine de F hors du domaine C51 (r̄ ≤ −5 %), en % ; NaN si aucune ; refus (`HorsDomaine`) s'il y en a
    plusieurs, qu'une valeur unique ne saurait publier."""
    hors = [r for r in calc.alpha()["alpha"][pi]["racines"] if r <= -0.05]
    if len(hors) > 1:
        raise HorsDomaine(f"lecture (α), π* = {pi!r} : {len(hors)} racines parasites (r̄ ≤ −5 %) au lieu d'au plus "
                          f"une ; racines {hors!r} (condition C51)")
    return 100 * hors[0] if hors else math.nan


def _fisher_hors_cible(par: Parametres, pi_bar: float, varpi_L: float) -> dict[str, float]:
    """Illustration de `sec:investissement-taux` (limites) : glissement stationnaire π̄ distinct de la cible π* de
    `par`, taux du crédit de Fisher au taux réel r̄ de `par`, écart ϖ_L donné. Rend, en % par an : i_L, ϱ_L (S1,
    lu sur π*) et Δϱ = ϱ_L − ϱ̄_L, ϱ̄_L étant lu à π̄ = π* ; arithmétique sans état résolu (catégorie S)."""
    def rho(pi: float) -> tuple[float, float]:
        i_L = (1 + par.rbar) * (1 + pi) - 1 + varpi_L
        return i_L, (1 + i_L) / (1 + par.pi_cible) - 1
    i_L, rho_L = rho(pi_bar)
    return {"i_L": 100 * i_L, "rho_L": 100 * rho_L, "d_rho": 100 * (rho_L - rho(par.pi_cible)[1])}


def _allocation_hors_cible(par: Parametres, pi_bar: float, zeta: float) -> dict[str, float]:
    """Illustration de `sec:investissement-taux` (limites), suite de `_fisher_hors_cible` (écart ϖ_L de `par`) :
    allocation stationnaire sous S2 à l'écart Δϱ, pour l'élasticité ζ donnée (non celle de `par`). Rend le taux
    d'utilisation tu = t̄u e^{ζΔϱ} (fraction de la capacité normale) et le capital en volume rapporté à la production
    annuelle κ/tu, en années (même forme que `etat_stationnaire`, K^vol = n_a κ y/tu), t̄u et κ de `par` (calibration
    indicative) ; Δϱ par an ; arithmétique sans état résolu (catégorie S)."""
    d_rho = _fisher_hors_cible(par, pi_bar, par.varpi_L)["d_rho"] / 100
    tu = par.tu_bar * math.exp(zeta * d_rho)
    return {"tu": tu, "capital": par.kappa / tu}


# (section, description, valeur publiée, fonction de calcul dans l'unité publiée, catégorie)
# Catégories : A (à reproduire, lue sur l'état résolu), S (arithmétique de la spécification : formule ou limite
# sans état résolu, sur des entrées d'illustration de la spécification ou sur les paramètres de la configuration ;
# comptée à part dans le bilan, elle ne contrôle pas l'état), B-2 (formes du bloc 7 sur l'état résolu,
# republication de #83), D (#80) ; C (périmée, remesurée) ne subsiste que dans l'historique (`VALEURS_AVANT_VISA`),
# B-1 et N dans la contre-épreuve (`VALEURS_CONTRE_EPREUVE`). Seules les valeurs en vigueur y figurent : chacune est
# écrite hors de \barre{…} (spécification) et de ~~…~~ (fiches) dans sa source, qu'un test lit. Les valeurs sont
# celles de la spécification republiée (commit 8b9fa94), qui affiche barrées les valeurs antérieures ; celles de
# « fiche 8 » (docs/blocs/banque_centrale.md) et de « fiche 9 » (docs/blocs/finances_publiques.md) sont les
# remesures annotées le 05/10/2026.
VALEURS_PUBLIEES: tuple[tuple[str, str, str, object, str], ...] = (
    ("sec:cadre-calendrier", "π^pas à 2 %, % par pas", "0,16516", lambda c: c.v()["pi_pas"], "A"),
    ("sec:cadre-calendrier", "Γ^e à 2 %", "1,0033059", lambda c: c.v()["Gamma"], "A"),
    ("sec:cadre-calendrier", "γ^e à 2 %, % par pas", "0,33059", lambda c: c.v()["gamma_pas"], "A"),
    ("sec:cadre-calendrier", "K^vol/I^vol annuel, n_a = 4", "14,3160",
     lambda c: c.etat(na=4)["K_vol"] / (4 * c.etat(na=4)["I_vol"]), "A"),
    ("sec:cadre-calendrier", "K^vol/I^vol annuel, n_a = 12", "14,3228",
     lambda c: c.etat()["K_vol"] / (12 * c.etat()["I_vol"]), "A"),
    ("sec:cadre-calendrier", "K^vol/I^vol annuel, n_a = 52", "14,3253",
     lambda c: c.etat(na=52)["K_vol"] / (52 * c.etat(na=52)["I_vol"]), "A"),
    ("sec:cadre-calendrier", "fraction annuelle résorbée, λ = 0,5", "0,3999", lambda c: 1 - (1 - 0.5 / 12) ** 12, "S"),
    ("sec:cadre-calendrier", "rendement annuel crédité, i = 4 %, %", "4,0742",
     lambda c: 100 * ((1 + 0.04 / 12) ** 12 - 1), "S"),
    ("sec:cadre-calendrier", "facteur restitué, volume (x = 2 %)", "1,0108", lambda c: c.v()["facteur_volume"], "A"),
    ("sec:cadre-calendrier", "facteur restitué, u.m. (x = 4,04 %)", "1,0216", lambda c: c.v()["facteur_stock"], "A"),
    ("sec:production-stationnaire", "IN^vol/v = n_a σ", "1,4", lambda c: c.v()["IN_sur_v"], "A"),
    ("sec:production-stationnaire", "y/v, n_a = 12", "1,0023122", lambda c: c.v()["y_sur_v"], "A"),
    ("sec:production-stationnaire", "y/v, n_a = 4", "1,0023160", lambda c: c.v(na=4)["y_sur_v"], "A"),
    ("sec:production-stationnaire", "y/v, n_a = 52", "1,0023107", lambda c: c.v(na=52)["y_sur_v"], "A"),
    ("sec:production-stationnaire", "ρ̄_IN à 2 %", "0,996057", lambda c: c.v()["rho_IN"], "A"),
    ("sec:production-stationnaire", "ρ̄_IN à 10 %", "0,981246", lambda c: c.v(pi=0.10)["rho_IN"], "A"),
    ("sec:production-stationnaire", "ρ̄_IN à 50 % (forme)", "0,923901",
     lambda c: rho_IN(12, c.base.sigma, c.etat()["g"], 0.50),
     "A"),
    ("sec:production-stationnaire", "ρ̄_IN, n_a = 4", "0,992779", lambda c: c.v(na=4)["rho_IN"], "A"),
    ("sec:production-stationnaire", "ρ̄_IN, n_a = 52", "0,997321", lambda c: c.v(na=52)["rho_IN"], "A"),
    ("sec:production-stationnaire", "ρ̄_IN, n_a → ∞ (limite)", "0,997700",
     lambda c: 1 / (1 + math.log(1 + c.base.pi_cible) * c.base.sigma
                    / (1 + c.base.sigma * math.log((1 + c.base.g_pr) * (1 + c.base.g_N)))), "S"),
    ("sec:production-stationnaire", "ΔIN/IN à 2 %, % par pas", "0,33059", lambda c: c.v()["dIN_sur_IN"], "A"),
    ("sec:production-stationnaire", "taux d'utilisation", "0,8", lambda c: c.v()["tu"], "A"),
    ("sec:production-capital", "ρ̄_K à 0 %", "1", lambda c: c.v(pi=0.0)["rho_K"], "A"),
    ("sec:production-capital", "ρ̄_K à 2 %", "0,7786", lambda c: c.v()["rho_K"], "A"),
    ("sec:production-capital", "ρ̄_K à 10 %", "0,4214", lambda c: c.v(pi=0.10)["rho_K"], "A"),
    ("sec:production-stationnaire", "ρ̄_K, n_a = 4", "0,7778", lambda c: c.v(na=4)["rho_K"], "A"),
    ("sec:production-stationnaire", "ρ̄_K, n_a = 52", "0,7789", lambda c: c.v(na=52)["rho_K"], "A"),
    ("sec:production-stationnaire", "ρ̄_K, n_a → ∞ (limite)", "0,7790",
     lambda c: ((math.log((1 + c.base.g_pr) * (1 + c.base.g_N)) + c.base.delta)
                / (math.log((1 + c.base.g_pr) * (1 + c.base.g_N) * (1 + c.base.pi_cible)) + c.base.delta)), "S"),
    ("sec:investissement-lignes", "écart de valorisation à 2 %, %", "-22,14", lambda c: c.v()["ecart_valorisation"],
     "A"),
    ("sec:investissement-lignes", "écart de valorisation à 10 %, %", "-57,86",
     lambda c: c.v(pi=0.10)["ecart_valorisation"], "A"),
    ("sec:investissement-lignes", "capital de clôture au prix du tour, 2 %, %", "-22,01",
     lambda c: c.v()["ecart_valorisation_cloture"], "A"),
    ("sec:investissement-lignes", "capital de clôture au prix du tour, 10 %, %", "-57,52",
     lambda c: c.v(pi=0.10)["ecart_valorisation_cloture"], "A"),
    ("sec:travail-stationnaire", "hausse du salaire, n_a = 4, % par pas", "0,99505",
     lambda c: c.v(na=4)["hausse_salaire_pas"], "A"),
    ("sec:travail-stationnaire", "hausse du salaire, n_a = 12, % par pas", "0,33059",
     lambda c: c.v()["hausse_salaire_pas"], "A"),
    ("sec:travail-stationnaire", "hausse du salaire, n_a = 52, % par pas", "0,07619",
     lambda c: c.v(na=52)["hausse_salaire_pas"], "A"),
    ("sec:travail-stationnaire", "glissement du salaire à 2 %, % par an", "4,0400",
     lambda c: c.v()["hausse_salaire_an"], "A"),
    ("sec:travail-stationnaire", "glissement du salaire à 10 %, % par an", "12,2000",
     lambda c: c.v(pi=0.10)["hausse_salaire_an"], "A"),
    ("sec:travail-stationnaire", "part salariale à 2 %, n_a = 12", "0,624645", lambda c: c.v()["part_salariale"], "A"),
    ("sec:travail-stationnaire", "part salariale à 2 %, n_a = 4", "0,624648", lambda c: c.v(na=4)["part_salariale"],
     "A"),
    ("sec:travail-stationnaire", "part salariale à 2 %, n_a = 52", "0,624644", lambda c: c.v(na=52)["part_salariale"],
     "A"),
    ("sec:travail-stationnaire", "écart à ω̄ à 2 %, point", "0,035", lambda c: c.v()["ecart_part_salariale"], "A"),
    ("sec:travail-stationnaire", "écart à ω̄ à 10 %, point", "0,370", lambda c: c.v(pi=0.10)["ecart_part_salariale"],
     "A"),
    ("sec:prix-stationnaire", "hausse du prix à 2 %, % par pas", "0,16516", lambda c: c.v()["hausse_prix_pas"], "A"),
    ("sec:prix-stationnaire", "hausse du prix à 10 %, % par pas", "0,79741", lambda c: c.v(pi=0.10)["hausse_prix_pas"],
     "A"),
    ("sec:prix-stationnaire", "part salariale à 10 %, n_a = 12", "0,621303", lambda c: c.v(pi=0.10)["part_salariale"],
     "A"),
    ("sec:prix-stationnaire", "part salariale à 10 %, n_a = 4", "0,621337",
     lambda c: c.v(pi=0.10, na=4)["part_salariale"], "A"),
    ("sec:prix-stationnaire", "part salariale à 10 %, n_a = 52", "0,621290",
     lambda c: c.v(pi=0.10, na=52)["part_salariale"], "A"),
    ("sec:menages-stationnaire", "V_H/(n_a YD) à 2 %", "1,076531", lambda c: c.v()["richesse_YD"], "A"),
    ("sec:menages-stationnaire", "V_H/(n_a YD) à 10 %", "0,995242", lambda c: c.v(pi=0.10)["richesse_YD"], "A"),
    ("sec:menages-stationnaire", "V_H/(n_a YD) à 2 %, n_a = 4", "1,076493", lambda c: c.v(na=4)["richesse_YD"], "A"),
    ("sec:menages-stationnaire", "V_H/(n_a YD) à 2 %, n_a = 52", "1,076545", lambda c: c.v(na=52)["richesse_YD"], "A"),
    ("sec:menages-stationnaire", "V_H/(n_a YD) à 10 %, n_a = 4", "0,994485",
     lambda c: c.v(pi=0.10, na=4)["richesse_YD"], "A"),
    ("sec:menages-stationnaire", "V_H/(n_a YD) à 10 %, n_a = 52", "0,995532",
     lambda c: c.v(pi=0.10, na=52)["richesse_YD"], "A"),
    ("sec:menages-stationnaire", "taux d'épargne à 2 %, %", "4,2707", lambda c: c.v()["epargne"], "A"),
    ("sec:menages-stationnaire", "dont maintien à 2 %, point", "2,1336", lambda c: c.v()["epargne_maintien"], "A"),
    ("sec:menages-stationnaire", "dont épargne réelle à 2 %, point", "2,1371", lambda c: c.v()["epargne_reelle"], "A"),
    ("sec:menages-stationnaire", "taux d'épargne à 10 %, %", "11,5116", lambda c: c.v(pi=0.10)["epargne"], "A"),
    ("sec:menages-stationnaire", "dont maintien à 10 %, point", "9,5234", lambda c: c.v(pi=0.10)["epargne_maintien"],
     "A"),
    ("sec:menages-stationnaire", "dont épargne réelle à 10 %, point", "1,9882",
     lambda c: c.v(pi=0.10)["epargne_reelle"], "A"),
    ("sec:menages-stationnaire", "C/YD à 2 %", "0,95729", lambda c: c.v()["C_sur_YD"], "A"),
    ("sec:menages-stationnaire", "C/YD à 10 %", "0,8849", lambda c: c.v(pi=0.10)["C_sur_YD"], "A"),
    ("sec:menages-stationnaire", "épargne visée à 2 %, %", "2,1837", lambda c: c.v()["epargne_visee"], "A"),
    ("sec:menages-stationnaire", "épargne visée à 10 %, %", "2,1975", lambda c: c.v(pi=0.10)["epargne_visee"], "A"),
    ("sec:menages-stationnaire", "épargne visée à 2 %, n_a = 4, %", "2,1945", lambda c: c.v(na=4)["epargne_visee"],
     "A"),
    ("sec:menages-stationnaire", "épargne visée à 2 %, n_a = 52, %", "2,1795", lambda c: c.v(na=52)["epargne_visee"],
     "A"),
    ("sec:menages-stationnaire", "marge du plafond à 2 %, mois", "13,49", lambda c: c.v()["marge_plafond_mois"], "A"),
    ("sec:menages-stationnaire", "V_H_0/YD_0 à 2 %", "12,9184", lambda c: c.v()["V_H_sur_YD"], "A"),
    ("sec:menages-stationnaire", "superneutralité, i_D = 1 % + π̄, 2 %", "1,010286",
     lambda c: 1 / (1 + (12 * c.v()["pi_pas"] / 100 - (0.01 + 0.02))), "A"),
    ("sec:menages-stationnaire", "superneutralité, i_D = 1 % + π̄, 10 %", "1,014518",
     lambda c: 1 / (1 + (12 * c.v(pi=0.10)["pi_pas"] / 100 - (0.01 + 0.10))), "A"),
    ("sec:menages-stationnaire", "richesse visée nominale (écartée), 2 %", "1,030928", lambda c: 1 / (1 - 0.03), "S"),
    ("sec:menages-stationnaire", "richesse visée nominale (écartée), 10 %", "1,123596", lambda c: 1 / (1 - 0.11), "S"),
    ("sec:menages-stationnaire", "Fisher sur la cible, 2 %", "1,010490",
     lambda c: 1 / (1 + (12 * c.v()["pi_pas"] / 100 - (1.01 * 1.02 - 1))), "A"),
    ("sec:menages-stationnaire", "Fisher sur la cible, 10 %", "1,015548",
     lambda c: 1 / (1 + (12 * c.v(pi=0.10)["pi_pas"] / 100 - (1.01 * 1.10 - 1))), "A"),
    ("sec:menages-stationnaire", "i_D = r + n_a π^pas", "1,010101", lambda c: 1 / (1 - 0.01), "S"),
    ("sec:investissement-stationnaire", "K^vol/(n_a y), ans", "2", lambda c: c.v()["K_vol_sur_y"], "A"),
    ("sec:investissement-stationnaire", "n_a[(1 + g)^{1/n_a} − 1] + δ, %", "6,9819",
     lambda c: 100 * 12 * c.etat()["I_vol"] / c.etat()["K_vol"], "A"),
    ("sec:investissement-stationnaire", "ti (C-F)", "0,13964", lambda c: c.v(cfg="C-F")["ti"], "A"),
    ("sec:investissement-stationnaire", "ti, n_a = 4 (C-F)", "0,13970", lambda c: c.v(na=4, cfg="C-F")["ti"], "A"),
    ("sec:investissement-stationnaire", "ti, n_a = 52 (C-F)", "0,13961", lambda c: c.v(na=52, cfg="C-F")["ti"], "A"),
    ("sec:investissement-stationnaire", "I/PIB à 2 % (C-F), %", "13,956", lambda c: c.v(cfg="C-F")["I_sur_PIB"], "A"),
    ("sec:investissement-stationnaire", "I/PIB à 10 % (C-F), %", "13,881",
     lambda c: c.v(pi=0.10, cfg="C-F")["I_sur_PIB"], "A"),
    ("sec:investissement-stationnaire", "I/PIB, n_a = 4 (C-F), %", "13,962",
     lambda c: c.v(na=4, cfg="C-F")["I_sur_PIB"], "A"),
    ("sec:investissement-stationnaire", "I/PIB, n_a = 52 (C-F), %", "13,953",
     lambda c: c.v(na=52, cfg="C-F")["I_sur_PIB"], "A"),
    ("sec:investissement-stationnaire", "capital au prix courant à 2 % (C-F)", "1,99887",
     lambda c: c.v(cfg="C-F")["K_courant"], "A"),
    ("sec:investissement-stationnaire", "capital au prix courant à 10 % (C-F)", "1,98817",
     lambda c: c.v(pi=0.10, cfg="C-F")["K_courant"], "A"),
    ("sec:investissement-stationnaire", "capital comptable à 2 % (C-F)", "1,55635",
     lambda c: c.v(cfg="C-F")["K_comptable"], "A"),
    ("sec:investissement-stationnaire", "capital comptable à 10 % (C-F)", "0,83790",
     lambda c: c.v(pi=0.10, cfg="C-F")["K_comptable"], "A"),
    ("sec:investissement-stationnaire", "capital comptable, n_a = 4 (C-F)", "1,55481",
     lambda c: c.v(na=4, cfg="C-F")["K_comptable"], "A"),
    ("sec:investissement-stationnaire", "capital comptable, n_a = 52 (C-F)", "1,55694",
     lambda c: c.v(na=52, cfg="C-F")["K_comptable"], "A"),
    ("sec:investissement-stationnaire", "crédits à 2 % (C-F)", "0,62254", lambda c: c.v(cfg="C-F")["credits"], "A"),
    ("sec:investissement-stationnaire", "crédits à 10 % (C-F)", "0,33516",
     lambda c: c.v(pi=0.10, cfg="C-F")["credits"], "A"),
    ("sec:investissement-stationnaire", "crédits nets à 2 % (C-F)", "0,45635",
     lambda c: c.v(cfg="C-F")["credits_nets"], "A"),
    ("sec:investissement-stationnaire", "crédits nets à 10 % (C-F)", "0,16986",
     lambda c: c.v(pi=0.10, cfg="C-F")["credits_nets"], "A"),
    ("sec:investissement-stationnaire", "dépôts à 2 % (C-F)", "0,16619", lambda c: c.v(cfg="C-F")["depots_F"], "A"),
    ("sec:investissement-stationnaire", "dépôts à 10 % (C-F)", "0,16530",
     lambda c: c.v(pi=0.10, cfg="C-F")["depots_F"], "A"),
    ("sec:investissement-stationnaire", "valeur nette des entreprises à 2 % (C-F)", "1,17242",
     lambda c: c.v(cfg="C-F")["V_F"], "A"),
    ("sec:investissement-stationnaire", "valeur nette des entreprises à 10 % (C-F)", "0,73900",
     lambda c: c.v(pi=0.10, cfg="C-F")["V_F"], "A"),
    ("sec:investissement-stationnaire", "FU/V_F à 2 % (C-F), % par pas", "0,33059",
     lambda c: c.v(cfg="C-F")["FU_sur_V_F"], "A"),
    ("sec:investissement-stationnaire", "FU/V_F à 10 % (C-F), % par pas", "0,96389",
     lambda c: c.v(pi=0.10, cfg="C-F")["FU_sur_V_F"], "A"),
    ("sec:investissement-stationnaire", "distribution à 2 % (C-F)", "0,83609",
     lambda c: c.v(cfg="C-F")["distribution"], "A"),
    ("sec:investissement-stationnaire", "distribution à 10 % (C-F)", "0,73116",
     lambda c: c.v(pi=0.10, cfg="C-F")["distribution"], "A"),
    ("sec:investissement-stationnaire", "distribution, n_a = 4 (C-F)", "0,83576",
     lambda c: c.v(na=4, cfg="C-F")["distribution"], "A"),
    ("sec:investissement-stationnaire", "distribution, n_a = 52 (C-F)", "0,83621",
     lambda c: c.v(na=52, cfg="C-F")["distribution"], "A"),
    ("sec:investissement-stationnaire", "dividendes/ventes à 2 % (C-F), %", "23,79",
     lambda c: c.v(cfg="C-F")["Div_F_sur_ventes"], "A"),
    ("sec:investissement-stationnaire", "dividendes/ventes à 10 % (C-F), %", "23,44",
     lambda c: c.v(pi=0.10, cfg="C-F")["Div_F_sur_ventes"], "A"),
    ("sec:investissement-stationnaire", "lv* ρ̄_K à 0 %", "0,4", lambda c: c.v(pi=0.0, cfg="C-F")["levier_courant"],
     "A"),
    ("sec:investissement-stationnaire", "lv* ρ̄_K à 2 %", "0,3114", lambda c: c.v(cfg="C-F")["levier_courant"], "A"),
    ("sec:investissement-stationnaire", "lv* ρ̄_K à 10 %", "0,1686",
     lambda c: c.v(pi=0.10, cfg="C-F")["levier_courant"], "A"),
    ("sec:investissement-stationnaire", "distribution à 2 % (R)", "0,82751", lambda c: c.v()["distribution"], "A"),
    ("sec:investissement-stationnaire", "distribution à 10 % (R)", "0,72390", lambda c: c.v(pi=0.10)["distribution"],
     "A"),
    ("sec:investissement-stationnaire", "dividendes/ventes à 2 % (R), %", "22,38", lambda c: c.v()["Div_F_sur_ventes"],
     "A"),
    ("sec:investissement-stationnaire", "dividendes/ventes à 10 % (R), %", "22,60",
     lambda c: c.v(pi=0.10)["Div_F_sur_ventes"], "A"),
    ("sec:investissement-taux", "ϱ̄_L sans écart (Fisher), 2 %, %", "1,000", lambda c: c.v(cfg="C-F")["rho_L"], "A"),
    # Valeurs de `sec:investissement-taux` vérifiées à la main par `monnaie` (#93, point 3), désormais comparées.
    ("sec:investissement-taux", "i_L,0 à 2 %, %", "5,02", lambda c: c.v()["i_L"], "A"),
    ("sec:investissement-taux", "ϱ̄_L à 2 %, %", "2,961", lambda c: c.v()["rho_L"], "A"),
    ("sec:investissement-taux", "i_L à π̄ = 10 %, π* = 2 %, %", "13,10",
     lambda c: _fisher_hors_cible(c.base, 0.10, c.base.varpi_L)["i_L"], "S"),
    ("sec:investissement-taux", "ϱ_L à π̄ = 10 %, π* = 2 %, %", "10,88",
     lambda c: _fisher_hors_cible(c.base, 0.10, c.base.varpi_L)["rho_L"], "S"),
    ("sec:investissement-taux", "Δϱ à π̄ = 10 %, π* = 2 %, point", "7,92",
     lambda c: _fisher_hors_cible(c.base, 0.10, c.base.varpi_L)["d_rho"], "S"),
    ("sec:investissement-taux", "i_L sans écart (Fisher) à π̄ = 10 %, π* = 2 %, %", "11,10",
     lambda c: _fisher_hors_cible(c.base, 0.10, 0.0)["i_L"], "S"),
    ("sec:investissement-taux", "ϱ_L sans écart (Fisher) à π̄ = 10 %, π* = 2 %, %", "8,92",
     lambda c: _fisher_hors_cible(c.base, 0.10, 0.0)["rho_L"], "S"),
    # Autres valeurs de la même section, comparées depuis #101 : i_L,0 de la configuration de contrôle (A) ; Δϱ à
    # π̄ = 0 et allocation stationnaire sous S2 à ζ = 4, 8 et 17 (paragraphe des limites, S).
    ("sec:investissement-taux", "i_L,0 sans écart (Fisher), 2 %, %", "3,02", lambda c: c.v(cfg="C-F")["i_L"], "A"),
    ("sec:investissement-taux", "Δϱ à π̄ = 0, π* = 2 %, point", "-1,98",
     lambda c: _fisher_hors_cible(c.base, 0.0, c.base.varpi_L)["d_rho"], "S"),
    ("sec:investissement-taux", "tu à π̄ = 10 %, ζ = 4", "1,098",
     lambda c: _allocation_hors_cible(c.base, 0.10, 4.0)["tu"], "S"),
    ("sec:investissement-taux", "capital à π̄ = 10 %, ζ = 4, an de production", "1,457",
     lambda c: _allocation_hors_cible(c.base, 0.10, 4.0)["capital"], "S"),
    ("sec:investissement-taux", "tu à π̄ = 10 %, ζ = 8", "1,508",
     lambda c: _allocation_hors_cible(c.base, 0.10, 8.0)["tu"], "S"),
    ("sec:investissement-taux", "capital à π̄ = 10 %, ζ = 8, an de production", "1,061",
     lambda c: _allocation_hors_cible(c.base, 0.10, 8.0)["capital"], "S"),
    ("sec:investissement-taux", "capital à π̄ = 0, ζ = 4, ans de production", "2,165",
     lambda c: _allocation_hors_cible(c.base, 0.0, 4.0)["capital"], "S"),
    ("sec:investissement-taux", "capital à π̄ = 0, ζ = 8, ans de production", "2,343",
     lambda c: _allocation_hors_cible(c.base, 0.0, 8.0)["capital"], "S"),
    ("sec:investissement-taux", "capital à π̄ = 0, ζ = 17, ans de production", "2,801",
     lambda c: _allocation_hors_cible(c.base, 0.0, 17.0)["capital"], "S"),
    ("sec:banque-taux", "ϱ̄_L à 0 %, %", "3,000", lambda c: c.v(pi=0.0)["rho_L"], "A"),
    ("sec:banque-taux", "ϱ̄_L à 2 % (tab:calibration), %", "2,961", lambda c: c.v()["rho_L"], "A"),
    ("sec:banque-taux", "ϱ̄_L à 10 %, %", "2,818", lambda c: c.v(pi=0.10)["rho_L"], "A"),
    ("sec:banque-taux", "écart de ϱ̄_L entre 0 et 10 %, point", "0,18",
     lambda c: c.v(pi=0.0)["rho_L"] - c.v(pi=0.10)["rho_L"], "A"),
)

VALEURS_PUBLIEES += (
    ("sec:finances_publiques-stationnaire", "θ_G à 0 %", "0,219575", lambda c: c.v(pi=0.0)["theta_G"], "A"),
    ("sec:finances_publiques-stationnaire", "θ_G à 2 %", "0,220584", lambda c: c.v()["theta_G"], "A"),
    ("sec:finances_publiques-stationnaire", "θ_G à 10 %", "0,220187", lambda c: c.v(pi=0.10)["theta_G"], "A"),
    ("sec:finances_publiques-stationnaire", "G/PIB à 0 %, %", "21,98", lambda c: c.v(pi=0.0)["G_sur_PIB"], "A"),
    ("sec:finances_publiques-stationnaire", "T_H/PIB à 0 %, %", "21,78", lambda c: c.v(pi=0.0)["T_H_sur_PIB"], "A"),
    ("sec:finances_publiques-stationnaire", "G/PIB à 2 %, %", "22,05", lambda c: c.v()["G_sur_PIB"], "A"),
    ("sec:finances_publiques-stationnaire", "T_H/PIB à 2 %, %", "21,71", lambda c: c.v()["T_H_sur_PIB"], "A"),
    ("sec:finances_publiques-stationnaire", "G/PIB à 10 %, %", "21,89", lambda c: c.v(pi=0.10)["G_sur_PIB"], "A"),
    ("sec:finances_publiques-stationnaire", "T_H/PIB à 10 %, %", "21,61", lambda c: c.v(pi=0.10)["T_H_sur_PIB"], "A"),
    ("sec:finances_publiques-stationnaire", "dette consolidée à 0 %", "0,20444",
     lambda c: c.v(pi=0.0)["dette_consolidee"], "A"),
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %", "0,35350", lambda c: c.v()["dette_consolidee"],
     "A"),
    ("sec:finances_publiques-stationnaire", "dette consolidée à 10 %", "0,59359",
     lambda c: c.v(pi=0.10)["dette_consolidee"], "A"),
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, n_a = 4", "0,35398",
     lambda c: c.v(na=4)["dette_consolidee"], "A"),
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, n_a = 52", "0,35331",
     lambda c: c.v(na=52)["dette_consolidee"], "A"),
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, arrondie", "0,353",
     lambda c: c.v()["dette_consolidee"], "A"),
    ("sec:finances_publiques-stationnaire", "dette brute à 0 %", "0,22291", lambda c: c.v(pi=0.0)["dette_brute"], "A"),
    ("sec:finances_publiques-stationnaire", "dette brute à 2 %", "0,37274", lambda c: c.v()["dette_brute"], "A"),
    ("sec:finances_publiques-stationnaire", "dette brute à 10 %", "0,61731", lambda c: c.v(pi=0.10)["dette_brute"],
     "A"),
    ("sec:finances_publiques-stationnaire", "décomposition à 2 % : richesse des ménages", "0,7165",
     lambda c: c.v()["decomp_v_H"], "A"),
    ("sec:finances_publiques-stationnaire", "décomposition à 2 % : −crédits nets", "-0,4564",
     lambda c: c.v()["decomp_entreprises"], "A"),
    ("sec:finances_publiques-stationnaire", "décomposition à 2 % : fonds propres de la banque", "0,0934",
     lambda c: c.v()["decomp_E_Bk"], "A"),
    ("sec:finances_publiques-stationnaire", "décomposition à 2 % : somme", "0,3535",
     lambda c: c.v()["decomp_v_H"] + c.v()["decomp_entreprises"] + c.v()["decomp_E_Bk"], "A"),
    ("sec:finances_publiques-stationnaire", "n_a(Γ̄ − 1) à 0 %, % par an", "1,9819",
     lambda c: c.v(pi=0.0)["domar_facteur"], "A"),
    ("sec:finances_publiques-stationnaire", "n_a(Γ̄ − 1) à 2 %, % par an", "3,9671", lambda c: c.v()["domar_facteur"],
     "A"),
    ("sec:finances_publiques-stationnaire", "n_a(Γ̄ − 1) à 10 %, % par an", "11,5667",
     lambda c: c.v(pi=0.10)["domar_facteur"], "A"),
    ("sec:finances_publiques-stationnaire", "déficit de Domar à 0 %, % du PIB", "0,4052",
     lambda c: c.v(pi=0.0)["deficit_i"], "A"),
    ("sec:finances_publiques-stationnaire", "déficit de Domar à 2 %, % du PIB", "1,4023", lambda c: c.v()["deficit_i"],
     "A"),
    ("sec:finances_publiques-stationnaire", "déficit de Domar à 10 %, % du PIB", "6,8659",
     lambda c: c.v(pi=0.10)["deficit_i"], "A"),
    ("sec:finances_publiques-stationnaire", "solde primaire à 0 %, % du PIB", "-0,2007",
     lambda c: c.v(pi=0.0)["primaire"], "A"),
    ("sec:finances_publiques-stationnaire", "solde primaire à 2 %, % du PIB", "-0,3348", lambda c: c.v()["primaire"],
     "A"),
    ("sec:finances_publiques-stationnaire", "solde primaire à 10 %, % du PIB", "-0,2770",
     lambda c: c.v(pi=0.10)["primaire"], "A"),
    ("sec:finances_publiques-stationnaire", "intérêts bruts à 0 %, % du PIB", "0,2229",
     lambda c: c.v(pi=0.0)["interets_bruts"], "A"),
    ("sec:finances_publiques-stationnaire", "intérêts nets à 0 %, % du PIB", "0,2044",
     lambda c: c.v(pi=0.0)["interets_nets"], "A"),
    ("sec:finances_publiques-stationnaire", "intérêts bruts à 2 %, % du PIB", "1,1257",
     lambda c: c.v()["interets_bruts"], "A"),
    ("sec:finances_publiques-stationnaire", "intérêts nets à 2 %, % du PIB", "1,0676",
     lambda c: c.v()["interets_nets"], "A"),
    ("sec:finances_publiques-stationnaire", "intérêts bruts à 10 %, % du PIB", "6,8522",
     lambda c: c.v(pi=0.10)["interets_bruts"], "A"),
    ("sec:finances_publiques-stationnaire", "intérêts nets à 10 %, % du PIB", "6,5888",
     lambda c: c.v(pi=0.10)["interets_nets"], "A"),
    ("sec:finances_publiques-stationnaire", "YD^HS/PIB à 0 %", "0,6533", lambda c: c.v(pi=0.0)["YD_HS"], "A"),
    ("sec:finances_publiques-stationnaire", "YD^HS/PIB à 2 %", "0,6513", lambda c: c.v()["YD_HS"], "A"),
    ("sec:finances_publiques-stationnaire", "YD^HS/PIB à 10 %", "0,6483", lambda c: c.v(pi=0.10)["YD_HS"], "A"),
    ("sec:finances_publiques-stationnaire", "Y^HS/PIB à 0 %", "0,8710", lambda c: c.v(pi=0.0)["Y_HS"], "A"),
    ("sec:finances_publiques-stationnaire", "Y^HS/PIB à 2 %", "0,8684", lambda c: c.v()["Y_HS"], "A"),
    ("sec:finances_publiques-stationnaire", "Y^HS/PIB à 10 %", "0,8645", lambda c: c.v(pi=0.10)["Y_HS"], "A"),
    ("sec:finances_publiques-stationnaire", "encaisse à 0 %", "0,018469", lambda c: c.v(pi=0.0)["encaisse"], "A"),
    ("sec:finances_publiques-stationnaire", "encaisse à 2 %", "0,019246", lambda c: c.v()["encaisse"], "A"),
    ("sec:finances_publiques-stationnaire", "encaisse à 10 %", "0,023722", lambda c: c.v(pi=0.10)["encaisse"], "A"),
    ("sec:finances_publiques-depense", "G/PB à 0 %", "0,98996", lambda c: c.v(pi=0.0)["G_sur_PB"], "A"),
    ("sec:finances_publiques-depense", "G/PB à 2 %", "0,95142", lambda c: c.v()["G_sur_PB"], "A"),
    ("sec:finances_publiques-depense", "G/PB à 10 %", "0,76159", lambda c: c.v(pi=0.10)["G_sur_PB"], "A"),
    ("sec:finances_publiques-depense", "marge de E1 à 0 %", "0,0084", lambda c: c.v(pi=0.0)["marge_E1"], "A"),
    ("sec:finances_publiques-depense", "marge de E1 à 2 %", "0,0454", lambda c: c.v()["marge_E1"], "A"),
    ("sec:finances_publiques-depense", "marge de E1 à 10 %", "0,2311", lambda c: c.v(pi=0.10)["marge_E1"], "A"),
    ("sec:finances_publiques-depense", "hausse admissible à 0 %, ν_G = 1, %", "0,85",
     lambda c: c.v(pi=0.0)["hausse_admissible"], "A"),
    ("sec:finances_publiques-emission", "borne de ν_G à 0 %", "1,0908", lambda c: c.v(pi=0.0)["borne_nu_G"], "A"),
    ("sec:finances_publiques-emission", "borne de ν_G à 2 %", "1,0500", lambda c: c.v()["borne_nu_G"], "A"),
    ("sec:finances_publiques-emission", "borne de ν_G à 10 %", "0,8458", lambda c: c.v(pi=0.10)["borne_nu_G"], "A"),
    ("sec:finances_publiques-emission", "retour après −5 % (approché), 0 %", "1,0432",
     lambda c: c.v(pi=0.0)["retour_approche"], "A"),
    ("sec:finances_publiques-emission ; tab:calibration", "marge J-ν à ν_G = 1,1, 0 %, %", "0,85",
     lambda c: 100 * c.v(pi=0.0, nu=1.1)["marge_J_nu"], "A"),
    ("sec:finances_publiques-impots", "dette consolidée, 10 % moins 2 %", "0,240",
     lambda c: c.v(pi=0.10)["dette_consolidee"] - c.v()["dette_consolidee"], "A"),
    ("sec:finances_publiques-transferts", "impôt des ménages à 2 %, % du PIB", "21,71", lambda c: c.v()["T_H_sur_PIB"],
     "A"),
    ("sec:finances_publiques-caisse", "dépôts des ménages / impôt du mois, environ", "39,6",
     lambda c: c.v()["D_H_sur_T_H"], "A"),
    ("sec:finances_publiques-restitution", "facteur d'un stock en u.m. à 10 %", "1,0638",
     lambda c: c.v(pi=0.10)["facteur_stock"], "A"),
    ("sec:finances_publiques-restitution", "taux des titres à 2 %, %", "3,02", lambda c: c.v()["i_CB"], "A"),
    ("sec:finances_publiques-restitution", "taux des titres à 10 %, %", "11,10", lambda c: c.v(pi=0.10)["i_CB"], "A"),
    ("sec:finances_publiques-restitution", "taux apparent = barème, %", "25", lambda c: c.v()["taux_apparent"], "A"),
    ("sec:banque_centrale-stationnaire", "facteur de l'indice par pas à 2 %", "1,0016516",
     lambda c: 1 + c.v()["pi_pas"] / 100, "A"),
    ("sec:banque_centrale-stationnaire", "glissement à 2 %, %", "2,0000", lambda c: c.v()["glissement"], "A"),
    ("sec:banque_centrale-stationnaire", "i_CB à 0 %, %", "1,00", lambda c: c.v(pi=0.0)["i_CB"], "A"),
    ("sec:banque_centrale-stationnaire", "i_CB à 2 %, %", "3,02", lambda c: c.v()["i_CB"], "A"),
    ("sec:banque_centrale-stationnaire", "i_CB à 10 %, %", "11,10", lambda c: c.v(pi=0.10)["i_CB"], "A"),
    ("sec:banque_centrale-stationnaire", "r restitué à 0 %, %", "1,00", lambda c: c.v(pi=0.0)["r_restitue"], "A"),
    ("sec:banque_centrale-stationnaire", "r restitué à 2 %, %", "1,02", lambda c: c.v()["r_restitue"], "A"),
    ("sec:banque_centrale-stationnaire", "r restitué à 10 %, %", "1,10", lambda c: c.v(pi=0.10)["r_restitue"], "A"),
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̄, % de la production par point de r̄", "-0,267",
     lambda c: c.fermeture()["dtheta_G_dr"], "A"),
    ("sec:banque_centrale-stationnaire", "points de r̄ par point de PIB de dépense", "-3,75",
     lambda c: c.fermeture()["points_r_par_point_PIB"], "A"),
    ("docs/blocs/banque_centrale.md § 2, critère 13 (b)", "taux réel exact à 0 %, %", "0,9996",
     lambda c: c.v(pi=0.0)["r_exact"], "A"),
    ("docs/blocs/banque_centrale.md § 2, critère 13 (b)", "taux réel exact à 2 %, %", "1,0359",
     lambda c: c.v()["r_exact"], "A"),
    ("docs/blocs/banque_centrale.md § 2, critère 13 (b)", "taux réel exact à 10 %, %", "1,5180",
     lambda c: c.v(pi=0.10)["r_exact"], "A"),
    ("docs/blocs/banque_centrale.md § 2, critère 13 (b)", "taux réel Haig-Simons (sur i_CB) à 0 %, %", "1,0000",
     lambda c: c.v(pi=0.0)["r_HS"], "A"),
    ("docs/blocs/banque_centrale.md § 2, critère 13 (b)", "taux réel Haig-Simons (sur i_CB) à 2 %, %", "1,0381",
     lambda c: c.v()["r_HS"], "A"),
    ("docs/blocs/banque_centrale.md § 2, critère 13 (b)", "taux réel Haig-Simons (sur i_CB) à 10 %, %", "1,5310",
     lambda c: c.v(pi=0.10)["r_HS"], "A"),
    ("sec:banque-stationnaire", "i_L à 0 %, %", "3,00", lambda c: c.v(pi=0.0)["i_L"], "A"),
    ("sec:banque-stationnaire", "i_L à 2 %, %", "5,02", lambda c: c.v()["i_L"], "A"),
    ("sec:banque-stationnaire", "i_L à 10 %, %", "13,10", lambda c: c.v(pi=0.10)["i_L"], "A"),
    ("sec:banque-stationnaire", "i_D à 0 %, %", "0,00", lambda c: c.v(pi=0.0)["i_D"], "A"),
    ("sec:banque-stationnaire", "i_D à 2 %, %", "2,02", lambda c: c.v()["i_D"], "A"),
    ("sec:banque-stationnaire", "i_D à 10 %, %", "10,10", lambda c: c.v(pi=0.10)["i_D"], "A"),
    ("sec:banque-stationnaire", "rendement réel des dépôts à 0 %, point", "0,00",
     lambda c: c.v(pi=0.0)["rendement_reel_depots"], "A"),
    ("sec:banque-stationnaire", "rendement réel des dépôts à 2 %, point", "0,02",
     lambda c: c.v()["rendement_reel_depots"], "A"),
    ("sec:banque-stationnaire", "rendement réel des dépôts à 10 %, point", "0,10",
     lambda c: c.v(pi=0.10)["rendement_reel_depots"], "A"),
    ("sec:banque-stationnaire", "e_Bk à 0 %", "0,12010", lambda c: c.v(pi=0.0)["e_Bk"], "A"),
    ("sec:banque-stationnaire", "e_Bk à 2 %", "0,09338", lambda c: c.v()["e_Bk"], "A"),
    ("sec:banque-stationnaire", "e_Bk à 10 %", "0,05027", lambda c: c.v(pi=0.10)["e_Bk"], "A"),
    ("sec:banque-stationnaire", "crédits à 0 %", "0,80069", lambda c: c.v(pi=0.0)["credits"], "A"),
    ("sec:banque-stationnaire", "crédits à 2 %", "0,62254", lambda c: c.v()["credits"], "A"),
    ("sec:banque-stationnaire", "crédits à 10 %", "0,33516", lambda c: c.v(pi=0.10)["credits"], "A"),
    ("sec:banque-stationnaire", "crédits à 2 %, n_a = 4", "0,621923", lambda c: c.v(na=4)["credits"], "A"),
    ("sec:banque-stationnaire", "crédits à 2 %, n_a = 12", "0,622539", lambda c: c.v()["credits"], "A"),
    ("sec:banque-stationnaire", "crédits à 2 %, n_a = 52", "0,622775", lambda c: c.v(na=52)["credits"], "A"),
    ("sec:banque-stationnaire", "dépôts des entreprises à 0 %", "0,16643", lambda c: c.v(pi=0.0)["depots_F"], "A"),
    ("sec:banque-stationnaire", "condition d'existence à écarts nuls, 2 %", "-0,001421",
     lambda c: c.v(cfg="C-F")["existence_Bk"], "A"),
    ("sec:banque-stationnaire", "impôt d'inflation net à 0 %, %", "0", lambda c: c.v(pi=0.0)["impot_inflation"], "A"),
    ("sec:banque-stationnaire", "impôt d'inflation net à 2 %, %", "-0,041", lambda c: c.v()["impot_inflation"], "A"),
    ("sec:banque-stationnaire", "impôt d'inflation net à 10 %, %", "-0,529", lambda c: c.v(pi=0.10)["impot_inflation"],
     "A"),
    ("sec:banque-conditions", "déficit de Domar dû à E^Bk à 0 %, % du PIB", "0,238",
     lambda c: c.v(pi=0.0)["domar_E_Bk"], "A"),
    ("sec:banque-conditions", "déficit de Domar dû à E^Bk à 2 %, % du PIB", "0,370", lambda c: c.v()["domar_E_Bk"],
     "A"),
    ("sec:banque-conditions", "déficit de Domar dû à E^Bk à 10 %, % du PIB", "0,582",
     lambda c: c.v(pi=0.10)["domar_E_Bk"], "A"),
    ("sec:banque-conditions", "couplage −ϑ lv*", "-0,06", lambda c: c.v()["couplage"], "A"),
)

# --- Contre-épreuve : valeurs barrées reproduites sous leurs entrées d'origine ---------
# Hors du bilan des valeurs en vigueur (revue finale, rang 8 ; décision du mainteneur du 05/10/2026, point A).
# Catégorie B-1 : formes du bloc 7 appelées avec v_H = 0,7 et m = 0,25/12, entrées d'illustration de la
# publication au commit 54edad8 (valeurs barrées) ; elles attribuent l'écart de la republication (B-2) à ces
# deux entrées seules. Catégorie N : valeurs barrées calculées à un ν_G non retenu (1 ou 1,1). Les paramètres de
# ces publications qui diffèrent des défauts actuels de `Parametres` sont rétablis par `ENTREES_D_ORIGINE`.
ENTREES_D_ORIGINE: dict[str, float] = {
    "mu_bar": 0.25,  # μ̄ avant la décision M34 (#92) : valeur des publications barrées
    "vartheta": 0.10,  # ϑ avant la décision M34 (#130) : valeur des publications barrées
    "nu_H": 1.0,  # ν_H avant la décision M34 (#62) : valeur des publications barrées
    "zeta": 4.0,  # ζ avant la décision M34 (#55) : valeur des publications barrées
    "lambda_w": 1.0,  # λ_w avant la décision M34 (#45) : valeur des publications barrées
}
VALEURS_CONTRE_EPREUVE: tuple[tuple[str, str, str, object, str], ...] = tuple(
    ("sec:banque-stationnaire", f"illustration : {nom} à {int(round(100 * pi))} %", pub,
     (lambda c, pi=pi, cle=cle, f=f: f * c.banque(pi=pi, **ILL)[cle]), "B-1")
    for (nom, cle, f), pubs in (
        (("masse monétaire M", "M", 1), ("0,86636", "0,86605", "0,86492")),
        (("titres de la banque", "b_Bk", 1), ("0,16686", "0,32705", "0,58480")),
        (("dette consolidée c", "c", 1), ("0,14603", "0,30622", "0,56397")),
        (("résultat Π^Bk/PIB", "Pi_Bk", 0.01), ("0,02547", "0,02298", "0,01905")),
        (("rendement des fonds propres, %", "roe", 1), ("31,82", "36,94", "56,97")),
        (("part distribuée", "part_distribuee", 1), ("0,93772", "0,89262", "0,79695")),
        (("part des titres dans l'actif", "part_titres", 1), ("0,1725", "0,3446", "0,6362")),
        (("marge nette d'intérêt, %", "marge_nette", 1), ("2,633", "2,421", "2,072")),
        (("canal rentier, % de YD par point", "canal_rentier", 1), ("0,209", "0,429", "0,735")),
    )
    for pi, pub in zip(POINTS_PI, pubs, strict=True)
) + (
    ("sec:banque-stationnaire", "illustration : refinancement", "0,02083", lambda c: c.banque(**ILL)["refinancement"],
     "B-1"),
    ("sec:banque-stationnaire", "illustration : ROE, variante basse, 0 %, %", "7,32",
     lambda c: c.banque(pi=0.0, varpi_L=0.004, varpi_D=0.00214, **ILL)["roe"], "B-1"),
    ("sec:banque-stationnaire", "illustration : ROE, variante basse, 10 %, %", "20,64",
     lambda c: c.banque(pi=0.10, varpi_L=0.004, varpi_D=0.00214, **ILL)["roe"], "B-1"),
    ("sec:banque-stationnaire", "illustration : part distribuée à 2 %, n_a = 4", "0,892301",
     lambda c: c.banque(na=4, **ILL)["part_distribuee"], "B-1"),
    ("sec:banque-stationnaire", "illustration : part distribuée à 2 %, n_a = 12", "0,892616",
     lambda c: c.banque(**ILL)["part_distribuee"], "B-1"),
    ("sec:banque-stationnaire", "illustration : part distribuée à 2 %, n_a = 52", "0,892737",
     lambda c: c.banque(na=52, **ILL)["part_distribuee"], "B-1"),
    ("sec:banque-stationnaire", "illustration : marge d'existence à 2 %", "0,0330",
     lambda c: c.banque(**ILL)["existence"], "B-1"),
    ("sec:banque-stationnaire", "illustration : titres de 2 à 10 %", "0,25775",
     lambda c: c.banque(pi=0.10, **ILL)["b_Bk"] - c.banque(**ILL)["b_Bk"], "B-1"),
    ("sec:banque-stationnaire", "illustration : dont entreprises (d_F − l)", "0,2865",
     lambda c: ((c.banque(pi=0.10, **ILL)["d_F"] - c.banque(pi=0.10, **ILL)["l"])
                - (c.banque(**ILL)["d_F"] - c.banque(**ILL)["l"])), "B-1"),
    ("sec:banque-stationnaire", "illustration : dont fonds propres (ϑ Δl)", "-0,0288",
     lambda c: c.banque(pi=0.10, **ILL)["e_Bk"] - c.banque(**ILL)["e_Bk"], "B-1"),
    ("sec:banque-stationnaire", "illustration : part des intérêts des dépôts, 2 %, %", "228,6",
     lambda c: c.banque(**ILL)["part_v_H"], "B-1"),
    ("sec:banque-stationnaire", "illustration : part des dividendes des entreprises, 2 %, %", "-148,9",
     lambda c: c.banque(**ILL)["part_entreprises"], "B-1"),
    ("sec:banque-stationnaire", "illustration : part du dividende de la banque, 2 %, %", "20,3",
     lambda c: c.banque(**ILL)["part_E_Bk"], "B-1"),
    ("sec:banque-resultat", "illustration : saut C29 au tour n, 2 %, %", "13,33",
     lambda c: c.banque(**ILL)["saut_C29"], "B-1"),
    ("sec:banque-resultat", "illustration : saut C29 ensuite, 2 %, %", "2,71",
     lambda c: c.banque(**ILL)["saut_C29_suite"], "B-1"),
    ("sec:banque-conditions", "illustration : (d2), 2 %, point", "1,33", lambda c: c.banque(**ILL)["d2"], "B-1"),
    ("sec:finances_publiques-transferts", "charge brute à 2 %, ν_G = 1, % du PIB", "0,83",
     lambda c: c.v()["interets_bruts"], "N"),
    ("sec:finances_publiques-restitution", "dette brute affichée à 2 %, ν_G = 1, % du PIB", "28,2",
     lambda c: c.v()["dette_brute_affichee"], "N"),
    ("sec:finances_publiques-restitution", "dette brute affichée à 10 %, ν_G = 1, % du PIB", "56,7",
     lambda c: c.v(pi=0.10)["dette_brute_affichee"], "N"),
    ("sec:banque-stationnaire", "effet de ν_G = 1,1 sur le refinancement, 2 %", "1,1003",
     lambda c: c.v(nu=1.1)["multiplicateur_nu"], "N"),
)

# Catégorie D : mesure de #80 (lecture (α), n_a = 12, ν_G = 1).
VALEURS_PUBLIEES += tuple(
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", f"r̄_α à π* = {pub_pi} %, %", pub,
     (lambda c, pi=pi: 100 * c.alpha()["alpha"][pi]["r_alpha"]), "D")
    for pi, pub_pi, pub in zip(PROFIL_PI, ("0", "1", "2", "3", "4", "6", "10"),
                               ("1,270", "1,109", "1,000", "0,932", "0,899", "0,922", "1,278"), strict=True)
) + (
    ("sec:banque_centrale-conditions", "r̄_α(0) − r̄_α(10 %), point", "-0,008",
     lambda c: -100 * c.alpha()["ecart_bornes"], "D"),
    ("sec:banque_centrale-conditions", "écart maximal de r̄_α sur le profil, point", "0,379",
     lambda c: 100 * c.alpha()["ecart_profil"], "D"),
    ("sec:banque_centrale-conditions", "marche de cible de 2 à 3 %, point", "-0,07",
     lambda c: 100 * c.alpha()["marche_2_3"], "D"),
    ("sec:finances_publiques-impots", "racine parasite à 0 %, %", AUCUNE, lambda c: _racine_parasite(c, 0.0), "D"),
    ("sec:finances_publiques-impots", "racine parasite à 2 %, %", AUCUNE, lambda c: _racine_parasite(c, 0.02), "D"),
    ("sec:finances_publiques-impots", "racine parasite à 10 %, %", AUCUNE, lambda c: _racine_parasite(c, 0.10), "D"),
    ("fiche 9 § 6.3", "(β) : écart de θ_G entre 0, 2 et 10 %, point", "0,101",
     lambda c: 100 * c.alpha()["beta_theta_G"], "D"),
    ("fiche 9 § 3.C", "(α) : C/PIB à 0 % moins à 2 %, point", "0,433",
     lambda c: 100 * c.alpha()["C_PIB_relatif_2"][0.0], "D"),
    ("fiche 9 § 3.C", "(α) : C/PIB à 10 % moins à 2 %, point", "-0,191",
     lambda c: 100 * c.alpha()["C_PIB_relatif_2"][0.10], "D"),
    ("fiche 9 § 6.3", "(α) : max − min de C/PIB, point", "0,624", lambda c: 100 * c.alpha()["allocations"]["C/PIB"],
     "D"),
)


# Valeurs en vigueur ajoutées à la revue finale (rang 8 ; décision du mainteneur du 05/10/2026, point A (ii)) :
# niveaux du bloc 7 republiés à ν_G retenu et entre crochets à ν_G = 1, tableau tab:etat-stationnaire, niveaux
# restitués, valeurs hors liste du constat m6 de `monnaie` et de la fiche 9. Chaque valeur est lue dans sa source.
# Catégorie B-2 : formes du bloc 7 appelées sur l'état résolu (v_H résolu, m par E8 ; republication de #83).
_NU = NU_G_RETENU  # colonne des valeurs publiées « à ν_G = 1,15 »


def _derivee_norme_tenue(calc: Calculs, phi: float, zeta: float, h: float = 1e-4) -> float:
    """dθ_G/dr̂ à l'arrivée, norme ϱ̄_L et i^ref tenus à l'état résolu (π* = 2 %, n_a = 12, ν_G retenu), sous φ et ζ
    donnés ; différence centrée de pas h autour de r̄, en point de la production potentielle par point."""
    r = calc.par(nu=calc.nu_g_retenu).rbar
    return (_theta_norme_tenue(calc, phi, zeta, r + h) - _theta_norme_tenue(calc, phi, zeta, r - h)) / (2 * h)


def _delta_r_alpha(calc: Calculs, zeta: float) -> float:
    """Δr̄_α = max − min de r̄_α sur {0 ; 2 % ; 10 %} à ζ donné, en point ; NaN dès qu'un r̄_α n'est pas fini (`max`
    et `min` ignorent un NaN qui n'est pas en tête : la valeur non finie serait masquée, constat M1 de l'audit de
    #173). Une ligne publiée qui lit cette valeur sort alors en écart (« script sans objet ; écart +nan »)."""
    r = [calc.r_alpha(pi, zeta) for pi in POINTS_PI]
    if not all(math.isfinite(x) for x in r):
        return math.nan
    return 100 * (max(r) - min(r))


def minimum_delta_r_alpha_en_zeta(calc: Calculs, bornes: tuple[float, float] = ZETA_MINIMUM_BORNES,
                                  tol: float = TOL_ZETA_MINIMUM) -> tuple[float, float]:
    """(ζ*, Δr̄_α(ζ*)) : minimum de Δr̄_α en ζ sur `bornes`, Δ en point (#173, forme P273, lecture de `monnaie`).

    Δr̄_α = max − min de r̄_α sur {0 ; 2 % ; 10 %}, r̄_α(2 %) étant r̄ (à quelques 1e−18 près). À la table T1, le
    point le plus haut est r̄_α(0) de ζ = 2 à 7, puis r̄_α(10 %) ; le plus bas est r̄_α(2 %) = r̄ jusqu'au point
    anguleux où r̄_α(0) le rejoint (ζ ≈ 63), puis r̄_α(0). Le minimum est ce point anguleux, artefact de la
    statistique max − min et non optimum économique. ζ* est localisé par bissection de r̄_α(0 ; ζ) − r̄_α(2 % ; ζ)
    jusqu'à une largeur `tol` (milieu de l'intervalle final ; ⌈log₂(largeur/tol)⌉ itérations, 18 sur [2 ; 200] à
    1e−3), puis contrôlé comme minimum local : avec [a ; b] l'intervalle final et w = b − a, Δr̄_α décroît de a − w à
    a et croît de b à b + w. Ces deux paires restent chacune d'un côté du point anguleux ; comparer Δr̄_α(ζ*) aux seules
    extrémités a et b refuserait un vrai minimum quand ζ* tombe au-delà du point anguleux plus loin que l'extrémité
    restée en deçà (mesuré : ν_H = 1 seul, ζ* = 64,384, écart de 1e−7 point). Ce contrôle est local ; Δr̄_α(ζ*) est
    enfin comparé à Δr̄_α aux deux bornes de recherche (P281, constat R1 de l'audit de #173, deux évaluations de plus),
    pour que le libellé « minimum sur [2 ; 200] » ne repose pas sur le seul voisinage de ζ*.

    Refus d'argument, par `HorsDomaine`, avant toute évaluation : bornes non finies ou non croissantes, `tol` non
    finie ou ≤ 0, borne basse ≤ 0 (ζ > 0, terme en 1/ζ de r̄_α), `tol` ≥ largeur de `bornes` (aucune bissection,
    voisins hors de l'intervalle). Refus par `MinimumNonEncadre` (#191, P320), que `table_publiees` publie
    « refusée » : différence de même signe (ou nulle) aux deux bornes, ou non finie (point anguleux non encadré ;
    minimum non localisé par cette méthode) ; refus de domaine (`HorsDomaine`) de `calc.r_alpha` en un ζ évalué,
    converti avec son message ; milieu hors de ]a ; b[ (précision de la machine, ou a + b qui déborde) ou
    `ITERATIONS_MAX` dépassé avant la largeur `tol` ; voisin a − w ou b + w hors de `bornes`, refusé sans écrêtage
    ni évaluation ; croisement trouvé mais Δr̄_α non décroissante à gauche ou non croissante à droite (croisement
    non minimal) ; Δr̄_α à l'une des bornes inférieure ou égale à Δr̄_α(ζ*) (minimum aux bornes) ; un r̄_α non fini
    à l'un des sept ζ où Δr̄_α est évaluée (r̄_α non fini), avant la comparaison qui le lirait. Chaque refus porte
    son motif ; tout ζ passé à `calc.r_alpha` est dans `bornes`, donc > 0."""
    a, b = bornes
    if not (math.isfinite(a) and math.isfinite(b) and a < b and math.isfinite(tol) and tol > 0):
        raise HorsDomaine(f"minimum de Δr̄_α en ζ : bornes [{a!r} ; {b!r}] finies et croissantes, tolérance {tol!r} "
                          "finie et > 0 attendues")
    if a <= 0:
        raise HorsDomaine(f"minimum de Δr̄_α en ζ : borne basse {a!r} ≤ 0 ; ζ > 0 attendu (terme en 1/ζ de r̄_α)")
    if tol >= b - a:
        raise HorsDomaine(f"minimum de Δr̄_α en ζ : tolérance {tol!r} ≥ largeur {b - a!r} de [{a!r} ; {b!r}] ; "
                          "tolérance inférieure à la largeur attendue")

    def evaluer(fonction, zeta: float) -> float:
        """`fonction(zeta)`, son refus de domaine (lecture (α) en ζ) converti en constat publié (#191)."""
        try:
            return fonction(zeta)
        except MinimumNonEncadre:
            raise
        except HorsDomaine as refus:
            raise MinimumNonEncadre(f"refus de domaine à ζ = {zeta!r} ({refus}) : minimum non localisé par cette "
                                    "méthode") from refus

    def ecart(zeta: float) -> float:
        return evaluer(lambda z: calc.r_alpha(0.0, z) - calc.r_alpha(0.02, z), zeta)

    fa, fb = ecart(a), ecart(b)
    if not (math.isfinite(fa) and math.isfinite(fb) and fa * fb < 0):
        raise MinimumNonEncadre(f"r̄_α(0) − r̄_α(2 %) vaut {fa!r} à ζ = {a!r} et {fb!r} à ζ = {b!r}, aucun "
                                f"changement de signe sur [{a!r} ; {b!r}] : point anguleux non encadré ; minimum "
                                "non localisé par cette méthode")
    iterations = 0
    while b - a > tol:
        if iterations >= ITERATIONS_MAX:
            raise MinimumNonEncadre(f"bissection en ζ non convergée en {ITERATIONS_MAX} itérations sur [{a!r} ; "
                                    f"{b!r}], largeur {tol!r} non atteinte : minimum non localisé par cette méthode")
        m = (a + b) / 2
        if not (a < m < b):  # milieu égal à une extrémité (précision) ou non fini (a + b déborde)
            raise MinimumNonEncadre(f"milieu {m!r} hors de ]{a!r} ; {b!r}[ (précision de la machine ou dépassement) "
                                    f"avant la largeur {tol!r} : minimum non localisé par cette méthode")
        fm = ecart(m)
        iterations += 1
        if not math.isfinite(fm):
            raise MinimumNonEncadre(f"r̄_α(0) − r̄_α(2 %) non fini ({fm!r}) à ζ = {m!r} : minimum non localisé par "
                                    "cette méthode")
        if (fa < 0) == (fm < 0):
            a, fa = m, fm
        else:
            b = m

    def delta_fini(z: float) -> float:
        d = evaluer(lambda x: _delta_r_alpha(calc, x), z)
        if not math.isfinite(d):
            raise MinimumNonEncadre(f"r̄_α non fini à ζ = {z!r} (Δr̄_α = {d!r}) : minimum non localisé par cette "
                                    "méthode")
        return d

    zeta, w = (a + b) / 2, b - a
    borne_basse, borne_haute = bornes
    hors = [z for z, dedans in ((a - w, borne_basse <= a - w), (b + w, b + w <= borne_haute)) if not dedans]
    if hors:
        raise MinimumNonEncadre(f"voisin du contrôle de minimum local hors de [{borne_basse!r} ; {borne_haute!r}] : "
                                f"ζ = {' et '.join(repr(z) for z in hors)} ; croisement trop près d'une borne, "
                                "minimum non localisé par cette méthode")
    gauche, delta_a, delta_b, droite = (delta_fini(z) for z in (a - w, a, b, b + w))
    if not (gauche > delta_a and droite > delta_b):
        raise MinimumNonEncadre(f"croisement trouvé mais non minimal : Δr̄_α vaut {gauche!r}, {delta_a!r}, "
                                f"{delta_b!r} et {droite!r} à ζ = {a - w!r}, {a!r}, {b!r} et {b + w!r}")
    delta = delta_fini(zeta)
    delta_basse, delta_haute = delta_fini(borne_basse), delta_fini(borne_haute)
    if not (delta_basse > delta and delta_haute > delta):
        raise MinimumNonEncadre(f"minimum aux bornes : Δr̄_α vaut {delta!r} à ζ* = {zeta!r}, {delta_basse!r} à "
                                f"ζ = {borne_basse!r} et {delta_haute!r} à ζ = {borne_haute!r} : le minimum sur "
                                f"[{borne_basse!r} ; {borne_haute!r}] n'est pas au croisement")
    return zeta, delta


def _canal_ecarts_nominaux(calc: Calculs, zeta: float) -> float:
    """Part de ϖ_L dans r̄_α(10 %) − r̄_α(0), en point, mesurée sur l'état résolu (#80 ; avis de `monnaie` du
    06/10/2026) : la différence en lecture (α) à ϖ_L de la configuration, moins la même différence à ϖ_L = 0, ϖ_D
    tenu, à ζ donné (n_a = 12, ν_G retenu).

    Limite : ϖ_L et ϖ_D ne peuvent être annulés ensemble (`HorsDomaine` sur l'existence du dividende de la banque,
    `sec:banque-stationnaire`) ; seul ϖ_L s'isole, ce qui est la formule publiée ϖ_L[1/1,02 − 1/1,10] −
    ϖ_L[1/1,02 − 1], égale à la mesure à quelques 1e−13 près et indépendante de ζ (`test_canal_ecarts_nominaux_*`).
    """
    p = replace(calc.base, nu_G=calc.nu_g_retenu, zeta=zeta, varpi_L=0.0)
    sans_L = mesure_alpha(p, 0.10, 12)["r_alpha"] - mesure_alpha(p, 0.0, 12)["r_alpha"]
    return 100 * ((calc.r_alpha(0.10, zeta) - calc.r_alpha(0.0, zeta)) - sans_L)


def _theta_norme_tenue(calc: Calculs, phi: float, zeta: float, r: float) -> float:
    """θ_G à l'arrivée sous r̂ = r, norme ϱ̄_L et i^ref tenus à l'état résolu (π* = 2 %, n_a = 12, ν_G retenu)."""
    p = replace(calc.par(nu=calc.nu_g_retenu), phi=phi, zeta=zeta)
    rho = calc.etat(nu=calc.nu_g_retenu)["rho_L"]
    return etat_stationnaire(p, r_neutre=r, rho_bar_L=rho, controler=False)["theta_G"]


def _hausse_d_un_point(calc: Calculs, phi: float, zeta: float) -> float:
    """θ_G(r̄ + 0,01) − θ_G(r̄), norme et i^ref tenus, sous φ et ζ donnés, en point de la production potentielle :
    effet d'un point fini, au voisinage de r̄ = 1 % (avis de `monnaie` du 06/10/2026)."""
    r = calc.par(nu=calc.nu_g_retenu).rbar
    return 100 * (_theta_norme_tenue(calc, phi, zeta, r + 0.01) - _theta_norme_tenue(calc, phi, zeta, r))


def _restitue(calc: Calculs, pi: float, ratio: float) -> float:
    """Ratio d'ouverture multiplié par le facteur d'un stock en u.m. (`sec:cadre-calendrier`), à ν_G retenu publié."""
    return ratio * calc.v(pi=pi, nu=_NU)["facteur_stock"]


# Tableau tab:etat-stationnaire : (grandeur, clé de `valeurs`, ν_G, libellé de la ligne dans la source, valeurs
# publiées à π̄ = 0, 2 et 10 %).
_TAB_ETAT: tuple[tuple[str, str, float, str, tuple[str, str, str]], ...] = (
    ("capital sur production (a), en volume", "K_vol_sur_y", _NU, "Capital sur production (a), en volume",
     ("2,000", "2,000", "2,000")),
    ("capital sur production (b), au prix courant", "K_courant", _NU, "Capital sur production (b), au prix courant",
     ("2,0017", "1,9989", "1,9882")),
    ("capital sur production (c), comptable", "K_comptable", _NU, "Capital sur production (c), comptable",
     ("2,0017", "1,5563", "0,8379")),
    ("part salariale", "part_salariale", _NU, "Part salariale", ("0,62554", "0,62465", "0,62130")),
    ("taux réel neutre, %", "rbar", _NU, "Taux réel neutre, paramètre", ("1,00", "1,00", "1,00")),
    ("taux directeur, %", "i_CB", _NU, "Taux directeur", ("1,00", "3,02", "11,10")),
    ("taux réel restitué, %", "r_restitue", _NU, "Taux réel restitué", ("1,00", "1,02", "1,10")),
    ("taux réel du crédit anticipé, %", "rho_L", _NU, "Taux réel du crédit anticipé", ("3,000", "2,961", "2,818")),
    ("inflation (glissement), %", "glissement", _NU, "Inflation", ("0", "2", "10")),
    ("hausse du prix par pas, %", "hausse_prix_pas", _NU, "dont hausse par pas", ("0", "0,16516", "0,79741")),
    ("part de la dépense publique θ_G", "theta_G", _NU, "Part de la dépense publique, résolue",
     ("0,219575", "0,220584", "0,220187")),
    ("taux d'investissement, %", "I_sur_PIB", _NU, "Taux d'investissement", ("13,976", "13,956", "13,881")),
    ("masse monétaire", "masse_monetaire", _NU, "Masse monétaire", ("0,88503", "0,88265", "0,87848")),
    ("dette consolidée", "dette_consolidee", _NU, "Dette consolidée", ("0,20444", "0,35350", "0,59359")),
    ("dette brute", "dette_brute", _NU, "Dette brute", ("0,22568", "0,37564", "0,62091")),
    ("dette brute, ν_G = 1", "dette_brute", 1.0, "Dette brute, $\\nu_G = 1$ (référence hors domaine)",
     ("0,22291", "0,37274", "0,61731")),
    ("dette brute affichée, % du PIB", "dette_brute_affichee", _NU, "Dette brute affichée", ("22,8", "38,4", "66,0")),
    ("déficit public (Domar), % du PIB", "deficit_i", _NU, "Déficit public (Domar)", ("0,4052", "1,4023", "6,8659")),
    ("solde primaire, % du PIB", "primaire", _NU, "Solde primaire", ("-0,2007", "-0,3348", "-0,2770")),
)


VALEURS_PUBLIEES += tuple(
    ("sec:banque-stationnaire", f"{nom} à {round(100 * pi)} %{suffixe}", pub,
     (lambda c, pi=pi, cle=cle, f=f, nu=nu: f * c.banque(pi=pi, nu=nu)[cle]), "B-2")
    for (nom, cle, f, nu, suffixe), pubs in (
        (("masse monétaire M", "M", 1, _NU, ""), ("0,88503", "0,88265", "0,87848")),
        (("titres de la banque", "b_Bk", 1, _NU, ", ν_G = 1,15"), ("0,22568", "0,37564", "0,62091")),
        (("titres de la banque", "b_Bk", 1, 1.0, ", ν_G = 1"), ("0,22291", "0,37274", "0,61731")),
        (("refinancement", "refinancement", 1, _NU, ", ν_G = 1,15"), ("0,021242", "0,022141", "0,027318")),
        (("refinancement", "refinancement", 1, 1.0, ", ν_G = 1"), ("0,018469", "0,019246", "0,023722")),
        (("dette consolidée c", "c", 1, _NU, ""), ("0,20444", "0,35350", "0,59359")),
        (("résultat Π^Bk/PIB", "Pi_Bk", 0.01, _NU, ""), ("0,02607", "0,02410", "0,02107")),
        (("rendement des fonds propres (brut, nominal, sans charges), %", "roe", 1, _NU, ""),
         ("21,70", "25,81", "41,91")),
        (("part distribuée", "part_distribuee", 1, _NU, ""), ("0,90868", "0,84627", "0,72399")),
        (("part des titres dans l'actif", "part_titres", 1, _NU, ", ν_G = 1,15"), ("0,2199", "0,3763", "0,6494")),
        (("part des titres dans l'actif", "part_titres", 1, 1.0, ", ν_G = 1"), ("0,2178", "0,3745", "0,6481")),
        (("marge nette d'intérêt (Π^Bk/actif), %", "marge_nette", 1, _NU, ", ν_G = 1,15"),
         ("2,540", "2,414", "2,204")),
        (("marge nette d'intérêt (Π^Bk/actif), %", "marge_nette", 1, 1.0, ", ν_G = 1"), ("2,546", "2,421", "2,212")),
        (("marge d'existence, par an", "existence", 1, _NU, ""), ("0,0296", "0,0328", "0,0455")),
        (("canal rentier, % de YD par point", "canal_rentier", 1, _NU, ""), ("0,313", "0,531", "0,828")),
    )
    for pi, pub in zip(POINTS_PI, pubs, strict=True)
) + tuple(
    ("sec:banque-stationnaire",
     f"rendement des fonds propres (brut, nominal, sans charges), variante basse, {round(100 * pi)} %, %", pub,
     (lambda c, pi=pi: c.banque(pi=pi, nu=_NU, varpi_L=0.004, varpi_D=0.00214)["roe"]), "B-2")
    for pi, pub in zip(POINTS_PI, ("5,24", "7,71", "17,51"), strict=True)
) + tuple(
    ("sec:banque-stationnaire", f"part distribuée à 2 %, n_a = {na}", pub,
     (lambda c, na=na: c.banque(na=na, nu=_NU)["part_distribuee"]), "B-2")
    for na, pub in zip(POINTS_NA, ("0,845815", "0,846271", "0,846445"), strict=True)
) + (
    ("sec:banque-stationnaire", "multiplicateur du refinancement à ν_G = 1,15, 2 %", "1,1504",
     lambda c: c.v(nu=_NU)["multiplicateur_nu"], "A"),
    ("sec:banque-stationnaire", "a = i_CB/(Γ̄ n_a) à 2 %", "0,0025084", lambda c: c.v(nu=_NU)["a"], "A"),
    ("sec:banque-stationnaire", "richesse des ménages à 2 %", "0,7165", lambda c: c.v(nu=_NU)["decomp_v_H"], "A"),
    ("sec:banque-stationnaire", "titres de 2 à 10 %, ν_G = 1,15", "0,24527",
     lambda c: c.banque(pi=0.10, nu=_NU)["b_Bk"] - c.banque(nu=_NU)["b_Bk"], "B-2"),
    ("sec:banque-stationnaire", "titres de 2 à 10 %, ν_G = 1", "0,24457",
     lambda c: c.banque(pi=0.10, nu=1.0)["b_Bk"] - c.banque(nu=1.0)["b_Bk"], "B-2"),
    ("sec:banque-stationnaire", "dette consolidée de 2 à 10 %", "0,24009",
     lambda c: c.banque(pi=0.10, nu=_NU)["c"] - c.banque(nu=_NU)["c"], "B-2"),
    ("sec:banque-stationnaire", "dont entreprises (d_F − l), 2 à 10 %", "0,2865",
     lambda c: ((c.banque(pi=0.10, nu=_NU)["d_F"] - c.banque(pi=0.10, nu=_NU)["l"])
                - (c.banque(nu=_NU)["d_F"] - c.banque(nu=_NU)["l"])), "B-2"),
    ("sec:banque-stationnaire", "dont fonds propres (ϑ Δl), 2 à 10 %", "-0,0431",
     lambda c: c.banque(pi=0.10, nu=_NU)["e_Bk"] - c.banque(nu=_NU)["e_Bk"], "B-2"),
    ("sec:banque-stationnaire", "dont richesse des ménages, 2 à 10 %", "-0,0033",
     lambda c: c.v(pi=0.10, nu=_NU)["decomp_v_H"] - c.v(nu=_NU)["decomp_v_H"], "A"),
    ("sec:banque-stationnaire", "encaisse de 2 à 10 %, ν_G = 1,15", "0,0052",
     lambda c: c.v(pi=0.10, nu=_NU)["encaisse"] - c.v(nu=_NU)["encaisse"], "A"),
    ("sec:banque-stationnaire", "encaisse de 2 à 10 %, ν_G = 1", "0,0045",
     lambda c: c.v(pi=0.10)["encaisse"] - c.v()["encaisse"], "A"),
    ("sec:banque-stationnaire", "part des intérêts des dépôts, 2 %, %", "202,7",
     lambda c: c.banque(nu=_NU)["part_v_H"], "B-2"),
    ("sec:banque-stationnaire", "part des dividendes des entreprises, 2 %, %", "-129,1",
     lambda c: c.banque(nu=_NU)["part_entreprises"], "B-2"),
    ("sec:banque-stationnaire", "part du dividende de la banque, 2 %, %", "26,4",
     lambda c: c.banque(nu=_NU)["part_E_Bk"], "B-2"),
    ("sec:banque-resultat", "saut C29 au tour n, 2 %, %", "14,67", lambda c: c.banque(nu=_NU)["saut_C29"], "B-2"),
    ("sec:banque-resultat", "saut C29 ensuite, 2 %, %", "3,88", lambda c: c.banque(nu=_NU)["saut_C29_suite"],
     "B-2"),
    ("sec:banque-conditions", "(d2), 2 %, point", "1,23", lambda c: c.banque(nu=_NU)["d2"], "B-2"),
) + tuple(
    ("sec:banque-restitution", f"{nom} restitué(e) à {round(100 * pi)} %", pub,
     (lambda c, pi=pi, cle=cle: _restitue(c, pi, c.banque(pi=pi, nu=_NU)[cle])), "B-2")
    for (nom, cle), pubs in (
        (("masse monétaire", "M"), ("0,90174", "0,93448")),
        (("refinancement", "refinancement"), ("0,02262", "0,02906")),
        (("titres de la banque", "b_Bk"), ("0,38376", "0,66049")),
    )
    for pi, pub in zip((0.02, 0.10), pubs, strict=True)
) + tuple(
    ("sec:banque_centrale-restitution", f"résultat de la banque centrale à {round(100 * pi)} %{suffixe}, % du PIB",
     pub, (lambda c, pi=pi, nu=nu: c.v(pi=pi, nu=nu)["Pi_CB"]), "A")
    for nu, suffixe, pubs in ((_NU, ", ν_G = 1,15", ("0,0212", "0,0669", "0,3032")),
                              (1.0, ", ν_G = 1", ("0,0185", "0,0581", "0,2633")))
    for pi, pub in zip(POINTS_PI, pubs, strict=True)
) + tuple(
    ("sec:banque_centrale-restitution", f"refinancement restitué à {round(100 * pi)} %", pub,
     (lambda c, pi=pi: _restitue(c, pi, c.v(pi=pi, nu=_NU)["refinancement"])), "A")
    for pi, pub in zip(POINTS_PI, ("0,02147", "0,02262", "0,02906"), strict=True)
) + (
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̄ à 0 %, point par point", "-0,151",
     lambda c: sensibilite_fermeture(c.par(pi=0.0, nu=c.nu_g_retenu))["dtheta_G_dr"], "A"),
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̄ à 10 %, point par point", "-0,488",
     lambda c: sensibilite_fermeture(c.par(pi=0.10, nu=c.nu_g_retenu))["dtheta_G_dr"], "A"),
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̂, norme et i^ref tenus, φ = 1, ζ = 4, point par point", "0,160",
     lambda c: _derivee_norme_tenue(c, 1.0, 4.0), "A"),
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̂, norme et i^ref tenus, φ = 1, ζ = 8, point par point", "0,320",
     lambda c: _derivee_norme_tenue(c, 1.0, 8.0), "A"),
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̂, norme et i^ref tenus, φ = 0, ζ = 4, point par point", "-0,107",
     lambda c: _derivee_norme_tenue(c, 0.0, 4.0), "A"),
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̂, norme et i^ref tenus, φ = 0, ζ = 8, point par point", "0,053",
     lambda c: _derivee_norme_tenue(c, 0.0, 8.0), "A"),
    ("sec:banque_centrale-stationnaire", "θ_G(r̄ + 1 point) − θ_G(r̄), norme et i^ref tenus, φ = 1, ζ = 4, point",
     "+0,157", lambda c: _hausse_d_un_point(c, 1.0, 4.0), "A"),
    ("sec:banque_centrale-stationnaire", "θ_G(r̄ + 1 point) − θ_G(r̄), norme et i^ref tenus, φ = 1, ζ = 8, point",
     "+0,308", lambda c: _hausse_d_un_point(c, 1.0, 8.0), "A"),
    ("sec:banque_centrale-stationnaire", "θ_G(r̄ + 1 point) − θ_G(r̄), norme et i^ref tenus, φ = 0, ζ = 4, point",
     "-0,131", lambda c: _hausse_d_un_point(c, 0.0, 4.0), "A"),
    ("sec:banque_centrale-stationnaire", "θ_G(r̄ + 1 point) − θ_G(r̄), norme et i^ref tenus, φ = 0, ζ = 8, point",
     "0,001", lambda c: _hausse_d_un_point(c, 0.0, 8.0), "A"),
    ("sec:banque_centrale-stationnaire", "L^CB_0 à 2 %, ν_G = 1,15, u.m.", "0,252554",
     lambda c: ouverture(c.etat(nu=_NU), c.par(nu=_NU))["L_CB"], "A"),
    ("sec:banque_centrale-conditions", "Δr̄_α, verdict (ζ = 8), point", "0,278",
     lambda c: 100 * c.alpha()["delta_r_alpha"], "D"),
    ("sec:banque_centrale-conditions", "(α) : écart de C/Y_o, point", "0,854",
     lambda c: 100 * c.alpha()["allocations"]["C/Y_o"], "D"),
    ("sec:banque_centrale-conditions", "(α) : écart de ti, point", "0,257",
     lambda c: 100 * c.alpha()["allocations"]["ti"], "D"),
    ("sec:banque_centrale-conditions", "(α) : écart de tu, point", "2,003",
     lambda c: 100 * c.alpha()["allocations"]["tu"], "D"),
    ("sec:banque_centrale-conditions", "Δr̄_α à ζ = 2, point", "1,197", lambda c: _delta_r_alpha(c, 2.0), "D"),
    ("sec:banque_centrale-conditions", "Δr̄_α à ζ = 8, point", "0,278", lambda c: _delta_r_alpha(c, 8.0), "D"),
    ("sec:banque_centrale-conditions", "Δr̄_α à ζ = 68, point", "0,1614", lambda c: _delta_r_alpha(c, 68.0), "D"),
    ("sec:banque_centrale-conditions", "Δr̄_α au minimum en ζ sur [2 ; 200], point", "0,1598",
     lambda c: minimum_delta_r_alpha_en_zeta(c)[1], "D"),
    ("sec:banque_centrale-conditions", "marche de cible de 2 à 3 % à ζ = 2, point", "-0,33",
     lambda c: 100 * (c.r_alpha(0.03, 2.0) - c.r_alpha(0.02, 2.0)), "D"),
    ("sec:banque_centrale-conditions", "marche de cible de 2 à 3 % à ζ = 8, point", "-0,07",
     lambda c: 100 * (c.r_alpha(0.03, 8.0) - c.r_alpha(0.02, 8.0)), "D"),
    ("sec:banque_centrale-conditions", "canal des écarts nominaux sur r̄_α(10 %) − r̄_α(0), point", "0,182",
     lambda c: _canal_ecarts_nominaux(c, 4.0), "D"),
    ("sec:banque_centrale-conditions ; fiche 8 § 9.6", "r̄_α(3 %) à ζ = 4, %", "0,8451",
     lambda c: 100 * c.r_alpha(0.03, 4.0), "D"),
    ("fiche 8 § 9.6", "r̄_α(3 %) à ζ = 8, %", "0,9320", lambda c: 100 * c.r_alpha(0.03, 8.0), "D"),
) + tuple(
    ("sec:finances_publiques-stationnaire", f"{nom} à {round(100 * pi)} %, ν_G = 1,15{unite}", pub,
     (lambda c, pi=pi, cle=cle: c.v(pi=pi, nu=_NU)[cle]), "A")
    for (nom, cle, unite), pubs in (
        (("dette brute", "dette_brute", ""), ("0,22568", "0,37564", "0,62091")),
        (("intérêts bruts", "interets_bruts", ", % du PIB"), ("0,2257", "1,1344", "6,8921")),
        (("encaisse", "encaisse", ""), ("0,021242", "0,022141", "0,027318")),
    )
    for pi, pub in zip(POINTS_PI, pubs, strict=True)
) + (
    ("sec:finances_publiques-transferts", "charge brute à 2 %, ν_G = 1,15, % du PIB", "1,13",
     lambda c: c.v(nu=_NU)["interets_bruts"], "A"),
    ("sec:finances_publiques-restitution", "dette brute affichée à 2 %, ν_G = 1,15, % du PIB", "38,4",
     lambda c: c.v(nu=_NU)["dette_brute_affichee"], "A"),
    ("sec:finances_publiques-restitution", "dette brute affichée à 10 %, ν_G = 1,15, % du PIB", "66,0",
     lambda c: c.v(pi=0.10, nu=_NU)["dette_brute_affichee"], "A"),
    ("sec:finances_publiques-restitution", "charge brute à 2 %, ν_G = 1,15, % du PIB", "1,1344",
     lambda c: c.v(nu=_NU)["interets_bruts"], "A"),
    ("sec:finances_publiques-restitution", "charge brute à 10 %, ν_G = 1,15, % du PIB", "6,8921",
     lambda c: c.v(pi=0.10, nu=_NU)["interets_bruts"], "A"),
) + tuple(
    ("sec:finances_publiques-emission", f"ν_G,min exact à {round(100 * pi)} %", pub,
     (lambda c, pi=pi: c.v(pi=pi, nu=_NU)["nu_G_min"]), "A")
    for pi, pub in zip(POINTS_PI, ("1,0907", "1,0499", "0,8470"), strict=True)
) + tuple(
    ("sec:finances_publiques-emission", f"hausse admissible à {round(100 * pi)} %, ν_G = 1,15, %", pub,
     (lambda c, pi=pi: c.v(pi=pi, nu=_NU)["hausse_admissible"]), "A")
    for pi, pub in zip(POINTS_PI, ("15,99", "20,52", "49,77"), strict=True)
) + (
    ("sec:finances_publiques-emission", "ν_G,min au pire point (n_a = 4, 0 %)", "1,0923",
     lambda c: c.v(pi=0.0, na=4, nu=_NU)["nu_G_min"], "A"),
    ("sec:finances_publiques-emission ; tab:calibration", "ν_G minimal pour la marge J-ν (n_a = 4, 0 %)",
     "1,1260", lambda c: c.v(pi=0.0, na=4, nu=_NU)["nu_G_J"], "A"),
    ("sec:finances_publiques-emission", "marge J-ν au pire point à ν_G = 1,1, %", "0,70",
     lambda c: 100 * c.v(pi=0.0, na=4, nu=1.1)["marge_J_nu"], "A"),
    ("sec:finances_publiques-emission ; tab:calibration", "marge J-ν au pire point à ν_G = 1,15", "0,0503",
     lambda c: c.v(pi=0.0, na=4, nu=_NU)["marge_J_nu"], "A"),
) + tuple(
    ("fiche 9 § 3.C ; § 9.6", f"dette consolidée à {round(100 * pi)} %, n_a = {na}", pub,
     (lambda c, pi=pi, na=na: c.v(pi=pi, na=na, nu=_NU)["dette_consolidee"]), "A")
    for (pi, na), pub in (((0.0, 4), "0,20440"), ((0.10, 4), "0,59499"), ((0.0, 52), "0,20446"),
                          ((0.10, 52), "0,59305"))
) + tuple(
    ("tab:etat-stationnaire", f"{nom} à {round(100 * pi)} %", pub,
     (lambda c, pi=pi, cle=cle, nu=nu: c.v(pi=pi, nu=nu)[cle]), "A")
    for nom, cle, nu, _, pubs in _TAB_ETAT
    for pi, pub in zip(POINTS_PI, pubs, strict=True)
)
# Rattachement des valeurs publiées dans un tableau de la spécification (constat mi-1 de l'audit) : (section,
# description) → (libellé de la ligne, première cellule écrite dans la source ; colonne de la valeur, comptée depuis
# 0, ou None si la valeur figure dans le texte d'une cellule de la ligne). Lu par le test de source.
LIGNES_DE_TABLEAU: dict[tuple[str, str], tuple[str, int | None]] = {
    ("tab:etat-stationnaire", f"{nom} à {round(100 * pi)} %"): (ligne, 3 + j)
    for nom, _, _, ligne, _ in _TAB_ETAT for j, pi in enumerate(POINTS_PI)
} | {
    ("sec:finances_publiques-emission ; tab:calibration", description): ("$\\nu_G$", None)
    for description in ("marge J-ν à ν_G = 1,1, 0 %, %", "ν_G minimal pour la marge J-ν (n_a = 4, 0 %)",
                        "marge J-ν au pire point à ν_G = 1,15")
}
# Rattachement des valeurs publiées à leur passage de source hors tableau de la spécification (#93, point 1) :
# (section, description, source) → fragments, chacun écrit dans une seule ligne de la source hors barre (paragraphe,
# élément de liste ou ligne de tableau Markdown, écrits sur une ligne). La valeur se lit dans chaque fragment qui la
# contient au signe près, sinon dans sa ligne. Source : label de la spécification ou fiche telle que le test de source
# la nomme (« fiche 8 », « fiche 9 », « banque_centrale.md »). Toute valeur lue dans une fiche y est rattachée ; dans
# la spécification, seulement là où la source entière lirait la valeur ailleurs, signe inversé compris.
_FICHE_9_DETTE = "| **J1 (n° 4 bis, P16 (a))** | **Ratio dette/PIB stationnaire"
PARAGRAPHES_DE_SOURCE: dict[tuple[str, str, str], tuple[str, ...]] = {
    ("sec:production-capital", "ρ̄_K à 0 %", "sec:production-capital"): ("soit 1 pour $\\bar\\pi = 0$",),
} | {
    ("docs/blocs/banque_centrale.md § 2, critère 13 (b)", f"{nom} à {pi} %, %", "banque_centrale.md"):
        ("| 13 | Superneutralité (C15",)
    for nom in ("taux réel exact", "taux réel Haig-Simons (sur i_CB)") for pi in ("0", "2", "10")
} | {
    ("sec:banque_centrale-conditions ; fiche 8 § 9.6", "r̄_α(3 %) à ζ = 4, %", "fiche 8"):
        ("| J3 | Cible relevée (critère 10 (b) (i))",),
    ("fiche 8 § 9.6", "r̄_α(3 %) à ζ = 8, %", "fiche 8"): ("| J3 | Cible relevée (critère 10 (b) (i))",),
} | {
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", f"r̄_α à π* = {pi} %, %", "fiche 9"):
        ("- profil C-HS tel quel, r̄ à π\\* = 0 / 1 / 2 / 3 / 4 / 6 / 10 %",)
    for pi in ("0", "1", "2", "3", "4", "6", "10")
} | {
    ("fiche 9 § 6.3", "(β) : écart de θ_G entre 0, 2 et 10 %, point", "fiche 9"): ("La lecture (β) échoue aussi",),
    ("fiche 9 § 3.C", "(α) : C/PIB à 0 % moins à 2 %, point", "fiche 9"): ("| Critère 13 : écart de C/PIB à 0 / 10 %",),
    ("fiche 9 § 3.C", "(α) : C/PIB à 10 % moins à 2 %, point", "fiche 9"):
        ("| Critère 13 : écart de C/PIB à 0 / 10 %",),
    ("fiche 9 § 6.3", "(α) : max − min de C/PIB, point", "fiche 9"): ("Celui de C/PIB vaut",),
} | {
    ("fiche 9 § 3.C ; § 9.6", f"dette consolidée à {pi} %, n_a = {na}", "fiche 9"): (ligne, _FICHE_9_DETTE)
    for na, ligne in ((4, "| Dette consolidée (B − M^G)/(n_a PIB) | 4 |"), (52, "| | 52 |")) for pi in ("0", "10")
}


# Historique : valeurs publiées avant le visa du 05/10/2026 (commit 9c8bdbd), toutes en écart, visées puis
# republiées (spécification, commit 8b9fa94 ; annotations de la fiche 9). L'ancien verdict reste publié. Clé :
# (section, description) de `VALEURS_PUBLIEES` ; valeur : l'ancienne valeur
# publiée (même fonction, même catégorie), ou l'entrée complète si la grandeur publiée a changé (|·|, catégorie C).
_AVANT_VISA: dict[tuple[str, str], object] = {
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, n_a = 4"): "0,25237",
    ("sec:finances_publiques-stationnaire", "dette consolidée à 2 %, n_a = 52"): "0,25844",
    ("sec:finances_publiques-stationnaire", "Y^HS/PIB à 2 %"): "0,8672",
    ("sec:finances_publiques-depense", "G/PB à 2 %"): "0,96343",
    ("sec:finances_publiques-depense", "G/PB à 10 %"): "0,78639",
    ("sec:finances_publiques-depense", "marge de E1 à 10 %"): "0,2060",
    ("sec:finances_publiques-emission", "borne de ν_G à 10 %"): "0,8734",
    ("sec:finances_publiques-emission ; tab:calibration", "marge J-ν à ν_G = 1,1, 0 %, %"): "0,37",
    ("sec:banque_centrale-stationnaire", "dθ_G/dr̄, % de la production par point de r̄"):
        ("sec:banque_centrale-stationnaire", "sensibilité de θ_G, % de la production par point de r̄ (|dθ_G/dr̄|)",
         "0,026", lambda c: abs(c.fermeture()["dtheta_G_dr"]), "C"),
    ("sec:banque_centrale-stationnaire", "points de r̄ par point de PIB de dépense"):
        ("sec:banque_centrale-stationnaire", "points de r̄ par point de PIB de dépense (|·|), environ", "38",
         lambda c: abs(c.fermeture()["points_r_par_point_PIB"]), "C"),
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 0 %, %"): "1,536",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 1 %, %"): "1,203",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 3 %, %"): "0,878",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 4 %, %"): "0,813",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 6 %, %"): "0,799",
    ("sec:banque_centrale-conditions ; fiche 9 § 3.Q", "r̄_α à π* = 10 %, %"): "1,075",
    ("sec:banque_centrale-conditions", "r̄_α(0) − r̄_α(10 %), point"): "0,461",
    ("sec:banque_centrale-conditions", "écart maximal de r̄_α sur le profil, point"): "0,74",
    ("sec:banque_centrale-conditions", "marche de cible de 2 à 3 %, point"): "-0,12",
    ("sec:finances_publiques-impots", "racine parasite à 0 %, %"): "-20,63",
    ("sec:finances_publiques-impots", "racine parasite à 2 %, %"): "-26,65",
    ("sec:finances_publiques-impots", "racine parasite à 10 %, %"): "-40,49",
    ("fiche 9 § 3.C", "(α) : C/PIB à 0 % moins à 2 %, point"): "0,435",
    ("fiche 9 § 3.C", "(α) : C/PIB à 10 % moins à 2 %, point"): "-0,473",
    # Libellé corrigé le 14/10/2026 (« fiche 9 § 3.C » → « fiche 9 § 6.3 »), décision du mainteneur ; valeur et
    # verdict inchangés.
    ("fiche 9 § 6.3", "(α) : max − min de C/PIB, point"): "0,908",
    # Fiche 9, § 3.C et critère 5 du § 9.6 : visées après la revue finale (décision du mainteneur du 05/10/2026,
    # point B), même cause que les deux écarts à 2 %.
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 0 %, n_a = 4"): "0,09466",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 10 %, n_a = 4"): "0,49978",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 0 %, n_a = 52"): "0,10045",
    ("fiche 9 § 3.C ; § 9.6", "dette consolidée à 10 %, n_a = 52"): "0,51438",
}
VALEURS_AVANT_VISA: tuple[tuple[str, str, str, object, str], ...] = tuple(
    (section, description, ancienne, fonction, categorie) if isinstance(ancienne, str) else ancienne
    for section, description, _, fonction, categorie in VALEURS_PUBLIEES
    if (ancienne := _AVANT_VISA.get((section, description))) is not None
)


def decimales(publie: str) -> int:
    """Nombre de décimales d'une valeur publiée écrite à la française (« 0,25674 » → 5)."""
    return len(publie.split(",")[1]) if "," in publie else 0


def comparer(publie: str, script: float) -> tuple[float, float, bool]:
    """Écart et seuil « dernière décimale publiée » : arrondi au plus proche (décision du 05/10/2026, point 2)."""
    x_pub = float(publie.replace(",", ".").replace("−", "-"))
    seuil = 0.5 * 10 ** (-decimales(publie)) + 1e-12
    ecart = script - x_pub
    return ecart, seuil, (not math.isnan(script)) and abs(ecart) <= seuil


def table_publiees(calc: Calculs, liste: tuple = VALEURS_PUBLIEES,
                   explications: dict[tuple[str, str], str] | None = None) -> list[dict[str, object]]:
    """Comparaison de chaque valeur publiée de `liste` à sa valeur de script ; `explications` nomme les écarts.

    Par défaut, les valeurs publiées en vigueur ; `table_historique` compare les valeurs d'avant le visa.
    """
    lignes = []
    for section, description, publie, fonction, categorie in liste:
        try:
            script = float(fonction(calc))
        except ReferenceNonPubliee as constat:  # la valeur lit un point de référence non publié (option (b))
            lignes.append({"section": section, "grandeur": description, "publie": publie, "script": math.nan,
                           "ecart": math.nan, "seuil": 0.0 if publie == AUCUNE else comparer(publie, 0.0)[1],
                           "verdict": "non publiée", "categorie": categorie, "libelle": str(constat),
                           "explication": ""})
            continue
        except MinimumNonEncadre as refus:  # minimum de Δr̄_α en ζ non encadré (#173) : refus publié, motif à l'appui
            lignes.append({"section": section, "grandeur": description, "publie": publie, "script": math.nan,
                           "ecart": math.nan, "seuil": 0.0 if publie == AUCUNE else comparer(publie, 0.0)[1],
                           "verdict": "refusée", "categorie": categorie, "libelle": f"refus ({refus.motif})",
                           "explication": ""})
            continue
        if publie == AUCUNE:
            ecart, seuil, ok = math.nan, 0.0, math.isnan(script)
        else:
            ecart, seuil, ok = comparer(publie, script)
        if ok:
            explication = ""
        elif categorie == "C":
            explication = f"écrite avant l'essai : {EXPL_C}"
        else:
            explication = (explications or {}).get((section, description), "")
        lignes.append({"section": section, "grandeur": description, "publie": publie, "script": script,
                       "ecart": ecart, "seuil": seuil, "verdict": "égal" if ok else "écart", "categorie": categorie,
                       "libelle": "aucune" if (math.isnan(script) and description in SANS_RACINE) else "",
                       "explication": explication})
    return lignes


def table_historique(calc: Calculs) -> list[dict[str, object]]:
    """Ancien verdict : valeurs publiées avant le visa du 05/10/2026 (commit 9c8bdbd) contre le script."""
    return table_publiees(calc, VALEURS_AVANT_VISA, EXPLICATIONS_ECARTS)


# --- Contrôles par point de grille ---------------------------------------------------


def controles(e: dict[str, float], par: Parametres) -> dict[str, object]:
    """Résidus des règles, matrices, routes doubles et identités du point (propriétés P2, P3, 6 et 7)."""
    s = un_pas(ouverture(e, par), par)
    res = residus_des_regles(e, s, par)
    mat = matrices(e, s, par)
    rd = routes_doubles(e, s, par)
    n = par.n_a
    A = n * e["PIB"]
    identites = {
        "C42 : D_c = V_H − (L − D_F) + E^Bk (route bilans : −V_G)":
            abs((e["B"] - e["M_G"] - e["E_CB"]) - (e["V_H"] - e["L"] + e["D_F"] + e["E_Bk"])) / A,
        "Domar : calcul (i) contre (ii)":
            abs(n * e["gam"] * e["D_c"] / A
                - (e["G"] + e["Tr"] + e["interets"] - e["T_H"] - e["T_F"] - e["Pi_CB"]) / e["PIB"]),
        "Walras : Em (E9) = γ̄ B": abs(e["Em"] - e["gam"] * e["B"]) / A,
        "solde primaire stabilisant = solde primaire réalisé":
            abs((e["i_CB"] / n - e["gam"]) * e["D_c"] - (e["T_H"] + e["T_F"] - e["G"] - e["Tr"])) / e["PIB"],
        "épargne : 1 − C/YD = γ̄ V_H/YD": abs((1 - e["C"] / e["YD"]) - e["gam"] * e["V_H"] / e["YD"]),
        "part salariale : forme fermée":
            abs(e["WB"] / e["PIB"] - e["y_sur_v"] / ((1 + par.mu_bar) + e["gam"] * e["rho_IN"] * n * par.sigma)),
        "i_CB = (1 + r̄)(1 + π*) − 1": abs(s["i_CB"] - ((1 + e["r_neutre"]) * (1 + par.pi_cible) - 1)),
        "T^cou = 0 (lecture (e))": abs(e["T_cou"]) / e["PIB"],
        "Res · L^CB = 0": min(abs(e["Res"]), abs(e["L_CB"])) / echelle_CB(e),
        "E^Bk = ϑ L": abs(e["E_Bk"] - par.vartheta * e["L"]) / A,
    }
    return {"residus_regles": res, "matrices": mat, "routes_doubles": rd, "identites": identites, "pas": s}


def max_controles(c: dict[str, object]) -> dict[str, float]:
    """Plus grand résidu de chaque famille de contrôles du point."""
    m = c["matrices"]
    return {
        "règles (P2)": max(c["residus_regles"].values()),
        "matrice des bilans, lignes et colonnes":
            max(max(m["lignes_bilans"].values()), max(m["colonnes_bilans"].values())),
        "matrice des flux, lignes": max(m["lignes_flux"].values()),
        "matrice des flux, colonnes de secteur": max(m["secteurs_flux"].values()),
        "valeurs nettes, stock contre flux": max(m["valeurs_nettes"].values()),
        "somme des valeurs nettes = K + IN": m["somme_valeurs_nettes"],
        "routes doubles": max(c["routes_doubles"].values()),
        "identités": max(c["identites"].values()),
    }


# --- Calcul complet et restitution ---------------------------------------------------


def plus_grand_residu(r: dict[str, object]) -> float:
    """Plus grand résidu de toute la grille (règles, matrices, routes doubles, identités) ; NaN compte comme échec."""
    valeurs_ = [v for c in r["controles"].values() for v in c.values()]
    return math.inf if any(math.isnan(v) for v in valeurs_) else max(valeurs_)


def nu_g_mesure(nu_g_retenu: float | None) -> float:
    """ν_G de la fermeture, de la mesure de #80 et du relevé : la valeur retenue, `NU_G_RETENU` si elle vaut None
    (colonne retirée).

    La valeur 1 est refusée : elle dupliquerait la colonne du point de référence.
    """
    if nu_g_retenu == 1.0:
        raise HorsDomaine("ν_G retenu = 1 : la colonne ν_G = 1 est déjà le point de référence de la grille")
    return NU_G_RETENU if nu_g_retenu is None else nu_g_retenu


def calculer(base: Parametres, nu_g_retenu: float | None = NU_G_RETENU) -> dict[str, object]:
    """Calcule la grille, les contrôles, la fermeture et la mesure de #80 de la table `base`.

    `nu_g_retenu` : troisième colonne ν_G (1,15 par défaut, décision du 05/10/2026) ; None la retire. La valeur 1
    est refusée : elle dupliquerait la colonne du point de référence.

    La comparaison aux valeurs publiées (relevé, historique, contre-épreuve) n'est pas calculée ici : elle porte sur
    la table de référence seule (`publier`, #185, option (a) de P313), et une variante de `base` n'y est pas soumise.

    Les colonnes de la table (ν_G > 1) sont calculées d'abord, la colonne de référence ν_G = 1 ensuite : un refus
    porte le nom de la colonne et du point où il survient. Sur la colonne de référence, un plafond de E1 actif
    n'est pas un refus : le point est publié comme constat déclaré (`reference_hors_domaine`, marge relative),
    sans valeur d'état ni résidu (décision de `macro`, option (b)) ; les autres refus y restent bloquants.

    L'état initial résolu (`niveaux`, niveaux d'ouverture du pas 0) est publié pour chaque colonne : d'abord à
    ν_G retenu, l'état que lira `scenarios/` (M^G_0, B_0, L^CB_0, B_Bk,0 et Π^CB dépendent de ν_G), puis au point
    de référence ν_G = 1. La fermeture et la mesure de #80 sont calculées à ν_G retenu, `NU_G_RETENU` si
    `nu_g_retenu` vaut None (voir `Calculs` et `nu_g_mesure`).
    """
    declares = controler_domaine(base)
    calc = Calculs(base, nu_g_mesure(nu_g_retenu))
    points = [(pi, na) for pi in POINTS_PI for na in POINTS_NA]
    nus = ([nu_g_retenu] if nu_g_retenu is not None else []) + [1.0]
    grille, ctrl, niveaux, hors_reference = {}, {}, {}, {}
    for nu in nus:
        controler_domaine(replace(base, nu_G=nu))
        for pi, na in points:
            try:
                e = calc.etat(pi, na, nu)
            except ReferenceNonPubliee as constat:
                hors_reference[(pi, na)] = constat.marge
                continue
            except HorsDomaine as refus:
                raise HorsDomaine(f"colonne ν_G = {nu!r}, π̄ = {pi!r}, n_a = {na} : {refus}") from refus
            p = calc.par(pi, na, nu)
            grille[(nu, pi, na)] = calc.v(pi, na, nu)
            ctrl[(nu, pi, na)] = max_controles(controles(e, p))
            o = ouverture(e, p)  # état initial résolu : niveaux d'ouverture du pas 0 de chaque colonne
            niveaux[(nu, pi, na)] = {k: v for k, v in o.items() if k != "registre"} | {
                "P_m1": o["registre"][0], f"P_m{na + 1}": o["registre"][-1], "theta_G": e["theta_G"],
                "y_0": e["y"], "v_0": e["v"], "N_0": e["N"], "W_0": e["W"], "YD_0": e["YD"], "T_F_0": e["T_F"],
                "B_0": e["B"], "Pi_CB": e["Pi_CB"], "i_CB_0": e["i_CB"], "T_cou_0": e["T_cou"],
                "mu_tilde_0": math.log(1 + base.mu_bar)}
    propositions = {}
    for nu in sorted(set(NU_G_PROPOSES) | ({nu_g_retenu} if nu_g_retenu is not None else set())):
        for pi, na in points:
            try:
                propositions[(nu, pi, na)] = calc.v(pi, na, nu)["marge_J_nu"]
            except HorsDomaine as refus:
                raise HorsDomaine(f"colonne ν_G = {nu!r}, π̄ = {pi!r}, n_a = {na} : {refus}") from refus
    republication = {}
    for nu in nus:
        for pi in POINTS_PI:
            if not (nu == 1.0 and (pi, 12) in hors_reference):
                republication[(nu, pi)] = calc.banque(pi=pi, nu=nu)
    return {
        "parametres": base, "declares": declares, "nu_g_retenu": nu_g_retenu, "grille": grille, "controles": ctrl,
        "reference_hors_domaine": hors_reference,
        "niveaux": niveaux, "propositions": propositions, "republication": republication,
        "fermeture": calc.fermeture(), "superneutralite": calc.alpha(),
        "cf": {pi: calc.v(pi, 12, 1.0, "C-F") for pi in POINTS_PI},
    }


def publier(nu_g_retenu: float | None = NU_G_RETENU) -> dict[str, object]:
    """Relevé des valeurs publiées en vigueur, historique et contre-épreuve, sur la table de référence `Parametres()`.

    Les valeurs publiées sont celles de la table de référence : la fonction ne prend pas de table en argument, et une
    variante ne peut pas y être soumise (#185, option (a) de P313). La contre-épreuve lit `ENTREES_D_ORIGINE` sur
    cette même table. `nu_g_retenu` : comme pour `calculer` (ν_G de la mesure de #80 et de la fermeture).
    """
    calc = Calculs(Parametres(), nu_g_mesure(nu_g_retenu))
    return {
        "publiees": table_publiees(calc), "historique": table_historique(calc),
        "contre_epreuve": table_publiees(Calculs(replace(calc.base, **ENTREES_D_ORIGINE), calc.nu_g_retenu),
                                         VALEURS_CONTRE_EPREUVE),
    }


def _f(x: float, chiffres: int = 10) -> str:
    """Format déterministe d'un nombre (chiffres significatifs, point décimal) ; NaN se lit « sans objet »."""
    if isinstance(x, float) and math.isnan(x):
        return "sans objet"
    if isinstance(x, float) and math.isinf(x):
        return str(x)
    return f"{x:.{chiffres}g}"


def _rang_nu(nu: float) -> tuple[bool, float]:
    """Ordre de publication des colonnes ν_G : valeurs de la table (ν_G > 1) d'abord, référence ν_G = 1 en dernier."""
    return (nu == 1.0, nu)


def _titre_nu(nu: float) -> str:
    """Titre d'une colonne ν_G à la publication."""
    if nu == 1.0:
        return "ν_G = 1 (référence hors domaine : point de référence de la forme fermée, jamais valeur de table)"
    return f"ν_G = {_f(nu)} (valeur retenue)"


SANS_OBJET_NON_FINI = "sans objet (valeur non finie)"  # verdict du rendu sur une mesure non finie (#188)


def _verdict_seuil(valeurs, seuil: float, tenu: str = "tenu", non_tenu: str = "non tenu (défaut connu, #80)") -> str:
    """Verdict « max(valeurs) ≤ seuil » du rendu ; « sans objet (valeur non finie) » dès qu'une valeur n'est pas
    finie (#188) : une comparaison à NaN est fausse et rendrait « non tenu », et `max` ignore un NaN hors de tête."""
    valeurs = list(valeurs)
    if not all(math.isfinite(v) for v in valeurs):
        return SANS_OBJET_NON_FINI
    return tenu if max(valeurs) <= seuil else non_tenu


def afficher(r: dict[str, object], sortie=None) -> None:
    """Publie la grille complète, les contrôles et la comparaison aux valeurs publiées (texte déterministe).

    La comparaison (relevé, historique, contre-épreuve) n'est imprimée que si `r` porte le résultat de `publier` :
    un résultat de `calculer` seul (variante de la table) s'arrête à la configuration de contrôle C-F.
    """
    out = sortie or sys.stdout

    def p(texte: str = "") -> None:
        print(texte, file=out)

    base = r["parametres"]
    p("# État stationnaire du socle sous forme fermée (issue #84)")
    p()
    p("## Paramètres (configuration R ; unité ; source ; équation)")
    for champ in fields(base):
        unite, source, eq = DECLARATIONS[champ.name]
        p(f"- {champ.name} = {_f(getattr(base, champ.name))} ; {unite} ; {source} ; {eq}")
    p(f"- tolérances : identités {TOL_IDENTITE:g} × S ; tol_F = {TOL_F:g} ; bissection {LARGEUR_BISSECTION:g}, "
      f"au plus {ITERATIONS_MAX} itérations")
    for d in r["declares"]:
        p(f"- point déclaré : {d}")
    hors = r["reference_hors_domaine"]
    for (pi, na), marge in sorted(hors.items()):
        p(f"- point déclaré : ν_G = 1, π̄ = {_f(100 * pi)} %, n_a = {na} : {constat_reference(marge)}")
    p()
    p("Normalisation : p_0 = 1 u.m./u.v., pr_0 = 1 u.v. par personne et par pas, N^pa_0 = 1 personne ; "
      "« ouverture » = stock d'ouverture du pas 0 ; « pas » = flux du pas 0, égal au rapport sur 12 tours.")
    entetes = [(pi, na) for pi in POINTS_PI for na in POINTS_NA]

    def grille(nu: float) -> None:
        p()
        p(f"## Grille, {_titre_nu(nu)}")
        p("Colonnes : " + " | ".join(f"π̄ = {_f(100 * pi)} %, n_a = {na}" for pi, na in entetes))
        for gr in GRANDEURS:
            p(f"- {gr.ident} — {gr.definition} [{gr.unite} ; dénominateur : {gr.denominateur} ; fenêtre : "
              f"{gr.fenetre} ; {gr.source}]")
            p("  " + " | ".join(_f(r["grille"][(nu, pi, na)][gr.ident]) if (nu, pi, na) in r["grille"]
                                else "non publié" for pi, na in entetes))

    # Ordre de publication (R3 de `macro`) : colonne ν_G retenue, forme fermée en ν_G, puis la référence ν_G = 1.
    if r["nu_g_retenu"] is not None:
        grille(r["nu_g_retenu"])
    p()
    p("## Forme fermée en ν_G (n_a, π̄ du point ; a, c, x publiés ci-dessus)")
    p("m(ν_G) = M^G/(n_a PIB) = ν_G [x/(n_a Γ̄) + a c]/(1 − ν_G a) ; dette brute b(ν_G) = c + m(ν_G) ; "
      "refinancement l^CB(ν_G) = m(ν_G) ; titres de la banque b_Bk(ν_G) = c + m(ν_G) (θ_CB = 0) ; "
      "charge d'intérêts brute i_CB b(ν_G) ; D2 : ν_G < 1/a.")
    p("Propriété J-ν : marge m_ν = 1 − 1,10 Γ̄ (G/PB)/ν_G, exigence ≥ 0,03 au pire point de la grille.")
    for nu in sorted({k[0] for k in r["propositions"]}):
        vals = [r["propositions"][(nu, pi, na)] for pi, na in entetes]
        p(f"- ν_G = {_f(nu)} : m_ν " + " | ".join(_f(v, 6) for v in vals) + f" ; pire point {_f(min(vals), 6)}")
    nus_min = {(pi, na): r["grille"][(1.0, pi, na)]["nu_G_J"] for pi, na in entetes if (1.0, pi, na) in r["grille"]}
    p("- ν_G minimal pour m_ν ≥ 0,03 : " + " | ".join(
        _f(nus_min[k], 7) if k in nus_min else "non publié" for k in entetes)
      + f" ; maximum {_f(max(nus_min.values()), 7) if nus_min else 'non publié'}")
    grille(1.0)
    p()
    p("## Niveaux bancaires (#83), republication (B-2) à v_H résolu et m par E8")
    p(f"Explication écrite avant l'essai : {EXPL_B2}.")
    for (nu, pi), b in sorted(r["republication"].items(), key=lambda kv: (_rang_nu(kv[0][0]), kv[0])):
        p(f"- ν_G = {_f(nu)}, π̄ = {_f(100 * pi)} %, n_a = 12 : " + " ; ".join(
            f"{k} = {_f(v, 8)}" for k, v in b.items()))
    for pi in POINTS_PI:
        if (pi, 12) in hors:
            p(f"- ν_G = 1, π̄ = {_f(100 * pi)} %, n_a = 12 : {constat_reference(hors[(pi, 12)])}")
    p()
    p("## État initial résolu, niveaux d'ouverture du pas 0")
    for nu in sorted({k[0] for k in r["niveaux"]} | ({1.0} if hors else set()), key=_rang_nu):
        p(f"### {_titre_nu(nu)}")
        for (nu_, pi, na), niv in sorted(r["niveaux"].items()):
            if nu_ == nu:
                p(f"- π̄ = {_f(100 * pi)} %, n_a = {na} : " + " ; ".join(f"{k} = {_f(v)}" for k, v in niv.items()))
        if nu == 1.0:
            for (pi, na), marge in sorted(hors.items()):
                p(f"- π̄ = {_f(100 * pi)} %, n_a = {na} : {constat_reference(marge)}")
    p()
    p("## Contrôles (plus grand résidu par famille, relatif à l'échelle déclarée ; seuil 1e−12)")
    for (nu, pi, na), c in sorted(r["controles"].items(), key=lambda kv: (_rang_nu(kv[0][0]), kv[0])):
        p(f"- ν_G = {_f(nu)}, π̄ = {_f(100 * pi)} %, n_a = {na} : " + " ; ".join(
            f"{k} {_f(v, 3)}" for k, v in c.items()))
    pire = plus_grand_residu(r)
    p(f"Plus grand résidu de la grille : {_f(pire, 3)} ({'tenu' if pire <= TOL_IDENTITE else 'NON TENU'}).")
    p()
    p("## Constats de domaine à l'état stationnaire")
    for (nu, pi, na), v in sorted(r["grille"].items(), key=lambda kv: (_rang_nu(kv[0][0]), kv[0])):
        constats = []
        if v["caisse_DF4"] < 0:
            constats.append(f"q1 : D_F en fin de phase 4 négatif, marge {_f(v['caisse_DF4'], 6)} de D_F ; "
                            f"ν_F,min = {_f(v['nu_F_min'], 6)} an > ν_F = {_f(base.nu_F, 6)}")
        if not 0.2 <= v["distribution"] <= 0.9:
            constats.append(f"distribution {_f(v['distribution'], 6)} hors de [0,2 ; 0,9] (#55)")
        if v["Em"] <= 0:
            constats.append("rachat net (Em ≤ 0)")
        if constats:
            p(f"- ν_G = {_f(nu)}, π̄ = {_f(100 * pi)} %, n_a = {na} : " + " ; ".join(constats))
    # Plafond de E1 actif : refus sur les colonnes ν_G > 1 ; constat déclaré sur la colonne de référence.
    for (pi, na), marge in sorted(hors.items()):
        p(f"- ν_G = 1, π̄ = {_f(100 * pi)} %, n_a = {na} : {constat_reference(marge)}")
    p()
    fe = r["fermeture"]
    nu_mesure = nu_g_mesure(r["nu_g_retenu"])  # ν_G de la fermeture et de la mesure de #80
    p(f"## Fermeture (#44, lecture (e)) : sensibilité de θ_G à r̄ (π̄ = 2 %, n_a = 12, ν_G = {_f(nu_mesure)} ; "
      "identique bit à bit à ν_G = 1, C59)")
    p(f"- dθ_G/dr̄ = {_f(fe['dtheta_G_dr'], 6)} (% de la production par point de r̄ ; différence centrée, "
      f"pas {fe['pas']:g} ; erreur déclarée {_f(fe['erreur'], 3)})")
    p(f"- d(G/PIB)/dr̄ = {_f(fe['dG_PIB_dr'], 6)} ; points de r̄ par point de PIB de dépense : "
      f"{_f(fe['points_r_par_point_PIB'], 6)}")
    p()
    sn = r["superneutralite"]
    p("## Superneutralité (#80, critère 13 de la fiche 8) : lecture (α), lecture A de i^ref, norme ϱ̄_L fixée "
      "(décision du mainteneur du 05/10/2026)")
    for gr in GRANDEURS_ALPHA:
        p(f"- {gr.ident} — {gr.definition} [{gr.unite} ; dénominateur : {gr.denominateur} ; fenêtre : "
          f"{gr.fenetre} ; {gr.source}]")
    for pi, a in sn["alpha"].items():
        p(f"- π* = {_f(100 * pi)} %, n_a = 12 : r̄_α = {100 * a['r_alpha']:.6f} % ; F(r̄_α) = {a['F']:+.3e} ; "
          f"{a['iterations']} itérations ; racines {[round(100 * x, 6) for x in a['racines']]} % ; "
          f"pôles {[round(100 * x, 6) for x in a['poles']]} % ; Δϱ = {100 * a['d_rho']:+.6f} point")
    for n, d in sn["alpha_n_a"].items():
        p(f"- n_a = {n} : r̄_α = " + " | ".join(f"{100 * d[pi]['r_alpha']:.6f} %" for pi in POINTS_PI)
          + f" ; Δr̄_α = {100 * sn['delta_r_alpha_n_a'][n]:.6f} point")
    p(f"- verdict : Δr̄_α = max − min sur {{0 ; 2 ; 10 %}}, n_a = 12, ν_G = {_f(nu_mesure)} (identique bit à bit à "
      "ν_G = 1, C59) : "
      f"{100 * sn['delta_r_alpha']:.6f} point ; "
      f"seuil {100 * SEUIL_SUPERNEUTRALITE:g} point : "
      f"{_verdict_seuil([sn['delta_r_alpha']], SEUIL_SUPERNEUTRALITE)}")
    p(f"- écart entre les bornes r̄_α(10 %) − r̄_α(0) : {100 * sn['ecart_bornes']:+.6f} point ; écart maximal sur le "
      f"profil : {100 * sn['ecart_profil']:.6f} point ; marche de 2 à 3 % : {100 * sn['marche_2_3']:+.6f} point")
    al = sn["allocations"]
    for pi, a in sn["alpha"].items():
        p(f"- allocations (α) à π* = {_f(100 * pi)} % : " + " ; ".join(
            f"{q} {_f(a['allocations'][q], 9)}" for q in ALLOCATIONS_VERDICT + ALLOCATIONS_INVARIANTES
            + ALLOCATIONS_MESUREES))
    verdict = _verdict_seuil((al[q] for q in ALLOCATIONS_VERDICT), SEUIL_SUPERNEUTRALITE)
    invariance = _verdict_seuil(sn["invariance"].values(), TOL_INVARIANCE, "tenue", "NON TENUE")
    p("- verdict des allocations (liste L2), max − min sur {0 ; 2 ; 10 %}, point : " + " ; ".join(
        f"{q} {100 * al[q]:.6f}" for q in ALLOCATIONS_VERDICT)
      + f" ; seuil {100 * SEUIL_SUPERNEUTRALITE:g} point : {verdict}")
    p("- invariance exacte (écart relatif max − min, seuil " + f"{TOL_INVARIANCE:g}) : " + " ; ".join(
        f"{q} {_f(v, 3)}" for q, v in sn["invariance"].items()) + f" : {invariance}")
    p("- mesures (sans verdict), max − min sur {0 ; 2 ; 10 %}, point : " + " ; ".join(
        f"{q} {100 * al[q]:.6f}" for q in ALLOCATIONS_MESUREES))
    p("- lecture (β) (r̄ = 1 % à chaque π*, mesure sans verdict) : "
      f"écart de θ_G {100 * sn['beta_theta_G']:.6f} point ; "
      + " ; ".join(f"{q} {100 * v:.6f}" for q, v in sn["beta_allocations"].items()))
    p(f"- sensibilité à ζ (mesure, décision de `macro`) : verdict jugé à ζ = {_f(base.zeta)} ; étendue max − min sur "
      "{0 ; 2 ; 10 %}, n_a = 12, ν_G = " + _f(nu_mesure) + ", en point, sur ζ ∈ {"
      + " ; ".join(_f(z) for z in ZETA_PLAGE) + "} (calibration indicative ; table T1) et à ζ = "
      + f"{_f(ZETA_ILLUSTRATION)} en illustration, sans verdict")
    for z, d in sn["zeta"].items():
        statut = ("table T1" if z == base.zeta else "calibration indicative" if z in ZETA_PLAGE
                  else "illustration, sans verdict")
        p(f"  - ζ = {_f(z)} ({statut}) : Δr̄_α {100 * d['delta_r_alpha']:.6f} ; " + " ; ".join(
            f"{q} {100 * v:.6f}" for q, v in d["allocations"].items()))
    p("  - allocations dépendantes de ζ (par r̄_α ; écart relatif > " + f"{TOL_INVARIANCE:g} entre ζ ∈ "
      "{" + " ; ".join(_f(z) for z in sn["zeta"]) + "}, mesuré) : " + ", ".join(sn["dependantes_de_zeta"]))
    p()
    p("## Configuration de contrôle C-F (ϖ_L = ϖ_D = 0), non admissible : "
      "condition d'existence du dividende de la banque")
    for pi, v in r["cf"].items():
        p(f"- π̄ = {_f(100 * pi)} % : marge d'existence {_f(v['existence_Bk'], 6)} ; "
          f"distribution {_f(v['distribution'], 6)} ; "
          f"dividendes/ventes {_f(v['Div_F_sur_ventes'], 6)} %")
    p()
    if "publiees" not in r:  # résultat de `calculer` seul : aucune comparaison aux valeurs publiées (#185)
        return

    def ligne(l: dict[str, object]) -> None:
        comparaison = ("" if l["publie"] == AUCUNE or l["verdict"] == "refusée"
                       else f"écart {l['ecart']:+.3g} (seuil {l['seuil']:.1g}) : ")
        p(f"- [{l['categorie']}] {l['section']} — {l['grandeur']} : publié {l['publie']} ; "
          f"script {l['libelle'] or _f(l['script'], 9)} ; {comparaison}{l['verdict']}"
          + (f" — explication {l['explication']}" if l["explication"].startswith(("écrite", "établie"))
             else f" — {l['explication']}" if l["explication"] else ""))

    p("## Valeurs publiées en vigueur : comparaison à la dernière décimale (arrondi au plus proche)")
    ecarts = [l for l in r["publiees"] if l["verdict"] == "écart"]
    non_publiees = [l for l in r["publiees"] if l["verdict"] == "non publiée"]
    refusees = [l for l in r["publiees"] if l["verdict"] == "refusée"]
    for l in r["publiees"]:
        ligne(l)
    p()
    egales_S = sum(1 for l in r["publiees"] if l["verdict"] == "égal" and l["categorie"] == "S")
    p(f"Bilan : {len(r['publiees'])} valeurs comparées, "
      f"{len(r['publiees']) - len(ecarts) - len(non_publiees) - len(refusees) - egales_S} égales sur "
      f"l'état résolu, {egales_S} égales en arithmétique de la spécification (catégorie S, sans état résolu), "
      + (f"{len(ecarts)} écarts (publiés avec leur explication ; aucun n'est masqué)" if ecarts else "aucun écart")
      + (f", {len(non_publiees)} non publiées (point de référence hors domaine, plafond de E1 actif)"
         if non_publiees else "")
      + (f", {len(refusees)} {'refusée' if len(refusees) == 1 else 'refusées'} (minimum de Δr̄_α en ζ non "
         "localisé, motif à la ligne)." if refusees else "."))
    p()
    p("## Contre-épreuve : valeurs barrées reproduites sous leurs entrées d'origine (illustration du bloc 7, "
      "publication au commit 54edad8 ; ν_G non retenu), hors du bilan des valeurs en vigueur")
    for l in r["contre_epreuve"]:
        ligne(l)
    p()
    ecarts_c = sum(1 for l in r["contre_epreuve"] if l["verdict"] != "égal")
    p(f"Bilan de la contre-épreuve : {len(r['contre_epreuve'])} valeurs barrées, "
      f"{len(r['contre_epreuve']) - ecarts_c} égales sous leurs entrées d'origine, "
      + (f"{ecarts_c} écarts." if ecarts_c else "aucun écart."))
    p()
    p("## Historique : valeurs publiées avant le visa du 05/10/2026 (commit 9c8bdbd), ancien verdict")
    for l in r["historique"]:
        ligne(l)
    p()
    ecarts_h = sum(1 for l in r["historique"] if l["verdict"] == "écart")
    p(f"Bilan de l'historique : {len(r['historique'])} valeurs, {ecarts_h} écarts, visés le 05/10/2026 et "
      "republiés (spécification, commit 8b9fa94 ; annotations de la fiche 9).")


def _jsonable(x):
    """Convertit les clés tuples et les paramètres pour l'export JSON."""
    if isinstance(x, Parametres):
        return {f.name: getattr(x, f.name) for f in fields(x)}
    if isinstance(x, dict):
        return {(" ; ".join(map(str, k)) if isinstance(k, tuple) else str(k)): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return str(x)
    return x


def main(arguments: list[str] | None = None) -> int:
    analyseur = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    analyseur.add_argument("--nu-g-retenu", type=float, default=NU_G_RETENU,
                           help=f"valeur retenue de ν_G, troisième colonne de la grille (défaut {NU_G_RETENU}, "
                                "décision du 05/10/2026 ; 1 est refusé, déjà point de référence)")
    analyseur.add_argument("--json", default=None, help="écrit aussi les résultats en JSON dans ce fichier")
    args = analyseur.parse_args(arguments)
    try:
        r = calculer(Parametres(), args.nu_g_retenu) | publier(args.nu_g_retenu)
    except HorsDomaine as refus:
        print(f"Refus de domaine : {refus}", file=sys.stderr)
        return 1
    afficher(r)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(_jsonable(r), f, ensure_ascii=False, indent=1, sort_keys=True)
            f.write("\n")
    pire = plus_grand_residu(r)
    if not pire <= TOL_IDENTITE:
        print(f"Résidu non tenu : plus grand résidu de la grille {pire!r} > {TOL_IDENTITE:g}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
