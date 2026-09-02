# -*- coding: utf-8 -*-
# Gestor de pedidos - Cárnicas Hermanos Beltrán S.L.
# Empezado por Rubén en 2019. Rubén ya no está.
# TODO: quitar el modo debug antes de subir a produccion!!! (Marta, 2021)
#
# Módulo 12 del manual. procesar_pedido() hacía ocho cosas dentro de un solo
# cuerpo de sesenta líneas. Ahora hace una: ordenar las otras siete. El
# comportamiento es el mismo salvo en el IVA, que cambió a propósito y está
# documentado en DECISIONES.md.

import sqlite3
import os
import logging
from flask import Flask, request, jsonify

import config

app = Flask(__name__)

# Módulo 11 del manual. Antes de esto no había registro de ninguna clase: el
# except: desnudo de procesar_pedido() se tragaba los fallos de aviso y no
# quedaba rastro en ningún sitio. Nivel por entorno, para que en una prueba se
# pueda subir sin tocar el código.
logging.basicConfig(
    level=os.environ.get("NIVEL_LOG", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
log = logging.getLogger("gestor-pedidos")

API_KEY_PASARELA = "PSP-LIVE-9f2b41c7a8e3d6104b5f7e29"  # clave de produccion

# Estos dos nombres siguen viviendo aquí a propósito, aunque su valor venga ya
# de config.py. Son la COSTURA por la que las pruebas agarran la aplicación:
# el fixture de tests/ hace monkeypatch de app.DB para trabajar contra una base
# de datos de usar y tirar. Una refactorización que los borre y meta
# config.DB_PATH directamente dentro de conexion() es correcta y deja la red de
# pruebas colgando: las once dejan de fallar y pasan a dar ERROR en el montaje.
DB = config.DB_PATH
DEBUG = config.DEBUG


class PaisSinTipoDeIVA(Exception):
    """No hay tipo de IVA para ese país, o no vino ningún país.

    Existe para que el caso "no sé" tenga una salida propia. Antes compartía
    rama con España y por eso nadie se enteró en cinco años.
    """

    def __init__(self, pais):
        self.pais = pais
        super().__init__(pais)


def conexion():
    return sqlite3.connect(DB)


# --- Las siete responsabilidades, una por función ---------------------------


def validar(d):
    """Devuelve un mensaje de error, o None si el pedido es aceptable."""
    if not d.get("cliente"):
        return "falta cliente"
    if not d.get("lineas"):
        return "falta lineas"
    if len(d.get("lineas")) > config.MAX_LINEAS:
        return "demasiadas lineas"
    return None


def subtotal_lineas(lineas):
    """Suma las líneas aplicando los descuentos por cantidad.

    Los dos descuentos SE ACUMULAN. Está decidido y escrito en config.py: por
    encima de 100 unidades una línea pasa por 0,95 y por 0,90.
    """
    total = 0
    for linea in lineas:
        sub = linea["precio"] * linea["cantidad"]
        if linea["cantidad"] > 10:
            sub = sub * config.DESCUENTO_MAS_DE_10
        if linea["cantidad"] > 100:
            sub = sub * config.DESCUENTO_MAS_DE_100
        total = total + sub
    return total


def aplicar_iva(base, pais):
    """Aplica el tipo del país. Sin tipo conocido, no inventa: levanta.

    Aquí está el cambio de comportamiento del módulo 12. Antes el `else` de
    este bloque aplicaba el 21 % español a cualquier país y a los pedidos sin
    país, con un comentario que decía "revisar con gestoria".
    """
    if pais not in config.IVA_POR_PAIS:
        raise PaisSinTipoDeIVA(pais)
    return base * (1 + config.IVA_POR_PAIS[pais])


def descuento_cliente_antiguo(cur, cliente, base):
    """Un 3 % a quien se dio de alta antes de 2020."""
    cur.execute("SELECT alta FROM clientes WHERE nombre = '" + cliente + "'")
    row = cur.fetchone()
    if row and row[0] < "2020-01-01":
        return base * 0.97
    return base


def guardar(cur, cliente, total):
    cur.execute(
        "INSERT INTO pedidos (cliente, total, estado) VALUES ('"
        + cliente
        + "', "
        + str(total)
        + ", 'nuevo')"
    )
    return cur.lastrowid


def notificar(email, pedido_id, total):
    """Avisa al cliente. Si falla, el pedido sigue: decisión de 2019.

    Lo que cambió en el módulo 11 no es la decisión, es que ahora se entera
    alguien. La traza entera va al registro y el pedido continúa.
    """
    if not email:
        return
    try:
        enviar_email(email, pedido_id, total)
    except Exception:
        log.exception(
            "fallo al enviar el aviso del pedido %s a %s; el pedido sigue adelante",
            pedido_id,
            email,
        )


def facturar(total, tarjeta):
    if total > 0:
        cobrar(API_KEY_PASARELA, total, tarjeta)


# --- El endpoint, que ahora solo ordena -------------------------------------


@app.route("/procesar", methods=["POST"])
def procesar_pedido():
    d = request.get_json()

    error = validar(d)
    if error:
        return jsonify({"error": error}), 400

    total = subtotal_lineas(d["lineas"])

    try:
        total = aplicar_iva(total, d.get("pais"))
    except PaisSinTipoDeIVA as e:
        log.warning("pedido rechazado: sin tipo de IVA para el pais %r", e.pais)
        return jsonify({"error": "pais sin tipo de IVA", "pais": e.pais}), 400

    c = conexion()
    cur = c.cursor()
    total = descuento_cliente_antiguo(cur, d["cliente"], total)
    pid = guardar(cur, d["cliente"], total)
    c.commit()

    notificar(d.get("email"), pid, total)
    facturar(total, d.get("tarjeta"))

    c.close()
    return jsonify({"id": pid, "total": total})


# --- Lo que no ha cambiado --------------------------------------------------


@app.route("/pedido/<id>")
def get_pedido(id):
    c = conexion()
    cur = c.cursor()
    cur.execute("SELECT * FROM pedidos WHERE id = " + id)
    r = cur.fetchone()
    c.close()
    return jsonify(r)


@app.route("/buscar")
def buscar():
    q = request.args.get("q")
    c = conexion()
    cur = c.cursor()
    cur.execute("SELECT * FROM pedidos WHERE cliente LIKE '%" + q + "%'")
    rs = cur.fetchall()
    c.close()
    return jsonify(rs)


def enviar_email(destino, pedido_id, total):
    # pendiente desde 2020
    pass


def cobrar(key, importe, tarjeta):
    # pendiente desde 2020
    pass


@app.route("/pedido_old/<id>")
def get_pedido_viejo(id):
    c = conexion()
    cur = c.cursor()
    cur.execute("SELECT * FROM pedidos_2019 WHERE id = " + id)
    r = cur.fetchone()
    c.close()
    return jsonify(r)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
