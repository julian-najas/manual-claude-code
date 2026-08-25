# Skills de este repositorio

Una sola skill, `.claude/skills/auditar-endpoint/`. Aquí está por qué está
escrita así, lo que cuesta y cuándo no se dispara.

## Qué es y quién la invoca

Es conocimiento con procedimiento: cómo se audita una ruta de **esta**
aplicación, con los siete puntos que aquí importan. La invoca el modelo cuando
la tarea encaja, y tú también con `/auditar-endpoint`.

## Por qué la descripción está escrita así

Porque es lo único que decide si se dispara sola. Medido sobre este mismo
repositorio, con la 2.1.245, cuatro repeticiones por fila:

| Lo que pide el usuario | Descripción de la skill | Se disparó |
|---|---|---|
| "Échale un vistazo al endpoint /buscar" | de catálogo, 43 caracteres | 4 de 4 |
| lo mismo | de tarea, 380 caracteres | 4 de 4 |
| "Un cliente O'Brien tumba la búsqueda" | de catálogo | 0 de 4 |
| lo mismo | de tarea | 0 de 4 |
| lo mismo | con el **síntoma** en `when_to_use` | **8 de 8** |

Por eso el `when_to_use` de esta skill habla de apóstrofes, de búsquedas que
fallan y de clientes que tumban la app: son las palabras con las que llega el
problema, no las palabras con las que se clasifica la tarea.

## Lo que cuesta

- Instalada y sin usarse: **208 tokens por turno**, que es lo que ocupa su
  frontmatter.
- El cuerpo: **cero** hasta que se invoca. Comprobado añadiéndole 20.000
  caracteres y midiendo el mismo número exacto.
- `description` y `when_to_use` juntas se cortan a **1.536 caracteres**.

## Lo que no hace

Que la skill se cargue no significa que se cumpla. Su cuerpo pide empezar la
respuesta por `AUDITORIA-GESTOR-PEDIDOS`, y en las ocho ejecuciones con disparo
automático salió **tres veces**. Una skill es contexto, no un candado. Lo que no
sea negociable va en un hook, como los dos de `HOOKS.md`.

## Cómo comprobar que sigue viva

```bash
claude -p "Un cliente que se llama O'Brien hace que la busqueda de la app falle. Dime que esta pasando." --allowedTools "Read,Grep,Glob"
```

Tiene que auditar el endpoint, no solo explicar el apóstrofe. Si solo explica el
apóstrofe, alguien ha tocado el `when_to_use`.
