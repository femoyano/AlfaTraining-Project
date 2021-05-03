"""
Download and open an nc variable
API for importing data from cds.climate.cpernicus.eu
"""

import cdsapi
import zipfile
import os

N = 55; W = 6; S = 47; E = 15
# area_germany = [55, 6, 47, 15, ]
model = 'mpi_esm1_2_lr'
time_step = 'monthly'  # one of: 'daily' or 'monthly'
# data_path = '/media/fernando/Elements/Data_and_Media/Climate/CMIP6/'
start_date = '2020-01-01'
end_date = '2050-12-31'
date = start_date+'/'+end_date
variable = 'near_surface_air_temperature'
data_path = '../Data/'
dn = data_path+variable+'_'+time_step+'_'+start_date+'_'+end_date+'_'+model
zipfn = dn+'.zip'


# The below is the API request to download the data (requires the cdsapi package)
c = cdsapi.Client()
c.retrieve(
    'projections-cmip6',
    {
        'format': 'zip',
        'temporal_resolution': time_step,
        'experiment': 'ssp2_4_5',
        'level': 'single_levels',
        'variable': variable,
        'model': model,
        'date': date,
        'area': [N, W, S, E, ],
    },
    zipfn)

# Unzip, cd into folder and open the .nc file
with zipfile.ZipFile(zipfn,"r") as zip_ref:
    zip_ref.extractall(dn)
os.remove(zipfn)

print(f"Data has been downloaded into directory: {dn}")

