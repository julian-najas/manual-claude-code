# Módulo 09 · Git, CI e IDE

> **Laboratorio de este módulo:** ~55 minutos · treinta y una ejecuciones, unos
> **1.958.000 tokens de entrada** y 4.100 de salida · **1,92 dólares** sumando
> las 45 llamadas que registró el propio CLI, que a cualquier cambio euro-dólar
> de agosto de 2026 se queda **por debajo de 2,15 €**. Con suscripción va
> incluido.
> **Verificado contra:** Claude Code 2.1.247 · 27 de agosto de 2026.

> **Nota de versión.** Es la zona del libro que más se mueve. Lo del CLI está
> medido; lo de la forja sale de la documentación oficial de ese mismo día.

---

## 9.1 · Síntoma

Montaste la revisión automática en la tubería (pipeline) un viernes. Funcionó a
la primera. Y desde entonces aprueba todo.

O peor: no es que apruebe todo, es que no corre. Sale en verde porque el paso
terminó, y el paso terminó porque el proceso salió con cero, y salió con cero
porque nadie llegó a preguntarle nada. Llevas seis semanas creyendo que tienes
una puerta de calidad y lo que tienes es una línea en un archivo YAML. Y de
fondo, alguien de finanzas preguntando por qué la factura de revisiones de este
mes es de tres cifras.

Los tres son el mismo fallo con tres caras: **en la CI nadie mira**. Aquí se
mide qué cambia cuando se apaga la luz.

---

## 9.2 · Modelo mental

### 9.2.1 · La CI no es tu terminal, y lo que carga tampoco

Lo primero que hay que desmontar es que `claude -p` en un runner sea tu sesión
sin colores. Misma petición trivial de siempre (`Responde solo con la palabra
OK.`), dos repeticiones por fila, las ocho **idénticas al token**:  ‹v2.1.247›

| Dónde y cómo | Tokens de entrada |
|---|---:|
| Un directorio vacío | 44.208 |
| `gestor-pedidos`, tal cual, todo cargado | **45.989** |
| `gestor-pedidos` con `--strict-mcp-config` | 45.771 |
| `gestor-pedidos` con `--safe-mode` | 41.924 |

**Lo que dejaron los módulos 03 a 07 cuesta 1.781 tokens por turno**, que es lo
que la CI paga en cada ejecución por tener un `CLAUDE.md`, una skill, un
servidor MCP, tres hooks y un archivo de permisos.

Y cuadra con lo medido desde el módulo 03: las piezas, una a una en su módulo,
suman 1.737 (memoria 1.311, skill 208, servidor MCP 218). Todas juntas y en otra
versión del CLI, 1.781. **Cuarenta y cuatro tokens de diferencia sobre mil
setecientos.** El impuesto de contexto no es una metáfora: se suma. Y la tercera
fila lo confirma aparte, porque quitar el servidor MCP cuesta exactamente **218
tokens**, el número del módulo 06 contra la 2.1.241.

### 9.2.2 · Lo que sí corre en un espacio que nadie ha aprobado

Una ejecución con `-p` **no muestra el diálogo de confianza del espacio de
trabajo** (workspace trust): no hay nadie para contestarlo. Lo que pasa entonces
no es lo que casi todo el mundo supone. Sobre `gestor-pedidos`, en un sandbox
donde nunca se aceptó esa confianza, dos ejecuciones idénticas:  ‹v2.1.247›

| Qué trae el repositorio | Qué hace la CI con ello |
|---|---|
| Los hooks de `.claude/settings.json` | **Los ejecuta.** Un `hook_started` y un `hook_response` con código 0 |
| Las entradas de `permissions.allow` del mismo archivo | **Las ignora**, y lo dice por la salida de error |
| Las reglas `deny` y `ask` del mismo archivo | Las aplica |
| El servidor de `.mcp.json` | Lo conecta |

El aviso, literal, va por la salida de error y no por la de datos:

```text
Ignoring 3 permissions.allow entries from .claude/settings.json: this
workspace has not been trusted.
```

> **Tu CI ejecuta los scripts del repositorio que acaba de clonar y descarta sus
> permisos.** Y si el runner atiende propuestas de cambio de bifurcaciones
> (forks), ese `hooks/loquesea.sh` lo ha escrito un desconocido.

Que se ignore `allow` y no `deny` tiene lógica: una lista blanca del repositorio
sería concederse permisos a sí mismo. Pero el efecto práctico es que tus
permisos, los del módulo 04, **no llegan enteros**, y tus hooks, los del módulo
05, sí. Conviene saber cuál de los dos te estaba protegiendo.

### 9.2.3 · `--bare`, y el peaje que no está en el titular

La respuesta de la documentación a todo lo anterior es `--bare`, que se salta
los hooks, la sincronización de plugins, la memoria automática y el
descubrimiento de `CLAUDE.md`  ‹v2.1.247›. Es el modo recomendado para scripts y
para el SDK, y va a ser el valor por defecto de `-p` en una versión futura. Lo
que necesites se pasa a mano: `--append-system-prompt`, `--settings`,
`--mcp-config`, `--agents`, `--plugin-dir`.

El titular es bueno. El peaje va en la letra pequeña: **en modo bare no se leen
ni las credenciales OAuth ni el llavero del sistema.** La autenticación es
estrictamente `ANTHROPIC_API_KEY`, o un `apiKeyHelper` por `--settings`. Medido
en una máquina de suscripción, sin esa variable, dos ejecuciones iguales:
 ‹v2.1.247›

```text
exit 1 · is_error: true · terminal_reason: api_error
result: "Authentication error · This may be a temporary network issue,
         please try again"
```

Ni una palabra sobre bare ni sobre el llavero: invita a reintentar un problema
que no se arregla reintentando.

> **La bandera que hace tu CI reproducible es la misma que te obliga a sacar una
> clave de API.** Si tu equipo trabaja con la suscripción, `--bare` no es una
> mejora que puedas activar el martes: es una decisión de facturación.

Hay un intermedio que sí funciona con la sesión de siempre y que en el
laboratorio se llevó por delante **4.065 tokens**: `--safe-mode`, que apaga
`CLAUDE.md`, skills, plugins, hooks, servidores MCP y comandos, y deja
autenticación y permisos como estaban. No es reproducible entre máquinas, pero
para una puerta que no debe leer el criterio de quien juzga, vale.

### 9.2.4 · Salir con cero no significa que haya salido bien

La tabla que hay que pegar en la pared antes de escribir un paso de CI, con
cuatro situaciones medidas dos veces cada una:  ‹v2.1.247›

| Qué pasó | Código de salida | `is_error` | `subtype` | ¿campo `result`? |
|---|---:|---|---|---|
| Todo bien | 0 | `false` | `success` | sí |
| Fallo de autenticación | 1 | **`true`** | **`success`** | sí, con el error dentro |
| Tope de presupuesto agotado | 1 | `true` | `error_max_budget_usd` | **no existe** |
| Bandera inválida | 1 | (no hay JSON) | (no hay JSON) | (no hay JSON) |

Dos trampas, y las dos muerden en silencio.

**`subtype` no es la puerta.** En el fallo de autenticación vale `success`
mientras `is_error` vale `true`. Un paso que decida con `subtype` aprueba una
fusión porque el modelo no llegó a hablar.

**Y `result` puede no existir.** Con el tope de presupuesto agotado el JSON trae
`errors` y no trae `result`, así que un `jq -r '.result'` devuelve `null` sin
fallar, y una puerta que encadene eso a un `grep` aprueba cada vez que se queda
sin dinero.

De ahí la regla, en este orden: **primero si la ejecución fue válida (`is_error`
y que `result` exista), y solo después qué dijo.**

### 9.2.5 · El presupuesto no es un presupuesto, es un freno

`--max-budget-usd` existe, funciona y solo va con `--print`  ‹v2.1.247›. Lo que
no hace es lo que su nombre promete. Con un tope de 0,01 dólares sobre una tarea
que se lo iba a gastar, dos ejecuciones:

| Repetición | Tope | Coste real antes de parar |
|---|---:|---:|
| Primera, caché fría | 0,01 $ | **0,193 $** |
| Segunda, caché caliente | 0,01 $ | **0,043 $** |

Las dos salieron con código 1 y `error_max_budget_usd`, y las dos se pasaron.
**El tope se comprueba entre llamadas, no antes**, así que la que lo agota ya
está pagada. La diferencia entre las dos cifras es la caché de prompt, fría la
primera vez y caliente la segunda, y avisa de que el coste de una sola ejecución
no significa nada. Sirve para que un bucle desbocado no se coma la tarjeta; no
para presupuestar por propuesta de cambio.

### 9.2.6 · Los tres niveles de revisión, y cuál cuesta cuánto

No es una sola cosa, y elegir mal se paga en dinero o en confianza.

| | `/code-review` | `/code-review ultra` | Code Review en la propuesta |
|---|---|---|---|
| Dónde corre | Tu sesión, en local | Sandbox en la nube | En la forja |
| Profundidad | Escala con el argumento de esfuerzo | Flota de agentes con verificación independiente | Automática |
| Duración | Segundos a minutos | 5 a 10 minutos | 20 minutos de media |
| Coste | Uso normal del plan | **5 a 25 $** en créditos | **15 a 25 $** por revisión |

⚠️ Los dos de la derecha **facturan contra créditos de uso, no contra tu plan**.
Pro y Max traen tres ultrarrevisiones gratis que **no se renuevan**; Team y
Enterprise, ninguna. A veinte personas y en modo "en cada empujón", la factura
se construye sola en una semana.

Tres detalles más: **`/review` es un alias de `/code-review`**  ‹v2.1.223› y sin
nivel de esfuerzo **reutiliza el último que escribiste**; la local corre **en
segundo plano, con ventana propia**  ‹v2.1.218›; y **Claude puede lanzarla por
su cuenta**  ‹v2.1.246›, lo que se apaga con
`skillOverrides: {"code-review": "user-invocable-only"}`.

Y el que decide si se lee: la comprobación de Code Review en la forja
**termina siempre con conclusión neutra**, así que nunca bloquea una fusión; hay
que leer su recuento por severidad desde tu propia CI. Qué es importante **aquí**
se calibra en un `REVIEW.md` en la raíz, con una trampa: se pega literalmente y
**la importación con `@` no se expande**.

---

## 9.3 · Receta

### 9.3.1 · Individual: la llamada que se puede meter en un script

Cuatro banderas y ya es una herramienta de línea de comandos más:

```bash
git diff --no-color "origin/main...HEAD" \
  | claude --bare -p "Eres una puerta de calidad de CI. Te llega un diff. Decide si BLOQUEA la fusion." \
      --output-format json \
      --json-schema '{"type":"object","properties":{"bloquea":{"type":"boolean"},"motivo":{"type":"string"}},"required":["bloquea","motivo"]}' \
      --max-budget-usd 0.50 \
      --allowedTools ""
```

Las que no son obvias:

- **`--json-schema`** convierte el veredicto en un booleano. Sin él tienes un
  párrafo, y un párrafo se interpreta con expresiones regulares, que es como se
  construye una puerta que un día dice lo contrario de lo que quería decir. Ojo:
  antes de la 2.1.205 un esquema inválido **se ignoraba en silencio**
   ‹v2.1.205›.
- **`--allowedTools ""`** la deja sin herramientas: el diff le llega por la
  entrada estándar, así que **lo que no puede abrir no lo puede filtrar**. Y
  **`--max-budget-usd`** es el freno de 9.2.5.

Y el veredicto se lee en dos pasos:

```bash
python3 - <<'FIN'
import json, sys
d = json.load(open("veredicto.json"))
if d.get("is_error") or "result" not in d:
    print("La puerta no llegó a emitir veredicto:", d.get("subtype"))
    sys.exit(1)
sys.exit(1 if (d.get("structured_output") or {}).get("bloquea") else 0)
FIN
```

### 9.3.2 · Equipo: el flujo, ordenado por precio

Tres trabajos, y el orden no es estético: **lo que no gasta dinero corre
primero.** Si las dependencias no se instalan o las pruebas fallan, la puerta no
llega a arrancar y el fallo cuesta cero.

| Trabajo | Qué hace | Cuándo falla |
|---|---|---|
| `entorno` | `pip install --no-deps` y `pip check` | El cierre de dependencias está incompleto |
| `pruebas` | `pytest -q` | Una prueba falla, o no hay ninguna |
| `puerta` | `claude --bare -p` sobre el diff | No hay veredicto, o el veredicto es bloquear |

El archivo entero está en `D6-repo-feo/gestor-pedidos/.github/workflows/ci.yml`.
Y una decisión que no se ve en la tabla: la puerta corre **solo en propuestas de
cambio** y **solo sobre el diff**, porque releer el repositorio entero en cada
empujón es gasto sin criterio.

Un cuarto trabajo que casi nadie pone: **fallar si un plugin o un servidor MCP
no cargó**. Medido: una entrada con `url` y sin `type` no rompe nada, se salta,
la ejecución sale con cero, y el único rastro es `type: url_missing_type` dentro
de `mcp_server_errors` del evento de inicio  ‹v2.1.219›. El aviso por la salida
de error **solo se imprime al correr a mano en una terminal**; con la salida
redirigida, que es lo que hace cualquier CI, no hay aviso. Sin ese trabajo
puedes llevar un mes sin la mitad de tus herramientas.

### 9.3.3 · Fijar dependencias: tres líneas son quince paquetes

El `requirements.txt` del laboratorio tenía tres líneas sin versión: `flask`,
`requests` y `sqlalchemy`. En un entorno limpio, el 27 de agosto de 2026, esas
tres líneas resuelven a **quince paquetes**: doce decisiones de versión que no
toma nadie del equipo y que cambian solas entre una instalación y la siguiente.

La prueba es de una línea, con el archivo viejo y `--no-deps`, que instala
exactamente lo que pone y nada más:

```text
$ pip install --no-deps -r requirements.txt && pip check
requests 2.34.2 requires certifi, which is not installed.
flask 3.1.3 requires werkzeug, which is not installed.
[... doce en total ...]
exit 1
```

Se arregla generándolo, no editándolo:

```bash
pip install flask requests sqlalchemy && pip freeze > requirements.txt
```

Lo de pruebas va aparte, en un `requirements-dev.txt` que empieza por
`-r requirements.txt`: lo que la CI instala para probar no es lo que se
despliega, y mezclarlos acaba con `pytest` en producción sin que nadie lo
decida.

### 9.3.4 · Varios árboles a la vez, y trabajo en segundo plano

**`-w`, `--worktree`** abre la sesión en un árbol de trabajo de git nuevo
 ‹v2.1.247›, así que dos tareas sobre el mismo repositorio no se pisan los
archivos. **`--bg`, `--background`** la arranca como agente de fondo y devuelve
el control; se gestionan con `claude agents`, que con `--json` lista las activas
sin necesitar terminal.

Un detalle que evita un cuelgue: un subagente de fondo dentro de un `claude -p`
**se espera**, con un tope de diez minutos  ‹v2.1.182› ajustable por
`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`. Los procesos de `Bash` de fondo, en
cambio, se cortan unos cinco segundos después del resultado.

### 9.3.5 · El IDE es una tercera superficie, y también carga cosas

La extensión de VS Code no es el CLI con botones. Corre **un servidor MCP local
propio, llamado `ide` y oculto en `/mcp`**, y mientras está conectado **manda tu
selección actual y la ruta del archivo abierto como contexto en cada petición**;
en la transcripción se ve como `⧉ Selected N lines from <archivo>`.

Se apaga por archivo con una regla `deny` de lectura, la del módulo 04: una
regla que case impide **tanto el texto seleccionado como el aviso de archivo
abierto**. Es la razón práctica de tener `Read(./.env*)` en `deny` aunque nunca
pienses pedirle que lo lea.

---

## 9.4 · Laboratorio · Que la CI falle por lo que tiene que fallar

Del módulo 08 traes un revisor que encuentra lo que el autor no. Hoy el
repositorio consigue lo que no ha tenido nunca: una red.

**Paso 1. Comprueba que hoy no hay nada.** Sobre `gestor-pedidos` tal cual,
`python3 -m pytest -q` sale `no tests ran` y **código de salida 5**. Ni 0 ni 1.
Un `|| true` puesto para callarlo deja la CI en verde con cero pruebas durante
años.

**Paso 2. Demuestra que las dependencias no están fijadas.** En un entorno
virtual limpio, `pip install --no-deps -r requirements.txt && pip check`. Doce
paquetes nombrados y código 1. Publica los tuyos: el árbol cambia.

**Paso 3. Fija el cierre entero.** `pip install flask requests sqlalchemy` y
`pip freeze > requirements.txt`. Quince líneas. Repite el paso 2: `No broken
requirements found`, código 0.

**Paso 4. Escribe las primeras pruebas, y escríbelas mal a propósito.** Nueve
en `tests/test_caracterizacion.py`, y **cinco empiezan por `test_hoy_`**: el IVA
español cobrado a Francia, el mismo IVA sin país, los dos descuentos de cantidad
acumulándose, el apóstrofo que tumba `/buscar` y el pedido inexistente que
responde 200 con `null`. No prueban lo que la aplicación debería hacer, prueban
lo que hace. **El día que el módulo 12 arregle el IVA, esas cinco tienen que
fallar: que fallen es el trabajo que hacen.** Una red no dice adónde ir, dice
desde dónde te has caído.

**Paso 5. Mide lo que la CI paga por tu configuración.** La petición trivial de
siempre, en un directorio vacío y en el laboratorio:

```bash
claude -p "Responde solo con la palabra OK." --output-format json \
  | python3 -c "import json,sys; u=json.load(sys.stdin)['usage']; print(u['input_tokens']+u['cache_creation_input_tokens']+u['cache_read_input_tokens'])"
```

44.208 y 45.989. **1.781 tokens** de diferencia, que tienen que parecerse a la
suma de lo que fuiste midiendo módulo a módulo.

**Paso 6. Comprueba qué corre sin que nadie lo apruebe.** Con los eventos de
hook a la vista y la salida de error aparte:

```bash
claude -p "Lee la primera linea de app.py y dime que dice." \
  --allowedTools "Read" --output-format stream-json --verbose \
  --include-hook-events 2>errores.txt \
  | grep -o '"subtype":"hook_response"'
```

Sale. Y en `errores.txt` está el `Ignoring 3 permissions.allow entries`, en la
misma ejecución: **el script del repositorio se ejecuta y sus permisos no.**

**Paso 7. Prueba `--bare` y encuentra el peaje.** Repite el paso 5 con `--bare`.
Por suscripción sale `Authentication error` con `is_error: true`. Ahí se decide
si vuestra CI lleva clave de API o se queda en `--safe-mode`.

**Paso 8. Rompe la puerta a propósito.** Monta la llamada de 9.3.1 y pásale el
diff que **quita** las versiones de `requirements.txt`, con `git diff -R`: dos
de dos, `bloquea: true`. Pásale el que las pone: dos de dos, `bloquea: false`. Y
después ponle `--max-budget-usd 0.01` y mira lo que devuelve, que no trae campo
`result`. **Esa es la ejecución que tu paso tiene que suspender, y la que casi
todos aprueban.**

**Paso 9. Escribe el porqué.** `CI.md`, al lado de `HOOKS.md`, `MCP.md`,
`SKILLS.md` y `AGENTES.md`: qué comprueba, en qué orden, qué cuesta y **qué no
cubre**. El del laboratorio dice, entre otras cosas, que la puerta mira el diff
y no el repositorio, así que la clave de 2019 no la ve nunca.

---

## 9.5 · Prueba

**PASA** si se cumplen las cuatro:

1. La CI **falla** con el repositorio tal cual estaba, y por los dos motivos
   correctos: `pip check` nombrando paquetes que faltan y `pytest` saliendo con
   5. No por una plantilla mal copiada.
2. La CI **pasa** después de arreglar el fallo 9 (dependencias sin fijar) y el
   14 (cero pruebas), y solo por eso.
3. Tienes una ejecución guardada en la que la puerta **no emitió veredicto** y
   tu paso la suspendió. Sin esa, tu puerta no está probada: está estrenada.
4. `CI.md` está en el control de versiones y dice **qué no cubre** la CI.

**FALLA** si tu paso decide con `subtype`, o si lee `result` sin comprobar antes
`is_error`. Un fallo de autenticación devuelve `is_error: true` con
`subtype: success`, y un presupuesto agotado devuelve un JSON **sin campo
`result`**: las dos se aprueban solas en casi todos los flujos escritos por ahí.

> **Esto va a cambiar.** `--bare` va camino de ser el valor por defecto de `-p`,
> y el día que lo sea, cualquier flujo que hoy dependa de que el `CLAUDE.md` se
> cargue dejará de comportarse igual sin que nadie toque nada. Los precios de
> revisión son del 27 de agosto de 2026 y son de lo que más envejece. Lo que
> esperamos que aguante es la forma: en la CI nadie mira, así que la validez de
> la ejecución se comprueba antes que el contenido.

---

## 9.6 · Coste de este módulo

| Concepto | Cantidad |
|---|---|
| Tokens de entrada del laboratorio | ~1.958.000 |
| Tokens de salida | ~4.100 |
| Coste, de las 45 llamadas que registró el CLI | 1,92 dólares |
| Coste en euros | por debajo de 2,15 € |
| Tiempo | 55 minutos |
| **Impuesto de contexto de todo el repositorio, por turno** | **1.781 tokens** |
| Lo que quita `--safe-mode` | 4.065 tokens |
| Lo que quita `--strict-mcp-config` | 218 tokens |
| Una puerta sobre un diff pequeño | 0,013 a 0,19 $ por ejecución |
| Mantenimiento continuo | regenerar el cierre de dependencias, releer el `REVIEW.md` |

La tabla comparada, misma máquina y misma petición trivial:

| Pieza | Coste por turno |
|---|---:|
| Reglas de permisos, módulo 04 | 0 |
| Hooks declarados, módulo 05 | 0 |
| Un subagente declarado, módulo 08 | 105 |
| Una skill instalada, módulo 07 | 208 |
| Un servidor MCP de tres herramientas, módulo 06 | 218 |
| `CLAUDE.md` de 67 líneas, módulo 03 | 1.311 |
| **El laboratorio entero, que es lo que paga la CI** | **1.781** |

La última fila es el módulo entero en un número, y en ella no está el subagente,
que el laboratorio prueba con `--agents` sin dejarlo declarado. Ninguna pieza es
cara: **lo caro es la suma, y se paga en cada turno.** Cien ejecuciones al día
son 178.000 tokens de entrada solo por tener el proyecto configurado.

El coste real no está en esa tabla: está en los dos números de 9.2.5, un tope de
un céntimo que se gastó diecinueve. **La única cifra fiable de gasto sale de
sumar `total_cost_usd` de lo que ya ha terminado.**

Y el mantenimiento no es el archivo YAML: es que **el cierre de dependencias
caduca**. Quince líneas fijadas hoy arrastran vulnerabilidades conocidas dentro
de tres meses si nadie las regenera. Fijar no es congelar: es hacer explícito
quién decide cuándo se mueve.

Queda pendiente lo de siempre, hoy con nombre: la puerta mira el diff, y la
clave de pasarela de `app.py` no está en ningún diff desde 2019. Ninguna
revisión automática de propuestas la va a encontrar. Eso es el módulo 10.

---

## Runbook · Módulo 09

> **"Mi puerta aprueba todo"**
>
> 1. ¿Decides con `subtype`? No sirve: un fallo de autenticación devuelve
>    `is_error: true` con `subtype: success`.
> 2. ¿Lees `result` directamente? Con el presupuesto agotado **ese campo no
>    existe** y `jq -r '.result'` te da `null` sin fallar.
> 3. Orden correcto: primero `is_error` y que `result` exista; después
>    `structured_output`.
> 4. ¿Devuelve un párrafo? `--json-schema`, y que devuelva un booleano.
>
> **"Falta la mitad de mis herramientas y nadie se enteró"**
> Un servidor MCP mal declarado **se salta y la ejecución sale con cero**. El
> rastro está en `mcp_server_errors` del evento de inicio  ‹v2.1.219›, y el
> aviso por la salida de error no se imprime si está redirigida. Falla con ese
> array no vacío. Lo mismo con `plugin_errors`.
>
> **"`--bare` no arranca"**
> En modo bare **no se lee ni OAuth ni el llavero**. Exige `ANTHROPIC_API_KEY` o
> un `apiKeyHelper` por `--settings`. El error dice `Authentication error` y no
> lo menciona. Por suscripción, la alternativa parcial es `--safe-mode`.
>
> **"La CI ejecuta cosas del repositorio que nadie ha aprobado"**
> Con `-p` no hay diálogo de confianza. **Los hooks del repositorio se ejecutan;
> sus `permissions.allow` se ignoran.** Con bifurcaciones, eso es código ajeno
> en tu runner. Se cierra con `--bare`.
>
> **"La factura de revisión se ha disparado"**
> Forja: 15 a 25 $ **por revisión**, y en modo "en cada empujón" se multiplica.
> Ultrarrevisión: 5 a 25 $, tres gratis en Pro y Max que **no se renuevan**,
> ninguna en Team ni Enterprise. Las dos contra créditos, no contra el plan.
>
> **"La revisión no aplica nuestras reglas"**
> `REVIEW.md` en la raíz, y **`@` no se expande ahí**. Su comprobación **nunca
> bloquea**: para bloquear hay que leer su recuento por severidad.
>
> **Lo que cuesta**
> Tu configuración entera: **1.781 tokens por turno**. `--safe-mode` quita
> 4.065; `--strict-mcp-config`, 218. **`--max-budget-usd` es un freno, no un
> presupuesto**: la llamada que lo agota ya está pagada.
>
> **Dependencias**
> `pip install --no-deps -r requirements.txt && pip check`. Si nombra paquetes,
> tu archivo es una sugerencia, no un cierre.
