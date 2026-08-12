# M16 · Datos, cumplimiento y privacidad

> **Para quién es:** quien firma. El CTO, el DPO, y el tech lead al que le han preguntado en una reunión.
> **Qué resuelve:** poder contestar por escrito qué sale de aquí, adónde va y cuánto se queda.
> **Qué NO cubre:** qué arquitectura elegir (M14) ni permisos técnicos (M5).

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*

---

## 16.1 · La línea que lo separa todo: consumo frente a comercial

Es la primera pregunta que hay que responder, y mucha gente que usa esto para
trabajar está del lado equivocado sin saberlo.

**Cuentas de consumo (Free, Pro y Max):** Anthropic te da la opción de permitir
que tus datos se usen para mejorar futuros modelos. **Cuando ese ajuste está
activado, se entrena con datos de esas cuentas, incluido lo que hagas con Claude
Code desde ellas.**

**Cuentas comerciales (Team, Enterprise, API, plataformas de terceros y Claude
Gov):** Anthropic **no entrena** modelos generativos con el código ni los prompts
enviados a Claude Code bajo términos comerciales, **salvo que el cliente haya
elegido aportar sus datos**, por ejemplo mediante el programa de socios de
desarrollo.

⚠️ **La consecuencia práctica para una empresa española es directa:** si tu gente
usa **cuentas Pro personales** para trabajar en código de clientes, no estás bajo
términos comerciales. Ese es un problema de contrato antes que de tecnología, y no
se arregla con configuración.

---

## 16.2 · Cuánto se queda

| Situación | Retención |
|---|---|
| Consumo **permitiendo** uso para mejora del modelo | **5 años** |
| Consumo **sin** permitirlo | 30 días |
| Comercial (Team, Enterprise, API), estándar | 30 días |
| Enterprise con **Zero Data Retention** | Ver 16.3 |

Los ajustes de privacidad de una cuenta de consumo se cambian cuando quieras
desde los controles de privacidad de datos de la cuenta.

Cinco años frente a treinta días es una diferencia de dos órdenes de magnitud, y
depende de una casilla. Merece una comprobación explícita en el onboarding de
cualquiera que vaya a tocar código ajeno.

---

## 16.3 · Zero Data Retention, con letra pequeña

**Qué cubre:** las llamadas de inferencia hechas a través de Claude Code en Claude
for Enterprise. Los prompts que envías y las respuestas que genera Claude **no los
retiene Anthropic**. Aplica a todos los modelos disponibles para organizaciones
con ZDR, y **algunos modelos requieren retención de datos y no están disponibles
bajo ZDR**.

**Qué NO cubre**, aunque tengas ZDR activado. Estas cosas siguen las políticas
estándar de retención:

| No cubierto | Detalle |
|---|---|
| Chat en claude.ai | Las conversaciones por la interfaz web de Enterprise |
| Cowork | Las sesiones de Cowork |
| Analítica de Claude Code | No guarda prompts ni respuestas, pero **sí metadatos de productividad**: correos de cuenta y estadísticas de uso. Las métricas de contribución **no están disponibles** para organizaciones con ZDR |
| Gestión de usuarios y plazas | Datos administrativos como correos y asignación de plazas |
| **Integraciones de terceros** | **Lo que procesen herramientas de terceros, servidores MCP u otras integraciones externas no está cubierto** |

**Qué apaga.** Al activar ZDR se desactivan automáticamente, en el servidor, las
funciones que necesitan guardar prompts o respuestas: **Claude Code en la web**,
**las sesiones cloud desde la aplicación de escritorio** y **Artifacts**.

💡 **Opinión operativa.** La fila de integraciones de terceros es la que más gente
pasa por alto, y es la que más nos toca después del M8: **un servidor MCP que
conecta con un sistema de la empresa queda fuera del paraguas de ZDR**. Si has
justificado el proyecto ante legal con "tenemos ZDR", y luego conectas tres MCP de
terceros, has cambiado el perímetro sin decírselo a nadie.

---

## 16.4 · Qué sale de tu máquina aunque no uses Anthropic como proveedor

Esta es la pregunta que hace el DPO, y tiene una respuesta concreta y honesta.

En Amazon Bedrock, Agent Platform de Google, Microsoft Foundry y Claude Platform
on AWS, **el reporte de errores y la telemetría hacia Anthropic están apagados por
defecto**. Pero "apagado por defecto" no es "nada sale", y la documentación tiene
una página entera de comportamientos por proveedor.

⚠️ **El caso que hay que conocer sí o sí, porque no se puede desactivar con la
variable habitual:**

> Antes de descargar una URL, la herramienta `WebFetch` **envía el nombre de host
> solicitado a `api.anthropic.com`** para comprobarlo contra una lista de bloqueo
> de seguridad. **Solo se envía el nombre de host**, no la URL completa, ni la
> ruta, ni el contenido de la página.

Y los detalles que importan para la respuesta escrita:

- **Este chequeo corre uses el proveedor de modelo que uses.**
- **No lo afecta `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`.**
- Un host que pasa el chequeo se cachea **cinco minutos**; uno bloqueado o fallido
  se vuelve a comprobar en la siguiente petición.
- **Si tu red bloquea `api.anthropic.com`, las peticiones de `WebFetch` fallan**
  hasta que lo permitas o pongas `skipWebFetchPreflight: true`.

Poder decir esa frase completa en una reunión, con el matiz de "solo el nombre de
host", es la diferencia entre una aprobación y una revisión de seis semanas.

---

## 16.5 · Sanidad, licencia y acuerdos

La documentación cubre los **acuerdos legales** (licencia y acuerdos
comerciales), el **cumplimiento sanitario mediante BAA**, la **política de uso
aceptable** incluida la parte de autenticación y uso de credenciales, y los
canales de **confianza y seguridad**, con el procedimiento para reportar una
vulnerabilidad.

Si tu sector es sanidad, la vía es el BAA y esa conversación empieza antes de la
técnica.

---

## 16.6 · RGPD y LOPD: el guion de la conversación

No es asesoramiento legal, es el guion de lo que hay que tener contestado por
escrito antes de que lo pregunten. Cinco puntos:

**1. Qué categoría de datos toca.** El agente lee el contenido de los archivos que
abre para trabajar. Si en tu repositorio hay datos personales, en volcados, en
ficheros de prueba o en registros confirmados por error, **eso viaja**. La medida
correcta es del M5: reglas `deny` sobre esas rutas, puestas en el proyecto.

**2. Quién es el encargado del tratamiento y bajo qué contrato.** Depende de la
arquitectura del M14: suscripción comercial, API, o un proveedor cloud con su
propio contrato. **No es lo mismo y no se puede responder en genérico.**

**3. Dónde se procesa.** Con entornos self-hosted, dentro de tu red. Con cloud,
en infraestructura de Anthropic. Con un proveedor externo, donde diga ese
proveedor.

**4. Cuánto se retiene.** La tabla del 16.2, y si aplica ZDR, con sus cinco
exclusiones del 16.3.

**5. Qué sale igualmente.** El chequeo de dominio de `WebFetch` del 16.4, y la
metadata de analítica que ZDR no cubre.

Y el punto que no está en ninguna documentación pero decide auditorías: **los
servidores MCP que conectes son subencargados de facto**. Cada uno tiene su propio
tratamiento de datos y su propio contrato. La lista blanca del M8 no es solo una
medida de seguridad: es también el inventario que te van a pedir.

---

## 16.7 · La política de un folio

Todo lo anterior se queda en nada si no está escrito donde alguien lo lea. La
plantilla de política interna de uso de agentes cubre exactamente estos huecos:
proveedor contratado, plan, tratamiento de datos según contrato, rutas excluidas
por defecto, y una firma que confirma que quien la estampa **ha leído la política
de datos del proveedor y es compatible con vuestros contratos con clientes**.

Cabe en una hoja a propósito. Una política que nadie se lee no protege a nadie.

---

## Checklist de verificación

- [ ] Sé si mi equipo está en términos de consumo o comerciales.
- [ ] Nadie trabaja con código de clientes desde una cuenta Pro personal.
- [ ] Sé cuánto tiempo se retiene lo nuestro.
- [ ] Si tenemos ZDR, conozco sus cinco exclusiones.
- [ ] Sé que los servidores MCP **no** están cubiertos por ZDR.
- [ ] Puedo explicar el chequeo de dominio de `WebFetch` sin consultar nada.
- [ ] Tengo por escrito quién es el encargado del tratamiento.
- [ ] Tengo inventariados los MCP conectados, como subencargados.
- [ ] La política de una hoja está firmada y colgada.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "No entrenan con nuestro código" | Cierto en comercial. **Falso en Free, Pro y Max con el ajuste activado** |
| "Tenemos ZDR, estamos cubiertos" | No cubre analítica, gestión de plazas ni integraciones de terceros |
| "Activamos ZDR y desapareció Claude Code en la web" | Se desactiva automáticamente, junto con sesiones cloud y Artifacts |
| "Usamos Bedrock, no sale nada a Anthropic" | El chequeo de dominio de `WebFetch` sale igual |
| "Desactivé el tráfico no esencial y `WebFetch` sigue llamando" | Ese chequeo no se ve afectado por esa variable |
| "`WebFetch` falla en toda la red corporativa" | Bloqueáis `api.anthropic.com`. Permitidlo o `skipWebFetchPreflight` |
| "Los MCP están dentro de nuestro perímetro" | No, y además no los cubre ZDR. Inventaríalos |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `data-usage.md` | 21.475 | Entrenamiento, retención, chequeo de dominio de `WebFetch` |
| `zero-data-retention.md` | 8.728 | Alcance, exclusiones y funciones desactivadas |
| `security.md` | 11.794 | Modelo de seguridad |
| `legal-and-compliance.md` | 3.591 | Licencia, acuerdos, BAA, uso aceptable |
| `feature-availability.md` | 23.493 | Telemetría apagada por defecto en proveedores externos |

Material propio: la plantilla de política interna de uso de agentes.

**Marcas pendientes:** ninguna. La sección 16.6 está marcada en su encabezado como
guion operativo y **no como asesoramiento legal**, que es exactamente lo que es.
