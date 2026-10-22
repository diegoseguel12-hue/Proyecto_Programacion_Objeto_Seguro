import os
from contextlib import contextmanager
from functools import lru_cache

import httpx
from dotenv import load_dotenv
from postgrest.exceptions import APIError
from supabase import create_client

from infraestructura.conexion import ErrorDeConexion, ErrorDeIntegridad

load_dotenv()

# Códigos de PostgreSQL para restricciones: not null, llave foránea, única y check
CODIGOS_INTEGRIDAD = {"23502", "23503", "23505", "23514"}


@lru_cache(maxsize=1)
def obtener_cliente():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ErrorDeConexion("Faltan SUPABASE_URL o SUPABASE_KEY en el .env")
    return create_client(url, key)


@contextmanager
def operacion_supabase():
    try:
        yield obtener_cliente()
    except APIError as e:
        mensaje = f"No se pudo operar sobre la base: {e.message}"
        if str(e.code) in CODIGOS_INTEGRIDAD:
            raise ErrorDeIntegridad(mensaje) from e
        raise ErrorDeConexion(mensaje) from e
    except httpx.HTTPError as e:
        raise ErrorDeConexion(f"No se pudo conectar con Supabase: {e}") from e
