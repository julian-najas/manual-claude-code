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
