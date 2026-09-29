# Glossaire

Vocabulaire à employer tel quel dans le code, la documentation, les issues et les comptes rendus d'agents. Un terme nouveau ou précisé est ajouté par `architect`.

## Domaine

**À ADAPTER** : un terme par entrée, sa définition, et les synonymes écartés.

- **<terme>** : <définition>. *Ne pas dire* : <synonyme écarté>.

## Organisation du travail

- **Branche de travail** : l'unique branche `claude/…` en cours, au périmètre fermé d'issues, portée par une PR brouillon vers `main`.
- **Correctif rapide** : modification hors périmètre qui laisse les résultats strictement identiques, touche un seul domaine de commit et pas la documentation de fond ; branche temporaire partie de `main`, PR directe.
- **Tableau avant / après** : pour un commit qui change un résultat, une ligne par grandeur modifiée (avant, après, écart, explication).
- **Visa** : approbation d'un tableau avant / après — par le mainteneur pour un résultat final ou un verdict, par `expert` sinon. Sans visa, rien n'est commité.
- **Surface d'impact documentaire** : liste, dans le commit proposé par `coder`, des endroits de la documentation que la modification oblige à rouvrir ; point de départ de `docwriter`.
- **Constat** : défaut du code relevé par un vérificateur, avec gravité (bloquant / majeur / mineur), `fichier:ligne` et mesure exécutée. Conduit à une reprise ou à un arrêt.
- **Question pour `expert`** : doute sur le fond, qui n'est pas un défaut du code ; ne relance pas `coder`.
- **Audit léger** : lecture du diff et des fonctions touchées avec leurs appelants et appelés.
- **Revue finale complète** : lecture de tout `git diff main...HEAD`, batteries complètes et scénarios adverses, avant la sortie du brouillon.
- **Mesure** : commande exécutée et sa sortie, qui fonde une affirmation sur le comportement du code.
