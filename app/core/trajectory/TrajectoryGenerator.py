# core/trajectory/TrajectoryGenerator.py
"""
Módulo para generar trayectorias seguras evitando colisiones
"""
from math import cos, sin, pi, sqrt
from core.Math_ellipse import Elipse
from core.collision.CollisionDetection import hay_colision_mejorada, punto_dentro_de_elipse

def generar_trayectoria_eliptica_segura(elipse_dron: Elipse, elipses_obstaculos: list, puntos=100, margen_seguridad=1.2):
    """
    Genera una trayectoria siguiendo el perímetro de la elipse del dron,
    ajustándola para evitar colisiones con obstáculos
    """
    trayectoria_original = elipse_dron.calcular_puntos(n=puntos)
    trayectoria_segura = []
    
    for x, y in trayectoria_original:
        punto_ajustado = ajustar_punto_seguro(x, y, elipses_obstaculos, margen_seguridad)
        trayectoria_segura.append(punto_ajustado)
    
    return trayectoria_segura

def ajustar_punto_seguro(x, y, elipses_obstaculos, margen_seguridad=1.2, max_intentos=20):
    """
    Ajusta un punto para que no esté dentro de ninguna elipse obstáculo
    """
    # Verificar si el punto original es seguro
    if es_punto_seguro(x, y, elipses_obstaculos, margen_seguridad):
        return (x, y)
    
    # Si no es seguro, buscar el punto seguro más cercano
    mejor_punto = (x, y)
    mejor_distancia = float('inf')
    
    # Probar en diferentes direcciones radiales
    for i in range(max_intentos):
        angulo = 2 * pi * i / max_intentos
        
        # Probar diferentes distancias
        for distancia in [0.5, 1.0, 1.5, 2.0, 3.0]:
            x_test = x + distancia * cos(angulo)
            y_test = y + distancia * sin(angulo)
            
            if es_punto_seguro(x_test, y_test, elipses_obstaculos, margen_seguridad):
                dist_original = sqrt((x - x_test)**2 + (y - y_test)**2)
                if dist_original < mejor_distancia:
                    mejor_distancia = dist_original
                    mejor_punto = (x_test, y_test)
                break
    
    return mejor_punto

def es_punto_seguro(x, y, elipses_obstaculos, margen_seguridad=1.2):
    """
    Verifica si un punto está a una distancia segura de todas las elipses obstáculo
    """
    for elipse in elipses_obstaculos:
        # Crear una elipse expandida para el margen de seguridad
        elipse_expandida = Elipse(
            elipse.h, elipse.k,
            elipse.a * margen_seguridad,
            elipse.b * margen_seguridad,
            elipse.orientacion
        )
        
        if punto_dentro_de_elipse(x, y, elipse_expandida):
            return False
    
    return True

def generar_trayectoria_punto_a_punto(punto_inicio, punto_fin, elipses_obstaculos, pasos=50):
    """
    Genera una trayectoria directa entre dos puntos evitando obstáculos
    """
    # Trayectoria directa inicial
    trayectoria_directa = interpolar_puntos(punto_inicio, punto_fin, pasos)
    
    # Ajustar cada punto para evitar colisiones
    trayectoria_segura = []
    for punto in trayectoria_directa:
        punto_seguro = ajustar_punto_seguro(punto[0], punto[1], elipses_obstaculos)
        trayectoria_segura.append(punto_seguro)
    
    return trayectoria_segura

def interpolar_puntos(punto_inicio, punto_fin, pasos):
    """
    Interpola linealmente entre dos puntos
    """
    x1, y1 = punto_inicio
    x2, y2 = punto_fin
    
    puntos = []
    for i in range(pasos + 1):
        t = i / pasos
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        puntos.append((x, y))
    
    return puntos

def calcular_longitud_trayectoria(trayectoria):
    """
    Calcula la longitud total de una trayectoria
    """
    if len(trayectoria) < 2:
        return 0.0
    
    longitud = 0.0
    for i in range(len(trayectoria) - 1):
        x1, y1 = trayectoria[i]
        x2, y2 = trayectoria[i + 1]
        longitud += sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    return longitud

def optimizar_trayectoria_simple(trayectoria, elipses_obstaculos, max_iter=10):
    """
    Optimización simple de trayectoria reduciendo puntos innecesarios
    """
    if len(trayectoria) < 3:
        return trayectoria
    
    trayectoria_optimizada = [trayectoria[0]]  # Siempre incluir el primer punto
    
    for _ in range(max_iter):
        i = 1
        while i < len(trayectoria) - 1:
            # Intentar conectar directamente puntos no consecutivos
            punto_actual = trayectoria_optimizada[-1]
            j = i + 1
            
            # Buscar el punto más lejano que se puede conectar directamente
            while j < len(trayectoria):
                if puede_conectar_directamente(punto_actual, trayectoria[j], elipses_obstaculos):
                    j += 1
                else:
                    break
            
            # Agregar el último punto válido
            if j - 1 > i:
                trayectoria_optimizada.append(trayectoria[j - 1])
                i = j - 1
            else:
                trayectoria_optimizada.append(trayectoria[i])
                i += 1
    
    # Siempre incluir el último punto
    if trayectoria_optimizada[-1] != trayectoria[-1]:
        trayectoria_optimizada.append(trayectoria[-1])
    
    return trayectoria_optimizada

def puede_conectar_directamente(punto1, punto2, elipses_obstaculos, pasos_verificacion=20):
    """
    Verifica si dos puntos se pueden conectar directamente sin colisiones
    """
    puntos_intermedios = interpolar_puntos(punto1, punto2, pasos_verificacion)
    
    for punto in puntos_intermedios:
        if not es_punto_seguro(punto[0], punto[1], elipses_obstaculos):
            return False
    
    return True