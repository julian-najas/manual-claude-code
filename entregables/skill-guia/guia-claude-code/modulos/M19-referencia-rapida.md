# M19 · Referencia rápida

> **Para quién es:** quien ya sabe y solo quiere el dato.
> **Qué resuelve:** dejar de buscar. Todo en tablas, pensado para imprimir.
> **Qué NO cubre:** explicaciones. Para eso están los otros veinte módulos.

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 19.1 · El tamaño real de la superficie

Antes de las tablas, los números, porque calibran expectativas:

| | Cantidad |
|---|---:|
| Comandos slash documentados | **111** |
| Banderas del CLI documentadas | **90** |
| Banderas visibles en `claude --help` en 2.1.228 | **65** |
| Variables de entorno documentadas | **336** |
| Eventos de hooks | **31** |
| Errores catalogados con mensaje literal | **83** |
| Páginas de documentación oficial | **187** |

Trescientas treinta y seis variables de entorno. Cualquiera que te diga que
conoce Claude Code entero está exagerando, y esta guía tampoco lo pretende: lo que
pretende es que sepas **dónde mirar**.

---

## 19.2 · Tabla 7 · Herramientas, comportamiento y límites

| Herramienta | Comportamiento que hay que conocer |
|---|---|
| **Bash** | Cada comando en **un proceso separado**. Un `cd` se arrastra a los siguientes **solo si queda dentro del proyecto o de un directorio añadido**; si sale, se resetea y añade `Shell cwd was reset to <dir>` al resultado. **Las sesiones de subagente nunca arrastran el cambio de directorio** |
| **Read** | Devuelve el contenido **con números de línea** y espera rutas absolutas. Si la lectura completa supera el límite de tokens, devuelve la primera página con un aviso `PARTIAL view` y cómo seguir con `offset` y `limit`. Con `offset` o `limit` explícitos que aun así superen el límite, **devuelve error** |
| **Grep** | Construido sobre **ripgrep**, y usa **su sintaxis de expresiones regulares, no la de grep POSIX**. `interface{}` en Go se busca como `interface\{\}`. ⚠️ **Antes de v2.1.208, una entrada rechazada se reportaba como `No files found`** aunque el texto existiera |
| **Glob** | Encuentra archivos por nombre; Grep busca dentro de ellos |
| **WebFetch** | **Lossy por diseño.** Descarga, convierte a Markdown y **ejecuta tu prompt contra el contenido con un modelo pequeño y rápido**. Claude recibe **la respuesta de ese modelo, no la página**. La conversión **no es configurable** |
| **WebSearch** | Devuelve **títulos y URLs**, no descarga las páginas. Puede lanzar **hasta ocho búsquedas de backend por llamada**. `allowed_domains` o `blocked_domains`, **no las dos en la misma llamada** |
| **Edit / Write** | Bloqueadas sobre rutas cubiertas por una regla `deny` de **lectura**, incluida la creación de archivos nuevos ahí. `NotebookEdit` **no** está cubierto |
| **PowerShell** | Herramienta propia en Windows, con selección de shell en settings, hooks y skills, y su propia gestión de codificación y códigos de salida |
| **Monitor** | Con fuente WebSocket |
| **LSP** | Inteligencia de código, para leer menos archivo |
| **Agent** | Lanza subagentes. Falla si ninguna entrada de su lista de herramientas casa |
| **EndConversation** | **Se salta `PreToolUse` y `PostToolUse`**, a diferencia de todas las demás |

⚠️ **La fila de `WebFetch` merece un cartel**, porque produce diagnósticos falsos:

> Un resultado que dice que una página **no menciona** algo puede significar solo
> que **el prompt no preguntó por ello**.

La salida es pedirlo otra vez con un prompt más específico, o **usar `curl` desde
Bash para la página sin procesar**. Es exactamente la trampa en la que se cae al
investigar documentación, y quien escribe esta guía ha caído en ella hoy mismo.

---

## 19.3 · Comandos slash

**111 documentados.** Los que se usan a diario, agrupados por para qué:

| Para | Comandos |
|---|---|
| Contexto y sesión | `/context` `/compact` `/clear` `/continue` `/resume` `/fork` `/rewind` |
| Configuración | `/config` `/status` `/doctor` `/permissions` `/hooks` `/mcp` `/memory` |
| Modelo y coste | `/model` `/effort` `/fast` `/usage` `/cost` `/autocompact` |
| Trabajo | `/agents` `/batch` `/bashes` `/background` `/goal` `/loop` `/diff` |
| Revisión | `/code-review` `/review` (alias) `/security-review` |
| Extensión | `/plugin` `/skill-name` `/add-dir` `/allowed-tools` |
| Otros | `/help` `/bug` `/feedback` `/exit` |

Para la lista completa, `commands.md`. Y para saber cuáles tienes **tú**
disponibles, que depende de plan, proveedor y plugins, `/help` en tu sesión.

---

## 19.4 · Banderas del CLI, y un cruce que merece la pena

Las que sostienen casi todo lo automático de esta guía:

| Bandera | Para qué |
|---|---|
| `-p`, `--print` | **Modo no interactivo.** La base del M10 y el M13 |
| `--permission-mode` | `default`/`manual`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` |
| `--allowedTools`, `--disallowedTools` | Lista de herramientas permitidas o denegadas |
| `--add-dir` | Directorios adicionales accesibles |
| `--agents` | Definir agentes en JSON desde la llamada |
| `--agent` | Agente para esta sesión |
| `--bg`, `--background` | Arrancar como agente en segundo plano |
| `--worktree` | Aislar en un árbol de trabajo propio |
| `--cloud` | Crear o adjuntarse a una sesión en la nube |
| `--autocompact` | Ventana antes de compactar, de 100k a 1M |
| `--effort` | Nivel de esfuerzo |
| `--settings` | Archivo de ajustes para esta ejecución |
| `--mcp-config`, `--plugin-dir` | Configuración puntual de MCP y plugins |
| `--append-system-prompt` | Añadir al system prompt |
| `--bare` | **Modo mínimo**: sin hooks, LSP, plugins, auto memory ni descubrimiento de `CLAUDE.md`. La herramienta de diagnóstico del M18 |
| `--debug` | Ver errores de análisis, como el YAML roto de una skill (M7) |
| `--dangerously-skip-permissions` | Saltarse todo. Solo en aislamiento |

Y los subcomandos: `agents`, `auth`, `doctor`, `mcp`, `plugin`, `project`,
`import`, `install`, `update`, `setup-token`, `gateway`, `auto-mode`,
`ultrareview`.

### El cruce contra el binario

Este módulo es el sitio natural para aplicar la disciplina de la guía a la propia
guía. Comparando `cli-reference.md` con lo que responde `claude --help` en la
versión 2.1.228 instalada:

⚠️ **Dos banderas del binario no aparecen en la referencia del CLI:**

- **`--brief`**: *Enable SendUserMessage tool for agent-to-user communication.* No
  aparece en `cli-reference.md` **ni en ninguna de las páginas descargadas para
  esta guía**.
- **`--file <specs...>`**: *File resources to download at startup*, con formato
  `file_id:ruta_relativa`. Se menciona en el changelog y en la página de permisos,
  pero **no en la referencia del CLI**.

**Matiz honesto y necesario:** para esta guía se han descargado unas 70 de las 187
páginas. "No aparece en las páginas descargadas" **no es** "no está documentada en
ningún sitio". Lo verificable es lo que digo: **no está en `cli-reference.md`**, y
esa es la página donde un lector iría a buscarla.

---

## 19.5 · Variables de entorno, por categoría

**336 documentadas.** Nadie las necesita todas; lo útil es saber por dónde
buscar:

| Categoría | Ejemplos representativos |
|---|---|
| Autenticación | `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_CUSTOM_HEADERS` |
| Enrutado y gateway | `ANTHROPIC_BASE_URL`, `ANTHROPIC_BETAS` |
| Proveedores cloud | `ANTHROPIC_AWS_*`, `ANTHROPIC_BEDROCK_*` |
| Contexto y modelo | `CLAUDE_CODE_AUTO_COMPACT_WINDOW` |
| Herramientas y MCP | `ENABLE_TOOL_SEARCH`, `MAX_MCP_OUTPUT_TOKENS`, `MCP_TOOL_TIMEOUT`, `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`, `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS` |
| Agentes | `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` |
| Memoria | `CLAUDE_CODE_DISABLE_AUTO_MEMORY`, `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` |
| Empresa | `CLAUDE_CODE_PROCESS_WRAPPER`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` |
| Actualización | `DISABLE_AUTOUPDATER` |

**Regla de oro:** una variable de entorno es **otra capa de anulación** por encima
de tus settings (M3). Cuando un ajuste no se aplica y ya has mirado los cuatro
ámbitos, mira el entorno.

---

## 19.6 · Sintaxis de reglas de permisos

```json
{
  "permissions": {
    "allow": ["Bash(npm run test *)", "Read(~/.zshrc)"],
    "ask":   ["Bash(git push *)"],
    "deny":  ["Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)", "Bash(curl *)"]
  }
}
```

| Concepto | Regla |
|---|---|
| Forma | `Herramienta(patrón)` o solo `Herramienta` |
| `allow` | Corre sin preguntar |
| `ask` | **Fuerza confirmación** aunque otra cosa lo permitiera |
| `deny` | Bloquea |
| Entre ámbitos | **Se fusionan**, no se sobrescriben |
| Nombre pelado | `Bash`, `Bash(*)` o comodín de nombre **quita la herramienta del contexto** e **invalida la caché** |
| `allow` de proyecto | Requiere **confianza del espacio de trabajo**. `deny` y `ask` no |

---

## 19.7 · Los 31 eventos de hooks

**Una vez por sesión:** `SessionStart` · `SessionEnd`
**Una vez por turno:** `UserPromptSubmit` · `Stop` · `StopFailure`
**En cada llamada a herramienta:** `PreToolUse` · `PostToolUse`
**Resto:** `Setup` · `InstructionsLoaded` · `UserPromptExpansion` · `MessageDisplay` ·
`PermissionRequest` · `PermissionDenied` · `PostToolUseFailure` · `PostToolBatch` ·
`Notification` · `SubagentStart` · `SubagentStop` · `TaskCreated` · `TaskCompleted` ·
`TeammateIdle` · `ConfigChange` · `CwdChanged` · `DirectoryAdded` · `FileChanged` ·
`WorktreeCreate` · `WorktreeRemove` · `PreCompact` · `PostCompact` · `Elicitation` ·
`ElicitationResult`

**Cinco tipos de manejador:** `command` · `http` · `mcp_tool` · `prompt` · `agent`.
No todos los eventos admiten los cinco: el reparto exacto está en el M10.

---

## 19.8 · Números que conviene tener a mano

| Concepto | Valor |
|---|---:|
| Subagentes concurrentes por defecto | **20** |
| Tope total de subagentes por sesión | **ninguno** (se eliminó) |
| Aviso de salida de herramienta MCP | 10.000 tokens |
| Límite por defecto de salida MCP | 25.000 tokens |
| Llamada MCP que pasa a segundo plano | **2 minutos** |
| Auto memory que se carga de `MEMORY.md` | **200 líneas o 25 KB** |
| Skills tras compactar: por skill | 5.000 tokens |
| Skills tras compactar: presupuesto total | 25.000 tokens |
| TTL de caché en suscripción | 1 hora |
| TTL de caché en subagentes | **5 minutos** |
| Reintentos automáticos | **hasta 10**, con retroceso exponencial |
| Búsquedas de backend por llamada de WebSearch | hasta 8 |
| Coste de una ultrareview | **5 a 25 $** |
| Ventana de auto-compactación configurable | 100k a 1M tokens |

---

## 19.9 · Glosario mínimo

| Castellano | Inglés | Qué es |
|---|---|---|
| Bucle agéntico | agentic loop | Reunir contexto, actuar, verificar |
| Arnés | harness | Lo que envuelve al modelo y le da herramientas |
| Ámbito | scope | Dónde vive una configuración y a quién afecta |
| Manejador | handler | Lo que ejecuta un hook |
| Grupo de coincidencia | matcher group | El filtro de un hook |
| Árbol de trabajo | worktree | Checkout de git separado |
| Subagente | subagent | Sesión aparte que devuelve un resumen |
| Bifurcación | fork | Copia que hereda contexto y caché del padre |
| Compactación | compaction | Resumen automático al llenarse la ventana |
| Diferido | deferred | Cargado bajo demanda, no al arrancar |

---

## Checklist de verificación

- [ ] Sé que `WebFetch` es lossy y cuándo usar `curl` en su lugar.
- [ ] Sé que Grep usa sintaxis de ripgrep, no de grep POSIX.
- [ ] Sé que un `cd` fuera del proyecto se resetea solo.
- [ ] Sé que las variables de entorno son otra capa de anulación.
- [ ] Tengo `--bare` y `--debug` en la cabeza para diagnosticar.
- [ ] Conozco los números de la tabla del 19.8 sin buscarlos.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "`WebFetch` dice que la página no menciona eso" | Puede ser que **tu prompt no preguntara**. Es lossy. Usa `curl` para la página cruda |
| "Mi patrón de Grep no encuentra nada" | Sintaxis de ripgrep, no de grep POSIX. Escapa los metacaracteres |
| "El `cd` no se mantiene entre comandos" | Salió del proyecto y se reseteó. Mira si el resultado dice `Shell cwd was reset to` |
| "Un subagente no hereda mi directorio de trabajo" | Nunca lo hace. Por diseño |
| "Busqué la bandera en la referencia y no está" | Puede estar en el binario y no en `cli-reference.md`. `claude --help` manda |
| "Cambié el ajuste en los cuatro ámbitos y sigue igual" | Una variable de entorno es **otra capa** por encima |
| "Puse `allowed_domains` y `blocked_domains` a la vez" | No se pueden combinar en la misma llamada |
| "Mi `MEMORY.md` largo no se carga entero" | 200 líneas o 25 KB, lo que llegue antes |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `tools-reference.md` | 89.853 | Tabla 7, comportamiento y límites por herramienta |
| `commands.md` | 153.980 | Los 111 comandos slash |
| `cli-reference.md` | 106.493 | Las 90 banderas documentadas |
| `env-vars.md` | 368.558 | Las 336 variables de entorno |
| `glossary.md` | 23.042 | Glosario |

Verificación propia: cruce de `cli-reference.md` contra `claude --help` en la
versión 2.1.228 instalada, 12 de agosto de 2026.

**Marcas pendientes:** las dos banderas del 19.4 quedan marcadas como
**verificadas contra el binario** y **ausentes de `cli-reference.md`**, con el
matiz explícito de que no se han revisado las 187 páginas.
