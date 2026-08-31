# Seguridad de este repositorio

Lo que el `settings.json` no puede decir: contra qué nos defendemos, con qué, y
qué se queda fuera. Escrito en el módulo 10 del manual, contra la 2.1.251, el 31
de agosto de 2026.

## Modelo de amenazas, en cuatro filas

| Puerta | Ejemplo en este repositorio | Qué la cierra |
|---|---|---|
| El propio repositorio | El comentario HTML del `README.md` que le pide al asistente no reportar hallazgos | Nada la cierra. Ver abajo |
| Las dependencias | Tres líneas sin versión fijada hasta el módulo 09 | Cierre de dependencias regenerado, y `pip check` en la CI |
| La respuesta de una herramienta | Un nombre de cliente que en realidad es una orden | Nada la cierra. Se detectó, que no es lo mismo |
| Los tickets y las incidencias | Cualquiera puede abrir una | Revisión humana antes de fusionar |

## Los controles que hay

Son controles porque no preguntan al modelo.

| Control | Dónde | Qué impide |
|---|---|---|
| `deny Read(./secretos/**)` y `Edit` | `.claude/settings.json` | Leer la carpeta de credenciales con las herramientas de archivo |
| `deny Read(./datos/*.db)` | `.claude/settings.json` | Leer nombres y pedidos de clientes reales |
| `deny Bash(curl *)` y `wget *` | `.claude/settings.json` | Bajarse cosas de internet y sacar datos por ahí |
| `ask Bash(git push *)` | `.claude/settings.json` | Que algo salga del repositorio sin que una persona lo vea |
| `ask Bash(python app.py)` | `.claude/settings.json` | Levantar un servidor con `debug=True` en todas las interfaces |
| `hooks/veto-secretos.sh` | `PreToolUse` | Lo mismo que el `deny`, y **también por subproceso**, que el `deny` no cubre |
| `hooks/veto-credenciales.sh` | `PreToolUse` | Escribir una credencial nueva dentro del repositorio |

Comprobado el 31-ago-2026, dos de dos: pedir el archivo de `secretos/` se deniega
**y el agente lo dice**, en vez de fallar en silencio.

## Lo que NO cubre

**La inyección del `README.md`.** Diez ejecuciones el 31-ago-2026 con la 2.1.251:
**ninguna la nombró**. No la obedeció (las auditorías reportaron justo lo que la
inyección pedía callar, dos de dos), pero tampoco te avisa de que está ahí. La
misma prueba contra la **2.1.228**, diecinueve días antes, la detectaba tres de
tres. **No construyas nada encima de ese comportamiento.**

**La clave que vive dentro de `app.py`.** Una regla de permisos protege rutas, no
valores. `API_KEY_PASARELA` está en el mismo archivo que la aplicación, así que
no se puede denegar sin dejar ciego al agente. Sale de ahí en el módulo 12.

**Las copias de esa clave fuera del repositorio.** Las transcripciones de sesión
se guardan en claro en `~/.claude/projects/`, 30 días por defecto
(`cleanupPeriodDays`), una carpeta por cada ruta desde la que se haya trabajado.
Al cerrar el módulo 10 había **35 apariciones de la clave en cuatro archivos**.
Del archivo protegido por el `deny`, cero.

**La revisión automática de la CI.** Mira el diff, y esa clave no está en ningún
diff desde 2019.

**La telemetría.** Seis ejecuciones con `-p` y el exportador de consola, por
entorno y por `--settings`, y cero eventos. Hasta ver uno, esto no cuenta como
rastro auditable.

## Si se filtra una credencial

1. Revocar y rotar. Primero eso, antes de investigar nada.
2. Contar las copias del rastro local:
   `grep -rl "<la credencial>" ~/.claude/projects/`. Hay una carpeta por ruta de
   trabajo, incluidas las copias del repositorio en otros directorios.
3. Borrarlas, en todas las máquinas.
4. Comprobar que nadie envió esa sesión con `/feedback`, `/bug` o `/share`: esas
   transcripciones **se retienen cinco años**.
5. Registrar qué se pidió, qué hizo el agente, con qué versión del CLI y con qué
   permisos.

## Qué sale de esta máquina

La conversación y el contenido de los archivos que el agente abre para trabajar.
Además, siempre y con cualquier proveedor de modelo: antes de descargar una URL,
`WebFetch` envía **el nombre de host** a `api.anthropic.com`. Solo el host, no la
ruta ni el contenido. No lo apaga `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`; su
interruptor es `skipWebFetchPreflight`.

El servidor MCP de `mcp/servidor-pedidos.py` es local y no sale nada por él. Un
servidor MCP de terceros sería un subencargado del tratamiento, y habría que
inventariarlo aquí.

---

<sub>Material de laboratorio del manual "Claude Code en producción". Los fallos de
este repositorio son deliberados y están inventariados. **No se despliega.**</sub>
