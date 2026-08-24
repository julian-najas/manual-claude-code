#!/usr/bin/env bash
# veto-secretos.sh · PreToolUse · matcher Read|Edit|Write
#
# Veta cualquier lectura o escritura sobre secretos/ y sobre archivos .env,
# venga de la herramienta que venga. Es el cinturon que acompana al tirante:
# la regla deny del modulo 04 cubre las referencias con @, que este hook NO ve,
# y este hook explica el bloqueo con palabras nuestras, que la regla no hace.
#
# Lo que este hook NO cubre, y esta medido en el modulo 05:
#   - Las referencias con @ en el prompt. No hay llamada a herramienta, asi que
#     PreToolUse no dispara. Para eso esta la regla deny de permisos.
#
# Sale 0 sin imprimir nada cuando no hay nada que vetar: es lo que deja pasar
# el flujo normal de permisos.
set -uo pipefail

ENTRADA="$(cat)"
RUTA="$(printf '%s' "$ENTRADA" | jq -r '.tool_input.file_path // empty')"
RUTA="${RUTA//\\//}"

case "$RUTA" in
  */secretos/*|*.env|*.env.*)
    jq -n --arg r "$RUTA" '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: ("Bloqueado por el hook veto-secretos: " + $r +
          " esta fuera de lo que este repositorio deja leer o escribir. Los secretos de gestor-pedidos viven en secretos/, fuera de git, y el codigo los lee del entorno. Si necesitas el valor, pidelo a quien lleve la pasarela.")
      }
    }'
    ;;
  *)
    exit 0
    ;;
esac
