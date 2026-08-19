# Sonda del esquema

Aquí no hay configuración de nadie. El `.claude/settings.json` de esta carpeta
tiene valores **inválidos a propósito**: `claude doctor`, al rechazarlos,
enumera lo que el esquema del binario acepta de verdad.

Es la técnica del módulo 02 aplicada al módulo 04. Sirve para dos cosas:

1. Comprobar que una clave existe en el binario instalado, no solo en la
   documentación. Una clave con el nombre mal escrito **no se reporta**, así que
   si su línea aparece en la salida es que el binario la conoce.
2. Leer la lista de valores válidos de un campo cerrado, como
   `permissions.defaultMode`.

Las pruebas `PRM-005` y `PRM-006` del registro corren `claude doctor` aquí.
**No copies este archivo a un proyecto.**
