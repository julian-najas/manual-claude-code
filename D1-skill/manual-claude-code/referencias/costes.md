# Costes y contexto

Números medidos en una operación multiagente real, 4.195 llamadas entre el
10-abr y el 12-ago de 2026. Reproducible con `D4-factura/analizar_gasto.py`.

## Las tres leyes

1. **Pagas por leer, no por escribir.** Medido: 24 tokens de entrada por cada
   token de salida (60.635.400 de entrada frente a 2.579.138 de salida).
2. **La conversación larga es el gasto.** La caché leída fue 594.025.760
   tokens, casi diez veces toda la entrada nueva. Es el mismo contexto pasando
   una y otra vez por delante del modelo.
3. **El modelo caro casi nunca es el problema.** En los datos, un modelo hizo la
   mitad de llamadas que otro y consumió el doble de entrada: 34.157 tokens por
   llamada frente a 9.183. Lo decidió el contexto, no la tarifa.

## El coste de la cortesía

168 llamadas (el 4,0 % del total) tuvieron respuestas de 50 tokens o menos.
Consumieron 1.325.628 tokens de entrada para producir 5.700 de salida.

**Cada "vale" costó 7.891 tokens de entrada para devolver 34.** Relación 232:1.

Qué hacer, por orden de rentabilidad:
- Instrucciones iniciales con criterios de aceptación, para no gastar tres
  turnos en aclarar lo que cabía en el primero.
- Permisos decididos de antemano en la configuración, no turno a turno. Cada
  pregunta de permisos es un turno completo.
- El trabajo largo, fuera de la sesión interactiva: modo no interactivo o
  segundo plano, donde no hay cortesía que pagar.

## Antes de fiarte de tu panel

Este proyecto tuvo durante meses una base de datos de costes que todo el mundo
daba por buena. Tenía cero filas. Los datos reales estaban en unos registros
JSONL que nadie miraba. **Cuenta las filas antes de citar el panel.**

## Qué medir cada mes

- Relación entrada/salida.
- Porcentaje de llamadas con respuesta corta.
- Caché leída frente a entrada nueva.

Si sube alguna de las dos primeras, has añadido contexto o ceremonia sin añadir
trabajo.
