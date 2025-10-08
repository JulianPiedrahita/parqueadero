"""
Generación de ticket con código de barras para impresión.
"""
from reportlab.lib.pagesizes import A7
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image
import io
import os
from parqueadero_app.db import db_functions as db

def generar_ticket_pdf(placa, tipo, hora_entrada, hora_salida=None, valor=None, ticket_id=None, ruta="ticket.pdf", tarifa_hora=None, tiempo_total=None):
    """
    Genera un ticket PDF con código de barras.
    
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
            c.drawString(10*mm, y_pos, f"TOTAL: ${valor:,.0f}")
            c.setFont("Helvetica", 9)
            y_pos -= 4*mm
    else:
        # Ticket de entrada - mostrar tarifa por hora
        if tarifa_hora:
            c.drawString(10*mm, y_pos, f"Tarifa/hora: ${tarifa_hora:,.0f}")
            y_pos -= 4*mm
    
    if not ticket_id:
        ticket_id = f"{placa}-{hora_entrada}"
    
    # Generar código de barras
    barcode_img = generar_codigo_barras(ticket_id)
    c.drawInlineImage(barcode_img, 10*mm, 30*mm, width=50*mm, height=20*mm)
    c.setFont("Helvetica", 7)
    c.drawString(10*mm, 25*mm, f"Codigo: {ticket_id}")
    
    # Descargo de responsabilidad
    c.setFont("Helvetica", 6)
    disclaimer = "El parqueadero no se hace responsable por daños,"
    disclaimer2 = "robos o pérdidas de objetos dentro del vehículo."
    c.drawString(10*mm, 18*mm, disclaimer)
    c.drawString(10*mm, 15*mm, disclaimer2)
    
    c.save()
    return ruta

def generar_codigo_barras(data):
    """
    Genera un código de barras Code128 como imagen PIL.
    
    Args:
        data: Texto a codificar en el código de barras
    
    Returns:
        Imagen PIL del código de barras
    """
    barcode = Code128(data, writer=ImageWriter())
    output = io.BytesIO()
    barcode.write(output, options={"module_height": 10.0, "font_size": 8, "text_distance": 1})
    output.seek(0)
    img = Image.open(output)
    return img

if __name__ == "__main__":
    generar_ticket_pdf("ABC123", "carro", "2025-10-08 08:00:00", valor=5000, ticket_id="ABC123-20251008T0800")
    print("Ticket generado en ticket.pdf")
