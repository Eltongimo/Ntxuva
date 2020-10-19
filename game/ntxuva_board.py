import numpy as np
import copy
from gpu_methods.optimized_methods import *


class Ntxuva:
    def __init__(self, str=[], turn='X'):
        self.COLUMNS = 8
        self.ROWS = 4
        self.grid = np.full((self.ROWS, self.COLUMNS), 2)
        self.turn = turn

    def winner(self):
        side_x = np.concatenate((self.grid[0], self.grid[1]))
        side_o = np.concatenate((self.grid[2], self.grid[3]))

        if len([data for data in side_x if data != 0]) == 0:
            return 'O'
        elif len([data for data in side_o if data != 0]) == 0:
            return 'X'

    def over(self):
        possible_moves = self.available_moves(self.turn)
        return self.winner() is not None or self.is_draw() or len(possible_moves) == 0

    def get_next_board(self, position):
        next_board = copy.deepcopy(self)
        next_board.move(position)
        return next_board

    def available_moves(self, turn):
        start = 0 if turn == 'X' else 2
        finish = 2 if turn == 'X' else self.ROWS
        sucessor = []
        if more_than_one_piece((start, 0), self.grid):
            while start < finish:
                for j in range(self.COLUMNS):
                    if self.grid[tuple((start, j))] > 1:
                        if not is_never_ending_move((start, j), self.grid):
                            sucessor.append((start, j))
                start = start + 1
        else:
            while start < finish:
                for j in range(self.COLUMNS):
                    if self.grid[tuple((start, j))] != 0:
                        next_pos = move_anticlockwise((start, j))
                        if self.grid[tuple(next_pos)] == 0:
                            sucessor.append((start, j))
                start = start + 1
        return sucessor

    def make_key(self, turn=None):
        return "".join(map(str, (map(int, self.grid.flatten()))))

    def is_valid_move(self, position):

        i = position[0]
        j = position[1]
        moves = self.available_moves(self.turn)
        return True if ((self.turn == 'X' and i < 2) or (self.turn == 'O' and i > 1)) and (i, j) in moves else False


    def change_turn(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'

    def is_draw(self):
        side_x = np.concatenate((self.grid[1], self.grid[0]))
        side_o = np.concatenate((self.grid[3], self.grid[2]))

        is_draw = False
        if len(self.available_moves('X')) == 1 and len(self.available_moves('O')) == 1:

            turn = 'O' if self.turn == 'X' else 'X'
            board = copy.deepcopy(self)

            if np.sum(side_x) == 4 and np.sum(side_o) == 4:
                is_draw = self.is_draw_method(board, turn)
            elif np.sum(side_x) == 6 and np.sum(side_o) == 6:
                is_draw = self.is_draw_method(board, turn)
            elif np.sum(side_x) == 5 and np.sum(side_o) == 5:
                is_draw = self.is_draw_method(board, turn)
            elif np.sum(side_x) == 7 and np.sum(side_o) == 7:
                is_draw = self.is_draw_method(board, turn)
            elif np.sum(side_x) == 8 and np.sum(side_o) == 8:
                is_draw = self.is_draw_method(board, turn)
            elif np.sum(side_x) == 9 and np.sum(side_o) == 9:
                is_draw = self.is_draw_method(board, turn)
            elif np.sum(side_x) == 10 and np.sum(side_o) == 10:
                is_draw = self.is_draw_method(board, turn)
            elif (np.sum(side_x) == 10 and np.sum(side_o) == 4) or (np.sum(side_x) == 4 and np.sum(side_o) == 10):
                is_draw = self.is_draw_method(board, turn)
            elif (np.sum(side_x) == 10 and np.sum(side_o) == 6) or (np.sum(side_x) == 6 and np.sum(side_o) == 10):
                is_draw = self.is_draw_method(board, turn)
            elif (np.sum(side_x) == 10 and np.sum(side_o) == 7) or (np.sum(side_x) == 7 and np.sum(side_o) == 10):
                is_draw = self.is_draw_method(board, turn)
            elif (np.sum(side_x) == 9 and np.sum(side_o) == 10) or (np.sum(side_x) == 10 and np.sum(side_o) == 9):
                is_draw = self.is_draw_method(board, turn)
            elif (np.sum(side_x) == 7 and np.sum(side_o) == 9) or (np.sum(side_x) == 9 and np.sum(side_o) == 7):
                is_draw = self.is_draw_method(board, turn)
            elif (np.sum(side_x) == 1 and np.sum(side_o) == 7) or (np.sum(side_x) == 7 and np.sum(side_o) == 1):
                is_draw = self.is_draw_method(board, turn)
            elif (np.sum(side_x) == 1 and np.sum(side_o) == 9) or (np.sum(side_x) == 9 and np.sum(side_o) == 1):
                is_draw = self.is_draw_method(board, turn)
            elif (np.sum(side_x) == 1 and np.sum(side_o) == 10) or (np.sum(side_x) == 10 and np.sum(side_o) == 1):
                is_draw = self.is_draw_method(board, turn)
            elif (np.sum(side_x) == 10 and np.sum(side_o) == 8) or (np.sum(side_x) == 8 and np.sum(side_o) == 10):
                is_draw = self.is_draw_method(board, turn)
            else:
                is_draw = self.is_draw_method(board, turn)
        return is_draw

    def is_draw_method(self, board, turn):
        is_draw = True
        i = 0
        while i < 100 and is_draw:
            if turn == 'X':
                move_x = board.available_moves('X')
                board.grid, has_moved, seeds_captured = move(move_x[0], board.grid)
                turn = 'O'
            else:
                move_o = board.available_moves('O')
                board.grid, has_moved, seeds_captured = move(move_o[0], board.grid)
                turn = 'X'

            if seeds_captured > 0:
                is_draw = False

            i = i + 1
        return is_draw

    def get_new_state_qs(self, turn):
        new_state_qs = []
        original_board = self.grid.copy()

        start = 0 if turn == 'X' else 2
        finish = 2 if turn == 'X' else self.ROWS

        while start < finish:
            for column in range(self.COLUMNS):

                new_board, moved, captured_stones = move((start, column),original_board)

                if not moved:
                    captured_stones = -1

                # means that the current position is an never ending move...
                if moved is None:
                    captured_stones = -10

                new_state_qs.append(round(captured_stones / 10, 1))
                self.grid = original_board.copy()
            start += 1

        self.grid = original_board.copy()
        return new_state_qs

    def sum_pieces(self, turn):
        first_row, second_row = (0, 1) if turn == 'X' else (2, 3)
        return np.sum(np.concatenate((self.grid[first_row], self.grid[second_row])))


