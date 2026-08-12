---
name: manual-claude-code
description: >
  El manual "Claude Code en producción" consultable desde la terminal. Úsala cuando
  haya que decidir dónde va una pieza de configuración (CLAUDE.md, skill, hook,
  subagente, comando, MCP o plugin), cuando alguien pregunte por permisos, sandbox,
  contexto que se agota, hooks, servidores MCP, subagentes, uso en CI o modo no
  interactivo, cuando haya que diagnosticar por qué una skill no se activa o por qué
  una sesión se queda sin contexto, y cuando se quiera reducir el gasto en tokens.
  También para consultar la política interna de uso de agentes y el estado de
  verificación del manual.
---

# Manual "Claude Code en producción"

Este es el libro, dentro de la herramienta que explica. Responde con la
recomendación concreta del manual, citando el capítulo, no con generalidades.

## Cómo usar esta skill

1. **Identifica qué tipo de pregunta es** con la tabla de abajo.
2. **Lee solo el archivo de referencia que toca.** No cargues todos: el manual
   entero no cabe en contexto y no hace falta.
3. **Responde con la decisión y el capítulo.** Si el manual no cubre el caso,
   dilo claramente en vez de improvisar. La credibilidad del libro depende de
   eso más que de acertar siempre.

| Si la pregunta es sobre... | Lee |
|---|---|
| Dónde poner algo: CLAUDE.md, skill, hook, subagente, comando, MCP, plugin | `referencias/arbol-decision.md` |
| Permisos, sandbox, secretos, inyección de prompt, qué sale de la máquina | `referencias/permisos-y-seguridad.md` |
| Gasto, tokens, contexto que se agota, sesiones caras | `referencias/costes.md` |
| Algo no funciona y no se sabe por qué | `referencias/diagnostico.md` |
| Qué puede hacer el equipo y qué no, política interna | `../../D5-politica/politica-uso-agentes.md` |

## Reglas de la casa

- **Cita el capítulo.** Toda respuesta lleva de dónde sale. Sin cita, es opinión.
- **Ninguna afirmación sin verificar.** Las afirmaciones del manual se comprueban
  a diario contra el CLI instalado. Si dudas de una, mira `estado.json` del
  verificador antes de repetirla.
- **La versión importa.** Este manual está verificado contra una versión concreta
  del CLI. Si la instalada es más nueva, avisa de la diferencia antes de
  responder, no después.
- **Si el manual se contradice con la máquina, gana la máquina.** Y es un fallo
  que hay que reportar, no disimular.

## Las cinco respuestas que se piden todos los días

**"¿Esto va en CLAUDE.md o en una skill?"**
Si hace falta en todas las tareas del repositorio, CLAUDE.md. Si solo a veces,
skill. Prueba rápida: si en la mitad de las tareas ese texto sobra, es una skill.
CLAUDE.md se paga en cada turno de cada sesión. Cap. 3.

**"Le he dicho que siempre haga X y a veces no lo hace."**
Porque una instrucción se interpreta. Si no es negociable, es un hook: código
determinista ante un evento, no una frase en un archivo. Cap. 5.

**"Se me acaba el contexto enseguida."**
Mira las dos únicas piezas que cobran en cada turno: el tamaño de CLAUDE.md y
cuántos servidores MCP hay conectados, con todas sus definiciones de
herramientas dentro. Cap. 3 y 6.

**"Mi skill no se activa sola."**
El problema casi nunca está en el cuerpo, está en la descripción, que es el
disparador. Reescríbela con las palabras que usarías tú al pedir esa tarea.
Cap. 7.

**"¿Cómo lo meto en CI?"**
Modo no interactivo con permisos explícitos y presupuesto acotado. Nunca con las
comprobaciones de permisos desactivadas en una máquina con acceso a producción.
Cap. 9 y 10.

## Verificación

Este manual se acompaña de un verificador que ejecuta las afirmaciones del libro
contra el CLI instalado:

```
python3 D2-verificador/verificar.py
```

Estado de la última pasada: `D2-verificador/ESTADO.md`.
