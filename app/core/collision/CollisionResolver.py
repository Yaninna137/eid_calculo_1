# core/collision/CollisionResolver.py
"""
Algoritmos para resolución automática de colisiones entre elipses
"""
from core.Math_ellipse import Elipse
from core.collision.CollisionDetection import hay_colision_mejorada, distancia_centros
from math import sqrt

def resolver_colisiones_automatico(elipses: list, max_iter=100, factor_ajuste=0.3, margen_seguridad=1.1):
    """
    Algoritmo mejorado para resolver colisiones entre múltiples elipses
    """
    if len(elipses) < 2:
        return elipses
    
    # Crear copias de las elipses para trabajar
    elipses_ajustadas = [Elipse(e.h, e.k, e.a, e.b, e.orientacion) for e in elipses]
    
    for iteracion in range(max_iter):
        colisiones_detectadas = 0
        
        # Primera pasada: detectar todas las colisiones
        pares_en_colision = []
        for i in range(len(elipses_ajustadas)):
            for j in range(i + 1, len(elipses_ajustadas)):
                if hay_colision_mejorada(elipses_ajustadas[i], elipses_ajustadas[j]):
                    pares_en_colision.append((i, j))
                    colisiones_detectadas += 1
        
        # Si no hay colisiones, terminar
        if colisiones_detectadas == 0:
            break
        
        # Segunda pasada: resolver colisiones con un factor de ajuste adaptativo
        factor_actual = factor_ajuste * (1 + iteracion / max_iter)  # Aumenta gradualmente
        
        for i, j in pares_en_colision:
            separar_elipses(
                elipses_ajustadas[i], 
                elipses_ajustadas[j], 
                factor_actual,
                margen_seguridad
            )
    
    return elipses_ajustadas

def separar_elipses(elipse1: Elipse, elipse2: Elipse, factor=0.3, margen_seguridad=1.1):
    """
    Separa dos elipses en colisión con un margen de seguridad
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
    
    # Calcular distancia mínima necesaria con margen de seguridad
    radio_efectivo_1 = max(elipse1.a, elipse1.b) * margen_seguridad
    radio_efectivo_2 = max(elipse2.a, elipse2.b) * margen_seguridad
    distancia_minima = radio_efectivo_1 + radio_efectivo_2
    
    # Normalizar el vector de dirección
    dx_norm = dx / distancia_actual
    dy_norm = dy / distancia_actual
    
    # Calcular movimiento necesario
    movimiento_necesario = max(0, (distancia_minima - distancia_actual)) * factor
    
    # Aplicar movimiento
    movimiento_x = dx_norm * movimiento_necesario
    movimiento_y = dy_norm * movimiento_necesario
    
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