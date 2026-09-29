#!/usr/bin/env bash
###############################################################################
#  .claude/hooks/preparer_latex.sh  --  HOOK SessionStart DE CLAUDE CODE
#
#  Rend xelatex disponible pour compiler docs/specification/
#  nations_et_marches.tex (ADR 0004, CONVENTIONS.md § 7) :
#    - xelatex deja dans le PATH : rien a faire ;
#    - poste Windows (Git Bash) : MiKTeX installe mais absent du PATH -> ajout
#      au PATH de la session ;
#    - Linux sans LaTeX (session cloud) : installation de TeX Live par apt,
#      seulement avec l'argument --installer (plusieurs minutes), que passe la
#      skill compiler-doc au moment de compiler ; au demarrage de session, le
#      hook se contente de signaler l'absence.
#  Au demarrage (sans argument), le hook n'echoue jamais.
#  Modele : .claude/hooks/preparer_latex.sh du depot Gerard-Garey/outil_usp,
#  adapte a XeLaTeX.
###############################################################################

# Paquets du preambule v1.5 (CONVENTIONS.md § 3), identiques au job de
# compilation de .github/workflows/ci.yml.
PAQUETS_TEXLIVE="texlive-xetex texlive-lang-french texlive-latex-recommended \
texlive-latex-extra texlive-pictures texlive-fonts-recommended fonts-lmodern"

# Ajoute un dossier au PATH de la session. $CLAUDE_ENV_FILE est fourni par
# Claude Code aux hooks SessionStart : les lignes qui y sont ecrites
# s'appliquent aux commandes Bash de la session.
ajouter_au_path() {
  export PATH="$1:$PATH"
  if [ -n "$CLAUDE_ENV_FILE" ]; then
    printf 'export PATH="%s:$PATH"\n' "$1" >> "$CLAUDE_ENV_FILE"
  fi
}

# installer_apt <paquet>... : installe par apt (session cloud Linux) et reussit
# si xelatex est ensuite disponible. La sortie d'apt va dans un journal, dont
# la fin est affichee en cas d'echec.
installer_apt() {
  command -v apt-get >/dev/null 2>&1 || return 1
  SUDO=""
  if [ "$(id -u)" != "0" ] && command -v sudo >/dev/null 2>&1; then SUDO="sudo -n"; fi
  journal="${TMPDIR:-/tmp}/apt_xelatex.log"
  apt="$SUDO env DEBIAN_FRONTEND=noninteractive apt-get"
  if $apt update -qq >"$journal" 2>&1 &&
     $apt install -y -qq --no-install-recommends "$@" >>"$journal" 2>&1 &&
     command -v xelatex >/dev/null 2>&1; then
    return 0
  fi
  tail -n 5 "$journal" >&2
  return 1
}

rapport() {
  echo "LaTeX pour cette session : $(xelatex --version 2>&1 | head -n 1) ($1)."
}

if command -v xelatex >/dev/null 2>&1; then
  rapport "deja dans le PATH"
  exit 0
fi

# --- Poste Windows (Git Bash) : MiKTeX installe hors du PATH -----------------
lad=$(cygpath -u "${LOCALAPPDATA:-}" 2>/dev/null || echo "${LOCALAPPDATA:-}")
for bin in "$lad/Programs/MiKTeX/miktex/bin/x64" "/c/Program Files/MiKTeX/miktex/bin/x64"; do
  if [ -x "$bin/xelatex.exe" ]; then
    ajouter_au_path "$bin"
    rapport "ajoute au PATH depuis $bin"
    exit 0
  fi
done

# --- Linux (session cloud) : installation par apt, a la demande --------------
if [ "${1:-}" != "--installer" ]; then
  echo "LaTeX absent ; la skill compiler-doc l'installera au besoin (bash .claude/hooks/preparer_latex.sh --installer)."
  exit 0
fi
echo "Installation de TeX Live par apt, plusieurs minutes..." >&2
# shellcheck disable=SC2086
if installer_apt $PAQUETS_TEXLIVE; then
  rapport "installe par apt"
  exit 0
fi
echo "ATTENTION : xelatex est introuvable et n'a pas pu etre installe ; le PDF ne peut pas etre compile dans cette session."
exit 1
