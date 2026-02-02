"""
Operaciones CRUD para la coleccion de peliculas.
"""

from pymongo.collection import Collection
from pymongo.errors import PyMongoError, WriteError
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid

from config import logger


class CRUDOperations:
    """
    Operaciones Create, Read, Update, Delete para peliculas.
    """
    
    def __init__(self, collection: Collection):
        """
        Inicializa con la coleccion de MongoDB.
        
        Args:
            collection: Coleccion de peliculas
        """
        self.collection = collection
    
    # ==================== CREATE ====================
    
    def insertar_pelicula(self, pelicula: Dict[str, Any]) -> Optional[str]:
        """
        Inserta una nueva pelicula.
        
        Args:
            pelicula: Diccionario con datos de la pelicula
            
        Returns:
            ID de la pelicula insertada o None si hay error
        """
        try:
            pelicula["id"] = str(uuid.uuid4())
            pelicula["createdAt"] = datetime.now()
            pelicula["updatedAt"] = datetime.now()
            
            resultado = self.collection.insert_one(pelicula)
            logger.info(f"Pelicula '{pelicula.get('titulo')}' insertada")
            return str(resultado.inserted_id)
        except WriteError as e:
            logger.error(f"Error de validacion: {e.details}")
            return None
        except PyMongoError as e:
            logger.error(f"Error al insertar: {e}")
            return None
    
    # ==================== READ ====================
    
    def obtener_todas(self) -> List[Dict]:
        """Obtiene todas las peliculas ordenadas por rating."""
        return list(self.collection.find(
            {},
            {"_id": 0, "titulo": 1, "año": 1, "rating": 1, "director": 1}
        ).sort("rating", -1))
    
    def buscar_por_titulo(self, titulo: str) -> List[Dict]:
        """Busca peliculas que contengan el texto en el titulo."""
        return list(self.collection.find(
            {"titulo": {"$regex": titulo, "$options": "i"}},
            {"_id": 0, "titulo": 1, "año": 1, "director": 1, "rating": 1}
        ))
    
    def buscar_por_genero(self, genero: str) -> List[Dict]:
        """Busca peliculas por genero."""
        return list(self.collection.find(
            {"generos": genero},
            {"_id": 0, "titulo": 1, "año": 1, "generos": 1, "rating": 1}
        ))
    
    def buscar_por_director(self, director: str) -> List[Dict]:
        """Busca peliculas por director."""
        return list(self.collection.find(
            {"director": {"$regex": director, "$options": "i"}},
            {"_id": 0, "titulo": 1, "año": 1, "director": 1, "rating": 1}
        ))
    
    def buscar_por_rating_minimo(self, rating_min: float) -> List[Dict]:
        """Busca peliculas con rating mayor o igual al especificado."""
        return list(self.collection.find(
            {"rating": {"$gte": rating_min}},
            {"_id": 0, "titulo": 1, "rating": 1, "director": 1}
        ).sort("rating", -1))
    
    def buscar_por_palabra_clave(self, palabra: str) -> List[Dict]:
        """Busca en titulo y comentarios de reviews."""
        return list(self.collection.find(
            {"$or": [
                {"titulo": {"$regex": palabra, "$options": "i"}},
                {"reviews.comentario": {"$regex": palabra, "$options": "i"}}
            ]},
            {"_id": 0, "titulo": 1, "reviews.comentario": 1, "rating": 1}
        ))
    
    def busqueda_texto_completo(self, texto: str) -> List[Dict]:
        """Realiza busqueda de texto completo usando indice."""
        return list(self.collection.find(
            {"$text": {"$search": texto}},
            {"_id": 0, "score": {"$meta": "textScore"}, "titulo": 1, "director": 1, "rating": 1}
        ).sort([("score", {"$meta": "textScore"})]))
    
    # ==================== UPDATE ====================
    
    def actualizar_rating(self, titulo: str, nuevo_rating: float) -> bool:
        """
        Actualiza el rating de una pelicula.
        
        Args:
            titulo: Titulo de la pelicula
            nuevo_rating: Nuevo valor de rating (0-10)
            
        Returns:
            True si se actualizo correctamente
        """
        if not 0 <= nuevo_rating <= 10:
            logger.error("Rating debe estar entre 0 y 10")
            return False
        
        resultado = self.collection.update_one(
            {"titulo": titulo},
            {"$set": {"rating": nuevo_rating, "updatedAt": datetime.now()}}
        )
        
        if resultado.modified_count > 0:
            logger.info(f"Rating de '{titulo}' actualizado a {nuevo_rating}")
            return True
        
        logger.warning(f"Pelicula '{titulo}' no encontrada")
        return False
    
    def añadir_review(
        self,
        titulo: str,
        usuario: str,
        puntuacion: int,
        comentario: str
    ) -> bool:
        """
        Añade una review a una pelicula.
        
        Args:
            titulo: Titulo de la pelicula
            usuario: Nombre del usuario
            puntuacion: Puntuacion (1-10)
            comentario: Texto del comentario
            
        Returns:
            True si se añadio correctamente
        """
        if not 1 <= puntuacion <= 10:
            logger.error("Puntuacion debe estar entre 1 y 10")
            return False
        
        nueva_review = {
            "usuario": usuario,
            "puntuacion": puntuacion,
            "comentario": comentario,
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "createdAt": datetime.now()
        }
        
        resultado = self.collection.update_one(
            {"titulo": titulo},
            {
                "$push": {"reviews": nueva_review},
                "$set": {"updatedAt": datetime.now()}
            }
        )
        
        if resultado.modified_count > 0:
            logger.info(f"Review añadida a '{titulo}' por {usuario}")
            return True
        
        logger.warning(f"Pelicula '{titulo}' no encontrada")
        return False
    
    # ==================== DELETE ====================
    
    def eliminar_review(self, titulo: str, usuario: str) -> bool:
        """
        Elimina una review de una pelicula.
        
        Args:
            titulo: Titulo de la pelicula
            usuario: Nombre del usuario cuya review eliminar
            
        Returns:
            True si se elimino correctamente
        """
        resultado = self.collection.update_one(
            {"titulo": titulo},
            {
                "$pull": {"reviews": {"usuario": usuario}},
                "$set": {"updatedAt": datetime.now()}
            }
        )
        
        if resultado.modified_count > 0:
            logger.info(f"Review de '{usuario}' eliminada de '{titulo}'")
            return True
        
        logger.warning("Review no encontrada")
        return False
    
    def eliminar_pelicula(self, titulo: str) -> bool:
        """
        Elimina una pelicula de la coleccion.
        
        Args:
            titulo: Titulo de la pelicula
            
        Returns:
            True si se elimino correctamente
        """
        resultado = self.collection.delete_one({"titulo": titulo})
        
        if resultado.deleted_count > 0:
            logger.info(f"Pelicula '{titulo}' eliminada")
            return True
        
        logger.warning(f"Pelicula '{titulo}' no encontrada")
        return False
