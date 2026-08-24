#!/usr/bin/env python3
"""
Servidor MCP de solo lectura sobre SQLite. Plantilla del manual.

Sin dependencias: habla JSON-RPC 2.0 por entrada y salida estándar, una línea
por mensaje, que es todo lo que exige el transporte stdio de MCP. Se lee entero
en cinco minutos, y ese es el punto: lo que devuelve un servidor MCP entra en tu
contexto como cualquier otro texto, así que un servidor que no puedes auditar es
código de terceros ejecutándose con tu confianza.

Configuración, por entorno:
    BD_RUTA   ruta al fichero .sqlite, relativa a CLAUDE_PROJECT_DIR o absoluta
    BD_NOMBRE nombre con el que se anuncia el servidor (opcional)

Declaración en `.mcp.json`, con el valor por defecto que hace falta ahí dentro:

    {
      "mcpServers": {
        "datos": {
          "type": "stdio",
          "command": "python3",
          "args": ["${CLAUDE_PROJECT_DIR:-.}/mcp/servidor-solo-lectura.py"],
          "env": { "BD_RUTA": "datos/app.db" }
        }
      }
    }

TRES CANDADOS, y ninguno se fía del anterior:
  1. Conexión en modo `ro` por URI: deniega el sistema de archivos, no este
     código. En `ro` tampoco crea el fichero si falta.
  2. Una sola sentencia, y que empiece por SELECT o WITH.
  3. `set_authorizer` denegando toda operación que no sea leer.

NUNCA imprimas por la salida estándar nada que no sea JSON-RPC. Los avisos van
por la de error. Un `print` de depuración rompe el transporte entero.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
from pathlib import Path

PROTOCOLO = "2024-11-05"
NOMBRE = os.environ.get("BD_NOMBRE", "datos-solo-lectura")
VERSION = "1.0.0"

RAIZ = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
BD = Path(os.environ.get("BD_RUTA", "datos/app.db"))
if not BD.is_absolute():
    BD = RAIZ / BD

SOLO_LECTURA = re.compile(r"^\s*(select|with)\b", re.I)
NOMBRE_VALIDO = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

INSTRUCCIONES = (
    "Base de datos en SOLO LECTURA. Úsala para responder preguntas sobre los "
    "datos en vez de abrir archivos del repositorio. No puede escribir."
)

HERRAMIENTAS = [
    {
        "name": "listar_tablas",
        "description": "Devuelve los nombres de las tablas de la base de datos.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "describir_tabla",
        "description": "Devuelve las columnas y sus tipos para una tabla concreta.",
        "inputSchema": {
            "type": "object",
            "properties": {"tabla": {"type": "string", "description": "Nombre de la tabla"}},
            "required": ["tabla"],
        },
    },
    {
        "name": "consultar",
        "description": (
            "Ejecuta una consulta SELECT y devuelve las filas. Solo lectura: "
            "cualquier otra sentencia se rechaza."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "Una sola sentencia SELECT o WITH"},
                "limite": {"type": "integer", "description": "Máximo de filas. Por defecto 100."},
            },
            "required": ["sql"],
        },
    },
]


def autorizador(accion, *_resto):
    permitidas = {
        sqlite3.SQLITE_SELECT,
        sqlite3.SQLITE_READ,
        sqlite3.SQLITE_FUNCTION,
        sqlite3.SQLITE_RECURSIVE,
    }
    return sqlite3.SQLITE_OK if accion in permitidas else sqlite3.SQLITE_DENY


def conectar() -> sqlite3.Connection:
    if not BD.exists():
        raise RuntimeError(f"No existe {BD}. Revisa BD_RUTA.")
    con = sqlite3.connect(f"file:{BD}?mode=ro", uri=True)
    con.set_authorizer(autorizador)
    return con


def texto(c: str) -> dict:
    return {"content": [{"type": "text", "text": c}]}


def error(c: str) -> dict:
    return {"content": [{"type": "text", "text": c}], "isError": True}


def listar_tablas() -> dict:
    with conectar() as con:
        filas = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    return texto("\n".join(f[0] for f in filas) or "(sin tablas)")


def describir_tabla(args: dict) -> dict:
    tabla = str(args.get("tabla", ""))
    # Un nombre de tabla no puede ir como parámetro en PRAGMA, así que se valida
    # en vez de interpolarse a lo bruto.
    if not NOMBRE_VALIDO.fullmatch(tabla):
        return error(f"Nombre de tabla no válido: {tabla!r}")
    with conectar() as con:
        if not con.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (tabla,)
        ).fetchone():
            return error(f"No existe la tabla {tabla}.")
        cols = con.execute(f"PRAGMA table_info({tabla})").fetchall()
    return texto("\n".join(f"{c[1]} {c[2] or 'SIN TIPO'}" for c in cols))


def consultar(args: dict) -> dict:
    sql = str(args.get("sql", "")).strip()
    limite = int(args.get("limite", 100))
    if sql.endswith(";"):
        sql = sql[:-1].strip()
    if ";" in sql:
        return error("Solo se admite una sentencia. Quita el punto y coma.")
    if not SOLO_LECTURA.match(sql):
        return error("Solo se admiten consultas SELECT o WITH. Esta base es de solo lectura.")
    try:
        with conectar() as con:
            cur = con.execute(sql)
            columnas = [d[0] for d in cur.description] if cur.description else []
            filas = cur.fetchmany(max(1, min(limite, 1000)))
    except sqlite3.DatabaseError as e:
        return error(f"La base de datos rechazó la consulta: {e}")
    except RuntimeError as e:
        return error(str(e))
    if not filas:
        return texto("(cero filas)")
    salida = [" | ".join(columnas)]
    salida += [" | ".join("" if v is None else str(v) for v in f) for f in filas]
    return texto("\n".join(salida))


def llamar(nombre: str, args: dict) -> dict:
    try:
        if nombre == "listar_tablas":
            return listar_tablas()
        if nombre == "describir_tabla":
            return describir_tabla(args)
        if nombre == "consultar":
            return consultar(args)
    except RuntimeError as e:
        return error(str(e))
    except sqlite3.DatabaseError as e:
        return error(f"La base de datos rechazó la operación: {e}")
    return error(f"Herramienta desconocida: {nombre}")


def responder(m: dict) -> dict | None:
    metodo, ident = m.get("method"), m.get("id")
    if metodo == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": ident,
            "result": {
                "protocolVersion": PROTOCOLO,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": NOMBRE, "version": VERSION},
                "instructions": INSTRUCCIONES,
            },
        }
    if metodo == "tools/list":
        return {"jsonrpc": "2.0", "id": ident, "result": {"tools": HERRAMIENTAS}}
    if metodo == "tools/call":
        params = m.get("params") or {}
        return {
            "jsonrpc": "2.0",
            "id": ident,
            "result": llamar(params.get("name", ""), params.get("arguments") or {}),
        }
    if ident is None:
        return None
    return {
        "jsonrpc": "2.0",
        "id": ident,
        "error": {"code": -32601, "message": f"Método no implementado: {metodo}"},
    }


def main() -> int:
    for linea in sys.stdin:
        linea = linea.strip()
        if not linea:
            continue
        try:
            mensaje = json.loads(linea)
        except json.JSONDecodeError:
            continue
        respuesta = responder(mensaje)
        if respuesta is not None:
            sys.stdout.write(json.dumps(respuesta, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
