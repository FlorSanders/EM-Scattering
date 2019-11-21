import numpy as np
import matplotlib.pyplot as plt
from scipy import special as sp

eps_0 = 8.854 * 10**(-12)
mu_0 = 4 * np.pi *  10**(-7)

class Space:
    ## Initialize the space by giving its dimensions
    def __init__(self, x_length, y_length, t_length, Delta_x, Delta_y, Delta_t):
        # Initializing an empty list of dielectric things
        self.things = []
        
        # Saving the given dimensions of our space
        self.x_length = x_length
        self.y_length = y_length
        self.t_length = t_length
    
    ## Define discretization and initialize zero-valued fields 
    def define_discretization(self, Delta_x, Delta_y, Delta_t):
        # Saving the given discretization steps 
        self.Delta_x = Delta_x
        self.Delta_y = Delta_y
        self.Delta_t = Delta_t

        # Calculating the amount of space/time indices
        self.N_x = int(self.x_length / Delta_x)
        self.N_y = int(self.y_length / Delta_y)
        self.N_t = int(self.t_length / Delta_t)

        # Initializing zero-valued fields of the correct size (as 3D numpy array)
        # E_z field at the corners of our discretized blocks
        self.E_z = np.zeros((self.N_x, self.N_y, self.N_t))
        # H_x and H_y fields on the edges of the discretized blocks
        self.H_x = np.zeros((self.N_x, self.N_y - 1, self.N_t))
        self.H_y = np.zeros((self.N_x - 1, self.N_y, self.N_t))
    
    ## Set the line source of our space
    def set_source(self, source):
        self.source = source
    
    ## Add a list of dielectric options to the space
    def add_objects(self, things):
        self.things.append(things)

    ## Makes a discretized representation of the space properties and sources in it
    def initialize_space(self):
        # Initializing a space where everything is 0 (level 1 = eps_r, level_2 = I)
        self.space = np.zeros((self.Nx-1, self.Ny-1, 2))
        # Setting the whole bottom layer to 1 (default: eps_r = 1)
        self.space[0,:,:] = 1
        # Changing the relative permittivity according to position and size of our objects (assuming no overlap exists)
        for thing in self.things:
            i = int(thing.pos_x / Delta_x)
            j = int(thing.pos_x / Delta_y)
            self.space[0:thing.pos_x]
