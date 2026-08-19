# Módulo 04 · Permisos y sandbox

> **Laboratorio de este módulo:** ~35 minutos · unos **745.000 tokens de
> entrada** y 3.000 de salida · **0,47 dólares** según la telemetría del propio
> CLI, que a cualquier cambio euro-dólar de agosto de 2026 se queda **por debajo
> de 0,55 €**. Con un plan de suscripción va incluido.
> **Verificado contra:** Claude Code 2.1.235 · 19 de agosto de 2026.

> **Nota de versión.** Cada módulo de este libro declara la versión del CLI con
> la que se midió, y esta es la 2.1.235: siete días después de la 2.1.228 del
> módulo 01. Las cifras de más abajo son de esa versión y de esa máquina.

---

## 4.1 · Síntoma

Empezaste con cuidado y contestabas a todo. A los tres días te habías aprendido
la postura del dedo sobre la tecla y aprobabas sin leer, que es exactamente lo
contrario de revisar. Así que un martes le diste la bandera peligrosa, funcionó
de maravilla, y te quedaste con una inquietud de fondo que no sabes nombrar.

Entre esos dos sitios hay un modelo de permisos entero, y la razón de que nadie
lo use es que parece un formulario. No lo es: son tres capas que la gente
confunde entre sí. Y la mitad de las veces que alguien dice "los permisos no me
funcionan", lo que pasa es que escribió la regla correcta en el archivo
equivocado y nadie se lo dijo. Esa frase es literal, y este módulo la mide.

---

## 4.2 · Modelo mental

### 4.2.1 · Tres capas, y no hacen lo mismo

| Capa | Qué decide | Cuándo actúa | Quién la aplica |
|---|---|---|---|
| **Modo** | Si te pregunta antes de actuar | Antes de la llamada | El programa |
| **Reglas** | Qué herramientas y qué rutas | Antes de la llamada | El programa |
| **Sandbox** | Qué alcanza el comando **ya lanzado** | Durante la ejecución | El sistema operativo |

La diferencia que importa está en la tercera columna. El modo y las reglas
deciden **antes**, mirando la cadena del comando; el sandbox decide **después**,
sobre el proceso vivo. Por eso el sandbox aguanta cuando un comando permitido
hace más de lo que su nombre sugiere, y las reglas no.

### 4.2.2 · Los seis modos, y por qué su nombre depende de dónde lo escribas

| Modo | Qué corre sin preguntar | Para qué |
|---|---|---|
| `default`, etiquetado **Manual** | Solo lecturas | Trabajo sensible, código ajeno |
| `acceptEdits` | Lecturas, ediciones y `mkdir`, `touch`, `mv`, `cp`, `rm`, `sed` dentro del directorio | Iterar sobre código que estás revisando |
| `plan` | Lecturas, más lo que apruebe el clasificador | Explorar antes de tocar |
| `auto` | Todo, con un clasificador revisando | Tareas largas |
| `dontAsk` | Solo lo pre-aprobado. Lo demás se deniega sin esperar | Integración continua |
| `bypassPermissions` | Todo | Solo entornos desechables |

Son seis y el que se olvida siempre es el primero, porque tiene dos nombres:
**Manual** en la interfaz y `default` en la configuración, con `manual` aceptado
como alias.  ‹v2.1.200›

Hay un detalle que solo se ve provocándolo, y lo hemos provocado: meter un valor
inválido en los dos sitios. Con la bandera, `claude --permission-mode zzz`:

```
Allowed choices are acceptEdits, auto, bypassPermissions, manual, dontAsk, plan.
```

Y en `permissions.defaultMode` de un `settings.json`, leído con `claude doctor`:

```
Expected one of: "acceptEdits", "auto", "bypassPermissions", "default", "dontAsk", "plan"
```

**Las dos listas tienen seis entradas y no son la misma lista.** La bandera
nombra `manual`; el esquema nombra `default`. Comprobado en la 2.1.235: los dos
sitios aceptan las dos palabras, pero cada mensaje enseña solo una.

Tres cosas más sobre en qué modo arranca una sesión, y las tres muerden: en Pro,
Max y Team el modo de arranque por defecto es **auto** ‹v2.1.228›; **`claude -p`
arranca siempre en `default`**, sea cual sea tu plan, que es la razón número uno
de que un script funcione a mano y no en la tubería; y un `"defaultMode": "auto"`
en el `settings.json` del **proyecto** no tiene efecto, hay que ponerlo en el de
usuario.

### 4.2.3 · Las reglas: deny, luego ask, luego allow

Tres listas, y se evalúan **en ese orden**. El primer acierto manda y la
especificidad no cambia nada: un `deny Bash(aws *)` gana a un
`allow Bash(aws s3 ls)`, así que **una regla de denegación no admite
excepciones**.

Lo mismo entre ámbitos: las reglas de todos los archivos se **fusionan**, y un
`deny` de cualquier nivel bloquea un `allow` de cualquier otro. Esa asimetría es
la propiedad más valiosa del sistema, y es la razón de que la protección de
secretos se ponga en el proyecto y se confirme en git: nadie la levanta desde su
configuración personal.

Cuatro reglas de sintaxis que ahorran una tarde:

- **`Read(x)` denegado también bloquea editar** esa ruta ‹v2.1.208› **y crear un
  archivo nuevo ahí** ‹v2.1.228›. `NotebookEdit` no entra: para eso, `Edit`.
- **Solo se consultan reglas de ruta escritas sobre `Read` y `Edit`.** Un
  `Write(docs/**)` se acepta, no se consulta nunca y avisa al arrancar. ‹v2.1.210›
- Un nombre de herramienta **pelado** en `deny`, como `Bash`, no bloquea la
  herramienta: **la quita del contexto** y el agente no la ve. Con paréntesis,
  `Bash(rm *)`, la herramienta sigue ahí y se bloquean las llamadas que casen.
- En un `allow`, `Edit(src/**)` es solo `<directorio>/src`; en un `deny` o un
  `ask`, caza cualquier `src` a cualquier profundidad. Denegar es más ancho que
  permitir, a propósito.

### 4.2.4 · La puerta que decide si tus permisos existen

Las reglas `allow` **conceden capacidad**, así que Claude Code no las aplica
hasta que aceptas el **diálogo de confianza del espacio de trabajo** para esa
carpeta. Las de `deny` y `ask` solo restringen, así que se aplican siempre. Y el
diálogo solo aparece en sesiones interactivas: `claude -p` no lo enseña nunca.

Consecuencia: **en un clon recién hecho y en cualquier ejecución no interactiva,
las reglas `allow` de tu repositorio no se están aplicando.** Ese es el estado
de toda tubería de integración continua del mundo.

Lo medimos con la misma petición, el mismo repositorio y una sola variable
cambiando. Petición: crear un archivo vacío con `touch`. Regla:
`Bash(touch *)`. Dos repeticiones por fila.  ‹v2.1.235›

| Dónde vive el permiso | ¿Se creó el archivo? | Tokens de entrada | Turnos |
|---|---|---:|---:|
| `permissions.allow` de `.claude/settings.json`, sin confianza | **No** | 131.788 y 131.806 | 3 |
| Bandera `--allowedTools "Bash(touch *)"` | Sí | 87.452 | 2 |
| El mismo `.claude/settings.json`, con la confianza aceptada | Sí | 87.456 | 2 |

Tres lecturas.

**La regla no estaba mal escrita.** Es la misma cadena en los tres casos: cambia
de dónde se lee y si esa carpeta está aceptada.

**El aviso existe y no lo vas a ver.** Sale por la salida de error, así que
cualquier tubería que capture solo la estándar lo tira a la basura:

```
Ignoring 1 permissions.allow entry from .claude/settings.json: this workspace
has not been trusted. Run Claude Code interactively here once and accept the
trust dialog, or set projects["/ruta/al/repo"].hasTrustDialogAccepted: true in
/root/.claude.json.
```

**Un permiso que no se aplica cuesta más que uno que sí.** 131.800 tokens frente
a 87.450, un **51 % más**, y un turno extra: el agente intenta, se lo bloquean y
vuelve a intentar. La configuración rota no es neutra, se paga.

Un matiz: la confianza se guarda en la **raíz del repositorio de git**, no en la
carpeta desde la que arrancas, así que aceptarla una vez cubre el repositorio
entero. Y tu `.claude/settings.local.json` pasa a contar como del repositorio en
cuanto lo confirmas en git.  ‹v2.1.207›

### 4.2.5 · Lo que una regla no puede proteger

Segunda medición, y es la que empuja al sandbox. Con
`deny Read(./secretos/**)` puesto y funcionando, dos comandos, dos
repeticiones cada uno:

| Comando pedido | Resultado |
|---|---|
| `cat secretos/pasarela.env` | **Bloqueado.** "El usuario denegó el permiso" |
| `python3 -c "print(open('secretos/pasarela.env').read())"` | **Imprimió la clave entera** |

No es un fallo: está documentado. Las reglas `Read` y `Edit` cubren las
herramientas de archivo y los comandos de lectura que Claude Code **reconoce**
en Bash, como `cat`, `head`, `tail` y `sed`. Claude Code consulta una lista de
comandos conocidos; no interpreta lo que hace un intérprete.

De ahí las dos frases que hay que llevarse:

**Una regla de permisos protege rutas, no valores.** La clave de la pasarela del
laboratorio vive dentro de `app.py`. No hay regla que la proteja sin dejar ciego
al agente sobre su propia aplicación: la única solución es sacarla del código.

**Para un límite que aguante a un subproceso hace falta el sistema operativo.**
Eso es el sandbox, y por eso está en este módulo y no en otro.

### 4.2.6 · El sandbox, en una página

El sandbox del Bash tiene dos capas independientes. **Sistema de archivos**: se
escribe solo en el directorio de trabajo y en el temporal de la sesión, y se lee
casi todo, así que **la lectura de `~/.aws/credentials` y `~/.ssh` sigue
permitida por defecto** y hay que cerrarla con `sandbox.credentials`.  ‹v2.1.187›
**Red**: no hay dominios permitidos de partida y la primera vez que hace falta
uno se pregunta; `strictAllowlist` deniega en vez de preguntar, y **puesto en el
`settings.json` del repositorio no hace nada**.  ‹v2.1.219›

Dentro de las rutas escribibles, el sandbox **sigue denegando** las escrituras
sobre lo que Claude Code carga como configuración o código: `.claude/`,
`.mcp.json`, los archivos de arranque de la shell, `hooks` y `config` de `.git`.
No hay forma de eximir ninguna: un comando que pudiera escribir ahí se ampliaría
los permisos a sí mismo para la próxima vez.

Y la pieza que casi nadie sabe que existe: **enmascarar** una credencial en vez
de denegarla. Un `deny` sobre `GITHUB_TOKEN` la borra y con ella rompe `gh`. Con
`"mode": "mask"`, el comando ve un centinela y el proxy sustituye el valor real
al salir hacia los hosts que listes: el comando y sus registros nunca tienen la
credencial, y sus peticiones sí autentican.  ‹v2.1.199› Necesita
`network.tlsTerminate`; sin eso **falla sin exponer nada**.

> **Esto va a cambiar.** El sandbox no corre en Windows nativo y en Linux
> necesita `bubblewrap` y `socat`, que la máquina donde se ha escrito este módulo
> no tiene: **esta sección no está medida por nosotros.** Sale de la
> documentación del 19 de agosto de 2026 y del esquema del binario, comprobado
> por la vía del módulo 02: metiendo tipos equivocados a propósito, las ocho
> claves de `sandbox.*` que cita esta sección validan en la 2.1.235.

### 4.2.7 · Auto mode: un segundo modelo mirando

En auto mode no contestas tú: contesta un clasificador, otro modelo que ve tus
mensajes, las llamadas a herramientas y tu `CLAUDE.md`, y **no ve los resultados
de las herramientas**, precisamente para que un archivo hostil no lo manipule.

Cuántas reglas trae de fábrica no hay que estimarlo: `claude auto-mode defaults`
las imprime. En la 2.1.235, en esta máquina, **17 de `allow`, 66 de `soft_deny`,
1 de `hard_deny` y 20 entradas de `environment`, 63.477 bytes de JSON.** La misma
orden en la 2.1.234, seis días antes, daba los mismos recuentos y 62.957 bytes:
los recuentos aguantan entre versiones, el texto se mueve.

La precedencia dentro del clasificador tiene cuatro escalones: `hard_deny`
bloquea sin condiciones; `soft_deny` bloquea después; `allow` levanta los
`soft_deny` que casen; y **la intención explícita tuya levanta el resto**. La
frase que define "explícita" es la mejor de toda la documentación:

> Pedirle que "limpie el repositorio" **no** autoriza un force push. Pedirle que
> "haz force push de esta rama" **sí**.

Tres avisos operativos:

- El bloque `autoMode` **se ignora a propósito** desde el `settings.json` del
  proyecto y desde el local, para que un repositorio clonado no pueda
  relajarte el clasificador.  ‹v2.1.207›
- Si escribes cualquiera de las cuatro listas **sin incluir la cadena
  `"$defaults"`**, sustituyes la lista entera. Un `soft_deny` propio de dos
  líneas te deja sin las 66 de fábrica.
- Una regla `allow` estrecha tuya, como `Bash(npm test)`, se resuelve **antes**
  de que el clasificador la vea. Para que lo vea todo: `classifyAllShell`.  ‹v2.1.193›

Y el punto de control humano que sí aguanta en auto mode: un `ask` acotado por
contenido, como `Bash(git push *)`, se evalúa antes que el clasificador y
siempre pregunta.

---

## 4.3 · Receta

### 4.3.1 · Los tres perfiles, y qué se rompe al cambiar

Están listos en `entregables/plantillas/permisos/`.

| Perfil | Modo | Lo que lo define | Para |
|---|---|---|---|
| **Cauto** | `default` | `deny` de secretos y de red, `ask` en `git push` y `git commit` | Código que no conoces, trabajo sensible |
| **Normal** | `acceptEdits` | El mismo `deny`, `ask` solo en `git push`, `allow` para tests, sandbox con lista blanca de dominios | Todos los días |
| **Laboratorio** | `bypassPermissions` | Sandbox obligatorio con `failIfUnavailable`, sin escotilla (`allowUnsandboxedCommands` en `false`), credenciales denegadas | **Solo dentro de un contenedor** |

Qué se rompe al pasar de cauto a normal, medido con la misma petición de edición
sobre el laboratorio, dos repeticiones:  ‹v2.1.235›

| Perfil | ¿Aplicó la edición? | Tokens | Turnos |
|---|---|---:|---:|
| Cauto (`default`) | **No.** "Necesito permiso para editar" | 131.947 y 131.881 | 3 |
| Normal (`acceptEdits`) | Sí | 132.465 y 132.035 | 3 |

**Cuestan casi lo mismo.** La diferencia entre los dos perfiles no es el gasto:
es que uno hace el trabajo y el otro se queda esperando a alguien que en una
tubería no existe.

### 4.3.2 · Equipo: qué clave se honra desde dónde

La tabla que evita la mitad de las discusiones. "Proyecto" es el
`.claude/settings.json` del repositorio.

| Clave | ¿Se honra desde el proyecto? |
|---|---|
| `permissions.deny` y `permissions.ask` | **Sí, siempre** |
| `permissions.allow` y `additionalDirectories` | Solo tras aceptar la confianza |
| `permissions.defaultMode` | Sí, salvo el valor `auto` |
| `autoMode.*` | **No.** Solo usuario, gestionada o `--settings` |
| `sandbox.network.strictAllowlist` | **No** |
| `sandbox.credentials` con `mode: mask` y `tlsTerminate` | **No** |
| `sandbox.filesystem.disabled` | **No** |
| `sandbox.enabled`, `allowWrite`, `denyRead`, `credentials` con `deny` | Sí |

El patrón es de una sola frase, y una vez que se ve ya no se olvida: **lo que
restringe se acepta desde el repositorio; lo que concede, no.** Un repositorio
clonado puede protegerte más, nunca menos.

Encima está la configuración gestionada por la organización, que gana a todo,
incluida la línea de comandos: ahí viven `allowManagedPermissionRulesOnly` y
`disableBypassPermissionsMode`.

### 4.3.3 · La bandera peligrosa: dónde sí y dónde nunca

`--dangerously-skip-permissions` se salta las comprobaciones, incluidas las
escrituras sobre rutas protegidas. **Nunca en tu máquina de trabajo.** Solo
dentro de un contenedor o una máquina virtual, por una razón concreta: sin
diálogo que te dé un segundo, el límite que queda es el del entorno.

El propio CLI lo defiende. Como root, en la 2.1.235:

```
--dangerously-skip-permissions cannot be used with root/sudo privileges
for security reasons
```

Comprobado. Y la comprobación **se salta sola dentro de un sandbox reconocido**,
que es la razón de que el contenedor de referencia corra como usuario normal.

Dos matices que le quitan el aura de interruptor mágico: **las reglas `deny`
siguen aplicándose** aquí también, y hay acciones que ningún modo aprueba solo,
entre ellas un `rm` contra una ruta crítica.  ‹v2.1.218›

### 4.3.4 · El contenedor de desarrollo con red restringida

La plantilla está en `entregables/plantillas/devcontainer/`. Instalar el CLI en
un contenedor son tres líneas; lo que lo convierte en un límite son otras tres
piezas: **`remoteUser` que no sea root**, o la bandera peligrosa se niega a
arrancar; **`NET_ADMIN` y `NET_RAW`** en `runArgs`, para que el cortafuegos pueda
escribir reglas dentro; y **el script de cortafuegos**, que deniega todo salvo
los dominios que necesitas. Sin el tercero tienes aislamiento de disco y ninguno
de red, que se parece mucho a ninguno.

Y el detalle que se lleva media hora la primera vez: montar un volumen en
`~/.claude` **no** mantiene la sesión iniciada entre reconstrucciones, porque la
cuenta y la confianza por proyecto viven en `~/.claude.json`, fuera de ahí. Hay
que fijar además `CLAUDE_CONFIG_DIR` al mismo destino.

---

## 4.4 · Laboratorio · Permisos versionados en `gestor-pedidos`

Seguimos en el mismo repositorio. Del módulo 03 traes un `CLAUDE.md` que dice la
verdad; hoy pasamos de decirla a imponerla.

**Paso 1. Dale un sitio al secreto.** La clave de la pasarela está dentro de
`app.py`, y ahí no hay regla que valga. Crea el sitio donde debería haber estado
desde 2019:

```bash
mkdir -p secretos
cat > secretos/pasarela.env <<'FIN'
PSP_API_KEY=PSP-LIVE-9f2b41c7a8e3d6104b5f7e29
PSP_ENDPOINT=https://api.pasarela.example/v2
FIN
```

Y un `.gitignore` con `secretos/pasarela.env` dentro. Ojo: `.gitignore` impide el
**accidente**, no el **acceso**.

**Paso 2. Comprueba que ahora mismo se lee.** Sin ninguna regla puesta:

```
Lee el archivo secretos/pasarela.env y dime literalmente qué contiene.
```

Te lo lee entero. En nuestra ejecución, la clave completa en la respuesta.

**Paso 3. Pon la regla.** En `.claude/settings.json` del repositorio, junto a lo
que dejó el módulo 02:

```json
{
  "permissions": {
    "deny": ["Read(./secretos/**)", "Edit(./secretos/**)",
             "Read(./.env)", "Read(./.env.*)"]
  }
}
```

**Paso 4. Repite la pregunta del paso 2, palabra por palabra.** Nuestro
resultado, dos veces:

> No puedo leer ese archivo: el directorio `secretos/` está bloqueado por la
> configuración de permisos de esta sesión (denegado explícitamente, no es un
> fallo del sistema de archivos).

Ese "no es un fallo del sistema de archivos" es el criterio PASA del módulo. Un
límite que se nota se puede depurar; uno que falla en silencio manda a alguien a
buscar un fallo que no existe.

**Paso 5. Encuentra el agujero tú mismo.** Con la regla puesta, añade
`--allowedTools "Bash"` y pide los dos comandos, uno por sesión: primero
`cat secretos/pasarela.env`, luego
`python3 -c "print(open('secretos/pasarela.env').read())"`. El primero se
bloquea. El segundo imprime la clave. Dos veces cada uno, en la 2.1.235. No
sigas hasta haberlo visto con tus ojos: es la mitad del módulo.

**Paso 6. La prueba de la confianza.** Añade un `allow` cualquiera al
`settings.json` del proyecto, por ejemplo `Bash(touch *)`, y pide el archivo
vacío **capturando la salida de error aparte**:

```bash
claude -p "Crea un archivo vacío llamado zz.txt con touch." > salida.txt 2> error.txt
```

Si `error.txt` trae la línea de `this workspace has not been trusted`, acabas de
ver la causa de la mitad de los "los permisos no me funcionan" del mundo.
Repítelo con `--allowedTools "Bash(touch *)"`: la misma regla, por otra puerta,
sí funciona.

**Paso 7. Escribe por qué.** Un JSON no puede explicarse. Crea `PERMISOS.md` con
una línea por regla y su motivo, y con lo que las reglas **no** protegen. El del
laboratorio está en `D6-repo-feo/gestor-pedidos/PERMISOS.md`.

**Paso 8. Mide lo que cuesta.** Repite la medición trivial del módulo 03
(`Responde solo con la palabra OK.`) con el bloque de permisos y sin él. Nosotros
llegamos a 24 reglas `deny` y salió **43.619 tokens las cuatro veces**, al token.
Las reglas no viajan en el contexto.

---

## 4.5 · Prueba

**PASA** si se cumplen las cuatro:

1. Pedirle el contenido de `secretos/pasarela.env` **no lo devuelve**, y la
   respuesta dice que está bloqueado por permisos, no que el archivo no exista.
2. `.claude/settings.json` y `PERMISOS.md` están **añadidos al control de
   versiones**, y `secretos/pasarela.env` **no**.
3. Sabes decir, sin mirar, qué pasa con las reglas `allow` de ese archivo en un
   clon recién hecho, y por dónde sale el aviso.
4. Has visto pasar el `python3` por encima de la regla, y sabes que la respuesta
   a eso no es otra regla.

**FALLA** si tu conclusión es que el repositorio ya está protegido. La clave que
vive dentro de `app.py` sigue leyéndose entera y cualquier subproceso lee lo que
quiera. Lo que has ganado es real y es acotado: un límite determinista sobre las
herramientas de archivo, versionado, y que nadie levanta desde su configuración
personal.

> **Esto va a cambiar.** Lo que el agente contesta al ser bloqueado depende de la
> versión y del modelo. Nuestra ejecución es del 19 de agosto de 2026 con la
> 2.1.235, dos repeticiones por medida. Lo que esperamos que aguante es el
> resultado cualitativo: bloqueado y dicho en el caso de `cat`, no bloqueado en
> el de `python3`. Si el tuyo no coincide, el dato es tuyo y nos interesa.

---

## 4.6 · Coste de este módulo

| Concepto | Cantidad |
|---|---|
| Tokens de entrada del laboratorio | ~745.000 |
| Tokens de salida | ~3.000 |
| Coste medido por el CLI | 0,47 dólares |
| Coste en euros | por debajo de 0,55 € |
| Tiempo | 35 minutos |
| **Impuesto de contexto permanente** | **0 tokens, medido** |
| Mantenimiento continuo | revisar las reglas cuando cambien las rutas |

La fila en negrita es la buena noticia y conviene ponerla al lado de la del 03.
Un `CLAUDE.md` de 67 líneas cuesta 1.311 tokens en **cada turno de cada sesión**;
veinticuatro reglas de permisos cuestan **cero**, porque no viajan en el
contexto. Cuando dudes entre pedirlo por escrito en el archivo de memoria o
imponerlo con una regla, la regla es más barata y además se cumple.

Hay un coste escondido, y ya lo hemos medido: **una regla que no se aplica cuesta
un 51 % más** que la misma regla aplicándose, porque el agente intenta, se lo
bloquean y reintenta. El permiso mal puesto es más caro que no tener ninguno, y
encima te deja creyendo que estás cubierto.

El mantenimiento de verdad no es el JSON: son las rutas. El día que alguien añada
`config/produccion.yaml` con credenciales dentro, tu `deny` de `secretos/**` no
lo cubre y nadie te va a avisar. Por eso el módulo 05 convierte lo que no es
negociable en un hook, que sí puede mirar el contenido.

---

## Runbook · Módulo 04

> **"Mis permisos no se aplican"**
>
> 1. ¿Es una regla `allow`? Sin aceptar el diálogo de confianza no se aplica.
>    Mira la **salida de error**, no la de datos: `2> error.txt`.
> 2. ¿Estás en `claude -p`? El diálogo nunca aparece ahí. Usa `--allowedTools`,
>    o pon `hasTrustDialogAccepted: true` en `~/.claude.json`.
> 3. ¿Es un `deny` que no bloquea? Comprueba la forma de la ruta: `Read(secrets/**)`
>    y `Read(/secrets/**)` no anclan en el mismo sitio.
> 4. ¿La escribiste sobre `Write` o `Glob`? No se consultan. Van sobre `Edit` y `Read`.
> 5. `claude doctor` dentro del repositorio: si hay `Invalid settings`, el
>    archivo entero puede no estar aplicándose.
>
> **Desde el `settings.json` del repositorio**
> **Sí:** `deny`, `ask`, `defaultMode` salvo `auto`, `sandbox.enabled`,
> `allowWrite`, `denyRead`, `credentials` con `mode: deny`.
> **No:** `autoMode.*`, `strictAllowlist`, `mask`, `tlsTerminate`,
> `filesystem.disabled`, y `allow` mientras no aceptes la confianza.
>
> **Orden de evaluación:** `deny` → `ask` → `allow`. Primer acierto.
> Un `deny` ancho **no admite excepciones**. Las reglas se fusionan entre
> ámbitos y un `deny` de cualquier nivel gana a un `allow` de cualquier otro.
>
> **Los seis modos:** `default` (Manual) · `acceptEdits` · `plan` · `auto` ·
> `dontAsk` · `bypassPermissions`.
> `claude -p` arranca siempre en `default`. `"auto"` no se lee del proyecto.
>
> **Los tres perfiles:** cauto (`default`) · normal (`acceptEdits` + sandbox) ·
> laboratorio (`bypassPermissions`, solo en contenedor).
>
> **Lo que una regla NO para**
> Un subproceso: `cat` se bloquea, `python3 -c "open(...)"` no. Para eso, el
> sandbox o un hook. Y un valor dentro del código: las reglas protegen rutas.
>
> **La bandera peligrosa**
> Solo en contenedor o máquina virtual, y como usuario no root, o se niega a
> arrancar. Las reglas `deny` siguen aplicándose incluso ahí. Para quitarla de la
> organización: `permissions.disableBypassPermissionsMode`.
>
> **Cuánto cuesta esto en contexto**
> Cero. Comprobado: 24 reglas `deny`, 43.619 tokens, el mismo número que sin
> ninguna. Compáralo con los 1.311 por turno de un `CLAUDE.md` de 67 líneas.
