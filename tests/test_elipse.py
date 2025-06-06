'''
# Tests unitarios para elipse 
'''
from app.core.Math_ellipse import Elipse
from math import pi
def test_area():
    e = Elipse(0, 0, 3, 2, "horizontal")
    assert abs(e.area() - (pi * 3 * 2)) < 0.01
