# Biblioteca de skills · cinco piezas

Una skill se instala copiando su carpeta a `.claude/skills/` del proyecto, o a
`~/.claude/skills/` si la quieres en todos. El nombre de la carpeta es el nombre
del comando.

| Skill | ¿La invoca el modelo? | ¿La invocas tú? | Para qué |
|---|---|---|---|
| `auditar-endpoint` | **Sí, sola** | Sí, `/auditar-endpoint` | Revisar una ruta HTTP con criterio de auditor |
| `revisar-cambio` | No | `/revisar-cambio [base]` | El diff contra la lista del equipo antes de pedir ojos |
| `preparar-release` | No | `/preparar-release` | La secuencia de publicar, con su comprobación |
| `postmortem` | No | `/postmortem [id]` | El documento del incidente, con sus huecos honestos |
| `poner-al-dia` | No | `/poner-al-dia [fecha]` | Qué ha cambiado desde que te fuiste |

Las cuatro últimas llevan `disable-model-invocation: true`: son **los cuatro
comandos de equipo**. Se invocan a mano porque son procedimientos con momento,
no conocimiento que convenga aplicar solo.

## Lo que hay que saber antes de tocar una descripción

**La descripción es lo único que decide si la skill se dispara sola**, y solo
importa cuando la petición **no nombra la tarea**. Medido en el módulo 07 sobre
`gestor-pedidos`, con la 2.1.245, veinticuatro ejecuciones:

- Petición que nombra la tarea ("échale un vistazo al endpoint"): se dispara
  4 de 4 incluso con una descripción de catálogo de 43 caracteres.
- Petición que cuenta el síntoma ("un cliente tumba la búsqueda"): 0 de 8 con
  descripciones escritas en vocabulario de tarea, **8 de 8** cuando el síntoma
  está escrito en `when_to_use`.

De ahí la regla: **escribe la descripción con las palabras del que pide, no con
las del que cataloga.** Y ten en cuenta el tope: `description` y `when_to_use`
juntas se cortan a **1.536 caracteres**, y lo que pasa de ahí no cuesta tokens
porque no existe.

## El cuerpo es gratis, la descripción no

También medido: **20.000 caracteres añadidos al cuerpo no mueven ni un token**
por turno, porque el cuerpo se carga cuando la skill se invoca. La descripción,
en cambio, viaja en cada turno de cada sesión. Escribe corto arriba y largo
abajo.
