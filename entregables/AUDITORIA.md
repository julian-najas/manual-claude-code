# Auditoría y cobertura

**Fase final del 12 de agosto de 2026.** Rúbrica del §8 aplicada al texto propio, y
lo que se corrigió por bajar de 4.

---

## 1 · Rúbrica

| # | Criterio | Nota | Sustento |
|---|---|:--:|---|
| 1 | **Precisión** | **5** | Cada módulo declara al pie las páginas que descargó. **Dos errores propios detectados y corregidos** durante la escritura, uno de ellos ya publicado. Lo no leído está declarado, no omitido |
| 2 | **Actualidad** | **5** | Verificada contra **2.1.228**, publicada el 11 de agosto. Cubre la semana 32 completa y, vía changelog, las versiones 225 a 228. Incluye el cambio del 14 de agosto **antes** de que ocurra |
| 3 | **Densidad** | **5** | **106 tablas** frente a las 15 exigidas. 4 diagramas Mermaid. 63 menciones de versión mínima. Cero párrafos de relleno: cada módulo tiene su síntoma, su receta y sus errores típicos |
| 4 | **Accionabilidad** | **3 → 5** | **Bajaba de 4 y se corrigió.** Ver apartado 2 |
| 5 | **Cobertura** | **4** | Los 21 módulos escritos, ninguno reducido a un párrafo. Se citan **120 de las 187 páginas**. Las 67 restantes están declaradas módulo a módulo, y ninguna sostiene una afirmación de la guía. **No sube a 5 porque no está todo leído, y decirlo es parte del trato** |
| 6 | **Honestidad** | **5** | **Seis funciones marcadas como research preview o beta.** Precios reales, incluido que Team y Enterprise no tienen ejecuciones gratis de ultrareview. Publicado que la propia guía tuvo un error de MCP, y que un laboratorio propio quedó falsificado por su propio experimento |
| 7 | **Navegabilidad** | **5** | Índice de **193 entradas, 0 enlaces rotos**, comprobado con script. **63 referencias cruzadas** entre módulos. Chuleta construida desde los módulos, no aparte |
| 8 | **Utilidad diferencial** | **5** | Tres correcciones al inventario de partida, dos hallazgos contra el binario, un experimento propio, telemetría propia de 4.195 llamadas, y criterio operativo marcado como tal en 21 puntos |

**Media: 4,9.** Ninguna nota queda por debajo de 4.

---

## 2 · Lo que bajaba de 4, y cómo se corrigió

**Criterio 4, Accionabilidad. Nota inicial: 3.**

El defecto, encontrado comprobando las plantillas contra su propia documentación:
el `hooks.json` apuntaba a `${CLAUDE_PROJECT_DIR}/.claude/hooks/…` mientras que los
scripts vivían en `plantillas/hooks/`. **Los ejemplos no se podían copiar y
ejecutar tal cual**, que es literalmente lo que exige el criterio: había un paso de
instalación que el lector tenía que deducir.

**Corrección aplicada:** `plantillas/instalar.sh`, que copia hooks, skills y
subagentes a `.claude/` del proyecto y **fusiona el perfil de settings con los
hooks en un solo `settings.json` válido**.

Probado en tres pasadas:

| Prueba | Resultado |
|---|---|
| Instalación limpia | 14 archivos copiados, `settings.json` generado con `permissions`, `worktree`, `autoUpdatesChannel`, `minimumVersion` y `hooks` |
| Segunda pasada | **Idempotente**: no pisa nada, avisa de lo que ya existe |
| Hook desde su nueva ruta | Bloquea `/x/.env` con código de salida 2 |

---

## 3 · Verificación de los entregables

| Entregable | Estado |
|---|---|
| `guia-claude-code-2026-08.md` | **44.717 palabras**, 21 módulos, índice de 193 entradas sin enlaces rotos |
| `cheatsheet.md` | Dos páginas, construida desde los módulos |
| `plantillas/CLAUDE.md` + `CLAUDE-monorepo.md` | Comentadas, con los comentarios HTML que cuestan cero tokens |
| `plantillas/settings.*.json` + `SETTINGS-COMENTADO.md` | Dos perfiles, JSON válido, comentarios **aparte** porque JSON no los admite |
| `plantillas/hooks/` | **6 hooks, los 6 probados con JSON de evento real** |
| `plantillas/skills/` | 2 skills, una **con script de apoyo probado** |
| `plantillas/agents/` | 3 subagentes con contrato: rol, límites, criterio de aceptación, salida |
| `plantillas/plugin/` | Plugin mínimo viable + `marketplace.json` con las dos fuentes |
| `FUENTES.md` | **120 páginas** con URL, fecha y módulos que las usan |
| `PENDIENTE-VERIFICAR.md` | Lo que caduca, lo no leído, lo verificado contra el binario |

**Comprobaciones automáticas:** 5 de 5 JSON válidos en plantillas, 6 de 6 hooks
funcionando, 0 enlaces rotos en el índice.

### Prueba de los hooks, en detalle

| Hook | Caso | Esperado | Obtenido |
|---|---|---|---|
| `veto-secretos` | `.env`, `secrets/`, ruta Windows | bloquear | salida 2 en los tres |
| `veto-secretos` | archivo normal | pasar | salida 0 |
| `veto-rm` | `rm -rf`, `rm -fr` | bloquear | salida 2 |
| `veto-rm` | `rm archivo`, `npm test` | pasar | salida 0 |
| `format` | archivo inexistente | no fallar nunca | salida 0 |
| `reinyectar-reglas` | tras compactar | imprimir reglas | imprime |
| `auditar` | evento `PostToolUse` | línea JSONL | escrita |
| `puerta-calidad` | pruebas que fallan | `decision: block` con la salida real | bloquea |
| `puerta-calidad` | pruebas que pasan | no bloquear | salida vacía, código 0 |

---

## 4 · Informe de cobertura documental

**Leídas y citadas: 120 de 187 páginas (64 %).**

| Bloque no leído | Páginas | Consecuencia declarada |
|---|---:|---|
| Referencias de la API del Agent SDK | 18 | **El M17 es mapa de decisiones, no referencia de API.** Para firmas concretas hay que ir a las de TypeScript y Python |
| Detalle de entornos self-hosted | 6 | El M14 cubre qué son y cuándo; el detalle operativo alimenta el playbook 20.4 |
| Detalle del gateway de Anthropic | 5 | Igual: el M14 cubre la decisión, no la configuración fina |
| Detalle de escritorio | 4 | El M12 cubre qué aporta la superficie |
| Resto de apoyo y quickstarts | ~34 | Sin afirmaciones dependientes |

**Ninguna afirmación de la guía se apoya en una página no leída.** Cada módulo que
tiene páginas pendientes lo dice en su propio apartado de marcas.

---

## 5 · Correcciones al Anexo A del megaprompt

Tres, todas verificadas contra la documentación oficial:

1. **Son seis modos de permisos, no cinco.** Falta `default`, que en el CLI, las
   extensiones y la app de escritorio se llama **Manual**. El alias `manual`
   requiere v2.1.200 o posterior.
2. **Son ocho invalidadores de caché, no siete.** Falta **denegar una herramienta
   entera**: un nombre pelado en una regla `deny` la quita del system prompt e
   invalida la caché a mitad de sesión.
3. **El Anexo cubre hasta v2.1.224 y la máquina corre 2.1.228.** Y el hueco de
   método: **no existe digest de la semana 31 ni de la 33**, así que el §2.3, que
   fija las fuentes en los digests semanales, **garantiza que la guía nazca
   desfasada**. La regla correcta es *digests disponibles más el changelog desde la
   última versión cubierta*.

**Lo que sí se sostuvo:** las 106 páginas que el Anexo nombra **existen todas**, y
los **31 eventos de hooks son exactos**, ni falta ni sobra ninguno.

---

## 6 · Hallazgos propios contra el binario

| Qué | Cómo se encontró |
|---|---|
| `--brief` no aparece en ninguna de las 120 páginas citadas | Cruce de `claude --help` contra `cli-reference.md` |
| `--file` se menciona en changelog y permisos, **no en la referencia del CLI** | Igual |
| El agente **no obedece** una inyección en el README, dos de dos | `evidencias/EXP-001`, dos pasadas con `claude -p` |
| 24 tokens de entrada por cada token de salida | 4.195 llamadas propias, `analizar_gasto.py` |
| Cada confirmación de una palabra costó 7.891 tokens de entrada | Mismos datos |

En el primer par, el matiz va escrito en el módulo: **no se han revisado las 187
páginas**, así que lo afirmable es que no están donde un lector iría a buscarlas.

---

## 7 · Errores propios cometidos y corregidos

Se publican porque la credibilidad de una guía así depende de que se vean:

1. **Dije que MCP era un peaje permanente de contexto.** Es falso desde tool
   search: solo pesan los nombres. Corregido en cuatro sitios, la lámina
   republicada, y dado de alta como `MCP-002` en el verificador.
2. **Diseñé un laboratorio sobre una hipótesis falsa.** Probado, el agente no se
   cree el README ni obedece la inyección. Dos laboratorios reescritos sobre lo
   medido, y el error de método documentado: el repositorio de pruebas llevaba
   carteles anunciando que era un laboratorio.
3. **Conté "7 banderas sin documentar"** por un fallo de mi propia expresión
   regular, que no capturaba las de estilo camelCase. Comprobadas una a una,
   quedaron dos.
4. **Al M19 le faltaba el bloque de errores típicos** que exige la estructura.
   Detectado por script y corregido antes de cerrar la fase.

---

## 8 · Cómo se mantiene vivo

| Pieza | Qué hace |
|---|---|
| `D2-verificador/verificar.py` | Ejecuta las afirmaciones contra el CLI instalado. **19 pasan, 0 fallan.** Corre en CI cada madrugada y abre incidencia sola |
| `D8-boletin/detectar-roturas.py` | Compara la superficie del CLI contra la instantánea anterior y redacta el borrador del boletín semanal |
| `PENDIENTE-VERIFICAR.md` | Lo que caduca, ordenado por urgencia. Lo primero, el 14 de agosto |

**Lo primero que caduca es pasado mañana:** auto mode pasa a ser el modo por
defecto, y la guía lo dice en futuro en cuatro módulos.
