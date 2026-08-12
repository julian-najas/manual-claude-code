# Política interna de uso de agentes de codificación

**Organización:** `_______________________`  ·  **Versión:** 1.0  ·  **Fecha:** `___ / ___ / ______`
**Responsable:** `_______________________`  ·  **Próxima revisión:** `___ / ___ / ______`

> Este documento cabe en una hoja a propósito. Una política que nadie se lee no
> protege a nadie. Rellena los huecos, tacha lo que no aplique, fírmalo y
> cuélgalo donde el equipo lo vea.

---

## 1 · Qué cubre

Esta política se aplica a cualquier agente de codificación con capacidad de
**leer o modificar** código, configuración o datos de la organización. Cubre el
uso en portátiles del equipo, en servidores y en integración continua.

No cubre el uso de asistentes de chat sin acceso al repositorio, que se rige por
`_______________________`.

## 2 · Quién puede usarlo, y sobre qué

| Entorno | Quién | Permisos | Revisión humana |
|---|---|---|---|
| Repositorio personal o de pruebas | Todo el equipo | Amplios | No hace falta |
| Repositorio de producto, rama de trabajo | Perfil `_________` en adelante | Escritura con confirmación | Antes de fusionar |
| Rama principal | Nadie directamente | Solo mediante propuesta de cambio | Obligatoria, por una persona distinta del autor |
| Integración continua | Cuenta de servicio | Solo lectura y comentarios | Obligatoria |
| Datos de clientes o producción | **Prohibido** salvo autorización escrita de `_________` | Solo lectura, entorno aislado | Obligatoria y registrada |

## 3 · Las cinco reglas que no se negocian

1. **Ningún secreto entra en el contexto.** Ni claves, ni tokens, ni volcados de
   base de datos, ni archivos `.env`. Si el agente necesita credenciales, se le
   dan por el gestor de secretos, nunca pegadas en la conversación.
2. **Nada se fusiona sin que una persona lo entienda.** Aprobar un cambio que no
   sabrías explicar en una reunión equivale a escribirlo tú a ciegas. La
   responsabilidad del código no se delega.
3. **Los permisos se deciden antes, no durante.** La configuración de permisos
   del proyecto está versionada en el repositorio. Nadie desactiva las
   comprobaciones de permisos en una máquina con acceso a producción.
4. **Todo lo que el agente toca deja rastro.** Los cambios llegan por propuesta
   de cambio, con su autoría marcada. No se sube nada directamente.
5. **Ante la duda, se para.** Cualquiera del equipo puede detener un uso
   automatizado sin pedir permiso y sin dar explicaciones previas.

## 4 · Qué sale de nuestra máquina

El agente envía a su proveedor el texto de la conversación y el contenido de los
archivos que abre para trabajar.

- Proveedor contratado: `_______________________`
- Plan y modalidad: `_______________________`
- Tratamiento de los datos según el contrato: `_______________________`
- Repositorios y rutas excluidos por defecto: `_______________________`

**Quien firme esta línea confirma que ha leído la política de datos del
proveedor y que es compatible con nuestros contratos con clientes.**

Firma: `_______________________`  Fecha: `___ / ___ / ______`

## 5 · Lo que está prohibido, sin excepciones

- Ejecutar el agente saltándose las comprobaciones de permisos en una máquina
  con acceso a producción o a datos de clientes.
- Dar al agente credenciales de escritura sobre sistemas en producción.
- Pegar en la conversación datos personales de clientes o empleados.
- Instalar servidores de conexión externa (MCP) de terceros sin revisión previa.
  El agente ejecuta lo que esos servidores le devuelven.
- Aceptar dependencias nuevas propuestas por el agente sin comprobar que existen
  y quién las publica.

## 6 · Presupuesto y control de gasto

- Presupuesto mensual por persona: `_______ €`
- Presupuesto mensual del equipo: `_______ €`
- Quien revisa el consumo y con qué periodicidad: `_______________________`
- Umbral que dispara aviso: `_______ %` del presupuesto

Regla práctica: el gasto no lo decide la tarifa del modelo, lo decide el tamaño
del contexto y el número de turnos improductivos. Se revisa mensualmente.

## 7 · Cuando algo sale mal

1. **Parar.** Detener el proceso. No intentar arreglarlo con el mismo agente.
2. **Aislar.** Revertir el cambio, revocar credenciales si estuvieron expuestas.
3. **Avisar** a `_______________________` en menos de `____` horas.
4. **Registrar** qué se pidió, qué hizo el agente, qué versión y con qué permisos.
5. **Revisar** esta política en la siguiente reunión de equipo.

Un incidente causado por un agente es un incidente de la organización. La
persona que lo lanzó no es la culpable: quien no puso el límite, sí.

## 8 · Revisión

Esta política se revisa cada `____` meses, y además siempre que cambie el
proveedor, el plan contratado o el alcance de los permisos.

---

**Aprobada por**

| Nombre | Cargo | Firma | Fecha |
|---|---|---|---|
| | | | |
| | | | |

---

<sub>Plantilla del manual "Claude Code en producción" · Cosas Agénticas · v2026.08.
Es un punto de partida, no asesoramiento legal: adáptala a tus contratos y a tu
jurisdicción antes de aplicarla.</sub>
