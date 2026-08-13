#!/usr/bin/env bash
# Publica el companion en el repositorio público.
#
#   ./fabrica/publicar-companion.sh
#
# Separación deliberada: **la fuente es privada, el build es público**. Este
# script regenera el sitio desde los módulos canónicos y lo empuja a un
# repositorio distinto, así que el repositorio del manual nunca se hace público
# por accidente.
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PUBLICO="https://github.com/julian-najas/claude-code-companion.git"
TRABAJO="${TMPDIR:-/tmp}/companion-publicacion"

echo "1. Regenerando desde los módulos canónicos"
python3 "$RAIZ/fabrica/generar-companion.py"

N=$(find "$RAIZ/companion" -name index.html | wc -l)
if [ "$N" -lt 100 ]; then
  echo "Solo $N páginas. Algo ha ido mal, no publico." >&2
  exit 1
fi

echo "2. Preparando el clon público"
rm -rf "$TRABAJO"
git clone -q "$PUBLICO" "$TRABAJO" 2>/dev/null || {
  mkdir -p "$TRABAJO" && git -C "$TRABAJO" init -q && \
  git -C "$TRABAJO" remote add origin "$PUBLICO"
}

# se borra todo menos .git: las páginas retiradas deben desaparecer
find "$TRABAJO" -mindepth 1 -maxdepth 1 -not -name .git -exec rm -rf {} +
cp -r "$RAIZ/companion/." "$TRABAJO/"

echo "3. Publicando"
git -C "$TRABAJO" add -A
if git -C "$TRABAJO" diff --cached --quiet; then
  echo "   Sin cambios."
  exit 0
fi
git -C "$TRABAJO" -c user.name="fabrica" -c user.email="fabrica@cosasagenticas.com" \
  commit -q -m "companion: $N páginas de síntoma regeneradas desde los módulos"
git -C "$TRABAJO" branch -M main
git -C "$TRABAJO" push -q -u origin main

echo "   Publicadas $N páginas en $PUBLICO"
echo "   https://julian-najas.github.io/claude-code-companion/"
