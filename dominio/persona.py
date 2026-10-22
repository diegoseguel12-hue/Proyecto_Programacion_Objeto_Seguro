"""
Esta pestaña contiene la clase persona para
la herencia con empleado
"""

import re

from dominio.excepciones import DatoInvalidoError


class Persona:

    def __init__(self, rut, nombre):
        # Se asigna a través de las propiedades para que se validen
        self.rut = rut
        self.nombre = nombre

    @property
    def rut(self):
        return self._rut

    @rut.setter
    def rut(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El RUT no puede estar vacío")
        limpio = valor.strip().replace(".", "").upper()
        if not re.fullmatch(r"\d{7,8}-[\dK]", limpio):
            raise DatoInvalidoError("El RUT debe tener el formato 12345678-9")
        self._rut = limpio

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío")
        self._nombre = valor.strip()

    def __str__(self):
        return f"{self.rut} - {self.nombre}"
