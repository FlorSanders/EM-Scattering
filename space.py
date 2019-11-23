# Importing necessary libraries and files
import numpy as np
from constants import eps_0, mu_0
import source
import dielectric
import measurement

### Space class: Combines other classes to implement the FDTD algorithm
class Space:
    ## Initialize the space by giving its dimensions
    def __init__(self, x_length, y_length, t_length):
        # Initializing an empty list of dielectric things
        self.dielectrics = []

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
    def add_objects(self, dielectrics):
        self.dielectrics.append(dielectrics)

    ## Makes a discretized representation of the (inner) space with its dielectric properties (eps_r) at the measurement points of E_z
    def initialize_space(self, eps_averaging = True):
        # Initialize space with relative permittivity (eps_r) 1 everywhere (vacuum)
        self.space = np.ones((self.N_x - 1, self.N_y - 1))
        
        # Changing the relative permittivity according to position and size of our objects (assuming no overlap exists)
        for thing in self.dielectrics:
            # Discretizing given dimensions and positions
            i = int(thing.pos_x / self.Delta_x)
            j = int(thing.pos_y / self.Delta_y)
            x_length = int(thing.width / self.Delta_x)
            y_length = int(thing.height / self.Delta_y)
            
            # Changing the value for eps_r at that position
            self.space[i:i + x_length, j:j + y_length] = thing.eps_r

            # Problem: The edges of the dielectric and the measurement points of E_z coincide, so eps_r is not well defined in this point
            if(eps_averaging):
                # Default solution: We use the average value of eps_r of the surrounding regions at every point for E_z.
                self.space = (self.space[:self.N_x-2, :self.N_y-2] + self.space[1:, :self.N_y-2] + self.space[:self.N_x-2, 1:] + self.space[1:, 1:]) / 4
            else:
                # Alternative solution: We shift the dielectrics slightly (1/2 step left- and downward) so we don't need to average values out.
                self.space = self.space[:self.N_x-2, :self.N_y-2]

    ## Implementation of the FDTD method using the leapfrog scheme
    def FDTD(self, measurement_points, eps_averaging = True):
        # Initialize the dielectric properties of the space
        self.initialize_space(eps_averaging)
        
        # Calculating the discretized postions of our line source
        i_source = int(self.source.pos_x / self.Delta_x)
        j_source = int(self.source.pos_y / self.Delta_y)
        
        # Use the iterative update functions for our fields
        for n in range(1, self.N_t): 
            # 1: Update H_y
            self.H_y[:, :, n] = self.H_y[:, :, n - 1]
            self.H_y[:, :, n] += self.Delta_t / (mu_0 * self.Delta_x) * (self.E_z[1:, :, n - 1] - self.E_z[:-2, :, n - 1])
            
            # 2: Update H_x
            self.H_x[:, :, n] = self.H_x[:, :, n - 1]
            self.H_x[:, :, n] -= self.Delta_t / (mu_0 * self.Delta_y) * (self.E_z[:, 1:, n - 1] - self.E_z[:, :-2, n - 1])
            
            # 3: Update E_z (central space, edges = 0 as per boundary conditions)
            self.E_z[:, :, n] = self.E_z[:, :, n - 1] 
            self.E_z[1:-2, 1:-2, n] += self.Delta_t / (eps_0 * self.Delta_x) * np.divide((self.H_y[1:, 1:-2, n - 1] - self.H_y[:-2, 1:-2, n - 1]), self.space)
            self.E_z[1:-2, 1:-2, n] -= self.Delta_t / (eps_0 * self.Delta_y) * np.divide((self.H_x[1:-2, 1:, n - 1] - self.H_x[1:-2, :-2, n - 1]), self.space)
            self.E_z[i_source, j_source, n] -= self.source.get_current((n-1/2)*self.Delta_t) * self.Delta_t / (self.Delta_x * self.Delta_y * eps_0 * self.space[i_source, j_source])
        
        # Going over wanted measurement points, creating measurements and adding them to a list
        measurements = []
        for point in measurement_points:
            # Rescaling the locations to indices
            i, j = point[0]/self.Delta_x, point[1]/self.Delta_y
            # Making the discrete time arrays for H (offset by half a step) and E-measurements
            time_H = (np.range(self.N_t) + 1/2) * self.Delta_t
            time_E = np.range(self.N_t) * self.Delta_t
            # Slicing our matrix to obtain correct measurements (Lower bound approximation to our indices)
            H_x = self.H_x[int(i), int(j), :]
            H_y = self.H_y[int(i + 1/2), int(j + 1/2), :]
            E_z = self.E_z[int(i + 1/2), int(j + 1/2), :]
            measure = measurement.Measurement(point[0], point[1], time_H, time_E, H_x, H_y, E_z)
            measurements.append(measure)
        # Returning the list of measurements
        return measurements