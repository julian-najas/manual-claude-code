#!/usr/bin/env python3
"""
Valida `estado.json` y regenera desde él el Markdown y el HTML.

    python3 D2-verificador/regenerar-desde-estado.py

Por qué existe: el trabajo que verifica **instala Claude Code desde un script
remoto**, así que todo lo que produce es material que no controlamos del todo.
El trabajo que publica, que sí tiene permiso de escritura, no debe aceptar HTML
ni Markdown venidos de ahí: solo acepta **un JSON, lo valida contra un esquema
estricto, y vuelve a renderizar** con el código de este repositorio.

Así, aunque el instalador remoto se comprometiera algún día, lo peor que podría
colar es un JSON con datos falsos, no marcado arbitrario en una página publicada.

Salida: 0 si el JSON es válido y se regeneró todo; 1 si no lo es.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ESTADOS = {"PASA", "FALLA", "REVISAR", "OMITIDO"}
# nada de rutas, comandos ni salidas: solo lo que se muestra
LARGO_MAX = 400


def error(msg: str) -> int:
    print(f"estado.json inválido: {msg}", file=sys.stderr)
    return 1


def validar(d: object) -> str | None:
    if not isinstance(d, dict):
        return "la raíz no es un objeto"
    for clave in ("libro", "version_libro", "cli_verificado", "sistema", "fecha_utc",
                  "resumen", "pruebas"):
        if clave not in d:
            return f"falta la clave {clave!r}"
    if not isinstance(d["resumen"], dict) or set(d["resumen"]) != ESTADOS:
        return "el resumen no tiene exactamente los cuatro estados"
    if not all(isinstance(v, int) and v >= 0 for v in d["resumen"].values()):
        return "el resumen tiene valores que no son enteros positivos"
    if not isinstance(d["pruebas"], list) or not d["pruebas"]:
        return "no hay pruebas"
    if len(d["pruebas"]) > 500:
        return "demasiadas pruebas, algo va mal"
    for i, p in enumerate(d["pruebas"]):
        if not isinstance(p, dict):
            return f"la prueba {i} no es un objeto"
        for clave in ("id", "capitulo", "afirmacion", "resultado"):
            if not isinstance(p.get(clave), str):
                return f"la prueba {i} no tiene {clave} como texto"
        if p["resultado"] not in ESTADOS:
            return f"la prueba {p['id']} tiene un resultado desconocido"
        if not re.fullmatch(r"[A-Z]{3,6}-\d{3}", p["id"]):
            return f"el identificador {p['id']!r} no tiene la forma XXX-000"
        for clave in ("afirmacion", "capitulo", "motivo", "comando"):
            if len(str(p.get(clave, ""))) > LARGO_MAX:
                return f"la prueba {p['id']} tiene {clave} sospechosamente largo"
    contados = {e: sum(1 for p in d["pruebas"] if p["resultado"] == e) for e in ESTADOS}
    if contados != d["resumen"]:
        return f"el resumen no cuadra con las pruebas: {d['resumen']} frente a {contados}"
    return None


def main() -> int:
    ruta = RAIZ / "estado.json"
    if not ruta.exists():
        return error("no existe")
    try:
        d = json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as ex:
        return error(f"no parsea: {ex}")

    fallo = validar(d)
    if fallo:
        return error(fallo)

    # se renderiza con el código de ESTE repositorio, no con nada que venga del
    # trabajo anterior
    sys.path.insert(0, str(RAIZ))
    from importlib.machinery import SourceFileLoader

    verif = SourceFileLoader("verif", str(RAIZ / "verificar.py")).load_module()
    (RAIZ / "ESTADO.md").write_text(verif.render_markdown(d), encoding="utf-8")

    web = SourceFileLoader("web", str(RAIZ / "generar-estado-web.py")).load_module()
    (RAIZ / "estado.html").write_text(web.render(d), encoding="utf-8")

    r = d["resumen"]
    print(f"estado.json válido · {len(d['pruebas'])} pruebas · "
          f"{r['PASA']} pasan, {r['FALLA']} fallan")
    print("ESTADO.md y estado.html regenerados desde el JSON validado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
