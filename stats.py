"""
Calculate and return some summary statistics for the climate data
"""

import numpy as np


def getstats(ds_vars, act_v, dis_v):
    # Get some ifno and stats
    var = ds_vars[act_v]
    var_m = round(var.mean(), 8)
    var_sd = round(var_m / len(var) ** 0.5, 8)
    # var_m = var.mean()
    # var_sd = var_m / len(var) ** 0.5
    var_sm = var.mean(axis=(1, 2))  # get the spatial mean (keeps the time dimension)
    var_tm = var.mean(axis=0)  # get of mean over time (keeps lat/lon)
    var_sm_sd = var_sm / len(var_sm) ** 0.5
    var_tm_sd = var_tm / len(var_tm) ** 0.5
    var_units = ds_vars[act_v + '_units']
    north = np.around(ds_vars['max_lat'], 2)
    south = np.around(ds_vars['min_lat'], 2)
    east = np.around(ds_vars['max_lon'], 2)
    west = np.around(ds_vars['min_lon'], 2)
    lat_units = ds_vars['lat_units']
    lon_units = ds_vars['lon_units']

    s = ['\n'+'Variable: ' + str(dis_v) + '\n' +
         'Units: ' + str(var_units) + '\n' +
         'Overall Mean: ' + str(var_m) + '\n' +
         'Standard Deviation: ' + str(var_sd) + '\n' +
         'Region coordinates: ' + '\n' +
         str(south) + ' to ' + str(north) + ' ' + str(lat_units) + '\n' +
         str(west) + ' to ' + str(east) + ' ' + str(lon_units) + '\n']

    return s[0]

