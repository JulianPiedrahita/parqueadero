"""
Interfaz de usuario principal para el sistema de parqueadero.
Pantallas: registro de entradas/salidas y consulta de reportes.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
from parqueadero_app.db import db_functions as db
from parqueadero_app.db.init_db import init_db
from parqueadero_app.reports.ticket import generar_ticket_pdf

class ParqueaderoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Parqueadero - Gestión de Entradas y Salidas")
        self.geometry("600x400")
        
        # Inicializar la base de datos al arrancar
        try:
            init_db()
            print("Base de datos inicializada correctamente")
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", 
                               f"No se pudo inicializar la base de datos:\n{str(e)}")
        
        self._crear_widgets()

    def _crear_widgets(self):
        tab_control = ttk.Notebook(self)
        self.tab_registro = ttk.Frame(tab_control)
        self.tab_reportes = ttk.Frame(tab_control)
        self.tab_tarifas = ttk.Frame(tab_control)
        self.tab_configuracion = ttk.Frame(tab_control)
        tab_control.add(self.tab_registro, text='Entradas/Salidas')
        tab_control.add(self.tab_reportes, text='Reportes')
        tab_control.add(self.tab_tarifas, text='Tarifas')
        tab_control.add(self.tab_configuracion, text='Configuración')
        tab_control.pack(expand=1, fill='both')
        self._crear_tab_registro()
        self._crear_tab_reportes()
        self._crear_tab_tarifas()
        self._crear_tab_configuracion()

    def _crear_tab_tarifas(self):
        frame = ttk.LabelFrame(self.tab_tarifas, text="Configurar Tarifas")
        frame.pack(padx=10, pady=10, fill='x')
        # Tarifas para carro
        ttk.Label(frame, text="Hora Carro:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.tarifa_hora_carro = tk.DoubleVar(value=3000)
        ttk.Entry(frame, textvariable=self.tarifa_hora_carro).grid(row=0, column=1, padx=5, pady=5)
        # Tarifas para moto
        ttk.Label(frame, text="Hora Moto:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.tarifa_hora_moto = tk.DoubleVar(value=2000)
        ttk.Entry(frame, textvariable=self.tarifa_hora_moto).grid(row=1, column=1, padx=5, pady=5)
        # Día, semana, mes (opcional, solo para referencia)
        ttk.Label(frame, text="Día (ref.):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.tarifa_dia = tk.DoubleVar(value=20000)
        ttk.Entry(frame, textvariable=self.tarifa_dia).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(frame, text="Semana (ref.):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.tarifa_semana = tk.DoubleVar(value=80000)
        ttk.Entry(frame, textvariable=self.tarifa_semana).grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(frame, text="Mensualidad (ref.):").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.tarifa_mes = tk.DoubleVar(value=250000)
        ttk.Entry(frame, textvariable=self.tarifa_mes).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Guardar Tarifas", command=self.guardar_tarifas).grid(row=5, column=0, columnspan=2, pady=10)

    def guardar_tarifas(self):
        # Guardar tarifas diferenciadas para carro y moto
        db.guardar_tarifas('carro', self.tarifa_hora_carro.get(), self.tarifa_hora_carro.get()/2)
        db.guardar_tarifas('moto', self.tarifa_hora_moto.get(), self.tarifa_hora_moto.get()/2)
        # Día, semana y mensualidad pueden ser extendidos en la base de datos si se requiere
        messagebox.showinfo("Tarifas guardadas", f"Hora Carro: {self.tarifa_hora_carro.get()}\nHora Moto: {self.tarifa_hora_moto.get()}\nDía: {self.tarifa_dia.get()}\nSemana: {self.tarifa_semana.get()}\nMensualidad: {self.tarifa_mes.get()}")

    def _crear_tab_configuracion(self):
        frame = ttk.LabelFrame(self.tab_configuracion, text="Datos del Parqueadero")
        frame.pack(padx=10, pady=10, fill='x')
        
        # Cargar configuración actual
        config = db.obtener_configuracion()
        
        ttk.Label(frame, text="Nombre del Parqueadero:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.nombre_parqueadero = tk.StringVar(value=config["nombre"])
        ttk.Entry(frame, textvariable=self.nombre_parqueadero, width=40).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="NIT/RUT:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.nit_parqueadero = tk.StringVar(value=config["nit"])
        ttk.Entry(frame, textvariable=self.nit_parqueadero, width=40).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Dirección:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.direccion_parqueadero = tk.StringVar(value=config["direccion"])
        ttk.Entry(frame, textvariable=self.direccion_parqueadero, width=40).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Teléfono:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.telefono_parqueadero = tk.StringVar(value=config["telefono"])
        ttk.Entry(frame, textvariable=self.telefono_parqueadero, width=40).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Button(frame, text="Guardar Configuración", command=self.guardar_configuracion).grid(row=4, column=0, columnspan=2, pady=10)
    
    def guardar_configuracion(self):
        db.guardar_configuracion(
            self.nombre_parqueadero.get(),
            self.nit_parqueadero.get(),
            self.direccion_parqueadero.get(),
            self.telefono_parqueadero.get()
        )
        messagebox.showinfo("✓ Configuración guardada", "Los datos del parqueadero han sido actualizados correctamente.")

    def _crear_tab_registro(self):
        # Frame principal con búsqueda arriba
        frame_busqueda = ttk.LabelFrame(self.tab_registro, text="Buscar por Placa")
        frame_busqueda.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(frame_busqueda, text="Placa:").grid(row=0, column=0, padx=5, pady=5)
        self.busqueda_placa_entry = ttk.Entry(frame_busqueda, width=20)
        self.busqueda_placa_entry.grid(row=0, column=1, padx=5, pady=5)
        self.busqueda_placa_entry.bind('<KeyRelease>', self._mayusculas_busqueda)
        self.btn_buscar_ticket = ttk.Button(frame_busqueda, text="Buscar", command=self.buscar_ticket_por_placa)
        self.btn_buscar_ticket.grid(row=0, column=2, padx=5, pady=5)
        
        # Frame del formulario centrado
        frame_form = ttk.LabelFrame(self.tab_registro, text="Registrar Entrada/Salida")
        frame_form.pack(padx=10, pady=10, fill='x')
        
        # Contenedor centrado
        form_container = ttk.Frame(frame_form)
        form_container.pack(expand=True)
        
        ttk.Label(form_container, text="Placa:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.placa_entry = ttk.Entry(form_container, width=20)
        self.placa_entry.grid(row=0, column=1, padx=5, pady=5)
        self.placa_entry.bind('<KeyRelease>', self._mayusculas_placa)
        
        ttk.Label(form_container, text="Tipo:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.tipo_cb = ttk.Combobox(form_container, values=["carro", "moto"], width=17)
        self.tipo_cb.grid(row=0, column=3, padx=5, pady=5)
        
        # Hora actual
        ttk.Label(form_container, text="Hora actual:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.hora_actual_var = tk.StringVar()
        self.hora_actual_var.set(datetime.now().strftime('%H:%M:%S'))
        self.hora_actual_label = ttk.Label(form_container, textvariable=self.hora_actual_var)
        self.hora_actual_label.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        # Botones
        btn_frame = ttk.Frame(form_container)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        self.btn_entrada = ttk.Button(btn_frame, text="Registrar Entrada", command=self.registrar_entrada)
        self.btn_entrada.pack(side='left', padx=10)
        self.btn_salida = ttk.Button(btn_frame, text="Registrar Salida", command=self.registrar_salida)
        self.btn_salida.pack(side='left', padx=10)
        
        # Tabla de tickets
        frame_tabla = ttk.LabelFrame(self.tab_registro, text="Tickets Recientes")
        frame_tabla.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Crear Treeview
        self.tree_tickets = ttk.Treeview(frame_tabla, columns=('Número', 'Placa', 'Tipo', 'Entrada', 'Salida'), show='headings', height=10)
        self.tree_tickets.heading('Número', text='Número')
        self.tree_tickets.heading('Placa', text='Placa')
        self.tree_tickets.heading('Tipo', text='Tipo')
        self.tree_tickets.heading('Entrada', text='Hora Entrada')
        self.tree_tickets.heading('Salida', text='Hora Salida')
        
        self.tree_tickets.column('Número', width=80, anchor='center')
        self.tree_tickets.column('Placa', width=100, anchor='center')
        self.tree_tickets.column('Tipo', width=80, anchor='center')
        self.tree_tickets.column('Entrada', width=150, anchor='center')
        self.tree_tickets.column('Salida', width=150, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical', command=self.tree_tickets.yview)
        self.tree_tickets.configure(yscrollcommand=scrollbar.set)
        
        self.tree_tickets.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar colores
        self.tree_tickets.tag_configure('activo', background='#90EE90')  # Verde claro
        self.tree_tickets.tag_configure('completado', background='#FFB6C6')  # Rojo claro
        
        # Cargar tickets iniciales
        self.actualizar_tabla_tickets()
        
        # Actualizar la hora actual cada segundo
        self._actualizar_hora_actual()

    def _mayusculas_placa(self, event):
        valor = self.placa_entry.get()
        if valor != valor.upper():
            self.placa_entry.delete(0, tk.END)
            self.placa_entry.insert(0, valor.upper())
    
    def _mayusculas_busqueda(self, event):
        valor = self.busqueda_placa_entry.get()
        if valor != valor.upper():
            self.busqueda_placa_entry.delete(0, tk.END)
            self.busqueda_placa_entry.insert(0, valor.upper())

    def buscar_ticket_por_placa(self):
        placa = self.busqueda_placa_entry.get().strip().upper()
        if not placa:
            messagebox.showerror("Error", "Debe ingresar una placa.")
            return
        
        resultados = db.buscar_ticket_por_placa(placa)
        
        if not resultados:
            messagebox.showinfo("Sin resultados", f"No se encontraron tickets para la placa {placa}.")
            return
        
        # Crear ventana emergente
        ventana = tk.Toplevel(self)
        ventana.title(f"Resultados para {placa}")
        ventana.geometry("800x400")
        ventana.transient(self)
        ventana.grab_set()
        
        # Frame para la tabla
        frame_tabla = ttk.Frame(ventana)
        frame_tabla.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Crear Treeview para resultados
        tree_resultados = ttk.Treeview(frame_tabla, columns=('Número', 'Placa', 'Tipo', 'Entrada', 'Salida', 'Cobro'), show='headings', height=15)
        tree_resultados.heading('Número', text='Número')
        tree_resultados.heading('Placa', text='Placa')
        tree_resultados.heading('Tipo', text='Tipo')
        tree_resultados.heading('Entrada', text='Hora Entrada')
        tree_resultados.heading('Salida', text='Hora Salida')
        tree_resultados.heading('Cobro', text='Valor Cobrado')
        
        tree_resultados.column('Número', width=80, anchor='center')
        tree_resultados.column('Placa', width=100, anchor='center')
        tree_resultados.column('Tipo', width=80, anchor='center')
        tree_resultados.column('Entrada', width=150, anchor='center')
        tree_resultados.column('Salida', width=150, anchor='center')
        tree_resultados.column('Cobro', width=100, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical', command=tree_resultados.yview)
        tree_resultados.configure(yscrollcommand=scrollbar.set)
        
        tree_resultados.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        # Configurar colores
        tree_resultados.tag_configure('activo', background='#90EE90')  # Verde claro
        tree_resultados.tag_configure('completado', background='#FFB6C6')  # Rojo claro
        
        # Llenar con resultados
        for row in resultados:
            numero_ticket, placa_v, tipo, hora_entrada, hora_salida, cobro = row
            numero_str = f"{numero_ticket:04d}"
            salida_str = hora_salida if hora_salida else "En parqueadero"
            cobro_str = f"${cobro:,.0f}" if cobro else "-"
            tag = 'completado' if hora_salida else 'activo'
            tree_resultados.insert('', 'end', values=(numero_str, placa_v, tipo, hora_entrada, salida_str, cobro_str), tags=(tag,))
        
        # Botón cerrar
        ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
    
    def actualizar_tabla_tickets(self):
        # Limpiar tabla
        for item in self.tree_tickets.get_children():
            self.tree_tickets.delete(item)
        
        # Obtener tickets activos
        tickets = db.obtener_tickets_activos()
        
        for row in tickets:
            numero_ticket, placa, tipo, hora_entrada, hora_salida = row
            numero_str = f"{numero_ticket:04d}"
            salida_str = hora_salida if hora_salida else "En parqueadero"
            tag = 'completado' if hora_salida else 'activo'
            self.tree_tickets.insert('', 'end', values=(numero_str, placa, tipo, hora_entrada, salida_str), tags=(tag,))

    def _actualizar_hora_actual(self):
        self.hora_actual_var.set(datetime.now().strftime('%H:%M:%S'))
        self.after(1000, self._actualizar_hora_actual)

    def _crear_tab_reportes(self):
        frame = ttk.LabelFrame(self.tab_reportes, text="Reporte Diario")
        frame.pack(padx=10, pady=10, fill='x')
        self.btn_generar_reporte = ttk.Button(frame, text="Generar Reporte", command=self.generar_reporte)
        self.btn_generar_reporte.pack(pady=10)

    def registrar_entrada(self):
        placa = self.placa_entry.get().strip().upper()
        tipo = self.tipo_cb.get().strip()
        if not placa or not tipo:
            messagebox.showerror("Error", "Debe ingresar placa y tipo de vehículo.")
            return
        hora_entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            # Registrar en base de datos y obtener número de ticket
            numero_ticket = db.registrar_entrada(placa, tipo, hora_entrada)
            # Mostrar mensaje de confirmación inmediato
            messagebox.showinfo("✓ Guardado", f"Entrada registrada\n\nTicket: {numero_ticket:04d}\nPlaca: {placa}\nTipo: {tipo}\nHora: {hora_entrada}")
            # Obtener tarifa por hora para mostrar en el ticket
            tarifa_hora, tarifa_fraccion = db.obtener_tarifa(tipo)
            if tarifa_hora is None:
                if tipo == 'carro':
                    tarifa_hora = self.tarifa_hora_carro.get() if hasattr(self, 'tarifa_hora_carro') else 3000
                elif tipo == 'moto':
                    tarifa_hora = self.tarifa_hora_moto.get() if hasattr(self, 'tarifa_hora_moto') else 2000
                else:
                    tarifa_hora = 3000
            # Generar ticket de entrada con tarifa por hora y número de ticket
            ruta_ticket = generar_ticket_pdf(placa, tipo, hora_entrada, tarifa_hora=tarifa_hora, numero_ticket=numero_ticket)
            # Previsualizar ticket en ventana emergente
            self.previsualizar_ticket(ruta_ticket)
            # Limpiar campos
            self.placa_entry.delete(0, tk.END)
            self.tipo_cb.set("")
            # Actualizar tabla de tickets
            self.actualizar_tabla_tickets()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar entrada:\n{str(e)}")

    def previsualizar_ticket(self, ruta_ticket):
        """
        Muestra el ticket en una ventana emergente dentro de la aplicación.
        """
        import tkinter as tk
        from tkinter import ttk
        from PIL import Image, ImageTk
        import fitz  # PyMuPDF para convertir PDF a imagen
        
        # Crear ventana emergente
        ventana = tk.Toplevel(self)
        ventana.title("Ticket Generado")
        ventana.geometry("400x600")
        ventana.transient(self)
        ventana.grab_set()
        
        try:
            # Convertir PDF a imagen usando PyMuPDF
            pdf_document = fitz.open(ruta_ticket)
            page = pdf_document[0]
            
            # Renderizar página a imagen con buena resolución
            zoom = 2  # Factor de zoom para mejor calidad
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convertir a PIL Image
            img_data = pix.tobytes("ppm")
            img = Image.frombytes("RGB", [pix.width, pix.height], img_data)
            
            # Redimensionar para que quepa en la ventana
            img.thumbnail((380, 500), Image.Resampling.LANCZOS)
            
            # Convertir a PhotoImage para tkinter
            photo = ImageTk.PhotoImage(img)
            
            # Crear frame con scroll
            frame = ttk.Frame(ventana)
            frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Label para mostrar la imagen
            label = ttk.Label(frame, image=photo)
            label.image = photo  # Mantener referencia
            label.pack()
            
            pdf_document.close()
            
            # Botones
            frame_botones = ttk.Frame(ventana)
            frame_botones.pack(fill='x', padx=10, pady=10)
            
            ttk.Button(frame_botones, text="Imprimir", 
                      command=lambda: self.imprimir_ticket(ruta_ticket)).pack(side='left', padx=5)
            ttk.Button(frame_botones, text="Cerrar", 
                      command=ventana.destroy).pack(side='right', padx=5)
            
        except Exception as e:
            # Si falla la conversión, mostrar el PDF externamente
            messagebox.showinfo("Ticket Generado", 
                              f"Ticket guardado en:\n{ruta_ticket}\n\nSe abrirá con el visor predeterminado.")
            import platform
            import subprocess
            if platform.system() == "Windows":
                os.startfile(ruta_ticket)
            elif platform.system() == "Darwin":
                subprocess.run(["open", ruta_ticket])
            else:
                subprocess.run(["xdg-open", ruta_ticket])
            ventana.destroy()

    def registrar_salida(self):
        placa = self.placa_entry.get().strip().upper()
        if not placa:
            messagebox.showerror("Error", "Debe ingresar la placa.")
            return
        hora_salida_dt = datetime.now()
        # Buscar ticket abierto y hora de entrada
        import sqlite3
        conn = sqlite3.connect("parqueadero.db")
        c = conn.cursor()
        c.execute("""
            SELECT t.hora_entrada, v.tipo, t.numero_ticket FROM tickets t
            JOIN vehiculos v ON t.vehiculo_id = v.id
            WHERE v.placa = ? AND t.hora_salida IS NULL
            ORDER BY t.hora_entrada DESC LIMIT 1
        """, (placa,))
        row = c.fetchone()
        conn.close()
        if not row:
            messagebox.showerror("Error", "No se encontró entrada activa para esta placa.")
            return
        hora_entrada_str, tipo, numero_ticket = row
        hora_entrada_dt = datetime.strptime(hora_entrada_str, '%Y-%m-%d %H:%M:%S')
        minutos = (hora_salida_dt - hora_entrada_dt).total_seconds() / 60
        horas = int(minutos // 60)
        minutos_restantes = int(minutos % 60)
        fraccion = 1 if minutos % 60 > 0 else 0
        tarifa_hora, tarifa_fraccion = db.obtener_tarifa(tipo)
        if tarifa_hora is None:
            if tipo == 'carro':
                tarifa_hora = self.tarifa_hora_carro.get() if hasattr(self, 'tarifa_hora_carro') else 3000
            elif tipo == 'moto':
                tarifa_hora = self.tarifa_hora_moto.get() if hasattr(self, 'tarifa_hora_moto') else 2000
            else:
                tarifa_hora = 3000
        if tarifa_fraccion is None:
            tarifa_fraccion = tarifa_hora / 2
        valor = horas * tarifa_hora + fraccion * tarifa_fraccion
        
        # Solicitar el valor con que paga el cliente
        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Registrar Pago")
        ventana_pago.geometry("400x250")
        ventana_pago.transient(self)
        ventana_pago.grab_set()
        
        # Información del cobro
        frame_info = ttk.LabelFrame(ventana_pago, text="Información del Cobro")
        frame_info.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(frame_info, text=f"Placa: {placa}", font=('Helvetica', 10, 'bold')).pack(pady=2)
        ttk.Label(frame_info, text=f"Tiempo: {horas}h {minutos_restantes}min").pack(pady=2)
        ttk.Label(frame_info, text=f"Valor a pagar: ${valor:,.0f}", font=('Helvetica', 12, 'bold')).pack(pady=5)
        
        # Campo para ingresar el pago
        frame_pago = ttk.Frame(ventana_pago)
        frame_pago.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(frame_pago, text="Pago recibido:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        pago_var = tk.DoubleVar(value=valor)
        pago_entry = ttk.Entry(frame_pago, textvariable=pago_var, width=20)
        pago_entry.grid(row=0, column=1, padx=5, pady=5)
        pago_entry.select_range(0, tk.END)
        pago_entry.focus()
        
        # Etiqueta para mostrar el cambio
        cambio_label = ttk.Label(frame_pago, text="Cambio: $0", font=('Helvetica', 11, 'bold'), foreground='green')
        cambio_label.grid(row=1, column=0, columnspan=2, pady=10)
        
        def actualizar_cambio(*args):
            try:
                pago = pago_var.get()
                cambio = pago - valor
                if cambio < 0:
                    cambio_label.config(text=f"Falta: ${abs(cambio):,.0f}", foreground='red')
                else:
                    cambio_label.config(text=f"Cambio: ${cambio:,.0f}", foreground='green')
            except:
                cambio_label.config(text="Cambio: $0", foreground='black')
        
        pago_var.trace('w', actualizar_cambio)
        actualizar_cambio()
        
        resultado_pago = {'confirmado': False}
        
        def confirmar_pago():
            try:
                pago = pago_var.get()
                if pago < valor:
                    messagebox.showerror("Error", f"El pago recibido (${pago:,.0f}) es menor al valor a pagar (${valor:,.0f})")
                    return
                resultado_pago['pago'] = pago
                resultado_pago['cambio'] = pago - valor
                resultado_pago['confirmado'] = True
                ventana_pago.destroy()
            except:
                messagebox.showerror("Error", "Ingrese un valor válido")
        
        def cancelar():
            ventana_pago.destroy()
        
        frame_botones = ttk.Frame(ventana_pago)
        frame_botones.pack(pady=10)
        ttk.Button(frame_botones, text="Confirmar", command=confirmar_pago).pack(side='left', padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=cancelar).pack(side='left', padx=5)
        
        pago_entry.bind('<Return>', lambda e: confirmar_pago())
        
        self.wait_window(ventana_pago)
        
        if not resultado_pago['confirmado']:
            return
        
        pago_recibido = resultado_pago['pago']
        cambio = resultado_pago['cambio']
        
        try:
            db.registrar_salida(placa, hora_salida_dt.strftime('%Y-%m-%d %H:%M:%S'), valor, pago_recibido, cambio)
            
            # Crear formato de tiempo para el ticket
            tiempo_total = f"{horas}h {minutos_restantes}min"
            
            # Mostrar mensaje de confirmación inmediato
            detalle = f"✓ Salida registrada en la base de datos\n\nPlaca: {placa}\nHora entrada: {hora_entrada_dt.strftime('%H:%M:%S')}\nHora salida: {hora_salida_dt.strftime('%H:%M:%S')}\nTiempo: {tiempo_total}\nValor a pagar: ${valor:,.0f}\nPago recibido: ${pago_recibido:,.0f}\nCambio: ${cambio:,.0f}"
            messagebox.showinfo("✓ Guardado", detalle)
            
            # Generar ticket de salida con toda la información
            ruta_ticket = generar_ticket_pdf(placa, tipo, hora_entrada_str, 
                                             hora_salida_dt.strftime('%Y-%m-%d %H:%M:%S'), 
                                             valor, tiempo_total=tiempo_total, 
                                             pago_recibido=pago_recibido, cambio=cambio,
                                             numero_ticket=numero_ticket)
            
            # Previsualizar ticket en ventana emergente
            self.previsualizar_ticket(ruta_ticket)
            
            # Limpiar campos
            self.placa_entry.delete(0, tk.END)
            self.tipo_cb.set("")
            # Actualizar tabla de tickets
            self.actualizar_tabla_tickets()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar salida:\n{str(e)}")

    def imprimir_ticket(self, ruta_ticket):
        # Abrir el PDF con el visor predeterminado del sistema para impresión manual
        import platform
        import subprocess
        if platform.system() == "Windows":
            os.startfile(ruta_ticket, "print")
        elif platform.system() == "Darwin":
            subprocess.run(["open", ruta_ticket])
        else:
            subprocess.run(["xdg-open", ruta_ticket])

    def generar_reporte(self):
        # Aquí se llamaría a la lógica de generación de reportes
        messagebox.showinfo("Reporte", "Reporte diario generado (ejemplo)")

if __name__ == "__main__":
    app = ParqueaderoApp()
    app.mainloop()
