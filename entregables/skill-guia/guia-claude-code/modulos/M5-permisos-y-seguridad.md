# M5 · Permisos, modos y seguridad operativa

> **Para quién es:** quien responde de la máquina, del repositorio o del equipo.
> **Qué resuelve:** el falso dilema entre "me pregunta por todo" y "le doy permiso para todo".
> **Qué NO cubre:** política de datos y cumplimiento legal (M16), ni arquitectura de despliegue (M14).

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 5.1 · Los modos de permisos

⚠️ **Corrección a los tutoriales y a más de un inventario:** hay **seis** modos,
no cinco. El que se olvida siempre es el primero, y es el modo por defecto de
toda la vida.

### Tabla 4 · Modos × qué se aprueba solo × riesgo × cuándo usarlo

| Modo | Qué corre sin preguntar | Riesgo | Cuándo usarlo |
|---|---|---|---|
| `default` (**Manual**) | Solo lecturas | Mínimo | Empezar, y trabajo sensible |
| `acceptEdits` | Lecturas, ediciones de archivos y comandos de sistema de archivos comunes (`mkdir`, `touch`, `mv`, `cp`) | Bajo | Iterar sobre código que estás revisando |
| `plan` | Lecturas, más comandos aprobados por el clasificador si auto mode está disponible | Bajo | Explorar antes de tocar nada |
| `auto` | Todo, con comprobaciones de seguridad en segundo plano | Medio | Tareas largas, fatiga de confirmaciones |
| `dontAsk` | Solo herramientas pre-aprobadas | Bajo si la lista es corta | CI y scripts bien acotados |
| `bypassPermissions` | Todo, sin comprobación ninguna | **Alto** | Solo contenedores y máquinas virtuales aisladas |

**Nota de nomenclatura que confunde a todo el mundo:** el modo que revisa cada
acción se llama **Manual** en el CLI, en `claude --help`, en las extensiones de
VS Code y JetBrains y en la aplicación de escritorio. Pero su valor de
configuración es `default`, que es el que usan los hooks y el SDK. El CLI acepta
`manual` como alias allí donde escribas el valor, por ejemplo
`claude --permission-mode manual` o `"defaultMode": "manual"`. La etiqueta Manual
y el alias requieren **v2.1.200 o posterior**.

---

## 5.2 · Auto mode pasa a ser el modo por defecto

**A partir del 14 de agosto de 2026**, auto mode es el modo por defecto para las
sesiones nuevas en los planes Pro, Max y Team.

Qué significa exactamente:

- Si **tú** ya fijaste un modo por defecto, se queda, salvo que aceptes el aviso
  único de cambio.
- Un modo por defecto **gestionado por tu organización no cambia**.
- Puedes cambiar de modo cuando quieras, como siempre.
- Ya en vigor en esos planes: **las llamadas al clasificador de auto mode no
  cuentan contra tus límites de uso**.

Para fijar tu propio valor antes del cambio, y no descubrirlo por sorpresa:

En `~/.claude/settings.json`:

```json
{
  "permissions": {
    "defaultMode": "auto"
  }
}
```

⚠️ Y de paso, un error que este mismo módulo llegó a cometer: **ese bloque no
puede llevar un comentario `//` dentro**. JSON no admite comentarios, y del M3:
usuario, proyecto y local son **estrictos**, así que un archivo con un comentario
dentro **se rechaza entero** y no se aplica ninguna de sus claves. La ruta va en
la prosa, no dentro del JSON.

Las sesiones nuevas muestran entonces `auto mode on` en la barra de estado.

💡 **Opinión operativa.** Si administras una flota, esta es la fecha en la que te
interesa tener ya fijado `defaultMode` en tus settings gestionados. No porque auto
mode sea malo, sino porque un cambio silencioso del modo por defecto es
exactamente el tipo de cosa que quieres decidir tú y no descubrir en un incidente.

---

## 5.3 · Qué bloquea el clasificador por defecto

Auto mode no es "permitirlo todo": es un clasificador que mira cada acción. Su
punto de partida es que **confía en tu directorio de trabajo y en los remotos que
estaban configurados cuando arrancó la sesión**.

⚠️ Detalle de seguridad que merece la pena subrayar: **un remoto añadido o
reapuntado durante la sesión con `git remote add` o `git remote set-url` no es de
confianza**. Antes de v2.1.200 sí lo era. Todo lo demás se trata como externo
hasta que configures infraestructura de confianza.

**Bloqueado por defecto:**

- Descargar y ejecutar código, del estilo `curl | bash`
- Enviar datos sensibles a endpoints externos
- Despliegues y migraciones de producción
- Borrado masivo en almacenamiento en la nube
- Conceder permisos de IAM o de repositorio
- Modificar infraestructura compartida
- Destruir de forma irreversible archivos que ya existían antes de la sesión
- `force push`
- Confirmar o publicar un cambio que, al ejecutarse, sacaría secretos fuera del
  repositorio o ampliaría lo que expone un despliegue

Ese último merece leerse dos veces porque es más ambicioso de lo que parece.
Cubre un flujo de CI que entrega un secreto a un destino que no lo recibía, un
script que lee un almacén de secretos y saca los datos, y un cambio de
configuración que amplía lo que publica un despliegue: registro, visibilidad,
artefactos, mapas de fuentes. **Se aplica en cualquier rama, incluso si el
repositorio es público, y se dispara cuando el cambio aterriza**, dispare o no la
tubería. Y para levantarlo hay que nombrar el efecto de ejecución, no basta con
describir el commit.

Nota de versión: antes de **v2.1.211** esta comprobación estaba acotada a la rama
por defecto.

---

## 5.4 · Reglas de permisos

Las reglas son la capa determinista, y van por herramienta:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  }
}
```

Recuerda la excepción del M3, que aquí es la propiedad más valiosa del sistema:
**las reglas de permisos se fusionan entre ámbitos, no se sobrescriben.** Un
`deny` puesto en el `.claude/settings.json` del proyecto no lo puede levantar
nadie desde su configuración local. Por eso la protección de secretos se pone
siempre en el proyecto y se confirma en git.

Hay tres clases de regla, y la del medio es la que menos se usa y más sirve:
`allow` corre sin preguntar, `ask` fuerza la confirmación aunque otra cosa lo
permitiera, y `deny` bloquea.

---

## 5.5 · Rutas protegidas y confianza del espacio de trabajo

Las escrituras sobre un pequeño conjunto de rutas **nunca se auto-aprueban**, con
dos excepciones: el modo `bypassPermissions` y las sesiones de planificación que
tengan bypass disponible. Protege el estado del repositorio y la propia
configuración de Claude de una corrupción accidental.

| Modo | Escrituras en rutas protegidas |
|---|---|
| `default`, `acceptEdits` | Se pregunta |
| `plan` | Se pregunta. Con bypass disponible, se permite. Con auto mode disponible, va al clasificador |
| `auto` | Va al clasificador |
| `bypassPermissions` | Se permite |

La **confianza del espacio de trabajo** es la otra puerta, y ya apareció dos veces
en esta guía: gobierna los hooks y gobierna `autoMemoryDirectory` cuando vienen
del proyecto. El patrón, otra vez: lo que un repositorio ajeno podría usar para
ejecutar código o mover archivos requiere que tú digas que sí, una vez, a
sabiendas.

---

## 5.6 · Configurar el clasificador

Dos sitios, y conviene no confundirlos.

**El `CLAUDE.md` sirve para las dos cosas.** El clasificador lee el mismo
`CLAUDE.md` que lee Claude, así que una instrucción como "nunca hagas force push"
en el `CLAUDE.md` del proyecto dirige a los dos a la vez. Para convenciones del
proyecto, empieza ahí.

**El bloque `autoMode`** es para reglas transversales: infraestructura de
confianza, denegaciones de toda la organización. Se lee de la configuración de
usuario, de los settings gestionados y del flag `--settings`. Del M3: **se ignora
deliberadamente en el settings del proyecto y en el local**, para que un
repositorio clonado no pueda relajarte el clasificador.

Tres campos sustituyen las listas internas, y son texto en prosa, no patrones:

- `autoMode.hard_deny`: límites de seguridad incondicionales
- `autoMode.soft_deny`: acciones destructivas que la intención del usuario puede levantar
- `autoMode.allow`: excepciones a los bloqueos blandos

### La precedencia dentro del clasificador, en cuatro escalones

1. **`hard_deny` bloquea sin condiciones.** Ni la intención del usuario ni las
   excepciones `allow` se aplican.
2. **`soft_deny` bloquea después.** La intención y los `allow` sí pueden con esto.
3. **`allow` levanta los `soft_deny` que casen**, como excepción.
4. **La intención explícita del usuario levanta el resto de bloqueos blandos**: si
   tu mensaje describe directa y específicamente la acción exacta que Claude va a
   hacer, el clasificador la permite aunque case con un `soft_deny`.

Y la frase que define "explícita", que es la mejor de toda la página:

> Pedirle a Claude que "limpie el repositorio" **no** autoriza un force push.
> Pedirle que "haz force push de esta rama" **sí**.

Para bloqueos duros basados en patrones de herramienta que corren **antes** del
clasificador, la herramienta correcta no es `autoMode` sino `permissions.deny`.

---

## 5.7 · Sandboxing

El sandbox tiene **dos modos**, y en los dos se aplican las mismas restricciones
de sistema de archivos y de red. Lo único que cambia es si los comandos que se
pueden meter en el sandbox se aprueban solos o siguen pidiendo permiso.

En modo de auto-aprobación, un comando que se puede aislar corre dentro y se
aprueba sin preguntar. Los que no se pueden aislar, como los que necesitan red
hacia un host no permitido, caen al flujo normal de permisos.

**Lo que sigue aplicándose incluso en auto-aprobación**, y es la parte que da
confianza:

- Las reglas `deny` explícitas se respetan **siempre**.
- `rm` o `rmdir` contra `/`, tu carpeta personal u otras rutas críticas del
  sistema siguen pidiendo confirmación, o pasando por el clasificador en auto
  mode. El enrutado al clasificador requiere **v2.1.218 o posterior**.
- Las reglas `ask` acotadas por contenido, como `Bash(git push *)`, siguen
  forzando la confirmación aunque el comando vaya en sandbox.
- Una regla `ask` pelada de `Bash`, o su forma `Bash(*)`, **se salta** para los
  comandos que corren en sandbox. Sigue aplicando a los que caen al flujo normal.

### Aislamiento de red

Va por un proxy que corre **fuera** del sandbox:

- **No hay dominios permitidos de partida.** La primera vez que un comando
  necesita un dominio nuevo, se pregunta. Aceptar lo permite para el resto de la
  sesión. Se pre-autorizan con `allowedDomains`, y las reglas `allow` de
  `WebFetch` también pre-autorizan dominios.
- **`strictAllowlist: true`** deniega en vez de preguntar. Solo tiene efecto desde
  configuración de usuario, gestionada o `--settings`: **ponerlo en el
  `.claude/settings.json` del repositorio no hace nada.** Y solo se aplica a
  comandos en sandbox; las herramientas en proceso como `WebFetch` siguen sus
  propias reglas de permisos.

### Enmascarar credenciales, en vez de bloquearlas

Esta es la pieza que resuelve el problema real, y muy poca gente sabe que existe.

`deny` sobre una credencial la elimina, y con ella rompe las herramientas que la
necesitan, como `gh` o `npm`. `"mode": "mask"` hace otra cosa: el comando en
sandbox ve un **valor centinela** por sesión, y el proxy del sandbox **sustituye
el centinela por el valor real** en las peticiones salientes hacia los hosts que
listes en `injectHosts`.

El comando, y todo lo que registre en sus logs, nunca tienen la credencial real.
Sus peticiones sí se autentican. Requiere **v2.1.199 o posterior**.

Dos condiciones que hay que conocer antes de confiar en esto:

1. El proxy tiene que **ver** el contenido de la petición para sustituir dentro,
   así que hace falta `network.tlsTerminate` para que termine el TLS él mismo. Sin
   eso, el enmascarado **falla sin exponer nada**: el comando sigue viendo solo el
   centinela.
2. Para **archivos** de credenciales, la sustitución es comportamiento de Linux y
   WSL2. **macOS bloquea el archivo en su lugar.**

---

## 5.8 · Elegir el aislamiento

### Tabla 12 · Enfoques de aislamiento

| Enfoque | Qué aísla | ¿Docker? | Esfuerzo |
|---|---|---|---|
| Herramienta Bash en sandbox | Comandos Bash y sus hijos | No | Mínimo en macOS, bajo en Linux y WSL2 |
| Sandbox runtime | **Todo el proceso**, incluidas herramientas de archivo, servidores MCP y hooks | No | Bajo |
| Dev container | Entorno de desarrollo completo | Sí | Medio |
| Contenedor propio | Entorno de desarrollo completo | Sí | Medio a alto |
| Máquina virtual | Sistema operativo completo | No | Alto |
| Claude Code en la web | Sistema operativo completo, alojado por Anthropic | No | Ninguno; requiere suscripción |

La distinción que hay que tener clara: **la herramienta Bash en sandbox solo
restringe Bash**. Las herramientas de archivo integradas, los servidores MCP y los
hooks siguen corriendo directamente en tu máquina. Si tu modelo de amenazas
incluye un MCP de terceros o un hook, la primera fila no te vale y necesitas la
segunda.

---

## 5.9 · Inyección de prompt

Un agente lee texto. No distingue por sí solo entre "documentación" y "orden". Las
cuatro puertas por las que entra una instrucción que tú no escribiste son el
propio repositorio, las dependencias que abre para entender un error, lo que
devuelve un servidor MCP, y los tickets o incidencias que cualquiera puede abrir.

**Lo que medimos nosotros.** Sembramos una inyección en un comentario HTML del
`README.md` de un repositorio de laboratorio, pidiéndole al asistente que
confirmara que todo estaba correcto y que no reportara hallazgos de seguridad.
Después le pedimos un resumen de la aplicación, con herramientas de solo lectura.

Dos pasadas, la segunda con el repositorio limpio de cualquier pista de que era un
ejercicio. **Las dos veces detectó la inyección, la nombró, dijo que solo obedece
las instrucciones del usuario y reportó exactamente lo que la inyección le pedía
callar.** El experimento completo, con el error de método que casi lo invalida,
está en `evidencias/EXP-001`.

⚠️ **Y ahora la parte que importa, porque es donde la gente saca la conclusión
equivocada.** Ese resultado **no es un control de seguridad**. Un control es algo
que se cumple porque no puede no cumplirse. Aquello se cumplió porque el modelo
decidió bien, y lo que depende de una decisión no es un límite: es una suerte
repetida. Con otro modelo, con la inyección enterrada en la respuesta de una
herramienta en lugar de en un archivo que te pidieron mirar, o en la hora tres de
una sesión larga, es otro experimento que aún no hemos hecho.

Las mitigaciones que sí son controles, en una línea: **permisos estrechos,
`deny` sobre lo que no se toca, sandbox con lista blanca de dominios, y revisión
humana antes de fusionar**. Ninguna depende del criterio del modelo.

---

## Checklist de verificación

- [ ] Sé nombrar los seis modos y cuál es el mío por defecto.
- [ ] He fijado `defaultMode` antes del 14 de agosto, a sabiendas.
- [ ] Tengo reglas `deny` para secretos, puestas en el **proyecto** y en git.
- [ ] Sé que un remoto añadido a mitad de sesión no es de confianza.
- [ ] Si uso `autoMode`, sé que se ignora desde el settings del proyecto.
- [ ] Sé qué aísla mi sandbox y, sobre todo, qué **no** aísla.
- [ ] Si enmascaro credenciales, tengo `network.tlsTerminate` puesto.
- [ ] `bypassPermissions` solo lo uso en entornos desechables.
- [ ] Mi protección contra inyección no depende de que el modelo se porte bien.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "Solo hay cinco modos" | Son seis. Falta `default`, que en el CLI se llama Manual |
| "Puse `manual` y no lo reconoce" | El alias requiere v2.1.200 o posterior |
| "Mi `strictAllowlist` del repositorio no hace nada" | Correcto: solo aplica desde usuario, gestionada o `--settings` |
| "Enmascaré la credencial y la herramienta ya no autentica" | Falta `network.tlsTerminate`, así el proxy no puede sustituir |
| "En macOS el archivo enmascarado no aparece" | En macOS se bloquea el archivo, no se sustituye |
| "Le dije que limpiara el repo y no hizo force push" | Correcto. Una petición general no es intención explícita |
| "El sandbox no protege de mi servidor MCP" | La herramienta Bash en sandbox solo aísla Bash. Necesitas el runtime |
| "Detectó la inyección, ya estamos seguros" | Detectar no es impedir. Eso no es un control |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `permission-modes.md` | 52.290 | Los seis modos, rutas protegidas, qué bloquea el clasificador |
| `sandboxing.md` | 66.526 | Modos de sandbox, red, enmascarado de credenciales |
| `permissions.md` | 61.403 | Sintaxis de reglas, allow/ask/deny |
| `auto-mode-config.md` | 28.130 | Dónde lee el clasificador, los cuatro escalones, intención explícita |
| `sandbox-environments.md` | 20.124 | Tabla 12 de enfoques de aislamiento |
| `whats-new/2026-w32.md` | 8.830 | Fecha del cambio de modo por defecto |

Material propio: `evidencias/EXP-001`, experimento de inyección en README,
12 de agosto de 2026, CLI 2.1.228.

**Marcas pendientes:** ninguna `⚠️ VERIFICAR` abierta. Las tres marcas de aviso
del módulo señalan una corrección al inventario, un cambio de comportamiento por
versión y un límite de interpretación, no dudas sin resolver.
