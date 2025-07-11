# core/elipse.py
"""
Archivo de lógica matemática para el cálculo de una elipse central:
- Ecuación canónica
- Ecuación general
- Área
- Cálculo de puntos sobre la elipse
- Generación de elipse a partir del RUT

OPTIMIZADO: Usa funciones matemáticas nativas de Python
"""

from dataclasses import dataclass
from math import cos, sin, pi

@dataclass
class Elipse:
    h: int
    k: int
    a: int
    b: int
    orientacion: str  # 'horizontal' o 'vertical'

    def __post_init__(self):
        if self.a == 0 and self.b == 0:
            raise ValueError("No es posible evualuar porque a y b son 0")
        if self.a == 0:
            raise ValueError("No es posible evaluar porque a es 0 ")
        if self.b == 0:
            raise ValueError("No es posible evaluar porque b es 0")
        if self.a < 0 or self.b < 0:
            raise ValueError("Los valores de 'a' y 'b' deben ser positivos.")

    def ecuacion_canonica(self):
        if self.orientacion == "horizontal":
            return f"\\frac{{(x - {self.h})^2}}{{{self.a ** 2}}} + \\frac{{(y - {self.k})^2}}{{{self.b ** 2}}} = 1"  # Formato latex
        else:
            return f"\\frac{{(x - {self.h})^2}}{{{self.b ** 2}}} + \\frac{{(y - {self.k})^2}}{{{self.a ** 2}}} = 1"  # Formato latex

    def ecuacion_general(self):
        a2 = self.a ** 2
        b2 = self.b ** 2
        h_exp2 = self.h ** 2 # Calculo de h^2  del binomio cuadrado (x - h)^2 
        k_exp2 = self.k ** 2 # Calculo de k^2  => del binomio cuadrado (y - k)^2 

        if self.orientacion == "horizontal":
            A = b2
            C = a2
        else:
            A = a2
            C = b2

        D = -2 * A * self.h
        E = -2 * C * self.k
        F = ((A * h_exp2) + (C * k_exp2))- (A * C)
        
        # Armar la ecuación
        partes = []
        if A != 0: partes.append(f"{A}x²")
        if C != 0: partes.append(f"{'+' if C > 0 else '-'} {C}y²")
        if D != 0: partes.append(f"{'+' if D > 0 else '-'} {abs(D)}x")
        if E != 0: partes.append(f"{'+' if E > 0 else '-'} {abs(E)}y")
        if F != 0: partes.append(f"{'+' if F > 0 else '-'} {abs(F)}")

        return " ".join(partes) + " = 0"
    
    def calcular_puntos(self, n=100):
        """
        OPTIMIZADO: Usa sin y cos para mejor rendimiento
        """
        puntos = []
        for i in range(n):
            angulo = 2 * pi * i / n
            if self.orientacion == "horizontal":
                x = self.h + self.a * cos(angulo)
                y = self.k + self.b * sin(angulo)
            else:
                x = self.h + self.b * cos(angulo)
                y = self.k + self.a * sin(angulo)
            puntos.append((x, y))
        return puntos

def generar_elipse_desde_rut(rut: str, grupo_impar=True) -> Elipse:
    """
    Genera una elipse a partir de los primeros 8 dígitos del RUT,
    siguiendo las reglas del proyecto MAT1186.
    """
    digitos = [int(c) for c in rut if c.isdigit()]
    if len(digitos) < 8:
        raise ValueError("El RUT debe tener al menos 8 dígitos.")

    # Tomar solo los primeros 8
    digitos = digitos[:8]

    h, k = digitos[0], digitos[1]

    if grupo_impar:
        a_raw = digitos[2] + digitos[3]
        b_raw = digitos[4] + digitos[5]
        orientacion = "horizontal" if digitos[7] % 2 == 0 else "vertical"
    else:
        a_raw = digitos[5] + digitos[6]
        b_raw = digitos[7] + digitos[2]
        orientacion = "horizontal" if digitos[3] % 2 == 0 else "vertical"
    
    # Asegurar que a sea mayor o igual que b
    a, b = sorted([a_raw, b_raw], reverse=True)
    return Elipse(h, k, a, b, orientacion)