#!/usr/bin/env python3
"""
Detector de roturas para el boletín semanal "Qué rompió Claude Code esta semana".

Toma una instantánea de la superficie del CLI (versión, subcomandos y banderas)
y la compara con la anterior. Lo que aparece, lo que desaparece y lo que cambia
de versión es, literalmente, el contenido del boletín.

Uso:
    python3 detectar-roturas.py                # compara y escribe el borrador
    python3 detectar-roturas.py --solo-guardar # primera vez, solo guarda
    python3 detectar-roturas.py --json         # salida en JSON

Por qué esto y no leer las notas de la versión: las notas cuentan lo que el
fabricante considera importante. La superficie del CLI cuenta lo que de verdad
ha cambiado debajo de tus pies.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
INSTANTANEAS = RAIZ / "instantaneas"
BORRADOR = RAIZ / "borrador-boletin.md"
TIEMPO_LIMITE = 45


def ejecutar(args: list[str]) -> str:
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=TIEMPO_LIMITE)
        return (r.stdout or "") + (r.stderr or "")
    except Exception:  # noqa: BLE001
        return ""


def tomar_instantanea() -> dict:
    binario = shutil.which("claude")
    if not binario:
        raise SystemExit("No hay ningún binario 'claude' en el PATH.")

    version = ejecutar([binario, "--version"]).strip()
    ayuda = ejecutar([binario, "--help"])

    # Banderas: --algo, capturando también la forma corta cuando va delante.
    banderas = sorted(set(re.findall(r"(--[a-zA-Z][a-zA-Z0-9-]+)", ayuda)))

    # Subcomandos: bloque "Commands:" hasta el final o hasta la siguiente sección.
    subcomandos: list[str] = []
    bloque = re.search(r"^Commands:\n(.*)", ayuda, re.S | re.M)
    if bloque:
        for linea in bloque.group(1).splitlines():
            m = re.match(r"^\s{2}([a-z][a-z0-9|-]*)\s", linea)
            if m:
                subcomandos.append(m.group(1).split("|")[0])
    subcomandos = sorted(set(subcomandos))

    return {
        "fecha_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "version": version,
        "banderas": banderas,
        "subcomandos": subcomandos,
    }


def ultima_instantanea() -> dict | None:
    INSTANTANEAS.mkdir(exist_ok=True)
    archivos = sorted(INSTANTANEAS.glob("*.json"))
    if not archivos:
        return None
    return json.loads(archivos[-1].read_text(encoding="utf-8"))


def guardar(inst: dict) -> Path:
    INSTANTANEAS.mkdir(exist_ok=True)
    marca = re.sub(r"[^0-9]", "", inst["fecha_utc"])[:14]
    ruta = INSTANTANEAS / f"{marca}.json"
    ruta.write_text(json.dumps(inst, ensure_ascii=False, indent=2), encoding="utf-8")
    return ruta


def comparar(antes: dict, ahora: dict) -> dict:
    a_b, n_b = set(antes["banderas"]), set(ahora["banderas"])
    a_s, n_s = set(antes["subcomandos"]), set(ahora["subcomandos"])
    return {
        "version_antes": antes["version"],
        "version_ahora": ahora["version"],
        "cambio_version": antes["version"] != ahora["version"],
        "banderas_nuevas": sorted(n_b - a_b),
        "banderas_retiradas": sorted(a_b - n_b),
        "subcomandos_nuevos": sorted(n_s - a_s),
        "subcomandos_retirados": sorted(a_s - n_s),
        "desde": antes["fecha_utc"],
        "hasta": ahora["fecha_utc"],
    }


def hay_novedad(d: dict) -> bool:
    return bool(
        d["cambio_version"]
        or d["banderas_nuevas"]
        or d["banderas_retiradas"]
        or d["subcomandos_nuevos"]
        or d["subcomandos_retirados"]
    )


def redactar(d: dict) -> str:
    fecha = d["hasta"][:10]
    L = [f"# Qué rompió Claude Code esta semana · {fecha}", ""]

    if not hay_novedad(d):
        L += [
            f"**Nada.** La superficie del CLI sigue igual que el {d['desde'][:10]}, "
            f"en `{d['version_ahora']}`.",
            "",
            "Una semana sin cambios también es información: si algo se te ha roto,",
            "no ha sido el CLI. Empieza a mirar por tu configuración.",
            "",
        ]
    else:
        if d["cambio_version"]:
            L += [
                f"**Versión:** `{d['version_antes']}` → `{d['version_ahora']}`",
                "",
            ]
        else:
            L += [f"**Versión:** sigue en `{d['version_ahora']}`", ""]

        if d["subcomandos_retirados"]:
            L += ["## Se ha ido (esto es lo que rompe)", ""]
            L += [f"- Subcomando `claude {s}`" for s in d["subcomandos_retirados"]]
            L += [""]
        if d["banderas_retiradas"]:
            if not d["subcomandos_retirados"]:
                L += ["## Se ha ido (esto es lo que rompe)", ""]
            L += [f"- Bandera `{b}`" for b in d["banderas_retiradas"]]
            L += [""]

        if d["subcomandos_nuevos"] or d["banderas_nuevas"]:
            L += ["## Es nuevo", ""]
            L += [f"- Subcomando `claude {s}`" for s in d["subcomandos_nuevos"]]
            L += [f"- Bandera `{b}`" for b in d["banderas_nuevas"]]
            L += [""]

    L += [
        "## Qué hacer con esto",
        "",
        "_(Rellenar a mano: una recomendación concreta, no un resumen de lo de arriba.)_",
        "",
        "---",
        "",
        f"Medido comparando la superficie real del CLI entre el {d['desde'][:10]} y "
        f"el {d['hasta'][:10]}. No es un resumen de las notas de la versión: es lo que "
        "ha cambiado de verdad debajo de tus pies.",
        "",
        "Boletín de *Claude Code en producción* · Cosas Agénticas · sin afiliación con Anthropic.",
        "",
    ]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="Detecta cambios en la superficie del CLI.")
    ap.add_argument("--solo-guardar", action="store_true", help="guarda instantánea y sale")
    ap.add_argument("--json", action="store_true", help="salida en JSON")
    args = ap.parse_args()

    ahora = tomar_instantanea()
    antes = ultima_instantanea()

    if args.solo_guardar or antes is None:
        ruta = guardar(ahora)
        print(f"Instantánea guardada en {ruta.name}")
        print(f"Versión: {ahora['version']}")
        print(f"{len(ahora['banderas'])} banderas y {len(ahora['subcomandos'])} subcomandos registrados.")
        if antes is None and not args.solo_guardar:
            print("Era la primera. Vuelve a pasarlo la semana que viene para tener comparación.")
        return 0

    d = comparar(antes, ahora)
    guardar(ahora)
    BORRADOR.write_text(redactar(d), encoding="utf-8")

    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
    else:
        print(f"Comparado {d['desde'][:10]} → {d['hasta'][:10]}")
        if hay_novedad(d):
            print("HAY NOVEDAD:")
            for k in ("subcomandos_retirados", "banderas_retiradas",
                      "subcomandos_nuevos", "banderas_nuevas"):
                if d[k]:
                    print(f"  {k.replace('_',' ')}: {', '.join(d[k])}")
        else:
            print("Sin cambios en la superficie del CLI.")
        print(f"Borrador escrito en {BORRADOR.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
