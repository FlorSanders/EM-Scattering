# Importing necessary libraries and files
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

### Simple plotting function taking care of matplotlib syntax
def plot(x_values, y_values, x_title, y_title, title, fig=None, yscale = 'linear', filename = "none"):
    plt.plot(x_values, y_values, marker=".")
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.yscale(yscale)
    plt.xlim(x_values[0], x_values[-1]) # confirming plot width to overrule interference line (if to far away)
    if filename != "none":
        fig.savefig("./plots/" + filename + ".png", dpi = fig.dpi)
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
        fig.savefig(filename + ".png", dpi = fig.dpi)
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
    
    ## General plot function to include lines for interference and 
    def plot(self, *args, **kwargs):
        fig = plt.figure()
        try:
            plt.axvline(self.interference_time, linestyle='--', label="Interference can start")
            plt.axvline(self.wave_time, color='green', label="Wave from source arrives")
            plt.legend(title='Guidelines:')
        except AttributeError:
            pass
        plot(*args, fig=fig, **kwargs)

    ## Plot function for H_x
    def plot_H_x(self, filename = "none", indicators = True):
        if(indicators):
            self.plot(self.time_H, self.H_x, "time (s)" , "H_x (A/m)", "H_x " + self.title, filename = filename)
        else:
            plot(self.time_H, self.H_x, "time (s)" , "H_x (A/m)", "H_x " + self.title, filename = filename)
    ## Plot function for H_y
    def plot_H_y(self, filename = "none", indicators = True):
        if(indicators):
            self.plot(self.time_H, self.H_y, "time (s)" , "H_y (A/m)", "H_y " + self.title, filename = filename)
        else:
            plot(self.time_H, self.H_y, "time (s)" , "H_y (A/m)", "H_y " + self.title, filename = filename)

    ## Plot function for E_z
    def plot_E_z(self, filename = "none", indicators = True):
        if(indicators):
            self.plot(self.time_E, self.E_z, "time (s)" , "E_z (V/m)", "E_z " + self.title, filename = filename)
        else:
            plot(self.time_E, self.E_z, "time (s)" , "E_z (V/m)", "E_z " + self.title, filename = filename)

    ## Plot function to plot both H-fields together
    def plot_H_xy(self, filename = "none"):
        plot_multiple([self.time_H, self.time_H], [self.H_x, self.H_y], ["H_x", "H_y"], "time (s)", "H (A/m)", "H " + self.title, filename= filename)
    
    ## Plot function for all measurement data, H-fields plotted separately
    def plot_all_separate(self, filename = "none", indicators = True):
        self.plot_H_x(filename = "H_x " * (filename != "none") + filename, indicators = indicators)
        self.plot_H_y(filename = "H_y " * (filename != "none") + filename, indicators = indicators)
        self.plot_E_z(filename = "E_z " * (filename != "none") + filename, indicators = indicators)
    
    ## Plot function for all measurement data, H-fields plotted together
    def plot_all(self, filename = "none", indicators = True):
        self.plot_H_xy(filename = "H_xy " * (filename!="none") +  filename)
        self.plot_E_z(filename = "E_z " * (filename!="none") + filename, indicators = indicators)
