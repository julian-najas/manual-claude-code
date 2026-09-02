# Configuración de gestor-pedidos. Módulo 12 del manual.
#
# Hasta el 2-sep-2026 había DOS archivos de configuración, config.py y
# settings.py, que se contradecían entre sí y que **no se importaban en ningún
# sitio**: app.py fijaba sus valores a mano. Este archivo es ahora el único, y
# app.py lo importa de verdad.
#
# Los valores de abajo son los que la aplicación tenía EN EJECUCIÓN, no los que
# decía settings.py. Unificar no es elegir el archivo más nuevo: es escribir lo
# que ya estaba pasando.

DEBUG = True
DB_PATH = "datos/pedidos.db"

# Tope de líneas por pedido. Cincuenta, que es lo que validaba app.py.
# settings.py decía 100 y llevaba cinco años sin que nadie lo aplicara.
MAX_LINEAS = 50


# --- IVA -------------------------------------------------------------------
#
# ESTOS TIPOS LOS FIJA LA GESTORÍA, NO ESTE ARCHIVO. El manual no certifica
# tipos impositivos: son un dato de negocio, y el laboratorio trabaja con los
# cuatro países que el código tiene que saber contestar.
#
# El día que la gestoría cambie uno, se cambia aquí y la prueba de ese país se
# pone roja. Que se ponga roja es el trabajo que hace.
#
# Lo que este archivo SÍ decide, y es la mitad del módulo 12: no hay tipo por
# defecto. Antes, un país que no estuviera en la lista pagaba el 21 % español
# en silencio, y "no sé de qué país es" y "es de España" eran el mismo caso.
IVA_POR_PAIS = {
    "ES": 0.21,
    "PT": 0.23,
    "FR": 0.20,
    "IT": 0.22,
}


# --- Descuentos por cantidad ------------------------------------------------
#
# SE ACUMULAN. Decidido el 2-sep-2026 y escrito aquí para que deje de ser una
# pregunta. Un pedido de más de 100 unidades pasa por los dos factores:
# 0,95 x 0,90 = 0,855.
#
# No es que se haya decidido que acumular sea lo correcto: es que era lo que
# llevaba pasando desde 2019, nadie decidió lo contrario, y un cambio de precios
# no se cuela dentro de una refactorización. El comentario original decía
# "¿esto no se acumula con el de arriba? nadie lo sabe". Ya se sabe, y está
# escrito. Si negocio decide que no deben acumularse, es cambiar el `elif` de
# app.py y la prueba que lo fija dirá exactamente cuánto cambia la factura.
DESCUENTO_MAS_DE_10 = 0.95
DESCUENTO_MAS_DE_100 = 0.90
