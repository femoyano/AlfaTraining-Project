"""
Main file

Use: tkinter, matplotlib backend, ...

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
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import netCDF4 as nC
from get_data import getdata_gui
from stats import getstats
from plots import *
import itertools as it
import numpy as np


nc_ds = []
ds_vars = {}
nc_vars = []
act_var = ''
disp_vars = ['--- no file loaded ---']
known_vars = {'tas': 'Surface Air Temperature',
              'tasmax': 'Max Air Temperature',
              'tasmin': 'Min Air Temperature',
              'pr': 'Precipitation'}

main_gui = tk.Tk()  # create the gui root object
tk_sel_var = tk.StringVar()
tk_summary = tk.StringVar()
tk_summary.set('Select a variable to display summary info.')

# Figure ojects
fig1 = plt.Figure(figsize=(9, 6))
axes1 = fig1.add_subplot(111)


def make_gui():
    def b1_open_file():
        global nc_ds
        fpath = filedialog.askopenfilename(filetypes=[("netcdf", "*.nc"), ("All Files", "*.*")])
        if fpath:
            nc_ds.append(nC.Dataset(fpath, mode='r'))
            get_dsdata(nc_ds[0])
            c1['values'] = disp_vars
            c1.current(0)
            c1_entry_changed(1)
            # b4.config(state="normal")
            b5.config(state="normal")
            b6.config(state="normal")

    def b2_call_getdatagui():
        getdata_gui()

    def c1_entry_changed(event):
        global act_var
        sel_v = str(tk_sel_var.get())  # get the displayed variable
        if sel_v != '--- no file loaded ---':
            act_var = nc_vars[disp_vars.index(sel_v)]  # find the corresponding nc variable and set as active globally
            tk_summary.set(getstats(ds_vars, act_var, sel_v))  # pass to the function and set output to var

    def b5_call_plottime():
        # messagebox.showinfo("Info", "Sorry, function still under construction.")
        plot_time(ds_vars, act_var, str(tk_sel_var.get()))
        b7.config(state="normal")
        canvas1.draw()

    def b6_call_plotmap():
        messagebox.showinfo("Info", "Sorry, function still under construction.")
        # b7.invoke()
        # b7.flash()
        # cp.plot_map()
        # canvas.draw()
        # b7.config(state="normal")

    def b7_clear():
        axes1.cla()  # clear axes
        canvas1.draw()

    def b8_call_subset():
        messagebox.showinfo("Info", "Sorry, function still under construction.")

    def b9_close_root():
        main_gui.quit()
        main_gui.destroy()

    def b4_save_summary():
        messagebox.showinfo("Info", "Sorry, function still under construction.")

    def plot_time(ds, var, dvar):
        y = ds['time']
        x = ds[var]
        x = x.mean(axis=(1, 2))  # averages across lat and lon (i.e. entire region)
        ylab = ds['time_units']
        xlab = ds[var + '_units']
        title = dvar
        print(y[0],x[0],ylab, xlab, title)
        axes1.set_xlabel(xlab)
        axes1.set_ylabel(ylab)
        axes1.scatter(x, y, color="blue")

    def plot_map():
        pass

    main_gui.wm_title('Climate Projections')
    mainframe = tk.Frame(main_gui)
    mainframe.grid()  # (row=0, column=0)
    maxrow = 40

    # Make a button frame and populate
    # mainframe = tk.Frame(main_gui)
    # mainframe.grid(row=0, column=0, sticky=tk.N)  # row=0, column=0, sticky=tk.N + tk.W)
    irow = 0
    h1 = tk.Label(mainframe, text='MENU OPTIONS')
    h1.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b1 = tk.Button(mainframe, text="Load File", command=b1_open_file)  #, height=1)
    b1.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b2 = tk.Button(mainframe, text="Download Data", command=b2_call_getdatagui)
    b2.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b5 = tk.Button(mainframe, text="Plot Time", command=b5_call_plottime, state="disabled")
    b5.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b6 = tk.Button(mainframe, text="Plot Map", command=b6_call_plotmap, state="disabled")
    b6.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b7 = tk.Button(mainframe, text="Clear Map", command=b7_clear, activeforeground="red", state="disabled")
    b7.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b8 = tk.Button(mainframe, text="Subset Data", command=b8_call_subset, state="disabled")
    b8.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 3
    l1 = tk.Label(mainframe, text="Selected Variable")  # , command=c1_varselect)
    l1.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    c1 = ttk.Combobox(mainframe, textvariable=tk_sel_var, values=disp_vars, justify='center')
    c1.bind('<<ComboboxSelected>>', c1_entry_changed)
    c1.current(0)
    c1.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 3
    l2 = tk.Label(mainframe, text="Summary Info")
    l2.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    m1 = tk.Message(mainframe, relief='sunken', textvariable=tk_summary, justify='left', width=150)
    m1.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, padx=5, ipadx=5)
    irow += 1
    b4 = tk.Button(mainframe, text="Save Summary", command=b4_save_summary, state="disabled")
    b4.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=5, padx=30)
    irow += 1
    b9 = tk.Button(mainframe, text="Quit", command=b9_close_root)
    b9.grid(row=maxrow-1, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=5, padx=30, pady=10)

    # Create canvas for figures
    canvas1 = FigureCanvasTkAgg(fig1, master=mainframe)
    canvas1.get_tk_widget().grid(row=1, column=1, columnspan=1, rowspan=maxrow)
    axes1.grid()

    # Add a figure toolbar
    toolbar = NavigationToolbar2Tk(canvas1, mainframe, pack_toolbar=False)  # pack_toolbar = false to use .grid
    toolbar.grid(row=0, column=1, sticky=tk.W)
    toolbar.update()

    main_gui.mainloop()


def get_dsdata(ds):
    """
    Dimensions of single layer climate variables are time:lat:lon
    """
    global disp_vars
    global nc_vars
    global ds_vars

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
    ds_vars['max_lon'] = ds.variables['lon'][0].data
    ds_vars['min_lon'] = ds.variables['lon'][size_lon - 1].data

    # Get units of the dims
    ds_vars['time_units'] = ds.variables['time'].units
    ds_vars['lat_units'] = ds.variables['lat'].units
    ds_vars['lon_units'] = ds.variables['lon'].units

    for n in nc_vars:
        v = ds.variables[n][:, :, :]
        ds_vars[n] = np.ma.asarray(v)
        ds_vars[n + '_units'] = ds.variables[n].units

    print(f"Variables in this file are: {str(nc_vars).strip('[]')}")
    print(f"Dimensions in this file are: {str(nc_dims).strip('[]')}")


make_gui()
