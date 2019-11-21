import numpy as np
import matplotlib.pyplot as plt
from scipy import special as sp

class Space:
    def __init__(self, N_x, N_y, N_t, Delta_x, Delta_y, Delta_t):
        self.N_x = N_x
        self.N_y = N_y 
        self.N_t = N_t
        self.Delta_x = Delta_x
        self.Delta_y = Delta_y
        self.Delta_t = Delta_t

        # Initiating all field components with 0-value for all t
        self.E_z = np.zeros((N_x, N_y, N_t))
        self.H_x = np.zeros((N_x, N_y, N_t))
        self.H_y = np.zeros(())