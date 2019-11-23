import numpy as np
import matplotlib.pyplot as plt
from scipy import special as sp
import constants as cst

class Source:

    def __init__(self, pos_x, pos_y, J0, tc, sigma):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.J0 = J0
        self.tc = tc
        self.sigma = sigma

    def get_lambda_min(self,eps_r):
        v_min = cst.c/np.sqrt(eps_r)
        omega_max = 3/self.sigma * cst.simulation_speed_factor
        return 2*np.pi * v_min / omega_max


class gaussian_pulse(Source):
    def __init__(self, pos_x, pos_y, J0, tc, sigma):
        super().__init__(pos_x, pos_y, J0, tc, sigma)

    def get_current(self,t)    :
        return self.J0*np.exp(-(t-self.tc)**2/(2*self.sigma**2))

class gaussian_modulated_rf_pulse(Source):
    def __init__(self, pos_x, pos_y, J0, tc, sigma, omega_c):
        super().__init__(pos_x, pos_y, J0, tc, sigma)
        self.omega_c = omega_c

    def get_current(self,t):
        return self.J0*np.exp(-(t-self.tc)**2/(2*self.sigma**2))*np.sin(self.omega_c*t)
