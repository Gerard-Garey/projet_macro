---
name: compiler-doc
description: Compiler la spécification LaTeX (docs/specification/nations_et_marches.tex) en XeLaTeX et contrôler le journal avant commit. À utiliser après toute modification du .tex, ou quand on demande de recompiler ou de régénérer le PDF.
---

# Compiler la spécification

Le PDF `docs/specification/nations_et_marches.pdf` est **versionné** : il est recompilé et commité avec toute modification du `.tex`, dans le **même commit** `docs:`, sur le poste local comme en session cloud (`docs/specification/CONVENTIONS.md` § 7, ADR 0004). Un `.tex` modifié sans son PDF est un commit incomplet.

La procédure (passes, contrôle du journal) est portée par le script `outils/compiler_specification.sh`, que la CI exécute aussi : la skill ne la refait pas à la main.

## Étapes

0. **Rendre `xelatex` disponible.** Le hook `SessionStart` (`.claude/hooks/preparer_latex.sh`) ajoute MiKTeX au `PATH` sur le poste local. En session cloud, il n'installe rien au démarrage : si `command -v xelatex` échoue, lancer depuis la racine du dépôt `bash .claude/hooks/preparer_latex.sh --installer` (TeX Live par `apt`, plusieurs minutes ; en arrière-plan dès que la tâche touche au `.tex`). En cas d'échec, le PDF ne peut pas être compilé : le dire dans le compte rendu, et ne pas commiter le `.tex` seul.

1. **Relever l'état d'avant** (pour la comparaison de l'étape 3) : nombre de pages du PDF versionné et `Overfull` / `Underfull` du dernier journal, s'il existe.

2. **Compiler** depuis la racine du dépôt :

   ```bash
   bash outils/compiler_specification.sh
   ```

   Le script enchaîne les passes XeLaTeX (`-interaction=nonstopmode -halt-on-error`), trois au moins, jusqu'à disparition de toute demande de relance dans le journal (motif `Rerun to get|Rerun LaTeX` : « Rerun to get cross-references right », et « Table widths have changed. Rerun LaTeX. » de `longtable`) ; au-delà de cinq passes, un renvoi oscille et le script échoue. Il contrôle ensuite le journal `docs/specification/nations_et_marches.log` :
   - aucune ligne commençant par `!` ;
   - aucune occurrence de `undefined` (renvoi ou citation indéfini) ;
   - les `Overfull` et `Underfull` sont comptés et listés, sans faire échouer.

   Code de sortie non nul → lire l'erreur affichée (lignes `!`, avec le numéro de ligne `l.NNN` du `.tex`), corriger et recommencer.

3. **Comparer à l'état d'avant** et le consigner dans le compte rendu :
   - les `Overfull` et `Underfull` **nouveaux** (à corriger s'ils débordent visiblement, plus de 10 pt, sur les lignes modifiées) ;
   - le nombre de pages et la table des matières ;
   - la chaîne de composition, affichée par le script en tête de sortie : MiKTeX sur le poste local, TeX Live en session cloud.

4. **Vérifier la concordance** : `uv run python outils/concordance_spec_moteur.py --strict` (labels, balises, `\code{…}`, encadrés « Lecture » ; contrat de `CONVENTIONS.md` § 9).

5. **Vérifier ce qui sera commité** : `git status docs/specification` doit montrer le `.tex` et le `.pdf` modifiés ensemble. Les fichiers auxiliaires (`.aux`, `.log`, `.out`, `.toc`) sont ignorés par Git.

La CI (job « Compilation de la spécification ») compile aussi le `.tex` à chaque push, avec le même script : c'est un contrôle, pas la source du PDF versionné.
