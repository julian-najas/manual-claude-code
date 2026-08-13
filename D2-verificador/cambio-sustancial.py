#!/usr/bin/env python3
"""
¿Ha cambiado algo que merezca un commit?

`estado.json` lleva la fecha de ejecución, así que comparar el archivo entero
daría cambios todos los días y llenaría el historial de ruido. Esto compara la
**sustancia**: la versión del CLI verificada y el resultado de cada prueba.

    python3 cambio-sustancial.py            # compara contra HEAD
    python3 cambio-sustancial.py --ref v2026.08

Salida:
    0  hay cambio sustancial, o no había estado previo → publica
    1  nada sustancial ha cambiado → no publiques
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
RUTA = "D2-verificador/estado.json"


def huella(texto: str) -> dict:
    d = json.loads(texto)
    return {
        "cli": d.get("cli_verificado"),
        "resumen": d.get("resumen"),
        "pruebas": {p["id"]: p["resultado"] for p in d.get("pruebas", [])},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Detecta cambios sustanciales de estado.")
    ap.add_argument("--ref", default="HEAD")
    ap.add_argument("--verboso", action="store_true")
    args = ap.parse_args()

    actual_ruta = RAIZ / "estado.json"
    if not actual_ruta.exists():
        print("No hay estado.json actual. Ejecuta antes verificar.py", file=sys.stderr)
        return 0  # publicar por si acaso es preferible a callarse

    nuevo = huella(actual_ruta.read_text(encoding="utf-8"))

    r = subprocess.run(
        ["git", "-C", str(RAIZ.parent), "show", f"{args.ref}:{RUTA}"],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print("No había estado previo: hay que publicar.")
        return 0

    viejo = huella(r.stdout)
    if viejo == nuevo:
        print("Sin cambios sustanciales: misma versión del CLI y mismos resultados.")
        return 1

    if args.verboso or True:
        if viejo["cli"] != nuevo["cli"]:
            print(f"Cambia la versión verificada: {viejo['cli']} → {nuevo['cli']}")
        for pid, res in nuevo["pruebas"].items():
            antes = viejo["pruebas"].get(pid)
            if antes != res:
                print(f"  {pid}: {antes or 'nueva'} → {res}")
        for pid in viejo["pruebas"]:
            if pid not in nuevo["pruebas"]:
                print(f"  {pid}: retirada")
    return 0


if __name__ == "__main__":
    sys.exit(main())
