from smo.simulation import Simulation
from tkinter import *
from tkinter import ttk
import smo.events_flow as flow
from pandastable import Table
import smo.data as data


class Interface:
    def __init__(self):
        self.simulation = Simulation()
        self.flow_time = 200
        self.intensity = 8
        self.pushers_max = 10

    def main(self, window):

        root = window
        root.title("СМО Толкачи")

        # Выравниваем окно по центру экрана
        w = 600
        h = 100
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (w / 2) + 30
        y = (hs / 2) - (h / 2) + 30
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

            # генерируем поток случайных событий
            events = flow.flow_init(int(intensity_txt.get()), int(flow_time_txt.get()))

            num_of_pushers = int(pushers_txt.get())
            result_list = [{'cost': 0., 'clock': 0.} for _ in range(1, num_of_pushers + 1)]

            for pushers_inx in range(1, num_of_pushers + 1):
                sim.cost = 0.
                sim.clock = 0.
                sim.simulate(events, pushers_inx)

                result = result_list[pushers_inx - 1]
                result['cost'] = sim.cost
                result['clock'] = sim.clock

            dataframe = data.get_data(result_list, num_of_pushers)

            new_window = Toplevel(root)
            frame = Frame(new_window)
            frame.pack(fill='both', expand=True)

            pt = Table(frame, dataframe=dataframe)
            pt.show()

            best = dataframe.min()

            res_str = 'ЛУЧШИЙ ТОЛКАЧ:\n' + str(best)

            # TODO обрезать последнюю строку

            # mass_res = stra.splitlines()
            # res_str = ''

            # res_str = res_str.join(mass_res)

            result_lbl = ttk.Label(frame, text=res_str)
            result_lbl.grid(column=1)

        btn = Button(root, text="Симулировать", command=btn_click)
        btn.grid(column=2, row=3)

        root.mainloop()
