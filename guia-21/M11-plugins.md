# M11 · Plugins y distribución interna

> **Para quién es:** quien ya tiene algo que funciona en su máquina y quiere que funcione en las de su equipo.
> **Qué resuelve:** el "a mí me va y a ti no", y el reparto versionado.
> **Qué NO cubre:** cómo se escriben skills, hooks o subagentes (M7, M10, M9). Aquí solo se **empaquetan** y se **reparten**.

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 11.1 · Cuándo un plugin y cuándo no

Hay dos formas de añadir skills, agentes y hooks, y la diferencia visible es el
nombre con el que se invocan:

| Enfoque | Nombre de la skill | Para qué |
|---|---|---|
| **Suelto**, en `.claude/` | `/hola` | Flujos personales, ajustes de un proyecto, experimentos rápidos |
| **Plugin**, con su manifiesto | `/nombre-plugin:hola` | Compartir con el equipo, distribuir, **releases versionadas**, reutilizar entre proyectos |

Ese prefijo con dos puntos no es cosmético: es **espacio de nombres**. En cuanto
tres equipos publican una skill llamada `desplegar`, el prefijo es lo único que
evita que se pisen.

La recomendación oficial coincide con la del árbol de decisión del M1: **empieza
suelto en `.claude/` para iterar rápido, y conviértelo en plugin cuando esté listo
para compartir.** Empaquetar antes de que funcione solo reparte el problema.

---

## 11.2 · Anatomía, y el error que comete todo el mundo

⚠️ **El fallo número uno**, y está marcado como aviso en la propia documentación:

> No pongas `commands/`, `agents/`, `skills/` ni `hooks/` dentro de
> `.claude-plugin/`. **Dentro de `.claude-plugin/` solo va `plugin.json`.** Todos
> los demás directorios van en la raíz del plugin.

Y la segunda parte del aviso, que aclara una confusión aún más común: **la raíz
del plugin es el directorio propio de ese plugin**, el que pasas a `--plugin-dir`
o el que contiene `.claude-plugin/plugin.json`. **Nunca es `~/.claude/`.** Por eso
un `.mcp.json` colocado en `~/.claude/.mcp.json` no lo lee nadie.

La estructura correcta:

```text
mi-plugin/
├── .claude-plugin/
│   └── plugin.json        ← solo esto va aquí dentro
├── skills/
│   └── auditar/SKILL.md
├── agents/
├── hooks/
│   └── hooks.json
└── .mcp.json
```

Un plugin puede llevar **skills, agentes, hooks, servidores MCP, servidores LSP,
monitores en segundo plano, temas y ajustes por defecto**. Es decir: casi todo lo
que has configurado en los módulos anteriores cabe dentro de una caja.

Nota de migración: `commands/` son skills en archivos markdown planos, y la
documentación dice explícitamente que **para plugins nuevos se use `skills/`**.

---

## 11.3 · De directorio de skills a plugin

No hace falta empezar de cero: se puede **desarrollar el plugin dentro del propio
directorio de skills**, y el manifiesto es opcional si los componentes están en
las ubicaciones por defecto.

Esa es la ruta de migración real de un equipo: lo que ya tienes en `.claude/`
funciona; lo que se añade es el manifiesto, el nombre y la versión.

---

## 11.4 · Marketplaces: dos conceptos que se confunden

Esta distinción vale por medio módulo, y en la documentación viene con nota
propia porque se malinterpreta constantemente:

| | Fuente del **marketplace** | Fuente del **plugin** |
|---|---|---|
| Qué localiza | El catálogo `marketplace.json` | Cada plugin listado dentro |
| Dónde se fija | `/plugin marketplace add` o `extraKnownMarketplaces` | El campo `source` de cada entrada del catálogo |
| Anclaje admitido | `ref` (rama o etiqueta), **no `sha`** | `ref` **y `sha`** (commit exacto) |

Se anclan **de forma independiente**: un catálogo alojado en
`acme/plugin-catalog` puede listar un plugin que se descarga de
`acme/formateador`. Son dos repositorios distintos y dos anclajes distintos.

💡 **Opinión operativa.** Que el catálogo no admita `sha` y el plugin sí es
exactamente lo que quieres: el catálogo debe poder moverse para añadir entradas,
mientras que lo que se ejecuta en la máquina de tu gente debe poder clavarse a un
commit. Si tu política de seguridad exige reproducibilidad, el anclaje va en la
entrada del plugin, no en el catálogo.

---

## 11.5 · Las cinco fuentes de plugin

| Fuente | Campos | Notas |
|---|---|---|
| **Ruta relativa** | — | Directorio local dentro del repo del catálogo. **Debe empezar por `./`** y se resuelve contra la raíz del catálogo, no contra `.claude-plugin/` |
| **`github`** | `repo`, `ref?`, `sha?` | Lo habitual |
| **`url`** | git genérico | Para forjas propias |
| **`npm`** | `package`, `version?`, `registry?` | Se instala con `npm install`, admite registro privado |
| **`archive`** | `url`, `sha256?` | **Zip por HTTPS. Funciona sin git y sin npm en la máquina del usuario.** Requiere **v2.1.224 o posterior** |

La última es de la semana 32 y resuelve un problema muy concreto de empresa:
máquinas donde no hay git, o donde el acceso a la forja está restringido. Con el
`sha256` opcional además tienes integridad verificable, que es lo que pedirá
cualquiera que revise esto desde seguridad.

**Dónde acaba todo:** tras clonar o descargar, Claude Code copia el plugin a la
caché local versionada en `~/.claude/plugins/cache`, e **instala ahí dentro las
dependencias de Node elegibles**. Saberlo importa para depurar y para entender qué
hay que limpiar.

---

## 11.6 · Dependencias con restricción de versión

El escenario de la documentación es tan reconocible que lo traduzco entero,
porque es el argumento para usar restricciones:

> El equipo de plataforma mantiene `secrets-vault`, un servidor MCP sobre el
> almacén de secretos. El equipo de despliegue mantiene `deploy-kit`, que llama a
> `secrets-vault` para obtener credenciales. `deploy-kit` está probado contra
> `secrets-vault` 2.1.0. **Sin restricción de versión**, la próxima vez que
> plataforma etiquete una release que renombre una herramienta MCP, la
> autoactualización mueve a **todos** los ingenieros a la nueva versión y
> `deploy-kit` se rompe.

Con restricción, `deploy-kit` declara que necesita el rango `~2.1.0`, la gente se
queda en el parche `2.1.x` más alto que case, y el equipo de despliegue actualiza
**a su ritmo** publicando una versión nueva con una restricción más ancha.

La documentación cubre además cómo **agrupar plugins para un equipo**, cómo
**depender de un plugin de otro catálogo**, cómo **etiquetar releases** para que
la resolución de versiones funcione, cómo interactúan varias restricciones, y algo
que se agradece: **eliminar las dependencias autoinstaladas que quedan huérfanas**.

---

## 11.7 · Gobierno: tres piezas para una organización

**Restricciones gestionadas.** Del M3 y el M8: los settings gestionados pueden
imponer qué marketplaces se conocen y qué se permite. La postura correcta es lista
blanca, no lista negra.

**Hints, o cómo una herramienta se recomienda sola.** Si mantienes un CLI o un SDK
y tienes plugin en el marketplace oficial, tu herramienta puede **escribir un
marcador de una línea en la salida de error cuando detecta que corre dentro de
Claude Code**. Claude Code lee el marcador, **lo quita de la salida** y muestra al
usuario una propuesta de instalación, una sola vez.

**Relevance, o sugerir el plugin adecuado.** Si operas un catálogo para tu
organización, añades un bloque `relevance` a la entrada del plugin en
`marketplace.json` y pones el catálogo en la lista blanca de los settings
gestionados. Cuando la sesión de alguien case con las señales declaradas, Claude
Code le sugiere instalarlo.

💡 Las dos últimas son la respuesta a un problema real que no es técnico: **tienes
un plugin interno estupendo y nadie sabe que existe**. En vez de mandar correos,
la sugerencia aparece en el momento en que alguien está haciendo justo el trabajo
que el plugin resuelve.

---

## 11.8 · Recorrido completo: de configuración suelta a catálogo privado

1. **Funciona suelto.** Tienes en `.claude/` una skill, dos hooks y un subagente
   que usas a diario. No empaquetes todavía.
2. **Dale forma de plugin.** Crea el directorio, mueve `skills/`, `agents/` y
   `hooks/` a la **raíz**, y `plugin.json` dentro de `.claude-plugin/`. Este es el
   paso donde todo el mundo se equivoca; relee el 11.2.
3. **Pruébalo en local** con `--plugin-dir` antes de publicar nada.
4. **Crea el catálogo.** Un `marketplace.json` con sus campos obligatorios, en un
   repositorio propio, distinto del plugin.
5. **Elige la fuente del plugin.** `github` con `sha` si quieres reproducibilidad
   estricta; `archive` con `sha256` si en las máquinas de tu gente no hay git.
6. **Etiqueta la release** para que la resolución de versiones funcione, y declara
   restricciones si tu plugin depende de otro.
7. **Añade el catálogo a los settings gestionados** de la organización, con lista
   blanca.
8. **Opcional pero rentable:** añade el bloque `relevance` para que se sugiera
   solo a quien le sirve.
9. **Verifica en una máquina limpia**, que es el único sitio donde se comprueba de
   verdad que un plugin está bien empaquetado.

El paso 9 no es retórico. Todo lo que este módulo intenta evitar se manifiesta
únicamente en una máquina que no sea la tuya.

---

## Checklist de verificación

- [ ] Dentro de `.claude-plugin/` solo tengo `plugin.json`.
- [ ] Sé que la raíz del plugin nunca es `~/.claude/`.
- [ ] Mi plugin nuevo usa `skills/` y no `commands/`.
- [ ] He anclado la fuente del plugin con `sha` o `sha256` si necesito reproducibilidad.
- [ ] Mis dependencias entre plugins llevan restricción de versión.
- [ ] He etiquetado la release para que la resolución funcione.
- [ ] Mi organización tiene lista blanca de catálogos en settings gestionados.
- [ ] Lo he probado en una máquina que no es la mía.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "Mi plugin no encuentra las skills" | Las metiste dentro de `.claude-plugin/`. Solo va `plugin.json` |
| "Puse un `.mcp.json` en `~/.claude/` y no lo lee" | La raíz del plugin nunca es `~/.claude/` |
| "Mi ruta relativa no resuelve" | Debe empezar por `./` y se resuelve contra la raíz del catálogo |
| "Quise anclar el catálogo a un commit y no me deja" | Las fuentes de catálogo admiten `ref`, no `sha`. El anclaje fino va en el plugin |
| "Una actualización de otro equipo me rompió el plugin" | Falta restricción de versión en la dependencia |
| "En las máquinas de mi equipo no hay git" | Fuente `archive`: zip por HTTPS, v2.1.224+ |
| "Nadie usa el plugin interno" | Bloque `relevance` en el catálogo, o hints desde tu propio CLI |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `plugins.md` | 26.226 | Plugin frente a suelto, anatomía, el aviso de estructura |
| `plugins-reference.md` | 98.838 | Referencia de componentes y dependencias de Node |
| `plugin-marketplaces.md` | 81.739 | Catálogo, las cinco fuentes, `archive`, caché |
| `plugin-dependencies.md` | 21.948 | Restricciones de versión y resolución |
| `discover-plugins.md` | 29.464 | Instalación y activación |
| `plugin-relevance.md` | 15.669 | Sugerencia por señales |
| `plugin-hints.md` | 9.546 | Marcador desde un CLI propio |
| `whats-new/2026-w32.md` | 8.830 | Fuente `archive` con pin SHA-256 |

**Marcas pendientes:** ninguna.
