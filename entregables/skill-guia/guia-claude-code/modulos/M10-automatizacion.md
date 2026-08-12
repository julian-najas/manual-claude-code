# M10 · Automatización: hooks, programación y modo no interactivo

> **Para quién es:** quien quiere que las cosas pasen sin él delante.
> **Qué resuelve:** convertir lo no negociable en código, y dejar de vigilar procesos a mano.
> **Qué NO cubre:** integración continua (M13) ni despliegue de flota (M14).

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 10.1 · Anatomía de un hook

La configuración tiene **tres niveles de anidamiento**, y la mitad de los errores
vienen de confundirlos:

1. Un **evento** al que responder, como `PreToolUse` o `Stop`.
2. Un **grupo de coincidencia** que filtra cuándo dispara.
3. Uno o varios **manejadores** que se ejecutan cuando hay coincidencia.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh",
            "args": []
          }
        ]
      }
    ]
  }
}
```

Fíjate en el campo **`if`**: es un segundo filtro más fino que el `matcher`. El
`matcher` dice "solo para la herramienta Bash"; el `if` dice "y solo cuando el
comando case con `rm *`". Sin él acabas ejecutando tu script en cada llamada a
Bash y filtrando dentro, que es más lento y más frágil.

### Dónde se define, y qué implica

| Ubicación | Alcance | ¿Se comparte? |
|---|---|---|
| `~/.claude/settings.json` | Todos tus proyectos | No |
| `.claude/settings.json` | Un proyecto | **Sí, va a git** |
| `.claude/settings.local.json` | Un proyecto | No |
| Settings gestionados | Toda la organización | Sí, lo controla sistemas |
| `hooks/hooks.json` de un plugin | Con el plugin activado | Sí, viaja con el plugin |
| Frontmatter de skill o agente | Mientras el componente está activo | Sí |

Los hooks de proyecto dependen del **diálogo de confianza del espacio de trabajo**.
Es la primera de las cuatro puertas que ya hemos visto colgar de ese mismo
diálogo, junto con `autoMemoryDirectory`, los permisos de proyecto y las skills
del repositorio.

---

## 10.2 · Los cinco tipos de manejador

Aquí es donde la mayoría de guías se quedan cortas: **no todos los hooks son un
script de shell**.

| Tipo | Qué hace | Cómo devuelve el resultado |
|---|---|---|
| `command` | Ejecuta un comando. Recibe el JSON del evento por entrada estándar | Códigos de salida y salida estándar |
| `http` | Envía el JSON del evento como POST a una URL | El cuerpo de la respuesta, mismo formato JSON |
| `mcp_tool` | Llama a una herramienta de un servidor MCP ya conectado | Su salida de texto se trata como la de un comando |
| `prompt` | Manda un prompt a un modelo para una evaluación de un turno | El modelo devuelve una decisión sí/no en JSON |
| `agent` | Lanza un subagente **con acceso a herramientas** que verifica | Como el anterior, pero puede investigar antes de decidir |

Los dos últimos son la novedad conceptual: **un hook puede razonar**. Un hook de
tipo `prompt` usa un modelo, Haiku por defecto, para decidir si permite o bloquea.
Uno de tipo `agent` puede además usar herramientas para comprobarlo.

⚠️ Y una advertencia que se deduce sola pero conviene decir: un hook que razona
**ya no es determinista**. Sigue siendo mucho más fiable que una instrucción en el
`CLAUDE.md`, porque el evento siempre dispara y la decisión siempre se toma, pero
si lo que buscas es una garantía dura, el tipo correcto es `command`.

### Qué tipo admite cada evento

No todos los eventos admiten los cinco tipos, y esto **no está en ningún tutorial**:

- **Los cinco tipos** (13 eventos): `PreToolUse`, `PostToolUse`, `PostToolUseFailure`,
  `PostToolBatch`, `PermissionRequest`, `PermissionDenied`, `Stop`, `SubagentStop`,
  `TaskCreated`, `TaskCompleted`, `TeammateIdle`, `UserPromptSubmit`,
  `UserPromptExpansion`.
- **Solo `command`, `http` y `mcp_tool`** (15 eventos): `ConfigChange`, `CwdChanged`,
  `DirectoryAdded`, `Elicitation`, `ElicitationResult`, `FileChanged`,
  `InstructionsLoaded`, `Notification`, `PreCompact`, `PostCompact`, `SessionEnd`,
  `StopFailure`, `SubagentStart`, `WorktreeCreate`, `WorktreeRemove`.
- **Solo `command` y `mcp_tool`**: `SessionStart` y `Setup`.

---

## 10.3 · Las tres cadencias

Los eventos se agrupan por con qué frecuencia disparan, y saberlo evita
sorpresas en la factura y en el rendimiento:

- **Una vez por sesión**: `SessionStart`, `SessionEnd`.
- **Una vez por turno**: `UserPromptSubmit`, `Stop`, `StopFailure`.
- **En cada llamada a herramienta**, dentro del bucle agéntico: `PreToolUse` y
  `PostToolUse`. Excepción documentada: las llamadas a `EndConversation` **se
  saltan los dos**.

Un hook pesado en la tercera cadencia es la forma más rápida de convertir una
sesión ágil en un suplicio.

---

## 10.4 · Tabla 6 · Los 31 eventos

| Evento | Cadencia | Tipos | Para qué sirve de verdad |
|---|---|---|---|
| `SessionStart` | Sesión | cmd, mcp | Cargar estado, avisar del entorno |
| `Setup` | Solo con `--init-only`, `--init` o `--maintenance` | cmd, mcp | Preparación de una máquina o un runner |
| `InstructionsLoaded` | Al cargar `CLAUDE.md` o una regla | cmd, http, mcp | Auditar qué instrucciones entraron y cuándo |
| `UserPromptSubmit` | Turno | los 5 | Validar o enriquecer la petición antes de que llegue |
| `UserPromptExpansion` | Al expandir un comando | los 5 | **Bloquear la invocación directa de comandos concretos** |
| `MessageDisplay` | Mientras se imprime la respuesta | cmd, http, mcp | Postproceso de lo que se muestra |
| `PreToolUse` | Cada herramienta | los 5 | **El veto. La pieza más importante de todas** |
| `PermissionRequest` | Al pedir permiso | los 5 | Automatizar decisiones de permiso |
| `PostToolUse` | Cada herramienta | los 5 | Formatear, registrar, validar el resultado |
| `PostToolUseFailure` | Al fallar una herramienta | los 5 | Reaccionar a fallos sin esperar a que Claude reintente |
| `PostToolBatch` | Tras resolverse **todo el lote** | los 5 | Comprobaciones que necesitan ver el conjunto |
| `PermissionDenied` | Al denegarse | los 5 | Registrar intentos y detectar fricción |
| `Notification` | Al notificar | cmd, http, mcp | Llevar avisos a Slack o al móvil |
| `SubagentStart` | Al lanzar subagente | cmd, http, mcp | Contabilidad de subagentes |
| `SubagentStop` | Al terminar subagente | los 5 | Puerta de calidad sobre lo que devuelve |
| `TaskCreated` | Al crear tarea | los 5 | Sincronizar con tu gestor de tareas |
| `TaskCompleted` | Al completar tarea | los 5 | Verificar el criterio de aceptación |
| `Stop` | Turno | los 5 | **Puerta de calidad de fin de turno** |
| `StopFailure` | Turno terminado por error de API | cmd, http, mcp | Alertar. Ojo: se ignoran su salida y su código |
| `TeammateIdle` | Compañero a punto de quedar ocioso | los 5 | **Puerta de calidad en agent teams** |
| `ConfigChange` | Al cambiar configuración | cmd, http, mcp | Detectar cambios no autorizados |
| `CwdChanged` | Al cambiar de directorio | cmd, http, mcp | Recargar entorno del nuevo directorio |
| `DirectoryAdded` | Al añadir directorio | cmd, http, mcp | Auditar ampliaciones de alcance |
| `FileChanged` | Al cambiar un archivo vigilado | cmd, http, mcp | Recargar variables al tocar configuración |
| `WorktreeCreate` | Al crear worktree | cmd, http, mcp | Preparar dependencias del nuevo árbol |
| `WorktreeRemove` | Al eliminar worktree | cmd, http, mcp | Limpieza |
| `PreCompact` | Antes de compactar | cmd, http, mcp | Salvar lo que no debe perderse |
| `PostCompact` | Después de compactar | cmd, http, mcp | **Reinyectar lo que la compactación se llevó** |
| `SessionEnd` | Sesión | cmd, http, mcp | Cerrar, archivar, reportar coste |
| `Elicitation` | Al pedir datos un MCP | cmd, http, mcp | Automatizar respuestas conocidas |
| `ElicitationResult` | Tras responder | cmd, http, mcp | Registrar qué se entregó |

Dos eventos merecen atención especial porque resuelven problemas que la gente
intenta resolver mal: **`PostCompact`** es la respuesta correcta a "se le olvidan
las cosas al compactar", mejor que repetir la instrucción cada turno. Y
**`TeammateIdle`** es la única forma de poner una puerta de calidad en un agent
team antes de que un compañero se dé por satisfecho.

---

## 10.5 · Hooks asíncronos

Por defecto un hook **bloquea** hasta terminar. Con `"async": true` corre en
segundo plano mientras Claude sigue trabajando, y su salida se entrega en el turno
siguiente.

Dos límites que hay que aceptar antes de usarlo:

- **Solo está disponible en hooks de tipo `command`.**
- **Un hook asíncrono no puede bloquear ni controlar nada.** Los campos de
  respuesta `decision`, `permissionDecision` y `continue` **no tienen efecto**,
  porque la acción que habrían controlado ya ocurrió.

O sea: async es para observar, no para vetar. Suite de tests, despliegue, llamada
a una API externa. Si necesitas que impida algo, tiene que bloquear.

---

## 10.6 · Tabla 13 · Programación temporal

| | Cloud (Routines) | Escritorio | `/loop` |
|---|---|---|---|
| Corre en | La nube, gestionada por Anthropic | Tu máquina | Tu máquina |
| ¿Máquina encendida? | **No** | Sí | Sí |
| ¿Sesión abierta? | No | No | **Sí** |
| Persiste al reiniciar | Sí | Sí | Se restaura con `--resume` si no caducó |
| Acceso a archivos locales | **No**, clon nuevo | Sí | Sí |
| Servidores MCP | Conectores por tarea | Archivos de config y conectores | Hereda de la sesión |
| Confirmaciones de permiso | **No, corre sola** | Configurable por tarea | Hereda de la sesión |
| Intervalo mínimo | **1 hora** | 1 minuto | 1 minuto |

Las tareas de `/loop` y los recordatorios son **de ámbito de sesión**: viven en la
conversación actual y mueren al empezar otra. `--resume` o `--continue` recuperan
las que no hayan **caducado a los siete días**: una recurrente creada en la última
semana, o una de un solo disparo cuya hora aún no pasó.

### Y la otra familia: no programar, reaccionar

- **Channels**: en lugar de sondear, tu CI **empuja** el fallo dentro de la sesión.
- **`/goal`**: fija una condición de terminación y Claude sigue trabajando turno
  tras turno hasta cumplirla. Tras cada turno, **un modelo pequeño y rápido
  comprueba si la condición se cumple**; si no, arranca otro turno en vez de
  devolverte el control. Se limpia solo al cumplirse.

| Enfoque | El siguiente turno arranca cuando | Para cuando |
|---|---|---|
| `/goal` | Termina el anterior | Un modelo confirma que la condición se cumple |
| `/loop` | Pasa un intervalo | Lo paras tú, o Claude decide que está hecho |
| Hook `Stop` | Termina el anterior | Lo decide tu script o tu prompt |

💡 **Opinión operativa.** La secuencia sana es: si puedes reaccionar a un evento,
usa **channels**; si tienes una condición verificable, usa **`/goal`**; si de
verdad hay que sondear algo externo, usa **`/loop`** con un intervalo acorde a lo
que tarda en cambiar ese algo. Sondear cada minuto un despliegue que tarda ocho es
pagar ocho veces por la misma respuesta.

---

## 10.7 · Modo no interactivo

`--print` es la base de todo lo automático. Lo que hay que conocer:

- **Salida estructurada** y **streaming**, para encadenarlo con otras
  herramientas.
- **Auto-aprobación de herramientas** acotada, que es lo que hace viable un script.
- **Bare mode** para arrancar más rápido, saltándose hooks, LSP, sincronización de
  plugins, auto memory y descubrimiento de `CLAUDE.md`.
- **Tareas en segundo plano al salir**: hay comportamiento definido para lo que
  quede corriendo.
- Se puede **fallar la CI si un plugin no carga**, que es la diferencia entre una
  automatización y una ilusión de automatización.

---

## 10.8 · Seis hooks listos para copiar

Los seis van en `.claude/settings.json`, para que viajen con el repositorio.

**1. Formatear después de editar.** El caso canónico: lo que no quieres pedir cada vez.

```json
{ "hooks": { "PostToolUse": [ { "matcher": "Edit|Write",
  "hooks": [ { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/format.sh" } ] } ] } }
```

**2. Vetar la lectura de secretos.** Cinturón además del `deny` de permisos.

```json
{ "hooks": { "PreToolUse": [ { "matcher": "Read",
  "hooks": [ { "type": "command", "if": "Read(./.env*)",
    "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/veto-secretos.sh" } ] } ] } }
```

**3. Bloquear el borrado masivo.** El `if` hace el trabajo fino.

```json
{ "hooks": { "PreToolUse": [ { "matcher": "Bash",
  "hooks": [ { "type": "command", "if": "Bash(rm -rf *)",
    "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/veto-rm.sh" } ] } ] } }
```

**4. Reinyectar las reglas tras compactar.** La cura correcta al olvido.

```json
{ "hooks": { "PostCompact": [ { "hooks": [ { "type": "command",
  "command": "cat ${CLAUDE_PROJECT_DIR}/.claude/reglas-permanentes.md" } ] } ] } }
```

**5. Auditoría sin frenar.** Asíncrono, porque solo observa.

```json
{ "hooks": { "PostToolUse": [ { "matcher": "*",
  "hooks": [ { "type": "command", "async": true,
    "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/auditar.sh" } ] } ] } }
```

**6. Puerta de calidad de fin de turno.** Bloqueante a propósito: tiene que poder vetar.

```json
{ "hooks": { "Stop": [ { "hooks": [ { "type": "command",
  "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/puerta-calidad.sh", "timeout": 120 } ] } ] } }
```

Para un agent team, el sexto va en `TeammateIdle` en lugar de en `Stop`.

---

## Checklist de verificación

- [ ] Sé la diferencia entre `matcher` y el campo `if`.
- [ ] Mis hooks del proyecto están en git y el equipo ha aceptado la confianza.
- [ ] Ninguno de mis hooks pesados dispara en cada llamada a herramienta.
- [ ] Sé que un hook `async` no puede vetar nada.
- [ ] Si necesito garantía dura, uso `command` y no `prompt`.
- [ ] Uso `PostCompact` en vez de repetir instrucciones cada turno.
- [ ] Mis intervalos de `/loop` se parecen a lo que tardan las cosas que vigilo.
- [ ] Mi CI falla si un plugin no carga.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "Mi hook no dispara nunca" | El evento no admite ese tipo de manejador. Repasa la lista de 10.2 |
| "Mi hook async no bloquea nada" | Por diseño: `decision` y `continue` no tienen efecto en async |
| "Puse async en un hook http" | Solo existe en `type: "command"` |
| "Las sesiones van lentas desde que puse hooks" | Tienes uno pesado en cadencia de cada herramienta |
| "Mi `StopFailure` no cambia nada" | Se ignoran su salida y su código de salida |
| "Mis tareas de `/loop` desaparecieron" | Son de ámbito de sesión, y caducan a los 7 días |
| "La tarea en la nube no ve mis archivos" | Corre sobre un clon nuevo, sin tu disco |
| "Quiero sondear cada minuto en la nube" | El mínimo en la nube es 1 hora. Usa escritorio o `/loop` |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `hooks.md` | 267.830 | Ciclo de vida, configuración, los 31 eventos, tipos, async |
| `hooks-guide.md` | 69.182 | Hooks de prompt y de agente |
| `scheduled-tasks.md` | 17.017 | Tabla 13, caducidad de 7 días |
| `goal.md` | 9.502 | `/goal` y la comparación de formas de seguir trabajando |
| `headless.md` | 27.831 | Modo no interactivo, bare mode, salida estructurada |
| `deep-links.md` | 14.751 | Enlaces profundos |

**Marcas pendientes:** ninguna. La columna "para qué sirve de verdad" de la
tabla 6 es criterio operativo propio, no documentación; los nombres, cadencias y
tipos admitidos sí salen de `hooks.md`.
