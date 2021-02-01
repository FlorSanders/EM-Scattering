# Importing necessary libraries and files
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy import special as sp
from constants import eps_0, mu_0, c
import space
import source
import dielectric
import measurement

import timeit

plt.rcParams.update({"font.size": 22})

# Source parameters
x_source = 100  # [m]
y_source = 100  # [m]
J0 = 1  # [A]
omega_c = 10 ** 5  # [Hz] = 1 GHz
omega_c = 0  # [Hz] = 1 GHz
sigma = 5 * 10 ** (-9)  # [s]
tc = 3 * sigma  # [s]
print("max_freq normal: {}".format(3 / (2 * np.pi * sigma)))
print("max_freq modulated: {}".format(3 / (2 * np.pi * sigma) + omega_c / (2 * np.pi)))

# Initializing the source (Choices: Sine_source, Gaussian_pulse, Gaussian_modulated_rd_pulse)
# src = source.Sine_source(x_source, y_source, J0, omega_c)
src = source.Gaussian_pulse(x_source, y_source, J0, tc, sigma)
# src = source.Gaussian_modulated_rf_pulse(x_source, y_source, J0, tc, sigma, omega_c)

# PEC box parameters
x_length, y_length = 2 * x_source, 2 * y_source  # [m]
t_length = 12 * tc  # [s]

# Initializing a space with a PEC bounding box
box = space.Space(x_length, y_length, t_length)

# Adding the source to our space
box.set_source(src)

# Discretization parameters (Based on limits in project description)
Delta_x = src.get_lambda_min(1) / 25
Delta_y = Delta_x
Delta_t = 1 / (c * np.sqrt(1 / Delta_x ** 2 + 1 / Delta_y ** 2)) / 3

# Handing discretization parameters to our space
box.define_discretization(Delta_x, Delta_y, Delta_t)

# Measurement parameters
measurement_points = (
    [(x_source, y_source)]
    + [(1.1 * x_source, 1.1 * y_source)]
    + [(1.2 * x_source, 1.24 * y_source)]
)  # List of measurement point coordinates [(m, m)]

# Debugging:
print(box)

# Getting measurments
max_times = box.add_measurement_points(measurement_points)
measurements = box.FDTD(plot_space=True, visualize_fields=00)

measurement.plot(
    measurements[0].time_E,
    src.get_current(measurements[0].time_E),
    "time [s]",
    "current [A]",
    "Source current",
)

# Plotting measurements
for measure in measurements:
    measure.plot_all_separate(indicators=False)
    pass

#### freq domain
def E_z_hankel(x, y, omega):
    z = omega / c * np.sqrt((x - box.source.pos_x) ** 2 + (y - box.source.pos_y) ** 2)
    E_z = -box.source.J0 * mu_0 * omega / 4 * sp.hankel2(0, z)
    return E_z


def SOURCE(omega):
    fourier = (
        box.source.J0
        * np.sqrt(2 * np.pi)
        * sigma
        * np.exp(-(sigma ** 2) * (omega ** 2) / 2)
    )
    return fourier


# restrict to bandwidth source
pad_zeros = 100000
reffreq = np.fft.rfftfreq(pad_zeros, d=Delta_t) * 2 * np.pi  # array of omega
use_indices = np.where(
    (reffreq >= (omega_c - 3 / sigma)) & (reffreq <= (omega_c + 3 / sigma))
)
reffreq = reffreq[use_indices]

validE_z = measurements[0].E_z[: int(measurements[0].interference_time // Delta_t)]
ref = np.fft.rfft(validE_z, n=pad_zeros) * Delta_t
ref = ref[use_indices]


def SOURCE_EXP(omega):
    t = measurements[0].time_E
    current = box.source.get_current(t)
    fourier = np.fft.rfft(current, n=pad_zeros) * Delta_t
    return fourier[use_indices]


for meas in measurements[1:]:
    # hankel
    h = E_z_hankel(meas.pos_x, meas.pos_y, reffreq)
    # meas
    validE_z = meas.E_z[: int(meas.interference_time // Delta_t)]
    meas_e = np.fft.rfft(validE_z, n=pad_zeros) * Delta_t
    # restrict to bandwith source
    meas_e = meas_e[use_indices]

    plt.plot(reffreq, abs(meas_e) / SOURCE(reffreq), label="experimental")
    plt.plot(reffreq, abs(h), label="analytical")
    plt.xlabel(r"$\omega$ [Hz]")
    plt.ylabel(r"Amplitude [$\frac{V}{m}$]")
    plt.title(
        r"Frequency domain of $e_z$ in ({:g} , {:g})".format(meas.pos_x, meas.pos_y)
    )
    plt.legend()
    plt.show()
    plt.plot(reffreq, np.angle(meas_e / SOURCE_EXP(reffreq)), label="experimental")
    plt.plot(reffreq, np.angle(h), label="analytical")
    plt.xlabel(r"$\omega$ [Hz]")
    plt.ylabel(r"Phase [radians]")
    plt.title(
        r"Frequency domain of $e_z$ in ({:g} , {:g})".format(meas.pos_x, meas.pos_y)
    )
    ax = plt.gca()
    ax.set_yticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    labels = [r"$-\pi$", r"$-\frac{\pi}{2}$", r"$0$", r"$\frac{\pi}{2}$", r"$\pi$"]
    ax.set_yticklabels(labels)
    # ax.yaxis.set_major_for(ticker.FuncFormatter(lambda x, pos: ""
    plt.legend()
    plt.show()
    plt.plot(reffreq, (meas_e / SOURCE(reffreq)).real)
    plt.plot(reffreq, h.real)
    plt.xlabel(r"$\omega$ [Hz]")
    plt.ylabel(r"Real part [-]")
    plt.title(
        r"Frequency domain of $e_z$ in ({:g} , {:g})".format(meas.pos_x, meas.pos_y)
    )
    plt.legend()
    plt.show()
    plt.plot(reffreq, (meas_e / SOURCE(reffreq)).imag)
    plt.plot(reffreq, h.imag)
    plt.xlabel(r"$\omega$ [Hz]")
    plt.ylabel(r"Imag part [-]")
    plt.title(
        r"Frequency domain of $e_z$ in ({:g} , {:g})".format(meas.pos_x, meas.pos_y)
    )
    plt.legend()
    plt.show()
