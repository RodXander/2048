__author__ = 'RodXander'


class GameOver(BaseException):
    def __str__(self):
        return "Game over"


class InvalidParam(BaseException):
    def __init__(self, wrong_param):
        self.wrong_param = wrong_param

    def __str__(self):
        return str.format("Invalid param {0}, it must be 'n', 'e', 's' or 'w'.", self.wrong_param)


class GameFinished(BaseException):
    def __str__(self):
        return "Game finished"