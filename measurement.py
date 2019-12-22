# Importing necessary libraries and files
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

### Simple plotting function taking care of matplotlib syntax
def plot(x_values, y_values, x_title, y_title, title, interference = 0, yscale = 'linear', filename = "none"):
    fig = plt.figure()
    plt.plot(x_values, y_values, marker=".")
    if(interference != 0):
        plt.axvline(interference)
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.yscale(yscale)
    if filename != "none":
        fig.savefig("./plots/" + filename + ".png", dpi = fig.dpi)
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

def plot_multiple(x_values_list, y_values_list, labels_list, x_title, y_title, title, filename = "none"):
    fig = plt.figure()
    for i in range(len(x_values_list)):
        plt.plot(x_values_list[i], y_values_list[i], label = labels_list[i], marker = ".")
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.legend()
    if filename != "none":
        fig.savefig("./plots/" + filename + ".png", dpi = fig.dpi)
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

    def plot_E_z(self, filename = "none"):
        plot(self.time_E, self.E_z, "time (s)" , "E_z (V/m)", "E_z " + self.title, filename = filename)
    def plot_H_xy(self, filename = "none"):
        plot_multiple([self.time_H, self.time_H], [self.H_x, self.H_y], ["H_x", "H_y"], "time (s)", "H (A/m)", "H " + self.title, filename= filename)
    def plot_all(self, filename = "none"):
        self.plot_H_xy(filename = filename + "H_xy" * (filename!="none"))
        self.plot_E_z(filename = filename + "E_z" * (filename!="none"))
