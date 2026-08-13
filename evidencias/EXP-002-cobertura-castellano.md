# EXP-002 · ¿Cuánta documentación oficial existe ya en castellano?

**Fecha:** 13 de agosto de 2026
**Método:** petición HTTP a `code.claude.com/docs/es/<slug>.md` para **los 187
slugs** del índice oficial `llms.txt`, tomados del inventario de la Fase 0.
**Datos crudos:** `EXP-002-datos-crudos.txt`, una línea por página con su código.

---

## Resultado

| | |
|---|---:|
| Páginas del índice oficial | 187 |
| Existen en castellano (HTTP 200) | **173** |
| No existen (HTTP 404) | 14 |
| **Cobertura** | **92,5 %** |

Esto **sustituye** al muestreo de 16 páginas del 13 de agosto, que daba 14 de 16.
La proporción se confirmó, pero un porcentaje sobre muestra no es un dato para
poner en la portada de un producto.

---

## Lo que de verdad dice este número

El titular obvio es que **"la guía en español" no es un diferencial**: nueve de
cada diez páginas ya están traducidas por Anthropic.

Pero **las 14 ausencias no son aleatorias**:

```
agent-sdk/examples
agent-sdk/troubleshooting
claude-tag
cross-session-messaging
github-actions-cloud-providers
self-hosted-environments
self-hosted-environments-configuration
self-hosted-environments-deploy
self-hosted-environments-identity
self-hosted-environments-quickstart
self-hosted-environments-reference
self-hosted-environments-testing
whats-new/2026-w30
whats-new/2026-w32
```

**Casi todas son lo más reciente**: los seis archivos de **entornos self-hosted**,
que son beta pública de la semana 32; la **mensajería entre sesiones**, que llegó
en la v2.1.224 de esa misma semana; **Claude Tag**, que es la sustitución en curso
de Claude Code en Slack; Actions con proveedores cloud; y **los digests de las
semanas 30 y 32**, es decir las novedades de julio y agosto.

> **La traducción oficial va por detrás justo en lo que acaba de salir.**

Y lo que acaba de salir es exactamente el material del M9 (mensajería entre
sesiones), el M12 (Claude Tag y la retirada de Slack) y el M14 (entornos
self-hosted) de esta guía.

---

## Consecuencia para el posicionamiento

No es "la guía en español". Es:

> El manual en castellano que **se verifica contra el binario** y que llega a lo
> nuevo **antes que la traducción oficial**.

La segunda mitad de esa frase es nueva y es comprobable: reejecutar esta medición
cada trimestre dice si el hueco se cierra o se mantiene. Si un día las 187 están
traducidas, esa parte del argumento cae y hay que decirlo, no esconderlo.

---

## Reproducirlo

Los 187 slugs salen de `guia-21/inventario.json`:

```bash
python3 -c "import json;print('\n'.join(s.replace('.md','') for s,_ in json.load(open('guia-21/inventario.json'))))" > slugs.txt

cat slugs.txt | xargs -P 8 -I{} sh -c \
  'printf "%s %s\n" "$(curl -sS -o /dev/null -w "%{http_code}" --max-time 25 \
   "https://code.claude.com/docs/es/{}.md")" "{}"' > resultado.txt

awk '{print $1}' resultado.txt | sort | uniq -c
```

Coste: cero. Son peticiones HEAD contra documentación pública.
