# Importing necessary libraries and files
import numpy as np
import matplotlib.pyplot as plt
from scipy import special as sp

### Dielectric class
class Dielectric:
    ## Intialization function with all properties
    def __init__(self, pos_x, pos_y, width, height, eps_r):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.eps_r= eps_r

    ## String representation functions
    def __str__(self):
        return "x: {}, y: {}, w: {}, h: {}, eps_r: {}".format(self.pos_x,self.pos_y,self.width,self.height,self.eps_r)
    def __repr__(self):
        return self.__str__()
