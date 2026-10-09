import os
import sqlite3
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()


class ErrorDeConexion(Exception):
    pass


@contextmanager
def obtener_conexion():
    ruta = os.environ.get("DB_NOMBRE")
    if not ruta:
        raise ErrorDeConexion("Falta la variable DB_NOMBRE. ¿Copiaste el .env.example?")
    conn = None
    try:
        conn = sqlite3.connect(ruta)
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise ErrorDeConexion(f"No se pudo operar sobre la base: {e}") from e
    finally:
        if conn:
            conn.close()


from infraestructura.conexion import obtener_conexion

with obtener_conexion() as conn:
    conn.execute(
        "INSERT INTO persona (rut, nombre) VALUES (?, ?)",
        ("12345678-9", "Ana Rojas")
    )
with obtener_conexion() as conn:
        filas = conn.execute("SELECT rut, nombre FROM persona").fetchall()
        for fila in filas:
            print(fila)
    