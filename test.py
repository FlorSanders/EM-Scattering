# Importing necessary libraries and files
import numpy as np
import matplotlib.pyplot as plt
from scipy import special as sp
from constants import eps_0, mu_0, c
import space
import source
import dielectric
import measurement

# Source parameters
x_source = 10 # [m]
y_source = 10 # [m]
J0 = 1 # [A/m**2]
omega_c = 10**9 # [Hz] = 1 GHz
sigma = 10**(-6) # [s]
tc = 3*sigma # [s]

# Initializing the source (Choices: Sine_source, Gaussian_pulse, Gaussian_modulated_rd_pulse)
src = source.Sine_source(pos_x, pos_y, J0, omega_c)
# src = source.Gaussian_pulse(pos_x, pos_y, J0, tc, sigma)
# src = source.Gaussian_modulated_rf_pulse(pos_x, pos_y, J0, tc, sigma, omega_c)

# PEC box parameters
x_length, y_length = 2*x_source, 2*y_source # [m]
t_length = 5/(omega_c) # [s]

# Initializing a space with a PEC bounding box
box = space.Space(x_length, y_length, t_length)

# Discretization parameters (Based on limits in project description)
print(src.get_lambda_min(1))
Delta_x = src.get_lambda_min(1)/25
Delta_y = Delta_x
Delta_t = 1 / (c * np.sqrt(1/Delta_x**2 + 1/Delta_y**2))

# Handing discretization parameters to our space
box.define_discretization(Delta_x, Delta_y, Delta_t)

# Adding the source to our space
box.set_source(src)

# Measurement parameters
measurement_points = [((1.01)*x_source, (1.01)*y_source)] # List of measurement point coordinates [(m, m)]

# Getting measurments
measurements = box.FDTD(measurement_points)

measurement.plot(measurements[0].time_E, src.get_current(measurements[0].time_E), "time [s]", "current [A/m**2]", "Current over time at source")

# Plotting measurements
for measure in measurements:
    measure.plot_E_z()
    print(measure.E_z)