# A class to chose and

from tkinter import ttk
import tkinter as tk


class Combo:

    def __init__(self, parent):
        self.varselect = tk.StringVar()
        self.box = ttk.Combobox(parent, textvariable=self.varselect)

    def create(self, varnames):
        self.box.bind('<<ComboboxSelected>>', self.entry_changed)
        self.box['values'] = varnames
        self.box.current(len(varnames)-1)

    def grid(self, row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W, ipadx=10):
        self.box.grid(row=row, column=column, sticky=sticky, ipadx=ipadx)

    def entry_changed(self, event):
        pass
        # self.var = str(self.varselect.get())
        # print(self.var)
        # return self.var


if __name__ == '__main__':
    root = tk.Tk()
    myvar = tk.StringVar()
    c = Combo(root)
    c.create(["one", "two", "three"])
    c.grid()
    root.mainloop()
