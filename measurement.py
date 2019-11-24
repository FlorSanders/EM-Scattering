# Importing necessary libraries and files
import numpy as np
import matplotlib.pyplot as plt

### Simple plotting function taking care of matplotlib syntax
def plot(x_values, y_values, x_title, y_title, title):
    plt.plot(x_values, y_values, color='black', marker='o')
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.show()

### Measurement class: Combine all measurement data for a certain point into a single callable instance
class Measurement:
    ## Initialization with all measurement data 
    def __init__(self, pos_x, pos_y, time_H, time_E, H_x, H_y, E_z):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.time_H = time_H
        self.time_E = time_E
        self.H_x = H_x
        self.H_y = H_y
        self.E_z = E_z

    ## Plot function for H_x
    def plot_H_x(self):
        plot(self.time_H, self.H_x, "time (s)" , "H_x (A/m)", "Measurement of H_x  at (" + str(self.pos_x) + "," + str(self.pos_y) + ")")
    ## Plot function for H_y
    def plot_H_y(self):
        plot(self.time_H, self.H_y, "time (s)" , "H_y (A/m)", "Measurement of H_y  at (" + str(self.pos_x) + "," + str(self.pos_y) + ")")
    ## Plot function for E_z
    def plot_E_z(self):
        plot(self.time_E, self.E_z, "time (s)" , "E_z (V/m)", "Measurement of E_z  at (" + str(self.pos_x) + "," + str(self.pos_y) + ")")
    ## Plot function for all measurement data
    def plot_all_separate(self):
        self.plot_H_x()
        self.plot_H_y()
        self.plot_E_z()