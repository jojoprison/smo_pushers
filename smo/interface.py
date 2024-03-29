from tkinter import *
from tkinter import ttk

import matplotlib
from pandastable import Table

import smo.data as data
import smo.events_flow as flow
from smo.graph import print_graph
from smo.simulation import Simulation
from smo.exceptions import SimulationInputValueError

import sys

matplotlib.use("TkAgg")


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
        w = 1000
        h = 200
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        flow_time_lbl = ttk.Label(root, text='Время наблюдения (в часах):')
        flow_time_lbl.configure(font=0.0001)
        flow_time_lbl.grid()

        flow_time_txt = Entry(root, width=7, text=IntVar(value=self.flow_time))
        flow_time_txt.configure(font=1)
        flow_time_txt.grid(column=1, row=0)

        intensity_lbl = ttk.Label(root, text='Интенсивность потока (ед./24 часа):')
        intensity_lbl.configure(font=1)
        intensity_lbl.grid(column=2, row=0)

        intensity_txt = Entry(root, width=7, text=IntVar(value=self.intensity))
        intensity_txt.configure(font=1)
        intensity_txt.grid(column=3, row=0)

        pushers_lbl = ttk.Label(root, text='Макс. кол-во толкачей:')
        pushers_lbl.configure(font=1)
        pushers_lbl.grid(column=4, row=0)

        pushers_txt = Entry(root, width=7, text=IntVar(value=self.pushers_max))
        pushers_txt.configure(font=1)
        pushers_txt.grid(column=5, row=0)

        carriages_lbl = ttk.Label(root, text='Число вагонов:')
        carriages_lbl.configure(font=1)
        carriages_lbl.grid(column=0, row=1)

        carriages_txt = Entry(root, width=7,
                              text=IntVar(value=self.simulation.num_of_carriages))
        carriages_txt.configure(font=1)
        carriages_txt.grid(column=1, row=1)

        carriage_price_lbl = ttk.Label(root, text='Стоимость простоя вагона (руб/час):')
        carriage_price_lbl.configure(font=1)
        carriage_price_lbl.grid(column=2, row=1)

        carriage_price_txt = Entry(root, width=7,
                                   text=IntVar(value=self.simulation.carriage_downtime_price))
        carriage_price_txt.configure(font=1)
        carriage_price_txt.grid(column=3, row=1)

        pusher_price_lbl = ttk.Label(root, text='Стоимость простоя толкача (руб/час):')
        pusher_price_lbl.configure(font=1)
        pusher_price_lbl.grid(column=4, row=1)

        pusher_price_txt = Entry(root, width=7,
                                 text=IntVar(value=self.simulation.pusher_downtime_price))
        pusher_price_txt.configure(font=1)
        pusher_price_txt.grid(column=5, row=1)

        pushing_price_lbl = ttk.Label(root, text='Стоимость толкания (руб/час):')
        pushing_price_lbl.configure(font=1)
        pushing_price_lbl.grid(column=0, row=2)

        pushing_price_txt = Entry(root, width=7,
                                  text=IntVar(value=self.simulation.pushing_price))
        pushing_price_txt.configure(font=1)
        pushing_price_txt.grid(column=1, row=2)

        # # шаг симуляции
        # time_step_lbl = ttk.Label(root, text='Шаг симуляции (в часах):')
        # time_step_lbl.configure(font=1)
        # time_step_lbl.grid(column=2, row=2)
        #
        # time_step_txt = Entry(root, width=7,
        #                       text=IntVar(value=self.simulation.time_step))
        # time_step_txt.configure(font=1)
        # time_step_txt.grid(column=3, row=2)

        analytic_func_lbl = ttk.Label(root, text='Аналитическая функция времени:')
        analytic_func_lbl.configure(font=1)
        analytic_func_lbl.grid(column=2, row=2)

        # значения для выбора аналитической функции
        analytic_func_var = StringVar(root)
        analytic_func_var.set('Метод Монте-Карло')

        # выбор аналитической функции
        analytic_func_option = OptionMenu(root, analytic_func_var, 'Метод Монте-Карло')
        analytic_func_option.configure(font=1)
        analytic_func_option.grid(column=3, row=2)

        def btn_click():
            sim = Simulation()

            try:
                try:
                    sim.num_of_carriages = int(carriages_txt.get())
                except ValueError:
                    raise SimulationInputValueError(
                        f'Неверно введено количество вагонов, введите число:{carriages_txt.get()}, введите число.')

                try:
                    sim.carriage_downtime_price = int(carriage_price_txt.get())
                except ValueError:
                    raise SimulationInputValueError(
                        f'Неверно введена стоимость простоя вагона: {carriage_price_txt.get()}, введите число.')

                try:
                    sim.pusher_downtime_price = int(pusher_price_txt.get())
                except ValueError:
                    raise SimulationInputValueError(
                        f'Неверно введена стоимость простоя толкача: {pusher_price_txt.get()}, введите число.')

                try:
                    sim.pushing_price = int(pushing_price_txt.get())
                except ValueError:
                    raise SimulationInputValueError(
                        f'Неверно введена стоимость толкания: {pushing_price_txt.get()}, введите число. ')
                # шаги симуляции теперь задаем статическим внутри класса и скроем ее с интерфейса
                # sim.time_step = float(time_step_txt.get())

                # генерируем поток случайных событий
                try:
                    intensity = int(intensity_txt.get())
                except ValueError:
                    raise SimulationInputValueError(
                        f'Неверно введна интенсивнось потока: {intensity_txt.get()}, введите число.')

                try:
                    flow_time = int(flow_time_txt.get())
                except ValueError:
                    raise SimulationInputValueError(
                        f'Неверно введено время наблюдения: {flow_time_txt.get()}, введите число.')

                events = flow.flow_init(intensity, flow_time)

                num_of_pushers = int(pushers_txt.get())
                result_list = [{'cost': 0., 'clock': 0., 'downtime_average': 0.}
                               for _ in range(1, num_of_pushers + 1)]

                for pushers_inx in range(1, num_of_pushers + 1):
                    # обновляем данные времени, общих затрат и массива времени простоя для симулиции
                    sim.reset_sim()
                    # симулируем относительно пуассоновского потока событий и количества толкачей
                    sim.simulate(events, pushers_inx)

                    result = result_list[pushers_inx - 1]
                    result['cost'] = sim.cost
                    result['clock'] = sim.clock
                    result['downtime_average_list'] = sim.downtime_average_list

                dataframe = data.get_data(result_list, num_of_pushers)

                new_window = Toplevel(root)
                frame = Frame(new_window)
                frame.pack()

                pt = Table(frame, dataframe=dataframe)
                pt.show()

                # получаем индекс строки с толкачей минимальными затратами
                best_res_idx = dataframe['Суммарные затраты (руб)'].idxmin()

                # выбираем строку из таблицы с лучшими результатами
                best_res = dataframe.iloc[[best_res_idx]]
                best_downtime_average_list = result_list[best_res_idx]['downtime_average_list']

                # создаем массив временных шагов для отображения интервалов симуляции на графике
                time_list = []
                for time_step_idx in range(int(sim.clock // sim.time_step)):
                    time_list.append(sim.time_step * time_step_idx)

                # подбиваем массивы значений для графика к одному размеру
                if len(best_downtime_average_list) > len(time_list):
                    len_max = len(best_downtime_average_list)
                    list_max = best_downtime_average_list
                    len_min = len(time_list)
                else:
                    len_max = len(time_list)
                    list_max = time_list
                    len_min = len(best_downtime_average_list)

                while len_max != len_min:
                    list_max.pop()
                    len_max = len(list_max)

                # рисуем график функции простоя от времени симуляции
                print_graph(frame, best_downtime_average_list, time_list)

                # TODO можно переделать вид вывозда лучшего результата, чтобы был в столбик
                # headers = list(best_res.columns.values)
                # print(headers)
                # print(best_res.get_values())

                # lol = best_res.to_csv(index=False).strip('\n').split('\n')
                # df_string = '\r\n'.join(lol)
                # print(df_string)

                # lol = best_res.to_csv(index=False, sep='\n')
                # print(type(lol))

                best_res = best_res.to_string(index=False)

                # df_bytes = df_string.encode('utf8')  # <= this is bytes object to write the file
                # print(df_bytes)
                # print(best_res.to_string(index=False))

                res_str = 'ЛУЧШИЙ РЕЗУЛЬТАТ:\n' + best_res

                result_lbl = ttk.Label(frame, text=res_str)
                result_lbl.configure(font=1)
                result_lbl.grid(column=1)
            except SimulationInputValueError as ex:

                new_window = Toplevel(root)
                new_window.wm_geometry('600x100')
                frame = Frame(new_window)
                frame.pack(fill='both', expand=True)

                error_lbl = ttk.Label(frame, text='ОШИБКА\n' + ex.__str__())
                error_lbl.configure(font=1)
                error_lbl.pack(fill='both', expand=True)

        btn = Button(root, text='Симулировать', command=btn_click)
        btn.configure(font=1)
        btn.grid(column=2, row=3)

        root.mainloop()
