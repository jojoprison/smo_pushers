import tkinter as tk
from pandastable import Table, TableModel
import pandas as pd

root = tk.Tk()
root.title('PandasTable Example')

frame = tk.Frame(root)
frame.pack(fill='both', expand=True)

pt = Table(frame)
pt.show()
pt.model.df = TableModel.getSampleData()
# pt.model.df = TableModel.getStackedData()

root.mainloop()
