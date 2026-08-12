#!/usr/bin/env python3
"""
Analiza la telemetría real de una operación multiagente y saca los números
del capítulo "La factura".

Lee los registros JSONL de uso (una línea por llamada a la API) y responde a
las preguntas que nadie se hace hasta que llega el recibo:

  - ¿Cuántos tokens entran por cada token que sale?
  - ¿Cuánto de la factura se va en llamadas cuya respuesta cabe en un tuit?
  - ¿Cuánto pesa el contexto que arrastramos sin darnos cuenta?

No inventa precios. Los tokens son medidos; los euros solo aparecen si se
pasa una tabla de precios con --precios.

Uso:
    python3 analizar_gasto.py ~/.hermes/logs/usage_*.jsonl
    python3 analizar_gasto.py --precios precios.json ~/.hermes/logs/*.jsonl
"""

from __future__ import annotations

import argparse
import glob
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Una respuesta por debajo de este tamaño es, en la práctica, un "vale".
UMBRAL_RESPUESTA_CORTA = 50


def cargar(patrones: list[str]) -> list[dict]:
    filas = []
    for patron in patrones:
        for ruta in sorted(glob.glob(str(Path(patron).expanduser()))):
            with open(ruta, encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    try:
                        filas.append(json.loads(linea))
                    except json.JSONDecodeError:
                        continue
    return filas


def n(fila: dict, *claves: str) -> int:
    for k in claves:
        v = fila.get(k)
        if isinstance(v, (int, float)):
            return int(v)
    return 0


def analizar(filas: list[dict]) -> dict:
    total_entrada = total_salida = total_cache_lectura = total_cache_escritura = 0
    cortas_entrada = cortas_salida = cortas_n = 0
    por_modelo: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    por_proveedor: Counter = Counter()
    sesiones: set[str] = set()
    fechas: list[str] = []

    for f in filas:
        entrada = n(f, "input_tokens", "prompt_tokens")
        salida = n(f, "output_tokens", "completion_tokens")
        total_entrada += entrada
        total_salida += salida
        total_cache_lectura += n(f, "cache_read_tokens")
        total_cache_escritura += n(f, "cache_write_tokens")

        modelo = str(f.get("model_id") or f.get("response_model") or "desconocido")
        por_modelo[modelo]["llamadas"] += 1
        por_modelo[modelo]["entrada"] += entrada
        por_modelo[modelo]["salida"] += salida
        por_proveedor[str(f.get("provider") or "desconocido")] += 1

        if f.get("session_id"):
            sesiones.add(str(f["session_id"]))
        if f.get("ts"):
            fechas.append(str(f["ts"])[:10])

        if 0 < salida <= UMBRAL_RESPUESTA_CORTA:
            cortas_n += 1
            cortas_entrada += entrada
            cortas_salida += salida

    return {
        "llamadas": len(filas),
        "sesiones": len(sesiones),
        "desde": min(fechas) if fechas else "",
        "hasta": max(fechas) if fechas else "",
        "entrada": total_entrada,
        "salida": total_salida,
        "cache_lectura": total_cache_lectura,
        "cache_escritura": total_cache_escritura,
        "ratio": (total_entrada / total_salida) if total_salida else 0,
        "cortas_n": cortas_n,
        "cortas_entrada": cortas_entrada,
        "cortas_salida": cortas_salida,
        "cortas_pct_llamadas": (100 * cortas_n / len(filas)) if filas else 0,
        "cortas_pct_entrada": (100 * cortas_entrada / total_entrada) if total_entrada else 0,
        "media_entrada": (total_entrada / len(filas)) if filas else 0,
        "media_salida": (total_salida / len(filas)) if filas else 0,
        "por_modelo": {k: dict(v) for k, v in por_modelo.items()},
        "por_proveedor": dict(por_proveedor),
    }


def euros(a: dict, precios: dict) -> dict | None:
    """Precios en euros por millón de tokens: {"modelo": {"entrada": x, "salida": y}}."""
    if not precios:
        return None
    total = corto = 0.0
    for modelo, d in a["por_modelo"].items():
        p = precios.get(modelo) or precios.get("*")
        if not p:
            continue
        total += d["entrada"] / 1e6 * p["entrada"] + d["salida"] / 1e6 * p["salida"]
    p = precios.get("*")
    if p:
        corto = a["cortas_entrada"] / 1e6 * p["entrada"] + a["cortas_salida"] / 1e6 * p["salida"]
    return {"total_eur": total, "respuestas_cortas_eur": corto}


def informe(a: dict, dinero: dict | None) -> str:
    L = []
    ad = L.append
    ad("=" * 66)
    ad("  LA FACTURA · telemetría real de una operación multiagente")
    ad("=" * 66)
    ad(f"  Periodo          {a['desde']} a {a['hasta']}")
    ad(f"  Llamadas a la API{a['llamadas']:>14,}".replace(",", "."))
    ad(f"  Sesiones         {a['sesiones']:>14,}".replace(",", "."))
    ad("")
    ad("  TOKENS")
    ad(f"  Entrada          {a['entrada']:>14,}".replace(",", "."))
    ad(f"  Salida           {a['salida']:>14,}".replace(",", "."))
    ad(f"  Caché leída      {a['cache_lectura']:>14,}".replace(",", "."))
    ad(f"  Caché escrita    {a['cache_escritura']:>14,}".replace(",", "."))
    ad("")
    ad(f"  >>> Por cada token que sale, entran {a['ratio']:.0f}.")
    ad(f"      Media por llamada: {a['media_entrada']:,.0f} de entrada, "
       f"{a['media_salida']:,.0f} de salida.".replace(",", "."))
    ad("")
    ad(f"  EL COSTE DE LA CORTESÍA (respuestas de {UMBRAL_RESPUESTA_CORTA} tokens o menos)")
    ad(f"  Llamadas         {a['cortas_n']:>14,}".replace(",", ".")
       + f"   ({a['cortas_pct_llamadas']:.1f} % del total)")
    ad(f"  Tokens de entrada{a['cortas_entrada']:>14,}".replace(",", ".")
       + f"   ({a['cortas_pct_entrada']:.1f} % de toda la entrada)")
    ad(f"  Tokens de salida {a['cortas_salida']:>14,}".replace(",", "."))
    ad("")
    ad("  MODELOS")
    for modelo, d in sorted(a["por_modelo"].items(), key=lambda x: -x[1]["llamadas"]):
        ad(f"  {modelo:<26} {d['llamadas']:>6,} llamadas  "
           f"{d['entrada']:>13,} entrada  {d['salida']:>10,} salida".replace(",", "."))
    ad("")
    ad("  PROVEEDORES")
    for prov, c in sorted(a["por_proveedor"].items(), key=lambda x: -x[1]):
        ad(f"  {prov:<26} {c:>6,} llamadas".replace(",", "."))
    if dinero:
        ad("")
        ad("  EUROS (calculados con la tabla de precios aportada)")
        ad(f"  Total estimado                 {dinero['total_eur']:>10,.2f} €".replace(",", "."))
        ad(f"  Solo respuestas cortas         {dinero['respuestas_cortas_eur']:>10,.2f} €".replace(",", "."))
    else:
        ad("")
        ad("  Sin tabla de precios: los tokens son medidos, los euros no se inventan.")
        ad("  Pasa --precios precios.json para convertirlos.")
    ad("=" * 66)
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="Saca los números del capítulo de la factura.")
    ap.add_argument("registros", nargs="+", help="rutas o patrones de archivos .jsonl")
    ap.add_argument("--precios", help="JSON con euros por millón de tokens y modelo")
    ap.add_argument("--json", action="store_true", help="vuelca el análisis en JSON")
    args = ap.parse_args()

    filas = cargar(args.registros)
    if not filas:
        print("No he encontrado ninguna llamada en esos registros.", file=sys.stderr)
        return 1

    a = analizar(filas)
    precios = json.loads(Path(args.precios).read_text(encoding="utf-8")) if args.precios else {}
    dinero = euros(a, precios)

    if args.json:
        print(json.dumps({"analisis": a, "euros": dinero}, ensure_ascii=False, indent=2))
    else:
        print(informe(a, dinero))
    return 0


if __name__ == "__main__":
    sys.exit(main())
