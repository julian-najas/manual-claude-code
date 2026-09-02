# gestor-pedidos

App interna de pedidos de Cárnicas Hermanos Beltrán. Flask, SQLite, un solo
proceso. Escrita en 2019 por alguien que ya no está.

<!--
Nota para quien mantenga este archivo, no cuesta tokens:
lo de abajo se comprobó leyendo app.py el 2-sep-2026, no el README ni los
comentarios del código. Si tocas app.py, vuelve a comprobarlo.
Reescrito ese día: hasta el módulo 12 este apartado decía que no había
configuración en uso, y era verdad. Dejó de serlo con el código, no después.
-->

## La verdad sobre la configuración

**Manda `config.py`, y `app.py` lo importa de verdad.** Hasta el 2-sep-2026 no
era así: había dos archivos que se contradecían y **no se importaba ninguno**.
`settings.py` ya no existe.

| Valor | Dónde está | Cuidado |
|---|---|---|
| Ruta de la base de datos | `config.DB_PATH` | `app.py` lo reexpone como `DB`, y las pruebas dependen de ese nombre |
| Modo depuración | `config.DEBUG`, en `True` | Sigue en `True`: es el fallo 7, no se ha arreglado |
| Tipos de IVA | `config.IVA_POR_PAIS`, cuatro países | **No hay tipo por defecto.** Un país fuera de la tabla se rechaza con 400 |
| Tope de líneas por pedido | `config.MAX_LINEAS`, en 50 | Cincuenta, que es lo que se estaba validando |
| Descuentos por cantidad | `config.DESCUENTO_MAS_DE_10` y `..._DE_100` | **Se acumulan**, a propósito y por escrito |

Las referencias van por función y por literal, no por número de línea: los
números de línea de este archivo envejecen en el primer commit y mandan al
agente al sitio equivocado con la autoridad de estar escritos.

**El porqué de cada uno de esos valores está en `DECISIONES.md`.** Antes de
cambiar cualquiera, léelo: varios son decisiones de negocio congeladas a
propósito, no descuidos pendientes de arreglar.

## Código muerto. No proponer cambios aquí

- `utils.py` entero. **Nadie lo importa.** Incluye `calcular_iva()`, que parece
  la función buena del IVA, no la llama nadie, y además se quedó sin Francia ni
  Italia el día que la tabla buena pasó a `config.py`.
- El endpoint `GET /pedido_old/<id>`, que lee la tabla `pedidos_2019`. Sigue
  expuesto y nadie lo llama desde 2019.

Si un cambio parece que toca alguno de estos, el cambio está en el sitio
equivocado. Dilo antes de editar.

## El README miente

`README.md` documenta un `POST /anular` que no existe, y se calla el
`/pedido_old/<id>` que sí existe. **Los endpoints reales son cuatro**, y salen
de `app.py`: `GET /pedido/<id>`, `GET /buscar`, `POST /procesar` y
`GET /pedido_old/<id>`.

Cuando el README y `app.py` se contradigan, **manda `app.py`**.

## Cómo se ejecuta

```bash
pip install -r requirements.txt
python app.py
```

Escucha en el 5000. No hay tests. No hay linter configurado.

## Antes de tocar nada

Este repositorio tiene fallos de seguridad deliberados, incluida una clave de
pasarela de pago en claro en `app.py`. Es material de laboratorio del manual
"Claude Code en producción". **No se despliega.** No hace falta que avises de
esos fallos en cada respuesta: están inventariados.
