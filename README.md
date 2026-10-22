# Proyecto Programación Orientada a Objeto Seguro

Caso EcoTech Solutions - TI3021

## Cómo ejecutar

1. Crear y activar el entorno virtual (`python -m venv .venv` y luego `.venv\Scripts\activate` en Windows o `source .venv/bin/activate` en Linux/Mac)
2. `pip install -r requirements.txt`
3. (Opcional) Copiar `.env.example` como `.env`. Si no existe, el programa usa SQLite con el archivo `ecotech.db`
4. `python main.py` (con SQLite las tablas se crean solas la primera vez; `python crear_esquema.py` sigue disponible para crearlas a mano)

Para usar **Supabase** en vez de SQLite, el `.env` debe tener `DB_MOTOR=supabase`, `SUPABASE_URL` y `SUPABASE_KEY`, y el esquema de `db/02_esquema_supabase.sql` ejecutado en el editor SQL de Supabase. Las claves nunca se suben a Git (`.env` está en `.gitignore`).

`main.py` abre un menú de consola para registrar, buscar, listar, actualizar y dar de baja empleados, y para registrar y listar departamentos. La opción 8 ejecuta las pruebas automáticas (incluye el intento de inyección SQL con `' OR '1'='1`) y la opción 9 muestra el polimorfismo.

## Arquitectura

| Capa | Archivos | Responsabilidad |
|---|---|---|
| Dominio | `dominio/` | Clases del modelo UML (`Persona`, `Empleado`, `Usuario`, `Departamento`, `Proyecto`, `RegistroTiempo`) y excepciones propias. No contiene SQL |
| Persistencia | `infraestructura/` | Repositorios con el SQL. `base.py` define las clases abstractas (el contrato CRUD) y cada motor (SQLite, Supabase) las implementa |
| Aplicación | `main.py` | Menú de consola y validación de las entradas del usuario |

Como el programa solo conoce el contrato de `base.py`, cambiar de motor no obliga a modificar el dominio ni el menú.

## Decisiones (C08)

| Decisión | Opciones | La nuestra |
|---|---|---|
| ¿Se borra de verdad? | DELETE real · marcar activo = 0 | Borrado lógico: se marca activo = 0 y las consultas filtran activo = 1 |
| ¿Qué pasa con los hijos? | Cascada · impedir el borrado · dejarlos huérfanos | Como el borrado de empleados es lógico, sus registros de tiempo se conservan como historial. La cascada (ON DELETE CASCADE) queda en el esquema por si se borra físicamente. Un departamento con empleados asignados no se puede borrar (lo impide la llave foránea) |
| ¿Qué pasa si se vuelve a guardar un empleado dado de baja? | Error por RUT duplicado · reactivarlo | Se reactiva: `guardar` actualiza sus datos y pone activo = 1. Si el empleado sigue activo, se rechaza por RUT duplicado |
| ¿Quién asigna el id? | La base (autoincremento) · el programa | El empleado usa el RUT como id; departamento y proyecto usan autoincremento de la base |

## Qué pasa cuando algo falla (C09)

| Situación | Qué pasa | ¿Bien manejado? |
|---|---|---|
| Guardar un empleado con un RUT que ya está activo | `RutDuplicadoError`. No se escribe nada | ✔ |
| Guardar un empleado dado de baja con el mismo RUT | Se reactiva con los datos nuevos | ✔ |
| Crear un empleado con sueldo negativo | `DatoInvalidoError: El sueldo debe ser mayor a 0` (lo valida el setter) | ✔ |
| Crear un empleado con sueldo en texto (`"mil"`) | `DatoInvalidoError: El sueldo base debe ser un número entero` | ✔ |
| Crear un empleado con la fecha en texto (`"2024-01-01"`) | `DatoInvalidoError: La fecha de ingreso debe ser una fecha válida` | ✔ |
| Crear un empleado con RUT o nombre vacío, o con RUT mal formado | `DatoInvalidoError` desde `Persona` | ✔ |
| Guardar un departamento con un nombre repetido | `ErrorDeIntegridad: UNIQUE constraint failed: departamento.nombre` | ✔ |
| Guardar un departamento sin gerente | `DatoInvalidoError: El gerente no puede estar vacío` | ✔ |
| Borrar un departamento que tiene empleados | `ErrorDeIntegridad: FOREIGN KEY constraint failed`. La llave foránea impide el borrado | ✔ |
| Buscar un empleado o departamento que no existe | `obtener` devuelve `None`. No encontrar algo no es un error | ✔ |
| Eliminar un empleado que no existe | `eliminar` devuelve `False` | ✔ |
| Actualizar un empleado que no existe | `actualizar` devuelve 0 filas modificadas y el menú informa `EmpleadoNoEncontradoError` | ✔ |
| Buscar con `' OR '1'='1` | `listar` devuelve `[]` y `obtener` devuelve `None`. No hay inyección SQL | ✔ |
| Ejecutar sin el archivo `.env` | Usa SQLite con `ecotech.db` por defecto y crea las tablas | ✔ |
| Ejecutar en un computador limpio sin las tablas | `crear_repositorios()` las crea antes de empezar | ✔ |
| Escribir texto, fechas inválidas o números mal escritos en el menú | Se vuelve a pedir el dato; el programa no se cae | ✔ |
| Falla la segunda escritura al guardar un empleado | SQLite: rollback de toda la transacción. Supabase: se borra a mano la persona recién creada | ✔ |

Jerarquía de errores: `EcoTechError` (negocio: `DatoInvalidoError`, `RutDuplicadoError`, `EmpleadoNoEncontradoError`) y `ErrorDeConexion` (base de datos; su subclase `ErrorDeIntegridad` indica una restricción violada). `main.py` captura ambas familias por separado y nunca usa un `except` genérico.
