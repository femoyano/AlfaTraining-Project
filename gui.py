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

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# from matplotlib.backend_bases import key_press_handler  # default Matplotlib key bindings.
import matplotlib.pyplot as plt
# import matplotlib as mpl
import netCDF4 as nC
from get_data import getdata_gui
# from climate_stats import *ge
# from climate_plots import *
from var_select import Combo
from process_ds import process_ds


ncsets = []
ncvars = []
ncdims = []
lat = []
lon = []
time = []

main_gui = tk.Tk()  # create the gui root object
tk_ds_varnames = tk.Variable()
tk_ds_varnames.set(["-- No file loaded --"])
tk_active_var = tk.StringVar()


def make_gui():
    def b1_open_file():
        global ncsets
        fpath = filedialog.askopenfilename(filetypes=[("netcdf", "*.nc"), ("All Files", "*.*")])
        ncsets.append(nC.Dataset(fpath, mode='r'))
        process_ds(ncsets[0])

    def b2_call_getdatagui():
        getdata_gui()

    def b4_getstats():
        pass
        # stats = getstats(ncsets[0], var)

    def b5_call_plottime():
        messagebox.showinfo("Info", "Sorry, function still under construction.")
        # b7.config(state="normal")
        # plot_time(x, y)
        # canvas.draw()

    def b6_call_plotmap():
        messagebox.showinfo("Info", "Sorry, function still under construction.")
        # b7.config(state="normal")
        # b7.invoke()
        # b7.flash()
        # cp.plot_map()
        # canvas.draw()

    def b7_clear():
        axes.cla()  # clear axes
        canvas.draw()

    def b8_call_subset():
        messagebox.showinfo("Info", "Sorry, function still under construction.")

    def b9_close_root():
        main_gui.quit()

    def c1_entry_changed():
        pass

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
    b1 = tk.Button(buttonframe, text="Load file", command=b1_open_file)
    b1.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    b2 = tk.Button(buttonframe, text="Get data", command=b2_call_getdatagui)
    b2.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    l1 = tk.Label(buttonframe, text="Select variable")  # , command=c1_varselect)
    l1.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    # c1 = ttk.Combobox(buttonframe, textvariable=tk_active_var)
    # c1.bind('<<ComboboxSelected>>', c1_entry_changed)
    # c1['values'] = ['X', 'Y', 'Z']
    # c1.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W, ipadx=10)
    c1 = Combo(buttonframe)
    c1.create()
    c1.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    b4 = tk.Button(buttonframe, text="Summary stats", command=b4_getstats, state="disabled")
    b4.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    b5 = tk.Button(buttonframe, text="Plot time", command=b5_call_plottime, state="disabled")
    b5.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    b6 = tk.Button(buttonframe, text="Plot map", command=b6_call_plotmap, state="disabled")
    b6.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    b7 = tk.Button(buttonframe, text="Clear", command=b7_clear, activeforeground="red", state="disabled")
    b7.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    b8 = tk.Button(buttonframe, text="Subset data", command=b8_call_subset, state="disabled")
    b8.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1
    b9 = tk.Button(buttonframe, text="Quit", command=b9_close_root)
    b9.grid(row=irow, column=0, sticky=tk.N + tk.S + tk.E + tk.W, ipadx=10)
    irow += 1

    main_gui.mainloop()


make_gui()
