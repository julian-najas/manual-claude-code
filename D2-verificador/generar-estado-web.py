#!/usr/bin/env python3
"""
Genera la página pública de estado a partir de estado.json.

    python3 verificar.py && python3 generar-estado-web.py

Produce `estado.html`, autocontenido y sin dependencias externas, listo para
publicar. Lo regenera la CI después de cada pasada del verificador.
"""

from __future__ import annotations

import html
import json
import sys
from collections import OrderedDict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ENTRADA = RAIZ / "estado.json"
SALIDA = RAIZ / "estado.html"

ICONO = {"PASA": "🟢", "FALLA": "🔴", "REVISAR": "🟡", "OMITIDO": "⚪"}
CLASE = {"PASA": "ok", "FALLA": "mal", "REVISAR": "rev", "OMITIDO": "omi"}


def cargar() -> dict:
    if not ENTRADA.exists():
        sys.exit(f"No encuentro {ENTRADA}. Ejecuta antes: python3 verificar.py")
    return json.loads(ENTRADA.read_text(encoding="utf-8"))


def por_capitulo(pruebas: list[dict]) -> "OrderedDict[str, list[dict]]":
    d: OrderedDict[str, list[dict]] = OrderedDict()
    for p in sorted(pruebas, key=lambda x: x.get("capitulo", "")):
        d.setdefault(p.get("capitulo", "sin capítulo"), []).append(p)
    return d


def e(s) -> str:
    return html.escape(str(s or ""))


def render(inf: dict) -> str:
    r = inf["resumen"]
    total_ejec = r["PASA"] + r["FALLA"]
    pct = (100 * r["PASA"] / total_ejec) if total_ejec else 0
    hay_fallo = r["FALLA"] > 0

    filas = []
    for cap, ps in por_capitulo(inf["pruebas"]).items():
        estado_cap = "mal" if any(x["resultado"] == "FALLA" for x in ps) else "ok"
        filas.append(
            f'<tr class="cap {estado_cap}"><td colspan="4">{e(cap)}</td></tr>'
        )
        for p in ps:
            res = p["resultado"]
            detalle = p["comando"] or p["motivo"]
            filas.append(
                f'<tr class="{CLASE[res]}">'
                f'<td class="ic">{ICONO[res]}</td>'
                f'<td class="id">{e(p["id"])}</td>'
                f'<td>{e(p["afirmacion"])}</td>'
                f'<td class="cmd">{e(detalle)}</td></tr>'
            )

    return f"""<title>Estado de verificación · Claude Code en producción</title>
<style>
  :root{{
    --bg:#ECEEEE; --surface:#FBFCFC; --surface-2:#F3F5F5;
    --ink:#15191B; --ink-2:#4E585C; --muted:#78838A; --rule:#D2D8D9;
    --brass:#9A6F14; --ok:#2F6B4F; --mal:#A33A2E; --rev:#8A6A12;
    --serif:"Charter","Bitstream Charter","Iowan Old Style",Palatino,Georgia,serif;
    --sans:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
    --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  }}
  @media (prefers-color-scheme:dark){{
    :root:not([data-theme="light"]){{
      --bg:#121516; --surface:#191D1F; --surface-2:#1E2325;
      --ink:#E8EAEA; --ink-2:#A9B3B7; --muted:#7E888D; --rule:#2A3033;
      --brass:#D5A442; --ok:#6FBF95; --mal:#D98873; --rev:#D5A442;
    }}
  }}
  :root[data-theme="dark"]{{
    --bg:#121516; --surface:#191D1F; --surface-2:#1E2325;
    --ink:#E8EAEA; --ink-2:#A9B3B7; --muted:#7E888D; --rule:#2A3033;
    --brass:#D5A442; --ok:#6FBF95; --mal:#D98873; --rev:#D5A442;
  }}
  body{{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}}
  .wrap{{max-width:900px;margin:0 auto;padding:52px 20px 80px;display:flex;flex-direction:column;gap:34px}}
  @media(max-width:640px){{.wrap{{padding:30px 14px 56px;gap:26px}}}}
  h1,h2{{font-family:var(--serif);font-weight:600;margin:0;line-height:1.15;text-wrap:balance}}
  h1{{font-size:clamp(1.8rem,5.4vw,2.5rem);letter-spacing:-.015em}}
  h2{{font-size:1.25rem}}
  p{{margin:0}}
  .eyebrow{{font-family:var(--mono);font-size:.71rem;letter-spacing:.15em;text-transform:uppercase;color:var(--muted)}}
  .veredicto{{background:var(--surface);border:1px solid var(--rule);border-top:3px solid var(--{'mal' if hay_fallo else 'ok'});padding:26px 24px;display:flex;flex-direction:column;gap:16px}}
  .titular{{font-family:var(--serif);font-size:clamp(1.4rem,4.4vw,1.9rem);line-height:1.2}}
  .titular .n{{color:var(--{'mal' if hay_fallo else 'ok'})}}
  .meta{{font-family:var(--mono);font-size:.78rem;color:var(--muted);line-height:1.8}}
  .cifras{{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:1px;background:var(--rule);border:1px solid var(--rule)}}
  .cifra{{background:var(--surface);padding:14px 16px;display:flex;flex-direction:column;gap:2px}}
  .cifra .v{{font-family:var(--serif);font-size:1.8rem;font-variant-numeric:tabular-nums;line-height:1}}
  .cifra .k{{font-family:var(--mono);font-size:.68rem;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}}
  .cifra.ok .v{{color:var(--ok)}} .cifra.mal .v{{color:var(--mal)}} .cifra.rev .v{{color:var(--rev)}}
  .scroller{{overflow-x:auto;border:1px solid var(--rule);background:var(--surface)}}
  table{{border-collapse:collapse;width:100%;min-width:620px;font-size:.88rem}}
  th,td{{text-align:left;padding:9px 12px;border-bottom:1px solid var(--rule);vertical-align:top}}
  thead th{{font-family:var(--mono);font-size:.67rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:500;background:var(--surface-2)}}
  tr.cap td{{background:var(--surface-2);font-family:var(--mono);font-size:.71rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}}
  tr.cap.mal td{{color:var(--mal)}}
  td.ic{{width:1.6rem;text-align:center}}
  td.id{{font-family:var(--mono);font-size:.76rem;color:var(--muted);white-space:nowrap}}
  td.cmd{{font-family:var(--mono);font-size:.74rem;color:var(--ink-2)}}
  tbody tr:last-child td{{border-bottom:none}}
  .nota{{background:var(--surface);border-left:2px solid var(--brass);padding:15px 18px;display:flex;flex-direction:column;gap:6px}}
  .nota .t{{font-weight:650}}
  .nota p{{color:var(--ink-2);font-size:.93rem}}
  footer{{border-top:1px solid var(--rule);padding-top:16px;font-family:var(--mono);font-size:.74rem;color:var(--muted);line-height:1.8}}
</style>

<div class="wrap">
  <header>
    <p class="eyebrow">Estado de verificación</p>
    <h1>{e(inf['libro'])}</h1>
  </header>

  <div class="veredicto">
    <p class="titular">De las {total_ejec} afirmaciones comprobables de este libro,
      <span class="n">{r['PASA']} siguen siendo ciertas</span> hoy.</p>
    <p class="meta">
      Verificado contra <strong>{e(inf['cli_verificado'])}</strong><br>
      {e(inf['fecha_utc'])} · {e(inf['sistema'])} · versión del libro {e(inf['version_libro'])}
    </p>
  </div>

  <div class="cifras">
    <div class="cifra ok"><span class="v">{r['PASA']}</span><span class="k">Pasan</span></div>
    <div class="cifra mal"><span class="v">{r['FALLA']}</span><span class="k">Fallan</span></div>
    <div class="cifra rev"><span class="v">{r['REVISAR']}</span><span class="k">A revisar</span></div>
    <div class="cifra"><span class="v">{r['OMITIDO']}</span><span class="k">Omitidas</span></div>
    <div class="cifra"><span class="v">{pct:.0f}%</span><span class="k">Vigencia</span></div>
  </div>

  <section>
    <h2>Afirmación por afirmación</h2>
    <div class="scroller">
      <table>
        <thead><tr><th></th><th>ID</th><th>Lo que dice el libro</th><th>Cómo se comprueba</th></tr></thead>
        <tbody>
          {chr(10).join(filas)}
        </tbody>
      </table>
    </div>
  </section>

  <div class="nota">
    <span class="t">Qué significa cada estado</span>
    <p><strong>🟢 Pasa:</strong> se ha ejecutado contra el CLI instalado y es cierto.
       <strong>🔴 Falla:</strong> ha dejado de ser cierto y el capítulo necesita corrección.
       <strong>🟡 A revisar:</strong> solo lo puede comprobar una persona, por ejemplo en una máquina limpia.
       <strong>⚪ Omitida:</strong> es destructiva y no se ejecuta nunca, o gasta dinero y se lanza a mano
       en la revisión trimestral.</p>
  </div>

  <div class="nota">
    <span class="t">Por qué existe esta página</span>
    <p>Claude Code publica versiones casi a diario. Un PDF estático envejece en silencio.
       Esta página la genera un script que ejecuta las afirmaciones del libro contra el CLI
       real, todos los días, y publica el resultado se vea bien o se vea mal.</p>
  </div>

  <footer>
    Generada automáticamente por <code>generar-estado-web.py</code> a partir de
    <code>estado.json</code>. No se edita a mano.<br>
    Cosas Agénticas · sin afiliación con Anthropic. Claude y Claude Code son marcas de Anthropic PBC.
  </footer>
</div>
"""


def main() -> int:
    inf = cargar()
    SALIDA.write_text(render(inf), encoding="utf-8")
    r = inf["resumen"]
    print(f"{SALIDA.name} generado · {r['PASA']} pasan, {r['FALLA']} fallan, "
          f"{r['REVISAR']} a revisar, {r['OMITIDO']} omitidas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
