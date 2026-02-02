"""
Interfaz grafica web con Streamlit para el sistema de peliculas.
Ejecutar: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from database import DatabaseManager
from crud import CRUDOperations
from queries import QueryOperations


# Configuracion de pagina
st.set_page_config(
    page_title="Sistema de Peliculas",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f1f1f;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def inicializar_conexion():
    """Inicializa la conexion a MongoDB (cached)."""
    db_manager = DatabaseManager()
    if db_manager.conectar():
        db_manager.inicializar_datos()
        db_manager.crear_indices()
        db_manager.aplicar_validacion()
        return db_manager
    return None


def main():
    # Inicializar conexion
    db_manager = inicializar_conexion()
    
    if not db_manager:
        st.error("Error: No se pudo conectar a MongoDB")
        st.info("Verifica que MongoDB este ejecutandose en mongodb://mongodb_service:27017/")
        return
    
    crud = CRUDOperations(db_manager.collection)
    queries = QueryOperations(db_manager.collection)
    
    # Header
    st.markdown('<p class="main-header">Sistema de Gestion de Peliculas</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">MongoDB + Python | MD003 - La Salle</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Navegacion")
        pagina = st.radio(
            "Selecciona una seccion:",
            ["Dashboard", "Busquedas", "Consultas Avanzadas", "Agregaciones", "Gestionar Reviews", "Administrar"]
        )
    
    # Contenido segun pagina
    if pagina == "Dashboard":
        mostrar_dashboard(queries)
    elif pagina == "Busquedas":
        mostrar_busquedas(crud)
    elif pagina == "Consultas Avanzadas":
        mostrar_consultas_avanzadas(queries)
    elif pagina == "Agregaciones":
        mostrar_agregaciones(queries)
    elif pagina == "Gestionar Reviews":
        mostrar_gestion_reviews(crud)
    elif pagina == "Administrar":
        mostrar_administrar(crud, queries)


def mostrar_dashboard(queries: QueryOperations):
    """Muestra el dashboard principal con metricas."""
    
    stats = queries.estadisticas_generales()
    
    # Metricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Peliculas", stats['total_peliculas'])
    with col2:
        st.metric("Total Reviews", stats['total_reviews'])
    with col3:
        st.metric("Generos", stats['generos_unicos'])
    with col4:
        st.metric("Directores", stats['directores'])
    
    st.divider()
    
    # Top peliculas y Rating por genero
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 5 Peliculas")
        top = queries.top_peliculas(5)
        df_top = pd.DataFrame(top)
        if not df_top.empty:
            df_top = df_top[['titulo', 'director', 'año', 'rating', 'score_combinado']]
            df_top.columns = ['Titulo', 'Director', 'Año', 'Rating', 'Score']
            st.dataframe(df_top, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("Rating por Genero")
        rating_genero = queries.rating_promedio_por_genero()
        df_rating = pd.DataFrame(rating_genero)
        if not df_rating.empty:
            st.bar_chart(df_rating.set_index('genero')['rating_promedio'])
    
    st.divider()
    
    # Reporte por decada
    st.subheader("Peliculas por Decada")
    decadas = queries.reporte_por_decada()
    df_decadas = pd.DataFrame([{
        'Decada': d['decada'],
        'Cantidad': d['cantidad'],
        'Rating Promedio': d['rating_promedio'],
        'Presupuesto Promedio': f"${d['presupuesto_promedio']:,.0f}"
    } for d in decadas])
    
    if not df_decadas.empty:
        st.dataframe(df_decadas, use_container_width=True, hide_index=True)


def mostrar_busquedas(crud: CRUDOperations):
    """Muestra la seccion de busquedas."""
    
    st.subheader("Busqueda de Peliculas")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Por Titulo", "Por Genero", "Por Director", "Por Rating", "Texto Completo"
    ])
    
    with tab1:
        titulo = st.text_input("Buscar por titulo:", key="buscar_titulo")
        if titulo:
            resultados = crud.buscar_por_titulo(titulo)
            if resultados:
                df = pd.DataFrame(resultados)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No se encontraron resultados")
    
    with tab2:
        generos = ["Drama", "Accion", "Comedia", "Ciencia Ficcion", "Thriller", 
                   "Fantasia", "Romance", "Crimen", "Animacion", "Aventura", "Guerra", "Misterio", "Familia"]
        genero = st.selectbox("Selecciona un genero:", generos)
        if st.button("Buscar por genero", key="btn_genero"):
            resultados = crud.buscar_por_genero(genero)
            if resultados:
                df = pd.DataFrame(resultados)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No se encontraron peliculas de este genero")
    
    with tab3:
        director = st.text_input("Buscar por director:", key="buscar_director")
        if director:
            resultados = crud.buscar_por_director(director)
            if resultados:
                df = pd.DataFrame(resultados)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No se encontraron resultados")
    
    with tab4:
        rating_min = st.slider("Rating minimo:", 0.0, 10.0, 8.0, 0.1)
        if st.button("Buscar por rating", key="btn_rating"):
            resultados = crud.buscar_por_rating_minimo(rating_min)
            if resultados:
                df = pd.DataFrame(resultados)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No se encontraron peliculas")
    
    with tab5:
        texto = st.text_input("Busqueda de texto completo:", key="texto_completo")
        if texto:
            resultados = crud.busqueda_texto_completo(texto)
            if resultados:
                df = pd.DataFrame(resultados)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No se encontraron resultados")


def mostrar_consultas_avanzadas(queries: QueryOperations):
    """Muestra consultas avanzadas."""
    
    st.subheader("Consultas Avanzadas")
    
    tab1, tab2, tab3 = st.tabs(["Rango de Años", "Top Directores", "Buscar en Reviews"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            año_inicio = st.number_input("Año inicio:", 1990, 2025, 2000)
        with col2:
            año_fin = st.number_input("Año fin:", 1990, 2025, 2020)
        
        if st.button("Buscar por rango", key="btn_rango"):
            resultados = queries.peliculas_por_rango_años(año_inicio, año_fin)
            if resultados:
                df = pd.DataFrame(resultados)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No se encontraron peliculas en este rango")
    
    with tab2:
        limite = st.slider("Cantidad de directores:", 3, 10, 5)
        directores = queries.directores_con_mas_peliculas(limite)
        
        for d in directores:
            with st.expander(f"{d['director']} - {d['cantidad']} peliculas"):
                st.write(f"**Rating promedio:** {d['rating_promedio']}")
                st.write(f"**Peliculas:** {', '.join(d['peliculas'])}")
    
    with tab3:
        palabra = st.text_input("Palabra clave en titulo o reviews:")
        if palabra:
            from crud import CRUDOperations
            db_manager = inicializar_conexion()
            crud = CRUDOperations(db_manager.collection)
            resultados = crud.buscar_por_palabra_clave(palabra)
            if resultados:
                for r in resultados:
                    st.write(f"**{r['titulo']}** (Rating: {r['rating']})")
                    if 'reviews' in r:
                        for review in r['reviews']:
                            if palabra.lower() in review.get('comentario', '').lower():
                                st.caption(f"Review: {review['comentario']}")
            else:
                st.info("No se encontraron resultados")


def mostrar_agregaciones(queries: QueryOperations):
    """Muestra resultados de agregaciones."""
    
    st.subheader("Agregaciones y Estadisticas")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Estadisticas por Genero", "Rating por Genero", "Analisis Reviews", "Reporte Decadas"
    ])
    
    with tab1:
        st.write("Estadisticas completas por genero")
        stats = queries.estadisticas_por_genero()
        df = pd.DataFrame(stats)
        if not df.empty:
            df.columns = ['Genero', 'Cantidad', 'Rating Prom', 'Rating Max', 'Rating Min', 'Presupuesto Total', 'Duracion Prom']
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab2:
        rating_genero = queries.rating_promedio_por_genero()
        df = pd.DataFrame(rating_genero)
        if not df.empty:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.bar_chart(df.set_index('genero')['rating_promedio'])
            with col2:
                st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.write("Analisis de reviews por pelicula")
        reviews = queries.analisis_reviews()
        df = pd.DataFrame(reviews)
        if not df.empty:
            df.columns = ['Titulo', 'Rating', 'Num Reviews', 'Promedio', 'Max', 'Min']
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab4:
        decadas = queries.reporte_por_decada()
        for d in decadas:
            with st.expander(f"{d['decada']} - {d['cantidad']} peliculas"):
                st.write(f"**Rating promedio:** {d['rating_promedio']}")
                st.write(f"**Presupuesto promedio:** ${d['presupuesto_promedio']:,.0f}")
                st.write("**Peliculas:**")
                for p in sorted(d['peliculas'], key=lambda x: x['año']):
                    st.write(f"- {p['titulo']} ({p['año']}) - Rating: {p['rating']}")


def mostrar_gestion_reviews(crud: CRUDOperations):
    """Muestra seccion de gestion de reviews."""
    
    st.subheader("Gestionar Reviews")
    
    tab1, tab2, tab3 = st.tabs(["Añadir Review", "Eliminar Review", "Actualizar Rating"])
    
    with tab1:
        st.write("Añadir una nueva review")
        
        # Obtener lista de peliculas
        peliculas = crud.obtener_todas()
        titulos = [p['titulo'] for p in peliculas]
        
        titulo = st.selectbox("Selecciona pelicula:", titulos, key="add_review_titulo")
        usuario = st.text_input("Tu nombre de usuario:", key="add_review_user")
        puntuacion = st.slider("Puntuacion:", 1, 10, 8, key="add_review_score")
        comentario = st.text_area("Comentario:", key="add_review_comment")
        
        if st.button("Añadir Review", type="primary"):
            if usuario and comentario:
                if crud.añadir_review(titulo, usuario, puntuacion, comentario):
                    st.success(f"Review añadida a '{titulo}'")
                else:
                    st.error("Error al añadir review")
            else:
                st.warning("Completa todos los campos")
    
    with tab2:
        st.write("Eliminar una review existente")
        
        titulo_del = st.selectbox("Selecciona pelicula:", titulos, key="del_review_titulo")
        usuario_del = st.text_input("Nombre del usuario:", key="del_review_user")
        
        if st.button("Eliminar Review", type="secondary"):
            if usuario_del:
                if crud.eliminar_review(titulo_del, usuario_del):
                    st.success(f"Review de '{usuario_del}' eliminada")
                else:
                    st.error("Review no encontrada")
            else:
                st.warning("Ingresa el nombre del usuario")
    
    with tab3:
        st.write("Actualizar rating de una pelicula")
        
        titulo_upd = st.selectbox("Selecciona pelicula:", titulos, key="upd_rating_titulo")
        nuevo_rating = st.slider("Nuevo rating:", 0.0, 10.0, 8.0, 0.1, key="upd_rating_value")
        
        if st.button("Actualizar Rating", type="primary"):
            if crud.actualizar_rating(titulo_upd, nuevo_rating):
                st.success(f"Rating de '{titulo_upd}' actualizado a {nuevo_rating}")
            else:
                st.error("Error al actualizar")


def mostrar_administrar(crud: CRUDOperations, queries: QueryOperations):
    """Muestra seccion de administracion."""
    
    st.subheader("Administracion del Sistema")
    
    tab1, tab2, tab3 = st.tabs(["Ver Todas", "Indices", "Estadisticas"])
    
    with tab1:
        st.write("Listado completo de peliculas")
        peliculas = crud.obtener_todas()
        df = pd.DataFrame(peliculas)
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.write("Indices de la coleccion")
        db_manager = inicializar_conexion()
        indices = db_manager.listar_indices()
        for idx in indices:
            st.code(f"{idx['name']}: {idx['key']}")
    
    with tab3:
        stats = queries.estadisticas_generales()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Peliculas", stats['total_peliculas'])
            st.metric("Total Reviews", stats['total_reviews'])
        with col2:
            st.metric("Generos Unicos", stats['generos_unicos'])
            st.metric("Directores", stats['directores'])


if __name__ == "__main__":
    main()
