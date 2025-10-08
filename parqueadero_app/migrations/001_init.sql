-- Script de migración inicial para la base de datos del parqueadero
CREATE TABLE IF NOT EXISTS vehiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT NOT NULL,
    tipo TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tarifas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_vehiculo TEXT NOT NULL,
    valor_hora REAL NOT NULL,
    valor_fraccion REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehiculo_id INTEGER NOT NULL,
    hora_entrada TEXT NOT NULL,
    hora_salida TEXT,
    tarifa_id INTEGER,
    cobro REAL,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id),
    FOREIGN KEY (tarifa_id) REFERENCES tarifas(id)
);
