#!/usr/bin/env bash
###############################################################################
#  .claude/outils/bilan_journal.sh  --  bilan du journal des sous-agents
#
#  Agrege .claude/journal-agents.jsonl (hook SubagentStop) par agent et par
#  modele servi : nombre de consultations, appels au modele, contexte au
#  dernier appel (moyenne et maximum), duree. Sert a la calibration de
#  docs/agents/routage.md, § 8. Aucune donnee de consommation n'est estimee :
#  seules les grandeurs lues dans les transcripts sont restituees.
#
#  Usage : bash .claude/outils/bilan_journal.sh [journal]
###############################################################################
set -euo pipefail
racine="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
journal="${1:-$racine/.claude/journal-agents.jsonl}"
[ -s "$journal" ] || { echo "Journal vide ou absent : $journal"; exit 0; }
py=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import json" >/dev/null 2>&1; then py="$c"; break; fi
done
[ -n "$py" ] || { echo "Python introuvable : bilan impossible."; exit 1; }
"$py" - "$journal" <<'PY'
import json, sys
from collections import defaultdict
g = defaultdict(list)
for l in open(sys.argv[1], encoding="utf-8"):
    try:
        d = json.loads(l)
    except Exception:
        continue
    g[(d.get("agent") or "?", ",".join(d.get("modeles") or ["?"]))].append(d)
print("%-24s %-28s %5s %7s %12s %12s %9s" % ("agent", "modele(s) servi(s)", "n", "appels", "ctx moyen", "ctx max", "duree moy"))
for (a, m), v in sorted(g.items()):
    ctx = [x["contexte_final"] for x in v if x.get("contexte_final") is not None]
    du = [x["duree_s"] for x in v if x.get("duree_s") is not None]
    print("%-24s %-28s %5d %7d %12s %12s %8ss" % (a, m[:28], len(v), sum(x.get("appels") or 0 for x in v),
          round(sum(ctx)/len(ctx)) if ctx else "-", max(ctx) if ctx else "-", round(sum(du)/len(du)) if du else "-"))
PY
