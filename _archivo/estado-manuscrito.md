# Estado del manuscrito

Una entrada por iteración. Dos líneas: qué se cerró y qué queda.

## Próxima iteración · Módulo 03 · Memoria y contexto

**No empezado.** La iteración del 17-ago se cortó por límite de uso antes de
escribir una línea, y no se dejó un módulo a medias a propósito.

Preparación ya hecha, para no repetirla:

- Fuente principal: `guia-21/M4-memoria-y-contexto.md`, leído y utilizable.
- Contrato: sección "Módulo 03" de `manuscrito/ESQUELETO.md`. IDs ya en el
  registro: `CTX-001` (`--add-dir`), `CTX-002` (`--autocompact`), `CTX-003`
  (`--bare`). Habrá que añadir entradas nuevas.
- Documentación oficial **pendiente de descargar de nuevo** (la regla es
  descargarla en cada módulo, no reutilizar la de otra sesión):
  `memory.md`, `context-window.md`, `claude-directory.md`, `settings.md`.
- Laboratorio: `D6-repo-feo/gestor-pedidos`, que ya tiene `.claude/settings.json`
  y `ENTORNO.md` del módulo 02. El `CLAUDE.md` lo escribe este módulo.
- **La trampa del laboratorio, ya documentada como hecho canónico
  `CONFIG-NINGUNO-SE-USA`:** la respuesta a "qué configuración manda" es
  **ninguna de las dos**. Ni `config.py` ni `settings.py` se importan; `app.py`
  fija sus valores a mano (`DB`, `DEBUG`, el IVA y el tope de 50 líneas). El
  módulo tiene que llevar al lector hasta ahí, no hasta "manda settings.py".
- El código muerto que el `CLAUDE.md` debe declarar: `/pedido_old/<id>`, que lee
  la tabla `pedidos_2019` (fallo 6 del guion de doma).

## 2026-08-17 · Módulo 02 · Instalación, autenticación y versiones

Cerrado `manuscrito/modulo-02-instalacion.md`, 3.849 palabras, las seis partes
del esqueleto y runbook de una página. Verificador en verde: **30 pasan, 0
fallan, 5 a revisar, 3 omitidas** contra 2.1.233. Quedan diez módulos: 03 a 12.

Añadidas al registro nueve entradas nuevas (CLI-004 a CLI-010, AUT-001, ENT-001,
ENT-002). Las cinco amarillas son manuales justificadas: HOK-001, MCP-002,
TRB-002 (trimestrales de siempre) y las dos nuevas, CLI-010 y AUT-001.

**Hallazgos propios del módulo, no copiados de la guía de 21:**

- `claude doctor` **termina en 0 aunque reporte `Invalid settings`**, y sigue
  imprimiendo `No installation issues found`. Una comprobación de CI que mire
  solo el código de salida da verde con la configuración del proyecto rota.
- Un nombre de clave mal escrito en `settings.json` **no se reporta en
  absoluto**. Los valores inválidos de claves conocidas sí, y con detalle.
- El binario acepta un tercer canal, **`rc`**, que no aparece en `setup.md` ni
  en `settings.md`. Marcado en caja "esto va a cambiar", no recomendado.
- La precedencia de credenciales **eran cuatro niveles en nuestra guía y hoy son
  siete**. Corregido en el manuscrito y anotado como recuento trimestral.
- `--help` es **byte a byte idéntico entre 2.1.228 y 2.1.233** (242 líneas),
  mientras la documentación condiciona comportamiento a 14 versiones distintas.
  Eso reorienta el módulo entero: la versión no quita comandos, cambia lo que
  hacen.

**Laboratorio:** `D6-repo-feo/gestor-pedidos` gana `.claude/settings.json` y
`ENTORNO.md`. Verificado que el archivo se carga de verdad: `claude doctor`
dentro del repo dice `Auto-update channel: stable` y fuera dice `latest`. Ese
contraste es el criterio PASA del módulo.

**Bookkeeping:** `fabrica/hechos.yaml` y `README.md` pasan de "1 de 12" a
"2 de 12". Coherencia y `construir.py --comprobar`, las dos en verde.

### PARA JULIÁN

1. **La fecha de corte del libro.** El esqueleto y el módulo 01 dicen "verificado
   contra 2.1.228, corte 12-ago-2026". La máquina va por la 2.1.233 y el
   verificador lleva días publicando estado contra 2.1.231, 2.1.232 y 2.1.233.
   El módulo 02 se ha escrito contra la 2.1.233 y lo declara en su cabecera, en
   vez de fingir. Decisión tuya: **recortar el libro entero a la versión del día
   de publicación** (tocar el esqueleto, el módulo 01 y la página de
   verificación), o **dejar el corte en 2.1.228 y que cada módulo declare la
   suya**. No lo he decidido yo porque afecta a la portada.
2. **El orden de escritura.** El esqueleto recomienda escribir el 02 el último
   ("es el que más envejece"). La orden del bucle es por número, así que va el
   segundo. No lo he cambiado, pero el módulo 02 va a necesitar un repaso corto
   justo antes de publicar, y conviene que esté presupuestado.
