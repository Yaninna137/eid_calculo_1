'''
 # Tests para colisión

'''
from app.core.Math_ellipse import Elipse
from app.core.collision.CollisionDetection import hay_colision, analizar_colision_detallada

def test_precision_colision():
    """
    Función de prueba para verificar la precisión del algoritmo.
    """
    # Test case 1: Elipses que se tocan apenas
    e1 = Elipse(0, 0, 5, 3, "horizontal")
    e2 = Elipse(7, 0, 3, 2, "horizontal")
    
    print(f"Test 1 - Elipses que se tocan: {hay_colision(e1, e2, tolerancia=0.5)}")
    print(f"Análisis detallado: {analizar_colision_detallada(e1, e2)}")
    
    # Test case 2: Elipses completamente separadas
    e3 = Elipse(0, 0, 2, 1, "horizontal")
    e4 = Elipse(10, 10, 2, 1, "horizontal")
    
    print(f"Test 2 - Elipses separadas: {hay_colision(e3, e4)}")
    
    # Test case 3: Elipses superpuestas
    e5 = Elipse(0, 0, 4, 3, "horizontal")
    e6 = Elipse(2, 1, 3, 2, "vertical")
    
    print(f"Test 3 - Elipses superpuestas: {hay_colision(e5, e6)}")
    print(f"Análisis detallado: {analizar_colision_detallada(e5, e6)}")