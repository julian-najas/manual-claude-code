# Los hooks de gestor-pedidos

Tres hooks, y ninguno es una opinión: son las tres cosas que en este
repositorio no dependen del criterio de nadie. Están declarados en
`.claude/settings.json` y los scripts viven en `hooks/`, fuera de `.claude/`,
a propósito: la configuración que los declara y el código que ejecutan son dos
cosas distintas y se revisan por separado.

Medido con Claude Code **2.1.241** el 24 de agosto de 2026.

| Hook | Evento | Qué impide | Qué NO impide |
|---|---|---|---|
| `veto-secretos.sh` | `PreToolUse` sobre `Read\|Edit\|Write` | Que cualquier herramienta de archivo abra `secretos/` o un `.env` | Una referencia con `@` en el prompt: ahí no hay llamada a herramienta y el hook no dispara. Lo cubre la regla `deny` de `PERMISOS.md` |
| `veto-credenciales.sh` | `PreToolUse` sobre `Write\|Edit` | Que se escriba una credencial **en cualquier ruta**, incluida una que nadie había previsto | Un secreto escrito por un subproceso de Bash. Para eso haría falta un hook sobre `Bash` mirando la cadena del comando |
| `formatear.sh` | `PostToolUse` sobre `Edit\|Write` | Nada. No puede: corre después | Que el `.py` quede sin formatear. Es lo único que hace |

## Por qué estos tres y no otros

**`veto-secretos.sh` es el cinturón del tirante.** La regla `deny` del módulo
04 ya bloquea `secretos/`. El hook está por dos razones: explica el bloqueo con
palabras nuestras cuando es él quien bloquea, y sigue en pie cuando alguien
cambia de modo de permisos, porque un `PreToolUse` corre antes que la
comprobación de modo, incluso en `bypassPermissions`.

**`veto-credenciales.sh` es lo único aquí que mira contenido.** El módulo 04
cerró con una frase que este archivo cumple: el día que alguien añada
`config/produccion.yaml` con credenciales dentro, un `deny` de `secretos/**` no
lo cubre. Este hook sí, porque no mira la ruta.

**`formatear.sh` no protege nada, y cuesta dinero.** Está aquí porque el
formato es una discusión que no merece ni un turno, y porque el módulo 05 lo
usa para enseñar lo que cuesta un hook que dispara en cada edición: la misma
edición de una línea pasó de 2 llamadas a herramienta a 6.

## Lo que estos hooks no son

No son una frontera de seguridad frente a alguien que quiera saltárselos. Son
una frontera frente al olvido, el mío y el tuyo. Quien pueda editar
`.claude/settings.json` puede quitarlos, y quien ejecute
`--settings '{"disableAllHooks": true}'` los apaga los tres para esa ejecución.

Y el aviso que hay que decir en voz alta: **los hooks de un repositorio se
ejecutan en `claude -p` sin que nadie acepte nada**. Clonar este repositorio y
lanzar una ejecución no interactiva dentro ejecuta estos tres scripts. Están
escritos para que puedas leerlos en dos minutos justamente por eso.

## Cómo se prueban

Un hook es un programa que lee JSON y escribe JSON, así que se prueba sin
arrancar una sesión. En `hooks/ejemplos/` hay cinco entradas de muestra:

```bash
hooks/veto-secretos.sh      < hooks/ejemplos/lectura-de-secreto.json
hooks/veto-credenciales.sh  < hooks/ejemplos/escritura-con-credencial.json
hooks/formatear.sh          < hooks/ejemplos/edicion-no-python.json
```

Las dos primeras tienen que imprimir un JSON con `"permissionDecision": "deny"`.
Las versiones inocuas (`lectura-inocua.json`, `escritura-inocua.json`) y la
tercera no tienen que imprimir nada y salir con 0. El verificador del manual
corre exactamente esto en `HOK-002` a `HOK-006`.

## Falsos positivos

`veto-credenciales.sh` mira contenido, así que se equivocará alguna vez. Un
archivo de pruebas con un `token: "abcdefghijklmnop"` de mentira lo dispara.
Cuando pase, se acota el patrón en el script y se anota aquí por qué. No se
quita el hook: un veto que se levanta la primera vez que molesta no era un veto.
