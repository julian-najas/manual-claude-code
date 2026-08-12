# M21 · Features retiradas, renombradas y trampas de tutoriales viejos

> **Para quién es:** quien llega desde un vídeo, un artículo o un tutorial de hace unos meses.
> **Qué resuelve:** horas perdidas persiguiendo algo que ya no existe o que cambió de nombre.
> **Qué NO cubre:** nada actual. Todo lo de aquí está muerto, renombrado o cambiado.

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 21.1 · Por qué este módulo existe

Claude Code publica versiones **casi a diario**. Entre la 2.1.178 de mediados de
junio y la 2.1.228 del 11 de agosto hay **cincuenta versiones en ocho semanas**.

Eso significa que un tutorial de hace tres meses no está "un poco desactualizado":
puede estar describiendo comportamientos por defecto que ya son los contrarios.
Este módulo es la lista de lo que hay que desaprender.

⚠️ **Y un aviso sobre las fuentes**, importante para quien mantenga esta guía: los
resúmenes semanales oficiales **no cubren todas las semanas**. No existe digest de
la semana 31 ni de la 33. **Para todo lo posterior al 7 de agosto, la única fuente
es el changelog.** Cualquier proceso de actualización que se apoye solo en los
digests nace desfasado.

---

## 21.2 · Tabla 15 · Cronología 2026

| Semana | Fechas | Versiones | Lo que cambió |
|---|---|---|---|
| **25** | 15-19 jun | v2.1.178 → 183 | **Artifacts**: publicar una página compartible desde la sesión · coincidencia por parámetro de entrada en reglas `deny` y `ask` · fijar cualquier ajuste desde el prompt con `/config` |
| **26** | 22-26 jun | v2.1.185 → 193 | `claude mcp login` para autenticar servidores MCP desde la shell · el modo shell responde a la salida del comando con el prefijo `!` · `/recap` |
| **27** | 29 jun - 3 jul | v2.1.195 → 201 | **Sonnet 5 pasa a ser el modelo por defecto** · **Claude en Chrome llega a disponibilidad general** · **los subagentes corren en segundo plano por defecto** · Desktop en Linux en beta · `/radio` |
| **28** | 6-10 jul | v2.1.202 → 206 | Navegador integrado en Desktop · **`/doctor` pasa a ser una revisión completa de instalación** |
| **29** | 13-17 jul | v2.1.207 → 212 | Los artifacts llaman a tus conectores MCP · **modo lector de pantalla** |
| **30** | 20-24 jul | v2.1.214 → 219 | **Opus 5 pasa a ser el modelo Opus por defecto** · panel de simulador de iOS en Desktop · **plugin Claude Security** |
| **31** | — | — | **Sin digest publicado** |
| **32** | 3-7 ago | v2.1.220 → 224 | **Mensajería entre sesiones** · **entornos self-hosted** en beta · **auto mode pasa a ser el modo de permisos por defecto** |
| **33** | 10-11 ago | v2.1.225 → 228 | **Sin digest.** Solo changelog: aviso de límite de gasto del gateway, confianza de espacio de trabajo en `claude agents`, `SendMessage` inicia conversación con Remote Control |

---

## 21.3 · Retirado: ya no existe

| Qué | Cuándo | Qué usar ahora |
|---|---|---|
| **Ultraplan**, el comando `/ultraplan` y la palabra clave `ultraplan` | Semana 32 | Modo plan, o Claude Code en la web |
| **API de sesiones V2 de TypeScript**: `unstable_v2_createSession`, `unstable_v2_resumeSession`, `unstable_v2_prompt`, y los tipos `SDKSession` y `SDKSessionOptions` | SDK de TypeScript 0.3.142 | La API `query()` con `AsyncIterable<SDKUserMessage>` o `options.resume` |
| **El tope de 200 subagentes por sesión** | Semana 32 | Ya no hay tope total. Siguen la concurrencia y la profundidad |

---

## 21.4 · Renombrado y en retirada

| Qué | Estado |
|---|---|
| **`/review`** | Ahora es **alias de `/code-review`**. Y `/code-review` sin nivel de esfuerzo **reutiliza el último que escribiste** |
| **Claude Code en Slack** | **En retirada en Team y Enterprise** en favor de **Claude Tag**, que ejecuta `@Claude` como identidad compartida de la organización en vez de bajo la cuenta de un usuario. La app y el identificador se quedan; la fecha de corte la da el equipo de cuenta. **En Pro y Max sigue siendo la vía de instalación** |
| **El modo `default`** | Se llama **Manual** en el CLI, en las extensiones y en la app de escritorio, pero su valor de configuración sigue siendo `default`. El alias `manual` requiere **v2.1.200+** |

---

## 21.5 · Cambios de comportamiento por defecto

Los más peligrosos, porque **no fallan**: simplemente hacen algo distinto de lo que
tu tutorial dice.

| Comportamiento | Antes | Ahora |
|---|---|---|
| **Modo de permisos por defecto** | `default` (Manual) | **Auto mode**, desde el **14 de agosto de 2026** en Pro, Max y Team. Si fijaste el tuyo, se queda |
| **Los subagentes** | En primer plano | **En segundo plano por defecto**, desde la semana 27 |
| **Modelo por defecto** | Varias resoluciones | **Sonnet 5** en Pro y Team Standard, **Opus 5** en Max, API y proveedores cloud. Antes de **v2.1.219** resolvía a Opus 4.8 en varias cuentas |
| **Definiciones de herramientas MCP** | Cargadas por adelantado | **Diferidas por defecto** con tool search. Solo los nombres pesan |
| **`/doctor`** | Pantalla de solo lectura, se pulsaba `f` para mandarle el informe a Claude | **Revisión completa que propone arreglos** y los aplica si confirmas. Cambió en **v2.1.205**; la revisión del `CLAUDE.md` requiere **v2.1.206+** |
| **Renderizado** | Clásico | **Pantalla completa por defecto si empezaste a usar Claude Code el 6 de mayo de 2026 o después**. Si empezaste antes, conservas el clásico |

---

## 21.6 · Endurecimientos silenciosos

Cambios que **cierran un agujero** y que hay que conocer si tu configuración se
apoyaba en el comportamiento antiguo:

| Desde | Qué cambió |
|---|---|
| **v2.1.200** | Un remoto añadido o reapuntado **a mitad de sesión ya no es de confianza** para el clasificador. Antes sí lo era |
| **v2.1.202** | Reinvocar una skill con contenido idéntico **ya no añade otra copia completa** a la conversación |
| **v2.1.208** | Una entrada rechazada por Grep **devuelve el error de ripgrep**. Antes reportaba `No files found` aunque el texto existiera |
| **v2.1.210** | Un `MEMORY.md` por encima del límite **avisa al escribir**. Antes se truncaba en silencio |
| **v2.1.211** | La comprobación de secretos en un push aplica **en cualquier rama**. Antes estaba acotada a la rama por defecto |
| **v2.1.214** | Un `pkill` cuyo patrón case con el proceso de Claude Code **se rechaza**. Antes corría y mataba la sesión. **Solo en Linux** |
| **v2.1.217** | Se reconoce la redacción de Bedrock `Input is too long for requested model.` Antes la autocompactación **nunca se disparaba** con ese mensaje |
| **v2.1.218** | Las skills bifurcadas **ya no bloquean el turno** por defecto. Y los booleanos del frontmatter aceptan `yes`/`no`/`on`/`off`/`1`/`0`, no solo `true`/`false` |
| **v2.1.223** | El bloque `env` de los settings gestionados **se fusiona por clave** entre fuentes |
| **v2.1.228** | Una regla `deny` de **lectura** bloquea también `Write`, no solo `Edit` |
| **Semana 32** | El aislamiento de worktrees bloquea también **comandos Bash y redirecciones de git**, no solo ediciones de archivo · un repositorio **ya no puede activar** la conexión automática de Remote Control, solo desactivarla · los hooks `PreToolUse` de auto-permitir **ya no saltan restricciones** en las tareas internas de Claude Code |

---

## 21.7 · Cómo saber si tu fuente está caducada

Cuatro señales, en orden de fiabilidad:

1. **Habla de `/ultraplan`.** Está retirado. La fuente es de antes de agosto.
2. **Dice que los subagentes bloquean.** Corren en segundo plano desde la semana 27.
3. **Dice que hay un tope de 200 subagentes.** Se eliminó en la semana 32.
4. **Dice que MCP carga todas sus herramientas en contexto.** Van diferidas por
   defecto, y esta guía tuvo publicado ese mismo error hasta que lo verificó.

Y la regla general, que es la razón de ser de todo este proyecto: **pregúntale la
versión al binario, no al artículo.** `claude --version` decide quién tiene razón.

---

## Checklist de verificación

- [ ] He comprobado la versión de mi CLI antes de seguir cualquier tutorial.
- [ ] Sé que auto mode pasa a ser el modo por defecto el 14 de agosto de 2026.
- [ ] Sé que mis subagentes corren en segundo plano por defecto.
- [ ] No tengo `/ultraplan` en ningún script.
- [ ] Si uso el SDK de TypeScript, no dependo de la API de sesiones V2.
- [ ] Si uso Slack en Team o Enterprise, conozco la migración a Claude Tag.
- [ ] Mi documentación interna lleva fecha y versión verificada.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "El tutorial dice `/ultraplan` y no existe" | Retirado en la semana 32 |
| "Mi subagente no bloquea como esperaba" | Segundo plano por defecto desde la semana 27 |
| "De pronto ya no me pregunta por los permisos" | Auto mode pasó a ser el modo por defecto |
| "Mi script del SDK dejó de compilar" | API de sesiones V2 eliminada en 0.3.142 |
| "Pulso `f` en `/doctor` y no pasa nada" | Cambió en v2.1.205 |
| "Mi `pkill` ya no funciona" | Se rechaza si casa con el proceso. Solo en Linux |
| "Comparo dos máquinas y dan resultados distintos" | Versiones distintas. Media docena de comportamientos cambian |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `changelog.md` | 528.057 | Los endurecimientos por versión y las semanas sin digest |
| `whats-new/2026-w25` a `w30`, `w32` | 4.324 a 8.830 cada uno | Tabla 15, titulares y rangos de versión |
| `whats-new/index.md` | 12.587 | Índice de digests, que confirma la ausencia de w31 |

Verificación propia: `claude --version` sobre el binario instalado, y el contraste
del inventario documental hecho en la Fase 0.

**Marcas pendientes:** ninguna. Los digests de la semana 31 y la 33 **no existen**,
y eso está declarado como hueco de fuente en 21.1 y 21.2, no como omisión.
