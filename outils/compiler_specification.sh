#!/usr/bin/env bash
###############################################################################
#  outils/compiler_specification.sh  --  compilation XeLaTeX de la specification
#
#  Usage : bash outils/compiler_specification.sh [chemin/du/fichier.tex]
#  (defaut : docs/specification/nations_et_marches.tex)
#
#  Procedure de docs/specification/CONVENTIONS.md, § 7, commune a la CI et a la
#  skill compiler-doc :
#    - passes XeLaTeX (au moins trois) jusqu'a disparition de « Rerun to get
#      cross-references right » dans le journal ; au-dela de cinq passes, un
#      renvoi oscille : echec ;
#    - controle du journal final : aucune ligne commencant par « ! », aucune
#      occurrence de « undefined » (renvoi ou citation) ; les « Overfull » et
#      « Underfull » sont comptes et listes, sans faire echouer.
#  Code de sortie : 0 si le PDF est produit et le journal propre, 1 sinon.
#  xelatex doit etre dans le PATH (.claude/hooks/preparer_latex.sh).
###############################################################################

set -u

TEX="${1:-docs/specification/nations_et_marches.tex}"
PASSES_MIN=3
PASSES_MAX=5

if ! command -v xelatex >/dev/null 2>&1; then
  echo "xelatex introuvable : lancer bash .claude/hooks/preparer_latex.sh --installer" >&2
  exit 1
fi
if [ ! -f "$TEX" ]; then
  echo "Specification introuvable : $TEX" >&2
  exit 1
fi

dossier=$(dirname "$TEX")
nom=$(basename "$TEX" .tex)
journal="$dossier/$nom.log"

echo "Chaine : $(xelatex --version 2>&1 | head -n 1)"
passe=0
while :; do
  passe=$((passe + 1))
  if ! (cd "$dossier" && xelatex -interaction=nonstopmode -halt-on-error "$nom.tex" >/dev/null); then
    echo "Passe $passe : echec de XeLaTeX. Fin du journal :" >&2
    grep -n -A 3 '^!' "$journal" >&2 || tail -n 30 "$journal" >&2
    exit 1
  fi
  relance=$(grep -c 'Rerun to get' "$journal")
  echo "Passe $passe : terminee (demandes de relance : $relance)."
  if [ "$passe" -ge "$PASSES_MIN" ] && [ "$relance" -eq 0 ]; then
    break
  fi
  if [ "$passe" -ge "$PASSES_MAX" ]; then
    echo "Renvois instables apres $PASSES_MAX passes." >&2
    exit 1
  fi
done

statut=0
if grep -n '^!' "$journal"; then
  echo "Erreur LaTeX dans $journal (lignes ci-dessus)." >&2
  statut=1
fi
if grep -n 'undefined' "$journal"; then
  echo "Renvoi ou citation indefini dans $journal (lignes ci-dessus)." >&2
  statut=1
fi
debordements=$(grep -c -E '^(Overfull|Underfull)' "$journal")
echo "Overfull et Underfull : $debordements."
grep -n -E '^(Overfull|Underfull)' "$journal"

if [ "$statut" -eq 0 ]; then
  echo "PDF produit : $dossier/$nom.pdf ; journal propre."
fi
exit $statut
