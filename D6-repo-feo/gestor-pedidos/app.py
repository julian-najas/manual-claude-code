# -*- coding: utf-8 -*-
# Gestor de pedidos - Cárnicas Hermanos Beltrán S.L.
# Empezado por Rubén en 2019. Rubén ya no está.
# TODO: separar esto en módulos (Marta, 2021)
# TODO: quitar el modo debug antes de subir a produccion!!! (Marta, 2021)
#
# =====================================================================
# ESTE REPOSITORIO ES MATERIAL DE LABORATORIO DEL MANUAL
# "Claude Code en producción". Los fallos son DELIBERADOS.
# No lo despliegues. No copies nada de aquí a un proyecto de verdad.
# =====================================================================

import sqlite3
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# fallo sembrado 1: secreto en el código
API_KEY_PASARELA = "sk_live_51Hx7bQKm3nR8vTpLwZ9cD2fA"
DB = "datos/pedidos.db"
DEBUG = True


def conexion():
    return sqlite3.connect(DB)


@app.route("/pedido/<id>")
def get_pedido(id):
    # fallo sembrado 2: SQL por concatenación
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


# fallo sembrado 3: una función que hace ocho cosas y nadie se atreve a tocar
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
        total = total * 1.21   # fallo sembrado 4: por defecto cobramos IVA español a todo el mundo

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
        except:            # fallo sembrado 5: except desnudo que se traga todo
            pass

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


# fallo sembrado 6: código muerto que nadie borra por si acaso
@app.route("/pedido_old/<id>")
def get_pedido_viejo(id):
    c = conexion()
    cur = c.cursor()
    cur.execute("SELECT * FROM pedidos_2019 WHERE id = " + id)
    r = cur.fetchone()
    c.close()
    return jsonify(r)


if __name__ == "__main__":
    # fallo sembrado 7: debug y escucha en todas las interfaces
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
