import smo.interface as smo
import pusher_selection.interface as pusher_selection
from tkinter import *

# Место запуска программы. Обращаемся к интерфейсу обеих задач
# execfile('main.py')

root = Tk()
root.title("Толкачи")

# Выравниваем окно по центру экрана
w = 400
h = 200
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

smo_interface = smo.Interface()
ps_interface = pusher_selection.Interface()


def smo_btn_click():
    new_window = Toplevel(root)

    smo_interface.main(new_window)


def ps_btn_click():
    new_window = Toplevel(root)

    ps_interface.main(new_window)


mode_lbl = Label(root, text='Режим работы программы:')
mode_lbl.configure(font=1)
mode_lbl.pack()

smo_btn = Button(root, text="СМО", command=smo_btn_click)
smo_btn.configure(font=1)
smo_btn.pack()

ps_btn = Button(root, text="Замена толкача", command=ps_btn_click)
ps_btn.configure(font=1)
ps_btn.pack()

root.mainloop()
