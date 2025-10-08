"""
Ejemplo de exportación de reporte diario a Excel usando openpyxl.
"""
from openpyxl import Workbook
from datetime import datetime

def exportar_reporte_excel(fecha: datetime, total_recaudado: float, total_vehiculos: int, ruta: str = "reporte_diario.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte Diario"
    ws.append(["Fecha", "Total Recaudado", "Total Vehículos"])
    ws.append([fecha.strftime("%Y-%m-%d"), total_recaudado, total_vehiculos])
    wb.save(ruta)

if __name__ == "__main__":
    exportar_reporte_excel(datetime.now(), 150000, 42)
    print("Reporte de ejemplo exportado a reporte_diario.xlsx")
