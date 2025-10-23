# Módulo de funciones de base de datos para importación estándar
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
		# Obtener el último número de ticket y sumar 1
		db.c.execute("SELECT MAX(numero_ticket) FROM tickets")
		max_num = db.c.fetchone()[0]
		numero_ticket = 1 if max_num is None else max_num + 1
		# Insertar ticket
		db.c.execute("INSERT INTO tickets (numero_ticket, vehiculo_id, hora_entrada, tarifa_id) VALUES (?, ?, ?, ?)", (numero_ticket, vehiculo_id, hora_entrada, tarifa_id))
		return numero_ticket

def registrar_salida(placa: str, hora_salida: str, cobro: float, pago_recibido: float = None, cambio: float = None):
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
			db.c.execute("UPDATE tickets SET hora_salida = ?, cobro = ?, pago_recibido = ?, cambio = ? WHERE id = ?", (hora_salida, cobro, pago_recibido, cambio, ticket_id))

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

def guardar_configuracion(nombre: str, nit: str, direccion: str, telefono: str):
	with DBConnection() as db:
		# Actualizar la configuración (siempre hay un solo registro)
		db.c.execute("UPDATE configuracion SET nombre_parqueadero = ?, nit = ?, direccion = ?, telefono = ? WHERE id = 1", (nombre, nit, direccion, telefono))

def obtener_configuracion():
	with DBConnection() as db:
		db.c.execute("SELECT nombre_parqueadero, nit, direccion, telefono FROM configuracion WHERE id = 1")
		row = db.c.fetchone()
		if row:
			return {"nombre": row[0], "nit": row[1], "direccion": row[2], "telefono": row[3]}
		return {"nombre": "PARQUEADERO", "nit": "", "direccion": "", "telefono": ""}

def obtener_tickets_activos():
	with DBConnection() as db:
		db.c.execute("""
			SELECT t.numero_ticket, v.placa, v.tipo, t.hora_entrada, t.hora_salida
			FROM tickets t
			JOIN vehiculos v ON t.vehiculo_id = v.id
			ORDER BY t.hora_entrada DESC
			LIMIT 50
		""")
		return db.c.fetchall()

def buscar_ticket_por_placa(placa: str):
	with DBConnection() as db:
		db.c.execute("""
			SELECT t.numero_ticket, v.placa, v.tipo, t.hora_entrada, t.hora_salida, t.cobro
			FROM tickets t
			JOIN vehiculos v ON t.vehiculo_id = v.id
			WHERE v.placa = ?
			ORDER BY t.hora_entrada DESC
			LIMIT 10
		""", (placa,))
		return db.c.fetchall()