__author__ = 'RodXander'

from random import randint
from judge import *


def test_sum_equals():
    print(('*' * 50) + '  testing sum_equals  ' + ('*' * 50))
    judge = Judge(4)
    for i in range(250):
        l1 = []
        for j in range(randint(3, 6)):
            l1.append(randint(3, 6))
        l2 = judge.sum_equals(l1, True)
        print(str(l1) + "\t" + str(l2))
        if sum(l1) != sum(l2):
            raise Exception()


def test_play():
    print(('*' * 50) + '  testing play  ' + ('*' * 50))
    j = Judge(4)
    moves = ['n', 'e', 's', 'w']
    print(j)
    for i in range(100):
        m = moves[randint(0, 3)]
        print('after play: ' + m)
        j.play(m)
        print(j)


def test_sum_increment_between_moves():
    print(('*' * 50) + '  testing sum increment between moves  ' + ('*' * 50))
    j = Judge(4)
    moves = ['n', 'e', 's', 'w']
    for i in range(1000):
        s1 = sum(sum(l) for l in j.board)
        j.play(moves[randint(0, 3)])
        s2 = sum(sum(l) for l in j.board)
        if (s2 - s1) != 2:
            raise Exception()
    print(j)


def test_game_over():
    j = Judge(4)
    moves = ['n', 'e', 's', 'w']
    for i in range(100):
        m = moves[randint(0, 3)]
        try:
            j.play(m)
        except GameOver as exc:
            print(exc)
            print(j)
            return
    print(j)


def test_score():
    j = Judge(4)
    j.board = [[2, 4, 16, 2], [4, 128, 8, 4], [4, 16, 32, 2], [2, 0, 8, 2]]
    j.play('e')
    print(j.score)


def test_collapse():
    j = Judge(4)
    print('playing n')
    j.board = [[0, 2, 4, 0], [2, 0, 4, 6], [2, 2, 0, 6], [2, 2, 4, 6]]
    print(j)
    j.play('n')
    print(j)

    print('playing s')
    j.board = [[2, 2, 4, 6], [2, 2, 0, 6], [2, 0, 4, 6], [0, 2, 4, 0]]
    print(j)
    j.play('s')
    print(j)

    print('playing e')
    j.board = [[2, 2, 2, 0], [2, 2, 0, 2], [4, 0, 4, 4], [6, 6, 6, 0]]
    print(j)
    j.play('e')
    print(j)

    print('playing w')
    j.board = [[6, 6, 6, 0], [4, 0, 4, 4], [2, 2, 0, 2], [2, 2, 2, 0]]
    print(j)
    j.play('w')
    print(j)


def bug():
    j = Judge(4)
    j.board = [[8, 32, 4, 2],[16, 128, 8, 4],[2, 64, 16, 8],[16, 8, 2, 2]]
    print('playing s')
    print(j)
    j.play('s')
    print(j)

def bug2():
    j = Judge(4)
    j.board = [[4, 0, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    print('playing e')
    print(j)
    j.play('e')
    print(j)





# test_sum_equals()
# test_play()
# test_sum_increment_between_moves()
# test_game_over()
# test_score()
test_collapse()
# bug()
# bug2()