import streamlit as st
from components.estilo import estilo_add
from components.Contenedor import mostrar_tarjeta_izquierda, mostrar_entrada_ruts, mostrar_columna_acciones
from components.rut_parser import limpiar_ruts
from components.simulador import procesar_ruts
from .state import inicializar_session_state
from .ellipses import mostrar_datos

def mostrar_interfaz():
    st.set_page_config(page_title="Simulador de Trayectorias Dron - RUT", layout="wide")
    estilo_add()
    inicializar_session_state()

    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='margin-bottom: 0; color: white;'>STD-RUT</h1>
        <p style='font-size: 18px; color: gray;'>Simulador de Trayectorias de Drones a partir del RUT</p>
    </div>
    """, unsafe_allow_html=True)

    col_izq, col_der = st.columns(2)

    with col_izq:
        mostrar_tarjeta_izquierda()

    with col_der:
        ruts_input = mostrar_entrada_ruts()
        ruts_limpios = limpiar_ruts(ruts_input)
        
        if mostrar_columna_acciones(ruts_limpios):
            elipses, errores = procesar_ruts(ruts_limpios)
            
            if errores:
                st.error("⚠️ Algunos RUTs no pudieron procesarse:")
                for err in errores:
                    st.markdown(f"- {err}")
                st.session_state.elipses_generadas = None
                st.session_state.ruts_procesados = None
                st.session_state.mostrar_datos = False
            else:
                st.success("✅ Elipses generadas correctamente.")
                st.session_state.elipses_generadas = elipses
                st.session_state.ruts_procesados = ruts_limpios
                st.session_state.mostrar_datos = True

    if st.session_state.mostrar_datos and st.session_state.elipses_generadas:
        mostrar_datos(st.session_state.elipses_generadas, st.session_state.ruts_procesados)