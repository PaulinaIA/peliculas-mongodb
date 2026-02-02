# Sistema de Gestion de Peliculas con MongoDB

**Autor:** Paulina Peralta  
**Asignatura:** MD003 - Estructuras de datos y su almacenamiento  
**Universidad:** La Salle - Ramon Llull

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
MONGO_URI = "mongodb://localhost:27017/"  # Cambiar segun tu configuracion
```

## Ejecucion

### Opcion 1: Interfaz Web (Streamlit)

```bash
streamlit run app.py
```

Abre automaticamente en http://localhost:8501

### Opcion 2: Linea de Comandos

```bash
python main.py
```

### Opcion 3: Como modulo

```python
from gestion_peliculas import DatabaseManager, CRUDOperations, QueryOperations

db = DatabaseManager()
db.conectar()
db.inicializar_datos()

crud = CRUDOperations(db.collection)
queries = QueryOperations(db.collection)

# Usar las operaciones
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
