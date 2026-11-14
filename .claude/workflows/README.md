# Workflows du projet

Ce fichier porte les règles des workflows de `.claude/workflows/`, déplacées de `CLAUDE.md` (« Sous-agents ») le 13/11/2026 sans changement de fond ni de numérotation : « principe N des workflows » renvoie ici. `CLAUDE.md` en garde le résumé.

Un workflow met en œuvre un circuit type et en fixe les appels d'agents, les sorties structurées et les conditions d'arrêt. Huit principes :

1. lancement **sur commande explicite du mainteneur** uniquement ;
2. **aucune écriture dans l'historique ni l'état partagé** par le workflow ou ses agents : ni `git commit`, ni `git push`, ni régénération de référence, ni création d'issue — interdiction portée par les consignes et les fiches, les permissions de `.claude/settings.json` ne l'imposant pas : la session principale vérifie `git status` et `git log` après chaque workflow ;
3. **arrêt avec les rapports à tout point de décision** (question de fond, visa du mainteneur, contradiction entre vérificateurs) ;
4. **au plus une reprise** `coder` → `audit` ;
5. **vérificateurs ciblés sur le diff** (audit léger) ;
6. **constats structurés** : gravité (bloquant / majeur / mineur), `fichier:ligne`, mesure exécutée ; un constat sans emplacement ni mesure n'est pas recevable ;
7. **tout contrôle mécanique est un script**, jamais un agent : un agent lit la sortie d'un script, il ne refait pas le décompte ; un contrôle récurrent sans script en appelle un (issue) ;
8. **effort réduit** pour les étapes mécaniques ; aucun `model` fixé dans un workflow (hérité de la session).

Un **constat** (défaut du code) conduit à la reprise ou à l'arrêt ; une **question pour l'expert** (doute de `coder`, question de l'audit) ne relance pas `coder`. Trois statuts de fin : `termine`, `termine avec questions` (les seules remontées sont des questions : la session principale les porte à l'expert pilote avant tout commit), `arrete` ; une batterie en échec à la dernière vérification finit toujours par `arrete`.
