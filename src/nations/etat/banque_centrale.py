"""Variable d'état du bloc 8, banque centrale et anticipations (radical
`banque_centrale`), schéma v2 : l'anticipation d'inflation π^e seule.

Contrat : ADR 0012, G1 (a), et annotation du 13/11/2026, points 1.2 et 1.6
(P53 ; avis de `monnaie`, synthèse du rang 1a, § 9). π^e est écrite en
phase 1 (BC3) ; à l'ouverture du pas t, `pi_e` vaut π^e_t, lue par `travail`
en phase 1 (T3), qui ne prend jamais π* ni Γ^e à sa place. Valeur
stationnaire : π̄ = π* (`sec:banque_centrale-anticipation`). Les autres
variables du bloc 8 s'ajoutent au J3-c.

Domaine au chargement (point 1.6) : 1 + π^e > 0, domaine du type « par an,
taux de croissance » (condition de `TauxDeCroissance` et de ln(1 + π^e) dans
T3), refusé par `schema.defaut_de_domaine` sous la forme « <valeur> hors du
domaine 1 + π^e > 0 (…) », qui refuse aussi `NaN`, sans écrêtage. Au fil des
pas, π^e > −1 est un invariant de BC3, éprouvé par les tests du bloc 8 (J3-c),
non par le moteur.
"""

from __future__ import annotations

from nations.etat.variables import Invariance, scalaire

RADICAL = "banque_centrale"

VARIABLES = (
    scalaire("pi_e", RADICAL, "1", "par an, taux de croissance",
             "π^e_t = π̄ = π* (sec:banque_centrale-anticipation)", Invariance.SANS_DIMENSION),
)

# Domaines au chargement : nom → (condition en clair, prédicat de la condition).
DOMAINES = {
    "pi_e": ("1 + π^e > 0 (domaine du taux de croissance ; ln(1 + π^e) dans T3)",
             lambda x: 1.0 + x > 0.0),
}
