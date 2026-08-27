# La CI de este repositorio

Tres trabajos en `.github/workflows/ci.yml`, en un orden deliberado: lo que no
gasta dinero corre primero. Aquí está por qué está escrita así, qué falla y qué
no cubre.

## Qué comprueba, en orden

| Trabajo | Qué hace | Cuándo falla |
|---|---|---|
| `entorno` | `pip install --no-deps -r requirements-dev.txt` y `pip check` | Cuando el cierre de dependencias está incompleto |
| `pruebas` | `python -m pytest -q` | Cuando una prueba falla, y también cuando no hay ninguna |
| `puerta` | Una llamada a `claude --bare -p` sobre el diff | Cuando la llamada no devuelve veredicto, o cuando el veredicto es bloquear |

`puerta` solo corre en propuestas de cambio y solo mira el diff. Leer el
repositorio entero en cada empujón es gasto sin criterio.

## Por qué `--no-deps`

Antes del módulo 09, `requirements.txt` tenía tres líneas sin versión: `flask`,
`requests` y `sqlalchemy`. Esas tres líneas resuelven a **quince paquetes**. Los
doce restantes entraban por arrastre, con la versión que hubiera ese día.

Con el cierre completo escrito y `--no-deps`, `pip` instala exactamente lo que
pone y nada más, y `pip check` avisa si falta algo. Sobre el
`requirements.txt` viejo, esa comprobación nombra **los doce paquetes que
faltan** y sale con código 1. Medido el 27-ago-2026.

Para regenerarlo:

```bash
pip install flask requests sqlalchemy && pip freeze > requirements.txt
```

## Por qué las pruebas son de caracterización

`tests/test_caracterizacion.py` no prueba lo que la aplicación **debería** hacer.
Prueba lo que hace hoy. **Cinco de las nueve empiezan por `test_hoy_`**: el IVA
español cobrado a Francia, el mismo IVA cuando no se dice el país, los dos
descuentos de cantidad acumulándose, el apóstrofo que tumba `/buscar` y el
pedido inexistente que responde 200 con `null`.

Los enunciados dicen "hoy", no "debe", a propósito. El día que el módulo 12
arregle el IVA, esas pruebas tienen que fallar: que fallen es el trabajo que
hacen. Una red no dice adónde ir, dice desde dónde te has caído.

**Sobre el repositorio tal cual venía, `pytest` sale con código 5** y escribe
"no tests ran". No es 0 ni es 1, así que un paso de CI que solo mire "salió
cero" lo cuenta como fallo, que es lo correcto, y un `|| true` puesto para
callarlo deja la CI en verde con cero pruebas durante años.

## Por qué la puerta va en modo `--bare`

Porque una puerta cuyo criterio lo fija el repositorio que juzga no es una
puerta. En modo `--bare` no se cargan el `CLAUDE.md`, ni los hooks de
`.claude/settings.json`, ni el `.mcp.json`, ni las skills de este repositorio.
Dos ejecuciones en dos máquinas dan lo mismo.

Tiene un precio que hay que saber antes de montarlo: **en modo `--bare` no se
lee ni la sesión de suscripción ni el llavero.** Exige `ANTHROPIC_API_KEY` en el
entorno. Sin ella, la ejecución termina con `is_error: true` y el texto
`Authentication error` en el campo `result`.

Y el veredicto se lee en dos pasos, en este orden:

1. `is_error`, y que el campo `result` exista.
2. Solo entonces, `structured_output.bloquea`.

Al revés se aprueba una fusión porque el modelo no llegó a hablar. Con el tope
de `--max-budget-usd` agotado, la salida JSON **no trae campo `result`**, así que
un `jq -r '.result'` devuelve `null` sin dar error.

## Lo que esta CI NO cubre

- **No mira el repositorio, solo el diff.** La clave de pasarela de `app.py`
  lleva ahí desde 2019 y ningún diff la introduce, así que la puerta no la ve
  nunca. Eso es del módulo 10, no de aquí.
- **No hay linter ni formateador.** El formateo lo hace el hook `formatear.sh`
  al editar, y eso no es lo mismo que comprobarlo.
- **`--max-budget-usd` no es un presupuesto, es un freno.** Se comprueba entre
  llamadas, así que la ejecución que lo agota ya se lo ha gastado. Medido: con
  un tope de 0,01 $, dos ejecuciones costaron 0,193 $ y 0,043 $ antes de parar.
- **La puerta no bloquea la fusión por sí sola.** Eso lo hace la protección de
  rama de la forja, y es una decisión de equipo.
