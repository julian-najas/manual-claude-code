---
name: revisar-cambio
description: Revisa el diff actual contra la lista de comprobación del equipo antes de pedir revisión humana.
disable-model-invocation: true
argument-hint: "[rama-base]"
allowed-tools: Bash(git diff *) Bash(git status) Read Grep
---

# Revisar el cambio antes de pedir ojos ajenos

Comando de equipo: lo invocas tú con `/revisar-cambio`. No se dispara solo, a
propósito, porque revisar a destiempo cuesta contexto y no aporta.

1. `git diff --stat` contra la rama base (`$1`, o la de por defecto si no se da).
2. Por cada archivo tocado, y **solo** por lo que el diff cambia:
   - ¿Hay algo que el diff rompe y que no está cubierto por un test?
   - ¿Se ha colado una credencial, una ruta absoluta o una URL interna?
   - ¿Queda algún `TODO`, `print` o `console.log` de depuración?
   - ¿El mensaje de commit describe lo que hace el diff, no lo que se intentaba?
3. Separa **lo que introduce este cambio** de lo que ya estaba mal. Lo segundo
   se anota, no se arregla aquí.
4. Termina con una de estas dos líneas y nada más: `LISTO PARA REVISIÓN` o
   `NO LISTO`, seguida de la lista de lo que falta.

No edites archivos. Este comando informa.
