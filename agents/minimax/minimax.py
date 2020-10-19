from agents.qplayerandothers.players import ComputerPlayer
from gpu_methods.optimized_methods import more_than_one_piece,is_never_ending_move,move,move_anticlockwise
from agents.minimax.sucessor import Sucessor
import numpy as np
import copy
import sys

class Minimax (ComputerPlayer):

    def __init__(self, mark, prof=10):
        super(Minimax, self).__init__(mark=mark)
        self.mark = mark
        self.maxProf = prof
        self.sucessors = []
        self.good_moves = 0
        self.bad_moves = 0
        print (f" ====== Minimax is initialized with prof {self.maxProf} =======")

    def get_move(self, ntxuva):

        self.sucessors.clear()

        v = self.max_value(ntxuva, -sys.maxsize, sys.maxsize, True, 1)

        for s in self.sucessors:
            if s.utility == v:
                return s.position

        return None

    def max_value(self, ntxuva, alpha, beta, prim, prof):

        if  int(prof) > int(self.maxProf):

            return self.utility(ntxuva)

        prof = prof + 1

        v = -sys.maxsize

        for s in self.possible_moves(ntxuva, 'X'):

            v = np.max([v , self.min_value(s.board, alpha, beta, prof)])
            s.utility = v

            if prim:
                self.sucessors.append(s)

            if v >= beta:
                return v

            alpha = np.max([alpha, v])

        return v

    def min_value(self, ntxuva, alpha, beta, prof):

        if  int(prof) > int(self.maxProf):
            return self.utility(ntxuva)

        prof = prof + 1

        v = sys.maxsize

        for s in self.possible_moves(ntxuva, 'O'):

            v = np.min([v,self.max_value(s.board, alpha, beta, False, prof)])
            s.utility = v

            if v <= alpha:
                return v

            beta = np.min([beta, v])

        return v

    def terminal_test(self, ntxuva):
        return False

    def utility(self, ntxuva):
        pc, usr = 0, 0

        pc = ntxuva.sum_pieces('O')
        usr = ntxuva.sum_pieces('X')
        return usr - pc

    def possible_moves(self, ntxuva, turn):
        start = 0 if turn == 'X' else 2
        finish = 2 if turn == 'X' else ntxuva.ROWS

        sucessor = []
        temp_ntxuva = copy.deepcopy(ntxuva)

        if more_than_one_piece((start, 0),ntxuva.grid):
            while start < finish:
                for j in range(ntxuva.COLUMNS):
                    ntxuva = copy.deepcopy(temp_ntxuva)
                    if ntxuva.grid[tuple((start, j))] > 1:
                        if not is_never_ending_move((start, j), ntxuva.grid):
                            move((start, j),ntxuva.grid)
                            sucessor.append(Sucessor(ntxuva, (start, j)))
                start = start + 1
        else:
            while start < finish:
                for j in range(ntxuva.COLUMNS):
                    ntxuva = copy.deepcopy(temp_ntxuva)
                    if ntxuva.grid[tuple((start, j))] != 0:
                        next_pos = move_anticlockwise((start, j))
                        if ntxuva.grid[tuple(next_pos)] == 0:
                            move((start, j),ntxuva.grid)
                            sucessor.append(Sucessor(ntxuva, (start, j)))
                start = start + 1
        ntxuva = temp_ntxuva
        return sucessor