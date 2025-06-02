import streamlit as st
from .rut_parser import generar_ruts_validos, limpiar_ruts, es_rut_valido


def mostrar_tarjeta_izquierda():
    # Tarjeta izquierda con borde animado de colores cálidos
    st.markdown("""
        <div style="
            padding: 2px;
            border-radius: 12px;
            position: relative;
            background: linear-gradient(270deg, #ff4b4b, #ffa500, #ffd700, #ffa500, #ff4b4b);
            background-size: 1000% 1000%;
            animation: animateBorder 8s linear infinite;
        ">
            <div style="
                border-radius: 10px;
                background-color: #0F111A;
                padding: 20px;
                color: white;
                font-size: 14px;
                line-height: 1.6;
            ">
                <h4 style="margin-top: 0; color: #FF4B4B;">STDR</h4>
                <p>La app STDR permite simular trayectorias elipsoidales para drones. Incluye:</p>
                <ul>
                    <li>Generación de elipses a partir del RUT</li>
                    <li>Visualización 2D y 3D</li>
                    <li>Detección de colisiones</li>
                    <li>Herramientas de análisis y verificación</li>
                </ul>
            </div>
        </div>

        <style>
        @keyframes animateBorder {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
        </style>
        """, unsafe_allow_html=True)


def mostrar_entrada_ruts():
    # Entrada y botones a la derecha
    st.markdown("""
    <style>
    .css-1kyxreq.effi0qh3 {
        display: none;
    }
    textarea {
        background-color: #1b1f2a !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid #444 !important;
    }
    </style>
    <p style="color: #ff6f61; font-weight: bold; margin-bottom: 0.2em;">Ingresar RUTs:</p>
    """, unsafe_allow_html=True)

    ruts_input = st.text_area(
        "",
        value=st.session_state.get("ruts_input", ""),
        height=120,
        placeholder="Ej: 12.345.678-5\n9.876.543-2"
    )

    return ruts_input


def mostrar_botones():
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 2])
    with col_btn2:
        if st.button("RUT aleatorio"):
            ruts_generados = generar_ruts_validos(3)
            st.session_state.ruts_input = "\n".join(ruts_generados)
            st.rerun()
    with col_btn3:
        return st.button("Simular elipse")


def mostrar_columna_acciones(ruts_limpios):
    return mostrar_botones() and bool(ruts_limpios)


# 💡 Agrega esta función para validar los RUTs ingresados
def obtener_ruts_validos_y_invalidos(texto_input):
    ruts_limpios = limpiar_ruts(texto_input)
    ruts_validos = [rut for rut in ruts_limpios if es_rut_valido(rut)]
    ruts_invalidos = [rut for rut in ruts_limpios if not es_rut_valido(rut)]
    return ruts_validos, ruts_invalidos


# ✅ Lógica de integración completa
def ejecutar_interfaz():
    mostrar_tarjeta_izquierda()
    texto_ruts = mostrar_entrada_ruts()
    ruts_validos, ruts_invalidos = obtener_ruts_validos_y_invalidos(texto_ruts)

    if ruts_invalidos:
        st.warning(f"RUTs inválidos detectados: {', '.join(ruts_invalidos)}")

    if mostrar_botones() and bool(ruts_validos):
        st.success(f"Simulando elipses para: {', '.join(ruts_validos)}")
