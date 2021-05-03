# read in a ncdf file

import netCDF4 as nc

fn = '../Data/HADGEM_SRA1B_1_MM_ts_1-1201.nc'
ds = nc.Dataset(fn)
print(ds)           # Print metadata
print(ds.__dict__)  # Metadata conversion to Python dictionary
print(ds.__dict__['variables'])