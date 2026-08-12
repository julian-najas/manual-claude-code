#!/usr/bin/env bash
# Formatea despues de editar. No bloquea nunca: si el formateador falla,
# el trabajo sigue. Sale 0 siempre a proposito.
set -uo pipefail

RUTA="$(cat | python3 -c 'import sys,json;print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null || true)"
RUTA="${RUTA//\\//}"
[ -f "$RUTA" ] || exit 0

case "$RUTA" in
  *.py)               command -v ruff       >/dev/null && ruff format "$RUTA"        >/dev/null 2>&1 ;;
  *.ts|*.tsx|*.js|*.jsx|*.json|*.css|*.md) command -v prettier >/dev/null && prettier -w "$RUTA" >/dev/null 2>&1 ;;
  *.go)               command -v gofmt      >/dev/null && gofmt -w "$RUTA"           >/dev/null 2>&1 ;;
  *.rs)               command -v rustfmt    >/dev/null && rustfmt "$RUTA"            >/dev/null 2>&1 ;;
esac
exit 0
