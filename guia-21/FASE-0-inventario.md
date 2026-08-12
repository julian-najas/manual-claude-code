<title>Fase 0 · Inventario de la Guía Definitiva</title>

# Fase 0 · Inventario y plan de módulos

**Ejecutado el 12 de agosto de 2026** · CLI instalado en la máquina: **2.1.228**
Fuentes descargadas hoy, no de memoria. Paro aquí, como pide el protocolo.

---

## 1 · Lo que he descargado

| Fuente | Resultado |
|---|---|
| `llms.txt` | 200 · 42.009 bytes · **187 páginas** indexadas |
| `claude_code_docs_map.md` | 200 · 116.557 bytes |
| `changelog.md` | 200 · 528.057 bytes · llega hasta **2.1.228, del 11 de agosto** |
| `whats-new/2026-w32.md` | 200 · 8.830 bytes |
| `whats-new/2026-w31.md` | **404** |
| `whats-new/2026-w33.md` | **404** |
| `hooks.md` | 200 · 267.830 bytes |

---

## 2 · Contraste con el Anexo A

### Lo que se sostiene

**El Anexo A no inventa nada.** He cruzado las 106 páginas que nombra contra las
187 reales del índice: **las 106 existen**. Cero slugs fantasma.

**Los 31 eventos de hooks son exactos.** Cruzados uno a uno contra `hooks.md`: no
falta ninguno y no sobra ninguno. Es el dato más fácil de inventar de todo el
anexo y está bien.

**La semana 32 coincide punto por punto** con el digest oficial: cross-session
messaging en 2.1.224, entornos self-hosted en beta, auto mode por defecto el 14
de agosto, `/review` como alias, tope de 200 subagentes eliminado, marketplaces
en zip con pin SHA-256, aislamiento de worktrees ampliado a Bash, Ultraplan
retirado.

### Lo que hay que corregir

**1. El Anexo A se queda una semana corto.** Cubre hasta `v2.1.224` (semana 32,
del 3 al 7 de agosto). La máquina corre **2.1.228, publicada el 11 de agosto**.
Faltan cuatro versiones.

**2. No hay digest de la semana 33, ni de la 31.** Los dos dan 404 y el índice
salta de la w30 a la w32. Es decir: **para todo lo posterior al 7 de agosto la
única fuente es el changelog**, no los digests. El protocolo del §2.3 del
megaprompt manda leer w28→w32 y eso deja fuera lo más reciente.

**3. Novedades de 2.1.225 a 2.1.228 que el Anexo A no recoge** (del changelog):

- Aviso de límite de gasto del gateway, nombrando el tope, su hora de reinicio y
  el mensaje del operador. Requiere el gateway en 2.1.225.
- `claude agents` ahora pide confirmación de confianza en directorios no fiables.
- `SendMessage` puede **iniciar** conversación con sesiones de Remote Control de
  otras máquinas por nombre, no solo responder.
- 2.1.228 es casi toda arreglos, y dos importan para nosotros: limpieza de sesión
  borrando contenido de la carpeta de memoria de un proyecto, y fusión de ajustes
  donde una entrada de marketplace heredaba cabeceras de otra capa.

**4. Siete páginas existen y el Anexo A no las nombra.** Cuatro son de
diagnóstico, y el Anexo A no asignaba ninguna página a ese tema:
`troubleshooting`, `troubleshoot-install`, `errors`, `debug-your-config`. Las
otras tres: `overview`, `quickstart`, `github-actions-cloud-providers`.

**5. `rules` no existe como página.** El módulo M4 del megaprompt pide cubrir
`.claude/rules/` con reglas por ruta y symlinks. En el índice solo hay `memory`.
O está dentro de esa página, o la fuente es otra. Marcado como `⚠️ VERIFICAR`
antes de escribir M4.

---

## 3 · Plan de módulos y esfuerzo

Las 187 páginas quedan repartidas entre los 21 módulos. **Ninguna sin asignar.**

| Módulo | Tema | Páginas fuente | Turnos | Palabras est. |
|---|---|---:|---:|---:|
| **M1** | Qué es y cómo funciona | 6 | 1 | 1.200 |
| **M2** | Instalación y auth | 3 | 1 | 1.400 |
| **M3** | .claude/ y configuración | 4 | 1 | 1.600 |
| **M4** | Memoria y contexto | 1 | 1 | 1.800 |
| **M5** | Permisos y seguridad operativa | 5 | 2 | 2.600 |
| **M6** | Flujo de trabajo | 5 | 1 | 1.800 |
| **M7** | Extensión | 10 | 2 | 2.400 |
| **M8** | MCP | 5 | 2 | 2.600 |
| **M9** | Paralelismo y agentes | 7 | 2 | 2.800 |
| **M10** | Automatización | 6 | 2 | 2.800 |
| **M11** | Plugins y distribución | 7 | 1 | 1.800 |
| **M12** | Superficies | 19 | 2 | 2.000 |
| **M13** | CI/CD y revisión | 7 | 1 | 1.600 |
| **M14** | Despliegue empresarial | 29 | 3 | 3.000 |
| **M15** | Modelos. coste. observabilidad | 7 | 2 | 2.200 |
| **M16** | Datos y cumplimiento | 4 | 1 | 1.400 |
| **M17** | Agent SDK | 32 | 3 | 3.000 |
| **M18** | Diagnóstico | 2 | 1 | 1.600 |
| **M19** | Referencia rápida | 5 | 2 | 2.200 |
| **M20** | Playbooks y adopción | 2 | 3 | 3.400 |
| **M21** | Retiradas y cambios | 21 | 1 | 1.200 |
| | **Total** | **187** | **35** | **44.400** |
Un turno es una sesión de redacción con sus fuentes descargadas delante. Los tres
módulos más caros son los previsibles: despliegue empresarial (29 páginas), Agent
SDK (32) y los playbooks, que no tienen página fuente porque hay que construirlos.

---

## 4 · Las cuatro decisiones que necesito antes de la Fase 1

### 4.1 · El presupuesto de palabras no cuadra con la ambición

El megaprompt pide **12.000 a 20.000 palabras** y a la vez 21 módulos
exhaustivos, 15 tablas, 3 diagramas y ningún módulo reducido a un párrafo. Las
dos cosas no caben juntas: sale a menos de mil palabras por módulo.

Mi estimación honesta para lo que pide el resto del documento es **44.000
palabras**. Hay tres salidas:

| Salida | Qué implica |
|---|---|
| **A. Subir el presupuesto a 45.000** | Es la guía de referencia que describe el §1. Unas 130 páginas maquetadas |
| **B. Mantener 20.000 y cortar a 12 módulos** | Vuelve a ser el manual que ya habíamos decidido, con menos cobertura empresarial |
| **C. Dos productos** | La guía de referencia larga, y el manual de 149 € como el camino guiado por encima |

**Recomiendo la C**, y no por ambición: es que ya tenemos construido el esqueleto
del manual de 12 módulos y ocho activos del bloque D. Esta guía de 21 módulos es
la **capa de referencia** que le falta debajo, y es exactamente lo que justifica
las actualizaciones de doce meses.

### 4.2 · El bloque VARIABLES viene sin rellenar

Propongo estos valores, sacados de tu contexto real. Corrige lo que no encaje:

| Variable | Propuesta |
|---|---|
| `AUDIENCIA` | **[C] arquitecto/consultor que despliega para equipos**, con [B] como lector secundario |
| `ENTORNO_OBJETIVO` | **Linux servidor propio** (el R630), con notas para macOS y WSL2 |
| `PROVEEDOR` | **Mixto**: suscripción Pro/Max como caso base y **gateway propio** como caso avanzado |
| `CASO_DE_USO_ANCLA` | Orquestación multiagente sobre servidor propio con MCP y cumplimiento RGPD |

El ancla importa más de lo que parece: decide qué ejemplos se escriben en los 21
módulos. Con esa, los módulos 14 y 16 dejan de ser relleno corporativo y pasan a
ser el corazón del producto.

### 4.3 · Qué hago con lo ya construido

Del bloque D hay tres piezas que encajan directamente y no hay que rehacer:

- El **árbol de decisión** y su tabla de impuesto de contexto son la mitad del M4.
- El **experimento EXP-001** sobre la inyección en el README es material de
  primera para el M5, y es propio, no parafraseado de la documentación.
- El **capítulo de la factura**, con 4.195 llamadas medidas, es el M15.

### 4.4 · Un aviso sobre el propio protocolo

El §2 manda no escribir nada que no se haya leído hoy. Bien. Pero el §2.3 fija
las fuentes en los digests semanales, y acabamos de ver que **la w31 y la w33 no
existen**. Propongo cambiar esa regla por: *digests disponibles más el changelog
desde la última versión cubierta por el anexo*. Si no, el protocolo garantiza que
la guía nazca una semana desfasada.

---

## 5 · Informe de cobertura de esta fase

| | |
|---|---|
| Páginas indexadas | 187 |
| Páginas descargadas y leídas hoy | 5 (`llms.txt`, docs map, changelog, w32, hooks) |
| Páginas clasificadas a módulo | 187 de 187 |
| Afirmaciones del Anexo A verificadas | 106 slugs + 31 eventos de hooks + 13 puntos de la w32 |
| Contradicciones encontradas | 0 |
| Huecos encontrados | 5 |

**No he leído todavía el contenido de 182 páginas.** Se descargan al empezar cada
módulo, como manda el protocolo. Lo de hoy es el mapa, no el territorio.

---

## 6 · Siguiente paso

En cuanto contestes a 4.1 y 4.2, ejecuto la **Fase 1**: índice definitivo con
tablas obligatorias asignadas a su módulo, y paro otra vez.
