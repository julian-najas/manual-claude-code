#!/usr/bin/env python3
"""
Servidor MCP de solo lectura sobre la base de datos de gestor-pedidos.

Sin dependencias. Habla JSON-RPC 2.0 por entrada y salida estándar, una línea
por mensaje, que es todo lo que exige el transporte stdio de MCP. Son doscientas
líneas y se leen enteras en cinco minutos, que es exactamente el punto: lo que
devuelve un servidor MCP entra en tu contexto como cualquier otro texto, así que
un servidor que no puedes leer es código de terceros ejecutándose con tu
confianza.

TRES CANDADOS, y ninguno se fía del anterior:

  1. La conexión se abre en modo `ro` por URI de SQLite. Es el sistema de
     archivos quien deniega la escritura, no este código.
  2. Solo se acepta una sentencia, y tiene que empezar por SELECT o WITH.
  3. `set_authorizer` de sqlite3 deniega cualquier operación que no sea leer.

El primero solo aguanta si el archivo existe: SQLite en modo `ro` falla si no
está, en vez de crearlo vacío, y eso también es a propósito.

NUNCA imprime nada por la salida estándar que no sea un mensaje JSON-RPC. Los
avisos van por la de error. Un `print` de depuración mal puesto rompe el
transporte entero, y es el fallo número uno de quien escribe su primer servidor.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
from pathlib import Path

PROTOCOLO = "2024-11-05"
NOMBRE = "pedidos-solo-lectura"
VERSION = "1.0.0"

# El proyecto puede arrancarse desde cualquier sitio. Claude Code pone
# CLAUDE_PROJECT_DIR en el entorno del servidor justo para esto.
RAIZ = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
BD = RAIZ / "datos" / "pedidos.db"

SOLO_LECTURA = re.compile(r"^\s*(select|with)\b", re.I)

INSTRUCCIONES = (
    "Base de datos de pedidos de gestor-pedidos, en SOLO LECTURA. "
    "Úsala para responder cualquier pregunta sobre pedidos, clientes o "
    "importes en vez de abrir archivos del repositorio: los datos no están en "
    "el código. No puede escribir, y rechaza cualquier sentencia que no sea "
    "una consulta."
)

HERRAMIENTAS = [
    {
        "name": "listar_tablas",
        "description": "Devuelve los nombres de las tablas de la base de datos de pedidos.",
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
            "Ejecuta una consulta SELECT contra la base de datos de pedidos y "
            "devuelve las filas. Solo lectura: cualquier otra sentencia se rechaza."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "Una sola sentencia SELECT o WITH"},
                "limite": {
                    "type": "integer",
                    "description": "Máximo de filas a devolver. Por defecto 100.",
                },
            },
            "required": ["sql"],
        },
    },
]


def autorizador(accion, *_resto):
    """Tercer candado. Todo lo que no sea leer, se deniega en el motor."""
    permitidas = {
        sqlite3.SQLITE_SELECT,
        sqlite3.SQLITE_READ,
        sqlite3.SQLITE_FUNCTION,
        sqlite3.SQLITE_RECURSIVE,
    }
    return sqlite3.SQLITE_OK if accion in permitidas else sqlite3.SQLITE_DENY


def conectar() -> sqlite3.Connection:
    if not BD.exists():
        raise RuntimeError(
            f"No existe {BD}. Créala con: "
            f"sqlite3 datos/pedidos.db < datos/esquema.sql"
        )
    # Primer candado: el sistema de archivos. `mode=ro` no crea el archivo si
    # falta y no deja escribir aunque el proceso tenga permisos de sobra.
    con = sqlite3.connect(f"file:{BD}?mode=ro", uri=True)
    con.set_authorizer(autorizador)
    return con


def texto(cadena: str) -> dict:
    return {"content": [{"type": "text", "text": cadena}]}


def error(cadena: str) -> dict:
    return {"content": [{"type": "text", "text": cadena}], "isError": True}


def listar_tablas() -> dict:
    with conectar() as con:
        filas = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    return texto("\n".join(f[0] for f in filas) or "(sin tablas)")


def describir_tabla(args: dict) -> dict:
    tabla = str(args.get("tabla", ""))
    # Un nombre de tabla no puede ir como parámetro en PRAGMA, así que se
    # valida en vez de interpolarse a lo bruto. El repo feo ya tiene tres
    # concatenaciones de SQL; aquí no se añade una cuarta.
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", tabla):
        return error(f"Nombre de tabla no válido: {tabla!r}")
    with conectar() as con:
        existe = con.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (tabla,)
        ).fetchone()
        if not existe:
            return error(f"No existe la tabla {tabla}.")
        cols = con.execute(f"PRAGMA table_info({tabla})").fetchall()
    return texto("\n".join(f"{c[1]} {c[2] or 'SIN TIPO'}" for c in cols))


def consultar(args: dict) -> dict:
    sql = str(args.get("sql", "")).strip()
    limite = int(args.get("limite", 100))

    # Segundo candado. Una sola sentencia: un `;` en medio es el camino
    # clásico para colar un UPDATE detrás de un SELECT.
    if sql.endswith(";"):
        sql = sql[:-1].strip()
    if ";" in sql:
        return error("Solo se admite una sentencia. Quita el punto y coma.")
    if not SOLO_LECTURA.match(sql):
        return error("Solo se admiten consultas SELECT o WITH. Esta base de datos es de solo lectura.")

    try:
        with conectar() as con:
            cur = con.execute(sql)
            columnas = [d[0] for d in cur.description] if cur.description else []
            filas = cur.fetchmany(max(1, min(limite, 1000)))
    except sqlite3.DatabaseError as e:
        # El autorizador levanta DatabaseError, y así es como se ve el tercer
        # candado desde fuera.
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


def responder(mensaje: dict) -> dict | None:
    metodo = mensaje.get("method")
    ident = mensaje.get("id")

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
        params = mensaje.get("params") or {}
        resultado = llamar(params.get("name", ""), params.get("arguments") or {})
        return {"jsonrpc": "2.0", "id": ident, "result": resultado}
    # Las notificaciones no llevan id y no se contestan.
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
