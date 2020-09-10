import tkinter as tk
from pandastable import Table, TableModel
import pandas as pd

root = tk.Tk()
root.title('PandasTable Example')

frame = tk.Frame(root)
frame.pack(fill='both', expand=True)

# df = pd.DataFrame(columns=['Количество толкачей', 'Суммарные затраты', 'Общее время работы'])
df = pd.DataFrame({
    'A': [1,2,3,4,5,6,],
    'B': [1,1,2,2,3,3,],
    'C': [1,2,3,1,2,3,],
    'D': [1,1,1,2,2,2,],
})

pt = Table(frame, dataframe=df)
pt.show()

root.mainloop()
