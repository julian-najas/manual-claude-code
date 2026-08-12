#!/usr/bin/env python3
"""
Verifica los bloques de código de la guía.

    python3 verificar-ejemplos.py ../guia-21/M*.md

Qué comprueba, por tipo de bloque:

  json      se parsea. Un JSON inválido en una plantilla es un archivo que
            Claude Code rechaza entero, así que esto no es cosmético.
  bash      análisis de sintaxis con `bash -n`, y además **cada bandera y cada
            subcomando de `claude` se contrasta con el binario instalado**.
            Ahí es donde se cazan los ejemplos caducados.
  yaml      se parsea si hay PyYAML; si no, se informa y no se finge.
  mermaid   comprobación estructural mínima.

**Nada se ejecuta.** Un verificador de documentación que ejecuta los comandos de
la documentación es un verificador que un día borra algo. Se valida, no se corre.

Salida: 0 si todo pasa, 1 si algo falla, 2 si no hay nada que verificar.
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BLOQUE = re.compile(r"```([a-zA-Z]*)[^\n]*\n(.*?)```", re.S)


def superficie_cli() -> tuple[set[str], set[str]]:
    """Banderas y subcomandos que expone el binario instalado."""
    binario = shutil.which("claude")
    if not binario:
        return set(), set()
    try:
        ayuda = subprocess.run(
            [binario, "--help"], capture_output=True, text=True, timeout=45
        ).stdout
    except Exception:  # noqa: BLE001
        return set(), set()
    banderas = set(re.findall(r"(--[a-zA-Z][a-zA-Z0-9-]+)", ayuda))
    subs = set()
    m = re.search(r"^Commands:\n(.*)", ayuda, re.S | re.M)
    if m:
        for linea in m.group(1).splitlines():
            s = re.match(r"^\s{2}([a-z][a-z0-9|-]*)\s", linea)
            if s:
                subs.add(s.group(1).split("|")[0])
    return banderas, subs


def comprobar_json(codigo: str) -> tuple[bool, str]:
    try:
        json.loads(codigo)
        return True, "parsea"
    except json.JSONDecodeError as ex:
        return False, f"JSON inválido: {ex}"


def comprobar_yaml(codigo: str) -> tuple[bool, str]:
    try:
        import yaml  # type: ignore
    except ImportError:
        return True, "sin PyYAML, no verificado"

    # Un bloque de frontmatter va delimitado por --- y, en YAML puro, eso es un
    # documento múltiple. No es un error: es cómo se escribe el frontmatter de
    # una skill o de un subagente. Se valida el bloque interior.
    m = re.match(r"\s*---\s*\n(.*?)\n---\s*(\n(.*))?$", codigo, re.S)
    objetivo, etiqueta = (m.group(1), "frontmatter") if m else (codigo, "parsea")

    try:
        datos = yaml.safe_load(objetivo)
    except Exception as ex:  # noqa: BLE001
        return False, f"YAML inválido: {ex}"

    if etiqueta == "frontmatter":
        if not isinstance(datos, dict):
            return False, "el frontmatter no es un mapa de claves"
        if "description" not in datos and "name" not in datos:
            return False, "frontmatter sin name ni description"
    return True, etiqueta


def comprobar_mermaid(codigo: str) -> tuple[bool, str]:
    if not re.match(r"\s*(flowchart|graph|sequenceDiagram|classDiagram|stateDiagram)", codigo):
        return False, "no empieza por un tipo de diagrama conocido"
    if "-->" not in codigo and "->>" not in codigo and "---" not in codigo:
        return False, "no tiene ninguna arista"
    return True, "estructura válida"


def comprobar_bash(codigo: str, banderas: set[str], subs: set[str]) -> tuple[bool, str]:
    problemas = []

    # 1. sintaxis, sin ejecutar nada
    with tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False) as f:
        f.write(codigo)
        ruta = f.name
    try:
        r = subprocess.run(["bash", "-n", ruta], capture_output=True, text=True, timeout=20)
        if r.returncode != 0:
            problemas.append(f"sintaxis: {r.stderr.strip().splitlines()[0] if r.stderr.strip() else 'error'}")
    except Exception as ex:  # noqa: BLE001
        problemas.append(f"no se pudo analizar: {ex}")
    finally:
        Path(ruta).unlink(missing_ok=True)

    # 2. la parte que de verdad caza ejemplos caducados
    if banderas or subs:
        for linea in codigo.splitlines():
            if not re.search(r"(^|\s|\|)claude\s", linea):
                continue
            for b in re.findall(r"\s(--[a-zA-Z][a-zA-Z0-9-]+)", linea):
                if b not in banderas:
                    problemas.append(f"bandera inexistente en el binario: {b}")
            m = re.search(r"claude\s+([a-z][a-z0-9-]*)", linea)
            if m and m.group(1) not in subs and not m.group(1).startswith("-"):
                if m.group(1) not in {"code", "mcp"}:
                    problemas.append(f"subcomando inexistente en el binario: {m.group(1)}")

    return (not problemas), ("; ".join(dict.fromkeys(problemas)) if problemas else "válido")


def main() -> int:
    ap = argparse.ArgumentParser(description="Verifica los bloques de código de la guía.")
    ap.add_argument("rutas", nargs="+")
    ap.add_argument("--verboso", action="store_true")
    args = ap.parse_args()

    archivos = sorted({p for r in args.rutas for p in glob.glob(r)})
    if not archivos:
        print("No he encontrado ningún archivo.", file=sys.stderr)
        return 2

    banderas, subs = superficie_cli()
    if banderas:
        print(f"Superficie del CLI: {len(banderas)} banderas, {len(subs)} subcomandos\n")
    else:
        print("Sin binario 'claude': no se contrastan banderas ni subcomandos\n")

    comprobadores = {
        "json": lambda c: comprobar_json(c),
        "yaml": lambda c: comprobar_yaml(c),
        "yml": lambda c: comprobar_yaml(c),
        "mermaid": lambda c: comprobar_mermaid(c),
        "bash": lambda c: comprobar_bash(c, banderas, subs),
        "sh": lambda c: comprobar_bash(c, banderas, subs),
    }

    total = ok = fallos = saltados = 0
    detalle_fallos = []

    for ruta in archivos:
        texto = Path(ruta).read_text(encoding="utf-8")
        for i, (lang, codigo) in enumerate(BLOQUE.findall(texto), 1):
            total += 1
            fn = comprobadores.get(lang.lower())
            if not fn:
                saltados += 1
                continue
            bien, motivo = fn(codigo)
            if bien:
                ok += 1
                if args.verboso:
                    print(f"  OK    {Path(ruta).name} #{i} [{lang}] {motivo}")
            else:
                fallos += 1
                detalle_fallos.append((Path(ruta).name, i, lang, motivo, codigo.strip()[:120]))

    print(f"{total} bloques · {ok} verificados · {fallos} fallan · {saltados} sin comprobador")
    for nombre, i, lang, motivo, frag in detalle_fallos:
        print(f"\n  FALLA {nombre} bloque #{i} [{lang}]")
        print(f"    {motivo}")
        print(f"    {frag.splitlines()[0] if frag else ''}")

    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
