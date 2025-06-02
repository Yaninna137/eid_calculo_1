# components/simulador.py
"""
Lógica de simulación principal con todas las funcionalidades integradas
"""
from core.Math_ellipse import generar_elipse_desde_rut
from core.collision.CollisionDetection import hay_colision_mejorada
from core.collision.CollisionAnalysis import (analizar_colision_detallada, tipo_colision)
from core.collision.CollisionResolver import (resolver_colisiones_automatico, obtener_estadisticas_resolucion)
from core.trajectory.TrajectoryGenerator import (generar_trayectoria_eliptica_segura, calcular_longitud_trayectoria)
from core.trajectory.ExternalIntegration import ( analizar_colision_avanzado, obtener_info_librerias)

def procesar_ruts(ruts):
    """
    Intenta generar elipses desde RUTs dados. Devuelve dos listas: elipses válidas y errores.
    """
    elipses = []
    errores = []

    for rut in ruts:
        try:
            elipse = generar_elipse_desde_rut(rut)
            elipses.append(elipse)
        except Exception as e:
            errores.append(f"{rut}: {e}")
    
    return elipses, errores

def analizar_colisiones_detallado(elipses, ruts):
    """
    Análisis detallado de colisiones con clasificación por tipos
    """
    resultados_detallados = []
    estadisticas = {
        'total_comparaciones': len(elipses) * (len(elipses) - 1) // 2,
        'sin_colision': 0,
        'colision_leve': 0,
        'colision_moderada': 0,
        'colision_severa': 0,
        'colision_inclusion': 0
    }
    
    for i in range(len(elipses)):
        for j in range(i + 1, len(elipses)):
            elipse1, elipse2 = elipses[i], elipses[j]
            rut1, rut2 = ruts[i], ruts[j]
            
            if hay_colision_mejorada(elipse1, elipse2):
                analisis = analizar_colision_detallada(elipse1, elipse2)
                tipo = tipo_colision(elipse1, elipse2)
                
                resultado = {
                    "rut1": rut1,
                    "rut2": rut2,
                    "colision": True,
                    "tipo": tipo,
                    "analisis_completo": analisis
                }
                
                # Clasificar para estadísticas
                if 'inclusión' in tipo.lower():
                    estadisticas['colision_inclusion'] += 1
                elif 'severa' in tipo.lower():
                    estadisticas['colision_severa'] += 1
                elif 'moderada' in tipo.lower():
                    estadisticas['colision_moderada'] += 1
                elif 'leve' in tipo.lower():
                    estadisticas['colision_leve'] += 1
                    
            else:
                resultado = {
                    "rut1": rut1,
                    "rut2": rut2,
                    "colision": False,
                    "tipo": "Sin colisión",
                    "analisis_completo": None
                }
                estadisticas['sin_colision'] += 1
            
            resultados_detallados.append(resultado)
    
    return resultados_detallados, estadisticas

def resolver_colisiones_multiples(elipses, ruts):
    """
    NUEVA FUNCIÓN: Resuelve automáticamente las colisiones entre múltiples elipses
    """
    if len(elipses) < 2:
        return {
            'elipses_originales': elipses,
            'elipses_resueltas': elipses,
            'colisiones_resueltas': True,
            'estadisticas': None
        }
    
    # Resolver colisiones
    elipses_resueltas = resolver_colisiones_automatico(elipses)
    
    # Obtener estadísticas
    estadisticas = obtener_estadisticas_resolucion(elipses, elipses_resueltas)
    
    return {
        'elipses_originales': elipses,
        'elipses_resueltas': elipses_resueltas,
        'colisiones_resueltas': estadisticas['colisiones_resueltas'] if estadisticas else False,
        'estadisticas': estadisticas,
        'ruts': ruts
    }

def generar_trayectorias_seguras(elipses, ruts, puntos_por_trayectoria=100):
    """
    NUEVA FUNCIÓN: Genera trayectorias seguras para cada dron evitando colisiones
    """
    trayectorias = []
    
    for i, elipse in enumerate(elipses):
        # Obtener obstáculos (otras elipses)
        obstaculos = [e for j, e in enumerate(elipses) if j != i]
        
        # Generar trayectoria segura
        trayectoria = generar_trayectoria_eliptica_segura(
            elipse, obstaculos, puntos=puntos_por_trayectoria
        )
        
        # Calcular métricas
        longitud = calcular_longitud_trayectoria(trayectoria)
        
        trayectorias.append({
            'rut': ruts[i],
            'elipse_original': elipse,
            'trayectoria': trayectoria,
            'longitud_trayectoria': round(longitud, 2),
            'numero_puntos': len(trayectoria)
        })
    
    return trayectorias

def analizar_precision_avanzada(elipses, ruts):
    """
    NUEVA FUNCIÓN: Análisis de precisión usando librerías externas cuando están disponibles
    """
    info_librerias = obtener_info_librerias()
    resultados_avanzados = []
    
    if len(elipses) < 2:
        return {
            'info_librerias': info_librerias,
            'resultados': [],
            'comparaciones_realizadas': 0
        }
    
    for i in range(len(elipses)):
        for j in range(i + 1, len(elipses)):
            try:
                analisis = analizar_colision_avanzado(elipses[i], elipses[j])
                resultados_avanzados.append({
                    'rut1': ruts[i],
                    'rut2': ruts[j],
                    'analisis_avanzado': analisis
                })
            except Exception as e:
                resultados_avanzados.append({
                    'rut1': ruts[i],
                    'rut2': ruts[j],
                    'error': str(e)
                })
    
    return {
        'info_librerias': info_librerias,
        'resultados': resultados_avanzados,
        'comparaciones_realizadas': len(resultados_avanzados)
    }

def simulacion_completa(ruts):
    """
    NUEVA FUNCIÓN: Ejecuta una simulación completa con todas las funcionalidades
    """
    # 1. Procesar RUTs
    elipses, errores = procesar_ruts(ruts)
    
    if errores:
        return {
            'exito': False,
            'errores': errores,
            'elipses': []
        }
    
    # 2. Análisis de colisiones básico
    resultados_colision, estadisticas_colision = analizar_colisiones_detallado(elipses, ruts)
    
    # 3. Resolución automática de colisiones
    resolucion = resolver_colisiones_multiples(elipses, ruts)
    
    # 4. Generación de trayectorias seguras
    trayectorias = generar_trayectorias_seguras(elipses, ruts)
    
    # 5. Análisis de precisión avanzada (si están disponibles las librerías)
    precision_avanzada = analizar_precision_avanzada(elipses, ruts)
    
    return {
        'exito': True,
        'elipses_originales': elipses,
        'ruts': ruts,
        'analisis_colisiones': {
            'resultados': resultados_colision,
            'estadisticas': estadisticas_colision
        },
        'resolucion_colisiones': resolucion,
        'trayectorias_seguras': trayectorias,
        'precision_avanzada': precision_avanzada
    }