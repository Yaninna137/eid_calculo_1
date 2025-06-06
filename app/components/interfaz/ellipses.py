import streamlit as st
from core.Items_ellipse import ElipseVisual
from core.Graph_ellipse import grafico_2d_simple
from components.Contenedor import encabezado_html
from .analysis import mostrar_analisis_colisiones, mostrar_resolucion_colisiones
def Mostrar_datos_encapsulado_elipse(elipse, rut):
    try:
        e_canonica = elipse.ecuacion_canonica()
        e_general = elipse.ecuacion_general()
        datos = ElipseVisual(**elipse.__dict__)
        elementos = datos.obtener_elementos()

        if not isinstance(elementos, dict):
            st.error("No se puede calcular la elipse porque 'a' es menor que 'b'.")
            return

        focos = elementos.get('focos', [])
        if (
            isinstance(focos, (list, tuple)) and len(focos) == 2
            and all(isinstance(f, tuple) and len(f) == 2 for f in focos)
        ):
            f1, f2 = focos
            f1_str = f"({f1[0]:.2f}, {f1[1]:.2f})"
            f2_str = f"({f2[0]:.2f}, {f2[1]:.2f})"
        else:
            f1_str = f2_str = "(no disponible)"

        st.markdown(f'''
            <h4 style="color: #ff6f61" >Elipse del dron-RUT ({rut})</h4>
            <p>Con el Rut Extrajimos los sig. datos y con ellos obtenemos nuevos datos.</p>
            <p>h = {elipse.h} ; k = {elipse.k} ; a = {elipse.a} ; b = {elipse.b}</p>
            <div class="block">
                <div class="row-flex">
                    <div class="scroll-inner">
                        <ul>
                            <li><b>C(h,k)</b> = C({elipse.h}, {elipse.k})</li>
                            <li><b>Focos</b> = F1: {f1_str} ; F2: {f2_str}</li>
                            <li><b>Vertices P.</b> = V1{elementos['vertices_principales'][0]} ; V2{elementos['vertices_principales'][1]}</li>
                            <li><b>Vertices A.</b> = B1{elementos['vertices_secundarios'][0]} ; B2{elementos['vertices_secundarios'][1]}</li>
                            <li><b>Distancia focal = √a² - b²</b> = {elementos['c']}</li>
                            <li><b>Eje mayor 2a</b> = {elementos['eje_mayor']}</li>
                            <li><b>Eje menor 2b</b> = {elementos['eje_menor']}</li>
                            <li><b>Eje focal 2c</b> = {elementos['eje_focal']}</li>
                            <li><b>Eje focal paralelo al eje {elementos['orientacion']}</b></li>
                        </ul>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

        st.markdown("Ec. Canónica:")
        st.latex(e_canonica)

        st.markdown("Ec. General:")
        st.latex(e_general)

    except Exception as e:
        st.error(f"Error al procesar los datos de la elipse: {e}")

def mostrar_datos(elipses, ruts_limpios):    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs([
        "Datos de elipses", 
        "Gráficos y Colisiones", 
        "Resolución de Colisiones",
    ])
    
    with tab1:
        st.markdown(encabezado_html("Datos de las elipses", "En esta sección encontrarás los detalles técnicos de cada elipse generada, incluyendo vértices, focos y parámetros calculados a partir del RUT del dron."), 
                    unsafe_allow_html=True)
        
        for idx, elipse in enumerate(elipses):
            col1, col2 = st.columns([2, 3])

            with col2:
                st.markdown('<div class="scroll-box">', unsafe_allow_html=True)
                try:
                    Mostrar_datos_encapsulado_elipse(elipse, ruts_limpios[idx])
                except Exception as e:
                    st.error(f"Error al mostrar datos: {e}")
                finally:
                    st.markdown('</div>', unsafe_allow_html=True)

            with col1:
                img_base64 = grafico_2d_simple(elipse)
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center;">
                        <div style="text-align: center; margin-top: 50px;">
                            <img src="data:image/png;base64,{img_base64}" width="400" height="400" />
                            <span style="font-size: 18px; color: gray; display: block; margin-top: 8px;">Gráfica 2D</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True) 
    
    with tab2:
        mostrar_analisis_colisiones(elipses, ruts_limpios)
    with tab3:
        mostrar_resolucion_colisiones(elipses, ruts_limpios)