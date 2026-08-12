# Estado y punto de continuación

**Pausa el 12 de agosto de 2026, 12:53 UTC.** Todo commiteado, árbol limpio, sin remoto.
Último commit: `20ec6ad`.

---

## Dónde está todo

| Ruta | Qué es |
|---|---|
| `D1-skill/` … `D8-boletin/` | **Bloque D**: los ocho diferenciales, terminados y verificados |
| `manuscrito/` | Esqueleto del **manual de 12 módulos** (149 €) y su módulo 01 completo |
| `guia-21/` | **Guía de referencia de 21 módulos**: Fases 0 y 1, y 16 módulos escritos |
| `evidencias/EXP-001…` | Experimento propio de inyección de prompt |
| `NOTICE-FUENTES.md` | Atribuciones. Tabla MIT pendiente de Escribano |

**Nada vive fuera de aquí** salvo las descargas de documentación, que estaban en el
scratchpad de la sesión y **se pueden perder sin problema**: el protocolo obliga a
descargarlas de nuevo al empezar cada módulo, y así salen más frescas. El
inventario de las 187 páginas sí está guardado, en `guia-21/mapeo.json` y
`guia-21/inventario.json`.

---

## Los dos productos

**Decidido en Fase 0, opción C.**

1. **Guía de referencia**, 21 módulos, ordenada por materia. Es `guia-21/`.
2. **Manual "Claude Code en producción"**, 12 módulos guiados con laboratorios
   sobre el repo feo, a **149 €**. Es `manuscrito/` más el bloque D.

La guía alimenta al manual; el manual no repite la guía.

---

## Progreso de la guía de 21 módulos

**16 de 21 módulos · 33.426 de 44.400 palabras (75 %) · 12 de 15 tablas · los 3 diagramas.**

| Escritos | Pendientes |
|---|---|
| M1, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, M13, M14, M15, M16, M17 | **M18, M19, M20, M21, M2** |

**Tablas pendientes:** 7 (en M19), 14 (en M18), 15 (en M21).

### El orden que queda, por dependencia

1. **M18 · Diagnóstico** · 1.600 palabras · **tabla 14** (los ~40 errores con su
   mensaje literal). Fuentes: `troubleshooting`, `errors`, `troubleshoot-install`,
   `debug-your-config`.
2. **M19 · Referencia rápida** · 2.200 · **tabla 7**. Fuentes: `cli-reference`,
   `commands`, `env-vars`, `tools-reference`, `glossary`.
3. **M20 · Playbooks** · 3.400 · **sin páginas fuente, hay que construirlo**. Los
   cinco recorridos, con el 20.4 como ancla: automatización nocturna desatendida
   en servidor propio.
4. **M21 · Retiradas y cambios** · 1.200 · **tabla 15**. Ya tiene material
   acumulado, ver abajo.
5. **M2 · Instalación** · 1.400 · **se escribe el último a propósito**, porque es
   el que más envejece.

### Material ya recopilado para el M21

Sale de los módulos escritos, no hay que volver a buscarlo:

- **Ultraplan retirado**, incluido `/ultraplan` y la palabra clave.
- **`/review` es ahora alias de `/code-review`**.
- **El tope de 200 subagentes por sesión se eliminó** (w32).
- **Auto mode pasa a ser el modo por defecto el 14 de agosto de 2026** en Pro, Max y Team.
- **Claude Code en Slack en retirada** en Team y Enterprise, en favor de Claude Tag.
- **API de sesiones V2 de TypeScript eliminada** en el SDK 0.3.142:
  `unstable_v2_createSession`, `unstable_v2_resumeSession`, `unstable_v2_prompt`,
  `SDKSession`, `SDKSessionOptions`.
- **`/doctor` anterior a v2.1.205** abría pantalla de solo lectura y se pulsaba `f`.
- **Antes de v2.1.219**, `default` resolvía a Opus 4.8 en varias cuentas.
- **Antes de v2.1.200**, los remotos añadidos a mitad de sesión eran de confianza.
- **Antes de v2.1.202**, cada reinvocación de skill añadía otra copia completa.
- **Antes de v2.1.211**, la comprobación de secretos en push estaba acotada a la rama por defecto.
- **Antes de v2.1.218**, las skills bifurcadas siempre bloqueaban el turno, y los
  booleanos del frontmatter solo aceptaban `true`/`false`.

---

## Correcciones al Anexo A del megaprompt, para el informe final

Tres encontradas hasta ahora, todas verificadas contra la documentación:

1. **Son seis modos de permisos, no cinco.** Falta `default`, que en el CLI se
   llama **Manual** (alias `manual`, v2.1.200+).
2. **Son ocho invalidadores de caché, no siete.** Falta **denegar una herramienta
   entera**.
3. **El Anexo llega a v2.1.224 y la máquina corre 2.1.228.** No existe digest de
   la w31 ni de la w33, así que **para todo lo posterior al 7 de agosto la única
   fuente es el changelog**, no los digests. El §2.3 del megaprompt hay que
   cambiarlo o la guía nace desfasada.

Lo que **sí** se sostiene: las 106 páginas que nombra existen todas, y los 31
eventos de hooks son exactos, ni falta ni sobra ninguno.

---

## Correcciones a material propio

Hechas y propagadas, no queda nada abierto:

- **MCP no es un peaje permanente.** Las definiciones de herramientas van
  diferidas por defecto. Corregido en lámina, skill, módulo 01 y esqueleto, y dado
  de alta como `MCP-002` en el verificador. La lámina está republicada.
- **Cinco casos en los que MCP sí vuelve a ser caro**, incluido **trabajar contra
  un gateway propio**, que es nuestro caso de uso ancla.
- **EXP-001 falsificó dos laboratorios míos.** El agente no se cree el README ni
  obedece la inyección. Los dos laboratorios están reescritos sobre lo medido.
- **El repo feo estaba lleno de chivatazos** que anunciaban que era un laboratorio.
  Retirados; el aviso vive fuera del repositorio.

---

## Estado técnico

- **Verificador:** 19 pasan, 0 fallan, 3 a revisar, 3 omitidas, contra CLI 2.1.228.
- **Sin remoto a propósito.** Ver el aviso de dos repos y un remoto antes de tocar
  git desde `/home/nombre`.
- **`NOTICE-FUENTES.md`** espera el inventario MIT de Escribano.
- **`D2-verificador/SEG-002` y `CST-001`** son pruebas con coste, no ejecutadas.

## Para retomar

Basta con decir **M18**. El protocolo es el de siempre: descargar sus páginas
fuente, escribir, listar las fuentes usadas al final del módulo, y parar.
