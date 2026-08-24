# Estado del manuscrito

Una entrada por iteración. Dos líneas: qué se cerró y qué queda.

## Cómo se escribe esto ahora · desde el 17-ago-2026

El manuscrito lo escribe una **rutina en la nube**, no el R630. Un módulo al día
a las 08:00 de Madrid (06:00 UTC), modelo Opus 5, sobre este mismo repositorio
clonado desde GitHub.

- Rutina: `trig_01RzL9eHhTvWuejJYqBLgV7Z`
- Panel: https://claude.ai/code/routines/trig_01RzL9eHhTvWuejJYqBLgV7Z
- Para pararla o cambiarla, ahí. No se borra por API.

**Lo que hay que saber para no romperlo:**

1. **El agente clona de GitHub, no ve el R630.** Si trabajas en local, empuja.
   Lo que no esté en `origin/main` no existe para la rutina.
2. **La rutina empuja a `main` cada día.** Si tienes trabajo local sin subir
   cuando termine, te va a tocar rebase.
3. **Guarda de seguridad:** si el agente no encuentra
   `manuscrito/modulo-02-instalacion.md`, para y no escribe nada, en vez de
   escribir un módulo duplicado. Es la red contra un repositorio desincronizado.
4. **08:00 y no 07:00 a propósito:** el flujo `verificar.yml` corre a las 05:00
   UTC, que son las 07:00 de Madrid. Ponerlos a la misma hora hacía que los dos
   empujaran a `main` a la vez.
6. **Una sesión que se muere no deja rastro, y por eso hay un latido.**
   `.github/workflows/latido-rutina.yml` corre a las 21:00 UTC y comprueba que
   el diario tiene entrada de hoy. Si no la tiene, abre incidencia con la
   etiqueta `rutina-callada` y no abre una nueva cada día: comenta en la que ya
   está. Se prueba a mano con `python3 fabrica/latido-rutina.py`.

5. **Nadie contesta a un diálogo de permisos.** La sesión se congela hasta que
   caduca y el día se pierde sin dejar nada escrito. Lo dispara copiar un
   archivo desde `/tmp` hacia dentro del repositorio; escribirlo con un heredoc
   no lo dispara. Está en el paso 0d de la rutina desde el 19-ago-2026.

## 2026-08-24 (tarde) · Los tres días en blanco, y el latido que los habría cazado

Al contar el ritmo real salió esto: **del 21 al 23 de agosto no hay una sola
entrada en este diario**. Lo único que hay en esos días son los commits
automáticos del verificador de las 05:20 UTC. La rutina dispara a las 06:00 y no
dejó nada, tres días seguidos, y no se detectó hasta hoy.

**El ritmo real, entonces, no es un módulo al día.** Son cuatro módulos en ocho
días naturales, del 17 al 24: uno cada dos. La cuenta de "siete módulos, ocho
días" era teórica; con lo observado son unas dos semanas.

**La causa no se puede saber desde aquí, y ese es exactamente el problema.** Una
sesión que se cuelga en un diálogo de permisos o que se corta por límite de uso
deja el repositorio idéntico a como quedaría si la rutina no hubiera disparado
nunca. El 19 y el 20 fallaron y quedaron escritos porque alguien lo escribió
después; del 21 al 23 no hay ni eso.

**Arreglo: `.github/workflows/latido-rutina.yml`.** Corre a las 21:00 UTC, quince
horas después de la rutina, cuando el día ya está decidido. Comprueba que el
diario tiene una entrada con la fecha de hoy y, si no la tiene, abre incidencia
con la etiqueta `rutina-callada`. Mientras el silencio dure comenta en la
incidencia abierta en vez de abrir una nueva cada día: una alarma que se repite
sola se acaba ignorando, que es como se perdieron estos tres días.

La lógica vive en `fabrica/latido-rutina.py`, fuera del YAML, para poder
probarla: `python3 fabrica/latido-rutina.py` dice si la rutina está viva, y
`--tolerancia N` afloja el umbral. Probado por los dos lados: contra el diario de
hoy da viva; contra el diario del 23 (quitando la entrada de hoy) da **5 días
callada** y sale con código 1.

**Lo que este latido NO hace, a propósito.** No entra en `registro.yaml` ni en
`verificar.yml`. El verificador dice si el libro sigue siendo cierto; esto dice
si la fábrica sigue viva. Mezclarlos haría que "0 fallan" significara dos cosas
distintas, y que un silencio de la rutina abriera una incidencia titulada
"Rotura con 2.1.24x", que es mentira.

### PARA JULIÁN

1. **El latido detecta el silencio, no lo evita.** Lo que lo evitaría de verdad
   es que la rutina anote en el diario **al empezar**, no solo al terminar: una
   línea después del paso 0c diciendo "arranco, toca el módulo NN". Entonces un
   día en blanco distinguiría "no disparó" de "disparó y murió", que hoy no se
   distingue. No lo he hecho porque el texto de la rutina vive en el panel, no
   en el repositorio, y eso lo tienes que pegar tú.
2. **Los tres días perdidos siguen sin causa.** En el panel de la rutina se ve
   si esas sesiones dispararon y en qué estado quedaron. Si alguna quedó en
   `requires_action`, es otra vez el diálogo de permisos y hay que mirar qué lo
   disparó para añadirlo al paso 0d.

## 2026-08-24 · Módulo 05 · Hooks · PUBLICADO

Cerrado `manuscrito/modulo-05-hooks.md`, **3.997 palabras**, las seis partes del
esqueleto y runbook de una página. Verificador contra la **2.1.241**: **54
pasan, 0 fallan, 18 a revisar, 3 omitidas**. Coherencia y `construir.py
--comprobar`, las dos en verde. Quedan siete módulos: 06 a 12.

**El paso 0d volvió a funcionar.** Cero llamadas colgadas. Los hooks del
laboratorio viven en `D6-repo-feo/gestor-pedidos/hooks/`, fuera de `.claude/`, y
los dos archivos que sí están dentro de una carpeta `.claude/`
(`gestor-pedidos/.claude/settings.json` y la sonda de esquema) se escribieron
enteros con heredoc. Nada entró al repositorio por `cp` desde `/tmp`. Y el sitio
de los scripts dejó de ser una precaución para convertirse en contenido: la
sección 5.3.1 explica por qué separar el código del hook de la configuración que
lo declara es además mejor práctica.

**Registro:** catorce entradas nuevas, `HOK-002` a `HOK-015`. Nueve se comprueban
solas y son de un tipo que no había: **corren los hooks del laboratorio en seco**,
con las fixtures de `hooks/ejemplos/`, comprobando que un hook devuelve `deny`
cuando toca y no imprime nada cuando no toca. Es la técnica de depuración de
5.3.3 convertida en prueba permanente, y no gasta un token. Las cinco amarillas
son las cinco mediciones con coste.

**Mediciones propias, 2.1.241.** Mismo repo, misma petición, variando una sola
cosa:

| Medida | Resultado |
|---|---|
| Credencial escrita, solo `CLAUDE.md` y regla de rutas | **5 de 7** |
| La misma, con el hook que mira contenido | **0 de 7** |
| `allow` y hook en el mismo archivo, sin confianza | `allow` ignorado, **hook ejecutado** |
| Secreto por la herramienta `Read`, con el hook | bloqueado 2 de 2, 91.054 tokens |
| El mismo secreto por `@ruta` | **clave impresa 2 de 2**, 45.530 tokens |
| El mismo `@ruta` con la regla `deny` del 04 | bloqueado 2 de 2 |
| Seis hooks declarados frente a ninguno | 45.381 tokens las cuatro veces |
| Formateo al editar, sin hook y con hook | 0 de 3 frente a 3 de 3 |
| Llamadas a herramienta del mismo turno | 2 frente a 6 |

**Hallazgos propios del módulo:**

- **La medida madre es el 5 de 7.** El síntoma del módulo ("unas veces lo hace y
  otras no") deja de ser una queja y pasa a ser un número. Y las dos veces que
  el agente NO escribió la credencial, se negó por criterio propio y lo explicó
  muy bien, que es exactamente lo que hace que la gente crea que tiene un límite
  donde solo tiene una coincidencia.
- **La asimetría del módulo 04 gira, y gira del lado malo.** Un `allow` de un
  repositorio clonado se ignora sin confianza; un **hook** del mismo archivo se
  ejecuta. Medido en una sola ejecución, con las dos cosas en el mismo
  `settings.json`: el CLI escribió el aviso de "workspace has not been trusted"
  por la salida de error mientras el script del hook ya había corrido. Es hecho
  canónico nuevo, `HOOKS-CORREN-SIN-CONFIANZA`.
- **El agujero del hook es `@`, y es el camino barato.** `PreToolUse` solo corre
  cuando hay llamada a herramienta, y un archivo metido en el prompt con `@` no
  la tiene. Se lleva la clave entera en 1 turno y 45.530 tokens, frente a los 2
  turnos y 91.054 del camino bloqueado. Nadie lo va a notar por la factura. La
  regla `deny` del módulo 04 sí lo cubre, así que la tesis de los dos módulos
  juntos es que **no son alternativas**: cada uno tapa el agujero del otro. Está
  en la tabla de coberturas de 5.2.7, que es el mejor activo del módulo.
- **Declarar cuesta cero; disparar, no.** 45.381 tokens con seis hooks y sin
  ninguno, al token, igual que las reglas del 04. Pero el hook de formato lleva
  el turno de 2 llamadas a herramienta a 6 y de ~167.000 a ~260.000 tokens,
  porque `black` reescribe el archivo y el agente vuelve a leerlo. **El hook que
  impide es barato; el que arregla, no.** Eso no está en ninguna documentación.
- **Un no medido que también vale.** El agujero de `python3` del módulo 04 no se
  reprodujo: el agente se negó por su cuenta las dos veces, en las dos
  configuraciones, sin llegar a llamar a Bash. No se publica ni como "sigue
  abierto" ni como "está cerrado", porque una negativa del modelo no es un
  límite del sistema. Es la misma lección que el 5 de 7, por el otro lado.

**Sonda de esquema ampliada:** `D2-verificador/sonda-esquema` gana un bloque
`hooks` y un `disableAllHooks` inválidos a propósito. `claude doctor` ahí
enumera `hooks.PreToolUse`, `hooks.PostCompact`, `hooks.TeammateIdle` y
`disableAllHooks`, y eso sostiene `HOK-009` sin gastar nada.

**Laboratorio:** `D6-repo-feo/gestor-pedidos` gana `hooks/` con los tres scripts
(`veto-secretos.sh`, `veto-credenciales.sh`, `formatear.sh`), `hooks/ejemplos/`
con las cinco fixtures de prueba en seco, `HOOKS.md` con lo que impide y lo que
NO impide cada uno, y el bloque `hooks` en `.claude/settings.json`. **Ningún
fallo sembrado se ha tocado**: `app.py` quedó restaurado con `DEBUG = True` y sin
formatear después de las mediciones.

**Activos:** `entregables/plantillas/hooks/` pasa de 4 scripts a 7 y deja de
tener referencias rotas (`veto-secretos.sh` y `veto-rm.sh` estaban declarados en
`hooks.json` y no existían). El `hooks.json` de la biblioteca pasa a apuntar a
`${CLAUDE_PROJECT_DIR}/hooks/` en vez de a `.claude/hooks/`, y todos sus
manejadores llevan ya `args: []`, la forma de ejecutable que la documentación
recomienda para cualquier hook con marcador de ruta.

**Bookkeeping:** `fabrica/hechos.yaml` y `README.md` pasan de "4 de 12" a "5 de
12". Hecho canónico nuevo, `HOOKS-CORREN-SIN-CONFIANZA`.

### PARA JULIÁN

1. **La fecha de corte del libro ya está decidida de facto, quinta vez que se
   anota.** El 05 se ha escrito contra la **2.1.241** y lo declara en cabecera,
   como el 02 (2.1.233), el 03 (2.1.234) y el 04 (2.1.235). Son cuatro módulos
   con versión propia y ninguna reescritura. La regla 8 del esqueleto ya lo dice
   por escrito desde el 19-ago; lo único que falta es que lo confirmes para
   poder cerrar el 01, que sigue sin declarar versión.
2. **El inventario del repo feo sigue sin actualizar, cuarto módulo que lo
   dice.** El módulo 05 añade al laboratorio `hooks/`, `hooks/ejemplos/` y
   `HOOKS.md`. La tabla del recorrido de `guion-de-doma.md` no lo refleja, y no
   la he tocado porque es material compartido por los doce módulos.
3. **Decisión nueva, y es tuya: la biblioteca de hooks son 7, no 10.** El
   esqueleto promete "los diez hooks de la biblioteca" como activo del módulo
   05. Hay siete, todos usados o citados por el libro. No he inventado tres para
   cuadrar el número. O bajas la promesa del esqueleto a siete, o dices cuáles
   son los tres que faltan y en qué módulo se ganan. Mi recomendación: bajarla a
   siete y dejar que la biblioteca crezca donde el libro la necesite, que es
   como han crecido las plantillas de permisos.
4. **Sigue abierto lo del módulo 04:** la clave de `app.py` se **acota** en el 04
   y en el 05, y se **elimina** en el 12. El módulo 05 vuelve a escribirlo así,
   explícitamente, en su sección de coste. El `guion-de-doma.md` sigue diciendo
   "04 y 10" para el fallo 1. Es una línea de la tabla.

## 2026-08-19 (tarde) · Módulo 04 · Permisos y sandbox · PUBLICADO

Cerrado `manuscrito/modulo-04-permisos-y-sandbox.md`, **3.996 palabras**, las
seis partes del esqueleto y runbook de una página. Verificador contra la
**2.1.235**: **45 pasan, 0 fallan, 13 a revisar, 3 omitidas**. Coherencia y
`construir.py --comprobar`, las dos en verde. Quedan ocho módulos: 05 a 12.

**El paso 0d funcionó.** Cero llamadas colgadas: todo lo que entró al
repositorio se escribió con heredoc, los archivos de medición se quedaron en
`/tmp`, y el `settings.json` del laboratorio se restauró escribiéndolo, no
copiándolo. La sesión de la mañana murió en un `cp`; esta no ha tenido ninguno.

**Registro:** trece entradas nuevas, `PRM-004` a `PRM-016`. Nueve se comprueban
solas; las cuatro amarillas son las tres mediciones con coste (`PRM-008`,
`PRM-009`, `PRM-010`) y la de la bandera peligrosa como root (`PRM-011`), que no
se automatiza porque su resultado depende del usuario que ejecute el
verificador y en una máquina normal daría falso rojo.

**Mediciones propias, dos repeticiones idénticas cada una, 2.1.235.** Mismo
repo, misma petición, variando una sola cosa:

| Medida | Resultado |
|---|---|
| `allow` en el settings del proyecto, sin confianza | **no se aplica**, 131.788 y 131.806 tokens, 3 turnos |
| La misma regla por `--allowedTools` | funciona, 87.452, 2 turnos |
| La misma regla en el mismo archivo, con confianza aceptada | funciona, 87.456, 2 turnos |
| `deny Read` frente a `cat` | bloqueado las dos veces, y lo dice |
| `deny Read` frente a `python3 -c open(...)` | **imprime la clave las dos veces** |
| 24 reglas `deny` frente a ninguna | 43.619 tokens las cuatro veces |
| `claude auto-mode defaults` | 17 / 66 / 1 / 20 y 63.477 bytes |

**Hallazgos propios del módulo:**

- **La asimetría de la confianza es la columna vertebral del módulo.** Lo que
  restringe (`deny`, `ask`) se acepta desde el repositorio; lo que concede
  (`allow`, `additionalDirectories`) no, hasta aceptar el diálogo. Y como el
  diálogo **no aparece nunca en `claude -p`**, toda tubería de integración
  continua del mundo corre con las reglas `allow` de su repositorio ignoradas.
  El aviso existe y sale **por la salida de error**, así que quien capture solo
  la estándar no lo ve. Es exactamente la trampa que la rutina ya tenía anotada
  desde la sesión de la mañana, medida y convertida en sección.
- **Una regla que no se aplica cuesta un 51 % más** que la misma regla
  aplicándose, y un turno extra. La configuración rota no es neutra.
- **Los seis modos tienen dos listas de nombres.** El error de
  `--permission-mode` enumera `manual`; el del esquema de `settings.json`
  enumera `default`. Los dos sitios aceptan las dos palabras y cada mensaje
  enseña solo una. Sostenido por `PRM-004` y `PRM-005`.
- **Las reglas de permisos cuestan cero tokens.** Al lado de los 1.311 por turno
  del `CLAUDE.md` del módulo 03, eso reordena el consejo: cuando se pueda elegir
  entre pedirlo en el archivo de memoria o imponerlo con una regla, la regla es
  más barata y además se cumple.
- **Lo que una regla no puede proteger.** `cat` se bloquea y `python3` no, y una
  regla protege rutas, no valores: la clave que vive dentro de `app.py` no tiene
  regla posible. Es el puente natural al hook del módulo 05.

**Sonda nueva en el repositorio:** `D2-verificador/sonda-esquema/`, con un
`settings.json` inválido a propósito. `claude doctor` corriendo ahí enumera lo
que el esquema del binario acepta de verdad, y es lo que sostiene `PRM-005` y
`PRM-006`. Es la técnica del módulo 02 convertida en herramienta permanente.

**Laboratorio:** `D6-repo-feo/gestor-pedidos` gana `.claude/settings.json` con
el perfil normal (deny de secretos y de red, ask en `git push`, allow para lo de
todos los días), `PERMISOS.md` con el porqué de cada regla y con lo que las
reglas **no** protegen, `.gitignore`, y `secretos/pasarela.env.ejemplo`. El
archivo real, `secretos/pasarela.env`, se queda fuera de git y `PRM-016` lo
vigila. **Ningún fallo sembrado se ha tocado**: la clave sigue dentro de
`app.py`, que es justo lo que el módulo usa para enseñar el límite del sistema.

**Activos:** `entregables/plantillas/permisos/` con los tres perfiles (cauto,
normal, laboratorio) y `entregables/plantillas/devcontainer/` con el contenedor
de red restringida.

**Bookkeeping:** `fabrica/hechos.yaml` y `README.md` pasan de "3 de 12" a
"4 de 12". Hecho canónico nuevo, `ALLOW-NECESITA-CONFIANZA`.

### PARA JULIÁN

1. **Sigue abierta la fecha de corte del libro**, cuarta vez. El 04 se ha
   escrito contra la 2.1.235 y lo declara en cabecera, igual que el 02 con la
   2.1.233 y el 03 con la 2.1.234. Ya van tres módulos con versión propia: la
   opción "cada módulo declara la suya" está ganando por goleada sin que nadie
   la haya decidido. Decidirlo cuesta cinco minutos y evita reescribir el 01.
2. **El inventario del repo feo sigue sin actualizar**, tercer módulo que lo
   dice. Además de lo del 03 (`utils.py`, `config.py` y `settings.py` son código
   muerto, no lógica duplicada), el módulo 04 añade dos cosas al recorrido del
   fallo 1: el laboratorio ahora tiene `secretos/` y `PERMISOS.md`, y la clave
   de `app.py` queda **explícitamente sin resolver** hasta el módulo 12. Si
   quieres que el guion lo refleje, es una línea en la tabla del recorrido y no
   la he tocado yo porque es material compartido por los doce módulos.
3. **Decisión nueva, y es tuya.** El módulo 04 dice que la clave de `app.py` se
   saca del código en el 12. El guion de doma dice que el fallo 1 se caza "en el
   04 y en el 10". Las dos cosas no encajan del todo: o el 04 la saca (y el 10
   pierde media auditoría), o el guion pasa a decir que en el 04 se **acota** y
   en el 12 se **elimina**, que es lo que hace el texto tal como está escrito.
   He escrito el módulo con la segunda lectura porque no destruye material de
   laboratorio, pero la palabra final es tuya.

## 2026-08-19 · El módulo 04 no se escribió: colgada en un diálogo de permisos

**La rutina disparó a las 06:17 y a las 06:22 se quedó parada.** No fue el paso
0a: el agente se arregló solo lo del `fetch`, pasó el dry-run, eligió el 04, se
leyó `permission-modes`, `permissions`, `sandboxing` y `sandbox-environments`, y
empezó a medir. Murió en la llamada que devolvía el laboratorio a su sitio:

```
cp /tmp/.../settings.bak2.json .claude/settings.json
```

Escribir en un `settings.json` **copiando desde fuera del repositorio** se lee
como escalada de privilegios y pide permiso. Que el mismo archivo lo hubiera
modificado un minuto antes con un `cat > ... <<'JSON'` sin que nadie preguntara
es exactamente lo que hace que la trampa no se vea venir. Cuatro horas y media
en `requires_action` delante de un `cp`.

**Arreglado en la rutina** (19-ago, 12:53): el `git fetch origin main` va delante
en el paso 0a, y hay un **paso 0d** nuevo con la regla: lo que entra al
repositorio se escribe, no se copia; y si algo se queda esperando permiso, no se
reintenta, se cambia de camino o se termina la sesión.

**Se rescatan dos cosas de lo que sí midió**, y valen para el módulo 04:

- `claude auto-mode defaults` imprime la política del clasificador en JSON: 17
  entradas en `allow`, 66 en `soft_deny`, 1 en `hard_deny` y 20 de `environment`,
  62.957 bytes. Es una cifra propia y comprobable, mejor que cualquier paráfrasis
  de la documentación.
- **El sandbox de la nube no puede medir el efecto de `permissions.allow`**: no
  ha aceptado el diálogo de confianza del espacio de trabajo, así que ignora las
  cuatro reglas y **lo avisa por la salida de error, no por la de datos**. Con
  reglas y sin reglas dio el mismo número exacto, 43.616 tokens. Quien lo mida
  sin mirar stderr publicará que las reglas no cuestan nada, y lo que pasa es que
  no se están aplicando. Anotado en la rutina.

**La CI llevaba seis ejecuciones en rojo desde el 17-ago**, y no se había mirado.
El trabajo `verificar` pasaba; el que moría era `publicar-estado`, con `la prueba
CLI-010 tiene motivo sospechosamente largo`. El tope de 400 caracteres valía para
afirmaciones y comandos, pero el `motivo` de una prueba amarilla es prosa: ya
eran tres los que no cabían (CLI-010, CTX-012 y CTX-013, los tres del 02 y el
03). El motivo tiene ahora su propio tope de 1200. Efecto colateral que importa:
**`estado.html`, la página pública de verificación, llevaba desde el 17-ago
congelada** diciendo 30 pruebas contra la 2.1.233, mientras `ESTADO.md` ya decía
36 contra la 2.1.234. Regenerada.

### PARA JULIÁN

1. **Sigue abierta la fecha de corte**, tercera vez que se pide. Recomendación:
   que cada módulo declare su versión, que es lo que ya hacen el 02 y el 03 de
   hecho, y que la portada diga solo `v2026.08`. Un libro que promete una
   versión única del CLI nace caducado; uno que fecha cada módulo, no.
2. Falta empujar el arreglo de la CI, que el R630 no puede:
   `! git -C ~/manual-claude-code push origin main`

## 2026-08-18 · Módulo 03 · Memoria y contexto · PUBLICADO

Cerrado `manuscrito/modulo-03-memoria-y-contexto.md`, **3.989 palabras**, las
seis partes del esqueleto y runbook de una página. Verificador contra la
**2.1.234**: **36 pasan, 0 fallan, 9 a revisar, 3 omitidas**. Coherencia y
`construir.py --comprobar`, las dos en verde. Quedan nueve módulos: 04 a 12.

**La rutina publicó por primera vez.** El paso 0a no bastaba: el sandbox clona
con un `origin/main` **también** atrasado, así que `git checkout -B main
origin/main` reseteaba a un commit viejo y el dry-run seguía dando
`non-fast-forward`. Se arregla con un `git fetch origin main` **antes** del
checkout. Conviene meterlo en el paso 0a de la rutina: con el fetch delante, el
dry-run dio `Everything up-to-date` a la primera.

**Registro:** diez entradas nuevas, `CTX-004` a `CTX-013`. Once de las trece
`CTX` se comprueban solas; las dos amarillas son la medición de tokens
(`CTX-012`, marcada además con `coste: true`) y el fallo de autenticación de
`--bare` (`CTX-013`).

**Mediciones propias, dos repeticiones idénticas cada una, 2.1.234.** Mismo
repo, misma petición, variando una sola cosa:

| Estado del archivo | Tokens de entrada |
|---|---:|
| Sin `CLAUDE.md` | 42.302 |
| `CLAUDE.md` de 66 líneas | 43.480 |
| Más 40 líneas dentro de `<!-- -->` | **43.480, el mismo número exacto** |
| Esas 40 líneas visibles | 46.720 |

El comentario HTML no cuesta "poco": cuesta **cero**, al token. Y el archivo
final de 67 líneas cuesta **1.311 tokens por turno**, que es el impuesto de
contexto que declara el módulo.

**El experimento del IVA, repetido y confirmado.** Con el `CLAUDE.md` final:
solo `app.py`, 3 turnos, 131.952 y 132.003 tokens. Sin él: `settings.py`,
`utils.py` y `app.py`, 7 turnos, 216.615 y 261.009. Acierta **y** cuesta entre
1,6 y 2 veces menos. Las dos ejecuciones sin archivo se diferencian un veinte
por ciento entre sí: sin contexto, cada una explora por su cuenta.

**Hallazgos propios del módulo:**

- **El agente corrigió mi `CLAUDE.md` en directo.** El borrador citaba números
  de línea y dos estaban mal; lo detectó y avisó. La versión publicada cita
  función y literal, y el módulo lo convierte en regla de escritura: los números
  de línea envejecen en el primer commit y luego mandan al sitio equivocado con
  la autoridad de estar escritos.
- **`--bare` no sirve de diagnóstico con login de suscripción.** No lee el OAuth
  guardado, así que contesta `Authentication error · This may be a temporary
  network issue`, que no lleva a nadie hasta la causa. El módulo da la
  alternativa: apartar el archivo con `mv` y volver a preguntar.
- **El suelo de arranque son 42.302 tokens** en este repo, antes de escribir una
  palabra. Pelearse por doscientos tokens de `CLAUDE.md` es pelearse por el
  0,5 %.
- **Partir el `CLAUDE.md` en reglas sin `paths` no ahorra ni un token**: se
  cargan al arrancar con la misma prioridad. Lo que ahorra es el frontmatter.
- La documentación de hoy trae cosas que la guía del 12-ago no tenía: el
  objetivo de 200 líneas, el recorte que propone `/doctor` desde la 2.1.206, el
  hook `InstructionsLoaded`, y que el `CLAUDE.md` **se entrega como mensaje de
  usuario después del sistema**, que es el fundamento de por qué no es
  configuración impuesta.

**Laboratorio:** `D6-repo-feo/gestor-pedidos` gana `CLAUDE.md`, 67 líneas, con
la tabla de dónde vive de verdad cada valor, la lista de código muerto y quién
gana los empates. `CTX-006` vigila que nadie lo reescriba diciendo que manda
`settings.py`.

**Bookkeeping:** `fabrica/hechos.yaml` y `README.md` pasan de "2 de 12" a
"3 de 12".

### PARA JULIÁN

1. **Sigue abierta la fecha de corte del libro**, sin tocar. El módulo 03 se ha
   escrito contra la 2.1.234 y lo declara en cabecera, igual que hizo el 02 con
   la 2.1.233. Ya van dos módulos declarando versión propia, así que la opción
   "cada módulo declara la suya" está ganando de hecho aunque no se haya
   decidido. Conviene decidirlo antes del 04.
2. **El inventario del repo feo se queda corto y ya son dos módulos que lo
   dicen.** El fallo 11 del guion de doma llama "lógica duplicada" a `utils.py`,
   y lo comprobado es peor: **nadie importa `utils.py`, ni `config.py`, ni
   `settings.py`**. Son tres módulos muertos, no una duplicación. Lo sostiene
   `CTX-007`. Actualizar `D6-repo-feo/guion-de-doma.md` es trabajo de una línea
   y no lo he hecho yo porque toca el material de laboratorio de los doce
   módulos.
3. **El paso 0a de la rutina necesita el `git fetch origin main` delante**, por
   lo explicado arriba. Sin él, la rutina se va a bloquear otra vez con un error
   que parece de credenciales y no lo es.

## 2026-08-17 · Tercera ejecución: murió por límite de uso, pero dejó oro

`cse_01LZNBhNjXkAaV63WnyvQXWS`. Con GitHub ya conectado, pasó las guardas y
midió de verdad. Murió a las 18:21 con `rate_limit: rejected (five_hour)`, no
por fallo propio: se habían encadenado tres ejecuciones en la misma ventana.

**Hallazgo que salva todas las ejecuciones futuras.** El 403 del push nunca fue
de credenciales del todo: **el sandbox clona en HEAD desprendido y deja un
`main` local viejo**, así que `git push origin main` intentaba enviar una rama
cuatro commits atrasada y fallaba con `non-fast-forward`. Se arregla con
`git checkout -B main origin/main` antes de nada. Ya está en el paso 0a de la
rutina. También dejó una rama de prueba `zz-cred-check` que no pudo borrar por
un fallo de sideband del proxy; se borró a mano desde el R630.

**Mediciones, con dos repeticiones idénticas cada una.** Sirven de patrón para
el módulo, no como cifras del libro (dependen de la máquina):

| Medida | Tokens de entrada |
|---|---:|
| `gestor-pedidos` sin `CLAUDE.md` | 39.625 |
| con `CLAUDE.md` de 58 líneas | 40.754 |
| **coste del archivo** | **1.129** |
| relleno dentro de comentario HTML | 40.754 |
| el mismo relleno visible | 44.594 |
| **lo que ahorra el comentario** | **3.840** |

**El experimento del laboratorio, que es el corazón del módulo 03.** Misma
petición ("sube el IVA de Portugal del 23 al 24, dime qué tocar"), mismo repo,
lo único distinto el `CLAUDE.md`:

| | Sin `CLAUDE.md` | Con `CLAUDE.md` |
|---|---|---|
| Respuesta | `settings.py:5`, `utils.py:23` y `app.py:74` | solo `app.py:74` |
| Correcta | **no**, dos de tres archivos están muertos | sí |
| Tokens de entrada | 209.868 | 85.217 |
| Turnos | 8 | 2 |

El archivo de memoria no solo lo hace acertar: lo hace costar **2,5 veces
menos**. Ese contraste vale el módulo entero.

**Fallo nuevo del laboratorio, no inventariado.** `utils.py` **no lo importa
nadie**, así que el módulo entero está muerto, incluida `calcular_iva()`, que
parece la función buena del IVA. El `guion-de-doma.md` lo lista como
"lógica duplicada" (fallo 11) y es peor que eso: es lógica muerta que atrae
cambios. Añadir al inventario.

## 2026-08-17 · La guardia funciona, y el bloqueo sigue

Segunda ejecución (`cse_018J8jRAL6L4rwo6o8VJCvyy`) con el paso 0a puesto:
**paró en 47 segundos sin escribir nada.** Antes eran treinta minutos tirados.

Su diagnóstico, mejor que el nuestro: no hay `credential.helper`, el proxy del
sandbox está sano (`recentRelayFailures` vacío, `gitConfigInjection` activo), y
la API de GitHub por MCP devuelve 503. **El 403 es de autorización, no de red.**

Comprobado desde el R630 el mismo minuto: GitHub "All Systems Operational", cero
incidentes, su API responde 200. El 503 del sandbox y el 500 de `/web-setup` son
del lado de Anthropic.

**Estado de las dos vías para desbloquear:**

- `/web-setup` sincroniza el token del `gh` local. En el R630 `gh` ya está
  autenticado como `julian-najas` con permisos `repo` y `workflow`, o sea que la
  materia prima está lista. El comando devolvió 500 el 17-ago; hay que
  reintentarlo.
- La Claude GitHub App, en `https://github.com/apps/claude`, no pasa por el
  servidor que está fallando. Instalarla en el repositorio no es obligatorio
  para que la sesión pueda empujar.

Cualquiera de las dos vale. Hasta que haya una, la rutina para en 47 segundos
cada mañana en vez de trabajar en balde.

## 2026-08-17 · Primera ejecución de la rutina: escribió el 03 y lo perdió

**El módulo 03 se escribió entero y no llegó a publicarse.** La ejecución de
prueba (`cse_013jyT7FnGxu85HXcXvgyvPi`) hizo el trabajo bien: 4.005 palabras,
seis partes, `CLAUDE.md` del laboratorio, entradas nuevas en el registro,
coherencia en verde, commit `07b30e6`. Y el push murió:

```
fatal: unable to access 'https://github.com/julian-najas/manual-claude-code/':
The requested URL returned error: 403
```

**Causa:** el sandbox de la nube clona sin credenciales (basta con que el repo
sea público) pero **no tiene credenciales de escritura**. Un push anónimo
siempre da 403. Falta conectar GitHub, con `/web-setup` desde el terminal o
autorizando la Claude GitHub App. Según `claude-code-on-the-web.md`, instalar la
App en el repositorio no es obligatorio: vale cualquiera de las dos vías.

**Culpa del montaje, no del agente.** La rutina se creó llamando a la API
directamente en vez de por el flujo interactivo, y así se salta el aviso que
`/schedule` da cuando no hay acceso de escritura.

**Arreglado ya:** la rutina hace ahora `git push --dry-run` como **paso 0a** y
para en seco si no puede publicar, sin escribir una línea. Media hora de máquina
en vez de treinta minutos tirados.

**Lo que se salvó del naufragio.** La ejecución destapó tres defectos reales del
verificador, y esos sí están arreglados y commiteados:

- `REPO-002` y `REPO-003` daban rojo por el proxy del sandbox (403), no porque
  el companion se hubiera caído.
- `CLI-007` daba por hecho una instalación nativa que en la nube no existe.
- De fondo: el verificador no distinguía **"es falso"** de **"no he podido
  comprobarlo"**. Ahora una prueba de red caída sale amarilla con el motivo
  escrito, y un 404 sigue siendo rojo.

## Próxima iteración · Módulo 03 · Memoria y contexto

**No empezado.** La iteración del 17-ago se cortó por límite de uso antes de
escribir una línea, y no se dejó un módulo a medias a propósito. Lo recoge la
rutina de la nube en su primera ejecución.

Preparación ya hecha, para no repetirla:

- Fuente principal: `guia-21/M4-memoria-y-contexto.md`, leído y utilizable.
- Contrato: sección "Módulo 03" de `manuscrito/ESQUELETO.md`. IDs ya en el
  registro: `CTX-001` (`--add-dir`), `CTX-002` (`--autocompact`), `CTX-003`
  (`--bare`). Habrá que añadir entradas nuevas.
- Documentación oficial **pendiente de descargar de nuevo** (la regla es
  descargarla en cada módulo, no reutilizar la de otra sesión):
  `memory.md`, `context-window.md`, `claude-directory.md`, `settings.md`.
- Laboratorio: `D6-repo-feo/gestor-pedidos`, que ya tiene `.claude/settings.json`
  y `ENTORNO.md` del módulo 02. El `CLAUDE.md` lo escribe este módulo.
- **La trampa del laboratorio, ya documentada como hecho canónico
  `CONFIG-NINGUNO-SE-USA`:** la respuesta a "qué configuración manda" es
  **ninguna de las dos**. Ni `config.py` ni `settings.py` se importan; `app.py`
  fija sus valores a mano (`DB`, `DEBUG`, el IVA y el tope de 50 líneas). El
  módulo tiene que llevar al lector hasta ahí, no hasta "manda settings.py".
- El código muerto que el `CLAUDE.md` debe declarar: `/pedido_old/<id>`, que lee
  la tabla `pedidos_2019` (fallo 6 del guion de doma).

## 2026-08-17 · Módulo 02 · Instalación, autenticación y versiones

Cerrado `manuscrito/modulo-02-instalacion.md`, 3.849 palabras, las seis partes
del esqueleto y runbook de una página. Verificador en verde: **30 pasan, 0
fallan, 5 a revisar, 3 omitidas** contra 2.1.233. Quedan diez módulos: 03 a 12.

Añadidas al registro nueve entradas nuevas (CLI-004 a CLI-010, AUT-001, ENT-001,
ENT-002). Las cinco amarillas son manuales justificadas: HOK-001, MCP-002,
TRB-002 (trimestrales de siempre) y las dos nuevas, CLI-010 y AUT-001.

**Hallazgos propios del módulo, no copiados de la guía de 21:**

- `claude doctor` **termina en 0 aunque reporte `Invalid settings`**, y sigue
  imprimiendo `No installation issues found`. Una comprobación de CI que mire
  solo el código de salida da verde con la configuración del proyecto rota.
- Un nombre de clave mal escrito en `settings.json` **no se reporta en
  absoluto**. Los valores inválidos de claves conocidas sí, y con detalle.
- El binario acepta un tercer canal, **`rc`**, que no aparece en `setup.md` ni
  en `settings.md`. Marcado en caja "esto va a cambiar", no recomendado.
- La precedencia de credenciales **eran cuatro niveles en nuestra guía y hoy son
  siete**. Corregido en el manuscrito y anotado como recuento trimestral.
- `--help` es **byte a byte idéntico entre 2.1.228 y 2.1.233** (242 líneas),
  mientras la documentación condiciona comportamiento a 14 versiones distintas.
  Eso reorienta el módulo entero: la versión no quita comandos, cambia lo que
  hacen.

**Laboratorio:** `D6-repo-feo/gestor-pedidos` gana `.claude/settings.json` y
`ENTORNO.md`. Verificado que el archivo se carga de verdad: `claude doctor`
dentro del repo dice `Auto-update channel: stable` y fuera dice `latest`. Ese
contraste es el criterio PASA del módulo.

**Bookkeeping:** `fabrica/hechos.yaml` y `README.md` pasan de "1 de 12" a
"2 de 12". Coherencia y `construir.py --comprobar`, las dos en verde.

### PARA JULIÁN

1. **La fecha de corte del libro.** El esqueleto y el módulo 01 dicen "verificado
   contra 2.1.228, corte 12-ago-2026". La máquina va por la 2.1.233 y el
   verificador lleva días publicando estado contra 2.1.231, 2.1.232 y 2.1.233.
   El módulo 02 se ha escrito contra la 2.1.233 y lo declara en su cabecera, en
   vez de fingir. Decisión tuya: **recortar el libro entero a la versión del día
   de publicación** (tocar el esqueleto, el módulo 01 y la página de
   verificación), o **dejar el corte en 2.1.228 y que cada módulo declare la
   suya**. No lo he decidido yo porque afecta a la portada.
2. **El orden de escritura.** El esqueleto recomienda escribir el 02 el último
   ("es el que más envejece"). La orden del bucle es por número, así que va el
   segundo. No lo he cambiado, pero el módulo 02 va a necesitar un repaso corto
   justo antes de publicar, y conviene que esté presupuestado.
