---
name: poner-al-dia
description: Resume qué ha cambiado en el repositorio desde una fecha, para quien vuelve de vacaciones o entra nuevo.
disable-model-invocation: true
argument-hint: "[fecha-o-rama]"
allowed-tools: Bash(git log *) Bash(git diff *) Read
---

# Poner al día desde $1

Para quien vuelve y no quiere leerse doscientos commits.

1. `git log --oneline --since="$1"` y agrúpalo **por tema**, no por autor ni por
   orden cronológico.
2. De cada tema: qué cambió, en qué archivos, y **qué hay que saber para no
   pisarlo**.
3. Marca aparte, con encabezado propio:
   - **Cambios de contrato**: API, esquema de base de datos, formato de
     configuración. Lo que rompe a quien no se entere.
   - **Cosas a medias**, con la rama donde viven.
4. Cierra con **tres cosas que mirar primero** si mañana algo falla.

Máximo una página. Si no cabe, es que hay que agrupar mejor, no escribir más.
