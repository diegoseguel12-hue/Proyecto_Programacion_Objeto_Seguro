"""
Esta pestaña contiene la clase registro_tiempo 
junto con sus atributos y métodos
"""

class RegistroTiempo():

    def __init__(self, id, horas_trabajadas, fecha, descripcion, empleado_rut, proyecto_id):

        self.id = id
        self.horas_trabajadas = horas_trabajadas
        self.fecha = fecha
        self.descripcion = descripcion
        self.empleado_rut = empleado_rut
        self.proyecto_id = proyecto_id
    