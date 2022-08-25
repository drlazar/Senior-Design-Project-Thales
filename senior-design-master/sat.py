# -*- coding: utf-8 -*-

"""
a = semi-major axis
inc = inclination
ecc = eccentricity
tanom = true anomoly 

"""
import numpy as np

class Sat:
    def __init__(self, a, inc, ecc = 0, tanom = 0):
        self.a = a
        self.inc = inc
        self.ecc = ecc
        self.tanom = tanom
       
        
    # Orbital Radius to Center of Earth
    def radius(self):
        radius = self.a * (1 - self.ecc**2)
        radius = radius / (1 + self.ecc * np.cos(self.tanom))
        return radius
    
    # Converts True anomoly and inclination to latitude
    def lat(self):
        lat = np.arcsin(np.sin(self.tanom)*np.sin(self.inc))
        return lat
    
    # Converts True anomoly and inclination to longtitude
    def long(self):
        long = np.arctan(np.tan(self.tanom)*np.sin(self.inc))
        return long

"""        
#Test
sat1 = Sat(7, 30, 0, 30)
print(sat1.radius())

"""