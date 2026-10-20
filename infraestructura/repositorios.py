import os
from dotenv import load_dotenv
from infraestructura.conexion import ErrorDeConexion

load_dotenv()


def crear_repositorios():
    motor = os.environ.get("DB_MOTOR", "sqlite")

    if motor == "sqlite":
        from infraestructura.empleado_repositorio import EmpleadoRepositorio
        from infraestructura.departamento_repositorio import DepartamentoRepositorio
        return EmpleadoRepositorio(), DepartamentoRepositorio()

    if motor == "supabase":
        from infraestructura.empleado_repositorio_supabase import EmpleadoRepositorioSupabase
        from infraestructura.departamento_repositorio_supabase import DepartamentoRepositorioSupabase
        return EmpleadoRepositorioSupabase(), DepartamentoRepositorioSupabase()

    raise ErrorDeConexion(f"DB_MOTOR desconocido: '{motor}'. Usa 'sqlite' o 'supabase'")
