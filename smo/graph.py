import matplotlib.pyplot as plt
import numpy as np

# x = [1, 5, 10, 15, 20]
# y1 = [1, 7, 3, 5, 11]
# y2 = [4, 3, 1, 8, 12]
#
# # plt.figure(figsize=(12, 7))
#
# plt.plot(x)
#
# # plt.plot(x, y1, 'o-r', alpha=0.7, label="first", lw=5, mec='b', mew=2, ms=10)
# # plt.plot(x, y2, 'v-.g', label="second", mec='r', lw=2, mew=2, ms=12)
# # plt.legend()
# plt.grid(True)
#
# plt.show()


def build_downtime_graph(downtime_average_list):

    print(downtime_average_list)

    plt.plot(downtime_average_list)
    plt.grid(True)

    return plt
