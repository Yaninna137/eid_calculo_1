import streamlit as st
from components.simulador import (analizar_colisiones_detallado, resolver_colisiones_multiples, 
                                  generar_trayectorias_seguras, analizar_precision_avanzada)
from core.Graph_ellipse import Grafico_3D_multiple, grafico_2d_interactivo
from core.collision.CollisionAnalysis import tipo_colision, analizar_colision_detallada
from components.Contenedor import encabezado_html

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