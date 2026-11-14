"""Schéma d'état typé et versionné.

L'état contient ce qui est nécessaire pour dérouler le pas suivant, et rien
d'autre : **aucun historique dans l'état** (les séries relèvent de
`nations.observation`). La sauvegarde et la reprise sont exactes : reprendre
une sauvegarde reproduit la trajectoire à l'identique, graines comprises (une
graine explicite par pays).

Modules (ADR 0012, Conséquences) :
- `unites` : `UNITES`, vocabulaire fermé des unités, unique pour les
  variables d'état et les paramètres du moteur ; n'importe rien de `nations` ;
- `variables` : `VariableEtat` et `Invariance`, module feuille (C1) ;
- `production`, `travail`, `prix`, `banque_centrale` : déclarations et
  domaines des variables d'état de chaque bloc, un module par radical
  (G1 (a) ; annotation du 13/11/2026, point 1) ;
- `schema` : `VARIABLES` assemblées, `EtatPays` engendré, `VERSION_SCHEMA`,
  domaines et bornes des champs (`defaut_de_domaine`) ;
- `sauvegarde` : `sauvegarder` et `charger` (JSON, `repr` des flottants).

`etat` n'importe de `nations` que `noyau` (noms des postes), et `unites`
rien du tout.
"""
