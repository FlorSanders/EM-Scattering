import numpy as np
import matplotlib.pyplot as plt
from scipy import special as sp
from constants import eps_0, mu_0, c
import space
import source
import dielectric
import measurement

def experiment(J0, eps_r, start_time, simulation_time):
    d = 0.2
    # PEC box parameters
    x_length, y_length = 2, 2 # [m] (i.c. approximately 30 wavelengths)

    # Initializing a space with a PEC bounding box
    box = space.Space(x_length, y_length, simulation_time)
    box.add_objects([dielectric.Dielectric(1/2*x_length, 0, 1/2*x_length, y_length, eps_r)])
    src = source.Gaussian_pulse(1/2*x_length-d, 1/2*y_length, J0, 4*10**(-10), 10**(-10))
    box.set_source(src)

    print("lambda_min (eps_r): {}".format(src.get_lambda_min(eps_r)))
    Delta_p = src.get_lambda_min(eps_r)/25
    Delta_t = 1 / (3*c*np.sqrt(2/Delta_p**2))
    box.define_discretization(Delta_p, Delta_p, Delta_t)

    # Measurement parameters
    measurement_points = [(1/2*x_length-d, 1/2*y_length), (1/2*x_length+d, 1/2*y_length)] 
    measurement_titles = ["Reflected field", "Transmitted field"]

    # Getting measurments
    box.add_measurement_points(measurement_points, measurement_titles)
    measurements = box.FDTD(plot_space=False ,visualize_fields=500, eps_averaging=True)
    start = int(start_time/Delta_t)
    return np.array([measurements[0].time_E[start:], measurements[0].time_H[start:], measurements[0].H_x[start:], measurements[0].H_y[start:], measurements[0].E_z[start:], measurements[1].H_x[start:], measurements[1].H_y[start:], measurements[1].E_z[start:]])

measurements = []
epsilons = []
for i in range(1):
    measurements.append(experiment(1, 2*i+2, 10**(-9), 4*10**(-9)))
    epsilons.append(2*i+1)

# Separate all fields
E_times = [measure[0] for measure in measurements]
H_times = [measure[1] for measure in measurements]
H_x_r = [measure[2] for measure in measurements]
H_y_r = [measure[3] for measure in measurements]
E_z_r = [measure[4] for measure in measurements]
H_x_t = [measure[5] for measure in measurements]
H_y_t = [measure[6] for measure in measurements]
E_z_t = [measure[7] for measure in measurements]
labels = ["eps_r = {}".format(eps_r) for eps_r in epsilons]

# Make and save all possible plots for these situations
measurement.plot_multiple(E_times, E_z_t, labels, "E_z [V/m]", "time [s]", "Transmitted E_z-fields for various eps_r", "TRcoeff/E_z_t_eps_r")
measurement.plot_multiple(E_times, E_z_r, labels, "E_z [V/m]", "time [s]", "Reflected E_z-fields for various eps_r", "TRcoeff/E_z_r_eps_r")
measurement.plot_multiple(H_times, H_x_t, labels, "H_x [A/m]", "time [s]", "Transmitted H_x-fields for various eps_r", "TRcoeff/H_x_t_eps_r")
measurement.plot_multiple(H_times, H_x_r, labels, "H_x [A/m]", "time [s]", "Reflected H_x-fields for various eps_r", "TRcoeff/H_x_r_eps_r")
measurement.plot_multiple(H_times, H_y_t, labels, "H_y [A/m]", "time [s]", "Transmitted H_y-fields for various eps_r", "TRcoeff/H_y_t_eps_r")
measurement.plot_multiple(H_times, H_y_r, labels, "H_y [A/m]", "time [s]", "Reflected H_y-fields for various eps_r", "TRcoeff/H_y_r_eps_r")

# Get the maximum amplitudes for the transmitted and reflected E and H fields to obtain the Transmission and reflection coefficients
E_t_amps = np.array([np.max(abs(E)) for E in E_z_t])
E_r_amps = np.array([np.max(abs(E)) for E in E_z_r])
# When eps_r = 1: full transmission --> maximum of E_t_amps is used as normalization factor for transmission and reflection coefficients
T_meas = E_t_amps / np.max(E_t_amps)
R_meas = E_r_amps / np.max(E_t_amps)
T_theory = 2/(np.sqrt(epsilons) + 1)
R_theory = (np.sqrt(epsilons) - 1) / (np.sqrt(epsilons) + 1)

measurement.plot_multiple([epsilons]*4, [T_meas, T_theory, R_meas, R_theory], ["measured T", "predicted T", "measured R", "predicted R"], "Relative amplitude [-]", "eps_r [-]", "T and R coefficients for various eps_r", "TRcoeff/TRcoeff_eps_r")