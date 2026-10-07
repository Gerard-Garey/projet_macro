"""Les quatre paramètres du cadre : n_a, n_m, ε, ε_V.

Contrat : ADR 0012, F1 ; ADR 0005, point 18 (quatre paramètres typés, sans
drapeau de mode) ; fiche « temps et comptabilité », § 9.2 et § 9.9 ;
spécification, `sec:cadre-calendrier`, `sec:cadre-identites` et
`tab:calibration`. Valeurs fixées par la décision M22 : aucune ne varie par
archétype.

`CADRE` porte les quatre valeurs sous leur nom : c'est l'objet que le moteur
passe au noyau (`ouvrir_pas`, protocole `ParametresCadre` : les deux
tolérances en `float`) et aux blocs (vue). Il est engendré des déclarations,
qui restent la seule source.
"""

from __future__ import annotations

from dataclasses import dataclass

from nations.moteur.parametres import (
    ENTIER_STRICTEMENT_POSITIF,
    FLOTTANT_STRICTEMENT_POSITIF,
    Domaine,
    Parametre,
)

# n_m = 1 : un pas est un tour (M22, pt 1). Le calendrier écrit t = n − 1
# (`sec:cadre-calendrier`), forme qui n'est exacte que sous n_m = 1 : le
# domaine le déclare plutôt que de laisser une autre valeur fausser la date.
UN_PAS_PAR_TOUR = Domaine("entier égal à 1 (un pas est un tour, M22)",
                          lambda x: type(x) is int and x == 1)

PAS_PAR_AN = Parametre(
    "pas_par_an", "n_a", 12, "pas par an",
    "décision M22, pt 1 (ADR 0005, points 1 et 18)",
    ("eq:moteur-calendrier-date", "eq:moteur-conversion-taux",
     "eq:moteur-conversion-croissance", "eq:moteur-registre-prix", "eq:moteur-glissement"),
    ENTIER_STRICTEMENT_POSITIF)

PAS_PAR_TOUR = Parametre(
    "pas_par_tour", "n_m", 1, "pas par tour",
    "décision M22, pt 1 (ADR 0005, points 1, 2 et 18)",
    ("eq:moteur-date-decision",),
    UN_PAS_PAR_TOUR)

TOLERANCE_IDENTITE_PAS = Parametre(
    "tolerance_identite_pas", "ε", 1e-12, "sans dimension",
    "décision M22, pt 14, Q4 (a) (ADR 0005, points 14 et 18)",
    ("eq:noyau-tolerance-pas",),
    FLOTTANT_STRICTEMENT_POSITIF)

TOLERANCE_IDENTITE_CUMULEE = Parametre(
    "tolerance_identite_cumulee", "ε_V", 1e-12, "sans dimension",
    "décision M22, pt 14, Q4 (b) (ADR 0005, points 14 et 18)",
    ("eq:noyau-tolerance-cumulee",),
    FLOTTANT_STRICTEMENT_POSITIF)

PARAMETRES_DU_CADRE = (PAS_PAR_AN, PAS_PAR_TOUR, TOLERANCE_IDENTITE_PAS,
                       TOLERANCE_IDENTITE_CUMULEE)


@dataclass(frozen=True, slots=True)
class Cadre:
    """Les quatre paramètres du cadre, sous leur nom, en `int` et `float`."""

    pas_par_an: int
    pas_par_tour: int
    tolerance_identite_pas: float
    tolerance_identite_cumulee: float


CADRE = Cadre(**{p.nom: p.valeur for p in PARAMETRES_DU_CADRE})
