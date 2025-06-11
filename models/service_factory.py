from typing import Dict, Type
from models.models import Servicio, ServicioReparacion, ServicioSoporteIT

class ServiceFactory:
    """
    Fábrica para la creación de diferentes tipos de servicios.
    
    Esta clase implementa el patrón Factory Method para encapsular la lógica
    de creación de diferentes tipos de servicios. Permite crear instancias
    de servicios específicos sin exponer la lógica de creación al cliente.
    
    Atributos:
        _service_types (Dict[str, Type[Servicio]]): Diccionario que mapea
            tipos de servicio con sus clases correspondientes
    
    Métodos:
        create_service(): Crea una instancia del tipo de servicio solicitado
    """
    _service_types: Dict[str, Type[Servicio]] = {
        'reparacion': ServicioReparacion,
        'soporte_it': ServicioSoporteIT
    }

    @classmethod
    def create_service(cls, service_type: str, **kwargs) -> Servicio:
        """
        Crea una instancia del tipo de servicio solicitado.
        
        Este método actúa como fábrica para crear diferentes tipos de servicios
        basándose en el tipo especificado. Utiliza el diccionario _service_types
        para mapear el tipo de servicio con su clase correspondiente.
        
        Args:
            service_type (str): Tipo de servicio a crear ('reparacion' o 'soporte_it')
            **kwargs: Argumentos adicionales requeridos para la creación del servicio
                - Para reparacion:
                    - descripcion (str)
                    - costo (float)
                    - duracion_estimada (int)
                    - tipo_reparacion (str)
                - Para soporte_it:
                    - descripcion (str)
                    - costo (float)
                    - duracion_estimada (int)
                    - nivel_soporte (str)
        
        Returns:
            Servicio: Una instancia del tipo de servicio solicitado
        
        Raises:
            ValueError: Si el tipo de servicio no está soportado
        """
        if service_type not in cls._service_types:
            raise ValueError(f"Tipo de servicio no soportado: {service_type}")
        # Compatibilidad: mapear 'costo' a 'costo_base' si es necesario
        if 'costo' in kwargs and 'costo_base' not in kwargs:
            kwargs['costo_base'] = kwargs['costo']
        service_class = cls._service_types[service_type]
        return service_class(**kwargs) 