# Starts here

import netCDF4 as nc
import numpy as np
import itertools as it


# ---- Import data (read file or get from internet ----

fn = "../Data/tas_Amon_HadGEM2-ES_rcp45_r1i1p1_203012-205511.nc"
ds = nc.Dataset(fn, mode='r')
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
ncvars = list(it.compress(ncvars, isvar))

# Get min and max values of dims (lat, lon)
size_lat = ds.variables['lat'].size
size_lon = ds.variables['lon'].size
min_lat = ds.variables['lat'][0].data
max_lat = ds.variables['lat'][size_lat-1].data
min_lon = ds.variables['lon'][0].data
max_lon = ds.variables['lon'][size_lon-1].data

print(f"Variables in this file are: {str(ncvars).strip('[]')}")
print(f"Dimensions in this file are: {str(ncdims).strip('[]')}")


# ---- Subset point location using variable name, time span and lat/lon ----

var1 = ncvars[1]
lat_range = (47, 55)  # units -90 to 90
lon_range = (6, 15)  # units 0 to 359

# Save selection as .csv

# Perform statistics

# Plot time series

# Plot maps

ds.close()
