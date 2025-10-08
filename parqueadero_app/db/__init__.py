# Paquete de persistencia y acceso a base de datos
import sqlite3
from datetime import datetime

DB_PATH = "parqueadero.db"

class DBConnection:
	def __enter__(self):
		self.conn = sqlite3.connect(DB_PATH)
		self.c = self.conn.cursor()
		return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_type is None:
			self.conn.commit()
		self.conn.close()

def registrar_entrada(placa: str, tipo: str, hora_entrada: str, tarifa_id: int = None):
	with DBConnection() as db:
		# Insertar o buscar vehículo
		db.c.execute("SELECT id FROM vehiculos WHERE placa = ?", (placa,))
		row = db.c.fetchone()
		if row:
			vehiculo_id = row[0]
		else:
			db.c.execute("INSERT INTO vehiculos (placa, tipo) VALUES (?, ?)", (placa, tipo))
			vehiculo_id = db.c.lastrowid
		# Insertar ticket
		db.c.execute("INSERT INTO tickets (vehiculo_id, hora_entrada, tarifa_id) VALUES (?, ?, ?)", (vehiculo_id, hora_entrada, tarifa_id))

def registrar_salida(placa: str, hora_salida: str, cobro: float):
	with DBConnection() as db:
		# Buscar ticket abierto
		db.c.execute("""
			SELECT t.id FROM tickets t
			JOIN vehiculos v ON t.vehiculo_id = v.id
			WHERE v.placa = ? AND t.hora_salida IS NULL
			ORDER BY t.hora_entrada DESC LIMIT 1
		""", (placa,))
		row = db.c.fetchone()
		if row:
			ticket_id = row[0]
			db.c.execute("UPDATE tickets SET hora_salida = ?, cobro = ? WHERE id = ?", (hora_salida, cobro, ticket_id))

def guardar_tarifas(tipo_vehiculo: str, valor_hora: float, valor_fraccion: float):
	with DBConnection() as db:
		# Actualizar o insertar tarifa
		db.c.execute("SELECT id FROM tarifas WHERE tipo_vehiculo = ?", (tipo_vehiculo,))
		row = db.c.fetchone()
		if row:
			db.c.execute("UPDATE tarifas SET valor_hora = ?, valor_fraccion = ? WHERE id = ?", (valor_hora, valor_fraccion, row[0]))
		else:
			db.c.execute("INSERT INTO tarifas (tipo_vehiculo, valor_hora, valor_fraccion) VALUES (?, ?, ?)", (tipo_vehiculo, valor_hora, valor_fraccion))

def obtener_tarifa(tipo_vehiculo: str):
	with DBConnection() as db:
		db.c.execute("SELECT valor_hora, valor_fraccion FROM tarifas WHERE tipo_vehiculo = ?", (tipo_vehiculo,))
		row = db.c.fetchone()
		if row:
			return row[0], row[1]
		return None, None