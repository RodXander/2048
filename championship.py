__author__ = 'RodXander'

import os
import time
from os.path import join

from game import Game


time_limit = 1
players = []
ignore = ['random_dummy.py', 'no_game_over.py']

for root, dirs, files in os.walk('players'):
    files = set(files) - set(ignore)
    players.extend([name for name in files if name.endswith('.py')])

print('Players found: ' + str(players))

score = dict()

for player1 in players:
    for player2 in players:
        if player1 == player2:
            continue
        print(str.format('{0} vs {1} started at {2}', player1, player2, time.asctime()))
        game = Game(join('players', player1), join('players', player2), time_limit)
        winner = game.play()
        print(str(winner) + ' wins\n')
        score[winner] = score[winner] + 1 if winner in score else 1

print(score)
