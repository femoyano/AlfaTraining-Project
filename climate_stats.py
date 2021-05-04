"""
Calculate and return some summary statistics for the climate data
"""

import numpy as np


def getstats(ds, act_v, dis_v):

    # Get valeus from the climate variable
    var = ds.variables[act_v][:, :, :]
    var = np.ma.asarray(var)
    var_sm = var.mean(axis=(1, 2))  # get the spatial mean mean (keeps the time dimension)
    var_tm = var.mean(axis=0)  # get of mean over time (keeps lat/lon)
    var_unit = ds.variables[act_v].units



    print(dis_v)



