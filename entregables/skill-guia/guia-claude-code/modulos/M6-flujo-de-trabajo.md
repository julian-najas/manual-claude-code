# M6 · El flujo de trabajo diario que de verdad funciona

> **Para quién es:** [B], el que ya lo usa a diario y sospecha que lo está usando a medias.
> **Qué resuelve:** la diferencia entre una sesión que vigilas y una de la que te puedes ir.
> **Qué NO cubre:** automatizarlo sin ti delante (M10) ni integración continua (M13).

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 6.1 · Explorar, planificar, implementar, verificar

Dejar que Claude salte directo a escribir código produce código que resuelve **el
problema equivocado**. El flujo recomendado separa la investigación de la
ejecución, en cuatro fases:

1. **Explorar.** Entra en modo plan con `Shift+Tab` hasta que la barra muestre
   `⏸ plan mode on`, o arranca con `claude --permission-mode plan`. Claude lee
   archivos y contesta preguntas **sin cambiar nada**.
2. **Planificar.** Pídele un plan detallado de implementación. **`Ctrl+G` abre el
   plan en tu editor de texto** para que lo edites directamente antes de que
   proceda. Ese atajo lo conoce muy poca gente y es donde se corrige el 80 % de lo
   que luego habría que deshacer.
3. **Implementar.** Sales del modo plan aprobando el plan.
4. **Verificar.** Lo de la sección siguiente, que es lo que realmente separa a los
   equipos que sacan partido de esto de los que no.

---

## 6.2 · Dale algo contra lo que verificar

Si solo te llevas una idea del módulo, que sea esta. La documentación la formula
así, y es difícil decirlo mejor:

> **Claude para cuando el trabajo *parece* terminado.** Sin una comprobación que
> pueda ejecutar, "parece terminado" es la única señal disponible, **y tú te
> conviertes en el bucle de verificación**: cada error espera a que tú lo notes.

Dale algo que produzca un **pasa o falla** y el bucle se cierra solo: Claude hace
el trabajo, ejecuta la comprobación, lee el resultado e itera hasta que pasa.

Vale cualquier cosa que devuelva una señal legible en la conversación: una batería
de tests, el código de salida de una compilación, un linter, un script que compare
la salida contra un fichero de referencia, o una captura del navegador comparada
con un diseño.

La diferencia práctica en una petición:

| Sin criterio | Con criterio |
|---|---|
| "implementa una función que valide correos" | "escribe `validateEmail`. Casos de prueba: `user@example.com` válido, `user@` inválido, vacío inválido. Que pasen los tests" |

**Esta es también la razón por la que el capítulo escéptico de nuestro manual dice
que el balance sale a favor en trabajo con criterio de éxito objetivo.** No es una
opinión sobre modelos: es que sin criterio el bucle agéntico se queda en dos fases
de las tres.

💡 **Opinión operativa.** El corolario incómodo es que **un repositorio sin tests
no solo es peor de mantener: es más caro de agentificar**. Cada tarea necesita que
tú hagas de verificador. Si estás decidiendo dónde invertir primero, la respuesta
casi nunca es "mejor prompt" y casi siempre es "algo que devuelva pasa o falla".

---

## 6.3 · Ser específico por adelantado

Un turno de aclaración cuesta el contexto entero (M15: cada confirmación de una
palabra costó 7.891 tokens de entrada en nuestra medición). Así que la
especificidad no es cortesía, es presupuesto.

Lo que convierte una petición vaga en una útil:

- **El resultado esperado**, no la tarea. "Que los cuatro países calculen bien el
  IVA y lo cubran los tests" en vez de "arregla el IVA".
- **El contexto que solo tienes tú**: qué se intentó ya, qué no se puede tocar,
  quién depende de eso.
- **Contenido rico** cuando lo haya: una captura, un fragmento de log, el diff.
- **Los criterios de aceptación**, que además son el criterio de verificación de
  6.2.

---

## 6.4 · Corregir el rumbo pronto

Es una conversación, no un encargo. Interrumpir en cuanto ves que va por otro
lado cuesta un turno; dejarlo llegar al final cuesta la revisión entera y el
rehacer.

La forma barata de corregir el rumbo es **el plan**, no el código. Por eso `Ctrl+G`
del 6.1 rinde tanto: editar un plan de veinte líneas es gratis comparado con
revisar el resultado de haberlo seguido.

---

## 6.5 · Gestión agresiva del contexto

Lo que hay que tener a mano, con el detalle en el M4 y el M15:

- **Lo que debe persistir va al `CLAUDE.md`**, no al historial, porque la
  compactación se lleva las instrucciones dadas solo en conversación.
- **El ruido va a un subagente**, que no computa en tu ventana.
- **Lo que se paga en cada turno es el `CLAUDE.md`**, así que se poda.
- **`/context`** antes de teorizar sobre por qué se llena.

---

## 6.6 · Rewind y sus límites

`Esc` `Esc` rebobina. Antes de editar, Claude guarda una instantánea del
contenido. Pero **los checkpoints cubren mucho menos de lo que la gente cree**, y
esta lista es de las cosas más importantes de todo el módulo:

⚠️ **Cinco límites documentados:**

1. **Los cambios hechos por comandos de Bash no se registran.** Si Claude ejecuta
   `rm`, `mv` o `cp`, **eso no se puede deshacer rebobinando**. Solo se registran
   las ediciones hechas con las herramientas de edición de archivos.
2. **Las ediciones de un subagente no se restauran**, con una excepción precisa:
   una skill con `context: fork` **en primer plano** edita tu árbol de trabajo
   durante tu propio turno, así que sí se restaura. Cualquier otro subagente,
   incluida una skill bifurcada en segundo plano, que es el comportamiento por
   defecto, y una pasada de `/code-review --fix` en segundo plano: **no**. Para
   eso, git.
3. **Los cambios externos no se registran.** Solo lo editado dentro de la sesión
   actual.
4. **Los enlaces simbólicos y duros no se restauran.**
5. **No sustituye al control de versiones.** Es literal en la documentación.

Y del M1: **lo que toca sistemas remotos no se puede rebobinar de ninguna manera**.
Bases de datos, APIs, despliegues.

La lectura práctica: **el rebobinado es una red de seguridad para las ediciones de
archivo, no para la sesión.** Confundir las dos cosas es cómo se pierde trabajo
con cara de sorpresa.

---

## 6.7 · Repositorios grandes

Cuatro tácticas que aparecen en la guía de bases de código grandes y que aplican
en cuanto el proyecto pasa de mediano:

**Dónde arrancas importa.** El `.claude/settings.json` del proyecto **se carga
desde tu directorio de arranque**. Si arrancas desde la raíz, ponlo en la raíz; si
arrancas desde cada paquete, hace falta un `.claude/` en cada uno.

**Elige entre `CLAUDE.md` por directorio y reglas por ruta:**

| | Dónde vive | Cuándo carga | Cuándo usarlo |
|---|---|---|---|
| `CLAUDE.md` por directorio | Junto al código de ese directorio | Al arrancar desde ahí, o al leer un archivo de ahí | El dueño del directorio mantiene sus convenciones, versionadas con su código |
| Regla con `paths` | En `.claude/rules/` | Al leer un archivo que casa con el patrón | Convenciones transversales que cruzan directorios |

**Bloquea la lectura de código generado y de terceros.** Las búsquedas de
contenido **respetan `.gitignore` por defecto**, así que `node_modules/`, `dist/` y
`build/` ya quedan fuera sin configurar nada. Para lo que **sí está confirmado en
git**, como un SDK copiado o código generado que se versiona, hacen falta reglas
`Read` en `permissions.deny`.

**Recorta el árbol.** `worktree.sparsePaths` del M3 escribe en disco solo los
directorios que necesitas.

---

## 6.8 · Anti-patrones, y a qué huelen

| Anti-patrón | El olor | Qué hacer |
|---|---|---|
| Pedir código antes de explorar | El resultado es correcto y resuelve otra cosa | Modo plan primero |
| Pedir sin criterio de éxito | Tú revisando cada línea | Dale tests o un linter |
| Dejarlo llegar al final para corregir | Rehacer más que hacer | Interrumpe pronto, corrige el plan |
| Aprobar lo que no sabrías explicar | Silencio en la revisión de código | Si no lo entiendes, no entra |
| Confiar en `Esc` `Esc` para todo | "Pero si lo deshice" | Git. Los checkpoints tienen cinco límites |
| Meterlo todo en el `CLAUDE.md` | La sesión se ahoga a media tarde | Reglas con `paths`, y skills |
| "Ya que estamos, refactoriza esto" | Diffs de 900 líneas que nadie revisa | El código viejo que funciona es un activo |
| Repetir la instrucción cada turno | Cansancio y gasto | `CLAUDE.md`, o un hook `PostCompact` |

---

## Checklist de verificación

- [ ] Mi proyecto tiene algo que devuelve pasa o falla y Claude puede ejecutarlo.
- [ ] Uso modo plan antes de tareas no triviales.
- [ ] Sé que `Ctrl+G` abre el plan en mi editor.
- [ ] Mis peticiones llevan criterio de aceptación, no solo la tarea.
- [ ] Interrumpo pronto en vez de corregir al final.
- [ ] Sé que rebobinar **no** deshace lo que hizo un comando de Bash.
- [ ] Sé que rebobinar **no** deshace lo que hizo un subagente en segundo plano.
- [ ] En mi monorepo, arranco donde está el `.claude/` que quiero que se cargue.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "Hace algo razonable pero no lo que pedía" | Saltó a implementar sin explorar. Modo plan |
| "Tengo que revisarle todo" | No hay comprobación que pueda ejecutar. Eres tú el bucle |
| "Rebobiné y el archivo seguía borrado" | Lo borró un comando de Bash. Eso no se registra |
| "Rebobiné y los cambios del subagente siguen ahí" | Solo se restauran los de un fork en primer plano |
| "En el monorepo no coge mi configuración" | El settings de proyecto se carga desde el directorio de arranque |
| "Se le va el contexto en leer `dist/`" | Está en `.gitignore` y ya se excluye. Lo confirmado en git necesita `deny` |
| "Cada tarea acaba en un refactor gigante" | Falta acotar el encargo en el plan |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `best-practices.md` | 40.029 | Verificación, explorar antes de planificar, comunicación |
| `common-workflows.md` | 18.938 | Recetas por tarea |
| `prompt-library.md` | 56.262 | Peticiones de referencia |
| `checkpointing.md` | 7.858 | Los cinco límites del rebobinado |
| `large-codebases.md` | 35.416 | Monorepos, dónde arrancar, qué bloquear |
| `how-claude-code-works.md` | 20.582 | El bucle y sus fases |

**Marcas pendientes:** ninguna.
