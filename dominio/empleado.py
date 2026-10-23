"""
Esta pestaña contiene la clase empleado junto con sus atributos
y métodos
"""

import hashlib
import hmac
import os
from datetime import date

from dominio.departamento import Departamento
from dominio.excepciones import DatoInvalidoError
from dominio.persona import Persona
from dominio.registro_tiempo import RegistroTiempo


class Empleado(Persona):

    def __init__(self, rut, nombre, fecha_ingreso, sueldo_base):

        super().__init__(rut, nombre)
        self.fecha_ingreso = fecha_ingreso
        self.sueldo_base = sueldo_base
        self.registros = []
        self.departamento = None

    @property
    def fecha_ingreso(self):
        return self._fecha_ingreso

    @fecha_ingreso.setter
    def fecha_ingreso(self, valor):
        if not isinstance(valor, date):
            raise DatoInvalidoError("La fecha de ingreso debe ser una fecha válida")
        self._fecha_ingreso = valor

    @property
    def sueldo_base(self):
        return self._sueldo_base

    @sueldo_base.setter
    def sueldo_base(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise DatoInvalidoError("El sueldo base debe ser un número entero")
        if valor <= 0:
            raise DatoInvalidoError("El sueldo debe ser mayor a 0")
        self._sueldo_base = valor

    def __str__(self):
        return f"{self.rut} - {self.nombre} - sueldo ${self.sueldo_base:,}"

    def registrarHoras(self, registro):
        """Agrega un registro de tiempo al historial del empleado."""
        if not isinstance(registro, RegistroTiempo):
            raise DatoInvalidoError("Solo se pueden registrar objetos RegistroTiempo")
        self.registros.append(registro)

    def totalHoras(self):
        """Suma las horas de todos los registros del empleado."""
        return sum(registro.horas_trabajadas for registro in self.registros)


# Permisos por rol: qué módulos puede usar cada tipo de usuario
PERMISOS = {
    "Administrador": {"empleados", "departamentos", "informes"},
    "Empleado": {"horas"},
}

ITERACIONES_HASH = 200_000


class Usuario(Empleado):

    def __init__(self, rut, nombre, fecha_ingreso, sueldo_base, usuario,
                 contrasena, rol="Empleado"):

        super().__init__(rut, nombre, fecha_ingreso, sueldo_base)
        if not isinstance(usuario, str) or not usuario.strip():
            raise DatoInvalidoError("El nombre de usuario no puede estar vacío")
        if rol not in PERMISOS:
            raise DatoInvalidoError(f"Rol desconocido: {rol}")
        if not isinstance(contrasena, str) or len(contrasena) < 8:
            raise DatoInvalidoError("La contraseña debe tener al menos 8 caracteres")
        self._usuario = usuario.strip()
        self._rol = rol
        # La contraseña nunca se guarda: solo su hash con sal aleatoria
        self._sal = os.urandom(16)
        self._hash = self._calcular_hash(contrasena)

    def _calcular_hash(self, contrasena):
        return hashlib.pbkdf2_hmac(
            "sha256", contrasena.encode("utf-8"), self._sal, ITERACIONES_HASH
        )

    def autenticar(self, contrasena):
        """True si la contraseña entregada coincide con la guardada."""
        if not isinstance(contrasena, str):
            return False
        return hmac.compare_digest(self._calcular_hash(contrasena), self._hash)

    def permiso(self, modulo):
        """True si el rol del usuario puede usar el módulo indicado."""
        return modulo in PERMISOS[self._rol]

    def asignar_departamento(self, asignar):
        """Asigna el departamento en el que trabaja el empleado."""
        if not isinstance(asignar, Departamento):
            raise DatoInvalidoError("Solo se puede asignar un objeto Departamento")
        self.departamento = asignar

    def generar_informe(self):
        """Devuelve un resumen del empleado con su departamento y horas."""
        depto = self.departamento.nombre if self.departamento else "sin departamento"
        return (f"Informe de {self.nombre} ({self.rut}): "
                f"departamento {depto}, {self.totalHoras()} horas registradas")

    def __str__(self):
        return f"{super().__str__()} - usuario {self._usuario} ({self._rol})"
