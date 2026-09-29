# projet_macro — modèle d'organisation Claude Code

Modèle de dépôt pour mener un projet avec Claude Code : sous-agents spécialisés, circuits de travail, règles Git et GitHub, traçabilité des changements de résultats. Il ne contient aucun code métier ; chaque projet part de ce modèle et remplit les passages marqués **À ADAPTER**.

Travail en cours.

## Contenu

| Chemin | Rôle |
|---|---|
| `CLAUDE.md` | Règles lues par Claude Code à chaque session : Git et GitHub, architecture, changements de résultats, rigueur, sous-agents, circuits, workflows |
| `.claude/agents/` | Six sous-agents : `architect` (pilotage), `expert` (fond, à spécialiser), `coder`, `docwriter` (réalisation), `audit`, `app-review` (vérification) |
| `.claude/workflows/circuit-technique.js` | Circuit `coder` → batteries → `audit` léger, une reprise au plus, sans commit ni push |
| `.claude/settings.json`, `.claude/hooks/` | Permissions, hook d'installation des plugins (skills `mattpocock-skills`, `document-skills`) |
| `CONTEXT.md` | Glossaire du domaine et de l'organisation |
| `docs/exigences.md` | Gabarit du cahier des charges |
| `docs/feuille-de-route.md` | Gabarit de la feuille de route tenue par `architect` |
| `docs/adr/` | Décisions consignées (gabarit `0000-gabarit.md`) |
| `docs/agents/` | Suivi des issues (GitHub, `gh` ou MCP), libellés de tri, documentation du domaine |
| `.github/` | Modèles d'issue et de PR, CI minimale, Dependabot |

## Démarrer un projet à partir du modèle

1. Créer le dépôt avec « Use this template » (ou copier les fichiers), puis appliquer « Sécurité du dépôt » ci-dessous : les réglages et le ruleset ne sont pas copiés par le modèle.
2. Remplir chaque passage **À ADAPTER** : `grep -rn "À ADAPTER\|A ADAPTER" .`
   - `CLAUDE.md` : contexte, dépôt de référence, batteries de vérification, domaines de commit, architecture, exigences de rigueur ;
   - `.claude/agents/expert.md` : spécialité et sources qui font foi (dupliquer la fiche si le projet a besoin de deux experts, par ex. méthode et réglementation) ;
   - `.claude/workflows/circuit-technique.js` : `BATTERIES` et `ZONES_PROTEGEES` ;
   - `docs/exigences.md`, `CONTEXT.md` ;
   - `.github/workflows/ci.yml` : jobs de tests, à ajouter aux contrôles requis du ruleset.
3. Retirer les agents inutiles (par ex. `app-review` sans interface) et leurs mentions dans `CLAUDE.md`.
4. Créer les libellés de `docs/agents/triage-labels.md` : `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`.
5. Premier travail : demander à `architect` le plan de la première branche de travail.

## Façon de travailler

- **Une branche de travail à la fois**, au périmètre fermé d'issues, PR brouillon dès la création ; fusion par le mainteneur, par commit de fusion, CI verte.
- **Ceux qui écrivent ne vérifient pas, ceux qui vérifient n'écrivent pas** ; un agent n'entre dans le circuit que si la modification touche son domaine.
- **Toute affirmation sur le code s'adosse à une mesure** exécutée ; tout changement de résultat a son tableau avant / après et son visa.
- **Audit léger en cours, revue finale complète avant la sortie du brouillon** ; documentation écrite une seule fois, en fin de branche.
- **Les issues ne sont créées qu'avec l'accord du mainteneur** ; les workflows ne commitent, ne poussent et ne créent rien.

Détail : `CLAUDE.md`.

## Sécurité du dépôt

Le dépôt est public. Réglages appliqués (à reproduire sur tout dépôt créé depuis ce modèle, `OWNER/REPO` à remplacer) :

- fusion par **commit de fusion seulement** (squash et rebase désactivés), wiki désactivé ;
- **secret scanning** et **push protection** activés ; **alertes et correctifs de sécurité Dependabot** activés ;
- Actions limitées à celles de GitHub (`github_owned_allowed`), jeton des workflows en lecture seule, actions épinglées par SHA ;
- ruleset **« Protection main »** : suppression et force-push interdits, PR obligatoire (fusion par commit de fusion, fils de discussion résolus), contrôle requis « Contrôles du dépôt » à jour avec `main`, sans contournement.

```bash
R=OWNER/REPO
gh api -X PATCH repos/$R -F allow_squash_merge=false -F allow_rebase_merge=false -F allow_merge_commit=true -F has_wiki=false \
  -f 'security_and_analysis[secret_scanning][status]=enabled' -f 'security_and_analysis[secret_scanning_push_protection][status]=enabled'
gh api -X PUT repos/$R/vulnerability-alerts
gh api -X PUT repos/$R/automated-security-fixes
gh api -X PUT repos/$R/actions/permissions -f enabled=true -f allowed_actions=selected
gh api -X PUT repos/$R/actions/permissions/selected-actions -F github_owned_allowed=true -F verified_allowed=false
gh api -X PUT repos/$R/actions/permissions/workflow -f default_workflow_permissions=read -F can_approve_pull_request_reviews=false
gh api -X POST repos/$R/rulesets --input .github/ruleset-main.json
```

Le ruleset est dans `.github/ruleset-main.json`. L'appliquer **après** le premier push sur `main`, qu'il bloque ensuite.
