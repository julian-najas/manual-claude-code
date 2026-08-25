# Módulo 07 · Skills y plugins

> **Laboratorio de este módulo:** ~50 minutos · veintiuna ejecuciones, unos
> **2.600.000 tokens de entrada** y 19.000 de salida · **1,49 dólares** según la
> telemetría del propio CLI, que a cualquier cambio euro-dólar de agosto de 2026
> se queda **por debajo de 1,60 €**. Con suscripción va incluido.
> **Verificado contra:** Claude Code 2.1.245 · 25 de agosto de 2026.

> **Nota de versión.** Es el módulo más caro del libro hasta ahora, y por una
> razón que conviene decir: aquí no se mide un número, se mide **con qué
> frecuencia pasa algo**. Eso obliga a repetir, y repetir cuesta. Cada fila de
> disparo de abajo son cuatro u ocho ejecuciones, no dos.

---

## 7.1 · Síntoma

Te leíste la documentación, escribiste la skill entera, la dejaste preciosa, y
no se activa nunca sola. Tú la invocas con su nombre y funciona de maravilla. El
resto del equipo no la usa porque no sabe que existe, y el agente, que sí sabe
que existe, no la usa tampoco.

Así que la conclusión a la que llega todo el mundo es que la descripción está
mal escrita, y a la tercera reescritura sigue sin dispararse. La conclusión es
media verdad. Este módulo mide cuál es la mitad.

---

## 7.2 · Modelo mental

### 7.2.1 · Qué entra en contexto y cuándo

Una skill son dos cosas en un archivo: un **frontmatter** (encabezado) en YAML y
un cuerpo en markdown. Y lo que hay que entender de ella es que **esas dos
partes no se cargan a la vez**.

- El **frontmatter** viaja en el catálogo de skills, en cada turno de cada
  sesión. Es lo que el modelo lee para decidir.
- El **cuerpo** no está. Se carga cuando la skill se invoca, y a partir de ahí
  se queda en la conversación.

Eso es la divulgación progresiva (progressive disclosure), y no hay que
creérsela: se mide. Misma petición trivial, mismo repositorio, dos repeticiones
por fila, y las cuatro **idénticas al token**:  ‹v2.1.245›

| Estado del repositorio | Tokens de entrada |
|---|---:|
| Sin ninguna skill instalada | 45.752 |
| Con la skill del laboratorio | 45.960 |
| La misma skill, con **20.000 caracteres más de cuerpo** | **45.960** |

Veinte mil caracteres añadidos al cuerpo cuestan **cero**. Los 208 tokens de
diferencia son el frontmatter, y se pagan siempre.

De ahí sale la regla de escritura del módulo, que es exactamente la contraria de
lo que hace la gente: **corto arriba, largo abajo.** Arriba se paga por línea en
cada turno; abajo es gratis hasta que se usa.

### 7.2.2 · Lo que decide de verdad que se dispare

Aquí está el módulo. Veinticuatro ejecuciones sobre el mismo repositorio,
cambiando **una sola cosa** cada vez, y con el disparo contado en la traza de la
sesión, no deducido de la respuesta:  ‹v2.1.245›

| Lo que pide el usuario | Descripción de la skill | Se disparó |
|---|---|---|
| "Échale un vistazo al endpoint `/buscar` de `app.py`" | de catálogo, 43 caracteres | **4 de 4** |
| lo mismo | de tarea, 380 caracteres | **4 de 4** |
| "Un cliente que se llama O'Brien hace que la búsqueda falle" | de catálogo | **0 de 4** |
| lo mismo | de tarea, 380 caracteres | **0 de 4** |
| lo mismo | con el **síntoma** escrito en `when_to_use` | **8 de 8** |

Tres lecturas, y la primera desmonta media creencia del gremio.

**Cuando la petición nombra la tarea, la descripción da igual.** Una descripción
de catálogo de cuarenta y tres caracteres dispara igual de bien que una redactada
con mimo. Por eso todo el mundo cree que su descripción está bien: la prueba con
la que la valida es la petición que ya nombra la tarea.

**Cuando la petición cuenta un síntoma, ninguna de las dos dispara.** Cero de
ocho. Y esa es la petición de verdad: nadie escribe "audita el endpoint", la
gente escribe "esto se cae con este cliente".

**Lo que cierra el hueco no es una descripción mejor, es una descripción de otra
cosa.** Ocho de ocho en cuanto el `when_to_use` habla de apóstrofes, de búsquedas
que fallan y de clientes que tumban la aplicación. La frase del libro, entonces,
no es "la descripción es el disparador". Es más incómoda y más útil:

> **La descripción se escribe con las palabras del que pide, no con las del que
> cataloga.** Si tu descripción describe lo que la skill hace, describe la mitad
> equivocada.

### 7.2.3 · Cómo se escribe, y el tope que nadie ve

Con lo medido, la receta de la descripción tiene tres partes: qué hace, en una
frase; **cuándo**, con síntomas y frases reales, en `when_to_use`; y las palabras
que la gente usa de verdad, sacadas de tu propio historial de incidencias, no
inventadas.

Y hay un tope. `description` y `when_to_use` **se cortan juntas a 1.536
caracteres** en el catálogo. Medido con dos descripciones cuyos primeros 1.536
caracteres son idénticos:  ‹v2.1.245›

| Longitud de la descripción | Tokens de entrada |
|---:|---:|
| 1.200 caracteres | 46.252 |
| 1.536 caracteres | 46.386 |
| 3.072 caracteres, los 1.536 primeros idénticos | **46.387** |

Duplicar la descripción cuesta **un token**. No porque comprima bien: porque la
segunda mitad no llega. Si tu skill no se dispara y su descripción pasa de mil
quinientos caracteres, es probable que el criterio que te importa esté escrito
en la parte que el modelo no ve.

La otra cara: los 1.536 caracteres que sí se leen cuestan **634 tokens en cada
turno**, casi la mitad de lo que cuesta un `CLAUDE.md` entero. Diez skills así
son un `CLAUDE.md` de más, todos los días.

### 7.2.4 · Los comandos ya no existen, y eso simplifica el módulo

Esto es nuevo y cambia el consejo clásico: **los comandos personalizados se han
fusionado con las skills.** Un archivo en `.claude/commands/deploy.md` y una
skill en `.claude/skills/deploy/SKILL.md` crean el mismo `/deploy` y funcionan
igual. Los archivos antiguos siguen valiendo, y si coinciden en nombre, **gana
la skill**.

Comprobado: un `.claude/commands/ping-lab.md` de cinco líneas responde a
`/ping-lab` en la 2.1.245, y cuesta 41 tokens por turno, que es lo que ocupa su
descripción.

Así que la pregunta "¿esto es un comando o una skill?" ya no existe. La que
queda es **quién la invoca**, y son dos casillas independientes:

| | El modelo la invoca solo | Solo tú, con `/nombre` |
|---|---|---|
| **Aparece en el menú `/`** | Lo normal | `disable-model-invocation: true` |
| **No aparece** | `user-invocable: false` | no tiene sentido |

Medido también: con `disable-model-invocation: true`, la misma petición que
disparaba ocho de ocho pasa a **cero de tres**, y la skill sigue funcionando
invocada por su nombre. La bandera hace exactamente lo que dice.  ‹v2.1.245›

Lo demás del frontmatter que se usa de verdad: `allowed-tools`, que preaprueba
herramientas **solo durante el turno que la invoca**; `paths`, que limita la
skill a los archivos que casen; `context: fork`, que la ejecuta en un subagente
aparte, y ahí enlaza con el módulo 08.

### 7.2.5 · Que se cargue no significa que se cumpla

Y el aviso que este libro tiene que dar, porque lo ha medido dos veces. El
cuerpo de la skill del laboratorio empieza pidiendo una cosa trivial: que la
respuesta abra con una línea concreta. En las **ocho** ejecuciones con disparo
automático, esa línea apareció **tres veces**.

La skill se cargó las ocho. Lo que falla no es el disparo, es la obediencia.

Es la misma medición del módulo 05 con otra ropa: una instrucción, por bien
colocada que esté, compite con todo lo demás del contexto. **Una skill es
contexto de calidad, no un candado.** Lo que no sea negociable no va en una
skill: va en un hook, que se ejecuta.

---

## 7.3 · Receta

### 7.3.1 · Individual: la skill mínima que sirve

```text
.claude/skills/auditar-endpoint/
└── SKILL.md
```

Cuatro decisiones y ya está escrita:

1. **El nombre de la carpeta es el comando.** `auditar-endpoint` da
   `/auditar-endpoint`.
2. **`description`, una frase de qué hace.** Corta: se paga por turno.
3. **`when_to_use`, los síntomas.** Frases reales de tus incidencias. Es la
   parte que decide el disparo y es la que casi nadie escribe.
4. **El cuerpo, todo lo largo que haga falta**, con el procedimiento numerado.
   No cuesta nada hasta que se usa.

Comprueba las dos mitades por separado, porque fallan por separado: que se
dispare sin nombrarla, y que hecha a mano con `/nombre` haga lo que quieres.

### 7.3.2 · Equipo: dónde vive y quién gana

| Dónde | Ruta | Para quién |
|---|---|---|
| Organización | Configuración gestionada | Todos, y gana a todo |
| Personal | `~/.claude/skills/<nombre>/SKILL.md` | Todos tus proyectos |
| Proyecto | `.claude/skills/<nombre>/SKILL.md` | Ese repositorio, **y va a git** |
| Plugin | `<plugin>/skills/<nombre>/SKILL.md` | Donde el plugin esté activo |

La precedencia tiene una trampa que muerde en equipos: **la personal gana a la
del proyecto**. Si alguien tiene una `deploy` suya en `~/.claude/skills/`, la del
repositorio no se ejecuta para él, y nadie se entera. Las de plugin no compiten,
porque viven en su propio espacio de nombres, `/plugin:skill`.

Dos comportamientos más que ahorran una tarde. Las skills del proyecto se cargan
**también desde los directorios padre** hasta la raíz del repositorio, así que
arrancar en un subdirectorio no las pierde. Y los cambios en un `SKILL.md` se
recogen **en la misma sesión**, sin reiniciar; crear el directorio de skills
cuando la sesión ya está abierta, no.

### 7.3.3 · Empaquetar para el equipo: el plugin

Cuando lo que repartes deja de ser una skill y pasa a ser un kit (skills, más
subagentes, más hooks, más servidores MCP), la unidad es el plugin. La plantilla
está en `entregables/plantillas/plugin/`, y el error que comete todo el mundo la
primera vez es este:

**Dentro de `.claude-plugin/` va solo `plugin.json`.** Las carpetas `skills/`,
`agents/` y `hooks/` van en la raíz del plugin, no ahí dentro. Y dentro de un
plugin las rutas se resuelven contra `${CLAUDE_PLUGIN_ROOT}`, no contra
`${CLAUDE_PROJECT_DIR}`.

Se prueba antes de publicar sin instalar nada:

```bash
claude --plugin-dir ./plugin
```

Y se publica por un catálogo (`marketplace.json`) apuntando a un **commit
exacto**, no a una rama: un kit que cambia bajo los pies del equipo es peor que
no tener kit.

### 7.3.4 · Los cuatro comandos de equipo

En `entregables/plantillas/skills/`, los cuatro con
`disable-model-invocation: true` porque son procedimientos con momento, no
conocimiento que convenga aplicar solo:

| Comando | Cuándo | Qué garantiza |
|---|---|---|
| `/revisar-cambio` | Antes de pedir revisión humana | Que el diff pasa la lista del equipo |
| `/preparar-release` | Antes de publicar | La secuencia completa, en orden |
| `/postmortem` | Después de un incidente | Las seis secciones, huecos incluidos |
| `/poner-al-dia` | Al volver de vacaciones | Qué cambió y qué rompe |

El criterio para decidir si algo lleva la bandera: **¿tiene momento?** Auditar un
endpoint no lo tiene, se hace cuando aparece el problema, así que se dispara
sola. Preparar una release lo tiene, y una skill que decida por su cuenta que ha
llegado el momento de publicar es un problema, no una ayuda.

---

## 7.4 · Laboratorio · La skill que se dispara sola

**Paso 1. Escribe la skill con una descripción de catálogo.** En
`.claude/skills/auditar-endpoint/SKILL.md`, la que escribiría cualquiera:

```yaml
---
name: auditar-endpoint
description: Auditoría de seguridad de endpoints HTTP.
allowed-tools: Read Grep Glob
---
```

Y en el cuerpo, el procedimiento de auditar una ruta de `gestor-pedidos`: los
siete puntos, citar archivo y función, ordenar por gravedad, no arreglar nada.
Empieza el cuerpo pidiendo que la respuesta abra con una línea marcada; luego se
usa.

**Paso 2. Pruébala como la probaría cualquiera.**

```bash
claude -p "Echale un vistazo al endpoint /buscar de app.py y dime si te preocupa algo." \
  --allowedTools "Read,Grep,Glob"
```

Se dispara. Las cuatro veces. Con esos cuarenta y tres caracteres de
descripción. **Aquí es donde se para casi todo el mundo y da la skill por
buena.**

**Paso 3. Pruébala como llega el trabajo de verdad.** Misma skill, sin tocar
nada, otra forma de pedir lo mismo:

```bash
claude -p "Un cliente que se llama O'Brien hace que la busqueda de la app falle. Dime que esta pasando." \
  --allowedTools "Read,Grep,Glob"
```

**Cero de cuatro.** Contesta bien, encuentra la concatenación de SQL, y no usa
tu skill: no aplica los siete puntos ni ordena por gravedad. Cambia ahora la
descripción por una de tarea, larga y bien escrita, y repite: **cero de cuatro
otra vez**. Ese es el experimento que hay que hacer con los ojos abiertos.

**Paso 4. Cambia lo que hay que cambiar.** Añade `when_to_use` con los
**síntomas**, no con la tarea:

```yaml
when_to_use: >
  Úsala cuando pidan revisar o auditar un endpoint, y también cuando cuenten un
  SÍNTOMA sin nombrar la tarea: que la búsqueda falla, que un nombre con
  apóstrofe rompe algo, que un cliente concreto tumba la app, que un pedido
  devuelve datos raros o que algo de app.py se cae.
```

Repite el paso 3. **Ocho de ocho.** No has tocado el cuerpo ni la petición: has
escrito el disparo con las palabras del que pide.

**Paso 5. Mide lo que cuesta tenerla.** La petición trivial de siempre
(`Responde solo con la palabra OK.`), con la skill y sin ella: 45.752 frente a
45.960. **208 tokens por turno.** Ahora añádele veinte mil caracteres al cuerpo
y repite: **45.960, el mismo número exacto.** El cuerpo no está en contexto
hasta que se invoca.

**Paso 6. Encuentra el tope tú mismo.** Infla la descripción a 1.536 caracteres,
mide, duplícala a 3.072 dejando idénticos los primeros 1.536, y vuelve a medir.
46.386 y 46.387. **Un token.** La segunda mitad no existe.

**Paso 7. Comprueba el límite de lo que una skill puede prometer.** Cuenta, de
las ocho ejecuciones del paso 4, en cuántas la respuesta empieza por la línea
marcada que pide el cuerpo. A nosotros nos salieron **tres**. La skill se cargó
ocho veces. Si necesitas las ocho, eso es un hook, y está en el módulo 05.

**Paso 8. Escribe el porqué.** `SKILLS.md`, al lado de `HOOKS.md` y
`PERMISOS.md`: qué mira la skill, qué cuesta y qué no garantiza. El del
laboratorio está en `D6-repo-feo/gestor-pedidos/SKILLS.md`.

---

## 7.5 · Prueba

**PASA** si se cumplen las cuatro:

1. La skill se dispara **sin nombrarla**, con una petición que cuenta un síntoma
   y no nombra la tarea, repetida al menos cuatro veces.
2. Sabes decir cuánto cuesta tu skill por turno, y por qué el cuerpo no cuenta.
3. Has visto con tus ojos que una descripción de más de 1.536 caracteres se
   corta.
4. `SKILLS.md` está en el control de versiones y dice **qué no garantiza** la
   skill.

**FALLA** si la única prueba que has hecho es la del paso 2, la que nombra la
tarea. Esa prueba pasa siempre, incluso con una descripción de catálogo, y es la
razón de que tanta gente tenga skills que cree buenas y no se disparan cuando
hacen falta.

> **Esto va a cambiar.** Las tasas de disparo son estadística de un modelo, no
> una propiedad del CLI: dependen de la versión, del modelo y de qué más haya
> instalado. Las nuestras son del 25 de agosto de 2026 con la 2.1.245, con **una
> sola skill instalada** en el repositorio. Con quince skills compitiendo, el
> reparto cambia y este experimento hay que rehacerlo. Lo que esperamos que
> aguante es la forma: la petición que nombra la tarea dispara casi siempre, y
> la que cuenta el síntoma solo dispara si el síntoma está escrito arriba.

---

## 7.6 · Coste de este módulo

| Concepto | Cantidad |
|---|---|
| Tokens de entrada del laboratorio | ~2.600.000 |
| Tokens de salida | ~19.000 |
| Coste medido por el CLI | 1,49 dólares |
| Coste en euros | por debajo de 1,60 € |
| Tiempo | 50 minutos |
| **Impuesto de contexto, por skill instalada** | **208 tokens por turno** |
| Descripción en el tope de 1.536 caracteres | 634 tokens por turno |
| Cuerpo de la skill, sin invocar | **0 tokens** |
| Archivo suelto en `.claude/commands/` | 41 tokens por turno |
| Mantenimiento continuo | reescribir `when_to_use` cuando cambie el vocabulario del equipo |

La tabla comparada con lo medido en los módulos anteriores, todo en la misma
máquina y con la misma petición, es el activo que hay que enseñarle a quien
decide:

| Pieza | Coste por turno |
|---|---:|
| Reglas de permisos, módulo 04 | 0 |
| Hooks declarados, módulo 05 | 0 |
| Una skill instalada, este módulo | 208 |
| Un servidor MCP de tres herramientas, módulo 06 | 218 |
| Una skill con la descripción en el tope | 634 |
| `CLAUDE.md` de 67 líneas, módulo 03 | 1.311 |

Una skill cuesta lo mismo que un servidor MCP entero y **seis veces menos que el
archivo de memoria**. Lo que convierte eso en un consejo: cuando dudes entre
meter un procedimiento en el `CLAUDE.md` o sacarlo a una skill, la skill es más
barata, se dispara sola cuando toca, y no ocupa contexto el resto del tiempo.
Pero solo si su descripción está escrita para disparar.

El mantenimiento de verdad tampoco es el archivo. Es que **el vocabulario del
equipo cambia**: el día que alguien empiece a decir "peticiones fantasma" en vez
de "la búsqueda falla", tu `when_to_use` deja de casar y la skill se apaga sin
avisar. Revísalo cuando revises el inventario de incidencias, no antes.

---

## Runbook · Módulo 07

> **"Mi skill no se dispara sola"**
>
> 1. **Prueba con la petición de verdad**, la que cuenta el síntoma. La que
>    nombra la tarea dispara hasta con una descripción de catálogo: no prueba nada.
> 2. ¿Tiene `when_to_use` con **síntomas y frases reales**? Es lo único que movió
>    la aguja en la medición: 0 de 8 sin él, 8 de 8 con él.
> 3. ¿La descripción pasa de **1.536 caracteres**? Lo que sobra no existe.
> 4. ¿Lleva `disable-model-invocation: true`? Entonces no se dispara nunca sola,
>    por diseño.
> 5. ¿Hay otra skill con el mismo nombre en `~/.claude/skills/`? **La personal
>    gana a la del proyecto.**
> 6. ¿La creaste con la sesión abierta? El `SKILL.md` se recoge en caliente; un
>    directorio de skills nuevo, no.
>
> **"Se dispara y no hace lo que pone"**
> Normal, y medido: 3 de 8 en el cuerpo de una instrucción trivial. Una skill es
> contexto, no un candado. Lo que no sea negociable, hook (módulo 05).
>
> **Dónde vive y quién gana**
> Organización → personal → proyecto. Las de plugin no compiten: `/plugin:skill`.
> Cuidado con la personal de alguien que tapa la del repositorio.
>
> **Comandos y skills son lo mismo**
> `.claude/commands/x.md` y `.claude/skills/x/SKILL.md` dan los dos `/x`. Si
> coinciden, gana la skill. La pregunta ya no es cuál usar, sino **quién la
> invoca**: `disable-model-invocation` y `user-invocable`.
>
> **Lo que cuesta**
> Skill instalada: 208 tokens por turno. Cuerpo sin invocar: cero, aunque tenga
> veinte mil caracteres. Descripción en el tope: 634. Escribe **corto arriba y
> largo abajo**.
>
> **Plugin**
> Dentro de `.claude-plugin/` solo `plugin.json`. Rutas con
> `${CLAUDE_PLUGIN_ROOT}`. Probar con `claude --plugin-dir ./plugin`. Publicar
> apuntando a un commit exacto, nunca a una rama.
