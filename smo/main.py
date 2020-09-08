import numpy as np
from operator import itemgetter
import pandas as pd


# функция генерации случайных чисел в пределе [0, 1]
def generate_r():
    return -np.log(np.random.uniform(low=0.0, high=1.0)) * 1


# на вход интенсивность событий (в час)
def flow_init(intensity):
    # Пуассоновский поток случайных событий
    # интенсивность потока (изделия/24 часа), λ
    intensity = intensity / 24
    # время потока (наблюдения) (в часах) , Tн
    flow_time = 200
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


class Simulation:
    def __init__(self):
        # затраты при простое одного вагона (руб/час)
        self.carriage_downtime_price = 60
        # затраты при простое толкача (руб/час)
        self.pusher_downtime_price = 120
        # затраты при толкании (руб/час)
        self.pushing_price = 30
        # общая сумма затрат
        self.cost = 0

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
        self.deterioration_percentage = 1.05
        # ТО
        self.service_time = 3

        self.pushers = None

        self.clock = 0.0

        self.trains_in_queue = set()

    def run(self, events, num_of_pushers):
        # наработка толкача между техническим обслуживанием (час, только время толкания)
        # t_in_action = 0
        # износ
        # deterioration = 1
        # число толкачей
        # num_of_pushers = 2

        self.pushers = [{'busy': False, 'action_time': 0., 'deterioration': 1., 'finish_time': 0.}
                        for _ in range(num_of_pushers)]
        # print("Init: ", self.pushers)

        for event_time in events:
            while self.clock < event_time:
                self.live()

            self.push(event_time)

        pushers_finish_time = []
        for pusher in self.pushers:
            pushers_finish_time.append(pusher['finish_time'])

        while self.clock < (max(enumerate(pushers_finish_time), key=itemgetter(1))[1]):
            self.live()

        # print("result: ", self.pushers)
        # print("clock: ", self.clock)
        # print("cost: ", self.cost)

    def live(self):

        hours = 1 / 4

        # симулируем 15 минут времени
        self.clock += hours

        # сообщаем, что толкачи свободны (БЕГИТЕ РАБЫ, ВАС ОСВОБОДИЛИ!!!)
        for pusher in self.pushers:
            if pusher['busy']:
                self.cost += self.pushing_price * hours
            else:
                self.cost += self.pusher_downtime_price * hours

            if self.clock >= pusher['finish_time']:
                pusher['busy'] = False

        self.cost += len(self.trains_in_queue) * self.carriage_downtime_price * self.num_of_carriages

    def service(self, pusher_index):
        pusher = self.pushers[pusher_index]
        pusher['busy'] = True
        pusher['action_time'] = 0
        pusher['finish_time'] = self.clock + (self.t_to_depot * pusher['deterioration']) \
                                + self.service_time
        pusher['deterioration'] = 1.

    def push(self, event_time):

        # будем выбирать наименее изношенный толкач
        deters = []

        while True:
            for index, pusher in enumerate(self.pushers):
                if not pusher['busy']:

                    # износ
                    pusher_deterioration = pusher['deterioration']

                    # считаем время будущей работы
                    action_time = (self.t_hitch_detach + self.t_pushing + self.t_return) \
                                  * pusher_deterioration
                    # время пути до депо
                    time_to_depot = self.t_to_depot * pusher_deterioration

                    # если время работы превысит 72 часа, отправляем на ТО
                    if pusher['action_time'] + action_time + time_to_depot >= 72:
                        self.service(index)
                        continue

                    pusher['busy'] = True
                    pusher['action_time'] += action_time
                    pusher['deterioration'] *= self.deterioration_percentage
                    pusher['finish_time'] = self.clock + action_time

                    self.trains_in_queue.discard(event_time)

                    return

                # deters.append(pusher['deterioration'])

            # if deters:
            #     # min_deter = min(deters)
            #     min_deter = min(enumerate(deters), key=itemgetter(1))
            #     print(min_deter)
            #     print(type(min_deter))

            self.trains_in_queue.add(event_time)

            self.live()




# интенсивность потока в час
intens = 8
# генерим ивенты
evs = flow_init(intens)

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
