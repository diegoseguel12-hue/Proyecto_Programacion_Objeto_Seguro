from infraestructura.conexion import inicializar_bd, ErrorDeConexion

try:
    inicializar_bd()
    print("Tablas creadas")
except ErrorDeConexion as e:
    print("Error:", e)
