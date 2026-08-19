# Módulo 02 · Instalación, autenticación y versiones

> **Laboratorio de este módulo:** ~25 minutos · **0 tokens** · **0,00 €.**
> Es el único laboratorio del libro que no habla con el modelo: todo lo que
> hay que comprobar aquí se comprueba contra el binario y contra tu disco.
> **Verificado contra:** Claude Code 2.1.233 · 17 de agosto de 2026.

> **Nota de versión de este módulo.** Este libro no promete una versión única
> del CLI: cada módulo declara la suya, la del día en que se escribió y se midió.
> El módulo 01 se hizo contra la 2.1.228 el 12 de agosto de 2026; este, cinco
> días después, contra la 2.1.233. Redondear las dos a una sola cifra de portada
> quedaría más limpio y sería mentira, y el módulo que trata precisamente de
> versiones es el peor sitio posible para empezar a mentir. En la sección 2.4
> verás exactamente qué se movió entre esas dos.

---

## 2.1 · Síntoma

Tu compañero pega en el chat del equipo un comando que a ti no te existe. O al
revés: a ti te funciona algo desde hace semanas y él jura que nunca ha visto esa
opción. Nadie miente. Estáis ejecutando programas distintos con el mismo nombre.

La versión suele salir a relucir tarde, cuando ya lleváis media hora mirando
configuraciones. Y cuando por fin sale, aparece la segunda incomodidad: nadie
sabe decir con qué versión se escribió el `CLAUDE.md` del repositorio, ni con
cuál pasó la última vez la tubería de integración continua, ni si la máquina que
ejecuta los trabajos nocturnos se actualiza sola o lleva cuatro meses parada.

En cualquier otro proyecto esto estaría resuelto: fijas la versión de tu
lenguaje, fijas la de tus dependencias y sigues. Aquí no lo has hecho, porque
Claude Code se instaló en un minuto y se actualiza solo, y algo que se actualiza
solo no parece una dependencia. Lo es. Es la que decide si tu configuración se
aplica o se ignora.

---

## 2.2 · Modelo mental

### 2.2.1 · Una instalación nativa es un enlace y una carpeta

La instalación recomendada es la nativa, que no depende de ningún gestor de
paquetes. Merece verse una de verdad, porque explica todo lo demás. Esta es la
máquina donde se ha escrito el libro:

```
~/.local/bin/claude  ->  ~/.local/share/claude/versions/2.1.233
```

El comando que hay en tu `PATH` no es el programa: es un **enlace simbólico**
(symlink) a una versión concreta. Y al lado de esa versión conviven las
anteriores. En esta máquina, ahora mismo, hay tres:

```
2.1.228   12 de agosto
2.1.229   12 de agosto
2.1.233   15 de agosto
```

De ahí salen tres consecuencias que se usan todos los días:

**Actualizar no rompe una sesión abierta.** Se instala la versión nueva al lado y
se mueve el enlace. El proceso que ya está corriendo sigue apuntando a su
binario. Por eso una actualización se aplica "la próxima vez que arranques".

**Puedes ejecutar una versión vieja sin desinstalar nada**, invocándola por su
ruta. Es lo que hace falta para reproducir un fallo que solo aparece en la
máquina de otro, y es la mitad del laboratorio de este módulo.

**Si sustituyes ese lanzador por un script tuyo, el actualizador lo respeta.**
`claude update` y las actualizaciones en segundo plano instalan versiones nuevas
bajo `versions/` y dejan tu lanzador en su sitio, así que es tu script el que
decide qué versión corre. Antes de la 2.1.207 no era así: el actualizador
pisaba el lanzador propio con su enlace en cada actualización.  ‹v2.1.207›

Con un lanzador propio, además, Claude Code **conserva todas las versiones en
disco**, porque no puede saber cuál necesita tu script. Y `claude doctor` avisa
de que ese lanzador no lo puso el instalador.

### 2.2.2 · Lo que cambia entre versiones no son las banderas

Aquí está la parte que nos sorprendió, y que cambia por completo cómo hay que
buscar el problema.

Si el síntoma es "a mi compañero le funciona un comando que a mí no me existe",
lo natural es pensar que la superficie de comandos se mueve mucho. Lo medimos
entre las dos versiones que tenemos en disco, la del corte del libro y la de
hoy:

```bash
~/.local/share/claude/versions/2.1.228 --help > h228.txt
~/.local/share/claude/versions/2.1.233 --help > h233.txt
diff h228.txt h233.txt
```

`diff` no devuelve nada. **242 líneas de ayuda, idénticas.** Cinco versiones de
diferencia y la superficie de banderas y subcomandos no se ha movido ni un
carácter.

Ahora la otra mitad de la medición. Las tres páginas de documentación oficial de
este módulo, descargadas hoy, condicionan comportamiento a **catorce versiones
distintas del CLI**, en diecisiete frases. Solo `authentication.md` cita ocho:

| Desde | Qué cambió, y qué pasaba antes |
|---|---|
| v2.1.146 | Antes, la restricción de organización no bloqueaba credenciales de variable de entorno |
| v2.1.203 | Aparece el aviso de caducidad del inicio de sesión al arrancar |
| v2.1.206 | Antes, un inicio de sesión caducado salía disfrazado de error del modelo |
| v2.1.208 | Antes, un `apiKeyHelper` que falla daba un 401 genérico tras unos diez reintentos silenciosos |
| v2.1.210 | `/status` muestra la fila `Login` con el estado caducado |
| v2.1.212 | Antes, `forceLoginMethod` solo se aplicaba a los inicios de sesión de terminal |
| v2.1.217 | Antes, el aviso de caducidad aparecía a cinco días en vez de a tres |
| v2.1.223 | El bloque `env` se fusiona clave a clave entre fuentes gestionadas |

Léela otra vez y fíjate en la forma de las frases: casi todas son **"antes
pasaba otra cosa"**. Ninguna añade un comando. Todas cambian cómo se comporta
algo que ya existía.

Esa es la lección del módulo. **La versión no te quita comandos: te cambia lo
que hacen.** Por eso el síntoma tarda tanto en resolverse. Estás buscando algo
que falta, y lo que hay es algo que responde distinto.

El ejemplo más caro de la lista está en la página de errores de instalación:
antes de la 2.1.211, en una máquina con varias sesiones abiertas, despertar el
ordenador de la suspensión podía hacer que dos sesiones renovaran el mismo
token, lo que **revocaba el inicio de sesión guardado** y obligaba a todas las
sesiones abiertas a volver a entrar a la vez.  ‹v2.1.211› Eso es un "ayer
funcionaba" perfecto, y ninguna configuración tuya lo explica.

### 2.2.3 · Los tres mandos: canal, suelo y verja

Hay tres ajustes distintos que la gente confunde entre sí. Hacen tres cosas que
no se parecen.

**El canal (release channel)**, con `autoUpdatesChannel`, decide de dónde vienen
las actualizaciones:

- `"latest"`, el valor por defecto: lo nuevo en cuanto sale.
- `"stable"`: una versión de aproximadamente una semana de antigüedad, que se
  salta las publicaciones con regresiones importantes.

**El suelo**, con `minimumVersion`, impide *bajar*. Las actualizaciones en
segundo plano y `claude update` se niegan a instalar por debajo de ese valor. Por
eso pasar de `latest` a `stable` no te degrada si ya estás en algo más nuevo: al
cambiarlo desde `/config` se te pregunta si quieres quedarte, y si te quedas,
`minimumVersion` se fija en la versión actual. Volver a `latest` lo limpia.

**La verja**, con `requiredMinimumVersion` y `requiredMaximumVersion`, solo
existe en los ajustes gestionados por la organización, y es la única que
**impide arrancar**. Si la versión que corre está fuera del rango, Claude Code
sale al inicio y le dice al usuario que actualice por la vía aprobada. Con una
salvedad bien pensada: `claude update`, `claude install` y `claude doctor`
siguen funcionando por debajo del suelo, para que se pueda salir del agujero.

Y una propiedad que conviene conocer antes de que te muerda: **las dos claves de
la verja fallan abiertas por diseño.** Un valor inválido se descarta en vez de
imponerse, para que un despliegue de política mal escrito no deje a toda la
empresa sin poder arrancar. Es la decisión correcta, y también significa que una
verja mal escrita no protege nada y no avisa.

Aparte de los tres, dos interruptores para apagar:

- `DISABLE_AUTOUPDATER` en el bloque `env` para la comprobación en segundo
  plano. `claude update` y `claude install` siguen funcionando.
- `DISABLE_UPDATES` para cerrar todas las vías, incluida la manual. Es lo que
  usa quien distribuye el binario por su cuenta.

> **Esto va a cambiar.** Al meter a propósito un valor inválido en
> `autoUpdatesChannel`, el binario 2.1.233 contesta:
> `Expected one of: "latest", "stable", "rc"`. Hay un tercer canal, `rc`, que
> **no aparece en `setup.md` ni en `settings.md`**, descargadas el 17 de agosto
> de 2026. El binario lo acepta; la documentación no dice qué contiene. No lo
> recomendamos y no lo hemos probado: lo dejamos escrito porque el día que se
> documente, esta caja se convierte en una sección.

### 2.2.4 · Autenticación: siete credenciales, y no gana la que crees

Cuando hay varias credenciales presentes a la vez, Claude Code elige una, y el
orden está fijado. La guía de referencia de la que sale este manual publicaba
una lista de cuatro. **Eran cuatro en su día y hoy son siete.** Esta es la de la
documentación descargada hoy, de mayor a menor prioridad:

| # | Credencial | Cómo viaja | Para qué es |
|---|---|---|---|
| 1 | Proveedor cloud, con `CLAUDE_CODE_USE_BEDROCK`, `_VERTEX` o `_FOUNDRY` | Según el proveedor | Bedrock, Agent Platform, Foundry |
| 2 | `ANTHROPIC_AUTH_TOKEN` | Cabecera `Authorization: Bearer` | Pasarelas y proxies con token |
| 3 | `ANTHROPIC_API_KEY` | Cabecera `X-Api-Key` | Acceso directo a la API |
| 4 | `apiKeyHelper` | Salida de un script tuyo | Credenciales rotatorias, vida corta |
| 5 | `CLAUDE_CODE_OAUTH_TOKEN` | Token de larga duración | Integración continua y scripts |
| 6 | Perfil Anthropic y credenciales de federación | Archivo de perfil | Identidad federada de empresa |
| 7 | Inicio de sesión de suscripción, con `/login` | OAuth guardado | Lo normal en Pro, Max, Team |

Fuera de la lista hay una octava: una sesión de pasarela de aplicaciones de
Claude iniciada gana incluso a la número 1.

Tres trampas de esta tabla, por orden de cuánta gente muerden:

**La de `-p`.** En modo interactivo, cuando hay una `ANTHROPIC_API_KEY` en el
entorno se te pregunta **una vez** si la apruebas, y tu respuesta se recuerda. En
modo no interactivo con `-p`, **la clave se usa siempre que esté presente**.
Puedes haberla rechazado a mano y estar pagándola en tus scripts sin enterarte.

**La del número 5.** Si arrancas `/login` con `CLAUDE_CODE_OAUTH_TOKEN` puesta,
la sesión actual pasa a la credencial nueva, pero la variable se vuelve a leer en
cada sesión siguiente hasta que la quites del perfil de tu shell o del bloque
`env`. Se arregla una sesión y se sigue rompiendo el resto.

**La del modo mínimo.** Con `--bare`, la autenticación de Anthropic es
estrictamente `ANTHROPIC_API_KEY` o `apiKeyHelper`: no se lee ni el OAuth
guardado ni el llavero del sistema, y **tampoco `CLAUDE_CODE_OAUTH_TOKEN`**. Un
script que arranque con `--bare` y dependa del token de larga duración no
autentica y el mensaje no te va a llevar hasta aquí.

Para saber cuál está ganando en tu máquina, sin abrir sesión:

```bash
claude auth status
```

Devuelve JSON con el método, el proveedor, la cuenta y la organización activas.
**Esa salida lleva datos personales**: el correo y el identificador de la
organización. Redáctalos antes de pegarla en una incidencia.

---

## 2.3 · Receta

### 2.3.1 · Individual: cuatro comandos y un archivo

Instalar por la vía nativa:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Comprobar, y quedarse con las tres salidas:

```bash
claude --version
claude doctor
claude auth status
```

Y fijar tus dos mandos en `~/.claude/settings.json`:

```json
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.233"
}
```

Con eso ya no te llega una regresión el día que sale, y no bajas nunca de un
suelo que tú has elegido.

### 2.3.2 · Equipo: el archivo va en el repositorio

En solitario, la versión es una curiosidad. En equipo es un dato del proyecto, y
un dato del proyecto vive en el repositorio o no existe.

Lo mínimo, y son dos archivos:

**Uno.** `.claude/settings.json` en la raíz del repositorio, versionado:

```json
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.233"
}
```

**Dos.** Un archivo corto que diga contra qué versión está escrito el proyecto y
cómo comprobarlo. En el laboratorio lo llamamos `ENTORNO.md`. No es
documentación: es la respuesta escrita a la primera pregunta de cualquier
discusión sobre comportamiento raro.

Para una organización, encima de los dos va la verja en ajustes gestionados:

```json
{
  "requiredMinimumVersion": "2.1.150"
}
```

Y el acuerdo humano que las hace funcionar, que cabe en tres líneas:

1. El suelo lo sube una persona, con un commit, cuando hay un motivo.
2. Nadie reporta un comportamiento raro sin pegar `claude --version` y
   `claude doctor`.
3. Si cambia el suelo, cambia también `ENTORNO.md`. En el mismo commit.

### 2.3.3 · Reproducir una versión concreta

Es lo que hace falta cuando el fallo solo aparece en la máquina de otro. El
instalador acepta un canal o un número exacto:

```bash
curl -fsSL https://claude.ai/install.sh | bash -s stable
curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89
```

El canal que elijas al instalar pasa a ser tu canal por defecto para las
actualizaciones, así que después de una instalación de este tipo conviene mirar
`claude doctor` antes de olvidarse.

### 2.3.4 · Procedencia, para cuando la pida seguridad

Cada publicación trae un `manifest.json` con las sumas SHA256 de todos los
binarios de todas las plataformas, y ese manifiesto **está firmado con una clave
GPG de Anthropic**. Verificar la firma del manifiesto verifica de forma
transitiva todos los binarios que lista.

```bash
curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import
gpg --fingerprint security@anthropic.com
```

La huella que tiene que aparecer:

```
31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE
```

Después, el manifiesto de la versión que quieras y su firma:

```bash
REPO=https://downloads.claude.ai/claude-code-releases
VERSION=2.1.89
curl -fsSLO "$REPO/$VERSION/manifest.json"
curl -fsSLO "$REPO/$VERSION/manifest.json.sig"
gpg --verify manifest.json.sig manifest.json
```

Una firma buena dice `Good signature from "Anthropic Claude Code Release
Signing <security@anthropic.com>"`. Junto a esa línea vas a ver un aviso de que
la clave no está certificada por una firma de confianza: eso es normal en
cualquier clave recién importada y no invalida nada. La comprobación
criptográfica es la línea de `Good signature`; que la clave sea la auténtica lo
demuestra la huella que comparaste antes.

Dos avisos. Las firmas del manifiesto existen a partir de la **2.1.89**: las
anteriores publican sumas sin firma. Y en Linux los binarios no llevan firma de
código propia, así que esta es la vía. En macOS y Windows sí la llevan.

### 2.3.5 · Cambiar de método de instalación

Cada vía tiene su procedimiento de desinstalación y no son intercambiables.
Hacerlo mal deja restos, y los restos producen **instalaciones duplicadas**, que
es una de las cosas que `claude doctor` reporta y una de las causas reales del
síntoma de este módulo.

La regla es de una línea: **desinstala primero con el procedimiento de la vía
vieja, instala después con la nueva.** Para encontrar lo que hay:

```bash
which -a claude
ls -la ~/.local/bin/claude
ls -la ~/.claude/local/
npm -g ls @anthropic-ai/claude-code 2>/dev/null
```

Que alguno diga `No such file or directory` no es un error: es que ahí no hay
nada, que es lo que quieres.

---

## 2.4 · Laboratorio · Dejar `gestor-pedidos` reproducible

Seguimos en el mismo repositorio del módulo 01. Este laboratorio no le pide nada
al modelo, así que no gasta.

**Paso 1. Averigua qué tienes y de dónde salió.**

```bash
claude --version
which -a claude
ls -la ~/.local/bin/claude
ls ~/.local/share/claude/versions/
```

La cuarta línea es la interesante. Si tienes más de una versión ahí, no es
basura: es tu máquina del tiempo.

**Paso 2. Diagnostica.**

```bash
claude doctor
```

Fíjate en `Config install method`, en `Auto-update channel` y en
`Last update attempt`. Esas tres líneas son las que te van a pedir cuando
reportes algo, y las que tienes que pedir tú cuando te reporten. Anota el canal
que ves ahora, que lo vas a necesitar en el paso 5.

**Paso 3. Comprueba con qué credencial estás trabajando.**

```bash
claude auth status
```

Lee el JSON y quédate con `authMethod` y `subscriptionType`. **No lo pegues en
ningún sitio sin quitar el correo y el `orgId`.**

**Paso 4. Fija los mandos del proyecto.** Crea `.claude/settings.json` dentro de
`gestor-pedidos`:

```json
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.233"
}
```

Pon tu versión, no la nuestra.

**Paso 5. Comprueba que el archivo se está leyendo de verdad.** Este paso es el
que hace que el laboratorio valga algo, porque es donde casi todo el mundo da
por hecho lo que no ha mirado. Ejecuta `claude doctor` dos veces, desde dos
sitios:

```bash
cd ~ && claude doctor | grep "Auto-update channel"
cd /ruta/a/gestor-pedidos && claude doctor | grep "Auto-update channel"
```

En nuestra máquina, la primera dice `latest` y la segunda dice `stable`. Esa
diferencia es la prueba de que el archivo del repositorio está entrando en la
configuración efectiva. Si las dos líneas dicen lo mismo, algo no se está
cargando y lo tienes que resolver ahora, no en el módulo 4.

**Paso 6. Rómpelo a propósito.** Añade una coma de más al final del JSON y
vuelve a ejecutar `claude doctor` desde el repositorio. Aparece un bloque nuevo:

```
Invalid settings
- /ruta/a/gestor-pedidos/.claude/settings.json: Invalid or malformed JSON
```

Y ahora mira las dos cosas que **no** pasan, que son las que hay que llevarse de
aquí:

**No cambia el código de salida.** `claude doctor` termina en 0 con el archivo
roto, y sigue imprimiendo `No installation issues found` unas líneas más abajo.
Una comprobación en integración continua que solo mire el código de salida da
verde con la configuración del proyecto en el suelo.

**No se avisa de las claves mal escritas.** Pon `"clavequenoexiste": true` con el
JSON ya bien formado y no aparece en ningún sitio. Los valores inválidos de
claves conocidas sí se reportan, y con detalle:

```
- .../settings.json › autoUpdatesChannel: Invalid value. Expected one of: "latest", "stable", "rc"
- .../settings.json › minimumVersion: Expected string, but received number
```

Un nombre de clave mal escrito, en cambio, es silencio. Y con `-p` la cosa va un
paso más allá: la documentación dice que en modo no interactivo **los archivos
de ajustes que no validan se ignoran en silencio**, sin diálogo de error. Es
decir, tu tubería nocturna puede llevar semanas corriendo sin el suelo de
versión que crees tener.

**Paso 7. Arregla el JSON y anota la versión.** Crea `ENTORNO.md` en la raíz de
`gestor-pedidos` con la versión de referencia, el suelo, el canal, el método de
instalación esperado y la fecha. Cinco filas de tabla. El archivo del
laboratorio está en `D6-repo-feo/gestor-pedidos/ENTORNO.md`.

**Paso 8, opcional pero recomendado. La máquina del tiempo.** Si tienes dos
versiones bajo `versions/`, compáralas:

```bash
~/.local/share/claude/versions/2.1.228 --help > /tmp/h228.txt
~/.local/share/claude/versions/2.1.233 --help > /tmp/h233.txt
diff /tmp/h228.txt /tmp/h233.txt
```

Lo esperable es que no salga nada, como nos pasó a nosotros. Sirve para
interiorizar la sección 2.2.2: cuando alguien dice que le falta un comando, casi
nunca le falta un comando.

---

## 2.5 · Prueba

**PASA** si se cumplen las cuatro:

1. `claude doctor` ejecutado dentro de `gestor-pedidos` no reporta ningún bloque
   `Invalid settings` y dice `No installation issues found`.
2. La línea `Auto-update channel` de ese `claude doctor` dice **algo distinto**
   de la que sale ejecutándolo desde tu directorio personal, o sabes explicar
   por qué coinciden.
3. `.claude/settings.json` y `ENTORNO.md` están **añadidos al control de
   versiones**, no solo creados.
4. Puedes contestar, sin mirar, qué credencial de las siete está usando tu
   máquina ahora mismo.

**FALLA** si la 1 se cumple pero la 2 no la has comprobado. Un `doctor` limpio
con un archivo que no se está leyendo es exactamente el estado en el que llega
la gente que tiene este problema: todo verde y nada aplicado.

> **Esto va a cambiar.** El texto exacto de `claude doctor` es salida de
> diagnóstico, no una interfaz estable, y las etiquetas se mueven entre
> versiones. Lo que comprobamos con un comando es que las líneas de método de
> instalación y de canal existen, no su redacción. Nuestra ejecución es del 17
> de agosto de 2026 con la 2.1.233. Si en tu versión se llaman de otra forma, el
> dato es tuyo y nos interesa.

---

## 2.6 · Coste de este módulo

| Concepto | Cantidad |
|---|---|
| Tokens de entrada del laboratorio | 0 |
| Tokens de salida | 0 |
| Coste | 0,00 € |
| Tiempo | 25 minutos |
| Impuesto de contexto permanente | ninguno |
| Mantenimiento continuo | subir el suelo cuando haya motivo, y tocar dos archivos |

Cero no es una errata. Todo lo de este módulo se comprueba contra el binario y
contra el disco, y esa es precisamente la razón por la que conviene hacerlo
antes que nada: es la única parte del sistema que puedes dejar bien sin gastar.

El coste real de este módulo no está en la factura, está en la disciplina. Dos
archivos que hay que tocar cuando cambia el suelo, y una costumbre de equipo que
consiste en pegar dos salidas de comando antes de opinar. Si esa costumbre no
cuaja, los dos archivos envejecen y vuelves al punto de partida con la ventaja
de creer que estás cubierto, que es peor que no tener nada.

---

## Runbook · Módulo 02

> **Cuando algo se comporta distinto en dos máquinas**
>
> 1. `claude --version` en las dos. Si difieren, ya está.
> 2. `claude doctor` en las dos. Mirar `Config install method`,
>    `Auto-update channel` y `Last update attempt`.
> 3. `claude auth status` en las dos. Redactar correo y `orgId` antes de pegarlo.
> 4. `which -a claude`. Más de uno es la respuesta.
>
> **Los tres mandos, que no son lo mismo**
>
> | Ajuste | Qué hace | Dónde vive |
> |---|---|---|
> | `autoUpdatesChannel` | De dónde vienen las actualizaciones: `latest` o `stable` | Cualquier settings |
> | `minimumVersion` | Impide bajar. No bloquea el arranque | Cualquier settings |
> | `requiredMinimumVersion` | Impide arrancar fuera de rango. Falla abierto si el valor es inválido | Solo ajustes gestionados |
>
> **Reproducir una versión**
> `curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89`
> Las versiones anteriores siguen en `~/.local/share/claude/versions/`.
>
> **Cambiar de método de instalación:** desinstalar con el procedimiento de la
> vía vieja **antes** de instalar con la nueva. Si no, instalaciones duplicadas.
>
> **Autenticación, orden de prioridad:**
> cloud → `ANTHROPIC_AUTH_TOKEN` → `ANTHROPIC_API_KEY` → `apiKeyHelper` →
> `CLAUDE_CODE_OAUTH_TOKEN` → perfil o federación → `/login`.
> Con `-p`, la `ANTHROPIC_API_KEY` se usa siempre que esté presente, la hayas
> rechazado o no. Con `--bare` no se lee `CLAUDE_CODE_OAUTH_TOKEN`.
>
> **`claude doctor` termina en 0 aunque tus ajustes no validen.**
> El código de salida no es la comprobación. El bloque `Invalid settings` sí.
> Una clave con el nombre mal escrito no se reporta en absoluto.
