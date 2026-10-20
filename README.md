# Proyecto Programación Orientada a Objeto Seguro

Caso EcoTech Solutions - TI3021

## Cómo ejecutar

1. Crear y activar el entorno virtual
2. `pip install -r requirements.txt`
3. Copiar `.env.example` como `.env`
4. `python crear_esquema.py`
5. `python main.py`

## Decisiones (C08)

| Decisión | Opciones | La nuestra |
|---|---|---|
| ¿Se borra de verdad? | DELETE real · marcar activo = 0 | Borrado lógico: se marca activo = 0 y las consultas filtran activo = 1 |
| ¿Qué pasa con los hijos? | Cascada · impedir el borrado · dejarlos huérfanos | Como el borrado de empleados es lógico, sus registros de tiempo se conservan como historial. La cascada (ON DELETE CASCADE) queda en el esquema por si se borra físicamente. Un departamento con empleados asignados no se puede borrar (lo impide la llave foránea) |
| ¿Quién asigna el id? | La base (autoincremento) · el programa | El empleado usa el RUT como id; departamento y proyecto usan autoincremento de la base |

## Qué pasa cuando algo falla (C09)

| Situación | Qué pasa | ¿Bien manejado? |
|---|---|---|
| Guardar un empleado con un RUT que ya existe | `ErrorDeConexion: UNIQUE constraint failed: persona.rut`. Se hace rollback y no queda nada a medias | ✔ |
| Crear un empleado con sueldo negativo | `ValueError: El sueldo debe ser mayor a 0` (lo valida el setter) | ✔ |
| Crear un empleado con sueldo en texto (`"mil"`) | `TypeError: El sueldo base debe ser un numero entero` | ✔ |
| Guardar un departamento con un nombre repetido | `ErrorDeConexion: UNIQUE constraint failed: departamento.nombre` | ✔ |
| Guardar un departamento sin gerente | `ErrorDeConexion: NOT NULL constraint failed: departamento.gerente` | ✔ |
| Borrar un departamento que tiene empleados | `ErrorDeConexion: FOREIGN KEY constraint failed`. La llave foránea impide el borrado | ✔ |
| Buscar un empleado o departamento que no existe | `obtener` devuelve `None`. No encontrar algo no es un error | ✔ |
| Eliminar un empleado que no existe | `eliminar` devuelve `False` | ✔ |
| Buscar con `' OR '1'='1` | `listar` devuelve `[]` y `obtener` devuelve `None`. No hay inyección SQL | ✔ |
| Ejecutar sin el archivo `.env` | `ErrorDeConexion: Falta la variable DB_NOMBRE`. El mensaje es claro, pero `main.py` no lo captura y el programa se cae con la traza completa | ✘ Falta `try/except` en `main.py` |
| Crear un empleado con la fecha en texto (`"2024-01-01"`) | `Empleado` lo acepta, y al guardar se cae con `AttributeError: 'str' object has no attribute 'isoformat'`. Como nunca se llega al commit, no queda nada guardado | ✘ Falta validar el tipo de la fecha en `Empleado` |
| Crear un empleado con RUT o nombre vacío | Se crea sin reclamar | ✘ Falta validar en `Persona` |
| Actualizar un empleado que no existe | No avisa: el método devuelve el empleado como si hubiera funcionado | ✘ Debería devolver cuántas filas cambiaron, como en `DepartamentoRepositorio` |
