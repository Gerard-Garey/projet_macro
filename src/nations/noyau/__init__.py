"""Noyau comptable : bilans, flux et grand livre.

C'est le **seul endroit où un flux monétaire s'exécute**. Les blocs proposent
des flux ; le noyau les inscrit, puis vérifie après chaque phase les identités
stock-flux avec une tolérance **relative à l'échelle du bilan**, jamais une
constante absolue. Toute agrégation entre pays suit l'ordre canonique des
identifiants de pays.

Modules (ADR 0012, Conséquences) :
- `catalogue` : postes, 28 lignes de la matrice des flux par termes, arbre des
  comptes, signatures dérivées, phases et proposants ;
- `grand_livre` : `ouvrir_pas`, `proposer`, `declarer_montant_couvert`,
  `clore_phase`, `clore_pas` et les lectures seules ;
- `identites` : identités, échelle S, tolérances, contrôle de signe unique ;
- `diagnostics` : exceptions typées d'arrêt.

Le noyau n'importe rien d'autre de `nations`.

Radical des labels d'équation des identités comptables : `noyau`
(`eq:noyau-<nom>`).
"""
