import numpy as np
import pandas as pd


def generate_r():
    return -np.log(np.random.uniform(low=0.0, high=1.0)) * 6

class Simulation():
    def __init__(self):
        # затраты при  простое одного вагона (руб/час)
        self.carriage_downtime_price = 60
        # затраты при простое толкача (руб/час)
        self.pusher_downtime_price = 120
        # затраты при толкании (руб/час)
        self.pushing_price = 30
        # число толкачей
        self.num_of_pushers = 3
        # число вагонов в составе одного поезда (одинаковое для всех поездов?)
        self.num_of_carriages = 6
        # наработка толкача между техническим обслуживанием (час, только время толкания)
        self.t_in_action = 1
        # износ
        self.deterioration = 0
        # время толкания (засунуть в функцию и будет увеличиваться)
        # 2 часа - туда, 1 час - обратно
        self.t_pushing = 3
        # время прицепа-отцепа толкача
        self.t_hitch_detach = 0.25
        # время движения толкача от начала участка толкания до депо (для прохождения ТО)
        # туда и обратно, едет от старта
        self.t_pusher_to_depot = 2
        # время возврата толкача к началу участка толкания (после толкания на старт)
        self.t_pusher_return = 1

        # Пуассоновский поток случайных событий
        # время потока (наблюдения) (в часах) , Tн
        self.flow_time = 0
        # интенсивность потока (изделия/24 часа), λ
        self.intensity = 0
        # интервал между случайными собитями , τ
        self.interval = 0
        # число событий за время наблюдения, N
        self.N = 0
        # время появления собития, m = 1/λ
        self.m = 0
        # равномерно распределенное от 0 до 1 случайное число,
        self.r = 0



    # износ толкача
    def pusher_deterioration(self):
        self.t_pushing *= self.deterioration



    def flow_init(self):
        intensity = 8 / 24
        flow_time = 200
        time_ = 0
        count = 0

        while time_ <= flow_time:
            r = generate_r()
            time_interval = 1 / intensity * r
            time_ = time_ + time_interval
            count += 1
            print(time_)

        print(count)


s = Simulation()
s.flow_init()
