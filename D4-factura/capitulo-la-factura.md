# Capítulo 10 · La factura

> **Fecha de corte:** 12 de agosto de 2026.
> **Datos:** 4.195 llamadas reales a la API entre el 10 de abril y el 12 de agosto de 2026,
> repartidas en 111 sesiones de una operación multiagente en producción.
> **Cómo reproducirlo:** `python3 analizar_gasto.py ~/.hermes/logs/usage_*.jsonl`

Casi todo lo que vas a leer sobre el coste de los agentes de codificación viene
de una de estas dos fuentes: la lista de precios del fabricante, o la sensación
de alguien que se llevó un susto. La lista de precios no te dice cuánto vas a
gastar, y la sensación no se puede auditar.

Este capítulo no es ninguna de las dos. Es la telemetría de cuatro meses de una
operación real, con los números que salieron, incluidos los que preferiríamos no
publicar.

---

## 10.1 · El número que lo explica casi todo

Por cada token que **sale** del modelo, entran **24**.

| | Tokens |
|---|---:|
| Entrada | 60.635.400 |
| Salida | 2.579.138 |
| Caché leída | 594.025.760 |

Léelo otra vez fijándote en la tercera fila. La caché leída, 594 millones de
tokens, es **casi diez veces** toda la entrada nueva del periodo. No es un error
de medición: es lo que pasa cuando una sesión larga vuelve a pasar por delante
del modelo el mismo contexto una y otra vez, turno tras turno.

De aquí salen las tres leyes de la factura:

1. **Pagas por leer, no por escribir.** Tu intuición dice que el gasto está en
   lo que el modelo produce. El gasto está en lo que el modelo tiene que mirar
   antes de producir nada.
2. **La conversación larga es el gasto.** Cada turno arrastra todos los
   anteriores. Una sesión de tres horas no cuesta tres veces una de una hora.
3. **La caché no es un detalle de implementación, es la mitad de tu recibo.**
   Entenderla es la diferencia entre una factura y un sobresalto.

---

## 10.2 · El coste de la cortesía

Aislemos las llamadas cuya respuesta cabe en un tuit: 50 tokens o menos. Un
"vale". Un "hecho". Un "de acuerdo, sigo".

| | |
|---|---:|
| Llamadas de respuesta corta | 168 |
| Porcentaje del total de llamadas | 4,0 % |
| Tokens de entrada que consumieron | 1.325.628 |
| Tokens de salida que produjeron | 5.700 |

Divide: **cada "vale" costó 7.891 tokens de entrada para producir 34 de salida.**
Una relación de 232 a 1.

Ese es el precio de la cortesía cuando el interlocutor tiene que releerse el
proyecto entero antes de contestar que sí. En cuatro meses, el 4 % de las
llamadas se llevó el 2,2 % de toda la entrada nueva sin aportar una sola línea
de trabajo.

No es una anécdota graciosa. Es el síntoma de un patrón caro: **turnos que no
producen artefactos**. Confirmaciones, aclaraciones, "¿seguro?", "sí, sigue".
Cada uno arrastra el contexto completo.

**Qué hacer con esto**, en orden de rentabilidad:

- Que la instrucción inicial no necesite confirmación. Una orden bien escrita
  con sus criterios de aceptación ahorra tres turnos de ida y vuelta.
- Que los permisos estén decididos de antemano en `settings.json` y no en
  mitad del trabajo, turno a turno. Cada pregunta de permisos es un turno.
- Que el trabajo largo salga de la sesión interactiva y se vaya a modo no
  interactivo o a segundo plano, donde no hay cortesía que pagar.

---

## 10.3 · Dónde se fue de verdad

| Modelo | Llamadas | Entrada | Salida |
|---|---:|---:|---:|
| gpt-5.6-sol | 1.678 | 15.407.956 | 834.706 |
| deepseek-v4-pro | 891 | 30.434.289 | 538.282 |
| deepseek-v4-flash | 633 | 4.327.384 | 645.531 |
| gpt-5.5 | 363 | 4.383.065 | 217.348 |
| glm-5.2 | 358 | 3.563.219 | 200.326 |
| gpt-5.4-mini | 162 | 886.974 | 99.949 |
| kimi-k3 | 75 | 790.112 | 19.712 |

Mira las dos primeras filas juntas y verás la trampa que más dinero cuesta:

**deepseek-v4-pro hizo la mitad de llamadas que gpt-5.6-sol y consumió el doble
de tokens de entrada.** 891 llamadas contra 1.678, pero 30,4 millones de tokens
contra 15,4. Es decir, 34.157 tokens de entrada por llamada frente a 9.183.

El modelo no era más caro por unidad. Se le estaba dando **casi cuatro veces más
contexto en cada llamada**. El coste no lo decidió la lista de precios, lo
decidió quien preparó el contexto.

> **La regla:** antes de cambiar de modelo para ahorrar, mide cuánto contexto
> le estás metiendo. Casi siempre el ahorro grande está en el contexto, no en
> la tarifa.

---

## 10.4 · Lo que este capítulo no te puede decir

Aquí es donde la mayoría de los libros seguirían inventando. Nosotros paramos.

**No hay euros en las tablas de arriba.** Los tokens están medidos uno a uno;
los euros dependen de la tarifa de cada modelo en cada fecha, y publicar una
cifra en euros sin la tabla de precios exacta sería exactamente el tipo de dato
que este libro se compromete a no fabricar. El script acepta `--precios` con tu
propia tabla y hace la conversión con tus tarifas reales, que son las únicas que
importan para tu factura.

**Estos números no son de Claude Code.** Son de una operación multiagente que
corre sobre otros modelos. Lo que transfiere a Claude Code es la **estructura**
del gasto, que es idéntica porque el mecanismo es el mismo: contexto que se
relee, turnos que no producen, caché que decide la mitad del recibo. Las
proporciones de tu instalación las tienes que medir tú, y el capítulo 10.5 dice
exactamente cómo.

**Una base de datos vacía no es un dato.** Durante meses este proyecto tuvo un
`costs.db` que todo el mundo daba por bueno. Tenía cero filas. Los datos reales
estaban en unos JSONL que nadie miraba. Antes de fiarte de tu propio panel,
cuenta las filas.

---

## 10.5 · Mide el tuyo

Laboratorio del capítulo. Coste estimado: menos de 0,10 € y diez minutos.

1. Localiza tus propios registros de uso.
2. Pásales `analizar_gasto.py`.
3. Anota tres números: la relación entrada/salida, el porcentaje de llamadas
   con respuesta corta y la caché leída frente a la entrada nueva.
4. Repite la medición dentro de un mes, después de aplicar los capítulos 3 y 4.

**PASA** si la relación entrada/salida baja, o si el porcentaje de llamadas de
respuesta corta baja. **FALLA** si sube alguna de las dos: significa que has
añadido contexto o ceremonia sin añadir trabajo.

---

## 10.6 · Resumen en una tarjeta

- Pagas por lo que el modelo lee, no por lo que escribe. Relación medida: 24 a 1.
- La caché leída fue casi 10 veces la entrada nueva. Ahí está media factura.
- Cada confirmación de una palabra costó 7.891 tokens de entrada.
- El modelo caro casi nunca es el problema. El contexto gordo casi siempre sí.
- Si tu panel de costes está vacío, tu panel de costes no existe.
