# Módulo 03 · Memoria y contexto

> **Laboratorio de este módulo:** ~40 minutos · unos **435.000 tokens de
> entrada** y 2.200 de salida · **0,31 dólares** según la telemetría del propio
> CLI, que a cualquier cambio euro-dólar de agosto de 2026 se queda **por debajo
> de 0,35 €**. Con un plan de suscripción va incluido.
> **Verificado contra:** Claude Code 2.1.234 · 18 de agosto de 2026.

> **Nota de versión de este módulo.** El libro declara corte el 12 de agosto de
> 2026 contra la 2.1.228; este módulo se ha escrito y medido seis días después
> contra la 2.1.234. Las cifras de tokens son de esa ejecución y de esa máquina,
> y están marcadas como tales.

---

## 3.1 · Síntoma

Empiezas la tarde explicándole el proyecto: que la configuración buena es la
nueva, que el endpoint viejo no se toca, que los tests se lanzan así y no asá.
Trabaja bien durante una hora.

Y entonces, sin aviso, vuelve a proponerte exactamente lo que le dijiste que no
hiciera. No te ha desobedecido: se le ha ido. La conversación se compactó
mientras mirabas otra cosa, y con ella se fue todo lo que solo existía ahí.

La reacción natural es escribirlo en el `CLAUDE.md`, porque siempre está ahí. Y
funciona, así que la próxima cosa también va al `CLAUDE.md`, y la siguiente.
Seis meses después tienes cuatrocientas líneas que se pagan en cada turno de
cada sesión, la mitad describen un código que ya no existe, dos se contradicen
entre sí, y sigues sin saber por qué unas se cumplen y otras no.

Los dos problemas son el mismo problema con dos caras. Y ninguna de las dos se
arregla escribiendo más.

---

## 3.2 · Modelo mental

### 3.2.1 · La ley que gobierna todo lo demás

Está en la documentación oficial, en una frase que casi nadie lee despacio:

> Claude trata ambos sistemas de memoria como **contexto, no como configuración
> impuesta**.

`CLAUDE.md` no es un archivo de reglas que se cumplen. Es un texto que se lee.
La documentación es todavía más concreta sobre el mecanismo: **el contenido del
`CLAUDE.md` se entrega como un mensaje de usuario después del sistema**, no
dentro del sistema. Es decir, ocupa el mismo sitio conceptual que si se lo
hubieras pegado tú al empezar. Con la misma autoridad que eso tiene, que es
mucha y no es absoluta.

De ahí salen las tres consecuencias que gobiernan el módulo entero:

**Una.** Si algo no puede fallar nunca, no va aquí. Va en un hook `PreToolUse`,
que es código y no interpretación. Es la pregunta 01 del árbol del módulo 01, y
este es su fundamento documentado.

**Dos.** Cuanto más específica y concisa sea la instrucción, más
consistentemente se sigue. La documentación pide instrucciones **concretas hasta
el punto de poder verificarlas**, y ese es un buen filtro: si no sabes qué
comando probaría que se ha cumplido, todavía no está escrita.

**Tres.** Si dos instrucciones se contradicen, se elige una de forma
arbitraria. No hay desempate. Podar es mantenimiento, no perfeccionismo.

### 3.2.2 · Cómo se cargan de verdad

Claude Code **sube por el árbol de directorios** desde donde lo arrancas,
mirando en cada nivel si hay `CLAUDE.md` y `CLAUDE.local.md`. Lanzando en
`foo/bar/`, carga `foo/bar/CLAUDE.md`, `foo/CLAUDE.md` y los `CLAUDE.local.md`
de al lado.

Tres reglas de orden que explican casi todo comportamiento raro:

1. **Todo se concatena, nada se sobrescribe.** No existe un `CLAUDE.md` que
   gane. El del proyecto no anula el tuyo personal: están los dos, y por eso se
   pueden contradecir.
2. **El orden va de la raíz hacia tu directorio**, así que lo más cercano se lee
   el último.
3. **Dentro de cada nivel, `CLAUDE.local.md` va después de `CLAUDE.md`.**

Y la excepción que explica media docena de sustos: los `CLAUDE.md` de
subdirectorios **por debajo** de donde arrancaste no se cargan al empezar.
Entran al leer un archivo de ese subdirectorio.

Dos trampas más, de las caras:

**`--add-dir` no carga los `CLAUDE.md` del directorio añadido.** Das acceso a la
carpeta y das por hecho que van sus instrucciones. No. Hay que pedirlo:

```bash
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../config-compartida
```

Eso sí carga `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md` y
`CLAUDE.local.md` del directorio adicional.

**Los imports externos se aprueban una sola vez, y el "no" es para siempre.** Un
`CLAUDE.md` puede importar otros archivos con `@ruta`, hasta cuatro saltos. Si
el import apunta fuera de tu directorio de trabajo, la primera vez aparece un
diálogo listando los archivos, y si lo rechazas, **los imports quedan
desactivados y el diálogo no vuelve a aparecer**. Es deliberado y protege de lo
que otra persona confirme en un repositorio compartido. También significa que un
"no" dado con prisa hace tiempo puede ser la razón de que hoy falte contexto.

### 3.2.3 · Lo que cuesta, medido aquí

La documentación publica un recorrido de ejemplo con un `CLAUDE.md` de proyecto
de 1.800 tokens. Es un ejemplo, no una constante. Estas son nuestras cifras, en
la máquina donde se escribe el libro, con la 2.1.234, sobre el repositorio del
laboratorio. Método: la misma petición trivial (`Responde solo con la palabra
OK.`) en el mismo repositorio, variando **una sola cosa**, con
`claude -p "..." --output-format json`, sumando `input_tokens`,
`cache_creation_input_tokens` y `cache_read_input_tokens`. Cada medida, dos
veces, y las dos idénticas.  ‹v2.1.234›

| Estado del archivo | Tokens de entrada |
|---|---:|
| Sin `CLAUDE.md` | 42.302 |
| `CLAUDE.md` de 66 líneas | 43.480 |
| Las mismas 66 líneas más 40 de notas dentro de `<!-- -->` | **43.480** |
| Las mismas 66 líneas con esas 40 notas visibles | 46.720 |

Tres lecturas, por orden de utilidad:

**El archivo cuesta 1.178 tokens**, unos 18 por línea, en cada turno de cada
sesión, se use o no lo que contiene. Un `CLAUDE.md` de cuatrocientas líneas es
un peaje de unos siete mil tokens por turno.

**Los comentarios HTML de bloque cuestan exactamente cero.** No "poco": la fila
tercera da el mismo número que la segunda, hasta el token. Se eliminan antes de
inyectar el contenido. Cuarenta líneas de notas para el humano que mantenga el
archivo salen gratis, y esas mismas cuarenta líneas visibles habrían costado
**3.240 tokens en cada turno**. Los comentarios dentro de bloques de código sí
se conservan, y todos siguen visibles si abres el archivo con la herramienta de
lectura.

**Los 42.302 de la primera fila no son el archivo.** Son el suelo: sistema,
entorno, nombres de herramientas, descripciones de skills. Conviene saberlo
antes de pelearse por recortar doscientos tokens de un `CLAUDE.md`.

> **Esto va a cambiar.** Estas cifras dependen de la máquina, del modelo y de la
> versión. No las copies: mídelas. El procedimiento de arriba es lo que hay que
> llevarse, no los números. Lo que sí esperamos que aguante es el **orden de
> magnitud de las relaciones**: el archivo cuesta bastante menos que el suelo de
> arranque, y el comentario HTML cuesta cero exacto.

### 3.2.4 · Qué sobrevive a la compactación

Esta es la respuesta a "se le ha olvidado lo que le dije", y es una tabla que
conviene tener a mano:

| Mecanismo | Después de compactar |
|---|---|
| Sistema y estilo de salida | Intactos. No son historial |
| `CLAUDE.md` de la raíz y reglas sin `paths` | **Se releen del disco y se reinyectan** |
| Auto memory | Se reinyecta del disco |
| Reglas con `paths:` | Se pierden hasta que se vuelva a leer un archivo que case |
| `CLAUDE.md` anidados en subdirectorios | Se pierden hasta que se lea un archivo de ahí |
| Cuerpos de skills invocadas | Se reinyectan, con tope de 5.000 tokens por skill y 25.000 en total, y se cae primero la más vieja |
| Hooks | No aplica. Son código, no contexto |

Así que si una instrucción desapareció al compactar, solo hay tres
posibilidades, y se descartan en este orden:

1. **Se dio solo en la conversación.** Es la causa con diferencia más frecuente.
2. Vive en un `CLAUDE.md` anidado que todavía no se ha recargado.
3. Es una regla por ruta que no ha casado con ningún archivo desde entonces.

La cura de la primera es la regla que gobierna el módulo: **lo que tiene que
persistir va al archivo, no al historial.** Y el corolario para las otras dos:
si una regla tiene que sobrevivir a la compactación sí o sí, quítale el
frontmatter `paths` o súbela al `CLAUDE.md` de la raíz.

---

## 3.3 · Receta

### 3.3.1 · Individual: el filtro de una sola pregunta

Para cada bloque que quieras meter en el `CLAUDE.md`, una pregunta: **¿esto hace
falta en todas las tareas de este repositorio?**

- **Sí** → se queda. Es lo único que justifica pagarlo en cada turno.
- **No, solo cuando toco cierta zona del código** → regla con `paths`.
- **No, solo cuando hago cierta tarea** → skill, que es el módulo 07.
- **No es contexto, es una prohibición** → hook, que es el módulo 05. No estaba
  en el sitio equivocado: estaba en la categoría equivocada.

El objetivo de tamaño que da la documentación es **por debajo de 200 líneas**.
Por encima, los archivos siguen cargándose enteros, pero la adherencia baja. Es
un objetivo, no un límite del programa.

Qué merece estar siempre presente: los comandos de compilar y probar, las
convenciones que difieren de lo que el modelo supondría por defecto, y **las
trampas**. Qué no: inventarios de directorios, listas de dependencias y
descripciones de arquitectura que se deducen leyendo el código, porque eso lo va
a averiguar igual y estás pagando por adelantado algo que ya sabe. Desde la
2.1.206,
`/doctor` propone recortes de un `CLAUDE.md` versionado siguiendo exactamente
ese criterio: quita lo derivable y conserva las trampas y las razones.  ‹v2.1.206›

Una regla que sale del laboratorio de este módulo, y nos costó una corrección en
directo: **no cites números de línea.** Envejecen en el primer commit y luego
mandan al agente al sitio equivocado con toda la autoridad de estar escritos.
Cita la función y el literal.

### 3.3.2 · Equipo: partir en reglas antes de que duela

Cuando el archivo se acerque a las 200 líneas, se parte en `.claude/rules/`:

```text
tu-proyecto/
└── .claude/
    ├── CLAUDE.md
    └── rules/
        ├── estilo-codigo.md
        ├── testing.md
        └── api.md
```

Con un matiz que lo cambia todo: **una regla sin `paths` se carga al arrancar
con la misma prioridad que el `CLAUDE.md`**. Partir el archivo en seis no ahorra
ni un token. Lo que ahorra es el frontmatter:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# Reglas de la API
- Todo endpoint valida su entrada
- Formato de error estándar
```

Esa regla solo entra cuando se lee un archivo que casa con el patrón. Se dispara
**al leer el archivo, no en cada uso de herramienta**. Desde la 2.1.198 la
coincidencia también funciona cuando se llega al archivo por un enlace
simbólico (symlink).  ‹v2.1.198›

Tres avisos sobre los patrones, aprendidos por las malas por otros:

- Las llaves multiplican. `{a,b}/{c,d}/*.{ts,tsx}` son ocho patrones, y la lista
  entera de una regla comparte un presupuesto de 1.000 expandidos. Lo que se
  pase se usa sin expandir, y las llaves literales no casan con nada. Antes de
  la 2.1.217 colgaba o tumbaba el CLI al arrancar.  ‹v2.1.217›
- El corchete abre una expresión de clase, así que `photos [2024/**` es inválido
  y no casa con nada; para un corchete literal, `photos \[2024/**`. Antes de la
  2.1.207, **un solo patrón inválido hacía fallar la lectura de todos los
  archivos** contra los que se evaluaba esa regla.  ‹v2.1.207›
- Las reglas de proyecto se saltan si excluyes `project` de `--setting-sources`.
  Antes de la 2.1.211, las que cargan bajo demanda se cargaban igualmente.  ‹v2.1.211›

Y para el monorepo, `claudeMdExcludes` en `.claude/settings.local.json`, para
saltarse los `CLAUDE.md` de otros equipos. Los gestionados por la organización
no se pueden excluir, que es justo el sentido de que sean gestionados.

Si el repositorio ya tiene un `AGENTS.md` para otros agentes, no lo dupliques:
Claude Code lee `CLAUDE.md` y no `AGENTS.md`, así que se crea un `CLAUDE.md`
cuya primera línea sea `@AGENTS.md` y se añade debajo lo específico de Claude.

### 3.3.3 · Auto memory, la memoria que escribe él

Aparte del archivo que escribes tú hay otro sistema, encendido por defecto, que
escribe Claude: comandos de compilación que aprende, hallazgos de depuración,
preferencias que le has corregido. Vive en
`~/.claude/projects/<proyecto>/memory/`, y la ruta se deriva del repositorio de
git, así que **todos los worktrees y subdirectorios del mismo repo comparten un
único directorio de memoria**. Es local a la máquina: no viaja.

Dentro hay un `MEMORY.md` que hace de índice, más archivos por tema. Del índice
se cargan **las primeras 200 líneas o 25 KB**, lo que llegue antes; lo que pase
de ahí se cae en la siguiente carga, y el programa devuelve un error pidiendo
reescribirlo. Ese recuento mide **solo lo que se carga**: el frontmatter y los
comentarios HTML se descuentan desde la 2.1.211.  ‹v2.1.211› Los archivos por
tema no se cargan al arrancar; se leen cuando hacen falta.

Se apaga con el interruptor de `/memory`, con `autoMemoryEnabled` en el
`settings.json` del proyecto, o con `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. Y
`autoMemoryDirectory` cambia dónde se guarda, pero puesto en el proyecto **solo
se honra tras aceptar el diálogo de confianza del espacio de trabajo**, la misma
puerta que gobierna los hooks: un repositorio clonado no te mueve archivos de
sitio sin permiso.

Dos datos que se olvidan: la auto memory **no se carga en los subagentes**,
salvo en una bifurcación (fork), así que el revisor del módulo 08 no sabe lo que
aprendió el principal; y los archivos de memoria quedan **fuera de la limpieza
automática** que borra las transcripciones viejas.

### 3.3.4 · Diagnóstico: tres herramientas, por orden

**`/context`.** Lo primero, siempre. Da el desglose real de la sesión por
categorías e incluye la lista de **Memory files** con lo que se cargó de verdad.
Si tu archivo no está ahí, no existe para la sesión, y lo demás sobra.

**El hook `InstructionsLoaded`.** Registra qué archivos de instrucciones se
cargan, cuándo y por qué. Es la herramienta para depurar reglas por ruta y
archivos que cargan tarde, los dos casos donde `/context` mirado en el momento
equivocado te engaña.

**El modo mínimo, `--bare`.** Arranca saltándose hooks, plugins, auto memory y
el descubrimiento automático de `CLAUDE.md`. Contesta a "¿esto lo hace el
programa o lo hace mi configuración?".

> **Esto va a cambiar.** Con `--bare`, la autenticación de Anthropic es
> estrictamente `ANTHROPIC_API_KEY` o `apiKeyHelper`: no se lee el OAuth
> guardado ni el llavero. Probado el 18 de agosto de 2026 con la 2.1.234 en una
> máquina con inicio de sesión de suscripción, `--bare` contesta
> `Authentication error · This may be a temporary network issue, please try
> again`, que no lleva a nadie hasta aquí. **Si no tienes clave de API, el modo
> mínimo no es tu herramienta de diagnóstico**: aparta el archivo con `mv` y
> vuelve a preguntar, que es lo que hace el laboratorio de este módulo.

---

## 3.4 · Laboratorio · El primer `CLAUDE.md` de `gestor-pedidos`

Seguimos en el repositorio de siempre. Del módulo 01 traes una lista de
contradicciones. Hoy se resuelven por escrito.

**Paso 1. Mide el suelo antes de tocar nada.** Sin `CLAUDE.md` todavía:

```bash
cd gestor-pedidos
claude -p "Responde solo con la palabra OK." --output-format json > sin.json
```

Suma `input_tokens`, `cache_creation_input_tokens` y
`cache_read_input_tokens` de `usage`. Ese es tu suelo. En nuestra máquina,
42.302.

**Paso 2. Haz la pregunta cara, sin archivo.** Esta es la pregunta que le harías
un martes cualquiera:

```
Hay que subir el IVA de Portugal del 23 al 24 por ciento. Dime exactamente qué
archivos y qué líneas hay que tocar. No edites nada, solo dímelo.
```

Guarda la respuesta y el gasto. Nuestras dos ejecuciones dijeron lo mismo:
**hay que tocar `settings.py`, `utils.py` y `app.py`.**

Es una respuesta excelente y es falsa. Dos de los tres archivos son código
muerto: nadie los importa, y cambiar `settings.py` no tiene ningún efecto sobre
lo que cobra la empresa. Fíjate en lo que hace tan convincente el error: no se
inventó nada. Los tres archivos existen, los tres contienen un `0.23` o un
`1.23`, y los encontró todos. Lo que no podía saber es **cuál está enchufado**,
porque eso no está escrito en ningún sitio del repositorio.

**Paso 3. Averigua tú la verdad.** Un comando:

```bash
grep -rn "import" --include=*.py .
```

`app.py` importa `sqlite3`, `os` y `flask`, y nada más. Ni `config`, ni
`settings`, ni `utils`. La respuesta a "cuál de los dos archivos de
configuración manda" es **ninguno de los dos**: `app.py` fija sus valores a
mano. Es el fallo 8 del guion de doma, y es peor de lo que dice el inventario,
porque `utils.py` entero está muerto, incluida `calcular_iva()`, que parece
justamente la función buena.

**Paso 4. Escríbelo.** Crea `CLAUDE.md` en la raíz del repositorio. El archivo
completo está en `D6-repo-feo/gestor-pedidos/CLAUDE.md`, 67 líneas, y tiene
cuatro secciones que valen para cualquier repositorio heredado:

1. **Qué es esto**, en tres líneas.
2. **La verdad sobre la configuración**, con una tabla de dónde vive de verdad
   cada valor y qué dicen los archivos muertos. Sin números de línea.
3. **Código muerto, no proponer cambios aquí**, con la lista completa y una
   instrucción explícita: si un cambio parece que toca esto, dilo antes de
   editar.
4. **Quién gana los empates**: cuando el README y `app.py` se contradigan, manda
   `app.py`.

Y las notas de mantenimiento, dentro de `<!-- -->`, porque son para el humano
que herede el archivo y cuestan cero.

**Paso 5. Repite la pregunta cara, palabra por palabra.** Lo único que ha
cambiado es el archivo. Nuestro resultado, dos veces:

| | Sin `CLAUDE.md` | Con `CLAUDE.md` |
|---|---|---|
| Archivos que dice tocar | `settings.py`, `utils.py`, `app.py` | **solo `app.py`** |
| ¿Correcta? | **No.** Dos de tres están muertos | Sí |
| Turnos | 7 y 7 | 3 y 3 |
| Tokens de entrada | 216.615 y 261.009 | 131.952 y 132.003 |

El archivo no solo lo hace acertar: lo hace costar **entre 1,6 y 2 veces menos**,
porque deja de ir a averiguar al código lo que podía haber leído. Las dos
ejecuciones con archivo coinciden en 51 tokens; las de sin archivo se
diferencian en un veinte por ciento entre sí, y esa inestabilidad también es un
dato: sin contexto, cada ejecución explora por su cuenta.

**Paso 6. Comprueba que se está cargando.** Abre una sesión interactiva y
ejecuta `/context`. Tu `CLAUDE.md` tiene que aparecer bajo **Memory files**. Si
no aparece, no se está leyendo, y el resto del laboratorio no significa nada.

**Paso 7, el que casi nadie hace. Comprueba lo que cuesta.** Repite el paso 1
ahora que el archivo existe y resta. En nuestra máquina, 43.613 menos 42.302:
**1.311 tokens por turno**. Ese es el precio de la memoria del proyecto, y ahora
lo sabes en vez de suponerlo.

**Paso 8, opcional. Comprueba que el comentario es gratis.** Añade cuarenta
líneas de notas dentro de `<!-- -->` y vuelve a medir. Tiene que salir el mismo
número, exacto. Luego quita las marcas de comentario y mide otra vez: a nosotros
nos costaron 3.240 tokens en cada turno.

---

## 3.5 · Prueba

**PASA** si se cumplen las cuatro:

1. Existe `CLAUDE.md` en la raíz de `gestor-pedidos`, **añadido al control de
   versiones**, y aparece bajo `Memory files` al ejecutar `/context`.
2. La misma pregunta del paso 2, repetida con el archivo puesto, señala
   **`app.py` y nada más**, sin que se lo recuerdes en la petición.
3. El archivo dice, por escrito, que **ninguno de los dos archivos de
   configuración está en uso**. No "manda `settings.py`".
4. Sabes cuántos tokens cuesta tu archivo, porque lo has restado.

**FALLA** si tu `CLAUDE.md` dice que la configuración buena es `settings.py`.
Es lo que sale de leer los comentarios del repositorio, es lo que contesta
cualquiera con prisa, y es falso. Un archivo de memoria que afirma algo falso es
peor que no tener archivo: has convertido una duda en una certeza equivocada, y
la has hecho persistente.

> **Esto va a cambiar.** Lo que el agente contesta depende de la versión y del
> modelo. Nuestra ejecución es del 18 de agosto de 2026 con la 2.1.234, dos
> repeticiones por medida. El resultado cualitativo (tres archivos sin memoria,
> uno con memoria) es el que esperamos que aguante; los tokens exactos, no. Si
> el tuyo no coincide, el dato es tuyo y nos interesa.

---

## 3.6 · Coste de este módulo

| Concepto | Cantidad |
|---|---|
| Tokens de entrada del laboratorio | ~435.000 |
| Tokens de salida | ~2.200 |
| Coste medido por el CLI | 0,31 dólares |
| Coste en euros | por debajo de 0,35 € |
| Tiempo | 40 minutos |
| **Impuesto de contexto permanente** | **1.311 tokens por turno, medidos** |
| Mantenimiento continuo | podar cuando el código cambie |

Este es el primer módulo del libro que te deja una factura recurrente, y por eso
lleva medida en vez de estimación. 1.311 tokens por turno no es nada. 400 líneas
de `CLAUDE.md` sí lo son, y se llega a 400 líneas sin darse cuenta, añadiendo
tres cada vez que algo sale mal.

El coste que de verdad se paga aquí no es el de arranque: es el de **mantener el
archivo honesto**. Un `CLAUDE.md` que describe el código de hace seis meses no
es contexto neutro que se ignora, es desinformación que se lee entera en cada
turno y compite con lo que el agente está viendo en el disco. La poda no es
opcional: es la mitad del trabajo.

---

## Runbook · Módulo 03

> **"Se le ha olvidado lo que le dije"**
>
> 1. ¿Lo dijiste solo en la conversación? Es la causa más frecuente. Al archivo.
> 2. ¿Vive en un `CLAUDE.md` de un subdirectorio? No se recarga solo tras
>    compactar. Vuelve al archivo de la raíz.
> 3. ¿Es una regla con `paths:`? Se pierde al compactar hasta que se lea un
>    archivo que case. Si tiene que persistir, quítale el `paths`.
>
> **"No me hace caso"**
>
> 1. `/context` → ¿aparece bajo `Memory files`? Si no, no se está cargando.
> 2. ¿La instrucción es verificable? "2 espacios" sí, "formatea bien" no.
> 3. ¿Hay dos instrucciones que se contradicen? Se elige una al azar. Poda.
> 4. ¿No puede fallar nunca? Entonces no es contexto: es un hook.
>
> **Dónde va cada cosa**
>
> | ¿Hace falta en todas las tareas del repo? | Sitio |
> |---|---|
> | Sí | `CLAUDE.md` de la raíz |
> | Solo al tocar cierta zona | regla con `paths:` en `.claude/rules/` |
> | Solo al hacer cierta tarea | skill |
> | No es contexto, es una prohibición | hook |
>
> **Orden de carga:** de la raíz hacia tu directorio, todo concatenado, nada
> sobrescribe. `CLAUDE.local.md` va después del `CLAUDE.md` de su nivel.
> Los subdirectorios entran al leer archivos de ahí, no al arrancar.
>
> **Gratis y de pago**
> Notas dentro de `<!-- -->`: **0 tokens**, medido. Las mismas notas visibles:
> 3.240. Objetivo de tamaño: por debajo de 200 líneas.
> Partir en reglas **sin `paths` no ahorra nada**: cuesta igual que el CLAUDE.md.
>
> **Trampas**
> `--add-dir` no carga los `CLAUDE.md` del directorio añadido: hace falta
> `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`.
> Un diálogo de imports externos rechazado no vuelve a preguntar nunca.
> `--bare` no lee el OAuth guardado: sin clave de API, no autentica.
>
> **Cómo se mide lo que cuesta tu archivo**
> ```
> claude -p "Responde solo con la palabra OK." --output-format json
> ```
> Suma `input_tokens` + `cache_creation_input_tokens` +
> `cache_read_input_tokens`. Una vez con el archivo y otra sin él. Resta.
> Dos repeticiones: si no coinciden, no te lo creas.
