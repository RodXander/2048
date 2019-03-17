__author__ = 'RodXander'

from copy import deepcopy
from exceptions import *


class Judge:
    def __init__(self, dimension):
        self.board = []
        for i in range(dimension):
            self.board.append([0] * dimension)
        self.board[0][0] = 2
        self.score = 0

    def __str__(self):
        s = ''
        for i in range(len(self.board)):
            s += str(self.board[i]) + "\n"
        return s

    #permited values: n, e, s, w
    def play(self, move):
        self.score = 0
        self.move(move)
        self.locate_new_box(move)

    def move(self, move):
        if move == 'n' or move == 's':
            for c in range(len(self.board)):
                column = self.get_column(c)
                column = self.remove_zeros(column)
                column = self.sum_equals(column, move == 's', True)
                self.fill_column(c, column, move == 's')
        elif move == 'w' or move == 'e':
            for r in range(len(self.board)):
                row = self.get_row(r)
                row = self.remove_zeros(row)
                row = self.sum_equals(row, move == 'e', True)
                self.fill_row(r, row, move == 'e')
        else:
            raise InvalidParam(move)

    def locate_new_box(self, move):
        if move == 'n':
            for r in range(len(self.board) - 1, -1, -1):
                for c in range(len(self.board) - 1, -1, -1):
                    if self.board[r][c] == 0:
                        self.board[r][c] = 2
                        return True
        elif move == 'e':
            for c in range(len(self.board)):
                for r in range(len(self.board) - 1, -1, -1):
                    if self.board[r][c] == 0:
                        self.board[r][c] = 2
                        return True
        elif move == 's':
            for r in range(len(self.board)):
                for c in range(len(self.board)):
                    if self.board[r][c] == 0:
                        self.board[r][c] = 2
                        return True
        elif move == 'w':
            for c in range(len(self.board) - 1, -1, -1):
                for r in range(len(self.board)):
                    if self.board[r][c] == 0:
                        self.board[r][c] = 2
                        return True
        else:
            raise InvalidParam()
        return False

    def is_game_over(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0:
                    return False
                if i > 0 and self.board[i-1][j] == self.board[i][j]:
                    return False
                if j > 0 and self.board[i][j-1] == self.board[i][j]:
                    return False
        return True

    def is_game_finished(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 2048:
                    return True
        return False

    def get_column(self, c):
        column = []
        for i in range(len(self.board)):
            column.append(self.board[i][c])
        return column

    def get_row(self, r):
        row = []
        for i in range(len(self.board)):
            row.append(self.board[r][i])
        return row

    def fill_column(self, column_index, column, reverse=False):
        for row in range(len(self.board)):
            self.board[row if not reverse else -1 - row][column_index] = \
                column[row if not reverse else -1 - row] if row < len(column) else 0

    def fill_row(self, row_index, row, reverse=False):
        for column in range(len(self.board)):
            self.board[row_index][column if not reverse else -1 - column] = \
                row[column if not reverse else -1 - column] if column < len(row) else 0

    def remove_zeros(self, l):
        _l = []
        for i in range(len(l)):
            if l[i] > 0:
                _l.append(l[i])
        return _l

    def sum_equals(self, l, reverse, score=False):
        if not l:
            return []

        if reverse:
            _l = [l[-1]]
            i = -2
            while i >= -len(l):
                if l[i] == l[i+1]:
                    _l[-1] *= 2
                    if score:
                        self.score += _l[-1]
                    i -= 1
                    if i >= -len(l):
                        _l.append(l[i])
                else:
                    _l.append(l[i])
                i -= 1
            _l.reverse()
            return _l
        else:
            _l = [l[0]]
            i = 1
            while i < len(l):
                if l[i] == l[i - 1]:
                    _l[-1] *= 2
                    if score:
                        self.score += _l[-1]
                    i += 1
                    if i < len(l):
                        _l.append(l[i])
                else:
                    _l.append(l[i])
                i += 1
            return _l
