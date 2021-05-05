import netCDF4 as nC
import itertools as it
from matplotlib import pyplot as plt
import numpy as np

ncsets = []

fpath = 'tas_Amon_MPI-ESM1-2-LR_ssp245_r1i1p1f1_gn_20200116-20301216.nc'
ncsets.append(nC.Dataset(fpath, mode='r'))
ds = ncsets[0]
nc_vars = ['tas', 'tasmax', 'tasmin', 'pr']
disp_vars = ['Surface Air Temperature', 'Max Air Temperature', 'Min Air Temperature', 'Precipitation']
gui_vars = ["---none loaded---"]

ncvars = list(ds.variables.keys())
ncdims = list(ds.dimensions.keys())
ncdims.append('height')

vind = []
# Find variables in the file
for var in nc_vars:
    try:
        i = nc_vars.index(var)
        vind.append(i)
    except ValueError:
        pass

if len(vind) == 0:
    print('Could not find any ')
c = 0
for ind in vind:



# # Remove dim vars from var list
# isvar = [True] * len(ncvars)
# for v in range(len(ncvars)):
#     for d in ncdims:
#         if ncvars[v].find(d) != -1:
#             isvar[v] = False
# ncvars = list(it.compress(ncvars, isvar))  # subset of variables

# Get min and max values of dims (lat, lon)
size_lat = ds.variables['lat'].size
size_lon = ds.variables['lon'].size
min_lat = ds.variables['lat'][0].data
max_lat = ds.variables['lat'][size_lat - 1].data
min_lon = ds.variables['lon'][0].data
max_lon = ds.variables['lon'][size_lon - 1].data

lat = ds.variables['lat'][:]
lon = ds.variables['lon'][:]
time = ds.variables['time'][:]  # becomes type 'numpy.ma.core.MaskedArray'
tas = ds.variables['tas'][:, :, :]

lat = np.ma.asarray(lat)
lon = np.ma.asarray(lon)
time = np.ma.asarray(time)
tas = np.ma.asarray(tas)
tas_sm = tas.mean(axis=(1, 2))  # get the spatial mean mean (keeps the time dimension)
tas_tm = tas.mean(axis=0)       # get of mean over time (keeps lat/lon)

time_units = ds.variables['time'].units
tas_units = ds.variables['tas'].units
lat_units = ds.variables['lat'].units
lon_units = ds.variables['lon'].units


