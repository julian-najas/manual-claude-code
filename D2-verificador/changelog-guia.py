#!/usr/bin/env python3
"""
Genera el changelog de la guía entre dos versiones, escrito para el lector.

    python3 changelog-guia.py v2026.08 HEAD
    python3 changelog-guia.py v2026.08 v2026.11 --salida CHANGELOG-v2026.11.md

Un `git diff` no sirve para esto: al lector no le importan las líneas, le importa
**qué afirmación cambió**, porque puede estar actuando con la versión vieja en la
cabeza. Así que el changelog se construye sobre tres fuentes:

  1. `estado.json`  → afirmaciones nuevas, retiradas y las que cambiaron de texto.
     Esto es lo que más importa: una afirmación corregida significa que el lector
     puede tener información equivocada.
  2. Los módulos     → qué secciones aparecen, desaparecen o cambian.
  3. La versión del CLI contra la que se verificó cada corte.

Cierra con el tiempo estimado de relectura, que es la promesa del producto:
solo lees lo nuevo.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PALABRAS_POR_MINUTO = 220


def git(*args: str) -> str:
    r = subprocess.run(["git", "-C", str(RAIZ), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} falló:\n{r.stderr.strip()}")
    return r.stdout


def existe_ref(ref: str) -> bool:
    return subprocess.run(
        ["git", "-C", str(RAIZ), "rev-parse", "--verify", "--quiet", ref],
        capture_output=True,
    ).returncode == 0


def leer(ref: str, ruta: str) -> str | None:
    r = subprocess.run(
        ["git", "-C", str(RAIZ), "show", f"{ref}:{ruta}"], capture_output=True, text=True
    )
    return r.stdout if r.returncode == 0 else None


def estado(ref: str) -> dict:
    crudo = leer(ref, "D2-verificador/estado.json")
    if not crudo:
        return {}
    try:
        return json.loads(crudo)
    except json.JSONDecodeError:
        return {}


def modulos(ref: str) -> dict[str, str]:
    salida = git("ls-tree", "-r", "--name-only", ref, "guia-21/")
    d = {}
    for ruta in salida.splitlines():
        if re.search(r"/M\d+-[^/]+\.md$", ruta):
            contenido = leer(ref, ruta)
            if contenido is not None:
                d[Path(ruta).name.split("-")[0]] = contenido
    return d


def secciones(texto: str) -> dict[str, str]:
    partes = re.split(r"^## (.+)$", texto, flags=re.M)
    return {partes[i].strip(): partes[i + 1] for i in range(1, len(partes) - 1, 2)}


def palabras(t: str) -> int:
    return len(re.sub(r"```.*?```", "", t, flags=re.S).split())


def main() -> int:
    ap = argparse.ArgumentParser(description="Changelog de la guía entre dos versiones.")
    ap.add_argument("desde")
    ap.add_argument("hasta", nargs="?", default="HEAD")
    ap.add_argument("--salida")
    args = ap.parse_args()

    for ref in (args.desde, args.hasta):
        if not existe_ref(ref):
            raise SystemExit(f"No existe la referencia: {ref}")

    ea, eb = estado(args.desde), estado(args.hasta)
    ma, mb = modulos(args.desde), modulos(args.hasta)

    if not mb:
        raise SystemExit(f"No encuentro módulos en {args.hasta}")

    L: list[str] = []
    a = L.append

    cli_a = ea.get("cli_verificado", "desconocido")
    cli_b = eb.get("cli_verificado", "desconocido")
    a(f"# Qué cambia respecto a `{args.desde}`")
    a("")
    a(f"**Verificada ahora contra `{cli_b}`**"
      + (f", antes contra `{cli_a}`." if cli_a != cli_b else "."))
    a("")
    a("Esto no es un `git diff`: es lo que te afecta a ti si ya te leíste la")
    a("versión anterior. Si solo tienes cinco minutos, lee el primer apartado.")
    a("")

    # ---- 1. afirmaciones ----
    pa = {p["id"]: p for p in ea.get("pruebas", [])}
    pb = {p["id"]: p for p in eb.get("pruebas", [])}
    nuevas = [i for i in pb if i not in pa]
    retiradas = [i for i in pa if i not in pb]
    corregidas = [i for i in pb if i in pa and pb[i]["afirmacion"] != pa[i]["afirmacion"]]
    cambio_estado = [
        i for i in pb if i in pa and pb[i]["resultado"] != pa[i]["resultado"]
    ]

    a("## 1 · Lo que cambia de lo que ya sabías")
    a("")
    if corregidas:
        a("### Afirmaciones corregidas · **léelas sí o sí**")
        a("")
        a("Si actuaste sobre la versión anterior, puedes tener información equivocada.")
        a("")
        for i in corregidas:
            a(f"- **{i}** ({pb[i]['capitulo']})")
            a(f"  - Antes: {pa[i]['afirmacion']}")
            a(f"  - Ahora: **{pb[i]['afirmacion']}**")
        a("")
    if cambio_estado:
        a("### Afirmaciones que cambiaron de estado")
        a("")
        for i in cambio_estado:
            a(f"- **{i}**: {pa[i]['resultado']} → **{pb[i]['resultado']}**. {pb[i]['afirmacion']}")
        a("")
    if not corregidas and not cambio_estado:
        a("Nada de lo que ya sabías ha cambiado. Ninguna afirmación se ha corregido")
        a("ni ha cambiado de estado.")
        a("")

    # ---- 2. novedades ----
    a("## 2 · Lo nuevo")
    a("")
    if nuevas:
        a(f"**{len(nuevas)} afirmaciones nuevas verificadas:**")
        a("")
        for i in nuevas:
            a(f"- **{i}** ({pb[i]['capitulo']}): {pb[i]['afirmacion']}")
        a("")
    if retiradas:
        a(f"**{len(retiradas)} retiradas:** " + ", ".join(retiradas))
        a("")
    if not nuevas and not retiradas:
        a("Sin cambios en el registro de afirmaciones.")
        a("")

    # ---- 3. módulos ----
    a("## 3 · Módulos tocados")
    a("")
    filas, nuevas_secciones, total_nuevas_palabras = [], [], 0
    for mid in sorted(mb, key=lambda x: int(x[1:])):
        antes, ahora = ma.get(mid), mb[mid]
        if antes is None:
            filas.append((mid, "**módulo nuevo**", palabras(ahora)))
            total_nuevas_palabras += palabras(ahora)
            continue
        if antes == ahora:
            continue
        sa, sb = secciones(antes), secciones(ahora)
        anadidas = [s for s in sb if s not in sa]
        quitadas = [s for s in sa if s not in sb]
        tocadas = [s for s in sb if s in sa and sa[s] != sb[s]]
        delta = palabras(ahora) - palabras(antes)
        total_nuevas_palabras += max(delta, 0)
        detalle = []
        if anadidas:
            detalle.append(f"{len(anadidas)} secciones nuevas")
            nuevas_secciones += [f"{mid} · {s}" for s in anadidas]
        if quitadas:
            detalle.append(f"{len(quitadas)} retiradas")
        if tocadas:
            detalle.append(f"{len(tocadas)} revisadas")
        filas.append((mid, ", ".join(detalle) or "cambios menores", delta))

    if filas:
        a("| Módulo | Qué cambió | Palabras |")
        a("|---|---|---:|")
        for mid, det, d in filas:
            a(f"| {mid} | {det} | {d:+d} |")
        a("")
        if nuevas_secciones:
            a("**Secciones nuevas:**")
            a("")
            for s in nuevas_secciones:
                a(f"- {s}")
            a("")
    else:
        a("Ningún módulo ha cambiado.")
        a("")

    # ---- 4. lo que cuesta ponerse al día ----
    minutos = max(1, round(total_nuevas_palabras / PALABRAS_POR_MINUTO))
    plural = "minuto" if minutos == 1 else "minutos"
    a("## 4 · Lo que te cuesta ponerte al día")
    a("")
    a(f"**{total_nuevas_palabras} palabras nuevas · unos {minutos} {plural} de lectura.**")
    a("")
    a("Esa es la promesa: no vuelves a leerte la guía, lees lo que cambió.")
    a("")
    a("---")
    a("")
    a(f"Generado con `changelog-guia.py {args.desde} {args.hasta}`. No se edita a mano.")

    texto = "\n".join(L) + "\n"
    if args.salida:
        Path(args.salida).write_text(texto, encoding="utf-8")
        print(f"{args.salida} escrito · {total_nuevas_palabras} palabras nuevas, ~{minutos} min")
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
