# Permisos y seguridad

## El principio

Un agente de codificación es un proceso con las credenciales de quien lo lanza.
Todo el modelo de seguridad se reduce a decidir **antes** qué puede tocar, no a
vigilarlo **durante**.

## Los cuatro niveles, de menos a más peligroso

| Nivel | Dónde | Qué se permite |
|---|---|---|
| Lectura | cualquier sitio | leer código y ejecutar comandos sin efectos |
| Escritura con confirmación | rama de trabajo | editar archivos, cada acción sensible se pregunta |
| Escritura amplia | repositorio de pruebas o contenedor | editar y ejecutar sin preguntar |
| Sin comprobaciones | **solo en aislamiento sin red ni credenciales** | todo |

La bandera que salta todas las comprobaciones existe y la propia ayuda del CLI
la marca como peligrosa. Su sitio es un contenedor desechable, nunca una máquina
con acceso a producción o a datos de clientes.

## Las cuatro puertas por las que entra el problema

1. **El propio repositorio.** Un README, un comentario o un archivo de datos
   pueden contener instrucciones dirigidas al agente. El agente lee texto: no
   distingue por sí solo entre "documentación" y "orden".
2. **Las dependencias.** Lo mismo, en código de terceros que el agente abre para
   entender un error.
3. **Los servidores de conexión externa.** Lo que un MCP devuelve entra en el
   contexto como cualquier otro texto. Un servidor de terceros sin revisar es
   código ejecutándose con tu confianza puesta.
4. **Los tickets y las incidencias.** Cualquiera que pueda abrir una incidencia
   en tu repositorio público puede escribirle al agente que la lea.

Mitigación en una línea: **permisos estrechos y revisión humana antes de
fusionar**. No hay filtro de texto que sustituya a ninguna de las dos.

## Secretos

Un `.env` leído por el agente es un incidente, no una anécdota: ese contenido ha
salido de la máquina. Se previene con un hook que veta la lectura de esas rutas,
no con una instrucción pidiendo que no las mire.

## Qué contestar cuando pregunten

"¿Esto manda nuestro código fuera?" Sí: el texto de la conversación y el
contenido de los archivos que el agente abre para trabajar van al proveedor. Lo
que hay que tener escrito es qué proveedor, con qué contrato, qué rutas están
excluidas y quién lo aprobó. La plantilla de política interna tiene los huecos
exactos que hay que rellenar.
