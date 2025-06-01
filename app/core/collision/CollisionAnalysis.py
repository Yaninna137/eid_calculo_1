from core.Math_ellipse import Elipse
from .CollisionDetection import hay_colision_mejorada
from .DistanceCalculations import distancia_centros

def tipo_colision(e1: Elipse, e2: Elipse, tolerancia: float = 0.1, dimensiones: int = 2) -> str:
    """
    Retorna un mensaje descriptivo sobre el tipo de colisión detectada.
    """
    if hay_colision_mejorada(e1, e2, tolerancia):
        distancia = distancia_centros(e1, e2)
        radio1_max = max(e1.a, e1.b)
        radio2_max = max(e2.a, e2.b)
        
        if distancia < abs(radio1_max - radio2_max):
            return "🔴 Colisión total - Una elipse está dentro de la otra"
        elif distancia < (radio1_max + radio2_max) * 0.5:
            return "🟡 Colisión parcial significativa"
        else:
            return "🟠 Colisión parcial menor"
    else:
        return "✅ Trayectorias seguras - Sin colisión"

def analizar_colision_detallada(e1: Elipse, e2: Elipse, tolerancia: float = 0.1) -> dict:
    """
    Proporciona un análisis detallado de la colisión entre dos elipses.
    """
    distancia = distancia_centros(e1, e2)
    radio1_max = max(e1.a, e1.b)
    radio2_max = max(e2.a, e2.b)
    
    colision = hay_colision_mejorada(e1, e2, tolerancia)
    
    resultado = {
        "hay_colision": colision,
        "distancia_centros": round(distancia, 4),
        "suma_radios_maximos": radio1_max + radio2_max,
        "diferencia_radios": abs(radio1_max - radio2_max),
        "porcentaje_solapamiento": 0,
        "tipo": tipo_colision(e1, e2, tolerancia)
    }
    
    if colision:
        if distancia < (radio1_max + radio2_max):
            solapamiento = (radio1_max + radio2_max - distancia) / (radio1_max + radio2_max)
            resultado["porcentaje_solapamiento"] = round(solapamiento * 100, 2)
    
    return resultado