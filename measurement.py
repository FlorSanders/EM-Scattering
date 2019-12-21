# Importing necessary libraries and files
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

### Simple plotting function taking care of matplotlib syntax
def plot(x_values, y_values, x_title, y_title, title, interference = 0, yscale = 'linear'):
    plt.plot(x_values, y_values, color='black', marker='o')
    if(interference != 0):
        plt.axvline(interference)
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.yscale(yscale)
    plt.show()

def field_plot(field, x_title, y_title, title):
    plt.imshow(field, origin='lower')
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.show()

def make_animation(field, save = True, name = "animation"):
    fig = plt.figure()
    images = []
    for n in range(field.shape[2]):
        images.append([plt.imshow(abs(field[:,:,n]), origin='lower', animated = True)])

    im_ani = animation.ArtistAnimation(fig, images, interval=25, blit=True,repeat_delay=100)
    im_ani.save(name + '.mp4')
    plt.show()

### Measurement class: Combine all measurement data for a certain point into a single callable instance
class Measurement:
    ## Initialization with all measurement data
    def __init__(self, pos_x, pos_y, interference_time = 0, title = ""):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.interference_time = interference_time
        self.H_x = np.empty(0)
        self.H_y = np.empty(0)
        self.E_z = np.empty(0)
        self.title = title
    
    def set_fields(self, time_H, time_E, H_x, H_y, E_z):
        self.time_H = time_H
        self.time_E = time_E
        self.H_x = H_x
        self.H_y = H_y
        self.E_z = E_z
    
    def append_fields(self, H_x, H_y, E_z):
        self.H_x = np.append(self.H_x, H_x)
        self.H_y = np.append(self.H_y, H_y)
        self.E_z = np.append(self.E_z, E_z)
    
    def set_time(self, time_H, time_E):
        self.time_H = time_H
        self.time_E = time_E

    ## Plot function for H_x
    def plot_H_x(self):
        plot(self.time_H, self.H_x, "time (s)" , "H_x (A/m)", "H_x " + self.title)
    ## Plot function for H_y
    def plot_H_y(self):
        plot(self.time_H, self.H_y, "time (s)" , "H_y (A/m)", "H_y " + self.title)
    ## Plot function for E_z
    def plot_E_z(self):
        plot(self.time_E, self.E_z, "time (s)" , "E_z (V/m)", "E_z " + self.title)
    ## Plot function for all measurement data
    def plot_all_separate(self):
        self.plot_H_x()
        self.plot_H_y()
        self.plot_E_z()
