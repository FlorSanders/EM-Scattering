# Importing scientific libraries to make our lives easier
import numpy as np
from constants import c


class Source:
    def __init__(self, pos_x, pos_y, J0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.J0 = J0

    def __str__(self):
        return "Source:\nx-location: {} m\ny-location: {} m\nCurrent {}\n".format(
            self.pos_x, self.pos_y, self.J0
        )


class Gaussian_pulse(Source):
    def __init__(self, pos_x, pos_y, J0, tc, sigma):
        super().__init__(pos_x, pos_y, J0)
        self.tc = tc
        self.sigma = sigma

    def get_current(self, t):
        return self.J0 * np.exp(-((t - self.tc) ** 2) / (2 * self.sigma ** 2))

    def get_lambda_min(self, eps_r):
        v_min = c / np.sqrt(eps_r)
        omega_max = 3 / self.sigma
        return 2 * np.pi * v_min / omega_max

    def __str__(self):
        s = super().__str__()
        return s + "sigma: {}\ntc: {}\n".format(self.sigma, self.tc)


class Gaussian_modulated_rf_pulse(Source):
    def __init__(self, pos_x, pos_y, J0, tc, sigma, omega_c):
        super().__init__(pos_x, pos_y, J0)
        self.omega_c = omega_c
        self.tc = tc
        self.sigma = sigma

    def get_current(self, t):
        return (
            self.J0
            * np.exp(-((t - self.tc) ** 2) / (2 * self.sigma ** 2))
            * np.sin(self.omega_c * t)
        )

    def get_lambda_min(self, eps_r):
        v_min = c / np.sqrt(eps_r)
        # Gaussian + freq shift sinus
        omega_max = 3 / self.sigma + self.omega_c
        return 2 * np.pi * v_min / omega_max

    def __str__(self):
        s = super().__str__()
        return s + "sigma: {}\ntc: {}\nomega_c: {}\n".format(
            self.sigma, self.tc, self.omega_c
        )
