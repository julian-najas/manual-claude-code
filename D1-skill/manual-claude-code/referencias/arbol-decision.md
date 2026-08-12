# Árbol de decisión

Fuente canónica de la Lámina 1. Baja en orden y para en el primer sí.

## Las siete preguntas

**01 · ¿Tiene que ocurrir siempre, sin que el modelo pueda saltárselo? → HOOK**
Código determinista ante un evento del ciclo de vida. Formatear tras editar,
vetar borrados masivos, impedir la lectura de un `.env`, dejar rastro.
Prueba: si te vale con "casi siempre", no es un hook. Si no, lo es.

**02 · ¿Necesita datos o acciones de fuera de esta máquina? → MCP**
Base de datos, API, sistema de tickets. MCP es el enchufe hacia fuera y nada
más. Si lo que quieres es que trabaje mejor con lo que ya tiene delante, te has
equivocado de pregunta.

**03 · ¿Es contexto necesario en todas las tareas del repositorio? → CLAUDE.md**
Cómo se compila, cómo se prueba, qué convenciones hay, qué no se toca.
Prueba: si en la mitad de las tareas ese texto sobra, no va aquí.

**04 · ¿Es un procedimiento ocasional que el agente puede reconocer? → SKILL**
Vive apagada y se enciende sola cuando la tarea encaja con su descripción. La
descripción es el disparador, no la documentación.

**05 · ¿Lo lanza siempre una persona con las mismas instrucciones? → COMANDO**
Prompt guardado que invocas a mano. La diferencia con la skill es quién decide:
la skill la decide el agente, el comando lo decides tú.

**06 · ¿Necesita contexto limpio, otro criterio o va a hacer mucho ruido? → SUBAGENTE**
Trabaja en su propia ventana y devuelve solo la conclusión. El precio: no
comparte tu contexto, hay que darle todo lo que necesite.

**07 · ¿Ya funciona y lo quiere tu equipo? → PLUGIN**
Es el envoltorio de las seis anteriores, nunca la respuesta a "cómo hago esto".
Empaquetar antes de que funcione es repartir el problema.

**¿Ningún sí?** No necesitas configurar nada, necesitas escribir mejor la
instrucción. La mitad de las configuraciones existen para compensar una petición
mal formulada.

## El impuesto de contexto

| Pieza | Ocupa | Se paga | La activa |
|---|---|---|---|
| Hook | nada, corre fuera del modelo | nunca | el programa, ante un evento |
| Comando | nada hasta invocarlo | al invocarlo | tú, a mano |
| Skill | solo su descripción | descripción siempre, cuerpo al activarse | el agente, si encaja |
| Subagente | su propia ventana | en su cuenta aparte | el agente principal o tú |
| CLAUDE.md | el archivo entero | **siempre, cada turno** | se carga al abrir |
| MCP | todas sus definiciones de herramientas | **siempre, cada turno** | se conecta al arrancar |
| Plugin | lo que lleve dentro | hereda | depende |

Las dos filas en negrita son las que la gente usa por defecto. Un CLAUDE.md de
mil líneas y cuatro MCP conectados por si acaso son un impuesto en cada turno,
se usen o no.

## Señales de que elegiste mal

| Síntoma | Diagnóstico | Vuelve a |
|---|---|---|
| "A veces lo hace y a veces no" | pusiste como instrucción algo no negociable | 01, hook |
| El CLAUDE.md no para de crecer | metes procedimientos ocasionales donde se paga siempre | 04, skill |
| La skill nunca se activa sola | la descripción no dispara, reescríbela con tus palabras | 04, skill |
| La sesión se queda sin contexto | mira tamaño de CLAUDE.md y número de MCP conectados | tabla del impuesto |
| El subagente devuelve algo inservible | no comparte contexto: lo que no le pasaste, no lo tiene | 06, subagente |
| A tu compañero no le funciona | lo tienes suelto en vez de empaquetado | 07, plugin |
