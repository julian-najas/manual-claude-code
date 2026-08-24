# El servidor MCP de gestor-pedidos

Un servidor, tres herramientas, solo lectura. Está declarado en `.mcp.json` y su
código vive entero en `mcp/servidor-pedidos.py`: doscientas líneas de Python sin
una sola dependencia, para que puedas leerlo antes de dejarlo correr.

Medido con Claude Code **2.1.241** el 24 de agosto de 2026.

## Qué expone

| Herramienta | Qué hace |
|---|---|
| `listar_tablas` | Los nombres de las tablas |
| `describir_tabla` | Columnas y tipos de una tabla |
| `consultar` | Ejecuta un `SELECT` y devuelve las filas, con tope de 1.000 |

Los datos viven en `datos/pedidos.db`, que está en `.gitignore`. No viene en el
clon: se construye con `sqlite3 datos/pedidos.db < datos/esquema.sql`.

## Qué NO puede hacer, y qué lo impide

**Tres candados, y ninguno se fía del anterior.** Están así a propósito: el día
que alguien afloje uno, quedan dos.

| # | Candado | Quién lo aplica |
|---|---|---|
| 1 | Conexión `file:...?mode=ro` por URI de SQLite | SQLite, no este código. En modo `ro` tampoco crea la base si falta |
| 2 | Una sola sentencia, empezando por `SELECT` o `WITH` | El servidor. Un `;` en medio es el camino para colar un `UPDATE` detrás de un `SELECT` |
| 3 | `set_authorizer` denegando toda operación que no sea leer | El motor de SQLite |

## Cómo se prueban

En seco, sin Claude Code de por medio, igual que los hooks:

```bash
export CLAUDE_PROJECT_DIR="$PWD"
printf '%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
 '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"consultar","arguments":{"sql":"DELETE FROM pedidos"}}}' \
 '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"consultar","arguments":{"sql":"SELECT 1; UPDATE pedidos SET total=0"}}}' \
 | python3 mcp/servidor-pedidos.py
```

Las dos primeras respuestas son el `serverInfo` y las tres herramientas. Las dos
últimas tienen que traer `isError` con su motivo. El verificador del manual corre
esto en `MCP-003` a `MCP-007`.

**Una advertencia que no es teórica.** Al pedirle al agente que borrara los
pedidos, se negó citando las instrucciones del servidor y **sin llegar a llamar a
la herramienta**, las dos veces que se probó. Eso no es un candado, es criterio
propio del modelo, que el módulo 05 midió fallando 5 de 7 veces. Lo que protege
esta base son los tres candados, y por eso se prueban en seco.

## Lo que cuesta tenerlo conectado

Medido con la petición trivial del módulo 04, dos repeticiones por celda, todas
idénticas al token:

| | Con tool search (el defecto) | Sin tool search |
|---|---:|---:|
| Sin servidor | 45.441 | 62.662 |
| Con este servidor, 3 herramientas | 45.659 | 63.220 |
| **Coste del servidor** | **+218** | **+558** |

218 tokens por turno. Menos que dos líneas del `CLAUDE.md`.

## Lo que este servidor no es

No es una frontera de seguridad frente a quien pueda editar `mcp/` o `.mcp.json`.
Es una frontera frente al accidente y frente a lo que el agente decida por su
cuenta.

Y el aviso en voz alta, que vale para cualquier repositorio y no solo para este:
**un `.mcp.json` confirmado en git arranca un proceso en la máquina de quien
clone.** En `claude -p`, con este archivo sin aprobar, el servidor conectó y sus
herramientas estaban disponibles. Para ignorar los servidores del repositorio en
una ejecución concreta: `--strict-mcp-config`.
