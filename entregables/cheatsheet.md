# Claude Code · Chuleta

**Verificado contra 2.1.228 · 12 de agosto de 2026 · Cosas Agénticas · sin afiliación con Anthropic**

---

## El árbol de decisión · para en el primer sí

| | Pregunta | Va en |
|---|---|---|
| 1 | ¿Tiene que pasar **siempre**, sin que el modelo lo decida? | **hook** |
| 2 | ¿Necesita datos o acciones **fuera** de esta máquina? | **MCP** |
| 3 | ¿Hace falta en **todas** las tareas del repo? | **CLAUDE.md** |
| 4 | ¿Solo **a veces**, y el agente lo reconoce? | **skill** |
| 5 | ¿Lo lanzo **yo a mano**, siempre igual? | **comando** |
| 6 | ¿Necesita contexto limpio u otro criterio? | **subagente** |
| 7 | ¿Ya funciona y lo quiere el equipo? | **plugin** |
| — | ¿Ningún sí? | **reescribe la instrucción** |

**Lo único que se paga entero en cada turno: `CLAUDE.md`.** MCP solo pesa los nombres de sus herramientas, salvo con gateway propio, `ENABLE_TOOL_SEARCH=false`, betas desactivadas o modelo sin `tool_reference`.

---

## Comandos que se usan de verdad

| | |
|---|---|
| `/context` `/mcp` `/usage` `/cost` | Qué ocupa y qué cuesta |
| `/status` `/doctor` `/hooks` `/permissions` | Qué configuración manda |
| `/compact` `/clear` `/rewind` `/fork` | Contexto y sesión |
| `/model` `/effort` `/fast` `/autocompact` | Modelo y velocidad |
| `/agents` `/batch` `/goal` `/loop` | Trabajo en paralelo y automático |
| `/code-review` (`/review` es alias) | Revisión |
| `/plugin` `/add-dir` `/memory` `/config` | Extensión y ajustes |

## Banderas que sostienen lo automático

```
-p, --print                 modo no interactivo
--permission-mode MODO      default|acceptEdits|plan|auto|dontAsk|bypassPermissions
--allowedTools "A,B"        lista blanca de herramientas
--add-dir RUTA              acceso fuera del proyecto
--worktree                  aislar en árbol de trabajo propio
--bg, --background          arrancar en segundo plano
--bare                      SIN hooks, plugins, memoria ni CLAUDE.md  ← diagnóstico
--debug                     ver errores de análisis (YAML de skills roto)
--settings ARCHIVO          ajustes solo para esta ejecución
```

## Los seis modos de permisos

| Modo | Corre sin preguntar |
|---|---|
| `default` (**Manual**) | Solo lecturas |
| `acceptEdits` | Lecturas, ediciones y comandos de archivos comunes |
| `plan` | Lecturas, más lo que apruebe el clasificador |
| `auto` | Todo, con comprobaciones de fondo. **Por defecto desde el 14-ago-2026** |
| `dontAsk` | Solo herramientas pre-aprobadas ← **el de los scripts** |
| `bypassPermissions` | Todo. **Solo en aislamiento** |

---

## Precedencia de configuración

**Managed → línea de comandos → local → proyecto → usuario**

- Las **reglas de permisos se fusionan**, no se sobrescriben.
- `allow` de proyecto **requiere confianza del espacio de trabajo**. `deny` y `ask` no.
- Las **variables de entorno son otra capa** por encima de todo.
- Dentro de managed las fuentes **no se fusionan**, salvo `env` y las lock keys.

## Reglas de permisos

```json
{"permissions":{
  "allow":["Bash(npm run test *)"],
  "ask":  ["Bash(git push *)"],
  "deny": ["Read(./.env)","Read(./.env.*)","Read(./secrets/**)"]
}}
```

---

## Qué invalida la caché · y qué no

| **Invalida** | **Mantiene** |
|---|---|
| Cambiar de modelo | Editar tu código |
| Cambiar el esfuerzo | Editar `CLAUDE.md` en caliente |
| Activar fast mode | Cambiar output style |
| Conectar o quitar un MCP | Cambiar modo de permisos |
| Activar o quitar un plugin | Invocar skills y comandos |
| **Denegar una herramienta entera** | `/recap` |
| Compactar | Rebobinar |
| Actualizar Claude Code | |

**Editar tu código no invalida nada. Tocar la configuración, sí.**

---

## Paralelismo · quién sostiene el plan

| | Quién decide lo siguiente | Escala |
|---|---|---|
| **Subagentes** | Claude, turno a turno | pocas por turno |
| **Agent teams** | El líder, turno a turno | puñado de pares |
| **Workflows** | **El script** | **decenas o cientos** |

Los subagentes **no hablan entre sí**. Si tienen que hablarse, es un equipo.

---

## Números que hay que saber

| | |
|---|---:|
| Subagentes concurrentes | 20 (tope total: **ninguno**) |
| Aviso / límite de salida MCP | 10.000 / 25.000 tokens |
| Llamada MCP a segundo plano | 2 minutos |
| Auto memory de `MEMORY.md` | **200 líneas o 25 KB** |
| Skills tras compactar | 5.000 por skill, 25.000 en total |
| TTL de caché: sesión / subagente | 1 hora / **5 minutos** |
| Reintentos automáticos | hasta 10 |
| Ultrareview | **5-25 $** por revisión |

---

## Diagnóstico en tres pasos

1. **`claude --version`** y anótala.
2. **Arranca con `--bare`**, sin hooks, plugins ni `CLAUDE.md`.
3. Si en mínimo **no** pasa, el problema es tuyo. Si pasa, es del CLI.

| Síntoma | Causa real |
|---|---|
| "A veces lo hace y a veces no" | Es instrucción, no hook |
| "Se le olvidó lo que le dije" | Compactó. Va al `CLAUDE.md` |
| "Mi skill no se activa sola" | Frontmatter roto: cuerpo cargado, metadatos vacíos. **`--debug`** |
| "Rebobiné y sigue borrado" | Bash y subagentes en segundo plano **no** se rebobinan |
| "La sesión se queda sin contexto" | Mide `CLAUDE.md` con `/context` antes de culpar a MCP |
| "`403 host_not_allowed`" | Política de red del entorno cloud, **no** tu red |
| "Mi ajuste no se aplica" | Otro ámbito o una variable de entorno |

---

## Trampas de tutoriales viejos

- **`/ultraplan` no existe.** Retirado.
- **Los subagentes corren en segundo plano** por defecto desde la semana 27.
- **No hay tope de 200 subagentes** por sesión.
- **MCP no carga sus esquemas** por defecto.
- **`/review`** es alias de `/code-review`.
- En Team y Enterprise, **Slack se retira** en favor de Claude Tag.

**Pregúntale la versión al binario, no al artículo.**

---

## Los 31 eventos de hooks

`SessionStart` `Setup` `InstructionsLoaded` `UserPromptSubmit` `UserPromptExpansion`
`MessageDisplay` `PreToolUse` `PermissionRequest` `PostToolUse` `PostToolUseFailure`
`PostToolBatch` `PermissionDenied` `Notification` `SubagentStart` `SubagentStop`
`TaskCreated` `TaskCompleted` `Stop` `StopFailure` `TeammateIdle` `ConfigChange`
`CwdChanged` `DirectoryAdded` `FileChanged` `WorktreeCreate` `WorktreeRemove`
`PreCompact` `PostCompact` `SessionEnd` `Elicitation` `ElicitationResult`

**Cinco tipos:** `command` · `http` · `mcp_tool` · `prompt` · `agent`.
**Async solo en `command`, y no puede vetar nada.**

---

## La regla que resume el resto

**Dale algo que devuelva PASA o FALLA.** Sin eso, "parece terminado" es la única señal que tiene, y el bucle de verificación eres tú.
