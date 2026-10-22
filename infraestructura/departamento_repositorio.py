from dominio.departamento import Departamento
from infraestructura.base import DepartamentoRepositorioBase
from infraestructura.conexion import obtener_conexion

# Consultas fijas: los valores del usuario siempre van en los parámetros (?)
SQL_LISTAR = "SELECT id, nombre, gerente FROM departamento ORDER BY nombre"
SQL_LISTAR_FILTRADO = """SELECT id, nombre, gerente FROM departamento
                         WHERE nombre LIKE ? ORDER BY nombre"""


class DepartamentoRepositorio(DepartamentoRepositorioBase):

    def guardar(self, departamento):
        with obtener_conexion() as conn:
            cursor = conn.execute(
                "INSERT INTO departamento (nombre, gerente) VALUES (?, ?)",
                (departamento.nombre, departamento.gerente),
            )
            departamento.id = cursor.lastrowid
        return departamento

    def obtener(self, id):
        with obtener_conexion() as conn:
            fila = conn.execute(
                "SELECT id, nombre, gerente FROM departamento WHERE id = ?",
                (id,),
            ).fetchone()
        return self._fila_a_departamento(fila) if fila else None

    def listar(self, nombre_contiene=None):
        with obtener_conexion() as conn:
            if nombre_contiene:
                filas = conn.execute(
                    SQL_LISTAR_FILTRADO, (f"%{nombre_contiene}%",)
                ).fetchall()
            else:
                filas = conn.execute(SQL_LISTAR).fetchall()
        return [self._fila_a_departamento(fila) for fila in filas]

    def actualizar(self, departamento):
        with obtener_conexion() as conn:
            cursor = conn.execute(
                "UPDATE departamento SET nombre = ?, gerente = ? WHERE id = ?",
                (departamento.nombre, departamento.gerente, departamento.id),
            )
        return cursor.rowcount

    def eliminar(self, id):
        with obtener_conexion() as conn:
            cursor = conn.execute("DELETE FROM departamento WHERE id = ?", (id,))
        return cursor.rowcount > 0

    @staticmethod
    def _fila_a_departamento(fila):
        return Departamento(
            id=fila[0],
            nombre=fila[1],
            gerente=fila[2],
        )
