---
name: preparar-release
description: >
  Prepara una release: comprueba el estado del repositorio, que las pruebas
  pasan, que no hay secretos en el diff y que el changelog está al día, y
  redacta las notas de versión. Úsala cuando pidan preparar, sacar o publicar
  una release, una versión o un tag.
disable-model-invocation: true
allowed-tools: Bash(git *) Read Grep
---

# Preparar una release

`disable-model-invocation: true` a propósito: esto lo lanza una persona, nunca se
activa solo. Como efecto secundario, su descripción no ocupa contexto hasta que la
invocas.

## Estado actual del repositorio

Estos comandos se ejecutan **antes** de que este contenido llegue al modelo, así
que los datos ya vienen dentro:

Rama y estado:
!`git status --short --branch`

Último tag y commits desde entonces:
!`git describe --tags --abbrev=0 2>/dev/null || echo "(sin tags)"`
!`git log $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~20)..HEAD --oneline 2>/dev/null | head -40`

Comprobaciones automáticas:
!`bash "${CLAUDE_PROJECT_DIR:-.}/.claude/skills/preparar-release/scripts/comprobar.sh"`

## Instrucciones permanentes

1. **Si alguna comprobación de arriba dice FALLA, para.** Di qué falla y no
   redactes notas de una release que no debería salir.
2. Redacta las notas agrupando por **qué cambia para quien lo usa**, no por commit.
3. Marca aparte los **cambios que rompen**, con qué hay que hacer para migrar.
4. Propón el número de versión y **justifícalo**: parche, menor o mayor.
5. **No etiquetes ni publiques nada.** Eso lo hace una persona.
