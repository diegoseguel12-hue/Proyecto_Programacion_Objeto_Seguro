from dominio.departamento import Departamento
from infraestructura.conexion import obtener_conexion


class DepartamentoRepositorio:

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
        sql = "SELECT id, nombre, gerente FROM departamento"
        params = []
        if nombre_contiene:
            sql += " WHERE nombre LIKE ?"
            params.append(f"%{nombre_contiene}%")
        sql += " ORDER BY nombre"
        with obtener_conexion() as conn:
            filas = conn.execute(sql, params).fetchall()
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
