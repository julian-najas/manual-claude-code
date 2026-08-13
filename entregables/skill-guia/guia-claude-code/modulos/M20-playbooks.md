# M20 · Playbooks

> **Para quién es:** quien quiere copiar una solución entera en vez de montarla desde cero.
> **Qué resuelve:** el "vale, ¿y todo junto cómo queda?".
> **Qué NO cubre:** teoría. Cada decisión aquí remite al módulo que la sostiene.

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

⚠️ **Este módulo es el único de la guía sin páginas de documentación propias.**
Está **construido** a partir de los dieciocho módulos anteriores. Las afirmaciones
técnicas remiten al módulo donde están verificadas; las decisiones de montaje son
**criterio operativo**, y van marcadas como tales.

---

## 20.1 · Monorepo grande

### La situación

Cuarenta paquetes, cuatro equipos, un repositorio. Cada equipo tiene sus
convenciones y ninguno quiere las del vecino en su contexto. Las sesiones se
ahogan antes de comer.

### El montaje

**Uno.** Decide **desde dónde se arranca**, porque el `.claude/settings.json` del
proyecto se carga **desde el directorio de arranque** (M6). Si tu gente arranca
desde cada paquete, hace falta un `.claude/` en cada paquete, no solo en la raíz.

**Dos.** Reparte las instrucciones por capas (M4 y M6):

| Qué | Dónde | Por qué |
|---|---|---|
| Lo que vale para todo el repo | `CLAUDE.md` de la raíz | Se paga en cada turno, así que va corto |
| Convenciones de un paquete | `CLAUDE.md` de ese directorio | Lo mantiene su dueño, versionado con su código |
| Reglas transversales por tipo de archivo | `.claude/rules/*.md` con `paths` | Solo cargan al tocar archivos que casan |

**Tres.** Excluye lo ajeno con `claudeMdExcludes` (M4), para que el `CLAUDE.md` de
otro equipo no se cuele.

**Cuatro.** Recorta lo que se lee:

```json
{
  "permissions": {
    "deny": ["Read(./vendor/**)", "Read(./**/generated/**)"]
  },
  "worktree": {
    "sparsePaths": ["packages/mi-app", "shared/utils"],
    "symlinkDirectories": ["node_modules", ".cache"]
  }
}
```

Las búsquedas ya respetan `.gitignore` (M6), así que `node_modules/` y `dist/`
están fuera sin configurar nada. El `deny` es para **lo que sí está confirmado en
git**: un SDK copiado, código generado que se versiona.

### Cómo se sabe que funciona

- El reparto de `/context` al arrancar en un paquete **no incluye** los `CLAUDE.md`
  de los otros tres equipos.
- Una sesión de trabajo normal llega a la tarde **sin compactar**.
- Crear un worktree tarda segundos, no minutos, gracias a `symlinkDirectories`.

### Riesgos

- **El `CLAUDE.md` de la raíz engorda.** Es el pozo donde todo el mundo tira lo
  suyo. Requiere poda con calendario, no buena voluntad.
- **Las reglas con `paths` no se reinyectan tras compactar** (M4). En sesiones
  largas vuelven solo al tocar un archivo que case.

---

## 20.2 · Legacy sin tests

### La situación

Es el caso de `gestor-pedidos` del manual: código de hace años, sin tests,
documentación que miente, dos configuraciones que se contradicen y alguien que ya
no trabaja aquí.

### El montaje

> **Antes de empezar, tres cosas que este playbook no decía y que se descubrieron
> ejecutándolo** (`evidencias/EXP-003`):
>
> - **Instala las dependencias del proyecto primero.** Si faltan, el agente puede
>   construirse un sustituto para que la suite corra, y entonces tus tests verdes
>   no han tocado el framework real. Aquí: `pip install -r requirements.txt pytest`.
> - **Decide los permisos.** En interactivo apruebas a mano. Para el paso 1 va bien
>   `--permission-mode acceptEdits`; para los pasos de solo análisis, `plan` con
>   `--allowedTools "Read,Glob,Grep"`.
> - **Presupuesto:** unos 8 minutos y unos céntimos por paso. El recorrido entero
>   ronda la media hora de reloj.

**Uno, y va primero por un motivo medido:** sin algo que devuelva pasa o falla,
**tú eres el bucle de verificación** (M6). En un repositorio sin tests, cada tarea
te obliga a revisar a mano. Así que el primer encargo al agente **no es tocar el
código, es construir la red**:

```
Escribe tests de caracterización para el comportamiento actual de
procesar_pedido(), sin cambiar nada del código. Quiero que capturen lo que hace
hoy, incluidos los casos que parezcan bugs. Criterio: los tests pasan contra el
código tal cual está.
```

Tests de caracterización, no tests correctos: **congelan el comportamiento
actual** para poder cambiarlo sin miedo después.

⚠️ **Y la trampa que hay que decir en voz alta:** ese prompt acota a **una
función**, así que la red que construye es **parcial**. En la prueba real produjo
46 tests que dejaban las otras tres rutas sin cubrir, **dos de ellas con inyección
SQL**. "Los tests pasan" puede ser cierto con la aplicación abierta de par en par.
Anota qué queda fuera y ponlo en la lista, o repite el encargo por cada superficie
de entrada.

**Dos.** Escribe el `CLAUDE.md` que resuelve los empates (M4). Un repositorio
legacy tiene siempre tres o cuatro contradicciones a la vista; el agente las va a
encontrar y **no puede saber cuál gana**:

```markdown
# gestor-pedidos

## Qué manda
- **Ni `config.py` ni `settings.py` se usan**: `app.py` fija sus valores a mano.
  Los dos están muertos. Migrar es una decisión pendiente, no un hecho.
- El README está desactualizado desde 2021. Ante duda, gana el código.
- `/pedido_old` sigue publicado como ruta. Está pendiente de borrar: no lo mejores,
  y si lo tocas, es para borrarlo.

## Cómo se prueba
- `pytest -q`. Todo cambio necesita test.
```

⚠️ **La primera versión de esta plantilla decía "la configuración efectiva es
`settings.py`", y era falso**: nadie lo importa. Lo detectó el propio agente al
ejecutar la prueba de realidad, y **corrigió el `CLAUDE.md`**. Se deja escrito
porque es el error más instructivo de este playbook: un `CLAUDE.md` que afirma
algo que el código desmiente es exactamente el README mentiroso del módulo 1, solo
que escrito por ti. **Comprueba tus "qué manda" contra el código antes de
escribirlos.**

**Tres.** Pon los límites antes de dar permisos amplios (M5):

```json
{
  "permissions": {
    "deny": ["Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)"]
  }
}
```

**Cuatro.** Un subagente revisor (M9), porque **el autor no puede ser el revisor**:
comparte contexto y comparte sesgo.

### Cómo se sabe que funciona

- Los tests de caracterización pasan **antes** de tocar nada, **con las
  dependencias reales instaladas**, no contra un sustituto.
- El agente **respeta lo que el `CLAUDE.md` declara muerto**: no lo mejora ni
  propone migrar a ello, sin que se lo recuerdes. Proponer **borrarlo** sí es
  correcto, porque la propia plantilla lo declara pendiente de borrado.
- **Sabes qué queda fuera de la red.** Si los tests cubren una función, di cuáles
  son las demás superficies de entrada sin cubrir.
- El revisor encuentra fallos que el agente principal dio por buenos. **Comprobado
  en la prueba de realidad**: encontró que los 46 tests dejaban dos rutas con
  inyección SQL sin cubrir, que la suite fija el valor literal de la clave (así que
  rotarla deja la CI en rojo), y corrigió a la baja dos hallazgos previos.

### Riesgos

- **El impulso de refactorizar de paso.** Diffs de novecientas líneas que nadie
  revisa. Se acota en el plan (M6), no después.
- **Los tests de caracterización congelan bugs.** Es intencionado, pero hay que
  escribirlo en el `CLAUDE.md` para que nadie los tome por especificación.
- **Y congelan más de lo que crees.** En la prueba real, la suite acabó fijando por
  contrato el valor literal de una credencial hardcodeada: rotarla dejaba la CI en
  rojo. Revisa qué está afirmando tu red antes de fiarte de ella.

---

## 20.3 · Equipo de veinte con despliegue gobernado

### La situación

Veinte desarrolladores, un CTO que responde ante clientes y un departamento de
seguridad que quiere saber qué se aprueba.

### El montaje

**Uno. La conversación de arquitectura antes que la técnica** (M14). La pregunta
no es qué proveedor: es **qué funciones estáis dispuestos a perder**. Enseña esa
lista al equipo y que la decisión quede firmada.

**Dos. Una sola fuente de settings gestionados** (M3 y M14). Server-managed o
endpoint-managed, no las dos: **dentro del nivel gestionado no se fusionan**, y el
diagnóstico de esa mezcla es infernal.

**Tres. La configuración del repositorio, en git:**

```json
{
  "permissions": {
    "defaultMode": "auto",
    "deny": ["Read(./.env*)", "Read(./secrets/**)", "Bash(curl *)"],
    "ask":  ["Bash(git push *)"]
  },
  "hooks": {
    "PreToolUse": [{ "matcher": "Bash",
      "hooks": [{ "type": "command", "if": "Bash(rm -rf *)",
        "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/veto-rm.sh" }] }],
    "PostToolUse": [{ "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/format.sh" }] }]
  }
}
```

Recuerda del M3: **los permisos se fusionan entre ámbitos**, así que ese `deny` no
lo puede levantar nadie desde su configuración local. Y del M18: **las reglas
`allow` de proyecto requieren confianza del espacio de trabajo, pero `deny` y `ask`
se aplican siempre**.

**Cuatro. Revisión calibrada** (M13). Un `REVIEW.md` en la raíz que diga qué es
importante **aquí**, con las reglas escritas dentro porque **los imports con `@` no
se expanden**.

**Cinco. El folio de política** firmado (M16), y la conversación de datos resuelta
por escrito: proveedor, contrato, retención, y el chequeo de dominio de `WebFetch`
que sale igual uses el proveedor que uses.

**Seis. Empaqueta y reparte** (M11): lo que funciona pasa a plugin, con catálogo
propio en la lista blanca de los settings gestionados.

### Cómo se sabe que funciona

- Un desarrollador nuevo clona, acepta la confianza del espacio de trabajo y
  **tiene la misma configuración que el resto**, sin instrucciones por chat.
- `/status` en cualquier máquina dice la misma fuente gestionada.
- La revisión automática se lee, en vez de cerrarse sin mirar.
- Hay una cifra de gasto del mes pasado y alguien la mira.

### Riesgos

- **Ultrareview en cada push.** A 5-25 $ la pasada y **sin ejecuciones gratis en
  Team ni Enterprise** (M13), veinte personas construyen una factura sorprendente
  en una semana. Es para antes de fusionar cambios sustanciales.
- **Auto mode pasa a ser el modo por defecto el 14 de agosto de 2026** (M5). Si no
  fijáis vuestro `defaultMode` en los settings gestionados, os cambia solo.
- **Los MCP conectados son subencargados de facto** (M16) y **no los cubre ZDR**.

---

## 20.4 · Automatización nocturna desatendida en servidor propio

### La situación

Un servidor propio, sin nadie delante, que tiene que hacer trabajo acotado por la
noche y dejarlo revisable por la mañana. Es el caso de uso ancla de esta guía.

### El montaje

**Uno. Decide qué le pides**, y que cumpla las tres condiciones del cierre del
manual: criterio de éxito objetivo, trabajo tedioso y conocido, y coste de
equivocarse reversible. Si falta una, no es trabajo para desatender.

**Dos. Modo no interactivo con permisos explícitos** (M10 y M5). **Nunca**
`--dangerously-skip-permissions` en una máquina con acceso a producción:

```bash
claude -p "$(cat tarea-nocturna.md)" \
  --permission-mode dontAsk \
  --allowedTools "Read,Glob,Grep,Edit,Write,Bash(npm run test *),Bash(git *)" \
  --worktree \
  --settings .claude/settings.nocturno.json
```

`dontAsk` **solo permite herramientas pre-aprobadas** (M5): es el modo correcto
para scripts, porque lo que no listaste no corre en vez de esperar a un humano que
no está.

`--worktree` porque el trabajo desatendido va aislado (M9), con sus **cuatro
comprobaciones** que bloquean también lo que no se puede verificar.

**Tres. Que el `CLAUDE.md` diga cómo se hacen los commits**, porque las sesiones en
segundo plano **siguen esas instrucciones** al confirmar y publicar (M9). Deja de
ser cosmética y pasa a gobernar lo que hace sin ti.

**Cuatro. Puerta de calidad bloqueante** (M10), en `Stop`, que es donde puede
vetar:

```json
{ "hooks": { "Stop": [{ "hooks": [{ "type": "command",
  "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/puerta-calidad.sh",
  "timeout": 120 }] }] } }
```

**Cinco. Auditoría asíncrona**, que solo observa y por eso no frena (M10):

```json
{ "hooks": { "PostToolUse": [{ "matcher": "*",
  "hooks": [{ "type": "command", "async": true,
    "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/auditar.sh" }] }] } }
```

**Seis. Programación.** Del M10: si puedes **reaccionar a un evento**, channels; si
tienes **condición verificable**, `/goal`; si hay que **sondear**, `/loop` con
intervalo acorde. Para trabajo nocturno que debe correr con el portátil cerrado,
**routines** o **tareas programadas de escritorio**, según si hace falta acceso al
disco local (M12).

**Siete. Si vas por gateway propio**, que es lo habitual en servidor propio:
comprueba `GET /protocol` (M14) y **verifica si tienes tool search activo**,
porque con `ANTHROPIC_BASE_URL` apuntando fuera **se desactiva solo** y MCP vuelve
a ser peaje permanente (M8).

**Ocho. Mide.** Del M15: relación entrada/salida, porcentaje de respuestas cortas
y caché leída frente a entrada nueva. Y no cambies modelo ni esfuerzo a mitad de
ejecución, porque **invalida la caché**.

### Cómo se sabe que funciona

- Por la mañana hay **una propuesta de cambio revisable**, no una rama tocada a
  mano.
- La puerta de calidad ha vetado al menos una vez en el primer mes. Si nunca veta,
  o el trabajo es trivial o la puerta no comprueba nada.
- El registro de auditoría permite responder **qué tocó y por qué** tres semanas
  después.
- El coste por ejecución es estable entre noches.

### Riesgos

- **Lo desatendido amplifica los errores de acotación.** Una instrucción ambigua a
  las tres de la mañana produce trabajo ambiguo durante horas.
- **Las tareas de `/loop` son de ámbito de sesión y caducan a los siete días**
  (M10). Para algo que debe sobrevivir, routines o tareas de escritorio.
- **El rebobinado no cubre lo que hizo Bash ni un subagente en segundo plano**
  (M6). En desatendido, tu red es git, no `Esc` `Esc`.
- **Si tu gateway no reenvía `tool_reference`**, forzar `ENABLE_TOOL_SEARCH` no te
  da tool search: te da fallos.

---

## 20.5 · Un plugin interno, de cero a catálogo

### La situación

Tienes una skill, dos hooks y un subagente que usas a diario y que tu equipo
quiere. Ahora mismo viven sueltos en tu `.claude/`.

### El montaje

**Uno. No empaquetes todavía.** Empaquetar antes de que funcione reparte el
problema (M11). Que lleve semanas funcionando en tu máquina.

**Dos. Dale forma**, y aquí es donde se equivoca todo el mundo (M11): dentro de
`.claude-plugin/` **solo va `plugin.json`**; `skills/`, `agents/` y `hooks/` van en
la **raíz** del plugin. Y la raíz del plugin **nunca es `~/.claude/`**.

```text
mi-plugin/
├── .claude-plugin/plugin.json
├── skills/auditar-endpoint/SKILL.md
├── agents/revisor.md
└── hooks/hooks.json
```

**Tres. Pruébalo con `--plugin-dir`** antes de publicar nada.

**Cuatro. Catálogo aparte**, en su propio repositorio. Recuerda que la fuente del
catálogo admite `ref` pero **no `sha`**, mientras que la del plugin admite los dos
(M11): **el anclaje fino va en la entrada del plugin**.

**Cinco. Elige fuente.** `github` con `sha` para reproducibilidad estricta, o
`archive` con `sha256` si en las máquinas de tu gente **no hay git ni npm**
(v2.1.224+).

**Seis. Etiqueta la release** y declara restricciones si dependes de otro plugin,
para que una actualización ajena no te rompa (M11).

**Siete. Añade el catálogo a los settings gestionados** con lista blanca, y
opcionalmente un bloque `relevance` para que se sugiera solo a quien le sirve.

**Ocho. Verifica en una máquina que no sea la tuya.** Es el único sitio donde se
comprueba de verdad que está bien empaquetado.

### Cómo se sabe que funciona

- Un compañero instala desde el catálogo y **la skill se activa sola** en la tarea
  que debería activarla, sin que él la nombre.
- El hook obligatorio se aplica en su máquina igual que en la tuya.
- Una actualización del plugin no rompe a quien depende de él.

### Riesgos

- **Una skill de repositorio puede concederse a sí misma acceso amplio a
  herramientas** (M7). Si repartes plugins, tu revisión es la única barrera antes
  de que alguien acepte la confianza del espacio de trabajo.
- **La descripción es el disparador** (M7). Un plugin cuya skill nunca se activa
  sola es un plugin que nadie usa, y la causa suele ser el frontmatter, no el
  cuerpo.

---

## 20.6 · Lo que comparten los cinco

Si de los cinco playbooks hubiera que sacar un patrón, es este, y en este orden:

1. **Primero el criterio de verificación.** Sin algo que devuelva pasa o falla, lo
   demás es decoración.
2. **Después los límites**, que son `deny` y hooks, no instrucciones.
3. **Después el contexto**, podado y por capas.
4. **Después el reparto**, cuando ya funciona.
5. **Y siempre la medición**, porque lo que no se mide se convierte en factura.

---

## Checklist de verificación

- [ ] Mi playbook tiene un criterio de éxito objetivo antes que nada.
- [ ] Lo no negociable está en hooks y en `deny`, no en el `CLAUDE.md`.
- [ ] Lo desatendido corre en worktree y con permisos explícitos.
- [ ] Mi `CLAUDE.md` dice cómo se hacen los commits.
- [ ] Tengo una puerta de calidad que **ha vetado alguna vez**.
- [ ] Puedo responder qué tocó el agente hace tres semanas.
- [ ] Si voy por gateway, he comprobado `GET /protocol`.
- [ ] Lo he verificado en una máquina que no es la mía.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "En el monorepo se cuela el contexto de otros equipos" | Falta `claudeMdExcludes` y capas por directorio |
| "Cada tarea del legacy acaba en refactor gigante" | Falta acotar en el plan, y tests de caracterización |
| "El nuevo no tiene la misma configuración" | No está en git, o no ha aceptado la confianza |
| "La factura de revisión se disparó" | Ultrareview en cada push. Sin ejecuciones gratis en Team |
| "La puerta de calidad nunca veta" | O el trabajo es trivial, o no comprueba nada |
| "El trabajo nocturno tocó la rama principal" | Falta `--worktree` |
| "Mi plugin no le funciona a nadie más" | Estructura mal: solo `plugin.json` en `.claude-plugin/` |

---

## Fuentes de este módulo

**No hay páginas de documentación propias de este módulo.** Está construido sobre
los módulos M3 a M19 de esta misma guía, cada uno verificado contra su fuente en
su propia pasada.

Páginas de apoyo descargadas el 12 de agosto de 2026:

| Página | Bytes | Para qué |
|---|---:|---|
| `large-codebases.md` | 35.416 | Tácticas de monorepo del 20.1 |
| `communications-kit.md` | 25.743 | Materiales de despliegue en equipo del 20.3 |
| `champion-kit.md` | 22.058 | Adopción interna del 20.3 |

**Marcas pendientes:** ninguna sin resolver. Todo el contenido técnico remite a un
módulo verificado; las decisiones de montaje son criterio operativo y están
señaladas como tales en la cabecera.
