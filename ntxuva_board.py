import numpy as np
import copy

class Ntxuva:
    def __init__(self, str=[], turn='X'):
        self.COLUMNS = 8
        self.ROWS = 4
        self.TIME_LIMIT = 2000
        self.INTERACTION = 0
        self.grid = np.full((self.ROWS,self.COLUMNS), 2)
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
        return self.winner() is not None or self.is_draw() or len(possible_moves)== 0

    def reset(self):
        self.__init__()

    
    def move(self, position):
        temp_grid = self.grid
        seeds_captured = 0

        if self.is_never_ending_move(position):
            return temp_grid, None, -1

        if temp_grid[tuple(position)] > 0:
            temp_seeds = 0

            if self.more_than_one_piece(position):
                if temp_grid[tuple(position)] > 1:
                    current_position = position
                    while True:
                        if temp_seeds == 0 and temp_grid[tuple(current_position)] == 1:
                            if self.is_attacking_position(current_position):
                                seeds_captured = self.capute(current_position, temp_grid)
                            self.grid = temp_grid
                            return temp_grid, True, seeds_captured

                        if temp_seeds == 0 and temp_grid[tuple(current_position)] > 0:
                            temp_seeds = temp_grid[tuple(current_position)]
                            temp_grid[tuple(current_position)] = 0

                        current_position = self.move_anticlockwise(current_position)
                        temp_grid[tuple(current_position)] = temp_grid[tuple(current_position)] + 1
                        temp_seeds = temp_seeds - 1
            else:
                if temp_grid[tuple(position)] > 0:
                    next_position = self.move_anticlockwise(position)
                    if temp_grid[tuple(next_position)] == 0:
                        if temp_seeds == 0 and temp_grid[tuple(position)] > 0:
                            temp_seeds = temp_grid[tuple(position)]
                            temp_grid[tuple(position)] = 0
                        position = self.move_anticlockwise(position)
                        temp_grid[tuple(position)] = temp_grid[tuple(position)] + 1
                        temp_seeds = temp_seeds - 1

                        if temp_seeds == 0 and  temp_grid[tuple(position)] == 1:
                            seeds_captured = self.capute(position, temp_grid)
                        self.grid = temp_grid
                        return temp_grid, True, seeds_captured
            self.grid = temp_grid
        return temp_grid, False, seeds_captured

    def get_next_board(self, position):
        next_board = copy.deepcopy(self)
        next_board.move(position)
        return next_board

    #@njit()
    def available_moves(self, turn):
        start = 0 if turn == 'X' else 2
        finish = 2 if turn == 'X' else self.ROWS

        sucessor = []

        if self.more_than_one_piece((start,0)):
            while start < finish:
                for j in range(self.COLUMNS):
                    if self.grid[tuple((start,j))] > 1:
                        if not self.is_never_ending_move((start,j)):
                            sucessor.append((start,j))
                start = start + 1
        else:
            while start < finish:
                for j in range(self.COLUMNS):
                    if self.grid[tuple((start, j))] != 0:
                        next_pos = self.move_anticlockwise((start, j))
                        if self.grid[tuple(next_pos)] == 0:
                            sucessor.append((start, j))
                start = start + 1
        return sucessor

   # @njit
    def is_never_ending_move(self, position):
        #temp_grid = copy.deepcopy(self.grid)
        #intial_grid = copy.deepcopy(self.grid)
        
        temp_grid = self.grid.copy()
        initial_grid = self.grid.copy()

        if temp_grid[tuple(position)] > 0:
            temp_seeds = 0
            if self.more_than_one_piece(position):
                if temp_grid[tuple(position)] > 1:
                    current_position = position
                    while True:
                        if temp_seeds == 0 and temp_grid[tuple(current_position)] == 1:
                            if self.is_attacking_position(current_position):
                                self.capute(current_position, temp_grid)
                            return False

                        if temp_seeds == 0 and temp_grid[tuple(current_position)] > 0:
                            temp_seeds = temp_grid[tuple(current_position)]
                            temp_grid[tuple(current_position)] = 0

                        current_position = self.move_anticlockwise(current_position)
                        temp_grid[tuple(current_position)] = temp_grid[tuple(current_position)] + 1
                        temp_seeds = temp_seeds - 1

                        pos_temp = current_position
                        pos_initial =  position

                        rsub = True
                        while True:
                            pos_initial = self.move_anticlockwise(pos_initial)
                            pos_temp = self.move_anticlockwise(pos_temp)
                            rsub = rsub and temp_grid[tuple(pos_temp)] == initial_grid[tuple(pos_initial)]
                            if pos_temp == current_position: break
                        if rsub:
                            return rsub
        return False

    def move_anticlockwise(self, position):
        i = position[0]
        j = position[1]

        if(i<2):
            j = j-1 if i == 0 else j+1
        else:
            j = j-1 if i == 2 else j+1

        if(j == -1):
            if(i<2):
                i = 1
            else:
                i = 3
            j = 0

        if(j == self.COLUMNS):
            if(i<2):
                i = 0
            else:
                i = 2
            j = self.COLUMNS - 1
        return tuple((i,j))

    def capute(self, position, board):
        total_score = 0
        i = position[0]
        j = position[1]

        if i==1:
            if board[2,j]>0:
                total_score = board[2,j] + board[3,j]
                board[2,j] = 0
                board[3,j] = 0
        else:
            if board[1, j] > 0:
                total_score = board[0, j] + board[1, j]
                board[0, j] = 0 
                board[1, j] = 0

        return total_score

    def more_than_one_piece(self, position):
        i = position[0]
        j = position[1]
        
        if i > 1:
            merged = np.concatenate((self.grid[2], self.grid[3]))
        else:
            merged = np.concatenate((self.grid[0], self.grid[1]))

        for k in range(len(merged)):
            if merged[k] > 1:
                return True
        return False

    def is_attacking_position(self, position):
        i = position[0]
        j = position[1]
        
        return True if i == 1 or i == 2 else False

    def make_key(self, turn):
        return "".join(map(str, (map(int, self.grid.flatten())))) + turn


    def is_valid_move(self, position):
        i = position[0]
        j = position[1]
        
        moves = self.available_moves(self.turn)
        return True if ((self.turn == 'X' and i < 2) or (self.turn == 'O' and i > 1)) and (i,j) in moves else False

    def give_reward(self):                          # Assign a reward for the player with mark X in the current board position.
        if self.over():
            if self.winner() is not None:
                if self.winner() == "X":
                    return 1.0                      # Player X won -> positive reward
                elif self.winner() == "O":
                    return -1.0                     # Player O won -> negative reward
            else:
                return 0.5                          # A smaller positive reward for cat's game
        else:
            return 0.0                              # No reward if the game is not yet finished


    def change_turn(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'


    def is_draw(self):
        side_x = np.concatenate(( self.grid[1], self.grid[0]))
        side_o = np.concatenate(( self.grid[3], self.grid[2]))

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
                board.grid, has_moved, seeds_captured = board.move(move_x[0])
                turn = 'O'
            else:
                move_o = board.available_moves('O')
                board.grid, has_moved, seeds_captured = board.move(move_o[0])
                turn = 'X'

            if seeds_captured > 0:
                is_draw = False

            i = i + 1
        return is_draw

    def flat_grid(self, turn='X'):
        available_move_x_position = self.available_moves(turn)[0]
        position_x = self.move_anticlockwise(available_move_x_position)
        array_x = [self.grid[tuple(available_move_x_position)]]
        while position_x != available_move_x_position:
            array_x.append(self.grid[tuple(position_x)])
            position_x = self.move_anticlockwise(position_x)
        return array_x

    def get_new_state_qs(self, turn):
        new_state_qs = []
        original_board = self.grid.copy()

        start = 0 if turn == 'X' else 2
        finish = 2 if turn == 'X' else self.ROWS

        while start < finish:
            for column in range(self.COLUMNS):
                
                new_board, moved, captured_stones = self.move((start, column))
                
                if not moved:
                    captured_stones = -1

                # means that the current position is an never ending move...
                if moved is None:
                    captured_stones = -10

                new_state_qs.append(round(captured_stones / 10,1))
                self.grid = original_board.copy()
            start += 1

        self.grid = original_board.copy()
        return new_state_qs
    
    def sum_pieces(self, turn):
        first_row, second_row = (0,1) if turn == 'X' else (2,3)
        return np.sum(np.concatenate((self.grid[first_row], self.grid[second_row])))
   
        




    
    
    
    