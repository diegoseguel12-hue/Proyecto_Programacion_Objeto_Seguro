from datetime import date
from dominio.departamento import Departamento
from infraestructura.conexion import obtener_conexion


class DepartamentoRepositorio:

    def guardar(self, departamento):
        with obtener_conexion() as conn:
            conn.execute(
                "INSERT INTO departamento (id, nombre, gerente) VALUES (?, ?, ?)",
                (departamento.id, departamento.nombre, departamento.gerente),
            )
        return departamento

    @staticmethod
    def _fila_a_departamento(fila):
        return Departamento(
            id=fila[0],
            nombre=fila[1],
            gerente=fila[2]
        )

    def obtener(self, ):
        ...