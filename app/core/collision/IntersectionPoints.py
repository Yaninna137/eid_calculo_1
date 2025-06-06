# core/collision/IntersectionPoints.py
"""
Módulo para calcular puntos de intersección específicos entre elipses
VERSIÓN OPTIMIZADA: Código factorizado y acortado
"""
from math import cos, sin, pi, sqrt
from core.Math_ellipse import Elipse

def _calcular_punto_elipse(elipse: Elipse, angulo: float):
    """Calcula un punto en el perímetro de una elipse dado un ángulo (ecuacion general)"""
    if elipse.orientacion == "horizontal":
        return (elipse.h + elipse.a * cos(angulo), elipse.k + elipse.b * sin(angulo))
    return (elipse.h + elipse.b * cos(angulo), elipse.k + elipse.a * sin(angulo))

def _valor_elipse(x: float, y: float, elipse: Elipse):
    """Calcula el valor de la ecuación de la elipse para un punto dado
    ≈ 1.0: está en el borde
    < 1.0: está dentro
    > 1.0: está fuera"""
    dx, dy = x - elipse.h, y - elipse.k
    if elipse.orientacion == "horizontal":
        return (dx**2)/(elipse.a**2) + (dy**2)/(elipse.b**2)
    return (dx**2)/(elipse.b**2) + (dy**2)/(elipse.a**2)

def _punto_dentro_elipse(x: float, y: float, elipse: Elipse, margen: float = 0.99):
    """Verifica si un punto está dentro de una elipse con margen dado de 0.99"""
    return _valor_elipse(x, y, elipse) < margen

def _punto_cerca_borde(x: float, y: float, elipse: Elipse, tolerancia: float = 0.01):
    """Verifica si un punto está cerca del borde de una elipse ∣valor−1.0∣≤tolerancia"""
    return abs(_valor_elipse(x, y, elipse) - 1.0) <= tolerancia

def _hay_punto_cercano(lista_puntos: list, x: float, y: float, distancia_min: float = 0.1):
    """Verifica si ya existe un punto cercano en la lista"""
    return any(sqrt((x - px)**2 + (y - py)**2) < distancia_min for px, py in lista_puntos)

def _es_transicion(punto_actual, punto_anterior, punto_siguiente, elipse_destino):
    """Verifica si existe una transición entre estados dentro/fuera de la elipse"""
    estados = [_punto_dentro_elipse(*punto, elipse_destino) for punto in [punto_anterior, punto_actual, punto_siguiente]]
    return estados[0] != estados[1] or estados[1] != estados[2]

def _refinar_interseccion(elipse_origen: Elipse, elipse_destino: Elipse, angulo_inicio: float, angulo_fin: float, iteraciones: int = 10):
    """Refina un punto de intersección usando búsqueda binaria"""
    for _ in range(iteraciones):
        angulo_medio = (angulo_inicio + angulo_fin) / 2
        x, y = _calcular_punto_elipse(elipse_origen, angulo_medio)
        
        valor = _valor_elipse(x, y, elipse_destino)
        if abs(valor - 1.0) < 0.001:
            return (round(x, 3), round(y, 3))
        
        if valor < 1.0:
            angulo_inicio = angulo_medio
        else:
            angulo_fin = angulo_medio
    return None

def encontrar_puntos_interseccion(elipse1: Elipse, elipse2: Elipse, precision: int = 1000):
    """
    Encuentra los puntos específicos donde dos elipses se intersectan
    ALGORITMO CORREGIDO: Solo encuentra puntos de intersección real
    """
    puntos_interseccion = []
    delta_angulo = 2 * pi / precision
    
    for i in range(precision):
        angulo = delta_angulo * i
        punto_actual = _calcular_punto_elipse(elipse1, angulo)
        
        # Verificar si está cerca del borde de elipse2
        if not _punto_cerca_borde(*punto_actual, elipse2):
            continue
        
        # Calcular puntos adyacentes para verificar transición
        punto_anterior = _calcular_punto_elipse(elipse1, angulo - delta_angulo)
        punto_siguiente = _calcular_punto_elipse(elipse1, angulo + delta_angulo)
        
        # Verificar transición y evitar duplicados
        if (_es_transicion(punto_actual, punto_anterior, punto_siguiente, elipse2) and
            not _hay_punto_cercano(puntos_interseccion, *punto_actual)):
            puntos_interseccion.append((round(punto_actual[0], 3), round(punto_actual[1], 3)))
    
    return puntos_interseccion

def encontrar_puntos_interseccion_mejorado(elipse1: Elipse, elipse2: Elipse):
    """ALGORITMO ALTERNATIVO: Método más robusto usando búsqueda bidireccional"""
    puntos_interseccion = []
    
    # Combinar puntos de ambas direcciones
    for elipse_origen, elipse_destino in [(elipse1, elipse2), (elipse2, elipse1)]:
        puntos_interseccion.extend(_encontrar_puntos_direccional(elipse_origen, elipse_destino))
    
    # Eliminar duplicados
    puntos_unicos = []
    for punto in puntos_interseccion:
        if not _hay_punto_cercano(puntos_unicos, *punto):
            puntos_unicos.append(punto)
    
    return puntos_unicos

def _encontrar_puntos_direccional(elipse_origen: Elipse, elipse_destino: Elipse, precision: int = 2000):
    """Encuentra puntos de intersección en una dirección específica"""
    puntos = []
    estado_anterior = None
    delta_angulo = 2 * pi / precision
    
    for i in range(precision + 1):
        angulo = delta_angulo * i
        x, y = _calcular_punto_elipse(elipse_origen, angulo)
        estado_actual = _punto_dentro_elipse(x, y, elipse_destino)
        
        # Detectar cambio de estado
        if estado_anterior is not None and estado_anterior != estado_actual:
            punto_refinado = _refinar_interseccion(elipse_origen, elipse_destino, angulo - delta_angulo, angulo)
            if punto_refinado:
                puntos.append(punto_refinado)
        
        estado_anterior = estado_actual
    
    return puntos

def formatear_puntos_interseccion(puntos):
    """Formatea la lista de puntos para mostrar en la interfaz"""
    if not puntos:
        return "No se encontraron puntos de intersección"
    return ", ".join(f"({x}, {y})" for x, y in puntos)