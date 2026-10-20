from dominio.departamento import Departamento
from infraestructura.supabase_cliente import operacion_supabase


class DepartamentoRepositorioSupabase:

    def guardar(self, departamento):
        with operacion_supabase() as db:
            res = db.table("departamento").insert(
                {"nombre": departamento.nombre, "gerente": departamento.gerente}
            ).execute()
        departamento.id = res.data[0]["id"]
        return departamento

    def obtener(self, id):
        id_valido = self._validar_id(id)
        if id_valido is None:
            return None
        with operacion_supabase() as db:
            res = db.table("departamento").select("*").eq("id", id_valido).execute()
        return self._fila_a_departamento(res.data[0]) if res.data else None

    def listar(self, nombre_contiene=None):
        with operacion_supabase() as db:
            consulta = db.table("departamento").select("*")
            if nombre_contiene:
                consulta = consulta.ilike("nombre", f"%{nombre_contiene}%")
            res = consulta.order("nombre").execute()
        return [self._fila_a_departamento(fila) for fila in res.data]

    def actualizar(self, departamento):
        with operacion_supabase() as db:
            res = (
                db.table("departamento")
                .update({"nombre": departamento.nombre, "gerente": departamento.gerente})
                .eq("id", departamento.id)
                .execute()
            )
        return len(res.data)

    def eliminar(self, id):
        id_valido = self._validar_id(id)
        if id_valido is None:
            return False
        with operacion_supabase() as db:
            res = db.table("departamento").delete().eq("id", id_valido).execute()
        return len(res.data) > 0

    @staticmethod
    def _validar_id(id):
        try:
            return int(id)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _fila_a_departamento(fila):
        return Departamento(
            id=fila["id"],
            nombre=fila["nombre"],
            gerente=fila["gerente"],
        )
