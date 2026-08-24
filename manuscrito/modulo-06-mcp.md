# Módulo 06 · MCP

> **Laboratorio de este módulo:** ~35 minutos · doce ejecuciones, unos
> **900.000 tokens de entrada** y 1.000 de salida · **0,65 dólares** según la
> telemetría del propio CLI, que a cualquier cambio euro-dólar de agosto de 2026
> se queda **por debajo de 0,75 €**. Con suscripción va incluido.
> **Verificado contra:** Claude Code 2.1.241 · 24 de agosto de 2026.

> **Nota de versión.** Cada módulo declara la versión con la que se midió, y
> esta es la 2.1.241, la misma que el módulo 05. Las cifras son de esa versión y
> de esa máquina.

---

## 6.1 · Síntoma

Tienes los datos en una base de datos y el agente no los ve. Le pides cuántos
pedidos hay y se pone a abrir archivos del repositorio buscando algo que ahí no
está, o peor: te contesta con un número que ha sacado de un README de 2019.

Y cuando alguien propone conectarle la base de datos, la sala se divide en dos.
Los que dicen que ni de broma, porque un agente con acceso a producción es un
`DROP TABLE` esperando su turno. Y los que dicen que sin datos esto no sirve de
nada. Los dos tienen razón, y por eso este módulo va de la única respuesta que
satisface a ambos: **acceso sí, escritura no, y demostrado**.

---

## 6.2 · Modelo mental

### 6.2.1 · Qué es MCP, y sobre todo qué no es

MCP (protocolo de contexto de modelo) es **el enchufe hacia fuera**. Un servidor
MCP expone herramientas, recursos y prompts, y Claude Code los usa como usa los
suyos. Cuatro transportes:

| Transporte | Para qué |
|---|---|
| **stdio** | Un proceso local en tu máquina. Es el del laboratorio |
| **HTTP** | Servidor remoto. Lo más común hoy |
| **SSE** | Remoto con eventos del servidor |
| **WebSocket** | Remoto bidireccional |

Y la frase que ahorra la mitad de los MCP que se montan: **si lo que quieres es
que trabaje mejor con lo que ya tiene delante, la respuesta no era un MCP.** Un
servidor para leer archivos del repositorio no aporta nada, porque ya sabe
leerlos. MCP es para lo que no está en el disco: la base de datos, el sistema de
incidencias, la forja.

### 6.2.2 · El impuesto que ya no es el que era

Durante dos años, el consejo sobre MCP fue "conecta poco, que cada servidor mete
sus definiciones de herramientas en cada turno". **Eso hoy es falso**, y este
libro lo ha dicho mal antes, así que va medido.

**Tool search (búsqueda de herramientas) está activada por defecto.** Al arrancar
solo entran en contexto **los nombres de las herramientas y las instrucciones
del servidor**; los esquemas completos se difieren y se traen cuando la tarea los
necesita. Lo medimos con la misma petición trivial y una sola variable, el número
de herramientas MCP conectadas. Dos repeticiones por celda, **las doce
idénticas al token**:  ‹v2.1.241›

| Herramientas MCP | Tokens de entrada | Coste del servidor |
|---:|---:|---:|
| Ninguna | 45.441 | |
| 3 (el del laboratorio) | 45.659 | **+218** |
| 12 | 45.772 | **+331** |

De tres herramientas a doce, nueve más, el coste sube 113 tokens: **unos 13
tokens por herramienta añadida**. Un servidor entero cuesta menos que dos líneas
de tu `CLAUDE.md`.

Así que el consejo se da la vuelta. **Conectar servidores es barato; el problema
de MCP nunca fue el contexto, es el permiso y la confianza**, que es de lo que va
el resto del módulo.

### 6.2.3 · Cuándo vuelve el impuesto, y cuánto duele

Tool search no está siempre. Deja de estarlo en cinco sitios, y cuatro de ellos
son configuraciones de empresa:

- **`ANTHROPIC_BASE_URL` apunta a un host que no es de primera parte.** Claude
  Code lo desactiva solo, porque la mayoría de proxies no reenvían los bloques
  `tool_reference`. Si tu arquitectura es una pasarela propia, **estás aquí**.
- **`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` puesto.** Queda apagado y
  **`ENABLE_TOOL_SEARCH` no puede con ello**.
- **Microsoft Foundry sobre Azure.** Lo rechaza el servidor. Tampoco se fuerza.
- **Agent Platform de Google con modelos anteriores a la generación 4.5.**
- **Un modelo sin soporte de `tool_reference`.** Hace falta Sonnet 4.5, Haiku
  4.5, Opus 4.5 o posterior.

La misma matriz de antes, apagándolo con `ENABLE_TOOL_SEARCH=false`, dos
repeticiones por celda:  ‹v2.1.241›

| Herramientas MCP | Con tool search | Sin tool search | Diferencia |
|---:|---:|---:|---:|
| Ninguna | 45.441 | 62.662 | **+17.221** |
| 3 | 45.659 | 63.220 | +17.561 |
| 12 | 45.772 | 65.016 | +19.244 |

Dos lecturas, y la primera no la esperábamos.

**Apagar tool search cuesta 17.221 tokens con cero servidores MCP conectados.**
No es un coste de MCP: es que los esquemas de las herramientas propias del CLI
también estaban diferidos. Es el número más grande de la tabla y no tiene nada
que ver con lo que este módulo trata. Si alguien de tu equipo apagó tool search
"porque no usamos MCP", está pagando diecisiete mil tokens por turno a cambio de
nada.

**Y el coste por herramienta se multiplica por dieciséis.** De 3 a 12
herramientas: con tool search, 13 tokens cada una; sin él, **200**. Ahí sí
vuelve el consejo antiguo, y solo ahí.

Comprobación en dos comandos, y en este orden: `/mcp` para lo que cuesta cada
servidor y `/context` para el reparto real de la sesión. **Mide antes de
desconectar nada.**

> **Esto va a cambiar.** Es la zona más movediza del CLI. Desde la 2.1.232 el
> cliente MCP usa un runtime nuevo con revisión de protocolo 2026-07-28 para
> servidores remotos que la soporten  ‹v2.1.232›, la organización puede fijar
> tool search desde configuración gestionada desde la 2.1.227  ‹v2.1.227›, y
> antes de la 2.1.214 un error pasajero al refrescar el catálogo de un servidor
> lo dejaba sin herramientas  ‹v2.1.214›. Comprueba tu versión antes de copiar
> una cifra de aquí.

### 6.2.4 · Ámbitos, y el detalle que no se fusiona

| Ámbito | Dónde vive | Quién lo ve |
|---|---|---|
| **Local** | `~/.claude.json`, por proyecto | Solo tú, solo ahí |
| **Proyecto** | `.mcp.json` del repositorio | Todo el equipo, va a git |
| **Usuario** | `~/.claude.json` | Tú, en todos tus proyectos |
| **De plugin** | Dentro del plugin | Quien lo instale |
| **Conectores de claude.ai** | Tu cuenta | Tú, en todas las superficies |

Precedencia, de más fuerte a menos: local, proyecto, usuario, plugin, conector.
Y dos detalles que cuestan una tarde:

- **Gana la entrada entera de la fuente que manda. Los campos no se fusionan.**
  No puedes poner la URL en el proyecto y la cabecera de autenticación en local:
  o una fuente o la otra.
- **Los tres primeros ámbitos detectan duplicados por nombre; los plugins y los
  conectores, por endpoint.** Un plugin que apunte a tu misma URL cuenta como
  duplicado aunque se llame distinto.

### 6.2.5 · La tercera puerta de entrada

Los módulos 04 y 05 dejaron un patrón: lo que un repositorio clonado te concede
necesita tu confianza, y lo que ejecuta, no. MCP es la tercera vuelta de tuerca,
y la medimos en el laboratorio.

Con el `.mcp.json` del proyecto puesto y **sin haberlo aprobado nunca**,
`claude mcp list` dice lo que esperas:

```
pedidos: python3 ... - ⏸ Pending approval (run `claude` to approve)
```

Y aun así, en `claude -p`, el servidor **conectó y sus herramientas estaban
disponibles**: el agente las encontró por tool search e intentó llamarlas. Dos
repeticiones. Lo único que faltaba era el permiso de la herramienta, no la
aprobación del servidor.

Consecuencia, y es la misma frase del módulo 05 con otro sujeto: **un repositorio
ajeno puede arrancarte un proceso.** Un `.mcp.json` confirmado en git es un
comando que se ejecuta en tu máquina. Antes de correr `claude -p` dentro de un
repositorio que no has escrito tú, mira su `.mcp.json` igual que miras su
`.claude/`. Para cerrarlo del todo: `--strict-mcp-config` usa solo los
servidores que le pases por `--mcp-config` e ignora los del repositorio.

Y lo que devuelve un servidor entra en tu contexto como cualquier otro texto, así
que **un servidor de terceros sin revisar es código de terceros ejecutándose con
tu confianza**. Por eso aquí la postura es lista blanca, no lista negra:
`deniedMcpServers` existe en la configuración gestionada, pero enumerar lo malo
siempre se queda corto.

### 6.2.6 · Límites de salida

Una herramienta que devuelve mucho es de las formas más rápidas de arruinar una
sesión. Tres números:

| Concepto | Valor |
|---|---|
| Umbral de aviso | **10.000 tokens** |
| Límite por defecto | **25.000 tokens** |
| Variable para cambiarlo | `MAX_MCP_OUTPUT_TOKENS` |

Con un matiz para quien escriba servidores: la variable solo aplica a las
herramientas que **no** declaran su propio límite. Una que fije
`anthropic/maxResultSizeChars` en su `tools/list` usa ese valor para el texto,
hasta medio millón de caracteres, pase lo que pase con la variable. Las que
devuelven imágenes siguen sujetas a ella.

Y por eso el servidor del laboratorio tiene un parámetro `limite` con tope: un
`SELECT *` contra una tabla de verdad se come los 25.000 sin despeinarse.

---

## 6.3 · Receta

### 6.3.1 · Añadir un servidor

```bash
# stdio, un proceso local
claude mcp add pedidos -- python3 ./mcp/servidor-pedidos.py

# remoto por HTTP con cabecera
claude mcp add --transport http interno https://api.empresa.com/mcp \
  --header "Authorization: Bearer ..."
```

El `--` no es decorativo: separa las opciones de Claude Code del comando del
servidor. Sin él, un `--port 8080` del servidor lo intenta interpretar el CLI
como suyo y falla.

Al servidor stdio se le pone `CLAUDE_PROJECT_DIR` en el entorno, apuntando a la
raíz del proyecto, para que resuelva rutas sin depender del directorio de
trabajo. Ojo con una asimetría: **dentro del `.mcp.json` esa variable necesita un
valor por defecto**, `${CLAUDE_PROJECT_DIR:-.}`, porque ahí la expansión ocurre
antes de que exista. Los servidores de plugin no lo necesitan.

Para depurar, `/mcp` desactiva un servidor sin borrarlo. Es lo que quieres en vez
de andar recortando el archivo.

### 6.3.2 · Equipo: el `.mcp.json` va a git, los secretos no

Es lo que hace compartible la configuración de MCP: la estructura se versiona,
los valores viven en el entorno de cada uno. Se expande `${VAR}` y
`${VAR:-porDefecto}` en `command`, `args`, `env`, `url` y `headers`.

```json
{
  "mcpServers": {
    "api-interna": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.empresa.com}/mcp",
      "headers": { "Authorization": "Bearer ${API_TOKEN}" }
    }
  }
}
```

Un `.mcp.json` con un token dentro es el módulo 04 otra vez: una regla de
permisos protege rutas, no valores, y ese archivo va a git por diseño.

Y para los remotos, **scopes mínimos**. Un servidor MCP con más permisos de los
que necesita es una escalada de privilegios esperando su turno.

### 6.3.3 · Construir el tuyo de solo lectura

Un servidor stdio es un programa que lee JSON-RPC por la entrada estándar y
escribe JSON-RPC por la salida, una línea por mensaje. Tres métodos bastan:
`initialize`, `tools/list` y `tools/call`. El del laboratorio son doscientas
líneas de Python **sin una sola dependencia**, y eso es a propósito: un servidor
que no puedes leer entero no lo puedes auditar, y ya vimos lo que entra en tu
contexto.

La parte que importa son **tres candados, y ninguno se fía del anterior**:

1. **El sistema de archivos.** La conexión se abre con
   `sqlite3.connect("file:...?mode=ro", uri=True)`. Quien deniega la escritura es
   SQLite, no tu código. Y en modo `ro` no crea la base si falta, en vez de
   crearla vacía.
2. **La forma de la sentencia.** Una sola, y empezando por `SELECT` o `WITH`. Un
   punto y coma en medio es el camino clásico para colar un `UPDATE` detrás de
   un `SELECT`, así que se rechaza.
3. **El autorizador del motor.** `set_authorizer` deniega toda operación que no
   sea leer. Es el que sigue en pie el día que alguien afloje los dos primeros.

Y una regla del transporte que hay que grabarse: **nunca imprimas por la salida
estándar nada que no sea un mensaje JSON-RPC**. Los avisos van por la de error.
Un `print` de depuración mal puesto rompe el transporte entero, y es el fallo
número uno del primer servidor de cualquiera.

### 6.3.4 · Cuándo no es un MCP

Tres casos donde la respuesta correcta es otra cosa:

**Cuando el dato está en el repositorio.** Ya sabe leer archivos. Un servidor
para eso añade una capa y no añade acceso.

**Cuando lo que quieres es imponer algo.** Un servidor MCP ofrece capacidades; no
obliga a nada. Lo que no es negociable es un hook, y eso fue el módulo 05.

**Cuando solo necesitas un comando.** Si la integración es "ejecuta esto y
devuélveme la salida", un script y una regla de permisos son menos piezas que un
servidor, y se auditan mejor.

---

## 6.4 · Laboratorio · La base de datos de `gestor-pedidos`, en solo lectura

Del módulo 05 traes tres hooks y un `HOOKS.md`. Hoy el repositorio gana lo
primero que mira hacia fuera.

**Paso 1. Construye la base de datos.** Está en `.gitignore` desde el módulo 04,
así que no viene en el clon: se construye. El esquema sí está versionado.

```bash
cd D6-repo-feo/gestor-pedidos
sqlite3 datos/pedidos.db < datos/esquema.sql
```

Y méte le unas filas, que una tabla vacía no demuestra nada. Catorce pedidos y
cinco clientes bastan.

**Paso 2. Comprueba el síntoma.** Sin nada conectado:

```
¿Cuántos pedidos hay en total en la base de datos?
```

Se pone a abrir archivos. No los encuentra, porque los datos no están en el
código.

**Paso 3. Escribe el servidor.** `mcp/servidor-pedidos.py`, con las tres
herramientas del laboratorio: `listar_tablas`, `describir_tabla` y `consultar`.
El del libro está en `D6-repo-feo/gestor-pedidos/mcp/`.

**Paso 4. Pruébalo en seco, sin Claude Code de por medio.** Igual que los hooks
del módulo 05: es un programa que lee JSON y escribe JSON.

```bash
export CLAUDE_PROJECT_DIR="$PWD"
printf '%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
 | python3 mcp/servidor-pedidos.py
```

Tienen que salir dos líneas de JSON: el `serverInfo` y las tres herramientas. Si
sale cualquier otra cosa por delante, tienes un `print` suelto.

**Paso 5. Prueba los candados, también en seco.** Por el mismo camino, pide
`consultar` con `DELETE FROM pedidos` y luego con
`SELECT 1; UPDATE pedidos SET total=0`. Los dos tienen que volver con
`isError` y su motivo. Y el primer candado se ve sin el servidor:

```bash
python3 -c "
import sqlite3
con=sqlite3.connect('file:datos/pedidos.db?mode=ro',uri=True)
con.execute('DELETE FROM pedidos')"
```

`attempt to write a readonly database`. Eso lo dice SQLite, no tú.

**Paso 6. Conéctalo.** `.mcp.json` en la raíz del laboratorio, con
`${CLAUDE_PROJECT_DIR:-.}` en la ruta, y `claude mcp list` para ver que aparece.

**Paso 7. Repite el paso 2.** Nuestro resultado, dos veces: **14**, y las
herramientas usadas en el turno fueron `ToolSearch` y
`mcp__pedidos__consultar`. **Ni un `Read`, ni un `Bash`.** Ese es el criterio
PASA del módulo, y conviene verlo en la lista de llamadas, no en la respuesta:

```bash
claude -p "¿Cuántos pedidos hay?" --output-format stream-json --verbose \
  | jq -r 'select(.type=="assistant") | .message.content[]?
           | select(.type=="tool_use") | .name'
```

**Paso 8. Mide lo que cuesta tenerlo.** La petición trivial del módulo 04
(`Responde solo con la palabra OK.`) con el servidor y sin él, moviendo el
`.mcp.json` a un lado. Nosotros: **45.659 frente a 45.441 tokens**, dos
repeticiones cada uno, idénticas. **218 tokens por tres herramientas.**

**Paso 9. Apaga tool search y vuelve a medir.** El mismo par con
`ENABLE_TOOL_SEARCH=false` delante: 63.220 y 62.662. Fíjate en la columna que no
esperabas: sin ningún servidor conectado, apagarlo ya cuesta **17.221 tokens**.

**Paso 10. Encuentra la puerta tú mismo.** Con el `.mcp.json` sin aprobar,
`claude mcp list` dice `Pending approval`. Lanza igualmente
`claude -p` y mira la lista de llamadas del paso 7: las herramientas del
servidor están ahí. Repítelo con `--strict-mcp-config` y desaparecen.

**Paso 11. Escribe por qué.** `MCP.md`, con qué expone el servidor, qué no puede
hacer y cuál de los tres candados lo impide. El del laboratorio está en
`D6-repo-feo/gestor-pedidos/MCP.md`.

---

## 6.5 · Prueba

**PASA** si se cumplen las cuatro:

1. El agente responde cuántos pedidos hay **sin abrir un solo archivo**, y lo has
   comprobado en la lista de llamadas a herramientas, no en la respuesta.
2. Las tres pruebas en seco del paso 5 devuelven error, y sabes decir qué candado
   paró cada una.
3. Tienes tu propio número del coste del servidor, y no es una estimación.
4. Sabes qué le pasa a un `.mcp.json` de un repositorio ajeno cuando lanzas
   `claude -p` dentro.

**FALLA** si tu conclusión es que la base de datos ya está a salvo porque el
agente dice que es de solo lectura. En nuestra medición, al pedirle que borrara
los pedidos, el agente se negó **citando las instrucciones del servidor y sin
llegar a llamar a la herramienta**, las dos veces. Eso no es un candado: es la
misma negativa por criterio propio que el módulo 05 midió en 5 de 7. Lo que
protege la base son los tres candados del servidor, y por eso se prueban en seco.

---

## 6.6 · Coste de este módulo

| Concepto | Cantidad |
|---|---|
| Tokens de entrada del laboratorio | ~900.000 |
| Tokens de salida | ~1.000 |
| Coste medido por el CLI | 0,65 dólares |
| Coste en euros | por debajo de 0,75 € |
| Tiempo | 35 minutos |
| **Impuesto de contexto del servidor** | **+218 tokens por turno, medido** |
| Coste por herramienta añadida | ~13 tokens con tool search, ~200 sin él |
| Mantenimiento continuo | el esquema de la base, y revisar servidores ajenos |

**Un servidor MCP es la pieza más barata de las cinco que llevamos.** Ponlo al
lado de las otras, todas medidas en la misma máquina con la misma petición:

| Pieza | Coste por turno |
|---|---:|
| Reglas de permisos, 24 de ellas (módulo 04) | **0** |
| Seis hooks declarados (módulo 05) | **0** |
| Servidor MCP de 3 herramientas | **218** |
| `CLAUDE.md` de 67 líneas (módulo 03) | **1.311** |
| Apagar tool search, sin MCP ninguno | **17.221** |

La última fila es la que hay que enseñarle a quien decide en tu empresa. **La
configuración que alguien puso "por prudencia" cuesta ochenta veces más que el
servidor que nadie deja conectar.** Y la penúltima recuerda que el archivo de
memoria sigue siendo, con diferencia, lo más caro que escribes a mano.

El mantenimiento real no es el servidor, es el esquema: el día que alguien
renombre una columna, tu servidor sigue funcionando y devolviendo error, y el
agente te dirá que no encuentra los datos. Es un fallo ruidoso, que es el que se
quiere.

Y queda pendiente lo de siempre: la clave de la pasarela sigue dentro de
`app.py`. El servidor de hoy no la toca, porque no lee código. Módulo 12.

---

## Runbook · Módulo 06

> **"Mi servidor no aparece"**
>
> 1. `claude mcp list`: ¿sale, y en qué estado? `Pending approval` en una sesión
>    interactiva se resuelve con `/mcp`.
> 2. ¿JSON válido? Una coma de más y el archivo entero deja de aplicarse.
> 3. ¿Le faltó el `--` al añadirlo? Sin él, el CLI intenta parsear los flags del
>    servidor como suyos.
> 4. En seco: `printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | tu-servidor`
> 5. ¿Imprime algo que no sea JSON-RPC por la salida estándar? Eso rompe el
>    transporte. Los avisos, por la de error.
>
> **Ámbitos y precedencia**
> Local → proyecto (`.mcp.json`) → usuario → plugin → conector de claude.ai.
> **Gana la entrada entera; los campos no se fusionan entre ámbitos.**
> Duplicados: por nombre en los tres primeros, por endpoint en plugins y
> conectores.
>
> **Lo que cuesta**
> Con tool search, que es el defecto: ~13 tokens por herramienta. Un servidor de
> 3 son 218 por turno. Sin tool search: ~200 por herramienta, y **17.221 de
> entrada aunque no tengas ningún servidor**.
> Mide con `/mcp` y `/context` antes de desconectar nada.
>
> **Dónde NO hay tool search**
> `ANTHROPIC_BASE_URL` no de primera parte · `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`
> · Foundry en Azure · Agent Platform con modelos previos a 4.5 · modelo sin
> `tool_reference`. En los tres últimos, `ENABLE_TOOL_SEARCH` no lo arregla.
>
> **Límites de salida**
> Aviso a los 10.000 tokens, tope a los 25.000, `MAX_MCP_OUTPUT_TOKENS` para
> cambiarlo. Una herramienta que declare `anthropic/maxResultSizeChars` usa el
> suyo. Una llamada que pase de dos minutos se va a segundo plano.  ‹v2.1.212›
>
> **Antes de correr `claude -p` en un repositorio ajeno**
> Su `.mcp.json` arranca procesos en tu máquina, y en `-p` sus herramientas
> están disponibles aunque el servidor figure como pendiente de aprobar.
> `--strict-mcp-config` con `--mcp-config` ignora los del repositorio.
>
> **Servidor propio de solo lectura: los tres candados**
> Conexión `mode=ro` por URI · una sola sentencia y que empiece por `SELECT` o
> `WITH` · `set_authorizer` denegando todo lo que no sea leer.
> Se prueban en seco. La negativa del agente no cuenta como candado.
