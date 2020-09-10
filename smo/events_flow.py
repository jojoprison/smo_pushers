import numpy as np


# функция генерации случайных чисел в пределе [0, 1]
def generate_r():
    return -np.log(np.random.uniform(low=0.0, high=1.0)) * 1


# на вход интенсивность событий (в час)
def flow_init(intensity, flow_time):
    # Пуассоновский поток случайных событий
    # интенсивность потока (изделия/24 часа), λ
    intensity = intensity / 24
    # время потока (наблюдения) (в часах) , Tн
    # flow_time = 200
    # затраченное время
    time_ = 0
    # число событий за время наблюдения, N
    count = 0

    # в какое время пришли поезда
    events = []

    while time_ <= flow_time:
        # равномерно распределенное от 0 до 1 случайное число, r
        r = generate_r()
        # время появления собития, m = 1/λ
        m = 1 / intensity
        # интервал между случайными собитями , τ
        time_interval = m * r
        time_ = time_ + time_interval
        count += 1

        events.append(time_)

    return events
