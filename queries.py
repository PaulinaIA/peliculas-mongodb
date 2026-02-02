"""
Consultas avanzadas y agregaciones para peliculas.
"""

from pymongo.collection import Collection
from pymongo import ASCENDING, DESCENDING
from typing import List, Dict, Any


class QueryOperations:
    """
    Consultas avanzadas y agregaciones con pipelines de MongoDB.
    """
    
    def __init__(self, collection: Collection):
        """
        Inicializa con la coleccion de MongoDB.
        
        Args:
            collection: Coleccion de peliculas
        """
        self.collection = collection
    
    # ==================== CONSULTAS AVANZADAS ====================
    
    def peliculas_por_rango_años(self, año_inicio: int, año_fin: int) -> List[Dict]:
        """
        Encuentra peliculas dentro de un rango de años.
        
        Args:
            año_inicio: Año inicial del rango
            año_fin: Año final del rango
            
        Returns:
            Lista de peliculas en el rango
        """
        return list(self.collection.find(
            {"año": {"$gte": año_inicio, "$lte": año_fin}},
            {"_id": 0, "titulo": 1, "año": 1, "director": 1, "rating": 1}
        ).sort("año", ASCENDING))
    
    def rating_promedio_por_genero(self) -> List[Dict]:
        """
        Calcula el rating promedio por genero.
        
        Returns:
            Lista con genero, rating promedio y cantidad
        """
        pipeline = [
            {"$unwind": "$generos"},
            {"$group": {
                "_id": "$generos",
                "rating_promedio": {"$avg": "$rating"},
                "cantidad": {"$sum": 1}
            }},
            {"$sort": {"rating_promedio": DESCENDING}},
            {"$project": {
                "_id": 0,
                "genero": "$_id",
                "rating_promedio": {"$round": ["$rating_promedio", 2]},
                "cantidad": 1
            }}
        ]
        return list(self.collection.aggregate(pipeline))
    
    def directores_con_mas_peliculas(self, limite: int = 5) -> List[Dict]:
        """
        Lista directores ordenados por cantidad de peliculas.
        
        Args:
            limite: Numero maximo de directores a retornar
            
        Returns:
            Lista de directores con sus peliculas
        """
        pipeline = [
            {"$group": {
                "_id": "$director",
                "cantidad": {"$sum": 1},
                "peliculas": {"$push": "$titulo"},
                "rating_promedio": {"$avg": "$rating"}
            }},
            {"$sort": {"cantidad": DESCENDING, "rating_promedio": DESCENDING}},
            {"$limit": limite},
            {"$project": {
                "_id": 0,
                "director": "$_id",
                "cantidad": 1,
                "peliculas": 1,
                "rating_promedio": {"$round": ["$rating_promedio", 2]}
            }}
        ]
        return list(self.collection.aggregate(pipeline))
    
    # ==================== AGREGACIONES ====================
    
    def estadisticas_por_genero(self) -> List[Dict]:
        """
        Calcula estadisticas completas por genero.
        
        Returns:
            Lista con estadisticas por genero
        """
        pipeline = [
            {"$unwind": "$generos"},
            {"$group": {
                "_id": "$generos",
                "cantidad": {"$sum": 1},
                "rating_promedio": {"$avg": "$rating"},
                "rating_max": {"$max": "$rating"},
                "rating_min": {"$min": "$rating"},
                "presupuesto_total": {"$sum": "$metadata.presupuesto"},
                "duracion_promedio": {"$avg": "$metadata.duracion_minutos"}
            }},
            {"$sort": {"cantidad": DESCENDING}},
            {"$project": {
                "_id": 0,
                "genero": "$_id",
                "cantidad": 1,
                "rating_promedio": {"$round": ["$rating_promedio", 2]},
                "rating_max": 1,
                "rating_min": 1,
                "presupuesto_total": 1,
                "duracion_promedio": {"$round": ["$duracion_promedio", 0]}
            }}
        ]
        return list(self.collection.aggregate(pipeline))
    
    def top_peliculas(self, n: int = 5) -> List[Dict]:
        """
        Obtiene las top N peliculas mejor valoradas.
        
        Combina rating oficial con promedio de reviews.
        
        Args:
            n: Numero de peliculas a retornar
            
        Returns:
            Lista de top peliculas
        """
        pipeline = [
            {"$addFields": {
                "promedio_reviews": {"$avg": "$reviews.puntuacion"}
            }},
            {"$addFields": {
                "score_combinado": {
                    "$avg": ["$rating", {"$ifNull": ["$promedio_reviews", "$rating"]}]
                }
            }},
            {"$sort": {"score_combinado": DESCENDING}},
            {"$limit": n},
            {"$project": {
                "_id": 0,
                "titulo": 1,
                "director": 1,
                "año": 1,
                "rating": 1,
                "promedio_reviews": {"$round": [{"$ifNull": ["$promedio_reviews", 0]}, 2]},
                "score_combinado": {"$round": ["$score_combinado", 2]},
                "generos": 1
            }}
        ]
        return list(self.collection.aggregate(pipeline))
    
    def analisis_reviews(self) -> List[Dict]:
        """
        Analiza las reviews de cada pelicula.
        
        Returns:
            Lista con analisis de reviews por pelicula
        """
        pipeline = [
            {"$project": {
                "_id": 0,
                "titulo": 1,
                "rating": 1,
                "num_reviews": {"$size": {"$ifNull": ["$reviews", []]}},
                "promedio_puntuacion": {"$avg": "$reviews.puntuacion"},
                "max_puntuacion": {"$max": "$reviews.puntuacion"},
                "min_puntuacion": {"$min": "$reviews.puntuacion"}
            }},
            {"$match": {"num_reviews": {"$gt": 0}}},
            {"$sort": {"num_reviews": DESCENDING, "promedio_puntuacion": DESCENDING}},
            {"$project": {
                "titulo": 1,
                "rating": 1,
                "num_reviews": 1,
                "promedio_puntuacion": {"$round": ["$promedio_puntuacion", 2]},
                "max_puntuacion": 1,
                "min_puntuacion": 1
            }}
        ]
        return list(self.collection.aggregate(pipeline))
    
    def reporte_por_decada(self) -> List[Dict]:
        """
        Genera reporte de peliculas agrupadas por decada.
        
        Returns:
            Lista con estadisticas por decada
        """
        pipeline = [
            {"$addFields": {
                "decada": {
                    "$concat": [
                        {"$toString": {"$multiply": [{"$floor": {"$divide": ["$año", 10]}}, 10]}},
                        "s"
                    ]
                }
            }},
            {"$group": {
                "_id": "$decada",
                "cantidad": {"$sum": 1},
                "peliculas": {"$push": {"titulo": "$titulo", "año": "$año", "rating": "$rating"}},
                "rating_promedio": {"$avg": "$rating"},
                "presupuesto_promedio": {"$avg": "$metadata.presupuesto"}
            }},
            {"$sort": {"_id": ASCENDING}},
            {"$project": {
                "_id": 0,
                "decada": "$_id",
                "cantidad": 1,
                "peliculas": 1,
                "rating_promedio": {"$round": ["$rating_promedio", 2]},
                "presupuesto_promedio": {"$round": ["$presupuesto_promedio", 0]}
            }}
        ]
        return list(self.collection.aggregate(pipeline))
    
    def estadisticas_generales(self) -> Dict[str, Any]:
        """
        Obtiene estadisticas generales de la coleccion.
        
        Returns:
            Diccionario con estadisticas
        """
        pipeline = [
            {"$facet": {
                "total": [{"$count": "count"}],
                "generos": [{"$unwind": "$generos"}, {"$group": {"_id": "$generos"}}],
                "directores": [{"$group": {"_id": "$director"}}],
                "reviews": [{"$unwind": "$reviews"}, {"$count": "count"}]
            }}
        ]
        result = list(self.collection.aggregate(pipeline))[0]
        
        return {
            "total_peliculas": result["total"][0]["count"] if result["total"] else 0,
            "generos_unicos": len(result["generos"]),
            "directores": len(result["directores"]),
            "total_reviews": result["reviews"][0]["count"] if result["reviews"] else 0
        }
