# core/collision/CollisionResolver.py
"""
Algoritmos para resolución automática de colisiones entre elipses
"""
from core.Math_ellipse import Elipse
from core.collision.CollisionDetection import hay_colision_mejorada, distancia_centros
from math import sqrt

def resolver_colisiones_automatico(elipses: list, max_iter=50, factor_ajuste=0.1):
    """
    Algoritmo principal para resolver colisiones entre múltiples elipses
    usando separación gradual de centros
    """
    if len(elipses) < 2:
        return elipses
    
    elipses_ajustadas = [Elipse(e.h, e.k, e.a, e.b, e.orientacion) for e in elipses]
    
    for iteracion in range(max_iter):
        colisiones_resueltas = True
        
        for i in range(len(elipses_ajustadas)):
            for j in range(i + 1, len(elipses_ajustadas)):
                if hay_colision_mejorada(elipses_ajustadas[i], elipses_ajustadas[j]):
                    colisiones_resueltas = False
                    separar_elipses(elipses_ajustadas[i], elipses_ajustadas[j], factor_ajuste)
        
        if colisiones_resueltas:
            break
    
    return elipses_ajustadas

def separar_elipses(elipse1: Elipse, elipse2: Elipse, factor=0.1):
    """
    Separa dos elipses en colisión moviendo sus centros
    """
    # Calcular vector de separación
    dx = elipse2.h - elipse1.h
    dy = elipse2.k - elipse1.k
    
    # Distancia actual entre centros
    distancia_actual = distancia_centros(elipse1, elipse2)
    
    # Si los centros coinciden, crear separación artificial
    if distancia_actual == 0:
        dx, dy = 1.0, 0.0
        distancia_actual = 1.0
    
    # Calcular distancia mínima necesaria
    radio_efectivo_1 = (elipse1.a + elipse1.b) / 2
    radio_efectivo_2 = (elipse2.a + elipse2.b) / 2
    distancia_minima = (radio_efectivo_1 + radio_efectivo_2) * 1.1  # 10% de margen
    
    # Si ya están suficientemente separados, no hacer nada
    if distancia_actual >= distancia_minima:
        return
    
    # Calcular cuánto mover cada elipse
    movimiento_necesario = (distancia_minima - distancia_actual) / 2
    
    # Normalizar el vector de dirección
    dx_norm = dx / distancia_actual
    dy_norm = dy / distancia_actual
    
    # Aplicar movimiento con factor de ajuste
    movimiento_x = dx_norm * movimiento_necesario * factor
    movimiento_y = dy_norm * movimiento_necesario * factor
    
    # Mover las elipses en direcciones opuestas
    elipse1.h -= movimiento_x
    elipse1.k -= movimiento_y
    elipse2.h += movimiento_x
    elipse2.k += movimiento_y

def verificar_resolucion(elipses: list):
    """
    Verifica si todas las colisiones han sido resueltas
    """
    for i in range(len(elipses)):
        for j in range(i + 1, len(elipses)):
            if hay_colision_mejorada(elipses[i], elipses[j]):
                return False
    return True

def obtener_estadisticas_resolucion(elipses_originales: list, elipses_resueltas: list):
    """
    Calcula estadísticas sobre el proceso de resolución
    """
    if len(elipses_originales) != len(elipses_resueltas):
        return None
    
    desplazamientos = []
    for orig, res in zip(elipses_originales, elipses_resueltas):
        desplazamiento = sqrt((orig.h - res.h)**2 + (orig.k - res.k)**2)
        desplazamientos.append(desplazamiento)
    
    return {
        'desplazamiento_promedio': sum(desplazamientos) / len(desplazamientos),
        'desplazamiento_maximo': max(desplazamientos),
        'desplazamiento_minimo': min(desplazamientos),
        'colisiones_resueltas': verificar_resolucion(elipses_resueltas)
    }