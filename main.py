# Importing scientific libraries to make our lives easier
import numpy as np
import matplotlib.pyplot as plt
from scipy import special as sp

import space
import dielectric

def question(questionstring, **kwargs):
    output = {}
    print("Please input a value for {}:".format(questionstring))
    for var, varstring in kwargs.items():
        output[var] = input(varstring + ":")
    return output
def dialog():
    # dict: simulation
    simulation = {}
    # space
    var_names = [ "x_length", "y_length", "t_length"]
    var_description = [ "the length of the simulation domain (units)", "the heigth of the simulation domain (units)", "the duration of the simulation (time units)"]
    var_name_desc = { name: desc for name, desc in zip(var_names,var_description)}
    dimensions = question("What are the dimensions of the simulation domain?", **var_name_desc)
    dimensions = { k:int(v) for k,v in dimensions.items() }
    simulation["space"] = space.Space(**dimensions)

    # dielectric objects
    simulation["objects"] = []
    var_names = [ "pos_x", "pos_y", "width", "height", "eps_r" ]
    var_description = [ "...", "...", "...", "...", "..." ]
    var_name_desc = { name: desc for name, desc in zip(var_names,var_description)}
    num_objs = int(question("number of objects", num_objs = "Number of objects")["num_objs"])
    for i in range(num_objs):
        obj_params = question("What are the parameters of object {}".format(i), **var_name_desc)
        dielec_obj = dielectric.Thing(**obj_params)
        simulation["objects"].append(dielec_obj)
    print(simulation)

dialog()
