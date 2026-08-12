#!/usr/bin/env python3
"""
Verificador del manual "Claude Code en producción".

Ejecuta cada afirmación del registro contra el Claude Code que hay instalado
en esta máquina y escribe el estado en ESTADO.md y estado.json.

Uso:
    python3 verificar.py                 # solo pruebas gratis
    python3 verificar.py --con-coste     # incluye las que gastan tokens
    python3 verificar.py --json          # vuelca el JSON por stdout

Códigos de salida:
    0  todas las pruebas ejecutadas han pasado
    1  hay al menos un FALLO
    2  error de configuración (registro ilegible, binario ausente)

Reglas de la casa:
  - Una prueba marcada como destructiva NUNCA se ejecuta.
  - Una prueba marcada con coste solo se ejecuta si se pide explícitamente.
  - Si el binario no está, se falla entero: un libro no puede decir "verificado"
    sobre una máquina donde no hay nada que verificar.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
REGISTRO = RAIZ / "registro.yaml"
TIEMPO_LIMITE = 45  # segundos por prueba

PASA = "PASA"
FALLA = "FALLA"
OMITIDO = "OMITIDO"
REVISAR = "REVISAR"


# --------------------------------------------------------------------------
# Lector de YAML mínimo
#
# El registro usa un subconjunto deliberadamente pobre de YAML para no
# arrastrar dependencias: un libro que necesita `pip install` para comprobarse
# a sí mismo es un libro que nadie comprueba. Si PyYAML está disponible se usa,
# y si no, este lector cubre el subconjunto que emplea el registro.
# --------------------------------------------------------------------------
def cargar_registro(ruta: Path) -> dict:
    texto = ruta.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        return yaml.safe_load(texto)
    except ImportError:
        return _yaml_pobre(texto)


def _valor(bruto: str):
    bruto = bruto.strip()
    if bruto.startswith("[") and bruto.endswith("]"):
        interior = bruto[1:-1].strip()
        if not interior:
            return []
        return [_valor(x) for x in _partir_lista(interior)]
    if len(bruto) >= 2 and bruto[0] == bruto[-1] and bruto[0] in "\"'":
        return bruto[1:-1]
    if bruto in ("true", "True"):
        return True
    if bruto in ("false", "False"):
        return False
    if re.fullmatch(r"-?\d+", bruto):
        return int(bruto)
    return bruto


def _partir_lista(interior: str) -> list[str]:
    partes, actual, comilla = [], "", None
    for ch in interior:
        if comilla:
            actual += ch
            if ch == comilla:
                comilla = None
        elif ch in "\"'":
            comilla = ch
            actual += ch
        elif ch == ",":
            partes.append(actual)
            actual = ""
        else:
            actual += ch
    if actual.strip():
        partes.append(actual)
    return partes


def _yaml_pobre(texto: str) -> dict:
    datos: dict = {"meta": {}, "pruebas": []}
    seccion = None
    actual: dict | None = None
    for linea_bruta in texto.splitlines():
        linea = linea_bruta.split(" #")[0].rstrip() if " #" in linea_bruta else linea_bruta.rstrip()
        if not linea.strip() or linea.lstrip().startswith("#"):
            continue
        sangria = len(linea) - len(linea.lstrip())
        limpia = linea.strip()

        if sangria == 0 and limpia.endswith(":"):
            seccion = limpia[:-1]
            if seccion == "pruebas":
                actual = None
            continue

        if seccion == "meta" and ":" in limpia:
            k, v = limpia.split(":", 1)
            datos["meta"][k.strip()] = _valor(v)
            continue

        if seccion == "pruebas":
            if limpia.startswith("- "):
                actual = {}
                datos["pruebas"].append(actual)
                limpia = limpia[2:]
            if actual is not None and ":" in limpia:
                k, v = limpia.split(":", 1)
                actual[k.strip()] = _valor(v)
    return datos


# --------------------------------------------------------------------------
# Ejecución
# --------------------------------------------------------------------------
def version_cli() -> str:
    binario = shutil.which("claude")
    if not binario:
        return ""
    try:
        r = subprocess.run(
            [binario, "--version"], capture_output=True, text=True, timeout=TIEMPO_LIMITE
        )
        return r.stdout.strip() or r.stderr.strip()
    except Exception as e:  # noqa: BLE001
        return f"error: {e}"


def ejecutar_prueba(p: dict, con_coste: bool, cwd: str) -> dict:
    res = {
        "id": p.get("id", "?"),
        "capitulo": p.get("capitulo", ""),
        "afirmacion": p.get("afirmacion", ""),
        "tipo": p.get("tipo", "cli"),
        "resultado": OMITIDO,
        "motivo": "",
        "comando": "",
        "salida": "",
    }

    if p.get("destructivo"):
        res["motivo"] = "prueba destructiva, documentada pero nunca ejecutada"
        return res

    if p.get("tipo") == "manual":
        res["resultado"] = REVISAR
        res["motivo"] = p.get("nota", "requiere comprobación humana")
        return res

    if p.get("coste") and not con_coste:
        res["motivo"] = "gasta tokens, se ejecuta solo con --con-coste"
        return res

    if p.get("tipo") == "fichero":
        ruta = Path(os.path.expanduser(str(p.get("ruta", "")))).resolve()
        res["comando"] = f"test -e {ruta}"
        existe = ruta.exists()
        res["resultado"] = PASA if existe else FALLA
        res["motivo"] = "existe" if existe else "no existe en esta máquina"
        return res

    comando = p.get("comando") or []
    if not comando:
        res["resultado"] = FALLA
        res["motivo"] = "la prueba no define comando"
        return res

    # Por defecto todo corre en un directorio temporal, para que una prueba no
    # dependa de dónde la lances. Una prueba puede pedir otro sitio con
    # `directorio:`, relativo a la raíz del proyecto, y entonces se comprueba
    # que exista: una prueba que corre en el sitio equivocado no prueba nada.
    donde = cwd
    if p.get("directorio"):
        donde = str((RAIZ.parent / str(p["directorio"])).resolve())
        if not Path(donde).is_dir():
            res["resultado"] = FALLA
            res["motivo"] = f"la prueba pide correr en {p['directorio']} y no existe"
            return res

    res["comando"] = " ".join(comando)
    try:
        r = subprocess.run(
            comando, capture_output=True, text=True, timeout=TIEMPO_LIMITE, cwd=donde
        )
    except FileNotFoundError:
        res["resultado"] = FALLA
        res["motivo"] = f"no existe el ejecutable {comando[0]}"
        return res
    except subprocess.TimeoutExpired:
        res["resultado"] = FALLA
        res["motivo"] = f"se pasó de {TIEMPO_LIMITE} s"
        return res

    salida = (r.stdout or "") + (r.stderr or "")
    res["salida"] = salida[:400]

    fallos = []
    if "espera_salida" in p and r.returncode != p["espera_salida"]:
        fallos.append(f"código de salida {r.returncode}, se esperaba {p['espera_salida']}")
    if "espera_patron" in p and not re.search(str(p["espera_patron"]), salida):
        fallos.append(f"no aparece el patrón /{p['espera_patron']}/")

    res["resultado"] = FALLA if fallos else PASA
    res["motivo"] = "; ".join(fallos) if fallos else "comprobado"
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="Verifica las afirmaciones del manual.")
    ap.add_argument("--con-coste", action="store_true", help="incluye pruebas que gastan tokens")
    ap.add_argument("--json", action="store_true", help="vuelca el JSON por stdout")
    args = ap.parse_args()

    if not REGISTRO.exists():
        print(f"No encuentro el registro en {REGISTRO}", file=sys.stderr)
        return 2

    datos = cargar_registro(REGISTRO)
    pruebas = datos.get("pruebas", [])
    if not pruebas:
        print("El registro no tiene pruebas.", file=sys.stderr)
        return 2

    version = version_cli()
    if not version:
        print("No hay ningún binario 'claude' en el PATH. No se puede verificar nada.", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="verificador-manual-") as cwd:
        resultados = [ejecutar_prueba(p, args.con_coste, cwd) for p in pruebas]

    informe = {
        "libro": datos.get("meta", {}).get("libro", ""),
        "version_libro": datos.get("meta", {}).get("version_libro", ""),
        "cli_verificado": version,
        "sistema": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "fecha_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "resumen": {
            estado: sum(1 for r in resultados if r["resultado"] == estado)
            for estado in (PASA, FALLA, REVISAR, OMITIDO)
        },
        "pruebas": resultados,
    }

    (RAIZ / "estado.json").write_text(
        json.dumps(informe, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (RAIZ / "ESTADO.md").write_text(render_markdown(informe), encoding="utf-8")

    if args.json:
        print(json.dumps(informe, ensure_ascii=False, indent=2))
    else:
        r = informe["resumen"]
        print(f"CLI verificado: {informe['cli_verificado']}")
        print(f"Fecha:          {informe['fecha_utc']}")
        print(
            f"{r[PASA]} pasan · {r[FALLA]} fallan · "
            f"{r[REVISAR]} a revisar · {r[OMITIDO]} omitidas"
        )
        for x in resultados:
            if x["resultado"] == FALLA:
                print(f"  FALLA {x['id']}: {x['afirmacion']} ({x['motivo']})")

    return 1 if informe["resumen"][FALLA] else 0


def render_markdown(informe: dict) -> str:
    icono = {PASA: "🟢", FALLA: "🔴", REVISAR: "🟡", OMITIDO: "⚪"}
    r = informe["resumen"]
    lineas = [
        f"# Estado de verificación · {informe['libro']}",
        "",
        f"**Versión del libro:** {informe['version_libro']}  ",
        f"**Verificado contra:** `{informe['cli_verificado']}`  ",
        f"**Sistema:** {informe['sistema']}  ",
        f"**Fecha:** {informe['fecha_utc']}",
        "",
        f"🟢 {r[PASA]} pasan · 🔴 {r[FALLA]} fallan · "
        f"🟡 {r[REVISAR]} a revisar · ⚪ {r[OMITIDO]} omitidas",
        "",
        "| | ID | Capítulo | Afirmación del libro | Comprobación |",
        "|---|---|---|---|---|",
    ]
    for x in informe["pruebas"]:
        comando = f"`{x['comando']}`" if x["comando"] else x["motivo"]
        lineas.append(
            f"| {icono[x['resultado']]} | {x['id']} | {x['capitulo']} | "
            f"{x['afirmacion']} | {comando} |"
        )
    lineas += [
        "",
        "---",
        "",
        "⚪ **Omitidas** son pruebas destructivas o que gastan dinero. Las destructivas "
        "están documentadas en el libro pero no se ejecutan nunca. Las de coste se "
        "ejecutan a mano con `--con-coste` en cada revisión trimestral.",
        "",
        "🟡 **A revisar** son afirmaciones que solo puede comprobar una persona, "
        "por ejemplo las que necesitan una máquina limpia.",
        "",
        "Este archivo lo genera `verificar.py`. No se edita a mano.",
    ]
    return "\n".join(lineas) + "\n"


if __name__ == "__main__":
    sys.exit(main())
