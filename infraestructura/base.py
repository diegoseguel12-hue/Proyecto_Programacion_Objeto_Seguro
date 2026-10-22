"""
Clases abstractas de la capa de persistencia.

Definen el contrato (los métodos CRUD) que debe cumplir cualquier
repositorio, sin importar la base de datos que haya detrás. Así el
programa principal usa SQLite o Supabase de la misma forma y se puede
cambiar de motor sin tocar el dominio ni el menú.
"""

from abc import ABC, abstractmethod


class EmpleadoRepositorioBase(ABC):

    @abstractmethod
    def guardar(self, empleado):
        """Registra un empleado nuevo (o reactiva uno dado de baja)."""

    @abstractmethod
    def obtener(self, rut):
        """Devuelve el empleado activo con ese RUT, o None si no existe."""

    @abstractmethod
    def listar(self, nombre_contiene=None):
        """Devuelve los empleados activos, opcionalmente filtrados por nombre."""

    @abstractmethod
    def actualizar(self, empleado):
        """Actualiza los datos de un empleado y devuelve las filas modificadas."""

    @abstractmethod
    def eliminar(self, rut):
        """Da de baja al empleado (borrado lógico). Devuelve True si existía."""


class DepartamentoRepositorioBase(ABC):

    @abstractmethod
    def guardar(self, departamento):
        """Registra un departamento nuevo y le asigna su id."""

    @abstractmethod
    def obtener(self, id):
        """Devuelve el departamento con ese id, o None si no existe."""

    @abstractmethod
    def listar(self, nombre_contiene=None):
        """Devuelve los departamentos, opcionalmente filtrados por nombre."""

    @abstractmethod
    def actualizar(self, departamento):
        """Actualiza un departamento y devuelve las filas modificadas."""

    @abstractmethod
    def eliminar(self, id):
        """Elimina el departamento. Devuelve True si existía."""
