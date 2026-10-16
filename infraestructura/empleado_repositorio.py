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

    def listar(self):
        with obtener_conexion() as conn:
            filas = conn.execute(
                """SELECT p.rut, p.nombre, e.fecha_ingreso, e.sueldo_base
                FROM empleado e JOIN persona p on p.rut = e.rut
                ORDER BY p.nombre"""
            ).fetchall()
        return [self._fila_a_empleado(fila) for fila in filas]

    def actualizar(self, empleado):
        with obtener_conexion() as conn:
            conn.execute(
                "UPDATE persona SET nombre = ? WHERE rut = ?",
                (empleado.nombre, empleado.rut),
            )
            conn.execute(
                """UPDATE empleado 
                SET fecha_ingreso = ?, sueldo_base = ?
                WHERE rut = ?"""
                (empleado.fecha_ingreso.isoformat(), empleado.sueldo_bse, empleado.rut),
            )
        return empleado

    def eliminar(self, rut):
        with self.obtener_coneccion() as conn:
            cursor = conn.execute("UPDATE empleado SET activo = 0 WHERE rut = ?"
            (rut,)
            )
        return cursor.rowcount > 0
    
    """def eliminar(self, rut):
        with obtener_conexion() as conn:
            cursor = conn.execute("DELETE FROM empledo WHERE rut = ?, (rut,)")
            conn.execute("DELETE FROM persona WHERE rut =?",(rut))
        return cursor.rowcount > 0 """

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
                """SELECT p.rut, p.nombre, e.fecha_ingreso, e.sueldobase
                   FROM empleado e JOIN persona p ON p.rut = e.rut
                   WHERE e.rut = ?""",
                (rut,),
            ).fetchone()
        return self._fila_a_empleado(fila) if fila else None