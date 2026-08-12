#!/usr/bin/env bash
# Auditoria. Va en async:true, asi que SOLO OBSERVA: sus campos de decision
# no tienen efecto porque la accion ya ocurrio.
set -uo pipefail

REG="${CLAUDE_PROJECT_DIR:-.}/.claude/auditoria.jsonl"
mkdir -p "$(dirname "$REG")"
cat | python3 -c '
import sys, json, datetime
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
print(json.dumps({
    "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "evento": d.get("hook_event_name"),
    "herramienta": d.get("tool_name"),
    "sesion": d.get("session_id"),
    "ruta": d.get("tool_input", {}).get("file_path"),
    "comando": (d.get("tool_input", {}).get("command") or "")[:200],
}, ensure_ascii=False))' >> "$REG" 2>/dev/null
exit 0
