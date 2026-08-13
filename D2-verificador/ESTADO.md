# Estado de verificación · Claude Code en producción

**Versión del libro:** v2026.08  
**Verificado contra:** `2.1.231 (Claude Code)`  
**Sistema:** Linux 6.17.0-1020-azure  
**Fecha:** 2026-08-13 09:40:49 UTC

🟢 19 pasan · 🔴 0 fallan · 🟡 3 a revisar · ⚪ 3 omitidas

| | ID | Capítulo | Afirmación del libro | Comprobación |
|---|---|---|---|---|
| 🟢 | CLI-001 | 02 · Instalación y autenticación | El binario responde a --version y devuelve una versión semántica. | `claude --version` |
| 🟢 | CLI-002 | 02 · Instalación y autenticación | claude doctor comprueba la salud de la instalación sin abrir sesión. | `claude doctor` |
| 🟢 | CLI-003 | 02 · Instalación y autenticación | claude setup-token crea un token de larga duración para suscriptores. | `claude --help` |
| 🟢 | CTX-001 | 03 · Memoria y contexto | --add-dir da acceso a directorios fuera del proyecto actual. | `claude --help` |
| 🟢 | CTX-002 | 03 · Memoria y contexto | --autocompact controla el tamaño de la ventana antes de compactar. | `claude --help` |
| 🟢 | CTX-003 | 03 · Memoria y contexto | --bare arranca sin CLAUDE.md, sin hooks y sin plugins, para depurar contexto. | `claude --help` |
| 🟢 | PRM-001 | 04 · Permisos y sandbox | --allowedTools acepta una lista de herramientas permitidas. | `claude --help` |
| 🟢 | PRM-002 | 04 · Permisos y sandbox | Existe una bandera para saltarse todos los permisos, y la documentación la marca como peligrosa. | `claude --help` |
| 🟢 | PRM-003 | 04 · Permisos y sandbox | El archivo de ajustes de usuario vive en ~/.claude/settings.json. | `test -e /home/runner/.claude` |
| 🟡 | HOK-001 | 05 · Hooks | Los hooks se configuran en settings.json, no en un archivo aparte. | Comprobar contra la documentación oficial en cada revisión trimestral. |
| 🟢 | MCP-001 | 06 · MCP | claude mcp gestiona los servidores MCP desde la línea de comandos. | `claude mcp --help` |
| 🟡 | MCP-002 | 06 · MCP | Por defecto solo se cargan los nombres de las herramientas MCP; los esquemas van diferidos y se traen bajo demanda con tool search. | Corrige material propio erróneo (12-ago-2026). Depende de ENABLE_TOOL_SEARCH: auto carga esquemas si caben en el 10 por ciento de la ventana, false los carga todos. Comprobar en /docs/en/mcp#scale-with-mcp-tool-search cada revisión trimestral. |
| ⚪ | SEG-002 | 10 · Seguridad y costes | Una inyección escrita en claro en un archivo del repositorio se detecta y se reporta, pero eso no es un control de seguridad. | gasta tokens, se ejecuta solo con --con-coste |
| 🟢 | SKL-001 | 07 · Skills y plugins | claude plugin gestiona los plugins instalados. | `claude plugin --help` |
| 🟢 | SKL-002 | 07 · Skills y plugins | Las skills se resuelven por /nombre-de-skill incluso en modo mínimo. | `claude --help` |
| 🟢 | SUB-001 | 08 · Subagentes | --agents permite definir agentes personalizados en JSON desde la propia llamada. | `claude --help` |
| 🟢 | SUB-002 | 08 · Subagentes | claude agents gestiona los agentes que corren en segundo plano. | `claude agents --help` |
| 🟢 | SUB-003 | 08 · Subagentes | --background arranca la sesión como agente en segundo plano y devuelve el control. | `claude --help` |
| 🟢 | CID-001 | 09 · Git, CI e IDE | -p ejecuta Claude Code sin sesión interactiva, que es la base de cualquier uso en CI. | `claude --help` |
| 🟢 | CID-002 | 09 · Git, CI e IDE | claude ultrareview lanza una revisión multiagente de la rama actual. | `claude --help` |
| 🟢 | CID-003 | 09 · Git, CI e IDE | claude import trae la configuración de otro agente de codificación. | `claude --help` |
| ⚪ | CST-001 | 10 · Seguridad y costes | Una llamada mínima con un CLAUDE.md grande ya consume decenas de miles de tokens de entrada. | gasta tokens, se ejecuta solo con --con-coste |
| 🟢 | TRB-001 | 11 · Troubleshooting | claude update comprueba e instala actualizaciones. | `claude --help` |
| 🟡 | TRB-002 | 11 · Troubleshooting | Borrar la caché de proyecto no borra la configuración de usuario. | Requiere una máquina limpia. Se comprueba en la revisión trimestral. |
| ⚪ | SEG-001 | 10 · Seguridad y costes | rm -rf sobre el directorio del proyecto lo destruye sin confirmación del sistema operativo. | prueba destructiva, documentada pero nunca ejecutada |

---

⚪ **Omitidas** son pruebas destructivas o que gastan dinero. Las destructivas están documentadas en el libro pero no se ejecutan nunca. Las de coste se ejecutan a mano con `--con-coste` en cada revisión trimestral.

🟡 **A revisar** son afirmaciones que solo puede comprobar una persona, por ejemplo las que necesitan una máquina limpia.

Este archivo lo genera `verificar.py`. No se edita a mano.
