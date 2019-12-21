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

# Measurement point and source placement configurations
d = 0.1 # (i.c. approximately 3 wavelengths)

# PEC box parameters
x_length, y_length = 1, 1 # [m] (i.c. approximately 30 wavelengths)
t_length = 20*10**(-10) # [s]

# Initializing a space with a PEC bounding box
box = space.Space(x_length, y_length, t_length)

# Parameters for the dielectric
x_diel = 2/3*x_length # [m]
y_diel = 0# [m]
w_diel = 1/3*x_length # [m]
h_diel = y_length # [m]
eps_r = 4 # [-]
# Initializing the dielectric and adding it to the box
diel = dielectric.Dielectric(x_diel, y_diel, w_diel, h_diel, eps_r)
box.add_objects([diel])

# Source parameters
x_source = x_diel - d # [m]
y_source = 1/2 * y_length - d # [m]
J0 = 1 # [A/m**2]
# omega_c = 10**9 # [Hz] = 1 GHz
sigma = 10**(-10) # [s]
tc = 4*sigma # [s]

# Initializing the source (Choices: Sine_source, Gaussian_pulse, Gaussian_modulated_rd_pulse)
# src = source.Sine_source(x_source, y_source, J0, omega_c)
src = source.Gaussian_pulse(x_source, y_source, J0, tc, sigma)
# src = source.Gaussian_modulated_rf_pulse(x_source, y_source, J0, tc, sigma, omega_c)
# Adding the source to our space
box.set_source(src)

print("lambda_min (eps_r): {}".format(src.get_lambda_min(eps_r)))
Delta_x = src.get_lambda_min(eps_r)/25
Delta_y = Delta_x
Delta_t = 1 / (c * np.sqrt(1/Delta_x**2 + 1/Delta_y**2))

# Handing discretization parameters to our space
box.define_discretization(Delta_x, Delta_y, Delta_t)
print(np.shape(box.E_z))

# Measurement parameters
measurement_points = [(x_source, y_source), (2/3*x_length, 1/2*y_length), (x_source, y_source + 2*d) ,(x_source+2*d, y_source+d*(1+1/np.sqrt(eps_r)))] # [(x_source, y_source), (1.1*x_source, 1.1*y_source), (1.5*x_source, 1.5*y_source)] # List of measurement point coordinates [(m, m)]
                #       At source               At surface                  Reflected wave at 45°       Transmitted wave at arcsin(1/sqrt(eps_r))
# Debugging:
# print(box)

start = timeit.default_timer()

# Getting measurments
box.add_measurement_points(measurement_points)
measurements = box.FDTD(plot_space=False ,visualize_fields=250)

print("Calculation time for 1 measurement point", timeit.default_timer() - start)

measurement.plot(measurements[0].time_E, src.get_current(measurements[0].time_E), "time [s]", "current [A/m**2]", "Current over time at source")

# Plotting measurements
for measure in measurements:
    measure.plot_all_separate()
