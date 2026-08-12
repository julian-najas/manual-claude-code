# Claude Code en producción

Repositorio companion del manual profesional en castellano.

**Versión:** v2026.08
**Verificado contra:** Claude Code 2.1.228, el 12 de agosto de 2026
**Estado de verificación:** [`D2-verificador/ESTADO.md`](D2-verificador/ESTADO.md)

Este repositorio no está afiliado, patrocinado ni respaldado por Anthropic.

---

## Qué hay aquí

| Carpeta | Qué es | Estado |
|---|---|---|
| `D1-skill/` | El manual empaquetado como skill, consultable desde dentro de Claude Code | Instalable |
| `D2-verificador/` | Registro de afirmaciones del libro y runner que las comprueba contra el CLI | Funciona, 19/19 |
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

1. **Ninguna afirmación entra en el libro sin estar en `registro.yaml`.** Si no
   se puede comprobar, no se publica.
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
