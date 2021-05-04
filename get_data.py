"""
Download climate data using the API from cds.climate.cpernicus.eu
For this data request to work, one must first create a user account
and follow the instructions for setting up the API (install cdsapi package and create file $HOME/.cdsapirc)
"""

import cdsapi
import zipfile
import os


def getdata(save_dir="./", var='near_surface_air_temperature',
            time_step='monthly',
            start_date='2020-01-01',
            end_date='2030-12-31',
            north=52.5, south=50.0, east=12.0, west=10.0,
            experiment='ssp2_4_5',
            model='mpi_esm1_2_lr'
            ):

    dates = start_date+'/'+end_date
    dn = save_dir+'/'+var+'_'+time_step+'_'+start_date+'_'+end_date+'_'+experiment
    zipfn = dn+'.zip'


    # Send the request
    c = cdsapi.Client()

    c.retrieve(
        'projections-cmip6',
        {
            'temporal_resolution': time_step,
            'experiment': experiment,
            'level': 'single_levels',
            'variable': var,
            'model': model,
            'date': dates,
            'area': [north, west, south, east, ],
            'format': 'zip',
        },
        zipfn)

    # Unzip, cd into folder and open the .nc file
    with zipfile.ZipFile(zipfn,"r") as zip_ref:
        zip_ref.extractall(dn)
    os.remove(zipfn)

    info = f"Data has been downloaded into directory: {dn}"

    return info


if __name__ == '__main__':
    getdata()
