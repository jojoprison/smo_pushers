import pandas as pd
from pusher_selection.pusher import Pusher


def get_data(pusher):
    # создаем датафрейм для результата
    if type(pusher) is Pusher:
        df = pd.DataFrame(columns=['Тип', 'Мощность', 'Время до ТО', 'Удаленность', 'Занятость'])
        row = pd.Series([pusher.type, pusher.power, pusher.t_until_service, pusher.remoteness,
                         pusher.employment], index=df.columns)

        df = df.append(row, ignore_index=True)
    else:
        df = pd.DataFrame(columns=['Оповещение'])
        row = pd.Series([pusher], index=df.columns)

        df = df.append(row, ignore_index=True)

    df.to_excel('./pusher_selection/pusher_selection.xlsx')
    print("pusher's selection data received")
    return df
