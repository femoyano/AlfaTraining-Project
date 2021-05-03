# GUI interface

"""
Use: tkinter, matplotlib backend, ...

Note:
Packing order is important. Widgets are processed sequentially and if there
is no space left, because the window is too small, they are not displayed.
The canvas is rather flexible in its size, so we pack it last which makes
sure the UI controls are displayed as long as possible.
"""

import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler  # default Matplotlib key bindings.
import matplotlib.pyplot as plt
# import matplotlib as mpl
import netCDF4 as nc
import get_data as gd


# Get data vars
climvars = [
    "near_surface_air_temperature",
    "daily_maximum_near_surface_air_temperature",
    "daily_minimum_near_surface_air_temperature",
    "precipitation"
    ]
timestep = ["monthly", "hourly"]
tk_save_dir = tk.StringVar()
tk_get_var = tk.StringVar()
tk_get_step = tk.StringVar()
tk_get_sdate = tk.StringVar()
tk_get_edate = tk.StringVar()
tk_get_N = tk.DoubleVar()
tk_get_E = tk.DoubleVar()
tk_get_S = tk.DoubleVar()
tk_get_W = tk.DoubleVar()
tk_message1 = tk.StringVar()

# Set defaults (coordinates for Germany)
tk_save_dir.set("./")
tk_get_var.set("near_surface_air_temperature")
tk_get_step.set("monthly")
tk_get_sdate.set("2020-01-01")
tk_get_sdate.set("2100-12-31")
tk_get_N.set(55.0)
tk_get_E.set(6.0)
tk_get_S.set(47.0)
tk_get_W.set(15.0)


def b1_open_file():
    global ds
    fpath = filedialog.askopenfilename(filetypes=[("netcdf", "*.nc"), ("All Files", "*.*")])
    ds = nc.Dataset(fpath, mode='r')


def b2_getdata():
    top_getdata = tk.Toplevel()
    top_getdata.grid()

    lab1 = tk.Label(top_getdata, text="Choose Variable")
    lab1.grid(row=0, column=0, clomnspan=2)
    for val, climvar in enumerate(climvars):  # enumerate generates tuples
        tk.Radiobutton(top_getdata,
                       text=climvar,
                       variable=tk_get_var,
                       indicatoron=1,
                       # command=,
                       value=climvar).grid(sticky=tk.W+tk.E)  # .grid(sticky=tk.W + tk.E)  # returns str

    lab2 = tk.Label(top_getdata, text="Choose Time Step")
    lab2.grid()
    for val, step in enumerate(timestep):  # enumerate generates tuples
        tk.Radiobutton(top_getdata,
                       text=timestep,
                       variable=tk_get_step,
                       indicatoron=1,
                       # command=,
                       value=step).grid(sticky=tk.W+tk.E)  # .grid(sticky=tk.W + tk.E)  # returns str

    lab3 = tk.Label(top_getdata, text="Start date (yyyy-mm-dd): ")
    lab3.grid()
    ent_sdate = tk.Entry(top_getdata, textvariable=tk_get_sdate)
    ent_sdate.grid()

    lab4 = tk.Label(top_getdata, text="End date (yyyy-mm-dd): ")
    lab4.grid()
    ent_edate = tk.Entry(top_getdata, textvariable=tk_get_edate)
    ent_edate.grid()

    lab5 = tk.Label(top_getdata, text="North bound (-90.0 to 90.0): ")
    lab5.grid()
    ent_N = tk.Entry(top_getdata, textvariable=tk_get_N)
    ent_N.grid()

    lab6 = tk.Label(top_getdata, text="South bound (-90.0 to 90.0): ")
    lab6.grid()
    ent_S = tk.Entry(top_getdata, textvariable=tk_get_S)
    ent_S.grid()

    lab7 = tk.Label(top_getdata, text="East bound (-180.0 to 180.0): ")
    lab7.grid()
    ent_E = tk.Entry(top_getdata, textvariable=tk_get_E)
    ent_E.grid()

    lab8 = tk.Label(top_getdata, text="West bound (-180.0 to 180.0): ")
    lab8.grid()
    ent_W = tk.Entry(top_getdata, textvariable=tk_get_W)
    ent_W.grid()

    dir_button = tk.Button(top_getdata, text="Save Folder", command=get_save_dir)
    dir_button.grid()

    dd_button = tk.Button(top_getdata, text="Download Data", command=call_get_data())
    dd_button.grid()

    close_button = tk.Button(top_getdata, text="Close", command=top_getdata.quit)
    close_button.grid()

    top_getdata.mainloop()


def b5_plot_time():
    b7.config(state="normal")
    b7.invoke()
    b7.flash()
    plot_time(x, y)
    canvas.draw()


def b7_clear():
    axes.cla()  # clear axes
    canvas.draw()


def get_save_dir():
    d = filedialog.askdirectory()
    tk_save_dir.set(d)


def call_get_data():
    gd.get_data(save_dir=str(tk_save_dir.get()),
                var=str(tk_get_var.get()),
                time_step=str(tk_get_step.get()),
                start_date=str(tk_get_sdate.get()),
                end_date=str(tk_get_edate.get()),
                north=float(tk_get_N.get()), south=float(tk_get_S.get()),
                east=float(tk_get_E.get()), west=float(tk_get_W.get())
                )


root = tk.Tk()
root.wm_title('Climate Projections')
frame_plot1 = tk.Frame(root)
frame_plot1.grid()  # (row=1, column=0)

fig = plt.Figure(figsize=(7, 6))
axes = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=frame_plot1)
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)

# Set pack_toolbar = false to use .grid geometry manager
toolbar = NavigationToolbar2Tk(canvas, frame_plot1, pack_toolbar=False)
toolbar.grid(row=0, column=0, sticky=tk.W)
toolbar.update()
# canvas.mpl_connect("key_press_event", key_press_handler)

# Make a button frame and populate
buttonframe = tk.Frame(root)
buttonframe.grid()  # row=0, column=0, sticky=tk.N + tk.W)

b1 = tk.Button(buttonframe, text="Load File", command=b1_open_file)
b1.grid()  # (row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

b2 = tk.Button(buttonframe, text="Get Data", command=b2_getdata)

b7 = tk.Button(buttonframe, text="Clear", command=b7_clear, activeforeground="red", state="disabled")
b7.grid()  # (row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

b8 = tk.Button(buttonframe, text="Quit", command=root.quit)
b8.grid()  # (row=0, column=1, sticky=tk.E+tk.N+tk.S, ipadx=10)

root.mainloop()
