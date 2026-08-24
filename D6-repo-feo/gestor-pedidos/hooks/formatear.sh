#!/usr/bin/env bash
# formatear.sh · PostToolUse · matcher Edit|Write
#
# Formatea el .py que se acaba de tocar. NUNCA bloquea: sale 0 pase lo que
# pase. Un hook de formato que rompe el turno cuando el formateador no esta
# instalado convierte una comodidad en una averia.
#
# PostToolUse corre DESPUES de que la herramienta haya hecho su trabajo, asi
# que esto no puede impedir nada: solo arregla lo que ya se escribio.
#
# Cuesta dinero, y esta medido en el modulo 05: con este hook puesto, la misma
# edicion de una linea paso de 2 llamadas a herramienta a 6, y de ~167.000 a
# ~260.000 tokens de entrada. El agente vuelve a mirar el archivo porque ya no
# es el que el escribio.
set -uo pipefail

ENTRADA="$(cat)"
RUTA="$(printf '%s' "$ENTRADA" | jq -r '.tool_input.file_path // empty')"
RUTA="${RUTA//\\//}"

case "$RUTA" in
  *.py) ;;
  *) exit 0 ;;
esac

[ -f "$RUTA" ] || exit 0

if ! command -v black >/dev/null 2>&1; then
  printf '{"systemMessage":"El hook de formato no encuentra black. Instalalo con pip install black o quita el hook de .claude/settings.json."}\n'
  exit 0
fi

black --quiet "$RUTA" >/dev/null 2>&1
exit 0
