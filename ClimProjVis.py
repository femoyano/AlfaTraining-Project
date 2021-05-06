"""
Climate Projections Visualizer:
- Download projected (modeled) climate data
- Get summary statistics
- Visualize data

This file contains the entire programm code.
"""

# from matplotlib.backend_bases import key_press_handler  # default Matplotlib key bindings.
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinter import font
# from matplotlib.figure import Figure
# import seaborn as sns
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
import json

# Defining global variables ----

nc_ds = []
ds_vars = {}
nc_vars = []
active = []
sumdict = {}
filename = ""
none = '--- none ---'
loaded_vars = {none: []}
known_vars = {'tas': ('Surface Air Temperature', 'orangered'),
              'tasmax': ('Max Air Temperature', 'red'),
              'tasmin': ('Min Air Temperature', 'darkorange'),
              'pr': ('Precipitation', 'royalblue')}


# Function declarations ----

def make_gui():
    """
    This is the starting function. It crates the main interface and plots data
    :return: none
    """
    global loaded_vars

    def b1_open_file():
        global nc_ds
        global loaded_vars
        fpath = filedialog.askopenfilename(filetypes=[("netcdf", "*.nc"), ("All Files", "*.*")])
        if fpath:
            loaded_vars = {}
            nc_ds = nC.Dataset(fpath, mode='r')
            get_dsdata(nc_ds)
            nc_ds.close()
            c1['values'] = list(loaded_vars.keys())
            c1.current(0)
            c1_entry_changed(1)

    def b2_call_getdatagui():
        getdata_gui()

    def c1_entry_changed(event):
        global active
        global sumdict
        sel_v = str(tk_sel_var.get())  # get the displayed variable
        if sel_v == none:
            b5.config(state="disabled")
            b6.config(state="disabled")
            b4.config(state="disabled")
        else:
            active = loaded_vars[sel_v]  # find corresponding nc var and set as active
            ss, sumdict = getstats(ds_vars, active[0], sel_v)
            tk_summary.set(ss)  # pass to the function and set output to var
            b5.config(state="normal")
            b6.config(state="normal")
            b4.config(state="normal")

    def b5_plottime():
        b7.config(state="normal")
        x = ds_vars['time']
        y = ds_vars[active[0]]
        y = y.mean(axis=(1, 2))  # averages across lat and lon (i.e. entire region)
        xlab = ds_vars['time_units']
        ylab = ds_vars[active[0] + '_units']
        ax1.title.set_text(str(tk_sel_var.get()) + ' (averaged over space for selected time)')
        ax1.set_xlabel(xlab)
        ax1.set_ylabel(ylab)
        ax1.plot(x, y, color=active[1])
        # plot_time(ds_vars, active[0], str(tk_sel_var.get()))
        canvas1.draw()
        b7.config(state="normal")

    def b6_plotmap():
        lat = ds_vars['lat']
        lon = ds_vars['lon']
        val = ds_vars[active[0]]
        val = val.mean(axis=0)
        unit = ds_vars[active[0] + '_units']

        ax2 = fig2.add_subplot(111, projection=ccrs.PlateCarree())
        ax2.set_global()
        ax2.add_feature(ct.feature.BORDERS, linestyle=':')
        ax2.add_feature(ct.feature.OCEAN)
        ax2.add_feature(ct.feature.COASTLINE)
        ax2.title.set_text(str(tk_sel_var.get()) + ' (averaged over time for selected region)')
        # ax2.gridlines(draw_labels=True)  # conflict with colorbar
        cf = ax2.contourf(lon, lat, val, 60, transform=ccrs.PlateCarree(), )
        cb = fig2.colorbar(cf, ax=ax2, orientation="vertical", pad=0.02, aspect=16, shrink=0.8)
        cb.set_label(unit, size=12, rotation=270, labelpad=15)
        cb.ax.tick_params(labelsize=10)
        canvas2.draw()
        b10.config(state="normal")

    def b_clear_time():
        ax1.cla()
        canvas1.draw()
        b7.config(state="disabled")

    def b_clear_map():
        fig2.clf()
        ax2 = fig2.add_subplot(111, projection=ccrs.PlateCarree())
        ax2.set_global()
        ax2.add_feature(ct.feature.BORDERS, linestyle=':')
        ax2.add_feature(ct.feature.OCEAN)
        ax2.add_feature(ct.feature.COASTLINE)
        canvas2.draw()
        b10.config(state="disabled")

    def b8_call_subset():
        messagebox.showinfo("Info", "Sorry, function still under construction.")

    def b9_close_root():
        main_gui.quit()
        main_gui.destroy()

    def b4_save_summary():
        with open('summary.json', 'w') as fp:
            json.dump(sumdict, fp)

    main_gui = tk.Tk()  # create the gui root object
    tk_sel_var = tk.StringVar()
    tk_summary = tk.StringVar()
    tk_summary.set('Select a variable to display summary info.')
    font1 = font.Font(family='mincho')  # Issue: font rendering does not seem to work well.
    # font1 = font.Font(family='latin modern roman')  # Issue: font rendering does not seem to work well.

    main_gui.wm_title('Climate Projections Visualizer')

    tbarframe1 = tk.Frame(main_gui)
    tbarframe1.grid(row=0, column=1)
    plotframe1 = tk.Frame(main_gui)
    plotframe1.grid(row=1, column=1)
    tbarframe2 = tk.Frame(main_gui)
    tbarframe2.grid(row=2, column=1)
    plotframe2 = tk.Frame(main_gui)
    plotframe2.grid(row=3, column=1)

    # Figures, canvas and axes and toolbar
    # sns.set_theme()
    # sns.set_style("whitegrid")
    plt.style.use("ggplot")
    fig1 = plt.Figure(figsize=(9, 4))
    ax1 = fig1.add_subplot(111)
    canvas1 = FigureCanvasTkAgg(fig1, master=plotframe1)
    toolbar1 = NavigationToolbar2Tk(canvas1, tbarframe1)  # pack_toolbar = false to use .grid
    toolbar1.pack()  # grid(row=0, column=0, sticky=tk.W)
    toolbar1.update()
    canvas1.get_tk_widget().pack(padx=10, pady=0)  # grid(row=1, column=0)

    # Figures, canvas and axes
    fig2 = plt.Figure(figsize=(9, 4))
    canvas2 = FigureCanvasTkAgg(fig2, master=plotframe2)
    # Create figure toolbar object
    toolbar2 = NavigationToolbar2Tk(canvas2, tbarframe2)  # pack_toolbar = false to use .grid
    toolbar2.pack()  # grid(row=0, column=0, sticky=tk.W)
    canvas2.get_tk_widget().pack(padx=10, pady=0)  # grid(row=1, column=0)
    ax2 = fig2.add_subplot(111, projection=ccrs.PlateCarree())
    ax2.set_global()
    ax2.add_feature(ct.feature.BORDERS, linestyle=':')
    ax2.add_feature(ct.feature.OCEAN)
    ax2.add_feature(ct.feature.COASTLINE)
    canvas2.draw()
    toolbar2.update()

    # Buttons
    buttonframe = tk.Frame(main_gui)
    buttonframe.grid(row=0, column=0, rowspan=4)

    irow = 0
    h1 = tk.Label(buttonframe, text='MENU OPTIONS')
    h1.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=3)
    irow += 1
    b1 = tk.Button(buttonframe, text="Load File", command=b1_open_file)
    b1.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=3)
    irow += 1
    b2 = tk.Button(buttonframe, text="Download Data", command=b2_call_getdatagui)
    b2.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=3)
    irow += 1
    b5 = tk.Button(buttonframe, text="Plot Time", command=b5_plottime, state="disabled")
    b5.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=3)
    irow += 1
    b7 = tk.Button(buttonframe, text="Clear Time Plot", command=b_clear_time, state="disabled")
    b7.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=3)
    irow += 1
    b6 = tk.Button(buttonframe, text="Plot Map", command=b6_plotmap, state="disabled")
    b6.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=3)
    irow += 1
    b10 = tk.Button(buttonframe, text="Clear Map", command=b_clear_map, state="disabled")
    b10.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=3)
    irow += 1
    b8 = tk.Button(buttonframe, text="Subset Data", command=b8_call_subset, state="disabled")
    b8.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=3)
    irow += 3
    b4 = tk.Button(buttonframe, text="Save Summary", command=b4_save_summary, state="disabled")
    b4.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=3)
    irow += 1
    l1 = tk.Label(buttonframe, text="Selected Variable")  # , command=c1_varselect)
    l1.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=3)
    irow += 1
    c1 = ttk.Combobox(buttonframe, textvariable=tk_sel_var, values=list(loaded_vars.keys()), justify='center')
    c1.bind('<<ComboboxSelected>>', c1_entry_changed)
    c1.current(0)
    c1.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=3)
    irow += 3
    l2 = tk.Label(buttonframe, text="Summary Info")
    l2.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=3)
    irow += 1
    m1 = tk.Message(buttonframe, relief='sunken', textvariable=tk_summary, justify='left', width=200)
    m1.grid(row=irow, column=0, sticky=tk.E + tk.W, padx=10, ipadx=0)
    irow += 1
    b9 = tk.Button(buttonframe, text="Quit", command=b9_close_root)
    b9.grid(row=irow, column=0, sticky=tk.E + tk.W, ipadx=5, padx=30, pady=30)

    main_gui.mainloop()


def getdata_gui():
    """
    getdata_gui() creates a window for user configuration of a climate data download request.
    :return: none
    """
    # Define vars for data download
    climvars = [
        "near_surface_air_temperature",
        "daily_maximum_near_surface_air_temperature",
        "daily_minimum_near_surface_air_temperature",
        "precipitation"
    ]
    timestep = ["monthly", "daily"]
    scenario = ['ssp1_2_3', 'ssp2_4_5', 'ssp3_7_0', 'ssp5_8_5']

    def get_save_dir():
        d = filedialog.askdirectory()
        tk_save_dir.set(d)

    def call_getdata():
        info = getdata(var=str(tk_get_var.get()),
                       time_step=str(tk_get_step.get()),
                       scenario=str(tk_get_scen.get()),
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
    tk_get_scen = tk.StringVar()
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
    tk_get_scen.set("ssp2_4_5")
    tk_get_sdate.set("2020-01-01")
    tk_get_edate.set("2030-12-31")
    tk_north.set(55.0)
    tk_east.set(15.0)
    tk_south.set(46.0)
    tk_west.set(6.0)

    irow = 0
    lab1 = tk.Label(top_getdata, text="Variable", justify='left')
    lab1.grid(row=irow, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
    irow += 1

    for val, climvar in enumerate(climvars):  # enumerate generates tuples
        tk.Radiobutton(top_getdata,
                       text=climvar,
                       variable=tk_get_var,
                       indicatoron=1,
                       # command=,
                       value=climvar).grid(row=irow, column=0, columnspan=3, sticky=tk.W, padx=20)
        irow += 1

    lab2 = tk.Label(top_getdata, text="Frequency", justify='left')
    lab2.grid(row=irow, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
    irow += 1

    for val, step in enumerate(timestep):  # enumerate generates tuples
        tk.Radiobutton(top_getdata,
                       text=step,
                       variable=tk_get_step,
                       indicatoron=1,
                       # command=,
                       value=step).grid(row=irow, column=0, columnspan=3, sticky=tk.W, padx=20)  # returns str
        irow += 1

    lab9 = tk.Label(top_getdata, text="Scenario (higher number -> more global warming)", justify='left')
    lab9.grid(row=irow, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
    irow += 1

    for val, scen in enumerate(scenario):  # enumerate generates tuples
        tk.Radiobutton(top_getdata,
                       text=scen,
                       variable=tk_get_scen,
                       indicatoron=1,
                       # command=,
                       value=scen).grid(row=irow, column=0, columnspan=3, sticky=tk.W, padx=20)  # returns str
        irow += 1

    mt1 = 'Choose a time range between 2020-01-01 and 2300-12-31'
    hlab1 = tk.Label(top_getdata, text=mt1)
    hlab1.grid(row=irow, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)
    irow += 1

    lab3 = tk.Label(top_getdata, text="Start date (yyyy-mm-dd)")
    lab3.grid(row=irow, column=0, columnspan=2, sticky=tk.W, padx=20)
    ent_sdate = tk.Entry(top_getdata, textvariable=tk_get_sdate)
    ent_sdate.grid(row=irow, column=2, columnspan=1, sticky=tk.W, padx=10)
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
            scenario,
            start_date,
            end_date,
            north, south, east, west,
            model='mpi_esm1_2_lr',
            save_dir="./"
            ):
    """
    Download climate data using the API from cds.climate.cpernicus.eu
    For this data request to work, one must first create a user account
    and follow the instructions for setting up the API (install cdsapi package and create file $HOME/.cdsapirc)
    """

    dates = start_date + '/' + end_date
    coord = south + '_' + north + '_' + east + '_' + west
    dn = save_dir + '/' + var + '_' + time_step + '_' + start_date + '_' + end_date + '_' + scenario + coord
    zipfn = dn + '.zip'

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


def get_dsdata(ds):
    """
    This function extracts data from a netCDF object.
    Argument ds is a netcdf dataset.
    Returns none but modifies global variables.
    """
    global loaded_vars
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

    # Add to display variables (using long name if known)
    for v in nc_vars:
        if v in known_vars.keys():
            loaded_vars[known_vars[v][0]] = [v, known_vars[v][1]]
        else:
            loaded_vars[v] = [v, 'dimgray']

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
        v = ds.variables[n][:, :, :]  # Note: Dimensions of single layer climate variables are time:lat:lon
        ds_vars[n] = np.ma.asarray(v)
        ds_vars[n + '_units'] = ds.variables[n].units

    # print(f"Variables in this file are: {str(nc_vars).strip('[]')}")
    # print(f"Dimensions in this file are: {str(nc_dims).strip('[]')}")


def getstats(ds_v, act_v, dis_v):
    """
    Function obtains summary data for the active climate variable
    :param ds_v:
    :param act_v:
    :param dis_v:
    :return: A string with text describing the data summary values.
    """
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

    sd = {'variable': str(dis_v), 'units': str(var_units), 'overall mean': var_m, 'stdev': var_sd,
          'max_lat': str(north), 'min_lat': str(south), 'max_lon': str(east), 'min_lon': str(west)}

    s = ['\n' + 'Variable: ' + '\n' +
         str(dis_v) + '\n\n' +
         'Units: ' + str(var_units) + '\n\n' +
         'Overall Mean: ' + str(var_m) + '\n\n' +
         'St.Dev: ' + str(var_sd) + '\n\n' +
         'Region Coordinates: ' + '\n\n' +
         str(lat_units) + ': ' + str(south) + ' to ' + str(north) + '\n\n' +
         str(lon_units) + ': ' + str(west) + ' to ' + str(east)]

    return s[0], sd


# Start the program ----

if __name__ == '__main__':
    make_gui()
