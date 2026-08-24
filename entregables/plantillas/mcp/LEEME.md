# Servidor MCP de solo lectura

`servidor-solo-lectura.py` es el servidor que se construye en el módulo 06 del
manual, generalizado: la ruta de la base de datos se pasa por entorno en vez de
estar fijada. Python, SQLite, **cero dependencias**.

Verificado con Claude Code **2.1.241** el 24 de agosto de 2026.

## Montarlo en cuatro pasos

**1.** Copia el archivo a `mcp/` en tu proyecto y hazlo ejecutable.

**2.** Declara el servidor en `.mcp.json`, en la raíz del repositorio:

```json
{
  "mcpServers": {
    "datos": {
      "type": "stdio",
      "command": "python3",
      "args": ["${CLAUDE_PROJECT_DIR:-.}/mcp/servidor-solo-lectura.py"],
      "env": { "BD_RUTA": "datos/app.db" }
    }
  }
}
```

El `:-.` no sobra. Dentro de un `.mcp.json` la variable se expande antes de que
exista, así que sin valor por defecto la ruta se queda a medias.

**3.** Pruébalo en seco, antes de conectarlo a nada:

```bash
export CLAUDE_PROJECT_DIR="$PWD" BD_RUTA="datos/app.db"
printf '%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
 '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"consultar","arguments":{"sql":"DELETE FROM lo_que_sea"}}}' \
 | python3 mcp/servidor-solo-lectura.py
```

Dos respuestas buenas y una con `isError`. Si sale cualquier cosa que no sea
JSON por delante, tienes un `print` suelto y el transporte no va a funcionar.

**4.** `claude mcp list` para ver que aparece, y una pregunta sobre tus datos.
Comprueba la lista de llamadas, no la respuesta:

```bash
claude -p "¿Cuántas filas hay en la tabla principal?" \
  --output-format stream-json --verbose \
  | jq -r 'select(.type=="assistant") | .message.content[]?
           | select(.type=="tool_use") | .name'
```

Si ahí sale `Read` o `Bash`, no está usando el servidor.

## Los tres candados

Ninguno se fía del anterior, y esa es la idea.

| # | Candado | Quién lo aplica |
|---|---|---|
| 1 | Conexión `file:...?mode=ro` por URI | SQLite. En `ro` tampoco crea el fichero si falta |
| 2 | Una sola sentencia, empezando por `SELECT` o `WITH` | El servidor |
| 3 | `set_authorizer` denegando todo lo que no sea leer | El motor de SQLite |

**La negativa del agente no cuenta como candado.** Al pedirle que borrara datos,
en la medición del módulo 06 se negó citando las instrucciones del servidor y sin
llegar a llamar a la herramienta. Eso es criterio propio del modelo, y el módulo
05 lo midió fallando cinco veces de siete. Prueba los candados en seco.

## Lo que cuesta

Con tool search activada, que es el defecto, este servidor de tres herramientas
cuesta **218 tokens de entrada por turno**, y cada herramienta que le añadas,
unos 13. Sin tool search, unos 200 por herramienta. Medido en el módulo 06.

## Antes de adaptarlo

- **Credenciales de solo lectura también en el motor**, si tu base no es SQLite.
  Estos candados son de proceso; el usuario de base de datos es de sistema, y
  los dos deberían decir lo mismo.
- **Tope de filas.** El valor por defecto es 100 y el máximo 1.000, porque una
  salida de más de 25.000 tokens se trunca y a los 10.000 ya avisa.
- **Nada de secretos en el `.mcp.json`**, que va a git por diseño. Usa `${VAR}`
  y deja los valores en el entorno.
