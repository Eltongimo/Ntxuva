import  sys

class Sucessor:

    def __init__(self, ntxuva, position):
        self.board = ntxuva
        self.position = position
        self.utility = -sys.maxsize