# Nations & Marchés

Simulateur macroéconomique multi-pays à **cohérence stock-flux**, destiné à devenir un jeu multijoueur tour par tour mensuel : chaque joueur incarne un État (politique monétaire, finances publiques, cadre institutionnel) face à un secteur privé autonome qui réagit aux prix et aux décisions publiques. Le modèle n'est pas un outil de prévision : il vise des trajectoires qualitativement justes et explicables.

Le projet reprend sur un **moteur neuf, dit « v3 »**, une première tentative (spécification v1.5, moteur v2.0), dont l'échec est analysé dans l'ADR 0001. Ce qui prime : la concordance exacte entre spécification et moteur, la reproductibilité, la lisibilité des mécanismes pour le joueur.

Travail en cours : jalons et périmètre de la branche courante dans `docs/feuille-de-route.md`.

## Arborescence

| Chemin | Rôle |
|---|---|
| `src/nations/` | Moteur v3, en couches (ADR 0002) : `noyau` (comptes, seul lieu d'exécution des flux monétaires), `blocs` (un module par bloc de la spécification), `moteur` (ordonnanceur et paramètres typés), `etat` (schéma d'état, sauvegarde et reprise), `observation` (séries, sans effet sur la trajectoire), `scenarios` (état initial résolu, archétypes), `leviers` (commandes du joueur) |
| `tests/unitaires/`, `tests/invariants/` | Batteries de vérification (propriétés, invariants d'architecture, budget de calcul) |
| `outils/` | Scripts de contrôle : concordance spécification ↔ moteur, compilation de la spécification |
| `docs/specification/` | Spécification LaTeX (`nations_et_marches.tex`, PDF versionné) et ses conventions (`CONVENTIONS.md`) |
| `docs/blocs/` | Inventaire des blocs et fiches comparatives (origine de chaque approche) |
| `docs/adr/` | Décisions d'architecture et d'organisation |
| `docs/exigences.md`, `docs/feuille-de-route.md` | Cahier des charges ; jalons et décisions du mainteneur |
| `CONTEXT.md` | Glossaire du domaine et de l'organisation |
| `archive/` | Pièces de la première tentative, en lecture seule, jamais importées (dossier temporaire) |
| `CLAUDE.md`, `.claude/` | Règles de travail, sous-agents, workflows, hooks et skills de Claude Code |
| `.github/` | CI, modèles d'issue et de PR, ruleset de `main`, Dependabot |

## Commandes

Python 3.12, géré par [uv](https://docs.astral.sh/uv/) (ADR 0003) : toute exécution passe par `uv run`, jamais par `python` seul (sur le poste Windows, `python` désigne l'alias du Microsoft Store).

Installer l'environnement verrouillé (Python 3.12, NumPy, pytest, selon `uv.lock`) :

```bash
uv sync --locked
```

Batteries de vérification (identiques dans `CLAUDE.md`, « Commandes », et dans le workflow `circuit-technique`) :

```bash
uv run pytest -q tests/unitaires
uv run pytest -q tests/invariants
uv run python outils/concordance_spec_moteur.py --strict
```

Un succès inattendu d'un test marqué en échec attendu fait échouer la batterie (`xfail_strict`). La concordance applique le contrat de `docs/specification/CONVENTIONS.md` § 9 ; sans `--strict`, elle rend compte sans échouer.

Vérification des matrices des bilans et des flux de la spécification (tables `tab:matrice-bilans`, `tab:matrice-flux` et `tab:portes-monnaie` de la section du cadre, lues terme à terme ; contrat de `docs/specification/CONVENTIONS.md` § 9, « Script des matrices » ; défaut : la spécification) :

```bash
uv run python outils/verifier_matrices.py [--strict] [fichier.tex]
```

Sans `--strict`, elle rend compte sans échouer, sauf si le fichier est absent, illisible ou non UTF-8 (code 1 dans les deux modes) ; la batterie `tests/unitaires` la lance en `--strict` sur la spécification.

Compilation de la spécification (XeLaTeX ; MiKTeX sur le poste local, TeX Live en session cloud et en CI) :

```bash
bash .claude/hooks/preparer_latex.sh              # xelatex au PATH (ajouter --installer en session cloud)
bash outils/compiler_specification.sh             # passes XeLaTeX et contrôle du journal
```

Le PDF est versionné et commité avec le `.tex` ; la procédure complète est la skill `compiler-doc` (`.claude/skills/compiler-doc/SKILL.md`).

La CI (`.github/workflows/ci.yml`) exécute à chaque PR et à chaque push sur `main` : contrôles du dépôt, tests, concordance stricte, compilation de la spécification, sur `ubuntu-latest`, plateforme de référence des résultats (ADR 0003).

## Façon de travailler

Le projet est mené avec Claude Code : sous-agents spécialisés (pilotage, experts de fond `macro`, `monnaie` et `jeu`, réalisation, vérification), circuits de travail, règles Git et GitHub, traçabilité des changements de résultats. Tout est dans `CLAUDE.md`. En bref :

- **une branche de travail à la fois**, au périmètre fermé d'issues, PR brouillon dès sa création ; fusion par le mainteneur, par commit de fusion, CI verte ;
- **ceux qui écrivent ne vérifient pas, ceux qui vérifient n'écrivent pas** ;
- **toute affirmation sur le code s'adosse à une mesure** exécutée ; tout changement de résultat a son tableau avant / après et son visa ;
- l'origine de chaque bloc (v1.5, v2.0 ou nouvelle) est **décidée par le mainteneur** sur fiche comparative.

## Routage du modèle et de l'effort

`architect`, `macro`, `monnaie` et `jeu` tournent sur Opus par défaut : effort `medium` pour la routine et `high` pour le jugement, Fable réservé à une liste fermée de cas ou à l'accord du mainteneur, avec des plafonds d'escalade (`docs/agents/routage.md`, ADR 0006). Politique issue du modèle `Modele_vibe_code`, adaptée à ce projet ; ses critères se réévaluent à mesure que le projet évolue (après les dix premières consultations, puis à chaque point d'étape d'`architect`).

- **Où** : critères (matrice, contrats partagés, seuil « macro », plafonds) dans `docs/agents/routage.md` ; effort et plafond de tours de routine dans le frontmatter des fiches de base ; rôles dédoublés, effort et plafond de jugement dans `.claude/outils/fiches_jumelles.sh` (`ROLES`, `EFFORT_APPROFONDI`, `TOURS_APPROFONDI`), puis `bash .claude/outils/fiches_jumelles.sh` pour régénérer les fiches `-approfondi`.
- **Articulation** : les règles de `CLAUDE.md` priment (visa, décisions réservées au mainteneur, deux lectures d'une source).
- **Vérification** : `bash .claude/outils/fiches_jumelles.sh --verifier` (la CI) ; dans une session neuve, une consultation de chaque fiche puis `bash .claude/outils/bilan_journal.sh` (modèle réellement servi, journal local des sous-agents terminés, hook `SubagentStop`) ; les escalades, relances ciblées et arrêts sont notés dans la PR (section « Escalades, relances et arrêts »).
- **Limites** : un plafond de tours n'est pas un plafond de tokens ; l'effort effectif n'est pas observable dans le journal ; la politique ne supprime pas les angles morts des modèles.

## Sécurité du dépôt

Le dépôt est public. Réglages appliqués (`OWNER/REPO` : `Gerard-Garey/projet_macro`) :

- fusion par **commit de fusion seulement** (squash et rebase désactivés), wiki désactivé ;
- **secret scanning** et **push protection** activés ; **alertes et correctifs de sécurité Dependabot** activés ;
- Actions limitées à celles de GitHub (`github_owned_allowed`), jeton des workflows en lecture seule, actions épinglées par SHA ; uv et TeX Live s'installent par des commandes visibles dans le workflow, jamais par une action tierce (ADR 0003) ;
- ruleset **« Protection main »** : suppression et force-push interdits, PR obligatoire (fusion par commit de fusion, fils de discussion résolus), contrôles requis à jour avec `main`, sans contournement : « Contrôles du dépôt », « Tests », « Concordance spécification-moteur », « Compilation de la spécification ».

```bash
R=Gerard-Garey/projet_macro
gh api -X PATCH repos/$R -F allow_squash_merge=false -F allow_rebase_merge=false -F allow_merge_commit=true -F has_wiki=false \
  -f 'security_and_analysis[secret_scanning][status]=enabled' -f 'security_and_analysis[secret_scanning_push_protection][status]=enabled'
gh api -X PUT repos/$R/vulnerability-alerts
gh api -X PUT repos/$R/automated-security-fixes
gh api -X PUT repos/$R/actions/permissions -F enabled=true -f allowed_actions=selected
gh api -X PUT repos/$R/actions/permissions/selected-actions -F github_owned_allowed=true -F verified_allowed=false
gh api -X PUT repos/$R/actions/permissions/workflow -f default_workflow_permissions=read -F can_approve_pull_request_reviews=false
gh api -X POST repos/$R/rulesets --input .github/ruleset-main.json
```

Le ruleset est dans `.github/ruleset-main.json`. S'il existe déjà, le mettre à jour plutôt que d'en créer un second :

```bash
ID=$(gh api repos/$R/rulesets --jq '.[] | select(.name == "Protection main") | .id')
gh api -X PUT repos/$R/rulesets/$ID --input .github/ruleset-main.json
```

Un contrôle requis n'est satisfait que par un job de ce nom exact dans `.github/workflows/ci.yml` : renommer un job impose de mettre à jour le ruleset dans la même PR.

Libellés d'issues (tri de `docs/agents/triage-labels.md`, plus `bug`, `enhancement`, `documentation`) : `bash .github/creer_labels.sh Gerard-Garey/projet_macro`.
