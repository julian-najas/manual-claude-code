# El plugin mínimo viable

```text
plugin/
├── .claude-plugin/
│   └── plugin.json      ← SOLO esto va aquí dentro
├── skills/
│   └── auditar-endpoint/SKILL.md
├── agents/
│   └── revisor.md
└── hooks/
    ├── hooks.json
    ├── veto-secretos.sh
    └── format.sh
```

## El error que comete todo el mundo

**No pongas `skills/`, `agents/`, `commands/` ni `hooks/` dentro de
`.claude-plugin/`.** Ahí dentro solo va `plugin.json`. Todo lo demás va en la raíz
del plugin.

Y **la raíz del plugin nunca es `~/.claude/`**: es el directorio propio de este
plugin, el que pasas a `--plugin-dir` o el que contiene `.claude-plugin/plugin.json`.

## `${CLAUDE_PLUGIN_ROOT}` y no `${CLAUDE_PROJECT_DIR}`

Fíjate en la diferencia con la plantilla suelta de `hooks/`: dentro de un plugin
las rutas se resuelven contra la raíz del **plugin**, no contra la del proyecto.

## Probar antes de publicar

```bash
claude --plugin-dir ./plugin
```

## Publicar

1. Sube el plugin a su repositorio.
2. **Etiqueta la release**, para que la resolución de versiones funcione.
3. Pon `marketplace.json` en **otro** repositorio, el del catálogo.
4. Ancla la fuente del plugin con `sha` o `sha256`. El catálogo admite `ref` pero
   **no `sha`**: el anclaje fino va en la entrada del plugin.
5. Añade el catálogo a los settings gestionados con lista blanca.
6. **Verifica en una máquina que no sea la tuya.**
