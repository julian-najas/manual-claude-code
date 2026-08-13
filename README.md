# Claude Code en producción

**El manual en castellano que no te pide que confíes en él: se verifica contra la
máquina.**

**Versión:** v2026.08
**Verificado contra:** Claude Code 2.1.228, el 12 de agosto de 2026
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
| **Manual guiado** · `manuscrito/` | 12 módulos con laboratorios sobre un repositorio real, el producto de 149 € | **En obra: 1 de 12 módulos** |

La guía alimenta al manual; el manual no repite la guía. **Lo terminado es la
guía.** Llamar terminado al manual sería falso.

Para instalar la guía completa como skill: `entregables/skill-guia/instalar.sh`.
La skill de `D1-skill/` es la del **manual**, que es más pequeña y aún está en obra.

---

## Qué hay aquí

| Carpeta | Qué es | Estado |
|---|---|---|
| `D1-skill/` | El **manual** empaquetado como skill. Para la **guía**, ver `entregables/skill-guia/` | Instalable, en obra |
| `D2-verificador/` | Registro de afirmaciones del libro y runner que las comprueba contra el CLI | Funciona, 21/21 |
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
   ejecuta contra el CLI instalado. Hoy son 25. **No son todas las afirmaciones
   del libro**: son las que se pueden comprobar solas y las que más daño harían
   si dejaran de ser ciertas. El resto lleva fuente, fecha y nivel de evidencia
   al pie de su módulo.
2. **Fecha de corte visible.** En la portada, no escondida en los créditos.
3. **Sin system prompts filtrados.** Sala limpia, declarada en el libro.
4. **Los euros no se inventan.** Los tokens se miden; las tarifas las pone quien
   las tiene.
5. **Si el libro y la máquina se contradicen, gana la máquina**, y eso es un
   fallo que se reporta, no que se disimula.

## Cómo se versiona

El libro se versiona como software: `v2026.08`, con changelog público y diff
entre versiones para que quien ya se lo leyó solo tenga que leer lo nuevo.
Cuatro revisiones al año, más parche cuando algo se rompa.

Cuando el verificador detecta una rotura, abre una incidencia sola. Antes de
cerrarla hay que: corregir el capítulo, subir la versión, anotar el changelog y
mandarlo al boletín.

---

## La fábrica: una fuente, muchas salidas

**`guia-21/M*.md` es la única fuente canónica de la guía.** Todo lo demás se
genera. Nunca se editan las salidas a mano.

```
guia-21/M*.md  ──┬─→ entregables/guia-claude-code-2026-08.md   (guía ensamblada)
                 ├─→ entregables/skill-guia/.../modulos/        (copias para la skill)
                 └─→ entregables/skill-guia/.../INDICE-SINTOMAS.md

fabrica/hechos.yaml ─→ comprobar-coherencia.py ─→ falla si algún .md se contradice
D2-verificador/registro.yaml ─→ verificar.py ─→ falla si el libro deja de ser cierto
```

| Comando | Qué hace |
|---|---|
| `python3 fabrica/construir.py` | Regenera todas las salidas |
| `python3 fabrica/construir.py --comprobar` | No escribe. Falla si alguna está desfasada |
| `python3 fabrica/comprobar-coherencia.py` | Falla si un archivo contradice un hecho canónico |

**Por qué existe esto.** Al corregir que MCP difiere sus esquemas de herramientas,
la corrección llegó a la referencia de una skill pero **no a su `SKILL.md`**, y las
dos frases opuestas convivieron sin que ninguna prueba fallara. El verificador de
afirmaciones comprueba que el libro dice la verdad sobre la herramienta; la fábrica
comprueba que el repositorio no se contradice a sí mismo. Son dos fallos distintos
y hacían falta dos redes.
