# -*- coding: utf-8 -*-
"""
Primeras pruebas de gestor-pedidos. Módulo 09 del manual.

NO son pruebas de lo que la aplicación DEBERÍA hacer. Son pruebas de lo que
hace HOY, escritas antes de tocar nada, para que el módulo 12 pueda cambiar el
comportamiento a propósito y enterarse si cambia algo más de paso.

Tres de ellas fijan un fallo del inventario. Llevan el número escrito y el
enunciado dice "hoy", no "debe": el día que el módulo 12 arregle el IVA, esta
prueba tiene que fallar. Que falle es el trabajo que hace.
"""

import sqlite3
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import app as aplicacion  # noqa: E402


@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    """Una base de datos nueva por prueba, fuera del repositorio."""
    bd = tmp_path / "pedidos.db"
    con = sqlite3.connect(bd)
    con.executescript((RAIZ / "datos" / "esquema.sql").read_text(encoding="utf-8"))
    con.execute("INSERT INTO clientes (nombre, alta) VALUES ('Panaderia Sol', '2017-03-14')")
    con.execute("INSERT INTO clientes (nombre, alta) VALUES ('Cash Aljarafe', '2023-02-17')")
    con.commit()
    con.close()

    monkeypatch.setattr(aplicacion, "DB", str(bd))
    aplicacion.app.config["TESTING"] = False
    return aplicacion.app.test_client()


def procesar(c, **campos):
    campos.setdefault("cliente", "Cash Aljarafe")
    campos.setdefault("lineas", [{"precio": 100, "cantidad": 1}])
    return c.post("/procesar", json=campos)


# --- IVA. Fallo 4 del inventario, arreglado en el módulo 12 ----------------
#
# Las dos que decían `test_hoy_a_francia...` y `test_hoy_sin_pais...` vivieron
# aquí desde el módulo 09 fijando el fallo. El 2-sep-2026 se pusieron rojas,
# que era su trabajo, y se sustituyeron por estas seis. No se editó su
# aserción: se borró la prueba y se escribió la del comportamiento decidido.
#
# Los cuatro números literales salen de config.IVA_POR_PAIS. Están escritos a
# mano a propósito: si alguien cambia un tipo, esta prueba se pone roja y dice
# cuánto cambia la factura. Una prueba que calcule el esperado leyendo la misma
# tabla que la aplicación no comprueba nada.

def test_iva_espanol(cliente):
    r = procesar(cliente, pais="ES")
    assert r.json["total"] == pytest.approx(121.0)


def test_iva_portugues(cliente):
    r = procesar(cliente, pais="PT")
    assert r.json["total"] == pytest.approx(123.0)


def test_iva_frances(cliente):
    r = procesar(cliente, pais="FR")
    assert r.json["total"] == pytest.approx(120.0)


def test_iva_italiano(cliente):
    r = procesar(cliente, pais="IT")
    assert r.json["total"] == pytest.approx(122.0)


def test_un_pais_sin_tipo_se_rechaza_y_lo_dice(cliente):
    """Lo contrario de lo que hacía antes: ni cobra ni calla."""
    r = procesar(cliente, pais="MA")
    assert r.status_code == 400
    assert r.json["error"] == "pais sin tipo de IVA"
    assert r.json["pais"] == "MA"


def test_un_pedido_sin_pais_ya_no_pasa_por_espanol(cliente):
    """"No sé de qué país es" dejó de ser un sinónimo de "es de España"."""
    r = procesar(cliente)
    assert r.status_code == 400
    assert r.json["pais"] is None


# --- Descuentos por cantidad ----------------------------------------------

def test_los_dos_descuentos_de_cantidad_se_acumulan_a_proposito(cliente):
    """El comentario del código decía que nadie lo sabía. Ya se sabe.

    150 x 1 EUR = 150, por 0,95 y por 0,90 son 128,25, y con el 21 % 155,1825.

    Se llamaba `test_hoy_...` hasta el 2-sep-2026, cuando dejó de ser un
    accidente heredado y pasó a ser una decisión escrita en config.py. Lo único
    que cambió es el nombre, y el nombre es la mitad del valor de la prueba:
    dice si lo que fija es lo que pasa o lo que queremos que pase.
    """
    r = procesar(cliente, pais="ES", lineas=[{"precio": 1, "cantidad": 150}])
    assert r.json["total"] == pytest.approx(155.1825)


def test_descuento_de_cliente_antiguo(cliente):
    """Alta anterior a 2020, un 3 % menos: 121 x 0,97."""
    r = procesar(cliente, cliente="Panaderia Sol", pais="ES")
    assert r.json["total"] == pytest.approx(117.37)


# --- Validación. El tope real es 50, no el 100 de settings.py -------------

def test_el_tope_de_lineas_es_cincuenta(cliente):
    r = procesar(cliente, lineas=[{"precio": 1, "cantidad": 1}] * 51)
    assert r.status_code == 400


# --- Fallo 2, la concatenación de SQL -------------------------------------

def test_hoy_un_apostrofo_en_el_nombre_tumba_la_busqueda(cliente):
    """Fallo 2. No es una fuga teórica: es un 500 con un cliente real."""
    r = cliente.get("/buscar?q=O'Brien")
    assert r.status_code == 500


# --- Un pedido que no existe ----------------------------------------------

def test_hoy_un_pedido_inexistente_responde_200_con_null(cliente):
    """Ni 404 ni error: HTTP 200 y un cuerpo `null`."""
    r = cliente.get("/pedido/99999")
    assert r.status_code == 200
    assert r.json is None
