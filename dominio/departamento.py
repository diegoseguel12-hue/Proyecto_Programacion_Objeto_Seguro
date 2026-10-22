"""
Esta pestaña contiene la clase departamento
y sus métodos
"""

from dominio.excepciones import DatoInvalidoError


class Departamento():

    def __init__(self, id, nombre, gerente):

        self.id = id
        self.nombre = nombre
        self.gerente = gerente

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El nombre del departamento no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def gerente(self):
        return self._gerente

    @gerente.setter
    def gerente(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El gerente no puede estar vacío")
        self._gerente = valor.strip()

    def __str__(self):
        return f"Departamento {self.id} - {self.nombre} (gerente: {self.gerente})"
