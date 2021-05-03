import cdsapi
import zipfile

'''
API for importing data from cds.climate.cpernicus.eu
'''
area_germany = [55, 6, 47, 15, ]

c = cdsapi.Client()

model = 'mpi_esm1_2_lr'
variable = 'near_surface_air_temperature'
path = '../Data/'
# path = '/media/fernando/Elements/Data_and_Media/Climate/CMIP6/'
date = '2020-01-01/2050-12-31'
zipfn = path+variable+'_'+model+'.zip'

# The below is the API request to download the data (requires the cdsapi package)
c.retrieve(
    'projections-cmip6',
    {
        'format': 'zip',
        'temporal_resolution': 'monthly',
        'experiment': 'ssp2_4_5',
        'level': 'single_levels',
        'variable': variable,
        'model': model,
        'date': date,
        'area': [
            55, 6, 47,
            15,
        ],
    },
    zipfn)

# Unzip, cd into folder and open the .nc file
with zipfile.ZipFile(zipfn,"r") as zip_ref:
    zip_ref.extractall()