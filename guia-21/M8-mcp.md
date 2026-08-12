# M8 · MCP a fondo

> **Para quién es:** quien conecta Claude Code con sistemas de la empresa.
> **Qué resuelve:** integrar sin regalar contexto ni permisos, y sin que la factura suba sin que te enteres.
> **Qué NO cubre:** construir servidores desde el SDK (M17) ni la política de datos (M16).

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 8.1 · Los cuatro transportes

| Transporte | Cuándo | Cómo se añade |
|---|---|---|
| **stdio** | Servidor local, un proceso en tu máquina | `claude mcp add` con el comando |
| **HTTP** | Servidor remoto, lo más común hoy | `--transport http` con la URL |
| **SSE** | Servidor remoto con eventos del servidor | `--transport sse` |
| **WebSocket** | Remoto bidireccional | `--transport ws` |

Dos comportamientos que conviene dar por hechos y no reinventar: hay
**actualización dinámica de herramientas**, así que un servidor puede cambiar su
catálogo en caliente, y hay **reconexión automática**. También se puede
**desactivar un servidor sin borrarlo**, que es lo que quieres al depurar en vez
de andar recortando el archivo.

---

## 8.2 · Ámbitos y precedencia

### Tabla 9 · Ámbitos de MCP

| Ámbito | Dónde vive | Quién lo ve | Cuándo usarlo |
|---|---|---|---|
| **Local** | `~/.claude.json`, por proyecto | Solo tú, solo en ese proyecto | Pruebas y credenciales personales |
| **Proyecto** | `.mcp.json` en el repositorio | Todo el equipo, va a git | Servidores que el proyecto necesita |
| **Usuario** | `~/.claude.json` | Tú, en todos tus proyectos | Tus herramientas de siempre |
| **De plugin** | Dentro del plugin | Quien instale el plugin | Reparto a escala de equipo |
| **Conectores de claude.ai** | Tu cuenta | Tú, en todas las superficies | Servicios ya conectados en la web |

**La precedencia**, cuando el mismo servidor está definido en más de un sitio:

1. Local · 2. Proyecto · 3. Usuario · 4. De plugin · 5. Conectores de claude.ai

⚠️ Dos detalles que se pagan caros si se ignoran:

- **Se usa la entrada entera de la fuente que gana. Los campos no se fusionan
  entre ámbitos.** No puedes definir la URL en el proyecto y la cabecera de
  autenticación en local: o una o la otra.
- **Los tres primeros ámbitos detectan duplicados por nombre. Los plugins y los
  conectores, por endpoint.** Así que un plugin que apunte a la misma URL que un
  servidor tuyo se trata como duplicado aunque se llame distinto.

### Variables de entorno en `.mcp.json`

Es lo que hace que un `.mcp.json` se pueda confirmar en git sin meter secretos:

- `${VAR}` se expande al valor de la variable
- `${VAR:-porDefecto}` usa el valor si existe, y si no el de reserva

Se expanden en `command`, `args`, `env`, `url` y `headers`.

```json
{
  "mcpServers": {
    "api-interna": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.empresa.com}/mcp",
      "headers": { "Authorization": "Bearer ${API_TOKEN}" }
    }
  }
}
```

Esa es la forma correcta de compartir configuración de MCP en un equipo: la
estructura va a git, los valores viven en el entorno de cada uno.

---

## 8.3 · Tool search, o por qué MCP ya no es el peaje que era

Esta sección corrige un error que este mismo proyecto tenía publicado, así que va
con todo el detalle.

**Tool search está activado por defecto.** Al arrancar la sesión solo se cargan
**los nombres de las herramientas y las instrucciones del servidor**; los esquemas
completos se difieren y Claude usa una herramienta de búsqueda para traer los
relevantes cuando la tarea los necesita. **Solo entran en contexto las que
realmente usa.**

Consecuencia directa: **añadir más servidores MCP tiene un impacto mínimo en tu
ventana de contexto**, y **no hay un tope fijo de herramientas por servidor**. El
límite práctico es tu presupuesto de contexto.

### Cuándo deja de estar activado, que es la parte importante

Aquí está lo que casi nadie cuenta, y para el caso de uso de esta guía es
determinante:

| Situación | Qué pasa |
|---|---|
| `ANTHROPIC_BASE_URL` apunta a un host que no es de primera parte | **Claude Code lo desactiva**, porque la mayoría de proxies no reenvían los bloques `tool_reference` |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` puesto | Queda apagado, y **no puedes forzarlo** con `ENABLE_TOOL_SEARCH` |
| Despliegues de Microsoft Foundry en Azure | Lo rechazan en el servidor. Claude Code lo detecta y carga todo por adelantado. `ENABLE_TOOL_SEARCH` **no puede** con esto |
| Agent Platform de Google, modelos anteriores a la generación 4.5 | Carga todo por adelantado |
| Modelo sin soporte de `tool_reference` | No hay tool search. Requiere Sonnet 4.5, Haiku 4.5, Opus 4.5 o posteriores |

💡 **Opinión operativa, y es la más importante de este módulo.** Si tu
arquitectura es un **gateway propio**, que es el caso de uso ancla de esta guía,
estás por defecto en la primera fila de esa tabla: **tool search desactivado, y
por tanto el peaje permanente de MCP de vuelta**, proporcional a cuántas
herramientas tengas conectadas.

Se arregla poniendo `ENABLE_TOOL_SEARCH` explícitamente para anular ese
comportamiento de reserva, pero antes hay que comprobar que tu gateway **reenvía
los bloques `tool_reference`**. Si no los reenvía, forzarlo no te da tool search:
te da fallos. Y si tu organización quiere garantizar que quede encendido, se puede
fijar desde settings gestionados a partir de **v2.1.227**.

Si prefieres un comportamiento intermedio, `ENABLE_TOOL_SEARCH=auto` carga los
esquemas por adelantado **cuando caben en el 10 % de la ventana** y difiere solo
lo que se pase.

Comprobación práctica en dos comandos: `/mcp` para el coste por servidor y
`/context` para el reparto real de la sesión. **Mide antes de desconectar nada.**

---

## 8.4 · Autenticación con servidores remotos

Cinco piezas, y cada una resuelve un problema concreto de empresa:

- **OAuth desde la línea de comandos** para el flujo normal.
- **Puerto de callback fijo**, cuando el registro de la aplicación exige una URL
  de retorno estable y no puedes usar un puerto aleatorio.
- **Credenciales OAuth preconfiguradas**, para no registrar cliente en cada
  máquina.
- **Anular el descubrimiento de metadatos**, cuando el servidor no publica los
  suyos donde el estándar dice.
- **Cabeceras dinámicas** para autenticación propia, que es la salida cuando lo de
  enfrente no habla OAuth.

Y **restricción de scopes**: se pide lo mínimo. Un servidor MCP con más permisos
de los que necesita es una escalada de privilegios esperando su turno.

---

## 8.5 · Límites de salida

Una herramienta MCP que devuelve mucho es una de las formas más rápidas de
arruinar una sesión. Hay tres números que hay que conocer:

| Concepto | Valor |
|---|---|
| Umbral de aviso | **10.000 tokens**: Claude Code avisa al superarlo |
| Límite por defecto | **25.000 tokens** |
| Variable para cambiarlo | `MAX_MCP_OUTPUT_TOKENS` |

Con un matiz que importa a quien escribe servidores: la variable aplica a las
herramientas **que no declaran su propio límite**. Una herramienta que fije
`anthropic/maxResultSizeChars` en su respuesta de `tools/list` usa ese valor para
el contenido de texto, **pase lo que pase con `MAX_MCP_OUTPUT_TOKENS`**. Las que
devuelven imágenes sí siguen sujetas a la variable.

---

## 8.6 · Llamadas largas en segundo plano

**Una llamada a una herramienta MCP que sigue corriendo a los dos minutos pasa a
tarea en segundo plano** en lugar de bloquear la sesión. Requiere **v2.1.212 o
posterior**.

Cómo se comporta:

- Claude recibe el identificador de la tarea **de inmediato** y sigue trabajando.
- El resultado llega como notificación cuando la llamada se resuelve.
- Aparece en `/tasks`, desde donde también se para.
- **No sobrevive a salir de la sesión.**
- Los límites por llamada siguen aplicando mientras corre en segundo plano: el de
  reloj, por el `timeout` del servidor o `MCP_TOOL_TIMEOUT`, y el de inactividad,
  por `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`.
- El umbral de los dos minutos se cambia con `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`,
  en milisegundos.

Es una de esas mejoras que cambian el carácter de la herramienta: una consulta
pesada a una base de datos deja de ser una sesión congelada.

---

## 8.7 · Recursos, prompts y elicitación

**Recursos.** Un servidor puede exponer recursos y referenciarlos desde la
conversación, en vez de que la única superficie sean herramientas.

**Prompts como comandos.** Los prompts que expone un servidor se ejecutan como
comandos. Es la vía más limpia para que un equipo de plataforma reparta
procedimientos sin que nadie instale nada.

**Elicitación.** Un servidor puede pedirte datos estructurados a mitad de tarea.
**No requiere configuración por tu parte**: el diálogo aparece solo. Hay dos
modos, **formulario**, con los campos que define el servidor, y **URL**, que abre
el navegador para completar una autenticación o una aprobación.

Y hay dos controles que conviene recordar que existen: se puede **exigir
aprobación para una herramienta concreta**, y se puede manejar el caso de los
esquemas de entrada con un combinador en la raíz, que es donde se atascan algunos
servidores de terceros.

---

## 8.8 · Claude Code como servidor MCP

```bash
claude mcp serve
```

Convierte a Claude Code en un servidor stdio al que se pueden conectar otras
aplicaciones.

⚠️ **El detalle que hace perder media hora a todo el mundo:** el comando **no
imprime nada** al arrancar. Un servidor stdio se comunica por entrada y salida
estándar, así que **un terminal silencioso y bloqueado significa que está
funcionando** y esperando cliente. No está colgado.

---

## 8.9 · Gobierno corporativo

Para una flota, la configuración de MCP no se deja al criterio de cada máquina.
Hay **configuración gestionada de MCP**, y sobre ella las listas de permitidos y
denegados de la organización, con `deniedMcpServers` entre las claves de settings
gestionados. Del M3: una entrada inválida ahí **se retira y se aplica el
subconjunto válido**, y un valor inválido del todo se descarta con aviso, porque
denegar todos los servidores bloquearía servidores que la política nunca nombró.

También se pueden **desactivar los conectores de claude.ai** y aplicar controles
de organización sobre sus herramientas.

💡 La lista blanca es la postura correcta aquí, no la lista negra. Lo que devuelve
un servidor MCP entra en el contexto como cualquier otro texto, así que un
servidor de terceros sin revisar es, funcionalmente, código de terceros
ejecutándose con tu confianza. Es la tercera de las cuatro puertas de inyección
del M5.

---

## 8.10 · Tres montajes completos

**Vigilancia de errores.** Conectar el sistema de incidencias como servidor
remoto y pedirle a Claude que correlacione un fallo con el commit que lo
introdujo. Aquí el valor es que el contexto del error llega solo, sin copiar y
pegar trazas.

**Revisión de código contra el repositorio remoto.** El servidor de la forja
expone las pull requests. Combinado con el M13, es la base de la revisión
automática. Ojo al límite de salida: un diff grande se come los 25.000 tokens sin
despeinarse.

**Consulta a la base de datos en solo lectura.** El montaje que más rendimiento da
en una empresa, y el que se recomienda construir en el laboratorio del manual:
credenciales de solo lectura, servidor local por stdio, y el agente respondiendo
preguntas sobre datos reales **sin abrir un solo archivo del repositorio**.

Ese tercero es también el mejor ejemplo del principio del módulo: **MCP es el
enchufe hacia fuera**. Si lo que quieres es que trabaje mejor con lo que ya tiene
delante, la respuesta no era un MCP.

---

## Checklist de verificación

- [ ] Sé en qué ámbito está definido cada uno de mis servidores.
- [ ] Mi `.mcp.json` está en git y no contiene ni un secreto.
- [ ] He comprobado con `/mcp` lo que cuestan de verdad mis servidores.
- [ ] **Si uso gateway propio, he verificado si tengo tool search activo.**
- [ ] Mis servidores remotos piden los scopes mínimos.
- [ ] Sé que el límite de salida por defecto son 25.000 tokens.
- [ ] Los servidores de terceros pasan revisión antes de entrar.
- [ ] Mi organización tiene lista blanca, no lista negra.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "Definí la URL en el proyecto y la cabecera en local" | Los campos no se fusionan. Gana una fuente entera |
| "Tengo el servidor dos veces y solo conecta uno" | Duplicado. Los tres ámbitos casan por nombre; plugins y conectores, por endpoint |
| "Con el gateway me como el contexto" | Tool search se desactiva con `ANTHROPIC_BASE_URL` no first-party |
| "Puse `ENABLE_TOOL_SEARCH` y sigue cargando todo" | Foundry en Azure lo rechaza en servidor, o tienes las betas experimentales desactivadas |
| "La herramienta devuelve menos de lo que debería" | Límite de salida. Sube `MAX_MCP_OUTPUT_TOKENS` |
| "`claude mcp serve` no imprime nada" | Correcto. Silencio y bloqueo significan que funciona |
| "La sesión se congela con una consulta larga" | A los 2 minutos pasa a segundo plano. Requiere v2.1.212+ |
| "Mi tarea en segundo plano desapareció" | No sobrevive a salir de la sesión |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `mcp.md` | 85.681 | Transportes, ámbitos, tool search, límites, OAuth, elicitación |
| `managed-mcp.md` | 30.879 | Gobierno corporativo y listas |
| `mcp-quickstart.md` | 25.425 | Montajes de ejemplo |
| `channels.md` | 25.442 | Mensajes push desde servidores |
| `channels-reference.md` | 47.676 | Referencia de canales |
| `settings.md` | 285.543 | `deniedMcpServers` y tolerancia a entradas inválidas |

**Marcas pendientes:** ninguna. La corrección sobre tool search que se abrió en el
M1 queda aquí documentada al completo, incluidos los cinco casos en los que **no**
está activo, que es la parte que faltaba.
