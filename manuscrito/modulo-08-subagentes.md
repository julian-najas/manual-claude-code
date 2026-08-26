# Módulo 08 · Subagentes

> **Laboratorio de este módulo:** ~60 minutos · veintinueve ejecuciones, unos
> **2.350.000 tokens de entrada** y 44.000 de salida · **4,29 dólares** según la
> telemetría del propio CLI, que a cualquier cambio euro-dólar de agosto de 2026
> se queda **por debajo de 4,70 €**. Con suscripción va incluido.
> **Verificado contra:** Claude Code 2.1.246 · 26 de agosto de 2026 · modelo
> principal Sonnet 5.

> **Nota de versión.** Es el módulo más caro del libro, y con motivo: cada fila
> de la tabla central es una auditoría entera de `app.py`, no una petición
> trivial. Un subagente que revisa código gasta lo que gasta un revisor.

---

## 8.1 · Síntoma

Le pides que revise su propio trabajo y te dice que está bien. Le insistes y te
dice que está bien con más palabras. Y tú tienes la sensación, sin poder
demostrarla, de que el problema no es que mienta: es que mira lo que acaba de
escribir con los mismos ojos con los que lo escribió.

Así que montas un subagente revisor, que es lo que dice todo el mundo, y el
informe que vuelve es más largo, más ordenado y encuentra lo mismo. Has pagado el
doble por una segunda opinión que no lo era.

Este módulo mide por qué, y las dos causas no son las que se cuentan.

---

## 8.2 · Modelo mental

### 8.2.1 · Lo que un subagente se lleva de tu ventana

Un subagente es un trabajador delegado **dentro de tu sesión**: arranca con su
propia ventana, su propio prompt de sistema y sus propias herramientas, hace la
tarea y **lo único que vuelve es su informe**. Ni sus lecturas, ni sus búsquedas,
ni sus vueltas atrás. Una sola variable, quién lee `app.py`:  ‹v2.1.246›

| Quién revisa `app.py` | Tokens en **tu** ventana | Coste de la ejecución |
|---|---:|---:|
| El agente principal, él mismo | 146.114 y 244.588 | 0,11 $ y 0,13 $ |
| Un subagente, delegando | 53.916 y 53.513 | 0,28 $ y 0,24 $ |

Dos lecturas, y las dos importan.

**La ventana del que delega no depende de lo que el subagente lea.** Las dos
ejecuciones del principal se separan en casi cien mil tokens, porque cada una
abrió lo que le pareció; las dos delegadas, en cuatrocientos. **Una sesión que
delega no se ahoga por una tarea que se hizo grande.**

**Y la factura va al revés.** Los tokens del subagente no salen en tu ventana,
pero sí en tu recibo, y con recargo: arranca de cero, así que vuelve a leer lo
que tu sesión ya tenía. Delegar salió **más del doble de caro** las dos veces.

> **Un subagente no ahorra dinero. Compra contexto con dinero.** Es un cambio de
> moneda, y solo interesa cuando el contexto es lo que te falta.

### 8.2.2 · Lo que cuesta tenerlo declarado

Eso era ejecutarlo; esto es que exista. Misma petición trivial de siempre
(`Responde solo con la palabra OK.`), dos repeticiones por fila, **idénticas al
token**:  ‹v2.1.246›

| Estado del repositorio | Tokens de entrada |
|---|---:|
| Sin ningún subagente declarado | 45.977 |
| Con uno (descripción de 199 caracteres) | 46.088 |
| Con **seis** (1.227 caracteres de descripción en total) | 46.610 |
| El mismo de una fila, con **21.228 caracteres de prompt** | **46.088** |

**Unos 105 tokens por subagente declarado.** Y la última fila cambia cómo se
escriben: veintiún mil caracteres de prompt de sistema cuestan **cero** en tu
ventana. El cuerpo vive en la ventana del subagente, y ahí no llega hasta que se
invoca.

Es la forma que el módulo 07 midió para las skills, a mitad de precio: una skill
instalada son 208 tokens por turno; un subagente, 105. Pero hay una diferencia
que muerde, y va en la dirección contraria:  ‹v2.1.246›

| Longitud de la descripción | Tokens de entrada |
|---:|---:|
| 1.536 caracteres | 46.588 |
| 5.616 caracteres | **48.068** |

**La descripción de un subagente no se corta.** La de una skill se recorta a
1.536 caracteres, y por eso el módulo 07 avisaba de que la segunda mitad no
existe. Aquí existe toda y se paga toda: 5.616 caracteres son **2.091 tokens por
turno**. La regla del módulo 07 vale igual y aprieta más: **corto arriba, largo
abajo.** Arriba no hay tope que te proteja.

### 8.2.3 · Lo que sí hereda, y por qué te arruina la revisión

Aquí está la mitad del módulo, y no la esperábamos.

Un subagente arranca sin tu conversación, sin tus archivos leídos y sin tus
skills invocadas. Pero **no arranca sin tu `CLAUDE.md`**: la jerarquía de memoria
entera, la del módulo 03, se carga en cada subagente igual que en la sesión
principal. Se salvan solo los integrados de exploración y de plan.

Y el `CLAUDE.md` del laboratorio, escrito en el módulo 03 y perfectamente
razonable, termina así:

```text
Este repositorio tiene fallos de seguridad deliberados, incluida una clave de
pasarela de pago en claro en app.py. Es material de laboratorio del manual
"Claude Code en producción". No se despliega. No hace falta que avises de
esos fallos en cada respuesta: están inventariados.
```

Mismo subagente revisor, mismo `app.py`, misma pregunta. Una sola variable: ese
párrafo, 309 caracteres, quitado o puesto.  ‹v2.1.246›

| `CLAUDE.md` del laboratorio | ¿Reporta la clave de pasarela en producción? |
|---|---|
| Tal cual, 2.857 caracteres | **0 de 2**, y lo dice por escrito |
| Sin el último párrafo, 2.548 caracteres | **2 de 2**, como hallazgo bloqueante |

Y no lo calla en silencio, que sería peor. Lo escribe en la primera línea del
informe: "Los hallazgos siguientes excluyen lo ya inventariado en CLAUDE.md
(clave de pasarela en claro, valores de configuración fijados a mano, IVA
duplicado)".

> **Tu archivo de memoria le está diciendo a tu revisor qué no tiene que
> mirar.** No es un fallo del CLI: hace exactamente lo documentado. Es que una
> frase escrita para que el agente no repita lo obvio en cada respuesta se
> convierte, en boca de un auditor, en una lista de temas prohibidos.

De ahí la regla que este libro añade al módulo 03: **lo que escribas en el
`CLAUDE.md` para ahorrarte ruido se lo dices también a quien te audita.** Si tu
memoria tiene una sección de "esto ya lo sabemos", tu revisor no la mira, tampoco
el día que uno de esos fallos pase de conocido a explotado.

### 8.2.4 · Lo que decide de verdad qué encuentra

La otra mitad. El laboratorio tiene tres fallos sembrados que el manual persigue
desde el módulo 01: SQL por concatenación (fallo 2), una función que hace ocho
cosas (fallo 3) y el IVA español cobrado a cualquier país por defecto (fallo 4).
Tres condiciones, dos repeticiones cada una, contadas sobre el informe:  ‹v2.1.246›

| Quién revisa | Fallo 2, inyección | Fallo 3, responsabilidades | Fallo 4, IVA por defecto |
|---|---|---|---|
| El agente principal, "revisa app.py" | **2 de 2** | 0 de 2 | 0 de 2 |
| Subagente con contrato de auditor | **2 de 2** | 0 de 2 | 1 de 2 |
| Subagente con **criterio de aceptación en tres preguntas** | **2 de 2** | **2 de 2** | **2 de 2** |

La segunda fila desmonta el consejo de siempre. **Ponerle un revisor aparte, por
sí solo, no movió la aguja**: encontró lo mismo que el principal, con más detalle
y por el doble de precio. Uno de los dos rozó la rama del IVA; el otro la excluyó
citando el `CLAUDE.md`. No es un segundo par de ojos: es el mismo par, mejor
peinado.

Lo que sí movió la aguja fue cambiar el **criterio de aceptación** por tres
preguntas que el informe está obligado a contestar:

```text
Tu informe NO está terminado hasta que conteste estas tres preguntas, cada
una con archivo y línea:
1. ¿Qué dato que viene de fuera llega hasta una sentencia SQL, y por qué camino?
2. ¿Cuántas responsabilidades distintas tiene cada función de más de veinte
   líneas? Enuméralas una a una.
3. ¿Qué hace cada rama else y cada valor por defecto cuando el caso real no es
   el que su autor tenía en la cabeza? Recórrelas una a una.
```

Con eso, dos de dos: **nueve responsabilidades contadas** en `procesar_pedido()`
y la rama del IVA nombrada con su caso de rotura (`"pais": "FR"` factura al 21 %
español, sin error y sin registro). Ninguna de las tres preguntas nombra un
fallo: nombran **dónde mirar**, que es lo que un autor nunca se pregunta sobre lo
suyo.

> **Un subagente no aporta criterio distinto. Aporta un sitio donde ponerlo.**
> El aislamiento es el envase; el criterio de aceptación es el contenido. Un
> revisor sin criterio de aceptación propio es el autor con otro sombrero.

### 8.2.5 · Y el autor, ¿de verdad se da el visto bueno?

Se midió y salió que no. Dos ejecuciones: escribir un endpoint nuevo en `app.py`
"siguiendo el estilo del archivo" y revisarse a continuación. Las dos veces **se
negó a copiar la inyección SQL del archivo** y las dos veces contestó que el
repositorio no está listo para producción. El visto bueno automático **no se
reprodujo**.  ‹v2.1.246›

Lo que sí se reprodujo, dos de dos, fue más fino: **"mi cambio es seguro"**. El
autor revisó el alcance que él mismo eligió y delegó lo demás en "está
inventariado". No hubo complacencia: hubo un alcance elegido por la misma cabeza
que escribió el código, que es la definición operativa del sesgo del autor.

### 8.2.6 · Fork, el subagente que sí ve tu conversación

Un **fork** (bifurcación) hereda la conversación entera en vez de arrancar de
cero: mismo prompt de sistema, mismas herramientas, mismo historial. Se lanza con
`/subtask`  ‹v2.1.212› y desde la 2.1.232 está encendido por defecto en sesiones
interactivas  ‹v2.1.232›. Sus llamadas siguen sin ensuciar tu ventana y
**comparte tu caché de prompt**, así que sale más barato que un subagente fresco.

La contrapartida es lo que este módulo persigue: **un fork hereda tu sesgo con tu
contexto.** Para explorar dos caminos desde el mismo punto, perfecto. Para
revisar, es el autor otra vez.

---

## 8.3 · Receta

### 8.3.1 · Individual: el contrato en cuatro casillas

Un subagente es un markdown con encabezado en YAML. Solo `name` y `description`
son obligatorios, y el cuerpo es su prompt de sistema. Las cuatro casillas, en
este orden:

1. **Rol.** Una frase. "No escribiste este código y esa es tu ventaja" hace más
   trabajo que tres párrafos de instrucciones.
2. **Límites.** `tools` como lista blanca, `disallowedTools` como lista negra. Un
   revisor sin `Edit` ni `Write` no puede arreglar lo que encuentra, y eso es la
   característica.
3. **Criterio de aceptación.** Las preguntas que el informe está obligado a
   contestar. **Es la casilla que decide qué encuentra**, y la que casi nadie
   escribe.
4. **Formato de salida.** Qué vuelve y ordenado cómo. Entra en tu ventana, así
   que aquí también se paga.

Un detalle que ahorra una tarde: si al archivo le falta `name`, le falta
`description`, o el YAML no parsea, **Claude Code se lo salta sin decírtelo en la
sesión** y escribe el motivo en el registro de depuración. Se comprueba antes de
arrancar y sin gastar nada:

```bash
claude plugin validate .claude/agents
```

Devuelve `Validation passed` o te nombra el archivo roto.  ‹v2.1.233›

### 8.3.2 · Dónde vive y quién gana

| Dónde | Ruta | Prioridad |
|---|---|---|
| Organización | Configuración gestionada | 1, gana a todo |
| Sesión | Bandera `--agents` con JSON | 2 |
| Proyecto | `.claude/agents/<lo-que-sea>.md` | 3, **y va a git** |
| Personal | `~/.claude/agents/<lo-que-sea>.md` | 4 |
| Plugin | `<plugin>/agents/` | 5 |

Cuatro cosas que no se deducen de la tabla:

- **La precedencia va al revés que en las skills.** Ahí la personal tapaba a la
  del proyecto; aquí manda **la del proyecto**. Un revisor versionado en el
  repositorio no lo desactiva nadie desde su carpeta personal.
- **La identidad la da el campo `name`, no el archivo ni la carpeta.** Dos `name`
  iguales en el mismo árbol cargan uno solo, elegido por el orden del sistema de
  archivos. `/doctor` los caza.
- **`--agents` no toca el disco**, y por eso va por ahí todo lo medido aquí: un
  experimento que depende de que un archivo esté en su sitio mide dos cosas a la
  vez.  ‹v2.1.246›
- **Los de plugin ignoran `hooks`, `mcpServers` y `permissionMode`.** Es a
  propósito. Si los necesitas, el archivo se copia al proyecto.

### 8.3.3 · Equipo: los seis contratos

En `entregables/plantillas/agents/`, con las cuatro casillas escritas y las
herramientas recortadas:

| Subagente | Para qué | Herramientas |
|---|---|---|
| `revisor` | Revisar un cambio con criterio de auditor | solo lectura |
| `auditor-seguridad` | Buscar lo explotable en un endpoint | solo lectura |
| `investigador` | Contestar una pregunta sin llenarte la ventana | solo lectura |
| `validador` | PASA o FALLA con la salida real del comando | lectura y pruebas |
| `probador` | Escribir la prueba que falla antes de tocar nada | escritura y pruebas |
| `arqueologo` | Reconstruir por qué el código está así | lectura e historial |

Los que auditan son de solo lectura por la misma razón: **el que audita no
arregla.** Uno que pueda editar arregla lo primero que ve, y lo que vuelve
entonces no es un informe, es un cambio que nadie ha revisado.

### 8.3.4 · Cuándo un subagente sale caro

Cuatro casos donde la respuesta correcta es otra cosa, y los cuatro salen de lo
medido arriba:

**Cuando la tarea es corta.** Vuelve a pagar el contexto que tu sesión ya tenía.
Por debajo de una tarea que se coma decenas de miles de tokens, el cambio de
moneda sale a perder.

**Cuando hace falta ir y venir.** Cada invocación arranca una instancia nueva. Se
reanuda por nombre, pero si la tarea es una conversación, es tuya.

**Cuando quieres imponer algo.** Lo que no sea negociable es un hook, módulo 05.

**Cuando no le has escrito criterio de aceptación.** Sin él pagas el doble por el
mismo informe.

---

## 8.4 · Laboratorio · Un revisor que encuentra lo que el autor no

Del módulo 07 traes una skill que se dispara sola. Hoy el repositorio gana lo
primero que le lleva la contraria.

**Paso 1. Comprueba el síntoma.** Pídele que añada un endpoint y que se revise:

```bash
cd D6-repo-feo/gestor-pedidos
claude -p "Añade a app.py un endpoint GET /cliente/<nombre> que devuelva los pedidos de ese cliente, siguiendo el estilo del archivo. Cuando termines, revisa tu propio trabajo y dime si esta listo para subir a produccion." \
  --allowedTools "Read,Edit,Write,Grep,Glob"
```

Fíjate en lo que **no** hace: no cuenta responsabilidades, no recorre ramas por
defecto, y cierra con "mi cambio es seguro". Deshaz el cambio antes de seguir.

**Paso 2. Escribe el contrato, y pruébalo sin tocar el disco.** El archivo del
libro está en `entregables/plantillas/agents/revisor.md` y su sitio en ejecución
es `.claude/agents/revisor.md`. Para el experimento no hace falta ninguno:
`--agents` acepta el mismo contrato en JSON, con el prompt de sistema en el campo
`prompt`.

```bash
claude -p "Delega en el subagente revisor la revisión de app.py y devuélveme su informe tal cual." \
  --allowedTools "Read,Grep,Glob,Agent" --agents "$(cat revisor.json)"
```

**Paso 3. Comprueba que delegó, en la traza y no en la respuesta.** Igual que en
el módulo 06 con las herramientas MCP:

```bash
claude -p "..." --output-format stream-json --verbose \
  | jq -r 'select(.type=="assistant") | .message.content[]?
           | select(.type=="tool_use") | .name'
```

Tiene que salir `Agent`. Si no sale, el informe lo escribió tu sesión principal y
el resto del laboratorio no mide nada.

**Paso 4. Cuenta los tres fallos.** Sobre el informe que vuelve: la inyección
(fallo 2), las responsabilidades de `procesar_pedido()` (fallo 3) y la rama por
defecto del IVA (fallo 4). A nosotros, con un contrato de auditor bien escrito,
nos salieron **el 2 las dos veces, el 3 ninguna y el 4 una de dos**. Es el
resultado incómodo del módulo y conviene verlo con los ojos propios.

**Paso 5. Cambia el criterio de aceptación, y solo eso.** Añade al contrato las
tres preguntas de 8.2.4. No toques el rol, ni las herramientas, ni la
descripción. Repite el paso 4: **tres de tres, dos de dos.**

**Paso 6. Encuentra el bozal tú mismo.** Copia el laboratorio a un lado, quita
del `CLAUDE.md` el último párrafo (el de "están inventariados") y repite el paso
2 contra la copia. Compara los dos informes buscando `API_KEY_PASARELA`: con el
párrafo puesto no aparece y el informe explica por qué; sin él es hallazgo
bloqueante. **309 caracteres de tu archivo de memoria.**

**Paso 7. Mide lo que cuesta tenerlo declarado.** La petición trivial de siempre,
con `--agents` y sin él: 46.088 frente a 45.977. **111 tokens.** Infla ahora el
campo `prompt` a veinte mil caracteres y repite: el mismo número exacto. Luego
infla la **descripción** a cinco mil, y mira cómo esa sí sube.

**Paso 8. Mide el cambio de moneda.** De los pasos 1 y 2, guarda tokens de
entrada y coste (`--output-format json`, campos `usage` y `total_cost_usd`). La
ventana baja de seis cifras a cincuenta y pico mil; la factura sube al doble.
Publica tus números, no los nuestros.

**Paso 9. Escribe el porqué.** `AGENTES.md`, al lado de `HOOKS.md`, `MCP.md` y
`SKILLS.md`: qué revisor hay, qué preguntas contesta, qué no puede hacer y **qué
le esconde el `CLAUDE.md`**. El del laboratorio está en
`D6-repo-feo/gestor-pedidos/AGENTES.md`.

---

## 8.5 · Prueba

**PASA** si se cumplen las cuatro:

1. Tu revisor encuentra los **fallos 2, 3 y 4** en dos ejecuciones seguidas, y la
   traza confirma que quien los encontró fue el subagente.
2. Puedes enseñar el par de informes del paso 6 y señalar la frase de tu
   `CLAUDE.md` que decide si aparece la clave de pasarela.
3. Tienes tus dos números del cambio de moneda: cuánto contexto ahorras y cuánto
   dinero cuesta ahorrarlo.
4. `AGENTES.md` está en el control de versiones y dice **qué no mira** tu revisor.

**FALLA** si tu conclusión es que ya tienes segunda opinión porque tienes un
revisor. En nuestra medición, un revisor aislado con contrato de auditor y sin
criterio de aceptación propio encontró **lo mismo que el agente principal** y
costó el doble. El aislamiento no es criterio: es un sitio vacío donde ponerlo.

> **Esto va a cambiar.** Las cuentas de hallazgos son estadística de un modelo,
> no una propiedad del CLI: las nuestras son del 26 de agosto de 2026, con la
> 2.1.246, Sonnet 5 y un solo subagente declarado. Y la zona se mueve rápido: el
> anidamiento por defecto ha sido cinco, luego uno y hoy son tres capas
>  ‹v2.1.219›, el tope de veinte subagentes concurrentes llegó en la 2.1.217
>  ‹v2.1.217›, el de 200 por sesión se eliminó, y desde la 2.1.210 el informe de
> un subagente pasa por un escaneo antes de que tu sesión lo lea  ‹v2.1.210›. Lo
> que esperamos que aguante es la forma: quien hereda tu memoria hereda tus
> puntos ciegos, y el criterio de aceptación decide el hallazgo.

---

## 8.6 · Coste de este módulo

| Concepto | Cantidad |
|---|---|
| Tokens de entrada del laboratorio | ~2.350.000 |
| Tokens de salida | ~44.000 |
| Coste medido por el CLI | 4,29 dólares |
| Coste en euros | por debajo de 4,70 € |
| Tiempo | 60 minutos |
| **Impuesto de contexto, por subagente declarado** | **~105 tokens por turno** |
| Prompt de sistema del subagente, sin invocar | **0 tokens** |
| Descripción de 5.616 caracteres | 2.091 tokens por turno |
| **Sobrecoste de delegar una revisión** | **×2 en dinero, ÷3 en contexto** |
| Mantenimiento continuo | releer el criterio de aceptación cuando cambie lo que os importa |

La tabla comparada, todo en la misma máquina y con la misma petición trivial:

| Pieza | Coste por turno |
|---|---:|
| Reglas de permisos, módulo 04 | 0 |
| Hooks declarados, módulo 05 | 0 |
| Prompt de un subagente, sin invocar | **0** |
| Un subagente declarado, este módulo | **105** |
| Una skill instalada, módulo 07 | 208 |
| Un servidor MCP de tres herramientas, módulo 06 | 218 |
| `CLAUDE.md` de 67 líneas, módulo 03 | 1.311 |
| Descripción de subagente de 5.616 caracteres | **2.091** |

Un subagente declarado es **lo más barato de tener** de las seis piezas que
llevamos: la mitad que una skill y que un servidor MCP entero. La última fila es
el contrapeso: una descripción larga de subagente es lo **segundo más caro que se
escribe a mano** en todo el libro, solo por detrás del archivo de memoria, y a
diferencia de las skills nadie la corta por ti.

El coste real no está en ninguna de esas filas. Está en la línea del ×2: **la
revisión delegada cuesta el doble que la propia**. Merece la pena cuando el
contexto es lo escaso y cuando el informe trae algo que el principal no traía. Si
tu revisor devuelve lo mismo con mejor tipografía, has comprado tipografía.

El mantenimiento tampoco es el archivo: es que **el criterio de aceptación
envejece con vosotros**. Las tres preguntas que hoy destapan nueve
responsabilidades y una rama de IVA son las de este repositorio en agosto de
2026. Revísalas con la cadencia del `when_to_use` del módulo 07.

Queda pendiente lo de siempre: la clave sigue dentro de `app.py`, y hoy sabemos
que hay una frase del `CLAUDE.md` que impide reportarla. Quitarla es decisión de
equipo, no del que escribe el revisor. Módulo 10.

---

## Runbook · Módulo 08

> **"Mi revisor encuentra lo mismo que el agente principal"**
>
> 1. ¿Tiene **criterio de aceptación**, o solo rol y límites? Es lo único que
>    movió la aguja: 0 de 2 sin él, 2 de 2 con él, sobre los mismos fallos.
> 2. Escríbelo como **preguntas que el informe está obligado a contestar**.
>    Nombra dónde mirar, nunca qué vas a encontrar.
> 3. ¿Puede editar? Quítale `Edit` y `Write`. El que arregla deja de auditar.
>
> **"Mi revisor no reporta algo que está claramente mal"**
> Mira tu `CLAUDE.md`. **La jerarquía de memoria entera llega al subagente**,
> integrados de exploración y de plan aparte. Una frase del tipo "esos fallos ya
> están inventariados" apaga ese hallazgo: 0 de 2 con la frase, 2 de 2 sin ella.
> Suele decirlo en la primera línea de su informe: búscalo.
>
> **"No sé si delegó"**
> `--output-format stream-json --verbose` y busca `Agent` en las llamadas. En la
> respuesta no se ve.
>
> **"Mi subagente no aparece"**
> `claude plugin validate .claude/agents`. Sin `name`, sin `description` o con
> YAML roto se salta el archivo **sin decírtelo en la sesión**. Si el directorio
> `agents` no existía al arrancar, hay que reiniciar.
>
> **Dónde vive y quién gana**
> Organización → `--agents` → **proyecto** → personal → plugin. Al revés que en
> las skills: aquí **la del proyecto gana a la personal**. La identidad es el
> campo `name`, no el archivo.
>
> **Lo que cuesta**
> Declarado: ~105 tokens por turno. Prompt de sistema sin invocar: cero, aunque
> tenga veinte mil caracteres. **La descripción no tiene tope**: 5.616 caracteres
> son 2.091 tokens por turno. Ejecutarlo: la ventana baja de ~146.000 a ~54.000 y
> la factura sube al doble. **Compra contexto con dinero.**
>
> **Cuándo NO**
> Tarea corta · conversación de ida y vuelta · algo no negociable (hook, módulo
> 05) · sin criterio de aceptación escrito.
>
> **Fork**
> `/subtask` hereda tu conversación y tu caché, así que sale más barato.
>  ‹v2.1.212› Bueno para explorar dos caminos. **Inútil para revisar: hereda tu
> sesgo.**
