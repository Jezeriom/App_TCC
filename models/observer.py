from abc import ABC, abstractmethod
from typing import List
from models.models import OrdenDeTrabajo

class Observer(ABC):
    """
    Clase base abstracta para los observadores en el patrón Observer.
    
    Esta clase define la interfaz que deben implementar todos los observadores
    que deseen recibir notificaciones sobre cambios en el estado de las órdenes
    de trabajo.
    
    Métodos:
        update(): Método abstracto que será llamado cuando el sujeto notifique
            un cambio
    """
    @abstractmethod
    def update(self, orden: OrdenDeTrabajo):
        """
        Método que será llamado cuando el sujeto notifique un cambio.
        
        Este método debe ser implementado por las clases concretas que
        deseen recibir notificaciones. Define la acción a realizar cuando
        se recibe una notificación.
        
        Args:
            orden (OrdenDeTrabajo): La orden de trabajo que ha cambiado
        """
        pass

class Subject(ABC):
    """
    Clase base abstracta para los sujetos en el patrón Observer.
    
    Esta clase define la interfaz para los sujetos que pueden ser observados.
    Mantiene una lista de observadores y proporciona métodos para agregar,
    eliminar y notificar a los observadores.
    
    Atributos:
        _observers (List[Observer]): Lista de observadores registrados
    
    Métodos:
        attach(): Registra un nuevo observador
        detach(): Elimina un observador registrado
        notify(): Notifica a todos los observadores sobre un cambio
    """
    def __init__(self):
        """
        Inicializa una nueva instancia de Subject.
        
        Crea una lista vacía para almacenar los observadores registrados.
        """
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        """
        Registra un nuevo observador.
        
        Agrega un observador a la lista de observadores si no está
        ya registrado.
        
        Args:
            observer (Observer): El observador a registrar
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        """
        Elimina un observador registrado.
        
        Remueve un observador de la lista de observadores.
        
        Args:
            observer (Observer): El observador a eliminar
        """
        self._observers.remove(observer)

    def notify(self, orden: OrdenDeTrabajo):
        """
        Notifica a todos los observadores sobre un cambio.
        
        Llama al método update() de cada observador registrado,
        pasándole la orden de trabajo que ha cambiado.
        
        Args:
            orden (OrdenDeTrabajo): La orden de trabajo que ha cambiado
        """
        for observer in self._observers:
            observer.update(orden)

class OrdenSubject(Subject):
    """
    Implementación concreta del sujeto para las órdenes de trabajo.
    
    Esta clase extiende la funcionalidad del Subject base para manejar
    específicamente las notificaciones relacionadas con órdenes de trabajo.
    
    Métodos:
        nueva_orden(): Crea una nueva orden y notifica a los observadores
    """
    def nueva_orden(self, orden: OrdenDeTrabajo):
        """
        Crea una nueva orden y notifica a los observadores.
        
        Este método es llamado cuando se crea una nueva orden de trabajo
        y notifica a todos los observadores registrados.
        
        Args:
            orden (OrdenDeTrabajo): La nueva orden de trabajo creada
        """
        self.notify(orden) 