# Parqueadero App

Software de gestión para parqueaderos (carros y motos), 100% offline, modular y escalable.

## Estructura del proyecto

- `core/`: Modelos y lógica de negocio
- `db/`: Persistencia y scripts de base de datos
- `ui/`: Interfaz de usuario de escritorio (Tkinter)
- `reports/`: Generación de reportes (PDF/Excel)
- `migrations/`: Scripts de migración y cambios de esquema

## Instalación

1. Instala Python 3.9+
2. Clona este repositorio
3. Ejecuta `python db/init_db.py` para crear la base de datos
4. Ejecuta `python ui/app.py` para iniciar la aplicación

## Uso
- Registra entradas y salidas de vehículos
- Configura tarifas
- Consulta reportes diarios

## Escalabilidad
- Arquitectura preparada para migrar a PostgreSQL y/o FastAPI en el futuro

## Dependencias
- Python estándar (sqlite3, tkinter, openpyxl, reportlab)

## Licencia
MIT
