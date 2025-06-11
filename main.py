import tkinter as tk
from tkinter import ttk, messagebox
from models.models import Cliente, Tecnico, OrdenDeTrabajo
from models.service_factory import ServiceFactory
from models.observer import Observer, OrdenSubject
from models.db_connection import DatabaseConnection
from datetime import datetime
import re
from PIL import Image, ImageTk

# Paleta de colores
COLOR_PRIMARY_BG = "#1C1C1C"  # Fondo principal muy oscuro
COLOR_SECONDARY_BG = "#2C2C2C" # Fondo de tarjetas/frames
COLOR_HEADER_BLUE = "#2196F3" # Azul vibrante para header y acentos
COLOR_ACCENT_BLUE = "#1976D2" # Azul un poco más oscuro para botones/hover
COLOR_TEXT_LIGHT = "#FFFFFF" # Texto principal blanco
COLOR_TEXT_DARK = "#CCCCCC"  # Texto secundario/placeholder gris claro
COLOR_ENTRY_BG = "#3C3C3C"    # Fondo de campos de entrada
COLOR_ENTRY_FG = "#FFFFFF"   # Texto de campos de entrada
COLOR_BORDER = "#2196F3"     # Borde de campos de entrada, igual que accent
FONT_MAIN = ("Segoe UI", 11)
FONT_HEADER = ("Segoe UI", 14, "bold")

# Paleta de colores para TEMA CLARO
COLOR_LIGHT_PRIMARY_BG = "#F0F0F0" # Fondo principal claro
COLOR_LIGHT_SECONDARY_BG = "#FFFFFF" # Fondo de tarjetas/frames claro
COLOR_LIGHT_HEADER_BLUE = "#2196F3" # Azul vibrante (se mantiene)
COLOR_LIGHT_ACCENT_BLUE = "#1976D2" # Azul acento (se mantiene)
COLOR_LIGHT_TEXT_DARK = "#333333"  # Texto principal oscuro
COLOR_LIGHT_TEXT_LIGHT = "#666666" # Texto secundario gris oscuro
COLOR_LIGHT_ENTRY_BG = "#E0E0E0"   # Fondo de campos de entrada claro
COLOR_LIGHT_ENTRY_FG = "#333333"   # Texto de campos de entrada oscuro
COLOR_LIGHT_BORDER = "#BBBBBB"    # Borde de campos de entrada claro

class NotificacionObserver(Observer):
    """
    Observador que maneja las notificaciones de nuevas órdenes de trabajo.
    
    Esta clase implementa el patrón Observer para recibir notificaciones
    cuando se crean nuevas órdenes de trabajo y mostrar mensajes al usuario.
    """
    def update(self, orden: OrdenDeTrabajo):
        """
        Actualiza el estado cuando se recibe una notificación de nueva orden.
        
        Args:
            orden (OrdenDeTrabajo): La orden de trabajo que ha cambiado
        """
        messagebox.showinfo("Nueva Orden", f"Se ha creado una nueva orden para {orden.cliente.nombre}")

class TecnicoObserver(Observer):
    """
    Observador que maneja las notificaciones para los técnicos.
    
    Esta clase implementa el patrón Observer para notificar a los técnicos
    cuando se les asigna una nueva orden de trabajo.
    """
    def update(self, orden: OrdenDeTrabajo):
        """
        Actualiza el estado cuando se recibe una notificación de nueva orden.
        
        Args:
            orden (OrdenDeTrabajo): La orden de trabajo que ha cambiado
        """
        if orden.tecnico:
            messagebox.showinfo("Asignación de Orden", 
                              f"Se ha asignado una nueva orden al técnico {orden.tecnico.nombre}")

class TechnicalServiceApp:
    """
    Aplicación principal para la gestión de servicios técnicos.
    
    Esta clase implementa la interfaz gráfica de usuario y maneja todas
    las interacciones del usuario con el sistema.
    
    Atributos:
        root (tk.Tk): Ventana principal de la aplicación
        orden_subject (OrdenSubject): Sujeto para el patrón Observer
        db (DatabaseConnection): Conexión a la base de datos
    """
    def __init__(self):
        """
        Inicializa la aplicación y configura la interfaz gráfica.
        """
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Servicios Técnicos")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        
        # Estado del tema: True = oscuro, False = claro
        self.is_dark_theme = True
        
        try:
            icon_image = Image.open("image.ico")
            photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(True, photo)
        except Exception as e:
            print(f"Error al cargar el icono: {e}")

        # Crear el header una sola vez
        self.header_frame = tk.Frame(self.root, height=75)
        self.header_frame.pack(fill='x', side='top')
        
        # Ahora usamos un Canvas para el título para tener control total sobre el fondo
        self.header_canvas = tk.Canvas(self.header_frame, bg=COLOR_HEADER_BLUE, highlightthickness=0)
        self.header_canvas.pack(fill='both', expand=True)

        # Crear el texto del título en el Canvas
        self.header_text_id = self.header_canvas.create_text(
            0, 0, # Posición inicial, se actualizará en _on_header_resize
            text="Sistema de Gestión de Servicios Técnicos", 
            font=FONT_HEADER, 
            fill=COLOR_TEXT_LIGHT, # Color inicial del texto
            anchor='center' # Asegurar que el ancla del texto sea el centro
        )
        
        # Bind al evento Configure del frame para centrar el texto al redimensionar
        self.header_frame.bind("<Configure>", self._on_header_resize)
        
        self._crear_theme_toggle_button()
        self.orden_subject = OrdenSubject()
        self.orden_subject.attach(NotificacionObserver())
        self.orden_subject.attach(TecnicoObserver())
        self.db = DatabaseConnection()
        self.notebook = ttk.Notebook(self.root, style="TNotebook")
        self.notebook.pack(expand=True, fill='both', padx=20, pady=(0, 20))
        
        self.clientes_frame = tk.Frame(self.notebook, bg=COLOR_PRIMARY_BG)
        self.tecnicos_frame = tk.Frame(self.notebook, bg=COLOR_PRIMARY_BG)
        self.ordenes_frame = tk.Frame(self.notebook, bg=COLOR_PRIMARY_BG)
        
        self.notebook.add(self.clientes_frame, text='Clientes')
        self.notebook.add(self.tecnicos_frame, text='Técnicos')
        self.notebook.add(self.ordenes_frame, text='Órdenes de Trabajo')
        
        self._init_clientes_tab()
        self._init_tecnicos_tab()
        self._init_ordenes_tab()
        
        self._apply_theme() # Aplicar el tema inicial
        self._on_header_resize() # Centrar el texto del Canvas al inicio de la aplicación

    def _get_current_colors(self):
        if self.is_dark_theme:
            return {
                "PRIMARY_BG": COLOR_PRIMARY_BG,
                "SECONDARY_BG": COLOR_SECONDARY_BG,
                "HEADER_BLUE": COLOR_HEADER_BLUE,
                "ACCENT_BLUE": COLOR_ACCENT_BLUE,
                "TEXT_LIGHT": COLOR_TEXT_LIGHT,
                "TEXT_DARK": COLOR_TEXT_DARK,
                "ENTRY_BG": COLOR_ENTRY_BG,
                "ENTRY_FG": COLOR_ENTRY_FG,
                "BORDER": COLOR_BORDER
            }
        else:
            return {
                "PRIMARY_BG": COLOR_LIGHT_PRIMARY_BG,
                "SECONDARY_BG": COLOR_LIGHT_SECONDARY_BG,
                "HEADER_BLUE": COLOR_LIGHT_HEADER_BLUE,
                "ACCENT_BLUE": COLOR_LIGHT_ACCENT_BLUE,
                "TEXT_LIGHT": COLOR_LIGHT_TEXT_DARK, # En tema claro, el texto claro es el oscuro
                "TEXT_DARK": COLOR_LIGHT_TEXT_LIGHT, # Y el texto oscuro es el claro
                "ENTRY_BG": COLOR_LIGHT_ENTRY_BG,
                "ENTRY_FG": COLOR_LIGHT_ENTRY_FG,
                "BORDER": COLOR_LIGHT_BORDER
            }

    def _apply_theme(self):
        colors = self._get_current_colors()
        
        # Configurar estilos de ttk
        style = ttk.Style()
        style.theme_use('clam')
        
        self.root.configure(bg=colors["PRIMARY_BG"])
        
        # Actualizar el header
        self.header_frame.configure(bg=colors["HEADER_BLUE"])
        # Actualizar el Canvas del título y el texto en él
        self.header_canvas.configure(bg=colors["HEADER_BLUE"])
        self.header_canvas.itemconfig(self.header_text_id, fill=colors["TEXT_LIGHT"])
        
        # Definir y aplicar estilo para el header_label
        # style.configure("Header.TLabel", background=colors["HEADER_BLUE"], foreground=colors["TEXT_LIGHT"], padding=0)

        style.configure("TFrame", background=colors["PRIMARY_BG"])
        style.configure("Card.TFrame", background=colors["SECONDARY_BG"], relief="flat")
        style.configure("TNotebook", background=colors["PRIMARY_BG"], borderwidth=0)
        style.configure("TNotebook.Tab", font=FONT_MAIN, padding=[20, 10], background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"], borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", colors["HEADER_BLUE"]), ("active", colors["ACCENT_BLUE"])],
                  foreground=[("selected", colors["TEXT_LIGHT"]), ("active", colors["TEXT_LIGHT"])])
        
        style.configure("TLabel", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"], font=FONT_MAIN)
        style.configure("TLabelFrame.Label", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"], font=FONT_MAIN)
        
        style.configure("TButton", background=colors["ACCENT_BLUE"], foreground=colors["TEXT_LIGHT"], font=FONT_MAIN, borderwidth=0, focusthickness=3, focuscolor=colors["ACCENT_BLUE"])
        style.map("TButton",
                  background=[("active", colors["HEADER_BLUE"]), ("pressed", colors["ACCENT_BLUE"])])
        
        style.configure("Treeview", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"], fieldbackground=colors["SECONDARY_BG"], font=FONT_MAIN, rowheight=28, borderwidth=0)
        style.configure("Treeview.Heading", background=colors["ACCENT_BLUE"], foreground=colors["TEXT_LIGHT"], font=("Segoe UI", 12, "bold"), borderwidth=0)
        style.map("Treeview.Heading", background=[("active", colors["HEADER_BLUE"])])
        
        style.configure("TEntry", fieldbackground=colors["ENTRY_BG"], foreground=colors["ENTRY_FG"], borderwidth=0, relief="flat", insertbackground=colors["ENTRY_FG"])
        style.configure("TCombobox", fieldbackground=colors["ENTRY_BG"], foreground=colors["ENTRY_FG"], selectbackground=colors["ACCENT_BLUE"], selectforeground=colors["TEXT_LIGHT"], background=colors["ENTRY_BG"], borderwidth=0, relief="flat", insertbackground=colors["ENTRY_FG"])
        style.map("TCombobox", fieldbackground=[('readonly', colors["ENTRY_BG"])])
        style.configure("TText", background=colors["ENTRY_BG"], foreground=colors["ENTRY_FG"], borderwidth=0, relief="flat", insertbackground=colors["ENTRY_FG"])
        
        # Actualizar colores de widgets tk (directos)
        self._update_tk_widgets_colors(self.root, colors)

    def _update_tk_widgets_colors(self, parent, colors):
        for widget in parent.winfo_children():
            if isinstance(widget, (tk.Frame, tk.LabelFrame, tk.Label, tk.Button, tk.Entry, tk.Text)):
                try:
                    widget.configure(bg=colors["SECONDARY_BG"], fg=colors["TEXT_LIGHT"]) # Default para la mayoría
                    if isinstance(widget, (tk.Button)):
                        widget.configure(bg=colors["ACCENT_BLUE"], fg=colors["TEXT_LIGHT"], activebackground=colors["HEADER_BLUE"], activeforeground=colors["TEXT_LIGHT"])
                    elif isinstance(widget, (tk.Entry, tk.Text)):
                        widget.configure(bg=colors["ENTRY_BG"], fg=colors["ENTRY_FG"], insertbackground=colors["ENTRY_FG"], highlightbackground=colors["BORDER"], highlightcolor=colors["BORDER"])
                    
                    # Specific cases for labels within frames/labelframes
                    if isinstance(widget, tk.Label) and widget.master in [self.clientes_frame, self.tecnicos_frame, self.ordenes_frame]:
                        widget.configure(bg=colors["SECONDARY_BG"], fg=colors["TEXT_LIGHT"])

                except tk.TclError: # Algunos widgets tk pueden no tener todas las propiedades
                    pass
            
            # Recorrer widgets anidados
            if hasattr(widget, "winfo_children") and widget.winfo_children():
                self._update_tk_widgets_colors(widget, colors)

    def _on_header_resize(self, event=None):
        # Centrar el texto en el Canvas cuando el frame del header se redimensiona
        canvas_width = self.header_canvas.winfo_width()
        canvas_height = self.header_canvas.winfo_height()
        self.header_canvas.coords(self.header_text_id, canvas_width / 2, canvas_height / 2)

    def _crear_theme_toggle_button(self):
        self.theme_button = tk.Button(self.root, text="Alternar Tema", command=self._toggle_theme)
        self._estilizar_boton(self.theme_button)
        self.theme_button.place(relx=0.95, rely=0.02, anchor='ne')

    def _toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self._apply_theme()

    def _estilizar_boton(self, boton):
        colors = self._get_current_colors()
        boton.configure(bg=colors["ACCENT_BLUE"], fg=colors["TEXT_LIGHT"], 
                        activebackground=colors["HEADER_BLUE"], activeforeground=colors["TEXT_LIGHT"], 
                        relief="flat", bd=0, font=FONT_MAIN, cursor="hand2")
        boton.bind("<Enter>", lambda e: boton.config(bg=colors["HEADER_BLUE"])) # Hover al color de header
        boton.bind("<Leave>", lambda e: boton.config(bg=colors["ACCENT_BLUE"])) # Volver al color del botón

    def _estilizar_entry(self, entry):
        colors = self._get_current_colors()
        entry.configure(bg=colors["ENTRY_BG"], fg=colors["ENTRY_FG"], insertbackground=colors["ENTRY_FG"], 
                        relief="flat", font=FONT_MAIN, highlightthickness=1, 
                        highlightbackground=colors["BORDER"], highlightcolor=colors["BORDER"])

    def _init_clientes_tab(self):
        colors = self._get_current_colors()
        
        # Configurar el grid de clientes_frame para que se expanda
        self.clientes_frame.grid_rowconfigure(0, weight=0) # Fila del formulario (no se expande verticalmente)
        self.clientes_frame.grid_rowconfigure(1, weight=1) # Fila de la tabla (se expande verticalmente)
        self.clientes_frame.grid_rowconfigure(2, weight=0) # Fila del botón cargar (no se expande verticalmente)
        self.clientes_frame.grid_columnconfigure(0, weight=1) # Columna única (se expande horizontalmente)

        form_frame = tk.LabelFrame(self.clientes_frame, text="Registro de Cliente", bg=colors["SECONDARY_BG"], fg=colors["TEXT_LIGHT"], font=FONT_MAIN)
        form_frame.grid(row=0, column=0, padx=20, pady=20, sticky='ew') # Usar grid para el formulario
        
        # Configurar la columna 1 del form_frame para que se expanda horizontalmente
        form_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Nombre:", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"]).grid(row=0, column=0, padx=5, pady=8, sticky='e')
        self.nombre_cliente = tk.Entry(form_frame)
        self.nombre_cliente.grid(row=0, column=1, padx=5, pady=8, sticky='ew')
        self._estilizar_entry(self.nombre_cliente)

        ttk.Label(form_frame, text="Email:", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"]).grid(row=1, column=0, padx=5, pady=8, sticky='e')
        self.email_cliente = tk.Entry(form_frame)
        self.email_cliente.grid(row=1, column=1, padx=5, pady=8, sticky='ew')
        self._estilizar_entry(self.email_cliente)

        ttk.Label(form_frame, text="Teléfono:", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"]).grid(row=2, column=0, padx=5, pady=8, sticky='e')
        self.telefono_cliente = tk.Entry(form_frame)
        self.telefono_cliente.grid(row=2, column=1, padx=5, pady=8, sticky='ew')
        self._estilizar_entry(self.telefono_cliente)

        ttk.Label(form_frame, text="Dirección:", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"]).grid(row=3, column=0, padx=5, pady=8, sticky='e')
        self.direccion_cliente = tk.Entry(form_frame)
        self.direccion_cliente.grid(row=3, column=1, padx=5, pady=8, sticky='ew')
        self._estilizar_entry(self.direccion_cliente)

        btn_registrar = tk.Button(form_frame, text="Registrar Cliente", command=self.registrar_cliente)
        btn_registrar.grid(row=4, column=0, columnspan=2, pady=15)
        self._estilizar_boton(btn_registrar)

        self.tabla_clientes = ttk.Treeview(self.clientes_frame, columns=("ID", "Nombre", "Email", "Teléfono", "Dirección"), show='headings', style="Treeview")
        for col in ("ID", "Nombre", "Email", "Teléfono", "Dirección"):
            self.tabla_clientes.heading(col, text=col)
            self.tabla_clientes.column(col, anchor='center', width=120)
        self.tabla_clientes.grid(row=1, column=0, sticky='nsew', padx=20, pady=10) # Eliminado fill/expand, añadido sticky='nsew'

        btn_cargar = tk.Button(self.clientes_frame, text="Cargar Clientes", command=self.cargar_clientes)
        btn_cargar.grid(row=2, column=0, pady=10) # Usar grid para el botón
        self._estilizar_boton(btn_cargar)

    def _init_tecnicos_tab(self):
        colors = self._get_current_colors()

        # Configurar el grid de tecnicos_frame para que se expanda
        self.tecnicos_frame.grid_rowconfigure(0, weight=0) # Fila del formulario
        self.tecnicos_frame.grid_rowconfigure(1, weight=1) # Fila de la tabla
        self.tecnicos_frame.grid_rowconfigure(2, weight=0) # Fila del botón cargar
        self.tecnicos_frame.grid_columnconfigure(0, weight=1) # Columna única

        form_frame = tk.LabelFrame(self.tecnicos_frame, text="Registro de Técnico", bg=colors["SECONDARY_BG"], fg=colors["TEXT_LIGHT"], font=FONT_MAIN) # Usar tk.LabelFrame
        form_frame.grid(row=0, column=0, padx=20, pady=20, sticky='ew') # Usar grid para el formulario

        # Configurar la columna 1 del form_frame para que se expanda
        form_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Nombre:", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"]).grid(row=0, column=0, padx=5, pady=8, sticky='e')
        self.nombre_tecnico = tk.Entry(form_frame)
        self.nombre_tecnico.grid(row=0, column=1, padx=5, pady=8, sticky='ew')
        self._estilizar_entry(self.nombre_tecnico)

        ttk.Label(form_frame, text="Especialidad:", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"]).grid(row=1, column=0, padx=5, pady=8, sticky='e')
        self.especialidad_tecnico = ttk.Combobox(form_frame, values=["Reparación", "Soporte IT"], style="TCombobox") # Apply style to Combobox
        self.especialidad_tecnico.grid(row=1, column=1, padx=5, pady=8, sticky='ew')

        ttk.Label(form_frame, text="Email:", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"]).grid(row=2, column=0, padx=5, pady=8, sticky='e')
        self.email_tecnico = tk.Entry(form_frame)
        self.email_tecnico.grid(row=2, column=1, padx=5, pady=8, sticky='ew')
        self._estilizar_entry(self.email_tecnico)

        ttk.Label(form_frame, text="Teléfono:", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"]).grid(row=3, column=0, padx=5, pady=8, sticky='e')
        self.telefono_tecnico = tk.Entry(form_frame)
        self.telefono_tecnico.grid(row=3, column=1, padx=5, pady=8, sticky='ew')
        self._estilizar_entry(self.telefono_tecnico)

        btn_registrar = tk.Button(form_frame, text="Registrar Técnico", command=self.registrar_tecnico)
        btn_registrar.grid(row=4, column=0, columnspan=2, pady=15)
        self._estilizar_boton(btn_registrar)

        self.tabla_tecnicos = ttk.Treeview(self.tecnicos_frame, columns=("ID", "Nombre", "Especialidad", "Email", "Teléfono"), show='headings', style="Treeview")
        for col in ("ID", "Nombre", "Especialidad", "Email", "Teléfono"):
            self.tabla_tecnicos.heading(col, text=col)
            self.tabla_tecnicos.column(col, anchor='center', width=120)
        self.tabla_tecnicos.grid(row=1, column=0, sticky='nsew', padx=20, pady=10) # Eliminado fill/expand, añadido sticky='nsew'

        btn_cargar = tk.Button(self.tecnicos_frame, text="Cargar Técnicos", command=self.cargar_tecnicos)
        btn_cargar.grid(row=2, column=0, pady=10) # Usar grid para el botón
        self._estilizar_boton(btn_cargar)

    def _init_ordenes_tab(self):
        colors = self._get_current_colors()

        # Configurar el grid de ordenes_frame para que se expanda
        self.ordenes_frame.grid_rowconfigure(0, weight=0) # Fila del formulario
        self.ordenes_frame.grid_rowconfigure(1, weight=1) # Fila de la tabla
        self.ordenes_frame.grid_rowconfigure(2, weight=0) # Fila del botón cargar
        self.ordenes_frame.grid_columnconfigure(0, weight=1) # Columna única

        form_frame = tk.LabelFrame(self.ordenes_frame, text="Nueva Orden de Trabajo", bg=colors["SECONDARY_BG"], fg=colors["TEXT_LIGHT"], font=FONT_MAIN) # Usar tk.LabelFrame
        form_frame.grid(row=0, column=0, padx=20, pady=20, sticky='ew') # Usar grid para el formulario

        # Configurar la columna 1 del form_frame para que se expanda
        form_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Cliente:", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"]).grid(row=0, column=0, padx=5, pady=8, sticky='e')
        self.cliente_orden = ttk.Combobox(form_frame, style="TCombobox")
        self.cliente_orden.grid(row=0, column=1, padx=5, pady=8, sticky='ew')

        ttk.Label(form_frame, text="Técnico:", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"]).grid(row=1, column=0, padx=5, pady=8, sticky='e')
        self.tecnico_orden = ttk.Combobox(form_frame, style="TCombobox")
        self.tecnico_orden.grid(row=1, column=1, padx=5, pady=8, sticky='ew')

        ttk.Label(form_frame, text="Tipo de Servicio:", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"]).grid(row=2, column=0, padx=5, pady=8, sticky='e')
        self.tipo_servicio = ttk.Combobox(form_frame, values=["Reparación", "Soporte IT"], style="TCombobox")
        self.tipo_servicio.grid(row=2, column=1, padx=5, pady=8, sticky='ew')

        ttk.Label(form_frame, text="Descripción:", background=colors["SECONDARY_BG"], foreground=colors["TEXT_LIGHT"]).grid(row=3, column=0, padx=5, pady=8, sticky='e')
        self.descripcion_orden = tk.Text(form_frame, height=3, width=30)
        self._estilizar_entry(self.descripcion_orden)
        self.descripcion_orden.grid(row=3, column=1, padx=5, pady=8, sticky='ew')

        btn_crear = tk.Button(form_frame, text="Crear Orden", command=self.crear_orden)
        btn_crear.grid(row=4, column=0, columnspan=2, pady=15)
        self._estilizar_boton(btn_crear)

        self.tabla_ordenes = ttk.Treeview(self.ordenes_frame, columns=("ID", "Cliente", "Técnico", "Servicio", "Estado", "Fecha"), show='headings', style="Treeview")
        for col in ("ID", "Cliente", "Técnico", "Servicio", "Estado", "Fecha"):
            self.tabla_ordenes.heading(col, text=col)
            self.tabla_ordenes.column(col, anchor='center', width=120)
        self.tabla_ordenes.grid(row=1, column=0, sticky='nsew', padx=20, pady=10) # Eliminado fill/expand, añadido sticky='nsew'

        btn_cargar = tk.Button(self.ordenes_frame, text="Cargar Órdenes", command=self.cargar_ordenes)
        btn_cargar.grid(row=2, column=0, pady=10)
        self._estilizar_boton(btn_cargar)

    def validar_email(self, email: str) -> bool:
        """
        Valida el formato de un correo electrónico.
        
        Args:
            email (str): Correo electrónico a validar
            
        Returns:
            bool: True si el email es válido, False en caso contrario
        """
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, email))

    def registrar_cliente(self):
        """
        Registra un nuevo cliente en el sistema.
        
        Valida los datos ingresados y guarda la información en la base de datos.
        Muestra mensajes de error si los datos no son válidos.
        """
        nombre = self.nombre_cliente.get()
        email = self.email_cliente.get()
        telefono = self.telefono_cliente.get()
        direccion = self.direccion_cliente.get()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        
        if email and not self.validar_email(email):
            messagebox.showerror("Error", "El formato del email no es válido")
            return
        
        try:
            cliente = Cliente(nombre, email, telefono, direccion)
            cliente.guardar()
            messagebox.showinfo("Éxito", "Cliente registrado correctamente")
            self.limpiar_campos_cliente()
            self.cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar cliente: {str(e)}")

    def registrar_tecnico(self):
        """
        Registra un nuevo técnico en el sistema.
        
        Valida los datos ingresados y guarda la información en la base de datos.
        Muestra mensajes de error si los datos no son válidos.
        """
        nombre = self.nombre_tecnico.get()
        especialidad = self.especialidad_tecnico.get()
        email = self.email_tecnico.get()
        telefono = self.telefono_tecnico.get()
        
        if not nombre or not especialidad:
            messagebox.showerror("Error", "Nombre y especialidad son obligatorios")
            return
        
        if email and not self.validar_email(email):
            messagebox.showerror("Error", "El formato del email no es válido")
            return
        
        try:
            tecnico = Tecnico(nombre, especialidad, email, telefono)
            tecnico.guardar()
            messagebox.showinfo("Éxito", "Técnico registrado correctamente")
            self.limpiar_campos_tecnico()
            self.cargar_tecnicos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar técnico: {str(e)}")

    def crear_orden(self):
        """
        Crea una nueva orden de trabajo en el sistema.
        
        Valida los datos ingresados, crea la orden y la guarda en la base de datos.
        Notifica a los observadores sobre la nueva orden.
        """
        cliente_nombre = self.cliente_orden.get()
        tecnico_nombre = self.tecnico_orden.get()
        tipo_servicio = self.tipo_servicio.get()
        descripcion = self.descripcion_orden.get("1.0", tk.END).strip()
        
        if not all([cliente_nombre, tecnico_nombre, tipo_servicio, descripcion]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        try:
            # Obtener cliente y técnico
            cliente = self.obtener_cliente_por_nombre(cliente_nombre)
            tecnico = self.obtener_tecnico_por_nombre(tecnico_nombre)
            
            if not cliente or not tecnico:
                messagebox.showerror("Error", "Cliente o técnico no encontrado")
                return
            
            # Crear servicio usando el factory
            if tipo_servicio.lower() == "reparación" or tipo_servicio.lower() == "reparacion":
                servicio = ServiceFactory.create_service(
                    "reparacion",
                    descripcion=descripcion,
                    costo=100.0,  # Puedes ajustar el costo según tu lógica
                    duracion_estimada=60,  # Puedes ajustar la duración
                    tipo_reparacion="General"
                )
            else:
                servicio = ServiceFactory.create_service(
                    "soporte_it",
                    descripcion=descripcion,
                    costo=80.0,  # Puedes ajustar el costo según tu lógica
                    duracion_estimada=45,  # Puedes ajustar la duración
                    nivel_soporte="Nivel 1"
                )
            
            # Crear orden
            orden = OrdenDeTrabajo(cliente, tecnico, servicio, descripcion)
            orden.guardar()
            
            # Notificar a los observadores
            self.orden_subject.nueva_orden(orden)
            
            messagebox.showinfo("Éxito", "Orden de trabajo creada correctamente")
            self.limpiar_campos_orden()
            self.cargar_ordenes()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear orden: {str(e)}")

    def obtener_cliente_por_nombre(self, nombre: str) -> Cliente:
        """
        Busca un cliente por su nombre en la base de datos.
        
        Args:
            nombre (str): Nombre del cliente a buscar
            
        Returns:
            Cliente: Objeto Cliente si se encuentra, None en caso contrario
        """
        query = "SELECT * FROM clientes WHERE nombre = ?"
        resultado = self.db.execute_query(query, (nombre,))
        if resultado:
            fila = resultado[0]
            return Cliente(
                nombre=fila[1],
                email=fila[2],
                telefono=fila[3],
                direccion=fila[4],
                id=fila[0]
            )
        return None

    def obtener_tecnico_por_nombre(self, nombre: str) -> Tecnico:
        """
        Busca un técnico por su nombre en la base de datos.
        
        Args:
            nombre (str): Nombre del técnico a buscar
            
        Returns:
            Tecnico: Objeto Tecnico si se encuentra, None en caso contrario
        """
        query = "SELECT * FROM tecnicos WHERE nombre = ?"
        resultado = self.db.execute_query(query, (nombre,))
        if resultado:
            fila = resultado[0]
            return Tecnico(
                nombre=fila[1],
                especialidad=fila[2],
                email=fila[3],
                telefono=fila[4],
                id=fila[0]
            )
        return None

    def cargar_clientes(self):
        """
        Carga la lista de clientes desde la base de datos y la muestra en la tabla.
        """
        for item in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(item)
            
        query = "SELECT * FROM clientes"
        clientes = self.db.execute_query(query)
        
        for cliente in clientes:
            self.tabla_clientes.insert("", "end", values=cliente)
            
        # Actualizar combobox de clientes en órdenes
        self.cliente_orden['values'] = [cliente[1] for cliente in clientes]

    def cargar_tecnicos(self):
        """
        Carga la lista de técnicos desde la base de datos y la muestra en la tabla.
        """
        for item in self.tabla_tecnicos.get_children():
            self.tabla_tecnicos.delete(item)
            
        query = "SELECT * FROM tecnicos"
        tecnicos = self.db.execute_query(query)
        
        for tecnico in tecnicos:
            self.tabla_tecnicos.insert("", "end", values=tecnico)
            
        # Actualizar combobox de técnicos en órdenes
        self.tecnico_orden['values'] = [tecnico[1] for tecnico in tecnicos]

    def cargar_ordenes(self):
        """
        Carga la lista de órdenes de trabajo desde la base de datos y la muestra en la tabla.
        """
        for item in self.tabla_ordenes.get_children():
            self.tabla_ordenes.delete(item)
            
        query = """
            SELECT o.id, c.nombre, t.nombre, s.tipo, o.estado, o.fecha_creacion
            FROM ordenes_trabajo o
            JOIN clientes c ON o.cliente_id = c.id
            JOIN tecnicos t ON o.tecnico_id = t.id
            JOIN servicios s ON o.servicio_id = s.id
        """
        ordenes = self.db.execute_query(query)
        
        for orden in ordenes:
            self.tabla_ordenes.insert("", "end", values=orden)

    def limpiar_campos_cliente(self):
        """
        Limpia los campos del formulario de registro de clientes.
        """
        self.nombre_cliente.delete(0, tk.END)
        self.email_cliente.delete(0, tk.END)
        self.telefono_cliente.delete(0, tk.END)
        self.direccion_cliente.delete(0, tk.END)

    def limpiar_campos_tecnico(self):
        """
        Limpia los campos del formulario de registro de técnicos.
        """
        self.nombre_tecnico.delete(0, tk.END)
        self.especialidad_tecnico.set('')
        self.email_tecnico.delete(0, tk.END)
        self.telefono_tecnico.delete(0, tk.END)

    def limpiar_campos_orden(self):
        """
        Limpia los campos del formulario de creación de órdenes.
        """
        self.cliente_orden.set('')
        self.tecnico_orden.set('')
        self.tipo_servicio.set('')
        self.descripcion_orden.delete("1.0", tk.END)

    def run(self):
        """
        Inicia la aplicación y carga los datos iniciales.
        """
        self.cargar_clientes()
        self.cargar_tecnicos()
        self.cargar_ordenes()
        self.root.mainloop()

if __name__ == "__main__":
    app = TechnicalServiceApp()
    app.run() 