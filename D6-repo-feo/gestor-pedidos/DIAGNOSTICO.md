# Diagnóstico de este repositorio

Qué hacer cuando algo de `gestor-pedidos` falla, dónde mirar, y **qué sigue sin
dejar rastro**. Escrito en el módulo 11 del manual, el 1 de septiembre de 2026.

## Lo que cambió, y por qué importa

Hasta hoy, `procesar_pedido()` llamaba a `enviar_email()` dentro de un
`except:` desnudo con un `pass` debajo. Efecto medido: con el aviso reventando
por `ConnectionRefusedError`, la petición devolvía **HTTP 200**, el pedido
quedaba guardado en la base de datos y **no se imprimía ni una línea**, ni
siquiera con el registro puesto en `DEBUG`. Dos de dos.

No había nada que diagnosticar porque no había nada que mirar. Ese es el fallo
número 5 del inventario, y era el peor de los catorce: los demás producen un
síntoma.

Ahora la misma situación deja una entrada de nivel `ERROR` con la traza entera,
y **el pedido sigue adelante igual**. La decisión de 2019 se conserva a
propósito: no se bloquea una venta porque falle un correo. Lo que cambia es que
alguien se entera.

## Cómo mirar el registro

```bash
NIVEL_LOG=DEBUG python app.py
```

El nivel sale de la variable de entorno `NIVEL_LOG` y por defecto es `INFO`. Es
la única pieza de configuración de este repositorio que **sí se lee de verdad**:
`config.py` y `settings.py` siguen sin importarse desde ningún sitio, como dice
el `CLAUDE.md`.

El registrador se llama `gestor-pedidos`. Para filtrar en producción, ese es el
nombre.

## Las pruebas de diagnóstico

`tests/test_diagnostico.py`, dos pruebas, y hacen trabajos distintos:

| Prueba | Qué fija |
|---|---|
| `test_un_aviso_que_falla_no_tumba_el_pedido` | La decisión de 2019: el pedido continúa. Pasaba antes y pasa ahora |
| `test_un_aviso_que_falla_deja_traza_en_el_registro` | Que el fallo queda escrito, con nivel `ERROR` y con `exc_info` |

La segunda es la red contra la reincidencia. Comprobado: contra el `except:`
desnudo original falla en la primera aserción, con la lista de registros vacía.
Contra el código de hoy pasa. Si alguien repone el `except:` desnudo, o cambia
el `log.exception()` por un `log.error()` sin traza, esa prueba se pone roja.

Comprobar `exc_info` y no solo el texto no es celo: sin traza tienes una línea
que dice que algo falló y no dice dónde.

## Qué sigue sin dejar rastro

Esto es la mitad útil de este archivo. Lo que **no** cubre el registro de hoy:

- **`cobrar()` y `enviar_email()` siguen vacías desde 2020.** No fallan: no
  hacen nada. Un aviso que nunca se manda no produce ninguna entrada de error,
  porque no hay error. Es peor que un fallo y no lo va a encontrar ningún
  registro.
- **Las cinco concatenaciones de SQL** no registran nada. Un `sqlite3` que
  revienta con un apóstrofo sube como error 500 de Flask, sin pasar por aquí.
- **`GET /pedido/<id>` con un id que no existe** responde **200 con `null`**, no
  404. Es una respuesta correcta desde el punto de vista del registro: nadie
  falló.
- **La clave de pasarela en claro** no es un fallo de ejecución y no aparecerá
  nunca en un registro. Ver `SEGURIDAD.md`.

## Antes de reportar un fallo del CLI

Los tres pasos, en este orden, y el segundo es el que se salta todo el mundo:

1. `claude --version`. Anótala. **`claude doctor` sale con código 0 aunque
   encuentre avisos**: hay que leer la salida, no el código.
2. `claude --safe-mode`. Si el problema desaparece, es de este repositorio: del
   `CLAUDE.md`, de la skill, del servidor MCP o de los tres hooks.
3. Si persiste, configuración limpia de verdad:
   `cd /tmp && CLAUDE_CONFIG_DIR=/tmp/claude-limpio claude`.

Y para ver algo en modo no interactivo, **`--debug` no vale, `--debug-file`
sí**. Medido el 1-sep-2026 con la 2.1.252 sobre este repositorio: `claude -p`
con `--debug` produce **cero líneas** de depuración; el mismo comando con
`--debug-file` escribe **211**, dos de dos.
