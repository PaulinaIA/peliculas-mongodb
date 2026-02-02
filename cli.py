"""
Interfaz de linea de comandos para el sistema de peliculas.
"""

from pymongo.errors import PyMongoError

from crud import CRUDOperations
from queries import QueryOperations


MENU_PRINCIPAL = """
+-------------------------------------------------------------------+
|       SISTEMA DE GESTION DE PELICULAS - MongoDB                   |
+-------------------------------------------------------------------+
|  1.  Listar todas las peliculas                                   |
|  2.  Buscar pelicula por titulo                                   |
|  3.  Buscar por genero                                            |
|  4.  Buscar por director                                          |
|  5.  Buscar por rating minimo                                     |
|  6.  Buscar peliculas por rango de años                           |
|  7.  Ver top 5 peliculas                                          |
|  8.  Ver estadisticas por genero                                  |
|  9.  Ver rating promedio por genero                               |
|  10. Ver directores con mas peliculas                             |
|  11. Ver analisis de reviews                                      |
|  12. Ver reporte por decada                                       |
|  13. Añadir nueva review                                          |
|  14. Actualizar rating de pelicula                                |
|  15. Eliminar review                                              |
|  16. Busqueda de texto completo                                   |
|  17. Ver estadisticas generales                                   |
|  0.  Salir                                                        |
+-------------------------------------------------------------------+
"""


class CLI:
    """
    Interfaz de linea de comandos interactiva.
    """
    
    def __init__(self, crud: CRUDOperations, queries: QueryOperations):
        """
        Inicializa la CLI con las operaciones disponibles.
        
        Args:
            crud: Operaciones CRUD
            queries: Operaciones de consulta
        """
        self.crud = crud
        self.queries = queries
    
    def ejecutar(self) -> None:
        """Ejecuta el bucle principal del menu."""
        while True:
            print(MENU_PRINCIPAL)
            opcion = input("    Seleccione una opcion: ").strip()
            
            try:
                if opcion == "0":
                    print("\n    Hasta luego!")
                    break
                
                self._procesar_opcion(opcion)
                
            except ValueError as e:
                print(f"    Error de entrada: {e}")
            except PyMongoError as e:
                print(f"    Error de base de datos: {e}")
            
            input("\n    Presione Enter para continuar...")
    
    def _procesar_opcion(self, opcion: str) -> None:
        """Procesa la opcion seleccionada."""
        
        if opcion == "1":
            self._listar_todas()
        elif opcion == "2":
            self._buscar_por_titulo()
        elif opcion == "3":
            self._buscar_por_genero()
        elif opcion == "4":
            self._buscar_por_director()
        elif opcion == "5":
            self._buscar_por_rating()
        elif opcion == "6":
            self._buscar_por_rango_años()
        elif opcion == "7":
            self._ver_top_peliculas()
        elif opcion == "8":
            self._ver_estadisticas_genero()
        elif opcion == "9":
            self._ver_rating_promedio_genero()
        elif opcion == "10":
            self._ver_top_directores()
        elif opcion == "11":
            self._ver_analisis_reviews()
        elif opcion == "12":
            self._ver_reporte_decada()
        elif opcion == "13":
            self._añadir_review()
        elif opcion == "14":
            self._actualizar_rating()
        elif opcion == "15":
            self._eliminar_review()
        elif opcion == "16":
            self._busqueda_texto()
        elif opcion == "17":
            self._ver_estadisticas_generales()
        else:
            print("    Opcion no valida")
    
    def _listar_todas(self) -> None:
        """Lista todas las peliculas."""
        print("\n    === Todas las Peliculas ===")
        for p in self.crud.obtener_todas():
            print(f"      {p['rating']} - {p['titulo']} ({p['año']})")
    
    def _buscar_por_titulo(self) -> None:
        """Busca peliculas por titulo."""
        titulo = input("    Titulo a buscar: ")
        print(f"\n    === Resultados para '{titulo}' ===")
        resultados = self.crud.buscar_por_titulo(titulo)
        if resultados:
            for p in resultados:
                print(f"      {p['titulo']} ({p['año']}) - Dir: {p['director']} Rating: {p['rating']}")
        else:
            print("      No se encontraron resultados")
    
    def _buscar_por_genero(self) -> None:
        """Busca peliculas por genero."""
        genero = input("    Genero: ")
        print(f"\n    === Peliculas de '{genero}' ===")
        resultados = self.crud.buscar_por_genero(genero)
        if resultados:
            for p in resultados:
                print(f"      {p['titulo']} ({p['año']}) Rating: {p['rating']}")
        else:
            print("      No se encontraron resultados")
    
    def _buscar_por_director(self) -> None:
        """Busca peliculas por director."""
        director = input("    Director: ")
        print(f"\n    === Peliculas de '{director}' ===")
        resultados = self.crud.buscar_por_director(director)
        if resultados:
            for p in resultados:
                print(f"      {p['titulo']} ({p['año']}) Rating: {p['rating']}")
        else:
            print("      No se encontraron resultados")
    
    def _buscar_por_rating(self) -> None:
        """Busca peliculas por rating minimo."""
        rating = float(input("    Rating minimo (0-10): "))
        print(f"\n    === Peliculas con rating >= {rating} ===")
        for p in self.crud.buscar_por_rating_minimo(rating):
            print(f"      {p['rating']} - {p['titulo']}")
    
    def _buscar_por_rango_años(self) -> None:
        """Busca peliculas por rango de años."""
        año_inicio = int(input("    Año inicio: "))
        año_fin = int(input("    Año fin: "))
        print(f"\n    === Peliculas {año_inicio}-{año_fin} ===")
        for p in self.queries.peliculas_por_rango_años(año_inicio, año_fin):
            print(f"      {p['año']} - {p['titulo']} (Dir: {p['director']})")
    
    def _ver_top_peliculas(self) -> None:
        """Muestra las top 5 peliculas."""
        print("\n    === Top 5 Peliculas ===")
        for i, p in enumerate(self.queries.top_peliculas(5), 1):
            print(f"      {i}. {p['titulo']} - Score: {p['score_combinado']}")
            print(f"         Director: {p['director']} | Rating: {p['rating']} | Reviews: {p['promedio_reviews']}")
    
    def _ver_estadisticas_genero(self) -> None:
        """Muestra estadisticas por genero."""
        print("\n    === Estadisticas por Genero ===")
        for e in self.queries.estadisticas_por_genero():
            print(f"\n      {e['genero']}")
            print(f"         Peliculas: {e['cantidad']} | Rating: {e['rating_min']}-{e['rating_max']} (prom: {e['rating_promedio']})")
            print(f"         Duracion promedio: {e['duracion_promedio']} min | Presupuesto total: ${e['presupuesto_total']:,}")
    
    def _ver_rating_promedio_genero(self) -> None:
        """Muestra rating promedio por genero."""
        print("\n    === Rating Promedio por Genero ===")
        for g in self.queries.rating_promedio_por_genero():
            print(f"      {g['genero']}: {g['rating_promedio']} ({g['cantidad']} peliculas)")
    
    def _ver_top_directores(self) -> None:
        """Muestra los directores con mas peliculas."""
        print("\n    === Top Directores ===")
        for d in self.queries.directores_con_mas_peliculas():
            print(f"      {d['director']}: {d['cantidad']} peliculas (rating prom: {d['rating_promedio']})")
            print(f"         Peliculas: {', '.join(d['peliculas'])}")
    
    def _ver_analisis_reviews(self) -> None:
        """Muestra analisis de reviews."""
        print("\n    === Analisis de Reviews ===")
        print(f"      {'Pelicula':<30} {'Reviews':>8} {'Prom':>6} {'Min':>5} {'Max':>5}")
        print("      " + "-" * 60)
        for p in self.queries.analisis_reviews():
            print(f"      {p['titulo']:<30} {p['num_reviews']:>8} {p['promedio_puntuacion']:>6} {p['min_puntuacion']:>5} {p['max_puntuacion']:>5}")
    
    def _ver_reporte_decada(self) -> None:
        """Muestra reporte por decada."""
        print("\n    === Reporte por Decada ===")
        for d in self.queries.reporte_por_decada():
            print(f"\n      {d['decada']}")
            print(f"         Total: {d['cantidad']} peliculas | Rating promedio: {d['rating_promedio']}")
            print(f"         Presupuesto promedio: ${d['presupuesto_promedio']:,.0f}")
            print("         Peliculas:")
            for p in sorted(d['peliculas'], key=lambda x: x['año']):
                print(f"           - {p['titulo']} ({p['año']}) {p['rating']}")
    
    def _añadir_review(self) -> None:
        """Añade una nueva review."""
        titulo = input("    Titulo de la pelicula: ")
        usuario = input("    Tu nombre de usuario: ")
        puntuacion = int(input("    Puntuacion (1-10): "))
        comentario = input("    Tu comentario: ")
        self.crud.añadir_review(titulo, usuario, puntuacion, comentario)
    
    def _actualizar_rating(self) -> None:
        """Actualiza el rating de una pelicula."""
        titulo = input("    Titulo de la pelicula: ")
        nuevo_rating = float(input("    Nuevo rating (0-10): "))
        self.crud.actualizar_rating(titulo, nuevo_rating)
    
    def _eliminar_review(self) -> None:
        """Elimina una review."""
        titulo = input("    Titulo de la pelicula: ")
        usuario = input("    Usuario de la review a eliminar: ")
        self.crud.eliminar_review(titulo, usuario)
    
    def _busqueda_texto(self) -> None:
        """Realiza busqueda de texto completo."""
        texto = input("    Texto a buscar: ")
        print(f"\n    === Busqueda de texto completo: '{texto}' ===")
        resultados = self.crud.busqueda_texto_completo(texto)
        if resultados:
            for p in resultados:
                print(f"      {p['titulo']} (Dir: {p['director']}) {p['rating']} - Score: {p.get('score', 0):.2f}")
        else:
            print("      No se encontraron resultados")
    
    def _ver_estadisticas_generales(self) -> None:
        """Muestra estadisticas generales."""
        stats = self.queries.estadisticas_generales()
        print("\n    === Estadisticas Generales ===")
        print(f"      Total peliculas: {stats['total_peliculas']}")
        print(f"      Total reviews: {stats['total_reviews']}")
        print(f"      Generos unicos: {stats['generos_unicos']}")
        print(f"      Directores: {stats['directores']}")
