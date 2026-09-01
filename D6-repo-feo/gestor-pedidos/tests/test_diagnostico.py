# -*- coding: utf-8 -*-
"""
Pruebas del registro. Módulo 11 del manual.

Las de test_caracterizacion.py fijan lo que la aplicación HACE. Estas dos fijan
que, cuando algo falla, **queda escrito**. Es la diferencia entre una prueba de
comportamiento y una prueba de diagnóstico, y hace falta una de cada.

La segunda es la que importa: pasa hoy, y volvería a fallar el día que alguien
reponga un `except:` desnudo o cambie el `log.exception()` por un `log.error()`
sin traza. Una red contra la reincidencia, no contra el fallo original.
"""

import logging
import sqlite3
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import app as aplicacion  # noqa: E402


@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    """Base de datos nueva por prueba, fuera del repositorio."""
    bd = tmp_path / "pedidos.db"
    con = sqlite3.connect(bd)
    con.execute(
        "CREATE TABLE pedidos (id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "cliente TEXT, total REAL, estado TEXT)"
    )
    con.execute("CREATE TABLE clientes (nombre TEXT, alta TEXT)")
    con.commit()
    con.close()
    monkeypatch.setattr(aplicacion, "DB", str(bd))
    return aplicacion.app.test_client()


PEDIDO = {
    "cliente": "Beltran",
    "pais": "ES",
    "email": "pedidos@carnicas.local",
    "lineas": [{"precio": 10, "cantidad": 2}],
}


def test_un_aviso_que_falla_no_tumba_el_pedido(cliente, monkeypatch):
    """La decisión de 2019 se conserva a propósito: el pedido sigue adelante."""

    def revienta(destino, pedido_id, total):
        raise ConnectionRefusedError("smtp.carnicas.local:25 rechaza la conexión")

    monkeypatch.setattr(aplicacion, "enviar_email", revienta)
    r = cliente.post("/procesar", json=PEDIDO)
    assert r.status_code == 200
    assert r.get_json()["id"] == 1


def test_un_aviso_que_falla_deja_traza_en_el_registro(cliente, monkeypatch, caplog):
    """Lo que el módulo 11 cambia: el fallo deja de ser invisible.

    Contra el `except:` desnudo original esta prueba fallaba en las tres
    comprobaciones: no había registro, no había nivel ERROR y no había traza.
    """

    def revienta(destino, pedido_id, total):
        raise ConnectionRefusedError("smtp.carnicas.local:25 rechaza la conexión")

    monkeypatch.setattr(aplicacion, "enviar_email", revienta)

    with caplog.at_level(logging.ERROR, logger="gestor-pedidos"):
        cliente.post("/procesar", json=PEDIDO)

    assert caplog.records, "el fallo del aviso no dejó ninguna entrada en el registro"
    entrada = caplog.records[-1]
    assert entrada.levelno == logging.ERROR
    # exc_info es lo que distingue log.exception() de log.error(): sin esto hay
    # una línea que dice que algo falló, pero no dice dónde ni por qué.
    assert entrada.exc_info is not None, "la entrada no lleva la traza"
    assert "ConnectionRefusedError" in caplog.text
