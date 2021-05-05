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
disp_vars = ['--- no file loaded ---']
known_vars = {'tas': 'Surface Air Temperature',
              'tasmax': 'Max Air Temperature',
              'tasmin': 'Min Air Temperature',
              'pr': 'Precipitation'}

main_gui = tk.Tk()  # create the gui root object
tk_sel_var = tk.StringVar()
tk_summary = tk.StringVar()
tk_summary.set('Select a variable to display summary info.')


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
        sel_v = str(tk_sel_var.get())  # get the displayed variable
        if sel_v != '--- no file loaded ---':
            act_v = nc_vars[disp_vars.index(sel_v)]  # find the corresponding nc variable
            tk_summary.set(getstats(ds_vars, act_v, sel_v))  # pass to the function and set output to var

    def b5_call_plottime():
        messagebox.showinfo("Info", "Sorry, function still under construction.")
        # plot_time(x, y)
        # canvas.draw()
        b7.config(state="normal")

    def b6_call_plotmap():
        messagebox.showinfo("Info", "Sorry, function still under construction.")
        # b7.invoke()
        # b7.flash()
        # cp.plot_map()
        # canvas.draw()
        # b7.config(state="normal")

    def b7_clear():
        axes.cla()  # clear axes
        canvas.draw()

    def b8_call_subset():
        messagebox.showinfo("Info", "Sorry, function still under construction.")

    def b9_close_root():
        main_gui.quit()
        main_gui.destroy()

    def b4_save_summary():
        messagebox.showinfo("Info", "Sorry, function still under construction.")

    main_gui.wm_title('Climate Projections')

    # Create a plotting frame
    plotframe = tk.Frame(main_gui)
    plotframe.grid(row=0, rowspan=9, column=1)  # (row=1, column=0)
    fig = plt.Figure(figsize=(7, 6))
    axes = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=plotframe)
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)
    # Set pack_toolbar = false to use .grid geometry manager
    toolbar = NavigationToolbar2Tk(canvas, plotframe, pack_toolbar=False)
    toolbar.grid(row=0, column=0, sticky=tk.W)
    toolbar.update()
    # canvas.mpl_connect("key_press_event", key_press_handler)

    # Make a button frame and populate
    buttonframe = tk.Frame(main_gui)
    buttonframe.grid(row=0, column=0, sticky=tk.N)  # row=0, column=0, sticky=tk.N + tk.W)
    irow = 0
    b1 = tk.Button(buttonframe, text="Load File", command=b1_open_file)
    b1.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=30)
    irow += 1
    b2 = tk.Button(buttonframe, text="Download Data", command=b2_call_getdatagui)
    b2.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    l1 = tk.Label(buttonframe, text="Selected Variable")  # , command=c1_varselect)
    l1.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    c1 = ttk.Combobox(buttonframe, textvariable=tk_sel_var, values=disp_vars, justify='center')
    c1.bind('<<ComboboxSelected>>', c1_entry_changed)
    c1.current(0)
    c1.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    b5 = tk.Button(buttonframe, text="Plot Time", command=b5_call_plottime, state="disabled")
    b5.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    b6 = tk.Button(buttonframe, text="Plot Map", command=b6_call_plotmap, state="disabled")
    b6.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    b7 = tk.Button(buttonframe, text="Clear Map", command=b7_clear, activeforeground="red", state="disabled")
    b7.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    b8 = tk.Button(buttonframe, text="Subset Data", command=b8_call_subset, state="disabled")
    b8.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    l2 = tk.Label(buttonframe, text="Summary Info")
    l2.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    m1 = tk.Message(buttonframe, relief='sunken', textvariable=tk_summary, justify='left', width=200)
    m1.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, padx=5, ipadx=5)
    irow += 1
    b4 = tk.Button(buttonframe, text="Save Summary Info", command=b4_save_summary, state="disabled")
    b4.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    b9 = tk.Button(buttonframe, text="Quit", command=b9_close_root)
    b9.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1

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
