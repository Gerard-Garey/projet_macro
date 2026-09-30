---
status: accepted
date: 2026-09-29
---

# Outillage : Python 3.12 géré par uv, NumPy et pytest, CI limitée aux actions GitHub, plateforme de référence unique pour les résultats

## Contexte

- Le moteur v2.0 tournait avec Python 3.12, NumPy 2.3.5 et SciPy 1.17.0 (versions de la session K, remesurées le 29/09/2026), sans fichier de verrouillage ni gestionnaire de projet : la reproduction d'une mesure exigeait de retrouver les versions à la main.
- Sur le poste Windows du mainteneur, `python` seul désigne l'alias du Microsoft Store et répond « introuvable » ; Python 3.14 est le défaut d'uv, 3.12 est dans son cache (constaté le 29/09/2026). Les sessions cloud tournent sous Linux. Deux plateformes de développement coexistent donc dès le départ.
- Les références de non-régression (`tests/references/`, à partir du jalon J3) comparent des trajectoires en virgule flottante. Deux plateformes (système, bibliothèque BLAS, nombre de fils) peuvent produire des différences au dernier bit qui, sur 60 ans de simulation, dépassent toute tolérance : il faut **une plateforme de référence unique**, et `CLAUDE.md`, « Changements de résultats », renvoie ici pour la désigner.
- Le dépôt est public ; ses réglages de sécurité (README, « Sécurité du dépôt ») limitent déjà les actions GitHub à celles publiées par GitHub, épinglées par SHA, avec jeton en lecture seule.
- La compilation de la spécification en XeLaTeX (ADR 0004) exige TeX Live avec `texlive-xetex` en CI et en session cloud, MiKTeX sur le poste local.

## Décision

Arrêtée par le mainteneur le 29/09/2026 : points 1 à 3 par M11, M14, `docs/exigences.md` § 4.2 et les réglages du dépôt ; point 4 par la décision **M16** de `docs/feuille-de-route.md`.

1. **Python 3.12, géré par uv.** `pyproject.toml` déclare le projet et ses dépendances ; `uv.lock` verrouille toutes les versions et est versionné. Toute exécution passe par `uv run` (batteries, scripts d'`outils/`, programme), jamais par `python` seul. Dépendances du moteur : NumPy ; tests : pytest. SciPy n'est pas une dépendance du moteur tant qu'une fiche comparative n'en établit pas le besoin (l'invariant 11 de l'ADR 0002 exclut les résolutions itératives à chaque pas).
2. **Batteries de vérification** (identiques dans `CLAUDE.md`, « Commandes », et dans `BATTERIES` du workflow `circuit-technique`) : `uv run pytest -q tests/unitaires`, `uv run pytest -q tests/invariants`, `uv run python outils/concordance_spec_moteur.py --strict`. La compilation XeLaTeX s'y ajoute en CI. Tout contrôle mécanique est un script, jamais un agent.
3. **CI limitée aux actions publiées par GitHub**, épinglées par SHA, jeton en lecture seule ; les outils système (TeX Live, uv) s'installent par des commandes, pas par des actions tierces. Les jobs de tests, de concordance et de compilation deviennent des contrôles requis du ruleset de `main` (issue #4).
4. **Plateforme de référence des résultats (M16)** : la CI Linux de GitHub Actions, exécuteur `ubuntu-latest` (x86-64), Python 3.12 installé par uv, versions verrouillées par `uv.lock`. `architect` y ajoute, en application : un seul fil BLAS (`OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`) pour que le résultat ne dépende pas du nombre de cœurs de l'exécuteur, et :
   - les références de `tests/references/` sont régénérées sur cette plateforme (par la session principale, après visa, `outils/regenerer_references.py`) ; une génération locale sert à préparer le tableau avant / après, pas à produire la référence ;
   - les tests de non-régression comparent avec une tolérance relative déclarée, et le test de budget (1 ms par pays-semaine) s'exécute sur cette plateforme, avec une marge pour la variabilité de l'exécuteur, mesurée avant d'être fixée ;
   - un écart entre poste local et plateforme de référence est un fait à consigner (issue), pas une raison de régénérer la référence ;
   - `ubuntu-latest` suit l'image courante de GitHub : chaque rapport de référence consigne la version d'image effectivement utilisée (variable `ImageOS` / `ImageVersion` de l'exécuteur), et un changement d'image qui modifie un résultat se traite comme tout changement de résultat (tableau avant / après, visa).

## Options écartées

- **`pip` et `requirements.txt`, ou `conda`.** Écarté : pas de verrouillage transitif natif pour le premier, environnement lourd et lent à installer en CI pour le second ; uv fournit le verrouillage, l'installation de Python et l'exécution en une commande.
- **Python 3.14 (défaut du poste).** Écarté : les dépendances numériques y sont moins éprouvées, et 3.12 est la version des mesures de la première tentative, ce qui permet de reproduire ses chiffres depuis `archive/` sans changer d'interpréteur.
- **Poste Windows du mainteneur comme plateforme de référence.** Écarté (M16) : non reproductible depuis une session cloud, alias Microsoft Store, BLAS différent ; la régénération dépendrait d'une seule machine.
- **Image Ubuntu épinglée** (`ubuntu-24.04`, comme dans le `ci.yml` du modèle d'organisation) plutôt que `ubuntu-latest`. Écartée par le mainteneur (M16) au profit de l'image courante de GitHub : pas de version à maintenir à la main ni d'image dépréciée à rattraper. Le risque d'un changement d'image silencieux est couvert par la consigne ci-dessus (version d'image consignée dans chaque rapport de référence).
- **Actions tierces** (installation de TeX Live, d'uv, mise en cache) : écartées par les réglages de sécurité du dépôt public ; on installe par `apt` et par le script officiel d'uv, commandes visibles dans le workflow.
- **Tolérance nulle (égalité bit à bit) entre plateformes.** Écarté : elle n'est garantie que sur la plateforme de référence elle-même ; entre plateformes, la comparaison est relative et déclarée.

## Conséquences

- **Fichiers** (issue #4) : `pyproject.toml`, `uv.lock`, `.python-version` (`3.12`), `.github/workflows/ci.yml` (jobs « Tests », « Concordance spécification-moteur », « Compilation de la spécification », à côté de « Contrôles du dépôt » ; `À ADAPTER` retirés), `.github/ruleset-main.json` (les trois nouveaux jobs ajoutés aux contrôles requis), `README.md` réécrit (commandes, environnement), `outils/concordance_spec_moteur.py`, `outils/compiler_specification.sh`, `tests/unitaires/`, `tests/invariants/`, hook `.claude/hooks/preparer_latex.sh`. `outils/regenerer_references.py` et `tests/references/` arrivent au jalon J3 avec les premières références.
- **Mise en œuvre de la plateforme de référence dans `ci.yml`** (relevée le 29/09/2026 sur l'arbre de travail de l'issue #4 ; elle applique la décision, elle ne la change pas) :
  - tous les jobs tournent sur `runs-on: ubuntu-latest`, sans épinglage d'image (M16) ;
  - `UV_MANAGED_PYTHON: "1"` (variable d'environnement du workflow) impose à uv un Python **géré par uv**, à la version de `.python-version`, jamais celui de l'image : la plateforme de référence ne dépend pas du Python préinstallé sur l'exécuteur ;
  - uv est installé par le **script officiel épinglé** (`curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh`, `UV_VERSION` en variable du workflow), pas par une action tierce (point 3) ; l'environnement est créé par `uv sync --locked` et chaque commande passe par `uv run --locked` ;
  - le job « Tests » fixe `OPENBLAS_NUM_THREADS=1` et `OMP_NUM_THREADS=1` (point 4) ;
  - l'étape « Image de l'exécuteur et environnement » du job « Tests » consigne `ImageOS`, `ImageVersion`, la version de Python (`uv run --locked python -VV`) et la liste des paquets (`uv pip list`) : c'est là que se lit la version d'image effectivement utilisée, exigée par le point 4 pour chaque rapport de référence.
  - Les contrôles requis du ruleset (« Tests », « Concordance spécification-moteur », « Compilation de la spécification ») sont appliqués par le mainteneur (`gh api -X PUT … --input .github/ruleset-main.json`, README, « Sécurité du dépôt ») **après la fusion de la PR #7 et un premier passage vert de la CI sur `main`**, pour ne pas exiger un contexte qui n'a jamais été rapporté.
- **Effet sur les résultats** : aucun à ce jour. À partir de J3, tout résultat de référence porte la plateforme, le commit et la graine qui l'ont produit.
- **Ce que l'ADR ne règle pas** : la tolérance numérique des tests de non-régression (fixée avec les premières références, avant l'essai) ; la marge du test de budget en CI ; la version du serveur web (J7).

Issues : #3, #4.
