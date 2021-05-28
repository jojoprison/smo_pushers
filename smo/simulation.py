from operator import itemgetter


class Simulation:
    """
    Имитационная модель СМО

    Attributes:
        carriage_downtime_price (int):
            Затраты при простое одного вагона (руб/час)
        pusher_downtime_price (int):
            Затраты при простое толкача (руб/час)
        pushing_price (int):
            Затраты при толкании (руб/час)
        cost (float):
            Общая сумма затрат
        num_of_carriages (int):
            Число вагонов в составе одного поезда (одинаковое для всех поездов)
        t_pushing (int):
            Время толкания поезда
        t_hitch_detach (int):
            Время прицепа-отцепа толкача
        t_to_depot (int):
            Время движения толкача от начала участка толкания до депо
            (для прохождения ТО) туда и обратно, едет со старта
        t_return (int):
            Время возврата толкача к началу участка толкания
            (после толкания на старт)
        deterioration_percentage (float):
            Процент износа толкача после совершения действия
        service_time (int):
            Время Технического обслуживания (ТО) толкача
        pushers (list of dict):
            Толкачи
        trains_in_queue (set):
            Поезда в очереди на толкание
        clock (float):
            Имитация часов
        time_step (float):
            Шаг времени изменения симуляции
    """

    def __init__(self):
        """Инициализирует объект симуляции с параметрами по умолчанию"""

        self.carriage_downtime_price = 60
        self.pusher_downtime_price = 120
        self.pushing_price = 30
        self.cost = 0.

        self.num_of_carriages = 6

        self.t_pushing = 2
        self.t_hitch_detach = 0.25
        self.t_to_depot = 2
        self.t_return = 1
        self.deterioration_percentage = 1.05
        self.service_time = 3
        self.downtime_average = 0.

        self.num_of_pushers = None
        self.pushers = None
        self.trains_in_queue = set()

        self.clock = 0.0
        self.time_step = 0.25

    def simulate(self, events, num_of_pushers):
        """
        Симулирует процесс подхода поездов и их толкания

        Args:
            events (list of float):
                Список, содержащий время прихода поездов
            num_of_pushers (int):
                Количество использующихся толкачей
        """

        self.num_of_pushers = num_of_pushers

        # создаем список толкачей в виде словарей с параметрами:
        # busy: занят ли толкач
        # action_time: время активной деятельности толкача (часы)
        # finish_time: время окончания толкания (часы)
        # downtime: время простоя (часы)
        # deterioration: износ толкача (дробное число в виде 1.05, 1.1 - процентное отношение)
        self.pushers = [{'busy': False, 'action_time': 0., 'finish_time': 0., 'downtime': 0.,
                         'deterioration': 1.} for _ in range(self.num_of_pushers)]

        # для каждого отдельного прибытия поезда
        for event_time in events:
            # пока текущее время симуляции меньше времени прибытия поезда
            while self.clock < event_time:
                # симулируем протекание времени
                self.live()

            # пытаемся толкнуть текущий поезд
            self.push(event_time)

        # время окончания всех действий толкачей
        pushers_finish_time = []
        for pusher in self.pushers:
            # засовываем время в список
            pushers_finish_time.append(pusher['finish_time'])

        # пока текущее время меньше максимального времени окончания среди толкачей
        while self.clock < (max(enumerate(pushers_finish_time), key=itemgetter(1))[1]):
            # симулируем протекание времени
            self.live()

    def live(self):
        """Симулирует процесс протекания времени в симуляции"""

        # симулируем протекание времени
        self.clock += self.time_step

        downtime_list = []

        # ищем свободный толкач
        for pusher in self.pushers:
            # если толкач занят
            if pusher['busy']:
                # к общим затратам прибавляем стоимость толкания
                # за единицу времени
                self.cost += self.pushing_price * self.time_step
                # сбрасываем время простоя толкача
                pusher['downtime'] = 0.
            else:
                # к общим затратам прибавляем стоимость простоя толкача
                # за единицу времени
                self.cost += self.pusher_downtime_price * self.time_step

                # записываем, сколько простаивает толкач
                pusher['downtime'] += self.time_step
                # добавляем время простоя каждого толкача в общий список для подсчета среднего времени простоя
                downtime_list.append(pusher['downtime'])

            # если текущее время больше времени окончания работы толкача
            if self.clock >= pusher['finish_time']:
                # освобождаем толкач
                pusher['busy'] = False

        # сумма времен простоя всех толкачей
        downtime_sum = sum(downtime for downtime in downtime_list)
        # вычисляем среднее время простоя толкачей
        self.downtime_average = downtime_sum / self.num_of_pushers
        print('downtime_average: ', self.downtime_average)

        # к общим затратам прибавляем стоимость простоя поезда с заданным
        # кол-вом вагонов, умноженную на кол-во поездов в ожидании толкания
        # за единицу времени
        self.cost += len(self.trains_in_queue) * self.carriage_downtime_price \
                     * self.num_of_carriages * self.time_step

    def service(self, pusher_index):
        """
        Техническое обслуживание (ТО) толкача

        Args:
            pusher_index (int):
                Индекс толкача, требующего техническое обслуживание
        """

        # выбираем толкач из списка по индексу
        pusher = self.pushers[pusher_index]
        # толкач занят
        pusher['busy'] = True
        # сбрасываем время работы
        pusher['action_time'] = 0
        # указываем время окончания, учитывая износ толкача, время возврата
        # на станцию толкания и время ТО
        pusher['finish_time'] = self.clock + (self.t_to_depot * pusher['deterioration']) \
                                + self.service_time
        # сбрасываем износ толкача
        pusher['deterioration'] = 1.

    def push(self, event_time):
        """
        Симулирует толкание поезда

        Args:
            event_time (float):
                Времени прибытия поезда
        """

        # TODO будем выбирать наименее изношенный толкач
        deters = []

        # бесконечный цикл, будем выходить из него с помощью return
        while True:
            # берем индекс толкача в списке и сам объект толкача
            for index, pusher in enumerate(self.pushers):
                # поочередно ищем свободный толкач
                if not pusher['busy']:
                    # износ запихиваем в переменную
                    pusher_deterioration = pusher['deterioration']

                    # TODO засунуть метод монтекарло сюда, чтобы сделать время толкания случайным в заданном диапазоне
                    # считаем время предстоящей работы
                    # TODO здесь будем плюсовать весь общий путь с учетом износа - это будет нижняя граница интервала
                    action_time = (self.t_hitch_detach + self.t_pushing + self.t_return) \
                                  * pusher_deterioration
                    # время пути до депо
                    time_to_depot = self.t_to_depot * pusher_deterioration

                    # если время работы превысит 72 часа, отправляем на ТО
                    if pusher['action_time'] + action_time + time_to_depot >= 72:
                        self.service(index)
                        # итерация в цикле на следующий толкач
                        continue

                    # толкач становится занятым
                    pusher['busy'] = True
                    # увеличиваем время работы
                    pusher['action_time'] += action_time
                    # увеличиваем износ
                    pusher['deterioration'] *= self.deterioration_percentage
                    # обновляем время окончания работ
                    pusher['finish_time'] = self.clock + action_time

                    # удаляем поезд и очереди на толкание
                    self.trains_in_queue.discard(event_time)

                    # выходим из метода
                    return

                # TODO deters.append(pusher['deterioration'])

            # if deters:
            #     # min_deter = min(deters)
            #     min_deter = min(enumerate(deters), key=itemgetter(1))
            #     print(min_deter)
            #     print(type(min_deter))

            # добавляем поезд в очередь на толкание
            self.trains_in_queue.add(event_time)

            # симулируем протекание времени
            self.live()
