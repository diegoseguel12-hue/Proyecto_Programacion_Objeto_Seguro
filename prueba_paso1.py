from datetime import date
from dominio.empleado import Empleado
from infraestructura.empleado_repositorio import EmpleadoRepositorio
from infraestructura.conexion import ErrorDeConexion

repo = EmpleadoRepositorio()
ana = Empleado("12345678-9", "Ana Rojas", date(2024, 3, 1), 950_000)

try:
    repo.guardar(ana)
    print("Guardado:", ana.rut, ana.nombre)
except ErrorDeConexion as e:
    print("Error:", e)