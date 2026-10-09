from infraestructura.conexion import obtener_conexion, ErrorDeConexion


def insertar_persona(rut, nombre):
    try:
        with obtener_conexion() as conn:
            conn.execute(
                "INSERT INTO persona (rut, nombre) VALUES (?, ?)",
                (rut, nombre),
            )
        print("Persona guardada:", rut, nombre)
    except ErrorDeConexion as e:
        print("No se pudo guardar:", e)


def mostrar_personas():
    with obtener_conexion() as conn:
        filas = conn.execute("SELECT rut, nombre FROM persona").fetchall()
    for fila in filas:
        print(fila)


try:
    insertar_persona("12345678-9", "Ana Rojas")
    mostrar_personas()
    insertar_persona("12345678-9", "Ana Rojas")
except ErrorDeConexion as e:
    print("Error:", e)
