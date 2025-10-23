"""
Generación de ticket para impresión.
"""
from reportlab.lib.pagesizes import A7
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
from parqueadero_app.db import db_functions as db

def generar_ticket_pdf(placa, tipo, hora_entrada, hora_salida=None, valor=None, ticket_id=None, ruta="ticket.pdf", tarifa_hora=None, tiempo_total=None, pago_recibido=None, cambio=None, numero_ticket=None):
    """
    Genera un ticket PDF.
    
    Args:
        placa: Placa del vehículo (en mayúsculas)
        tipo: Tipo de vehículo (carro/moto)
        hora_entrada: Fecha y hora de entrada
        hora_salida: Fecha y hora de salida (opcional)
        valor: Valor total a cobrar (opcional)
        ticket_id: ID único del ticket (opcional)
        ruta: Ruta donde guardar el PDF
        tarifa_hora: Valor por hora (opcional)
        tiempo_total: Tiempo total en formato texto (opcional)
        pago_recibido: Valor con que paga el cliente (opcional)
        cambio: Cambio a devolver (opcional)
        numero_ticket: Número de ticket de 4 dígitos (opcional)
    """
    # Obtener configuración del parqueadero
    config = db.obtener_configuracion()
    
    c = canvas.Canvas(ruta, pagesize=A7)
    
    # Encabezado con datos del parqueadero
    y_pos = 100*mm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(10*mm, y_pos, config["nombre"])
    y_pos -= 4*mm
    
    c.setFont("Helvetica", 8)
    if config["nit"]:
        c.drawString(10*mm, y_pos, f"NIT: {config['nit']}")
        y_pos -= 3*mm
    if config["direccion"]:
        c.drawString(10*mm, y_pos, config["direccion"])
        y_pos -= 3*mm
    if config["telefono"]:
        c.drawString(10*mm, y_pos, f"Tel: {config['telefono']}")
        y_pos -= 3*mm
    
    # Línea separadora
    y_pos -= 2*mm
    c.line(10*mm, y_pos, 64*mm, y_pos)
    y_pos -= 4*mm
    
    # Número de ticket
    if numero_ticket:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(10*mm, y_pos, f"Ticket N°: {numero_ticket:04d}")
        y_pos -= 5*mm
    
    # Datos del ticket
    c.setFont("Helvetica", 9)
    c.drawString(10*mm, y_pos, f"Placa: {placa.upper()}")
    y_pos -= 4*mm
    c.drawString(10*mm, y_pos, f"Tipo: {tipo.capitalize()}")
    y_pos -= 4*mm
    c.drawString(10*mm, y_pos, f"Entrada: {hora_entrada}")
    y_pos -= 4*mm
    
    if hora_salida:
        c.drawString(10*mm, y_pos, f"Salida: {hora_salida}")
        y_pos -= 4*mm
        if tiempo_total:
            c.drawString(10*mm, y_pos, f"Tiempo: {tiempo_total}")
            y_pos -= 4*mm
        if valor:
            c.setFont("Helvetica-Bold", 9)
            c.drawString(10*mm, y_pos, f"TOTAL A PAGAR: ${valor:,.0f}")
            c.setFont("Helvetica", 9)
            y_pos -= 5*mm
        if pago_recibido:
            c.drawString(10*mm, y_pos, f"Pago recibido: ${pago_recibido:,.0f}")
            y_pos -= 4*mm
        if cambio is not None:
            c.setFont("Helvetica-Bold", 9)
            c.drawString(10*mm, y_pos, f"CAMBIO: ${cambio:,.0f}")
            c.setFont("Helvetica", 9)
            y_pos -= 4*mm
    else:
        # Ticket de entrada - mostrar tarifa por hora
        if tarifa_hora:
            c.drawString(10*mm, y_pos, f"Tarifa/hora: ${tarifa_hora:,.0f}")
            y_pos -= 4*mm
    
    # Descargo de responsabilidad
    y_pos -= 5*mm
    c.setFont("Helvetica", 6)
    disclaimer = "El parqueadero no se hace responsable por daños,"
    disclaimer2 = "robos o pérdidas de objetos dentro del vehículo."
    c.drawString(10*mm, y_pos, disclaimer)
    y_pos -= 3*mm
    c.drawString(10*mm, y_pos, disclaimer2)
    
    c.save()
    return ruta

if __name__ == "__main__":
    generar_ticket_pdf("ABC123", "carro", "2025-10-08 08:00:00", valor=5000, ticket_id="ABC123-20251008T0800")
    print("Ticket generado en ticket.pdf")
