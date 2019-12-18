# Importing necessary libraries and files
import numpy as np
from scipy import special as sp
import space
import dielectric
import source as src

# global dictionaries
var_names = {}          # var names in simulation program
var_description = {}    # var description to print
questions = {}          # General question asked
functions = {}          # dict of used functions

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
    print(questionstring)
    for var, varstring in kwargs.items():
        output[var] = input(varstring + ":")
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
    var_names["dielectric"] = [ "pos_x", "pos_y", "width", "height", "eps_r" ]
    var_description["dielectric"] = [ "...", "...", "...", "...", "..." ]
    questions["dielectric"] = []
    functions["dielectric"] = []
    for i in range(num_dielek):
        questions["dielectric"].append("What are the parameters of object {}".format(i))
        functions["dielectric"].append(dielectric.Dielectric)
    return None

# object to remember line source position
class placing_line_source:
    def __init__(self, **kwargs):
        self.position = kwargs
    def choose_profile(self, profile):
        self.profile = profile
        if profile == 1:
            # profile
            var_names["source_parameters"] = [ "J0", "tc", "sigma" ]
            var_description["source_parameters"] = var_names["source_parameters"].copy()
            questions["source_parameters"] = ["Profile line source"]
            functions["source_parameters"] = [self.pulse]
        elif profile == 2:
            var_names["source_parameters"] = [ "J0", "tc", "sigma", "omega_c" ]
            var_description["source_parameters"] = var_names["source_parameters"].copy()
            questions["source_parameters"] = ["Profile line source"]
            functions["source_parameters"] = [self.pulse]
        else:
            raise UnsupportedError("profile doesn't match")
        return None
    def pulse(self, **kwargs):
        if self.profile == 1:
            return src.Gaussian_pulse(**self.position, **kwargs)
        elif self.profile == 2:
            return src.Gaussian_modulated_rf_pulse(**self.position, **kwargs)

def place_source(**kwargs):
    functions["source_profile"] = [placing_line_source(**kwargs).choose_profile]
    return None


def dialog():
    """Dialog
    Returns
    -------
    simulation : dict
        Objects for each simulation domain
    """
    simulation = {}         # simulation dict: contains all usefull objects
    # iteration order of questions/subjects
    keys = ["space", "num_dielek", "dielectric", "line_source", "source_profile", "source_parameters"]

    ## All variable names, descriptions
    # space
    var_names["space"] = [ "x_length", "y_length", "t_length"]
    var_description["space"] = [ "the length of the simulation domain (units)", "the heigth of the simulation domain (units)", "the duration of the simulation (time units)"]
    questions["space"] = "What are the dimensions of the simulation domain?"
    functions["space"] = [space.Space]

    # number of objects
    var_names["num_dielek"] = [ "num_dielek" ]
    var_description["num_dielek"] = [ "Number of dielectric objects" ]
    questions["num_dielek"] = "Enter the number of dielectric"
    functions["num_dielek"] = [create_dielek]

    # dielectric objects
    # See create_dielek

    ## Line source
    # position
    var_names["line_source"] = [ "pos_x", "pos_y" ]
    var_description["line_source"] = [ "pos_x", "pos_y" ]
    questions["line_source"] = "Position of line source"
    functions["line_source"] = [place_source]

    # choose profile
    var_names["source_profile"] = [ "profile" ]
    var_description["source_profile"] = var_names["source_profile"].copy()
    questions["source_profile"] = "Profile line source: 1 = Gaus, 2=sin"
    #functions["source_profile"] = [choose_profile]
    # profile
    #var_names["source_parameters"] = [ "J0", "tc", "sigma" ]
    #var_description["source_profile"] = var_names.copy()
    #questions["source_profile"] = ["Profile line source"]
    #functions["source_parameters"] = []

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
            answer = { k:int(v) for k,v in answer.items() }

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

print(dialog())
