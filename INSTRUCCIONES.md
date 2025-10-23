# Sistema de Parqueadero - Instrucciones de Uso

## Características Principales

- ✅ Gestión de entradas y salidas de vehículos (carros y motos)
- ✅ Sistema de numeración automática de tickets (formato 0001, 0002, etc.)
- ✅ Búsqueda rápida por placa
- ✅ Tabla visual con código de colores:
  - **Verde**: Vehículos actualmente en el parqueadero
  - **Rojo**: Vehículos que ya salieron
- ✅ Cálculo automático de tarifas diferenciadas (carro/moto)
- ✅ Sistema de pago con cálculo de cambio en tiempo real
- ✅ Generación e impresión de tickets en PDF
- ✅ Configuración personalizable del parqueadero
- ✅ Base de datos SQLite local (funciona sin internet)

## Instalación y Ejecución

### Opción 1: Ejecutar desde código fuente

1. Asegúrate de tener Python 3.12 instalado
2. Instala las dependencias:
   ```bash
   pip install reportlab PyMuPDF pillow
   ```
3. Ejecuta la aplicación:
   ```bash
   python run_app.py
   ```

### Opción 2: Ejecutar el archivo .exe (recomendado)

1. Descarga el archivo `ParqueaderoApp.exe`
2. Haz doble clic para ejecutar
3. La base de datos se creará automáticamente en la misma carpeta

## Guía de Uso

### 1. Configuración Inicial

Al iniciar por primera vez, ve a la pestaña **"Configuración"**:

1. Ingresa los datos de tu parqueadero:
   - Nombre del parqueadero
   - NIT/RUT
   - Dirección
   - Teléfono
2. Haz clic en **"Guardar Configuración"**

### 2. Configurar Tarifas

En la pestaña **"Tarifas"**:

1. Establece la tarifa por hora para **carros**
2. Establece la tarifa por hora para **motos**
3. Haz clic en **"Guardar Tarifas"**

### 3. Registrar Entrada de Vehículo

En la pestaña **"Registro"**:

1. Ingresa la **placa** del vehículo (se convierte automáticamente a mayúsculas)
2. Selecciona el **tipo** (carro o moto)
3. Haz clic en **"Registrar Entrada"**
4. El sistema:
   - Asigna automáticamente un número de ticket (ej: 0001, 0002)
   - Guarda la entrada en la base de datos
   - Genera un ticket PDF con código QR
   - Muestra una vista previa del ticket
5. Puedes imprimir el ticket directamente

### 4. Buscar Vehículo por Placa

En la sección **"Buscar por Placa"** (parte superior):

1. Ingresa la placa del vehículo
2. Haz clic en **"Buscar"**
3. La tabla mostrará todos los tickets relacionados con esa placa

### 5. Registrar Salida de Vehículo

En la pestaña **"Registro"**:

1. Ingresa la **placa** del vehículo
2. Haz clic en **"Registrar Salida"**
3. El sistema calcula automáticamente:
   - Tiempo de permanencia
   - Valor a pagar según la tarifa
4. En el diálogo de pago:
   - El sistema muestra el valor a pagar
   - Ingresa el **monto con que paga el cliente**
   - El sistema calcula automáticamente el cambio:
     - **Verde**: Cambio correcto
     - **Rojo**: Pago insuficiente
5. Haz clic en **"Confirmar"**
6. El sistema genera un ticket de salida con todos los detalles

### 6. Tabla de Tickets Recientes

En la parte inferior de la pestaña **"Registro"**:

- **Verde**: Vehículos que están actualmente en el parqueadero
- **Rojo**: Vehículos que ya salieron
- Columnas:
  - **Número**: Número de ticket (4 dígitos)
  - **Placa**: Placa del vehículo
  - **Tipo**: Carro o moto
  - **Hora Entrada**: Fecha y hora de ingreso
  - **Hora Salida**: Fecha y hora de salida (o "En parqueadero")

### 7. Generar Reportes

En la pestaña **"Reportes"**:

1. Haz clic en **"Generar Reporte"**
2. Se genera un reporte diario con todas las transacciones

## Cálculo de Tarifas

El sistema calcula el cobro de la siguiente manera:

- **Tarifa completa** por cada hora
- **Media tarifa** por fracción de hora
- Ejemplo con tarifa de $3,000/hora:
  - 1 hora 15 minutos = $3,000 + $1,500 = $4,500
  - 2 horas exactas = $6,000
  - 30 minutos = $1,500

## Tickets Impresos

Cada ticket incluye:

- **Número de ticket** (4 dígitos)
- Datos del parqueadero (nombre, NIT, dirección, teléfono)
- Placa del vehículo
- Tipo de vehículo
- Hora de entrada
- **Ticket de entrada**: Tarifa por hora
- **Ticket de salida**: 
  - Hora de salida
  - Tiempo total
  - Valor a pagar
  - Pago recibido
  - Cambio
- Descargo de responsabilidad legal

## Migración de Base de Datos Existente

Si ya tenías una base de datos anterior sin números de ticket:

```bash
python parqueadero_app/migrations/add_numero_ticket.py
```

Este script:
- Agrega la columna `numero_ticket` a la tabla
- Asigna números correlativos a tickets existentes

## Compilar Ejecutable

Para crear tu propio archivo .exe:

```bash
pip install pyinstaller
pyinstaller --name=ParqueaderoApp --onefile --windowed run_app.py
```

El ejecutable se generará en la carpeta `dist/`

## Soporte y Troubleshooting

### La aplicación no inicia
- Verifica que tengas Python 3.12 instalado
- Asegúrate de haber instalado todas las dependencias

### Error al generar tickets
- Verifica que la carpeta tenga permisos de escritura
- Asegura que reportlab esté instalado correctamente

### Base de datos corrupta
- Haz una copia de seguridad de `parqueadero.db`
- Elimina el archivo y deja que la aplicación cree uno nuevo
- Puedes exportar los datos antiguos desde la copia

## Estructura de Archivos

```
parqueadero/
├── parqueadero_app/
│   ├── core/          # Modelos de dominio
│   ├── db/            # Funciones de base de datos
│   ├── ui/            # Interfaz gráfica
│   ├── reports/       # Generación de tickets
│   └── migrations/    # Scripts de migración
├── parqueadero.db     # Base de datos SQLite
├── ticket.pdf         # Último ticket generado
└── run_app.py         # Punto de entrada
```

## Licencia

Este software se proporciona "tal cual" sin garantías de ningún tipo.

## Desarrollado por

Sistema de Gestión de Parqueadero - 2025
