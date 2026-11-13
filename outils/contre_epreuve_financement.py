"""Contre-épreuve indépendante des boucles de la fiche 6 et des variantes écartées de la règle F.

Contrat : issue #66 (critères d'acceptation : chiffres reproduits, ou écart
expliqué, par un script cité avec sa commande et sa sortie ; aucune ligne de
`tab:instabilites` n'est versée sans concordance). Expert pilote `macro`, avis
de `monnaie` (crédit).

**Indépendance** (consigne P39 du plan de J3-a). La maquette est écrite depuis
la seule spécification (`docs/specification/nations_et_marches.tex`, règles
N1 à N11, T1 à T6, P1 à P4, H2 à H7, S1 à S7, F1 à F4, B1 à B6, BC1 à BC3,
E1, E3 à E5, E12) et l'état stationnaire résolu de `outils/etat_stationnaire.py`
(fonction `etat_stationnaire` et classe `Parametres`, seules importées). Ni la
maquette conjointe de #65, ni les maquettes de la fiche 6 (`conj6_*.py`,
`stat.py`), ni `src/`, ni `archive/` n'ont été lues ni importées. La fiche
`docs/blocs/investissement.md` n'a été lue qu'au § 3.N, pour la définition
des variantes de F et les chiffres publiés à comparer (une recherche par motif
y a aussi affiché les titres de sections et les lignes qui citent 1,05 et
1,49). La fonction `un_pas` de
`outils/etat_stationnaire.py` a été lue (fichier autorisé) mais n'est pas
appelée : le pas ci-dessous est transcrit des encadrés de la spécification.

**Objet.** Remesurer, autour de l'état stationnaire :

1. les deux variantes écartées de F (`sec:ecartees`, fiche § 3.N) : « levier
   sur p K^vol » (publié 1,0528 à 1,0538 selon l'écriture, 1,0530 en tête du
   tableau de la fiche) et « cible de dépôts sur les ventes du pas » (publié
   1,49 ; 1,4991 avec le levier comptable, 1,4925 avec le levier sur p K^vol),
   avec F retenue pour référence (0,9971 à λ_ti × 2, 0,9980 à la base) ;
2. les rayons cités par `sec:investissement-conditions` : boucle propre
   (0,99793, 0,99923, 0,9971, approximation 0,99709), boucle réduite
   investissement – demande (neuf rayons, cinq seuils de λ_ti, domaine A),
   racine lente du capital comptable sans levier (0,99255).

**Méthode.**

- *Boucle conjointe.* Un pas complet du socle, phases 1 à 9 de `tab:phases`,
  est transcrit des encadrés (`pas`). L'état d'ouverture est réduit sans
  perte aux variables qui rétroagissent : par les bilans de
  `tab:matrice-bilans` (B_H = 0, E^CB = 0, i_B = i_res = i_CB au socle), la
  dette consolidée B − M^G − E^CB égale D_H + D_F + E^Bk − L, ce qui donne
  T^cou (E4) et le résultat de la banque (B5) sans tenir B, M^G, Res ni
  L^CB ; le plafond de E1 (encaisse du Trésor) et celui de E6 (θ_Tr = 0)
  sont inactifs à l'état stationnaire et ne sont pas tenus. Le pas d'un état
  stationnaire résolu reproduit le sentier à 1e−12 près (contrôle publié).
  Ce contrôle porte sur les niveaux, pas sur les pentes : un terme d'écart
  nul à l'état stationnaire (λ_H (V* − V) de H4, ψ_ξ ξ de P2, β (U − U^eq)
  de T3, η_r (ϱ_L − ϱ̄_L) de S3…) peut changer de signe sans qu'il le voie.
  Les pentes de ces termes sont vérifiées à part, par des tests de signe sur
  `pas` (`tests/unitaires/test_contre_epreuve_financement.py`).
- *Linéarisation.* Jacobienne de l'application détendancée (volumes divisés
  par (1 + g)^{t/n_a}, prix par (1 + π̄)^{t/n_a}, montants nominaux par
  Γ̄^t), en écarts relatifs, par différences centrées (pas 1e−6). Contrôle
  de dérivabilité : différences avant et arrière comparées colonne par
  colonne (écart au plus `TOL_COUDE`) ; une colonne dont la ligne de J est
  nulle en est exemptée, car son coude est sans effet sur le spectre
  (développement de det(λI − J) selon cette ligne). Les
  grandeurs exogènes (productivité, population active, cible, ϱ̄_L, θ_G, et
  r̂* quand le taux est exogène) sont tenues hors de la perturbation.
- *Racine nominale.* L'application est homogène de degré un dans les
  grandeurs nominales (aucune ancre nominale en u.m., `sec:finances_publiques-
  depense`) : la direction h des grandeurs nominales vérifie J h = h (résidu
  publié). Cette racine 1 est retirée par déflation de Wielandt (J − h e_Wᵀ,
  e_Wᵀ h = 1), comme le demande la condition C36 (« hors de la racine
  nominale »). Le rayon publié est le module dominant du reste du spectre.
- *État stationnaire des variantes.* Une variante de F déplace les encours
  (L, D_F, puis D_H, E^Bk). Son état stationnaire est résolu sur le sentier
  π̄ = π* et U = U^eq, la part θ_G de la dépense publique étant la variable de
  fermeture (lecture (e) de la décision M32, comme l'état initial résolu), par
  Newton sur l'application détendancée, salaire d'ouverture tenu (normalisation
  nominale). Coût mesuré : voir `--chrono`.
- *Régimes de l'emploi.* T4 a un coude à l'état stationnaire (N* égale
  l'ajustement partiel) : la jacobienne est prise de chaque côté, régime de
  hausse (N = N*) et régime de baisse (ajustement partiel). N5 en hérite un
  coude (pr N = y* à l'état stationnaire) : dans chaque régime, sa branche
  est prise sous la forme y = min(y*, pr N^pa), égale à N5 dans le régime
  (hausse : pr min(N^pa, N*) ; baisse : ajustement partiel ≥ N*, donc
  y = y* tant que N^pa ne lie pas).
- *Boucle propre et boucle réduite.* Récurrences de `sec:investissement-
  conditions` : capital et part visée à demande, prix et taux exogènes ;
  production (N1 à N7) et S3, S6, avec d = A + m y_{t−1} + I^{vol,plan},
  A tiré de la condition de domaine. Seuils de λ_ti par balayage puis
  bissection.

**Configurations de la boucle conjointe.** `socle` : paramètres de
`Parametres` (écarts ϖ_L, ϖ_D du bloc banque, ϑ = 0,1, τ_H = 0,25) ;
`fiche` : hypothèses de la fiche § 3.N, i_L = i_D = 3 % (ϖ = 0 et r̄ tel
que i_CB = 3 %), sans fonds propres bancaires (ϑ = 0, la banque ne verse
alors rien) et sans impôt (τ_H = τ_F = 0) ; le reste de la maquette de la
fiche n'est pas publié, et la configuration n'en est qu'une approximation.
Dans les deux, le taux est exogène (a_π = a_I = 0 dans BC1 et BC2 ; π^e suit
BC3) ; la règle de taux active est publiée en mesure complémentaire.

Usage : `uv run python outils/contre_epreuve_financement.py [--json FICHIER]
[--chrono]`. Déterministe : deux exécutions donnent la même sortie à l'octet
(hors `--chrono`). Code de sortie 0 si les contrôles internes (sentier
stationnaire, homogénéité, convergence de Newton, dérivabilité, seuil de λ_ti
encadré par sa grille) passent, 2 sinon ; les écarts
aux valeurs publiées sont publiés, jamais bloquants (le verdict relève de
`macro` et du mainteneur).
"""

from __future__ import annotations

import argparse
import cmath
import importlib.util
import json
import math
import sys
import time
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np

RACINE = Path(__file__).resolve().parents[1]


def _charger_etat_stationnaire():
    """Charge `outils/etat_stationnaire.py` par son chemin (`outils/` n'est pas un paquet)."""
    nom = "etat_stationnaire"
    if nom in sys.modules:
        return sys.modules[nom]
    spec = importlib.util.spec_from_file_location(nom, RACINE / "outils" / "etat_stationnaire.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[nom] = module
    spec.loader.exec_module(module)
    return module


ES = _charger_etat_stationnaire()
Parametres = ES.Parametres

# --- Tolérances et pas numériques déclarés ---------------------------------------

PAS_DIFF = 1e-6  # pas relatif des différences centrées
TOL_SENTIER = 1e-12  # résidu relatif du pas d'un état stationnaire résolu
TOL_HOMOGENEITE = 1e-6  # résidu de J h = h (différences finies)
TOL_NEWTON = 1e-13  # résidu relatif de l'état stationnaire d'une variante
ITERATIONS_NEWTON = 30
TOL_RACINE_NOMINALE = 1e-6  # |λ − 1| sous lequel une racine est tenue pour la racine nominale (contrôle)
TOL_COUDE = 1e-3  # écart admis entre différences avant et arrière d'une colonne de J (coude non résolu au-delà)

# --- Variantes de la règle F (fiche 6, § 3.N ; `sec:ecartees`) ------------------

CREDITS = {
    "comptable": "F1 retenue : lv* [(1 − δ/n_a) K + I^plan]",
    "pK_phat_ouv": "levier sur p K^vol : lv* p̂_t K^vol_t (ouverture), p̂_t = P_{t−1}(1 + π*)^{1/n_a}",
    "pK_phat_apres": "levier sur p K^vol : lv* p̂_t [(1 − δ/n_a) K^vol_t + I^{vol,plan}_t]",
    "pK_pm1_ouv": "levier sur p K^vol : lv* P_{t−1} K^vol_t (ouverture)",
    "pK_pm1_apres": "levier sur p K^vol : lv* P_{t−1} [(1 − δ/n_a) K^vol_t + I^{vol,plan}_t]",
}
DEPOTS = {
    "ve": "F2 retenue : ν_F n_a P_{t−1}(1 + π^pas)² v^e_{t+1}",
    "ventes_du_pas": "cible de dépôts sur les ventes du pas : ν_F n_a p_t v_t",
}


@dataclass(frozen=True)
class Config:
    """Configuration de la boucle conjointe : règle F et régime de l'emploi (T4)."""

    credit: str = "comptable"
    depots: str = "ve"
    regime: str = "hausse"  # "hausse" : N = N* ; "baisse" : ajustement partiel de T4
    taux: str = "exogene"  # "exogene" : a_π = a_I = 0 ; "regle" : BC1 et BC2 de `Parametres`


# --- État d'ouverture -------------------------------------------------------------

# Grandeurs exogènes de l'ouverture : avancées par leur tendance, jamais perturbées.
EXOGENES = ("pr", "N_pa", "pi_cible", "rho_bar_L", "theta_G")
# Classes de croissance par pas sur le sentier stationnaire.
NOMINAUX = ("W_m1", "IN", "K", "L", "D_F", "D_H", "E_Bk", "YD_m1", "Y_HS_m1", "T_F_m1")
VOLUMES = ("ve", "IN_vol", "K_vol", "y_m1")
CONSTANTES = ("U_m1", "ti", "i_L", "i_D", "r_hat", "pi_e")


def cles_etat(n: int) -> tuple[str, ...]:
    """Ordre canonique des grandeurs d'ouverture perturbables (registre des prix compris)."""
    return NOMINAUX + tuple(f"P{u}" for u in range(n + 1)) + VOLUMES + ("N_m1",) + CONSTANTES


def ouverture_resolue(par: Parametres) -> dict[str, float]:
    """Ouverture du pas 0 tirée de l'état stationnaire résolu (sections « État initial résolu »)."""
    e = ES.etat_stationnaire(par)
    n = par.n_a
    Gr, Gam, Pp = e["Gr"], e["Gam"], e["Pp"]
    pr_m1 = e["pr"] * (1 + par.g_pr) ** (-1 / n)
    o = {f"P{u}": e["p"] * Pp ** (-(u + 1)) for u in range(n + 1)}  # P{u} = P_{t−1−u}
    o.update(
        W_m1=o["P0"] * pr_m1 / (1 + par.mu_bar),  # T2 à ω = ω*
        IN=e["IN"], K=e["K"], L=e["L"], D_F=e["D_F"], D_H=e["D_H"], E_Bk=e["E_Bk"],
        YD_m1=e["YD"] / Gam, Y_HS_m1=e["Y_HS"] / Gam, T_F_m1=e["T_F"] / Gam,
        ve=e["ve"], IN_vol=e["IN_vol"], K_vol=e["K_vol"], y_m1=e["y"] / Gr,
        N_m1=e["N"] * (1 + par.g_N) ** (-1 / n), U_m1=par.U_eq, ti=e["ti"], i_L=e["i_L"], i_D=e["i_D"],
        r_hat=e["r_hat"], pi_e=par.pi_cible,
        pr=e["pr"], N_pa=e["N_pa"], pi_cible=par.pi_cible, rho_bar_L=e["rho_bar_L"], theta_G=e["theta_G"],
    )
    return o


def facteurs_sentier(par: Parametres) -> dict[str, float]:
    """Facteur de croissance par pas de chaque grandeur d'ouverture, sentier π̄ = π*."""
    n = par.n_a
    g = (1 + par.g_pr) * (1 + par.g_N) - 1
    Gr = (1 + g) ** (1 / n)
    Pp = (1 + par.pi_cible) ** (1 / n)
    Gam = Gr * Pp
    f = {k: Gam for k in NOMINAUX}
    f["W_m1"] = Pp * (1 + par.g_pr) ** (1 / n)
    f.update({f"P{u}": Pp for u in range(n + 1)})
    f.update({k: Gr for k in VOLUMES})
    f["N_m1"] = (1 + par.g_N) ** (1 / n)
    f.update({k: 1.0 for k in CONSTANTES})
    f.update(pr=(1 + par.g_pr) ** (1 / n), N_pa=(1 + par.g_N) ** (1 / n), pi_cible=1.0, rho_bar_L=1.0,
             theta_G=1.0)
    return f


# --- Un pas du socle, transcrit de la spécification -------------------------------


def pas(o: dict[str, float], par: Parametres, cfg: Config) -> dict[str, float]:
    """Un pas, phases 1 à 9 ; rend l'ouverture du pas suivant (mêmes clés que `o`)."""
    n = par.n_a
    P = [o[f"P{u}"] for u in range(n + 1)]
    g = (1 + par.g_pr) * (1 + par.g_N) - 1
    Gr = (1 + g) ** (1 / n)
    pi_c = o["pi_cible"]
    Gam_e = ((1 + g) * (1 + pi_c)) ** (1 / n)  # Γ^e du moteur, sur la cible d'ouverture
    gam_e = Gam_e - 1
    pis = (1 + pi_c) ** (1 / n) - 1  # π^{*,pas}
    a_pi, a_I = (0.0, 0.0) if cfg.taux == "exogene" else (par.a_pi, par.a_I)

    # Phase 1 : salaire (T2, T3), banque centrale (BC1 à BC3).
    pi_prec = P[0] / P[n] - 1  # π_{t−1}
    pr = o["pr"]
    pr_m1 = pr * (1 + par.g_pr) ** (-1 / n)
    omega_m1 = o["W_m1"] / (P[0] * pr_m1)  # T2
    W = math.exp(math.log(o["W_m1"]) + (math.log(1 + par.g_pr) + math.log(1 + o["pi_e"])) / n
                 + par.lambda_w / n * (math.log(1 / (1 + par.mu_bar) / omega_m1)
                                       - par.beta * (o["U_m1"] - par.U_eq)))  # T3
    i_CB = (1 + o["r_hat"]) * (1 + pi_c) + a_pi * (pi_prec - pi_c) - 1  # BC1
    r_hat_1 = o["r_hat"] + a_I / n * (pi_prec - pi_c)  # BC2
    pi_e_1 = o["pi_e"] + par.lambda_e / n * (pi_prec - o["pi_e"])  # BC3

    # Phase 2 : plans (N2 à N4, N8, H2 à H5, S1 à S4, E1, E3, E4).
    IN_star = n * par.sigma * o["ve"]  # N2
    y_star = max(0.0, o["ve"] + (Gr - 1) * IN_star + par.lambda_IN / n * (IN_star - o["IN_vol"]))  # N3
    N_star = y_star / pr  # N4
    UC = W / pr  # N8
    D_c = o["D_H"] + o["D_F"] + o["E_Bk"] - o["L"]  # B − M^G − E^CB par les bilans (B_H = 0)
    i_ref = (1 + par.rbar) * (1 + pi_c) - 1
    T_cou = par.phi * (i_CB - i_ref) * D_c / n  # E4
    T_H = par.tau_H * Gam_e * o["Y_HS_m1"] + T_cou  # E3
    YD_e = Gam_e * o["YD_m1"]  # H2
    V_H = o["D_H"]
    V_star = par.nu_H * n * (YD_e - pis * V_H)  # H3
    C_regle = YD_e - gam_e * V_H - par.lambda_H / n * (V_star - V_H)  # H4
    C_plan = min(o["D_H"], max(0.0, C_regle))  # H5
    rho_L = (1 + o["i_L"]) / (1 + pi_c) - 1  # S1
    tu_star = par.tu_bar * math.exp(par.zeta * (rho_L - o["rho_bar_L"]))  # S2
    I_vol_plan = o["ti"] * Gr * o["y_m1"] * math.exp(-par.eta_r * (rho_L - o["rho_bar_L"]))  # S3
    I_plan = P[0] * (1 + pis) * I_vol_plan  # S4
    y_pot = pr * (1 - par.U_eq) * o["N_pa"]
    G_plan = P[0] * (1 + pis) * o["theta_G"] * y_pot  # E1, plafond de l'encaisse inactif (non tenu)

    # Phase 3 : crédit (F1 ou variante).
    if cfg.credit == "comptable":
        L_cible = par.lv * ((1 - par.delta / n) * o["K"] + I_plan)
    else:
        prix = P[0] * (1 + pis) if "phat" in cfg.credit else P[0]
        capital = o["K_vol"] if cfg.credit.endswith("ouv") else (1 - par.delta / n) * o["K_vol"] + I_vol_plan
        L_cible = par.lv * prix * capital
    dL_d = L_cible - o["L"]
    dL = (1 - par.varsigma_L) * max(dL_d, 0.0) + min(dL_d, 0.0)

    # Phase 4 : travail (T4 à T6), puis production (N5, N11).
    partiel = (1 + par.g_N) ** (1 / n) * (1 - par.lambda_N / n) * o["N_m1"] + par.lambda_N / n * N_star
    N = min(o["N_pa"], N_star if cfg.regime == "hausse" else partiel)  # T4, branche du régime
    U = 1 - N / o["N_pa"]  # T5
    WB = W * N  # T6
    # N5, branche du régime : y = min(y*, pr N) avec N = min(N^pa, N*) en hausse, N ≥ N* en baisse (T4) ;
    # dans les deux cas y = min(y*, pr N^pa), sans le coude pr N = y* de l'état stationnaire.
    y = min(y_star, pr * o["N_pa"])  # N5
    tu = y / (o["K_vol"] / (n * par.kappa))  # N11

    # Phase 5 : prix (P1 à P3), production (N6 à N10, N1), acheteurs (H6, S5, E2), S6.
    xi = 1 - o["IN_vol"] / IN_star  # P1
    UC_m1 = o["W_m1"] / pr_m1
    mu_t = ((1 - par.lambda_mu / n) * math.log(P[0] / UC_m1)
            + par.lambda_mu / n * (math.log(1 + par.mu_bar) + par.psi_xi * xi))  # P2
    p = UC * math.exp(mu_t)  # P3, P4
    d_H, d_F, d_G = C_plan / p, I_plan / p, G_plan / p  # N6
    d = d_H + d_F + d_G
    v = min(d, o["IN_vol"] + y)
    v_H, v_F, v_G = v / d * d_H, v / d * d_F, v / d * d_G
    IN_vol_1 = o["IN_vol"] + y - v  # N7
    cm = (o["IN"] + UC * y) / (o["IN_vol"] + y)  # N8
    dIN = UC * y - cm * v
    K_vol_1 = (1 - par.delta / n) * o["K_vol"] + v_F  # N10
    ve_1 = Gr * ((1 - par.lambda_v / n) * o["ve"] + par.lambda_v / n * d)  # N1
    C, I, G = p * v_H, p * v_F, p * v_G  # H6, S5, E2
    ti_1 = o["ti"] * math.exp(par.lambda_ti / n * (tu - tu_star))  # S6

    # Phase 6 : S7, B3 à B6, E5, F2 à F4.
    amort = par.delta * o["K"] / n  # S7
    l9 = o["i_L"] * o["L"] / n  # B3
    l10_H, l10_F = o["i_D"] * o["D_H"] / n, o["i_D"] * o["D_F"] / n  # B4
    Pi_av = C + G + I + dIN - WB - amort - l9 + l10_F
    T_F = par.tau_F * Pi_av  # E5
    if cfg.depots == "ve":
        D_F_star = par.nu_F * n * P[0] * (1 + pis) ** 2 * ve_1  # F2
    else:
        D_F_star = par.nu_F * n * p * v  # variante : ventes du pas
    T_F_e = Gam_e * o["T_F_m1"]  # F4
    tresorerie_F = o["D_F"] + dL + C + G - WB - l9 + l10_F - T_F_e - D_F_star
    Div_F = max(0.0, tresorerie_F)  # F3
    L_1 = o["L"] + dL
    # B5, avec i_B = i_res = i_CB et B_Bk + Res − L^CB = D_H + D_F + E^Bk − L (bilan de la banque).
    Pi_Bk = (o["i_L"] * o["L"] + i_CB * D_c - o["i_D"] * (o["D_H"] + o["D_F"])) / n
    exces_Bk = o["E_Bk"] + Pi_Bk - par.vartheta * L_1
    Div_Bk = max(0.0, exces_Bk)  # B6

    # Phase 7 : assiette (E12). Phase 8 (c) : B1, B2. Phase 9 : H7, registre, T_F retenu.
    Y_HS = WB + l10_H + Div_F + Div_Bk - pis * o["D_H"] - T_cou  # E12
    YD = WB - T_H + l10_H + Div_F + Div_Bk  # H7 (Tr = 0, B_H = 0)
    o1 = {"P0": p}
    o1.update({f"P{u}": P[u - 1] for u in range(1, n + 1)})
    o1.update(
        W_m1=W,
        IN=o["IN"] + dIN,
        K=o["K"] + I - amort,
        L=L_1,
        D_F=o["D_F"] + dL - WB + C + G - l9 + l10_F - T_F - Div_F,
        D_H=o["D_H"] + WB - C - T_H + l10_H + Div_F + Div_Bk,
        E_Bk=o["E_Bk"] + Pi_Bk - Div_Bk,
        YD_m1=YD, Y_HS_m1=Y_HS, T_F_m1=T_F,
        ve=ve_1, IN_vol=IN_vol_1, K_vol=K_vol_1, y_m1=y, N_m1=N, U_m1=U, ti=ti_1,
        i_L=i_CB + par.varpi_L, i_D=i_CB - par.varpi_D,  # B1, B2
        r_hat=r_hat_1, pi_e=pi_e_1,
        pr=pr * (1 + par.g_pr) ** (1 / n), N_pa=o["N_pa"] * (1 + par.g_N) ** (1 / n), pi_cible=pi_c,
        rho_bar_L=o["rho_bar_L"], theta_G=o["theta_G"],
    )
    # Bornes de F3, B6, H5 et N6 qui mordent (argument strictement hors du domaine de la forme sans borne).
    # Un argument nul aux arrondis près (E^Bk + Π^Bk sous ϑ = 0 et ϖ = 0) n'est pas compté.
    seuil = TOL_SENTIER * abs(o["D_F"])
    o1["_planchers"] = (tresorerie_F < -seuil) + (exces_Bk < -seuil) + (C_plan != C_regle) + (v != d)
    return o1


# --- Application détendancée, jacobienne, spectre --------------------------------


def perturbables(par: Parametres, cfg: Config) -> tuple[str, ...]:
    """Grandeurs perturbées : r̂* est inerte sous un taux exogène (BC2 sans gain) ; E^Bk est identiquement nul
    sans exigence de fonds propres (ϑ = 0 : B6 verse tout le résultat), et son coude en 0 n'est pas perturbé."""
    cles = cles_etat(par.n_a)
    return tuple(k for k in cles if not (k == "r_hat" and cfg.taux == "exogene")
                 and not (k == "E_Bk" and par.vartheta == 0.0))


SEUIL_NUL = 1e-9  # en deçà de cette fraction des dépôts des entreprises, un montant est tenu pour nul


def echelle(o: dict[str, float], k: str) -> float:
    """Échelle de l'écart de `k` : |valeur|, sauf montant nul (ou résidu d'arrondi d'un montant nul, comme E^Bk
    sous ϑ = 0), rapporté au salaire de l'ouverture."""
    if k in NOMINAUX and abs(o[k]) <= SEUIL_NUL * abs(o["D_F"]):
        return abs(o["W_m1"])
    return abs(o[k]) if o[k] != 0.0 else abs(o["W_m1"])


def echelles(o: dict[str, float], cles: tuple[str, ...]) -> np.ndarray:
    return np.array([echelle(o, k) for k in cles])


def application(o0, par, cfg, cles, s, f):
    """x ↦ x' : écarts relatifs détendanciés d'un pas, autour de l'ouverture `o0`."""

    def phi(x: np.ndarray) -> np.ndarray:
        o = dict(o0)
        for k, sk, xk in zip(cles, s, x):
            o[k] = o0[k] + sk * xk
        o1 = pas(o, par, cfg)
        return np.array([(o1[k] / f[k] - o0[k]) / sk for k, sk in zip(cles, s)])

    return phi


def jacobienne(phi, m: int) -> tuple[np.ndarray, float]:
    """Jacobienne de `phi` en 0 par différences centrées, et contrôle de dérivabilité : plus grand écart
    entre différences avant et arrière, sur les colonnes dont la ligne de J n'est pas nulle (une colonne
    à ligne nulle ne change pas le spectre)."""
    J = np.empty((m, m))
    coude = np.empty(m)
    z = phi(np.zeros(m))
    for j in range(m):
        e = np.zeros(m)
        e[j] = PAS_DIFF
        plus, moins = phi(e), phi(-e)
        J[:, j] = (plus - moins) / (2 * PAS_DIFF)
        coude[j] = np.max(np.abs((plus - z) - (z - moins))) / PAS_DIFF
    actives = np.max(np.abs(J), axis=1) > 0.0
    return J, float(np.max(coude[actives], initial=0.0))


def direction_nominale(o0, cles, s) -> np.ndarray:
    """Direction h d'une homothétie des grandeurs nominales (prix, salaire, montants), en écarts relatifs."""
    nominales = set(NOMINAUX) | {k for k in cles if k.startswith("P") and k[1:].isdigit()}
    return np.array([o0[k] / sk if k in nominales else 0.0 for k, sk in zip(cles, s)])


@dataclass
class Spectre:
    rayon: float  # module dominant hors racine nominale
    valeur: complex  # valeur propre dominante
    homogeneite: float  # ‖J h − h‖∞
    racine_retiree: complex  # valeur propre retirée (contrôle : ≈ 1)
    racine_restante: complex | None  # racine de J déflatée à |λ − 1| ≤ TOL_RACINE_NOMINALE (contrôle : aucune)
    periode: float | None  # en pas, si la dominante est complexe
    demi_vie: float | None  # en pas, si rayon < 1


def spectre(J: np.ndarray, h: np.ndarray | None, i_pivot: int | None) -> Spectre:
    """Spectre de J, racine nominale retirée par déflation de Wielandt si h est donné."""
    homog, retiree, restante = 0.0, complex(math.nan), None
    if h is not None:
        homog = float(np.max(np.abs(J @ h - h)))
        w = np.zeros_like(h)
        w[i_pivot] = 1.0 / h[i_pivot]
        lam_avant = np.linalg.eigvals(J)
        J = J - np.outer(h, w)
        lam = np.linalg.eigvals(J)
        # Contrôle : la valeur propre disparue (remplacée par 0) est celle la plus proche de 1.
        retiree = complex(lam_avant[np.argmin(np.abs(lam_avant - 1))])
        # Contrôle : la déflation n'a retiré qu'une racine, aucune autre ne reste à |λ − 1| sous la tolérance.
        proche = complex(lam[np.argmin(np.abs(lam - 1))])
        restante = proche if abs(proche - 1) <= TOL_RACINE_NOMINALE else None
    else:
        lam = np.linalg.eigvals(J)
    # Ordre canonique : module décroissant, puis partie imaginaire positive d'abord.
    ordre = sorted(range(len(lam)), key=lambda i: (-round(abs(lam[i]), 12), -lam[i].imag))
    dom = complex(lam[ordre[0]])
    rayon = abs(dom)
    arg = abs(cmath.phase(dom))
    periode = 2 * math.pi / arg if dom.imag != 0 and arg > 1e-12 else None
    demi_vie = math.log(0.5) / math.log(rayon) if 0 < rayon < 1 else None
    return Spectre(rayon, dom, homog, retiree, restante, periode, demi_vie)


def residu_sentier(o0, par, cfg) -> float:
    """Plus grand écart relatif entre le pas de `o0` et le sentier stationnaire (contrôle de transcription)."""
    f = facteurs_sentier(par)
    o1 = pas(o0, par, cfg)
    cles = cles_etat(par.n_a) + EXOGENES
    return max(abs(o1[k] / f[k] - o0[k]) / echelle(o0, k) for k in cles)


# --- État stationnaire d'une variante (Newton, θ_G de fermeture) ----------------


@dataclass
class Stationnaire:
    ouverture: dict[str, float]
    iterations: int
    residu: float
    theta_G: float


def stationnaire_variante(par: Parametres, cfg: Config) -> Stationnaire:
    """État stationnaire de la configuration sur le sentier π̄ = π*, θ_G de fermeture, W_{t−1} tenu.

    Inconnues : écarts relatifs des grandeurs perturbables, sauf W_{t−1} (normalisation nominale) et
    r̂* (tenu à r̄, lecture (e) de la décision M32 : sous la règle active, BC2 est stationnaire pour
    tout r̂* dès que π = π*, et son équation est retirée), plus θ_G. Équations : x' = x. Point de
    départ : l'état résolu de F retenue. Newton à jacobienne par différences centrées, au plus
    `ITERATIONS_NEWTON` itérations ; un pas qui sort du domaine des flottants arrête la résolution,
    dont le résidu publié est alors infini.
    """
    base = ouverture_resolue(par)
    f = facteurs_sentier(par)
    cles = perturbables(par, cfg)
    s = echelles(base, cles)
    m = len(cles)
    libres = [i for i, k in enumerate(cles) if k not in ("W_m1", "r_hat")]
    equations = [i for i, k in enumerate(cles) if k != "r_hat"]
    q = len(libres) + 1

    def ouvrir(u: np.ndarray) -> dict[str, float]:
        x = np.zeros(m)
        x[libres] = u[:-1]
        o = dict(base)
        for k, sk, xk in zip(cles, s, x):
            o[k] = base[k] + sk * xk
        o["theta_G"] = base["theta_G"] * (1 + u[-1])
        return o

    def residu(u: np.ndarray) -> np.ndarray:
        o = ouvrir(u)
        o1 = pas(o, par, cfg)
        r = np.array([(o1[k] / f[k] - o[k]) / sk for k, sk in zip(cles, s)])
        return r[equations]

    u = np.zeros(q)
    it = 0
    try:
        r = residu(u)
        while np.max(np.abs(r)) > TOL_NEWTON and it < ITERATIONS_NEWTON:
            Jr = np.empty((q, q))
            for j in range(q):
                e = np.zeros(q)
                e[j] = PAS_DIFF
                Jr[:, j] = (residu(u + e) - residu(u - e)) / (2 * PAS_DIFF)
            u = u - np.linalg.solve(Jr, r)
            r = residu(u)
            it += 1
        res = float(np.max(np.abs(r)))
    except (OverflowError, ValueError, np.linalg.LinAlgError):
        res = math.inf
    o = ouvrir(u)
    return Stationnaire(o, it, res, o["theta_G"])


def rayon_conjoint(par: Parametres, cfg: Config) -> dict[str, object]:
    """Rayon de la boucle conjointe hors racine nominale, à l'état stationnaire de la configuration."""
    st = stationnaire_variante(par, cfg)
    o0 = st.ouverture
    f = facteurs_sentier(par)
    cles = perturbables(par, cfg)
    s = echelles(o0, cles)
    J, coude = jacobienne(application(o0, par, cfg, cles, s, f), len(cles))
    h = direction_nominale(o0, cles, s)
    sp = spectre(J, h, cles.index("W_m1"))
    planchers = pas(o0, par, cfg)["_planchers"]
    return {"spectre": sp, "coude": coude, "newton": st.iterations, "residu_stationnaire": st.residu,
            "theta_G": st.theta_G, "planchers_actifs": int(planchers), "L/K": o0["L"] / o0["K"],
            "L/(P K^vol)": o0["L"] / (o0["P0"] * facteurs_sentier(par)["P0"] * o0["K_vol"])}


# --- Boucle propre et boucle réduite (`sec:investissement-conditions`) -----------


def rayon_boucle_propre(par: Parametres) -> Spectre:
    """Capital en volume et part visée, à demande, prix et taux exogènes (y sur son sentier)."""
    n = par.n_a
    Gr = ((1 + par.g_pr) * (1 + par.g_N)) ** (1 / n)
    k0 = n * par.kappa / par.tu_bar  # K^vol / y
    ti0 = (Gr - 1 + par.delta / n) * k0

    def phi(x):
        k, ti = k0 * (1 + x[0]), ti0 * (1 + x[1])
        tu = n * par.kappa / k  # N11
        k1 = ((1 - par.delta / n) * k + ti) / Gr  # N10 et S3 (I^vol = ti y_t), détendancé
        ti1 = ti * math.exp(par.lambda_ti / n * (tu - par.tu_bar))  # S6
        return np.array([k1 / k0 - 1, ti1 / ti0 - 1])

    J, _ = jacobienne(phi, 2)
    return spectre(J, None, None)


def part_autonome(par: Parametres, m: float) -> float:
    """A de la condition de domaine (`sec:investissement-conditions`), fraction de la production."""
    n = par.n_a
    Gr = ((1 + par.g_pr) * (1 + par.g_N)) ** (1 / n)
    v_sur_y = 1 / (1 + n * par.sigma * (Gr - 1))
    return v_sur_y - m / Gr - (n * (Gr - 1) + par.delta) * par.kappa / par.tu_bar


def rayon_boucle_reduite(par: Parametres, m: float) -> Spectre:
    """Production (N1 à N7, N10, N11) et S3, S6 ; d = A + m y_{t−1} + I^{vol,plan} ; prix et taux exogènes."""
    n = par.n_a
    Gr = ((1 + par.g_pr) * (1 + par.g_N)) ** (1 / n)
    A = part_autonome(par, m)
    y0 = 1.0
    v0 = y0 / (1 + n * par.sigma * (Gr - 1))
    z0 = np.array([v0, n * par.sigma * v0, n * par.kappa * y0 / par.tu_bar,
                   (Gr - 1 + par.delta / n) * n * par.kappa / par.tu_bar, y0 / Gr])

    def phi(x):
        ve, IN_vol, K_vol, ti, y_m1 = z0 * (1 + x)
        IN_star = n * par.sigma * ve  # N2
        y = max(0.0, ve + (Gr - 1) * IN_star + par.lambda_IN / n * (IN_star - IN_vol))  # N3, N5 (travail non lié)
        I_plan = ti * Gr * y_m1  # S3, Δϱ = 0
        d = A * y0 + m * y_m1 + I_plan
        v = min(d, IN_vol + y)  # N6
        tu = y / (K_vol / (n * par.kappa))  # N11
        z1 = np.array([
            Gr * ((1 - par.lambda_v / n) * ve + par.lambda_v / n * d),  # N1
            IN_vol + y - v,  # N7
            (1 - par.delta / n) * K_vol + v / d * I_plan,  # N10
            ti * math.exp(par.lambda_ti / n * (tu - par.tu_bar)),  # S6
            y,
        ])
        z1[[0, 1, 2, 4]] /= Gr  # détendancé (volumes)
        return z1 / z0 - 1

    J, _ = jacobienne(phi, 5)
    return spectre(J, None, None)


def seuil_lambda_ti(par: Parametres, m: float) -> float | None:
    """Plus petite λ_ti (par an) où le rayon de la boucle réduite atteint 1 : balayage puis bissection.

    None si le rayon reste sous 1 sur toute la grille ; refus (ValueError) si le rayon atteint déjà 1 au
    premier point de la grille : le seuil, inférieur à ce point, n'y est pas encadré. `calculer` publie alors
    le seuil sans mesure et en fait un contrôle en échec (code de sortie 2).
    """
    grille = [0.002 * k for k in range(1, 501)]  # 0,002 à 1 par an
    precedent = None
    for lam in grille:
        r = rayon_boucle_reduite(replace(par, lambda_ti=lam), m).rayon
        if r >= 1:
            if precedent is None:
                raise ValueError(f"rayon {r!r} ≥ 1 dès le premier point de la grille (λ_ti = {lam}) : seuil non "
                                 "encadré")
            bas, haut = precedent, lam
            for _ in range(40):
                mil = 0.5 * (bas + haut)
                if rayon_boucle_reduite(replace(par, lambda_ti=mil), m).rayon >= 1:
                    haut = mil
                else:
                    bas = mil
            return 0.5 * (bas + haut)
        precedent = lam
    return None


# --- Valeurs publiées et comparaison ----------------------------------------------


def config_fiche(par: Parametres) -> Parametres:
    """Hypothèses de la boucle conjointe de la fiche § 3.N : i_L = i_D = 3 %, sans banque ni impôt."""
    return replace(par, varpi_L=0.0, varpi_D=0.0, vartheta=0.0, tau_H=0.0, tau_F=0.0,
                   rbar=1.03 / (1 + par.pi_cible) - 1)


def decimales(publie: str) -> int:
    return len(publie.split(",")[1]) if "," in publie else 0


TOL_ENVIRON = 0.005  # valeur publiée « environ » : écart relatif admis


def ligne(objet: str, publie: str | None, mesure: float | None, source: str,
          environ: bool = False) -> dict[str, object]:
    """Une ligne du tableau : publié (texte), remesuré, écart ; concordance à la dernière décimale publiée
    (arrondi au plus proche), ou à `TOL_ENVIRON` près en relatif pour une valeur publiée « environ »."""
    lig = {"objet": objet, "publie": publie, "remesure": mesure, "source": source}
    if publie is not None and mesure is not None:
        v = float(publie.replace(",", "."))
        lig["ecart"] = mesure - v
        if environ:
            lig["concorde"] = abs(mesure / v - 1) <= TOL_ENVIRON
        else:
            lig["concorde"] = abs(mesure - v) <= 0.5 * 10 ** (-decimales(publie)) * (1 + 1e-9)
    return lig


def calculer(par: Parametres | None = None) -> dict[str, object]:
    """Toutes les mesures, dans un ordre fixe."""
    par = Parametres() if par is None else par
    deux = replace(par, lambda_ti=2 * par.lambda_ti)
    demi = replace(par, lambda_ti=par.lambda_ti / 2)
    lignes: list[dict[str, object]] = []
    controles: dict[str, float] = {}

    # Contrôle de transcription : le pas d'un état résolu reste sur le sentier.
    for nom, p_ in (("socle", par), ("fiche", config_fiche(par))):
        for reg in ("hausse", "baisse"):
            for taux in ("exogene", "regle"):
                controles[f"sentier {nom} {reg} {taux}"] = residu_sentier(ouverture_resolue(p_), p_,
                                                                          Config(regime=reg, taux=taux))

    # 1. Boucle conjointe : F retenue et variantes écartées.
    conjoint: list[dict[str, object]] = []
    cas = [
        ("F retenue", "comptable", "ve", {"x2": "0,9971", "x1": "0,9980"}),
        ("levier sur p K^vol (p̂, K^vol d'ouverture)", "pK_phat_ouv", "ve", {"x2": "1,0530"}),
        ("levier sur p K^vol (p̂, après investissement)", "pK_phat_apres", "ve", {}),
        ("levier sur p K^vol (P_{t−1}, K^vol d'ouverture)", "pK_pm1_ouv", "ve", {}),
        ("levier sur p K^vol (P_{t−1}, après investissement)", "pK_pm1_apres", "ve", {}),
        ("dépôts sur les ventes du pas, levier comptable", "comptable", "ventes_du_pas", {"x2": "1,4991"}),
        ("dépôts sur les ventes du pas, levier sur p K^vol", "pK_phat_ouv", "ventes_du_pas", {"x2": "1,4925"}),
    ]
    for nom_conf, p_conf in (("socle", par), ("fiche", config_fiche(par))):
        for vitesse, p_v in (("x1", p_conf), ("x2", replace(p_conf, lambda_ti=2 * p_conf.lambda_ti))):
            for libelle, cr, dep, publies in cas:
                for reg in ("hausse", "baisse"):
                    for taux in ("exogene", "regle"):
                        if taux == "regle" and nom_conf == "fiche":
                            continue  # la fiche mesure à taux exogène ; i_L = i_D n'a pas de règle déclarée
                        res = rayon_conjoint(p_v, Config(credit=cr, depots=dep, regime=reg, taux=taux))
                        sp = res["spectre"]
                        controles[f"homogénéité {nom_conf} {vitesse} {cr} {dep} {reg} {taux}"] = sp.homogeneite
                        # Une racine restée près de 1 après déflation fait échouer le contrôle (valeur infinie).
                        controles[f"racine retirée − 1 {nom_conf} {vitesse} {cr} {dep} {reg} {taux}"] = abs(
                            sp.racine_retiree - 1) if sp.racine_restante is None else math.inf
                        controles[f"Newton {nom_conf} {vitesse} {cr} {dep} {reg} {taux}"] = res[
                            "residu_stationnaire"]
                        controles[f"coude {nom_conf} {vitesse} {cr} {dep} {reg} {taux}"] = res["coude"]
                        conjoint.append({
                            "configuration": nom_conf, "lambda_ti": p_v.lambda_ti, "vitesse": vitesse,
                            "variante": libelle, "credit": cr, "depots": dep, "regime": reg, "taux": taux,
                            "rayon": sp.rayon, "dominante": [sp.valeur.real, sp.valeur.imag],
                            "periode_pas": sp.periode, "demi_vie_pas": sp.demi_vie,
                            "theta_G": res["theta_G"], "iterations_newton": res["newton"],
                            "planchers_actifs": res["planchers_actifs"], "L/K": res["L/K"],
                            "L/(p K^vol)": res["L/(P K^vol)"], "publie": publies.get(vitesse),
                        })

    def r_conj(conf, vit, cr, dep, reg, taux="exogene"):
        return next(c["rayon"] for c in conjoint if (c["configuration"], c["vitesse"], c["credit"], c["depots"],
                                                       c["regime"], c["taux"]) == (conf, vit, cr, dep, reg, taux))

    for conf in ("fiche", "socle"):
        for reg in ("hausse", "baisse"):
            src = f"conjointe, config. {conf}, régime de {reg}, taux exogène"
            lignes.append(ligne(f"F retenue, λ_ti × 2 [{src}]", "0,9971",
                                r_conj(conf, "x2", "comptable", "ve", reg), "fiche § 3.N"))
            lignes.append(ligne(f"F retenue, λ_ti de base [{src}]", "0,9980",
                                r_conj(conf, "x1", "comptable", "ve", reg), "fiche § 3.N (précision)"))
            vals = [r_conj(conf, "x2", cr, "ve", reg) for cr in CREDITS if cr != "comptable"]
            lignes.append(ligne(f"levier sur p K^vol, min des 4 écritures, λ_ti × 2 [{src}]", "1,0528", min(vals),
                                "fiche § 3.N ; sec:ecartees"))
            lignes.append(ligne(f"levier sur p K^vol, max des 4 écritures, λ_ti × 2 [{src}]", "1,0538", max(vals),
                                "fiche § 3.N ; sec:ecartees"))
            lignes.append(ligne(f"dépôts sur les ventes du pas, levier comptable, λ_ti × 2 [{src}]", "1,49",
                                r_conj(conf, "x2", "comptable", "ventes_du_pas", reg), "sec:ecartees ; fiche § 3.N"))
            lignes.append(ligne(f"dépôts sur les ventes du pas, levier comptable, λ_ti × 2 [{src}]", "1,4991",
                                r_conj(conf, "x2", "comptable", "ventes_du_pas", reg), "fiche § 3.N"))
            lignes.append(ligne(f"dépôts sur les ventes du pas et levier sur p K^vol, λ_ti × 2 [{src}]", "1,4925",
                                r_conj(conf, "x2", "pK_phat_ouv", "ventes_du_pas", reg), "fiche § 3.N"))

    # 2. Boucle propre.
    for lib, p_, pub in (("base", par, "0,99793"), ("λ_ti / 2", demi, "0,99923"), ("λ_ti × 2", deux, "0,9971")):
        sp = rayon_boucle_propre(p_)
        lignes.append(ligne(f"boucle propre, module dominant, {lib}", pub, sp.rayon, "sec:investissement-conditions"))
        if lib == "base":
            lignes.append(ligne("boucle propre, demi-vie (tours), base", "334", sp.demi_vie,
                                "sec:investissement-conditions"))
        if lib == "λ_ti / 2":
            lignes.append(ligne("boucle propre, demi-vie (tours), λ_ti / 2", "902", sp.demi_vie,
                                "sec:investissement-conditions"))
        if lib == "λ_ti × 2":
            lignes.append(ligne("boucle propre, demi-vie (tours), λ_ti × 2", "239", sp.demi_vie,
                                "sec:investissement-conditions"))
            lignes.append(ligne("boucle propre, période (tours), λ_ti × 2", "2360", sp.periode,
                                "sec:investissement-conditions (« environ »)", environ=True))
    n = par.n_a
    Gr = ((1 + par.g_pr) * (1 + par.g_N)) ** (1 / n)
    lignes.append(ligne("boucle propre, approximation √((1 − δ/n_a)/(1 + g)^{1/n_a})", "0,99709",
                        math.sqrt((1 - par.delta / n) / Gr), "sec:investissement-conditions"))

    # 3. Boucle réduite investissement – demande.
    par3 = replace(par, kappa=3 * par.tu_bar)  # 3 ans de capital
    for m, pub in ((0.6, "0,2590"), (0.7, "0,1592"), (0.8, "0,0594")):
        lignes.append(ligne(f"domaine A, m = {m}, 2 ans", pub, part_autonome(par, m), "sec:investissement-conditions"))
    lignes.append(ligne("domaine A, m = 0.8, 3 ans", "-0,0104", part_autonome(par3, 0.8),
                        "sec:investissement-conditions"))
    publies = {("base", 0.6): "0,9975", ("base", 0.7): "0,9977", ("base", 0.8): "0,9986",
               ("λ_ti / 2", 0.6): "0,9992", ("λ_ti / 2", 0.7): "0,9991", ("λ_ti / 2", 0.8): "0,9987",
               ("λ_ti × 2", 0.6): "0,9978", ("λ_ti × 2", 0.7): "0,9983", ("λ_ti × 2", 0.8): "1,0003"}
    for (lib, m), pub in publies.items():
        p_ = {"base": par, "λ_ti / 2": demi, "λ_ti × 2": deux}[lib]
        lignes.append(ligne(f"boucle réduite, rayon, {lib}, m = {m}, 2 ans", pub, rayon_boucle_reduite(p_, m).rayon,
                            "sec:investissement-conditions"))
    for p_, ans, m, pub in ((par, 2, 0.6, "0,157"), (par, 2, 0.7, "0,097"), (par, 2, 0.8, "0,036"),
                            (par3, 3, 0.6, "0,077"), (par3, 3, 0.7, "0,037")):
        try:
            seuil = seuil_lambda_ti(p_, m)
        except ValueError:
            # Seuil non encadré : contrôle en échec (valeur infinie), seuil publié sans mesure.
            seuil = None
            controles[f"seuil de λ_ti encadré, m = {m}, {ans} ans"] = math.inf
        lignes.append(ligne(f"boucle réduite, seuil de λ_ti (par an), m = {m}, {ans} ans", pub, seuil,
                            "sec:investissement-conditions"))

    # 4. Racine lente du capital comptable et du crédit, sans levier (forme fermée de la spécification).
    Pp = (1 + par.pi_cible) ** (1 / n)
    lignes.append(ligne("racine lente du capital comptable, lv* = 0, π̄ = 2 %", "0,99255",
                        (1 - par.delta / n) / (Gr * Pp), "sec:investissement-conditions"))

    return {"lignes": lignes, "conjoint": conjoint, "controles": controles}


def controles_passent(r: dict[str, object]) -> bool:
    """Vrai si chaque contrôle interne est sous sa tolérance ; une valeur absente ou non finie (`None` après
    passage par JSON, `inf` d'une résolution qui diverge) est un échec."""
    c = r["controles"]
    ok = True
    for k, v in c.items():
        if v is None or not math.isfinite(v):
            return False
        if k.startswith("coude"):
            ok &= v <= TOL_COUDE
        elif k.startswith("sentier"):
            ok &= v <= TOL_SENTIER
        elif k.startswith("homogénéité"):
            ok &= v <= TOL_HOMOGENEITE
        elif k.startswith("racine retirée"):
            ok &= v <= TOL_RACINE_NOMINALE
        elif k.startswith("Newton"):
            ok &= v <= TOL_NEWTON
    return bool(ok)


def _f(x, chiffres=6) -> str:
    if x is None:
        return "—"
    return f"{x:.{chiffres}f}"


def afficher(r: dict[str, object], sortie=None) -> None:
    sortie = sys.stdout if sortie is None else sortie
    print("Contre-épreuve indépendante de la fiche 6 (#66) : publié, remesuré, écart", file=sortie)
    print(file=sortie)
    print("| Grandeur | Publié | Remesuré | Écart | Concorde | Source |", file=sortie)
    print("|---|---|---|---|---|---|", file=sortie)
    for lig in r["lignes"]:
        ec = lig.get("ecart")
        conc = {True: "oui", False: "non", None: "—"}[lig.get("concorde")]
        print(f"| {lig['objet']} | {lig['publie']} | {_f(lig['remesure'])} | "
              f"{'—' if ec is None else f'{ec:+.6f}'} | {conc} | {lig['source']} |", file=sortie)
    print(file=sortie)
    print("Boucle conjointe, détail (rayon hors racine nominale ; période et demi-vie en pas) :", file=sortie)
    print("| Config. | λ_ti | Crédit | Dépôts | Régime | Taux | Rayon | Dominante | Période | Demi-vie | "
          "θ_G | Newton | Planchers | L/K | L/(p K^vol) |", file=sortie)
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|", file=sortie)
    for c in r["conjoint"]:
        dom = complex(*c["dominante"])
        print(f"| {c['configuration']} | {c['lambda_ti']:.2f} | {c['credit']} | {c['depots']} | {c['regime']} | "
              f"{c['taux']} | {c['rayon']:.6f} | {dom.real:+.6f}{dom.imag:+.6f}i | {_f(c['periode_pas'], 1)} | "
              f"{_f(c['demi_vie_pas'], 1)} | {c['theta_G']:.6f} | {c['iterations_newton']} | "
              f"{c['planchers_actifs']} | {c['L/K']:.6f} | {c['L/(p K^vol)']:.6f} |", file=sortie)
    print(file=sortie)
    pires = {}
    for k, v in r["controles"].items():
        famille = k.split(" ")[0]
        pires[famille] = max(pires.get(famille, 0.0), v)
    print("Contrôles internes (pire cas) : " + " ; ".join(f"{k} {v:.2e}" for k, v in sorted(pires.items())),
          file=sortie)
    print(f"Contrôles : {'passent' if controles_passent(r) else 'ÉCHEC'}", file=sortie)


def _jsonable(x):
    if isinstance(x, dict):
        return {k: _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        return x.item()
    if isinstance(x, float) and not math.isfinite(x):
        return None
    return x


def main(arguments: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", type=Path, help="écrit les résultats en JSON")
    ap.add_argument("--chrono", action="store_true", help="publie le temps de calcul (non déterministe)")
    args = ap.parse_args(arguments)
    t0 = time.perf_counter()
    r = calculer()
    duree = time.perf_counter() - t0
    afficher(r)
    if args.chrono:
        print(f"Durée : {duree:.2f} s")
    if args.json:
        args.json.write_text(json.dumps(_jsonable(r), ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if controles_passent(r) else 2


if __name__ == "__main__":
    sys.exit(main())
