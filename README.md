# Proyecto Programación Orientada a Objeto Seguro

Caso EcoTech Solutions - TI3021

## Cómo ejecutar

1. Crear y activar el entorno virtual
2. `pip install -r requirements.txt`
3. Copiar `.env.example` como `.env`
4. `python crear_esquema.py`
5. `python verificar_c07.py`

## Decisiones (C08)

| Decisión | Opciones | La nuestra |
|---|---|---|
| ¿Se borra de verdad? | DELETE real · marcar activo = 0 | |
| ¿Qué pasa con los hijos? | Cascada · impedir el borrado · dejarlos huérfanos | |
| ¿Quién asigna el id? | La base (autoincremento) · el programa | |
