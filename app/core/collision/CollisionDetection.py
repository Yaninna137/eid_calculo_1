from .DistanceCalculations import distancia_centros, distancia_punto_centro
from ..Math_ellipse import Elipse
from math import cos, sin, pi
import numpy as np

def punto_en_elipse(x: float, y: float, elipse: Elipse) -> bool:
    """
    Verifica si un punto (x, y) está dentro o sobre una elipse usando su ecuación canónica.
    Retorna True si el punto está dentro o en el borde de la elipse.
    """
    dx = x - elipse.h
    dy = y - elipse.k
    
    if elipse.orientacion == "horizontal":
        valor = (dx**2) / (elipse.a**2) + (dy**2) / (elipse.b**2)
    else:
        valor = (dx**2) / (elipse.b**2) + (dy**2) / (elipse.a**2)
    
    return valor <= 1.0

def punto_en_elipse_con_tolerancia(x: float, y: float, elipse: Elipse, tolerancia: float) -> bool:
    """
    Verifica si un punto está dentro de una elipse expandida por la tolerancia.
    """
    dx = x - elipse.h
    dy = y - elipse.k
    
    # Expandir la elipse por la tolerancia
    a_expandido = elipse.a + tolerancia
    b_expandido = elipse.b + tolerancia
    
    if elipse.orientacion == "horizontal":
        valor = (dx**2) / (a_expandido**2) + (dy**2) / (b_expandido**2)
    else:
        valor = (dx**2) / (b_expandido**2) + (dy**2) / (a_expandido**2)
    
    return valor <= 1.0

def hay_colision_mejorada(e1: Elipse, e2: Elipse, tolerancia: float = 0.1, precision: int = 500) -> bool:
    """
    Versión mejorada de detección de colisiones entre elipses.
    
    Algoritmo multi-etapa:
    1. Filtro rápido por distancia de centros
    2. Verificación de contención mutua
    3. Verificación de intersección de perímetros con alta precisión
    4. Verificación bidireccional punto-a-elipse
    """
    # Etapa 1: Filtro rápido por distancia
    distancia = distancia_centros(e1, e2)
    radio1_max = max(e1.a, e1.b)
    radio2_max = max(e2.a, e2.b)
    radio1_min = min(e1.a, e1.b)
    radio2_min = min(e2.a, e2.b)
    
    if distancia > (radio1_max + radio2_max + tolerancia):
        return False
    
    # Etapa 2: Verificar si una elipse está completamente dentro de la otra
    if distancia + radio1_max <= radio2_min or distancia + radio2_max <= radio1_min:
        return True
    
    # Etapa 3: Verificación de intersección con alta precisión
    puntos1 = generar_puntos_precision(e1, precision)
    puntos2 = generar_puntos_precision(e2, precision)
    
    for x, y in puntos1:
        if punto_en_elipse_con_tolerancia(x, y, e2, tolerancia):
            return True
    
    for x, y in puntos2:
        if punto_en_elipse_con_tolerancia(x, y, e1, tolerancia):
            return True
    
    # Etapa 4: Verificación adicional de puntos críticos
    puntos_criticos1 = obtener_puntos_extremos(e1)
    puntos_criticos2 = obtener_puntos_extremos(e2)
    
    for x, y in puntos_criticos1:
        if punto_en_elipse_con_tolerancia(x, y, e2, tolerancia):
            return True
    
    for x, y in puntos_criticos2:
        if punto_en_elipse_con_tolerancia(x, y, e1, tolerancia):
            return True
    
    return False

def generar_puntos_precision(elipse: Elipse, n: int) -> list:
    """
    Genera puntos sobre el perímetro de la elipse con distribución uniforme.
    """
    puntos = []
    
    for i in range(n):
        angulo = 2 * pi * i / n
        
        if elipse.orientacion == "horizontal":
            x = elipse.h + elipse.a * cos(angulo)
            y = elipse.k + elipse.b * sin(angulo)
        else:
            x = elipse.h + elipse.b * cos(angulo)
            y = elipse.k + elipse.a * sin(angulo)
        
        puntos.append((x, y))
    
    return puntos

def obtener_puntos_extremos(elipse: Elipse) -> list:
    """
    Obtiene los puntos extremos de la elipse (vértices).
    """
    puntos = []
    
    if elipse.orientacion == "horizontal":
        puntos.extend([
            (elipse.h + elipse.a, elipse.k),
            (elipse.h - elipse.a, elipse.k),
            (elipse.h, elipse.k + elipse.b),
            (elipse.h, elipse.k - elipse.b)
        ])
    else:
        puntos.extend([
            (elipse.h, elipse.k + elipse.a),
            (elipse.h, elipse.k - elipse.a),
            (elipse.h + elipse.b, elipse.k),
            (elipse.h - elipse.b, elipse.k)
        ])
    
    return puntos

def hay_colision(e1: Elipse, e2: Elipse, tolerancia: float = 0.1, dimensiones: int = 2) -> bool:
    """
    Función principal de detección de colisiones (mantiene compatibilidad).
    Utiliza el algoritmo mejorado por defecto.
    """
    return hay_colision_mejorada(e1, e2, tolerancia, precision=1000)

def hay_colision_3d(elipsoide1, elipsoide2):
    """Verifica colisión entre dos elipsoides (simplificado)."""
    distancia_centros = np.sqrt(
        (elipsoide1.h - elipsoide2.h)**2 +
        (elipsoide1.k - elipsoide2.k)**2 +
        (elipsoide1.l - elipsoide2.l)**2
    )
    return distancia_centros < (elipsoide1.a + elipsoide2.a)  # Radio mayor como aproximación