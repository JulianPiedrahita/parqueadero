"""
Script de prueba para verificar la funcionalidad del sistema.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Probar importaciones
print("=== PRUEBA DE IMPORTACIONES ===")
try:
    from parqueadero_app.db import db_functions as db
    print("✓ db_functions importado correctamente")
except Exception as e:
    print(f"✗ Error al importar db_functions: {e}")

try:
    from parqueadero_app.reports.ticket import generar_ticket_pdf
    print("✓ generar_ticket_pdf importado correctamente")
except Exception as e:
    print(f"✗ Error al importar generar_ticket_pdf: {e}")

try:
    from parqueadero_app.ui.app import ParqueaderoApp
    print("✓ ParqueaderoApp importado correctamente")
except Exception as e:
    print(f"✗ Error al importar ParqueaderoApp: {e}")

# Probar generación de ticket
print("\n=== PRUEBA DE GENERACIÓN DE TICKET ===")
try:
    ruta = generar_ticket_pdf("ABC123", "carro", "2025-10-08 14:30:00", tarifa_hora=3000, ruta="test_ticket_entrada.pdf")
    print(f"✓ Ticket de entrada generado en: {ruta}")
    if os.path.exists(ruta):
        print(f"✓ Archivo existe: {os.path.getsize(ruta)} bytes")
    else:
        print("✗ Archivo NO existe")
except Exception as e:
    print(f"✗ Error al generar ticket: {e}")

# Probar ticket de salida
try:
    ruta = generar_ticket_pdf("ABC123", "carro", "2025-10-08 14:30:00", 
                              hora_salida="2025-10-08 16:45:00",
                              valor=9000, 
                              tiempo_total="2h 15min",
                              ruta="test_ticket_salida.pdf")
    print(f"✓ Ticket de salida generado en: {ruta}")
    if os.path.exists(ruta):
        print(f"✓ Archivo existe: {os.path.getsize(ruta)} bytes")
    else:
        print("✗ Archivo NO existe")
except Exception as e:
    print(f"✗ Error al generar ticket de salida: {e}")

print("\n=== PRUEBA COMPLETADA ===")
print("Si todas las pruebas pasaron, el código funciona correctamente.")
print("El problema puede estar en el ejecutable o en la configuración.")
