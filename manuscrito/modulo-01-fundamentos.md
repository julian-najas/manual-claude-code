# Módulo 01 · Fundamentos y el árbol de decisión

> **Laboratorio de este módulo:** ~15 minutos · una sola invocación:
> **147.176 tokens de entrada** y unos 2.650 de salida · entre **0,04 y 0,09
> dólares** según cómo esté la caché, que a cualquier cambio euro-dólar de 2026
> se queda **por debajo de 0,10 €**. Con un plan de suscripción va incluido.
> **Verificado contra:** Claude Code 2.1.228 · 12 de agosto de 2026.
> **Cifras vueltas a medir contra:** Claude Code 2.1.296 · 11 de octubre de 2026.

> **Nota de versión.** Este módulo se escribió con la 2.1.228 y su texto es de
> entonces. La factura de arriba, no: estaba estimada en 40.000 tokens y ahora
> está medida con la 2.1.296, y son 147.176. Se corrige en vez de maquillarse
> porque la regla de la casa dice que los tokens se miden. Las cifras pertenecen
> a esa versión y a esa máquina, y van marcadas al margen.

---

## 1.1 · Síntoma

Llevas meses usándolo todos los días. Sabes pedirle cosas y sabes cuándo no
fiarte. Y aun así, cada vez que quieres que algo se comporte de una manera
concreta, acabas en la misma duda:

*"¿Esto lo pongo en el CLAUDE.md, me hago una skill, monto un hook, o llamo a un
subagente?"*

Y como no hay una respuesta clara, haces lo que hacemos todos: lo escribes en el
`CLAUDE.md`, porque es lo que siempre está ahí. El archivo crece. Un día tiene
cuatrocientas líneas, la sesión se queda sin contexto a media tarea, y sigues sin
entender por qué la mitad de las instrucciones que escribiste se cumplen y la
otra mitad no.

Ese es el problema que resuelve este módulo. No es un problema de conocimiento:
es un problema de **taxonomía**. Nadie te ha dicho para qué sirve cada pieza, así
que usas la que tienes más a mano.

---

## 1.2 · Modelo mental

### 1.2.1 · Lo que separa a un agente de un chat con código

Un chat te devuelve texto. Un agente **actúa**: lee archivos que tú no le has
pegado, ejecuta comandos, escribe en tu disco y decide el siguiente paso sin
preguntarte. La diferencia no es la calidad del modelo, es que uno tiene manos.

Conviene ver una vez qué forma tienen esas manos. El agente no contesta: entra
en un bucle de tres fases que se mezclan entre sí, **reunir contexto**,
**actuar** y **verificar**, y usa herramientas en las tres. Busca archivos,
edita, lanza los tests para comprobar lo que acaba de escribir y decide en cada
paso qué hace en el siguiente.

El laboratorio de este módulo lo deja a la vista: a una sola pregunta, sin más
contexto, el agente respondió en **diez turnos** y tras abrir **nueve archivos**
que nadie le señaló. ‹v2.1.296› No es un prompt con suerte, es el bucle.

De ahí sale la consecuencia que más decide si esto funciona en un proyecto
real: **la calidad de la fase de verificar la pones tú**. Si el repositorio no
tiene nada contra lo que verificar, ni tests ni un esquema, el bucle se queda en
dos fases y lo que sale es plausible en vez de correcto. No depende del modelo,
depende de lo que haya en tu disco, y es la razón de que el módulo 9 insista
tanto con los primeros tests.

Y una segunda cosa, antes que cualquier configuración: lo que puede tocar no es
una integración con permisos recortados, es **cualquier comando que pudieras
ejecutar tú**. Los módulos 4 y 5 existen enteros por esa línea.

Y en cuanto algo tiene manos, deja de ser una cuestión de prompts y pasa a ser
una cuestión de **sistema**. Un sistema, en este libro, son seis cosas:

| Pieza | La pregunta que responde |
|---|---|
| **Rol** | Qué se espera de él y qué no |
| **Memoria** | Qué sabe sin que se lo cuentes cada vez |
| **Herramientas** | Qué puede tocar |
| **Límites** | Qué no puede tocar, aunque se lo pidas |
| **Control de calidad** | Cómo sabemos si lo hizo bien |
| **Métricas** | Cuánto costó y cuánto tardó |

Si falta una, no tienes un agente: tienes un prompt caro con permisos de
escritura. Esa frase es la tesis del libro y va a volver en cada módulo.

Lo importante para ahora mismo: **cada una de esas seis columnas se configura con
una pieza distinta de Claude Code**. Por eso hace falta el árbol.

### 1.2.2 · Las siete piezas

Claude Code te da siete sitios donde poner cosas. Casi toda la confusión del
mundo viene de que se parecen entre sí en la superficie y no se parecen en nada
por dentro.

**CLAUDE.md** es memoria de proyecto. Un archivo de texto que se carga al abrir y
acompaña a toda la sesión. Es lo que el agente sabe sin preguntar.

**Skill** es un procedimiento guardado que vive apagado. Tiene una descripción y
un cuerpo. La descripción está siempre presente; el cuerpo solo se carga cuando
la tarea encaja con esa descripción. Es memoria bajo demanda.

**Hook** es código tuyo que el programa ejecuta ante un evento del ciclo de vida:
antes de una herramienta, después de editar, al terminar. No pasa por el modelo.
No se interpreta. Se ejecuta.

**Comando** es un prompt guardado con nombre, que invocas tú escribiendo una
barra y su nombre. Es un atajo de teclado con texto dentro.

Un aviso sobre el comando, que es la pieza que peor ha envejecido: los comandos
personalizados y las skills **se han fusionado**. Un archivo en
`.claude/commands/` y una skill del mismo nombre crean el mismo comando, y si
coinciden gana la skill. ‹v2.1.296› La página oficial de comandos ya sirve la de
skills. Aquí se cuentan como dos piezas porque la pregunta que las separa sigue
siendo la del eje 1: quién decide. La implementación converge; la decisión, no.

**Subagente** es otra sesión, con su propia ventana de contexto, su propio rol y
su propio presupuesto, que trabaja aparte y te devuelve una conclusión.

**MCP** es un enchufe hacia fuera: una base de datos, una API, un servicio. Lo
que hay al otro lado no vive en tu máquina.

**Plugin** es una caja para repartir cualquiera de las seis anteriores a tu
equipo.

### 1.2.3 · El eje que de verdad las separa

Puestas en fila parecen siete sabores del mismo helado. No lo son. Se separan por
**dos ejes**, y con esos dos ejes se decide casi siempre bien:

**Eje 1: ¿quién decide que esto ocurra?**

- El programa, siempre, pase lo que pase → **hook**
- Tú, a propósito → **comando**
- El agente, si le parece que encaja → **skill**
- Nadie: simplemente está ahí → **CLAUDE.md**

**Eje 2: ¿dónde vive el trabajo?**

- En tu contexto → CLAUDE.md, skill, comando
- En otro contexto → subagente
- Fuera de la máquina → MCP

Casi todos los errores de diseño que verás en un proyecto real son un error en el
eje 1: alguien escribió como instrucción algo que no era negociable. Y como las
instrucciones se interpretan, se cumple el ochenta por ciento de las veces. El
veinte restante es el incidente.

### 1.2.4 · El impuesto de contexto

Aquí está la parte que casi nadie cuenta, y es la que se paga todos los días.

| Pieza | Qué ocupa en contexto | Cuándo se paga |
|---|---|---|
| Hook | Nada. Corre fuera del modelo. | Nunca |
| Comando | Nada hasta que lo invocas | Al invocarlo |
| Skill | Solo su descripción | Descripción siempre, cuerpo al activarse |
| Subagente | Su propia ventana, aparte | En su cuenta |
| **CLAUDE.md** | **El archivo entero** | **Cada turno de cada sesión** |
| MCP | Solo los nombres. Los esquemas van diferidos | Nombres siempre, esquemas al usarlos |
| Plugin | Lo que lleve dentro | Hereda |

La fila en negrita es, casualmente, la que la gente usa por defecto para todo.

Un `CLAUDE.md` de mil líneas es un peaje que pagas en cada turno, hayas usado o
no lo que contiene. Con MCP el reflejo habitual está mal calibrado: por defecto
solo pesan los nombres de las herramientas y los esquemas se traen bajo demanda,
así que desconectar servidores para ahorrar contexto suele ahorrar menos de lo
que crees. Solo se vuelve caro si fuerzas `ENABLE_TOOL_SEARCH=false`. En una
operación real que medimos durante cuatro meses, **por cada token que salía del
modelo entraban veinticuatro**. El módulo 10 tiene los números completos.

Y ahora el número que falta, porque hasta aquí la tabla es un modelo mental.
Medido con el patrón de la casa: misma petición, mismo repositorio, variando una
sola cosa. ‹v2.1.296›

| Qué se mide | Tokens de entrada |
|---|---:|
| Un directorio vacío, petición trivial | 35.460 |
| El repositorio del laboratorio, petición trivial | 35.458 |
| El repositorio del laboratorio, la pregunta del laboratorio | **147.176** |

Las dos primeras filas son el mismo número con dos tokens de diferencia, y eso
ya dice algo: **un repositorio de siete archivos y 5.830 bytes no cuesta nada
por estar ahí**. Lo que cuesta es mirarlo. De los 147.176, **35.458 son el suelo
del arnés** antes de leer un solo archivo tuyo, y los otros **111.718 son la
exploración**: nueve lecturas y diez turnos reenviando un contexto que crece.

Ese es el impuesto que nadie presupuesta. No lo paga tu código por ser grande:
lo paga el agente por ir a buscarlo. Y el suelo no se hereda del libro, que el
mismo método dio 42.540 tokens en la máquina y la versión del módulo 12.

Elegir bien no es elegancia de arquitecto. Es tu factura.

### 1.2.5 · Señales de que elegiste mal

El árbol se baja una vez y se vive con la decisión meses. Casi ningún error se
presenta como tal: se presenta como una molestia que se aguanta.

| Lo que notas | Lo que pasó | Vuelve a |
|---|---|---|
| "A veces lo hace y a veces no" | pusiste como instrucción algo no negociable | 01, hook |
| El `CLAUDE.md` no para de crecer | metes procedimientos ocasionales donde se paga siempre | 04, skill |
| La skill nunca se activa sola | la descripción no dispara, reescríbela con tus palabras | 04, skill |
| La sesión se queda sin contexto | empieza por el tamaño del `CLAUDE.md` y confírmalo con `/context` | la tabla del impuesto |
| El subagente devuelve algo inservible | no comparte tu contexto: lo que no le pasaste, no lo tiene | 06, subagente |
| A tu compañero no le funciona | lo tienes suelto en vez de empaquetado | 07, plugin |

La primera fila es la mitad de los casos que verás en un proyecto real.

---

## 1.3 · Receta

### 1.3.1 · Lámina 1 · El árbol, en orden

Baja por las preguntas y **para en el primer sí**. El orden va de menos
negociable a más flexible, a propósito: lo que no se puede dejar al criterio de
nadie se resuelve antes de que aparezca la tentación de resolverlo con un prompt.

**01. ¿Tiene que ocurrir siempre, sin que el modelo pueda saltárselo? → HOOK**
Prueba rápida: si te vale con "casi siempre", no es un hook. Si no te vale, lo es.

**02. ¿Necesita datos o acciones que viven fuera de esta máquina? → MCP**
Si lo que quieres es que trabaje mejor con lo que ya tiene delante, no es un MCP.

**03. ¿Es contexto necesario en todas las tareas del repositorio? → CLAUDE.md**
Prueba rápida: si en la mitad de las tareas ese texto sobra, no va aquí.

**04. ¿Es un procedimiento ocasional que el agente puede reconocer? → SKILL**
La descripción es el disparador. Escríbela con las palabras con las que pedirías
la tarea, no con las que usarías para documentarla.

**05. ¿Lo lanza siempre una persona, con las mismas instrucciones? → COMANDO**
La diferencia con la skill es quién decide. ¿Te fías de que se active solo?

**06. ¿Necesita contexto limpio, otro criterio, o va a hacer mucho ruido? → SUBAGENTE**
El precio es que no comparte tu contexto. Lo que no le pases, no lo tiene.

**07. ¿Ya funciona y lo quiere tu equipo? → PLUGIN**
Nunca es la respuesta a "cómo hago esto". Siempre es la respuesta a "cómo hago
que los demás también lo tengan".

**¿Ningún sí?** Entonces no necesitas configurar nada: necesitas escribir mejor la
instrucción. Una parte incómodamente grande de las configuraciones de cualquier
proyecto existe para compensar peticiones mal formuladas, y sale mucho más cara
que reescribirlas.

### 1.3.2 · Versión equipo

En solitario, el árbol es una ayuda. En equipo, es una **norma escrita**, porque
si cada persona decide distinto acabáis con cinco sistemas que se pisan.

Lo mínimo que hay que acordar por escrito, en una reunión de treinta minutos:

1. Qué va en el `CLAUDE.md` del repositorio y qué no. Con criterio, no con gusto.
2. Qué hooks son obligatorios para todos y quién los mantiene.
3. Qué servidores MCP están aprobados. Lista blanca, no lista negra.
4. Quién puede añadir skills al repositorio y quién las revisa.
5. Dónde vive todo eso versionado.

El punto 5 no es burocracia: si la configuración no está en el repositorio, no
existe. Está en el portátil de alguien.

### 1.3.3 · Los cinco niveles de madurez

Sirve para saber por dónde empezar y, sobre todo, para no saltarse peldaños.

| Nivel | Cómo se reconoce | Lo que falta |
|---|---|---|
| **1 · Copiloto** | Lo usas como un chat que además edita archivos | Memoria: se lo cuentas todo cada vez |
| **2 · Configurado** | Tienes `CLAUDE.md` y permisos decididos | Determinismo: lo importante sigue siendo una sugerencia |
| **3 · Determinista** | Hay hooks. Lo no negociable ya no se negocia | Reparto: solo funciona en tu máquina |
| **4 · Repartido** | El equipo comparte plugins y skills versionadas | Medición: nadie sabe qué cuesta |
| **5 · Medido** | Hay presupuesto, telemetría y revisión periódica | Nada. Aquí se vive bien |

La mayoría de los equipos que se creen del nivel 4 están en el 2 con más
archivos. La prueba es sencilla y está en el laboratorio.

### 1.3.4 · Test de autodiagnóstico

Seis preguntas. Cuenta los sí.

1. ¿Existe un `CLAUDE.md` en el repositorio, versionado, escrito en los últimos
   tres meses?
2. ¿Hay al menos un hook que impida algo que no quieres que pase nunca?
3. ¿Están los permisos decididos en un archivo, y no a base de ir contestando?
4. ¿Un compañero puede clonar el repositorio y tener tu misma configuración?
5. ¿Sabes cuánto gastaste el mes pasado?
6. ¿Hay algo que el agente **no** pueda hacer aunque tú se lo pidas?

**0-1 sí:** nivel 1. Empieza por el módulo 3.
**2-3 sí:** nivel 2. Tu siguiente módulo es el 5, hooks.
**4-5 sí:** nivel 3 o 4. Ve al módulo 9 y al 10.
**6 sí:** nivel 5. Salta a los casos completos del módulo 12.

---

## 1.4 · Laboratorio · Primer contacto con el repo feo

A partir de aquí, todo el libro ocurre sobre el mismo repositorio:
`gestor-pedidos`, una aplicación interna de una cárnica, escrita en 2019 por
alguien que ya no trabaja allí. 222 líneas, siete archivos, cero tests.

No es un ejemplo de juguete. Es lo que hay.

**Paso 1.** Abre el repositorio y pide un resumen, sin más contexto:

```
Explícame qué hace esta aplicación y cuáles son sus endpoints.
```

**Paso 2.** Lee la respuesta con atención. Es buena. Es clara. Está bien
estructurada.

**Paso 3.** Ahora comprueba, uno por uno, los endpoints que te ha listado
contra el código de `app.py`.

### Lo que va a pasar

Cuando escribimos este laboratorio dábamos por hecho que el agente leería el
`README.md`, se lo creería y te listaría un endpoint `POST /anular` que no existe
desde que se documentó en 2021.

Lo probamos. **No pasa eso.** Lo dejamos escrito porque equivocarse en público es
parte del trato de este libro, y porque lo que pasa de verdad es más útil.

Lo que hace el agente es leer el código, listar los cuatro endpoints que existen
de verdad, y **decirte por su cuenta que tu README miente**: que anuncia un
`POST /anular` que no está y que se calla un `/pedido_old/<id>` que sí está
expuesto. Nadie le ha pedido que audite la documentación. Le has pedido un
resumen.

Y aquí están las dos lecciones del módulo, que valen más que la sorpresa que
esperábamos:

**Primera: tu documentación es un pasivo, no un activo.** En este repositorio hay
tres documentos que se contradicen entre sí. El agente los ve todos y ninguno le
dice cuál gana. Tuvo que ir al código para resolver el empate, y eso lo pagaste
en tokens. Decidir por escrito qué fuente manda es el trabajo del módulo 3, y
empieza a ahorrar dinero desde el primer turno.

**Segunda, y más incómoda: te ha contestado más de lo que preguntaste.** Eso hoy
te ha venido bien. Pero un agente que decide por su cuenta ampliar el encargo es
el mismo mecanismo que un día refactoriza tres archivos que nadie le pidió tocar.
No es un fallo que haya que corregir, es una propiedad que hay que **acotar**, y
acotarla es lo que hacen los módulos 4 y 5.

**Lo volvimos a medir para esta edición.** Cuatro pasadas con la 2.1.296, misma
pregunta y mismo repositorio: **cuatro de cuatro** listaron los cuatro endpoints
que existen, señalaron el `POST /anular` que el README anuncia y no está, y el
`/pedido_old/<id>` que está expuesto y el README se calla. ‹v2.1.296› El
experimento original está en `evidencias/EXP-001` y la ficha que lo vigila es
`FUN-001`.

Una de las cuatro salió más barata, y explica por qué la factura de un
laboratorio es un rango. **Tres pasadas costaron 147.176 tokens de entrada, al
token.** La cuarta, 111.165. No cambió el repositorio ni la pregunta: cambió el
camino. En tres el agente intentó leer los siete archivos de una vez con un
comando de consola, se lo denegaron, y los leyó de uno en uno gastando un turno
más. Mismo resultado, **un 32 % más de tokens**: entre dos pasadas idénticas lo
que varía no es lo que sabe, es por dónde lo busca.

**Paso 4.** Anota las contradicciones que aparezcan. Vas a necesitar esa lista en
el módulo siguiente. Hay al menos tres a la vista, y una cuarta que solo se ve
leyendo el código con cuidado.

---

## 1.5 · Prueba

**PASA** si al terminar tienes escrita una lista de al menos tres contradicciones
del repositorio, y para cada una sabes decir **qué archivo debería ganar el
empate**.

**FALLA** si tu lista es un resumen de lo que dijo el agente. El ejercicio no es
recoger su respuesta: es decidir tú cuál de tus archivos dice la verdad. Esa
decisión no la puede tomar por ti, y es exactamente lo que vas a escribir en el
módulo 3.

> **Esto va a cambiar.** Lo que el agente detecta por su cuenta depende de la
> versión del CLI y del modelo. Nuestra prueba es del 12 de agosto de 2026 con la
> 2.1.228, está documentada en `evidencias/EXP-001` y se repite cada trimestre:
> el 11 de octubre de 2026, con la 2.1.296, volvió a salir cuatro de cuatro.
> ‹v2.1.296›
>
> Coincidir dos trimestres no la convierte en garantía. En este mismo libro hay
> una afirmación vecina que se cayó: que el agente **nombre** la inyección
> escondida en ese README se midió tres de tres con la 2.1.228 y **cero de diez**
> diecinueve días después con la 2.1.251. Lo que se cumple porque el modelo
> decidió bien no es un límite, es una suerte repetida. Si tu resultado no
> coincide, el dato es tuyo y nos interesa.

---

## 1.6 · Coste de este módulo

| Concepto | Cantidad |
|---|---|
| Tokens de entrada del laboratorio | **147.176, medidos** |
| De ellos, suelo del arnés | 35.458 |
| De ellos, la exploración | 111.718 |
| Tokens de salida | ~2.650 |
| Coste medido por el CLI | 0,09 dólares en frío · 0,04 con la caché caliente |
| Coste en euros | por debajo de 0,10 € |
| Tiempo | 15 minutos |
| **Impuesto de contexto permanente** | **0 tokens** |
| Mantenimiento continuo | ninguno |

La penúltima fila es la que importa, y este es el único módulo del libro que
puede escribirla así. No te deja nada en el contexto: ni un `CLAUDE.md`, ni un
servidor, ni una skill. Te deja una decisión tomada, y las decisiones no viajan
en el prompt. A partir del módulo 3 cada pieza que montes tendrá su fila aquí y
su número por turno, y por eso el árbol va primero: **sale más barato elegir
bien que desmontar**.

Y dos cosas sobre la factura de arriba.

**La primera: estaba estimada en 40.000 tokens y son 147.176.** El error no fue
de cálculo, fue de método: se estimó contando lo que pesa el repositorio en vez
de medir lo que cuesta mirarlo. 5.830 bytes de código fuente generaron 147.176
tokens de entrada, porque el gasto no está en el archivo, está en los turnos que
hacen falta para recorrerlo.

**La segunda: el coste en dólares de la misma ejecución varió más del doble**,
entre 0,04 y 0,09, sin cambiar una palabra de la petición. Lo que cambió fue la
caché: la primera pasada la crea y la paga, las siguientes la leen. Una cifra de
coste que no dice en qué estado estaba la caché cuenta media historia.

---

## Runbook · Módulo 01

> **Lámina 1 · El árbol, en orden. Para en el primer sí.**
>
> 1. ¿Siempre, sin excepción? → **hook**
> 2. ¿Fuera de la máquina? → **MCP**
> 3. ¿En todas las tareas? → **CLAUDE.md**
> 4. ¿Solo a veces, y se reconoce solo? → **skill**
> 5. ¿Lo lanzo yo a mano? → **comando**
> 6. ¿Contexto limpio u otro criterio? → **subagente**
> 7. ¿Ya funciona y lo quiere el equipo? → **plugin**
> 8. ¿Ningún sí? → **reescribe la instrucción**
>
> **Los dos ejes, si el árbol no decide solo**
> Quién lo dispara: el programa → hook · tú → comando · el agente → skill ·
> nadie → `CLAUDE.md`.
> Dónde vive: tu contexto → `CLAUDE.md`, skill, comando · otro → subagente ·
> fuera → MCP.
>
> **Qué se paga en cada turno**
> El `CLAUDE.md` se paga entero, siempre. MCP paga solo los nombres de sus
> herramientas: los esquemas van diferidos y se traen al usarlos. Hook y
> comando, cero. Skill, su descripción.
> Medido en producción: 24 tokens de entrada por cada token de salida.
>
> **Si elegiste mal, se nota así**
>
> "A veces sí y a veces no" → 01, hook · El `CLAUDE.md` no para de crecer →
> 04, skill · La skill no se activa sola → la descripción, no el cuerpo · Se
> queda sin contexto → el tamaño del `CLAUDE.md`, con `/context` · El subagente
> no sirve → lo que no le pasaste, no lo tiene · A tu compañero no le va →
> 07, plugin. La tabla entera, en 1.2.5.
>
> **Por dónde seguir, contando los sí del test de 1.3.4**
> 0-1 → módulo 3 · 2-3 → módulo 5 · 4-5 → módulos 9 y 10 · 6 → módulo 12.
>
> **Antes de presupuestar nada, mide tu suelo**
> ```
> claude -p "Responde solo con la palabra OK." --output-format json
> ```
> Suma `input_tokens` + `cache_creation_input_tokens` +
> `cache_read_input_tokens`. Dos veces: si no coinciden, no te lo creas.
> En esta máquina con la 2.1.296: 35.458 en el laboratorio y 35.460 en un
> directorio vacío. El suelo se mide, no se hereda.
>
> **Si algo se cumple "casi siempre", está en el sitio equivocado.**
