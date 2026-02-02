"""
Configuracion del sistema de gestion de peliculas.
"""

import logging

# Configuracion de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "gestion_peliculas"
COLLECTION_NAME = "peliculas"

# Configuracion de logging
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Configurar logger
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)
