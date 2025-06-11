from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from models.db_connection import DatabaseConnection

class Cliente:
    """
    Clase que representa a un cliente en el sistema.
    
    Atributos:
        nombre (str): Nombre completo del cliente
        email (str): Correo electrónico del cliente
        telefono (str): Número de teléfono del cliente
        direccion (str): Dirección del cliente
        id (Optional[int]): Identificador único del cliente
    """
    def __init__(self, nombre: str, email: str = None, telefono: str = None, direccion: str = None, id: int = None):
        """
        Inicializa una nueva instancia de Cliente.
        
        Args:
            nombre (str): Nombre completo del cliente
            email (str, opcional): Correo electrónico del cliente
            telefono (str, opcional): Número de teléfono del cliente
            direccion (str, opcional): Dirección del cliente
            id (Optional[int]): Identificador único del cliente
        """
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.id = id

    def guardar(self):
        """
        Guarda el cliente en la base de datos.
        
        Returns:
            int: ID del cliente guardado
        """
        db = DatabaseConnection()
        query = """
            INSERT INTO clientes (nombre, email, telefono, direccion)
            VALUES (?, ?, ?, ?)
        """
        db.execute_query(query, (self.nombre, self.email, self.telefono, self.direccion))
        self.id = db.execute_query("SELECT last_insert_rowid()")[0][0]
        return self.id

class Tecnico:
    """
    Clase que representa a un técnico en el sistema.
    
    Atributos:
        nombre (str): Nombre completo del técnico
        especialidad (str): Especialidad del técnico
        email (str): Correo electrónico del técnico
        telefono (str): Número de teléfono del técnico
        id (Optional[int]): Identificador único del técnico
    """
    def __init__(self, nombre: str, especialidad: str, email: str = None, telefono: str = None, id: int = None):
        """
        Inicializa una nueva instancia de Tecnico.
        
        Args:
            nombre (str): Nombre completo del técnico
            especialidad (str): Especialidad del técnico
            email (str, opcional): Correo electrónico del técnico
            telefono (str, opcional): Número de teléfono del técnico
            id (Optional[int]): Identificador único del técnico
        """
        self.nombre = nombre
        self.especialidad = especialidad
        self.email = email
        self.telefono = telefono
        self.ordenes = []
        self.id = id

    def agregar_orden(self, orden):
        """
        Agrega una orden de trabajo a la lista de órdenes del técnico.
        
        Args:
            orden (OrdenDeTrabajo): Orden de trabajo a agregar
        """
        self.ordenes.append(orden)

    def guardar(self):
        """
        Guarda el técnico en la base de datos.
        
        Returns:
            int: ID del técnico guardado
        """
        db = DatabaseConnection()
        query = """
            INSERT INTO tecnicos (nombre, especialidad, email, telefono)
            VALUES (?, ?, ?, ?)
        """
        db.execute_query(query, (self.nombre, self.especialidad, self.email, self.telefono))
        self.id = db.execute_query("SELECT last_insert_rowid()")[0][0]
        return self.id

class Servicio(ABC):
    """
    Clase abstracta base para los servicios.
    
    Atributos:
        descripcion (str): Descripción del servicio
        costo_base (float): Costo base del servicio
        duracion_estimada (int): Duración estimada en minutos
    """
    def __init__(self, descripcion: str, costo_base: float = None, duracion_estimada: int = None, costo: float = None):
        """
        Inicializa una nueva instancia de Servicio.
        
        Args:
            descripcion (str): Descripción del servicio
            costo_base (float): Costo base del servicio
            duracion_estimada (int): Duración estimada en minutos
            costo (float): Costo total del servicio
        """
        self.descripcion = descripcion
        self.costo_base = costo_base if costo_base is not None else costo
        self.duracion_estimada = duracion_estimada

    @abstractmethod
    def calcular_costo(self) -> float:
        """
        Calcula el costo total del servicio.
        
        Returns:
            float: Costo total del servicio
        """
        pass

    def guardar(self):
        """
        Guarda el servicio en la base de datos.
        
        Returns:
            int: ID del servicio guardado
        """
        db = DatabaseConnection()
        query = """
            INSERT INTO servicios (tipo, descripcion, costo_base)
            VALUES (?, ?, ?)
        """
        tipo = self.__class__.__name__.lower()
        db.execute_query(query, (tipo, self.descripcion, self.costo_base))
        return db.execute_query("SELECT last_insert_rowid()")[0][0]

class ServicioReparacion(Servicio):
    """
    Clase que representa un servicio de reparación.
    
    Atributos:
        descripcion (str): Descripción del servicio
        costo_base (float): Costo base del servicio
        duracion_estimada (int): Duración estimada en minutos
        tipo_reparacion (str): Tipo de reparación
    """
    def __init__(self, descripcion: str, costo_base: float = None, duracion_estimada: int = None, tipo_reparacion: str = None, costo: float = None):
        """
        Inicializa una nueva instancia de ServicioReparacion.
        
        Args:
            descripcion (str): Descripción del servicio
            costo_base (float): Costo base del servicio
            duracion_estimada (int): Duración estimada en minutos
            tipo_reparacion (str): Tipo de reparación
            costo (float): Costo total del servicio
        """
        super().__init__(descripcion, costo_base, duracion_estimada, costo)
        self.tipo_reparacion = tipo_reparacion

    def calcular_costo(self) -> float:
        """
        Calcula el costo total del servicio de reparación.
        
        El costo incluye un incremento del 10% por materiales.
        
        Returns:
            float: Costo total del servicio
        """
        return round(self.costo_base * 1.1, 2)  # 10% adicional por materiales

class ServicioSoporteIT(Servicio):
    """
    Clase que representa un servicio de soporte IT.
    
    Atributos:
        descripcion (str): Descripción del servicio
        costo_base (float): Costo base del servicio
        duracion_estimada (int): Duración estimada en minutos
        nivel_soporte (str): Nivel de soporte
    """
    def __init__(self, descripcion: str, costo_base: float = None, duracion_estimada: int = None, nivel_soporte: str = None, costo: float = None):
        """
        Inicializa una nueva instancia de ServicioSoporteIT.
        
        Args:
            descripcion (str): Descripción del servicio
            costo_base (float): Costo base del servicio
            duracion_estimada (int): Duración estimada en minutos
            nivel_soporte (str): Nivel de soporte
            costo (float): Costo total del servicio
        """
        super().__init__(descripcion, costo_base, duracion_estimada, costo)
        self.nivel_soporte = nivel_soporte

    def calcular_costo(self) -> float:
        """
        Calcula el costo total del servicio de soporte IT.
        
        El costo incluye un incremento del 20% por soporte especializado.
        
        Returns:
            float: Costo total del servicio
        """
        return round(self.costo_base * 1.2, 2)  # 20% adicional por soporte especializado

class OrdenDeTrabajo:
    """
    Clase que representa una orden de trabajo.
    
    Atributos:
        cliente (Cliente): Cliente asociado a la orden
        tecnico (Tecnico): Técnico asignado a la orden
        servicio (Servicio): Servicio a realizar
        descripcion (str): Descripción detallada de la orden
        fecha_creacion (str): Fecha de creación de la orden
        estado (str): Estado actual de la orden
    """
    def __init__(self, cliente: Cliente, servicio: Servicio, tecnico: Tecnico = None, descripcion: str = None):
        """
        Inicializa una nueva instancia de OrdenDeTrabajo.
        
        Args:
            cliente (Cliente): Cliente asociado a la orden
            servicio (Servicio): Servicio a realizar
            tecnico (Tecnico): Técnico asignado a la orden
            descripcion (str): Descripción detallada de la orden
        """
        if isinstance(servicio, Tecnico) and (isinstance(tecnico, Servicio) or tecnico is None):
            cliente, tecnico, servicio, descripcion = cliente, servicio, tecnico, descripcion
        self.cliente = cliente
        self.tecnico = tecnico
        self.servicio = servicio
        self.descripcion = descripcion
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.estado = "Pendiente"
        self.costo_total = servicio.calcular_costo()

    def guardar(self):
        """
        Guarda la orden de trabajo en la base de datos.
        
        Returns:
            int: ID de la orden guardada
        """
        db = DatabaseConnection()
        query = """
            INSERT INTO ordenes_trabajo (
                cliente_id, tecnico_id, servicio_id, fecha_creacion,
                estado, descripcion, costo_total
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        # Solo guardar cliente/tecnico si no tienen id
        cliente_id = self.cliente.id if hasattr(self.cliente, 'id') and self.cliente.id else self.cliente.guardar()
        tecnico_id = self.tecnico.id if hasattr(self.tecnico, 'id') and self.tecnico.id else self.tecnico.guardar()
        servicio_id = self.servicio.guardar()
        db.execute_query(query, (
            cliente_id, tecnico_id, servicio_id,
            self.fecha_creacion, self.estado,
            self.descripcion, self.costo_total
        ))
        return db.execute_query("SELECT last_insert_rowid()")[0][0] 