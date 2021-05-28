from pusher_selection.pusher import Pusher
import random


class Depot:
    # TODO написать комменты
    def __init__(self):
        self.hue = 1
        self.pushers = []

    def fill_depot(self):
        num_of_pushers = random.randint(0, 20)
        for i in range(num_of_pushers):
            self.pushers.append(Pusher().randomize_specifications())

    def replace_pusher(self, broken_pusher):
        suitable_pushers = [{'index': None, 'remoteness': 0., 't_until_service': 0.} for _ in range(len(self.pushers))]

        for pusher_idx, pusher in enumerate(self.pushers):
            if not pusher.employment and broken_pusher.type == pusher.type and broken_pusher.power <= pusher.power:
                suitable_pushers[pusher_idx]['index'] = pusher_idx
                suitable_pushers[pusher_idx]['remoteness'] = pusher.remoteness
                suitable_pushers[pusher_idx]['t_until_service'] = pusher.t_until_service

        res = [i for i in suitable_pushers if not (i['index'] is None)]

        pshrs_remoteness = []
        for pshr in res:
            if pshr['t_until_service'] >= 69:
                continue

            pshrs_remoteness.append(pshr['remoteness'])

        if not pshrs_remoteness:
            for pshr in res:
                pshrs_remoteness.append(pshr['remoteness'])

        min_ = min(pshrs_remoteness)

        replaceable_pusher_idx = None

        for pshr in res:
            if pshr['remoteness'] == min_:
                replaceable_pusher_idx = pshr['index']
                break

        h = self.pushers[replaceable_pusher_idx]
        self.pushers[replaceable_pusher_idx] = broken_pusher

        return h
