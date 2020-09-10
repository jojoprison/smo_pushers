from tkinter import *
from tkinter.ttk import *
from tkinter import ttk

root = Tk()
root.title("test")
root.geometry('350x200')

ttk.Style().configure('green/black.TLabel', foreground='green',
                      bakcground='black')
ttk.Style().configure('red/black.TButton', foreground='red',
                      background='black')

menu = Menu(root)
item = Menu(menu, tearoff=0)
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)

label = ttk.Label(root, text='lablE', style='green/black.TLabel')
label.grid()

txt = Entry(root, width=10)
txt.grid(column=1, row=0)


def clicked():
    res = 'You wrote ' + txt.get()
    label.configure(text=res)


btn = Button(root, text="Click me", command=clicked,
             style='red/black.TButton')
btn.grid(column=2, row=0)

root.mainloop()
