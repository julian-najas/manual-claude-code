# Contenedor de desarrollo con red restringida

Plantilla del módulo 04 del manual. Es el aislamiento que hace defendible
`--dangerously-skip-permissions`, y no lo es sin las tres piezas juntas.

| Pieza | Qué aporta | Qué pasa si falta |
|---|---|---|
| `remoteUser` distinto de root | El CLI se niega a arrancar con la bandera peligrosa como root | La bandera no funciona, y con razón |
| `NET_ADMIN` y `NET_RAW` | Permiten levantar el cortafuegos dentro del contenedor | El script no puede escribir reglas |
| Script de cortafuegos | Deniega todo salvo los dominios que necesitas | El contenedor aísla el disco y no la red, que es media protección |

El script de referencia es `init-firewall.sh` del repositorio
`anthropics/claude-code`, en `.devcontainer/`. Ni el script ni las dos
capacidades son obligatorios para que Claude Code funcione: son obligatorios
para que el contenedor sea un límite y no un decorado.

## Lo que este contenedor NO protege

- **Los archivos del proyecto.** Están montados y se escriben en tu disco.
- **Las credenciales que metas dentro.** Con la bandera peligrosa puesta, todo
  lo que el contenedor alcance es alcanzable. No montes `~/.ssh` ni archivos de
  credenciales de nube: usa fichas de vida corta y de alcance acotado.
- **Lo que sale hacia el modelo.** El aislamiento no cambia qué se envía.

## Persistir la sesión entre reconstrucciones

El volumen montado en `~/.claude` no basta: la cuenta y la confianza por
proyecto viven en `~/.claude.json`, **fuera** de ese directorio. Por eso la
plantilla fija `CLAUDE_CONFIG_DIR` al mismo destino del volumen.
