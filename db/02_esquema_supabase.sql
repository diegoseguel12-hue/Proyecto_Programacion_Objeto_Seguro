CREATE TABLE IF NOT EXISTS persona (
    rut     TEXT PRIMARY KEY,
    nombre  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS departamento (
    id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre   TEXT NOT NULL UNIQUE,
    gerente  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS empleado (
    rut              TEXT PRIMARY KEY REFERENCES persona(rut),
    fecha_ingreso    DATE NOT NULL,
    sueldo_base      INTEGER NOT NULL CHECK (sueldo_base > 0),
    departamento_id  BIGINT REFERENCES departamento(id),
    activo           BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS usuario (
    id               BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rut_empleado     TEXT NOT NULL REFERENCES empleado(rut),
    usuario          TEXT NOT NULL UNIQUE,
    contrasena_hash  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS proyecto (
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre        TEXT NOT NULL,
    descripcion   TEXT,
    fecha_inicio  DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS registro_tiempo (
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    empleado_rut  TEXT NOT NULL REFERENCES empleado(rut) ON DELETE CASCADE,
    proyecto_id   BIGINT NOT NULL REFERENCES proyecto(id),
    horas         NUMERIC(5,2) NOT NULL CHECK (horas > 0),
    fecha         DATE NOT NULL,
    descripcion   TEXT NOT NULL
);

ALTER TABLE persona          ENABLE ROW LEVEL SECURITY;
ALTER TABLE departamento     ENABLE ROW LEVEL SECURITY;
ALTER TABLE empleado         ENABLE ROW LEVEL SECURITY;
ALTER TABLE usuario          ENABLE ROW LEVEL SECURITY;
ALTER TABLE proyecto         ENABLE ROW LEVEL SECURITY;
ALTER TABLE registro_tiempo  ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS app_crud ON persona;
DROP POLICY IF EXISTS app_crud ON departamento;
DROP POLICY IF EXISTS app_crud ON empleado;
DROP POLICY IF EXISTS app_crud ON proyecto;
DROP POLICY IF EXISTS app_crud ON registro_tiempo;

CREATE POLICY app_crud ON persona          FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY app_crud ON departamento     FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY app_crud ON empleado         FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY app_crud ON proyecto         FOR ALL TO anon USING (true) WITH CHECK (true);
CREATE POLICY app_crud ON registro_tiempo  FOR ALL TO anon USING (true) WITH CHECK (true);
