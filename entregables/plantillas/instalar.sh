#!/usr/bin/env bash
# Instala estas plantillas en un proyecto.
#
#   ./instalar.sh /ruta/al/proyecto [conservador|autonomo]
#
# Copia hooks, skills y subagentes a <proyecto>/.claude/ y deja el settings.json
# del perfil elegido. No sobrescribe nada: lo que ya existe se respeta y se avisa.
set -euo pipefail

ORIGEN="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESTINO="${1:-}"
PERFIL="${2:-conservador}"

if [ -z "$DESTINO" ]; then
  echo "Uso: $0 /ruta/al/proyecto [conservador|autonomo]" >&2
  exit 1
fi
if [ ! -d "$DESTINO" ]; then
  echo "No existe el directorio: $DESTINO" >&2
  exit 1
fi
case "$PERFIL" in
  conservador|autonomo) ;;
  *) echo "Perfil desconocido: $PERFIL. Usa conservador o autonomo." >&2; exit 1 ;;
esac

C="$DESTINO/.claude"
mkdir -p "$C/hooks" "$C/skills" "$C/agents"

copiar() {
  if [ -e "$2" ]; then
    echo "  ya existe, no lo toco: ${2#"$DESTINO"/}"
  else
    cp -r "$1" "$2"
    echo "  copiado: ${2#"$DESTINO"/}"
  fi
}

echo "Instalando en $DESTINO (perfil: $PERFIL)"

for f in "$ORIGEN"/hooks/*.sh; do copiar "$f" "$C/hooks/$(basename "$f")"; done
chmod +x "$C"/hooks/*.sh
copiar "$ORIGEN/hooks/reglas-permanentes.md" "$C/reglas-permanentes.md"

for d in "$ORIGEN"/skills/*/; do copiar "$d" "$C/skills/$(basename "$d")"; done
for f in "$ORIGEN"/agents/*.md; do copiar "$f" "$C/agents/$(basename "$f")"; done

if [ -e "$C/settings.json" ]; then
  echo "  ya existe .claude/settings.json: lo dejo intacto."
  echo "  Fusiona a mano lo de settings.$PERFIL.json y hooks/hooks.json."
else
  python3 - "$ORIGEN/settings.$PERFIL.json" "$ORIGEN/hooks/hooks.json" "$C/settings.json" <<'PY'
import json, sys
perfil, hooks, salida = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(perfil))
d.update(json.load(open(hooks)))
json.dump(d, open(salida, "w"), ensure_ascii=False, indent=2)
PY
  echo "  creado: .claude/settings.json (perfil $PERFIL + hooks)"
fi

echo
echo "Listo. Comprueba con:  cd $DESTINO && claude doctor"
echo
echo "Dos avisos:"
echo " 1. Acepta la confianza del espacio de trabajo. Sin ella no se aplican los"
echo "    hooks ni las reglas allow del proyecto. Las deny y ask sí se aplican."
echo " 2. Ajusta el comando de la puerta de calidad en hooks/puerta-calidad.sh"
echo "    a como se prueba TU proyecto. Si no hay nada que comprobar, no hay puerta."
