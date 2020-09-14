import random


class Pusher:
    def __init__(self):
        self.power = 0.
        self.type = ''
        self.employment = False
        self.remoteness = 0.
        self.t_until_service = 0.

    def change_specifications(self, power_, type_, employment_, remoteness_,
                              t_until_service_):
        self.power = power_
        self.type = type_
        self.employment = employment_
        self.remoteness = remoteness_
        self.t_until_service = t_until_service_

    def randomize_specifications(self):
        self.power = random.uniform(0, 10)
        self.employment = random.choice([True, False])
        self.remoteness = random.uniform(0, 100)
        self.t_until_service = random.uniform(0, 70)

        # chars = string.ascii_letters
        chars = 'ab'
        size = 3
        self.type = ''.join(random.choice(chars) for _ in range(size))

        return self

    def __str__(self):
        return "Толкач:\nМощность = %s, Тип = %s, Занятость = %s, " \
               "Удаленность от участка толкания = %s, Время до ТО = %s" \
               % (self.power, self.type, self.employment, self.remoteness,
                  self.t_until_service)


class PusherType:
    def __init__(self):
        self.name = ''

    def set_type(self, type_name):
        self.name = type_name
