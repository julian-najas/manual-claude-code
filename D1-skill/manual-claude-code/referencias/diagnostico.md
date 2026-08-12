# Diagnóstico

Índice por síntoma. Busca lo que te pasa, no lo que crees que es.

| Síntoma | Causa más probable | Qué hacer |
|---|---|---|
| "A veces lo hace y a veces no" | es una instrucción, y las instrucciones se interpretan | conviértelo en hook |
| La sesión se queda sin contexto pronto | CLAUDE.md enorme o varios MCP conectados | mide ambos, quita lo que no se use |
| La skill no se activa sola | la descripción no dispara | reescríbela con las palabras de la petición real |
| El subagente devuelve algo inservible | no comparte tu contexto | pásale explícitamente lo que necesite |
| Cambió de comportamiento de un día para otro | el CLI se actualizó | `claude --version` y compara con la versión verificada del manual |
| Funciona en tu máquina y en la del compañero no | configuración suelta sin empaquetar | plugin, y versiónalo en el repositorio |
| Toca archivos que no debería | permisos demasiado amplios | configuración de permisos versionada en el repositorio |
| Gasta mucho más de lo esperado | turnos improductivos y contexto grande | mide relación entrada/salida y respuestas cortas |
| Propone dependencias que no existen | alucinación de paquetes | comprobación obligatoria antes de instalar nada |
| No encuentra archivos que están ahí | están fuera de los directorios permitidos | `--add-dir` |

## Antes de abrir una incidencia

1. `claude --version` y anótala.
2. Arranca en modo mínimo para descartar que sea tu propia configuración: sin
   CLAUDE.md, sin hooks y sin plugins.
3. Si en modo mínimo no pasa, el problema es tuyo y está en una de esas tres
   piezas. Si sigue pasando, es del CLI y merece la pena reportarlo.

Ese orden ahorra la mayoría de las horas que se pierden en estos fallos.
