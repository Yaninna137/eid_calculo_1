# core/collision/CollisionDetection.py
"""
Módulo para la detección de colisiones entre elipses
Integra funcionalidades de cálculo de distancias
"""
from math import sqrt, cos, sin, pi
from core.Math_ellipse import Elipse

def distancia_centros(e1: Elipse, e2: Elipse, dimensiones: int = 2) -> float:
    # Calcula la distancia euclidiana entre centros de dos elipses
    dx = e1.h - e2.h
    dy = e1.k - e2.k
    
    if dimensiones == 3:
        dz = getattr(e1, 'z', 0) - getattr(e2, 'z', 0)
        return sqrt(dx**2 + dy**2 + dz**2)
    
    return sqrt(dx**2 + dy**2)

# ==================== FUNCIONES DE DETECCIÓN DE COLISIÓN ====================
def hay_colision_mejorada(elipse1, elipse2):
    """
    Detección mejorada de colisión que considera ambos semiejes
    Mantiene la funcionalidad original para compatibilidad
    """
    # Usar la nueva función de distancia_centros
    distancia_centros_val = distancia_centros(elipse1, elipse2)
    
    # Aproximación conservadora: usar el promedio de los semiejes
    radio_efectivo_1 = (elipse1.a + elipse1.b) / 2
    radio_efectivo_2 = (elipse2.a + elipse2.b) / 2
    
    suma_radios_efectivos = radio_efectivo_1 + radio_efectivo_2
    
    # Hay colisión si la distancia es menor que la suma de radios efectivos
    return distancia_centros_val < suma_radios_efectivos

def hay_colision_precisa(elipse1, elipse2, precision=100):
    """
    NUEVA FUNCIÓN: Detección de colisión más precisa
    Verifica múltiples puntos en el perímetro de una elipse contra la otra
    """
    if not hay_colision_mejorada(elipse1, elipse2):
        # Si la detección rápida dice que no hay colisión, confiamos en ella
        return False
    
    # Verificación más precisa: revisar puntos en el perímetro
    for i in range(0, precision):
        angulo = 2 * pi * i / precision
        
        # Punto en elipse1
        if elipse1.orientacion == "horizontal":
            x1 = elipse1.h + elipse1.a * cos(angulo)
            y1 = elipse1.k + elipse1.b * sin(angulo)
        else:
            x1 = elipse1.h + elipse1.b * cos(angulo)
            y1 = elipse1.k + elipse1.a * sin(angulo)
        
        # Verificar si este punto está dentro de elipse2
        if punto_dentro_de_elipse(x1, y1, elipse2):
            return True
        
        # Punto en elipse2
        if elipse2.orientacion == "horizontal":
            x2 = elipse2.h + elipse2.a * cos(angulo)
            y2 = elipse2.k + elipse2.b * sin(angulo)
        else:
            x2 = elipse2.h + elipse2.b * cos(angulo)
            y2 = elipse2.k + elipse2.a * sin(angulo)
        
        # Verificar si este punto está dentro de elipse1
        if punto_dentro_de_elipse(x2, y2, elipse1):
            return True
    
    return False

def punto_dentro_de_elipse(x, y, elipse):
    """
    NUEVA FUNCIÓN: Verifica si un punto está dentro de una elipse
    """
    # Trasladar el punto al sistema de coordenadas con centro en el origen
    dx = x - elipse.h
    dy = y - elipse.k
    
    # Aplicar la ecuación de la elipse 
    if elipse.orientacion == "horizontal":
        valor = (dx**2)/(elipse.a**2) + (dy**2)/(elipse.b**2)
    else:
        valor = (dx**2)/(elipse.b**2) + (dy**2)/(elipse.a**2)
    
    return valor <= 1.0

def distancia_minima_entre_elipses(elipse1, elipse2, precision=360):
    """
    NUEVA FUNCIÓN: Calcula la distancia mínima entre los perímetros de dos elipses
    """
    if hay_colision_mejorada(elipse1, elipse2):
        return 0.0  # Si hay colisión, la distancia mínima es 0
    
    distancia_minima = float('inf')
    
    # Generar puntos en el perímetro de la primera elipse
    for i in range(precision):
        angulo = 2 * pi * i / precision
        
        # Punto en elipse1
        if elipse1.orientacion == "horizontal":
            x1 = elipse1.h + elipse1.a * cos(angulo)
            y1 = elipse1.k + elipse1.b * sin(angulo)
        else:
            x1 = elipse1.h + elipse1.b * cos(angulo)
            y1 = elipse1.k + elipse1.a * sin(angulo)
        
        # Encontrar el punto más cercano en elipse2
        for j in range(precision):
            angulo2 = 2 * pi * j / precision
            
            # Punto en elipse2
            if elipse2.orientacion == "horizontal":
                x2 = elipse2.h + elipse2.a * cos(angulo2)
                y2 = elipse2.k + elipse2.b * sin(angulo2)
            else:
                x2 = elipse2.h + elipse2.b * cos(angulo2)
                y2 = elipse2.k + elipse2.a * sin(angulo2)
            
            # Calcular distancia entre puntos
            distancia = sqrt((x1 - x2)**2 + (y1 - y2)**2)
            
            if distancia < distancia_minima:
                distancia_minima = distancia
    
    return distancia_minima