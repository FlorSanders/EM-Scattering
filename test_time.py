import numpy as np
import matplotlib.pyplot as plt
from scipy import special as sp
from constants import eps_0, mu_0, c
import space
import source
import dielectric
import measurement
import timeit
def experiment(omega_factor):
    # Defining experiment parameters
    J0 = 1
    simulation_time = 2*10**(-9)
    # PEC box parameters
    x_length, y_length = 1, 1 # [m] (i.c. approximately 30 wavelengths)

    # Initializing a space with a PEC bounding box
    box = space.Space(x_length, y_length, simulation_time)
    src = source.Gaussian_pulse(1/2*x_length, 1/2*y_length, J0, 4*10**(-10), 10**(-10))
    box.set_source(src)

    lambda_min = 3/omega_factor*src.get_lambda_min(1)
    Delta_p = lambda_min/25
    Delta_t = 1 / (3*c*np.sqrt(2/Delta_p**2))
    box.define_discretization(Delta_p, Delta_p, Delta_t)

    # Measurement parameters
    measurement_points = [(1/2*x_length, 1/2*y_length)] 
    measurement_titles = ["Reflected field"]
    
    # Adding measurment points
    box.add_measurement_points(measurement_points, measurement_titles)
    
    # Measuring time to perform measurement 
    start = timeit.default_timer()
    box.FDTD(plot_space=False ,visualize_fields=False, eps_averaging=False)
    time = timeit.default_timer() - start
    return [time, Delta_p, Delta_t, lambda_min]

experiments = [[experiment(i) for j in range(5)] for i in range(2,5)]
for i in range(2,6):
    experiments = [experiment(i) for j in range(5)]
    time = np.average([experiment[0] for experiment in experiments])
    print(time, experiments[0][1], experiments[0][2], experiments[0][3])