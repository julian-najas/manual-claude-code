# Fuentes y atribuciones

Este documento lista de dónde sale cada cosa que no hemos escrito nosotros.
Se actualiza en cada versión del libro. Si algo falta aquí, es un fallo que hay
que reportar.

## Declaración de sala limpia

**Este manual no contiene, cita ni parafrasea system prompts filtrados**, ni
material obtenido por ingeniería inversa de los mecanismos internos de Claude
Code. Todo lo que se afirma sobre el comportamiento de la herramienta procede de
una de estas tres fuentes:

1. La documentación pública oficial.
2. La superficie observable del CLI instalado, es decir lo que el programa dice
   de sí mismo al ejecutarlo.
3. Mediciones propias sobre nuestra propia infraestructura.

Lo que no encaja en ninguna de las tres, no entra. Esa decisión nos deja fuera
material interesante, y aun así se mantiene.

## Software de terceros

| Proyecto | Licencia | Cómo se usa aquí |
|---|---|---|
| _(pendiente de completar por Escribano con el inventario definitivo)_ | MIT | Fragmentos adaptados, citados en el capítulo correspondiente |

**Regla:** cada fragmento reutilizado se marca en el punto exacto del libro
donde aparece, con el proyecto, el autor y la licencia. La atribución en el
apéndice no sustituye a la atribución en el sitio.

## Datos propios

| Dato | Origen | Periodo | Reproducible con |
|---|---|---|---|
| 4.195 llamadas a la API | Telemetría propia de una operación multiagente | 10-abr a 12-ago 2026 | `D4-factura/analizar_gasto.py` |
| Superficie del CLI (65 banderas, 13 subcomandos) | `claude --help` sobre 2.1.228 | 12-ago 2026 | `D8-boletin/detectar-roturas.py` |
| 19 afirmaciones verificadas | Ejecución real contra el CLI instalado | 12-ago 2026 | `D2-verificador/verificar.py` |

Los datos de telemetría corresponden a modelos de terceros, no a Claude Code.
Lo que transfiere es la estructura del gasto, y así se dice en el capítulo 10.

## Marcas

Claude y Claude Code son marcas de Anthropic PBC. Este manual y sus autores no
están afiliados, patrocinados ni respaldados por Anthropic. El uso del nombre es
descriptivo: el libro trata sobre esa herramienta.

## Precios y cifras de mercado

Las cifras de mercado citadas en materiales comerciales de este proyecto se
consultaron el 12 de agosto de 2026 en las páginas de origen, y llevan marcada
la diferencia entre lo leído en la ficha real y lo que solo aparecía en
resultados de buscador. Los precios cambian: la fecha de consulta va siempre
junto a la cifra.
