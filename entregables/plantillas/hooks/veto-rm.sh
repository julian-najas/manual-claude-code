#!/usr/bin/env bash
# Bloquea borrados masivos. El filtro fino va en el campo "if" del hook,
# esto es la segunda linea de defensa.
set -euo pipefail

CMD="$(cat | python3 -c 'import sys,json;print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null || true)"

if printf '%s' "$CMD" | grep -qE '(^|[;&|]\s*)rm\s+(-[a-zA-Z]*\s+)*-[a-zA-Z]*[rR][a-zA-Z]*f|rm\s+-fr'; then
  echo "Bloqueado: borrado recursivo forzado. Hazlo a mano si de verdad toca." >&2
  exit 2
fi
exit 0
