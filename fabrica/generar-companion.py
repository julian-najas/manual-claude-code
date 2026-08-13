#!/usr/bin/env python3
"""
Genera el companion público: una página por síntoma.

    python3 fabrica/generar-companion.py

Por qué una página por síntoma y no una sola con anclas: **las anclas no se miden**.
Una ruta propia por síntoma convierte el tráfico de búsqueda en el dato que
buscamos, que es por qué problema entra la gente. Eso decide el posicionamiento
con datos en vez de con criterio.

Fuente: los 21 módulos canónicos de `guia-21/`. Nada se escribe a mano aquí.

Salida: `companion/` con index.html, una página por síntoma, sitemap.xml y robots.txt.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "guia-21"
SALIDA = RAIZ / "companion"
BASE = "https://julian-najas.github.io/claude-code-companion"

PALABRAS_VACIAS = {
    "que", "de", "la", "el", "en", "y", "a", "los", "las", "un", "una", "no", "se",
    "me", "mi", "se", "lo", "por", "con", "para", "es", "sin", "al", "del", "su",
    "pero", "como", "más", "esto", "eso", "hay", "ya", "muy", "the",
}


def ranura(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_]+", "-", s)[:70].strip("-")


def limpiar_md(s: str) -> str:
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    return s.strip().strip('"')


def modulos() -> list[Path]:
    return sorted(FUENTE.glob("M*.md"), key=lambda p: int(p.name.split("-")[0][1:]))


def contexto(texto: str, sintoma: str, causa: str) -> str:
    """Busca en el módulo el párrafo que mejor explica este síntoma."""
    claves = {
        w for w in re.findall(r"\w{4,}", (sintoma + " " + causa).lower())
        if w not in PALABRAS_VACIAS
    }
    if not claves:
        return ""
    mejor, puntos = "", 0
    for parrafo in re.split(r"\n\s*\n", texto):
        p = parrafo.strip()
        if p.startswith(("|", "#", "```", "- [ ]", ">")) or len(p) < 120 or len(p) > 900:
            continue
        pl = p.lower()
        n = sum(1 for k in claves if k in pl)
        if n > puntos:
            mejor, puntos = p, n
    if puntos < 2:
        return ""
    p = limpiar_md(re.sub(r"\s+", " ", mejor))
    # el párrafo viene de dentro de un módulo, así que puede empezar por una
    # marca o un conector que fuera de contexto no significa nada
    p = re.sub(r"^[⚠️💡>\s]+", "", p)
    p = re.sub(r"^(Y|Pero|Además|También|Por eso|Así que|Es decir)[,:]?\s+", "", p)
    return p[0].upper() + p[1:] if p else ""


def recoger() -> list[dict]:
    out = []
    for f in modulos():
        t = f.read_text(encoding="utf-8")
        mod = f.name.split("-")[0]
        titulo_mod = t.splitlines()[0].lstrip("# ").strip()
        resuelve = re.search(r"\*\*Qué resuelve:\*\* (.+)", t)
        seg = re.split(r"^## Errores típicos.*$", t, flags=re.M)
        if len(seg) < 2:
            continue
        cuerpo = re.split(r"^---\s*$", seg[1], flags=re.M)[0]
        for s, c in re.findall(r'^\|\s*"?([^|"]+?)"?\s*\|\s*(.+?)\s*\|\s*$', cuerpo, re.M):
            if s.strip() in ("Síntoma", "Lo que se hace") or set(s.strip()) <= set("-: "):
                continue
            sintoma, causa = limpiar_md(s), limpiar_md(c)
            out.append({
                "sintoma": sintoma,
                "causa": causa,
                "modulo": mod,
                "titulo_modulo": titulo_mod,
                "resuelve": limpiar_md(resuelve.group(1)) if resuelve else "",
                "contexto": contexto(t, sintoma, causa),
                "ranura": ranura(sintoma),
            })
    # ranuras únicas
    vistas: dict[str, int] = {}
    for d in out:
        r = d["ranura"]
        if r in vistas:
            vistas[r] += 1
            d["ranura"] = f"{r}-{vistas[r]}"
        else:
            vistas[r] = 1
    return out


CSS = """
:root{--bg:#ECEEEE;--sf:#FBFCFC;--sf2:#F3F5F5;--ink:#15191B;--ink2:#4E585C;
--mut:#78838A;--rl:#D2D8D9;--br:#9A6F14;
--sr:"Charter","Bitstream Charter","Iowan Old Style",Palatino,Georgia,serif;
--sa:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
--mo:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#121516;--sf:#191D1F;
--sf2:#1E2325;--ink:#E8EAEA;--ink2:#A9B3B7;--mut:#7E888D;--rl:#2A3033;--br:#D5A442}}
:root[data-theme=dark]{--bg:#121516;--sf:#191D1F;--sf2:#1E2325;--ink:#E8EAEA;
--ink2:#A9B3B7;--mut:#7E888D;--rl:#2A3033;--br:#D5A442}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--sa);font-size:17px;
line-height:1.6;margin:0;-webkit-font-smoothing:antialiased}
.w{max-width:760px;margin:0 auto;padding:44px 20px 80px}
a{color:var(--br)}
h1{font-family:var(--sr);font-weight:600;font-size:clamp(1.6rem,5vw,2.3rem);
line-height:1.2;margin:.2em 0 .6em;text-wrap:balance}
h2{font-family:var(--sr);font-weight:600;font-size:1.2rem;margin:1.8em 0 .5em}
.eb{font-family:var(--mo);font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;
color:var(--mut);text-decoration:none}
.card{background:var(--sf);border:1px solid var(--rl);border-left:2px solid var(--br);
padding:18px 20px;margin:1.2em 0}
.card .t{font-weight:650;margin-bottom:.35em}
.card p{margin:0;color:var(--ink2)}
.meta{font-family:var(--mo);font-size:.76rem;color:var(--mut);margin-top:2.5em;
border-top:1px solid var(--rl);padding-top:14px;line-height:1.8}
input[type=search]{width:100%;padding:13px 15px;font-size:1rem;font-family:var(--sa);
background:var(--sf);color:var(--ink);border:1px solid var(--rl);border-radius:0}
input[type=search]:focus{outline:2px solid var(--br);outline-offset:1px}
ul.lista{list-style:none;padding:0;margin:1.4em 0 0}
ul.lista li{border-bottom:1px solid var(--rl)}
ul.lista a{display:block;padding:11px 2px;text-decoration:none;color:var(--ink)}
ul.lista a:hover{background:var(--sf2)}
ul.lista .m{font-family:var(--mo);font-size:.7rem;color:var(--mut);margin-left:.5em}
.cnt{font-family:var(--mo);font-size:.78rem;color:var(--mut);margin-top:.8em}
.cta{background:var(--sf2);border:1px solid var(--rl);padding:20px;margin-top:2.5em}
.cta .t{font-family:var(--sr);font-size:1.15rem;margin-bottom:.4em}
.cta p{color:var(--ink2);margin:.4em 0 0;font-size:.95rem}
"""


def envoltura(titulo: str, desc: str, cuerpo: str, canon: str) -> str:
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{html.escape(titulo)}">
<meta property="og:description" content="{html.escape(desc)}">
<style>{CSS}</style></head><body><div class="w">{cuerpo}</div></body></html>"""


PIE = """<p class="meta">
Companion público de <strong>Claude Code en producción</strong>, la guía en castellano
que se verifica contra el binario.<br>
Verificado contra Claude Code 2.1.228 · Cosas Agénticas · sin afiliación con Anthropic.
</p>"""


def pagina_sintoma(d: dict) -> str:
    ctx = f'<h2>Por qué pasa</h2><p>{html.escape(d["contexto"])}</p>' if d["contexto"] else ""
    cuerpo = f"""<a class="eb" href="./">← Índice por síntoma</a>
<h1>{html.escape(d["sintoma"])}</h1>
<div class="card"><div class="t">Qué está pasando</div><p>{html.escape(d["causa"])}</p></div>
{ctx}
<h2>Dónde se cuenta entero</h2>
<p>Esto sale del <strong>{html.escape(d["titulo_modulo"])}</strong> de la guía,
que resuelve {html.escape(d["resuelve"] or "este tipo de problema")}</p>
<div class="cta"><div class="t">La guía completa</div>
<p>21 módulos, 15 tablas de referencia y 156 síntomas como este, todos con su causa.
Cada afirmación crítica se ejecuta contra el binario instalado y el resultado se
publica, se vea bien o se vea mal.</p>
<p><a href="./">Ver los 156 síntomas</a></p></div>
{PIE}"""
    desc = f"{d['sintoma']} — {d['causa'][:120]}"
    return envoltura(f"{d['sintoma']} · Claude Code", desc, cuerpo,
                     f"{BASE}/{d['ranura']}/")


def pagina_indice(ds: list[dict]) -> str:
    items = "".join(
        f'<li data-t="{html.escape((d["sintoma"]+" "+d["causa"]).lower())}">'
        f'<a href="{d["ranura"]}/">{html.escape(d["sintoma"])}'
        f'<span class="m">{d["modulo"]}</span></a></li>'
        for d in ds
    )
    cuerpo = f"""<p class="eb">Claude Code en producción</p>
<h1>Índice por síntoma</h1>
<p>Busca <strong>lo que te pasa</strong>, no lo que crees que es. {len(ds)} síntomas
reales con su causa, extraídos de los 21 módulos de la guía.</p>
<input type="search" id="q" placeholder="mi skill no se activa, se me acaba el contexto…"
 autocomplete="off" aria-label="Buscar síntoma">
<p class="cnt" id="c">{len(ds)} síntomas</p>
<ul class="lista" id="l">{items}</ul>
<div class="cta"><div class="t">¿Por qué existe esto?</div>
<p>Porque Claude Code publica versiones casi a diario y un manual estático envejece
en silencio. Este índice sale de una guía cuyas afirmaciones se ejecutan cada
madrugada contra el binario real, y cuyo resultado es público.</p></div>
{PIE}
<script>
const q=document.getElementById('q'),l=document.getElementById('l'),c=document.getElementById('c');
const items=[...l.children];
q.addEventListener('input',()=>{{
  const v=q.value.toLowerCase().trim();let n=0;
  for(const it of items){{const ok=!v||it.dataset.t.includes(v);it.hidden=!ok;if(ok)n++;}}
  c.textContent=v?n+' de {len(ds)} síntomas':'{len(ds)} síntomas';
}});
</script>"""
    return envoltura(
        "Índice por síntoma · Claude Code en producción",
        f"{len(ds)} síntomas reales de Claude Code con su causa: skills que no se activan, "
        "contexto que se agota, hooks que no disparan, permisos, MCP y coste.",
        cuerpo, f"{BASE}/")


def main() -> int:
    ds = recoger()
    if SALIDA.exists():
        shutil.rmtree(SALIDA)
    SALIDA.mkdir(parents=True)

    (SALIDA / "index.html").write_text(pagina_indice(ds), encoding="utf-8")
    for d in ds:
        carpeta = SALIDA / d["ranura"]
        carpeta.mkdir()
        (carpeta / "index.html").write_text(pagina_sintoma(d), encoding="utf-8")

    urls = "".join(f"<url><loc>{BASE}/{d['ranura']}/</loc></url>" for d in ds)
    (SALIDA / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"<url><loc>{BASE}/</loc></url>{urls}</urlset>",
        encoding="utf-8")
    (SALIDA / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    (SALIDA / ".nojekyll").write_text("", encoding="utf-8")
    (SALIDA / "sintomas.json").write_text(
        json.dumps(ds, ensure_ascii=False, indent=1), encoding="utf-8")

    con_ctx = sum(1 for d in ds if d["contexto"])
    print(f"companion generado en {SALIDA.name}/")
    print(f"  {len(ds)} páginas de síntoma · {con_ctx} con explicación del módulo "
          f"({100*con_ctx//len(ds)} %)")
    print(f"  índice con buscador · sitemap con {len(ds)+1} URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
