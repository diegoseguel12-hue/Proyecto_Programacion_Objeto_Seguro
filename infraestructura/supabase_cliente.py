import os
from contextlib import contextmanager
from functools import lru_cache

import httpx
from dotenv import load_dotenv
from postgrest.exceptions import APIError
from supabase import create_client

from infraestructura.conexion import ErrorDeConexion

load_dotenv()


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
        raise ErrorDeConexion(f"No se pudo operar sobre la base: {e.message}") from e
    except httpx.HTTPError as e:
        raise ErrorDeConexion(f"No se pudo conectar con Supabase: {e}") from e
