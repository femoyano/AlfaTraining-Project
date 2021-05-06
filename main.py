"""
Main file

Note:
Packing order is important. Widgets are processed sequentially and if there
is no space left, because the window is too small, they are not displayed.
The canvas is rather flexible in its size, so we pack it last which makes
sure the UI controls are displayed as long as possible.

Check kap_19_tkinter_validate1 for callback functions validating inputs
"""

# from matplotlib.backend_bases import key_press_handler  # default Matplotlib key bindings.
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import netCDF4 as nC
import cartopy as ct
import cartopy.crs as ccrs
import numpy as np
import itertools as it
import cdsapi
import zipfile
import os


nc_ds = []
ds_vars = {}
nc_vars = []
act_var = ''
disp_vars = ['--- no file loaded ---']
known_vars = {'tas': 'Surface Air Temperature',
              'tasmax': 'Max Air Temperature',
              'tasmin': 'Min Air Temperature',
              'pr': 'Precipitation'}


def make_gui():
    def b1_open_file():
        global nc_ds
        fpath = filedialog.askopenfilename(filetypes=[("netcdf", "*.nc"), ("All Files", "*.*")])
        if fpath:
            nc_ds = nC.Dataset(fpath, mode='r')
            get_dsdata(nc_ds)
            nc_ds.close()
            c1['values'] = disp_vars
            c1.current(0)
            c1_entry_changed(1)
            b5.config(state="normal")
            b6.config(state="normal")
            b4.config(state="normal")

    def b2_call_getdatagui():
        getdata_gui()

    def c1_entry_changed(event):
        global act_var
        sel_v = str(tk_sel_var.get())  # get the displayed variable
        if sel_v != '--- no file loaded ---':
            act_var = nc_vars[disp_vars.index(sel_v)]  # find the corresponding nc variable and set as active globally
            tk_summary.set(getstats(ds_vars, act_var, sel_v))  # pass to the function and set output to var

    def b5_plottime():
        b7.config(state="normal")
        x = ds_vars['time']
        y = ds_vars[act_var]
        y = y.mean(axis=(1, 2))  # averages across lat and lon (i.e. entire region)
        xlab = ds_vars['time_units']
        ylab = ds_vars[act_var + '_units']
        ax1.title.set_text(str(tk_sel_var.get())+': average temporal change in the region')
        ax1.set_xlabel(xlab)
        ax1.set_ylabel(ylab)
        ax1.plot(x, y, color="blue")
        # plot_time(ds_vars, act_var, str(tk_sel_var.get()))
        canvas1.draw()

    def b6_plotmap():
        lat = ds_vars['lat']
        lon = ds_vars['lon']
        val = ds_vars[act_var]
        val = val.mean(axis=0)
        unit = ds_vars[act_var + '_units']

        ax2 = fig2.add_subplot(111, projection=ccrs.PlateCarree())
        ax2.set_global()
        ax2.add_feature(ct.feature.BORDERS, linestyle=':')
        ax2.add_feature(ct.feature.OCEAN)
        ax2.add_feature(ct.feature.COASTLINE)
        # ax2.coastlines()
        ax1.title.set_text(str(tk_sel_var.get())+': average spatial values over time period')
        cf = ax2.contourf(lon, lat, val, 60, transform=ccrs.PlateCarree(), )
        cb = fig2.colorbar(cf, ax=ax2, orientation="vertical", pad=0.02, aspect=16, shrink=0.8)
        cb.set_label(unit, size=12, rotation=270, labelpad=15)
        cb.ax.tick_params(labelsize=10)

        canvas2.draw()

        b7.config(state="normal")

    def b7_clear():
        ax1.cla()
        fig2.clf()
        canvas1.draw()
        canvas2.draw()

    def b8_call_subset():
        messagebox.showinfo("Info", "Sorry, function still under construction.")

    def b9_close_root():
        main_gui.quit()
        main_gui.destroy()

    def b4_save_summary():
        messagebox.showinfo("Info", "Sorry, function still under construction.")

    main_gui = tk.Tk()  # create the gui root object
    tk_sel_var = tk.StringVar()
    tk_summary = tk.StringVar()
    tk_summary.set('Select a variable to display summary info.')

    main_gui.wm_title('Climate Projections')
    mainframe = tk.Frame(main_gui)
    mainframe.grid()  # (row=0, column=0)
    maxrow = 40
    midrow = 20

    # Figures, canvas and axes
    fig1 = plt.Figure(figsize=(9, 4))
    ax1 = fig1.add_subplot(111)
    ax1.grid()
    canvas1 = FigureCanvasTkAgg(fig1, master=mainframe)
    canvas1.get_tk_widget().grid(row=1, column=1, columnspan=1, rowspan=midrow - 1)
    # Create figure toolbar object
    toolbar1 = NavigationToolbar2Tk(canvas1, mainframe, pack_toolbar=False)  # pack_toolbar = false to use .grid
    toolbar1.grid(row=0, column=1, sticky=tk.W)
    toolbar1.update()

    # Figures, canvas and axes
    fig2 = plt.Figure(figsize=(9, 4))
    canvas2 = FigureCanvasTkAgg(fig2, master=mainframe)
    canvas2.get_tk_widget().grid(row=midrow + 1, column=1, columnspan=1, rowspan=maxrow)
    canvas2.draw()
    # Create figure toolbar object
    toolbar2 = NavigationToolbar2Tk(canvas2, mainframe, pack_toolbar=False)  # pack_toolbar = false to use .grid
    toolbar2.grid(row=midrow, column=1, sticky=tk.W)
    toolbar2.update()

    # Buttons
    irow = 0
    h1 = tk.Label(mainframe, text='MENU OPTIONS')
    h1.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b1 = tk.Button(mainframe, text="Load File", command=b1_open_file)
    b1.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b2 = tk.Button(mainframe, text="Download Data", command=b2_call_getdatagui)
    b2.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b5 = tk.Button(mainframe, text="Plot Time", command=b5_plottime, state="disabled")
    b5.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b6 = tk.Button(mainframe, text="Plot Map", command=b6_plotmap, state="disabled")
    b6.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b7 = tk.Button(mainframe, text="Clear Plots", command=b7_clear, state="disabled")
    b7.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b8 = tk.Button(mainframe, text="Subset Data", command=b8_call_subset, state="disabled")
    b8.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 3
    l1 = tk.Label(mainframe, text="Selected Variable")  # , command=c1_varselect)
    l1.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    c1 = ttk.Combobox(mainframe, textvariable=tk_sel_var, values=disp_vars, justify='center')
    c1.bind('<<ComboboxSelected>>', c1_entry_changed)
    c1.current(0)
    c1.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 3
    l2 = tk.Label(mainframe, text="Summary Info")
    l2.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    m1 = tk.Message(mainframe, relief='sunken', textvariable=tk_summary, justify='left', width=180)
    m1.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, padx=5, ipadx=5)
    irow += 1
    b4 = tk.Button(mainframe, text="Save Summary", command=b4_save_summary, state="disabled")
    b4.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b9 = tk.Button(mainframe, text="Quit", command=b9_close_root)
    b9.grid(row=irow, column=0, sticky=tk.S + tk.E + tk.W, ipadx=5, padx=30, pady=30)

    main_gui.mainloop()


def get_dsdata(ds):
    """
    Dimensions of single layer climate variables are time:lat:lon
    """
    global disp_vars
    global nc_vars
    global ds_vars
    global known_vars

    nc_vars = list(ds.variables.keys())
    nc_dims = list(ds.dimensions.keys())
    nc_dims.append('height')

    isvar = [True] * len(nc_vars)
    for i in range(len(nc_vars)):
        for d in nc_dims:
            if nc_vars[i].find(d) != -1:
                isvar[i] = False
    nc_vars = list(it.compress(nc_vars, isvar))  # removing dimension variables

    # Add to display variables (using display name if available)
    disp_vars = []
    for v in nc_vars:
        if v in known_vars.keys():
            disp_vars.append(known_vars[v])
        else:
            disp_vars.append(v)

    # Get the values of the dimension variables (as type 'numpy.ma.core.MaskedArray')
    lat = ds.variables['lat'][:]
    lon = ds.variables['lon'][:]
    time = ds.variables['time'][:]
    ds_vars['lat'] = np.ma.asarray(lat)  # Is this step necessary?
    ds_vars['lon'] = np.ma.asarray(lon)
    ds_vars['time'] = np.ma.asarray(time)

    # Get min and max values of dims (lat, lon)
    size_lat = ds.variables['lat'].size
    size_lon = ds.variables['lon'].size
    ds_vars['min_lat'] = ds.variables['lat'][0].data
    ds_vars['max_lat'] = ds.variables['lat'][size_lat - 1].data
    ds_vars['min_lon'] = ds.variables['lon'][0].data
    ds_vars['max_lon'] = ds.variables['lon'][size_lon - 1].data

    # Get units of the dims
    ds_vars['time_units'] = ds.variables['time'].units
    ds_vars['lat_units'] = ds.variables['lat'].units
    ds_vars['lon_units'] = ds.variables['lon'].units

    for n in nc_vars:
        v = ds.variables[n][:, :, :]
        ds_vars[n] = np.ma.asarray(v)
        ds_vars[n + '_units'] = ds.variables[n].units

    # print(f"Variables in this file are: {str(nc_vars).strip('[]')}")
    # print(f"Dimensions in this file are: {str(nc_dims).strip('[]')}")


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
        info = getdata(var=str(tk_get_var.get()),
                       time_step=str(tk_get_step.get()),
                       start_date=str(tk_get_sdate.get()),
                       end_date=str(tk_get_edate.get()),
                       north=float(tk_north.get()), south=float(tk_south.get()),
                       east=float(tk_east.get()), west=float(tk_west.get()),
                       save_dir=str(tk_save_dir.get())
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
    tk_north = tk.DoubleVar()
    tk_east = tk.DoubleVar()
    tk_south = tk.DoubleVar()
    tk_west = tk.DoubleVar()
    # Set defaults (default coordinates given for Germany)
    tk_save_dir.set(".")
    tk_get_var.set("near_surface_air_temperature")
    tk_get_step.set("monthly")
    tk_get_sdate.set("2020-01-01")
    tk_get_edate.set("2030-12-31")
    tk_north.set(55.0)
    tk_east.set(15.0)
    tk_south.set(46.0)
    tk_west.set(6.0)

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
                       value=climvar).grid(row=irow, column=0, columnspan=3,  sticky=tk.W, padx=20)
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
    ent_n = tk.Entry(top_getdata, textvariable=tk_north)
    ent_n.grid(row=irow, column=2, columnspan=1, sticky=tk.W, padx=10)
    irow += 1

    lab6 = tk.Label(top_getdata, text="South bound (-90.0 to 90.0)")
    lab6.grid(row=irow, column=0, columnspan=2, sticky=tk.W, padx=20)
    ent_s = tk.Entry(top_getdata, textvariable=tk_south)
    ent_s.grid(row=irow, column=2, columnspan=1, sticky=tk.W, padx=10)
    irow += 1

    lab7 = tk.Label(top_getdata, text="East bound (-180.0 to 180.0)")
    lab7.grid(row=irow, column=0, columnspan=2, sticky=tk.W, padx=20)
    ent_e = tk.Entry(top_getdata, textvariable=tk_east)
    ent_e.grid(row=irow, column=2, columnspan=1, sticky=tk.W, padx=10)
    irow += 1

    lab8 = tk.Label(top_getdata, text="West bound (-180.0 to 180.0)")
    lab8.grid(row=irow, column=0, columnspan=2, sticky=tk.W, padx=20)
    ent_w = tk.Entry(top_getdata, textvariable=tk_west)
    ent_w.grid(row=irow, column=2, columnspan=1, sticky=tk.W, padx=10)
    irow += 1

    dir_button = tk.Button(top_getdata, text="Choose Folder", command=get_save_dir, padx=5)
    dir_button.grid(row=irow, column=0, sticky=tk.W, padx=10, pady=5)

    dd_button = tk.Button(top_getdata, text="Download Data", command=call_getdata, padx=5)
    dd_button.grid(row=irow, column=1, sticky=tk.W, padx=10, pady=5)

    close_button = tk.Button(top_getdata, text="Cancel", command=close_getdatawin, padx=5)
    close_button.grid(row=irow, column=2, sticky=tk.E, padx=10, pady=5)

    top_getdata.mainloop()


def getdata(var,
            time_step,
            start_date,
            end_date,
            north, south, east, west,
            experiment='ssp2_4_5',
            model='mpi_esm1_2_lr',
            save_dir="./"
            ):
    """
    Download climate data using the API from cds.climate.cpernicus.eu
    For this data request to work, one must first create a user account
    and follow the instructions for setting up the API (install cdsapi package and create file $HOME/.cdsapirc)
    """

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


def getstats(ds_v, act_v, dis_v):
    # Get some ifno and stats
    var = ds_v[act_v]
    var_m = round(var.mean(), 8)
    var_sd = round(var_m / len(var) ** 0.5, 8)
    # var_m = var.mean()
    # var_sd = var_m / len(var) ** 0.5
    var_sm = var.mean(axis=(1, 2))  # get the spatial mean (keeps the time dimension)
    var_tm = var.mean(axis=0)  # get of mean over time (keeps lat/lon)
    var_sm_sd = var_sm / len(var_sm) ** 0.5
    var_tm_sd = var_tm / len(var_tm) ** 0.5
    var_units = ds_v[act_v + '_units']
    north = np.around(ds_v['max_lat'], 2)
    south = np.around(ds_v['min_lat'], 2)
    east = np.around(ds_v['max_lon'], 2)
    west = np.around(ds_v['min_lon'], 2)
    lat_units = ds_v['lat_units']
    lon_units = ds_v['lon_units']

    s = ['\n'+'Variable: ' + str(dis_v) + '\n' +
         'Units: ' + str(var_units) + '\n' +
         'Overall Mean: ' + str(var_m) + '\n' +
         'Standard Deviation: ' + str(var_sd) + '\n' +
         'Region coordinates: ' + '\n' +
         str(south) + ' to ' + str(north) + ' ' + str(lat_units) + '\n' +
         str(west) + ' to ' + str(east) + ' ' + str(lon_units) + '\n']

    return s[0]


if __name__ == '__main__':
    make_gui()
