import numpy as np
import matplotlib.pyplot as plt
from scipy import special as sp
from constants import eps_0, mu_0, c
import space
import source
import dielectric
import measurement

# Defining experiment parameters
J0 = 1
simulation_time = 4*10**(-9)
# PEC box parameters
x_length, y_length = 0.35, 0.35 # [m] (i.c. approximately 30 wavelengths)

# Initializing a space with a PEC bounding box
box = space.Space(x_length, y_length, simulation_time)
src = source.Gaussian_pulse(1/2*x_length, 1/2*y_length, J0, 4*10**(-10), 10**(-10))
box.set_source(src)

Delta_p = src.get_lambda_min(1)/25
Delta_t = 1 / (3*c*np.sqrt(2/Delta_p**2))
box.define_discretization(Delta_p, Delta_p, Delta_t)
print(Delta_p, Delta_t)

# Measurement parameters
measurement_points = [(1/2*x_length, 1/2*y_length)] 
measurement_titles = ["at source"]

# Getting measurments
box.add_measurement_points(measurement_points, measurement_titles)
measurements = box.FDTD(plot_space=True ,visualize_fields=False, eps_averaging=False)

measurement.plot(measurements[0].time_E, src.get_current(measurements[0].time_E), "time [s]", "current [A]", "Source current", filename="PEC/current")

for measure in measurements:
    measure.plot_all_separate("PEC/" + measure.title)