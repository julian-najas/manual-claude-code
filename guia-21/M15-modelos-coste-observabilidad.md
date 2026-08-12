# M15 · Modelos, coste y observabilidad

> **Para quién es:** quien paga la factura, y quien tiene que justificarla.
> **Qué resuelve:** que el gasto deje de sorprender, y saber qué palanca mover.
> **Qué NO cubre:** privacidad y retención de datos (M16).

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 15.1 · Qué modelo estás usando de verdad

`default` no es un modelo: es un valor especial que **limpia cualquier anulación**
y vuelve al recomendado para tu tipo de cuenta, o al modelo por defecto que haya
fijado tu organización.

Y ahí está la trampa: **"default" significa cosas distintas según quién pague**.

| Tipo de cuenta | `default` resuelve a |
|---|---|
| Max, Team Premium, Enterprise de pago por uso, API de Anthropic | **Opus 5** |
| Claude Platform on AWS, Amazon Bedrock, Agent Platform de Google | **Opus 5** |
| Pro, Team Standard, plazas de suscripción Enterprise | **Sonnet 5** |
| Microsoft Foundry | **Sonnet 4.5** |

⚠️ Antes de **v2.1.219**, `default` resolvía a Opus 4.8 en varias de esas filas.
Si comparas rendimiento o coste entre dos máquinas y una no está actualizada, no
estás comparando lo mismo.

**`opusplan`** es el híbrido automático: **Opus en modo plan** para el
razonamiento y la arquitectura, y **cambio automático a Sonnet en ejecución** para
generar el código. La fase de plan usa la misma ventana que el ajuste `opus`, así
que en los niveles donde Opus se sube automáticamente a 1M de contexto,
`opusplan` recibe la subida también en la fase de plan. Para forzar 1M en las dos
fases sin estar en un nivel con subida automática, `opusplan[1m]`.

---

## 15.2 · Tabla 11 · Modelos, alias y niveles de esfuerzo

Los **niveles de esfuerzo** controlan el razonamiento adaptativo: el modelo decide
si piensa y cuánto según la complejidad de cada paso.

| Familia de modelo | Niveles disponibles |
|---|---|
| Fable 5 | `low`, `medium`, `high`, `xhigh`, `max` |
| Opus 5, Sonnet 5, Opus 4.8, Opus 4.7 | `low`, `medium`, `high`, `xhigh`, `max` |
| Opus 4.6 y Sonnet 4.6 | `low`, `medium`, `high`, `max` |
| Los no listados | No admiten esfuerzo |

Cuatro reglas de comportamiento que evitan sorpresas:

1. **El esfuerzo por defecto es `high`** en todos los que lo admiten, **salvo Opus
   4.7, que va a `xhigh`**.
2. Si fijas un nivel que el modelo activo no admite, **baja al más alto admitido
   por debajo del que pediste**. `xhigh` corre como `high` en Opus 4.6.
3. Tu organización puede **limitar** qué niveles están disponibles.
4. Al estrenar Fable 5, Opus 4.8 u Opus 4.7, Claude Code **aplica el esfuerzo por
   defecto de ese modelo aunque tuvieras otro puesto**, y lo mantiene entre
   sesiones hasta que elijas explícitamente con `/effort` o `--effort`. **Opus 5
   no hace esa retención**: el nivel que tuvieras se arrastra.

### Fast mode no es lo mismo que bajar el esfuerzo

| Ajuste | Efecto |
|---|---|
| **Fast mode** | Misma calidad de modelo, **menos latencia, más coste** |
| **Menos esfuerzo** | Menos tiempo pensando, respuestas más rápidas, **posible pérdida de calidad** en tareas complejas |

Se pueden combinar para velocidad máxima en tareas sencillas. Pero la distinción
importa a fin de mes: **fast mode compra tiempo con dinero; bajar el esfuerzo
compra tiempo con calidad.** Confundirlas es cómo se acaba pagando más por
respuestas peores.

---

## 15.3 · Tabla 10 · Qué invalida la caché y qué no

Media factura se decide aquí, así que esta tabla es probablemente la más rentable
de toda la guía.

| **Invalida la caché** | **Mantiene la caché** |
|---|---|
| Cambiar de modelo | Editar archivos de tu repositorio |
| Cambiar el nivel de esfuerzo | Editar el `CLAUDE.md` en caliente |
| Activar fast mode | Cambiar el output style |
| Conectar o desconectar un servidor MCP | Cambiar el modo de permisos |
| Activar o desactivar un plugin | Invocar skills y comandos |
| **Denegar una herramienta entera** | Ejecutar `/recap` |
| Compactar la conversación | Rebobinar la conversación |
| Actualizar Claude Code | |

⚠️ **Corrección al Anexo A.** Tu inventario listaba siete invalidadores y se
dejaba **"denegar una herramienta entera"**. Merece explicación porque es sutil:
añadir un nombre de herramienta pelado como `Bash` o `WebFetch` en una regla
`deny` **la quita del contexto de Claude por completo**. Como las definiciones de
las herramientas integradas viven en la capa del system prompt, añadir o quitar
esa regla a mitad de sesión **invalida la caché**. Solo pasa con reglas que casan
en la posición del nombre de herramienta: el nombre pelado, la forma `Bash(*)`, o
un comodín de nombre de herramienta.

La columna derecha es la buena noticia y casi nadie la aprovecha: **editar tu
código no invalida nada**. Puedes trabajar todo el día tocando archivos sin
recalcular el prefijo. Lo que rompe la caché es tocar **la configuración**, no el
trabajo.

---

## 15.4 · Cuánto dura la caché

Los prefijos cacheados caducan por **inactividad**, y **cada petición que acierta
reinicia el reloj**, así que la caché se mantiene caliente mientras trabajas. Tras
un hueco suficiente, la siguiente petición recalcula la entrada entera, y por eso
**el primer turno al volver de un descanso es notablemente más lento**.

Hay dos tiempos de vida: **cinco minutos** y **una hora**. El de una hora aguanta
pausas largas pero **factura las escrituras de caché a una tarifa más alta**.

| Situación | TTL |
|---|---|
| Suscripción de Claude | **Una hora, solicitada automáticamente** |
| Clave de API o proveedor externo | Se elige según cómo autentiques, anulable por variables de entorno |
| **Subagentes, incluso con suscripción** | **Cinco minutos** |

Esa última fila es la que nadie espera: **el TTL automático de una hora aplica a
la conversación principal, no a los subagentes**. Un subagente arranca su propia
conversación, con su propio system prompt y sus propias herramientas, **empieza
sin ningún acierto de caché** y se va calentando en sus propios turnos.

**Y el contraste que hay que tener presente al elegir entre los dos:** un **fork**
hereda el system prompt, las herramientas y el historial del padre **exactamente**,
así que **su primera petición lee la caché del padre**. Un subagente empieza de
cero; un fork llega caliente. En trabajo repetido sobre el mismo contexto, esa
diferencia es dinero real.

Detalle de coste que conviene saber si te pasas del límite del plan: cuando Claude
Code tira de créditos de uso, se te factura ese uso, **y las escrituras de caché
cuestan más con el TTL de una hora que con el de cinco minutos**.

---

## 15.5 · Cómo se mira

Dos contadores que la API devuelve en cada respuesta cuentan toda la historia, y
la forma más directa de verlos en vivo es un script de barra de estado que lea el
objeto `current_usage`:

- **`cache_creation_input_tokens`**: lo que se escribió en la caché este turno, a
  tarifa de escritura.
- El contador de lectura de caché, que es el que debería ser enorme si todo va
  bien.

Más allá de eso: `/usage` y `/context` para la sesión, **telemetría OTLP** con
métricas, eventos y trazas para la organización, y **analytics** en Team y
Enterprise.

---

## 15.6 · Lo que medimos nosotros

Reproducible con `D4-factura/analizar_gasto.py`. **4.195 llamadas reales entre el
10 de abril y el 12 de agosto de 2026**, 111 sesiones de una operación multiagente
en producción.

| | Tokens |
|---|---:|
| Entrada | 60.635.400 |
| Salida | 2.579.138 |
| **Caché leída** | **594.025.760** |

**Por cada token que sale, entran 24.** Y la caché leída fue **casi diez veces
toda la entrada nueva del periodo**. Con la tabla 10 delante, ese número deja de
ser una curiosidad y pasa a ser el argumento: si tocar configuración a media
sesión te invalida esos 594 millones, la diferencia en la factura no es marginal.

**El coste de la cortesía.** Aislando las llamadas con respuesta de 50 tokens o
menos, un "vale", un "hecho", un "sigue":

| | |
|---|---:|
| Llamadas | 168 (4,0 % del total) |
| Tokens de entrada consumidos | 1.325.628 |
| Tokens de salida producidos | 5.700 |

**Cada confirmación de una palabra costó 7.891 tokens de entrada para devolver 34.**
Relación de 232 a 1.

**Y la trampa del modelo caro.** En los mismos datos, un modelo hizo **la mitad de
llamadas que otro y consumió el doble de tokens de entrada**: 34.157 por llamada
frente a 9.183. No era más caro por unidad. **Se le estaba dando cuatro veces más
contexto.**

> **La regla:** antes de cambiar de modelo para ahorrar, mide cuánto contexto le
> estás metiendo. Casi siempre el ahorro grande está en el contexto, no en la
> tarifa.

⚠️ **Lo que estos números no son.** No hay euros en las tablas: los tokens están
medidos uno a uno, pero los euros dependen de la tarifa de cada modelo en cada
fecha, y publicar una cifra sin la tabla de precios exacta sería fabricar un dato.
El script acepta `--precios` con tu propia tabla. Y los datos son de una operación
que corre sobre otros modelos: lo que transfiere es **la estructura** del gasto,
no las proporciones.

**Y un aviso de método que nos costó meses:** este proyecto tuvo una base de datos
de costes que todo el mundo daba por buena. Tenía **cero filas**. Los datos reales
estaban en unos JSONL que nadie miraba. **Cuenta las filas antes de citar tu
propio panel.**

---

## 15.7 · Recetas de reducción, por impacto real

En orden, de lo que más ahorra a lo que menos:

1. **Deja de tocar la configuración a mitad de sesión.** Modelo, esfuerzo, fast
   mode, MCP, plugins: cada cambio recalcula el prefijo entero. Decídelo al
   arrancar.
2. **Adelgaza lo que se paga en cada turno**, que es el `CLAUDE.md` (M4).
3. **Elimina los turnos que no producen artefactos.** Instrucciones con criterio
   de aceptación y permisos decididos de antemano, para no gastar tres turnos en
   aclarar lo que cabía en el primero.
4. **Manda el ruido a un subagente** (M9), que no computa en tu ventana.
5. **Ajusta el esfuerzo a la tarea**, sabiendo que baja calidad y no solo coste.
6. **Fast mode solo cuando la latencia valga dinero**, porque sube el coste.

---

## Checklist de verificación

- [ ] Sé a qué modelo resuelve `default` en **mi** tipo de cuenta.
- [ ] Sé qué nivel de esfuerzo estoy usando y si es el que quiero.
- [ ] No cambio modelo ni esfuerzo a mitad de sesión sin motivo.
- [ ] Sé que editar mi código **no** invalida la caché.
- [ ] Sé que mis subagentes usan TTL de cinco minutos aunque tenga suscripción.
- [ ] He mirado `/usage` y `/context` en una sesión real.
- [ ] Mi panel de costes tiene filas de verdad.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "A mi compañero le sale otro modelo con `default`" | Depende del tipo de cuenta, y cambió en v2.1.219 |
| "Puse `xhigh` y corre como `high`" | El modelo no admite ese nivel. Baja al más alto admitido |
| "Estrené modelo y se me cambió el esfuerzo" | Fable 5, Opus 4.8 y 4.7 imponen su defecto hasta que elijas |
| "Activé fast mode para ahorrar" | Fast mode **sube** el coste. Lo que baja coste es menos esfuerzo |
| "La caché no me aprovecha nada" | Repasa la columna izquierda de la tabla 10 |
| "El primer turno tras el café va lentísimo" | Caducó la caché por inactividad. Es lo esperado |
| "Mis subagentes no aprovechan la caché" | Empiezan de cero y usan TTL de 5 minutos. Un fork sí hereda |
| "Cambié de modelo para ahorrar y gasto igual" | El coste lo decide el contexto, no la tarifa |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `prompt-caching.md` | 30.389 | Tabla 10, TTL, subagentes y forks frente a la caché |
| `model-config.md` | 93.827 | `default`, `opusplan`, alias, niveles de esfuerzo |
| `fast-mode.md` | 18.169 | Fast mode frente a nivel de esfuerzo |
| `costs.md` | 33.541 | Coste y facturación |
| `monitoring-usage.md` | 134.020 | `/usage`, `/context`, telemetría OTLP |
| `analytics.md` | 12.545 | Analítica de Team y Enterprise |
| `advisor.md` | 15.753 | Advisor |
| `statusline.md` | 64.067 | `current_usage` para ver la caché en vivo |

Material propio: telemetría de 4.195 llamadas, 10-abr a 12-ago 2026, analizada
con `D4-factura/analizar_gasto.py`.

**Marcas pendientes:** ninguna. La marca del 15.3 corrige el Anexo A del
megaprompt, que listaba siete invalidadores de caché en vez de ocho.
