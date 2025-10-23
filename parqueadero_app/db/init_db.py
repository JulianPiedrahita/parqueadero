"""
Script de inicialización de la base de datos SQLite.
"""
import sqlite3

DB_PATH = "parqueadero.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Tabla de vehículos
    c.execute('''
        CREATE TABLE IF NOT EXISTS vehiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    ''')
    # Tabla de tarifas
    c.execute('''
        CREATE TABLE IF NOT EXISTS tarifas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_vehiculo TEXT NOT NULL,
            valor_hora REAL NOT NULL,
            valor_fraccion REAL NOT NULL
        )
    ''')
    # Tabla de tickets
    c.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_ticket INTEGER,
            vehiculo_id INTEGER NOT NULL,
            hora_entrada TEXT NOT NULL,
            hora_salida TEXT,
            tarifa_id INTEGER,
            cobro REAL,
            pago_recibido REAL,
            cambio REAL,
            FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id),
            FOREIGN KEY (tarifa_id) REFERENCES tarifas(id)
        )
    ''')
    # Tabla de configuración del parqueadero
    c.execute('''
        CREATE TABLE IF NOT EXISTS configuracion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_parqueadero TEXT NOT NULL,
            nit TEXT,
            direccion TEXT,
            telefono TEXT
        )
    ''')
    # Insertar configuración por defecto si no existe
    c.execute("SELECT COUNT(*) FROM configuracion")
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO configuracion (nombre_parqueadero, nit, direccion, telefono)
            VALUES (?, ?, ?, ?)
        ''', ("PARQUEADERO", "", "", ""))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada.")
