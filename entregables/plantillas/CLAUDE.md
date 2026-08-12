# <NOMBRE DEL PROYECTO>

<!--
  Plantilla de CLAUDE.md. Los comentarios HTML de bloque como este SE ELIMINAN
  antes de inyectar el contenido en contexto: cuestan CERO tokens. Úsalos para
  notas al que mantenga el archivo.

  REGLA DE ORO: aquí solo va lo que hace falta en TODAS las tareas del repo.
  Se paga en cada turno de cada sesión. Si en la mitad de las tareas sobra,
  va en una regla con `paths` o en una skill.

  Y RECUERDA: esto es CONTEXTO, no configuración impuesta. Lo que no puede
  dejarse al criterio del modelo va en un hook, no aquí.
-->

Qué es: <una frase. Qué hace el proyecto y para quién>

## Cómo se trabaja aquí

- Compilar: `<comando>`
- Probar: `<comando>`
- Formatear: lo hace un hook al editar, no lo pidas
- Arrancar en local: `<comando>`

## Qué manda cuando algo se contradice

<!-- Esta sección es la que más tiempo ahorra en un repo con historia -->

- La configuración efectiva es `<archivo>`. `<el otro>` está muerto.
- Ante duda entre documentación y código, **gana el código**.
- `<ruta>` es código muerto pendiente de borrar. No lo mejores.

## Convenciones

- <convención concreta, no "escribe código limpio">
- <convención concreta>

## Git

<!-- Las sesiones en segundo plano SIGUEN estas instrucciones al confirmar y
     publicar, así que esto gobierna lo que pasa cuando no estás delante. -->

- Rama por tarea, nunca directo a `main`.
- Mensajes en imperativo y en castellano.
- No hagas `push` sin que pasen las pruebas.

## Compact Instructions

<!-- Dirige qué se conserva al compactar -->

Conserva: el objetivo de la tarea, las decisiones tomadas y por qué, y los
archivos tocados. Descarta: salidas largas de comandos ya resueltos.
