#!/usr/bin/env python3
"""Regenera INDICE-SINTOMAS.md a partir de las tablas de errores típicos de los módulos."""
import re, pathlib, sys
B = pathlib.Path(__file__).resolve().parent
mods = sorted((B/"modulos").glob("M*.md"), key=lambda x: int(x.name.split('-')[0][1:]))
if not mods:
    sys.exit("No encuentro los módulos en modulos/")
filas = []
for f in mods:
    t = f.read_text(encoding='utf-8'); mod = f.name.split('-')[0]
    seg = re.split(r'^## Errores típicos.*$', t, flags=re.M)
    if len(seg) < 2:
        continue
    cuerpo = re.split(r'^---\s*$', seg[1], flags=re.M)[0]
    for s, c in re.findall(r'^\|\s*"?([^|"]+?)"?\s*\|\s*(.+?)\s*\|\s*$', cuerpo, re.M):
        if s.strip() in ('Síntoma', 'Lo que se hace') or set(s.strip()) <= set('-: '):
            continue
        filas.append((s.strip(), c.strip(), mod))
L = ["# Índice por síntoma", "",
     f"**{len(filas)} síntomas** extraídos de las tablas de errores típicos de los 21 módulos.",
     "Generado, no escrito a mano: si un módulo cambia su tabla, este índice se regenera.", "",
     "Busca lo que te pasa, no lo que crees que es.", "",
     "| Síntoma | Qué está pasando | Módulo |", "|---|---|---|"]
L += [f"| {s} | {c} | [{m}](modulos/) |" for s, c, m in filas]
L += ["", "---", "", "Regenerar: `python3 generar-indice.py`"]
(B/"INDICE-SINTOMAS.md").write_text("\n".join(L), encoding='utf-8')
print(f"INDICE-SINTOMAS.md regenerado: {len(filas)} síntomas de {len(mods)} módulos")
