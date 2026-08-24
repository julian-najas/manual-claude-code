#!/usr/bin/env bash
# veto-secretos.sh · PreToolUse · matcher Read|Edit|Write
#
# Veta que cualquier herramienta de archivo toque una ruta protegida.
# Acompana, NO sustituye, a una regla deny de permisos: un archivo metido en el
# prompt con @ no pasa por ninguna herramienta y este hook no lo ve.
#
# Ajusta RUTAS_VETADAS a tu proyecto. Se comparan sobre la ruta ABSOLUTA, que
# es la que llega siempre: Claude Code expande ~ y las rutas relativas antes.
set -uo pipefail

ENTRADA="$(cat)"
RUTA="$(printf '%s' "$ENTRADA" | jq -r '.tool_input.file_path // empty')"
RUTA="${RUTA//\\//}"   # Windows llega con barras invertidas

case "$RUTA" in
  */secretos/*|*/.ssh/*|*.env|*.env.*|*.pem|*.key)
    jq -n --arg r "$RUTA" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: ("Bloqueado por el hook veto-secretos: " + $r +
          " es una ruta protegida de este repositorio.")
      }
    }'
    ;;
  *)
    exit 0
    ;;
esac
