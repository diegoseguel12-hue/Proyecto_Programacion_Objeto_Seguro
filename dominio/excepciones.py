"""
Excepciones propias del dominio de EcoTech.

Permiten que el resto del programa hable el idioma del negocio
(RUT duplicado, dato inválido) en vez de depender de los errores
crudos de la base de datos.
"""


class EcoTechError(Exception):
    """Excepción base para todos los errores del negocio de EcoTech."""


class DatoInvalidoError(EcoTechError, ValueError):
    """Se lanza cuando un dato no cumple las reglas del negocio
    (RUT mal formado, nombre vacío, sueldo menor o igual a 0, etc.)."""


class RutDuplicadoError(EcoTechError):
    """Se lanza al intentar registrar un empleado con un RUT que ya está activo."""


class EmpleadoNoEncontradoError(EcoTechError):
    """Se lanza al operar sobre un empleado que no existe o está dado de baja."""
