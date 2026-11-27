"""État stationnaire du socle en formes fermées : résolveur, module feuille de `scenarios/` (ADR 0015).

Les formes sont celles des huit sections `sec:<bloc>-stationnaire` de la
spécification, dans l'ordre triangulaire de la part de `macro` (issue #84,
§ 3) : cadre et taux, offre, financement des entreprises, banque, ménages et
impôt (forme fermée linéaire de la richesse), fermeture (part de la dépense
publique résolue, première lecture de #44, décision M32, lecture (e)), dette
(forme fermée linéaire de l'encaisse). Aucune boucle, aucun point fixe, aucune
bissection : la résolution numérique de la mesure (α) de #80 reste dans
`outils/etat_stationnaire.py`.

**Origine.** Ces fonctions sont déplacées d'`outils/etat_stationnaire.py`
(`facteurs`, `rho_IN`, `rho_K`, `etat_stationnaire`, conditions de
`controler_etat`, `ouverture` ; option R1, décision P247 du 26/11/2026), à
ordre d'opérations conservé : mêmes opérandes, même ordre, mêmes parenthèses,
mêmes appels (`**`, `math.exp`, `math.log`), aucune simplification algébrique.
Le script les importe et garde ses signatures comme adaptateurs ; sa sortie est
identique à l'octet (ADR 0015, point 3).

**Module feuille** (ADR 0015, point 6) : bibliothèque standard seule, aucun
module de `nations` ; fonctions pures sur des flottants (ni table, ni
`EtatPays`, ni variable de module modifiée, ni cache, ni graine). Aucun
argument optionnel ni drapeau de mode : r̂* et ϱ̄_L sont des arguments
obligatoires de `etat_stationnaire` ; la norme de l'état initial, ϱ̄_L = ϱ_L,
s'obtient par `taux`, que la résolution rappelle sur les mêmes opérandes
(Δϱ = 0,0 exactement) ; le calcul des formes (`etat_stationnaire`) et le
relevé des conditions d'existence violées (`relever_conditions`) sont deux
fonctions distinctes.

**Hypothèses structurelles et conventions** (ADR 0015, point 10). Les formes
fermées supposent E^CB_0 = 0 (M32), B_H = 0 (M27, C42) et ς_L = ς_B = 0
(placement réussi, `sec:banque-stationnaire`) : ce sont des **hypothèses
structurelles du résolveur**, fixées dans les formes et non paramétrables
(aucune entrée ne les porte). Les conventions de sélection sur le continuum
d'équilibres, elles, s'appliquent chez l'appelant, jamais par défaut ici :
r̂*_0 (r̂* = r̄ pour l'état initial), la norme ϱ̄_L (ϱ̄_L = ϱ_{L,0}, par
`taux`), et les normalisations p_0, pr_0, N^pa_0 (entrées ; l'état est
homogène de degré un en ces échelles).

**Concordance.** Les sections `sec:<bloc>-stationnaire` ne numérotent aucune
équation : les formes ne portent aucune balise d'équation ; chaque étape
renvoie à sa section par un commentaire `# sec:<bloc>-stationnaire` (P252 ;
ADR 0015, point 11). Leur lien à la spécification est tenu par les valeurs
publiées du script et par la stationnarité exacte du moteur (critère A2).

**Conversions.** Les formes sont écrites à n_a quelconque (le script les évalue
à n_a ∈ {4 ; 12 ; 52}) : leurs divisions par n_a et puissances en 1/n_a ne
passent pas par `nations.moteur.conversions`, exemption fermée et nommée du
test « conversion unique » (ADR 0015, point 13 ; décision S1).

**Valeurs rendues.** Entrées en dataclasse gelée ; résultats (`Facteurs`,
`Taux`, `EtatStationnaire`, `Ouverture`) en n-uplets nommés, immuables, à
champs fixes déclarés, chacun avec son unité (ADR 0015, point 6.4) : leur
construction est plus rapide que celle d'une dataclasse gelée de 89 champs
(rapport 2,6, mesure indicative du 26/11/2026, hors plateforme de référence),
et la mesure (α) du script appelle la résolution quelque 62 000 fois par
exécution.

Unités : u.m. (unité monétaire), u.v. (unité de volume), personnes ; « par
pas » pour un flux, « d'ouverture » pour un stock ; taux annuels en fraction
par an, facteurs par pas sans dimension.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import NamedTuple


@dataclass(frozen=True)
class EntreesStationnaires:
    """Entrées du résolveur, sous les noms des tables du moteur (ADR 0015, point 7).

    Champs obligatoires, sans valeur par défaut : le type ne porte aucune valeur de référence
    (celles du moteur restent dans les tables, celles du script dans ses `Parametres`). Aucune
    vitesse, aucun gain, aucune entrée de scénario n'y figure : une vitesse d'ajustement ne
    détermine pas l'état d'arrivée. ζ et η_r sont des élasticités de niveau, sans effet sous
    Δϱ = 0. Les entrées de scénario ς_L et ς_B n'y figurent pas : ς_L = ς_B = 0 est une
    hypothèse structurelle des formes (placement réussi). Le domaine est plus large que celui des tables (n_a ≠ 12, ν_G = 1) : seul n_a, entier
    ≥ 1, est contrôlé ici ; les domaines de définition restent ceux des tables (moteur) et de
    `controler_domaine` (script).
    """

    pas_par_an: int  # n_a, pas par an
    g_pr: float  # croissance de la productivité, par an
    sigma: float  # σ, durée de stock visée, années de ventes
    kappa: float  # κ, coefficient de capital, années
    g_N: float  # croissance de la population active, par an
    U_eq: float  # U^eq, chômage d'équilibre, fraction de la population active
    mu_bar: float  # μ̄, marge visée, fraction du coût unitaire
    nu_H: float  # ν_H, richesse visée, années de revenu de Haig-Simons
    delta: float  # δ, dépréciation, par an
    tu_bar: float  # t̄u, utilisation normale, fraction de la capacité normale
    lv_etoile: float  # lv*, levier visé, fraction du capital comptable
    nu_F: float  # ν_F, dépôts visés des entreprises, années de ventes
    zeta: float  # ζ, élasticité de l'utilisation visée, par unité de taux réel annuel
    eta_r: float  # η_r, élasticité de l'investissement, par unité de taux réel annuel
    varpi_L: float  # ϖ_L, écart du taux des crédits, par an
    varpi_D: float  # ϖ_D, écart du taux des dépôts, par an
    vartheta: float  # ϑ, fonds propres visés, fraction des crédits
    pi_etoile: float  # π*, cible d'inflation, par an (π̄ = π*)
    r_bar: float  # r̄, taux réel de Fisher sur la cible (taux de référence de E4), par an
    theta_CB: float  # θ_CB, part du besoin d'émission achetée par la banque centrale
    tau_H: float  # τ_H, taux de l'impôt des ménages, fraction de l'assiette
    tau_F: float  # τ_F, taux de l'impôt des entreprises, fraction de l'assiette
    theta_Tr: float  # θ_Tr, transferts, fraction de la production potentielle
    phi: float  # φ, couverture des intérêts, sans dimension, {0 ; 1}
    nu_G: float  # ν_G, compte du Trésor visé, multiple des paiements bruts d'un pas
    p_0: float  # normalisation du prix, u.m. par u.v.
    pr_0: float  # normalisation de la productivité, u.v. par personne et par pas
    N_pa_0: float  # population active, personnes

    def __post_init__(self) -> None:
        n = self.pas_par_an
        if isinstance(n, bool) or not isinstance(n, int) or n < 1:
            raise ValueError(f"pas_par_an = {n!r} : entier ≥ 1 attendu (formes définies à n_a ≥ 1)")


class Facteurs(NamedTuple):
    """Facteurs du cadre (`sec:cadre-calendrier`), sans dimension."""

    g: float  # croissance réelle annuelle (1 + g_pr)(1 + g_N) − 1, par an
    Gr: float  # G_r, facteur réel par pas
    Pp: float  # Π_p, facteur des prix par pas
    Gam: float  # Γ̄, facteur nominal par pas
    gam: float  # γ̄ = Γ̄ − 1, par pas
    pis: float  # π^pas = Π_p − 1, par pas


class Taux(NamedTuple):
    """Taux de l'état stationnaire (BC1 au point fixe, B1, B2, E4, S1), fractions par an."""

    i_CB: float  # taux directeur
    i_ref: float  # taux de référence de E4 (lecture A : paramètre r̄)
    i_L: float  # taux des crédits
    i_D: float  # taux des dépôts
    rho_L: float  # ϱ_L, taux réel des crédits


class EtatStationnaire(NamedTuple):
    """État stationnaire résolu : niveaux d'ouverture et flux du pas 0, dans l'ordre de calcul.

    Les noms et l'ordre des champs sont ceux des clés du dictionnaire du script d'état
    stationnaire, que son adaptateur reconstruit dans cet ordre. Flux en u.m. par pas, stocks
    en u.m. d'ouverture, volumes en u.v., sauf indication.
    """

    g: float  # croissance réelle annuelle, par an
    Gr: float  # G_r, facteur réel par pas
    Pp: float  # Π_p, facteur des prix par pas
    Gam: float  # Γ̄, facteur nominal par pas
    gam: float  # γ̄, par pas
    pis: float  # π^pas, par pas
    r_neutre: float  # r̂*, taux réel neutre de l'état, par an
    i_CB: float  # par an
    i_ref: float  # par an
    i_L: float  # par an
    i_D: float  # par an
    rho_L: float  # ϱ_L, par an
    rho_bar_L: float  # ϱ̄_L, norme de S2, par an
    d_rho: float  # Δϱ = ϱ_L − ϱ̄_L, par an
    p: float  # prix, u.m. par u.v.
    N_pa: float  # population active, personnes
    N: float  # emploi, personnes
    pr: float  # productivité, u.v. par personne et par pas
    y: float  # production, u.v. par pas
    y_pot: float  # production potentielle, u.v. par pas
    y_sur_v: float  # production sur ventes, sans dimension
    v: float  # ventes, u.v. par pas
    ve: float  # ventes anticipées, u.v. par pas
    UC: float  # coût unitaire, u.m. par u.v.
    W: float  # salaire, u.m. par personne et par pas
    WB: float  # masse salariale, u.m. par pas
    IN_vol: float  # stocks en volume, u.v. d'ouverture
    rho_IN: float  # ϱ̄_IN, valeur comptable des stocks sur le coût du pas, sans dimension
    IN: float  # stocks, u.m. d'ouverture
    dIN: float  # variation des stocks, u.m. par pas
    tu: float  # utilisation, fraction de la capacité normale
    K_vol: float  # capital en volume, u.v. d'ouverture
    rho_K: float  # ϱ̄_K, valeur comptable du capital sur le prix courant, sans dimension
    K: float  # capital, u.m. d'ouverture
    I_vol: float  # investissement en volume, u.v. par pas
    I: float  # investissement, u.m. par pas
    ti: float  # taux d'investissement, sans dimension
    PIB: float  # u.m. par pas
    U: float  # chômage, fraction de la population active
    y_cap: float  # capacité, u.v. par pas
    L: float  # crédits, u.m. d'ouverture
    D_F: float  # dépôts des entreprises, u.m. d'ouverture
    V_F: float  # valeur nette des entreprises, u.m. d'ouverture
    Pi_av: float  # profit avant impôt, u.m. par pas
    T_F: float  # impôt des entreprises, u.m. par pas
    FU: float  # profits non distribués, u.m. par pas
    Div_F: float  # dividendes des entreprises, u.m. par pas
    dL: float  # variation des crédits, u.m. par pas
    D1: float  # pôle de la richesse, sans dimension
    E_Bk: float  # fonds propres de la banque, u.m. d'ouverture
    Tr: float  # transferts, u.m. par pas
    t_cou: float  # taux de couverture des intérêts, par an
    A0: float  # revenu hors richesse, u.m. par pas
    c: float  # rendement marginal de la richesse net de l'érosion visée, par pas
    k: float  # ν_H n_a (1 − τ_H), pas
    D_H: float  # dépôts des ménages, u.m. d'ouverture
    V_H: float  # richesse des ménages, u.m. d'ouverture
    B_H: float  # titres des ménages, u.m. d'ouverture
    Y_HS: float  # revenu de Haig-Simons avant impôt, u.m. par pas
    D_c: float  # dette consolidée B − M^G − E^CB, u.m. d'ouverture
    T_cou: float  # couverture des intérêts, u.m. par pas
    T_H: float  # impôt des ménages, u.m. par pas
    Pi_Bk: float  # profit de la banque, u.m. par pas
    Div_Bk: float  # dividendes de la banque, u.m. par pas
    YD: float  # revenu disponible, u.m. par pas
    YD_HS: float  # revenu disponible de Haig-Simons, u.m. par pas
    C: float  # consommation, u.m. par pas
    G: float  # dépense publique, u.m. par pas
    theta_G: float  # θ_G, part de la dépense publique résolue, fraction de la production potentielle
    a: float  # i_CB/(n_a Γ̄), par pas
    X: float  # paiements hors intérêts sur l'encaisse, u.m. par pas
    D2: float  # existence de l'encaisse, sans dimension
    M_G: float  # compte du Trésor, u.m. d'ouverture
    M_G_star: float  # compte du Trésor visé, u.m.
    B: float  # dette brute, u.m. d'ouverture
    PB: float  # paiements bruts, u.m. par pas
    B_CB: float  # titres de la banque centrale, u.m. d'ouverture
    B_Bk: float  # titres de la banque, u.m. d'ouverture
    L_CB: float  # avances de la banque centrale, u.m. d'ouverture
    Res: float  # réserves, u.m. d'ouverture
    E_CB: float  # fonds propres de la banque centrale, u.m. d'ouverture
    Pi_CB: float  # profit de la banque centrale, u.m. par pas
    interets: float  # intérêts de la dette, u.m. par pas
    Em: float  # émission nette, u.m. par pas
    r_hat: float  # r̂*, par an
    pi_e: float  # π^e, par an
    existence_Bk_montant: float  # n_a Π^Bk − n_a γ̄ E^Bk, u.m. par an
    existence_Bk: float  # existence rapportée à L, par an (NaN si L = 0)
    marge_E1_montant: float  # ν_G PB − Γ̄ G, u.m. par pas


class Ouverture(NamedTuple):
    """État d'ouverture du pas 0, tel que les sections le résolvent (« État initial résolu »).

    Noms et ordre des clés du dictionnaire `ouverture` du script. `registre` porte les prix
    P_{t−u}, u = 1 … n_a + 1, en u.m. par u.v. ; `mu_tilde_m1` est la marge en logarithme
    d'ouverture μ̃_{−1} = ln(1 + μ̄) (ADR 0012, annotation du 13/11/2026, point 1.4 ; P54, #112).
    """

    registre: tuple[float, ...]  # u.m. par u.v.
    pr: float  # u.v. par personne et par pas
    N_pa: float  # personnes
    N_m1: float  # personnes
    U_m1: float  # fraction de la population active
    W_m1: float  # u.m. par personne et par pas
    mu_tilde_m1: float  # sans dimension
    ve: float  # u.v. par pas
    IN_vol: float  # u.v.
    IN: float  # u.m.
    K_vol: float  # u.v.
    K: float  # u.m.
    ti: float  # sans dimension
    y_m1: float  # u.v. par pas
    T_F_m1: float  # u.m. par pas
    rho_bar_L: float  # par an
    L: float  # u.m.
    D_F: float  # u.m.
    YD_m1: float  # u.m. par pas
    D_H: float  # u.m.
    B_H: float  # u.m.
    i_L: float  # par an
    i_D: float  # par an
    E_Bk: float  # u.m.
    L_CB: float  # u.m.
    Res: float  # u.m.
    B_Bk: float  # u.m.
    B_CB: float  # u.m.
    M_G: float  # u.m.
    E_CB: float  # u.m.
    r_hat: float  # par an
    pi_e: float  # par an
    pi_cible: float  # par an
    Y_HS_m1: float  # u.m. par pas
    theta_G: float  # fraction de la production potentielle


@dataclass(frozen=True)
class ConditionViolee:
    """Condition d'existence violée : identifiant (`CONDITIONS_D_EXISTENCE`), valeur, section."""

    identifiant: str
    valeur: float
    section: str


class EtatStationnaireInexistant(Exception):
    """Refus typé : l'état stationnaire n'existe pas (ADR 0015, point 8 ; décision S10).

    `conditions` : conditions d'existence violées, dans l'ordre de `CONDITIONS_D_EXISTENCE`.
    Hors de la famille `ArretMoteur`, que le script ne doit pas charger. Levée par
    `etat_stationnaire` à un pôle exact (D1 = 0 ou D2 = 0), où les formes ne sont pas définies.
    """

    def __init__(self, conditions: tuple[ConditionViolee, ...]) -> None:
        super().__init__("état stationnaire inexistant : " + " ; ".join(
            f"{c.identifiant} = {c.valeur!r} ({c.section})" for c in conditions))
        self.conditions = conditions


# Liste fermée des conditions d'existence, dans l'ordre du script (identifiant, condition,
# section de la spécification). L'ordre est celui du relevé et du premier refus.
CONDITIONS_D_EXISTENCE: tuple[tuple[str, str, str], ...] = (
    ("D1", "D1 > 0", "sec:menages-conditions"),
    ("D2", "D2 > 0", "sec:finances_publiques-conditions"),
    ("existence_dividende_banque", "n_a Π^Bk − n_a γ̄ E^Bk ≥ 0", "sec:banque-stationnaire"),
    ("Div_F", "Div_F ≥ 0", "sec:investissement-conditions"),
    ("theta_G", "θ_G > 0", "sec:finances_publiques-conditions"),
    ("marge_plafond_E1", "ν_G PB − Γ̄ G > 0", "sec:finances_publiques-conditions"),
    ("B", "B ≥ 0", "sec:finances_publiques-conditions"),
    ("B_Bk", "B_Bk ≥ 0", "sec:finances_publiques-conditions"),
    ("B_CB", "B_CB ≥ 0", "sec:finances_publiques-conditions"),
    ("B_H", "B_H = 0", "sec:finances_publiques-stationnaire"),
)
_SECTIONS = {identifiant: section for identifiant, _, section in CONDITIONS_D_EXISTENCE}


def _violee(identifiant: str, valeur: float) -> ConditionViolee:
    return ConditionViolee(identifiant, valeur, _SECTIONS[identifiant])


# --- Formes fermées ------------------------------------------------------------


def facteurs(n_a: int, g_pr: float, g_N: float, pi: float) -> Facteurs:
    """Facteurs du cadre (`sec:cadre-calendrier`) : G_r, Π_p, Γ̄, γ̄, π^pas, g."""
    g = (1 + g_pr) * (1 + g_N) - 1
    Gr = (1 + g) ** (1 / n_a)
    Pp = (1 + pi) ** (1 / n_a)
    Gam = ((1 + g) * (1 + pi)) ** (1 / n_a)
    return Facteurs(g=g, Gr=Gr, Pp=Pp, Gam=Gam, gam=Gam - 1, pis=Pp - 1)


def rho_IN(n_a: int, sigma: float, g: float, pi: float) -> float:
    """ρ̄_IN, valeur comptable des stocks rapportée au coût du pas (`sec:production-stationnaire`)."""
    Gr = (1 + g) ** (1 / n_a)
    Pp = (1 + pi) ** (1 / n_a)
    return 1 / (1 + (Pp - 1) * (1 + n_a * sigma / (1 + n_a * sigma * (Gr - 1))))


def rho_K(n_a: int, delta: float, g: float, pi: float) -> float:
    """ρ̄_K, valeur comptable du capital rapportée au prix courant (`sec:production-capital`)."""
    return (n_a * ((1 + g) ** (1 / n_a) - 1) + delta) / (n_a * (((1 + g) * (1 + pi)) ** (1 / n_a) - 1) + delta)


def taux(entrees: EntreesStationnaires, r_neutre: float) -> Taux:
    """Étape 1 de l'ordre triangulaire : taux de l'état (BC1 au point fixe, B1, B2, E4, S1).

    `r_neutre` : r̂* de l'état (BC1). Le taux de référence de E4 lit toujours r̄ (lecture A).
    La norme de l'état initial, ϱ̄_L = ϱ_L (M32, lecture (e)), est le champ `rho_L`.
    """
    pi = entrees.pi_etoile
    # sec:banque_centrale-stationnaire, sec:banque-stationnaire, sec:investissement-stationnaire
    i_CB = (1 + r_neutre) * (1 + pi) - 1
    i_ref = (1 + entrees.r_bar) * (1 + pi) - 1
    i_L = i_CB + entrees.varpi_L
    i_D = i_CB - entrees.varpi_D
    rho_L = (1 + i_L) / (1 + pi) - 1
    return Taux(i_CB=i_CB, i_ref=i_ref, i_L=i_L, i_D=i_D, rho_L=rho_L)


def etat_stationnaire(entrees: EntreesStationnaires, r_neutre: float, rho_bar_L: float) -> EtatStationnaire:
    """État stationnaire en formes fermées, ordre triangulaire de la part de `macro` (§ 3).

    `r_neutre` : taux réel neutre de l'état (r̂* de BC1) ; `rho_bar_L` : norme ϱ̄_L de S2. Les
    deux sont obligatoires ; l'état initial résolu prend r̂* = r̄ et ϱ̄_L = `taux(entrees,
    r̄).rho_L` (Δϱ = 0). Aucune condition d'existence n'est jugée ici (`relever_conditions`),
    sauf un pôle exact (D1 = 0 ou D2 = 0), où les formes ne sont pas définies :
    `EtatStationnaireInexistant`. Em ≤ 0 n'est pas une condition : Em = γ̄ B a le signe de γ̄.
    """
    n = entrees.pas_par_an
    f = facteurs(n, entrees.g_pr, entrees.g_N, entrees.pi_etoile)
    g, Gr, Gam, gam, pis = f.g, f.Gr, f.Gam, f.gam, f.pis
    pi = entrees.pi_etoile
    r = r_neutre
    # 1. Cadre et taux (BC1 au point fixe, B1, B2, E4, S1).
    t = taux(entrees, r)
    i_CB, i_ref, i_L, i_D, rho_L = t.i_CB, t.i_ref, t.i_L, t.i_D, t.rho_L
    rho_bar = rho_bar_L
    d_rho = rho_L - rho_bar
    # 2. Offre (blocs 2, 3, 4).
    # sec:production-stationnaire, sec:travail-stationnaire, sec:prix-stationnaire
    p = entrees.p_0
    N_pa = entrees.N_pa_0
    N = (1 - entrees.U_eq) * N_pa
    pr = entrees.pr_0
    y = pr * N
    y_pot = pr * (1 - entrees.U_eq) * N_pa
    y_sur_v = 1 + n * entrees.sigma * (Gr - 1)
    v = y / y_sur_v
    UC = p / (1 + entrees.mu_bar)
    W = UC * pr
    WB = W * N
    IN_vol = n * entrees.sigma * v
    rIN = rho_IN(n, entrees.sigma, g, pi)
    IN = rIN * UC * IN_vol
    dIN = gam * IN
    # sec:investissement-stationnaire
    tu = entrees.tu_bar * math.exp(entrees.zeta * d_rho)
    K_vol = n * entrees.kappa * y / tu
    rK = rho_K(n, entrees.delta, g, pi)
    K = rK * p * K_vol
    I_vol = (Gr - 1 + entrees.delta / n) * K_vol
    I = p * I_vol
    ti = (I_vol / y) * math.exp(entrees.eta_r * d_rho)
    PIB = p * v + dIN
    # 3. Financement des entreprises (bloc 6) : indépendant de G et de θ_G.
    # sec:investissement-stationnaire
    L = entrees.lv_etoile * K
    D_F = entrees.nu_F * n * p * v
    V_F = K + IN + D_F - L
    Pi_av = p * v + dIN - WB - entrees.delta * K / n - i_L * L / n + i_D * D_F / n
    T_F = entrees.tau_F * Pi_av
    FU = gam * V_F
    Div_F = Pi_av - T_F - FU
    # 4. Banque (bloc 7) ; 5. ménages et impôt (blocs 5 et 9) : forme fermée linéaire de D_H.
    # sec:banque-stationnaire, sec:menages-stationnaire, sec:finances_publiques-stationnaire
    E_Bk = entrees.vartheta * L
    Tr = p * entrees.theta_Tr * y_pot
    t_cou = entrees.phi * (i_CB - i_ref)
    X0 = -L + D_F + E_Bk  # D_c = D_H + X0 (C42, E^CB = 0, B_H = 0)
    A0 = WB + Div_F + (i_CB * E_Bk + entrees.varpi_L * L + entrees.varpi_D * D_F) / n - gam * E_Bk
    c = i_CB / n - pis  # rendement marginal de la richesse (C43), net de l'érosion visée
    A0p = A0 - t_cou * X0 / n
    cp = c - t_cou / n
    k = entrees.nu_H * n * (1 - entrees.tau_H)
    D1 = 1 - k * cp
    if D1 == 0:
        raise EtatStationnaireInexistant((_violee("D1", D1),))
    D_H = entrees.nu_H * n * ((1 - entrees.tau_H) * A0p + Tr) / D1
    Y_HS = A0p + cp * D_H
    D_c = D_H + X0
    T_cou = t_cou * D_c / n
    T_H = entrees.tau_H * Y_HS + T_cou
    Pi_Bk = (i_CB * E_Bk + entrees.varpi_L * L + entrees.varpi_D * (D_H + D_F)) / n
    Div_Bk = Pi_Bk - gam * E_Bk
    YD = WB + Tr - T_H + i_D * D_H / n + Div_F + Div_Bk
    C = YD - gam * D_H
    # 6. Fermeture (#44, lecture (e)) : équilibre du marché des biens, puis E1.
    # sec:finances_publiques-stationnaire
    G = p * v - C - I
    theta_G = G / (p * y_pot)
    # 7. Dette (bloc 9, C42) : forme fermée linéaire de l'encaisse.
    # sec:finances_publiques-stationnaire, sec:banque_centrale-stationnaire
    a = i_CB / (n * Gam)
    X = G + Tr + i_CB * D_c / n
    D2 = 1 - entrees.nu_G * a
    if D2 == 0:
        anterieures = () if D1 > 0 else (_violee("D1", D1),)
        raise EtatStationnaireInexistant(anterieures + (_violee("D2", D2),))
    M_G = entrees.nu_G * X / (Gam * D2)
    B = D_c + M_G  # E^CB = 0
    PB = G + Tr + i_CB * B / n
    B_CB = entrees.theta_CB * B
    L_CB = max(M_G - B_CB, 0.0)
    Res = max(B_CB - M_G, 0.0)
    B_Bk = B - B_CB
    Pi_CB = i_CB * M_G / n
    interets = i_CB * B / n
    Em = G + Tr + interets - T_H - T_F - Pi_CB + entrees.nu_G * PB - M_G
    # Conditions des formes fermées, écrites en montants (aucune division par un encours qui peut être nul).
    # Existence du dividende de la banque : n_a Π^Bk − n_a γ̄ E^Bk ≥ 0 ; la marge publiée la rapporte à L
    # (« par an », sec:banque-stationnaire), sans objet si L = 0 (lv* = 0, domaine fermé).
    existence_montant = n * Pi_Bk - n * gam * E_Bk
    existence = existence_montant / L if L != 0 else math.nan
    # Plafond de E1 : ν_G PB − Γ̄ G > 0, soit une marge 1 − Γ̄ (G/PB)/ν_G > 0 quand PB > 0.
    marge_E1_montant = entrees.nu_G * PB - Gam * G
    return EtatStationnaire(
        g=f.g, Gr=f.Gr, Pp=f.Pp, Gam=f.Gam, gam=f.gam, pis=f.pis,
        r_neutre=r, i_CB=i_CB, i_ref=i_ref, i_L=i_L, i_D=i_D, rho_L=rho_L, rho_bar_L=rho_bar, d_rho=d_rho,
        p=p, N_pa=N_pa, N=N, pr=pr, y=y, y_pot=y_pot, y_sur_v=y_sur_v, v=v, ve=v, UC=UC, W=W, WB=WB,
        IN_vol=IN_vol, rho_IN=rIN, IN=IN, dIN=dIN, tu=tu, K_vol=K_vol, rho_K=rK, K=K, I_vol=I_vol, I=I,
        ti=ti, PIB=PIB, U=entrees.U_eq, y_cap=K_vol / (n * entrees.kappa),
        L=L, D_F=D_F, V_F=V_F, Pi_av=Pi_av, T_F=T_F, FU=FU, Div_F=Div_F, dL=gam * L,
        D1=D1,
        E_Bk=E_Bk, Tr=Tr, t_cou=t_cou, A0=A0, c=c, k=k, D_H=D_H, V_H=D_H, B_H=0.0, Y_HS=Y_HS, D_c=D_c,
        T_cou=T_cou, T_H=T_H, Pi_Bk=Pi_Bk, Div_Bk=Div_Bk, YD=YD, YD_HS=YD - pis * D_H, C=C,
        G=G, theta_G=theta_G,
        a=a, X=X, D2=D2,
        M_G=M_G, M_G_star=entrees.nu_G * PB, B=B, PB=PB, B_CB=B_CB, B_Bk=B_Bk, L_CB=L_CB, Res=Res, E_CB=0.0,
        Pi_CB=Pi_CB, interets=interets, Em=Em, r_hat=r, pi_e=pi,
        existence_Bk_montant=existence_montant, existence_Bk=existence, marge_E1_montant=marge_E1_montant,
    )


def relever_conditions(etat: EtatStationnaire) -> tuple[ConditionViolee, ...]:
    """Conditions d'existence violées par l'état `etat`, dans l'ordre de `CONDITIONS_D_EXISTENCE`.

    Rend un n-uplet vide si l'état existe. Aucune condition n'est écartée ici (le point de
    référence ν_G = 1 du script, où le plafond de E1 est publié en constat, est traité par le
    script). B_Bk ≥ 0, B_CB ≥ 0 et B_H = 0 sont inatteignables sous θ_CB ∈ [0 ; 1] et B ≥ 0 :
    ils gardent les formes contre une modification ultérieure de l'ordre triangulaire.
    """
    # Inégalité large pour Div_F, comme l'existence du dividende de la banque : Div_F = 0 est
    # encore un état stationnaire, le plancher max(0, ·) de F3 y est atteint sans être
    # contraignant (réponse (b) de `macro`, rang 7 de #84).
    releves = (
        ("D1", etat.D1, not etat.D1 > 0),
        ("D2", etat.D2, not etat.D2 > 0),
        ("existence_dividende_banque", etat.existence_Bk_montant, not etat.existence_Bk_montant >= 0),
        ("Div_F", etat.Div_F, not etat.Div_F >= 0),
        ("theta_G", etat.theta_G, not etat.theta_G > 0),
        ("marge_plafond_E1", etat.marge_E1_montant, not etat.marge_E1_montant > 0),
        ("B", etat.B, not etat.B >= 0),
        ("B_Bk", etat.B_Bk, not etat.B_Bk >= 0),
        ("B_CB", etat.B_CB, not etat.B_CB >= 0),
        ("B_H", etat.B_H, etat.B_H != 0.0),
    )
    return tuple(_violee(identifiant, valeur) for identifiant, valeur, violee in releves if violee)


def ouverture(etat: EtatStationnaire, entrees: EntreesStationnaires) -> Ouverture:
    """État d'ouverture du pas 0 (« État initial résolu » des sections `sec:<bloc>-stationnaire`).

    `mu_tilde_m1` = ln(1 + μ̄), variable d'état du bloc 4 du schéma v2 ; π^e_0 = π*_0 = π*
    (`sec:banque_centrale-stationnaire`) ; E^CB_0 = 0 et B_H = 0.
    """
    n = entrees.pas_par_an
    Gr, Gam = etat.Gr, etat.Gam
    pr_m1 = etat.pr * (1 + entrees.g_pr) ** (-1 / n)
    # P_{t−u} = P_t (1 + π̄)^{−u/n_a}  (sec:prix-stationnaire)
    P = tuple(etat.p * (1 + entrees.pi_etoile) ** (-u / n) for u in range(1, n + 2))
    return Ouverture(
        registre=P,
        pr=etat.pr, N_pa=etat.N_pa, N_m1=etat.N * (1 + entrees.g_N) ** (-1 / n), U_m1=entrees.U_eq,
        W_m1=P[0] * pr_m1 / (1 + entrees.mu_bar), mu_tilde_m1=math.log(1 + entrees.mu_bar),
        ve=etat.ve, IN_vol=etat.IN_vol, IN=etat.IN, K_vol=etat.K_vol, K=etat.K,
        ti=etat.ti, y_m1=etat.y / Gr, T_F_m1=etat.T_F / Gam, rho_bar_L=etat.rho_bar_L,
        L=etat.L, D_F=etat.D_F, YD_m1=etat.YD / Gam, D_H=etat.D_H, B_H=0.0,
        i_L=etat.i_L, i_D=etat.i_D, E_Bk=etat.E_Bk, L_CB=etat.L_CB, Res=etat.Res,
        B_Bk=etat.B_Bk, B_CB=etat.B_CB, M_G=etat.M_G, E_CB=0.0,
        r_hat=etat.r_hat, pi_e=entrees.pi_etoile, pi_cible=entrees.pi_etoile, Y_HS_m1=etat.Y_HS / Gam,
        theta_G=etat.theta_G,
    )
