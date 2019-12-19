# Importing necessary libraries and files
import numpy as np
from scipy import special as sp
import space
import dielectric
import source as src
from constants import c

# global dictionaries
var_names = {}          # var names in simulation program
var_description = {}    # var description to print
questions = {}          # General question asked
functions = {}          # dict of used functions
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
    var_description["dielectric"] = [ "x-position [m]", "y-postition [m]", "width [m]", "height [m]", "Relative permittivity (εᵣ) [-]" ]
    questions["dielectric"] = []
    functions["dielectric"] = []
    for i in range(num_dielek):
        questions["dielectric"].append("What are the parameters of the {}-th dielectric object?".format(i+1))
        functions["dielectric"].append(make_dielek) # used for catching max_eps_r
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
            var_description["source_parameters"] = ["Source amplitude (J₀) [A/m²]", "Pulse width (σ) [s]", "Central time (tc) [s]"]
            questions["source_parameters"] = "What are the parameters for the Gaussian pulse source?"
            functions["source_parameters"] = [self.pulse]
        elif profile == 2:
            var_names["source_parameters"] = [ "J0", "sigma", "tc", "omega_c" ]
            var_description["source_parameters"] = ["Source amplitude (J₀) [A/m²]", "Pulse width (σ) [s]", "Central time (tc) [s]", "Central frequency (ω_c) [Hz]" ]
            questions["source_parameters"] = "What are the parameters for the Gaussian-modulated sinusoidal radio-frequency pulse source?"
            functions["source_parameters"] = [self.pulse]
        else:
            raise UnsupportedError("profile doesn't match")
        return None
    def pulse(self, **kwargs):
        if self.profile == 1:
            source_obj = src.Gaussian_pulse(**self.position, **kwargs)
        elif self.profile == 2:
            source_obj = src.Gaussian_modulated_rf_pulse(**self.position, **kwargs)
        lambda_min = source_obj.get_lambda_min(max_eps_r)
        print("It is recommended to take the discretization steps between {l1} & {l2} [m]".format(l1=lambda_min/30, l2=lambda_min/20))
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
    # iteration order of questions/subjects
    keys = ["space", "num_dielek", "dielectric", "line_source", "source_profile", "source_parameters", "discretization_space", "discretization_time", "num_meas", "measurement"]

    ## All variable names, descriptions
    # space
    var_names["space"] = [ "x_length", "y_length", "t_length"]
    var_description["space"] = [ "The length of the simulation domain (x-axis) [m]", "The heigth of the simulation domain (y-axis) [m]", "The duration of the simulation [s]"]
    questions["space"] = "What are the dimensions of the simulation domain?"
    functions["space"] = [space.Space]

    # number of objects
    var_names["num_dielek"] = [ "num_dielek" ]
    var_description["num_dielek"] = [ "Number of dielectric objects" ]
    questions["num_dielek"] = "How many (rectangular) dielectric objects do you want to add?"
    functions["num_dielek"] = [create_dielek]

    # dielectric objects
    # See create_dielek

    ## Line source
    # position
    var_names["line_source"] = [ "pos_x", "pos_y" ]
    var_description["line_source"] = [ "x-position [m]", "y-position [m]" ]
    questions["line_source"] = "Where does the line source has to be placed?"
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
    var_description["discretization_time"] = [ "d_t" ]
    questions["discretization_time"] = "give dis time"
    functions["discretization_time"] = [lambda **kwargs : kwargs]

    ## Measurements
    # number of measurements
    var_names["num_meas"] = [ "num_meas" ]
    var_description["num_meas"] = [ "Number of meas objects" ]
    questions["num_meas"] = "Enter the number of meas"
    functions["num_meas"] = [create_meas]
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
    box.FDTD(simulation["measurement"], make_animation=False)

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
          """)
    simulation = dialog()
    print(simulation)
    simulate(simulation)
