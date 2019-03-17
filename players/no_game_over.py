__author__ = 'RodXander'

import sys
from judge import Judge
from copy import deepcopy

moves = ['s', 'w', 'e', 'n']
board = eval(sys.argv[1])
time_limit = float(sys.argv[2])

move = None
score = -1
j = Judge(len(board))

for m in moves:
    j.board = deepcopy(board)
    j.play(m)
    if not j.is_game_over():
        print(m)
        exit(0)

