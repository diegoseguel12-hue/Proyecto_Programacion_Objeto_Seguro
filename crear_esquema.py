from infraestructura.conexion import obtener_conexion, ErrorDeConexion

try:
    with open("db/01_esquema.sql", encoding="utf-8") as archivo:
        sql = archivo.read()
    with obtener_conexion() as conn:
        conn.executescript(sql)
    print("Tablas creadas")
except ErrorDeConexion as e:
    print("Error:", e)
