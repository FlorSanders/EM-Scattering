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
eps_r = 4
simulation_time = 3*10**(-9)
d = 0.2
# PEC box parameters
x_length, y_length = 1.5, 1.5 # [m] (i.c. approximately 30 wavelengths)

# Initializing a space with a PEC bounding box
box = space.Space(x_length, y_length, simulation_time)
box.add_objects([dielectric.Dielectric(1/2*x_length, 0, 1/2*x_length, y_length, eps_r)])
src = source.Gaussian_pulse(1/2*x_length-d, 1/2*y_length, J0, 4*10**(-10), 10**(-10))
box.set_source(src)

print("lambda_min ({}): {}".format(eps_r, src.get_lambda_min(eps_r)))
Delta_p = src.get_lambda_min(eps_r)/25
Delta_t = 1 / (3*c*np.sqrt(2/Delta_p**2))
box.define_discretization(Delta_p, Delta_p, Delta_t)
print(Delta_p, Delta_t)

# Measurement parameters
measurement_points = [(1/2*x_length-d, 1/2*y_length), (1/2*x_length+d, 1/2*y_length)] 
measurement_titles = ["Reflected field", "Transmitted field"]

# Getting measurments
box.add_measurement_points(measurement_points, measurement_titles)
measurements = box.FDTD(plot_space=True ,visualize_fields=1000, eps_averaging=False)

for measure in measurements:
    measure.plot_all(measure.title, indicators = False)