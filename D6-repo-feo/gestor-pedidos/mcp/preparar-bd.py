#!/usr/bin/env python3
"""
Construye datos/pedidos.db desde datos/esquema.sql y le mete filas de muestra.

La base de datos está en `.gitignore` desde el módulo 04, así que NO viene en el
clon: se construye. Esto es el paso 1 del laboratorio del módulo 06, y también
lo que deja al verificador comprobar el servidor MCP desde un clon limpio.

Es determinista a propósito: siempre catorce pedidos y cinco clientes, para que
la prueba pueda afirmar un número. Rehace la base cada vez.

Los datos son inventados, pero no inocentes: `O'Brien Foods` lleva un apóstrofo
porque el `app.py` del laboratorio concatena SQL a mano y se cae con él. Ese
fallo se caza en el módulo 10; aquí solo se deja plantado.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

RAIZ = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
BD = RAIZ / "datos" / "pedidos.db"
ESQUEMA = RAIZ / "datos" / "esquema.sql"

CLIENTES = [
    ("Panadería Sol", "2017-03-14"),
    ("O'Brien Foods", "2019-11-02"),
    ("Mercado Central", "2021-06-30"),
    ("Hostelería Nervión", "2015-01-09"),
    ("Cash Aljarafe", "2023-02-17"),
]

PEDIDOS = [
    ("Panadería Sol", 1210.5, "servido"),
    ("O'Brien Foods", 484.0, "pendiente"),
    ("Mercado Central", 2662.75, "servido"),
    ("Hostelería Nervión", 96.8, "anulado"),
    ("Cash Aljarafe", 5324.0, "servido"),
    ("Panadería Sol", 363.0, "pendiente"),
    ("Mercado Central", 1815.25, "servido"),
    ("Cash Aljarafe", 242.0, "pendiente"),
    ("Hostelería Nervión", 7986.0, "servido"),
    ("O'Brien Foods", 1089.0, "servido"),
    ("Panadería Sol", 605.0, "servido"),
    ("Mercado Central", 121.0, "anulado"),
    ("Cash Aljarafe", 3025.0, "servido"),
    ("Hostelería Nervión", 847.0, "pendiente"),
]

ANTIGUOS = [(1, "Ultramarinos Rota", 300.0), (2, "Panadería Sol", 150.0)]


def main() -> int:
    if not ESQUEMA.exists():
        print(f"No existe {ESQUEMA}.")
        return 1
    BD.parent.mkdir(parents=True, exist_ok=True)
    if BD.exists():
        BD.unlink()
    con = sqlite3.connect(BD)
    con.executescript(ESQUEMA.read_text(encoding="utf-8"))
    con.executemany("INSERT INTO clientes (nombre, alta) VALUES (?, ?)", CLIENTES)
    con.executemany("INSERT INTO pedidos (cliente, total, estado) VALUES (?, ?, ?)", PEDIDOS)
    con.executemany("INSERT INTO pedidos_2019 (id, cliente, total) VALUES (?, ?, ?)", ANTIGUOS)
    con.commit()
    con.close()
    print(f"{BD} lista: {len(PEDIDOS)} pedidos, {len(CLIENTES)} clientes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
