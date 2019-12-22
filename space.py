# Importing necessary libraries and files
import numpy as np
# import matplotlib.pyplot as plt
from constants import eps_0, mu_0, c
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
        self.N_x = int(self.x_length / Delta_x + 1)
        self.N_y = int(self.y_length / Delta_y + 1)
        self.N_t = int(self.t_length / Delta_t) # t_length not inclusive

        # Initializing zero-valued fields of the correct size (as 3D numpy array)
        # E_z field at the corners of our discretized blocks
        self.E_z = np.zeros((self.N_x, self.N_y))
        # H_x and H_y fields on the edges of the discretized blocks
        self.H_x = np.zeros((self.N_x, self.N_y - 1))
        self.H_y = np.zeros((self.N_x - 1, self.N_y))

    ## Set the line source of our space
    def set_source(self, source):
        self.source = source

    ## Add a list of dielectric options to the space
    def add_objects(self, dielectrics):
        self.dielectrics.extend(dielectrics)

    ## Add a list of measurement point in the form of: [(x,y), ...], as well as optional titles for the measurements
    def add_measurement_points(self, measurement_points, measurement_titles = []):
        # Make a list of empty titles if no titles were given
        if(len(measurement_titles) == 0):
            measurement_titles = [""]*len(measurement_points)
        # list of tuples
        self.measurement_points = np.empty(len(measurement_points), dtype=measurement.Measurement)
        self.interference_times = np.empty(len(measurement_points))
        for i, meas in enumerate(measurement_points):
            # reflecting on the PEC walls
            # dist : the 4 reflection points of measurement in the PEC
            dist = np.empty((4,2))
            dist[0,:] = -meas[0],meas[1]
            dist[1,:] = meas[0],-meas[1]
            dist[2,:] = 2*self.x_length - meas[0], meas[1]
            dist[3,:] = meas[0],2*self.y_length - meas[1]
            dist -= (self.source.pos_x, self.source.pos_y)
            # euclidian distance
            dist = np.linalg.norm(dist,axis=-1)
            # the least distance between the source & the reflection point of
            # the measurement will be approx the distance the wave has to
            # travel
            min_dist = np.min(dist)
            # set interference
            self.interference_times[i] = min_dist/c
            self.measurement_points[i] = measurement.Measurement(meas[0],meas[1], self.interference_times[i], measurement_titles[i])
        # return an estimate maximum of time before inteference occurs (foreach meas_point)
        return self.interference_times

    ## Makes a discretized representation of the (inner) space with its dielectric properties (eps_r) at the measurement points of E_z
    def initialize_space(self, eps_averaging = True, plot_space = True):
        # Initialize space with relative permittivity (eps_r) 1 everywhere (vacuum)
        self.space = np.ones((self.N_x - 1, self.N_y - 1))

        # Changing the relative permittivity according to position and size of our objects (assuming no overlap exists)
        for dielectric in self.dielectrics:
            # Discretizing given dimensions and positions
            i = int(dielectric.pos_x / self.Delta_x)
            j = int(dielectric.pos_y / self.Delta_y)
            x_length = int(dielectric.width / self.Delta_x)
            y_length = int(dielectric.height / self.Delta_y)

            # Changing the value for eps_r at that position
            self.space[i:i + x_length, j:j + y_length] = dielectric.eps_r
        # Problem: The edges of the dielectric and the measurement points of E_z coincide, so eps_r is not well defined in this point
        if(eps_averaging):
            # Default solution: We use the average value of eps_r of the surrounding regions at every point for E_z.
            self.space = (self.space[:-1, :-1] + self.space[1:, :-1] + self.space[:-1, 1:] + self.space[1:, 1:]) / 4
        else:
            # Alternative solution: We shift the dielectrics slightly (1/2 step left- and downward) so we don't need to average values out.
            self.space = self.space[:-1, :-1]

        # Visualizing our space using a plot
        if(plot_space):
            measurement.field_plot(self.space, "i", "j", "Visualisatie van de ruimte")

    ## Implementation of the FDTD method using the leapfrog scheme
    def FDTD(self, eps_averaging = True, plot_space = False, visualize_fields = 0):
        # Initialize the dielectric properties of the space
        self.initialize_space(eps_averaging, plot_space)
        # Making the discrete time arrays for H (offset by half a step) and E-measurements
        time_H = (np.arange(self.N_t) + 1/2) * self.Delta_t
        time_E = np.arange(self.N_t) * self.Delta_t
        for meas in self.measurement_points:
            # Adding the time arrays to our measurements
            meas.set_time(time_H, time_E)
            meas.append_fields(0,0,0)
        # Returning the list of measurements

        # Calculating the discretized postions of our line source
        i_source = int(self.source.pos_x / self.Delta_x)
        j_source = int(self.source.pos_y / self.Delta_y)

        # Use the iterative update functions for our fields
        for n in range(1, self.N_t):
            # 1: Update H_y
            self.H_y[:, :] += self.Delta_t / (mu_0 * self.Delta_x) * (self.E_z[1:, :] - self.E_z[:-1, :])

            # 2: Update H_x
            self.H_x[:, :] -= self.Delta_t / (mu_0 * self.Delta_y) * (self.E_z[:, 1:] - self.E_z[:, :-1])

            # 3: Update E_z (inner space, edges = 0 as per boundary conditions)
            self.E_z[1:-1, 1:-1] += self.Delta_t / (eps_0 * self.Delta_x) * (self.H_y[1:, 1:-1] - self.H_y[:-1, 1:-1]) / self.space
            self.E_z[1:-1, 1:-1] -= self.Delta_t / (eps_0 * self.Delta_y) * (self.H_x[1:-1, 1:] - self.H_x[1:-1, :-1]) / self.space
            self.E_z[i_source, j_source] -= self.source.get_current((n-1/2)*self.Delta_t) * self.Delta_t / (self.Delta_x * self.Delta_y * eps_0 * self.space[i_source, j_source])

            # 4: Saving measurements
            for meas in self.measurement_points:
                # Rescaling the locations to indices
                i, j = int(meas.pos_x/self.Delta_x), int(meas.pos_y/self.Delta_y)
                H_x = self.H_x[i, j]
                H_y = self.H_y[i, j]
                E_z = self.E_z[i, j]
                meas.append_fields(H_x, H_y, E_z)

            # If requested, a periodic visualisation of the space is given
            if(visualize_fields != 0 and n % visualize_fields == 0):
                print(n*self.Delta_t)
                measurement.field_plot(abs(self.E_z), "i", "j", "E_z")
                measurement.field_plot(np.sqrt(self.H_x[1:,]**2 + self.H_y[:,1:]**2), "i", "j", "H")      

        # Getting measurements
        return self.measurement_points
    
    ## String representation function for our box-space
    def __str__(self):
        s = "Box parameters: {} m, {} m, {} s\n".format(self.x_length, self.y_length, self.t_length)
        s += "Discretization: {} m, {} m, {} s\n".format(self.Delta_x, self.Delta_y, self.Delta_t)
        s += str(self.source) + "\n"
        s += "Dielectrics ({}):\n".format(len(self.dielectrics))
        for diel in self.dielectrics:
            s+= str(diel) + "\n"
        return s
