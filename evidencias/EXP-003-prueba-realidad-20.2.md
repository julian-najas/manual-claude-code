# EXP-003 · Prueba de realidad del playbook 20.2

**Fechas:** 12 y 13 de agosto de 2026 · **CLI:** 2.1.228 y 2.1.229
**Método:** seguir el playbook 20.2 *literalmente*, sobre una copia limpia de
`D6-repo-feo/gestor-pedidos`, anotando cada punto de fricción. Cuatro llamadas
reales, unos 21 minutos de reloj.

**Por qué:** la guía estaba verificada contra documentación y **nunca contra un
lector**. Ningún volumen de investigación encuentra lo que encuentra usarla.

---

## Los tres criterios del playbook

| Criterio | Resultado |
|---|---|
| Los tests de caracterización pasan antes de tocar nada | **PASA**, y verificado dos veces: 46 tests, con el doble de Flask y con Flask 3.1.3 real |
| El agente deja de proponer cambios sobre el código muerto y la configuración equivocada | **PARCIAL.** Ver defecto 2 |
| El revisor encuentra fallos que el agente principal dio por buenos | **PASA.** Ver abajo |

**Yo predije que el tercero era inalcanzable y me equivoqué.** El razonamiento
era que el agente principal ya reporta todo con mucho detalle, así que no quedaría
delta. Quedaba, y era el hallazgo más grave de toda la prueba.

---

## Lo que salió mejor de lo prometido

**Paso 1.** El agente escribió **46 tests de caracterización**, no tocó ni un
archivo de producción (`git diff` vacío sobre los cinco originales), y **hizo una
pasada de mutación que nadie le pidió**: introdujo siete cambios temporales en
`app.py`, comprobó que los siete rompen tests, y restauró. Eso es mejor práctica
que la que prescribe el playbook.

**Encontró siete bugs que yo no había sembrado**, así que mi inventario de 14
fallos del `guion-de-doma.md` estaba incompleto: fechas de alta comparadas como
texto, `"10" * 3` cuando el precio llega como cadena, un cliente llamado `O'Brien`
que tumba el endpoint, la conexión abierta antes de validar, `cobrar()` después
del `commit()`, `utils.limpiar()` que existe y nadie llama, y `MAX_LINEAS` de
`settings.py` que dice 100 mientras el código fija 50 a mano.

**Paso 4, el revisor.** Encontró un delta real y verificado por mí:

| Hallazgo del revisor | Comprobado |
|---|---|
| **Los 46 tests cubren solo `procesar_pedido`.** Las inyecciones SQL de `/pedido/<id>` y `/buscar` tienen **cero cobertura** | Cierto: 0 menciones de `get_pedido`, 0 de `get_pedido_viejo` |
| **La suite fija el valor literal de la clave**, así que rotarla deja la CI en rojo | Cierto, `test_procesar_pedido.py:425` |
| `GET /pedido/<inexistente>` devuelve **HTTP 200 con `null`**, no 404 | Cierto, reproducido con Flask real |
| `/pedido_old` **no es código muerto**: su `@app.route` lo publica igual que las demás | Cierto |

Y **corrigió a la baja dos afirmaciones previas**, que es lo que se le pide a un
revisor adversarial: el test etiquetado como "fuga de conexión" en los caminos 400
no mide una conexión real sino el flag de un doble, y en CPython el refcount la
cierra al salir; y la inyección SQL no permite `; DROP TABLE` porque `sqlite3`
rechaza sentencias múltiples, así que es lectura y corrupción, no destrucción.

---

## Los seis defectos del playbook

Esto es lo que la prueba existía para encontrar.

### 1. El `CLAUDE.md` de la plantilla afirma algo falso

El playbook da esta línea:

> `- La configuración efectiva es settings.py. config.py está muerto, no lo toques.`

**Es falso en su propio laboratorio.** `app.py` solo importa `sqlite3`, `os` y
`flask`: **nadie importa `settings.py` ni `config.py`**. Los dos están muertos.

El agente lo detectó y **corrigió el `CLAUDE.md`** por su cuenta. Es el defecto más
grave de los seis, porque el módulo 4 enseña que el `CLAUDE.md` sirve para
resolver empates y decir la verdad, y la plantilla que reparte **comete
exactamente el pecado que enseña a evitar**: afirma algo que el código desmiente,
igual que el README mentiroso del propio laboratorio.

### 2. El criterio 2 se contradice con la plantilla que él mismo da

El criterio dice *"deja de proponer cambios sobre el código muerto"*. La plantilla
dice *"`/pedido_old` es código muerto **pendiente de borrar**"*. El agente propuso
**borrarlo**, citando el `CLAUDE.md`. Eso es obedecer, no desobedecer: la
plantilla invita al borrado y el criterio lo cuenta como fallo.

### 3. No dice con qué permisos ejecutar

El playbook da los prompts y no dice si van en interactivo, con `acceptEdits`, con
`plan` o en modo no interactivo. Un lector en interactivo aprueba a mano; quien lo
automatice tiene que adivinar. Es el primer punto donde hubo que improvisar.

### 4. No dice que hay que instalar las dependencias antes

Flask no estaba instalado y `pip install` no está disponible en sesión no
interactiva. El agente **construyó un sustituto mínimo de Flask** para que la
suite corriera, y lo avisó. Funcionó, pero **el criterio "los tests pasan" se
habría cumplido contra un doble**. Un lector podría dar por buena su red de
seguridad sin saber que no ha tocado Flask. Lo cerré instalando Flask 3.1.3 real:
los 46 pasan igual, pero eso fue trabajo mío, no del playbook.

### 5. El prompt acota a una función y eso da falsa sensación de red

El prompt caracteriza `procesar_pedido()`. Los 46 tests que produce **no cubren
las otras tres rutas**, incluidas dos con inyección SQL. El playbook celebra que
"los tests pasan" cuando la aplicación sigue abierta de par en par. Hay que decir
explícitamente qué queda fuera.

### 6. No hay expectativa de tiempo ni de coste

El paso 1 tardó **7 min 52 s** y el paso 4, **8 min 29 s**. Los módulos del manual
abren con su factura estimada; el M20 no. Y una sesión de prueba agotó el límite
de uso del plan a mitad del recorrido, cosa que un playbook debería advertir.

---

## Lo que confirma que esto no era opcional

Cuatro llamadas y un rato de verificación produjeron **seis defectos del
playbook**, **siete bugs del laboratorio que faltaban en mi inventario** y **una
predicción mía desmentida**. Ninguno de los seis se veía leyendo la guía: los seis
aparecieron al usarla.

Es el mismo patrón que ya dejó EXP-001, que falsificó dos laboratorios míos, y que
las pruebas de coste, que destaparon dos defectos del verificador. **Los bugs de
este proyecto están en el uso, no en la investigación.**
