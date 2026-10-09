from datetime import date

from dominio.empleado import Empleado
from dominio.departamento import Departamento
from dominio.persona import Persona
from dominio.registro_tiempo import RegistroTiempo

def main():
    ...

if __name__ == "__main__":
    main()


repo = EmpleadoRepositorio()

ana = Empleado("12345678-9", "Ana Rojas", date(2024,3,1),950_000)
repo.guardar(ana)
print(repo.obtener("12345678-9"))
print(len(repo.listar()))
ana.sueldo_base = 1_050_000
repo.actualizar(ana)
print(repo.eliminar("12345678-9"))

    