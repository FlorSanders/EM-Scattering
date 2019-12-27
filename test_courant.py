# Importing necessary libraries and files
import numpy as np
import matplotlib.pyplot as plt
from scipy import special as sp
from constants import eps_0, mu_0, c
import space
import source
import dielectric
import measurement
import timeit

plt.rcParams.update({'font.size':22}) # plot font

# Source parameters
x_source = 50 # [m]
y_source = 50 # [m]
J0 = 1 # [A]
omega_c = 10**5 # [Hz] = 1 GHz
omega_c = 0 # [Hz] = 1 GHz
sigma = 5*10**(-9) # [s]
tc = 3*sigma # [s]

# Initializing the source (Choices: Sine_source, Gaussian_pulse, Gaussian_modulated_rd_pulse)
# src = source.Sine_source(x_source, y_source, J0, omega_c)
src = source.Gaussian_pulse(x_source, y_source, J0, tc, sigma)
#src = source.Gaussian_modulated_rf_pulse(x_source, y_source, J0, tc, sigma, omega_c)

# PEC box parameters
x_length, y_length = 2*x_source, 2*y_source # [m]
t_length = 7*tc # [s]

# Initializing a space with a PEC bounding box
box = space.Space(x_length, y_length, t_length)
box.set_source(src)

# Discretization parameters (Based on limits in project description)
Delta_x = src.get_lambda_min(1)/30
Delta_y = Delta_x
Delta_t = 1 / (c * np.sqrt(1/Delta_x**2 + 1/Delta_y**2)) * 1.0001

# Handing discretization parameters to our space
box.define_discretization(Delta_x, Delta_y, Delta_t)

# Measurement parameters
measurement_points = [(x_source, y_source)] # [(1.1*x_source, 1.1*y_source)] + [(1.2*x_source, 1.24*y_source)] # List of measurement point coordinates [(m, m)]
measurement_labels = [r"     $1.0001$ Courant limit     $t_{max} = 7 t_c$" ] #, "", "" ]

# Debugging:
print(box)

# Getting measurments
max_times = box.add_measurement_points(measurement_points, measurement_labels)
measurements = box.FDTD(plot_space=True ,visualize_fields=00)

measurement.plot(measurements[0].time_E, src.get_current(measurements[0].time_E), "time [s]", "current [A]", "Source current")

# Plotting measurements
for measure in measurements:
    measure.plot_all_separate(measure.title)
    pass

exit()
