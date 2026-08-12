# Los dos perfiles de settings, comentados

Los comentarios van aquí porque **JSON no admite comentarios** y un `settings.json`
con `//` dentro se rechaza entero: usuario, proyecto y local son estrictos y un
archivo que no valida no se aplica en absoluto (M3).

## Qué cambia entre los dos

| Clave | Conservador | Autónomo | Por qué |
|---|---|---|---|
| `defaultMode` | `default` (Manual) | `auto` | El conservador revisa cada acción. El autónomo delega en el clasificador |
| `allow` | Comandos concretos | Familias enteras | Cuanto más ancho, menos confirmaciones y menos control |
| `ask` | push **y** commit | Solo push | `ask` fuerza confirmación aunque otra regla lo permitiera |
| `deny` | Añade `curl` y `wget` | Solo secretos | El conservador corta la salida a red desde Bash |
| `worktree` | No lo fija | `fresh` y symlinks | El autónomo trabaja aislado por defecto |

## Lo que comparten, y no es negociable

- **`deny` sobre secretos.** Las reglas de permisos **se fusionan entre ámbitos**,
  así que un `deny` en el settings del proyecto **no lo puede levantar nadie**
  desde su configuración local. Por eso la protección va aquí y va a git.
- **`minimumVersion`.** Fija el suelo para que las autoactualizaciones no
  degraden a nadie por debajo de la versión verificada.
- **`autoUpdatesChannel: "stable"`.** Una semana de retraso a cambio de saltarse
  las releases con regresiones importantes.

## Avisos

- **`allow` de proyecto requiere confianza del espacio de trabajo.** `deny` y
  `ask` se aplican siempre. Si ves `Ignoring N ...` al arrancar, es eso.
- **`defaultMode` importa más desde el 14 de agosto de 2026**, cuando auto mode
  pasa a ser el modo por defecto en Pro, Max y Team. Fijarlo aquí es decidir tú.
- **`autoMode` no se lee del settings de proyecto ni del local**, a propósito: un
  repositorio clonado no puede relajarte el clasificador.
