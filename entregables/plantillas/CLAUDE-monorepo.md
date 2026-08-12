# <MONOREPO>  ·  CLAUDE.md de la raíz

<!--
  VARIANTE MONOREPO. La raíz va CORTA a propósito: se concatena con los
  CLAUDE.md de cada directorio y se paga en cada turno.

  Reparto recomendado:
    - Raíz            → lo que vale para los 40 paquetes (este archivo)
    - packages/X/     → CLAUDE.md propio, lo mantiene su equipo
    - .claude/rules/  → reglas con `paths:` para lo transversal por tipo de archivo

  Los CLAUDE.md de subdirectorios NO se cargan al arrancar: entran cuando Claude
  lee un archivo de ahí. Y NO se reinyectan tras compactar.
-->

Monorepo de <N> paquetes. Cada paquete tiene su propio `CLAUDE.md`; **este archivo
solo contiene lo común**.

## Común a todo el repositorio

- Gestor de paquetes: `<pnpm|yarn|npm>`. No mezclar.
- Probar un paquete: `<comando> --filter <paquete>`
- Nunca edites `packages/*/dist` ni nada bajo `generated/`.

## Dónde vive cada cosa

| Zona | Dueño | Su CLAUDE.md |
|---|---|---|
| `packages/api` | equipo A | sí |
| `packages/web` | equipo B | sí |
| `shared/` | plataforma | sí |

## Aviso de contexto

Si trabajas en un solo paquete, **arranca Claude Code desde ese paquete**: el
`.claude/settings.json` de proyecto se carga desde el directorio de arranque, y
así no cargas el contexto de los otros equipos.

<!-- Para excluir CLAUDE.md de otros equipos, usa claudeMdExcludes en settings. -->
