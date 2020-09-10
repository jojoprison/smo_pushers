from smo.simulation import Simulation
import smo.interface
import smo.events_flow as flow
import pandas as pd


# интенсивность потока в час
intens = 24
# генерим ивенты
evs = flow.flow_init(intens, 200)

# создаем датафрейм для результата
df = pd.DataFrame(columns=['Индекс', 'Количество толкачей', 'Суммарные затраты', 'Общее время работы'])

for i in range(1, 10):
    s = Simulation()
    s.__init__()
    s.run(evs, i)

    row = pd.Series([i, i, s.cost, s.clock], index=df.columns)

    df = df.append(row, ignore_index=True)

df.to_excel('pushers_result.xlsx')
print("Done")