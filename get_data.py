"""
Download climate data using the API from cds.climate.cpernicus.eu
For this data request to work, one must first create a user account
and follow the instructions for setting up the API (install cdsapi package and create file $HOME/.cdsapirc)
"""

import cdsapi
import zipfile
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def getdata_gui():
    # Define vars for data download
    climvars = [
        "near_surface_air_temperature",
        "daily_maximum_near_surface_air_temperature",
        "daily_minimum_near_surface_air_temperature",
        "precipitation"
    ]
    timestep = ["monthly", "daily"]

    def get_save_dir():
        d = filedialog.askdirectory()
        tk_save_dir.set(d)

    def call_getdata():
        info = getdata(save_dir=str(tk_save_dir.get()),
                       var=str(tk_get_var.get()),
                       time_step=str(tk_get_step.get()),
                       start_date=str(tk_get_sdate.get()),
                       end_date=str(tk_get_edate.get()),
                       north=float(tk_get_N.get()), south=float(tk_get_S.get()),
                       east=float(tk_get_E.get()), west=float(tk_get_W.get())
                       )
        messagebox.showinfo("Data Download", info)
        top_getdata.quit()
        top_getdata.destroy()

    def close_getdatawin():
        top_getdata.quit()
        top_getdata.destroy()

    top_getdata = tk.Toplevel()
    top_getdata.grid()

    # Create tk variables for data download
    tk_save_dir = tk.StringVar()
    tk_get_var = tk.StringVar()
    tk_get_step = tk.StringVar()
    tk_get_sdate = tk.StringVar()
    tk_get_edate = tk.StringVar()
    tk_get_N = tk.DoubleVar()
    tk_get_E = tk.DoubleVar()
    tk_get_S = tk.DoubleVar()
    tk_get_W = tk.DoubleVar()
    # Set defaults (default coordinates given for Germany)
    tk_save_dir.set(".")
    tk_get_var.set("near_surface_air_temperature")
    tk_get_step.set("monthly")
    tk_get_sdate.set("2020-01-01")
    tk_get_edate.set("2030-12-31")
    tk_get_N.set(55.0)
    tk_get_E.set(15.0)
    tk_get_S.set(47.0)
    tk_get_W.set(6.0)

    irow = 0
    lab1 = tk.Label(top_getdata, text="Variable", justify='left')
    lab1.grid(row=irow, column=0, columnspan=3,  sticky=tk.W, padx=10, pady=5)
    irow += 1

    for val, climvar in enumerate(climvars):  # enumerate generates tuples
        tk.Radiobutton(top_getdata,
                       text=climvar,
                       variable=tk_get_var,
                       indicatoron=1,
                       # command=,
                       value=climvar).grid(row=irow, column=0, columnspan=3,  sticky=tk.W, padx=20)  # .grid(sticky=tk.W + tk.E)  # returns str
        irow += 1

    lab2 = tk.Label(top_getdata, text="Time Step", justify='left')
    lab2.grid(row=irow, column=0,  columnspan=3,  sticky=tk.W, padx=10, pady=5)
    irow += 1

    for val, step in enumerate(timestep):  # enumerate generates tuples
        tk.Radiobutton(top_getdata,
                       text=step,
                       variable=tk_get_step,
                       indicatoron=1,
                       # command=,
                       value=step).grid(row=irow, column=0, columnspan=3, sticky=tk.W, padx=20)  # returns str
        irow += 1

    mt1 = 'Choose a time range between 2020-01-01 and 2300-12-31'
    hlab1 = tk.Label(top_getdata, text=mt1)
    hlab1.grid(row=irow, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)
    irow += 1

    lab3 = tk.Label(top_getdata, text="Start date (yyyy-mm-dd)")
    lab3.grid(row=irow, column=0, columnspan=2, sticky=tk.W, padx=20)
    ent_sdate = tk.Entry(top_getdata, textvariable=tk_get_sdate)
    ent_sdate.grid(row=irow, column=2, columnspan=1,  sticky=tk.W, padx=10)
    irow += 1

    lab4 = tk.Label(top_getdata, text="End date (yyyy-mm-dd)")
    lab4.grid(row=irow, column=0, columnspan=2, sticky=tk.W, padx=20)
    ent_edate = tk.Entry(top_getdata, textvariable=tk_get_edate)
    ent_edate.grid(row=irow, column=2, columnspan=1, sticky=tk.W, padx=10)
    irow += 1

    mt2 = 'Choose the region boundaries'
    hlab2 = tk.Label(top_getdata, text=mt2)
    hlab2.grid(row=irow, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)
    irow += 1

    lab5 = tk.Label(top_getdata, text="North bound (-90.0 to 90.0)")
    lab5.grid(row=irow, column=0, columnspan=2, sticky=tk.W, padx=20)
    ent_n = tk.Entry(top_getdata, textvariable=tk_get_N)
    ent_n.grid(row=irow, column=2, columnspan=1, sticky=tk.W, padx=10)
    irow += 1

    lab6 = tk.Label(top_getdata, text="South bound (-90.0 to 90.0)")
    lab6.grid(row=irow, column=0, columnspan=2, sticky=tk.W, padx=20)
    ent_s = tk.Entry(top_getdata, textvariable=tk_get_S)
    ent_s.grid(row=irow, column=2, columnspan=1, sticky=tk.W, padx=10)
    irow += 1

    lab7 = tk.Label(top_getdata, text="East bound (-180.0 to 180.0)")
    lab7.grid(row=irow, column=0, columnspan=2, sticky=tk.W, padx=20)
    ent_e = tk.Entry(top_getdata, textvariable=tk_get_E)
    ent_e.grid(row=irow, column=2, columnspan=1, sticky=tk.W, padx=10)
    irow += 1

    lab8 = tk.Label(top_getdata, text="West bound (-180.0 to 180.0)")
    lab8.grid(row=irow, column=0, columnspan=2, sticky=tk.W, padx=20)
    ent_w = tk.Entry(top_getdata, textvariable=tk_get_W)
    ent_w.grid(row=irow, column=2, columnspan=1, sticky=tk.W, padx=10)
    irow += 1

    dir_button = tk.Button(top_getdata, text="Choose Folder", command=get_save_dir, padx=5)
    dir_button.grid(row=irow, column=0, sticky=tk.W, padx=10, pady=5)

    dd_button = tk.Button(top_getdata, text="Download Data", command=call_getdata, padx=5)
    dd_button.grid(row=irow, column=1, sticky=tk.W, padx=10, pady=5)

    close_button = tk.Button(top_getdata, text="Cancel", command=close_getdatawin, padx=5)
    close_button.grid(row=irow, column=2, sticky=tk.E, padx=10, pady=5)

    top_getdata.mainloop()


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
    with zipfile.ZipFile(zipfn, "r") as zip_ref:
        zip_ref.extractall(dn)
    os.remove(zipfn)

    info = f"Data has been downloaded into directory: {dn}"

    return info


if __name__ == '__main__':
    getdata()
