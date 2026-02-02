"""
Sistema de Gestion de Peliculas con MongoDB
============================================
Autor: Paulina Peralta y Katherine Soto
Asignatura: MD003 - Estructuras de datos y su almacenamiento
Universidad: La Salle - Ramon Llull

Punto de entrada principal del sistema.
"""

from database import DatabaseManager
from crud import CRUDOperations
from queries import QueryOperations
from cli import CLI
from config import logger


def demo_crud(crud: CRUDOperations) -> None:
    """Demuestra operaciones CRUD."""
    print("\n" + "=" * 60)
    print("DEMOSTRACION: Operaciones CRUD")
    print("=" * 60)
    
    # Actualizar rating
    crud.actualizar_rating("Inception", 9.0)
    crud.actualizar_rating("Roma", 8.0)
    
    # Añadir y eliminar review
    crud.añadir_review("Matrix", "TestUser", 9, "Excelente pelicula de ciencia ficcion")
    crud.eliminar_review("Matrix", "TestUser")
    
    # Busquedas
    print("\n--- Busqueda por titulo 'Coco' ---")
    for p in crud.buscar_por_titulo('Coco'):
        print(f"  {p['titulo']} ({p['año']})")
    
    print("\n--- Busqueda por genero 'Drama' (primeros 3) ---")
    for p in crud.buscar_por_genero("Drama")[:3]:
        print(f"  {p['titulo']} ({p['año']})")
    
    print("\n--- Busqueda por director 'Nolan' ---")
    for p in crud.buscar_por_director("Nolan"):
        print(f"  {p['titulo']} - Rating: {p['rating']}")
    
    print("\n--- Peliculas con rating >= 8.5 ---")
    for p in crud.buscar_por_rating_minimo(8.5):
        print(f"  {p['titulo']} - Rating: {p['rating']}")


def demo_consultas(queries: QueryOperations) -> None:
    """Demuestra consultas avanzadas."""
    print("\n" + "=" * 60)
    print("DEMOSTRACION: Consultas Avanzadas")
    print("=" * 60)
    
    print("\n--- Peliculas 2000-2010 ---")
    for p in queries.peliculas_por_rango_años(2000, 2010):
        print(f"  {p['año']} - {p['titulo']} (Dir: {p['director']})")
    
    print("\n--- Rating promedio por genero (top 5) ---")
    for g in queries.rating_promedio_por_genero()[:5]:
        print(f"  {g['genero']}: {g['rating_promedio']} ({g['cantidad']} peliculas)")
    
    print("\n--- Directores con mas peliculas ---")
    for d in queries.directores_con_mas_peliculas(3):
        print(f"  {d['director']}: {d['cantidad']} peliculas")


def demo_agregaciones(queries: QueryOperations) -> None:
    """Demuestra agregaciones."""
    print("\n" + "=" * 60)
    print("DEMOSTRACION: Agregaciones")
    print("=" * 60)
    
    print("\n--- Top 5 peliculas ---")
    for i, p in enumerate(queries.top_peliculas(5), 1):
        print(f"  {i}. {p['titulo']} - Score: {p['score_combinado']}")
    
    print("\n--- Analisis de reviews ---")
    for p in queries.analisis_reviews()[:5]:
        print(f"  {p['titulo']}: {p['num_reviews']} reviews (prom: {p['promedio_puntuacion']})")
    
    print("\n--- Reporte por decada ---")
    for d in queries.reporte_por_decada():
        print(f"  {d['decada']}: {d['cantidad']} peliculas (rating prom: {d['rating_promedio']})")


def demo_bonus(db_manager: DatabaseManager, crud: CRUDOperations) -> None:
    """Demuestra funcionalidades bonus."""
    print("\n" + "=" * 60)
    print("DEMOSTRACION: Funcionalidades Bonus")
    print("=" * 60)
    
    # Indices
    print("\n--- Indices creados ---")
    for index in db_manager.listar_indices():
        print(f"  {index['name']}: {index['key']}")
    
    # Busqueda de texto
    print("\n--- Busqueda de texto completo: 'Nolan ciencia' ---")
    for p in crud.busqueda_texto_completo("Nolan ciencia"):
        print(f"  {p['titulo']} (Dir: {p['director']}) - Score: {p.get('score', 0):.2f}")


def imprimir_resumen() -> None:
    """Imprime el resumen del sistema implementado."""
    print("\n" + "=" * 60)
    print("RESUMEN DEL SISTEMA IMPLEMENTADO")
    print("=" * 60)
    print("""
CRUD Operations (30 pts)
   - 11 peliculas insertadas con estructura completa
   - actualizar_rating(), añadir_review(), eliminar_review()
   - Busquedas por titulo, genero, director, rating

Consultas Avanzadas (30 pts)
   - peliculas_por_rango_años()
   - rating_promedio_por_genero()
   - directores_con_mas_peliculas()
   - buscar_por_palabra_clave()

Agregaciones (30 pts)
   - estadisticas_por_genero()
   - top_peliculas()
   - analisis_reviews()
   - reporte_por_decada()

Bonus (10 pts extra)
   - Busqueda de texto completo (indice TEXT)
   - Indices para optimizacion
   - Interfaz CLI interactiva
   - Validacion de esquema JSON
    """)


def main():
    """Funcion principal del programa."""
    print("\n" + "=" * 60)
    print("SISTEMA DE GESTION DE PELICULAS CON MONGODB")
    print("Autor: Paulina Peralta | MD003 - La Salle")
    print("=" * 60)
    
    # Inicializar gestor de base de datos
    db_manager = DatabaseManager()
    
    if not db_manager.conectar():
        logger.error("No se pudo conectar a MongoDB")
        return
    
    try:
        # Configuracion inicial
        db_manager.inicializar_datos()
        db_manager.crear_indices()
        db_manager.aplicar_validacion()
        
        # Crear operaciones
        crud = CRUDOperations(db_manager.collection)
        queries = QueryOperations(db_manager.collection)
        
        # Ejecutar demostraciones
        demo_crud(crud)
        demo_consultas(queries)
        demo_agregaciones(queries)
        demo_bonus(db_manager, crud)
        
        # Resumen
        imprimir_resumen()
        
        # Preguntar si ejecutar CLI
        respuesta = input("\nDesea ejecutar el menu interactivo? (s/n): ").strip().lower()
        if respuesta == 's':
            cli = CLI(crud, queries)
            cli.ejecutar()
    
    finally:
        db_manager.desconectar()


if __name__ == "__main__":
    main()
