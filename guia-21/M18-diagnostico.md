# M18 · Diagnóstico y errores

> **Para quién es:** todos, el día malo.
> **Qué resuelve:** no perder una tarde. Es el módulo que más se consulta y el que menos se lee entero.
> **Qué NO cubre:** nada nuevo. Es transversal a toda la guía.

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 18.1 · Antes de diagnosticar nada: ya ha reintentado

Lo primero que hay que saber, porque cambia cómo se leen todos los errores:

> Claude Code **reintenta los fallos transitorios hasta diez veces con retroceso
> exponencial** antes de enseñarte un error.

Es decir: **cuando ves un mensaje, los reintentos que aplicaban ya se han hecho**.
No lo vuelvas a lanzar esperando que "esta vez pille". No siempre reintenta un
fallo que llega a mitad de la respuesta, y la documentación separa qué fallos
reciben el presupuesto completo de reintentos, cuáles uno menor y cuáles ninguno.

Sí reintenta: errores de servidor, respuestas de sobrecarga y tiempos de espera
**que llegan antes de que se haya emitido nada de la respuesta**; y conexiones
caídas a mitad de petición, incluido durante el razonamiento, reemitiendo con el
mismo retroceso.

---

## 18.2 · El procedimiento de tres pasos

Antes de leer ningún catálogo, esto descarta la mitad de los casos y cuesta dos
minutos:

1. **`claude --version`.** Anótala. Media docena de comportamientos de esta guía
   cambian según la versión, y comparar dos máquinas con versiones distintas no
   compara nada.
2. **Arranca en modo mínimo**, sin `CLAUDE.md`, sin hooks y sin plugins.
3. **Decide de quién es el problema.** Si en mínimo **no** pasa, el problema es
   tuyo y está en una de esas tres piezas. Si **sigue** pasando, es del CLI y
   merece la pena reportarlo.

Y las tres herramientas de inspección, del M3: **`/status`** para saber qué
fuentes de configuración mandan, **`/doctor`** para los errores de validación con
su origen, y **`claude doctor`** desde el terminal para un diagnóstico de solo
lectura sin abrir sesión. Añade **`/context`** para el reparto de la ventana,
**`/mcp`** para el coste por servidor y **`/hooks`** para los hooks activos.

---

## 18.3 · Tabla 14 · El catálogo completo

La documentación oficial cataloga **83 errores con su mensaje literal**, repartidos
en quince categorías. El megaprompt pedía "los ~40 más frecuentes"; hay más del
doble documentados, y saber que existe el catálogo completo vale más que
memorizar cuarenta.

| Categoría | Errores | Qué suele indicar |
|---|---:|---|
| Reintentos automáticos | 2 | Comportamiento, no fallo |
| Errores de servidor | 6 | Del otro lado. Ya se reintentó |
| Límites de uso | 5 | Créditos, cuota, 429 |
| **Autenticación** | **18** | **La categoría más poblada con diferencia** |
| Red y conexión | 6 | Proxy, TLS, política de red |
| Petición | 15 | Contexto, tamaño, modelo, políticas |
| Instalación | 2 | Descarga o proceso interrumpido |
| Línea de comandos | 13 | Banderas incompatibles, configuración ilegible |
| Plugins | 2 | Origen no confiable, integridad |
| Herramientas | 4 | Permisos y límites |
| Sesiones en segundo plano | 6 | Rutas, transcripciones, lanzador |
| Envoltorio e IDE | 1 | Salida inesperada del proceso |
| Guardado de sesión | 1 | Escrituras de transcripción fallando |
| Avisos de configuración | 2 | Confianza del espacio de trabajo |
| Rebobinado y calidad | 0 | Secciones explicativas |

💡 Que **autenticación** tenga dieciocho errores, más del doble que la siguiente
categoría, dice dónde está el dolor real de una instalación empresarial. No es el
modelo ni el contexto: es quién eres y contra qué te identificas.

---

## 18.4 · Los que más se ven, con causa y arreglo

**`Prompt is too long`.** La conversación más los archivos adjuntos superan la
ventana. `/compact` para resumir turnos anteriores, o `/clear` para empezar
limpio. ⚠️ Amazon Bedrock lo reporta como `Input is too long for requested
model.`, y **antes de v2.1.217 Claude Code no reconocía esa redacción**, así que
la autocompactación nunca se disparaba y `/compact` fallaba con el mismo error.

**`Error during compaction: Conversation too long`.** El propio `/compact` falló
porque **no queda contexto libre para alojar el resumen que produce**. Pasa cuando
la ventana ya está llena al dispararse la autocompactación. La salida es `Esc`
`Esc` para retroceder varios turnos y volver a intentarlo.

**`Agent would be spawned with zero tools`.** Todas las entradas de la lista de
herramientas del subagente fallaron al casar, así que se negó a lanzarlo: sin
herramientas no podría actuar. El mensaje **agrupa tus entradas por qué falló**:
no reconocida, normalmente una errata como `Grpe` por `Grep`, o no disponible para
subagentes.

**`File is covered by a Read deny rule`.** Se llamó a `Edit` o `Write` sobre una
ruta cubierta por una regla `deny` de lectura, incluida la creación de un archivo
nuevo ahí. Ambas herramientas cambian contenido que Claude tiene que poder releer,
así que se rechaza **antes de tocar el archivo**. `NotebookEdit` no está cubierto.
⚠️ **Antes de v2.1.228 la regla bloqueaba solo `Edit`**, y antes de v2.1.208 hacía
falta una regla `deny` de `Edit`.

**`pkill` que casa con el propio proceso.** Un `pkill`, típicamente con `-f`, cuyo
patrón casa con el proceso de Claude Code: se rechaza en vez de dejar que mate la
sesión. Lo comprueba con `pgrep` antes de ejecutar. **Solo en Linux; en macOS
`pkill` corre sin modificar.** Y **antes de v2.1.214 el comando corría**, así que
un patrón que casara mataba la sesión a media tarea.

**`Ignoring N ...` por confianza del espacio de trabajo.** Encontró reglas
`permissions.allow` o entradas `additionalDirectories` en el settings del proyecto
y **no las aplicó**, porque las reglas `allow` de proyecto requieren confianza del
espacio de trabajo. **Las reglas `deny` y `ask` no se ven afectadas**, que es
exactamente el diseño correcto: lo que restringe se aplica siempre, lo que permite
necesita tu consentimiento.

**`Diff is too large for ultrareview`.** El diff contra la rama base, incluidos
cambios sin confirmar y preparados, supera los límites. Se rechaza **antes de
arrancar la sesión en la nube**, y el dato que tranquiliza: **una revisión
rechazada no consume una ejecución gratuita ni factura créditos**. El mensaje
nombra los límites, el tamaño de tu diff y los archivos que más líneas aportan.

**`Memory index is over its read limit`.** Claude escribió en el `MEMORY.md` de la
auto memory y lo dejó por encima de sus límites de lectura, **200 líneas o 25 KB**.
La escritura funcionó, pero solo se carga hasta ese límite, **así que todo lo que
pase se descarta en cada arranque**. ⚠️ **Antes de v2.1.210 se truncaba en
silencio, sin ninguna señal en el momento de escribir.**

**`Plugin archive integrity check failed`.** La entrada del catálogo usa una
fuente `archive` con `sha256` y **el resumen del archivo descargado no casa**. Se
rechaza la instalación y **la caché de plugins no cambia**. Tres causas posibles:
el archivo cambió después de que el autor calculara el resumen, el autor puso el
resumen equivocado, o la URL sirve un archivo distinto del que el autor ancló.

**`HTTP 403 x-deny-reason: host_not_allowed`.** Una petición saliente de una
sesión en la nube bloqueada por la política de red del entorno. Puedes ver además
**un certificado TLS que no casa** con el del destino real: eso significa que **el
proxy terminó la conexión**, no el destino. **No es un problema de red del
cliente**, y perseguirlo como si lo fuera es la tarde perdida clásica.

---

## 18.5 · Rendimiento y estabilidad

La página de solución de problemas cubre, ya con Claude Code funcionando: **uso
alto de CPU o memoria**, **tablas grandes que se cortan en el terminal**, **la
autocompactación que se atasca con el error de golpeteo** que ya vimos en el M1,
**comandos que se cuelgan**, **texto corrupto en la terminal integrada de un
editor**, y **búsquedas lentas o incompletas en WSL**.

Esa última merece una nota para quien despliegue en Windows: si tu equipo trabaja
en WSL y se queja de que "no encuentra archivos que están ahí", hay una causa
documentada antes de empezar a culpar a la configuración.

---

## 18.6 · Qué reportar, y cómo

Cuando hayas llegado al paso 3 del procedimiento y el problema siga en modo
mínimo, lo que hace útil un reporte:

- **La versión exacta**, de `claude --version`.
- **El mensaje literal**, no una paráfrasis. El catálogo está organizado por
  mensaje literal precisamente por eso.
- **Que reproduce en configuración limpia**, que es lo que descarta tu entorno.
- **El proveedor y el plan**, porque medio módulo depende de eso.

---

## Checklist de verificación

- [ ] Sé que cuando veo un error los reintentos ya se hicieron.
- [ ] Hago los tres pasos antes de buscar en ningún catálogo.
- [ ] Sé usar `/status`, `/doctor`, `/context`, `/mcp` y `/hooks`.
- [ ] Sé que las reglas `deny` se aplican aunque no haya confianza del espacio de trabajo.
- [ ] Sé que una ultrareview rechazada no gasta ejecución ni créditos.
- [ ] Mi `MEMORY.md` está por debajo de 200 líneas y 25 KB.
- [ ] Reporto con versión, mensaje literal y reproducción en limpio.

## Errores típicos al diagnosticar

| Lo que se hace | Lo que habría que hacer |
|---|---|
| Relanzar el comando esperando que funcione | Ya reintentó hasta diez veces. Lee el mensaje |
| Buscar en Google la paráfrasis del error | El catálogo está indexado por **mensaje literal** |
| Culpar a la red de un `403 host_not_allowed` | Es la política del entorno cloud, no tu red |
| Tocar la configuración a ciegas | Modo mínimo primero, para saber de quién es el problema |
| Comparar dos máquinas sin mirar versiones | Media docena de comportamientos cambian por versión |
| Dar por hecho que un `allow` de proyecto se aplica | Necesita confianza del espacio de trabajo |
| Suponer que `MEMORY.md` entero se carga | 200 líneas o 25 KB, lo que llegue antes |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `errors.md` | 223.030 | Tabla 14: los 83 errores con su mensaje literal |
| `troubleshooting.md` | 11.631 | Rendimiento, estabilidad y búsqueda |
| `troubleshoot-install.md` | 60.388 | Fallos de instalación |
| `debug-your-config.md` | 23.449 | El procedimiento y las herramientas de inspección |

**Marcas pendientes:** ninguna. La tabla 14 recoge el recuento por categoría y el
detalle de los diez más frecuentes; el catálogo completo con los 83 mensajes vive
en `errors.md`, y esta guía **enlaza a él en vez de copiarlo**, porque un catálogo
copiado envejece peor que el original.
