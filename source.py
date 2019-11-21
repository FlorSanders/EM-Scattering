import numpy as np
import matplotlib.pyplot as plt
from scipy import special as sp

def gaussian_pulse(t, J0, tc, sigma):
    return J0*np.exp(-(t-tc)**2/(2*sigma**2))

def gaussian_modulated_rf_pulse(t, J0, tc, sigma, omega_c):
    return gaussian_pulse(t, J0, tc, sigma)*np.sin(omega_c*t)