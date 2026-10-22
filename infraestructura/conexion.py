import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

RUTA_ESQUEMA = Path(__file__).resolve().parent.parent / "db" / "01_esquema.sql"


class ErrorDeConexion(Exception):
    pass


class ErrorDeIntegridad(ErrorDeConexion):
    """La base rechazó la operación por una restricción (clave duplicada,
    llave foránea, campo obligatorio, etc.)."""


@contextmanager
def obtener_conexion():
    # Si no hay .env, se usa un archivo local por defecto para que el
    # proyecto también corra en un computador limpio.
    ruta = os.environ.get("DB_NOMBRE", "ecotech.db")
    conn = None
    try:
        conn = sqlite3.connect(ruta)
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
        conn.commit()
    except sqlite3.IntegrityError as e:
        if conn:
            conn.rollback()
        raise ErrorDeIntegridad(f"No se pudo operar sobre la base: {e}") from e
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise ErrorDeConexion(f"No se pudo operar sobre la base: {e}") from e
    finally:
        if conn:
            conn.close()


def inicializar_bd():
    """Crea las tablas de SQLite si todavía no existen (es seguro repetirla,
    porque el esquema usa CREATE TABLE IF NOT EXISTS)."""
    try:
        sql = RUTA_ESQUEMA.read_text(encoding="utf-8")
    except OSError as e:
        raise ErrorDeConexion(f"No se pudo leer el esquema {RUTA_ESQUEMA}: {e}") from e
    with obtener_conexion() as conn:
        conn.executescript(sql)
