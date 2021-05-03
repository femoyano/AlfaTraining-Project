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
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler  # default Matplotlib key bindings.
from matplotlib.figure import Figure


# Input stuff
var1 = 'tas'
var1_name = 'near_surface_air_temperature'


def b1_open_file():
    f_name = tk.filedialog.askopenfilename(filetypes=[
        ("json", "*.json"), ("csv", "*.csv"), ("txt", "*.txt"), ("All Files", "*.*")
    ])  # filetypes enthält Filter für Dateitypen


def b5_plot_time(x, y):
    b2.invoke()
    b2.flash()
#    b2.config(bg = "green",state = "disabled")
#    b2["state"]="disabled"
#    print(b2.keys())
    axes.scatter(x, y, marker="o", color="blue")
    canvas.draw()


def clear():
    axes.cla()  # clear axes
    canvas.draw()


root = tk.Tk()
root.wm_title('Future Climate Projections')
mainframe = tk.Frame(root)
buttonframe = tk.Frame(root)

fig = Figure(figsize=(5, 4), dpi=100)
axes = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)

# Set pack_toolbar = false to use .grid geometry manager
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()
toolbar.grid()  # (row=0, column=0, sticky=tk.W)
canvas.mpl_connect("key_press_event", key_press_handler)

b1 = tk.Button(buttonframe, text="Load File", command=b1_open_file)
b2 = tk.Button(buttonframe, text="Clear", command=clear, activeforeground="red", state="disabled")
b2.grid()  # (row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
b7 = tk.Button(buttonframe, text="Quit", command=root.quit)
b7.grid()  # (row=0, column=1, sticky=tk.E+tk.N+tk.S, ipadx=10)


root.mainloop()
