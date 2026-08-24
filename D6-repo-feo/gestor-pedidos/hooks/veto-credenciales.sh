#!/usr/bin/env bash
# veto-credenciales.sh · PreToolUse · matcher Write|Edit
#
# Mira el CONTENIDO que se va a escribir, no la ruta. Es lo unico de este
# repositorio que puede parar una credencial escrita en un archivo nuevo, en
# una carpeta que nadie habia previsto. Una regla de permisos protege rutas
# conocidas; esto protege valores.
#
# Medido el 24-ago-2026 con la 2.1.241: misma peticion siete veces, escribir
# config/produccion.yaml con una clave dentro. Sin este hook el archivo se
# escribio 5 de 7 veces. Con el, 0 de 7.
#
# Falsos positivos: los habra. Es la contrapartida de mirar contenido. Cuando
# uno moleste, se acota el patron, no se quita el hook.
set -uo pipefail

ENTRADA="$(cat)"
TEXTO="$(printf '%s' "$ENTRADA" | jq -r '[.tool_input.content, .tool_input.new_string] | map(select(. != null)) | join("\n")')"
RUTA="$(printf '%s' "$ENTRADA" | jq -r '.tool_input.file_path // "(sin ruta)"')"

PATRON='PSP-LIVE-|BEGIN [A-Z ]*PRIVATE KEY|(api[_-]?key|secret|password|passwd|token)[[:space:]]*[:=][[:space:]]*["'\'']?[A-Za-z0-9_\-]{16,}'

if printf '%s' "$TEXTO" | grep -Eiq "$PATRON"; then
  jq -n --arg f "$RUTA" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: ("Bloqueado por el hook veto-credenciales: lo que ibas a escribir en " + $f +
        " contiene algo con forma de credencial. En gestor-pedidos los secretos van en secretos/, que esta fuera de git, y el codigo los lee del entorno. Si es un falso positivo, acota el patron en hooks/veto-credenciales.sh y di por que en HOOKS.md.")
    }
  }'
else
  exit 0
fi
