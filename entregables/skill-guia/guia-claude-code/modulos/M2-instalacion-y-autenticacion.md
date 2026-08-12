# M2 · Instalación, autenticación y actualización

> **Para quién es:** quien monta la máquina, la suya o la de veinte personas.
> **Qué resuelve:** un entorno reproducible y saber siempre contra qué versión trabajas.
> **Qué NO cubre:** despliegue de flota, proveedores cloud ni gateways (M14).

*Verificado contra Claude Code 2.1.228 el 12 de agosto de 2026.*
*Este módulo se escribió el último a propósito: es el que más rápido envejece.*

---

## 2.1 · Instaladores

Hay varias vías y **no son equivalentes**, sobre todo en cómo se actualizan:

| Vía | Notas |
|---|---|
| **Nativa** | La recomendada. Instala un binario propio y gestiona sus versiones |
| **Homebrew** | En macOS. Las actualizaciones las lleva Homebrew, no Claude Code |
| **WinGet** | En Windows |
| **Gestores de Linux** | apt, dnf, apk |
| **npm** | Sigue disponible |

La documentación cubre además **instalar una versión concreta**, que es lo que
necesitas para reproducir un fallo o para fijar una máquina de CI.

---

## 2.2 · Anatomía de una instalación nativa

Merece verse una de verdad, porque explica cómo funcionan las actualizaciones.
Esta es la de la máquina donde se ha escrito esta guía:

```
~/.local/bin/claude  →  ~/.local/share/claude/versions/2.1.228
```

**El comando del `PATH` es un enlace simbólico a una versión concreta.** Actualizar
es instalar una versión nueva al lado y mover el enlace, por eso una actualización
no rompe una sesión que ya está corriendo.

⚠️ Y de ahí sale la trampa del lanzador corporativo del M14: **los procesos que
Claude Code lanza desde su propio binario arrancan por la ruta directa**, no
consultando el `PATH`, así que un lanzador que envuelva el `claude` del `PATH`
**no los alcanza**.

---

## 2.3 · Windows, WSL2 y musl

Tres casos con página propia, y conviene saber que existen antes de pelearse:

- **Windows**: instalación nativa o vía WinGet, con su propia guía de puesta a
  punto.
- **WSL2**: funciona, con un aviso del M18 que ahorra una tarde: hay un problema
  documentado de **búsquedas lentas o incompletas en WSL**. Si tu gente dice que
  "no encuentra archivos que están ahí", empieza por ahí y no por la
  configuración.
- **Alpine Linux y distribuciones basadas en musl**: tienen sección propia, con
  dependencias adicionales. No des por hecho que lo que funciona en Debian
  funciona en Alpine, que es justo el caso de muchos contenedores de CI.

---

## 2.4 · Verificar la instalación

```bash
claude --version      # la versión, y es el dato que zanja discusiones
claude doctor         # diagnóstico de solo lectura, sin abrir sesión
```

`claude doctor` responde lo que importa para dar soporte a otro: método de
instalación, plataforma, ruta, si las autoactualizaciones están activadas, qué
canal sigue y **cuándo fue el último intento de actualización y con qué
resultado**. En la máquina de esta guía:

```
Running: native (2.1.228)
Platform: linux-x64
Config install method: native
Auto-updates: enabled
Auto-update channel: latest
Last update attempt: success → 2.1.228 (2026-08-12)
No installation issues found.
```

Del M3: **`/doctor` dentro de una sesión hace mucho más**, incluida la propuesta de
arreglos que aplica solo si confirmas.

---

## 2.5 · Integridad del binario

Esta sección es la que pide seguridad y casi nadie sabe que existe:

> Cada release publica un **`manifest.json` con las sumas SHA256 de todos los
> binarios de todas las plataformas**. El manifiesto **está firmado con una clave
> GPG de Anthropic**, así que **verificar la firma del manifiesto verifica de
> forma transitiva todos los binarios que lista**.

La clave pública se publica en una URL fija y se importa con `gpg`. El
procedimiento necesita una shell POSIX con `gpg` y `curl`; en Windows, Git Bash o
WSL, y el paso final tiene alternativa en PowerShell.

💡 Si tu organización exige verificación de procedencia del software que instala,
esto es lo que hay que enseñarle a quien lo pida, y es una respuesta mucho mejor
que "lo bajamos de la web oficial".

---

## 2.6 · Canales de release y suelo de versión

Dos ajustes que juntos resuelven el problema de "a mi compañero le funciona un
comando que a mí no me existe":

**Canal**, con `autoUpdatesChannel`:

- **`"latest"`**, el valor por defecto: funciones nuevas en cuanto salen.
- **`"stable"`**: una versión de **aproximadamente una semana de antigüedad**, que
  **se salta las releases con regresiones importantes**.

**Suelo**, con `minimumVersion`: las autoactualizaciones y `claude update`
**se niegan a instalar por debajo de ese valor**.

```json
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.100"
}
```

Y el detalle bien pensado: **pasar de `latest` a `stable` no te degrada** si ya
estás en una versión más nueva. Al cambiar desde `/config` te pregunta si quieres
quedarte en la actual o permitir la bajada; **si eliges quedarte, fija
`minimumVersion` en esa versión**. Volver a `latest` lo limpia.

En **settings gestionados**, `minimumVersion` impone un mínimo para toda la
organización. Recuerda del M3 que **`requiredMinimumVersion` falla abierto por
diseño**: un valor inválido se descarta en vez de impedir que Claude Code arranque.

💡 **Recomendación para un equipo:** canal `stable` y un `minimumVersion` explícito
en los settings del repositorio, más la versión anotada en el `CLAUDE.md`. Con eso,
cuando alguien reporte un comportamiento raro, la primera pregunta ya tiene
respuesta escrita.

---

## 2.7 · Autenticación, y su orden de precedencia

Cuando hay varias credenciales presentes, Claude Code elige **en este orden**:

| # | Credencial | Cómo viaja | Cuándo usarla |
|---|---|---|---|
| 1 | **Proveedor cloud**, si está `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX` o `CLAUDE_CODE_USE_FOUNDRY` | Según el proveedor | Bedrock, Agent Platform, Foundry |
| 2 | **`ANTHROPIC_AUTH_TOKEN`** | Cabecera `Authorization: Bearer` | **Gateways y proxies** que autentican con bearer |
| 3 | **`ANTHROPIC_API_KEY`** | Cabecera `X-Api-Key` | Acceso directo a la API con clave de la consola |
| 4 | **`apiKeyHelper`** | Salida del script | **Credenciales dinámicas o rotatorias**, tokens de vida corta |

⚠️ **La trampa del número 3, que muerde en automatización.** En modo interactivo se
te pregunta **una vez** si apruebas o rechazas la clave, y tu elección se recuerda;
el interruptor "Use custom API key" de `/config` **solo aparece mientras la
variable esté puesta en tu entorno**. Pero **en modo no interactivo con `-p`, la
clave se usa siempre que esté presente**.

Es decir: puedes haber rechazado esa clave en tu sesión interactiva y estar
usándola sin enterarte en tus scripts. Si tienes claves de varias cuentas en el
entorno, revísalo antes de montar nada desatendido.

Para el resto: inicio de sesión de Claude for Teams o Enterprise, autenticación de
la consola, autenticación de proveedor cloud, y **restringir el inicio de sesión a
tu organización**, que es lo que impide que alguien use su cuenta personal en una
máquina de la empresa.

---

## 2.8 · Tokens de larga duración

```bash
claude setup-token
```

Genera un token de larga duración, y **requiere una suscripción de Claude**. Es la
vía para CI y automatización cuando no quieres una clave de API rodando por ahí.
La documentación cubre además **renovar un inicio de sesión que está a punto de
caducar**, que es el aviso que aparece antes de que se rompa un flujo automático.

---

## 2.9 · Desinstalación limpia

Tiene procedimiento propio **por cada vía de instalación**: nativa, Homebrew y
WinGet. No es lo mismo y hacerlo mal deja restos que luego producen
**instalaciones duplicadas**, que es una de las cosas que `/doctor` reporta.

Si vas a cambiar de método de instalación, desinstala primero con el procedimiento
de la vía antigua.

---

## 2.10 · Errores de instalación

El catálogo del M18 tiene una categoría propia con dos errores documentados:
**instalación interrumpida antes de terminar** y **conexión caída durante la
descarga de la actualización**. Los dos se resuelven reintentando, porque dejan el
estado a medias y no corrupto.

Para todo lo demás, `troubleshoot-install.md` tiene 60 KB dedicados solo a esto.

---

## Checklist de verificación

- [ ] Sé por qué vía está instalado en cada máquina de mi equipo.
- [ ] `claude doctor` sale limpio.
- [ ] La versión está anotada en el repositorio, no solo en mi cabeza.
- [ ] Mi equipo tiene canal y `minimumVersion` fijados en settings.
- [ ] Sé qué credencial gana en mi entorno, de las cuatro posibles.
- [ ] Sé que con `-p` la `ANTHROPIC_API_KEY` se usa siempre que esté presente.
- [ ] Si hay política de procedencia, sé verificar la firma del manifiesto.
- [ ] Si cambio de método de instalación, desinstalo primero.

## Errores típicos

| Síntoma | Qué está pasando |
|---|---|
| "A mi compañero le existe un comando que a mí no" | Versiones distintas. Canal y `minimumVersion` |
| "Pasé a `stable` y me degradó" | No debería: pasar de `latest` a `stable` pregunta antes |
| "Homebrew no me actualiza a la última" | Las actualizaciones las lleva Homebrew, no Claude Code |
| "En mi contenedor Alpine falla" | Distribuciones musl tienen dependencias propias |
| "En WSL no encuentra archivos que están ahí" | Problema documentado de búsqueda en WSL |
| "Mi script usa una clave que yo rechacé" | Con `-p` la clave se usa siempre que esté presente |
| "`claude doctor` dice instalaciones duplicadas" | Restos de otra vía de instalación |
| "El token de CI caducó de golpe" | Hay aviso de renovación antes. `claude setup-token` |

---

## Fuentes usadas en este módulo

Descargadas el 12 de agosto de 2026 desde `code.claude.com/docs/en/`:

| Página | Bytes | Para qué |
|---|---:|---|
| `setup.md` | 30.871 | Instaladores, canales, `minimumVersion`, firma GPG, desinstalación |
| `authentication.md` | 23.943 | Precedencia de credenciales, tokens de larga duración |
| `troubleshoot-install.md` | 60.388 | Errores de instalación |

Verificación propia: `claude --version` y `claude doctor` sobre la instalación
nativa 2.1.228 de la máquina donde se ha escrito esta guía, 12 de agosto de 2026.

**Marcas pendientes:** ninguna. Este módulo cierra las afirmaciones `CLI-001`,
`CLI-002` y `CLI-003` del registro del verificador, que pasan las tres.
