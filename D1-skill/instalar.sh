#!/usr/bin/env bash
# Instala el manual como skill de Claude Code.
#
#   ./instalar.sh              -> para tu usuario  (~/.claude/skills)
#   ./instalar.sh --proyecto   -> solo este repo   (./.claude/skills)
#
# Después, dentro de Claude Code:  /manual-claude-code
set -euo pipefail

ORIGEN="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/manual-claude-code"
DESTINO="$HOME/.claude/skills"
AMBITO="tu usuario"

if [[ "${1:-}" == "--proyecto" ]]; then
  DESTINO="$PWD/.claude/skills"
  AMBITO="este proyecto"
fi

if [[ ! -f "$ORIGEN/SKILL.md" ]]; then
  echo "No encuentro SKILL.md en $ORIGEN" >&2
  exit 1
fi

mkdir -p "$DESTINO"
if [[ -e "$DESTINO/manual-claude-code" ]]; then
  echo "Ya existe $DESTINO/manual-claude-code"
  read -r -p "¿Lo sobrescribo? [s/N] " r
  [[ "$r" == "s" || "$r" == "S" ]] || { echo "Cancelado."; exit 0; }
  rm -rf "$DESTINO/manual-claude-code"
fi

cp -r "$ORIGEN" "$DESTINO/"
echo "Instalado para $AMBITO en $DESTINO/manual-claude-code"
echo "Abre Claude Code y escribe: /manual-claude-code"
