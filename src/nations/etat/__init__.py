"""Schéma d'état typé et versionné.

L'état contient ce qui est nécessaire pour dérouler le pas suivant, et rien
d'autre : **aucun historique dans l'état** (les séries relèvent de
`nations.observation`). La sauvegarde et la reprise sont exactes : reprendre
une sauvegarde reproduit la trajectoire à l'identique, graines comprises (une
graine explicite par pays).

Modules (ADR 0012, Conséquences) :
- `schema` : déclarations `VariableEtat`, `EtatPays` engendré, `VERSION_SCHEMA` ;
- `sauvegarde` : `sauvegarder` et `charger` (JSON, `repr` des flottants).

`etat` n'importe de `nations` que `noyau` (noms des postes).
"""
