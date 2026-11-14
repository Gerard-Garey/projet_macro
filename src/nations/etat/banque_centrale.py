"""Variables d'état du bloc 8, banque centrale et anticipations (radical
`banque_centrale`) : l'anticipation d'inflation π^e (schéma v2), puis la cible
en vigueur π* (schéma v3).

Contrat : ADR 0012, G1 (a), et annotation du 13/11/2026, points 1.2 et 1.6
(P53 ; avis de `monnaie`, synthèse du rang 1a, § 9). π^e est écrite en
phase 1 (BC3) ; à l'ouverture du pas t, `pi_e` vaut π^e_t, lue par `travail`
en phase 1 (T3), qui ne prend jamais π* ni Γ^e à sa place. Valeur
stationnaire : π̄ = π* (`sec:banque_centrale-anticipation`).

π* (schéma v3 ; ADR 0013, annotation du 14/11/2026, points 3 et 4 ; P96 ; #61)
est la **cible en vigueur**, écrite en phase 1 (BC4, π*_{t+1} = π*_t à levier
fermé) ; à l'ouverture du pas t, `pi_etoile` vaut π*_t, lue par la phase 0
(Γ^e et π^{∗,pas}, `nations.moteur.ouverture`) et par les blocs (ADR 0010).
Valeur initiale : le paramètre `pi_etoile` de la table du bloc 8 (BC4 ; état
résolu). r̂* s'ajoute, avant elle, avec le bloc 8 (#91, rang 4 de J3-c).

Domaine au chargement (point 1.6) : 1 + π^e > 0, domaine du type « par an,
taux de croissance » (condition de `TauxDeCroissance` et de ln(1 + π^e) dans
T3), refusé par `schema.defaut_de_domaine` sous la forme « <valeur> hors du
domaine 1 + π^e > 0 (…) », qui refuse aussi `NaN`, sans écrêtage. Au fil des
pas, π^e > −1 est un invariant de BC3, éprouvé par les tests du bloc 8 (J3-c),
non par le moteur.

Domaine de π* au chargement et à l'écriture (point 4) : 1 + π* > 0, domaine du
type (facteur de Fisher de BC1 et f(π*) de Γ^e), même forme de refus.
"""

from __future__ import annotations

from nations.etat.variables import Invariance, scalaire

RADICAL = "banque_centrale"

VARIABLES = (
    scalaire("pi_e", RADICAL, "1", "par an, taux de croissance",
             "π^e_t = π̄ = π* (sec:banque_centrale-anticipation)", Invariance.SANS_DIMENSION),
    scalaire("pi_etoile", RADICAL, "1", "par an, taux de croissance",
             "π*_t = π* déclarée (BC4 ; ADR 0010)", Invariance.SANS_DIMENSION),
)

# Domaines au chargement : nom → (condition en clair, prédicat de la condition).
DOMAINES = {
    "pi_e": ("1 + π^e > 0 (domaine du taux de croissance ; ln(1 + π^e) dans T3)",
             lambda x: 1.0 + x > 0.0),
    "pi_etoile": ("1 + π* > 0 (domaine du taux de croissance ; facteur de Fisher de BC1 et "
                  "f(π*) de Γ^e)", lambda x: 1.0 + x > 0.0),
}
