# Módulo 11 · Troubleshooting

> **Laboratorio de este módulo:** ~45 minutos · treinta y una invocaciones del
> CLI, quince de ellas con el JSON conservado: **947.086 tokens de entrada** y
> 2.025 de salida · **0,61 dólares** sumando lo que devolvió cada ejecución, que
> a cualquier cambio euro dólar de agosto de 2026 se queda **por debajo de
> 0,70 €**. Con suscripción va incluido.
> **Verificado contra:** Claude Code 2.1.252 · 1 de septiembre de 2026.

> **Nota de versión.** Cierra un pendiente que el módulo 10 dejó abierto hace un
> día: por qué no llegaba ni un evento de telemetría. Está en 11.2.5.

---

## 11.1 · Síntoma

"Ayer funcionaba."

Nadie ha tocado nada. Eso lo has preguntado ya dos veces. La aplicación devuelve
doscientos, los tests pasan, la CI está en verde y el agente responde. Y sin
embargo los avisos por correo llevan semanas sin llegar, y nadie sabe desde
cuándo, porque **no hay una fecha a partir de la cual empezar a mirar**.

La tarde no se va en arreglar, que son diez minutos. Se va en encontrar algo que
arreglar, a ciegas, en un sistema que no se queja.

Eso no es mala suerte: es el efecto de una decisión que alguien tomó, casi
siempre con buena intención. **Alguien se tragó el error.** Aquí fue Rubén en
2019, con un `except:` desnudo y un comentario amable al lado. En tu herramienta
lo hace un aviso que sale por la salida de error mientras tu script lee la de
datos.

Es el mismo fallo en dos capas, y por eso el módulo trata las dos a la vez. El
método no empieza por adivinar la causa: empieza por **devolver el error a un
canal que alguien lea**.

---

## 11.2 · Modelo mental

### 11.2.1 · Cuando ves el mensaje, los reintentos ya se hicieron

Lo primero, porque cambia cómo se leen todos los demás errores: Claude Code
**reintenta los fallos transitorios hasta diez veces con retroceso exponencial
antes de enseñarte nada**  ‹v2.1.252›. Relanzar "a ver si esta vez pilla" no es
un diagnóstico: es repetir el último intento de una serie de diez.

La distinción que más ahorra: un fallo de validación de certificado TLS **no se
reintenta a propósito**, para que lo veas a la primera. Si tu red mete un proxy
de inspección y falta el paquete de certificados, perseguirlo como intermitente
es una tarde tirada.

### 11.2.2 · El catálogo crece más rápido de lo que se puede memorizar

La documentación mantiene un catálogo de errores **indexado por mensaje
literal**, con una tabla de cabecera de **205 filas**  ‹v2.1.252›. Lo que ha
hecho en veinte días:

| | 12-ago-2026 · 2.1.228 | 1-sep-2026 · 2.1.252 |
|---|---:|---:|
| Entradas del catálogo | 83 | **106** |
| Tamaño de la página | 223.030 B | **347.515 B** |

De ahí la única conclusión operativa que aguanta: **memorizar errores no escala,
y buscarlos por paráfrasis tampoco**. Se indexa por el mensaje literal porque es
lo que tú tienes delante: cópialo entero, con sus comillas y sus nombres de
archivo, y búscalo tal cual.

La categoría más poblada sigue siendo **autenticación**, con veinte entradas, más
del doble que la siguiente: el dolor real de una instalación de equipo no está en
el modelo, sino en quién eres y contra qué te identificas.

### 11.2.3 · Tu CLI tiene su propio `except:` desnudo

La pieza que hay que llevarse del módulo. Sobre el laboratorio, con su
`settings.json` del módulo 04, una petición trivial y la salida de error
apartada: el JSON de resultado trae **veintiséis campos de primer nivel**, y esto
dicen los que importan.  ‹v2.1.252›

```text
is_error: false · subtype: "success" · permission_denials: [] · exit 0
```

Y esto es lo que salió, en la misma ejecución, por la salida de error:

```text
Ignoring 3 permissions.allow entries from .claude/settings.json: this
workspace has not been trusted. Run Claude Code interactively here once
and accept the trust dialog, or set
projects["/ruta/del/proyecto"].hasTrustDialogAccepted: true in
/root/.claude.json.
```

Cinco repeticiones, siempre igual. Tres de tus reglas de permisos se han caído al
suelo y **ninguno de los veintiséis campos lo menciona**: la ejecución se declara
exitosa y el proceso sale con cero.

> Un `2>/dev/null` puesto para que los logs de la CI queden limpios borra el
> único aviso que existe. **No lo pierde: lo borra**, y no queda constancia de
> que hubo uno.

El módulo 09 midió esto mismo contra la 2.1.247. Quince versiones de parche
después sigue igual, lo cual, en un libro donde una medición del módulo 10 caducó
en diecinueve días, merece decirse: **no es un fallo transitorio, es la forma de
la herramienta.**

Y no está escondido: la documentación lo recoge como `Workspace has not been
trusted`, y el diseño es correcto, porque una lista blanca del repositorio sería
concederse permisos a sí mismo. Lo que hay que saber es **por dónde te lo
cuenta**.

### 11.2.4 · El hook que no veta, y no lo dice

El caso peor del apartado anterior. Un hook de `PreToolUse` de tres líneas
colgado de las lecturas, sobre una copia del laboratorio, dos repeticiones por
fila, cambiando **una sola cosa**.  ‹v2.1.252›

| El hook sale con | ¿Bloquea la lectura? | `permission_denials` | `is_error` | Código de salida |
|---|---|---|---|---:|
| `exit 1` y un mensaje en la salida de error | **No** | `[]` | `false` | 0 |
| `exit 2` y el mismo mensaje | **Sí** | una entrada, con herramienta y ruta | `false` | 0 |

La fila de arriba es la que arruina la tarde. El hook **se ejecutó**, falló, y su
fallo no impidió nada ni apareció en ningún sitio que un script lea. Hay una sola
manera de ver el evento:

```bash
claude -p "..." --output-format stream-json --verbose --include-hook-events \
  | grep '"subtype":"hook_response"'
```

Ahí sale entero: `exit_code: 1`, `outcome: "error"` y el `stderr` del hook.

> **Tu veto puede llevar seis semanas sin vetar.** Un `chmod` perdido en un
> despliegue, un intérprete que no está en el PATH del runner, una ruta que
> cambió: el hook falla, sale con 1, y todo lo demás sigue diciendo que va bien.
> Los hooks del módulo 05 son la pieza que no negocia, y **una pieza que no
> negocia también se rompe.**

La fila de abajo se ve desde dos sitios: `permission_denials` trae una entrada, y
el modelo lo cuenta nombrando el archivo del hook. **Un veto que funciona deja
rastro por diseño; uno roto, ninguno.** Y el detalle que decide la comprobación:
**el código de salida es 0 en las dos filas**, así que el campo que sirve es
`permission_denials`.

### 11.2.5 · `--debug` no depura, y el pendiente del módulo 10

El consejo universal es "arráncalo con `--debug`". Sobre el laboratorio, en modo
no interactivo, dos repeticiones, en texto y con `--output-format json`:
 ‹v2.1.252›

| Bandera | Líneas de depuración |
|---|---:|
| `--debug` | **0** |
| `--debug-file /tmp/x.log` | **211** |

Cero: ni por la salida de datos ni por la de error. Con `--debug-file`, las
mismas doscientas once líneas las dos veces: **205 `[DEBUG]`, 3 `[INFO]`, 2
`[ERROR]` y 1 `[WARN]`**. Ninguna de esas tres últimas sale por otro canal.

Y con eso se cierra lo que el módulo 10 dejó abierto ayer, cuando seis intentos
de ver un evento de telemetría con el exportador de consola no dieron ninguno.
La respuesta estaba en ese archivo:  ‹v2.1.252›

| `OTEL_LOGS_EXPORTER` | Tipos reconocidos | Exportadores creados | Eventos |
|---|---|---:|---|
| `console` | `[]` | **0** | `Event dropped (no event logger initialized)` |
| `otlp` | `["otlp"]` | **1** | ninguno tirado |

La telemetría **no estaba rota**: el propio registro dice
`isTelemetryEnabled=true`. El valor `console` **no entra en la lista de tipos**,
se crean cero exportadores, y cada evento se tira con un `[WARN]` que no llega a
ninguna parte.

> Un aviso perfectamente escrito, emitido en el momento exacto, con el nombre del
> evento que se pierde, **enviado a un canal que por defecto no existe**. Es el
> `except:` de Rubén con mejor educación.

Si tu panel de observabilidad tiene cero filas y usas el exportador de consola,
no busques en el panel. Y la consecuencia de gobierno, que ya estaba en el módulo
10 y hoy tiene prueba: **un control cuya evidencia no has visto llegar no es un
control.**

---

## 11.3 · Receta

### 11.3.1 · Individual: los tres pasos, y el segundo es el que se salta todo el mundo

Antes de abrir ningún catálogo. Cuesta dos minutos y descarta la mitad de los
casos.

**Paso 1. La versión, y anotada.** `claude --version`. Media docena de
comportamientos de este libro cambian con la versión, y comparar dos máquinas sin
mirar las suyas no compara nada. Para la instalación, `claude doctor`, **leyendo
la salida y no el código**.

**Paso 2. Modo mínimo.**

```bash
claude --safe-mode
```

Apaga `CLAUDE.md`, skills, plugins, hooks, servidores MCP y comandos, y deja la
autenticación y los permisos como estaban. Sobre el laboratorio, dos veces por
fila:  ‹v2.1.252›

| | Tokens de entrada |
|---|---:|
| Sin banderas | 41.292 |
| Con `--safe-mode` | 37.103 |
| **Lo que pesa la configuración del proyecto** | **4.189** |

El módulo 09 midió 4.065 con el mismo método contra la 2.1.247. Ciento
veinticuatro tokens de diferencia sobre cuatro mil en cinco versiones: el
impuesto de contexto es estable, y por eso se puede presupuestar.

Un aviso que ahorra una confusión: **el modo seguro no silencia el aviso de
confianza del espacio de trabajo**, porque no toca los permisos. Si lo usas
esperando una salida limpia, creerás que no ha hecho efecto.

**Paso 3. Decidir de quién es el problema.** Si en modo mínimo **desaparece**, es
tuyo, y está en una de esas seis piezas: reintrodúcelas de una en una. Si
**sigue**, es del CLI y merece reportarse.

Cuando sospeches de tu configuración de usuario y no solo de la del proyecto, el
escalón siguiente es una configuración limpia de verdad:

```bash
cd /tmp && CLAUDE_CONFIG_DIR=/tmp/claude-limpio claude
```

Sin ajustes de usuario, hooks, servidores ni memoria. **Que aparezcan las
pantallas de primer arranque confirma que está en efecto.**

### 11.3.2 · Cómo se lee un fallo que alguien se tragó

Cuando los tres pasos no bastan, el orden es siempre el mismo.

1. **Aparta la salida de error.** `2>errores.txt`, nunca `2>/dev/null`. Ahí viven
   los avisos que no están en el JSON.
2. **Enciende el archivo de depuración**, no la bandera:
   `--debug-file /tmp/claude.log`, y después `grep -E '\[(ERROR|WARN)\]'`. En una
   ejecución trivial son tres líneas de doscientas once.
3. **Si hay hooks**, `--output-format stream-json --verbose
   --include-hook-events`, buscando `outcome: "error"`.
4. **Solo entonces** el catálogo, con el mensaje literal entre comillas.

### 11.3.3 · Equipo: los tres canales que hay que conectar

Un procedimiento individual no sobrevive a un equipo; una comprobación que corre
sola, sí. Ninguna de estas cuesta una llamada al modelo.

| Qué se vigila | Cómo | Qué caza |
|---|---|---|
| La salida de error, no vacía | `2>errores.txt` y fallar si tiene contenido | Permisos ignorados, avisos de configuración |
| `permission_denials` | Leerlo del JSON y fallar si no está vacío cuando no debería | Un hook que veta lo que no toca, o uno que dejó de vetar |
| `[ERROR]` y `[WARN]` en el archivo de depuración | `--debug-file` y un `grep` | Credenciales, exportadores, servidores que no cargaron |

El módulo 09 ya puso un cuarto: fallar si `mcp_server_errors` o `plugin_errors`
del evento de inicio no vienen vacíos. Los cuatro son la política entera y caben
en una frase: **si un canal habla, alguien lo lee.**

Lo que ninguno puede vigilar es el código de salida, porque no dice lo que
parece:  ‹v2.1.252›

| Situación | Código | Qué hay que leer de verdad |
|---|---:|---|
| `claude doctor` con tres avisos | **0** | La salida. Termina en `3 warnings found` |
| Herramienta bloqueada por un hook | **0** | `permission_denials` |
| Bandera desconocida | 1 | La salida de error. **No hay JSON**, ni siquiera vacío |

La primera es la trampa de equipo: un paso que corre `claude doctor` y mira el
código da por sana una instalación que acaba de nombrar tres problemas. La
tercera es la de script: `--output-format json` no garantiza que haya JSON, y el
`json.load()` revienta con un error que es el tuyo.

### 11.3.4 · Qué reportar, y por qué se rechaza un reporte

Cuando el problema sobrevive al paso 3, cuatro datos hacen accionable un reporte:
**la versión exacta**; **el mensaje literal** y no una paráfrasis, porque el
catálogo está indexado así; **que reproduce en configuración limpia**, que
descarta tu entorno; y **el proveedor y el plan**, porque medio comportamiento
depende de eso.

Y el aviso del módulo 10, aquí más urgente que en ningún otro sitio: **una
transcripción enviada con `/feedback`, `/bug` o `/share` se retiene cinco años**,
y si tu clave de producción está en el código que el agente ha leído, sube con
ella.

---

## 11.4 · Laboratorio · Perseguir el error que el `except:` se traga

El fallo número 5 del inventario, y el peor de los catorce no por hacer más daño,
sino porque **es el único que no produce síntoma**.

**Paso 1. Ponle el síntoma, no el archivo.** Sobre `gestor-pedidos`, con
herramientas de solo lectura, sin nombrar `app.py`:

```bash
claude -p "Los avisos por correo de los pedidos no llegan y en los registros no aparece ningun error. Por que? Responde en menos de 120 palabras." \
  --allowedTools "Read,Glob,Grep" --output-format json
```

Dos de dos encuentra **las dos causas**: que `enviar_email()` está vacía desde
2020, y que aunque enviara algo y fallara, el `except:` de `procesar_pedido()` se
lo tragaría sin registrar nada. **Guarda esa respuesta.** Es justo lo que hace
peligroso el fallo: el agente lee el código en segundos, pero **hasta que alguien
no formula la pregunta, nada le lleva a ese archivo.** El coste no está en
encontrarlo, está en los seis meses que nadie preguntó.

**Paso 2. Demuéstralo, que es distinto de leerlo.** Fuera del repositorio, un
script que sustituya `enviar_email` por una función que revienta:

```python
def email_que_revienta(destino, pedido_id, total):
    raise ConnectionRefusedError("smtp.carnicas.local:25 rechaza la conexión")
aplicacion.enviar_email = email_que_revienta
logging.basicConfig(level=logging.DEBUG)
```

Dos de dos:

```text
CODIGO HTTP: 200
CUERPO: {'id': 1, 'total': 24.2}
PEDIDOS EN BD: 1
```

Doscientos. Pedido guardado. Cobro lanzado. Y **cero líneas de registro con el
nivel en `DEBUG`**. La excepción no se degradó: desapareció.

**Paso 3. Mira qué más se está tragando.** Un `except:` desnudo no es un
`except Exception:` con menos letras:

| Excepción | `except:` | `except Exception:` |
|---|---|---|
| `ConnectionRefusedError` | tragada | tragada |
| `MemoryError` | tragada | tragada |
| `KeyboardInterrupt` | **tragada** | escapa |
| `SystemExit` | **tragada** | escapa |
| `GeneratorExit` | **tragada** | escapa |

Dentro de ese bloque, **`Ctrl+C` no hace nada** y un apagado ordenado tampoco.
Convence a quien no se dejaba convencer por el argumento del registro.

**Paso 4. Escribe la prueba antes que el arreglo.** Dos, en
`tests/test_diagnostico.py`. La primera fija la decisión de 2019, que un aviso
fallido **no** tumbe el pedido, y pasa también contra el código viejo. La segunda
es la nueva:

```python
assert caplog.records, "el fallo del aviso no dejó ninguna entrada en el registro"
entrada = caplog.records[-1]
assert entrada.levelno == logging.ERROR
assert entrada.exc_info is not None, "la entrada no lleva la traza"
```

Comprobar `exc_info` y no solo el texto no es celo: es lo que distingue
`log.exception()` de un `log.error()` que dice que algo falló sin decir dónde.
Contra el `except:` desnudo esa prueba falla en la primera aserción, con la lista
vacía. **Compruébalo antes de arreglar nada**, o no sabrás si la prueba prueba
algo.

**Paso 5. Arregla, conservando la decisión.** El `except:` pasa a
`except Exception:` con un `log.exception()` dentro, y arriba un `basicConfig`
con el nivel en una variable de entorno. Lo que **no** cambia: el pedido sigue
adelante. La decisión de 2019 era razonable; que no se enterara nadie, no.

**Paso 6. Corre las once.** Nueve de caracterización del módulo 09 y las dos
nuevas: `11 passed`, y las nueve viejas **sin tocarlas**. Si alguna cambia, has
cambiado comportamiento, y eso es el módulo 12.

**Paso 7. Ahora el otro `except:`, el de tu herramienta.** Cuelga un hook de tres
líneas de `PreToolUse` sobre las lecturas, **en una copia del laboratorio**, que
salga con 1 y escriba en la salida de error. Pídele que lea `app.py`. La lee, y
el JSON dice `success`. Cambia el 1 por un 2 y repite: se bloquea, y
`permission_denials` trae una entrada. **La diferencia es un dígito, y decide si
te enteras.**

**Paso 8. Mira tu archivo de depuración.** Una ejecución trivial con
`--debug-file` y un `grep -E '\[(ERROR|WARN)\]'` encima. Tres líneas de
doscientas once. Si alguna te sorprende, acabas de encontrar algo que llevaba
meses ahí.

**Paso 9. Escribe el porqué.** `DIAGNOSTICO.md`, al lado de `PERMISOS.md`,
`HOOKS.md`, `MCP.md`, `SKILLS.md`, `AGENTES.md`, `CI.md` y `SEGURIDAD.md`: qué
registra este repositorio, cómo se sube el nivel, y **qué sigue sin dejar
rastro**. Esa última sección es la mitad útil del archivo, y la del laboratorio
dice que `cobrar()` y `enviar_email()` siguen vacías desde 2020: **un aviso que
nunca se manda no produce ningún error, porque no hay error.**

---

## 11.5 · Prueba

**PASA** si se cumplen las cuatro:

1. El `except:` desnudo **ya no existe**, y tienes guardada la ejecución que
   demuestra que antes devolvía **200 sin una sola línea de registro**. Sin esa
   captura has arreglado algo sin saber qué.
2. La prueba de diagnóstico **falla contra el código viejo y pasa contra el
   nuevo**, comprobado en ese orden, y mira `exc_info`, no solo el texto.
3. Sabes decir **por qué canal** te habría llegado cada uno de estos tres avisos:
   los permisos ignorados, un hook que falla con código 1 y un exportador de
   telemetría descartado. Tres canales distintos, y ninguno es el JSON.
4. Las nueve pruebas de caracterización del módulo 09 **siguen pasando sin
   tocarlas**.

**FALLA** si tu procedimiento incluye "relanzarlo": los reintentos ya se
hicieron, hasta diez, antes de que vieras el mensaje. También **FALLA** si un
script tuyo decide con el código de salida de `claude doctor`, que sale con **0
con tres avisos delante**, o si redirige la salida de error a `/dev/null` en
cualquier punto de la cadena.

> **Esto va a cambiar.** El catálogo de errores creció un 28 % en veinte días y
> va a seguir. Lo que `--debug` hace o deja de hacer en modo no interactivo puede
> arreglarse mañana, y sería una buena noticia. El reparto entre las dos salidas
> es más estable, y aun así se mide, no se supone. Lo que esperamos que aguante
> es el criterio: **antes de explicar un fallo, comprueba que estás mirando el
> canal donde se cuenta.** Un sistema que no se queja casi nunca está sano.

---

## 11.6 · Coste de este módulo

Las quince ejecuciones de las que se conservó el JSON:

| Concepto | Cantidad |
|---|---:|
| Tokens de entrada | 947.086 |
| De ellos, servidos desde caché | 845.049 (**89,2 %**) |
| Tokens de salida | **2.025** |
| **Relación entrada / salida** | **467,7 a 1** |
| Coste, sumando lo que devolvió el CLI | 0,61 $ |
| Coste en euros | por debajo de 0,70 € |
| Invocaciones totales del CLI | 31 |
| Tiempo | 45 minutos |

Esa relación es la cifra del módulo, y no se parece a ninguna anterior:

| Actividad | Entrada por token de salida |
|---|---:|
| Operación multiagente de cuatro meses, `D4-factura/` | 24 a 1 |
| Auditoría de seguridad, módulo 10 | 90 a 1 |
| **Diagnóstico, este módulo** | **468 a 1** |

**Diagnosticar es la actividad más desequilibrada del libro**, y tiene sentido en
cuanto se mira lo que se hace: releer la configuración entera, una vez por
comprobación, para obtener dos palabras o un número.

De ahí la recomendación de presupuesto, contraria a la intuición: **cuando estés
diagnosticando, apaga lo que puedas apagar.** No por dinero, que son céntimos,
sino porque `--safe-mode` quita **4.189 tokens** que compiten por la atención del
modelo mientras intentas aislar una variable.

Y otra vez, una medición suelta no es un dato: la misma pregunta del paso 1, dos
veces seguidas y sin cambiar nada, costó **0,205 $** y **0,037 $**. Lo único que
cambió fue la temperatura de la caché.

El coste que no está en la tabla es el que el módulo intenta evitar: **la tarde
buscando algo que arreglar**, la partida más cara del libro y la única que no
aparece en ninguna factura, porque se paga en sueldo. Los tres canales de 11.3.3
cuestan cero por turno, como el `deny` del 04 y los hooks del 05.

Queda pendiente lo de siempre, hoy con nombre nuevo. El registro captura fallos,
y **`cobrar()` y `enviar_email()` no fallan: no hacen nada**. Ningún registro
encuentra un trabajo que nadie intentó hacer. Eso, y desmontar la función de ocho
responsabilidades donde vive, es el módulo 12.

---

## Runbook · Módulo 11

> **Los tres pasos, antes de nada**
> 1. `claude --version`, anotada. `claude doctor` **leyendo la salida**: sale con
>    **0 aunque encuentre avisos**.
> 2. `claude --safe-mode`. Apaga `CLAUDE.md`, skills, plugins, hooks, MCP y
>    comandos; deja autenticación y permisos. Quita **4.189 tokens**. **No
>    silencia el aviso de confianza.**
> 3. ¿Desaparece? Es tuyo, en una de esas seis piezas. ¿Sigue? Es del CLI.
> Si sospechas de tus ajustes de usuario:
> `cd /tmp && CLAUDE_CONFIG_DIR=/tmp/claude-limpio claude`.
>
> **"Va todo bien y no va bien"**
> Los canales, en este orden. Ninguno es el JSON:
> 1. **Salida de error.** `2>errores.txt`, nunca `2>/dev/null`.
> 2. **Archivo de depuración.** `--debug-file /tmp/claude.log` y
>    `grep -E '\[(ERROR|WARN)\]'`. **`--debug` a secas no imprime nada en modo no
>    interactivo:** 0 líneas frente a 211.
> 3. **Eventos de hook.** `--output-format stream-json --verbose
>    --include-hook-events`, buscando `outcome: "error"`.
>
> **"Mis permisos no se aplican y nadie avisó"**
> Con `-p` no hay diálogo de confianza: las entradas de `permissions.allow` del
> proyecto **se ignoran**, `deny` y `ask` no. El aviso sale **solo por la salida
> de error**, y no está en ninguno de los 26 campos del JSON. Acepta el diálogo
> una vez, o pon `hasTrustDialogAccepted` con la clave `projects` del mensaje.
>
> **"Mi hook de veto no veta"**
> `exit 1` **no bloquea** y no deja rastro: `permission_denials` vacío,
> `is_error: false`, salida 0. `exit 2` bloquea y aparece en
> `permission_denials`. El código del proceso es **0 en los dos casos**: vigila
> el campo, no el código.
>
> **"El panel de telemetría tiene cero filas"**
> `OTEL_LOGS_EXPORTER=console` se descarta sin error: tipos `[]`, **0
> exportadores**, y cada evento se tira con un `[WARN]` que solo aparece en
> `--debug-file`. Con `otlp` se crea 1. Y `OTEL_LOG_TOOL_DETAILS=1`, o el nombre
> de la herramienta MCP se queda en `"mcp_tool"`.
>
> **En tu propio código**
> Un `except:` desnudo también se traga **`KeyboardInterrupt`, `SystemExit` y
> `GeneratorExit`**: ahí dentro, `Ctrl+C` no hace nada. `except Exception:` más
> `log.exception()`, y una prueba que compruebe **`exc_info`**, no solo el texto.
>
> **"Vuelvo a lanzarlo a ver si pilla"**
> Ya se reintentó **hasta diez veces con retroceso exponencial**. Excepción: los
> fallos de certificado TLS **no se reintentan a propósito** y son de tu proxy.
>
> **"No encuentro mi error"**
> El catálogo se indexa por **mensaje literal**: cópialo con comillas y nombres
> de archivo. **106 entradas en 15 categorías** el 1-sep-2026, frente a 83 el
> 12-ago. La más poblada, **autenticación**, con 20.
>
> **Un script que llama al CLI**
> Una bandera desconocida sale con 1 y **no imprime JSON**, ni vacío: envuelve el
> `json.load()`. Después `is_error`, que exista `result`, y `permission_denials`.
