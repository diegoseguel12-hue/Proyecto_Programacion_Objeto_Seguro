PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS persona (
    rut          TEXT PRIMARY KEY,
    nombre       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS departamento (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre       TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS proyecto (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre       TEXT NOT NULL,
    descripcion  TEXT,
    fecha_inicio DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS empleado (
    rut             TEXT PRIMARY KEY,
    fecha_ingreso   DATE NOT NULL,
    sueldo_base     INTEGER NOT NULL,
    departamento_id INTEGER,
    FOREIGN KEY (rut) REFERENCES persona(rut),
    FOREIGN KEY (departamento_id) REFERENCES departamento(id)
);

CREATE TABLE IF NOT EXISTS registro_tiempo (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    empleado_rut TEXT NOT NULL,
    proyecto_id  INTEGER NOT NULL,
    horas        REAL NOT NULL,
    fecha        DATE NOT NULL,
    FOREIGN KEY (empleado_rut) REFERENCES empleado(rut) ON DELETE CASCADE,
    FOREIGN KEY (proyecto_id)  REFERENCES proyecto(id)
);
