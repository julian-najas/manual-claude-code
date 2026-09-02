# Decisiones de este repositorio

Al lado de `PERMISOS.md`, `HOOKS.md`, `MCP.md`, `SKILLS.md`, `AGENTES.md`,
`CI.md`, `SEGURIDAD.md` y `DIAGNOSTICO.md`. Este archivo existe porque el módulo
12 del manual se dio de bruces con el problema que ninguno de los once
anteriores resuelve: **el agente sabe leer el código, y no sabe a quién
preguntar.**

Todo lo de aquí abajo es una decisión que **no estaba escrita en ningún sitio**
y que el código estaba tomando igual, en silencio, desde 2019.

---

## D1 · Un país sin tipo de IVA se rechaza. No se le cobra el español

**Decidido el 2-sep-2026. Cambia el comportamiento.**

Antes, el bloque `# iva` de `procesar_pedido()` tenía tres ramas: `ES`, `PT` y
un `else` con el 21 % español y el comentario `# revisar con gestoria`. Ese
`else` atendía dos casos que no se parecen en nada:

- un pedido de un país con su propio tipo, al que se le cobraba el español;
- un pedido **sin país**, del que no se sabía nada, al que se le cobraba el
  español también.

Ahora los tipos viven en `config.IVA_POR_PAIS` y un país que no esté en esa
tabla, o un pedido sin país, devuelve **400 con el país en el cuerpo** y deja
una línea de nivel `WARNING` en el registro.

**Lo que esto rompe, y hay que saberlo antes de desplegar:** todo pedido que hoy
llegue sin el campo `pais` deja de crearse. Si eso es la mayoría del tráfico
nacional, el arreglo del código es de una línea y el despliegue no: hace falta
rellenar el campo en el origen primero, o aceptar `ES` por defecto durante una
ventana de transición y con fecha de caducidad escrita.

**Lo que sigue sin decidir:** qué países van en la tabla y con qué tipo. Lo fija
la gestoría. Los cuatro que hay son los que el código tiene que saber contestar
hoy en el laboratorio; el manual no certifica tipos impositivos.

## D2 · Los dos descuentos por cantidad se acumulan

**Decidido el 2-sep-2026. No cambia el comportamiento.**

Una línea de más de 100 unidades pasa por los dos factores: `0,95 × 0,90 =
0,855`. El comentario original decía *"ojo: esto no se acumula con el de arriba?
nadie lo sabe"*.

La decisión no es que acumular sea lo correcto. Es que **era lo que llevaba
pasando cinco años**, nadie decidió lo contrario, y un cambio de precios no se
cuela dentro de una refactorización. Lo que cambia es que ha dejado de ser un
accidente: está en `config.py` con nombre, y la prueba que lo fija ya no se
llama `test_hoy_`.

Si negocio decide que no deben acumularse, es cambiar un `if` por un `elif` y la
prueba dirá exactamente cuánto cambia la factura de un pedido de 150 unidades.

## D3 · La configuración vive en `config.py`, y `settings.py` ya no existe

**Decidido el 2-sep-2026. No cambia el comportamiento.**

Había dos archivos que se contradecían **y ninguno se importaba**. Los valores
que se conservan son los que la aplicación tenía en ejecución, no los del
archivo más nuevo:

| Valor | Se queda | `settings.py` decía | Por qué |
|---|---|---|---|
| Tope de líneas | 50 | 100 | Es lo que validaba `app.py` |
| Modo depuración | `True` | `False` | Ídem, y su arreglo es del módulo 04 |
| Ruta de la base | `datos/pedidos.db` | `/var/lib/pedidos/pedidos.db` | Ídem |

**Unificar no es elegir el archivo más nuevo: es escribir lo que ya estaba
pasando.** Poner `MAX_LINEAS = 100` porque lo decía el archivo de 2021 habría
sido un cambio de producto disfrazado de limpieza.

## D4 · `app.DB` y `app.DEBUG` se quedan como nombres de módulo

**Decidido el 2-sep-2026. Restricción técnica, no preferencia.**

Su valor viene ya de `config`, pero los nombres siguen existiendo en `app.py`
porque **el fixture de `tests/` hace `monkeypatch` de `app.DB`** para trabajar
contra una base de datos de usar y tirar.

Meter `config.DB_PATH` directamente dentro de `conexion()` es más limpio, es
correcto, no cambia el comportamiento de la aplicación **y deja las trece
pruebas dando ERROR en el montaje**. Es una costura: la red de pruebas agarra la
aplicación por ahí. Quien la quite tiene que mover el fixture en el mismo
commit.

---

## Lo que este archivo no es

No es un registro de cambios: para eso está el historial. Es la lista de
**preguntas que el código contestaba sin que nadie las hubiera hecho**. Cuando
una de ellas se decida de verdad, se cambia aquí y se cambia la prueba, en el
mismo commit.
