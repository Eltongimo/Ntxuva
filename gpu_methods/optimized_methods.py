from numba import njit
import numpy as np
import copy
from agents.minimax.sucessor import Sucessor

@njit
def move_anticlockwise(position):
    i = position[0]
    j = position[1]

    if (i < 2):
        j = j - 1 if i == 0 else j + 1
    else:
        j = j - 1 if i == 2 else j + 1

    if (j == -1):
        if (i < 2):
            i = 1
        else:
            i = 3
        j = 0

    if (j == 8):
        if (i < 2):
            i = 0
        else:
            i = 2
        j = 8 - 1
    return tuple((i, j))


@njit
def capute(position, board):
    total_score = 0
    i = position[0]
    j = position[1]

    if i == 1:
        if board[2, j] > 0:
            total_score = board[2, j] + board[3, j]
            board[2, j] = 0
            board[3, j] = 0
    else:
        if board[1, j] > 0:
            total_score = board[0, j] + board[1, j]
            board[0, j] = 0
            board[1, j] = 0

    return total_score

@njit
def is_attacking_position(position):
    i = position[0]
    j = position[1]
    return True if i == 1 or i == 2 else False

@njit
def more_than_one_piece(position, grid):
    i = position[0]
    j = position[1]

    if i > 1:
        merged = np.concatenate((grid[2],grid[3]))
    else:
        merged = np.concatenate((grid[0],grid[1]))

    for k in range(len(merged)):
        if merged[k] > 1:
            return True
    return False

@njit
def move(position, grid):
    temp_grid =  grid
    seeds_captured = 0

    if  is_never_ending_move(position, grid):
        return temp_grid, False, -1

    if temp_grid[tuple(position)] > 0:
        temp_seeds = 0

        if  more_than_one_piece(position, grid):
            if temp_grid[tuple(position)] > 1:
                current_position = position
                while True:
                    if temp_seeds == 0 and temp_grid[tuple(current_position)] == 1:
                        if  is_attacking_position(current_position):
                            seeds_captured = capute(current_position, temp_grid)
                        grid = temp_grid
                        return temp_grid, True, seeds_captured

                    if temp_seeds == 0 and temp_grid[tuple(current_position)] > 0:
                        temp_seeds = temp_grid[tuple(current_position)]
                        temp_grid[tuple(current_position)] = 0

                    current_position =  move_anticlockwise(current_position)
                    temp_grid[tuple(current_position)] = temp_grid[tuple(current_position)] + 1
                    temp_seeds = temp_seeds - 1
        else:
            if temp_grid[tuple(position)] > 0:
                next_position =  move_anticlockwise(position)
                if temp_grid[tuple(next_position)] == 0:
                    if temp_seeds == 0 and temp_grid[tuple(position)] > 0:
                        temp_seeds = temp_grid[tuple(position)]
                        temp_grid[tuple(position)] = 0
                    position =  move_anticlockwise(position)
                    temp_grid[tuple(position)] = temp_grid[tuple(position)] + 1
                    temp_seeds = temp_seeds - 1

                    if temp_seeds == 0 and temp_grid[tuple(position)] == 1:
                        seeds_captured = capute(position, temp_grid)
                    grid = temp_grid
                    return temp_grid, True, seeds_captured
        grid = temp_grid
    return temp_grid, False, seeds_captured

@njit
def is_never_ending_move(position, grid):
    temp_grid = grid.copy()
    initial_grid = grid.copy()

    if temp_grid[tuple(position)] > 0:
        temp_seeds = 0
        if more_than_one_piece(position, grid):
            if temp_grid[tuple(position)] > 1:
                current_position = position
                while True:
                    if temp_seeds == 0 and temp_grid[tuple(current_position)] == 1:
                        if is_attacking_position(current_position):
                            capute(current_position, temp_grid)
                        return False

                    if temp_seeds == 0 and temp_grid[tuple(current_position)] > 0:
                        temp_seeds = temp_grid[tuple(current_position)]
                        temp_grid[tuple(current_position)] = 0

                    current_position = move_anticlockwise(current_position)
                    temp_grid[tuple(current_position)] = temp_grid[tuple(current_position)] + 1
                    temp_seeds = temp_seeds - 1

                    pos_temp = current_position
                    pos_initial =  position

                    rsub = True
                    while True:
                        pos_initial = move_anticlockwise(pos_initial)
                        pos_temp = move_anticlockwise(pos_temp)
                        rsub = rsub and temp_grid[tuple(pos_temp)] == initial_grid[tuple(pos_initial)]
                        if pos_temp == current_position:
                            break
                    if rsub:
                        # This is an never ending move
                        return rsub
    return False

@njit
def possible_moves(board, turn):
    start = 0 if turn == 'X' else 2
    finish = 2 if turn == 'X' else 8


    board_sucessor = ([board.copy()])
    position_sucessor = [tuple((-1,-1))]

    temp_ntxuva = board.copy()

    if  more_than_one_piece((start, 0), board):
        while start < finish:
            for j in range(8):
                board = temp_ntxuva.copy()
                if board[tuple((start, j))] > 1:
                    if not is_never_ending_move((start, j), board):
                        move((start, j), board)
                        board_sucessor.append(board)
                        position_sucessor.append((start,j))
            start = start + 1
    else:
        while start < finish:
            for j in range(8):
                board = temp_ntxuva.copy()
                if board[tuple((start, j))] != 0:
                    next_pos = move_anticlockwise((start, j))
                    if board[tuple(next_pos)] == 0:
                        move((start, j),board)
                        board_sucessor.append(board)
                        position_sucessor.append((start,j))
            start = start + 1
    board = temp_ntxuva
    return board_sucessor, position_sucessor