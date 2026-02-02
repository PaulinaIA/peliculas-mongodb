"""
Sistema de Gestion de Peliculas con MongoDB
============================================

Modulos:
    - config: Configuracion y logging
    - models: Datos de peliculas y esquema de validacion
    - database: Conexion y configuracion de MongoDB
    - crud: Operaciones Create, Read, Update, Delete
    - queries: Consultas avanzadas y agregaciones
    - cli: Interfaz de linea de comandos
    - main: Punto de entrada principal
"""

from database import DatabaseManager
from crud import CRUDOperations
from queries import QueryOperations
from cli import CLI

__version__ = "1.0.0"
__author__ = "Paulina Peralta"

__all__ = [
    "DatabaseManager",
    "CRUDOperations", 
    "QueryOperations",
    "CLI"
]
