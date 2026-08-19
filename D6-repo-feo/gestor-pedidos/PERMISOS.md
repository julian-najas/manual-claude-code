# Permisos de este repositorio

Los permisos viven en `.claude/settings.json`, versionado. Este archivo explica
por qué está cada regla, que es lo que el JSON no puede decir.

| Regla | Por qué |
|---|---|
| `deny Read(./secretos/**)` | Ahí vive la clave de la pasarela de pago. Nadie la lee, ni el agente ni tú desde el agente |
| `deny Edit(./secretos/**)` | Un `deny` de lectura ya cubre editar desde la 2.1.208, pero se escribe aparte para que se vea |
| `deny Read(./.env)` y `.env.*` | Todavía no existen. La regla se pone antes que el archivo, no después |
| `deny Read(./datos/*.db)` | La base tiene nombres y pedidos de clientes reales |
| `deny Bash(curl *)` y `wget *` | Nada de este proyecto necesita bajarse cosas de internet |
| `ask Bash(git push *)` | Punto de control humano. Se cumple también en auto mode |
| `ask Bash(python app.py)` | Levanta un servidor con `debug=True` escuchando en todas las interfaces |
| `allow Bash(git status)`, `git diff *`, `pytest *` | Lo que se repite treinta veces al día y no rompe nada |

## Lo que estas reglas NO protegen

**La clave que está dentro de `app.py`.** Una regla de permisos protege rutas,
no valores. `API_KEY_PASARELA` vive en el mismo archivo que la aplicación, así
que no hay forma de denegar su lectura sin dejar ciego al agente. Sacarla del
código es trabajo del módulo 12; hasta entonces, esa clave está expuesta y
conviene saberlo.

**Lo que hace un subproceso.** `deny Read` bloquea las herramientas de archivo y
los comandos de lectura que Claude Code reconoce, como `cat`. Un
`python3 -c "print(open('secretos/pasarela.env').read())"` pasa por encima:
está comprobado en el módulo 04 del manual. Para un límite que aguante eso hace
falta el sandbox o un hook, que es el módulo 05.

## Si las reglas `allow` no se aplican

En una sesión nueva sobre un repositorio recién clonado, las entradas de
`permissions.allow` de este archivo **se ignoran** hasta que aceptes el diálogo
de confianza del espacio de trabajo. Las de `deny` y `ask` se aplican siempre.
El aviso sale por la salida de error, no por la de datos.
