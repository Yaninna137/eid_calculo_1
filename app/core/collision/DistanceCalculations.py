from core.Math_ellipse import Elipse
from math import sqrt, cos, sin, pi

def distancia_centros(e1: Elipse, e2: Elipse, dimensiones: int = 2) -> float:
    """
    Calcula la distancia euclidiana entre los centros de dos elipses.
    """
    dx = e1.h - e2.h
    dy = e1.k - e2.k
    
    if dimensiones == 3:
        dz = getattr(e1, 'z', 0) - getattr(e2, 'z', 0)
        return sqrt(dx**2 + dy**2 + dz**2)
    
    return sqrt(dx**2 + dy**2)

def distancia_punto_centro(x: float, y: float, elipse: Elipse) -> float:
    """
    Calcula la distancia desde un punto hasta el centro de la elipse.
    """
    return sqrt((x - elipse.h)**2 + (y - elipse.k)**2)

def punto_mas_cercano_en_elipse(x: float, y: float, elipse: Elipse) -> tuple:
    """
    Encuentra el punto más cercano en el perímetro de la elipse a un punto dado.
    Utiliza búsqueda binaria para encontrar el ángulo óptimo.
    """
    mejor_distancia = float('inf')
    mejor_punto = None
    
    # Búsqueda gruesa inicial
    for i in range(360):
        angulo = i * pi / 180
        
        if elipse.orientacion == "horizontal":
            px = elipse.h + elipse.a * cos(angulo)
            py = elipse.k + elipse.b * sin(angulo)
        else:
            px = elipse.h + elipse.b * cos(angulo)
            py = elipse.k + elipse.a * sin(angulo)
        
        distancia = sqrt((x - px)**2 + (y - py)**2)
        
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_punto = (px, py)
    
    return mejor_punto