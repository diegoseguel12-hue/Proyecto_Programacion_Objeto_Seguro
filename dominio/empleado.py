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
            