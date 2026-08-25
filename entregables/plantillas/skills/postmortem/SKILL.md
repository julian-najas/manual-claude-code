---
name: postmortem
description: Redacta el postmortem de un incidente con la plantilla del equipo, sin buscar culpables.
disable-model-invocation: true
argument-hint: "[identificador-del-incidente]"
allowed-tools: Read Grep Glob Bash(git log *)
---

# Postmortem del incidente $1

Escribe el documento con estas secciones y en este orden. Si un dato no lo
tienes, escribe **"no consta"**: un postmortem con huecos honestos vale, uno con
huecos rellenados a ojo no.

1. **Qué vio el usuario**, en una frase, sin jerga.
2. **Cronología**, en UTC, desde el primer síntoma hasta la vuelta a la
   normalidad. Cada línea con su fuente: registro, alerta o persona.
3. **Causa técnica**, con el archivo y la función. Una causa, no cinco.
4. **Por qué no se detectó antes.** Esta sección suele ser la útil.
5. **Qué se ha cambiado ya** y **qué falta**, cada punto con responsable y fecha.
6. **Lo que no se va a hacer**, y por qué. Sin esta sección la lista de acciones
   es una lista de deseos.

Reglas: sin nombres propios en las causas, los sistemas fallan por diseño;
tiempo en UTC; y nada de "error humano" como causa raíz.
