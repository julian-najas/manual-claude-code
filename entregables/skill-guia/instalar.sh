#!/usr/bin/env bash
# Instala la Guía Definitiva de Claude Code como skill.
#
#   ./instalar.sh              -> para tu usuario  (~/.claude/skills)
#   ./instalar.sh --proyecto   -> solo este repo   (./.claude/skills)
#
# Después, dentro de Claude Code:  /guia-claude-code
# O simplemente pregunta y la skill se activa sola cuando la duda es sobre
# el propio Claude Code.
set -euo pipefail

ORIGEN="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/guia-claude-code"
DESTINO="$HOME/.claude/skills"
AMBITO="tu usuario"

if [ "${1:-}" = "--proyecto" ]; then
  DESTINO="$PWD/.claude/skills"
  AMBITO="este proyecto"
fi

if [ ! -f "$ORIGEN/SKILL.md" ]; then
  echo "No encuentro SKILL.md en $ORIGEN" >&2
  exit 1
fi

N=$(ls "$ORIGEN"/modulos/M*.md 2>/dev/null | wc -l)
if [ "$N" -ne 21 ]; then
  echo "Esperaba 21 módulos en modulos/ y encuentro $N. No instalo a medias." >&2
  exit 1
fi

mkdir -p "$DESTINO"
if [ -e "$DESTINO/guia-claude-code" ]; then
  echo "Ya existe $DESTINO/guia-claude-code"
  read -r -p "¿Lo sobrescribo? [s/N] " r
  case "$r" in
    s|S) rm -rf "${DESTINO:?}/guia-claude-code" ;;
    *) echo "Cancelado."; exit 0 ;;
  esac
fi

cp -r "$ORIGEN" "$DESTINO/"
echo "Instalada para $AMBITO en $DESTINO/guia-claude-code"
# grep '^| ' cuenta la cabecera y las filas; la línea separadora empieza por "|-"
# y no entra. De ahí el -1.
echo "  21 módulos · $(( $(grep -c '^| ' "$ORIGEN/INDICE-SINTOMAS.md") - 1 )) entradas en el índice por síntoma"
echo
echo "Pruébala:  /guia-claude-code"
echo "O pregunta sin más: \"por qué mi skill no se activa sola\""
