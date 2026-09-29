"""Schéma d'état typé et versionné.

L'état contient ce qui est nécessaire pour dérouler le pas suivant, et rien
d'autre : **aucun historique dans l'état** (les séries relèvent de
`nations.observation`). La sauvegarde et la reprise sont exactes : reprendre
une sauvegarde reproduit la trajectoire à l'identique, graines comprises (une
graine explicite par pays).
"""
