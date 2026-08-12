# M13 · CI/CD y revisión de código

> **Para quién es:** [C], y el tech lead que quiere revisión automática sin perder el control.
> **Qué resuelve:** poner a Claude en la tubería con presupuesto, permisos y criterio propio.
> **Qué NO cubre:** despliegue de flota ni proveedores cloud (M14).

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 13.1 · Los tres niveles de revisión, y cuál cuesta cuánto

No es una sola cosa, son tres, y elegir mal se paga en dinero o en confianza:

| | `/code-review` | `/code-review ultra` | Code Review en la PR |
|---|---|---|---|
| Objetivo | Tu diff, una PR, una rama o una ruta | Tu diff o una PR | Cada pull request |
| Dónde corre | **Local**, en tu sesión | **Remoto**, en un sandbox en la nube | En la forja |
| Profundidad | Escala con el argumento de esfuerzo | **Flota multiagente con verificación independiente** | Automática |
| Duración | Segundos a pocos minutos | **5 a 10 minutos** | Al abrir o actualizar |
| Coste | Cuenta contra tu uso normal | **Unos 5 a 25 $ por revisión** en créditos | Según plan |
| Para qué | Realimentación rápida mientras iteras | **Confianza antes de fusionar** en cambios grandes | Red de seguridad del equipo |

⚠️ **El dato de coste que nadie pone en su guía:** ultrareview es una función
premium que **factura contra créditos de uso, no contra el uso incluido en tu
plan**.

| Plan | Ejecuciones gratis | Después |
|---|---|---|
| Pro | 3 | Créditos de uso |
| Max | 3 | Créditos de uso |
| **Team y Enterprise** | **ninguna** | Créditos de uso |

Que Team y Enterprise no tengan ejecuciones gratis es contraintuitivo y conviene
saberlo **antes** de montar un flujo que lo lance en cada PR. A 5-25 $ por
revisión, un equipo de veinte personas puede construirse una factura sorprendente
en una semana.

`/review` es desde la semana 32 **un alias de `/code-review`**, y `/code-review`
sin nivel de esfuerzo **reutiliza el último que escribiste**.

---

## 13.2 · Cómo se leen los hallazgos

Cada hallazgo lleva una severidad, y las tres importan por motivos distintos:

| | Severidad | Qué significa |
|---|---|---|
| 🔴 | **Important** | Un fallo que hay que arreglar **antes de fusionar** |
| 🟡 | **Nit** | Menor, merece la pena pero no bloquea |
| 🟣 | **Pre-existing** | Un fallo que ya estaba en el código y **no lo introdujo esta PR** |

La tercera es la que hace que el sistema sea usable en un repositorio con
historia: sin ella, la primera revisión de un proyecto legacy sería un muro de
mil hallazgos y nadie volvería a mirarla.

Cada hallazgo trae además una sección plegable con **el razonamiento extendido**:
por qué lo marcó y cómo verificó el problema. Es lo que permite discutirlo en vez
de acatarlo.

---

## 13.3 · `REVIEW.md`, o cómo se calibra un revisor

Un archivo en la raíz del repositorio que **anula cómo se comporta Code Review en
tu repo**. Su contenido se inyecta en el system prompt de **todos los agentes de
la tubería de revisión** como **bloque de instrucciones de máxima prioridad**, por
encima de la guía de revisión por defecto.

⚠️ **La trampa, y es de las que cuestan una tarde:** se pega **literalmente**. La
sintaxis de import con `@` **no se expande** y los archivos referenciados **no se
leen**. Si escribes `@docs/estandares.md` esperando que se cargue, lo que has
metido en el prompt es el texto `@docs/estandares.md`. **Las reglas van dentro del
archivo, escritas.**

Lo que más rinde calibrar:

- **Qué significa 🔴 Important en tu repo.** La calibración por defecto apunta a
  código de producción; un repositorio de documentación, uno de configuración o un
  prototipo quieren algo mucho más estrecho.
- **Poner tope a los nits**, para que la señal no se ahogue.
- **Qué no reportar nunca.**
- **Qué comprobar siempre.**

💡 **Opinión operativa.** El `REVIEW.md` es la pieza que convierte la revisión
automática de un ruido que el equipo aprende a ignorar en algo que se lee. Si tu
gente ha empezado a cerrar los comentarios sin mirarlos, el problema no es la
herramienta: es que nadie ha calibrado qué es importante **aquí**.

---

## 13.4 · GitHub Actions: los dos modos

La acción **detecta sola cómo tiene que correr**, según lo que le pongas en el
flujo de trabajo:

- **Modo interactivo**, cuando el flujo **no** lleva entrada `prompt`: Claude
  espera la frase disparadora, `@claude` por defecto, en un comentario de
  incidencia o de pull request, en una revisión de PR, o en el cuerpo o el título
  de una incidencia recién abierta. El progreso y el resultado aparecen **como
  comentario**.
- **Modo automatización**, cuando el flujo **sí** lleva `prompt`: corre sin
  esperar a que la mencionen. El resultado aparece **en el registro de la
  ejecución**, no como comentario.

Esa diferencia de dónde aparece el resultado es más importante de lo que parece:
en modo automatización, si nadie mira el registro, es como si no hubiera corrido.

---

## 13.5 · Quién puede dispararla

En los dos modos, la acción hace **dos comprobaciones sobre quien la dispara**
antes de que Claude arranque, y **la ejecución falla si cualquiera de las dos la
rechaza**:

1. **Acceso de escritura.** En eventos de incidencia y de pull request, quien
   dispara **debe tener acceso de escritura al repositorio**. Para permitir a
   personas concretas sin escritura, `allowed_non_write_users` y pasar tu propio
   `github_token`. Los eventos que no tienen autor, como un disparo programado,
   **se saltan esta comprobación**.
2. **Actor humano.** En **todos** los eventos, **se rechaza a un actor que sea un
   bot**, salvo que lo listes en `allowed_bots`.

Las dos juntas son la respuesta a la pregunta que hará seguridad: **no, un
desconocido no puede hacer que tu CI ejecute a Claude comentando en una
incidencia**. Y la segunda cierra el encadenamiento de bots, que es el vector
menos obvio.

---

## 13.6 · La app de GitHub y sus permisos

Un detalle de honestidad que la documentación declara y conviene trasladar tal
cual, porque lo va a preguntar quien apruebe la instalación:

> La app de GitHub de Claude **la comparten todas las funciones de Claude que se
> integran con GitHub**: la acción de GitHub, Code Review y el auto-arreglo de
> pull requests en Claude Code en la web. Una app de GitHub tiene **un único
> conjunto de permisos que cubre todas sus funciones**, así que el conjunto
> incluye **algunos permisos que la acción no usa**.

Traducción para la reunión con seguridad: al instalar concedes el superconjunto,
no el mínimo de la función que te interesa. No es un fallo, es cómo funcionan las
apps de GitHub, pero **hay que decirlo antes y no cuando alguien lo descubra**.

---

## 13.7 · Fuera de GitHub

- **GitLab CI/CD** tiene su propia integración documentada.
- **GitHub Enterprise Server**, para instalaciones autoalojadas de la forja.
- **Proveedores cloud en Actions**, para cuando el modelo no viene de la API de
  Anthropic sino de Bedrock, Agent Platform o Foundry. Eso enlaza con el M14.

---

## 13.8 · Los dos plugins de seguridad, que no son lo mismo

| | `security-guidance` | `claude-security` |
|---|---|---|
| Cuándo actúa | **Mientras Claude escribe**, en la sesión | **Bajo demanda**, escaneando |
| Qué hace | Revisa sus propios cambios y **arregla en la misma sesión** | Escaneo multiagente de vulnerabilidades |
| Alcance | Lo que se está tocando | Todo el repositorio, o solo un diff, una PR o un commit |
| Cómo se usa | **Automático, no hay que invocar nada** | Se lanza y produce hallazgos |
| Salida | Correcciones sobre la marcha | Hallazgos que **tú** conviertes en parches y aplicas |

El primero caza inyección, deserialización insegura y APIs del DOM peligrosas
**antes de que el código llegue a una pull request**, que es donde sale barato.

El segundo hace algo más ambicioso: un equipo de agentes **mapea tu arquitectura,
construye un modelo de amenazas, busca vulnerabilidades y revisa cada hallazgo de
forma independiente** antes de escribir el informe. Corre en local.

La combinación correcta es la de un equipo maduro: `security-guidance` siempre
puesto, `claude-security` antes de una release o cuando se toca algo sensible, y
Code Review en la PR como red.

---

## 13.9 · Qué automatizar y qué no

**Sí, automatiza:**

- Revisión en cada pull request, calibrada con `REVIEW.md`.
- Comprobaciones que devuelven pasa o falla, del M6.
- Que la CI **falle si un plugin no carga**, del M10. Sin eso, tu automatización
  puede estar sin correr y nadie enterarse.
- Tareas programadas para trabajo tedioso y acotado.

**No automatices, y esto es criterio propio:**

- **Fusionar.** La revisión automática informa la decisión, no la toma.
- **Ultrareview en cada push.** A 5-25 $ la pasada, es para antes de fusionar
  cambios sustanciales, no para cada commit.
- **Nada con credenciales de escritura en producción**, del M5.
- **Lo que nadie va a leer.** Un informe automático que llega a un canal que todo
  el mundo silencia es gasto puro.

---

## Checklist de verificación

- [ ] Sé qué me cuesta cada nivel de revisión.
- [ ] Sé que Team y Enterprise **no** tienen ejecuciones gratis de ultrareview.
- [ ] Tengo un `REVIEW.md` que dice qué es importante **en mi repo**.
- [ ] Sé que en `REVIEW.md` los imports con `@` no se expanden.
- [ ] Sé en qué modo corre mi acción y dónde aparece su resultado.
- [ ] He explicado a quien aprueba la app que el permiso es un superconjunto.
- [ ] Mi CI falla si un plugin no carga.
- [ ] Nadie fusiona por aprobación automática.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "La revisión no aplica nuestras reglas" | Falta `REVIEW.md`, o pusiste un `@import` que no se expande |
| "La primera revisión del legacy es un muro" | Para eso está 🟣 Pre-existing. Calibra con `REVIEW.md` |
| "Corre pero no veo nada" | Modo automatización: el resultado va al registro, no a un comentario |
| "A un compañero le falla siempre el disparo" | No tiene acceso de escritura. `allowed_non_write_users` |
| "Nuestro bot no puede dispararla" | Se rechazan los bots salvo los de `allowed_bots` |
| "Factura de ultrareview disparada" | Lo estáis lanzando en cada push. Es para antes de fusionar |
| "Seguridad nos ha parado la instalación" | Explica antes que el permiso de la app es un superconjunto |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `code-review.md` | 31.690 | Severidades, `REVIEW.md`, qué revisa |
| `ultrareview.md` | 17.537 | Comparativa, precio y ejecuciones gratis |
| `github-actions.md` | 30.827 | Los dos modos, quién dispara, permisos de la app |
| `github-actions-cloud-providers.md` | 19.148 | Actions con Bedrock, Agent Platform y Foundry |
| `github-enterprise-server.md` | 23.391 | Forja autoalojada |
| `gitlab-ci-cd.md` | 18.880 | GitLab |
| `security-guidance.md` | 20.987 | Revisión en sesión |
| `claude-security.md` | 13.547 | Escaneo multiagente |
| `whats-new/2026-w32.md` | 8.830 | `/review` como alias |

**Marcas pendientes:** ninguna. La sección 13.9 está marcada como criterio propio
en su encabezado, no como documentación.
