#!/usr/bin/env bash
# PostCompact: reinyecta las reglas que la compactacion se lleva.
# El CLAUDE.md de la raiz se reinyecta solo; los CLAUDE.md anidados y las
# reglas con paths NO. Esto cubre ese hueco.
set -euo pipefail
cat >/dev/null   # consumimos la entrada, no la necesitamos

ARCHIVO="${CLAUDE_PROJECT_DIR:-.}/.claude/reglas-permanentes.md"
[ -f "$ARCHIVO" ] || exit 0
echo "Recordatorio de reglas permanentes tras compactar:"
cat "$ARCHIVO"
exit 0
