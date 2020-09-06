import numpy as np
import pandas as pd
from array import *


# функция генерации случайных чисел в пределе [0, 1]
def generate_r():
    return -np.log(np.random.uniform(low=0.0, high=1.0)) * 1


# на вход интенсивность событий (в час)
def flow_init(intensity):
    # Пуассоновский поток случайных событий
    # интенсивность потока (изделия/24 часа), λ
    intensity = intensity / 24
    # время потока (наблюдения) (в часах) , Tн
    flow_time = 30
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

    print(count)
    print(events)

    return events


class Simulation:
    def __init__(self):
        # затраты при простое одного вагона (руб/час)
        self.carriage_downtime_price = 60
        # затраты при простое толкача (руб/час)
        self.pusher_downtime_price = 120
        # затраты при толкании (руб/час)
        self.pushing_price = 30
        # общая сумма затрат
        self.full_price = 0
        # число вагонов в составе одного поезда (одинаковое для всех поездов)
        self.num_of_carriages = 6
        # время толкания (засунуть в функцию и будет увеличиваться)
        # 2 часа - туда, 1 час - обратно
        self.t_pushing = 2
        # время прицепа-отцепа толкача
        self.t_hitch_detach = 0.25
        # время движения толкача от начала участка толкания до депо (для прохождения ТО)
        # туда и обратно, едет от старта
        self.t_to_depot = 2
        # время возврата толкача к началу участка толкания (после толкания на старт)
        self.t_return = 1
        # процент износа толкача
        self.deterioration_percentage = 1.03
        # ТО
        self.to = 3

        self.full_time = 0
        self.pushers = None

    def run(self, events):
        # наработка толкача между техническим обслуживанием (час, только время толкания)
        t_in_action = 0
        # износ
        deterioration = 1
        # число толкачей
        num_of_pushers = 2

        # TODO сделать норм массив
        self.pushers = np.zeros([1, num_of_pushers, 2])
        print(self.pushers)

        # dict_ = dict.fromkeys(['busy', 't_in_action', 'deterioration'], 0)

        cur_t_event = events[0]
        two_t_event = events[1]

        time_ = 0
        after_push_time = 0

        print(self.pushers)

        ret = self.push(self.pushers[0])
        print(self.pushers)


    def push(self, pusher):
        pusher[0] = True

        in_action = (self.t_hitch_detach + self.t_pushing + self.t_return) \
                    * pusher[2]

        pusher[1] += in_action
        pusher[2] *= self.deterioration_percentage
        pusher[0] = False

        print(pusher)

        self.full_time += pusher[1]
        print(self.full_time)

        return pusher

s = Simulation()
ev = flow_init(8)
s.run(ev)


