# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 16:56:21 2020

@author: amendelsohn_local
"""
import math
import numpy
import sat


        
class Grdstation:
    def __init__(self, lat, long):
        self.long = long
        self.lat = lat
        
class Link:
    def __init__(self, Sat, Grdstation):
        self.sat = Sat
        self.grd = Grdstation


    def distance(self):
        

        r_e = 6378 # radius of earth
        
        # Convert from degrees to radian for Grd
        phi_grd = math.radians(90 - self.grd.lat)
        theta_grd = math.radians(self.grd.long)
        
        # Convert from degrees to radian for Sat
        phi_sat = math.radians(90 - self.sat.lat())
        theta_sat = math.radians(self.sat.long())
        
        """
        # Test code
        print(phi_sat, " ", theta_sat)
        print(phi_grd, " ", theta_grd)
        
        """
        
        # Convert Spherical to Cartesian for grd
        x_grd = r_e * math.sin(phi_grd) * math.cos(theta_grd)
        y_grd = r_e * math.sin(phi_grd) * math.sin(theta_grd)
        z_grd = r_e * math.cos(phi_grd)
        
        # Convert Spherical to Cartesian for sat
        r_sat = r_e + self.sat.a
        x_sat = r_sat * math.sin(phi_sat) * math.cos(theta_sat)
        y_sat = r_sat * math.sin(phi_sat) * math.sin(theta_sat)
        z_sat = r_sat * math.cos(phi_sat)
        
        # Find the squared differences
        x_sqdif = (x_grd - x_sat)**2
        y_sqdif = (y_grd - y_sat)**2
        z_sqdif = (z_grd - z_sat)**2
        
        # Distance 
        dist = math.sqrt(x_sqdif + y_sqdif + z_sqdif)
        return dist







