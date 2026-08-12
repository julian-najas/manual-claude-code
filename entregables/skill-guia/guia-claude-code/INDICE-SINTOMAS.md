# Índice por síntoma

**156 síntomas** extraídos de las tablas de errores típicos de los 21 módulos.
Generado, no escrito a mano: si un módulo cambia su tabla, este índice se regenera.

Busca lo que te pasa, no lo que crees que es.

| Síntoma | Qué está pasando | Módulo |
|---|---|---|
| Se le olvida lo que le dije al principio | Compactó. Esa instrucción tenía que estar en `CLAUDE.md`, no en el chat | [M1](modulos/) |
| Desconecto los MCP para ahorrar contexto | Por defecto solo pesan los nombres. Mide con `/mcp` antes de amputar | [M1](modulos/) |
| Deshice con `Esc` `Esc` y la base de datos seguía modificada | Los checkpoints solo cubren archivos. Nunca sistemas remotos | [M1](modulos/) |
| Da respuestas plausibles pero incorrectas | No hay contra qué verificar. El bucle se quedó en dos fases | [M1](modulos/) |
| El resumen automático se repite sin avanzar | Un archivo o salida gigante. Es el error de *thrashing*, está documentado | [M1](modulos/) |
| A mi compañero le existe un comando que a mí no | Versiones distintas. Canal y `minimumVersion` | [M2](modulos/) |
| Pasé a `stable` y me degradó | No debería: pasar de `latest` a `stable` pregunta antes | [M2](modulos/) |
| Homebrew no me actualiza a la última | Las actualizaciones las lleva Homebrew, no Claude Code | [M2](modulos/) |
| En mi contenedor Alpine falla | Distribuciones musl tienen dependencias propias | [M2](modulos/) |
| En WSL no encuentra archivos que están ahí | Problema documentado de búsqueda en WSL | [M2](modulos/) |
| Mi script usa una clave que yo rechacé | Con `-p` la clave se usa siempre que esté presente | [M2](modulos/) |
| `claude doctor` dice instalaciones duplicadas | Restos de otra vía de instalación | [M2](modulos/) |
| El token de CI caducó de golpe | Hay aviso de renovación antes. `claude setup-token` | [M2](modulos/) |
| Mi ajuste no se aplica | Otro ámbito o una variable de entorno lo sobrescriben. `/status` primero | [M3](modulos/) |
| Mi `allow` local no sustituye al del proyecto | Los permisos se fusionan, no se sobrescriben. Es por diseño | [M3](modulos/) |
| No encuentro mis servidores MCP en settings.json | Están en `~/.claude.json`, otro archivo | [M3](modulos/) |
| Cambié la política en el servidor y no llega | Los settings cacheados persisten hasta el siguiente fetch correcto | [M3](modulos/) |
| Puse los settings de servidor y los del plist se ignoran | Correcto: dentro de managed no se fusionan, salvo `env` y las lock keys | [M3](modulos/) |
| Mi settings.json entero dejó de aplicarse | Usuario, proyecto y local son estrictos: si no valida, se rechaza completo | [M3](modulos/) |
| Pulso `f` en `/doctor` y no pasa nada | Eso era anterior a v2.1.205 | [M3](modulos/) |
| Le digo que siempre haga X y no siempre lo hace | Es contexto, no configuración. Si no es negociable, hook | [M4](modulos/) |
| Se le olvidó lo que le dije al principio | Se dio solo en conversación. Compactó y se fue | [M4](modulos/) |
| Mi regla de la API no se aplica | Tiene `paths` y aún no ha leído ningún archivo que case | [M4](modulos/) |
| El `CLAUDE.md` del subdirectorio no aparece | No carga al arrancar, entra al leer archivos de ahí | [M4](modulos/) |
| Añadí un directorio con `--add-dir` y no lee su `CLAUDE.md` | Necesitas `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` | [M4](modulos/) |
| Rechacé un diálogo de imports y ya no me lo pide | Es por diseño: quedan desactivados y no vuelve a preguntar | [M4](modulos/) |
| En el monorepo se cuela el `CLAUDE.md` de otro equipo | `claudeMdExcludes` | [M4](modulos/) |
| Claude elige una de dos reglas al azar | Se contradicen. Poda periódica | [M4](modulos/) |
| Solo hay cinco modos | Son seis. Falta `default`, que en el CLI se llama Manual | [M5](modulos/) |
| Puse `manual` y no lo reconoce | El alias requiere v2.1.200 o posterior | [M5](modulos/) |
| Mi `strictAllowlist` del repositorio no hace nada | Correcto: solo aplica desde usuario, gestionada o `--settings` | [M5](modulos/) |
| Enmascaré la credencial y la herramienta ya no autentica | Falta `network.tlsTerminate`, así el proxy no puede sustituir | [M5](modulos/) |
| En macOS el archivo enmascarado no aparece | En macOS se bloquea el archivo, no se sustituye | [M5](modulos/) |
| Le dije que limpiara el repo y no hizo force push | Correcto. Una petición general no es intención explícita | [M5](modulos/) |
| El sandbox no protege de mi servidor MCP | La herramienta Bash en sandbox solo aísla Bash. Necesitas el runtime | [M5](modulos/) |
| Detectó la inyección, ya estamos seguros | Detectar no es impedir. Eso no es un control | [M5](modulos/) |
| Hace algo razonable pero no lo que pedía | Saltó a implementar sin explorar. Modo plan | [M6](modulos/) |
| Tengo que revisarle todo | No hay comprobación que pueda ejecutar. Eres tú el bucle | [M6](modulos/) |
| Rebobiné y el archivo seguía borrado | Lo borró un comando de Bash. Eso no se registra | [M6](modulos/) |
| Rebobiné y los cambios del subagente siguen ahí | Solo se restauran los de un fork en primer plano | [M6](modulos/) |
| En el monorepo no coge mi configuración | El settings de proyecto se carga desde el directorio de arranque | [M6](modulos/) |
| Se le va el contexto en leer `dist/` | Está en `.gitignore` y ya se excluye. Lo confirmado en git necesita `deny` | [M6](modulos/) |
| Cada tarea acaba en un refactor gigante | Falta acotar el encargo en el plan | [M6](modulos/) |
| `/mi-skill` funciona pero nunca se activa sola | Frontmatter mal formado: cuerpo cargado, metadatos vacíos. `--debug` | [M7](modulos/) |
| Se activa cuando no toca | Descripción demasiado genérica. Estréchala o desactiva la invocación por modelo | [M7](modulos/) |
| Dejó de seguir el procedimiento a mitad de sesión | Compactó y esa skill se salió del presupuesto de 25.000 tokens | [M7](modulos/) |
| Me sigue pidiendo permiso pese a `allowed-tools` | Caducó con tu mensaje anterior. Reinvoca, o usa reglas `allow` | [M7](modulos/) |
| El subagente de la skill no sabe de qué hablamos | `context: fork` no comparte tu historial. Por diseño | [M7](modulos/) |
| Puse `yes` en un booleano y no funciona | Requiere v2.1.218 o posterior | [M7](modulos/) |
| Cambié el output style y sigue pidiendo permisos | Correcto. Son ejes independientes | [M7](modulos/) |
| Han desaparecido las pistas de teclado del pie | Tienes barra de estado configurada | [M7](modulos/) |
| Definí la URL en el proyecto y la cabecera en local | Los campos no se fusionan. Gana una fuente entera | [M8](modulos/) |
| Tengo el servidor dos veces y solo conecta uno | Duplicado. Los tres ámbitos casan por nombre; plugins y conectores, por endpoint | [M8](modulos/) |
| Con el gateway me como el contexto | Tool search se desactiva con `ANTHROPIC_BASE_URL` no first-party | [M8](modulos/) |
| Puse `ENABLE_TOOL_SEARCH` y sigue cargando todo | Foundry en Azure lo rechaza en servidor, o tienes las betas experimentales desactivadas | [M8](modulos/) |
| La herramienta devuelve menos de lo que debería | Límite de salida. Sube `MAX_MCP_OUTPUT_TOKENS` | [M8](modulos/) |
| `claude mcp serve` no imprime nada | Correcto. Silencio y bloqueo significan que funciona | [M8](modulos/) |
| La sesión se congela con una consulta larga | A los 2 minutos pasa a segundo plano. Requiere v2.1.212+ | [M8](modulos/) |
| Mi tarea en segundo plano desapareció | No sobrevive a salir de la sesión | [M8](modulos/) |
| Mis subagentes no se coordinan entre sí | Por diseño: solo reportan al principal. Si deben hablarse, es un equipo | [M9](modulos/) |
| `Concurrent subagent limit reached` | 20 corriendo. Sube `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` o espera | [M9](modulos/) |
| Leí que hay un tope de 200 por sesión | Se eliminó en la semana 32 | [M9](modulos/) |
| El workflow me llena el contexto | No debería: los intermedios viven en el script. Revisa qué devuelves | [M9](modulos/) |
| Dos sesiones se pisan los archivos | No están en worktrees | [M9](modulos/) |
| Mi comando se bloquea en un worktree y no entiendo por qué | Cuarta comprobación: lo que no se puede verificar, se bloquea | [M9](modulos/) |
| La otra sesión no recibe nada | Requiere v2.1.224+, macOS o Linux. Comprueba con `/list-agents` | [M9](modulos/) |
| El equipo de agentes se ha comido el presupuesto | Es el enfoque más caro: sesiones completas y longevas | [M9](modulos/) |
| Mi hook no dispara nunca | El evento no admite ese tipo de manejador. Repasa la lista de 10.2 | [M10](modulos/) |
| Mi hook async no bloquea nada | Por diseño: `decision` y `continue` no tienen efecto en async | [M10](modulos/) |
| Puse async en un hook http | Solo existe en `type: "command"` | [M10](modulos/) |
| Las sesiones van lentas desde que puse hooks | Tienes uno pesado en cadencia de cada herramienta | [M10](modulos/) |
| Mi `StopFailure` no cambia nada | Se ignoran su salida y su código de salida | [M10](modulos/) |
| Mis tareas de `/loop` desaparecieron | Son de ámbito de sesión, y caducan a los 7 días | [M10](modulos/) |
| La tarea en la nube no ve mis archivos | Corre sobre un clon nuevo, sin tu disco | [M10](modulos/) |
| Quiero sondear cada minuto en la nube | El mínimo en la nube es 1 hora. Usa escritorio o `/loop` | [M10](modulos/) |
| Mi plugin no encuentra las skills | Las metiste dentro de `.claude-plugin/`. Solo va `plugin.json` | [M11](modulos/) |
| Puse un `.mcp.json` en `~/.claude/` y no lo lee | La raíz del plugin nunca es `~/.claude/` | [M11](modulos/) |
| Mi ruta relativa no resuelve | Debe empezar por `./` y se resuelve contra la raíz del catálogo | [M11](modulos/) |
| Quise anclar el catálogo a un commit y no me deja | Las fuentes de catálogo admiten `ref`, no `sha`. El anclaje fino va en el plugin | [M11](modulos/) |
| Una actualización de otro equipo me rompió el plugin | Falta restricción de versión en la dependencia | [M11](modulos/) |
| En las máquinas de mi equipo no hay git | Fuente `archive`: zip por HTTPS, v2.1.224+ | [M11](modulos/) |
| Nadie usa el plugin interno | Bloque `relevance` en el catálogo, o hints desde tu propio CLI | [M11](modulos/) |
| Desde el móvil no veo mis archivos | El móvil es un cliente. Depende de dónde corra la sesión | [M12](modulos/) |
| Busco la app de Claude Code y no existe | No hay app separada: pestaña **Code** de la app de Claude | [M12](modulos/) |
| Computer use no me aparece | Research preview, macOS, solo Pro y Max, y no con `-p` | [M12](modulos/) |
| Remote Control no conecta en la empresa | Apagado por defecto en Team y Enterprise | [M12](modulos/) |
| Puse la conexión automática en el repo y no funciona | Desde la w32, el repositorio solo puede desactivarla | [M12](modulos/) |
| Activamos ZDR y desapareció la web | Se desactiva automáticamente | [M12](modulos/) |
| Nuestro Slack va a dejar de funcionar | Retirada en Team y Enterprise en favor de Claude Tag | [M12](modulos/) |
| Claude entró en un panel donde yo estaba logueado | Comparte el estado de sesión del navegador. Por diseño | [M12](modulos/) |
| La revisión no aplica nuestras reglas | Falta `REVIEW.md`, o pusiste un `@import` que no se expande | [M13](modulos/) |
| La primera revisión del legacy es un muro | Para eso está 🟣 Pre-existing. Calibra con `REVIEW.md` | [M13](modulos/) |
| Corre pero no veo nada | Modo automatización: el resultado va al registro, no a un comentario | [M13](modulos/) |
| A un compañero le falla siempre el disparo | No tiene acceso de escritura. `allowed_non_write_users` | [M13](modulos/) |
| Nuestro bot no puede dispararla | Se rechazan los bots salvo los de `allowed_bots` | [M13](modulos/) |
| Factura de ultrareview disparada | Lo estáis lanzando en cada push. Es para antes de fusionar | [M13](modulos/) |
| Seguridad nos ha parado la instalación | Explica antes que el permiso de la app es un superconjunto | [M13](modulos/) |
| Nos fuimos a Bedrock y perdimos la revisión de código | Requiere suscripción. Estaba en la lista del 14.1 | [M14](modulos/) |
| No me funcionan los server-managed settings | No están en Bedrock, y requieren Team o Enterprise | [M14](modulos/) |
| Con el gateway se nos come el contexto | No reenvía `tool_reference`. Mira `GET /protocol` | [M14](modulos/) |
| Pedimos ZDR y no aparece | Solo Enterprise | [M14](modulos/) |
| Nuestro lanzador no envuelve el servicio en segundo plano | Envuelve el `claude` del `PATH`. Usa `CLAUDE_CODE_PROCESS_WRAPPER` | [M14](modulos/) |
| Puse la variable del lanzador y no hace nada | Requiere v2.1.208+. Antes se ignora en silencio | [M14](modulos/) |
| Los settings del plist se ignoran | Los de servidor entregaron claves. Dentro de managed no se fusionan | [M14](modulos/) |
| Auto mode no va en Bedrock | Soporte parcial: solo Sonnet 5, Opus 4.7+ y Fable 5 | [M14](modulos/) |
| A mi compañero le sale otro modelo con `default` | Depende del tipo de cuenta, y cambió en v2.1.219 | [M15](modulos/) |
| Puse `xhigh` y corre como `high` | El modelo no admite ese nivel. Baja al más alto admitido | [M15](modulos/) |
| Estrené modelo y se me cambió el esfuerzo | Fable 5, Opus 4.8 y 4.7 imponen su defecto hasta que elijas | [M15](modulos/) |
| Activé fast mode para ahorrar | Fast mode **sube** el coste. Lo que baja coste es menos esfuerzo | [M15](modulos/) |
| La caché no me aprovecha nada | Repasa la columna izquierda de la tabla 10 | [M15](modulos/) |
| El primer turno tras el café va lentísimo | Caducó la caché por inactividad. Es lo esperado | [M15](modulos/) |
| Mis subagentes no aprovechan la caché | Empiezan de cero y usan TTL de 5 minutos. Un fork sí hereda | [M15](modulos/) |
| Cambié de modelo para ahorrar y gasto igual | El coste lo decide el contexto, no la tarifa | [M15](modulos/) |
| No entrenan con nuestro código | Cierto en comercial. **Falso en Free, Pro y Max con el ajuste activado** | [M16](modulos/) |
| Tenemos ZDR, estamos cubiertos | No cubre analítica, gestión de plazas ni integraciones de terceros | [M16](modulos/) |
| Activamos ZDR y desapareció Claude Code en la web | Se desactiva automáticamente, junto con sesiones cloud y Artifacts | [M16](modulos/) |
| Usamos Bedrock, no sale nada a Anthropic | El chequeo de dominio de `WebFetch` sale igual | [M16](modulos/) |
| Desactivé el tráfico no esencial y `WebFetch` sigue llamando | Ese chequeo no se ve afectado por esa variable | [M16](modulos/) |
| `WebFetch` falla en toda la red corporativa | Bloqueáis `api.anthropic.com`. Permitidlo o `skipWebFetchPreflight` | [M16](modulos/) |
| Los MCP están dentro de nuestro perímetro | No, y además no los cubre ZDR. Inventaríalos | [M16](modulos/) |
| No puedo interrumpir al agente | Estás en mensaje único. El streaming es el modo recomendado | [M17](modulos/) |
| Una réplica no reanuda la sesión de otra | Transcripciones en disco local. Necesitas `SessionStore` | [M17](modulos/) |
| A veces devuelve un error en vez de mi JSON | Falló la validación tras los reintentos. Es una rama esperada | [M17](modulos/) |
| Mi coste no cuadra con la factura | El campo del SDK es una estimación con tabla congelada | [M17](modulos/) |
| `unstable_v2_createSession` ya no existe | Eliminado en TypeScript SDK 0.3.142. Migra a `query()` | [M17](modulos/) |
| El agente de un cliente vio datos de otro | Eso no lo arreglan los permisos: es aislamiento | [M17](modulos/) |
| Nuestro DPO pregunta dónde están las conversaciones | Por defecto en disco local. `SessionStore` a vuestro almacén | [M17](modulos/) |
| Relanzar el comando esperando que funcione | Ya reintentó hasta diez veces. Lee el mensaje | [M18](modulos/) |
| Buscar en Google la paráfrasis del error | El catálogo está indexado por **mensaje literal** | [M18](modulos/) |
| Culpar a la red de un `403 host_not_allowed` | Es la política del entorno cloud, no tu red | [M18](modulos/) |
| Tocar la configuración a ciegas | Modo mínimo primero, para saber de quién es el problema | [M18](modulos/) |
| Comparar dos máquinas sin mirar versiones | Media docena de comportamientos cambian por versión | [M18](modulos/) |
| Dar por hecho que un `allow` de proyecto se aplica | Necesita confianza del espacio de trabajo | [M18](modulos/) |
| Suponer que `MEMORY.md` entero se carga | 200 líneas o 25 KB, lo que llegue antes | [M18](modulos/) |
| `WebFetch` dice que la página no menciona eso | Puede ser que **tu prompt no preguntara**. Es lossy. Usa `curl` para la página cruda | [M19](modulos/) |
| Mi patrón de Grep no encuentra nada | Sintaxis de ripgrep, no de grep POSIX. Escapa los metacaracteres | [M19](modulos/) |
| El `cd` no se mantiene entre comandos | Salió del proyecto y se reseteó. Mira si el resultado dice `Shell cwd was reset to` | [M19](modulos/) |
| Un subagente no hereda mi directorio de trabajo | Nunca lo hace. Por diseño | [M19](modulos/) |
| Busqué la bandera en la referencia y no está | Puede estar en el binario y no en `cli-reference.md`. `claude --help` manda | [M19](modulos/) |
| Cambié el ajuste en los cuatro ámbitos y sigue igual | Una variable de entorno es **otra capa** por encima | [M19](modulos/) |
| Puse `allowed_domains` y `blocked_domains` a la vez | No se pueden combinar en la misma llamada | [M19](modulos/) |
| Mi `MEMORY.md` largo no se carga entero | 200 líneas o 25 KB, lo que llegue antes | [M19](modulos/) |
| En el monorepo se cuela el contexto de otros equipos | Falta `claudeMdExcludes` y capas por directorio | [M20](modulos/) |
| Cada tarea del legacy acaba en refactor gigante | Falta acotar en el plan, y tests de caracterización | [M20](modulos/) |
| El nuevo no tiene la misma configuración | No está en git, o no ha aceptado la confianza | [M20](modulos/) |
| La factura de revisión se disparó | Ultrareview en cada push. Sin ejecuciones gratis en Team | [M20](modulos/) |
| La puerta de calidad nunca veta | O el trabajo es trivial, o no comprueba nada | [M20](modulos/) |
| El trabajo nocturno tocó la rama principal | Falta `--worktree` | [M20](modulos/) |
| Mi plugin no le funciona a nadie más | Estructura mal: solo `plugin.json` en `.claude-plugin/` | [M20](modulos/) |
| El tutorial dice `/ultraplan` y no existe | Retirado en la semana 32 | [M21](modulos/) |
| Mi subagente no bloquea como esperaba | Segundo plano por defecto desde la semana 27 | [M21](modulos/) |
| De pronto ya no me pregunta por los permisos | Auto mode pasó a ser el modo por defecto | [M21](modulos/) |
| Mi script del SDK dejó de compilar | API de sesiones V2 eliminada en 0.3.142 | [M21](modulos/) |
| Pulso `f` en `/doctor` y no pasa nada | Cambió en v2.1.205 | [M21](modulos/) |
| Mi `pkill` ya no funciona | Se rechaza si casa con el proceso. Solo en Linux | [M21](modulos/) |
| Comparo dos máquinas y dan resultados distintos | Versiones distintas. Media docena de comportamientos cambian | [M21](modulos/) |

---

Regenerar: `python3 generar-indice.py`