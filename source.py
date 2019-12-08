# Importing scientific libraries to make our lives easier
import numpy as np
from constants import c, simulation_speed_factor

class Source:
    def __init__(self, pos_x, pos_y, J0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.J0 = J0

class Gaussian_pulse(Source):
    def __init__(self, pos_x, pos_y, J0, tc, sigma):
        super().__init__(pos_x, pos_y, J0)
        self.tc = tc
        self.sigma = sigma

    def get_current(self,t)    :
        return self.J0*np.exp(-(t-self.tc)**2/(2*self.sigma**2))

    def get_lambda_min(self,eps_r):
        v_min = c/np.sqrt(eps_r)
        omega_max = 3/self.sigma * simulation_speed_factor
        return 2*np.pi * v_min / omega_max

class Gaussian_modulated_rf_pulse(Source):
    def __init__(self, pos_x, pos_y, J0, tc, sigma, omega_c):
        super().__init__(pos_x, pos_y, J0)
        self.omega_c = omega_c
        self.tc = tc
        self.sigma = sigma

    def get_current(self,t):
        return self.J0*np.exp(-(t-self.tc)**2/(2*self.sigma**2))*np.sin(self.omega_c*t)

    def get_lambda_min(self,eps_r):
        v_min = c / np.sqrt(eps_r)
        # Gaussian + freq shift sinus
        omega_max = 3 / self.sigma * simulation_speed_factor + self.omega_c
        return 2 * np.pi * v_min / omega_max

class Sine_source(Source):
    def __init__(self, pos_x, pos_y, J0, omega_c):
        super().__init__(pos_x, pos_y, J0)
        self.omega_c = omega_c

    def get_current(self,t):
        return self.J0*np.sin(self.omega_c*t)

    def get_lambda_min(self, eps_r):
        v_min = c / np.sqrt(eps_r)
        return 2 * np.pi * v_min / self.omega_c
