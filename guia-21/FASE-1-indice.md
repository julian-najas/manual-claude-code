<title>Fase 1 · Índice de la Guía Definitiva</title>

# Fase 1 · Índice definitivo

**Guía Definitiva de Claude Code** · corte 12 de agosto de 2026 · CLI 2.1.228
Aprobado en Fase 0: **opción C** (dos productos) y las variables propuestas.

| Variable | Valor fijado |
|---|---|
| `AUDIENCIA` | [C] arquitecto o consultor que despliega para equipos. Lector secundario: [B] dev diario |
| `ENTORNO_OBJETIVO` | Linux servidor propio, con notas para macOS y WSL2 |
| `PROVEEDOR` | Mixto: suscripción Pro/Max como base, gateway propio como caso avanzado |
| `CASO_DE_USO_ANCLA` | Orquestación multiagente sobre servidor propio con MCP y cumplimiento RGPD |
| `LONGITUD_OBJETIVO` | **44.000 palabras** (revisado al alza en Fase 0) |

**Los dos productos y cómo se relacionan:** esta guía es la **capa de
referencia**, ordenada por materia, para consultar. El manual "Claude Code en
producción" (12 módulos, 149 €) es el **camino guiado** por encima, ordenado por
recorrido de aprendizaje y con laboratorios sobre un repositorio real. La guía
alimenta al manual; el manual no repite la guía.

---

## Reglas que valen para los 21 módulos

Cada módulo **abre** con tres líneas fijas: *para quién es · qué resuelve · qué
NO cubre*. Y **cierra** con dos bloques fijos: *checklist de verificación* y
*errores típicos*.

Cada sección responde en este orden: qué es → cuándo lo usas → cuándo NO lo usas
→ cómo se configura → cómo verificas que funciona → cómo falla.

Marcas obligatorias: `⚠️ VERIFICAR` con URL, `💡 OPINIÓN OPERATIVA`, versión
mínima cuando la documentación la dé, plan requerido, y etiqueta de *beta* o
*retirado*.

---

## Reparto de los artefactos de datos

Las 15 tablas obligatorias del §5, asignadas. Ninguna huérfana, ninguna repetida.

| # | Tabla | Módulo |
|---|---|---|
| 1 | Paridad de features por superficie | M12 |
| 2 | Disponibilidad por proveedor y por plan | M14 |
| 3 | Precedencia de settings, con conflicto resuelto | M3 |
| 4 | Modos de permisos × auto-aprobación × riesgo | M5 |
| 5 | Coste de contexto por mecanismo de extensión | M4 |
| 6 | Eventos de hooks × payload × control × ejemplo | M10 |
| 7 | Herramientas × permisos × límites de salida | M19 |
| 8 | Subagentes vs teams vs forks vs workflows vs background vs worktrees | M9 |
| 9 | Ámbitos de MCP × dónde vive × quién lo ve | M8 |
| 10 | Qué invalida el prompt cache y qué no | M15 |
| 11 | Modelos × alias × effort × contexto | M15 |
| 12 | Enfoques de aislamiento | M5 |
| 13 | Opciones de programación temporal | M10 |
| 14 | Errores frecuentes × mensaje literal × causa × fix | M18 |
| 15 | Cronología de cambios 2026 por semana | M21 |

**Diagramas:** bucle agéntico (M1), precedencia de configuración (M3), topología
de orquestación multiagente (M9). **Árbol de decisión:** arquitectura de
despliegue (M14).

---

## El índice

### M1 · Qué es y cómo funciona por dentro · 1.200 palabras
*Para quién:* todos. *Resuelve:* el modelo mental del bucle. *No cubre:* nada de configuración.
1.1 El bucle agéntico: modelo, herramientas, verificación · 1.2 Qué puede tocar y qué no ·
1.3 Superficies de ejecución frente a interfaces · 1.4 Sesiones y su ciclo de vida ·
1.5 Ventana de contexto y compactación · 1.6 Checkpoints y rewind
**Diagrama 1.** **Fuentes:** `overview`, `how-claude-code-works`, `features-overview`, `context-window`, `sessions`, `quickstart`

### M2 · Instalación, autenticación y actualización · 1.400
*Para quién:* quien monta la máquina. *Resuelve:* entorno reproducible. *No cubre:* despliegue de flota (M14).
2.1 Requisitos e instaladores · 2.2 Windows y WSL2 · 2.3 Alpine y musl ·
2.4 Verificación de firma y canales de release · 2.5 Fijar versión mínima en el equipo ·
2.6 Autenticación y precedencia de credenciales · 2.7 Tokens de larga duración ·
2.8 Desinstalación limpia · 2.9 Tabla: error de instalación → causa → fix
**Fuentes:** `setup`, `authentication`, `troubleshoot-install`

### M3 · El directorio `.claude/` y el sistema de configuración · 1.600
*Para quién:* quien configura para otros. *Resuelve:* "no me hace caso". *No cubre:* memoria (M4).
3.1 Mapa de ficheros, uno por uno · 3.2 Ámbitos y **precedencia exacta** ·
3.3 Settings de worktree · 3.4 `/config` y ver los settings efectivos ·
3.5 Depurar configuración · 3.6 Exclusión de ficheros sensibles
**Tabla 3 · Diagrama 2.** **Fuentes:** `claude-directory`, `settings`, `server-managed-settings`, `debug-your-config`

### M4 · Memoria y contexto · 1.800
*Para quién:* todos, desde el día dos. *Resuelve:* instrucciones que se pierden. *No cubre:* skills (M7).
4.1 CLAUDE.md por niveles e imports · 4.2 `AGENTS.md` · 4.3 `.claude/rules/`, reglas por ruta y symlinks (documentado dentro de `memory`) ·
4.4 Auto memory y `/memory` · 4.5 Despliegue de CLAUDE.md a nivel de organización ·
4.6 Qué sobrevive a la compactación · 4.7 Cómo se pierde una instrucción y cómo se diagnostica ·
4.8 Cuándo mover instrucciones de CLAUDE.md a una skill
**Tabla 5.** **Reutiliza:** árbol de decisión y tabla de impuesto de contexto del bloque D.
**Fuentes:** `memory` (contiene `rules`), `claude-directory`, `context-window`, `settings`

### M5 · Permisos, modos y seguridad operativa · 2.600
*Para quién:* quien responde de la máquina. *Resuelve:* el falso dilema entre preguntar por todo o permitirlo todo. *No cubre:* cumplimiento (M16).
5.1 Los seis modos, uno a uno (el Anexo A listaba cinco) · 5.2 **Auto mode pasa a ser el default el 14 de agosto**: qué implica y cómo fijar el tuyo ·
5.3 Sintaxis de reglas por herramienta · 5.4 Comandos compuestos y wrappers ·
5.5 Rutas protegidas y workspace trust · 5.6 Configurar el clasificador de auto mode ·
5.7 Sandboxing: aislamiento de FS y red, enmascarado de credenciales · 5.8 Dev containers, VM y cloud ·
5.9 Prompt injection: superficie de ataque real y mitigaciones
**Tablas 4 y 12.** **Reutiliza:** EXP-001, experimento propio de inyección en README.
**Fuentes:** `permissions`, `permission-modes`, `sandboxing`, `sandbox-environments`, `auto-mode-config`

### M6 · El flujo de trabajo diario que de verdad funciona · 1.800
*Para quién:* [B]. *Resuelve:* usarlo bien, no solo usarlo. *No cubre:* automatización (M10).
6.1 Explorar → planificar → implementar → verificar · 6.2 Darle algo contra lo que verificar ·
6.3 Corregir el rumbo pronto · 6.4 Gestión agresiva del contexto ·
6.5 Recetas por tarea: entender un repo, bug, refactor, tests, PR, docs, imágenes, notebooks ·
6.6 Modo plan y aprobación · 6.7 Rewind y checkpoints · 6.8 Anti-patrones y a qué huelen
**Fuentes:** `common-workflows`, `best-practices`, `prompt-library`, `checkpointing`, `large-codebases`

### M7 · Extensión: skills, comandos, output styles, statusline · 2.400
*Para quién:* quien ya repite tareas. *Resuelve:* procedimientos que no se activan. *No cubre:* reparto (M11).
7.1 Anatomía de una skill y su frontmatter · 7.2 **La descripción es el disparador**: cómo se escribe ·
7.3 Discovery y ficheros de soporte · 7.4 Argumentos y contexto dinámico inyectado ·
7.5 Ejecución en subagente y pre-aprobación de herramientas · 7.6 Evaluar e iterar una skill ·
7.7 Comandos slash propios · 7.8 Output styles frente a system prompt frente a CLAUDE.md ·
7.9 Statusline con contexto y coste · 7.10 Keybindings, fullscreen, dictado, accesibilidad
**Fuentes:** `skills`, `output-styles`, `statusline`, `terminal-config`, `fullscreen`, `accessibility`, `voice-dictation`, `keybindings`, `artifacts`, `interactive-mode`

### M8 · MCP a fondo · 2.600
*Para quién:* quien conecta sistemas. *Resuelve:* integrar sin regalar contexto ni permisos. *No cubre:* construir servidores desde el SDK (M17).
8.1 Transportes: stdio, HTTP, SSE, WebSocket · 8.2 Ámbitos y precedencia · 8.3 `.mcp.json` y expansión de variables ·
8.4 OAuth: callback fijo, credenciales pre-configuradas, scopes · 8.5 Headers dinámicos ·
8.6 Recursos MCP · 8.7 Prompts MCP como comandos · 8.8 Elicitation · 8.9 Límites de salida ·
8.10 **MCP tool search** para escalar a muchos servidores · 8.11 Backgrounding de llamadas largas ·
8.12 Claude Code *como* servidor MCP · 8.13 Configuración gestionada y allowlist corporativa ·
8.14 Tres ejemplos completos de principio a fin
**Tabla 9.** **Fuentes:** `mcp`, `mcp-quickstart`, `managed-mcp`, `channels`, `channels-reference`

### M9 · Paralelismo y agentes · 2.800
*Para quién:* [C]. *Resuelve:* la decisión que más dinero mueve. *No cubre:* hooks de ciclo de vida (M10).
9.1 Matriz de decisión entre las siete formas de paralelizar · 9.2 Subagentes: frontmatter, memoria persistente, hooks propios ·
9.3 Delegación automática frente a invocación explícita · 9.4 Agent teams ·
9.5 Forks · 9.6 Workflows · 9.7 Agent view y dispatch en segundo plano ·
9.8 **Cross-session messaging** (v2.1.224+, macOS y Linux) · 9.9 Worktrees y su aislamiento ·
9.10 Qué aísla, qué comparte, qué cuesta y cómo se mata cada uno ·
9.11 Ejemplos: revisión adversarial, hipótesis en competencia, fan-out sobre N ficheros
**Tabla 8 · Diagrama 3.** **Fuentes:** `agents`, `sub-agents`, `agent-view`, `agent-teams`, `cross-session-messaging`, `workflows`, `worktrees`

### M10 · Automatización: hooks, tareas programadas y headless · 2.800
*Para quién:* quien quiere que pase sin él delante. *Resuelve:* lo no negociable. *No cubre:* CI (M13).
10.1 Ciclo de vida y ubicaciones · 10.2 Matchers y el campo `if` ·
10.3 Entrada y salida: exit codes, JSON estructurado, HTTP · 10.4 Hooks basados en prompt y en agente ·
10.5 Hooks asíncronos · 10.6 **Los 31 eventos, con caso de uso real por evento** ·
10.7 `/loop`, recordatorios, cron, `/goal` · 10.8 Deep links ·
10.9 Modo no interactivo: `--print`, streaming JSON, salida estructurada, fallo de CI si no carga un plugin ·
10.10 Channels · 10.11 **Seis hooks listos para copiar**
**Tablas 6 y 13.** **Fuentes:** `hooks`, `hooks-guide`, `scheduled-tasks`, `goal`, `headless`, `deep-links`

### M11 · Plugins y distribución interna · 1.800
*Para quién:* quien ya tiene algo que funciona. *Resuelve:* que le funcione al equipo. *No cubre:* gobierno corporativo (M14).
11.1 Anatomía: skills, agents, hooks, MCP, LSP, monitors, themes · 11.2 El manifest ·
11.3 Plugins desde un directorio de skills · 11.4 Marketplaces: GitHub, git genérico, npm, rutas locales ·
11.5 **Zip con pin SHA-256** (nuevo en w32) · 11.6 Dependencias y versionado ·
11.7 Canales de release · 11.8 Restricciones gestionadas, hints y relevance ·
11.9 Walkthrough: de configuración suelta a plugin publicado en marketplace privado
**Fuentes:** `plugins`, `discover-plugins`, `plugin-marketplaces`, `plugin-dependencies`, `plugin-hints`, `plugin-relevance`, `plugins-reference`

### M12 · Superficies · 2.000
*Para quién:* equipos mixtos. *Resuelve:* qué se puede hacer dónde. *No cubre:* CI (M13).
12.1 Terminal · 12.2 VS Code · 12.3 JetBrains · 12.4 Desktop, con Linux, WSL, tareas programadas y simulador iOS ·
12.5 Web y entornos cloud · 12.6 Móvil · 12.7 Slack y Claude Tag · 12.8 Chrome y computer use ·
12.9 Remote Control y Trusted Devices · 12.10 Teleport terminal↔web · 12.11 Routines
**Tabla 1.** **Fuentes:** las 19 páginas de plataformas

### M13 · CI/CD y revisión de código · 1.600
*Para quién:* [C]. *Resuelve:* revisión sin humano delante. *No cubre:* qué NO automatizar va aquí, sí.
13.1 GitHub Actions: setup, permisos de la App, modos, coste · 13.2 Actions con proveedores cloud ·
13.3 GitHub Enterprise Server · 13.4 GitLab CI/CD · 13.5 Code Review y `REVIEW.md` ·
13.6 `/code-review` local y `/review` como alias · 13.7 ultrareview y su coste ·
13.8 Plugins de seguridad · 13.9 Qué automatizar y qué no
**Fuentes:** `github-actions`, `github-actions-cloud-providers`, `github-enterprise-server`, `gitlab-ci-cd`, `code-review`, `security-guidance`, `claude-security`

### M14 · Despliegue empresarial · 3.000
*Para quién:* [C], es su módulo. *Resuelve:* qué arquitectura elegir. *No cubre:* política de datos (M16).
14.1 Managed settings frente a server-managed settings, y fail-closed · 14.2 Bedrock y Claude Platform on AWS ·
14.3 Google Agent Platform · 14.4 Microsoft Foundry · 14.5 Pinning de modelo, IAM, contexto de 1M ·
14.6 Claude apps gateway: config, spend limits, deploy, AWS, GCP · 14.7 Gateways genéricos: protocolo, headers, descubrimiento de modelos ·
14.8 Rotación de credenciales con `apiKeyHelper` · 14.9 Proxies corporativos, CA propia, mTLS ·
14.10 Launcher corporativo y devcontainers · 14.11 **Entornos self-hosted** (beta, Team/Enterprise) ·
14.12 **Árbol de decisión: qué arquitectura según tamaño de equipo y requisitos de datos**
**Tabla 2 · Árbol de decisión.** **Fuentes:** las 29 páginas de despliegue

### M15 · Modelos, coste y observabilidad · 2.200
*Para quién:* quien paga. *Resuelve:* que la factura deje de sorprender. *No cubre:* privacidad (M16).
15.1 Modelos y alias, `default` y `opusplan` · 15.2 Cadenas de fallback ·
15.3 Niveles de effort y extended thinking · 15.4 Fast mode y advisor ·
15.5 Contexto extendido y umbrales de auto-compactación · 15.6 **Prompt caching: qué lo invalida y qué no** ·
15.7 `/usage` y `/context` · 15.8 Telemetría OTLP: métricas, eventos, trazas ·
15.9 Analytics de Team y Enterprise · 15.10 Recetas de reducción de tokens por impacto real
**Tablas 10 y 11.** **Reutiliza:** el capítulo de la factura, 4.195 llamadas medidas.
**Fuentes:** `model-config`, `fast-mode`, `advisor`, `prompt-caching`, `costs`, `monitoring-usage`, `analytics`

### M16 · Datos, cumplimiento y privacidad · 1.400
*Para quién:* quien firma. *Resuelve:* qué contestar a legal. *No cubre:* arquitectura (M14).
16.1 Política de datos y entrenamiento · 16.2 Retención · 16.3 ZDR: qué cubre, qué no, qué features desactiva ·
16.4 BAA y salud · 16.5 Auditoría de eventos hacia SIEM · 16.6 Control de artifacts y conectores ·
16.7 **RGPD y LOPD: qué sale de tu red en cada arquitectura y cómo se cierra**
**Reutiliza:** la política interna de un folio del bloque D.
**Fuentes:** `security`, `data-usage`, `zero-data-retention`, `legal-and-compliance`

### M17 · Agent SDK · 3.000
*Para quién:* quien construye producto. *Resuelve:* cuándo dejar el CLI. *No cubre:* uso interactivo.
17.1 Cuándo pasar de CLI a SDK · 17.2 El bucle de agente · 17.3 Sesiones y `SessionStore` ·
17.4 Streaming · 17.5 Structured outputs · 17.6 Custom tools · 17.7 MCP desde el SDK y tool search ·
17.8 Subagentes · 17.9 Modificar el system prompt · 17.10 Slash commands, skills y plugins desde el SDK ·
17.11 Permisos y hooks · 17.12 File checkpointing · 17.13 Cost tracking y observabilidad ·
17.14 Hosting y despliegue seguro · 17.15 **Un agente completo, comentado línea a línea**
**Fuentes:** las 32 páginas de `agent-sdk/`

### M18 · Diagnóstico y errores · 1.600
*Para quién:* todos, el día malo. *Resuelve:* no perder una tarde. *No cubre:* nada nuevo, es transversal.
18.1 Árbol: síntoma → capa → comprobación → fix · 18.2 Capa de instalación · 18.3 Auth · 18.4 Red ·
18.5 Permisos · 18.6 Contexto · 18.7 Plugins · 18.8 MCP · 18.9 Sandbox ·
18.10 `claude doctor`, `/context`, `/hooks`, `/mcp` · 18.11 Arranque con configuración limpia ·
18.12 **Los ~40 errores más frecuentes con su mensaje literal**
**Tabla 14.** **Fuentes:** `troubleshooting`, `errors`, `troubleshoot-install`, `debug-your-config`

### M19 · Referencia rápida · 2.200
*Para quién:* quien ya sabe y solo quiere el dato. *Resuelve:* dejar de buscar. *No cubre:* explicaciones.
19.1 Todos los comandos slash · 19.2 Todos los flags del CLI · 19.3 Variables de entorno por categoría ·
19.4 Herramientas con su comportamiento y límites · 19.5 Atajos de teclado ·
19.6 Sintaxis de reglas de permisos · 19.7 Los 31 eventos de hooks · 19.8 Glosario
**Tabla 7.** Todo en formato tabla, pensado para imprimir. **Fuentes:** `cli-reference`, `commands`, `env-vars`, `tools-reference`, `glossary`

### M20 · Playbooks · 3.400
*Para quién:* quien quiere copiar una solución entera. *Resuelve:* el "y todo junto, ¿cómo queda?". *No cubre:* teoría.
20.1 Monorepo grande · 20.2 Legacy sin tests · 20.3 Equipo de 20 devs con despliegue gobernado ·
20.4 **Automatización nocturna desatendida en servidor propio** (el ancla) · 20.5 Desarrollo de un plugin interno
Cada uno: setup concreto, ficheros completos, métricas de éxito, riesgos.
**Sin páginas fuente: se construye.** Apoyo en `large-codebases`, `communications-kit`, `champion-kit`

### M21 · Features retiradas, renombradas y trampas de tutoriales viejos · 1.200
*Para quién:* quien llega de YouTube. *Resuelve:* horas perdidas. *No cubre:* nada actual.
21.1 Retiradas: Ultraplan y su comando · 21.2 Renombrados: `/review` → alias de `/code-review` ·
21.3 Límites que ya no existen: el tope de 200 subagentes · 21.4 Cambios de default: auto mode desde el 14 de agosto ·
21.5 **Cronología semanal 2026 con versión**
**Tabla 15.** **Fuentes:** las 21 páginas de `whats-new/` y el `changelog`

---

## Resumen de presupuesto

| | |
|---|---|
| Módulos | 21 |
| Palabras | 44.400 |
| Páginas fuente | 187, todas asignadas |
| Turnos de redacción | 35 |
| Tablas obligatorias | 15, todas asignadas |
| Diagramas | 3 Mermaid + 1 árbol de decisión |
| Piezas reutilizadas del bloque D | 4 (árbol, EXP-001, factura, política) |

## Orden de escritura

Por dependencia, no por número: **M1 → M3 → M4 → M5 → M7 → M9 → M8 → M10 → M11 →
M15 → M6 → M13 → M14 → M16 → M12 → M17 → M18 → M19 → M20 → M21 → M2**.

El M2 se escribe el último a propósito: es el que más envejece y conviene
redactarlo lo más cerca posible de publicar. El M21 va justo antes porque necesita
que el resto esté escrito para saber qué contradice a los tutoriales viejos.

---

**Siguiente:** Fase 2, módulo M1. Descargo sus 6 páginas fuente, escribo, listo
las fuentes usadas y paro.
