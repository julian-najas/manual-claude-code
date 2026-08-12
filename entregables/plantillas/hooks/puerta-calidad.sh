#!/usr/bin/env bash
# Puerta de calidad de fin de turno. BLOQUEANTE a proposito: tiene que poder vetar.
# Usa la salida JSON de decision de nivel superior, cuyo unico valor es "block".
set -uo pipefail
cat >/dev/null

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

# Ajusta este comando a tu proyecto. Si no hay nada que comprobar, no hay puerta.
if [ -f package.json ] && command -v npm >/dev/null; then
  COMPROBAR="npm test --silent"
elif [ -f pyproject.toml ] && command -v pytest >/dev/null; then
  COMPROBAR="pytest -q"
else
  exit 0
fi

if SALIDA="$($COMPROBAR 2>&1)"; then
  exit 0
else
  python3 -c '
import json, sys
print(json.dumps({
  "decision": "block",
  "reason": "La bateria de pruebas falla. No des el turno por terminado:\n" + sys.stdin.read()[-1500:]
}, ensure_ascii=False))' <<< "$SALIDA"
  exit 0
fi
