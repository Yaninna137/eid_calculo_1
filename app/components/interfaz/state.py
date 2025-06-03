import streamlit as st

def inicializar_session_state():
    """Inicializa las variables de session_state si no existen"""
    if 'elipses_generadas' not in st.session_state:
        st.session_state.elipses_generadas = None
    if 'ruts_procesados' not in st.session_state:
        st.session_state.ruts_procesados = None
    if 'mostrar_datos' not in st.session_state:
        st.session_state.mostrar_datos = False
    if 'mostrar_resolucion' not in st.session_state:
        st.session_state.mostrar_resolucion = False
    if 'mostrar_trayectorias' not in st.session_state:
        st.session_state.mostrar_trayectorias = False
    if 'elipses_resueltas' not in st.session_state:
        st.session_state.elipses_resueltas = None
    if 'resultado_resolucion' not in st.session_state:
        st.session_state.resultado_resolucion = None
    if 'trayectorias_generadas' not in st.session_state:
        st.session_state.trayectorias_generadas = None