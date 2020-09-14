from pusher_selection.depot import Depot
from pusher_selection.pusher import Pusher
from tkinter import *
from tkinter import ttk
from pandastable import Table
import pusher_selection.data as data


class Interface:
    def __init__(self):
        self.depot = Depot()
        self.broken_pusher = Pusher()

    # симулируем толкач с адекватными характеристиками
    def simulate_pusher(self):
        self.broken_pusher.type = 'aaa'
        self.broken_pusher.power = 2.
        self.broken_pusher.t_until_service = 70.
        self.broken_pusher.remoteness = 1.

    def print_depot(self):
        for index, pusher in enumerate(self.depot.pushers):
            print(index, ' : ', pusher.type)

    def replace_pusher(self):
        try:
            new_pusher = self.depot.replace_pusher(self.broken_pusher)
            return new_pusher
        except:
            return "В депо нет замены для данного токача"

    def main(self, window):

        root = window
        root.title("Замена толкача")

        # Выравниваем окно по центру экрана
        w = 600
        h = 100
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (w / 2) + 30
        y = (hs / 2) - (h / 2) + 30
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.simulate_pusher()

        type_lbl = ttk.Label(root, text='Тип толкача:')
        type_lbl.grid(column=0, row=0)
        type_txt = Entry(root, width=7, text=IntVar(value=self.broken_pusher.type))
        type_txt.grid(column=1, row=0)

        power_lbl = ttk.Label(root, text='Мощность толкача:')
        power_lbl.grid(column=2, row=0)
        power_txt = Entry(root, width=7,
                          text=IntVar(value=self.broken_pusher.power))
        power_txt.grid(column=3, row=0)

        t_until_service_lbl = ttk.Label(root, text='Время до ТО:')
        t_until_service_lbl.grid(column=4, row=0)
        t_until_service_txt = Entry(root, width=7,
                                    text=IntVar(value=self.broken_pusher.t_until_service))
        t_until_service_txt.grid(column=5, row=0)

        remoteness_lbl = ttk.Label(root, text='Удаленность от точки толкания:')
        remoteness_lbl.grid(column=0, row=1)
        remoteness_txt = Entry(root, width=7, text=IntVar(value=self.broken_pusher.remoteness))
        remoteness_txt.grid(column=1, row=1)

        employment_lbl = ttk.Label(root, text='Занятость толкача:')
        employment_lbl.grid(column=2, row=1)
        employment_txt = Entry(root, width=7,
                               text=IntVar(value=self.broken_pusher.employment))
        employment_txt.grid(column=3, row=1)

        def btn_click():
            self.broken_pusher.type = str(type_txt.get())
            self.broken_pusher.power = float(power_txt.get())
            self.broken_pusher.remoteness = float(remoteness_txt.get())
            self.broken_pusher.t_until_service = float(t_until_service_txt.get())
            self.broken_pusher.employment = bool(employment_txt.get())

            # заполняем депо
            self.depot.fill_depot()

            dataframe = data.get_data(self.replace_pusher())

            new_window = Toplevel(root)
            frame = Frame(new_window)
            frame.pack(fill='both', expand=True)

            pt = Table(frame, dataframe=dataframe)
            pt.show()

        btn = Button(root, text="Заменить толкач", command=btn_click)
        btn.grid(column=2, row=3)

        root.mainloop()
