---
name: guia-claude-code
description: >
  La Guía Definitiva de Claude Code en español, consultable desde la terminal.
  Úsala para cualquier duda sobre el propio Claude Code: dónde va una pieza de
  configuración (CLAUDE.md, skill, hook, subagente, comando, MCP o plugin),
  permisos y modos, sandbox, memoria y contexto que se agota, hooks y sus
  eventos, servidores MCP y tool search, skills que no se activan, subagentes y
  paralelismo, worktrees, plugins y marketplaces, superficies e IDE, CI y
  revisión de código, despliegue empresarial y gateways, modelos, caché y coste,
  datos y cumplimiento, Agent SDK, diagnóstico de errores, y qué features se han
  retirado. También cuando algo falle y no se sepa por qué.
---

# Guía Definitiva de Claude Code

**v2026.08 · verificada contra Claude Code 2.1.228 el 12 de agosto de 2026.**

21 módulos, 15 tablas de referencia, 120 páginas de documentación oficial
contrastadas y mediciones propias. Sin afiliación con Anthropic.

## Cómo usar esta skill

1. **Si el usuario describe un síntoma**, empieza por `INDICE-SINTOMAS.md`: son
   156 síntomas reales con su causa y su módulo. Busca por lo que le pasa, no por
   lo que crees que es.
2. **Si pregunta por un tema**, ve directo al módulo con la tabla de abajo.
3. **Lee solo el módulo que toca.** Son 44.000 palabras en total: cargarlos todos
   no cabe y no hace falta.
4. **Responde con la respuesta y el módulo.** Sin cita, es opinión.

## Ruta por tema

| Si la pregunta es sobre... | Lee |
|---|---|
| Cómo funciona por dentro, el bucle, contexto, checkpoints | `modulos/M1-*.md` |
| Instalar, autenticar, versiones, canales | `modulos/M2-*.md` |
| `.claude/`, settings, **precedencia**, "no me hace caso" | `modulos/M3-*.md` |
| `CLAUDE.md`, rules, auto memory, **qué sobrevive a compactar** | `modulos/M4-*.md` |
| Permisos, los **seis** modos, sandbox, inyección de prompt | `modulos/M5-*.md` |
| Flujo diario, plan, verificación, **límites del rebobinado** | `modulos/M6-*.md` |
| Skills, comandos, output styles, barra de estado | `modulos/M7-*.md` |
| MCP, transportes, ámbitos, **tool search**, límites de salida | `modulos/M8-*.md` |
| Subagentes, teams, workflows, worktrees, mensajería | `modulos/M9-*.md` |
| Hooks y sus **31 eventos**, programación, modo no interactivo | `modulos/M10-*.md` |
| Plugins, marketplaces, dependencias | `modulos/M11-*.md` |
| Terminal, IDE, escritorio, web, móvil, Slack, Chrome | `modulos/M12-*.md` |
| CI, GitHub Actions, revisión de código, ultrareview | `modulos/M13-*.md` |
| Despliegue empresarial, proveedores, **gateways**, self-hosted | `modulos/M14-*.md` |
| Modelos, esfuerzo, **caché**, coste, observabilidad | `modulos/M15-*.md` |
| Datos, retención, ZDR, RGPD | `modulos/M16-*.md` |
| Agent SDK | `modulos/M17-*.md` |
| **Diagnóstico**, los 83 errores catalogados | `modulos/M18-*.md` |
| Referencia rápida: comandos, banderas, variables, herramientas | `modulos/M19-*.md` |
| Playbooks completos: monorepo, legacy, equipo, nocturno, plugin | `modulos/M20-*.md` |
| **Qué se ha retirado o renombrado**, trampas de tutoriales viejos | `modulos/M21-*.md` |

## Reglas de la casa

- **Cita el módulo.** Toda respuesta lleva de dónde sale.
- **La versión manda.** Esta guía está verificada contra 2.1.228. Si la instalada
  es distinta, **dilo antes de responder**, no después. Compruébalo con
  `claude --version`.
- **Si la guía y la máquina se contradicen, gana la máquina**, y eso es un fallo
  que se reporta.
- **No inventes.** Si la guía no lo cubre, dilo y señala la página oficial. La
  lista completa de fuentes está en `FUENTES.md` del repositorio.

## Las siete respuestas que se piden todos los días

**"¿Esto va en CLAUDE.md o en una skill?"**
Si hace falta en todas las tareas del repo, `CLAUDE.md`. Si solo a veces, skill.
Prueba: si en la mitad de las tareas ese texto sobra, es una skill. **M4.**

**"Le he dicho que siempre haga X y a veces no lo hace."**
Porque `CLAUDE.md` es contexto, no configuración impuesta. Lo no negociable es un
hook `PreToolUse`: código, no interpretación. **M4 y M10.**

**"Se me acaba el contexto."**
Empieza por el tamaño de tu `CLAUDE.md`, que es lo único que se paga entero cada
turno. MCP va diferido por defecto, así que desconectar servidores ahorra menos de
lo que crees. Mide con `/context` y `/mcp` antes de amputar. **M4, M8 y M15.**

**"Mi skill no se activa sola."**
Casi siempre el frontmatter está mal formado: se carga el cuerpo con los metadatos
vacíos, así que `/nombre` funciona a mano pero no hay `description` contra la que
casar. Arranca con `--debug`. **M7.**

**"Se le olvidó lo que le dije."**
Compactó. El `CLAUDE.md` de la raíz se reinyecta; los anidados y las reglas con
`paths` no. Lo que debe persistir va al `CLAUDE.md`, no al historial. **M4.**

**"Rebobiné y sigue ahí."**
Los checkpoints **no** cubren lo que hizo un comando de Bash, ni lo que hizo un
subagente en segundo plano, ni nada remoto. En desatendido tu red es git. **M6.**

**"¿Qué me cuesta esto?"**
Medido en producción: **24 tokens de entrada por cada token de salida**, y cada
confirmación de una palabra costó **7.891 tokens de entrada**. El coste lo decide
el contexto, no la tarifa del modelo. **M15.**

## Lo que más rápido caduca

- **Auto mode pasa a ser el modo de permisos por defecto el 14 de agosto de 2026**
  en Pro, Max y Team. Si el usuario pregunta después de esa fecha, ya ocurrió.
- La versión verificada, 2.1.228, envejece en días.

Consulta `PENDIENTE-VERIFICAR.md` del repositorio antes de afirmar algo sensible
al tiempo.
