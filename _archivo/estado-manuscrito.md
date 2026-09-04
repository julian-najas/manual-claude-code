# Estado del manuscrito

Una entrada por iteración. Dos líneas: qué se cerró y qué queda.

## Cómo se escribe esto ahora · desde el 17-ago-2026

El manuscrito lo escribe una **rutina en la nube**, no el R630. Un módulo al día
a las 08:00 de Madrid (06:00 UTC), modelo Opus 5, sobre este mismo repositorio
clonado desde GitHub.

- Rutina: `trig_01RzL9eHhTvWuejJYqBLgV7Z`
- Panel: https://claude.ai/code/routines/trig_01RzL9eHhTvWuejJYqBLgV7Z
- Para pararla o cambiarla, ahí. No se borra por API.

**Lo que hay que saber para no romperlo:**

1. **El agente clona de GitHub, no ve el R630.** Si trabajas en local, empuja.
   Lo que no esté en `origin/main` no existe para la rutina.
2. **La rutina empuja a `main` cada día.** Si tienes trabajo local sin subir
   cuando termine, te va a tocar rebase.
3. **Guarda de seguridad:** si el agente no encuentra
   `manuscrito/modulo-02-instalacion.md`, para y no escribe nada, en vez de
   escribir un módulo duplicado. Es la red contra un repositorio desincronizado.
4. **08:00 y no 07:00 a propósito:** el flujo `verificar.yml` corre a las 05:00
   UTC, que son las 07:00 de Madrid. Ponerlos a la misma hora hacía que los dos
   empujaran a `main` a la vez.
6. **Una sesión que se muere no deja rastro, y por eso hay un latido.**
   `.github/workflows/latido-rutina.yml` corre a las 21:00 UTC y comprueba que
   el diario tiene entrada de hoy. Si no la tiene, abre incidencia con la
   etiqueta `rutina-callada` y no abre una nueva cada día: comenta en la que ya
   está. Se prueba a mano con `python3 fabrica/latido-rutina.py`.

5. **Nadie contesta a un diálogo de permisos.** La sesión se congela hasta que
   caduca y el día se pierde sin dejar nada escrito. Lo dispara copiar un
   archivo desde `/tmp` hacia dentro del repositorio; escribirlo con un heredoc
   no lo dispara. Está en el paso 0d de la rutina desde el 19-ago-2026.

## 2026-09-04 · Sin módulo · Segundo día sin trabajo pendiente

**La rutina disparó, comprobó y no escribió módulo, porque sigue sin haberlo.**
Los doce están escritos. No lo doy por bueno porque lo dijera la entrada de
ayer: he vuelto a mirar los doce archivos uno a uno y los doce llevan las seis
partes del esqueleto en orden, cabecera con factura del laboratorio y marca de
versión, y runbook de cierre.

Verificador contra la **2.1.260**, versión nueva de hoy y tercer salto en tres
días (2.1.258 el 2, 2.1.259 el 3, 2.1.260 hoy): **93 pasan, 0 fallan, 45 a
revisar, 6 omitidas**. `comprobar-coherencia.py`, sin contradicciones sobre 19
hechos canónicos y 80 archivos. `construir.py --comprobar`, todas las salidas al
día, huella `43b9c8d2`, la misma de ayer. Ningún salto de versión del CLI ha
roto todavía una afirmación publicada.

**Los dos REVISAR nuevos son de la máquina, no del libro, y conviene dejarlo
escrito para que nadie los "arregle".** El `estado.json` que había en el
repositorio decía 95 pasan y 43 a revisar; hoy salen 93 y 45. Los dos que se
mueven son `REPO-002` y `REPO-003`, los dos con `red: true`. Este entorno saca
el HTTPS por un proxy que responde **403** a la URL del companion, y así sale en
el registro: `REPO-002` con `403` y `REPO-003` con `curl: (56) CONNECT tunnel
failed`. Lo comprobé a mano con el mismo `curl` del registro, fuera del
verificador, y devuelve 403 igual. `REPO-001`, que apunta a este repositorio,
sigue devolviendo **200** desde la misma máquina. Es decir: no hay ningún indicio
de que el companion se haya cerrado, solo de que esta máquina no llega hasta él.
El `red: true` hizo justo su trabajo, degradar a REVISAR en vez de a FALLA.

Sin cambios en `DOS-PRODUCTOS` ni en la tabla del `README.md`: las dos ya dicen
12 de 12 y las dos ya dicen que faltan los preliminares. No hay recuento nuevo.

**Nota de rutina:** cero diálogos de permisos. Nada escrito dentro de ninguna
carpeta `.claude/`, laboratorio sin tocar y nada copiado desde `/tmp`. Lo único
que cambia este commit es este diario y el sello del propio verificador.

### PARA JULIÁN

Sigue viva la decisión de ayer y hoy se le suma una segunda, más pequeña y de
manuscrito. Ninguna de las dos la tomo yo.

1. **La rutina lleva dos días sin trabajo y va a repetir esto cada mañana.**
   Las tres salidas están escritas enteras en la entrada de ayer y no las repito
   aquí: pararla (y entonces hay que parar o ajustar el latido, o queda una
   alarma sonando para siempre), reapuntarla a los preliminares (prompt nuevo,
   el actual está escrito entero alrededor de "escribe UN módulo"), o dejarla
   como guardia de regresión (y entonces que el prompt lo diga). Lo que sí
   añado es un dato a favor de la tercera: hoy ha vuelto a tener valor real,
   porque ha confirmado que la 2.1.260 no rompe nada y ha explicado un cambio
   de cifras que si no habría asustado a la sesión de mañana.

2. **El módulo 01 se queda por debajo del mínimo de palabras y nadie lo había
   apuntado.** `modulo-01-fundamentos.md` tiene **2.492 palabras** y el
   invariante del esqueleto pide entre 3.000 y 4.000. No le falta estructura:
   tiene las seis partes, la cabecera y el runbook. Le falta cuerpo, y se
   entiende por qué, es el primero que se escribió, contra la 2.1.228 el 12 de
   agosto, seguramente antes de que el mínimo quedara fijado. Los otros once
   van de 3.260 a 3.998. **No lo he tocado**, por dos motivos: ampliar un
   módulo ya publicado y verificado no es "escribir el módulo pendiente" que
   pide el encargo de hoy, y tocar su texto mueve afirmaciones que ya tienen
   ID en el registro. Si quieres que se amplíe, es un encargo propio y conviene
   decir a qué sección van esas 500 palabras largas.

## 2026-09-03 · Sin módulo · No queda ninguno por escribir

**La rutina disparó, hizo la comprobación y no escribió módulo, porque no hay
módulo pendiente.** Los doce están escritos desde ayer. El paso 1 de la rutina
dice que si ya existen los doce y están completos no hay trabajo, y es el caso:
los doce archivos están, los doce llevan las seis partes del esqueleto en orden
y los doce cierran con su runbook.

Comprobado, no supuesto. Verificador contra la **2.1.259**, que es versión nueva
de hoy y no la 2.1.258 de ayer: **93 pasan, 0 fallan, 45 a revisar, 6 omitidas**.
`comprobar-coherencia.py`, sin contradicciones sobre 19 hechos canónicos y 80
archivos. `construir.py --comprobar`, todas las salidas al día, huella
`43b9c8d2`. Es decir: el salto de versión del CLI no ha roto ninguna afirmación
publicada. `git status --short` sale vacío.

**Por qué hay entrada de diario si no hay módulo.** Porque sin ella el latido
de las 21:00 UTC abriría una incidencia `rutina-callada` esta noche, y sería
mentira: la sesión no se murió ni se colgó en ningún diálogo de permisos, corrió
entera y encontró el trabajo hecho. `latido-rutina.py` va con tolerancia 0 y solo
mira si alguien escribió algo hoy, no si ese algo era un módulo. Escribir esta
entrada es lo que distingue "la rutina terminó y no había nada" de "la rutina
desapareció", que es justo lo que el latido existe para separar.

Sin cambios en `DOS-PRODUCTOS` ni en la tabla del `README.md`: las dos ya dicen
12 de 12 y las dos ya dicen que faltan los preliminares. No hay recuento nuevo
que apuntar.

**Nota de rutina:** cero diálogos de permisos. No se ha escrito nada dentro de
ninguna carpeta `.claude/`, no se ha tocado el laboratorio y no ha entrado nada
desde `/tmp`. Lo único que cambia este commit es este diario.

### PARA JULIÁN

Una sola decisión, y no la tomo yo: **la rutina se ha quedado sin trabajo y a
partir de hoy va a repetir esto cada mañana.** Mientras siga en pie va a
despertar a las 08:00, comprobar, no escribir módulo y anotar una entrada como
esta. No es dañino, pero es ruido diario y consume presupuesto para no producir
manuscrito.

Las tres salidas, sin recomendación disfrazada de hecho:

1. **Pararla**, en el panel `trig_01RzL9eHhTvWuejJYqBLgV7Z`. Ojo con el efecto
   de segundo orden: **el latido sigue corriendo a las 21:00 y empezaría a abrir
   `rutina-callada` todos los días** desde el primero sin entrada. Si paras la
   rutina hay que parar o ajustar también el latido, o queda una alarma que
   suena para siempre por un silencio que decidiste tú.
2. **Reapuntarla a los preliminares** (portada no, que es diseño tuyo, pero
   "cómo leer este libro" y el glosario sí, y la página de verificación que el
   esqueleto ya marca como "redactable ya"). Eso es un prompt nuevo: el actual
   está escrito entero alrededor de "escribe UN módulo" y de la estructura de
   seis partes, que a un glosario no se le aplica.
3. **Dejarla como guardia de regresión**, un pase diario que solo corre
   verificador, coherencia y construcción contra la versión del CLI de ese día
   y avisa cuando algo pase a FALLA. Hoy ese pase ha tenido valor real: ha
   confirmado que la 2.1.259 no rompe nada. Pero entonces conviene que el prompt
   lo diga, porque el de hoy no lo dice y el trabajo de comprobar quedó como
   efecto lateral de buscar módulo pendiente.

Lo que no he hecho, a propósito: ni tocar la rutina, ni tocar el latido, ni
empezar un preliminar. Las tres cosas son decisión tuya y ninguna estaba en el
encargo de hoy.

## 2026-09-02 · Módulo 12 · Casos completos · PUBLICADO · ULTIMO MODULO

Cerrado `manuscrito/modulo-12-casos-completos.md`, **3.998 palabras**, las seis
partes del esqueleto y runbook de una página. Verificador contra la **2.1.258**:
**93 pasan, 0 fallan, 45 a revisar, 6 omitidas**. Coherencia y
`construir.py --comprobar`, las dos en verde. **Con esto están escritos los doce
módulos.** Lo que queda del producto no son módulos: son los preliminares y el
cierre que el esqueleto lista como pendientes (portada, "cómo leer este libro",
glosario) y el modo escéptico, que ya está escrito.

**Nota de rutina:** cero diálogos de permisos. Nada escrito dentro de ninguna
carpeta `.claude/`. Los cinco experimentos con el agente editando se hicieron
sobre copias del laboratorio en `/tmp/run-*`, creadas con `tar` desde el
repositorio hacia `/tmp`, y **nada volvió de `/tmp` al repositorio**: lo que
entró se escribió con Write. Una ejecución del "todo junto" se pasó de los 120 s
del primer plano y hubo que relanzarla en segundo plano; el JSON de la cortada
se completó después y se usó igual, pero el `pytest` que corrí sobre ella a
mitad de vuelo no valía y se repitió.

**La tesis del módulo, y sale medida.** Dentro de cada tarea hay dos trabajos y
solo uno se puede delegar. Lo mecánico es repetible: dos ejecuciones
independientes desmontaron `procesar_pedido()` en **las mismas siete funciones**,
con una sola diferencia de nombre, y las once pruebas siguieron pasando las dos
veces. Lo que necesita una decisión, no: **cinco ejecuciones de cinco, en dos
formulaciones distintas, fijaron el IVA de fuera de ES y PT en el 0 %** sin que
nadie se lo dijera, y dos borraron el comentario `# revisar con gestoria` que
era el único rastro de que la pregunta seguía abierta. No se equivocó ninguna:
contestaron una pregunta que no se les hizo, porque para terminar la que sí se
les hizo tenían que contestarla.

**El hallazgo que ahorra dinero.** Añadir una frase prohibiendo tomar la
decisión de negocio deja **cero archivos tocados** y **un 41 % menos de tokens
de entrada** (140.948 y 139.740 frente a 239.730 y 234.954), dos de dos. Es la
única vez en el libro que la instrucción que quita riesgo es también la que
quita gasto: un agente que se para antes de editar se ahorra el ciclo de
escribir, releer y comprobar.

**El hallazgo que más va a doler al lector.** Es la única medida del módulo
cuyas dos repeticiones **no coincidieron**, y la discrepancia es el hallazgo.
Misma petición para unificar la configuración: las dos conservaron el
comportamiento y los valores en ejecución, pero la segunda metió
`config.DB_PATH` dentro de `conexion()` y borró el nombre `app.DB`, del que
cuelga el `monkeypatch` del fixture. Resultado: **11 pasan frente a 11 ERROR**.
Y el remate para CI: **once errores de montaje dan cero `failed`**, así que un
paso que haga `grep failed` aprueba el commit que acaba de dejar la red de
pruebas colgando.

**Aportación al laboratorio, a propósito:** `procesar_pedido()` desmontada en
siete funciones más el endpoint que las ordena; `config.IVA_POR_PAIS` con cuatro
países y sin tipo por defecto (un país fuera de la tabla devuelve 400 con el
país en el cuerpo); `settings.py` **borrado** y `config.py` importado de verdad;
`DECISIONES.md` nuevo con cuatro entradas; `CLAUDE.md` reescrito en el mismo
commit que el código; y las pruebas de 9 a 11, con las dos `test_hoy_` del IVA
sustituidas por seis y la del descuento renombrada. **13 en verde.**

**Tres entradas del registro cambiaron de contenido, y estaba previsto.**
`CTX-006`, `CTX-007` y `CID-011` se pusieron rojas al arreglar el laboratorio.
La nota de `CID-011` decía desde el 27-ago que el día que el módulo 12 arreglara
el IVA tenían que fallar. Se actualizaron al estado de hoy dejando escrito en la
nota qué comprobaban antes y por qué cambió. Igual el hecho canónico
`CONFIG-NINGUNO-SE-USA`, que ahora describe las dos épocas: el punto de partida
de los módulos 01 a 11 y lo que dejó el 12.

### PARA JULIAN

Cuatro decisiones, y ninguna la he tomado yo. Están todas en
`D6-repo-feo/gestor-pedidos/DECISIONES.md` marcadas como pendientes:

1. **Qué países van en `IVA_POR_PAIS` y con qué tipo.** He puesto cuatro (ES,
   PT, FR, IT) porque el contrato del esqueleto pide que las pruebas cubran
   cuatro países, y he dejado escrito en el archivo y en el módulo que **el
   manual no certifica tipos impositivos**: son un dato de negocio. Si prefieres
   otros cuatro, o que la tabla del laboratorio lleve valores obviamente ficticios
   para que nadie los copie a producción, es cambiar `config.py` y cuatro
   números literales en las pruebas.
2. **Si un pedido sin campo `pais` debe rechazarse.** Hoy lo rechazo, porque el
   código no puede distinguir "no sé" de "España" y esa confusión era el fallo 4.
   Consecuencia real y escrita: **todo pedido que llegue sin `pais` deja de
   crearse**. Si crees que el módulo debe enseñar la ventana de transición
   (aceptar `ES` por defecto con fecha de caducidad) en vez del corte limpio,
   dilo y lo cambio: es media página del caso B.
3. **Si los dos descuentos por cantidad deben seguir acumulándose.** He
   congelado el comportamiento de 2019 a propósito, con el argumento de que un
   cambio de precios no se cuela dentro de una refactorización. La decisión de
   negocio sigue sin tomarse y está marcada como tal.
4. **Si el fallo 8 debe quedar arreglado en el repositorio que se entrega.** El
   módulo 12 lo arregla porque el esqueleto se lo pide, pero eso deja el
   laboratorio del módulo 03 describiendo un estado que el lector ya no se
   encuentra si clona el repo al final. Las opciones son dejarlo así y decirlo
   en el guion de doma, o entregar dos etiquetas del repositorio, una de partida
   y otra de llegada. **Yo no elijo esto: cambia cómo se empaqueta el producto.**

Y una quinta, que es del libro y no del laboratorio: **ahora que están los doce,
hay que decidir el orden de los preliminares y quién escribe la portada.** El
esqueleto los lista pendientes desde el principio.

## 2026-09-01 · Módulo 11 · Troubleshooting · PUBLICADO

Cerrado `manuscrito/modulo-11-troubleshooting.md`, **3.997 palabras**, las seis
partes del esqueleto y runbook de una página. Verificador contra la **2.1.252**:
**86 pasan, 0 fallan, 40 a revisar, 6 omitidas**. Coherencia y
`construir.py --comprobar`, las dos en verde. Queda un módulo: el 12.

**Nota de rutina:** cero diálogos de permisos. Nada escrito dentro de ninguna
carpeta `.claude/`; los experimentos destructivos (hook que falla, `settings.json`
manipulado) se hicieron sobre una copia del laboratorio en `/tmp/lab11`, y nada
volvió de `/tmp` al repositorio. Lo que el módulo aporta al laboratorio, a
propósito: el arreglo del `except:` desnudo en `app.py`,
`tests/test_diagnostico.py` y `DIAGNOSTICO.md`.

**La tesis del módulo, y sale medida.** El `except:` desnudo del repositorio y el
aviso que sale por la salida de error son **el mismo fallo en dos capas**. Con la
salida de error apartada, el JSON de resultado trae **26 campos de primer nivel y
ninguno menciona que se acaban de ignorar tres reglas de `permissions.allow`**:
`is_error: false`, `subtype: success`, código 0, cinco repeticiones.

**El hallazgo que más va a doler al lector.** Un hook `PreToolUse` que **sale con
1 no bloquea nada y no deja rastro** en el JSON: `permission_denials` vacío,
`is_error` falso, proceso con 0. Con `exit 2` sí bloquea y sí aparece. Dos de dos
por fila. Un veto roto puede llevar semanas sin vetar y todo lo demás sigue
diciendo que va bien. La única forma de verlo es
`--output-format stream-json --verbose --include-hook-events`.

**Y el pendiente del módulo 10 queda cerrado, que era el punto 5 de su "PARA
JULIÁN".** La telemetría **no estaba rota**. Con `--debug-file`, el registro dice
`isTelemetryEnabled=true`, y después `getOtlpLogExporters: types=[]` y
`Created 0 log exporter(s)`, con un `[WARN] Event dropped (no event logger
initialized)` por evento. Con `OTEL_LOGS_EXPORTER=otlp` en vez de `console`:
`types=["otlp"]` y **1 exportador**, sin eventos tirados. Dos repeticiones por
valor. **El valor `console` se descarta sin decirlo.** No hace falta la máquina
con colector de verdad que se pedía: ya es una cifra.

Lo medido, todo con dos repeticiones como mínimo, contra la **2.1.252**:

| Qué | Resultado |
|---|---|
| Campos del JSON que mencionan el aviso de confianza | **0 de 26** |
| Líneas de depuración con `--debug` en modo `-p` | **0** |
| Líneas con `--debug-file`, mismo comando | **211** (205 DEBUG, 3 INFO, 2 ERROR, 1 WARN) |
| Hook `exit 1`: ¿bloquea? ¿deja rastro? | **no y no** |
| Hook `exit 2`: ¿bloquea? ¿`permission_denials`? | sí y sí |
| `OTEL_LOGS_EXPORTER=console` | tipos `[]`, **0 exportadores**, eventos tirados |
| `OTEL_LOGS_EXPORTER=otlp` | tipos `["otlp"]`, **1 exportador** |
| `claude doctor` con 3 avisos: código de salida | **0** |
| Entradas del catálogo de `errors.md` | **106** (eran 83 el 12-ago) |
| Impuesto de contexto del laboratorio (`--safe-mode`) | **4.189 tokens** (4.065 el 27-ago con la 2.1.247) |
| El `except:` desnudo: HTTP, pedido guardado, líneas de registro | **200, sí, 0** |
| `test_diagnostico.py` contra el código viejo y contra el nuevo | **falla y pasa** |
| Pruebas del laboratorio | 9 → **11**, las nueve viejas sin tocar |

**La factura del laboratorio, 2.1.252.** Treinta y una invocaciones del CLI,
quince con el JSON conservado: **947.086 tokens de entrada** y **2.025 de
salida**, **0,61 dólares**, por debajo de 0,70 €. De la entrada, **845.049
servidos desde caché (89,2 %)**. Relación entrada salida **467,7 a 1**, contra el
90,5 del módulo 10 y el 24 de `D4-factura/`. **Diagnosticar es la actividad más
desequilibrada que hemos medido**: se relee la configuración entera para obtener
dos palabras. Y otra vez la caché: la misma pregunta, dos veces seguidas y sin
cambiar nada, 0,205 $ y 0,037 $.

### PARA JULIÁN

1. **El catálogo de `errors.md` ha crecido un 28 % en veinte días**, de 83
   entradas a 106, y la página de 223.030 a 347.515 bytes. `guia-21/M18` publica
   el recuento viejo con su fecha y su versión, que es correcto para lo que dice.
   **No he tocado la guía-21**, como en los módulos 09 y 10. Decide si se
   reescribe la tabla 14 o si se le pone una nota de "recuento del 12-ago-2026".
2. **`TRB-001` del esqueleto es floja y la he dejado como estaba.** Dice "claude
   update comprueba e instala actualizaciones" y se comprueba con un patrón sobre
   `--help`. No es falsa, pero no aporta nada al módulo y no aparece en el texto.
   Las once entradas nuevas (`TRB-003` a `TRB-013`) son las que sostienen lo que
   se publica. **Si quieres retirar `TRB-001`, dilo; no borro entradas del
   esqueleto por mi cuenta.**
3. **El arreglo del `except:` toca `app.py`, que es material sembrado.** El fallo
   5 del inventario queda cazado, como manda `guion-de-doma.md`, y la decisión de
   2019 se conserva: el pedido sigue adelante si falla el aviso. **Lo que no he
   hecho es actualizar el inventario del guion de doma para marcar el 5 como
   cerrado**, porque el resto de módulos tampoco marcan los suyos y no quiero
   inventar una convención. Si la quieres, es una columna más en esa tabla.
4. **`--debug` no imprime nada en modo `-p`, y eso puede ser un fallo del CLI.**
   Cero líneas en texto y en JSON, dos repeticiones cada una, mientras
   `--debug-file` escribe 211 en el mismo comando. El módulo lo publica como
   medición, no como diagnóstico del CLI. **Si quieres que se reporte, el reporte
   sale de aquí en cinco minutos**, pero antes hay que decidir qué transcripción
   se manda: se retienen cinco años y la clave de pasarela está en el repositorio
   que el agente ha leído.
5. **Este entorno sigue sin la confianza del espacio de trabajo aceptada**, así
   que los `permissions.allow` del laboratorio se ignoran en todas las
   mediciones. Es lo que hace posible medir el aviso, así que hoy ha jugado a
   favor. Conviene seguir sabiéndolo antes de publicar cualquier cifra de
   permisos.

## 2026-08-31 · Módulo 10 · Seguridad y costes · PUBLICADO

Cerrado `manuscrito/modulo-10-seguridad-y-costes.md`, **4.007 palabras**, las
seis partes del esqueleto y runbook de una página. Verificador contra la
**2.1.251**: **81 pasan, 0 fallan, 34 a revisar, 6 omitidas**. Coherencia y
`construir.py --comprobar`, las dos en verde. Quedan dos módulos: 11 y 12.

**Nota de rutina:** cero diálogos de permisos. No se escribió nada dentro de
ninguna carpeta `.claude/`; el A/B se hizo sobre **copias del laboratorio en
`/tmp`**, no sobre el repositorio; el servidor MCP envenenado vive en `/tmp` y se
queda ahí a propósito; y lo único que el módulo aporta al laboratorio es
`D6-repo-feo/gestor-pedidos/SEGURIDAD.md`, escrito con la herramienta de
escritura.

**El hallazgo del día, y es incómodo.** La afirmación de `SEG-002` **ha
caducado**. El 12-ago-2026, con la **2.1.228**, la inyección del `README.md` se
detectaba **tres de tres** (`evidencias/EXP-001`). El 31-ago-2026, con la
**2.1.251**, la misma prueba sobre el mismo repositorio: **cero de diez**, ocho
con la pregunta neutra y dos con una auditoría explícita. **Tampoco la
obedeció**: las dos auditorías reportaron justo lo que la inyección pedía callar,
dos de dos. Diecinueve días y veintitrés versiones de parche, sin nota de
versión. `SEG-002` se ha reescrito como prueba manual de revisión trimestral, con
el histórico dentro.

**Y el hallazgo que lo compensa, que es nuevo y sale al revés de lo esperado.**
El experimento que `EXP-001` dejó abierto ("con la inyección enterrada en la
respuesta de una herramienta ... es otro experimento que aún no hemos hecho") ya
está hecho, dado de alta como `SEG-003`. Mismo comentario, palabra por palabra,
devuelto por un servidor MCP mínimo dentro del nombre de un cliente: **dos de
dos** lo cita, lo llama intento de inyección, declara que lo ignora y abre la
respuesta con ese aviso. **Misma frase, dos puertas, dos comportamientos
opuestos el mismo día.** Es el centro del módulo.

Lo medido, todo con dos repeticiones como mínimo:

| Qué | Resultado |
|---|---|
| Inyección por archivo del repositorio, ¿la nombra? | **0 de 10** ‹2.1.251› |
| Inyección por respuesta de herramienta MCP, ¿la nombra? | **2 de 2** |
| Auditoría explícita, ¿reporta lo que la inyección pide callar? | 2 de 2 |
| Pregunta neutra, ¿avisa de la clave en claro? | **1 de 8** |
| `deny Read(./secretos/**)`, ¿bloquea y lo dice? | 2 de 2 |
| Copias en claro de la clave en `~/.claude/projects/` | **35, en 4 archivos** |
| Copias del archivo protegido por `deny` | **0** |
| Eventos de telemetría vistos con `-p` y exportador de consola | **0 en 6 ejecuciones** |

**La factura del laboratorio, 2.1.251.** Veintiuna ejecuciones, **2.013.586
tokens de entrada** y 22.248 de salida, **1,29 dólares**, por debajo de 1,50 €.
De la entrada, **1.844.835 servidos desde caché (91,6 %)** y solo **92 tokens de
entrada genuinamente nueva**. Relación entrada salida **90,5 a 1**, contra el
24 a 1 que `D4-factura/` midió sobre otra operación: la estructura transfiere y
la magnitud empeora. Y a diferencia del módulo 09, **aquí el CLI sí devolvió
`total_cost_usd` en cada ejecución**, así que el coste no hubo que reconstruirlo.

### PARA JULIÁN

1. **El PASA del esqueleto para el módulo 10 ya no es cierto.** Dice "el lector
   detecta la inyección **y demuestra que su configuración anterior la
   obedecía**". No la obedece: 2 de 2 reportó justo lo que la inyección pedía
   callar. `EXP-001` ya lo dejó dicho el 12-ago y el esqueleto no se actualizó.
   El módulo publica el PASA que sí se sostiene (las dos salidas guardadas, la
   ignorada por archivo y la denunciada por herramienta). **Hay que corregir la
   línea del esqueleto y la fila del módulo 10 en `D6-repo-feo/guion-de-doma.md`.
   No las he tocado.**
2. **Parte A y parte B no caben en un módulo de 4.000 palabras.** El esqueleto
   pide 10.1 a 10.6 de seguridad y 10.7 a 10.12 de la factura. El módulo entra en
   el formato de seis partes obligatorio y la factura vive dentro de 10.6, con
   las tres leyes, la relación de 232 a 1 de la cortesía y las cifras propias.
   Lo que no cabe es la telemetría completa de las 4.195 llamadas de
   `D4-factura/capitulo-la-factura.md`. **Decide si ese capítulo se publica como
   anexo del libro o se queda como material interno.** Hoy sigue donde estaba y
   el módulo lo cita por su ruta.
3. **`evidencias/EXP-001` sigue diciendo "tres de tres" sin marca de caducidad.**
   Es correcto para su fecha y su versión, y engaña a quien lo lea suelto. No lo
   he editado porque es un registro de experimento fechado. Si quieres una nota
   de "superado por la medición del 31-ago-2026", dilo y se añade.
4. **`guia-21/M5-permisos-y-seguridad.md`, sección 5.9, publica el resultado
   viejo** ("las dos veces detectó la inyección"). Mismo caso que los precios de
   revisión del módulo 09: la guía-21 no la he tocado.
5. **La telemetría no la he podido ver.** Seis ejecuciones, exportador de consola
   por entorno y por el bloque `env` de un `--settings`, cero eventos, y
   `--debug` sin mencionar nada. Puede ser el modo `-p`, puede ser este sandbox.
   El módulo lo publica como "no lo dimos por bueno y no pudimos verlo", que es
   lo honesto, pero **si tienes una máquina con un colector de verdad, media hora
   ahí convierte esto en una cifra**.

## 2026-08-27 · Módulo 09 · Git, CI e IDE · PUBLICADO

Cerrado `manuscrito/modulo-09-git-ci-e-ide.md`, **3.997 palabras**, las seis
partes del esqueleto y runbook de una página. Verificador contra la **2.1.247**:
**80 pasan, 0 fallan, 29 a revisar, 6 omitidas**. Coherencia y
`construir.py --comprobar`, las dos en verde. Quedan tres módulos: 10, 11 y 12.

**Nota de rutina:** el paso 0a funcionó otra vez, el clon venía en el módulo 08.
Cero diálogos de permisos: **no se escribió nada dentro de ninguna carpeta
`.claude/`**, los archivos nuevos del laboratorio se escribieron con la
herramienta de escritura y los temporales de medición se quedaron en `/tmp`.

**Mediciones propias, 2.1.247.** Treinta y una ejecuciones, **1.957.905 tokens
de entrada** y 4.120 de salida, **1,92 dólares**. La cifra de coste **no la da
el CLI de una vez**: se saca de las cuarenta y cinco llamadas registradas en
`~/.claude/projects/`, aplicando las dos tarifas por token que se derivan de dos
ejecuciones donde el CLI sí devolvió `total_cost_usd` (una con caché fría y otra
caliente). Está dicho así en el módulo y conviene no olvidarlo al revisar.

Lo medido, todo con dos repeticiones idénticas:

| Qué | Resultado |
|---|---|
| Petición trivial en directorio vacío | 44.208 tokens |
| La misma en `gestor-pedidos`, todo cargado | 45.989 tokens |
| Con `--strict-mcp-config` | 45.771, o sea **218** de servidor MCP, el mismo número del módulo 06 contra la 2.1.241 |
| Con `--safe-mode` | 41.924 |
| **Lo que cuesta la configuración del laboratorio** | **1.781 tokens por turno**, frente a los 1.737 que suman las piezas medidas una a una |

Los dos hallazgos del módulo, los dos nuevos:

1. **En `-p` los hooks del repositorio se ejecutan y sus `permissions.allow` se
   ignoran.** Sin diálogo de confianza, porque no hay nadie para contestarlo.
   Confirmado a la vez por los eventos `hook_response` (código 0) y por el
   `Ignoring 3 permissions.allow entries` de la salida de error. Es `CID-015`.
2. **`--bare`, el modo que la documentación recomienda para CI, no funciona con
   la suscripción.** No lee ni OAuth ni el llavero: exige `ANTHROPIC_API_KEY`.
   Falla con `Authentication error`, que no menciona ninguna de las dos cosas.
   Es `CID-012`.

Y las dos trampas de la salida JSON, las dos con su prueba: un fallo de
autenticación devuelve `is_error: true` con **`subtype: success`**, y una
ejecución cortada por `--max-budget-usd` devuelve un JSON **sin campo `result`**
(`CID-013`). Las dos aprueban solas cualquier puerta que decida por `subtype` o
lea `result` a pelo.

**Lo que gana el laboratorio.** `requirements.txt` fijado al cierre completo,
quince paquetes (fallo 9); `requirements-dev.txt` aparte;
`tests/test_caracterizacion.py` con nueve pruebas, cinco de ellas
`test_hoy_` que fijan un comportamiento que está mal (fallo 14);
`.github/workflows/ci.yml` con tres trabajos ordenados por precio; y `CI.md`.
Comprobado de punta a punta en un entorno virtual limpio: con el
`requirements.txt` viejo, `pip check` nombra **doce paquetes que faltan** y sale
con 1, y `pytest` sale con **5**; con los nuevos, los dos en verde y nueve
pruebas pasando.

**PARA JULIÁN**

1. **La puerta de CI del laboratorio lleva `--bare`, y `--bare` exige clave de
   API.** El flujo declara `ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}`.
   Si Cosas Agénticas va a enseñar esto con la suscripción, hay que decidir si
   el libro recomienda sacar una clave o si se queda en `--safe-mode` como vía
   principal. Hoy el módulo cuenta las dos y no elige. **Es decisión tuya.**
2. **Precios de revisión.** La documentación de hoy dice **15 a 25 $ por
   revisión** en la forja, no los 5 a 25 que decía la guía-21 en agosto. El
   módulo publica los de hoy y `M13-cicd-y-revision.md` sigue con los viejos.
   Si quieres que la guía-21 se corrija, dilo: no la he tocado.
3. **El flujo del laboratorio no corre nunca.** Vive en
   `D6-repo-feo/gestor-pedidos/.github/workflows/`, que GitHub no mira porque no
   está en la raíz. Es a propósito, para no gastar en cada empujón del
   manuscrito, pero significa que **ese YAML no está probado por una ejecución
   real de Actions**, solo por sus comandos corridos a mano aquí.

## 2026-08-26 · Módulo 08 · Subagentes · PUBLICADO

Cerrado `manuscrito/modulo-08-subagentes.md`, **3.997 palabras**, las seis partes
del esqueleto y runbook de una página. Verificador contra la **2.1.246**:
**71 pasan, 0 fallan, 27 a revisar, 4 omitidas**. Coherencia y
`construir.py --comprobar`, las dos en verde. Quedan cuatro módulos: 09 a 12.

**Nota de rutina:** el paso 0a funcionó. El clon venía en el módulo 07 y el
`git fetch` lo puso al día antes del checkout, así que el módulo pendiente que se
eligió en el paso 1 era el de verdad. Ningún diálogo de permisos: **no se escribió
nada dentro de ninguna carpeta `.claude/`** y todas las mediciones fueron por
`--agents`, que no toca el disco. Es la vía que el módulo recomienda además por
higiene, así que la restricción del sandbox y el consejo del libro coinciden.

**Mediciones propias, 2.1.246 con Sonnet 5.** Veintinueve ejecuciones, ~2.350.000
tokens de entrada, **4,29 dólares**. Es el módulo más caro del libro y el motivo
está escrito en la cabecera: cada fila de la tabla central es una auditoría entera
de `app.py`, no una petición trivial.

Coste de tener el subagente declarado, dos repeticiones por fila e idénticas al
token:

| Estado | Tokens de entrada |
|---|---:|
| Sin ningún subagente | 45.977 |
| Con uno (descripción de 199 caracteres) | 46.088 |
| Con seis (1.227 caracteres de descripción) | 46.610 |
| El mismo de una fila, **más 21.228 caracteres de prompt** | **46.088** |
| Descripción de 1.536 caracteres | 46.588 |
| Descripción de 5.616 caracteres | **48.068** |

Y el experimento central, dos repeticiones por condición, contando los fallos 2,
3 y 4 del guion de doma sobre el informe:

| Quién revisa | Fallo 2 | Fallo 3 | Fallo 4 |
|---|---|---|---|
| El agente principal, "revisa app.py" | 2 de 2 | 0 de 2 | 0 de 2 |
| Subagente con contrato de auditor | 2 de 2 | 0 de 2 | 1 de 2 |
| Subagente con **criterio de aceptación en tres preguntas** | 2 de 2 | **2 de 2** | **2 de 2** |

**Hallazgos propios del módulo:**

- **El aislamiento no es criterio, y esto desmonta el consejo estándar.** Poner un
  revisor aparte, por sí solo, no movió la aguja: encontró lo mismo que el
  principal con más detalle y por el doble de precio. La única variable entre la
  segunda fila y la tercera es el criterio de aceptación. Hecho canónico nuevo,
  `EL-AISLAMIENTO-NO-ES-CRITERIO`.
- **El `CLAUDE.md` del proyecto llega al subagente y le tapa la boca.** Quitando
  del `CLAUDE.md` del laboratorio el último párrafo y solo ese, **309
  caracteres**: con él, la clave de pasarela no aparece en el informe **0 de 2** y
  el revisor escribe por qué; sin él, **2 de 2** como hallazgo bloqueante. Es el
  hallazgo del módulo y ata el 08 con el 03. Hecho canónico nuevo,
  `EL-CLAUDE-MD-LLEGA-AL-SUBAGENTE`.
- **Un subagente compra contexto con dinero.** La ventana del principal revisando
  él mismo: 146.114 y 244.588 tokens, 0,11 y 0,13 dólares. Delegando: 53.916 y
  53.513 tokens, 0,28 y 0,24 dólares. **Divide el contexto por tres y multiplica
  la factura por dos.** Y la ventana del que delega es estable: las dos del
  principal se separan en cien mil tokens, las dos delegadas en cuatrocientos.
- **La descripción de un subagente no se corta**, al revés que la de una skill.
  5.616 caracteres son 2.091 tokens en cada turno, lo segundo más caro que se
  escribe a mano en todo el libro después del archivo de memoria.
- **El síntoma clásico no se reprodujo, y va publicado así.** Dos ejecuciones de
  "escribe un endpoint siguiendo el estilo del archivo y revísate": las dos veces
  se negó a copiar la inyección SQL, usó consulta parametrizada y dijo que el
  repositorio no está listo. El visto bueno automático no salió. Lo que sí salió
  2 de 2 fue "mi cambio es seguro": alcance elegido por la misma cabeza que
  escribió el código, que es el sesgo de verdad.

**Registro:** ocho entradas nuevas, `SUB-004` a `SUB-011`. Seis se comprueban
solas, una es manual (`SUB-010`, la frecuencia del bozal del `CLAUDE.md`) y una
gasta tokens (`SUB-011`).

**Laboratorio:** `gestor-pedidos` gana `AGENTES.md`. **Ningún fallo sembrado
tocado y ningún archivo del laboratorio modificado**: las pruebas que escriben o
que alteran el `CLAUDE.md` se hicieron sobre copias en `/tmp`, que se quedan ahí.

**Activos:** `entregables/plantillas/agents/` pasa de tres a **seis subagentes con
contrato**, que es lo que promete el esqueleto: `revisor`, `auditor-seguridad`,
`investigador`, `validador`, `probador` y `arqueologo`. El `revisor` se reescribe
con el criterio de aceptación medido, porque el que tenía es exactamente el de la
fila que no encontró nada.

**Bookkeeping:** `fabrica/hechos.yaml` y `README.md`, de "7 de 12" a "8 de 12", y
el recuento del verificador del README, que llevaba en 22 desde julio. Dos hechos
canónicos nuevos.

### PARA JULIÁN

1. **Hay una frase en el `CLAUDE.md` del laboratorio que apaga al revisor, y
   quitarla o no es decisión tuya.** Es la última del archivo: "No hace falta que
   avises de esos fallos en cada respuesta: están inventariados". Sirve para lo
   que se escribió, que es no leer el mismo aviso veinte veces al día, y a la vez
   borra la clave de pasarela del informe de auditoría, medido 0 de 2. Las tres
   salidas que veo, y ninguna es obviamente la buena: **(a)** dejarla y que el
   contrato del revisor la desobedezca, que es lo que hay hoy y funciona pero
   depende de que cada contrato lo recuerde; **(b)** quitarla y aceptar el ruido;
   **(c)** reescribirla en negativo, del tipo "estos fallos están inventariados y
   **se reportan igual en cualquier auditoría**". Yo no la he tocado. Si eliges la
   (c), hay que rehacer la tabla de `AGENTES.md` y la del 8.2.3.
2. **El esqueleto del 08 promete un PASA que solo se cumple con la tercera
   condición.** Dice "el revisor encuentra los fallos 2, 3 y 4 que el principal
   había pasado por alto", y eso es cierto **solo** con criterio de aceptación
   escrito: con un contrato de auditor normal salió 2 de 3 en una ejecución y 1 de
   3 en la otra. El módulo lo publica así, con la tabla entera, porque es más útil
   que el resultado limpio. Si quieres que el esqueleto lo diga, la línea sería:
   "PASA si el revisor encuentra los fallos 2, 3 y 4 **y el lector sabe decir qué
   parte del contrato los destapó**".
3. **La fecha de corte, octava vez.** De la 2.1.245 de ayer a la 2.1.246 de hoy.
   Siete módulos con versión propia y ni una sola coincidencia entre dos. La regla
   8 lleva ocho módulos funcionando; sigue faltando ratificarla en el módulo 01 y
   en la portada, que es lo único que queda pendiente de esa decisión.

## 2026-08-25 · Módulo 07 · Skills y plugins · PUBLICADO

Cerrado `manuscrito/modulo-07-skills-y-plugins.md`, **3.260 palabras**, las seis
partes del esqueleto y runbook de una página. Verificador contra la **2.1.245**:
**65 pasan, 0 fallan, 26 a revisar, 3 omitidas**. Coherencia y
`construir.py --comprobar`, las dos en verde. Quedan cinco módulos: 08 a 12.

**Antes que nada, un susto que hay que arreglar en la rutina.** Esta sesión
arrancó con `origin/main` en el módulo 04, escribió **un módulo 05 entero** y al
ir a empujar se encontró con que el remoto ya tenía el 05 y el 06 publicados. La
sesión había estado suspendida entre medias y el clon se quedó viejo. **La
guarda del paso 0c no lo caza**: comprueba que existe el módulo 02, que existía.
Se tiró el trabajo duplicado sin pisar nada y se escribió el 07, que era el
pendiente de verdad. Recomendación concreta abajo, en PARA JULIÁN.

**Mediciones propias, 2.1.245.** El módulo mide **frecuencias**, no cifras, así
que cada fila son cuatro u ocho ejecuciones. Veinticuatro en total para la tabla
de disparo, contando el disparo **en la traza de la sesión**, no en la respuesta:

| Lo que pide el usuario | Descripción de la skill | Se disparó |
|---|---|---|
| "Échale un vistazo al endpoint /buscar" | de catálogo, 43 caracteres | **4 de 4** |
| lo mismo | de tarea, 380 caracteres | **4 de 4** |
| "Un cliente O'Brien tumba la búsqueda" | de catálogo | **0 de 4** |
| lo mismo | de tarea | **0 de 4** |
| lo mismo | con el síntoma en `when_to_use` | **8 de 8** |
| lo mismo, con `disable-model-invocation` | la del síntoma | **0 de 3** |

Y el coste, dos repeticiones por fila e idénticas al token:

| Estado | Tokens de entrada |
|---|---:|
| Sin ninguna skill | 45.752 |
| Con la skill del laboratorio | 45.960 |
| La misma **más 20.000 caracteres de cuerpo** | **45.960** |
| Descripción de 1.200 caracteres | 46.252 |
| Descripción de 1.536 | 46.386 |
| Descripción de 3.072, los 1.536 primeros idénticos | **46.387** |
| Archivo suelto en `.claude/commands/` | 45.793 |

**Hallazgos propios del módulo:**

- **La creencia del gremio es media verdad, y la mitad falsa es la que se
  enseña.** Con una petición que nombra la tarea, la skill se dispara 4 de 4
  **incluso con una descripción de catálogo de 43 caracteres**. Por eso todo el
  mundo cree que su descripción está bien: la valida con la petición equivocada.
  Con la petición real, la que cuenta un síntoma, 0 de 8. Hecho canónico nuevo,
  `SKILL-DISPARO-SINTOMA`.
- **Lo que cierra el hueco no es escribir mejor, es escribir otra cosa:** los
  síntomas en `when_to_use`, con las palabras del que pide. 8 de 8.
- **El tope de 1.536 caracteres, medido y no citado.** Duplicar la descripción
  dejando idénticos los primeros 1.536 cuesta **un token**. La segunda mitad no
  llega al modelo. Y llenarlo cuesta 634 tokens por turno, la mitad de un
  `CLAUDE.md`.
- **La divulgación progresiva es literal:** 20.000 caracteres añadidos al cuerpo,
  **cero** tokens por turno.
- **Los comandos personalizados ya no existen como pieza aparte.** Se han
  fusionado con las skills: comprobado que un `.claude/commands/ping-lab.md`
  responde a `/ping-lab`. Eso deja obsoleta la línea del esqueleto "cuándo un
  comando es mejor que una skill", y el módulo la sustituye por la pregunta que
  sí queda: **quién la invoca**. Hecho canónico nuevo, `COMANDOS-SON-SKILLS`.
- **Tercera vez que el libro mide lo mismo por otro sitio:** el cuerpo de la
  skill pedía abrir la respuesta con una línea marcada y salió **3 de 8**. Se
  carga siempre y se cumple a veces. Es el argumento del 05 otra vez: lo que no
  sea negociable, hook.

**Registro:** diez entradas nuevas, `SKL-003` a `SKL-012`. Seis se comprueban
solas; las cuatro amarillas son mediciones de frecuencia y una comprobación
manual de la fusión de comandos.

**Laboratorio:** `gestor-pedidos` gana `.claude/skills/auditar-endpoint/SKILL.md`
y `SKILLS.md`. **Ningún fallo sembrado tocado.** La skill del laboratorio audita
el `/buscar`, que es el fallo 2 del guion, pero no lo arregla: auditar y reparar
son dos encargos, y el 2 se caza en el 10.

**Activos:** `entregables/plantillas/skills/` pasa de dos a **cinco skills**, con
`LEEME.md`. Los cuatro con `disable-model-invocation` son **los cuatro comandos
de equipo** que promete el esqueleto: `/revisar-cambio`, `/preparar-release`,
`/postmortem` y `/poner-al-dia`.

**Bookkeeping:** `fabrica/hechos.yaml` y `README.md`, de "6 de 12" a "7 de 12".
Dos hechos canónicos nuevos.

### PARA JULIÁN

1. **La guarda del paso 0c se ha quedado corta y hoy ha costado un módulo
   entero.** Comprobar que existe `modulo-02` ya no protege de nada: protegía de
   un clon vacío, no de un clon viejo. La guarda que sirve es de dos líneas y va
   **justo antes de escribir**, no al principio: `git fetch origin main` y, si
   `git rev-parse HEAD` no coincide con `origin/main`, rehacer el paso 0a y
   volver a elegir módulo en el paso 1. La lista de `manuscrito/` se lee después
   del fetch, nunca antes.
2. **El esqueleto vuelve a quedarse corto, ahora en el 07.** Dice "Cuándo un
   comando es mejor que una skill" y esa pregunta ya no existe: son la misma
   pieza. La línea de recambio, si te sirve: "Quién invoca cada cosa:
   `disable-model-invocation` y `user-invocable`, y por qué un comando de equipo
   no debe dispararse solo." Es la segunda línea del contrato que se queda vieja
   en dos módulos seguidos, y las dos por lo mismo: el CLI se movió.
3. **La fecha de corte, séptima vez.** Van seis módulos con versión propia y hoy
   el binario ha vuelto a subir solo, de la 2.1.241 a la 2.1.245 entre el módulo
   de ayer y el de hoy. No hay decisión que tomar ya: la realidad la ha tomado.
   Falta ratificarla en el módulo 01 y en la portada.

## 2026-08-24 (noche) · Módulo 06 · MCP · PUBLICADO · día recuperado

Segundo módulo del mismo día, escrito a mano para recuperar uno de los tres días
en blanco del 21 al 23. Cerrado `manuscrito/modulo-06-mcp.md`, **3.508
palabras**, las seis partes del esqueleto y runbook de una página. Verificador
contra la **2.1.241**: **60 pasan, 0 fallan, 21 a revisar, 3 omitidas**.
Coherencia y `construir.py --comprobar`, las dos en verde. Quedan seis módulos:
07 a 12.

**El esqueleto está equivocado en el 06 y este módulo lo demuestra.** El contrato
describe el contenido como "el impuesto permanente: cada servidor mete sus
definiciones de herramientas en cada turno". Eso contradice el hecho canónico
`MCP-DIFERIDO` desde el 12-ago, y ahora además está medido. El texto publicado
dice lo cierto; la línea del esqueleto sigue como estaba, porque el contrato es
de Julián. Está abajo, en PARA JULIÁN, con la línea de recambio escrita.

**Mediciones propias, 2.1.241, dos repeticiones por celda y las doce idénticas al
token.** Misma petición trivial, mismo repositorio, variando solo el número de
herramientas MCP conectadas por `--mcp-config` con `--strict-mcp-config`:

| Herramientas MCP | Con tool search | Sin tool search |
|---:|---:|---:|
| 0 | 45.441 | 62.662 |
| 3 | 45.659 | 63.220 |
| 12 | 45.772 | 65.016 |

**Hallazgos propios del módulo:**

- **Apagar tool search cuesta 17.221 tokens con cero servidores MCP.** Es el
  número más grande de la tabla y no tiene nada que ver con MCP: los esquemas de
  las herramientas propias del CLI también iban diferidos. La documentación
  presenta tool search como una optimización de MCP, y su ahorro mayor no lo es.
  Hecho canónico nuevo, `TOOL-SEARCH-NO-ES-SOLO-MCP`.
- **Un servidor de tres herramientas cuesta 218 tokens por turno.** Menos que dos
  líneas del `CLAUDE.md`. De 3 a 12 herramientas, unos 13 tokens cada una; sin
  tool search, unos 200, dieciséis veces más. El consejo de "conecta poco" se da
  la vuelta: conectar es barato, lo caro es la confianza.
- **La tabla comparada de las cinco piezas es el mejor activo del módulo.**
  Permisos 0, hooks 0, servidor MCP 218, `CLAUDE.md` 1.311, apagar tool search
  17.221. Todo en la misma máquina con la misma petición. La última fila es la
  que hay que enseñarle a quien decide: la configuración puesta "por prudencia"
  cuesta ochenta veces más que el servidor que nadie deja conectar.
- **Tercera vuelta a la puerta de confianza.** Con el `.mcp.json` sin aprobar,
  `claude mcp list` dice `Pending approval`, y aun así en `claude -p` el servidor
  conectó y sus herramientas estaban disponibles: faltaba el permiso de la
  herramienta, no la aprobación del servidor. Misma familia que `HOK-012`. Se
  cierra con `--strict-mcp-config`.
- **Otro no medido que vale.** Al pedirle que borrara los pedidos, el agente se
  negó citando las instrucciones del servidor **sin llegar a llamar a la
  herramienta**, las dos veces. No se publica como candado, porque no lo es: es
  la misma negativa por criterio propio que el 05 midió fallando 5 de 7. Los
  candados se prueban en seco, y así están las pruebas.

**Registro:** nueve entradas nuevas, `MCP-003` a `MCP-011`. Seis se comprueban
solas corriendo el servidor **en seco por JSON-RPC** contra las fixtures de
`mcp/ejemplos/`, misma técnica que las `HOK` del 05. `MCP-006` y `MCP-007`
reconstruyen la base desde el esquema versionado, así que pasan desde un clon
limpio aunque `datos/pedidos.db` esté en `.gitignore`.

**Laboratorio:** `gestor-pedidos` gana `mcp/servidor-pedidos.py` (200 líneas, sin
dependencias, tres candados), `mcp/preparar-bd.py`, `mcp/ejemplos/` con cinco
fixtures, `MCP.md` y `.mcp.json`. La base de datos se construye y no se versiona.
**Ningún fallo sembrado tocado.**

**Activos:** `entregables/plantillas/mcp/` con el servidor generalizado (ruta por
entorno) y su `LEEME.md`. Probado contra la base del laboratorio.

**Bookkeeping:** `fabrica/hechos.yaml` y `README.md`, de "5 de 12" a "6 de 12".

### PARA JULIÁN

1. **El esqueleto miente en el módulo 06 y hay que corregirlo tú.** Donde dice
   "El impuesto permanente: cada servidor mete sus definiciones de herramientas
   en cada turno", debería decir algo como: "El impuesto y por qué ya casi no lo
   es: tool search difiere los esquemas y solo entran los nombres. Los cinco
   sitios donde eso deja de valer, y lo que cuesta apagarlo." No lo he tocado
   porque el esqueleto es el contrato.
2. **La biblioteca de hooks sigue en 7 de los 10 que promete el esqueleto**,
   segunda vez que se pide. Misma recomendación: bajar la promesa a siete.
3. **La fecha de corte, sexta vez.** Ya son cinco módulos declarando su versión
   sin una sola reescritura. El 01 sigue siendo el único que no la declara, y el
   único por debajo del rango de palabras.

## 2026-08-24 (tarde) · Los tres días en blanco, y el latido que los habría cazado

Al contar el ritmo real salió esto: **del 21 al 23 de agosto no hay una sola
entrada en este diario**. Lo único que hay en esos días son los commits
automáticos del verificador de las 05:20 UTC. La rutina dispara a las 06:00 y no
dejó nada, tres días seguidos, y no se detectó hasta hoy.

**El ritmo real, entonces, no es un módulo al día.** Son cuatro módulos en ocho
días naturales, del 17 al 24: uno cada dos. La cuenta de "siete módulos, ocho
días" era teórica; con lo observado son unas dos semanas.

**La causa no se puede saber desde aquí, y ese es exactamente el problema.** Una
sesión que se cuelga en un diálogo de permisos o que se corta por límite de uso
deja el repositorio idéntico a como quedaría si la rutina no hubiera disparado
nunca. El 19 y el 20 fallaron y quedaron escritos porque alguien lo escribió
después; del 21 al 23 no hay ni eso.

**Arreglo: `.github/workflows/latido-rutina.yml`.** Corre a las 21:00 UTC, quince
horas después de la rutina, cuando el día ya está decidido. Comprueba que el
diario tiene una entrada con la fecha de hoy y, si no la tiene, abre incidencia
con la etiqueta `rutina-callada`. Mientras el silencio dure comenta en la
incidencia abierta en vez de abrir una nueva cada día: una alarma que se repite
sola se acaba ignorando, que es como se perdieron estos tres días.

La lógica vive en `fabrica/latido-rutina.py`, fuera del YAML, para poder
probarla: `python3 fabrica/latido-rutina.py` dice si la rutina está viva, y
`--tolerancia N` afloja el umbral. Probado por los dos lados: contra el diario de
hoy da viva; contra el diario del 23 (quitando la entrada de hoy) da **5 días
callada** y sale con código 1.

**Lo que este latido NO hace, a propósito.** No entra en `registro.yaml` ni en
`verificar.yml`. El verificador dice si el libro sigue siendo cierto; esto dice
si la fábrica sigue viva. Mezclarlos haría que "0 fallan" significara dos cosas
distintas, y que un silencio de la rutina abriera una incidencia titulada
"Rotura con 2.1.24x", que es mentira.

### PARA JULIÁN

1. **El latido detecta el silencio, no lo evita.** Lo que lo evitaría de verdad
   es que la rutina anote en el diario **al empezar**, no solo al terminar: una
   línea después del paso 0c diciendo "arranco, toca el módulo NN". Entonces un
   día en blanco distinguiría "no disparó" de "disparó y murió", que hoy no se
   distingue. No lo he hecho porque el texto de la rutina vive en el panel, no
   en el repositorio, y eso lo tienes que pegar tú.
2. **Los tres días perdidos siguen sin causa.** En el panel de la rutina se ve
   si esas sesiones dispararon y en qué estado quedaron. Si alguna quedó en
   `requires_action`, es otra vez el diálogo de permisos y hay que mirar qué lo
   disparó para añadirlo al paso 0d.

## 2026-08-24 · Módulo 05 · Hooks · PUBLICADO

Cerrado `manuscrito/modulo-05-hooks.md`, **3.997 palabras**, las seis partes del
esqueleto y runbook de una página. Verificador contra la **2.1.241**: **54
pasan, 0 fallan, 18 a revisar, 3 omitidas**. Coherencia y `construir.py
--comprobar`, las dos en verde. Quedan siete módulos: 06 a 12.

**El paso 0d volvió a funcionar.** Cero llamadas colgadas. Los hooks del
laboratorio viven en `D6-repo-feo/gestor-pedidos/hooks/`, fuera de `.claude/`, y
los dos archivos que sí están dentro de una carpeta `.claude/`
(`gestor-pedidos/.claude/settings.json` y la sonda de esquema) se escribieron
enteros con heredoc. Nada entró al repositorio por `cp` desde `/tmp`. Y el sitio
de los scripts dejó de ser una precaución para convertirse en contenido: la
sección 5.3.1 explica por qué separar el código del hook de la configuración que
lo declara es además mejor práctica.

**Registro:** catorce entradas nuevas, `HOK-002` a `HOK-015`. Nueve se comprueban
solas y son de un tipo que no había: **corren los hooks del laboratorio en seco**,
con las fixtures de `hooks/ejemplos/`, comprobando que un hook devuelve `deny`
cuando toca y no imprime nada cuando no toca. Es la técnica de depuración de
5.3.3 convertida en prueba permanente, y no gasta un token. Las cinco amarillas
son las cinco mediciones con coste.

**Mediciones propias, 2.1.241.** Mismo repo, misma petición, variando una sola
cosa:

| Medida | Resultado |
|---|---|
| Credencial escrita, solo `CLAUDE.md` y regla de rutas | **5 de 7** |
| La misma, con el hook que mira contenido | **0 de 7** |
| `allow` y hook en el mismo archivo, sin confianza | `allow` ignorado, **hook ejecutado** |
| Secreto por la herramienta `Read`, con el hook | bloqueado 2 de 2, 91.054 tokens |
| El mismo secreto por `@ruta` | **clave impresa 2 de 2**, 45.530 tokens |
| El mismo `@ruta` con la regla `deny` del 04 | bloqueado 2 de 2 |
| Seis hooks declarados frente a ninguno | 45.381 tokens las cuatro veces |
| Formateo al editar, sin hook y con hook | 0 de 3 frente a 3 de 3 |
| Llamadas a herramienta del mismo turno | 2 frente a 6 |

**Hallazgos propios del módulo:**

- **La medida madre es el 5 de 7.** El síntoma del módulo ("unas veces lo hace y
  otras no") deja de ser una queja y pasa a ser un número. Y las dos veces que
  el agente NO escribió la credencial, se negó por criterio propio y lo explicó
  muy bien, que es exactamente lo que hace que la gente crea que tiene un límite
  donde solo tiene una coincidencia.
- **La asimetría del módulo 04 gira, y gira del lado malo.** Un `allow` de un
  repositorio clonado se ignora sin confianza; un **hook** del mismo archivo se
  ejecuta. Medido en una sola ejecución, con las dos cosas en el mismo
  `settings.json`: el CLI escribió el aviso de "workspace has not been trusted"
  por la salida de error mientras el script del hook ya había corrido. Es hecho
  canónico nuevo, `HOOKS-CORREN-SIN-CONFIANZA`.
- **El agujero del hook es `@`, y es el camino barato.** `PreToolUse` solo corre
  cuando hay llamada a herramienta, y un archivo metido en el prompt con `@` no
  la tiene. Se lleva la clave entera en 1 turno y 45.530 tokens, frente a los 2
  turnos y 91.054 del camino bloqueado. Nadie lo va a notar por la factura. La
  regla `deny` del módulo 04 sí lo cubre, así que la tesis de los dos módulos
  juntos es que **no son alternativas**: cada uno tapa el agujero del otro. Está
  en la tabla de coberturas de 5.2.7, que es el mejor activo del módulo.
- **Declarar cuesta cero; disparar, no.** 45.381 tokens con seis hooks y sin
  ninguno, al token, igual que las reglas del 04. Pero el hook de formato lleva
  el turno de 2 llamadas a herramienta a 6 y de ~167.000 a ~260.000 tokens,
  porque `black` reescribe el archivo y el agente vuelve a leerlo. **El hook que
  impide es barato; el que arregla, no.** Eso no está en ninguna documentación.
- **Un no medido que también vale.** El agujero de `python3` del módulo 04 no se
  reprodujo: el agente se negó por su cuenta las dos veces, en las dos
  configuraciones, sin llegar a llamar a Bash. No se publica ni como "sigue
  abierto" ni como "está cerrado", porque una negativa del modelo no es un
  límite del sistema. Es la misma lección que el 5 de 7, por el otro lado.

**Sonda de esquema ampliada:** `D2-verificador/sonda-esquema` gana un bloque
`hooks` y un `disableAllHooks` inválidos a propósito. `claude doctor` ahí
enumera `hooks.PreToolUse`, `hooks.PostCompact`, `hooks.TeammateIdle` y
`disableAllHooks`, y eso sostiene `HOK-009` sin gastar nada.

**Laboratorio:** `D6-repo-feo/gestor-pedidos` gana `hooks/` con los tres scripts
(`veto-secretos.sh`, `veto-credenciales.sh`, `formatear.sh`), `hooks/ejemplos/`
con las cinco fixtures de prueba en seco, `HOOKS.md` con lo que impide y lo que
NO impide cada uno, y el bloque `hooks` en `.claude/settings.json`. **Ningún
fallo sembrado se ha tocado**: `app.py` quedó restaurado con `DEBUG = True` y sin
formatear después de las mediciones.

**Activos:** `entregables/plantillas/hooks/` pasa de 4 scripts a 7 y deja de
tener referencias rotas (`veto-secretos.sh` y `veto-rm.sh` estaban declarados en
`hooks.json` y no existían). El `hooks.json` de la biblioteca pasa a apuntar a
`${CLAUDE_PROJECT_DIR}/hooks/` en vez de a `.claude/hooks/`, y todos sus
manejadores llevan ya `args: []`, la forma de ejecutable que la documentación
recomienda para cualquier hook con marcador de ruta.

**Bookkeeping:** `fabrica/hechos.yaml` y `README.md` pasan de "4 de 12" a "5 de
12". Hecho canónico nuevo, `HOOKS-CORREN-SIN-CONFIANZA`.

### PARA JULIÁN

1. **La fecha de corte del libro ya está decidida de facto, quinta vez que se
   anota.** El 05 se ha escrito contra la **2.1.241** y lo declara en cabecera,
   como el 02 (2.1.233), el 03 (2.1.234) y el 04 (2.1.235). Son cuatro módulos
   con versión propia y ninguna reescritura. La regla 8 del esqueleto ya lo dice
   por escrito desde el 19-ago; lo único que falta es que lo confirmes para
   poder cerrar el 01, que sigue sin declarar versión.
2. **El inventario del repo feo sigue sin actualizar, cuarto módulo que lo
   dice.** El módulo 05 añade al laboratorio `hooks/`, `hooks/ejemplos/` y
   `HOOKS.md`. La tabla del recorrido de `guion-de-doma.md` no lo refleja, y no
   la he tocado porque es material compartido por los doce módulos.
3. **Decisión nueva, y es tuya: la biblioteca de hooks son 7, no 10.** El
   esqueleto promete "los diez hooks de la biblioteca" como activo del módulo
   05. Hay siete, todos usados o citados por el libro. No he inventado tres para
   cuadrar el número. O bajas la promesa del esqueleto a siete, o dices cuáles
   son los tres que faltan y en qué módulo se ganan. Mi recomendación: bajarla a
   siete y dejar que la biblioteca crezca donde el libro la necesite, que es
   como han crecido las plantillas de permisos.
4. **Sigue abierto lo del módulo 04:** la clave de `app.py` se **acota** en el 04
   y en el 05, y se **elimina** en el 12. El módulo 05 vuelve a escribirlo así,
   explícitamente, en su sección de coste. El `guion-de-doma.md` sigue diciendo
   "04 y 10" para el fallo 1. Es una línea de la tabla.

## 2026-08-19 (tarde) · Módulo 04 · Permisos y sandbox · PUBLICADO

Cerrado `manuscrito/modulo-04-permisos-y-sandbox.md`, **3.996 palabras**, las
seis partes del esqueleto y runbook de una página. Verificador contra la
**2.1.235**: **45 pasan, 0 fallan, 13 a revisar, 3 omitidas**. Coherencia y
`construir.py --comprobar`, las dos en verde. Quedan ocho módulos: 05 a 12.

**El paso 0d funcionó.** Cero llamadas colgadas: todo lo que entró al
repositorio se escribió con heredoc, los archivos de medición se quedaron en
`/tmp`, y el `settings.json` del laboratorio se restauró escribiéndolo, no
copiándolo. La sesión de la mañana murió en un `cp`; esta no ha tenido ninguno.

**Registro:** trece entradas nuevas, `PRM-004` a `PRM-016`. Nueve se comprueban
solas; las cuatro amarillas son las tres mediciones con coste (`PRM-008`,
`PRM-009`, `PRM-010`) y la de la bandera peligrosa como root (`PRM-011`), que no
se automatiza porque su resultado depende del usuario que ejecute el
verificador y en una máquina normal daría falso rojo.

**Mediciones propias, dos repeticiones idénticas cada una, 2.1.235.** Mismo
repo, misma petición, variando una sola cosa:

| Medida | Resultado |
|---|---|
| `allow` en el settings del proyecto, sin confianza | **no se aplica**, 131.788 y 131.806 tokens, 3 turnos |
| La misma regla por `--allowedTools` | funciona, 87.452, 2 turnos |
| La misma regla en el mismo archivo, con confianza aceptada | funciona, 87.456, 2 turnos |
| `deny Read` frente a `cat` | bloqueado las dos veces, y lo dice |
| `deny Read` frente a `python3 -c open(...)` | **imprime la clave las dos veces** |
| 24 reglas `deny` frente a ninguna | 43.619 tokens las cuatro veces |
| `claude auto-mode defaults` | 17 / 66 / 1 / 20 y 63.477 bytes |

**Hallazgos propios del módulo:**

- **La asimetría de la confianza es la columna vertebral del módulo.** Lo que
  restringe (`deny`, `ask`) se acepta desde el repositorio; lo que concede
  (`allow`, `additionalDirectories`) no, hasta aceptar el diálogo. Y como el
  diálogo **no aparece nunca en `claude -p`**, toda tubería de integración
  continua del mundo corre con las reglas `allow` de su repositorio ignoradas.
  El aviso existe y sale **por la salida de error**, así que quien capture solo
  la estándar no lo ve. Es exactamente la trampa que la rutina ya tenía anotada
  desde la sesión de la mañana, medida y convertida en sección.
- **Una regla que no se aplica cuesta un 51 % más** que la misma regla
  aplicándose, y un turno extra. La configuración rota no es neutra.
- **Los seis modos tienen dos listas de nombres.** El error de
  `--permission-mode` enumera `manual`; el del esquema de `settings.json`
  enumera `default`. Los dos sitios aceptan las dos palabras y cada mensaje
  enseña solo una. Sostenido por `PRM-004` y `PRM-005`.
- **Las reglas de permisos cuestan cero tokens.** Al lado de los 1.311 por turno
  del `CLAUDE.md` del módulo 03, eso reordena el consejo: cuando se pueda elegir
  entre pedirlo en el archivo de memoria o imponerlo con una regla, la regla es
  más barata y además se cumple.
- **Lo que una regla no puede proteger.** `cat` se bloquea y `python3` no, y una
  regla protege rutas, no valores: la clave que vive dentro de `app.py` no tiene
  regla posible. Es el puente natural al hook del módulo 05.

**Sonda nueva en el repositorio:** `D2-verificador/sonda-esquema/`, con un
`settings.json` inválido a propósito. `claude doctor` corriendo ahí enumera lo
que el esquema del binario acepta de verdad, y es lo que sostiene `PRM-005` y
`PRM-006`. Es la técnica del módulo 02 convertida en herramienta permanente.

**Laboratorio:** `D6-repo-feo/gestor-pedidos` gana `.claude/settings.json` con
el perfil normal (deny de secretos y de red, ask en `git push`, allow para lo de
todos los días), `PERMISOS.md` con el porqué de cada regla y con lo que las
reglas **no** protegen, `.gitignore`, y `secretos/pasarela.env.ejemplo`. El
archivo real, `secretos/pasarela.env`, se queda fuera de git y `PRM-016` lo
vigila. **Ningún fallo sembrado se ha tocado**: la clave sigue dentro de
`app.py`, que es justo lo que el módulo usa para enseñar el límite del sistema.

**Activos:** `entregables/plantillas/permisos/` con los tres perfiles (cauto,
normal, laboratorio) y `entregables/plantillas/devcontainer/` con el contenedor
de red restringida.

**Bookkeeping:** `fabrica/hechos.yaml` y `README.md` pasan de "3 de 12" a
"4 de 12". Hecho canónico nuevo, `ALLOW-NECESITA-CONFIANZA`.

### PARA JULIÁN

1. **Sigue abierta la fecha de corte del libro**, cuarta vez. El 04 se ha
   escrito contra la 2.1.235 y lo declara en cabecera, igual que el 02 con la
   2.1.233 y el 03 con la 2.1.234. Ya van tres módulos con versión propia: la
   opción "cada módulo declara la suya" está ganando por goleada sin que nadie
   la haya decidido. Decidirlo cuesta cinco minutos y evita reescribir el 01.
2. **El inventario del repo feo sigue sin actualizar**, tercer módulo que lo
   dice. Además de lo del 03 (`utils.py`, `config.py` y `settings.py` son código
   muerto, no lógica duplicada), el módulo 04 añade dos cosas al recorrido del
   fallo 1: el laboratorio ahora tiene `secretos/` y `PERMISOS.md`, y la clave
   de `app.py` queda **explícitamente sin resolver** hasta el módulo 12. Si
   quieres que el guion lo refleje, es una línea en la tabla del recorrido y no
   la he tocado yo porque es material compartido por los doce módulos.
3. **Decisión nueva, y es tuya.** El módulo 04 dice que la clave de `app.py` se
   saca del código en el 12. El guion de doma dice que el fallo 1 se caza "en el
   04 y en el 10". Las dos cosas no encajan del todo: o el 04 la saca (y el 10
   pierde media auditoría), o el guion pasa a decir que en el 04 se **acota** y
   en el 12 se **elimina**, que es lo que hace el texto tal como está escrito.
   He escrito el módulo con la segunda lectura porque no destruye material de
   laboratorio, pero la palabra final es tuya.

## 2026-08-19 · El módulo 04 no se escribió: colgada en un diálogo de permisos

**La rutina disparó a las 06:17 y a las 06:22 se quedó parada.** No fue el paso
0a: el agente se arregló solo lo del `fetch`, pasó el dry-run, eligió el 04, se
leyó `permission-modes`, `permissions`, `sandboxing` y `sandbox-environments`, y
empezó a medir. Murió en la llamada que devolvía el laboratorio a su sitio:

```
cp /tmp/.../settings.bak2.json .claude/settings.json
```

Escribir en un `settings.json` **copiando desde fuera del repositorio** se lee
como escalada de privilegios y pide permiso. Que el mismo archivo lo hubiera
modificado un minuto antes con un `cat > ... <<'JSON'` sin que nadie preguntara
es exactamente lo que hace que la trampa no se vea venir. Cuatro horas y media
en `requires_action` delante de un `cp`.

**Arreglado en la rutina** (19-ago, 12:53): el `git fetch origin main` va delante
en el paso 0a, y hay un **paso 0d** nuevo con la regla: lo que entra al
repositorio se escribe, no se copia; y si algo se queda esperando permiso, no se
reintenta, se cambia de camino o se termina la sesión.

**Se rescatan dos cosas de lo que sí midió**, y valen para el módulo 04:

- `claude auto-mode defaults` imprime la política del clasificador en JSON: 17
  entradas en `allow`, 66 en `soft_deny`, 1 en `hard_deny` y 20 de `environment`,
  62.957 bytes. Es una cifra propia y comprobable, mejor que cualquier paráfrasis
  de la documentación.
- **El sandbox de la nube no puede medir el efecto de `permissions.allow`**: no
  ha aceptado el diálogo de confianza del espacio de trabajo, así que ignora las
  cuatro reglas y **lo avisa por la salida de error, no por la de datos**. Con
  reglas y sin reglas dio el mismo número exacto, 43.616 tokens. Quien lo mida
  sin mirar stderr publicará que las reglas no cuestan nada, y lo que pasa es que
  no se están aplicando. Anotado en la rutina.

**La CI llevaba seis ejecuciones en rojo desde el 17-ago**, y no se había mirado.
El trabajo `verificar` pasaba; el que moría era `publicar-estado`, con `la prueba
CLI-010 tiene motivo sospechosamente largo`. El tope de 400 caracteres valía para
afirmaciones y comandos, pero el `motivo` de una prueba amarilla es prosa: ya
eran tres los que no cabían (CLI-010, CTX-012 y CTX-013, los tres del 02 y el
03). El motivo tiene ahora su propio tope de 1200. Efecto colateral que importa:
**`estado.html`, la página pública de verificación, llevaba desde el 17-ago
congelada** diciendo 30 pruebas contra la 2.1.233, mientras `ESTADO.md` ya decía
36 contra la 2.1.234. Regenerada.

### PARA JULIÁN

1. **Sigue abierta la fecha de corte**, tercera vez que se pide. Recomendación:
   que cada módulo declare su versión, que es lo que ya hacen el 02 y el 03 de
   hecho, y que la portada diga solo `v2026.08`. Un libro que promete una
   versión única del CLI nace caducado; uno que fecha cada módulo, no.
2. Falta empujar el arreglo de la CI, que el R630 no puede:
   `! git -C ~/manual-claude-code push origin main`

## 2026-08-18 · Módulo 03 · Memoria y contexto · PUBLICADO

Cerrado `manuscrito/modulo-03-memoria-y-contexto.md`, **3.989 palabras**, las
seis partes del esqueleto y runbook de una página. Verificador contra la
**2.1.234**: **36 pasan, 0 fallan, 9 a revisar, 3 omitidas**. Coherencia y
`construir.py --comprobar`, las dos en verde. Quedan nueve módulos: 04 a 12.

**La rutina publicó por primera vez.** El paso 0a no bastaba: el sandbox clona
con un `origin/main` **también** atrasado, así que `git checkout -B main
origin/main` reseteaba a un commit viejo y el dry-run seguía dando
`non-fast-forward`. Se arregla con un `git fetch origin main` **antes** del
checkout. Conviene meterlo en el paso 0a de la rutina: con el fetch delante, el
dry-run dio `Everything up-to-date` a la primera.

**Registro:** diez entradas nuevas, `CTX-004` a `CTX-013`. Once de las trece
`CTX` se comprueban solas; las dos amarillas son la medición de tokens
(`CTX-012`, marcada además con `coste: true`) y el fallo de autenticación de
`--bare` (`CTX-013`).

**Mediciones propias, dos repeticiones idénticas cada una, 2.1.234.** Mismo
repo, misma petición, variando una sola cosa:

| Estado del archivo | Tokens de entrada |
|---|---:|
| Sin `CLAUDE.md` | 42.302 |
| `CLAUDE.md` de 66 líneas | 43.480 |
| Más 40 líneas dentro de `<!-- -->` | **43.480, el mismo número exacto** |
| Esas 40 líneas visibles | 46.720 |

El comentario HTML no cuesta "poco": cuesta **cero**, al token. Y el archivo
final de 67 líneas cuesta **1.311 tokens por turno**, que es el impuesto de
contexto que declara el módulo.

**El experimento del IVA, repetido y confirmado.** Con el `CLAUDE.md` final:
solo `app.py`, 3 turnos, 131.952 y 132.003 tokens. Sin él: `settings.py`,
`utils.py` y `app.py`, 7 turnos, 216.615 y 261.009. Acierta **y** cuesta entre
1,6 y 2 veces menos. Las dos ejecuciones sin archivo se diferencian un veinte
por ciento entre sí: sin contexto, cada una explora por su cuenta.

**Hallazgos propios del módulo:**

- **El agente corrigió mi `CLAUDE.md` en directo.** El borrador citaba números
  de línea y dos estaban mal; lo detectó y avisó. La versión publicada cita
  función y literal, y el módulo lo convierte en regla de escritura: los números
  de línea envejecen en el primer commit y luego mandan al sitio equivocado con
  la autoridad de estar escritos.
- **`--bare` no sirve de diagnóstico con login de suscripción.** No lee el OAuth
  guardado, así que contesta `Authentication error · This may be a temporary
  network issue`, que no lleva a nadie hasta la causa. El módulo da la
  alternativa: apartar el archivo con `mv` y volver a preguntar.
- **El suelo de arranque son 42.302 tokens** en este repo, antes de escribir una
  palabra. Pelearse por doscientos tokens de `CLAUDE.md` es pelearse por el
  0,5 %.
- **Partir el `CLAUDE.md` en reglas sin `paths` no ahorra ni un token**: se
  cargan al arrancar con la misma prioridad. Lo que ahorra es el frontmatter.
- La documentación de hoy trae cosas que la guía del 12-ago no tenía: el
  objetivo de 200 líneas, el recorte que propone `/doctor` desde la 2.1.206, el
  hook `InstructionsLoaded`, y que el `CLAUDE.md` **se entrega como mensaje de
  usuario después del sistema**, que es el fundamento de por qué no es
  configuración impuesta.

**Laboratorio:** `D6-repo-feo/gestor-pedidos` gana `CLAUDE.md`, 67 líneas, con
la tabla de dónde vive de verdad cada valor, la lista de código muerto y quién
gana los empates. `CTX-006` vigila que nadie lo reescriba diciendo que manda
`settings.py`.

**Bookkeeping:** `fabrica/hechos.yaml` y `README.md` pasan de "2 de 12" a
"3 de 12".

### PARA JULIÁN

1. **Sigue abierta la fecha de corte del libro**, sin tocar. El módulo 03 se ha
   escrito contra la 2.1.234 y lo declara en cabecera, igual que hizo el 02 con
   la 2.1.233. Ya van dos módulos declarando versión propia, así que la opción
   "cada módulo declara la suya" está ganando de hecho aunque no se haya
   decidido. Conviene decidirlo antes del 04.
2. **El inventario del repo feo se queda corto y ya son dos módulos que lo
   dicen.** El fallo 11 del guion de doma llama "lógica duplicada" a `utils.py`,
   y lo comprobado es peor: **nadie importa `utils.py`, ni `config.py`, ni
   `settings.py`**. Son tres módulos muertos, no una duplicación. Lo sostiene
   `CTX-007`. Actualizar `D6-repo-feo/guion-de-doma.md` es trabajo de una línea
   y no lo he hecho yo porque toca el material de laboratorio de los doce
   módulos.
3. **El paso 0a de la rutina necesita el `git fetch origin main` delante**, por
   lo explicado arriba. Sin él, la rutina se va a bloquear otra vez con un error
   que parece de credenciales y no lo es.

## 2026-08-17 · Tercera ejecución: murió por límite de uso, pero dejó oro

`cse_01LZNBhNjXkAaV63WnyvQXWS`. Con GitHub ya conectado, pasó las guardas y
midió de verdad. Murió a las 18:21 con `rate_limit: rejected (five_hour)`, no
por fallo propio: se habían encadenado tres ejecuciones en la misma ventana.

**Hallazgo que salva todas las ejecuciones futuras.** El 403 del push nunca fue
de credenciales del todo: **el sandbox clona en HEAD desprendido y deja un
`main` local viejo**, así que `git push origin main` intentaba enviar una rama
cuatro commits atrasada y fallaba con `non-fast-forward`. Se arregla con
`git checkout -B main origin/main` antes de nada. Ya está en el paso 0a de la
rutina. También dejó una rama de prueba `zz-cred-check` que no pudo borrar por
un fallo de sideband del proxy; se borró a mano desde el R630.

**Mediciones, con dos repeticiones idénticas cada una.** Sirven de patrón para
el módulo, no como cifras del libro (dependen de la máquina):

| Medida | Tokens de entrada |
|---|---:|
| `gestor-pedidos` sin `CLAUDE.md` | 39.625 |
| con `CLAUDE.md` de 58 líneas | 40.754 |
| **coste del archivo** | **1.129** |
| relleno dentro de comentario HTML | 40.754 |
| el mismo relleno visible | 44.594 |
| **lo que ahorra el comentario** | **3.840** |

**El experimento del laboratorio, que es el corazón del módulo 03.** Misma
petición ("sube el IVA de Portugal del 23 al 24, dime qué tocar"), mismo repo,
lo único distinto el `CLAUDE.md`:

| | Sin `CLAUDE.md` | Con `CLAUDE.md` |
|---|---|---|
| Respuesta | `settings.py:5`, `utils.py:23` y `app.py:74` | solo `app.py:74` |
| Correcta | **no**, dos de tres archivos están muertos | sí |
| Tokens de entrada | 209.868 | 85.217 |
| Turnos | 8 | 2 |

El archivo de memoria no solo lo hace acertar: lo hace costar **2,5 veces
menos**. Ese contraste vale el módulo entero.

**Fallo nuevo del laboratorio, no inventariado.** `utils.py` **no lo importa
nadie**, así que el módulo entero está muerto, incluida `calcular_iva()`, que
parece la función buena del IVA. El `guion-de-doma.md` lo lista como
"lógica duplicada" (fallo 11) y es peor que eso: es lógica muerta que atrae
cambios. Añadir al inventario.

## 2026-08-17 · La guardia funciona, y el bloqueo sigue

Segunda ejecución (`cse_018J8jRAL6L4rwo6o8VJCvyy`) con el paso 0a puesto:
**paró en 47 segundos sin escribir nada.** Antes eran treinta minutos tirados.

Su diagnóstico, mejor que el nuestro: no hay `credential.helper`, el proxy del
sandbox está sano (`recentRelayFailures` vacío, `gitConfigInjection` activo), y
la API de GitHub por MCP devuelve 503. **El 403 es de autorización, no de red.**

Comprobado desde el R630 el mismo minuto: GitHub "All Systems Operational", cero
incidentes, su API responde 200. El 503 del sandbox y el 500 de `/web-setup` son
del lado de Anthropic.

**Estado de las dos vías para desbloquear:**

- `/web-setup` sincroniza el token del `gh` local. En el R630 `gh` ya está
  autenticado como `julian-najas` con permisos `repo` y `workflow`, o sea que la
  materia prima está lista. El comando devolvió 500 el 17-ago; hay que
  reintentarlo.
- La Claude GitHub App, en `https://github.com/apps/claude`, no pasa por el
  servidor que está fallando. Instalarla en el repositorio no es obligatorio
  para que la sesión pueda empujar.

Cualquiera de las dos vale. Hasta que haya una, la rutina para en 47 segundos
cada mañana en vez de trabajar en balde.

## 2026-08-17 · Primera ejecución de la rutina: escribió el 03 y lo perdió

**El módulo 03 se escribió entero y no llegó a publicarse.** La ejecución de
prueba (`cse_013jyT7FnGxu85HXcXvgyvPi`) hizo el trabajo bien: 4.005 palabras,
seis partes, `CLAUDE.md` del laboratorio, entradas nuevas en el registro,
coherencia en verde, commit `07b30e6`. Y el push murió:

```
fatal: unable to access 'https://github.com/julian-najas/manual-claude-code/':
The requested URL returned error: 403
```

**Causa:** el sandbox de la nube clona sin credenciales (basta con que el repo
sea público) pero **no tiene credenciales de escritura**. Un push anónimo
siempre da 403. Falta conectar GitHub, con `/web-setup` desde el terminal o
autorizando la Claude GitHub App. Según `claude-code-on-the-web.md`, instalar la
App en el repositorio no es obligatorio: vale cualquiera de las dos vías.

**Culpa del montaje, no del agente.** La rutina se creó llamando a la API
directamente en vez de por el flujo interactivo, y así se salta el aviso que
`/schedule` da cuando no hay acceso de escritura.

**Arreglado ya:** la rutina hace ahora `git push --dry-run` como **paso 0a** y
para en seco si no puede publicar, sin escribir una línea. Media hora de máquina
en vez de treinta minutos tirados.

**Lo que se salvó del naufragio.** La ejecución destapó tres defectos reales del
verificador, y esos sí están arreglados y commiteados:

- `REPO-002` y `REPO-003` daban rojo por el proxy del sandbox (403), no porque
  el companion se hubiera caído.
- `CLI-007` daba por hecho una instalación nativa que en la nube no existe.
- De fondo: el verificador no distinguía **"es falso"** de **"no he podido
  comprobarlo"**. Ahora una prueba de red caída sale amarilla con el motivo
  escrito, y un 404 sigue siendo rojo.

## Próxima iteración · Módulo 03 · Memoria y contexto

**No empezado.** La iteración del 17-ago se cortó por límite de uso antes de
escribir una línea, y no se dejó un módulo a medias a propósito. Lo recoge la
rutina de la nube en su primera ejecución.

Preparación ya hecha, para no repetirla:

- Fuente principal: `guia-21/M4-memoria-y-contexto.md`, leído y utilizable.
- Contrato: sección "Módulo 03" de `manuscrito/ESQUELETO.md`. IDs ya en el
  registro: `CTX-001` (`--add-dir`), `CTX-002` (`--autocompact`), `CTX-003`
  (`--bare`). Habrá que añadir entradas nuevas.
- Documentación oficial **pendiente de descargar de nuevo** (la regla es
  descargarla en cada módulo, no reutilizar la de otra sesión):
  `memory.md`, `context-window.md`, `claude-directory.md`, `settings.md`.
- Laboratorio: `D6-repo-feo/gestor-pedidos`, que ya tiene `.claude/settings.json`
  y `ENTORNO.md` del módulo 02. El `CLAUDE.md` lo escribe este módulo.
- **La trampa del laboratorio, ya documentada como hecho canónico
  `CONFIG-NINGUNO-SE-USA`:** la respuesta a "qué configuración manda" es
  **ninguna de las dos**. Ni `config.py` ni `settings.py` se importan; `app.py`
  fija sus valores a mano (`DB`, `DEBUG`, el IVA y el tope de 50 líneas). El
  módulo tiene que llevar al lector hasta ahí, no hasta "manda settings.py".
- El código muerto que el `CLAUDE.md` debe declarar: `/pedido_old/<id>`, que lee
  la tabla `pedidos_2019` (fallo 6 del guion de doma).

## 2026-08-17 · Módulo 02 · Instalación, autenticación y versiones

Cerrado `manuscrito/modulo-02-instalacion.md`, 3.849 palabras, las seis partes
del esqueleto y runbook de una página. Verificador en verde: **30 pasan, 0
fallan, 5 a revisar, 3 omitidas** contra 2.1.233. Quedan diez módulos: 03 a 12.

Añadidas al registro nueve entradas nuevas (CLI-004 a CLI-010, AUT-001, ENT-001,
ENT-002). Las cinco amarillas son manuales justificadas: HOK-001, MCP-002,
TRB-002 (trimestrales de siempre) y las dos nuevas, CLI-010 y AUT-001.

**Hallazgos propios del módulo, no copiados de la guía de 21:**

- `claude doctor` **termina en 0 aunque reporte `Invalid settings`**, y sigue
  imprimiendo `No installation issues found`. Una comprobación de CI que mire
  solo el código de salida da verde con la configuración del proyecto rota.
- Un nombre de clave mal escrito en `settings.json` **no se reporta en
  absoluto**. Los valores inválidos de claves conocidas sí, y con detalle.
- El binario acepta un tercer canal, **`rc`**, que no aparece en `setup.md` ni
  en `settings.md`. Marcado en caja "esto va a cambiar", no recomendado.
- La precedencia de credenciales **eran cuatro niveles en nuestra guía y hoy son
  siete**. Corregido en el manuscrito y anotado como recuento trimestral.
- `--help` es **byte a byte idéntico entre 2.1.228 y 2.1.233** (242 líneas),
  mientras la documentación condiciona comportamiento a 14 versiones distintas.
  Eso reorienta el módulo entero: la versión no quita comandos, cambia lo que
  hacen.

**Laboratorio:** `D6-repo-feo/gestor-pedidos` gana `.claude/settings.json` y
`ENTORNO.md`. Verificado que el archivo se carga de verdad: `claude doctor`
dentro del repo dice `Auto-update channel: stable` y fuera dice `latest`. Ese
contraste es el criterio PASA del módulo.

**Bookkeeping:** `fabrica/hechos.yaml` y `README.md` pasan de "1 de 12" a
"2 de 12". Coherencia y `construir.py --comprobar`, las dos en verde.

### PARA JULIÁN

1. **La fecha de corte del libro.** El esqueleto y el módulo 01 dicen "verificado
   contra 2.1.228, corte 12-ago-2026". La máquina va por la 2.1.233 y el
   verificador lleva días publicando estado contra 2.1.231, 2.1.232 y 2.1.233.
   El módulo 02 se ha escrito contra la 2.1.233 y lo declara en su cabecera, en
   vez de fingir. Decisión tuya: **recortar el libro entero a la versión del día
   de publicación** (tocar el esqueleto, el módulo 01 y la página de
   verificación), o **dejar el corte en 2.1.228 y que cada módulo declare la
   suya**. No lo he decidido yo porque afecta a la portada.
2. **El orden de escritura.** El esqueleto recomienda escribir el 02 el último
   ("es el que más envejece"). La orden del bucle es por número, así que va el
   segundo. No lo he cambiado, pero el módulo 02 va a necesitar un repaso corto
   justo antes de publicar, y conviene que esté presupuestado.
