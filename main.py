from datetime import date
from infraestructura.repositorios import crear_repositorios
from infraestructura.conexion import ErrorDeConexion
from dominio.empleado import Empleado
from dominio.departamento import Departamento


def probar_empleados(repo):
    print("--- Empleados ---")
    ana = Empleado("12345678-9", "Ana Rojas", date(2024, 3, 1), 950_000)
    repo.guardar(ana)
    print(repo.obtener("12345678-9"))
    print(len(repo.listar()))
    print(len(repo.listar(nombre_contiene="Ana")))
    print(repo.listar(nombre_contiene="' OR '1'='1"))
    print(repo.obtener("' OR '1'='1"))
    ana.sueldo_base = 1_050_000
    repo.actualizar(ana)
    print(repo.eliminar("12345678-9"))
    print(repo.obtener("12345678-9"))


def probar_departamentos(repo):
    print("--- Departamentos ---")
    ti = Departamento(None, "Tecnología", "Pedro Soto")
    repo.guardar(ti)
    print(ti.id, ti.nombre, ti.gerente)
    print(len(repo.listar()))
    print(repo.listar(nombre_contiene="' OR '1'='1"))
    print(repo.obtener("' OR '1'='1"))
    ti.gerente = "María Pérez"
    print(repo.actualizar(ti))
    print(repo.obtener(ti.id).gerente)
    print(repo.eliminar(ti.id))
    print(repo.obtener(ti.id))


def main():
    try:
        repo_empleados, repo_departamentos = crear_repositorios()
    except ErrorDeConexion as e:
        print("Error de configuración:", e)
        return

    for prueba, repo in ((probar_empleados, repo_empleados),
                         (probar_departamentos, repo_departamentos)):
        try:
            prueba(repo)
        except ErrorDeConexion as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
