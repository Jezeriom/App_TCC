import pytest
from models.models import Cliente, Tecnico, ServicioReparacion, ServicioSoporteIT, OrdenDeTrabajo
from models.service_factory import ServiceFactory

def test_cliente_creation():
    cliente = Cliente("Juan Pérez", "juan@email.com", "123456789", "Calle 123")
    assert cliente.nombre == "Juan Pérez"
    assert cliente.id is None  # ID should be None before saving

def test_tecnico_creation():
    tecnico = Tecnico("María García", "Hardware", "maria@email.com", "987654321")
    assert tecnico.nombre == "María García"
    assert tecnico.id is None

def test_servicio_reparacion():
    servicio = ServicioReparacion(
        "Reparación de laptop",
        100.0,
        120,
        "Hardware"
    )
    assert servicio.calcular_costo() == 110.0  # 10% adicional

def test_servicio_soporte_it():
    servicio = ServicioSoporteIT(
        "Soporte remoto",
        80.0,
        60,
        "Nivel 2"
    )
    assert servicio.calcular_costo() == 96.0  # 20% adicional

def test_service_factory():
    servicio = ServiceFactory.create_service(
        service_type="reparacion",
        descripcion="Reparación de PC",
        costo=150.0,
        duracion_estimada=90,
        tipo_reparacion="Hardware"
    )
    assert isinstance(servicio, ServicioReparacion)
    assert servicio.calcular_costo() == 165.0

def test_orden_trabajo():
    cliente = Cliente("Juan Pérez", "juan@email.com", "123456789", "Calle 123")
    tecnico = Tecnico("María García", "Hardware", "maria@email.com", "987654321")
    servicio = ServicioReparacion("Reparación", 100.0, 60, "Hardware")
    
    orden = OrdenDeTrabajo(cliente, servicio, tecnico)
    assert orden.cliente == cliente
    assert orden.tecnico == tecnico
    assert orden.servicio == servicio 