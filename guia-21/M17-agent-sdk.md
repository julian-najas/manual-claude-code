# M17 · Agent SDK

> **Para quién es:** quien construye producto, no quien usa la herramienta.
> **Qué resuelve:** cuándo dejar el CLI, y qué te llevas al hacerlo.
> **Qué NO cubre:** el uso interactivo diario, que es todo lo anterior.

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 17.1 · Cuál de las cuatro cosas necesitas

Hay cuatro formas de construir sobre Claude y elegir mal cuesta meses:

| Si estás... | Usa | Por qué |
|---|---|---|
| Construyendo un agente **sin implementar tú el bucle de herramientas** | **Agent SDK** | Una biblioteca que corre el bucle **en tu propio proceso**, en Python o TypeScript |
| Haciendo desarrollo interactivo o tareas puntuales desde el terminal | **CLI** | La interfaz de terminal, para uso diario |
| Llamando a la API directamente e **implementando tú el bucle** | **Client SDK** | Control total, y todo el trabajo |
| Queriendo agentes alojados con sandbox gestionado | **Managed Agents** | No operas tú la infraestructura |

La frase que define el Agent SDK: te da **las mismas herramientas, el mismo bucle
de agente y la misma gestión de contexto que mueven Claude Code**, programables.

💡 **Opinión operativa.** La señal de que te toca el SDK no es la complejidad, es
**quién invoca**. Mientras el que arranca la tarea sea una persona con un
terminal, el CLI en modo no interactivo del M10 te llega para casi todo. En cuanto
quien arranca es **tu producto**, y hay usuarios que no son tú, el CLI se te queda
corto en sesiones, permisos y almacenamiento, que son justo las tres cosas que el
SDK resuelve.

---

## 17.2 · Los dos modos de entrada, y cuál se recomienda

**Modo de entrada en streaming**, que es **el preferido**: una sesión persistente
e interactiva. Deja que el agente funcione como un **proceso de vida larga** que
recibe entrada, **maneja interrupciones**, **expone peticiones de permiso** y
gestiona la sesión.

**Mensaje único**: consultas de un tiro que usan estado de sesión y reanudación.

La diferencia práctica no es de comodidad, es de **qué puedes construir**. Sin
streaming no hay interrupciones ni diálogo de permisos, y sin eso no hay producto
con humano en el bucle: solo un trabajo por lotes.

---

## 17.3 · Sesiones, y dónde viven de verdad

Por defecto el SDK escribe las transcripciones de sesión en archivos JSONL bajo
`~/.claude/projects/`, **en el sistema de archivos local**.

Eso está bien en una máquina y se rompe en cuanto tienes producto. Por eso existe
el adaptador **`SessionStore`**, que refleja esas transcripciones en tu propio
backend: S3, Redis, una base de datos.

Tres motivos, y los tres son de producción:

- **Despliegues multi-host.** Funciones serverless, trabajadores autoescalados y
  runners de CI **no comparten sistema de archivos**. Un almacén compartido deja
  que **cualquier réplica reanude cualquier sesión**.
- **Durabilidad.** Los contenedores locales son efímeros. Un almacén sobre S3 o
  base de datos sobrevive a reinicios y redespliegues.
- **Cumplimiento y auditoría.** Guardar las transcripciones **en almacenamiento
  que ya gobiernas**, con tus reglas de retención, tu cifrado y tus controles de
  acceso.

Ese tercer punto conecta directamente con el M16: si tu DPO pregunta dónde viven
las conversaciones de tu producto, **la respuesta correcta es "en nuestro almacén,
con nuestra retención"**, y el mecanismo para que sea verdad es este.

La interfaz es deliberadamente pequeña: **dos métodos obligatorios, `append` y
`load`**, y cuatro opcionales. Implementarla contra un backend propio es trabajo
de una tarde, no de un sprint.

---

## 17.4 · Salidas estructuradas

Los agentes devuelven texto libre por defecto, que sirve para chat y no sirve
cuando la salida alimenta a otro sistema.

Con salidas estructuradas defines la forma exacta de los datos con **JSON Schema**,
y para seguridad de tipos completa con **Zod** en TypeScript o **Pydantic** en
Python. El agente usa las herramientas que necesite para completar la tarea, y **al
final obtienes JSON validado contra tu esquema**.

Dos comportamientos que hay que conocer antes de confiar en ello:

1. **El SDK valida y vuelve a preguntar si no casa.** No falla al primer intento.
2. **Si la validación no pasa dentro del límite de reintentos, el resultado es un
   error, no datos estructurados.** Tu código tiene que contemplar esa rama, y es
   la que nadie escribe hasta que la ve en producción.

---

## 17.5 · Herramientas propias, permisos y hooks

Las tres piezas que convierten el SDK en algo que puedes desplegar:

**Herramientas propias.** Expones funciones tuyas al bucle. Es la vía natural para
que el agente hable con tu dominio sin montar un servidor MCP.

**Permisos.** El mismo modelo del M5, programable. Aquí es donde se decide qué
puede tocar el agente **de tus usuarios**, que es otra conversación que cuando el
usuario eres tú.

**Hooks.** Los mismos eventos del M10, disponibles desde el SDK. Es lo que permite
poner puertas de calidad deterministas dentro de tu producto.

Y del M8: **MCP desde el SDK**, con su propia página de tool search, así que el
comportamiento diferido del contexto también aplica aquí.

---

## 17.6 · Coste: el aviso que hay que leer dos veces

⚠️ **Esta es la advertencia más importante del módulo y encaja exactamente con la
regla de esta guía sobre no inventar euros.** La documentación lo dice sin rodeos:

> Los campos `total_cost_usd` y `costUSD` son **estimaciones del lado del cliente,
> no datos autorizados de facturación**. El SDK los calcula localmente a partir de
> **una tabla de precios empaquetada en tiempo de compilación**.

Y lista los tres casos en los que se desvían de lo que te facturan de verdad:

1. **Cuando cambian los precios.** Tu tabla es la del día que se compiló el SDK.
2. **Cuando la versión instalada del SDK no reconoce un modelo.**
3. **Cuando aplican reglas de facturación que el cliente no puede modelar.**

La recomendación oficial: úsalos para **desarrollo y presupuesto aproximado**, y
para facturación autorizada **la API de uso y coste**.

💡 Si construyes un producto que **repercute costes a tus clientes**, esto no es un
matiz: es un requisito. Facturar a un tercero con una estimación calculada contra
una tabla de precios congelada en tiempo de compilación es un problema que se
descubre tarde y en forma de discusión con un cliente.

Del M15, y aplica igual aquí: los tokens se miden, los euros se consultan.

---

## 17.7 · Despliegue seguro

La página de despliegue seguro plantea el problema con una honestidad que merece
citarse, porque es el mejor resumen del M5 escrito desde el lado de quien
construye:

> A diferencia del software tradicional, que sigue rutas de código
> predeterminadas, estas herramientas **generan sus acciones dinámicamente** según
> el contexto y los objetivos. Esa flexibilidad es lo que las hace útiles, pero
> también significa que **su comportamiento puede verse influido por el contenido
> que procesan**: archivos, páginas web o entrada de usuario.

Y añade el criterio que evita tanto la paranoia como la negligencia:

> **No todos los despliegues necesitan seguridad máxima.** Un desarrollador
> corriendo Claude Code en su portátil tiene requisitos distintos de una empresa
> procesando datos de clientes en un entorno multi-inquilino.

Las tres palancas, que son las mismas del M5 pero decididas por ti y no por el
usuario: **aislamiento**, **gestión de credenciales** y **controles de red**.

En un producto multi-inquilino la pregunta cambia de "¿qué puede tocar el agente?"
a **"¿qué puede tocar el agente del inquilino A que pertenezca al inquilino B?"**,
y esa no se responde con permisos: se responde con aislamiento de proceso y de
almacenamiento.

---

## 17.8 · Lo que se ha retirado

⚠️ **La API de sesiones V2 de TypeScript ya no está soportada.** El SDK de
TypeScript **0.3.142 elimina** `unstable_v2_createSession`,
`unstable_v2_resumeSession`, `unstable_v2_prompt` y los tipos `SDKSession` y
`SDKSessionOptions`.

La migración es a la API `query()` con las opciones de sesión que acepta: se pasa
un `AsyncIterable<SDKUserMessage>` para conversaciones de varios turnos, o
`options.resume` para continuar una sesión guardada.

Era una API experimental que quitaba la necesidad de generadores asíncronos, con
cada turno como un ciclo `send()`/`stream()` separado. Si mantienes código en
0.2.x o anterior, la página sigue publicada como referencia.

Este apartado va también al M21: si alguien copia un tutorial de hace unos meses,
va a copiar exactamente estas cinco cosas.

---

## 17.9 · El esqueleto de un agente, decidido pieza a pieza

Más útil que un ejemplo de cien líneas es la lista de decisiones, en el orden en
que hay que tomarlas:

1. **Modo de entrada.** Streaming, salvo que tu caso sea de verdad un tiro único.
2. **Dónde viven las sesiones.** ¿Un host o varios? Si son varios, `SessionStore`
   desde el día uno, no cuando escales.
3. **Qué devuelve.** Si otro sistema consume la salida, esquema y validación, con
   la rama de error contemplada.
4. **Qué herramientas propias expone**, y cuáles de las integradas se desactivan.
5. **Qué permisos tiene**, y en un producto multi-inquilino, respecto a quién.
6. **Qué hooks son obligatorios.** Lo que no puede pasar nunca es código, no
   instrucción. Aplica igual dentro del SDK.
7. **Cómo se mide el coste**, sabiendo que el campo del SDK es una estimación.
8. **Cómo se aísla**, según el modelo de amenazas real y no el máximo teórico.
9. **Dónde se aloja** y con qué credenciales, del 17.7.

Las nueve tienen su página en el inventario del SDK. Ninguna se puede aplazar a
"cuando esté en producción", porque las tres primeras condicionan la arquitectura
entera.

---

## Checklist de verificación

- [ ] He comprobado que necesito el SDK y no el CLI en modo no interactivo.
- [ ] Uso modo streaming salvo justificación.
- [ ] Si despliego en más de un host, tengo `SessionStore`.
- [ ] Mis transcripciones viven donde mi organización las gobierna.
- [ ] Mi código contempla que la salida estructurada falle tras los reintentos.
- [ ] **Sé que `total_cost_usd` es una estimación del cliente.**
- [ ] Si repercuto costes, uso la API de uso y coste como fuente autorizada.
- [ ] Mi aislamiento se corresponde con mi modelo de amenazas real.
- [ ] No uso la API de sesiones V2 de TypeScript.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "No puedo interrumpir al agente" | Estás en mensaje único. El streaming es el modo recomendado |
| "Una réplica no reanuda la sesión de otra" | Transcripciones en disco local. Necesitas `SessionStore` |
| "A veces devuelve un error en vez de mi JSON" | Falló la validación tras los reintentos. Es una rama esperada |
| "Mi coste no cuadra con la factura" | El campo del SDK es una estimación con tabla congelada |
| "`unstable_v2_createSession` ya no existe" | Eliminado en TypeScript SDK 0.3.142. Migra a `query()` |
| "El agente de un cliente vio datos de otro" | Eso no lo arreglan los permisos: es aislamiento |
| "Nuestro DPO pregunta dónde están las conversaciones" | Por defecto en disco local. `SessionStore` a vuestro almacén |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/agent-sdk/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `overview.md` | 9.069 | La comparación entre las cuatro formas de construir |
| `agent-loop.md` | 48.429 | El bucle programable |
| `sessions.md` | 23.306 | Sesiones |
| `session-storage.md` | 23.466 | `SessionStore` y sus tres motivos |
| `streaming-vs-single-mode.md` | 10.385 | Los dos modos de entrada |
| `structured-outputs.md` | 21.249 | Esquemas, validación y la rama de error |
| `custom-tools.md` | 40.813 | Herramientas propias |
| `permissions.md` | 22.608 | Permisos programables |
| `hooks.md` | 54.040 | Hooks desde el SDK |
| `cost-tracking.md` | 24.111 | **El aviso sobre `total_cost_usd`** |
| `secure-deployment.md` | 24.030 | Aislamiento, credenciales, red |
| `hosting.md` | 23.866 | Alojamiento |
| `migration-guide.md` | 8.212 | Migración |
| `typescript-v2-preview.md` | 12.266 | La API V2 retirada |

**Marcas pendientes:** de las 32 páginas del SDK he leído 14 en esta pasada. Las
18 restantes (referencias de TypeScript y Python, skills, plugins, subagentes,
tool search, todo-tracking, observability, quickstart, examples, troubleshooting,
user-input, file-checkpointing, claude-code-features, modifying-system-prompts,
slash-commands, mcp, python, typescript) están inventariadas y **no leídas**. Este
módulo es el mapa de decisiones, no la referencia de la API: **para firmas
concretas hay que ir a las referencias de TypeScript y Python**, y así se dice
aquí en vez de inventarlas.
