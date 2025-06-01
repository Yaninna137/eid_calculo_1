"""
Módulo de detección y análisis de colisiones entre elipses.

Este paquete proporciona funcionalidades para:
- Detectar colisiones entre elipses
- Analizar tipos de colisión
- Calcular distancias relacionadas
"""

# Importa las funciones principales para exponerlas en el espacio de nombres del paquete
from .CollisionDetection import (
    hay_colision,
    hay_colision_mejorada,
    punto_en_elipse,
    punto_en_elipse_con_tolerancia
)

from .DistanceCalculations import (
    distancia_centros,
    distancia_punto_centro,
    punto_mas_cercano_en_elipse
)

from .CollisionAnalysis import (
    tipo_colision,
    analizar_colision_detallada
)

# Define qué se exporta cuando se usa 'from core.collision import *'
__all__ = [
    'hay_colision',
    'hay_colision_mejorada',
    'punto_en_elipse',
    'punto_en_elipse_con_tolerancia',
    'distancia_centros',
    'distancia_punto_centro',
    'punto_mas_cercano_en_elipse',
    'tipo_colision',
    'analizar_colision_detallada'
]

# Versión del paquete
__version__ = '1.0.0'