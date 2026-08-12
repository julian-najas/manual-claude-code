# Módulo 01 · Fundamentos y el árbol de decisión

> **Laboratorio de este módulo:** ~15 minutos · unos 40.000 tokens de entrada ·
> por debajo de 0,15 € con un plan de suscripción normal.
> **Verificado contra:** Claude Code 2.1.228 · 12 de agosto de 2026.

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

Elegir bien no es elegancia de arquitecto. Es tu factura.

---

## 1.3 · Receta

### 1.3.1 · El árbol, en orden

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
> 2.1.228, está documentada en `evidencias/EXP-001` y se repite cada trimestre.
> Si tu resultado no coincide, el dato es tuyo y nos interesa.

---

## 1.6 · Coste de este módulo

| Concepto | Cantidad |
|---|---|
| Tokens de entrada del laboratorio | ~40.000 |
| Tokens de salida | ~2.000 |
| Coste con plan de suscripción | incluido |
| Tiempo | 15 minutos |
| Mantenimiento continuo | ninguno |

Este módulo no añade nada a tu contexto permanente: es el único del libro cuyo
impuesto es cero. A partir del módulo 3, cada decisión que tomes tendrá un coste
por turno, y por eso el árbol va primero.

---

## Runbook · Módulo 01

> **El árbol, en orden. Para en el primer sí.**
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
> **Solo dos piezas se pagan en cada turno: CLAUDE.md y MCP.**
> Medido en producción: 24 tokens de entrada por cada token de salida.
>
> **Si algo se cumple "casi siempre", está en el sitio equivocado.**
