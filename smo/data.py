import pandas as pd


def get_data(result_list, num_of_pushers):
    # создаем датафрейм для результата
    df = pd.DataFrame(columns=['Количество толкачей', 'Суммарные затраты', 'Общее время работы'])

    for i in range(num_of_pushers):
        row = pd.Series([int(i + 1), result_list[i]['cost'], result_list[i]['clock']], index=df.columns)

        df = df.append(row, ignore_index=True)

    df.to_excel('SMO_result.xlsx')
    print("data got")
    return df
