# A class to chose and

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
