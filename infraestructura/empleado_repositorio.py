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
                (empleado.rut, empleado.fecha_ingreso.isoformat(), empleado._sueldo_base),
            )
        return empleado

    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(
            rut=fila[0],
            nombre=fila[1],
            fecha_ingreso=date.fromisoformat(fila[2]),
            sueldo_base=fila[3],
        )

    def obtener(self, rut):
        with obtener_conexion() as conn:
            fila = conn.execute(
                """SELECT p.rut, p.nombre, e.fecha_ingreso, e._sueldobase
                   FROM empleado e JOIN persona p ON p.rut = e.rut
                   WHERE e.rut = ?""",
                (rut,),
            ).fetchone()
        return self._fila_a_empleado(fila) if fila else None