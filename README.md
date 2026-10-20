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
