"""
Modelos de datos y esquema de validacion para peliculas.
"""

from typing import List, Dict, Any


PELICULAS_INICIALES: List[Dict[str, Any]] = [
    {
        "titulo": "Inception",
        "año": 2010,
        "director": "Christopher Nolan",
        "generos": ["Ciencia Ficcion", "Accion", "Thriller"],
        "rating": 8.8,
        "actores": [
            {"nombre": "Leonardo DiCaprio", "rol": "Dom Cobb"},
            {"nombre": "Joseph Gordon-Levitt", "rol": "Arthur"}
        ],
        "reviews": [
            {"usuario": "DreamWatcher", "puntuacion": 9, 
             "comentario": "Mente brillante de Nolan", "fecha": "2024-01-10"}
        ],
        "disponible": True,
        "metadata": {"duracion_minutos": 148, "idioma_original": "Ingles", "presupuesto": 160000000}
    },
    {
        "titulo": "Parasitos",
        "año": 2019,
        "director": "Bong Joon-ho",
        "generos": ["Drama", "Thriller", "Comedia"],
        "rating": 8.5,
        "actores": [
            {"nombre": "Song Kang-ho", "rol": "Kim Ki-taek"},
            {"nombre": "Choi Woo-shik", "rol": "Kim Ki-woo"}
        ],
        "reviews": [
            {"usuario": "KoreanCinema", "puntuacion": 10, 
             "comentario": "Revoluciono el cine asiatico en Hollywood", "fecha": "2024-02-14"}
        ],
        "disponible": True,
        "metadata": {"duracion_minutos": 132, "idioma_original": "Coreano", "presupuesto": 11400000}
    },
    {
        "titulo": "Pulp Fiction",
        "año": 1994,
        "director": "Quentin Tarantino",
        "generos": ["Crimen", "Drama"],
        "rating": 8.9,
        "actores": [
            {"nombre": "John Travolta", "rol": "Vincent Vega"},
            {"nombre": "Samuel L. Jackson", "rol": "Jules Winnfield"}
        ],
        "reviews": [
            {"usuario": "TarantinoFan", "puntuacion": 10, 
             "comentario": "Dialogos inolvidables", "fecha": "2023-11-05"},
            {"usuario": "ClassicMovies", "puntuacion": 9, 
             "comentario": "Cambio el cine de los 90s", "fecha": "2024-03-01"}
        ],
        "disponible": True,
        "metadata": {"duracion_minutos": 154, "idioma_original": "Ingles", "presupuesto": 8000000}
    },
    {
        "titulo": "El Laberinto del Fauno",
        "año": 2006,
        "director": "Guillermo del Toro",
        "generos": ["Fantasia", "Drama", "Guerra"],
        "rating": 8.2,
        "actores": [
            {"nombre": "Ivana Baquero", "rol": "Ofelia"},
            {"nombre": "Sergi Lopez", "rol": "Capitan Vidal"}
        ],
        "reviews": [
            {"usuario": "FantasyWorld", "puntuacion": 9, 
             "comentario": "Magia oscura y hermosa", "fecha": "2023-07-22"}
        ],
        "disponible": True,
        "metadata": {"duracion_minutos": 118, "idioma_original": "Espanol", "presupuesto": 19000000}
    },
    {
        "titulo": "Interestelar",
        "año": 2014,
        "director": "Christopher Nolan",
        "generos": ["Ciencia Ficcion", "Drama", "Aventura"],
        "rating": 8.7,
        "actores": [
            {"nombre": "Matthew McConaughey", "rol": "Cooper"},
            {"nombre": "Anne Hathaway", "rol": "Brand"}
        ],
        "reviews": [
            {"usuario": "SpaceLover", "puntuacion": 10, 
             "comentario": "Epica espacial emotiva", "fecha": "2024-01-20"},
            {"usuario": "SciFiFan", "puntuacion": 8, 
             "comentario": "Visualmente impresionante", "fecha": "2023-12-15"}
        ],
        "disponible": True,
        "metadata": {"duracion_minutos": 169, "idioma_original": "Ingles", "presupuesto": 165000000}
    },
    {
        "titulo": "Roma",
        "año": 2018,
        "director": "Alfonso Cuaron",
        "generos": ["Drama"],
        "rating": 7.7,
        "actores": [
            {"nombre": "Yalitza Aparicio", "rol": "Cleo"},
            {"nombre": "Marina de Tavira", "rol": "Sofia"}
        ],
        "reviews": [
            {"usuario": "ArtHouse", "puntuacion": 8, 
             "comentario": "Poesia visual en blanco y negro", "fecha": "2023-09-10"}
        ],
        "disponible": True,
        "metadata": {"duracion_minutos": 135, "idioma_original": "Espanol", "presupuesto": 15000000}
    },
    {
        "titulo": "Matrix",
        "año": 1999,
        "director": "Lana Wachowski",
        "generos": ["Ciencia Ficcion", "Accion"],
        "rating": 8.7,
        "actores": [
            {"nombre": "Keanu Reeves", "rol": "Neo"},
            {"nombre": "Laurence Fishburne", "rol": "Morpheus"}
        ],
        "reviews": [
            {"usuario": "TechNerd", "puntuacion": 10, 
             "comentario": "Revoluciono los efectos especiales", "fecha": "2024-02-28"},
            {"usuario": "ActionFan", "puntuacion": 9, 
             "comentario": "Filosofia y accion perfectas", "fecha": "2023-06-18"}
        ],
        "disponible": True,
        "metadata": {"duracion_minutos": 136, "idioma_original": "Ingles", "presupuesto": 63000000}
    },
    {
        "titulo": "Coco",
        "año": 2017,
        "director": "Lee Unkrich",
        "generos": ["Animacion", "Fantasia", "Familia"],
        "rating": 8.4,
        "actores": [
            {"nombre": "Anthony Gonzalez", "rol": "Miguel"},
            {"nombre": "Gael Garcia Bernal", "rol": "Hector"}
        ],
        "reviews": [
            {"usuario": "PixarFan", "puntuacion": 10, 
             "comentario": "Emotiva celebracion de la cultura mexicana", "fecha": "2023-11-02"}
        ],
        "disponible": True,
        "metadata": {"duracion_minutos": 105, "idioma_original": "Ingles", "presupuesto": 175000000}
    },
    {
        "titulo": "El Secreto de sus Ojos",
        "año": 2009,
        "director": "Juan Jose Campanella",
        "generos": ["Drama", "Misterio", "Romance"],
        "rating": 8.2,
        "actores": [
            {"nombre": "Ricardo Darin", "rol": "Benjamin Exposito"},
            {"nombre": "Soledad Villamil", "rol": "Irene Menendez Hastings"}
        ],
        "reviews": [
            {"usuario": "CineArgentino", "puntuacion": 9, 
             "comentario": "La mejor pelicula argentina", "fecha": "2024-01-05"}
        ],
        "disponible": True,
        "metadata": {"duracion_minutos": 129, "idioma_original": "Espanol", "presupuesto": 2000000}
    },
    {
        "titulo": "Amelie",
        "año": 2001,
        "director": "Jean-Pierre Jeunet",
        "generos": ["Comedia", "Romance"],
        "rating": 8.3,
        "actores": [
            {"nombre": "Audrey Tautou", "rol": "Amelie Poulain"},
            {"nombre": "Mathieu Kassovitz", "rol": "Nino Quincampoix"}
        ],
        "reviews": [
            {"usuario": "FrenchCinema", "puntuacion": 9, 
             "comentario": "Encantadora y unica", "fecha": "2023-04-14"}
        ],
        "disponible": False,
        "metadata": {"duracion_minutos": 122, "idioma_original": "Frances", "presupuesto": 10000000}
    },
    {
        "titulo": "Ciudad de Dios",
        "año": 2002,
        "director": "Fernando Meirelles",
        "generos": ["Crimen", "Drama"],
        "rating": 8.6,
        "actores": [
            {"nombre": "Alexandre Rodrigues", "rol": "Buscape"},
            {"nombre": "Leandro Firmino", "rol": "Ze Pequeno"}
        ],
        "reviews": [
            {"usuario": "BrazilCinema", "puntuacion": 10, 
             "comentario": "Impactante y real", "fecha": "2023-08-30"}
        ],
        "disponible": True,
        "metadata": {"duracion_minutos": 130, "idioma_original": "Portugues", "presupuesto": 3300000}
    }
]


SCHEMA_VALIDATOR: Dict[str, Any] = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["titulo", "año", "director", "generos", "rating"],
        "properties": {
            "titulo": {
                "bsonType": "string",
                "description": "Titulo de la pelicula - requerido"
            },
            "año": {
                "bsonType": "int",
                "minimum": 1888,
                "maximum": 2030,
                "description": "Año de estreno (1888-2030)"
            },
            "director": {
                "bsonType": "string",
                "description": "Nombre del director - requerido"
            },
            "generos": {
                "bsonType": "array",
                "minItems": 1,
                "items": {"bsonType": "string"},
                "description": "Lista de generos (minimo 1)"
            },
            "rating": {
                "bsonType": "double",
                "minimum": 0,
                "maximum": 10,
                "description": "Rating de 0 a 10"
            },
            "actores": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["nombre", "rol"],
                    "properties": {
                        "nombre": {"bsonType": "string"},
                        "rol": {"bsonType": "string"}
                    }
                }
            },
            "reviews": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["usuario", "puntuacion", "comentario", "fecha"],
                    "properties": {
                        "usuario": {"bsonType": "string"},
                        "puntuacion": {"bsonType": "int", "minimum": 1, "maximum": 10},
                        "comentario": {"bsonType": "string"},
                        "fecha": {"bsonType": "string"}
                    }
                }
            },
            "disponible": {"bsonType": "bool"},
            "metadata": {
                "bsonType": "object",
                "properties": {
                    "duracion_minutos": {"bsonType": "int", "minimum": 1},
                    "idioma_original": {"bsonType": "string"},
                    "presupuesto": {"bsonType": "int", "minimum": 0}
                }
            }
        }
    }
}
