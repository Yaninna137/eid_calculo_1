# components/interfaz.py
import streamlit as st

from components.estilo import estilo_add
from components.rut_parser import limpiar_ruts
from components.Contenedor import mostrar_tarjeta_izquierda, mostrar_entrada_ruts, mostrar_columna_acciones
from components.simulador import (procesar_ruts, analizar_colisiones_detallado, resolver_colisiones_multiples, 
                                  generar_trayectorias_seguras, analizar_precision_avanzada, simulacion_completa)
from core.Graph_ellipse import Grafico_3D_multiple, grafico_2d_simple, grafico_2d_interactivo
from core.Items_ellipse import ElipseVisual
from core.collision.CollisionAnalysis import tipo_colision, analizar_colision_detallada

def encabezado_html(titulo: str, descripcion: str):
    return f"""
    <div style='background-color: #1b1f2a; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
        <h2 style='margin-bottom: 5px; color: white; text-align: center;'>{titulo}</h2>
        <p style='font-size: 18px; color: gray; text-align: center;'>{descripcion}</p>
    </div>
    """

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
        
        # Botón para generar elipses
        if mostrar_columna_acciones(ruts_limpios):
            elipses, errores = procesar_ruts(ruts_limpios)
            
            if errores:
                st.error("⚠️ Algunos RUTs no pudieron procesarse:")
                for err in errores:
                    st.markdown(f"- {err}")
                # Limpiar datos del session_state si hay errores
                st.session_state.elipses_generadas = None
                st.session_state.ruts_procesados = None
                st.session_state.mostrar_datos = False
            else:
                st.success("✅ Elipses generadas correctamente.")
                # Guardar datos en session_state
                st.session_state.elipses_generadas = elipses
                st.session_state.ruts_procesados = ruts_limpios
                st.session_state.mostrar_datos = True

    # Mostrar datos si existen en session_state
    if st.session_state.mostrar_datos and st.session_state.elipses_generadas:
        mostrar_datos(st.session_state.elipses_generadas, st.session_state.ruts_procesados)


def mostrar_datos(elipses, ruts_limpios):
    st.markdown("---")
    
    # Agregar más pestañas para las nuevas funcionalidades
    tab1, tab2, tab3, tab4 = st.tabs([
        "Datos de elipses", 
        "Gráficos y Colisiones", 
        "Resolución de Colisiones",
        "Trayectorias Seguras"
    ])
    
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
        mostrar_analisis_colisiones(elipses, ruts_limpios)
    
    with tab3:
        mostrar_resolucion_colisiones(elipses, ruts_limpios)
    
    with tab4:
        mostrar_trayectorias_seguras(elipses, ruts_limpios)


def mostrar_analisis_colisiones(elipses, ruts_limpios):
    """Pestaña original de análisis de colisiones"""
    st.markdown(encabezado_html("Comparación visual y detección de colisiones", "Sección visual de gráfica 2D, 3D, colisión (si existe)"), unsafe_allow_html=True)

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
        
        if r["colision"]:
            elipse1 = next(e for e, rut in zip(elipses, ruts_limpios) if rut == r['rut1'])
            elipse2 = next(e for e, rut in zip(elipses, ruts_limpios) if rut == r['rut2'])
            
            tipo = tipo_colision(elipse1, elipse2)
            st.error(f"{tipo} : {mensaje}")
            
            with st.expander(f"Ver detalles de colisión entre {r['rut1']} y {r['rut2']}"):
                analisis = analizar_colision_detallada(elipse1, elipse2)
                st.write(f"**Distancia entre centros:** {analisis['distancia_centros']}")
                st.write(f"**Suma de radios máximos:** {analisis['suma_radios_maximos']}")
                st.write(f"**Diferencia de radios:** {analisis['diferencia_radios']}")
                st.write(f"**Porcentaje de solapamiento:** {analisis.get('porcentaje_solapamiento', 0)}%")
                st.write(f"**Tipo de colisión:** {analisis['tipo']}")
                st.write(f"**Nivel de riesgo:** {analisis['nivel_riesgo']}")
        else:
            st.success(f"{mensaje}")
    
    total_colisiones = (estadisticas['colision_leve'] + estadisticas['colision_moderada'] + 
                       estadisticas['colision_severa'] + estadisticas['colision_inclusion'])
    total_sin_colisiones = estadisticas['sin_colision']

    st.markdown(
        f""" 
        <div style="font-size:16px">
            <p><strong>Total de operaciones por detección de colisiones:</strong> {estadisticas['total_comparaciones']}</p>
            <p style="color:red">🔴 <strong>Total de colisiones:</strong> {total_colisiones}</p>
            <p style="color:green">🟢 <strong>Sin colisión:</strong> {total_sin_colisiones}</p>
        </div>
        """, unsafe_allow_html=True)


def mostrar_resolucion_colisiones(elipses, ruts_limpios):
    """Nueva pestaña para resolución automática de colisiones"""
    st.markdown(encabezado_html("Resolución automática de colisiones",
            "Sistema inteligente para separar drones en colisión y generar configuraciones seguras"),unsafe_allow_html=True)

    # Controles para la resolución
    ejecutar_resolucion = st.button("🔧 Resolver Colisiones", type="primary", key="btn_resolver_colisiones")

    if ejecutar_resolucion:
        st.session_state.mostrar_resolucion = True

        with st.spinner("Resolviendo colisiones..."):
            resultado_resolucion = resolver_colisiones_multiples(elipses, ruts_limpios)

            # Guardar resultado en session_state
            st.session_state.resultado_resolucion = resultado_resolucion
            st.session_state.elipses_resueltas = resultado_resolucion.get('elipses_resueltas', [])

    # Mostrar resultados si existen en session_state
    if st.session_state.get("mostrar_resolucion") and st.session_state.get("resultado_resolucion"):
        resultado_resolucion = st.session_state.resultado_resolucion

        if resultado_resolucion.get('colisiones_resueltas'):
            st.success("✅ ¡Todas las colisiones han sido resueltas!")
        else:
            st.warning("⚠️ Algunas colisiones aún persisten. Intenta aumentar las iteraciones.")

        # Comparación visual: antes y después
        st.markdown("### Comparación: Antes vs Después")
        col_antes, col_despues = st.columns(2)

        with col_antes:
            st.markdown("**Configuración Original**")
            fig_antes = grafico_2d_interactivo(elipses, ruts_limpios)
            st.plotly_chart(fig_antes, use_container_width=True)

        with col_despues:
            st.markdown("**Configuración Resuelta**")
            fig_despues = grafico_2d_interactivo(
                resultado_resolucion.get('elipses_resueltas', []),
                ruts_limpios
            )
            st.plotly_chart(fig_despues, use_container_width=True)

        # Estadísticas de resolución
        estadisticas = resultado_resolucion.get('estadisticas')
        if estadisticas:
            st.markdown("### Estadísticas de Resolución")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Desplazamiento Promedio", f"{estadisticas['desplazamiento_promedio']:.2f}")
            with col2:
                st.metric("Desplazamiento Máximo", f"{estadisticas['desplazamiento_maximo']:.2f}")
            with col3:
                st.metric("Desplazamiento Mínimo", f"{estadisticas['desplazamiento_minimo']:.2f}")
            with col4:
                estado_resolucion = "✅ Completado" if estadisticas['colisiones_resueltas'] else "❌ Pendiente"
                st.metric("Estado", estado_resolucion)

        # Análisis post-resolución
        st.markdown("### Verificación Post-Resolución")
        resultados_post, _ = analizar_colisiones_detallado(
            resultado_resolucion.get('elipses_resueltas', []),
            ruts_limpios
        )

        colisiones_restantes = sum(1 for r in resultados_post if r.get("colision"))

        if colisiones_restantes == 0:
            st.success(f"🎉 Configuración completamente segura: {len(elipses)} drones sin colisiones")
        else:
            st.error(f"⚠️ Aún quedan {colisiones_restantes} colisiones por resolver")

def mostrar_trayectorias_seguras(elipses, ruts_limpios):
    """Nueva pestaña para trayectorias seguras"""
    st.markdown(encabezado_html("Generación de trayectorias seguras", "Calcula rutas de vuelo que evitan colisiones entre drones"), unsafe_allow_html=True)
    
    # Configuración de trayectorias
    col1, col2, col3 = st.columns(3)
    with col1:
        puntos_trayectoria = st.slider("Puntos por trayectoria", 50, 500, 100, step=50, key="puntos_trayectoria")
    with col2:
        margen_seguridad = st.slider("Margen de seguridad", 1.0, 2.0, 1.2, step=0.1, key="margen_seguridad")
    with col3:
        generar_trayectorias = st.button("🛤️ Generar Trayectorias", type="primary", key="btn_generar_trayectorias")
    
    if generar_trayectorias:
        st.session_state.mostrar_trayectorias = True
        
        with st.spinner("Generando trayectorias seguras..."):
            trayectorias = generar_trayectorias_seguras(elipses, ruts_limpios, puntos_trayectoria)
            # Guardar en session_state
            st.session_state.trayectorias_generadas = trayectorias
    
    # Mostrar trayectorias si existen en session_state
    if st.session_state.mostrar_trayectorias and st.session_state.trayectorias_generadas:
        trayectorias = st.session_state.trayectorias_generadas
        
        st.success(f"✅ Generadas {len(trayectorias)} trayectorias seguras")
        
        # Mostrar métricas de trayectorias
        st.markdown("### Métricas de Trayectorias")
        
        # Crear columnas dinámicas basadas en el número de trayectorias
        num_cols = min(len(trayectorias), 4)  # Máximo 4 columnas
        cols = st.columns(num_cols)
        
        for i, trayectoria in enumerate(trayectorias):
            with cols[i % num_cols]:
                st.metric(
                    f"Dron {trayectoria['rut']}", 
                    f"{trayectoria['longitud_trayectoria']} unidades",
                    f"{trayectoria['numero_puntos']} puntos"
                )
        
        # Visualización de trayectorias (esto requeriría modificar las funciones de gráficos)
        st.markdown("### Visualización de Trayectorias")
        st.info("💡 Las trayectorias se muestran como rutas optimizadas que evitan las zonas de colisión entre elipses")
        
        # Mostrar detalles expandibles para cada trayectoria
        for trayectoria in trayectorias:
            with st.expander(f"Detalles de trayectoria - Dron {trayectoria['rut']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Longitud total:** {trayectoria['longitud_trayectoria']} unidades")
                    st.write(f"**Número de puntos:** {trayectoria['numero_puntos']}")
                    st.write(f"**Elipse original:** Centro ({trayectoria['elipse_original'].h}, {trayectoria['elipse_original'].k})")
                
                with col2:
                    # Aquí podrías mostrar un gráfico específico de la trayectoria
                    st.write("**Primeros 5 puntos de la trayectoria:**")
                    for i, punto in enumerate(trayectoria['trayectoria'][:5]):
                        st.write(f"{i+1}. ({punto[0]:.2f}, {punto[1]:.2f})")

    # Sección de análisis avanzado (opcional)
    if st.checkbox("🔬 Mostrar análisis de precisión avanzada", key="checkbox_precision_avanzada"):
        with st.spinner("Ejecutando análisis avanzado..."):
            precision_avanzada = analizar_precision_avanzada(elipses, ruts_limpios)
        
        st.markdown("### Análisis de Precisión Avanzada")
        
        # Mostrar información de librerías
        info_libs = precision_avanzada['info_librerias']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            estado_shapely = "✅ Disponible" if info_libs['shapely'] else "❌ No disponible"
            st.write(f"**Shapely:** {estado_shapely}")
        with col2:
            estado_numpy = "✅ Disponible" if info_libs['numpy'] else "❌ No disponible"
            st.write(f"**NumPy:** {estado_numpy}")
        with col3:
            st.write(f"**Comparaciones:** {precision_avanzada['comparaciones_realizadas']}")
        
        if not info_libs['shapely'] or not info_libs['numpy']:
            st.info(f"💡 {info_libs['recomendacion']}")


# Procesar y mostrar datos                 
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