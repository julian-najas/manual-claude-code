# Capítulo 12 · Modo escéptico

> Este capítulo argumenta en contra de la herramienta sobre la que trata el
> resto del libro. No es un gesto de falsa modestia para parecer honestos: es
> que un manual que solo sabe decir que sí no sirve para decidir nada, y tú has
> pagado por poder decidir.

---

## 12.1 · La pregunta que casi nadie hace

La pregunta de moda es "¿cómo saco más partido a Claude Code?". La pregunta cara
es la otra: **"¿en qué parte de mi trabajo lo estoy metiendo donde no toca?"**

La respuesta honesta, después de meses midiendo, es que hay bastantes sitios. Y
que reconocerlos sale más rentable que cualquier truco de configuración.

---

## 12.2 · Las siete situaciones en las que sale peor

### 1. El cambio de una línea que ya sabes hacer

Sabes exactamente qué archivo, qué línea y qué poner. Escribirlo son quince
segundos. Pedirlo son: redactar la petición, esperar, revisar el diff, corregir
el matiz que no cogió. Y en el camino has pagado por que se leyera medio
proyecto para cambiar una línea.

**La regla:** si sabes escribir el cambio más rápido de lo que tardas en
describirlo, escríbelo.

### 2. Lo que no puedes verificar

Un agente escribe con la misma seguridad lo que sabe y lo que se inventa. Si el
resultado cae en un terreno donde no puedes juzgar si está bien (una fórmula
fiscal que no dominas, un algoritmo criptográfico, una normativa que no has
leído), no has ganado velocidad: has trasladado un riesgo que ahora no sabes
medir.

**La regla:** solo puedes delegar lo que sabrías revisar. El resto es apostar.

### 3. Decisiones de arquitectura sin restricciones escritas

Pedir "diseña la arquitectura de este sistema" produce algo razonable, genérico
y ajeno a las tres restricciones reales que tienes y que no le contaste: el
equipo que lo va a mantener, lo que ya hay en producción y lo que la empresa
sabe operar. La arquitectura es la suma de esas restricciones, y esas las tienes
tú, no el modelo.

**La regla:** las decisiones estructurales las tomas tú. El agente ejecuta y
critica, no decide.

### 4. Código que ya funciona y nadie ha pedido tocar

La tentación de "aprovechar y refactorizar esto de paso" es enorme cuando el
coste aparente de escribir código baja. Pero el coste de escribir código nunca
fue el problema: el problema es el de revisarlo, probarlo y responder de él a
las tres de la mañana. Ese no ha bajado.

**La regla:** el código que no ha cambiado en dos años y funciona es un activo,
no una deuda.

### 5. Prototipos de usar y tirar de menos de una hora

Para un guion de veinte líneas que vas a ejecutar una vez y borrar, montar el
contexto, los permisos y la revisión cuesta más que el guion. La ceremonia solo
se amortiza cuando hay algo que mantener.

**La regla:** por debajo de una hora de trabajo desechable, a mano.

### 6. Cuando el problema es que nadie sabe qué hay que hacer

Un agente amplifica la claridad que le des. Si el equipo no se ha puesto de
acuerdo en qué se está construyendo, lo que produce es la misma confusión, pero
en forma de código y a más velocidad. Ahora hay tres implementaciones distintas
del mismo malentendido.

**La regla:** primero se decide, después se automatiza. Nunca al revés.

### 7. Cuando los datos no pueden salir

Hay contratos, sectores y clientes donde el contenido de un archivo no puede
enviarse a un tercero. Eso no se arregla con una cláusula en la configuración ni
con buena voluntad. O hay una vía contractual que lo permita, o ese repositorio
queda fuera. Punto.

**La regla:** esto no lo decide el equipo técnico.

---

## 12.3 · Las cuentas que casi nadie hace

El argumento de venta es la productividad. Vale, hagamos la cuenta completa.

En la columna del ahorro va el tiempo de escribir código. En la columna del
coste va todo lo demás, y es una lista larga: preparar el contexto, redactar
peticiones útiles, revisar diffs que no escribiste, la factura de tokens, el
tiempo de configurar permisos y hooks, mantener esa configuración cuando el CLI
cambia, y las horas perdidas persiguiendo un fallo que introdujo el agente y que
no habrías escrito tú.

Nadie que venda formación mete la segunda columna. Este libro sí, y por eso el
capítulo 10 se llama "La factura".

**La conclusión medida en nuestra propia operación**: el balance sale claramente
a favor en trabajo repetitivo, con criterio de éxito objetivo y bien acotado.
Sale mucho menos claro en trabajo exploratorio, en decisiones y en todo lo que
depende de contexto que no está escrito en ningún sitio. Que es, casualmente,
donde más se promete que va a arrasar.

---

## 12.4 · Las señales de que te has pasado de rosca

- Tu configuración de agentes es más grande que la parte del proyecto que
  automatiza.
- Dedicas más tiempo a afinar prompts que el que dedicabas a escribir el código.
- Apruebas cambios que no sabrías explicar en una reunión.
- El equipo ha dejado de discutir decisiones porque "ya lo mira el agente".
- Nadie sabe cuánto se está gastando.
- Empezaste automatizando una tarea y llevas tres semanas construyendo una
  plataforma para automatizar tareas.

Si reconoces tres o más, el problema ya no es de configuración.

---

## 12.5 · Entonces, ¿cuándo sí?

Para que quede en su sitio, la otra cara, con la misma honestidad. Sale bien y
sale muy bien cuando se cumplen a la vez estas tres condiciones:

1. **Hay criterio de éxito objetivo.** Tests que pasan o fallan, un linter, un
   esquema que valida. Algo que diga PASA o FALLA sin que haya que opinar.
2. **El trabajo es tedioso y conocido.** Migraciones, cobertura de tests,
   documentación desactualizada, adaptar cien archivos al mismo patrón nuevo.
3. **El coste de equivocarse es reversible.** Rama aparte, revisión antes de
   fusionar, nada tocando producción directamente.

Cuando se cumplen las tres, la diferencia es enorme y sostenida. Cuando falta
una, entra en zona de duda. Cuando faltan dos, vuelve a leer este capítulo.

---

## 12.6 · Resumen en una tarjeta

- Solo puedes delegar lo que sabrías revisar.
- Si escribirlo es más rápido que describirlo, escríbelo.
- Las decisiones son tuyas. El agente ejecuta y critica.
- Primero se decide qué se construye, luego se automatiza.
- El código viejo que funciona es un activo.
- La cuenta de la productividad tiene dos columnas. Escribe las dos.
