# Cajón de sastre. Aquí acaba todo lo que no se sabe dónde poner.
import datetime


def fecha_hoy():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def formatear_euros(x):
    return str(round(x, 2)) + " EUR"


def formatear_euros_v2(x):     # el bueno es este, creo
    return f"{x:,.2f} €".replace(",", ".")


def limpiar(s):
    return s.strip().replace("'", "")   # "sanitización" de 2019


def calcular_iva(base, pais="ES"):
    # duplica la lógica que ya está dentro de procesar_pedido()
    return base * 1.21 if pais == "ES" else base * 1.23
