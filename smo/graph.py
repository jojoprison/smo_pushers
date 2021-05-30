import tkinter as tk

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

matplotlib.use("TkAgg")


def build_downtime_graph(downtime_average_list):

    plt.plot(downtime_average_list)
    plt.grid(True)

    return plt


def print_graph(parent_window, downtime_average_list, time_list):

    figure = Figure(figsize=(7, 5), dpi=100)
    subplot = figure.add_subplot(111)

    # build_downtime_graph(downtime_average_list)

    subplot.plot(time_list, downtime_average_list, label='Время простоя', lw=1)
    # print(downtime_average_list)
    # plt.plot(x, y1, 'o-r', label="first", lw=5, mec='b', mew=2, ms=10)
    # plt.plot(x, y2, 'v-.g', label="second", mec='r', lw=2, mew=2, ms=12)
    subplot.legend()
    subplot.grid(True)

    new_window = tk.Toplevel(parent_window)
    canvas = FigureCanvasTkAgg(figure, new_window)

    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    toolbar = NavigationToolbar2Tk(canvas, new_window)
    toolbar.update()

    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

