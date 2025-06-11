import sqlite3
from typing import Optional, List, Tuple, Any
import os

class DatabaseConnection:
    """
    Clase para manejar la conexión a la base de datos SQLite.
    
    Esta clase implementa el patrón Singleton para asegurar una única
    instancia de conexión a la base de datos. Proporciona métodos para
    ejecutar consultas SQL y gestionar transacciones.
    
    Atributos:
        _instance (DatabaseConnection): Instancia única de la clase
        _conn (sqlite3.Connection): Conexión a la base de datos
        _cursor (sqlite3.Cursor): Cursor para ejecutar consultas
    """
    _instance = None

    def __new__(cls):
        """
        Implementa el patrón Singleton para la conexión a la base de datos.
        
        Returns:
            DatabaseConnection: La única instancia de la clase
        """
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Inicializa la conexión a la base de datos y crea las tablas necesarias.
        
        Este método es llamado automáticamente al crear la primera instancia
        de la clase. Crea la base de datos si no existe y configura las
        tablas necesarias para el sistema.
        """
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')
        self._conn = sqlite3.connect(db_path)
        self._cursor = self._conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """
        Crea las tablas necesarias en la base de datos si no existen.
        
        Crea las siguientes tablas:
        - clientes: Almacena información de los clientes
        - tecnicos: Almacena información de los técnicos
        - servicios: Almacena información de los servicios
        - ordenes_trabajo: Almacena las órdenes de trabajo
        """
        self._cursor.executescript('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE,
                telefono TEXT,
                direccion TEXT
            );

            CREATE TABLE IF NOT EXISTS tecnicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especialidad TEXT NOT NULL,
                email TEXT UNIQUE,
                telefono TEXT
            );

            CREATE TABLE IF NOT EXISTS servicios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                costo_base REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ordenes_trabajo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                tecnico_id INTEGER,
                servicio_id INTEGER,
                fecha_creacion TEXT NOT NULL,
                estado TEXT NOT NULL,
                descripcion TEXT,
                costo_total REAL,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (tecnico_id) REFERENCES tecnicos (id),
                FOREIGN KEY (servicio_id) REFERENCES servicios (id)
            );
        ''')
        self._conn.commit()

    def execute_query(self, query: str, params: tuple = ()) -> Optional[List[Tuple[Any, ...]]]:
        """
        Ejecuta una consulta SQL en la base de datos.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple): Parámetros para la consulta SQL
            
        Returns:
            Optional[List[Tuple[Any, ...]]]: Resultados de la consulta o None si es una operación de escritura
            
        Raises:
            sqlite3.Error: Si ocurre un error al ejecutar la consulta
        """
        try:
            self._cursor.execute(query, params)
            if query.strip().upper().startswith(('SELECT', 'PRAGMA')):
                return self._cursor.fetchall()
            self._conn.commit()
            return None
        except sqlite3.Error as e:
            self._conn.rollback()
            raise e

    def close(self):
        """
        Cierra la conexión a la base de datos.
        
        Este método debe ser llamado cuando ya no se necesite la conexión
        para liberar los recursos.
        """
        if hasattr(self, '_conn'):
            self._conn.close() 