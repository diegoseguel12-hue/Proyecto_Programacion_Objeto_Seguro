from datetime import date
from dominio.empleado import Empleado
from infraestructura.supabase_cliente import operacion_supabase

COLUMNAS = "rut, fecha_ingreso, sueldo_base, persona!inner(nombre)"


class EmpleadoRepositorioSupabase:

    def guardar(self, empleado):
        with operacion_supabase() as db:
            existente = (
                db.table("empleado").select("activo")
                .eq("rut", empleado.rut).execute()
            )
            if existente.data and not existente.data[0]["activo"]:
                # El empleado fue dado de baja (borrado logico): se reactiva
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
            except Exception:
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
