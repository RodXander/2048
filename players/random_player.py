__author__ = 'RodXander'

import sys
import random

moves = ['n', 'e', 's', 'w']
board = eval(sys.argv[1])
time_limit = float(sys.argv[2])

print(moves[random.randint(0, 3)])