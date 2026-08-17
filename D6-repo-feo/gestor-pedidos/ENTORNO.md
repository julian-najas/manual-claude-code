# Entorno de herramientas

Este archivo existe para que dos personas de este proyecto puedan comparar sus
máquinas sin adivinar. Se actualiza cuando cambia el suelo de versión, no cada
vez que alguien se actualiza.

| Dato | Valor | Cómo se comprueba |
|---|---|---|
| Claude Code, versión de referencia | 2.1.233 | `claude --version` |
| Suelo de versión del proyecto | 2.1.233 | `.claude/settings.json` → `minimumVersion` |
| Canal de actualización | `stable` | `.claude/settings.json` → `autoUpdatesChannel` |
| Método de instalación esperado | nativo | `claude doctor` → `Config install method` |
| Fecha de la anotación | 17 de agosto de 2026 | este archivo |

## Si algo se comporta distinto en tu máquina

Antes de abrir una discusión, pega la salida de estos tres comandos:

```bash
claude --version
claude doctor
claude auth status
```

`claude auth status` devuelve JSON con la cuenta y la organización activas.
**Contiene datos personales: quita el correo y el identificador de organización
antes de pegarlo en ningún sitio compartido.**

## Reproducir la versión de referencia

```bash
curl -fsSL https://claude.ai/install.sh | bash -s 2.1.233
```

Instalar una versión concreta no borra las demás: quedan bajo
`~/.local/share/claude/versions/` y el lanzador del `PATH` apunta a la que toca.

## Aviso

Este repositorio es material de laboratorio del manual "Claude Code en
producción". Tiene fallos de seguridad deliberados. No lo despliegues.
