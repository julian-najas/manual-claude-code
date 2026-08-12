# M12 · Superficies

> **Para quién es:** equipos mixtos, y quien tiene que decir "esto aquí no se puede".
> **Qué resuelve:** qué se puede hacer desde dónde, sin descubrirlo a mitad de una tarea.
> **Qué NO cubre:** CI y forjas (M13) ni arquitectura de despliegue (M14).

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 12.1 · Dos ejes que la gente colapsa en uno

Del M1, y aquí es donde se aplica: **dónde se ejecuta** y **desde dónde lo
pilotas** son independientes.

Una sesión puede correr en tu máquina y pilotarla desde el móvil. Puede correr en
la nube y pilotarla desde el terminal. Confundir los dos ejes produce preguntas
sin respuesta como "¿el móvil tiene acceso a mis archivos?", que depende
enteramente de dónde corra la sesión, no del móvil.

**El móvil, de hecho, es el ejemplo perfecto:** la aplicación de Claude para iOS y
Android **es un cliente de sesiones, no un sitio donde corre código**. Y no hay
aplicación móvil separada de Claude Code: las sesiones cloud y Remote Control
viven en la pestaña **Code** de la app de Claude, y Dispatch es una tarea a la que
le escribes.

---

## 12.2 · Tabla 1 · Paridad por superficie

| Superficie | Dónde ejecuta | Lo que aporta | Lo que no tienes |
|---|---|---|---|
| **CLI** | Tu máquina | **Conjunto completo**, Agent SDK, proveedores externos, computer use en macOS | Nada. Es la referencia |
| **Desktop** | Tu máquina | Visor de diffs, vista previa de la app, computer use y Dispatch en Pro y Max | Requiere suscripción |
| **VS Code** | Tu máquina | Diffs en línea, terminal integrada, contexto de archivos | Requiere suscripción |
| **JetBrains** | Tu máquina | Visor de diffs, compartir selección, sesión de terminal | Requiere suscripción |
| **Web** | **Nube**, gestionada por Anthropic | Tareas largas que siguen aunque te desconectes | Sin acceso a tu disco. Requiere suscripción. **Se apaga con ZDR** |
| **Móvil** | Nube, o tu máquina vía Remote Control | Arrancar y vigilar desde fuera | Es un cliente: no ejecuta nada |
| **Slack** | Nube | Delegar desde el chat | **En retirada en Team y Enterprise** |
| **Chrome** | Tu máquina | Automatización de navegador desde CLI o VS Code | Requiere la extensión |

Y la capa que atraviesa la tabla, del M14: **todo lo que no sea el CLI puro
requiere suscripción de Claude**. Con clave de API o proveedor externo, la columna
de superficies se reduce drásticamente.

### Estado de madurez, que hay que decir

| Función | Estado |
|---|---|
| **Computer use** | **Research preview**, solo macOS, **solo Pro y Max**, **no en Team ni Enterprise**, **no en modo no interactivo** |
| **Remote Control** | **Research preview**, todos los planes. En Team y Enterprise **apagado por defecto** hasta que un propietario lo active |
| **Routines** | **Research preview**. Comportamiento, límites y API pueden cambiar |
| **Agent view** | **Research preview** (M9) |
| **Renderizado a pantalla completa** | **Research preview** (M7) |
| **Entornos self-hosted** | **Beta pública**, Team y Enterprise, apagado por defecto (M14) |

Seis funciones en preview o beta. No es una crítica: es que un equipo que apoya un
proceso crítico sobre cualquiera de ellas debería saberlo, y en la mayoría de
guías aparecen como si fueran producto estable.

---

## 12.3 · El terminal sigue siendo la referencia

El CLI tiene **el conjunto completo de funciones**, es el único con Agent SDK, el
único que habla con proveedores externos y el único donde funciona el modo no
interactivo que sostiene todo el M10 y el M13.

💡 **Opinión operativa.** Toda la documentación que escribas para tu equipo debería
tener el CLI como referencia y describir las otras superficies **por diferencia**.
Al revés se produce el efecto contrario al buscado: gente que aprende en la IDE y
se queda sin la mitad de la herramienta porque nunca supo que existía.

---

## 12.4 · Las IDE

**VS Code** aporta diffs en línea, terminal integrada y contexto de archivos. En la
semana 32 ganó **Focus view**, que esconde la actividad de herramientas tras una
fila desplegable por turno, con `Ctrl+Alt+F` o `Ctrl+Option+F` en Mac.

**JetBrains** cubre IntelliJ, PyCharm, WebStorm y el resto: visor de diffs,
compartir selección y sesión de terminal.

Las dos resuelven el mismo problema, que es no cambiar de ventana, y **ninguna
sustituye al terminal** para lo automático.

---

## 12.5 · Escritorio

Su valor propio es **la revisión visual y las sesiones en paralelo**: visor de
diffs, vista previa de la aplicación, y **computer use y Dispatch en Pro y Max**.
Tiene además páginas propias para Linux, WSL, tareas programadas y simulador de
iOS.

Del M10: las **tareas programadas de escritorio** son la opción intermedia entre
`/loop`, que necesita sesión abierta, y las routines en la nube, que no necesitan
ni máquina encendida: corren en tu máquina, con acceso a tus archivos, **sin
sesión abierta** y con intervalo mínimo de un minuto.

---

## 12.6 · Web y sesiones en la nube

Su caso de uso es preciso: **tareas largas que no necesitan mucha dirección, o
trabajo que debe continuar cuando te desconectas**. Corren en infraestructura
gestionada por Anthropic **por defecto**, o dentro de tu red si tu organización
tiene un entorno self-hosted del M14.

Dos límites que hay que tener presentes: **no ven tu disco**, porque trabajan
sobre un clon; y del M16, **se desactivan automáticamente bajo ZDR**, junto con
las sesiones cloud desde escritorio y Artifacts.

---

## 12.7 · Móvil y Remote Control

**Remote Control** conecta claude.ai/code o la app de Claude **a una sesión que
corre en tu máquina**. Empiezas en el escritorio y sigues desde el sofá.

Tres cosas que hay que saber antes de prometérselo a un equipo:

1. Es **research preview**.
2. En **Team y Enterprise está apagado por defecto** hasta que un propietario
   active el interruptor en la configuración de administración.
3. Del M3: **la configuración confirmada en un repositorio ya no puede activar la
   conexión automática de Remote Control**. Se fija en los settings de usuario o
   gestionados, y los de proyecto y local **solo pueden desactivarla**. Es un
   endurecimiento de la semana 32 y va en la dirección correcta: un repositorio
   ajeno no puede abrirte un canal remoto.

Del M9, y encaja aquí: desde **v2.1.225**, `SendMessage` puede **iniciar**
conversación con tus sesiones de Remote Control en otras máquinas llamándolas por
nombre.

---

## 12.8 · Slack, y una retirada que hay que anunciar

⚠️ **Cambio importante que pertenece también al M21.** La versión actual de Claude
Code en Slack, que corre cada sesión **bajo la cuenta de un usuario individual**,
**está siendo retirada en los planes Team y Enterprise** en favor de **Claude
Tag**, que ejecuta `@Claude` como **identidad compartida de la organización** con
acceso configurado por administración.

Para quien ya lo tiene: la aplicación de Slack y el identificador `@Claude` se
quedan, y la fecha de corte la da el equipo de cuenta de Anthropic. **En Pro y Max
sigue siendo la vía de instalación**.

Que el cambio vaya de "identidad individual" a "identidad compartida con control
de administración" no es cosmético: es exactamente el tipo de cosa que decide si
seguridad aprueba el canal.

---

## 12.9 · Chrome y computer use

**Chrome** da automatización de navegador desde el CLI o desde la extensión de VS
Code: probar aplicaciones web, depurar con los registros de consola, rellenar
formularios, extraer datos.

⚠️ **Y el aviso de seguridad, que es literal y hay que trasladar sin suavizar:**

> Claude abre pestañas nuevas y **comparte el estado de sesión de tu navegador**,
> así que **puede acceder a cualquier sitio en el que ya estés identificado**.

Es decir: tu banco, tu panel de administración, tu correo. Las acciones ocurren en
una ventana visible y en tiempo real, y cuando encuentra una pantalla de acceso o
un CAPTCHA se detiene y te pide que lo resuelvas tú. Pero la superficie es tu
sesión entera del navegador. Eso pertenece a la conversación del M5, no a la de
comodidad.

**Computer use** deja que Claude abra aplicaciones, controle la pantalla y trabaje
en tu máquina como lo harías tú: compilar una app, lanzarla, pulsar cada botón y
capturar el resultado, todo en la misma conversación donde escribió el código. Con
los cuatro límites de la tabla del 12.2, y el que más sorprende: **no está en
Team ni en Enterprise**.

---

## 12.10 · Routines

Una routine es **una configuración de Claude Code guardada**: un prompt, uno o
varios repositorios y un conjunto de conectores, empaquetados una vez y ejecutados
automáticamente. Corren en infraestructura gestionada por Anthropic, **o en el
entorno self-hosted de tu organización** si se enrutan ahí, así que **siguen
funcionando con el portátil cerrado**.

Sus disparadores son tres: **programado** (cadencia recurrente o una vez en un
momento futuro), **API**, y **eventos de GitHub**. Es la pieza que convierte
"automatización" en algo que no depende de que alguien tenga una terminal abierta.

Research preview: comportamiento, límites y superficie de la API pueden cambiar.

---

## Checklist de verificación

- [ ] Sé distinguir dónde corre una sesión de desde dónde la piloto.
- [ ] Mi documentación interna toma el CLI como referencia y describe el resto por diferencia.
- [ ] El equipo sabe qué seis funciones están en preview o beta.
- [ ] Sé que computer use no existe en Team ni en Enterprise.
- [ ] Si uso Remote Control en Team, un propietario lo ha activado a sabiendas.
- [ ] He avisado de la retirada de Slack en favor de Claude Tag.
- [ ] Todo el mundo sabe que Chrome comparte la sesión del navegador.
- [ ] Sé que las sesiones web se apagan bajo ZDR.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "Desde el móvil no veo mis archivos" | El móvil es un cliente. Depende de dónde corra la sesión |
| "Busco la app de Claude Code y no existe" | No hay app separada: pestaña **Code** de la app de Claude |
| "Computer use no me aparece" | Research preview, macOS, solo Pro y Max, y no con `-p` |
| "Remote Control no conecta en la empresa" | Apagado por defecto en Team y Enterprise |
| "Puse la conexión automática en el repo y no funciona" | Desde la w32, el repositorio solo puede desactivarla |
| "Activamos ZDR y desapareció la web" | Se desactiva automáticamente |
| "Nuestro Slack va a dejar de funcionar" | Retirada en Team y Enterprise en favor de Claude Tag |
| "Claude entró en un panel donde yo estaba logueado" | Comparte el estado de sesión del navegador. Por diseño |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `platforms.md` | 12.360 | Tabla 1, dónde correr y qué aporta cada una |
| `desktop.md` | 96.593 | Escritorio, Dispatch, computer use |
| `vs-code.md` | 50.584 | VS Code y Focus view |
| `jetbrains.md` | 12.389 | JetBrains |
| `claude-code-on-the-web.md` | 37.038 | Sesiones en la nube |
| `mobile.md` | 8.690 | El móvil como cliente |
| `remote-control.md` | 48.861 | Research preview y activación |
| `slack.md` | 15.771 | Retirada en favor de Claude Tag |
| `chrome.md` | 17.323 | Automatización y el aviso de sesión compartida |
| `computer-use.md` | 12.836 | Límites de plan y de modo |
| `routines.md` | 33.540 | Los tres disparadores |
| `feature-availability.md` | 23.493 | Qué requiere suscripción |
| `whats-new/2026-w32.md` | 8.830 | Focus view y el endurecimiento de Remote Control |

**Marcas pendientes:** las páginas de detalle de escritorio (Linux, WSL, tareas
programadas, simulador de iOS) están inventariadas y no leídas en profundidad;
alimentan el M20 y no sostienen afirmaciones de este módulo más allá de su
existencia.
