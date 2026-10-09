from datetime import date
from dominio.empleado import Empleado
from infraestructura.conexion import obtener_conexion


class EmpleadoRepositorio:

    def guardar(self, empleado):
        with obtener_conexion() as conn:
            conn.execute(
                "INSERT INTO persona (rut, nombre) VALUES (?, ?)",
                (empleado.rut, empleado.nombre),
            )
            conn.execute(
                """INSERT INTO empleado (rut, fecha_ingreso, sueldo_base)
                   VALUES (?, ?, ?)""",
                (empleado.rut, empleado.fecha_ingreso.isoformat(), empleado.sueldo_base),
            )
        return empleado