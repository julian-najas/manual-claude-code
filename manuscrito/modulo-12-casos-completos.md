# Módulo 12 · Casos completos

> **Laboratorio de este módulo:** ~55 minutos · veinte invocaciones del CLI,
> doce de ellas con el JSON conservado: **9.263.966 tokens de entrada** y 80.315
> de salida · **3,77 dólares** sumando lo que devolvió cada ejecución, que a
> cualquier cambio euro dólar de agosto de 2026 se queda **por debajo de
> 4,25 €**. Con suscripción va incluido.
> **Verificado contra:** Claude Code 2.1.258 · 2 de septiembre de 2026.

> **Nota de versión.** Es el módulo que más código toca y el que menos depende
> de la versión: lo que se mide es qué hace el agente con una decisión que nadie
> escribió, y eso no lo arregla un parche.

---

## 12.1 · Síntoma

"Vale, ¿y todo junto?"

Has terminado los once módulos. Tienes un `CLAUDE.md` que dice la verdad,
permisos versionados, dos hooks, una skill, un servidor MCP de solo lectura, un
subagente revisor, CI que falla cuando debe y trece pruebas. Cada pieza,
probada en su módulo, funciona.

Y el lunes te toca la tarea de verdad: **desmontar la función que hace ocho
cosas**, esa que todo el mundo evita, la que lleva desde 2019 sin que nadie se
atreva. Abres la sesión, escribes "desmonta `procesar_pedido()`", y a los dos
minutos tienes un diff de ciento setenta líneas.

Ahí está el módulo entero, en la pregunta que viene después: **¿qué haces con
ese diff?** No es un problema de calidad del cambio. Casi siempre está bien.
Es que **no sabes qué ha decidido por ti dentro de esas ciento setenta
líneas**, y hay decisiones ahí dentro que no le tocaban a él.

---

## 12.2 · Modelo mental

### 12.2.1 · Hay dos trabajos dentro de cada tarea, y solo uno se puede delegar

La distinción que ordena el módulo. En toda tarea real conviven:

**El trabajo mecánico.** Extraer siete funciones de un cuerpo de sesenta
líneas. Mover valores de un archivo a otro. Tiene una respuesta correcta, se
deduce del código que hay delante, y es verificable: o el comportamiento se
conserva o no.

**La decisión.** ¿Qué IVA se le cobra a un pedido de Francia? ¿Se acumulan los
dos descuentos por cantidad? ¿Manda el archivo de 2019 o el de 2021? No se
deduce de nada: alguien tiene que decidirlo, y ese alguien no está en el
repositorio.

Medido sobre el mismo `app.py`, dos repeticiones por fila, con herramientas de
edición y sin `Bash`:  ‹v2.1.258›

| Tarea | Repetible entre ejecuciones | Comportamiento conservado |
|---|---|---|
| Desmontar `procesar_pedido()` | **Sí**, siete funciones con los mismos nombres las dos veces | Sí, las once pruebas siguen pasando |
| Arreglar el IVA por países | Sí, y ahí está el problema | **No**, y decidió él |

La primera fila es tranquilizadora: dos ejecuciones independientes extrajeron
`validar`, `subtotal_lineas`, `aplicar_iva`, `descuento_cliente_antiguo`,
`guardar`, `notificar` y `facturar`, con una sola diferencia de nombre entre
ambas. **La refactorización es la parte segura.**

### 12.2.2 · Lo que hace cuando la decisión no está escrita

La medición que da nombre al módulo. La petición fue esta, y no menciona qué
hacer con los demás países:

```text
Hoy, a cualquier pais que no sea ES ni PT, esta aplicacion le cobra el IVA
espanol del 21 por ciento. Es un fallo. Arreglalo en el codigo.
```

**Cinco ejecuciones de cinco, en dos formulaciones distintas, tomaron la misma
decisión: cero por ciento de IVA fuera de España y Portugal.**  ‹v2.1.258› En
dos de ellas borró además el comentario `# revisar con gestoria`, que era el
único sitio del repositorio donde constaba que la pregunta seguía abierta.

```text
    # fuera de ES y PT no se aplica IVA español: no hay tipo definido para
    # otros países, así que no se recarga nada
```

Está bien redactado, es defendible, y **nadie con autoridad para decidirlo lo ha
decidido**. Un tipo impositivo que se aplica a facturas reales salió de un turno
de un agente al que se le pidió arreglar un fallo.

> Fíjate en lo que **no** pasó: no se equivocó, no alucinó y no rompió nada. El
> diff es correcto en todo lo que se le pidió. **Contestó una pregunta que no se
> le hizo**, porque para terminar la que sí se le hizo tenía que contestarla, y
> preguntar no estaba entre sus opciones.

### 12.2.3 · Una frase cambia el resultado, y sale más barata

La misma petición con una frase añadida al final:

```text
Si el arreglo necesita una decision de negocio que no esta escrita en el
repositorio, NO la tomes tu: no edites nada y dime cual es la decision que falta.
```

Dos repeticiones por fila, mismo repositorio, misma versión:  ‹v2.1.258›

| Petición | Archivos tocados | Pruebas rojas | Tokens de entrada | Coste |
|---|---|---:|---:|---:|
| "Arréglalo" | `app.py` | 2 | 239.730 · 234.954 | 0,113 $ · 0,107 $ |
| "Arréglalo, y la decisión no la tomas tú" | **ninguno** | **0** | **140.948 · 139.740** | **0,089 $ · 0,085 $** |

Cuarenta y un por ciento menos de tokens de entrada, y lo que devuelve es la
pregunta bien formulada: si los pedidos de fuera van sin IVA, o si hay que
aplicar el tipo del país de destino, y que entonces hace falta una tabla que hoy
no existe en ningún archivo.

**No es prudencia, es que trabajar cuesta.** Un agente que se para antes de
editar se ahorra el ciclo entero de escribir, releer y comprobar. La
instrucción que evita el riesgo es también la que evita el gasto, y es la única
vez en el libro que esas dos cosas coinciden.

### 12.2.4 · La red de pruebas cuelga de una costura, y una refactorización correcta la arranca

Lo peor del módulo, y la única medición cuyas dos repeticiones **no
coincidieron**. Misma petición, unificar `config.py` y `settings.py`, dos
ejecuciones seguidas:  ‹v2.1.258›

| | Comportamiento de la aplicación | Pruebas |
|---|---|---|
| Primera | Idéntico | **11 pasan** |
| Segunda | Idéntico | **11 dan ERROR** |

Las dos hicieron un trabajo correcto. Las dos conservaron los valores que
estaban en ejecución, `MAX_LINEAS` en 50 y no el 100 del archivo nuevo. La única
diferencia está en dos líneas:

```python
# Primera ejecución            # Segunda ejecución
DB = config.DB_PATH            def conexion():
def conexion():                    return sqlite3.connect(config.DB_PATH)
    return sqlite3.connect(DB)
```

La segunda es más limpia. Y borra el nombre `app.DB`, que es por donde el
fixture de las pruebas agarra la aplicación con un `monkeypatch` para trabajar
contra una base de datos de usar y tirar. Sin ese nombre, las once revientan en
el montaje.

> **Once errores no son once fallos.** Un paso de CI que busque `failed` en la
> salida de `pytest` encuentra **cero**. La aplicación funciona exactamente
> igual: lo que se ha roto es el instrumento con el que ibas a comprobarlo, y se
> rompió en el mismo commit en el que ibas a necesitarlo.

Una costura (seam) es un punto por el que el código deja que lo agarren desde
fuera sin cambiar lo que hace. No se ve leyendo el código de producción: se ve
leyendo las pruebas. **Antes de aceptar una refactorización, mira si sigue
existiendo el nombre del que cuelga.**

### 12.2.5 · Por qué la receta oficial no basta aquí

La documentación oficial trae una receta de refactorización de cuatro pasos, y
es buena: identificar, pedir recomendaciones, aplicar **conservando el
comportamiento**, y verificar corriendo las pruebas  ‹v2.1.258›. La receta de
pruebas, dos secciones más abajo, termina en un paso que sobre una red de
caracterización es exactamente el movimiento equivocado: *"corre las pruebas
nuevas y arregla los fallos"*.

Sobre una prueba de caracterización, **el fallo es el entregable**. Las cinco
`test_hoy_` que el módulo 09 dejó puestas no describen lo que la aplicación
debería hacer: describen lo que hace. Que se pongan rojas es el trabajo que
hacen. Arreglarlas, en el sentido de tocar la aserción hasta que vuelvan a
pasar, borra la única prueba que tenías de que el cambio ocurrió.

---

## 12.3 · Receta

### 12.3.1 · Individual: el caso completo en cinco pasos

Vale para cualquier tarea que toque comportamiento. El orden importa.

**Paso 1. Congela lo que hace hoy, antes de leer nada.** Si no hay pruebas de
caracterización, ese es el trabajo del día y no la refactorización. Se escriben
con el prefijo `test_hoy_` y con el enunciado en presente: *"hoy a Francia se le
cobra el IVA español"*, no *"debe cobrarse"*.

**Paso 2. Separa las decisiones antes de pedir nada.** Lee el diff que **no**
existe todavía: recorre el código y anota cada sitio donde hay una pregunta sin
contestar. Los comentarios las señalan solos. En el laboratorio eran tres:
`# revisar con gestoria`, `# ojo: esto no se acumula con el de arriba? nadie lo
sabe` y `¿cuál manda? nadie lo sabe`.

**Paso 3. Pide el trabajo mecánico con el freno puesto.** Siempre con las dos
condiciones, que son la diferencia medida en 12.2.3:

```text
El comportamiento no puede cambiar. Si el arreglo necesita una decision de
negocio que no esta escrita en el repositorio, NO la tomes tu: para y dime
cual es.
```

**Paso 4. Decide tú, y escríbelo donde se lea.** No en el mensaje del commit: en
un archivo del repositorio. La decisión y **por qué**, que es lo que nadie
apunta y lo que se pregunta dentro de dos años.

**Paso 5. Aplica la decisión y deja que la red se ponga roja.** Las pruebas que
fijaban el comportamiento viejo tienen que fallar. Se borran y se escriben las
del comportamiento nuevo. **No se edita su aserción**, porque una prueba
reescrita a mano hasta que pasa no ha comprobado nada.

### 12.3.2 · Equipo: dónde viven las decisiones

Un procedimiento individual no sobrevive a un equipo. Lo que sí, es que el
repositorio tenga un sitio con nombre.

| Archivo | Qué contesta | Coste por turno |
|---|---|---:|
| `CLAUDE.md` | Cómo es el proyecto hoy | Se paga entero, cada turno |
| `DECISIONES.md` | Por qué es así, y quién lo decidió | **0** |
| `tests/test_caracterizacion.py` | Qué pasa si alguien lo cambia | 0 |

La fila del medio es la barata y la que nadie tiene. **`DECISIONES.md` no es
memoria: es un archivo que el agente abre cuando le hace falta**, y por eso no
paga impuesto de contexto. Medido: añadirlo al laboratorio cambió el gasto por
turno en **17 tokens**, y esos diecisiete son de la tabla del `CLAUDE.md`, no
del archivo nuevo.  ‹v2.1.258›

Tres reglas para que sirva:

1. **Una entrada por decisión, no por cambio.** Para eso está el historial.
2. **Se escribe también cuando se decide no cambiar nada.** La entrada de los
   descuentos acumulados no cambia una línea de comportamiento, y es la más
   útil de las cuatro: convierte un accidente de 2019 en una decisión de 2026.
3. **Lo que sigue sin decidirse va dentro, con su nombre.** Un archivo de
   decisiones que solo tiene decisiones tomadas miente por omisión.

### 12.3.3 · Cómo se revisa un diff de ciento setenta líneas

Tres pasadas, en este orden, y ninguna es leer el diff entero de arriba abajo.

**Primera, las pruebas.** Antes que el código. Si alguna cambió de contenido,
ahí está la discusión. Si el recuento cambió, ahí está el cambio de
comportamiento. Y si salen **errores en vez de fallos**, es la costura de
12.2.4.

**Segunda, los comentarios que desaparecieron.** `git diff` con las líneas
borradas, buscando las que empiezan por `#`. Un comentario que decía que algo
estaba sin decidir y que ya no está es la señal más fiable de que se decidió sin
avisar. En el laboratorio, dos de cinco ejecuciones se llevaron por delante
`# revisar con gestoria`.

**Tercera, los literales.** Números y cadenas que cambiaron de valor, no de
sitio. Mover `50` de `app.py` a `config.py` es mecánico; convertirlo en `100`
porque lo decía el archivo más nuevo es un cambio de producto disfrazado de
limpieza.

---

## 12.4 · Laboratorio · Tres recorridos completos

Los tres van seguidos, sobre `gestor-pedidos`, y en este orden a propósito: el
que no decide nada primero, el que decide después.

### Caso A · Desmontar la función de ocho responsabilidades

**Paso 1.** Corre las once pruebas y **guarda la salida**. Es tu única
referencia.

**Paso 2.** Pide el desmontaje con el freno puesto:

```bash
claude -p "La funcion procesar_pedido() de app.py hace demasiadas cosas. Desmontala en funciones con una sola responsabilidad cada una. El comportamiento no puede cambiar." \
  --allowedTools "Read,Glob,Grep,Edit" --output-format json 2>errores.txt
```

**Paso 3.** Cuenta las responsabilidades antes de mirar el resultado, y después
compara. Dos de dos salieron siete: validar, sumar líneas, IVA, descuento de
cliente antiguo, guardar, notificar y facturar. La octava se queda en
`procesar_pedido()`, que ahora hace **una** cosa: poner las otras siete en
orden.

**Paso 4.** Corre las once. Pasan. Este caso no tiene sorpresa, y esa es la
lección: **con la red puesta, la refactorización es la parte aburrida del día.**

### Caso B · El IVA por países, que es donde está el módulo

**Paso 5. Pídelo mal a propósito, una vez.** El comando de 12.2.2, sin la frase
del freno, sobre una copia. **Va a decidir por ti**, y verlo una vez en tu
propio repositorio vale más que este párrafo.

**Paso 6. Comprueba qué se puso rojo.** Dos, y son las dos correctas:

```text
FAILED tests/test_caracterizacion.py::test_hoy_a_francia_se_le_cobra_el_iva_espanol
FAILED tests/test_caracterizacion.py::test_hoy_sin_pais_tambien_se_cobra_el_iva_espanol
2 failed, 9 passed
```

La red funciona: te dice **que** el comportamiento cambió y **cuál**. Lo que no
te dice, y no puede, es si el nuevo es el correcto.

**Paso 7. Tira ese cambio y pídelo con el freno.** Cero archivos tocados, once
pruebas pasando, y una respuesta que nombra la decisión que falta. Así se
termina la jornada cuando quien decide no está.

**Paso 8. Decide, y escribe el porqué.** Dos decisiones, y las dos van a
`DECISIONES.md`:

- **Un país sin tipo se rechaza.** Los tipos pasan a `config.IVA_POR_PAIS` con
  cuatro países, y lo que no está en la tabla devuelve **400 con el país en el
  cuerpo** y un `WARNING` en el registro. Lo importante no es la tabla: es que
  **"no sé de qué país es" ha dejado de ser un sinónimo de "es de España"**.
- **Los descuentos se acumulan.** No porque acumular sea lo correcto, sino
  porque **es lo que llevaba pasando cinco años** y un cambio de precios no se
  cuela dentro de una refactorización.

Y escribe también lo que rompe, que es la mitad que nadie apunta: **todo pedido
que hoy llegue sin el campo `pais` deja de crearse**. El arreglo del código es de
una línea; el despliegue, no.

**Paso 9. Sustituye las pruebas, no las edites.** Las dos `test_hoy_` se borran
y en su sitio van seis: los cuatro países de la tabla, un país que no está en
ella, y un pedido sin país. Los números esperados se escriben a mano, no se
calculan leyendo la misma tabla que usa la aplicación: **una prueba que lee la
tabla del código no comprueba la tabla, la copia.**

Y una que solo cambia de nombre: `test_hoy_los_dos_descuentos_de_cantidad_se_
acumulan` pierde el `hoy_` y gana un `_a_proposito`. No cambia ni una aserción.
**El nombre es la mitad del valor de una prueba**: dice si lo que fija es lo que
pasa o lo que queremos que pase.

### Caso C · La configuración duplicada, y la costura

**Paso 10.** Unifica `config.py` y `settings.py`. Se conservan los valores que
estaban **en ejecución**: 50 y no 100, `True` y no `False`. `settings.py` se
borra.

**Paso 11. Corre las pruebas y mira si son fallos o errores.** Aquí es donde
salta 12.2.4. Si son once errores en el montaje, busca en el diff el nombre
`DB`: alguien lo ha metido dentro de `conexion()` y la red se ha quedado
colgando. La aplicación va perfecta. Tu forma de saberlo, no.

**Paso 12. Actualiza el `CLAUDE.md` en el mismo commit.** Decía, con razón, que
no había configuración en uso. Ha dejado de ser verdad **con el código, no
después**. Un `CLAUDE.md` que describe el repositorio de la semana pasada es
contexto equivocado que se paga en cada turno.

**Paso 13. Las trece en verde.** Once de caracterización y las dos de
diagnóstico del módulo 11.

---

## 12.5 · Prueba

**PASA** si se cumplen las cuatro:

1. Las pruebas **cubren los cuatro países** de la tabla, más el país que no está
   en ella y el pedido sin país. Trece en verde.
2. **El descuento acumulado está decidido y escrito**, con el porqué, y su
   prueba ya no se llama `test_hoy_`.
3. El comportamiento **no cambió en ningún sitio salvo donde se decidió**, y lo
   demuestras con las nueve pruebas que no tocaste.
4. Tienes guardada **una ejecución en la que el agente decidió por ti** y sabes
   señalar la línea. Sin ella, este módulo lo has leído, no lo has hecho.

**FALLA** si alguna prueba pasó de roja a verde porque le cambiaste la
aserción. También **FALLA** si tu comprobación de CI busca `failed` en la salida
de `pytest`: once errores en el montaje dan **cero fallos** y verde.

> **Esto va a cambiar.** Los nombres que extrae y el reparto exacto de las siete
> funciones dependen de la versión y del modelo, y la cifra de coste de un
> refactorado envejece en semanas. Lo que no esperamos que cambie es el hallazgo
> de 12.2.2: mientras preguntar no sea una opción disponible, **un agente al que
> le falta una decisión para terminar la va a tomar**. Y no por un fallo de
> alineamiento, sino porque le has pedido que termine.

---

## 12.6 · Coste de este módulo

Las once ejecuciones de las que se conservó el JSON:

| Concepto | Cantidad |
|---|---:|
| Tokens de entrada | 9.263.966 |
| De ellos, servidos desde caché | 8.974.615 (**96,9 %**) |
| Tokens de salida | 80.315 |
| **Relación entrada / salida** | **115 a 1** |
| Coste, sumando lo que devolvió el CLI | 3,77 $ |
| Coste en euros | por debajo de 4,25 € |
| Invocaciones totales del CLI | 20 |
| Tiempo | 55 minutos |

Los 115 a 1 colocan este módulo entre los dos extremos del libro:

| Actividad | Entrada por token de salida |
|---|---:|
| Diagnóstico, módulo 11 | 468 a 1 |
| **Cambiar código con red, este módulo** | **115 a 1** |
| Auditoría de seguridad, módulo 10 | 90 a 1 |
| Operación multiagente de cuatro meses, `D4-factura/` | 24 a 1 |

**Escribir código es lo más equilibrado que se le puede pedir**, porque es lo
único donde lo que sale es tan grande como para notarse. Y aun así entran ciento
quince por cada uno que sale.

La comparación que rompe la intuición:

| Cómo se pidió | Coste |
|---|---:|
| Los tres casos en una sola petición, tres repeticiones | 0,53 $ · 0,78 $ · 0,84 $ |
| Los tres por separado | 0,18 $ + 0,11 $ + 0,39 $ = 0,68 $ |

Las tres repeticiones del "todo junto" **no coinciden entre sí**: un 59 % de
diferencia entre la más barata y la más cara con la misma petición y el mismo
repositorio, que es la caché otra vez, como en el módulo 09 y en el 10. Y el
total de pedirlo por separado cae **dentro de esa horquilla**. De ahí la
conclusión honesta: **el argumento contra pedirlo todo junto no es el dinero.**
Es que las tres tomaron exactamente la misma decisión silenciosa sobre el IVA, y
la enterraron en un diff de tres archivos que hay que revisar entero para
encontrarla.

Lo que este módulo deja instalado y lo que cuesta mantenerlo:

| Pieza | Coste por turno | Mantenimiento |
|---|---:|---|
| `DECISIONES.md` | **0** | Una entrada cuando se decide algo |
| Las cuatro pruebas nuevas de país | 0 | Rojas cuando cambie un tipo, que es lo que deben hacer |
| Tabla del `CLAUDE.md` reescrita | 17 | Releerla cuando cambie `config.py` |

Diecisiete tokens por turno es lo que cuesta el módulo entero, y el impuesto del
laboratorio completo queda en **1.796 tokens**, contra los 1.779 de esta mañana
y los 1.781 que midió el módulo 09 contra la 2.1.247. **Once versiones de
parche y dos tokens de diferencia:** el impuesto de contexto se puede
presupuestar, y este libro lleva cuatro módulos demostrándolo.

El coste que no está en ninguna tabla es el de la decisión que se tomó sola. Una
factura con el IVA mal es cara de dos maneras: la primera se paga a la gestoría
y la segunda a un abogado. **Ninguna de las dos aparece en `total_cost_usd`.**

Y con esto el repositorio de 2019 tiene lo que no tenía en el módulo 01:
memoria, límites, determinismo, un revisor, una red y un sitio donde consta
quién decidió qué. Lo que sigue sin tener es alguien a quien preguntar cuando
falta una decisión, y ninguna herramienta de este libro lo va a resolver. Por
eso el cierre del libro no es un módulo más, sino el modo escéptico.

---

## Runbook · Módulo 12

> **Antes de tocar comportamiento**
> 1. ¿Hay pruebas de caracterización? Si no, **ese es el trabajo de hoy**, no la
>    refactorización.
> 2. Se llaman `test_hoy_` y su enunciado va en presente: fijan lo que pasa, no
>    lo que debería pasar.
> 3. Corre las pruebas y **guarda la salida**. Es tu única referencia.
>
> **Las dos frases que van en cada petición**
> ```text
> El comportamiento no puede cambiar. Si el arreglo necesita una decision de
> negocio que no esta escrita en el repositorio, NO la tomes tu: para y dime
> cual es.
> ```
> Medido: **cero archivos tocados** frente a uno, y **41 % menos de tokens de
> entrada**. La instrucción que evita el riesgo es la que evita el gasto.
>
> **Sin esa frase, decide él**
> Cinco de cinco fijaron el IVA de fuera de ES y PT en **0 %**, sin que nadie
> se lo dijera, y dos borraron el comentario `# revisar con gestoria` que era el
> único rastro de que la pregunta seguía abierta.
>
> **Revisar el diff, en tres pasadas y en este orden**
> 1. **Las pruebas.** ¿Cambió alguna de contenido? ¿Cambió el recuento?
> 2. **Los comentarios borrados.** Un `#` que decía "nadie lo sabe" y ya no está
>    significa que alguien lo decidió sin avisar.
> 3. **Los literales.** Que cambien de sitio es mecánico. Que cambien de valor,
>    no.
>
> **"Todas las pruebas dan ERROR y la app va bien"**
> Se ha llevado por delante una **costura**. En el laboratorio es el nombre
> `app.DB`, del que cuelga el `monkeypatch` del fixture. Meter `config.DB_PATH`
> dentro de `conexion()` es más limpio y deja **11 errores**. Y ojo:
> **11 errores dan cero `failed`**, así que un `grep failed` en CI lo aprueba.
>
> **Cuando la prueba se pone roja**
> Es su trabajo. Se **borra y se escribe la nueva**; no se edita la aserción
> hasta que pase. La receta oficial dice "corre las pruebas y arregla los
> fallos": sobre una red de caracterización, ese paso es el equivocado.
>
> **Dónde va cada cosa**
> `CLAUDE.md` dice **cómo es** el proyecto y se paga cada turno.
> `DECISIONES.md` dice **por qué**, y cuesta **0**: no es memoria, es un archivo
> que se abre cuando hace falta. Ahí van también las decisiones **de no
> cambiar nada**, y las que siguen sin tomarse.
>
> **Unificar dos configuraciones**
> Se conserva lo que estaba **en ejecución**, no lo que decía el archivo más
> nuevo. `MAX_LINEAS = 100` porque lo ponía el de 2021 es un cambio de producto
> disfrazado de limpieza.
