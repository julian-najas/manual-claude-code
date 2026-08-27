# Claude Code en producción

**El manual en castellano que no te pide que confíes en él: se verifica contra la
máquina.**

**Versión:** v2026.08
**Verificado contra:** cada módulo declara su versión del CLI, la del día en que
se midió. El libro no finge una sola.
**Estado de verificación:** [`D2-verificador/ESTADO.md`](D2-verificador/ESTADO.md)

Este repositorio no está afiliado, patrocinado ni respaldado por Anthropic.

> **Nota de posicionamiento, medida el 13 de agosto de 2026.** La documentación
> oficial de Claude Code **ya está traducida al castellano**: **173 de las 187
> páginas**, el **92,5 %**. Medición completa, no muestra, en
> [`evidencias/EXP-002`](evidencias/EXP-002-cobertura-castellano.md).
>
> Así que "en español" **no es el diferencial**. Lo son dos cosas: que aquí cada
> afirmación crítica **se ejecuta contra el binario** y el resultado se publica se
> vea bien o se vea mal; y que **las 14 páginas que faltan por traducir son casi
> todas de lo más reciente** (entornos self-hosted, mensajería entre sesiones,
> Claude Tag, los digests de las semanas 30 y 32), así que la traducción oficial
> va por detrás justo donde esta guía llega antes.

---

## Aquí hay dos productos, y no están al mismo nivel

| | Qué es | Estado |
|---|---|---|
| **Guía de referencia** · `guia-21/` | 21 módulos ordenados por materia, para consultar. 44.717 palabras, 15 tablas, 3 diagramas | **Terminada** |
| **Manual guiado** · `manuscrito/` | 12 módulos con laboratorios sobre un repositorio real, el producto de 149 € | **En obra: 9 de 12 módulos** |

La guía alimenta al manual; el manual no repite la guía. **Lo terminado es la
guía.** Llamar terminado al manual sería falso.

Para instalar la guía completa como skill: `entregables/skill-guia/instalar.sh`.
La skill de `D1-skill/` es la del **manual**, que es más pequeña y aún está en obra.

---

## Qué hay aquí

| Carpeta | Qué es | Estado |
|---|---|---|
| `D1-skill/` | El **manual** empaquetado como skill. Para la **guía**, ver `entregables/skill-guia/` | Instalable, en obra |
| `D2-verificador/` | Registro de afirmaciones del libro y runner que las comprueba contra el CLI | 71 pasan, 0 fallan |
| `D3-arbol/` | La lámina del árbol de decisión, en HTML e imprimible | Lista |
| `D4-factura/` | Analizador de gasto real y el capítulo de costes | Con datos medidos |
| `D5-politica/` | Plantilla de política interna de uso de agentes | Lista para firmar |
| `D6-repo-feo/` | El repositorio legacy que atraviesa los doce módulos | Sembrado |
| `D7-esceptico/` | El capítulo que argumenta cuándo no usar la herramienta | Escrito |
| `D8-boletin/` | Detector de roturas entre versiones y borrador del boletín semanal | Funciona |

## Empezar

**Instalar el manual como skill:**

```bash
cd D1-skill && ./instalar.sh
```

Después, dentro de Claude Code: `/manual-claude-code`.

**Comprobar que el libro sigue siendo cierto:**

```bash
python3 D2-verificador/verificar.py
```

Devuelve 0 si todas las afirmaciones comprobables pasan, 1 si alguna ha dejado
de ser cierta. Es el mismo comando que corre la CI cada madrugada.

**Medir tu propio gasto:**

```bash
python3 D4-factura/analizar_gasto.py 'ruta/a/tus/registros/*.jsonl'
```

**Preparar el boletín de la semana:**

```bash
python3 D8-boletin/detectar-roturas.py
```

## Las reglas de esta fábrica

1. **Toda afirmación crítica y automatizable está en `registro.yaml`** y se
   ejecuta contra el CLI instalado. Hoy son 28. **No son todas las afirmaciones
   del libro**: son las que se pueden comprobar solas y las que más daño harían
   si dejaran de ser ciertas. El resto lleva fuente, fecha y nivel de evidencia
   al pie de su módulo.
2. **La versión, visible y por módulo.** No hay una fecha de corte única que
   cubra el libro entero: cada módulo dice contra qué versión del CLI se
   escribió, en su cabecera y no en los créditos. La portada lleva la edición.
3. **Sin system prompts filtrados.** Sala limpia, declarada en el libro.
4. **Los euros no se inventan.** Los tokens se miden; las tarifas las pone quien
   las tiene.
5. **Si el libro y la máquina se contradicen, gana la máquina**, y eso es un
   fallo que se reporta, no que se disimula.
6. **Las decisiones de gobierno también se comprueban.** Que los dos repositorios
   sigan públicos y que el companion siga sirviendo son tres afirmaciones del
   registro (`REPO-001` a `REPO-003`), no algo que alguien tenga que recordar. Se
   añadieron después de que este repositorio cambiara de visibilidad y nadie se
   enterara en veinticuatro horas.

## Cómo se versiona

El libro se versiona como software: `v2026.08`, con changelog público y diff
entre versiones para que quien ya se lo leyó solo tenga que leer lo nuevo.
Cuatro revisiones al año, más parche cuando algo se rompa.

Cuando el verificador detecta una rotura, abre una incidencia sola. Antes de
cerrarla hay que: corregir el capítulo, subir la versión, anotar el changelog y
mandarlo al boletín.

---

## Licencia

**Dos licencias, a propósito** ([texto completo](LICENSE)):

| Qué | Licencia | En claro |
|---|---|---|
| **Código y plantillas** · `fabrica/`, `D2-verificador/`, `entregables/plantillas/`, hooks, workflows | **MIT** | Cógelo, adáptalo, úsalo en tu empresa, véndelo. Solo conserva el aviso |
| **Texto de la guía y el manual** · `guia-21/`, `manuscrito/`, láminas, evidencias | **Derechos reservados** | Léelo, úsalo en tu trabajo, cítalo con enlace. No lo republiques ni lo traduzcas |

Está público **para que se pueda auditar**, no para que se pueda redistribuir.
El argumento del producto es que cualquiera puede comprobar sus afirmaciones, y
eso exige poder leerlo.

---

## La fábrica: dos fuentes, muchas salidas

**Nada se edita a mano salvo las dos fuentes canónicas:**

- **`guia-21/M*.md`** · los 21 módulos. De su tabla de errores típicos salen los
  155 síntomas del companion.
- **`fabrica/resoluciones.yaml`** · el procedimiento completo de los síntomas que
  lo tienen: diagnóstico, comando de comprobación, pasos, criterio de aceptación,
  versión mínima, nivel de evidencia, límites y síntomas vecinos.

```
guia-21/M*.md  ──┬─→ entregables/guia-claude-code-2026-08.md   (guía ensamblada)
                 ├─→ entregables/skill-guia/.../modulos/        (copias para la skill)
                 ├─→ entregables/skill-guia/.../INDICE-SINTOMAS.md
                 └─┐
fabrica/resoluciones.yaml ─┴─→ companion/  (155 páginas, una por síntoma)

fabrica/hechos.yaml ─→ comprobar-coherencia.py ─→ falla si un .md o el .yaml se contradicen
D2-verificador/registro.yaml ─→ verificar.py ─→ falla si el libro deja de ser cierto
```

| Comando | Qué hace |
|---|---|
| `python3 fabrica/construir.py` | Regenera todas las salidas |
| `python3 fabrica/construir.py --comprobar` | No escribe. Falla si alguna está desfasada |
| `python3 fabrica/comprobar-coherencia.py` | Falla si un archivo contradice un hecho canónico |
| `python3 fabrica/generar-companion.py` | Regenera el companion. Falla si `resoluciones.yaml` no valida |

### Cobertura del companion

**Los 155 síntomas** salen con el procedimiento entero: diagnóstico, un comando
para comprobarlo, los pasos, un criterio objetivo de aceptación, versión mínima,
nivel de evidencia, límites y tres síntomas vecinos. Son **204 comprobaciones** y
**589 pasos**.

| Nivel de evidencia | Cuántos | Qué significa |
|---|---:|---|
| **Ejecutada** | **73** | El comando de «Compruébalo» se lanzó contra el binario instalado y devolvió lo que dice la página |
| **Documentada** | 82 | Sale de la página oficial citada. No se ha ejecutado, y la página lo dice |
| Sin respaldo | **0** | No se publica |

La distinción se declara en cada página, no se promedia. Muchas de las
documentadas dependen de un entorno que esta máquina no tiene (Bedrock, Foundry,
Team, Enterprise, macOS, móvil): ahí el comando lo puede ejecutar el lector que
sí lo tenga, y el campo «No aplica si» nombra el entorno.

Un síntoma sin entrada en `resoluciones.yaml` sale con síntoma y causa, y su
página lo dice. Hoy no hay ninguno, pero el camino sigue existiendo a propósito:
cuando un módulo añada un error típico nuevo, su página saldrá corta y honesta
hasta que alguien haga el trabajo de campo.

El generador falla si una resolución apunta a un síntoma que ya no existe, si un
«síntoma vecino» es un enlace roto, si falta cualquiera de los nueve campos o si
el nivel de evidencia no está en el vocabulario.

**Por qué existe esto.** Al corregir que MCP difiere sus esquemas de herramientas,
la corrección llegó a la referencia de una skill pero **no a su `SKILL.md`**, y las
dos frases opuestas convivieron sin que ninguna prueba fallara. El verificador de
afirmaciones comprueba que el libro dice la verdad sobre la herramienta; la fábrica
comprueba que el repositorio no se contradice a sí mismo. Son dos fallos distintos
y hacían falta dos redes.
