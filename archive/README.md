# archive/ — pièces de la première tentative

Dossier **temporaire**, constitué par l'issue #5 le 29/09/2026 selon la décision M6 du mainteneur (`docs/feuille-de-route.md`, ADR 0001). Il contient le strict nécessaire aux fiches comparatives (`docs/blocs/`) et aux premiers essais du moteur v3. Il sera **supprimé au plus tard à la fin du jalon J6**.

## Règles

- **Lecture seule** : aucune pièce n'est modifiée après son versement (`CLAUDE.md`, invariant 4 ; `ZONES_PROTEGEES` du workflow `circuit-technique`).
- **Jamais importée** : aucun module de `src/`, `tests/` ou `outils/` n'importe `archive/`.
- **Source historique, pas référence** : la spécification v3 fait foi pour le moteur. Une équation reprise d'ici passe par une fiche comparative et une décision du mainteneur (M-n).

## Contenu

| Pièce | Origine | Taille (octets) | SHA-256 |
|---|---|---|---|
| `v1.5/Nations_et_Marches_v1_5.tex` | Spécification v1.5 (XeLaTeX, 2 696 lignes, 104 p. compilées) | 414 855 | `097d023fa9d0bde837df9e854604de93dc1fedf45dcd95ec98d1613bded240ec` |
| `v2.0/prototype/*.py` (27 fichiers) | Moteur v2.0, répertoire `W10_P1/prototype/` de l'archive d'exécution de la session K du 19/09/2026 (`NATIONS_MARCHES_EXECUTION_K_20260919.zip`, SHA-256 `9e67aa768c149de3a906a7e752121075086ca75e711e20c603f832b0845e5bd4`), copié sans modification | 292 661 au total | voir ci-dessous |
| `cours/Cours_Nations_et_Marches_Vol1.pdf` | Cours, chapitres 1 à 7 (compilé le 04/09/2026, antérieur à la v1.4) | 185 039 | `4577fa9c4598183eb803d044e577635475e5862c507b995108e00c45e756c910` |
| `cours/Cours_Nations_et_Marches_Vol2.pdf` | Cours, chapitres 8 à 12 (même date) | 165 623 | `b8f27cf0a3d2ff5aeed74f25a5ceea9b9a4e3a3972bcbd6e2cae0c713462697c` |
| `faits_mesures_G_K.md` | Synthèse, rédigée le 29/09/2026, des faits mesurés en sessions G à K sur le moteur v2.0 | — | — |

Empreinte du code v2.0 : `sha256sum *.py | sha256sum` dans `v2.0/prototype/` donne `64f4757767544b4b544d2d09b9ac94a1656692c6ad5411b2527f5e19614c8fee`.

## Pièces absentes

- **État de référence `D1_prepare150.json`** (72 Mo, t = 20 280, obtenu après 150 ans de préparation) : exclu par décision M6. Le code v2.0 ne peut donc pas être relancé depuis la référence des sessions G à K.
- **`config/reference.json`** : `v2.0/prototype/reference.py` le lit, mais il ne figure pas dans l'archive K ; `simulate.py` et `World.homogeneous()` ne fonctionnent pas en l'état.
- **Suites de tests du moteur v2.0** (`tests.py`, `tests3.py` à `tests5.py`, `test_zero.py`, `w10_checks.py`, `audit3.py`, `run_suites.py`) : absentes de l'archive K.
- **Prototype et document v1.7** : non retrouvés ; le mainteneur a décidé de s'en passer (M10).
- **Plan du cours v1.5 et relevé d'erreurs de la v1.5** : non retrouvés.

## Exclusions (dépôt public)

Ne sont pas versés : la correspondance entre configurations et pays réels, les liens de partage, les notes de supervision, les archives compressées, les rapports bruts des sessions et l'état D1.

Le source v1.5 et le cours citent des épisodes historiques (crises, hyperinflations) et des références bibliographiques qui nomment des pays ; la grille des dix configurations de la v1.5 (§ 11, « archétypes de jeu anonymisés, pas des pays ») n'en nomme aucun. Contrôle du 29/09/2026 : aucune occurrence de `drive.google` ni de `docs.google` dans `archive/`.
