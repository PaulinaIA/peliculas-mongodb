"""
Modulo de conexion y configuracion de MongoDB.
"""

from pymongo import MongoClient, TEXT, ASCENDING, DESCENDING
from pymongo.errors import PyMongoError
from pymongo.collection import Collection
from pymongo.database import Database
from datetime import datetime
from typing import Optional, List
import uuid

from config import MONGO_URI, DB_NAME, COLLECTION_NAME, logger
from models import PELICULAS_INICIALES, SCHEMA_VALIDATOR


class DatabaseManager:
    """
    Gestor de conexion a MongoDB.
    
    Maneja la conexion, inicializacion de datos, creacion de indices
    y validacion de esquema.
    """
    
    def __init__(
        self,
        uri: str = MONGO_URI,
        db_name: str = DB_NAME,
        collection_name: str = COLLECTION_NAME
    ):
        """
        Inicializa la conexion a MongoDB.
        
        Args:
            uri: URI de conexion a MongoDB
            db_name: Nombre de la base de datos
            collection_name: Nombre de la coleccion
        """
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.collection: Optional[Collection] = None
    
    def conectar(self) -> bool:
        """
        Establece conexion con MongoDB.
        
        Returns:
            True si la conexion fue exitosa
        """
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            logger.info(f"Conectado a MongoDB: {self.uri}")
            logger.info(f"Base de datos: {self.db_name} | Coleccion: {self.collection_name}")
            return True
        except PyMongoError as e:
            logger.error(f"Error de conexion: {e}")
            return False
    
    def desconectar(self) -> None:
        """Cierra la conexion a MongoDB."""
        if self.client:
            self.client.close()
            logger.info("Conexion cerrada")
    
    def inicializar_datos(self, limpiar: bool = True) -> int:
        """
        Carga las peliculas iniciales en la base de datos.
        
        Args:
            limpiar: Si True, elimina datos existentes
            
        Returns:
            Numero de peliculas insertadas
        """
        if limpiar:
            self.collection.drop()
            logger.info("Coleccion limpiada")
        
        timestamp = datetime.now()
        peliculas = []
        
        for p in PELICULAS_INICIALES:
            pelicula = p.copy()
            pelicula["id"] = str(uuid.uuid4())
            pelicula["createdAt"] = timestamp
            pelicula["updatedAt"] = timestamp
            peliculas.append(pelicula)
        
        resultado = self.collection.insert_many(peliculas)
        count = len(resultado.inserted_ids)
        logger.info(f"{count} peliculas insertadas")
        return count
    
    def crear_indices(self) -> List[str]:
        """
        Crea indices para optimizar consultas.
        
        Returns:
            Lista de nombres de indices creados
        """
        indices_config = [
            ([("titulo", ASCENDING)], "idx_titulo"),
            ([("año", DESCENDING)], "idx_año"),
            ([("generos", ASCENDING)], "idx_generos"),
            ([("rating", DESCENDING)], "idx_rating"),
            ([("director", ASCENDING)], "idx_director"),
        ]
        
        indices_creados = []
        
        for campos, nombre in indices_config:
            try:
                self.collection.create_index(campos, name=nombre)
                indices_creados.append(nombre)
            except PyMongoError as e:
                logger.warning(f"Indice {nombre}: {e}")
        
        # Indice de texto completo
        try:
            self.collection.create_index(
                [("titulo", TEXT), ("reviews.comentario", TEXT), ("director", TEXT)],
                name="idx_texto",
                default_language="spanish"
            )
            indices_creados.append("idx_texto")
        except PyMongoError:
            logger.warning("Indice de texto ya existe")
        
        logger.info(f"Indices creados: {indices_creados}")
        return indices_creados
    
    def aplicar_validacion(self) -> bool:
        """
        Aplica validacion de esquema JSON a la coleccion.
        
        Returns:
            True si se aplico correctamente
        """
        try:
            self.db.command(
                "collMod",
                self.collection_name,
                validator=SCHEMA_VALIDATOR,
                validationLevel="moderate"
            )
            logger.info("Validacion de esquema aplicada")
            return True
        except PyMongoError as e:
            logger.error(f"Error en validacion: {e}")
            return False
    
    def listar_indices(self) -> List[dict]:
        """Lista todos los indices de la coleccion."""
        return list(self.collection.list_indexes())
