# M4 · Memoria y contexto

> **Para quién es:** todos, desde el segundo día de uso.
> **Qué resuelve:** las instrucciones que se pierden, el `CLAUDE.md` que no para de crecer y el contexto que se agota.
> **Qué NO cubre:** skills (M7) ni subagentes (M9), aunque el módulo termina justo señalando cuándo mover algo allí.

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*
*⚠️ de la Fase 0 resuelto: `.claude/rules/` no tiene página propia, se documenta dentro de `memory.md`.*

---

## 4.1 · La ley que gobierna todo el módulo

Hay dos sistemas de memoria y los dos se cargan al empezar cada conversación:

| | `CLAUDE.md` | Auto memory |
|---|---|---|
| Quién lo escribe | Tú | Claude |
| Qué contiene | Instrucciones y reglas | Aprendizajes y patrones |
| Ámbito | Proyecto, usuario u organización | Por repositorio, compartido entre worktrees |

Y antes de nada, la frase que hay que tatuarse, porque está en la documentación
oficial y contradice lo que casi todo el mundo cree:

> **Claude trata ambos como contexto, no como configuración impuesta.**

Es decir: `CLAUDE.md` **no es un archivo de reglas que se cumplen**. Es un texto
que se lee. Para bloquear una acción pase lo que pase, hace falta un hook
`PreToolUse`, que es código y no interpretación. Esta es la pregunta 01 del árbol
de decisión y aquí está su fundamento documentado.

Corolario práctico: **cuanto más específica y concisa sea la instrucción, más
consistentemente se sigue**. "Usa indentación de 2 espacios" funciona; "formatea
bien el código" no. Y si dos reglas se contradicen, Claude puede elegir una
arbitrariamente, así que revisar y podar es trabajo de mantenimiento, no de
perfeccionismo.

---

## 4.2 · Cómo se cargan de verdad los `CLAUDE.md`

Claude Code **sube por el árbol de directorios** desde tu directorio de trabajo,
mirando en cada nivel si hay `CLAUDE.md` y `CLAUDE.local.md`. Si lanzas en
`foo/bar/`, carga `foo/bar/CLAUDE.md`, `foo/CLAUDE.md` y los `CLAUDE.local.md` que
haya al lado.

Tres reglas de orden que casi nadie conoce y que explican comportamientos raros:

1. **Todo se concatena, nada se sobrescribe.** No hay un `CLAUDE.md` que gane.
2. **El orden va de la raíz hacia tu directorio**, así que lo más cercano se lee
   **el último**. En el ejemplo, `foo/CLAUDE.md` aparece antes que
   `foo/bar/CLAUDE.md`.
3. **Dentro de cada directorio, `CLAUDE.local.md` va después de `CLAUDE.md`**, así
   que tus notas personales son lo último que se lee en ese nivel.

Los `CLAUDE.md` de **subdirectorios por debajo** del directorio de trabajo no se
cargan al arrancar: entran cuando Claude lee archivos de esos subdirectorios.
Guarda ese dato, porque es media explicación de la sección 4.7.

**Dos trucos que ahorran contexto de verdad:**

- **Los comentarios HTML de bloque se eliminan antes de inyectar el contenido.**
  `<!-- nota para el que mantenga esto -->` cuesta **cero tokens**. Los comentarios
  dentro de bloques de código sí se conservan, y todos siguen visibles si abres el
  archivo con la herramienta de lectura. Es documentación gratis para humanos.
- **`claudeMdExcludes`** para saltarte los `CLAUDE.md` de otros equipos en un
  monorepo.

Y una trampa: **`--add-dir` no carga los `CLAUDE.md` del directorio añadido**. Si
los quieres, hay que pedirlo explícitamente:

```bash
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../config-compartida
```

Eso carga `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md` y
`CLAUDE.local.md` del directorio adicional.

---

## 4.3 · Imports, y qué hacer si ya tienes `AGENTS.md`

Un `CLAUDE.md` puede importar otros archivos con `@ruta/al/archivo`. Se expanden y
se cargan al arrancar, junto al archivo que los referencia.

- Rutas relativas y absolutas. **Las relativas se resuelven respecto al archivo que
  contiene el import**, no respecto al directorio de trabajo.
- Los imports pueden anidarse, con un **máximo de cuatro saltos**.
- El análisis se salta el código en línea y los bloques cercados. Para nombrar una
  ruta sin importarla, ponla entre comillas invertidas.

**`AGENTS.md`: Claude Code lee `CLAUDE.md`, no `AGENTS.md`.** Si tu repositorio ya
usa `AGENTS.md` para otros agentes, crea un `CLAUDE.md` que lo importe y añade
debajo lo específico de Claude. Así no duplicas:

```markdown
@AGENTS.md

# Específico de Claude Code
- Los tests se lanzan con `npm test`, nunca con `jest` directamente
```

⚠️ **El aviso de seguridad de esta sección.** Un import de un archivo de memoria
del proyecto es **externo** cuando su ruta resuelve fuera del directorio de
trabajo. La primera vez, Claude Code muestra un diálogo de aprobación listando los
archivos. **Si lo rechazas, los imports quedan desactivados y el diálogo no vuelve
a aparecer.** Existe para protegerte de lo que otros confirmen en un proyecto
compartido. Los imports de los archivos de ámbito de usuario los escribiste tú, así
que cargan sin diálogo.

Detalle de worktrees: un `CLAUDE.local.md` ignorado por git **solo existe en el
worktree donde lo creaste**. Para compartir preferencias personales entre
worktrees, importa un archivo de tu carpeta personal: `@~/.claude/mis-notas.md`.

---

## 4.4 · Organizar con `.claude/rules/`

Para proyectos grandes, las instrucciones se parten en archivos dentro de
`.claude/rules/`. Todos los `.md` se descubren **recursivamente**, así que puedes
tener `frontend/` y `backend/` dentro.

```text
tu-proyecto/
└── .claude/
    ├── CLAUDE.md
    └── rules/
        ├── estilo-codigo.md
        ├── testing.md
        └── seguridad.md
```

**Sin frontmatter `paths`, una regla se carga al arrancar con la misma prioridad
que `.claude/CLAUDE.md`.** O sea: es contexto permanente, igual de caro.

Lo interesante son las **reglas por ruta**:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# Reglas de la API
- Todo endpoint valida su entrada
- Formato de error estándar
```

Solo se cargan cuando Claude trabaja con archivos que casan con el patrón. **Se
disparan al leer un archivo que coincide, no en cada uso de herramienta.** Desde
**v2.1.198** la coincidencia también funciona cuando Claude llega al archivo por
una ruta con enlace simbólico.

Nota de versión que importa en equipos: las reglas de proyecto se saltan si
excluyes `project` de `--setting-sources`. **Antes de v2.1.211**, las reglas que
cargan bajo demanda se cargaban igualmente aunque lo excluyeras.

💡 **Opinión operativa.** La documentación lo dice de pasada y merece un cartel:
*para instrucciones específicas de una tarea que no necesitan estar siempre en
contexto, usa skills en vez de reglas*. Una regla sin `paths` es tan cara como el
`CLAUDE.md`. La progresión sana es: `CLAUDE.md` → regla con `paths` → skill, y casi
todo el mundo se queda en el primer escalón.

---

## 4.5 · Auto memory

Claude acumula conocimiento entre sesiones sin que escribas nada: comandos de
compilación, hallazgos de depuración, notas de arquitectura, preferencias de
estilo. No guarda algo cada sesión; decide según si le va a servir en el futuro.

**Dónde vive:** `~/.claude/projects/<proyecto>/memory/`. La ruta se deriva del
repositorio git, así que **todos los worktrees y subdirectorios del mismo repo
comparten un único directorio de memoria**. Fuera de un repo, se usa la raíz del
proyecto.

Dentro hay un `MEMORY.md` que es el índice, más archivos por tema. Del M1: **se
cargan las primeras 200 líneas o 25 KB de `MEMORY.md`**, lo que llegue antes.

**Cómo se apaga:** está encendida por defecto. El interruptor de `/memory` escribe
`autoMemoryEnabled` en tu configuración de usuario; para un solo proyecto, ponlo en
el `settings.json` de ese proyecto; por variable de entorno,
`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

**Dónde se guarda:** `autoMemoryDirectory` se lee de cualquier ámbito, pero puesto
en el proyecto o en local **solo se honra tras aceptar el diálogo de confianza del
espacio de trabajo**, la misma puerta que gobierna los hooks. Es el patrón del M3:
lo que un repositorio ajeno podría usar para moverte archivos, no se lee del
repositorio sin permiso explícito.

---

## 4.6 · `CLAUDE.md` para toda la organización

Se despliega un `CLAUDE.md` gestionado que aplica a todos los usuarios de la
máquina, **y que la configuración individual no puede excluir**:

| Sistema | Ruta |
|---|---|
| macOS | `/Library/Application Support/ClaudeCode/CLAUDE.md` |
| Linux y WSL | `/etc/claude-code/CLAUDE.md` |
| Windows | `C:\Program Files\ClaudeCode\CLAUDE.md` |

Se reparte con MDM, directivas de grupo, Ansible o lo que uses. Alternativa sin
archivo suelto: la clave `claudeMd` dentro de `managed-settings.json`.

**Ámbito:** todas las sesiones de la máquina, en todos los repositorios. Para guía
específica de un repositorio, un `CLAUDE.md` de proyecto confirmado en git.
**Precedencia:** carga antes que el de usuario y el de proyecto.

---

## 4.7 · Qué sobrevive a la compactación

La sección más útil del módulo, y la respuesta a "se le ha olvidado lo que le dije".

**Sobrevive:** el `CLAUDE.md` de la raíz del proyecto. Tras `/compact`, Claude lo
**vuelve a leer del disco y lo reinyecta**.

**No se reinyecta automáticamente:** los `CLAUDE.md` anidados en subdirectorios y
las reglas con frontmatter `paths`. Vuelven a cargarse la próxima vez que Claude
lea un archivo de ese subdirectorio o que case con el patrón.

Así que si una instrucción desapareció tras compactar, solo hay tres
posibilidades, y conviene descartarlas en este orden:

1. Se dio **solo en la conversación**. Es la causa más frecuente con diferencia.
2. Vive en un `CLAUDE.md` anidado que aún no se ha recargado.
3. Es una regla por ruta que no ha casado con ningún archivo desde entonces.

La cura de la primera es la regla que gobierna el módulo: **lo que tiene que
persistir va al `CLAUDE.md`, no al historial.**

---

## 4.8 · Cuándo mover algo del `CLAUDE.md` a otro sitio

### Tabla 5 · Coste de contexto por mecanismo

| Mecanismo | Qué ocupa | Cuándo se paga | Ejemplo oficial |
|---|---|---|---:|
| `CLAUDE.md` de proyecto | El archivo entero | **Cada turno de cada sesión** | 1.800 tokens |
| `~/.claude/CLAUDE.md` | El archivo entero | Cada turno de cada sesión | 320 tokens |
| Regla sin `paths` | El archivo entero | Cada turno de cada sesión | como el anterior |
| Auto memory | 200 líneas o 25 KB de `MEMORY.md` | Cada sesión | 680 tokens |
| Regla con `paths` | El archivo | Al leer un archivo que casa | variable |
| Skill | Solo su descripción | Descripción siempre, cuerpo al activarse | 450 tokens todas |
| Servidor MCP | Solo los **nombres** de las herramientas | Nombres siempre, esquemas bajo demanda | 120 tokens |
| Subagente | Nada en tu sesión | Solo vuelve su resumen | 420 tokens de vuelta |
| Hook | Nada. Corre fuera del modelo | Nunca | 120 tokens su salida |

*Cifras del recorrido de ejemplo de la documentación oficial, no constantes universales. Mide las tuyas con `/context`.*

### La regla de decisión

Mira tu `CLAUDE.md` y para cada bloque pregúntate: **¿esto hace falta en todas las
tareas de este repositorio?**

- **Sí** → se queda. Es lo único que justifica pagarlo en cada turno.
- **No, solo cuando toco cierta zona del código** → regla con `paths`.
- **No, solo cuando hago cierta tarea** → skill.
- **No es contexto, es una prohibición** → hook. No estaba en el sitio equivocado:
  estaba en la categoría equivocada.

---

## Checklist de verificación

- [ ] Sé que `CLAUDE.md` es contexto y no configuración impuesta.
- [ ] Sé cuántos `CLAUDE.md` se están cargando en mi proyecto y en qué orden.
- [ ] He usado comentarios HTML para las notas de mantenimiento, que salen gratis.
- [ ] Ninguna de mis reglas sin `paths` contiene algo que solo aplica a veces.
- [ ] Si tengo `AGENTS.md`, mi `CLAUDE.md` lo importa en vez de duplicarlo.
- [ ] Sé dónde está mi directorio de auto memory y he mirado qué guardó.
- [ ] Lo que tiene que sobrevivir a `/compact` está en el `CLAUDE.md` de la raíz.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "Le digo que siempre haga X y no siempre lo hace" | Es contexto, no configuración. Si no es negociable, hook |
| "Se le olvidó lo que le dije al principio" | Se dio solo en conversación. Compactó y se fue |
| "Mi regla de la API no se aplica" | Tiene `paths` y aún no ha leído ningún archivo que case |
| "El `CLAUDE.md` del subdirectorio no aparece" | No carga al arrancar, entra al leer archivos de ahí |
| "Añadí un directorio con `--add-dir` y no lee su `CLAUDE.md`" | Necesitas `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` |
| "Rechacé un diálogo de imports y ya no me lo pide" | Es por diseño: quedan desactivados y no vuelve a preguntar |
| "En el monorepo se cuela el `CLAUDE.md` de otro equipo" | `claudeMdExcludes` |
| "Claude elige una de dos reglas al azar" | Se contradicen. Poda periódica |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `memory.md` | 35.604 | Todo el módulo: CLAUDE.md, imports, rules, auto memory, compactación |
| `claude-directory.md` | 90.641 | Ubicación de `rules/` en el árbol |
| `context-window.md` | 58.687 | Cifras de la tabla 5 y qué sobrevive a la compactación |
| `settings.md` | 285.543 | `autoMemoryEnabled`, `autoMemoryDirectory`, `claudeMdExcludes` |

**Marcas pendientes:** ninguna. El `⚠️ VERIFICAR` que venía de la Fase 0 queda
cerrado: `.claude/rules/` se documenta dentro de `memory.md`, no en una página
propia, y el índice de la guía se corrige en consecuencia.
