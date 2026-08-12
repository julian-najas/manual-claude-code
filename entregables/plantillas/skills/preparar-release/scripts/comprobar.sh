#!/usr/bin/env bash
# Script de apoyo de la skill preparar-release.
# Imprime un informe corto y determinista que se inyecta en el prompt.
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0

r(){ printf '%-34s %s\n' "$1" "$2"; }

# 1. árbol limpio
if [ -z "$(git status --porcelain 2>/dev/null)" ]; then r "arbol limpio" "OK"; else r "arbol limpio" "FALLA: hay cambios sin confirmar"; fi

# 2. pruebas
if [ -f package.json ] && command -v npm >/dev/null; then
  if npm test --silent >/dev/null 2>&1; then r "pruebas" "OK"; else r "pruebas" "FALLA"; fi
elif [ -f pyproject.toml ] && command -v pytest >/dev/null; then
  if pytest -q >/dev/null 2>&1; then r "pruebas" "OK"; else r "pruebas" "FALLA"; fi
else
  r "pruebas" "AVISO: no encuentro como probar este proyecto"
fi

# 3. secretos en el diff desde el ultimo tag
BASE="$(git describe --tags --abbrev=0 2>/dev/null || echo HEAD)"
if git diff "$BASE"..HEAD 2>/dev/null | grep -qE '(sk_live_|BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16})'; then
  r "secretos en el diff" "FALLA: hay algo que parece una credencial"
else
  r "secretos en el diff" "OK"
fi

# 4. changelog
if [ -f CHANGELOG.md ]; then
  if [ -n "$(git diff "$BASE"..HEAD --name-only 2>/dev/null | grep -x 'CHANGELOG.md')" ]; then
    r "changelog" "OK"
  else
    r "changelog" "AVISO: CHANGELOG.md no se ha tocado desde $BASE"
  fi
else
  r "changelog" "AVISO: no hay CHANGELOG.md"
fi
