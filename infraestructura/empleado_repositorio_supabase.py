from datetime import date
from postgrest.exceptions import APIError
from dominio.empleado import Empleado
from dominio.excepciones import RutDuplicadoError
from infraestructura.base import EmpleadoRepositorioBase
from infraestructura.supabase_cliente import operacion_supabase

COLUMNAS = "rut, fecha_ingreso, sueldo_base, persona!inner(nombre)"


class EmpleadoRepositorioSupabase(EmpleadoRepositorioBase):

    def guardar(self, empleado):
        with operacion_supabase() as db:
            existente = (
                db.table("empleado").select("activo")
                .eq("rut", empleado.rut).execute()
            )
            if existente.data and existente.data[0]["activo"]:
                raise RutDuplicadoError(
                    f"Ya existe un empleado activo con el RUT {empleado.rut}"
                )
            if existente.data:
                # Fue dado de baja (borrado lógico): se reactiva con los datos nuevos
                db.table("persona").update(
                    {"nombre": empleado.nombre}
                ).eq("rut", empleado.rut).execute()
                db.table("empleado").update({
                    "fecha_ingreso": empleado.fecha_ingreso.isoformat(),
                    "sueldo_base": empleado.sueldo_base,
                    "activo": True,
                }).eq("rut", empleado.rut).execute()
                return empleado
            db.table("persona").insert(
                {"rut": empleado.rut, "nombre": empleado.nombre}
            ).execute()
            try:
                db.table("empleado").insert({
                    "rut": empleado.rut,
                    "fecha_ingreso": empleado.fecha_ingreso.isoformat(),
                    "sueldo_base": empleado.sueldo_base,
                }).execute()
            except APIError:
                # Supabase no ofrece transacciones desde este cliente: si falla
                # la segunda escritura, se deshace a mano la primera.
                db.table("persona").delete().eq("rut", empleado.rut).execute()
                raise
        return empleado

    def obtener(self, rut):
        with operacion_supabase() as db:
            res = (
                db.table("empleado").select(COLUMNAS)
                .eq("rut", rut).eq("activo", True)
                .execute()
            )
        return self._fila_a_empleado(res.data[0]) if res.data else None

    def listar(self, nombre_contiene=None):
        with operacion_supabase() as db:
            consulta = db.table("empleado").select(COLUMNAS).eq("activo", True)
            if nombre_contiene:
                consulta = consulta.ilike("persona.nombre", f"%{nombre_contiene}%")
            res = consulta.execute()
        empleados = [self._fila_a_empleado(fila) for fila in res.data]
        return sorted(empleados, key=lambda e: e.nombre)

    def actualizar(self, empleado):
        with operacion_supabase() as db:
            db.table("persona").update(
                {"nombre": empleado.nombre}
            ).eq("rut", empleado.rut).execute()
            res = (
                db.table("empleado").update({
                    "fecha_ingreso": empleado.fecha_ingreso.isoformat(),
                    "sueldo_base": empleado.sueldo_base,
                })
                .eq("rut", empleado.rut).eq("activo", True)
                .execute()
            )
        return len(res.data)

    def eliminar(self, rut):
        with operacion_supabase() as db:
            res = (
                db.table("empleado").update({"activo": False})
                .eq("rut", rut).eq("activo", True)
                .execute()
            )
        return len(res.data) > 0

    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(
            rut=fila["rut"],
            nombre=fila["persona"]["nombre"],
            fecha_ingreso=date.fromisoformat(fila["fecha_ingreso"]),
            sueldo_base=fila["sueldo_base"],
        )
