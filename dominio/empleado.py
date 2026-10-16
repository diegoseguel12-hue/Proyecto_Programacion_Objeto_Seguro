"""
Esta pestaña contiene la clase empleado junto con sus atributos
y mètodos
"""

from dominio.persona import Persona

class Empleado(Persona):

    def __init__(self, rut, nombre, fecha_ingreso, sueldo_base):

        super().__init__(rut, nombre)
        self.fecha_ingreso = fecha_ingreso
        self._sueldo_base = sueldo_base
        self.registros = []
        self.departamento = None

        @property
        def sueldo_base(self):
            return self._sueldo_base

        @sueldo_base.setter
        def sueldo_base(self, valor):
            if not isinstance(valor, int):
                raise TypeError("El sueldo base debe ser un numero entero")
            if valor <= 0:
                raise ValueError("EL sueldo debe ser mayor a 0")
            self._sueldo_base = valor

        def __str__(self):
            return f"{self.rut} - {self.nombre} - sueldo ${self.sueldo_base:,}"

    def registrarHoras(self, registro):
        ...

    def totalHoras(self):
        ...

class Usuario(Empleado):

    def __init__(self, rut, nombre, fecha_ingreso, sueldo_base, usuario, contrasena):

        super().__init__(rut, nombre, fecha_ingreso, sueldo_base)
        self._usuario = usuario
        self._contrasena = contrasena

    def asigar_departamento(self, asignar):
        ...
        
    def generar_informe():
        ...
            