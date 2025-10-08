"""
Script de inicio para la aplicación de parqueadero.
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar y ejecutar la aplicación
from parqueadero_app.ui.app import ParqueaderoApp

if __name__ == "__main__":
    app = ParqueaderoApp()
    app.mainloop()
