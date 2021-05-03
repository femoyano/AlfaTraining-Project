# Starts here

import netCDF4 as nc
import numpy as np
import itertools as it


# ---- Import data (read file or get from internet ----

fpath = '../Data/near_surface_air_temperature_monthly_2020-01-01_2050-12-31_mpi_esm1_2_lr/'
fname = 'tas_Amon_MPI-ESM1-2-LR_ssp245_r1i1p1f1_gn_20200116-20501216.nc'
ds = nc.Dataset(fpath+fname, mode='r')
# print(ds)

# ---- Read and print variables and dimensions ----

ncvars = list(ds.variables.keys())
ncdims = list(ds.dimensions.keys())

# Remove dim vars from var list
isvar = [True] * len(ncvars)
for v in range(len(ncvars)):
    for d in ncdims:
        if ncvars[v].find(d) != -1:
            isvar[v] = False
ncvars_s = list(it.compress(ncvars, isvar))  # subset of variables

# Get min and max values of dims (lat, lon)
size_lat = ds.variables['lat'].size
size_lon = ds.variables['lon'].size
min_lat = ds.variables['lat'][0].data
max_lat = ds.variables['lat'][size_lat-1].data
min_lon = ds.variables['lon'][0].data
max_lon = ds.variables['lon'][size_lon-1].data

print(f"Variables in this file are: {str(ncvars_s).strip('[]')}")
print(f"Dimensions in this file are: {str(ncdims).strip('[]')}")


# ---- Subset using variable, time, etc ----

# Choose a variable
var1 = ncvars[-1]

# Choose start and end dates


# ---- Subset point location using time span and lat/lon ----

p_lat = 50  # units -90 to 90
p_lon = 10  # units 0 to 359


# Save selection as .csv

# Perform statistics

# Plot time series

# Plot maps

# ds.close()
