import tkinter as tk
from tkinter import ttk, messagebox
from models.models import Cliente, Tecnico, OrdenDeTrabajo
from models.service_factory import ServiceFactory
from models.observer import Observer, OrdenSubject
from models.db_connection import DatabaseConnection
from datetime import datetime
import re

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
        self.root.geometry("800x600")
        
        # Configurar el patrón Observer
        self.orden_subject = OrdenSubject()
        self.orden_subject.attach(NotificacionObserver())
        self.orden_subject.attach(TecnicoObserver())
        
        # Inicializar la base de datos
        self.db = DatabaseConnection()
        
        # Crear pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Crear frames para cada pestaña
        self.clientes_frame = ttk.Frame(self.notebook)
        self.tecnicos_frame = ttk.Frame(self.notebook)
        self.ordenes_frame = ttk.Frame(self.notebook)
        
        # Agregar frames al notebook
        self.notebook.add(self.clientes_frame, text='Clientes')
        self.notebook.add(self.tecnicos_frame, text='Técnicos')
        self.notebook.add(self.ordenes_frame, text='Órdenes de Trabajo')
        
        # Inicializar componentes
        self._init_clientes_tab()
        self._init_tecnicos_tab()
        self._init_ordenes_tab()

    def _init_clientes_tab(self):
        """
        Inicializa la pestaña de gestión de clientes.
        
        Configura los campos de entrada, botones y la tabla de clientes
        para la gestión de información de clientes.
        """
        # Frame para el formulario
        form_frame = ttk.LabelFrame(self.clientes_frame, text="Registro de Cliente")
        form_frame.pack(fill='x', padx=5, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_cliente = ttk.Entry(form_frame)
        self.nombre_cliente.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_cliente = ttk.Entry(form_frame)
        self.email_cliente.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
        self.telefono_cliente = ttk.Entry(form_frame)
        self.telefono_cliente.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Dirección:").grid(row=3, column=0, padx=5, pady=5)
        self.direccion_cliente = ttk.Entry(form_frame)
        self.direccion_cliente.grid(row=3, column=1, padx=5, pady=5)
        
        # Botones
        ttk.Button(form_frame, text="Registrar Cliente", 
                  command=self.registrar_cliente).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Tabla de clientes
        self.tabla_clientes = ttk.Treeview(self.clientes_frame, 
                                         columns=("ID", "Nombre", "Email", "Teléfono", "Dirección"),
                                         show='headings')
        
        self.tabla_clientes.heading("ID", text="ID")
        self.tabla_clientes.heading("Nombre", text="Nombre")
        self.tabla_clientes.heading("Email", text="Email")
        self.tabla_clientes.heading("Teléfono", text="Teléfono")
        self.tabla_clientes.heading("Dirección", text="Dirección")
        
        self.tabla_clientes.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botón para cargar clientes
        ttk.Button(self.clientes_frame, text="Cargar Clientes", 
                  command=self.cargar_clientes).pack(pady=5)

    def _init_tecnicos_tab(self):
        """
        Inicializa la pestaña de gestión de técnicos.
        
        Configura los campos de entrada, botones y la tabla de técnicos
        para la gestión de información de técnicos.
        """
        # Frame para el formulario
        form_frame = ttk.LabelFrame(self.tecnicos_frame, text="Registro de Técnico")
        form_frame.pack(fill='x', padx=5, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_tecnico = ttk.Entry(form_frame)
        self.nombre_tecnico.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Especialidad:").grid(row=1, column=0, padx=5, pady=5)
        self.especialidad_tecnico = ttk.Combobox(form_frame, 
                                               values=["Reparación", "Soporte IT"])
        self.especialidad_tecnico.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email_tecnico = ttk.Entry(form_frame)
        self.email_tecnico.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, padx=5, pady=5)
        self.telefono_tecnico = ttk.Entry(form_frame)
        self.telefono_tecnico.grid(row=3, column=1, padx=5, pady=5)
        
        # Botones
        ttk.Button(form_frame, text="Registrar Técnico", 
                  command=self.registrar_tecnico).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Tabla de técnicos
        self.tabla_tecnicos = ttk.Treeview(self.tecnicos_frame, 
                                         columns=("ID", "Nombre", "Especialidad", "Email", "Teléfono"),
                                         show='headings')
        
        self.tabla_tecnicos.heading("ID", text="ID")
        self.tabla_tecnicos.heading("Nombre", text="Nombre")
        self.tabla_tecnicos.heading("Especialidad", text="Especialidad")
        self.tabla_tecnicos.heading("Email", text="Email")
        self.tabla_tecnicos.heading("Teléfono", text="Teléfono")
        
        self.tabla_tecnicos.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botón para cargar técnicos
        ttk.Button(self.tecnicos_frame, text="Cargar Técnicos", 
                  command=self.cargar_tecnicos).pack(pady=5)

    def _init_ordenes_tab(self):
        """
        Inicializa la pestaña de gestión de órdenes de trabajo.
        
        Configura los campos de entrada, botones y la tabla de órdenes
        para la gestión de órdenes de trabajo.
        """
        # Frame para el formulario
        form_frame = ttk.LabelFrame(self.ordenes_frame, text="Nueva Orden de Trabajo")
        form_frame.pack(fill='x', padx=5, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
        self.cliente_orden = ttk.Combobox(form_frame)
        self.cliente_orden.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Técnico:").grid(row=1, column=0, padx=5, pady=5)
        self.tecnico_orden = ttk.Combobox(form_frame)
        self.tecnico_orden.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Tipo de Servicio:").grid(row=2, column=0, padx=5, pady=5)
        self.tipo_servicio = ttk.Combobox(form_frame, values=["Reparación", "Soporte IT"])
        self.tipo_servicio.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Descripción:").grid(row=3, column=0, padx=5, pady=5)
        self.descripcion_orden = tk.Text(form_frame, height=3, width=30)
        self.descripcion_orden.grid(row=3, column=1, padx=5, pady=5)
        
        # Botones
        ttk.Button(form_frame, text="Crear Orden", 
                  command=self.crear_orden).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Tabla de órdenes
        self.tabla_ordenes = ttk.Treeview(self.ordenes_frame, 
                                        columns=("ID", "Cliente", "Técnico", "Servicio", "Estado", "Fecha"),
                                        show='headings')
        
        self.tabla_ordenes.heading("ID", text="ID")
        self.tabla_ordenes.heading("Cliente", text="Cliente")
        self.tabla_ordenes.heading("Técnico", text="Técnico")
        self.tabla_ordenes.heading("Servicio", text="Servicio")
        self.tabla_ordenes.heading("Estado", text="Estado")
        self.tabla_ordenes.heading("Fecha", text="Fecha")
        
        self.tabla_ordenes.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botón para cargar órdenes
        ttk.Button(self.ordenes_frame, text="Cargar Órdenes", 
                  command=self.cargar_ordenes).pack(pady=5)

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