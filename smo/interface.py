from smo.simulation import Simulation
from tkinter import *
from tkinter import ttk


class Interface:
    def __init__(self):
        self.simulation = Simulation()
        self.flow_time = 200
        self.intensity = 8
        self.pushers_max = 10

    def main(self):

        root = Tk()
        root.title("СМО Толкачи")

        # Выравниваем окно по центру экрана
        w = 600
        h = 100
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        flow_time_lbl = ttk.Label(root, text='Время наблюдения:')
        flow_time_lbl.grid()

        flow_time_txt = Entry(root, width=7, text=IntVar(value=self.flow_time))
        flow_time_txt.grid(column=1, row=0)

        intensity_lbl = ttk.Label(root, text='Интенсивность потока:')
        intensity_lbl.grid(column=2, row=0)

        intensity_txt = Entry(root, width=7, text=IntVar(value=self.intensity))
        intensity_txt.grid(column=3, row=0)

        pushers_lbl = ttk.Label(root, text='Макс. кол-во толкачей:')
        pushers_lbl.grid(column=4, row=0)

        pushers_txt = Entry(root, width=7, text=IntVar(value=self.pushers_max))
        pushers_txt.grid(column=5, row=0)

        carriages_lbl = ttk.Label(root, text='Число вагонов:')
        carriages_lbl.grid(column=0, row=1)

        carriages_txt = Entry(root, width=7,
                              text=IntVar(value=self.simulation.num_of_carriages))
        carriages_txt.grid(column=1, row=1)

        carriage_price_lbl = ttk.Label(root, text='Стоимость простоя вагона:')
        carriage_price_lbl.grid(column=2, row=1)

        carriage_price_txt = Entry(root, width=7,
                                   text=IntVar(value=self.simulation.carriage_downtime_price))
        carriage_price_txt.grid(column=3, row=1)

        pusher_price_lbl = ttk.Label(root, text='Стоимость простоя толкача:')
        pusher_price_lbl.grid(column=4, row=1)

        pusher_price_txt = Entry(root, width=7,
                                 text=IntVar(value=self.simulation.pusher_downtime_price))
        pusher_price_txt.grid(column=5, row=1)

        pushing_price_lbl = ttk.Label(root, text='Стоимость толкания:')
        pushing_price_lbl.grid(column=0, row=2)

        pushing_price_txt = Entry(root, width=7,
                                  text=IntVar(value=self.simulation.pushing_price))
        pushing_price_txt.grid(column=1, row=2)

        time_step_lbl = ttk.Label(root, text='Шаг симуляции:')
        time_step_lbl.grid(column=2, row=2)

        time_step_txt = Entry(root, width=7,
                              text=IntVar(value=self.simulation.time_step))
        time_step_txt.grid(column=3, row=2)

        def btn_click():
            sim = Simulation()
            sim.num_of_carriages = int(carriages_txt.get())
            sim.carriage_downtime_price = int(carriage_price_txt.get())
            sim.pusher_downtime_price = int(pusher_price_txt.get())
            sim.pushing_price = int(pushing_price_txt.get())
            sim.time_step = float(time_step_txt.get())

            print(self.simulation)

        btn = Button(root, text="Симулировать", command=btn_click)
        btn.grid(column=2, row=3)

        root.mainloop()


interface_ = Interface()
interface_.main()