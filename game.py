__author__ = 'RodXander'

import subprocess
from os.path import join, basename, splitext
from threading import Thread
import time
from copy import deepcopy

from judge import Judge


class Game:
    def __init__(self, player1, player2, time_limit):
        self.player1 = player1
        self.player2 = player2
        self.time_limit = time_limit
        self.delta = 0.5
        self.score = {player1: 0, player2: 0}
        self.repetitions = 0
        self.repetitions_limit = 10

    def play(self):
        judge = Judge(4)
        log = open(join('games', str.format('{0} vs {1}.txt', splitext(basename(self.player1))[0],
                                            splitext(basename(self.player2))[0])), 'a')
        log.write(('*' * 25) + time.asctime() + ('*' * 25) + '\n')
        player = self.player2
        while True:
            player = ({self.player1, self.player2} - {player}).pop()

            def run_script():
                global move
                move = bytes.decode(subprocess.check_output(['python', player, str(judge.board), str(self.time_limit)]).strip())

            t = Thread(target=run_script)
            t.daemon = True
            t.start()
            t.join(self.time_limit + self.delta)  # un poco de sesgo por los overheads

            if t.is_alive():
                log.write(str.format('{0} timeout\n', player))
                log.close()
                return ({self.player1, self.player2} - {player}).pop()

            log.write(str.format('{0} moves {1}\n', player, move))
            board = deepcopy(judge.board)
            judge.play(move)
            self.repetitions = self.repetitions + 1 if board == judge.board else 0
            self.score[player] += judge.score
            log.write(str.format('+ {0} = {1}\n', str(judge.score), str(self.score[player])))
            log.write(str(judge) + "\n")

            if judge.is_game_finished():
                log.write(str.format('{0}\n', 'Game finished'))
                log.close()
                adversary = ({self.player1, self.player2} - {player}).pop()
                return player if self.score[player] >= self.score[adversary] else adversary
            if judge.is_game_over():
                log.write(str.format('{0}\n', 'Game over'))
                log.close()
                return ({self.player1, self.player2} - {player}).pop()
            if self.repetitions == self.repetitions_limit:
                log.write(str.format('{0}\n', 'Game invalidated'))
                log.close()
                return None
