#!/usr/bin/env bash
# veto-credenciales.sh · PreToolUse · matcher Write|Edit
#
# El unico hook de esta biblioteca que mira el CONTENIDO en vez de la ruta.
# Es lo que cubre el hueco que una regla de permisos no puede cubrir: una
# credencial escrita en un archivo nuevo, en una carpeta que nadie preveia.
#
# Va a dar falsos positivos, y esa es la contrapartida de mirar contenido.
# Cuando uno moleste, se acota PATRON y se anota por que. No se quita el hook.
set -uo pipefail

ENTRADA="$(cat)"
TEXTO="$(printf '%s' "$ENTRADA" | jq -r '[.tool_input.content, .tool_input.new_string] | map(select(. != null)) | join("\n")')"
RUTA="$(printf '%s' "$ENTRADA" | jq -r '.tool_input.file_path // "(sin ruta)"')"

PATRON='BEGIN [A-Z ]*PRIVATE KEY|(api[_-]?key|secret|password|passwd|token)[[:space:]]*[:=][[:space:]]*["'\'']?[A-Za-z0-9_\-]{16,}'

if printf '%s' "$TEXTO" | grep -Eiq "$PATRON"; then
  jq -n --arg f "$RUTA" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: ("Bloqueado por el hook veto-credenciales: lo que ibas a escribir en " + $f +
        " contiene algo con forma de credencial. Sacala del codigo y leela del entorno.")
    }
  }'
else
  exit 0
fi
