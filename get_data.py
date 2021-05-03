"""
Download and open an nc variable
API for importing data from cds.climate.cpernicus.eu
"""

import cdsapi
import zipfile
import os


def get_data(save_dir="./", var='near_surface_air_temperature',
             time_step='monthly',
             start_date='2020-01-01',
             end_date='2100-12-31',
             north=55.0, south=47.0, east=9.0, west=16.0,
             model='mpi_esm1_2_lr',
             info=""):

    date = start_date+'/'+end_date
    dn = save_dir+var+'_'+time_step+'_'+start_date+'_'+end_date+'_'+model
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
            'variable': var,
            'model': model,
            'date': date,
            'area': [north, west, south, east, ],
        },
        zipfn)

    # Unzip, cd into folder and open the .nc file
    with zipfile.ZipFile(zipfn,"r") as zip_ref:
        zip_ref.extractall(dn)
    os.remove(zipfn)

    info = f"Data has been downloaded into directory: {dn}"

    return info
