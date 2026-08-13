#!/usr/bin/env python3
"""
Caza contradicciones entre archivos.

    python3 fabrica/comprobar-coherencia.py

El verificador de afirmaciones comprueba que el libro dice la verdad **sobre la
herramienta**. Esto comprueba que el repositorio no se contradice **a sí mismo**,
que es una clase de fallo distinta y la que nos mordió: al corregir el
comportamiento de MCP, la corrección llegó a la referencia de una skill pero no a
su SKILL.md, y las dos frases opuestas convivieron sin que ninguna prueba fallara.

Lee `fabrica/hechos.yaml`, y por cada hecho busca sus `prohibido` en todos los
`.md` del repositorio, saltándose los archivos declarados en `excepto` y los
directorios de trabajo.

Salida: 0 si no hay contradicciones, 1 si las hay.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
HECHOS = RAIZ / "fabrica" / "hechos.yaml"
IGNORAR = {".git", "_archivo", "__pycache__", "node_modules", "D6-repo-feo"}


def cargar_hechos() -> list[dict]:
    """Lee el subconjunto de YAML que usa hechos.yaml, sin dependencias."""
    try:
        import yaml  # type: ignore

        return yaml.safe_load(HECHOS.read_text(encoding="utf-8"))["hechos"]
    except ImportError:
        pass

    hechos: list[dict] = []
    actual: dict | None = None
    lista: str | None = None
    for bruta in HECHOS.read_text(encoding="utf-8").splitlines():
        if not bruta.strip() or bruta.lstrip().startswith("#"):
            continue
        sangria = len(bruta) - len(bruta.lstrip())
        linea = bruta.strip()
        if linea.startswith("- id:"):
            actual = {"id": linea.split(":", 1)[1].strip(), "prohibido": [], "excepto": []}
            hechos.append(actual)
            lista = None
            continue
        if actual is None:
            continue
        if linea.startswith("- "):
            if lista:
                actual[lista].append(linea[2:].strip().strip('"'))
            continue
        if ":" in linea:
            k, v = linea.split(":", 1)
            k, v = k.strip(), v.strip().strip('"')
            if k in ("prohibido", "excepto"):
                lista = k
                if v and v != "[]":
                    actual[k].append(v)
            else:
                lista = None
                actual[k] = v
    return hechos


AVISO_GENERADO = "GENERADO por fabrica/construir.py"


def archivos_md() -> tuple[list[Path], int]:
    """Devuelve los archivos canónicos, y cuántos derivados se saltó.

    Los archivos generados no se revisan: son copia byte a byte de una fuente que
    sí se revisa. Revisarlos triplicaría cada aviso y obligaría a declarar la
    misma excepción tres veces, que es el problema de duplicación que esta
    fábrica existe para matar.
    """
    out, derivados = [], 0
    for p in sorted(RAIZ.rglob("*.md")):
        if any(parte in IGNORAR for parte in p.parts):
            continue
        cabecera = p.read_text(encoding="utf-8")[:400]
        if AVISO_GENERADO in cabecera:
            derivados += 1
            continue
        # las copias de módulos de la skill no llevan cabecera propia: son el
        # archivo fuente tal cual, así que se identifican por su ruta
        if "skill-guia" in p.parts and "modulos" in p.parts:
            derivados += 1
            continue
        out.append(p)
    return out, derivados


def main() -> int:
    hechos = cargar_hechos()
    archivos, derivados = archivos_md()
    print(f"{len(hechos)} hechos canónicos · {len(archivos)} archivos canónicos "
          f"· {derivados} derivados omitidos\n")

    fallos: list[tuple[str, str, str, int, str]] = []
    for h in hechos:
        prohibidos = [p for p in h.get("prohibido", []) if p]
        if not prohibidos:
            continue
        excepto = {e.strip() for e in h.get("excepto", [])}
        for f in archivos:
            rel = str(f.relative_to(RAIZ))
            if rel in excepto:
                continue
            texto = f.read_text(encoding="utf-8")
            for pat in prohibidos:
                for m in re.finditer(re.escape(pat), texto, re.I):
                    linea = texto[: m.start()].count("\n") + 1
                    ctx = texto.splitlines()[linea - 1].strip()[:110]
                    fallos.append((h["id"], rel, pat, linea, ctx))

    if not fallos:
        print("Sin contradicciones.")
        return 0

    print(f"{len(fallos)} contradicciones:\n")
    for hid, rel, pat, linea, ctx in fallos:
        print(f"  [{hid}] {rel}:{linea}")
        print(f"    patrón prohibido: «{pat}»")
        print(f"    {ctx}\n")
    print("Corrige el texto, o declara el archivo en `excepto` si el patrón es legítimo ahí.",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
