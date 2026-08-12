# M7 · Extensión: skills, comandos, output styles y barra de estado

> **Para quién es:** quien ya repite tareas y quiere dejar de repetirlas a mano.
> **Qué resuelve:** la skill que escribiste bien y no se activa nunca sola.
> **Qué NO cubre:** repartirlo al equipo (M11) ni paralelizar trabajo (M9).

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 7.1 · Anatomía de una skill

Una skill es un `SKILL.md` con frontmatter YAML y un cuerpo en markdown:

```yaml
---
name: mi-skill
description: Qué hace esta skill
disable-model-invocation: true
allowed-tools: Read Grep
---

Aquí van las instrucciones.
```

**Todos los campos son opcionales.** Solo se recomienda `description`, para que
Claude sepa cuándo usarla. Si falta `name`, se usa el nombre del directorio.

Detalle menor con consecuencias: los campos booleanos aceptan `yes`, `no`, `on`,
`off`, `1` y `0` en cualquier combinación de mayúsculas, además de `true` y
`false`. **Antes de v2.1.218 solo se reconocían `true` y `false`**, así que una
skill escrita con `yes` no hará lo que crees en una máquina con versión anterior.

---

## 7.2 · La descripción es el disparador

Este es el punto que separa una skill que sirve de una que se queda dormida para
siempre, y ahora tiene respaldo documental.

**La descripción no es documentación: es el texto contra el que Claude decide si
la tarea encaja.** Se escribe con las palabras que diría quien pide el trabajo,
no con las que usarías para catalogarlo.

El procedimiento oficial cuando una skill no se dispara, en orden:

1. Comprueba que la descripción incluye **las palabras clave que la gente diría de
   forma natural**.
2. Verifica que aparece al preguntar `¿Qué skills hay disponibles?`.
3. Reformula tu petición para acercarla a la descripción, y observa qué palabra la
   activa.
4. Invócala directamente con `/nombre-de-skill` si es invocable por el usuario.

⚠️ **Y la causa que nadie diagnostica sola.** Si el YAML del frontmatter está mal
formado, **Claude Code carga el cuerpo de la skill con los metadatos vacíos**. El
resultado es de manual de terror: `/nombre-de-skill` sigue funcionando
perfectamente a mano, así que juras que la skill está bien, pero Claude **no tiene
ninguna `description` contra la que casar** y por eso no se activa nunca sola.
Se ve con `--debug`, que muestra el error de análisis.

Si tuvieras que quedarte con un solo dato de este módulo, quédate con ese.

---

## 7.3 · El ciclo de vida del contenido

La sección que más cambia la forma de escribir skills, y la que casi nadie conoce.

Cuando se invoca una skill, **el contenido renderizado entra en la conversación
como un único mensaje y se queda ahí el resto de la sesión**. Claude Code **no
vuelve a leer el archivo** en turnos posteriores.

Consecuencia directa para quien escribe: lo que deba aplicarse durante toda la
tarea se redacta como **instrucción permanente**, no como paso puntual. "Ahora
haz X" envejece mal; "durante esta tarea, siempre X" es lo correcto.

Tres comportamientos derivados que conviene tener claros:

- **La persistencia es del contenido, no de los permisos.** Un `allowed-tools`
  caduca en cuanto envías tu siguiente mensaje, aunque el texto de la skill siga
  en contexto.
- **Reinvocar con contenido idéntico no duplica.** Claude Code añade una nota
  corta de que ya está cargada. Si el contenido cambió, porque cambiaron los
  argumentos o el contexto dinámico, sí se añade entero otra vez. **Antes de
  v2.1.202, cada reinvocación añadía otra copia completa.**
- **La compactación arrastra las skills con presupuesto.** Al resumir, Claude Code
  reengancha la invocación más reciente de cada skill después del resumen,
  conservando **los primeros 5.000 tokens de cada una**, con un **presupuesto
  conjunto de 25.000 tokens**. Se llena empezando por la más reciente, así que
  **las skills antiguas pueden desaparecer del todo**.

💡 **Opinión operativa.** Esos dos números explican un fallo que se diagnostica
fatal: una sesión larga con seis skills invocadas y una tarea que "de repente deja
de seguir el procedimiento". No es que se olvide: es que esa skill se quedó fuera
del presupuesto de 25.000 tokens al compactar. La cura no es repetir la
instrucción, es volver a invocar la skill o mover lo esencial al `CLAUDE.md`.

---

## 7.4 · Argumentos y contexto dinámico

La sintaxis `` !`<comando>` `` **ejecuta comandos de shell antes** de que el
contenido de la skill se envíe. La salida sustituye al marcador, así que Claude
recibe datos reales y no el comando.

```yaml
---
name: pr-summary
description: Resume los cambios de una pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

Diff de la PR:
!`gh pr diff`
```

Es la diferencia entre una skill que le pide a Claude que vaya a buscar algo, con
sus turnos y su coste, y una que **ya llega con el dato dentro**.

---

## 7.5 · Pre-aprobar herramientas

`allowed-tools` concede permiso para las herramientas listadas **durante el turno
que invoca la skill**, para que Claude las use sin pedirte aprobación.

Cuatro precisiones que evitan malentendidos peligrosos:

1. **El permiso caduca con tu siguiente mensaje.** Invocarla otra vez lo vuelve a
   aplicar para ese turno.
2. **No restringe nada.** Todas las herramientas siguen siendo invocables; tus
   ajustes de permisos siguen gobernando las que no estén listadas. Es una lista
   de pre-aprobación, no una jaula.
3. Para pre-aprobar durante toda la sesión, lo correcto son reglas `allow` en los
   permisos, no esto.
4. ⚠️ **Para skills confirmadas en el `.claude/skills/` de un proyecto,
   `allowed-tools` surte efecto tras aceptar el diálogo de confianza del espacio
   de trabajo.** Y aquí está el aviso literal de la documentación, que conviene
   traducir sin suavizar: **revisa las skills de un proyecto antes de confiar en
   el repositorio, porque una skill puede concederse a sí misma acceso amplio a
   herramientas.**

Es el mismo patrón del M3 y del M5. Ya van cuatro puertas que dependen del mismo
diálogo de confianza: hooks, `autoMemoryDirectory`, permisos de proyecto y ahora
las skills del repositorio.

---

## 7.6 · Ejecutar una skill en un subagente

`context: fork` en el frontmatter hace que la skill corra aislada. El contenido de
la skill **pasa a ser el prompt que dirige al subagente**, que **no tiene acceso a
tu historial de conversación**.

Por defecto el subagente bifurcado corre **en segundo plano**: sigues trabajando y
su resultado llega cuando termina. Con `background: false` esperas el resultado en
el mismo turno. **Antes de v2.1.218, las skills bifurcadas siempre bloqueaban el
turno.**

Claude Code espera igualmente, aunque no pongas `background: false`, en estos
casos: en modo no interactivo con `-p` o con el SDK; con
`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`; cuando invocas una skill bifurcada
mientras otra invocación de la misma sigue corriendo; y cuando la dispara una
tarea programada.

---

## 7.7 · Cuando se activa demasiado

El problema simétrico al de 7.2, y se resuelve por el mismo sitio: la descripción
es demasiado genérica y casa con tareas que no le tocan. Se estrecha nombrando el
dominio y el disparador concreto.

Si quieres que **solo** se invoque a mano, `disable-model-invocation: true`. Como
bonus, eso mantiene su descripción fuera del contexto hasta que la necesites, que
es la recomendación que ya salía en la tabla 5 del M4.

---

## 7.8 · Output styles: qué son y qué no

Los output styles **cambian cómo responde Claude, no lo que sabe**. Modifican el
system prompt para fijar rol, tono y formato de salida. Se usan cuando te
descubres repitiendo la misma indicación de voz o formato en cada turno, o cuando
quieres que Claude actúe como algo que no es un ingeniero de software.

Un estilo propio añade tus instrucciones al system prompt y te deja elegir si
conservas las instrucciones de ingeniería integradas: **consérvalas** si sigues
programando y solo cambias la comunicación, **quítalas** si Claude no está
haciendo ingeniería en absoluto, como un asistente de redacción o de análisis de
datos.

Los tres estilos integrados además del **Default**:

- **Proactive**: ejecuta de inmediato, asume lo razonable en vez de parar ante
  decisiones rutinarias y prefiere la acción a la planificación. Es una guía de
  ejecución autónoma **más fuerte que la de auto mode**, y funciona **sin cambiar
  tu modo de permisos**: sigues viendo las confirmaciones antes de que corran las
  herramientas.
- **Explanatory**: intercala "Insights" educativos mientras trabaja, para
  entender las decisiones de implementación y los patrones del código.
- **Learning**: modo colaborativo de aprender haciendo. Además de los "Insights",
  **te pide que escribas tú piezas pequeñas y estratégicas de código**, dejando
  marcadores `TODO(human)` para que los implementes.

Se elige con `/config` → **Output style**, y la selección se guarda en
`.claude/settings.local.json`, a nivel local del proyecto. En la aplicación de
escritorio se fija el campo `outputStyle` en ese mismo archivo.

Ese matiz de **Proactive** es importante y se malinterpreta constantemente:
cambiar el estilo de salida **no te quita ninguna barrera de permisos**. Son ejes
independientes, y confundirlos lleva a creer que se ha bajado la guardia cuando no
es así, o al revés.

### La comparación que hay que tener clara

| | Qué cambia | Dónde vive | Cuándo usarlo |
|---|---|---|---|
| **Output style** | Cómo responde: rol, tono, formato | System prompt | Repites la misma indicación de voz o formato cada turno |
| **System prompt propio** | El comportamiento base entero | Flags del CLI o SDK | Construyes producto sobre Claude Code |
| **`CLAUDE.md`** | Qué sabe del proyecto | Repositorio o usuario | Convenciones, arquitectura, comandos |

La regla, literal de la documentación: **para instrucciones sobre tu proyecto, tus
convenciones o tu código, usa `CLAUDE.md`, no un output style.**

---

## 7.9 · Barra de estado

Es una barra configurable al pie que **ejecuta cualquier script de shell**: recibe
datos de sesión en JSON por la entrada estándar y muestra lo que tu script
imprima. Sirve para vigilar el uso del contexto, el coste acumulado, el estado de
git o para distinguir sesiones cuando llevas varias abiertas.

⚠️ **El coste oculto de ponerla, que no cuenta casi nadie.** La barra se dibuja en
su propia fila encima de las insignias del pie, pero **con una barra de estado
configurada, Claude Code deja de mostrar la mayoría de las pistas de teclado del
pie**, incluidas `esc to interrupt`, el `? for shortcuts` y la de mantener espacio
para dictar. Si tu equipo tiene gente que empieza, es un peaje real: ganas
métricas y pierdes descubribilidad.

Si lo único que querías eran insignias con enlace cuando aparece un
identificador en la conversación, existe `footerLinksRegexes` y no requiere script
ninguno.

---

## 7.10 · La interfaz alrededor

- **Renderizado a pantalla completa**: modo sin parpadeo, con soporte de ratón y
  uso de memoria estable en conversaciones largas. Está marcado como **research
  preview**. Regla de activación que sorprende: **si empezaste a usar Claude Code
  el 6 de mayo de 2026 o después, se renderiza a pantalla completa por defecto**;
  si empezaste antes, conservas el clásico. Se cambia con `/tui default` y
  `/tui fullscreen`.
- **Dictado por voz**: se habilita con `/voice`, y luego o mantienes una tecla
  mientras hablas o pulsas una vez para empezar y otra para enviar. Se transcribe
  en vivo sobre el campo de entrada, así que puedes mezclar voz y teclado en el
  mismo mensaje.
- **Lector de pantalla**: hay un modo que sustituye la interfaz visual por texto
  plano y lineal. En vez de cajas, animaciones de progreso y redibujados en el
  sitio, imprime líneas etiquetadas. Cubre también lupas de pantalla, movimiento
  reducido y temas aptos para daltonismo.
- **Atajos de teclado**: reconfigurables, con soporte de combinaciones.

---

## Checklist de verificación

- [ ] Cada una de mis skills tiene `description` escrita con las palabras del que pide la tarea.
- [ ] He arrancado con `--debug` al menos una vez para descartar YAML mal formado.
- [ ] Mis skills están escritas como instrucciones permanentes, no como pasos puntuales.
- [ ] Sé que `allowed-tools` caduca con mi siguiente mensaje.
- [ ] He revisado las skills del repositorio **antes** de aceptar la confianza del espacio de trabajo.
- [ ] Las skills que solo lanzo yo llevan `disable-model-invocation: true`.
- [ ] Sé que mi output style no cambia mis permisos.
- [ ] Si pongo barra de estado, mi equipo sabe que desaparecen las pistas del pie.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "`/mi-skill` funciona pero nunca se activa sola" | Frontmatter mal formado: cuerpo cargado, metadatos vacíos. `--debug` |
| "Se activa cuando no toca" | Descripción demasiado genérica. Estréchala o desactiva la invocación por modelo |
| "Dejó de seguir el procedimiento a mitad de sesión" | Compactó y esa skill se salió del presupuesto de 25.000 tokens |
| "Me sigue pidiendo permiso pese a `allowed-tools`" | Caducó con tu mensaje anterior. Reinvoca, o usa reglas `allow` |
| "El subagente de la skill no sabe de qué hablamos" | `context: fork` no comparte tu historial. Por diseño |
| "Puse `yes` en un booleano y no funciona" | Requiere v2.1.218 o posterior |
| "Cambié el output style y sigue pidiendo permisos" | Correcto. Son ejes independientes |
| "Han desaparecido las pistas de teclado del pie" | Tienes barra de estado configurada |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `skills.md` | 88.121 | Frontmatter, ciclo de vida, argumentos, fork, diagnóstico |
| `statusline.md` | 64.067 | Barra de estado y el coste en pistas del pie |
| `output-styles.md` | 10.270 | Estilos integrados y la comparación con `CLAUDE.md` |
| `fullscreen.md` | 23.243 | Research preview y regla del 6 de mayo |
| `voice-dictation.md` | 16.045 | `/voice` |
| `accessibility.md` | 12.164 | Modo lector de pantalla |
| `keybindings.md` | 31.968 | Atajos reconfigurables |

**Marcas pendientes:** ninguna. Los cuatro estilos integrados quedan documentados
y la forma de cambiarlos también.
