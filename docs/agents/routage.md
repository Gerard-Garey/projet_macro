# Routage du modèle et de l'effort des agents de pilotage et de fond

Politique appliquée par la session principale quand elle consulte `architect` ou un agent de fond (`macro`, `monnaie`, `jeu`). Décision : ADR 0006. Les agents de réalisation et de vérification (`coder`, `docwriter`, `audit`, `app-review`) ne sont pas concernés : leur fiche fixe leur modèle.

**Critères propres à ce projet**, dérivés de la politique du modèle `Modele_vibe_code` (son ADR 0001) et adaptés au moteur v3 et à l'instruction des blocs (§ 9). Ils se réévaluent à mesure que le projet évolue (§ 8), au plus tard à chaque jalon.

## 1. Principes

1. **Opus par défaut, Fable rarement.** Fable est réservé aux cas du § 4.1, ou à l'accord du mainteneur ; il n'est jamais un réflexe devant une difficulté.
2. **L'effort se règle indépendamment du modèle** : `medium` pour la routine, `high` pour le jugement.
3. **Les sous-agents rendent des constats, des preuves et des points ouverts ; la session principale applique la politique et décide de la suite.** Un agent signale les critères qu'il a rencontrés (§ 6), il ne décide pas de sa propre escalade, et il ne peut lancer aucun autre agent (l'outil `Agent` est absent de sa liste d'outils).
4. **Aucune escalade sans motif observable, aucune boucle** : plafonds du § 5.
5. **Aucun remplacement silencieux** d'un modèle par un autre (§ 5.3).

## 2. Mécanisme

Le paramètre `model` d'un appel `Agent` l'emporte sur le `model` de la fiche ; l'effort, lui, ne peut pas être passé à l'appel et vient de la fiche (champ `effort`), qui prime sur l'effort de la session (documentation Claude Code des sous-agents, champ `effort` : « Overrides the session effort level ») mais n'est pas observable dans le journal (§ 7). D'où deux fiches par rôle, au même corps :

| Fiche | Modèle servi | Effort | `maxTurns` | Usage |
|---|---|---|---|---|
| `architect`, `macro`, `monnaie`, `jeu` | `opus` | `medium` | 40 | routine (§ 3) |
| `architect-approfondi`, `macro-approfondi`, `monnaie-approfondi`, `jeu-approfondi` | `opus` | `high` | 80 | jugement (§ 3) |
| `architect-approfondi`, `macro-approfondi`, `monnaie-approfondi`, `jeu-approfondi` appelées avec `model: "fable"` | Fable (fiche : `opus`, l'appel l'emporte) | `high` | 80 | cas du § 4.1, ou accord du mainteneur |

- Les fiches `-approfondi` sont **générées** par `bash .claude/outils/fiches_jumelles.sh` à partir de la fiche de base : seul le frontmatter diffère (nom, description, effort, `maxTurns`). Ne jamais les modifier à la main ; la CI (job « Contrôles du dépôt ») vérifie la concordance (`--verifier`). La liste des rôles dédoublés est la variable `ROLES` du script.
- Fable en `xhigh` ou `max` : jamais sans accord explicite du mainteneur (il faudrait alors une troisième fiche, à créer sur décision). Fable en `medium` (fiche de base appelée avec `model: "fable"`) : sur indication explicite du mainteneur seulement.
- Les modèles sont désignés par **alias** (`opus`, `fable`), qui suivent les nouvelles versions ; le journal (§ 7) note la version effectivement servie.
- Une fiche modifiée n'est prise en compte que par une **session neuve** (`docs/agents/issue-tracker.md`, constat 3).

## 3. Matrice

« Routine » = fiche de base (Opus `medium`) ; « jugement » = fiche `-approfondi` (Opus `high`) ; « Fable » = fiche `-approfondi` avec `model: "fable"`.

| Rôle | Mission | Signaux observables | Départ | Preuves attendues | Suite | Arrêt |
|---|---|---|---|---|---|---|
| architect | Rattacher les nouvelles issues au point d'étape (lot) | aucun critère du § 4.2 | routine | tableau de couverture : chaque issue du lot → tâche → branche prévue, ou hors plan / doublon, avec la raison | un critère du § 4.2 → ligne « issue sensible » | toutes les issues du lot couvertes |
| architect | Point d'étape après fusion | lot ≥ 8 issues, plusieurs branches touchées, ou passage de jalon | routine ; jugement si l'un des signaux | SHA cités, dépendances ajoutées / retirées explicites, décisions M-n | seuil « macro » (§ 4.3) atteint → Fable **proposé** au mainteneur | feuille de route à jour |
| architect | Plan de la branche suivante | — | jugement | trois à cinq issues, ordre des commits, agent et circuit par tâche, critères d'acceptation | § 4.1 | plan complet |
| architect | Issue sensible : ADR, invariant de `CLAUDE.md` ou contrat partagé touché | § 4.2 | jugement | ADR et invariants cités, effet sur les contrats, branches touchées | § 4.1 ; sinon Fable **proposé** | avis rendu, ou décision du mainteneur |
| architect | Rédaction d'un ADR **d'architecture** (couches, invariants, contrats) | — | **Fable** (routage initial) | contexte, options écartées, conséquences | décision du mainteneur | ADR proposé |
| architect | Rédaction d'un ADR d'organisation (Git, processus, outillage) | — | jugement | idem | idem | idem |
| architect | Relecture d'une PR ou d'un diff de processus | — | jugement | constats par fichier et passage, texte proposé, motif, gravité | § 4.1 | relecture complète |
| `macro`, `monnaie` (expert pilote) | Validation après audit, sans changement de résultat | — | routine | diff, rapport d'audit, verdict référencé | relance ciblée si une preuve manque | verdict |
| `jeu` | Avis de lisibilité sur un levier, un indicateur ou une restitution, sans choix d'approche | — | routine | élément, verdict lisible / à clarifier / à revoir, scénario exécuté quand le simulateur existe, sinon passage cité de la fiche ou de la spécification qui décrit le mécanisme | relance ciblée si une preuve manque | avis rendu |
| `macro`, `monnaie` (expert pilote), `jeu` | Validation avec tableau avant / après (hors résultat final ou verdict) ; conformité à une source ; spécification ou plan | — | jugement | citation précise (texte, article, paragraphe) ou mesure exécutée ; chaque conclusion marquée vérifiée / hypothèse / non vérifiée | § 4.1 ; deux lectures → § 4.4 | verdict, matrice ou plan complet |
| `macro`, `monnaie` (expert pilote), `jeu` | Fiche comparative (instruction par l'expert pilote, avis de `jeu`), nouvelle approche | au moins deux options sans preuve qui départage | jugement | options, apport de chacune, références retrouvées | **arbitrage du mainteneur** ; Fable seulement à sa demande ou par § 4.1 | options décrites |
| tous | Changement d'un résultat final ou d'un verdict | tableau avant / après | jugement | tableau avant / après, lignes expliquées | Fable **seulement sur décision du mainteneur** | visa du mainteneur |

Mission absente de la matrice (par exemple révision globale, revue de fond avant un jalon) : jugement par défaut ; la session principale propose de l'ajouter à la matrice au point d'étape suivant.

## 4. Critères

### 4.1 Fable sans demander au mainteneur (liste fermée)

1. **Échec documenté d'Opus `high`** : après la consultation en jugement (et, s'il y a lieu, la relance ciblée), la preuve attendue manque encore **et** le blocage est de raisonnement — ni une information manquante, ni une exploration interrompue (§ 5.1).
2. **Désaccord entre agents** : expert contre `audit`, deux experts entre eux, ou un avis rendu par un agent qui contredit un ADR accepté alors que la question ne porte pas sur cet ADR (une issue ou une consultation qui propose de le modifier est une issue sensible, § 4.2 : Opus `high` d'abord, ADR 0006, décision 3). Fable **instruit** le désaccord, par une consultation neuve de la fiche `-approfondi` du rôle dont relève la question (le fond à l'expert pilote, la jouabilité à `jeu`, la forme du code et les ADR à `architect`), avec le dossier (§ 5.4) ; un désaccord entre `macro` et `monnaie` est instruit par `architect-approfondi`, tiers au désaccord, qui expose les deux positions sans trancher ; la décision reste au mainteneur quand `CLAUDE.md` la lui réserve.
3. **Rédaction d'un ADR d'architecture** (routage initial, § 3).

Tout autre usage de Fable est **proposé** au mainteneur (un message, réponse oui / non), qui peut aussi le demander d'office.

### 4.2 Issue sensible (revue plus forte, même pour une seule issue)

- un ADR accepté ou un invariant de `CLAUDE.md`, « Architecture », est contredit ou modifié ;
- un **contrat partagé** change : interface entre modules ou couches, format de données ou d'état, catalogue ou table utilisés par plusieurs branches ; dans ce projet : le noyau comptable (`noyau/` : grand livre, seul lieu d'exécution des flux, identités stock-flux et leur tolérance relative) ; l'interface bloc → noyau (état d'ouverture lu, flux proposés rendus, montants exécutés lus en lecture seule : ADR 0009) ; le schéma d'état typé et versionné (`etat/`) et la reprise exacte ; les phases numérotées de l'ordonnanceur, dont le groupe de la phase 9 (ADR 0009), et les paramètres typés (`moteur/`) ; les balises de concordance `eq:` ; le catalogue des leviers (`leviers/`) ; le cadre comptable de M22 (ADR 0005) : la matrice des bilans et la matrice des flux de transactions de `sec:cadre` (`tab:matrice-bilans`, `tab:matrice-flux`) — instruments et leurs émetteurs, règles de caisse, contreparties de règlement — et les portes de la monnaie (`tab:portes-monnaie`), avec leur convention d'écriture (fiche « temps et comptabilité » § 9.7, `docs/specification/CONVENTIONS.md` § 9), lues par `outils/verifier_matrices.py` et, au J2, par le noyau ; la règle de conversion `eq:moteur-conversion-taux` (linéaire, x/n_a, pour les taux d'intérêt, les flux et les vitesses : M22, lecture (a)) ; la conversion géométrique des taux de croissance et d'inflation `eq:moteur-conversion-croissance` ((1 + x)^{1/n_a} par pas : M25 (b), ADR 0008, partie I) ; le registre de l'indice des prix, 13 niveaux avancés en phase 9, et l'empreinte calendaire de l'état, 14 variables (ADR 0008, partie II) ; le retrait du texte non composé et ses anomalies (`preparer_tex_et_anomalies`, dont `preparer_tex` est l'enveloppe), commun au script de concordance et au script des matrices ;
- un résultat final ou un verdict change (Fable sur décision du mainteneur seulement).

Le nombre d'issues d'un lot n'est qu'un complément : un gros lot fait passer en jugement, il ne déclenche jamais Fable à lui seul ; une issue unique à fort impact est sensible quel que soit le lot.

### 4.3 Seuil « macro » du point d'étape (Fable proposé au mainteneur)

Un nouvel ADR d'architecture, ou le remplacement d'un ADR, est proposé ; **ou**, selon leur importance, au-dessus des seuils suivants :
- au moins deux couches de l'ADR 0002 (`noyau`, `blocs`, `moteur`, `etat`, `observation`, `scenarios`, `leviers`, interface) dont les dépendances changent ;
- au moins deux branches suivantes redécoupées ou réordonnées, ou l'ordre d'instruction des blocs (`docs/blocs/README.md`) modifié ;
- un jalon J1 à J8 dont le contenu ou le critère de passage change (un critère s'écrit avant l'essai : `docs/exigences.md` § 2).

Sous le seuil : jugement, sans question au mainteneur.

### 4.4 Ni Fable ni effort : obtenir une information ou une preuve

- **Deux lectures d'une source** : vérifier d'abord qu'il ne s'agit pas d'un problème de documentation (version erronée, texte inaccessible, extraction défectueuse) ; si oui, obtenir la bonne source. Si les deux lectures subsistent, l'expert les décrit et le mainteneur tranche (`CLAUDE.md`) : Fable n'est pas requis.
- **Issue insuffisamment décrite** : question au mainteneur (libellé `needs-info`), pas d'escalade.
- **Source non retrouvée** par l'agent : décision du mainteneur, même si l'agent se dit sûr.
- **Question qu'aucun test ni aucune source ne tranche** : d'abord chercher la mesure ou la source ; si le blocage est de raisonnement, Fable est **proposé**.

## 5. Transitions, plafonds et arrêts

### 5.1 Cinq actions, choisies selon la nature du blocage

| Blocage constaté dans le retour | Action | Forme |
|---|---|---|
| statut `complet` sans les preuves prévues, retour marqué partiel par Claude Code (plafond de tours `maxTurns` atteint), ou retour sans bloc « Retour » | **relance ciblée** | reprise du même agent (`SendMessage`), contexte conservé, même fiche ; statut requalifié `partiel` |
| exploration incomplète (lectures non faites, périmètre non couvert) ou blocage de raisonnement, en routine | **hausse d'effort** | consultation neuve de la fiche `-approfondi`, avec le dossier (§ 5.4) |
| exploration incomplète en jugement | **relance ciblée** | reprise du même agent (`SendMessage`), même fiche ; ensuite arrêt (§ 5.2) |
| blocage de raisonnement en jugement, ou critère du § 4.1 | **changement de modèle** | consultation neuve de la fiche `-approfondi` avec `model: "fable"`, avec le dossier |
| information, source ou mesure manquante | **obtenir l'information ou la preuve** | lancer la mesure, retrouver la source, ou demander au mainteneur |
| décision réservée (visa, deux lectures, approche, source non retrouvée, Fable proposé) | **décision humaine** | question au mainteneur, avec les rapports |

Ordre selon la nature du blocage : information → preuve ; exploration → effort ; raisonnement → effort en routine, puis modèle en jugement. Pas de palier Opus `high` imposé avant Fable quand un critère du § 4.1 est présent d'emblée : § 4.1.3 (ADR d'architecture) dès le départ, § 4.1.2 (désaccord) dès qu'il est constaté, même entre consultations de routine.

### 5.2 Plafonds

- **Par question** : au plus une relance ciblée, une hausse d'effort et une consultation Fable ; ensuite arrêt et compte rendu au mainteneur, statut `revue requise` ; l'accord du mainteneur lève le plafond (§ 5.5).
- **Par branche de travail** : au-delà de **3 consultations Fable** (ADR compris), accord du mainteneur avant chaque nouvelle consultation.
- **Par consultation** : `maxTurns` de la fiche (40 ou 80). Ce plafond borne les tours, **pas les tokens** ; une réponse courte ne borne pas le raisonnement.

### 5.3 Modèle indisponible, plafond atteint

Arrêt et question au mainteneur : attendre, ou accepter une consultation Opus `high` dont l'avis porte la mention « rendu sans Fable, à revoir ». Jamais de remplacement silencieux : la session principale compare le modèle servi, relevé par le journal (§ 7), au modèle demandé (modèle de la fiche, ou `model` de l'appel), qu'elle note dans la ligne d'escalade de la PR ; le journal ne voit pas le `model` passé à l'appel.

### 5.4 Dossier d'escalade

Une consultation neuve (hausse d'effort ou changement de modèle) reçoit un dossier court, et non une nouvelle revue globale :

```
Question résiduelle :
Contraintes (ADR, invariants, décisions M-n) :
Conclusions établies (avec leurs preuves) :
Sources et fichiers utiles (chemins, articles) :
Tentatives et résultats (fiche, modèle, statut, ce qui a manqué) :
Contradictions :
Preuve attendue pour conclure :
```

### 5.5 Priorité entre règles

1. `CLAUDE.md` (visa, décisions réservées au mainteneur, deux lectures d'une source) ;
2. indisponibilité d'un modèle ou plafond atteint (§ 5.2, § 5.3) : arrêt et question au mainteneur ; seul son accord, donné après l'arrêt, lève le plafond ;
3. décisions explicites du mainteneur ;
4. critères du § 4.1 ;
5. jugement de la session principale, appuyé sur les signaux du § 3.

Un signal auto-déclaré (difficulté ressentie, note de confiance) complète l'analyse sans la remplacer.

## 6. Retour structuré des agents

Chaque consultation se termine par un bloc « Retour » (fiches `architect`, `macro`, `monnaie`, `jeu`, section « Retour ») : statut (`complet`, `partiel`, `revue requise`), résultat, preuves (chaque conclusion vérifiée / hypothèse / non vérifiée), informations manquantes, décisions non résolues, critères déclenchés (§ 4), prochaine action recommandée. `architect` y ajoute le tableau de couverture du lot et les dépendances modifiées. `complet` exige toutes les preuves prévues au § 3 ; sinon la session principale requalifie en `partiel` (§ 5.1).

## 7. Traçabilité

- **Journal local** : le hook `SubagentStop` (`.claude/hooks/journal_agents.sh`) ajoute une ligne JSON par sous-agent terminé (toutes fiches, pas seulement les consultations) à `.claude/journal-agents.jsonl` (non versionné) : date, agent, identifiant, modèles servis, nombre d'appels au modèle, contexte au dernier appel (tokens d'entrée, cache compris), durée. Il ne mesure ni l'effort (non exposé) ni les tokens de sortie (non fiables dans le transcript). Exception à `CLAUDE.md`, « Commandes », et à l'ADR 0003, pt 1 (« Python s'exécute toujours par `uv run` ») : le hook et le bilan appellent le Python du système, sans dépendre de l'environnement du projet ; un interpréteur qui échoue au test `import json` (alias du Microsoft Store) est écarté, et la session se poursuit sans journal. Le transcript est écrit de façon asynchrone et peut ne pas contenir les derniers messages quand le hook s'exécute : appels et contexte au dernier appel sont des minorants possibles. En session cloud, il disparaît avec le conteneur : avant la fin d'une telle session, la session principale colle la sortie de `bash .claude/outils/bilan_journal.sh` dans un commentaire de la PR de la branche de travail.
- **Bilan** : `bash .claude/outils/bilan_journal.sh` agrège le journal par agent et par modèle. Une reprise (`SendMessage`) ajoute pour le même sous-agent une ligne cumulative (appels, durée attente comprise) : le bilan ne garde que la dernière et compte les reprises.
- **Trace durable** : chaque escalade (hausse d'effort, Fable), relance ciblée ou arrêt est notée par la session principale dans la PR de la branche de travail, une ligne : `fiche / modèle / critère déclenché / statut obtenu / suite`. Hors de toute branche ouverte (point d'étape entre deux branches, par exemple), la ligne va dans la section « Escalades, relances et arrêts hors branche » de `docs/feuille-de-route.md` (citée par son nom, son numéro pouvant changer), et une consultation Fable faite hors branche compte pour la branche suivante (§ 5.2).
- `/usage` (abonnement) attribue approximativement l'usage récent aux sous-agents (24 h ou 7 jours, poste courant seulement : une session cloud n'est vue que d'elle-même) ; l'export OpenTelemetry est l'autre source, que le dépôt ne configure pas.

## 8. Calibration et retour arrière

- **Calibration** : après les dix premières consultations `architect`, `macro`, `monnaie`, `jeu`, puis à chaque point d'étape d'`architect`, relire le bilan du journal et les lignes d'escalade des PR et de `docs/feuille-de-route.md` (escalades hors branche) : part des relances ciblées (fiches trop légères ?), escalades vers Fable et leur apport réel, contexte au dernier appel (lectures trop larges ?). Ajuster les seuils et efforts par un commit `claude:` motivé ; une réorientation durable s'annote dans l'ADR 0006.
- **Retour au comportement antérieur** (Fable pour tout), sur décision du mainteneur : de préférence, annuler le commit de fusion de la PR qui a introduit la politique (`git revert -m 1 <sha>`), puis rétablir l'ADR 0006, la ligne M23 et la section « Escalades, relances et arrêts hors branche » de la feuille de route, avec ses lignes (l'annulation les supprime), en les annotant « Politique abandonnée le … » (ou `superseded by NNNN` si un nouvel ADR consigne le retour) ; à défaut, à la main : remettre `model: fable` dans `architect.md`, `macro.md`, `monnaie.md` et `jeu.md`, retirer `effort`, `maxTurns` et la phrase « Fiche de routine… » des descriptions, vider `ROLES` dans `.claude/outils/fiches_jumelles.sh`, supprimer les fiches `-approfondi` et le contrôle CI correspondant, retirer de `CLAUDE.md` le paragraphe « Routage du modèle et de l'effort », et annoter l'ADR 0006 et la ligne M23.

## 9. Adapter la politique à un projet

Emplacements réellement lus :

| Emplacement | Ce qu'on y adapte |
|---|---|
| `docs/agents/routage.md` (ce fichier) | matrice (§ 3), seuils et contrats partagés (§ 4.2, § 4.3), plafonds (§ 5.2) |
| frontmatter de `architect.md`, `macro.md`, `monnaie.md` et `jeu.md` | effort et `maxTurns` de routine ; le script reprend leur modèle, leurs outils et leur corps dans les fiches `-approfondi` |
| `.claude/outils/fiches_jumelles.sh`, variables `ROLES`, `EFFORT_APPROFONDI`, `TOURS_APPROFONDI` | rôles dédoublés (experts supplémentaires), effort et plafond de jugement |
| `CLAUDE.md`, « Sous-agents » | renvoi à ce fichier ; règles qui priment (§ 5.5, rang 1) ; liste du § 4.1 et plafonds du § 5.2, recopiés : à tenir identiques |

Ces critères s'articulent avec `CLAUDE.md` sans le remplacer : les décisions qu'il réserve au mainteneur restent les siennes quel que soit le modèle. Vérification : `bash .claude/outils/fiches_jumelles.sh --verifier` (la CI), puis, dans une session neuve, une consultation de chaque fiche suivie de `bash .claude/outils/bilan_journal.sh` pour lire le modèle servi.

Adaptations retenues pour ce projet (30/09/2026) : les trois agents de fond (`macro`, `monnaie`, `jeu`) sont dédoublés ; « expert » désigne l'expert pilote du bloc (`CLAUDE.md`, « Experts de fond ») ; une fiche comparative part en jugement, et l'approche reste **décidée par le mainteneur** (M-n) quel que soit le modèle ; un désaccord entre `macro` et `monnaie` est tranché par le mainteneur (`CLAUDE.md`) : Fable peut l'instruire (§ 4.1, point 2), jamais le trancher ; est **résultat final** l'état stationnaire de référence et le verdict du test zéro ou d'un scénario ; contrats partagés et seuil « macro » ci-dessus (§ 4.2, § 4.3). Complétées le 02/10/2026 (relecture de la PR #22) : mission de routine propre à `jeu` (§ 3) ; désaccord entre `macro` et `monnaie` instruit par `architect-approfondi` (§ 4.1, point 2) ; plafond levé par un accord donné après l'arrêt (§ 5.5) ; exception à `uv run` pour le journal et son bilan (§ 7). Complétées le 02/10/2026 (point d'étape après la PR #20, constat C15 de la relecture de la PR #22, accord du mainteneur) : contrats partagés issus de M22 et `preparer_tex` (§ 4.2).
