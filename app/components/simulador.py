# components/simulador.py
"""
Lógica de simulación principal con todas las funcionalidades integradas
"""
from core.Math_ellipse import generar_elipse_desde_rut
from core.collision.CollisionDetection import hay_colision_mejorada
from core.collision.CollisionAnalysis import (analizar_colision_detallada, tipo_colision)
from core.collision.CollisionResolver import (resolver_colisiones_automatico, obtener_estadisticas_resolucion)

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
