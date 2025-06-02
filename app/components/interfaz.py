# components/interfaz.py
import streamlit as st

from components.estilo import estilo_add
from components.rut_parser import limpiar_ruts
from components.Contenedor import mostrar_tarjeta_izquierda, mostrar_entrada_ruts, mostrar_columna_acciones
from components.simulador import procesar_ruts, analizar_colisiones_detallado
from core.Graph_ellipse import Grafico_3D_multiple, grafico_2d_simple, grafico_2d_interactivo
from core.Items_ellipse import ElipseVisual
from core.collision.CollisionAnalysis import tipo_colision, analizar_colision_detallada # Importamos las nuevas funciones

def encabezado_html(titulo: str, descripcion: str):
    return f"""
    <div style='background-color: #1b1f2a; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
        <h2 style='margin-bottom: 5px; color: white; text-align: center;'>{titulo}</h2>
        <p style='font-size: 18px; color: gray; text-align: center;'>{descripcion}</p>
    </div>
    """

def mostrar_interfaz():
    st.set_page_config(page_title="Simulador de Trayectorias Dron - RUT", layout="wide")
    estilo_add()

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
        mostrar = False

        if mostrar_columna_acciones(ruts_limpios):
            elipses, errores = procesar_ruts(ruts_limpios)
            
            if errores:
                st.error("⚠️ Algunos RUTs no pudieron procesarse:")
                for err in errores:
                    st.markdown(f"- {err}")
            else:
                st.success("✅ Elipses generadas correctamente.")
                mostrar = True

    if mostrar:
        mostrar_datos(elipses, ruts_limpios)


def mostrar_datos(elipses, ruts_limpios):
    st.markdown("---")
    tab1, tab2 = st.tabs(["Datos de elipses", "Gráficos y Colisiones"])
    
    with tab1:
        st.markdown(encabezado_html("Datos de las elipses", "En esta sección encontrarás los detalles técnicos de cada elipse generada, incluyendo vértices, focos y parámetros calculados a partir del RUT del dron."), 
                    unsafe_allow_html=True)
        
        for idx, elipse in enumerate(elipses):
            col1, col2 = st.columns([2, 3])

            with col2:
                st.markdown('<div class="scroll-box">', unsafe_allow_html=True)
                Mostrar_datos_encapsulado_elipse(elipse, ruts_limpios[idx])
                st.markdown('</div>', unsafe_allow_html=True)

            with col1:
                img_base64 = grafico_2d_simple(elipse)
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <img src="data:image/png;base64,{img_base64}" width="400", height=400"/>
                        <span style='font-size: 18px; color: gray; display: block; margin-top: 8px;'>Gráfica 2D</span>
                    </div>
                    """, unsafe_allow_html=True) 
    
    with tab2:
        st.markdown(encabezado_html("Comparación visual y detección de colisiones", "Sección visual de grafica 2D, 3D, colision(si existe)"), unsafe_allow_html=True)

        col1, col2 = st.columns([2, 2])
        with col1:
            fig2d = grafico_2d_interactivo(elipses, ruts_limpios)
            st.plotly_chart(fig2d, use_container_width=True, key="graf2d_tab2")

        with col2:
            fig3d = Grafico_3D_multiple(elipses, ruts_limpios)
            st.plotly_chart(fig3d, use_container_width=True, key="graf3d_tab2")
        
        st.markdown("---")
        st.markdown("""<h4 style="color: #ff6f61" >Resultados de colisión</h4>""", unsafe_allow_html=True)

        resultados, estadisticas = analizar_colisiones_detallado(elipses, ruts_limpios)

        # Mostrar resultados detallados de colisiones
        for r in resultados:
            estado = "❌ Colisión " if r["colision"] else "✅ Sin colisión"
            mensaje = f"- {r['rut1']} vs {r['rut2']}: {estado}"
            
            # Usamos la función tipo_colision para obtener más detalles
            if r["colision"]:
                # Obtenemos las elipses correspondientes
                elipse1 = next(e for e, rut in zip(elipses, ruts_limpios) if rut == r['rut1'])
                elipse2 = next(e for e, rut in zip(elipses, ruts_limpios) if rut == r['rut2'])
                
                tipo = tipo_colision(elipse1, elipse2)
                st.error(f"{tipo} : {mensaje}")
                
                # Mostrar análisis detallado en un expander
                with st.expander(f"Ver detalles de colisión entre {r['rut1']} y {r['rut2']}"):
                    analisis = analizar_colision_detallada(elipse1, elipse2)
                    st.write(f"**Distancia entre centros:** {analisis['distancia_centros']}")
                    st.write(f"**Suma de radios máximos:** {analisis['suma_radios_maximos']}")
                    st.write(f"**Diferencia de radios:** {analisis['diferencia_radios']}")
                    st.write(f"**Porcentaje de solapamiento:** {analisis.get('porcentaje_solapamiento', 0)}%")
                    st.write(f"**Tipo de colisión:** {analisis['tipo']}")
            else:
                st.success(f"{mensaje}")
        
        total_colisiones = (estadisticas['colision_leve'] + estadisticas['colision_moderada'] + estadisticas['colision_severa'] + estadisticas['colision_inclusion'])

        total_sin_colisiones = estadisticas['sin_colision']

        # Usar el mismo formato que tenías
        st.markdown(
            f""" 
            <div style="font-size:16px">
                <p><strong>Total de operaciones por detección de colisiones:</strong> {estadisticas['total_comparaciones']}</p>
                <p style="color:red">🔴 <strong>Total de colisiones:</strong> {total_colisiones}</p>
                <p style="color:green">🟢 <strong>Sin colisión:</strong> {total_sin_colisiones}</p>
            </div>
            """, unsafe_allow_html=True)
        
# Procesar y mostrar datos                 
def Mostrar_datos_encapsulado_elipse(elipse, rut):
    try:
        e_canonica = elipse.ecuacion_canonica()
        e_general = elipse.ecuacion_general()
        datos = ElipseVisual(**elipse.__dict__)  # Crear instancia en una clase de herencia
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
            <p>h = {elipse.h} k = {elipse.k} a = {elipse.a}  b = {elipse.b}</p>
            <div class="block">
                <div class="row-flex">
                    <div class="scroll-inner">
                        <ul>
                            <li><b>C(h,k)</b> = C({elipse.h}, {elipse.k})</li>
                            <li><b>Focos</b> = F1: {f1_str} ; F2: {f2_str}</li>
                            <li><b>Vertices P.</b> = V1{elementos['vertices_principales'][0]} ; V2{elementos['vertices_principales'][1]}</li>
                            <li><b>Vertices A.</b> = B1{elementos['vertices_secundarios'][0]} ; B2{elementos['vertices_secundarios'][1]}</li>
                            <li><b>c = √a² - b²</b> = {elementos['c']}</li>
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