#!/usr/bin/env bash
# veto-rm.sh · PreToolUse · matcher Bash · if Bash(rm *)
#
# El campo `if` del manejador ya filtra por Bash(rm *). Esto es el segundo
# cinturon: comprueba la cadena de verdad, porque el filtro `if` FALLA ABIERTO
# cuando no puede analizar el comando, y porque un `rm` puede venir dentro de
# un $(...) o detras de un &&.
set -uo pipefail

ENTRADA="$(cat)"
COMANDO="$(printf '%s' "$ENTRADA" | jq -r '.tool_input.command // empty')"

if printf '%s' "$COMANDO" | grep -Eq '(^|[;&|]|\$\()[[:space:]]*rm[[:space:]]+(-[a-zA-Z]*[rf]|--recursive|--force)'; then
  jq -n --arg c "$COMANDO" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "ask",
      permissionDecisionReason: ("Borrado recursivo o forzado detectado: " + $c +
        ". Confirma tu, esto no se auto-aprueba en este repositorio.")
    }
  }'
else
  exit 0
fi
