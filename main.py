#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importing necessary libraries and files
import numpy as np
from scipy import special as sp
import space
import dielectric
import source as src
import measurement
from constants import c

# global dictionaries
var_names = {}          # var names in simulation program
var_description = {}    # var description to print
questions = {}          # General question asked
functions = {}          # dict of used functions
# iteration order of questions/subjects
keys = ["space", "num_dielek", "dielectric", "eps_avg", "line_source", "source_profile", "source_parameters", "discretization_space", "discretization_time", "num_meas", "measurement", "visualize_fields"]
max_eps_r = 1

def tofloat():
    pass

def question(questionstring, **kwargs):
    """Prints out questionstring & returns output dict
    asks for each key in kwargs a value
    returns value associated with each key

    Parameters
    ----------
    questionstring : str
        The question to print
    **kwargs
        The keyword arguments are used to ask all parameters
    Raises
    ------
    Returns
    -------
    output : dict
        keys : **kwargs.keys()
        values : input()
    """
    output = {}
    print()
    print(questionstring)
    for var, varstring in kwargs.items():
        output[var] = input(varstring + ": ")
    return output


def create_dielek(num_dielek):
    """Makes space for 'num_dielek' dielectrics

    In place operator on known data structures (var_... dicts)
    Parameters
    ----------
    num_dielek : int
        Number of dielectrics
    Returns
    -------
        None
    """
    num_dielek = int(num_dielek)
    if num_dielek >= 1:
        print("Note: the position of the dielectric object is referred from it's left down corner to the left down corner of the grid")
    var_names["dielectric"] = [ "pos_x", "pos_y", "width", "height", "eps_r" ]
    var_description["dielectric"] = [ "x-position [m]", "y-postition [m]", "width (x-axis) [m]", "height (y-axis) [m]", "Relative permittivity (εᵣ) [-]" ]
    questions["dielectric"] = []
    functions["dielectric"] = []
    for i in range(num_dielek):
        questions["dielectric"].append("What are the parameters of the {}-th dielectric object?".format(i+1))
        functions["dielectric"].append(make_dielek) # used for catching max_eps_r
    if num_dielek == 0:
        keys.remove("eps_avg")
    return None

def make_dielek(**kwargs):
    global max_eps_r
    if kwargs["eps_r"] > max_eps_r:
        max_eps_r = kwargs["eps_r"]
    return dielectric.Dielectric(**kwargs)

def create_meas(num_meas):
    num_meas = int(num_meas)
    # see also create_dielek
    var_names["measurement"] = [ "pos_x", "pos_y" ]
    var_description["measurement"] = [ "x-position [m]", "y-position [m]" ]
    questions["measurement"] = []
    functions["measurement"] = []
    for i in range(num_meas):
        questions["measurement"].append("What are the parameters of the {}-th measurement point?".format(i+1))
        functions["measurement"].append(lambda **kwargs:(kwargs["pos_x"],kwargs["pos_y"]))
    return None

# object to remember line source position
class placing_line_source:
    def __new__(cls, **kwargs):
        new_obj = super().__new__(cls)
        new_obj.__init__(**kwargs)
        functions["source_profile"] = [new_obj.choose_profile]
        return None
    def __init__(self, **kwargs):
        self.position = kwargs
    def choose_profile(self, profile):
        self.profile = profile
        if profile == 1:
            # profile
            var_names["source_parameters"] = [ "J0", "sigma", "tc" ]
            var_description["source_parameters"] = ["Source amplitude (J₀) [A]", "Pulse width (σ) [s]", "Central time (tc) [s]"]
            questions["source_parameters"] = "What are the parameters for the Gaussian pulse source?"
            functions["source_parameters"] = [self.pulse]
        elif profile == 2:
            var_names["source_parameters"] = [ "J0", "sigma", "tc", "omega_c" ]
            var_description["source_parameters"] = ["Source amplitude (J₀) [A]", "Pulse width (σ) [s]", "Central time (tc) [s]", "Central frequency (ω_c) [Hz]" ]
            questions["source_parameters"] = "What are the parameters for the Gaussian-modulated sinusoidal radio-frequency pulse source?"
            functions["source_parameters"] = [self.pulse]
        else:
            raise ValueError("profile doesn't match")
        return None
    def pulse(self, **kwargs):
        if self.profile == 1:
            source_obj = src.Gaussian_pulse(**self.position, **kwargs)
        elif self.profile == 2:
            source_obj = src.Gaussian_modulated_rf_pulse(**self.position, **kwargs)
        lambda_min = source_obj.get_lambda_min(max_eps_r)
        print()
        print("It is recommended to take the discretization steps between exact {l1} & {l2} [m]".format(l1=lambda_min/30, l2=lambda_min/20))
        print("Human readable: {mini:.2g} < Δspace < {maxi:.2g}".format(mini=lambda_min/30, maxi=lambda_min/20))
        return source_obj

def discretization(**kwargs):
    max_d_t = 1 / (c * np.sqrt(1/(kwargs["Delta_x"]**2) + 1/(kwargs["Delta_y"]**2)))
    print("The time discretization should be less than {} [s] for a stable simulation.".format(max_d_t))
    return kwargs

def dialog():
    """Dialog
    Returns
    -------
    simulation : dict
        Objects for each simulation domain
    """
    simulation = {}         # simulation dict: contains all usefull objects
    simulation["eps_avg"] = False

    ## All variable names, descriptions
    # space
    var_names["space"] = [ "x_length", "y_length", "t_length"]
    var_description["space"] = [ "The length of the simulation domain (x-axis) [m]", "The height of the simulation domain (y-axis) [m]", "The duration of the simulation [s]"]
    questions["space"] = "What are the dimensions of the simulation domain?"
    functions["space"] = [space.Space]

    # number of objects
    var_names["num_dielek"] = [ "num_dielek" ]
    var_description["num_dielek"] = [ "Number of dielectric objects" ]
    questions["num_dielek"] = "How many (rectangular) dielectric objects do you want to add?"
    functions["num_dielek"] = [create_dielek]

    # dielectric objects
    # See create_dielek

    ## Epsilon averaging
    var_names["eps_avg"] = ["eps_averaging"]
    var_description["eps_avg"] = ["Relative permittivity averaging, enter number of choice"]
    questions["eps_avg"] = \
"""Do you want to use relative permittivity averaging? See our report for a full explanation.
0) No εᵣ averaging
1) εᵣ averaging"""
    functions["eps_avg"] = [lambda **kwargs : bool(kwargs["eps_averaging"])]

    ## Line source
    # position
    var_names["line_source"] = [ "pos_x", "pos_y" ]
    var_description["line_source"] = [ "x-position [m]", "y-position [m]" ]
    questions["line_source"] = "Position of the line source?"
    functions["line_source"] = [placing_line_source]

    # choose profile
    var_names["source_profile"] = [ "profile" ]
    var_description["source_profile"] = [ "Enter the number of your choice" ]
    questions["source_profile"] = \
"""Which current profile do you want to use for the line source?
1) Gaussian pulse
2) Gaussian-modulated sinusoidal radio-frequency pulse"""

    # profile

    ## Discretization
    var_names["discretization_space"] = ["Delta_x", "Delta_y"]
    var_description["discretization_space"] = ["Step in x-direction (Δx) [m]", "Step in y-direction (Δy) [m]"]
    questions["discretization_space"] = "How do you want to discretize space?"
    functions["discretization_space"] = [discretization]
    # time
    var_names["discretization_time"] = [ "Delta_t" ]
    var_description["discretization_time"] = [ "Time step (Δt) [s]" ]
    questions["discretization_time"] = "How do you want to discretize time?"
    functions["discretization_time"] = [lambda **kwargs : kwargs]

    ## Measurements
    # number of measurements
    var_names["num_meas"] = [ "num_meas" ]
    var_description["num_meas"] = [ "Number of measurement points" ]
    questions["num_meas"] = "How many measurement points do you want to add?"
    functions["num_meas"] = [create_meas]

    ## Visualize fields
    #
    var_names["visualize_fields"] = [ "visualize_fields" ]
    var_description["visualize_fields"] = ["Seconds of the visualisation time step or 0"]
    questions["visualize_fields"] = \
"""Do you want to visualize the magnitude of the fields every x seconds during the simulation?
0) No
x) Every x seconds, with x a value given by you and between 0 and the length of simulation"""
    functions["visualize_fields"] = [ lambda visualize_fields : visualize_fields//simulation["discretization_time"]["Delta_t"] ]
    # iterate over all simulation domains
    for k in keys:
        # if list --> simulation domain is list too
        if isinstance(questions[k], list):
            simulation[k] = []
            subqst = questions[k]
        else:
            subqst = [ questions[k] ]

        # iterate over all subquestions
        for i, qst in enumerate(subqst):
            var_name_desc = { name: desc for name, desc in zip(var_names[k],var_description[k])}
            answer = question(qst, **var_name_desc)
            # convert answer to integers
            answer = { k:float(v) for k,v in answer.items() }

            #if list --> append to sim domain
            if isinstance(questions[k], list):
                simulation[k].append(functions[k][i](**answer))
            else:
                simulation[k] = functions[k][i](**answer)
    # Remove all None values
    simulation = { k:v for k, v in simulation.items() if v is not None }
    return simulation

def simulate(simulation):
    """
    Parameters
    ----------
    simulation : dict
        Dictionary with all parameters for simulation

    Returns
    -------
    """
    box = simulation["space"]
    box.add_objects(simulation["dielectric"])
    box.set_source(simulation["source_parameters"])
    box.define_discretization(**simulation["discretization_space"], **simulation["discretization_time"])
    titles = [ "  at ({:g} , {:g})".format(meas[0], meas[1]) for meas in simulation["measurement"]]
    box.add_measurement_points(simulation["measurement"], titles)
    measurements = box.FDTD(eps_averaging=simulation["eps_avg"], plot_space=True, visualize_fields = simulation["visualize_fields"])
    measurement.plot(measurements[0].time_E, box.source.get_current(measurements[0].time_E), "time [s]", "current [A]", "Source current", filename = "current")

    for meas in measurements:
        meas.plot_all_separate(meas.title)

if __name__ == '__main__':
    print("""
Applied ElectroMagnetism project
made by:
    Paul De Smul
    Thijs Paelman
    Flor Sanders

This is the input dialog to test our discrete solver

Note: We do not test if the inputted parameters make sense
Note2: All input values are (floating) numbers
    if you want to insert a number like: 1.23*10^(-67)
    use this notation: 1.23e-67
    In all other case, a ValueError will be thrown and you'll have to start again

2 more examples:
    use 1.2 instead of 1,2
    use 1e6 instead of e6 for plain powers of 10
          """)
    simulation = dialog()
    #print(simulation)
    #x = 175
    #y = 100
    #simulation = {'space': space.Space(x*2,500,4e-6), 'dielectric': [ dielectric.Dielectric(20, 200, 310, 100, 7), dielectric.Dielectric(20,300,310,100,15) ],
    #              'eps_avg': False, 'source_parameters': src.Gaussian_pulse(x,y,1,4e-7,1e-7), 'discretization_space': {'Delta_x': 0.6, 'Delta_y': 0.75},
    #              'discretization_time': {'Delta_t': 1e-09}, 'measurement': [(x, 120.0), (x, 220.0), (x, 320.0), (x/2, 340)], 'visualize_fields': 800.0}
    simulate(simulation)
