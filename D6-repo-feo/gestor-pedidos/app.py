# -*- coding: utf-8 -*-
# Gestor de pedidos - Cárnicas Hermanos Beltrán S.L.
# Empezado por Rubén en 2019. Rubén ya no está.
# TODO: separar esto en módulos (Marta, 2021)
# TODO: quitar el modo debug antes de subir a produccion!!! (Marta, 2021)
#

import sqlite3
import os
import logging
from flask import Flask, request, jsonify

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
DB = "datos/pedidos.db"
DEBUG = True


def conexion():
    return sqlite3.connect(DB)


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


@app.route("/procesar", methods=["POST"])
def procesar_pedido():
    d = request.get_json()
    c = conexion()
    cur = c.cursor()

    # validar
    if not d.get("cliente"):
        return jsonify({"error": "falta cliente"}), 400
    if not d.get("lineas"):
        return jsonify({"error": "falta lineas"}), 400
    if len(d.get("lineas")) > 50:
        return jsonify({"error": "demasiadas lineas"}), 400

    # calcular
    total = 0
    for l in d["lineas"]:
        p = l["precio"]
        cant = l["cantidad"]
        sub = p * cant
        if cant > 10:
            sub = sub * 0.95
        if cant > 100:
            sub = sub * 0.90   # ojo: esto no se acumula con el de arriba? nadie lo sabe
        total = total + sub

    # iva
    if d.get("pais") == "ES":
        total = total * 1.21
    elif d.get("pais") == "PT":
        total = total * 1.23
    else:
        total = total * 1.21   # revisar con gestoria

    # descuento cliente antiguo
    cur.execute("SELECT alta FROM clientes WHERE nombre = '" + d["cliente"] + "'")
    row = cur.fetchone()
    if row:
        if row[0] < "2020-01-01":
            total = total * 0.97

    # guardar
    cur.execute(
        "INSERT INTO pedidos (cliente, total, estado) VALUES ('"
        + d["cliente"] + "', " + str(total) + ", 'nuevo')"
    )
    c.commit()
    pid = cur.lastrowid

    # notificar
    if d.get("email"):
        try:
            enviar_email(d["email"], pid, total)
        except Exception:
            # La decisión de 2019 sigue en pie: si falla el aviso no se bloquea
            # el pedido. Lo que cambia es que ahora se entera alguien. Con
            # .exception() la traza entera va al registro, y el pedido continúa.
            log.exception(
                "fallo al enviar el aviso del pedido %s a %s; el pedido sigue adelante",
                pid,
                d["email"],
            )

    # facturar
    if total > 0:
        cobrar(API_KEY_PASARELA, total, d.get("tarjeta"))

    c.close()
    return jsonify({"id": pid, "total": total})


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
