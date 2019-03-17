__author__ = 'RodXander'

import sys
from judge import Judge
from exceptions import *
from copy import deepcopy

moves = ['n', 'e', 's', 'w']
board = eval(sys.argv[1])
time_limit = float(sys.argv[2])

move = None
score = -1
j = Judge(len(board))

for m in moves:
    j.board = deepcopy(board)
    j.play(m)
    if j.score > score:
        score = j.score
        move = m

print(move)

