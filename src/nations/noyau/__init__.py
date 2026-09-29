"""Noyau comptable : bilans, flux et grand livre.

C'est le **seul endroit où un flux monétaire s'exécute**. Les blocs proposent
des flux ; le noyau les inscrit, puis vérifie après chaque phase les identités
stock-flux avec une tolérance **relative à l'échelle du bilan**, jamais une
constante absolue. Toute agrégation entre pays suit l'ordre canonique des
identifiants de pays.

Radical des labels d'équation des identités comptables : `noyau`
(`eq:noyau-<nom>`).
"""
