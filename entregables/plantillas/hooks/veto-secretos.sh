#!/usr/bin/env bash
# Veta la lectura de secretos. Cinturón sobre el tirante de permissions.deny.
# Contrato: recibe el JSON del evento por stdin. Código de salida 2 = bloquea.
set -euo pipefail

ENTRADA="$(cat)"
RUTA="$(printf '%s' "$ENTRADA" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null || true)"

# Las rutas llegan SIEMPRE absolutas: Claude Code expande ~ y las relativas antes
# de ejecutar el hook, así que no se puede esquivar escribiéndolas de otra forma.
# En Windows llegan con barras invertidas, de ahí la normalización.
RUTA="${RUTA//\\//}"

case "$RUTA" in
  */.env|*/.env.*|*/secrets/*|*/id_rsa|*/id_ed25519|*/.aws/credentials|*/.npmrc)
    echo "Bloqueado por politica del repositorio: $RUTA contiene credenciales." >&2
    exit 2 ;;
esac
exit 0
