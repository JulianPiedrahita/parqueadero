"""
Modelos principales del dominio del parqueadero.
"""
from datetime import datetime
from typing import Optional

class Vehiculo:
    """Representa un vehículo que ingresa al parqueadero."""
    def __init__(self, placa: str, tipo: str):
        self.placa = placa.upper()
        self.tipo = tipo  # 'carro' o 'moto'

class Tarifa:
    """Representa la tarifa para un tipo de vehículo."""
    def __init__(self, tipo_vehiculo: str, valor_hora: float, valor_fraccion: float):
        self.tipo_vehiculo = tipo_vehiculo
        self.valor_hora = valor_hora
        self.valor_fraccion = valor_fraccion

class Ticket:
    """Representa un ticket de entrada/salida de un vehículo."""
    def __init__(self, vehiculo: Vehiculo, hora_entrada: datetime, hora_salida: Optional[datetime] = None, tarifa: Optional[Tarifa] = None):
        self.vehiculo = vehiculo
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida
        self.tarifa = tarifa
        self.cobro = 0.0

    def calcular_cobro(self) -> float:
        if not self.hora_salida or not self.tarifa:
            return 0.0
        tiempo = self.hora_salida - self.hora_entrada
        minutos = tiempo.total_seconds() / 60
        horas = int(minutos // 60)
        fraccion = 1 if minutos % 60 > 0 else 0
        self.cobro = horas * self.tarifa.valor_hora + fraccion * self.tarifa.valor_fraccion
        return self.cobro

class Reporte:
    """Representa un reporte diario de operaciones."""
    def __init__(self, fecha: datetime, total_recaudado: float, total_vehiculos: int):
        self.fecha = fecha
        self.total_recaudado = total_recaudado
        self.total_vehiculos = total_vehiculos
