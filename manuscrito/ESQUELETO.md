# Esqueleto del manuscrito

**Libro:** Claude Code en producción
**Versión:** v2026.08 · **Cada módulo declara la versión del CLI con la que se
escribió y se midió.** El libro no tiene una versión única.
**Objetivo de extensión:** 240 páginas (12 módulos × ~18 pp + preliminares y cierre)

Este archivo es el contrato de la obra. Cualquiera que escriba un módulo escribe
contra esto. Si un módulo no cumple el esqueleto, no entra, por bueno que sea el
texto.

---

## 1 · El esqueleto fijo de cada módulo

Los doce módulos tienen **exactamente** estas seis partes, en este orden. La
repetición no es pereza: es lo que permite auditar el libro y lo que permite al
lector saltar directamente a la parte que necesita.

| # | Parte | Qué contiene | Extensión |
|---|---|---|---|
| 1 | **Síntoma** | El problema real con el que llega el lector, escrito como lo diría él. Nunca "en este capítulo aprenderás". | ½ pp |
| 2 | **Modelo mental** | Cómo funciona la pieza por dentro, lo justo para decidir bien. Sin arqueología. | 3-4 pp |
| 3 | **Receta** | El procedimiento, en versión individual y en versión equipo. Con el archivo real. | 5-7 pp |
| 4 | **Laboratorio** | Sobre `gestor-pedidos`, el repo feo. Siempre sobre el mismo repo. | 4-5 pp |
| 5 | **Prueba** | Criterio PASA/FALLA objetivo. Nada de "deberías ver algo parecido". | ½ pp |
| 6 | **Coste** | Qué gasta esta pieza: en contexto, en tokens y en mantenimiento. | 1 pp |

**Invariantes de todos los módulos:**

- Abre con la **factura estimada del laboratorio** en tokens y euros.
- Cada afirmación comprobable tiene su ID en `D2-verificador/registro.yaml`.
- Las marcas de versión van **al margen, en la línea que importa**, no en un anexo.
- Lo inestable se marca con una caja "esto va a cambiar". Se marca, no se oculta.
- Cero capturas de pantalla de la terminal. Bloques de texto copiables.
- Cierra con un **runbook de una página**, imprimible, sin prosa.

---

## 2 · Las dos rutas de lectura

**Ruta corta, el sistema mínimo (2 horas).** Módulos 2, 3, 4 y 5, y solo la parte
"Receta" de cada uno. Con eso el lector tiene un proyecto configurado, con
permisos sanos y con lo que no es negociable convertido en hooks. El índice marca
esta ruta con una banda al margen.

**Ruta completa.** Los doce módulos en orden. Es la que convierte a un usuario en
alguien que puede implantarlo en un equipo.

---

## 3 · Los doce módulos

### Módulo 01 · Fundamentos y el árbol de decisión
**Síntoma de entrada:** "Lo uso todos los días y sigo sin saber dónde va cada cosa."
**Promesa:** salir sabiendo decidir entre las siete piezas sin dudar.
**Contenido:** qué es un agente de codificación frente a un chat con código. La
tesis del libro: rol, memoria, herramientas, límites, control de calidad y
métricas. El árbol de decisión completo (Lámina 1). El impuesto de contexto de
cada pieza. Los cinco niveles de madurez y el test de autodiagnóstico.
**Laboratorio:** primer contacto con `gestor-pedidos`. Pedirle que explique la app.
**PASA si:** el lector detecta al menos una afirmación falsa en el resumen del
agente, causada por el README mentiroso del repo.
**Activos:** Lámina 1, test de autodiagnóstico.
**Verifica:** ninguna afirmación de CLI; es el módulo conceptual.

### Módulo 02 · Instalación, autenticación y versiones
**Síntoma:** "A mi compañero le funciona un comando que a mí no me existe."
**Promesa:** entorno reproducible y saber siempre contra qué versión trabajas.
**Contenido:** instalación, autenticación y sus modos, token de larga duración,
diagnóstico de la instalación. Por qué la versión del CLI es un dato de primera
clase en un proyecto de equipo, y cómo se fija y se anota.
**Laboratorio:** dejar el entorno reproducible y anotar la versión en el repo.
**PASA si:** el diagnóstico sale limpio y la versión queda escrita en el repositorio.
**Verifica:** `CLI-001`, `CLI-002`, `CLI-003`.

### Módulo 03 · Memoria y contexto
**Síntoma:** "Se me acaba el contexto a media tarea y se le olvida lo que le dije."
**Promesa:** un `CLAUDE.md` que dice la verdad y una sesión que no se ahoga.
**Contenido:** qué se carga y cuándo. Jerarquía de memoria: usuario, proyecto,
directorio. Qué merece estar siempre presente y qué no. Compactación y su coste.
Los directorios adicionales. El modo mínimo como herramienta de diagnóstico.
**Laboratorio:** escribir el primer `CLAUDE.md` de `gestor-pedidos` resolviendo
las dos contradicciones del repo: qué configuración manda y qué código está muerto.
**PASA si:** el agente deja de proponer cambios sobre el endpoint muerto y sobre
el archivo de configuración equivocado, sin que se lo recuerdes.
**Verifica:** `CTX-001`, `CTX-002`, `CTX-003`.

### Módulo 04 · Permisos y sandbox
**Síntoma:** "O me pregunta por todo, o le doy permiso para todo. No hay medio."
**Promesa:** permisos versionados en el repositorio y un sitio seguro donde fallar.
**Contenido:** el modelo de permisos, los tres perfiles (cauto, normal,
laboratorio) y qué se rompe al pasar de uno a otro. Herramientas permitidas de
forma explícita. La bandera peligrosa: dónde sí y dónde nunca. Contenedor de
desarrollo con red restringida.
**Laboratorio:** configurar permisos para `gestor-pedidos` y prohibir la lectura
de las rutas con secretos.
**PASA si:** el agente no puede leer el archivo con la clave de pasarela **y lo
dice**, en vez de fallar en silencio.
**Verifica:** `PRM-001`, `PRM-002`, `PRM-003`.
**Activos:** tres perfiles de permisos listos, contenedor de desarrollo.

### Módulo 05 · Hooks
**Síntoma:** "Le he dicho mil veces que haga X y unas veces lo hace y otras no."
**Promesa:** lo que no es negociable deja de depender del criterio de nadie.
**Contenido:** el ciclo de vida y sus puntos de enganche. Determinismo frente a
instrucción: la frase que abre el libro por dentro. Cómo se depura un hook.
Cuándo un hook es peor que una instrucción.
**Laboratorio:** dos hooks sobre `gestor-pedidos`: veto de lectura de secretos y
formateo automático al editar.
**PASA si:** intentar leer la clave se bloquea, y editar cualquier `.py` lo deja
formateado sin pedirlo.
**Verifica:** `HOK-001` (marcada como revisión humana trimestral).
**Activos:** los diez hooks de la biblioteca.

### Módulo 06 · MCP
**Síntoma:** "Necesito que consulte la base de datos sin darle acceso a escribir."
**Promesa:** conectar sistemas externos sin regalar el contexto ni los permisos.
**Contenido:** qué es y qué no es MCP. El impuesto permanente: cada servidor mete
sus definiciones de herramientas en cada turno. Servidores de terceros como
superficie de ataque. Construir un servidor propio de solo lectura.
**Laboratorio:** conectar la base de datos de `gestor-pedidos` en solo lectura.
**PASA si:** el agente responde cuántos pedidos hay sin abrir un archivo de datos.
**Verifica:** `MCP-001`.
**Activos:** el servidor MCP de solo lectura construido en el libro.

### Módulo 07 · Skills y plugins
**Síntoma:** "Escribí una skill perfecta y no se activa nunca sola."
**Promesa:** procedimientos que se encienden solos cuando toca, y que se reparten.
**Contenido:** anatomía de una skill. **La descripción es el disparador, no la
documentación**: cómo se escribe. Divulgación progresiva y por qué el cuerpo no
debe cargarse entero. Empaquetar en plugin para el equipo. Cuándo un comando es
mejor que una skill.
**Laboratorio:** convertir "auditar un endpoint" en una skill de `gestor-pedidos`.
**PASA si:** la skill se dispara sin nombrarla, solo describiendo la tarea.
**Verifica:** `SKL-001`, `SKL-002`.
**Activos:** biblioteca de skills, los cuatro comandos de equipo.

### Módulo 08 · Subagentes
**Síntoma:** "Le pido que revise su propio trabajo y siempre se da el visto bueno."
**Promesa:** un segundo par de ojos que de verdad tiene criterio distinto.
**Contenido:** contexto separado y qué implica. Por qué el revisor no puede ser el
autor. El contrato de un subagente: rol, límites, criterio de aceptación, formato
de salida. Cuándo un subagente sale caro.
**Laboratorio:** un subagente revisor sobre `gestor-pedidos`.
**PASA si:** el revisor encuentra los fallos 2, 3 y 4 del inventario, que el
agente principal había pasado por alto.
**Verifica:** `SUB-001`, `SUB-002`, `SUB-003`.
**Activos:** los seis subagentes con contrato.

### Módulo 09 · Git, CI e IDE
**Síntoma:** "Quiero que revise cada propuesta de cambio sin un humano delante."
**Promesa:** el agente trabajando en la tubería, con presupuesto y sin sorpresas.
**Contenido:** modo no interactivo como base de todo lo automático. Revisión
automática de propuestas de cambio. Trabajo en segundo plano y en varios árboles
a la vez. Fijar dependencias. Presupuesto por ejecución.
**Laboratorio:** fijar las dependencias de `gestor-pedidos`, primeros tests y
revisión automática en cada propuesta de cambio.
**PASA si:** la CI falla con el repo tal cual está, y pasa cuando se arreglan los
fallos 9 y 14 del inventario.
**Verifica:** `CID-001`, `CID-002`, `CID-003`.
**Activos:** el flujo de CI, plantillas de propuesta de cambio y de postmortem.

### Módulo 10 · Seguridad y costes
**Síntoma:** "Mi CTO me ha preguntado qué sale de aquí y no he sabido contestar."
**Promesa:** poder responder por escrito, y saber cuánto cuesta todo esto.
**Parte A, seguridad (10.1 a 10.6):** modelo de amenazas. Las cuatro puertas de
entrada de la inyección de prompt. Secretos. Qué sale de tu máquina y adónde.
Rastro auditable. Plan de incidente. Dónde poner al humano.
**Parte B, la factura (10.7 a 10.12):** ya escrita, con telemetría real.
**Laboratorio:** auditoría completa de `gestor-pedidos`, incluida la inyección
escondida en el README, y medición del gasto propio.
**PASA si:** el lector detecta la inyección **y demuestra que su configuración
anterior la obedecía**.
**Activos:** la política interna de un folio, el analizador de gasto.

### Módulo 11 · Troubleshooting
**Síntoma:** "Ayer funcionaba."
**Promesa:** un método para no perder una tarde cada vez.
**Contenido:** el índice por síntoma. El procedimiento de tres pasos: versión,
modo mínimo, y decidir si el problema es tuyo o del CLI. Cómo se lee un fallo que
alguien se tragó. Qué reportar y cómo.
**Laboratorio:** perseguir el error que el `except:` desnudo de `gestor-pedidos`
se está tragando.
**PASA si:** el error aparece en el registro con su traza y el `except` desnudo ya
no existe.
**Verifica:** `TRB-001`, `TRB-002`.

### Módulo 12 · Casos completos
**Síntoma:** "Vale, ¿y todo junto?"
**Promesa:** ver el sistema entero funcionando sobre un problema de verdad.
**Contenido:** tres recorridos completos de principio a fin sobre `gestor-pedidos`:
desmontar la función de ocho responsabilidades, arreglar el IVA por países, y
migrar la configuración duplicada. Cada uno con sus decisiones, sus vueltas atrás
y su coste real.
**PASA si:** los tests cubren los cuatro países, el descuento acumulado queda
decidido y documentado, y el comportamiento no cambia salvo donde se decidió.

### Cierre · Modo escéptico
Ya escrito. Va después del módulo 12, sin numerar como módulo, a propósito: no es
una lección más, es el contrapeso de todas.

---

## 4 · Preliminares y finales

| Pieza | Qué es | Estado |
|---|---|---|
| Portada | Diseño de Julián. En portada va la edición, `v2026.08`, no una versión del CLI. | Pendiente |
| Página de verificación | Versión del CLI, fecha, dirección de la página de estado | Redactable ya |
| Cómo leer este libro | Las dos rutas, en una página | Pendiente |
| Glosario | Término en castellano, término en inglés al lado | Pendiente |
| Índice por síntoma | "Tengo este problema" → módulo | Base hecha en `diagnostico.md` |
| Aviso de no afiliación | Portada interior | Redactado |
| Fuentes y atribuciones | `NOTICE-FUENTES.md` | Esperando inventario de Escribano |

---

## 5 · Reglas de escritura

1. **Castellano fijado en el módulo 01 y respetado hasta el final.** El término
   inglés va entre paréntesis la primera vez y no vuelve a aparecer.
2. **Sin guiones largos.** Regla de la casa.
3. **Nada de "en este capítulo aprenderás".** Se empieza por el síntoma.
4. **Si una afirmación no está en el registro del verificador, no se publica.**
5. **Los euros no se inventan.** Los tokens se miden.
6. **El repo del laboratorio es siempre el mismo.** Doce demos no son un sistema.
7. **Todo módulo termina en un runbook de una página.**
8. **Cada módulo declara en su cabecera la versión del CLI contra la que se
   escribió, y la fecha.** Decidido el 19-ago-2026. Un libro sobre una
   herramienta que publica versión casi a diario no puede prometer una sola: o
   miente en la portada, o se reescribe entero cada semana. La portada lleva la
   edición (`v2026.08`); la versión la lleva cada módulo, donde se midió. Las
   cifras de tokens pertenecen a esa ejecución y a esa máquina, y se dicen así.

## 6 · Orden de escritura recomendado

Por dependencia, no por número: **01 → 03 → 04 → 05 → 07 → 08 → 06 → 02 → 09 →
10A → 11 → 12**. El 01 fija la tesis y el vocabulario; el 03 y el 04 son la
columna vertebral; el 02 se escribe tarde a propósito, porque es el que más
envejece y conviene redactarlo lo más cerca posible de la publicación.
