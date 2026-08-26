# Subagentes de este repositorio

Uno solo, `revisor`, en `.claude/agents/revisor.md`. Aquí está por qué su
contrato está escrito así, lo que cuesta, y **qué no va a reportar nunca**, que
es la parte que hay que leer antes de fiarse de él.

## Qué es y quién lo invoca

Es un revisor con ventana de contexto propia: no ve nuestra conversación, no ve
lo que el agente principal ya ha leído, y lo único que vuelve a la sesión es su
informe. Lo invoca el modelo cuando la tarea encaja, y también se puede pedir por
su nombre.

Es de **solo lectura** a propósito: `tools: Read, Grep, Glob`. Un revisor que
puede editar arregla lo primero que ve, y entonces lo que vuelve no es un informe
sino un cambio que nadie ha revisado.

## Por qué el contrato está escrito así

Porque el aislamiento por sí solo no aporta criterio. Medido sobre este mismo
`app.py`, con la 2.1.246 y Sonnet 5, dos repeticiones por fila:

| Quién revisa | Fallo 2, inyección | Fallo 3, responsabilidades | Fallo 4, IVA por defecto |
|---|---|---|---|
| El agente principal, "revisa app.py" | 2 de 2 | 0 de 2 | 0 de 2 |
| Subagente con contrato de auditor | 2 de 2 | 0 de 2 | 1 de 2 |
| Subagente con **criterio de aceptación en tres preguntas** | 2 de 2 | **2 de 2** | **2 de 2** |

La única variable entre la segunda fila y la tercera es el criterio de
aceptación: las tres preguntas que el informe está obligado a contestar. Ninguna
nombra un fallo; nombran dónde mirar.

## Lo que le esconde el `CLAUDE.md`

**La jerarquía de memoria entera llega al subagente**, igual que a la sesión
principal. Y el `CLAUDE.md` de este repositorio termina diciendo que no hace
falta avisar de los fallos inventariados. Consecuencia, medida quitando ese
párrafo y solo ese, 309 caracteres:

| `CLAUDE.md` | ¿Reporta `API_KEY_PASARELA`? |
|---|---|
| Tal cual | **0 de 2**, y lo dice en la primera línea del informe |
| Sin el último párrafo | **2 de 2**, como hallazgo bloqueante |

Por eso el contrato del revisor lleva una línea explícita que le dice que no
acepte esa instrucción. **Si alguien añade otra frase de ese tipo al `CLAUDE.md`,
hay que volver a comprobar esta tabla.**

## Lo que cuesta

- Declarado y sin usarse: **~105 tokens por turno**. La mitad que la skill de
  `SKILLS.md`.
- Su prompt de sistema: **cero** hasta que se invoca. Comprobado con 21.228
  caracteres y el mismo número exacto de tokens.
- Su descripción: se paga entera y **no tiene tope**, al contrario que la de una
  skill. Cinco mil caracteres ahí son más de dos mil tokens en cada turno.
- Ejecutarlo: la ventana de la sesión principal baja de ~146.000 tokens a
  ~54.000, y la factura de la ejecución **sube al doble**.

## Cómo comprobar que sigue vivo

```bash
claude -p "Delega en el subagente revisor la revisión de app.py y devuélveme su informe tal cual." \
  --allowedTools "Read,Grep,Glob,Agent" \
  --output-format stream-json --verbose \
  | jq -r 'select(.type=="assistant") | .message.content[]?
           | select(.type=="tool_use") | .name'
```

Tiene que salir `Agent`. Si no sale, el informe lo escribió la sesión principal y
no hay segunda opinión, solo una factura.
