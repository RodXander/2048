__author__ = 'RodXander'

import sys
import random
from threading import Thread

moves = ['n', 'e', 's', 'w']
board = eval(sys.argv[1])
time_limit = float(sys.argv[2])


def dummy():
    while True:
        pass


t = Thread(target=dummy)
t.daemon = True
t.start()
t.join(time_limit)

print(moves[random.randint(0, 3)])