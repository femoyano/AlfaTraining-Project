from matplotlib import pyplot as plt
# Make plot of time series

def plot_time(time, var, x_lab, y_lab):
    # axes.scatter(x, y, marker="o", color="blue")
    plt.subplot()
    plt.plot(time, var, linestyle='-')
    plt.show()


def plot_map():
    pass
