---
status: accepted
date: 2026-09-30
---

# Opus par défaut pour architect et les agents de fond, effort réglé à part, Fable réservé à une liste fermée de cas

## Contexte

`architect`, `macro`, `monnaie` et `jeu` tournaient sur Fable pour toutes leurs missions, sans effort ni plafond de tours fixés (effort hérité de la session). La lecture imposée au démarrage d'`architect` (`CLAUDE.md`, `docs/exigences.md`, `CONTEXT.md`, tous les ADR, la feuille de route) représentait environ 103 Ko au 30/09/2026 (`wc -c` : 20 898 + 12 656 + 8 479 + 43 784 + 17 265 octets), celle de `macro` et `monnaie` environ 94 Ko (tous les ADR et l'inventaire des blocs `docs/blocs/README.md`, 8 193 octets, compris : 94 010 octets), celle de `jeu` environ 103 Ko (la feuille de route au lieu de l'inventaire : 103 082 octets), relue à chaque consultation, y compris pour un simple rattachement d'issues. Le mainteneur travaille sur abonnement : la contrainte est la limite d'usage. Aucune mesure de consommation par agent n'existait.

Le modèle `Modele_vibe_code` a adopté le 30/09/2026 une politique de routage (ADR 0001 de ce dépôt-là, PR Gerard-Garey/Modele_vibe_code#1, tête `58bee0e`, fusionnée en `fac6999`), arrêtée par le mainteneur après entretien ; le présent ADR la reprend et l'adapte. Contraintes techniques (Claude Code 2.1.286) : le paramètre `model` d'un appel `Agent` l'emporte sur la fiche ; l'effort ne se fixe que dans la fiche pour l'outil `Agent` (l'API des workflows l'accepte à l'appel : `.claude/workflows/circuit-technique.js`, `effort: 'low'`) ; une fiche n'est pas rechargée en cours de session (`docs/agents/issue-tracker.md`, constat 3).

## Décision

Arrêtée par le mainteneur le 30 septembre 2026 (M23) :

1. Opus par défaut ; deux fiches par rôle au même corps : de base (effort `medium`, 40 tours) et `-approfondi` (effort `high`, 80 tours), générée par `.claude/outils/fiches_jumelles.sh`, contrôlée par la CI (job « Contrôles du dépôt »). Les trois agents de fond (`macro`, `monnaie`, `jeu`) sont dédoublés.
2. Fable (fiche `-approfondi` avec `model: "fable"`) sans demander dans trois cas : échec documenté d'Opus `high` sur un blocage de raisonnement ; désaccord entre agents ; rédaction d'un ADR d'architecture. Tout autre usage est proposé au mainteneur ; un changement de résultat final n'appelle Fable que sur sa décision.
3. Escalade selon la nature du blocage ; une issue qui touche un ADR, un invariant ou un contrat partagé passe d'abord par Opus `high` ; plafonds (une relance ciblée, une hausse d'effort, une consultation Fable par question ; trois consultations Fable par branche, ADR compris) ; arrêt sans remplacement silencieux si un modèle est indisponible.
4. Lecture ciblée par type de mission ; retour structuré ; journal local (hook `SubagentStop`) et une ligne par escalade, relance ciblée ou arrêt dans la PR (hors branche : feuille de route, section « Escalades, relances et arrêts hors branche »).
5. Critères propres au projet : `docs/agents/routage.md` § 4.2, § 4.3 et § 9. L'approche d'un bloc reste décidée par le mainteneur sur fiche comparative, et un désaccord entre `macro` et `monnaie` reste tranché par lui : Fable peut l'instruire, jamais le trancher.

## Options écartées

Reprises de l'ADR 0001 du modèle (`fac6999`), avec leurs motifs :

- **Fable pour tout** (état antérieur) : qualité sûre, mais consommation maximale sur des missions routinières.
- **Une seule fiche par rôle, effort hérité de la session** : l'effort ne peut alors varier qu'avec la session entière, pas par mission.
- **Fiches jumelles tenues à la main** : dérive certaine entre les deux corps ; remplacée par une génération contrôlée par la CI.
- **Fable en `medium` par défaut** : Fable n'étant appelé qu'après filtrage des cas faciles, un passage en `medium` risquerait de gâcher l'unique consultation Fable autorisée par question ; `medium` reste possible sur indication du mainteneur.
- **Routage par le nombre d'issues ou par la confiance déclarée de l'agent** : signaux complémentaires seulement ; une issue unique à fort impact serait sous-évaluée.
- **Consultation par un workflow fixant l'effort à l'appel** : un workflow ne se lance que sur commande explicite du mainteneur (`CLAUDE.md`, « Workflows », principe 1) et sert à des circuits, pas à des consultations isolées.
- **Escalade décidée par le sous-agent** : impossible techniquement (ni modèle ni effort modifiables en cours de consultation, pas d'outil `Agent`) et contraire à la séparation constats / décision.

Propres au projet :

- **Garder `jeu` sur Fable** : le mainteneur a inclus `jeu` parmi les agents de fond concernés.
- **Fable d'office pour les fiches comparatives** : l'approche est décidée par le mainteneur, pas par l'agent.

## Conséquences

- Fichiers : fiches `architect.md`, `macro.md`, `monnaie.md`, `jeu.md` et leurs `-approfondi` ; `.claude/outils/` ; `.claude/hooks/journal_agents.sh`, `.claude/settings.json` ; `.github/workflows/ci.yml` ; `docs/agents/routage.md` ; `CLAUDE.md`, `README.md`, `CONTEXT.md`, modèle de PR, `.gitignore`, `docs/feuille-de-route.md` (M23, section « Escalades, relances et arrêts hors branche »).
- Branche : `claude/routage-modele-effort` (PR #22), ad hoc, sur instruction du mainteneur du 30/09/2026, sans créer de catégorie de branche : pendant qu'elle est ouverte, la PR #22 n'est pas la PR d'une branche de travail (`CLAUDE.md`, « Session cloud ») ; la branche de travail reste `claude/j1-temps-comptabilite` (PR #20) ; les consultations faites pour #22 sont tracées dans la PR #22 et comptent pour son propre plafond Fable. Les messages des commits `e0df3bb` et `4408522` citent encore « ADR 0005, décision M20 », numéros renumérotés avant fusion (collision avec la PR #20).
- Effet sur les résultats : aucun.
- Non réglé : l'effort de la fiche prime sur celui de la session (documentation Claude Code des sous-agents, champ `effort` : « Overrides the session effort level ») mais n'est pas observable dans le journal ; `maxTurns` ne borne pas les tokens ; seuils à calibrer sur les premières consultations (`docs/agents/routage.md`, § 8), qui dit aussi comment revenir en arrière.

Issues : aucune (branche ad hoc sur instruction du mainteneur, M23) ; PR #22.
