from datetime import date
from dominio.empleado import Empleado
from dominio.excepciones import RutDuplicadoError
from infraestructura.base import EmpleadoRepositorioBase
from infraestructura.conexion import obtener_conexion

# Consultas fijas: nunca se arman concatenando texto. Los datos del usuario
# viajan siempre aparte, en los parámetros (?), y la base los trata como datos.
SQL_LISTAR = """SELECT p.rut, p.nombre, e.fecha_ingreso, e.sueldo_base
                FROM empleado e JOIN persona p ON p.rut = e.rut
                WHERE e.activo = 1
                ORDER BY p.nombre"""
SQL_LISTAR_FILTRADO = """SELECT p.rut, p.nombre, e.fecha_ingreso, e.sueldo_base
                         FROM empleado e JOIN persona p ON p.rut = e.rut
                         WHERE e.activo = 1 AND p.nombre LIKE ?
                         ORDER BY p.nombre"""


class EmpleadoRepositorio(EmpleadoRepositorioBase):

    def guardar(self, empleado):
        # Las escrituras ocurren en una sola transacción: si algo falla,
        # obtener_conexion hace rollback y no queda nada a medias.
        with obtener_conexion() as conn:
            existente = conn.execute(
                "SELECT activo FROM empleado WHERE rut = ?",
                (empleado.rut,),
            ).fetchone()
            if existente and existente[0] == 1:
                raise RutDuplicadoError(
                    f"Ya existe un empleado activo con el RUT {empleado.rut}"
                )
            if existente:
                # Fue dado de baja (borrado lógico): se reactiva con los datos nuevos
                conn.execute(
                    "UPDATE persona SET nombre = ? WHERE rut = ?",
                    (empleado.nombre, empleado.rut),
                )
                conn.execute(
                    """UPDATE empleado
                       SET fecha_ingreso = ?, sueldo_base = ?, activo = 1
                       WHERE rut = ?""",
                    (empleado.fecha_ingreso.isoformat(), empleado.sueldo_base, empleado.rut),
                )
                return empleado
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

    def obtener(self, rut):
        with obtener_conexion() as conn:
            fila = conn.execute(
                """SELECT p.rut, p.nombre, e.fecha_ingreso, e.sueldo_base
                   FROM empleado e JOIN persona p ON p.rut = e.rut
                   WHERE e.rut = ? AND e.activo = 1""",
                (rut,),
            ).fetchone()
        return self._fila_a_empleado(fila) if fila else None

    def listar(self, nombre_contiene=None):
        with obtener_conexion() as conn:
            if nombre_contiene:
                filas = conn.execute(
                    SQL_LISTAR_FILTRADO, (f"%{nombre_contiene}%",)
                ).fetchall()
            else:
                filas = conn.execute(SQL_LISTAR).fetchall()
        return [self._fila_a_empleado(fila) for fila in filas]

    def actualizar(self, empleado):
        with obtener_conexion() as conn:
            conn.execute(
                "UPDATE persona SET nombre = ? WHERE rut = ?",
                (empleado.nombre, empleado.rut),
            )
            cursor = conn.execute(
                """UPDATE empleado
                   SET fecha_ingreso = ?, sueldo_base = ?
                   WHERE rut = ? AND activo = 1""",
                (empleado.fecha_ingreso.isoformat(), empleado.sueldo_base, empleado.rut),
            )
        return cursor.rowcount

    def eliminar(self, rut):
        with obtener_conexion() as conn:
            cursor = conn.execute(
                "UPDATE empleado SET activo = 0 WHERE rut = ? AND activo = 1",
                (rut,),
            )
        return cursor.rowcount > 0

    @staticmethod
    def _fila_a_empleado(fila):
        # Único punto donde una fila de la base se convierte en un objeto Empleado
        return Empleado(
            rut=fila[0],
            nombre=fila[1],
            fecha_ingreso=date.fromisoformat(fila[2]),
            sueldo_base=fila[3],
        )
