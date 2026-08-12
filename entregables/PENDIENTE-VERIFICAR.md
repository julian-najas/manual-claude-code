# Pendiente de verificar

**Corte: 12 de agosto de 2026 · CLI 2.1.228.**

Los 21 módulos cierran **sin ninguna marca `⚠️ VERIFICAR` abierta**: los 44 avisos
que lleva la guía son correcciones resueltas, cambios de comportamiento por versión
o límites de interpretación, no dudas.

Lo que sigue es lo que **sí** queda por hacer, ordenado por lo que más deprisa
caduca.

---

## 1 · Caduca solo, y hay que revisarlo pronto

| Qué | Por qué caduca | Cuándo revisar |
|---|---|---|
| **Auto mode pasa a ser el modo por defecto el 14 de agosto de 2026** | Está escrito en futuro en el M5, el M12, el M20 y el M21 | **Pasado mañana.** Cambiar a pasado |
| **Versión verificada, 2.1.228** | Salen versiones casi a diario | En cada revisión |
| **Digests de las semanas 31 y 33** | No existían al escribir. Pueden publicarse | Semanal |
| **Precio de ultrareview, 5-25 $** | Precio de terceros | Trimestral |
| **Retirada de Claude Code en Slack** | La fecha de corte la da el equipo de cuenta | Trimestral |

---

## 2 · Páginas inventariadas y no leídas

De las **187 páginas** del índice oficial, esta guía cita **120**. Las que faltan
están declaradas en el módulo que las tocaría, y ninguna sostiene una afirmación
de la guía. Son estas:

| Bloque | Páginas | Módulo destino | Para qué harían falta |
|---|---:|---|---|
| Detalle del gateway de Anthropic | 5 | M14 | Configuración, límites de gasto, despliegue, AWS, GCP |
| Detalle de entornos self-hosted | 6 | M14 | Quickstart, deploy, configuración, pruebas, referencia, identidad |
| Referencias del Agent SDK | 18 | M17 | **Firmas concretas de la API** de TypeScript y Python |
| Detalle de escritorio | 4 | M12 | Linux, WSL, tareas programadas, simulador de iOS |
| Resto | ~34 | varios | Páginas de apoyo y quickstarts |

⚠️ **La fila del SDK es la que más importa.** El M17 es un mapa de decisiones, no
una referencia de API. **Quien vaya a escribir código necesita las referencias de
TypeScript y Python**, y así está dicho en el módulo.

---

## 3 · Verificado contra el binario, ausente de la documentación

Hallazgos propios del cruce de `cli-reference.md` contra `claude --help` en 2.1.228:

| Bandera | Qué hace | Estado |
|---|---|---|
| `--brief` | *Enable SendUserMessage tool for agent-to-user communication* | **No aparece en ninguna de las 120 páginas citadas** |
| `--file <specs...>` | *File resources to download at startup*, formato `file_id:ruta` | Se menciona en `changelog` y `permissions`, **no en `cli-reference`** |

**Matiz obligatorio:** no se han revisado las 187 páginas. Lo verificable es que
**no están en la página donde un lector iría a buscarlas**.

---

## 4 · Pruebas con coste, no ejecutadas

En `D2-verificador/registro.yaml`, marcadas y omitidas a propósito porque gastan
dinero:

| ID | Qué comprueba | Cómo lanzarla |
|---|---|---|
| `CST-001` | Que una llamada mínima con `CLAUDE.md` grande ya consume decenas de miles de tokens de entrada | `verificar.py --con-coste` |
| `SEG-002` | El experimento de inyección de EXP-001, que **depende del modelo y de la versión y por tanto caduca** | `verificar.py --con-coste` |

---

## 5 · Comprobaciones que necesitan una persona

| ID | Qué | Por qué no se automatiza |
|---|---|---|
| `HOK-001` | Que los hooks se configuran en `settings.json` y no en archivo aparte | Contraste documental trimestral |
| `TRB-002` | Que borrar la caché de proyecto no borra la configuración de usuario | Requiere una máquina limpia |

---

## 6 · Fuera del alcance de esta guía

| Qué | Quién |
|---|---|
| Inventario de atribuciones MIT en `NOTICE-FUENTES.md` | Escribano |
| Confirmar el tipo de IVA del producto, 4 % o 21 % | Gestor |
| Portada y diseño editorial | Julián |

---

## 7 · Cómo se mantiene esto vivo

El mecanismo ya está construido y no depende de que nadie se acuerde:

1. **`D2-verificador/verificar.py`** ejecuta las afirmaciones contra el CLI
   instalado y falla si alguna deja de ser cierta. Corre en CI cada madrugada y
   abre incidencia sola.
2. **`D8-boletin/detectar-roturas.py`** compara la superficie del CLI, banderas y
   subcomandos, contra la instantánea anterior y redacta el borrador del boletín.
3. **Regla de fuentes, corregida respecto al megaprompt:** digests disponibles
   **más el changelog desde la última versión cubierta**. Solo con digests, la
   guía nace desfasada, porque faltan semanas enteras.
