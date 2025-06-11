# Sistema de Gestión de Servicios Técnicos

Aplicación de escritorio para la gestión de servicios técnicos, desarrollada en Python usando Tkinter y SQLite.

## Características

- Gestión completa de clientes
- Gestión de técnicos y especialidades
- Creación y seguimiento de órdenes de trabajo
- Múltiples tipos de servicios (reparación y soporte IT)
- Sistema de notificaciones automáticas
- Interfaz gráfica intuitiva y fácil de usar

## Arquitectura del Sistema

### Patrones de Diseño Implementados

1. **Singleton (Instancia Única)**
   - Implementado en `DatabaseConnection`
   - Garantiza una única conexión a la base de datos
   - Optimiza el uso de recursos
   - Facilita la gestión de transacciones

2. **Factory (Fábrica)**
   - Implementado en `ServiceFactory`
   - Centraliza la creación de diferentes tipos de servicios
   - Permite agregar nuevos tipos de servicios fácilmente
   - Encapsula la lógica de creación de objetos

3. **Observer (Observador)**
   - Sistema de notificaciones para técnicos
   - Notificaciones automáticas de nuevas órdenes
   - Desacoplamiento entre emisores y receptores
   - Facilita la comunicación entre componentes

### Estructura del Proyecto

```
.
├── database/
│   └── db_connection.py    # Gestión de conexión a base de datos
├── models/
│   ├── models.py          # Clases principales del sistema
│   ├── service_factory.py # Fábrica de servicios
│   └── observer.py        # Sistema de notificaciones
├── tests/
│   └── test_models.py     # Pruebas unitarias
├── main.py                # Aplicación principal
├── requirements.txt       # Dependencias
└── README.md             # Documentación
```

## Requisitos del Sistema

- Python 3.8 o superior
- Tkinter (incluido en Python)
- SQLite3 (incluido en Python)
- pytest (para pruebas unitarias)

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone [url-del-repositorio]
   ```

2. Crear entorno virtual (recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso del Sistema

### Gestión de Clientes

1. **Registro de Clientes**
   - Ingresar nombre, email, teléfono y dirección
   - Validación automática de datos
   - Almacenamiento en base de datos

2. **Consulta de Clientes**
   - Lista completa de clientes
   - Búsqueda por diferentes criterios
   - Visualización de historial de servicios

### Gestión de Técnicos

1. **Registro de Técnicos**
   - Datos personales y de contacto
   - Especialidades técnicas
   - Disponibilidad

2. **Asignación de Trabajos**
   - Asignación automática según especialidad
   - Notificaciones de nuevas órdenes
   - Seguimiento de carga de trabajo

### Órdenes de Trabajo

1. **Creación de Órdenes**
   - Selección de cliente
   - Tipo de servicio
   - Asignación de técnico
   - Descripción del problema

2. **Seguimiento**
   - Estado de la orden
   - Historial de actualizaciones
   - Notificaciones de cambios

## Base de Datos

### Tablas Principales

1. **Clientes**
   - ID (clave primaria)
   - Nombre
   - Email
   - Teléfono
   - Dirección

2. **Técnicos**
   - ID (clave primaria)
   - Nombre
   - Especialidad
   - Email
   - Teléfono

3. **Servicios**
   - ID (clave primaria)
   - Tipo
   - Descripción
   - Costo
   - Duración estimada

4. **Órdenes de Trabajo**
   - ID (clave primaria)
   - Cliente (clave foránea)
   - Técnico (clave foránea)
   - Servicio (clave foránea)
   - Fecha de creación
   - Estado

## Pruebas

El sistema incluye pruebas unitarias para validar:
- Creación de objetos
- Cálculos de costos
- Gestión de órdenes
- Funcionalidad de la fábrica de servicios

Para ejecutar las pruebas:
```bash
pytest tests/
```

## Mantenimiento

### Actualizaciones
- Revisar regularmente las dependencias
- Actualizar la base de datos según necesidades
- Mantener copias de seguridad

### Mejores Prácticas
- Seguir las convenciones de código
- Documentar cambios importantes
- Realizar pruebas antes de implementar cambios

## Contribución

1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit de cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 