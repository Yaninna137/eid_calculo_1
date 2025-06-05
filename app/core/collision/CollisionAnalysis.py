# core/collision/CollisionAnalysis.py
"""
Módulo para el análisis detallado de colisiones entre elipses
Utiliza las funciones mejoradas de CollisionDetection e incluye puntos de intersección
"""
from math import pi
from .CollisionDetection import (distancia_centros, hay_colision_mejorada, hay_colision_precisa,
    distancia_minima_entre_elipses, punto_dentro_de_elipse)
from .IntersectionPoints import encontrar_puntos_interseccion, formatear_puntos_interseccion

def tipo_colision(elipse1, elipse2):
    """
    Determina el tipo de colisión entre dos elipses con mayor precisión
    """
    if not hay_colision_mejorada(elipse1, elipse2):
        return "Sin colisión"
    
    # Usar la función mejorada de distancia entre centros
    distancia_centros_val = distancia_centros(elipse1, elipse2)
    
    # Radios efectivos, se estima el el radio medio (a+b)/2
    radio_efectivo_1 = (elipse1.a + elipse1.b) / 2
    radio_efectivo_2 = (elipse2.a + elipse2.b) / 2
    
    # Verificar si hay inclusión completa
    if punto_dentro_de_elipse(elipse1.h, elipse1.k, elipse2) or \
       punto_dentro_de_elipse(elipse2.h, elipse2.k, elipse1):
        return "🔴 Colisión por inclusión"
    
    # Clasificar tipo de colisión basado en distancia
    if distancia_centros_val < abs(radio_efectivo_1 - radio_efectivo_2):
        return "🔴 Colisión por inclusión"
    elif distancia_centros_val < (radio_efectivo_1 + radio_efectivo_2) * 0.3:
        return "🟠 Colisión severa"
    elif distancia_centros_val < (radio_efectivo_1 + radio_efectivo_2) * 0.7:
        return "🟡 Colisión moderada"
    else:
        return "🟢 Colisión leve"

def analizar_colision_detallada(elipse1, elipse2):
    """
    Proporciona un análisis detallado de la colisión entre dos elipses
    Utiliza las funciones mejoradas de detección e incluye puntos de intersección
    """
    # Usar la función mejorada de distancia entre centros
    distancia_centros_val = distancia_centros(elipse1, elipse2)
    
    # Radios máximos y mínimos
    radio_max_1 = elipse1.a
    radio_min_1 = elipse1.b
    radio_max_2 = elipse2.a
    radio_min_2 = elipse2.b
    
    # Suma de radios
    suma_radios_maximos = radio_max_1 + radio_max_2
    suma_radios_minimos = radio_min_1 + radio_min_2
    diferencia_radios = abs(radio_max_1 - radio_max_2)
    
    # Porcentaje de solapamiento aproximado (R1+R2-d)/(R1+R2)*100
    if distancia_centros_val < suma_radios_maximos:
        solapamiento = ((suma_radios_maximos - distancia_centros_val) / suma_radios_maximos) * 100
    else:
        solapamiento = 0
    
    # Determinar tipo de colisión
    tipo = tipo_colision(elipse1, elipse2)
    
    # NUEVA FUNCIONALIDAD: Encontrar puntos de intersección
    puntos_interseccion = []
    puntos_interseccion_str = "No hay intersección"
    
    if hay_colision_mejorada(elipse1, elipse2):
        puntos_interseccion = encontrar_puntos_interseccion(elipse1, elipse2)
        puntos_interseccion_str = formatear_puntos_interseccion(puntos_interseccion)
    
    # Análisis de riesgo mejorado
    if distancia_centros_val == 0:
        riesgo = "CRÍTICO - Centros coincidentes"
    elif punto_dentro_de_elipse(elipse1.h, elipse1.k, elipse2) or \
         punto_dentro_de_elipse(elipse2.h, elipse2.k, elipse1):
        riesgo = "CRÍTICO - Una elipse contiene el centro de la otra"
    elif distancia_centros_val < diferencia_radios:
        riesgo = "ALTO - Posible inclusión de elipses"
    elif solapamiento > 50:
        riesgo = "MEDIO-ALTO - Solapamiento significativo"
    elif solapamiento > 20:
        riesgo = "MEDIO - Solapamiento moderado"
    elif solapamiento > 0:
        riesgo = "BAJO - Solapamiento mínimo"
    else:
        riesgo = "NULO - Sin solapamiento"
    
    # Calcular distancia mínima entre perímetros
    distancia_minima = 0
    if not hay_colision_mejorada(elipse1, elipse2):
        distancia_minima = distancia_minima_entre_elipses(elipse1, elipse2)
    
    return {
        'distancia_centros': round(distancia_centros_val, 2),
        'suma_radios_maximos': round(suma_radios_maximos, 2),
        'suma_radios_minimos': round(suma_radios_minimos, 2),
        'diferencia_radios': round(diferencia_radios, 2),
        'porcentaje_solapamiento': round(solapamiento, 1),
        'distancia_minima_perimetros': round(distancia_minima, 2),
        'tipo': tipo,
        'nivel_riesgo': riesgo,
        'area_elipse1': round(pi * elipse1.a * elipse1.b, 2),
        'area_elipse2': round(pi * elipse2.a * elipse2.b, 2),
        'orientacion_1': elipse1.orientacion,
        'orientacion_2': elipse2.orientacion,
        'colision_precisa': hay_colision_precisa(elipse1, elipse2) if hay_colision_mejorada(elipse1, elipse2) else False,
        # NUEVOS CAMPOS
        'puntos_interseccion': puntos_interseccion,
        'puntos_interseccion_str': puntos_interseccion_str,
        'numero_puntos_interseccion': len(puntos_interseccion)
    }

def analizar_multiples_colisiones(elipses, identificadores=None):
    """
    FUNCIÓN ACTUALIZADA: Analiza colisiones entre múltiples elipses incluyendo puntos de intersección
    """
    if identificadores is None:
        identificadores = [f"Elipse_{i+1}" for i in range(len(elipses))]
    
    resultados = []
    matriz_colisiones = {}
    
    for i in range(len(elipses)):
        for j in range(i + 1, len(elipses)):
            analisis = analizar_colision_detallada(elipses[i], elipses[j])
            
            resultado = {
                'id1': identificadores[i],
                'id2': identificadores[j],
                'tiene_colision': hay_colision_mejorada(elipses[i], elipses[j]),
                'analisis': analisis
            }
            
            resultados.append(resultado)
            matriz_colisiones[f"{identificadores[i]}-{identificadores[j]}"] = resultado['tiene_colision']
    
    # Estadísticas generales
    total_comparaciones = len(resultados)
    total_colisiones = sum(1 for r in resultados if r['tiene_colision'])
    
    return {
        'resultados_detallados': resultados,
        'matriz_colisiones': matriz_colisiones,
        'estadisticas': {
            'total_comparaciones': total_comparaciones,
            'total_colisiones': total_colisiones,
            'total_sin_colisiones': total_comparaciones - total_colisiones,
            'porcentaje_colisiones': round((total_colisiones / total_comparaciones) * 100, 1) if total_comparaciones > 0 else 0
        }
    }