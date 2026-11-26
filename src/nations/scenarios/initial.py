"""État initial résolu du moteur : adaptateur des tables vers le résolveur (ADR 0015, point 9).

`etat_initial(parametres, normalisation, *, identifiant, graine)` lit les
entrées du résolveur en formes fermées (`nations.scenarios.stationnaire`) sur
les tables du moteur (`ENTREES_DES_TABLES`), y applique en clair les
conventions de sélection de l'état initial (point 10), refuse un état dont une
condition d'existence est violée (`EtatStationnaireInexistant`, point 8.2) et
rend l'`EtatPays` d'ouverture du pas 0 avec l'ensemble des tables **aligné**,
dont la table `finances_publiques` porte θ_G résolu.

**Conventions de sélection** (continuum d'équilibres ; ADR 0015, point 10),
appliquées ici et nulle part ailleurs :
- r̂*_0 = r̄ et π^e_0 = π*_0 = π* (`sec:banque_centrale-stationnaire`) ; π* est
  lu sur la table du bloc 8 (`banque_centrale.pi_etoile` ; décision S4), un
  autre π* passe par `varier` ;
- ϱ̄_L = ϱ_{L,0} (M32, lecture (e) ; `sec:investissement-stationnaire`), par
  `stationnaire.taux` sur les mêmes opérandes (Δϱ = 0,0 exactement) ;
- θ_G résolu ; r̄, τ_H et ν_G donnés (`sec:finances_publiques-stationnaire`,
  première lecture de #44). **θ_G de l'ensemble reçu n'est pas lu** : il est
  l'inconnue de la fermeture (#44, lecture (e) de M32 ; décision S4) ;
- E^CB_0 = 0, B_H = 0, ς_L = ς_B = 0 : hypothèses structurelles du résolveur ;
- normalisations p_0, pr_0, N^pa_0 (`Normalisation`) : l'état est homogène de
  degré un en ces échelles.

**Normalisation** (décision S7) : domaine « float fini > 0 », sans la borne
d'échelle du script (`BORNE_ECHELLE`, borne de l'outil). Une échelle extrême
(ou un paramètre de table extrême) qui rend une grandeur de l'état non finie ou
dénormale, ou les formes non définies (division par une grandeur tombée à
zéro, dépassement de `**` ou de `math.exp`), est refusée par
`EchelleNonRepresentable`, jamais propagée : toute grandeur de l'état
stationnaire résolu (hors `_RAPPORTS_SANS_OBJET`), de l'`EtatPays`, du registre
et θ_G est exactement 0,0 ou un flottant normal fini (|x| ≥
`sys.float_info.min`), contrôlé avant le relevé des conditions d'existence
(condition de `macro` sur S7 et sa précision, écrites avant l'essai).

**Correspondance** : `OUVERTURE_DES_VARIABLES`, table fermée variable d'état
des blocs → champ de l'ouverture du résolveur, en bijection avec
`schema.VARIABLES_DES_BLOCS` (point 9.5) ; positions : postes du catalogue
sous leur nom ; V^flux = V^stock (`identites.valeur_nette_stock`). La graine
traverse la fonction comme champ d'identité : la résolution ne tire aucun aléa.

n_a ≠ 12 n'est pas servi (registre de 13 niveaux, `Cadre` ; #120) : le cadre
des tables le refuse à sa construction. Aucune division par n_a ici (règle
commune du test « conversion unique ») : les formes à n_a quelconque sont dans
le module feuille. La résolution a lieu une fois par scénario, hors
d'`executer_pas`, sans boucle sur un résidu.

Imports (point 9.7) : `nations.etat`, `nations.moteur.parametres`,
`nations.noyau` et le module feuille ; ni `blocs`, ni l'ordonnanceur, ni
`observation`.
"""

from __future__ import annotations

import math
import sys
import types
from dataclasses import dataclass, replace

from nations.etat import schema
from nations.etat.schema import EtatPays
from nations.moteur.parametres import varier
from nations.moteur.parametres.ensemble import EnsembleDesParametres
from nations.noyau import catalogue as cat
from nations.noyau import identites as idt
from nations.scenarios import stationnaire as resolveur

# Champ d'`EntreesStationnaires` → (table de l'ensemble, champ de la table), hors normalisations :
# correspondance déclarée, que lit `entrees_des_tables` champ par champ (test de concordance). Les
# noms sont ceux des tables (ADR 0015, point 7.1) ; θ_G n'y figure pas (inconnue, S4).
ENTREES_DES_TABLES: types.MappingProxyType[str, tuple[str, str]] = types.MappingProxyType({
    "pas_par_an": ("cadre", "pas_par_an"),
    "g_pr": ("production", "g_pr"), "sigma": ("production", "sigma"),
    "kappa": ("production", "kappa"),
    "g_N": ("travail", "g_N"), "U_eq": ("travail", "U_eq"),
    "mu_bar": ("prix", "mu_bar"),
    "nu_H": ("menages", "nu_H"),
    "delta": ("investissement", "delta"), "tu_bar": ("investissement", "tu_bar"),
    "lv_etoile": ("investissement", "lv_etoile"), "nu_F": ("investissement", "nu_F"),
    "zeta": ("investissement", "zeta"), "eta_r": ("investissement", "eta_r"),
    "varpi_L": ("banque", "varpi_L"), "varpi_D": ("banque", "varpi_D"),
    "vartheta": ("banque", "vartheta"),
    "pi_etoile": ("banque_centrale", "pi_etoile"), "r_bar": ("banque_centrale", "r_bar"),
    "theta_CB": ("banque_centrale", "theta_CB"),
    "tau_H": ("finances_publiques", "tau_H"), "tau_F": ("finances_publiques", "tau_F"),
    "theta_Tr": ("finances_publiques", "theta_Tr"), "phi": ("finances_publiques", "phi"),
    "nu_G": ("finances_publiques", "nu_G"),
})

# Variable d'état des blocs → champ de `stationnaire.Ouverture` (valeur à l'ouverture du pas 0).
OUVERTURE_DES_VARIABLES: types.MappingProxyType[str, str] = types.MappingProxyType({
    "v_e": "ve", "IN_vol": "IN_vol", "pr": "pr", "K_vol": "K_vol", "W": "W_m1", "U": "U_m1",
    "N": "N_m1", "N_pa": "N_pa", "mu_tilde": "mu_tilde_m1", "i_L": "i_L", "i_D": "i_D",
    "pi_e": "pi_e", "r_hat_etoile": "r_hat", "pi_etoile": "pi_cible", "YD_m1": "YD_m1",
    "ti": "ti", "y_m1": "y_m1", "T_F_m1": "T_F_m1", "varrho_bar_L": "rho_bar_L",
    "Y_HS_m1": "Y_HS_m1",
})


class NormalisationHorsDomaine(ValueError):
    """Refus d'une normalisation hors de son domaine « float fini > 0 » (décision S7)."""


class EchelleNonRepresentable(ValueError):
    """Refus typé : aux tables et à la normalisation reçues, une grandeur de l'état stationnaire
    ou de l'état initial n'est ni exactement 0,0 ni un flottant normal fini (`inf`, `NaN`,
    nombre dénormal), ou les formes ne sont pas définies en flottants (division par une grandeur
    tombée à zéro, dépassement) ; condition de `macro` sur S7 et sa précision sur les dénormaux.
    La cause peut être la normalisation ou un paramètre de table (par exemple t̄u = 5e−324).
    Champs : `normalisation`, `grandeur` (nom du champ ou de l'opération fautive), `valeur`."""

    def __init__(self, normalisation: Normalisation, grandeur: str, valeur: object) -> None:
        super().__init__(
            f"échelle non représentable : {grandeur} = {valeur!r} aux tables reçues et à la "
            f"normalisation p_0 = {normalisation.p_0!r}, pr_0 = {normalisation.pr_0!r}, "
            f"N_pa_0 = {normalisation.N_pa_0!r} (0,0 ou flottant normal fini attendu ; refusé, "
            "jamais propagé)")
        self.normalisation = normalisation
        self.grandeur = grandeur
        self.valeur = valeur


@dataclass(frozen=True, slots=True)
class Normalisation:
    """Normalisations de l'état initial, champs obligatoires, domaine « float fini > 0 » (S7).

    p_0 : prix, u.m. par u.v. ; pr_0 : productivité, u.v. par personne et par pas ;
    N_pa_0 : population active, personnes. L'état est homogène de degré un en ces échelles.
    """

    p_0: float
    pr_0: float
    N_pa_0: float

    def __post_init__(self) -> None:
        for nom, valeur in (("p_0", self.p_0), ("pr_0", self.pr_0), ("N_pa_0", self.N_pa_0)):
            if not (type(valeur) is float and math.isfinite(valeur) and valeur > 0.0):
                raise NormalisationHorsDomaine(
                    f"Normalisation.{nom} = {valeur!r} : float fini > 0 attendu (S7)")


# Normalisation de référence (p_0, pr_0, N^pa_0) = (1 ; 1 ; 1) (part de `macro`, § 0).
NORMALISATION_DE_REFERENCE = Normalisation(1.0, 1.0, 1.0)


@dataclass(frozen=True, slots=True)
class EtatInitial:
    """État initial résolu : l'`EtatPays` d'ouverture du pas 0 et l'ensemble des tables aligné
    (θ_G résolu dans `finances_publiques`, autres tables celles reçues)."""

    etat: EtatPays
    parametres: EnsembleDesParametres


# Champ de `stationnaire.EtatStationnaire` qui peut être `NaN` dans le domaine : la marge
# d'existence du dividende de la banque rapportée à L, sans objet si L = 0 (lv* = 0) ; le montant
# `existence_Bk_montant` reste contrôlé.
_RAPPORTS_SANS_OBJET = frozenset({"existence_Bk"})


def _refuser_non_representable(normalisation: Normalisation, valeurs) -> None:
    """Lève `EchelleNonRepresentable` sur la première grandeur de `valeurs` (nom, valeur), dans
    l'ordre reçu, qui n'est ni exactement 0,0 ni un flottant normal fini
    (`sys.float_info.min` ≤ |x| < ∞) : `inf`, `NaN` ou nombre dénormal (précision perdue)."""
    for nom, valeur in valeurs:
        if not (valeur == 0.0 or (math.isfinite(valeur) and abs(valeur) >= sys.float_info.min)):
            raise EchelleNonRepresentable(normalisation, nom, valeur)


def entrees_des_tables(parametres: EnsembleDesParametres,
                       normalisation: Normalisation) -> resolveur.EntreesStationnaires:
    """Entrées du résolveur lues sur les tables, champ par champ selon `ENTREES_DES_TABLES`
    (accès nommés, sans accès dynamique ; correspondance tenue par un test), et sur la
    normalisation. Un taux typé (`TauxDeFlux`, `TauxDeCroissance`) passe sa valeur annuelle ;
    les conversions au pas sont dans le résolveur. θ_G de l'ensemble n'est pas lu (S4)."""
    p = parametres
    return resolveur.EntreesStationnaires(
        pas_par_an=p.cadre.pas_par_an,
        g_pr=p.production.g_pr.valeur, sigma=p.production.sigma, kappa=p.production.kappa,
        g_N=p.travail.g_N.valeur, U_eq=p.travail.U_eq,
        mu_bar=p.prix.mu_bar,
        nu_H=p.menages.nu_H,
        delta=p.investissement.delta.valeur, tu_bar=p.investissement.tu_bar,
        lv_etoile=p.investissement.lv_etoile, nu_F=p.investissement.nu_F,
        zeta=p.investissement.zeta, eta_r=p.investissement.eta_r,
        varpi_L=p.banque.varpi_L.valeur, varpi_D=p.banque.varpi_D.valeur,
        vartheta=p.banque.vartheta,
        pi_etoile=p.banque_centrale.pi_etoile.valeur, r_bar=p.banque_centrale.r_bar.valeur,
        theta_CB=p.banque_centrale.theta_CB,
        tau_H=p.finances_publiques.tau_H, tau_F=p.finances_publiques.tau_F,
        theta_Tr=p.finances_publiques.theta_Tr, phi=p.finances_publiques.phi,
        nu_G=p.finances_publiques.nu_G,
        p_0=normalisation.p_0, pr_0=normalisation.pr_0, N_pa_0=normalisation.N_pa_0)


def etat_initial(parametres: EnsembleDesParametres, normalisation: Normalisation, *,
                 identifiant: str, graine: int) -> EtatInitial:
    """État initial résolu du pas 0 et tables alignées (ADR 0015, point 9).

    Refus : `EtatStationnaireInexistant` si une condition d'existence est violée (liste de
    `stationnaire.CONDITIONS_D_EXISTENCE`, toutes relevées), jamais un état ni un écrêtage ;
    `EchelleNonRepresentable` si une grandeur de l'état n'est ni 0,0 ni un flottant normal
    fini aux tables et à la normalisation reçues. θ_G de `parametres` n'est pas lu : le résultat ne dépend pas de sa valeur.
    """
    entrees = entrees_des_tables(parametres, normalisation)
    # Conventions de sélection (point 10) : r̂*_0 = r̄ ; ϱ̄_L = ϱ_{L,0} (Δϱ = 0).
    r_neutre = entrees.r_bar
    try:
        rho_bar_L = resolveur.taux(entrees, r_neutre).rho_L
        etat = resolveur.etat_stationnaire(entrees, r_neutre, rho_bar_L)
        # Représentabilité avant le relevé des conditions : une grandeur non finie ou dénormale
        # est un refus d'échelle, non une condition d'existence violée en `inf`, `NaN` ou en une
        # grandeur tombée sous la plage des flottants normaux (critère de `macro`, S7).
        _refuser_non_representable(normalisation, ((nom, valeur) for nom, valeur in etat._asdict().items()
                                          if nom not in _RAPPORTS_SANS_OBJET))
        conditions = resolveur.relever_conditions(etat)
        if conditions:
            raise resolveur.EtatStationnaireInexistant(conditions)
        o = resolveur.ouverture(etat, entrees)
    except (ZeroDivisionError, OverflowError) as erreur:
        # Une grandeur tombée à zéro ou sortie de la plage des flottants à une échelle extrême.
        raise EchelleNonRepresentable(normalisation, type(erreur).__name__, str(erreur)) from erreur
    ouverture = o._asdict()
    positions = {nom: ouverture[nom] for nom in cat.NOMS_POSTES}
    variables = {v.nom: ouverture[OUVERTURE_DES_VARIABLES[v.nom]]
                 for v in schema.VARIABLES_DES_BLOCS}
    v_flux = {cat.VALEUR_NETTE_FLUX[s]: idt.valeur_nette_stock(positions, s)
              for s in cat.SECTEURS}
    _refuser_non_representable(normalisation, (
        *positions.items(), *v_flux.items(), *variables.items(), ("theta_G", o.theta_G),
        *((f"registre_prix[{u - 1}]", x) for u, x in enumerate(o.registre, start=1))))
    pays = EtatPays(identifiant=identifiant, graine=graine, t=0, registre_prix=o.registre,
                    **positions, **v_flux, **variables)
    alignees = replace(parametres, finances_publiques=varier(parametres.finances_publiques,
                                                            theta_G=o.theta_G))
    return EtatInitial(pays, alignees)
