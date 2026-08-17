# Estado de verificación · Claude Code en producción

**Versión del libro:** v2026.08  
**Verificado contra:** `2.1.233 (Claude Code)`  
**Sistema:** Linux 6.17.0-41-generic  
**Fecha:** 2026-08-17 13:24:05 UTC

🟢 30 pasan · 🔴 0 fallan · 🟡 5 a revisar · ⚪ 3 omitidas

| | ID | Capítulo | Afirmación del libro | Comprobación |
|---|---|---|---|---|
| 🟢 | CLI-001 | 02 · Instalación y autenticación | El binario responde a --version y devuelve una versión semántica. | `claude --version` |
| 🟢 | CLI-002 | 02 · Instalación y autenticación | claude doctor comprueba la salud de la instalación sin abrir sesión. | `claude doctor` |
| 🟢 | CLI-003 | 02 · Instalación y autenticación | claude setup-token crea un token de larga duración para suscriptores. | `claude --help` |
| 🟢 | CLI-004 | 02 · Instalación, autenticación y versiones | claude doctor informa del método de instalación, del canal de actualización y del resultado del último intento. | `claude doctor` |
| 🟢 | CLI-005 | 02 · Instalación, autenticación y versiones | claude install acepta como destino un canal o un número de versión concreto, que es la vía para reproducir un fallo ajeno. | `claude install --help` |
| 🟢 | CLI-006 | 02 · Instalación, autenticación y versiones | claude auth gestiona el inicio de sesión y expone status, que dice qué credencial está activa sin abrir sesión. | `claude auth --help` |
| 🟢 | CLI-007 | 02 · Instalación, autenticación y versiones | La instalación nativa deja en el PATH un enlace simbólico a una versión concreta bajo ~/.local/share/claude/versions/, y por eso conviven varias versiones en disco. | `bash -c L="$HOME/.local/bin/claude"; if [ -L "$L" ]; then readlink "$L" | grep -q "/.local/share/claude/versions/" && echo LANZADOR-ES-ENLACE-A-VERSIONS || echo ENLACE-A-OTRO-SITIO; else echo NO-APLICA-SIN-INSTALACION-NATIVA; fi` |
| 🟢 | CLI-008 | 02 · Instalación, autenticación y versiones | claude doctor termina con código 0 aunque reporte ajustes inválidos: el código de salida no sirve como comprobación de configuración. | `bash -c d=$(mktemp -d); mkdir -p "$d/.claude"; echo "{" > "$d/.claude/settings.json"; cd "$d"; claude doctor > out.txt 2>&1; c=$?; grep -q "Invalid settings" out.txt && [ "$c" = "0" ] && echo AJUSTES-INVALIDOS-Y-SALIDA-CERO; rm -f "$d/out.txt" "$d/.claude/settings.json"; rmdir "$d/.claude" "$d"` |
| 🟢 | CLI-009 | 02 · Instalación, autenticación y versiones | La documentación oficial condiciona comportamiento a versiones concretas del CLI: authentication.md cita seis o más. | `bash -c D=$(curl -fsS --max-time 25 https://code.claude.com/docs/en/authentication.md 2>/dev/null) || { echo SIN-RED; exit 0; }; printf "%s" "$D" | grep -oE "v2[.]1[.][0-9]+" | sort -u | wc -l` |
| 🟡 | CLI-010 | 02 · Instalación, autenticación y versiones | El binario acepta un tercer canal de publicación, rc, que la documentación oficial no menciona. | Comprobado el 17-ago-2026 con la 2.1.233. Poniendo un autoUpdatesChannel inválido en un settings.json, claude doctor contesta: Expected one of latest, stable, rc. Y rc no aparece ni en setup.md ni en settings.md descargadas ese mismo día. Se deja manual a propósito: automatizarlo exige comillas dobles dentro del comando, y el lector de YAML sin dependencias del verificador las deja escapadas, así que pasaría en local con PyYAML y fallaría en CI sin él. Es la misma clase de fallo que documenta REPO-001. Se revisa cada trimestre; el día que se documente, deja de ser una caja de aviso y pasa a ser una sección. |
| 🟡 | AUT-001 | 02 · Instalación, autenticación y versiones | El orden de precedencia de credenciales tiene siete niveles, y una sesión de pasarela de aplicaciones de Claude queda por encima de los siete. | Eran cuatro en el material propio del 12-ago-2026 y son siete en authentication.md del 17-ago-2026. Es una lista que crece: se recuenta contra la documentación oficial en cada revisión trimestral, no se copia de una edición anterior. |
| 🟢 | ENT-001 | 02 · Instalación, autenticación y versiones | El laboratorio del módulo 02 deja los mandos del proyecto versionados en gestor-pedidos. | `test -f .claude/settings.json` |
| 🟢 | ENT-002 | 02 · Instalación, autenticación y versiones | El laboratorio del módulo 02 deja la versión del CLI anotada en el repositorio, no en la cabeza de nadie. | `grep -qE [0-9]+[.][0-9]+[.][0-9]+ ENTORNO.md` |
| 🟢 | CTX-001 | 03 · Memoria y contexto | --add-dir da acceso a directorios fuera del proyecto actual. | `claude --help` |
| 🟢 | CTX-002 | 03 · Memoria y contexto | --autocompact controla el tamaño de la ventana antes de compactar. | `claude --help` |
| 🟢 | CTX-003 | 03 · Memoria y contexto | --bare arranca sin CLAUDE.md, sin hooks y sin plugins, para depurar contexto. | `claude --help` |
| 🟢 | PRM-001 | 04 · Permisos y sandbox | --allowedTools acepta una lista de herramientas permitidas. | `claude --help` |
| 🟢 | PRM-002 | 04 · Permisos y sandbox | Existe una bandera para saltarse todos los permisos, y la documentación la marca como peligrosa. | `claude --help` |
| 🟢 | PRM-003 | 04 · Permisos y sandbox | El archivo de ajustes de usuario vive en ~/.claude/settings.json. | `test -e /tmp/home-sin-claude-2i7eaczc/.claude` |
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
| 🟢 | REPO-001 | 00 · Gobierno del proyecto | El repositorio del manual está público, como se decidió el 13 de agosto de 2026. | `curl -sS --max-time 25 -o /dev/null -w %{http_code} https://github.com/julian-najas/manual-claude-code` |
| 🟢 | REPO-002 | 00 · Gobierno del proyecto | El companion público sigue publicado: si dejara de serlo, GitHub Pages dejaría de servir las 156 páginas. | `curl -sS --max-time 25 -o /dev/null -w %{http_code} https://github.com/julian-najas/claude-code-companion` |
| 🟢 | REPO-003 | 00 · Gobierno del proyecto | El sitio del companion responde y sirve el índice por síntoma. | `curl -sS --max-time 25 https://julian-najas.github.io/claude-code-companion/` |
| ⚪ | SEG-001 | 10 · Seguridad y costes | rm -rf sobre el directorio del proyecto lo destruye sin confirmación del sistema operativo. | prueba destructiva, documentada pero nunca ejecutada |

---

⚪ **Omitidas** son pruebas destructivas o que gastan dinero. Las destructivas están documentadas en el libro pero no se ejecutan nunca. Las de coste se ejecutan a mano con `--con-coste` en cada revisión trimestral.

🟡 **A revisar** son afirmaciones que solo puede comprobar una persona, por ejemplo las que necesitan una máquina limpia.

Este archivo lo genera `verificar.py`. No se edita a mano.
