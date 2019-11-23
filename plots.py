import numpy as np
import matplotlib.pyplot as plt
from scipy import special as sp

def plot(x_values, y_values, x_title, y_title):
    plt.plot(x_values, y_values, color='black', marker='o')
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.show()
    return
