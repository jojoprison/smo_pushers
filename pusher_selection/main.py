from pusher_selection.depot import Depot
from pusher_selection.pusher import Pusher

# execfile('pusher_selection/main.py')

broken_pusher = Pusher()
broken_pusher.t_until_service = 70.
broken_pusher.type = 'aaa'
broken_pusher.remoteness = 1.
broken_pusher.power = 2.

depot = Depot()
depot.fill_depot()
for index, pshr in enumerate(depot.pushers):
    print(index, ' : ', pshr.type)

try:
    new_pusher = depot.replace_pusher(broken_pusher)
    print(new_pusher)
except:
    print("В депо нет замены для данного токача")
