# gestor-pedidos

App interna de pedidos de Cárnicas Hermanos Beltrán. Flask, SQLite, un solo
proceso. Escrita en 2019 por alguien que ya no está.

<!--
Nota para quien mantenga este archivo, no cuesta tokens:
lo de abajo se comprobó leyendo app.py el 18-ago-2026, no el README ni los
comentarios del código. Si tocas app.py, vuelve a comprobarlo.
-->

## La verdad sobre la configuración

**No hay archivo de configuración en uso.** `config.py` y `settings.py` existen,
se contradicen entre sí, y **ninguno de los dos se importa en ningún sitio**.
`app.py` fija sus valores a mano:

| Valor | Dónde está de verdad | Qué dicen los archivos muertos |
|---|---|---|
| Ruta de la base de datos | `app.py`, constante `DB` | `settings.py` dice `/var/lib/pedidos/pedidos.db` |
| Modo depuración | `app.py`, constante `DEBUG`, en `True` | `settings.py` dice `False` |
| IVA de España | `app.py`, literal `1.21` dentro del bloque `# iva` de `procesar_pedido()`, y otra vez en el `else` | `config.py` dice `IVA = 0.21` |
| IVA de Portugal | `app.py`, literal `1.23` en la rama `pais == "PT"` de `procesar_pedido()` | `settings.py` dice `IVA_PT = 0.23` |
| Tope de líneas por pedido | `app.py`, literal `50` en la validación de `procesar_pedido()` | `settings.py` dice `100` |

Las referencias van por función y por literal, no por número de línea: los
números de línea de este archivo envejecen en el primer commit y mandan al
agente al sitio equivocado con la autoridad de estar escritos.

**Para cambiar cualquiera de esos valores hay que editar `app.py`.** Editar
`config.py` o `settings.py` no tiene ningún efecto sobre la aplicación.

## Código muerto. No proponer cambios aquí

- `utils.py` entero. **Nadie lo importa.** Incluye `calcular_iva()`, que parece
  la función buena del IVA y no la llama nadie.
- `config.py` y `settings.py`, por lo dicho arriba.
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
