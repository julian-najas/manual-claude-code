#!/usr/bin/env python3
"""
Latido de la rutina del manuscrito.

El problema que resuelve es real y ya nos costó tres módulos. La rutina de la
nube escribe un módulo al día y, cuando termina, anota una entrada en
`_archivo/estado-manuscrito.md`. Cuando NO termina, no anota nada: una sesión
que se cuelga en un diálogo de permisos o que muere por límite de uso deja el
repositorio exactamente igual que si nunca hubiera disparado.

Eso pasó del 21 al 23 de agosto de 2026. Tres días seguidos sin una sola línea,
y solo se detectó el 24 al contar el ritmo real. Tres módulos perdidos y ninguna
señal.

Este script es la señal. Mira la fecha de la entrada más reciente del diario y
falla cuando el silencio pasa de la tolerancia. No comprueba que el módulo esté
bien: para eso está el verificador. Comprueba que ALGUIEN escribió algo, que es
justo lo que no ocurre cuando una sesión se muere sola.

Uso:
    python3 fabrica/latido-rutina.py                    # tolerancia 0: hoy
    python3 fabrica/latido-rutina.py --tolerancia 1     # vale también ayer
    python3 fabrica/latido-rutina.py --json             # para la CI

Códigos de salida:
    0  hay entrada dentro de la tolerancia
    1  la rutina lleva callada más de la cuenta
    2  no se puede comprobar (diario ilegible o sin entradas con fecha)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIARIO = RAIZ / "_archivo" / "estado-manuscrito.md"

# Solo cuentan los encabezados de nivel 2 que empiezan por una fecha ISO. El
# diario tiene además secciones sin fecha ("Cómo se escribe esto ahora"), y
# esas no son latidos.
ENCABEZADO_CON_FECHA = re.compile(r"^##\s+(\d{4})-(\d{2})-(\d{2})", re.M)


def entradas(texto: str) -> list[date]:
    vistas = []
    for anio, mes, dia in ENCABEZADO_CON_FECHA.findall(texto):
        try:
            vistas.append(date(int(anio), int(mes), int(dia)))
        except ValueError:
            # Una fecha imposible en un encabezado es una errata del diario, no
            # un latido. Se ignora en vez de reventar el flujo entero.
            continue
    return sorted(vistas, reverse=True)


def main() -> int:
    p = argparse.ArgumentParser(description="Comprueba que la rutina sigue viva.")
    p.add_argument(
        "--tolerancia",
        type=int,
        default=0,
        help="días de silencio admitidos. 0 exige una entrada de hoy.",
    )
    p.add_argument("--json", action="store_true", help="vuelca el veredicto en JSON")
    args = p.parse_args()

    if not DIARIO.exists():
        print(f"No existe {DIARIO.relative_to(RAIZ)}: no se puede comprobar.", file=sys.stderr)
        return 2

    fechas = entradas(DIARIO.read_text(encoding="utf-8"))
    if not fechas:
        print("El diario no tiene ninguna entrada con fecha.", file=sys.stderr)
        return 2

    hoy = datetime.now(timezone.utc).date()
    ultima = fechas[0]
    silencio = (hoy - ultima).days

    # Una entrada con fecha futura es una errata o un reloj mal puesto. Se avisa
    # y se cuenta como cero días de silencio: no vamos a dar la alarma por eso.
    if silencio < 0:
        print(f"Aviso: la entrada más reciente ({ultima}) está en el futuro.", file=sys.stderr)
        silencio = 0

    vivo = silencio <= args.tolerancia
    veredicto = {
        "fecha_comprobacion": hoy.isoformat(),
        "ultima_entrada": ultima.isoformat(),
        "dias_de_silencio": silencio,
        "tolerancia": args.tolerancia,
        "viva": vivo,
        "entradas_totales": len(fechas),
    }

    if args.json:
        print(json.dumps(veredicto, ensure_ascii=False, indent=2))
    elif vivo:
        print(f"La rutina está viva. Última entrada: {ultima} ({silencio} día(s) de silencio).")
    else:
        print(
            f"LA RUTINA LLEVA {silencio} DÍA(S) CALLADA. "
            f"Última entrada: {ultima}. Tolerancia: {args.tolerancia}.",
            file=sys.stderr,
        )
        print(
            "Una sesión que se cuelga no deja rastro, así que esto no dice qué "
            "pasó, solo que pasó. Mira el panel de la rutina.",
            file=sys.stderr,
        )

    return 0 if vivo else 1


if __name__ == "__main__":
    raise SystemExit(main())
