# core/trajectory/ExternalIntegration.py
"""
Integración con librerías externas para mejorar precisión de colisiones
"""
from math import pi, cos, sin

# Verificar disponibilidad de librerías externas
try:
    from shapely.geometry import Polygon
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

def verificar_colision_con_shapely(elipse1, elipse2, puntos=100):
    """
    Usa Shapely para detección precisa de colisiones entre elipses
    """
    if not SHAPELY_AVAILABLE:
        raise ImportError("Shapely no está disponible. Instale con: pip install shapely")
    
    def elipse_a_poligono(elipse, n_puntos=puntos):
        """Convierte una elipse en un polígono de Shapely"""
        coordenadas = []
        for i in range(n_puntos):
            angulo = 2 * pi * i / n_puntos
            if elipse.orientacion == "horizontal":
                x = elipse.h + elipse.a * cos(angulo)
                y = elipse.k + elipse.b * sin(angulo)
            else:
                x = elipse.h + elipse.b * cos(angulo)
                y = elipse.k + elipse.a * sin(angulo)
            coordenadas.append((x, y))
        return Polygon(coordenadas)
    
    try:
        poligono1 = elipse_a_poligono(elipse1)
        poligono2 = elipse_a_poligono(elipse2)
        
        # Verificar intersección
        intersecta = poligono1.intersects(poligono2)
        
        # Calcular área de intersección si existe
        area_interseccion = 0
        if intersecta:
            interseccion = poligono1.intersection(poligono2)
            area_interseccion = interseccion.area
        
        return {
            'colision': intersecta,
            'area_interseccion': area_interseccion,
            'area_elipse1': poligono1.area,
            'area_elipse2': poligono2.area,
            'porcentaje_solapamiento': (area_interseccion / min(poligono1.area, poligono2.area)) * 100 if intersecta else 0
        }
    
    except Exception as e:
        print(f"Error en detección con Shapely: {e}")
        return {'colision': False, 'error': str(e)}

def calcular_distancia_minima_numpy(elipse1, elipse2, puntos=360):
    """
    Usa NumPy para cálculos vectorizados de distancia mínima entre elipses
    """
    if not NUMPY_AVAILABLE:
        raise ImportError("NumPy no está disponible. Instale con: pip install numpy")
    
    try:
        # Generar puntos de ambas elipses usando NumPy
        angulos = np.linspace(0, 2 * np.pi, puntos)
        
        # Puntos de la primera elipse
        if elipse1.orientacion == "horizontal":
            x1 = elipse1.h + elipse1.a * np.cos(angulos)
            y1 = elipse1.k + elipse1.b * np.sin(angulos)
        else:
            x1 = elipse1.h + elipse1.b * np.cos(angulos)
            y1 = elipse1.k + elipse1.a * np.sin(angulos)
        
        # Puntos de la segunda elipse
        if elipse2.orientacion == "horizontal":
            x2 = elipse2.h + elipse2.a * np.cos(angulos)
            y2 = elipse2.k + elipse2.b * np.sin(angulos)
        else:
            x2 = elipse2.h + elipse2.b * np.cos(angulos)
            y2 = elipse2.k + elipse2.a * np.sin(angulos)
        
        # Calcular matriz de distancias
        distancias = np.sqrt((x1[:, np.newaxis] - x2)**2 + (y1[:, np.newaxis] - y2)**2)
        
        return float(np.min(distancias))
    
    except Exception as e:
        print(f"Error en cálculo con NumPy: {e}")
        return float('inf')

def analizar_colision_avanzado(elipse1, elipse2):
    """
    Análisis avanzado combinando múltiples métodos cuando están disponibles
    """
    resultado = {
        'metodos_disponibles': [],
        'resultados': {}
    }
    
    # Método básico (siempre disponible)
    from core.collision.CollisionDetection import hay_colision_mejorada
    resultado['resultados']['basico'] = hay_colision_mejorada(elipse1, elipse2)
    resultado['metodos_disponibles'].append('basico')
    
    # Método con Shapely si está disponible
    if SHAPELY_AVAILABLE:
        try:
            resultado['resultados']['shapely'] = verificar_colision_con_shapely(elipse1, elipse2)
            resultado['metodos_disponibles'].append('shapely')
        except Exception as e:
            resultado['resultados']['shapely_error'] = str(e)
    
    # Método con NumPy si está disponible
    if NUMPY_AVAILABLE:
        try:
            resultado['resultados']['numpy_distancia'] = calcular_distancia_minima_numpy(elipse1, elipse2)
            resultado['metodos_disponibles'].append('numpy')
        except Exception as e:
            resultado['resultados']['numpy_error'] = str(e)
    
    # Determinar resultado final
    if 'shapely' in resultado['metodos_disponibles']:
        resultado['colision_final'] = resultado['resultados']['shapely']['colision']
        resultado['metodo_usado'] = 'shapely'
    else:
        resultado['colision_final'] = resultado['resultados']['basico']
        resultado['metodo_usado'] = 'basico'
    
    return resultado

def obtener_info_librerias():
    """
    Devuelve información sobre las librerías externas disponibles
    """
    return {
        'shapely': SHAPELY_AVAILABLE,
        'numpy': NUMPY_AVAILABLE,
        'recomendacion': 'Para mejor precisión, instale: pip install shapely numpy'
    }