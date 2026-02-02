# Sistema de Gestión de Películas con MongoDB

**Autores:** Paulina Peralta y Katherine Soto  
**Asignatura:** MD003 - Estructuras de datos y su almacenamiento  
**Universidad:** La Salle - Ramón Llull

## Descripción General

Sistema empresarial de gestión de películas construido sobre **MongoDB**, diseñado para demostrar patrones modernos de arquitectura de software, operaciones CRUD avanzadas y análisis de datos mediante agregaciones. El proyecto implementa una solución escalable, modular y auditada para la administración completa del catálogo cinematográfico.

## Arquitectura Modular

Este proyecto adopta una **arquitectura modular y orientada a objetos**, que proporciona múltiples beneficios:

### Ventajas de la Arquitectura Modular

- **Separación de responsabilidades:** Cada módulo tiene una función específica, facilitando el mantenimiento y las pruebas
- **Reutilización de código:** Los componentes pueden ser utilizados independientemente en otros proyectos
- **Escalabilidad:** Agregar nuevas funcionalidades no requiere modificar código existente
- **Mantenibilidad:** Los cambios se localizan en módulos específicos, reduciendo el riesgo de efectos secundarios
- **Testabilidad:** Los módulos pueden ser testeados de forma aislada

### Implementación Orientada a Objetos

La solución utiliza **clases** como abstracción fundamental para modelar entidades y operaciones:

- **DatabaseManager:** Gestiona la conexión y ciclo de vida de la base de datos
- **CRUDOperations:** Encapsula todas las operaciones de creación, lectura, actualización y eliminación
- **QueryOperations:** Proporciona consultas avanzadas y agregaciones de datos
- **CLI:** Interfaz de línea de comandos para interacción del usuario

Esta estructura orientada a objetos facilita la extensibilidad y mantiene el código limpio y legible.

## Consideraciones de Seguridad y Auditoría

Cada documento en la base de datos incorpora tres campos críticos para auditoría y seguridad:

### Campos de Auditoría Implementados

| Campo | Tipo | Propósito |
|-------|------|----------|
| **_id (UUID)** | UUID v4 | Identificador único distribuido para cada documento |
| **createdAt** | ISO 8601 DateTime | Timestamp de creación del documento |
| **updatedAt** | ISO 8601 DateTime | Timestamp de última modificación |

Estos campos permiten:
- **Trazabilidad completa:** Identificar cuándo se creó y modificó cada registro
- **Seguridad:** Detectar cambios no autorizados mediante comparación de timestamps
- **Cumplimiento normativo:** Satisfacer requisitos de auditoría en entornos empresariales
- **Análisis histórico:** Generar reportes temporales del estado de los datos
- **Identificación única:** Garantizar que cada película tenga un identificador único a nivel global

## Estructura del Proyecto

```
gestion_peliculas/
    __init__.py      - Definicion del paquete
    config.py        - Configuracion MongoDB y logging
    models.py        - Datos de peliculas y esquema JSON
    database.py      - Conexion y configuracion de BD
    crud.py          - Operaciones CRUD
    queries.py       - Consultas avanzadas y agregaciones
    cli.py           - Interfaz de linea de comandos
    app.py           - Interfaz grafica web (Streamlit)
    main.py          - Punto de entrada principal
    requirements.txt - Dependencias
```

## Instalacion

```bash
pip install -r requirements.txt
```

## Configuracion

Editar `config.py` para cambiar la URI de MongoDB:

```python
MONGO_URI = "mongodb://localhost:27017/"
```

## Ejecucion

### Linea de Comandos

```bash
python main.py
```
El cual ejecutara todas las funciones implementadas del proyecto y al ultimo preguntara si vas a querer entrar al cli (y/n). Con "y" ingresas

### Como modulo

```python
from gestion_peliculas import DatabaseManager, CRUDOperations, QueryOperations

db = DatabaseManager()
db.conectar()
db.inicializar_datos()

crud = CRUDOperations(db.collection)
queries = QueryOperations(db.collection)

peliculas = crud.buscar_por_director("Nolan")
top5 = queries.top_peliculas(5)
```

## Funcionalidades Implementadas

### CRUD (30 pts)
- Insertar peliculas con estructura completa
- Actualizar ratings
- Añadir/eliminar reviews
- Busquedas por titulo, genero, director, rating

### Consultas Avanzadas (30 pts)
- Peliculas por rango de años
- Rating promedio por genero
- Directores con mas peliculas
- Busqueda por palabra clave

### Agregaciones (30 pts)
- Estadisticas por genero
- Top 5 peliculas mejor valoradas
- Analisis de reviews por pelicula
- Reporte de peliculas por decada

### Bonus (10 pts)
- Busqueda de texto completo (indice TEXT)
- Indices para optimizacion de consultas
- Interfaz CLI interactiva
- Interfaz web con Streamlit
- Validacion de esquema JSON


