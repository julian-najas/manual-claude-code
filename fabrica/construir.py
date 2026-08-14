#!/usr/bin/env python3
"""
La fábrica. Una fuente canónica, todas las salidas generadas.

    python3 fabrica/construir.py            # regenera todo
    python3 fabrica/construir.py --comprobar  # no escribe: falla si algo está desfasado

Fuente canónica única:

    guia-21/M*.md          los 21 módulos de la guía
    fabrica/hechos.yaml    los hechos que se citan en más de un sitio

Salidas generadas, que **no se editan a mano**:

    entregables/guia-claude-code-2026-08.md              guía ensamblada con índice
    entregables/skill-guia/guia-claude-code/modulos/     copias para la skill
    entregables/skill-guia/guia-claude-code/INDICE-SINTOMAS.md

El modo `--comprobar` es el que va en CI: no escribe nada y devuelve 1 si alguna
salida no coincide con lo que se generaría hoy. Así una edición a mano de un
archivo derivado se detecta en vez de sobrevivir semanas, que es exactamente lo
que nos pasó con la contradicción del MCP.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "guia-21"
SKILL = RAIZ / "entregables" / "skill-guia" / "guia-claude-code"
GUIA = RAIZ / "entregables" / "guia-claude-code-2026-08.md"

AVISO = "<!-- GENERADO por fabrica/construir.py · no editar a mano -->"


def modulos() -> list[Path]:
    return sorted(FUENTE.glob("M*.md"), key=lambda p: int(p.name.split("-")[0][1:]))


def ancla(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s·-]", "", s).replace("·", "").strip()
    return re.sub(r"\s+", "-", s)


# --------------------------------------------------------------------------
# salidas
# --------------------------------------------------------------------------
def render_guia(mods: list[Path]) -> str:
    partes = [
        AVISO,
        "",
        "# Guía Definitiva de Claude Code",
        "",
        "**Versión de la guía:** v2026.08",
        "**Verificada contra:** Claude Code **2.1.228**",
        "**Fecha de corte:** 12 de agosto de 2026",
        "**Audiencia:** arquitecto o consultor que despliega para equipos; lector secundario, dev diario",
        "**Entorno de referencia:** Linux en servidor propio, con notas para macOS y WSL2",
        "",
        "> Esta guía no está afiliada, patrocinada ni respaldada por Anthropic.",
        "> Toda afirmación técnica procede de documentación oficial descargada el 12 de",
        "> agosto de 2026, de la superficie observable del CLI instalado, o de mediciones",
        "> propias, y cada módulo declara sus fuentes al pie.",
        "",
        "---",
        "",
        "## Índice",
    ]
    idx = []
    for f in mods:
        t = f.read_text(encoding="utf-8")
        tit = t.splitlines()[0].lstrip("# ").strip()
        idx.append(f"- [{tit}](#{ancla(tit)})")
        for s in re.findall(r"^## (\d+\.\d+ · .+)$", t, re.M):
            idx.append(f"  - [{s}](#{ancla(s)})")
    partes.append("\n".join(idx))
    partes.append("\n\n---\n")
    for f in mods:
        partes.append(f.read_text(encoding="utf-8").rstrip() + "\n\n---\n")
    return "\n".join(partes)


COMPANION = "https://julian-najas.github.io/claude-code-companion"


def ranura(s: str) -> str:
    """Misma normalización que `generar-companion.py`. Si las dos divergen, el
    generador del companion lo detecta al validar y falla; aquí solo se usa para
    enlazar."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_]+", "-", s)[:70].strip("-")


def con_resolucion() -> set[str]:
    """Ranuras que tienen resolución completa en `resoluciones.yaml`.

    Se leen las claves de primer nivel con una expresión regular en vez de con
    PyYAML a propósito: esto solo decide si una fila lleva enlace, y no merece
    añadirle una dependencia a la construcción entera. La validación de verdad
    la hace `generar-companion.py`, que sí carga el YAML y falla si no cuadra.
    """
    ruta = RAIZ / "fabrica" / "resoluciones.yaml"
    if not ruta.exists():
        return set()
    return set(re.findall(r"^([a-z0-9][a-z0-9-]*):\s*$", ruta.read_text(encoding="utf-8"), re.M))


def render_indice_sintomas(mods: list[Path]) -> str:
    filas = []
    for f in mods:
        t = f.read_text(encoding="utf-8")
        mod = f.name.split("-")[0]
        seg = re.split(r"^## Errores típicos.*$", t, flags=re.M)
        if len(seg) < 2:
            continue
        cuerpo = re.split(r"^---\s*$", seg[1], flags=re.M)[0]
        for s, c in re.findall(r'^\|\s*"?([^|"]+?)"?\s*\|\s*(.+?)\s*\|\s*$', cuerpo, re.M):
            if s.strip() in ("Síntoma", "Lo que se hace") or set(s.strip()) <= set("-: "):
                continue
            filas.append((s.strip(), c.strip(), mod))
    res = con_resolucion()
    limpio = re.compile(r"[`*]")
    marcadas = [(s, c, m, ranura(limpio.sub("", s).strip('"'))) for s, c, m in filas]
    n = sum(1 for *_, r in marcadas if r in res)
    L = [
        AVISO,
        "",
        "# Índice por síntoma",
        "",
        f"**{len(filas)} síntomas** extraídos de las tablas de errores típicos de los "
        f"{len(mods)} módulos.",
        "",
        "Busca lo que te pasa, no lo que crees que es.",
        "",
        # el texto se deriva del dato: cuando faltaban resoluciones, esta línea lo
        # decía; decir "los demás llegan hasta la causa" con cobertura completa
        # sería mentir por inercia
        (f"**Los {len(filas)} tienen resolución verificable publicada**: diagnóstico, "
         "un comando para comprobarlo, los pasos y un criterio objetivo que dice si "
         "quedó resuelto. La columna **Resolución** enlaza a la suya."
         if n >= len(filas) else
         f"De los {len(filas)}, **{n} tienen resolución verificable publicada**: "
         "diagnóstico, un comando para comprobarlo, los pasos y un criterio objetivo "
         "que dice si quedó resuelto. La columna **Resolución** enlaza a la suya. "
         "Los demás llegan hasta la causa, que es lo que hay en esta tabla."),
        "",
        "| Síntoma | Qué está pasando | Módulo | Resolución |",
        "|---|---|---|---|",
    ]
    L += [
        f"| {s} | {c} | [{m}](modulos/) | "
        f"{f'[procedimiento]({COMPANION}/{r}/)' if r in res else '—'} |"
        for s, c, m, r in marcadas
    ]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Genera todas las salidas desde la fuente canónica.")
    ap.add_argument("--comprobar", action="store_true",
                    help="no escribe: falla si alguna salida está desfasada")
    args = ap.parse_args()

    mods = modulos()
    if len(mods) != 21:
        print(f"Esperaba 21 módulos en {FUENTE} y encuentro {len(mods)}", file=sys.stderr)
        return 2

    desfasadas: list[str] = []

    def emitir(destino: Path, contenido: str, etiqueta: str) -> None:
        actual = destino.read_text(encoding="utf-8") if destino.exists() else None
        if actual == contenido:
            print(f"  al día    {etiqueta}")
            return
        if args.comprobar:
            desfasadas.append(etiqueta)
            print(f"  DESFASADA {etiqueta}")
        else:
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(contenido, encoding="utf-8")
            print(f"  escrita   {etiqueta}")

    print(f"Fuente: {len(mods)} módulos en guia-21/\n")
    emitir(GUIA, render_guia(mods), "guía ensamblada")
    emitir(SKILL / "INDICE-SINTOMAS.md", render_indice_sintomas(mods), "índice por síntoma")

    # copias de módulos para la skill
    destino_mods = SKILL / "modulos"
    for f in mods:
        emitir(destino_mods / f.name, f.read_text(encoding="utf-8"), f"skill · {f.name}")
    if destino_mods.exists():
        sobrantes = {p.name for p in destino_mods.glob("M*.md")} - {f.name for f in mods}
        for s in sobrantes:
            if args.comprobar:
                desfasadas.append(f"sobra en la skill: {s}")
                print(f"  SOBRA     skill · {s}")
            else:
                (destino_mods / s).unlink()
                print(f"  borrada   skill · {s}")

    huella = hashlib.md5(b"".join(f.read_bytes() for f in mods)).hexdigest()[:8]
    print(f"\nHuella de la fuente: {huella}")

    if args.comprobar and desfasadas:
        print(f"\n{len(desfasadas)} salidas desfasadas. Ejecuta: python3 fabrica/construir.py",
              file=sys.stderr)
        return 1
    if args.comprobar:
        print("\nTodas las salidas están al día.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
